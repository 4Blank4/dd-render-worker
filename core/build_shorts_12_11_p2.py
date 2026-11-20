#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng Video Short 9:16 Tin #03 ngày 12.11.2026 tại outputs/Orther/12.11.2026/shorts/:
  - Tin #03 (Giọng Nam — Minh Quân Pro Mẫu 15):
    Steven Gerrard đánh giá Lamine Yamal xuất sắc hơn Messi & Ronaldo ở tuổi 19,
    tích hợp 3 cảnh đồ thị dữ liệu động Cyber-Stadium (DataViz + phong cách 05.11.2026).

Dùng chung bộ pipeline chuẩn tại core/diemdoc/short_batch.py.
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

CTX = ShortDayContext(
    day_dir=Path(paths.ROOT) / "outputs" / "Orther" / "12.11.2026",
    inspect_dir=Path.home() / "Library" / "Caches" / "DiemDoc" / "inspect_12_11_p2",
    work_tag="12_11_p2",
)

AVATAR_YAMAL = "outputs/Orther/12.11.2026/assets/avatars/yamal.jpg"
AVATAR_MESSI = "outputs/Orther/12.11.2026/assets/avatars/messi.jpg"
AVATAR_RONALDO = "outputs/Orther/12.11.2026/assets/avatars/ronaldo.jpg"

COLOR_YAMAL = "#0095D6"
COLOR_MESSI = "#C98500"
COLOR_RONALDO = "#D55181"


def _charts_yamal_19() -> Dict[str, Any]:
    """Khởi tạo 3 cảnh đồ thị dữ liệu động chuẩn DataViz cho Tin #03."""
    return {
        # Câu 2: 73 bàn, 69 kiến tạo vs Messi (36 bàn, 14 kiến tạo) & Ronaldo (22 bàn, 22 kiến tạo)
        "2": {
            "type": "grouped_race",
            "credit": "VNEXPRESS / ĐIỂM ĐỌC DATA",
            "kicker": "DỮ LIỆU SỰ NGHIỆP • ĐẾN CỘT MỐC 19 TUỔI",
            "title": "SO SÁNH YAMAL, MESSI & RONALDO Ở TUỔI 19",
            "legend": [
                {"label": "Lamine Yamal", "color": COLOR_YAMAL},
                {"label": "Lionel Messi", "color": COLOR_MESSI},
                {"label": "Cristiano Ronaldo", "color": COLOR_RONALDO},
            ],
            "sections": [
                {
                    "label": "BÀN THẮNG Ở TUỔI 19",
                    "sub": "CLB & Đội tuyển quốc gia",
                    "max_axis": 80,
                    "ticks": [0, 20, 40, 60, 80],
                    "unit": "",
                    "rows": [
                        {
                            "name": "Lamine Yamal",
                            "sub": "Tây Ban Nha • Barca",
                            "flag": "ES",
                            "avatar": AVATAR_YAMAL,
                            "color": COLOR_YAMAL,
                            "value": 73,
                            "delta": "+37 vs Messi",
                            "leader": True,
                        },
                        {
                            "name": "Lionel Messi",
                            "sub": "Argentina • Barca",
                            "flag": "AR",
                            "avatar": AVATAR_MESSI,
                            "color": COLOR_MESSI,
                            "value": 36,
                        },
                        {
                            "name": "Cristiano Ronaldo",
                            "sub": "Bồ Đào Nha • MU",
                            "flag": "PT",
                            "avatar": AVATAR_RONALDO,
                            "color": COLOR_RONALDO,
                            "value": 22,
                        },
                    ],
                },
                {
                    "label": "KIẾN TẠO Ở TUỔI 19",
                    "sub": "Đường chuyền thành bàn",
                    "max_axis": 80,
                    "ticks": [0, 20, 40, 60, 80],
                    "unit": "",
                    "rows": [
                        {
                            "name": "Lamine Yamal",
                            "sub": "Tây Ban Nha • Barca",
                            "flag": "ES",
                            "avatar": AVATAR_YAMAL,
                            "color": COLOR_YAMAL,
                            "value": 69,
                            "delta": "+47 vs CR7",
                            "leader": True,
                        },
                        {
                            "name": "Cristiano Ronaldo",
                            "sub": "Bồ Đào Nha • MU",
                            "flag": "PT",
                            "avatar": AVATAR_RONALDO,
                            "color": COLOR_RONALDO,
                            "value": 22,
                        },
                        {
                            "name": "Lionel Messi",
                            "sub": "Argentina • Barca",
                            "flag": "AR",
                            "avatar": AVATAR_MESSI,
                            "color": COLOR_MESSI,
                            "value": 14,
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Tổng đóng góp (G+A)", "value": "142", "sub": "73 bàn + 69 kiến tạo"},
                {"label": "So với Lionel Messi", "value": "Gấp 2,8x", "sub": "142 vs 50 G+A tuổi 19"},
                {"label": "So với Cristiano Ronaldo", "value": "Gấp 3,2x", "sub": "142 vs 44 G+A tuổi 19"},
            ],
            "foot_left": "Nguồn: VnExpress • Tổng hợp đến tháng 11/2026",
            "foot_right": "Mốc đối chiếu: 19 tuổi",
        },
        # Câu 3: Yamal (142 G+A) vs Messi + Ronaldo cộng lại (94 G+A)
        "3": {
            "type": "duel_stack",
            "credit": "VNEXPRESS / ĐIỂM ĐỌC DATA",
            "kicker": "ĐỐI CHIẾU TỔNG LỰC • MỘT ĐẤU HAI",
            "title": "MỘT MÌNH YAMAL ÁP ĐẢO MESSI + RONALDO CỘNG LẠI",
            "legend": [
                {"label": "Lamine Yamal (Đơn lẻ)", "color": COLOR_YAMAL},
                {"label": "Lionel Messi", "color": COLOR_MESSI},
                {"label": "Cristiano Ronaldo", "color": COLOR_RONALDO},
            ],
            "hero": {
                "left_avatar": AVATAR_YAMAL,
                "left_color": COLOR_YAMAL,
                "left_val": 142,
                "left_label": "Lamine Yamal (G+A)",
                "center_badge": "+48 G+A",
                "right_val": 94,
                "right_label": "Messi (50) + CR7 (44)",
                "right_avatars": [
                    {"src": AVATAR_MESSI, "color": COLOR_MESSI},
                    {"src": AVATAR_RONALDO, "color": COLOR_RONALDO},
                ],
            },
            "sections": [
                {
                    "label": "TỔNG BÀN THẮNG & KIẾN TẠO (G+A)",
                    "max_axis": 160,
                    "ticks": [0, 40, 80, 120, 160],
                    "rows": [
                        {
                            "name": "Lamine Yamal",
                            "sub": "Đơn lẻ",
                            "flag": "ES",
                            "avatar": AVATAR_YAMAL,
                            "color": COLOR_YAMAL,
                            "value": 142,
                            "delta": "+48",
                            "leader": True,
                        },
                        {
                            "name": "Messi + Ronaldo",
                            "sub": "Cộng dồn hai siêu sao",
                            "avatars": [
                                {"src": AVATAR_MESSI, "color": COLOR_MESSI},
                                {"src": AVATAR_RONALDO, "color": COLOR_RONALDO},
                            ],
                            "value": 94,
                            "breakdown": "50 + 44",
                            "segments": [
                                {"value": 50, "color": COLOR_MESSI},
                                {"value": 44, "color": COLOR_RONALDO},
                            ],
                        },
                    ],
                },
                {
                    "label": "BÀN THẮNG",
                    "max_axis": 80,
                    "ticks": [0, 20, 40, 60, 80],
                    "rows": [
                        {
                            "name": "Lamine Yamal",
                            "sub": "Đơn lẻ",
                            "flag": "ES",
                            "avatar": AVATAR_YAMAL,
                            "color": COLOR_YAMAL,
                            "value": 73,
                            "delta": "+15",
                            "leader": True,
                        },
                        {
                            "name": "Messi + Ronaldo",
                            "sub": "Cộng dồn",
                            "avatars": [
                                {"src": AVATAR_MESSI, "color": COLOR_MESSI},
                                {"src": AVATAR_RONALDO, "color": COLOR_RONALDO},
                            ],
                            "value": 58,
                            "breakdown": "36 + 22",
                            "segments": [
                                {"value": 36, "color": COLOR_MESSI},
                                {"value": 22, "color": COLOR_RONALDO},
                            ],
                        },
                    ],
                },
                {
                    "label": "KIẾN TẠO",
                    "max_axis": 80,
                    "ticks": [0, 20, 40, 60, 80],
                    "rows": [
                        {
                            "name": "Lamine Yamal",
                            "sub": "Đơn lẻ",
                            "flag": "ES",
                            "avatar": AVATAR_YAMAL,
                            "color": COLOR_YAMAL,
                            "value": 69,
                            "delta": "+33",
                            "leader": True,
                        },
                        {
                            "name": "Messi + Ronaldo",
                            "sub": "Cộng dồn",
                            "avatars": [
                                {"src": AVATAR_MESSI, "color": COLOR_MESSI},
                                {"src": AVATAR_RONALDO, "color": COLOR_RONALDO},
                            ],
                            "value": 36,
                            "breakdown": "14 + 22",
                            "segments": [
                                {"value": 14, "color": COLOR_MESSI},
                                {"value": 22, "color": COLOR_RONALDO},
                            ],
                        },
                    ],
                },
            ],
            "foot_left": "Nguồn: VnExpress Thể thao",
            "foot_right": "Tất cả thống kê đến tuổi 19",
        },
        # Câu 4: 8 danh hiệu lớn vs Messi (5) & Ronaldo (2)
        "4": {
            "type": "trophy_race",
            "credit": "VNEXPRESS / ĐIỂM ĐỌC DATA",
            "kicker": "THÀNH TÍCH TẬP THỂ • ĐỈNH CAO QUỐC TẾ & CLB",
            "title": "BỘ SƯU TẬP 8 DANH HIỆU LỚN Ở TUỔI 19",
            "legend": [
                {"label": "Lamine Yamal", "color": COLOR_YAMAL},
                {"label": "Lionel Messi", "color": COLOR_MESSI},
                {"label": "Cristiano Ronaldo", "color": COLOR_RONALDO},
            ],
            "sections": [
                {
                    "label": "SỐ DANH HIỆU TẬP THỂ Ở TUỔI 19",
                    "sub": "Cấp CLB & Đội tuyển quốc gia",
                    "max_axis": 10,
                    "ticks": [0, 2, 4, 6, 8, 10],
                    "unit": "",
                    "rows": [
                        {
                            "name": "Lamine Yamal",
                            "sub": "Tây Ban Nha • Barca",
                            "flag": "ES",
                            "avatar": AVATAR_YAMAL,
                            "color": COLOR_YAMAL,
                            "value": 8,
                            "delta": "+3 vs Messi",
                            "leader": True,
                        },
                        {
                            "name": "Lionel Messi",
                            "sub": "Barca & Argentina",
                            "flag": "AR",
                            "avatar": AVATAR_MESSI,
                            "color": COLOR_MESSI,
                            "value": 5,
                        },
                        {
                            "name": "Cristiano Ronaldo",
                            "sub": "Sporting & Man Utd",
                            "flag": "PT",
                            "avatar": AVATAR_RONALDO,
                            "color": COLOR_RONALDO,
                            "value": 2,
                        },
                    ],
                },
            ],
            "trophy_title": "CHI TIẾT 8 CHIẾC CÚP CỦA LAMINE YAMAL",
            "trophy_sub": "Gồm cả Euro 2024 và World Cup 2026",
            "trophies": [
                {"count": "1x", "name": "World Cup", "sub": "ĐT Tây Ban Nha • 2026", "major": True},
                {"count": "1x", "name": "Euro", "sub": "ĐT Tây Ban Nha • 2024", "major": True},
                {"count": "3x", "name": "La Liga", "sub": "FC Barcelona", "major": False},
                {"count": "2x", "name": "Siêu cúp Tây Ban Nha", "sub": "FC Barcelona", "major": False},
                {"count": "1x", "name": "Cúp Nhà vua", "sub": "FC Barcelona", "major": False},
                {"count": "8 CÚP", "name": "Tổng danh hiệu lớn", "sub": "Hơn Messi + CR7 cộng lại (7)", "major": True},
            ],
            "banner": {
                "tag": "CỘT MỐC 2023",
                "text": "Ra mắt và đá chính thường xuyên cho Barcelona ngay từ tuổi 16",
            },
            "foot_left": "Nguồn: VnExpress Thể thao",
            "foot_right": "Không tính giải thưởng cá nhân",
        },
    }


NEWS_DATA_12_11_P2: List[Dict[str, Any]] = [
    {
        "id": 3,
        "slug": "Short_Gerrard_Yamal_Hay_Hon_Messi_Ronaldo_Tuoi_19",
        "voice_preset": "primary",  # Giọng Nam: Minh Quân Pro (Mẫu 15)
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Gerrard: Yamal hay hơn Messi và Ronaldo ở tuổi 19",
        "summary": (
            "Chia sẻ trên podcast The Overlap ngày 10 tháng 11, huyền thoại Liverpool Steven Gerrard khẳng định Lamine Yamal xuất sắc hơn cả Lionel Messi và Cristiano Ronaldo ở tuổi 19. "
            "Thống kê cho thấy tính đến tuổi 19, ngôi sao của Barcelona đã ghi tới 73 bàn thắng cùng 69 kiến tạo, vượt xa mức 36 bàn của Messi và 22 bàn của Ronaldo. "
            "Thậm chí, tổng số bàn thắng và kiến tạo của riêng Yamal là 142, áp đảo hoàn toàn con số 94 nếu cộng thành tích của cả Messi lẫn Ronaldo lại. "
            "Ở đấu trường tập thể, tiền đạo sinh năm 2007 cũng sở hữu tám danh hiệu lớn gồm Euro 2024, World Cup 2026, ba chức vô địch La Liga, hai Siêu cúp Tây Ban Nha và một Cúp Nhà vua. "
            "Dù vậy, Gerrard cảnh báo duy trì phong độ ghi trên 40 bàn mỗi mùa suốt hàng chục năm trước chấn thương và sự bắt bài mới là thử thách quyết định. "
            "Quan điểm này nhận được sự đồng tình từ Simone Inzaghi và Hansi Flick, trong khi HLV Luis de la Fuente khuyên người hâm mộ tránh gây áp lực quá sớm lên tài năng trẻ này."
        ),
        "source": "VnExpress",
        "news_source": "VnExpress",
        "credit": "WIKIMEDIA COMMONS / ARCHIVE",
        "hide_date_chip": True,
        "seo_title": "Gerrard: Yamal hay hơn Messi và Ronaldo ở tuổi 19 #Shorts",
        "description": [
            "Huyền thoại Liverpool Steven Gerrard gây chú ý khi nhận định trên podcast The Overlap ngày 10/11 rằng ở cột mốc tuổi 19, Lamine Yamal xuất sắc hơn cả Lionel Messi lẫn Cristiano Ronaldo.",
            "Tính đến tuổi 19, Lamine Yamal sở hữu 73 bàn thắng, 69 kiến tạo (142 G+A) cùng 8 danh hiệu tập thể gồm Euro 2024, World Cup 2026, 3 La Liga, 2 Siêu cúp Tây Ban Nha và 1 Cúp Nhà vua — vượt trội tổng thành tích tuổi 19 của Messi (36 bàn, 14 kiến tạo, 5 cúp) và Ronaldo (22 bàn, 22 kiến tạo, 2 cúp) cộng lại.",
            "Bên cạnh đó, Steven Gerrard, HLV Hansi Flick, Simone Inzaghi và Luis de la Fuente đều nhấn mạnh yếu tố duy trì sự ổn định lâu dài để chạm tới đẳng cấp bền bỉ hơn một thập kỷ của hai huyền thoại.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#LamineYamal", "#StevenGerrard", "#LionelMessi",
            "#CristianoRonaldo", "#Barcelona", "#BongDaQuocTe", "#TheOverlap",
        ],
        "thumb": {
            "image": "Tin_03_2.jpg",
            "badge": "BÓNG ĐÁ QUỐC TẾ",
            "kicker": "SO SÁNH TUỔI 19 • ĐỒ HỌA SỐ LIỆU",
            "hero_html": 'GERRARD: YAMAL HAY HƠN <span class="hl">MESSI & RONALDO</span>',
            "subtitle": "73 bàn, 69 kiến tạo, 8 danh hiệu: áp đảo tổng thành tích của cả hai huyền thoại cộng lại",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "12.11.2026",
            "obj_pos": "center 12%",
        },
        "sentence_charts": _charts_yamal_19(),
        "images": [
            # Title (0)
            {"dest": "Tin_03_1.jpg", "src": "candidates/tin02_10_8.jpg", "credit": "FC BARCELONA / ARCHIVE", "desc": "Lamine Yamal áo số 10 Barcelona ăn mừng động tác vương miện"},
            {"dest": "Tin_03_2.jpg", "src": "candidates/wm_yamal_3.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Chân dung Lamine Yamal khoác áo số 19 tuyển Tây Ban Nha"},
            # Câu 1: Steven Gerrard trên podcast The Overlap nhắc đến Messi và Ronaldo
            {"dest": "Tin_03_3.jpg", "src": "candidates/wm_gerrard_4.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Huyền thoại Liverpool Steven Gerrard ăn mừng chiến thắng"},
            {"dest": "Tin_03_4.jpg", "src": "candidates/c01_a_resized.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Cristiano Ronaldo và Lionel Messi đối đầu trong màu áo ĐTQG"},
            # Câu 2 (nền mờ dưới Chart 1): Messi 2007 tuổi 19 & Ronaldo Man Utd thời trẻ
            {"dest": "Tin_03_5.jpg", "src": "candidates/wm_messi_2007_2.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Lionel Messi thời trẻ ở tuổi 19 ghi bàn cho Barcelona năm 2007"},
            {"dest": "Tin_03_6.jpg", "src": "candidates/wm_ronaldo_mu_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Cristiano Ronaldo thời trẻ khoác áo số 7 Manchester United"},
            # Câu 3 (nền mờ dưới Chart 2): Messi dứt điểm Barca & Ronaldo trẻ Man Utd
            {"dest": "Tin_03_7.jpg", "src": "candidates/wm_messi_fcb.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Lionel Messi dứt điểm trong màu áo Barcelona"},
            {"dest": "Tin_03_8.jpg", "src": "candidates/wm_ronaldo_mu_4.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Chân dung Cristiano Ronaldo thời khoác áo Man Utd"},
            # Câu 4 (nền mờ dưới Chart 3): Yamal nâng cúp vô địch & ăn mừng huy chương
            {"dest": "Tin_03_9.jpg", "src": "candidates/tin02_10_9.jpg", "credit": "UEFA / EURO ARCHIVE", "desc": "Lamine Yamal cùng tuyển Tây Ban Nha nâng cao cúp vô địch"},
            {"dest": "Tin_03_10.jpg", "src": "candidates/wm_yamal_2.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Lamine Yamal nâng niu huy chương vàng cùng tuyển Tây Ban Nha"},
            # Câu 5: Cảnh báo thử thách duy trì >40 bàn/mùa, tránh chấn thương
            {"dest": "Tin_03_11.jpg", "src": "candidates/wm_gerrard_3.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Steven Gerrard thi đấu trên sân cỏ"},
            {"dest": "Tin_03_12.jpg", "src": "candidates/wm_yamal_4.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Lamine Yamal đi bóng tốc độ trong màu áo tuyển Tây Ban Nha"},
            # Câu 6: Bình luận của Simone Inzaghi, Hansi Flick và Luis de la Fuente
            {"dest": "Tin_03_13.jpg", "src": "candidates/wm_inzaghi_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Cựu HLV Inter Milan Simone Inzaghi"},
            {"dest": "Tin_03_14.jpg", "src": "candidates/wm_flick_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "HLV trưởng Barcelona Hansi Flick"},
            {"dest": "Tin_03_15.jpg", "src": "candidates/wm_delafuente_3.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "HLV trưởng đội tuyển Tây Ban Nha Luis de la Fuente"},
        ],
        "plan_slots": [
            ("title", 0, "Tin_03_1.jpg"),
            ("title", 0, "Tin_03_2.jpg"),
            ("sentence", 1, "Tin_03_3.jpg"),
            ("sentence", 1, "Tin_03_4.jpg"),
            ("sentence", 2, "Tin_03_5.jpg"),
            ("sentence", 2, "Tin_03_6.jpg"),
            ("sentence", 3, "Tin_03_7.jpg"),
            ("sentence", 3, "Tin_03_8.jpg"),
            ("sentence", 4, "Tin_03_9.jpg"),
            ("sentence", 4, "Tin_03_10.jpg"),
            ("sentence", 5, "Tin_03_11.jpg"),
            ("sentence", 5, "Tin_03_12.jpg"),
            ("sentence", 6, "Tin_03_13.jpg"),
            ("sentence", 6, "Tin_03_14.jpg"),
            ("sentence", 6, "Tin_03_15.jpg"),
        ],
    },
]


def main() -> None:
    run_short_batch(
        ctx=CTX,
        items=NEWS_DATA_12_11_P2,
        title_banner="SẢN XUẤT VIDEO SHORT TIN #03 NGÀY 12.11.2026 (GERRARD: YAMAL HAY HƠN MESSI & RONALDO TUỔI 19)",
    )


if __name__ == "__main__":
    main()
