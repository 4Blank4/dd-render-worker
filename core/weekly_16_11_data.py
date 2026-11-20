# -*- coding: utf-8 -*-
"""
weekly_16_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh (1 Intro + 26 bản tin tuần 09.11 - 15.11.2026).
Phân bổ giọng đọc luân phiên Nam (primary) / Nữ (secondary) và 1-3 ảnh ngang HD mỗi câu.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent
ORTHER = ROOT / "outputs" / "Orther"
CACHE_ROOT = Path.home() / "Library" / "Caches" / "DiemDoc"


def _orther(day: str, fname: str) -> tuple[str, str]:
    return ("local", str(ORTHER / day / "images" / fname))


def _cache(subdir: str, fname: str) -> tuple[str, str]:
    return ("local", str(CACHE_ROOT / subdir / fname))


def _url(u: str) -> tuple[str, str]:
    return ("url", u)


def _ddgs(q: str) -> tuple[str, str]:
    return ("ddgs", q)


def _slot(slot_type: str, sent_idx: int, sources: List[tuple[str, str]], credit: str, desc: str) -> Dict[str, Any]:
    return {
        "type": slot_type,
        "sentence_idx": sent_idx,
        "sources": sources,
        "credit": credit,
        "desc": desc,
    }


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO TUẦN QUA",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao tuần qua từ ngày 9 tháng 11 đến ngày 15 tháng 11. "
        "Bóng đá quốc tế tuần qua rúng động với loạt địa chấn của tuyển Anh, Đan Mạch, Bỉ, Nhật Bản cùng biến động thượng tầng tại Man Utd. "
        "Ở trong nước, U23 Việt Nam đăng quang tại Gia Lai, đội tuyển Việt Nam vươn lên hạng 98 thế giới và VFF mạnh tay xử phạt tiêu cực. "
        "Cùng tấm vé Olympic của Trịnh Thu Vinh và ngôi vương cờ tướng thế giới, hãy điểm lại 26 tin nóng ngay sau đây."
    ),
    "source": "VnExpress / Thanh Niên / Dân Trí",
    "news_source": "VNEXPRESS / THANH NIÊN",
    "credit": "REUTERS / AP / VNEXPRESS",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {"voice_preset": "secondary", "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao tuần qua từ ngày 9 tháng 11 đến ngày 15 tháng 11."},
        {"voice_preset": "primary", "text": "Bóng đá quốc tế tuần qua rúng động với loạt địa chấn của tuyển Anh, Đan Mạch, Bỉ, Nhật Bản cùng biến động thượng tầng tại Man Utd."},
        {"voice_preset": "secondary", "text": "Ở trong nước, U23 Việt Nam đăng quang tại Gia Lai, đội tuyển Việt Nam vươn lên hạng 98 thế giới và VFF mạnh tay xử phạt tiêu cực."},
        {"voice_preset": "primary", "text": "Cùng tấm vé Olympic của Trịnh Thu Vinh và ngôi vương cờ tướng thế giới, hãy điểm lại 26 tin nóng ngay sau đây."},
    ],
    "slots": [
        # Câu 1 (Nữ): Chào mừng quý vị đến với Điểm Đọc... từ ngày 9 tháng 11 đến ngày 15 tháng 11
        _slot("sentence", 1, [_orther("16.11.2026", "v3_spain_england.jpg")], "AHRAM ONLINE", "Tây Ban Nha đối đầu tuyển Anh tại Madrid"),
        _slot("sentence", 1, [_orther("16.11.2026", "v1_messi_10.jpg")], "REUTERS", "Chiếc áo số 10 tri ân kỷ nguyên Ronaldo và Messi"),
        _slot("sentence", 1, [_orther("13.11.2026", "short_2_u23_celebrate.jpg")], "BAOMOI", "U23 Việt Nam bùng nổ ăn mừng ngôi vương"),
        # Câu 2 (Nam): Tuyển Anh chấm dứt 43 trận bất bại, Bồ Đào Nha & Argentina gục ngã, Man Utd đón Pochettino
        _slot("sentence", 2, [_orther("16.11.2026", "v3_kane_cel.jpg")], "BHASKAR", "Harry Kane giúp tuyển Anh thắng 3-2 tại Madrid"),
        _slot("sentence", 2, [_orther("16.11.2026", "v1_match_duel.jpg")], "PERFIL", "Argentina thua Uruguay 1-2 trong trận đầu hậu Messi"),
        _slot("sentence", 2, [_cache("candidates_13_11", "poch_0.jpg"), _orther("11.11.2026", "Tin_06_5.jpg")], "REUTERS", "HLV Mauricio Pochettino đồng ý dẫn dắt Man Utd"),
        # Câu 3 (Nữ): U23 Việt Nam vô địch Gia Lai, ĐT Việt Nam thắng Đài Loan lên hạng 98
        _slot("sentence", 3, [_orther("11.11.2026", "Tin_04_1.jpg")], "VNEXPRESS / ĐỨC CƯỜNG", "U23 Việt Nam thắng đậm U23 Thái Lan 3-0"),
        _slot("sentence", 3, [_orther("13.11.2026", "short_2_baolong_goal.jpg")], "VNEXPRESS", "Nguyễn Bảo Long ăn mừng bàn thắng vào lưới Singapore"),
        _slot("sentence", 3, [_orther("12.11.2026", "Tin_01_1.jpg")], "VNEXPRESS", "Tuyển Việt Nam đánh bại Đài Loan 2-0 tại Thiên Trường"),
        # Câu 4 (Nam): Trịnh Thu Vinh Olympic 2028, Phan Huy Hoàng cờ tướng, ATP Finals Turin
        _slot("sentence", 4, [_orther("11.11.2026", "Tin_03_1.jpg")], "VNEXPRESS / ISSF", "Xạ thủ Trịnh Thu Vinh đoạt HCB thế giới và vé Olympic 2028"),
        _slot("sentence", 4, [_orther("14.11.2026", "s3_hoang_podium.jpg")], "LIÊN ĐOÀN CỜ TƯỚNG VN", "Phan Huy Hoàng đăng quang HCV cờ tướng thế giới"),
        _slot("sentence", 4, [_orther("09.11.2026", "Tin_03_1.jpg")], "AP PHOTO", "Carlos Alcaraz hướng đến ngôi vương ATP Finals tại Turin"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Tây Ban Nha thua Anh 2-3 tại Madrid, đứt chuỗi 43 trận bất bại",
        "summary": (
            "Tại sân Metropolitano ở Madrid, nhà đương kim vô địch châu Âu và thế giới Tây Ban Nha bất ngờ gục ngã 2-3 trước đội tuyển Anh ở lượt cuối bảng A3 UEFA Nations League. "
            "Harry Kane mở tỷ số từ chấm phạt đền cuối hiệp một sau pha phạm lỗi của Pau Cubarsi, trước khi Ezri Konsa và Ben White liên tiếp lập công đầu hiệp hai giúp Tam Sư dẫn 3-0. "
            "Dù Elliot Anderson nhận thẻ đỏ trực tiếp phút 63 tạo điều kiện cho Mikel Oyarzabal và Nico Williams rút ngắn cách biệt xuống 2-3, La Roja vẫn không kịp thoát thua trên sân nhà. "
            "Trận thua kịch tính này chính thức khép lại chuỗi 43 trận bất bại lịch sử kéo dài từ năm 2023 của HLV Luis de la Fuente, đồng thời đưa tuyển Anh dưới thời Thomas Tuchel hiên ngang chiếm ngôi đầu bảng."
        ),
        "source": "VnExpress / Independent",
        "news_source": "VNEXPRESS / INDEPENDENT",
        "credit": "UEFA / THE GLOBE AND MAIL / MIRROR",
        "slots": [
            _slot("title", 0, [_orther("16.11.2026", "v3_spain_england.jpg")], "AHRAM ONLINE", "Màn đọ sức rực lửa giữa Tây Ban Nha và Anh"),
            _slot("title", 0, [_orther("16.11.2026", "v3_metropolitano.jpg")], "GETOUTTRIP", "Chảo lửa Metropolitano Madrid trong đêm thi đấu"),
            _slot("title", 0, [_orther("16.11.2026", "v3_kane_cel.jpg")], "BHASKAR", "Harry Kane ăn mừng chiến thắng ấn tượng của Tam Sư"),
            _slot("sentence", 1, [_orther("16.11.2026", "v3_yamal_trophy.jpg")], "ACN", "Nhà vô địch châu Âu và thế giới Tây Ban Nha nếm trái đắng"),
            _slot("sentence", 1, [_orther("16.11.2026", "v3_spain_eng_2.jpg")], "FOOTBALL ACTION", "Cuộc đối đầu căng thẳng tại bảng A3 Nations League"),
            _slot("sentence", 2, [_orther("16.11.2026", "v3_kane_kick.jpg")], "THE GLOBE AND MAIL", "Harry Kane ghi bàn mở tỷ số từ chấm phạt đền cuối hiệp một"),
            _slot("sentence", 2, [_orther("16.11.2026", "v3_konsa_white.jpg")], "DAILY MIRROR", "Ezri Konsa cùng Ben White giúp Anh vươn lên dẫn 3-0"),
            _slot("sentence", 3, [_orther("16.11.2026", "v3_oyarzabal.jpg")], "BOLAVIP", "Mikel Oyarzabal rút ngắn tỷ số cho Tây Ban Nha"),
            _slot("sentence", 3, [_cache("candidates_16_11", "v3_11.jpg"), _ddgs("England Spain Nations League match 2026 action")], "UEFA", "Hàng thủ tuyển Anh đứng vững sau tấm thẻ đỏ phút 63"),
            _slot("sentence", 4, [_orther("16.11.2026", "v3_delafuente_1.jpg")], "UEFA", "HLV Luis de la Fuente đứt mạch 43 trận bất bại cùng La Roja"),
            _slot("sentence", 4, [_orther("16.11.2026", "v3_tuchel_press.jpg")], "FMT", "HLV Thomas Tuchel đưa tuyển Anh chiếm ngôi đầu bảng A3"),
            _slot("sentence", 4, [_orther("16.11.2026", "v3_yamal_medal.jpg")], "UEFA", "Lamine Yamal và đồng đội đón nhận bài học phòng ngự đắt giá"),
        ],
    },
    # 02 (Nữ) - Mới
    {
        "id": 2,
        "art_id": "art_02",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Bồ Đào Nha thua Đan Mạch 1-4 trên sân nhà ngay ngày tri ân Ronaldo",
        "summary": (
            "Rạng sáng 15 tháng 11 tại sân Municipal de Braga, đội tuyển Bồ Đào Nha bước vào trận đấu chính thức đầu tiên vắng Cristiano Ronaldo sau 23 năm trong khuôn khổ UEFA Nations League. "
            "Trước giờ bóng lăn, khán đài giăng đại kỳ cảm ơn đội trưởng, đồng thời Liên đoàn Bóng đá Bồ Đào Nha ra mắt mẫu áo số 7 mới để tri ân vĩnh viễn biểu tượng cũ. "
            "Tuy nhiên, hàng thủ thiếu chắc chắn khiến chủ nhà nhận trận thua sân nhà đậm nhất lịch sử 1-4 trước Đan Mạch khi tiền đạo Rasmus Hojlund lập cú đúp còn trung vệ Ruben Dias mắc lỗi ở ba bàn thua. "
            "Truyền thông châu Âu lập tức chỉ trích dữ dội màn trình diễn bạc nhược của thầy trò HLV Jorge Jesus và đặt câu hỏi lớn về bản lĩnh đội tuyển thời hậu Ronaldo."
        ),
        "source": "VnExpress / Thanh Niên",
        "news_source": "VNEXPRESS / THANH NIÊN",
        "credit": "REUTERS / AP / VNEXPRESS",
        "slots": [
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/15/2026t214124z-mt1sipa000ydas16-6469-7927-1794706438.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=Kk4vGVz0h6hywFtoduS7ww"),
                _ddgs("Portugal Denmark Nations League Braga match action"),
            ], "REUTERS / SIPA", "Bồ Đào Nha đối đầu Đan Mạch trên sân Municipal de Braga"),
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/15/ronaldo-7938-1794685237.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=Yr5V98_ZBDvffmJgsl2hzg"),
                _ddgs("Cristiano Ronaldo Portugal national team number 7"),
            ], "AP PHOTO", "Cristiano Ronaldo khép lại hành trình 23 năm cùng tuyển Bồ Đào Nha"),
            _slot("title", 0, [
                _ddgs("Rasmus Hojlund Denmark celebration goal"),
                _ddgs("Rasmus Hojlund Denmark football match"),
            ], "REUTERS", "Rasmus Hojlund bùng nổ giúp Đan Mạch đại thắng 4-1"),
            _slot("sentence", 1, [
                _ddgs("Estadio Municipal de Braga Portugal stadium"),
                _ddgs("Municipal de Braga stadium night match"),
            ], "UEFA", "Sân Municipal de Braga trong đêm đầu tiên Bồ Đào Nha vắng Ronaldo"),
            _slot("sentence", 1, [
                _ddgs("Portugal national team lineup 2026 Nations League"),
                _ddgs("Bruno Fernandes Portugal national team match"),
            ], "REUTERS", "Đội tuyển Bồ Đào Nha ra sân không có thủ quân 41 tuổi"),
            _slot("sentence", 2, [
                _url("https://iv1.vnecdn.net/thethao/images/web/2026/11/15/bo-dao-nha-doi-cach-viet-so-7-de-tri-an-ronaldo-1794684304.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=riZd8m4RO5TQIVBveJWClA"),
                _ddgs("Portugal jersey number 7 Cristiano Ronaldo tribute"),
            ], "FPF / VNEXPRESS", "Bồ Đào Nha đổi nét chữ số 7 để tôn vinh di sản của CR7"),
            _slot("sentence", 2, [
                _ddgs("Cristiano Ronaldo Portugal fans stadium banner tribute"),
                _ddgs("Portugal fans stadium crowd Braga flag"),
            ], "REUTERS", "Người hâm mộ trên khán đài tri ân đội trưởng huyền thoại"),
            _slot("sentence", 3, [
                _ddgs("Rasmus Hojlund Denmark striker celebration"),
                _ddgs("Denmark national football team celebration goal"),
            ], "REUTERS", "Tiền đạo Rasmus Hojlund lập cú đúp nhấn chìm đội chủ nhà"),
            _slot("sentence", 3, [
                _ddgs("Ruben Dias Portugal national team frustrated match"),
                _ddgs("Pierre-Emile Hojbjerg Denmark Portugal match"),
            ], "AP PHOTO", "Trung vệ Ruben Dias và hàng thủ Bồ Đào Nha mắc nhiều sai lầm"),
            _slot("sentence", 4, [
                _ddgs("Jorge Jesus coach Portugal press conference"),
                _ddgs("Jorge Jesus football coach touchline"),
            ], "REUTERS", "HLV Jorge Jesus chịu sức ép nặng nề sau trận thua đậm nhất lịch sử sân nhà"),
            _slot("sentence", 4, [
                _ddgs("Bernardo Silva Portugal national team disappointed"),
                _ddgs("Joao Felix Portugal national team match"),
            ], "AP PHOTO", "Báo chí châu Âu đặt dấu hỏi lớn về Bồ Đào Nha thời hậu Ronaldo"),
        ],
    },
    # 03 (Nam)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Italia thua thảm Bỉ 1-4, mất vé tứ kết Nations League dù vừa hạ Pháp",
        "summary": (
            "Chỉ ba ngày sau khi ngược dòng thắng Pháp 3-1 ngay tại San Siro để khiến HLV Zinedine Zidane nếm thất bại đầu tiên, đội tuyển Italia lại gây sốc khi thảm bại 1-4 trên sân Bỉ sáng 16 tháng 11. "
            "Bước vào lượt cuối bảng A1 với lợi thế chỉ cần một điểm để đi tiếp, Italia khởi đầu như mơ nhờ bàn mở tỷ số phút 11 của tiền đạo trẻ Francesco Pio Esposito. "
            "Thế nhưng chỉ trong vòng 11 phút từ phút 15 đến phút 26, Maxim De Cuyper, Nathan Ngoy và Jeremy Doku liên tiếp xé lưới thủ môn Gianluigi Donnarumma trước khi Diego Moreira ấn định tỷ số 4-1 và Esposito hỏng phạt đền phút bù giờ. "
            "Trận sụp đổ chóng vánh trước đoàn quân của HLV Mark van Bommel khiến thầy trò Roberto Mancini mất tấm vé tứ kết và phơi bày căn bệnh yếu bản lĩnh sân khách."
        ),
        "source": "VnExpress / Football Italia",
        "news_source": "VNEXPRESS / FOOTBALL ITALIA",
        "credit": "UEFA / AP / REUTERS",
        "slots": [
            _slot("title", 0, [_orther("16.11.2026", "v2_belgium_italy.jpg")], "HINDUSTAN TIMES", "Tuyển Bỉ ăn mừng chiến thắng hủy diệt 4-1 trước Italia"),
            _slot("title", 0, [_orther("16.11.2026", "v2_brussels_stadium.jpg")], "KING BAUDOUIN STADIUM", "Sân vận động King Baudouin tại Brussels đêm diễn ra trận đấu"),
            _slot("title", 0, [_orther("16.11.2026", "v2_italy_despair.jpg")], "IRISH EXAMINER", "Nỗi thất vọng tột cùng của cầu thủ Italia khi bị loại"),
            _slot("sentence", 1, [_url("https://i1-thethao.vnecdn.net/2026/11/14/AP26316758827855-7457-1794651171.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=CgU2-p6phs6kLS5ysZM-qQ"), _orther("16.11.2026", "v2_san_siro.jpg")], "AP PHOTO", "Italia từng bùng nổ thắng Pháp 3-1 ngay tại San Siro ba ngày trước đó"),
            _slot("sentence", 1, [_url("https://i1-thethao.vnecdn.net/2026/11/14/AP26316780248222-7736-1794651171.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=cXWA3J5dhYssNq5IkkUz_w"), _ddgs("Zinedine Zidane France coach touchline 2026")], "AP PHOTO", "HLV Zinedine Zidane nhận trận thua đầu tay khi dẫn dắt tuyển Pháp"),
            _slot("sentence", 2, [_orther("16.11.2026", "v2_esposito_port.jpg")], "FOOTBALL ITALIA", "Francesco Pio Esposito cùng tuyển Italia bước vào lượt trận quyết định"),
            _slot("sentence", 2, [_orther("16.11.2026", "v2_esposito_goal.jpg")], "FOOTBALL ITALIA", "Esposito mở tỷ số phút 11 nhưng sau đó đá hỏng 11m phút 90+1"),
            _slot("sentence", 3, [_orther("16.11.2026", "v2_decuyper.jpg")], "FOOTBALL ITALIA", "Maxim De Cuyper mở màn cơn lốc ba bàn trong 11 phút của Bỉ"),
            _slot("sentence", 3, [_orther("16.11.2026", "v2_donnarumma.jpg")], "UEFA", "Thủ môn Gianluigi Donnarumma bốn lần vào lưới nhặt bóng"),
            _slot("sentence", 3, [_orther("16.11.2026", "v2_debruyne.jpg")], "BELGIAN RED DEVILS", "Kevin De Bruyne và Jeremy Doku làm chủ hoàn toàn thế trận"),
            _slot("sentence", 4, [_orther("16.11.2026", "v2_van_bommel.jpg")], "NRC", "HLV Mark van Bommel giúp tuyển Bỉ đoạt vé vào tứ kết"),
            _slot("sentence", 4, [_orther("16.11.2026", "v2_mancini.jpg")], "UEFA", "HLV Roberto Mancini đối mặt bài toán tâm lý sân khách của Italia"),
            _slot("sentence", 4, [_orther("16.11.2026", "v2_italy_collapse.jpg")], "AP PHOTO", "Đội tuyển Italia gục ngã đánh rơi quyền tự quyết"),
        ],
    },
    # 04 (Nữ)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Hà Lan hủy diệt Hy Lạp 7-0, Tijjani Reijnders lập hat-trick trong 21 phút",
        "summary": (
            "Tại lượt áp chót bảng A2 UEFA Nations League trên sân Amsterdam, đội tuyển Hà Lan của HLV Xavi Hernandez đã tạo nên cơn mưa bàn thắng hủy diệt Hy Lạp 7-0. "
            "Ngay sau pha mở tỷ số phút thứ sáu của Crysencio Summerville, tiền vệ Tijjani Reijnders bùng nổ lập cú hat-trick chỉ trong 21 phút hiệp một, tái lập kỳ tích của huyền thoại Marco van Basten năm 1990. "
            "Hậu vệ Jurrien Timber tiếp tục tỏa sáng với một cú đúp cùng bàn ấn định của Donyell Malen, giúp Cơn lốc màu da cam tung ra 17 cú sút và san bằng kỷ lục thắng đậm nhất lịch sử giải đấu. "
            "Chiến thắng tưng bừng này đưa Hà Lan lên dẫn đầu bảng A2 với 11 điểm, tạo đà tâm lý rực lửa trước cuộc quyết đấu gặp đội tuyển Đức của HLV Jurgen Klopp."
        ),
        "source": "VnExpress / Goal & Reuters",
        "news_source": "VNEXPRESS / REUTERS",
        "credit": "REUTERS / AP / UEFA",
        "slots": [
            _slot("title", 0, [_orther("14.11.2026", "s2_reijnders_ball.jpg")], "REUTERS", "Tijjani Reijnders ôm bóng sau cú hat-trick siêu tốc"),
            _slot("title", 0, [_orther("14.11.2026", "s2_oranje_greece.jpg")], "REUTERS", "Đội tuyển Hà Lan áp đảo hoàn toàn trước Hy Lạp"),
            _slot("title", 0, [_ddgs("Johan Cruijff Arena Amsterdam football match night")], "UEFA", "Khán đài rực sắc cam tại Johan Cruijff Arena Amsterdam"),
            _slot("sentence", 1, [_orther("14.11.2026", "s2_xavi_coach.jpg")], "GIVEMESPORT", "HLV Xavi Hernandez xây dựng lối chơi tấn công rực lửa cho Hà Lan"),
            _slot("sentence", 1, [_orther("14.11.2026", "s2_pavlidis_sad.jpg")], "REUTERS", "Đội tuyển Hy Lạp nhận thất bại choáng váng trên đất khách"),
            _slot("sentence", 2, [_orther("14.11.2026", "s2_summerville.jpg")], "INT INSIGHT", "Crysencio Summerville mở tỷ số ngay phút thứ sáu"),
            _slot("sentence", 2, [_orther("14.11.2026", "s2_reijnders_cel.jpg")], "GIVEMESPORT", "Reijnders tái lập kỳ tích ghi hat-trick trong hiệp một của Van Basten"),
            _slot("sentence", 3, [_orther("14.11.2026", "s2_timber.jpg")], "CAUGHTOFFSIDE", "Hậu vệ Jurrien Timber tỏa sáng với cú đúp bàn thắng"),
            _slot("sentence", 3, [_orther("14.11.2026", "s2_malen.jpg")], "THE NATIONAL HERALD", "Donyell Malen ghi bàn ấn định chiến thắng kỷ lục 7-0"),
            _slot("sentence", 3, [_orther("14.11.2026", "s2_dumfries.jpg")], "SEMPREINTER", "Denzel Dumfries cùng hàng công Hà Lan áp đảo 17 cú dứt điểm"),
            _slot("sentence", 4, [_orther("14.11.2026", "s2_reijnders_orange.jpg")], "SOCCERNEWS NL", "Hà Lan độc chiếm ngôi đầu bảng A2 với 11 điểm"),
            _slot("sentence", 4, [_orther("14.11.2026", "s2_xavi_press.jpg")], "DIARIO AS", "HLV Xavi giữ sự tập trung cho trận đại chiến quyết định"),
            _slot("sentence", 4, [_orther("14.11.2026", "s2_klopp_germany.jpg")], "AP PHOTO", "HLV Jurgen Klopp cùng đội tuyển Đức là thử thách cuối cùng"),
        ],
    },
    # 05 (Nam)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Argentina gục ngã 1-2 trước Uruguay ngay trận đầu thời hậu Messi",
        "summary": (
            "Ngày 13 tháng 11 tại sân La Bombonera, đội tuyển Argentina bước vào trận giao hữu gặp Uruguay lần đầu tiên sau khi siêu sao Lionel Messi giã từ sự nghiệp quốc tế, với chiếc áo số 10 được bỏ trống để tri ân. "
            "Dù kiểm soát bóng tới 72% và tung ra 17 cú dứt điểm, đội chủ nhà bất ngờ thủng lưới hai bàn chóng vánh đầu hiệp hai từ pha phản lưới của Leonardo Balerdi phút 48 và cú dứt điểm của Maximiliano Araujo phút 53, trước khi Julian Alvarez rút ngắn tỷ số phút 73. "
            "Thất bại ngay trên thánh địa Bombonera giữa những khán đài thưa thớt hơn thường lệ là hồi chuông cảnh tỉnh cho kỷ nguyên hậu Messi của HLV Lionel Scaloni sau khi ông vừa gia hạn hợp đồng đến năm 2030. "
            "Argentina cầm bóng nhiều nhưng hoàn toàn bế tắc trước khối phòng ngự kỷ luật mà tân HLV Diego Forlan xây dựng cho Uruguay, phơi bày bài toán cấp thiết tìm nhạc trưởng mới."
        ),
        "source": "Sky Sports / BeIN Sports & VnExpress",
        "news_source": "SKY SPORTS / VNEXPRESS",
        "credit": "PERFIL / REUTERS / PROKERALA",
        "slots": [
            _slot("title", 0, [_orther("16.11.2026", "v1_match_duel.jpg")], "PERFIL", "Pha tranh chấp quyết liệt giữa Argentina và Uruguay"),
            _slot("title", 0, [_orther("16.11.2026", "v1_bombonera_night.jpg")], "HEADOUT", "Chảo lửa La Bombonera rực sáng trong đêm thi đấu"),
            _slot("title", 0, [_orther("16.11.2026", "v1_messi_10.jpg")], "REUTERS", "Chiếc áo số 10 huyền thoại của Lionel Messi được bỏ trống"),
            _slot("sentence", 1, [_cache("candidates_16_11", "v1_03.jpg")], "REUTERS", "Đội tuyển Argentina bước vào kỷ nguyên không còn Lionel Messi"),
            _slot("sentence", 1, [_orther("16.11.2026", "v1_arg_fans.jpg")], "HINDUSTAN TIMES", "Cổ động viên Argentina dõi theo đội tuyển trong diện mạo mới"),
            _slot("sentence", 2, [_orther("16.11.2026", "v1_balerdi.jpg")], "MADEINMARSEILLAIS", "Trung vệ Leonardo Balerdi không may phản lưới nhà phút 48"),
            _slot("sentence", 2, [_orther("16.11.2026", "v1_alvarez_goal.jpg")], "PROKERALA", "Julian Alvarez ghi bàn rút ngắn tỷ số xuống 1-2 phút 73"),
            _slot("sentence", 2, [_cache("candidates_16_11", "v1_20.jpg")], "REUTERS", "Uruguay tận dụng tối đa cơ hội trừng phạt chủ nhà Argentina"),
            _slot("sentence", 3, [_orther("16.11.2026", "v1_scaloni_wc.jpg")], "PROKERALA", "HLV Lionel Scaloni đối mặt thử thách sau khi gia hạn đến 2030"),
            _slot("sentence", 3, [_orther("16.11.2026", "v1_scaloni_touch.jpg")], "XINHUA", "HLV Scaloni căng thẳng chỉ đạo bên đường biên"),
            _slot("sentence", 4, [_orther("16.11.2026", "v1_forlan_1.jpg")], "SABC SPORT", "Tân HLV Diego Forlan tổ chức khối phòng ngự kín kẽ cho Uruguay"),
            _slot("sentence", 4, [_orther("16.11.2026", "v1_ronald_araujo.jpg")], "EL OBSERVADOR", "Hàng thủ Uruguay đứng vững trước 17 pha dứt điểm của Argentina"),
        ],
    },
    # 06 (Nữ) - Mới
    {
        "id": 6,
        "art_id": "art_06",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Brazil thua ngược Nhật Bản 2-3 phút bù giờ, HLV Ancelotti nhận thẻ đỏ",
        "summary": (
            "Tối 14 tháng 11 tại sân Quốc gia Singapore, đội tuyển Brazil của HLV Carlo Ancelotti đã gây thất vọng lớn khi thua Nhật Bản 2-3 trong trận giao hữu quốc tế. "
            "Takefusa Kubo và Keito Nakamura sớm giúp đại diện châu Á dẫn hai bàn chỉ sau 19 phút, trước khi ngôi sao Vinicius Junior lập cú đúp ở phút 33 và phút 75 để gỡ hòa 2-2. "
            "Đúng phút bù giờ đầu tiên của hiệp hai, tiền đạo Tatsuhiro Sakamoto ghi bàn cận thành ấn định thắng lợi lịch sử 3-2, khiến HLV Carlo Ancelotti và thủ quân Raphinha mất bình tĩnh phản ứng trọng tài và cùng nhận thẻ đỏ trực tiếp. "
            "Ngay sau thất bại thứ hai liên tiếp trước Nhật Bản dưới thời Ancelotti, huyền thoại Romario đã lên tiếng chỉ trích gay gắt và yêu cầu sa thải chiến lược gia người Italy."
        ),
        "source": "VnExpress / Dân Trí",
        "news_source": "VNEXPRESS / DÂN TRÍ",
        "credit": "AP PHOTO / REUTERS / VNEXPRESS",
        "slots": [
            _slot("title", 0, [
                _url("https://iv1.vnecdn.net/thethao/images/web/2026/11/14/ancelotti-bi-duoi-khi-brazil-thua-nhat-ban-1794663212.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=E-CTZmUAOz7l2uAE9zoy4Q"),
                _ddgs("Carlo Ancelotti Brazil coach angry red card match"),
            ], "AP PHOTO / VNEXPRESS", "HLV Carlo Ancelotti bức xúc bên đường biên trước Nhật Bản"),
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/14/AP26318379770516-4278-1794663572.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=R4vBAAEc1hAoN7LbgS6kHg"),
                _ddgs("Japan Brazil football match action 2026"),
            ], "AP PHOTO", "Đội tuyển Nhật Bản thi đấu kiên cường đánh bại Brazil 3-2"),
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/14/AP26318436930290-3034-1794663573.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=hfEtkVla7QX8Ip5dRwhxkg"),
                _ddgs("Singapore National Stadium football match crowd"),
            ], "AP PHOTO", "Sức nóng trận giao hữu Brazil và Nhật Bản tại Singapore"),
            _slot("sentence", 1, [
                _ddgs("Singapore National Stadium pitch view match"),
                _ddgs("Brazil national football team match 2026"),
            ], "REUTERS", "Sân Quốc gia Singapore chứng kiến màn so tài kịch tính"),
            _slot("sentence", 1, [
                _ddgs("Carlo Ancelotti Brazil national team coach bench"),
                _ddgs("Brazil national team starting lineup 2026"),
            ], "AP PHOTO", "Brazil chơi thiếu thuyết phục dưới tay HLV Carlo Ancelotti"),
            _slot("sentence", 2, [
                _ddgs("Takefusa Kubo Japan national team celebration goal"),
                _ddgs("Keito Nakamura Japan national team goal"),
            ], "REUTERS", "Takefusa Kubo và Keito Nakamura giúp Nhật Bản dẫn sớm 2-0"),
            _slot("sentence", 2, [
                _ddgs("Vinicius Junior Brazil national team goal celebration"),
                _ddgs("Vinicius Junior Brazil national team dribbling"),
            ], "AP PHOTO", "Vinicius Junior lập cú đúp níu giữ hy vọng hòa 2-2 cho Brazil"),
            _slot("sentence", 3, [
                _ddgs("Tatsuhiro Sakamoto Japan national team player celebration"),
                _ddgs("Japan national football team celebration victory"),
            ], "REUTERS", "Tatsuhiro Sakamoto ghi bàn quyết định phút bù giờ 90+1"),
            _slot("sentence", 3, [
                _ddgs("Raphinha Brazil national team angry referee"),
                _ddgs("Referee red card football match argument"),
            ], "AP PHOTO", "Raphinha và HLV Ancelotti nhận thẻ đỏ vì phản ứng trọng tài"),
            _slot("sentence", 4, [
                _url("https://i1-thethao.vnecdn.net/2026/11/15/romario-2-1794709586-3456-1794710297.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=ZWvHHXT7WMZ6fUdNaI8IUg"),
                _ddgs("Romario Brazil legend interview"),
            ], "VNEXPRESS", "Huyền thoại Romario gay gắt yêu cầu Ancelotti rời tuyển Brazil"),
            _slot("sentence", 4, [
                _url("https://i1-thethao.vnecdn.net/2026/11/15/Ancelotti-7834-1794710297.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=BbypnCstAefwwoKAZHu8GA"),
                _ddgs("Carlo Ancelotti press conference Brazil"),
            ], "AP PHOTO", "Tương lai của Carlo Ancelotti tại Selecao bị đặt dấu hỏi lớn"),
        ],
    },
    # 07 (Nam) - Mới
    {
        "id": 7,
        "art_id": "art_07",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Harry Kane cán mốc 126 trận, phá kỷ lục tồn tại 36 năm của tuyển Anh",
        "summary": (
            "Đá chính trong chiến thắng 2-1 trước Croatia tại sân Wembley tối 12 tháng 11 ở Nations League, tiền đạo Harry Kane chính thức chạm mốc 126 lần khoác áo đội tuyển Anh. "
            "Thành tích này giúp chân sút 33 tuổi xô đổ kỷ lục 125 trận của thủ môn huyền thoại Peter Shilton từng đứng vững suốt 36 năm kể từ World Cup 1990. "
            "Trước giờ bóng lăn, Hoàng tử William cùng cựu danh thủ Peter Shilton và đội trưởng Croatia Luka Modric đã trực tiếp trao kỷ vật vinh danh chủ nhân Quả Bóng Vàng trước hàng vạn khán giả. "
            "Không chỉ đi vào lịch sử về số lần ra sân, Harry Kane còn trực tiếp ghi bàn quyết định mang về ba điểm trọn vẹn cho Tam Sư."
        ),
        "source": "VnExpress / UEFA",
        "news_source": "VNEXPRESS / UEFA",
        "credit": "REUTERS / AP / UEFA",
        "slots": [
            _slot("title", 0, [
                _ddgs("Harry Kane England Wembley celebration match"),
                _orther("16.11.2026", "v3_kane_cel.jpg"),
            ], "REUTERS", "Harry Kane rực sáng trong ngày đi vào lịch sử tại Wembley"),
            _slot("title", 0, [
                _ddgs("Wembley Stadium London football match England"),
                _ddgs("Wembley Stadium pitch night England"),
            ], "UEFA", "Thánh địa Wembley tôn vinh kỷ lục gia của đội tuyển Anh"),
            _slot("title", 0, [
                _ddgs("Harry Kane Peter Shilton England caps record"),
                _ddgs("Peter Shilton England legend goalkeeper"),
            ], "AP PHOTO", "Kỷ lục 125 trận tồn tại 36 năm của Peter Shilton bị xô đổ"),
            _slot("sentence", 1, [
                _ddgs("England Croatia Nations League Wembley match action"),
                _ddgs("Harry Kane England captain match action"),
            ], "REUTERS", "Harry Kane ra sân trận thứ 126 gặp Croatia tại Wembley"),
            _slot("sentence", 1, [
                _ddgs("England national football team Wembley fans"),
                _ddgs("England national football team lineup 2026"),
            ], "UEFA", "Khán giả Wembley giương đại kỳ chúc mừng đội trưởng Tam Sư"),
            _slot("sentence", 2, [
                _ddgs("Peter Shilton England goalkeeper 1990 World Cup"),
                _ddgs("Peter Shilton Wembley ceremony"),
            ], "PA / REUTERS", "Huyền thoại Peter Shilton từng giữ kỷ lục từ World Cup 1990"),
            _slot("sentence", 2, [
                _ddgs("Harry Kane England national team jersey tribute"),
                _ddgs("Prince William Harry Kane England Wembley"),
            ], "AP PHOTO", "Hoàng tử William và Peter Shilton chúc mừng cột mốc 126 trận"),
            _slot("sentence", 3, [
                _ddgs("Harry Kane Luka Modric captains handshake"),
                _ddgs("Luka Modric Croatia national team 2026"),
            ], "UEFA", "Đội trưởng Luka Modric của Croatia cũng tặng quà tri ân Kane"),
            _slot("sentence", 3, [
                _ddgs("Harry Kane Ballon dOr England striker portrait"),
                _ddgs("Harry Kane England fans banner Wembley"),
            ], "REUTERS", "Chủ nhân Quả Bóng Vàng bước ra sân cùng các con trong lễ vinh danh"),
            _slot("sentence", 4, [
                _ddgs("Harry Kane England goal celebration Croatia"),
                _orther("16.11.2026", "v3_kane_kick.jpg"),
            ], "AP PHOTO", "Harry Kane trực tiếp ghi bàn quyết định giúp Anh thắng Croatia 2-1"),
        ],
    },
    # 08 (Nữ) - Kế thừa 11.11 ID 1 + 11.11 ID 6 + 13.11 ID 1
    {
        "id": 8,
        "art_id": "art_08",
        "group": "Nhóm: Tâm điểm ngôi sao thế giới",
        "title": "Man Utd sa thải Michael Carrick, chi 10 triệu USD giải phóng HLV Pochettino",
        "summary": (
            "Cuộc khủng hoảng đưa Man Utd xuống nhóm cầm đèn đỏ đã kết thúc bằng quyết định sa thải HLV Michael Carrick chỉ ít ngày sau cuộc họp khẩn tại Monaco của đồng sở hữu Jim Ratcliffe. "
            "Để tìm người thay thế ngay trước đại chiến gặp Liverpool ngày 22 tháng 11, Quỷ đỏ chấp nhận chi 10 triệu USD bồi thường cho Liên đoàn Bóng đá Mỹ để ký hợp đồng với Mauricio Pochettino tới hè năm 2029. "
            "Tuy nhiên, cách ban lãnh đạo để lộ tin cho báo chí ngay lúc Carrick còn chỉ đạo buổi tập và bức tâm thư vỏn vẹn 142 từ đã bị Rio Ferdinand cùng Paul Merson chỉ trích gay gắt. "
            "Trong khi đó, đội trưởng Bruno Fernandes cũng hai lần từ chối gia hạn hợp đồng, báo hiệu những ngày tháng sóng gió phía trước tại Old Trafford."
        ),
        "source": "VnExpress / The Athletic & Sky Sports",
        "news_source": "VNEXPRESS / THE ATHLETIC",
        "credit": "REUTERS / AP / SKY SPORTS",
        "slots": [
            _slot("title", 0, [_cache("candidates_13_11", "poch_0.jpg")], "REUTERS", "Mauricio Pochettino đồng ý tiếp quản ghế nóng Man Utd"),
            _slot("title", 0, [_orther("13.11.2026", "short_1_old_trafford.jpg")], "REUTERS", "Sân Old Trafford bước vào triều đại huấn luyện viên mới"),
            _slot("title", 0, [_orther("13.11.2026", "short_1_carrick_sad.jpg")], "REUTERS", "Michael Carrick chia tay Man Utd sau chuỗi trận bết bát"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_06_3.jpg")], "TALKSPORT", "Sir Jim Ratcliffe triệu tập cuộc họp chốt tương lai ghế nóng"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_01_2.jpg")], "INEOS / MAN UTD", "Ban lãnh đạo Ineos quyết định thay tướng giữa mùa giải"),
            _slot("sentence", 1, [_orther("13.11.2026", "short_1_carrick_0.jpg")], "REUTERS", "HLV Michael Carrick không thể cứu vãn chuỗi thành tích tệ hại"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_06_5.jpg")], "VNEXPRESS / REUTERS", "Man Utd bồi thường 10 triệu USD giải phóng hợp đồng của Pochettino"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_06_6.jpg")], "MARCA / AP", "Chiến lược gia Argentina ký hợp đồng đến hè năm 2029"),
            _slot("sentence", 2, [_orther("13.11.2026", "short_1_poch_tactics.jpg")], "REUTERS", "Pochettino sẽ ra mắt Man Utd ở trận đại chiến gặp Liverpool"),
            _slot("sentence", 3, [_orther("11.11.2026", "Tin_01_8.jpg")], "SKY SPORTS", "Cựu danh thủ Paul Merson cảnh báo nền móng yếu kém của Man Utd"),
            _slot("sentence", 3, [_orther("11.11.2026", "Tin_01_7.jpg")], "SKY SPORTS", "Cách đối xử với Carrick bị Rio Ferdinand chỉ trích dữ dội"),
            _slot("sentence", 4, [_ddgs("Bruno Fernandes Manchester United captain 2026")], "REUTERS", "Đội trưởng Bruno Fernandes hai lần từ chối gia hạn hợp đồng"),
            _slot("sentence", 4, [_orther("11.11.2026", "Tin_06_2.jpg")], "USA TODAY / REUTERS", "Old Trafford đối mặt áp lực tái thiết khổng lồ"),
        ],
    },
    # 09 (Nam) - Kế thừa 10.11 ID 2 + bổ sung ảnh ngang >=800
    {
        "id": 9,
        "art_id": "art_09",
        "group": "Nhóm: Tâm điểm ngôi sao thế giới",
        "title": "FIFPRO World 11 năm 2026: Quả bóng vàng Harry Kane bị loại, Messi lập kỷ lục",
        "summary": (
            "Hiệp hội Cầu thủ Chuyên nghiệp Thế giới vừa công bố Đội hình hay nhất năm 2026 từ lá phiếu của gần 20000 đồng nghiệp toàn cầu. "
            "Cú sốc lớn nhất là việc đương kim Quả Bóng Vàng Harry Kane bị gạch tên khỏi hàng tiền đạo khi xếp sau Erling Haaland với cách biệt sít sao 27,6% so với 28,4%. "
            "Ở chiều ngược lại, huyền thoại Lionel Messi ở tuổi 39 nâng kỷ lục vô tiền khoáng hậu lên 18 lần góp mặt, bỏ xa cột mốc 15 lần của Cristiano Ronaldo. "
            "Hàng công trong mơ còn có Kylian Mbappé dẫn đầu với 46% phiếu bầu và Lamine Yamal, góp phần giúp Tây Ban Nha thống trị danh sách với bốn đại diện sau chức vô địch World Cup 2026."
        ),
        "source": "VnExpress / FIFPRO",
        "news_source": "VNEXPRESS / FIFPRO",
        "credit": "REUTERS / AP / FIFPRO",
        "slots": [
            _slot("title", 0, [_orther("10.11.2026", "Tin_02_12.jpg")], "FIFPRO", "Đội hình tiêu biểu thế giới FIFPRO World 11 năm 2026"),
            _slot("title", 0, [_orther("10.11.2026", "Tin_02_6.jpg")], "AP PHOTO", "Lionel Messi xác lập kỷ lục 18 lần lọt vào đội hình năm"),
            _slot("title", 0, [_orther("10.11.2026", "Tin_02_3.jpg")], "REUTERS", "Harry Kane bất ngờ vắng mặt dù vừa giành Quả Bóng Vàng"),
            _slot("sentence", 1, [_ddgs("FIFPRO World 11 football awards trophy")], "FIFPRO", "Gần 20000 cầu thủ chuyên nghiệp bỏ phiếu bình chọn đội hình hay nhất"),
            _slot("sentence", 1, [_orther("10.11.2026", "Tin_02_9.jpg")], "AP PHOTO", "Các ngôi sao hàng đầu thế giới góp mặt trong đội hình tiêu biểu"),
            _slot("sentence", 2, [_ddgs("Erling Haaland Manchester City celebration 2026")], "REUTERS", "Erling Haaland vượt qua Harry Kane với 28,4% tỷ lệ phiếu bầu"),
            _slot("sentence", 2, [_ddgs("Harry Kane Bayern Munich disappointed match")], "AP PHOTO", "Harry Kane lỡ hẹn cay đắng với khoảng cách chỉ 0,8% phiếu"),
            _slot("sentence", 3, [_ddgs("Lionel Messi Inter Miami Argentina celebration 2026")], "AP PHOTO", "Lionel Messi nối dài kỷ lục lên 18 lần liên tiếp kể từ năm 2007"),
            _slot("sentence", 3, [_ddgs("Cristiano Ronaldo Al Nassr Portugal match")], "REUTERS", "Messi vượt xa kỷ lục 15 lần góp mặt của Cristiano Ronaldo"),
            _slot("sentence", 4, [_orther("10.11.2026", "Tin_02_11.jpg")], "AFP / GETTY IMAGES", "Kylian Mbappé dẫn đầu tuyệt đối lượng phiếu bầu với 46%"),
            _slot("sentence", 4, [_orther("10.11.2026", "Tin_02_8.jpg")], "GETTY IMAGES / LA LIGA", "Lamine Yamal đi vào lịch sử khi hai năm liền góp mặt trước tuổi 20"),
            _slot("sentence", 4, [_orther("16.11.2026", "v3_spain_2024.jpg")], "DAILY SABAH", "Tây Ban Nha áp đảo với 4 ngôi sao vô địch World Cup 2026"),
        ],
    },
    # 10 (Nữ) - Kế thừa 10.11 ID 3
    {
        "id": 10,
        "art_id": "art_10",
        "group": "Nhóm: Tâm điểm ngôi sao thế giới",
        "title": "Trung vệ 19 tuổi Pau Cubarsi đoạt giải Cậu bé Vàng Golden Boy 2026",
        "summary": (
            "Nhật báo thể thao Italy Tuttosport chính thức trao danh hiệu Cậu bé Vàng Golden Boy 2026 cho trung vệ 19 tuổi Pau Cubarsi của Barcelona. "
            "Ngôi sao sinh năm 2007 đã thuyết phục 50 nhà báo châu Âu uy tín sau khi cùng Barcelona vô địch La Liga và đưa đội tuyển Tây Ban Nha đăng quang World Cup 2026. "
            "Vượt qua 24 đối thủ tài năng như Warren Zaire-Emery của PSG, Cubarsi trở thành hậu vệ thứ hai trong 24 kỳ trao giải giành chiến thắng sau Matthijs de Ligt năm 2018. "
            "Thành tích này cũng giúp lò đào tạo La Masia độc chiếm kỷ lục năm lần chiến thắng giải thưởng trẻ danh giá nhất hành tinh sau Messi, Pedri, Gavi và Lamine Yamal."
        ),
        "source": "VnExpress / Tuttosport",
        "news_source": "VNEXPRESS / TUTTOSPORT",
        "credit": "FC BARCELONA / REUTERS / TUTTOSPORT",
        "slots": [
            _slot("title", 0, [_orther("10.11.2026", "Tin_03_5.jpg")], "VNEXPRESS / TUTTOSPORT", "Trung vệ Pau Cubarsi chính thức đoạt giải Golden Boy 2026"),
            _slot("title", 0, [_orther("10.11.2026", "Tin_03_3.jpg")], "REUTERS", "Pau Cubarsi hôn cúp vàng World Cup 2026 cùng Tây Ban Nha"),
            _slot("title", 0, [_orther("10.11.2026", "Tin_03_2.jpg")], "BARCA UNIVERSAL / REUTERS", "Pau Cubarsi chơi chắc chắn nơi hàng thủ Barcelona"),
            _slot("sentence", 1, [_orther("10.11.2026", "Tin_03_8.jpg")], "TUTTOSPORT / FC BARCELONA", "Tuttosport vinh danh tài năng trẻ hay nhất châu Âu năm 2026"),
            _slot("sentence", 1, [_orther("10.11.2026", "Tin_03_7.jpg")], "GOAL.COM / TUTTOSPORT", "Thủ lĩnh trẻ sinh năm 2007 khẳng định đẳng cấp thế giới"),
            _slot("sentence", 2, [_orther("10.11.2026", "Tin_03_4.jpg")], "FC BARCELONA", "Pau Cubarsi ăn mừng ngôi vô địch La Liga cùng Barcelona"),
            _slot("sentence", 2, [_orther("10.11.2026", "Tin_03_12.jpg")], "REUTERS / FIFA", "Pau Cubarsi góp công lớn đưa Tây Ban Nha lên đỉnh World Cup 2026"),
            _slot("sentence", 3, [_orther("10.11.2026", "Tin_03_6.jpg")], "PSG TALK / ICON SPORT", "Cubarsi vượt qua đối thủ sừng sỏ Warren Zaire-Emery trong cuộc bầu chọn"),
            _slot("sentence", 3, [_ddgs("Matthijs de Ligt Golden Boy trophy 2018 Ajax")], "REUTERS", "Trung vệ người Tây Ban Nha tiếp bước Matthijs de Ligt năm 2018"),
            _slot("sentence", 4, [_orther("10.11.2026", "Tin_03_9.jpg")], "FC BARCELONA / TUTTOSPORT", "Lò La Masia nối dài kỷ lục năm lần đoạt giải Cậu bé Vàng"),
            _slot("sentence", 4, [_orther("10.11.2026", "Tin_03_10.jpg")], "REUTERS / FC BARCELONA", "Sau Messi, Pedri, Gavi và Yamal, đến lượt Cubarsi bước lên bục vinh quang"),
            _slot("sentence", 4, [_orther("10.11.2026", "Tin_03_11.jpg")], "ACTION IMAGES / REUTERS", "Tương lai rạng rỡ của hàng phòng ngự đội tuyển Tây Ban Nha"),
        ],
    },
    # 11 (Nam) - Kế thừa 10.11 ID 1
    {
        "id": 11,
        "art_id": "art_11",
        "group": "Nhóm: Tâm điểm ngôi sao thế giới",
        "title": "Jose Mourinho xô đổ kỷ lục tỷ lệ thắng của Pep Guardiola tại La Liga",
        "summary": (
            "Bảng thống kê lịch sử giải vô địch quốc gia Tây Ban Nha La Liga vừa chứng kiến cột mốc kinh điển khi Jose Mourinho vượt qua Pep Guardiola về tỷ lệ thắng cao nhất lịch sử. "
            "Tính trong nhóm các HLV cầm quân từ 100 trận trở lên, chiến lược gia người Bồ Đào Nha đạt tỷ lệ thắng 77%, nhỉnh hơn con số 76,3% của đối thủ truyền kiếp. "
            "Thành tích này nối dài đà thăng hoa khi nhà cầm quân 63 tuổi vừa được vinh danh là HLV xuất sắc nhất tháng 10 sau chuỗi tám trận thắng liên tiếp cùng Real Madrid. "
            "Dù phá vỡ kỷ lục lịch sử của Pep Guardiola, Mourinho vẫn khẳng định ông chỉ hướng tới chiến thắng tiếp theo thay vì sống bằng những con số quá khứ."
        ),
        "source": "VnExpress / La Liga",
        "news_source": "VNEXPRESS / LA LIGA",
        "credit": "AFP / REUTERS / LA LIGA",
        "slots": [
            _slot("title", 0, [_orther("10.11.2026", "Tin_01_1.jpg")], "AFP", "Jose Mourinho vượt qua kình địch Pep Guardiola tại La Liga"),
            _slot("title", 0, [_orther("10.11.2026", "Tin_01_3.jpg")], "REUTERS", "Chiến lược gia Bồ Đào Nha đạt tỷ lệ thắng kỷ lục 77%"),
            _slot("title", 0, [_orther("10.11.2026", "Tin_01_10.jpg")], "REAL MADRID CF", "Real Madrid thăng hoa mạnh mẽ dưới sự dẫn dắt của Mourinho"),
            _slot("sentence", 1, [_orther("10.11.2026", "Tin_01_2.jpg")], "VNEXPRESS / LA LIGA", "Thống kê tỷ lệ thắng ấn tượng nhất lịch sử giải đấu Tây Ban Nha"),
            _slot("sentence", 1, [_orther("10.11.2026", "Tin_01_5.jpg")], "AFP", "Ký ức những màn so tài El Clasico rực lửa giữa hai chiến lược gia"),
            _slot("sentence", 2, [_orther("10.11.2026", "Tin_01_6.jpg")], "ACTION IMAGES / REUTERS", "Tỷ lệ 77% của Mourinho vượt mốc 76,3% của Pep Guardiola"),
            _slot("sentence", 2, [_ddgs("Pep Guardiola Barcelona La Liga coach match")], "AFP", "Kỷ lục cũ của Pep Guardiola tồn tại nhiều năm chính thức bị phá"),
            _slot("sentence", 3, [_orther("10.11.2026", "Tin_01_9.jpg")], "LA LIGA", "Jose Mourinho nhận giải HLV xuất sắc nhất tháng 10 La Liga"),
            _slot("sentence", 3, [_orther("10.11.2026", "Tin_01_11.jpg")], "AP PHOTO", "Chuỗi 8 trận toàn thắng giúp Real Madrid áp đảo giải quốc nội"),
            _slot("sentence", 4, [_orther("10.11.2026", "Tin_01_7.jpg")], "AP PHOTO", "Người Đặc Biệt khẳng định chỉ tập trung cho trận đấu tiếp theo"),
            _slot("sentence", 4, [_orther("10.11.2026", "Tin_01_12.jpg")], "REAL MADRID CF", "Mourinho tiến sát cột mốc top 5 HLV vĩ đại nhất Real Madrid"),
        ],
    },
    # 12 (Nữ) - Kế thừa 12.11 ID 3 (chỉ lấy ảnh ngang, thay thế 6 ảnh dọc)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "Nhóm: Tâm điểm ngôi sao thế giới",
        "title": "Steven Gerrard đánh giá Lamine Yamal xuất sắc hơn Messi và Ronaldo ở tuổi 19",
        "summary": (
            "Chia sẻ trên podcast The Overlap đầu tuần qua, huyền thoại Liverpool Steven Gerrard gây xôn xao khi khẳng định Lamine Yamal xuất sắc hơn cả Lionel Messi lẫn Cristiano Ronaldo ở tuổi 19. "
            "Thống kê chỉ ra rằng trước cột mốc tuổi đôi mươi, ngôi sao của Barcelona đã ghi 73 bàn thắng và có 69 kiến tạo, bỏ xa thành tích ghi 36 bàn của Messi và 22 bàn của Ronaldo cùng độ tuổi. "
            "Thậm chí tổng số 142 lần in dấu giày vào bàn thắng của riêng Yamal còn áp đảo con số 94 nếu cộng thành tích của hai siêu sao đàn anh lại, đi kèm bộ sưu tập 8 danh hiệu lớn gồm Euro 2024 và World Cup 2026. "
            "Dù vậy, Gerrard cảnh báo thử thách thật sự nằm ở khả năng duy trì đỉnh cao suốt hàng chục năm, còn HLV Luis de la Fuente khuyên người hâm mộ tránh gây áp lực quá sớm lên thần đồng này."
        ),
        "source": "VnExpress / The Overlap",
        "news_source": "VNEXPRESS / THE OVERLAP",
        "credit": "WIKIMEDIA COMMONS / UEFA / BARCELONA",
        "slots": [
            _slot("title", 0, [_orther("12.11.2026", "Tin_03_1.jpg")], "FC BARCELONA / ARCHIVE", "Thần đồng Lamine Yamal trong màu áo số 10 Barcelona"),
            _slot("title", 0, [_orther("12.11.2026", "Tin_03_3.jpg")], "WIKIMEDIA COMMONS", "Huyền thoại Liverpool Steven Gerrard gây bão với nhận định mới"),
            _slot("title", 0, [_orther("12.11.2026", "Tin_03_4.jpg")], "WIKIMEDIA COMMONS", "Sự so sánh thú vị với Lionel Messi và Cristiano Ronaldo"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_03_11.jpg")], "WIKIMEDIA COMMONS", "Steven Gerrard đưa ra góc nhìn trên chương trình The Overlap"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_03_12.jpg")], "WIKIMEDIA COMMONS", "Lamine Yamal trình diễn kỹ thuật siêu đẳng ở tuổi 19"),
            _slot("sentence", 2, [_ddgs("Lionel Messi young Barcelona 2006 football")], "WIKIMEDIA COMMONS", "Lionel Messi thời trẻ ghi 36 bàn cho Barcelona đến tuổi 19"),
            _slot("sentence", 2, [_orther("12.11.2026", "Tin_03_6.jpg")], "WIKIMEDIA COMMONS", "Cristiano Ronaldo thời mới nổi ở tuổi 19 có 22 pha lập công"),
            _slot("sentence", 3, [_orther("12.11.2026", "Tin_03_9.jpg")], "UEFA / EURO ARCHIVE", "Yamal vô địch cả Euro 2024 lẫn World Cup 2026 trước tuổi 20"),
            _slot("sentence", 3, [_ddgs("Lamine Yamal Barcelona trophy celebration")], "FC BARCELONA", "Ngôi sao trẻ sở hữu 142 lần in dấu giày cùng 8 chiếc cúp lớn"),
            _slot("sentence", 4, [_orther("12.11.2026", "Tin_03_14.jpg")], "WIKIMEDIA COMMONS", "HLV Hansi Flick trân trọng tài năng và sự trưởng thành của học trò"),
            _slot("sentence", 4, [_orther("12.11.2026", "Tin_03_15.jpg")], "WIKIMEDIA COMMONS", "HLV Luis de la Fuente mong giữ đôi chân học trò trên mặt đất"),
        ],
    },
    # 13 (Nam) - Kế thừa 14.11 ID 1 (có sẵn 13 ảnh ngang HD + Memorial Grayscale)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "Nhóm: Tâm điểm ngôi sao thế giới",
        "title": "Thủ môn Jesus Owono bị phạt kịch khung 12 trận sau bi kịch của De Miguel",
        "summary": (
            "Ngày 13 tháng 11, Liên đoàn Bóng đá Tây Ban Nha chính thức công bố án phạt kịch khung treo giò 12 trận đối với thủ môn Jesus Owono của CLB Andorra. "
            "Theo Điều 102 Quy định Kỷ luật, pha lao ra ngoài vòng cấm dùng lực quá mức ở trận gặp Tenerife ngày 2 tháng 11 đã khiến tiền đạo 30 tuổi Jesus de Miguel ngừng tim ngay trên sân và qua đời sáng hôm sau. "
            "Cảnh sát Tây Ban Nha đã mở cuộc điều tra tư pháp bắt buộc, còn thủ môn Owono đang rơi vào cú sốc tâm lý nặng nề và mong muốn được gửi lời xin lỗi trực tiếp tới gia đình đồng nghiệp xấu số. "
            "Để sẻ chia mất mát, chiến dịch do tiền đạo Fran Sol khởi xướng đã quyên góp 239000 USD hỗ trợ thân nhân, trong khi CLB Tenerife cam kết bảo trợ con gái 16 tháng tuổi của De Miguel đến năm 18 tuổi."
        ),
        "source": "VnExpress / Marca & AS",
        "news_source": "VNEXPRESS / MARCA & AS",
        "credit": "DIARIO DE AVISOS / REUTERS / CD TENERIFE",
        "slots": [
            _slot("title", 0, [_orther("14.11.2026", "s1_collision_1.jpg")], "DIARIO DE AVISOS", "Tình huống va chạm kinh hoàng ở trận Andorra gặp Tenerife"),
            _slot("title", 0, [_orther("14.11.2026", "s1_rfef_hq.jpg")], "MARCA", "Liên đoàn Bóng đá Tây Ban Nha ra án kỷ luật kịch khung"),
            _slot("title", 0, [_orther("14.11.2026", "s1_demiguel_bw1.jpg")], "CD TENERIFE (B&W)", "Tiền đạo xấu số Jesus de Miguel qua đời ở tuổi 30"),
            _slot("sentence", 1, [_orther("14.11.2026", "s1_rfef_ball.jpg")], "ANTENA 3", "Án treo giò 12 trận được tuyên dựa trên Điều 102 Quy định Kỷ luật"),
            _slot("sentence", 1, [_orther("14.11.2026", "s1_owono_andorra.jpg")], "FC ANDORRA", "Thủ môn Jesus Owono nhận mức kỷ luật nghiêm khắc nhất"),
            _slot("sentence", 2, [_orther("14.11.2026", "s1_collision_2.jpg")], "DIARIO DE AVISOS", "Pha băng ra ngoài vòng cấm gây chấn thương trí mạng phút bù giờ"),
            _slot("sentence", 2, [_orther("14.11.2026", "s1_demiguel_bw2.jpg")], "PRENSA IBÉRICA (B&W)", "Nỗi đau tột cùng của bóng đá Tây Ban Nha trước sự ra đi của De Miguel"),
            _slot("sentence", 2, [_orther("14.11.2026", "s1_tenerife_stadium.jpg")], "ESPAÑA ESTADIOS", "Sân Heliodoro Rodríguez López của CLB Tenerife tưởng niệm tiền đạo"),
            _slot("sentence", 3, [_orther("14.11.2026", "s1_funeral_bw.jpg")], "REUTERS (B&W)", "Tang lễ tiễn đưa Jesus de Miguel trong niềm tiếc thương vô hạn"),
            _slot("sentence", 3, [_orther("14.11.2026", "s1_owono_kneel.jpg")], "CAF ONLINE", "Thủ môn Owono suy sụp tâm lý nặng nề sau tai nạn thương tâm"),
            _slot("sentence", 4, [_orther("14.11.2026", "s1_fran_sol.jpg")], "MÁLAGA CF", "Tiền đạo Fran Sol khởi xướng quỹ quyên góp 239000 USD sẻ chia"),
            _slot("sentence", 4, [_orther("14.11.2026", "s1_memorial_flowers_bw.jpg")], "NOGOMANIA (B&W)", "CLB Tenerife cam kết bảo trợ con gái 16 tháng tuổi của De Miguel đến năm 18 tuổi"),
        ],
    },
    # 14 (Nữ) - Mới
    {
        "id": 14,
        "art_id": "art_14",
        "group": "Nhóm: Tâm điểm ngôi sao thế giới",
        "title": "Huyền thoại Ronaldinho tái xuất sân cỏ chuyên nghiệp ở tuổi 46 tại Serie C",
        "summary": (
            "Ở tuổi 46 và sau 11 năm giải nghệ, huyền thoại bóng đá Brazil Ronaldinho vừa chính thức tái xuất sân cỏ chuyên nghiệp trong màu áo CLB Ravenna tại giải hạng Ba Italy Serie C. "
            "Không chỉ đảm nhận vai trò cổ đông kiêm nhà đầu tư của đội bóng, chủ nhân Quả Bóng Vàng 2005 còn đá chính trọn vẹn 45 phút hiệp một trong trận thắng Forli 2-0 tối 15 tháng 11. "
            "Ngay ở phút 36 trên sân Bruno Benelli, Ronaldinho đã để lại dấu ấn đẳng cấp với pha xoay người châm ngòi cho đường phối hợp giúp hậu vệ Giulio Donati sút chéo góc mở tỷ số. "
            "Trước giờ bóng lăn một ngày, danh thủ Brazil cũng gây bão mạng xã hội với video khống chế bóng bổng dính chặt vào chân trên sân tập mượt mà như sản phẩm trí tuệ nhân tạo."
        ),
        "source": "VnExpress / Bongdaplus",
        "news_source": "VNEXPRESS / BONGDAPLUS",
        "credit": "VNEXPRESS / RAVENNA FC / REUTERS",
        "slots": [
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/16/Ronaldinho-JPG-4859-1794767689.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=bphBuF3uzZrh8MSiEzQ9Bg"),
                _ddgs("Ronaldinho Ravenna FC match 2026"),
            ], "RAVENNA FC / VNEXPRESS", "Ronaldinho tái xuất chuyên nghiệp trong màu áo Ravenna"),
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/15/Ronaldinho-4746-1794691968.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=j7on3toIZERyIMw6FmRobg"),
                _ddgs("Ronaldinho training ball control Ravenna"),
            ], "VNEXPRESS", "Nụ cười rạng rỡ và kỹ thuật điêu luyện ở tuổi 46"),
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/16/Ronaldinho-Ravenna-JPG-5585-1794767690.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=gWF8M-VQb0BvNaYpTOpGYg"),
                _ddgs("Ronaldinho playing football Serie C Italy"),
            ], "RAVENNA FC", "Chủ nhân Quả Bóng Vàng 2005 trở lại sau 11 năm giải nghệ"),
            _slot("sentence", 1, [
                _ddgs("Ravenna FC stadium Bruno Benelli Italy"),
                _ddgs("Ronaldinho Serie C Italy Ravenna"),
            ], "RAVENNA FC", "Sân Comunale Bruno Benelli chào đón huyền thoại Brazil"),
            _slot("sentence", 1, [
                _ddgs("Ronaldinho Brazil Ballon dOr legend portrait"),
                _ddgs("Ronaldinho Barcelona legend football"),
            ], "REUTERS", "Bước chạy ngẫu hứng gợi nhớ thời kỳ đỉnh cao của ảo thuật gia"),
            _slot("sentence", 2, [
                _ddgs("Ronaldinho Serie C Ravenna match November 2026"),
                _ddgs("Ravenna FC football team Serie C match"),
            ], "RAVENNA FC", "Ronaldinho vừa làm cổ đông vừa đá chính 45 phút trước Forli"),
            _slot("sentence", 2, [
                _ddgs("Giulio Donati football player Serie C Ravenna"),
                _ddgs("Ravenna FC stadium players celebration"),
            ], "RAVENNA FC", "Đội chủ nhà Ravenna giành chiến thắng thuyết phục 2-0"),
            _slot("sentence", 3, [
                _ddgs("Ronaldinho passing ball football action"),
                _ddgs("Ronaldinho Brazil football dribbling match"),
            ], "REUTERS", "Pha xoay người kiến tạo châm ngòi cho bàn mở tỷ số của Donati"),
            _slot("sentence", 4, [
                _url("https://iv1.vnecdn.net/thethao/images/web/2026/11/15/ronaldinho-gay-sot-voi-pha-do-bong-nhu-san-pham-ai-1794690976.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=dE21nEUSSjqNGaFCaIKClg"),
                _ddgs("Ronaldinho ball control touch skill training"),
            ], "VNEXPRESS / X", "Pha khống chế bóng dính chặt vào chân trên sân tập gây bão toàn cầu"),
        ],
    },
    # 15 (Nam) - Kế thừa 11.11 ID 4 + 13.11 ID 2
    {
        "id": 15,
        "art_id": "art_15",
        "group": "Nhóm: Chuyển động bóng đá Việt Nam",
        "title": "U23 Việt Nam đại thắng Thái Lan 3-0 và áp đảo hạ Singapore 1-0 tại Pleiku",
        "summary": (
            "U23 Việt Nam có màn khởi đầu tưng bừng tại giải giao hữu quốc tế Gia Lai VTV Cup 2026 khi đánh bại đại kình địch U23 Thái Lan 3-0 trên sân vận động Pleiku tối 10 tháng 11. "
            "Chân sút sinh năm 2005 Nguyễn Minh Tâm rực sáng với cú đúp đánh đầu ở hiệp một, trước khi cầu thủ Việt kiều Williams Minh Hoàng ấn định thắng lợi trên chấm phạt đền phút 85. "
            "Hai ngày sau, đoàn quân áo đỏ tiếp tục áp đảo toàn diện với 70% kiểm soát bóng cùng 14 cú dứt điểm và hạ gục U23 Singapore 1-0 nhờ pha giật gót điệu nghệ phút 70 của hậu vệ Nguyễn Bảo Long. "
            "Chứng kiến sức mạnh áp đảo ấy, HLV trưởng Singapore Firdaus Kassim hết lời ca ngợi U23 Việt Nam hoàn toàn đủ năng lực cạnh tranh ngôi vô địch châu Á."
        ),
        "source": "VnExpress / VFF & Thanh Niên",
        "news_source": "VNEXPRESS / VFF",
        "credit": "VNEXPRESS / VFF / DÂN TRÍ",
        "slots": [
            _slot("title", 0, [_orther("11.11.2026", "Tin_04_1.jpg")], "VNEXPRESS / ĐỨC CƯỜNG", "U23 Việt Nam thắng đậm đại kình địch U23 Thái Lan 3-0"),
            _slot("title", 0, [_orther("13.11.2026", "short_2_baolong_goal.jpg")], "VNEXPRESS", "Nguyễn Bảo Long ăn mừng bàn thắng đánh gót vào lưới Singapore"),
            _slot("title", 0, [_orther("13.11.2026", "short_2_u23_celebrate.jpg")], "BAOMOI", "Tinh thần gắn kết bùng nổ của các cầu thủ U23 Việt Nam"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_04_2.jpg")], "VNEXPRESS / ĐỨC CƯỜNG", "Đội hình U23 Việt Nam thi đấu tự tin trên chảo lửa Pleiku"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_04_4.jpg")], "VFF / KHÁNH VY", "Lối chơi phòng ngự phản công sắc bén trước U23 Thái Lan"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_04_8.jpg")], "DÂN TRÍ / TRẦN HẢO", "Tiền đạo Nguyễn Minh Tâm tỏa sáng rực rỡ với cú đúp đánh đầu"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_04_9.jpg")], "DÂN TRÍ / TRẦN HẢO", "Cầu thủ Việt kiều Williams Minh Hoàng ghi bàn thắng lịch sử"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_04_10.jpg")], "DÂN TRÍ / TRẦN HẢO", "Thủ thành Cao Văn Bình giúp U23 Việt Nam giữ sạch lưới"),
            _slot("sentence", 3, [_orther("13.11.2026", "short_2_u23_attack.jpg")], "VNEXPRESS", "Đoàn quân áo đỏ kiểm soát bóng 70% và dứt điểm 14 lần"),
            _slot("sentence", 3, [_orther("13.11.2026", "short_2_baolong_heel.jpg")], "VNEXPRESS", "Pha giật gót điệu nghệ của Nguyễn Bảo Long ở phút 70"),
            _slot("sentence", 3, [_orther("13.11.2026", "short_2_quocviet_assist.jpg")], "VNEXPRESS", "Nguyễn Quốc Việt kiến tạo chuẩn xác cho đồng đội lập công"),
            _slot("sentence", 4, [_orther("13.11.2026", "short_2_kassim_press.jpg")], "VNEXPRESS", "HLV Firdaus Kassim đánh giá rất cao sức mạnh của U23 Việt Nam"),
            _slot("sentence", 4, [_orther("13.11.2026", "short_2_hlv_vinh_smile.jpg")], "VOV", "HLV Đinh Hồng Vinh hài lòng với màn trình diễn toàn diện của học trò"),
        ],
    },
    # 16 (Nữ) - Mới (VnExpress & Thanh Niên)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "Nhóm: Chuyển động bóng đá Việt Nam",
        "title": "Hòa kịch tính Qatar 1-1, U23 Việt Nam vô địch Gia Lai VTV Cup và nhận 2,6 tỷ đồng",
        "summary": (
            "Trong trận quyết đấu tối 14 tháng 11 trên sân Pleiku, U23 Việt Nam trải qua 90 phút căng thẳng trước U23 Qatar vượt trội về thể hình và bị dẫn trước ngay trong hiệp một. "
            "Bước sang đầu hiệp hai, tiền đạo Nguyễn Minh Tâm tỏa sáng đúng lúc ghi bàn gỡ hòa quý giá giúp thầy trò HLV Đinh Hồng Vinh bảo toàn tỷ số 1-1 chung cuộc. "
            "Kết quả bất bại với hai thắng một hòa, ghi năm bàn và chỉ thủng lưới một lần giúp U23 Việt Nam hiên ngang đăng quang ngôi vô địch Gia Lai VTV Cup 2026. "
            "Cá nhân Minh Tâm thâu tóm cú đúp danh hiệu Cầu thủ xuất sắc nhất và Vua phá lưới, còn toàn đội đón nhận khoản thưởng 2,6 tỷ đồng tương đương 100000 USD từ bầu Đức."
        ),
        "source": "VnExpress / Thanh Niên",
        "news_source": "VNEXPRESS / THANH NIÊN",
        "credit": "VNEXPRESS / ĐỨC ĐỒNG / THANH NIÊN",
        "slots": [
            _slot("title", 0, [
                _url("https://images2.thanhnien.vn/528068263637045248/2026/11/15/tnw-dll08092-17947212006981483619589.jpg"),
            ], "THANH NIÊN", "U23 Việt Nam nâng cao chiếc cúp vô địch Gia Lai VTV Cup 2026"),
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/14/wm1-wm1-1794661885290-527379806675-3211-2847-1794667409.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=208JArjHBp179CZnXcxmsA"),
            ], "ĐỨC ĐỒNG / VNEXPRESS", "Nguyễn Minh Tâm ăn mừng bàn thắng quý hơn vàng vào lưới Qatar"),
            _slot("title", 0, [
                _url("https://images2.thanhnien.vn/528068263637045248/2026/11/15/tnw-dln06057-17947212738271513462690.jpg"),
            ], "THANH NIÊN", "Niềm vui vỡ òa của thầy trò HLV Đinh Hồng Vinh tại Pleiku"),
            _slot("sentence", 1, [
                _url("https://i1-thethao.vnecdn.net/2026/11/14/wm1-wm1-1794658997968-g75896842860-4700-1834-1794667410.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=g7t5jkTJJboqjE4f7ZQpjQ"),
            ], "ĐỨC ĐỒNG / VNEXPRESS", "U23 Qatar gây ra nhiều khó khăn nhờ ưu thế thể lực và pressing"),
            _slot("sentence", 1, [
                _url("https://i1-thethao.vnecdn.net/2026/11/14/wm1-wm1-1794667514287-527379806675-5984-1175-1794667680.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=mFrKHU6FC2C6SG7HP1lKxQ"),
            ], "ĐỨC ĐỒNG / VNEXPRESS", "Các cầu thủ trẻ Việt Nam chiến đấu kiên cường suốt 90 phút"),
            _slot("sentence", 2, [
                _url("https://images2.thanhnien.vn/528068263637045248/2026/11/15/tnw-dln06047-17947213242061540858513.jpg"),
            ], "THANH NIÊN", "Minh Tâm lập công đầu hiệp hai đưa trận đấu về thế cân bằng 1-1"),
            _slot("sentence", 2, [
                _url("https://images2.thanhnien.vn/528068263637045248/2026/11/15/tnw-dln06037-1794721369116945897478.jpg"),
            ], "THANH NIÊN", "Hàng thủ bọc lót kín kẽ bảo toàn tỷ số đến hết trận"),
            _slot("sentence", 3, [
                _url("https://images2.thanhnien.vn/528068263637045248/2026/11/15/tnw-dln06027-17947214070261033503566.jpg"),
            ], "THANH NIÊN", "U23 Việt Nam bất bại cả ba trận để lên ngôi vô địch xứng đáng"),
            _slot("sentence", 3, [
                _url("https://images2.thanhnien.vn/528068263637045248/2026/11/15/tnw-dln06019-1794721502900214350920.jpg"),
            ], "THANH NIÊN", "Lễ trao cúp vô địch rực rỡ trên sân vận động Pleiku"),
            _slot("sentence", 4, [
                _url("https://images2.thanhnien.vn/528068263637045248/2026/11/15/tnw-dll09892-17947215672991806323029.jpg"),
            ], "THANH NIÊN", "Bầu Đức trao thưởng nóng 2,6 tỷ đồng cho nhà vô địch U23 Việt Nam"),
            _slot("sentence", 4, [
                _url("https://images2.thanhnien.vn/528068263637045248/2026/11/15/tnw-dll09917-1794721567809276277708.jpg"),
            ], "THANH NIÊN", "Nguyễn Minh Tâm nhận cú đúp danh hiệu cá nhân xuất sắc nhất giải"),
        ],
    },
    # 17 (Nam) - Kế thừa 12.11 ID 1 + ảnh VnExpress mới
    {
        "id": 17,
        "art_id": "art_17",
        "group": "Nhóm: Chuyển động bóng đá Việt Nam",
        "title": "Tuyển Việt Nam thắng Đài Loan 2-0, lên hạng 98 FIFA và hủy giao hữu Nhật Bản",
        "summary": (
            "Tối 11 tháng 11 tại sân Thiên Trường, đội tuyển Việt Nam đánh bại Đài Loan 2-0 trong trận giao hữu khi HLV Kim Sang-sik trao cơ hội đá chính cho năm tân binh trẻ. "
            "Tiền đạo nhập tịch Olaha Mạnh Đức lập tức tỏa sáng ghi bàn mở tỷ số ngay trong trận ra mắt, trước khi Nguyễn Đình Bắc ấn định chiến thắng 2-0 ở phút 58 sau pha chọc khe của Khuất Văn Khang. "
            "Kết quả tích cực giúp đoàn quân áo đỏ vươn lên vị trí thứ 98 trên bảng xếp hạng FIFA, tạo bước đệm tinh thần tốt trước trận tranh ngôi vô địch Casper Cup gặp Kyrgyzstan tối 17 tháng 11. "
            "Ở chiều ngược lại, Liên đoàn Bóng đá Nhật Bản bất ngờ thông báo hủy trận giao hữu với Việt Nam ngày 30 tháng 12 do Asian Cup 2027 bị hoãn sang cuối năm 2027."
        ),
        "source": "VnExpress / Thanh Niên",
        "news_source": "VNEXPRESS / THANH NIÊN",
        "credit": "VNEXPRESS / HIẾU LƯƠNG",
        "slots": [
            _slot("title", 0, [_orther("12.11.2026", "Tin_01_1.jpg")], "VNEXPRESS", "Các tuyển thủ trẻ và Olaha Mạnh Đức tỏa sáng trước Đài Loan"),
            _slot("title", 0, [_orther("12.11.2026", "Tin_01_7.jpg")], "VNEXPRESS", "Tiền đạo nhập tịch Olaha Mạnh Đức dứt điểm mở tỷ số"),
            _slot("title", 0, [_orther("12.11.2026", "Tin_01_10.jpg")], "VNEXPRESS", "Nguyễn Đình Bắc ăn mừng bàn ấn định chiến thắng 2-0"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_01_2.jpg")], "VNEXPRESS", "Đội tuyển Việt Nam hát Quốc ca trước trận đấu trên sân Thiên Trường"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_01_5.jpg")], "VNEXPRESS", "HLV Kim Sang-sik mạnh dạn trao cơ hội cho năm tân binh đá chính"),
            _slot("sentence", 2, [_orther("12.11.2026", "Tin_01_6.jpg")], "VNEXPRESS", "Tân binh Trần Ngọc Sơn thi đấu năng nổ bên hành lang cánh"),
            _slot("sentence", 2, [_orther("12.11.2026", "Tin_01_9.jpg")], "VNEXPRESS", "Nguyễn Đình Bắc đột phá tốc độ uy hiếp khung thành Đài Loan"),
            _slot("sentence", 3, [_orther("12.11.2026", "Tin_01_12.jpg")], "VNEXPRESS", "Đội tuyển Việt Nam vươn lên hạng 98 thế giới trên bảng xếp hạng FIFA"),
            _slot("sentence", 3, [_orther("12.11.2026", "Tin_01_14.jpg")], "VNEXPRESS", "Toàn đội sẵn sàng bước vào trận đấu gặp Kyrgyzstan ngày 17 tháng 11"),
            _slot("sentence", 4, [_url("https://i1-thethao.vnecdn.net/2026/11/13/wm1-wm1-12-1794566956-4924-1794566992.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=ub-gZT0sQWjik47cH_qOCg"), _orther("12.11.2026", "Tin_01_3.jpg")], "VNEXPRESS / HIẾU LƯƠNG", "Liên đoàn Bóng đá Nhật Bản thông báo hủy trận giao hữu cuối năm"),
            _slot("sentence", 4, [_url("https://i1-thethao.vnecdn.net/2026/11/13/wm1-b73i3145-1794566876-6796-1794566992.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=GAG75ZHiW7e1M4bDz2ySxg"), _orther("12.11.2026", "Tin_01_13.jpg")], "VNEXPRESS / HIẾU LƯƠNG", "Việc Asian Cup 2027 bị hoãn khiến kế hoạch thi đấu cuối năm thay đổi"),
        ],
    },
    # 18 (Nữ) - Kế thừa 12.11 ID 4
    {
        "id": 18,
        "art_id": "art_18",
        "group": "Nhóm: Chuyển động bóng đá Việt Nam",
        "title": "Mỹ rút khỏi U17 World Cup 2026, FIFA chốt đội thay và công bố danh sách U17 Việt Nam",
        "summary": (
            "Ngày 11 tháng 11, Liên đoàn Bóng đá Mỹ bất ngờ tuyên bố rút đội tuyển U17 nam khỏi vòng chung kết World Cup 2026 tại Qatar do lo ngại an ninh khu vực Trung Đông, đối mặt án phạt tối thiểu 20000 franc Thụy Sĩ. "
            "Hai ngày sau, FIFA chính thức chỉ định đội tuyển U17 Cộng hòa Dominica thay thế vào bảng J để giữ nguyên thể thức 48 đội chia 12 bảng đấu. "
            "Nhờ quyết định kịp thời này, lịch thi đấu và cục diện bảng G của U17 Việt Nam cùng Bỉ, New Zealand và Mali hoàn toàn không bị xáo trộn. "
            "Tối 14 tháng 11, FIFA đã công bố danh sách chính thức 21 cầu thủ U17 Việt Nam do HLV Cristiano Roland dẫn dắt, sẵn sàng cho hành trình lịch sử từ ngày 20 tháng 11 tại Doha."
        ),
        "source": "VnExpress / Thanh Niên",
        "news_source": "VNEXPRESS / THANH NIÊN",
        "credit": "VNEXPRESS / FIFA / WIKIMEDIA COMMONS",
        "slots": [
            _slot("title", 0, [_orther("12.11.2026", "Tin_04_1.jpg")], "VNEXPRESS / AFP", "Đội tuyển U17 Mỹ đột ngột rút khỏi World Cup 2026 tại Qatar"),
            _slot("title", 0, [_orther("12.11.2026", "Tin_04_10.jpg")], "VNEXPRESS", "Thầy trò HLV Cristiano Roland tập trung cao độ tại Doha"),
            _slot("title", 0, [_orther("12.11.2026", "Tin_04_3.jpg")], "WIKIMEDIA COMMONS", "Sân vận động tại Qatar nơi tổ chức ngày hội bóng đá trẻ thế giới"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_04_2.jpg")], "WIKIMEDIA COMMONS", "Liên đoàn Bóng đá Mỹ hủy kế hoạch tập huấn chỉ năm ngày sau khi chốt quân"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_04_4.jpg")], "WIKIMEDIA COMMONS", "Trụ sở FIFA xử lý khẩn biến cố rút lui sát ngày khai mạc"),
            _slot("sentence", 2, [_orther("12.11.2026", "Tin_04_6.jpg")], "WIKIMEDIA COMMONS", "FIFA chọn Cộng hòa Dominica thuộc khu vực Bắc Trung Mỹ thay thế"),
            _slot("sentence", 2, [_orther("12.11.2026", "Tin_04_7.jpg")], "WIKIMEDIA COMMONS", "Giải đấu giữ nguyên thể thức 48 đội tuyển chia làm 12 bảng"),
            _slot("sentence", 3, [_orther("12.11.2026", "Tin_04_12.jpg")], "VNEXPRESS", "Bảng G của U17 Việt Nam giữ nguyên ổn định lịch thi đấu"),
            _slot("sentence", 3, [_orther("12.11.2026", "Tin_04_8.jpg")], "WIKIMEDIA COMMONS", "U17 Việt Nam chạm trán các đối thủ Bỉ, New Zealand và Mali"),
            _slot("sentence", 4, [_orther("12.11.2026", "Tin_04_11.jpg")], "VNEXPRESS", "Danh sách 21 tuyển thủ trẻ Việt Nam sẵn sàng làm nên lịch sử"),
            _slot("sentence", 4, [_orther("12.11.2026", "Tin_04_13.jpg")], "VNEXPRESS", "HLV Cristiano Roland rèn chiến thuật trên cụm sân Học viện Aspire"),
        ],
    },
    # 19 (Nam) - Kế thừa 11.11 ID 5
    {
        "id": 19,
        "art_id": "art_19",
        "group": "Nhóm: Chuyển động bóng đá Việt Nam",
        "title": "VFF đình chỉ vô thời hạn nhóm cầu thủ CLB Long An dàn xếp tỷ số",
        "summary": (
            "Ban kỷ luật VFF vừa ban hành quyết định đình chỉ thi đấu vô thời hạn đối với sáu cá nhân liên quan đến vụ án dàn xếp tỷ số tại CLB Long An. "
            "Án phạt áp dụng cho bốn cầu thủ Nguyễn Thanh Hải, Nguyễn Anh Tài, Lê Văn Hưng, Bùi Hoàng Mỹ cùng cặp song sinh cựu tuyển thủ Hoàng Nhật Nam và Hoàng Danh Ngọc. "
            "Theo hồ sơ từ Cục Cảnh sát hình sự Bộ Công an, nhóm cầu thủ này bị cáo buộc móc nối đá dưới sức ở các trận thua Quy Nhơn 1-4 và Nam Định 0-2 nhằm trục lợi cá cược. "
            "Cùng tuần qua, Liên đoàn Bóng rổ Việt Nam cũng mạnh tay đình chỉ thi đấu các vận động viên vi phạm tiêu cực, khẳng định quyết tâm làm sạch thể thao nước nhà."
        ),
        "source": "VnExpress / VFF & Dân Trí",
        "news_source": "VNEXPRESS / VFF",
        "credit": "VFF / BỘ CÔNG AN / VNEXPRESS",
        "slots": [
            _slot("title", 0, [_orther("11.11.2026", "Tin_05_3.jpg")], "VFF", "VFF ra án phạt nghiêm khắc đối với nhóm cầu thủ tiêu cực"),
            _slot("title", 0, [_orther("11.11.2026", "Tin_05_1.jpg")], "CỤC CẢNH SÁT HÌNH SỰ / VNEXPRESS", "Hồ sơ điều tra vụ án dàn xếp tỷ số tại giải Hạng Nhất"),
            _slot("title", 0, [_orther("11.11.2026", "Tin_05_4.jpg")], "VFF", "Cuộc chiến chống tiêu cực nhằm giữ sự trong sạch cho bóng đá Việt Nam"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_05_5.jpg")], "VFF", "Ban kỷ luật VFF quyết định đình chỉ vô thời hạn sáu cá nhân"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_05_2.jpg")], "VNEXPRESS", "CLB Long An chủ động thanh lý hợp đồng nhóm cầu thủ vi phạm"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_05_6.jpg")], "THỂ THAO VĂN HÓA", "Cặp song sinh Hoàng Nhật Nam và Hoàng Danh Ngọc nằm trong danh sách bị phạt"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_05_9.jpg")], "THANH NIÊN", "Các cầu thủ nhúng chàm đánh mất sự nghiệp vì cá độ bất hợp pháp"),
            _slot("sentence", 3, [_orther("11.11.2026", "Tin_05_7.jpg")], "BỘ CÔNG AN", "Cục Cảnh sát hình sự khởi tố 21 bị can trong đường dây dàn xếp tỷ số"),
            _slot("sentence", 3, [_orther("11.11.2026", "Tin_05_8.jpg")], "BÁO GIAO THÔNG / BỘ CÔNG AN", "Cơ quan điều tra xác định hành vi cố tình thi đấu dưới sức trục lợi"),
            _slot("sentence", 4, [_orther("11.11.2026", "Tin_05_11.jpg")], "SÀI GÒN GIẢI PHÓNG", "Bóng đá và bóng rổ Việt Nam đồng loạt xử lý nghiêm hành vi bán độ"),
            _slot("sentence", 4, [_orther("11.11.2026", "Tin_05_14.jpg")], "LAO ĐỘNG", "Thông điệp răn đe mạnh mẽ hướng tới môi trường thi đấu minh bạch"),
        ],
    },
    # 20 (Nữ) - Kế thừa 12.11 ID 2 (chỉ dùng ảnh ngang sạch, tránh logo CLB Tin_02_12)
    {
        "id": 20,
        "art_id": "art_20",
        "group": "Nhóm: Chuyển động bóng đá Việt Nam",
        "title": "HLV Park Hang-seo bị phạt tại Thái Lan dù bảo vệ học trò bị miệt thị chủng tộc",
        "summary": (
            "Ngày 11 tháng 11, Ban kỷ luật Liên đoàn Bóng đá Thái Lan bất ngờ ra án cấm chỉ đạo hai trận và phạt tiền hơn 13000 baht đối với HLV Park Hang-seo. "
            "Sự việc bắt nguồn ở cuối trận Kanchanaburi hòa Pattaya United 2-2 tại giải hạng Nhì Thái Lan khi khán giả quá khích buông lời miệt thị chủng tộc nhắm vào ông Park và tiền đạo John Baggio. "
            "Vì bức xúc bước vào khu vực không được phép để bênh vực học trò, nhà cầm quân người Hàn Quốc bị quy lỗi làm gia tăng căng thẳng dù chủ nhà Pattaya cũng bị phạt 40000 baht. "
            "Khẳng định không bao giờ im lặng trước hành vi lăng mạ học trò, HLV Park Hang-seo vừa cùng Kanchanaburi đánh bại Nakhon Ratchasima 1-0 để vươn lên hạng tư."
        ),
        "source": "VnExpress / Dân Trí",
        "news_source": "VNEXPRESS / DÂN TRÍ",
        "credit": "THANH NIÊN / BANGKOK POST / KANCHANABURI FC",
        "slots": [
            _slot("title", 0, [_orther("12.11.2026", "Tin_02_1.jpg")], "BERNY ZIMMER", "HLV Park Hang-seo giữa tâm bão án phạt tại Thái Lan"),
            _slot("title", 0, [_orther("12.11.2026", "Tin_02_7.jpg")], "THANH NIÊN", "Chiến lược gia Hàn Quốc phản ứng quyết liệt bảo vệ học trò"),
            _slot("title", 0, [_orther("12.11.2026", "Tin_02_5.jpg")], "ZNEWS", "CLB Kanchanaburi thi đấu ấn tượng tại Thai League 2"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_02_3.jpg")], "FA THAILAND", "Ban kỷ luật Thái Lan ban hành án treo giò hai trận đối với ông Park"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_02_11.jpg")], "BÁO AN GIANG", "Án phạt tiền hơn 13000 baht gây nhiều tranh luận trong giới chuyên môn"),
            _slot("sentence", 2, [_orther("12.11.2026", "Tin_02_6.jpg")], "BANGKOK POST", "Tiền đạo John Baggio trở thành mục tiêu lời lẽ phân biệt chủng tộc"),
            _slot("sentence", 2, [_orther("12.11.2026", "Tin_02_9.jpg")], "DER FARANG", "Khán đài sân Pattaya nơi xảy ra sự cố thóa mạ từ khán giả"),
            _slot("sentence", 3, [_orther("12.11.2026", "Tin_02_8.jpg")], "KANCHANABURI POWER FC", "Ban huấn luyện và cầu thủ Kanchanaburi phản đối thái độ phân biệt đối xử"),
            _slot("sentence", 3, [_ddgs("Thai League football referee match sideline")], "BANGKOK POST", "Chủ nhà Pattaya United cũng nhận án phạt 40000 baht từ ban tổ chức"),
            _slot("sentence", 4, [_orther("12.11.2026", "Tin_02_13.jpg")], "KANCHANABURI FC", "Cổ động viên địa phương đồng lòng ủng hộ tinh thần của HLV Park Hang-seo"),
            _slot("sentence", 4, [_orther("12.11.2026", "Tin_02_14.jpg")], "KANCHANABURI FC", "Kanchanaburi giành chiến thắng 1-0 vươn lên vị trí thứ tư trên bảng xếp hạng"),
        ],
    },
    # 21 (Nam) - Kế thừa 11.11 ID 3
    {
        "id": 21,
        "art_id": "art_21",
        "group": "Nhóm: Tinh hoa thể thao thế giới",
        "title": "Xạ thủ Trịnh Thu Vinh đoạt HCB thế giới, giành vé Olympic 2028 đầu tiên cho Việt Nam",
        "summary": (
            "Thể thao Việt Nam đón tin vui rạng rỡ từ Doha, Qatar khi nữ xạ thủ Trịnh Thu Vinh trở thành VĐV đầu tiên của nước nhà giành vé dự Thế vận hội Olympic Los Angeles 2028. "
            "Tại Giải vô địch bắn súng thế giới 2026, tuyển thủ 26 tuổi đoàn Công an Nhân dân thi đấu bản lĩnh để vượt qua vòng loại với 585 điểm. "
            "Trong chung kết nội dung 25m súng ngắn thể thao nữ, Thu Vinh liên tục dẫn đầu qua chín loạt bắn trước khi giành HCB sát nút 43-44 trước nhà vô địch Hàn Quốc Yang Ji-in. "
            "Cùng tấm HCĐ đồng đội nữ, chiến tích vang dội giúp bắn súng Việt Nam thăng tiến lên hạng 17 thế giới và mở ra niềm hy vọng lớn tại đấu trường Olympic sắp tới."
        ),
        "source": "VnExpress / ISSF",
        "news_source": "VNEXPRESS / ISSF",
        "credit": "VNEXPRESS / ISSF / REUTERS",
        "slots": [
            _slot("title", 0, [_orther("11.11.2026", "Tin_03_1.jpg")], "VNEXPRESS / ISSF", "Xạ thủ Trịnh Thu Vinh trên bục nhận HCB thế giới tại Qatar"),
            _slot("title", 0, [_orther("11.11.2026", "Tin_03_2.jpg")], "VNEXPRESS / ISSF", "Trịnh Thu Vinh giành suất đầu tiên dự Olympic 2028 cho Việt Nam"),
            _slot("title", 0, [_orther("11.11.2026", "Tin_03_12.jpg")], "LA28 / IOC", "Tấm vé chính thức hướng tới Thế vận hội Los Angeles 2028"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_03_3.jpg")], "HIẾU LƯƠNG / VNEXPRESS", "Niềm tự hào rạng ngời của thể thao Việt Nam tại Doha"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_03_10.jpg")], "ISSF / LUSAIL", "Trường bắn hiện đại tại Lusail, Qatar đăng cai giải thế giới"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_03_4.jpg")], "REUTERS", "Nữ tuyển thủ sinh năm 2000 giữ tâm lý vững vàng ở vòng loại"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_03_5.jpg")], "BÁO VĂN HÓA", "Thu Vinh thi đấu tập trung cao độ qua từng loạt đạn áp lực"),
            _slot("sentence", 3, [_orther("11.11.2026", "Tin_03_6.jpg")], "YONHAP / ISSF", "Màn so tài đỉnh cao cùng đối thủ Hàn Quốc Yang Ji-in"),
            _slot("sentence", 3, [_orther("11.11.2026", "Tin_03_8.jpg")], "AP PHOTO", "Khoảnh khắc căng thẳng quyết định ở loạt bắn cuối 43-44"),
            _slot("sentence", 4, [_orther("11.11.2026", "Tin_03_7.jpg")], "BÁO LAO ĐỘNG", "Đội tuyển bắn súng nữ Việt Nam giành thêm HCĐ đồng đội"),
            _slot("sentence", 4, [_orther("11.11.2026", "Tin_03_9.jpg")], "VNEXPRESS / VASC", "Bắn súng Việt Nam vươn lên vị trí thứ 17 trên bảng xếp hạng thế giới"),
        ],
    },
    # 22 (Nữ) - Kế thừa 14.11 ID 3 + bổ sung Lại Lý Huynh á quân cờ chớp
    {
        "id": 22,
        "art_id": "art_22",
        "group": "Nhóm: Tinh hoa thể thao thế giới",
        "title": "Phan Huy Hoàng 18 tuổi đoạt HCV cờ tướng thế giới, Lại Lý Huynh giành Á quân cờ chớp",
        "summary": (
            "Tại Giải cờ tướng thế giới mở rộng 2026 ở Singapore, kỳ thủ 18 tuổi Phan Huy Hoàng gây chấn động khi giành HCV cá nhân nội dung đồng đội nam với thành tích bất bại 13 điểm. "
            "Được tin tưởng đánh chính thay đàn anh Lại Lý Huynh, tài năng trẻ đến từ Thành phố Hồ Chí Minh xuất sắc vượt qua hàng loạt đại cao thủ Trung Quốc như Lưu Bách Hoành và Mạnh Phồn Duệ. "
            "Cùng tấm HCĐ cá nhân của Nguyễn Minh Nhật Quang, đoàn Việt Nam mang về hai tấm HCB đồng đội nam và nữ nhờ công Đàm Thị Thùy Dung và Nguyễn Hoàng Yến. "
            "Tiếp nối thành công đó vào ngày 15 tháng 11, kỳ thủ số một Việt Nam Lại Lý Huynh cũng xuất sắc giành thêm hai danh hiệu Á quân thế giới ở cả hai nội dung cờ nhanh và cờ chớp."
        ),
        "source": "VnExpress / Thanh Niên",
        "news_source": "VNEXPRESS / THANH NIÊN",
        "credit": "LIÊN ĐOÀN CỜ TƯỚNG VN / THANH NIÊN",
        "slots": [
            _slot("title", 0, [_orther("14.11.2026", "s3_hoang_podium.jpg")], "LIÊN ĐOÀN CỜ TƯỚNG VN", "Phan Huy Hoàng nhận HCV cá nhân giải cờ tướng thế giới"),
            _slot("title", 0, [_cache("candidates_14_11", "t3_ddg_02.jpg")], "THANH NIÊN", "Lại Lý Huynh tỏa sáng giành ngôi Á quân cờ nhanh và cờ chớp"),
            _slot("title", 0, [_orther("14.11.2026", "s3_xiangqi_boards.jpg")], "BÁO HẢI DƯƠNG", "Không khí đấu trí căng thẳng tại Singapore"),
            _slot("sentence", 1, [_orther("14.11.2026", "s3_podium_wide.jpg")], "LIÊN ĐOÀN CỜ TƯỚNG VN", "Kỳ thủ 18 tuổi bất bại sáu thắng một hòa đạt 13 điểm"),
            _slot("sentence", 1, [_cache("candidates_14_11", "t3_ex_01.jpg")], "THANH NIÊN", "Phan Huy Hoàng tạo bước ngoặt lịch sử cho cờ tướng trẻ Việt Nam"),
            _slot("sentence", 2, [_orther("14.11.2026", "s3_luubachhoanh_1.jpg")], "WEBCOTUONG", "Huy Hoàng xuất sắc cầm hòa nhà vô địch châu Á Lưu Bách Hoành"),
            _slot("sentence", 2, [_orther("14.11.2026", "s3_luubachhoanh_2.jpg")], "WEBCOTUONG", "Tài năng Việt Nam xếp trên ba cao thủ hàng đầu Trung Quốc"),
            _slot("sentence", 3, [_orther("14.11.2026", "s3_nhatquang.jpg")], "THANH NIÊN", "Nguyễn Minh Nhật Quang giành HCĐ giúp tuyển nam đoạt HCB đồng đội"),
            _slot("sentence", 3, [_orther("14.11.2026", "s3_thuydung.jpg")], "NGƯỜI LAO ĐỘNG", "Đàm Thị Thùy Dung góp công đưa tuyển nữ Việt Nam đoạt HCB"),
            _slot("sentence", 3, [_orther("14.11.2026", "s3_hoangyen_podium.jpg")], "NGƯỜI LAO ĐỘNG", "Nguyễn Hoàng Yến cùng đồng đội trên bục nhận huy chương"),
            _slot("sentence", 4, [
                _url("https://images2.thanhnien.vn/528068263637045248/2026/11/15/90718341514106604775019122839922493361294950n-1-17947176765441234760734.jpg"),
                _orther("14.11.2026", "s3_lailyhuynh_match.jpg"),
            ], "THANH NIÊN / VOV", "Lại Lý Huynh vào chung kết cờ chớp thế giới đối đầu Mạnh Phồn Duệ"),
            _slot("sentence", 4, [_cache("candidates_14_11", "t3_ddg_09.jpg")], "THANH NIÊN", "Lại Lý Huynh mang về thêm hai tấm HCB cờ nhanh và cờ chớp thế giới"),
        ],
    },
    # 23 (Nam) - Kế thừa 12.11 ID 5 + ảnh mới Quang Liêm & Carlsen
    {
        "id": 23,
        "art_id": "art_23",
        "group": "Nhóm: Tinh hoa thể thao thế giới",
        "title": "Lê Quang Liêm thắng ván cờ chính xác 99% và bất bại vòng bảng giải toàn năng thế giới",
        "summary": (
            "Tại giải cờ vua toàn năng thế giới 2026 có quỹ thưởng 650000 USD ở Budapest, siêu đại kiện tướng Lê Quang Liêm gây tiếng vang lớn với ván thắng Vladislav Artemiev đạt độ chính xác 99%. "
            "Kỳ thủ số một Việt Nam tiếp tục phong độ chói sáng khi đánh bại kỳ thủ hạng 9 thế giới Vincent Keymer ở các lượt đấu giữa tuần. "
            "Sau hai ván hòa bản lĩnh trước hạt giống hàng đầu Fabiano Caruana tối 14 tháng 11, Quang Liêm khép lại vòng bảng với thành tích bất bại 14 điểm, đứng nhì bảng B tử thần. "
            "Ở chiều ngược lại, vua cờ Magnus Carlsen bất ngờ sa sút khi để thua Haik Martirosyan và rơi xuống mức Elo 2807, thấp nhất trong vòng 17 năm qua."
        ),
        "source": "VnExpress / Total Chess",
        "news_source": "VNEXPRESS / TOTAL CHESS",
        "credit": "TOTAL CHESS / MARIA EMELIANOVA / VNEXPRESS",
        "slots": [
            _slot("title", 0, [_orther("12.11.2026", "Tin_05_1.jpg")], "VNEXPRESS / TOTAL CHESS", "Lê Quang Liêm thi đấu thăng hoa tại giải toàn năng thế giới 2026"),
            _slot("title", 0, [_url("https://i1-thethao.vnecdn.net/2026/11/15/quang-lie-m-1794693121-1396-1794693184.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=3MZH-V1RSHUMFUwnUXvfbw")], "VNEXPRESS / TOTAL CHESS", "Kỳ thủ số một Việt Nam duy trì mạch bất bại trước các cao thủ hàng đầu"),
            _slot("title", 0, [_orther("12.11.2026", "Tin_05_4.jpg")], "VNEXPRESS / TOTAL CHESS", "Toàn cảnh sân khấu tranh tài giải cờ vua 650000 USD tại Budapest"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_05_2.jpg")], "VNEXPRESS", "Quang Liêm tung nước thí mã đỉnh cao đánh bại Vladislav Artemiev"),
            _slot("sentence", 1, [_orther("12.11.2026", "Tin_05_3.jpg")], "WIKIMEDIA COMMONS", "Nước cờ đạt độ chính xác 99% sau 32 nước của kỳ thủ Việt Nam"),
            _slot("sentence", 2, [_ddgs("Vincent Keymer chess grandmaster tournament")], "WIKIMEDIA COMMONS", "Siêu đại kiện tướng Đức Vincent Keymer nhận thất bại trước Quang Liêm"),
            _slot("sentence", 2, [_orther("12.11.2026", "Tin_05_5.jpg")], "VNEXPRESS", "Phong độ ổn định giúp Lê Quang Liêm vững vàng top đầu bảng B"),
            _slot("sentence", 3, [_ddgs("Fabiano Caruana chess grandmaster match")], "WIKIMEDIA COMMONS", "Fabiano Caruana chia điểm sau hai ván đấu trí căng thẳng với Quang Liêm"),
            _slot("sentence", 3, [_orther("12.11.2026", "Tin_05_12.jpg")], "VNEXPRESS", "Thành tích hai thắng tám hòa đưa Quang Liêm đứng nhì bảng tử thần"),
            _slot("sentence", 4, [_url("https://i1-thethao.vnecdn.net/2026/11/14/carlsen-1794615992-1928-1794616159.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=NZt2ISZhhi57LJanhGJsNQ"), _orther("12.11.2026", "Tin_05_7.jpg")], "TOTAL CHESS / MARIA EMELIANOVA", "Vua cờ Magnus Carlsen nhận thất bại khiến Elo tụt xuống 2807"),
            _slot("sentence", 4, [_orther("12.11.2026", "Tin_05_9.jpg")], "WIKIMEDIA COMMONS", "Lần đầu tiên sau 17 năm Carlsen rơi xuống mốc Elo thấp kỷ lục"),
        ],
    },
    # 24 (Nữ) - Mới (Bóng bàn Đông Nam Á)
    {
        "id": 24,
        "art_id": "art_24",
        "group": "Nhóm: Tinh hoa thể thao thế giới",
        "title": "Nguyễn Anh Tú lập cú đúp HCV, bóng bàn Việt Nam đại thắng ở giải Đông Nam Á 2026",
        "summary": (
            "Tại Giải vô địch bóng bàn Đông Nam Á 2026 diễn ra ở Malaysia, đội tuyển bóng bàn Việt Nam đã khép lại hành trình rực rỡ với năm huy chương gồm hai HCV, một HCB và hai HCĐ. "
            "Mở màn ngày 12 tháng 11, năm tuyển thủ nam gồm Nguyễn Anh Tú, Đinh Anh Hoàng, Đoàn Bá Tuấn Anh, Lê Đình Đức và Bùi Thế Nghĩa thắng chủ nhà Malaysia 3-1 để đòi lại ngôi vương đồng đội sau 10 năm chờ đợi. "
            "Chiều 14 tháng 11, Nguyễn Anh Tú tiếp tục thể hiện bản lĩnh thép khi ngược dòng thắng kịch tính tay vợt Singapore Nicholas Tan 4-3 để lần đầu tiên giành HCV đơn nam khu vực. "
            "Ngoài ra, Anh Tú còn cùng Tuấn Anh giành HCB đôi nam, trong khi Mai Hoàng Mỹ Trang và cặp Trần Mai Ngọc, Hoàng Trà My mang về hai tấm HCĐ cho đoàn Việt Nam."
        ),
        "source": "VnExpress / Dân Trí & Thanh Niên",
        "news_source": "VNEXPRESS / DÂN TRÍ",
        "credit": "LIÊN ĐOÀN BÓNG BÀN VN / DÂN TRÍ",
        "slots": [
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/14/1794650252518-g375453853057237-2083-9674-1794657092.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=HuaHdIpwG7ICaoBPTz35AQ"),
            ], "LIÊN ĐOÀN BÓNG BÀN VN", "Nguyễn Anh Tú rạng rỡ với tấm HCV đơn nam Đông Nam Á 2026"),
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/14/904904920-n-1794657086-3798-1794657093.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=eDlyZaQ7xniSVQiRJqkWaw"),
            ], "LIÊN ĐOÀN BÓNG BÀN VN", "Tuyển bóng bàn nam Việt Nam vô địch đồng đội sau 10 năm"),
            _slot("title", 0, [
                _url("https://cdnphoto.dantri.com.vn/Jh-OicrvrZ7HSCmOaC1V6SPtch4=/thumb_w/1020/2026/11/12/bong-ban-7-1794459645920.jpg"),
            ], "DÂN TRÍ", "Thành tích rực rỡ năm huy chương của bóng bàn Việt Nam tại Malaysia"),
            _slot("sentence", 1, [
                _url("https://cdnphoto.dantri.com.vn/kOxU0TcfbVUxqFas9jEVtDQssK0=/thumb_w/1020/2026/11/12/tuyen-bong-ban-2-1794459646708.jpg"),
            ], "DÂN TRÍ", "Đội tuyển bóng bàn Việt Nam ăn mừng chiến thắng tại Malaysia"),
            _slot("sentence", 1, [
                _ddgs("Nguyen Anh Tu bong ban Viet Nam"),
                _ddgs("table tennis championship match arena Malaysia"),
            ], "LIÊN ĐOÀN BÓNG BÀN VN", "Các tay vợt Việt Nam gặt hái hai HCV, một HCB và hai HCĐ"),
            _slot("sentence", 2, [
                _ddgs("Dinh Anh Hoang Nguyen Anh Tu bong ban"),
                _ddgs("Nguyen Anh Tu bong ban SEA Games"),
                _ddgs("table tennis men team celebration Asia"),
            ], "VNEXPRESS", "Đội tuyển đồng đội nam thắng Malaysia 3-1 ở chung kết"),
            _slot("sentence", 2, [
                _ddgs("Dinh Anh Hoang table tennis Vietnam"),
                _ddgs("Vietnam table tennis team champion medal"),
            ], "VNEXPRESS", "Việt Nam lấy lại ngôi vương đồng đội nam sau một thập kỷ"),
            _slot("sentence", 3, [
                _ddgs("Nguyen Anh Tu table tennis match action"),
                _ddgs("table tennis single final intense rally"),
            ], "VNEXPRESS", "Nguyễn Anh Tú ba lần bị dẫn trước nhưng lội ngược dòng 4-3"),
            _slot("sentence", 3, [
                _ddgs("Nguyen Anh Tu huy chuong vang bong ban"),
                _ddgs("table tennis champion gold medal celebration"),
            ], "LIÊN ĐOÀN BÓNG BÀN VN", "Chức vô địch đơn nam đầu tiên sau hai kỳ liên tiếp giành HCB"),
            _slot("sentence", 4, [
                _ddgs("Tran Mai Ngoc Mai Hoang My Trang bong ban"),
                _ddgs("table tennis women doubles match Southeast Asia"),
            ], "LIÊN ĐOÀN BÓNG BÀN VN", "Các tay vợt nữ đóng góp thêm hai HCĐ cho đoàn Việt Nam"),
        ],
    },
    # 25 (Nam) - Kế thừa 11.11 ID 2 + bổ sung 2 ảnh ngang thay thế 2 ảnh dọc
    {
        "id": 25,
        "art_id": "art_25",
        "group": "Nhóm: Tinh hoa thể thao thế giới",
        "title": "Nữ luật sư Stephanie Case chạy 160 km ở Nam Cực phá kỷ lục nam hơn 5 giờ",
        "summary": (
            "Nữ VĐV siêu marathon Stephanie Case vừa lập kỳ tích lịch sử khi trở thành người phụ nữ đầu tiên chinh phục cự ly 100 dặm tương đương 161 kilômét tại giải Antarctic Ice Ultra ở Nam Cực. "
            "Giữa nền nhiệt âm 35 độ C và gió tuyết dữ dội tại ốc đảo Schirmacher, chân chạy 44 tuổi người Canada hoàn thành 38 vòng đua trong 24 giờ 31 phút 44 giây. "
            "Thành tích phi thường này giúp cô xô đổ sâu kỷ lục trước đó của nam VĐV Paul Giblin tới hơn năm giờ đồng hồ. "
            "Là một luật sư nhân quyền đồng thời là nhà sáng lập tổ chức thiện nguyện, chiến thắng của Stephanie Case đã truyền cảm hứng mạnh mẽ về nghị lực không giới hạn trên toàn thế giới."
        ),
        "source": "VnExpress / The North Face",
        "news_source": "VNEXPRESS / THE NORTH FACE",
        "credit": "THE NORTH FACE / ANTARCTIC ICE ULTRA",
        "slots": [
            _slot("title", 0, [_orther("11.11.2026", "Tin_02_5.jpg")], "THE NORTH FACE", "Stephanie Case chinh phục đường chạy băng giá tại Nam Cực"),
            _slot("title", 0, [_orther("11.11.2026", "Tin_02_3.jpg")], "ANTARCTIC ICE ULTRA", "Giải chạy khắc nghiệt bậc nhất hành tinh giữa bão tuyết"),
            _slot("title", 0, [_orther("11.11.2026", "Tin_02_7.jpg")], "THE NORTH FACE", "Nữ VĐV Canada vỡ òa khi chạm đích cự ly 100 dặm lịch sử"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_02_4.jpg")], "WIKIMEDIA COMMONS", "Cảnh quan tuyết trắng khắc nghiệt tại vùng Nam Cực lạnh giá"),
            _slot("sentence", 1, [_orther("11.11.2026", "Tin_02_9.jpg")], "THE NORTH FACE", "Stephanie Case vượt qua điều kiện thời tiết âm 35 độ C"),
            _slot("sentence", 2, [_orther("11.11.2026", "Tin_02_10.jpg")], "IRUNFAR", "Chân chạy 44 tuổi hoàn thành 38 vòng đua quanh trại căn cứ"),
            _slot("sentence", 2, [_ddgs("Stephanie Case ultra runner snow trail mountain")], "RUNNING MAGAZINE", "Chiếc mặt nạ đóng băng buộc cô phải điều chỉnh nhịp thở liên tục"),
            _slot("sentence", 3, [_orther("11.11.2026", "Tin_02_6.jpg")], "RUNNING MAGAZINE", "Kỷ lục 24 giờ 31 phút 44 giây xô đổ thành tích của nam giới"),
            _slot("sentence", 3, [_orther("11.11.2026", "Tin_02_11.jpg")], "GLORIOUS SPORT", "Khoảnh khắc vinh quang phá sâu kỷ lục cũ tới hơn năm giờ"),
            _slot("sentence", 4, [_orther("11.11.2026", "Tin_02_8.jpg")], "FREE TO RUN", "Nữ luật sư nhân quyền lan tỏa thông điệp trao quyền cho phụ nữ"),
            _slot("sentence", 4, [_orther("11.11.2026", "Tin_02_12.jpg")], "THE NORTH FACE / FREE TO RUN", "Câu chuyện phi thường truyền cảm hứng cho cộng đồng chạy bộ toàn cầu"),
        ],
    },
    # 26 (Nữ) - Mới (ATP Finals Turin 2026)
    {
        "id": 26,
        "art_id": "art_26",
        "group": "Nhóm: Tinh hoa thể thao thế giới",
        "title": "ATP Finals 2026 khởi tranh tại Turin: Carlos Alcaraz và Alexander Zverev dẫn đầu cuộc đua vô địch",
        "summary": (
            "Từ ngày 15 đến 22 tháng 11 tại nhà thi đấu Inalpi Arena ở Turin, Italy, giải quần vợt cuối mùa ATP Finals 2026 chính thức khởi tranh với sự góp mặt của tám tay vợt đơn xuất sắc nhất năm. "
            "Bước vào giải với tư cách hạt giống số một, tay vợt người Đức Alexander Zverev hướng tới danh hiệu thứ ba trong sự nghiệp khi nằm chung bảng với Ben Shelton, Arthur Fils và Rafael Jodar. "
            "Trong khi đó, Carlos Alcaraz tràn đầy hưng phấn sau chức vô địch Paris Masters để sánh ngang kỷ lục cùng Novak Djokovic và Rafael Nadal với chín danh hiệu Masters 1000. "
            "Sự vắng mặt đáng tiếc do chấn thương của tay vợt chủ nhà Jannik Sinner hứa hẹn mở ra cuộc đua vô địch kịch tính nhất giữa Zverev, Alcaraz và Daniil Medvedev."
        ),
        "source": "VnExpress / ATP Tour",
        "news_source": "VNEXPRESS / ATP TOUR",
        "credit": "ATP TOUR / AP PHOTO / REUTERS",
        "slots": [
            _slot("title", 0, [
                _url("https://i1-thethao.vnecdn.net/2026/11/15/nitto-atp-finals-2026-official-5151-2816-1794706477.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=CjE0rslPnuAm0aMEKTUVcA"),
            ], "ATP TOUR", "Tám tay vợt xuất sắc nhất năm chụp ảnh bên cúp ATP Finals tại Turin"),
            _slot("title", 0, [_orther("09.11.2026", "Tin_03_1.jpg")], "AP PHOTO", "Carlos Alcaraz tiến vào Turin với phong độ đỉnh cao"),
            _slot("title", 0, [
                _ddgs("Alexander Zverev tennis ATP Finals Turin"),
                _ddgs("Alexander Zverev tennis serve indoor court"),
            ], "REUTERS", "Hạt giống số một Alexander Zverev hướng tới ngôi vương thứ ba"),
            _slot("sentence", 1, [
                _ddgs("Inalpi Arena Turin ATP Finals tennis court"),
                _ddgs("Pala Alpitour Inalpi Arena Turin ATP Finals"),
            ], "ATP TOUR", "Nhà thi đấu Inalpi Arena tại Turin năm thứ sáu liên tiếp đăng cai"),
            _slot("sentence", 1, [
                _ddgs("ATP Finals Turin trophy court arena"),
                _ddgs("Nitto ATP Finals tennis tournament crowd"),
            ], "ATP TOUR", "Tám tay vợt đơn chia hai bảng thi đấu vòng tròn tính điểm"),
            _slot("sentence", 2, [
                _ddgs("Alexander Zverev tennis forehand action"),
                _ddgs("Ben Shelton tennis ATP match serve"),
            ], "AP PHOTO", "Alexander Zverev đối đầu Ben Shelton và Arthur Fils ở vòng bảng"),
            _slot("sentence", 3, [_orther("09.11.2026", "Tin_03_9.jpg")], "GETTY IMAGES / ATP TOUR", "Alcaraz vừa đoạt danh hiệu Masters 1000 thứ 9 tại Paris Masters"),
            _slot("sentence", 3, [_orther("09.11.2026", "Tin_03_12.jpg")], "ATP TOUR", "Tay vợt Tây Ban Nha tự tin chinh phục danh hiệu cuối mùa đầu tiên"),
            _slot("sentence", 4, [
                _ddgs("Jannik Sinner tennis Italy Turin"),
                _ddgs("Daniil Medvedev tennis ATP Finals Turin"),
            ], "REUTERS", "Sự vắng mặt của Jannik Sinner mở ra cơ hội lớn cho nhóm ứng viên"),
            _slot("sentence", 4, [_orther("09.11.2026", "Tin_03_2.jpg")], "REUTERS", "Cuộc đua kịch tính giữa Zverev, Alcaraz và Daniil Medvedev tại Italy"),
        ],
    },
]
