#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_daily_19_11_video.py — Pha 2 (Bước 2):
Render toàn bộ video 16:9 HTML v2 (tin_00_intro_long.mp4 + tin_01..18_long.mp4 @ 1920x1080 30fps),
ghép Cut-Concat với logo/Intro.mp4 và logo/Outro.mp4, trộn nhạc nền liên tục
và chuẩn hóa EBU R128 (-14.0 LUFS, TP <= -1.0 dBTP) ra outputs/19.11.2026/Tin-The-Thao-19-11.mp4.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse
import concurrent.futures
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
if os.path.join(_ROOT, "engines", "html") not in sys.path:
    sys.path.insert(0, os.path.join(_ROOT, "engines", "html"))

from diemdoc import paths
from diemdoc.audio import measure_loudness, two_pass_loudnorm
from diemdoc.log import banner, die, ok, step
from m8_news_bridge import export_bridge_project
from renderer import render_html_engine

DAY_STR = "19.11.2026"
ROOT = Path(_ROOT)
DAY_DIR = ROOT / "outputs" / DAY_STR
PREVIEW_DIR = DAY_DIR / "_preview_v2"
WORK_ROOT = Path(paths.WORK) / "daily_1911_video"
INTRO_STAGE_DAY = Path(paths.WORK) / "daily_1911_intro_stage" / DAY_STR
HTML_BRIDGES_DIR = WORK_ROOT / "bridges"
NORM_DIR = WORK_ROOT / "norm_segments"

VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS = 30
TARGET_TIMESCALE = "15360"


def probe_duration(path: Path) -> float:
    """Đo thời lượng thực tế của file video/audio bằng ffprobe."""
    res = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(res.stdout.strip())


def probe_stream_duration(path: Path, stream_selector: str = "v:0") -> float:
    """Đo thời lượng thực tế của một stream cụ thể (v:0 hoặc a:0) bằng ffprobe."""
    res = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            stream_selector,
            "-show_entries",
            "stream=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(res.stdout.strip().splitlines()[0])


def prepare_intro_stage(intro_obj: Dict[str, Any], news_objs: List[Dict[str, Any]]) -> Path:
    """Dựng thư mục tạm cho Intro (id=0) ngoài Drive để tái sử dụng m8_news_bridge."""
    INTRO_STAGE_DAY.mkdir(parents=True, exist_ok=True)
    for name in ("images", "image_plan.json", "image_credits.json", "audio", "audio-title"):
        src = DAY_DIR / name
        dst = INTRO_STAGE_DAY / name
        if dst.is_symlink() or dst.exists():
            if dst.is_symlink() or dst.is_file():
                dst.unlink()
            else:
                shutil.rmtree(dst)
        os.symlink(src, dst)

    staged_items = [intro_obj] + news_objs
    (INTRO_STAGE_DAY / "thethao.json").write_text(
        json.dumps(staged_items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return INTRO_STAGE_DAY


def prepare_bridge_project(
    day_dir_for_bridge: str,
    item_id: int,
    dest_mp4: Path,
    bridge_subdir: str,
    global_offset_sec: float,
    force: bool = False,
) -> Optional[str]:
    """Xuất bridge timeline tuần tự (tránh load Whisper song song) và tắt BGM cục bộ."""
    if (not force) and dest_mp4.exists() and dest_mp4.stat().st_size > 120_000:
        return None

    proj_dir = str(HTML_BRIDGES_DIR / bridge_subdir)
    _, tl_path, _ = export_bridge_project(
        day_dir_for_bridge,
        item_id=item_id,
        format_type="long",
        work_proj_dir=proj_dir,
        global_offset_sec=global_offset_sec,
    )

    tl_p = Path(tl_path)
    tl_obj = json.loads(tl_p.read_text(encoding="utf-8"))
    tl_obj["bgm_volume"] = 0.0
    tl_p.write_text(json.dumps(tl_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return proj_dir


def render_prepared_chunk(
    item_id: int,
    proj_dir: Optional[str],
    dest_mp4: Path,
) -> Path:
    """Render Playwright HTML v2 từ bridge project đã xuất."""
    if proj_dir is None and dest_mp4.exists() and dest_mp4.stat().st_size > 120_000:
        dur = probe_duration(dest_mp4)
        ok(f"[Resume] Đã có sẵn {dest_mp4.name} ({dur:.2f}s), bỏ qua render.")
        return dest_mp4

    out_v = render_html_engine(
        proj_dir,
        template="long_sports_news_v2.html",
        scene_number=None,
        fps=VIDEO_FPS,
        preview=False,
        use_cache=False,
        force=True,
    )
    if not out_v or not os.path.exists(out_v):
        raise RuntimeError(f"Render thất bại cho item_id={item_id}")

    dest_mp4.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_v, dest_mp4)
    return dest_mp4


def extract_bumper_pair(src_mp4: Path, vonly_mp4: Path, wav_out: Path, force: bool = False) -> Tuple[Path, Path, float]:
    """Chuẩn hóa Intro.mp4 / Outro.mp4 thành track video-only (1920x1080@30fps) & PCM WAV cắt đúng thời lượng hình."""
    if force or not vonly_mp4.exists() or vonly_mp4.stat().st_size < 60_000:
        vonly_mp4.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(src_mp4),
                "-vf",
                (
                    f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,"
                    f"pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={VIDEO_FPS},format=yuv420p"
                ),
                "-an",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "18",
                "-video_track_timescale",
                TARGET_TIMESCALE,
                str(vonly_mp4),
            ],
            check=True,
        )
    v_dur = probe_stream_duration(vonly_mp4, "v:0")
    if force or not wav_out.exists() or wav_out.stat().st_size < 40_000:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(src_mp4),
                "-vn",
                "-af",
                f"aresample=44100,aformat=channel_layouts=stereo,loudnorm=I=-14.0:TP=-1.5:LRA=11.0,apad,atrim=0:{v_dur:.6f}",
                "-c:a",
                "pcm_s16le",
                "-ar",
                "44100",
                "-ac",
                "2",
                str(wav_out),
            ],
            check=True,
        )
    return vonly_mp4, wav_out, v_dur


def extract_chunk_pair(src_mp4: Path, vonly_mp4: Path, wav_out: Path, force: bool = False) -> Tuple[Path, Path, float]:
    """Tách video-only copy & PCM WAV cắt chuẩn sample theo đúng thời lượng hình từng tin."""
    if force or not vonly_mp4.exists() or vonly_mp4.stat().st_size < 60_000:
        vonly_mp4.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(src_mp4),
                "-an",
                "-c:v",
                "copy",
                "-video_track_timescale",
                TARGET_TIMESCALE,
                str(vonly_mp4),
            ],
            check=True,
        )
    v_dur = probe_stream_duration(vonly_mp4, "v:0")
    if force or not wav_out.exists() or wav_out.stat().st_size < 40_000:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-i",
                str(src_mp4),
                "-vn",
                "-af",
                f"aresample=44100,aformat=channel_layouts=stereo,apad,atrim=0:{v_dur:.6f}",
                "-c:a",
                "pcm_s16le",
                "-ar",
                "44100",
                "-ac",
                "2",
                str(wav_out),
            ],
            check=True,
        )
    return vonly_mp4, wav_out, v_dur


def write_concat_list(paths_list: List[Path], list_file: Path) -> None:
    lines = []
    for p in paths_list:
        safe = str(p).replace("\\", "/").replace("'", "'\\''")
        lines.append(f"file '{safe}'")
    list_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pha 2: Render & Ghép Video Ngày 19.11.2026 (16:9 HTML v2)")
    parser.add_argument("--workers", type=int, default=2, help="Số worker Playwright song song (mặc định: 2)")
    parser.add_argument("--force", action="store_true", help="Render lại toàn bộ kể cả khi đã có file")
    parser.add_argument("--only", type=int, nargs="+", help="Chỉ render các chunk cụ thể (0=Intro, 1..18)")
    parser.add_argument("--skip-compose", action="store_true", help="Chỉ render chunk, bỏ qua bước ghép cuối")
    parser.add_argument("--compose-only", action="store_true", help="Chỉ chạy lại bước ghép master từ các chunk đã render")
    args = parser.parse_args()

    for d in (PREVIEW_DIR, WORK_ROOT, HTML_BRIDGES_DIR, NORM_DIR):
        d.mkdir(parents=True, exist_ok=True)

    intro_obj = json.loads((DAY_DIR / "intro_hook.json").read_text(encoding="utf-8"))
    news_objs = json.loads((DAY_DIR / "thethao.json").read_text(encoding="utf-8"))
    total_news = len(news_objs)
    only_set = set(args.only) if args.only else None

    intro_chunk_mp4 = PREVIEW_DIR / "tin_00_intro_long.mp4"
    chunk_mp4_map: Dict[int, Path] = {int(it["id"]): (PREVIEW_DIR / f"tin_{int(it['id']):02d}_long.mp4") for it in news_objs}

    if not args.compose_only:
        banner(f"PHA 2 BƯỚC 2 — RENDER VIDEO 16:9 HTML V2 NGÀY {DAY_STR}", f"Workers={args.workers}")

        intro_wav = Path(intro_obj["audio_path"])
        if not intro_wav.exists():
            die(f"Thiếu {intro_wav}")
        intro_dur_audio = probe_duration(intro_wav)

        cum_off = intro_dur_audio
        offsets_by_id: Dict[int, float] = {0: 0.0}
        for it in news_objs:
            sc_id = int(it["id"])
            offsets_by_id[sc_id] = round(cum_off, 3)
            ap = Path(it["audio_path"])
            if not ap.exists():
                die(f"Thiếu {ap}")
            cum_off += probe_duration(ap)

        stage_day_dir = prepare_intro_stage(intro_obj, news_objs)
        if only_set is None or 0 in only_set:
            step(f"[00/{total_news}] Render Intro 16:9 HTML v2 -> tin_00_intro_long.mp4...")
            intro_proj = prepare_bridge_project(
                str(stage_day_dir),
                item_id=0,
                dest_mp4=intro_chunk_mp4,
                bridge_subdir="tin_00_intro_long",
                global_offset_sec=0.0,
                force=args.force,
            )
            render_prepared_chunk(0, intro_proj, intro_chunk_mp4)
            ok(f"  -> tin_00_intro_long.mp4 ({probe_duration(intro_chunk_mp4):.2f}s)")

        target_items = [it for it in news_objs if only_set is None or int(it["id"]) in only_set]
        prepared_jobs: List[Tuple[Dict[str, Any], Optional[str], Path]] = []
        for it in target_items:
            sc_id = int(it["id"])
            dest = chunk_mp4_map[sc_id]
            proj_dir = prepare_bridge_project(
                str(DAY_DIR),
                item_id=sc_id,
                dest_mp4=dest,
                bridge_subdir=f"tin_{sc_id:02d}_long",
                global_offset_sec=offsets_by_id[sc_id],
                force=args.force,
            )
            prepared_jobs.append((it, proj_dir, dest))

        def _task(job: Tuple[Dict[str, Any], Optional[str], Path]) -> Tuple[int, Path]:
            it, proj_dir, dest = job
            sc_id = int(it["id"])
            step(f"[{sc_id:02d}/{total_news}] Render Tin #{sc_id:02d} ({it['voice_preset']}, offset={offsets_by_id[sc_id]:.1f}s)...")
            out_p = render_prepared_chunk(sc_id, proj_dir, dest)
            ok(f"  -> Hoàn tất Tin #{sc_id:02d}: {out_p.name} ({probe_duration(out_p):.2f}s)")
            return sc_id, out_p

        if prepared_jobs:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
                futs = [ex.submit(_task, job) for job in prepared_jobs]
                for fut in concurrent.futures.as_completed(futs):
                    fut.result()

        if args.skip_compose or only_set is not None:
            ok("Đã hoàn tất render các cảnh yêu cầu (--skip-compose / --only).")
            return

    banner("GHÉP CUT-CONCAT & MASTER AUDIO SAMPLE-ACCURATE (-14.0 LUFS)", f"Intro.mp4 + tin_00 + tin_01..{total_news:02d} + Outro.mp4")

    logo_intro = ROOT / "logo" / "Intro.mp4"
    logo_outro = ROOT / "logo" / "Outro.mp4"
    if not logo_intro.exists() or not logo_outro.exists():
        die("Thiếu logo/Intro.mp4 hoặc logo/Outro.mp4")

    re_norm = args.force or args.compose_only
    intro_vonly, intro_wav_exact, intro_bumper_dur = extract_bumper_pair(
        logo_intro, NORM_DIR / "logo_intro_vonly.mp4", NORM_DIR / "logo_intro_exact.wav", force=re_norm
    )
    outro_vonly, outro_wav_exact, outro_bumper_dur = extract_bumper_pair(
        logo_outro, NORM_DIR / "logo_outro_vonly.mp4", NORM_DIR / "logo_outro_exact.wav", force=re_norm
    )

    middle_raw_chunks = [intro_chunk_mp4] + [chunk_mp4_map[int(it["id"])] for it in news_objs]
    mid_vonly_list: List[Path] = []
    mid_wav_list: List[Path] = []
    mid_v_durs: List[float] = []

    for src_c in middle_raw_chunks:
        if not src_c.exists():
            die(f"Thiếu chunk render: {src_c}")
        vo, wv, vd = extract_chunk_pair(
            src_c, NORM_DIR / f"{src_c.stem}_vonly.mp4", NORM_DIR / f"{src_c.stem}_exact.wav", force=re_norm
        )
        mid_vonly_list.append(vo)
        mid_wav_list.append(wv)
        mid_v_durs.append(vd)

    chapters: List[Dict[str, Any]] = []
    cur_t = 0.0
    chapters.append({"time": "00:00", "seconds": 0.0, "label": "Nhập cuộc & Tâm điểm thể thao 19.11.2026"})
    cur_t += intro_bumper_dur + mid_v_durs[0]

    for it, vd in zip(news_objs, mid_v_durs[1:]):
        sc_id = int(it["id"])
        m, s = divmod(int(round(cur_t)), 60)
        chapters.append(
            {
                "time": f"{m:02d}:{s:02d}",
                "seconds": round(cur_t, 3),
                "label": f"[{sc_id:02d}] {it['title']}",
            }
        )
        cur_t += vd

    (PREVIEW_DIR / "chapters_19_11.json").write_text(
        json.dumps({"total_content_end_sec": round(cur_t, 3), "chapters": chapters}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    all_v_list = WORK_ROOT / "concat_all_vonly.txt"
    write_concat_list([intro_vonly] + mid_vonly_list + [outro_vonly], all_v_list)
    master_vonly_mp4 = WORK_ROOT / "master_video_only.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(all_v_list), "-c", "copy", str(master_vonly_mp4)],
        check=True,
    )
    master_v_dur = probe_stream_duration(master_vonly_mp4, "v:0")

    mid_wav_concat_list = WORK_ROOT / "concat_mid_wav.txt"
    write_concat_list(mid_wav_list, mid_wav_concat_list)
    mid_voice_wav = WORK_ROOT / "middle_voice_exact.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(mid_wav_concat_list), "-c", "copy", str(mid_voice_wav)],
        check=True,
    )
    mid_v_dur = sum(mid_v_durs)

    bgm_file = ROOT / "assets" / "bgm" / "bgm_editorial_2_momentum.mp3"
    if not bgm_file.exists():
        die(f"Không tìm thấy BGM: {bgm_file}")

    mid_premix_wav = WORK_ROOT / "middle_premix.wav"
    fade_out_st = max(0.0, mid_v_dur - 2.5)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(mid_voice_wav),
            "-stream_loop",
            "-1",
            "-i",
            str(bgm_file),
            "-filter_complex",
            (
                f"[1:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.05,"
                f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_out_st:.6f}:d=2.5,atrim=0:{mid_v_dur:.6f}[bgm];"
                f"[0:a]aresample=44100,aformat=channel_layouts=stereo[fg];"
                f"[fg][bgm]amix=inputs=2:duration=first:normalize=0,atrim=0:{mid_v_dur:.6f}[aout]"
            ),
            "-map",
            "[aout]",
            "-c:a",
            "pcm_s16le",
            str(mid_premix_wav),
        ],
        check=True,
    )

    mid_loudnorm_raw = WORK_ROOT / "middle_loudnorm_raw.wav"
    if not two_pass_loudnorm(str(mid_premix_wav), str(mid_loudnorm_raw), target_i=-14.0, target_tp=-1.5, target_lra=11.0):
        shutil.copy2(mid_premix_wav, mid_loudnorm_raw)

    mid_master_exact = WORK_ROOT / "middle_master_exact.wav"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(mid_loudnorm_raw),
            "-af",
            f"aresample=44100,aformat=channel_layouts=stereo,apad,atrim=0:{mid_v_dur:.6f}",
            "-c:a",
            "pcm_s16le",
            str(mid_master_exact),
        ],
        check=True,
    )

    full_wav_list = WORK_ROOT / "concat_full_wav.txt"
    write_concat_list([intro_wav_exact, mid_master_exact, outro_wav_exact], full_wav_list)
    full_master_wav = WORK_ROOT / "full_master_audio.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(full_wav_list), "-c", "copy", str(full_master_wav)],
        check=True,
    )

    final_out = DAY_DIR / "Tin-The-Thao-19-11.mp4"
    tmp_final = WORK_ROOT / "Tin-The-Thao-19-11.tmp.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(master_vonly_mp4),
            "-i",
            str(full_master_wav),
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "copy",
            "-af",
            f"apad,atrim=0:{master_v_dur:.6f}",
            "-c:a",
            "aac",
            "-ar",
            "44100",
            "-ac",
            "2",
            "-b:a",
            "192k",
            "-t",
            f"{master_v_dur:.6f}",
            "-movflags",
            "+faststart",
            str(tmp_final),
        ],
        check=True,
    )
    shutil.copy2(tmp_final, final_out)

    v_chk = probe_stream_duration(final_out, "v:0")
    a_chk = probe_stream_duration(final_out, "a:0")
    drift_ms = abs(v_chk - a_chk) * 1000.0
    stats = measure_loudness(str(final_out))
    ok("=" * 72)
    ok(f"HOÀN TẤT VIDEO 16:9 NGÀY {DAY_STR} -> {paths.rel_to_root(str(final_out))}")
    ok(f"Video={v_chk:.4f}s | Audio={a_chk:.4f}s | Drift={drift_ms:.2f}ms | Intro+Hook={intro_bumper_dur + mid_v_durs[0]:.2f}s")
    if stats:
        ok(f"Âm lượng đo thực tế: I={stats.get('input_i')} LUFS, TP={stats.get('input_tp')} dBTP")
    if drift_ms > 33.3:
        die(f"LỆCH A/V VƯỢT NGƯỠNG CHO PHÉP: {drift_ms:.2f}ms > 33.3ms")


if __name__ == "__main__":
    main()
