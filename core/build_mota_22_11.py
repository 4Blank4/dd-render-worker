# -*- coding: utf-8 -*-
"""
build_mota_22_11.py — Sinh mô tả YouTube chuẩn 2 phần `outputs/22.11.2026/mota.txt`
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

DAY_STR = "22.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
CHAPTERS_FILE = OUT_DIR / "_preview_v2" / "chapters_22_11.json"


def main() -> None:
    if not CHAPTERS_FILE.exists():
        raise FileNotFoundError(f"Chưa có file chapters: {CHAPTERS_FILE}")
    raw = json.loads(CHAPTERS_FILE.read_text(encoding="utf-8"))

    chapters: List[Tuple[str, str]] = [
        (c["time"], c["label"]) for c in raw.get("chapters", [])
    ]

    titles_abc = [
        "Man City mất điểm, Chelsea thảm bại, đại hội toàn quốc khai mạc",
        "VAR hủy bàn Haaland, Real ngược dòng, Messi thua đậm 0-3",
        "Tin thể thao 22/11: Arsenal chia điểm, UFC Qatar địa chấn, F1 rực lửa",
    ]

    intro_paragraphs = [
        (
            "Bản tin Điểm Đọc Thể Thao ngày 22/11/2026 tổng hợp toàn cảnh những diễn biến nóng nhất "
            "của thể thao Việt Nam và thế giới: Đại hội Thể thao toàn quốc 2026, V-League, Ngoại hạng Anh, "
            "La Liga, Ligue 1, MLS Cup, ATP Finals, F1 Las Vegas, UFC Qatar, NBA và MotoGP."
        )
    ]

    highlight_bullets = [
        "Đại hội Thể thao toàn quốc 2026 chính thức khai mạc rực rỡ bên sông Sài Gòn; kình ngư đội tuyển Mỹ Watson Nguyễn chuẩn bị so tài Phạm Thanh Bảo và Esports lần đầu tranh huy chương.",
        "Vòng 8 V-League chứng kiến Nam Định thắng Hải Phòng 2-1 giữ ngôi đầu, Hà Nội FC ngược dòng hạ Đồng Nai 3-1; U17 Việt Nam soi điểm yếu New Zealand trước trận quyết đấu tối 23/11.",
        "Ngoại hạng Anh dậy sóng: VAR hủy bàn thắng của Haaland khiến Man City hòa Fulham 1-1, Chelsea thảm bại 1-4 trước Leeds ngay tại Stamford Bridge, Arsenal hòa Newcastle 2-2 và lo chấn thương David Raya.",
        "Real Madrid thắng ngược Celta Vigo 2-1 dù Kylian Mbappé sút hỏng phạt đền; PSG thắng Nice 3-2 nhưng mất Désiré Doué; Roma và RB Leipzig cùng thắng 5-1 còn Hearts đè bẹp Dundee 8-0.",
        "Lionel Messi đoạt Vua phá lưới MLS nhưng Inter Miami thua Columbus Crew 0-3; Carlos Alcaraz đấu Alexander Zverev ở chung kết ATP Finals; địa chấn tại UFC Qatar, F1 Las Vegas GP, NBA và MotoGP Portimão.",
    ]

    hashtags = [
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TinTheThao",
        "#DaiHoiTheThaoToanQuoc2026",
        "#VLeague",
        "#NgoaiHangAnh",
        "#ManCity",
        "#Chelsea",
        "#RealMadrid",
        "#LionelMessi",
        "#UFC",
        "#F1",
    ]

    out_path = publisher.write_mota_16x9(
        out_path=OUT_DIR / "mota.txt",
        titles_abc=titles_abc,
        chapters=chapters,
        video_type="daily_digest",
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        sources_line="📰 Nguồn tổng hợp & đối chiếu: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, ESPN, Sky Sports, The Guardian, ATP Tour, Formula 1, UFC, MotoGP.",
        hashtags=hashtags,
        day_str=DAY_STR,
    )
    print(f"[ok] Đã xuất {out_path} ({len(chapters)} chapters)")


if __name__ == "__main__":
    main()
