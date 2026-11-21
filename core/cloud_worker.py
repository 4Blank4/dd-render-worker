#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/cloud_worker.py — Trình Thực Thi Đám Mây Trên GitHub Actions (Matrix & Compose)
====================================================================================
Chạy bên trong máy ảo GitHub Actions Ubuntu (4 vCPU, 16 GB RAM).
Hỗ trợ 3 loại công việc nặng nhất của kênh Điểm Đọc:
  1. `daily_long`:
     - `shard`: Chia Matrix 6–10 máy ảo chạy song song TTS (ViTTS v3turbo) + Whisper + Render HTML v2 (16:9).
     - `compose`: Gom toàn bộ mảnh MP4/WAV từ các shard, ghép Cut-Concat sample-accurate PCM WAV,
       trộn BGM + SFX + 2-pass loudnorm (-14.0 LUFS, Drift <= 33.3ms) và render bộ 3 Thumbnail 16:9.
  2. `short_batch`:
     - `shard`: Mỗi máy ảo xử lý độc lập 1–2 video Short 9:16 (Single-voice hoặc Dual-voice `voice_segments`,
       Opening Hook HUD, DataViz, Outro 9:16, Thumbnail 9:16, Mô tả SEO `_mota.txt`, Contact Sheet QA).
     - `compose`: Gom toàn bộ thành phẩm từ các shard và hợp nhất metadata (`thethao.json`, `image_plan.json`, `image_credits.json`).
  3. `digest_short`:
     - Chạy trọn gói Video Short Bản Tin Nhanh (17–26 tin, < 3 phút gồm Outro 9:16) trên template `short_digest_v2.html`.
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
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pydub import AudioSegment

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for p in (_HERE, os.path.join(_HERE, "vendor"), os.path.join(_ROOT, "engines", "html")):
    if p not in sys.path:
        sys.path.insert(0, p)

from build_thumbnails_09_11 import render_thumbnails
from daily_runner import (
    _format_vi_date_chip,
    _probe_dur,
    _run_ffmpeg,
    _synth_text_chunks,
    _write_concat_list,
)
from diemdoc import paths
from diemdoc.audio import apply_voice_standard, build_sfx_track, measure_loudness, two_pass_loudnorm
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.publisher import load_voice_preset, render_thumbnail_9x16, write_mota_9x16
from diemdoc.short_batch import (
    ShortDayContext,
    build_and_publish_short,
    build_contact_sheet,
    copy_and_verify_images,
    merge_day_metadata,
    synthesize_item_audio,
)
from diemdoc.short_outro import append_short_outro
from diemdoc.tts_text import prepare
from m3_voice import render_chunk_vitts, trim_segment_silence
from m8_news_bridge import compute_daily_plan, compute_pan_params, export_bridge_project, interpolate_sentence_words
from renderer import _has_videotoolbox, render_html_engine

ROOT = Path(_ROOT)


def _fix_day_paths(obj: Any, day_dir: Path) -> Any:
    """Chuẩn hóa mọi đường dẫn tuyệt đối từ máy Mac sang đường dẫn thực tế trên máy ảo Linux."""
    if isinstance(obj, dict):
        return {k: _fix_day_paths(v, day_dir) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_fix_day_paths(x, day_dir) for x in obj]
    if isinstance(obj, str):
        for folder in ("images", "audio", "audio-title", "shorts", "qa"):
            marker = f"/{folder}/"
            if marker in obj and (obj.startswith("/") or "outputs/" in obj):
                fname = obj.split(marker)[-1]
                cand = day_dir / folder / fname
                return str(cand)
    return obj


def _load_job_manifest(job_dir: Path) -> Dict[str, Any]:
    mf = job_dir / "job_manifest.json"
    if not mf.exists():
        die(f"Không tìm thấy job_manifest.json trong {job_dir}")
    return json.loads(mf.read_text(encoding="utf-8"))


def _stage_day_dir(job_dir: Path, manifest: Dict[str, Any]) -> Path:
    """Đồng bộ dữ liệu từ _cloud_job/payload sang đúng cấu trúc outputs/<rel_day_dir> để mọi module chạy nguyên bản."""
    rel_day = manifest["rel_day_dir"]
    day_dir = ROOT / rel_day
    day_dir.mkdir(parents=True, exist_ok=True)
    payload_dir = job_dir / "payload"
    if payload_dir.exists():
        for item in payload_dir.iterdir():
            dest = day_dir / item.name
            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
    # Sửa đường dẫn tuyệt đối của Mac trong thethao.json / intro_hook.json
    for jf in ("thethao.json", "intro_hook.json"):
        jp = day_dir / jf
        if jp.exists():
            data = json.loads(jp.read_text(encoding="utf-8"))
            data = _fix_day_paths(data, day_dir)
            jp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return day_dir


# ==============================================================================
# 1. DAILY LONG / WEEKLY DIGEST (16:9) — SHARD & COMPOSE
# ==============================================================================

def _ensure_all_daily_tts(day_dir: Path, day_str: str, target_ids: Optional[List[int]] = None) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Sinh giọng đọc TTS cho các mục trong target_ids (hoặc toàn bộ nếu target_ids=None).
    Lưu ý: Để tính `global_offset_sec` chính xác trên từng shard khi chưa có đủ WAV của các shard khác,
    hàm này chỉ sinh TTS cho `target_ids` nếu các file khác đã có `duration` trong JSON;
    nếu chưa có `duration`, sinh TTS hoặc đọc từ audio có sẵn.
    """
    from vieneu import Vieneu

    audio_dir = day_dir / "audio"
    title_dir = day_dir / "audio-title"
    audio_dir.mkdir(parents=True, exist_ok=True)
    title_dir.mkdir(parents=True, exist_ok=True)

    tag = day_str.replace(".", "_")
    tts_cache = Path(paths.WORK) / f"tts_cache_cloud_{tag}"
    tts_cache.mkdir(parents=True, exist_ok=True)

    p_male = load_voice_preset("primary")
    p_female = load_voice_preset("secondary")
    model = None

    def get_model():
        nonlocal model
        if model is None:
            step("Khởi tạo mô hình ViTTS v3turbo...")
            model = Vieneu(mode="v3turbo")
        return model

    intro_p = day_dir / "intro_hook.json"
    intro = json.loads(intro_p.read_text(encoding="utf-8")) if intro_p.exists() else None
    if intro is not None:
        intro_wav = audio_dir / "audio_intro.wav"
        need_intro = (target_ids is None or 0 in target_ids)
        if intro_wav.exists() and intro_wav.stat().st_size > 30_000:
            dur = round(len(AudioSegment.from_wav(str(intro_wav))) / 1000.0, 2)
            intro["duration"] = dur
            intro["audio_duration"] = dur
            intro["audio_path"] = str(intro_wav)
            intro["audio_title"] = ""
        elif need_intro:
            segs = intro.get("voice_segments") or intro.get("segments") or []
            gap = AudioSegment.silent(duration=250, frame_rate=44100).set_channels(2)
            intro_audio = AudioSegment.silent(duration=0, frame_rate=44100).set_channels(2)
            for i, seg_obj in enumerate(segs):
                vp = seg_obj.get("voice_preset") or seg_obj.get("voice") or ("secondary" if i % 2 == 0 else "primary")
                pr = p_male if vp == "primary" else p_female
                seg = _synth_text_chunks(get_model(), seg_obj["text"], pr, tts_cache)
                if i > 0:
                    intro_audio += gap
                intro_audio += seg
            intro_audio = apply_voice_standard(intro_audio.set_frame_rate(44100).set_channels(2))
            intro_audio.export(str(intro_wav), format="wav")
            dur = round(len(intro_audio) / 1000.0, 2)
            intro["duration"] = dur
            intro["audio_duration"] = dur
            intro["audio_path"] = str(intro_wav)
            intro["audio_title"] = ""
            ok(f"[Cloud TTS Intro] {dur:.2f}s -> audio_intro.wav")
        intro_p.write_text(json.dumps(intro, ensure_ascii=False, indent=2), encoding="utf-8")

    items_p = day_dir / "thethao.json"
    items = json.loads(items_p.read_text(encoding="utf-8"))
    title_gap = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)

    for it in items:
        sc_id = int(it["id"])
        t_wav = title_dir / f"audio_title_{sc_id:02d}.wav"
        f_wav = audio_dir / f"audio_{sc_id:02d}.wav"
        need_this = (target_ids is None or sc_id in target_ids)

        if t_wav.exists() and f_wav.exists() and f_wav.stat().st_size > 30_000:
            f_dur = round(len(AudioSegment.from_wav(str(f_wav))) / 1000.0, 2)
            t_dur = round(len(AudioSegment.from_wav(str(t_wav))) / 1000.0, 2)
            it["duration"] = f_dur
            it["audio_duration"] = f_dur
            it["title_duration"] = t_dur
            it["audio_path"] = str(f_wav)
            it["audio_title"] = str(t_wav)
        elif need_this:
            vp = it.get("voice_preset") or ("primary" if (sc_id % 2 == 1) else "secondary")
            pr = p_male if vp == "primary" else p_female
            title_seg = _synth_text_chunks(get_model(), it["title"], pr, tts_cache)
            body_seg = _synth_text_chunks(get_model(), it["summary"], pr, tts_cache)
            full_seg = apply_voice_standard((title_seg + title_gap + body_seg).set_frame_rate(44100).set_channels(2))
            title_seg.export(str(t_wav), format="wav")
            full_seg.export(str(f_wav), format="wav")
            f_dur = round(len(full_seg) / 1000.0, 2)
            t_dur = round(len(title_seg) / 1000.0, 2)
            it["duration"] = f_dur
            it["audio_duration"] = f_dur
            it["title_duration"] = t_dur
            it["audio_path"] = str(f_wav)
            it["audio_title"] = str(t_wav)
            ok(f"[Cloud TTS Tin #{sc_id:02d}] full={f_dur:.2f}s (title={t_dur:.2f}s)")

    items_p.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    return intro, items


def run_daily_long_shard(day_dir: Path, day_str: str, shard_index: int, total_shards: int, out_dir: Path, workers: int = 2) -> None:
    items = json.loads((day_dir / "thethao.json").read_text(encoding="utf-8"))
    has_intro = (day_dir / "intro_hook.json").exists()
    all_ids: List[int] = ([0] if has_intro else []) + [int(it["id"]) for it in items]

    my_ids = [sc_id for idx, sc_id in enumerate(all_ids) if (idx % total_shards) == shard_index]
    banner(f"CLOUD SHARD {shard_index + 1}/{total_shards} — NGÀY {day_str}", f"Phụ trách các mục ID: {my_ids}")

    if not my_ids:
        ok(f"Shard {shard_index} không có mục nào cần xử lý.")
        return

    intro, items = _ensure_all_daily_tts(day_dir, day_str, target_ids=my_ids)
    date_chip = _format_vi_date_chip(day_str)
    all_plan_items = ([intro] if intro else []) + items
    compute_daily_plan(all_plan_items, date_chip, str(day_dir / "images"))

    tag = day_str.replace(".", "_")
    work_root = Path(paths.WORK) / f"cloud_daily_{tag}_s{shard_index}"
    bridges_dir = work_root / "bridges"
    bridges_dir.mkdir(parents=True, exist_ok=True)

    # Ước tính global_offset_sec cho hiệu ứng hạt/ticker
    id_to_dur: Dict[int, float] = {}
    if intro:
        id_to_dur[0] = float(intro.get("duration") or 40.0)
    for it in items:
        id_to_dur[int(it["id"])] = float(it.get("duration") or 45.0)

    render_jobs: List[Tuple[int, str, str, Path, List[Dict[str, Any]]]] = []
    for sc_id in my_ids:
        offset_sec = sum(id_to_dur.get(x, 45.0) for x in all_ids if x < sc_id)
        if sc_id == 0 and intro is not None:
            wav_p = Path(intro["audio_path"])
            b_dir = bridges_dir / "tin_00_intro_long"
            b_dir.mkdir(parents=True, exist_ok=True)
            _, tl_path, _ = export_bridge_project(
                str(day_dir), item_id=0, format_type="long", work_proj_dir=str(b_dir), global_offset_sec=offset_sec
            )
            tl_d = json.loads(Path(tl_path).read_text(encoding="utf-8"))
            tl_d["output_filename"] = "tin_00_long.mp4"
            tl_d["ticker_headlines"] = [it["title"].upper() for it in items[:8]]
            Path(tl_path).write_text(json.dumps(tl_d, ensure_ascii=False, indent=2), encoding="utf-8")
            render_jobs.append((0, "Intro", str(b_dir), wav_p, tl_d.get("sfx_events") or []))
        else:
            it_obj = next(x for x in items if int(x["id"]) == sc_id)
            wav_p = Path(it_obj["audio_path"])
            b_dir = bridges_dir / f"tin_{sc_id:02d}_long"
            b_dir.mkdir(parents=True, exist_ok=True)
            _, tl_path, _ = export_bridge_project(
                str(day_dir), item_id=sc_id, format_type="long", work_proj_dir=str(b_dir), global_offset_sec=offset_sec
            )
            tl_d = json.loads(Path(tl_path).read_text(encoding="utf-8"))
            tl_d["output_filename"] = f"tin_{sc_id:02d}_long.mp4"
            Path(tl_path).write_text(json.dumps(tl_d, ensure_ascii=False, indent=2), encoding="utf-8")
            render_jobs.append((sc_id, f"Tin #{sc_id:02d}", str(b_dir), wav_p, tl_d.get("sfx_events") or []))

    def _render_job(job: Tuple[int, str, str, Path, List[Dict[str, Any]]]) -> Dict[str, Any]:
        sc_id, lbl, b_dir, wav_p, sfx_ev = job
        step(f"[Shard {shard_index}] Render {lbl}...")
        mp4 = render_html_engine(
            project_dir=b_dir,
            template="long_sports_news_v2.html",
            scene_number=None,
            fps=30,
            preview=False,
            use_cache=False,
            force=True,
            format_override="long",
            video_only_output=True,
            jpeg_quality=88,
            hw_encode=True,
        )
        if not mp4 or not os.path.exists(mp4):
            die(f"Render thất bại cho {lbl}")

        shard_chunks = out_dir / "chunks"
        shard_audio = out_dir / "audio"
        shard_title = out_dir / "audio-title"
        for d in (shard_chunks, shard_audio, shard_title):
            d.mkdir(parents=True, exist_ok=True)

        dest_mp4 = shard_chunks / f"chunk_{sc_id:02d}.mp4"
        shutil.copy2(mp4, dest_mp4)
        dest_wav = shard_audio / wav_p.name
        shutil.copy2(wav_p, dest_wav)

        t_dur = 0.0
        if sc_id > 0:
            t_wav = day_dir / "audio-title" / f"audio_title_{sc_id:02d}.wav"
            if t_wav.exists():
                shutil.copy2(t_wav, shard_title / t_wav.name)
                t_dur = round(len(AudioSegment.from_wav(str(t_wav))) / 1000.0, 2)

        f_dur = round(len(AudioSegment.from_wav(str(wav_p))) / 1000.0, 2)
        return {
            "id": sc_id,
            "chunk_mp4": f"chunks/chunk_{sc_id:02d}.mp4",
            "audio_wav": f"audio/{wav_p.name}",
            "title_wav": f"audio-title/audio_title_{sc_id:02d}.wav" if sc_id > 0 else "",
            "duration": f_dur,
            "title_duration": t_dur,
            "sfx_events": sfx_ev,
        }

    results: List[Dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        for res in ex.map(_render_job, render_jobs):
            results.append(res)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"shard_{shard_index:02d}.json").write_text(
        json.dumps({"shard_index": shard_index, "items": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    ok(f"HOÀN TẤT SHARD {shard_index}: Đã xuất {len(results)} mảnh video/audio vào {out_dir}")


def run_daily_long_compose(day_dir: Path, day_str: str, shards_root: Path, final_out_dir: Path) -> None:
    banner(f"CLOUD COMPOSE — GHÉP MASTER VIDEO & AUDIO NGÀY {day_str}")
    dd_mm = "-".join(day_str.split(".")[:2])
    tag = day_str.replace(".", "_")
    work_root = Path(paths.WORK) / f"cloud_compose_{tag}"
    chunks_dir = work_root / "chunks"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    # Thu thập toàn bộ shard metadata & copy audio về day_dir
    audio_dir = day_dir / "audio"
    title_dir = day_dir / "audio-title"
    audio_dir.mkdir(parents=True, exist_ok=True)
    title_dir.mkdir(parents=True, exist_ok=True)

    shard_records: Dict[int, Tuple[Path, Path, List[Dict[str, Any]], float, float]] = {}
    for sf in sorted(shards_root.rglob("shard_*.json")):
        s_base = sf.parent
        s_data = json.loads(sf.read_text(encoding="utf-8"))
        for rec in s_data.get("items", []):
            sc_id = int(rec["id"])
            c_mp4 = s_base / rec["chunk_mp4"]
            a_wav = s_base / rec["audio_wav"]
            shutil.copy2(a_wav, audio_dir / a_wav.name)
            if rec.get("title_wav"):
                t_wav = s_base / rec["title_wav"]
                if t_wav.exists():
                    shutil.copy2(t_wav, title_dir / t_wav.name)
            shard_records[sc_id] = (
                c_mp4,
                audio_dir / a_wav.name,
                rec.get("sfx_events") or [],
                float(rec.get("duration", 0.0)),
                float(rec.get("title_duration", 0.0)),
            )

    items_p = day_dir / "thethao.json"
    items = json.loads(items_p.read_text(encoding="utf-8"))
    intro_p = day_dir / "intro_hook.json"
    intro = json.loads(intro_p.read_text(encoding="utf-8")) if intro_p.exists() else None

    if intro is not None and 0 in shard_records:
        _, w_p, _, dur, _ = shard_records[0]
        intro["duration"] = dur
        intro["audio_duration"] = dur
        intro["audio_path"] = str(w_p)
        intro_p.write_text(json.dumps(intro, ensure_ascii=False, indent=2), encoding="utf-8")

    for it in items:
        sc_id = int(it["id"])
        if sc_id not in shard_records:
            die(f"Thiếu mảnh render của Tin #{sc_id:02d} từ các shard!")
        _, w_p, _, f_dur, t_dur = shard_records[sc_id]
        it["duration"] = f_dur
        it["audio_duration"] = f_dur
        it["title_duration"] = t_dur
        it["audio_path"] = str(w_p)
        it["audio_title"] = str(title_dir / f"audio_title_{sc_id:02d}.wav")
    items_p.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    intro_bumper = ROOT / "logo" / "Intro.mp4"
    outro_bumper = ROOT / "logo" / "Outro.mp4"
    target_timescale = "15360"
    use_hw = _has_videotoolbox()
    v_enc_args = ["-c:v", "h264_videotoolbox", "-b:v", "2600k", "-maxrate", "3600k", "-bufsize", "5400k", "-pix_fmt", "yuv420p"] if use_hw else [
        "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-maxrate", "3600k", "-bufsize", "5400k", "-pix_fmt", "yuv420p"
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

    ordered_ids = ([0] if (intro is not None and 0 in shard_records) else []) + [int(it["id"]) for it in items]
    mid_vid_parts: List[Path] = []
    mid_aud_parts: List[Path] = []
    mid_sfx_events: List[Dict[str, Any]] = []
    chapters: List[Dict[str, Any]] = []
    cum_t = b_intro[2] if b_intro else 0.0
    mid_t = 0.0

    if 0 in shard_records:
        chapters.append({"time": "00:00", "seconds": 0.0, "label": f"Nhập cuộc & Tâm điểm thể thao {day_str}"})

    for sc_id in ordered_ids:
        mp4_p, wav_p, sfx_ev, _, _ = shard_records[sc_id]
        v_out = chunks_dir / f"seg_{sc_id:02d}_v.mp4"
        a_out = chunks_dir / f"seg_{sc_id:02d}_a.wav"
        _run_ffmpeg(
            ["ffmpeg", "-y", "-i", str(mp4_p), "-an", "-c:v", "copy", "-video_track_timescale", target_timescale, str(v_out)],
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
    ok(f"SFX track: {sfx_cnt} sự kiện âm thanh")

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
    chapters_file = preview_dir / f"chapters_{dd_mm.replace('-', '_')}.json"
    chapters_file.write_text(
        json.dumps({"day": day_str, "total_content_end_sec": round(cum_t, 3), "chapters": chapters}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Render bộ 3 Thumbnail 16:9 nếu có thumbnails_plan.json
    if (day_dir / "thumbnails_plan.json").exists():
        try:
            render_thumbnails(day_str)
        except Exception as e:
            warn(f"Không thể render thumbnails_plan.json: {e}")

    # Đóng gói toàn bộ file đầu ra vào final_out_dir để GitHub Actions upload artifact
    final_out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_mp4, final_out_dir / out_mp4.name)
    for f_name in ("thethao.json", "intro_hook.json", "thumbnail.jpg", "thumbnail_A.jpg", "thumbnail_B.jpg", "thumbnail_C.jpg", "mota.txt"):
        fp = day_dir / f_name
        if fp.exists():
            shutil.copy2(fp, final_out_dir / f_name)
    for sub in ("audio", "audio-title", "_preview_v2"):
        sp = day_dir / sub
        if sp.exists():
            dest_sub = final_out_dir / sub
            if dest_sub.exists():
                shutil.rmtree(dest_sub)
            shutil.copytree(sp, dest_sub)

    vd_final = _probe_dur(str(out_mp4), "v:0")
    ad_final = _probe_dur(str(out_mp4), "a:0")
    drift_ms = abs(vd_final - ad_final) * 1000.0
    final_stats = measure_loudness(str(out_mp4)) or {}
    ok(f"HOÀN TẤT CLOUD COMPOSE 16:9 -> {out_mp4.name}")
    ok(f"Video={vd_final:.3f}s | Audio={ad_final:.3f}s | Drift={drift_ms:.2f}ms | I={final_stats.get('input_i')} LUFS | TP={final_stats.get('input_tp')} dBTP")


# ==============================================================================
# 2. SHORT BATCH (9:16) — SHARD & COMPOSE (HỖ TRỢ MỌI LOẠI VIDEO SHORT)
# ==============================================================================

def run_short_batch_shard(day_dir: Path, day_str: str, shard_index: int, total_shards: int, out_dir: Path) -> None:
    """
    Chạy dựng video Short 9:16 trên đám mây.
    Hỗ trợ cả 2 chế độ:
      A) Từ `shorts_spec.json` (cấu trúc chuẩn `diemdoc.short_batch` với `voice_segments`, `sentence_charts`, `hook`, `thumb`).
      B) Từ `thethao.json` đã chuẩn bị sẵn trong `day_dir` (khi người dùng truyền `--mode short_batch` cho các tin có sẵn).
    """
    from vieneu import Vieneu

    spec_file = day_dir / "shorts_spec.json"
    ctx = ShortDayContext(
        day_dir=day_dir,
        inspect_dir=day_dir / "images",
        work_tag=f"cloud_short_{day_str.replace('.', '_')}_s{shard_index}",
    )
    ctx.ensure_dirs()

    if spec_file.exists():
        all_specs: List[Dict[str, Any]] = json.loads(spec_file.read_text(encoding="utf-8"))
        my_specs = [sp for idx, sp in enumerate(all_specs) if (idx % total_shards) == shard_index]
        banner(f"CLOUD SHORT SHARD {shard_index + 1}/{total_shards} ({day_str})", f"Số lượng Shorts trong shard: {len(my_specs)}")
        if not my_specs:
            return

        all_credits: Dict[str, str] = {}
        for item in my_specs:
            # Nếu ảnh đã nằm sẵn trong day_dir/images thì chỉ kiểm tra và tạo contact sheet
            for img_sp in item.get("images", []):
                img_sp["abs_src"] = str(day_dir / "images" / (img_sp.get("dest") or img_sp.get("src")))
            all_credits.update(copy_and_verify_images(ctx, item))
            build_contact_sheet(ctx, item)

        tts_model = Vieneu(mode="v3turbo")
        audio_meta: Dict[int, Dict[str, Any]] = {}
        for item in my_specs:
            audio_meta[int(item["id"])] = synthesize_item_audio(ctx, tts_model, item)

        merge_day_metadata(ctx, my_specs, all_credits, audio_meta)
        for item in my_specs:
            build_and_publish_short(ctx, item)
    else:
        # Chế độ B: Dựng trực tiếp từ thethao.json có sẵn trong day_dir
        items = json.loads((day_dir / "thethao.json").read_text(encoding="utf-8"))
        my_items = [it for idx, it in enumerate(items) if (idx % total_shards) == shard_index]
        banner(f"CLOUD SHORT (THETHAO.JSON) SHARD {shard_index + 1}/{total_shards}", f"Số tin: {len(my_items)}")
        if not my_items:
            return

        my_ids = [int(it["id"]) for it in my_items]
        _, items = _ensure_all_daily_tts(day_dir, day_str, target_ids=my_ids)
        for it in items:
            sc_id = int(it["id"])
            if sc_id not in my_ids:
                continue
            slug = it.get("slug") or f"Short_{sc_id:02d}"
            work_proj_dir = os.path.join(ctx.work_shorts_dir, f"short_{sc_id}")
            pdir, _, _ = export_bridge_project(
                day_dir=str(day_dir),
                item_id=str(sc_id),
                format_type="short",
                work_proj_dir=work_proj_dir,
                global_offset_sec=0.0,
            )
            out_work_mp4 = render_html_engine(
                project_dir=str(pdir),
                template="short_news_v2.html",
                scene_number=None,
                fps=30,
                preview=False,
                force=True,
            )
            out_mp4 = ctx.shorts_dir / f"{slug}.mp4"
            shutil.copy2(out_work_mp4, str(out_mp4))
            if it.get("include_outro", True):
                append_short_outro(out_mp4, voice_hint=it.get("voice_preset"))

    # Gom kết quả của shard vào out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    for sub in ("shorts", "audio", "audio-title", "qa"):
        sp = day_dir / sub
        if sp.exists():
            dest_s = out_dir / sub
            if dest_s.exists():
                shutil.rmtree(dest_s)
            shutil.copytree(sp, dest_s)
    for jf in ("thethao.json", "image_plan.json", "image_credits.json"):
        jp = day_dir / jf
        if jp.exists():
            shutil.copy2(jp, out_dir / f"shard_{shard_index:02d}_{jf}")
    ok(f"HOÀN TẤT SHORT SHARD {shard_index} -> {out_dir}")


def run_short_batch_compose(day_dir: Path, shards_root: Path, final_out_dir: Path) -> None:
    banner("CLOUD SHORT COMPOSE — HỢP NHẤT VIDEO SHORTS & METADATA")
    final_out_dir.mkdir(parents=True, exist_ok=True)

    for sub in ("shorts", "audio", "audio-title", "qa"):
        target_sub = final_out_dir / sub
        target_sub.mkdir(parents=True, exist_ok=True)
        for sp in sorted(shards_root.rglob(sub)):
            if sp.is_dir():
                for f in sp.iterdir():
                    if f.is_file():
                        shutil.copy2(f, target_sub / f.name)

    # Hợp nhất thethao.json từ các shard
    merged_tt: Dict[int, Dict[str, Any]] = {}
    if (day_dir / "thethao.json").exists():
        for row in json.loads((day_dir / "thethao.json").read_text(encoding="utf-8")):
            merged_tt[int(row["id"])] = row
    for tf in sorted(shards_root.rglob("shard_*_thethao.json")):
        for row in json.loads(tf.read_text(encoding="utf-8")):
            rid = int(row["id"])
            if row.get("audio_path") or rid not in merged_tt:
                merged_tt[rid] = row
    if merged_tt:
        ordered_tt = [merged_tt[k] for k in sorted(merged_tt.keys())]
        (final_out_dir / "thethao.json").write_text(json.dumps(ordered_tt, ensure_ascii=False, indent=2), encoding="utf-8")

    ok(f"Đã hợp nhất toàn bộ Shorts vào {final_out_dir}")


# ==============================================================================
# 3. DIGEST SHORT (9:16 — ĐỌC NHANH 17-26 TIN < 3 PHÚT)
# ==============================================================================

def run_digest_short_cloud(day_dir: Path, day_str: str, final_out_dir: Path) -> None:
    """
    Chạy dựng Digest Short (Bản tin nhanh 17–26 tin < 180s) từ file `shorts/digest_specs.json`
    hoặc `digest_specs.json` đặt trong `day_dir`.
    """
    from vieneu import Vieneu

    spec_p = day_dir / "shorts" / "digest_specs.json"
    if not spec_p.exists():
        spec_p = day_dir / "digest_specs.json"
    if not spec_p.exists():
        die(f"Không tìm thấy digest_specs.json trong {day_dir}")

    cfg = json.loads(spec_p.read_text(encoding="utf-8"))
    digest_specs: List[Dict[str, Any]] = cfg["items"] if isinstance(cfg, dict) and "items" in cfg else cfg
    total_items = len(digest_specs)

    out_video_name = cfg.get("out_video_name", f"Short_Tin_Nhanh_{total_items}_Tin.mp4") if isinstance(cfg, dict) else f"Short_Tin_Nhanh_{total_items}_Tin.mp4"
    out_thumb_name = out_video_name.replace(".mp4", "_thumbnail.jpg")
    out_mota_name = out_video_name.replace(".mp4", "_mota.txt")

    images_dir = day_dir / "images"
    shorts_dir = day_dir / "shorts"
    digest_audio_dir = shorts_dir / "digest_audio"
    qa_dir = day_dir / "qa"
    work_dir = Path(paths.WORK) / f"cloud_digest_{day_str.replace('.', '_')}"
    tts_cache_dir = Path(paths.WORK) / f"tts_cache_digest_{day_str.replace('.', '_')}"
    for d in (shorts_dir, digest_audio_dir, qa_dir, work_dir, tts_cache_dir):
        d.mkdir(parents=True, exist_ok=True)

    thethao_items = {int(it["id"]): it for it in json.loads((day_dir / "thethao.json").read_text(encoding="utf-8"))} if (day_dir / "thethao.json").exists() else {}
    credits_map = json.loads((day_dir / "image_credits.json").read_text(encoding="utf-8")) if (day_dir / "image_credits.json").exists() else {}

    male_preset = load_voice_preset("primary")
    female_preset = load_voice_preset("secondary")
    model = Vieneu(mode="v3turbo")

    gap_ms = int(cfg.get("gap_ms", 220)) if isinstance(cfg, dict) else 220
    gap_seg = AudioSegment.silent(duration=gap_ms, frame_rate=44100).set_channels(2)
    combined_voice = AudioSegment.silent(duration=0, frame_rate=44100).set_channels(2)

    items_data: List[Dict[str, Any]] = []
    all_words: List[Dict[str, Any]] = []
    all_karaoke: List[Dict[str, Any]] = []
    raw_sfx: List[Dict[str, Any]] = []
    cum_sec = 0.0

    for idx, spec in enumerate(digest_specs, 1):
        sc_id = int(spec["id"])
        orig_item = thethao_items.get(sc_id, {})
        img_path = images_dir / spec["image_file"]
        preset = male_preset if spec.get("voice_preset") == "primary" else female_preset
        digest_text = spec["digest_line"].strip()
        tts_str, _ = prepare(digest_text)

        wav_out = digest_audio_dir / f"tin_{sc_id:02d}.wav"
        seg, _ = render_chunk_vitts(
            model, tts_str, preset["voice_id"],
            temperature=preset["temperature"], speed=preset["speed"], pitch=preset["pitch"],
            cache_dir=str(tts_cache_dir), use_cache=True, max_chars=768,
        )
        seg = apply_voice_standard(trim_segment_silence(seg).set_frame_rate(44100).set_channels(2))
        seg.export(str(wav_out), format="wav")
        it_dur = round(len(seg) / 1000.0, 3)

        if idx > 1:
            combined_voice += gap_seg
            cum_sec += gap_ms / 1000.0
            raw_sfx.append({"sfx": "whoosh_cinematic_short.mp3", "time": round(cum_sec, 3), "volume": 0.20})

        it_start = round(cum_sec, 3)
        combined_voice += seg
        cum_sec += len(seg) / 1000.0
        it_end = round(cum_sec, 3)

        s_words = interpolate_sentence_words(digest_text, 0.0, it_dur)
        abs_words = []
        for w in s_words:
            aw = {"word": w["word"], "start": round(it_start + w["start"], 3), "end": round(it_start + w["end"], 3), "matched": True}
            abs_words.append(aw)
            all_words.append(aw)

        for ci in range(0, len(abs_words), 4):
            c_words = abs_words[ci : ci + 4]
            all_karaoke.append({
                "start": c_words[0]["start"],
                "end": c_words[-1]["end"],
                "text": " ".join(cw["word"] for cw in c_words),
                "words": c_words,
            })

        pan_info = compute_pan_params(str(img_path), duration=it_dur, dir_toggle=(idx % 2 == 1))
        photo_credit = credits_map.get(spec["image_file"]) or orig_item.get("credit", "REUTERS")
        news_source = orig_item.get("news_source") or orig_item.get("source") or "VNEXPRESS"

        items_data.append({
            "id": str(sc_id),
            "title": spec["title"],
            "digest_line": digest_text,
            "region": spec.get("region", ""),
            "voice_gender": spec.get("voice_gender", ""),
            "voice_label": preset["voice_label"],
            "image": str(img_path),
            "credit": photo_credit,
            "news_source": news_source,
            "start": it_start,
            "end": it_end,
            "duration": it_dur,
            **pan_info,
        })

    voiceover_wav = work_dir / "voiceover.wav"
    combined_voice.export(str(voiceover_wav), format="wav")
    body_dur = round(len(combined_voice) / 1000.0, 3)
    date_chip = _format_vi_date_chip(day_str)

    # Kiểm tra trần 180s tính cả Outro (~6.5s)
    if body_dur + 6.55 >= 180.0:
        die(f"Digest Short quá dài: body={body_dur:.2f}s (+Outro ~6.5s >= 180s)! Hãy rút gọn digest_line.")

    # Tạo bảng đối chứng Contact Sheet QA cho Digest Short
    try:
        from PIL import Image, ImageDraw, ImageFont
        cols = 4
        rows = (len(items_data) + cols - 1) // cols
        cell_w, cell_h, thumb_w, thumb_h, margin, header_h = 460, 340, 432, 238, 20, 72
        sheet = Image.new("RGB", (cols * cell_w + margin * 2, rows * cell_h + margin * 2 + header_h), (8, 13, 24))
        draw = ImageDraw.Draw(sheet)
        f_bold = ROOT / "assets" / "fonts" / "Be_Vietnam_Pro" / "BeVietnamPro-Bold.ttf"
        f_semi = ROOT / "assets" / "fonts" / "Be_Vietnam_Pro" / "BeVietnamPro-SemiBold.ttf"
        f_hdr = ImageFont.truetype(str(f_bold), 24) if f_bold.exists() else ImageFont.load_default()
        f_lbl = ImageFont.truetype(str(f_bold), 15) if f_bold.exists() else ImageFont.load_default()
        f_sub = ImageFont.truetype(str(f_semi), 13) if f_semi.exists() else ImageFont.load_default()
        draw.text((margin, 22), f"KIỂM DUYỆT {len(items_data)} ẢNH DIGEST SHORT ({day_str}) — VIỆT NAM: NỮ | QUỐC TẾ: NAM", fill=(0, 229, 255), font=f_hdr)
        for idx, rec in enumerate(items_data):
            r, c = divmod(idx, cols)
            x0, y0 = margin + c * cell_w, header_h + margin + r * cell_h
            img_p = Path(rec["image"])
            with Image.open(img_p) as im:
                iw, ih = im.size
                im_rgb = im.convert("RGB")
                im_rgb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                tw, th = im_rgb.size
                sheet.paste(im_rgb, (x0 + 14 + (thumb_w - tw) // 2, y0 + 6 + (thumb_h - th) // 2))
            tag_color = (56, 189, 248) if rec.get("voice_gender") == "Nam" else (244, 114, 182)
            draw.rectangle([x0 + 10, y0 + 4, x0 + cell_w - 10, y0 + thumb_h + 8], outline=tag_color, width=2)
            draw.text((x0 + 12, y0 + thumb_h + 14), f"[{int(rec['id']):02d}] {rec.get('region', '')} ({rec.get('voice_gender', '')}) · {img_p.name} ({iw}x{ih})", fill=tag_color, font=f_lbl)
            draw.text((x0 + 12, y0 + thumb_h + 38), f"📷 {rec['credit']} | {rec['digest_line'][:44]}...", fill=(226, 232, 240), font=f_sub)
            draw.text((x0 + 12, y0 + thumb_h + 58), f"📰 {rec['news_source']}", fill=(148, 163, 184), font=f_sub)
        dd_mm_u = "_".join(day_str.split(".")[:2])
        sheet.save(str(qa_dir / f"contact_digest_{dd_mm_u}.jpg"), quality=92)
    except Exception as e:
        warn(f"Không thể tạo Contact Sheet Digest: {e}")

    # Lưu script export JSON
    dd_mm_u = "_".join(day_str.split(".")[:2])
    (shorts_dir / f"digest_script_{dd_mm_u}.json").write_text(
        json.dumps({"day": day_str, "total_items": len(items_data), "body_duration_sec": body_dur, "items": items_data}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    fx_cfg = json.loads((Path(paths.CONFIG) / "fx.json").read_text(encoding="utf-8")) if (Path(paths.CONFIG) / "fx.json").exists() else {}
    timeline = {
        "title": cfg.get("title", f"TIN NHANH THỂ THAO {'.'.join(day_str.split('.')[:2])}") if isinstance(cfg, dict) else "TIN NHANH THỂ THAO",
        "channel_name": "ĐIỂM ĐỌC",
        "date_str": date_chip,
        "date_chip": date_chip,
        "hide_date_chip": bool(cfg.get("hide_date_chip", False)) if isinstance(cfg, dict) else False,
        "total_duration": body_dur,
        "format": "short",
        "template": "short_digest_v2.html",
        "dimensions": [1080, 1920],
        "fps": 30,
        "bgm": "bgm_editorial_2_momentum.mp3",
        "bgm_volume": 0.06,
        "audio_path": str(voiceover_wav),
        "global_offset_sec": 0.0,
        "fx": fx_cfg,
        "sfx_events": raw_sfx,
        "items": items_data,
        "karaoke_chunks": all_karaoke,
    }
    (work_dir / "video_timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    (work_dir / "word_timestamps.json").write_text(json.dumps({"words": all_words, "karaoke_chunks": all_karaoke}, ensure_ascii=False, indent=2), encoding="utf-8")

    rendered_body = render_html_engine(
        project_dir=str(work_dir),
        template="short_digest_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        use_cache=False,
        force=True,
    )
    out_video = shorts_dir / out_video_name
    last_voice = digest_specs[-1].get("voice_preset", "primary")
    final_path, chosen_outro = append_short_outro(rendered_body, voice_hint=last_voice, out_path=out_video, enabled=True)

    v_dur = _probe_dur(str(final_path), "v:0")
    a_dur = _probe_dur(str(final_path), "a:0")
    drift_ms = abs(v_dur - a_dur) * 1000.0
    stats = measure_loudness(str(final_path)) or {}
    if v_dur >= 180.0:
        die(f"Video sau Outro dài {v_dur:.2f}s >= 180.0s!")
    if drift_ms > 33.3:
        die(f"Lệch A/V vượt ngưỡng 33.3ms: {drift_ms:.2f}ms")

    if isinstance(cfg, dict) and cfg.get("thumb"):
        t_cfg = cfg["thumb"]
        render_thumbnail_9x16(
            out_path=shorts_dir / out_thumb_name,
            image_path=images_dir / t_cfg["image"],
            kicker=t_cfg["kicker"],
            hero_html=t_cfg["hero_html"],
            subtitle=t_cfg["subtitle"],
            badge=t_cfg["badge"],
            tag_a=t_cfg["tag_a"],
            tag_b=t_cfg["tag_b"],
            hero_size=t_cfg.get("hero_size"),
            obj_pos=t_cfg.get("obj_pos", "center 20%"),
        )

    if isinstance(cfg, dict) and cfg.get("seo_title"):
        chapters_list = [(f"{int(it['start']) // 60:02d}:{int(it['start']) % 60:02d}", it["title"]) for it in items_data]
        write_mota_9x16(
            out_path=shorts_dir / out_mota_name,
            seo_title=cfg["seo_title"],
            description_paragraphs=cfg.get("description", []),
            chapters=chapters_list,
            sources_line=cfg.get("sources_line", "📰 Nguồn tin: VnExpress, Thanh Niên, Tuổi Trẻ, Dân Trí, Reuters, AP."),
            hashtags=cfg.get("hashtags", ["#Shorts", "#TinNhanh", "#DiemDoc"]),
            tiktok_caption=cfg.get("tiktok_caption"),
            fb_hook=cfg.get("fb_hook"),
        )

    final_out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(shorts_dir, final_out_dir / "shorts", dirs_exist_ok=True)
    if qa_dir.exists():
        shutil.copytree(qa_dir, final_out_dir / "qa", dirs_exist_ok=True)
    ok(f"HOÀN TẤT CLOUD DIGEST SHORT -> {out_video.name} | Dur={v_dur:.2f}s | Drift={drift_ms:.2f}ms | I={stats.get('input_i')} LUFS | TP={stats.get('input_tp')} dBTP | Outro={chosen_outro.name if chosen_outro else 'None'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Cloud Worker cho GitHub Actions (DD-The-thao)")
    parser.add_argument("--job-dir", default="_cloud_job", help="Thư mục chứa job_manifest.json và payload/")
    parser.add_argument("--role", choices=["shard", "compose"], required=True)
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--total-shards", type=int, default=1)
    parser.add_argument("--shards-dir", default="_cloud_shards", help="Thư mục chứa artifacts của các shard (cho role=compose)")
    parser.add_argument("--out-dir", default="_cloud_out", help="Thư mục xuất kết quả của worker")
    parser.add_argument("--workers", type=int, default=2, help="Số luồng Playwright bên trong 1 máy ảo")
    args = parser.parse_args()

    job_dir = ROOT / args.job_dir
    manifest = _load_job_manifest(job_dir)
    mode = manifest["mode"]
    day_str = manifest["day"]
    day_dir = _stage_day_dir(job_dir, manifest)
    out_dir = Path(args.out_dir).resolve()

    if mode == "daily_long":
        if args.role == "shard":
            run_daily_long_shard(day_dir, day_str, args.shard_index, args.total_shards, out_dir, workers=args.workers)
        else:
            run_daily_long_compose(day_dir, day_str, Path(args.shards_dir).resolve(), out_dir)
    elif mode == "short_batch":
        if args.role == "shard":
            run_short_batch_shard(day_dir, day_str, args.shard_index, args.total_shards, out_dir)
        else:
            run_short_batch_compose(day_dir, Path(args.shards_dir).resolve(), out_dir)
    elif mode == "digest_short":
        if args.role == "shard":
            if args.shard_index == 0:
                run_digest_short_cloud(day_dir, day_str, out_dir)
        else:
            # Copy từ shard 0 sang final_out_dir
            s0 = Path(args.shards_dir).resolve()
            out_dir.mkdir(parents=True, exist_ok=True)
            for item in s0.rglob("*"):
                if item.is_file():
                    rel = item.relative_to(s0)
                    parts = rel.parts
                    # Bỏ qua thư mục bọc shard_00 nếu có
                    if parts[0].startswith("shard-"):
                        rel = Path(*parts[1:])
                    dest = out_dir / rel
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest)
    else:
        die(f"Chế độ mode không hợp lệ: {mode}")


if __name__ == "__main__":
    main()
