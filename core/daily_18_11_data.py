# -*- coding: utf-8 -*-
"""
daily_18_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 18.11.2026
(Tổng hợp tin nổi bật từ 18h tối 17.11 đến sáng 18.11.2026 — Việt Nam + Thế giới).
Phân bổ giọng đọc luân phiên Nam (primary) / Nữ (secondary) và 1–3 ảnh ngang HD sạch logo mỗi câu.
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
WEEKLY_16 = ROOT / "outputs" / "16.11.2026" / "images"
WEEKLY_09 = ROOT / "outputs" / "09.11.2026" / "images"


def _url(u: str) -> tuple[str, str]:
    return ("url", u)


def _ddgs(q: str) -> tuple[str, str]:
    return ("ddgs", q)


def _local(p: Path) -> tuple[str, str]:
    return ("local", str(p))


def _slot(slot_type: str, sent_idx: int, sources: List[tuple[str, str]], credit: str, desc: str) -> Dict[str, Any]:
    return {
        "type": slot_type,
        "sentence_idx": sent_idx,
        "sources": sources,
        "credit": credit,
        "desc": desc,
    }


# ── URL ảnh sạch (không logo/watermark) trích trực tiếp từ báo chí 17–18.11.2026 ──
TN_VN_KGZ_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/dinh-bac-lap-sieu-pham-de-mo-ty-so-cho-doi-tuyen-viet-nam-1-17949243494651768177852.jpg"
TN_VN_KGZ_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/dinh-bac-linh-xuong-hang-cong-17949231844561085987617.jpg"
TN_VN_KGZ_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/vietnam-kyrgyzstan-3-17949245993511432984873.jpg"
TN_VN_KGZ_4 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/vietnam-kyrgyzstan-5-1794924599373725838588.jpg"
TN_VN_KGZ_5 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/hlv-kim-sang-sik-trao-co-hoi-cho-thu-mon-trung-kien-1794923184592737857003.jpg"
TN_VN_KGZ_6 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/doi-tuyen-kyrgyzstan-khong-the-xuyen-thung-manh-luoi-cua-trung-kien-1794923184522135166309.jpg"
TN_VN_KGZ_7 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/doi-tuyen-kyrgyzstan-don-len-tim-ban-go-17949231844891889116394.jpg"
TN_VN_KGZ_8 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/doi-tuyen-kyrgyzstan-don-len-tim-ban-go-1-1794924349496481309745.jpg"
TN_VN_KGZ_9 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/doi-tuyen-kyrgyzstan-ghi-lien-tiep-2-ban-cuoi-tran-1794923650496684022637.jpg"
TN_VN_KGZ_10 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/vietnam-kyrgyzstan-6-1794924898753205276681.jpg"
TN_VN_KGZ_11 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/vietnam-kyrgyzstan-9-17949245996861219322279.jpg"
TN_VN_KGZ_12 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/vietnam-kyrgyzstan-1-17949245993001446768308.jpg"

VNE_BRA_SIN = "https://i1-thethao.vnecdn.net/2026/11/17/AP26321413721161-9286-1794921675.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=rrwqZIWjiU-aWKBGJLm0Qg"
VNE_POCH = "https://i1-thethao.vnecdn.net/2026/11/17/Pochettino-7077-1794877434.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=5smPi-bEu0Rs-0llz9v5jA"

TN_THAI_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/179492768660720554668242885303635923414894611837492652b59ab7b1d386429806dc9cd7989e-17949277053131236451718.jpg"
TN_THAI_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/17949275350942055466824288530363592341489461183749ce4aef67e9fe173b6ca9ebc4fe3fe33f-17949275521331881547835.jpg"
TN_THAI_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/1794929458742205546682428853036359234148946118374924a07c8714b246d9580269d0a648d41c-17949294775051489627648.jpg"
TN_THAI_5 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/179492986425720554668242885303635923414894611837494df75b2470e5c26c17c9924aac55e14b-1794929885539147751265.jpg"

TN_CATPHCM_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/arthur-clb-17949156408121553172722.jpg"
TN_CATPHCM_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/quang-kiet-clb-17949156406821325996753.jpg"
TN_CATPHCM_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/tien-linh-clb-17949156401361988490823.jpg"

TN_DH_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/tnw-sankhaukhaimacdhthethaotoanquoc2026-13-1794909663527937825628-17949133103221969849102.jpeg"
TN_DH_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/tnw-b9c040541bbc9be2c2ad-17949126967671865956113-17949133103221328173770.jpg"
TN_DH_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/tnw-sankhaukhaimacdhthethaotoanquoc2026-11-1794909663408330331479-17949133103221440806752.jpeg"
TN_DH_4 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/tnw-sankhaukhaimacdhthethaotoanquoc2026-8-1794909662983236216644-1794913768498137647650.jpeg"
TN_DH_5 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/tnw-sankhaukhaimacdhthethaotoanquoc2026-3-1794909662490965522956-17949139621621838102785.jpeg"
TN_DH_6 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/tnw-sankhaukhaimacdhthethaotoanquoc2026-2-17949096624431586126945-17949133103221874805852.jpeg"

TN_QL_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/liem-new-1794928362994947174052.jpg"
TN_QL_2 = "https://images2.thanhnien.vn/528068263637045248/2023/8/2/le-quang-liem-wc-2023-16910124497171884050447.jpg"

VNE_ABEL_1 = "https://i1-thethao.vnecdn.net/2026/11/17/abdel-nunez-jpeg-1794932202-6822-1794932339.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=04qJe1Ce3g_koK5iqmOJeg"
VNE_ROONEY_1 = "https://i1-thethao.vnecdn.net/2026/11/17/rooney-4381-1794930736.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=nwYZ9-p6CIX4Xm1c7nenBA"
VNE_ROONEY_2 = "https://i1-thethao.vnecdn.net/2026/11/18/576186332-858888049987854-6874-5832-9142-1794958530.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=QOi-5CpqIqHWl-DGUSRCGQ"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 18.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao sáng ngày 18 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất từ 18 giờ tối qua đến sáng nay. "
        "Ở trong nước, đội tuyển Việt Nam đánh rơi chiến thắng nghiệt ngã trước Kyrgyzstan trong hai phút cuối trận chung kết Casper Cup 2026, nhưng tiền đạo Nguyễn Đình Bắc vẫn kịp ghi dấu ấn lịch sử. "
        "Trên đấu trường quốc tế, UEFA Nations League chính thức chốt đủ tám cái tên vào tứ kết sau những màn rượt đuổi tỷ số nghẹt thở của Bồ Đào Nha và Na Uy, trong khi Brazil và Argentina cùng trút mưa bàn thắng 7-0. "
        "Cùng bước ngoặt Mauricio Pochettino bay chuyên cơ tới Manchester United và hành trình của Lê Quang Liêm tại giải cờ vua toàn năng thế giới, hãy điểm lại 17 tin nóng ngay sau đây."
    ),
    "source": "Thanh Niên / VnExpress / Dân Trí",
    "news_source": "THANH NIÊN / VNEXPRESS",
    "credit": "THANH NIÊN / REUTERS / AP",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao sáng ngày 18 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất từ 18 giờ tối qua đến sáng nay.",
        },
        {
            "voice_preset": "primary",
            "text": "Ở trong nước, đội tuyển Việt Nam đánh rơi chiến thắng nghiệt ngã trước Kyrgyzstan trong hai phút cuối trận chung kết Casper Cup 2026, nhưng tiền đạo Nguyễn Đình Bắc vẫn kịp ghi dấu ấn lịch sử.",
        },
        {
            "voice_preset": "secondary",
            "text": "Trên đấu trường quốc tế, UEFA Nations League chính thức chốt đủ tám cái tên vào tứ kết sau những màn rượt đuổi tỷ số nghẹt thở của Bồ Đào Nha và Na Uy, trong khi Brazil và Argentina cùng trút mưa bàn thắng 7-0.",
        },
        {
            "voice_preset": "primary",
            "text": "Cùng bước ngoặt Mauricio Pochettino bay chuyên cơ tới Manchester United và hành trình của Lê Quang Liêm tại giải cờ vua toàn năng thế giới, hãy điểm lại 17 tin nóng ngay sau đây.",
        },
    ],
    "slots": [
        # Câu 1 (Nữ)
        _slot("sentence", 1, [_url(TN_VN_KGZ_3)], "THANH NIÊN", "Đội tuyển Việt Nam tranh tài quyết liệt trước Kyrgyzstan trên sân Thiên Trường"),
        _slot("sentence", 1, [_local(ORTHER / "16.11.2026" / "images" / "v3_spain_england.jpg")], "UEFA", "Sân cỏ UEFA Nations League bùng nổ ở lượt trận hạ màn vòng bảng"),
        _slot("sentence", 1, [_url(TN_QL_1)], "THANH NIÊN", "Kỳ thủ Lê Quang Liêm thi đấu ấn tượng tại Hungary"),
        # Câu 2 (Nam)
        _slot("sentence", 2, [_url(TN_VN_KGZ_1)], "THANH NIÊN", "Nguyễn Đình Bắc tung cú sút lập siêu phẩm mở tỷ số vào lưới Kyrgyzstan"),
        _slot("sentence", 2, [_url(TN_VN_KGZ_9)], "THANH NIÊN", "Kyrgyzstan ghi liền hai bàn trong hai phút cuối trận"),
        _slot("sentence", 2, [_url(TN_VN_KGZ_4)], "THANH NIÊN", "Đình Bắc cán mốc 12 bàn thắng cho đội tuyển quốc gia"),
        # Câu 3 (Nữ)
        _slot("sentence", 3, [_ddgs("Bruno Fernandes Portugal football match celebration"), _local(WEEKLY_16 / "Tin_02_1.jpg")], "REUTERS", "Bồ Đào Nha thắng kịch tính Xứ Wales với 15 điểm tuyệt đối"),
        _slot("sentence", 3, [_ddgs("Erling Haaland Norway national team goal celebration")], "AP PHOTO", "Erling Haaland lập cú đúp đưa Na Uy vào tứ kết Nations League"),
        _slot("sentence", 3, [_url(VNE_BRA_SIN)], "AP PHOTO", "Vinícius Júnior giúp Brazil đại thắng Singapore 7-0"),
        # Câu 4 (Nam)
        _slot("sentence", 4, [_url(VNE_POCH)], "VNEXPRESS / REUTERS", "Mauricio Pochettino bay chuyên cơ sang tiếp quản Manchester United"),
        _slot("sentence", 4, [_local(WEEKLY_16 / "Tin_23_1.jpg")], "TOTAL CHESS / FIDE", "Lê Quang Liêm áp sát tốp 10 thế giới ở giải cờ vua toàn năng"),
        _slot("sentence", 4, [_local(WEEKLY_16 / "Tin_26_3.jpg")], "ATP TOUR / REUTERS", "Alexander Zverev sớm giành vé bán kết ATP Finals 2026 tại Turin"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — Trọng điểm 1)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "Nhóm: Tâm điểm đội tuyển Việt Nam",
        "title": "Tuyển Việt Nam thua ngược Kyrgyzstan 1-2 trong hai phút cuối, lỡ chức vô địch Casper Cup 2026",
        "summary": (
            "Tối ngày 17 tháng 11 trước khoảng 5000 khán giả trên sân Thiên Trường tại Ninh Bình, đội tuyển Việt Nam bước vào trận giao hữu quyết định ngôi vô địch Casper Cup 2026 gặp Kyrgyzstan. "
            "Trong thế trận giằng co ở hiệp một, tiền đạo Nguyễn Đình Bắc bất ngờ tạo nên siêu phẩm ở phút 19 khi đi bóng từ biên trái xộc thẳng vào trung lộ rồi cứa lòng chân phải đưa bóng xoáy vào góc cao khung thành thủ môn Erzhan Tokotaev, mở tỷ số 1-0 cho chủ nhà. "
            "Suốt phần lớn thời gian còn lại, hàng thủ Việt Nam chơi tập trung và tưởng như đã cầm chắc chiến thắng trong tay. "
            "Thế nhưng đúng ở phút 86, từ quả phạt góc bên cánh trái của Erbol Atabaev, đội trưởng 34 tuổi Kichin Valeriy bật cao đánh đầu cận thành trong thế không bị ai kèm để gỡ hòa 1-1. "
            "Chưa kịp xốc lại tinh thần, chỉ hai phút sau, tiền vệ Ngọc Sơn để mất bóng ở tuyến giữa tạo điều kiện cho Atabaev tung cú sút xa từ khoảng cách gần 60 mét qua đầu thủ môn Trần Trung Kiên đang dâng cao, ấn định thắng lợi 2-1 đầy cay đắng cho Kyrgyzstan."
        ),
        "source": "VnExpress / Thanh Niên",
        "news_source": "VNEXPRESS / THANH NIÊN",
        "credit": "THANH NIÊN",
        "slots": [
            _slot("title", 0, [_url(TN_VN_KGZ_3)], "THANH NIÊN", "Đội tuyển Việt Nam đối đầu Kyrgyzstan trên sân Thiên Trường"),
            _slot("title", 0, [_url(TN_VN_KGZ_1)], "THANH NIÊN", "Đình Bắc tỏa sáng với siêu phẩm sút xa mở tỷ số"),
            _slot("title", 0, [_url(TN_VN_KGZ_9)], "THANH NIÊN", "Kyrgyzstan lội ngược dòng trong hai phút cuối trận"),
            # Câu 1
            _slot("sentence", 1, [_url(TN_VN_KGZ_4)], "THANH NIÊN", "Không khí quyết liệt trận chung kết Casper Cup 2026 tại Ninh Bình"),
            _slot("sentence", 1, [_url(TN_VN_KGZ_12)], "THANH NIÊN", "Đội tuyển Việt Nam nhập cuộc tự tin trước đại diện Trung Á"),
            # Câu 2
            _slot("sentence", 2, [_url(TN_VN_KGZ_2)], "THANH NIÊN", "Nguyễn Đình Bắc đi bóng đột phá bên hành lang trái"),
            _slot("sentence", 2, [_local(WEEKLY_16 / "Tin_17_3.jpg")], "VNEXPRESS", "Niềm vui vỡ òa của Đình Bắc và đồng đội sau cú cứa lòng mở tỷ số phút 19"),
            # Câu 3
            _slot("sentence", 3, [_url(TN_VN_KGZ_6)], "THANH NIÊN", "Thủ môn Trần Trung Kiên và hàng thủ đứng vững trong phần lớn trận đấu"),
            _slot("sentence", 3, [_url(TN_VN_KGZ_7)], "THANH NIÊN", "Kyrgyzstan gặp nhiều bế tắc trước khối phòng ngự áo trắng"),
            # Câu 4
            _slot("sentence", 4, [_url(TN_VN_KGZ_8)], "THANH NIÊN", "Kyrgyzstan dồn toàn lực tìm bàn gỡ từ tình huống cố định phút 86"),
            _slot("sentence", 4, [_local(WEEKLY_16 / "Tin_17_9.jpg")], "VNEXPRESS", "Không khí căng thẳng bên đường biên ở những phút cuối trận"),
            # Câu 5
            _slot("sentence", 5, [_url(TN_VN_KGZ_5)], "THANH NIÊN", "Thủ môn Trần Trung Kiên tiếc nuối sau bàn thua bất ngờ từ giữa sân"),
            _slot("sentence", 5, [_url(TN_VN_KGZ_10)], "THANH NIÊN", "Nỗi thất vọng của các tuyển thủ Việt Nam sau hai phút đánh mất tất cả"),
        ],
    },
    # 02 (Nữ — Trọng điểm 2)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "Nhóm: Tâm điểm đội tuyển Việt Nam",
        "title": "Đình Bắc sánh ngang Công Phượng, tuyển Việt Nam bị trừ 5,3 điểm FIFA dù dùng đúng luật thay tám người",
        "summary": (
            "Dù đội tuyển Việt Nam không thể giữ lại chiếc cúp trên sân nhà, bàn thắng vào lưới Kyrgyzstan vẫn đánh dấu cột mốc đáng nhớ cho cá nhân Nguyễn Đình Bắc. "
            "Pha lập công này giúp chân sút sinh năm 2004 cán mốc 12 bàn thắng trong màu áo đội tuyển quốc gia, chính thức sánh ngang thành tích ghi bàn của đàn anh Nguyễn Công Phượng. "
            "Ở trận đấu khép lại năm 2026, ban huấn luyện Việt Nam đã sử dụng tổng cộng 19 cầu thủ với 8 sự thay đổi người, qua đó khiến nhiều khán giả băn khoăn về tính hợp lệ. "
            "Tuy nhiên, theo luật mới của IFAB có hiệu lực từ ngày 1 tháng 7 năm 2026, các trận giao hữu cấp đội tuyển quốc gia nhóm A được phép đăng ký tối đa 15 dự bị và thay tới 8 cầu thủ trong ba lượt bóng chết, nên tuyển Việt Nam hoàn toàn tuân thủ đúng quy định. "
            "Dù vậy, thất bại trước đối thủ xếp dưới khiến Việt Nam bị trừ nặng 5,3 điểm trên bảng xếp hạng FIFA xuống còn 1228,34 điểm và tạm giữ hạng 98, trong khi Kyrgyzstan được cộng 5,3 điểm để vươn hai bậc lên vị trí 102 thế giới."
        ),
        "source": "VnExpress / Thanh Niên / Dân Trí",
        "news_source": "VNEXPRESS / THANH NIÊN / DÂN TRÍ",
        "credit": "THANH NIÊN / VNEXPRESS",
        "slots": [
            _slot("title", 0, [_url(TN_VN_KGZ_4)], "THANH NIÊN", "Nguyễn Đình Bắc cán mốc 12 bàn thắng cho đội tuyển Việt Nam"),
            _slot("title", 0, [_local(WEEKLY_09 / "Tin_18_5.jpg")], "VNEXPRESS", "Thành tích của Đình Bắc sánh ngang đàn anh Nguyễn Công Phượng"),
            _slot("title", 0, [_url(TN_VN_KGZ_3)], "THANH NIÊN", "Đội tuyển Việt Nam sử dụng 19 cầu thủ ở trận gặp Kyrgyzstan"),
            # Câu 1
            _slot("sentence", 1, [_url(TN_VN_KGZ_1)], "THANH NIÊN", "Khoảnh khắc Đình Bắc ghi dấu ấn trên sân Thiên Trường"),
            # Câu 2
            _slot("sentence", 2, [_url(TN_VN_KGZ_2)], "THANH NIÊN", "Chân sút sinh năm 2004 tỏa sáng với pha lập công thứ 12 ở ĐTQG"),
            _slot("sentence", 2, [_local(WEEKLY_09 / "Tin_18_3.jpg")], "THANH NIÊN", "Nguyễn Công Phượng từng ghi 12 bàn cho đội tuyển Việt Nam"),
            # Câu 3
            _slot("sentence", 3, [_url(TN_VN_KGZ_8)], "THANH NIÊN", "HLV Kim Sang-sik tung tới 8 cầu thủ dự bị vào sân trong hiệp hai"),
            _slot("sentence", 3, [_url(TN_VN_KGZ_7)], "THANH NIÊN", "Tổng cộng 19 cầu thủ Việt Nam được trao cơ hội thi đấu"),
            # Câu 4
            _slot("sentence", 4, [_ddgs("football fourth official substitution board stadium"), _local(WEEKLY_16 / "Tin_17_6.jpg")], "FIFA / IFAB", "Luật mới từ tháng 7 năm 2026 cho phép thay tối đa 8 cầu thủ ở trận giao hữu"),
            _slot("sentence", 4, [_url(TN_VN_KGZ_12)], "THANH NIÊN", "Các cầu thủ trẻ vào sân thử nghiệm đội hình đúng quy định FIFA"),
            # Câu 5
            _slot("sentence", 5, [_url(TN_VN_KGZ_10)], "THANH NIÊN", "Thất bại khiến tuyển Việt Nam bị trừ 5,3 điểm trên BXH FIFA"),
            _slot("sentence", 5, [_url(TN_VN_KGZ_9)], "THANH NIÊN", "Kyrgyzstan tăng hai bậc lên hạng 102 thế giới sau trận thắng ngược"),
        ],
    },
    # 03 (Nam — Trọng điểm 3)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "Nhóm: Tâm điểm đội tuyển Việt Nam",
        "title": "HLV Kim Sang-sik nhận lỗi với người hâm mộ, bảo vệ thủ môn Trần Trung Kiên sau trận thua đau",
        "summary": (
            "Bước vào phòng họp báo sau trận thua ngược Kyrgyzstan, HLV Kim Sang-sik thẳng thắn gửi lời xin lỗi tới người hâm mộ và các câu lạc bộ trong nước vì không thể khép lại năm 2026 bằng một chiến thắng. "
            "Nhà cầm quân người Hàn Quốc đặc biệt lên tiếng bảo vệ thủ môn trẻ Trần Trung Kiên trước những chỉ trích nhắm vào bàn thua thứ hai từ khoảng cách 60 mét. "
            "Ông khẳng định trước tình huống đó các tiền vệ phía trên đã mắc sai lầm để mất bóng nên không thể đổ toàn bộ trách nhiệm lên vai cá nhân thủ môn, đồng thời nhấn mạnh Trung Kiên vẫn hoàn thành tốt nhiệm vụ trong bối cảnh chịu áp lực cạnh tranh gay gắt với Đặng Văn Lâm, Nguyễn Filip và Lê Giang Patrik. "
            "Bên cạnh nỗi tiếc nuối về sự mất tập trung ở cuối trận khi thể lực suy giảm, HLV Kim Sang-sik vẫn dành lời khen cho bốn tân binh vừa ra mắt, đặc biệt là trung vệ trẻ Lương Chí Khải ở khả năng không chiến và tranh chấp tay đôi. "
            "Trận đấu này cũng khép lại bản hợp đồng hiện tại của ông Kim trong lúc chờ làm việc với VFF về chặng đường tiếp theo."
        ),
        "source": "VnExpress / VOV",
        "news_source": "VNEXPRESS / VOV",
        "credit": "THANH NIÊN / VNEXPRESS",
        "slots": [
            _slot("title", 0, [_local(WEEKLY_16 / "Tin_17_5.jpg")], "VNEXPRESS", "HLV Kim Sang-sik nhận trách nhiệm trong họp báo sau trận"),
            _slot("title", 0, [_url(TN_VN_KGZ_5)], "THANH NIÊN", "Thủ môn Trần Trung Kiên được HLV trưởng hết mực bảo vệ"),
            _slot("title", 0, [_url(TN_VN_KGZ_10)], "THANH NIÊN", "Đội tuyển Việt Nam khép lại năm 2026 nhiều thử thách"),
            # Câu 1
            _slot("sentence", 1, [_url(TN_VN_KGZ_2)], "THANH NIÊN", "HLV Kim Sang-sik gửi lời xin lỗi người hâm mộ và các câu lạc bộ"),
            # Câu 2
            _slot("sentence", 2, [_url(TN_VN_KGZ_6)], "THANH NIÊN", "Thủ môn Trần Trung Kiên chịu nhiều áp lực sau bàn thua ở phút 88"),
            # Câu 3
            _slot("sentence", 3, [_local(WEEKLY_16 / "Tin_17_4.jpg")], "VNEXPRESS", "Cuộc cạnh tranh vị trí gắt gao trong khung gỗ đội tuyển Việt Nam"),
            _slot("sentence", 3, [_local(WEEKLY_16 / "Tin_17_8.jpg")], "VNEXPRESS", "Các cầu thủ trẻ Việt Nam thi đấu nỗ lực suốt trận"),
            # Câu 4
            _slot("sentence", 4, [_url(TN_VN_KGZ_3)], "THANH NIÊN", "Bốn tân binh được trao cơ hội ra mắt và ghi điểm với HLV trưởng"),
            _slot("sentence", 4, [_url(TN_VN_KGZ_8)], "THANH NIÊN", "Sự suy giảm thể lực ở những phút cuối là bài học lớn cho lứa trẻ"),
            # Câu 5
            _slot("sentence", 5, [_local(WEEKLY_16 / "Tin_17_11.jpg")], "VNEXPRESS", "Tương lai của HLV Kim Sang-sik chờ quyết định làm việc cùng VFF"),
        ],
    },
    # 04 (Nữ — Quốc tế chi tiết 1)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Bồ Đào Nha thắng nghẹt thở Xứ Wales 3-2 trong thế thiếu người, khép lại vòng bảng với 15 điểm tuyệt đối",
        "summary": (
            "Rạng sáng ngày 18 tháng 11 tại lượt cuối bảng A4 UEFA Nations League trên sân Cardiff, đội tuyển Bồ Đào Nha đã tìm lại niềm vui chiến thắng sau cú sốc thua Đan Mạch khi vượt qua chủ nhà Xứ Wales với tỷ số 3-2. "
            "Đội trưởng Bruno Fernandes sớm đưa đội khách vượt lên ở phút 11, nhưng Xứ Wales vùng lên mạnh mẽ để dẫn ngược 2-1 nhờ hai pha lập công của David Brooks và Sorba Thomas trước khi Pedro Neto kịp gỡ hòa 2-2 cuối hiệp một. "
            "Sang hiệp hai, tài năng trẻ Carlos Forbs — người được trao chiếc áo số 7 thay Cristiano Ronaldo — tỏa sáng với pha độc diễn dứt điểm hiểm hóc ở phút 70 để tái lập thế dẫn bàn cho Selecao châu Âu. "
            "Chỉ bốn phút sau, Pedro Neto nhận thẻ vàng thứ hai rời sân khiến Bồ Đào Nha phải gồng mình chơi thiếu người trong gần 20 phút cuối, nhưng họ vẫn bảo toàn thành công thắng lợi để kết thúc vòng bảng với 15 điểm tuyệt đối. "
            "Sau trận, HLV Jorge Jesus còn gây chú ý khi nhận định Nations League hiện nay có tính cạnh tranh khốc liệt hơn cả vòng chung kết Euro."
        ),
        "source": "VnExpress / Dân Trí / VOV",
        "news_source": "VNEXPRESS / DÂN TRÍ / VOV",
        "credit": "VNEXPRESS / REUTERS / AP",
        "slots": [
            _slot("title", 0, [_ddgs("Portugal Wales Nations League football match")], "AP PHOTO", "Bồ Đào Nha giành chiến thắng kịch tính 3-2 trên sân Xứ Wales"),
            _slot("title", 0, [_ddgs("Bruno Fernandes Portugal national team match")], "REUTERS", "Đội trưởng Bruno Fernandes mở tỷ số từ sớm cho đội khách"),
            _slot("title", 0, [_ddgs("Portugal national football team celebrating goal")], "AP PHOTO", "Bồ Đào Nha hoàn tất vòng bảng với 15 điểm tuyệt đối"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("Cardiff City Stadium Wales football night match")], "UEFA", "Chảo lửa Cardiff City đón màn đối đầu quyết liệt bảng A4"),
            _slot("sentence", 1, [_ddgs("Portugal national football team players lineup")], "REUTERS", "Bồ Đào Nha trở lại mạnh mẽ sau cú vấp trước Đan Mạch"),
            # Câu 2
            _slot("sentence", 2, [_ddgs("Bruno Fernandes Portugal national team celebration")], "REUTERS", "Bruno Fernandes khai thông thế bế tắc ở phút thứ 11"),
            _slot("sentence", 2, [_ddgs("David Brooks Wales football goal celebration")], "AP PHOTO", "David Brooks và Sorba Thomas giúp Xứ Wales dẫn ngược 2-1"),
            # Câu 3
            _slot("sentence", 3, [_ddgs("Carlos Forbs football winger dribbling")], "REUTERS", "Tài năng trẻ Carlos Forbs bùng nổ trong chiếc áo số 7 lịch sử"),
            _slot("sentence", 3, [_ddgs("Pedro Neto Portugal football action")], "AP PHOTO", "Pedro Neto ghi bàn gỡ 2-2 trước khi nhận thẻ đỏ ở hiệp hai"),
            # Câu 4
            _slot("sentence", 4, [_ddgs("Portugal national team football defending match")], "UEFA", "Mười cầu thủ Bồ Đào Nha kiên cường bảo vệ thành quả 15 điểm"),
            # Câu 5
            _slot("sentence", 5, [_ddgs("Jorge Jesus coach Portugal press conference")], "REUTERS", "HLV Jorge Jesus đánh giá rất cao chất lượng chuyên môn của Nations League"),
        ],
    },
    # 05 (Nam — Quốc tế chi tiết 2)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Haaland lập cú đúp phút bù giờ giúp Na Uy thắng Đan Mạch 3-2, chốt đủ tám đội vào tứ kết Nations League",
        "summary": (
            "Ở trận đấu còn lại của bảng A4 diễn ra cùng giờ tại Copenhagen, người hâm mộ được chứng kiến màn lội ngược dòng ngoạn mục bậc nhất vòng bảng UEFA Nations League. "
            "Chủ nhà Đan Mạch khởi đầu như mơ và sớm dẫn trước 2-0 chỉ sau 14 phút bóng lăn nhờ các pha ghi bàn của Rasmus Hojlund và Pierre-Emile Hojbjerg. "
            "Tuy nhiên, Erling Haaland thắp lại hy vọng cho đội tuyển Na Uy bằng bàn rút ngắn cách biệt ở phút 37 trước khi đội trưởng Martin Odegaard đưa trận đấu về vạch xuất phát ở phút 83. "
            "Kịch tính đẩy lên đỉnh điểm ở phút bù giờ thứ sáu của hiệp hai, khi Na Uy được hưởng phạt đền và chính Haaland dứt điểm lạnh lùng hoàn tất cú đúp, ấn định chiến thắng 3-2 ngay trên đất Đan Mạch. "
            "Ba điểm quý giá giúp Na Uy cán đích ở vị trí nhì bảng A4 và chính thức giành tấm vé cuối cùng góp mặt tại vòng tứ kết UEFA Nations League mùa giải 2026-2027 cùng với Pháp, Đức, Anh, Bồ Đào Nha, Tây Ban Nha, Bỉ và Hà Lan."
        ),
        "source": "VietnamNet / Bongdaplus",
        "news_source": "VIETNAMNET / BONGDAPLUS",
        "credit": "REUTERS / AP / UEFA",
        "slots": [
            _slot("title", 0, [_ddgs("Erling Haaland Norway national team celebration")], "REUTERS", "Erling Haaland rực sáng giúp Na Uy ngược dòng thắng Đan Mạch 3-2"),
            _slot("title", 0, [_ddgs("Parken Stadium Copenhagen football pitch night")], "UEFA", "Sân Parken chứng kiến màn rượt đuổi tỷ số nghẹt thở"),
            _slot("title", 0, [_ddgs("Martin Odegaard Norway football match action")], "AP PHOTO", "Martin Odegaard góp công lớn đưa Na Uy vào tứ kết"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("Denmark Norway football match Nations League")], "REUTERS", "Cuộc thư hùng nảy lửa tại Copenhagen tranh vé vào tứ kết"),
            # Câu 2
            _slot("sentence", 2, [_ddgs("Rasmus Hojlund Denmark celebration goal")], "AP PHOTO", "Rasmus Hojlund và Hojbjerg đưa Đan Mạch dẫn trước 2-0 từ rất sớm"),
            # Câu 3
            _slot("sentence", 3, [_ddgs("Erling Haaland Norway jersey goal match")], "REUTERS", "Haaland rút ngắn tỷ số xuống 1-2 trước giờ nghỉ hiệp một"),
            _slot("sentence", 3, [_ddgs("Martin Odegaard Norway jersey football")], "AP PHOTO", "Martin Odegaard gỡ hòa 2-2 ở phút 83 đầy cảm xúc"),
            # Câu 4
            _slot("sentence", 4, [_ddgs("Erling Haaland penalty kick football match")], "REUTERS", "Haaland lạnh lùng sút phạt đền phút 90+6 ấn định tỷ số 3-2"),
            # Câu 5
            _slot("sentence", 5, [_ddgs("Norway national football team celebrating victory")], "UEFA", "Na Uy hoàn tất danh sách 8 anh tài bước vào vòng tứ kết Nations League"),
            _slot("sentence", 5, [_local(WEEKLY_16 / "Tin_01_1.jpg")], "UEFA", "Tám đội mạnh nhất châu Âu sẵn sàng cho vòng knock-out"),
        ],
    },
    # 06 (Nữ — Quốc tế chi tiết 3)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Vinícius lập hat-trick trong 21 phút, Brazil đè bẹp Singapore 7-0 để thắng đậm nhất sau 14 năm",
        "summary": (
            "Tối ngày 17 tháng 11 tại sân Quốc gia Singapore, đội tuyển Brazil đã trút cơn thịnh nộ sau thất bại trước Nhật Bản bằng chiến thắng hủy diệt 7-0 trước đội chủ nhà. "
            "Do HLV trưởng Carlo Ancelotti cùng tiền đạo Raphinha phải ngồi khán đài chịu án phạt thẻ đỏ từ trận trước, trợ lý Paul Clement trực tiếp chỉ đạo ngoài đường biên nhưng vẫn giữ nguyên bộ tứ tấn công trẻ trung mà ông Ancelotti thử nghiệm. "
            "Ngôi sao Vinícius Júnior rũ bỏ áp lực phong độ tại Real Madrid để bùng nổ với cú hat-trick chỉ trong vòng 21 phút đầu trận ở các phút 9, 15 và 21. "
            "Ba gương mặt trẻ đá chính cùng anh là Endrick, Estêvão và Rayan lần lượt nối dài cách biệt trước khi hậu vệ Raoul Suhaimi của Singapore phản lưới nhà ở phút 71. "
            "Với 21 cú dứt điểm áp đảo hoàn toàn, Selecao chính thức có chiến thắng đậm nhất trong 14 năm qua và thu về bài thử nghiệm giàu tín hiệu cho hàng công thế hệ kế cận."
        ),
        "source": "VnExpress / Dân Trí",
        "news_source": "VNEXPRESS / DÂN TRÍ",
        "credit": "AP PHOTO / REUTERS",
        "slots": [
            _slot("title", 0, [_url(VNE_BRA_SIN)], "AP PHOTO", "Vinícius Júnior bùng nổ giúp Brazil đè bẹp Singapore 7-0"),
            _slot("title", 0, [_ddgs("Brazil national football team match celebration")], "REUTERS", "Sức mạnh vượt trội của Selecao tại sân Quốc gia Singapore"),
            _slot("title", 0, [_ddgs("Endrick Estevao Brazil football celebration")], "AP PHOTO", "Dàn sao trẻ Brazil thi đấu thăng hoa trong chiến thắng lịch sử"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("National Stadium Singapore football match")], "REUTERS", "Sân Quốc gia Singapore trong buổi tối Brazil trút cơn mưa bàn thắng"),
            # Câu 2
            _slot("sentence", 2, [_ddgs("Carlo Ancelotti Brazil coach press conference")], "AP PHOTO", "HLV Carlo Ancelotti thử nghiệm hàng công mới dù ngồi trên khán đài"),
            # Câu 3
            _slot("sentence", 3, [_ddgs("Vinicius Junior Brazil jersey goal celebration")], "REUTERS", "Vinícius Júnior lập hat-trick chỉ trong 21 phút hiệp một"),
            _slot("sentence", 3, [_ddgs("Vinicius Junior Brazil national team match action")], "AP PHOTO", "Ngôi sao 26 tuổi tìm lại cảm hứng ghi bàn rực rỡ"),
            # Câu 4
            _slot("sentence", 4, [_ddgs("Endrick Brazil national team goal celebration")], "AP PHOTO", "Endrick vừa ghi bàn vừa kiến tạo cho đàn anh lập công"),
            _slot("sentence", 4, [_ddgs("Estevao Willian Brazil national team football")], "REUTERS", "Estêvão và Rayan góp công hoàn tất thắng lợi 7 sao"),
            # Câu 5
            _slot("sentence", 5, [_ddgs("Brazil national football team celebrating players")], "REUTERS", "Chiến thắng đậm nhất của Brazil sau 14 năm mang lại tín hiệu tích cực"),
        ],
    },
    # 07 (Nam — Quốc tế chi tiết 4)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Truyền nhân Messi lập cú đúp, Argentina vùi dập Costa Rica 7-0 để giải tỏa áp lực",
        "summary": (
            "Không chịu kém cạnh đại kình địch Brazil, đội tuyển Argentina cũng có màn trình diễn tưng bừng vào sáng ngày 18 tháng 11 theo giờ Việt Nam khi vùi dập Costa Rica tới 7-0 trên sân nhà Mario Alberto Kempes. "
            "Sau thất bại đáng quên trước Uruguay ở lượt trận trước, Albiceleste nhập cuộc đầy quyết tâm và sớm áp đặt thế trận ngay từ những phút đầu tiên. "
            "Tài năng trẻ được ví như truyền nhân của Lionel Messi là tiền vệ Nico Paz sắm vai người hùng khi mở tỷ số ở phút thứ tám và hoàn tất cú đúp trước giờ nghỉ ở phút 38. "
            "Xen giữa màn tỏa sáng đó là hai pha lập công sắc bén của tiền đạo Julián Álvarez ở các phút 35 và 43, trước khi sao mai Franco Mastantuono tiếp tục ghi dấu ấn trong cơn mưa bàn thắng ở hiệp hai. "
            "Chiến thắng 7 sao giúp nhà đương kim vô địch thế giới lấy lại sự tự tin cần thiết trong giai đoạn chuyển giao lực lượng."
        ),
        "source": "VietnamNet / Sportsmole",
        "news_source": "VIETNAMNET / SPORTSMOLE",
        "credit": "REUTERS / AP",
        "slots": [
            _slot("title", 0, [_ddgs("Nico Paz Argentina football match")], "REUTERS", "Nico Paz lập cú đúp giúp Argentina đại thắng Costa Rica 7-0"),
            _slot("title", 0, [_ddgs("Julian Alvarez Argentina football goal celebration")], "AP PHOTO", "Julián Álvarez bùng nổ với hai bàn thắng ngay trong hiệp một"),
            _slot("title", 0, [_ddgs("Argentina national football team celebrating goal")], "REUTERS", "Argentina lấy lại hình ảnh nhà vô địch trên sân nhà Córdoba"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("Estadio Mario Alberto Kempes Cordoba match")], "AP PHOTO", "Sân Mario Alberto Kempes bùng nổ với chiến thắng 7-0 của chủ nhà"),
            # Câu 2
            _slot("sentence", 2, [_local(ORTHER / "16.11.2026" / "images" / "v1_match_duel.jpg")], "REUTERS", "Albiceleste nhập cuộc áp đảo ngay từ tiếng còi khai cuộc"),
            # Câu 3
            _slot("sentence", 3, [_ddgs("Nico Paz Como Argentina midfielder celebration")], "AP PHOTO", "Tài năng trẻ Nico Paz mở tỷ số phút thứ 8 và hoàn tất cú đúp"),
            # Câu 4
            _slot("sentence", 4, [_local(ORTHER / "16.11.2026" / "images" / "v1_alvarez_goal.jpg")], "REUTERS", "Julián Álvarez ghi liền hai bàn ở phút 35 và 43"),
            _slot("sentence", 4, [_ddgs("Franco Mastantuono Argentina football")], "AP PHOTO", "Sao mai Franco Mastantuono tiếp tục khẳng định tài năng ở hiệp hai"),
            # Câu 5
            _slot("sentence", 5, [_ddgs("Lionel Scaloni Argentina coach touchline")], "REUTERS", "HLV Lionel Scaloni hài lòng với màn chuyển giao lực lượng trẻ"),
        ],
    },
    # 08 (Nữ — Quốc tế chi tiết 5)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Mauricio Pochettino chia tay tuyển Mỹ, bay chuyên cơ riêng sang tiếp quản Manchester United",
        "summary": (
            "Sáng ngày 18 tháng 11 theo giờ Việt Nam, trận hòa không bàn thắng trước Haiti tại lượt về tứ kết CONCACAF Nations League trên sân Cincinnati đã chính thức khép lại hành trình của HLV Mauricio Pochettino trên cương vị thuyền trưởng đội tuyển Mỹ. "
            "Nhờ thắng lợi áp đảo 6-0 ở lượt đi, tuyển Mỹ vẫn ung dung đi tiếp vào vòng bán kết và giành vé dự Gold Cup 2027 với tổng tỷ số 6-0. "
            "Ngay sau khi hoàn tất nghi thức chia tay các học trò và họp báo cuối cùng, chiến lược gia người Argentina lập tức lên chuyên cơ riêng do ban lãnh đạo Manchester United thuê sẵn để bay thẳng xuyên đêm sang Anh. "
            "Theo kế hoạch, sáng ngày 18 tháng 11 theo giờ địa phương, ông Pochettino đặt chân tới trung tâm huấn luyện Carrington để bắt tay ngay vào công việc dẫn dắt Quỷ đỏ, chuẩn bị cho trận ra mắt đầy thử thách gặp đại kình địch Liverpool tại Anfield."
        ),
        "source": "VietnamNet / Goal",
        "news_source": "VIETNAMNET / GOAL",
        "credit": "VNEXPRESS / REUTERS / AP",
        "slots": [
            _slot("title", 0, [_url(VNE_POCH)], "VNEXPRESS / AP", "Mauricio Pochettino hoàn tất trận cuối dẫn dắt đội tuyển Mỹ"),
            _slot("title", 0, [_local(ORTHER / "13.11.2026" / "images" / "short_1_old_trafford.jpg")], "REUTERS", "Manchester United bố trí chuyên cơ đón tân HLV trưởng"),
            _slot("title", 0, [_ddgs("TQL Stadium Cincinnati USMNT soccer")], "CONCACAF", "Tuyển Mỹ hòa Haiti 0-0 để đi tiếp với tổng tỷ số 6-0"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("USA Haiti CONCACAF Nations League match")], "AP PHOTO", "Trận đấu trên sân TQL Stadium khép lại nhiệm kỳ của Pochettino"),
            # Câu 2
            _slot("sentence", 2, [_ddgs("Christian Pulisic USMNT soccer team")], "REUTERS", "Tuyển Mỹ nhẹ nhàng giành vé bán kết và suất dự Gold Cup 2027"),
            # Câu 3
            _slot("sentence", 3, [_url("https://cdn.sanity.io/images/oyf3dba6/production/2fd6ad7b201676bdbf65b2913438373c7c01fc48-1800x1200.jpg?w=960&fit=max&auto=format"), _ddgs("Mauricio Pochettino press conference coach")], "REUTERS", "Chiến lược gia Argentina lập tức bay xuyên đêm sang Manchester"),
            _slot("sentence", 3, [_url("https://images.aircharterservice.com/blog/a-private-jet-parked-on-the-tarmac-near-an-airport-at-night.jpg"), _ddgs("private jet airport tarmac night")], "AIR CHARTER / REUTERS", "Chuyên cơ riêng đưa ông Pochettino sớm hội quân cùng Quỷ đỏ"),
            # Câu 4
            _slot("sentence", 4, [_local(ORTHER / "13.11.2026" / "images" / "short_1_poch_prep.jpg")], "REUTERS", "Pochettino bắt tay làm việc ngay tại Carrington trước đại chiến Liverpool"),
        ],
    },
    # 09 (Nam — Lướt nhanh Quốc tế)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "Nhóm: Sôi động bóng đá quốc tế",
        "title": "Nhật Bản thua sốc Paraguay, Ireland thắng đậm Kosovo tại League B Nations League",
        "summary": (
            "Ở các trận giao hữu quốc tế khu vực châu Á tối ngày 17 tháng 11, đội tuyển Nhật Bản bất ngờ gây thất vọng khi để thua Paraguay 1-2 ngay trên sân nhà sau hai bàn thua sớm trong hiệp một, trong khi Australia cũng gục ngã 0-2 trước Jordan còn Hàn Quốc thắng tối thiểu Qatar 1-0 nhờ pha lập công của Oh Se-hun. "
            "Tại League B UEFA Nations League rạng sáng ngày 18 tháng 11, Cộng hòa Ireland đánh bại Kosovo 3-0 với cú đúp của Troy Parrott, Bosnia và Herzegovina thắng Romania 2-1 còn Ukraine vượt qua Gruzia 1-0, trong khi cả ba cặp đấu giữa Hungary, Ba Lan và Israel gặp Bắc Ireland, Thụy Điển và Áo đều kết thúc với tỷ số hòa 1-1."
        ),
        "source": "Dân Trí / UEFA / Sofascore",
        "news_source": "DÂN TRÍ / UEFA",
        "credit": "AP PHOTO / REUTERS",
        "slots": [
            _slot("title", 0, [_ddgs("Japan national football team match action")], "AP PHOTO", "Đội tuyển Nhật Bản bất ngờ thất bại 1-2 trước Paraguay"),
            _slot("title", 0, [_ddgs("Troy Parrott Ireland national team goal")], "REUTERS", "Troy Parrott lập cú đúp giúp CH Ireland thắng Kosovo 3-0"),
            _slot("title", 0, [_ddgs("South Korea national football team match action")], "AP PHOTO", "Hàn Quốc giành chiến thắng 1-0 trên sân của Qatar"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("Japan Paraguay football friendly match")], "REUTERS", "Samurai Xanh nhận hai bàn thua ngay trong hiệp một trước Paraguay"),
            _slot("sentence", 1, [_ddgs("Jordan Australia football match")], "AP PHOTO", "Australia nhận thất bại 0-2 trước chủ nhà Jordan"),
            # Câu 2
            _slot("sentence", 2, [_ddgs("Republic of Ireland Kosovo Nations League match")], "UEFA", "CH Ireland thi đấu thăng hoa tại sân Aviva ở Dublin"),
            _slot("sentence", 2, [_ddgs("Poland Sweden Nations League football match")], "REUTERS", "Các trận đấu cân tài cân sức ở League B UEFA Nations League"),
        ],
    },
    # 10 (Nữ — Đông Nam Á chi tiết)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "Nhóm: Chuyển động bóng đá Đông Nam Á và Việt Nam",
        "title": "Supachok tỏa sáng giúp Thái Lan hạ Tajikistan 3-0, lần thứ 17 vô địch King's Cup trên sân nhà",
        "summary": (
            "Tối ngày 17 tháng 11 trên sân vận động tỉnh Sisaket, đội tuyển Thái Lan dưới sự dẫn dắt của HLV Anthony Hudson đã đánh bại Tajikistan với tỷ số đậm 3-0 để đăng quang tại trận chung kết King's Cup 2026. "
            "Bước ngoặt của trận đấu xảy ra ở phút 37 khi tiền vệ Nozim Babajanov bên phía Tajikistan phải nhận thẻ đỏ trực tiếp sau tình huống trọng tài kiểm tra công nghệ VAR. "
            "Chỉ bốn phút sau lợi thế hơn người, ngôi sao Supachok Sarachat xử lý kỹ thuật khéo léo trong vòng cấm trước khi sút chìm mở tỷ số cho chủ nhà. "
            "Sang đầu hiệp hai, chính Supachok tiếp tục ghi dấu ấn với pha đột phá kiến tạo giúp Teerasak Poeiphimai nhân đôi cách biệt ở phút 49, trước khi tiền đạo này hoàn tất cú đúp vào phút 75. "
            "Chiến thắng thuyết phục giúp Voi chiến giải tỏa cơn khát danh hiệu bằng chức vô địch King's Cup lần thứ 17 trong lịch sử, mang lại niềm vui vỡ òa cho Chủ tịch Liên đoàn Bóng đá Thái Lan Madam Pang."
        ),
        "source": "Thanh Niên / Dân Trí",
        "news_source": "THANH NIÊN / DÂN TRÍ",
        "credit": "THANH NIÊN / FAT",
        "slots": [
            _slot("title", 0, [_url(TN_THAI_1)], "THANH NIÊN / FAT", "Đội tuyển Thái Lan thắng đậm Tajikistan 3-0 ở chung kết King's Cup 2026"),
            _slot("title", 0, [_url(TN_THAI_3)], "THANH NIÊN / FAT", "Voi chiến nâng cao chiếc cúp vô địch lần thứ 17 trong lịch sử"),
            _slot("title", 0, [_url(TN_THAI_2)], "THANH NIÊN / FAT", "Supachok Sarachat tỏa sáng rực rỡ trên sân Sisaket"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("Thailand national football team blue jersey action")], "FAT", "Thầy trò HLV Anthony Hudson áp đảo đối thủ Trung Á"),
            # Câu 2
            _slot("sentence", 2, [_ddgs("Thailand Tajikistan football match action")], "FAT", "Thẻ đỏ phút 37 sau khi kiểm tra VAR khiến Tajikistan vỡ trận"),
            # Câu 3
            _slot("sentence", 3, [_url(TN_THAI_5)], "THANH NIÊN / FAT", "Supachok xử lý khéo léo mở tỷ số 1-0 ở phút 41"),
            # Câu 4
            _slot("sentence", 4, [_ddgs("Thailand national football team goal celebration blue jersey")], "FAT", "Teerasak Poeiphimai lập cú đúp ấn định thắng lợi 3-0"),
            # Câu 5
            _slot("sentence", 5, [_ddgs("Madam Pang Nualphan Lamsam Thailand football")], "FAT", "Madam Pang và người hâm mộ Thái Lan ăn mừng ngôi vô địch"),
        ],
    },
    # 11 (Nam — Lướt nhanh VN)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "Nhóm: Chuyển động bóng đá Đông Nam Á và Việt Nam",
        "title": "U19 Việt Nam hòa U19 Tajikistan 2-2 trong ngày chia tay giải giao hữu Panda Cup 2026",
        "summary": (
            "Cũng trong tối ngày 17 tháng 11 tại lượt trận cuối giải trẻ quốc tế Panda Cup 2026 diễn ra ở Trung Quốc, đội tuyển U19 Việt Nam đã cống hiến trận cầu rượt đuổi tỷ số hấp dẫn và cầm hòa U19 Tajikistan với kết quả 2-2. "
            "Tiền đạo Hoàng Công Hậu trở thành điểm sáng lớn nhất của đội bóng áo đỏ khi lập cú đúp với bàn mở tỷ số phút 36 và pha lập công quý giá ở phút 84 giữ lại 1 điểm cho thầy trò HLV Hoàng Anh Tuấn sau hai trận thua trước đó. "
            "Ở cặp đấu còn lại, U19 Trung Quốc gây bất ngờ khi đánh bại U19 Hàn Quốc 2-1 để lên ngôi vô địch với thành tích bất bại."
        ),
        "source": "VietnamNet / Bongdaplus",
        "news_source": "VIETNAMNET / BONGDAPLUS",
        "credit": "VFF / BONGDAPLUS",
        "slots": [
            _slot("title", 0, [_local(WEEKLY_16 / "Tin_15_1.jpg")], "VFF / THANH NIÊN", "Các cầu thủ trẻ Việt Nam thi đấu đầy nỗ lực tại Panda Cup 2026"),
            _slot("title", 0, [_local(WEEKLY_16 / "Tin_16_1.jpg")], "VFF / THANH NIÊN", "U19 Việt Nam khép lại giải đấu bằng trận hòa 2-2 trước Tajikistan"),
            _slot("title", 0, [_ddgs("China youth football team red jersey match")], "CFA", "U19 Trung Quốc đánh bại Hàn Quốc 2-1 để vô địch giải đấu"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("Vietnam youth football team red jersey match action")], "VFF", "U19 Việt Nam và U19 Tajikistan tạo thế trận đôi công hấp dẫn"),
            # Câu 2
            _slot("sentence", 2, [_ddgs("Hoang Anh Tuan Vietnam football coach")], "VFF", "HLV Hoàng Anh Tuấn đánh giá cao tinh thần không bỏ cuộc của học trò"),
            # Câu 3
            _slot("sentence", 3, [_ddgs("China South Korea youth football match")], "CFA", "Chủ nhà Trung Quốc đăng quang ngôi vô địch Panda Cup 2026"),
        ],
    },
    # 12 (Nữ — Lướt nhanh VN)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "Nhóm: Chuyển động bóng đá Đông Nam Á và Việt Nam",
        "title": "CLB Công an TP.HCM tự tin chơi tấn công trước đương kim vô địch Buriram United tại Shopee Cup",
        "summary": (
            "Hướng tới lượt trận sân nhà tại Cúp C1 Đông Nam Á 2026-2027 diễn ra vào lúc 18 giờ tối nay ngày 18 tháng 11 trên sân Bình Dương, thầy trò CLB Công an TP.HCM đứng trước thử thách cực đại mang tên đương kim vô địch Buriram United. "
            "Dù đối thủ đến từ Thái Lan được đánh giá cao hơn về kinh nghiệm và dàn ngoại binh, HLV Arthur Diles vẫn khẳng định đội bóng ngành công an sẽ không co cụm phòng ngự mà chủ động triển khai lối chơi tấn công nhằm hướng tới mục tiêu giành trọn ba điểm."
        ),
        "source": "Thanh Niên / VOV",
        "news_source": "THANH NIÊN / VOV",
        "credit": "THANH NIÊN",
        "slots": [
            _slot("title", 0, [_url(TN_CATPHCM_1)], "THANH NIÊN", "HLV Arthur Diles khẳng định CLB Công an TP.HCM sẽ chơi tấn công"),
            _slot("title", 0, [_url(TN_CATPHCM_3)], "THANH NIÊN", "Tiền đạo Tiến Linh và đồng đội sẵn sàng nghênh đón Buriram United"),
            _slot("title", 0, [_url(TN_CATPHCM_2)], "THANH NIÊN", "Các cầu thủ trẻ CLB Công an TP.HCM tự tin trước trận đấu 18 giờ tối nay"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("Binh Duong Go Dau stadium Vietnam football")], "THANH NIÊN", "Cuộc đối đầu tâm điểm tại sân Bình Dương thuộc Shopee Cup 2026-2027"),
            _slot("sentence", 1, [_ddgs("Buriram United football team celebration match")], "SHOPEE CUP", "Đương kim vô địch Buriram United sở hữu đội hình giàu kinh nghiệm"),
            # Câu 2
            _slot("sentence", 2, [_ddgs("Nguyen Tien Linh V-League football match action")], "THANH NIÊN", "CLB Công an TP.HCM đặt mục tiêu giành trọn 3 điểm trên sân nhà"),
            _slot("sentence", 2, [_ddgs("V-League Vietnam club football match")], "THANH NIÊN", "Toàn đội quyết tâm cống hiến lối đá đẹp mắt trước khán giả nhà"),
        ],
    },
    # 13 (Nam — Lướt nhanh VN)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "Nhóm: Chuyển động bóng đá Đông Nam Á và Việt Nam",
        "title": "Sơ duyệt sân khấu gần 2000 chỗ ngồi cho Lễ khai mạc Đại hội Thể thao toàn quốc 2026 tại TP.HCM",
        "summary": (
            "Trong hai ngày 17 và 18 tháng 11, công tác chuẩn bị cho sự kiện thể thao lớn nhất cả nước là Đại hội Thể thao toàn quốc lần thứ X năm 2026 bước vào giai đoạn nước rút tại TP.HCM. "
            "Ban tổ chức đang tiến hành sơ duyệt và hoàn thiện các hạng mục cuối cùng cho khu vực sân khấu gần 2000 chỗ ngồi nổi bật với biểu tượng ngọn đuốc vàng bên Công viên Bờ sông Sài Gòn, sẵn sàng cho chương trình thảm xanh Đại lộ vinh quang và Lễ khai mạc chính thức vào tối ngày 21 tháng 11."
        ),
        "source": "Thanh Niên / Cục TDTT",
        "news_source": "THANH NIÊN / CỤC TDTT",
        "credit": "THANH NIÊN",
        "slots": [
            _slot("title", 0, [_url(TN_DH_1)], "THANH NIÊN", "Cận cảnh sân khấu Lễ khai mạc Đại hội Thể thao toàn quốc 2026"),
            _slot("title", 0, [_url(TN_DH_2)], "THANH NIÊN", "Điểm nhấn ngọn đuốc vàng rực rỡ bên bờ sông Sài Gòn"),
            _slot("title", 0, [_url(TN_DH_3)], "THANH NIÊN", "Khán đài gần 2000 chỗ ngồi đang được hoàn thiện khâu cuối"),
            # Câu 1
            _slot("sentence", 1, [_url(TN_DH_4)], "THANH NIÊN", "Công tác chuẩn bị tại TP.HCM diễn ra khẩn trương trong ngày 17 và 18 tháng 11"),
            # Câu 2
            _slot("sentence", 2, [_url(TN_DH_5)], "THANH NIÊN", "Toàn cảnh không gian hoành tráng sẵn sàng cho đêm khai mạc 21 tháng 11"),
            _slot("sentence", 2, [_url(TN_DH_6)], "THANH NIÊN", "Hệ thống âm thanh ánh sáng hiện đại phục vụ Đại lộ vinh quang"),
        ],
    },
    # 14 (Nữ — Tinh hoa thế giới chi tiết 1)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "Nhóm: Tinh hoa thể thao thế giới và hậu trường",
        "title": "Lê Quang Liêm leo hạng 12 thế giới, tạm thất thế trước Hans Niemann ở bán kết lượt đi nhánh 5-8",
        "summary": (
            "Tại Giải vô địch cờ vua toàn năng thế giới 2026 đang diễn ra ở thủ đô Budapest của Hungary, kỳ thủ số một Việt Nam Lê Quang Liêm vừa ghi nhận bước nhảy vọt ấn tượng trên bảng xếp hạng thế giới. "
            "Sau khi kết thúc vòng bảng với thành tích bất bại gồm hai ván thắng và tám ván hòa để xếp nhì bảng B sau Fabiano Caruana, Quang Liêm tích lũy thêm 10,4 điểm Elo trực tiếp lên mức 2742,4, qua đó áp sát tốp 10 ở vị trí hạng 12 thế giới và cầm chắc tối thiểu 32000 USD tiền thưởng. "
            "Bước vào loạt trận bán kết lượt đi nhánh tranh hạng 5 đến 8 gặp kỳ thủ Mỹ Hans Niemann, đại diện Việt Nam khởi đầu thuận lợi khi dẫn trước 6,5-5,5 sau bốn ván cờ chớp và hai ván cờ nhanh. "
            "Tuy nhiên, sai sót ở ván cờ tiêu chuẩn quyết định tính 8 điểm khiến Quang Liêm để thua sau 46 nước và tạm bị đối thủ dẫn ngược 6,5-13,5 trước khi bước vào lượt về tái đấu trong tối ngày 18 tháng 11."
        ),
        "source": "Thanh Niên / Lao Động",
        "news_source": "THANH NIÊN / LAO ĐỘNG",
        "credit": "THANH NIÊN / FIDE",
        "slots": [
            _slot("title", 0, [_url(TN_QL_1)], "THANH NIÊN", "Lê Quang Liêm đạt thứ hạng 12 thế giới cao nhất sự nghiệp"),
            _slot("title", 0, [_local(WEEKLY_16 / "Tin_23_2.jpg")], "TOTAL CHESS", "Giải cờ vua toàn năng thế giới 2026 quy tụ dàn siêu đại kiện tướng tại Budapest"),
            _slot("title", 0, [_ddgs("Hans Niemann chess player tournament")], "FIDE", "Kỳ thủ Mỹ Hans Niemann đối đầu Lê Quang Liêm ở nhánh 5-8"),
            # Câu 1
            _slot("sentence", 1, [_url(TN_QL_2)], "THANH NIÊN", "Phong độ ổn định giúp kỳ thủ Việt Nam bứt phá mạnh mẽ"),
            # Câu 2
            _slot("sentence", 2, [_local(WEEKLY_16 / "Tin_23_8.jpg")], "WIKIMEDIA COMMONS", "Quang Liêm bất bại cả 10 ván vòng bảng và chạm mốc Elo 2742,4"),
            _slot("sentence", 2, [_local(WEEKLY_16 / "Tin_23_9.jpg")], "TOTAL CHESS / FIDE", "Nhì bảng B mang về ít nhất 32000 USD tiền thưởng cho kỳ thủ số một Việt Nam"),
            # Câu 3
            _slot("sentence", 3, [_local(ORTHER / "12.11.2026" / "images" / "Tin_05_2.jpg")], "VNEXPRESS", "Quang Liêm dẫn trước 6,5-5,5 sau các ván cờ chớp và cờ nhanh"),
            # Câu 4
            _slot("sentence", 4, [_ddgs("Hans Niemann chess board game")], "FIDE", "Hans Niemann thắng ván cờ tiêu chuẩn 46 nước để dẫn ngược ở lượt đi"),
            _slot("sentence", 4, [_local(WEEKLY_16 / "Tin_23_5.jpg")], "WIKIMEDIA COMMONS", "Hai kỳ thủ sẽ tái đấu quyết định ở lượt về tối 18 tháng 11"),
        ],
    },
    # 15 (Nam — Tinh hoa thế giới chi tiết 2)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "Nhóm: Tinh hoa thể thao thế giới và hậu trường",
        "title": "Alexander Zverev sớm đoạt vé bán kết ATP Finals 2026, Arthur Fils thắng ngược Rafael Jodar",
        "summary": (
            "Rạng sáng ngày 18 tháng 11 theo giờ Việt Nam, lượt trận thứ hai bảng John McEnroe tại giải quần vợt danh giá cuối năm ATP Finals 2026 ở Turin đã xác định tấm vé vào bán kết đầu tiên. "
            "Tay vợt số một thế giới Alexander Zverev tái hiện lại ưu thế của trận chung kết Mỹ mở rộng khi đánh bại tay vợt Mỹ Ben Shelton sau hai set đấu với tỷ số 6-2 và 7-6, qua đó nâng thành tích lên hai trận toàn thắng và sớm ghi tên mình vào vòng bốn tay vợt mạnh nhất. "
            "Ở trận đấu còn lại của bảng đấu này, hai gương mặt trẻ lần đầu dự giải đã cống hiến màn so tài ba set kịch tính, nơi tay vợt người Pháp Arthur Fils ngược dòng hạ gục tài năng Tây Ban Nha Rafael Jodar với các tỷ số 4-6, 6-2 và 6-2 để giành chiến thắng đầu tay."
        ),
        "source": "ATP Tour / VietnamNet",
        "news_source": "ATP TOUR / VIETNAMNET",
        "credit": "ATP TOUR / REUTERS",
        "slots": [
            _slot("title", 0, [_local(WEEKLY_16 / "Tin_26_3.jpg")], "REUTERS", "Alexander Zverev sớm giành quyền vào bán kết ATP Finals 2026"),
            _slot("title", 0, [_ddgs("Ben Shelton tennis serve match")], "REUTERS", "Ben Shelton thất bại sau hai set trước tay vợt số một thế giới"),
            _slot("title", 0, [_ddgs("Arthur Fils tennis player match")], "ATP TOUR", "Arthur Fils ngược dòng ấn tượng ở trận đấu ba set tại Turin"),
            # Câu 1
            _slot("sentence", 1, [_local(WEEKLY_16 / "Tin_26_5.jpg")], "ATP TOUR", "Nhà thi đấu Inalpi Arena tại Turin sôi động ở ngày thi đấu thứ ba"),
            # Câu 2
            _slot("sentence", 2, [_local(WEEKLY_16 / "Tin_26_6.jpg")], "AP PHOTO", "Zverev thể hiện bản lĩnh với thắng lợi 6-2, 7-6 trước Ben Shelton"),
            _slot("sentence", 2, [_local(WEEKLY_16 / "Tin_26_4.jpg")], "ATP TOUR", "Tay vợt Đức nâng thành tích lên 2-0 tại bảng John McEnroe"),
            # Câu 3
            _slot("sentence", 3, [_ddgs("Arthur Fils tennis backhand match")], "ATP TOUR", "Arthur Fils ngược dòng đánh bại Rafael Jodar 4-6, 6-2, 6-2"),
            _slot("sentence", 3, [_ddgs("Rafael Jodar tennis player court")], "ATP TOUR", "Tài năng trẻ Tây Ban Nha Rafael Jodar thi đấu đầy nỗ lực"),
        ],
    },
    # 16 (Nữ — Lướt nhanh Bi kịch — Memorial Grayscale)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "Nhóm: Tinh hoa thể thao thế giới và hậu trường",
        "title": "Bóng đá trẻ Argentina bàng hoàng trước sự ra đi của tiền vệ 16 tuổi Abel Nunez",
        "summary": (
            "Sáng ngày 18 tháng 11, truyền thông thể thao thế giới đồng loạt bày tỏ niềm tiếc thương trước bi kịch sân cỏ vừa xảy ra tại Argentina liên quan đến cầu thủ trẻ Abel Nunez. "
            "Tiền vệ 16 tuổi thuộc biên chế đội trẻ câu lạc bộ FC Ezeiza đã không qua khỏi sau bốn ngày nhập viện phẫu thuật khẩn cấp vì chấn thương sọ não nặng, xuất phát từ tình huống bị đối phương phá bóng cực mạnh ở cự ly gần đập trúng đầu ngay trong trận đấu."
        ),
        "source": "VnExpress / Tuổi Trẻ",
        "news_source": "VNEXPRESS / TUỔI TRẺ",
        "credit": "VNEXPRESS / FC EZEIZA",
        "slots": [
            _slot("title", 0, [_url("https://album.mediaset.es/eimg/2026/11/16/abel-nunez-futbolista-de-las-categorias-inferiores-del-fc-ezeiza-16-9-aspect-ratio-default-1060819_da39.jpg"), _url("https://media.dib.com.ar/p/02a15ad2841accdf71ccf89b17ef6bf8/adjuntos/377/imagenes/100/060/0100060874/1000x0/smart/abel-nunez-ezeiza-fc-rs.jpg")], "MEDIASET / FC EZEIZA", "Tài năng trẻ 16 tuổi Abel Nunez đột ngột qua đời sau tai nạn sân cỏ"),
            _slot("title", 0, [_local(ORTHER / "04.11.2026" / "images" / "Tin_02_4.jpg")], "WIKIMEDIA COMMONS", "Làng bóng đá Argentina tiếc thương cầu thủ xấu số"),
            _slot("title", 0, [_local(ORTHER / "16.11.2026" / "images" / "v1_bombonera_night.jpg")], "REUTERS", "Lời cảnh tỉnh về an toàn chấn thương đầu trong bóng đá trẻ"),
            # Câu 1
            _slot("sentence", 1, [_local(ORTHER / "16.11.2026" / "images" / "v1_arg_fans.jpg")], "REUTERS", "Giới bóng đá Argentina bàng hoàng trước sự ra đi của Abel Nunez"),
            # Câu 2
            _slot("sentence", 2, [_ddgs("football pitch grass closeup match ball")], "REUTERS", "Tai nạn hi hữu trên sân cỏ cướp đi sinh mạng tài năng 16 tuổi"),
        ],
    },
    # 17 (Nam — Lướt nhanh Hậu trường)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "Nhóm: Tinh hoa thể thao thế giới và hậu trường",
        "title": "Wayne Rooney thừa nhận từng có ý định tự tử trong giai đoạn đỉnh cao tại Manchester United",
        "summary": (
            "Cũng trong sáng ngày 18 tháng 11, cựu danh thủ Wayne Rooney khiến làng bóng đá Anh chấn động khi công khai thừa nhận từng nghĩ tới việc tự kết liễu cuộc đời ngay trong thời kỳ đỉnh cao sự nghiệp khoác áo Manchester United. "
            "Cựu thủ quân Tam Sư cho biết áp lực khổng lồ từ truyền thông và sự kỳ vọng đã đẩy anh rơi vào khủng hoảng tâm lý kéo dài, buộc phải tìm đến rượu để giải tỏa trước khi kịp thời vực dậy nhờ sự đồng hành của gia đình."
        ),
        "source": "VnExpress / Mirror",
        "news_source": "VNEXPRESS / MIRROR",
        "credit": "VNEXPRESS / AP",
        "slots": [
            _slot("title", 0, [_url(VNE_ROONEY_1)], "VNEXPRESS", "Wayne Rooney chia sẻ góc khuất tâm lý gây sốc truyền thông Anh"),
            _slot("title", 0, [_url("https://e0.365dm.com/16/10/2048x1152/skysports-wayne-rooney-manchester-city_3801513.jpg?20161005181456"), _ddgs("Wayne Rooney Manchester United celebration goal")], "SKY SPORTS / MAN UTD", "Giai đoạn đỉnh cao nhiều áp lực của Rooney tại Old Trafford"),
            _slot("title", 0, [_ddgs("Wayne Rooney Manchester United Old Trafford")], "AP PHOTO", "Cựu thủ quân tuyển Anh từng vật lộn với chứng trầm cảm kéo dài"),
            # Câu 1
            _slot("sentence", 1, [_ddgs("Wayne Rooney Manchester United celebration")], "AP PHOTO", "Rooney thừa nhận từng suy nghĩ tiêu cực khi còn thi đấu đỉnh cao"),
            # Câu 2
            _slot("sentence", 2, [_local(ORTHER / "13.11.2026" / "images" / "short_1_ot_2.jpg"), _ddgs("Old Trafford stadium night exterior Manchester")], "REUTERS", "Áp lực khổng lồ tại Old Trafford từng đè nặng lên cựu danh thủ Anh"),
        ],
    },
]
