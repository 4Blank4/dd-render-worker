#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_mota_19_11.py — Xuất file mô tả SEO YouTube chuẩn 2 phần Sentence Case
từ chapters_19_11.json cho Bản tin thể thao ngày 19.11.2026.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
import re
from pathlib import Path
from typing import List, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc.log import die, ok
from diemdoc.publisher import write_mota_16x9

DAY_STR = "19.11.2026"
ROOT = Path(_ROOT)
DAY_DIR = ROOT / "outputs" / DAY_STR


def main() -> None:
    chap_path = DAY_DIR / "_preview_v2" / "chapters_19_11.json"
    if not chap_path.exists():
        die(f"Thiếu {chap_path} — hãy chạy build_daily_19_11_video.py trước.")

    data = json.loads(chap_path.read_text(encoding="utf-8"))
    chapters: List[Tuple[str, str]] = [
        (str(c["time"]), re.sub(r"^\[\d+\]\s*", "", str(c["label"]))) for c in data.get("chapters", [])
    ]

    titles_abc = [
        "Đình Bắc nghỉ hết năm, Công an TP.HCM hạ Buriram, Messi dọa kiện AFA | Điểm Đọc 19.11",
        "U17 World Cup khai mạc hôm nay, Pochettino ra mắt MU, Haaland sắp cán mốc 400 | Điểm Đọc",
        "Ronaldo mất đề cử lớn, UEFA thách thức Infantino, Quang Liêm tranh hạng 7 | Điểm Đọc",
    ]

    intro_paragraphs = [
        (
            "Chào mừng quý vị và các bạn đến với Điểm Đọc — Bản tin tổng hợp thể thao ngày 19/11/2026, "
            "cập nhật toàn cảnh những diễn biến nóng nhất trong nước và quốc tế. Ở tâm điểm trong nước, "
            "tiền đạo Nguyễn Đình Bắc dính đa chấn thương đầu gối phải nghỉ hết năm 2026, nhưng câu lạc bộ Công an TP.HCM "
            "vừa tạo địa chấn hạ đương kim vô địch Buriram United 1-0 tại Shopee Cup, còn U17 Việt Nam đã sẵn sàng cho "
            "FIFA U17 World Cup 2026 khai mạc hôm nay tại Qatar."
        ),
        (
            "Trên đấu trường quốc tế, Lionel Messi cắt đứt liên hệ và dọa kiện Liên đoàn bóng đá Argentina, "
            "Cristiano Ronaldo vắng mặt ở hạng mục lớn nhất của Globe Soccer Awards 2026, HLV Mauricio Pochettino "
            "chính thức đặt chân tới Carrington làm việc tại Manchester United, còn UEFA chọn Philippe Diallo đối đầu Gianni Infantino. "
            "Cùng bước tiến tranh hạng 7 của Lê Quang Liêm, màn hủy diệt của Carlos Alcaraz tại ATP Finals 2026 và "
            "câu chuyện xúc động của nữ võ sĩ Vovinam Kim Lụa tại Đại hội Thể thao toàn quốc."
        ),
    ]

    highlight_bullets = [
        (
            "Tâm điểm bóng đá Việt Nam: Nguyễn Đình Bắc rách bán phần dây chằng bên ngoài, nghỉ thi đấu hết năm 2026; "
            "tuyển Việt Nam chốt hạng 99 FIFA giữ lợi thế hạt giống số 2 vòng loại World Cup 2030; "
            "Công an TP.HCM đánh bại Buriram United 1-0 nhờ siêu phẩm phút 88 của Quốc Cường; Công an Hà Nội quyết chiến Johor Darul Ta'zim tối nay."
        ),
        (
            "Sẵn sàng FIFA U17 World Cup 2026: Giải đấu 48 đội khai mạc hôm nay 19/11 tại Qatar, HLV Cristiano Roland "
            "lần đầu có quyền yêu cầu trọng tài xem lại video FVS; đối thủ ra quân U17 Bỉ mất 4 cầu thủ từ Anderlecht."
        ),
        (
            "Tâm điểm bóng đá quốc tế: Lionel Messi thuê luật sư dọa kiện AFA; Cristiano Ronaldo vắng đề cử Quả bóng vàng Dubai 2026; "
            "Mauricio Pochettino ra mắt Carrington cùng 5 cộng sự trước đại chiến Liverpool; Philippe Diallo tranh ghế Chủ tịch FIFA; "
            "Erling Haaland chạm mốc 399 bàn thắng ở tuổi 26; Arsenal ba lần chịu phạt đền oan; bóng đá Indonesia dậy sóng khiếu nại lên FIFA."
        ),
        (
            "Tinh hoa thể thao VN & thế giới: Lê Quang Liêm tranh hạng 7 gặp Ian Nepomniachtchi tại Hungary; "
            "Carlos Alcaraz thắng Daniil Medvedev 6-2, 6-4 tại ATP Finals; nữ võ sĩ Vovinam Kim Lụa đoạt HCV lấy tiền chữa bệnh cho em; "
            "bóng bàn Việt Nam thưởng nóng 400 triệu đồng; tay vợt gốc Việt Allison Quynh Lee lập địa chấn cầu lông; "
            "HLV Dylan Kerr trở lại Hải Phòng và huyền thoại UFC Stephen Thompson chia tay bằng cú đá knock-out."
        ),
    ]

    mota_out = DAY_DIR / "mota.txt"
    write_mota_16x9(
        out_path=mota_out,
        titles_abc=titles_abc,
        chapters=chapters,
        video_type="weekly_digest",
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        sources_line="Báo Thanh Niên, VnExpress, Báo Tuổi Trẻ, Báo Dân Trí, Reuters, AP, FIFA, UEFA, ATP Tour, FIDE.",
        hashtags=[
            "#DiemDoc",
            "#DiemDocTheThao",
            "#TinTheThao1911",
            "#NguyenDinhBac",
            "#CongAnTPHCM",
            "#U17WorldCup",
            "#LionelMessi",
            "#ManUtd",
        ],
        day_str=DAY_STR,
    )
    ok(f"Đã xuất mô tả SEO chuẩn 2 phần Sentence Case -> {mota_out}")


if __name__ == "__main__":
    main()
