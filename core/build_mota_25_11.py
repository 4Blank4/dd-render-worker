# -*- coding: utf-8 -*-
"""
build_mota_25_11.py — Sinh mô tả YouTube chuẩn 2 phần `outputs/25.11.2026/mota.txt`
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

DAY_STR = "25.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
CHAPTERS_FILE = OUT_DIR / "_preview_v2" / "chapters_25_11.json"


def main() -> None:
    if not CHAPTERS_FILE.exists():
        raise FileNotFoundError(f"Chưa có file chapters: {CHAPTERS_FILE}")
    raw = json.loads(CHAPTERS_FILE.read_text(encoding="utf-8"))

    chapters: List[Tuple[str, str]] = [
        (c["time"], c["label"]) for c in raw.get("chapters", [])
    ]

    titles_abc = [
        "CAHN hạ sốc Vissel Kobe 3-1, Real Madrid thắng 5-1 & Ánh Viên lập kỷ lục",
        "CAHN thắng Vissel Kobe 3-1, Ronaldo nhại trọng tài & Senegal đòi lại cúp",
        "Real thắng 5-1, U17 Việt Nam tăng bậc & De Bruyne tái ngộ Man City",
    ]

    intro_paragraphs = [
        (
            "Bản tin Điểm Đọc Thể Thao ngày 25/11/2026 tổng hợp toàn cảnh những diễn biến nóng nhất "
            "của thể thao Việt Nam và thế giới: AFC Champions League Elite, U17 World Cup 2026, "
            "Đại hội Thể thao toàn quốc 2026, UEFA Champions League, Ngoại hạng Anh, Cúp châu Phi AFCON, "
            "Copa América 2028, Cờ tướng, Cricket và Cờ vua Thế giới."
        )
    ]

    highlight_bullets = [
        "Công an Hà Nội tạo địa chấn tại Hàng Đẫy khi quật ngã đội đầu bảng Vissel Kobe 3-1 nhờ các bàn thắng của Stefan Mauk và cú đúp của Brayan Perea, mở toang cánh cửa vào vòng 16 đội Cúp C1 châu Á; trong khi Buriram United tung 11 ngoại binh vẫn thua Shanghai Port 1-3.",
        "U17 Việt Nam tăng từ hạng 8 lên hạng 7 nhóm đội xếp thứ ba tại U17 World Cup 2026 nhờ Nhật Bản thua Serbia 0-1; tiền vệ Chu Ngọc Nguyễn Lực lọt Top 17 cầu thủ hay nhất theo Sofascore trước lượt cuối gặp U17 Mali.",
        "Tại Đại hội Thể thao toàn quốc 2026, Nguyễn Thị Ánh Viên lập cú đúp 2 HCV kèm kỷ lục 100m ngửa nữ sau 8 năm và kỷ lục quốc gia tiếp sức; Nguyễn Thúy Hiền nâng thành tích lên 6 HCV đưa Quân Đội vào Top 3; xạ thủ 37 tuổi Nguyễn Thùy Dung gây sốc thắng Trịnh Thu Vinh; Nguyễn Thùy Linh hẹn Vũ Thị Trang ở chung kết cầu lông.",
        "Trên sân cỏ châu Âu, Real Madrid ngược dòng thắng PSV 5-1 nhờ dấu ấn thay người của José Mourinho, siêu phẩm Jude Bellingham và cú đúp Kylian Mbappé; Man City hòa kịch tính Napoli 2-2 trong đêm tri ân De Bruyne; Arsenal hòa Dortmund 1-1.",
        "Tòa án Thể thao CAS chính thức tước chức vô địch AFCON 2025 của Morocco để trả lại cho Senegal; Ronaldo chạm mốc 987 bàn nhưng gây tranh cãi che mắt nhại trọng tài; FA hủy thẻ đỏ của Leny Yoro khiến HLV Pochettino vẫn phẫn nộ.",
    ]

    hashtags = [
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TinTheThao",
        "#CongAnHaNoi",
        "#U17VietNam",
        "#DaiHoiTheThaoToanQuoc2026",
        "#AnhVien",
        "#RealMadrid",
        "#ManCity",
        "#Senegal",
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
