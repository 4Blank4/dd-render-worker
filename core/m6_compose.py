#!/usr/bin/env python3
"""
m6 — COMPOSE (Nối cảnh 'cut', âm thanh master liên tục & loudnorm cho Điểm Đọc)
=============================================================================
Quy tắc bất biến:
  1. Không dùng xfade video giữa các cảnh khi có voiceover liên tục (tránh lệch sync).
  2. Mặc định là "cut": nối bằng ffmpeg concat demuxer (-c copy).
  3. Âm thanh cuối luôn dựng MỘT LẦN từ voiceover.wav liên tục (không ghép theo cảnh).
  4. Ducking bằng sidechaincompress (voice làm sidechain).
  5. Loudnorm hai lượt chuẩn YouTube: I trong [-14.8, -13.2] LUFS, TP <= -1.0 dBTP.
  6. Mux: -c:v copy, -c:a aac -b:a 192k, -movflags +faststart.
  7. Độ lệch video vs audio <= 1 frame (33 ms).

Cách dùng:
  python3 core/m6_compose.py <project>
  python3 core/m6_compose.py <project> --bgm-pool sports_hype
  python3 core/m6_compose.py <project> --no-loudness
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import glob
import json
import math
import os
import subprocess

from diemdoc import paths
from diemdoc.audio import (
    apply_sidechain_ducking,
    build_bgm_playlist,
    build_sfx_track,
    load_audio_config,
    measure_loudness,
    measure_voice_bgm_separation,
    mix_master_audio,
    two_pass_loudnorm,
)
from diemdoc.jsonio import load_json
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.timeline import load_timeline


def _probe_stream(file_path: str, select: str = "v:0") -> dict:
    """Trích xuất thông số kỹ thuật chi tiết của stream."""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", select,
        "-show_entries", "stream=codec_name,width,height,r_frame_rate,duration",
        "-show_entries", "format=duration",
        "-of", "json", file_path,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(r.stdout)
    except Exception:
        return {}


def _get_duration(path: str) -> float:
    data = _probe_stream(path)
    streams = data.get("streams", [])
    if streams and "duration" in streams[0]:
        try:
            return float(streams[0]["duration"])
        except ValueError:
            pass
    fmt = data.get("format", {})
    if "duration" in fmt:
        try:
            return float(fmt["duration"])
        except ValueError:
            pass
    return 0.0


def stitch_scenes_cut(scene_files: list[str], out_video: str) -> bool:
    """Nối thẳng các cảnh bằng concat demuxer (cực nhanh, không re-encode)."""
    if not scene_files:
        return False

    if len(scene_files) == 1:
        import shutil
        shutil.copy2(scene_files[0], out_video)
        return True

    # Xác nhận các cảnh cùng tham số (codec, resolution)
    base_info = _probe_stream(scene_files[0], "v:0")
    b_stream = (base_info.get("streams") or [{}])[0]
    b_codec = b_stream.get("codec_name")
    b_w = b_stream.get("width")
    b_h = b_stream.get("height")

    for f in scene_files[1:]:
        info = _probe_stream(f, "v:0")
        s = (info.get("streams") or [{}])[0]
        if s.get("codec_name") != b_codec or s.get("width") != b_w or s.get("height") != b_h:
            warn(f"Cảnh {os.path.basename(f)} khác tham số ({s.get('width')}x{s.get('height')}) so với cảnh gốc ({b_w}x{b_h})! Cần re-encode.")
            return _stitch_reencode(scene_files, out_video)

    list_file = out_video + ".concat.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for fp in scene_files:
            safe = fp.replace("'", "'\\''")
            f.write(f"file '{safe}'\n")

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", list_file,
        "-c", "copy", out_video,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        os.remove(list_file)
    except OSError:
        pass

    if r.returncode != 0:
        warn(f"Concat copy thất bại ({r.stderr[-200:]}), thử re-encode...")
        return _stitch_reencode(scene_files, out_video)

    return True


def _stitch_reencode(scene_files: list[str], out_video: str) -> bool:
    list_file = out_video + ".concat_reenc.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for fp in scene_files:
            safe = fp.replace("'", "'\\''")
            f.write(f"file '{safe}'\n")

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", list_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", out_video,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        os.remove(list_file)
    except OSError:
        pass
    return r.returncode == 0


def compose_project(project_name: str, bgm_pool: str | None = None,
                    no_loudness: bool = False, output_file: str | None = None) -> str:
    """Thực hiện trọn gói pipeline m6 compose cho project."""
    pdir = paths.project_dir(project_name)
    wdir = paths.work_project_dir(project_name)
    tl = load_timeline(pdir)

    # 1. Tìm danh sách file cảnh
    # Ưu tiên scenes_out trong WORK, sau đó tới project_dir
    scenes_dir = paths.work_project_file(project_name, "scenes_out")
    if not os.path.exists(scenes_dir) or not glob.glob(os.path.join(scenes_dir, "scene_*.mp4")):
        scenes_dir = os.path.join(pdir, "scenes_out")

    scene_files = sorted(glob.glob(os.path.join(scenes_dir, "scene_*.mp4")))
    single_full = os.path.join(pdir, tl.get("output_filename", "final_video.mp4"))

    # Đích cuối cùng
    final_name = output_file or tl.get("output_filename") or "final_video.mp4"
    if not final_name.endswith(".mp4"):
        final_name += ".mp4"
    final_path = os.path.join(pdir, final_name)

    step("Nối video (Cut Concat)")
    video_stitched = os.path.join(wdir, "video_stitched.mp4")

    if scene_files:
        log(f"Tìm thấy {len(scene_files)} cảnh trong {paths.rel_to_root(scenes_dir)}.")
        ok_stitch = stitch_scenes_cut(scene_files, video_stitched)
        if not ok_stitch or not os.path.exists(video_stitched):
            die("Nối cảnh video thất bại.")
    elif os.path.exists(single_full):
        log(f"Không có scenes_out riêng lẻ, sử dụng video đầy đủ có sẵn: {paths.rel_to_root(single_full)}")
        import shutil
        shutil.copy2(single_full, video_stitched)
    else:
        die(f"Không tìm thấy cảnh nào để ghép trong {scenes_dir} hoặc {single_full}")

    v_duration = _get_duration(video_stitched)
    ok(f"Video đã ghép xong: {v_duration:.3f}s")

    # 2. Xử lý âm thanh liên tục (Master Audio Pipeline)
    step("Xử lý âm thanh Master liên tục")
    # Tìm voiceover.wav trong WORK hoặc project
    voice_candidates = [
        paths.work_project_file(project_name, "voiceover.wav"),
        paths.work_project_file(os.path.basename(project_name), "voiceover.wav"),
        os.path.join(pdir, "voiceover.wav"),
        paths.work_file(os.path.basename(pdir), "voiceover.wav")
    ]
    voice_wav = None
    for cand in voice_candidates:
        if os.path.exists(cand) and os.path.getsize(cand) > 1000:
            voice_wav = cand
            break

    if not voice_wav:
        die(f"LỖI BẮT BUỘC (NO VOICEOVER): Không tìm thấy voiceover.wav trong WORK ({paths.work_project_dir(project_name)}) hay ({pdir})! Bắt buộc phải có lời thoại BLV để dựng video Điểm Đọc. Hãy chạy m3_voice trước!")

    v_voice_dur = _get_duration(voice_wav)
    log(f"Voiceover master: {paths.rel_to_root(voice_wav)} ({v_voice_dur:.3f}s)", tag="voice")

    audio_cfg = load_audio_config()
    target_pool = bgm_pool or tl.get("bgm_pool") or audio_cfg.get("bgm_transition", {}).get("default_pool", "sports_modern")

    master_audio_wav = os.path.join(wdir, "master_audio.wav")
    num_sfx = 0
    sep_db = 0.0

    # A. Dựng SFX Track
    sfx_wav = os.path.join(wdir, "sfx_track.wav")
    sfx_path, num_sfx = build_sfx_track(tl, v_duration, sfx_wav, config=audio_cfg)
    if sfx_path:
        log(f"Dựng xong SFX Track: {num_sfx} sự kiện âm thanh.")

    # B. Dựng BGM Playlist (acrossfade)
    bgm_raw = os.path.join(wdir, "bgm_playlist.wav")
    bgm_path = build_bgm_playlist(v_duration, bgm_raw, pool_name=target_pool, config=audio_cfg)
    if bgm_path:
        log(f"Dựng xong BGM Track từ pool '{target_pool}': {v_duration:.2f}s.")

    # C. Ducking thật qua sidechaincompress (voice làm sidechain)
    bgm_ducked = os.path.join(wdir, "bgm_ducked.wav")
    if bgm_path and apply_sidechain_ducking(voice_wav, bgm_path, bgm_ducked, config=audio_cfg):
        log("Áp dụng sidechain ducking thành công.")
        sep_db = measure_voice_bgm_separation(voice_wav, bgm_ducked)
        log(f"Độ phân tách Giọng / Ducked BGM: {sep_db:.1f} dB (Mục tiêu >= 18 dB).")
        used_bgm = bgm_ducked
    else:
        used_bgm = bgm_path

    # D. Mix Master Audio + Two-Pass Loudnorm
    step("Mix & Chuẩn hoá Loudnorm 2 lượt")
    ok_mix = mix_master_audio(voice_wav, used_bgm, sfx_path, master_audio_wav,
                              duration=v_duration, config=audio_cfg)
    if not ok_mix or not os.path.exists(master_audio_wav):
        die("Trộn âm thanh master thất bại.")

    # 3. Mux Video + Audio
    step("Mux xuất bản video hoàn chỉnh")
    cmd_mux = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", video_stitched,
        "-i", master_audio_wav,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
        "-t", str(v_duration),
        "-movflags", "+faststart",
        final_path,
    ]
    r_mux = subprocess.run(cmd_mux, capture_output=True, text=True)
    if r_mux.returncode != 0:
        die(f"Mux video thất bại: {r_mux.stderr[-250:]}")

    # 4. Kiểm tra độ lệch video vs audio & Loudness nghiệm thu
    v_end = _get_duration(final_path)
    a_end = _get_duration(master_audio_wav)
    diff_ms = abs(v_end - a_end) * 1000.0

    print()
    log("=== NGHIỆM THU KỸ THUẬT (AUDIO/VIDEO QA) ===")
    log(f"Thời lượng Video: {v_end:.3f} s")
    log(f"Thời lượng Audio: {a_end:.3f} s")
    log(f"Độ lệch Video vs Audio: {diff_ms:.1f} ms ({diff_ms / 33.33:.2f} frames)")

    if diff_ms <= 34.0:
        ok("Đạt chuẩn đồng bộ: Độ lệch <= 1 frame (33.3 ms)!")
    else:
        warn(f"CẢNH BÁO ĐỒNG BỘ: Độ lệch {diff_ms:.1f} ms vượt quá 1 frame!")

    meas = measure_loudness(final_path)
    if meas:
        i_val = meas["input_i"]
        tp_val = meas["input_tp"]
        lra_val = meas["input_lra"]
        log(f"Loudness cuối: I = {i_val:.1f} LUFS | TP = {tp_val:.1f} dBTP | LRA = {lra_val:.1f} LU")
        if -14.8 <= i_val <= -13.2 and tp_val <= -1.0:
            ok("Loudness ĐẠT CHUẨN YouTube [-14.8, -13.2] LUFS và TP <= -1.0 dBTP!")
        else:
            warn("Loudness nằm ngoài dải khuyến nghị.")

    if voice_wav and sep_db > 0:
        if sep_db >= 18.0:
            ok(f"Độ phân tách Giọng / BGM: {sep_db:.1f} dB (>= 18 dB ĐẠT CHUẨN)")
        else:
            warn(f"Độ phân tách Giọng / BGM: {sep_db:.1f} dB (< 18 dB)")

    ok(f"Hoàn thành m6! File xuất: {paths.rel_to_root(final_path)}")
    return final_path


def main() -> None:
    ap = argparse.ArgumentParser(description="m6 — Compose & Master Audio cho Điểm Đọc")
    ap.add_argument("project", help="Tên hoặc đường dẫn project")
    ap.add_argument("--bgm-pool", default=None, help="BGM pool chỉ định (sports_modern, sports_hype...)")
    ap.add_argument("--no-loudness", action="store_true", help="Bỏ qua chuẩn hoá loudness")
    ap.add_argument("--output", default=None, help="Tên file video đầu ra")
    args = ap.parse_args()

    banner("M6 — COMPOSE & AUDIO MASTER", "Điểm Đọc")
    compose_project(args.project, bgm_pool=args.bgm_pool,
                    no_loudness=args.no_loudness, output_file=args.output)


if __name__ == "__main__":
    main()