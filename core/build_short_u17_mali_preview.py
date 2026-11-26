#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Short 9:16 bình luận trước giờ G: U17 Việt Nam vs U17 Mali (20h ngày 26.11.2026, U17 World Cup 2026).
Lưu tại outputs/Orther/26.11.2026/shorts/. Song giọng: đoạn đầu giọng Nữ (bối cảnh) — đoạn sau giọng Nam (bình luận).
Chạy: python3 -B core/build_short_u17_mali_preview.py --cloud
"""

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR / "core") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "core"))

from diemdoc import paths
from diemdoc.short_batch import ShortDayContext, run_short_batch

CAND = Path.home() / "Library" / "Caches" / "DiemDoc" / "candidates_26_11_u17"
CTX = ShortDayContext(
    day_dir=Path(paths.ROOT) / "outputs" / "Orther" / "26.11.2026",
    inspect_dir=CAND,
    work_tag="26_11_u17",
)

COLOR_ROSE = "#EF4444"
COLOR_GOLD = "#F59E0B"


def _chart() -> Dict[str, Any]:
    return {
        "7": {
            "type": "grouped_race",
            "credit": "VNEXPRESS / THANH NIÊN / TUỔI TRẺ",
            "kicker": "U17 WORLD CUP 2026 • BẢNG G • ASPIRE ZONE",
            "title": "SO KÈ TRƯỚC GIỜ G: VIỆT NAM vs MALI",
            "legend": [
                {"label": "U17 Việt Nam (HLV Cristiano Roland)", "color": COLOR_ROSE},
                {"label": "U17 Mali (HLV Soumaila Coulibaly)", "color": COLOR_GOLD},
            ],
            "sections": [
                {
                    "label": "ĐIỂM SỐ SAU 2 LƯỢT TRẬN",
                    "sub": "Mali toàn thắng và đã chắc ngôi đầu bảng G",
                    "max_axis": 6,
                    "ticks": [0, 2, 4, 6],
                    "unit": " đ",
                    "rows": [
                        {
                            "name": "U17 Mali",
                            "sub": "Thắng New Zealand 3-0, thắng Bỉ 2-1",
                            "flag": "ML",
                            "color": COLOR_GOLD,
                            "value": 6,
                            "delta": "Đã đi tiếp",
                            "leader": True,
                        },
                        {
                            "name": "U17 Việt Nam",
                            "sub": "Thua Bỉ 2-3, hòa New Zealand 3-3",
                            "flag": "VN",
                            "color": COLOR_ROSE,
                            "value": 1,
                            "delta": "Cần thắng để có 4 điểm",
                        },
                    ],
                },
                {
                    "label": "BÀN THUA SAU 2 LƯỢT TRẬN",
                    "sub": "Hàng thủ là bài toán lớn nhất của Việt Nam",
                    "max_axis": 6,
                    "ticks": [0, 2, 4, 6],
                    "unit": " bàn",
                    "rows": [
                        {
                            "name": "U17 Việt Nam",
                            "sub": "Ghi 5 bàn, thủng lưới 6 bàn",
                            "flag": "VN",
                            "color": COLOR_ROSE,
                            "value": 6,
                            "delta": "Dễ tổn thương bóng bổng",
                            "leader": True,
                        },
                        {
                            "name": "U17 Mali",
                            "sub": "Ghi 5 bàn, chỉ thủng lưới 1 bàn",
                            "flag": "ML",
                            "color": COLOR_GOLD,
                            "value": 1,
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Hạng ba hiện tại", "value": "Thứ 8/12"},
                {"label": "Chiều cao trung bình", "value": "Mali +7 cm"},
                {"label": "Khai cuộc", "value": "20h tối nay"},
            ],
            "foot_left": "Nguồn: VnExpress • Thanh Niên • Tuổi Trẻ • Dân Trí",
            "foot_right": "Thắng Mali: 4 điểm, mở cửa vào vòng 32 đội",
        }
    }


MATCH_TEXT = (
    "Lúc 20 giờ tối nay trên sân số 9 Aspire Zone tại Qatar, U17 Việt Nam bước vào lượt cuối bảng G U17 World Cup 2026 với đối thủ mạnh nhất bảng là U17 Mali. "
    "Sau hai trận, thầy trò huấn luyện viên Cristiano Roland có một điểm nhờ trận thua Bỉ 2-3 và màn rượt đuổi 3-3 với New Zealand, trong đó Duy Khang ghi bàn gỡ hòa ở phút bù giờ. "
    "Mali đã toàn thắng sáu điểm, ghi năm bàn và chỉ thủng lưới một lần nên chắc chắn đứng đầu bảng nhờ hơn Bỉ về thành tích đối đầu. "
    "Việt Nam buộc phải thắng để có bốn điểm, hiện đội đang đứng thứ tám trong nhóm 12 đội hạng ba, còn kết quả hòa chỉ còn cơ hội trên lý thuyết."
)

COMMENT_TEXT = (
    "Điểm cộng lớn nhất của Việt Nam là tinh thần, hai trận liền đều bị dẫn bàn nhưng vẫn gỡ lại, và Chu Ngọc Nguyễn Lực đã góp dấu giày vào ba trong năm bàn thắng của đội. "
    "Ba bàn từ tình huống cố định cho thấy bóng chết sẽ là vũ khí đáng giá, nhất là khi Nguyễn Lực có những cú sút phạt rất đáng gờm. "
    "Ngược lại, thủng lưới sáu bàn sau hai trận là điểm yếu rõ nhất, và Mali cao trung bình khoảng 1,82 mét, hơn Việt Nam gần 7 cm nên bóng bổng sẽ là mối đe dọa thường trực. "
    "Huấn luyện viên Soumaila Coulibaly cho biết sẽ dùng đội hình hoàn toàn khác hai trận đầu, nhưng ông cũng nhấn mạnh phải rất dè chừng Việt Nam, và các cầu thủ dự bị của Mali đều muốn chứng tỏ bản thân. "
    "Theo tôi, chìa khóa nằm ở việc chịu đựng sức ép đầu trận, giữ cự ly đội hình gọn rồi chọn đúng thời điểm tăng tốc thay vì chơi dồn dập đến cuối trận vì chênh lệch thể lực. "
    "Một bàn thắng sớm từ bóng chết có thể thay đổi hoàn toàn thế trận, và nếu giữ được kỷ luật trong chín mươi phút, tấm vé lịch sử vào vòng 32 đội vẫn còn trong tầm tay thầy trò ông Roland."
)

IMAGES: List[Dict[str, str]] = [
    {"dest": "m1_duel.jpg", "src": "c30.jpg", "credit": "DÂN TRÍ", "desc": "U17 Việt Nam tranh chấp quyết liệt ở lượt trận thứ hai bảng G"},
    {"dest": "m1_mali_team.jpg", "src": "c17.jpg", "credit": "VNEXPRESS", "desc": "Đội hình U17 Mali tại U17 World Cup 2026"},
    {"dest": "m1_mali_14.jpg", "src": "c20.jpg", "credit": "VNEXPRESS", "desc": "Cầu thủ số 14 của U17 Mali trên sân Qatar"},
    {"dest": "m1_mali_train.jpg", "src": "c14.jpg", "credit": "VNEXPRESS", "desc": "U17 Mali khởi động trên sân tập tại Qatar"},
    {"dest": "m1_vn_hug.jpg", "src": "c15.jpg", "credit": "VNEXPRESS", "desc": "U17 Việt Nam cùng ban huấn luyện ăn mừng bàn gỡ hòa"},
    {"dest": "m1_vn_cel9.jpg", "src": "c16.jpg", "credit": "VNEXPRESS", "desc": "Các cầu thủ U17 Việt Nam ăn mừng bàn thắng trước khán đài"},
    {"dest": "m1_luc_goal.jpg", "src": "c06.jpg", "credit": "THANH NIÊN", "desc": "Nguyễn Lực ghi bàn ngay đầu hiệp hai trận gặp New Zealand"},
    {"dest": "m1_mali_belgium.jpg", "src": "c10.jpg", "credit": "VNEXPRESS", "desc": "U17 Mali thi đấu giàu tốc độ và thể lực ở vòng bảng"},
    {"dest": "m1_mali_attack.jpg", "src": "c21.jpg", "credit": "TUỔI TRẺ", "desc": "Cầu thủ U17 Mali đi bóng tốc độ trước hàng thủ đối phương"},
    {"dest": "m1_vn_team.jpg", "src": "c01.jpg", "credit": "THANH NIÊN", "desc": "U17 Việt Nam trước một trận đấu tại Qatar"},
    {"dest": "m1_vn_cheer.jpg", "src": "c31.jpg", "credit": "DÂN TRÍ", "desc": "Hai cầu thủ U17 Việt Nam ăn mừng bàn thắng"},
    {"dest": "m1_luc_nz.jpg", "src": "c03.jpg", "credit": "THANH NIÊN", "desc": "Chu Ngọc Nguyễn Lực đi bóng trước hậu vệ New Zealand"},
    {"dest": "m1_vn_group.jpg", "src": "c07.jpg", "credit": "THANH NIÊN", "desc": "Nguyễn Lực cùng đồng đội U17 Việt Nam"},
    {"dest": "m1_vn_train.jpg", "src": "c25.jpg", "credit": "TUỔI TRẺ", "desc": "U17 Việt Nam tập luyện chuẩn bị cho trận gặp Mali"},
    {"dest": "m1_vn_train2.jpg", "src": "c13.jpg", "credit": "VNEXPRESS", "desc": "Các cầu thủ U17 Việt Nam luyện tập tại Doha"},
    {"dest": "m1_mali_coach.jpg", "src": "c08.jpg", "credit": "VNEXPRESS", "desc": "Huấn luyện viên U17 Mali trả lời phỏng vấn trước trận"},
    {"dest": "m1_roland_1.jpg", "src": "c11.jpg", "credit": "VNEXPRESS", "desc": "Huấn luyện viên Cristiano Roland trên sân tập"},
    {"dest": "m1_roland_2.jpg", "src": "c27.jpg", "credit": "DÂN TRÍ", "desc": "Huấn luyện viên Roland chỉ đạo các cầu thủ U17 Việt Nam"},
    {"dest": "m1_vn_cel17.jpg", "src": "c28.jpg", "credit": "DÂN TRÍ", "desc": "Nguyễn Lực và Đại Nhân ăn mừng bàn thắng"},
]

PLAN_SLOTS = [
    ("title", 0, "m1_duel.jpg"),
    ("title", 0, "m1_mali_team.jpg"),
    ("title", 0, "m1_mali_14.jpg"),
    ("sentence", 1, "m1_mali_train.jpg"),
    ("sentence", 1, "m1_vn_hug.jpg"),
    ("sentence", 2, "m1_vn_cel9.jpg"),
    ("sentence", 2, "m1_luc_goal.jpg"),
    ("sentence", 3, "m1_mali_belgium.jpg"),
    ("sentence", 3, "m1_mali_attack.jpg"),
    ("sentence", 4, "m1_vn_team.jpg"),
    ("sentence", 4, "m1_vn_cheer.jpg"),
    ("sentence", 5, "m1_luc_nz.jpg"),
    ("sentence", 5, "m1_vn_group.jpg"),
    ("sentence", 6, "m1_vn_train.jpg"),
    ("sentence", 6, "m1_vn_train2.jpg"),
    ("sentence", 7, "m1_mali_attack.jpg"),
    ("sentence", 7, "m1_mali_train.jpg"),
    ("sentence", 8, "m1_mali_coach.jpg"),
    ("sentence", 8, "m1_mali_14.jpg"),
    ("sentence", 9, "m1_roland_1.jpg"),
    ("sentence", 9, "m1_roland_2.jpg"),
    ("sentence", 10, "m1_vn_cel17.jpg"),
    ("sentence", 10, "m1_vn_hug.jpg"),
]

ITEM: Dict[str, Any] = {
    "id": 1,
    "slug": "Short_Nhan_Dinh_U17_Viet_Nam_vs_U17_Mali_20h",
    "voice_preset": "mixed",
    "voice_segments": [
        {"voice_preset": "secondary", "text": MATCH_TEXT},
        {"voice_preset": "primary", "text": COMMENT_TEXT},
    ],
    "group": "U17 WORLD CUP 2026 • BẢNG G",
    "title": "U17 Việt Nam quyết đấu U17 Mali: Trận sinh tử lúc 20h tối nay",
    "summary": f"{MATCH_TEXT} {COMMENT_TEXT}",
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí",
    "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ / DÂN TRÍ",
    "credit": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ / DÂN TRÍ",
    "hide_date_chip": True,
    "seo_title": "Nhận định U17 Việt Nam vs U17 Mali 20h: thắng mới mở cửa vào vòng 32 đội",
    "description": [
        "Lúc 20h tối 26/11/2026 tại sân số 9 Aspire Zone (Qatar), U17 Việt Nam đá lượt cuối bảng G U17 World Cup 2026 gặp U17 Mali. Việt Nam có 1 điểm sau trận thua Bỉ 2-3 và hòa New Zealand 3-3, trong khi Mali toàn thắng 6 điểm và đã chắc ngôi đầu bảng.",
        "Thắng Mali, thầy trò huấn luyện viên Cristiano Roland sẽ có 4 điểm và mở cửa vào vòng 32 đội; hòa chỉ còn cơ hội trên lý thuyết.",
        "Góc nhìn bình luận: tinh thần quật cường và các tình huống cố định là vũ khí của Việt Nam, nhưng hàng thủ (thủng lưới 6 bàn sau 2 trận) và chênh lệch thể hình, thể lực với Mali (cao hơn gần 7 cm) là bài toán lớn nhất.",
    ],
    "hashtags": [
        "#Shorts", "#DiemDoc", "#U17VietNam", "#U17Mali", "#U17WorldCup2026",
        "#NhanDinhBongDa", "#HLVRoland", "#NguyenLuc",
    ],
    "hook": {
        "kicker": "TRẬN SINH TỬ • U17 WORLD CUP 2026",
        "vs_badge": "VIỆT NAM vs MALI",
        "stat_val": 20,
        "stat_unit": "H",
        "stat_label": "THẮNG MALI MỚI MỞ CỬA VÀO VÒNG 32 ĐỘI",
        "stat_sub": "VIỆT NAM 1 ĐIỂM • MALI 6 ĐIỂM • KHAI CUỘC 20H TỐI NAY",
        "opp_val": 0,
        "count_dur": 0.65,
        "pills": [
            {"text": "CẦN 4 ĐIỂM", "style": "cyan", "delay": 1.15},
            {"text": "MALI CAO HƠN 7 CM", "style": "gold", "delay": 1.85},
            {"text": "BÓNG CHẾT LÀ VŨ KHÍ", "style": "", "delay": 2.50},
        ],
        "fast_cut": True,
    },
    "sentence_charts": _chart(),
    "thumb": {
        "image": "m1_vn_cel9.jpg",
        "badge": "VIỆT NAM vs MALI",
        "kicker": "U17 WORLD CUP 2026 • LƯỢT CUỐI BẢNG G",
        "hero_html": 'U17 VIỆT NAM <span class="hl">QUYẾT ĐẤU MALI 20H</span>',
        "subtitle": "Thắng để có 4 điểm, hòa gần như hết cửa; Mali cao hơn gần 7 cm",
        "tag_a": "ĐIỂM ĐỌC SHORTS",
        "tag_b": "26.11.2026",
        "obj_pos": "center 25%",
    },
    "images": IMAGES,
    "plan_slots": PLAN_SLOTS,
}


def main() -> None:
    run_short_batch(CTX, [ITEM], "XUẤT BẢN SHORT NHẬN ĐỊNH U17 VIỆT NAM vs U17 MALI (26.11.2026)")


if __name__ == "__main__":
    main()
