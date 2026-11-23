# -*- coding: utf-8 -*-
"""
build_mota_23_11.py — Sinh mô tả YouTube chuẩn 2 phần `outputs/23.11.2026/mota.txt`
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

DAY_STR = "23.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
CHAPTERS_FILE = OUT_DIR / "_preview_v2" / "chapters_23_11.json"


def main() -> None:
    if not CHAPTERS_FILE.exists():
        raise FileNotFoundError(f"Chưa có file chapters: {CHAPTERS_FILE}")
    raw = json.loads(CHAPTERS_FILE.read_text(encoding="utf-8"))

    chapters: List[Tuple[str, str]] = [
        (c["time"], c["label"]) for c in raw.get("chapters", [])
    ]

    titles_abc = [
        "Liverpool đè bẹp Man Utd 4-0, Barca ngược dòng & mưa kỷ lục bơi lội",
        "Ác mộng Pochettino tại Anfield, Alcaraz vô địch ATP Finals & Márquez lập kỷ lục",
        "Tin thể thao 23/11: Ánh Viên tái xuất, Hoàng Đức tỏa sáng, Verstappen thắng F1",
    ]

    intro_paragraphs = [
        (
            "Bản tin Điểm Đọc Thể Thao ngày 23/11/2026 tổng hợp toàn cảnh những diễn biến nóng nhất "
            "của thể thao Việt Nam và thế giới: Đại hội Thể thao toàn quốc 2026, V-League, U17 World Cup, "
            "Ngoại hạng Anh, La Liga, Serie A, ATP Finals, F1 Las Vegas, MotoGP Bồ Đào Nha, Golf LPGA và MLB."
        )
    ]

    highlight_bullets = [
        "Môn bơi Đại hội Thể thao toàn quốc 2026 bùng nổ kỷ lục: Võ Thị Mỹ Tiên phá kỷ lục Đại hội đánh bại Nguyễn Thị Ánh Viên ở cự ly 200m hỗn hợp; Watson Nguyễn thắng Phạm Thanh Bảo phá kỷ lục quốc gia 50m ếch; TP.HCM vượt mốc 109 huy chương dẫn đầu toàn đoàn.",
        "Vòng 8 V-League chứng kiến Nguyễn Hoàng Đức ghi bàn giúp Ninh Bình thắng Đà Nẵng 1-0 vươn lên nhì bảng, Hà Tĩnh thắng Công an TP.HCM 2-1 trong trận đấu trung vệ Nguyễn Nhật Minh phải rời sân bằng xe cấp cứu; U17 Việt Nam sẵn sàng đấu U17 New Zealand lúc 22h30 tối nay.",
        "Tại Ngoại hạng Anh, Liverpool hủy diệt Manchester United 4-0 khiến HLV Mauricio Pochettino cân bằng kỷ lục ra mắt tệ nhất sau 100 năm và đẩy Quỷ đỏ xuống hạng 19; Hull City gây sốc thắng Brighton 2-0 bằng hai bàn thắng phút bù giờ.",
        "Ở La Liga và Serie A, Barcelona thắng ngược Villarreal 3-2 dù Lamine Yamal sút hỏng phạt đền; Atalanta hòa điên rồ Inter Milan 4-4 với hat-trick của Esposito; AC Milan thắng Frosinone 5-1, Juventus hạ Venezia 4-0 và PSG mất Désiré Doué hết mùa vì đứt ACL.",
        "Carlos Alcaraz đánh bại Alexander Zverev lần đầu vô địch ATP Finals; Max Verstappen thắng chặng F1 Las Vegas đầy hỗn loạn; Marc Márquez san bằng kỷ lục tám lần vô địch MotoGP của Agostini; Jeeno Thitikul và Tarik Skubal thiết lập hai kỷ lục tiền thưởng lịch sử.",
    ]

    hashtags = [
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TinTheThao",
        "#DaiHoiTheThaoToanQuoc2026",
        "#AnhVien",
        "#VLeague",
        "#U17VietNam",
        "#Liverpool",
        "#ManUtd",
        "#Barcelona",
        "#CarlosAlcaraz",
        "#MotoGP",
    ]

    out_path = publisher.write_mota_16x9(
        out_path=OUT_DIR / "mota.txt",
        titles_abc=titles_abc,
        chapters=chapters,
        video_type="daily_digest",
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        sources_line="📰 Nguồn tổng hợp & đối chiếu: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, ESPN, Sky Sports, The Guardian, ATP Tour, Formula 1, LPGA, MotoGP.",
        hashtags=hashtags,
        day_str=DAY_STR,
    )
    print(f"[ok] Đã xuất {out_path} ({len(chapters)} chapters)")


if __name__ == "__main__":
    main()
