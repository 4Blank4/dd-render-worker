# -*- coding: utf-8 -*-
"""
build_mota_24_11.py — Sinh mô tả YouTube chuẩn 2 phần `outputs/24.11.2026/mota.txt`
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

DAY_STR = "24.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
CHAPTERS_FILE = OUT_DIR / "_preview_v2" / "chapters_24_11.json"


def main() -> None:
    if not CHAPTERS_FILE.exists():
        raise FileNotFoundError(f"Chưa có file chapters: {CHAPTERS_FILE}")
    raw = json.loads(CHAPTERS_FILE.read_text(encoding="utf-8"))

    chapters: List[Tuple[str, str]] = [
        (c["time"], c["label"]) for c in raw.get("chapters", [])
    ]

    titles_abc = [
        "U17 Việt Nam hòa New Zealand 3-3, Thúy Hiền 5 kỷ lục & Brentford thắng 4-0",
        "Duy Khang gỡ hòa phút 90+2, Ánh Viên giành HCV & Jannik Sinner mổ đầu gối",
        "Tin thể thao 24/11: U17 Việt Nam giành điểm lịch sử, MU kháng cáo thẻ đỏ Yoro",
    ]

    intro_paragraphs = [
        (
            "Bản tin Điểm Đọc Thể Thao ngày 24/11/2026 tổng hợp toàn cảnh những diễn biến nóng nhất "
            "của thể thao Việt Nam và thế giới: U17 World Cup 2026, Đại hội Thể thao toàn quốc 2026, "
            "AFC Champions League Elite, Ngoại hạng Anh, Champions League, La Liga, Quần vợt ATP, Quyền Anh và Bóng bàn thế giới."
        )
    ]

    highlight_bullets = [
        "U17 Việt Nam tạo nên cuộc rượt đuổi cảm xúc hòa U17 New Zealand 3-3 với bàn gỡ phút 90+2 của Duy Khang, giành điểm số lịch sử tại World Cup 11 người, được FIFA ca ngợi và VFF thưởng nóng 400 triệu đồng trước trận gặp U17 Mali.",
        "Đường đua bơi Đại hội Thể thao toàn quốc 2026 bùng nổ kỷ lục: kình ngư 17 tuổi Nguyễn Thúy Hiền giành 5 HCV và phá 5 kỷ lục sau 2 ngày, Nguyễn Thị Ánh Viên đoạt HCV đầu tiên sau 1437 ngày giải nghệ, Phạm Thanh Bảo phá kỷ lục quốc gia 100m ếch nam.",
        "TP.HCM dẫn đầu bảng tổng sắp Đại hội với 54 HCV, hẹn Thái Nguyên ở chung kết bóng đá nữ; Lại Lý Huynh và Minh Nhật Quang thắng cờ tướng, Chu Việt Hoàng vô địch pool 9 bi, Lê Ngọc Sơn té xe vẫn giành HCV xe đạp; Nguyễn Xuân Son lọt Top 30 đề cử Quả bóng vàng châu Á.",
        "Tại Ngoại hạng Anh, Brentford đè bẹp Everton 4-0 với cú đúp của Keane Lewis-Potter và thẻ đỏ của James Tarkowski; Manchester United kháng cáo thẻ đỏ Leny Yoro giữa cơn thịnh nộ của Gary Neville.",
        "Bayern Munich mất Harry Kane 3 tháng và tranh cãi quanh Jamal Musiala; Diego Simeone lập kỷ lục 345 chiến thắng tại La Liga; FIFA chốt chủ nhà World Cup nữ 2031 và 2035; Jannik Sinner phẫu thuật đầu gối nguy cơ lỡ Australian Open 2027.",
    ]

    hashtags = [
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TinTheThao",
        "#U17VietNam",
        "#U17WorldCup2026",
        "#DaiHoiTheThaoToanQuoc2026",
        "#NguyenThuyHien",
        "#AnhVien",
        "#ManUtd",
        "#Brentford",
        "#JannikSinner",
    ]

    out_path = publisher.write_mota_16x9(
        out_path=OUT_DIR / "mota.txt",
        titles_abc=titles_abc,
        chapters=chapters,
        video_type="daily_digest",
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        sources_line="📰 Nguồn tổng hợp & đối chiếu: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian, FIFA.",
        hashtags=hashtags,
        day_str=DAY_STR,
    )
    print(f"[ok] Đã xuất {out_path} ({len(chapters)} chapters)")


if __name__ == "__main__":
    main()
