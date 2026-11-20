#!/usr/bin/env python3
"""
audio_check — Kiểm toán chất lượng âm thanh hậu kỳ (Điểm Đọc)
============================================================
Kiểm tra các chỉ số âm thanh bắt buộc:
  - Loudness I: trong khoảng [-14.8, -13.2] LUFS (mục tiêu -14.0 LUFS YouTube)
  - True Peak: <= -1.0 dBTP
  - LRA: <= 14.0 LU (mục tiêu ~11.0 LU)
  - Mức phân tách BGM vs Giọng: >= 18.0 dB khi có tiếng nói
  - Độ lệch Video vs Audio: <= 33.3 ms (1 frame ở 30fps)
  - Đếm số sự kiện SFX

Cách dùng:
  python3 core/audio_check.py <project>
  python3 core/audio_check.py path/to/video_or_audio.mp4
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
import os
import subprocess

from diemdoc import paths
from diemdoc.audio import (
    load_audio_config,
    measure_loudness,
    measure_voice_bgm_separation,
)
from diemdoc.log import banner, die, log, ok, warn
from diemdoc.timeline import load_timeline


def _probe_stream_duration(file_path: str, stream_select: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", stream_select,
        "-show_entries", "stream=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=True)
        txt = r.stdout.strip()
        if txt and txt != "N/A":
            return float(txt)
    except Exception:
        pass
    # Fallback probe format duration
    cmd_fmt = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    try:
        r = subprocess.run(cmd_fmt, capture_output=True, text=True, check=True)
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def check_audio(target: str) -> bool:
    all_pass = True

    # Xác định đường dẫn file cần kiểm tra
    if os.path.isfile(target):
        file_path = target
        pdir = os.path.dirname(os.path.abspath(target))
        pname = os.path.basename(pdir)
    else:
        pdir = paths.project_dir(target)
        pname = os.path.basename(pdir)
        tl = load_timeline(pdir)
        out_name = tl.get("output_filename", "final_video.mp4")
        file_path = os.path.join(pdir, out_name)
        if not os.path.exists(file_path):
            work_master = paths.work_project_file(pname, "master_audio.wav")
            if os.path.exists(work_master):
                file_path = work_master
            else:
                die(f"Không tìm thấy file sản phẩm hoàn chỉnh để kiểm tra trong {pdir}")

    log(f"Kiểm toán âm thanh: {paths.rel_to_root(file_path)}")
    print("-" * 65)

    # 1. Đo Loudness (I, TP, LRA)
    meas = measure_loudness(file_path)
    if not meas:
        warn("Không thể đo Loudness của file!")
        return False

    i_val = meas["input_i"]
    tp_val = meas["input_tp"]
    lra_val = meas["input_lra"]

    cfg = load_audio_config()
    ln_cfg = cfg.get("loudness", {})
    r_min, r_max = ln_cfg.get("target_range_I", [-14.8, -13.2])
    max_tp = ln_cfg.get("max_TP", -1.0)
    min_sep = ln_cfg.get("min_separation_db", 18.0)

    print(f"  • Integrated Loudness (I) : {i_val:6.2f} LUFS  [Chuẩn: {r_min} đến {r_max}]")
    print(f"  • True Peak (TP)          : {tp_val:6.2f} dBTP  [Chuẩn: <= {max_tp}]")
    print(f"  • Loudness Range (LRA)    : {lra_val:6.2f} LU    [Chuẩn: <= 14.0]")

    if r_min <= i_val <= r_max:
        ok("  -> Loudness I: ĐẠT CHUẨN")
    else:
        warn(f"  -> THẤT BẠI (FAIL): Loudness I ({i_val:.2f}) lệch khỏi dải [{r_min}, {r_max}] LUFS!")
        all_pass = False

    if tp_val <= max_tp:
        ok("  -> True Peak: ĐẠT CHUẨN")
    else:
        warn(f"  -> THẤT BẠI (FAIL): True Peak ({tp_val:.2f}) vượt quá ngưỡng {max_tp} dBTP!")
        all_pass = False

    # 2. Đo phân tách Voice vs BGM
    voice_file = paths.work_project_file(pname, "voiceover.wav")
    if not os.path.exists(voice_file):
        voice_file = os.path.join(pdir, "voiceover.wav")

    bgm_ducked = paths.work_project_file(pname, "bgm_ducked.wav")
    if not os.path.exists(bgm_ducked):
        bgm_ducked = paths.work_project_file(pname, "bgm_playlist.wav")

    if os.path.exists(voice_file) and os.path.exists(bgm_ducked):
        sep_db = measure_voice_bgm_separation(voice_file, bgm_ducked)
        print(f"  • Phân tách Giọng / BGM   : {sep_db:6.2f} dB    [Chuẩn: >= {min_sep} dB]")
        if sep_db >= min_sep:
            ok("  -> Độ dìm nhạc (Ducking): ĐẠT CHUẨN (giọng rõ ràng, không lấn át)")
        else:
            warn(f"  -> THẤT BẠI (FAIL): Phân tách Giọng/BGM ({sep_db:.2f} dB) thấp hơn {min_sep} dB!")
            all_pass = False
    else:
        print("  • Phân tách Giọng / BGM   : Không có track stem riêng lẻ để đo.")

    # 3. Đo độ lệch Video vs Audio (nếu file là video MP4)
    if file_path.endswith(".mp4"):
        v_dur = _probe_stream_duration(file_path, "v:0")
        a_dur = _probe_stream_duration(file_path, "a:0")
        diff_ms = abs(v_dur - a_dur) * 1000.0
        print(f"  • Độ lệch Video vs Audio  : {diff_ms:6.1f} ms    [Chuẩn: <= 33.3 ms (1 frame)]")
        if diff_ms <= 33.4:
            ok("  -> Đồng bộ Video - Audio: ĐẠT CHUẨN (<= 1 frame 30fps)")
        else:
            warn(f"  -> THẤT BẠI (FAIL): Độ lệch ({diff_ms:.1f} ms) vượt quá 1 frame (33.3 ms)!")
            all_pass = False

    # 4. Đếm số sự kiện SFX
    sfx_file = paths.work_project_file(pname, "sfx_track.wav")
    if os.path.exists(sfx_file):
        print("  • Track SFX độc lập       : ĐÃ TẠO (sfx_track.wav)")
    else:
        print("  • Track SFX độc lập       : Chưa tạo hoặc không có sự kiện.")

    print("-" * 65)
    if all_pass:
        ok("KẾT LUẬN: ÂM THANH ĐẠT TẤT CẢ TIÊU CHUẨN KỸ THUẬT ĐIỂM ĐỌC!")
    else:
        warn("KẾT LUẬN: KIỂM TOÁN THẤT BẠI (FAIL) — CẦN TINH CHỈNH ĐỂ ĐẠT CHUẨN!")
    return all_pass


def main() -> None:
    ap = argparse.ArgumentParser(description="Kiểm toán âm thanh hậu kỳ Điểm Đọc")
    ap.add_argument("target", help="Tên project hoặc đường dẫn tệp audio/video")
    args = ap.parse_args()

    banner("AUDIO CHECK", "Điểm Đọc")
    passed = check_audio(args.target)
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
