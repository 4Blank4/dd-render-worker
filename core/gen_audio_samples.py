#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_audio_samples.py — Sinh 8 mẫu giọng đọc đối chiếu cho dự án '10 kỷ lục bóng đá'

Mục đích:
  Cung cấp 8 phiên bản đọc thử cùng một đoạn văn bản mở đầu (Intro)
  để người dùng và Claude đối chiếu, lựa chọn chất giọng và nhịp điệu tối ưu nhất
  thay cho cấu hình mặc định nếu cần.
"""

import sys
sys.dont_write_bytecode = True

import os
import shutil
import subprocess
from pathlib import Path

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent
sys.path.insert(0, str(ROOT / "core" / "vendor"))
sys.path.insert(1, str(ROOT / "core"))

from vieneu import Vieneu
from diemdoc.tts_text import prepare

TEST_TEXT = (
    "Bóng đá đã tồn tại hơn 160 năm. Hàng triệu trận đấu, hàng triệu cầu thủ, "
    "hàng triệu khoảnh khắc lịch sử. Nhưng trong tất cả những con số đó, "
    "có một nhóm rất nhỏ — những kỷ lục mà ngay cả những thiên tài vĩ đại nhất "
    "thời đại cũng không thể vươn tới. Hôm nay, Điểm Đọc sẽ điểm qua 10 kỷ lục "
    "bóng đá gần như bất tử — những cột mốc mà để phá vỡ chúng, bạn không chỉ cần "
    "thiên tài... bạn còn cần thời gian, may mắn, và có lẽ cả một điều kỳ diệu."
)

SAMPLES = [
    {
        "id": "01",
        "voice": "Minh Quân Pro",
        "speed": 1.15,
        "pitch": 0.85,
        "desc": "Cấu hình chuẩn Điểm Đọc hiện tại (nhịp 1.15, hạ tone nam trầm 0.85)"
    },
    {
        "id": "02",
        "voice": "Minh Quân Pro",
        "speed": 1.10,
        "pitch": 0.90,
        "desc": "Minh Quân Pro nhịp chậm hơn (1.10), tone tự nhiên đĩnh đạc (0.90)"
    },
    {
        "id": "03",
        "voice": "Minh Quân Pro",
        "speed": 1.20,
        "pitch": 0.80,
        "desc": "Minh Quân Pro nhịp nhanh kịch tính (1.20), tone nam trầm điện ảnh (0.80)"
    },
    {
        "id": "04",
        "voice": "Anh Khôi",
        "speed": 1.15,
        "pitch": 0.90,
        "desc": "Giọng nam Anh Khôi: Năng động, thanh thoát, phong cách thể thao hiện đại"
    },
    {
        "id": "05",
        "voice": "Thái Sơn",
        "speed": 1.15,
        "pitch": 0.90,
        "desc": "Giọng nam Thái Sơn: Trẻ trung, dứt khoát, hào sảng và cuốn hút"
    },
    {
        "id": "06",
        "voice": "Quang Sơn",
        "speed": 1.15,
        "pitch": 0.85,
        "desc": "Giọng nam Quang Sơn: Trầm ấm, vang, phong thái phóng viên tài liệu"
    },
    {
        "id": "07",
        "voice": "Minh Đức",
        "speed": 1.15,
        "pitch": 0.85,
        "desc": "Giọng nam Minh Đức: Trưởng thành, chuyên nghiệp, chuẩn mực truyền hình"
    },
    {
        "id": "08",
        "voice": "Thanh Bình",
        "speed": 1.15,
        "pitch": 0.90,
        "desc": "Giọng nam Thanh Bình: Rõ ràng, ngữ điệu bình luận viên thể thao trực tiếp"
    },
]

OUT_DIR = ROOT / "outputs" / "10_ky_luc_bong_da" / "audio_samples"
PROJ_DIR = ROOT / "projects" / "10_ky_luc_bong_da" / "audio_samples"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PROJ_DIR.mkdir(parents=True, exist_ok=True)


def run():
    print("=" * 66)
    print("  PHASE 1B — SINH 8 MẪU GIỌNG ĐỌC CHO 10 KỶ LỤC BÓNG ĐÁ")
    print("=" * 66)

    print("Đang tải mô hình ViNeu-TTS v3turbo...")
    model = Vieneu(mode="v3turbo")
    clean_text, tokens = prepare(TEST_TEXT)
    print(f"Văn bản thử nghiệm ({len(clean_text.split())} từ):\n\"{clean_text}\"\n")

    summary_rows = []

    for s in SAMPLES:
        sid = s["id"]
        vname = s["voice"]
        speed = s["speed"]
        pitch = s["pitch"]
        slug = vname.replace(" ", "_")

        raw_tmp = OUT_DIR / f"tmp_raw_{sid}.wav"
        out_wav = OUT_DIR / f"sample_{sid}_{slug}_spd{speed}_pch{pitch}.wav"
        out_m4a = OUT_DIR / f"sample_{sid}_{slug}_spd{speed}_pch{pitch}.m4a"

        print(f"[{sid}/08] Đang sinh giọng: {vname} (speed={speed}, pitch={pitch})...")
        audio_data = model.infer(clean_text, voice=vname, temperature=0.5)
        model.save(audio_data, str(raw_tmp))

        # Áp dụng bộ lọc âm thanh pitch & speed qua FFmpeg
        if abs(pitch - 1.0) > 0.01:
            filter_str = f"rubberband=pitch={pitch}:tempo={speed}"
        else:
            filter_str = f"atempo={speed}"

        # Xuất file WAV 44.1kHz chuẩn master
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_tmp),
            "-filter:a", filter_str,
            "-ar", "44100", "-ac", "2",
            str(out_wav)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Xuất thêm file M4A (AAC 192k) nghe thử siêu nhẹ
        subprocess.run([
            "ffmpeg", "-y", "-i", str(out_wav),
            "-c:a", "aac", "-b:a", "192k",
            str(out_m4a)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if raw_tmp.exists():
            raw_tmp.unlink()

        # Sao chép sang projects/
        shutil.copyfile(out_wav, PROJ_DIR / out_wav.name)
        shutil.copyfile(out_m4a, PROJ_DIR / out_m4a.name)

        wav_size_kb = out_wav.stat().st_size // 1024
        m4a_size_kb = out_m4a.stat().st_size // 1024
        print(f"  -> [OK] {out_wav.name} ({wav_size_kb} KB, m4a: {m4a_size_kb} KB)")

        summary_rows.append({
            "id": sid,
            "voice": vname,
            "speed": speed,
            "pitch": pitch,
            "wav_file": out_wav.name,
            "m4a_file": out_m4a.name,
            "desc": s["desc"]
        })

    # Tạo bảng mô tả Markdown
    md_content = [
        "# 🎧 Bảng Đánh Giá & Lựa Chọn Giọng Đọc (8 Mẫu Thử Nghiệm)\n",
        f"**Dự án:** `10_ky_luc_bong_da`\n",
        f"**Văn bản thử:** {clean_text}\n\n",
        "| Mẫu | Tên Giọng | Tốc độ | Cao độ (Pitch) | Đặc trưng & Phong cách | Tệp âm thanh nghe thử |",
        "|:---:|---|:---:|:---:|---|---|"
    ]

    for r in summary_rows:
        md_content.append(
            f"| **{r['id']}** | **{r['voice']}** | {r['speed']} | {r['pitch']} | {r['desc']} | `{r['m4a_file']}` |"
        )

    md_content.append("\n---\n")
    md_content.append("> **Hướng dẫn:** Người dùng và Claude có thể nghe trực tiếp các tệp `.m4a` / `.wav` trong thư mục `outputs/10_ky_luc_bong_da/audio_samples/` để chọn ra mẫu chất lượng nhất trước khi render chính thức.\n")

    md_path = OUT_DIR / "samples_review.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
    shutil.copyfile(md_path, PROJ_DIR / "samples_review.md")

    print("\n" + "=" * 66)
    print("  [HOÀN THÀNH PHASE 1B] Đã sinh thành công 8 mẫu audio.")
    print(f"  Thư mục: {OUT_DIR}")
    print("=" * 66)


if __name__ == "__main__":
    run()
