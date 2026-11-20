#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng 2 Video Shorts 9:16 tiếp theo trong ngày 12.11.2026 tại outputs/Orther/12.11.2026/shorts/:
  - Tin #04 (Giọng Nam — Minh Quân Pro Mẫu 15):
    Mỹ đột ngột rút khỏi U17 World Cup 2026 vì lo ngại xung đột Trung Đông & lịch đấu U17 Việt Nam ở bảng G
  - Tin #05 (Giọng Nữ — Ngọc Huyền Mẫu 14):
    Lê Quang Liêm thắng ván cờ đạt độ chính xác 99% tại Giải cờ vua toàn năng thế giới 2026
    tích hợp 2 cảnh đồ thị dữ liệu động Cyber-Stadium DataViz (99% vs 85% & BXH Bảng B Elo 2735).

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
    inspect_dir=Path.home() / "Library" / "Caches" / "DiemDoc" / "inspect_12_11_p3",
    work_tag="12_11_p3",
)

AV_QL = "outputs/Orther/12.11.2026/assets/avatars/quangliem.jpg"
AV_CARUANA = "outputs/Orther/12.11.2026/assets/avatars/caruana.jpg"
AV_PRAG = "outputs/Orther/12.11.2026/assets/avatars/prag.jpg"
AV_KEYMER = "outputs/Orther/12.11.2026/assets/avatars/keymer.jpg"
AV_ARTEMIEV = "outputs/Orther/12.11.2026/assets/avatars/artemiev.jpg"
AV_RAPPORT = "outputs/Orther/12.11.2026/assets/avatars/rapport.jpg"

COLOR_CYAN = "#0095D6"
COLOR_AMBER = "#C98500"
COLOR_ROSE = "#D55181"


def _charts_quang_liem() -> Dict[str, Any]:
    """Khởi tạo 2 cảnh đồ thị dữ liệu động Cyber-Stadium DataViz cho Tin #05."""
    return {
        # Câu 2: Độ chính xác 99% vs 85%, thắng 4-1 điểm, diễn biến nước 14 / 22 / 32
        "2": {
            "type": "grouped_race",
            "credit": "VNEXPRESS / ĐIỂM ĐỌC DATA",
            "kicker": "PHÂN TÍCH VÁN THẮNG LƯỢT VỀ • BUDAPEST 2026",
            "title": "ĐỘ CHÍNH XÁC 99% TRƯỚC VLADISLAV ARTEMIEV",
            "legend": [
                {"label": "Lê Quang Liêm (Quân Trắng)", "color": COLOR_CYAN},
                {"label": "Vladislav Artemiev (Quân Đen)", "color": COLOR_ROSE},
            ],
            "sections": [
                {
                    "label": "TỶ LỆ NƯỚC ĐI CHÍNH XÁC",
                    "sub": "Đánh giá bằng động cơ phân tích cờ vua",
                    "max_axis": 100,
                    "ticks": [0, 25, 50, 75, 100],
                    "unit": "%",
                    "rows": [
                        {
                            "name": "Lê Quang Liêm",
                            "sub": "Việt Nam • Quân Trắng",
                            "flag": "VN",
                            "avatar": AV_QL,
                            "color": COLOR_CYAN,
                            "value": 99,
                            "delta": "+14% vs Đen",
                            "leader": True,
                        },
                        {
                            "name": "V. Artemiev",
                            "sub": "FIDE • Quân Đen",
                            "flag": "FIDE",
                            "avatar": AV_ARTEMIEV,
                            "color": COLOR_ROSE,
                            "value": 85,
                        },
                    ],
                },
                {
                    "label": "ĐIỂM ĐỐI ĐẦU SAU 2 LƯỢT (11/11)",
                    "sub": "Thể thức giải: Thắng 3đ • Hòa 1đ • Thua 0đ",
                    "max_axis": 4,
                    "ticks": [0, 1, 2, 3, 4],
                    "unit": " đ",
                    "rows": [
                        {
                            "name": "Lê Quang Liêm",
                            "sub": "1 thắng, 1 hòa",
                            "flag": "VN",
                            "avatar": AV_QL,
                            "color": COLOR_CYAN,
                            "value": 4,
                            "delta": "+3 điểm",
                            "leader": True,
                        },
                        {
                            "name": "V. Artemiev",
                            "sub": "1 hòa, 1 thua",
                            "flag": "FIDE",
                            "avatar": AV_ARTEMIEV,
                            "color": COLOR_ROSE,
                            "value": 1,
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Khai cuộc Catalan", "value": "14 nước", "sub": "Đi chuẩn như thuộc bài"},
                {"label": "Nước đi thí mã", "value": "Nước 22", "sub": "Phá vỡ thành đối thủ"},
                {"label": "Kết thúc ván đấu", "value": "Nước 32", "sub": "Thế chiếu hết sau 1 nước"},
            ],
            "foot_left": "Nguồn: VnExpress • Total Chess 2026",
            "foot_right": "45 phút + 30 giây/nước",
        },
        # Câu 3: BXH Bảng B (Tử thần) + Elo trung bình 4 bảng đấu
        "3": {
            "type": "grouped_race",
            "credit": "VNEXPRESS / ĐIỂM ĐỌC DATA",
            "kicker": "BẢNG TỬ THẦN • CẬP NHẬT SAU NGÀY MỞ MÀN",
            "title": "XẾP HẠNG BẢNG B & ELO TRUNG BÌNH 4 BẢNG",
            "legend": [
                {"label": "Nhóm dẫn đầu (4đ / Cao nhất)", "color": COLOR_CYAN},
                {"label": "Nhóm giữa (2đ)", "color": COLOR_AMBER},
                {"label": "Nhóm cuối (1đ)", "color": COLOR_ROSE},
            ],
            "sections": [
                {
                    "label": "BẢNG XẾP HẠNG BẢNG B (SAU 2 VÁN)",
                    "sub": "Top 4 mỗi bảng vào vòng loại trực tiếp",
                    "max_axis": 5,
                    "ticks": [0, 1, 2, 3, 4, 5],
                    "unit": " đ",
                    "rows": [
                        {
                            "name": "Fabiano Caruana",
                            "sub": "Mỹ • Hạng 1 (chớp)",
                            "flag": "US",
                            "avatar": AV_CARUANA,
                            "color": COLOR_CYAN,
                            "value": 4,
                            "leader": True,
                        },
                        {
                            "name": "Lê Quang Liêm",
                            "sub": "Việt Nam • Đồng dẫn đầu",
                            "flag": "VN",
                            "avatar": AV_QL,
                            "color": COLOR_CYAN,
                            "value": 4,
                            "delta": "Hạng 2",
                            "leader": True,
                        },
                        {
                            "name": "Praggnanandhaa",
                            "sub": "Ấn Độ • 2 ván hòa",
                            "flag": "IN",
                            "avatar": AV_PRAG,
                            "color": COLOR_AMBER,
                            "value": 2,
                        },
                        {
                            "name": "Vincent Keymer",
                            "sub": "Đức • 2 ván hòa",
                            "flag": "DE",
                            "avatar": AV_KEYMER,
                            "color": COLOR_AMBER,
                            "value": 2,
                        },
                        {
                            "name": "V. Artemiev",
                            "sub": "FIDE • 1 hòa, 1 thua",
                            "flag": "FIDE",
                            "avatar": AV_ARTEMIEV,
                            "color": COLOR_ROSE,
                            "value": 1,
                        },
                        {
                            "name": "Richard Rapport",
                            "sub": "Hungary • 1 hòa, 1 thua",
                            "flag": "HU",
                            "avatar": AV_RAPPORT,
                            "color": COLOR_ROSE,
                            "value": 1,
                        },
                    ],
                },
                {
                    "label": "ELO TRUNG BÌNH CÁC BẢNG ĐẤU",
                    "sub": "Bảng B có 5 kỳ thủ Top 25 toàn năng",
                    "max_axis": 3000,
                    "ticks": [0, 1000, 2000, 3000],
                    "unit": "",
                    "rows": [
                        {
                            "name": "Bảng B (Quang Liêm)",
                            "sub": "Elo trung bình cao nhất",
                            "color": COLOR_CYAN,
                            "value": 2735,
                            "delta": "+84 vs Bảng D",
                            "leader": True,
                        },
                        {
                            "name": "Bảng A & Bảng C",
                            "sub": "Carlsen, Firouzja, Giri",
                            "color": COLOR_AMBER,
                            "value": 2719,
                        },
                        {
                            "name": "Bảng D",
                            "sub": "Vachier-Lagrave dẫn đầu",
                            "color": COLOR_ROSE,
                            "value": 2651,
                        },
                    ],
                },
            ],
            "foot_left": "Nguồn: VnExpress • Total Chess Budapest 2026",
            "foot_right": "24 kỳ thủ • 13 quốc gia",
        },
    }


NEWS_DATA_12_11_P3: List[Dict[str, Any]] = [
    {
        "id": 4,
        "slug": "Short_My_Dot_Ngot_Rut_Khoi_U17_World_Cup_2026",
        "voice_preset": "primary",  # Giọng Nam: Minh Quân Pro (Mẫu 15)
        "group": "WORLD CUP U17",
        "title": "Mỹ đột ngột rút khỏi U17 World Cup 2026 vì lo ngại xung đột Trung Đông",
        "summary": (
            "Ngày 11 tháng 11, Liên đoàn Bóng đá Mỹ bất ngờ quyết định rút đội U17 nam khỏi giải World Cup 2026 diễn ra từ ngày 19 tháng 11 đến 13 tháng 12 tại Qatar. "
            "Thông báo hủy tập huấn được đưa ra chỉ năm ngày sau khi HLV Alex Aldaz chốt 21 cầu thủ, viện dẫn cảnh báo du lịch cấp độ 3 của Bộ Ngoại giao Mỹ trước nguy cơ an ninh Trung Đông. "
            "Trước giải đấu này, bất ổn khu vực cũng buộc WTA Finals rời Arab Saudi và hủy các chặng Công thức 1 ở Jeddah lẫn Bahrain, trong khi đội bỏ giải muộn có thể bị FIFA phạt ít nhất 20000 franc Thụy Sĩ. "
            "Sự vắng mặt của Mỹ đặt FIFA vào thế khó khi tìm phương án giữ đủ 48 đội ở 12 bảng, đồng thời có thể gián tiếp tác động tới cách xét vé đi tiếp cho các đội thứ ba. "
            "Về phía Việt Nam, thầy trò HLV Cristiano Roland là đại diện duy nhất của Đông Nam Á lần đầu góp mặt, nằm tại bảng G rất nặng ký cùng Bỉ, New Zealand và Mali. "
            "Theo lịch thi đấu từ ngày 20 đến 26 tháng 11, U17 Việt Nam sẽ lần lượt chạm trán Bỉ, New Zealand và cựu á quân Mali trên cụm sân Học viện Aspire tại Doha."
        ),
        "source": "VnExpress",
        "news_source": "VnExpress",
        "credit": "VNEXPRESS / AFP",
        "hide_date_chip": True,
        "seo_title": "Mỹ đột ngột rút khỏi U17 World Cup 2026 vì lo ngại xung đột #Shorts",
        "description": [
            "Liên đoàn Bóng đá Mỹ (US Soccer) bất ngờ thông báo rút đội U17 nam khỏi VCK U17 World Cup 2026 tại Qatar (diễn ra từ 19/11 đến 13/12) do lo ngại an ninh khu vực Trung Đông.",
            "Quyết định đưa ra chỉ 5 ngày sau khi HLV Alex Aldaz công bố danh sách 21 tuyển thủ. Theo quy định của FIFA, đội bỏ giải trong vòng 30 ngày trước khai mạc có thể đối diện án phạt tối thiểu 20.000 franc Thụy Sĩ.",
            "Dù lịch đấu bảng G của U17 Việt Nam (thầy trò HLV Cristiano Roland gặp Bỉ 20/11, New Zealand 23/11 và Mali 26/11 tại Doha) không thay đổi trực tiếp, FIFA sẽ phải cân nhắc phương án thay thế hoặc điều chỉnh cách tính điểm cho các đội hạng ba.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#U17WorldCup2026", "#U17VietNam", "#USSoccer",
            "#Qatar2026", "#CristianoRoland", "#BongDaTheGioi",
        ],
        "thumb": {
            "image": "Tin_04_1.jpg",
            "badge": "WORLD CUP U17",
            "kicker": "BIẾN ĐỘNG TRƯỚC GIỜ G • QATAR 2026",
            "hero_html": 'MỸ ĐỘT NGỘT RÚT KHỎI <span class="hl">U17 WORLD CUP</span>',
            "subtitle": "Hủy kế hoạch sát ngày khai mạc vì an ninh Trung Đông; bảng G của U17 Việt Nam chờ động thái từ FIFA",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "12.11.2026",
            "obj_pos": "center 28%",
        },
        "images": [
            # Title (0)
            {"dest": "Tin_04_1.jpg", "src": "candidates/art1_u17_1.jpg", "credit": "VNEXPRESS / AFP", "desc": "Tuyển U17 Mỹ ăn mừng tấm vé dự FIFA U17 World Cup 2026"},
            {"dest": "Tin_04_2.jpg", "src": "candidates/wm_doha_2.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Toàn cảnh thành phố Doha, Qatar đăng cai U17 World Cup 2026"},
            # Câu 1: US Soccer rút U17 Mỹ khỏi giải 19/11 - 13/12 tại Qatar
            {"dest": "Tin_04_3.jpg", "src": "candidates/wm_usmnt_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Đội tuyển bóng đá Mỹ đứng đội hình trước trận đấu"},
            {"dest": "Tin_04_4.jpg", "src": "candidates/wm_aspire_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Khu liên hợp thể thao Aspire ở Doha, nơi diễn ra phần lớn 104 trận đấu"},
            # Câu 2: Bộ Ngoại giao Mỹ cảnh báo cấp độ 3 sau 5 ngày chốt 21 cầu thủ
            {"dest": "Tin_04_5.jpg", "src": "candidates/wm_state_dept_2.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Biển hiệu Bộ Ngoại giao Mỹ"},
            {"dest": "Tin_04_6.jpg", "src": "candidates/wm_state_dept_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Trụ sở Bộ Ngoại giao Mỹ tại Washington"},
            # Câu 3: Xung đột Trung Đông ảnh hưởng WTA, F1 & án phạt FIFA 20000 franc
            {"dest": "Tin_04_7.jpg", "src": "candidates/wm_doha_3.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Đường chân trời Doha bên vịnh Ba Tư"},
            {"dest": "Tin_04_8.jpg", "src": "candidates/wm_fifa_2.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Trụ sở Liên đoàn Bóng đá Thế giới FIFA tại Zurich"},
            # Câu 4: Giải pháp 48 đội, 12 bảng đấu và vé đội hạng ba
            {"dest": "Tin_04_9.jpg", "src": "candidates/wm_ahmad_ali_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Sân vận động Ahmad bin Ali, địa điểm tổ chức trận chung kết ngày 13/12"},
            {"dest": "Tin_04_10.jpg", "src": "candidates/vne_wta_f1_4.jpg", "credit": "VNEXPRESS", "desc": "Bảng chia 12 bảng đấu của 48 đội tại FIFA U17 World Cup Qatar 2026"},
            # Câu 5: U17 Việt Nam & HLV Cristiano Roland tại bảng G cùng Bỉ, New Zealand, Mali
            {"dest": "Tin_04_11.jpg", "src": "candidates/vne_wta_f1_2.jpg", "credit": "VNEXPRESS", "desc": "HLV trưởng Cristiano Roland chỉ đạo trên sân tập U17 Việt Nam"},
            {"dest": "Tin_04_12.jpg", "src": "candidates/vne_vn17_3.jpg", "credit": "VNEXPRESS", "desc": "Các cầu thủ U17 Việt Nam ăn mừng tại giải U17 châu Á 2026"},
            # Câu 6: Lịch đấu Bỉ 20/11, New Zealand 23/11, Mali 26/11 trên cụm sân Aspire
            {"dest": "Tin_04_13.jpg", "src": "candidates/vne_vn17_1.jpg", "credit": "VNEXPRESS", "desc": "Niềm vui chiến thắng của các tuyển thủ U17 Việt Nam"},
            {"dest": "Tin_04_14.jpg", "src": "candidates/vne_vn17_4.jpg", "credit": "VNEXPRESS", "desc": "Pha đi bóng tranh chấp của cầu thủ U17 Việt Nam"},
        ],
        "plan_slots": [
            ("title", 0, "Tin_04_1.jpg"),
            ("title", 0, "Tin_04_2.jpg"),
            ("sentence", 1, "Tin_04_3.jpg"),
            ("sentence", 1, "Tin_04_4.jpg"),
            ("sentence", 2, "Tin_04_5.jpg"),
            ("sentence", 2, "Tin_04_6.jpg"),
            ("sentence", 3, "Tin_04_7.jpg"),
            ("sentence", 3, "Tin_04_8.jpg"),
            ("sentence", 4, "Tin_04_9.jpg"),
            ("sentence", 4, "Tin_04_10.jpg"),
            ("sentence", 5, "Tin_04_11.jpg"),
            ("sentence", 5, "Tin_04_12.jpg"),
            ("sentence", 6, "Tin_04_13.jpg"),
            ("sentence", 6, "Tin_04_14.jpg"),
        ],
    },
    {
        "id": 5,
        "slug": "Short_Le_Quang_Liem_Thang_Van_Co_Chinh_Xac_99_Phan_Tram",
        "voice_preset": "secondary",  # Giọng Nữ: Ngọc Huyền (Mẫu 14)
        "group": "CỜ VUA THẾ GIỚI",
        "title": "Quang Liêm thắng ván cờ có độ chính xác 99% tại Giải toàn năng thế giới",
        "summary": (
            "Ngày 11 tháng 11 tại Budapest, siêu đại kiện tướng Lê Quang Liêm khởi đầu ấn tượng ở bảng B giải cờ vua toàn năng thế giới 2026 sau màn so tài kịch tính với Vladislav Artemiev. "
            "Hòa ván lượt đi bằng quân đen, Quang Liêm chuyển sang cầm quân trắng chơi khai cuộc Catalan và tung nước thí mã xuất sắc ở nước 22, qua đó thắng sau 32 nước với độ chính xác đạt 99%. "
            "Thu về bốn điểm sau hai lượt trận, kỳ thủ số một Việt Nam cùng Fabiano Caruana chia sẻ hai vị trí dẫn đầu bảng B tử thần, nơi sở hữu Elo trung bình 2735 cao nhất giải. "
            "Cùng ngày tại bảng C, vua cờ Magnus Carlsen bất ngờ bị Anish Giri cầm hòa cả hai ván, trong khi giải đấu thử nghiệm của FIDE và Norway Chess có tổng quỹ thưởng lên tới 650000 USD. "
            "Vào lúc 21 giờ tối nay 12 tháng 11 theo giờ Hà Nội, Lê Quang Liêm sẽ bước vào hai lượt trận tiếp theo chạm trán siêu đại kiện tướng Đức Vincent Keymer."
        ),
        "source": "VnExpress",
        "news_source": "VnExpress",
        "credit": "VNEXPRESS / TOTAL CHESS",
        "hide_date_chip": True,
        "seo_title": "Quang Liêm thắng ván cờ có độ chính xác 99% tại Budapest #Shorts",
        "description": [
            "Siêu đại kiện tướng Lê Quang Liêm khởi đầu như mơ tại giải cờ vua toàn năng thế giới (Total Chess World Championship) 2026 ở Budapest, Hungary ngày 11/11.",
            "Sau trận hòa bằng quân đen ở lượt đi, Quang Liêm cầm quân trắng chọn khai cuộc Catalan, tung nước thí mã tuyệt đẹp ở nước 22 và đánh bại Vladislav Artemiev ở nước 32 với tỷ lệ nước đi chính xác lên tới 99% (so với 85% của đối thủ).",
            "Với 4 điểm sau ngày mở màn, Quang Liêm đồng dẫn đầu bảng B 'tử thần' (Elo trung bình 2735) cùng Fabiano Caruana và sẽ tiếp tục chạm trán Vincent Keymer lúc 21h tối 12/11 (giờ Hà Nội).",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#LeQuangLiem", "#CoVuaVietNam", "#TotalChess2026",
            "#Budapest", "#FIDE", "#FabianoCaruana", "#MagnusCarlsen",
        ],
        "thumb": {
            "image": "Tin_05_2.jpg",
            "badge": "CỜ VUA THẾ GIỚI",
            "kicker": "BUDAPEST 2026 • ĐỒ HỌA PHÂN TÍCH",
            "hero_html": 'VÁN CỜ <span class="hl">CHÍNH XÁC 99%</span><br>CỦA LÊ QUANG LIÊM',
            "subtitle": "Thí mã tuyệt đẹp hạ Artemiev, thu 4 điểm đồng dẫn đầu bảng B tử thần cùng Fabiano Caruana",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "12.11.2026",
            "obj_pos": "center 18%",
        },
        "sentence_charts": _charts_quang_liem(),
        "images": [
            # Title (0)
            {"dest": "Tin_05_1.jpg", "src": "candidates/art2_ql_1.jpg", "credit": "VNEXPRESS / TOTAL CHESS", "desc": "Lê Quang Liêm đối đầu Vladislav Artemiev tại Total Chess Budapest 2026"},
            {"dest": "Tin_05_2.jpg", "src": "candidates/vne_ql_more_1.jpg", "credit": "VNEXPRESS", "desc": "Siêu đại kiện tướng Lê Quang Liêm rạng rỡ cùng tấm huy chương vàng"},
            # Câu 1: Khởi đầu Budapest với Vladislav Artemiev
            {"dest": "Tin_05_3.jpg", "src": "candidates/wm_budapest_chess_3.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Toàn cảnh hội trường thi đấu cờ vua quốc tế tại Budapest, Hungary"},
            {"dest": "Tin_05_4.jpg", "src": "candidates/art2_ql_1.jpg", "credit": "VNEXPRESS / TOTAL CHESS", "desc": "Quang Liêm và Artemiev tập trung cao độ trong ngày khai màn 11/11"},
            # Câu 2 (nền mờ dưới Chart 1): Nước thí mã !! (art2_ql_2) & Artemiev
            {"dest": "Tin_05_5.jpg", "src": "candidates/art2_ql_2.jpg", "credit": "VNEXPRESS", "desc": "Nước thí mã thiên tài ở nước 22 giúp Quang Liêm đạt 99% chính xác"},
            {"dest": "Tin_05_6.jpg", "src": "candidates/wm_artemiev_2.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Siêu đại kiện tướng Vladislav Artemiev"},
            # Câu 3 (nền mờ dưới Chart 2): Caruana & Praggnanandhaa ở Bảng B tử thần
            {"dest": "Tin_05_7.jpg", "src": "candidates/wm_caruana_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Siêu đại kiện tướng Mỹ Fabiano Caruana"},
            {"dest": "Tin_05_8.jpg", "src": "candidates/wm_prag_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Kỳ thủ Ấn Độ R Praggnanandhaa"},
            # Câu 4: Magnus Carlsen hòa Anish Giri & FIDE x Norway Chess 650000 USD
            {"dest": "Tin_05_9.jpg", "src": "candidates/wm_carlsen_giri_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Magnus Carlsen bắt tay Anish Giri bên bàn cờ"},
            {"dest": "Tin_05_10.jpg", "src": "candidates/wm_fide_2.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Magnus Carlsen tại giải đấu thuộc hệ thống FIDE"},
            # Câu 5: 21h tối nay 12/11 gặp Vincent Keymer & Richard Rapport / Quang Liêm
            {"dest": "Tin_05_11.jpg", "src": "candidates/wm_keymer_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Siêu đại kiện tướng Đức Vincent Keymer, đối thủ tối 12/11"},
            {"dest": "Tin_05_12.jpg", "src": "candidates/art2_ql_2.jpg", "credit": "VNEXPRESS", "desc": "Thế trận áp đảo của Quang Liêm trong ván thắng lượt về"},
        ],
        "plan_slots": [
            ("title", 0, "Tin_05_1.jpg"),
            ("title", 0, "Tin_05_2.jpg"),
            ("sentence", 1, "Tin_05_3.jpg"),
            ("sentence", 1, "Tin_05_4.jpg"),
            ("sentence", 2, "Tin_05_5.jpg"),
            ("sentence", 2, "Tin_05_6.jpg"),
            ("sentence", 3, "Tin_05_7.jpg"),
            ("sentence", 3, "Tin_05_8.jpg"),
            ("sentence", 4, "Tin_05_9.jpg"),
            ("sentence", 4, "Tin_05_10.jpg"),
            ("sentence", 5, "Tin_05_11.jpg"),
            ("sentence", 5, "Tin_05_12.jpg"),
        ],
    },
]


def main() -> None:
    run_short_batch(
        ctx=CTX,
        items=NEWS_DATA_12_11_P3,
        title_banner="SẢN XUẤT 2 VIDEO SHORTS TIN #04 & TIN #05 NGÀY 12.11.2026 (MỸ RÚT U17 WC & LÊ QUANG LIÊM 99%)",
    )


if __name__ == "__main__":
    main()
