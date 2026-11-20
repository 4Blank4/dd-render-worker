#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng 2 Video Shorts 9:16 độc lập ngày 13.11.2026 tại outputs/Orther/13.11.2026/shorts/:
  - Tin #01 (Giọng Nam — Minh Quân Pro Mẫu 15):
    Pochettino đồng ý dẫn dắt Man Utd tới năm 2029 & làn sóng chỉ trích vụ sa thải Michael Carrick.
    Tích hợp Opening Hook kích thích 3s đầu (10 triệu USD phí giải phóng hợp đồng) & đồ thị DataViz tỷ lệ thắng các đời HLV Man Utd hậu Alex Ferguson.
  - Tin #02 (Giọng Nữ — Ngọc Huyền Mẫu 14):
    U23 Việt Nam áp đảo toàn diện hạ U23 Singapore 1-0 tại giải Gia Lai VTV Cup 2026 sân Pleiku & HLV Kassim khen ngợi.
    Tích hợp Opening Hook kích thích 3s đầu (70% kiểm soát bóng, 14 cú sút) & đồ thị DataViz thống kê áp đảo tuyệt đối U23 Việt Nam vs U23 Singapore.

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
    day_dir=Path(paths.ROOT) / "outputs" / "Orther" / "13.11.2026",
    inspect_dir=Path.home() / "Library" / "Caches" / "DiemDoc" / "candidates_13_11",
    work_tag="13_11",
)

COLOR_CYAN = "#00E5FF"
COLOR_GOLD = "#F59E0B"
COLOR_ROSE = "#EF4444"


def _charts_pochettino() -> Dict[str, Any]:
    """Đồ thị Cyber-Stadium DataViz phân tích tỷ lệ chiến thắng các đời HLV Man Utd hậu Sir Alex."""
    return {
        "2": {
            "type": "grouped_race",
            "credit": "THE ATHLETIC / STATS PERFORM",
            "kicker": "KỶ NGUYÊN HẬU ALEX FERGUSON • 2013-2026",
            "title": "TỶ LỆ THẮNG CỦA CÁC ĐỜI HLV MAN UTD",
            "legend": [
                {"label": "Tỷ lệ thắng cao (>50%)", "color": COLOR_CYAN},
                {"label": "HLV vừa bị sa thải", "color": COLOR_ROSE},
            ],
            "sections": [
                {
                    "label": "TỶ LỆ THẮNG TRẬN CHÍNH THỨC",
                    "sub": "Thống kê mọi đấu trường thời hậu Sir Alex Ferguson",
                    "max_axis": 70,
                    "ticks": [0, 20, 40, 60],
                    "unit": "%",
                    "rows": [
                        {
                            "name": "Jose Mourinho",
                            "sub": "144 trận • 3 danh hiệu",
                            "flag": "PT",
                            "color": COLOR_CYAN,
                            "value": 58,
                            "delta": "Cao nhất",
                            "leader": True,
                        },
                        {
                            "name": "Erik ten Hag",
                            "sub": "128 trận • 2 cúp quốc nội",
                            "flag": "NL",
                            "color": COLOR_CYAN,
                            "value": 55,
                        },
                        {
                            "name": "Ole Solskjaer",
                            "sub": "168 trận • Á quân C2",
                            "flag": "NO",
                            "color": COLOR_CYAN,
                            "value": 54,
                        },
                        {
                            "name": "Michael Carrick",
                            "sub": "32 trận • Vừa bị sa thải",
                            "flag": "GB",
                            "color": COLOR_ROSE,
                            "value": 47,
                            "delta": "Bị sa thải",
                            "leader": True,
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Phí bồi thường", "value": "10 triệu USD"},
                {"label": "Hợp đồng mới", "value": "Hè 2029"},
                {"label": "Tâm thư sa thải", "value": "142 từ"},
            ],
            "foot_left": "Nguồn: The Athletic • BBC Sport",
            "foot_right": "Pochettino tiếp quản từ 22/11",
        }
    }


def _charts_u23_vietnam() -> Dict[str, Any]:
    """Đồ thị Cyber-Stadium DataViz phân tích thế trận áp đảo tuyệt đối U23 Việt Nam vs U23 Singapore."""
    return {
        "3": {
            "type": "grouped_race",
            "credit": "VNEXPRESS / VFF STATS",
            "kicker": "GIA LAI VTV CUP 2026 • SÂN PLEIKU",
            "title": "THỐNG KÊ ÁP ĐẢO: U23 VIỆT NAM VS SINGAPORE",
            "legend": [
                {"label": "U23 Việt Nam", "color": COLOR_CYAN},
                {"label": "U23 Singapore", "color": COLOR_ROSE},
            ],
            "sections": [
                {
                    "label": "TỶ LỆ KIỂM SOÁT BÓNG",
                    "sub": "Áp đảo toàn diện suốt 90 phút thi đấu",
                    "max_axis": 100,
                    "ticks": [0, 25, 50, 75, 100],
                    "unit": "%",
                    "rows": [
                        {
                            "name": "U23 Việt Nam",
                            "sub": "Thầy trò Đinh Hồng Vinh",
                            "flag": "VN",
                            "color": COLOR_CYAN,
                            "value": 70,
                            "delta": "+40% kiểm soát",
                            "leader": True,
                        },
                        {
                            "name": "U23 Singapore",
                            "sub": "HLV Firdaus Kassim",
                            "flag": "SG",
                            "color": COLOR_ROSE,
                            "value": 30,
                        },
                    ],
                },
                {
                    "label": "CƠ HỘI HÃM THÀNH NGUY HIỂM",
                    "sub": "Tổng số cú dứt điểm & phạt góc",
                    "max_axis": 16,
                    "ticks": [0, 4, 8, 12, 16],
                    "unit": "",
                    "rows": [
                        {
                            "name": "Dứt điểm (U23 VN)",
                            "sub": "14 pha hãm thành",
                            "flag": "VN",
                            "color": COLOR_CYAN,
                            "value": 14,
                            "delta": "vs 0 cú sút",
                            "leader": True,
                        },
                        {
                            "name": "Phạt góc (U23 VN)",
                            "sub": "12 quả phạt góc",
                            "flag": "VN",
                            "color": COLOR_GOLD,
                            "value": 12,
                            "delta": "vs 0 phạt góc",
                            "leader": True,
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Bàn thắng phút 70", "value": "1-0"},
                {"label": "Nguyễn Bảo Long", "value": "Đánh gót"},
                {"label": "Dẫn đầu bảng", "value": "6 điểm"},
            ],
            "foot_left": "Nguồn: VnExpress • VFF",
            "foot_right": "Chung kết tranh 100000 USD vs Qatar",
        }
    }


NEWS_DATA_13_11: List[Dict[str, Any]] = [
    {
        "id": 1,
        "slug": "Short_Pochettino_Dan_Dat_Man_Utd_Carrick_Bi_Chi_Trich",
        "voice_preset": "primary",  # Giọng Nam: Minh Quân Pro (Mẫu 15)
        "group": "MANCHESTER UNITED",
        "title": "Pochettino đồng ý dẫn dắt Man Utd tới năm 2029",
        "summary": (
            "Huấn luyện viên Mauricio Pochettino đã đạt thỏa thuận dẫn dắt Manchester United với bản hợp đồng hai năm rưỡi đến hè năm 2029. "
            "Để có được chữ ký của chiến lược gia người Argentina, Quỷ đỏ chấp nhận bồi thường 10 triệu USD cho Liên đoàn Bóng đá Mỹ, đưa tổng mức chi phí thương vụ vượt mốc 16 triệu USD. "
            "Pochettino sẽ hoàn tất hai lượt trận tứ kết gặp Haiti vào ngày 14 và ngày 17 tháng 11, trước khi chính thức ra mắt đội bóng mới ở trận đại chiến với Liverpool tại Anfield. "
            "Trong khi đó, quyết định sa thải Michael Carrick lại vấp phải làn sóng chỉ trích dữ dội từ giới chuyên môn và người hâm mộ. "
            "Cựu trung vệ Rio Ferdinand thẳng thừng gọi bức tâm thư chia tay vỏn vẹn 142 từ là sản phẩm vô cảm do trí tuệ nhân tạo soạn thảo, khi ban lãnh đạo để lộ tin cho truyền thông ngay lúc Carrick đang chỉ đạo buổi tập tại Carrington."
        ),
        "source": "VnExpress / The Athletic & BBC Sport",
        "news_source": "VNEXPRESS / THE ATHLETIC",
        "credit": "REUTERS / GETTY IMAGES",
        "hide_date_chip": True,
        "seo_title": "Pochettino đồng ý dẫn dắt Man Utd tới năm 2029, Carrick bị sa thải #Shorts",
        "description": [
            "Huấn luyện viên Mauricio Pochettino chính thức đạt thỏa thuận dẫn dắt Manchester United với bản hợp đồng hai năm rưỡi đến hè năm 2029. Quỷ đỏ chấp nhận chi trả khoản phí giải phóng 10 triệu USD cho Liên đoàn Bóng đá Mỹ (US Soccer).",
            "Chiến lược gia người Argentina sẽ hoàn tất 2 lượt trận Concacaf Nations League gặp Haiti vào ngày 14 và 17/11, trước khi chính thức ra mắt Man Utd trong chuyến làm khách gặp kình địch Liverpool tại Anfield vào ngày 22/11.",
            "Trong khi đó, việc ban lãnh đạo sa thải Michael Carrick bằng thông báo vỏn vẹn 142 từ bị cựu danh thủ Rio Ferdinand và giới chuyên môn chỉ trích dữ dội vì thiếu sự tôn trọng.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#Pochettino", "#ManUtd", "#Carrick",
            "#MUFC", "#PremierLeague", "#BongDaQuocTe",
        ],
        "hook": {
            "kicker": "THƯƠNG VỤ BOM TẤN",
            "vs_badge": "MAN UTD vs US SOCCER",
            "stat_val": 10,
            "stat_unit": "TRIỆU USD",
            "stat_label": "PHÍ GIẢI PHÓNG HỢP ĐỒNG",
            "stat_sub": "POCHETTINO CHÍNH THỨC CẬP BẾN OLD TRAFFORD ĐẾN NĂM 2029",
            "opp_val": 0,
            "count_dur": 0.70,
            "pills": [
                {"text": "HÈ 2029", "style": "cyan", "delay": 1.15},
                {"text": "ANFIELD 22/11", "style": "gold", "delay": 1.85},
                {"text": "SA THẢI CARRICK", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        "sentence_charts": _charts_pochettino(),
        "thumb": {
            "image": "short_1_poch_main.jpg",
            "badge": "MANCHESTER UNITED",
            "kicker": "THƯƠNG VỤ BOM TẤN • OLD TRAFFORD",
            "hero_html": 'POCHETTINO DẪN DẮT <span class="hl">MAN UTD ĐẾN 2029</span>',
            "subtitle": "Chi 10 triệu USD bồi thường hợp đồng; chỉ trích dữ dội cách sa thải Michael Carrick",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "13.11.2026",
            "obj_pos": "center 22%",
        },
        "images": [
            # Title (0)
            {"dest": "short_1_poch_main.jpg", "src": "wm_poch_2026.jpg", "credit": "GETTY IMAGES", "desc": "Mauricio Pochettino ký hợp đồng dẫn dắt Man Utd"},
            {"dest": "short_1_poch_tactics.jpg", "src": "poch_0.jpg", "credit": "REUTERS", "desc": "Pochettino chỉ đạo chiến thuật trên sân"},
            {"dest": "short_1_old_trafford.jpg", "src": "old_trafford_exterior.jpg", "credit": "REUTERS", "desc": "Sân vận động Old Trafford"},
            # Câu 1: Đạt thỏa thuận 2.5 năm đến hè 2029
            {"dest": "short_1_poch_portrait.jpg", "src": "poch_1.jpg", "credit": "THE ATHLETIC", "desc": "Chân dung HLV Mauricio Pochettino"},
            {"dest": "short_1_ratcliffe.jpg", "src": "wm_ratcliffe.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Sir Jim Ratcliffe quyết định bổ nhiệm Pochettino"},
            # Câu 2: Chi 10 triệu USD đền bù US Soccer, tổng chi phí vượt 16 triệu USD
            {"dest": "short_1_poch_pitch.jpg", "src": "poch_2.jpg", "credit": "REUTERS", "desc": "Pochettino trong màu áo tuyển Mỹ"},
            {"dest": "short_1_ot_2.jpg", "src": "old_trafford_exterior.jpg", "credit": "REUTERS", "desc": "Old Trafford chuẩn bị đón tân thuyền trưởng"},
            # Câu 3: Hoàn tất 2 trận Haiti, ra mắt gặp Liverpool tại Anfield
            {"dest": "short_1_poch_match.jpg", "src": "wm_poch_2026.jpg", "credit": "GETTY IMAGES", "desc": "Pochettino hoàn tất 2 trận gặp Haiti"},
            {"dest": "short_1_poch_prep.jpg", "src": "poch_0.jpg", "credit": "REUTERS", "desc": "Pochettino chuẩn bị cho đại chiến với Liverpool"},
            # Câu 4: Sa thải Michael Carrick vấp phải làn sóng chỉ trích gay gắt
            {"dest": "short_1_carrick_0.jpg", "src": "carrick_0.jpg", "credit": "REUTERS", "desc": "Michael Carrick bị sa thải sau 32 trận"},
            {"dest": "short_1_carrick_coaching.jpg", "src": "wm_carrick_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Carrick trên sân tập Carrington"},
            # Câu 5: Rio Ferdinand chỉ trích bức thư 142 từ do ChatGPT viết
            {"dest": "short_1_rio_ferdinand.jpg", "src": "wm_ferdinand_1.jpg", "credit": "WIKIMEDIA COMMONS", "desc": "Rio Ferdinand chỉ trích ban lãnh đạo Man Utd"},
            {"dest": "short_1_carrick_sad.jpg", "src": "carrick_1.jpg", "credit": "REUTERS", "desc": "Michael Carrick rời Carrington"},
        ],
        "plan_slots": [
            ("title", 0, "short_1_poch_main.jpg"),
            ("title", 0, "short_1_poch_tactics.jpg"),
            ("title", 0, "short_1_old_trafford.jpg"),
            ("sentence", 1, "short_1_poch_portrait.jpg"),
            ("sentence", 1, "short_1_ratcliffe.jpg"),
            ("sentence", 2, "short_1_poch_pitch.jpg"),
            ("sentence", 2, "short_1_ot_2.jpg"),
            ("sentence", 3, "short_1_poch_match.jpg"),
            ("sentence", 3, "short_1_poch_prep.jpg"),
            ("sentence", 4, "short_1_carrick_0.jpg"),
            ("sentence", 4, "short_1_carrick_coaching.jpg"),
            ("sentence", 5, "short_1_rio_ferdinand.jpg"),
            ("sentence", 5, "short_1_carrick_sad.jpg"),
        ],
    },
    {
        "id": 2,
        "slug": "Short_U23_Viet_Nam_Ha_Singapore_HLV_Kassim_Khen_Ngoi",
        "voice_preset": "secondary",  # Giọng Nữ: Ngọc Huyền (Mẫu 14)
        "group": "U23 VIỆT NAM",
        "title": "U23 Việt Nam áp đảo hạ Singapore tại Pleiku",
        "summary": (
            "Tại giải giao hữu quốc tế Gia Lai VTV Cup 2026, U23 Việt Nam tiếp tục thể hiện phong độ ấn tượng khi đánh bại U23 Singapore với tỷ số một không trên sân vận động Pleiku. "
            "Khoảnh khắc bùng nổ diễn ra ở phút 70, xuất phát từ quả căng ngang chuẩn xác của Nguyễn Quốc Việt, hậu vệ Nguyễn Bảo Long đã có pha giật gót điệu nghệ làm tung lưới đối phương. "
            "Đoàn quân áo đỏ áp đảo toàn diện với 70% thời lượng kiểm soát bóng, tung ra 14 cú dứt điểm và 12 quả phạt góc, không để đối thủ tạo ra bất kỳ pha bắn phá nguy hiểm nào. "
            "Phát biểu sau trận đấu, huấn luyện viên trưởng Singapore Firdaus Kassim hết lời ca ngợi và khẳng định U23 Việt Nam hoàn toàn đủ năng lực cạnh tranh chức vô địch U23 châu Á. "
            "Toàn thắng hai trận với hiệu số dương bốn, thầy trò huấn luyện viên Đinh Hồng Vinh vững vàng ngôi đầu bảng trước cuộc quyết đấu tranh cúp 100000 USD với U23 Qatar."
        ),
        "source": "VnExpress / VFF & Thanh Niên",
        "news_source": "VNEXPRESS / VFF",
        "credit": "VNEXPRESS / VFF / BAOMOI",
        "hide_date_chip": True,
        "seo_title": "U23 Việt Nam áp đảo hạ Singapore tại Pleiku, HLV Kassim khen ngợi #Shorts",
        "description": [
            "Tại giải giao hữu quốc tế Gia Lai VTV Cup 2026 trên sân Pleiku chiều 12/11, U23 Việt Nam giành thắng lợi 1-0 trước U23 Singapore nhờ pha giật gót ngẫu hứng của hậu vệ Nguyễn Bảo Long ở phút 70 sau quả căng ngang của Nguyễn Quốc Việt.",
            "Thầy trò HLV Đinh Hồng Vinh thể hiện sự áp đảo tuyệt đối với 70% kiểm soát bóng, tung ra 14 cú dứt điểm và 12 quả phạt góc, trong khi đối thủ không có pha dứt điểm trúng đích nào.",
            "HLV trưởng Singapore Firdaus Kassim hết lời ca ngợi và khẳng định U23 Việt Nam đủ sức vô địch U23 châu Á. Thắng trận này, U23 Việt Nam dẫn đầu bảng với 6 điểm trọn vẹn trước trận tranh ngôi vương 100000 USD gặp U23 Qatar.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#U23VietNam", "#GiaLaiVTVCup", "#BaoLong",
            "#DinhHongVinh", "#BongDaVietNam", "#U23Singapore",
        ],
        "hook": {
            "kicker": "ÁP ĐẢO TUYỆT ĐỐI",
            "vs_badge": "U23 VN 1-0 SINGAPORE",
            "stat_val": 70,
            "stat_unit": "%",
            "stat_label": "TỶ LỆ KIỂM SOÁT BÓNG",
            "stat_sub": "14 CÚ DỨT ĐIỂM • HẠ GỤC SINGAPORE BẰNG SIÊU PHẨM ĐÁNH GÓT",
            "opp_val": 30,
            "count_dur": 0.70,
            "pills": [
                {"text": "BẢO LONG 70'", "style": "cyan", "delay": 1.15},
                {"text": "14 CÚ SÚT - 0", "style": "gold", "delay": 1.85},
                {"text": "6 ĐIỂM DẪN ĐẦU", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        "sentence_charts": _charts_u23_vietnam(),
        "thumb": {
            "image": "short_2_baolong_goal.jpg",
            "badge": "U23 VIỆT NAM",
            "kicker": "GIA LAI VTV CUP • SÂN PLEIKU",
            "hero_html": 'U23 VIỆT NAM HẠ SINGAPORE <span class="hl">BẰNG SIÊU PHẨM</span>',
            "subtitle": "Bảo Long giật gót điệu nghệ phút 70; HLV Kassim khen ngợi đủ sức vô địch U23 châu Á",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "13.11.2026",
            "obj_pos": "center 25%",
        },
        "images": [
            # Title (0)
            {"dest": "short_2_baolong_goal.jpg", "src": "bao_long_celebrate.jpg", "credit": "VNEXPRESS", "desc": "Nguyễn Bảo Long ăn mừng bàn thắng vào lưới Singapore"},
            {"dest": "short_2_u23_celebrate.jpg", "src": "baomoi_u23_2.jpg", "credit": "BAOMOI", "desc": "U23 Việt Nam ăn mừng chiến thắng tại Pleiku"},
            {"dest": "short_2_u23_lineup.jpg", "src": "baomoi_u23_1.jpg", "credit": "BAOMOI", "desc": "Đội hình xuất phát U23 Việt Nam"},
            # Câu 1: Gia Lai VTV Cup 2026 trên sân Pleiku
            {"dest": "short_2_u23_speed.jpg", "src": "thailand_match_0.jpg", "credit": "VNEXPRESS", "desc": "U23 Việt Nam thi đấu tốc độ trên sân Pleiku"},
            {"dest": "short_2_hlv_vinh_side.jpg", "src": "hlv_vinh_2.jpg", "credit": "VOV", "desc": "HLV Đinh Hồng Vinh trên băng ghế chỉ đạo"},
            # Câu 2: Phút 70 Bảo Long lập siêu phẩm đánh gót từ đường chuyền Quốc Việt
            {"dest": "short_2_baolong_heel.jpg", "src": "bao_long_celebrate.jpg", "credit": "VNEXPRESS", "desc": "Nguyễn Bảo Long lập siêu phẩm đánh gót"},
            {"dest": "short_2_quocviet_assist.jpg", "src": "khoa_ngo_action.jpg", "credit": "VNEXPRESS", "desc": "Pha tấn công biên tạo nên bàn thắng"},
            # Câu 3: Áp đảo 70% kiểm soát bóng, 14 dứt điểm, 12 phạt góc
            {"dest": "short_2_u23_attack.jpg", "src": "thailand_match_1.jpg", "credit": "VNEXPRESS", "desc": "U23 Việt Nam kiểm soát bóng 70%"},
            {"dest": "short_2_u23_press.jpg", "src": "baomoi_u23_0.jpg", "credit": "BAOMOI", "desc": "Thế trận áp đảo toàn diện của U23 Việt Nam"},
            # Câu 4: HLV Firdaus Kassim khen ngợi U23 VN đủ sức vô địch U23 châu Á
            {"dest": "short_2_kassim_press.jpg", "src": "u23_kassim_0.jpg", "credit": "VNEXPRESS", "desc": "HLV Firdaus Kassim trong phòng họp báo"},
            {"dest": "short_2_kassim_coach.jpg", "src": "u23_kassim_1.jpg", "credit": "VNEXPRESS", "desc": "HLV Singapore thừa nhận U23 Việt Nam vượt trội"},
            # Câu 5: Toàn thắng 2 trận vững vàng ngôi đầu bảng trước đại chiến Qatar
            {"dest": "short_2_hlv_vinh_smile.jpg", "src": "hlv_vinh_4.jpg", "credit": "VOV", "desc": "HLV Đinh Hồng Vinh hài lòng với phong độ của học trò"},
            {"dest": "short_2_u23_win.jpg", "src": "baomoi_u23_2.jpg", "credit": "BAOMOI", "desc": "U23 Việt Nam dẫn đầu bảng với 6 điểm trọn vẹn"},
        ],
        "plan_slots": [
            ("title", 0, "short_2_baolong_goal.jpg"),
            ("title", 0, "short_2_u23_celebrate.jpg"),
            ("title", 0, "short_2_u23_lineup.jpg"),
            ("sentence", 1, "short_2_u23_speed.jpg"),
            ("sentence", 1, "short_2_hlv_vinh_side.jpg"),
            ("sentence", 2, "short_2_baolong_heel.jpg"),
            ("sentence", 2, "short_2_quocviet_assist.jpg"),
            ("sentence", 3, "short_2_u23_attack.jpg"),
            ("sentence", 3, "short_2_u23_press.jpg"),
            ("sentence", 4, "short_2_kassim_press.jpg"),
            ("sentence", 4, "short_2_kassim_coach.jpg"),
            ("sentence", 5, "short_2_hlv_vinh_smile.jpg"),
            ("sentence", 5, "short_2_u23_win.jpg"),
        ],
    },
]


def main() -> None:
    run_short_batch(
        ctx=CTX,
        items=NEWS_DATA_13_11,
        title_banner="SẢN XUẤT 2 VIDEO SHORTS TIN #01 & TIN #02 NGÀY 13.11.2026 (POCHETTINO MAN UTD & U23 VIỆT NAM)",
    )


if __name__ == "__main__":
    main()
