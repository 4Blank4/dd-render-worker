# -*- coding: utf-8 -*-
"""
build_mota_26_11.py — Sinh mô tả YouTube chuẩn 2 phần `outputs/26.11.2026/mota.txt`
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

DAY_STR = "26.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
CHAPTERS_FILE = OUT_DIR / "_preview_v2" / "chapters_26_11.json"


def main() -> None:
    if not CHAPTERS_FILE.exists():
        raise FileNotFoundError(f"Chưa có file chapters: {CHAPTERS_FILE}")
    raw = json.loads(CHAPTERS_FILE.read_text(encoding="utf-8"))

    chapters: List[Tuple[str, str]] = [
        (c["time"], c["label"]) for c in raw.get("chapters", [])
    ]

    titles_abc = [
        "Man Utd hòa hỗn loạn Sporting, Bayern thua sốc Lille & U17 Việt Nam quyết đấu",
        "Man Utd rơi hạng 19, U17 Việt Nam quyết đấu Mali & Thùy Linh lập hat-trick",
        "Man Utd hòa 2-2 đầy tranh cãi, Bayern thua sốc & Ronaldo nguy cơ bị treo giò",
    ]

    intro_paragraphs = [
        (
            "Bản tin Điểm Đọc Thể Thao ngày 26/11/2026 tổng hợp toàn cảnh những diễn biến nóng nhất "
            "của thể thao Việt Nam và thế giới: U17 World Cup 2026, AFC Champions League Elite, "
            "AFC Champions League Two, Đại hội Thể thao toàn quốc 2026, UEFA Champions League, "
            "Ngoại hạng Anh, Cờ tướng Trung Quốc, NFL, Formula 1, Quyền Anh hạng nặng và Cờ vua Thế giới."
        )
    ]

    highlight_bullets = [
        "U17 Việt Nam chuẩn bị bước vào lượt trận quyết định bảng G U17 World Cup 2026 gặp U17 Mali lúc 20h tối 26/11 với nhiệm vụ giành trọn 3 điểm để tự quyết vé vào vòng 32 đội; tiền đạo trẻ Lê Sỹ Bách được FIFA đề cử Bàn thắng đẹp nhất giải.",
        "Thể Công Viettel hòa Melbourne Victory 0-0 và sớm dừng bước ở Cúp C2 châu Á với chuỗi 12 trận không thắng; trong khi Buriram United sa thải HLV Raul Caneda chỉ sau 25 ngày (thay 3 HLV trong 81 ngày), còn Công an Hà Nội bỏ xa cả 3 CLB Thái Lan.",
        "Tại Đại hội Thể thao toàn quốc 2026, Nguyễn Thùy Linh thắng Vũ Thị Trang 2-0 lập hat-trick HCV cầu lông, Võ Thị Mỹ Tiên chạm mốc 6 HCV cá nhân môn bơi, Ánh Viên đạt 5 HCV kèm kỷ lục quốc gia tiếp sức, Phạm Quang Huy thắng shoot-off bắn súng, còn TP.HCM vững ngôi đầu với 74 HCV.",
        "Tại Champions League, Man Utd hòa hỗn loạn Sporting CP 2-2 trong đêm trọng tài Szymon Marciniak bị chỉ trích dữ dội và thủ môn Senne Lammens mắc sai lầm, khiến Quỷ đỏ rơi hạng 19 và bị Opta cảnh báo 27,48% nguy cơ xuống hạng.",
        "Bayern Munich nhận thất bại đầu tiên mùa giải khi thua Lille 1-2 của HLV Davide Ancelotti; Liverpool thắng Club Brugge 3-0 nhờ cú đúp Isak và bàn thắng của Wirtz; Barcelona hạ Sabah 4-1 sau chuyến bay kỷ lục 3970 km; PSG hòa AS Roma 2-2.",
        "Thể thao quốc tế: Ronaldo nguy cơ bị treo giò 4 trận vì chế nhạo trọng tài; IFR sẵn sàng ép đổi chủ Man City; Saudi Arabia rao bán 25% cổ phần Newcastle; Raheem Sterling lĩnh 12 tháng tù treo; Steelers sa thải Aaron Rodgers; Williams F1 bị phạt vượt trần ngân sách; chốt đại chiến Daniel Dubois vs Joseph Parker.",
    ]

    hashtags = [
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TinTheThao",
        "#ManUtd",
        "#ChampionsLeague",
        "#U17VietNam",
        "#DaiHoiTheThaoToanQuoc2026",
        "#ThuyLinh",
        "#BayernMunich",
        "#Liverpool",
        "#Ronaldo",
    ]

    out_path = publisher.write_mota_16x9(
        out_path=OUT_DIR / "mota.txt",
        titles_abc=titles_abc,
        chapters=chapters,
        video_type="daily_digest",
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        sources_line="📰 Nguồn tổng hợp & đối chiếu: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian.",
        hashtags=hashtags,
        day_str=DAY_STR,
    )
    print(f"[ok] Đã xuất {out_path} ({len(chapters)} chapters)")


if __name__ == "__main__":
    main()
