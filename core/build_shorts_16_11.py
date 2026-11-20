#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng tuần tự từng Video Short 9:16 dưới 2 phút ngày 16.11.2026 tại outputs/Orther/16.11.2026/shorts/:
  - Cấu trúc song giọng (Dual-Voice):
    + Đoạn đầu (Tiêu đề + Tường thuật trận đấu): Giọng Nữ (Ngọc Huyền Mẫu 14 - secondary)
    + Đoạn sau (Bình luận chuyên môn): Giọng Nam (Minh Quân Pro Mẫu 15 - primary)
  - Tích hợp Opening Hook HUD 3-5s đầu + 5 SFX, DataViz cờ quốc gia SVG, Thumbnail 9:16, Mô tả SEO & Outro 9:16.
  - Hỗ trợ chạy từng video riêng lẻ qua `--only 1|2|3`.
"""

import argparse
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
    day_dir=Path(paths.ROOT) / "outputs" / "Orther" / "16.11.2026",
    inspect_dir=Path.home() / "Library" / "Caches" / "DiemDoc" / "candidates_16_11",
    work_tag="16_11",
)

COLOR_CYAN = "#00E5FF"
COLOR_GOLD = "#F59E0B"
COLOR_ROSE = "#EF4444"


def _charts_argentina() -> Dict[str, Any]:
    """Đồ thị Cyber-Stadium DataViz phân tích nghịch lý cầm bóng 72% vẫn thua của Argentina."""
    return {
        "3": {
            "type": "grouped_race",
            "credit": "SKY SPORTS / FLASHSCORE",
            "kicker": "GIAO HỮU QUỐC TẾ • LA BOMBONERA 13/11",
            "title": "NGHỊCH LÝ THỐNG KÊ: ARGENTINA 1-2 URUGUAY",
            "legend": [
                {"label": "Argentina (HLV Scaloni)", "color": COLOR_CYAN},
                {"label": "Uruguay (HLV Diego Forlan)", "color": COLOR_ROSE},
            ],
            "sections": [
                {
                    "label": "TỶ LỆ KIỂM SOÁT BÓNG & CHUYỀN CHÍNH XÁC",
                    "sub": "Argentina cầm bóng vượt trội nhưng thiếu đột biến cuối sân",
                    "max_axis": 100,
                    "ticks": [0, 25, 50, 75, 100],
                    "unit": "%",
                    "rows": [
                        {
                            "name": "Kiểm soát bóng (ARG)",
                            "sub": "674 đường chuyền chuẩn (90,2%)",
                            "flag": "AR",
                            "color": COLOR_CYAN,
                            "value": 72,
                            "delta": "+44% cầm bóng",
                            "leader": True,
                        },
                        {
                            "name": "Kiểm soát bóng (URU)",
                            "sub": "220 đường chuyền (77,5%)",
                            "flag": "UY",
                            "color": COLOR_ROSE,
                            "value": 28,
                        },
                    ],
                },
                {
                    "label": "HIỆU SUẤT DỨT ĐIỂM",
                    "sub": "Uruguay chỉ sút 6 lần nhưng tận dụng tối đa cơ hội",
                    "max_axis": 20,
                    "ticks": [0, 5, 10, 15, 20],
                    "unit": "",
                    "rows": [
                        {
                            "name": "Tổng cú sút (ARG)",
                            "sub": "6 lần trúng đích • 1 bàn thắng",
                            "flag": "AR",
                            "color": COLOR_CYAN,
                            "value": 17,
                            "delta": "vs 6 của Uruguay",
                            "leader": True,
                        },
                        {
                            "name": "Tổng cú sút (URU)",
                            "sub": "3 lần trúng đích • Thắng 2-1",
                            "flag": "UY",
                            "color": COLOR_ROSE,
                            "value": 6,
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Tỷ số chung cuộc", "value": "1-2"},
                {"label": "Kiểm soát bóng", "value": "72%"},
                {"label": "Áo số 10 Messi", "value": "Bỏ trống"},
            ],
            "foot_left": "Nguồn: Sky Sports • BeIN Sports",
            "foot_right": "Trận giao hữu tiếp theo vs Costa Rica 17/11",
        }
    }


def _charts_italia() -> Dict[str, Any]:
    """Đồ thị Cyber-Stadium DataViz thống kê Bỉ 4-1 Italia (Bảng A1 UEFA Nations League)."""
    return {
        "3": {
            "type": "grouped_race",
            "credit": "SOFASCORE / FOOTYSTATS",
            "kicker": "UEFA NATIONS LEAGUE • BẢNG A1 • BRUSSELS",
            "title": "TOÀN CẢNH SỤP ĐỔ: BỈ 4-1 ITALIA",
            "legend": [
                {"label": "Bỉ (HLV Mark van Bommel)", "color": COLOR_ROSE},
                {"label": "Italia (HLV Roberto Mancini)", "color": COLOR_CYAN},
            ],
            "sections": [
                {
                    "label": "ÁP LỰC DỨT ĐIỂM TOÀN TRẬN",
                    "sub": "Hàng thủ Italia vỡ vụn trước 22 cú sút của Bỉ",
                    "max_axis": 25,
                    "ticks": [0, 5, 10, 15, 20, 25],
                    "unit": "",
                    "rows": [
                        {
                            "name": "Tổng cú sút (Bỉ)",
                            "sub": "10 trúng đích • xG 3,42 • 4 bàn thắng",
                            "flag": "BE",
                            "color": COLOR_ROSE,
                            "value": 22,
                            "delta": "vs 12 của Italia",
                            "leader": True,
                        },
                        {
                            "name": "Tổng cú sút (Italia)",
                            "sub": "4 trúng đích • xG 1,38 • Hỏng 11m phút 90+1",
                            "flag": "IT",
                            "color": COLOR_CYAN,
                            "value": 12,
                        },
                    ],
                },
                {
                    "label": "ĐIỂM SỐ CHUNG CUỘC BẢNG A1",
                    "sub": "Pháp dẫn đầu 13đ • Bỉ đoạt vé tứ kết từ tay Italia",
                    "max_axis": 15,
                    "ticks": [0, 5, 10, 15],
                    "unit": " đ",
                    "rows": [
                        {
                            "name": "Bỉ (Hạng 2)",
                            "sub": "Giành vé vào tứ kết",
                            "flag": "BE",
                            "color": COLOR_ROSE,
                            "value": 12,
                            "delta": "Đi tiếp",
                            "leader": True,
                        },
                        {
                            "name": "Italia (Hạng 3)",
                            "sub": "Bị loại dù chỉ cần 1 điểm",
                            "flag": "IT",
                            "color": COLOR_CYAN,
                            "value": 10,
                            "delta": "Bị loại",
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Bỉ lội ngược dòng", "value": "4-1"},
                {"label": "3 bàn chóng vánh", "value": "11 phút"},
                {"label": "Chung cuộc bảng A1", "value": "Bị loại"},
            ],
            "foot_left": "Nguồn: Football Italia • The Guardian",
            "foot_right": "Esposito ghi bàn 11' rồi sút hỏng 11m phút 90+1",
        }
    }


def _charts_tay_ban_nha() -> Dict[str, Any]:
    """Đồ thị Cyber-Stadium DataViz phân tích Tây Ban Nha 2-3 Anh (Chấm dứt 43 trận bất bại)."""
    return {
        "4": {
            "type": "grouped_race",
            "credit": "SOFASCORE / FORZA FOOTBALL",
            "kicker": "UEFA NATIONS LEAGUE • BẢNG A3 • MADRID",
            "title": "CHẤM DỨT 43 TRẬN BẤT BẠI: TBN 2-3 ANH",
            "legend": [
                {"label": "Tây Ban Nha (HLV De la Fuente)", "color": COLOR_CYAN},
                {"label": "Anh (HLV Thomas Tuchel)", "color": COLOR_ROSE},
            ],
            "sections": [
                {
                    "label": "KIỂM SOÁT BÓNG & SỨC ÉP CHUNG CUỘC",
                    "sub": "Tây Ban Nha cầm bóng 64% nhưng trả giá vì 3 bàn thua sớm",
                    "max_axis": 100,
                    "ticks": [0, 25, 50, 75, 100],
                    "unit": "%",
                    "rows": [
                        {
                            "name": "Kiểm soát bóng (TBN)",
                            "sub": "xG 2,83 • Gỡ 2 bàn sau phút 63",
                            "flag": "ES",
                            "color": COLOR_CYAN,
                            "value": 64,
                            "delta": "+28% cầm bóng",
                            "leader": True,
                        },
                        {
                            "name": "Kiểm soát bóng (Anh)",
                            "sub": "xG 2,15 • Chơi thiếu người từ phút 63",
                            "flag": "ENG",
                            "color": COLOR_ROSE,
                            "value": 36,
                        },
                    ],
                },
                {
                    "label": "CÚ SÚT TRÚNG ĐÍCH & HIỆU QUẢ",
                    "sub": "James Trafford cản phá 6 lần giúp Tam Sư đứng vững",
                    "max_axis": 10,
                    "ticks": [0, 2, 4, 6, 8, 10],
                    "unit": "",
                    "rows": [
                        {
                            "name": "Trúng đích (TBN)",
                            "sub": "7 pha dứt điểm trúng khung thành • 2 bàn",
                            "flag": "ES",
                            "color": COLOR_CYAN,
                            "value": 7,
                        },
                        {
                            "name": "Trúng đích (Anh)",
                            "sub": "5 lần trúng đích • Ghi 3 bàn dẫn trước",
                            "flag": "ENG",
                            "color": COLOR_ROSE,
                            "value": 5,
                            "delta": "Hiệu suất 60%",
                            "leader": True,
                        },
                    ],
                },
            ],
            "kpis": [
                {"label": "Chuỗi bất bại", "value": "Đứt 43 trận"},
                {"label": "Cản phá Trafford", "value": "6 pha cứu thua"},
                {"label": "Thẻ đỏ Anderson", "value": "Phút 63"},
            ],
            "foot_left": "Nguồn: VnExpress • Independent • BBC",
            "foot_right": "Anh vươn lên chiếm ngôi đầu bảng A3",
        }
    }


def _make_dual_item(
    item_id: int,
    slug: str,
    group: str,
    title: str,
    match_text: str,
    comment_text: str,
    source: str,
    news_source: str,
    credit: str,
    seo_title: str,
    description: List[str],
    hashtags: List[str],
    hook: Dict[str, Any],
    sentence_charts: Dict[str, Any],
    thumb: Dict[str, Any],
    images: List[Dict[str, str]],
    plan_slots: List[tuple],
) -> Dict[str, Any]:
    return {
        "id": item_id,
        "slug": slug,
        "voice_preset": "mixed",
        "voice_segments": [
            {"voice_preset": "secondary", "text": match_text},
            {"voice_preset": "primary", "text": comment_text},
        ],
        "group": group,
        "title": title,
        "summary": f"{match_text} {comment_text}",
        "source": source,
        "news_source": news_source,
        "credit": credit,
        "hide_date_chip": True,
        "seo_title": seo_title,
        "description": description,
        "hashtags": hashtags,
        "hook": hook,
        "sentence_charts": sentence_charts,
        "thumb": thumb,
        "images": images,
        "plan_slots": plan_slots,
    }


NEWS_DATA_16_11: List[Dict[str, Any]] = [
    _make_dual_item(
        item_id=1,
        slug="Short_Argentina_Thua_Uruguay_1_2_Thoi_Hau_Messi",
        group="GIAO HỮU QUỐC TẾ • ARGENTINA",
        title="Argentina thua Uruguay 1-2 thời hậu Messi",
        match_text=(
            "Ngày 13 tháng 11 tại sân La Bombonera, đội tuyển Argentina bước vào trận giao hữu gặp Uruguay lần đầu tiên sau khi siêu sao Lionel Messi giã từ sự nghiệp quốc tế, với chiếc áo số 10 được bỏ trống để tri ân. "
            "Dù kiểm soát bóng tới 72 phần trăm và tung ra 17 cú dứt điểm, đội chủ nhà bất ngờ thủng lưới hai bàn chóng vánh đầu hiệp hai từ pha phản lưới của Leonardo Balerdi phút 48 và cú dứt điểm của Maximiliano Araujo phút 53, trước khi Julian Alvarez ghi bàn rút ngắn tỷ số xuống 1-2 ở phút 73."
        ),
        comment_text=(
            "Thất bại ngay trên thánh địa Bombonera là hồi chuông cảnh tỉnh cho kỷ nguyên hậu Messi của HLV Lionel Scaloni sau khi ông vừa gia hạn hợp đồng đến năm 2030. "
            "Argentina cầm bóng nhiều nhưng hoàn toàn bế tắc trước khối phòng ngự chặt chẽ mà tân HLV Diego Forlan xây dựng cho Uruguay, thiếu người tạo đột biến và dễ tổn thương ở các tình huống cố định. "
            "Nếu không sớm tìm ra nhạc trưởng mới trước cuộc chạm trán Costa Rica ngày 17 tháng 11, sức ép lên đội bóng xứ Tango sẽ ngày một lớn."
        ),
        source="Sky Sports / BeIN Sports & Báo Quảng Ninh",
        news_source="SKY SPORTS / BEIN SPORTS",
        credit="PERFIL / REUTERS / PROKERALA",
        seo_title="Argentina thua Uruguay 1-2 ngay trên sân nhà trong trận đầu thời hậu Messi #Shorts",
        description=[
            "Ngày 13/11/2026 tại sân La Bombonera (Buenos Aires), đội tuyển Argentina nhận thất bại 1-2 trước Uruguay trong trận đấu đầu tiên đánh dấu kỷ nguyên hậu Lionel Messi (áo số 10 được bỏ trống tri ân).",
            "Dù kiểm soát bóng 72% và tung ra 17 cú sút, đoàn quân của HLV Lionel Scaloni vẫn gục ngã bởi bàn phản lưới của Leonardo Balerdi (48') cùng pha lập công của Maximiliano Araujo (53'), trước khi Julian Alvarez gỡ lại 1 bàn ở phút 73.",
            "Góc nhìn bình luận: Khối phòng ngự kỷ luật của tân HLV Diego Forlan đã phơi bày sự thiếu đột biến và bài toán tìm nhạc trưởng mới của Argentina trước trận gặp Costa Rica ngày 17/11.",
        ],
        hashtags=[
            "#Shorts", "#DiemDoc", "#Argentina", "#Uruguay", "#LionelMessi",
            "#JulianAlvarez", "#LionelScaloni", "#BongDaNamMy",
        ],
        hook={
            "kicker": "KỶ NGUYÊN HẬU MESSI • LA BOMBONERA",
            "vs_badge": "ARGENTINA vs URUGUAY",
            "stat_val": 1,
            "stat_unit": "- 2",
            "stat_label": "GỤC NGÃ NGAY TRÊN SÂN NHÀ",
            "stat_sub": "CẦM BÓNG 72% VẪN THUA URUGUAY • ÁO SỐ 10 ĐỂ TRỐNG",
            "opp_val": 2,
            "count_dur": 0.65,
            "pills": [
                {"text": "72% KIỂM SOÁT", "style": "cyan", "delay": 1.15},
                {"text": "BALERDI PHẢN LƯỚI", "style": "gold", "delay": 1.85},
                {"text": "HỒI CHUÔNG CẢNH TỈNH", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        sentence_charts=_charts_argentina(),
        thumb={
            "image": "v1_match_duel.jpg",
            "badge": "ARGENTINA vs URUGUAY",
            "kicker": "LA BOMBONERA • THỜI HẬU MESSI",
            "hero_html": 'ARGENTINA GỤC NGÃ <span class="hl">1-2 TRƯỚC URUGUAY</span>',
            "subtitle": "Cầm bóng 72% vẫn thua ngay sân nhà; hồi chuông cảnh tỉnh cho HLV Scaloni",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "16.11.2026",
            "obj_pos": "center 20%",
        },
        images=[
            # Title (0)
            {"dest": "v1_match_duel.jpg", "src": "v1_01.jpg", "credit": "PERFIL", "desc": "Pha tranh chấp quyết liệt giữa Argentina và Uruguay"},
            {"dest": "v1_bombonera_night.jpg", "src": "v1_16.jpg", "credit": "HEADOUT", "desc": "Chảo lửa La Bombonera rực sáng trong đêm thi đấu"},
            {"dest": "v1_messi_10.jpg", "src": "v1_22_messi.jpg", "credit": "REUTERS", "desc": "Chiếc áo số 10 huyền thoại của Lionel Messi được bỏ trống"},
            # Câu 1 (Nữ): Trận đầu hậu Messi tại Bombonera, bỏ trống áo số 10
            {"dest": "v1_bombonera_day.jpg", "src": "v1_17.jpg", "credit": "TRIPADVISOR", "desc": "Sân vận động La Bombonera tại Buenos Aires"},
            {"dest": "v1_arg_fans.jpg", "src": "v1_18.jpg", "credit": "HINDUSTAN TIMES", "desc": "Người hâm mộ Argentina cổ vũ đội tuyển thời kỳ mới"},
            # Câu 2 (Nữ): Cầm bóng 72%, 17 sút, Balerdi phản lưới 48', Araujo 53', Alvarez 73'
            {"dest": "v1_balerdi.jpg", "src": "v1_06.jpg", "credit": "MADEINMARSEILLAIS", "desc": "Trung vệ Leonardo Balerdi không may phản lưới phút 48"},
            {"dest": "v1_alvarez_goal.jpg", "src": "v1_05.jpg", "credit": "PROKERALA", "desc": "Julian Alvarez ghi bàn rút ngắn tỷ số xuống 1-2"},
            # Câu 3 (Nam - Bình luận + DataViz): Hồi chuông cảnh tỉnh cho HLV Scaloni (gia hạn 2030)
            {"dest": "v1_scaloni_wc.jpg", "src": "v1_08.jpg", "credit": "PROKERALA", "desc": "HLV Lionel Scaloni đối mặt thử thách lớn sau khi gia hạn đến 2030"},
            {"dest": "v1_scaloni_touch.jpg", "src": "v1_07.jpg", "credit": "XINHUA", "desc": "Lionel Scaloni chỉ đạo ngoài đường biên"},
            # Câu 4 (Nam - Bình luận): Bế tắc trước khối phòng ngự Uruguay của Diego Forlan
            {"dest": "v1_forlan_1.jpg", "src": "v1_11.jpg", "credit": "SABC SPORT", "desc": "Tân HLV Diego Forlan tổ chức hàng thủ kỷ luật cho Uruguay"},
            {"dest": "v1_ronald_araujo.jpg", "src": "v1_21.jpg", "credit": "EL OBSERVADOR", "desc": "Hàng phòng ngự Uruguay đứng vững trước sức ép của chủ nhà"},
            # Câu 5 (Nam - Bình luận): Chờ nhạc trưởng mới trước trận gặp Costa Rica 17/11
            {"dest": "v1_alvarez_cel.jpg", "src": "v1_04.jpg", "credit": "PROKERALA", "desc": "Julian Alvarez là điểm sáng hiếm hoi trên hàng công Argentina"},
            {"dest": "v1_arg_uru_2.jpg", "src": "v1_02.jpg", "credit": "SITIO ANDINO", "desc": "Tuyển Argentina cần lời giải mới trước trận gặp Costa Rica"},
        ],
        plan_slots=[
            ("title", 0, "v1_match_duel.jpg"),
            ("title", 0, "v1_bombonera_night.jpg"),
            ("title", 0, "v1_messi_10.jpg"),
            ("sentence", 1, "v1_bombonera_day.jpg"),
            ("sentence", 1, "v1_arg_fans.jpg"),
            ("sentence", 2, "v1_balerdi.jpg"),
            ("sentence", 2, "v1_alvarez_goal.jpg"),
            ("sentence", 3, "v1_scaloni_wc.jpg"),
            ("sentence", 3, "v1_scaloni_touch.jpg"),
            ("sentence", 4, "v1_forlan_1.jpg"),
            ("sentence", 4, "v1_ronald_araujo.jpg"),
            ("sentence", 5, "v1_alvarez_cel.jpg"),
            ("sentence", 5, "v1_arg_uru_2.jpg"),
        ],
    ),
    _make_dual_item(
        item_id=2,
        slug="Short_Bi_Thang_Dam_Italia_4_1_Mat_Ve_Tu_Ket_Nations_League",
        group="UEFA NATIONS LEAGUE • BẢNG A1",
        title="Italia thua thảm Bỉ 1-4 và bị loại khỏi Nations League",
        match_text=(
            "Rạng sáng 16 tháng 11 tại Brussels, đội tuyển Italia bước vào lượt cuối bảng A1 UEFA Nations League với lợi thế chỉ cần một trận hòa trước Bỉ để giành vé vào tứ kết. "
            "Tiền đạo trẻ Francesco Pio Esposito thắp lên hy vọng khi mở tỷ số ngay phút 11, nhưng chỉ trong vòng 11 phút từ phút 15 đến phút 26, Maxim De Cuyper, Nathan Ngoy và Jeremy Doku liên tiếp ghi bàn khiến thủ môn Gianluigi Donnarumma vào lưới nhặt bóng ba lần, trước khi Diego Moreira ấn định tỷ số 4-1 ở phút 80 và chính Esposito đá hỏng phạt đền phút bù giờ."
        ),
        comment_text=(
            "Chỉ ba ngày sau chiến thắng ấn tượng 3-1 trước tuyển Pháp tại San Siro, màn sụp đổ chóng vánh tại Bỉ phơi bày căn bệnh cố hữu về bản lĩnh sân khách của đoàn quân HLV Roberto Mancini. "
            "Hàng thủ từng là điểm tựa vững chắc của người Ý vỡ vụn trước tốc độ của Jeremy Doku và những đường phản công sắc lẹm do Kevin De Bruyne châm ngòi. "
            "Từ vị thế nắm quyền tự quyết, Italia tự đánh mất tấm vé tứ kết về tay thầy trò Mark van Bommel và để lại bài toán lớn về sự ổn định."
        ),
        source="Football Italia / The Guardian & BeIN Sports",
        news_source="FOOTBALL ITALIA / GUARDIAN",
        credit="UEFA / FOOTBALL ITALIA / L'AVENIR",
        seo_title="Italia thua sốc Bỉ 1-4, đánh rơi vé tứ kết Nations League đầy cay đắng #Shorts",
        description=[
            "Rạng sáng 16/11/2026 tại Brussels (lượt cuối bảng A1 UEFA Nations League), tuyển Italia dù chỉ cần 1 điểm để vào tứ kết và sớm dẫn trước nhờ công Francesco Pio Esposito (11') vẫn thua ngược Bỉ 1-4.",
            "Chỉ trong 11 phút (15'-26'), Maxim De Cuyper, Nathan Ngoy và Jeremy Doku ghi liền 3 bàn cho Bỉ trước khi Diego Moreira ấn định tỷ số phút 80, còn Esposito đá hỏng 11m ở phút 90+1.",
            "Góc nhìn bình luận: Từ chiến thắng 3-1 trước Pháp tại San Siro đến thảm bại ở Brussels, thầy trò HLV Roberto Mancini bộc lộ sự mong manh nơi hàng thủ và bản lĩnh sân khách trước Bỉ của Mark van Bommel.",
        ],
        hashtags=[
            "#Shorts", "#DiemDoc", "#Italia", "#Belgium", "#NationsLeague",
            "#Donnarumma", "#DeBruyne", "#BongDaChauAu",
        ],
        hook={
            "kicker": "THẢM BẠI TẠI BRUSSELS • NATIONS LEAGUE",
            "vs_badge": "BỈ vs ITALIA",
            "stat_val": 4,
            "stat_unit": "- 1",
            "stat_label": "NGƯỢC DÒNG LOẠI ITALIA KHỎI TỨ KẾT",
            "stat_sub": "CHỈ CẦN HÒA NHƯNG THỦNG LƯỚI 3 BÀN TRONG 11 PHÚT",
            "opp_val": 1,
            "count_dur": 0.65,
            "pills": [
                {"text": "3 BÀN TRONG 11 PHÚT", "style": "cyan", "delay": 1.15},
                {"text": "HỎNG 11M PHÚT 90+1", "style": "gold", "delay": 1.85},
                {"text": "MẤT VÉ TỨ KẾT", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        sentence_charts=_charts_italia(),
        thumb={
            "image": "v2_belgium_italy.jpg",
            "badge": "UEFA NATIONS LEAGUE",
            "kicker": "BẢNG A1 • KING BAUDOUIN STADIUM",
            "hero_html": 'ITALIA THUA THẢM BỈ <span class="hl">1-4 BỊ LOẠI</span>',
            "subtitle": "Thủng lưới 3 bàn trong 11 phút; tự đánh mất tấm vé tứ kết dù chỉ cần 1 điểm",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "16.11.2026",
            "obj_pos": "center 20%",
        },
        images=[
            # Title (0)
            {"dest": "v2_belgium_italy.jpg", "src": "v2_02.jpg", "credit": "HINDUSTAN TIMES", "desc": "Tuyển Bỉ ăn mừng chiến thắng hủy diệt trước Italia"},
            {"dest": "v2_brussels_stadium.jpg", "src": "v2_11.jpg", "credit": "KING BAUDOUIN STADIUM", "desc": "Sân vận động King Baudouin tại Brussels"},
            {"dest": "v2_italy_despair.jpg", "src": "v2_19.jpg", "credit": "IRISH EXAMINER", "desc": "Nỗi thất vọng tột cùng của cầu thủ Italia khi bị loại"},
            # Câu 1 (Nữ): Brussels bảng A1, chỉ cần hòa để vào tứ kết
            {"dest": "v2_esposito_port.jpg", "src": "v2_03.jpg", "credit": "FOOTBALL ITALIA", "desc": "Francesco Pio Esposito cùng Italia trước trận quyết định"},
            {"dest": "v2_brussels_aerial.jpg", "src": "v2_12.jpg", "credit": "FOOTBALL TRIPPER", "desc": "Toàn cảnh sân King Baudouin nơi Italia chỉ cần 1 điểm"},
            # Câu 2 (Nữ): Esposito mở tỷ số 11', De Cuyper/Ngoy/Doku ghi 3 bàn trong 11 phút, Donnarumma, Moreira 80'
            {"dest": "v2_esposito_goal.jpg", "src": "v2_04.jpg", "credit": "FOOTBALL ITALIA", "desc": "Esposito mở tỷ số phút 11 nhưng sau đó đá hỏng phạt đền phút 90+1"},
            {"dest": "v2_decuyper.jpg", "src": "v2_06.jpg", "credit": "FOOTBALL ITALIA", "desc": "Maxim De Cuyper mở màn cuộc lội ngược dòng phút 15"},
            # Câu 3 (Nam - Bình luận + DataViz): Hạ Pháp 3-1 ở San Siro, sụp đổ sân khách, Roberto Mancini
            {"dest": "v2_san_siro.jpg", "src": "v2_14.jpg", "credit": "FOOTBALL ITALIA", "desc": "San Siro rực sáng khi Italia thắng Pháp 3-1 cách đó 3 ngày"},
            {"dest": "v2_mancini.jpg", "src": "v2_17.jpg", "credit": "UEFA", "desc": "HLV Roberto Mancini đối mặt áp lực lớn sau thất bại ở Brussels"},
            # Câu 4 (Nam - Bình luận): Hàng thủ vỡ vụn, Donnarumma, De Bruyne châm ngòi
            {"dest": "v2_donnarumma.jpg", "src": "v2_07.jpg", "credit": "UEFA", "desc": "Thủ môn Gianluigi Donnarumma bốn lần phải vào lưới nhặt bóng"},
            {"dest": "v2_debruyne.jpg", "src": "v2_09.jpg", "credit": "BELGIAN RED DEVILS", "desc": "Kevin De Bruyne kiến tạo sắc lẹm xé toang hàng thủ Italia"},
            # Câu 5 (Nam - Bình luận): Đánh mất vé tứ kết về tay Bỉ của Mark van Bommel
            {"dest": "v2_van_bommel.jpg", "src": "v2_13.jpg", "credit": "NRC", "desc": "HLV Mark van Bommel giúp tuyển Bỉ lách qua khe cửa hẹp"},
            {"dest": "v2_italy_collapse.jpg", "src": "v2_18.jpg", "credit": "AP PHOTO", "desc": "Tuyển Italia gục ngã đánh rơi vé vào tứ kết Nations League"},
        ],
        plan_slots=[
            ("title", 0, "v2_belgium_italy.jpg"),
            ("title", 0, "v2_brussels_stadium.jpg"),
            ("title", 0, "v2_italy_despair.jpg"),
            ("sentence", 1, "v2_esposito_port.jpg"),
            ("sentence", 1, "v2_brussels_aerial.jpg"),
            ("sentence", 2, "v2_esposito_goal.jpg"),
            ("sentence", 2, "v2_decuyper.jpg"),
            ("sentence", 3, "v2_san_siro.jpg"),
            ("sentence", 3, "v2_mancini.jpg"),
            ("sentence", 4, "v2_donnarumma.jpg"),
            ("sentence", 4, "v2_debruyne.jpg"),
            ("sentence", 5, "v2_van_bommel.jpg"),
            ("sentence", 5, "v2_italy_collapse.jpg"),
        ],
    ),
    _make_dual_item(
        item_id=3,
        slug="Short_Tay_Ban_Nha_Thua_Anh_2_3_Dut_Chuoi_43_Tran_Bat_Bai",
        group="UEFA NATIONS LEAGUE • BẢNG A3",
        title="Tây Ban Nha thua Anh 2-3, đứt chuỗi 43 trận bất bại",
        match_text=(
            "Tại sân Metropolitano ở Madrid, nhà đương kim vô địch châu Âu và thế giới Tây Ban Nha bất ngờ gục ngã 2-3 trước đội tuyển Anh ở lượt cuối bảng A3 UEFA Nations League. "
            "Harry Kane mở tỷ số từ chấm phạt đền cuối hiệp một sau pha phạm lỗi của Pau Cubarsi, trước khi Ezri Konsa và Ben White liên tiếp lập công đầu hiệp hai giúp Tam Sư dẫn 3-0. "
            "Dù Elliot Anderson nhận thẻ đỏ trực tiếp phút 63 tạo điều kiện cho Mikel Oyarzabal và Nico Williams rút ngắn cách biệt xuống 2-3, La Roja vẫn không kịp thoát thua trên sân nhà."
        ),
        comment_text=(
            "Trận thua kịch tính này chính thức khép lại chuỗi 43 trận bất bại lịch sử kéo dài từ năm 2023 của thầy trò HLV Luis de la Fuente, đồng thời giúp tuyển Anh dưới thời Thomas Tuchel hiên ngang chiếm ngôi đầu bảng. "
            "Dù kiểm soát bóng 64 phần trăm và vùng lên mạnh mẽ khi chơi hơn người, Tây Ban Nha đã bộc lộ điểm yếu chết người trong khả năng chống bóng bổng và chuyển trạng thái. "
            "Thất bại đúng lúc này như một lời nhắc nhở kịp thời để nhà vô địch thế giới nhìn lại hàng phòng ngự thay vì ngủ quên trên ánh hào quang."
        ),
        source="VnExpress / Independent & Thanh Niên",
        news_source="VNEXPRESS / INDEPENDENT",
        credit="UEFA / THE GLOBE AND MAIL / MIRROR",
        seo_title="Tây Ban Nha thua Anh 2-3 ngay tại Madrid, chấm dứt chuỗi 43 trận bất bại #Shorts",
        description=[
            "Đêm 15/11/2026 tại sân Riyadh Air Metropolitano (Madrid), đội tuyển Anh tạo nên cú sốc khi đánh bại nhà đương kim vô địch thế giới Tây Ban Nha với tỷ số 3-2 ở lượt cuối bảng A3 UEFA Nations League.",
            "Harry Kane (45'+ pen), Ezri Konsa (53') và Ben White (57') giúp Tam Sư dẫn 3-0. Sau khi Elliot Anderson nhận thẻ đỏ phút 63, Mikel Oyarzabal (65' pen) và Nico Williams (75') ghi liền 2 bàn nhưng Tây Ban Nha vẫn không thể lật ngược thế cờ.",
            "Góc nhìn bình luận: Thất bại này chấm dứt chuỗi 43 trận bất bại lịch sử của HLV Luis de la Fuente kể từ năm 2023 và đưa tuyển Anh của Thomas Tuchel lên ngôi đầu bảng, đồng thời chỉ ra điểm yếu chống bóng bổng của La Roja.",
        ],
        hashtags=[
            "#Shorts", "#DiemDoc", "#TayBanNha", "#England", "#NationsLeague",
            "#HarryKane", "#LamineYamal", "#ThomasTuchel",
        ],
        hook={
            "kicker": "ĐỊA CHẤN TẠI MADRID • NATIONS LEAGUE",
            "vs_badge": "TÂY BAN NHA vs ANH",
            "stat_val": 43,
            "stat_unit": "TRẬN",
            "stat_label": "CHẤM DỨT CHUỖI BẤT BẠI LỊCH SỬ",
            "stat_sub": "TAM SƯ DẪN TRƯỚC 3-0 NGAY TẠI METROPOLITANO ĐỂ CHIẾM NGÔI ĐẦU",
            "opp_val": 0,
            "count_dur": 0.70,
            "pills": [
                {"text": "ANH DẪN 3-0", "style": "cyan", "delay": 1.15},
                {"text": "THẺ ĐỎ PHÚT 63", "style": "gold", "delay": 1.85},
                {"text": "ĐỨT MẠCH 43 TRẬN", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        sentence_charts=_charts_tay_ban_nha(),
        thumb={
            "image": "v3_spain_england.jpg",
            "badge": "UEFA NATIONS LEAGUE",
            "kicker": "BẢNG A3 • METROPOLITANO MADRID",
            "hero_html": 'TÂY BAN NHA GỤC NGÃ <span class="hl">2-3 TRƯỚC ANH</span>',
            "subtitle": "Chấm dứt chuỗi 43 trận bất bại từ năm 2023; Tam Sư hiên ngang chiếm ngôi đầu",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "16.11.2026",
            "obj_pos": "center 20%",
        },
        images=[
            # Title (0)
            {"dest": "v3_spain_england.jpg", "src": "v3_01.jpg", "credit": "AHRAM ONLINE", "desc": "Màn đọ sức rực lửa giữa Tây Ban Nha và Anh"},
            {"dest": "v3_metropolitano.jpg", "src": "v3_13.jpg", "credit": "GETOUTTRIP", "desc": "Chảo lửa Riyadh Air Metropolitano trong đêm thi đấu"},
            {"dest": "v3_kane_cel.jpg", "src": "v3_18.jpg", "credit": "BHASKAR", "desc": "Harry Kane ăn mừng chiến thắng ấn tượng của Tam Sư"},
            # Câu 1 (Nữ): Nhà vô địch thế giới Tây Ban Nha gục ngã 2-3 tại Madrid
            {"dest": "v3_yamal_trophy.jpg", "src": "v3_20.jpg", "credit": "ACN", "desc": "Nhà vô địch châu Âu và thế giới Tây Ban Nha nếm trái đắng trên sân nhà"},
            {"dest": "v3_spain_eng_2.jpg", "src": "v3_02.jpg", "credit": "FOOTBALL ACTION", "desc": "Cuộc đối đầu căng thẳng tại bảng A3 UEFA Nations League"},
            # Câu 2 (Nữ): Kane pen 45'+, Konsa 53' & Ben White 57' giúp Anh dẫn 3-0
            {"dest": "v3_kane_kick.jpg", "src": "v3_17.jpg", "credit": "THE GLOBE AND MAIL", "desc": "Harry Kane ghi bàn mở tỷ số từ chấm phạt đền cuối hiệp một"},
            {"dest": "v3_konsa_white.jpg", "src": "v3_14.jpg", "credit": "DAILY MIRROR", "desc": "Ezri Konsa cùng Ben White giúp Anh vươn lên dẫn 3-0"},
            # Câu 3 (Nữ): Thẻ đỏ Anderson 63', Oyarzabal & Nico Williams gỡ 2-3 -> DataViz ở câu 4 khi Bình luận bắt đầu?
            # Lưu ý: giữ DataViz ở câu 3 hoặc câu 4 (ngay đầu đoạn bình luận Nam - câu 4!)
            {"dest": "v3_oyarzabal.jpg", "src": "v3_19.jpg", "credit": "BOLAVIP", "desc": "Mikel Oyarzabal rút ngắn tỷ số xuống 1-3 từ chấm phạt đền"},
            {"dest": "v3_ben_white.jpg", "src": "v3_16.jpg", "credit": "CAUGHTOFFSIDE", "desc": "Hàng thủ Anh gồng mình giữ tỷ số 3-2 sau thẻ đỏ phút 63"},
            # Câu 4 (Nam - Bình luận): Khép lại 43 trận bất bại, Luis de la Fuente vs Thomas Tuchel
            {"dest": "v3_delafuente_1.jpg", "src": "v3_06.jpg", "credit": "UEFA", "desc": "HLV Luis de la Fuente đứt mạch 43 trận bất bại cùng La Roja"},
            {"dest": "v3_tuchel_press.jpg", "src": "v3_07.jpg", "credit": "FMT", "desc": "HLV Thomas Tuchel đưa tuyển Anh chiếm ngôi đầu bảng A3"},
            # Câu 5 (Nam - Bình luận): Kiểm soát bóng 64%, điểm yếu bóng bổng & chuyển trạng thái
            {"dest": "v3_delafuente_2.jpg", "src": "v3_09.jpg", "credit": "VANGUARD", "desc": "Tây Ban Nha cần khắc phục điểm yếu bóng bổng nơi hàng thủ"},
            {"dest": "v3_tuchel_touch.jpg", "src": "v3_08.jpg", "credit": "YAHOO SPORTS", "desc": "Thomas Tuchel khai thác triệt để khoảng trống phản công"},
            # Câu 6 (Nam - Bình luận): Lời nhắc nhở kịp thời cho nhà vô địch thế giới
            {"dest": "v3_yamal_medal.jpg", "src": "v3_21.jpg", "credit": "UEFA", "desc": "Lamine Yamal và đồng đội cần giữ đôi chân trên mặt đất"},
            {"dest": "v3_spain_2024.jpg", "src": "v3_10.jpg", "credit": "DAILY SABAH", "desc": "Bài học đắt giá cho nhà đương kim vô địch thế giới"},
        ],
        plan_slots=[
            ("title", 0, "v3_spain_england.jpg"),
            ("title", 0, "v3_metropolitano.jpg"),
            ("title", 0, "v3_kane_cel.jpg"),
            ("sentence", 1, "v3_yamal_trophy.jpg"),
            ("sentence", 1, "v3_spain_eng_2.jpg"),
            ("sentence", 2, "v3_kane_kick.jpg"),
            ("sentence", 2, "v3_konsa_white.jpg"),
            ("sentence", 3, "v3_oyarzabal.jpg"),
            ("sentence", 3, "v3_ben_white.jpg"),
            ("sentence", 4, "v3_delafuente_1.jpg"),
            ("sentence", 4, "v3_tuchel_press.jpg"),
            ("sentence", 5, "v3_delafuente_2.jpg"),
            ("sentence", 5, "v3_tuchel_touch.jpg"),
            ("sentence", 6, "v3_yamal_medal.jpg"),
            ("sentence", 6, "v3_spain_2024.jpg"),
        ],
    ),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Dựng tuần tự Shorts 16.11.2026")
    parser.add_argument("--only", type=int, nargs="+", help="Chỉ chạy các ID tin chỉ định (vd: --only 1)")
    args = parser.parse_args()

    items = NEWS_DATA_16_11
    if args.only:
        target = set(args.only)
        items = [it for it in NEWS_DATA_16_11 if it["id"] in target]
    if not items:
        raise SystemExit("Không tìm thấy item nào phù hợp với --only")

    run_short_batch(
        CTX,
        items,
        f"XUẤT BẢN VIDEO SHORTS 16.11.2026 (TIN {','.join(str(i['id']) for i in items)} — SONG GIỌNG NỮ/NAM)",
    )


if __name__ == "__main__":
    main()
