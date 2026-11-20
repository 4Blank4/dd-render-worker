#!/usr/bin/env python3
"""
pron_test.py — Sinh tệp âm thanh kiểm thử từ điển phát âm thể thao cho người dùng đánh giá
========================================================================================
Chọn tối đa ~60 mục rủi ro cao (tên cầu thủ, HLV, CLB, thuật ngữ ngoại quốc),
sinh câu mẫu đọc đối chiếu 2 lần (nguyên bản và bản phiên âm), chia thành các tệp
nghe thử outputs/_samples/pron_test_XX.m4a kèm bảng đánh giá outputs/_samples/pron_test.md.
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import os
import json
import subprocess
from pathlib import Path
from pydub import AudioSegment

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core", "vendor"))
sys.path.insert(1, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.tts_text import load_pronunciation_dict

# 60 mục thể thao rủi ro cao nhất cần người dùng kiểm tra
RISKY_NAMES = [
    # Cầu thủ khó
    "Erling Haaland", "Kylian Mbappe", "Vinicius Junior", "Jude Bellingham",
    "Kevin De Bruyne", "Dominik Szoboszlai", "Martin Odegaard", "Alexis Mac Allister",
    "Darwin Nunez", "Cole Palmer", "Nicolas Jackson", "Alejandro Garnacho",
    "Rasmus Hojlund", "Kobbie Mainoo", "Son Heung-min", "Alexander Isak",
    "Robert Lewandowski", "Lamine Yamal", "Antoine Griezmann", "Harry Kane",
    "Jamal Musiala", "Florian Wirtz", "Khvicha Kvaratskhelia", "Lautaro Martinez",
    "William Saliba", "Gabriel Magalhaes",
    # Huấn luyện viên
    "Mikel Arteta", "Pep Guardiola", "Jurgen Klopp", "Arne Slot",
    "Erik ten Hag", "Enzo Maresca", "Ange Postecoglou", "Unai Emery",
    "Carlo Ancelotti", "Xabi Alonso", "Hansi Flick", "Simone Inzaghi", "Ruben Amorim",
    # Câu lạc bộ & Giải đấu
    "Manchester City", "Manchester United", "Newcastle", "Tottenham",
    "Bayer Leverkusen", "Borussia Dortmund", "Bayern Munich", "Atletico Madrid",
    "Sporting CP", "UEFA Champions League", "Conference League", "Bundesliga", "Copa America",
    # Thuật ngữ & Kỹ thuật
    "hat-trick", "clean sheet", "offside", "penalty", "playmaker", "derby", "El Clasico",
    "VAR", "BXH", "ĐT", "vs", "1/8"
]


def generate_pronunciation_tests(batch_size: int = 15, max_items: int = 60) -> None:
    dict_entries = load_pronunciation_dict()
    entry_map = {e["display"].lower(): e for e in dict_entries}

    selected = []
    for name in RISKY_NAMES:
        if name.lower() in entry_map:
            selected.append(entry_map[name.lower()])
        else:
            selected.append({"display": name, "say": name, "group": False})
        if len(selected) >= max_items:
            break

    print(f"Đã chọn {len(selected)} mục phát âm thể thao rủi ro cao để sinh mẫu nghe thử.")

    # Đọc cấu hình giọng
    cfg_voice = os.path.join(paths.CONFIG, "voice.json")
    voice_name = "Minh Quân Pro"
    speed = 1.20
    pitch = 0.85
    temperature = 0.5
    if os.path.exists(cfg_voice):
        try:
            with open(cfg_voice, "r", encoding="utf-8") as f:
                vcfg = json.load(f)
                voice_name = vcfg.get("voice", voice_name)
                speed = vcfg.get("speed", speed)
                pitch = vcfg.get("pitch", pitch)
                temperature = vcfg.get("temperature", temperature)
        except Exception:
            pass

    out_samples_dir = os.path.join(paths.OUTPUTS, "_samples")
    os.makedirs(out_samples_dir, exist_ok=True)
    temp_work_dir = paths.work_file("pron_test_tmp")
    os.makedirs(temp_work_dir, exist_ok=True)

    from vieneu import Vieneu
    print("Đang nạp mô hình ViTTS v3turbo...")
    model = Vieneu(mode="v3turbo")

    # Chia thành các batch ~15-20 mục
    batches = [selected[i:i + batch_size] for i in range(0, len(selected), batch_size)]
    md_rows = []

    global_idx = 1
    for b_idx, batch in enumerate(batches, 1):
        print(f"\n--- Đang xử lý Nhóm {b_idx:02d} ({len(batch)} mục) ---")
        batch_audio = AudioSegment.empty()
        m4a_filename = f"pron_test_{b_idx:02d}.m4a"
        m4a_path = os.path.join(out_samples_dir, m4a_filename)

        for item in batch:
            disp = item["display"]
            say = item["say"]
            # Tạo câu đọc đối chiếu:
            # "Mục số X. Bản gốc: disp. Phiên âm: say."
            phrase = f"Mục số {global_idx}. Tên gốc: {disp}. Đọc chuẩn: {say}."
            print(f"  [{global_idx:02d}] {phrase}")

            raw_wav = os.path.join(temp_work_dir, f"item_{global_idx:03d}_raw.wav")
            fx_wav = os.path.join(temp_work_dir, f"item_{global_idx:03d}_fx.wav")

            audio_data = model.infer(phrase, voice=voice_name, temperature=temperature)
            model.save(audio_data, raw_wav)

            # Rubberband pitch & tempo
            cmd = ["ffmpeg", "-y", "-i", raw_wav, "-filter:a", f"rubberband=pitch={pitch}:tempo={speed}", fx_wav]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            seg = AudioSegment.from_wav(fx_wav)
            batch_audio += seg
            batch_audio += AudioSegment.silent(duration=600)  # khoảng nghỉ 0.6s giữa các mục

            md_rows.append(f"| {global_idx:02d} | `{disp}` | **{say}** | `{m4a_filename}` | [ ] Đạt / [ ] Chưa đạt |")
            global_idx += 1

        # Xuất file m4a chất lượng cao
        batch_wav = os.path.join(temp_work_dir, f"batch_{b_idx:02d}.wav")
        batch_audio.export(batch_wav, format="wav")
        cmd_m4a = ["ffmpeg", "-y", "-i", batch_wav, "-c:a", "aac", "-b:a", "192k", m4a_path]
        subprocess.run(cmd_m4a, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"-> Đã xuất tệp nghe thử: {paths.rel_to_root(m4a_path)}")

    # Tạo bảng markdown
    md_content = f"""# BẢNG ĐÁNH GIÁ PHÁT ÂM THỂ THAO (PRONUNCIATION TEST REPORT)

*Kênh: Điểm Đọc Thể Thao | Giọng: {voice_name} (pitch {pitch}, tempo {speed})*  
*Người dùng nghe các file âm thanh trong `outputs/_samples/` và tích chọn ✓ hoặc ✗ để Agent điều chỉnh từ điển.*

| STT | Tên gốc (Display) | Phiên âm đọc (Say) | File âm thanh | Đánh giá của người dùng |
|:---:|:---|:---|:---|:---:|
""" + "\n".join(md_rows) + "\n"

    md_path = os.path.join(out_samples_dir, "pron_test.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"\n[XONG] Bảng đánh giá đã tạo tại: {paths.rel_to_root(md_path)}")


if __name__ == "__main__":
    generate_pronunciation_tests()
