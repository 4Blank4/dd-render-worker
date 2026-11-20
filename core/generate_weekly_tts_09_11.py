#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_weekly_tts_09_11.py — Sinh giọng đọc ViTTS v3turbo Minh Quân Pro Mẫu 15
cho 25 bản tin tuần 09.11.2026 với chuẩn âm lượng -16.0 LUFS (EBU R128).
"""

import sys
sys.dont_write_bytecode = True

import os
import json
from pathlib import Path
from typing import Optional

from pydub import AudioSegment

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.diemdoc import paths
from core.diemdoc.log import log, ok, warn
from core.diemdoc.audio import apply_voice_standard
from core.diemdoc.tts_text import prepare
from core.vendor.vieneu import Vieneu

DAY_DIR = ROOT / "outputs" / "09.11.2026"
AUDIO_DIR = DAY_DIR / "audio"
TITLE_DIR = DAY_DIR / "audio-title"
CACHE_DIR = paths.work_file("vitts_cache")

for d in (AUDIO_DIR, TITLE_DIR):
    d.mkdir(parents=True, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# Preset Giọng Nam chính Minh Quân Pro Mẫu 15 (Cập nhật 07-08.11.2026)
V_VOICE = "male"
V_SPEED = 1.12
V_PITCH = 0.93


def synthesize_text(model: Vieneu, text: str, voice: str = V_VOICE, speed: float = V_SPEED, pitch: float = V_PITCH) -> AudioSegment:
    """Tổng hợp âm thanh qua ViNeu-TTS với chuẩn hoá từ viết tắt và cache SHA-256."""
    tts_text, _ = prepare(text)
    
    # Chia câu nhỏ để ViTTS đọc tự nhiên không hụt hơi (ngắt tại chấm, phẩy lớn)
    raw_wav = model.synthesize(
        tts_text,
        voice=voice,
        speed=speed,
        pitch=pitch,
        cache_dir=str(CACHE_DIR)
    )
    return AudioSegment.from_file(raw_wav, format="wav")


def main():
    json_path = DAY_DIR / "thethao.json"
    if not json_path.exists():
        print(f"Error: Không tìm thấy {json_path}")
        sys.exit(1)

    items = json.loads(json_path.read_text(encoding="utf-8"))
    print(f"=== BẮT ĐẦU SINH GIỌNG ĐỌC MINH QUÂN PRO MẪU 15 CHO {len(items)} BẢN TIN ===")
    print(f"Preset: voice={V_VOICE}, speed={V_SPEED}, pitch={V_PITCH}, target_loudness=-16.0 LUFS")
    print("=" * 80)

    model = Vieneu(mode="v3turbo")
    silence_08 = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)

    total_duration_sec = 0.0

    for idx, item in enumerate(items, 1):
        sc_num = f"{idx:02d}"
        target_audio = AUDIO_DIR / f"audio_{sc_num}.wav"
        target_title = TITLE_DIR / f"audio_title_{sc_num}.wav"

        print(f"[{idx:02d}/{len(items):02d}] Đang xử lý Tin {sc_num}: {item['title'][:45]}...")

        # 1. Sinh Audio Tiêu đề
        seg_title = synthesize_text(model, item["title"])
        seg_title = seg_title.set_frame_rate(44100).set_channels(2)
        seg_title.export(str(target_title), format="wav")

        # 2. Sinh Audio Chi tiết
        seg_summary = synthesize_text(model, item["summary"])

        # 3. Kết hợp title + silence 0.8s + summary và chuẩn hóa âm lượng -16.0 LUFS
        combined = seg_title + silence_08 + seg_summary
        combined = apply_voice_standard(combined)
        combined = combined.set_frame_rate(44100).set_channels(2)
        combined.export(str(target_audio), format="wav")

        dur = len(combined) / 1000.0
        total_duration_sec += dur
        print(f"       -> Xong ({dur:.1f}s, Title: {len(seg_title)/1000.0:.1f}s)")

        # Cập nhật đường dẫn tuyệt đối vào item
        item["audio_path"] = str(target_audio)
        item["audio_title"] = str(target_title)

    # Cập nhật lại thethao.json
    json_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 80)
    print(f"[HOÀN TẤT] 100% 25 file Audio và Audio-Title đã sinh thành công!")
    print(f"Tổng thời lượng giọng đọc: {total_duration_sec:.1f}s (~{total_duration_sec/60:.2f} phút)")


if __name__ == "__main__":
    main()
