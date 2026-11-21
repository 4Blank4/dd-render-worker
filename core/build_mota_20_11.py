# -*- coding: utf-8 -*-
"""
build_mota_20_11.py — Sinh mô tả YouTube chuẩn 2 phần `outputs/20.11.2026/mota.txt`
từ dữ liệu chapters thực tế và module xuất bản trung tâm `publisher.write_mota_16x9`.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import List, Tuple

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

from core.diemdoc import publisher

DAY_STR = "20.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
CHAPTERS_FILE = OUT_DIR / "_preview_v2" / "chapters_20_11.json"


def main() -> None:
    if not CHAPTERS_FILE.exists():
        raise FileNotFoundError(f"Chưa có file chapters: {CHAPTERS_FILE}")
    raw = json.loads(CHAPTERS_FILE.read_text(encoding="utf-8"))

    chapters: List[Tuple[str, str]] = [
        (c["time"], c["label"]) for c in raw.get("chapters", [])
    ]

    titles_abc = [
        "CAHN dội cột dọc ba lần thua Johor 1-3, Nuno Gomes thăm U17 Việt Nam",
        "U17 Úc thắng sốc Argentina 2-0, flycam lộ sơ đồ M.U & Messi dẫn đầu lương MLS",
        "Real Madrid gia hạn Tchouameni, U17 Việt Nam đấu Bỉ & ATP Finals Turin",
    ]

    intro_paragraphs = [
        (
            "Bản tin Điểm Đọc Thể Thao ngày 20/11/2026 tổng hợp nhanh 21 diễn biến nổi bật "
            "của bóng đá Việt Nam, khu vực Đông Nam Á và đấu trường thể thao quốc tế."
        )
    ]

    highlight_bullets = [
        "Công an Hà Nội 3 lần dứt điểm trúng khung gỗ và thua ngược Johor Darul Ta'zim 1-3 trên sân Hàng Đẫy.",
        "U17 Việt Nam nhận sự tiếp lửa bất ngờ từ danh thủ Nuno Gomes trước trận ra quân gặp U17 Bỉ lúc 20h tối nay.",
        "U17 Australia tạo địa chấn thắng U17 Argentina 2-0 với hai tài năng gốc Việt trong đội hình xuất phát.",
        "Flycam ghi hình lộ sơ đồ 3-2-5 của HLV Mauricio Pochettino tại Man Utd; Lionel Messi dẫn đầu bảng lương MLS với 28,33 triệu USD.",
        "Real Madrid gia hạn hợp đồng cùng Tchouameni và Courtois; cập nhật Đại hội Thể thao toàn quốc 2026 & ATP Finals tại Turin.",
    ]

    hashtags = [
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TinTheThao",
        "#BongDaVietNam",
        "#U17WorldCup",
        "#CAHN",
        "#ManUtd",
        "#LionelMessi",
        "#ATPFinals",
    ]

    out_path = publisher.write_mota_16x9(
        out_path=OUT_DIR / "mota.txt",
        titles_abc=titles_abc,
        chapters=chapters,
        video_type="daily_digest",
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        sources_line="📰 Nguồn tổng hợp & đối chiếu: VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí, Bóng Đá Plus, AFC, FIFA, ATP Tour.",
        hashtags=hashtags,
        day_str=DAY_STR,
    )
    print(f"[ok] Đã xuất {out_path} ({len(chapters)} chapters)")

    # Đồng bộ luôn file mô tả Short_Tin_Nhanh_21_Tin_mota.txt (nếu có) sang chuẩn 3 mạng xã hội mới
    short_mota = OUT_DIR / "shorts" / "Short_Tin_Nhanh_21_Tin_mota.txt"
    if short_mota.exists():
        old_lines = short_mota.read_text(encoding="utf-8").splitlines()
        sh_chapters: List[Tuple[str, str]] = []
        for ln in old_lines:
            ln_s = ln.strip()
            if len(ln_s) >= 6 and ln_s[:2].isdigit() and ln_s[2] == ":" and ln_s[3:5].isdigit():
                ts, lbl = ln_s.split(" ", 1)
                sh_chapters.append((ts, lbl.strip()))
        publisher.write_mota_9x16(
            out_path=short_mota,
            seo_title="Tin nhanh 20/11: CAHN thua JDT, U17 Việt Nam đấu Bỉ & Messi dẫn đầu lương MLS",
            description_paragraphs=[
                "Điểm nhanh 21 tin tức thể thao nóng nhất ngày 20/11/2026: CAHN thua ngược Johor Darul Ta'zim 1-3, U17 Việt Nam sẵn sàng đấu U17 Bỉ, U17 Australia thắng sốc Argentina 2-0, flycam lộ sơ đồ Man Utd của Pochettino và Messi dẫn đầu bảng lương MLS với 28,33 triệu USD."
            ],
            chapters=sh_chapters,
            sources_line="📰 Nguồn: VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí, Bóng Đá Plus, FIFA, AFC, ATP Tour.",
            hashtags=["#DiemDoc", "#DiemDocTheThao", "#TinTheThao", "#BongDaVietNam", "#U17WorldCup", "#ManUtd", "#LionelMessi"],
            tiktok_caption="Điểm nhanh 21 tin nóng thể thao 20/11: CAHN thua tiếc nuối JDT 1-3, Nuno Gomes tiếp lửa U17 Việt Nam đấu Bỉ, flycam lộ sơ đồ 3-2-5 của Man Utd và Messi dẫn đầu lương MLS!",
        )
        print(f"[ok] Đã nâng cấp chuẩn 3 MXH cho {short_mota}")


if __name__ == "__main__":
    main()
