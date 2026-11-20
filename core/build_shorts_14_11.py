#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng 3 Video Shorts 9:16 độc lập ngày 14.11.2026 tại outputs/Orther/14.11.2026/shorts/:
  - Tin #01 (Giọng Nam — Minh Quân Pro Mẫu 15):
    Thủ môn Jesus Owono bị phạt kịch khung treo giò 12 trận sau pha va chạm khiến tiền đạo Jesus de Miguel qua đời.
    Áp dụng Memorial Grayscale cho ảnh tưởng niệm & tang lễ, Opening Hook HUD 12 trận & 5 SFX đồng bộ, kèm Outro 9:16.
  - Tin #02 (Giọng Nam — Minh Quân Pro Mẫu 15):
    Hà Lan hủy diệt Hy Lạp 7-0 ở UEFA Nations League, Reijnders lập hat-trick trong 21 phút hiệp một.
    Tích hợp Opening Hook HUD 7-0, đồ thị DataViz thống kê áp đảo Hà Lan vs Hy Lạp & Outro 9:16.
  - Tin #03 (Giọng Nam — Minh Quân Pro Mẫu 15):
    Kỳ thủ 18 tuổi Phan Huy Hoàng bất bại đoạt HCV cá nhân Giải cờ tướng thế giới mở rộng 2026 tại Singapore.
    Tích hợp Opening Hook HUD 13 điểm bất bại, đồ thị DataViz bảng tổng sắp Việt Nam vs Trung Quốc & Outro 9:16.

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
    day_dir=Path(paths.ROOT) / "outputs" / "Orther" / "14.11.2026",
    inspect_dir=Path.home() / "Library" / "Caches" / "DiemDoc" / "candidates_14_11",
    work_tag="14_11",
)

COLOR_CYAN = "#00E5FF"
COLOR_GOLD = "#F59E0B"
COLOR_ROSE = "#EF4444"


def _charts_ha_lan() -> Dict[str, Any]:
    """Đồ thị Cyber-Stadium DataViz thống kê áp đảo Hà Lan 7-0 Hy Lạp (UEFA Nations League)."""
    return {
        "3": {
            "type": "grouped_race",
            "credit": "365SCORES / UEFA STATS",
            "kicker": "UEFA NATIONS LEAGUE • BẢNG A2 • AMSTERDAM",
            "title": "THỐNG KÊ ÁP ĐẢO: HÀ LAN 7-0 HY LẠP",
            "legend": [
                {"label": "Hà Lan (HLV Xavi)", "color": COLOR_CYAN},
                {"label": "Hy Lạp", "color": COLOR_ROSE},
            ],
            "sections": [
                {
                    "label": "CƠ HỘI & HIỆU SUẤT DỨT ĐIỂM",
                    "sub": "Thống kê 90 phút tại Johan Cruijff Arena",
                    "max_axis": 20,
                    "ticks": [0, 5, 10, 15, 20],
                    "unit": "",
                    "rows": [
                        {
                            "name": "Tổng cú sút (Hà Lan)",
                            "sub": "xG 4,39 • 7 bàn thắng",
                            "flag": "NL",
                            "color": COLOR_CYAN,
                            "value": 17,
                            "delta": "vs 9 cú sút",
                            "leader": True,
                        },
                        {
                            "name": "Sút trúng đích (Hà Lan)",
                            "sub": "Hiệu suất dứt điểm hủy diệt",
                            "flag": "NL",
                            "color": COLOR_GOLD,
                            "value": 13,
                            "delta": "vs 1 của Hy Lạp",
                            "leader": True,
                        },
                        {
                            "name": "Tổng cú sút (Hy Lạp)",
                            "sub": "xG 0,44 • Chỉ 1 lần trúng đích",
                            "flag": "GR",
                            "color": COLOR_ROSE,
                            "value": 9,
                        },
                    ],
                },
                {
                    "label": "KIỂM SOÁT BÓNG",
                    "sub": "Thế trận chủ động của Cơn lốc màu da cam",
                    "max_axis": 100,
                    "ticks": [0, 25, 50, 75, 100],
                    "unit": "%",
                    "rows": [
                        {
                            "name": "Hà Lan",
                            "sub": "Dẫn 5-0 ngay trong hiệp một",
                            "flag": "NL",
                            "color": COLOR_CYAN,
                            "value": 53,
                            "delta": "+6%",
                            "leader": True,
                        },
                        {
                            "name": "Hy Lạp",
                            "sub": "Đứt mạch bất bại 4 lượt đầu",
                            "flag": "GR",
                            "color": COLOR_ROSE,
                            "value": 47,
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Thắng kỷ lục", "value": "7-0"},
                {"label": "Hat-trick Reijnders", "value": "21 phút"},
                {"label": "Dẫn đầu bảng A2", "value": "11 điểm"},
            ],
            "foot_left": "Nguồn: 365Scores • VnExpress • Goal",
            "foot_right": "Chung kết bảng A2 vs Đức ngày 16/11",
        }
    }


def _charts_co_tuong() -> Dict[str, Any]:
    """Đồ thị Cyber-Stadium DataViz bảng điểm Đồng đội Nam & Nữ Giải cờ tướng thế giới mở rộng 2026."""
    return {
        "4": {
            "type": "grouped_race",
            "credit": "LIÊN ĐOÀN CỜ TƯỚNG VN",
            "kicker": "WORLD XIANGQI OPEN 2026 • SINGAPORE",
            "title": "BẢNG TỔNG SẮP ĐỒNG ĐỘI NAM & NỮ",
            "legend": [
                {"label": "Việt Nam (2 HCB đồng đội)", "color": COLOR_CYAN},
                {"label": "Trung Quốc (HCV đồng đội)", "color": COLOR_ROSE},
            ],
            "sections": [
                {
                    "label": "NỘI DUNG ĐỒNG ĐỘI NAM (ĐIỂM TRẬN)",
                    "sub": "Phan Huy Hoàng xuất sắc giành HCV cá nhân 13 điểm",
                    "max_axis": 16,
                    "ticks": [0, 4, 8, 12, 16],
                    "unit": " đ",
                    "rows": [
                        {
                            "name": "Trung Quốc",
                            "sub": "Hạng Nhất đồng đội nam",
                            "flag": "CN",
                            "color": COLOR_ROSE,
                            "value": 13,
                            "delta": "HCV đồng đội",
                            "leader": True,
                        },
                        {
                            "name": "Việt Nam",
                            "sub": "Huy Hoàng • Nhật Quang • Khai Nguyên",
                            "flag": "VN",
                            "color": COLOR_CYAN,
                            "value": 11,
                            "delta": "HCB đồng đội",
                            "leader": True,
                        },
                        {
                            "name": "Hong Kong",
                            "sub": "Hạng Ba đồng đội nam",
                            "flag": "HK",
                            "color": COLOR_GOLD,
                            "value": 10,
                        },
                    ],
                },
                {
                    "label": "NỘI DUNG ĐỒNG ĐỘI NỮ (ĐIỂM TRẬN)",
                    "sub": "Thùy Dung giành HCĐ cá nhân, Hoàng Yến hạng 5",
                    "max_axis": 16,
                    "ticks": [0, 4, 8, 12, 16],
                    "unit": " đ",
                    "rows": [
                        {
                            "name": "Trung Quốc",
                            "sub": "Hạng Nhất đồng đội nữ",
                            "flag": "CN",
                            "color": COLOR_ROSE,
                            "value": 14,
                            "delta": "HCV đồng đội",
                            "leader": True,
                        },
                        {
                            "name": "Việt Nam",
                            "sub": "Thùy Dung • Hoàng Yến",
                            "flag": "VN",
                            "color": COLOR_CYAN,
                            "value": 12,
                            "delta": "HCB đồng đội",
                            "leader": True,
                        },
                        {
                            "name": "Malaysia",
                            "sub": "Hạng Ba đồng đội nữ",
                            "flag": "MY",
                            "color": COLOR_GOLD,
                            "value": 9,
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Phan Huy Hoàng", "value": "13 điểm (HCV)"},
                {"label": "Minh Nhật Quang", "value": "12 điểm (HCĐ)"},
                {"label": "Thành tích đoàn", "value": "2 HCB đồng đội"},
            ],
            "foot_left": "Nguồn: VnExpress • Tuổi Trẻ • Bongdaplus",
            "foot_right": "Bất bại 7 vòng tại Singapore 13/11",
        }
    }


NEWS_DATA_14_11: List[Dict[str, Any]] = [
    {
        "id": 1,
        "slug": "Short_Thu_Mon_Owono_Bi_Phat_Kich_Khung_12_Tran_Vu_De_Miguel",
        "voice_preset": "primary",
        "group": "LA LIGA 2 • TÂY BAN NHA",
        "title": "Thủ môn gây cái chết cho De Miguel bị phạt kịch khung",
        "summary": (
            "Ngày 13 tháng 11, Liên đoàn Bóng đá Tây Ban Nha chính thức công bố án phạt kịch khung treo giò 12 trận đối với thủ môn Jesus Owono của CLB Andorra. "
            "Căn cứ Điều 102 Quy định Kỷ luật, pha lao ra khỏi vòng cấm dùng lực quá mức ở phút bù giờ trận gặp Tenerife ngày 2 tháng 11 đã khiến tiền đạo 30 tuổi Jesus de Miguel ngừng tim ngay trên sân và qua đời sáng hôm sau. "
            "Cảnh sát Tây Ban Nha đã mở cuộc điều tra tư pháp bắt buộc với ca tử vong không tự nhiên, dù cơ quan công tố nhận định khả năng truy tố hình sự không cao. "
            "Theo báo Marca, thủ môn Owono đang rơi vào cú sốc tâm lý nặng nề, chưa thể trở lại tập luyện và mong muốn được gửi lời xin lỗi trực tiếp tới gia đình đồng nghiệp xấu số. "
            "Trong khi đó, chiến dịch quyên góp do tiền đạo Fran Sol khởi xướng đã trao 239000 USD hỗ trợ thân nhân, còn CLB Tenerife cam kết bảo trợ con gái 16 tháng tuổi của De Miguel đến năm 18 tuổi."
        ),
        "source": "VnExpress / Marca, AS & RFEF",
        "news_source": "VNEXPRESS / MARCA & AS",
        "credit": "DIARIO DE AVISOS / REUTERS / MARCA",
        "hide_date_chip": True,
        "seo_title": "Thủ môn Owono bị phạt kịch khung 12 trận sau bi kịch qua đời của De Miguel #Shorts",
        "description": [
            "Ngày 13/11/2026, Ủy ban Kỷ luật Liên đoàn Bóng đá Tây Ban Nha (RFEF) chính thức tuyên án treo giò kịch khung 12 trận theo Điều 102 đối với thủ môn Jesus Owono (CLB Andorra) sau pha va chạm khiến tiền đạo Jesus de Miguel (CLB Tenerife) ngừng tim trên sân và qua đời ở tuổi 30.",
            "Cảnh sát Tây Ban Nha đã mở cuộc điều tra tư pháp theo quy định với các ca tử vong không tự nhiên, dù khả năng truy tố hình sự được đánh giá không cao. Hiện Owono đang chịu sang chấn tâm lý nặng và được CLB hỗ trợ y tế.",
            "Hiệp hội Cầu thủ Tây Ban Nha (AFE) cùng chiến dịch của tiền đạo Fran Sol đã quyên góp khoảng 239000 USD giúp đỡ gia đình nạn nhân, trong khi Tenerife cam kết chăm lo cho con gái 16 tháng tuổi Carla của De Miguel tới khi trưởng thành.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#JesusDeMiguel", "#JesusOwono", "#LaLiga2",
            "#Tenerife", "#Andorra", "#BongDaTayBanNha",
        ],
        "hook": {
            "kicker": "ÁN PHẠT KỊCH KHUNG • ĐIỀU 102 RFEF",
            "vs_badge": "ANDORRA vs TENERIFE",
            "stat_val": 12,
            "stat_unit": "TRẬN",
            "stat_label": "MỨC TREO GIÒ TỐI ĐA",
            "stat_sub": "SAU BI KỊCH KHIẾN TIỀN ĐẠO JESUS DE MIGUEL QUA ĐỜI Ở TUỔI 30",
            "opp_val": 0,
            "count_dur": 0.70,
            "pills": [
                {"text": "ĐIỀU 102 KỶ LUẬT", "style": "cyan", "delay": 1.15},
                {"text": "ĐIỀU TRA TƯ PHÁP", "style": "gold", "delay": 1.85},
                {"text": "239000 USD SẺ CHIA", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        "thumb": {
            "image": "s1_collision_1.jpg",
            "badge": "BÓNG ĐÁ TÂY BAN NHA",
            "kicker": "BI KỊCH LA LIGA 2 • RFEF",
            "hero_html": 'PHẠT KỊCH KHUNG <span class="hl">TREO GIÒ 12 TRẬN</span>',
            "subtitle": "Thủ môn Owono nhận án nặng nhất sau va chạm khiến tiền đạo De Miguel tử vong",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "14.11.2026",
            "obj_pos": "center 20%",
        },
        "images": [
            # Title (0) — 3 nhịp mở màn
            {"dest": "s1_collision_1.jpg", "src": "t1_vne_1.jpg", "credit": "DIARIO DE AVISOS", "desc": "Khoảnh khắc va chạm giữa Owono và Jesus de Miguel ngày 2/11"},
            {"dest": "s1_rfef_hq.jpg", "src": "t1_ddg_11.jpg", "credit": "MARCA", "desc": "Trụ sở Liên đoàn Bóng đá Tây Ban Nha RFEF"},
            {"dest": "s1_demiguel_bw1.jpg", "src": "t1_ddg_06.jpg", "credit": "CD TENERIFE", "desc": "Tưởng niệm tiền đạo Jesus de Miguel (ảnh đen trắng)"},
            # Câu 1: RFEF công bố án phạt kịch khung 12 trận đối với Owono
            {"dest": "s1_rfef_ball.jpg", "src": "t1_ddg_10.jpg", "credit": "ANTENA 3", "desc": "Ủy ban Kỷ luật RFEF ra án treo giò tối đa 12 trận"},
            {"dest": "s1_owono_andorra.jpg", "src": "t1_ddg_01.jpg", "credit": "FC ANDORRA", "desc": "Thủ môn Jesus Owono trong màu áo CLB Andorra"},
            # Câu 2: Điều 102, pha lao ra ở phút bù giờ trận gặp Tenerife ngày 2/11
            {"dest": "s1_collision_2.jpg", "src": "t1_vne_2.jpg", "credit": "DIARIO DE AVISOS", "desc": "Tình huống dùng lực quá mức khiến De Miguel ngừng tim"},
            {"dest": "s1_demiguel_bw2.jpg", "src": "t1_ex_03_bw.jpg", "credit": "PRENSA IBÉRICA", "desc": "Tiền đạo Jesus de Miguel qua đời ở tuổi 30 (ảnh tưởng niệm)"},
            # Câu 3: Cảnh sát Tây Ban Nha mở điều tra tư pháp, khả năng truy tố không cao
            {"dest": "s1_tenerife_stadium.jpg", "src": "t1_ddg_07.jpg", "credit": "ESPAÑA ESTADIOS", "desc": "Sân Heliodoro Rodríguez López nơi xảy ra bi kịch"},
            {"dest": "s1_funeral_bw.jpg", "src": "t1_vne_3_bw.jpg", "credit": "REUTERS", "desc": "Gia đình và người thân tiễn biệt De Miguel tại Navahermosa"},
            # Câu 4: Owono sốc tâm lý nặng, chưa tập luyện, muốn xin lỗi gia đình
            {"dest": "s1_owono_kneel.jpg", "src": "t1_ddg_03.jpg", "credit": "CAF ONLINE", "desc": "Jesus Owono đối mặt cú sốc tinh thần nặng nề"},
            {"dest": "s1_andorra_stadium.jpg", "src": "t1_ddg_14.jpg", "credit": "FC ANDORRA", "desc": "CLB Andorra trở lại chuẩn bị thi đấu tại Almeria"},
            # Câu 5: Quyên góp 239000 USD qua Fran Sol, Tenerife bảo trợ con gái 16 tháng tuổi
            {"dest": "s1_fran_sol.jpg", "src": "t1_ex_02.jpg", "credit": "MÁLAGA CF", "desc": "Tiền đạo Fran Sol khởi xướng chiến dịch quyên góp 239000 USD"},
            {"dest": "s1_memorial_flowers_bw.jpg", "src": "t1_ddg_05_bw.jpg", "credit": "NOGOMANIA", "desc": "CĐV đặt hoa tưởng niệm tiền đạo Jesus de Miguel"},
        ],
        "plan_slots": [
            ("title", 0, "s1_collision_1.jpg"),
            ("title", 0, "s1_rfef_hq.jpg"),
            ("title", 0, "s1_demiguel_bw1.jpg"),
            ("sentence", 1, "s1_rfef_ball.jpg"),
            ("sentence", 1, "s1_owono_andorra.jpg"),
            ("sentence", 2, "s1_collision_2.jpg"),
            ("sentence", 2, "s1_demiguel_bw2.jpg"),
            ("sentence", 3, "s1_tenerife_stadium.jpg"),
            ("sentence", 3, "s1_funeral_bw.jpg"),
            ("sentence", 4, "s1_owono_kneel.jpg"),
            ("sentence", 4, "s1_andorra_stadium.jpg"),
            ("sentence", 5, "s1_fran_sol.jpg"),
            ("sentence", 5, "s1_memorial_flowers_bw.jpg"),
        ],
    },
    {
        "id": 2,
        "slug": "Short_Ha_Lan_Huy_Diet_Hy_Lap_7_0_Reijnders_Hat_Trick",
        "voice_preset": "primary",
        "group": "UEFA NATIONS LEAGUE",
        "title": "Hà Lan hủy diệt Hy Lạp 7-0 ở Nations League",
        "summary": (
            "Tại lượt áp chót bảng A2 UEFA Nations League ở Amsterdam, đội tuyển Hà Lan của HLV Xavi Hernandez đã tạo nên cơn mưa bàn thắng hủy diệt Hy Lạp 7-0. "
            "Ngay sau pha mở tỷ số phút thứ sáu của Crysencio Summerville, tiền vệ Tijjani Reijnders bùng nổ lập cú hat-trick chỉ trong 21 phút hiệp một, tái lập kỳ tích của huyền thoại Marco van Basten năm 1990. "
            "Hậu vệ Jurrien Timber tiếp tục tỏa sáng với một cú đúp cùng bàn ấn định của Donyell Malen, giúp Cơn lốc màu da cam tung ra 17 cú sút với 13 lần trúng đích và san bằng kỷ lục thắng đậm nhất lịch sử giải đấu. "
            "HLV Xavi ca ngợi tinh thần tập luyện của học trò nhưng nhắc toàn đội giữ sự tập trung cho trận quyết đấu gặp đội tuyển Đức của Jurgen Klopp vào ngày 16 tháng 11. "
            "Thắng lợi này giúp Hà Lan dẫn đầu bảng A2 với 11 điểm, hơn Đức và Hy Lạp ba điểm trước lượt trận cuối."
        ),
        "source": "VnExpress / Goal, 365Scores & Reuters",
        "news_source": "VNEXPRESS / GOAL & REUTERS",
        "credit": "REUTERS / AP / UEFA",
        "hide_date_chip": True,
        "seo_title": "Hà Lan thắng hủy diệt Hy Lạp 7-0, Reijnders lập hat-trick 21 phút ở Nations League #Shorts",
        "description": [
            "Rạng sáng 14/11/2026 tại sân Johan Cruijff Arena (Amsterdam), đội tuyển Hà Lan dưới sự dẫn dắt của HLV Xavi Hernandez thắng tưng bừng Hy Lạp 7-0 ở lượt trận thứ 5 bảng A2 UEFA Nations League.",
            "Crysencio Summerville mở tỷ số phút thứ 6, trước khi Tijjani Reijnders ghi liền 3 bàn trong 21 phút hiệp một (12', 18', 33') — trở thành cầu thủ Hà Lan đầu tiên lập hat-trick ngay hiệp một kể từ Marco van Basten năm 1990. Jurrien Timber lập cú đúp (40', 59') và Donyell Malen ấn định chiến thắng phút 61.",
            "Kết quả 7-0 giúp Hà Lan san bằng kỷ lục thắng cách biệt lớn nhất lịch sử Nations League và giữ vững ngôi đầu bảng A2 với 11 điểm, hơn Đức (thắng Serbia 3-1) và Hy Lạp 3 điểm trước đại chiến lượt cuối ngày 16/11.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#HaLan", "#Netherlands", "#NationsLeague",
            "#Reijnders", "#XaviHernandez", "#BongDaChauAu",
        ],
        "hook": {
            "kicker": "CƠN ĐỊA CHẤN AMSTERDAM • NATIONS LEAGUE",
            "vs_badge": "HÀ LAN vs HY LẠP",
            "stat_val": 7,
            "stat_unit": "- 0",
            "stat_label": "SAN BẰNG KỶ LỤC LỊCH SỬ GIẢI ĐẤU",
            "stat_sub": "REIJNDERS HAT-TRICK TRONG 21 PHÚT • HÀ LAN DẪN ĐẦU BẢNG A2",
            "opp_val": 0,
            "count_dur": 0.65,
            "pills": [
                {"text": "REIJNDERS 21 PHÚT", "style": "cyan", "delay": 1.15},
                {"text": "TIMBER CÚ ĐÚP", "style": "gold", "delay": 1.85},
                {"text": "11 ĐIỂM ĐẦU BẢNG", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        "sentence_charts": _charts_ha_lan(),
        "thumb": {
            "image": "s2_reijnders_ball.jpg",
            "badge": "UEFA NATIONS LEAGUE",
            "kicker": "BẢNG A2 • JOHAN CRUIJFF ARENA",
            "hero_html": 'HÀ LAN HỦY DIỆT HY LẠP <span class="hl">TỶ SỐ 7-0</span>',
            "subtitle": "Reijnders lập hat-trick sau 21 phút; san bằng kỷ lục thắng đậm nhất lịch sử giải",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "14.11.2026",
            "obj_pos": "center 20%",
        },
        "images": [
            # Title (0)
            {"dest": "s2_reijnders_ball.jpg", "src": "t2_vne_3.jpg", "credit": "REUTERS", "desc": "Tijjani Reijnders cầm bóng kỷ niệm cú hat-trick trước Hy Lạp"},
            {"dest": "s2_oranje_greece.jpg", "src": "t2_vne_2.jpg", "credit": "REUTERS", "desc": "Các cầu thủ Hà Lan ăn mừng chiến thắng 7-0 trước Hy Lạp"},
            {"dest": "s2_cruijff_arena.jpg", "src": "t2_ex_05.jpg", "credit": "NORDIC STADIUMS", "desc": "Khán đài rực lửa tại sân Johan Cruijff Arena"},
            # Câu 1: Amsterdam, HLV Xavi Hernandez, hủy diệt Hy Lạp 7-0
            {"dest": "s2_xavi_coach.jpg", "src": "t2_ddg_05.jpg", "credit": "GIVEMESPORT", "desc": "HLV Xavi Hernandez chỉ đạo chiến thuật cho tuyển Hà Lan"},
            {"dest": "s2_pavlidis_sad.jpg", "src": "t2_vne_1.jpg", "credit": "REUTERS", "desc": "Hy Lạp thảm bại 0-7 ngay tại Amsterdam"},
            # Câu 2: Summerville mở tỷ số, Reijnders hat-trick 21 phút (như Van Basten 1990)
            {"dest": "s2_summerville.jpg", "src": "t2_ddg_04.jpg", "credit": "INT INSIGHT", "desc": "Crysencio Summerville mở tỷ số phút thứ 6"},
            {"dest": "s2_reijnders_cel.jpg", "src": "t2_ex_04.jpg", "credit": "GIVEMESPORT", "desc": "Tijjani Reijnders bùng nổ với cú hat-trick trong 21 phút"},
            # Câu 3 (có DataViz): Jurrien Timber cú đúp, Donyell Malen, 17 cú sút 13 trúng đích
            {"dest": "s2_timber.jpg", "src": "t2_timber_clean_01.jpg", "credit": "CAUGHTOFFSIDE", "desc": "Hậu vệ Jurrien Timber lập cú đúp bàn thắng"},
            {"dest": "s2_malen.jpg", "src": "t2_ex_02.jpg", "credit": "THE NATIONAL HERALD", "desc": "Donyell Malen ghi 1 bàn và đóng góp 2 kiến tạo"},
            # Câu 4: Xavi nhắc tập trung trước trận gặp Đức của Jurgen Klopp ngày 16/11
            {"dest": "s2_xavi_press.jpg", "src": "t2_ddg_07.jpg", "credit": "DIARIO AS", "desc": "Xavi nhắc học trò tập trung tối đa cho lượt cuối"},
            {"dest": "s2_klopp_germany.jpg", "src": "t2_vne_4.jpg", "credit": "AP PHOTO", "desc": "HLV Jurgen Klopp cùng tuyển Đức thắng Serbia 3-1"},
            # Câu 5: Hà Lan dẫn đầu bảng A2 với 11 điểm, hơn Đức & Hy Lạp 3 điểm
            {"dest": "s2_reijnders_orange.jpg", "src": "t2_ex_03.jpg", "credit": "SOCCERNEWS NL", "desc": "Hà Lan dẫn đầu bảng A2 với 11 điểm trọn vẹn thế chủ động"},
            {"dest": "s2_dumfries.jpg", "src": "t2_ddg_14.jpg", "credit": "SEMPREINTER", "desc": "Denzel Dumfries góp sức giúp Hà Lan tiến sát tứ kết"},
        ],
        "plan_slots": [
            ("title", 0, "s2_reijnders_ball.jpg"),
            ("title", 0, "s2_oranje_greece.jpg"),
            ("title", 0, "s2_cruijff_arena.jpg"),
            ("sentence", 1, "s2_xavi_coach.jpg"),
            ("sentence", 1, "s2_pavlidis_sad.jpg"),
            ("sentence", 2, "s2_summerville.jpg"),
            ("sentence", 2, "s2_reijnders_cel.jpg"),
            ("sentence", 3, "s2_timber.jpg"),
            ("sentence", 3, "s2_malen.jpg"),
            ("sentence", 4, "s2_xavi_press.jpg"),
            ("sentence", 4, "s2_klopp_germany.jpg"),
            ("sentence", 5, "s2_reijnders_orange.jpg"),
            ("sentence", 5, "s2_dumfries.jpg"),
        ],
    },
    {
        "id": 3,
        "slug": "Short_Phan_Huy_Hoang_Doat_HCV_Co_Tuong_The_Gioi_2026",
        "voice_preset": "primary",
        "group": "CỜ TƯỚNG THẾ GIỚI",
        "title": "Kỳ thủ Việt Nam đoạt HCV cờ tướng thế giới 2026",
        "summary": (
            "Tại Giải cờ tướng thế giới mở rộng 2026 vừa khép lại ở Singapore, kỳ thủ 18 tuổi Phan Huy Hoàng xuất sắc tạo địa chấn khi đoạt HCV cá nhân nội dung đồng đội nam. "
            "Được tin tưởng trao suất đánh chính thay đương kim vô địch thế giới Lại Lý Huynh, tài năng trẻ đến từ Thành phố Hồ Chí Minh thi đấu thăng hoa với thành tích bất bại 6 thắng, 1 hòa, đạt 13 điểm. "
            "Đáng chú ý, Huy Hoàng đã cầm hậu thủ hòa nhà vô địch châu Á Lưu Bách Hoành và xếp trên cả ba cao thủ Trung Quốc gồm Như Nhất Thuần, Mạnh Phồn Duệ lẫn Bách Hoành. "
            "Chung cuộc, đồng đội Nguyễn Minh Nhật Quang giành HCĐ cá nhân, giúp tuyển nam Việt Nam đoạt HCB đồng đội, trong khi tuyển nữ cũng mang về tấm HCB nhờ công Đàm Thị Thùy Dung và Nguyễn Hoàng Yến. "
            "Đây là cột mốc khẳng định sức bật mạnh mẽ của thế hệ kế cận cờ tướng Việt Nam trên đấu trường quốc tế."
        ),
        "source": "VnExpress / Tuổi Trẻ & Bongdaplus",
        "news_source": "VNEXPRESS / TUỔI TRẺ",
        "credit": "LIÊN ĐOÀN CỜ TƯỚNG VN / THANH NIÊN",
        "hide_date_chip": True,
        "seo_title": "Kỳ thủ 18 tuổi Phan Huy Hoàng đoạt HCV cá nhân Giải cờ tướng thế giới 2026 #Shorts",
        "description": [
            "Tại Giải cờ tướng thế giới mở rộng lần thứ 5 năm 2026 tại Singapore (13/11), kỳ thủ trẻ 18 tuổi Phan Huy Hoàng (TP.HCM) xuất sắc giành HCV cá nhân nội dung đồng đội nam với thành tích bất bại 13 điểm (6 thắng, 1 hòa sau 7 vòng).",
            "Thay thế đàn anh Lại Lý Huynh tập trung cho nội dung cờ nhanh, Phan Huy Hoàng đã cầm hòa nhà vô địch châu Á Lưu Bách Hoành ở vòng 3 và vượt mặt dàn siêu sao Trung Quốc gồm Như Nhất Thuần (12đ, HCB), Mạnh Phồn Duệ (hạng 4) và Lưu Bách Hoành (hạng 5).",
            "Ngoài HCV của Huy Hoàng, kỳ thủ Nguyễn Minh Nhật Quang giành HCĐ cá nhân (12đ), giúp tuyển nam và tuyển nữ Việt Nam (Đàm Thị Thùy Dung, Nguyễn Hoàng Yến) cùng mang về 2 tấm HCB đồng đội đầy tự hào.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#PhanHuyHoang", "#CoTuongVietNam", "#WorldXiangqiOpen",
            "#LaiLyHuynh", "#MinhNhatQuang", "#TheThaoVietNam",
        ],
        "hook": {
            "kicker": "ĐỊA CHẤN CỜ TƯỚNG • SINGAPORE 2026",
            "vs_badge": "VIỆT NAM vs TRUNG QUỐC",
            "stat_val": 13,
            "stat_unit": "ĐIỂM",
            "stat_label": "BẤT BẠI 7 VÒNG • 6 THẮNG 1 HÒA",
            "stat_sub": "PHAN HUY HOÀNG 18 TUỔI VƯỢT DÀN SIÊU SAO TRUNG QUỐC ĐOẠT HCV",
            "opp_val": 12,
            "count_dur": 0.70,
            "pills": [
                {"text": "TUỔI 18 BẤT BẠI", "style": "cyan", "delay": 1.15},
                {"text": "VƯỢT SAO TRUNG QUỐC", "style": "gold", "delay": 1.85},
                {"text": "HCV CÁ NHÂN THẾ GIỚI", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        "sentence_charts": _charts_co_tuong(),
        "thumb": {
            "image": "s3_hoang_podium.jpg",
            "badge": "CỜ TƯỚNG THẾ GIỚI",
            "kicker": "WORLD XIANGQI OPEN 2026 • SINGAPORE",
            "hero_html": 'KỲ THỦ 18 TUỔI ĐOẠT <span class="hl">HCV THẾ GIỚI</span>',
            "subtitle": "Phan Huy Hoàng bất bại 13 điểm, vượt mặt dàn siêu sao Trung Quốc tại Singapore",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "14.11.2026",
            "obj_pos": "center 18%",
        },
        "images": [
            # Title (0)
            {"dest": "s3_hoang_podium.jpg", "src": "t3_vne_2.jpg", "credit": "LIÊN ĐOÀN CỜ TƯỚNG VN", "desc": "Phan Huy Hoàng và Nguyễn Minh Nhật Quang nhận huy chương tại Singapore"},
            {"dest": "s3_hoang_flag.jpg", "src": "t3_ex_hoang_crop.jpg", "credit": "LIÊN ĐOÀN CỜ TƯỚNG VN", "desc": "Kỳ thủ 18 tuổi Phan Huy Hoàng giương cao cờ Tổ quốc cùng HCV"},
            {"dest": "s3_xiangqi_boards.jpg", "src": "t3_ddg_17.jpg", "credit": "BÁO HẢI DƯƠNG", "desc": "Không khí tranh tài căng thẳng trên bàn cờ tướng"},
            # Câu 1: Giải cờ tướng thế giới mở rộng 2026 tại Singapore, Phan Huy Hoàng 18 tuổi HCV
            {"dest": "s3_podium_wide.jpg", "src": "t3_vne_1.jpg", "credit": "LIÊN ĐOÀN CỜ TƯỚNG VN", "desc": "Bục trao giải nội dung đồng đội nam tại Singapore 13/11"},
            {"dest": "s3_hoang_solo.jpg", "src": "t3_ex_hoang_crop.jpg", "credit": "LIÊN ĐOÀN CỜ TƯỚNG VN", "desc": "Phan Huy Hoàng đạt 13 điểm để giành HCV cá nhân"},
            # Câu 2: Thay thế Lại Lý Huynh, 6 thắng 1 hòa 13 điểm
            {"dest": "s3_lailyhuynh_1.jpg", "src": "t3_ddg_06.jpg", "credit": "TUỔI TRẺ", "desc": "Đương kim vô địch thế giới Lại Lý Huynh tập trung nội dung cờ nhanh"},
            {"dest": "s3_lailyhuynh_2.jpg", "src": "t3_ddg_04.jpg", "credit": "NHÂN DÂN", "desc": "Lại Lý Huynh tại giải thế giới"},
            # Câu 3: Thủ hòa Lưu Bách Hoành, vượt Như Nhất Thuần & Mạnh Phồn Duệ
            {"dest": "s3_luubachhoanh_1.jpg", "src": "t3_ddg_10.jpg", "credit": "WEBCOTUONG", "desc": "Nhà vô địch châu Á Lưu Bách Hoành của Trung Quốc"},
            {"dest": "s3_luubachhoanh_2.jpg", "src": "t3_ddg_11.jpg", "credit": "WEBCOTUONG", "desc": "Cuộc đấu trí đỉnh cao giữa các cao thủ hàng đầu châu Á"},
            # Câu 4 (có DataViz): Minh Nhật Quang HCĐ, Đàm Thị Thùy Dung & Hoàng Yến HCB nữ
            {"dest": "s3_nhatquang.jpg", "src": "t3_ddg_07.jpg", "credit": "THANH NIÊN", "desc": "Nguyễn Minh Nhật Quang giành HCĐ cá nhân với 12 điểm"},
            {"dest": "s3_thuydung.jpg", "src": "t3_ex_05.jpg", "credit": "NGƯỜI LAO ĐỘNG", "desc": "Kỳ thủ Đàm Thị Thùy Dung góp công vào HCB đồng đội nữ"},
            # Câu 5: Khẳng định sức bật thế hệ kế cận cờ tướng Việt Nam
            {"dest": "s3_hoangyen_podium.jpg", "src": "t3_ex_06.jpg", "credit": "NGƯỜI LAO ĐỘNG", "desc": "Nguyễn Hoàng Yến và Đàm Thị Thùy Dung trên bục nhận giải"},
            {"dest": "s3_lailyhuynh_match.jpg", "src": "t3_ddg_05.jpg", "credit": "VOV", "desc": "Cờ tướng Việt Nam khẳng định vị thế trên đấu trường quốc tế"},
        ],
        "plan_slots": [
            ("title", 0, "s3_hoang_podium.jpg"),
            ("title", 0, "s3_hoang_flag.jpg"),
            ("title", 0, "s3_xiangqi_boards.jpg"),
            ("sentence", 1, "s3_podium_wide.jpg"),
            ("sentence", 1, "s3_hoang_solo.jpg"),
            ("sentence", 2, "s3_lailyhuynh_1.jpg"),
            ("sentence", 2, "s3_lailyhuynh_2.jpg"),
            ("sentence", 3, "s3_luubachhoanh_1.jpg"),
            ("sentence", 3, "s3_luubachhoanh_2.jpg"),
            ("sentence", 4, "s3_nhatquang.jpg"),
            ("sentence", 4, "s3_thuydung.jpg"),
            ("sentence", 5, "s3_hoangyen_podium.jpg"),
            ("sentence", 5, "s3_lailyhuynh_match.jpg"),
        ],
    },
]


def main() -> None:
    run_short_batch(
        CTX,
        NEWS_DATA_14_11,
        "XUẤT BẢN 3 VIDEO SHORTS 9:16 NGÀY 14.11.2026 (GIỌNG NAM + HOOK + DATAVIZ + OUTRO)",
    )


if __name__ == "__main__":
    main()
