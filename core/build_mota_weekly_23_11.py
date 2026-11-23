#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_mota_weekly_23_11.py — Xuất Bản Mô Tả SEO Chuẩn YouTube cho Bản Tin Tuần Weekly-23.11.2026
====================================================================================================
Đọc chapters_Weekly_23_11.json từ _preview_v2/ và tạo outputs/Weekly-23.11.2026/mota.txt
qua module chuẩn core/diemdoc/publisher.py (video_type='weekly_digest').
"""

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
from pathlib import Path
from typing import List, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc.log import ok
from diemdoc.publisher import write_mota_16x9

ROOT = Path(_ROOT)
DAY_STR = "Weekly-23.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR


def main() -> None:
    chap_path = OUT_DIR / "_preview_v2" / "chapters_Weekly_23_11.json"
    data = json.loads(chap_path.read_text(encoding="utf-8"))
    chapters_raw = data.get("chapters", [])

    chapters: List[Tuple[str, str]] = []
    for i, ch in enumerate(chapters_raw):
        t = str(ch["time"]).strip()
        lbl = str(ch["label"]).strip()
        if i == 0:
            lbl = "Nhập cuộc & Tâm điểm thể thao tuần qua (18–23/11)"
        chapters.append((t, lbl))

    titles_abc = [
        "Tổng hợp thể thao tuần: Liverpool 4-0 Man Utd, U17 Việt Nam & Đại hội Toàn quốc",
        "U17 Việt Nam ghi 2 siêu phẩm, Đại hội mưa kỷ lục & Man Utd thảm bại Liverpool",
        "Ánh Viên giành HCB, Pochettino ra mắt ác mộng, Alcaraz & Márquez lập kỳ tích",
    ]

    intro_paragraphs = [
        "Bản tin Điểm Đọc Tổng Hợp Tuần tới ngày 23/11/2026 điểm lại toàn cảnh 21 sự kiện thể thao Việt Nam và quốc tế nổi bật nhất tuần qua (18–23/11).",
        "Theo dõi trọn vẹn từng diễn biến từ bóng đá Việt Nam, U17 World Cup 2026, V-League, Đại hội Thể thao toàn quốc lần thứ X tới Ngoại hạng Anh, La Liga, ATP Finals, F1 Las Vegas và MotoGP.",
    ]

    highlight_bullets = [
        "Tuyển Việt Nam tụt hạng 99 FIFA kèm chấn thương nghỉ hết năm của Đình Bắc nhưng giữ hạt giống số 2 World Cup 2030.",
        "U17 Việt Nam ghi hai siêu phẩm vào lưới U17 Bỉ trước giờ quyết đấu U17 New Zealand (22h30 ngày 23/11); Công an TP.HCM hạ ĐKVĐ Buriram 1-0 tại Shopee Cup.",
        "Đại hội Thể thao toàn quốc 2026 khai mạc bên sông Sài Gòn: TP.HCM bứt phá 109 huy chương, Ánh Viên giành HCB tái xuất và Watson Nguyễn phá kỷ lục quốc gia bơi lội.",
        "Ngoại hạng Anh đại địa chấn: Liverpool thắng Man Utd 4-0 (Pochettino lập kỷ lục ra mắt tệ nhất 100 năm), Chelsea thua Leeds 1-4; Barcelona thắng ngược Villarreal 3-2 giữ đỉnh La Liga.",
        "Carlos Alcaraz vô địch ATP Finals 2026, Max Verstappen thắng F1 Las Vegas hỗn loạn 35 lần đổi ngôi đầu và Marc Márquez san bằng kỷ lục 8 lần vô địch MotoGP.",
    ]

    sources_line = "Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian, ESPN, Formula 1, ATP Tour, FIFA, AFC"

    hashtags = [
        "#DiemDoc",
        "#TinTheThaoTuan",
        "#TongHopTheThao",
        "#BongDaVietNam",
        "#U17WorldCup",
        "#DaiHoiTheThaoToanQuoc2026",
        "#NgoaiHangAnh",
        "#VLeague",
        "#Alcaraz",
        "#MarcMarquez",
    ]

    out_p = write_mota_16x9(
        out_path=OUT_DIR / "mota.txt",
        titles_abc=titles_abc,
        chapters=chapters,
        video_type="weekly_digest",
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        sources_line=sources_line,
        hashtags=hashtags,
        day_str=DAY_STR,
    )
    ok(f"Đã xuất bản SEO 2 phần chuẩn Điểm Đọc Tuần: {out_p}")


if __name__ == "__main__":
    main()
