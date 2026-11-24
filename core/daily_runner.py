#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/daily_runner.py — Bộ Điều Phối Sản Xuất Bản Tin Ngày Tổng Quát (1 Lệnh Duy Nhất)
====================================================================================
Thay thế việc nhân bản script theo từng ngày (`generate_daily_tts_XX_XX.py`, `build_daily_XX_XX_video.py`).
Đọc trực tiếp dữ liệu chuẩn tại `outputs/<DD.MM.YYYY>/` (`intro_hook.json`, `thethao.json`,
`image_plan.json`, `image_credits.json`, `thumbnails_plan.json`) và chạy trọn gói các bước:

  python3 -B core/daily_runner.py --day 20.11.2026 --step qa
  python3 -B core/daily_runner.py --day 20.11.2026 --step tts
  python3 -B core/daily_runner.py --day 20.11.2026 --step video --workers 3
  python3 -B core/daily_runner.py --day 20.11.2026 --step thumbs
  python3 -B core/daily_runner.py --day 20.11.2026 --step all --workers 3

Tận dụng đầy đủ nâng cấp Giai đoạn 1 & 2:
  - 9 layout chống lặp + Broadcast Stat HUD (long_sports_news_v2.html + m8_news_bridge.py)
  - Render chunk `video_only_output=True` + `h264_videotoolbox` + CDP screenshot + 3 workers
  - Cut-Concat PCM WAV sample-accurate + 2-pass loudnorm -14.0 LUFS + A/V Drift <= 33.3ms
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse
import concurrent.futures
import datetime as dt
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple

from pydub import AudioSegment

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
if os.path.join(_HERE, "vendor") not in sys.path:
    sys.path.insert(0, os.path.join(_HERE, "vendor"))
engines_html = os.path.join(_ROOT, "engines", "html")
if engines_html not in sys.path:
    sys.path.insert(0, engines_html)

from clean import clean_work_dir, send_to_trash
from diemdoc import paths
from diemdoc.audio import apply_voice_standard, build_sfx_track, measure_loudness, two_pass_loudnorm
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.publisher import load_voice_preset, write_mota_16x9
from diemdoc.tts_text import prepare
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from m8_news_bridge import compute_daily_plan, export_bridge_project
from qa_precheck import run_qa
from renderer import _has_videotoolbox, render_html_engine

ROOT = Path(_ROOT)
WEEKDAYS_VI = ["THỨ HAI", "THỨ BA", "THỨ TƯ", "THỨ NĂM", "THỨ SÁU", "THỨ BẢY", "CHỦ NHẬT"]


def _format_vi_date_chip(day_str: str) -> str:
    if day_str.lower().startswith("weekly-"):
        from diemdoc.weekly_coverage import format_weekly_date_chip
        return format_weekly_date_chip(day_str)
    try:
        d = dt.datetime.strptime(day_str, "%d.%m.%Y").date()
        return f"{WEEKDAYS_VI[d.weekday()]} · {day_str}"
    except Exception:
        return day_str


def _probe_dur(path: str, selector: str) -> float:
    out = subprocess.check_output(
        [
            "ffprobe", "-v", "error", "-select_streams", selector,
            "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1",
            path,
        ],
        text=True,
    ).strip()
    return float(out.splitlines()[0])


def _run_ffmpeg(cmd: List[str], err_msg: str) -> None:
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        die(f"{err_msg}\n{res.stderr[-1200:]}")


def _synth_text_chunks(model, text: str, preset: Dict[str, Any], cache_dir: Path) -> AudioSegment:
    tts_str, _ = prepare(text.strip())
    chunks = build_chunks_from_text(tts_str, max_words_per_chunk=60, inter_sentence_pause=0.25)
    out = AudioSegment.silent(duration=0, frame_rate=44100).set_channels(2)
    for ch in chunks:
        if ch.get("type") == "pause":
            pause_ms = int(round(float(ch.get("pause_sec", 0.25)) * 1000))
            if pause_ms > 0:
                out += AudioSegment.silent(duration=pause_ms, frame_rate=44100).set_channels(2)
            continue
        seg, _ = render_chunk_vitts(
            model,
            ch["text"],
            preset["voice_id"],
            temperature=preset["temperature"],
            speed=preset["speed"],
            pitch=preset["pitch"],
            cache_dir=str(cache_dir),
            use_cache=True,
            max_chars=768,
        )
        seg = trim_segment_silence(seg).set_frame_rate(44100).set_channels(2)
        out += seg
    return apply_voice_standard(out)


def run_tts_step(day_str: str, force: bool = False) -> None:
    from vieneu import Vieneu

    day_dir = ROOT / "outputs" / day_str
    audio_dir = day_dir / "audio"
    title_dir = day_dir / "audio-title"
    audio_dir.mkdir(parents=True, exist_ok=True)
    title_dir.mkdir(parents=True, exist_ok=True)

    tag = day_str.replace(".", "_")
    tts_cache = Path(paths.WORK) / f"tts_cache_daily_{tag}"
    tts_cache.mkdir(parents=True, exist_ok=True)

    p_male = load_voice_preset("primary")
    p_female = load_voice_preset("secondary")

    banner(f"BƯỚC TTS — TỔNG HỢP GIỌNG ĐỌC NGÀY {day_str}")
    model = Vieneu(mode="v3turbo")

    total_sec = 0.0
    intro_p = day_dir / "intro_hook.json"
    if intro_p.exists():
        intro = json.loads(intro_p.read_text(encoding="utf-8"))
        intro_wav = audio_dir / "audio_intro.wav"
        if (not force) and intro_wav.exists() and intro_wav.stat().st_size > 50_000:
            dur = round(len(AudioSegment.from_wav(str(intro_wav))) / 1000.0, 2)
            ok(f"[Intro] Đã có sẵn ({dur:.2f}s) -> audio_intro.wav")
        else:
            segs = intro.get("voice_segments") or intro.get("segments") or []
            gap = AudioSegment.silent(duration=250, frame_rate=44100).set_channels(2)
            intro_audio = AudioSegment.silent(duration=0, frame_rate=44100).set_channels(2)
            for i, seg_obj in enumerate(segs):
                vp = seg_obj.get("voice_preset") or seg_obj.get("voice") or ("secondary" if i % 2 == 0 else "primary")
                pr = p_male if vp == "primary" else p_female
                seg = _synth_text_chunks(model, seg_obj["text"], pr, tts_cache)
                if i > 0:
                    intro_audio += gap
                intro_audio += seg
            intro_audio = apply_voice_standard(intro_audio.set_frame_rate(44100).set_channels(2))
            intro_audio.export(str(intro_wav), format="wav")
            dur = round(len(intro_audio) / 1000.0, 2)
            ok(f"[Intro] {dur:.2f}s -> audio_intro.wav")
        intro["duration"] = dur
        intro["audio_duration"] = dur
        intro["audio_path"] = str(intro_wav)
        intro["audio_title"] = ""
        intro_p.write_text(json.dumps(intro, ensure_ascii=False, indent=2), encoding="utf-8")
        total_sec += dur

    items_p = day_dir / "thethao.json"
    items = json.loads(items_p.read_text(encoding="utf-8"))
    title_gap = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)
    for it in items:
        sc_id = int(it["id"])
        t_wav = title_dir / f"audio_title_{sc_id:02d}.wav"
        f_wav = audio_dir / f"audio_{sc_id:02d}.wav"
        if (not force) and t_wav.exists() and f_wav.exists() and f_wav.stat().st_size > 50_000:
            f_dur = round(len(AudioSegment.from_wav(str(f_wav))) / 1000.0, 2)
            t_dur = round(len(AudioSegment.from_wav(str(t_wav))) / 1000.0, 2)
            ok(f"[Tin #{sc_id:02d}/{len(items)}] Đã có sẵn full={f_dur:.2f}s (title={t_dur:.2f}s)")
        else:
            vp = it.get("voice_preset") or ("primary" if (sc_id % 2 == 1) else "secondary")
            pr = p_male if vp == "primary" else p_female
            title_seg = _synth_text_chunks(model, it["title"], pr, tts_cache)
            body_seg = _synth_text_chunks(model, it["summary"], pr, tts_cache)
            full_seg = apply_voice_standard((title_seg + title_gap + body_seg).set_frame_rate(44100).set_channels(2))

            title_seg.export(str(t_wav), format="wav")
            full_seg.export(str(f_wav), format="wav")
            f_dur = round(len(full_seg) / 1000.0, 2)
            t_dur = round(len(title_seg) / 1000.0, 2)
            ok(f"[Tin #{sc_id:02d}/{len(items)}] full={f_dur:.2f}s (title={t_dur:.2f}s)")

        it["duration"] = f_dur
        it["audio_duration"] = f_dur
        it["title_duration"] = t_dur
        it["audio_path"] = str(f_wav)
        it["audio_title"] = str(t_wav)
        total_sec += f_dur

    items_p.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    ok(f"HOÀN TẤT TTS NGÀY {day_str}: Tổng lời đọc {total_sec:.1f}s (~{total_sec / 60:.2f} phút) cho {len(items)} bản tin")


def _write_concat_list(paths_list: List[Path], list_file: Path) -> None:
    lines = []
    for p in paths_list:
        safe = str(p).replace("\\", "/").replace("'", "'\\''")
        lines.append(f"file '{safe}'")
    list_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_video_step(day_str: str, workers: int = 3, force: bool = False) -> None:
    day_dir = ROOT / "outputs" / day_str
    tag = day_str.replace(".", "_")
    dd_mm = "-".join(day_str.split(".")[:2])
    work_root = Path(paths.WORK) / f"daily_{tag}_video"
    bridges_dir = work_root / "bridges"
    chunks_dir = work_root / "chunks"
    bridges_dir.mkdir(parents=True, exist_ok=True)
    chunks_dir.mkdir(parents=True, exist_ok=True)

    date_chip = _format_vi_date_chip(day_str)
    items = json.loads((day_dir / "thethao.json").read_text(encoding="utf-8"))
    intro = json.loads((day_dir / "intro_hook.json").read_text(encoding="utf-8")) if (day_dir / "intro_hook.json").exists() else None
    all_plan_items = ([intro] if intro else []) + items
    compute_daily_plan(all_plan_items, date_chip, str(day_dir / "images"))

    banner(f"BƯỚC VIDEO 16:9 HTML V2 — {date_chip}", f"{len(items)} bản tin | Workers={workers} | Video-only chunks + VideoToolbox")

    render_jobs: List[Tuple[int, str, str, Path, List[Dict[str, Any]]]] = []
    cur_offset = 0.0

    # Chuẩn bị bridge tuần tự (tái sử dụng Whisper singleton cache, tránh tranh chấp RAM)
    if intro is not None:
        intro_wav = Path(intro.get("audio_path") or (day_dir / "audio" / "audio_intro.wav"))
        b_dir = bridges_dir / "tin_00_intro_long"
        b_dir.mkdir(parents=True, exist_ok=True)
        _, tl_path, _ = export_bridge_project(
            str(day_dir), item_id=0, format_type="long", work_proj_dir=str(b_dir), global_offset_sec=cur_offset
        )
        tl_d = json.loads(Path(tl_path).read_text(encoding="utf-8"))
        tl_d["output_filename"] = "tin_00_long.mp4"
        tl_d["ticker_headlines"] = [it["title"].upper() for it in items[:8]]
        Path(tl_path).write_text(json.dumps(tl_d, ensure_ascii=False, indent=2), encoding="utf-8")
        render_jobs.append((0, "Intro", str(b_dir), intro_wav, tl_d.get("sfx_events") or []))
        cur_offset += float(tl_d.get("total_duration", 0.0))

    for it in items:
        sc_id = int(it["id"])
        wav_p = Path(it.get("audio_path") or (day_dir / "audio" / f"audio_{sc_id:02d}.wav"))
        b_dir = bridges_dir / f"tin_{sc_id:02d}_long"
        b_dir.mkdir(parents=True, exist_ok=True)
        _, tl_path, _ = export_bridge_project(
            str(day_dir), item_id=sc_id, format_type="long", work_proj_dir=str(b_dir), global_offset_sec=cur_offset
        )
        tl_d = json.loads(Path(tl_path).read_text(encoding="utf-8"))
        tl_d["output_filename"] = f"tin_{sc_id:02d}_long.mp4"
        Path(tl_path).write_text(json.dumps(tl_d, ensure_ascii=False, indent=2), encoding="utf-8")
        render_jobs.append((sc_id, f"Tin #{sc_id:02d}/{len(items)}", str(b_dir), wav_p, tl_d.get("sfx_events") or []))
        cur_offset += float(tl_d.get("total_duration", 0.0))

    def _render_one(job: Tuple[int, str, str, Path, List[Dict[str, Any]]]) -> Tuple[int, str, Path, List[Dict[str, Any]]]:
        sc_id, lbl, b_dir, wav_p, sfx_ev = job
        step(f"Render {lbl} (video_only_output=True)...")
        mp4 = render_html_engine(
            project_dir=b_dir,
            template="long_sports_news_v2.html",
            scene_number=None,
            fps=30,
            preview=False,
            use_cache=not force,
            force=force,
            format_override="long",
            video_only_output=True,
            jpeg_quality=88,
            hw_encode=True,
        )
        if not mp4 or not os.path.exists(mp4):
            die(f"Render thất bại cho {lbl}")
        return sc_id, mp4, wav_p, sfx_ev

    rendered: Dict[int, Tuple[str, Path, List[Dict[str, Any]]]] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        for sc_id, mp4, wav_p, sfx_ev in ex.map(_render_one, render_jobs):
            rendered[sc_id] = (mp4, wav_p, sfx_ev)

    # Ghép Cut-Concat Video + Master Audio PCM sample-accurate + SFX + BGM + 2-pass Loudnorm -14.0 LUFS
    step("Ghép Cut-Concat, SFX, BGM & Master Audio (-14.0 LUFS)...")
    intro_bumper = ROOT / "logo" / "Intro.mp4"
    outro_bumper = ROOT / "logo" / "Outro.mp4"
    bumper_v_parts: Dict[str, Tuple[Path, Path, float]] = {}
    target_timescale = "15360"
    use_hw = _has_videotoolbox()
    v_enc_args = ["-c:v", "h264_videotoolbox", "-b:v", "2600k", "-maxrate", "3600k", "-bufsize", "5400k", "-pix_fmt", "yuv420p"] if use_hw else [
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p"
    ]

    def _prep_bumper(bp: Path, name: str) -> Optional[Tuple[Path, Path, float]]:
        if not bp.exists():
            return None
        v_out = chunks_dir / f"{name}_v.mp4"
        a_out = chunks_dir / f"{name}_a.wav"
        _run_ffmpeg(
            [
                "ffmpeg", "-y", "-i", str(bp), "-an",
                "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p",
                *v_enc_args, "-r", "30", "-video_track_timescale", target_timescale, str(v_out),
            ],
            f"Lỗi tách video bumper {name}",
        )
        vd = _probe_dur(str(v_out), "v:0")
        _run_ffmpeg(
            [
                "ffmpeg", "-y", "-i", str(bp), "-vn",
                "-af", f"aresample=44100,aformat=channel_layouts=stereo,loudnorm=I=-14.0:TP=-1.5:LRA=11.0,apad,atrim=0:{vd:.6f}",
                "-ac", "2", "-ar", "44100", "-c:a", "pcm_s16le", str(a_out),
            ],
            f"Lỗi tách audio bumper {name}",
        )
        return v_out, a_out, vd

    b_intro = _prep_bumper(intro_bumper, "000_intro_bumper")
    b_outro = _prep_bumper(outro_bumper, "999_outro_bumper")

    mid_vid_parts: List[Path] = []
    mid_aud_parts: List[Path] = []
    mid_sfx_events: List[Dict[str, Any]] = []
    chapters: List[Dict[str, Any]] = []
    cum_t = b_intro[2] if b_intro else 0.0
    mid_t = 0.0

    if 0 in rendered:
        chapters.append({"time": "00:00", "seconds": 0.0, "label": f"Nhập cuộc & Tâm điểm thể thao {day_str}"})

    for sc_id, lbl, _, _, _ in render_jobs:
        mp4_str, wav_p, sfx_ev = rendered[sc_id]
        v_out = chunks_dir / f"seg_{sc_id:02d}_v.mp4"
        a_out = chunks_dir / f"seg_{sc_id:02d}_a.wav"
        _run_ffmpeg(
            ["ffmpeg", "-y", "-i", mp4_str, "-an", "-c:v", "copy", "-video_track_timescale", target_timescale, str(v_out)],
            f"Lỗi tách video chunk {sc_id}",
        )
        vd = _probe_dur(str(v_out), "v:0")
        _run_ffmpeg(
            [
                "ffmpeg", "-y", "-i", str(wav_p),
                "-af", f"aresample=44100,aformat=channel_layouts=stereo,apad,atrim=0:{vd:.6f}",
                "-ac", "2", "-ar", "44100", "-c:a", "pcm_s16le", str(a_out),
            ],
            f"Lỗi chuẩn hóa audio chunk {sc_id}",
        )
        for ev in sfx_ev:
            ev_t = float(ev.get("time", 0.0))
            if 0.0 <= ev_t < vd - 0.1:
                mid_sfx_events.append({
                    "file": ev.get("sfx") or ev.get("file") or "whoosh_cinematic_short.mp3",
                    "time": round(mid_t + ev_t, 3),
                    "type": "card",
                })
        if sc_id > 0:
            mm, ss = divmod(int(round(cum_t)), 60)
            it_obj = next(x for x in items if int(x["id"]) == sc_id)
            chapters.append({"time": f"{mm:02d}:{ss:02d}", "seconds": round(cum_t, 3), "label": it_obj["title"]})
        mid_vid_parts.append(v_out)
        mid_aud_parts.append(a_out)
        cum_t += vd
        mid_t += vd

    all_vid_parts = ([b_intro[0]] if b_intro else []) + mid_vid_parts + ([b_outro[0]] if b_outro else [])
    v_list = chunks_dir / "v_concat.txt"
    a_mid_list = chunks_dir / "a_mid_concat.txt"
    _write_concat_list(all_vid_parts, v_list)
    _write_concat_list(mid_aud_parts, a_mid_list)

    master_v = work_root / "master_video.mp4"
    mid_voice = work_root / "mid_voice.wav"
    _run_ffmpeg(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(v_list), "-c", "copy", str(master_v)], "Lỗi Cut-Concat video")
    _run_ffmpeg(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(a_mid_list), "-c:a", "pcm_s16le", str(mid_voice)], "Lỗi Concat audio thân")

    bgm_path = ROOT / "assets" / "bgm" / "bgm_editorial_2_momentum.mp3"
    sfx_wav_path, sfx_cnt = build_sfx_track(mid_sfx_events, mid_t, str(work_root / "mid_sfx.wav"))
    ok(f"SFX track: {sfx_cnt} sự kiện âm thanh chuyển cảnh/điểm nhấn")

    mid_premix = work_root / "mid_premix.wav"
    fade_out_st = max(0.0, mid_t - 2.5)
    if sfx_wav_path and os.path.exists(sfx_wav_path):
        _run_ffmpeg(
            [
                "ffmpeg", "-y", "-i", str(mid_voice), "-stream_loop", "-1", "-i", str(bgm_path), "-i", str(sfx_wav_path),
                "-filter_complex", (
                    f"[1:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.052,"
                    f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_out_st:.6f}:d=2.5,atrim=0:{mid_t:.6f}[bg];"
                    f"[2:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.38,atrim=0:{mid_t:.6f}[sx];"
                    f"[0:a]aresample=44100,aformat=channel_layouts=stereo[fg];"
                    f"[fg][bg][sx]amix=inputs=3:duration=first:normalize=0,atrim=0:{mid_t:.6f}[m]"
                ),
                "-map", "[m]", "-ac", "2", "-ar", "44100", "-c:a", "pcm_s16le", str(mid_premix),
            ],
            "Lỗi trộn BGM + SFX",
        )
    else:
        _run_ffmpeg(
            [
                "ffmpeg", "-y", "-i", str(mid_voice), "-stream_loop", "-1", "-i", str(bgm_path),
                "-filter_complex", (
                    f"[1:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.055,"
                    f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_out_st:.6f}:d=2.5,atrim=0:{mid_t:.6f}[bg];"
                    f"[0:a]aresample=44100,aformat=channel_layouts=stereo[fg];"
                    f"[fg][bg]amix=inputs=2:duration=first:normalize=0,atrim=0:{mid_t:.6f}[m]"
                ),
                "-map", "[m]", "-ac", "2", "-ar", "44100", "-c:a", "pcm_s16le", str(mid_premix),
            ],
            "Lỗi trộn BGM",
        )

    mid_ln = work_root / "mid_loudnorm.wav"
    if not two_pass_loudnorm(str(mid_premix), str(mid_ln), target_i=-14.0, target_tp=-1.5, target_lra=11.0):
        shutil.copy2(mid_premix, mid_ln)

    mid_exact = work_root / "mid_exact.wav"
    _run_ffmpeg(
        [
            "ffmpeg", "-y", "-i", str(mid_ln),
            "-af", f"aresample=44100,aformat=channel_layouts=stereo,apad,atrim=0:{mid_t:.6f}",
            "-ac", "2", "-ar", "44100", "-c:a", "pcm_s16le", str(mid_exact),
        ],
        "Lỗi căn mẫu audio thân",
    )

    all_aud_parts = ([b_intro[1]] if b_intro else []) + [mid_exact] + ([b_outro[1]] if b_outro else [])
    a_full_list = chunks_dir / "a_full_concat.txt"
    _write_concat_list(all_aud_parts, a_full_list)
    full_master_wav = work_root / "full_master.wav"
    _run_ffmpeg(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(a_full_list), "-c", "copy", str(full_master_wav)], "Lỗi ghép master audio")

    total_v = _probe_dur(str(master_v), "v:0")
    out_mp4 = day_dir / f"Tin-The-Thao-{dd_mm}.mp4"
    tmp_out = work_root / f"Tin-The-Thao-{dd_mm}.tmp.mp4"
    _run_ffmpeg(
        [
            "ffmpeg", "-y", "-i", str(master_v), "-i", str(full_master_wav),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy",
            "-af", f"apad,atrim=0:{total_v:.6f}",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-t", f"{total_v:.6f}", "-movflags", "+faststart", str(tmp_out),
        ],
        "Lỗi xuất MP4 cuối cùng",
    )
    shutil.copy2(tmp_out, out_mp4)

    preview_dir = day_dir / "_preview_v2"
    preview_dir.mkdir(parents=True, exist_ok=True)
    (preview_dir / f"chapters_{dd_mm.replace('-', '_')}.json").write_text(
        json.dumps({"day": day_str, "total_content_end_sec": round(cum_t, 3), "chapters": chapters}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    vd_final = _probe_dur(str(out_mp4), "v:0")
    ad_final = _probe_dur(str(out_mp4), "a:0")
    drift_ms = abs(vd_final - ad_final) * 1000.0
    final_stats = measure_loudness(str(out_mp4)) or {}
    ok(f"HOÀN TẤT VIDEO 16:9 -> {paths.rel_to_root(str(out_mp4))}")
    ok(f"Video={vd_final:.3f}s | Audio={ad_final:.3f}s | Drift={drift_ms:.2f}ms | I={final_stats.get('input_i')} LUFS | TP={final_stats.get('input_tp')} dBTP")
    if drift_ms > 33.3:
        die(f"LỆCH A/V VƯỢT NGƯỠNG CHO PHÉP: {drift_ms:.2f}ms > 33.3ms")

    # Tự động dọn thư mục đệm render video (~2-10 GB) sau khi đã xuất thành phẩm đạt chuẩn
    if work_dir.exists():
        if send_to_trash(str(work_dir)):
            ok(f"Đã tự động dọn thư mục đệm render vào Trash: {work_dir.name}")


def run_mota_step(day_str: str) -> Path:
    day_dir = ROOT / "outputs" / day_str
    dd_mm = "-".join(day_str.split(".")[:2])
    ch_path = day_dir / "_preview_v2" / f"chapters_{dd_mm.replace('-', '_')}.json"
    chapters = []
    if ch_path.exists():
        raw_ch = json.loads(ch_path.read_text(encoding="utf-8"))
        chapters = [(c["time"], c["label"]) for c in raw_ch.get("chapters", [])]

    th_path = day_dir / "thethao.json"
    items = json.loads(th_path.read_text(encoding="utf-8")) if th_path.exists() else []
    top_titles = [it.get("title", "").strip() for it in items[:5] if it.get("title")]

    t_a = top_titles[0] if len(top_titles) >= 1 else f"Tổng hợp tin tức thể thao nóng nhất ngày {day_str}"
    t_b = top_titles[1] if len(top_titles) >= 2 else t_a
    t_c = top_titles[2] if len(top_titles) >= 3 else t_a
    bullets = [it.get("title", "").strip() for it in items[:5] if it.get("title")]

    out_mota = write_mota_16x9(
        out_path=day_dir / "mota.txt",
        titles_abc=[t_a, t_b, t_c],
        chapters=chapters,
        video_type="daily_digest",
        highlight_bullets=bullets,
        sources_line="📰 Nguồn tổng hợp & đối chiếu: VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí, Bóng Đá Plus, AFC, FIFA.",
        day_str=day_str,
    )
    ok(f"Đã xuất mô tả chuẩn YouTube (| Điểm Đọc): {paths.rel_to_root(str(out_mota))}")
    return out_mota


def main() -> None:
    parser = argparse.ArgumentParser(description="Bộ điều phối sản xuất bản tin hằng ngày Điểm Đọc")
    parser.add_argument("--day", required=True, help="Ngày định dạng DD.MM.YYYY")
    parser.add_argument("--step", choices=["qa", "tts", "video", "thumbs", "mota", "clean", "all"], default="all")
    parser.add_argument("--workers", type=int, default=3, help="Số worker render song song (mặc định: 3)")
    parser.add_argument("--force", action="store_true", help="Tạo lại kể cả khi đã có cache/file đầu ra")
    parser.add_argument("--cloud", action="store_true", help="Đẩy phần việc nặng (TTS + Render Video) lên GitHub Actions Matrix")
    parser.add_argument("--local", action="store_true", help="Ép buộc chạy 100% trực tiếp trên máy Mac")
    parser.add_argument("--shards", type=int, default=8, help="Số máy ảo GitHub chạy song song khi bật --cloud (mặc định: 8)")
    args = parser.parse_args()

    if args.step == "clean":
        clean_work_dir(days=0.0, apply=True, quiet=False)
        return

    if args.step in ("qa", "all"):
        errs, _ = run_qa(args.day)
        if errs > 0:
            die("Dừng pipeline vì Auto-QA phát hiện lỗi nghiêm trọng.")

    use_cloud = (args.cloud or os.environ.get("DD_USE_CLOUD", "0") == "1") and (not args.local)
    if use_cloud and args.step in ("tts", "video", "all"):
        step(f"Chuyển giao bước nặng (TTS + Render Video 16:9) ngày {args.day} lên GitHub Cloud Matrix ({args.shards} shards)...")
        res = subprocess.run([
            sys.executable, "-B", str(ROOT / "core" / "cloud_runner.py"),
            "--day", args.day,
            "--mode", "daily_long",
            "--shards", str(args.shards),
            "--skip-qa",
        ])
        if res.returncode == 0:
            return
        warn("Cloud Render gặp sự cố, tự động fallback về chạy trực tiếp trên máy Mac...")

    if args.step in ("tts", "all"):
        run_tts_step(args.day, force=args.force)
    if args.step in ("video", "all"):
        run_video_step(args.day, workers=args.workers, force=args.force)
    if args.step in ("thumbs", "all"):
        subprocess.run([sys.executable, "-B", str(ROOT / "core" / "build_thumbnails_09_11.py"), "--day", args.day], check=True)
    if args.step in ("mota", "all"):
        run_mota_step(args.day)


if __name__ == "__main__":
    main()
