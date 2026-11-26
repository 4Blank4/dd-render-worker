# -*- coding: utf-8 -*-
"""
daily_26_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 26.11.2026
(Tổng hợp song hành báo Việt Nam & Thế giới: 12:00 ngày 25.11 đến 08:17 ngày 26.11.2026).
Tuân thủ quy chuẩn Anti-Bundling (1 sự kiện / 1 vấn đề = 1 tin, 3–5 câu súc tích):
  - Intro (00): Song giọng Nữ & Nam, hide_title=True
  - 25 bản tin chính độc lập (01–25): mỗi tin 1 vấn đề rõ ràng, luân phiên Nam/Nữ
  - Mục 26 (CÁC TIN THỂ THAO KHÁC): 100% Giọng Nữ điểm nhanh tin bên lề
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent


def _url(u: str) -> tuple[str, str]:
    return ("url", u)


def _ddgs(q: str) -> tuple[str, str]:
    return ("ddgs", q)


def _local(p: str) -> tuple[str, str]:
    return ("local", p)


def _slot(slot_type: str, sent_idx: int, sources: List[tuple[str, str]], credit: str, desc: str) -> Dict[str, Any]:
    return {
        "type": slot_type,
        "sentence_idx": sent_idx,
        "sources": sources,
        "credit": credit,
        "desc": desc,
    }


# ── URL ảnh báo chí sạch gốc 25–26.11.2026 (Việt Nam & Thế giới) ──

# 1. U17 Việt Nam & U17 World Cup 2026
TN_U17_LUC = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/u17-2-17954563777421047966338.jpeg"
DT_U17_TEAM = "https://cdnphoto.dantri.com.vn/KWAHElDJqs_-M7cvfMBq7xUjOdo=/thumb_w/1020/2026/11/24/u17vn7aseanfootball24-11-26-1795506829889.jpeg"
DT_U17_FIGHT = "https://cdnphoto.dantri.com.vn/zElJCOabXZwDNJPmcLr_Lo6Wzfs=/thumb_w/1020/2026/11/24/u17vn624-11-26-1795506627284.jpeg"
TT_U17_TAP = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/u17-viet-nam-tap-luyen-1795623370444809334255.jpg"
TT_U17_DAINHAN = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/dai-nhan-u17-new-zealand-1795578935971740563583.png"
TT_U17_VIET = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/dai-nhan-u17-viet-nam-17954392024301039720928.png"
TN_U17_ROL_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/17956161350313343106628512696865334310662851269686502a2beff3a7e36e30bf644d9e9d2bf69-17956170477881731706318.jpg"
TN_U17_ROL_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/roland-1-17955984953981246388654.jpeg"
TN_U17_MALI_COACH = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/179561618721771473839597338316537147383959733831653c3fca77e0ec7643adfc638d806e51fb5-17956172752751486896182.jpg"
TN_U17_REF = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/2026-11-05t182045z1148523536up1emb51eyjiprtrmadp3soccer-europa-and-rbs-17956053307941164399372.jpg"
TN_U17_REF_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/img9485-1536x1054-17956053972821276573741.jpeg"
VNE_MALI_1 = "https://i1-thethao.vnecdn.net/2026/11/25/img-1795589142-6859-1795589177.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=NwcOLccEGp4PTrOoZUmhCQ"
VNE_MALI_2 = "https://i1-thethao.vnecdn.net/2026/11/25/IMG-6862-9805-1795589175.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=0znOPjCTZUR1FPZcdsP65g"
TT_SY_BACH = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/sy-bach-1795616041063871237024.jpeg"
TN_SY_BACH_CARD = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/sy-bach-17955991015191417048407.png"
TN_U17_CELEB = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/u17-vn-1795397357515859549085.jpg"
TN_U17_KOR = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/f5349ab9-c47d-4b0f-8353-10eb8d8b4be5png-1795616727504383091846.jpg"
TN_U17_UGA = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/9d7fbc29-80bf-4d24-8c5d-fea6322cf92bpng-17956157819201779416261.jpg"

# 2. Thể Công Viettel, Buriram United & Port FC / CAHN
TN_TCVT_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/20a2-17956170732372061280262.jpg"
TN_TCVT_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/tcvt-1795599961755310973986.jpeg"
TT_TCVT_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/the-cong-164809-1795601576302374522542.jpeg"
DT_TCVT_4 = "https://cdnphoto.dantri.com.vn/19TiV_oCiuQGyPzXOgPdLU476Xs=/thumb_w/1020/2026/11/25/91650432711577027936778327587480509882413893n-edited-1795610760057.jpg"
DT_TCVT_5 = "https://cdnphoto.dantri.com.vn/dSaI_qHUZRn6Vq9BjnIIfRxq-eA=/thumb_w/1020/2026/11/25/92085826111577027870111667998560363012026374n-edited-1795610810079.jpg"
TT_BURIRAM_CANEDA = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/buriram-caneda-179560599810269397295.jpg"
TT_PORT_FC = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/edit-port-fc-1-1795617627538644584138.jpeg"
TN_CAHN_POLKING = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/cahn-vissel-kobe-3-17955278454542070901397.jpg"
TT_VAN_HAU = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/base64-1795599594893402369879.jpeg"

# 3. Đại hội Thể thao toàn quốc 2026 (Cầu lông, Bơi, Bắn súng, Taekwondo, Võ cổ truyền)
TN_LINH_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/tnw-179562030763862501232106622760886250123210662276088138fd923089b3fd8cedef038b063daf3-179562167704378946209.jpg"
TN_LINH_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/tnw-17956203076986250123210662276088625012321066227608812711c80a6df0a3d615c207343541ced-17956216771191243359327.jpg"
TN_LINH_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/tnw-17956188929884951488922155853666495148892215585366612804b424a8ed43080bffd9122fce5a7-1795619243748934247155.jpg"
VNE_LINH_4 = "https://i1-thethao.vnecdn.net/2026/11/25/4-JPG-1795624854-1795625145.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=7UWHA3MKff0PyOyV_oAKrw"
VNE_TRANG = "https://i1-thethao.vnecdn.net/2026/11/25/6-JPG-1795625063-1795625147.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=cFa2V2kKgeN4U-ORUGFyKQ"
VNE_CROWD = "https://i1-thethao.vnecdn.net/2026/11/26/Khan-gia-1795647318.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=lMmbKyWNMMNP4oAw7aYzpQ"
TN_MYTIEN_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/tnw-17953496431064951488922155853666495148892215585366625b4c632522d06aab56c7736f2d73750-17956102234311357296428.jpg"
TN_MYTIEN_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/tnw-1795350932698495148892215585366649514889221558536662ddfdaf588e84e38846d297303a861ce-17956102238741337852162.jpg"
VNE_AV_1 = "https://i1-thethao.vnecdn.net/2026/11/25/931970760-n-1795612798-7958-1795612914.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=XEHzsn6bkKirN1BYy9UXnA"
VNE_AV_2 = "https://iv1.vnecdn.net/thethao/images/web/2026/11/25/anh-vien-gianh-hc-vang-50m-ngua-1795621858.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=CTh21NGSX6DhQNkUHXmDnw"
VNE_AV_3 = "https://i1-thethao.vnecdn.net/2026/11/25/931970760-1648559800282746-168-7489-5393-1795612914.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=lKhCL5lYj5gojjT9fMX1GA"
VNE_AV_4 = "https://i1-thethao.vnecdn.net/2026/11/25/1795606131035-g770323143873897-4467-9354-1795609360.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=X_KyvoIbvLOmB3bixrRdHQ"
TN_PQH_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/pham-quang-huy--17956037875861140387814.jpg"
TN_PQH_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/hcv-quang-huy-9-bui-luong-17956047487781861712571.jpg"
TT_PQH_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/179560620003420664181444029384276225853887195716592126fa78c0617c4aeb95374f562fd359f-17956063515631403194409.jpg"
TT_CTV_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/base64-17956063655182142963952.jpeg"
TT_CTV_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/base64-17956063655371149523535.jpeg"
TT_CTV_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/base64-17956063655621857900621.jpeg"
TT_SUTHAY = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/25/568f5f90-a42e-48ed-addb-1f212277fe3e-1-17956137835821835345220.png"

# 4. Champions League & Bóng đá Thế giới 26.11.2026
TN_MU_POCH = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/pochettino-mu-1795654878863518295693.jpg"
TN_MU_POCH_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/pochettino--1795654878837416751715.jpg"
VNE_MU_1 = "https://i1-thethao.vnecdn.net/2026/11/26/man-utd-1795642979-7283-1795643293.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=4qtjuvsFaVKFY1eAdRCrLA"
VNE_MU_2 = "https://i1-thethao.vnecdn.net/2026/11/26/Man-Utd-3002-1795643292.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=bpcrlAnkIo3xmNwl9qFRuA"
VNE_MU_SPO = "https://i1-thethao.vnecdn.net/2026/11/26/Sporting-2044-1795645067.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=r1pO1xETme9NQoO1k1IOcw"
VNE_MU_DORGU = "https://i1-thethao.vnecdn.net/2026/11/26/Dorgu-3439-1795645067.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=S97Q_2nmtRBEEHkmbTET9w"
VNE_MU_REF_1 = "https://i1-thethao.vnecdn.net/2026/11/26/tro-ng-ta-i-marciniak-17956470-4642-5170-1795647959.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=_42DZeJ5EVD25yh76mu_PQ"
VNE_MU_REF_2 = "https://i1-thethao.vnecdn.net/2026/11/26/Marciniak-7801-1795645066.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=rAwOEAgfsfMjBNMriSDoUQ"
VNE_MU_TIE = "https://i1-thethao.vnecdn.net/2026/11/26/Tielemans-2637-1795647959.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=mZdnsRI0UzY1mJnLkr8Q0Q"
SKY_MU_LAMMENS = "https://e0.365dm.com/26/11/1600x900/skysports-senne-lammens-man-utd_7416704.jpg?20261125235511"
SKY_MU_SPO = "https://e0.365dm.com/26/11/1600x900/skysports-sanne-lammens-sporting_7416617.jpg?20261125221019"
SKY_MU_BRUNO = "https://e0.365dm.com/26/11/1600x900/skysports-bruno-fernandes-man-utd_7416591.jpg?20261125213050"
DT_MU_POCH = "https://cdnphoto.dantri.com.vn/NTY9hnvsqqNosbZm93r92iFZJ1E=/thumb_w/1020/2026/11/26/pochettino-1795649207924.jpg"
DT_MU_CUNHA = "https://cdnphoto.dantri.com.vn/ftjmslPEYPaeoaVMehkMFscOfVI=/zoom/1200_630/2026/11/25/matheus-cunha-manchester-united-l-1121839864-cropped-1795618284861.jpg"
DT_MU_DEJ = "https://cdnphoto.dantri.com.vn/sYNLiscGn8gXCJiuVB49tGpxEVY=/thumb_w/1020/2026/11/19/united-players-look-dejected-bournemouth-1118474354-1795049121191.jpg"

VNE_BAYERN_DAVIDE = "https://i1-thethao.vnecdn.net/2026/11/26/davide-jpg-1795648280-6785-1795648316.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=WEUM-IjmNwNsasqASGcJ6A"
SKY_LIV_ISAK = "https://e0.365dm.com/26/11/1600x900/skysports-alexander-isak-liverpool_7416550.jpg?20261125203911"
SKY_LIV_NGU = "https://e0.365dm.com/26/11/1600x900/skysports-rio-ngumoha-liverpool_7416586.jpg?20261125212429"
SKY_LIV_BRU = "https://e0.365dm.com/26/11/1600x900/skysports-liverpool-brugge_7416556.jpg?20261125204946"
BBC_LIV_WIRTZ = "https://ichef.bbci.co.uk/ace/standard/1056/cpsprodpb/b36f/live/27ecdb70-e922-11f1-a094-5fdc692f3e33.png"

VNE_BARCA_1 = "https://i1-thethao.vnecdn.net/2026/11/26/barca-jpg-1795646658-9627-1795646664.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=B-QIPGkq-ixZVOlqMpCvfw"
DT_BARCA_1 = "https://cdnphoto.dantri.com.vn/e3VrjvnSkk9QaKCwoHh0Z78Q2No=/thumb_w/1020/2026/11/26/barca2-cropped-1795647297544.jpg"
DT_BARCA_2 = "https://cdnphoto.dantri.com.vn/gGW_5sgtzZGLggRjIAKHr3HBVRU=/thumb_w/1020/2026/11/26/barca1-1795647288589.jpg"

VNE_PSG_1 = "https://i1-thethao.vnecdn.net/2026/11/26/2026-11-25T233050Z-1241836145-9621-7254-1795651660.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=m5gkVTF03D5FFwUEuhZReg"
VNE_PSG_2 = "https://i1-thethao.vnecdn.net/2026/11/26/2026t201045z-up1embp1k1whf-rtr-8205-1961-1795651660.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=tuOI-qbRF1no2JrHKnoHdw"

VNE_RONALDO_REF = "https://iv1.vnecdn.net/thethao/images/web/2026/11/25/ronaldo-che-mat-nhai-dong-tac-bao-viet-vi-cua-trong-tai-1795554697.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=rl3RXVrJKqoQEdZWtulOEA"
VNE_RONALDO_2 = "https://i1-thethao.vnecdn.net/2026/11/25/AFP-20261012-D32V29G-v1-MidRes-7257-9389-1795617125.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=EQthSIVvDFDdOITJQJ8MxQ"
BBC_CITY_REG = "https://ichef.bbci.co.uk/ace/standard/3840/cpsprodpb/894b/live/46715940-e913-11f1-8383-53f283141713.jpg"
BBC_CITY_2 = "https://ichef.bbci.co.uk/ace/standard/929/cpsprodpb/c146/live/274c5090-c642-11f1-abff-0d918239b2e3.jpg"
BBC_STERLING = "https://ichef.bbci.co.uk/ace/standard/905/cpsprodpb/78b1/live/4b3ef840-e8a2-11f1-869a-f96fd5660210.png"

# 5. Thể thao đa môn Thế giới (Cờ tướng, NFL, F1, Boxing, Cờ vua, Championship)
TT_TPV_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/3/2/trieu-phan-vi-1-1772432305137166110697.png"
TT_TPV_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/10/27/trieu-phan-vi-2-17931174757452143977339.png"
TT_TPV_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/5/17/ta-van-tinh-trieu-phan-vi-1779018046736860865112.jpg"
BBC_RODGERS = "https://ichef.bbci.co.uk/ace/standard/976/cpsprodpb/1B51/production/_121539960_rogers_big_bird_getty_976.jpg"
BBC_F1_WILLIAMS = "https://ichef.bbci.co.uk/ace/standard/3840/cpsprodpb/73ee/live/00ebc900-e8f5-11f1-8808-1d4222955d7e.jpg"
SKY_F1_VOWLES = "https://e0.365dm.com/26/11/1600x900/skysports-james-vowles-williams_7403380.jpg?20261110185518"
SKY_F1_SAINZ = "https://e0.365dm.com/26/09/1600x900/skysports-carlos-sainz-williams_7361279.jpg?20260925163803"
SKY_BOX_DUBOIS = "https://e0.365dm.com/24/09/1600x900/skysports-daniel-dubois-joseph-parker_6694816.jpg?20240923141617"
SKY_STOKE = "https://e0.365dm.com/26/11/1600x900/skysports-stoke-city_7416585.jpg?20261125212401"
SKY_BURNLEY = "https://e0.365dm.com/26/11/1600x900/skysports-birmingham-city_7416526.jpg?20261125200137"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 26.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 26 tháng 11 năm 2026, mang đến những diễn biến nóng bỏng nhất của thể thao Việt Nam và thế giới. "
        "Tại U17 World Cup, đội tuyển U17 Việt Nam bước vào trận quyết đấu gặp U17 Mali lúc 20 giờ tối nay với nhiệm vụ phải thắng để tự quyết tấm vé lịch sử vào vòng 32 đội, trong khi Thể Công Viettel dừng bước sớm ở Cúp C2 châu Á. "
        "Ở đấu trường quốc nội, Đại hội Thể thao toàn quốc 2026 chứng kiến Nguyễn Thùy Linh lập hat-trick huy chương vàng cầu lông, Võ Thị Mỹ Tiên chạm mốc sáu ngôi vô địch bơi lội còn Nguyễn Thị Ánh Viên cán mốc năm huy chương vàng kèm kỷ lục quốc gia. "
        "Trên sân cỏ châu Âu, Manchester United hòa hỗn loạn 2-2 trên sân Sporting CP trong ngày trọng tài gây bão chỉ trích, Bayern Munich nhận thất bại đầu tiên của mùa giải trước Lille, còn Liverpool và Barcelona đồng loạt thắng đậm."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí / BBC Sport / Sky Sports / The Guardian",
    "news_source": "VIỆT NAM & THẾ GIỚI",
    "credit": "ĐIỂM ĐỌC TỔNG HỢP",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 26 tháng 11 năm 2026, mang đến những diễn biến nóng bỏng nhất của thể thao Việt Nam và thế giới.",
        },
        {
            "voice_preset": "primary",
            "text": "Tại U17 World Cup, đội tuyển U17 Việt Nam bước vào trận quyết đấu gặp U17 Mali lúc 20 giờ tối nay với nhiệm vụ phải thắng để tự quyết tấm vé lịch sử vào vòng 32 đội, trong khi Thể Công Viettel dừng bước sớm ở Cúp C2 châu Á.",
        },
        {
            "voice_preset": "secondary",
            "text": "Ở đấu trường quốc nội, Đại hội Thể thao toàn quốc 2026 chứng kiến Nguyễn Thùy Linh lập hat-trick huy chương vàng cầu lông, Võ Thị Mỹ Tiên chạm mốc sáu ngôi vô địch bơi lội còn Nguyễn Thị Ánh Viên cán mốc năm huy chương vàng kèm kỷ lục quốc gia.",
        },
        {
            "voice_preset": "primary",
            "text": "Trên sân cỏ châu Âu, Manchester United hòa hỗn loạn 2-2 trên sân Sporting CP trong ngày trọng tài gây bão chỉ trích, Bayern Munich nhận thất bại đầu tiên của mùa giải trước Lille, còn Liverpool và Barcelona đồng loạt thắng đậm.",
        },
    ],
    "stat_badges": {
        "1": {"label": "BẢN TIN NGÀY", "value": "26.11.2026", "sub": "Toàn cảnh Việt Nam & Thế giới"},
        "2": {"label": "U17 WORLD CUP", "value": "20H • VIỆT NAM - MALI", "sub": "Thắng là chắc vé vòng 32 đội"},
        "4": {"label": "CHAMPIONS LEAGUE", "value": "MU 2-2 • BAYERN THUA 1-2", "sub": "Liverpool thắng 3-0 • Barcelona 4-1"},
    },
    "slots": [
        # Câu 1 (4 ảnh)
        _slot("sentence", 1, [_url(VNE_MU_1)], "VNEXPRESS", "Manchester United trải qua trận hòa 2-2 đầy sóng gió tại Lisbon rạng sáng 26 tháng 11"),
        _slot("sentence", 1, [_url(TN_U17_LUC)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực và U17 Việt Nam trước giờ quyết đấu với U17 Mali"),
        _slot("sentence", 1, [_url(VNE_LINH_4)], "VNEXPRESS", "Nguyễn Thùy Linh đăng quang lần thứ ba liên tiếp tại Đại hội Thể thao toàn quốc"),
        _slot("sentence", 1, [_url(SKY_LIV_ISAK)], "SKY SPORTS", "Alexander Isak lập cú đúp giúp Liverpool thắng đậm Club Brugge 3-0"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(DT_U17_TEAM)], "DÂN TRÍ", "Đội tuyển U17 Việt Nam quyết tâm tạo nên kỳ tích tại Qatar tối 26 tháng 11"),
        _slot("sentence", 2, [_url(VNE_MALI_1)], "VNEXPRESS", "U17 Mali dẫn đầu bảng G nhưng vẫn tuyên bố thi đấu quyết liệt"),
        _slot("sentence", 2, [_url(TN_TCVT_1)], "THANH NIÊN", "Thể Công Viettel hòa Melbourne Victory 0-0 và sớm dừng bước ở Cúp C2 châu Á"),
        _slot("sentence", 2, [_url(DT_TCVT_4)], "DÂN TRÍ", "Chuỗi không thắng của Thể Công Viettel trên mọi đấu trường đã kéo dài lên 12 trận"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url(TN_LINH_1)], "THANH NIÊN", "Nguyễn Thùy Linh đánh bại Vũ Thị Trang 2-0 tại nhà thi đấu Hồ Xuân Hương"),
        _slot("sentence", 3, [_url(TN_MYTIEN_1)], "THANH NIÊN", "Kình ngư Tây Ninh Võ Thị Mỹ Tiên bùng nổ với sáu huy chương vàng cá nhân"),
        _slot("sentence", 3, [_url(VNE_AV_1)], "VNEXPRESS", "Nguyễn Thị Ánh Viên cán mốc năm huy chương vàng và phá kỷ lục tiếp sức"),
        _slot("sentence", 3, [_url(TN_PQH_1)], "THANH NIÊN", "Xạ thủ Phạm Quang Huy thắng loạt bắn thêm nghẹt thở ở nội dung súng ngắn bắn nhanh"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_url(SKY_MU_BRUNO)], "SKY SPORTS", "Bruno Fernandes lập cú đúp chỉ trong hai phút vào lưới đội bóng cũ Sporting CP"),
        _slot("sentence", 4, [_url(VNE_BAYERN_DAVIDE)], "VNEXPRESS", "Huấn luyện viên Davide Ancelotti giúp Lille đánh bại Bayern Munich 2-1"),
        _slot("sentence", 4, [_url(VNE_BARCA_1)], "VNEXPRESS", "Barcelona đè bẹp Sabah 4-1 trong chuyến làm khách xa nhất lịch sử dự Cúp châu Âu"),
        _slot("sentence", 4, [_url(VNE_PSG_1)], "VNEXPRESS", "Nhà đương kim vô địch PSG bị AS Roma cầm hòa 2-2 ngay tại sân nhà Parc des Princes"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — U17 VIỆT NAM: CỤC DIỆN & KỊCH BẢN VÀO VÒNG 32 ĐỘI)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Việt Nam trước giờ G gặp U17 Mali: Cục diện bảng đấu và kịch bản vào vòng 32 đội",
        "summary": (
            "Lúc 20 giờ tối nay ngày 26 tháng 11 tại Qatar, đội tuyển U17 Việt Nam bước vào lượt trận hạ màn bảng G U17 World Cup 2026 gặp đội đầu bảng U17 Mali. "
            "Khép lại bốn bảng đấu đầu tiên đêm 25 tháng 11, các đội hạng ba gồm Uruguay sáu điểm, Mozambique bốn điểm, Ecuador bốn điểm và Qatar ba điểm khiến U17 Việt Nam bị đẩy xuống hạng tám trong nhóm 12 đội xếp thứ ba. "
            "Với một điểm và hiệu số bàn thắng bại âm một sau hai lượt trận, thầy trò huấn luyện viên Cristiano Roland sẽ nắm chắc tấm vé vào vòng 32 đội nếu đánh bại U17 Mali. "
            "Khi ấy, U17 Việt Nam đạt bốn điểm cùng hiệu số tối thiểu là không nhưng ghi nhiều bàn thắng hơn Ecuador, chắc chắn vượt qua cả Qatar lẫn các đội hạng ba ở bảng K và bảng L."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / DÂN TRÍ",
        "stat_badges": {
            "1": {"label": "LƯỢT CUỐI BẢNG G", "value": "20H • VIỆT NAM - MALI", "sub": "Sân Aspire Zone, Al Rayyan, Qatar"},
            "2": {"label": "ÁP LỰC VÉ VỚT", "value": "VIỆT NAM HẠNG 8/12", "sub": "1 điểm, hiệu số -1, đã ghi 5 bàn"},
            "3": {"label": "CỬA ĐI TIẾP 100%", "value": "THẮNG MALI = 4 ĐIỂM", "sub": "Chắc chắn vượt Ecuador, Qatar, bảng K & L"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_U17_TEAM)], "DÂN TRÍ", "Đội tuyển U17 Việt Nam bước vào trận quyết đấu cuối cùng bảng G gặp U17 Mali"),
            _slot("title", 0, [_url(TN_U17_LUC)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực và đồng đội hướng tới tấm vé lịch sử vào vòng 32 đội"),
            _slot("sentence", 1, [_url(TT_U17_TAP)], "TUỔI TRẺ", "U17 Việt Nam hoàn tất khâu chuẩn bị cho trận đấu lúc 20 giờ ngày 26 tháng 11"),
            _slot("sentence", 2, [_url(TT_U17_VIET)], "TUỔI TRẺ", "Cục diện các bảng A đến D vừa kết thúc khiến cuộc đua vé vớt thêm khốc liệt"),
            _slot("sentence", 3, [_url(DT_U17_FIGHT)], "DÂN TRÍ", "Chiến thắng trước Mali sẽ giúp thầy trò ông Roland tự quyết quyền đi tiếp"),
            _slot("sentence", 4, [_url(TN_U17_CELEB)], "THANH NIÊN", "Lợi thế ghi năm bàn sau hai lượt trận là điểm tựa quan trọng cho U17 Việt Nam"),
        ],
    },

    # 02 (Nữ — ĐẤU TRÍ TRƯỚC TRẬN MALI & TRỌNG TÀI "VUA THẺ" ELCHIN MASIYEV)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Mali cảnh giác cao độ trước U17 Việt Nam, trọng tài vua thẻ châu Âu bắt chính",
        "summary": (
            "Trước giờ bóng lăn, huấn luyện viên Cristiano Roland khẳng định U17 Việt Nam còn cơ hội là còn chiến đấu hết mình để tiếp tục mang lại niềm tự hào cho người hâm mộ nước nhà. "
            "Ở phía đối diện, dù U17 Mali đã toàn thắng sáu điểm và sớm giữ ngôi đầu bảng G, huấn luyện viên Soumaila Coulibaly vẫn tỏ ra thận trọng khi gọi U17 Việt Nam là một đối thủ mạnh và tuyên bố sẽ chơi tấn công quyết liệt. "
            "Tuy vậy, truyền thông Mali nhận định ban huấn luyện đội bóng Tây Phi nhiều khả năng vẫn xoay tua đội hình nhằm giữ sức cho vòng loại trực tiếp. "
            "FIFA đồng thời phân công trọng tài người Azerbaijan là ông Elchin Masiyev điều khiển trận đấu này, vị vua áo đen nổi tiếng nghiêm khắc với trung bình 3,36 thẻ vàng mỗi trận trong năm 2026."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ",
        "news_source": "THANH NIÊN / VNEXPRESS",
        "credit": "THANH NIÊN / VNEXPRESS",
        "stat_badges": {
            "2": {"label": "HLV U17 MALI", "value": "CẢNH GIÁC VIỆT NAM", "sub": "Khẳng định sẽ chơi tấn công quyết liệt"},
            "4": {"label": "TRỌNG TÀI FIFA", "value": "ELCHIN MASIYEV", "sub": "Trung bình 3,36 thẻ vàng mỗi trận"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_U17_ROL_1)], "THANH NIÊN", "Huấn luyện viên Cristiano Roland truyền lửa cho các học trò trước giờ quyết đấu"),
            _slot("title", 0, [_url(TN_U17_REF)], "THANH NIÊN / REUTERS", "Trọng tài Elchin Masiyev được FIFA giao cầm còi trận U17 Việt Nam gặp U17 Mali"),
            _slot("sentence", 1, [_url(TN_U17_ROL_2)], "THANH NIÊN", "Thầy trò huấn luyện viên Cristiano Roland thoải mái tâm lý ở buổi tập chiến thuật"),
            _slot("sentence", 2, [_url(TN_U17_MALI_COACH)], "THANH NIÊN", "Huấn luyện viên Soumaila Coulibaly đánh giá cao lối chơi giàu tốc độ của Việt Nam"),
            _slot("sentence", 3, [_url(VNE_MALI_2)], "VNEXPRESS", "Các cầu thủ U17 Mali có thể xoay tua nhân sự sau khi đã chắc chắn nhất bảng G"),
            _slot("sentence", 4, [_url(TN_U17_REF_2)], "THANH NIÊN", "Ông Elchin Masiyev từng rút tám thẻ vàng chỉ trong một trận tại Champions League"),
        ],
    },

    # 03 (Nam — FIFA ĐỀ CỬ SIÊU PHẨM CỦA LÊ SỸ BÁCH)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "U17 WORLD CUP 2026",
        "title": "FIFA đề cử siêu phẩm đánh gót của Lê Sỹ Bách là bàn thắng đẹp nhất U17 World Cup 2026",
        "summary": (
            "Trang chủ FIFA World Cup cùng tài khoản FIFA Training Centre vừa đồng loạt đăng tải lại đoạn video bàn thắng của tiền đạo Lê Sỹ Bách vào lưới U17 Bỉ và đưa pha lập công này vào danh sách đề cử Bàn thắng đẹp nhất U17 World Cup 2026. "
            "Đó là tình huống ở phút thứ tư trong trận ra quân ngày 20 tháng 11, khi tiền đạo thuộc lò đào tạo PVF thực hiện cú vô lê đánh gót chân trái đầy ngẫu hứng sau quả phạt góc của Nguyễn Minh Thủy. "
            "Trả lời phỏng vấn truyền thông FIFA, Sỹ Bách cho biết đây là bài phối hợp đá phạt góc mà toàn đội đã rèn luyện rất nhiều lần trên sân tập và vỡ òa hạnh phúc khi ghi bàn mở tỷ số đầu tiên cho Việt Nam tại giải. "
            "Chân sút trẻ đồng thời bày tỏ khát vọng tiếp tục tỏa sáng để hướng tới mục tiêu được thi đấu tại V-League và khoác áo đội tuyển quốc gia trong tương lai."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / FIFA",
        "news_source": "THANH NIÊN / TUỔI TRẺ / FIFA",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "ĐỀ CỬ TỪ FIFA", "value": "BÀN THẮNG ĐẸP NHẤT", "sub": "Pha giật gót chân trái phút 4 vào lưới Bỉ"},
            "3": {"label": "TÀI NĂNG LÒ PVF", "value": "LÊ SỸ BÁCH", "sub": "Mơ ước khoác áo tuyển quốc gia"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_SY_BACH)], "TUỔI TRẺ", "Tiền đạo trẻ Lê Sỹ Bách nhận đề cử danh giá từ FIFA tại U17 World Cup 2026"),
            _slot("title", 0, [_url(TN_SY_BACH_CARD)], "THANH NIÊN / FIFA", "Kênh truyền thông FIFA liên tục vinh danh siêu phẩm đánh gót của Sỹ Bách"),
            _slot("sentence", 1, [_url(TN_U17_LUC)], "THANH NIÊN / VFF", "Bàn thắng vào lưới U17 Bỉ được FIFA xem là ứng viên hàng đầu của giải đấu"),
            _slot("sentence", 2, [_url(TN_SY_BACH_CARD)], "THANH NIÊN / FIFA", "Pha cắt mặt đánh gót sau quả phạt góc của Minh Thủy khiến hàng thủ Bỉ bất ngờ"),
            _slot("sentence", 3, [_url(TT_U17_DAINHAN)], "TUỔI TRẺ", "Tinh thần đồng đội giúp các cầu thủ trẻ Việt Nam tự tin trước những đối thủ hàng đầu"),
            _slot("sentence", 4, [_url(TN_U17_CELEB)], "THANH NIÊN", "Thế hệ U17 Việt Nam đang cho thấy khát vọng vươn tầm sân chơi chuyên nghiệp"),
        ],
    },

    # 04 (Nữ — THỂ CÔNG VIETTEL BỊ LOẠI SỚM Ở CÚP C2 CHÂU Á)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "AFC CHAMPIONS LEAGUE TWO",
        "title": "Thể Công Viettel hòa Melbourne Victory 0-0, chính thức bị loại sớm ở Cúp C2 châu Á",
        "summary": (
            "Chiều ngày 25 tháng 11 trên đất Úc, câu lạc bộ Thể Công Viettel chỉ giành được kết quả hòa 0-0 trước chủ nhà Melbourne Victory ở lượt trận thứ năm bảng E AFC Champions League Two. "
            "Trong thế trận chịu nhiều sức ép, thủ môn Việt kiều Úc Caruso Minh Khang đã trở thành điểm tựa vững chắc với ít nhất bốn pha cứu thua xuất sắc trước khung thành đội khách. "
            "Ngược lại, hàng công của đại diện V-League dù tung ra 14 cú sút nhưng tỏ ra kém duyên và thậm chí bỏ lỡ cơ hội phản công thuận lợi ngay trong những phút bù giờ cuối trận. "
            "Chỉ có vỏn vẹn hai điểm sau năm lượt trận, Thể Công Viettel đứng chót bảng E, chính thức dừng bước sớm một vòng đấu và nối dài chuỗi không thắng trên mọi mặt trận lên con số 12."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / VNEXPRESS / DÂN TRÍ",
        "credit": "THANH NIÊN / DÂN TRÍ",
        "stat_badges": {
            "1": {"label": "LƯỢT 5 BẢNG E", "value": "MELBOURNE 0-0 VIETTEL", "sub": "Chính thức bị loại sớm trước 1 lượt đấu"},
            "4": {"label": "CHUỖI BÁO ĐỘNG", "value": "12 TRẬN KHÔNG THẮNG", "sub": "Mới có 2 điểm, xếp cuối bảng E"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_TCVT_1)], "THANH NIÊN", "Thể Công Viettel không thể tìm kiếm chiến thắng trên sân Melbourne Victory"),
            _slot("title", 0, [_url(DT_TCVT_4)], "DÂN TRÍ", "Đại diện V-League chính thức dừng bước từ vòng bảng AFC Champions League Two"),
            _slot("sentence", 1, [_url(TT_TCVT_3)], "TUỔI TRẺ", "Trận hòa 0-0 chiều 25 tháng 11 khép lại hy vọng đi tiếp của đội bóng áo lính"),
            _slot("sentence", 2, [_url(TN_TCVT_2)], "THANH NIÊN", "Thủ thành Việt kiều Caruso Minh Khang chơi nổi bật ngay trên quê hương"),
            _slot("sentence", 3, [_url(DT_TCVT_5)], "DÂN TRÍ", "Các mũi nhọn Thể Công Viettel bế tắc trước hàng thủ chủ nhà ở những thời điểm quyết định"),
            _slot("sentence", 4, [_url(DT_TCVT_4)], "DÂN TRÍ", "Huấn luyện viên Guilherme Almeida vẫn chưa có chiến thắng đầu tay sau khi lên nắm quyền"),
        ],
    },

    # 05 (Nam — BURIRAM SA THẢI HLV LẦN 3 TRONG 81 NGÀY & CAHN BỎ XA 3 CLB THÁI LAN)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "BÓNG ĐÁ ĐÔNG NAM Á",
        "title": "Buriram United sa thải huấn luyện viên lần ba trong 81 ngày, CAHN bỏ xa các đội Thái Lan",
        "summary": (
            "Chiều ngày 25 tháng 11, chưa đầy một ngày sau thất bại 1-3 trước Shanghai Port, đương kim vô địch Thái Lan Buriram United thông báo sa thải huấn luyện viên người Tây Ban Nha Raul Caneda chỉ sau 25 ngày bổ nhiệm. "
            "Ông Caneda chỉ kịp cầm quân bốn trận với một thắng, một hòa và hai thất bại, qua đó trở thành nhà cầm quân thứ ba rời ghế nóng tại Buriram chỉ trong vòng 81 ngày sau Mark Jackson và Mario Silva. "
            "Cùng ở lượt năm AFC Champions League Elite, đại diện Thái Lan khác là Port FC cũng để thua Gamba Osaka 0-2 vào tối 25 tháng 11. "
            "Sau năm vòng đấu, cả ba đội bóng Thái Lan mới thắng đúng một trong tổng số 15 trận với tổng cộng tám điểm, hoàn toàn bị câu lạc bộ Công an Hà Nội bỏ xa dù đại diện Việt Nam chỉ có một suất tham dự nhưng đang giữ bảy điểm và xếp hạng chín."
        ),
        "source": "Tuổi Trẻ / Thanh Niên",
        "news_source": "TUỔI TRẺ / THANH NIÊN",
        "credit": "TUỔI TRẺ / THANH NIÊN",
        "stat_badges": {
            "1": {"label": "BURIRAM UNITED", "value": "SA THẢI SAU 25 NGÀY", "sub": "Thay 3 HLV trưởng chỉ trong 81 ngày"},
            "4": {"label": "CÚP C1 CHÂU Á", "value": "CAHN BỎ XA THÁI LAN", "sub": "3 CLB Thái thắng 1/15 trận • CAHN 7 điểm"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_BURIRAM_CANEDA)], "TUỔI TRẺ", "Huấn luyện viên Raul Caneda mất việc tại Buriram United chỉ sau 25 ngày làm việc"),
            _slot("title", 0, [_url(TN_CAHN_POLKING)], "THANH NIÊN", "Công an Hà Nội vượt trội ba đại diện Thái Lan tại sân chơi Cúp C1 châu Á"),
            _slot("sentence", 1, [_url(TT_BURIRAM_CANEDA)], "TUỔI TRẺ", "Thất bại 1-3 trước Shanghai Port là giọt nước tràn ly với ban lãnh đạo Buriram"),
            _slot("sentence", 2, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_03_1.jpg"))], "VNEXPRESS", "Nhà vô địch Thái Lan liên tục biến động băng ghế chỉ đạo mùa giải năm nay"),
            _slot("sentence", 3, [_url(TT_PORT_FC)], "TUỔI TRẺ", "Port FC gục ngã 0-2 trên sân Gamba Osaka khiến bóng đá Thái Lan trắng tay ở lượt năm"),
            _slot("sentence", 4, [_url(TT_VAN_HAU)], "TUỔI TRẺ", "Sự tỏa sáng của Đoàn Văn Hậu và đồng đội giúp CAHN rộng cửa cạnh tranh top tám"),
        ],
    },

    # 06 (Nữ — NGUYỄN THÙY LINH LẬP HAT-TRICK HCV CẦU LÔNG ĐẠI HỘI)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "ĐẠI HỘI THỂ THAO TOÀN QUỐC",
        "title": "Nguyễn Thùy Linh thắng Vũ Thị Trang 2-0, lập hat-trick vô địch cầu lông Đại hội",
        "summary": (
            "Tối ngày 25 tháng 11, nhà thi đấu Hồ Xuân Hương tại Thành phố Hồ Chí Minh chật kín khán giả và ban tổ chức phải xếp thêm hơn 400 ghế dưới sân để phục vụ trận chung kết đơn nữ cầu lông giữa Nguyễn Thùy Linh và đàn chị Vũ Thị Trang. "
            "Trước sự cổ vũ cuồng nhiệt, tay vợt số một Việt Nam đang khoác áo Đồng Nai làm chủ hoàn toàn thế trận và giành chiến thắng áp đảo 2-0 với các tỷ số 21-9 và 21-10. "
            "Danh hiệu này giúp Nguyễn Thùy Linh hoàn tất cú hat-trick huy chương vàng đơn nữ qua ba kỳ Đại hội Thể thao toàn quốc liên tiếp vào các năm 2018, 2022 và 2026. "
            "Khép lại Đại hội, tay vợt 29 tuổi tiết lộ sẽ sang Thái Lan tập huấn khoảng 30 ngày trong tháng 12 để tích lũy điểm số hướng tới SEA Games 2027 và Olympic 2028."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "credit": "THANH NIÊN / VNEXPRESS",
        "stat_badges": {
            "2": {"label": "CHUNG KẾT ĐƠN NỮ", "value": "THÙY LINH 2-0 VŨ TRANG", "sub": "Tỷ số áp đảo 21-9 và 21-10"},
            "3": {"label": "KỶ LỤC ĐẠI HỘI", "value": "HAT-TRICK HCV", "sub": "Vô địch 3 kỳ liên tiếp 2018, 2022, 2026"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_LINH_4)], "VNEXPRESS", "Nguyễn Thùy Linh thể hiện đẳng cấp vượt trội ở chung kết đơn nữ tối 25 tháng 11"),
            _slot("title", 0, [_url(TN_LINH_1)], "THANH NIÊN", "Tay vợt Đồng Nai hoàn tất cú hat-trick huy chương vàng Đại hội toàn quốc"),
            _slot("sentence", 1, [_url(VNE_CROWD)], "VNEXPRESS", "Hàng nghìn khán giả lấp kín nhà thi đấu Hồ Xuân Hương theo dõi các trận chung kết"),
            _slot("sentence", 2, [_url(VNE_TRANG)], "VNEXPRESS", "Vũ Thị Trang nỗ lực thi đấu ở tuổi 34 nhưng không thể cản bước đàn em"),
            _slot("sentence", 3, [_url(TN_LINH_3)], "THANH NIÊN", "Nguyễn Thùy Linh không để thua bất kỳ ván đấu nào trên hành trình bảo vệ ngôi hậu"),
            _slot("sentence", 4, [_url(TN_LINH_2)], "THANH NIÊN", "Thùy Linh chuẩn bị tập huấn Thái Lan nhằm cải thiện thứ hạng thế giới hướng tới Olympic"),
        ],
    },

    # 07 (Nam — KÌNH NGƯ TÂY NINH VÕ THỊ MỸ TIÊN BÙNG NỔ 6 HCV CÁ NHÂN)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "ĐẠI HỘI THỂ THAO TOÀN QUỐC",
        "title": "Kình ngư Tây Ninh Võ Thị Mỹ Tiên lập thành tích khủng với sáu huy chương vàng cá nhân",
        "summary": (
            "Trên đường đua xanh Đại hội Thể thao toàn quốc ngày 25 tháng 11, nữ kình ngư 21 tuổi Võ Thị Mỹ Tiên của đoàn Tây Ninh tiếp tục tỏa sáng rực rỡ khi giành thêm cú đúp huy chương vàng ở hai nội dung khắc nghiệt bậc nhất. "
            "Ở chung kết 400 mét hỗn hợp cá nhân nữ, Mỹ Tiên bỏ xa năm đối thủ để cán đích đầu tiên với thành tích bốn phút 58 giây 21. "
            "Không lâu sau đó, cô tiếp tục thống lĩnh đường bơi 800 mét tự do nữ để mang về tấm huy chương vàng thứ hai trong ngày với thông số tám phút 55 giây 25. "
            "Chỉ sau bốn ngày thi đấu, Võ Thị Mỹ Tiên đã sở hữu tới sáu huy chương vàng cá nhân, đưa Tây Ninh vươn lên xếp nhì bảng tổng sắp môn bơi, chỉ sau đoàn Quân Đội."
        ),
        "source": "Thanh Niên",
        "news_source": "THANH NIÊN",
        "credit": "THANH NIÊN",
        "stat_badges": {
            "2": {"label": "400M HỖN HỢP & 800M", "value": "CÚ ĐÚP HCV NGÀY 25/11", "sub": "4p58s21 và 8p55s25 đầy thuyết phục"},
            "4": {"label": "SAU 4 NGÀY THI ĐẤU", "value": "6 HCV CÁ NHÂN", "sub": "Giúp Tây Ninh xếp nhì bảng tổng sắp môn bơi"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_MYTIEN_1)], "THANH NIÊN", "Võ Thị Mỹ Tiên thi đấu thăng hoa tại câu lạc bộ bơi lặn Phú Thọ"),
            _slot("title", 0, [_url(TN_MYTIEN_2)], "THANH NIÊN", "Kình ngư 21 tuổi của Tây Ninh đã giành tới sáu huy chương vàng cá nhân"),
            _slot("sentence", 1, [_url(TN_MYTIEN_1)], "THANH NIÊN", "Mỹ Tiên duy trì nền tảng thể lực bền bỉ dù thi đấu liên tiếp hai cự ly dài"),
            _slot("sentence", 2, [_url(TN_MYTIEN_2)], "THANH NIÊN", "Ở nội dung 400 mét hỗn hợp cá nhân, tay bơi Tây Ninh hoàn toàn áp đảo đường đua"),
            _slot("sentence", 3, [_url(TN_MYTIEN_1)], "THANH NIÊN", "Tấm huy chương vàng 800 mét tự do khẳng định vị thế số một ở các cự ly dài"),
            _slot("sentence", 4, [_url(TN_MYTIEN_2)], "THANH NIÊN", "Thành tích của Mỹ Tiên giúp đoàn Tây Ninh cạnh tranh sòng phẳng ở môn bơi"),
        ],
    },

    # 08 (Nữ — ÁNH VIÊN GIÀNH HCV THỨ 5 & PHÁ KỶ LỤC QUỐC GIA TIẾP SỨC)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "ĐẠI HỘI THỂ THAO TOÀN QUỐC",
        "title": "Ánh Viên giành huy chương vàng thứ năm nhờ chiến thắng 0,03 giây và kỷ lục tiếp sức",
        "summary": (
            "Tối ngày 25 tháng 11, kình ngư Nguyễn Thị Ánh Viên có ngày thi đấu thứ hai liên tiếp lập cú đúp huy chương vàng để nâng tổng thành tích tại Đại hội năm nay lên năm vàng và một bạc. "
            "Ở chung kết 50 mét ngửa nữ, cô chạm thành bể sau 29 giây 61 để đánh bại đối thủ bám đuổi quyết liệt Nguyễn Ngọc Thủy Tiên chỉ đúng 0,03 giây. "
            "Ít phút sau, Ánh Viên cùng Nguyễn Thúy Hiền, Võ Thị Bảo Ngọc và Trần Anh Thư thống trị nội dung tiếp sức 4x100 mét hỗn hợp nữ cho đoàn Quân Đội với thời gian bốn phút 15 giây 69. "
            "Thông số này giúp đội bơi Quân Đội phá sâu cả kỷ lục quốc gia cũ lẫn kỷ lục Đại hội, trong khi kình ngư trẻ Nguyễn Thúy Hiền tiếp tục dẫn đầu toàn giải với bảy huy chương vàng."
        ),
        "source": "VnExpress / Thanh Niên",
        "news_source": "VNEXPRESS / THANH NIÊN",
        "credit": "VNEXPRESS",
        "stat_badges": {
            "2": {"label": "50M NGỬA NỮ", "value": "29S61 • HƠN 0,03 GIÂY", "sub": "Nghẹt thở vượt Nguyễn Ngọc Thủy Tiên"},
            "3": {"label": "4X100M HỖN HỢP NỮ", "value": "PHÁ KỶ LỤC QUỐC GIA", "sub": "Quân Đội đạt 4 phút 15 giây 69"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_AV_1)], "VNEXPRESS", "Nguyễn Thị Ánh Viên rạng rỡ sau khi chạm mốc năm huy chương vàng Đại hội"),
            _slot("title", 0, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_07_1.jpg"))], "THANH NIÊN", "Kình ngư 30 tuổi thắng nghẹt thở 50 mét ngửa nữ chỉ với cách biệt 0,03 giây"),
            _slot("sentence", 1, [_url(VNE_AV_3)], "VNEXPRESS", "Ánh Viên tiếp tục truyền cảm hứng mạnh mẽ sau gần bốn năm rời đấu trường đỉnh cao"),
            _slot("sentence", 2, [_url("https://i1-thethao.vnecdn.net/2026/11/25/1795606131097-2609998466311226-1628-7227-1795609360.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=nfFOhQPEje9FLaqTaSngMg")], "VNEXPRESS", "Hệ thống tính giờ điện tử xác định Ánh Viên về nhất trước hai kình ngư chủ nhà"),
            _slot("sentence", 3, [_url(VNE_AV_4)], "VNEXPRESS", "Đội tiếp sức nữ Quân Đội ăn mừng kỷ lục quốc gia mới ở nội dung 4x100 mét hỗn hợp"),
            _slot("sentence", 4, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_08_1.jpg"))], "THANH NIÊN", "Nguyễn Thúy Hiền góp công lớn vào chuỗi huy chương vàng liên tiếp của đoàn Quân Đội"),
        ],
    },

    # 09 (Nam — BẮN SÚNG: PHẠM QUANG HUY THẮNG SHOOT-OFF NGHẸT THỞ 2-1)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "ĐẠI HỘI THỂ THAO TOÀN QUỐC",
        "title": "Nhà vô địch ASIAD Phạm Quang Huy thắng loạt bắn thêm nghẹt thở, đoạt huy chương vàng thứ hai",
        "summary": (
            "Chiều ngày 25 tháng 11 tại trường bắn Đại học Thể dục Thể thao Thành phố Hồ Chí Minh, xạ thủ Phạm Quang Huy của đoàn Hải Phòng đã giành tấm huy chương vàng đầy kịch tính ở nội dung 25 mét súng ngắn bắn nhanh nam. "
            "Dẫn trước đối thủ chủ nhà Trần Công Hiếu hai điểm trước loạt bắn cuối cùng, Quang Huy bất ngờ trượt cả năm phát khiến tỷ số bị san bằng 19-19 sau tám loạt. "
            "Bước vào loạt bắn phân định thắng thua cân não, bản lĩnh của nhà vô địch ASIAD giúp xạ thủ sinh năm 1996 bắn trúng hai phát để vượt qua đồng đội ở đội tuyển quốc gia với tỷ số 2-1. "
            "Chiến thắng này nâng thành tích khởi đầu của Phạm Quang Huy tại Đại hội năm nay lên hai huy chương vàng cá nhân cùng một huy chương bạc đồng đội."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "CHUNG KẾT SÚNG NGẮN", "value": "HÒA 19-19 SAU 8 LOẠT", "sub": "Phân định bằng loạt shoot-off cân não"},
            "3": {"label": "BẢN LĨNH NHÀ VÔ ĐỊCH", "value": "THẮNG 2-1 • 2 HCV", "sub": "Tấm HCV cá nhân thứ 2 cho đoàn Hải Phòng"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_PQH_1)], "THANH NIÊN", "Xạ thủ Phạm Quang Huy thể hiện bản lĩnh ở thời khắc quyết định nội dung 25 mét bắn nhanh"),
            _slot("title", 0, [_url(TN_PQH_2)], "THANH NIÊN", "Nhà vô địch ASIAD 2023 mang về tấm huy chương vàng cá nhân thứ hai cho Hải Phòng"),
            _slot("sentence", 1, [_url(TT_PQH_3)], "TUỔI TRẺ", "Cuộc đối đầu giữa Phạm Quang Huy và Trần Công Hiếu diễn ra căng thẳng từng loạt bắn"),
            _slot("sentence", 2, [_url(TN_PQH_1)], "THANH NIÊN", "Sự kịch tính lên đến đỉnh điểm khi tỷ số bị gỡ hòa 19-19 ở loạt thứ tám"),
            _slot("sentence", 3, [_url(TT_PQH_3)], "TUỔI TRẺ", "Quang Huy giữ vững sự điềm tĩnh để thắng 2-1 trong loạt shoot-off"),
            _slot("sentence", 4, [_url(TN_PQH_2)], "THANH NIÊN", "Xạ thủ sinh năm 1996 khởi đầu rực rỡ với hai HCV và một HCB tại Đại hội"),
        ],
    },

    # 10 (Nữ — TAEKWONDO CHÂU TUYẾT VÂN & BẢNG TỔNG SẮP HUY CHƯƠNG ĐẠI HỘI)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "ĐẠI HỘI THỂ THAO TOÀN QUỐC",
        "title": "Chị em Châu Tuyết Vân cùng giành huy chương, TP. HCM vững ngôi đầu bảng tổng sắp",
        "summary": (
            "Ngày thi đấu 25 tháng 11 ở môn taekwondo chứng kiến khoảnh khắc xúc động khi nữ võ sĩ kỳ cựu Châu Tuyết Vân cùng đàn em Hồ Thanh Ân mang về huy chương vàng nội dung quyền đôi nam nữ cho chủ nhà Thành phố Hồ Chí Minh. "
            "Ở tuổi 36, đây là lần trở lại đỉnh cao đầy ý nghĩa của Tuyết Vân sau kỳ Đại hội trước bị chấn thương, trong khi cô em gái út Châu Ngọc Tuyết Sang cũng đoạt huy chương bạc quyền cá nhân nữ trong lần đầu tham dự. "
            "Khép lại ngày thi đấu 25 tháng 11 lúc 22 giờ, đoàn Thành phố Hồ Chí Minh tiếp tục dẫn đầu bảng tổng sắp huy chương với 74 vàng, 58 bạc và 80 đồng, đạt tổng cộng 212 huy chương. "
            "Bám sát phía sau lần lượt là Hà Nội với 58 huy chương vàng, Quân Đội 35 huy chương vàng, Công an Nhân dân 28 vàng, Hải Phòng 21 vàng và Cần Thơ 20 vàng."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "TAEKWONDO QUYỀN ĐÔI", "value": "HCV CHÂU TUYẾT VÂN", "sub": "Em gái Tuyết Sang giành HCB cá nhân nữ"},
            "3": {"label": "BẢNG TỔNG SẮP 25/11", "value": "TP. HCM 74 HCV (212 HC)", "sub": "Hà Nội 58 HCV • Quân Đội 35 HCV"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_CTV_1)], "TUỔI TRẺ", "Châu Tuyết Vân và Hồ Thanh Ân giành huy chương vàng quyền đôi nam nữ taekwondo"),
            _slot("title", 0, [_url(TT_CTV_2)], "TUỔI TRẺ", "Chị em Châu Tuyết Vân và Châu Ngọc Tuyết Sang cùng mang vinh quang về cho TP. HCM"),
            _slot("sentence", 1, [_url(TT_CTV_1)], "TUỔI TRẺ", "Đẳng cấp thế giới giúp Châu Tuyết Vân vượt qua cặp đối thủ Hà Nội ở chung kết"),
            _slot("sentence", 2, [_url(TT_CTV_3)], "TUỔI TRẺ", "Cô em út Châu Ngọc Tuyết Sang giành tấm huy chương bạc ý nghĩa ngay lần đầu dự Đại hội"),
            _slot("sentence", 3, [_url(TT_CTV_2)], "TUỔI TRẺ", "Đoàn chủ nhà Thành phố Hồ Chí Minh nới rộng khoảng cách lên 74 huy chương vàng"),
            _slot("sentence", 4, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_08_2.jpg"))], "THANH NIÊN", "Các đoàn Hà Nội, Quân Đội và Công an Nhân dân bám đuổi quyết liệt phía sau"),
        ],
    },

    # 11 (Nam — MAN UTD 2-2 SPORTING CP: SAI LẦM LAMMENS & CÚ ĐÚP BRUNO FERNANDES)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "UEFA CHAMPIONS LEAGUE",
        "title": "Manchester United hòa hỗn loạn Sporting CP 2-2: Sai lầm thủ môn và cú đúp 2 phút của Bruno",
        "summary": (
            "Rạng sáng ngày 26 tháng 11 tại Lisbon, Manchester United trải qua trận hòa điên rồ 2-2 trước Sporting CP với ba quả phạt đền, hai bàn thắng bị từ chối và một chiếc thẻ đỏ. "
            "Phút 31, thủ môn Senne Lammens cản phá thành công cú sút 11 mét của Luis Suárez, nhưng chỉ 75 giây sau chính anh phạm lỗi để đối thủ sút phạt đền thứ hai mở tỷ số ở phút 33. "
            "Đầu hiệp hai, đội trưởng Bruno Fernandes tỏa sáng rực rỡ với cú đúp trong vòng hai phút vào lưới đội bóng cũ, gồm quả phạt đền phút 48 và cú sút xa đập mô đất gồ ghề bay vào lưới ở phút 50. "
            "Dẫu vậy, tới phút 80 thủ thành Lammens bắt hụt quả tạt đơn giản tạo điều kiện cho Suárez tung người móc bóng gỡ hòa 2-2, trước khi Youri Tielemans nhận thẻ vàng thứ hai rời sân ở phút bù giờ 90+3."
        ),
        "source": "VnExpress / Tuổi Trẻ / Sky Sports / The Guardian",
        "news_source": "SKY SPORTS / VNEXPRESS / THE GUARDIAN",
        "credit": "SKY SPORTS / VNEXPRESS",
        "stat_badges": {
            "1": {"label": "TRẬN CẦU HỖN LOẠN", "value": "SPORTING 2-2 MAN UTD", "sub": "3 phạt đền • 2 bàn bị hủy • 1 thẻ đỏ"},
            "3": {"label": "CÚ ĐÚP TRONG 2 PHÚT", "value": "BRUNO FERNANDES 48', 50'", "sub": "Ghi bàn kỳ lạ từ cú sút đập mô đất"},
            "4": {"label": "TAI HỌA PHÚT 80", "value": "LAMMENS BẮT HỤT BÓNG", "sub": "Suárez móc bóng gỡ hòa • Tielemans thẻ đỏ"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_MU_LAMMENS)], "SKY SPORTS", "Thủ môn Senne Lammens có một đêm thi đấu thảm họa tại sân José Alvalade"),
            _slot("title", 0, [_url(SKY_MU_BRUNO)], "SKY SPORTS", "Bruno Fernandes lập cú đúp chỉ trong hai phút vào lưới đội bóng cũ Sporting CP"),
            _slot("sentence", 1, [_url(VNE_MU_1)], "VNEXPRESS", "Trận đấu tại Lisbon chứng kiến hàng loạt diễn biến hỗn loạn khó tin"),
            _slot("sentence", 2, [_url(SKY_MU_SPO)], "SKY SPORTS", "Chỉ 75 giây sau khi cản phá phạt đền, Lammens lại tự tay biếu đối thủ quả 11 mét"),
            _slot("sentence", 3, [_url(VNE_MU_2)], "VNEXPRESS", "Bàn thắng nâng tỷ số lên 2-1 của Bruno Fernandes nảy qua đầu thủ môn Kaique Pereira"),
            _slot("sentence", 4, [_url(VNE_MU_SPO)], "VNEXPRESS", "Pha bắt bóng lỗi của Lammens ở phút 80 khiến Quỷ đỏ đánh rơi chiến thắng"),
            _slot("sentence", 4, [_url(VNE_MU_TIE)], "VNEXPRESS", "Youri Tielemans nhận thẻ đỏ ở phút 90+3 khép lại đêm đáng quên của Man Utd"),
        ],
    },

    # 12 (Nữ — TRỌNG TÀI MARCINIAK HỨNG BÃO CHỈ TRÍCH & MU RƠI HẠNG 19 / OPTA 27,48%)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "NGOẠI HẠNG ANH & CÚP C1",
        "title": "Trọng tài Marciniak bị tố xử ép Manchester United, Quỷ đỏ đứng hạng 19 với nguy cơ rớt hạng 27,48%",
        "summary": (
            "Sau trận hòa tại Bồ Đào Nha, trọng tài Szymon Marciniak hứng chịu làn sóng chỉ trích gay gắt từ các chuyên gia bóng đá Anh như Ashley Young, Owen Hargreaves và Dean Ashton khi tước hai bàn thắng của Manchester United. "
            "Ở phút 40, vị trọng tài từng bắt chung kết World Cup 2022 thổi phạt sớm khiến VAR không thể can thiệp cứu bàn thắng hợp lệ của Amad Diallo, rồi tới phút 83 tiếp tục từ chối pha phản lưới của thủ môn Sporting sau tác động từ Patrick Dorgu. "
            "Kết quả này khiến tân huấn luyện viên Mauricio Pochettino vẫn chưa có chiến thắng đầu tay sau thảm bại 0-4 trước Liverpool, đẩy Quỷ đỏ đứng đúng hạng 19 tại cả Champions League lẫn Ngoại hạng Anh. "
            "Trước tình cảnh chỉ có tám điểm sau 11 vòng tại giải quốc nội và trải qua chín trận liền không thắng, siêu máy tính Opta vừa đưa ra cảnh báo Manchester United đối mặt tới 27,48% nguy cơ phải xuống hạng mùa này."
        ),
        "source": "Thanh Niên / VnExpress / Dân Trí / The Guardian",
        "news_source": "THANH NIÊN / VNEXPRESS / DÂN TRÍ",
        "credit": "VNEXPRESS / DÂN TRÍ",
        "stat_badges": {
            "1": {"label": "TRANH CÃI TRỌNG TÀI", "value": "HỦY 2 BÀN CỦA MAN UTD", "sub": "Szymon Marciniak bị chuyên gia chỉ trích"},
            "3": {"label": "CÙNG ĐỨNG HẠNG 19", "value": "CHƯA THẮNG DƯỚI POCHETTINO", "sub": "8 điểm/11 vòng Ngoại hạng Anh"},
            "4": {"label": "SIÊU MÁY TÍNH OPTA", "value": "27,48% XUỐNG HẠNG", "sub": "0% cơ hội vô địch Ngoại hạng Anh"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_MU_REF_1)], "VNEXPRESS", "Trọng tài Szymon Marciniak trở thành tâm điểm chỉ trích sau hai quyết định gây tranh cãi"),
            _slot("title", 0, [_url(TN_MU_POCH)], "THANH NIÊN", "Huấn luyện viên Mauricio Pochettino vẫn bất lực trong việc tìm chiến thắng đầu tay"),
            _slot("sentence", 1, [_url(VNE_MU_REF_2)], "VNEXPRESS", "Giới chuyên môn Anh cho rằng pha thổi phạt của Marciniak ở phút 40 là sai lầm nghiêm trọng"),
            _slot("sentence", 2, [_url(VNE_MU_DORGU)], "VNEXPRESS", "Bàn thắng thứ ba của Man Utd ở phút 83 cũng bị từ chối sau khi trọng tài xem lại VAR"),
            _slot("sentence", 3, [_url(DT_MU_POCH)], "DÂN TRÍ", "Pochettino đối mặt áp lực lớn khi Man Utd tụt xuống vị trí thứ 19 ở hai đấu trường"),
            _slot("sentence", 4, [_url(DT_MU_CUNHA)], "DÂN TRÍ", "Dữ liệu siêu máy tính Opta cảnh báo kịch bản tồi tệ cho đội chủ sân Old Trafford"),
            _slot("sentence", 4, [_url(DT_MU_DEJ)], "DÂN TRÍ", "Chuỗi chín trận không thắng đẩy Man Utd vào nhóm ba đội cầm đèn đỏ Ngoại hạng Anh"),
        ],
    },

    # 13 (Nam — ĐỊA CHẤN TẠI PHÁP: BAYERN MUNICH THUA LILLE 1-2 CỦA CON TRAI ANCELOTTI)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "UEFA CHAMPIONS LEAGUE",
        "title": "Địa chấn nước Pháp: Bayern Munich nhận thất bại đầu mùa trước Lille của con trai Ancelotti",
        "summary": (
            "Đêm 25 tháng 11, chuỗi trận bất bại trên mọi đấu trường của Bayern Munich từ đầu mùa giải chính thức bị chặn đứng khi họ thua ngược sốc 1-2 trên sân của Lille. "
            "Do mất tiền đạo chủ lực Harry Kane nhiều tháng vì chấn thương dây chằng mắt cá và thiếu cả Michael Olise, hàng công Bayern chỉ còn trung vệ Dayot Upamecano đánh đầu mở tỷ số ở phút 15. "
            "Bước sang hiệp hai, đội bóng của huấn luyện viên Davide Ancelotti — con trai chiến lược gia lừng danh Carlo Ancelotti — bùng nổ mạnh mẽ với bàn gỡ hòa của chân sút Nhật Bản Ayase Ueda ở phút 62. "
            "Chỉ bốn phút sau, em trai Kylian Mbappé là Ethan Mbappé tung cú sút dội cột dọc khiến tiền vệ Aleksandar Pavlović lúng túng đá phản lưới nhà, giúp đội xếp hạng 35 Lille hạ gục gã khổng lồ nước Đức và đẩy Bayern xuống thứ 15."
        ),
        "source": "VnExpress / BBC Sport / The Guardian",
        "news_source": "VNEXPRESS / THE GUARDIAN / BBC",
        "credit": "VNEXPRESS / BING SEARCH",
        "stat_badges": {
            "1": {"label": "ĐỨT MẠCH BẤT BẠI", "value": "LILLE 2-1 BAYERN MUNICH", "sub": "Thất bại đầu tiên từ đầu mùa giải"},
            "3": {"label": "DẤU ẤN DAVIDE ANCELOTTI", "value": "UEDA 62' • PAVLOVIĆ PHẢN LƯỚI 66'", "sub": "Ethan Mbappé sút dội cột tạo bước ngoặt"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_BAYERN_DAVIDE)], "VNEXPRESS", "Huấn luyện viên Davide Ancelotti đánh bại đội bóng cũ Bayern Munich ngay tại Pháp"),
            _slot("title", 0, [_ddgs("Harry Kane Bayern Munich")], "BING SEARCH", "Bayern Munich nhận thất bại đầu tiên trong mùa giải khi vắng Harry Kane"),
            _slot("sentence", 1, [_ddgs("Lille football team celebration Champions League")], "BING SEARCH", "Đội chủ nhà đứng hạng 35 trước vòng đấu đã tạo nên cú sốc lớn nhất lượt năm"),
            _slot("sentence", 2, [_ddgs("Dayot Upamecano Bayern Munich header goal")], "BING SEARCH", "Trung vệ Dayot Upamecano mở tỷ số phút 15 trong ngày Bayern thiếu Harry Kane"),
            _slot("sentence", 3, [_url(VNE_BAYERN_DAVIDE)], "VNEXPRESS", "Con trai Carlo Ancelotti điều chỉnh chiến thuật sắc bén giúp Lille lội ngược dòng"),
            _slot("sentence", 4, [_ddgs("Aleksandar Pavlovic Bayern Munich")], "BING SEARCH", "Cú dứt điểm của Ethan Mbappé dẫn đến pha phản lưới nhà tai hại của Pavlović"),
        ],
    },

    # 14 (Nữ — LIVERPOOL ĐÈ BẸP CLUB BRUGGE 3-0 TRONG ĐÊM TÁI NGỘ SAU 48 NĂM)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "UEFA CHAMPIONS LEAGUE",
        "title": "Liverpool thắng đậm Club Brugge 3-0 trong lần tái ngộ lịch sử sau 48 năm",
        "summary": (
            "Tiếp đà hưng phấn sau trận thắng Manchester United 4-0 cuối tuần qua, Liverpool hành quân tới Bỉ đánh bại Club Brugge 3-0 rạng sáng 26 tháng 11 trong lần đầu hai đội tái ngộ kể từ chung kết Cúp C1 năm 1978. "
            "Ngay ở phút 13, đội trưởng thay thế Dominik Szoboszlai kiến tạo để tiền đạo Alexander Isak dứt điểm một chạm mở tỷ số. "
            "Đến phút 79, tài năng trẻ Rio Ngumoha đột phá dọn cỗ cho Florian Wirtz nhân đôi cách biệt, đánh dấu trận thứ ba liên tiếp ngôi sao người Đức nổ súng cho The Reds. "
            "Chỉ ba phút sau, thủ môn Alisson phát bóng dài để Isak thoát xuống tâng bóng qua đầu Yann Sommer ấn định chiến thắng 3-0, đưa chân sút Thụy Điển cán mốc 10 bàn mùa này và giúp Liverpool vươn lên hạng năm vòng phân hạng."
        ),
        "source": "VnExpress / Sky Sports / BBC Sport / The Guardian",
        "news_source": "SKY SPORTS / VNEXPRESS / BBC",
        "credit": "SKY SPORTS / BBC SPORT",
        "stat_badges": {
            "1": {"label": "TÁI NGỘ SAU 48 NĂM", "value": "CLUB BRUGGE 0-3 LIVERPOOL", "sub": "Gặp lại lần đầu từ chung kết C1 1978"},
            "4": {"label": "SONG TẤU ĐỈNH CAO", "value": "ISAK 13', 82' • WIRTZ 79'", "sub": "Liverpool vươn lên hạng 5 Champions League"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_LIV_ISAK)], "SKY SPORTS", "Alexander Isak lập cú đúp giúp Liverpool thắng thuyết phục tại Jan Breydel"),
            _slot("title", 0, [_ddgs("Florian Wirtz Liverpool football")], "BING SEARCH", "Florian Wirtz ghi bàn trong ba trận đấu liên tiếp cho đội bóng vùng Merseyside"),
            _slot("sentence", 1, [_url(SKY_LIV_BRU)], "SKY SPORTS", "Hai câu lạc bộ tái ngộ đầy cảm xúc trong tiếng hát You'll Never Walk Alone trên khán đài"),
            _slot("sentence", 2, [_url(SKY_LIV_ISAK)], "SKY SPORTS", "Chân sút 125 triệu bảng đã ghi bàn trong sáu chuyến làm khách liên tiếp"),
            _slot("sentence", 3, [_url(SKY_LIV_NGU)], "SKY SPORTS", "Rio Ngumoha kiến tạo thuận lợi để Florian Wirtz nhân đôi cách biệt ở phút 79"),
            _slot("sentence", 4, [_url(SKY_LIV_BRU)], "SKY SPORTS", "Liverpool có 12 điểm sau năm trận và sáng cửa vào thẳng vòng 16 đội"),
        ],
    },

    # 15 (Nam — BARCELONA THẮNG ĐẬM SABAH 4-1 TRONG CHUYẾN LÀM KHÁCH XA NHẤT LỊCH SỬ)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "UEFA CHAMPIONS LEAGUE",
        "title": "Barcelona thắng Sabah 4-1 trong chuyến làm khách xa nhất lịch sử dự Cúp châu Âu",
        "summary": (
            "Vượt quãng đường kỷ lục 3970 ki-lô-mét từ Tây Ban Nha tới thủ đô Baku của Azerbaijan, Barcelona vẫn giành chiến thắng tưng bừng 4-1 trước chủ nhà Sabah rạng sáng 26 tháng 11. "
            "Dù huấn luyện viên Hansi Flick xoay tua đội hình khi không mang theo Lamine Yamal và cất cả Rodri lẫn Raphinha, đại diện xứ Catalonia vẫn áp đảo hoàn toàn tân binh Champions League. "
            "Ngôi sao người Anh Anthony Gordon tỏa sáng với cú đúp bàn thắng ở phút 31 và phút 51, trước khi Karim Adeyemi cùng Gabriel Jesus ghi liên tiếp hai bàn ở phút 55 và 60 để định đoạt trận đấu. "
            "Bàn danh dự của Mickels ở phút 63 không thể ngăn Barcelona giành chiến thắng thứ tư sau năm lượt trận để vững vàng trong top bốn bảng xếp hạng."
        ),
        "source": "VnExpress / Dân Trí / The Guardian",
        "news_source": "VNEXPRESS / DÂN TRÍ / THE GUARDIAN",
        "credit": "VNEXPRESS / DÂN TRÍ",
        "stat_badges": {
            "1": {"label": "KỶ LỤC 3970 KM", "value": "SABAH 1-4 BARCELONA", "sub": "Chuyến đi xa nhất lịch sử Cúp châu Âu"},
            "3": {"label": "BÙNG NỔ HÀNG CÔNG", "value": "GORDON 31', 51' • ADEYEMI • JESUS", "sub": "Vắng Yamal vẫn đứng hạng 4 toàn giải"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_BARCA_1)], "VNEXPRESS", "Barcelona dễ dàng vượt qua đại diện Azerbaijan trong chuyến đi xa kỷ lục"),
            _slot("title", 0, [_url(DT_BARCA_1)], "DÂN TRÍ", "Anthony Gordon lập cú đúp dẫn dắt hàng công đội bóng xứ Catalonia"),
            _slot("sentence", 1, [_url(VNE_BARCA_1)], "VNEXPRESS", "Khoảng cách 3970 ki-lô-mét đến Baku phá kỷ lục cũ của Barcelona tại Nga"),
            _slot("sentence", 2, [_url(DT_BARCA_2)], "DÂN TRÍ", "Dù thiếu vắng Lamine Yamal, các cầu thủ tấn công khác vẫn chơi biến hóa"),
            _slot("sentence", 3, [_url(DT_BARCA_1)], "DÂN TRÍ", "Ba bàn thắng liên tiếp chỉ trong chín phút đầu hiệp hai nhấn chìm hy vọng của Sabah"),
            _slot("sentence", 4, [_url(DT_BARCA_2)], "DÂN TRÍ", "Thầy trò Hansi Flick tiến rất gần tấm vé vào thẳng vòng 16 đội"),
        ],
    },

    # 16 (Nữ — PSG HÒA AS ROMA 2-2, ĐỨT MẠCH TOÀN THẮNG)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "UEFA CHAMPIONS LEAGUE",
        "title": "Đương kim vô địch PSG lần đầu mất điểm sau trận hòa 2-2 trước AS Roma",
        "summary": (
            "Tại sân nhà Parc des Princes rạng sáng 26 tháng 11, nhà đương kim vô địch Paris Saint-Germain lần đầu tiên đánh rơi điểm số ở Champions League mùa này khi bị AS Roma cầm hòa 2-2. "
            "Trận cầu cởi mở giữa hai đội bóng có hàng công đạt hiệu suất trên hai bàn mỗi trận ghi nhận tổng chỉ số bàn thắng kỳ vọng lên tới 4,47. "
            "Cuộc đối đầu còn là màn đấu trí chiến thuật hấp dẫn giữa huấn luyện viên Luis Enrique — người từng có một năm dang dở ở Roma — và lối chơi kèm người quyết liệt của Gian Piero Gasperini. "
            "Dù PSG vượt lên dẫn 2-1, tiền đạo vào sân thay người Donyell Malen đã thực hiện thành công quả phạt đền ở phút 78 để kéo dài mạch ghi bàn bốn trận Champions League liên tiếp và giữ lại một điểm cho đại diện Italy."
        ),
        "source": "VnExpress / BBC Sport / The Guardian",
        "news_source": "VNEXPRESS / BBC SPORT",
        "credit": "VNEXPRESS / REUTERS",
        "stat_badges": {
            "1": {"label": "ĐỨT MẠCH TOÀN THẮNG", "value": "PSG 2-2 AS ROMA", "sub": "Trận cầu cởi mở với chỉ số xG 4,47"},
            "4": {"label": "PHÚT 78 QUYẾT ĐỊNH", "value": "DONYELL MALEN GHI BÀN", "sub": "Nổ súng 4 trận Champions League liên tiếp"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_PSG_1)], "VNEXPRESS / REUTERS", "PSG và AS Roma cống hiến màn rượt đuổi tỷ số hấp dẫn tại Paris"),
            _slot("title", 0, [_url(VNE_PSG_2)], "VNEXPRESS / REUTERS", "Huấn luyện viên Luis Enrique lần đầu mất điểm cùng PSG ở vòng phân hạng"),
            _slot("sentence", 1, [_url(VNE_PSG_1)], "VNEXPRESS / REUTERS", "Cả hai đội bóng hàng đầu nước Pháp và Italy đều chơi tấn công phóng khoáng"),
            _slot("sentence", 2, [_ddgs("PSG Roma Champions League football match 2026")], "BING SEARCH", "Tổng chỉ số bàn thắng kỳ vọng 4,47 phản ánh thế trận đôi công mãn nhãn"),
            _slot("sentence", 3, [_url(VNE_PSG_2)], "VNEXPRESS / REUTERS", "Ông Luis Enrique đối đầu triết lý kèm người một đối một giàu tốc độ của Gasperini"),
            _slot("sentence", 4, [_url("https://i1-thethao.vnecdn.net/2026/11/26/c5b0b3c5632e4ec986a8be10df0f1c-9308-3192-1795651661.png?w=1200&h=675&q=100&dpr=1&fit=crop&s=UHMb1U4ITom5uUsmO0HW5Q")], "VNEXPRESS", "Donyell Malen ghi bàn phạt đền phút 78 giúp Roma chấm dứt mạch toàn thắng của PSG"),
        ],
    },

    # 17 (Nam — CRISTIANO RONALDO ĐỐI MẶT ÁN TREO GIÒ 4 TRẬN TẠI AFC)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "BÓNG ĐÁ CHÂU Á",
        "title": "Cristiano Ronaldo đối mặt nguy cơ bị treo giò bốn trận vì cử chỉ chế nhạo trọng tài",
        "summary": (
            "Truyền thông Ả Rập Xê Út ngày 25 tháng 11 đồng loạt cảnh báo Cristiano Ronaldo có thể đối mặt án phạt nặng từ Liên đoàn Bóng đá châu Á sau cử chỉ gây tranh cãi trong trận Al Nassr thắng Al Sadd 2-1. "
            "Khi trọng tài chính người Jordan từ chối cho Al Nassr hưởng phạt đền và cắt còi việt vị, siêu sao 41 tuổi đã quay sang trọng tài biên dùng một tay che mắt rồi nhại động tác phất cờ. "
            "Theo Điều 49.1.1 trong Bộ Quy tắc Kỷ luật và Đạo đức của AFC, hành vi dùng cử chỉ khiếm nhã hoặc xúc phạm quan chức trận đấu có thể bị treo giò tối thiểu bốn trận hoặc ít nhất ba tháng kèm phạt tiền. "
            "Nếu án phạt được kích hoạt, đội trưởng Al Nassr có nguy cơ vắng mặt trong cả bốn lượt trận còn lại của vòng phân hạng, ảnh hưởng lớn tới toan tính của huấn luyện viên Ange Postecoglou."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / AFP",
        "stat_badges": {
            "2": {"label": "TRẬN AL NASSR - AL SADD", "value": "CHE MẮT NHẠI TRỌNG TÀI", "sub": "Phản ứng khi bị thổi việt vị hiệp 2"},
            "3": {"label": "ĐIỀU 49.1.1 LUẬT AFC", "value": "TREO GIÒ TỐI THIỂU 4 TRẬN", "sub": "Hoặc cấm thi đấu 3 tháng nếu bị kết luận"},
        },
        "slots": [
            _slot("title", 0, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_17_2.jpg"))], "VNEXPRESS", "Khoảnh khắc Ronaldo che mắt và nhại động tác phất cờ của trọng tài biên"),
            _slot("title", 0, [_url(VNE_RONALDO_2)], "VNEXPRESS / AFP", "Đội trưởng Al Nassr đối diện nguy cơ nghỉ hết phần còn lại của vòng phân hạng"),
            _slot("sentence", 1, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_17_3.jpg"))], "VNEXPRESS", "Ronaldo ghi bàn phạt đền nhưng phản ứng gay gắt khi bị thổi việt vị ở hiệp hai"),
            _slot("sentence", 2, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_17_1.jpg"))], "THANH NIÊN", "Phản ứng nóng nảy của tiền đạo 41 tuổi ngay trước ống kính truyền hình châu Á"),
            _slot("sentence", 3, [_url(VNE_RONALDO_2)], "VNEXPRESS / AFP", "Quy định kỷ luật của AFC áp dụng khung phạt rất nghiêm với hành vi xúc phạm trọng tài"),
            _slot("sentence", 4, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_17_2.jpg"))], "VNEXPRESS", "Al Nassr đứng thứ năm bảng đấu và rất cần Ronaldo ở bốn lượt trận quyết định"),
        ],
    },

    # 18 (Nữ — CƠ QUAN QUẢN LÝ ANH TƯỚC QUYỀN / ÉP ĐỔI CHỦ MAN CITY NẾU KHÁNG CÁO THUA)
    {
        "id": 18,
        "art_id": "art_18",
        "group": "NGOẠI HẠNG ANH",
        "title": "Cơ quan quản lý độc lập Anh tuyên bố sẵn sàng điều tra và ép đổi chủ Manchester City",
        "summary": (
            "Phát biểu trước Ủy ban Văn hóa, Truyền thông và Thể thao Quốc hội Anh ngày 25 tháng 11, Chủ tịch Cơ quan Quản lý Bóng đá Độc lập David Kogan khẳng định sẵn sàng hành động cứng rắn đối với Manchester City. "
            "Trước đó hồi tháng chín, một ủy ban độc lập đã kết luận giới chủ Abu Dhabi của Manchester City vi phạm quy tắc tài chính Ngoại hạng Anh suốt chín mùa giải, thổi phồng doanh thu và che giấu khoản lỗ tới 900 triệu bảng. "
            "Câu lạc bộ nửa xanh thành Manchester đã kháng cáo, nhưng ông Kogan nhấn mạnh cơ quan giám sát sẽ không chùn bước trước tên tuổi hay quy mô của bất kỳ đội bóng nào nếu phán quyết giữ nguyên. "
            "Theo luật định mới của nước Anh, Cơ quan Quản lý Độc lập có toàn quyền điều tra năng lực lãnh đạo, bãi nhiệm các giám đốc không đủ tư cách và thậm chí buộc chủ sở hữu phải bán lại câu lạc bộ."
        ),
        "source": "BBC Sport",
        "news_source": "BBC SPORT",
        "credit": "BBC SPORT",
        "stat_badges": {
            "2": {"label": "PHÁN QUYẾT THÁNG 9", "value": "GIAN LẬN 900 TRIỆU BẢNG", "sub": "Vi phạm tài chính suốt 9 mùa giải"},
            "4": {"label": "QUYỀN HẠN CỦA IFR", "value": "BÃI NHIỆM HOẶC ÉP BÁN CLB", "sub": "Nếu đơn kháng cáo của Man City thất bại"},
        },
        "slots": [
            _slot("title", 0, [_url(BBC_CITY_REG)], "BBC SPORT", "Chủ tịch IFR David Kogan tuyên bố cứng rắn trước Quốc hội về hồ sơ Manchester City"),
            _slot("title", 0, [_url(BBC_CITY_2)], "BBC SPORT", "Sân Etihad đối diện sóng gió pháp lý nếu đơn kháng cáo bị bác bỏ"),
            _slot("sentence", 1, [_url(BBC_CITY_REG)], "BBC SPORT", "Cơ quan Quản lý Bóng đá Độc lập khẳng định thực thi trách nhiệm công bằng với mọi CLB"),
            _slot("sentence", 2, [_url(BBC_CITY_2)], "BBC SPORT", "Vụ việc liên quan tới những thỏa thuận tài chính bị cáo buộc kéo dài chín mùa"),
            _slot("sentence", 3, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_14_1.jpg"))], "SKY SPORTS", "Ban lãnh đạo Manchester City đang chờ kết quả phân xử đơn kháng cáo chính thức"),
            _slot("sentence", 4, [_url(BBC_CITY_REG)], "BBC SPORT", "Luật mới cho phép cơ quan độc lập can thiệp sâu tới quyền sở hữu câu lạc bộ"),
        ],
    },

    # 19 (Nam — QUỸ ĐẦU TƯ SAUDI ARABIA RAO BÁN TỚI 25% CỔ PHẦN NEWCASTLE UNITED)
    {
        "id": 19,
        "art_id": "art_19",
        "group": "NGOẠI HẠNG ANH",
        "title": "Quỹ đầu tư công Saudi Arabia rao bán tới 25% cổ phần câu lạc bộ Newcastle United",
        "summary": (
            "Theo báo Anh The Guardian và The Athletic ngày 25 tháng 11, chủ sở hữu Newcastle United là Quỹ Đầu tư Công Saudi Arabia đã thuê ngân hàng JP Morgan xử lý kế hoạch phát hành cổ phần mới để bán tới 25% cổ phần đội bóng. "
            "Quỹ nhà nước hiện nắm giữ 84% cổ phần Chích chòe cùng 16% của anh em tỷ phú nhà Reuben kể từ sau thương vụ mua lại câu lạc bộ với giá 305 triệu bảng cách đây năm năm. "
            "Các nguồn tin khẳng định bên mua sẽ rót vốn trực tiếp để tài trợ những dự án hạ tầng tỷ đô như xây mới hoặc nâng cấp sân vận động St James' Park thay vì chảy vào túi chủ cũ. "
            "Động thái này diễn ra trong bối cảnh quỹ Saudi Arabia đang mạnh tay cắt giảm chi tiêu thể thao toàn cầu sau khi giải golf LIV Golf nộp đơn xin phá sản và quỹ này cũng rút sớm hợp đồng đăng cai giải quần vợt nữ WTA."
        ),
        "source": "The Guardian Sport",
        "news_source": "THE GUARDIAN SPORT",
        "credit": "BING SEARCH",
        "stat_badges": {
            "1": {"label": "THƯƠNG VỤ CHUYỂN NHƯỢNG", "value": "BÁN 25% CỔ PHẦN", "sub": "JP Morgan đứng ra tìm đối tác đầu tư"},
            "4": {"label": "THẮT CHẶT CHI TIÊU", "value": "SAU KHI LIV GOLF PHÁ SẢN", "sub": "PIF dồn vốn nâng cấp sân St James' Park"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("St James Park Newcastle United stadium exterior matchday")], "BING SEARCH", "Sân vận động St James' Park cần nguồn vốn lớn để mở rộng hoặc xây mới"),
            _slot("title", 0, [_ddgs("Newcastle United Premier League football team match")], "BING SEARCH", "Quỹ đầu tư Saudi Arabia tìm thêm cổ đông chiến lược cho Newcastle United"),
            _slot("sentence", 1, [_ddgs("JP Morgan headquarters New York finance building")], "BING SEARCH", "Ngân hàng đầu tư JP Morgan được giao phụ trách đợt phát hành cổ phần mới"),
            _slot("sentence", 2, [_ddgs("St James Park Newcastle fans stadium")], "BING SEARCH", "Sau năm năm tiếp quản, Chích chòe từng hai lần dự Champions League và vô địch Carabao Cup"),
            _slot("sentence", 3, [_ddgs("Newcastle United Eddie Howe football match")], "BING SEARCH", "Toàn bộ tiền thu về được cam kết phục vụ đầu tư hạ tầng và phát triển câu lạc bộ"),
            _slot("sentence", 4, [_ddgs("LIV Golf tournament trophy golf")], "BING SEARCH", "Saudi Arabia đang thu hẹp danh mục thể thao sau sự sụp đổ của giải đấu LIV Golf"),
        ],
    },

    # 20 (Nữ — RAHEEM STERLING NHẬN ÁN 12 THÁNG TÙ TREO VÌ LÁI XE KHI HÍT BÓNG CƯỜI)
    {
        "id": 20,
        "art_id": "art_20",
        "group": "HẬU TRƯỜNG BÓNG ĐÁ",
        "title": "Cựu tuyển thủ Anh Raheem Sterling nhận án 12 tháng tù treo vì lái xe khi dùng bóng cười",
        "summary": (
            "Ngày 25 tháng 11 tại Tòa án Basingstoke, cựu ngôi sao đội tuyển Anh Raheem Sterling đã thoát cảnh ngồi tù khi nhận bản án 12 tháng tù nhưng cho hưởng án treo trong thời gian thử thách 18 tháng. "
            "Trước đó vào sáng 28 tháng năm, cầu thủ từng bốn lần vô địch Ngoại hạng Anh bị nhân chứng phát hiện vừa hít khí cười vừa điều khiển chiếc Lamborghini Urus lạng lách nguy hiểm trên cao tốc trước khi đâm vào dải phân cách. "
            "Ngoài án tù treo, thẩm phán Kirsty Allman còn buộc cầu thủ 31 tuổi thực hiện 100 giờ lao động công ích và cấm lái xe trong vòng 24 tháng. "
            "Tòa án ghi nhận việc Sterling tự nguyện vào trung tâm cai nghiện trong 12 ngày hồi tháng sáu cùng các hoạt động thiện nguyện lâu năm là tình tiết giảm nhẹ quan trọng."
        ),
        "source": "BBC Sport / The Guardian Sport",
        "news_source": "BBC SPORT / THE GUARDIAN",
        "credit": "BBC SPORT",
        "stat_badges": {
            "1": {"label": "PHÁN QUYẾT TÒA ÁN", "value": "12 THÁNG TÙ TREO", "sub": "Thời gian thử thách 18 tháng tại Anh"},
            "3": {"label": "HÌNH PHẠT BỔ SUNG", "value": "100H CÔNG ÍCH • CẤM LÁI 24 THÁNG", "sub": "Do lái Lamborghini mất kiểm soát"},
        },
        "slots": [
            _slot("title", 0, [_url(BBC_STERLING)], "BBC SPORT", "Raheem Sterling nhận án tù treo sau vụ tai nạn giao thông nghiêm trọng hồi tháng 5"),
            _slot("title", 0, [_ddgs("Raheem Sterling England football match")], "BING SEARCH", "Cựu tuyển thủ Anh từng khoác áo Liverpool, Man City, Chelsea và Arsenal"),
            _slot("sentence", 1, [_url(BBC_STERLING)], "BBC SPORT", "Ngôi sao 31 tuổi giữ vẻ mặt lặng lẽ khi nghe tuyên án tại tòa án Basingstoke"),
            _slot("sentence", 2, [_ddgs("Raheem Sterling Chelsea football")], "BING SEARCH", "Cựu sao Ngoại hạng Anh đối mặt rắc rối pháp lý sau vụ tai nạn trên cao tốc M3"),
            _slot("sentence", 3, [_url(BBC_STERLING)], "BBC SPORT", "Sterling bị tước bằng lái hai năm và phải hoàn thành 100 giờ phục vụ cộng đồng"),
            _slot("sentence", 4, [_ddgs("Raheem Sterling MBE charity England")], "BING SEARCH", "Danh hiệu MBE và quá trình điều trị cai nghiện tự nguyện giúp cầu thủ này được giảm nhẹ"),
        ],
    },

    # 21 (Nam — KỲ THỦ XE LĂN TRIỆU PHÀN VĨ QUẬT NGÃ NHÀ VÔ ĐỊCH THẾ GIỚI MẠNH THẦN)
    {
        "id": 21,
        "art_id": "art_21",
        "group": "CỜ TƯỚNG QUỐC TẾ",
        "title": "Kỳ thủ xe lăn Triệu Phàn Vĩ quật ngã nhà vô địch thế giới Mạnh Thần tại giải Trung Quốc",
        "summary": (
            "Giải vô địch cờ tướng cá nhân Trung Quốc 2026 tại Trường Xuân chiều 25 tháng 11 tiếp tục tạo cơn sốt với màn ngược dòng đầy nghị lực của kỳ thủ khuyết tật Triệu Phàn Vĩ ở vòng 16. "
            "Chạm trán người đồng đội sừng sỏ từng vô địch thế giới năm 2023 là Mạnh Thần, Triệu Phàn Vĩ cầm hòa đối thủ suốt hai ván cờ tiêu chuẩn và hai ván cờ nhanh trước khi tung đòn quyết định thắng ở ván cờ chớp thứ năm. "
            "Chiến thắng ngoạn mục ngay ở thể thức cờ tốc độ sở trường của đối phương giúp kỳ thủ 34 tuổi đòi lại món nợ thua trận chung kết ba năm trước và hiên ngang tiến vào tứ kết. "
            "Mắc chứng loạn dưỡng cơ tiến triển khiến đôi chân bị liệt từ năm 15 tuổi và gắn bó với chiếc xe lăn, câu nói truyền cảm hứng 'Tôi không cần đôi chân để chơi cờ' của Triệu Phàn Vĩ một lần nữa làm lay động giới thể thao châu Á."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "VÒNG 16 TRUNG QUỐC", "value": "TRIỆU PHÀN VĨ THẮNG 5 VÁN", "sub": "Hạ gục nhà vô địch thế giới Mạnh Thần"},
            "4": {"label": "NGHỊ LỰC PHI THƯỜNG", "value": "KỲ VƯƠNG XE LĂN", "sub": "Ngồi xe lăn từ năm 15 tuổi, vào tứ kết"},
        },
        "slots": [
            _slot("title", 0, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_21_2.jpg"))], "BING SEARCH", "Giải vô địch cờ tướng cá nhân Trung Quốc chứng kiến màn so tài đỉnh cao"),
            _slot("title", 0, [_url(TT_TPV_2)], "TUỔI TRẺ", "Anh vượt qua nhà vô địch thế giới năm 2023 Mạnh Thần sau năm ván cân não"),
            _slot("sentence", 1, [_url(TT_TPV_3)], "TUỔI TRẺ", "Triệu Phàn Vĩ tạo nên chiến thắng giàu cảm xúc nhất vòng 16 giải Trung Quốc"),
            _slot("sentence", 2, [_url(TT_TPV_2)], "TUỔI TRẺ", "Ở ván cờ chớp quyết định, Triệu Phàn Vĩ tận dụng hoàn hảo lợi thế đi tiên"),
            _slot("sentence", 3, [_url(TT_TPV_3)], "TUỔI TRẺ", "Tài năng sinh năm 1992 khẳng định bản lĩnh ở cả ba thể thức cờ tiêu chuẩn, nhanh và chớp"),
            _slot("sentence", 4, [_ddgs("chinese chess xiangqi wooden board")], "BING SEARCH", "Nghị lực vượt qua bạo bệnh của Triệu Phàn Vĩ tiếp thêm động lực cho hàng triệu người hâm mộ"),
        ],
    },

    # 22 (Nữ — CHẤN ĐỘNG NFL: STEELERS SA THẢI AARON RODGERS SAU KHI TỐ HLV NGỦ GẬT)
    {
        "id": 22,
        "art_id": "art_22",
        "group": "BÓNG BẦU DỤC NFL",
        "title": "Chấn động NFL: Pittsburgh Steelers sa thải Aaron Rodgers vài giờ sau khi anh tố huấn luyện viên ngủ gật",
        "summary": (
            "Làng bóng bầu dục Mỹ rung chuyển ngày 25 tháng 11 khi câu lạc bộ Pittsburgh Steelers chính thức ra thông báo chấm dứt hợp đồng với ngôi sao từng bốn lần giành danh hiệu Cầu thủ xuất sắc nhất NFL là Aaron Rodgers. "
            "Quyết định cứng rắn được ban lãnh đạo Steelers đưa ra chỉ vài giờ sau khi tiền vệ sắp bước sang tuổi 43 bất ngờ xuất hiện trong chương trình của kênh ESPN để công kích dữ dội huấn luyện viên trưởng Mike McCarthy. "
            "Bức xúc vì bị đẩy lên ghế dự bị, Rodgers tố cáo ông McCarthy đã ngủ gật và ngáy to ngay trong buổi họp chiến thuật tuần trước, thậm chí hô nhầm khẩu hiệu cổ vũ đội bóng cũ Packers giữa giờ nghỉ trận đấu. "
            "Giới truyền thông Mỹ nhận định cuộc chia tay ồn ào này có thể đặt dấu chấm hết cho sự nghiệp lẫy lừng của một trong những tiền vệ vĩ đại nhất lịch sử giải đấu."
        ),
        "source": "BBC Sport / The Guardian Sport",
        "news_source": "THE GUARDIAN / BBC SPORT",
        "credit": "BBC SPORT / BING SEARCH",
        "stat_badges": {
            "1": {"label": "CHỦ NHÂN 4 MVP", "value": "AARON RODGERS BỊ SA THẢI", "sub": "Pittsburgh Steelers cắt hợp đồng ngay lập tức"},
            "3": {"label": "CÁO BUỘC GÂY SỐC", "value": "TỐ HLV NGỦ GẬT KHI HỌP", "sub": "Mâu thuẫn đỉnh điểm với Mike McCarthy"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Aaron Rodgers Steelers 2026")], "BING SEARCH", "Ngôi sao kỳ cựu Aaron Rodgers bất ngờ bị Pittsburgh Steelers thanh lý hợp đồng"),
            _slot("title", 0, [_ddgs("Aaron Rodgers Pittsburgh Steelers quarterback NFL")], "BING SEARCH", "Tiền vệ từng bốn lần giành MVP đối diện nguy cơ giải nghệ sau sự cố ồn ào"),
            _slot("sentence", 1, [_ddgs("Pittsburgh Steelers NFL stadium Acrisure")], "BING SEARCH", "Ban lãnh đạo Pittsburgh Steelers đưa ra thông báo ngắn gọn ngay trong chiều 25 tháng 11"),
            _slot("sentence", 2, [_ddgs("Aaron Rodgers quarterback interview ESPN")], "BING SEARCH", "Cuộc phỏng vấn kéo dài 34 phút trên ESPN làm bùng phát mâu thuẫn nội bộ"),
            _slot("sentence", 3, [_ddgs("Mike McCarthy NFL head coach sideline")], "BING SEARCH", "Huấn luyện viên Mike McCarthy phản bác cáo buộc và cho rằng Rodgers đã vượt giới hạn"),
            _slot("sentence", 4, [_ddgs("Aaron Rodgers NFL quarterback passing")], "BING SEARCH", "Nếu không đội bóng nào nhận hợp đồng, Rodgers sẽ trở thành cầu thủ tự do ở tuổi 43"),
        ],
    },

    # 23 (Nam — FORMULA 1: WILLIAMS BỊ PHẠT VÌ VƯỢT TRẦN NGÂN SÁCH 627000 BẢNG ANH)
    {
        "id": 23,
        "art_id": "art_23",
        "group": "ĐUA XE FORMULA 1",
        "title": "Formula 1: Đội đua Williams bị FIA phạt vì vượt trần ngân sách 627000 bảng Anh",
        "summary": (
            "Liên đoàn Ô tô Quốc tế FIA tối 25 tháng 11 công bố kết quả kiểm toán tài chính mùa giải Formula 1 năm 2025, xác nhận đội đua Williams đã vô tình vượt trần chi tiêu khoảng 627000 bảng Anh. "
            "Mức vượt chi này tương đương 0,48% so với giới hạn ngân sách 135 triệu đô la Mỹ và phát sinh từ việc Williams phân loại nhầm một số chi phí hành chính khi tái cấu trúc công ty. "
            "Theo thỏa thuận nhận lỗi với FIA, đội đua nước Anh phải nộp một khoản tiền phạt, chịu toàn bộ chi phí điều tra và bị cắt giảm 1,5% thời gian thử nghiệm hầm gió lẫn mô phỏng khí động học trong 12 tháng tới. "
            "Cùng đợt kiểm toán, đội đua Alpine cũng bị FIA phạt tiền do vi phạm thủ tục hành chính dù không chi tiêu vượt ngưỡng cho phép."
        ),
        "source": "BBC Sport / Sky Sports",
        "news_source": "SKY SPORTS / BBC SPORT",
        "credit": "BBC SPORT / SKY SPORTS",
        "stat_badges": {
            "1": {"label": "KIỂM TOÁN FIA 2025", "value": "VƯỢT TRẦN 627000 BẢNG", "sub": "Tương đương 0,48% giới hạn ngân sách"},
            "3": {"label": "ÁN PHẠT CHÍNH THỨC", "value": "PHẠT TIỀN • CẮT 1,5% HẦM GIÓ", "sub": "Alpine cũng bị phạt lỗi thủ tục"},
        },
        "slots": [
            _slot("title", 0, [_url(BBC_F1_WILLIAMS)], "BBC SPORT", "Đội đua Williams đạt thỏa thuận chấp nhận án phạt từ Liên đoàn Ô tô Quốc tế FIA"),
            _slot("title", 0, [_url(SKY_F1_VOWLES)], "SKY SPORTS", "Lãnh đội James Vowles lý giải sai sót xuất phát từ chi phí tái cấu trúc doanh nghiệp"),
            _slot("sentence", 1, [_url(BBC_F1_WILLIAMS)], "BBC SPORT", "FIA ghi nhận đội đua Anh hợp tác thiện chí và không thu lợi bất chính trên đường đua"),
            _slot("sentence", 2, [_url(SKY_F1_SAINZ)], "SKY SPORTS", "Williams đang xếp thứ chín bảng xếp hạng đội đua trước hai chặng cuối mùa 2026"),
            _slot("sentence", 3, [_url(SKY_F1_VOWLES)], "SKY SPORTS", "Việc bị cắt 1,5% thời gian thử nghiệm khí động học ảnh hưởng tới quá trình nâng cấp xe"),
            _slot("sentence", 4, [_ddgs("Alpine F1 car Formula 1 race")], "BING SEARCH", "Đội đua Alpine cũng nhận án phạt tài chính nhẹ vì thiếu sót thủ tục báo cáo"),
        ],
    },

    # 24 (Nữ — QUYỀN ANH HẠNG NẶNG: CHỐT ĐẠI CHIẾN DANIEL DUBOIS VS JOSEPH PARKER)
    {
        "id": 24,
        "art_id": "art_24",
        "group": "QUYỀN ANH THẾ GIỚI",
        "title": "Chốt đại chiến hạng nặng: Daniel Dubois bảo vệ đai WBO trước Joseph Parker tại Manchester",
        "summary": (
            "Làng quyền Anh thế giới ngày 26 tháng 11 chính thức xác nhận nhà vô địch hạng nặng WBO Daniel Dubois sẽ thượng đài bảo vệ đai trước cựu vương Joseph Parker vào ngày 30 tháng một năm 2027. "
            "Trận so găng đỉnh cao diễn ra tại nhà thi đấu Co-op Live ở Manchester, đánh dấu màn tái hẹn sau khi Dubois từng đổ bệnh rút lui sát giờ đấu với Parker hồi năm 2025. "
            "Đây là cơ hội lớn để tay đấm New Zealand Joseph Parker đòi lại chiếc đai vô địch thế giới sau khi anh vừa được gỡ bỏ án đình chỉ thi đấu hồi tháng tám. "
            "Cùng thời điểm tại Xứ Wales, hội đồng thành phố Cardiff cũng chính thức bật đèn xanh cho siêu trận đấu giữa Tyson Fury và Anthony Joshua tháng tới bất chấp những phản đối về khung giờ kết thúc lúc ba giờ sáng."
        ),
        "source": "Sky Sports / BBC Sport",
        "news_source": "SKY SPORTS / BBC SPORT",
        "credit": "SKY SPORTS",
        "stat_badges": {
            "1": {"label": "TRANH ĐAI WBO", "value": "DUBOIS VS PARKER • 30/01", "sub": "Tổ chức tại Co-op Live, Manchester"},
            "4": {"label": "TIN BÊN LỀ CARDIFF", "value": "DUYỆT TRẬN FURY VS JOSHUA", "sub": "Diễn ra tháng tới dù kết thúc lúc 3h sáng"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_BOX_DUBOIS)], "SKY SPORTS", "Daniel Dubois và Joseph Parker chính thức ấn định ngày thượng đài tranh đai WBO"),
            _slot("title", 0, [_ddgs("Daniel Dubois heavyweight boxing champion")], "BING SEARCH", "Nhà vô địch nước Anh bước vào trận bảo vệ đai thứ hai kể từ khi hạ Fabio Wardley"),
            _slot("sentence", 1, [_url(SKY_BOX_DUBOIS)], "SKY SPORTS", "Co-op Live ở Manchester hứa hẹn đón bầu không khí rực lửa vào cuối tháng giêng"),
            _slot("sentence", 2, [_ddgs("Joseph Parker boxer heavyweight ring")], "BING SEARCH", "Joseph Parker từng thắng ấn tượng trước Deontay Wilder và Trương Chí Lỗi"),
            _slot("sentence", 3, [_ddgs("Daniel Dubois boxing ring celebration")], "BING SEARCH", "Cả hai tay đấm từng hụt hẹn đối đầu vào năm 2025 nên quyết tâm cống hiến trận thư hùng"),
            _slot("sentence", 4, [_ddgs("Tyson Fury Anthony Joshua boxing face off")], "BING SEARCH", "Cardiff kỳ vọng đại chiến Fury và Joshua sẽ tạo cú hích lớn cho doanh thu địa phương"),
        ],
    },

    # 25 (Nam — CỜ VUA THẾ GIỚI 2026: GUKESH VÀ SINDAROV HÒA CHÓNG VÁNH SAU 20 NƯỚC VÁN 2)
    {
        "id": 25,
        "art_id": "art_25",
        "group": "CỜ VUA THẾ GIỚI",
        "title": "Chung kết Cờ vua Thế giới 2026: Gukesh và Sindarov hòa chóng vánh chỉ sau 20 nước ở ván hai",
        "summary": (
            "Ván đấu thứ hai trận Chung kết Cờ vua Thế giới 2026 tại Geneva tối ngày 25 tháng 11 khép lại nhanh bất ngờ khi đương kim vô địch Gukesh Dommaraju và người thách đấu Javokhir Sindarov bắt tay hòa sau vỏn vẹn 20 nước đi. "
            "Lần đầu cầm quân trắng trong trận chung kết, đại kiện tướng Ấn Độ chọn khai cuộc hệ thống London quen thuộc, nhưng kỳ thủ Uzbekistan đã chuẩn bị sẵn phương án đối phó sắc bén ngay từ nước thứ bảy. "
            "Thế trận trung cuộc nhanh chóng đóng kín khiến hai kỳ thủ trẻ đồng ý chia điểm bằng thế lặp nước ba lần sau một giờ 57 phút thi đấu, đưa tổng tỷ số trận đấu về cân bằng 1-1. "
            "Đây là một trong những ván cờ tiêu chuẩn ngắn nhất trong lịch sử các trận chung kết vô địch thế giới kể từ năm 2006."
        ),
        "source": "The Guardian Sport / FIDE",
        "news_source": "THE GUARDIAN / FIDE",
        "credit": "BING SEARCH",
        "stat_badges": {
            "1": {"label": "VÁN 2 TẠI GENEVA", "value": "HÒA SAU 20 NƯỚC • 1-1", "sub": "Kết thúc chỉ sau 1 giờ 57 phút"},
            "4": {"label": "CỘT MỐC HIẾM GẶP", "value": "NGẮN NHẤT TỪ NĂM 2006", "sub": "Hai kỳ thủ dùng thế lặp nước ba lần"},
        },
        "slots": [
            _slot("title", 0, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_1.jpg"))], "BING SEARCH", "Đương kim vô địch thế giới Gukesh Dommaraju cầm quân trắng ở ván hai tại Thụy Sĩ"),
            _slot("title", 0, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_2.jpg"))], "BING SEARCH", "Javokhir Sindarov chuẩn bị khai cuộc kỹ lưỡng để hóa giải ưu thế đi trước của Gukesh"),
            _slot("sentence", 1, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_3.jpg"))], "BING SEARCH", "Ván đấu diễn ra tại Geneva nhanh chóng đi vào thế cân bằng tuyệt đối"),
            _slot("sentence", 2, [_ddgs("Gukesh Dommaraju FIDE chess 2025")], "BING SEARCH", "Gukesh dành gần nửa giờ suy nghĩ ở nước thứ 16 nhưng không tìm được khe hở"),
            _slot("sentence", 3, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_5.jpg"))], "BING SEARCH", "Tổng tỷ số sau hai ván là 1-1 trước khi Sindarov cầm quân trắng ở ván ba"),
            _slot("sentence", 4, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_6.jpg"))], "BING SEARCH", "Trận chung kết vẫn còn dài phía trước với sự cân tài cân sức của hai tài năng trẻ"),
        ],
    },

    # 26 (100% Giọng Nữ — MỤC TIN VẮN CUỐI VIDEO: CÁC TIN THỂ THAO KHÁC)
    {
        "id": 26,
        "art_id": "art_26",
        "group": "CÁC TIN THỂ THAO KHÁC",
        "title": "Điểm nhanh các tin thể thao đáng chú ý khác",
        "voice_preset": "secondary",
        "summary": (
            "Ở các trận đấu còn lại tại lượt năm Champions League rạng sáng 26 tháng 11, Inter Milan thắng Stuttgart 2-0 nhờ công Petar Sučić và Lautaro Martínez, Atlético Madrid vượt qua Viking 2-0, trong khi Fenerbahce và Villarreal cùng giành thắng lợi tối thiểu 1-0 trên sân khách. "
            "Tại giải hạng Nhất Anh, Burnley thiết lập kỷ lục buồn với 24 trận liên tiếp không thắng trên sân nhà kéo dài 403 ngày sau trận thua Birmingham 0-2, còn Stoke City đánh bại Millwall 2-1 để nối dài chuỗi năm trận toàn thắng. "
            "Trên sàn bóng rổ Mỹ, giải NBA công bố kế hoạch đầu tư ít nhất 10 tỷ euro phát triển hệ thống nhà thi đấu tại châu Âu, đồng thời tại NBA Cup sáng nay, Philadelphia 76ers đánh bại Miami Heat 111-104 nhờ triple-double đầu tiên của LeBron James trong màu áo mới. "
            "Ở môn bóng chày MLB, ban tổ chức giải bất ngờ đệ đơn kiện Hiệp hội Cầu thủ ra tòa án liên bang nhằm bảo đảm tính pháp lý cho kịch bản đóng cửa giải đấu nếu không đạt thỏa thuận lương mới trước hạn chót ngày 1 tháng 12. "
            "Ở bộ môn snooker và cricket, huyền thoại Ronnie O'Sullivan gây thất vọng khi thua tay cơ 61 tuổi Tony Drago 3-5, còn truyền thông quốc tế đã tìm ra danh tính người hùng bắt gọn bóng cricket bằng một tay khi ngồi sau xe máy tại Pakistan là Mehran Khan. "
            "Khép lại bản tin, tại U17 World Cup bảng B tối 25 tháng 11, U17 Hàn Quốc thắng Ecuador 3-2 để giữ ngôi đầu với chín điểm tuyệt đối và cùng Uganda giành vé đi tiếp, còn tại Đại hội Thể thao toàn quốc ở Thành phố Hồ Chí Minh, sư thầy 32 tuổi Đặng Thanh Tiến mang pháp danh Thích Toàn Tĩnh gây xúc động khi giành huy chương bạc nội dung Phong Hoa Đao môn võ cổ truyền."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / BBC Sport / Sky Sports / The Guardian",
        "news_source": "ĐIỂM ĐỌC TỔNG HỢP",
        "credit": "THANH NIÊN / TUỔI TRẺ / SKY SPORTS",
        "stat_badges": {
            "1": {"label": "CHAMPIONS LEAGUE", "value": "INTER 2-0 • ATLETICO 2-0", "sub": "Fenerbahce & Villarreal thắng 1-0"},
            "3": {"label": "BÓNG RỔ NBA", "value": "ĐẦU TƯ 10 TỶ EURO CHÂU ÂU", "sub": "76ers thắng Heat 111-104"},
            "6": {"label": "U17 & ĐẠI HỘI 2026", "value": "HÀN QUỐC NHẤT BẢNG B", "sub": "Sư thầy Thích Toàn Tĩnh giành HCB võ cổ truyền"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Inter Milan Lautaro Martinez Champions League")], "BING SEARCH", "Inter Milan và Atlético Madrid đồng loạt thắng 2-0 ở lượt năm Champions League"),
            _slot("title", 0, [_url(SKY_STOKE)], "SKY SPORTS", "Stoke City nối dài mạch năm trận thắng liên tiếp tại giải hạng Nhất Anh"),
            _slot("title", 0, [_url(TT_SUTHAY)], "TUỔI TRẺ", "Võ sĩ đặc biệt Đặng Thanh Tiến tỏa sáng tại Đại hội Thể thao toàn quốc 2026"),
            # Câu 1: Inter, Atletico, Fenerbahce, Villarreal
            _slot("sentence", 1, [_ddgs("Lautaro Martinez Inter Milan goal celebration")], "BING SEARCH", "Lautaro Martínez vào sân ghi bàn giúp Inter Milan đánh bại Stuttgart 2-0"),
            _slot("sentence", 1, [_ddgs("Atletico Madrid football match celebration")], "BING SEARCH", "Atlético Madrid có trọn ba điểm trước đại diện Na Uy Viking FK"),
            # Câu 2: Burnley & Stoke City
            _slot("sentence", 2, [_url(SKY_BURNLEY)], "SKY SPORTS", "Birmingham City đẩy Burnley vào kỷ lục buồn 24 trận không thắng tại Turf Moor"),
            _slot("sentence", 2, [_url(SKY_STOKE)], "SKY SPORTS", "Cú đúp của George Hirst đưa Stoke City trở lại nhóm thăng hạng trực tiếp"),
            # Câu 3: NBA 10 tỷ euro & 76ers 111-104 Heat
            _slot("sentence", 3, [_ddgs("NBA basketball arena Europe London Paris")], "BING SEARCH", "NBA đẩy mạnh kế hoạch thành lập giải đấu nhà nghề tại lục địa già"),
            _slot("sentence", 3, [_ddgs("LeBron James Philadelphia 76ers basketball")], "BING SEARCH", "LeBron James lập triple-double giúp Philadelphia 76ers đánh bại Miami Heat"),
            # Câu 4: MLB kiện MLBPA
            _slot("sentence", 4, [_ddgs("MLB Major League Baseball stadium field")], "BING SEARCH", "Bóng chày nhà nghề Mỹ đối mặt nguy cơ đình công trước hạn chót ngày 1 tháng 12"),
            # Câu 5: Ronnie O'Sullivan & Mehran Khan
            _slot("sentence", 5, [_ddgs("Ronnie O Sullivan snooker tournament")], "BING SEARCH", "Ronnie O'Sullivan nhận thất bại bất ngờ trước tay cơ lão tướng Tony Drago"),
            _slot("sentence", 5, [_ddgs("cricket match stadium catch Pakistan")], "BING SEARCH", "Khoảnh khắc bắt bóng trên xe máy tại Pakistan thu hút hàng triệu lượt xem"),
            # Câu 6: U17 Hàn Quốc, Uganda & Sư thầy võ cổ truyền
            _slot("sentence", 6, [_url(TN_U17_KOR)], "THANH NIÊN", "U17 Hàn Quốc thắng kịch tính U17 Ecuador 3-2 để đứng đầu bảng B"),
            _slot("sentence", 6, [_ddgs("Uganda football national team celebration")], "BING SEARCH", "U17 Uganda thắng đậm 6-0 để trở thành đội thứ 12 vào vòng 32 đội"),
            _slot("sentence", 6, [_url(TT_SUTHAY)], "TUỔI TRẺ", "Nhà sư 32 tuổi Đặng Thanh Tiến giành huy chương bạc nội dung Phong Hoa Đao"),
        ],
    },
]
