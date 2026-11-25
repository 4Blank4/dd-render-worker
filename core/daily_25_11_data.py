# -*- coding: utf-8 -*-
"""
daily_25_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 25.11.2026
(Tổng hợp song hành báo Việt Nam & Thế Giới: 12:00 ngày 24.11 đến 08:20 ngày 25.11.2026).
Tuân thủ quy chuẩn Anti-Bundling (1 sự kiện / 1 vấn đề = 1 tin, 3–5 câu súc tích):
  - Intro (00): Song giọng Nữ & Nam, hide_title=True
  - 23 bản tin chính độc lập (01–23): mỗi tin 1 vấn đề rõ ràng, luân phiên Nam/Nữ
  - Mục 24 (CÁC TIN THỂ THAO KHÁC): 100% Giọng Nữ điểm nhanh tin bên lề
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


# ── URL ảnh báo chí sạch gốc 24–25.11.2026 (Việt Nam & Thế Giới) ──

# 1. CAHN 3-1 Vissel Kobe & Dư chấn & Bóng đá Thái Lan
TN_CAHN_1 = "https://images2.thanhnien.vn/zoom/1200_630/528068263637045248/2026/11/25/1k86va90v7cr2qo-17955306315261374739076-216-0-1466-2000-crop-17955665353881066607144.jpeg"
TN_CAHN_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/1k86vadtr7cr2qo-1795566108233101663182.jpeg"
TN_CAHN_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/cahn-vissel-kobe-2-17955249070612003792383.jpg"
TN_CAHN_4 = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/cahn-vissel-kobe-1-17955249070011090018068.jpg"
TN_CAHN_5 = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/cahn-vissel-kobe-3-17955278454542070901397.jpg"
TN_CAHN_6 = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/cahn-vissel-kobe-4-17955278454911887574274.jpg"
VNE_CAHN_1 = "https://i1-thethao.vnecdn.net/2026/11/24/16_1795529311-1795530684.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=c7qpYC74lDepP8YRueVBaw"
TT_CAHN_CELEB = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/17955273298298973244394868833818g14038781258001894144450113acb11361b73b351c889757b74-179552750698210924788.jpg"
TT_FILIP_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/base64-17955346812152079265625.jpeg"
TT_FILIP_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/base64-1795534681244445342545.jpeg"
TT_FILIP_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/base64-17955346812531721744580.jpeg"
TT_FILIP_4 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/base64-17955346812761415398753.jpeg"
TT_POLKING = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/polking-17955325937271066401121.jpg"
TT_SKIBBE = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/skibbe-17955320706861069792545.jpg"
TT_OSAKO_1 = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/24/base64-17955382380671684297533.jpeg"
TT_OSAKO_2 = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/24/base64-17955382380981164076171.jpeg"
TT_OSAKO_3 = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/24/base64-1795538238115606252482.jpeg"
VNE_BURIRAM_1 = "https://i1-thethao.vnecdn.net/2026/11/24/tha-i-lan-1795537262-2125-1795537442.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=oQfLf9t8WAFfUf4t23chrQ"
TT_BURIRAM_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/edit-buriram-fc-2-1795530846556157258517.jpeg"
TT_BURIRAM_CH = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/buriram-nevin-17951415538021682963902.jpg"

# 2. U17 Việt Nam, U17 World Cup & Malaysia
TN_U17_LUC = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/92829925914648034791768631245591373098348425n-1795543430849434439852.jpg"
TN_U17_KOR = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/16df9bad-514e-4ae9-896a-94df731939b0png-1795542188424527939406.jpg"
TN_U17_ESP = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/831a78cb-569e-4b73-8ad0-68bc231b4f6apng-1795542239941278436296.jpg"
TN_U17_JPN = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/5c7fafc7-ddca-42ca-8ab4-aabec3522f78png-1795528532401631857942.jpg"
TN_U17_VEN = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/9cb391de-6009-4ef9-97a9-014100f2f959png-17955319232271656085626.jpg"
TN_U17_DEP = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/1-1795523494127184052414.jpg"
TN_U17_DUONG = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/17955289011283343106628512696865334310662851269686523a5540c25eb7c91b37045937931d314-1795529501011113505849.jpg"
TN_U17_ROL = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/179552890121033431066285126968653343106628512696865561ee25bc64798e857871d471c068dde-1795529500942177364959.jpg"
TN_U17_TAP = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/179552890117633431066285126968653343106628512696865083422b83681eca0a3e229de48350235-1795529500873171682741.jpg"
TN_U17_LUC_10 = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/92370468014875575999956553220487339033369127n-1-17954578889691751040385.jpg"
TN_U17_MALI_LUC = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/6-1795489252368664267347.jpg"
TT_U17_DUONG = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/van-duong-tra-loi-phong-van-17955622257861682550681.jpg"
TT_U17_ROL_TAP = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/hlv-cristaino-roland-tren-san-tap-1795562443391944355949.jpg"
TT_U17_FVS = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/dkawky8n-p5tgxmljls4iuaya9yxzjpahlhl09lnhgtdzcw6zww24oy5baxo1hmdhnixccfd1b5xwm6atwfgldyothwvxvmbufnnomshyyzvy5-u2h2tu3dakiwqtolokrork8zxj6vipm-17955061307581427599962.jpg"
DT_U17_VFF = "https://cdnphoto.dantri.com.vn/ONVHahlKEHwz2SHx3cNpk1B9xUg=/thumb_w/1020/2026/11/24/img9483-2048x1152-1-1795520893485.jpeg"
DT_MAL_1 = "https://cdnphoto.dantri.com.vn/UdnAoXuMru68BpR3gGa6c9G_Dbk=/thumb_w/1020/2026/11/24/bojan-hodak-1795531298531.jpg"
DT_MAL_2 = "https://cdnphoto.dantri.com.vn/0dMqg8h_BDuJFEkBqvQ15qOGmZI=/thumb_w/1020/2026/11/24/bojan-hodak-2-1795531723687.jpg"

# 3. Đại hội Thể thao toàn quốc 2026
TN_AV_NGUA = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/tnw-1795525097510495148892215585366649514889221558536667c679fe9784a982c6641dd6ac8320f15-17955662243761715062102.jpg"
TN_AV_HCV = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/17953326087804663956325243268460466395632524326846029db3ffd844cfc5e193a9d98ff5699e4-1795522121946941325617.jpg"
TN_AV_SMILE = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/17955227214728319004782376440998g6772048047385145902a79ad5d0efa612caca7059574593dccc-1795522821946571066068.jpg"
TT_AV_OLD = "https://cdn2.tuoitre.vn/thumb_w/730/2021/11/16/anh-vien-doat-hcv-100-ngua-43-1637063475054991186017.jpg"
TN_THUY_HIEN = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/tnw-2-1795530972304657594740.jpg"
TT_SHOOT_VINH = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/1795527224721206641814440293842762258538871957165927535cd5181a180abe3dd56db333cfec9-17955277258421539805795.jpg"
TT_SHOOT_DUNG = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/179552722418120664181444029384276225853887195716592515670bf91922678c3c3bf656c4082b1-17955277577381786710605.jpg"
TT_SHOOT_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/baphunudeokinhthethao-179552768555882733788.png"
TT_SHOOT_HUY = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/179552722383520664181444029384276225853887195716592d51bffc853181b5c340cfbbdbffa6a26-17955275432581618940041.jpg"
TT_BAD_LINH = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/nguyen-thuy-linh-cau-long-dai-hoi-the-thao-toan-quoc-1795533186026330502709.jpeg"
TT_BAD_TRANG = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/vu-thi-trang-cau-long-dai-hoi-cau-long-toan-quoc--1795533186040477749143.jpeg"
TT_BAD_CROWD = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/cau-long-dai-hoi-the-thao-toan-quoc-3-179554983343646356069.jpg"
DT_BAD_ARENA = "https://cdnphoto.dantri.com.vn/sQH_Q0E53rLrKG8lrGg2AOLMdqI=/zoom/1200_630/2026/11/25/banket-caulong-dhtttq2026namanh0h1a0589-cropped-1795562704888.jpg"
TN_BILL_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/17955141515636144854729594737154g5150099017876529614d61959df29dfd196f5f235781220918-17955170931401073189270.jpg"
TN_BILL_YS = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/ndys-17955175530201673340354.jpg"
VNE_CYCLE_1 = "https://iv1.vnecdn.net/thethao/images/web/2026/11/24/cua-ro-khong-chiu-can-dich-o-giai-xe-dap-dai-hoi-the-thao-to-1795504014.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=9c3XhOTDRyxgc-O3hAgEjA"
TT_FUTSAL_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/futsal-tphcm-1795527457675302715191.jpg"
TT_ATH_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/san-thong-nhat-dien-kinh-dai-hoi-the-thao-toan-quoc-1795515002799995650391.jpg"
TT_ATH_OANH = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2025/12/16/nguyen-thi-oanh-sea-games-33-dien-kinh-2-17658857588191942388160.jpg"
TN_VO_CT = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/17954833408553390983560814719843390983560814719843d92d599fe42338c48346150c03058fa-1795498544022504086543.jpg"
TT_GHE_NGO = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/img8583-1795514435083148504187.jpeg"

# 4. Champions League & Bóng đá Thế giới
VNE_REAL_1 = "https://i1-thethao.vnecdn.net/2026/11/25/Real-4683-1795557288.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=rWtvpl-7wycfSIxWxQdDGQ"
VNE_REAL_BEL = "https://i1-thethao.vnecdn.net/2026/11/25/Bellingham-6465-1795559099.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=pMNKBVx5kurvUEvE1yysSg"
VNE_REAL_MBA = "https://i1-thethao.vnecdn.net/2026/11/25/Mbappe-8010-1795559100.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=9DVOtoY7LpCp1DOwYIXHAA"
VNE_REAL_VIN = "https://i1-thethao.vnecdn.net/2026/11/25/Vinicius-2556-1795559100.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Q8tBT7MeXIrzmT91ElEmwA"
DT_REAL_PERI = "https://cdnphoto.dantri.com.vn/mvcx9Vbs87KDL0HjXhbFobM8nVw=/thumb_w/1020/2026/11/25/real2-1795561087283.webp"
DT_REAL_TEAM = "https://cdnphoto.dantri.com.vn/5HrzW8oPU-CGLhsFDBagitiCeSk=/thumb_w/1020/2026/11/25/real1-1795561086774.jpg"

SKY_CITY_CHERKI = "https://e0.365dm.com/26/11/1600x900/skysports-rayan-cherki-man-city_7415764.jpg?20261124222209"
SKY_CITY_KDB = "https://e0.365dm.com/26/11/1600x900/skysports-kevin-de-bruyne-man-city_7415656.jpg?20261124210427"
SKY_CITY_HOJ = "https://e0.365dm.com/26/11/1600x900/skysports-rasmus-hojlund-scott-mctominay_7415698.jpg?20261124214234"
SKY_CITY_HAAL = "https://e0.365dm.com/26/11/1600x900/skysports-haaland-manchester-city_7415835.jpg?20261124230423"
VNE_CITY_BANNER = "https://i1-thethao.vnecdn.net/2026/11/25/A-nh-ma-n-hi-nh-2026-11-25-lu-4844-4733-1795562811.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=fkIoGRo5WgHLEL_8GqhHtg"
VNE_CITY_KDB = "https://i1-thethao.vnecdn.net/2026/11/25/bruyne-7951-1795562811.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=hTi9RkHsGMdp31GHdk51Gg"

SKY_ARS_BVB = "https://e0.365dm.com/26/11/1600x900/skysports-arsenal-borussia-dortmund_7415724.jpg?20261124215641"
SKY_ARS_GYO = "https://e0.365dm.com/26/11/1600x900/skysports-arsenal-bvb_7415620.jpg?20261124201939"
BBC_ARS_GYO = "https://ichef.bbci.co.uk/ace/standard/1024/cpsprodpb/f58f/live/d9bad6f0-e859-11f1-9b85-e50d1e9de678.jpg"
VNE_ARS_RICE = "https://i1-thethao.vnecdn.net/2026/11/25/A-nh-ma-n-hi-nh-2026-11-25-lu-7738-4183-1795560179.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=aJGKZw4QaxNqa_3p22Cl_Q"

SKY_VILLA_GALA = "https://e0.365dm.com/26/11/1600x900/skysports-galatasaray-deniz-gul_7415608.jpg?20261124194142"
SKY_VILLA_MAAT = "https://e0.365dm.com/26/11/1600x900/skysports-ian-maatsen-aston-villa_7415552.jpg?20261124182322"

TN_RONALDO_987 = "https://images2.thanhnien.vn/528068263637045248/2026/11/25/ronaldo-179556810175464573423.jpg"
VNE_RONALDO_REF = "https://i1-thethao.vnecdn.net/2026/11/25/ro-1795559051-9612-1795559072.png?w=1200&h=675&q=100&dpr=1&fit=crop&s=unGtFkT5Ap29Yv6fNAPmUQ"
VNE_RONALDO_PEN = "https://iv1.vnecdn.net/thethao/images/web/2026/11/25/ronaldo-ghi-ban-phat-den-1795554720.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=dnhU5Egi-6RkDEMSl2Eqyw"
TN_MESSI_MLS = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/messi-17953100026131801351791.jpg"

VNE_SEN_MANE = "https://i1-thethao.vnecdn.net/2026/11/25/senegal-1262-1795539849.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=4T30rDIX0Xz_oX2rwsLaPw"
VNE_SEN_DIAZ = "https://i1-thethao.vnecdn.net/2026/11/25/Diaz-5317-1795539850.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=HeTfGFP8oBQrX15g7FIHeQ"
VNE_SEN_MOR = "https://i1-thethao.vnecdn.net/2026/11/25/morocco-1795539397-6214-1795539850.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Lvm2IeP-u5R1J-b5DWS6gg"
TT_SEN_CAS = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/jciuk2cacqt1d7sdrqhoth-v8dswb8gvwtkfjdelyf29pesclpdkc-zzohmf3timlt-pu8p3gsmzdytzelnyeao8hyftp3lottrjt9qybwtt63socobelcqlnxawfkscqgb2gwv252sgz0-17955355647491353801009.jpg"
TT_SEN_FIGHT = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/r16024081296x72916-9-1795535513600699478561.jpg"

VNE_YORO_1 = "https://i1-thethao.vnecdn.net/2026/11/24/Yoro-7398-1795538326.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=tcxZHJrPJNdcXKaEy3vMvg"
SKY_POCH_1 = "https://e0.365dm.com/26/11/1600x900/skysports-mauricio-pochettino_7415728.jpg?20261124215803"
SKY_POCH_2 = "https://e0.365dm.com/26/11/1600x900/skysports-poch-man-uited_7415789.jpg?20261124223850"
SKY_YORO_FOUL = "https://e0.365dm.com/26/11/1600x900/skysports-leny-yoro-alexander-isak_7413680.jpg?20261122164441"
DT_POCH_1 = "https://cdnphoto.dantri.com.vn/uFF9MHdQVee1qUiavrkXGzLtxds=/thumb_w/1020/2026/11/24/pochettino-2-1795534207432.jpg"
DT_POCH_2 = "https://cdnphoto.dantri.com.vn/0mLHGBAsip7vy4FPxDAQDso0O5g=/thumb_w/1020/2026/11/24/maguire-1795534024426.jpg"

# 5. Thể thao Thế giới đa môn & Tin bên lề
TT_QUACH_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/edit-quach-dinh-nam-2-1795518675700454517436.png"
TT_QUACH_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/quach-dinh-nam-1-17955189351581093119458.jpg"
BBC_SOORYA_1 = "https://ichef.bbci.co.uk/ace/standard/2048/cpsprodpb/f124/live/9f6b8b40-e802-11f1-95bb-3f37d3e026b0.jpg"
BBC_SOORYA_2 = "https://ichef.bbci.co.uk/ace/standard/3840/cpsprodpb/2c44/live/713ea650-63f3-11f1-abe1-f36e5ae3bba8.jpg"
BBC_INF_JET = "https://ichef.bbci.co.uk/ace/standard/1024/cpsprodpb/8a18/live/c4779660-e5bc-11f1-a188-ff49e70cc466.jpg"
SKY_MCILROY = "https://e0.365dm.com/26/08/1600x900/skysports-rory-mcilroy-golf_7333094.jpg?20260827203403"
SKY_RUGBY_SHEEHAN = "https://e0.365dm.com/26/11/1600x900/skysports-dan-sheehan-ireland_7411383.jpg?20261120124340"
TT_SPEED_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/edit-edit-ishowspeed-bolt-1-1795503944945696509287.jpeg"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 25.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 25 tháng 11 năm 2026, cập nhật những diễn biến nổi bật nhất tại Việt Nam và trên toàn thế giới. "
        "Ở đấu trường châu lục, câu lạc bộ Công an Hà Nội tạo địa chấn khi đánh bại đội đầu bảng Vissel Kobe 3-1 trên sân Hàng Đẫy, trong khi U17 Việt Nam bất ngờ thăng hạng trong nhóm các đội đứng thứ ba tại U17 World Cup 2026. "
        "Tại Đại hội Thể thao toàn quốc, Nguyễn Thị Ánh Viên lập cú đúp huy chương vàng kèm kỷ lục sau tám năm, Nguyễn Thúy Hiền nâng thành tích lên sáu ngôi vô địch, còn xạ thủ 37 tuổi Nguyễn Thùy Dung gây bất ngờ khi vượt qua Á quân thế giới Trịnh Thu Vinh. "
        "Trên sân cỏ châu Âu, Real Madrid ngược dòng hủy diệt PSV 5-1, Manchester City hòa nghẹt thở Napoli 2-2 ngày tri ân De Bruyne, Tòa án Thể thao trả lại ngôi vương châu Phi cho Senegal cùng nhiều tin tức thể thao đáng chú ý khác ngay sau đây."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí / BBC Sport / Sky Sports / The Guardian",
    "news_source": "VIỆT NAM & THẾ GIỚI",
    "credit": "ĐIỂM ĐỌC TỔNG HỢP",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 25 tháng 11 năm 2026, cập nhật những diễn biến nổi bật nhất tại Việt Nam và trên toàn thế giới.",
        },
        {
            "voice_preset": "primary",
            "text": "Ở đấu trường châu lục, câu lạc bộ Công an Hà Nội tạo địa chấn khi đánh bại đội đầu bảng Vissel Kobe 3-1 trên sân Hàng Đẫy, trong khi U17 Việt Nam bất ngờ thăng hạng trong nhóm các đội đứng thứ ba tại U17 World Cup 2026.",
        },
        {
            "voice_preset": "secondary",
            "text": "Tại Đại hội Thể thao toàn quốc, Nguyễn Thị Ánh Viên lập cú đúp huy chương vàng kèm kỷ lục sau tám năm, Nguyễn Thúy Hiền nâng thành tích lên sáu ngôi vô địch, còn xạ thủ 37 tuổi Nguyễn Thùy Dung gây bất ngờ khi vượt qua Á quân thế giới Trịnh Thu Vinh.",
        },
        {
            "voice_preset": "primary",
            "text": "Trên sân cỏ châu Âu, Real Madrid ngược dòng hủy diệt PSV 5-1, Manchester City hòa nghẹt thở Napoli 2-2 ngày tri ân De Bruyne, Tòa án Thể thao trả lại ngôi vương châu Phi cho Senegal cùng nhiều tin tức thể thao đáng chú ý khác ngay sau đây.",
        },
    ],
    "stat_badges": {
        "1": {"label": "BẢN TIN NGÀY", "value": "25.11.2026", "sub": "Toàn cảnh Việt Nam & Thế giới"},
        "2": {"label": "CÚP C1 CHÂU Á", "value": "CAHN 3-1 KOBE", "sub": "Thắng lợi lịch sử trước đại diện Nhật Bản"},
        "4": {"label": "CHAMPIONS LEAGUE", "value": "REAL MADRID 5-1", "sub": "Mbappé lập cú đúp • Man City 2-2 Napoli"},
    },
    "slots": [
        # Câu 1 (4 ảnh)
        _slot("sentence", 1, [_url(VNE_CAHN_1)], "VNEXPRESS", "Các cầu thủ Công an Hà Nội ăn mừng chiến thắng lịch sử trước Vissel Kobe trên sân Hàng Đẫy"),
        _slot("sentence", 1, [_url(TN_AV_SMILE)], "THANH NIÊN", "Kình ngư Nguyễn Thị Ánh Viên rạng rỡ sau tấm HCV cá nhân tại Đại hội Thể thao toàn quốc"),
        _slot("sentence", 1, [_url(VNE_REAL_1)], "VNEXPRESS / GETTY", "Jude Bellingham và Kylian Mbappé cùng tỏa sáng trong đại thắng 5-1 của Real Madrid"),
        _slot("sentence", 1, [_url(VNE_SEN_MANE)], "VNEXPRESS / REUTERS", "Senegal chính thức được Tòa án Trọng tài Thể thao khôi phục ngôi vô địch châu Phi"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(TN_CAHN_5)], "THANH NIÊN", "Brayan Perea lập cú đúp giúp Công an Hà Nội quật ngã đội bóng dẫn đầu bảng Nhật Bản"),
        _slot("sentence", 2, [_url(TT_CAHN_CELEB)], "TUỔI TRẺ / MINH ĐỖ", "Tập thể Công an Hà Nội vỡ òa sau ba điểm quý giá tại AFC Champions League Elite"),
        _slot("sentence", 2, [_url(TN_U17_LUC)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực và U17 Việt Nam tăng lên hạng bảy nhóm đội đứng thứ ba World Cup"),
        _slot("sentence", 2, [_url(TN_U17_DUONG)], "THANH NIÊN / VFF", "Tiền đạo Nguyễn Văn Dương cùng đồng đội quyết tâm đánh bại U17 Mali ở lượt cuối"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url(TN_AV_NGUA)], "THANH NIÊN", "Ánh Viên phá kỷ lục 100 mét ngửa nữ tại Đại hội sau tám năm chờ đợi"),
        _slot("sentence", 3, [_url(TN_THUY_HIEN)], "THANH NIÊN", "Nguyễn Thúy Hiền nâng thành tích lên sáu HCV kèm sáu kỷ lục đại hội chỉ sau vài ngày"),
        _slot("sentence", 3, [_url(TT_SHOOT_DUNG)], "TUỔI TRẺ / THANH ĐỊNH", "Xạ thủ kỳ cựu Nguyễn Thùy Dung gây sốc khi đánh bại đàn em giành HCV súng ngắn"),
        _slot("sentence", 3, [_url(TT_BAD_LINH)], "TUỔI TRẺ / ĐỨC KHUÊ", "Nguyễn Thùy Linh sẵn sàng đại chiến Vũ Thị Trang ở chung kết cầu lông đơn nữ"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_url(VNE_REAL_BEL)], "VNEXPRESS / GETTY", "Bellingham ghi bàn thắng đẳng cấp sau khi vào sân từ đầu hiệp hai trước PSV"),
        _slot("sentence", 4, [_url(SKY_CITY_KDB)], "SKY SPORTS", "Kevin De Bruyne đối đầu đội bóng cũ Man City trong đêm CĐV Etihad tri ân King Kev"),
        _slot("sentence", 4, [_url(SKY_ARS_BVB)], "SKY SPORTS", "Arsenal hòa Dortmund 1-1 và đứt mạch 12 trận thắng sân nhà tại Champions League"),
        _slot("sentence", 4, [_url(TN_RONALDO_987)], "THANH NIÊN", "Cristiano Ronaldo ghi bàn thứ 987 nhưng gây tranh cãi với cử chỉ nhại trọng tài"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — CAHN 3-1 VISSEL KOBE: DIỄN BIẾN TRẬN ĐẤU)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "AFC CHAMPIONS LEAGUE ELITE",
        "title": "Công an Hà Nội quật ngã đội đầu bảng Vissel Kobe 3-1, mở toang cửa vào vòng 16 đội",
        "summary": (
            "Tối ngày 24 tháng 11 tại sân vận động Hàng Đẫy, câu lạc bộ Công an Hà Nội đã tạo nên cơn địa chấn khi đánh bại đội đầu bảng Vissel Kobe của Nhật Bản với tỷ số 3-1 ở lượt năm AFC Champions League Elite. "
            "Dù tiền đạo Alan sút hỏng phạt đền ở phút thứ 11 và thủ thành Nguyễn Filip chấn thương phải rời sân nhường chỗ cho thủ môn trẻ Vũ Thành Vinh từ phút 27, đại diện Việt Nam vẫn kiểm soát tốt thế trận. "
            "Phút 45, Alan lập công chuộc tội với đường chọc khe để Stefan Mauk dứt điểm góc gần mở tỷ số, trước khi Brayan Perea đánh đầu bồi nhân đôi cách biệt ở phút 49. "
            "Sau tình huống Thành Vinh chuyền bóng lỗi giúp Erik rút ngắn tỷ số phút 53, chính Perea phá bẫy việt vị nâng tỷ số lên 3-1 ở phút 57, mang về chiến thắng đầu tiên trong lịch sử câu lạc bộ trước một đại diện J1 League để vươn lên hạng 10 với bảy điểm."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "ĐỊA CHẤN HÀNG ĐẪY", "value": "CAHN 3-1 KOBE", "sub": "Thắng trận đầu tiên trước CLB J1 League"},
            "3": {"label": "BÙNG NỔ HIỆP 2", "value": "MAUK 45' • PEREA 49', 57'", "sub": "Quật ngã đội bóng toàn thắng trước đó"},
            "4": {"label": "CỤC DIỆN BẢNG ĐẤU", "value": "7 ĐIỂM • HẠNG 10", "sub": "Bằng điểm đội hạng 8, rộng cửa đi tiếp"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_CAHN_1)], "THANH NIÊN", "Các cầu thủ Công an Hà Nội thi đấu bùng nổ trước Vissel Kobe tối 24 tháng 11"),
            _slot("title", 0, [_url(TT_CAHN_CELEB)], "TUỔI TRẺ / MINH ĐỖ", "Niềm vui vỡ òa của Công an Hà Nội sau chiến thắng lịch sử tại Hàng Đẫy"),
            _slot("sentence", 1, [_url(VNE_CAHN_1)], "VNEXPRESS", "Công an Hà Nội khiến đội đầu bảng Vissel Kobe nhận thất bại đầu tiên ở Cúp C1 châu Á"),
            _slot("sentence", 2, [_url(TN_CAHN_4)], "THANH NIÊN", "Alan đá hỏng phạt đền đầu trận nhưng kịp sửa sai bằng pha kiến tạo đẳng cấp"),
            _slot("sentence", 2, [_url(TT_FILIP_1)], "TUỔI TRẺ / MINH ĐỖ", "Thủ môn Nguyễn Filip dính chấn thương sau pha truy cản dũng cảm ở hiệp một"),
            _slot("sentence", 2, [_url(TT_FILIP_2)], "TUỔI TRẺ / MINH ĐỖ", "Thủ thành trẻ Vũ Thành Vinh được tung vào sân thay Nguyễn Filip từ phút 27"),
            _slot("sentence", 3, [_url(TN_CAHN_3)], "THANH NIÊN", "Stefan Mauk và đồng đội phá vỡ thế bế tắc ngay trước khi hiệp một khép lại"),
            _slot("sentence", 4, [_url(TN_CAHN_5)], "THANH NIÊN", "Brayan Perea lập cú đúp bàn thắng dập tắt hy vọng lội ngược dòng của đội khách Nhật Bản"),
            _slot("sentence", 4, [_url(TT_FILIP_4)], "TUỔI TRẺ / MINH ĐỖ", "Chiến thắng 3-1 mở ra cơ hội lớn giúp đại diện Việt Nam cạnh tranh vé vòng 16 đội"),
        ],
    },

    # 02 (Nữ — DƯ CHẤN CAHN: POLKING, SKIBBE & YUYA OSAKO)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "AFC CHAMPIONS LEAGUE ELITE",
        "title": "Huấn luyện viên Polking nể phục học trò, tiền đạo đẳng cấp World Cup Yuya Osako mờ nhạt",
        "summary": (
            "Sau trận thua đầu tiên tại giải đấu, huấn luyện viên Michael Skibbe của Vissel Kobe thẳng thắn thừa nhận Công an Hà Nội đã chơi bóng sáng tạo, giàu năng lượng và xứng đáng giành trọn ba điểm. "
            "Phía bên kia chiến tuyến, huấn luyện viên Mano Polking bày tỏ niềm tự hào khi học trò vượt qua áp lực lịch thi đấu dày đặc để đánh bại cựu thuyền trưởng Borussia Dortmund. "
            "Tâm điểm thất vọng của đội bóng Nhật Bản dồn vào tiền đạo từng dự hai kỳ World Cup là Yuya Osako, người được tung vào sân đầu hiệp hai nhằm xoay chuyển cục diện. "
            "Suốt hơn 45 phút góp mặt, chân sút 36 tuổi hoàn toàn bị hàng thủ đội chủ nhà phong tỏa, chỉ tung ra đúng một cú sút chệch khung thành và cúi đầu rời sân trong sự bất lực."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "TUỔI TRẺ / MINH ĐỖ",
        "stat_badges": {
            "1": {"label": "HLV VISSEL KOBE", "value": "KHEN CAHN SÁNG TẠO", "sub": "Michael Skibbe thừa nhận thua tâm phục"},
            "4": {"label": "SAO NHẬT BẢN BẤT LỰC", "value": "YUYA OSAKO • 1 CÚ SÚT", "sub": "Mờ nhạt toàn tập trước hàng thủ CAHN"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_POLKING)], "TUỔI TRẺ / MINH ĐỖ", "Huấn luyện viên Mano Polking tự hào sau chiến thắng vang dội trước Vissel Kobe"),
            _slot("title", 0, [_url(TT_OSAKO_1)], "TUỔI TRẺ", "Cựu tuyển thủ Nhật Bản Yuya Osako không thể tạo khác biệt tại sân Hàng Đẫy"),
            _slot("sentence", 1, [_url(TT_SKIBBE)], "TUỔI TRẺ / MINH ĐỖ", "Huấn luyện viên Michael Skibbe đánh giá rất cao lối chơi chủ động của Công an Hà Nội"),
            _slot("sentence", 2, [_url(TT_POLKING)], "TUỔI TRẺ / MINH ĐỖ", "Chiến thuật hợp lý của ông Polking giúp đại diện Việt Nam vượt qua thử thách lớn"),
            _slot("sentence", 3, [_url(TT_OSAKO_2)], "TUỔI TRẺ", "Ngôi sao từng thi đấu nhiều năm tại Bundesliga thường xuyên rơi vào cảnh đói bóng"),
            _slot("sentence", 4, [_url(TT_OSAKO_3)], "TUỔI TRẺ", "Yuya Osako cúi đầu rời sân sau thất bại tâm phục khẩu phục 1-3"),
        ],
    },

    # 03 (Nam — BÓNG ĐÁ THÁI LAN THẤT VỌNG Ở CÚP C1 CHÂU Á)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "BÓNG ĐÁ ĐÔNG NAM Á",
        "title": "Dùng đội hình 11 ngoại binh vẫn thua, báo chí Thái Lan thất vọng vì bị Công an Hà Nội bỏ xa",
        "summary": (
            "Trái ngược hoàn toàn với chiến thắng vang dội của Công an Hà Nội, các câu lạc bộ Thái Lan vừa trải qua một đêm đáng quên ở lượt năm AFC Champions League Elite. "
            "Trên sân khách tại Trung Quốc tối 24 tháng 11, đương kim vô địch Thai League là Buriram United gây xôn xao khi tung ra đội hình xuất phát gồm trọn vẹn 11 ngoại binh mà không có bất kỳ cầu thủ Thái Lan nào, nhưng vẫn nhận thất bại 1-3 trước Shanghai Port. "
            "Cùng giờ, đại diện còn lại của xứ Chùa Vàng là Ratchaburi để Johor Darul Ta'zim của Malaysia cầm hòa 1-1 trên sân nhà và tiếp tục chưa có nổi trận thắng nào sau năm lượt đấu. "
            "Truyền thông Thái Lan đồng loạt bày tỏ sự thất vọng khi ba đội bóng nước này mới thắng đúng một trong 14 trận đã qua, bị Công an Hà Nội bỏ xa tới hơn gấp đôi điểm số."
        ),
        "source": "VnExpress / Tuổi Trẻ",
        "news_source": "VNEXPRESS / TUỔI TRẺ",
        "credit": "VNEXPRESS / TUỔI TRẺ / THAIRATH",
        "stat_badges": {
            "2": {"label": "BURIRAM UNITED", "value": "11 NGOẠI BINH • THUA 1-3", "sub": "Không có cầu thủ Thái Lan nào đá chính"},
            "4": {"label": "NỖI BUỒN THAI LEAGUE", "value": "1 THẮNG / 14 TRẬN", "sub": "Buriram 3 điểm, Ratchaburi 2 điểm"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_BURIRAM_1)], "VNEXPRESS", "Đội hình xuất phát 11 ngoại binh của Buriram United trong trận gặp Shanghai Port"),
            _slot("title", 0, [_url(TT_BURIRAM_2)], "TUỔI TRẺ", "Đội bóng số một Thái Lan tiếp tục chuỗi trận thất vọng ở Cúp C1 châu Á"),
            _slot("sentence", 1, [_url(TT_BURIRAM_CH)], "TUỔI TRẺ / THAIRATH", "Chủ tịch Newin Chidchob và bóng đá Thái Lan đối mặt áp lực lớn ở sân chơi châu lục"),
            _slot("sentence", 2, [_url(VNE_BURIRAM_1)], "VNEXPRESS", "Buriram United gục ngã 1-3 tại Thượng Hải dù sử dụng toàn bộ cầu thủ ngoại"),
            _slot("sentence", 3, [_url(TT_BURIRAM_2)], "TUỔI TRẺ", "Cả Buriram lẫn Ratchaburi đều chưa biết mùi chiến thắng sau năm lượt trận"),
            _slot("sentence", 4, [_url(TN_CAHN_6)], "THANH NIÊN", "Truyền thông khu vực so sánh sự vươn lên của Công an Hà Nội với chuỗi sa sút của Thai League"),
        ],
    },

    # 04 (Nữ — U17 VIỆT NAM TĂNG BẬC & 11 ĐỘI VÀO VÒNG 32 ĐỘI)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Việt Nam tăng bậc vào top 8 đội hạng ba, lộ diện 11 đội sớm vào vòng knock-out",
        "summary": (
            "Khép lại lượt trận thứ hai vòng bảng U17 World Cup 2026 vào rạng sáng 25 tháng 11, đội tuyển U17 Việt Nam bất ngờ đón tin vui khi tăng từ hạng tám lên hạng bảy trên bảng xếp hạng các đội đứng thứ ba có thành tích tốt nhất. "
            "Bước nhảy này có được nhờ việc U17 Nhật Bản để thua U17 Serbia 0-1 ở bảng L, rơi xuống thứ 11 với 0 điểm, qua đó giúp Việt Nam đứng trên cả Nhật Bản, Tanzania, Uganda và Trung Quốc. "
            "Ban tổ chức đồng thời xác định 11 trên 32 đội tuyển sớm giành vé đi tiếp trước một lượt trận, trong đó có U17 Mali, U17 Hàn Quốc, U17 Hy Lạp, U17 Tây Ban Nha, U17 Brazil, U17 Italia, U17 Uruguay, U17 Mexico, U17 Venezuela, U17 Colombia và U17 Serbia. "
            "Dù đang tạm giữ suất vé vớt, thầy trò huấn luyện viên Cristiano Roland vẫn phải hướng tới chiến thắng trước U17 Mali ở lượt cuối ngày 26 tháng 11 để chắc chắn tự quyết tấm vé lịch sử."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / VFF",
        "stat_badges": {
            "1": {"label": "NHÓM ĐỘI HẠNG BA", "value": "VIỆT NAM HẠNG 7/12", "sub": "1 điểm, hiệu số -1, ghi 5 bàn thắng"},
            "3": {"label": "SỚM VÀO VÒNG 32", "value": "11 ĐỘI CHẮC SUẤT", "sub": "Có U17 Mali, Hàn Quốc, Brazil, Tây Ban Nha"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_U17_LUC)], "THANH NIÊN / VFF", "U17 Việt Nam vươn lên đứng thứ bảy trong nhóm các đội xếp thứ ba có thành tích tốt nhất"),
            _slot("title", 0, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_03_1.jpg"))], "FIFA / DAILYSPORTS", "U17 Mali dẫn đầu bảng G sớm giành quyền vào vòng 32 đội U17 World Cup 2026"),
            _slot("sentence", 1, [_url(TN_U17_DEP)], "THANH NIÊN", "Vị trí thứ bảy hiện tại giúp đại diện Đông Nam Á tạm nằm trong nhóm tám đội vé vớt"),
            _slot("sentence", 2, [_ddgs("Japan U17 World Cup football match")], "BING SEARCH", "Thất bại liên tiếp đẩy U17 Nhật Bản xuống gần cuối bảng xếp hạng các đội hạng ba"),
            _slot("sentence", 3, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_20_1.jpg"))], "FIFA", "U17 Tây Ban Nha là một trong 11 đội sớm ghi tên vào vòng knock-out"),
            _slot("sentence", 3, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_20_4.jpg"))], "FIFA", "Các ứng viên hàng đầu đều thể hiện sức mạnh vượt trội sau hai lượt trận vòng bảng"),
            _slot("sentence", 4, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_03_3.jpg"))], "FIFA", "Cục diện vòng bảng đang bước vào giai đoạn căng thẳng trước lượt đấu quyết định"),
        ],
    },

    # 05 (Nam — NGUYỄN LỰC TOP 17 SOFASCORE, FVS & QUYẾT TÂM CỦA VĂN DƯƠNG)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "U17 WORLD CUP 2026",
        "title": "Chu Ngọc Nguyễn Lực lọt Top 17 Sofascore, U17 Việt Nam tự tin chơi sòng phẳng trước Mali",
        "summary": (
            "Chuyên trang thống kê quốc tế Sofascore vừa xếp tiền vệ Chu Ngọc Nguyễn Lực của U17 Việt Nam đứng thứ 17 toàn giải về điểm số trung bình sau hai lượt trận vòng bảng. "
            "Chân sút sinh năm 2009 đạt điểm trung bình 8,15 sau khi ghi hai bàn và có một kiến tạo, trực tiếp góp dấu giày vào ba trong năm bàn thắng của đội nhà trước Bỉ và New Zealand. "
            "Bên cạnh đó, giới chuyên môn cũng đánh giá cao sự chuẩn xác của ban huấn luyện khi U17 Việt Nam là một trong số ít đội tận dụng thành công quyền khiếu nại công nghệ video FVS để giành lại bàn thắng hợp lệ. "
            "Chia sẻ trước buổi tập phục hồi chiều 24 tháng 11, tiền đạo Nguyễn Văn Dương khẳng định toàn đội không trông chờ vào việc đối thủ giữ sức mà quyết tâm thắng U17 Mali bất kể đội bạn dùng đội hình nào."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / TUỔI TRẺ / DÂN TRÍ",
        "credit": "THANH NIÊN / TUỔI TRẺ / VFF",
        "stat_badges": {
            "2": {"label": "CHU NGỌC NGUYỄN LỰC", "value": "TOP 17 SOFASCORE", "sub": "8,15 điểm • 2 bàn thắng, 1 kiến tạo"},
            "3": {"label": "CÔNG NGHỆ FVS", "value": "KHIẾU NẠI THÀNH CÔNG", "sub": "Giữ lại bàn gỡ hòa 2-2 quý giá"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_U17_LUC_10)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực xếp hạng 17 trong danh sách cầu thủ hay nhất U17 World Cup của Sofascore"),
            _slot("title", 0, [_url(TT_U17_DUONG)], "TUỔI TRẺ / VFF", "Tiền đạo Nguyễn Văn Dương trả lời phỏng vấn trước buổi tập chiều 24 tháng 11"),
            _slot("sentence", 1, [_url(TN_U17_MALI_LUC)], "THANH NIÊN / VFF", "Tiền vệ số 10 của U17 Việt Nam nhận nhiều lời khen từ giới chuyên môn quốc tế"),
            _slot("sentence", 2, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_01_6.jpg"))], "DÂN TRÍ / VFF", "Nguyễn Lực ghi dấu ấn trong ba trên năm bàn thắng của đội tuyển tại Qatar"),
            _slot("sentence", 3, [_url(TT_U17_FVS)], "TUỔI TRẺ / L'EQUIPE", "Ban huấn luyện sử dụng thành công quyền khiếu nại FVS để đòi lại bàn thắng hợp lệ"),
            _slot("sentence", 4, [_url(TT_U17_ROL_TAP)], "TUỔI TRẺ / VFF", "Thầy trò huấn luyện viên Cristiano Roland tập trung rèn chiến thuật trước trận gặp Mali"),
            _slot("sentence", 4, [_url(TN_U17_TAP)], "THANH NIÊN / VFF", "Toàn đội quyết tâm chiến thắng để giành vé lịch sử vào vòng 32 đội"),
        ],
    },

    # 06 (Nữ — ĐT MALAYSIA BỔ NHIỆM HLV BOJAN HODAK)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "BÓNG ĐÁ ĐÔNG NAM Á",
        "title": "Đội tuyển Malaysia bổ nhiệm huấn luyện viên từng ba lần vô địch Indonesia",
        "summary": (
            "Tối ngày 24 tháng 11, Liên đoàn Bóng đá Malaysia chính thức công bố quyết định bổ nhiệm chiến lược gia người Croatia là ông Bojan Hodak làm huấn luyện viên trưởng đội tuyển quốc gia. "
            "Nhà cầm quân 55 tuổi sẽ kế nhiệm người tiền nhiệm Peter Cklamovski, trong khi huấn luyện viên tạm quyền Tan Cheng Hoe chuyển sang giữ vai trò Giám đốc các đội tuyển quốc gia. "
            "Trước khi nhận lời dẫn dắt bầy Hổ Mã Lai, ông Hodak từng có nhiều năm gắn bó với bóng đá Malaysia và vừa giúp câu lạc bộ Persib Bandung lập kỳ tích giành ba chức vô địch giải quốc nội Indonesia liên tiếp. "
            "Kinh nghiệm dày dạn tại khu vực Đông Nam Á của vị chiến lược gia ngoại thứ 45 trong lịch sử được kỳ vọng sẽ giúp tuyển Malaysia lấy lại vị thế trước các giải đấu lớn sắp tới."
        ),
        "source": "Dân Trí / ZNews",
        "news_source": "DÂN TRÍ / ZNEWS",
        "credit": "DÂN TRÍ / THEASIANGAME",
        "stat_badges": {
            "1": {"label": "TÂN HLV MALAYSIA", "value": "BOJAN HODAK", "sub": "Chiến lược gia 55 tuổi người Croatia"},
            "3": {"label": "THÀNH TÍCH ẤN TƯỢNG", "value": "3 LẦN VĐ INDONESIA", "sub": "Vừa thành công rực rỡ cùng Persib Bandung"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_MAL_1)], "DÂN TRÍ / THEASIANGAME", "Huấn luyện viên Bojan Hodak chính thức trở thành thuyền trưởng mới của đội tuyển Malaysia"),
            _slot("title", 0, [_url(DT_MAL_2)], "DÂN TRÍ / THEASIANGAME", "Ông Bojan Hodak từng gặt hái ba chức vô địch quốc gia tại Indonesia cùng Persib Bandung"),
            _slot("sentence", 1, [_url(DT_MAL_1)], "DÂN TRÍ / THEASIANGAME", "Quyết định bổ nhiệm được Ủy ban Quản lý đội tuyển Malaysia thông qua tối 24 tháng 11"),
            _slot("sentence", 2, [_url(DT_MAL_2)], "DÂN TRÍ / THEASIANGAME", "Bojan Hodak thay thế Peter Cklamovski tiếp quản chiếc ghế nóng tại Harimau Malaya"),
            _slot("sentence", 3, [_url(DT_MAL_1)], "DÂN TRÍ / THEASIANGAME", "Sự am hiểu bóng đá Đông Nam Á là điểm cộng lớn của nhà cầm quân người Croatia"),
            _slot("sentence", 4, [_url(DT_MAL_2)], "DÂN TRÍ / THEASIANGAME", "Liên đoàn Bóng đá Malaysia kỳ vọng ông Hodak sẽ vực dậy sức mạnh đội tuyển"),
        ],
    },

    # 07 (Nam — ÁNH VIÊN CÚ ĐÚP 2 HCV & PHÁ KỶ LỤC SAU 8 NĂM)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Ánh Viên giành cú đúp hai huy chương vàng, phá kỷ lục Đại hội sau tám năm",
        "summary": (
            "Đường đua xanh Đại hội Thể thao toàn quốc 2026 tối ngày 24 tháng 11 tiếp tục bùng nổ với màn trình diễn đỉnh cao của kình ngư kỳ cựu Nguyễn Thị Ánh Viên ở tuổi 30. "
            "Tại chung kết nội dung 100 mét ngửa nữ, tượng đài bơi lội Việt Nam bứt tốc ở 50 mét cuối để chạm thành bể với thông số 1 phút 02 giây 75, giành huy chương vàng cá nhân đầu tiên và xô đổ kỷ lục đại hội tồn tại tám năm do chính cô lập năm 2018. "
            "Ngay sau đó, Ánh Viên còn cùng em trai Nguyễn Quang Thuấn, Trần Hưng Nguyên và Nguyễn Thúy Hiền giành thêm huy chương vàng tiếp sức 4x100 mét hỗn hợp nam nữ với thời gian 3 phút 58 giây 95, phá cả kỷ lục quốc gia lẫn kỷ lục đại hội. "
            "Sau gần bốn năm giải nghệ, Ánh Viên đã có ba tấm huy chương vàng và sẽ tiếp tục tranh tài ở nội dung 50 mét ngửa trong ngày thi đấu 25 tháng 11."
        ),
        "source": "VnExpress / Thanh Niên / Tuổi Trẻ",
        "news_source": "VNEXPRESS / THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "100M NGỬA NỮ", "value": "1 PHÚT 02,75", "sub": "Phá kỷ lục đại hội năm 2018 của chính mình"},
            "3": {"label": "4X100M HỖN HỢP", "value": "3 PHÚT 58,95", "sub": "Phá kỷ lục quốc gia & kỷ lục đại hội"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_AV_NGUA)], "THANH NIÊN", "Nguyễn Thị Ánh Viên thi đấu thăng hoa và phá kỷ lục 100 mét ngửa nữ sau tám năm"),
            _slot("title", 0, [_url(TN_AV_SMILE)], "THANH NIÊN", "Kình ngư 30 tuổi rạng rỡ với tấm huy chương vàng cá nhân đầu tiên tại Đại hội 2026"),
            _slot("sentence", 1, [_url(TN_AV_HCV)], "THANH NIÊN", "Ánh Viên chứng minh bản lĩnh phi thường dù đã rời đỉnh cao gần bốn năm"),
            _slot("sentence", 2, [_url(TN_AV_NGUA)], "THANH NIÊN", "Thông số 1 phút 02 giây 75 giúp cô vượt qua cột mốc cũ 1 phút 03 giây 71 lập năm 2018"),
            _slot("sentence", 3, [_url(TN_AV_SMILE)], "THANH NIÊN", "Ánh Viên cùng đồng đội đoàn Quân đội phá sâu kỷ lục quốc gia nội dung tiếp sức hỗn hợp"),
            _slot("sentence", 4, [_url(TT_AV_OLD)], "TUỔI TRẺ", "Cựu tuyển thủ quốc gia hướng tới tấm huy chương vàng thứ tư ở nội dung 50 mét ngửa"),
        ],
    },

    # 08 (Nữ — THÚY HIỀN 6 HCV & BẢNG TỔNG SẮP ĐẠI HỘI NGÀY 24/11)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Nguyễn Thúy Hiền đạt sáu huy chương vàng, đoàn Quân Đội bứt phá vào Top 3 bảng tổng sắp",
        "summary": (
            "Bên cạnh sự tỏa sáng của Ánh Viên, tài năng 17 tuổi Nguyễn Thúy Hiền tiếp tục thống trị đường đua xanh Đại hội Thể thao toàn quốc khi nâng tổng thành tích cá nhân và tiếp sức lên sáu huy chương vàng. "
            "Đáng chú ý, cô gái trẻ đoàn Quân Đội phá kỷ lục đại hội ở cả sáu nội dung giành chiến thắng, đồng thời thiết lập kỷ lục quốc gia mới ở cự ly 50 mét ếch để dẫn đầu danh sách vận động viên giàu thành tích nhất Đại hội. "
            "Nhờ cơn mưa vàng từ môn bơi và bắn súng trong ngày 24 tháng 11, đoàn Quân Đội đạt tròn 100 huy chương với 31 huy chương vàng, chính thức vượt qua Công an Nhân dân để vươn lên vị trí thứ ba toàn đoàn. "
            "Trên ngôi đầu, chủ nhà Thành phố Hồ Chí Minh vẫn vững vàng với 66 huy chương vàng trong tổng số 179 huy chương, theo sau là Hà Nội với 53 huy chương vàng."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "NGUYỄN THÚY HIỀN", "value": "6 HCV • 6 KỶ LỤC", "sub": "Phá thêm kỷ lục quốc gia 50m ếch"},
            "4": {"label": "BẢNG TỔNG SẮP 24/11", "value": "TP.HCM 66 • HN 53 • QĐ 31", "sub": "Quân Đội vượt CAND chiếm vị trí thứ 3"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_THUY_HIEN)], "THANH NIÊN", "Nguyễn Thúy Hiền giành sáu huy chương vàng và phá sáu kỷ lục đại hội chỉ sau vài ngày"),
            _slot("title", 0, [_url(TT_AV_OLD)], "TUỔI TRẺ", "Môn bơi mang lại nguồn huy chương vàng chủ lực giúp đoàn Quân Đội bứt phá"),
            _slot("sentence", 1, [_url(TN_THUY_HIEN)], "THANH NIÊN", "Kình ngư 17 tuổi là vận động viên sở hữu nhiều huy chương vàng nhất tại Đại hội tính đến lúc này"),
            _slot("sentence", 2, [_url(TN_AV_HCV)], "THANH NIÊN", "Hai thế hệ vàng của bơi lội Quân đội góp công lớn vào thành tích chung toàn đoàn"),
            _slot("sentence", 3, [_url(TT_SHOOT_DUNG)], "TUỔI TRẺ / THANH ĐỊNH", "Đoàn Quân Đội cán mốc 100 huy chương để vươn lên chiếm vị trí thứ ba"),
            _slot("sentence", 4, [_url(TT_FUTSAL_1)], "TUỔI TRẺ", "Chủ nhà Thành phố Hồ Chí Minh duy trì khoảng cách an toàn trên ngôi đầu bảng tổng sắp"),
        ],
    },

    # 09 (Nam — ĐỊA CHẤN BẮN SÚNG: XẠ THỦ 37 TUỔI THẮNG TRỊNH THU VINH)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Xạ thủ 37 tuổi Nguyễn Thùy Dung gây sốc khi đánh bại Á quân thế giới Trịnh Thu Vinh",
        "summary": (
            "Trường bắn Đại hội Thể thao toàn quốc ngày 24 tháng 11 chứng kiến bất ngờ lớn ở chung kết nội dung 25 mét súng ngắn thể thao nữ. "
            "Á quân thế giới vừa giành vé dự Olympic 2028 là Trịnh Thu Vinh bước vào lượt bắn quyết định với tư cách ứng viên số một nhưng lại đánh mất nhịp độ và sớm dừng bước ở loạt thứ chín với 27 điểm, nhận huy chương đồng. "
            "Người bước lên bục cao nhất là xạ thủ kỳ cựu 37 tuổi Nguyễn Thùy Dung của đoàn Quân Đội, người chỉ xếp thứ tư vòng loại nhưng thể hiện bản lĩnh lạnh lùng để vượt qua đàn em Nguyễn Thùy Trang với tỷ số sít sao 32-31. "
            "Dù lỡ hẹn với tấm huy chương vàng cá nhân, Trịnh Thu Vinh vẫn kịp cùng các đồng đội đoàn Công an Nhân dân đoạt huy chương vàng ở nội dung đồng đội nữ."
        ),
        "source": "Tuổi Trẻ / Dân Trí",
        "news_source": "TUỔI TRẺ / DÂN TRÍ",
        "credit": "TUỔI TRẺ / THANH ĐỊNH",
        "stat_badges": {
            "2": {"label": "CÚ SỐC TRƯỜNG BẮN", "value": "THU VINH CHỈ ĐOẠT HCĐ", "sub": "Dừng bước ở loạt bắn thứ 9 với 27 điểm"},
            "3": {"label": "BẢN LĨNH TUỔI 37", "value": "THÙY DUNG HCV 32-31", "sub": "Thắng kịch tính đàn em Nguyễn Thùy Trang"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_SHOOT_3)], "TUỔI TRẺ / THANH ĐỊNH", "Ba xạ thủ Nguyễn Thùy Dung, Nguyễn Thùy Trang và Trịnh Thu Vinh trên bục nhận huy chương"),
            _slot("title", 0, [_url(TT_SHOOT_VINH)], "TUỔI TRẺ / THANH ĐỊNH", "Á quân thế giới Trịnh Thu Vinh thi đấu dưới sức ở loạt bắn chung kết cá nhân"),
            _slot("sentence", 1, [_url(TT_SHOOT_HUY)], "TUỔI TRẺ / THANH ĐỊNH", "Môn bắn súng Đại hội Thể thao toàn quốc 2026 chứng kiến nhiều màn so tài kịch tính"),
            _slot("sentence", 2, [_url(TT_SHOOT_VINH)], "TUỔI TRẺ / THANH ĐỊNH", "Dù khởi đầu ấn tượng với năm phát trúng đích, Thu Vinh vẫn hụt hơi ở giai đoạn quyết định"),
            _slot("sentence", 3, [_url(TT_SHOOT_DUNG)], "TUỔI TRẺ / THANH ĐỊNH", "Xạ thủ 37 tuổi Nguyễn Thùy Dung lội ngược dòng ngoạn mục mang về tấm HCV quý giá cho Quân Đội"),
            _slot("sentence", 4, [_url(TT_SHOOT_3)], "TUỔI TRẺ / THANH ĐỊNH", "Thu Vinh cùng các đồng đội Công an Nhân dân vẫn giữ vững ngôi vô địch đồng đội nữ"),
        ],
    },

    # 10 (Nữ — ĐẠI CHIẾN CẦU LÔNG NGUYỄN THÙY LINH VS VŨ THỊ TRANG)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Nguyễn Thùy Linh đại chiến Vũ Thị Trang ở chung kết cầu lông đơn nữ tối 25 tháng 11",
        "summary": (
            "Tối ngày 24 tháng 11 tại nhà thi đấu Hồ Xuân Hương, khán giả Thành phố Hồ Chí Minh đã lấp kín mọi khán đài để theo dõi hai trận bán kết kịch tính nội dung đơn nữ môn cầu lông Đại hội Thể thao toàn quốc 2026. "
            "Hạt giống số một Nguyễn Thùy Linh đại diện đoàn Đồng Nai thể hiện đẳng cấp vượt trội khi chỉ cần hai ván đấu để thắng áp đảo Vũ Thị Anh Thư với các tỷ số 21-9 và 21-7. "
            "Ở nhánh bán kết còn lại, tay vợt dày dạn kinh nghiệm Vũ Thị Trang của chủ nhà Thành phố Hồ Chí Minh thắng dễ 21-7 trong ván đầu trước tài năng 15 tuổi Nguyễn Thị Thu Huyền nhưng phải vất vả mới khép lại ván hai ở điểm số 23-21. "
            "Kết quả này tạo nên trận chung kết trong mơ giữa hai tay vợt nữ hàng đầu Việt Nam vào tối nay 25 tháng 11, bên cạnh màn nội chiến đơn nam giữa Nguyễn Hải Đăng và Phan Phúc Thịnh."
        ),
        "source": "Tuổi Trẻ / Dân Trí / Thanh Niên",
        "news_source": "TUỔI TRẺ / DÂN TRÍ / THANH NIÊN",
        "credit": "TUỔI TRẺ / DÂN TRÍ",
        "stat_badges": {
            "2": {"label": "BÁN KẾT ĐƠN NỮ", "value": "THÙY LINH THẮNG 21-9, 21-7", "sub": "Vượt qua Vũ Thị Anh Thư nhanh chóng"},
            "4": {"label": "CHUNG KẾT TỐI 25/11", "value": "THÙY LINH VS VŨ THỊ TRANG", "sub": "Nhà thi đấu Hồ Xuân Hương lúc 18h30"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_BAD_LINH)], "TUỔI TRẺ / ĐỨC KHUÊ", "Nguyễn Thùy Linh tiến vào chung kết đơn nữ Đại hội với phong độ áp đảo"),
            _slot("title", 0, [_url(TT_BAD_TRANG)], "TUỔI TRẺ / ĐỨC KHUÊ", "Vũ Thị Trang bản lĩnh vượt qua tài năng trẻ Thu Huyền để tranh huy chương vàng"),
            _slot("sentence", 1, [_url(DT_BAD_ARENA)], "DÂN TRÍ / NAM ANH", "Khán giả phủ kín nhà thi đấu Hồ Xuân Hương cổ vũ các trận bán kết tối 24 tháng 11"),
            _slot("sentence", 2, [_url(TT_BAD_LINH)], "TUỔI TRẺ / ĐỨC KHUÊ", "Tay vợt số một Việt Nam không gặp nhiều khó khăn để áp đặt lối chơi trước Anh Thư"),
            _slot("sentence", 3, [_url(TT_BAD_TRANG)], "TUỔI TRẺ / ĐỨC KHUÊ", "Vũ Thị Trang phải tận dụng kinh nghiệm trận mạc mới khuất phục được đàn em 15 tuổi ở ván hai"),
            _slot("sentence", 4, [_url(TT_BAD_CROWD)], "TUỔI TRẺ / ĐÌNH GIA LƯƠNG", "Người hâm mộ háo hức chờ đợi cuộc so tài đỉnh cao tối 25 tháng 11 tại Thành phố Hồ Chí Minh"),
        ],
    },

    # 11 (Nam — BILLIARDS: ĐKVĐ CHÂU Á NGUYỄN ĐỨC YẾN SINH BỊ LOẠI SỐC)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Đương kim vô địch carom 3 băng châu Á Nguyễn Đức Yến Sinh bất ngờ bị loại ở Đại hội",
        "summary": (
            "Ngày thi đấu 24 tháng 11 môn billiards và snooker tại Đại hội Thể thao toàn quốc 2026 chứng kiến cú sốc lớn ở nội dung carom 3 băng nữ. "
            "Nhà đương kim vô địch châu Á Nguyễn Đức Yến Sinh của Thành phố Hồ Chí Minh bất ngờ dừng bước ngay tại vòng tứ kết sau thất bại 18-25 trước cơ thủ Nguyễn Thị Thu Hiền của Đà Nẵng sau 17 lượt cơ. "
            "Ở nội dung carom 1 băng đơn nam, cơ thủ Vương Minh Thiện của đoàn Bắc Ninh xuất sắc đánh bại Nguyễn Như Lê với tỷ số 100-70 sau 11 lượt cơ nhờ những sê-ri điểm 21 và 17 đầy bản lĩnh để giành huy chương vàng. "
            "Trong khi đó, trận chung kết snooker 6 bi đỏ đơn nam chứng kiến chiến thắng 3-1 của Thái Văn Nam trước đồng đội Hà Nội là Phạm Hoài Nam."
        ),
        "source": "Thanh Niên",
        "news_source": "THANH NIÊN",
        "credit": "THANH NIÊN",
        "stat_badges": {
            "2": {"label": "CÚ SỐC CAROM 3 BĂNG", "value": "YẾN SINH THUA 18-25", "sub": "Dừng bước sớm ở tứ kết trước Thu Hiền"},
            "3": {"label": "CAROM 1 BĂNG NAM", "value": "VƯƠNG MINH THIỆN HCV", "sub": "Thắng Nguyễn Như Lê 100-70 sau 11 lượt cơ"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_BILL_YS)], "THANH NIÊN", "Nhà vô địch châu Á Nguyễn Đức Yến Sinh bất ngờ dừng bước tại tứ kết Đại hội Toàn quốc"),
            _slot("title", 0, [_url(TN_BILL_1)], "THANH NIÊN", "Vương Minh Thiện giành HCV nội dung carom 1 băng nam đầy thuyết phục"),
            _slot("sentence", 1, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_10_1.jpg"))], "TUỔI TRẺ / ĐỨC PHONG", "Các nội dung billiards Đại hội Thể thao toàn quốc diễn ra với nhiều bất ngờ thú vị"),
            _slot("sentence", 2, [_url(TN_BILL_YS)], "THANH NIÊN", "Nguyễn Thị Thu Hiền tung sê-ri 6 điểm để loại đương kim vô địch châu Á Yến Sinh"),
            _slot("sentence", 3, [_url(TN_BILL_1)], "THANH NIÊN", "Cơ thủ Bắc Ninh Vương Minh Thiện bứt phá ngoạn mục ở giai đoạn nước rút"),
            _slot("sentence", 4, [_url(TN_BILL_YS)], "THANH NIÊN", "Đoàn Hà Nội thống trị hoàn toàn trận chung kết nội dung snooker 6 bi đỏ đơn nam"),
        ],
    },

    # 12 (Nữ — HY HỮU XE ĐẠP ĐẠI HỘI: CUA-RƠ ĐỒNG NAI PHANH SÁT VẠCH ĐÍCH)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Hy hữu cua-rơ Đồng Nai phanh gấp trước vạch đích nhường đồng đội nhưng vẫn bất thành",
        "summary": (
            "Nội dung xe đạp đường trường tính điểm nam tại xã Cần Giờ thuộc Đại hội Thể thao toàn quốc 2026 vừa chứng kiến một tình huống chiến thuật hy hữu ngay trước vạch đích. "
            "Khi cua-rơ Lê Ngọc Sơn của An Giang đã chắc chắn giành huy chương vàng, tay đua Trần Trọng Phúc của Đồng Nai giảm tốc độ và dừng hẳn xe sát vạch đích theo hiệu lệnh ban huấn luyện để chờ đồng đội Nguyễn Hướng vượt lên tích lũy điểm tranh huy chương đồng. "
            "Tuy nhiên, trong khoảnh khắc khựng lại ngoái đầu nhìn đồng đội, bánh trước xe của Trọng Phúc đã vô tình lướt qua vạch đích trước khi Nguyễn Hướng kịp lao tới. "
            "Trọng tài xác định Trọng Phúc về nhì giành huy chương bạc, còn Nguyễn Hướng chỉ có tổng 11 điểm và chấp nhận xếp thứ tư, kém tay đua giành huy chương đồng của Hà Nội đúng một điểm."
        ),
        "source": "VnExpress / 24h",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / BING SEARCH",
        "stat_badges": {
            "2": {"label": "TÌNH HUỐNG HY HỮU", "value": "PHANH SÁT VẠCH ĐÍCH", "sub": "Chờ đồng đội Nguyễn Hướng tranh HCĐ"},
            "4": {"label": "KẾT QUẢ ĐÁNG TIẾC", "value": "KÉM ĐÚNG 1 ĐIỂM", "sub": "Bánh trước lướt qua vạch trước khi chờ kịp"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_CYCLE_1)], "VNEXPRESS", "Khoảnh khắc cua-rơ Trần Trọng Phúc dừng xe sát vạch đích chờ đồng đội tại Cần Giờ"),
            _slot("title", 0, [_ddgs("road cycling sprint finish line race")], "BING SEARCH", "Diễn biến nước rút căng thẳng trên đường đua xe đạp đường trường"),
            _slot("sentence", 1, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_11_2.jpg"))], "TUỔI TRẺ / XE ĐẠP ONLINE", "Chặng đua tính điểm 41,52 ki-lô-mét diễn ra với kịch bản đầy bất ngờ ở vòng cuối"),
            _slot("sentence", 2, [_ddgs("cyclist stopping before finish line team tactics")], "BING SEARCH", "Ban huấn luyện Đồng Nai ra hiệu lệnh cho Trọng Phúc giảm tốc nhường điểm cho Nguyễn Hướng"),
            _slot("sentence", 3, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_11_1.jpg"))], "TUỔI TRẺ / XE ĐẠP ONLINE", "Bánh xe trước của Trọng Phúc vô tình cán vạch đích khiến toan tính chiến thuật đổ bể"),
            _slot("sentence", 4, [_ddgs("road cycling race peloton finish")], "BING SEARCH", "Nguyễn Văn Dương của Hà Nội bảo toàn tấm huy chương đồng nhờ hơn đúng một điểm"),
        ],
    },

    # 13 (Nam — REAL MADRID 5-1 PSV EINDHOVEN: MOURINHO, BELLINGHAM & MBAPPÉ)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "UEFA CHAMPIONS LEAGUE",
        "title": "Mourinho thay ba người xoay chuyển cục diện, Real Madrid thắng PSV 5-1 lên đỉnh bảng",
        "summary": (
            "Rạng sáng ngày 25 tháng 11 tại sân Santiago Bernabéu, Real Madrid trải qua hiệp một đầy khó khăn khi bị PSV Eindhoven dẫn trước 1-0 sau quả phạt đền thành công của lão tướng Ivan Perišić ở phút 32. "
            "Bước ngoặt xuất hiện ngay đầu hiệp hai khi huấn luyện viên José Mourinho quyết định thay liền ba cầu thủ, tung Jude Bellingham vào sân để lập tức xoay chuyển nhịp độ tấn công. "
            "Sau bàn gỡ hòa của Federico Valverde phút 50, Bellingham tạo nên siêu phẩm vẩy má ngoài kiểu Zinedine Zidane phút 60 trước khi Kylian Mbappé lập cú đúp ở các phút 64 và 84 để trở thành cầu thủ Pháp đầu tiên ghi bàn bảy trận Champions League liên tiếp. "
            "Pha lập công của Vinícius Júnior ở phút 87 ấn định chiến thắng hủy diệt 5-1, đưa Real Madrid giữ mạch toàn thắng năm trận và độc chiếm ngôi đầu bảng."
        ),
        "source": "VnExpress / Tuổi Trẻ / BBC Sport",
        "news_source": "VNEXPRESS / TUỔI TRẺ / BBC SPORT",
        "credit": "VNEXPRESS / DÂN TRÍ / GETTY",
        "stat_badges": {
            "2": {"label": "DẤU ẤN MOURINHO", "value": "THAY 3 NGƯỜI HIỆP 2", "sub": "Tung Bellingham tạo bước ngoặt 5 bàn"},
            "3": {"label": "KYLIAN MBAPPÉ", "value": "CÚ ĐÚP • 7 TRẬN LIÊN TIẾP", "sub": "Chạm mốc 75 bàn tại Champions League"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_REAL_1)], "VNEXPRESS / GETTY", "Bellingham và Mbappé ăn mừng trong chiến thắng ngược dòng 5-1 của Real Madrid"),
            _slot("title", 0, [_url(DT_REAL_TEAM)], "DÂN TRÍ / GETTY", "Đội bóng của José Mourinho toàn thắng cả năm lượt trận để dẫn đầu Champions League"),
            _slot("sentence", 1, [_url(DT_REAL_PERI)], "DÂN TRÍ / GETTY", "Ivan Perišić ghi bàn phạt đền giúp PSV gây sốc khi dẫn trước tại Bernabéu trong hiệp một"),
            _slot("sentence", 2, [_url(VNE_REAL_BEL)], "VNEXPRESS / GETTY", "Jude Bellingham vào sân từ đầu hiệp hai và lập tức thắp sáng lối chơi cho đội chủ nhà"),
            _slot("sentence", 3, [_url(VNE_REAL_MBA)], "VNEXPRESS / GETTY", "Kylian Mbappé ghi cú đúp, nối dài kỷ lục nổ súng bảy trận liên tiếp ở đấu trường châu Âu"),
            _slot("sentence", 4, [_url(VNE_REAL_VIN)], "VNEXPRESS / GETTY", "Vinícius Júnior ấn định thắng lợi 5-1 sau đường kiến tạo tinh tế của Bellingham"),
        ],
    },

    # 14 (Nữ — MAN CITY 2-2 NAPOLI: TRI ÂN DE BRUYNE & NỖI THẤT VỌNG CỦA HAALAND)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "UEFA CHAMPIONS LEAGUE",
        "title": "Man City hòa kịch tính Napoli 2-2 trong đêm tri ân De Bruyne, Haaland thừa nhận bế tắc",
        "summary": (
            "Sân vận động Etihad rạng sáng 25 tháng 11 chứng kiến bầu không khí đầy xúc động khi hàng vạn cổ động viên Manchester City giăng biểu ngữ King Kev chào đón huyền thoại Kevin De Bruyne trở lại trong màu áo Napoli. "
            "Tuy nhiên trên sân cỏ, đội bóng của huấn luyện viên Enzo Maresca tiếp tục phơi bày lỗ hổng phòng ngự khi hai lần bị đại diện nước Ý vượt lên dẫn trước nhờ công của Rasmus Højlund và Noa Lang. "
            "Manchester City phải nhờ đến bàn thắng đầu tiên cho đội một của tài năng trẻ Ayyoub Bouaddi và pha solo gỡ hòa ở phút 86 của Rayan Cherki mới giữ lại được kết quả hòa 2-2. "
            "Phát biểu sau trận đấu, tiền đạo Erling Haaland không giấu nổi sự thất vọng khi thừa nhận toàn đội đang rơi vào trạng thái hoài nghi mọi thứ giữa chuỗi trận sa sút."
        ),
        "source": "Sky Sports / VnExpress / Dân Trí",
        "news_source": "SKY SPORTS / VNEXPRESS / DÂN TRÍ",
        "credit": "SKY SPORTS / VNEXPRESS",
        "stat_badges": {
            "1": {"label": "NGÀY TRỞ LẠI ETIHAD", "value": "TRI ÂN DE BRUYNE", "sub": "Biểu ngữ King Kev rực sáng khán đài"},
            "3": {"label": "RƯỢT ĐUỔI TỶ SỐ", "value": "MAN CITY 2-2 NAPOLI", "sub": "Rayan Cherki gỡ hòa quý giá phút 86"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_CITY_KDB)], "SKY SPORTS", "Kevin De Bruyne thi đấu đầy nỗ lực trong ngày tái ngộ đội bóng cũ Manchester City"),
            _slot("title", 0, [_url(SKY_CITY_CHERKI)], "SKY SPORTS", "Rayan Cherki vỗ tay tri ân khán giả sau bàn thắng giữ lại 1 điểm ở phút 86"),
            _slot("sentence", 1, [_url(VNE_CITY_BANNER)], "VNEXPRESS", "Khán đài Etihad phủ kín thông điệp tri ân dành cho huyền thoại người Bỉ"),
            _slot("sentence", 2, [_url(SKY_CITY_HOJ)], "SKY SPORTS", "Rasmus Højlund ăn mừng bàn mở tỷ số khiến hàng thủ Man City chao đảo"),
            _slot("sentence", 3, [_url(SKY_CITY_CHERKI)], "SKY SPORTS", "Khoảnh khắc tỏa sáng muộn màng của Cherki giúp thầy trò Enzo Maresca tránh thất bại sân nhà"),
            _slot("sentence", 4, [_url(SKY_CITY_HAAL)], "SKY SPORTS", "Erling Haaland thừa nhận cả đội đang chịu áp lực tâm lý nặng nề vì phong độ trồi sụt"),
        ],
    },

    # 15 (Nam — ARSENAL 1-1 DORTMUND: PHUNG PHÍ 30 CÚ SÚT & ĐỨT MẠCH THẮNG)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "UEFA CHAMPIONS LEAGUE",
        "title": "Arsenal tung 30 cú sút vẫn hòa Dortmund 1-1, lỡ hẹn cân bằng kỷ lục của Liverpool",
        "summary": (
            "Tiếp đón Borussia Dortmund trên sân Emirates rạng sáng 25 tháng 11, Arsenal khởi đầu như mơ khi tiền đạo Viktor Gyökeres sút xa uy lực mở tỷ số ngay phút thứ 10. "
            "Thầy trò huấn luyện viên Mikel Arteta hoàn toàn áp đảo khi tung ra tới 30 pha dứt điểm suốt trận đấu nhưng liên tục phung phí cơ hội ngon ăn và đưa bóng tìm đến khung gỗ. "
            "Sự thiếu sắc bén khiến Pháo thủ phải trả giá ở phút 55 khi tiền đạo Maximilian Beier tận dụng khoảnh khắc lơi lỏng của hàng thủ để ghi bàn gỡ hòa 1-1 cho đại diện nước Đức. "
            "Trận hòa đáng tiếc khiến Arsenal đứt chuỗi 12 chiến thắng sân nhà liên tiếp tại vòng bảng và vòng phân hạng Champions League, lỡ cơ hội san bằng kỷ lục của Liverpool đúng một trận."
        ),
        "source": "VnExpress / Sky Sports / BBC Sport / The Guardian",
        "news_source": "VNEXPRESS / SKY SPORTS / BBC SPORT",
        "credit": "SKY SPORTS / BBC SPORT / VNEXPRESS",
        "stat_badges": {
            "2": {"label": "SỨC ÉP ÁP ĐẢO", "value": "30 CÚ SÚT • 1 BÀN", "sub": "Phung phí cơ hội và dứt điểm trúng cột"},
            "4": {"label": "ĐỨT CHUỖI SÂN NHÀ", "value": "DỪNG Ở 12 TRẬN", "sub": "Lỡ hẹn san bằng kỷ lục 13 trận của Liverpool"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_ARS_BVB)], "SKY SPORTS", "Các cầu thủ Arsenal tiếc nuối sau khi đánh rơi chiến thắng trước Borussia Dortmund"),
            _slot("title", 0, [_url(SKY_ARS_GYO)], "SKY SPORTS", "Viktor Gyökeres ăn mừng bàn mở tỷ số sớm ở phút thứ 10 tại sân Emirates"),
            _slot("sentence", 1, [_url(BBC_ARS_GYO)], "BBC SPORT", "Pha sút xa búa bổ của Gyökeres mở ra thế trận vượt trội cho đội chủ nhà"),
            _slot("sentence", 2, [_url(VNE_ARS_RICE)], "VNEXPRESS / AP", "Declan Rice ôm đầu tiếc nuối sau cú dứt điểm dội cột dọc trong hiệp hai"),
            _slot("sentence", 3, [_url(SKY_ARS_BVB)], "SKY SPORTS", "Maximilian Beier trừng phạt sự phung phí của Arsenal bằng bàn gỡ hòa 1-1"),
            _slot("sentence", 4, [_url(SKY_ARS_GYO)], "SKY SPORTS", "Đoàn quân của Mikel Arteta lỡ cơ hội cân bằng chuỗi trận thắng sân nhà của Liverpool"),
        ],
    },

    # 16 (Nữ — ASTON VILLA THUA GALATASARAY 0-1)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "UEFA CHAMPIONS LEAGUE",
        "title": "Aston Villa gục ngã 0-1 tại Istanbul, nối dài chuỗi sáu trận liên tiếp không thắng",
        "summary": (
            "Chuyến làm khách đầy bão táp của Aston Villa trên sân RAMS Park của Galatasaray tối ngày 24 tháng 11 khép lại bằng kịch bản cay đắng cho đại diện Ngoại hạng Anh. "
            "Trong suốt 90 phút bế tắc trước hàng phòng ngự kín kẽ của đội bóng Thổ Nhĩ Kỳ, thầy trò huấn luyện viên Unai Emery thậm chí không có nổi một cú sút trúng đích nào và tịt ngòi trận thứ hai liên tiếp. "
            "Bước ngoặt đến ở phút 77 khi cầu thủ vào sân thay người Deniz Gül bật cao đánh đầu chuẩn xác ghi bàn thắng duy nhất mang về thắng lợi 1-0 cho Galatasaray. "
            "Thất bại này nối dài mạch không thắng của Aston Villa lên sáu trận liên tiếp trên mọi đấu trường và đẩy họ vào thế hiểm nghèo trước hai cuộc đại chiến gặp PSG và Dortmund."
        ),
        "source": "Sky Sports / The Guardian",
        "news_source": "SKY SPORTS / THE GUARDIAN",
        "credit": "SKY SPORTS",
        "stat_badges": {
            "2": {"label": "HÀNG CÔNG BẾ TẮC", "value": "0 CÚ SÚT TRÚNG ĐÍCH", "sub": "Tịt ngòi hai trận liên tiếp"},
            "4": {"label": "KHỦNG HOẢNG PHONG ĐỘ", "value": "6 TRẬN KHÔNG THẮNG", "sub": "Thua hai trận liên tiếp tại Champions League"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_VILLA_GALA)], "SKY SPORTS", "Deniz Gül ăn mừng bàn thắng quý giá giúp Galatasaray hạ gục Aston Villa 1-0"),
            _slot("title", 0, [_url(SKY_VILLA_MAAT)], "SKY SPORTS", "Hậu vệ Ian Maatsen và Aston Villa trải qua đêm thi đấu đầy bế tắc tại Istanbul"),
            _slot("sentence", 1, [_ddgs("Galatasaray Champions League RAMS Park football match")], "BING SEARCH", "Sức ép từ chảo lửa RAMS Park khiến đại diện nước Anh không thể triển khai bóng"),
            _slot("sentence", 2, [_ddgs("Unai Emery Aston Villa coach touchline serious")], "BING SEARCH", "Huấn luyện viên Unai Emery bất lực nhìn hàng công không tạo nổi cú sút trúng đích"),
            _slot("sentence", 3, [_url(SKY_VILLA_GALA)], "SKY SPORTS", "Pha đánh đầu phút 77 của Deniz Gül nhấn chìm mọi nỗ lực giữ lại 1 điểm của đội khách"),
            _slot("sentence", 4, [_ddgs("Aston Villa football team disappointed match")], "BING SEARCH", "Aston Villa lần đầu thua hai trận châu Âu liên tiếp dưới thời ông Unai Emery"),
        ],
    },

    # 17 (Nam — RONALDO GHI BÀN THỨ 987 & CHE MẮT NHẠI TRỌNG TÀI)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "AFC CHAMPIONS LEAGUE ELITE",
        "title": "Ronaldo chạm mốc 987 bàn thắng nhưng gây tranh cãi với cử chỉ che mắt nhại trọng tài",
        "summary": (
            "Đêm 24 tháng 11 ở lượt trận thứ năm AFC Champions League Elite khu vực Tây Á, Cristiano Ronaldo sút phạt đền mở tỷ số ngay phút 13 giúp Al Nassr đánh bại Al Sadd 2-1 với pha móc bóng xe đạp chổng ngược ấn định của João Félix. "
            "Bàn thắng này giúp siêu sao 41 tuổi nâng thành tích sự nghiệp lên 987 pha lập công, chỉ còn cách cột mốc lịch sử 1000 bàn đúng 13 lần xé lưới nữa, đồng thời đưa Al Nassr sớm vào vòng 16 đội. "
            "Tuy nhiên trong hiệp hai, khi bị trọng tài người Jordan Adham Makhadmeh từ chối phạt đền vì trợ lý căng cờ báo việt vị, Ronaldo đã nổi giận dùng tay che mắt và nhại động tác phất cờ đầy mỉa mai. "
            "Hành vi thiếu kiềm chế này khiến báo chí Trung Đông cảnh báo đội trưởng Al Nassr hoàn toàn có thể đối mặt án phạt tiền hoặc treo giò từ Liên đoàn Bóng đá châu Á."
        ),
        "source": "Thanh Niên / VnExpress / Lao Động",
        "news_source": "THANH NIÊN / VNEXPRESS",
        "credit": "THANH NIÊN / VNEXPRESS",
        "stat_badges": {
            "2": {"label": "HÀNH TRÌNH LỊCH SỬ", "value": "987 BÀN THẮNG", "sub": "Chỉ còn cách cột mốc 1000 bàn đúng 13 pha lập công"},
            "3": {"label": "TRANH CÃI TRÊN SÂN", "value": "CHE MẮT NHẠI TRỌNG TÀI", "sub": "Nguy cơ đối mặt án kỷ luật từ AFC"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_RONALDO_987)], "THANH NIÊN", "Cristiano Ronaldo nâng thành tích sự nghiệp lên 987 bàn thắng trong màu áo Al Nassr"),
            _slot("title", 0, [_url(VNE_RONALDO_REF)], "VNEXPRESS", "Siêu sao Bồ Đào Nha che mắt nhại động tác báo việt vị sau khi bị từ chối phạt đền"),
            _slot("sentence", 1, [_ddgs("Cristiano Ronaldo Al Nassr football match action")], "BING SEARCH", "Ronaldo mở tỷ số ở phút 13 góp phần giúp Al Nassr đánh bại Al Sadd 2-1"),
            _slot("sentence", 2, [_url(TN_RONALDO_987)], "THANH NIÊN", "Chân sút 41 tuổi tiếp tục tiến sát cột mốc vĩ đại 1000 bàn thắng chuyên nghiệp"),
            _slot("sentence", 3, [_url(VNE_RONALDO_REF)], "VNEXPRESS", "Cử chỉ mỉa mai trọng tài biên không thấy đường của Ronaldo gây bão mạng xã hội"),
            _slot("sentence", 4, [_ddgs("Cristiano Ronaldo Al Nassr captain Saudi Pro League")], "BING SEARCH", "Người hâm mộ Al Nassr lo ngại thủ quân đội bóng có thể nhận án phạt từ AFC"),
        ],
    },

    # 18 (Nữ — CAS TRẢ CHỨC VÔ ĐỊCH AFCON 2025 CHO SENEGAL, TƯỚC CÚP MOROCCO)
    {
        "id": 18,
        "art_id": "art_18",
        "group": "BÓNG ĐÁ THẾ GIỚI",
        "title": "Tòa án Thể thao tước chức vô địch châu Phi của Morocco, trao lại ngôi vương cho Senegal",
        "summary": (
            "Ngày 24 tháng 11, Tòa án Trọng tài Thể thao thế giới đã tạo nên bước ngoặt pháp lý lịch sử khi chấp thuận đơn kháng cáo của Senegal và tước lại chức vô địch Cúp bóng đá châu Phi 2025 mà Morocco nắm giữ trên giấy tờ suốt 252 ngày. "
            "Nguồn cơn vụ việc bắt nguồn từ trận chung kết hồi tháng 1 tại Rabat khi các cầu thủ Senegal bỏ vào đường hầm phản đối quả phạt đền phút cuối, trước khi trở lại thi đấu và thắng 1-0 trong hiệp phụ nhờ bàn thắng của Pape Gueye. "
            "Hội đồng ba thẩm phán khẳng định vì trọng tài chính không dừng hẳn trận đấu mà cho đá tiếp đến hết giờ nên quyết định chuyên môn trên sân là chung cuộc, qua đó hủy án xử thua 0-3 của Liên đoàn Bóng đá châu Phi hồi tháng 3. "
            "Tuy nhiên dư âm vụ án vẫn chưa lắng xuống khi truyền thông Pháp tung nghi vấn quan chức Senegal từng điện đàm với thành viên hội đồng xét xử trước giờ tuyên án, khiến Morocco để ngỏ khả năng tiếp tục khiếu kiện."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ / BBC Sport",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ / BBC SPORT",
        "credit": "VNEXPRESS / TUỔI TRẺ / REUTERS",
        "stat_badges": {
            "1": {"label": "PHÁN QUYẾT LỊCH SỬ", "value": "SENEGAL ĐÒI LẠI CÚP", "sub": "Morocco mất danh hiệu sau 252 ngày"},
            "3": {"label": "CƠ SỞ PHÁP LÝ", "value": "LUẬT BÓNG ĐÁ ĐIỀU 5", "sub": "Quyết định trên sân của trọng tài là tối hậu"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_SEN_MANE)], "VNEXPRESS / REUTERS", "Sadio Mane và đội tuyển Senegal chính thức được khôi phục danh hiệu vô địch châu Phi 2025"),
            _slot("title", 0, [_url(TT_SEN_CAS)], "TUỔI TRẺ / REUTERS", "Trụ sở Tòa án Trọng tài Thể thao tại Thụy Sĩ nơi đưa ra phán quyết lịch sử"),
            _slot("sentence", 1, [_url(VNE_SEN_MANE)], "VNEXPRESS / REUTERS", "Cúp vô địch AFCON 2025 trở về tay Senegal sau cuộc chiến pháp lý kéo dài 10 tháng"),
            _slot("sentence", 2, [_url(TT_SEN_FIGHT)], "TUỔI TRẺ / REUTERS", "Sự cố cầu thủ rời sân phản đối ở chung kết hồi tháng 1 từng gây chấn động bóng đá thế giới"),
            _slot("sentence", 3, [_url(VNE_SEN_DIAZ)], "VNEXPRESS / REUTERS", "Cú đá phạt đền hỏng ăn của Brahim Diaz và bàn thắng hiệp phụ của Pape Gueye được công nhận"),
            _slot("sentence", 4, [_url(VNE_SEN_MOR)], "VNEXPRESS / REUTERS", "Phía Morocco phản ứng gay gắt và xem xét kháng cáo lên Tòa án Liên bang Thụy Sĩ"),
        ],
    },

    # 19 (Nam — FA HỦY ÁN TREO GIÒ YORO, POCHETTINO NỔI GIẬN & NGÂN SÁCH 50 TRIỆU BẢNG)
    {
        "id": 19,
        "art_id": "art_19",
        "group": "NGOẠI HẠNG ANH",
        "title": "FA xóa án treo giò Leny Yoro, Pochettino vẫn phẫn nộ và đối mặt ngân sách mua sắm eo hẹp",
        "summary": (
            "Liên đoàn Bóng đá Anh ngày 24 tháng 11 chính thức chấp thuận đơn kháng cáo của Manchester United, hủy bỏ án treo giò một trận của trung vệ Leny Yoro sau tấm thẻ đỏ phút thứ tám ở trận thua Liverpool 0-4. "
            "Dù Yoro đủ điều kiện ra sân gặp Brentford cuối tuần này, sếp trọng tài Howard Webb vẫn lên truyền hình bảo vệ quyết định phạt thẻ đỏ ban đầu, khiến huấn luyện viên Mauricio Pochettino nổi cơn thịnh nộ. "
            "Nhà cầm quân người Argentina chỉ trích gay gắt tổ trọng tài lẫn công nghệ VAR khi bỏ qua cả tình huống Bradley Barcola đứng sát hàng rào ở bàn mở tỷ số của Szoboszlai, đồng thời chất vấn rằng việc hủy thẻ đỏ lúc này không thể trả lại ba điểm đã mất. "
            "Khó khăn càng chồng chất với tân thuyền trưởng Quỷ đỏ khi báo chí Anh tiết lộ ông chỉ được cấp ngân sách dưới 50 triệu bảng cho tối đa hai tân binh vào kỳ chuyển nhượng tháng 1 năm 2027."
        ),
        "source": "VnExpress / Sky Sports / Dân Trí / BBC Sport",
        "news_source": "VNEXPRESS / SKY SPORTS / DÂN TRÍ",
        "credit": "SKY SPORTS / VNEXPRESS / DÂN TRÍ",
        "stat_badges": {
            "1": {"label": "PHÁN QUYẾT CỦA FA", "value": "XÓA ÁN TREO GIÒ YORO", "sub": "Kịp trở lại trận gặp Brentford ngày 28/11"},
            "4": {"label": "CHUYỂN NHƯỢNG 1/2027", "value": "DƯỚI 50 TRIỆU BẢNG", "sub": "Ngân sách hạn hẹp cho HLV Pochettino"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_YORO_1)], "VNEXPRESS", "FA chính thức hủy bỏ án treo giò sau thẻ đỏ gây tranh cãi của trung vệ Leny Yoro"),
            _slot("title", 0, [_url(SKY_POCH_1)], "SKY SPORTS", "Huấn luyện viên Mauricio Pochettino công khai chỉ trích dữ dội tổ trọng tài và VAR"),
            _slot("sentence", 1, [_url(SKY_YORO_FOUL)], "SKY SPORTS", "Pha va chạm giữa Leny Yoro và Alexander Isak ở phút thứ tám đã làm xoay chuyển trận đại chiến"),
            _slot("sentence", 2, [_ddgs("Howard Webb PGMOL Premier League referee")], "BING SEARCH", "Pochettino bất bình khi trưởng ban trọng tài Howard Webb vẫn bênh vực quyết định sai lầm"),
            _slot("sentence", 3, [_url(DT_POCH_1)], "DÂN TRÍ / GETTY", "Tân thuyền trưởng Manchester United đặt câu hỏi về tính công bằng của công nghệ VAR"),
            _slot("sentence", 4, [_url(DT_POCH_2)], "DÂN TRÍ / GETTY", "Với ngân sách dưới 50 triệu bảng, Pochettino phải tính toán kỹ để trục vớt Quỷ đỏ"),
        ],
    },

    # 20 (Nữ — MỸ ĐĂNG CAI COPA AMÉRICA 2028)
    {
        "id": 20,
        "art_id": "art_20",
        "group": "BÓNG ĐÁ THẾ GIỚI",
        "title": "CONMEBOL và CONCACAF chốt Mỹ đăng cai Copa América 2028 với 16 đội tuyển",
        "summary": (
            "Hai liên đoàn bóng đá Nam Mỹ và Bắc Trung Mỹ tối ngày 24 tháng 11 chính thức công bố thỏa thuận hợp tác chiến lược đưa vòng chung kết Copa América 2028 trở lại tổ chức tại Hoa Kỳ. "
            "Kỳ đại hội lần thứ 49 sẽ diễn ra từ ngày 9 tháng 6 đến ngày 9 tháng 7 năm 2028, trùng với lịch thi đấu của Euro 2028 tại châu Âu và khép lại ngay trước khi môn bóng đá Thế vận hội Los Angeles khởi tranh. "
            "Giải đấu giữ nguyên quy mô mở rộng 16 đội tuyển, bao gồm toàn bộ 10 đội bóng Nam Mỹ cùng sáu đại diện khách mời xuất sắc nhất từ khu vực Bắc Trung Mỹ thông qua thành tích tại Cúp Vàng 2027. "
            "Đây là lần thứ ba Hoa Kỳ đăng cai giải đấu lâu đời nhất thế giới sau các năm 2016 và 2024, biến nước này thành trung tâm sự kiện bóng đá toàn cầu suốt giai đoạn 2026 đến 2028."
        ),
        "source": "The Guardian / CONCACAF / ESPN",
        "news_source": "THE GUARDIAN / CONCACAF",
        "credit": "BING SEARCH",
        "stat_badges": {
            "2": {"label": "THỜI GIAN TỔ CHỨC", "value": "09/06 – 09/07/2028", "sub": "Ngay trước thềm Thế vận hội Los Angeles"},
            "3": {"label": "QUY MÔ 16 ĐỘI", "value": "10 NAM MỸ + 6 CONCACAF", "sub": "Lần thứ ba tổ chức tại Hoa Kỳ"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Copa America trophy football match stadium USA")], "BING SEARCH", "Copa América 2028 chính thức quay trở lại tổ chức tại Hoa Kỳ với 16 đội tuyển"),
            _slot("title", 0, [_ddgs("Argentina Copa America champions celebration trophy")], "BING SEARCH", "Đội tuyển Argentina đang là nhà đương kim vô địch giải đấu danh giá nhất Nam Mỹ"),
            _slot("sentence", 1, [_ddgs("MetLife Stadium USA soccer match crowd")], "BING SEARCH", "Các sân vận động hiện đại tại Mỹ tiếp tục đón nhận giải đấu lớn cấp châu lục"),
            _slot("sentence", 2, [_ddgs("CONMEBOL CONCACAF Copa America logo press")], "BING SEARCH", "Lịch thi đấu từ tháng 6 đến tháng 7 năm 2028 được sắp xếp tránh trùng Olympic Los Angeles"),
            _slot("sentence", 3, [_ddgs("CONCACAF Gold Cup national team soccer")], "BING SEARCH", "Sáu suất khách mời khu vực Bắc Trung Mỹ sẽ được phân định qua giải Gold Cup 2027"),
            _slot("sentence", 4, [_ddgs("Los Angeles Memorial Coliseum 2028 Olympics stadium")], "BING SEARCH", "Hoa Kỳ trở thành tâm điểm của hàng loạt đại hội bóng đá liên tiếp đến năm 2028"),
        ],
    },

    # 21 (Nam — THẦN ĐỒNG CỜ TƯỚNG 10 TUỔI QUÁCH ĐINH NAM GÂY ĐỊA CHẤN TRUNG QUỐC)
    {
        "id": 21,
        "art_id": "art_21",
        "group": "CỜ TƯỚNG QUỐC TẾ",
        "title": "Thần đồng cờ tướng 10 tuổi Quách Đinh Nam lập kỷ lục 70 năm lịch sử Trung Quốc",
        "summary": (
            "Giải vô địch cờ tướng cá nhân Trung Quốc 2026 diễn ra tại Trường Xuân vừa chứng kiến cơn địa chấn mang tên kỳ thủ nhí 10 tuổi Quách Đinh Nam của tỉnh Hà Bắc. "
            "Đối đầu hàng loạt đàn anh và đại kiện tướng dày dạn kinh nghiệm ở bảng 16, cậu bé sinh năm 2016 thi đấu điềm tĩnh để đạt thành tích bất bại với ba ván thắng và ba ván hòa. "
            "Kết quả này giúp Quách Đinh Nam đứng đầu bảng và trở thành kỳ thủ trẻ nhất trong suốt khoảng 70 năm lịch sử giải đấu giành quyền lọt vào nhóm 32 kỳ thủ mạnh nhất vòng loại trực tiếp. "
            "Truyền thông Trung Quốc đồng loạt ca ngợi chiến tích này là bước ngoặt thần kỳ cho thấy sức bật mạnh mẽ của thế hệ kỳ thủ trẻ nước này."
        ),
        "source": "Tuổi Trẻ / Quảng Tượng Võng",
        "news_source": "TUỔI TRẺ / QUẢNG TƯỢNG VÕNG",
        "credit": "TUỔI TRẺ / BAIDU",
        "stat_badges": {
            "2": {"label": "BẤT BẠI VÒNG BẢNG", "value": "3 THẮNG • 3 HÒA", "sub": "Đứng đầu bảng 16 giải vô địch Trung Quốc"},
            "3": {"label": "KỶ LỤC 70 NĂM", "value": "10 TUỔI VÀO TOP 32", "sub": "Kỳ thủ trẻ nhất lịch sử giải đấu"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_QUACH_1)], "TUỔI TRẺ / BAIDU", "Kỳ thủ nhí 10 tuổi Quách Đinh Nam tạo nên cú sốc lớn nhất tại giải vô địch Trung Quốc"),
            _slot("title", 0, [_ddgs("xiangqi chinese chess tournament")], "BING SEARCH", "Quách Đinh Nam đối đầu các kỳ thủ hàng đầu của làng cờ tướng Trung Quốc"),
            _slot("sentence", 1, [_url(TT_QUACH_1)], "TUỔI TRẺ / BAIDU", "Đại diện tỉnh Hà Bắc là kỳ thủ nhỏ tuổi nhất góp mặt tại giải đấu ở Trường Xuân"),
            _slot("sentence", 2, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_09_5.jpg"))], "BING SEARCH", "Chuỗi sáu ván bất bại giúp cậu bé 10 tuổi vượt qua hàng loạt đối thủ sừng sỏ"),
            _slot("sentence", 3, [_url(TT_QUACH_1)], "TUỔI TRẺ / BAIDU", "Giới chuyên môn ghi nhận Quách Đinh Nam phá sâu kỷ lục độ tuổi tồn tại gần 70 năm"),
            _slot("sentence", 4, [_local(str(ROOT / "outputs" / "24.11.2026" / "images" / "Tin_09_2.jpg"))], "BING SEARCH", "Thần đồng sinh năm 2016 được kỳ vọng sớm vươn tầm ngôi sao hàng đầu thế giới"),
        ],
    },

    # 22 (Nữ — THẦN ĐỒNG CRICKET 15 TUỔI VAIBHAV SOORYAVANSHI PHÁ KỶ LỤC THẾ GIỚI)
    {
        "id": 22,
        "art_id": "art_22",
        "group": "CRICKET THẾ GIỚI",
        "title": "Thần đồng 15 tuổi Vaibhav Sooryavanshi phá kỷ lục thế giới với 204 điểm sau 53 bóng",
        "summary": (
            "Làng thể thao thế giới ngày 24 tháng 11 ngỡ ngàng trước màn trình diễn siêu hạng của thần đồng cricket người Ấn Độ Vaibhav Sooryavanshi khi mới bước sang tuổi 15. "
            "Trong trận đấu giữa Ấn Độ A và Các Tiểu vương quốc Ả Rập Thống nhất tại Doha, tay đập tuổi teen ghi tới 204 điểm chỉ sau 53 quả giao bóng để giúp đội nhà rượt đuổi thành công mục tiêu 250 điểm trong chưa đầy 15 lượt đấu. "
            "Màn bùng nổ với kỷ lục thế giới 28 cú đánh sáu điểm giúp Sooryavanshi xô đổ hàng loạt cột mốc lịch sử gồm 100 điểm nhanh nhất sau 28 bóng và 200 điểm nhanh nhất mọi thời đại của thể thức List A. "
            "Bất chấp mới 15 tuổi, tài năng trẻ này còn vượt qua hiệu suất ghi điểm tồn tại hơn một thập kỷ của huyền thoại AB de Villiers."
        ),
        "source": "BBC Sport / The Guardian",
        "news_source": "BBC SPORT / THE GUARDIAN",
        "credit": "BBC SPORT",
        "stat_badges": {
            "2": {"label": "HIỆU SUẤT KHÔNG TƯỞNG", "value": "204 ĐIỂM / 53 BÓNG", "sub": "28 cú đánh sáu điểm kỷ lục thế giới"},
            "3": {"label": "PHÁ KỶ LỤC LIST A", "value": "100 ĐIỂM TRONG 28 BÓNG", "sub": "Cầu thủ trẻ nhất ghi cú đúp thế kỷ"},
        },
        "slots": [
            _slot("title", 0, [_url(BBC_SOORYA_1)], "BBC SPORT", "Tài năng trẻ 15 tuổi Vaibhav Sooryavanshi đi vào lịch sử môn cricket thế giới"),
            _slot("title", 0, [_url(BBC_SOORYA_2)], "BBC SPORT", "Màn trình diễn bùng nổ tại Doha giúp Ấn Độ A giành chiến thắng áp đảo"),
            _slot("sentence", 1, [_url(BBC_SOORYA_1)], "BBC SPORT", "Vaibhav Sooryavanshi gây chấn động truyền thông quốc tế ở tuổi 15"),
            _slot("sentence", 2, [_url(BBC_SOORYA_2)], "BBC SPORT", "Tay đập Ấn Độ ghi 204 điểm trong trận đấu diễn ra tại Doha, Qatar"),
            _slot("sentence", 3, [_ddgs("Vaibhav Sooryavanshi batting cricket match")], "BING SEARCH", "Kỷ lục 28 cú sáu điểm trong một lượt đánh phá sâu mọi cột mốc của các đàn anh"),
            _slot("sentence", 4, [_url(BBC_SOORYA_1)], "BBC SPORT", "Giới chuyên môn ví Sooryavanshi là hiện tượng trăm năm có một của cricket Ấn Độ"),
        ],
    },

    # 23 (Nam — KHAI MÀN CHUNG KẾT CỜ VUA THẾ GIỚI 2026: GUKESH HÒA SINDAROV)
    {
        "id": 23,
        "art_id": "art_23",
        "group": "CỜ VUA THẾ GIỚI",
        "title": "Khai màn Chung kết Cờ vua Thế giới 2026: Đương kim vô địch Gukesh thoát hiểm cầm hòa Sindarov",
        "summary": (
            "Ván đấu mở màn trận Chung kết Cờ vua Thế giới 2026 giữa đương kim vô địch Gukesh Dommaraju và người thách đấu Javokhir Sindarov vừa khép lại vào tối ngày 24 tháng 11 tại Geneva, Thụy Sĩ. "
            "Đây là cặp đấu tranh ngôi vương trẻ nhất lịch sử cờ vua khi cả đại diện Ấn Độ lẫn kỳ thủ Uzbekistan đều mới tròn 20 tuổi. "
            "Cầm quân đen chọn khai cuộc phòng thủ Berlin, Gukesh trải qua thử thách cực đại về mặt thời gian khi suy nghĩ hơn 36 phút chỉ cho một nước đi và rơi vào cảnh cạn giờ sớm hơn đối thủ rất nhiều. "
            "Dẫu vậy, bản lĩnh tính toán chuẩn xác đã giúp nhà đương kim vô địch hóa giải sức ép, đưa thế cờ về tàn cuộc cân bằng và buộc Sindarov chấp nhận bắt tay chia điểm sau 38 nước đi."
        ),
        "source": "The Guardian / FIDE / ChessBase",
        "news_source": "THE GUARDIAN / FIDE",
        "credit": "BING SEARCH",
        "stat_badges": {
            "2": {"label": "CẶP ĐẤU TRẺ NHẤT", "value": "GUKESH VS SINDAROV", "sub": "Hai kỳ thủ cùng 20 tuổi tranh ngôi vương"},
            "4": {"label": "VÁN 1 TẠI GENEVA", "value": "HÒA SAU 38 NƯỚC", "sub": "Gukesh mất 36 phút cho 1 nước vẫn giữ vững thế trận"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Gukesh Dommaraju world chess championship FIDE")], "BING SEARCH", "Đương kim vô địch thế giới Gukesh Dommaraju bước vào ván khai màn tại Thụy Sĩ"),
            _slot("title", 0, [_ddgs("Javokhir Sindarov chess grandmaster FIDE")], "BING SEARCH", "Thách đấu 20 tuổi Javokhir Sindarov cầm quân trắng tạo áp lực thời gian lớn"),
            _slot("sentence", 1, [_ddgs("FIDE World Chess Championship match board hall")], "BING SEARCH", "Trận chung kết thế giới 2026 thu hút sự theo dõi của cộng đồng cờ vua toàn cầu"),
            _slot("sentence", 2, [_ddgs("Gukesh Dommaraju chess thinking board")], "BING SEARCH", "Cuộc đối đầu giữa hai ngôi sao 20 tuổi đánh dấu kỷ nguyên mới của cờ vua đỉnh cao"),
            _slot("sentence", 3, [_ddgs("Javokhir Sindarov chess tournament")], "BING SEARCH", "Gukesh phải dành tới 36 phút suy tính ở giai đoạn trung cuộc đầy biến ảo"),
            _slot("sentence", 4, [_ddgs("FIDE World Chess Championship board pieces")], "BING SEARCH", "Hai kỳ thủ bắt tay hòa sau 38 nước trước khi bước tiếp vào các ván đấu tiếp theo"),
        ],
    },

    # 24 (100% Giọng Nữ — MỤC TIN VẮN CUỐI VIDEO: CÁC TIN THỂ THAO KHÁC)
    {
        "id": 24,
        "art_id": "art_24",
        "group": "CÁC TIN THỂ THAO KHÁC",
        "title": "Điểm nhanh các tin thể thao đáng chú ý khác",
        "voice_preset": "secondary",
        "summary": (
            "Tại giải bóng đá nhà nghề Mỹ, truyền thông cho biết Lionel Messi nhiều khả năng chỉ bị phạt tiền chứ không bị treo giò sau vụ ném bóng vào mặt Gonzalo Tapia, giúp anh đủ điều kiện cùng Inter Miami đá lượt về sống còn với Columbus Crew ngày 28 tháng 11. "
            "Tại Anh, đội nữ Crystal Palace bị trừ ba điểm và rơi xuống hạng 13 vì dùng tới bốn lượt thay người ở trận thắng Everton, trong khi Chủ tịch Liên đoàn Bóng đá Anh Debbie Hewitt phải ký thỏa thuận bảo mật mới được xem tài liệu mật bán quyền World Cup của Chủ tịch FIFA Gianni Infantino giữa lúc ông bị soi dùng 39 chuyến chuyên cơ trong 115 ngày. "
            "Ở môn golf, Rory McIlroy bất ngờ trượt danh sách năm ứng viên Cầu thủ xuất sắc nhất năm của PGA Tour dù bảo vệ thành công chức vô địch The Masters. "
            "Trên các đấu trường khác, tuyển cricket Anh đè bẹp Úc trong 13,1 lượt ném nhờ công Aneurin Donald và Phil Salt, còn đội trưởng rugby Ireland Dan Sheehan bị treo giò hai trận lỡ đại chiến gặp đội tuyển Úc. "
            "Tại đấu trường quốc nội và mạng xã hội, môn điền kinh Đại hội Thể thao toàn quốc chính thức khởi tranh hôm nay 25 tháng 11, futsal Thành phố Hồ Chí Minh toàn thắng vòng bảng vào bán kết, võ cổ truyền bỏ giáp mở đòn chỏ gối, ghe nữ Tum Núp lần thứ tư vô địch đua ghe ngo Cần Thơ, còn YouTuber IShowSpeed gây sốt khi chạy 100 mét hết 10,352 giây trước mắt Usain Bolt, suýt chạm kỷ lục quốc gia Việt Nam."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / BBC Sport / Sky Sports",
        "news_source": "ĐIỂM ĐỌC TỔNG HỢP",
        "credit": "THANH NIÊN / TUỔI TRẺ / BBC / SKY SPORTS",
        "stat_badges": {
            "1": {"label": "TIN MỚI MLS", "value": "MESSI KHÔNG BỊ TREO GIÒ", "sub": "Kịp đá lượt về ngày 28/11 với Columbus Crew"},
            "2": {"label": "HẬU TRƯỜNG BÓNG ĐÁ ANH", "value": "PALACE BỊ TRỪ 3 ĐIỂM", "sub": "Chủ tịch FA ký NDA xem hồ sơ mật FIFA"},
            "5": {"label": "ĐẠI HỘI & VIRAL", "value": "ĐIỀN KINH KHỞI TRANH", "sub": "IShowSpeed chạy 100m hết 10,352 giây"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_MESSI_MLS)], "THANH NIÊN", "Lionel Messi nhiều khả năng tránh được án treo giò trước trận lượt về ngày 28 tháng 11"),
            _slot("title", 0, [_url(BBC_INF_JET)], "BBC SPORT", "Chủ tịch FIFA Gianni Infantino đối mặt nhiều câu hỏi về 39 chuyến chuyên cơ và đề án mật"),
            _slot("title", 0, [_url(TT_SPEED_1)], "TUỔI TRẺ / TGCOM24", "YouTuber IShowSpeed gây ngỡ ngàng khi chạy 100 mét sát kỷ lục quốc gia Việt Nam"),
            # Câu 1: Messi MLS
            _slot("sentence", 1, [_url(TN_MESSI_MLS)], "THANH NIÊN", "Inter Miami thở phào khi đội trưởng Messi có thể góp mặt ở trận lượt về play-off MLS"),
            # Câu 2: Palace nữ & FIFA NDA
            _slot("sentence", 2, [_url(BBC_INF_JET)], "BBC SPORT", "Sếp bóng đá Anh Debbie Hewitt bị ràng buộc bảo mật khi kiểm tra hồ sơ thương mại của FIFA"),
            _slot("sentence", 2, [_ddgs("Crystal Palace Women football WSL match")], "BING SEARCH", "Đội nữ Crystal Palace rơi xuống nhóm nguy hiểm sau án trừ ba điểm từ ban tổ chức"),
            # Câu 3: Rory McIlroy
            _slot("sentence", 3, [_url(SKY_MCILROY)], "SKY SPORTS", "Rory McIlroy vắng mặt đáng tiếc trong danh sách rút gọn giải thưởng PGA Tour năm 2026"),
            # Câu 4: Cricket & Rugby
            _slot("sentence", 4, [_ddgs("England Australia T20 cricket match 2026")], "BING SEARCH", "Aneurin Donald và Phil Salt giúp tuyển cricket Anh nghiền nát Úc chỉ sau 13,1 lượt đấu"),
            _slot("sentence", 4, [_url(SKY_RUGBY_SHEEHAN)], "SKY SPORTS", "Đội trưởng tuyển rugby Ireland Dan Sheehan bị cấm thi đấu hai trận sau pha phạm lỗi"),
            # Câu 5: Điền kinh, Futsal, Võ cổ truyền, Ghe ngo, IShowSpeed
            _slot("sentence", 5, [_url(TT_ATH_OANH)], "TUỔI TRẺ", "Nguyễn Thị Oanh cùng các ngôi sao điền kinh bước vào tranh tài từ ngày 25 tháng 11"),
            _slot("sentence", 5, [_url(TT_FUTSAL_1)], "TUỔI TRẺ", "Futsal Thành phố Hồ Chí Minh toàn thắng cả ba trận vòng bảng để hiên ngang vào bán kết"),
            _slot("sentence", 5, [_url(TN_VO_CT)], "THANH NIÊN", "Thể thức võ cổ truyền bỏ giáp và mở đòn chỏ gối tạo sức hút lớn trên sàn đài Đại hội"),
            _slot("sentence", 5, [_url(TT_GHE_NGO)], "TUỔI TRẺ / KHẮC TÂM", "Đội ghe nữ Tum Núp khẳng định vị thế với bốn lần liên tiếp vô địch đua ghe ngo Cần Thơ"),
            _slot("sentence", 5, [_url(TT_SPEED_1)], "TUỔI TRẺ / TGCOM24", "Cú chạy 10,352 giây của IShowSpeed khiến huyền thoại Usain Bolt phải trầm trồ thán phục"),
        ],
    },
]
