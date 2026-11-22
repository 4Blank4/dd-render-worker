# -*- coding: utf-8 -*-
"""
daily_22_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 22.11.2026
(Tổng hợp song hành báo Việt Nam & Thế Giới: 12:00 ngày 21.11 đến 09:30 ngày 22.11.2026).
Cấu trúc ĐỘNG 100% theo sự kiện thực tế:
  - Intro (00): Song giọng Nữ (Ngọc Huyền #14) & Nam (Minh Quân Pro #15), hide_title=True
  - 22 bản tin chính (01–22): Mỗi tin 1 vấn đề trọng tâm (4–5 câu), luân phiên Nam / Nữ
  - Mục 23 (CÁC TIN THỂ THAO KHÁC): 100% Giọng Nữ (Ngọc Huyền #14) điểm nhanh các kết quả phụ trước Outro
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent
DAILY_21 = ROOT / "outputs" / "21.11.2026" / "images"
DAILY_20 = ROOT / "outputs" / "20.11.2026" / "images"
DAILY_19 = ROOT / "outputs" / "19.11.2026" / "images"
ORTHER_14 = ROOT / "outputs" / "Orther" / "14.11.2026" / "images"
ORTHER_12 = ROOT / "outputs" / "Orther" / "12.11.2026" / "images"
ORTHER_08 = ROOT / "outputs" / "Orther" / "08.11.2026" / "images"


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


# ── URL ảnh báo chí sạch gốc 21–22.11.2026 (Việt Nam & Thế Giới) ──

# Đại hội Thể thao toàn quốc 2026 khai mạc bên sông Sài Gòn
TN_DH_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/tnw-17952647939163340916704444917640g130542549375725460027d33b9b4dda63fbd8676a25c27e4375-1795269289906677932095.jpg"
TN_DH_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/tnw-17952640887993340916704444917640g1305425493757254600849632e0bcb12de05af67f3638e2e578-1795269290857416615855.jpg"
TN_DH_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/tnw-17952703321743340916704444917640g1305425493757254600d50664244e241fc9fe897227291ab5e5-17952722795111678949892.jpg"
TN_DH_4 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/tnw-17952703388773340916704444917640g1305425493757254600229191dff168a29412c1821c30106f85-1795272279551892162410.jpg"
TN_DH_5 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/tnw-17952672507563340916704444917640g1305425493757254600bc741357bacbac2df11efd0892e02223-17952699226771348702243.jpg"
TT_DH_1 = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/21/83c77d95-d348-4bad-b581-88da5ca4ce27-17952694024061061492699.jpeg"
TT_DH_PTT = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/21/pho-thu-tuong-pham-thi-thanh-tra-le-khai-mac-dai-hoi-the-thao-toan-quoc-1795274960383541640380.jpg"
DT_DH_1 = "https://cdnphoto.dantri.com.vn/2Hn4YuRWG6LDa2EPQY5eQzAI6P8=/thumb_w/1920/2026/11/21/3-edited-1795277662103.jpg"
DT_DH_2 = "https://cdnphoto.dantri.com.vn/ApExztT3tB7Og40dnFGaRbY6nls=/thumb_w/1020/2026/11/21/khaimac5nhuhuy21-11-26-1795279325721.jpeg"
VNE_DH_1 = "https://i1-thethao.vnecdn.net/2026/11/21/7-1795272493.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=UlSWNstYrPYaSQ_dTbmxkw"

# Watson Nguyễn vs Phạm Thanh Bảo
TT_BOI_1 = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/21/watson-nguyen-pham-thanh-bao-1-17952727733141121467134-83-0-841-1448-crop-17952727930142076100935.png"
TT_BOI_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/5/edit-watson-nguyen-1-1793858719987980249763.jpeg"
TT_BOI_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/21/6f14466d-98aa-4892-ab44-700e9fdb8688-17952731720731073308591.png"

# Esports tại Đại hội Toàn quốc
TT_ESP_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/21/91444430918396768407023378087195807580113816n11zon-1795252600415301397157.jpg"
TT_ESP_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/21/1795251248423652499672771735195265249967277173519527156273287ab8ac541632d0ef2478483-1795251798062148874064.jpg"

# V-League: Nam Định 2-1 Hải Phòng & Đồng Nai 1-3 Hà Nội & Đà Nẵng - Ninh Bình
TN_ND_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/179526496394020554668242885303635923414894611837491e25fc71926a35fb2aad0097ac8f4dd8-17952650177062083279002.jpg"
TN_ND_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/17952628577892055466824288530363592341489461183749ab8e775c52b90fe24700c1b8c1e588c9-1795262903765621167932.jpg"
DT_ND_1 = "https://cdnphoto.dantri.com.vn/sbnsOBMxvWKt_UA031rqj3YQbsw=/thumb_w/1020/2026/11/21/clb-nam-dinh-26-1795268937973.jpg"
DT_ND_2 = "https://cdnphoto.dantri.com.vn/jmMOB0j399t63d3R2zeC6gW_zbs=/thumb_w/1020/2026/11/21/clb-nam-dinh-30-1795268932839.jpg"
TN_HN_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/quoc-lo-tpdn-vs-hnfc-clb-17952612832091791020005.jpg"
TN_HN_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/tpdn-vs-hnfc-clb1-1795261283108838097177.jpg"
TN_HN_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/tpdn-vs-hnfc-clb-1795264095911418139097.jpg"
TN_DN_NB_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/5-8-1920x1277-1795309399346365294098.jpg"
TN_DN_NB_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/1-13-1920x1261-1795309399505486375486.jpg"
TN_VL_SUN = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/8-8-1920x1251-1795268307762155031722.jpg"

# U17 Việt Nam vs U17 New Zealand & FVS & CAHN & Quang Liêm & ĐNA 2027
TN_U17_NL = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/nguyen-luc-1795263677906493284280.jpg"
TN_U17_FVS = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/u17-vietnam-u17-bi-2-1795186706827250288634.jpg"
TN_U17_NZ1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/5-1795266328344383338032.jpg"
TN_U17_NZ2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/2-1795253917716270793801.jpg"
VNE_U17_BE1 = "https://i1-thethao.vnecdn.net/2026/11/21/img-1795256741-3279-1795256854.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=fDGFT-UaesgmAt7tKpIhog"
VNE_U17_BE2 = "https://i1-thethao.vnecdn.net/2026/11/21/IMG-6616-3001-1795256854.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=EUVmzdNwF5u1LREjNsZmIw"
TN_CAHN_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/81290366310667289892767152525320632567161806n-1795257097371148190256.jpg"
TN_CAHN_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/81222402616683429615368702912982825507861103n-1795257148392887621472.jpg"
VNE_QL_1 = "https://i1-thethao.vnecdn.net/2026/11/21/quang-lie-m-1795252550-2480-1795252654.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=EpdCLebjg5E4QPJdhUtIDA"
VNE_QL_2 = "https://i1-thethao.vnecdn.net/2026/11/21/quang-lie-m-6985-1795252654.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=t-j6K6wn6-pipuiMlttnpA"
TT_INDO_4 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/21/indonesia-celebration-1795237930492307071767.jpg"
DT_U17_AFC = "https://cdnphoto.dantri.com.vn/je6tQ9e-5VO2BIQm2-C70liMpLk=/thumb_w/1020/2026/11/21/u17chauaaseanfootball21-11-26-1795236878429.jpeg"

# Man City 1-1 Fulham
VNE_MC_1 = "https://i1-thethao.vnecdn.net/2026/11/22/AP26325476591688-5458-1795307558.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=sWKX2ysrV8_C09di1IwhcQ"
VNE_MC_2 = "https://i1-thethao.vnecdn.net/2026/11/21/anderson-9019-1795271156.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=x6M2jPEROjga4bg_VXXBUw"
DT_MC_1 = "https://cdnphoto.dantri.com.vn/0IiVeXih2EjUn1foTOzPEhHLgCs=/thumb_w/1020/2026/11/21/erling-braut-haaland-manchester-city-1124648800-1795277199994.jpg"
DT_MC_2 = "https://cdnphoto.dantri.com.vn/rhFm2-41srFQt-om7tUDE3H_jNQ=/thumb_w/1020/2026/11/21/erling-haaland-manchester-city-scores-1124648617-1795277200306.jpg"
DT_MC_3 = "https://cdnphoto.dantri.com.vn/1sUes3mV9JO60PrnH0iGItR9K6M=/thumb_w/1020/2026/11/21/haaland-1795277551157.jpg"
DT_MC_MAR = "https://cdnphoto.dantri.com.vn/xrgXtM6Nq7xUXUvzuStKVvnzFNw=/thumb_w/1020/2026/11/21/maresca-1795277549074.jpg"

# Chelsea 1-4 Leeds
VNE_CHE_1 = "https://i1-thethao.vnecdn.net/2026/11/22/xabialonsomanagerchelsealooks1-9861-7333-1795297751.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=r7OZ6cj2Ko2sfbcsdqKkQA"
VNE_CHE_2 = "https://i1-thethao.vnecdn.net/2026/11/22/2026-chelsea-manager-xabi-alon-5936-7416-1795297750.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=ZT0eTnK6X_a3UhYtXszx9w"
VNE_CHE_3 = "https://i1-thethao.vnecdn.net/2026/11/22/ket-qua-bong-da-chelsea-1-4-le-3981-2443-1795297750.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=_UAeR0y8KAkrh7PVjKNI9A"
DT_CHE_1 = "https://cdnphoto.dantri.com.vn/HMi3MGH0ORzhrtIfV3ApBxV7VY0=/thumb_w/1020/2026/11/22/chelsea-1-1795303256774.jpg"
DT_CHE_2 = "https://cdnphoto.dantri.com.vn/PNpOj_ZeBb_MCs4c2pryavRED20=/thumb_w/1020/2026/11/22/chelsea-2-1795303255694.jpg"

# Arsenal 2-2 Newcastle
VNE_ARS_1 = "https://i1-thethao.vnecdn.net/2026/11/22/AP26325684555914-1795299247-5633-1795299981.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=CsNLCxheleC1gqg33jQruQ"
VNE_ARS_2 = "https://i1-thethao.vnecdn.net/2026/11/22/ap26325673408928-1795299973-7845-1795299982.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=LQ5dkShQtKkwMo0vofJVDg"
VNE_ARS_3 = "https://i1-thethao.vnecdn.net/2026/11/22/ap26325641047502-1795299974-7213-1795299982.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Yhf2pPI5hxYlWBwj7f2q7w"
VNE_ARS_4 = "https://i1-thethao.vnecdn.net/2026/11/22/AP26325693869616-9287-1795306419.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=ulD-6jbKbk1YTq-s2_oDwQ"
DT_ARS_1 = "https://cdnphoto.dantri.com.vn/hhTmTQQr_zAClv7gIbsqAKqk4vs=/thumb_w/1020/2026/11/22/arsenal-1-1795300682702.jpg"
DT_ARS_2 = "https://cdnphoto.dantri.com.vn/W50wCzxFyS_5hA1n86W2UJTKXMM=/thumb_w/1020/2026/11/22/arsenal-2-1795300839556.jpg"
SKY_ARS_NEW = "https://e0.365dm.com/26/11/1600x900/skysports-malick-thiaw-newcastle_7412895.jpg?20261121194652"

# Tottenham 2-0 Ipswich & Bournemouth
SKY_SPURS_1 = "https://e0.365dm.com/26/11/1600x900/skysports-tottenham-spurs-luca-williams-barnett_7412663.jpg?20261121173422"

# Real Madrid 2-1 Celta Vigo
VNE_RMA_1 = "https://i1-thethao.vnecdn.net/2026/11/22/AP26325731408005-1-1795301548-4109-1795301911.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=69HrzRVXq-ydJCGwF5_D8Q"
VNE_RMA_2 = "https://i1-thethao.vnecdn.net/2026/11/22/AP26325750379086-1-1795301564-6506-1795301911.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=2h0Vug0bvZ6SdY1kbk3CvA"
VNE_RMA_3 = "https://i1-thethao.vnecdn.net/2026/11/22/AP26325777583242-1-1795301585-9590-1795301912.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=6y1bJ-6B6NZMu8A-yC-Jkw"
DT_RMA_1 = "https://cdnphoto.dantri.com.vn/fiL_7EnAtcWIGeGDNljRDDj-S-M=/thumb_w/1020/2026/11/22/mbappe-1795304731533.jpg"
DT_RMA_2 = "https://cdnphoto.dantri.com.vn/ysjAsHPRT84UBGuSqNbm6A_h808=/thumb_w/1020/2026/11/22/real-1795304732876.jpg"

# PSG & Doué
SKY_PSG_DOUE = "https://e0.365dm.com/26/11/1600x900/skysports-doue-psg_7413016.jpg?20261121215948"

# Messi & Inter Miami
TN_MESSI_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/messi-17953100026131801351791.jpg"
TN_MESSI_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/messi-mls-17953100026401861527854.jpg"

# ATP Finals 2026
VNE_ATP_1 = "https://i1-thethao.vnecdn.net/2026/11/22/ap26325570285477-1795298634-2474-1795298645.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=dSTpbAw-ZSofFkITjxBn5g"
VNE_ATP_2 = "https://i1-thethao.vnecdn.net/2026/11/22/ap26325769333657-1795298637-9522-1795298645.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=iCFdjVlIQ_BMbk4UHYg7kg"
DT_ATP_1 = "https://cdnphoto.dantri.com.vn/TWExODmpCDyHYg6o2xHC-88VBsw=/thumb_w/1020/2026/11/21/alcaraz-1795278482166.jpg"
DT_ATP_2 = "https://cdnphoto.dantri.com.vn/CgV5RY9hBAMQG-kmUtKicsOSqWQ=/thumb_w/1020/2026/11/22/zverev-1795299868170.jpg"

# F1 Academy, Rugby, Golf, Indonesia, Đua ghe Ngo, U17 Nhật Bản & FIFA 15 tuổi
SKY_F1_ACA = "https://e0.365dm.com/26/11/1600x900/skysports-f1-f1-academy_7413063.jpg?20261122003316"
SKY_RUGBY_FR = "https://e1.365dm.com/26/11/1600x900/skysports-antoine-dupont-france_7413058.jpg"
SKY_RUGBY_WA = "https://e1.365dm.com/26/11/1600x900/skysports-louis-rees-zammit_7413047.jpg"
SKY_LPGA = "https://e0.365dm.com/26/11/1600x900/skysports-a-lim-kim-lpga-cme-group-tour_7413021.jpg?20261121220647"
TT_INDO_THOHIR = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/21/erick-thohir-1795267315168473951769.jpg"
TN_U17_JAP = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/8e6f23f5-8bcf-47be-b211-18de758c00b5png-1795271939847819483452.jpg"
VNE_U15_U17 = "https://i1-thethao.vnecdn.net/2026/11/21/FIFA-Under-15-World-Cup-Festiv-4122-2354-1795227327.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=BZtbhHTRJcCkMVRBLqPuFw"
TT_GHENGO_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/21/base64-179525600870397527295.jpeg"
DT_POCH = "https://cdnphoto.dantri.com.vn/wbP-H3wcd4OTPg72o_zEko6OEBw=/thumb_w/1020/2026/11/21/man-utd-1-1795236283129.jpg"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 22.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 22 tháng 11 năm 2026, cập nhật những sự kiện nóng nhất tại Việt Nam và trên toàn thế giới. "
        "Ở sân chơi quốc nội, Đại hội Thể thao toàn quốc 2026 chính thức khai mạc rực rỡ bên dòng sông Sài Gòn, còn ở V-League, Nam Định giữ vững ngôi đầu bảng trong khi Hà Nội FC ngược dòng ngoạn mục trên sân Đồng Nai. "
        "Tại Ngoại hạng Anh và La Liga, Man City hòa Fulham đầy tranh cãi khi VAR từ chối bàn thắng của Erling Haaland, Chelsea thảm bại 1-4 trước Leeds ngay tại Stamford Bridge, Arsenal chia điểm trên sân Newcastle, còn Real Madrid thắng ngược Celta Vigo dù Kylian Mbappé sút hỏng phạt đền. "
        "Cùng thất bại sốc 0-3 của Inter Miami trước Columbus Crew dù Lionel Messi đoạt Vua phá lưới MLS, chung kết trong mơ ATP Finals giữa Carlos Alcaraz và Alexander Zverev, cú sốc ở UFC Qatar, sức nóng F1 Las Vegas và nhiều tin thể thao đáng chú ý khác ngay sau đây."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí / BBC Sport / ESPN / Sky Sports",
    "news_source": "VIỆT NAM & THẾ GIỚI",
    "credit": "ĐIỂM ĐỌC TỔNG HỢP",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 22 tháng 11 năm 2026, cập nhật những sự kiện nóng nhất tại Việt Nam và trên toàn thế giới.",
        },
        {
            "voice_preset": "primary",
            "text": "Ở sân chơi quốc nội, Đại hội Thể thao toàn quốc 2026 chính thức khai mạc rực rỡ bên dòng sông Sài Gòn, còn ở V-League, Nam Định giữ vững ngôi đầu bảng trong khi Hà Nội FC ngược dòng ngoạn mục trên sân Đồng Nai.",
        },
        {
            "voice_preset": "secondary",
            "text": "Tại Ngoại hạng Anh và La Liga, Man City hòa Fulham đầy tranh cãi khi VAR từ chối bàn thắng của Erling Haaland, Chelsea thảm bại 1-4 trước Leeds ngay tại Stamford Bridge, Arsenal chia điểm trên sân Newcastle, còn Real Madrid thắng ngược Celta Vigo dù Kylian Mbappé sút hỏng phạt đền.",
        },
        {
            "voice_preset": "primary",
            "text": "Cùng thất bại sốc 0-3 của Inter Miami trước Columbus Crew dù Lionel Messi đoạt Vua phá lưới MLS, chung kết trong mơ ATP Finals giữa Carlos Alcaraz và Alexander Zverev, cú sốc ở UFC Qatar, sức nóng F1 Las Vegas và nhiều tin thể thao đáng chú ý khác ngay sau đây.",
        },
    ],
    "stat_badges": {
        "1": {"label": "BẢN TIN NGÀY", "value": "22.11.2026", "sub": "Toàn cảnh Việt Nam & Thế giới"},
        "2": {"label": "ĐẠI HỘI TOÀN QUỐC", "value": "KHAI MẠC", "sub": "36 đoàn tranh tài 48 môn"},
        "3": {"label": "NGOẠI HẠNG ANH", "value": "CHELSEA 1-4", "sub": "Man City 1-1 • Arsenal 2-2"},
    },
    "slots": [
        # Câu 1 (4 ảnh)
        _slot("sentence", 1, [_url(TN_DH_1)], "THANH NIÊN", "Đêm khai mạc Đại hội Thể thao toàn quốc 2026 rực rỡ bên sông Sài Gòn"),
        _slot("sentence", 1, [_url(DT_MC_1)], "DÂN TRÍ / GETTY", "Erling Haaland phản ứng gay gắt khi bàn thắng vào lưới Fulham bị VAR từ chối"),
        _slot("sentence", 1, [_url(VNE_CHE_1)], "VNEXPRESS / REUTERS", "HLV Xabi Alonso thất thần trong trận thua thảm 1-4 của Chelsea trước Leeds"),
        _slot("sentence", 1, [_url(TN_MESSI_1)], "THANH NIÊN / REUTERS", "Lionel Messi bất lực khi Inter Miami thua đậm trận mở màn play-off MLS"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(TT_DH_1)], "TUỔI TRẺ", "Ngọn đuốc Đại hội Thể thao toàn quốc lần thứ X bừng sáng tối 21 tháng 11"),
        _slot("sentence", 2, [_url(TN_DH_3)], "THANH NIÊN", "Hơn 1500 nghệ sĩ và vận động viên góp mặt trong chương trình Khát vọng Vinh quang"),
        _slot("sentence", 2, [_url(TN_ND_1)], "THANH NIÊN", "Thép Xanh Nam Định đánh bại Hải Phòng 2-1 để củng cố ngôi đầu V-League"),
        _slot("sentence", 2, [_url(TN_HN_1)], "THANH NIÊN", "Hai Long tỏa sáng giúp Hà Nội FC thắng ngược TP Đồng Nai 3-1"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url(VNE_MC_1)], "VNEXPRESS / AP", "Trọng tài cho rằng thủ môn Bernd Leno đã kiểm soát bóng trước khi Haaland đá bồi"),
        _slot("sentence", 3, [_url(DT_CHE_1)], "DÂN TRÍ / REUTERS", "Leeds United thắng đậm ngay tại Stamford Bridge lần đầu tiên kể từ năm 1999"),
        _slot("sentence", 3, [_url(VNE_ARS_1)], "VNEXPRESS / AP", "Arsenal đứt mạch 16 trận thắng khi mở tỷ số sau trận hòa 2-2 trước Newcastle"),
        _slot("sentence", 3, [_url(DT_RMA_1)], "DÂN TRÍ / REUTERS", "Kylian Mbappé sút hỏng phạt đền nhưng Real Madrid vẫn ngược dòng thắng Celta Vigo"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_url(TN_MESSI_2)], "THANH NIÊN / AP", "Inter Miami sớm rơi vào thế thiếu người và thua Columbus Crew 0-3"),
        _slot("sentence", 4, [_url(VNE_ATP_1)], "VNEXPRESS / AP", "Carlos Alcaraz gặp Alexander Zverev ở chung kết ATP Finals 2026 tại Turin"),
        _slot("sentence", 4, [_ddgs("Navajo Stirling UFC Qatar knockout Jiri Prochazka")], "UFC / MMA", "Navajo Stirling tạo địa chấn hạ knock-out cựu vương Jiri Prochazka tại UFC Qatar"),
        _slot("sentence", 4, [_ddgs("Max Verstappen George Russell Las Vegas F1 qualifying 2026")], "FORMULA 1", "Max Verstappen và George Russell chia nhau hàng xuất phát đầu tiên tại Las Vegas"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — ĐẠI HỘI THỂ THAO TOÀN QUỐC 2026)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Đại hội Thể thao toàn quốc 2026 chính thức khai mạc rực rỡ bên sông Sài Gòn",
        "summary": (
            "Tối ngày 21 tháng 11 tại Công viên Bờ sông Sài Gòn, lễ khai mạc Đại hội Thể thao toàn quốc lần thứ X năm 2026 đã diễn ra trang trọng sau 20 năm ngày hội lớn trở lại Thành phố Hồ Chí Minh. "
            "Chương trình nghệ thuật chủ đề Khát vọng Vinh quang quy tụ hơn 1500 nghệ sĩ, vận động viên cùng 37 đoàn diễu hành đại diện cho 36 đoàn thể thao cả nước và lực lượng trọng tài. "
            "Phát biểu chỉ đạo, Phó Thủ tướng Phạm Thị Thanh Trà đề nghị ngành thể thao tiếp tục chăm lo thể thao học đường và đầu tư mũi nhọn cho những tài năng đủ sức vươn tầm châu lục và thế giới. "
            "Trước giờ khai mạc, đoàn chủ nhà Thành phố Hồ Chí Minh tạm dẫn đầu bảng tổng sắp với 40 huy chương vàng, xếp trên Hà Nội có 32 huy chương vàng và Công an Nhân dân với 23 huy chương vàng."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "QUY MÔ ĐẠI HỘI", "value": "36 ĐOÀN", "sub": "Hơn 1500 nghệ sĩ và VĐV"},
            "4": {"label": "BẢNG TỔNG SẮP", "value": "TP.HCM 40 HCV", "sub": "Hà Nội 32 HCV • CAND 23 HCV"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_DH_1)], "THANH NIÊN", "Toàn cảnh lễ khai mạc Đại hội Thể thao toàn quốc 2026 bên sông Sài Gòn"),
            _slot("title", 0, [_url(TT_DH_1)], "TUỔI TRẺ", "Ngọn đuốc truyền thống được thắp sáng mở màn ngày hội thể thao lớn nhất cả nước"),
            _slot("title", 0, [_url(DT_DH_1)], "DÂN TRÍ", "Màn trình diễn ánh sáng và nghệ thuật trên mặt nước sông Sài Gòn"),
            _slot("sentence", 1, [_url(VNE_DH_1)], "VNEXPRESS", "Sau 20 năm, Thành phố Hồ Chí Minh đăng cai lễ khai mạc bên bờ sông Sài Gòn"),
            _slot("sentence", 1, [_url(TN_DH_2)], "THANH NIÊN", "Các đoàn thể thao diễu hành qua lễ đài trong không khí rực rỡ sắc màu"),
            _slot("sentence", 2, [_url(TN_DH_3)], "THANH NIÊN", "Chương trình nghệ thuật Khát vọng Vinh quang với hơn 1500 diễn viên và VĐV"),
            _slot("sentence", 2, [_url(TN_DH_4)], "THANH NIÊN", "Những tiết mục sân khấu kết hợp giữa truyền thống và công nghệ trình diễn hiện đại"),
            _slot("sentence", 3, [_url(TT_DH_PTT)], "TUỔI TRẺ", "Phó Thủ tướng Phạm Thị Thanh Trà phát biểu chỉ đạo tại lễ khai mạc"),
            _slot("sentence", 3, [_url(TN_DH_5)], "THANH NIÊN", "Lãnh đạo Trung ương và Thành phố chứng kiến nghi thức thắp đài lửa"),
            _slot("sentence", 4, [_url(DT_DH_2)], "DÂN TRÍ", "Đoàn Thành phố Hồ Chí Minh tạm dẫn đầu bảng tổng sắp với 40 huy chương vàng"),
            _slot("sentence", 4, [_local(DAILY_21 / "Tin_10_1.jpg")], "THANH NIÊN", "Cuộc đua huy chương ở 48 môn thi đấu tiếp tục diễn ra sôi động"),
        ],
    },

    # 02 (Nữ — BƠI LỘI ĐẠI HỘI 2026)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Kình ngư đội tuyển Mỹ Watson Nguyễn so tài hoàng tử ếch Phạm Thanh Bảo",
        "summary": (
            "Môn bơi Đại hội Thể thao toàn quốc 2026 khởi tranh từ ngày 22 đến ngày 27 tháng 11 tại hồ bơi Phú Thọ hứa hẹn cuộc đối đầu tâm điểm giữa tài năng Việt kiều Watson Nguyễn và Phạm Thanh Bảo. "
            "Sinh năm 2005 tại Texas và đang khoác áo đoàn An Giang, Watson Nguyễn vừa giành huy chương vàng 50 mét ếch tại Giải vô địch quốc gia Mỹ với thông số 26,65 giây cùng suất vào đội tuyển bơi quốc gia Mỹ. "
            "Đáng chú ý, thành tích tốt nhất của Watson ở cả hai cự ly 50 mét và 100 mét ếch đều đang nhanh hơn kỷ lục quốc gia của Phạm Thanh Bảo khoảng hơn một giây. "
            "Tuy nhiên, hoàng tử ếch Việt Nam vẫn nắm ưu thế kinh nghiệm trận mạc cùng sở trường ở cự ly 200 mét ếch đạt mốc 2 phút 11,45 giây sau sáu huy chương vàng qua ba kỳ SEA Games."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "WATSON NGUYỄN", "value": "26,65 GIÂY", "sub": "HCV 50m ếch quốc gia Mỹ"},
            "4": {"label": "PHẠM THANH BẢO", "value": "6 HCV SEA GAMES", "sub": "Sở trường 200m ếch 2:11.45"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_BOI_1)], "TUỔI TRẺ", "Cuộc so tài đáng chờ đợi giữa Watson Nguyễn và Phạm Thanh Bảo tại hồ bơi Phú Thọ"),
            _slot("title", 0, [_url(TT_BOI_2)], "TUỔI TRẺ", "Kình ngư Việt kiều Mỹ Watson Nguyễn thi đấu cho đoàn An Giang tại Đại hội 2026"),
            _slot("title", 0, [_url(TT_BOI_3)], "TUỔI TRẺ", "Hoàng tử ếch Phạm Thanh Bảo sẵn sàng bảo vệ vị thế số một bơi ếch Việt Nam"),
            _slot("sentence", 1, [_url(TT_BOI_1)], "TUỔI TRẺ", "Môn bơi Đại hội Thể thao toàn quốc diễn ra từ ngày 22 đến 27 tháng 11 tại TP.HCM"),
            _slot("sentence", 1, [_ddgs("swimming pool competition lane starting blocks")], "BƠI LỘI", "Hồ bơi câu lạc bộ Phú Thọ là nơi diễn ra những màn tranh tài đỉnh cao"),
            _slot("sentence", 2, [_url(TT_BOI_2)], "TUỔI TRẺ", "Watson Nguyễn vừa đánh bại ngôi sao Michael Andrew tại giải vô địch quốc gia Mỹ"),
            _slot("sentence", 2, [_ddgs("breaststroke swimmer racing underwater pool")], "USA SWIMMING", "Kình ngư sinh năm 2005 đạt thông số 59,79 giây ở nội dung 100 mét ếch"),
            _slot("sentence", 3, [_url(TT_BOI_3)], "TUỔI TRẺ", "Thông số 50 mét và 100 mét ếch của Watson đang vượt kỷ lục quốc gia Việt Nam"),
            _slot("sentence", 3, [_ddgs("competitive swimmer touch wall finish pool")], "BƠI LỘI", "Khoảng cách hơn một giây ở cự ly ngắn là thử thách lớn cho Thanh Bảo"),
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_16_1.jpg")], "TUỔI TRẺ", "Phạm Thanh Bảo giữ phong độ ổn định sau tấm huy chương vàng SEA Games và thành tích ASIAD"),
            _slot("sentence", 4, [_url(TT_BOI_1)], "TUỔI TRẺ", "Cự ly 200 mét ếch vẫn là điểm tựa để tuyển thủ sinh năm 2001 đáp trả đối thủ"),
        ],
    },

    # 03 (Nam — ESPORTS ĐẠI HỘI TOÀN QUỐC 2026)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Khoảnh khắc lịch sử khi Esports lần đầu tranh huy chương ở Đại hội Toàn quốc",
        "summary": (
            "Từ ngày 21 đến ngày 29 tháng 11 tại Hội trường Trường Đại học Thể dục Thể thao Thành phố Hồ Chí Minh, thể thao điện tử lần đầu tiên trong lịch sử chính thức trở thành môn tranh huy chương tại Đại hội Thể thao toàn quốc. "
            "Sau hơn một năm vượt qua các rào cản về bản quyền trò chơi và huy động lực lượng địa phương, ban tổ chức đã đưa vào thi đấu ba bộ môn gồm Liên Quân Mobile, Free Fire Mobile và Audition PC. "
            "Riêng nội dung Liên Quân Mobile quy tụ năm đội tuyển đến từ Hà Nội, Quảng Ninh, Đà Nẵng, Cần Thơ và chủ nhà Thành phố Hồ Chí Minh thi đấu vòng tròn một lượt tính điểm. "
            "Chủ tịch Liên đoàn Thể thao điện tử Thành phố Hồ Chí Minh Mai Bá Hùng nhấn mạnh cột mốc này khẳng định Esports là môn thể thao trí tuệ ngang hàng với các bộ môn truyền thống."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / VIRESA",
        "stat_badges": {
            "1": {"label": "CỘT MỐC LỊCH SỬ", "value": "LẦN ĐẦU TIÊN", "sub": "Esports tranh huy chương quốc gia"},
            "2": {"label": "3 BỘ MÔN", "value": "LIÊN QUÂN • FF", "sub": "Cùng nội dung Audition PC"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_ESP_1)], "TUỔI TRẺ", "Esports lần đầu tiên góp mặt tranh huy chương tại Đại hội Thể thao toàn quốc 2026"),
            _slot("title", 0, [_url(TT_ESP_2)], "TUỔI TRẺ", "Các vận động viên thể thao điện tử bước vào tranh tài từ ngày 21 tháng 11"),
            _slot("title", 0, [_ddgs("esports arena tournament stage players mobile gaming")], "ESPORTS", "Không khí thi đấu chuyên nghiệp tại Trường Đại học Thể dục Thể thao TP.HCM"),
            _slot("sentence", 1, [_url(TT_ESP_1)], "TUỔI TRẺ", "Sự kiện diễn ra từ ngày 21 đến 29 tháng 11 tại Thành phố Hồ Chí Minh"),
            _slot("sentence", 1, [_url(TT_ESP_2)], "TUỔI TRẺ", "Thể thao điện tử chính thức gia nhập hệ thống thi đấu quốc gia"),
            _slot("sentence", 2, [_ddgs("Arena of Valor mobile esports tournament players")], "VIRESA", "Liên Quân Mobile và Free Fire đại diện cho nhóm game MOBA và sinh tồn"),
            _slot("sentence", 2, [_local(DAILY_21 / "Tin_11_1.jpg")], "ESPORTS", "Các tuyển thủ chuẩn bị kỹ lưỡng cho cuộc đua huy chương đầu tiên"),
            _slot("sentence", 3, [_url(TT_ESP_1)], "TUỔI TRẺ", "Năm đội mạnh gồm Hà Nội, Quảng Ninh, Đà Nẵng, Cần Thơ và TP.HCM tranh tài vòng tròn"),
            _slot("sentence", 3, [_ddgs("esports team players headsets competing stage")], "VIRESA", "Ba đội dẫn đầu sẽ nhận huy chương vàng, bạc và đồng chung cuộc"),
            _slot("sentence", 4, [_url(TT_ESP_2)], "TUỔI TRẺ", "Ông Mai Bá Hùng khẳng định vị thế thể thao trí tuệ của Esports Việt Nam"),
            _slot("sentence", 4, [_ddgs("gaming tournament trophy stage lights crowd")], "ESPORTS", "Cột mốc mở ra hướng đầu tư bài bản hơn cho vận động viên trẻ"),
        ],
    },

    # 04 (Nữ — V-LEAGUE VÒNG 8 NGÀY 21/11)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "V-LEAGUE 2026-2027",
        "title": "Nam Định thắng Hải Phòng giữ ngôi đầu, Hà Nội ngược dòng hạ Đồng Nai",
        "summary": (
            "Ở vòng 8 V-League tối ngày 21 tháng 11 trên sân Thiên Trường, Thép Xanh Nam Định đánh bại Hải Phòng 2-1 để củng cố vững chắc ngôi đầu bảng với 19 điểm, nới rộng cách biệt lên năm điểm so với đội nhì bảng Sông Lam Nghệ An. "
            "Bước ngoặt xảy ra ở phút 20 khi hậu vệ Nguyễn Hữu Thái Bảo của Hải Phòng nhận thẻ đỏ trực tiếp sau khi trọng tài kiểm tra VAR, tạo tiền đề để Caio Cesar đá phạt đền mở tỷ số phút 40 và Trần Mạnh Quỳnh nhân đôi cách biệt phút 57 trước khi Makaric gỡ lại một bàn phút 78. "
            "Cùng tối ngày 21 tháng 11, Hà Nội FC dù bị dẫn sớm ngay phút thứ tư vì pha phản lưới nhà của Anh Tiệp vẫn ngược dòng đánh bại chủ nhà Đồng Nai với tỷ số 3-1 nhờ các bàn thắng của Yuval Sade, Nguyễn Hai Long và Lê Xuân Tú. "
            "Chiến thắng giúp huấn luyện viên Harry Kewell giải tỏa áp lực khi đưa Hà Nội FC lên 12 điểm, trong khi Đồng Nai dù vắng Công Phượng tiếp tục chìm sâu dưới đáy bảng với chỉ bốn điểm."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / TUỔI TRẺ / DÂN TRÍ",
        "credit": "THANH NIÊN / DÂN TRÍ",
        "stat_badges": {
            "1": {"label": "NAM ĐỊNH 2-1 HẢI PHÒNG", "value": "19 ĐIỂM", "sub": "Hơn nhì bảng SLNA 5 điểm"},
            "3": {"label": "ĐỒNG NAI 1-3 HÀ NỘI", "value": "12 ĐIỂM", "sub": "Hai Long ghi bàn quyết định"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_ND_1)], "THANH NIÊN", "Các cầu thủ Nam Định ăn mừng chiến thắng trước Hải Phòng tại sân Thiên Trường"),
            _slot("title", 0, [_url(TN_HN_1)], "THANH NIÊN", "Nguyễn Hai Long tỏa sáng rực rỡ giúp Hà Nội FC thắng ngược 3-1 trên sân Bình Phước"),
            _slot("title", 0, [_url(DT_ND_1)], "DÂN TRÍ", "Vòng 8 V-League chứng kiến sức mạnh của nhà đương kim vô địch Nam Định"),
            _slot("sentence", 1, [_url(TN_ND_1)], "THANH NIÊN", "Nam Định giành trọn ba điểm để đạt 19 điểm sau tám vòng đấu"),
            _slot("sentence", 1, [_url(DT_ND_2)], "DÂN TRÍ", "Đội bóng thành Nam tận dụng tốt việc Sông Lam Nghệ An bị cầm hòa không bàn thắng"),
            _slot("sentence", 2, [_url(TN_ND_2)], "THANH NIÊN", "Thẻ đỏ của Thái Bảo khiến Hải Phòng rơi vào thế chống đỡ vất vả"),
            _slot("sentence", 2, [_url(DT_ND_1)], "DÂN TRÍ", "Caio Cesar và Mạnh Quỳnh lập công giúp đội chủ nhà dẫn trước hai bàn"),
            _slot("sentence", 3, [_url(TN_HN_1)], "THANH NIÊN", "Hà Nội FC bị thủng lưới phút thứ tư nhưng kịp bừng tỉnh nhờ Yuval Sade và Hai Long"),
            _slot("sentence", 3, [_url(TN_HN_2)], "THANH NIÊN", "Lê Xuân Tú ấn định tỷ số 3-1 cho đội khách ở phút bù giờ 90+5"),
            _slot("sentence", 4, [_url(TN_HN_3)], "THANH NIÊN", "HLV Harry Kewell giải tỏa sức ép còn Đồng Nai lún sâu ở cuối bảng xếp hạng"),
            _slot("sentence", 4, [_local(DAILY_20 / "Tin_09_1.jpg")], "TUỔI TRẺ", "Công Phượng vắng mặt trên sân chỉ có thể cổ vũ đồng đội từ khán đài"),
        ],
    },

    # 05 (Nam — V-LEAGUE HÔM NAY 22/11)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "V-LEAGUE 2026-2027",
        "title": "Tân HLV Lee Young-jin ra mắt CLB Đà Nẵng tiếp đón Ninh Bình chiều nay",
        "summary": (
            "Tâm điểm loạt trận V-League chiều tối ngày 22 tháng 11 dồn về sân Chi Lăng khi câu lạc bộ Đà Nẵng chính thức trình làng tân huấn luyện viên trưởng Lee Young-jin trong cuộc tiếp đón Ninh Bình lúc 18 giờ. "
            "Cựu trợ lý lâu năm của huấn luyện viên Park Hang-seo được kỳ vọng sẽ thổi luồng sinh khí kỷ luật vào đội bóng sông Hàn đang xếp thứ 10 với chín điểm sau thất bại trước Đồng Nai. "
            "Tuy nhiên, thử thách ngay trận ra mắt của ông Lee Young-jin là rất lớn khi Ninh Bình sở hữu 13 điểm cùng ngôi sao Nguyễn Hoàng Đức đang khao khát trở lại ngôi nhì bảng. "
            "Cùng giờ thi đấu, Hồng Lĩnh Hà Tĩnh tiếp đón Công an Thành phố Hồ Chí Minh, đội bóng vừa tạo cú hích tinh thần lớn bằng chiến thắng trước Buriram United ở giải vô địch các câu lạc bộ Đông Nam Á."
        ),
        "source": "Thanh Niên",
        "news_source": "THANH NIÊN",
        "credit": "THANH NIÊN",
        "stat_badges": {
            "1": {"label": "18H00 HÔM NAY", "value": "CHI LĂNG", "sub": "Đà Nẵng (9đ) vs Ninh Bình (13đ)"},
            "4": {"label": "CÙNG GIỜ", "value": "HÀ TĨNH", "sub": "Chủ nhà tiếp CA TP.HCM"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_DN_NB_1)], "THANH NIÊN", "CLB Đà Nẵng bước vào trận đấu mới với sự dẫn dắt của HLV Lee Young-jin"),
            _slot("title", 0, [_url(TN_DN_NB_2)], "THANH NIÊN", "Nguyễn Hoàng Đức là niềm hy vọng lớn nhất của CLB Ninh Bình trên sân Chi Lăng"),
            _slot("title", 0, [_url(TN_VL_SUN)], "THANH NIÊN", "Các trận đấu vòng 8 V-League chiều 22 tháng 11 hứa hẹn nhiều kịch tính"),
            _slot("sentence", 1, [_url(TN_DN_NB_1)], "THANH NIÊN", "Trận đấu giữa Đà Nẵng và Ninh Bình diễn ra lúc 18 giờ ngày 22 tháng 11"),
            _slot("sentence", 1, [_ddgs("Lee Young-jin coach Vietnam football")], "THANH NIÊN", "Chiến lược gia Hàn Quốc từng nhiều năm gắn bó với bóng đá Việt Nam"),
            _slot("sentence", 2, [_url(TN_VL_SUN)], "THANH NIÊN", "Đà Nẵng cần nhanh chóng tìm lại sự ổn định sau vòng đấu trắng tay"),
            _slot("sentence", 2, [_ddgs("SHB Da Nang football stadium V-League")], "VPF", "Hiệu ứng thay tướng được kỳ vọng giúp đội chủ nhà chơi khởi sắc"),
            _slot("sentence", 3, [_url(TN_DN_NB_2)], "THANH NIÊN", "Hoàng Đức cùng đồng đội hướng tới mục tiêu giành trọn ba điểm để đua nhóm đầu"),
            _slot("sentence", 3, [_local(DAILY_20 / "Tin_09_4.jpg")], "VPF", "Ninh Bình nhỉnh hơn về lực lượng và thành tích đối đầu gần đây"),
            _slot("sentence", 4, [_local(DAILY_21 / "Tin_20_6.jpg")], "THANH NIÊN", "CA TP.HCM tự tin làm khách Hà Tĩnh sau khi đánh bại Buriram United"),
            _slot("sentence", 4, [_ddgs("V-League football match action players Vietnam")], "VPF", "Cả Hà Tĩnh và CA TP.HCM đều cần điểm để bám đuổi tốp đầu"),
        ],
    },

    # 06 (Nữ — U17 VIỆT NAM VS NEW ZEALAND)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Việt Nam soi điểm yếu New Zealand trước trận đánh then chốt tối 23 tháng 11",
        "summary": (
            "Trước lượt trận thứ hai bảng G U17 World Cup lúc 22 giờ 30 ngày 23 tháng 11, đội tuyển U17 Việt Nam đang tạm xếp trên U17 New Zealand nhờ hơn hiệu số bàn thắng bại sau ngày ra quân. "
            "Thất bại 0-3 trước U17 Mali đã phơi bày lỗ hổng lớn nơi hàng phòng ngự đại diện châu Đại Dương, đặc biệt ở khả năng mất tập trung đầu hiệp hai khiến họ thủng lưới hai bàn chỉ trong bốn phút. "
            "Trong khi đó, màn trình diễn sòng phẳng cùng hai siêu phẩm của Lê Sỹ Bách và Chu Ngọc Nguyễn Lực trước U17 Bỉ tiếp tục nhận mưa lời khen từ báo chí Bỉ lẫn truyền thông Đông Nam Á. "
            "Bên cạnh yếu tố chuyên môn, việc ban huấn luyện chủ động dùng cả ba lần quyền khiếu nại công nghệ hỗ trợ video FVS trước Bỉ cũng giúp toàn đội tích lũy thêm kinh nghiệm quý giá cho trận cầu quyết định vé đi tiếp."
        ),
        "source": "Thanh Niên / VnExpress / Dân Trí",
        "news_source": "THANH NIÊN / VNEXPRESS / DÂN TRÍ",
        "credit": "THANH NIÊN / VFF",
        "stat_badges": {
            "1": {"label": "LƯỢT 2 BẢNG G", "value": "22H30 23/11", "sub": "U17 Việt Nam vs U17 New Zealand"},
            "2": {"label": "ĐỐI THỦ TRỰC TIẾP", "value": "NZ THUA 0-3", "sub": "Thủng lưới 2 bàn trong 4 phút"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_U17_NL)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực là tâm điểm kỳ vọng của U17 Việt Nam trước trận gặp New Zealand"),
            _slot("title", 0, [_url(TN_U17_NZ1)], "THANH NIÊN", "U17 New Zealand bộc lộ nhiều khoảng trống phòng ngự trong trận thua Mali 0-3"),
            _slot("title", 0, [_url(VNE_U17_BE1)], "VNEXPRESS", "Báo chí Bỉ thừa nhận suýt chút nữa bị U17 Việt Nam gây sốc ở ngày mở màn"),
            _slot("sentence", 1, [_url(TN_U17_NL)], "THANH NIÊN / VFF", "U17 Việt Nam hiện xếp thứ ba bảng G, trên New Zealand nhờ hiệu số bàn thắng bại"),
            _slot("sentence", 1, [_url(TN_U17_NZ2)], "THANH NIÊN", "Trận đấu tối 23 tháng 11 có ý nghĩa then chốt với cơ hội vào vòng 32 đội"),
            _slot("sentence", 2, [_url(TN_U17_NZ1)], "THANH NIÊN", "U17 New Zealand gặp khó trước tốc độ và khả năng tranh chấp của đối thủ"),
            _slot("sentence", 2, [_local(DAILY_21 / "Tin_04_5.jpg")], "TUỔI TRẺ", "Cả ba bàn thua trước Mali đều đến khi hàng thủ New Zealand rối loạn"),
            _slot("sentence", 3, [_url(VNE_U17_BE1)], "VNEXPRESS", "Truyền thông Bỉ ca ngợi cú đánh gót và pha sút phạt góc thành bàn là đẳng cấp thế giới"),
            _slot("sentence", 3, [_url(VNE_U17_BE2)], "VNEXPRESS", "Báo chí Thái Lan và Indonesia đồng loạt ấn tượng với lối chơi pressing của U17 Việt Nam"),
            _slot("sentence", 4, [_url(TN_U17_FVS)], "THANH NIÊN", "HLV Cristiano Roland tận dụng tốt công nghệ FVS cho phép khiếu nại trực tiếp"),
            _slot("sentence", 4, [_local(DAILY_21 / "Tin_03_2.jpg")], "DÂN TRÍ", "Toàn đội rút kinh nghiệm giữ sự tập trung tối đa trước cuộc đấu quyết định"),
        ],
    },

    # 07 (Nam — CLB CAHN BỊ AFC PHẠT)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "BÓNG ĐÁ VIỆT NAM",
        "title": "CLB Công an Hà Nội bị AFC phạt 2000 USD vì sự cố cổ động viên tại Nhật Bản",
        "summary": (
            "Ủy ban Kỷ luật và Đạo đức Liên đoàn Bóng đá châu Á AFC vừa công bố quyết định phạt câu lạc bộ Công an Hà Nội 2000 USD, tương đương hơn 51 triệu đồng, theo điều 65.1 Bộ quy tắc kỷ luật. "
            "Sự việc bắt nguồn từ trận đấu trên sân của Gamba Osaka tại Nhật Bản ngày 15 tháng 9 ở AFC Champions League Elite, khi một số cổ động viên trưng biểu tượng cờ bị cấm trên khán đài. "
            "Theo quy định của AFC, đội khách mặc nhiên phải chịu trách nhiệm đối với hành vi của nhóm khán giả ngồi tại khu vực dành cho cổ động viên đội mình bất kể có trực tiếp tổ chức hay không. "
            "Tuy nhiên, án phạt này đang gây nhiều tranh luận trong người hâm mộ vì công tác kiểm tra an ninh tại cổng sân vốn thuộc trách nhiệm của đơn vị chủ nhà Nhật Bản theo điều 64.3."
        ),
        "source": "Thanh Niên",
        "news_source": "THANH NIÊN",
        "credit": "THANH NIÊN / CAHN FC",
        "stat_badges": {
            "1": {"label": "ÁN PHẠT AFC", "value": "2000 USD", "sub": "Vi phạm điều 65.1 tại Nhật Bản"},
            "4": {"label": "TRANH LUẬN", "value": "ĐIỀU 64.3", "sub": "Trách nhiệm kiểm soát an ninh sân"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_CAHN_1)], "THANH NIÊN", "CLB Công an Hà Nội nhận án phạt tài chính từ Ủy ban Kỷ luật AFC"),
            _slot("title", 0, [_url(TN_CAHN_2)], "THANH NIÊN", "Sự cố xảy ra trên khán đài trong chuyến làm khách tại Nhật Bản"),
            _slot("title", 0, [_local(DAILY_19 / "Tin_13_1.jpg")], "AFC", "AFC siết chặt quy định kiểm soát biểu tượng bị cấm tại cúp châu Á"),
            _slot("sentence", 1, [_url(TN_CAHN_1)], "THANH NIÊN", "Mức phạt 2000 USD được công bố sau phiên họp kỷ luật ngày 19 tháng 11"),
            _slot("sentence", 1, [_ddgs("Asian Football Confederation AFC headquarters Kuala Lumpur")], "AFC", "Quyết định xử phạt căn cứ theo điều 65.1 Bộ quy tắc Kỷ luật và Đạo đức"),
            _slot("sentence", 2, [_url(TN_CAHN_2)], "THANH NIÊN", "Vụ việc diễn ra trong trận CAHN gặp Gamba Osaka ở cúp C1 châu Á"),
            _slot("sentence", 2, [_ddgs("Gamba Osaka Panasonic Stadium Suita Japan")], "AFC", "Cờ không hợp lệ xuất hiện ở khu vực khán đài đội khách"),
            _slot("sentence", 3, [_url(TN_CAHN_1)], "THANH NIÊN", "Quy định của AFC buộc đội bóng chịu trách nhiệm gián tiếp về cổ động viên"),
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_13_2.jpg")], "CAHN FC", "Đội bóng ngành công an gặp bất lợi dù không nắm quyền tổ chức trận đấu"),
            _slot("sentence", 4, [_url(TN_CAHN_2)], "THANH NIÊN", "Nhiều ý kiến đặt câu hỏi về khâu kiểm soát an ninh ở cổng vào sân"),
            _slot("sentence", 4, [_ddgs("football stadium security check fans entrance")], "THANH NIÊN", "Điều 64.3 quy định rõ nghĩa vụ ngăn chặn vật phẩm cấm của ban tổ chức sân"),
        ],
    },

    # 08 (Nữ — LÊ QUANG LIÊM TOP 15 THẾ GIỚI)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "CỜ VUA QUỐC TẾ",
        "title": "Lê Quang Liêm đánh bại Nepomniachtchi, trở lại Top 15 thế giới",
        "summary": (
            "Ở ngày thi đấu cuối cùng tại Giải cờ vua toàn năng thế giới 2026 diễn ra tại Budapest, đại kiện tướng Lê Quang Liêm đã xuất sắc đánh bại Ian Nepomniachtchi để đòi lại vị trí trong Top 15 trên bảng xếp hạng Elo tiêu chuẩn thế giới. "
            "Cầm quân trắng ở ván tiêu chuẩn nhanh có giá trị tám điểm, kỳ thủ số một Việt Nam tận dụng triệt để sai lầm của đối thủ người Nga ở nước thứ chín, sớm hơn chất và buộc Nepomniachtchi xin thua sau 29 nước đi. "
            "Chiến thắng giúp Quang Liêm lật ngược thế trận khép lại ngày thi đấu với tỷ số 14-6, dù sau đó anh để thua đáng tiếc ở ván Armageddon quyết định và nhận vị trí thứ tám chung cuộc kèm 32000 USD tiền thưởng. "
            "Việc giữ vững vị trí trong nhóm 15 kỳ thủ mạnh nhất hành tinh mở ra cơ hội lớn để Lê Quang Liêm cạnh tranh suất tham dự hệ thống giải toàn năng thế giới vào năm sau."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / TOTAL CHESS",
        "stat_badges": {
            "1": {"label": "BẢNG ELO THẾ GIỚI", "value": "TOP 15", "sub": "Thắng Nepomniachtchi sau 29 nước"},
            "3": {"label": "XẾP HẠNG CHUNG CUỘC", "value": "32000 USD", "sub": "Hạng 8 tại Budapest, Hungary"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_QL_1)], "VNEXPRESS", "Lê Quang Liêm giành chiến thắng ấn tượng trước Ian Nepomniachtchi"),
            _slot("title", 0, [_url(VNE_QL_2)], "VNEXPRESS", "Kỳ thủ số một Việt Nam chính thức trở lại nhóm 15 người mạnh nhất thế giới"),
            _slot("title", 0, [_local(DAILY_21 / "Tin_07_1.jpg")], "TOTAL CHESS", "Giải cờ vua toàn năng thế giới 2026 tại Budapest quy tụ 24 siêu đại kiện tướng"),
            _slot("sentence", 1, [_url(VNE_QL_1)], "VNEXPRESS", "Quang Liêm vượt qua chính Nepomniachtchi để trở lại Top 15 bảng Elo tiêu chuẩn"),
            _slot("sentence", 1, [_ddgs("Le Quang Liem chess grandmaster tournament")], "TOTAL CHESS", "Đây là cột mốc quan trọng sau giai đoạn nhiều biến động ở vòng loại trực tiếp"),
            _slot("sentence", 2, [_url(VNE_QL_2)], "VNEXPRESS", "Kỳ thủ Việt Nam khai thác chính xác sai lầm nước c5 của đối thủ Nga"),
            _slot("sentence", 2, [_ddgs("Ian Nepomniachtchi chess grandmaster")], "TOTAL CHESS", "Sau 29 nước cờ, Nepomniachtchi buộc phải xin thua trước sức ép lớn"),
            _slot("sentence", 3, [_local(DAILY_21 / "Tin_07_2.jpg")], "TOTAL CHESS", "Ở ván Armageddon phân định hạng bảy, Quang Liêm cạn giờ khi cầm quân đen"),
            _slot("sentence", 3, [_url(VNE_QL_1)], "VNEXPRESS", "Kỳ thủ 35 tuổi kết thúc giải ở hạng tám với phần thưởng 32000 USD"),
            _slot("sentence", 4, [_local(DAILY_21 / "Tin_07_4.jpg")], "TOTAL CHESS", "Alireza Firouzja đăng quang ngôi vô địch trước Anish Giri tại Budapest"),
            _slot("sentence", 4, [_url(VNE_QL_2)], "VNEXPRESS", "Duy trì Top 15 thế giới giúp Quang Liêm nuôi hy vọng dự chuỗi giải năm 2027"),
        ],
    },

    # 09 (Nam — ĐÔNG NAM Á TẠI 4 VCK CHÂU Á 2027)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "BÓNG ĐÁ ĐÔNG NAM Á",
        "title": "Duy nhất Indonesia giành đủ bốn suất dự Vòng chung kết châu Á năm 2027",
        "summary": (
            "Theo thống kê chính thức từ Liên đoàn Bóng đá châu Á AFC, năm 2027 có bốn giải đấu lớn cấp đội tuyển gồm Asian Cup nam, U20 nam, U17 nam và U17 nữ châu Á, trong đó Indonesia là quốc gia Đông Nam Á duy nhất góp mặt ở cả bốn sân chơi. "
            "Đại diện xứ vạn đảo hoàn tất bộ tứ giải châu Á sau khi đội U17 nam đứng đầu bảng A vòng loại, nối tiếp thành công của đội tuyển quốc gia, đội U20 nam từng thắng Úc 2-0 và đội U17 nữ toàn thắng bảng B. "
            "Trong khi đó, Việt Nam và Thái Lan cùng giành quyền tham dự ba trên bốn giải đấu châu lục vào năm 2027. "
            "Với bóng đá Việt Nam, sự vắng mặt đáng tiếc nhất thuộc về đội U20 nam khi để thua ở vòng loại hồi tháng 9, còn Thái Lan vừa đánh rơi vé U17 nam châu Á sau thất bại 1-2 trước Iraq tối ngày 20 tháng 11."
        ),
        "source": "Tuổi Trẻ / Dân Trí",
        "news_source": "TUỔI TRẺ / DÂN TRÍ",
        "credit": "TUỔI TRẺ / AFC",
        "stat_badges": {
            "1": {"label": "THỐNG KÊ AFC 2027", "value": "INDONESIA 4/4", "sub": "Việt Nam & Thái Lan cùng 3/4"},
            "4": {"label": "VÉ ĐÃ CÓ CỦA VN", "value": "ĐTQG • U17 NAM/NỮ", "sub": "Thiếu suất U20 nam châu Á"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_INDO_4)], "TUỔI TRẺ", "Indonesia hoàn tất trọn bộ bốn vé dự các Vòng chung kết châu Á 2027"),
            _slot("title", 0, [_url(DT_U17_AFC)], "DÂN TRÍ / ASEAN FOOTBALL", "Việt Nam và Thái Lan cùng có mặt ở ba trên bốn giải đấu châu Á năm 2027"),
            _slot("title", 0, [_local(DAILY_21 / "Tin_05_1.jpg")], "AFC", "Cuộc cạnh tranh đào tạo trẻ giữa các nền bóng đá Đông Nam Á ngày càng gay gắt"),
            _slot("sentence", 1, [_url(TT_INDO_4)], "TUỔI TRẺ", "Indonesia trở thành nền bóng đá duy nhất khu vực dự đủ bốn giải châu Á 2027"),
            _slot("sentence", 1, [_ddgs("Indonesia national football team celebration 2026")], "AFC", "Chủ tịch PSSI Erick Thohir xem đây là thước đo của đào tạo trẻ ổn định"),
            _slot("sentence", 2, [_url(DT_U17_AFC)], "DÂN TRÍ / ASEAN FOOTBALL", "Cả bốn cấp độ tuyển nam nữ của Indonesia đều đứng đầu bảng vòng loại"),
            _slot("sentence", 2, [_ddgs("Indonesia U20 football team match celebration")], "AFC", "Thành tích thắng Úc 2-0 giúp U20 Indonesia đoạt ngôi đầu bảng H"),
            _slot("sentence", 3, [_local(DAILY_21 / "Tin_05_3.jpg")], "THANH NIÊN", "Việt Nam có vé dự Asian Cup, U17 nam nhờ suất World Cup và U17 nữ toàn thắng"),
            _slot("sentence", 3, [_local(DAILY_21 / "Tin_05_2.jpg")], "TUỔI TRẺ", "Thái Lan cũng sở hữu ba suất sau khi U17 nữ đứng đầu bảng F"),
            _slot("sentence", 4, [_local(DAILY_21 / "Tin_05_4.jpg")], "DÂN TRÍ", "U17 Thái Lan thủng lưới phút 84 trước Iraq nên lỡ hẹn giải châu Á"),
            _slot("sentence", 4, [_url(DT_U17_AFC)], "DÂN TRÍ", "Bóng đá Việt Nam đặt mục tiêu cải thiện thành tích ở lứa U20 thời gian tới"),
        ],
    },

    # 10 (Nữ — MAN CITY 1-1 FULHAM & TRANH CÃI VAR HAALAND)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "NGOẠI HẠNG ANH",
        "title": "VAR hủy bàn thắng gây tranh cãi của Haaland, Man City hòa Fulham 1-1",
        "summary": (
            "Tiếp đón Fulham trên sân Etihad tối ngày 21 tháng 11 ở vòng 11 Ngoại hạng Anh, Manchester City sớm bị dội gáo nước lạnh ở phút 16 khi cựu cầu thủ Oscar Bobb kiến tạo để Rodrigo Muniz cứa lòng mở tỷ số. "
            "Phút 25, Erling Haaland lao vào đá bồi tung lưới đội khách nhưng trọng tài Thomas Bramall và tổ VAR kiên quyết từ chối bàn thắng vì nhận định thủ môn Bernd Leno đã kiểm soát bóng giữa hai tay theo Luật 12 của IFAB. "
            "Quyết định này thổi bùng tranh cãi dữ dội khi huấn luyện viên Enzo Maresca phản đối gay gắt ngoài đường biên còn nhiều chuyên gia cho rằng bóng chưa nằm gọn trong tay Leno. "
            "Dù tiền vệ Elliot Anderson tung cú vô lê gỡ hòa 1-1 ở phút 57, Man City vẫn nối dài mạch bốn trận liên tiếp không thắng, đứt chuỗi 20 trận toàn thắng trước Fulham và kém đội đầu bảng Arsenal năm điểm dù đá nhiều hơn một trận."
        ),
        "source": "BBC Sport / VnExpress / Dân Trí / The Guardian",
        "news_source": "BBC SPORT / VNEXPRESS / DÂN TRÍ",
        "credit": "AP / REUTERS",
        "stat_badges": {
            "2": {"label": "TRANH CÃI PHÚT 25", "value": "HỦY BÀN HAALAND", "sub": "VAR viện dẫn Luật 12 IFAB"},
            "4": {"label": "MAN CITY KHỦNG HOẢNG", "value": "4 TRẬN KHÔNG THẮNG", "sub": "Đứt chuỗi 20 trận thắng Fulham"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_MC_1)], "DÂN TRÍ / GETTY", "Erling Haaland bức xúc khi bàn thắng vào lưới Fulham không được công nhận"),
            _slot("title", 0, [_url(VNE_MC_1)], "VNEXPRESS / AP", "Tình huống va chạm giữa Haaland và thủ môn Bernd Leno ở phút 25"),
            _slot("title", 0, [_url(VNE_MC_2)], "VNEXPRESS", "Elliot Anderson ghi bàn đầu tiên cho Man City ở Ngoại hạng Anh nhưng chưa đủ giành ba điểm"),
            _slot("sentence", 1, [_url(DT_MC_2)], "DÂN TRÍ / GETTY", "Rodrigo Muniz trừng phạt hàng thủ lỏng lẻo của Man City ngay phút 16"),
            _slot("sentence", 1, [_url(DT_MC_MAR)], "DÂN TRÍ / GETTY", "HLV Enzo Maresca tiếp tục đối mặt bài toán phòng ngự chuyển trạng thái"),
            _slot("sentence", 2, [_url(VNE_MC_1)], "VNEXPRESS / AP", "VAR xác định bóng nằm giữa hai tay Leno khi chân Haaland chạm tới"),
            _slot("sentence", 2, [_url(DT_MC_1)], "DÂN TRÍ / GETTY", "Ban tổ chức Ngoại hạng Anh phải đăng thông báo giải thích trên mạng xã hội"),
            _slot("sentence", 3, [_url(DT_MC_3)], "DÂN TRÍ / GETTY", "CĐV trên sân Etihad hô vang phản đối quyết định của tổ trọng tài"),
            _slot("sentence", 3, [_url(DT_MC_MAR)], "DÂN TRÍ / GETTY", "Nhiều bình luận viên Anh như Joe Cole cho rằng thổi phạt Haaland là quá nặng"),
            _slot("sentence", 4, [_url(VNE_MC_2)], "VNEXPRESS", "Elliot Anderson vô lê đẹp mắt gỡ hòa 1-1 từ quả phạt góc phút 57"),
            _slot("sentence", 4, [_url(DT_MC_2)], "DÂN TRÍ / GETTY", "Man City mới thắng một trong bốn vòng gần nhất và nguy cơ tụt sâu trong cuộc đua vô địch"),
        ],
    },

    # 11 (Nam — CHELSEA 1-4 LEEDS)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "NGOẠI HẠNG ANH",
        "title": "Chelsea thảm bại 1-4 trước Leeds ngay tại Stamford Bridge, Xabi Alonso lâm nguy",
        "summary": (
            "Chelsea vừa trải qua cơn ác mộng thực sự ngay trên sân nhà Stamford Bridge tối ngày 21 tháng 11 khi để Leeds United lội ngược dòng đè bẹp với tỷ số đậm 4-1 ở vòng 11 Ngoại hạng Anh. "
            "Dù tiền đạo trẻ Emmanuel Emegha mở tỷ số cho đội chủ nhà ở phút 25, sự mong manh của hàng thủ khiến Chelsea nhanh chóng sụp đổ trước cú đúp của Noah Okafor, quả phạt đền gây tranh cãi của Calvert-Lewin sau lỗi chạm tay của Morgan Rogers và bàn ấn định của Brenden Aaronson. "
            "Đây là chiến thắng đầu tiên của Leeds trên sân Chelsea kể từ năm 1999, đồng thời là lần đầu tiên từ năm 1967 đội bóng thành London thua cả Tottenham lẫn Leeds trên sân nhà trong cùng một mùa giải. "
            "Thất bại thứ tư trong năm trận gần nhất đẩy đoàn quân của huấn luyện viên Xabi Alonso tụt xuống vị trí thứ tám và bị đội đầu bảng Arsenal bỏ xa tới 12 điểm."
        ),
        "source": "BBC Sport / The Guardian / VnExpress / Dân Trí",
        "news_source": "BBC SPORT / GUARDIAN / VNEXPRESS",
        "credit": "REUTERS / GETTY",
        "stat_badges": {
            "1": {"label": "STAMFORD BRIDGE", "value": "CHELSEA 1-4 LEEDS", "sub": "Leeds thắng tại đây sau 27 năm"},
            "4": {"label": "XABI ALONSO", "value": "THUA 4/5 TRẬN", "sub": "Chelsea tụt xuống hạng 8"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_CHE_1)], "VNEXPRESS / REUTERS", "HLV Xabi Alonso đối mặt làn sóng la ó dữ dội từ khán đài Stamford Bridge"),
            _slot("title", 0, [_url(DT_CHE_1)], "DÂN TRÍ / REUTERS", "Các cầu thủ Leeds United ăn mừng chiến thắng lịch sử 4-1 trên sân Chelsea"),
            _slot("title", 0, [_url(VNE_CHE_3)], "VNEXPRESS / AP", "Nhiều cổ động viên Chelsea đã bỏ về sớm khi đội nhà nhận bàn thua thứ ba"),
            _slot("sentence", 1, [_url(DT_CHE_1)], "DÂN TRÍ / REUTERS", "Leeds United thắng thuyết phục ngay tại Stamford Bridge ở vòng 11 Ngoại hạng Anh"),
            _slot("sentence", 1, [_url(DT_CHE_2)], "DÂN TRÍ / GETTY", "HLV Daniel Farke lần đầu tiên đánh bại được người đồng nghiệp Xabi Alonso"),
            _slot("sentence", 2, [_url(VNE_CHE_3)], "VNEXPRESS / AP", "Noah Okafor lập cú đúp còn Morgan Rogers mắc lỗi dẫn tới phạt đền"),
            _slot("sentence", 2, [_url(DT_CHE_2)], "DÂN TRÍ / GETTY", "Hàng thủ Chelsea hoàn toàn bất lực trước lối chơi áp sát của đội khách"),
            _slot("sentence", 3, [_url(VNE_CHE_2)], "VNEXPRESS / REUTERS", "Kể từ năm 1967, Chelsea mới lại thua cả Leeds và Tottenham trên sân nhà trong một mùa"),
            _slot("sentence", 3, [_ddgs("Leeds United players celebrating goal Stamford Bridge")], "REUTERS", "Chiến thắng đưa Leeds vươn lên vị trí thứ sáu trên bảng xếp hạng"),
            _slot("sentence", 4, [_url(VNE_CHE_1)], "VNEXPRESS / REUTERS", "Xabi Alonso thừa nhận Chelsea đang ở trạng thái mong manh về tinh thần"),
            _slot("sentence", 4, [_url(VNE_CHE_2)], "VNEXPRESS / REUTERS", "Cơ hội cạnh tranh vé Champions League của Chelsea đang bị đặt dấu hỏi lớn"),
        ],
    },

    # 12 (Nữ — ARSENAL 2-2 NEWCASTLE & CHẤN THƯƠNG RAYA)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "NGOẠI HẠNG ANH",
        "title": "Arsenal đánh rơi chiến thắng trước Newcastle và lo âu chấn thương David Raya",
        "summary": (
            "Hành quân tới sân St James Park, đương kim vô địch Arsenal áp đảo hoàn toàn trong hiệp một với 66 phần trăm thời lượng kiểm soát bóng và mở tỷ số ở phút 33 nhờ cú sút cận thành của Eberechi Eze. "
            "Tuy nhiên, sự chùng xuống đầu hiệp hai khiến Pháo thủ trả giá đắt khi Newcastle tận dụng sai lầm của hàng thủ để ghi liền hai bàn do công Harvey Barnes và Malick Thiaw chỉ trong 13 phút. "
            "Phải nhờ khoảnh khắc tỏa sáng của Noni Madueke với pha đi bóng cắt vào trung lộ sút chân trái ở phút 78, Arsenal mới giữ lại trận hòa 2-2 nhưng đứt chuỗi 16 trận thắng liên tiếp khi ghi bàn mở tỷ số. "
            "Điều khiến huấn luyện viên Mikel Arteta lo lắng hơn cả hai điểm đánh rơi là chấn thương vai của thủ môn số một David Raya ở phút 70, buộc anh phải chụp cộng hưởng từ để xác định thời gian nghỉ thi đấu."
        ),
        "source": "BBC Sport / Sky Sports / VnExpress / Tuổi Trẻ",
        "news_source": "BBC SPORT / SKY SPORTS / VNEXPRESS",
        "credit": "AP / SKY SPORTS",
        "stat_badges": {
            "3": {"label": "NEWCASTLE 2-2 ARSENAL", "value": "ĐỨT MẠCH 16 TRẬN", "sub": "Vẫn dẫn đầu với 28 điểm"},
            "4": {"label": "TỔN THẤT LỚN", "value": "DAVID RAYA", "sub": "Chấn thương vai rời sân phút 70"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_ARS_1)], "VNEXPRESS / AP", "Arsenal có trận đấu đầy vất vả trên sân St James Park của Newcastle"),
            _slot("title", 0, [_url(SKY_ARS_NEW)], "SKY SPORTS", "Malick Thiaw ăn mừng bàn thắng đưa Newcastle vượt lên dẫn 2-1 ở phút 62"),
            _slot("title", 0, [_url(DT_ARS_1)], "DÂN TRÍ / GETTY", "Noni Madueke ghi bàn thắng quan trọng giúp Pháo thủ thoát thua"),
            _slot("sentence", 1, [_url(VNE_ARS_2)], "VNEXPRESS / AP", "Eberechi Eze phá bẫy việt vị mở tỷ số sau đường chuyền của Kai Havertz"),
            _slot("sentence", 1, [_url(VNE_ARS_4)], "VNEXPRESS / AP", "HLV Mikel Arteta tiếc nuối khi Arsenal bỏ lỡ quá nhiều cơ hội hiệp một"),
            _slot("sentence", 2, [_url(SKY_ARS_NEW)], "SKY SPORTS", "Harvey Barnes và Malick Thiaw trừng phạt sự lỏng lẻo của hàng thủ đội khách"),
            _slot("sentence", 2, [_url(DT_ARS_2)], "DÂN TRÍ / GETTY", "Tân HLV Matthias Jaissle giúp Newcastle vùng lên mạnh mẽ đầu hiệp hai"),
            _slot("sentence", 3, [_url(DT_ARS_1)], "DÂN TRÍ / GETTY", "Noni Madueke dứt điểm chân trái hiểm hóc ấn định tỷ số hòa 2-2"),
            _slot("sentence", 3, [_url(VNE_ARS_1)], "VNEXPRESS / AP", "Arsenal vẫn hơn đội nhì bảng Brighton sáu điểm nhưng lỡ cơ hội bứt phá sâu hơn"),
            _slot("sentence", 4, [_url(VNE_ARS_3)], "VNEXPRESS / AP", "Thủ môn David Raya ôm vai rời sân nhường chỗ cho Kepa Arrizabalaga"),
            _slot("sentence", 4, [_url(VNE_ARS_4)], "VNEXPRESS / AP", "Arteta chờ kết quả kiểm tra y tế với nỗi lo mất chốt chặn số một"),
        ],
    },

    # 13 (Nam — TOTTENHAM & HIỆN TƯỢNG BOURNEMOUTH)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "NGOẠI HẠNG ANH",
        "title": "Sao mai 18 tuổi Tottenham gây sốt, Bournemouth nối dài mạch chín trận thắng",
        "summary": (
            "Vòng 11 Ngoại hạng Anh chứng kiến màn ra mắt rực rỡ của tài năng 18 tuổi Luca Williams-Barnett trong chiến thắng 2-0 của Tottenham Hotspur trước Ipswich Town. "
            "Được huấn luyện viên Roberto De Zerbi trao suất đá chính lần đầu tiên, cầu thủ trưởng thành từ học viện Spurs đã ghi bàn mở tỷ số và góp dấu giày vào bàn ấn định của Dominic Solanke, khiến ông thầy người Ý ví anh với Lamine Yamal. "
            "Ở một diễn biến đáng chú ý khác, hiện tượng Bournemouth dưới sự dẫn dắt của tân huấn luyện viên Marco Rose đã đánh bại Nottingham Forest 2-0 để nối dài kỷ lục chín trận thắng liên tiếp trên mọi đấu trường. "
            "Tiền đạo Evanilson tiếp tục phong độ thăng hoa với bàn thắng trong trận đấu thứ sáu liên tiếp tại Ngoại hạng Anh, đẩy Nottingham Forest của Oliver Glasner lùi sát nhóm xuống hạng."
        ),
        "source": "BBC Football / Sky Sports / The Guardian",
        "news_source": "BBC SPORT / SKY SPORTS / GUARDIAN",
        "credit": "SKY SPORTS / REUTERS",
        "stat_badges": {
            "2": {"label": "TOTTENHAM 2-0 IPSWICH", "value": "WILLIAMS-BARNETT", "sub": "18 tuổi được ví như Lamine Yamal"},
            "3": {"label": "BOURNEMOUTH BAY CAO", "value": "9 THẮNG LIÊN TIẾP", "sub": "Evanilson ghi bàn 6 trận liền"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_SPURS_1)], "SKY SPORTS", "Tài năng trẻ 18 tuổi Luca Williams-Barnett bùng nổ trong màu áo Tottenham"),
            _slot("title", 0, [_ddgs("Roberto De Zerbi Tottenham Hotspur manager 2026")], "SKY SPORTS", "HLV Roberto De Zerbi hết lời khen ngợi viên ngọc thô của lò đào tạo Spurs"),
            _slot("title", 0, [_ddgs("AFC Bournemouth Evanilson Premier League celebration")], "BBC SPORT", "Bournemouth lập chuỗi chín trận thắng liên tiếp đầy ấn tượng"),
            _slot("sentence", 1, [_url(SKY_SPURS_1)], "SKY SPORTS", "Williams-Barnett chơi nổi bật trên hàng công Tottenham trước Ipswich Town"),
            _slot("sentence", 1, [_ddgs("Dominic Solanke Tottenham Hotspur celebration goal")], "BBC SPORT", "Spurs giành chiến thắng thuyết phục 2-0 trên sân nhà"),
            _slot("sentence", 2, [_ddgs("Roberto De Zerbi touchline coach Tottenham")], "SKY SPORTS", "HLV Roberto De Zerbi so sánh tài năng của cậu học trò trẻ với Lamine Yamal"),
            _slot("sentence", 2, [_url(SKY_SPURS_1)], "SKY SPORTS", "Cầu thủ 18 tuổi góp công lớn vào cả hai bàn thắng của đội bóng Bắc London"),
            _slot("sentence", 3, [_ddgs("Evanilson Bournemouth striker Premier League")], "BBC SPORT", "Evanilson và Justin Kluivert lập công giúp Bournemouth hạ Nottingham Forest 2-0"),
            _slot("sentence", 3, [_ddgs("Marco Rose football manager touchline")], "REUTERS", "HLV Marco Rose biến Bournemouth thành tập thể đáng gờm nhất giải"),
            _slot("sentence", 4, [_ddgs("Nottingham Forest Oliver Glasner football")], "BBC SPORT", "Thất bại khiến Nottingham Forest của Oliver Glasner chỉ hơn nhóm xuống hạng về hiệu số"),
            _slot("sentence", 4, [_ddgs("Vitality Stadium Bournemouth Premier League")], "REUTERS", "Chuỗi chín trận toàn thắng là cột mốc lịch sử mới của đội bóng miền Nam nước Anh"),
        ],
    },

    # 14 (Nữ — REAL MADRID 2-1 CELTA VIGO)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "LA LIGA 2026-2027",
        "title": "Real Madrid thắng ngược Celta Vigo 2-1 dù Kylian Mbappé sút hỏng phạt đền",
        "summary": (
            "Trên sân Bernabeu rạng sáng ngày 22 tháng 11 ở vòng 13 La Liga, Real Madrid khởi đầu chuệch choạc và để Celta Vigo chọc thủng lưới ngay phút thứ sáu bởi cú đệm bóng của Pablo Duran. "
            "Cơ hội gỡ hòa đến ở phút 39 khi đội chủ nhà được hưởng phạt đền, nhưng Kylian Mbappé lại sút vọt xà ngang, đánh dấu lần đá hỏng thứ ba trong sáu quả phạt đền gần nhất của tiền đạo người Pháp. "
            "Sang hiệp hai, huấn luyện viên Jose Mourinho tung liền Vinicius Junior, Federico Valverde, Endrick và tiền đạo trẻ Carlos Espi vào sân để tạo canh bạc tất tay trên hàng công. "
            "Phút 66, Mbappé chuộc lỗi bằng pha kiến tạo để Jude Bellingham sút căng gỡ hòa 1-1, trước khi Carlos Espi ghi bàn ấn định thắng lợi 2-1 ở phút 86 giúp Real Madrid san bằng 33 điểm với đội đầu bảng Barcelona."
        ),
        "source": "VnExpress / Tuổi Trẻ / Dân Trí",
        "news_source": "VNEXPRESS / TUỔI TRẺ / DÂN TRÍ",
        "credit": "AP / REUTERS",
        "stat_badges": {
            "2": {"label": "CÚ SÚT PHÚT 39", "value": "HỎNG 3/6 PEN", "sub": "Mbappé sút vọt xà từ chấm 11m"},
            "4": {"label": "BÁM ĐUỔI BARCA", "value": "33 ĐIỂM", "sub": "Bellingham 66' • Carlos Espi 86'"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_RMA_1)], "DÂN TRÍ / REUTERS", "Kylian Mbappé ôm đầu tiếc nuối sau cú đá phạt đền vọt xà phút 39"),
            _slot("title", 0, [_url(VNE_RMA_2)], "VNEXPRESS / AP", "Jude Bellingham ăn mừng bàn gỡ hòa 1-1 quan trọng cho Real Madrid"),
            _slot("title", 0, [_url(VNE_RMA_3)], "VNEXPRESS / AP", "Tài năng trẻ Carlos Espi ghi bàn thắng vàng ở phút 86 tại Bernabeu"),
            _slot("sentence", 1, [_url(DT_RMA_2)], "DÂN TRÍ / REUTERS", "Celta Vigo bất ngờ vươn lên dẫn trước sau 15 đường chuyền phối hợp ngay phút thứ sáu"),
            _slot("sentence", 1, [_url(VNE_RMA_1)], "VNEXPRESS / AP", "Hàng công Real Madrid gặp nhiều bế tắc trước lối chơi kỷ luật của đội khách"),
            _slot("sentence", 2, [_url(DT_RMA_1)], "DÂN TRÍ / REUTERS", "Đây là lần thứ ba trong sáu lượt sút 11 mét gần nhất Mbappé không thành công"),
            _slot("sentence", 2, [_url(VNE_RMA_1)], "VNEXPRESS / AP", "Thủ môn Ionut Radu của Celta Vigo có hiệp một thi đấu xuất sắc"),
            _slot("sentence", 3, [_local(DAILY_21 / "Tin_13_2.jpg")], "REUTERS", "HLV Jose Mourinho điều chỉnh hàng loạt ngôi sao tấn công trong hiệp hai"),
            _slot("sentence", 3, [_url(DT_RMA_2)], "DÂN TRÍ / REUTERS", "Real Madrid chơi với bốn tiền đạo cùng lúc trong những phút cuối"),
            _slot("sentence", 4, [_url(VNE_RMA_2)], "VNEXPRESS / AP", "Bellingham đạt dấu ấn bàn thắng thứ chín tại La Liga mùa này"),
            _slot("sentence", 4, [_url(VNE_RMA_3)], "VNEXPRESS / AP", "Carlos Espi tỏa sáng giữ trọn ba điểm, gây áp lực lên Barcelona trước trận gặp Villarreal"),
        ],
    },

    # 15 (Nam — PSG THẮNG NICE 3-2 & CHẤN THƯƠNG DOUÉ)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "LIGUE 1",
        "title": "PSG thắng nghẹt thở Nice 3-2 nhưng trả giá đắt với chấn thương nặng của Doué",
        "summary": (
            "Paris Saint-Germain trải qua chuyến làm khách đầy cảm xúc trước Nice ở vòng 11 Ligue 1 tối ngày 21 tháng 11 để giành thắng lợi kịch tính 3-2. "
            "Các bàn thắng của Senny Mayulu, Désiré Doué cùng pha lập công quyết định ở phút cuối của Ferran Torres giúp đội bóng thủ đô nước Pháp mang về trọn vẹn ba điểm. "
            "Tuy nhiên, niềm vui chiến thắng của PSG lập tức bị phủ bóng đen khi ngôi sao tấn công trẻ Désiré Doué dính chấn thương đầu gối nghiêm trọng ở cuối hiệp một và phải rời sân bằng cáng trong nước mắt. "
            "Chia sẻ sau trận, tiền đạo người Pháp thừa nhận rất buồn và lo lắng, đặt ban huấn luyện PSG vào bài toán nhân sự nan giải sau khi Khvicha Kvaratskhelia cũng vừa phải nghỉ thi đấu từ tháng trước."
        ),
        "source": "ESPN / Sky Sports / The Guardian / Bongdaplus",
        "news_source": "ESPN / SKY SPORTS / GUARDIAN",
        "credit": "SKY SPORTS / GETTY",
        "stat_badges": {
            "2": {"label": "NICE 2-3 PSG", "value": "PHÚT CUỐI", "sub": "Ferran Torres ấn định chiến thắng"},
            "3": {"label": "ÁM ẢNH CHẤN THƯƠNG", "value": "DÉSIRÉ DOUÉ", "sub": "Chấn thương đầu gối nghiêm trọng"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_PSG_DOUE)], "SKY SPORTS", "Désiré Doué đau đớn rời sân bằng cáng trong trận PSG thắng Nice 3-2"),
            _slot("title", 0, [_ddgs("Ferran Torres PSG Paris Saint-Germain goal celebration")], "ESPN", "Ferran Torres ghi bàn thắng quyết định ở phút cuối giúp PSG giành ba điểm"),
            _slot("title", 0, [_ddgs("Paris Saint-Germain OGC Nice Ligue 1 match 2026")], "REUTERS", "Trận cầu năm bàn thắng đầy kịch tính trên sân Allianz Riviera"),
            _slot("sentence", 1, [_ddgs("Paris Saint-Germain Ligue 1 players celebrating goal")], "REUTERS", "PSG vượt qua sức ép lớn trên sân khách ở vòng 11 Ligue 1"),
            _slot("sentence", 1, [_ddgs("OGC Nice football team stadium Ligue 1")], "GETTY", "Nice chơi đầy nỗ lực nhưng vẫn trắng tay ở những khoảnh khắc cuối"),
            _slot("sentence", 2, [_ddgs("Senny Mayulu PSG Paris Saint-Germain football")], "ESPN", "Senny Mayulu và Ferran Torres lập công trong chiến thắng 3-2"),
            _slot("sentence", 2, [_ddgs("Ferran Torres football player celebration")], "REUTERS", "Bàn thắng muộn giúp đội bóng thủ đô duy trì ưu thế ở giải quốc nội"),
            _slot("sentence", 3, [_url(SKY_PSG_DOUE)], "SKY SPORTS", "Doué ngã xuống ôm đầu gối sau tình huống tiếp đất không thuận lợi"),
            _slot("sentence", 3, [_ddgs("Desire Doue PSG France football player")], "GUARDIAN", "Tiền đạo 21 tuổi bật khóc khi được nhân viên y tế khiêng khỏi sân"),
            _slot("sentence", 4, [_url(SKY_PSG_DOUE)], "SKY SPORTS", "Chấn thương của Doué nối dài danh sách vắng mặt sau Kvaratskhelia"),
            _slot("sentence", 4, [_ddgs("Parc des Princes PSG Paris stadium")], "REUTERS", "Hàng công PSG đứng trước thử thách lực lượng ở chặng đua sắp tới"),
        ],
    },

    # 16 (Nữ — SERIE A, BUNDESLIGA & SCOTLAND)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "BÓNG ĐÁ CHÂU ÂU",
        "title": "Cơn mưa bàn thắng châu Âu: AS Roma và Leipzig thắng 5-1, Hearts đè bẹp Dundee 8-0",
        "summary": (
            "Sân cỏ châu Âu đêm ngày 21 tháng 11 chứng kiến hàng loạt chiến thắng hủy diệt tại các giải vô địch quốc gia hàng đầu. "
            "Ở vòng 12 Serie A, AS Roma vùi dập Parma với tỷ số 5-1 ngay trên sân khách nhờ màn trình diễn bùng nổ của tiền đạo Donyell Malen với cú poker bốn bàn thắng cùng một pha lập công của Rodrigo Mora. "
            "Tại vòng 10 Bundesliga, RB Leipzig cũng giành thắng lợi 5-1 trên sân Union Berlin nhờ sự tỏa sáng của Antonio Nusa, Brajan Gruda và các đồng đội, trong khi Borussia Dortmund vượt qua Monchengladbach 1-0 nhờ bàn thắng phút 80 của Felix Nmecha. "
            "Ấn tượng hơn cả về mặt tỷ số là tại giải vô địch quốc gia Scotland, câu lạc bộ Hearts trút cơn mưa tám bàn không gỡ vào lưới Dundee khiến huấn luyện viên đối thủ phải công khai xin lỗi người hâm mộ."
        ),
        "source": "The Guardian / BBC Sport / AS Roma / Bongda24h",
        "news_source": "GUARDIAN / BBC SPORT / AS ROMA",
        "credit": "REUTERS / GETTY",
        "stat_badges": {
            "2": {"label": "PARMA 1-5 AS ROMA", "value": "MALEN 4 BÀN", "sub": "Cùng bàn thắng của Rodrigo Mora"},
            "4": {"label": "GIẢI SCOTLAND", "value": "HEARTS 8-0 DUNDEE", "sub": "Leipzig 5-1 • Dortmund 1-0"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Donyell Malen AS Roma Serie A goal celebration")], "AS ROMA", "Donyell Malen lập cú poker bốn bàn giúp AS Roma đè bẹp Parma 5-1"),
            _slot("title", 0, [_ddgs("RB Leipzig Bundesliga football players celebration")], "BUNDESLIGA", "RB Leipzig thắng đậm 5-1 trên sân Union Berlin ở vòng 10 Bundesliga"),
            _slot("title", 0, [_ddgs("Heart of Midlothian Hearts Scottish Premiership goal")], "BBC SPORT", "Hearts tạo cơn địa chấn khi hủy diệt Dundee với tỷ số 8-0"),
            _slot("sentence", 1, [_ddgs("Stadio Ennio Tardini Parma AS Roma Serie A")], "REUTERS", "Các giải vô địch châu Âu chứng kiến nhiều trận đấu bùng nổ bàn thắng"),
            _slot("sentence", 1, [_ddgs("Bundesliga football match stadium action")], "REUTERS", "Nhóm các đội bóng lớn đồng loạt thể hiện sức mạnh tấn công"),
            _slot("sentence", 2, [_ddgs("Donyell Malen football celebration")], "AS ROMA", "Donyell Malen ghi tới bốn bàn trong ngày AS Roma thăng hoa tại Ennio Tardini"),
            _slot("sentence", 2, [_ddgs("Rodrigo Mora football player action")], "GETTY", "Rodrigo Mora đóng góp một bàn vào thắng lợi 5-1 của đại diện thủ đô Ý"),
            _slot("sentence", 3, [_ddgs("Antonio Nusa RB Leipzig football player")], "BUNDESLIGA", "Antonio Nusa và các đồng đội giúp Leipzig vượt qua Union Berlin 5-1"),
            _slot("sentence", 3, [_ddgs("Felix Nmecha Borussia Dortmund goal celebration")], "BUNDESLIGA", "Felix Nmecha ghi bàn duy nhất phút 80 mang về ba điểm cho Dortmund"),
            _slot("sentence", 4, [_ddgs("Tynecastle Park Hearts football club Scotland")], "BBC SPORT", "Hearts ghi tám bàn không gỡ vào lưới đội khách Dundee chỉ còn 10 người"),
            _slot("sentence", 4, [_ddgs("Scottish Premiership football match action")], "GUARDIAN", "HLV Steven Pressley của Dundee thừa nhận xấu hổ sau thất bại nặng nề"),
        ],
    },

    # 17 (Nam — MESSI & INTER MIAMI THẢM BẠI 0-3)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "MLS CUP 2026",
        "title": "Messi nhận danh hiệu Vua phá lưới MLS nhưng Inter Miami thua sốc Columbus Crew 0-3",
        "summary": (
            "Sáng ngày 22 tháng 11 theo giờ Việt Nam, dù vừa nhận danh hiệu Vua phá lưới MLS 2026 với thành tích 26 bàn thắng cùng 17 pha kiến tạo, Lionel Messi vẫn không thể cứu Inter Miami khỏi trận thua đậm 0-3 trước Columbus Crew ở trận mở màn play-off MLS Cup. "
            "Đội bóng áo hồng tự bắn vào chân mình ngay phút thứ chín khi thủ môn Dayne St Clair phạm lỗi dẫn đến quả phạt đền của Gonzalo Tapia, trước khi hậu vệ Gonzalo Lujan nhận thẻ vàng thứ hai rời sân ở phút 36. "
            "Bản thân Messi chơi đầy quyết tâm với hai cơ hội nguy hiểm bị thủ môn Patrick Schulte xuất sắc cản phá và nhiều lần trao đổi chiến thuật với huấn luyện viên Kily Gonzalez ngoài đường biên nhưng vẫn phải nhận thẻ vàng vì nóng nảy. "
            "Trong thế thiếu người ở hiệp hai, Taha Habroune và Tapia tiếp tục ghi bàn đẩy Inter Miami vào thế chân tường trước trận lượt về trên sân khách vào ngày 28 tháng 11."
        ),
        "source": "Thanh Niên / ESPN / MLS",
        "news_source": "THANH NIÊN / ESPN / MLS",
        "credit": "REUTERS / AP",
        "stat_badges": {
            "1": {"label": "VUA PHÁ LƯỚI MLS", "value": "26 BÀN • 17 KT", "sub": "Inter Miami thua 0-3 trên sân nhà"},
            "4": {"label": "THỂ THỨC BEST-OF-3", "value": "NGÀY 28.11", "sub": "Phải thắng sân khách để đi tiếp"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_MESSI_1)], "THANH NIÊN / REUTERS", "Lionel Messi nhận danh hiệu Vua phá lưới nhưng Inter Miami vẫn thua 0-3"),
            _slot("title", 0, [_url(TN_MESSI_2)], "THANH NIÊN / AP", "Siêu sao Argentina bất lực trong thế đội nhà chơi thiếu người trước Columbus Crew"),
            _slot("title", 0, [_ddgs("Columbus Crew Inter Miami MLS Cup playoffs 2026")], "ESPN", "Columbus Crew tạo cú sốc ngay ở Game 1 vòng một play-off MLS Cup"),
            _slot("sentence", 1, [_url(TN_MESSI_1)], "THANH NIÊN / REUTERS", "Messi ghi 26 bàn và có 17 kiến tạo trong mùa giải chính thức MLS 2026"),
            _slot("sentence", 1, [_url(TN_MESSI_2)], "THANH NIÊN / AP", "Inter Miami có màn khởi đầu ác mộng ngay tại sân nhà"),
            _slot("sentence", 2, [_ddgs("Gonzalo Tapia Columbus Crew soccer goal")], "MLS", "Gonzalo Tapia mở tỷ số từ chấm 11 mét ngay phút thứ chín"),
            _slot("sentence", 2, [_ddgs("Inter Miami red card soccer match referee")], "REUTERS", "Thẻ đỏ của hậu vệ trái bất đắc dĩ Gonzalo Lujan khiến cục diện sụp đổ"),
            _slot("sentence", 3, [_url(TN_MESSI_1)], "THANH NIÊN / REUTERS", "Thủ môn Patrick Schulte chơi xuất sắc từ chối cú sút phạt của Messi"),
            _slot("sentence", 3, [_ddgs("Kily Gonzalez Inter Miami coach touchline")], "ESPN", "Messi liên tục ra sát đường biên trao đổi cùng HLV Kily Gonzalez"),
            _slot("sentence", 4, [_url(TN_MESSI_2)], "THANH NIÊN / AP", "Taha Habroune và Tapia ấn định thắng lợi 3-0 cho Columbus Crew"),
            _slot("sentence", 4, [_ddgs("Lower.com Field Columbus Crew stadium MLS")], "MLS", "Inter Miami buộc phải thắng trận ngày 28 tháng 11 nếu không muốn thành cựu vương"),
        ],
    },

    # 18 (Nữ — CHUNG KẾT ATP FINALS 2026)
    {
        "id": 18,
        "art_id": "art_18",
        "group": "QUẦN VỢT ATP FINALS",
        "title": "Chung kết trong mơ ATP Finals 2026 tối nay: Carlos Alcaraz chạm trán Alexander Zverev",
        "summary": (
            "Giải quần vợt ATP Finals 2026 tại Turin chính thức xác định hai gương mặt xuất sắc nhất bước vào trận chung kết tối ngày 22 tháng 11 là Carlos Alcaraz và tay vợt số một thế giới Alexander Zverev. "
            "Ở trận bán kết đầu tiên, dù phải quấn băng bảo vệ vùng đùi trái bị chấn thương, Alcaraz vẫn thể hiện bản lĩnh thép khi ngược dòng hạ Ben Shelton sau ba set căng thẳng 3-6, 6-3 và 7-6, nâng chuỗi thắng liên tiếp lên 13 trận. "
            "Ít giờ sau đó, Alexander Zverev tiếp tục phong độ hủy diệt khi vượt qua Daniil Medvedev với tỷ số 7-6 và 6-4, qua đó chưa để thua bất kỳ set nào từ đầu giải và cán mốc 69 trận thắng trong mùa giải 2026. "
            "Đây là lần đối đầu thứ 14 giữa hai nhà vô địch Grand Slam trong năm nay, với Alcaraz đang tạm dẫn 7-6 về đối đầu nhưng Zverev lại có kinh nghiệm hai lần đăng quang giải đấu cuối năm."
        ),
        "source": "BBC Sport / The Guardian / VnExpress / Dân Trí",
        "news_source": "BBC SPORT / VNEXPRESS / DÂN TRÍ",
        "credit": "AP / REUTERS",
        "stat_badges": {
            "2": {"label": "CARLOS ALCARAZ", "value": "13 TRẬN THẮNG", "sub": "Lội ngược dòng hạ Ben Shelton"},
            "3": {"label": "ALEXANDER ZVEREV", "value": "CHƯA THUA SET", "sub": "69 trận thắng mùa giải 2026"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_ATP_1)], "VNEXPRESS / AP", "Carlos Alcaraz ăn mừng chiến thắng kịch tính trước Ben Shelton tại bán kết"),
            _slot("title", 0, [_url(VNE_ATP_2)], "VNEXPRESS / AP", "Alexander Zverev đánh bại Daniil Medvedev để tiến vào chung kết ATP Finals"),
            _slot("title", 0, [_url(DT_ATP_1)], "DÂN TRÍ / GETTY", "Trận chung kết tại Turin là cuộc đọ sức giữa hai tay vợt hay nhất năm 2026"),
            _slot("sentence", 1, [_url(DT_ATP_1)], "DÂN TRÍ / GETTY", "Carlos Alcaraz lần thứ hai liên tiếp góp mặt ở trận tranh ngôi vô địch ATP Finals"),
            _slot("sentence", 1, [_url(DT_ATP_2)], "DÂN TRÍ / GETTY", "Số một thế giới Alexander Zverev hướng tới danh hiệu thứ ba tại giải đấu này"),
            _slot("sentence", 2, [_url(VNE_ATP_1)], "VNEXPRESS / AP", "Alcaraz áp đảo 7-1 trong loạt tie-break set quyết định dù gặp vấn đề ở đùi trái"),
            _slot("sentence", 2, [_ddgs("Ben Shelton tennis ATP Finals Turin")], "ATP TOUR", "Ben Shelton thắng set đầu 6-3 nhưng không thể cản bước tay vợt Tây Ban Nha"),
            _slot("sentence", 3, [_url(VNE_ATP_2)], "VNEXPRESS / AP", "Zverev giao bóng cực kỳ hiệu quả trước Daniil Medvedev trong chiến thắng hai set"),
            _slot("sentence", 3, [_url(DT_ATP_2)], "DÂN TRÍ / GETTY", "Tay vợt Đức dẫn đầu hệ thống ATP Tour với 69 chiến thắng trong năm 2026"),
            _slot("sentence", 4, [_local(DAILY_21 / "Tin_19_2.jpg")], "ATP TOUR", "Alcaraz từng thắng Zverev năm set ở bán kết Australia Mở rộng đầu năm"),
            _slot("sentence", 4, [_local(DAILY_21 / "Tin_19_1.jpg")], "ATP TOUR", "Trận chung kết tối 22 tháng 11 hứa hẹn màn so tài đỉnh cao tại Inalpi Arena"),
        ],
    },

    # 19 (Nam — F1 LAS VEGAS GP)
    {
        "id": 19,
        "art_id": "art_19",
        "group": "ĐUA XE F1",
        "title": "F1 Las Vegas GP rực lửa khẩu chiến Russell và Verstappen, Antonelli nhất Q3 nhưng mất Pole",
        "summary": (
            "Đường đua đêm F1 Las Vegas Grand Prix trở nên căng thẳng tột độ sau vòng phân hạng ngày 21 tháng 11 khi tân binh Kimi Antonelli của Mercedes chạy nhanh nhất Q3 nhưng đánh rơi vị trí xuất phát đầu tiên vì án phạt thay động cơ. "
            "Với kết quả tụt năm bậc xuống thứ sáu của Antonelli, nhà đương kim vô địch Max Verstappen được đôn lên giành Pole, xếp ngay bên cạnh đối thủ George Russell ở hàng xuất phát đầu tiên. "
            "Sức nóng giữa Verstappen và Russell càng bị đẩy lên cao sau pha va chạm bánh xe ở buổi chạy thử cuối cùng khiến tay đua người Anh công khai chỉ trích Verstappen đang làm ảnh hưởng tới toàn bộ các đồng nghiệp. "
            "Cũng tại đường phố Las Vegas ở chặng hạ màn giải đua nữ F1 Academy, tay đua Chloe Palmowski xuất sắc vượt qua đối thủ cạnh tranh để giành chiến thắng nghẹt thở."
        ),
        "source": "BBC Sport / The Guardian / Sky Sports / Formula 1",
        "news_source": "BBC SPORT / GUARDIAN / SKY SPORTS",
        "credit": "FORMULA 1 / SKY SPORTS",
        "stat_badges": {
            "2": {"label": "VÒNG PHÂN HẠNG Q3", "value": "VERSTAPPEN POLE", "sub": "Antonelli 1:33.893 phạt 5 bậc"},
            "4": {"label": "F1 ACADEMY FINALE", "value": "PALMOWSKI THẮNG", "sub": "Chặng đua kết mùa tại Las Vegas"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Max Verstappen Red Bull F1 Las Vegas Grand Prix")], "FORMULA 1", "Max Verstappen giành vị trí xuất phát đầu tiên cho chặng đua chính Las Vegas GP"),
            _slot("title", 0, [_ddgs("Kimi Antonelli Mercedes F1 car night race")], "FORMULA 1", "Tân binh Kimi Antonelli đạt vòng chạy nhanh nhất Q3 nhưng bị phạt năm bậc"),
            _slot("title", 0, [_ddgs("George Russell Mercedes F1 driver helmet")], "REUTERS", "George Russell thẳng thắn công kích Max Verstappen trước giờ đua chính"),
            _slot("sentence", 1, [_ddgs("Kimi Antonelli Mercedes F1 qualifying Las Vegas")], "FORMULA 1", "Antonelli lập thành tích 1 phút 33 giây 893 nhưng phải xuất phát từ vị trí thứ sáu"),
            _slot("sentence", 1, [_ddgs("Las Vegas Strip Circuit F1 night lights")], "FORMULA 1", "Đường đua ánh đèn Las Vegas chứng kiến nhiều án phạt thay thành phần động cơ"),
            _slot("sentence", 2, [_ddgs("Max Verstappen Red Bull Racing F1 car")], "REUTERS", "Verstappen và Russell chia nhau hai vị trí dẫn đầu trên vạch xuất phát"),
            _slot("sentence", 2, [_ddgs("Charles Leclerc Lewis Hamilton Ferrari F1 2026")], "FORMULA 1", "Bộ đôi Ferrari là Charles Leclerc và Lewis Hamilton gây thất vọng khi bị loại từ Q2"),
            _slot("sentence", 3, [_ddgs("George Russell Max Verstappen F1 drivers")], "GUARDIAN", "Hai tay đua xảy ra va chạm ở cua 14 trong buổi chạy thử FP3"),
            _slot("sentence", 3, [_ddgs("George Russell Mercedes F1 press conference")], "BBC SPORT", "Russell tuyên bố ai đó cần đứng lên đối đầu với lối lái xe của Verstappen"),
            _slot("sentence", 4, [_url(SKY_F1_ACA)], "SKY SPORTS", "Chloe Palmowski giành chiến thắng ấn tượng ở chặng cuối mùa giải F1 Academy"),
            _slot("sentence", 4, [_ddgs("F1 Academy race cars Las Vegas")], "SKY SPORTS", "Khép lại một mùa giải sôi động của sân chơi tốc độ dành cho các tay đua nữ"),
        ],
    },

    # 20 (Nữ — UFC QATAR & BOXING THẾ GIỚI)
    {
        "id": 20,
        "art_id": "art_20",
        "group": "VÕ THUẬT THẾ GIỚI",
        "title": "Địa chấn UFC Qatar: Stirling hạ knock-out Procházka, Lauren Price thống nhất đai quyền Anh",
        "summary": (
            "Sự kiện võ thuật tổng hợp UFC Fight Night tại Doha, Qatar tối ngày 21 tháng 11 đã chứng kiến cú sốc lớn khi võ sĩ bất bại người New Zealand Navajo Stirling hạ knock-out cựu vương hạng bán nặng Jiří Procházka. "
            "Ở thời điểm bốn phút 58 giây của hiệp hai, Stirling tung loạt đòn tay chuẩn xác đánh gục tượng đài người Cộng hòa Séc để giành chiến thắng lớn nhất sự nghiệp, trong khi Kevin Vallejos và Dan Hooker cũng thắng điểm tại sự kiện này. "
            "Trên sàn đấu quyền Anh chuyên nghiệp tại Cardiff, nữ võ sĩ Lauren Price làm nên lịch sử khi đánh bại Michaela Kotaskova với điểm số tuyệt đối 100-90 từ cả ba giám khảo. "
            "Thắng lợi áp đảo giúp Lauren Price thâu tóm chiếc đai WBO còn thiếu bên cạnh các đai WBA, WBC, IBF, IBO và Ring Magazine, trở thành nhà vô địch thế giới tuyệt đối đầu tiên trong lịch sử Xứ Wales."
        ),
        "source": "BBC Sport / Combat Press / Taipei Times",
        "news_source": "BBC SPORT / COMBAT PRESS",
        "credit": "UFC / BBC SPORT",
        "stat_badges": {
            "2": {"label": "UFC QATAR MAIN EVENT", "value": "KO HIỆP 2", "sub": "Navajo Stirling hạ Jiří Procházka"},
            "4": {"label": "QUYỀN ANH THẾ GIỚI", "value": "LAUREN PRICE", "sub": "Nhà vô địch tuyệt đối đầu tiên của Wales"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Navajo Stirling UFC MMA fighter")], "UFC", "Ngôi sao bất bại Navajo Stirling tạo địa chấn lớn tại UFC Fight Night Qatar"),
            _slot("title", 0, [_ddgs("Jiri Prochazka UFC light heavyweight fighter")], "UFC", "Cựu vương Jiří Procházka gục ngã ở giây cuối hiệp hai trước đòn đánh của Stirling"),
            _slot("title", 0, [_ddgs("Lauren Price boxing world champion belts")], "BBC SPORT", "Lauren Price đi vào lịch sử quyền Anh Xứ Wales với chiến thắng thống nhất đai"),
            _slot("sentence", 1, [_ddgs("UFC Fight Night Doha Qatar arena octagon")], "UFC", "Lồng bát giác tại Doha chứng kiến bất ngờ lớn nhất ở trận đấu chính hạng bán nặng"),
            _slot("sentence", 1, [_ddgs("Navajo Stirling MMA celebration UFC")], "UFC", "Võ sĩ trẻ New Zealand duy trì mạch bất bại ấn tượng trên đấu trường UFC"),
            _slot("sentence", 2, [_ddgs("Jiri Prochazka UFC octagon action")], "COMBAT PRESS", "Procházka nhận thất bại knock-out ở phút 4 giây 58 hiệp đấu thứ hai"),
            _slot("sentence", 2, [_ddgs("Dan Hooker UFC fighter octagon")], "UFC", "Cùng sự kiện, Dan Hooker đánh bại Brian Ortega bằng tính điểm đồng thuận"),
            _slot("sentence", 3, [_ddgs("Lauren Price boxer ring Cardiff fight")], "BBC SPORT", "Lauren Price thắng tuyệt đối 100-90 trước đối thủ người Séc Michaela Kotaskova"),
            _slot("sentence", 3, [_ddgs("women boxing championship fight ring")], "REUTERS", "Võ sĩ từng giành HCV Olympic hoàn toàn làm chủ trận tranh đai tại Cardiff"),
            _slot("sentence", 4, [_ddgs("Lauren Price boxing undisputed champion")], "BBC SPORT", "Cô chính thức sở hữu trọn bộ sáu danh hiệu lớn ở hạng bán trung nữ"),
            _slot("sentence", 4, [_ddgs("boxing championship belts collection ring")], "BBC SPORT", "Cột mốc lịch sử đưa tên tuổi Lauren Price vào ngôi đền huyền thoại thể thao Xứ Wales"),
        ],
    },

    # 21 (Nam — NBA & MOTOGP THẾ GIỚI)
    {
        "id": 21,
        "art_id": "art_21",
        "group": "BÓNG RỔ & MOTOGP",
        "title": "Sixers thoát thua dù Herro ghi 50 điểm tại NBA, Bezzecchi thắng Sprint mưa MotoGP Bồ Đào Nha",
        "summary": (
            "Sàn đấu bóng rổ nhà nghề Mỹ NBA ngày 21 tháng 11 bùng nổ kịch tính khi Philadelphia 76ers chật vật đánh bại Milwaukee Bucks với tỷ số 132-129 trong màn rượt đuổi nghẹt thở đến giây cuối cùng. "
            "Ngôi sao Tyler Herro của Bucks lập kỷ lục cá nhân với 50 điểm, 11 rebound và bảy kiến tạo, thậm chí ném thành công cú ba điểm gỡ hòa sát còi nhưng trọng tài xem lại băng hình xác định bóng rời tay sau khi hết giờ. "
            "Trên đường đua mô tô MotoGP chặng Bồ Đào Nha tại Portimão, tay đua Marco Bezzecchi của đội Aprilia đã xuất sắc cán đích đầu tiên ở cuộc đua nước rút Sprint trong điều kiện mặt đường trơn trượt vì mưa. "
            "Kết quả này tạo bước đệm căng thẳng cho cuộc đua chính tối ngày 22 tháng 11, nơi Marc Márquez và Jorge Martín bước vào màn phân định ngôi vô địch thế giới MotoGP 2026."
        ),
        "source": "ESPN / NBA / MotoGP",
        "news_source": "ESPN / NBA / MOTOGP",
        "credit": "ESPN / MOTOGP",
        "stat_badges": {
            "2": {"label": "76ERS 132-129 BUCKS", "value": "HERRO 50 ĐIỂM", "sub": "Cú ném gỡ hòa hết giờ bị hủy"},
            "4": {"label": "MOTOGP PORTIMÃO", "value": "BEZZECCHI SPRINT", "sub": "Chờ đại chiến Márquez vs Martín"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Tyler Herro Milwaukee Bucks NBA 2026")], "NBA / ESPN", "Tyler Herro bùng nổ với 50 điểm nhưng không thể cứu Milwaukee Bucks khỏi thất bại"),
            _slot("title", 0, [_ddgs("Philadelphia 76ers basketball NBA celebration")], "NBA / ESPN", "Philadelphia 76ers bảo toàn chiến thắng 132-129 sau khoảnh khắc xem lại băng hình"),
            _slot("title", 0, [_ddgs("Marco Bezzecchi Aprilia MotoGP racing rain")], "MOTOGP", "Marco Bezzecchi giành chiến thắng cuộc đua Sprint dưới mưa tại Portimão"),
            _slot("sentence", 1, [_ddgs("Philadelphia 76ers Milwaukee Bucks NBA game")], "ESPN", "76ers suýt đánh rơi lợi thế dẫn 10 điểm ở những phút cuối trận"),
            _slot("sentence", 1, [_ddgs("NBA basketball arena scoreboard clutch shot")], "NBA", "Chiến thắng bản lĩnh giúp Philadelphia 76ers duy trì đà hưng phấn"),
            _slot("sentence", 2, [_ddgs("Tyler Herro basketball shooting three pointer")], "ESPN", "Cú ném ba điểm của Herro rời tay chậm hơn còi kết thúc trận chỉ tích tắc"),
            _slot("sentence", 2, [_ddgs("NBA referee replay review court")], "NBA", "Trọng tài hủy pha ghi điểm quyết định sau khi kiểm tra đồng hồ thi đấu"),
            _slot("sentence", 3, [_ddgs("Marco Bezzecchi Aprilia MotoGP Portimao")], "MOTOGP", "Mặt đường ướt mưa tại Algarve chứng kiến màn bứt phá ấn tượng của Bezzecchi"),
            _slot("sentence", 3, [_ddgs("MotoGP race wet track Algarve Portugal")], "MOTOGP", "Đội đua Aprilia thể hiện khả năng thích nghi thời tiết vượt trội ở chặng Sprint"),
            _slot("sentence", 4, [_ddgs("Marc Marquez Jorge Martin MotoGP racers")], "MOTOGP", "Mọi ánh mắt đổ dồn vào cuộc đua vô địch giữa Marc Márquez và Jorge Martín"),
            _slot("sentence", 4, [_ddgs("Autodromo Internacional do Algarve Portimao MotoGP")], "MOTOGP", "Chặng đua chính tối 22 tháng 11 hứa hẹn kịch tính đến vòng cuối cùng"),
        ],
    },

    # 22 (Nữ — THỂ THAO INDONESIA RÚNG ĐỘNG 4 CA TỬ VONG)
    {
        "id": 22,
        "art_id": "art_22",
        "group": "AN TOÀN THỂ THAO",
        "title": "Thể thao Indonesia rúng động khi liên tiếp bốn vận động viên tử vong trong một tháng",
        "summary": (
            "Làng thể thao Indonesia đang đối mặt làn sóng phẫn nộ dữ dội sau khi vận động viên bơi chân vịt 20 tuổi Muhammad Ryan Najwan Muttaqin qua đời trong cuộc đua cự ly 3000 mét ngoài biển hôm 19 tháng 11. "
            "Thảm kịch tại Đại hội thể thao tỉnh Tây Java xảy ra chưa đầy ba tuần sau cái chết tương tự của nữ vận động viên 22 tuổi Syabilla Rizkia Putri Raharja ở đúng nội dung bơi chân vịt ngoài biển tại Trung Java. "
            "Tính chung trong khoảng một tháng qua, thể thao xứ vạn đảo đã ghi nhận tới bốn vận động viên thiệt mạng khi thi đấu và hậu phẫu, bao gồm cả nữ võ sĩ pencak silat 19 tuổi Ayudiah cùng một sinh viên chạy marathon 21 tuổi. "
            "Trước hàng trăm ca cần chăm sóc y tế và phản ứng gay gắt của dư luận, Bộ trưởng Thanh niên và Thể thao Indonesia Erick Thohir đã yêu cầu điều tra minh bạch và khẳng định không chiến thắng nào quý giá hơn sinh mạng vận động viên."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / KONI",
        "stat_badges": {
            "1": {"label": "THẢM KỊCH TÂY JAVA", "value": "3000M BIỂN", "sub": "VĐV 20 tuổi tử vong trên đường bơi"},
            "3": {"label": "BÁO ĐỘNG ĐỎ", "value": "4 CA TỬ VONG", "sub": "Liên tiếp trong khoảng một tháng"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_INDO_THOHIR)], "TUỔI TRẺ", "Bộ trưởng Erick Thohir lệnh điều tra toàn diện sau bốn ca tử vong liên tiếp"),
            _slot("title", 0, [_ddgs("open water finswimming race rescue ocean")], "TUỔI TRẺ", "Hai vận động viên bơi chân vịt Indonesia thiệt mạng chỉ trong chưa đầy một tháng"),
            _slot("title", 0, [_ddgs("medical rescue stretcher sports competition")], "TUỔI TRẺ", "Công tác giám sát y tế và cứu hộ tại các giải tỉnh Indonesia bị chất vấn dữ dội"),
            _slot("sentence", 1, [_ddgs("open water sea swimming competition buoys")], "TUỔI TRẺ", "VĐV 20 tuổi Muhammad Ryan gặp sự cố ở vòng bơi thứ ba khi đang dẫn đầu"),
            _slot("sentence", 1, [_ddgs("lifeguard rescue boat sea race")], "TUỔI TRẺ", "Khi anh được đưa vào bờ, lực lượng y tế đang quá tải chăm sóc nhiều VĐV kiệt sức"),
            _slot("sentence", 2, [_ddgs("finswimming swimmer competition ocean")], "TUỔI TRẺ", "Trước đó ngày 25 tháng 10, nữ VĐV Syabilla cũng tử vong khi bơi cự ly 3000 mét"),
            _slot("sentence", 2, [_ddgs("Indonesia sports arena competition")], "TUỔI TRẺ", "Cảnh sát đã đình chỉ cán bộ phụ trách kỹ thuật để làm rõ trách nhiệm cứu hộ"),
            _slot("sentence", 3, [_ddgs("pencak silat martial arts match Indonesia")], "TUỔI TRẺ", "Nữ võ sĩ pencak silat 19 tuổi và một VĐV marathon cũng qua đời trong tháng qua"),
            _slot("sentence", 3, [_ddgs("paramedic ambulance sports event emergency")], "TUỔI TRẺ", "Đại hội Trung Java từng ghi nhận tới 157 trường hợp phải chăm sóc y tế"),
            _slot("sentence", 4, [_url(TT_INDO_THOHIR)], "TUỔI TRẺ", "Ông Erick Thohir yêu cầu rà soát toàn bộ quy chuẩn an toàn thi đấu toàn quốc"),
            _slot("sentence", 4, [_ddgs("Ministry of Youth and Sports Indonesia Jakarta")], "TUỔI TRẺ", "Dư luận Indonesia đòi hỏi thay đổi căn bản quy trình cấp cứu thể thao"),
        ],
    },

    # 23 (100% Giọng Nữ — MỤC TIN VẮN CUỐI VIDEO: CÁC TIN THỂ THAO KHÁC)
    {
        "id": 23,
        "art_id": "art_23",
        "group": "CÁC TIN THỂ THAO KHÁC",
        "title": "Điểm nhanh các tin thể thao đáng chú ý khác",
        "voice_preset": "secondary",
        "summary": (
            "Tại các trận đấu khác của vòng 11 Ngoại hạng Anh, Coventry City thắng kịch tính Crystal Palace 3-2 nhờ pha phản lưới phút 85 của Dwight McNeil làm hỏng ngày ra mắt của tân huấn luyện viên Thomas Frank, trong khi Aston Villa bị Sunderland cầm hòa 0-0 và tâm điểm tối nay 23 giờ 30 sẽ là đại chiến Liverpool gặp Manchester United đánh dấu trận ra mắt của tân huấn luyện viên Mauricio Pochettino tại Anfield. "
            "Ở đấu trường U17 World Cup 2026, đương kim vô địch châu Á U17 Nhật Bản nhận thẻ đỏ của đội trưởng Motosuna rồi thua ngược U17 Colombia 1-2 bởi quả phạt đền phút bù giờ 90+3, U17 Brazil thắng nhọc Cộng hòa Ireland 2-1, còn FIFA ghi nhận kỷ lục hai cầu thủ 15 tuổi của Tajikistan và Fiji thi đấu tại hai kỳ World Cup U15 và U17 chỉ trong ba tuần. "
            "Tại giải bóng bầu dục Nations Championship tối ngày 21 tháng 11, tuyển Anh đè bẹp New Zealand 37-12 với cách biệt kỷ lục 25 điểm, đội tuyển Pháp thắng Argentina 45-17 để vào chung kết gặp Nam Phi dù Nam Phi vừa thua Ireland 17-20, còn Scotland vùi dập Nhật Bản 67-5 và Australia thắng Xứ Wales 29-26. "
            "Trên đấu trường golf và cầu lông thế giới, A-Lim Kim giữ ngôi đầu cách biệt một gậy trước số một thế giới Nelly Korda trước vòng cuối giải LPGA CME Group Tour Championship, còn đôi nam Malaysia Man Wei Chong và Tee Kai Wun đánh bại cặp hạt giống Ấn Độ để vào chung kết Hong Kong Open. "
            "Khép lại bản tin, luật sư của tỷ phú Elon Musk gây chú ý khi gia nhập nhóm của huyền thoại Tom Brady nhằm mua cổ phần câu lạc bộ Chelsea, trong khi ở trong nước tỉnh Vĩnh Long lần đầu khai mạc Giải đua ghe Ngo trên sông Láng Thé với khán đài 4000 chỗ ngồi và tổng giải thưởng 900 triệu đồng."
        ),
        "source": "BBC Sport / Sky Sports / ESPN / Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí",
        "news_source": "ĐIỂM ĐỌC TỔNG HỢP",
        "credit": "BBC SPORT / SKY SPORTS / TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "23H30 TỐI NAY", "value": "LIVERPOOL VS MU", "sub": "Màn ra mắt của HLV Pochettino"},
            "2": {"label": "U17 WORLD CUP", "value": "NHẬT BẢN 1-2", "sub": "Thua Colombia phút bù giờ 90+3"},
            "3": {"label": "RUGBY QUỐC TẾ", "value": "ANH 37-12 NZ", "sub": "Pháp vs Nam Phi ở chung kết"},
            "5": {"label": "ĐUA GHE NGO", "value": "4000 CHỖ NGỒI", "sub": "Lần đầu tổ chức trên sông Láng Thé"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_POCH)], "DÂN TRÍ / REUTERS", "HLV Mauricio Pochettino trước thử thách lớn tại Anfield đêm nay"),
            _slot("title", 0, [_url(SKY_RUGBY_FR)], "SKY SPORTS", "Tuyển bóng bầu dục Pháp thắng Argentina 45-17 để tiến vào chung kết"),
            _slot("title", 0, [_url(TT_GHENGO_1)], "TUỔI TRẺ", "Giải đua ghe Ngo Vĩnh Long sôi động trên sông Láng Thé"),
            # Câu 1: Premier League & Liverpool vs MU
            _slot("sentence", 1, [_ddgs("Coventry City Crystal Palace Premier League match")], "BBC SPORT", "Coventry thắng Crystal Palace 3-2 nhờ bàn phản lưới phút 85 của McNeil"),
            _slot("sentence", 1, [_url(DT_POCH)], "DÂN TRÍ / REUTERS", "HLV Mauricio Pochettino có trận ra mắt Man Utd gặp Liverpool lúc 23h30 tối nay"),
            # Câu 2: U17 World Cup Japan, Brazil, 15yo
            _slot("sentence", 2, [_url(TN_U17_JAP)], "THANH NIÊN", "U17 Nhật Bản nhận thẻ đỏ rồi thua đau Colombia ở phút bù giờ 90+3"),
            _slot("sentence", 2, [_url(VNE_U15_U17)], "VNEXPRESS / FIFA", "Hai thiếu niên 15 tuổi lập kỳ tích dự hai kỳ World Cup trẻ trong ba tuần"),
            # Câu 3: Rugby Nations Championship
            _slot("sentence", 3, [_url(SKY_RUGBY_FR)], "SKY SPORTS", "Pháp áp đảo Argentina để hẹn tái đấu Nam Phi ở chung kết tại Twickenham"),
            _slot("sentence", 3, [_url(SKY_RUGBY_WA)], "SKY SPORTS", "Australia thắng sát nút Xứ Wales 29-26 còn Anh thắng kỷ lục New Zealand 37-12"),
            # Câu 4: Golf LPGA & Badminton HK Open
            _slot("sentence", 4, [_url(SKY_LPGA)], "SKY SPORTS", "A-Lim Kim giữ ngôi đầu trước sự bám đuổi của Nelly Korda ở LPGA Tour Finale"),
            _slot("sentence", 4, [_ddgs("Man Wei Chong Tee Kai Wun badminton Hong Kong Open")], "BWF", "Đôi nam Malaysia giành vé vào chơi trận chung kết Hong Kong Open 2026"),
            # Câu 5: Chelsea stake & Đua ghe Ngo Vĩnh Long
            _slot("sentence", 5, [_ddgs("Tom Brady Chelsea football Stamford Bridge")], "GUARDIAN", "Nhóm đầu tư của Tom Brady có thêm luật sư của Elon Musk tham gia hỏi mua cổ phần Chelsea"),
            _slot("sentence", 5, [_url(TT_GHENGO_1)], "TUỔI TRẺ", "Hơn 1200 VĐV tranh tài tại Giải đua ghe Ngo tỉnh Vĩnh Long mở rộng 2026"),
        ],
    },
]
