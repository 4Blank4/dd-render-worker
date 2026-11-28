# -*- coding: utf-8 -*-
"""
build_mota_28_11.py — Sinh mô tả YouTube chuẩn 2 phần `outputs/28.11.2026/mota.txt`
từ dữ liệu chapters thực tế và module xuất bản trung tâm `publisher.write_mota_16x9`.
Đồng nhất 3 Option tiêu đề với 3 kiểu thumbnail (Option A: 1 ảnh, Option B: 3 ảnh, Option C: 2 ảnh).
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

DAY_STR = "28.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
CHAPTERS_FILE = OUT_DIR / "_preview_v2" / "chapters_28_11.json"


def main() -> None:
    if not CHAPTERS_FILE.exists():
        raise FileNotFoundError(f"Chưa có file chapters: {CHAPTERS_FILE}")
    raw = json.loads(CHAPTERS_FILE.read_text(encoding="utf-8"))

    chapters: List[Tuple[str, str]] = [
        (c["time"], c["label"]) for c in raw.get("chapters", [])
    ]

    # Đồng nhất 100% với bộ 3 Thumbnail A/B/C (Option C đúng 2 tin khớp 2 ảnh)
    titles_abc = [
        "Nottingham Forest hạ Chelsea 3-2, Xabi Alonso lún sâu vào khủng hoảng",
        "Chelsea thua trận thứ 3, Marc Márquez giải nghệ & Nam Định hòa CAHN",
        "Nam Định hòa CAHN 0-0 & Nottingham Forest hạ gục Chelsea 3-2",
    ]

    intro_paragraphs = [
        (
            "Bản tin Điểm Đọc Thể Thao ngày 28/11/2026 tổng hợp toàn cảnh những diễn biến nóng nhất "
            "của thể thao Việt Nam và thế giới: V-League 2026-2027, Đội tuyển Việt Nam, U17 World Cup 2026, "
            "Đại hội Thể thao toàn quốc 2026, Ngoại hạng Anh, Bundesliga, MotoGP, Formula 1 Qatar GP, "
            "Quyền anh hạng nặng, Davis Cup 2026, Giải hạng Nhất Quốc gia, NFL và NBA."
        )
    ]

    highlight_bullets = [
        "Tâm điểm vòng 9 V-League: Thép Xanh Nam Định hòa 0-0 CLB Công an Hà Nội tại Thiên Trường để duy trì cách biệt năm điểm; HLV Alexandre Polking bác bỏ tin đồn Quang Hải chia tay tuyển Việt Nam; Sông Lam Nghệ An hạ Ninh Bình 1-0 nối dài mạch chín trận bất bại.",
        "U17 World Cup 2026 xác định đủ 32 đội vào vòng 1/16, Nhật Bản thắng đậm Honduras 7-0 và chạm trán Hàn Quốc; truyền thông khu vực ghi nhận màn trình diễn sòng phẳng của U17 Việt Nam cùng dấu ấn hai bàn thắng từ Chu Ngọc Nguyễn Lực.",
        "Đại hội Thể thao toàn quốc 2026: Nguyễn Thị Ánh Viên khép lại môn bơi với bảy HCV, Võ Thị Mỹ Tiên thống trị với chín HCV cá nhân; điền kinh phá kỷ lục 100m rào nhưng Ngần Ngọc Nghĩa bị thẻ đỏ loại sốc; Châu Tuyết Vân giành HCV thứ năm liên tiếp giúp TP.HCM chạm mốc 96 HCV.",
        "Ngoại hạng Anh: Nottingham Forest đánh bại Chelsea 3-2 đẩy thầy trò Xabi Alonso vào chuỗi ba thất bại liên tiếp, Wesley Fofana bị cổ động viên nhà la ó; Man Utd gia hạn Bruno Fernandes tới năm 2028; nhiều CLB Ngoại hạng Anh đề xuất buộc chủ sở hữu Man City bán đội bóng.",
        "Chấn động MotoGP: Nhà vô địch tám lần thế giới Marc Márquez bất ngờ tuyên bố giải nghệ ở tuổi 33; F1 Qatar GP chứng kiến Kimi Antonelli và Mercedes thống trị ngày tập đầu; Tyson Fury được cấp phép đấu Anthony Joshua; Italy vào chung kết Davis Cup lần thứ tư liên tiếp.",
    ]

    hashtags = [
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TinTheThao",
        "#VLeague",
        "#NamDinh",
        "#CAHN",
        "#DaiHoiTheThaoToanQuoc2026",
        "#Chelsea",
        "#NottinghamForest",
        "#ManUtd",
        "#MarcMarquez",
    ]

    out_path = publisher.write_mota_16x9(
        out_path=OUT_DIR / "mota.txt",
        titles_abc=titles_abc,
        video_type="daily_digest",
        day_str=DAY_STR,
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        chapters=chapters,
        sources_line="📰 Nguồn tổng hợp & đối chiếu: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian, ESPN.",
        hashtags=hashtags,
    )
    print(f"[ok] Đã xuất mô tả SEO chuẩn 2 phần: {out_path}")


if __name__ == "__main__":
    main()
