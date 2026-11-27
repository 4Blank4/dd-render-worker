# -*- coding: utf-8 -*-
"""
build_mota_27_11.py — Sinh mô tả YouTube chuẩn 2 phần `outputs/27.11.2026/mota.txt`
từ dữ liệu chapters thực tế và module xuất bản trung tâm `publisher.write_mota_16x9`.
Đồng nhất 3 Option tiêu đề với 3 kiểu thumbnail (1 ảnh -> 2 ảnh -> 3 ảnh).
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

DAY_STR = "27.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
CHAPTERS_FILE = OUT_DIR / "_preview_v2" / "chapters_27_11.json"


def main() -> None:
    if not CHAPTERS_FILE.exists():
        raise FileNotFoundError(f"Chưa có file chapters: {CHAPTERS_FILE}")
    raw = json.loads(CHAPTERS_FILE.read_text(encoding="utf-8"))

    chapters: List[Tuple[str, str]] = [
        (c["time"], c["label"]) for c in raw.get("chapters", [])
    ]

    # Đồng nhất 100% theo quy chuẩn: 1 sự kiện -> 2 sự kiện -> 3 sự kiện (khớp thumbnail A/B/C)
    titles_abc = [
        "U17 Việt Nam thua Mali 0-2, khép lại hành trình lịch sử tại U17 World Cup 2026",
        "U17 Việt Nam dừng bước trước Mali, Mỹ Tiên hạ Ánh Viên lập kỷ lục 8 HCV",
        "U17 Việt Nam rời World Cup, Mỹ Tiên hạ Ánh Viên & AC Milan ngược dòng 4-2",
    ]

    intro_paragraphs = [
        (
            "Bản tin Điểm Đọc Thể Thao ngày 27/11/2026 tổng hợp toàn cảnh những diễn biến nóng nhất "
            "của thể thao Việt Nam và thế giới: U17 World Cup 2026, Đại hội Thể thao toàn quốc 2026, "
            "Quả bóng vàng Việt Nam, V-League 2026-2027, Billiards PBA Tour, AFC Champions League Two, "
            "UEFA Europa League, Ngoại hạng Anh, Quần vợt, Cờ vua Thế giới, Formula 1 và NFL."
        )
    ]

    highlight_bullets = [
        "U17 Việt Nam để thua U17 Mali 0-2 ở lượt cuối bảng G U17 World Cup 2026 nhưng vẫn lập cột mốc lịch sử với thứ hạng ba bảng đấu và năm bàn thắng; HLV Cristiano Roland và Chu Ngọc Nguyễn Lực rơi nước mắt tri ân khán giả.",
        "Tại Đại hội Thể thao toàn quốc 2026, kình ngư Võ Thị Mỹ Tiên lần thứ hai đánh bại Nguyễn Thị Ánh Viên ở nội dung 200m tự do để chạm mốc tám HCV cá nhân; Lại Lý Huynh - Nhật Quang thắng siêu kinh điển cờ tướng, giúp TP. HCM dẫn đầu với 86 HCV.",
        "Phó Chủ tịch VFF Trần Anh Tú tiết lộ đội trưởng Nguyễn Quang Hải có nguyện vọng chia tay tuyển Việt Nam nhưng HLV Kim Sang Sik chưa đồng ý; trong khi vòng 9 V-League chiều nay chứng kiến hai trận đại chiến Nam Định gặp CAHN và SLNA tiếp Ninh Bình.",
        "Cơ thủ Mã Minh Cẩm ngược dòng cứu match-point để hạ cựu số 1 thế giới Kim Jun-tae ở PBA Tour; còn CLB Svay Rieng của Campuchia gây địa chấn Cúp C2 châu Á khi đánh bại Machida Zelvia 2-0.",
        "Rạng sáng 27/11 tại Europa League, AC Milan ngược dòng thắng Olympiacos 4-2, Juventus đè bẹp Omonia Nicosia 4-1, Bournemouth dù mất người vẫn thắng Celta Vigo 2-1 để trở thành CLB Anh đầu tiên toàn thắng cả năm trận mở màn.",
        "Thể thao quốc tế: Jannik Sinner phẫu thuật đầu gối lỡ hẹn Australian Open 2027; tuyển Anh vào bán kết Davis Cup sau bảy năm; bốn ông lớn Ngoại hạng Anh chuẩn bị kiện Man City; Gukesh và Sindarov hòa 1,5 - 1,5 sau ván 3 gần năm giờ.",
    ]

    hashtags = [
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TinTheThao",
        "#U17VietNam",
        "#U17WorldCup",
        "#DaiHoiTheThaoToanQuoc2026",
        "#VoThiMyTien",
        "#QuangHai",
        "#VLeague",
        "#ACMilan",
        "#EuropaLeague",
    ]

    out_path = publisher.write_mota_16x9(
        out_path=OUT_DIR / "mota.txt",
        titles_abc=titles_abc,
        video_type="daily_digest",
        day_str=DAY_STR,
        intro_paragraphs=intro_paragraphs,
        highlight_bullets=highlight_bullets,
        chapters=chapters,
        sources_line="📰 Nguồn tổng hợp & đối chiếu: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian.",
        hashtags=hashtags,
    )
    print(f"[ok] Đã xuất mô tả SEO chuẩn 2 phần: {out_path}")


if __name__ == "__main__":
    main()
