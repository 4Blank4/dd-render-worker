# -*- coding: utf-8 -*-
"""
build_mota_21_11.py — Sinh mô tả YouTube chuẩn 2 phần `outputs/21.11.2026/mota.txt`
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

DAY_STR = "21.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
CHAPTERS_FILE = OUT_DIR / "_preview_v2" / "chapters_21_11.json"


def main() -> None:
    if not CHAPTERS_FILE.exists():
        raise FileNotFoundError(f"Chưa có file chapters: {CHAPTERS_FILE}")
    raw = json.loads(CHAPTERS_FILE.read_text(encoding="utf-8"))

    chapters: List[Tuple[str, str]] = [
        (c["time"], c["label"]) for c in raw.get("chapters", [])
    ]

    titles_abc = [
        "U17 Việt Nam thua Bỉ 2-3 với 2 siêu phẩm, Ronaldo hỏng 11m & Kane nghỉ hết năm",
        "Báo Bỉ thán phục U17 Việt Nam, CR7 ghi bàn 986 rồi thua & Mourinho rời họp báo",
        "Siêu phẩm của U17 Việt Nam, VFS gây tranh cãi, Quang Liêm nhận 800 triệu đồng",
    ]

    intro_paragraphs = [
        (
            "Bản tin Điểm Đọc Thể Thao ngày 21/11/2026 tổng hợp toàn cảnh những diễn biến nóng nhất "
            "của U17 World Cup, bóng đá Việt Nam, Đại hội Thể thao toàn quốc 2026 và đấu trường quốc tế."
        )
    ]

    highlight_bullets = [
        "U17 Việt Nam dù thua sát nút U17 Bỉ 2-3 ở trận ra quân World Cup tại Qatar nhưng tạo tiếng vang lớn nhờ hai siêu phẩm của Lê Sỹ Bách và Chu Ngọc Nguyễn Lực.",
        "Trọng tài toàn nữ Brazil điều hành trận Việt Nam - Bỉ lần đầu áp dụng hệ thống thẻ xanh VFS thay VAR gây nhiều tranh cãi; Thái Lan và Malaysia đồng loạt lỡ hẹn U17 châu Á 2027.",
        "Thanh Hóa phá dớp tám năm hạ HAGL 2-1 tại V-League; Lê Quang Liêm xếp hạng 8 giải cờ vua toàn năng thế giới kèm thưởng 800 triệu đồng; Phan Huy Hoàng gây sốt làng cờ tướng.",
        "Cristiano Ronaldo đạt mốc 986 bàn thắng nhưng sút hỏng phạt đền khiến Al Nassr thua Al Ahli 1-3; Jose Mourinho đột ngột rời phòng họp báo Real Madrid; Harry Kane chấn thương cổ chân nặng.",
        "Điểm nhanh các tin thể thao khác: Bốc thăm tứ kết UEFA Nations League, nguy cơ KFA bị FIFA đình chỉ, Man City phản đối EPL, Messi dự MLS Cup, bán kết ATP Finals và F1 Las Vegas GP.",
    ]

    hashtags = [
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TinTheThao",
        "#U17VietNam",
        "#U17WorldCup",
        "#VLeague",
        "#CristianoRonaldo",
        "#HarryKane",
        "#JoseMourinho",
    ]

    out_path = publisher.write_mota_16x9(
        out_path=OUT_DIR / "mota.txt",
        titles_abc=titles_abc,
        chapters=chapters,
        video_type="daily_digest",
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        sources_line="📰 Nguồn tổng hợp & đối chiếu: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, Bóng Đá Plus, FIFA, AFC, UEFA, ATP Tour.",
        hashtags=hashtags,
        day_str=DAY_STR,
    )
    print(f"[ok] Đã xuất {out_path} ({len(chapters)} chapters)")


if __name__ == "__main__":
    main()
