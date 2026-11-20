#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_mota_18_11.py — Xuất file mô tả SEO YouTube chuẩn 2 phần Sentence Case
từ chapters_18_11.json cho Bản tin thể thao ngày 18.11.2026.
"""

from __future__ import annotations

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

from diemdoc.log import die, ok
from diemdoc.publisher import write_mota_16x9

DAY_STR = "18.11.2026"
ROOT = Path(_ROOT)
DAY_DIR = ROOT / "outputs" / DAY_STR


def main() -> None:
    chap_path = DAY_DIR / "_preview_v2" / "chapters_18_11.json"
    if not chap_path.exists():
        die(f"Thiếu {chap_path} — hãy chạy build_daily_18_11_video.py trước.")

    data = json.loads(chap_path.read_text(encoding="utf-8"))
    import re as _re
    chapters: List[Tuple[str, str]] = [
        (str(c["time"]), _re.sub(r"^\[\d+\]\s*", "", str(c["label"]))) for c in data.get("chapters", [])
    ]

    titles_abc = [
        "Tuyển Việt Nam thua ngược phút cuối, Haaland cứu Na Uy, MU đón Pochettino | Điểm Đọc 18.11",
        "Đình Bắc sánh ngang Công Phượng, Brazil và Argentina đại thắng 7-0 | Điểm Đọc Thể Thao",
        "Lê Quang Liêm vào top 12 thế giới, Pochettino bay sang Man Utd, Rooney gây sốc | Điểm Đọc",
    ]

    intro_paragraphs = [
        (
            "Chào mừng quý vị và các bạn đến với Điểm Đọc — Bản tin tổng hợp thể thao ngày 18/11/2026, "
            "cập nhật toàn cảnh diễn biến nóng nhất từ 18 giờ tối qua đến sáng nay. Ở tâm điểm trong nước, "
            "đội tuyển Việt Nam đánh rơi chức vô địch Casper Cup 2026 đầy cay đắng trước Kyrgyzstan trong hai phút cuối "
            "nhưng Nguyễn Đình Bắc vẫn kịp ghi siêu phẩm sánh ngang thành tích của Nguyễn Công Phượng, còn HLV Kim Sang-sik "
            "thẳng thắn nhận lỗi và bảo vệ thủ môn trẻ Trần Trung Kiên."
        ),
        (
            "Trên sân cỏ quốc tế, UEFA Nations League chính thức chốt đủ tám đội vào tứ kết sau những màn rượt đuổi 3-2 "
            "nghẹt thở của Bồ Đào Nha và Na Uy, Brazil cùng Argentina đồng loạt đại thắng 7-0, trong khi HLV Mauricio Pochettino "
            "rời tuyển Mỹ bay chuyên cơ sang tiếp quản Manchester United. Bên cạnh đó là bước nhảy vọt lên hạng 12 thế giới "
            "của kỳ thủ Lê Quang Liêm, tấm vé bán kết sớm của Alexander Zverev tại ATP Finals 2026 và những câu chuyện hậu trường đáng chú ý."
        ),
    ]

    highlight_bullets = [
        (
            "Tâm điểm đội tuyển Việt Nam: Tuyển Việt Nam thua ngược Kyrgyzstan 1-2 ở phút 86 và 88 trên sân Thiên Trường; "
            "Nguyễn Đình Bắc cán mốc 12 bàn cho ĐTQG ngang bằng Công Phượng, tuyển Việt Nam bị trừ 5,3 điểm FIFA dù thay 8 người đúng luật IFAB; "
            "HLV Kim Sang-sik lên tiếng bảo vệ thủ môn Trần Trung Kiên và khen ngợi các tân binh."
        ),
        (
            "Sôi động bóng đá quốc tế: Bồ Đào Nha thắng Xứ Wales 3-2 khép lại vòng bảng với 15 điểm tuyệt đối; "
            "Erling Haaland lập cú đúp phút bù giờ giúp Na Uy hạ Đan Mạch 3-2 vào tứ kết Nations League; "
            "Vinícius Júnior lập hat-trick giúp Brazil thắng Singapore 7-0; Argentina vùi dập Costa Rica 7-0 nhờ cú đúp của Nico Paz và Julián Álvarez; "
            "Mauricio Pochettino chia tay tuyển Mỹ bay xuyên đêm sang Manchester United; Nhật Bản thua sốc Paraguay 1-2."
        ),
        (
            "Chuyển động Đông Nam Á & Việt Nam: Thái Lan thắng Tajikistan 3-0 lần thứ 17 vô địch King's Cup; "
            "U19 Việt Nam hòa Tajikistan 2-2 khép lại Panda Cup 2026; CLB Công an TP.HCM tự tin tiếp đón Buriram United tại Shopee Cup; "
            "TP.HCM sơ duyệt sân khấu gần 2000 chỗ ngồi cho Lễ khai mạc Đại hội Thể thao toàn quốc 2026."
        ),
        (
            "Tinh hoa thể thao & hậu trường: Lê Quang Liêm vươn lên hạng 12 thế giới với Elo 2742,4 và cầm chắc 32000 USD dù tạm thất thế trước Hans Niemann; "
            "Alexander Zverev sớm vào bán kết ATP Finals 2026; bóng đá Argentina thương tiếc tiền vệ 16 tuổi Abel Nunez; "
            "Wayne Rooney tiết lộ góc khuất tâm lý gây sốc trong giai đoạn khoác áo Man Utd."
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
        sources_line="VnExpress, Báo Thanh Niên, Báo Dân Trí, Reuters, AP, UEFA, FIFA, FAT, ATP Tour, FIDE.",
        hashtags=[
            "#DiemDoc",
            "#DiemDocTheThao",
            "#TinTheThao1811",
            "#DTQGVietNam",
            "#NguyenDinhBac",
            "#NationsLeague",
            "#ManUtd",
            "#LeQuangLiem",
        ],
        day_str=DAY_STR,
    )
    ok(f"Đã xuất mô tả SEO chuẩn 2 phần Sentence Case -> {mota_out}")


if __name__ == "__main__":
    main()
