# -*- coding: utf-8 -*-
"""
daily_21_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 21.11.2026
(Tổng hợp tin tức từ 12:00 ngày 20.11 đến 08:15 ngày 21.11.2026).
Cấu trúc:
  - Intro (00): Song giọng Nữ (Ngọc Huyền #14) & Nam (Minh Quân Pro #15), hide_title=True
  - 19 bản tin chính (01–19): Mỗi tin 1 vấn đề trọng tâm (4–6 câu), luân phiên Nam / Nữ
  - Mục 20 (CÁC TIN THỂ THAO KHÁC): 100% Giọng Nữ (Ngọc Huyền #14), đọc nhanh 9 tin bên lề trước Outro
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent
DAILY_20 = ROOT / "outputs" / "20.11.2026" / "images"
DAILY_19 = ROOT / "outputs" / "19.11.2026" / "images"
DAILY_18 = ROOT / "outputs" / "18.11.2026" / "images"
DAILY_16 = ROOT / "outputs" / "16.11.2026" / "images"
DAILY_02 = ROOT / "outputs" / "02.11.2026" / "images"
ORTHER_14 = ROOT / "outputs" / "Orther" / "14.11.2026" / "images"
ORTHER_12 = ROOT / "outputs" / "Orther" / "12.11.2026" / "images"
ORTHER_10 = ROOT / "outputs" / "Orther" / "10.11.2026" / "images"
ORTHER_08 = ROOT / "outputs" / "Orther" / "08.11.2026" / "images"
ORTHER_05 = ROOT / "outputs" / "Orther" / "05.11.2026" / "images"


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


# ── URL ảnh báo chí gốc 20–21.11.2026 (sạch logo/watermark) ──
# U17 Việt Nam 2-3 U17 Bỉ
TN_U17_SYBACH_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/img17951805073731795181994940-2048x1236-1795191916613578954624.jpg"
TN_U17_SYBACH_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/9182332991873250944007900605216454588938566n-2-1795194241168245394833.jpg"
TN_U17_SYBACH_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/9182332991873250944007900605216454588938566n-1795189101499785821307.jpg"
TN_U17_SYBACH_4 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/u17-vietnam-u17-bi-1-17951867067841947929001.jpg"
TN_U17_NGLUC_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/u17-vn-17951890616671726700154.jpg"
TN_U17_NGLUC_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/91685630111859341139623571054268814634611042n-1795188826284988715097.jpg"
TN_U17_TEAM_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/0f1e6706-df5e-48a5-af0d-99d197070b0cpng-17951920322622013019681.jpg"
TN_U17_TEAM_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/91379570111859341706290186349847934012411751n-17951887897511785182697.jpg"
TN_U17_TEAM_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/17951821443554977336025469002040g22640386832928284801055cb021f3f903adfcf13e18a6131f4-1795188880988851919264.jpg"
TN_U17_MATCH_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/u17-vietnam-u17-bi-3-1795186706850487025400.jpg"
TN_U17_MATCH_4 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/u17-vietnam-u17-bi-4-17951867068851067163162.jpg"
TN_U17_MATCH_5 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/u17-vietnam-u17-bi-5-17951867069101866818322.jpg"
TN_U17_MATCH_6 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/u17-vietnam-u17-bi-6-1795186706939320601046.jpg"
TN_U17_AFC = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/cab3c9fd-15b8-47d2-8525-8cbd3369f99epng-17952038787281844609032.jpg"
TN_U17_ROLAND = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/17951906365484977336025469002040g16272974396902930965392106ed39310bf1054a31d3679f7-1795190857291338414521.jpg"
VNE_U17_1 = "https://i1-thethao.vnecdn.net/2026/11/20/IMG-6607-1795189760.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=hDuGEetlXZDou5vIiDs9nA"
VNE_U17_2 = "https://i1-thethao.vnecdn.net/2026/11/20/IMG-6591_1795181026-1795182346.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=9Sur6aUL5p1GDNjUlQcNYg"
VNE_U17_3 = "https://i1-thethao.vnecdn.net/2026/11/20/IMG-6577_1795181025-1795181648.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=XcD4RoRTcE_3VrMC49DslA"
VNE_U17_4 = "https://i1-thethao.vnecdn.net/2026/11/20/IMG-6583_1795181025-1795182347.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=unxqCHtvwbUVsY1-brrg4g"
VNE_U17_5 = "https://i1-thethao.vnecdn.net/2026/11/20/IMG-6638-1795189758.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=zX142e-Br8bOqR6x4imVeg"
VNE_U17_6 = "https://i1-thethao.vnecdn.net/2026/11/20/IMG-6651-1795189758.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=QwIHWYe0hyD2oqB0Tb5HRg"
VNE_U17_7 = "https://i1-thethao.vnecdn.net/2026/11/20/IMG-6618-1795189759.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=RV5-K3krTafo1_1a_cDPLA"
VNE_U17_ROL = "https://i1-thethao.vnecdn.net/2026/11/20/img-1795192528-6423-1795192706.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=wlkiWADK2ZrIAE3QU37PLA"
DT_U17_ASEAN = "https://cdnphoto.dantri.com.vn/oC8EcWvciwrWzbga_BwkFEI_aFY=/thumb_w/1020/2026/11/20/u17vn5aseanfootball20-11-26-1795187374927.jpeg"
DT_U17_CELEB = "https://cdnphoto.dantri.com.vn/oPkfF0rDkpFqgjTc35Y_8aqp7QQ=/thumb_w/1020/2026/11/20/u17-viet-nam-5-1795180913336-1795182922021.jpg"
DT_U17_GETTY = "https://cdnphoto.dantri.com.vn/QuyWbLnyZnJ108TgDXUQ3ra5ZGE=/thumb_w/1020/2026/11/20/u17-viet-nam-8-1795183706660.jpg"
DT_U17_NGLUC = "https://cdnphoto.dantri.com.vn/O4qE0waUGk9M2WtUfRaa-F5Qfu8=/thumb_w/1020/2026/11/20/rrr-1795187897008.png"
DT_VFS_1 = "https://cdnphoto.dantri.com.vn/dU_uugRy6OWEqCV1nosKt4WS7s8=/thumb_w/1020/2026/11/20/u17vn220-11-26-1795187372854.jpg"
DT_VFS_2 = "https://cdnphoto.dantri.com.vn/t5sjZboXrEg83u4Pb-yBuON3ff0=/thumb_w/1020/2026/11/20/u17vn120-11-26-1795187372407.jpg"
DT_REF_1 = "https://cdnphoto.dantri.com.vn/GBNrbL6wvCp_I8mSjcz-JWmNnyY=/thumb_w/1020/2026/11/20/img1118-2011144140-1795169519123.webp"
DT_REF_2 = "https://cdnphoto.dantri.com.vn/siuH26RJc8FI1VLfRi6syVw1jBk=/thumb_w/1020/2026/11/20/nu-trong-tai-xinh-dep-bat-chinh-tran-ra-quan-cua-u17-viet-nam-o-world-cup-edited-1795169604395.jpg"
DT_REF_3 = "https://cdnphoto.dantri.com.vn/BolBKMt4B0sKGyjqCCpZoB4WxeQ=/thumb_w/1020/2026/11/20/u17tructiep-1795170699127.jpg"
TT_REF_GOAL = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/daiane-muniz-2-17951437998191606601788.jpg"
TT_U17_MALI = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/u17-mali-edit-1795192407122971223856.png"
DT_U17_MALI_2 = "https://cdnphoto.dantri.com.vn/RF5GIksHA_AHF7Q_saQO9oFiGh0=/thumb_w/1020/2026/11/20/91483153723201931521582854700273240670061960n-edited-1795189218995.jpg"
TT_U17_NZ = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/3ik4h4dc0zs5rbxgf2msapjlfsipa34bx8spugbr1ylik3xodfgcwibwaklft6o81hvdwz2dohx-cnedaxhwmdi07hkqjii0dvfkntrokcagc-0qh9rlqpaiejqgcd6jk92tjqicns3va6b-1795188012867161607749.jpg"
TT_U17_FIFA = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/u17-viet-nam-bi-1-17951873624791321336690.jpg"
TT_U17_THAI = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/u17-thai-lan-edit-17951862011721583065673.jpg"
VNE_U17_THAI = "https://i1-thethao.vnecdn.net/2026/11/20/u17-tha-i-lan-1795193801-4181-1795193909.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=efMxdJuwQY4J7EGwhhHzWA"
TT_U17_VN_AFC = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/13/u17-viet-nam-an-mung-1794564681460259032126.jpg"

# V-League vòng 8 & Hạng Nhất
TN_VL_TH_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/v-league-17951859332811492298672.jpg"
TN_VL_TH_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/thanh-hoa-1795177648776789000898.jpeg"
TT_VL_DAMOTH = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/4/19/thanh-hoa-1776603513347744428616.jpeg"
TT_VL_KIM = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/kim-17951798323071418489796.jpg"
TN_VL_TC_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/65774-17951823738431472131100.jpg"
TN_VL_TC_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/65773-17951823738732109240587.jpg"
TN_VL_TC_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/65776-17951827964242036249230.jpg"
TT_VL_SLNA_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/base64-17951867636361012540772.jpeg"
TT_VL_SLNA_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/base64-17951867636541910502074.jpeg"

# Cờ vua & Cờ tướng
TN_QUANGLIEM = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/911709157182152695943682421459038209837518572n-1795213948552941106021.jpg"
TT_PHANHUYHOANG = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/edit-edit-phan-huy-hoang-co-tuong-1-17951863036061758366393.jpeg"

# Đại hội Thể thao toàn quốc 2026
TN_DH_KHAIMAC = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/le-khai-mac-17951890616212047993316.jpg"
TN_DH_VOVINAM = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/17950776434764359474416865369463g782008143832193140651e2b39800d4e11066a6f9065a0fabb9-17951646170371437612101.jpg"
TT_DH_CANOEING = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/nguyen-thi-huong-edit-rotate-1795174184313651163707.jpg"
TT_DH_JUDO_HCM = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/le-anh-tai-judo-tphcm-17951908451391279071782.jpg"
TT_DH_JUDO_QD = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/judo-quan-doi-hcv-1795191146911523087151.jpg"

# P Esports
TT_PESPORTS = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/p-esports-vietnam-freefire-1795181824635761939501.jpg"

# Quốc tế: Ronaldo, Mourinho, Nations League, Hàn Quốc, Man City, Messi
TN_CR7_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/ronaldo-17952193360321165388076.jpg"
TN_CR7_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/ronaldo--1795219336004611699509.jpg"
VNE_CR7_1 = "https://i1-thethao.vnecdn.net/2026/11/21/ronaldo-jpeg-1795212909-9140-1795212913.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=E89b3i4Vyskokb9Y2w-58g"
VNE_CR7_GOAL = "https://iv1.vnecdn.net/thethao/images/web/2026/11/21/ronaldo-ghi-ban-trong-tran-thua-al-ahli-1795212845.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=Eg2alevNXeY6k8X3S7wxyA"
VNE_CR7_MISS = "https://iv1.vnecdn.net/thethao/images/web/2026/11/21/ronaldo-da-hong-phat-den-1795212891.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=4uhADwmn2wtp1eFWx6q66g"
TT_CR7_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/21/ronaldo-21112026-17952214854191231442276.jpeg"
VNE_MOU_PRESS = "https://i1-thethao.vnecdn.net/2026/11/20/mourinho-jpeg-1795191821-2444-1795192616.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=uRzpBzIJoeCLzANiqPczCA"
VNE_NL_ESP_FRA = "https://i1-thethao.vnecdn.net/2026/11/21/Yamal-Barcola-9236-1795195590.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=pDWk8mY5OElIjev5Xe5b-w"
VNE_NL_NOR_ENG = "https://i1-thethao.vnecdn.net/2026/11/21/AFP-20260711-B9XK4F8-v2-HighRe-8894-9912-1795195591.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=XMQIGtg83XLT-aEWsaRIIg"
VNE_NL_POR = "https://i1-thethao.vnecdn.net/2026/11/21/AP26321732831006-1920-1795195591.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=_33mnxoH6HBDT_3oX91mrw"
TT_NL_POR = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/7/6/z8015135419782715b1c2d72401aa759fa49a9b3b1fd60-17833760681641218287113.jpg"
TT_KFA_SON = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/6/25/son-heung-min-1-1782360477367375355875.jpeg"
TT_KFA_LEE = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/lnn6ogbbw4nevdlqrcrptktslpfzgv8vl1oe9xeo8ydlzblddhwwvnrijnsgdwf8vvdhuxsyjzn54dw65vxvtk9xbrflwm-wmuojvg37p2e41r7kw7crdih8lr407v8c4kkmdqf7cbxqjm-17951732345011437016399.jpg"
TT_KFA_PARK = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/7/5/ahn-jung-hwan-park-ji-sung-4-17832288826002127030067.jpg"
VNE_MC_MASTERS = "https://i1-thethao.vnecdn.net/2026/11/20/d0a2cb9f-df67-42b8-ad66-69d489-1999-5060-1795144610.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=l3w6nO6v6Wt4kuYIpp3FKA"
VNE_MC_OWNERS = "https://i1-thethao.vnecdn.net/2026/11/20/0776c911-d6c6-469e-a651-c95435-9231-6673-1795144610.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=StbmzYhR_b5eiKG_7uFh4A"
VNE_MC_ETIHAD = "https://i1-thethao.vnecdn.net/2026/11/20/8342a40e-ba96-4212-ab6a-085636-2697-7974-1795144610.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=Ljvrj3QrFJYk0illHRP5yQ"
VNE_MESSI_1 = "https://i1-thethao.vnecdn.net/2026/11/20/messi-1795110789-1856-1795111985.webp?w=1020&h=0&q=100&dpr=1&fit=crop&s=mav0vVuqCNntUbokaHtvkg"

# Các tin thể thao khác (bên lề)
TN_U17_ESP_CHN = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/5a091733-5fc8-4493-b1ee-93a83f724972png-1795190264057626392989.jpg"
TN_U17_TAJ_CUB = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/cd00a91a-48f3-4e3d-8c63-e97996bd1c5fpng-17951903977841622959561.jpg"
TT_U17_ESP_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/u17-tay-ban-nha-edit-17951925995851321461459.png"
TN_U17_GK_SON = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/thu-mon-thai-son-1795162047476465403244.jpg"
TT_U17_BI_COACH = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/u17-bi3-hlv-17951655774411980987117.jpg"
TT_HCM_FIRSTDIV = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/91396345115413344778250626053780257557978643n-1795186573486479019992.jpeg"
TN_DONGNAI_CP = "https://images2.thanhnien.vn/528068263637045248/2026/10/22/cong-phuong-01-tpdn-1792650099713605292842.jpeg"
TN_PICKLE_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/20/kt5a9025-17951794033191720665782.jpg"
TT_MCV_SIGN = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/cuc-the-duc-the-thao-mcv-sport-179515934581491724355.jpg"
VNE_WENGER_1 = "https://i1-thethao.vnecdn.net/2026/11/20/7c570502-ffcc-44b5-a2c8-e01364-7877-5419-1795160324.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=bD99rlq6YmK-gE9v4RwNUg"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 21.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 21 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất trên sân cỏ trong nước và đấu trường quốc tế. "
        "Ở tâm điểm bóng đá trẻ thế giới, đội tuyển U17 Việt Nam dù thua sát nút U17 Bỉ 2-3 ở trận ra quân World Cup tại Qatar nhưng đã khiến FIFA, AFC và truyền thông Bỉ ngỡ ngàng bằng hai siêu phẩm lịch sử của Lê Sỹ Bách và Chu Ngọc Nguyễn Lực. "
        "Trên bình diện quốc tế, Cristiano Ronaldo chạm mốc 986 bàn thắng nhưng sút hỏng phạt đền khiến Al Nassr thua ngược Al Ahli 1-3, Jose Mourinho đột ngột rời phòng họp báo Real Madrid, còn Harry Kane dính chấn thương cổ chân nặng khiến Bayern Munich lo sốt vó sau trận hòa Cologne 1-1. "
        "Cùng màn phá dớp tám năm của Thanh Hóa trước Hoàng Anh Gia Lai ở V-League, tiền thưởng 800 triệu đồng của Lê Quang Liêm, không khí trước giờ khai mạc Đại hội Thể thao toàn quốc 2026 và mục điểm nhanh các tin thể thao đáng chú ý khác ngay sau đây."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí",
    "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
    "credit": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 21 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất trên sân cỏ trong nước và đấu trường quốc tế.",
        },
        {
            "voice_preset": "primary",
            "text": "Ở tâm điểm bóng đá trẻ thế giới, đội tuyển U17 Việt Nam dù thua sát nút U17 Bỉ 2-3 ở trận ra quân World Cup tại Qatar nhưng đã khiến FIFA, AFC và truyền thông Bỉ ngỡ ngàng bằng hai siêu phẩm lịch sử của Lê Sỹ Bách và Chu Ngọc Nguyễn Lực.",
        },
        {
            "voice_preset": "secondary",
            "text": "Trên bình diện quốc tế, Cristiano Ronaldo chạm mốc 986 bàn thắng nhưng sút hỏng phạt đền khiến Al Nassr thua ngược Al Ahli 1-3, Jose Mourinho đột ngột rời phòng họp báo Real Madrid, còn Harry Kane dính chấn thương cổ chân nặng khiến Bayern Munich lo sốt vó sau trận hòa Cologne 1-1.",
        },
        {
            "voice_preset": "primary",
            "text": "Cùng màn phá dớp tám năm của Thanh Hóa trước Hoàng Anh Gia Lai ở V-League, tiền thưởng 800 triệu đồng của Lê Quang Liêm, không khí trước giờ khai mạc Đại hội Thể thao toàn quốc 2026 và mục điểm nhanh các tin thể thao đáng chú ý khác ngay sau đây.",
        },
    ],
    "stat_badges": {
        "1": {"label": "BẢN TIN NGÀY", "value": "21.11.2026", "sub": "20 chuyên mục chọn lọc"},
        "2": {"label": "U17 WORLD CUP", "value": "VN 2-3 BỈ", "sub": "2 siêu phẩm lịch sử tại Qatar"},
        "3": {"label": "SAUDI PRO LEAGUE", "value": "986 BÀN", "sub": "Ronaldo ghi bàn rồi hỏng 11m"},
    },
    "slots": [
        # Câu 1 (4 ảnh)
        _slot("sentence", 1, [_url(TN_U17_SYBACH_1)], "THANH NIÊN / VFF", "Lê Sỹ Bách ghi bàn thắng đầu tiên của Việt Nam tại U17 World Cup"),
        _slot("sentence", 1, [_url(VNE_U17_1)], "VNEXPRESS", "Các cầu thủ U17 Việt Nam chiến đấu kiên cường trước á quân châu Âu"),
        _slot("sentence", 1, [_url(TN_CR7_1)], "THANH NIÊN / REUTERS", "Cristiano Ronaldo ghi bàn thứ 986 trong trận đấu trên sân Al Ahli"),
        _slot("sentence", 1, [_url(TN_DH_KHAIMAC)], "THANH NIÊN / XUÂN CƯỜNG", "Thành phố Hồ Chí Minh sẵn sàng cho đêm khai mạc Đại hội Thể thao toàn quốc"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(TN_U17_SYBACH_2)], "THANH NIÊN / VFF", "Pha đánh gót ngẫu hứng ngay phút thứ tư của Lê Sỹ Bách"),
        _slot("sentence", 2, [_url(TN_U17_NGLUC_1)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực sút thẳng phạt góc ghi siêu phẩm phút 84"),
        _slot("sentence", 2, [_url(VNE_U17_2)], "VNEXPRESS", "Cầu thủ hai đội tranh chấp quyết liệt trên sân bóng Học viện Aspire"),
        _slot("sentence", 2, [_url(VNE_U17_ROL)], "VNEXPRESS / ĐOÀN CA", "HLV Cristiano Roland tự hào về màn chào sân World Cup của học trò"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url("https://f.rpp-noticias.io/2026/11/20/340334_1931342.jpg?width=860&quality=60")], "RPP / REUTERS", "Ronaldo đá phạt đền trúng cột dọc khiến Al Nassr đánh rơi lợi thế"),
        _slot("sentence", 3, [_url(VNE_MOU_PRESS)], "VNEXPRESS / FOOTBALLTWEET", "HLV Jose Mourinho đột ngột rời họp báo khi bị hỏi về Ronaldo"),
        _slot("sentence", 3, [_local(DAILY_02 / "Tin_01_8.jpg")], "REUTERS", "Tiền đạo Harry Kane của Bayern Munich gặp chấn thương cổ chân nghiêm trọng"),
        _slot("sentence", 3, [_url(VNE_NL_ESP_FRA)], "VNEXPRESS / AP", "Tây Ban Nha gặp Pháp ở tứ kết UEFA Nations League 2026-2027"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_url(TN_VL_TH_1)], "THANH NIÊN / CLB THANH HÓA", "Thanh Hóa đánh bại HAGL 2-1 để chấm dứt chuỗi tám năm không thắng"),
        _slot("sentence", 4, [_url(TN_QUANGLIEM)], "THANH NIÊN / TOTAL CHESS", "Lê Quang Liêm cán đích hạng tám giải cờ vua toàn năng thế giới"),
        _slot("sentence", 4, [_url(TN_DH_VOVINAM)], "THANH NIÊN / VOVINAM TP", "Đoàn thể thao TP.HCM bứt phá dẫn đầu nhờ tám huy chương vàng Vovinam"),
        _slot("sentence", 4, [_url(TT_PESPORTS)], "TUỔI TRẺ / P ESPORTS", "Đội tuyển P Esports Việt Nam giành vé sớm vào chung kết thế giới"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — U17 WORLD CUP 2026)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Việt Nam thua sát nút U17 Bỉ 2-3 với hai siêu phẩm lịch sử của Sỹ Bách và Nguyễn Lực",
        "summary": (
            "Tối ngày 20 tháng 11 tại Qatar ở lượt trận mở màn bảng G Vòng chung kết U17 World Cup 2026, đội tuyển U17 Việt Nam dù chịu thất bại sát nút 2-3 trước đương kim á quân châu Âu U17 Bỉ nhưng đã tạo nên dấu mốc lịch sử không thể quên. "
            "Ngay phút thứ tư từ quả phạt góc bên cánh trái của Nguyễn Minh Thủy, tiền đạo Lê Sỹ Bách thực hiện cú đánh gót ngẫu hứng đưa bóng găm thẳng vào góc cao khung thành, ghi bàn thắng đầu tiên cho bóng đá Việt Nam tại một kỳ World Cup sân 11 người. "
            "Sau trận đấu, Sỹ Bách thật thà tiết lộ ý đồ ban đầu chỉ muốn đánh gót đưa bóng về phía cột dọc để đồng đội băng vào tranh chấp bóng hai, không ngờ lại trở thành tuyệt tác để đời. "
            "Bị dẫn bàn sớm, U17 Bỉ vùng lên ghi liền ba bàn nhờ công Tinus Moorthamer ở phút 39, Kiyan Achahbar phút 42 và Philips phút 60, trước khi tiền vệ Chu Ngọc Nguyễn Lực tỏa sáng ở phút 84 bằng cú sút phạt góc xoáy thẳng vào lưới rút ngắn tỷ số xuống 2-3."
        ),
        "source": "Thanh Niên / VnExpress / Dân Trí",
        "news_source": "THANH NIÊN / VNEXPRESS / DÂN TRÍ",
        "credit": "THANH NIÊN / VFF",
        "stat_badges": {
            "2": {"label": "CỘT MỐC LỊCH SỬ", "value": "PHÚT 04", "sub": "Lê Sỹ Bách đánh gót mở tỷ số"},
            "4": {"label": "SIÊU PHẨM THỨ HAI", "value": "PHÚT 84", "sub": "Nguyễn Lực sút thẳng phạt góc"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_U17_SYBACH_1)], "THANH NIÊN / VFF", "Lê Sỹ Bách ăn mừng bàn thắng lịch sử vào lưới U17 Bỉ"),
            _slot("title", 0, [_url(VNE_U17_1)], "VNEXPRESS", "Các cầu thủ U17 Việt Nam quyết tâm đưa bóng nhập cuộc nhanh sau bàn rút ngắn"),
            _slot("title", 0, [_url(TN_U17_NGLUC_1)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực lập siêu phẩm từ chấm đá phạt góc phút 84"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TN_U17_TEAM_1)], "THANH NIÊN / VFF", "Đội tuyển U17 Việt Nam chơi sòng phẳng trước đương kim á quân châu Âu"),
            _slot("sentence", 1, [_url(TN_U17_MATCH_4)], "THANH NIÊN / HƯƠNG NGUYỄN", "Thế trận tự tin của các học trò HLV Cristiano Roland tại Qatar"),
            _slot("sentence", 1, [_url(TN_U17_MATCH_6)], "THANH NIÊN / HƯƠNG NGUYỄN", "Những pha tranh chấp quyết liệt giữa hai đội trên sân Học viện Aspire"),
            # Câu 2 (4 ảnh)
            _slot("sentence", 2, [_url(TN_U17_SYBACH_2)], "THANH NIÊN / VFF", "Khoảnh khắc Lê Sỹ Bách xoay người đánh gót làm bó tay thủ môn Bỉ"),
            _slot("sentence", 2, [_url(DT_U17_CELEB)], "DÂN TRÍ / VFF", "Niềm vui vỡ òa của các tuyển thủ trẻ sau bàn mở tỷ số phút thứ tư"),
            _slot("sentence", 2, [_url(VNE_U17_4)], "VNEXPRESS", "Đây là pha lập công đầu tiên của bóng đá Việt Nam ở World Cup 11 người"),
            _slot("sentence", 2, [_url(VNE_U17_5)], "VNEXPRESS", "U17 Việt Nam tạo địa chấn ngay đầu trận đấu bảng G"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(TN_U17_SYBACH_4)], "THANH NIÊN / HƯƠNG NGUYỄN", "Sỹ Bách chia sẻ ban đầu chỉ định đánh gót hướng bóng cho đồng đội"),
            _slot("sentence", 3, [_url(VNE_U17_7)], "VNEXPRESS", "Tiền đạo số 20 dành tặng bàn thắng lịch sử cho người hâm mộ Việt Nam"),
            _slot("sentence", 3, [_url(VNE_U17_ROL)], "VNEXPRESS / ĐOÀN CA", "Sự gắn kết trong các tình huống cố định mà ban huấn luyện đã chuẩn bị"),
            # Câu 4 (4 ảnh)
            _slot("sentence", 4, [_url(DT_U17_GETTY)], "DÂN TRÍ / GETTY", "U17 Bỉ tận dụng lợi thế thể hình để lật ngược thế trận dẫn 3-1"),
            _slot("sentence", 4, [_url(TN_U17_NGLUC_1)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực tỏa sáng rực rỡ với bàn thắng trực tiếp từ góc sân"),
            _slot("sentence", 4, [_url(TN_U17_NGLUC_2)], "THANH NIÊN / VFF", "Cú đá phạt góc táo bạo ở phút 84 khiến hàng thủ Bỉ sững sờ"),
            _slot("sentence", 4, [_url(VNE_U17_6)], "VNEXPRESS", "Những phút cuối nghẹt thở khi U17 Việt Nam dồn ép tìm bàn gỡ hòa"),
        ],
    },

    # 02 (Nữ — U17 WORLD CUP 2026)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "U17 WORLD CUP 2026",
        "title": "FIFA, AFC và truyền thông Bỉ thán phục hai siêu phẩm của U17 Việt Nam",
        "summary": (
            "Ngay sau tiếng còi mãn cuộc tại Doha, màn trình diễn quả cảm cùng hai bàn thắng mãn nhãn của U17 Việt Nam lập tức phủ sóng truyền thông bóng đá quốc tế. "
            "Trang chủ Liên đoàn Bóng đá Thế giới FIFA và Liên đoàn Bóng đá Châu Á AFC đều dành lời khen đặc biệt cho pha đánh gót ngẫu hứng của Lê Sỹ Bách lẫn cú đá phạt góc chuẩn xác của Chu Ngọc Nguyễn Lực. "
            "Tờ báo lớn Het Laatste Nieuws của Bỉ gọi chiến thắng 3-2 của đội nhà là màn khởi đầu đầy thót tim và thừa nhận thủ thành Mattis Seghers đã phải vào lưới nhặt bóng trước hai ứng cử viên sáng giá cho danh hiệu bàn thắng đẹp nhất giải. "
            "Tại khu vực Đông Nam Á, báo chí Thái Lan và Indonesia cũng bày tỏ sự ngạc nhiên trước bản lĩnh của đại diện Việt Nam, trong khi HLV Cristiano Roland khẳng định các học trò hoàn toàn xứng đáng được ca ngợi và tự hào."
        ),
        "source": "Thanh Niên / VnExpress / Dân Trí",
        "news_source": "THANH NIÊN / VNEXPRESS / DÂN TRÍ",
        "credit": "THANH NIÊN / VFF",
        "stat_badges": {
            "2": {"label": "PHẢN ỨNG QUỐC TẾ", "value": "FIFA & AFC", "sub": "Ca ngợi 2 bàn thắng tuyệt đẹp"},
            "3": {"label": "TRUYỀN THÔNG BỈ", "value": "ĐẦY THÓT TIM", "sub": "Tờ HLN thán phục 2 siêu phẩm"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_U17_AFC)], "THANH NIÊN / THE-AFC", "Trang chủ AFC đánh giá rất cao màn ra mắt của U17 Việt Nam"),
            _slot("title", 0, [_url(TN_U17_ROLAND)], "THANH NIÊN / VFF", "HLV Cristiano Roland bày tỏ niềm tự hào về tinh thần thi đấu của học trò"),
            _slot("title", 0, [_url(DT_U17_ASEAN)], "DÂN TRÍ / ASEAN FOOTBALL", "Màn trình diễn quả cảm tạo tiếng vang lớn trên truyền thông khu vực"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TN_U17_MATCH_5)], "THANH NIÊN / HƯƠNG NGUYỄN", "U17 Việt Nam nhận mưa lời khen dù chịu thất bại sát nút trước Bỉ"),
            _slot("sentence", 1, [_url(VNE_U17_7)], "VNEXPRESS", "Các cầu thủ trẻ chơi sòng phẳng cho đến những giây bù giờ cuối cùng"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(TN_U17_AFC)], "THANH NIÊN / THE-AFC", "AFC điểm tên Lê Sỹ Bách và Chu Ngọc Nguyễn Lực là hai ngôi sao sáng"),
            _slot("sentence", 2, [_url(TT_U17_FIFA)], "TUỔI TRẺ / FIFA", "FIFA.com gọi pha đánh gót mở tỷ số là khoảnh khắc lịch sử"),
            _slot("sentence", 2, [_url(TN_U17_NGLUC_2)], "THANH NIÊN / VFF", "Nguyễn Lực tiếp tục khẳng định vai trò nhạc trưởng sáng tạo"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(TN_U17_MATCH_3)], "THANH NIÊN / HƯƠNG NGUYỄN", "Báo Het Laatste Nieuws của Bỉ thừa nhận đội nhà thắng đầy thót tim"),
            _slot("sentence", 3, [_url(TN_U17_MATCH_4)], "THANH NIÊN / HƯƠNG NGUYỄN", "Hai pha lập công được báo giới châu Âu đánh giá đẳng cấp thế giới"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_url(DT_U17_ASEAN)], "DÂN TRÍ / ASEAN FOOTBALL", "Truyền thông Thái Lan và Indonesia đồng loạt dành lời tán thưởng"),
            _slot("sentence", 4, [_url(VNE_U17_ROL)], "VNEXPRESS / ĐOÀN CA", "HLV Cristiano Roland nhắn nhủ toàn đội giữ sự tự tin cho hai trận còn lại"),
            _slot("sentence", 4, [_url(TN_U17_TEAM_2)], "THANH NIÊN / VFF", "Tập thể U17 Việt Nam hướng tới cuộc đối đầu quan trọng với New Zealand"),
        ],
    },

    # 03 (Nam — U17 WORLD CUP 2026)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "U17 WORLD CUP 2026",
        "title": "Công nghệ VFS mới thay VAR gây tranh cãi dưới sự điều hành của tổ trọng tài toàn nữ Brazil",
        "summary": (
            "Bên cạnh hai siêu phẩm, trận đấu giữa U17 Việt Nam và U17 Bỉ còn thu hút sự chú ý đặc biệt khi được điều hành bởi tổ trọng tài toàn nữ đầu tiên của Brazil tại một kỳ World Cup bóng đá nam, đứng đầu là trọng tài chính Daiane Muniz. "
            "Thay vì áp dụng VAR tự động như truyền thống, giải U17 World Cup năm nay sử dụng hệ thống hỗ trợ video theo yêu cầu VFS, cấp cho mỗi đội tối đa hai quyền khiếu nại trong mỗi hiệp đấu. "
            "Trong hiệp hai trận đấu tối ngày 20 tháng 11, ban huấn luyện U17 Việt Nam đã hai lần yêu cầu xem lại VFS sau pha vào bóng cao chân của Van Gelder với Minh Thủy ở phút 64 và tình huống nghi vấn bóng chạm tay trong vòng cấm phút 69. "
            "Sau cả hai lần xem băng hình cùng lần khiếu nại ngược lại từ phía U17 Bỉ ở phút 72 nhắm vào Nguyễn Lực, trọng tài Daiane Muniz đều giữ nguyên quyết định trên sân khi không rút thẻ đỏ cũng như không thổi phạt đền."
        ),
        "source": "Dân Trí / Tuổi Trẻ",
        "news_source": "DÂN TRÍ / TUỔI TRẺ",
        "credit": "DÂN TRÍ / GETTY / CBF",
        "stat_badges": {
            "1": {"label": "CỘT MỐC TRỌNG TÀI", "value": "TỔ NỮ BRAZIL", "sub": "Daiane Muniz bắt chính"},
            "3": {"label": "CÔNG NGHỆ VFS", "value": "3 LẦN KHIẾU NẠI", "sub": "2 quyền mỗi hiệp thay cho VAR"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_REF_1)], "DÂN TRÍ / CBF", "Nữ trọng tài Brazil Daiane Muniz điều hành trận U17 Việt Nam gặp U17 Bỉ"),
            _slot("title", 0, [_url(DT_VFS_2)], "DÂN TRÍ / GETTY", "Trọng tài chính trực tiếp kiểm tra màn hình VFS bên đường biên"),
            _slot("title", 0, [_url(DT_VFS_1)], "DÂN TRÍ / GETTY", "Nhiều pha va chạm quyết liệt khiến hai đội ba lần dùng quyền khiếu nại"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(DT_REF_2)], "DÂN TRÍ / GETTY", "Daiane Muniz cùng hai nữ trợ lý tạo dấu mốc lịch sử cho trọng tài Brazil"),
            _slot("sentence", 1, [_url(TT_REF_GOAL)], "TUỔI TRẺ / GOAL", "Nữ trọng tài sinh năm 1988 từng điều hành nhiều giải đấu lớn của FIFA"),
            _slot("sentence", 1, [_url(DT_REF_1)], "DÂN TRÍ / CBF", "Bà Muniz phối hợp chặt chẽ cùng hai cộng sự Leila Cruz và Maira Moreira"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(DT_VFS_2)], "DÂN TRÍ / GETTY", "Công nghệ VFS chỉ hoạt động khi huấn luyện viên chủ động giơ thẻ yêu cầu"),
            _slot("sentence", 2, [_url(TN_U17_ROLAND)], "THANH NIÊN / VFF", "HLV Roland đánh giá cao cơ chế mới giúp các đội tự bảo vệ quyền lợi"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(DT_VFS_1)], "DÂN TRÍ / GETTY", "Phút 64 U17 Việt Nam khiếu nại pha vào bóng cao chân với Minh Thủy"),
            _slot("sentence", 3, [_url(VNE_U17_2)], "VNEXPRESS", "Đến phút 69 ban huấn luyện tiếp tục đề nghị kiểm tra lỗi chạm tay"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(DT_REF_1)], "DÂN TRÍ / CBF", "Trọng tài Daiane Muniz giữ nguyên quyết định không phạt đền và không thẻ đỏ"),
            _slot("sentence", 4, [_url(TN_U17_NGLUC_1)], "THANH NIÊN / VFF", "Phút 72 phía Bỉ cũng khiếu nại Nguyễn Lực nhưng không được chấp nhận"),
        ],
    },

    # 04 (Nữ — U17 WORLD CUP 2026)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "U17 WORLD CUP 2026",
        "title": "Cục diện bảng G U17 World Cup: Mali thắng đậm New Zealand 3-0, Việt Nam đứng thứ ba",
        "summary": (
            "Ở trận đấu còn lại của bảng G diễn ra tối ngày 20 tháng 11, đại diện Tây Phi là U17 Mali đã phô diễn sức mạnh vượt trội khi đánh bại U17 New Zealand với tỷ số đậm 3-0. "
            "Halidou Maiga mở tỷ số ngay phút 11 rồi tự mình hoàn tất cú đúp ở phút 50, trước khi Makan Sacko ấn định thắng lợi tưng bừng chỉ bốn phút sau đó. "
            "Kết quả này giúp U17 Mali tạm vươn lên dẫn đầu bảng G nhờ hơn hiệu số so với U17 Bỉ, trong khi U17 Việt Nam đứng thứ ba và xếp trên New Zealand nhờ ghi được hai bàn thắng. "
            "Đáng chú ý, trước lượt ra quân tờ Friends of Football của New Zealand từng nhận định Việt Nam là đối thủ dễ kiếm ba điểm nhất bảng, nhưng màn thể hiện trước Bỉ đang buộc đối thủ phải dè chừng trước cuộc đối đầu trực tiếp ngày 23 tháng 11."
        ),
        "source": "Tuổi Trẻ / Dân Trí",
        "news_source": "TUỔI TRẺ / DÂN TRÍ",
        "credit": "TUỔI TRẺ / FIFA / NZF",
        "stat_badges": {
            "1": {"label": "TRẬN CÒN LẠI BẢNG G", "value": "MALI 3-0 NZ", "sub": "Halidou Maiga lập cú đúp"},
            "3": {"label": "BẢNG XẾP HẠNG", "value": "HẠNG 3 BẢNG G", "sub": "U17 Việt Nam xếp trên New Zealand"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_U17_MALI)], "TUỔI TRẺ / FIFA", "U17 Mali áp đảo hoàn toàn và giành chiến thắng 3-0 trước New Zealand"),
            _slot("title", 0, [_url(DT_U17_MALI_2)], "DÂN TRÍ / NZF", "Đội bóng châu Phi vươn lên chiếm ngôi đầu bảng G sau lượt mở màn"),
            _slot("title", 0, [_url(TT_U17_NZ)], "TUỔI TRẺ / NZF", "U17 New Zealand rơi xuống cuối bảng và chịu áp lực lớn trước lượt hai"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TT_U17_MALI)], "TUỔI TRẺ / FIFA", "Lối chơi tốc độ ở hai biên của Mali khiến hàng thủ New Zealand vỡ trận"),
            _slot("sentence", 1, [_url(DT_U17_MALI_2)], "DÂN TRÍ / NZF", "Thủ môn Joseph Chalabi liên tục phải đối mặt các pha hãm thành nguy hiểm"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url("https://www.cafonline.com/media/rfmdllkx/new_mali-2.jpg")], "CAF / FIFA", "Halidou Maiga tỏa sáng với hai pha lập công ở phút 11 và phút 50"),
            _slot("sentence", 2, [_url("https://www.afrik-foot.com/app/uploads/2025/04/487377406_983484023897450_7477037389585812729_n.jpg")], "AFRIK FOOT", "U17 Mali khẳng định vị thế ứng cử viên hàng đầu tại bảng G"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(DT_U17_CELEB)], "DÂN TRÍ / VFF", "Hai bàn thắng vào lưới Bỉ giúp U17 Việt Nam tạm xếp trên New Zealand"),
            _slot("sentence", 3, [_url(VNE_U17_1)], "VNEXPRESS", "Cơ hội đi tiếp vẫn rộng mở nếu thầy trò HLV Roland giành điểm lượt hai"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(TT_U17_NZ)], "TUỔI TRẺ / NZF", "Truyền thông New Zealand trước giải từng xem Việt Nam là mục tiêu ba điểm"),
            _slot("sentence", 4, [_url(TT_U17_FIFA)], "TUỔI TRẺ / FIFA", "Cuộc đọ sức ngày 23 tháng 11 giữa hai đội mang tính chất then chốt"),
        ],
    },

    # 05 (Nam — BÓNG ĐÁ CHÂU Á)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "BÓNG ĐÁ CHÂU Á",
        "title": "Chốt 16 đội dự Vòng chung kết U17 châu Á 2027: Thái Lan và Malaysia đồng loạt bị loại",
        "summary": (
            "Loạt trận cuối vòng loại khép lại rạng sáng ngày 21 tháng 11 đã xác định đầy đủ 16 đội tuyển góp mặt tại Vòng chung kết U17 châu Á 2027 tổ chức tại Uzbekistan. "
            "Khu vực Đông Nam Á chứng kiến nỗi thất vọng lớn khi U17 Thái Lan dù chỉ cần một trận hòa trên sân nhà Buriram nhưng lại để thua ngược U17 Iraq 1-2 và chính thức đánh mất vé đi tiếp. "
            "Cùng chung cảnh ngộ, U17 Malaysia bị Ấn Độ cầm hòa 0-0 ở lượt quyết định nên chỉ đứng thứ ba bảng E với bảy điểm và dừng bước ngay trên sân nhà. "
            "Như vậy, Đông Nam Á chỉ còn đúng hai đại diện dự ngày hội bóng đá trẻ châu lục vào tháng 5 năm 2027 là U17 Việt Nam nhờ suất đặc cách vào thẳng và U17 Indonesia với ngôi nhất bảng A."
        ),
        "source": "VnExpress / Tuổi Trẻ",
        "news_source": "VNEXPRESS / TUỔI TRẺ",
        "credit": "VNEXPRESS / TUỔI TRẺ / AFC",
        "stat_badges": {
            "2": {"label": "CÚ SỐC VÒNG LOẠI", "value": "THÁI LAN 1-2", "sub": "Thua ngược Iraq tại Buriram"},
            "4": {"label": "ĐẠI DIỆN ĐÔNG NAM Á", "value": "VN & INDONESIA", "sub": "2 đội góp mặt trong 16 suất VCK"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_U17_THAI)], "VNEXPRESS / FAT", "U17 Thái Lan thất bại cay đắng trước Iraq ngay trên sân nhà"),
            _slot("title", 0, [_url(TT_U17_THAI)], "TUỔI TRẺ / CHANGSUEK", "Đại diện xứ chùa vàng lỡ hẹn với vòng chung kết châu lục"),
            _slot("title", 0, [_url(TT_U17_VN_AFC)], "TUỔI TRẺ / AFC", "U17 Việt Nam được đặc cách vào thẳng nhờ thành tích giải 2026"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TN_U17_TEAM_3)], "THANH NIÊN / VFF", "Tám đội dự World Cup cùng Qatar và bảy đội nhất bảng hội tụ tại Uzbekistan"),
            _slot("sentence", 1, [_local(DAILY_20 / "Tin_06_1.jpg")], "THANH NIÊN", "Vòng chung kết U17 châu Á 2027 dự kiến khởi tranh từ tháng 5 năm 2027"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(VNE_U17_THAI)], "VNEXPRESS / FAT", "Thái Lan thủng lưới ngay phút thứ sáu trước lối chơi tốc độ của Iraq"),
            _slot("sentence", 2, [_url(TT_U17_THAI)], "TUỔI TRẺ / CHANGSUEK", "Dù gỡ hòa trong hiệp hai nhưng đội chủ nhà vẫn nhận bàn thua quyết định"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_ddgs("Malaysia U17 football national team match action")], "FAM / AFC", "U17 Malaysia hòa không bàn thắng với Ấn Độ và tụt xuống thứ ba bảng E"),
            _slot("sentence", 3, [_ddgs("India U17 football team celebration AFC")], "AIFF / AFC", "Ấn Độ giữ vững ngôi đầu bảng E với 10 điểm để giành vé đi tiếp"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(TN_U17_TEAM_2)], "THANH NIÊN / VFF", "Việt Nam cùng Indonesia là hai lá cờ đầu còn lại của Đông Nam Á"),
            _slot("sentence", 4, [_ddgs("Indonesia U17 football team AFC match")], "PSSI / AFC", "U17 Indonesia bất bại với 10 điểm để đứng đầu bảng A vòng loại"),
        ],
    },

    # 06 (Nữ — BÓNG ĐÁ VIỆT NAM)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "BÓNG ĐÁ VIỆT NAM",
        "title": "Vòng 8 V-League: Thanh Hóa phá dớp tám năm hạ HAGL 2-1, Thể Công Viettel 11 trận chưa thắng",
        "summary": (
            "Hai trận đấu sớm vòng tám V-League 2026-2027 tối ngày 20 tháng 11 đã mang lại những thái cực hoàn toàn trái ngược cho các đội bóng tham dự. "
            "Trên sân nhà, tân huấn luyện viên người Hàn Quốc Kim Young Chul có màn ra mắt mỹ mãn khi giúp câu lạc bộ Thanh Hóa đánh bại Hoàng Anh Gia Lai 2-1 nhờ cú sút xa 25 mét của Damoth Thongkhamsavat ở phút 26 và bàn ấn định từ ngoại binh Martins phút 60. "
            "Chiến thắng quan trọng này giúp đội bóng xứ Thanh chính thức phá dớp hơn tám năm với 14 trận liên tiếp chỉ hòa và thua đối thủ phố núi kể từ tháng 9 năm 2018. "
            "Ở trận đấu cùng ngày tại sân Hàng Đẫy, Thể Công Viettel tiếp tục lún sâu vào khủng hoảng khi bị Sông Lam Nghệ An cầm hòa 0-0, qua đó kéo dài mạch không biết mùi chiến thắng trên mọi đấu trường lên con số 11."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / TUỔI TRẺ / DÂN TRÍ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "PHÁ DỚP LỊCH SỬ", "value": "THANH HÓA 2-1", "sub": "Thắng HAGL sau hơn 8 năm chờ đợi"},
            "4": {"label": "CHUỖI BẤT ỔN", "value": "11 TRẬN", "sub": "Thể Công Viettel chưa biết thắng"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_VL_TH_1)], "THANH NIÊN / CLB THANH HÓA", "Câu lạc bộ Thanh Hóa đánh bại HAGL 2-1 trong ngày ra mắt tân HLV"),
            _slot("title", 0, [_url(TT_VL_KIM)], "TUỔI TRẺ / MINH ĐỖ", "Tân HLV Kim Young Chul mang lại luồng sinh khí mới cho đội bóng xứ Thanh"),
            _slot("title", 0, [_url(TN_VL_TC_1)], "THANH NIÊN / MINH TÚ", "Thể Công Viettel chia điểm cùng Sông Lam Nghệ An trên sân Hàng Đẫy"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TN_VL_TH_2)], "THANH NIÊN / CLB THANH HÓA", "Bầu không khí sôi động trên sân Thanh Hóa tối ngày 20 tháng 11"),
            _slot("sentence", 1, [_url(TN_VL_TC_2)], "THANH NIÊN / MINH TÚ", "Trận đấu trên sân Hàng Đẫy diễn ra giằng co và quyết liệt"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(TT_VL_DAMOTH)], "TUỔI TRẺ / THFC", "Damoth Thongkhamsavat tung cú sút xa đẳng cấp hạ thủ môn Trung Kiên"),
            _slot("sentence", 2, [_url(TT_VL_KIM)], "TUỔI TRẺ / MINH ĐỖ", "Cựu trợ lý HLV Kim Sang Sik khởi đầu suôn sẻ ngay trận đầu cầm quân"),
            _slot("sentence", 2, [_url(TN_VL_TH_1)], "THANH NIÊN / CLB THANH HÓA", "Ngoại binh Martins tận dụng sai lầm hàng thủ HAGL để ghi bàn quyết định"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(TN_VL_TH_2)], "THANH NIÊN / CLB THANH HÓA", "Lần gần nhất Thanh Hóa thắng HAGL đã diễn ra từ tháng 9 năm 2018"),
            _slot("sentence", 3, [_local(DAILY_20 / "Tin_04_3.jpg")], "THANH NIÊN", "Thất bại khiến Hoàng Anh Gia Lai tiếp tục đối mặt nguy cơ rơi xuống đáy bảng"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_url(TT_VL_SLNA_2)], "TUỔI TRẺ / MINH ĐỖ", "Khuất Văn Khang và đồng đội bỏ lỡ cơ hội trước hàng thủ SLNA"),
            _slot("sentence", 4, [_url(TT_VL_SLNA_1)], "TUỔI TRẺ / MINH ĐỖ", "Cầu thủ Việt kiều Trần Đức Vinh thi đấu nổi bật giúp SLNA giữ mạch bất bại"),
            _slot("sentence", 4, [_url(TN_VL_TC_3)], "THANH NIÊN / MINH TÚ", "Thể Công Viettel nối dài chuỗi 11 trận không thắng trên mọi đấu trường"),
        ],
    },

    # 07 (Nam — THỂ THAO VIỆT NAM)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "THỂ THAO VIỆT NAM",
        "title": "Lê Quang Liêm xếp hạng 8 giải cờ vua toàn năng thế giới 2026, nhận thưởng 800 triệu đồng",
        "summary": (
            "Giải cờ vua toàn năng thế giới Total Chess 2026 tại Budapest, Hungary vừa khép lại rạng sáng ngày 21 tháng 11 với vị trí hạng tám chung cuộc dành cho kỳ thủ số một Việt Nam Lê Quang Liêm. "
            "Ở lượt về trận tranh hạng bảy trước đại kiện tướng Nga Ian Nepomniachtchi, Quang Liêm cầm hòa 6-6 sau các ván cờ chớp và cờ nhanh rồi xuất sắc thắng áp đảo 14-6 ở ván cờ tiêu chuẩn để cân bằng tỷ số sau hai ngày thi đấu. "
            "Bước vào ván Armageddon sinh tử khi phải cầm quân đen trước lợi thế đi trước của đối thủ, kỳ thủ Việt Nam đành chấp nhận thất bại sau 55 nước đi đầy căng thẳng. "
            "Với kết quả hạng tám chung cuộc sau hành trình bất bại ở vòng bảng từng giúp anh vươn lên hạng 12 thế giới, Lê Quang Liêm nhận khoản tiền thưởng 32000 USD, tương đương khoảng 800 triệu đồng."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "credit": "THANH NIÊN / TOTAL CHESS",
        "stat_badges": {
            "2": {"label": "CỜ TIÊU CHUẨN", "value": "THẮNG 14-6", "sub": "San bằng tỷ số trước Nepomniachtchi"},
            "4": {"label": "TIỀN THƯỞNG", "value": "32000 USD", "sub": "Khoảng 800 triệu đồng hạng 8"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_QUANGLIEM)], "THANH NIÊN / TOTAL CHESS", "Lê Quang Liêm khép lại giải cờ vua toàn năng thế giới với vị trí hạng tám"),
            _slot("title", 0, [_local(DAILY_19 / "Tin_14_2.jpg")], "FIDE", "Đại kiện tướng Nga Ian Nepomniachtchi là đối thủ cuối cùng của Quang Liêm"),
            _slot("title", 0, [_local(ORTHER_12 / "Tin_05_2.jpg")], "VNEXPRESS", "Kỳ thủ số một Việt Nam để lại nhiều dấu ấn chuyên môn tại Hungary"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TN_QUANGLIEM)], "THANH NIÊN / TOTAL CHESS", "Giải đấu tại Budapest quy tụ dàn siêu đại kiện tướng hàng đầu thế giới"),
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_14_5.jpg")], "WIKIMEDIA COMMONS", "Alireza Firouzja lên ngôi vô địch sau khi thắng Anish Giri ở chung kết"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_local(DAILY_19 / "Tin_14_6.jpg")], "THANH NIÊN", "Lê Quang Liêm thi đấu bùng nổ ở lượt về với chiến thắng 14-6 cờ tiêu chuẩn"),
            _slot("sentence", 2, [_local(DAILY_19 / "Tin_14_2.jpg")], "FIDE", "Ian Nepomniachtchi bị đẩy vào thế bám đuổi sau ván cờ tiêu chuẩn căng thẳng"),
            _slot("sentence", 2, [_local(ORTHER_12 / "Tin_05_5.jpg")], "VNEXPRESS", "Bản lĩnh xử lý trung cuộc sắc sảo giúp Quang Liêm đưa trận đấu về vạch xuất phát"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_14_1.jpg")], "THANH NIÊN / CHESS.COM", "Hai kỳ thủ phải giải quyết thắng thua bằng ván Armageddon sinh tử"),
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_14_4.jpg")], "THANH NIÊN", "Quang Liêm cầm quân đen và dừng bước đáng tiếc sau 55 nước đi"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_local(ORTHER_12 / "Tin_05_4.jpg")], "VNEXPRESS / TOTAL CHESS", "Thành tích bất bại vòng bảng từng giúp anh chạm mốc Elo 2742 và hạng 12 thế giới"),
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_14_12.jpg")], "THANH NIÊN", "Ngày 30 tháng 11 tới, Quang Liêm sẽ về TP.HCM thi đấu đại hội toàn quốc"),
        ],
    },

    # 08 (Nữ — CỜ TƯỚNG VIỆT NAM)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "THỂ THAO VIỆT NAM",
        "title": "Làng cờ tướng Trung Quốc đặc biệt chú ý đến kỳ thủ 18 tuổi Phan Huy Hoàng",
        "summary": (
            "Không chỉ có cờ vua, kỳ đàn Việt Nam còn vừa đón nhận tin vui từ làng cờ tướng khi tài năng trẻ 18 tuổi Phan Huy Hoàng nhận được sự chú ý đặc biệt từ truyền thông Trung Quốc. "
            "Trong bài tổng kết mới đăng tải, tờ Dương Thành Vãn Báo cùng nhiều chuyên trang cờ tướng Hoa ngữ đã phân tích kỹ và dành nhiều lời khen cho chức vô địch cá nhân đồng đội nam mà Huy Hoàng giành được tại Giải cờ tướng thế giới mở rộng 2026 ở Singapore. "
            "Được tin tưởng trao suất đánh chính thay đàn anh Lại Lý Huynh, kỳ thủ trẻ Việt Nam thi đấu bùng nổ đạt 13 điểm với sáu thắng một hòa, trong đó có trận hòa ấn tượng trước thần đồng Trung Quốc Lưu Bách Hoành và thắng lợi trước nhà vô địch châu Á Phùng Gia Thường. "
            "Truyền thông Trung Quốc đánh giá Phan Huy Hoàng sẽ là đối trọng mới đáng gờm của Việt Nam bên cạnh Lại Lý Huynh trên bản đồ cờ tướng thế giới."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / LĐCTVN",
        "stat_badges": {
            "2": {"label": "TRUYỀN THÔNG HOA NGỮ", "value": "DƯƠNG THÀNH VÃN BÁO", "sub": "Ca ngợi kỳ thủ trẻ Việt Nam"},
            "3": {"label": "THÀNH TÍCH BẤT BẠI", "value": "13 ĐIỂM", "sub": "6 thắng 1 hòa giành HCV cá nhân"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_PHANHUYHOANG)], "TUỔI TRẺ / TLKĐ", "Kỳ thủ 18 tuổi Phan Huy Hoàng gây ấn tượng mạnh với truyền thông Trung Quốc"),
            _slot("title", 0, [_local(DAILY_16 / "Tin_22_1.jpg")], "LIÊN ĐOÀN CỜ TƯỚNG VN", "Phan Huy Hoàng giương cao cờ Tổ quốc với HCV cá nhân thế giới"),
            _slot("title", 0, [_local(DAILY_16 / "Tin_22_6.jpg")], "WEBCOTUONG", "Màn trình diễn đạt 13 điểm đưa tên tuổi Huy Hoàng vươn tầm quốc tế"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TT_PHANHUYHOANG)], "TUỔI TRẺ / TLKĐ", "Làng cờ tướng Trung Quốc dành sự quan tâm lớn tới tài năng trẻ Việt Nam"),
            _slot("sentence", 1, [_local(DAILY_16 / "Tin_22_5.jpg")], "LIÊN ĐOÀN CỜ TƯỚNG VN", "Ở tuổi 18, Huy Hoàng cho thấy bản lĩnh thi đấu chững chạc trước các đại sư"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_local(ORTHER_14 / "s3_hoang_podium.jpg")], "LIÊN ĐOÀN CỜ TƯỚNG VN", "Huy Hoàng và Minh Nhật Quang mang về huy chương quý giá tại Singapore"),
            _slot("sentence", 2, [_local(DAILY_16 / "Tin_22_7.jpg")], "WEBCOTUONG", "Tờ Dương Thành Vãn Báo phân tích sâu các ván đấu đỉnh cao của kỳ thủ Việt"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_local(DAILY_16 / "Tin_22_4.jpg")], "LIÊN ĐOÀN CỜ TƯỚNG VN", "Anh vượt qua nhiều cao thủ hàng đầu châu Á để độc chiếm ngôi đầu cá nhân"),
            _slot("sentence", 3, [_url(TT_PHANHUYHOANG)], "TUỔI TRẺ / TLKĐ", "Trận hòa bản lĩnh trước Lưu Bách Hoành tạo bước ngoặt lớn cho bảng điểm"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_local(DAILY_20 / "Tin_18_2.jpg")], "TUỔI TRẺ / TLKĐ", "Bên cạnh Lại Lý Huynh, Việt Nam có thêm ngòi nổ mới cực kỳ chất lượng"),
            _slot("sentence", 4, [_local(DAILY_16 / "Tin_22_11.jpg")], "THANH NIÊN / VOV", "Tương lai rộng mở chờ đón thế hệ trẻ của cờ tướng Việt Nam"),
        ],
    },

    # 09 (Nam — ĐẠI HỘI THỂ THAO TOÀN QUỐC 2026)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "ĐẠI HỘI THỂ THAO TOÀN QUỐC",
        "title": "Khai mạc Đại hội Thể thao toàn quốc 2026 tối nay bên sông Sài Gòn: TP.HCM bứt phá vượt Hà Nội",
        "summary": (
            "Vào lúc 19 giờ tối nay ngày 21 tháng 11, Lễ khai mạc Đại hội Thể thao toàn quốc 2026 mang chủ đề Khát vọng vinh quang sẽ chính thức diễn ra tại Công viên Bờ sông Sài Gòn ở thành phố Hồ Chí Minh. "
            "Điểm nhấn đặc sắc của đêm khai mạc là nghi thức rước ngọn đuốc thiêng từ Bảo tàng Hồ Chí Minh tại Bến Nhà Rồng di chuyển dọc sông Sài Gòn qua cột cờ Thủ Ngữ, cầu đi bộ Thủ Thiêm và bến Bạch Đằng kết hợp trình diễn thể thao mặt nước. "
            "Ngay trước giờ khai mạc chính thức, đoàn chủ nhà thành phố Hồ Chí Minh đã tạo cú hích ngoạn mục trên bảng tổng sắp khi vượt qua Hà Nội để vươn lên dẫn đầu toàn đoàn. "
            "Đóng góp lớn nhất cho bước nhảy vọt này là đội tuyển Vovinam thành phố Hồ Chí Minh với màn thống trị tuyệt đối cả nội dung quyền lẫn đối kháng để mang về tới tám huy chương vàng."
        ),
        "source": "Thanh Niên",
        "news_source": "THANH NIÊN",
        "credit": "THANH NIÊN / XUÂN CƯỜNG",
        "stat_badges": {
            "1": {"label": "KHAI MẠC CHÍNH THỨC", "value": "19H TỐI NAY", "sub": "Công viên Bờ sông Sài Gòn"},
            "4": {"label": "MƯA VÀNG VOVINAM", "value": "8 HCV", "sub": "TP.HCM vượt Hà Nội dẫn đầu"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_DH_KHAIMAC)], "THANH NIÊN / XUÂN CƯỜNG", "Sân khấu hoành tráng bên sông Sài Gòn sẵn sàng cho đêm khai mạc 21 tháng 11"),
            _slot("title", 0, [_url(TN_DH_VOVINAM)], "THANH NIÊN / VOVINAM TP", "Võ sĩ Vovinam TP.HCM thi đấu thăng hoa giành tám huy chương vàng"),
            _slot("title", 0, [_local(DAILY_20 / "Tin_15_1.jpg")], "TUỔI TRẺ", "Toàn cảnh không gian tổng duyệt rực rỡ sắc màu của lễ khai mạc Đại hội"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TN_DH_KHAIMAC)], "THANH NIÊN / XUÂN CƯỜNG", "Đêm khai mạc chủ đề Khát vọng vinh quang mở màn lúc 19 giờ tối nay"),
            _slot("sentence", 1, [_local(DAILY_20 / "Tin_15_5.jpg")], "THANH NIÊN / HCMC SPORTS HUB", "Hơn 1500 nghệ sĩ và vận động viên góp mặt trong chương trình nghệ thuật"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_13_1.jpg")], "THANH NIÊN", "Lễ rước đuốc từ Bến Nhà Rồng di chuyển trên sông Sài Gòn đầy ấn tượng"),
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_13_5.jpg")], "THANH NIÊN", "Các hoạt động trình diễn đua thuyền rồng và thể thao nước kết nối dòng sông"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_local(DAILY_20 / "Tin_15_1.jpg")], "TUỔI TRẺ", "Đoàn chủ nhà TP.HCM bứt tốc vươn lên dẫn đầu bảng tổng sắp huy chương"),
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_16_1.jpg")], "TUỔI TRẺ", "Cuộc đua huy chương giữa hai trung tâm lớn TP.HCM và Hà Nội diễn ra gay cấn"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(TN_DH_VOVINAM)], "THANH NIÊN / VOVINAM TP", "Vovinam TP.HCM giành 8 HCV, 2 HCB và 2 HCĐ giữa hơn 400 võ sĩ toàn quốc"),
            _slot("sentence", 4, [_local(DAILY_20 / "Tin_16_2.jpg")], "TUỔI TRẺ", "Các võ sĩ chủ nhà áp đảo ở cả nội dung quyền truyền thống và đối kháng"),
        ],
    },

    # 10 (Nữ — ĐẠI HỘI THỂ THAO TOÀN QUỐC 2026)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "ĐẠI HỘI THỂ THAO TOÀN QUỐC",
        "title": "Sức nóng các môn Đại hội 2026: Hải Phòng thống trị Canoeing, Quân Đội soán ngôi Judo TP.HCM",
        "summary": (
            "Song song với sức nóng của Vovinam, các môn thi đấu sớm tại Đại hội Thể thao toàn quốc 2026 cũng vừa chứng kiến những màn tranh tài kịch tính ở Canoeing và Judo. "
            "Trên đường đua hồ Đá Bàng ở môn Canoeing, tay chèo chủ lực Nguyễn Thị Hương xuất sắc giành bốn huy chương vàng và một huy chương đồng, giúp đoàn Hải Phòng thống trị ngôi nhất toàn đoàn và bỏ xa chủ nhà thành phố Hồ Chí Minh năm huy chương vàng. "
            "Đáng nhớ nhất là ở chung kết thuyền đơn nữ 200 mét, Nguyễn Thị Hương cùng đồng đội ăn ý tại Asiad là Diệp Thị Hương của đoàn Công an Nhân dân đã cán đích gần như cùng lúc và được ban tổ chức trao đồng huy chương vàng. "
            "Ở bộ môn Judo diễn ra tại Bà Rịa, đoàn Quân Đội bứt phá mạnh mẽ trong ngày thi đấu cuối nội dung quyền khi giành ba trên tổng số mười huy chương vàng để chính thức soán ngôi nhất toàn đoàn sau ba kỳ liên tiếp thuộc về thành phố Hồ Chí Minh."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / QUÝ LƯỢNG",
        "stat_badges": {
            "2": {"label": "NGÔI SAO CANOEING", "value": "4 HCV", "sub": "Nguyễn Thị Hương giúp Hải Phòng nhất đoàn"},
            "4": {"label": "SOÁN NGÔI JUDO", "value": "ĐOÀN QUÂN ĐỘI", "sub": "Ngắt mạch 3 kỳ nhất đoàn của TP.HCM"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_DH_CANOEING)], "TUỔI TRẺ / QUÝ LƯỢNG", "Nguyễn Thị Hương thi đấu áp đảo trên đường đua hồ Đá Bàng"),
            _slot("title", 0, [_url(TT_DH_JUDO_QD)], "TUỔI TRẺ / FBNV", "Đoàn Judo Quân Đội vươn lên vị trí số một toàn đoàn tại Bà Rịa"),
            _slot("title", 0, [_url(TT_DH_JUDO_HCM)], "TUỔI TRẺ / HCMC HUB SPORTS", "Lê Anh Tài và các võ sĩ TP.HCM trải qua kỳ tranh tài đầy quyết liệt"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TT_DH_CANOEING)], "TUỔI TRẺ / QUÝ LƯỢNG", "Canoeing và Judo mang lại nhiều kịch tính trước lễ khai mạc chính thức"),
            _slot("sentence", 1, [_local(ROOT / "outputs" / "Orther" / "17.11.2026" / "images" / "v3_judo_phan_ngoc_dung_gold.jpg")], "BÁO TUỔI TRẺ", "Các đoàn thể thao mạnh cạnh tranh từng tấm huy chương vàng"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(TT_DH_CANOEING)], "TUỔI TRẺ / QUÝ LƯỢNG", "Nguyễn Thị Hương đem về bốn HCV giúp Hải Phòng dẫn đầu tuyệt đối Canoeing"),
            _slot("sentence", 2, [_url("https://thumb.wikimedia.org/wikipedia/commons/thumb/3/33/2014_ICF_Canoe_Sprint_World_Championships_-_Race_173_-_K4_W_500_-_VC.jpg/1920px-2014_ICF_Canoe_Sprint_World_Championships_-_Race_173_-_K4_W_500_-_VC.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail")], "WIKIMEDIA COMMONS", "Hải Phòng khẳng định thế mạnh vượt trội ở các nội dung đua thuyền tốc độ"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(TT_DH_CANOEING)], "TUỔI TRẺ / QUÝ LƯỢNG", "Nguyễn Thị Hương và Diệp Thị Hương cùng bước lên bục cao nhất cự ly 200m"),
            _slot("sentence", 3, [_url("https://upload.wikimedia.org/wikipedia/commons/f/fe/Mohammad_Abubakar_Durrani_in_Asian_Canoe_Sprint_Championship_Samarqand_2013.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail_unscaled")], "WIKIMEDIA COMMONS", "Cả hai từng chung thuyền giành tấm huy chương Asiad đầu tiên cho Canoeing Việt Nam"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(TT_DH_JUDO_QD)], "TUỔI TRẺ / FBNV", "Đoàn Quân Đội thắng ba nội dung quyền ngày cuối để lật đổ sự thống trị của TP.HCM"),
            _slot("sentence", 4, [_url("https://assets-global.website-files.com/5d655866b2055c7cbb5d79a1/640b4d2d84373f31945bf2fb_030423_Junko+Suzuki019.webp")], "JUDO WORLD", "Thành phố Hồ Chí Minh kết thúc chuỗi ba kỳ đại hội liên tiếp dẫn đầu môn Judo"),
        ],
    },

    # 11 (Nam — THỂ THAO ĐIỆN TỬ VIỆT NAM)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "THỂ THAO VIỆT NAM",
        "title": "P Esports Việt Nam vượt qua Thái Lan giành vé đầu tiên dự chung kết Free Fire thế giới 2026",
        "summary": (
            "Thể thao điện tử Việt Nam vừa tạo tiếng vang lớn trên đất Thái Lan khi đội tuyển P Esports xuất sắc đứng đầu ngày thi đấu mở màn giai đoạn hai giải vô địch thế giới Free Fire World Series Global Finals 2026. "
            "Sau sáu ván đấu căng thẳng quy tụ 12 đội tuyển hàng đầu tại Bangkok, đại diện Việt Nam đạt tổng cộng 101 điểm với 60 mạng hạ gục, qua đó vượt qua chủ nhà All Gamers Global xếp thứ hai với 99 điểm. "
            "Ấn tượng hơn nữa là màn trình diễn ổn định của P Esports đã bỏ xa đương kim vô địch thế giới Buriram United của Thái Lan tới 39 điểm, đẩy đối thủ xuống tận vị trí thứ chín. "
            "Thành tích đứng đầu bảng xếp hạng ngày giúp P Esports cùng All Gamers Global trở thành hai đội đầu tiên chính thức góp mặt ở vòng chung kết thế giới diễn ra vào ngày 28 tháng 11 tới."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / P ESPORTS",
        "stat_badges": {
            "2": {"label": "DẪN ĐẦU BANGKOK", "value": "101 ĐIỂM", "sub": "60 mạng hạ gục vượt 2 đội Thái Lan"},
            "4": {"label": "VÉ CHUNG KẾT", "value": "28 THÁNG 11", "sub": "Đội đầu tiên vào chung kết FFWS 2026"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_PESPORTS)], "TUỔI TRẺ / P ESPORTS", "Đội tuyển P Esports Việt Nam thi đấu thăng hoa tại Bangkok"),
            _slot("title", 0, [_ddgs("esports tournament stage arena Bangkok players")], "FFWS", "Sân khấu vòng loại trực tiếp giải vô địch thế giới Free Fire 2026"),
            _slot("title", 0, [_url("https://double-xp.net/wp-content/uploads/2026/11/DSC00026.webp")], "FFWS / DOUBLE-XP", "Đại diện Việt Nam vượt qua nhiều ông lớn khu vực để đoạt vé chung kết sớm"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TT_PESPORTS)], "TUỔI TRẺ / P ESPORTS", "P Esports mở màn giai đoạn hai đầy ấn tượng trước các đối thủ mạnh"),
            _slot("sentence", 1, [_ddgs("Free Fire World Series tournament arena")], "SPORTSDUNIA", "Các trận đấu diễn ra quyết liệt với 12 đội tuyển hàng đầu thế giới"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(TT_PESPORTS)], "TUỔI TRẺ / P ESPORTS", "Đội Việt Nam giành 101 điểm sau sáu ván để vượt qua chủ nhà All Gamers Global"),
            _slot("sentence", 2, [_ddgs("esports trophy championship stage celebration")], "FFWS", "Khả năng giao tranh và kiểm soát vòng bo hiệu quả giúp P Esports bứt phá"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url("https://double-xp.net/wp-content/uploads/2026/11/DSC00026.webp")], "FFWS / DOUBLE-XP", "Đương kim vô địch Buriram United hụt hơi và rơi xuống hạng chín với 62 điểm"),
            _slot("sentence", 3, [_url(TT_PESPORTS)], "TUỔI TRẺ / P ESPORTS", "Khoảng cách 39 điểm cho thấy phong độ vượt trội của đại diện Việt Nam"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_ddgs("esports tournament stage arena Bangkok players")], "FFWS", "P Esports giành quyền nghỉ ngơi chuẩn bị cho chung kết ngày 28 tháng 11"),
            _slot("sentence", 4, [_url(TT_PESPORTS)], "TUỔI TRẺ / P ESPORTS", "Người hâm mộ kỳ vọng đội nhà sẽ tiến tới ngôi vô địch thế giới"),
        ],
    },

    # 12 (Nữ — BÓNG ĐÁ QUỐC TẾ)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Cristiano Ronaldo ghi bàn thứ 986 rồi hỏng phạt đền khiến Al Nassr thua ngược Al Ahli 1-3",
        "summary": (
            "Rạng sáng ngày 21 tháng 11 tại giải vô địch quốc gia Arab Saudi, siêu sao Cristiano Ronaldo trở thành tâm điểm buồn vui lẫn lộn trong trận Al Nassr làm khách trước Al Ahli. "
            "Ngay phút 14, tiền đạo 41 tuổi dứt điểm chân phải vào góc xa mở tỷ số, nâng tổng số bàn thắng trong sự nghiệp lên con số 986 và chỉ còn cách cột mốc lịch sử 1000 bàn đúng 14 pha lập công nữa. "
            "Thế nhưng chỉ bốn phút sau, chính Ronaldo lại đá phạt đền trúng cột dọc bên trái, đánh dấu lần đầu tiên trong màu áo Al Nassr anh bỏ lỡ hai quả 11 mét liên tiếp. "
            "Việc đánh mất cơ hội nhân đôi cách biệt khiến Al Nassr trả giá đắt khi để Galeno, Ivan Toney và Roger Ibanez ghi liền ba bàn giúp Al Ahli thắng ngược 3-1, đẩy HLV Ange Postecoglou vào sức ép bị sa thải rất lớn."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "credit": "THANH NIÊN / VNEXPRESS / REUTERS",
        "stat_badges": {
            "2": {"label": "CỘT MỐC SỰ NGHIỆP", "value": "986 BÀN", "sub": "Còn 14 bàn nữa tới mốc 1000"},
            "4": {"label": "TỶ SỐ CHUNG CUỘC", "value": "AL AHLI 3-1", "sub": "Ronaldo hỏng phạt đền phút 18"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_CR7_1)], "THANH NIÊN / REUTERS", "Cristiano Ronaldo mở tỷ số ở phút 14 nhưng lại bỏ lỡ phạt đền ngay sau đó"),
            _slot("title", 0, [_url("https://f.rpp-noticias.io/2026/11/20/340334_1931342.jpg?width=860&quality=60")], "RPP / REUTERS", "Cú sút phạt đền của Ronaldo đưa bóng đập trúng cột dọc khung thành Al Ahli"),
            _slot("title", 0, [_url(TT_CR7_1)], "TUỔI TRẺ / AL NASSR", "Tiền đạo 41 tuổi đạt cột mốc 986 bàn thắng trong sự nghiệp thi đấu"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(VNE_CR7_1)], "VNEXPRESS / AL NASSR", "Al Nassr làm khách trên sân King Abdullah Sports City đầy thử thách"),
            _slot("sentence", 1, [_url(TN_CR7_2)], "THANH NIÊN / REUTERS", "Hàng thủ Al Ahli theo sát Ronaldo trong suốt 90 phút thi đấu"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url("https://images.talpa.digital/fetch/f_webp,c_limit,w_3840,q_auto/https://images.ctfassets.net/h0r08og5wngf/6Tm626hZHR4Jbl4pT7WS14/57cc3e68d2dbb9195e091b4d6c5d522c/videogoal-cristiano-ronaldo-schiet-al-nassr-op-0-1-voorsprong-tegen-al-ahli.jpg")], "TALPA / REUTERS", "Pha dứt điểm góc xa mở tỷ số giúp Ronaldo chạm mốc 986 bàn thắng"),
            _slot("sentence", 2, [_url(TT_CR7_1)], "TUỔI TRẺ / AL NASSR", "Đây là pha lập công thứ tám của anh tại Saudi Pro League mùa này"),
            _slot("sentence", 2, [_url(TN_CR7_1)], "THANH NIÊN / REUTERS", "Chân sút Bồ Đào Nha chỉ còn cách ngưỡng 1000 bàn đúng 14 pha lập công"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url("https://f.rpp-noticias.io/2026/11/20/340334_1931342.jpg?width=860&quality=60")], "RPP / REUTERS", "Phút 18 Ronaldo sút phạt đền dội cột dọc bỏ lỡ cơ hội nâng tỷ số lên 2-0"),
            _slot("sentence", 3, [_url(TN_CR7_2)], "THANH NIÊN / REUTERS", "Lần đầu tiên tại giải Arab Saudi anh sút hỏng hai quả phạt đền liên tiếp"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("Ivan Toney Al Ahli celebration goal")], "REUTERS", "Ivan Toney ghi bàn từ chấm 11m góp phần giúp Al Ahli thắng ngược 3-1"),
            _slot("sentence", 4, [_ddgs("Ange Postecoglou football manager touchline")], "REUTERS", "Thất bại khiến Al Nassr tụt xuống thứ ba và HLV Postecoglou chịu áp lực lớn"),
            _slot("sentence", 4, [_url(VNE_CR7_1)], "VNEXPRESS / AL NASSR", "Al Nassr hiện kém đội đầu bảng Al Hilal hai điểm nhưng đá nhiều hơn một trận"),
        ],
    },

    # 13 (Nam — BÓNG ĐÁ QUỐC TẾ)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "HLV Jose Mourinho đột ngột ngừng họp báo Real Madrid khi bị hỏi về Cristiano Ronaldo",
        "summary": (
            "Một tình huống căng thẳng bất ngờ đã xảy ra trong buổi họp báo của câu lạc bộ Real Madrid ngày 20 tháng 11 trước thềm trận tiếp Celta Vigo ở vòng 13 La Liga. "
            "Sau khi trả lời bình tĩnh phần lớn câu hỏi về lực lượng và phong độ các học trò, HLV Jose Mourinho lập tức đổi sắc mặt khi một phóng viên nhắc tới đội tuyển Bồ Đào Nha trong đợt tập trung đầu tiên vắng Cristiano Ronaldo. "
            "Chiến lược gia người Bồ Đào Nha lắc ngón tay nói không năm lần liên tiếp, tuyên bố ngắn gọn rằng ông chỉ mong đội tuyển quê hương chiến thắng và sẽ không bình luận thêm điều gì rồi đứng dậy rời khỏi phòng họp báo. "
            "Trước đó trong ba mùa giải dẫn dắt Real Madrid từ năm 2010 đến 2013, Mourinho từng giúp Ronaldo bùng nổ với 168 bàn thắng qua 164 trận nhưng hai thầy trò cũng nhiều lần nảy sinh bất đồng."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / REAL MADRID CF",
        "stat_badges": {
            "3": {"label": "PHẢN ỨNG GAY GẮT", "value": "RỜI HỌP BÁO", "sub": "Từ chối bình luận về Ronaldo"},
            "4": {"label": "KỶ LỤC CÙNG NHAU", "value": "168 BÀN", "sub": "Thành tích CR7 dưới thời Mourinho"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_MOU_PRESS)], "VNEXPRESS / FOOTBALLTWEET", "HLV Jose Mourinho lắc tay từ chối trả lời rồi đứng dậy rời phòng họp báo"),
            _slot("title", 0, [_local(DAILY_16 / "Tin_11_3.jpg")], "REAL MADRID CF / REUTERS", "Nhà cầm quân Bồ Đào Nha đang giúp Real Madrid duy trì phong độ cao tại La Liga"),
            _slot("title", 0, [_local(ORTHER_10 / "Tin_01_7.jpg")], "AP PHOTO", "Mourinho kiên quyết khép lại mọi câu hỏi liên quan tới Ronaldo"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_local(DAILY_16 / "Tin_11_8.jpg")], "LA LIGA", "Real Madrid chuẩn bị cho cuộc tiếp đón Celta Vigo ở vòng 13 La Liga"),
            _slot("sentence", 1, [_local(DAILY_16 / "Tin_11_3.jpg")], "REAL MADRID CF / REUTERS", "Buổi họp báo ngày 20 tháng 11 đột ngột kết thúc sớm vì một câu hỏi nhạy cảm"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(VNE_MOU_PRESS)], "VNEXPRESS / FOOTBALLTWEET", "Nghe nhắc tới đội tuyển Bồ Đào Nha vắng Ronaldo, Mourinho lập tức phản ứng"),
            _slot("sentence", 2, [_url(TN_CR7_1)], "THANH NIÊN / REUTERS", "Ronaldo vừa tuyên bố giã từ sự nghiệp quốc tế sau 146 bàn cho tuyển Bồ Đào Nha"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_local(ORTHER_10 / "Tin_01_3.jpg")], "REUTERS", "Mourinho nói không năm lần liên tiếp và bước thẳng ra ngoài"),
            _slot("sentence", 3, [_local(ORTHER_10 / "Tin_01_7.jpg")], "AP PHOTO", "Ông khẳng định bản thân không liên quan và không bình luận thêm về chủ đề này"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_local(DAILY_16 / "Tin_11_6.jpg")], "AFP / REUTERS", "Dưới trướng Mourinho giai đoạn 2010–2013, Ronaldo đạt hiệu suất ghi bàn cao nhất"),
            _slot("sentence", 4, [_local(DAILY_16 / "Tin_11_1.jpg")], "AFP", "Tuy nhiên mối quan hệ giữa hai nhân vật cá tính mạnh này từng nhiều lần rạn nứt"),
        ],
    },

    # 14 (Nữ — BÓNG ĐÁ QUỐC TẾ)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Bayern Munich hòa Cologne 1-1, Harry Kane rách dây chằng cổ chân phải nghỉ dài hạn",
        "summary": (
            "Trận đấu sớm vòng 10 Bundesliga trên sân Allianz Arena rạng sáng ngày 21 tháng 11 đã mang lại cơn ác mộng thực sự cho câu lạc bộ Bayern Munich cả về điểm số lẫn lực lượng. "
            "Đội khách Cologne bất ngờ vượt lên dẫn trước ở phút 12 nhờ pha lập công của tài năng trẻ Mikey Moore, trước khi Nathaniel Brown ghi bàn gỡ hòa 1-1 cho Hùm xám ở phút 37. "
            "Tổn thất lớn nhất giáng xuống Bayern ngay trong hiệp một khi tiền đạo vừa giành Quả bóng vàng Harry Kane bị đau nặng sau pha va chạm với hậu vệ Joel Schmied và buộc phải rời sân ở phút 20. "
            "Kết quả kiểm tra xác nhận đội trưởng tuyển Anh bị rách dây chằng khớp mộng chày mác cổ chân trái, nhiều khả năng phải nghỉ thi đấu từ hai đến bốn tháng và lỡ toàn bộ phần còn lại của năm 2026 trong bối cảnh Michael Olise cũng dính chấn thương bàn chân."
        ),
        "source": "Bongdaplus / Webthethao / Sky Sports",
        "news_source": "BONGDAPLUS / SKY SPORTS",
        "credit": "REUTERS / AP PHOTO",
        "stat_badges": {
            "2": {"label": "VÒNG 10 BUNDESLIGA", "value": "BAYERN 1-1", "sub": "Cologne cầm chân Hùm xám tại Munich"},
            "4": {"label": "CHẤN THƯƠNG NẶNG", "value": "NGHỈ 2-4 THÁNG", "sub": "Harry Kane rách dây chằng cổ chân"},
        },
        "slots": [
            _slot("title", 0, [_local(DAILY_02 / "Tin_11_1.jpg")], "REUTERS", "Harry Kane ôm mặt đau đớn trên sân trong ngày Bayern gặp tổn thất lớn"),
            _slot("title", 0, [_local(DAILY_02 / "Tin_01_8.jpg")], "REUTERS", "Chân sút chủ lực của Bayern Munich đứng trước nguy cơ nghỉ thi đấu hết năm"),
            _slot("title", 0, [_url("https://s.yimg.com/lo/mysterio/api/83d22c33c1ec0de7b374de6723ad74415d1531f4d5541fff362992d0a2e5e1fe/lightyear_networkapi/resizefill_w1200_h675;quality_80;format_webp/https://media.zenfs.com/en/sb_nation_articles_115/7a85ac86b90ad99ccc2cee4a80965144.jpg")], "BAYERN MUNICH", "HLV Vincent Kompany lo âu bên đường biên tại Allianz Arena"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_ddgs("Allianz Arena Bayern Munich stadium match night")], "REUTERS", "Allianz Arena chứng kiến đêm thi đấu đầy bất ổn của đội chủ nhà"),
            _slot("sentence", 1, [_url("https://cdnphoto.dantri.com.vn/xB_jH9hi7W2YFVfC8Ihdqrfe474=/thumb_w/1360/2026/11/21/harry-kane-bayern-munich-1-1124512098-1795227375708.jpg")], "DÂN TRÍ / REUTERS", "Bayern Munich trả giá đắt dù có sự trở lại của HLV Vincent Kompany"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url("https://images.ctfassets.net/nurz7nsnha04/7uD92hdg9Np66tjZUVBqNz/df777e8383992bceae09ee5efebd1710/Stadion__20_.jpg?fm=webp&w=1920&q=75")], "FC KOLN", "Cologne mở tỷ số sớm ở phút 12 nhờ pha dứt điểm của Mikey Moore"),
            _slot("sentence", 2, [_local(DAILY_02 / "Tin_01_8.jpg")], "REUTERS", "Nathaniel Brown giữ lại một điểm cho Bayern bằng bàn gỡ hòa phút 37"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_local(DAILY_02 / "Tin_11_1.jpg")], "REUTERS", "Harry Kane rời sân từ phút 20 sau tình huống va chạm mạnh ở cổ chân trái"),
            _slot("sentence", 3, [_local(DAILY_02 / "Tin_01_1.jpg")], "REUTERS", "Chấn thương ập đến đúng giai đoạn chủ nhân Quả bóng vàng 2026 đạt phong độ cao"),
            _slot("sentence", 3, [_local(DAILY_02 / "Tin_11_10.jpg")], "REUTERS", "Cả sân Allianz Arena lặng đi khi thấy số 9 không thể tự bước tiếp"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_local(DAILY_02 / "Tin_01_11.jpg")], "REUTERS", "Kane rách dây chằng cổ chân trái và phải ngồi ngoài ít nhất hai đến bốn tháng"),
            _slot("sentence", 4, [_ddgs("Michael Olise Bayern Munich football action")], "GETTY", "Đồng đội Michael Olise cũng chấn thương bàn chân và rời sân sau giờ nghỉ"),
        ],
    },

    # 15 (Nam — BÓNG ĐÁ CHÂU ÂU)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Bốc thăm tứ kết UEFA Nations League: Tây Ban Nha đại chiến Pháp, Bồ Đào Nha gặp Hà Lan",
        "summary": (
            "Lễ bốc thăm vòng tứ kết UEFA Nations League 2026-2027 diễn ra tại Nyon, Thụy Sĩ tối ngày 20 tháng 11 đã tạo nên bốn cặp đấu đỉnh cao cực kỳ cân não. "
            "Tâm điểm lớn nhất là cuộc tái ngộ giữa đương kim vô địch thế giới Tây Ban Nha và đội tuyển Pháp dưới triều đại tân HLV Zinedine Zidane, nơi Kylian Mbappe có cơ hội đòi món nợ bán kết World Cup trước Lamine Yamal. "
            "Ở cặp đấu giàu duyên nợ khác, nhà đương kim vô địch Nations League Bồ Đào Nha chạm trán Hà Lan trong màn tái hiện trận chung kết mùa đầu tiên năm 2019 và đối mặt nhánh bán kết tử thần nếu đi tiếp. "
            "Hai cặp tứ kết còn lại chứng kiến tuyển Anh tái đấu Na Uy của Erling Haaland còn Đức đối đầu Bỉ, với các lượt trận đi và về dự kiến diễn ra vào cuối tháng 3 năm 2027."
        ),
        "source": "VnExpress / Tuổi Trẻ / UEFA",
        "news_source": "VNEXPRESS / TUỔI TRẺ / UEFA",
        "credit": "VNEXPRESS / AP / REUTERS",
        "stat_badges": {
            "2": {"label": "SIÊU ĐẠI CHIẾN", "value": "TBN VS PHÁP", "sub": "Lamine Yamal tái đấu Kylian Mbappe"},
            "3": {"label": "NHÁNH TỬ THẦN", "value": "BỒ ĐÀO NHA VS HÀ LAN", "sub": "Tái hiện chung kết năm 2019"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_NL_ESP_FRA)], "VNEXPRESS / AP", "Tây Ban Nha đối đầu Pháp là cặp tứ kết được mong chờ nhất"),
            _slot("title", 0, [_url(VNE_NL_POR)], "VNEXPRESS / AP", "Bồ Đào Nha rơi vào nhánh đấu đầy chông gai để bảo vệ ngôi vương"),
            _slot("title", 0, [_url(VNE_NL_NOR_ENG)], "VNEXPRESS / AFP", "Tuyển Anh tái ngộ Erling Haaland và đội tuyển Na Uy tại tứ kết"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_ddgs("UEFA Nations League trophy draw Nyon")], "UEFA", "Lễ bốc thăm tại trụ sở UEFA ở Thụy Sĩ xác định bốn cặp tứ kết League A"),
            _slot("sentence", 1, [_url(VNE_NL_POR)], "VNEXPRESS / AP", "Tám đội tuyển mạnh nhất châu Âu bước vào vòng loại trực tiếp đầy kịch tính"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(VNE_NL_ESP_FRA)], "VNEXPRESS / AP", "Yamal ghi bốn bàn và hai kiến tạo cho Tây Ban Nha tại vòng bảng"),
            _slot("sentence", 2, [_ddgs("Zinedine Zidane France national team coach")], "REUTERS", "HLV Zinedine Zidane nhận định đây là thử thách lớn cho tập thể mới của Pháp"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(TT_NL_POR)], "TUỔI TRẺ / REUTERS", "Bồ Đào Nha từng thắng Hà Lan 1-0 ở chung kết Nations League 2019"),
            _slot("sentence", 3, [_url(VNE_NL_POR)], "VNEXPRESS / AP", "Đội thắng cặp đấu này sẽ gặp Tây Ban Nha hoặc Pháp tại bán kết"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(VNE_NL_NOR_ENG)], "VNEXPRESS / AFP", "Anh tái ngộ Na Uy trong khi đội tuyển Đức đối đầu tuyển Bỉ ở nhánh còn lại"),
            _slot("sentence", 4, [_local(DAILY_16 / "Tin_07_4.jpg")], "REUTERS", "Vòng tứ kết diễn ra hai lượt đi về từ ngày 25 đến 30 tháng 3 năm 2027"),
        ],
    },

    # 16 (Nữ — BÓNG ĐÁ CHÂU Á)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "BÓNG ĐÁ CHÂU Á",
        "title": "Bóng đá Hàn Quốc đối mặt nguy cơ bị FIFA đình chỉ, lỡ vòng loại World Cup 2030",
        "summary": (
            "Làng bóng đá xứ sở kim chi đang rúng động trước thông tin Liên đoàn Bóng đá Hàn Quốc KFA có thể bị FIFA đình chỉ tư cách thành viên, dẫn tới nguy cơ mất quyền dự vòng loại World Cup 2030. "
            "Theo tiết lộ của tờ JoongAng Ilbo, FIFA đã gửi văn bản cảnh báo trước những tranh cãi gay gắt xung quanh cuộc cải tổ bộ máy và thay đổi quy chế bầu cử chủ tịch KFA sau thất bại bị loại ngay vòng bảng World Cup 2026. "
            "Dưới sức ép từ Ủy ban Cải cách có sự tham gia của cựu danh thủ Park Ji Sung, số lượng cử tri bầu cử được đề xuất mở rộng từ 192 lên khoảng 20000 người, làm dấy lên lo ngại can thiệp hành chính vi phạm quy định độc lập của FIFA. "
            "Một quan chức KFA thừa nhận nếu lệnh cấm có hiệu lực, các nhà tài trợ có thể đồng loạt hủy hợp đồng, đẩy liên đoàn vào khủng hoảng tài chính nghiêm trọng và đóng băng hoạt động chuyển nhượng quốc tế."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / REUTERS / NEWSIS",
        "stat_badges": {
            "1": {"label": "CẢNH BÁO TỪ FIFA", "value": "NGUY CƠ CẤM", "sub": "Ảnh hưởng vòng loại World Cup 2030"},
            "3": {"label": "TRANH CÃI BẦU CỬ", "value": "20000 CỬ TRI", "sub": "Mở rộng từ 192 phiếu bầu KFA"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_KFA_SON)], "TUỔI TRẺ / REUTERS", "Bóng đá Hàn Quốc rơi vào khủng hoảng sâu rộng sau World Cup 2026"),
            _slot("title", 0, [_url(TT_KFA_LEE)], "TUỔI TRẺ / SEDAILY", "Quyền chủ tịch KFA Lee Yong Soo chịu áp lực nặng nề từ dư luận và FIFA"),
            _slot("title", 0, [_url(TT_KFA_PARK)], "TUỔI TRẺ / NEWSIS", "Cựu danh thủ Park Ji Sung tham gia Ủy ban Cải cách bóng đá Hàn Quốc"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TT_KFA_SON)], "TUỔI TRẺ / REUTERS", "Đội tuyển Hàn Quốc đứng trước nguy cơ mất suất dự các giải lớn của FIFA"),
            _slot("sentence", 1, [_local(DAILY_16 / "Tin_18_5.jpg")], "WIKIMEDIA COMMONS", "FIFA theo dõi sát sao biến động thượng tầng tại liên đoàn thành viên"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(TT_KFA_LEE)], "TUỔI TRẺ / SEDAILY", "Chủ tịch Chung Mong Gyu đã từ chức hồi tháng 7 sau 13 năm lãnh đạo"),
            _slot("sentence", 2, [_url(TT_KFA_SON)], "TUỔI TRẺ / REUTERS", "Thất bại ở vòng bảng World Cup 2026 châm ngòi cho cuộc khủng hoảng kéo dài"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(TT_KFA_PARK)], "TUỔI TRẺ / NEWSIS", "Đề xuất nâng cử tri từ 192 lên 20000 người gây tranh cãi về tính độc lập"),
            _slot("sentence", 3, [_url(TT_KFA_LEE)], "TUỔI TRẺ / SEDAILY", "FIFA nghiêm cấm mọi hình thức can thiệp từ bên ngoài vào liên đoàn bóng đá"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(TT_KFA_SON)], "TUỔI TRẺ / REUTERS", "Án đình chỉ sẽ làm tê liệt cả chuyển nhượng cầu thủ lẫn tài trợ thương mại"),
            _slot("sentence", 4, [_local(DAILY_16 / "Tin_18_5.jpg")], "WIKIMEDIA COMMONS", "KFA đang chạy đua thời gian để tìm tiếng nói chung tránh án phạt nặng"),
        ],
    },

    # 17 (Nam — NGOẠI HẠNG ANH)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "NGOẠI HẠNG ANH",
        "title": "Man City và Nottingham Forest phản đối lá chắn pháp lý bảo vệ CEO Ngoại hạng Anh",
        "summary": (
            "Cuộc chiến pháp lý âm ỉ giữa Manchester City và ban tổ chức Ngoại hạng Anh tiếp tục leo thang sau cuộc bỏ phiếu cổ đông gây tranh cãi được báo The Times tiết lộ ngày 20 tháng 11. "
            "Ban tổ chức giải đấu đã đề nghị các câu lạc bộ thông qua việc cấp chứng thư bồi thường thiệt hại cá nhân cho Giám đốc điều hành Richard Masters cùng Chủ tịch Alison Brittain và ba thành viên hội đồng quản trị khác. "
            "Văn bản này đóng vai trò như lá chắn tài chính bảo vệ năm lãnh đạo giải đấu trước nguy cơ bị các nhà tài trợ của Manchester City khởi kiện đòi bồi thường lên tới hàng trăm triệu thậm chí hàng tỷ USD. "
            "Trong phiên bỏ phiếu, có tới 18 câu lạc bộ đồng ý hoặc không phản đối, riêng chỉ có Manchester City và Nottingham Forest kiên quyết bỏ phiếu chống lại đề xuất này."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / REUTERS / THE TIMES",
        "stat_badges": {
            "2": {"label": "BẢO VỆ LÃNH ĐẠO EPL", "value": "5 THÀNH VIÊN", "sub": "Cấp chứng thư miễn trừ cá nhân"},
            "4": {"label": "KẾT QUẢ BỎ PHIẾU", "value": "2 PHIẾU CHỐNG", "sub": "Chỉ Man City và Nottingham phản đối"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_MC_MASTERS)], "VNEXPRESS / REUTERS", "Giám đốc điều hành Ngoại hạng Anh Richard Masters đứng giữa tâm bão kiện tụng"),
            _slot("title", 0, [_url(VNE_MC_OWNERS)], "VNEXPRESS / THE TIMES", "Giới chủ và ban lãnh đạo Man City giữ lập trường cứng rắn trước EPL"),
            _slot("title", 0, [_url(VNE_MC_ETIHAD)], "VNEXPRESS / REUTERS", "Sân vận động Etihad của nhà đương kim vô địch Ngoại hạng Anh"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_local(ORTHER_05 / "Tin_03_2.jpg")], "GETTY IMAGES", "Căng thẳng giữa Man City và ban tổ chức giải đấu bước vào giai đoạn mới"),
            _slot("sentence", 1, [_local(ORTHER_05 / "Tin_03_3.jpg")], "GETTY IMAGES", "Các tranh chấp thương mại liên quan quy tắc tài trợ vẫn chưa có hồi kết"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(VNE_MC_MASTERS)], "VNEXPRESS / REUTERS", "Năm lãnh đạo cấp cao của Ngoại hạng Anh được đề xuất cấp chứng thư bảo vệ"),
            _slot("sentence", 2, [_url(VNE_MC_OWNERS)], "VNEXPRESS / THE TIMES", "Đề xuất này nhằm miễn trừ trách nhiệm tài chính cá nhân cho ban điều hành"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_local(ORTHER_08 / "Tin_01_11.jpg")], "AP PHOTO", "Những vụ kiện tiềm tàng từ đối tác tài trợ có giá trị lên tới hàng trăm triệu USD"),
            _slot("sentence", 3, [_local(ORTHER_08 / "Tin_01_7.jpg")], "AP PHOTO", "Tranh cãi pháp lý kéo dài tạo áp lực tài chính lớn lên bộ máy điều hành giải"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(VNE_MC_ETIHAD)], "VNEXPRESS / REUTERS", "Chỉ Man City và Nottingham Forest bỏ phiếu chống trong cuộc họp cổ đông"),
            _slot("sentence", 4, [_url(VNE_MC_MASTERS)], "VNEXPRESS / REUTERS", "Đa số câu lạc bộ còn lại chấp thuận để giữ ổn định bộ máy lãnh đạo giải"),
        ],
    },

    # 18 (Nữ — BÓNG ĐÁ MỸ MLS)
    {
        "id": 18,
        "art_id": "art_18",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Lionel Messi cùng Inter Miami săn ngôi vô địch MLS Cup thứ hai liên tiếp từ sáng mai",
        "summary": (
            "Sau khi hoàn tất cú đúp danh hiệu Chiếc Giày Vàng mùa thứ hai liên tiếp, siêu sao Lionel Messi sẽ chính thức bước vào hành trình bảo vệ ngôi vương MLS Cup cùng Inter Miami vào lúc 6 giờ sáng mai ngày 22 tháng 11 theo giờ Hà Nội. "
            "Ở vòng đầu tiên thể thức đấu loại tối đa ba trận, đội bóng áo hồng tiếp đón đối thủ khó chịu Columbus Crew trên sân nhà Nu Stadium nhờ vị trí nhì bảng miền Đông với 60 điểm. "
            "Mục tiêu của thầy trò Inter Miami là trở thành câu lạc bộ đầu tiên bảo vệ thành công chiếc cúp vô địch nhà nghề Mỹ kể từ chiến tích của LA Galaxy năm 2012. "
            "Tuy nhiên giới chuyên môn cảnh báo Messi và đồng đội cần hết sức dè chừng khi Inter Miami chỉ thắng sáu trận sân nhà suốt mùa giải chính, thấp nhất trong nhóm 18 đội dự play-off."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / AP / REUTERS",
        "stat_badges": {
            "1": {"label": "MLS CUP PLAY-OFF", "value": "6H SÁNG 22/11", "sub": "Inter Miami tiếp Columbus Crew"},
            "3": {"label": "MỤC TIÊU LỊCH SỬ", "value": "BẢO VỆ CÚP", "sub": "Chưa đội nào làm được từ 2012"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_MESSI_1)], "VNEXPRESS / AP", "Lionel Messi sẵn sàng bước vào chiến dịch bảo vệ chức vô địch MLS Cup"),
            _slot("title", 0, [_local(DAILY_20 / "Tin_09_1.jpg")], "VNEXPRESS / REUTERS", "Chủ nhân Chiếc Giày Vàng dẫn dắt hàng công Inter Miami tại play-off"),
            _slot("title", 0, [_ddgs("MLS Cup trophy soccer stadium Miami")], "MLS", "Đội trưởng Argentina hướng tới cột mốc chưa từng có trong hơn một thập kỷ"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(VNE_MESSI_1)], "VNEXPRESS / AP", "Messi khép lại giai đoạn tính điểm với phong độ ghi bàn vượt trội"),
            _slot("sentence", 1, [_local(DAILY_20 / "Tin_09_1.jpg")], "VNEXPRESS / REUTERS", "Trận mở màn gặp Columbus Crew diễn ra lúc 6 giờ sáng ngày 22 tháng 11"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_ddgs("Chase Stadium Inter Miami night match")], "AP PHOTO", "Inter Miami đứng nhì miền Đông với 60 điểm nên nắm lợi thế sân nhà"),
            _slot("sentence", 2, [_ddgs("Columbus Crew MLS soccer match celebration")], "USA TODAY", "Columbus Crew đang có phong độ cao dưới thời HLV tạm quyền Laurent Courtois"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(VNE_MESSI_1)], "VNEXPRESS / AP", "Lần gần nhất một đội bảo vệ thành công MLS Cup là LA Galaxy năm 2012"),
            _slot("sentence", 3, [_ddgs("MLS Cup trophy soccer stadium Miami")], "MLS", "Thể thức ba trận thắng hai ở vòng một đòi hỏi sự tập trung tối đa"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_local(DAILY_20 / "Tin_09_1.jpg")], "VNEXPRESS / REUTERS", "Phong độ sân nhà với chỉ sáu trận thắng là điểm yếu Inter Miami cần khắc phục"),
            _slot("sentence", 4, [_ddgs("Chase Stadium Inter Miami night match")], "AP PHOTO", "Người hâm mộ kỳ vọng bản lĩnh ngôi sao của Messi sẽ tỏa sáng đúng lúc"),
        ],
    },

    # 19 (Nam — QUẦN VỢT QUỐC TẾ)
    {
        "id": 19,
        "art_id": "art_19",
        "group": "THỂ THAO QUỐC TẾ",
        "title": "ATP Finals 2026 tại Turin chốt hai cặp bán kết hôm nay: Alcaraz gặp Shelton, Zverev đấu Medvedev",
        "summary": (
            "Vòng bảng giải quần vợt cuối năm ATP Finals 2026 tại Turin, Italy vừa khép lại sau lượt trận cuối bảng Ivan Lendl ngày 20 tháng 11 với những tấm vé xứng đáng cho các ngôi sao hàng đầu. "
            "Vượt qua nỗi lo chấn thương chân trái từng khiến anh phải kiểm tra y tế trước đó, tay vợt Tây Ban Nha Carlos Alcaraz xuất sắc đánh bại Flavio Cobolli sau hai set với tỷ số 6-4 và 6-1 để đứng đầu bảng tuyệt đối. "
            "Ở trận đấu còn lại, cựu số một thế giới Daniil Medvedev vượt qua Frances Tiafoe 6-3 và 6-4 để đoạt suất nhì bảng đi tiếp vào vòng bốn tay vợt mạnh nhất. "
            "Như vậy, hai trận bán kết đỉnh cao diễn ra hôm nay ngày 21 tháng 11 sẽ là màn so tài giữa Carlos Alcaraz gặp tay vợt trẻ Mỹ Ben Shelton và hạt giống số một Alexander Zverev đụng độ Daniil Medvedev."
        ),
        "source": "ATP Tour / 24h",
        "news_source": "ATP TOUR / 24H",
        "credit": "ATP TOUR / REUTERS",
        "stat_badges": {
            "2": {"label": "LƯỢT CUỐI BẢNG LENDL", "value": "6-4, 6-1", "sub": "Alcaraz toàn thắng vượt qua Cobolli"},
            "4": {"label": "BÁN KẾT HÔM NAY", "value": "ALCARAZ VS SHELTON", "sub": "Zverev gặp Medvedev tại Turin"},
        },
        "slots": [
            _slot("title", 0, [_local(DAILY_20 / "Tin_21_3.jpg")], "DÂN TRÍ / ATP TOUR", "Carlos Alcaraz tiến vào bán kết ATP Finals với thành tích toàn thắng"),
            _slot("title", 0, [_local(DAILY_20 / "Tin_21_1.jpg")], "ATP TOUR", "Hạt giống số một Alexander Zverev chờ đón thử thách từ Daniil Medvedev"),
            _slot("title", 0, [_local(DAILY_20 / "Tin_21_2.jpg")], "ATP TOUR", "Ben Shelton là tay vợt Mỹ trẻ nhất vào bán kết giải từ năm 2004"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_local(DAILY_16 / "Tin_26_10.jpg")], "REUTERS", "Bốn tay vợt xuất sắc nhất lộ diện tại nhà thi đấu Inalpi Arena ở Turin"),
            _slot("sentence", 1, [_local(ROOT / "outputs" / "Orther" / "17.11.2026" / "images" / "v2_sports_world_stage.jpg")], "ATP TOUR", "Các lượt trận cuối bảng Ivan Lendl khép lại không có bất ngờ nào"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_local(DAILY_20 / "Tin_21_12.jpg")], "DÂN TRÍ / ATP TOUR", "Alcaraz bỏ lại nỗi lo cơ đùi trái để hạ Flavio Cobolli chỉ sau hai set"),
            _slot("sentence", 2, [_local(DAILY_19 / "Tin_15_9.jpg")], "ATP TOUR", "Đội ngũ y tế xác nhận ngôi sao Tây Ban Nha đủ thể lực chinh phục ngôi vương"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_local(DAILY_20 / "Tin_21_14.jpg")], "REUTERS", "Daniil Medvedev đánh bại Frances Tiafoe 6-3 và 6-4 ở trận quyết định"),
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_15_2.jpg")], "DÂN TRÍ", "Tay vợt Nga tận dụng tốt mặt sân cứng trong nhà để giành tấm vé cuối"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_local(DAILY_16 / "Tin_26_2.jpg")], "AP PHOTO", "Alcaraz sẽ tái đấu Ben Shelton sau trận chung kết Paris Masters kịch tính"),
            _slot("sentence", 4, [_local(DAILY_20 / "Tin_21_9.jpg")], "ATP TOUR", "Ben Shelton hưng phấn cao độ trong lần đầu tiên dự bán kết ATP Finals"),
            _slot("sentence", 4, [_local(DAILY_20 / "Tin_21_6.jpg")], "REUTERS", "Cặp bán kết còn lại hứa hẹn giằng co giữa Alexander Zverev và Medvedev"),
        ],
    },

    # 20 (100% Giọng Nữ — MỤC TIN VẮN CUỐI VIDEO: CÁC TIN THỂ THAO KHÁC)
    {
        "id": 20,
        "art_id": "art_20",
        "group": "CÁC TIN THỂ THAO KHÁC",
        "title": "Điểm nhanh các tin thể thao đáng chú ý khác",
        "voice_preset": "secondary",
        "summary": (
            "Tại các bảng đấu khác ở U17 World Cup 2026 tối ngày 20 tháng 11, Tây Ban Nha thắng đậm Trung Quốc 5-0, Italia đè bẹp Jamaica 6-0 và Tajikistan vượt qua Cuba với tỷ số 5-3. "
            "Cũng ở sân chơi U17 World Cup, U17 Việt Nam chia tay thủ môn cao một mét 87 Nguyễn Thái Sơn sát giờ thi đấu do chấn thương cổ tay, còn đội trưởng U17 Bỉ tiết lộ toàn đội bị huấn luyện viên cấm chơi máy PlayStation tại Qatar. "
            "Tại giải bóng đá Hạng Nhất quốc gia, câu lạc bộ thành phố Hồ Chí Minh thắng đội đầu bảng Thái Nguyên 1-0 nhờ pha đánh đầu phút bù giờ của Đào Tấn Lộc để nối dài mạch bốn trận toàn thắng, trước khi Đồng Nai của Công Phượng tiếp đón Hà Nội tối nay ở V-League. "
            "Trong nước, tay vợt pickleball số một đơn nam hệ thống APP Mỹ Ronan Camron cùng Drake Palm vừa giao lưu biểu diễn tại Hà Nội, đồng thời Cục Thể dục Thể thao ký kết hợp tác truyền thông số chiến lược với MCV Sport. "
            "Tại đấu trường luật bóng đá quốc tế, đề xuất sửa luật việt vị với khoảng trống rõ ràng của Arsene Wenger đứng trước nguy cơ bị bác bỏ vì thử nghiệm tại Canada khiến các đội lùi sâu phòng ngự hơn. "
            "Ở bóng đá châu Âu đêm qua, Espanyol hạ Athletic Bilbao 1-0 tại vòng 13 La Liga còn Troyes đánh bại Le Havre 3-1 ở vòng 11 Ligue 1. "
            "Trên đường đua Công thức 1 Las Vegas Grand Prix, mưa lớn làm tê liệt buổi chạy thử đầu tiên trước khi tay đua Mercedes George Russell bứt tốc dẫn đầu buổi chạy thử thứ hai vượt qua Pierre Gasly và Charles Leclerc. "
            "Trong làng quần vợt, Hiệp hội Quần vợt Nam chuyên nghiệp ATP vừa phê chuẩn gói tài chính hơn 350 triệu USD áp dụng từ năm 2028, đảm bảo thu nhập tối thiểu 1,1 triệu USD mỗi năm cho nhóm 100 tay vợt hàng đầu. "
            "Khép lại bản tin, câu lạc bộ Gunma Green Wings của chủ công Trần Thị Thanh Thúy bước vào hai trận gặp Aleeza Aichi cuối tuần này với mạch bảy chiến thắng liên tiếp trước khi cô về dự Đại hội toàn quốc, còn Hội đồng Quyền Anh Thế giới WBC chính thức bật đèn xanh cho đại chiến giữa Canelo Alvarez và Willy Hutchinson."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ / ATP / F1",
        "news_source": "ĐIỂM ĐỌC TỔNG HỢP",
        "credit": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "U17 WORLD CUP", "value": "TBN 5-0 • ITA 6-0", "sub": "Trung Quốc và Jamaica thua đậm"},
            "3": {"label": "GIẢI HẠNG NHẤT", "value": "CLB TP.HCM 1-0", "sub": "Thắng trận thứ 4 liên tiếp phút 90+1"},
            "5": {"label": "LUẬT VIỆT VỊ MỚI", "value": "NGUY CƠ BỊ BÁC", "sub": "Thử nghiệm tại Canada phản tác dụng"},
            "7": {"label": "F1 LAS VEGAS GP", "value": "RUSSELL NHANH NHẤT", "sub": "1:47.272 ở buổi chạy thử FP2"},
            "8": {"label": "ATP ONEVISION 2028", "value": "350 TRIỆU USD", "sub": "Top 100 tối thiểu 1,1 triệu USD/năm"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_U17_ESP_2)], "TUỔI TRẺ / FIFA", "Điểm nhanh các tin thể thao trong nước và quốc tế đáng chú ý"),
            _slot("title", 0, [_url(TT_HCM_FIRSTDIV)], "TUỔI TRẺ / HCMFC", "Các kết quả nổi bật tại giải quốc nội và đấu trường châu Âu"),
            _slot("title", 0, [_local(DAILY_02 / "Tin_25_1.jpg")], "SV.LEAGUE", "Cập nhật F1, quần vợt ATP, bóng chuyền và quyền Anh thế giới"),
            # Câu 1: U17 World Cup bảng H, E, F (2 ảnh)
            _slot("sentence", 1, [_url(TT_U17_ESP_2)], "TUỔI TRẺ / FIFA", "U17 Tây Ban Nha thắng áp đảo U17 Trung Quốc 5-0 tại bảng H"),
            _slot("sentence", 1, [_url("https://assets.the-afc.com/2027_AFC_Asian_Cup/Qualifiers/Final_Round/Group_A/MD6/Tajikistan-Philippines/Tajikistan-v-Philippines-Reaction.JPG")], "AFC", "Trong khi đó U17 Tajikistan đánh bại U17 Cuba trong trận cầu 8 bàn thắng"),
            # Câu 2: Thủ môn Thái Sơn & lệnh cấm PlayStation Bỉ (2 ảnh)
            _slot("sentence", 2, [_url("https://cdn2.tuoitre.vn/471584752817336320/2025/4/5/u17-viet-nam-0604-2025-5-17438841633281761322479.jpg")], "TUỔI TRẺ", "Thủ môn cao 1m87 Nguyễn Thái Sơn lỡ U17 World Cup vì chấn thương cổ tay"),
            _slot("sentence", 2, [_url(TT_U17_BI_COACH)], "TUỔI TRẺ", "HLV U17 Bỉ Sven Vermant cấm học trò mang máy PlayStation tới Qatar"),
            # Câu 3: CLB TP.HCM 1-0 Thái Nguyên & Đồng Nai - Hà Nội (2 ảnh)
            _slot("sentence", 3, [_url(TT_HCM_FIRSTDIV)], "TUỔI TRẺ / HCMFC", "Đào Tấn Lộc đánh đầu phút 90+1 giúp CLB TP.HCM hạ đầu bảng Thái Nguyên"),
            _slot("sentence", 3, [_url(TN_DONGNAI_CP)], "THANH NIÊN", "Tối nay Công Phượng cùng Đồng Nai tiếp đón Hà Nội ở vòng 8 V-League"),
            # Câu 4: Pickleball & Cục TDTT - MCV Sport (2 ảnh)
            _slot("sentence", 4, [_url(TN_PICKLE_1)], "THANH NIÊN / BTC", "Ronan Camron và Drake Palm thi đấu biểu diễn pickleball tại Hà Nội"),
            _slot("sentence", 4, [_url(TT_MCV_SIGN)], "TUỔI TRẺ / MCV", "Cục Thể dục Thể thao ký hợp tác truyền thông số với MCV Sport"),
            # Câu 5: Luật việt vị Wenger (2 ảnh)
            _slot("sentence", 5, [_local(DAILY_19 / "Tin_10_3.jpg")], "VNEXPRESS / REUTERS", "Đề xuất luật việt vị mới của Arsene Wenger có nguy cơ bị bác bỏ"),
            _slot("sentence", 5, [_url(VNE_WENGER_1)], "VNEXPRESS / THE TIMES", "Thử nghiệm tại giải Canada khiến các đội bóng lùi sâu phòng ngự hơn"),
            # Câu 6: La Liga & Ligue 1 (2 ảnh)
            _slot("sentence", 6, [_ddgs("RCD Espanyol Athletic Bilbao La Liga football match")], "LA LIGA", "Espanyol giành chiến thắng 1-0 trước Athletic Bilbao tại vòng 13 La Liga"),
            _slot("sentence", 6, [_url("https://prod-media.beinsports.com/image/1795211530506_43bc2b19-1bc2-4419-9a0f-29d8d494b38b.1080.png")], "BEIN SPORTS", "Troyes đánh bại Le Havre 3-1 ở trận đấu sớm vòng 11 Ligue 1"),
            # Câu 7: F1 Las Vegas GP (2 ảnh)
            _slot("sentence", 7, [_ddgs("George Russell Mercedes F1 Las Vegas Grand Prix")], "FORMULA 1", "George Russell đưa chiếc xe Mercedes lên dẫn đầu buổi chạy thử FP2"),
            _slot("sentence", 7, [_url("https://e0.365dm.com/25/02/2048x1152/skysports-charles-leclerc-ferrari_6833841.jpg?20250219161935")], "SKY SPORTS", "Charles Leclerc xếp thứ ba sau Russell và Gasly trên đường phố ướt mưa"),
            # Câu 8: ATP 350 triệu USD (2 ảnh)
            _slot("sentence", 8, [_local(DAILY_20 / "Tin_21_3.jpg")], "DÂN TRÍ / ATP TOUR", "ATP thông qua gói đãi ngộ 350 triệu USD áp dụng từ mùa giải 2028"),
            _slot("sentence", 8, [_local(DAILY_19 / "Tin_15_12.jpg")], "ATP TOUR", "Các tay vợt Top 100 thế giới được đảm bảo thu nhập tối thiểu 1,1 triệu USD"),
            # Câu 9: Thanh Thúy & Canelo Alvarez (2 ảnh)
            _slot("sentence", 9, [_local(DAILY_02 / "Tin_25_4.jpg")], "SV.LEAGUE", "Trần Thị Thanh Thúy cùng Gunma Green Wings giữ chuỗi bảy trận thắng tại Nhật"),
            _slot("sentence", 9, [_ddgs("Canelo Alvarez boxing champion ring fight")], "WBC / SKY SPORTS", "Hội đồng WBC phê chuẩn siêu trận giữa Canelo Alvarez và Willy Hutchinson"),
        ],
    },
]
