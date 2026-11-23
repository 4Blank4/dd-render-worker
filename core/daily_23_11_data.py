# -*- coding: utf-8 -*-
"""
daily_23_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 23.11.2026
(Tổng hợp song hành báo Việt Nam & Thế Giới: 12:00 ngày 22.11 đến 08:11 ngày 23.11.2026).
Cấu trúc ĐỘNG 100% theo mật độ sự kiện thực tế:
  - Intro (00): Song giọng Nữ (Ngọc Huyền #14) & Nam (Minh Quân Pro #15), hide_title=True
  - 16 bản tin chính chi tiết (01–16): mỗi tin 5–6 câu đầy đủ diễn biến, tỷ số, kỷ lục, luân phiên Nam/Nữ
  - Mục 17 (CÁC TIN THỂ THAO KHÁC): 100% Giọng Nữ (Ngọc Huyền #14) điểm nhanh các kết quả phụ trước Outro
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


def _slot(slot_type: str, sent_idx: int, sources: List[tuple[str, str]], credit: str, desc: str) -> Dict[str, Any]:
    return {
        "type": slot_type,
        "sentence_idx": sent_idx,
        "sources": sources,
        "credit": credit,
        "desc": desc,
    }


# ── URL ảnh báo chí sạch gốc 22–23.11.2026 (Việt Nam & Thế Giới) ──

# Đại hội Thể thao toàn quốc 2026 — Bơi lội, Bảng tổng sắp, Billiards, Thể hình, Cầu lông, Bóng đá nam
TN_BOI_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/21a1-17953612379681441534542.jpg"
TN_BOI_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/tnw-1795349643099495148892215585366649514889221558536665e4b60650e3e04a322d89545e5e7c46a-1795354776707972330035.jpg"
TN_BOI_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/tnw-1795349643091495148892215585366649514889221558536665ef47fc891519928b147ca6e0ad674f4-179535477643170142949.jpg"
VNE_BOI_1 = "https://i1-thethao.vnecdn.net/2026/11/22/asdasd-1795352556-9014-1795352600.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=xRabAcyB_YF23g0KVJgPkA"
VNE_BOI_2 = "https://i1-thethao.vnecdn.net/2026/11/22/asdasd-1795352585-1464-1795352599.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=pzWiWZiq3IyQ0cDB3pnG-A"
TT_BOI_WAT = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/edit-watson-nguyen-2-17953545632151583921889.png"
TT_BOI_MT = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2025/12/28/my-tien-5-read-only-1766938450278731222206.jpg"
DT_BOI_AV = "https://cdnphoto.dantri.com.vn/cOWWMC3bYbmAJdIy_r6H2WzqOaI=/zoom/1200_630/2026/11/23/anhvien2t22-11-26-cropped-1795368043678.jpg"

TT_BXH_DH = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/bxh-huy-chuong-22-11-2026-17953619983791923105948.png"
TN_BILL_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/1795343923766147528790956295670147528790956295670a687818cc832b827f0af44d117ecbc53-17953560613441903827357.jpg"
TT_BILL_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/duong-quoc-hoang-billiards-dai-hoi-the-thao-toan-quoc-17953503318171173944975.jpg"
TN_MACH_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/the-hinh-1795343584387629322816.png"
TT_TM_1 = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/22/nguyen-tien-minh-cau-long-dai-hoi-the-thao-toan-quoc-1795363378611877488441-1795365098032713623765-86-0-894-1542-crop-17953651182351151596559.jpeg"
TT_U21_NA = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/hoang-minh-hoi-an-mung-cho-slna-17953674293311163310829.jpeg"

# V-League V8: Đà Nẵng 0-1 Ninh Bình & Hà Tĩnh 2-1 CA TP.HCM
TN_NB_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/hoang-duc-vs-da-nang-nb-dong-nghi-179535103206098012727.jpg"
TN_NB_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/lee-young-jin-minh-tu-17953521326941318214571.jpg"
TN_CA_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/ca-17953513615911017099139.jpg"
TN_CA_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/ca1-1795351361617403281421.jpg"
TT_NM_CC = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/anh-chup-man-hinh-2026-11-23-002013-1795368517286381926905.png"
DT_VL_1 = "https://cdnphoto.dantri.com.vn/jU7JNKkNGFCJ1aGIc19rpRQ10aQ=/thumb_w/1020/2026/11/22/92634701529861317650771296839542015188830575n-1795359028095.jpg"

# U17 Việt Nam vs U17 New Zealand
TN_U17_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/img8804-17953909167141889464279.jpeg"
TN_U17_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/img8799-1795390916576574809588.jpeg"
TN_U17_NL = "https://images2.thanhnien.vn/528068263637045248/2026/11/21/nguyen-luc-1795272710670454801885.jpg"
DT_U17_1 = "https://cdnphoto.dantri.com.vn/TJnMAHf_B-MD4Z6-3NCICmwfA7k=/thumb_w/1020/2026/11/22/u17vn322-11-26-1795365650925.jpeg"
DT_U17_2 = "https://cdnphoto.dantri.com.vn/SPDsz6ec0ttIssVhq5d6alqiMnM=/thumb_w/1020/2026/11/22/u17vn422-11-26-1795365651540.jpeg"

# MMA Bùi Đình Khải & Cờ vua Lê Quang Liêm & Lại Lý Huynh & Minh Vương
TT_MMA_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/17952796922903105331723490236558g7537619067278874637d060650c23407bd9681342021518938c-17953170516471685514126.jpg"
TT_MMA_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/17952900631166680986947116613665g7537619067278874637439e6a5d04b32954374e8cb1abcdc9a9-17953170516541796519370.jpg"
TT_QL_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/21/55659955541888d67aa4ak-1795305068491140224211.jpg"
TT_LLH_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/10/5/lai-ly-huynh-05102026-1791172552954738399323.png"
TT_MV_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/minh-vuong-1795360280412308905372.jpg"
TT_QN_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/qn-17953531202181362642229.jpg"

# Ngoại hạng Anh: Liverpool 4-0 Man Utd & Hull City 2-0 Brighton
TN_LIV_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/2026-11-22t163620z2012732391up1embm1a4j3rrtrmadp3soccer-england-liv-mun-1795369372032233017574.jpg"
TN_LIV_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/2026-11-22t164205z546558491up1embm1ae442rtrmadp3soccer-england-liv-mun-17953700846281679611852.jpg"
VNE_LIV_1 = "https://i1-thethao.vnecdn.net/2026/11/23/AP26326620429647-2961-1795392623.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=AFKgrWmu8cf0_NzXxcM4NQ"
VNE_LIV_2 = "https://i1-thethao.vnecdn.net/2026/11/23/AP26326600469949-2556-1795392796.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=0R-fCD14A-Z5SAF6VpAE5w"
DT_LIV_1 = "https://cdnphoto.dantri.com.vn/2jxSRL9Zo8WmTp7NuXoGvl_ix1s=/thumb_w/1020/2026/11/23/yoro-2-1795387281260.jpg"
SKY_LIV_NGU = "https://e1.365dm.com/26/11/1920x1080/skysports-rio-ngumoha-liverpool_7413795.jpg?20261122181605"
SKY_LIV_YORO = "https://e2.365dm.com/26/11/1920x1080/skysports-leny-yoro-alexander-isak_7413680.jpg?20261122164441"
SKY_LIV_POCH = "https://e2.365dm.com/26/11/1920x1080/skysports-mauricio-pochettino_7413726.jpg?20261122171838"
GDN_LIV_1 = "https://i.guim.co.uk/img/media/eabaf0f7802df08b573f0b7df40105a767d353ce/338_150_2492_1994/master/2492.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=a3c86be864bbd2274aafe3d8d9469eed"
GDN_HULL_1 = "https://i.guim.co.uk/img/media/a031f718e08daf83f40bfd6d6b0d289d49346209/604_120_3916_3133/master/3916.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=7285abd629dca24dc8d2eea8f35ca5f3"
SUN_HULL_2 = "https://www.thescottishsun.co.uk/wp-content/uploads/sites/2/2026/11/oliver-mcburnie-hull-city-celebrates-1124932195_5f2c20.jpg?quality=90&strip=all&w=1024"

# Barcelona 3-2 Villarreal & Serie A & Doué ACL
VNE_BAR_1 = "https://i1-thethao.vnecdn.net/2026/11/22/dag-m1a3540-1795362671-1286-1795362914.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=BvtfVUB7Q7WeTNUyIALqkQ"
VNE_BAR_2 = "https://i1-thethao.vnecdn.net/2026/11/22/AFP-20261122-D8AN42G-v1-HighRe-1554-7400-1795360571.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=vKaFiPXMDpm1JfH0Dz04Bg"
DT_BAR_1 = "https://cdnphoto.dantri.com.vn/0pLah3VIol-xy8gfUDh0SAUTFL4=/thumb_w/1020/2026/11/22/barca2-cropped-1795361407220.jpg"
GDN_BAR_1 = "https://i.guim.co.uk/img/media/e156c5f2d84c63c34abb465b35688771f70fdb64/0_0_2350_1880/master/2350.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=60842459eeba6d39398a426ee3893728"
FI_INT_1 = "https://icdn.football-italia.net/wp-content/uploads/2026/11/Atalanta-Inter-XI.jpg"
UA_INT_2 = "https://cdn-cabinet.ua.news/uploads/images/atalanta_inter_4_4_seria_a_esposito_hat_1795384175147.webp?8186763"
FI_JUV_1 = "https://icdn.football-italia.net/wp-content/uploads/2025/04/Juventus-Lecce-hugs.jpg"
ATH_DOUE_1 = "https://static01.nyt.com/athletic/uploads/wp/2026/11/22071526/GettyImages-2305653320-1-2048x1365.jpg"

# U17 Hàn Quốc & FIFA 2035 & NWSL Kansas City
TN_KOR_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/7101d581-b173-4251-99a8-2410ac957e8bpng-17953628611641116028026.jpg"
TN_KOR_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/14cb70b8-8429-42bd-9dde-2b188e5a73ecpng-1795364563172683876959.jpg"
FGG_UK_35 = "https://footballgroundguide.com/thumbor/iWbflubpyStbY9doONwNtR0x56Q=/2507x2006/smart/filters:format(webp)/https://media.footballgroundguide.com/main/2026/11/imago1076069568h.jpg"
GDN_NWSL_1 = "https://i.guim.co.uk/img/media/546fafdee8a7c55af0f3197c68e9e63455348a3f/311_0_4057_3247/master/4057.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=4a8f4b1555817368509a89d3ae2089c6"

# ATP Finals Alcaraz, F1 Las Vegas GP Verstappen, MotoGP Marc Márquez, LPGA Jeeno Thitikul, MLB Tarik Skubal
SKY_ATP_1 = "https://e2.365dm.com/26/11/1920x1080/sky-sports-tennis-atp-finals_7413906.jpg?20261122200247"
VNE_ATP_1 = "https://i1-thethao.vnecdn.net/2026/11/23/GU6QBIN72ZNZNHUSFL5VVLQ2FQ-1549-1795383861.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=00wS_Xv8oejCjgIgEdEQfw"
VNE_ATP_2 = "https://i1-thethao.vnecdn.net/2026/11/23/zverev-alcaraz-nitto-atp-final-5207-5528-1795383861.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=bWqqCoDY0B0815roG8CcnQ"
DT_ATP_1 = "https://cdnphoto.dantri.com.vn/Oulu0QTY17jhUVzFOScU1uJ4940=/thumb_w/1020/2026/11/23/alcaraz-2-1795388601818.jpg"
DT_ATP_2 = "https://cdnphoto.dantri.com.vn/ArO8KafNGI6BML86cmIP0gVMHT0=/thumb_w/1020/2026/11/23/alcaraz-1-1795388603265.jpg"
GDN_ATP_1 = "https://i.guim.co.uk/img/media/6984924ff8a89514c7d1768a9f1d06d27e7fd5e8/699_0_6990_5592/master/6990.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=133e04ec2d9d31b6dda38b456f9e1088"

GDN_F1_WIN = "https://i.guim.co.uk/img/media/d0a9ab789d250cb38b422c64b38f325f59d9c741/503_0_4225_3380/master/4225.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=0565067df1e95872c05c00e7b4f7639b"
GDN_F1_WAR = "https://i.guim.co.uk/img/media/7b058d455219210daab6a78fc0833fcf02ef0168/0_206_2336_1868/master/2336.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=043d453eaa5d4f0a7582c672b5df02eb"
MS_F1_FER = "https://cdn-7.motorsport.com/images/amp/0JXw4kMY/s1000/lewis-hamilton-charles-leclerc.jpg"
SKY_F1_ALL = "https://e2.365dm.com/26/03/1920x1080/skysports-f1-f1-2026-f1-field_7186813.jpg?20260309102551"
SKY_F1_HAAS = "https://e0.365dm.com/26/11/1920x1080/skysports-rafael-camara-haas_7407635.jpg?20261116094531"

GDN_MOTO_MM = "https://i.guim.co.uk/img/media/2117e7846babfe872897b50715741c9d6e22e48a/457_0_4819_3857/master/4819.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=d1717ff53ca62541b87e37ffd1458840"
MCS_MOTO_MM = "https://motorcyclesports.net/wp-content/uploads/2026/11/marc-marquez-equals-giacomo-agostini-with-record-eighth-motogp-title-at-portuguese-grand-p-1024x683.webp"
MS_MOTO_MM = "https://cdn-1.motorsport.com/images/amp/6b8ZA5w2/s1000/marc-marquez-ducati-team.webp"
BEZ_MOTO = "https://www.motociclismo.es/uploads/s1/15/53/07/68/marco-bezzecchi-ha-culminado-el-doblete-en-portimao.jpeg"

SKY_LPGA_1 = "https://e2.365dm.com/26/11/1920x1080/skysports-jeeno-thitikul-cme-group-tour-champ_7414042.jpg?20261122222312"
SKY_LPGA_2 = "https://e0.365dm.com/26/11/1920x1080/skysports-golf-cme-tour-championship_7414029.jpg?20261122221004"
GDN_MLB_1 = "https://i.guim.co.uk/img/media/43179824af3ae4d1651ab19890a048d52a810d7e/512_0_6130_4904/master/6130.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=20f261dfb21077b52ba9ca334be0b0b1"

# Paredes, Neymar, Darts Price, Sophia Huỳnh, NFL Metcalf
VNE_PAR_1 = "https://iv1.vnecdn.net/thethao/images/web/2026/11/22/nha-vo-dich-world-cup-do-guc-khi-tra-loi-phong-van-1795347418.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=MD0EEaBzByq6om7SXcd_3g"
VNE_PAR_2 = "https://iv1.vnecdn.net/thethao/images/web/2026/11/22/paredes-cung-cac-dong-doi-boca-juniors-nang-cup-1795347640.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=hyvQAdS5BxIiAot3YdAMjQ"
DT_PAR_1 = "https://cdnphoto.dantri.com.vn/xOv2la4F0dAWlqBWGhSifDVlsJI=/thumb_w/1020/2026/11/22/paredes2-1795351544579.jpg"
VNE_NEY_1 = "https://i1-thethao.vnecdn.net/2026/11/22/neymar-jr-bsop-millions-poker-5777-2306-1795339451.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=-PlzJjs0e9Asv0aUmd1_iQ"
VNE_NEY_2 = "https://i1-thethao.vnecdn.net/2026/11/22/AP26186808325707-5466-1795339963.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Fbxc5vu7lpracDHUE4ekFA"
SKY_DART_1 = "https://e0.365dm.com/26/11/1920x1080/skysports-gerwyn-price-darts_7413987.jpg?20261122213041"
SKY_DART_2 = "https://e2.365dm.com/26/11/1920x1080/skysports-price-van-veen_7413997.jpg?20261122214222"
GDN_DART_1 = "https://i.guim.co.uk/img/media/96ff4bbe1b63f81685e8b1f12942277b77085c43/556_584_3811_3050/master/3811.jpg?width=1200&height=900&quality=85&auto=format&fit=crop&s=273ca6db73a89fae97990f32c8f1f15c"
TT_SOPHIA_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/22/sophia-huynh-17953440136291046957035.jpg"
SKY_NFL_MET = "https://e2.365dm.com/26/11/1920x1080/skysports-dk-metcalf_7413981.jpg?20261122211710"
SKY_NFL_STL = "https://e2.365dm.com/26/11/1920x1080/skysports-aaron-rodgers-pittsburgh-steelers_7414036.jpg?20261122221502"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 23.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 23 tháng 11 năm 2026, cập nhật đầy đủ những diễn biến nóng nhất tại Việt Nam và trên toàn thế giới. "
        "Ở đấu trường quốc nội, đường đua bơi Đại hội Thể thao toàn quốc 2026 bùng nổ kỷ lục trong ngày Nguyễn Thị Ánh Viên tái xuất và kình ngư Việt kiều Watson Nguyễn vượt qua Phạm Thanh Bảo, còn ở vòng 8 V-League, Hoàng Đức ghi bàn đưa Ninh Bình chiếm ngôi nhì trong khi trung vệ Nguyễn Nhật Minh rời sân bằng xe cấp cứu. "
        "Trên sân cỏ châu Âu, Liverpool đè bẹp Manchester United 4-0 khiến tân huấn luyện viên Mauricio Pochettino lập kỷ lục ra mắt tệ nhất sau 100 năm, Barcelona thắng ngược Villarreal 3-2 dù Lamine Yamal sút hỏng phạt đền, và Atalanta hòa điên rồ Inter Milan 4-4. "
        "Bên cạnh đó là chức vô địch ATP Finals đầu tiên của Carlos Alcaraz, chiến thắng hỗn loạn của Max Verstappen tại F1 Las Vegas, cột mốc lịch sử tám lần vô địch MotoGP của Marc Márquez, hai kỷ lục tiền thưởng tại Golf và bóng chày MLB cùng nhiều tin thể thao đáng chú ý khác ngay sau đây."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí / BBC Sport / ESPN / Sky Sports / The Guardian",
    "news_source": "VIỆT NAM & THẾ GIỚI",
    "credit": "ĐIỂM ĐỌC TỔNG HỢP",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 23 tháng 11 năm 2026, cập nhật đầy đủ những diễn biến nóng nhất tại Việt Nam và trên toàn thế giới.",
        },
        {
            "voice_preset": "primary",
            "text": "Ở đấu trường quốc nội, đường đua bơi Đại hội Thể thao toàn quốc 2026 bùng nổ kỷ lục trong ngày Nguyễn Thị Ánh Viên tái xuất và kình ngư Việt kiều Watson Nguyễn vượt qua Phạm Thanh Bảo, còn ở vòng 8 V-League, Hoàng Đức ghi bàn đưa Ninh Bình chiếm ngôi nhì trong khi trung vệ Nguyễn Nhật Minh rời sân bằng xe cấp cứu.",
        },
        {
            "voice_preset": "secondary",
            "text": "Trên sân cỏ châu Âu, Liverpool đè bẹp Manchester United 4-0 khiến tân huấn luyện viên Mauricio Pochettino lập kỷ lục ra mắt tệ nhất sau 100 năm, Barcelona thắng ngược Villarreal 3-2 dù Lamine Yamal sút hỏng phạt đền, và Atalanta hòa điên rồ Inter Milan 4-4.",
        },
        {
            "voice_preset": "primary",
            "text": "Bên cạnh đó là chức vô địch ATP Finals đầu tiên của Carlos Alcaraz, chiến thắng hỗn loạn của Max Verstappen tại F1 Las Vegas, cột mốc lịch sử tám lần vô địch MotoGP của Marc Márquez, hai kỷ lục tiền thưởng tại Golf và bóng chày MLB cùng nhiều tin thể thao đáng chú ý khác ngay sau đây.",
        },
    ],
    "stat_badges": {
        "1": {"label": "BẢN TIN NGÀY", "value": "23.11.2026", "sub": "Toàn cảnh Việt Nam & Thế giới"},
        "2": {"label": "ĐẠI HỘI 2026", "value": "MƯA KỶ LỤC", "sub": "Ánh Viên HCB • Watson Nguyễn phá KLQG"},
        "3": {"label": "ANFIELD DẬY SÓNG", "value": "LIVERPOOL 4-0 MU", "sub": "Ác mộng đầu tiên của Pochettino"},
    },
    "slots": [
        # Câu 1 (4 ảnh)
        _slot("sentence", 1, [_url(TN_BOI_1)], "THANH NIÊN", "Nguyễn Thị Ánh Viên và Võ Thị Mỹ Tiên tạo màn so tài cảm xúc tại hồ bơi Phú Thọ"),
        _slot("sentence", 1, [_url(SKY_LIV_NGU)], "SKY SPORTS", "Rio Ngumoha bùng nổ giúp Liverpool vùi dập Manchester United 4-0 tại Anfield"),
        _slot("sentence", 1, [_url(SKY_ATP_1)], "SKY SPORTS", "Carlos Alcaraz nâng cúp vô địch ATP Finals 2026 lần đầu tiên trong sự nghiệp"),
        _slot("sentence", 1, [_url(GDN_F1_WIN)], "THE GUARDIAN", "Max Verstappen lên ngôi tại chặng đua F1 Las Vegas đầy hỗn loạn"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(VNE_BOI_1)], "VNEXPRESS", "Ngày mở màn môn bơi Đại hội Toàn quốc 2026 chứng kiến nhiều kỷ lục quốc gia bị xô đổ"),
        _slot("sentence", 2, [_url(TT_BOI_WAT)], "TUỔI TRẺ", "Watson Nguyễn và Phạm Thanh Bảo cùng phá kỷ lục quốc gia cự ly 50 mét ếch nam"),
        _slot("sentence", 2, [_url(TN_NB_1)], "THANH NIÊN", "Nguyễn Hoàng Đức ghi bàn giúp Ninh Bình giành trọn ba điểm trước Đà Nẵng"),
        _slot("sentence", 2, [_url(TT_NM_CC)], "TUỔI TRẺ / FPT PLAY", "Trung vệ Nguyễn Nhật Minh gặp chấn thương nặng phải rời sân bằng xe cấp cứu"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url(SKY_LIV_POCH)], "SKY SPORTS", "HLV Mauricio Pochettino trải qua ngày ra mắt ác mộng ngay tại Anfield"),
        _slot("sentence", 3, [_url(VNE_BAR_1)], "VNEXPRESS / AFP", "Barcelona thắng ngược Villarreal 3-2 dù Lamine Yamal đá hỏng phạt đền hiệp một"),
        _slot("sentence", 3, [_url(FI_INT_1)], "FOOTBALL ITALIA", "Atalanta và Inter Milan tạo trận cầu tám bàn thắng kịch tính tại Serie A"),
        _slot("sentence", 3, [_url(ATH_DOUE_1)], "THE ATHLETIC", "PSG đối mặt hung tin chấn thương dây chằng của ngôi sao trẻ Désiré Doué"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_url(GDN_ATP_1)], "THE GUARDIAN", "Carlos Alcaraz khuất phục số một thế giới Alexander Zverev sau hai set đấu"),
        _slot("sentence", 4, [_url(GDN_MOTO_MM)], "THE GUARDIAN", "Marc Márquez san bằng kỷ lục tám chức vô địch hạng cao nhất của Giacomo Agostini"),
        _slot("sentence", 4, [_url(SKY_LPGA_1)], "SKY SPORTS", "Jeeno Thitikul giành danh hiệu LPGA Tour Championship thứ ba liên tiếp"),
        _slot("sentence", 4, [_url(GDN_MLB_1)], "THE GUARDIAN", "Tarik Skubal ký hợp đồng kỷ lục lịch sử 450 triệu USD với New York Mets"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — BƠI LỘI ĐẠI HỘI TOÀN QUỐC 2026)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Bơi lội Đại hội Toàn quốc mưa kỷ lục: Ánh Viên giành HCB tái xuất, Watson Nguyễn vượt Phạm Thanh Bảo",
        "summary": (
            "Đêm chung kết đầu tiên của môn bơi tại Đại hội Thể thao toàn quốc 2026 tối ngày 22 tháng 11 tại hồ bơi Phú Thọ đã chứng kiến cơn mưa kỷ lục quốc gia lẫn kỷ lục đại hội bị xô đổ. "
            "Sau bốn năm vắng bóng ở các giải đấu đỉnh cao, tượng đài Nguyễn Thị Ánh Viên khoác áo đoàn Quân đội tạo sức hút đặc biệt ở cự ly sở trường 200 mét hỗn hợp nữ và xuất sắc giành huy chương bạc với thông số 2 phút 16,30 giây. "
            "Chiến thắng thuộc về đương kim số một Việt Nam Võ Thị Mỹ Tiên của đoàn Tây Ninh với thành tích 2 phút 14,38 giây, phá sâu kỷ lục đại hội 2 phút 19,43 giây do chính Ánh Viên nắm giữ từ năm 2018. "
            "Ở chung kết 50 mét ếch nam được chờ đợi nhất, kình ngư Việt kiều Mỹ 21 tuổi Watson Nguyễn của đoàn An Giang đạt thành tích 27,09 giây để giành huy chương vàng trước Phạm Thanh Bảo của Vĩnh Long về nhì với 27,50 giây, giúp cả hai cùng vượt qua kỷ lục quốc gia cũ 27,70 giây. "
            "Bên cạnh đó, kình ngư 17 tuổi Nguyễn Thúy Hiền tỏa sáng với hai huy chương vàng cùng hai kỷ lục mới ở các cự ly 50 mét ếch nữ đạt 31,73 giây và 100 mét tự do nữ đạt 56,10 giây. "
            "Đường đua xanh còn ghi nhận tình huống hy hữu tại chung kết 100 mét tự do nam khi Trần Văn Nguyễn Quốc của Đà Nẵng và Lương Jerremie Loic Nino của Thành phố Hồ Chí Minh chạm đích cùng lúc ở mốc 50,03 giây nên cùng nhận huy chương vàng."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "credit": "THANH NIÊN / VNEXPRESS",
        "stat_badges": {
            "2": {"label": "200M HỖN HỢP NỮ", "value": "MỸ TIÊN 2:14.38", "sub": "Ánh Viên HCB với 2 phút 16,30"},
            "4": {"label": "50M ẾCH NAM", "value": "WATSON 27.09", "sub": "Phá KLQG cũ 27.70 của Thanh Bảo"},
            "5": {"label": "NGUYỄN THÚY HIỀN", "value": "2 HCV + 2 KỶ LỤC", "sub": "50m ếch 31.73s • 100m tự do 56.10s"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_BOI_1)], "THANH NIÊN", "Nguyễn Thị Ánh Viên và Võ Thị Mỹ Tiên rạng rỡ sau chung kết 200m hỗn hợp nữ"),
            _slot("title", 0, [_url(VNE_BOI_1)], "VNEXPRESS", "Các kình ngư tranh tài quyết liệt trong đêm chung kết đầu tiên tại hồ bơi Phú Thọ"),
            _slot("title", 0, [_url(TT_BOI_WAT)], "TUỔI TRẺ", "Watson Nguyễn phá kỷ lục quốc gia 50m ếch nam trong cuộc đối đầu với Phạm Thanh Bảo"),
            _slot("sentence", 1, [_url(VNE_BOI_1)], "VNEXPRESS", "Hàng loạt kỷ lục quốc gia và Đại hội được thiết lập ngay tối 22 tháng 11"),
            _slot("sentence", 1, [_url(VNE_BOI_2)], "VNEXPRESS", "Khán đài CLB Bơi lặn Phú Thọ chật kín khán giả theo dõi ngày thi đấu đỉnh cao"),
            _slot("sentence", 2, [_url(DT_BOI_AV)], "DÂN TRÍ", "Ở tuổi 30, Ánh Viên vẫn cải thiện gần 11 giây so với vòng loại để giành HCB"),
            _slot("sentence", 2, [_url(TN_BOI_1)], "THANH NIÊN", "Ánh Viên chủ động ôm chúc mừng đàn em Võ Thị Mỹ Tiên ngay dưới làn bơi"),
            _slot("sentence", 3, [_url(TT_BOI_MT)], "TUỔI TRẺ", "Võ Thị Mỹ Tiên phá sâu kỷ lục đại hội tồn tại suốt tám năm của Ánh Viên"),
            _slot("sentence", 4, [_url(TN_BOI_2)], "THANH NIÊN", "Watson Nguyễn khẳng định đẳng cấp nhà vô địch 50m ếch quốc gia Mỹ"),
            _slot("sentence", 4, [_url(TT_BOI_WAT)], "TUỔI TRẺ", "Phạm Thanh Bảo giữ thế trận giằng co nhưng vẫn về sau Watson 0,41 giây"),
            _slot("sentence", 5, [_url(TN_BOI_3)], "THANH NIÊN", "Kình ngư trẻ Nguyễn Thúy Hiền xô đổ cả kỷ lục quốc gia lẫn đại hội ở cự ly 50m ếch nữ"),
            _slot("sentence", 6, [_url(VNE_BOI_2)], "VNEXPRESS", "Lần đầu tiên sau nhiều năm nội dung 100m tự do nam chứng kiến hai VĐV cùng đoạt HCV"),
        ],
    },

    # 02 (Nữ — TOÀN CẢNH ĐẠI HỘI TOÀN QUỐC NGÀY 22/11)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "TP.HCM vượt mốc 109 huy chương dẫn đầu Đại hội, Hoàng Sao bị loại sốc, Tiến Minh gây sốt & Phạm Văn Mách giành HCB",
        "summary": (
            "Theo bảng tổng sắp huy chương tính đến tối ngày 22 tháng 11, đoàn chủ nhà Thành phố Hồ Chí Minh trở thành đơn vị đầu tiên chạm mốc 109 huy chương với 41 vàng, 25 bạc và 43 đồng nhờ phong độ bùng nổ ở hai môn thế mạnh canoeing đạt 10 huy chương vàng và vovinam đạt tám huy chương vàng. "
            "Xếp ngay phía sau là đoàn Hà Nội với 34 huy chương vàng trong tổng số 96 huy chương, còn Công an Nhân dân đứng thứ ba với 23 huy chương vàng, xếp trên Quân Đội và Cần Thơ cùng có 19 huy chương vàng. "
            "Tại nhà thi đấu Nguyễn Du ở môn billiards và snooker, cú sốc lớn nhất ngày khai màn nổ ra khi cơ thủ số một Việt Nam Dương Quốc Hoàng biệt danh Hoàng Sao dẫn trước Chu Việt Hoàng tới 8-6 ở trận chạm 9 nhưng lại bỏ lỡ bi số 6 để thua ngược 8-9 đầy cay đắng tại vòng 16 pool 9 bi. "
            "Ở chung kết môn thể hình hạng cân đến 60 kilôgam diễn ra tại nhà thi đấu Rạch Miễu, lực sĩ kỳ cựu Phạm Văn Mách thi đấu đầy nỗ lực song đành nhận huy chương bạc khi xếp sau nhà vô địch đang độ sung mãn là Phạm Văn Phước của đoàn Đà Nẵng. "
            "Trong khi đó, trên sân cầu lông Hồ Xuân Hương, tay vợt 43 tuổi Nguyễn Tiến Minh làm bùng nổ khán đài với pha đánh cầu không cần nhìn đậm chất nghệ sĩ để giành chiến thắng thuyết phục trước đối thủ trẻ Hà Nội là Nguyễn Thế Ngọc. "
            "Cũng trong chiều ngày 22 tháng 11 tại sân Bình Dương, môn bóng đá nam lứa U21 chính thức khởi tranh với chiến thắng đậm 3-0 của Đồng Tháp trước An Giang, còn đương kim vô địch Nghệ An bị Công an Nhân dân cầm hòa 1-1."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "TUỔI TRẺ / THANH NIÊN",
        "stat_badges": {
            "1": {"label": "TỔNG SẮP 22/11", "value": "TP.HCM 41 HCV", "sub": "109 huy chương • Hà Nội 34 HCV"},
            "3": {"label": "SỐC BILLIARDS", "value": "HOÀNG SAO 8-9", "sub": "Dẫn 8-6 thua ngược Chu Việt Hoàng"},
            "5": {"label": "CẦU LÔNG 43 TUỔI", "value": "TIẾN MINH GÂY SỐT", "sub": "Cú đánh không cần nhìn ngoạn mục"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_BXH_DH)], "TUỔI TRẺ", "Bảng tổng sắp huy chương Đại hội Thể thao toàn quốc 2026 tối 22 tháng 11"),
            _slot("title", 0, [_url(TN_BILL_1)], "THANH NIÊN", "Dương Quốc Hoàng dừng bước đầy tiếc nuối ở nội dung pool 9 bi đơn nam"),
            _slot("title", 0, [_url(TT_TM_1)], "TUỔI TRẺ", "Tay vợt 43 tuổi Nguyễn Tiến Minh trình diễn kỹ thuật cầu lông mãn nhãn"),
            _slot("sentence", 1, [_url(TT_BXH_DH)], "TUỔI TRẺ", "Canoeing và vovinam đóng góp gần một nửa số HCV của đoàn TP.HCM"),
            _slot("sentence", 2, [_url(TT_BXH_DH)], "TUỔI TRẺ", "Hà Nội, Công an Nhân dân và Quân Đội bám đuổi quyết liệt trong nhóm đầu"),
            _slot("sentence", 3, [_url(TT_BILL_1)], "TUỔI TRẺ", "Hoàng Sao đánh mất lợi thế dẫn 8-6 và nhìn Chu Việt Hoàng thắng ngược 9-8"),
            _slot("sentence", 3, [_url(TN_BILL_1)], "THANH NIÊN", "Chu Việt Hoàng tiếp tục vượt qua Lô Văn Hoàn để ghi tên vào bán kết"),
            _slot("sentence", 4, [_url(TN_MACH_1)], "THANH NIÊN", "Lực sĩ sinh năm 1976 Phạm Văn Mách giành HCB trước đối thủ trẻ Phạm Văn Phước"),
            _slot("sentence", 5, [_url(TT_TM_1)], "TUỔI TRẺ", "Khán giả thích thú với pha xử lý cầu sau lưng đậm đẳng cấp của Nguyễn Tiến Minh"),
            _slot("sentence", 6, [_url(TT_U21_NA)], "TUỔI TRẺ", "Hoàng Minh Hợi ghi bàn mở tỷ số nhưng U21 Nghệ An bị CAND gỡ hòa 1-1"),
        ],
    },

    # 03 (Nam — V-LEAGUE VÒNG 8 NGÀY 22/11)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "V-LEAGUE 2026-2027",
        "title": "V-League Vòng 8: Hoàng Đức đưa Ninh Bình lên ngôi nhì, Hà Tĩnh hạ Công an TP.HCM 2-1 & Nhật Minh đi cấp cứu",
        "summary": (
            "Hai trận đấu muộn khép lại vòng 8 V-League tối ngày 22 tháng 11 đã chứng kiến những diễn biến nghẹt thở trên sân Chi Lăng và sân Hà Tĩnh. "
            "Tiếp đón Ninh Bình trong ngày ra mắt tân huấn luyện viên trưởng Lee Young-jin, đội chủ nhà Đà Nẵng thi đấu kỷ luật nhưng vẫn gục ngã bởi pha đột phá và dứt điểm chuẩn xác ở phút 24 của đội trưởng Nguyễn Hoàng Đức, chấp nhận thất bại tối thiểu 0-1. "
            "Chiến thắng giúp Ninh Bình đạt 16 điểm để đòi lại ngôi nhì bảng và rút ngắn khoảng cách xuống còn ba điểm so với đội đầu bảng Thép Xanh Nam Định, trong khi Đà Nẵng giậm chân ở vị trí nguy hiểm với chín điểm. "
            "Ở trận đấu cùng giờ tại Hà Tĩnh, đội khách Công an Thành phố Hồ Chí Minh sớm chịu tổn thất nặng ngay phút 14 khi trung vệ sinh năm 2003 Nguyễn Nhật Minh va chạm mạnh vùng đầu với tiền đạo Atshimene đến mức chảy máu và phải rời sân bằng xe cấp cứu. "
            "Sau khi Daniel Passira đánh đầu mở tỷ số phút 51 và Olaha Mạnh Đức gỡ hòa cho đội khách, tiền vệ Luiz Antonio tung cú sút quyết đoán ở phút 89 ấn định chiến thắng 2-1 cho Hồng Lĩnh Hà Tĩnh, đẩy Công an Thành phố Hồ Chí Minh vào chuỗi ba trận liên tiếp trắng tay. "
            "Trên bảng xếp hạng sau tám vòng đấu, Nam Định dẫn đầu với 19 điểm, ba đội Sông Lam Nghệ An, Công an Hà Nội và Hà Tĩnh cùng có 14 điểm, còn Thành phố Đồng Nai đứng cuối bảng với vỏn vẹn bốn điểm."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / TUỔI TRẺ / DÂN TRÍ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "ĐÀ NẴNG 0-1 NINH BÌNH", "value": "HOÀNG ĐỨC 24'", "sub": "Ngày ra mắt buồn của HLV Lee Young-jin"},
            "4": {"label": "SỰ CỐ HÀ TĨNH", "value": "NHẬT MINH CẤP CỨU", "sub": "Va chạm vùng đầu ở phút 14"},
            "6": {"label": "BXH SAU VÒNG 8", "value": "NAM ĐỊNH 19 Đ", "sub": "Ninh Bình 16đ • Đồng Nai 4đ"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_NB_1)], "THANH NIÊN", "Nguyễn Hoàng Đức ghi bàn thắng quý như vàng giúp Ninh Bình đánh bại Đà Nẵng 1-0"),
            _slot("title", 0, [_url(TN_CA_1)], "THANH NIÊN", "Hồng Lĩnh Hà Tĩnh giành chiến thắng kịch tính 2-1 trước Công an TP.HCM"),
            _slot("title", 0, [_url(TT_NM_CC)], "TUỔI TRẺ / FPT PLAY", "Trung vệ Nguyễn Nhật Minh rời sân bằng xe cấp cứu sau pha va chạm mạnh"),
            _slot("sentence", 1, [_url(DT_VL_1)], "DÂN TRÍ", "Vòng 8 V-League khép lại với nhiều biến động ở cả nhóm đầu lẫn nhóm cuối bảng"),
            _slot("sentence", 2, [_url(TN_NB_1)], "THANH NIÊN", "Hoàng Đức tự phát động rồi dứt điểm ghi bàn mở tỷ số ở phút 24 trên sân Chi Lăng"),
            _slot("sentence", 2, [_url(TN_NB_2)], "THANH NIÊN", "Tân HLV Lee Young-jin không thể giúp Đà Nẵng giữ điểm ngay trận đầu cầm quân"),
            _slot("sentence", 3, [_url(DT_VL_1)], "DÂN TRÍ", "Ninh Bình trở lại vị trí thứ hai với 16 điểm, chỉ kém đội đầu bảng Nam Định ba điểm"),
            _slot("sentence", 4, [_url(TT_NM_CC)], "TUỔI TRẺ / FPT PLAY", "Thủ môn Lê Giang Patrik vội vã gọi đội ngũ y tế khi thấy Nhật Minh chảy máu vùng đầu"),
            _slot("sentence", 5, [_url(TN_CA_1)], "THANH NIÊN", "Luiz Antonio tỏa sáng đúng phút 89 mang về ba điểm trọn vẹn cho đội bóng núi Hồng"),
            _slot("sentence", 5, [_url(TN_CA_2)], "THANH NIÊN", "HLV Arthur Diles đối mặt áp lực lớn khi Công an TP.HCM thua liền ba vòng V-League"),
            _slot("sentence", 6, [_url(TN_NB_1)], "THANH NIÊN", "Cuộc đua vô địch lẫn trụ hạng hứa hẹn căng thẳng trước giai đoạn giữa lượt đi"),
        ],
    },

    # 04 (Nữ — U17 VIỆT NAM VS U17 NEW ZEALAND 22H30 TỐI NAY)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Việt Nam quyết đấu New Zealand lúc 22h30 tối nay tranh vé vào vòng knock-out World Cup",
        "summary": (
            "Vào lúc 22 giờ 30 tối nay ngày 23 tháng 11, đội tuyển U17 Việt Nam sẽ bước vào lượt trận thứ hai bảng G tại Vòng chung kết U17 World Cup 2026 gặp U17 New Zealand với mục tiêu bắt buộc giành chiến thắng. "
            "Trước giờ bóng lăn, trang chủ FIFA World Cup gây chú ý khi ca ngợi siêu phẩm đá phạt góc thành bàn ở phút 84 của Chu Ngọc Nguyễn Lực vào lưới U17 Bỉ là một bàn thắng Olympic cực kỳ hiếm gặp ở sân chơi thế giới. "
            "Về phía đối thủ, huấn luyện viên trưởng U17 New Zealand cũng dành sự tôn trọng đặc biệt cho pha lập công của Nguyễn Lực nhưng khẳng định đại diện châu Đại Dương buộc phải đánh bại Việt Nam sau thất bại 0-3 trước Mali. "
            "Huấn luyện viên Cristiano Roland đã tổ chức mổ băng kỹ thuật nhằm khắc phục sai sót hàng thủ ở trận gặp Bỉ, nhắc các học trò giữ sự tỉnh táo, khiêm tốn và đặc biệt cảnh giác trước những tiền đạo cao 1,94 mét của New Zealand trong các tình huống bóng bổng. "
            "Với thể thức mới dành cho 48 đội tuyển, ngoài hai đội nhất nhì mỗi bảng còn có tám đội xếp thứ ba có thành tích tốt nhất vào vòng 32 đội, nên một thắng lợi tối nay sẽ giúp U17 Việt Nam rộng cửa tự định đoạt tấm vé lịch sử."
        ),
        "source": "Thanh Niên / Dân Trí / Tuổi Trẻ",
        "news_source": "THANH NIÊN / DÂN TRÍ",
        "credit": "DÂN TRÍ / THANH NIÊN",
        "stat_badges": {
            "1": {"label": "22H30 TỐI NAY", "value": "U17 VN VS NZ", "sub": "Lượt trận hai bảng G tại Qatar"},
            "2": {"label": "FIFA WORLD CUP", "value": "OLYMPIC GOAL", "sub": "Khen ngợi siêu phẩm của Nguyễn Lực"},
            "4": {"label": "HLV ROLAND NHẮC NHỞ", "value": "PHÒNG BÓNG BỔNG", "sub": "Cảnh giác cầu thủ NZ cao 1,94m"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_U17_1)], "DÂN TRÍ", "U17 Việt Nam tích cực rèn chiến thuật hướng tới trận gặp New Zealand tối nay"),
            _slot("title", 0, [_url(TN_U17_1)], "THANH NIÊN", "HLV Cristiano Roland truyền sự tự tin nhưng yêu cầu học trò giữ đôi chân trên mặt đất"),
            _slot("title", 0, [_url(TN_U17_NL)], "THANH NIÊN", "Chu Ngọc Nguyễn Lực được FIFA nhắc tên nhờ bàn thắng phạt góc mẫu mực"),
            _slot("sentence", 1, [_url(DT_U17_1)], "DÂN TRÍ", "Cả Việt Nam và New Zealand đều chưa có điểm sau lượt trận ra quân bảng G"),
            _slot("sentence", 2, [_url(TN_U17_NL)], "THANH NIÊN", "Cú đá phạt góc phút 84 vào lưới U17 Bỉ được FIFA gọi bằng thuật ngữ Bàn thắng Olympic"),
            _slot("sentence", 3, [_url(DT_U17_2)], "DÂN TRÍ", "U17 New Zealand đang xếp cuối bảng với hiệu số âm ba nên chắc chắn dâng cao tấn công"),
            _slot("sentence", 4, [_url(TN_U17_1)], "THANH NIÊN", "HLV Roland phân tích kỹ những tình huống bóng bổng và thể hình vượt trội của đối thủ"),
            _slot("sentence", 5, [_url(TN_U17_2)], "THANH NIÊN", "Ba điểm tối nay sẽ mở toang cánh cửa đi tiếp cho thầy trò HLV Roland tại World Cup"),
        ],
    },

    # 05 (Nam — VÕ THUẬT MMA LION CHAMPIONSHIP)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "VÕ THUẬT MMA",
        "title": "Bùi Đình Khải tung loạt đòn chỏ, hạ knock-out nhà vô địch Muay thế giới Lê Hoàng Đức ngay hiệp 1",
        "summary": (
            "Đêm võ thuật Lion Championship tại Bắc Ninh chứng kiến màn so tài đỉnh cao cho chiếc đai vô địch hạng cân 52 kilôgam giữa võ sĩ trẻ Bùi Đình Khải và tượng đài Lê Hoàng Đức. "
            "Dù đối đầu với võ sĩ từng hai lần vô địch Muay thế giới và hai lần vô địch châu Á, Bùi Đình Khải sinh năm 2001 vẫn nhập cuộc đầy tự tin và chủ động tìm cách kéo trận đấu xuống mặt sàn. "
            "Sau lần đầu kéo ngã bị Hoàng Đức thoát đòn siết cổ, Đình Khải ở nửa cuối hiệp một tiếp tục quật ngã thành công đối thủ xuống sàn rồi kiểm soát hoàn toàn thế nằm trên. "
            "Từ vị thế áp đảo, tay đấm trẻ tung liên tiếp loạt đòn đấm búa và cùi chỏ uy lực khiến trọng tài buộc phải can thiệp dừng trận đấu, giúp Đình Khải giành chiến thắng knock-out kỹ thuật ngay hiệp một trong cuộc đấu dự kiến kéo dài năm hiệp. "
            "Với chuỗi ba trận thắng knock-out liên tiếp để lên ngôi vô địch, Bùi Đình Khải dự kiến sẽ đối đầu với người thách đấu Nguyễn Phú Thịnh trong trận bảo vệ đai vào năm 2027."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "LION CHAMPIONSHIP", "value": "ĐAI 52 KG", "sub": "Diễn ra sôi động tại Bắc Ninh"},
            "4": {"label": "KẾT THÚC HIỆP 1", "value": "TKO HOÀNG ĐỨC", "sub": "Loạt đòn đấm búa và cùi chỏ"},
            "5": {"label": "THÁCH ĐẤU 2027", "value": "3 TRẬN TKO", "sub": "Chờ so găng Nguyễn Phú Thịnh"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_MMA_1)], "TUỔI TRẺ", "Bùi Đình Khải chiếm thế kiểm soát trên mặt sàn trước Lê Hoàng Đức tại Bắc Ninh"),
            _slot("title", 0, [_url(TT_MMA_2)], "TUỔI TRẺ", "Khoảnh khắc chiến thắng thuyết phục giúp Bùi Đình Khải đăng quang đai 52 kg"),
            _slot("sentence", 1, [_url(TT_MMA_1)], "TUỔI TRẺ", "Trận tranh đai Lion Championship 52 kg thu hút sự quan tâm đặc biệt của giới võ thuật"),
            _slot("sentence", 2, [_url(TT_MMA_2)], "TUỔI TRẺ", "Lê Hoàng Đức mang theo bề dày thành tích hai lần vô địch Muay thế giới"),
            _slot("sentence", 3, [_url(TT_MMA_1)], "TUỔI TRẺ", "Pha quật ngã ở nửa cuối hiệp một mở ra bước ngoặt quyết định cho Đình Khải"),
            _slot("sentence", 4, [_url(TT_MMA_2)], "TUỔI TRẺ", "Trọng tài cho dừng trận ngay hiệp đầu trước loạt đòn chỏ dồn dập của võ sĩ sinh năm 2001"),
            _slot("sentence", 5, [_url(TT_MMA_1)], "TUỔI TRẺ", "Bùi Đình Khải sẽ chuẩn bị cho màn bảo vệ đai đầu tiên gặp Nguyễn Phú Thịnh năm 2027"),
        ],
    },

    # 06 (Nữ — CỜ VUA, CỜ TƯỚNG & HẠNG NHẤT QUỐC GIA)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "CỜ VUA & BÓNG ĐÁ NỘI",
        "title": "Lê Quang Liêm dự siêu giải 250000 USD, Lại Lý Huynh đấu cờ đôi Đại hội & Minh Vương tái xuất ấn tượng",
        "summary": (
            "Ngay sau khi đòi lại vị trí trong Top 15 thế giới tại Budapest, kỳ thủ số một Việt Nam Lê Quang Liêm lập tức bước vào tranh tài tại siêu giải cờ nhanh Jerusalem Masters 2026 diễn ra từ ngày 23 đến 25 tháng 11. "
            "Giải đấu quy tụ 12 kỳ thủ tinh hoa gồm năm siêu đại kiện tướng hàng đầu với tổng quỹ tiền thưởng lên tới 250000 USD, trong đó nhà vô địch sẽ nhận 101000 USD. "
            "Ở bộ môn cờ tướng Đại hội Thể thao toàn quốc tại Vũng Tàu, nhà vô địch thế giới Lại Lý Huynh kết hợp cùng Nguyễn Minh Nhật Quang ở nội dung cờ đôi tiêu chuẩn nhưng vấp phải sự cạnh tranh vô cùng quyết liệt từ các kỳ thủ mạnh trong nước. "
            "Trên sân cỏ vòng 8 Giải hạng Nhất quốc gia tối ngày 22 tháng 11, tiền vệ Trần Minh Vương đánh dấu ngày tái xuất sau chấn thương gãy tay bằng cú treo bóng đá phạt phút 28 giúp Công an Nhân dân mở tỷ số trước Thép Cần Thơ, góp phần ngắt mạch trận thất vọng. "
            "Cùng vòng đấu tại sân Bà Rịa, câu lạc bộ Quy Nhơn United dù bị Đại học Văn Hiến chọc thủng lưới trước ở phút 28 bởi pha lập công của Ilias Namli vẫn bản lĩnh ngược dòng giành chiến thắng chung cuộc."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "JERUSALEM MASTERS", "value": "250000 USD", "sub": "Vô địch nhận 101000 USD (23-25/11)"},
            "4": {"label": "GIẢI HẠNG NHẤT V8", "value": "MINH VƯƠNG TRỞ LẠI", "sub": "Kiến tạo giúp CAND thắng Thép Cần Thơ"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_QL_1)], "TUỔI TRẺ", "Lê Quang Liêm liên tiếp thử lửa ở các siêu giải cờ vua quốc tế"),
            _slot("title", 0, [_url(TT_LLH_1)], "TUỔI TRẺ", "Đương kim vô địch cờ tướng thế giới Lại Lý Huynh tranh tài ở Đại hội 2026"),
            _slot("title", 0, [_url(TT_MV_1)], "TUỔI TRẺ", "Trần Minh Vương tỏa sáng ngay ngày trở lại màu áo Công an Nhân dân"),
            _slot("sentence", 1, [_url(TT_QL_1)], "TUỔI TRẺ", "Quang Liêm duy trì phong độ cao sau chiến thắng trước Ian Nepomniachtchi"),
            _slot("sentence", 2, [_url(TT_QL_1)], "TUỔI TRẺ", "Jerusalem Masters 2026 là cuộc đọ trí của 12 kỳ thủ hàng đầu thế giới"),
            _slot("sentence", 3, [_url(TT_LLH_1)], "TUỔI TRẺ", "Đôi TP.HCM của Lại Lý Huynh gặp không ít khó khăn ngay từ những ván mở màn"),
            _slot("sentence", 4, [_url(TT_MV_1)], "TUỔI TRẺ", "Minh Vương bình phục chấn thương gãy tay từ vòng 3 và nhanh chóng tạo khác biệt"),
            _slot("sentence", 5, [_url(TT_QN_1)], "TUỔI TRẺ", "Quy Nhơn United chơi phản công sắc bén để ngược dòng thắng Đại học Văn Hiến"),
        ],
    },

    # 07 (Nam — LIVERPOOL 4-0 MANCHESTER UNITED)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "NGOẠI HẠNG ANH",
        "title": "Liverpool đè bẹp Man Utd 4-0 tại Anfield — Pochettino lập kỷ lục ra mắt tệ nhất sau 100 năm",
        "summary": (
            "Trận đại chiến nước Anh tại sân Anfield tối ngày 22 tháng 11 đã biến thành cơn ác mộng thực sự cho tân huấn luyện viên Mauricio Pochettino ngay trong ngày đầu tiên ông dẫn dắt Manchester United. "
            "Áp dụng sơ đồ ba hậu vệ 3-4-3, Quỷ đỏ sớm vỡ trận ngay phút thứ tám khi trung vệ trẻ Leny Yoro nhận thẻ đỏ trực tiếp vì pha phạm lỗi ngăn cản tình huống dẫn tới bàn thắng rõ rệt. "
            "Ngay từ quả đá phạt sau đó, Dominik Szoboszlai sút tung lưới mở tỷ số trước khi Florian Wirtz nhân đôi cách biệt ở phút 13, tạo thế trận một chiều hoàn toàn cho đội chủ nhà. "
            "Sang hiệp hai, tài năng trẻ Rio Ngumoha thi đấu bùng nổ ghi bàn nâng tỷ số rồi Victor Muñoz ấn định chiến thắng tưng bừng 4-0 giúp Liverpool vững vàng trong nhóm bốn đội dẫn đầu. "
            "Theo thống kê của Opta, Pochettino trở thành huấn luyện viên đầu tiên sau đúng một thế kỷ cân bằng kỷ lục thua đậm nhất ngày ra mắt Man Utd của Lal Hilditch hồi tháng 10 năm 1926, đẩy đội chủ sân Old Trafford tụt xuống vị trí thứ 19 áp chót bảng xếp hạng. "
            "Sau trận đấu, dù Pochettino cho rằng tấm thẻ đỏ là khắc nghiệt, cựu đội trưởng Roy Keane vẫn chỉ trích dữ dội sự bạc nhược của toàn đội trong tiếng vỗ tay khó hiểu cuối trận."
        ),
        "source": "BBC Sport / Sky Sports / The Guardian / VnExpress / Dân Trí",
        "news_source": "BBC SPORT / SKY SPORTS / VNEXPRESS",
        "credit": "SKY SPORTS / REUTERS",
        "stat_badges": {
            "2": {"label": "THẺ ĐỎ PHÚT 8", "value": "LENY YORO OUT", "sub": "Bước ngoặt khiến MU vỡ trận sớm"},
            "4": {"label": "LIVERPOOL 4-0 MU", "value": "NGUMOHA RỰC SÁNG", "sub": "Szoboszlai • Wirtz • Ngumoha • Muñoz"},
            "5": {"label": "KỶ LỤC 100 NĂM", "value": "HẠNG 19 BXH", "sub": "Thất bại ra mắt tệ nhất từ năm 1926"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_LIV_NGU)], "SKY SPORTS", "Rio Ngumoha ăn mừng bàn thắng trong chiến thắng hủy diệt 4-0 của Liverpool"),
            _slot("title", 0, [_url(SKY_LIV_POCH)], "SKY SPORTS", "HLV Mauricio Pochettino chết lặng bên đường biên ngay trận ra mắt Quỷ đỏ"),
            _slot("title", 0, [_url(SKY_LIV_YORO)], "SKY SPORTS", "Thẻ đỏ của Leny Yoro ở phút thứ tám đặt dấu chấm hết cho toan tính của đội khách"),
            _slot("sentence", 1, [_url(VNE_LIV_1)], "VNEXPRESS / AP", "Chưa đầy bốn ngày sau khi chia tay tuyển Mỹ tiếp quản MU, Pochettino nếm trái đắng"),
            _slot("sentence", 2, [_url(DT_LIV_1)], "DÂN TRÍ / REUTERS", "Trọng tài rút thẻ đỏ trực tiếp cho Leny Yoro sau pha tranh chấp với Alexander Isak"),
            _slot("sentence", 3, [_url(TN_LIV_1)], "THANH NIÊN / REUTERS", "Florian Wirtz dễ dàng nhân đôi cách biệt lên 2-0 chỉ sau 13 phút bóng lăn"),
            _slot("sentence", 3, [_url(TN_LIV_2)], "THANH NIÊN / REUTERS", "Hàng thủ chắp vá với sơ đồ 3-4-3 của Man Utd liên tiếp bị Liverpool xé toang"),
            _slot("sentence", 4, [_url(SKY_LIV_NGU)], "SKY SPORTS", "Rio Ngumoha và Victor Muñoz ghi thêm hai bàn trong hiệp hai hoàn tất thắng lợi 4-0"),
            _slot("sentence", 5, [_url(GDN_LIV_1)], "THE GUARDIAN", "Man Utd rơi xuống vị trí thứ 19 với áp lực khổng lồ bủa vây tân HLV người Argentina"),
            _slot("sentence", 6, [_url(VNE_LIV_2)], "VNEXPRESS / AP", "Pochettino và các học trò rời Anfield trong tâm trạng nặng nề cùng làn sóng chỉ trích"),
        ],
    },

    # 08 (Nữ — HULL CITY 2-0 BRIGHTON)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "NGOẠI HẠNG ANH",
        "title": "Hull City tạo địa chấn hạ Brighton 2-0 bằng hai bàn thắng phút bù giờ, thủ môn Tzolakis hóa người hùng",
        "summary": (
            "Một bất ngờ thú vị khác tại vòng 11 Ngoại hạng Anh đã diễn ra tối ngày 22 tháng 11 khi câu lạc bộ Hull City xuất sắc quật ngã Brighton với tỷ số 2-0 đầy kịch tính. "
            "Trong suốt phần lớn thời gian trận đấu, Brighton kiểm soát thế trận và liên tục dồn ép nhưng mọi cơ hội đều bị chặn đứng bởi phong độ xuất thần của thủ môn Konstantinos Tzolakis. "
            "Người gác đền vừa vượt qua ám ảnh thất bại đậm ở trận trước đã thực hiện hàng loạt pha bay người cản phá không tưởng để giữ sạch lưới cho đội chủ nhà. "
            "Bước ngoặt xảy ra khi hậu vệ João Costinha của Brighton nhận thẻ đỏ rời sân, mở ra cơ hội để tiền đạo Oli McBurnie bùng nổ với cú đúp bàn thắng chớp nhoáng ở các phút bù giờ 90 cộng 2 và 90 cộng 5. "
            "Chiến thắng nghẹt thở giúp thầy trò huấn luyện viên Jakirovic tạo bước nhảy vọt tinh thần quan trọng, đồng thời khiến Brighton nối dài nỗi thất vọng dù chơi lấn lướt hơn."
        ),
        "source": "BBC Sport / The Guardian / Sky Sports",
        "news_source": "BBC SPORT / GUARDIAN / SKY SPORTS",
        "credit": "THE GUARDIAN / SCOTTISH SUN",
        "stat_badges": {
            "2": {"label": "NGƯỜI HÙNG KHUNG GỖ", "value": "TZOLAKIS RỰC SÁNG", "sub": "Cứu thua hàng loạt pha dứt điểm"},
            "4": {"label": "BÙNG NỔ BÙ GIỜ", "value": "MCBURNIE 90+2, 90+5", "sub": "Hull City thắng 2-0 trước 10 người"},
        },
        "slots": [
            _slot("title", 0, [_url(GDN_HULL_1)], "THE GUARDIAN", "Oli McBurnie vỡ òa cảm xúc sau cú đúp quyết định ở thời gian bù giờ"),
            _slot("title", 0, [_url(SUN_HULL_2)], "SCOTTISH SUN", "Hai pha lập công phút 90+2 và 90+5 nhấn chìm hoàn toàn Brighton"),
            _slot("sentence", 1, [_url(GDN_HULL_1)], "THE GUARDIAN", "Hull City kiên cường chống đỡ trước khi tung đòn kết liễu ở những giây cuối"),
            _slot("sentence", 2, [_ddgs("Konstantinos Tzolakis goalkeeper save football")], "BBC SPORT", "Thủ thành Konstantinos Tzolakis xứng đáng là chốt chặn đáng tin cậy nhất trận"),
            _slot("sentence", 3, [_url(SUN_HULL_2)], "SCOTTISH SUN", "Huấn luyện viên Jakirovic hết lời khen ngợi bản lĩnh vượt khó của thủ môn người Hy Lạp"),
            _slot("sentence", 4, [_url(GDN_HULL_1)], "THE GUARDIAN", "Brighton mất người từ thẻ đỏ của Costinha và sụp đổ hoàn toàn trong năm phút bù giờ"),
            _slot("sentence", 5, [_url(SUN_HULL_2)], "SCOTTISH SUN", "CĐV Hull City ăn mừng cuồng nhiệt chiến thắng 2-0 ngoạn mục trên sân nhà"),
        ],
    },

    # 09 (Nam — BARCELONA 3-2 VILLARREAL)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "LA LIGA 2026-2027",
        "title": "Lamine Yamal sút hỏng phạt đền, Barcelona vẫn ngược dòng thắng nghẹt thở Villarreal 3-2 giữ đỉnh bảng",
        "summary": (
            "Tiếp đón Villarreal tại vòng 13 La Liga tối ngày 22 tháng 11, Barcelona trải qua màn rượt đuổi tỷ số thót tim ngay trên sân nhà Spotify Camp Nou. "
            "Đội bóng xứ Catalonia bất ngờ bị dội hai gáo nước lạnh liên tiếp trong hiệp một sau các pha lập công của Tajon Buchanan và Tani Oluwaseyi bên phía đội khách. "
            "Cơ hội rút ngắn cách biệt đến ở phút 23 khi VAR cho Barca hưởng phạt đền, nhưng tiền đạo 19 tuổi Lamine Yamal lại sút bóng trúng cột dọc phải, qua đó vượt Fernando Torres để trở thành cầu thủ trẻ nhất lịch sử La Liga ba lần sút hỏng phạt đền ở tuổi 19 năm 132 ngày. "
            "Không hề nao núng sau giờ nghỉ, đoàn quân của huấn luyện viên Hansi Flick vùng lên mạnh mẽ và san bằng tỷ số 2-2 nhờ hai pha lập công của Gerard Martín cùng Fermín López. "
            "Kịch tính khép lại bằng bàn phản lưới nhà của hậu vệ Pau Navarro bên phía Villarreal, ấn định màn ngược dòng thắng 3-2 giúp Barcelona giữ vững ngôi đầu bảng La Liga với ba điểm nhiều hơn đại kình địch Real Madrid."
        ),
        "source": "The Guardian / VnExpress / Dân Trí",
        "news_source": "THE GUARDIAN / VNEXPRESS / DÂN TRÍ",
        "credit": "VNEXPRESS / AFP / GUARDIAN",
        "stat_badges": {
            "3": {"label": "KỶ LỤC KHÔNG MONG MUỐN", "value": "YAMAL HỎNG 11M", "sub": "3 lần đá hỏng ở tuổi 19 năm 132 ngày"},
            "5": {"label": "BARCA 3-2 VILLARREAL", "value": "GIỮ NGÔI ĐẦU", "sub": "Hơn Real Madrid 3 điểm trên BXH"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_BAR_1)], "VNEXPRESS / AFP", "Lamine Yamal ôm mặt tiếc nuối sau cú sút phạt đền dội cột dọc ở phút 23"),
            _slot("title", 0, [_url(GDN_BAR_1)], "THE GUARDIAN", "Cầu thủ Barcelona bùng nổ trong hiệp hai hoàn tất cuộc lội ngược dòng 3-2"),
            _slot("title", 0, [_url(DT_BAR_1)], "DÂN TRÍ", "Barca duy trì khoảng cách ba điểm trước Real Madrid trên đỉnh bảng La Liga"),
            _slot("sentence", 1, [_url(DT_BAR_1)], "DÂN TRÍ", "Trận đấu trên sân Spotify Camp Nou diễn ra cởi mở với năm bàn thắng được ghi"),
            _slot("sentence", 2, [_url(GDN_BAR_1)], "THE GUARDIAN", "Villarreal gây sốc cho hàng thủ chủ nhà bằng hai bàn dẫn trước ngay trong hiệp một"),
            _slot("sentence", 3, [_url(VNE_BAR_1)], "VNEXPRESS / AFP", "Đây là lần hỏng phạt đền thứ ba trong bảy lần thực hiện của Yamal tại La Liga"),
            _slot("sentence", 3, [_url(VNE_BAR_2)], "VNEXPRESS / AFP", "Ở tuổi 19 năm 132 ngày, Yamal phá cột mốc cũ của tiền đạo Fernando Torres"),
            _slot("sentence", 4, [_url(GDN_BAR_1)], "THE GUARDIAN", "Gerard Martín và Fermín López liên tiếp ghi bàn kéo Barcelona trở lại thế cân bằng"),
            _slot("sentence", 5, [_url(DT_BAR_1)], "DÂN TRÍ", "Pha phản lưới của Pau Navarro mang về trọn vẹn ba điểm quý giá cho thầy trò Hansi Flick"),
        ],
    },

    # 10 (Nữ — SERIE A & CHẤN THƯƠNG DÉSIRÉ DOUÉ)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "SERIE A & CHÂU ÂU",
        "title": "Atalanta hòa điên rồ Inter Milan 4-4, AC Milan và Juventus đại thắng; PSG mất Désiré Doué hết mùa",
        "summary": (
            "Sân cỏ Italy tối ngày 22 tháng 11 chứng kiến bữa tiệc bàn thắng mãn nhãn, tâm điểm là trận hòa điên rồ 4-4 giữa chủ nhà Atalanta và Inter Milan tại Bergamo. "
            "Tài năng trẻ Francesco Pio Esposito tỏa sáng rực rỡ với cú hat-trick ở các phút 16, 32 và 52 cùng bàn thắng từ chấm phạt đền của Petar Sučić giúp Inter nhiều lần dẫn trước hai bàn. "
            "Tuy nhiên, Atalanta chiến đấu ngoan cường nhờ các bàn thắng của Eljif Elmas, cú đúp của Charles De Ketelaere trước khi cựu tiền vệ Franck Kessié sút thành công quả 11 mét phút 90 cộng 1 để giữ lại một điểm kịch tính. "
            "Ở hai trận đấu khác tại Serie A, AC Milan dễ dàng đè bẹp Frosinone 5-1 với pha độc diễn ghi bàn đẳng cấp của Christian Pulisic cùng các pha lập công của Gonçalo Ramos và Ardon Jashari để tiến vào Top 4, còn Juventus vùi dập Venezia 4-0 nhờ Nick Woltemade, Teun Koopmeiners, Juan Cabal và Randal Kolo Muani. "
            "Tại Pháp, câu lạc bộ Paris Saint-Germain xác nhận hung tin chấn thương nặng nhất mùa giải khi ngôi sao trẻ Désiré Doué bị đứt hoàn toàn dây chằng chéo trước đầu gối trong trận thắng Nice 3-2. "
            "Doué sẽ phải lên bàn mổ trong ít ngày tới và chính thức nói lời chia tay phần còn lại của mùa giải, giáng đòn mạnh vào lực lượng hàng công PSG."
        ),
        "source": "BBC Sport / ESPN / The Guardian / Football Italia",
        "news_source": "BBC SPORT / ESPN / THE GUARDIAN",
        "credit": "FOOTBALL ITALIA / THE ATHLETIC",
        "stat_badges": {
            "2": {"label": "ATALANTA 4-4 INTER", "value": "ESPOSITO HAT-TRICK", "sub": "Kessié gỡ hòa 11m phút 90+1"},
            "4": {"label": "MILAN 5-1 • JUVE 4-0", "value": "BÙNG NỔ SERIE A", "sub": "Pulisic, Ramos, Kolo Muani ghi bàn"},
            "5": {"label": "HUNG TIN PSG", "value": "DOUÉ ĐỨT ACL", "sub": "Phải phẫu thuật, nghỉ hết mùa giải"},
        },
        "slots": [
            _slot("title", 0, [_url(FI_INT_1)], "FOOTBALL ITALIA", "Cuộc rượt đuổi tỷ số tám bàn giữa Atalanta và Inter Milan làm rung chuyển Serie A"),
            _slot("title", 0, [_url(ATH_DOUE_1)], "THE ATHLETIC", "Chấn thương đứt dây chằng chéo trước buộc Désiré Doué sớm khép lại mùa giải"),
            _slot("sentence", 1, [_url(FI_INT_1)], "FOOTBALL ITALIA", "New Balance Arena chứng kiến một trong những trận cầu hay nhất mùa giải Serie A"),
            _slot("sentence", 2, [_url(UA_INT_2)], "UA NEWS", "Chân sút trẻ Francesco Pio Esposito lập hat-trick ngoạn mục cho Inter Milan"),
            _slot("sentence", 3, [_url(FI_INT_1)], "FOOTBALL ITALIA", "Quả phạt đền lạnh lùng phút 90+1 của Franck Kessié giúp Atalanta giật lại một điểm"),
            _slot("sentence", 4, [_url(FI_JUV_1)], "FOOTBALL ITALIA", "Juventus thắng tưng bừng 4-0 trước Venezia còn AC Milan hạ Frosinone 5-1"),
            _slot("sentence", 5, [_url(ATH_DOUE_1)], "THE ATHLETIC", "PSG đối diện cơn khủng hoảng nhân sự sau ca đứt dây chằng ACL của Désiré Doué"),
            _slot("sentence", 6, [_url(ATH_DOUE_1)], "THE ATHLETIC", "Trước Doué, nhà vô địch nước Pháp cũng mất Khvicha Kvaratskhelia vì chấn thương"),
        ],
    },

    # 11 (Nam — U17 WORLD CUP, FIFA 2035 & NWSL CHAMPIONSHIP)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "BÓNG ĐÁ THẾ GIỚI",
        "title": "U17 Hàn Quốc hủy diệt 6-0, Pháp thua sốc Saudi Arabia; Anh sắp đăng cai World Cup nữ 2035 & Kansas City vô địch Mỹ",
        "summary": (
            "Tại đấu trường U17 World Cup 2026 tối ngày 22 tháng 11, đội tuyển U17 Hàn Quốc phô diễn sức mạnh vượt trội với tỷ lệ kiểm soát bóng 80 phần trăm để đè bẹp U17 New Caledonia 6-0, trong đó chân sút Kim Ji-woo lập hat-trick giúp đội bóng xứ kim chi sớm giành vé vào vòng 32 đội. "
            "Bất ngờ lớn nhất lượt trận đến từ bảng đấu của U17 Pháp khi đội bóng trẻ áo lam gục ngã 0-1 trước Saudi Arabia, trong khi U17 Argentina vượt qua Mozambique với tỷ số 2-1. "
            "Ở bình diện bóng đá nữ thế giới, Liên đoàn Bóng đá Thế giới FIFA dự kiến chính thức phê chuẩn Vương quốc Anh gồm Anh, Scotland, Xứ Wales và Bắc Ireland làm chủ nhà World Cup nữ 2035 trong Đại hội bất thường tại Zurich ngày 23 tháng 11 do đây là hồ sơ đăng cai duy nhất. "
            "Tại chung kết giải vô địch bóng đá nữ nhà nghề Mỹ NWSL Championship 2026 diễn ra ở sân Audi Field, Kansas City Current xuất sắc đánh bại Washington Spirit 2-1 để lần đầu tiên nâng cao chiếc cúp vô địch. "
            "Tiền vệ kỳ cựu Vanessa DiBernardo ghi siêu phẩm đá phạt góc mở tỷ số và đoạt danh hiệu cầu thủ xuất sắc nhất trận, trước khi Debinha ghi bàn quyết định dập tắt nỗ lực gỡ hòa muộn của Trinity Rodman."
        ),
        "source": "BBC Sport / The Guardian / ESPN / Thanh Niên",
        "news_source": "BBC SPORT / THE GUARDIAN / THANH NIÊN",
        "credit": "THANH NIÊN / THE GUARDIAN",
        "stat_badges": {
            "1": {"label": "U17 WORLD CUP", "value": "HÀN QUỐC 6-0", "sub": "Pháp thua sốc Saudi Arabia 0-1"},
            "3": {"label": "WORLD CUP NỮ 2035", "value": "VƯƠNG QUỐC ANH", "sub": "Ứng viên chủ nhà duy nhất được FIFA duyệt"},
            "4": {"label": "NWSL CHAMPIONSHIP", "value": "KANSAS CITY 2-1", "sub": "Chức vô địch Mỹ đầu tiên trong lịch sử"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_KOR_1)], "THANH NIÊN", "U17 Hàn Quốc áp đảo hoàn toàn để sớm giành quyền vào vòng knock-out World Cup"),
            _slot("title", 0, [_url(FGG_UK_35)], "FOOTBALL GROUND GUIDE", "Sân Wembley sẵn sàng dẫn đầu kế hoạch đăng cai World Cup nữ 2035 tại Vương quốc Anh"),
            _slot("title", 0, [_url(GDN_NWSL_1)], "THE GUARDIAN", "Kansas City Current lần đầu vô địch NWSL Championship sau chiến thắng 2-1"),
            _slot("sentence", 1, [_url(TN_KOR_1)], "THANH NIÊN", "Kim Ji-woo ghi ba bàn đưa U17 Hàn Quốc đạt sáu điểm tuyệt đối đứng đầu bảng B"),
            _slot("sentence", 2, [_url(TN_KOR_2)], "THANH NIÊN", "Saudi Arabia tạo cú sốc khi hạ U17 Pháp 1-0 còn Argentina thắng Mozambique 2-1"),
            _slot("sentence", 3, [_url(FGG_UK_35)], "FOOTBALL GROUND GUIDE", "Đại hội bất thường FIFA tại Zurich ngày 23 tháng 11 bỏ phiếu xác nhận quyền đăng cai"),
            _slot("sentence", 4, [_url(GDN_NWSL_1)], "THE GUARDIAN", "Kansas City Current khép lại cơn khát danh hiệu bằng chiến thắng trước Washington Spirit"),
            _slot("sentence", 5, [_url(GDN_NWSL_1)], "THE GUARDIAN", "Cú đá phạt góc thành bàn của DiBernardo tạo đà cho ngôi vương xứng đáng"),
        ],
    },

    # 12 (Nữ — ATP FINALS 2026: CARLOS ALCARAZ VÔ ĐỊCH)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "QUẦN VỢT ATP FINALS",
        "title": "Carlos Alcaraz đánh bại số một thế giới Alexander Zverev 6-2, 7-6(7) lần đầu vô địch ATP Finals",
        "summary": (
            "Trận chung kết giải quần vợt danh giá ATP Finals 2026 tại nhà thi đấu Inalpi Arena ở Turin tối ngày 22 tháng 11 đã khép lại với chiến thắng thuyết phục thuộc về tay vợt người Tây Ban Nha Carlos Alcaraz. "
            "Chạm trán đối thủ số một thế giới Alexander Zverev từng hai lần vô địch giải đấu cuối năm, Alcaraz nhập cuộc áp đảo và dễ dàng khép lại set một với tỷ số cách biệt 6-2. "
            "Kịch tính đẩy lên cao trào trong set hai khi Zverev vùng lên dữ dội để đưa trận đấu vào loạt tie-break căng thẳng, thậm chí nắm tới ba cơ hội kết thúc set nhưng Alcaraz vẫn bản lĩnh cứu thua ngoạn mục trước khi ấn định tỷ số 9-7. "
            "Chiến thắng sau hai giờ thi đấu giúp tay vợt Tây Ban Nha chấm dứt bốn năm chờ đợi chiếc cúp ATP Finals đầu tiên trong sự nghiệp, đồng thời nối dài mạch 14 trận bất bại cùng ba danh hiệu liên tiếp ở cuối mùa giải. "
            "Ở nội dung đánh đôi tại Turin, bộ đôi lần đầu góp mặt gồm Theo Arribage và Albano Olivetti cũng tạo bất ngờ đẹp khi đăng quang ngôi vô địch."
        ),
        "source": "BBC Sport / Sky Sports / The Guardian / VnExpress / Dân Trí",
        "news_source": "BBC SPORT / SKY SPORTS / VNEXPRESS",
        "credit": "SKY SPORTS / VNEXPRESS / AP",
        "stat_badges": {
            "2": {"label": "CHUNG KẾT TURIN", "value": "ALCARAZ 6-2, 7-6", "sub": "Đánh bại số 1 thế giới Zverev"},
            "3": {"label": "BẢN LĨNH TIE-BREAK", "value": "CỨU 3 SET-POINT", "sub": "Thắng nghẹt thở 9-7 ở loạt đánh cân não"},
            "4": {"label": "PHONG ĐỘ HỦY DIỆT", "value": "14 TRẬN THẮNG", "sub": "Chức vô địch ATP Finals đầu tiên"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_ATP_1)], "SKY SPORTS", "Carlos Alcaraz lần đầu bước lên bục vinh quang tại ATP Finals ở Turin"),
            _slot("title", 0, [_url(VNE_ATP_1)], "VNEXPRESS / AP", "Alcaraz quỳ sụp ăn mừng sau cú trái tay quyết định đánh bại Zverev"),
            _slot("title", 0, [_url(GDN_ATP_1)], "THE GUARDIAN", "Tay vợt Tây Ban Nha thể hiện đẳng cấp đỉnh cao trước đối thủ số một thế giới"),
            _slot("sentence", 1, [_url(DT_ATP_1)], "DÂN TRÍ / AP", "Không khí cuồng nhiệt tại Inalpi Arena trong đêm hạ màn mùa giải quần vợt nam 2026"),
            _slot("sentence", 2, [_url(VNE_ATP_2)], "VNEXPRESS / AP", "Alcaraz hoàn toàn áp đảo Zverev ở set mở màn với những pha điều bóng uy lực"),
            _slot("sentence", 3, [_url(DT_ATP_2)], "DÂN TRÍ / AP", "Bản lĩnh thép giúp Alcaraz hóa giải ba set-point của Zverev trong loạt tie-break"),
            _slot("sentence", 4, [_url(SKY_ATP_1)], "SKY SPORTS", "Danh hiệu ATP Finals bổ sung mảnh ghép còn thiếu vào bộ sưu tập đồ sộ của Alcaraz"),
            _slot("sentence", 5, [_url(VNE_ATP_1)], "VNEXPRESS / AP", "Alcaraz chạy lên khán đài ôm chặt đội ngũ huấn luyện sau khoảnh khắc lịch sử"),
        ],
    },

    # 13 (Nam — F1 LAS VEGAS GP 2026)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "ĐUA XE FORMULA 1",
        "title": "F1 Las Vegas GP hỗn loạn với 35 lần đổi ngôi đầu: Max Verstappen thắng chặng, Ferrari nội chiến & Russell đâm rào",
        "summary": (
            "Chặng đua đêm Formula 1 Las Vegas Grand Prix ngày 22 tháng 11 đã mang đến một trong những cuộc đua hỗn loạn nhất mùa giải khi ghi nhận tới 35 lần thay đổi vị trí dẫn đầu sau 50 vòng chạy. "
            "Nhà đương kim vô địch Max Verstappen của Red Bull Racing giữ được cái đầu lạnh xuyên suốt các màn bám đuổi bằng lực hút gió để cán đích đầu tiên, xếp trên bộ đôi đội McLaren là Lando Norris về nhì và Oscar Piastri về ba. "
            "Tâm điểm tranh cãi bùng phát ở vòng 38 tại khúc cua số bảy khi Charles Leclerc cố gắng vượt vào làn trong nhưng va chạm trực diện với người đồng đội Ferrari là Lewis Hamilton, khiến chiếc xe của Hamilton xoay vòng giữa đường đua. "
            "Sự cố nội bộ khiến Leclerc nhận án phạt 10 giây tụt xuống hạng 10 còn Hamilton nhận phạt tương tự về đích thứ bảy, làm lãnh đội Fred Vasseur tức giận gọi màn va chạm này là hoàn toàn không thể chấp nhận được. "
            "Ngoài ra, tay đua George Russell của Mercedes gặp tai nạn đâm rào ở những vòng cuối và chỉ về thứ chín sau đồng đội trẻ Kimi Antonelli xếp thứ tư, kéo theo màn đấu khẩu gay gắt với Verstappen sau khi chặng đua khép lại. "
            "Cũng liên quan tới Formula 1, tài năng trẻ Rafael Camara vừa quyết định hy sinh cuộc đua vô địch F2 để thay thế thi đấu hai chặng cuối mùa giải F1 trong màu áo đội đua Haas."
        ),
        "source": "Formula 1 / BBC Sport / The Guardian / Sky Sports",
        "news_source": "FORMULA 1 / BBC SPORT / THE GUARDIAN",
        "credit": "THE GUARDIAN / MOTORSPORT",
        "stat_badges": {
            "2": {"label": "F1 LAS VEGAS GP", "value": "35 LẦN ĐỔI NGÔI", "sub": "Verstappen thắng trước Norris & Piastri"},
            "3": {"label": "NỘI CHIẾN FERRARI", "value": "LECLERC TÔNG HAMILTON", "sub": "Vòng 38 • Vasseur gọi là không chấp nhận"},
            "5": {"label": "KHẨU CHIẾN & TAI NẠN", "value": "RUSSELL ĐÂM RÀO", "sub": "Căng thẳng nảy lửa với Verstappen"},
        },
        "slots": [
            _slot("title", 0, [_url(GDN_F1_WIN)], "THE GUARDIAN", "Max Verstappen lần thứ ba giành chiến thắng trên đường phố đêm Las Vegas"),
            _slot("title", 0, [_url(MS_F1_FER)], "MOTORSPORT", "Nội bộ Ferrari căng thẳng tột độ sau cú va chạm giữa Leclerc và Hamilton"),
            _slot("title", 0, [_url(GDN_F1_WAR)], "THE GUARDIAN", "Max Verstappen và George Russell tiếp tục đẩy màn khẩu chiến lên đỉnh điểm"),
            _slot("sentence", 1, [_url(SKY_F1_ALL)], "SKY SPORTS", "Đường đua tốc độ cao tại Las Vegas chứng kiến 35 lần đổi ngôi đầu nghẹt thở"),
            _slot("sentence", 2, [_url(GDN_F1_WIN)], "THE GUARDIAN", "Verstappen cùng hai tay đua McLaren là Norris và Piastri chia nhau ba vị trí trên bục podium"),
            _slot("sentence", 3, [_url(MS_F1_FER)], "MOTORSPORT", "Pha tấn công mạo hiểm ở cua số bảy vòng 38 khiến cả hai xe Ferrari trả giá đắt"),
            _slot("sentence", 4, [_url(MS_F1_FER)], "MOTORSPORT", "Lãnh đội Fred Vasseur triệu tập gấp cuộc họp khẩn phê bình Charles Leclerc"),
            _slot("sentence", 5, [_url(GDN_F1_WAR)], "THE GUARDIAN", "George Russell đâm rào cuối chặng nhưng vẫn tranh cãi quyết liệt với Verstappen"),
            _slot("sentence", 6, [_url(SKY_F1_HAAS)], "SKY SPORTS", "Tài năng trẻ Rafael Camara nắm cơ hội thử sức ở hai chặng F1 cuối cùng đội Haas"),
        ],
    },

    # 14 (Nữ — MOTOGP PORTIMÃO 2026: MARC MÁRQUEZ VÔ ĐỊCH LẦN THỨ 8)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "ĐUA XE MOTOGP",
        "title": "Lịch sử MotoGP 2026: Marc Márquez cán đích thứ 8 tại Bồ Đào Nha, san bằng kỷ lục tám lần vô địch của Agostini",
        "summary": (
            "Đường đua quốc tế Algarve tại Portimão, Bồ Đào Nha tối ngày 22 tháng 11 đã chính thức ghi dấu một trong những cột mốc vĩ đại nhất lịch sử môn đua mô tô MotoGP. "
            "Ở cuộc đua chính trên đường khô ráo, tay đua Marco Bezzecchi của đội Aprilia hoàn tất cú đúp hoàn hảo trong tuần lễ thi đấu khi cán đích đầu tiên, xếp ngay trên người đồng đội Jorge Martín về nhì và Raúl Fernández đứng thứ ba. "
            "Tuy nhiên, mọi ánh đèn sân khấu và sự ngưỡng mộ đều hướng về ngôi sao đội Ducati là Marc Márquez khi anh điều khiển chiếc xe an toàn qua vạch đích ở vị trí thứ tám. "
            "Bởi trước chặng đấu chỉ cần nằm trong nhóm chín tay đua dẫn đầu là đủ điều kiện đăng quang sớm một vòng, chiến thuật tỉnh táo giúp Marc Márquez chính thức đoạt danh hiệu vô địch thế giới hạng cao nhất lần thứ tám trong sự nghiệp. "
            "Thành tích phi thường này giúp tay đua 33 tuổi người Tây Ban Nha san bằng kỷ lục mọi thời đại tám chức vô địch thế giới hạng cao nhất của huyền thoại Italy Giacomo Agostini."
        ),
        "source": "BBC Sport / ESPN / The Guardian / Crash.net",
        "news_source": "BBC SPORT / ESPN / THE GUARDIAN",
        "credit": "THE GUARDIAN / MOTORSPORT",
        "stat_badges": {
            "2": {"label": "CHẶNG BỒ ĐÀO NHA", "value": "BEZZECCHI VÔ ĐỊCH", "sub": "Jorge Martín nhì • Raúl Fernández ba"},
            "4": {"label": "CÁN ĐÍCH THỨ 8", "value": "8 LẦN VÔ ĐỊCH", "sub": "Đăng quang sớm trước 1 vòng đấu"},
            "5": {"label": "ĐI VÀO HUYỀN THOẠI", "value": "NGANG AGOSTINI", "sub": "San bằng kỷ lục mọi thời đại MotoGP"},
        },
        "slots": [
            _slot("title", 0, [_url(GDN_MOTO_MM)], "THE GUARDIAN", "Marc Márquez vỡ òa cảm xúc khi chính thức chạm mốc tám lần vô địch hạng cao nhất"),
            _slot("title", 0, [_url(MCS_MOTO_MM)], "MOTORCYCLE SPORTS", "Tay đua Tây Ban Nha san bằng tượng đài Giacomo Agostini ngay tại Portimão"),
            _slot("sentence", 1, [_url(MS_MOTO_MM)], "MOTORSPORT", "Chặng Bồ Đào Nha khép lại hành trình hồi sinh thần kỳ trong màu áo đội Ducati"),
            _slot("sentence", 2, [_url(BEZ_MOTO)], "MOTOCICLISMO", "Marco Bezzecchi giành chiến thắng thuyết phục sau màn cạnh tranh sát sao với Jorge Martín"),
            _slot("sentence", 3, [_url(MCS_MOTO_MM)], "MOTORCYCLE SPORTS", "Márquez tụt xuống nhóm giữa sau pha xuất phát nhưng kiên nhẫn giữ vững vị trí thứ tám"),
            _slot("sentence", 4, [_url(GDN_MOTO_MM)], "THE GUARDIAN", "Thứ hạng tám vừa đủ giúp anh nâng cúp vô địch thế giới lần thứ tám trước một chặng"),
            _slot("sentence", 5, [_url(MS_MOTO_MM)], "MOTORSPORT", "Giới chuyên môn đánh giá chức vô địch năm 2026 là màn đăng quang ấn tượng nhất của Márquez"),
        ],
    },

    # 15 (Nam — KỶ LỤC TIỀN THƯỞNG LPGA & MLB)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "GOLF & BÓNG CHÀY MLB",
        "title": "Jeeno Thitikul lập hat-trick vô địch LPGA vượt Annika Sörenstam; Tarik Skubal ký hợp đồng kỷ lục 450 triệu USD",
        "summary": (
            "Thể thao quốc tế rạng sáng ngày 23 tháng 11 chứng kiến hai cột mốc tiền thưởng chưa từng có trong lịch sử môn golf nữ lẫn bóng chày nhà nghề Mỹ. "
            "Tại vòng chung kết giải đấu hạ màn mùa giải LPGA CME Group Tour Championship ở Florida, tay golf người Thái Lan Jeeno Thitikul đánh xuất sắc âm bảy gậy với 65 gậy không mắc bất kỳ lỗi bogey nào để kết thúc ở điểm âm 24. "
            "Thành tích vượt qua Akie Iwai xếp nhì với âm 22 và số một thế giới Nelly Korda xếp ba giúp Thitikul bỏ túi bốn triệu USD tiền thưởng, lập hat-trick vô địch ba năm liên tiếp và chính thức vượt huyền thoại Annika Sörenstam dẫn đầu lịch sử tiền thưởng LPGA. "
            "Trong khi đó trên thị trường bóng chày MLB, tay ném bóng từng hai lần đoạt giải thưởng Cy Young là Tarik Skubal vừa đạt thỏa thuận gia nhập câu lạc bộ New York Mets. "
            "Bản hợp đồng kéo dài chín năm có tổng giá trị lên tới 450 triệu USD của Skubal chính thức xô đổ mọi kỷ lục trước đó để trở thành giao kèo đắt giá nhất lịch sử dành cho một tay ném bóng tại MLB."
        ),
        "source": "LPGA / ESPN / Sky Sports / The Guardian",
        "news_source": "LPGA / ESPN / SKY SPORTS",
        "credit": "SKY SPORTS / THE GUARDIAN",
        "stat_badges": {
            "3": {"label": "JEENO THITIKUL", "value": "3 NĂM LIÊN TIẾP", "sub": "Thưởng 4 triệu USD • Vượt Sörenstam"},
            "5": {"label": "MLB CHẤN ĐỘNG", "value": "SKUBAL 450 TRIỆU USD", "sub": "Hợp đồng 9 năm đắt nhất lịch sử pitcher"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_LPGA_1)], "SKY SPORTS", "Jeeno Thitikul làm nên lịch sử với năm thứ ba liên tiếp thắng CME Group Tour Championship"),
            _slot("title", 0, [_url(GDN_MLB_1)], "THE GUARDIAN", "Pitcher xuất sắc Tarik Skubal nhận bản hợp đồng chín năm trị giá 450 triệu USD"),
            _slot("sentence", 1, [_url(SKY_LPGA_2)], "SKY SPORTS", "Hai môn thể thao đỉnh cao cùng chứng kiến những con số tiền thưởng choáng ngợp"),
            _slot("sentence", 2, [_url(SKY_LPGA_2)], "SKY SPORTS", "Vòng cuối 65 gậy không lỗi bogey giúp Thitikul bỏ xa các đối thủ bám đuổi"),
            _slot("sentence", 3, [_url(SKY_LPGA_1)], "SKY SPORTS", "Phần thưởng 4 triệu USD đưa golfer Thái Lan vượt qua kỷ lục của Annika Sörenstam"),
            _slot("sentence", 4, [_url(GDN_MLB_1)], "THE GUARDIAN", "New York Mets kích nổ bom tấn chiêu mộ ngôi sao ném bóng từng hai lần đoạt Cy Young"),
            _slot("sentence", 5, [_url(GDN_MLB_1)], "THE GUARDIAN", "Thỏa thuận 450 triệu USD thiết lập chuẩn mực tài chính mới cho bóng chày Mỹ"),
        ],
    },

    # 16 (Nữ — PAREDES NGẤT XỈU, NEYMAR POKER & GERWYN PRICE)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "ĐỜI SỐNG THỂ THAO",
        "title": "Nhà vô địch World Cup Paredes ngất xỉu khi phỏng vấn; Neymar thắng giải poker hơn 63000 USD; Price vô địch Darts",
        "summary": (
            "Người hâm mộ bóng đá Nam Mỹ được một phen thót tim sau trận chung kết Copa Sudamericana tại Colombia khi tiền vệ vô địch World Cup 2022 Leandro Paredes bất ngờ đổ gục ngay lúc đang trả lời phỏng vấn truyền hình. "
            "Trước đó, Paredes đeo băng đội trưởng cùng Boca Juniors thắng Atletico Mineiro 2-0 nhưng sớm có dấu hiệu kiệt sức từ phút 58 và phải rời sân nghỉ ngơi. "
            "Rất may sau vài giây ngất lịm trong đường hầm, ngôi sao 32 tuổi đã nhanh chóng tỉnh lại, được đưa tới cơ sở y tế kiểm tra rồi xuất viện trở về khách sạn cùng đồng đội trong tình trạng hoàn toàn ổn định. "
            "Ở một sân chơi khác tại quê nhà São Paulo, tiền đạo Neymar bất ngờ giành chức vô địch nội dung poker High Roller thuộc hệ thống giải BSOP Millions sau khi vượt qua 121 lượt đăng ký để nhận khoản thưởng hơn 63000 USD. "
            "Tại Anh tối ngày 22 tháng 11, cơ thủ phi tiêu Xứ Wales Gerwyn Price đánh bại Gian van Veen với tỷ số 16-11 để lần thứ tư đăng quang Grand Slam of Darts, chính thức chấm dứt bốn năm khát danh hiệu lớn."
        ),
        "source": "BBC Sport / The Guardian / Sky Sports / VnExpress / Dân Trí",
        "news_source": "BBC SPORT / VNEXPRESS / DÂN TRÍ",
        "credit": "VNEXPRESS / SKY SPORTS / GUARDIAN",
        "stat_badges": {
            "1": {"label": "SỰ CỐ ĐƯỜNG HẦM", "value": "PAREDES ĐỔ GỤC", "sub": "Ngất xỉu sau chức vô địch cùng Boca"},
            "4": {"label": "BSOP MILLIONS", "value": "NEYMAR 63000 USD", "sub": "Vô địch giải poker tại São Paulo"},
            "5": {"label": "GRAND SLAM OF DARTS", "value": "PRICE 16-11", "sub": "Chức vô địch thứ 4 sau 4 năm chờ đợi"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_PAR_1)], "VNEXPRESS", "Khoảnh khắc Leandro Paredes bất ngờ đổ gục trước ống kính truyền hình ở Colombia"),
            _slot("title", 0, [_url(VNE_NEY_1)], "VNEXPRESS", "Tiền đạo Neymar rạng rỡ bên chiếc cúp vô địch giải poker BSOP Millions"),
            _slot("title", 0, [_url(SKY_DART_1)], "SKY SPORTS", "Gerwyn Price ăn mừng chiến thắng 16-11 tại chung kết Grand Slam of Darts"),
            _slot("sentence", 1, [_url(VNE_PAR_1)], "VNEXPRESS", "Paredes ngã quỵ giữa lúc chia sẻ niềm vui vô địch khiến phóng viên và nhân viên y tế hốt hoảng"),
            _slot("sentence", 2, [_url(VNE_PAR_2)], "VNEXPRESS", "Trước đó, cựu tiền vệ tuyển Argentina vừa cùng Boca Juniors nâng cao cúp Nam Mỹ"),
            _slot("sentence", 3, [_url(DT_PAR_1)], "DÂN TRÍ", "Paredes nhanh chóng đăng ảnh từ phòng khám trấn an người hâm mộ rằng mình đã ổn"),
            _slot("sentence", 4, [_url(VNE_NEY_2)], "VNEXPRESS", "Neymar đánh bại người bạn thân Gilmar Araújo để nhận 380000 real tại São Paulo"),
            _slot("sentence", 5, [_url(SKY_DART_2)], "SKY SPORTS", "Gerwyn Price vượt qua Gian van Veen để hướng thẳng tới Giải vô địch thế giới"),
            _slot("sentence", 5, [_url(GDN_DART_1)], "THE GUARDIAN", "Chức vô địch giúp tay ném Xứ Wales lấy lại sự tự tin sau bốn năm chờ đợi danh hiệu"),
        ],
    },

    # 17 (100% Giọng Nữ — MỤC TIN VẮN CUỐI VIDEO: CÁC TIN THỂ THAO KHÁC)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "CÁC TIN THỂ THAO KHÁC",
        "title": "Điểm nhanh các tin thể thao đáng chú ý khác",
        "voice_preset": "secondary",
        "summary": (
            "Tại các giải bóng đá châu Âu đêm ngày 22 tháng 11, Werder Bremen vùi dập Hamburger SV với tỷ số 4-0 và Augsburg thắng Mainz 3-1 ở Bundesliga, trong khi tại Ligue 1, Paris FC đè bẹp Angers 4-0, Lorient hòa Rennes 1-1 còn Marseille bất ngờ gục ngã 2-3 trước Le Mans. "
            "Ở bóng đá nữ, đội nữ Tottenham giành chiến thắng ấn tượng trước Manchester City để làm nóng cuộc đua vô địch Super League Anh, còn câu lạc bộ nữ Celtic tạo tỷ số không tưởng 17-0 tại Cúp Quốc gia Scotland. "
            "Tại sân chơi pickleball MLP Asia 2026 ở Thành phố Hồ Chí Minh, tay vợt trẻ Sophia Huỳnh Trần gặp sự cố bị bóng đập cạnh vợt bay trúng mặt trong trận đôi nam nữ cùng Trương Vinh Hiển, rất may không bị chấn thương nghiêm trọng nhờ đeo kính bảo hộ. "
            "Trên đấu trường thể thao Mỹ, Atlanta Hawks đánh bại Detroit Pistons 107-97 tại NBA với màn trình diễn toàn diện của Dyson Daniels, tuần 11 giải bầu dục NFL chứng kiến DK Metcalf bị truất quyền thi đấu sau xô xát trong trận Steelers thua Eagles và làng truyền hình Mỹ thương tiếc bình luận viên kỳ cựu Tom Jackson qua đời ở tuổi 75. "
            "Khép lại bản tin hôm nay, cơ thủ snooker Trung Quốc Liu Wenwei vừa bị đình chỉ thi đấu để phục vụ điều tra nghi án bán độ, còn ở giải đấu PGA Tour RSM Classic, tay golf Rasmus Højgaard thực hiện cú gạt 25 feet giữ đỉnh bảng trước ngày đánh bù thứ Hai."
        ),
        "source": "BBC Sport / Sky Sports / ESPN / The Guardian / Tuổi Trẻ",
        "news_source": "ĐIỂM ĐỌC TỔNG HỢP",
        "credit": "SKY SPORTS / TUỔI TRẺ / GUARDIAN",
        "stat_badges": {
            "1": {"label": "BUNDESLIGA & LIGUE 1", "value": "BREMEN 4-0 HSV", "sub": "Paris FC thắng 4-0 • Marseille thua 2-3"},
            "3": {"label": "MLP ASIA TP.HCM", "value": "SOPHIA HUỲNH AN TOÀN", "sub": "Kính bảo hộ cứu khỏi chấn thương nặng"},
            "4": {"label": "NBA & NFL MỸ", "value": "HAWKS 107-97 PISTONS", "sub": "Tiếc thương BLV ESPN Tom Jackson"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_SOPHIA_1)], "TUỔI TRẺ", "Khoảnh khắc Sophia Huỳnh gặp sự cố bóng trúng mặt tại giải pickleball MLP Asia"),
            _slot("title", 0, [_url(SKY_NFL_MET)], "SKY SPORTS", "Ngôi sao NFL DK Metcalf bị truất quyền thi đấu sau tình huống va chạm căng thẳng"),
            _slot("title", 0, [_url(SKY_NFL_STL)], "SKY SPORTS", "Tuần 11 giải bóng bầu dục NFL diễn ra kịch tính trên nhiều sân đấu"),
            # Câu 1: Bundesliga & Ligue 1
            _slot("sentence", 1, [_ddgs("Werder Bremen Hamburger SV Bundesliga football")], "BBC SPORT", "Werder Bremen giành chiến thắng tưng bừng 4-0 trước đối thủ cùng vùng Hamburger SV"),
            _slot("sentence", 1, [_ddgs("Marseille Ligue 1 football match stadium")], "THE GUARDIAN", "Marseille bất ngờ nhận thất bại 2-3 ngay tại Ligue 1 trước Le Mans"),
            # Câu 2: WSL & Women Scottish Cup
            _slot("sentence", 2, [_ddgs("Tottenham Women football Manchester City WSL 2026")], "BBC SPORT", "Đội nữ Tottenham giành ba điểm quan trọng trước Manchester City tại giải vô địch Anh"),
            # Câu 3: Sophia Huỳnh
            _slot("sentence", 3, [_url(TT_SOPHIA_1)], "TUỔI TRẺ", "Cặp Trương Vinh Hiển và Sophia Huỳnh khiến khán giả lo lắng vì pha bóng dội vợt bất ngờ"),
            # Câu 4: NBA & NFL
            _slot("sentence", 4, [_ddgs("Atlanta Hawks Detroit Pistons NBA basketball 2026")], "ESPN", "Atlanta Hawks giành thắng lợi 107-97 trước Detroit Pistons trên sân nhà"),
            _slot("sentence", 4, [_url(SKY_NFL_MET)], "SKY SPORTS", "Cầu thủ DK Metcalf bị trọng tài đuổi khỏi sân vì va chạm với Cooper DeJean của Eagles"),
            # Câu 5: Snooker & PGA Tour
            _slot("sentence", 5, [_ddgs("snooker player table cue ball tournament")], "BBC SPORT", "Làng snooker chấn động với án đình chỉ phục vụ điều tra dành cho Liu Wenwei"),
            _slot("sentence", 5, [_url("https://e0.365dm.com/26/11/1920x1080/skysports-rasmus-hojgaard-rsm-classic_7414044.jpg?20261122223339")], "SKY SPORTS", "Rasmus Højgaard chia sẻ ngôi đầu giải golf RSM Classic trước loạt đánh quyết định"),
        ],
    },
]
