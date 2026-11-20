#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_weekly_tts_16_11.py — Pha 1 (Bước 2): Sinh giọng đọc ViTTS v3turbo v4.1 No-Cut
luân phiên Nam (Minh Quân Pro Mẫu 15) / Nữ (Ngọc Huyền Mẫu 14) cho Intro + 26 bản tin tuần 16.11.2026.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse
import json
import shutil
import time
from pathlib import Path
from typing import Any, Dict

from pydub import AudioSegment

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
if os.path.join(_HERE, "vendor") not in sys.path:
    sys.path.insert(0, os.path.join(_HERE, "vendor"))

from diemdoc import paths
from diemdoc.audio import apply_voice_standard
from diemdoc.log import banner, ok, step, warn
from diemdoc.publisher import load_voice_preset
from diemdoc.tts_text import prepare
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from vieneu import Vieneu

DAY_STR = "16.11.2026"
ROOT = Path(_ROOT)
DAY_DIR = ROOT / "outputs" / DAY_STR
AUDIO_DIR = DAY_DIR / "audio"
TITLE_DIR = DAY_DIR / "audio-title"
CACHE_DIR = os.path.join(paths.WORK, "tts_cache_weekly_16_11")


def synth_text_with_preset(model: Any, text: str, preset_key: str) -> AudioSegment:
    """Tổng hợp văn bản theo preset giọng chuẩn và cân chỉnh -16.0 LUFS."""
    p_info = load_voice_preset(preset_key)
    voice_id = p_info["voice_id"]
    spd, pch, temp = p_info["speed"], p_info["pitch"], p_info["temperature"]
    clean_text, _ = prepare(text)
    chunks = build_chunks_from_text(clean_text, max_words_per_chunk=60, inter_sentence_pause=0.25)
    seg = AudioSegment.empty()
    for ch in chunks:
        c_seg, _ = render_chunk_vitts(
            model,
            ch["text"],
            voice_id,
            temperature=temp,
            speed=spd,
            pitch=pch,
            cache_dir=CACHE_DIR,
            use_cache=True,
            max_chars=768,
        )
        seg += trim_segment_silence(c_seg)
        pause_ms = int(round(ch.get("pause_after", 0.25) * 1000))
        if pause_ms > 0:
            seg += AudioSegment.silent(duration=pause_ms)
    return apply_voice_standard(seg.set_frame_rate(44100).set_channels(2))


def synth_intro(model: Any, intro_item: Dict[str, Any], force: bool = False) -> Dict[str, Any]:
    title_out = TITLE_DIR / "audio_title_intro.wav"
    full_out = AUDIO_DIR / "audio_intro.wav"
    title_text = (intro_item.get("title") or "").strip()
    need_title = bool(title_text) and not bool(intro_item.get("hide_title", False))

    if (not force) and ((not need_title) or title_out.exists()) and full_out.exists() and full_out.stat().st_size > 50_000:
        dur = round(AudioSegment.from_wav(str(full_out)).duration_seconds, 2)
        ok(f"[Intro] Đã có sẵn audio ({dur}s), bỏ qua.")
        intro_item["duration"] = dur
        return intro_item

    step("[Intro] Tổng hợp Song giọng Nữ (Ngọc Huyền) + Nam (Minh Quân Pro)...")

    segs = intro_item.get("voice_segments", [])
    summary_seg = AudioSegment.empty()
    for idx, vs in enumerate(segs):
        vp = vs["voice_preset"]
        p_info = load_voice_preset(vp)
        step(f"  Intro Câu {idx + 1}/{len(segs)} [{p_info['voice_label']}]")
        s_std = synth_text_with_preset(model, vs["text"], vp)
        if idx > 0:
            summary_seg += AudioSegment.silent(duration=250, frame_rate=44100).set_channels(2)
        summary_seg += s_std

    if need_title:
        # Tiêu đề Intro đọc bằng giọng Nữ để tạo mở đầu sáng rõ
        title_std = synth_text_with_preset(model, title_text, "secondary")
        title_std.export(str(title_out), format="wav")
        combined = title_std + AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2) + summary_seg
        combined = combined.set_frame_rate(44100).set_channels(2)
        combined.export(str(full_out), format="wav")
        dur = round(combined.duration_seconds, 2)
        title_dur = round(title_std.duration_seconds, 2)
        intro_item["audio_title"] = str(title_out)
        ok(f"[Intro] Hoàn tất: full={dur}s (title={title_dur}s) -> {full_out.name}")
    else:
        if title_out.exists():
            trash_dir = Path.home() / ".Trash"
            trash_dir.mkdir(parents=True, exist_ok=True)
            trash_dst = trash_dir / f"{title_out.stem}_{int(time.time())}{title_out.suffix}"
            shutil.move(str(title_out), str(trash_dst))
        combined = summary_seg.set_frame_rate(44100).set_channels(2)
        combined.export(str(full_out), format="wav")
        dur = round(combined.duration_seconds, 2)
        intro_item["audio_title"] = ""
        ok(f"[Intro] Hoàn tất (không tiêu đề): full={dur}s -> {full_out.name}")

    intro_item["duration"] = dur
    intro_item["audio_path"] = str(full_out)
    return intro_item


def synth_news_item(model: Any, item: Dict[str, Any], force: bool = False) -> Dict[str, Any]:
    sc_id = int(item["id"])
    title_out = TITLE_DIR / f"audio_title_{sc_id:02d}.wav"
    full_out = AUDIO_DIR / f"audio_{sc_id:02d}.wav"

    if (not force) and title_out.exists() and full_out.exists() and full_out.stat().st_size > 50_000:
        dur = round(AudioSegment.from_wav(str(full_out)).duration_seconds, 2)
        ok(f"[Tin #{sc_id:02d}] Đã có sẵn audio ({dur}s), bỏ qua.")
        item["duration"] = dur
        return item

    preset_key = item.get("voice_preset") or ("primary" if sc_id % 2 == 1 else "secondary")
    p_info = load_voice_preset(preset_key)
    step(f"[Tin #{sc_id:02d}/26] Giọng {p_info['voice_label']}: {item['title'][:52]}...")

    title_std = synth_text_with_preset(model, item["title"], preset_key)
    title_std.export(str(title_out), format="wav")

    summary_std = synth_text_with_preset(model, item["summary"], preset_key)
    combined = title_std + AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2) + summary_std
    combined = apply_voice_standard(combined.set_frame_rate(44100).set_channels(2))
    combined.export(str(full_out), format="wav")

    dur = round(combined.duration_seconds, 2)
    title_dur = round(title_std.duration_seconds, 2)
    item["duration"] = dur
    item["audio_path"] = str(full_out)
    item["audio_title"] = str(title_out)
    ok(f"  -> Tin #{sc_id:02d}: full={dur}s (title={title_dur}s) [{p_info['voice_label']}]")
    return item


def main() -> None:
    parser = argparse.ArgumentParser(description="Pha 1 Bước 2: Sinh âm thanh ViTTS song giọng tuần 16.11.2026")
    parser.add_argument("--force", action="store_true", help="Sinh lại toàn bộ file âm thanh")
    parser.add_argument("--only", type=int, nargs="+", help="Chỉ sinh cho scene_id cụ thể (0=Intro, 1..26)")
    args = parser.parse_args()

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    TITLE_DIR.mkdir(parents=True, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

    intro_path = DAY_DIR / "intro_hook.json"
    tt_path = DAY_DIR / "thethao.json"
    if not intro_path.exists() or not tt_path.exists():
        raise FileNotFoundError("Thiếu intro_hook.json hoặc thethao.json — hãy chạy prepare_weekly_16_11.py trước.")

    intro_item = json.loads(intro_path.read_text(encoding="utf-8"))
    items = json.loads(tt_path.read_text(encoding="utf-8"))
    only_set = set(args.only) if args.only else None

    banner(f"PHA 1 BƯỚC 2 — TỔNG HỢP GIỌNG ĐỌC LUÂN PHIÊN NAM/NỮ TUẦN {DAY_STR}", "ViTTS v3turbo v4.1 No-Cut")
    model = Vieneu(mode="v3turbo")

    if only_set is None or 0 in only_set:
        intro_item = synth_intro(model, intro_item, force=args.force)
        intro_path.write_text(json.dumps(intro_item, ensure_ascii=False, indent=2), encoding="utf-8")

    total_sec = float(intro_item.get("duration") or 0.0)
    for idx, it in enumerate(items):
        sc_id = int(it["id"])
        if only_set is None or sc_id in only_set:
            items[idx] = synth_news_item(model, it, force=args.force)
        total_sec += float(items[idx].get("duration") or 0.0)

    tt_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    ok("=" * 72)
    ok(f"HOÀN TẤT ÂM THANH PHA 1: Intro ({intro_item.get('duration')}s) + 26 bản tin!")
    ok(f"Tổng thời lượng lời đọc: {total_sec:.1f}s (~{total_sec / 60:.2f} phút)")
    if not (24.0 <= float(intro_item.get("duration") or 0.0) <= 32.0):
        warn(f"Cảnh báo: audio_intro.wav = {intro_item.get('duration')}s (ngoài khoảng 24-32s)")


if __name__ == "__main__":
    main()
