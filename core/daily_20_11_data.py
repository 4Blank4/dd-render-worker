# -*- coding: utf-8 -*-
"""
daily_20_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 20.11.2026
(Tổng hợp tin tức từ 12:00 ngày 19.11 đến 08:10 ngày 20.11.2026 — 21 bản tin chọn lọc).
Phân bổ giọng đọc luân phiên Nam (primary) / Nữ (secondary), biến thiên 1–5 ảnh/câu
để kích hoạt toàn bộ 9 layout, 4 chuyển cảnh và Broadcast Stat Callout HUD.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent
DAILY_19 = ROOT / "outputs" / "19.11.2026" / "images"
DAILY_18 = ROOT / "outputs" / "18.11.2026" / "images"


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


# ── URL ảnh sạch (không logo/watermark) từ báo chí chính thống 19–20.11.2026 ──
# 01. CAHN 1-3 Johor Darul Ta'zim
TN_CAHN_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/cahn-johor-1-1795094725584675989777.jpg"
TN_CAHN_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/cahn-johor-2-17950947255921683599195.jpg"
TN_CAHN_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/cahn-johor-3-1795094725635231006110.jpg"
VNE_CAHN_HAU = "https://i1-thethao.vnecdn.net/2026/11/19/1795097284270fda820654f8a0a02a-9772-8474-1795098265.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=HZw6W8c6t-EYux7Dq7QH4Q"
VNE_CAHN_DO = "https://i1-thethao.vnecdn.net/2026/11/19/1795093683530bdfe1569f71f63a5c-6287-4030-1795101321.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=HmwEJNI_ss0fio9Ljn7cqg"
TT_CAHN_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/cahn-17951025229902103785406.jpg"
TT_CAHN_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/cahn-1-1795102713102579834629.jpg"
TT_JDT_CELEB = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/17950962299158973244394868833818g14038781258001894147554d63f02376164b7add9442d5f4f02-1795096280303828654953.jpg"

# 02. Shopee Cup: Svay Rieng 4-1 Port FC, Chủ tịch Buriram xin lỗi
TT_SVAY_RIENG = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/edit-svay-rieng-2-17950996053341914616349.jpeg"
TT_NEWIN = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/buriram-nevin-1795086353845780011058.jpg"
TT_BUR_QC = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/18/quoc-cuong-catphcm-tran-gap-buriram-edit-17950119853231116409463.jpg"

# 03. Quốc Cường & phát hiện mới ĐTQG
TN_QC_SEA = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-qc-1795066901105264611587.jpg"
TN_QC_MID = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-qc2-1795066900954730182578.jpg"
TN_OLAHA = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/olaha2minhtutn18-11-26-17950017957131525714357.png"
TN_QC_VN = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/quoccuong2minhtutn18-11-26-17950019047361587638251.png"
TN_HONGPHUC = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/hongphuc2minhtutn18-11-26-17950019445501214669375.png"
DT_KIMSANGSIK = "https://cdnphoto.dantri.com.vn/xP-J1K0YpOFCBizcfRiDttUTsxQ=/thumb_w/1020/2026/11/19/bao-han-quoc-len-tieng-khi-tuyen-viet-nam-tang-hang-manh-nhat-the-gioi-1775467296162-1795091631924.jpg"

# 04. Vòng 8 V-League
TN_MINHTAM = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/3-1795097435951960179542.jpg"
TN_HAGL_HN = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/89029473016768148341092243281447452698522160n-1795070393330372464546.jpeg"
TN_CP_DN = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/1795058398987497733602546900204049773360254690020407964a152a7ec90a6d3463234a3d2e864-17950652589151900721978.jpg"

# 05 & 06. U17 Việt Nam vs U17 Bỉ & Nuno Gomes
TN_NUNO_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/u17-vn-vffm-1-2-3-1795103134145984520686.jpg"
TN_NUNO_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/u17-vn-vffm-86-1-scaled-1795103134241542852582.jpg"
TN_NUNO_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/u17-vn-vffm-3-2-1-1795103134031397215281.jpg"
TN_ROLAND_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/img8739-17951026007751300458469.jpeg"
TN_ROLAND_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/vffm-1-20-1795101374317-17951013749651847747286.jpg"
TN_ROLAND_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/vffm-39-scaled-1795101376590-1795101376939384297929.jpg"
TN_ROLAND_4 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/vffm-3-2-1-1795101384353-1795101384621125634089.jpg"
TN_ROLAND_5 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/vffm-129-scaled-1795101382776-1795101383155816428334.jpg"
TN_NGUYENLUC = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/1-1795094551110918544661.jpg"
DT_U17_LAST = "https://cdnphoto.dantri.com.vn/vBhu-_tto5OO5znmx-9Nxi9uTec=/thumb_w/1020/2026/11/20/vffm-27-1-2048x1417-1795107703698.jpg"
DT_U17_ROL = "https://cdnphoto.dantri.com.vn/4Cuf32eXO9QCnN8ZFcmVpXY3izo=/thumb_w/1020/2026/11/20/img20241025220807-1795107878353.jpg"
DT_U17_SCOUT = "https://cdnphoto.dantri.com.vn/B3pduJZNNxfOxT5KGKQc_RkS9so=/thumb_w/980/2026/11/20/doha-qatar-owen-mukisa-of-uganda-is-challenged-by-hawon-jung-of-korea-republic-during-the-1795112477891.jpg"
DT_U17_VFF = "https://cdnphoto.dantri.com.vn/Oum3Lgmt-P4UKWWYD3zvSSnR9so=/thumb_w/980/2026/11/20/z54392701694802ca3e7dd63390c1828a9d353e4ae2016-1795112590055.jpg"
DT_U17_HEIGHT1 = "https://cdnphoto.dantri.com.vn/qHc6LuDOTULZJAwUC81hmQmJXug=/thumb_w/1020/2026/11/19/u17vn1vff19-11-26-1795069701309.jpg"
DT_U17_HEIGHT2 = "https://cdnphoto.dantri.com.vn/YmfGqg657MzkOOVXOKttvkWh27Q=/thumb_w/1020/2026/11/19/u17vn2vff19-11-26-1795069797974.jpg"
DT_BI_SEKE = "https://cdnphoto.dantri.com.vn/2x2TX791Ir_2L055d9wh1wqeAMw=/thumb_w/1020/2026/11/19/u17-viet-nam-bat-ngo-nhan-loi-the-truoc-tran-ra-quan-gap-u17-bi-o-world-cup-edited-1795072199242.jpg"
DT_BI_TEAM = "https://cdnphoto.dantri.com.vn/Ok4Vh9vI6k-YADGTUfOMVWwXFsQ=/thumb_w/1020/2026/11/19/belgiums-players-celebrate-after-winning-a-soccer-game-between-belgium-u21-and-belarus-u21-1795072247748.jpg"
DT_BI_DIERCKX = "https://cdnphoto.dantri.com.vn/Jglonvih_vphmzZNih8iPZIU0hY=/thumb_w/1020/2026/11/19/output1-1623-1536x864-1795063696247.jpg"
DT_BI_FILIPPO = "https://cdnphoto.dantri.com.vn/bqgRyi_Pv_p7Z22vXcNarKqTgsc=/thumb_w/1020/2026/11/19/164766021-2-1795063807886.jpg"
TN_BI_VERMANT = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/edit-insaverto913268110180396488668507721059847477148705963n-17950644324571801528267.jpeg"
TN_BI_BLONDEEL = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/f03a91d3-205c-40b1-bd49-1979c55ccaadpng-17950790013161543824130.jpg"

# 07. Kết quả ngày 1 U17 World Cup (Úc 2-0 Argentina)
TN_AUS_AKON = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/7b7536b7-fbd6-4f2f-99cb-df9c8090728dpng-1795111029662742365449.jpg"
TT_AUS_CELEB = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/capture-17951299757911249629849.jpg"
TN_KOR_U17 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/6dfc9d22-e9f3-4992-b31d-ebcbd1a28f94png-1795109883976879351530.jpg"
TN_URU_U17 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/b3264f7c-59cb-4ec4-a550-fa7fdbe7e9a9png-1795109933142519247268.jpg"

# 08. Flycam Man Utd & Mbeumo GTA VI
VNE_FLY_1 = "https://i1-thethao.vnecdn.net/2026/11/20/Screenshot-2026-11-20-073126-1-8252-6079-1795134884.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=zZLkyD1zmRxleHiSWZI-4A"
VNE_FLY_2 = "https://i1-thethao.vnecdn.net/2026/11/20/Screenshot-2026-11-20-063359-1-8847-6259-1795134884.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=qQQ_xA3YAj6vBDNinPUi-A"
VNE_FLY_3 = "https://i1-thethao.vnecdn.net/2026/11/20/Screenshot-2026-11-20-073231-1-3303-1351-1795134885.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=ils6y8RPNXoYlSsV2E89GA"
VNE_MBEUMO_GTA = "https://i1-thethao.vnecdn.net/2026/11/19/mbeumo-1795097391-1917-1795097451.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=A4rCaULWswbSCnAXnbJQyg"
VNE_GTA_LONDON = "https://i1-thethao.vnecdn.net/2026/11/19/A-nh-ma-n-hi-nh-2026-11-19-lu-5471-1687-1795097451.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=GzmRqeTEImzUvF3LVJbIBQ"

# 09. Bảng lương MLS & Mẹ Messi - Nico Paz
VNE_MESSI_MLS = "https://i1-thethao.vnecdn.net/2026/11/20/2026t230428z-mt1usatoday303037-1178-1620-1795130419.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=D8Q-ojV7iqNiKOZfEisw3Q"
VNE_GRIEZ_LEW = "https://i1-thethao.vnecdn.net/2026/11/20/2026t212951z-mt1sipa000m1jzi2-3774-8130-1795130419.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=x8jm7D9uRI53ONa_FMgjUw"
VNE_NICO_CELIA = "https://i1-thethao.vnecdn.net/2026/11/19/Nico-Mess-Celia-1795104201-6114-1795104580.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=ZawtHM-bPqw3Jw1gvwAwew"
VNE_NICO_PAZ = "https://i1-thethao.vnecdn.net/2026/11/19/Nico-Paz-1354-1795104580.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=U7TK8nQRsN_Gpm39cIzvLA"

# 11. Nhà Esposito (Italy)
VNE_ESP_1 = "https://i1-thethao.vnecdn.net/2026/11/19/AP26316783590611-4006-1795101423.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=kguNLUPjN3xTE1XKXVGeRg"
VNE_ESP_2 = "https://i1-thethao.vnecdn.net/2026/11/19/esposito-intervista-rai-179510-6049-8171-1795101424.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=PSV9D78BiQy0IzwQX-ei3A"
VNE_ESP_3 = "https://i1-thethao.vnecdn.net/2026/11/19/Epositos-1795099123-6018-1795101424.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=rlrTP6Mv-JatcBrPXU0Vjw"
VNE_ESP_4 = "https://i1-thethao.vnecdn.net/2026/11/19/espo-1795100724-5737-1795101424.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=j9_pd0LIyvlCzfFumD9W1w"

# 12. Cassano - Ronaldinho & Pique - Tenerife
VNE_RONALDINHO = "https://i1-thethao.vnecdn.net/2026/11/19/A-nh-ma-n-hi-nh-2026-11-19-lu-4669-7078-1795100067.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=E1MNMMCL1LAIPAzx13uyMA"
VNE_CASSANO = "https://i1-thethao.vnecdn.net/2026/11/19/cassano-8861-1795100068.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=jM5SKz9etW3cgVO7MfW9zA"
TT_PIQUE = "https://cdn2.tuoitre.vn/thumb_w/730/2018/gerard-pique-1517316439-1517325123714.jpg"
TT_OWONO = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/14/jesus-owono-edit-1794616209230403082991.png"

# 13. Mudryk & Ecuador
TT_MUDRYK = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/6ezmzredqrji5pbztmlj32h3oy11zon-17950659731711260831579.jpg"
VNE_ECU_1 = "https://iv1.vnecdn.net/thethao/images/web/2026/11/19/cau-thu-bi-cam-8-nam-vi-nem-da-vao-trong-tai-1795073357.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=58unS_bwq2GSWW6oxTkN9A"
VNE_ECU_2 = "https://i1-thethao.vnecdn.net/2026/11/19/medium-1795073144-6727-1795073480.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=-RfjV1FZSujhtcQkvzEgeg"

# 14. Beiranvand AFC
TT_BEIRANVAND = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/29186-17951303518391819267245.png"

# 15. Sân Thống Nhất, Khai mạc & Cải tổ Đại hội 2030
TN_TN_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/17950555970431890119276910686313g7581630409918926693a677f9d6fa3f4e1bc97c7eae98079183-1795093245510769126428.jpg"
TN_TN_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/17950555972861890119276910686313g75816304099189266932cf50c8dfab3fdceb47c8ff85b0ebab8-17950932454631128690889.jpg"
TN_TN_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/17950555970261890119276910686313g7581630409918926693559752e8ec61b213380a61b0a3373bbd-17950932455391349009016.jpg"
TN_CAITO = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/2-1795094551146390519081.jpg"
TT_KM_PARA = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/19/base64-179510010841093817055.jpeg"
TT_KM_JET = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/19/base64-17951001084401412124587.jpeg"
TT_KM_TORCH = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/19/base64-17951001088071219712659.jpeg"
TT_KM_ALL = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/19/base64-1795100108837555068170.jpeg"
TT_KM_FIRE = "https://cdn2.tuoitre.vn/thumb_w/1460/471584752817336320/2026/11/19/base64-1795100108861579122920.jpeg"
DT_HOINGHI = "https://cdnphoto.dantri.com.vn/ltTeIVz337HkkiiaLRzKyFaywQs=/thumb_w/1020/2026/11/19/hoinghi3th19-11-26-1795090049453.jpeg"

# 16. Cầu lông, Vovinam, Bóng đá nữ Đại hội 2026
TN_VTT = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/9058666271220960882555556613026627171989164676n-17950638582231234085236.jpg"
TN_NHD = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/9134088891220981999435556611109428412066778809n-17950638583551166773850.jpg"
TT_CAULONG_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/vu-thi-trang-vu-thi-anh-thu-cau-long-dai-hoi-the-thao-toan-quoc-1-1795077690734390169153.jpeg"
TT_CAULONG_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/cau-long-tphcm-dai-hoi-the-thao-toan-quoc-2-17950737596971379321684.jpeg"
TT_CAULONG_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/cau-long-tphcm-dai-hoi-the-thao-toan-quoc-4-17950737597071430668598.jpeg"
TT_VOVINAM_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/tphcm-1795088418379457648447.jpg"
TT_VOVINAM_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/rin01441-17950887664871521456941.jpg"
TT_NU_HN = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/hai-yen-ts-media-1795112141675578253544.jpg"
TT_NU_TTRANG = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/91240602518507940592767315252255310141999874n-1795112210072256569316.jpeg"

# 17. ĐH Bách khoa TP.HCM hat-trick vô địch THACO Cup
TN_BK_CUP = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-nt06859-1795099756965985071312.jpg"
TN_BK_ACT = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-nt06050-2-1795099752510873117374.jpg"
TN_BK_CROWD = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-nt05588-179509973505810709340.jpg"
TN_BK_GOAL = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-nt05917-1795099749837853019265.jpg"
TN_BK_CELEB = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-nt06006-1795099753022351189639.jpg"
TN_BK_WIN = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-nt05949-1795099747208681075624-1795100780899881920108.jpg"
TN_BK_MVP = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-nt06594-17950997551771026038661.jpg"
TN_BK_RMIT = "https://images2.thanhnien.vn/528068263637045248/2026/11/19/tnw-nt06036-17950997523312139789651.jpg"

# 18. Làng cờ: Lại Lý Huynh, Lang Kỳ Kỳ, Carlsen - Bibisara, Levy Rozman
TT_LLH_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/8/24/edit-lai-ly-huynh-ngu-duong-boi-2-17721431157281893394332-17875369479221148082080.jpg"
TT_LLH_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/15/lai-ly-huynh-phung-gia-tuan-1-1794749571886898575794.jpg"
TT_LKK_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/base64-17950915407651791274602.jpeg"
TT_LKK_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/lang-ky-ky-1795085979638382456238.jpg"
TT_DANGPHI = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/lieu-dai-hoa-dang-phi-1795086096242997478307.jpg"
TT_CARLSEN_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/bibisara-carlsen-1795064105507872256657.jpg"
TT_CARLSEN_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/19/bibisara-carlsen-2-17950647253351979664454.jpg"
VNE_ROZMAN_KANE = "https://i1-thethao.vnecdn.net/2026/11/19/HVwSt3TW8AAIic3-1795080064-1641-1795080132.webp?w=1020&h=0&q=100&dpr=1&fit=crop&s=MDQa2UzqPwc6c7E6Vx_Uqw"

# 19. Peres Jepchirchir doping
VNE_JEP_1 = "https://i1-thethao.vnecdn.net/2026/11/19/Jepchirchir-1795100447-6480-1795101067.webp?w=1020&h=0&q=100&dpr=1&fit=crop&s=oHFDir1pGkMzZebv6NqwgA"
VNE_LOLEO = "https://i1-thethao.vnecdn.net/2026/11/19/A-nh-ma-n-hi-nh-2026-11-19-lu-1710-2789-1795101067.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=uqSQD7wKS_9a-eXml-27qQ"

# 20. Đô cử Malaysia Hafizuddin
VNE_MALAY_1 = "https://i1-thethao.vnecdn.net/2026/11/19/A-nh-ma-n-hi-nh-2026-11-19-lu-3297-2059-1795102773.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=_agpOg_0f0T8nuxhKnm4EA"
VNE_MALAY_2 = "https://i1-thethao.vnecdn.net/2026/11/19/A-nh-ma-n-hi-nh-2026-11-19-lu-1578-1433-1795102773.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=ALP9q8D93XsCA_C36TtIDQ"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 20.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 20 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất trên sân cỏ trong nước và đấu trường quốc tế. "
        "Ở tâm điểm khu vực, câu lạc bộ Công an Hà Nội ba lần dứt điểm trúng cột dọc và thua ngược Johor Darul Ta'zim 1-3 trên sân Hàng Đẫy, trong khi bóng đá Thái Lan đồng loạt sẩy chân tại Shopee Cup; còn U17 Việt Nam đã hoàn tất buổi tập cuối cùng cùng sự tiếp lửa từ danh thủ Nuno Gomes trước trận ra quân gặp U17 Bỉ lúc 20 giờ tối nay. "
        "Trên bình diện quốc tế, U17 Australia gây địa chấn đánh bại U17 Argentina 2-0 với hai cầu thủ gốc Việt trong đội hình xuất phát; buổi tập đầu tiên của tân HLV Mauricio Pochettino tại Manchester United bị máy bay không người lái ghi hình làm lộ sơ đồ 3-2-5, còn Lionel Messi tiếp tục dẫn đầu bảng lương MLS với 28,33 triệu USD. "
        "Cùng bản gia hạn hợp đồng lớn của Real Madrid với Tchouameni và Courtois, những tấm huy chương vàng kịch tính tại Đại hội Thể thao toàn quốc 2026 và diễn biến mới nhất tại ATP Finals, hãy cùng điểm lại 21 tin tức nổi bật ngay sau đây."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí",
    "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
    "credit": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 20 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất trên sân cỏ trong nước và đấu trường quốc tế.",
        },
        {
            "voice_preset": "primary",
            "text": "Ở tâm điểm khu vực, câu lạc bộ Công an Hà Nội ba lần dứt điểm trúng cột dọc và thua ngược Johor Darul Ta'zim 1-3 trên sân Hàng Đẫy, trong khi bóng đá Thái Lan đồng loạt sẩy chân tại Shopee Cup; còn U17 Việt Nam đã hoàn tất buổi tập cuối cùng cùng sự tiếp lửa từ danh thủ Nuno Gomes trước trận ra quân gặp U17 Bỉ lúc 20 giờ tối nay.",
        },
        {
            "voice_preset": "secondary",
            "text": "Trên bình diện quốc tế, U17 Australia gây địa chấn đánh bại U17 Argentina 2-0 với hai cầu thủ gốc Việt trong đội hình xuất phát; buổi tập đầu tiên của tân HLV Mauricio Pochettino tại Manchester United bị máy bay không người lái ghi hình làm lộ sơ đồ 3-2-5, còn Lionel Messi tiếp tục dẫn đầu bảng lương MLS với 28,33 triệu USD.",
        },
        {
            "voice_preset": "primary",
            "text": "Cùng bản gia hạn hợp đồng lớn của Real Madrid với Tchouameni và Courtois, những tấm huy chương vàng kịch tính tại Đại hội Thể thao toàn quốc 2026 và diễn biến mới nhất tại ATP Finals, hãy cùng điểm lại 21 tin tức nổi bật ngay sau đây.",
        },
    ],
    "stat_badges": {
        "1": {"label": "BẢN TIN NGÀY", "value": "20.11.2026", "sub": "21 tin nóng chọn lọc"},
        "2": {"label": "SHOPEE CUP", "value": "CAHN 1-3 JDT", "sub": "Dội cột dọc 3 lần"},
        "3": {"label": "LƯƠNG CAO NHẤT MLS", "value": "28,33 TRIỆU USD", "sub": "Lionel Messi dẫn đầu"},
    },
    "slots": [
        # Câu 1 (4 ảnh -> bento_grid / hero_mosaic)
        _slot("sentence", 1, [_url(TT_CAHN_1)], "TUỔI TRẺ", "Công an Hà Nội tiếp đón Johor Darul Ta'zim trên sân Hàng Đẫy"),
        _slot("sentence", 1, [_url(TN_NUNO_1)], "THANH NIÊN / VFF", "Danh thủ Nuno Gomes bất ngờ thăm đội tuyển U17 Việt Nam tại Qatar"),
        _slot("sentence", 1, [_url(VNE_MESSI_MLS)], "VNEXPRESS / REUTERS", "Lionel Messi tiếp tục dẫn đầu danh sách cầu thủ hưởng lương cao nhất MLS"),
        _slot("sentence", 1, [_url(VNE_FLY_3)], "VNEXPRESS", "HLV Mauricio Pochettino trực tiếp chỉ đạo buổi tập đầu tiên tại Carrington"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(TN_CAHN_1)], "THANH NIÊN", "Công an Hà Nội nhập cuộc áp đảo trước đại diện Malaysia"),
        _slot("sentence", 2, [_url(TT_SVAY_RIENG)], "TUỔI TRẺ / SVAY RIENG FC", "Svay Rieng ăn mừng chiến thắng đậm 4-1 trước Port FC của Thái Lan"),
        _slot("sentence", 2, [_url(DT_U17_LAST)], "DÂN TRÍ / VFF", "Đội tuyển U17 Việt Nam hoàn tất buổi tập cuối trước trận gặp Bỉ"),
        _slot("sentence", 2, [_url(DT_BI_DIERCKX)], "DÂN TRÍ / GETTY", "Tiền vệ Xander Dierckx là ngôi sao đắt giá nhất của U17 Bỉ"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url(TT_AUS_CELEB)], "TUỔI TRẺ / AUSTRALIA FOOTBALL", "U17 Australia tạo cú sốc đánh bại U17 Argentina 2-0 ngày khai mạc"),
        _slot("sentence", 3, [_url(VNE_FLY_2)], "VNEXPRESS", "Máy bay không người lái ghi lại sơ đồ 3-2-5 của HLV Mauricio Pochettino"),
        _slot("sentence", 3, [_url(VNE_GRIEZ_LEW)], "VNEXPRESS / REUTERS", "Antoine Griezmann và Robert Lewandowski bám sát Messi trên bảng lương MLS"),
        _slot("sentence", 3, [_url(VNE_MBEUMO_GTA)], "VNEXPRESS / REUTERS", "Bryan Mbeumo gây tranh cãi khi đăng ảnh chơi GTA VI lúc nửa đêm"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_ddgs("Aurelien Tchouameni Real Madrid action")], "REUTERS", "Real Madrid gia hạn hợp đồng sáu mùa giải với tiền vệ Aurelien Tchouameni"),
        _slot("sentence", 4, [_url(TT_KM_ALL)], "TUỔI TRẺ", "Tổng duyệt lễ khai mạc rực rỡ của Đại hội Thể thao toàn quốc 2026"),
        _slot("sentence", 4, [_url(TN_VTT)], "THANH NIÊN", "Tay vợt Vũ Thị Trang giúp cầu lông nữ TP.HCM đoạt huy chương vàng"),
        _slot("sentence", 4, [_ddgs("Alexander Zverev tennis ATP Finals Turin")], "ATP TOUR", "Alexander Zverev toàn thắng vòng bảng tại ATP Finals 2026 ở Turin"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — BÓNG ĐÁ VIỆT NAM)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "BÓNG ĐÁ VIỆT NAM",
        "title": "Công an Hà Nội dội cột dọc ba lần, thua ngược Johor Darul Ta'zim 1-3 tại Hàng Đẫy",
        "summary": (
            "Tối ngày 19 tháng 11 trên sân Hàng Đẫy ở lượt hai bảng B Shopee Cup, câu lạc bộ Công an Hà Nội nhập cuộc bùng nổ khi mở tỷ số ngay phút thứ tư nhờ pha phản lưới của hậu vệ Nene sau đường chọc khe giữa Alan và Bryan Perea. "
            "Suốt hiệp một dù vắng Nguyễn Đình Bắc và cất Quang Hải dự bị, đội chủ nhà vẫn áp đảo hoàn toàn thế trận nhưng hai cú dứt điểm uy lực của Alan và Perea lần lượt tìm đúng cột dọc. "
            "Bước sang hiệp hai khi đối thủ tung Oscar Arribas vào sân, đẳng cấp dàn ngoại binh giúp nhà vô địch Malaysia lội ngược dòng thắng 3-1 với cú đúp của Arribas ở phút 50 và 86 cùng bàn thắng của Marcos Guilherme, xen giữa là thêm một lần Alan sút dội cột dọc và pha lập công phút 90 của Quang Hải bị VAR từ chối vì lỗi việt vị. "
            "Phát biểu sau trận đấu, HLV Mano Polking khẳng định các học trò không hề hụt hơi thể lực mà chỉ thiếu sắc bén hơn ở khâu dứt điểm trước khi bước vào chuỗi 10 trận trong 40 ngày tới."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "credit": "THANH NIÊN / VNEXPRESS",
        "stat_badges": {
            "1": {"label": "MỞ TỶ SỐ SỚM", "value": "PHÚT 04", "sub": "Nene phản lưới tại Hàng Đẫy"},
            "3": {"label": "TỶ SỐ CHUNG CUỘC", "value": "CAHN 1-3 JDT", "sub": "3 lần dội cột dọc + VAR từ chối"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_CAHN_1)], "TUỔI TRẺ", "Công an Hà Nội tiếp đón Johor Darul Ta'zim tại Hàng Đẫy"),
            _slot("title", 0, [_url(TN_CAHN_1)], "THANH NIÊN", "Đội chủ nhà chơi sòng phẳng với nhà vô địch Malaysia"),
            _slot("title", 0, [_url(VNE_CAHN_HAU)], "VNEXPRESS", "Đoàn Văn Hậu tranh chấp quyết liệt trong trận thua 1-3"),
            # Câu 1 (3 ảnh -> hero_mosaic / filmstrip / triptych)
            _slot("sentence", 1, [_url(TN_CAHN_2)], "THANH NIÊN", "Pha áp sát ngay phút thứ 4 khiến hậu vệ Johor đá phản lưới nhà"),
            _slot("sentence", 1, [_url(VNE_CAHN_HAU)], "VNEXPRESS", "Hàng thủ Công an Hà Nội giữ cự ly chắc chắn đầu trận"),
            _slot("sentence", 1, [_url(TT_CAHN_1)], "TUỔI TRẺ", "Cầu thủ hai đội tranh chấp quyết liệt trên sân Hàng Đẫy"),
            # Câu 2 (4 ảnh -> bento_grid / filmstrip)
            _slot("sentence", 2, [_url(TN_CAHN_1)], "THANH NIÊN", "Alan và Perea tạo nhiều sóng gió trước khung thành đối phương"),
            _slot("sentence", 2, [_local(DAILY_19 / "Tin_04_1.jpg")], "DÂN TRÍ", "HLV Mano Polking tiếc nuối khi đội nhà bỏ lỡ cơ hội nhân đôi cách biệt"),
            _slot("sentence", 2, [_url(VNE_CAHN_DO)], "VNEXPRESS", "Lê Văn Đô cơ động bên hành lang cánh của Công an Hà Nội"),
            _slot("sentence", 2, [_local(DAILY_19 / "Tin_04_3.jpg")], "THANH NIÊN", "Cao Pendant Quang Vinh và các đồng đội chơi áp đảo trong hiệp một"),
            # Câu 3 (5 ảnh -> filmstrip_carousel / bento_grid / spotlight)
            _slot("sentence", 3, [_url(TN_CAHN_3)], "THANH NIÊN", "Johor Darul Ta'zim vùng lên mạnh mẽ ở hiệp đấu thứ hai"),
            _slot("sentence", 3, [_url(TT_JDT_CELEB)], "TUỔI TRẺ", "Đội khách ăn mừng hai pha lập công của Oscar Arribas"),
            _slot("sentence", 3, [_url(TT_CAHN_2)], "TUỔI TRẺ", "Quang Hải dứt điểm tung lưới phút 90 nhưng không được VAR công nhận"),
            _slot("sentence", 3, [_ddgs("Johor Darul Tazim AFC Champions League celebration")], "REUTERS", "Nhà vô địch Malaysia thể hiện bản lĩnh với dàn ngoại binh chất lượng"),
            _slot("sentence", 3, [_ddgs("Hang Day stadium Hanoi football night")], "VPF", "Công an Hà Nội tạm xếp thứ ba bảng B với 3 điểm sau hai lượt"),
            # Câu 4 (2 ảnh -> split / cinema / spotlight)
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_04_2.jpg")], "VNEXPRESS", "HLV Mano Polking chia sẻ trong phòng họp báo sau trận"),
            _slot("sentence", 4, [_ddgs("Mano Polking Cong An Ha Noi coach")], "BÓNG ĐÁ PLUS", "Đội bóng ngành công an hướng tới hành trình 10 trận trong 40 ngày"),
        ],
    },

    # 02 (Nữ — SHOPEE CUP 2026)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "SHOPEE CUP 2026",
        "title": "Bóng đá Việt Nam vượt Thái Lan tại Shopee Cup; Port FC thảm bại 1-4 và Chủ tịch Buriram xin lỗi",
        "summary": (
            "Cùng khung giờ tối ngày 19 tháng 11 ở bảng B Shopee Cup, đại gia Thái Lan là câu lạc bộ Port FC gây sốc khi thua thảm 1-4 trên sân của nhà vô địch Campuchia Svay Rieng. "
            "Đội chủ nhà liên tiếp xé lưới đại diện Thai League nhờ công của Min Ratanak, Martins Junior, Tiago Alves và Kwame Peprah, đẩy Port FC chìm sâu ở vị trí áp chót với không điểm sau hai trận toàn thua và bảy bàn lọt lưới. "
            "Trước đó, việc đương kim vô địch Buriram United thất thủ 0-1 trước Công an TP.HCM đã khiến Chủ tịch Newin Chidchob phải đăng tâm thư công khai xin lỗi người hâm mộ Thái Lan vì khởi đầu đáng thất vọng. "
            "Sau hai lượt trận vòng bảng, bóng đá Việt Nam đứng trên hoàn toàn khi Công an TP.HCM giữ nhì bảng A với 4 điểm còn Công an Hà Nội có 3 điểm, trong lúc cả ba câu lạc bộ Thái Lan gồm Buriram, Ratchaburi và Port FC đều chưa biết mùi chiến thắng."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "CÚ SỐC ĐÔNG NAM Á", "value": "PORT FC 1-4", "sub": "Thua đậm Svay Rieng trên sân khách"},
            "4": {"label": "THÁI LAN TẠI SHOPEE CUP", "value": "0 CHIẾN THẮNG", "sub": "Cả 3 đại diện Thai League chưa thắng"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_SVAY_RIENG)], "TUỔI TRẺ / SVAY RIENG FC", "Các cầu thủ Svay Rieng ăn mừng chiến thắng 4-1 trước Port FC"),
            _slot("title", 0, [_url(TT_NEWIN)], "TUỔI TRẺ / THAIRATH", "Chủ tịch Buriram United Newin Chidchob công khai xin lỗi người hâm mộ"),
            _slot("title", 0, [_url(TT_BUR_QC)], "TUỔI TRẺ", "Công an TP.HCM tạo tiếng vang khi đánh bại Buriram United 1-0"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TT_SVAY_RIENG)], "TUỔI TRẺ / SVAY RIENG FC", "Svay Rieng thi đấu thăng hoa trên sân Morodok Techo"),
            _slot("sentence", 1, [_ddgs("Morodok Techo National Stadium Cambodia")], "AFC", "Chảo lửa Morodok Techo chứng kiến cú sốc lớn trước đại diện Thai League"),
            _slot("sentence", 1, [_ddgs("Port FC Thai League 1 football match")], "THAI LEAGUE", "Port FC sở hữu dàn tuyển thủ Thái Lan nhưng gục ngã hoàn toàn"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_ddgs("Preah Khan Reach Svay Rieng football team")], "SVAY RIENG FC", "Nhà vô địch Campuchia ba mùa liên tiếp khẳng định sức mạnh ở sân chơi khu vực"),
            _slot("sentence", 2, [_ddgs("Madam Pang Nualphan Lamsam Thailand football")], "THAIRATH", "Trận thua đậm của Port FC giáng đòn mạnh vào niềm tự hào bóng đá Thái Lan"),
            # Câu 3 (4 ảnh)
            _slot("sentence", 3, [_url(TT_NEWIN)], "TUỔI TRẺ / THAIRATH", "Ông Newin Chidchob thừa nhận Buriram còn nhiều vấn đề phải khắc phục"),
            _slot("sentence", 3, [_url(TT_BUR_QC)], "TUỔI TRẺ", "Thất bại 0-1 tại Bình Dương khiến báo chí Thái Lan sững sờ"),
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_03_2.jpg")], "THANH NIÊN", "Nguyễn Thái Quốc Cường ghi bàn thắng quý như vàng phút 88"),
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_03_4.jpg")], "THANH NIÊN", "Thủ môn Lê Giang Patrik hóa giải toàn bộ pha dứt điểm của Buriram"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_03_1.jpg")], "VNEXPRESS", "Công an TP.HCM vươn lên nhì bảng A với 4 điểm"),
            _slot("sentence", 4, [_ddgs("Tampines Rovers Singapore football club")], "AFC", "Tampines Rovers cũng vừa đánh bại Ratchaburi 3-2 ở lượt trận này"),
            _slot("sentence", 4, [_ddgs("Buriram United Chang Arena stadium")], "THAI LEAGUE", "Cả ba CLB Thái Lan đều rơi xuống nửa dưới bảng xếp hạng sau 2 lượt"),
        ],
    },

    # 03 (Nam — BÓNG ĐÁ VIỆT NAM)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "BÓNG ĐÁ VIỆT NAM",
        "title": "Quốc Cường trưởng thành vượt bậc sau cú vấp SEA Games; lộ diện nhân tố mới tuyển Việt Nam",
        "summary": (
            "Gần một năm sau khoảnh khắc bị rút ra sớm ở phút 38 trận chung kết bóng đá nam SEA Games 33 trước Thái Lan, tiền vệ 22 tuổi Nguyễn Thái Quốc Cường đã lột xác mạnh mẽ để trở thành trụ cột tuyến giữa. "
            "Từ tấm huy chương đồng U23 châu Á 2026 tới màn ra mắt đội tuyển quốc gia và pha lập công phút 88 hạ gục Buriram United, cầu thủ quê Nghệ An đang nhận được sự tin tưởng lớn của ban huấn luyện. "
            "Cùng với Quốc Cường, loạt trận giao hữu vừa qua tại Thiên Trường còn giúp tuyển Việt Nam phát hiện thêm tiền đạo nhập tịch cao 1 mét 86 là Olaha Mạnh Đức cùng hậu vệ cánh phải Nguyễn Hồng Phúc sở hữu thể hình 1 mét 78. "
            "Khép lại năm 2026 ở vị trí hạng 99 FIFA, đội tuyển Việt Nam chắc chắn nằm ở nhóm hạt giống số 2 tại lễ bốc thăm vòng loại thứ hai World Cup 2030 ngày 15 tháng 12 tới để tránh Thái Lan và Trung Quốc, trong khi hợp đồng của HLV Kim Sang-sik sẽ được VFF xem xét gia hạn sau Đại hội khóa 10 đầu năm 2027."
        ),
        "source": "Thanh Niên / Dân Trí",
        "news_source": "THANH NIÊN / DÂN TRÍ",
        "credit": "THANH NIÊN / DÂN TRÍ",
        "stat_badges": {
            "2": {"label": "CỘT MỐC ẤN TƯỢNG", "value": "PHÚT 88", "sub": "Quốc Cường ghi bàn hạ Buriram"},
            "4": {"label": "XẾP HẠNG CUỐI NĂM", "value": "HẠNG 99 FIFA", "sub": "Hạt giống số 2 World Cup 2030"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_QC_MID)], "THANH NIÊN", "Nguyễn Thái Quốc Cường trưởng thành vượt bậc ở tuyến giữa"),
            _slot("title", 0, [_url(TN_OLAHA)], "THANH NIÊN", "Tiền đạo nhập tịch Olaha Mạnh Đức là phát hiện mới trên hàng công"),
            _slot("title", 0, [_url(DT_KIMSANGSIK)], "DÂN TRÍ", "HLV Kim Sang-sik có thêm nhiều lựa chọn chất lượng cho vòng loại World Cup"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TN_QC_SEA)], "THANH NIÊN", "Quốc Cường từng trải qua thử thách tâm lý ở chung kết SEA Games 33"),
            _slot("sentence", 1, [_url(TN_QC_MID)], "THANH NIÊN", "Tiền vệ sinh năm 2004 đứng dậy mạnh mẽ sau bài học đắt giá"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(TN_QC_VN)], "THANH NIÊN", "Quốc Cường giữ nhịp tốt khi khoác áo đội tuyển Việt Nam"),
            _slot("sentence", 2, [_local(DAILY_19 / "Tin_03_3.jpg")], "THANH NIÊN", "Cú cứa lòng mẫu mực giúp Công an TP.HCM đánh bại Buriram"),
            _slot("sentence", 2, [_ddgs("Vietnam U23 football team celebration 2026")], "VFF", "Anh cũng là nhân tố quan trọng giành HCĐ U23 châu Á 2026"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(TN_OLAHA)], "THANH NIÊN", "Olaha Mạnh Đức cao 1m86 mang lại sức mạnh tranh chấp bóng bổng"),
            _slot("sentence", 3, [_url(TN_HONGPHUC)], "THANH NIÊN", "Hậu vệ phải Nguyễn Hồng Phúc lên công về thủ ấn tượng"),
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_02_1.jpg")], "TUỔI TRẺ", "Đội tuyển Việt Nam tích cực thử nghiệm nhân sự ở sân Thiên Trường"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_url(DT_KIMSANGSIK)], "DÂN TRÍ", "Tương lai HLV Kim Sang-sik sẽ được VFF bàn thảo sau tháng 1/2027"),
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_02_2.jpg")], "THANH NIÊN", "Vị trí hạng 99 thế giới giúp tuyển Việt Nam giữ nhóm hạt giống số 2"),
            _slot("sentence", 4, [_ddgs("AFC headquarters Kuala Lumpur Malaysia")], "AFC", "Lễ bốc thăm vòng loại thứ hai World Cup 2030 diễn ra vào ngày 15/12"),
        ],
    },

    # 04 (Nữ — V-LEAGUE 2026-2027)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "V-LEAGUE 2026-2027",
        "title": "Vòng 8 V-League khởi tranh hôm nay: Chờ màn ra mắt hai HLV ngoại và bài toán HAGL của Thanh Hóa",
        "summary": (
            "Chiều tối nay ngày 20 tháng 11, vòng 8 V-League 2026-2027 mở màn bằng hai cặp đấu đáng chú ý giữa Thanh Hóa gặp Hoàng Anh Gia Lai lúc 17 giờ và Thể Công Viettel tiếp Sông Lam Nghệ An lúc 19 giờ 15. "
            "Dù đang đứng trên đối thủ ở bảng xếp hạng, đội bóng xứ Thanh đối diện rào cản tâm lý cực lớn khi chưa từng thắng phố núi suốt 14 lần chạm trán liên tiếp từ tháng 9 năm 2018 với 8 trận hòa và 6 thất bại. "
            "Tâm điểm của vòng đấu cuối tuần còn hướng về băng ghế chỉ đạo với màn ra mắt của hai tân HLV ngoại là ông Dylan Kerr dẫn dắt Hải Phòng làm khách trước đội đầu bảng Nam Định và chiến lược gia Lee Young-jin cầm quân Đà Nẵng tiếp đón Ninh Bình. "
            "Bên cạnh đó, tân binh TP.Đồng Nai của Nguyễn Công Phượng sau chiến thắng đầu tay ở vòng 7 đang đặt mục tiêu tạo thêm bất ngờ trước CLB Hà Nội của HLV Harry Kewell vào tối mai."
        ),
        "source": "Thanh Niên / Bongdaplus",
        "news_source": "THANH NIÊN / BÓNG ĐÁ PLUS",
        "credit": "THANH NIÊN / VPF",
        "stat_badges": {
            "2": {"label": "KỴ RƠ LỊCH SỬ", "value": "14 TRẬN BẤT BẠI", "sub": "HAGL trước Thanh Hóa từ 2018"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_MINHTAM)], "THANH NIÊN", "Nguyễn Minh Tâm mang phong độ cao từ U23 trở lại HAGL"),
            _slot("title", 0, [_local(DAILY_19 / "Tin_18_2.jpg")], "TUỔI TRẺ", "HLV Dylan Kerr trở lại dẫn dắt Hải Phòng sau hơn một thập kỷ"),
            _slot("title", 0, [_url(TN_CP_DN)], "THANH NIÊN / FPT PLAY", "Công Phượng sẵn sàng cùng TP.Đồng Nai tiếp đón CLB Hà Nội"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TN_MINHTAM)], "THANH NIÊN", "HAGL hành quân tới sân Thanh Hóa lúc 17h00 chiều nay"),
            _slot("sentence", 1, [_ddgs("Thanh Hoa FC V-League stadium match")], "VPF", "Tân HLV Kim Young-chul tìm kiếm chiến thắng sân nhà cùng Thanh Hóa"),
            _slot("sentence", 1, [_ddgs("The Cong Viettel SLNA V-League football")], "VPF", "Thể Công Viettel đối đầu SLNA đang bất bại 7 trận mùa này"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(TN_HAGL_HN)], "THANH NIÊN / CLB HAGL", "HAGL vừa thắng Hà Nội 2-1 đầy tự tin ở vòng đấu trước"),
            _slot("sentence", 2, [_ddgs("Hoang Anh Gia Lai Pleiku football match")], "VPF", "Đội bóng phố núi giữ mạch 14 trận liền không thua Thanh Hóa"),
            # Câu 3 (4 ảnh)
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_18_2.jpg")], "TUỔI TRẺ", "Ông Dylan Kerr đối mặt thử thách lớn ngay trận gặp Nam Định"),
            _slot("sentence", 3, [_ddgs("Lee Young Jin football coach Vietnam")], "VFF", "Cựu trợ lý tuyển Việt Nam Lee Young-jin chính thức nắm quyền tại Đà Nẵng"),
            _slot("sentence", 3, [_ddgs("Nam Dinh FC Thien Truong stadium V-League")], "VPF", "Thép Xanh Nam Định bảo vệ ngôi đầu bảng trên sân Thiên Trường"),
            _slot("sentence", 3, [_ddgs("Chi Lang stadium Da Nang football")], "VPF", "CLB Đà Nẵng tiếp Ninh Bình trên sân nhà ở vòng 8"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(TN_CP_DN)], "THANH NIÊN / FPT PLAY", "Công Phượng vừa mang về quả phạt đền giúp TP.Đồng Nai thắng trận đầu"),
            _slot("sentence", 4, [_ddgs("Harry Kewell Hanoi FC coach V-League")], "VPF", "HLV Harry Kewell tìm lời giải cho hàng công của CLB Hà Nội"),
        ],
    },

    # 05 (Nam — U17 WORLD CUP 2026)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "U17 WORLD CUP 2026",
        "title": "Trước giờ G gặp U17 Bỉ: Danh thủ Nuno Gomes thăm U17 Việt Nam, HLV Roland truyền lửa tự tin",
        "summary": (
            "Vào lúc 20 giờ tối nay ngày 20 tháng 11 trên sân số 9 khu phức hợp Aspire Zone tại Qatar, đội tuyển U17 Việt Nam sẽ bước vào trận mở màn lịch sử tại bảng G FIFA U17 World Cup 2026 gặp U17 Bỉ. "
            "Ở buổi tập cuối cùng chiều qua, thầy trò HLV Cristiano Roland bất ngờ đón huyền thoại bóng đá Bồ Đào Nha Nuno Gomes tới giao lưu và chụp ảnh động viên với tư cách đại sứ FIFA, tạo nên bầu không khí vô cùng hứng khởi. "
            "Chia sẻ trước giờ bóng lăn, HLV Cristiano Roland nhắn nhủ các học trò hãy gạt bỏ áp lực thành tích, tận hưởng niềm vui chơi bóng và chiến đấu hết mình để tự hào khi rời sân. "
            "Theo truyền thông quốc tế, giải đấu năm nay thu hút hơn 130 tuyển trạch viên từ các câu lạc bộ lớn như Barcelona, Real Madrid hay Manchester United tới Qatar săn tìm tài năng trẻ, mở ra cơ hội bằng vàng cho các cầu thủ Việt Nam khẳng định tên tuổi."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / TUỔI TRẺ / DÂN TRÍ",
        "credit": "THANH NIÊN / VFF",
        "stat_badges": {
            "1": {"label": "TRẬN MỞ MÀN LỊCH SỬ", "value": "20H00 TỐI NAY", "sub": "U17 Việt Nam vs U17 Bỉ"},
            "4": {"label": "CƠ HỘI BẰNG VÀNG", "value": "130+ SCOUTS", "sub": "Tuyển trạch viên Barca, Real, MU"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_NUNO_1)], "THANH NIÊN / VFF", "Danh thủ Nuno Gomes bất ngờ thăm đội tuyển U17 Việt Nam"),
            _slot("title", 0, [_url(DT_U17_LAST)], "DÂN TRÍ / VFF", "U17 Việt Nam hoàn tất buổi tập cuối tại Doha"),
            _slot("title", 0, [_url(DT_U17_ROL)], "DÂN TRÍ / VFF", "HLV Cristiano Roland truyền sự tự tin cho các cầu thủ trẻ"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TN_NUNO_3)], "THANH NIÊN / VFF", "Các cầu thủ U17 Việt Nam tràn đầy quyết tâm trước ngày ra quân"),
            _slot("sentence", 1, [_local(DAILY_19 / "Tin_05_4.jpg")], "THANH NIÊN / FIFA", "Khu phức hợp Aspire Zone tại Doha sẵn sàng cho loạt trận bảng G"),
            _slot("sentence", 1, [_url(DT_U17_VFF)], "DÂN TRÍ / VFF", "Đây là lần đầu tiên bóng đá U17 Việt Nam góp mặt ở sân chơi World Cup"),
            # Câu 2 (4 ảnh)
            _slot("sentence", 2, [_url(TN_NUNO_1)], "THANH NIÊN / VFF", "Nuno Gomes từng là đồng đội cũ của HLV Roland tại Benfica"),
            _slot("sentence", 2, [_url(TN_NUNO_2)], "THANH NIÊN / VFF", "Tinh thần các tuyển thủ trẻ Việt Nam vô cùng thoải mái và gắn kết"),
            _slot("sentence", 2, [_url(TN_ROLAND_4)], "THANH NIÊN / VFF", "Ban huấn luyện tổ chức các bài tập vận động giải tỏa tâm lý"),
            _slot("sentence", 2, [_url(TN_ROLAND_5)], "THANH NIÊN / VFF", "Toàn đội chụp ảnh lưu niệm khép lại hai tháng chuẩn bị"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(TN_ROLAND_1)], "THANH NIÊN / FPT PLAY", "HLV Cristiano Roland trả lời báo chí trước trận gặp U17 Bỉ"),
            _slot("sentence", 3, [_url(TN_ROLAND_2)], "THANH NIÊN / FPT PLAY", "Nhà cầm quân người Brazil yêu cầu học trò tuân thủ chặt đấu pháp"),
            _slot("sentence", 3, [_url(TN_ROLAND_3)], "THANH NIÊN / FPT PLAY", "Ông Roland quan sát từng bước chạy của học trò trên sân tập Qatar"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_url(DT_U17_SCOUT)], "DÂN TRÍ / GETTY", "Các trận đấu tại U17 World Cup luôn thu hút đông đảo tuyển trạch viên châu Âu"),
            _slot("sentence", 4, [_url(DT_U17_LAST)], "DÂN TRÍ / VFF", "Đây là sân khấu lớn nhất để lứa cầu thủ trẻ Việt Nam vươn tầm"),
            _slot("sentence", 4, [_url(TN_NGUYENLUC)], "THANH NIÊN / VFF", "Tiền vệ Chu Ngọc Nguyễn Lực là một trong những niềm hy vọng lớn"),
        ],
    },

    # 06 (Nữ — U17 WORLD CUP 2026)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Việt Nam thấp thứ tư giải đấu đối đầu U17 Bỉ 12,5 triệu euro nhưng đối thủ vắng 4 trụ cột",
        "summary": (
            "Theo thống kê từ FIFA, U17 Việt Nam sở hữu chiều cao trung bình 1,7505 mét, xếp thứ 45 trên 48 đội tuyển và thấp nhất tại bảng G trước ba đối thủ gồm Bỉ, New Zealand và Mali. "
            "Trong khi cầu thủ cao nhất của chúng ta là thủ môn Nguyễn Thái Sơn đạt 1 mét 87 còn tiền đạo Lê Sỹ Bách cao 1 mét 66, đối thủ tối nay U17 Bỉ có chiều cao trung bình tới 1,8386 mét cùng tổng giá trị đội hình 12,5 triệu euro đứng thứ ba toàn giải. "
            "Tuy vậy, đội đương kim á quân châu Âu lại chịu tổn thất nặng nề khi câu lạc bộ Anderlecht từ chối nhả bốn trụ cột gồm ngôi sao trị giá 2,5 triệu euro Jayden Onia Seke cùng Joshua Kana, Noa Ojea và Noah Kalonji. "
            "Chính sự sứt mẻ nhân sự này khiến HLV trưởng Sven Vermant cùng báo chí Bỉ đồng loạt cảnh báo các cầu thủ không được phép chủ quan trước lối chơi kỷ luật của tân binh Đông Nam Á duy nhất tại giải."
        ),
        "source": "VnExpress / Dân Trí / Thanh Niên",
        "news_source": "VNEXPRESS / DÂN TRÍ / THANH NIÊN",
        "credit": "DÂN TRÍ / THANH NIÊN",
        "stat_badges": {
            "1": {"label": "SO SÁNH THỂ HÌNH", "value": "1,75M vs 1,84M", "sub": "U17 Việt Nam xếp 45/48 đội"},
            "3": {"label": "LỢI THẾ BẤT NGỜ", "value": "MẤT 4 TRỤ CỘT", "sub": "Anderlecht giữ quân U17 Bỉ"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_U17_HEIGHT1)], "DÂN TRÍ / VFF", "U17 Việt Nam đối mặt thử thách thể hình tại sân chơi thế giới"),
            _slot("title", 0, [_url(DT_BI_SEKE)], "DÂN TRÍ / GETTY", "Tài năng 2,5 triệu euro Jayden Onia Seke vắng mặt ở tuyển U17 Bỉ"),
            _slot("title", 0, [_url(DT_BI_DIERCKX)], "DÂN TRÍ / GETTY", "Tiền vệ Xander Dierckx cao 1m86 được định giá 5 triệu euro"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(DT_U17_HEIGHT1)], "DÂN TRÍ / VFF", "Các cầu thủ U17 Việt Nam bù đắp bất lợi chiều cao bằng tốc độ và kỹ thuật"),
            _slot("sentence", 1, [_url(DT_U17_HEIGHT2)], "DÂN TRÍ / VFF", "Nhóm thủ môn U17 Việt Nam đạt chiều cao trung bình 1m8133"),
            # Câu 2 (4 ảnh)
            _slot("sentence", 2, [_url(DT_BI_DIERCKX)], "DÂN TRÍ / GETTY", "Xander Dierckx đã có kinh nghiệm thi đấu tại giải VĐQG Bỉ"),
            _slot("sentence", 2, [_url(DT_BI_FILIPPO)], "DÂN TRÍ / HBVL", "Tiền đạo Niels Filippo nằm trong dàn mũi nhọn nguy hiểm của U17 Bỉ"),
            _slot("sentence", 2, [_url(DT_BI_TEAM)], "DÂN TRÍ / GETTY", "Đội hình U17 Bỉ đạt giá trị 12,5 triệu euro chỉ sau Tây Ban Nha và Italy"),
            _slot("sentence", 2, [_url(TN_BI_BLONDEEL)], "THANH NIÊN / VFF", "Preben Blondeel cũng là gương mặt được FIFA đặc biệt chú ý"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(DT_BI_SEKE)], "DÂN TRÍ / GETTY", "Anderlecht giữ chân Jayden Onia Seke vì giải U17 không thuộc FIFA Days"),
            _slot("sentence", 3, [_ddgs("RSC Anderlecht academy youth football Belgium")], "REUTERS", "Sự vắng mặt của nhóm cầu thủ Anderlecht làm giảm đáng kể hỏa lực U17 Bỉ"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_url(TN_BI_VERMANT)], "THANH NIÊN / RBFA", "HLV Sven Vermant yêu cầu học trò tôn trọng tối đa U17 Việt Nam"),
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_06_4.jpg")], "DÂN TRÍ / VFF", "Truyền thông Bỉ đánh giá cao tinh thần kỷ luật của đại diện Đông Nam Á"),
            _slot("sentence", 4, [_url(TN_NGUYENLUC)], "THANH NIÊN / VFF", "U17 Việt Nam đặt mục tiêu tạo địa chấn ngay lượt mở màn bảng G"),
        ],
    },

    # 07 (Nam — U17 WORLD CUP 2026)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "U17 WORLD CUP 2026",
        "title": "Địa chấn ngày khai mạc U17 World Cup: U17 Australia có 2 cầu thủ gốc Việt đánh bại Argentina 2-0",
        "summary": (
            "Đêm ngày 19 tháng 11 ở lượt trận mở màn bảng C giải U17 World Cup 2026, U17 Australia gây bất ngờ lớn khi đánh bại đương kim á quân Nam Mỹ là U17 Argentina với tỷ số 2-0. "
            "Đáng chú ý, đội hình xuất phát của đội bóng châu Á góp mặt tới hai tài năng trẻ gốc Việt là Jariyah Shah thuộc lò Manchester United và Max Court của Brisbane Roar. "
            "Sau hiệp một giằng co, phút 60 cầu thủ chạy cánh Akol Akon tạt bóng khiến Guich đá phản lưới nhà trước khi tự mình ấn định thắng lợi ở phút 71 nhờ công nghệ khiếu nại video FVS, còn Argentina khép lại trận thua bằng tấm thẻ đỏ ở phút bù giờ. "
            "Cũng trong ngày thi đấu đầu tiên, U17 Mozambique đè bẹp Đan Mạch 4-0, U17 Hàn Quốc thắng Uganda 3-0, U17 Pháp vượt qua Haiti 3-1 còn chủ nhà Qatar hạ Panama 2-0 vào phút bù giờ."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Bongdaplus",
        "news_source": "THANH NIÊN / TUỔI TRẺ / BÓNG ĐÁ PLUS",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "ĐỊA CHẤN BẢNG C", "value": "ÚC 2-0 ARGENTINA", "sub": "Hạ gục á quân Nam Mỹ"},
            "4": {"label": "BẤT NGỜ KHÁC", "value": "MOZAMBIQUE 4-0", "sub": "Hàn Quốc 3-0 | Pháp 3-1"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_AUS_CELEB)], "TUỔI TRẺ / AUSTRALIA FOOTBALL", "U17 Australia ăn mừng chiến thắng lịch sử trước Argentina"),
            _slot("title", 0, [_url(TN_AUS_AKON)], "THANH NIÊN / FIFA", "Akol Akon tỏa sáng rực rỡ giúp U17 Australia tạo địa chấn"),
            _slot("title", 0, [_url(TN_KOR_U17)], "THANH NIÊN / FIFA", "Đại diện châu Á U17 Hàn Quốc thắng đậm 3-0 trong ngày ra quân"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TT_AUS_CELEB)], "TUỔI TRẺ / AUSTRALIA FOOTBALL", "U17 Australia trở lại World Cup đầy ngoạn mục sau bảy năm"),
            _slot("sentence", 1, [_ddgs("Argentina U17 national football team match")], "FIFA", "Á quân Nam Mỹ U17 Argentina bỏ lỡ nhiều cơ hội và trả giá đắt"),
            _slot("sentence", 1, [_ddgs("FIFA U17 World Cup Qatar 2026 stadium")], "FIFA", "Ngày khai mạc U17 World Cup 2026 chứng kiến nhiều tỷ số bất ngờ"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_ddgs("Jariyah Shah Manchester United youth")], "MAN UTD", "Tài năng gốc Việt Jariyah Shah đá chính ở tuyến giữa U17 Australia"),
            _slot("sentence", 2, [_ddgs("Australia Joeys U17 football team players")], "AUSTRALIA FOOTBALL", "HLV Carl Veart tin dùng hai cầu thủ gốc Việt trong đội hình chính"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(TN_AUS_AKON)], "THANH NIÊN / FIFA", "Akol Akon in dấu giày vào cả hai bàn thắng trong hiệp hai"),
            _slot("sentence", 3, [_ddgs("soccer referee VAR review monitor pitch")], "FIFA", "Bàn thắng thứ hai được công nhận sau quyền khiếu nại video FVS"),
            _slot("sentence", 3, [_ddgs("football referee red card match")], "REUTERS", "Argentina còn mất người vì tấm thẻ đỏ của Ulises Vallejo cuối trận"),
            # Câu 4 (4 ảnh)
            _slot("sentence", 4, [_url(TN_KOR_U17)], "THANH NIÊN / FIFA", "U17 Hàn Quốc dẫn đầu bảng B sau chiến thắng 3-0 trước Uganda"),
            _slot("sentence", 4, [_url(TN_URU_U17)], "THANH NIÊN / FIFA", "U17 Uruguay thắng ngược kịch tính Saudi Arabia với tỷ số 3-2"),
            _slot("sentence", 4, [_ddgs("France U17 national football team match")], "FFF", "U17 Pháp dễ dàng vượt qua Haiti 3-1 để dẫn đầu bảng D"),
            _slot("sentence", 4, [_ddgs("Qatar U17 national football team stadium")], "QFA", "Chủ nhà U17 Qatar thắng Panama 2-0 nhờ hai bàn phút bù giờ"),
        ],
    },

    # 08 (Nữ — BÓNG ĐÁ ANH)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "BÓNG ĐÁ ANH",
        "title": "Flycam lộ sơ đồ 3-2-5 của Pochettino tại Man Utd; tiền đạo Mbeumo bị chỉ trích chơi GTA VI nửa đêm",
        "summary": (
            "Buổi tập đầu tiên của tân HLV Mauricio Pochettino tại trung tâm Carrington ngày 19 tháng 11 vừa gặp sự cố an ninh khi một máy bay không người lái quay lén suốt 12 phút và đăng lên YouTube thu hút hơn 180000 lượt xem. "
            "Đoạn phim hé lộ chiến lược gia người Argentina chia đội hình làm ba nhóm, trực tiếp sắp xếp sơ đồ 3-2-5 và đón chào sự trở lại kịp lúc của Harry Maguire cùng Patrick Dorgu trước chuyến làm khách trước Liverpool vào ngày 22 tháng 11. "
            "Tuy nhiên, tinh thần chuẩn bị của Quỷ đỏ lập tức vấp phải làn sóng chỉ trích khi tiền đạo Bryan Mbeumo vô tư đăng ảnh khởi động trò chơi GTA VI vào lúc nửa đêm ngay trước buổi tập đầu cùng thầy mới. "
            "Trước sức ép giúp Manchester United thoát khỏi vị trí thứ 18 Ngoại hạng Anh, truyền thông Anh nhận định Pochettino nhiều khả năng sẽ gạch tên Diogo Dalot và Amad Diallo khỏi đội hình xuất phát tại Anfield."
        ),
        "source": "VnExpress / Bongdaplus",
        "news_source": "VNEXPRESS / BÓNG ĐÁ PLUS",
        "credit": "VNEXPRESS / REUTERS",
        "stat_badges": {
            "1": {"label": "SỰ CỐ CARRINGTON", "value": "180000+ VIEWS", "sub": "Video flycam quay lén 12 phút"},
            "2": {"label": "SƠ ĐỒ CHIẾN THUẬT", "value": "3-2-5", "sub": "Maguire và Dorgu trở lại tập luyện"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_FLY_3)], "VNEXPRESS", "HLV Mauricio Pochettino hội ý chiến thuật cùng các học trò"),
            _slot("title", 0, [_url(VNE_FLY_1)], "VNEXPRESS", "Toàn cảnh sân tập Carrington bị máy bay không người lái ghi hình"),
            _slot("title", 0, [_url(VNE_MBEUMO_GTA)], "VNEXPRESS / REUTERS", "Bryan Mbeumo đăng ảnh chơi game lúc nửa đêm gây tranh cãi"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(VNE_FLY_1)], "VNEXPRESS", "Đoạn phim flycam dài 12 phút thu hút hàng trăm nghìn lượt xem trên mạng"),
            _slot("sentence", 1, [_local(DAILY_19 / "Tin_09_1.jpg")], "VNEXPRESS / MAN UTD", "Mauricio Pochettino vừa hạ cánh xuống Manchester bằng chuyên cơ riêng"),
            _slot("sentence", 1, [_ddgs("Carrington Manchester United training ground aerial")], "REUTERS", "An ninh tại trung tâm huấn luyện Carrington đặt dấu hỏi lớn"),
            # Câu 2 (4 ảnh)
            _slot("sentence", 2, [_url(VNE_FLY_2)], "VNEXPRESS", "Sơ đồ chiến thuật 3-2-5 lộ rõ qua góc quay từ trên cao"),
            _slot("sentence", 2, [_url(VNE_FLY_3)], "VNEXPRESS", "Ông Pochettino trực tiếp hướng dẫn nhóm cầu thủ đá chính"),
            _slot("sentence", 2, [_ddgs("Harry Maguire Manchester United training 2026")], "GETTY", "Harry Maguire bình phục chấn thương lưng để kịp đối đầu Liverpool"),
            _slot("sentence", 2, [_ddgs("Patrick Dorgu Manchester United training")], "REUTERS", "Patrick Dorgu trở lại tập luyện sau màn tỏa sáng trước Aston Villa"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(VNE_MBEUMO_GTA)], "VNEXPRESS / REUTERS", "Bryan Mbeumo đăng ảnh khởi động GTA VI ngay lúc sang ngày 19/11"),
            _slot("sentence", 3, [_url(VNE_GTA_LONDON)], "VNEXPRESS / REUTERS", "Cơn sốt GTA VI khiến nhiều ngôi sao bóng đá mải chơi thâu đêm"),
            _slot("sentence", 3, [_ddgs("Bryan Mbeumo soccer player action")], "REUTERS", "Người hâm mộ Quỷ đỏ lo ngại tiền đạo người Cameroon thiếu tập trung"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_09_4.jpg")], "VNEXPRESS", "Diogo Dalot có nguy cơ mất vị trí sau sai lầm trận gặp Villa"),
            _slot("sentence", 4, [_ddgs("Amad Diallo Manchester United match")], "REUTERS", "Amad Diallo cũng đứng trước nguy cơ nhường chỗ cho Zirkzee"),
            _slot("sentence", 4, [_ddgs("Anfield stadium Liverpool pitch night")], "LIVERPOOL FC", "Manchester United hành quân đến chảo lửa Anfield ngày 22/11"),
        ],
    },

    # 09 (Nam — BÓNG ĐÁ QUỐC TẾ)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Bảng lương MLS: Messi dẫn đầu với 28,33 triệu USD, vượt Lewandowski và Griezmann; mẹ Messi động viên Nico Paz",
        "summary": (
            "Sáng ngày 20 tháng 11, Hiệp hội Cầu thủ MLS chính thức công bố bảng thu nhập đảm bảo của giải nhà nghề Mỹ với ngôi đầu tuyệt đối thuộc về siêu sao Lionel Messi ở mức 28,33 triệu USD mỗi năm. "
            "Xếp ngay phía sau trong nhóm cầu thủ hưởng lương trên 10 triệu USD là hai tân binh mùa hè gồm Robert Lewandowski của Chicago Fire với 19,51 triệu USD, Antoine Griezmann của Orlando City đạt 13,94 triệu USD, Son Heung-Min nhận 11,25 triệu USD và Breel Embolo với 10,81 triệu USD. "
            "Đáng chú ý, dù dẫn đầu về thu nhập tuyệt đối nhưng tỷ trọng quỹ lương của Messi tại Inter Miami ở mức 47,7 phần trăm đã bị Griezmann vượt qua khi ngôi sao người Pháp chiếm tới 49,5 phần trăm ngân sách của Orlando. "
            "Ở một câu chuyện xúc động bên lề, chú của tiền vệ trẻ Nico Paz vừa tiết lộ mẹ Messi là bà Celia Cuccittini từng nắm tay cầu thủ 22 tuổi đang khoác áo Como sau trận chia tay của El Pulga và nhắn nhủ anh chính là người kế nhiệm con trai bà."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / REUTERS",
        "stat_badges": {
            "1": {"label": "SỐ 1 MLS 2026", "value": "28,33 TRIỆU USD", "sub": "Thu nhập đảm bảo của Lionel Messi"},
            "2": {"label": "TOP LƯƠNG CAO MLS", "value": "5 SIÊU SAO >10M", "sub": "Lewandowski 19,51M • Griezmann 13,94M"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_MESSI_MLS)], "VNEXPRESS / REUTERS", "Lionel Messi dẫn đầu bảng lương MLS ở mức 28,33 triệu USD"),
            _slot("title", 0, [_url(VNE_GRIEZ_LEW)], "VNEXPRESS / REUTERS", "Antoine Griezmann và Robert Lewandowski lọt tốp 3 thu nhập tại Mỹ"),
            _slot("title", 0, [_url(VNE_NICO_CELIA)], "VNEXPRESS / BOLAVIP", "Mẹ Messi bà Celia Cuccittini động viên tiền vệ trẻ Nico Paz"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(VNE_MESSI_MLS)], "VNEXPRESS / REUTERS", "Thu nhập của Messi tại Inter Miami tăng mạnh so với mức 20,45 triệu USD năm ngoái"),
            _slot("sentence", 1, [_local(DAILY_19 / "Tin_07_1.jpg")], "DÂN TRÍ / REUTERS", "Siêu sao Argentina vẫn là biểu tượng số một của giải nhà nghề Mỹ"),
            # Câu 2 (4 ảnh)
            _slot("sentence", 2, [_url(VNE_GRIEZ_LEW)], "VNEXPRESS / REUTERS", "Robert Lewandowski và Antoine Griezmann là hai bom tấn mùa hè tại MLS"),
            _slot("sentence", 2, [_ddgs("Robert Lewandowski Chicago Fire MLS soccer")], "REUTERS", "Lewandowski hưởng mức lương đảm bảo 19,51 triệu USD tại Chicago Fire"),
            _slot("sentence", 2, [_ddgs("Son Heung-Min LAFC Los Angeles FC MLS")], "AP PHOTO", "Son Heung-Min đứng thứ tư bảng lương MLS với 11,25 triệu USD ở LAFC"),
            _slot("sentence", 2, [_ddgs("Breel Embolo Atlanta United MLS soccer")], "MLS", "Tiền đạo Breel Embolo khép lại tốp 5 cầu thủ nhận trên 10 triệu USD"),
            # Câu 3 (1 ảnh -> cinema / full / polaroid)
            _slot("sentence", 3, [_ddgs("Inter Miami Chase Stadium Lionel Messi match")], "REUTERS", "Toàn giải MLS hiện có 150 cầu thủ đạt thu nhập đảm bảo từ một triệu USD trở lên"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_url(VNE_NICO_CELIA)], "VNEXPRESS / BOLAVIP", "Bà Celia Cuccittini gọi Nico Paz là người kế nhiệm con trai sau trận gặp Benin"),
            _slot("sentence", 4, [_url(VNE_NICO_PAZ)], "VNEXPRESS / AP", "Nico Paz thi đấu bùng nổ với 5 bàn sau 4 trận gần nhất cho Argentina"),
            _slot("sentence", 4, [_ddgs("Nico Paz Como Serie A football")], "SERIE A", "Cầu thủ 22 tuổi trưởng thành từ Real Madrid đang là nhạc trưởng của Como"),
        ],
    },

    # 10 (Nữ — BÓNG ĐÁ QUỐC TẾ)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Real Madrid trói chân bộ khung tương lai: Gia hạn Tchouameni sáu mùa và giữ Courtois tới năm 2028",
        "summary": (
            "Ban lãnh đạo câu lạc bộ Real Madrid vừa công bố thông tin quan trọng nhằm bảo đảm bộ khung ổn định lâu dài tại sân Santiago Bernabeu. "
            "Theo thông báo chính thức, tiền vệ người Pháp Aurelien Tchouameni sẽ tiếp tục gắn bó với đội bóng Hoàng gia Tây Ban Nha thêm sáu mùa giải sau khi đã ra sân 205 trận và giành 8 danh hiệu lớn nhỏ từ năm 2022. "
            "Động thái này diễn ra chỉ 24 giờ sau khi Real Madrid ký hợp đồng mới tới năm 2032 với tài năng trẻ Arda Guler, kết hợp cùng giao kèo tới năm 2031 của Jude Bellingham tạo nên tuyến giữa giàu sức trẻ. "
            "Ở vị trí chốt chặn, nhà báo Fabrizio Romano cũng xác nhận thủ thành Thibaut Courtois đã hoàn tất việc ký gia hạn hợp đồng kéo dài tới năm 2028 và chỉ còn chờ ngày công bố chính thức."
        ),
        "source": "Bongdaplus",
        "news_source": "BÓNG ĐÁ PLUS",
        "credit": "REUTERS / AP",
        "stat_badges": {
            "2": {"label": "GIA HẠN DÀI HẠN", "value": "THÊM 6 MÙA", "sub": "Tchouameni: 205 trận • 8 cúp"},
            "4": {"label": "CHỐT CHẶN BỀN VỮNG", "value": "ĐẾN NĂM 2028", "sub": "Thủ môn Thibaut Courtois"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Aurelien Tchouameni Real Madrid celebration")], "REUTERS", "Real Madrid gia hạn hợp đồng thêm sáu mùa với Aurelien Tchouameni"),
            _slot("title", 0, [_ddgs("Thibaut Courtois Real Madrid goalkeeper match")], "AP PHOTO", "Thủ môn Thibaut Courtois đạt thỏa thuận gắn bó tới năm 2028"),
            _slot("title", 0, [_ddgs("Arda Guler Jude Bellingham Real Madrid")], "REUTERS", "Bộ khung trẻ của đội bóng Hoàng gia Tây Ban Nha được giữ chân dài hạn"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_ddgs("Santiago Bernabeu stadium Real Madrid pitch")], "REAL MADRID", "Real Madrid củng cố kế hoạch nhân sự dài hạn tại Santiago Bernabeu"),
            _slot("sentence", 1, [_ddgs("Real Madrid players huddle Champions League")], "UEFA", "Đội bóng Hoàng gia Tây Ban Nha duy trì tính kế thừa giữa các thế hệ"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_ddgs("Aurelien Tchouameni Real Madrid Champions League")], "REUTERS", "Ở tuổi 26, Tchouameni là mắt xích không thể thiếu ở tuyến giữa"),
            _slot("sentence", 2, [_ddgs("Aurelien Tchouameni France national team")], "AP PHOTO", "Anh cũng có 50 lần khoác áo đội tuyển Pháp và từng vô địch Nations League"),
            _slot("sentence", 2, [_ddgs("Real Madrid trophy celebration Champions League")], "REAL MADRID", "Tiền vệ người Pháp đã sưu tập 8 danh hiệu cùng Los Blancos"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Arda Guler Real Madrid match action")], "REUTERS", "Arda Guler vừa đặt bút ký hợp đồng mới có thời hạn tới năm 2032"),
            _slot("sentence", 3, [_ddgs("Jude Bellingham Real Madrid goal celebration")], "AP PHOTO", "Jude Bellingham giữ cam kết gắn bó tới năm 2031"),
            _slot("sentence", 3, [_ddgs("Real Madrid midfielders training Valdebebas")], "REAL MADRID", "Bộ ba Tchouameni, Bellingham và Guler định hình tương lai tuyến giữa"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_ddgs("Thibaut Courtois Real Madrid save Champions League")], "UEFA", "Thibaut Courtois tiếp tục là điểm tựa vững chắc trong khung gỗ"),
            _slot("sentence", 4, [_ddgs("Thibaut Courtois Real Madrid training")], "REUTERS", "Hợp đồng mới của thủ thành người Bỉ kéo dài tới mùa hè 2028"),
        ],
    },

    # 11 (Nam — BÓNG ĐÁ QUỐC TẾ)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Dấu ấn lịch sử ở tuyển Italy: Ba anh em ruột nhà Esposito cùng nhau khoác áo Azzurri",
        "summary": (
            "Bóng đá Italy vừa chứng kiến cột mốc chưa từng có trong lịch sử khi ba anh em ruột nhà Esposito gồm Salvatore, Sebastiano và Francesco Pio lần lượt được khoác áo đội tuyển quốc gia. "
            "Trong trận thắng Thổ Nhĩ Kỳ 4-1 ở Nations League vừa qua, Sebastiano lần đầu ra mắt và sát cánh đá chính trên hàng công cùng người em út Pio vốn lập công góp sức cho Azzurri, khiến anh cả Salvatore theo dõi qua màn hình ở quê nhà vô cùng xúc động. "
            "Trước gia đình Esposito, lần gần nhất hai anh em ruột cùng đá chính cho tuyển Italy đã diễn ra từ năm 1915, còn cặp anh em gần nhất cùng ra sân là Filippo và Simone Inzaghi cách đây đúng 26 năm. "
            "Đáng quý hơn, khi thành công ở Serie A, cả ba anh em còn chung tay xây tặng sân bóng cho khu phố tuổi thơ và mua lại câu lạc bộ Voluntas Brescia đang khó khăn để tri ân người thầy cũ quá cố."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / AP",
        "stat_badges": {
            "1": {"label": "CỘT MỐC LỊCH SỬ", "value": "3 ANH EM RUỘT", "sub": "Gia đình đầu tiên tại tuyển Italy"},
            "3": {"label": "KỶ LỤC TÁI LẬP", "value": "SAU 111 NĂM", "sub": "Hai anh em cùng đá chính từ 1915"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_ESP_1)], "VNEXPRESS / AP", "Pio Esposito ăn mừng cùng anh trai Sebastiano trong màu áo tuyển Italy"),
            _slot("title", 0, [_url(VNE_ESP_3)], "VNEXPRESS / GAZZETTA DELLO SPORT", "Ba anh em nhà Esposito từng trưởng thành cùng nhau tại Brescia"),
            _slot("title", 0, [_url(VNE_ESP_2)], "VNEXPRESS / AP", "Anh cả Salvatore Esposito ra mắt đội tuyển Italy từ năm 2022"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(VNE_ESP_3)], "VNEXPRESS / GAZZETTA DELLO SPORT", "Từ trái qua: Salvatore, Pio và Sebastiano Esposito thời còn ở Brescia"),
            _slot("sentence", 1, [_url(VNE_ESP_4)], "VNEXPRESS / GAZZETTA DELLO SPORT", "Ba anh em nhà Esposito giữ mối gắn bó khăng khít cả trong và ngoài sân cỏ"),
            _slot("sentence", 1, [_ddgs("Italy national football team Azzurri players")], "FIGC", "Chưa từng có gia đình nào có ba anh em ruột đều chơi cho tuyển nam Italy"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(VNE_ESP_1)], "VNEXPRESS / AP", "Pio và Sebastiano đá chính cạnh nhau trên hàng công trước Thổ Nhĩ Kỳ"),
            _slot("sentence", 2, [_url(VNE_ESP_2)], "VNEXPRESS / AP", "Salvatore gọi điện chúc mừng hai em ngay sau chiến thắng 4-1"),
            _slot("sentence", 2, [_ddgs("Francesco Pio Esposito Inter Milan Italy")], "SERIE A", "Em út Francesco Pio đang thi đấu thăng hoa trong màu áo Inter và tuyển Italy"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_ddgs("Filippo Inzaghi Simone Inzaghi Italy national team")], "GETTY", "Anh em nhà Inzaghi là cặp anh em gần nhất cùng ra sân cho Italy năm 2000"),
            _slot("sentence", 3, [_ddgs("Franco Baresi Giuseppe Baresi Italy Milan")], "SERIE A", "Hai anh em nhà Baresi trước đây cũng là niềm tự hào của bóng đá Italy"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(VNE_ESP_4)], "VNEXPRESS / GAZZETTA DELLO SPORT", "Gia đình ông Agostino và bà Flavia luôn đồng hành sát cánh cùng ba con trai"),
            _slot("sentence", 4, [_ddgs("Brescia Italy youth football pitch")], "FIGC", "Ba anh em mua lại CLB Voluntas Brescia để đền ơn người thầy Clerici"),
        ],
    },

    # 12 (Nữ — BÓNG ĐÁ QUỐC TẾ)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Châu Âu dậy sóng tranh cãi: Cassano chê Ronaldinho là trò hề, Pique bị Chủ tịch Tenerife đáp trả",
        "summary": (
            "Làng bóng đá châu Âu những ngày qua chứng kiến hai màn khẩu chiến nảy lửa xuất phát từ phát ngôn của các cựu danh thủ. "
            "Tại Italy, cựu tiền đạo Antonio Cassano thẳng thừng chỉ trích màn tái xuất chuyên nghiệp ở tuổi 46 của Ronaldinho trong màu áo đội hạng ba Ravenna sau 11 năm giải nghệ là một trò hề lố bịch vì động cơ thương mại, dù Phó chủ tịch Serie C Gianfranco Zola lại khen ngợi sức hút từ huyền thoại Brazil. "
            "Cùng lúc ở Tây Ban Nha, Chủ tịch CLB Tenerife là ông Felipe Minambres phải công khai nhắn nhủ Gerard Pique rằng đôi khi im lặng tốt hơn nhiều so với lên tiếng. "
            "Phản ứng gay gắt này nổ ra sau khi cựu trung vệ Barca vốn là cổ đông lớn của FC Andorra đăng video bênh vực thủ môn Jesus Owono trước án treo giò 12 trận liên quan tới cái chết thương tâm của tiền đạo Jesus de Miguel."
        ),
        "source": "VnExpress / Tuổi Trẻ",
        "news_source": "VNEXPRESS / TUỔI TRẺ",
        "credit": "VNEXPRESS / TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "TÁI XUẤT TUỔI 46", "value": "SAU 11 NĂM", "sub": "Ronaldinho đá 45 phút cho Ravenna"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_RONALDINHO)], "VNEXPRESS / AP", "Ronaldinho ra sân thi đấu cho CLB hạng ba Italy Ravenna ở tuổi 46"),
            _slot("title", 0, [_url(VNE_CASSANO)], "VNEXPRESS / AFP", "Antonio Cassano gọi màn trở lại của Ronaldinho là trò hề khó xem"),
            _slot("title", 0, [_url(TT_PIQUE)], "TUỔI TRẺ / REUTERS", "Gerard Pique vấp phải làn sóng phản đối từ phòng thay đồ Tenerife"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(VNE_CASSANO)], "VNEXPRESS / AFP", "Các phát ngôn thẳng thừng của Cassano thường gây tranh cãi lớn"),
            _slot("sentence", 1, [_url(TT_PIQUE)], "TUỔI TRẺ / REUTERS", "Phát biểu trên mạng xã hội của Gerard Pique châm ngòi bức xúc tại Tây Ban Nha"),
            # Câu 2 (4 ảnh)
            _slot("sentence", 2, [_url(VNE_RONALDINHO)], "VNEXPRESS / AP", "Ronaldinho đá trọn hiệp một trong trận Ravenna thắng Forli"),
            _slot("sentence", 2, [_ddgs("Ronaldinho Ravenna FC Serie C Italy")], "SERIE C", "Cựu danh thủ Brazil là cổ đông thiểu số của CLB Ravenna"),
            _slot("sentence", 2, [_ddgs("Gianfranco Zola Italy football Serie C")], "ANSA", "Phó chủ tịch Serie C Gianfranco Zola bảo vệ màn tái xuất truyền cảm hứng"),
            _slot("sentence", 2, [_url(VNE_CASSANO)], "VNEXPRESS / AFP", "Cassano vẫn xếp Ronaldinho trong tốp 5 cầu thủ hay nhất lịch sử"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_ddgs("CD Tenerife stadium Heliodoro Rodriguez Lopez")], "LA LIGA 2", "Chủ tịch Tenerife Felipe Minambres không hài lòng khi Pique khơi lại nỗi đau"),
            _slot("sentence", 3, [_ddgs("Alvaro Cervera Tenerife coach press conference")], "MARCA", "HLV Alvaro Cervera cho rằng pha va chạm hoàn toàn có thể tránh được"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(TT_OWONO)], "TUỔI TRẺ / LA NACION", "Thủ môn Jesus Owono nhận án treo giò kịch khung 12 trận"),
            _slot("sentence", 4, [_ddgs("FC Andorra football club stadium")], "RFEF", "Gerard Pique là cổ đông lớn nhất tiếp quản FC Andorra từ năm 2018"),
        ],
    },

    # 13 (Nam — BÓNG ĐÁ QUỐC TẾ)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Mudryk tố LĐBĐ Ukraine khiến mình dính doping; cầu thủ Ecuador bị cấm 8 năm vì ném đá trọng tài",
        "summary": (
            "Tiền vệ thuộc biên chế Chelsea đang khoác áo Tottenham theo dạng cho mượn là Mykhailo Mudryk vừa gây sốc khi công khai quy trách nhiệm cho Liên đoàn Bóng đá Ukraine về vụ anh dương tính với chất cấm meldonium. "
            "Ngôi sao 25 tuổi khẳng định dược phẩm này chỉ lưu hành ở Đông Âu, tố đội tuyển Ukraine phát thuốc thiếu kiểm soát trước trận đấu và còn cố tình rò rỉ thư từ riêng tư khiến anh phải tự chi hàng triệu bảng thuê luật sư kháng cáo giảm án. "
            "Ở một án phạt chấn động khác, Liên đoàn Bóng đá Ecuador vừa chính thức cấm cầu thủ John Michel Perlaza Salas hoạt động bóng đá suốt 8 năm tới ngày 19 tháng 10 năm 2034. "
            "Hành vi ném đá từ ghế dự bị trúng mặt trọng tài biên Lenin Ojeda Nunez khiến nạn nhân phải phẫu thuật khẩn cấp này còn đứng trước nguy cơ bị FIFA mở rộng lệnh cấm trên phạm vi toàn cầu."
        ),
        "source": "Tuổi Trẻ / VnExpress",
        "news_source": "TUỔI TRẺ / VNEXPRESS",
        "credit": "TUỔI TRẺ / VNEXPRESS",
        "stat_badges": {
            "2": {"label": "ÁN PHẠT DOPING", "value": "11/2024 - 7/2026", "sub": "Mudryk kháng cáo thành công lên CAS"},
            "3": {"label": "KỶ LUẬT THÉP", "value": "CẤM 8 NĂM", "sub": "Tới 19/10/2034 tại Ecuador"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_MUDRYK)], "TUỔI TRẺ / REUTERS", "Mykhailo Mudryk tố LĐBĐ Ukraine khiến anh vướng bê bối chất cấm"),
            _slot("title", 0, [_url(VNE_ECU_1)], "VNEXPRESS / HAVOLINE", "Cầu thủ giải hạng Ba Ecuador ném đá vào trọng tài biên"),
            _slot("title", 0, [_url(VNE_ECU_2)], "VNEXPRESS / HAVOLINE", "Trọng tài biên Ojeda phải ngồi xe lăn nhập viện phẫu thuật vùng mặt"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TT_MUDRYK)], "TUỔI TRẺ / REUTERS", "Mudryk chia sẻ thẳng thắn trong cuộc phỏng vấn phát sáng 19/11"),
            _slot("sentence", 1, [_ddgs("Mykhailo Mudryk Ukraine national football team")], "UAF", "Cầu thủ sinh năm 2001 khẳng định chưa từng nghe tên chất cấm meldonium"),
            _slot("sentence", 1, [_ddgs("Mykhailo Mudryk Chelsea Premier League")], "REUTERS", "Vụ dương tính cuối năm 2024 từng giáng đòn mạnh vào tâm lý Mudryk"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_ddgs("Mykhailo Mudryk Tottenham Hotspur match")], "PREMIER LEAGUE", "Sau án đình chỉ tới tháng 7/2026, Mudryk tái hợp HLV De Zerbi tại Tottenham"),
            _slot("sentence", 2, [_ddgs("Court of Arbitration for Sport CAS Lausanne")], "CAS", "Anh đã phải tự bỏ tiền thuê luật sư kháng cáo từ án 4 năm xuống nhẹ hơn"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(VNE_ECU_1)], "VNEXPRESS / HAVOLINE", "Sự cố bạo lực xảy ra ở phút bù giờ trận hạng Ba Ecuador"),
            _slot("sentence", 3, [_ddgs("Ecuador Football Federation FEF logo stadium")], "FEF", "Ủy ban Kỷ luật FEF phạt CLB Ciudad de Yantzaza nộp tiền và cấm sân"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(VNE_ECU_2)], "VNEXPRESS / HAVOLINE", "Trọng tài Ojeda cần tới 60 ngày nghỉ dưỡng sau ca phẫu thuật"),
            _slot("sentence", 4, [_ddgs("FIFA headquarters Zurich soccer")], "FIFA", "Hội Trọng tài Ecuador đồng thời xúc tiến hồ sơ tố cáo hình sự"),
        ],
    },

    # 14 (Nữ — BÓNG ĐÁ CHÂU Á)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "BÓNG ĐÁ QUỐC TẾ",
        "title": "Thủ môn Alireza Beiranvand lập cột mốc lịch sử khi lần đầu giành giải Cầu thủ xuất sắc nhất châu Á của AFC",
        "summary": (
            "Liên đoàn Bóng đá châu Á vừa tạo nên cột mốc chưa từng có khi trao danh hiệu Cầu thủ xuất sắc nhất châu Á năm 2026 cho thủ môn kỳ cựu người Iran Alireza Beiranvand. "
            "Ở tuổi 34, Beiranvand trở thành người gác đền đầu tiên trong lịch sử giành được phần thưởng cá nhân cao quý nhất của bóng đá châu lục nhờ màn trình diễn xuất thần suốt năm qua. "
            "Dấu ấn đậm nét nhất giúp anh chiến thắng là trận hòa 0-0 đầy quả cảm của Iran trước tuyển Bỉ tại World Cup 2026 với bảy pha cứu thua xuất sắc trước những ngôi sao như Kevin De Bruyne hay Leandro Trossard, bên cạnh ngôi á quân quốc gia cùng CLB Tractor FC. "
            "Cũng tại lễ trao giải, tiền vệ người Hàn Quốc Lee Kang-in của Atletico Madrid trở thành cầu thủ đầu tiên thắng hai năm liên tiếp hạng mục Ngôi sao châu Á thi đấu tại nước ngoài, còn giải nữ gọi tên Kim Kyong-yong của Triều Tiên."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / AFC",
        "stat_badges": {
            "2": {"label": "LỊCH SỬ BÓNG ĐÁ CHÂU Á", "value": "THỦ MÔN ĐẦU TIÊN", "sub": "Alireza Beiranvand ở tuổi 34"},
            "3": {"label": "TRẬN GẶP BỈ WORLD CUP", "value": "7 PHA CỨU THUA", "sub": "Giữ sạch lưới trước De Bruyne"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_BEIRANVAND)], "TUỔI TRẺ / AFC", "Thủ môn Alireza Beiranvand nhận giải Cầu thủ xuất sắc nhất châu Á 2026"),
            _slot("title", 0, [_ddgs("Alireza Beiranvand Iran goalkeeper save")], "AFC", "Người gác đền 34 tuổi khẳng định đây là vinh dự dành cho người dân Iran"),
            _slot("title", 0, [_ddgs("Lee Kang In Atletico Madrid football")], "AFC", "Lee Kang-in lập cú đúp danh hiệu Ngôi sao châu Á ở nước ngoài"),
            # Câu 1 (1 ảnh -> cinema / full / polaroid)
            _slot("sentence", 1, [_url(TT_BEIRANVAND)], "TUỔI TRẺ / AFC", "Khoảnh khắc lịch sử của thủ thành Iran tại lễ vinh danh của AFC"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_ddgs("Alireza Beiranvand Iran national football team")], "REUTERS", "Chưa từng có thủ môn nào giành giải thưởng cao quý này trước Beiranvand"),
            _slot("sentence", 2, [_ddgs("Tractor FC Tabriz Iran football")], "AFC", "Beiranvand đồng thời đưa Tractor FC giành ngôi á quân giải VĐQG Iran"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Alireza Beiranvand World Cup Iran goalkeeper")], "FIFA", "Bảy pha cản phá trước tuyển Bỉ giúp tên tuổi Beiranvand tỏa sáng rực rỡ"),
            _slot("sentence", 3, [_ddgs("Kevin De Bruyne Belgium World Cup match")], "REUTERS", "Ngay cả Kevin De Bruyne cũng bất lực trước phong độ của thủ thành Iran"),
            _slot("sentence", 3, [_ddgs("Iran national team World Cup 2026")], "AFC", "Dù bị loại tiếc nuối vì hiệu số, màn trình diễn của Beiranvand vẫn đi vào lịch sử"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_ddgs("Lee Kang In South Korea football player")], "KFA", "Lee Kang-in thắng hai năm liên tiếp giải Cầu thủ châu Á xuất sắc tại châu Âu"),
            _slot("sentence", 4, [_ddgs("AFC Annual Awards ceremony stage")], "AFC", "Kim Kyong-yong của Triều Tiên được vinh danh ở hạng mục bóng đá nữ"),
        ],
    },

    # 15 (Nam — ĐẠI HỘI TDTT 2026)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "ĐẠI HỘI TDTT 2026",
        "title": "Sân Thống Nhất 320 tỷ đồng khoác áo mới, hé lộ rước đuốc trên sông Sài Gòn & cải tổ Đại hội 2030",
        "summary": (
            "Tối ngày 19 tháng 11 tại công viên bờ sông Sài Gòn, lễ tổng duyệt khai mạc Đại hội Thể thao toàn quốc lần thứ X năm 2026 đã diễn ra hoành tráng với sự tham gia của hơn 1500 nghệ sĩ và vận động viên trước giờ khai màn chính thức tối ngày 21 tháng 11. "
            "Điểm nhấn đặc biệt của kỳ đại hội quy tụ 12000 thành viên từ 36 đoàn là nghi thức rước ngọn lửa truyền thống từ Bến Nhà Rồng trên mặt nước sông Sài Gòn kết hợp trình diễn dù lượn và mô tô nước. "
            "Song song đó, chủ nhà TP.HCM cũng hoàn tất diện mạo khang trang cho các công trình trọng điểm gồm sân Thống Nhất nâng cấp gần 320 tỷ đồng cùng nhà thi đấu Phú Thọ cải tạo 229 tỷ đồng. "
            "Tại hội nghị trưởng đoàn sáng cùng ngày, Cục Thể dục thể thao đề xuất cải tổ mạnh mẽ Đại hội năm 2030 tại Đà Nẵng theo hướng giảm 51 phần trăm xuống còn 476 nội dung thi đấu để tập trung nguồn lực cho 9 môn trọng điểm hướng tới ASIAD và Olympic."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / TUỔI TRẺ / DÂN TRÍ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "2": {"label": "QUY MÔ ĐẠI HỘI X", "value": "12000 NGƯỜI", "sub": "48 môn • 973 bộ huy chương"},
            "3": {"label": "ĐẦU TƯ HẠ TẦNG", "value": "320 TỶ ĐỒNG", "sub": "Sân Thống Nhất • Phú Thọ 229 tỷ"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_KM_ALL)], "TUỔI TRẺ", "Tổng duyệt lễ khai mạc Đại hội Thể thao toàn quốc 2026 trên sông Sài Gòn"),
            _slot("title", 0, [_url(TN_TN_2)], "THANH NIÊN", "Đường chạy điền kinh sân Thống Nhất hoàn thiện sau dự án 320 tỷ đồng"),
            _slot("title", 0, [_url(TT_KM_FIRE)], "TUỔI TRẺ", "Đài lửa Đại hội Thể thao toàn quốc rực sáng trong đêm tổng duyệt"),
            # Câu 1 (4 ảnh)
            _slot("sentence", 1, [_url(TT_KM_ALL)], "TUỔI TRẺ", "Chủ đề Khát vọng Vinh quang kết hợp nghệ thuật và thể thao hiện đại"),
            _slot("sentence", 1, [_url(TN_CAITO)], "THANH NIÊN / HCMC SPORTS HUB", "Hơn 1500 nghệ sĩ và vận động viên góp mặt trong đêm khai mạc tối 21/11"),
            _slot("sentence", 1, [_url(DT_HOINGHI)], "DÂN TRÍ", "Thứ trưởng Hoàng Đạo Cương kiểm tra và đánh giá cao công tác chuẩn bị của TP.HCM"),
            _slot("sentence", 1, [_url(TT_KM_FIRE)], "TUỔI TRẺ", "TP.HCM đăng cai 44 môn trong kỳ đại hội lớn nhất cả nước"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(TT_KM_TORCH)], "TUỔI TRẺ", "Nghi thức rước đuốc khởi nguồn từ khu vực Bến Nhà Rồng"),
            _slot("sentence", 2, [_url(TT_KM_PARA)], "TUỔI TRẺ", "Trình diễn dù lượn kết hợp ánh sáng rực rỡ trên bầu trời thành phố"),
            _slot("sentence", 2, [_url(TT_KM_JET)], "TUỔI TRẺ", "Các bộ môn thể thao mặt nước như jetski khuấy động sông Sài Gòn"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(TN_TN_1)], "THANH NIÊN", "Khán đài sân Thống Nhất được lắp mới đồng bộ phục vụ điền kinh"),
            _slot("sentence", 3, [_url(TN_TN_2)], "THANH NIÊN", "Mặt đường chạy đạt chuẩn sẵn sàng cho các kỷ lục mới"),
            _slot("sentence", 3, [_url(TN_TN_3)], "THANH NIÊN", "Mặt cỏ và hệ thống thoát nước tại sân Thống Nhất được nâng cấp toàn diện"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(DT_HOINGHI)], "DÂN TRÍ", "Hội nghị trưởng đoàn thảo luận lộ trình Đại hội 2030 tại Đà Nẵng"),
            _slot("sentence", 4, [_ddgs("Olympic shooting track swimming sports training Vietnam")], "CỤC TDTT", "Định hướng dồn lực cho 9 môn mũi nhọn gồm bắn súng, điền kinh, bơi, cử tạ"),
        ],
    },

    # 16 (Nữ — ĐẠI HỘI TDTT 2026)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "ĐẠI HỘI TDTT 2026",
        "title": "Đại hội 2026 bùng nổ: Vũ Thị Trang giúp TP.HCM thâu tóm 2 HCV cầu lông, Thùy Trang ghi bàn hạ Hà Nội",
        "summary": (
            "Sáng ngày 19 tháng 11 tại nhà thi đấu Hồ Xuân Hương, cầu lông TP.HCM tạo nên cú đúp huy chương vàng nội dung đồng đội nam và nữ đầy kịch tính tại Đại hội Thể thao toàn quốc 2026. "
            "Khi tỷ số chung kết đồng đội nữ với Hà Nội đang hòa 2-2, ban huấn luyện TP.HCM táo bạo ghép hai tay vợt đánh đơn Vũ Thị Trang và Vũ Thị Anh Thư vào trận đôi quyết định để thắng ngược cặp hạng năm quốc gia Lê Thu Huyền và Nguyễn Thị Thảo Ly với tỷ số 2-1, qua đó nhận thưởng nóng 50 triệu đồng cho mỗi đội cùng đội nam của Nguyễn Hải Đăng. "
            "Ở môn Vovinam chính thức bế mạc cùng ngày với sự hỗ trợ của công nghệ VAR, đoàn chủ nhà TP.HCM cũng bảo vệ thành công ngôi nhất toàn đoàn với 8 huy chương vàng, xếp trên Thanh Hóa và Cần Thơ. "
            "Khép lại ngày thi đấu sôi động trên sân Bà Rịa tối 19 tháng 11, tiền vệ 38 tuổi Trần Thị Thùy Trang băng xuống ghi bàn thắng duy nhất đầu hiệp hai giúp bóng đá nữ TP.HCM đánh bại Hà Nội 1-0 ở trận ra quân."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / TUỔI TRẺ / DÂN TRÍ",
        "credit": "TUỔI TRẺ / THANH NIÊN",
        "stat_badges": {
            "2": {"label": "CÚ ĐÚP CẦU LÔNG", "value": "50 TRIỆU / ĐỘI", "sub": "Vũ Thị Trang & Hải Đăng vô địch"},
            "3": {"label": "VOVINAM TOÀN ĐOÀN", "value": "8 HCV", "sub": "TP.HCM giữ vững ngôi nhất"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_CAULONG_1)], "TUỔI TRẺ", "Vũ Thị Trang và Vũ Thị Anh Thư ăn mừng chiến thắng nghẹt thở trước Hà Nội"),
            _slot("title", 0, [_url(TT_VOVINAM_1)], "TUỔI TRẺ", "Đoàn Vovinam TP.HCM áp đảo bảng tổng sắp với 8 huy chương vàng"),
            _slot("title", 0, [_url(TT_NU_TTRANG)], "TUỔI TRẺ / HCMWFC", "Lão tướng 38 tuổi Trần Thị Thùy Trang ghi bàn quyết định hạ Hà Nội"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TT_CAULONG_2)], "TUỔI TRẺ", "Cầu lông TP.HCM thâu tóm cả hai ngôi vô địch đồng đội sau hơn 20 năm"),
            _slot("sentence", 1, [_url(TN_NHD)], "THANH NIÊN / HCMS", "Nguyễn Hải Đăng giúp đội nam TP.HCM thắng chóng vánh Lâm Đồng 3-0"),
            _slot("sentence", 1, [_url(TT_CAULONG_3)], "TUỔI TRẺ", "Niềm vui trên bục huy chương của các tay vợt TP.HCM"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(TN_VTT)], "THANH NIÊN / HCMS", "Kinh nghiệm của Vũ Thị Trang tỏa sáng ở trận đánh đôi trái sở trường"),
            _slot("sentence", 2, [_url(TT_CAULONG_1)], "TUỔI TRẺ", "Hai chị em Trang và Thư thắng set quyết định 21-17 đầy cảm xúc"),
            _slot("sentence", 2, [_url(TT_CAULONG_2)], "TUỔI TRẺ", "Liên đoàn Cầu lông TP.HCM thưởng nóng ngay tại nhà thi đấu Hồ Xuân Hương"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(TT_VOVINAM_1)], "TUỔI TRẺ", "Công nghệ VAR giúp công tác trọng tài môn Vovinam diễn ra công bằng"),
            _slot("sentence", 3, [_url(TT_VOVINAM_2)], "TUỔI TRẺ", "Giải đấu quy tụ 400 võ sĩ từ 24 đơn vị tranh 26 bộ huy chương"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(TT_NU_TTRANG)], "TUỔI TRẺ / HCMWFC", "Trần Thị Thùy Trang dứt điểm tung lưới Hà Nội ngay phút 47"),
            _slot("sentence", 4, [_url(TT_NU_HN)], "TUỔI TRẺ / TS MEDIA", "Đội trưởng Hải Yến và CLB Hà Nội I bỏ lỡ cơ hội đáng tiếc trong hiệp một"),
        ],
    },

    # 17 (Nam — BÓNG ĐÁ SINH VIÊN)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "BÓNG ĐÁ VIỆT NAM",
        "title": "ĐH Bách khoa TP.HCM lập hat-trick vô địch giải bóng đá sinh viên ĐHQG TP.HCM - THACO Cup 2026",
        "summary": (
            "Chiều ngày 19 tháng 11 trên sân vận động Đông Hòa trước hàng nghìn khán giả cổ vũ cuồng nhiệt, trận chung kết giải bóng đá sinh viên Đại học Quốc gia TP.HCM mở rộng THACO Cup 2026 đã khép lại với ngôi vương thuộc về Trường Đại học Bách khoa TP.HCM. "
            "Đối đầu đối thủ khó chịu là Trường Đại học RMIT Việt Nam, các học trò HLV Nguyễn Thanh Nhã kiểm soát hoàn toàn thế trận trước khi định đoạt trận đấu ở phút 42 bằng cú đánh đầu hiểm hóc của số 11 Lê Hải Đăng từ quả tạt bên cánh phải của Nguyễn Nhật Khôi. "
            "Chiến thắng tối thiểu 1-0 giúp đội bóng áo xanh chính thức lập cú hat-trick vô địch ba năm liên tiếp kể từ mùa giải 2024 và thu hút hơn hai triệu lượt theo dõi trên nền tảng số. "
            "Ở lễ trao giải, Trường Đại học Bách khoa TP.HCM cũng thâu tóm luôn các danh hiệu cá nhân danh giá gồm Cầu thủ xuất sắc nhất cho Phạm Ngô Thế Dân và Vua phá lưới thuộc về Bùi Hòa Khánh với 8 bàn thắng."
        ),
        "source": "Thanh Niên",
        "news_source": "THANH NIÊN",
        "credit": "THANH NIÊN / NHẬT THỊNH",
        "stat_badges": {
            "2": {"label": "BÀN THẮNG VÀNG", "value": "PHÚT 42", "sub": "Cú đánh đầu của Lê Hải Đăng"},
            "3": {"label": "THỐNG TRỊ GIẢI ĐẤU", "value": "3 NĂM LIÊN TIẾP", "sub": "Vô địch 2024 • 2025 • 2026"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_BK_CUP)], "THANH NIÊN / NHẬT THỊNH", "Khoảnh khắc nâng cúp vô địch của ĐH Bách khoa TP.HCM"),
            _slot("title", 0, [_url(TN_BK_WIN)], "THANH NIÊN / NHẬT THỊNH", "Cầu thủ và ban huấn luyện vỡ òa cảm xúc sau tiếng còi mãn cuộc"),
            _slot("title", 0, [_url(TN_BK_CROWD)], "THANH NIÊN / NHẬT THỊNH", "Khán đài sân Đông Hòa phủ kín cổ động viên sinh viên"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TN_BK_CROWD)], "THANH NIÊN / NHẬT THỊNH", "Bầu không khí rực lửa tại sân vận động Đông Hòa chiều 19/11"),
            _slot("sentence", 1, [_url(TN_BK_ACT)], "THANH NIÊN / NHẬT THỊNH", "Giải đấu quy tụ 400 VĐV của 16 đội bóng tranh tài qua 32 trận"),
            _slot("sentence", 1, [_url(TN_BK_RMIT)], "THANH NIÊN / NHẬT THỊNH", "Hai đội tạo nên màn đối đầu đầy tốc độ và fair-play"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(TN_BK_GOAL)], "THANH NIÊN / NHẬT THỊNH", "Lê Hải Đăng đánh đầu ghi bàn thắng duy nhất ở phút 42"),
            _slot("sentence", 2, [_url(TN_BK_CELEB)], "THANH NIÊN / NHẬT THỊNH", "Niềm vui vỡ òa của các cầu thủ ĐH Bách khoa sau bàn mở tỷ số"),
            _slot("sentence", 2, [_url(TN_BK_RMIT)], "THANH NIÊN / NHẬT THỊNH", "ĐH RMIT nỗ lực phản công nhưng không thể xuyên thủng hàng thủ áo xanh"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_url(TN_BK_CUP)], "THANH NIÊN / NHẬT THỊNH", "ĐH Bách khoa TP.HCM khẳng định vị thế số một với chức vô địch thứ 3 liên tiếp"),
            _slot("sentence", 3, [_url(TN_BK_WIN)], "THANH NIÊN / NHẬT THỊNH", "Giải đấu ghi nhận hơn 2 triệu lượt xem trên kênh chính thức"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(TN_BK_MVP)], "THANH NIÊN / NHẬT THỊNH", "Phạm Ngô Thế Dân đoạt giải Cầu thủ xuất sắc nhất giải"),
            _slot("sentence", 4, [_url(TN_BK_ACT)], "THANH NIÊN / NHẬT THỊNH", "Chân sút Bùi Hòa Khánh giành Vua phá lưới với 8 pha lập công"),
        ],
    },

    # 18 (Nữ — CỜ TƯỚNG & CỜ VUA)
    {
        "id": 18,
        "art_id": "art_18",
        "group": "CỜ TƯỚNG & CỜ VUA",
        "title": "Báo Trung Quốc ca ngợi Lại Lý Huynh, Lang Kỳ Kỳ kết hôn cùng Đảng Phỉ; Carlsen gây tranh cãi bỏ ván",
        "summary": (
            "Dù chỉ về nhì trước Mạnh Phồn Duệ với cách biệt đúng 8 giây ở chung kết cờ tướng nhanh thế giới tại Singapore, kỳ thủ số một Việt Nam Lại Lý Huynh vừa được chuyên trang Quảng Tượng Võng của Trung Quốc ca ngợi là đối thủ đáng kính nhất trên bàn cờ sau hai chiến thắng thí quân đầy táo bạo trước Lưu Bách Hoành và Như Nhất Thuần. "
            "Cũng ở kỳ đàn Hoa ngữ, nữ đại sư Lang Kỳ Kỳ từng sát cánh đánh cặp cùng Lại Lý Huynh ở giải thế giới năm 2025 vừa xác nhận đăng ký kết hôn với kỳ thủ kỷ lục thế giới cờ tưởng mù Đảng Phỉ. "
            "Chuyển sang cờ vua thế giới tại giải Total Chess ở Budapest, nữ kỳ thủ Kazakhstan Bibisara Assaubayeva thẳng thắn mỉa mai vua cờ Magnus Carlsen sợ mất mốc 2800 Elo khi anh tự ý bỏ ván đấu cuối khiến cô phải chờ trước ghế trống 15 phút. "
            "Trong khi Carlsen vấp phải chỉ trích ở nhánh dưới, người sáng tạo nội dung cờ vua Levy Rozman của kênh GothamChess lại gây kinh ngạc khi đạt hơn 8,6 triệu lượt đăng ký YouTube, vượt xa cả Carlsen lẫn nhà vô địch thế giới Gukesh về sức ảnh hưởng mạng xã hội."
        ),
        "source": "Tuổi Trẻ / VnExpress",
        "news_source": "TUỔI TRẺ / VNEXPRESS",
        "credit": "TUỔI TRẺ / VNEXPRESS",
        "stat_badges": {
            "1": {"label": "CỜ TƯỚNG THẾ GIỚI", "value": "CHỈ KÉM 8 GIÂY", "sub": "Lại Lý Huynh thắng 2 đại sư TQ"},
            "3": {"label": "TRANH CÃI BUDAPEST", "value": "2801,2 ELO", "sub": "Carlsen bị tố né ván sợ mất Elo"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_LLH_1)], "TUỔI TRẺ / YCWB", "Lại Lý Huynh nhận mưa lời khen từ truyền thông cờ tướng Trung Quốc"),
            _slot("title", 0, [_url(TT_LKK_1)], "TUỔI TRẺ / CTNN", "Nữ đại sư Lang Kỳ Kỳ thông báo kết hôn với kỳ thủ Đảng Phỉ"),
            _slot("title", 0, [_url(TT_CARLSEN_1)], "TUỔI TRẺ / FIDE", "Magnus Carlsen gây tranh cãi khi bỏ ván đấu gặp Bibisara Assaubayeva"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TT_LLH_1)], "TUỔI TRẺ / YCWB", "Chuyên trang Quảng Tượng Võng phân tích sâu các nước thí quân của Lại Lý Huynh"),
            _slot("sentence", 1, [_url(TT_LLH_2)], "TUỔI TRẺ / TLKĐ", "Kỳ thủ Việt Nam phá vỡ thế độc tôn của dàn cao thủ Trung Quốc"),
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_09_2.jpg")], "SINCHEW", "Màn đấu trí căng thẳng giữa Lại Lý Huynh và Mạnh Phồn Duệ ở chung kết"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(TT_LKK_1)], "TUỔI TRẺ / CTNN", "Lang Kỳ Kỳ và Đảng Phỉ là cặp đôi nổi tiếng của làng cờ Hoa ngữ"),
            _slot("sentence", 2, [_url(TT_LKK_2)], "TUỔI TRẺ / LĐCTVN", "Nữ kỳ thủ sinh năm 1999 từng cùng Lại Lý Huynh vô cùng ăn ý năm 2025"),
            _slot("sentence", 2, [_url(TT_DANGPHI)], "TUỔI TRẺ / LIÊN HỢP TẢO BÁO", "Đảng Phỉ từng lập kỷ lục Guinness đấu cờ tưởng cùng lúc 25 người"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(TT_CARLSEN_1)], "TUỔI TRẺ / FIDE", "Bibisara ngồi chờ 15 phút trước chiếc ghế trống của Magnus Carlsen"),
            _slot("sentence", 3, [_url(TT_CARLSEN_2)], "TUỔI TRẺ / FIDE", "Dù dẫn điểm áp đảo nhưng Carlsen bị xử thua hai ván do vắng mặt"),
            _slot("sentence", 3, [_local(DAILY_19 / "Tin_14_1.jpg")], "THANH NIÊN / CHESS.COM", "Trong khi đó Lê Quang Liêm tranh hạng bảy cùng Ian Nepomniachtchi"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(VNE_ROZMAN_KANE)], "VNEXPRESS / BMFC", "Levy Rozman giao lưu đánh cờ cùng Harry Kane và Michael Olise ở Bayern"),
            _slot("sentence", 4, [_ddgs("Levy Rozman GothamChess chess interview")], "CHESS.COM", "Kênh GothamChess đạt 5,9 tỷ lượt xem cùng hai cuốn sách bán chạy hàng đầu"),
        ],
    },

    # 19 (Nam — THỂ THAO QUỐC TẾ)
    {
        "id": 19,
        "art_id": "art_19",
        "group": "THỂ THAO QUỐC TẾ",
        "title": "Rúng động điền kinh thế giới: Nhà vô địch marathon Olympic Peres Jepchirchir bị cấm 3 năm vì EPO",
        "summary": (
            "Đơn vị Liêm chính Điền kinh vừa giáng cú sốc lớn vào làng chạy bộ đường dài thế giới khi ra quyết định cấm thi đấu ba năm đối với nhà vô địch marathon Olympic Tokyo và đương kim vô địch thế giới là Peres Jepchirchir. "
            "Mẫu xét nghiệm thu hồi tháng 7 năm 2026 của chân chạy 33 tuổi người Kenya phát hiện dương tính với chất cấm EPO, hormone kích thích sản sinh hồng cầu giúp tăng sức bền. "
            "Án phạt buộc toàn bộ thành tích của Jepchirchir từ giữa tháng 7 bị hủy bỏ, đồng nghĩa cô chính thức bị tước luôn ngôi vô địch giải Sydney Marathon 2026 từng đạt thông số 2 giờ 18 phút 31 giây. "
            "Cùng ngày, cơ quan chống doping còn treo giò ba năm Veronica Loleo và cấm sáu năm Ronald Korir, nâng tổng số vận động viên Kenya từng bị xử phạt từ năm 2017 lên gần 150 trường hợp."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / AFP",
        "stat_badges": {
            "1": {"label": "ÁN PHẠT ĐIỀN KINH", "value": "CẤM 3 NĂM", "sub": "Peres Jepchirchir dương tính EPO"},
            "3": {"label": "TƯỚC DANH HIỆU", "value": "SYDNEY 2026", "sub": "Hủy toàn bộ thành tích từ 17/7"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_JEP_1)], "VNEXPRESS / AFP", "Peres Jepchirchir bị tước chức vô địch Sydney Marathon và cấm 3 năm"),
            _slot("title", 0, [_url(VNE_LOLEO)], "VNEXPRESS / COLIN MULVANY", "Đồng hương Veronica Loleo cũng nhận án treo giò ba năm vì EPO"),
            _slot("title", 0, [_ddgs("Peres Jepchirchir Tokyo Olympics marathon gold")], "REUTERS", "Nhà vô địch marathon Olympic Tokyo từng lập nhiều kỷ lục thế giới"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(VNE_JEP_1)], "VNEXPRESS / AFP", "Jepchirchir từng đánh bại Tigst Assefa ở giải vô địch thế giới 2025"),
            _slot("sentence", 1, [_ddgs("Peres Jepchirchir London Marathon finish")], "AP PHOTO", "Cô từng là nữ VĐV đầu tiên vô địch cả Olympic lẫn New York Marathon cùng năm"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_ddgs("Peres Jepchirchir marathon runner race action")], "GETTY", "Mẫu thử hồi tháng 7 phát hiện chất cấm EPO trong cơ thể Jepchirchir"),
            _slot("sentence", 2, [_ddgs("Athletics Integrity Unit doping test laboratory")], "REUTERS", "Chân chạy Kenya đã ký văn bản thừa nhận vi phạm quy định chống doping"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_ddgs("Sydney Marathon Harbour Bridge runners")], "AP PHOTO", "Chức vô địch Sydney Marathon 2026 của cô chính thức bị hủy kết quả"),
            _slot("sentence", 3, [_ddgs("Peres Jepchirchir Boston Marathon winner")], "REUTERS", "Từ ngày 17/7 mọi huy chương và giải thưởng của Jepchirchir đều bị tước"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(VNE_LOLEO)], "VNEXPRESS / COLIN MULVANY", "Veronica Loleo vừa giành HCB half marathon thế giới cũng dính EPO"),
            _slot("sentence", 4, [_ddgs("Kenya marathon runners training rift valley")], "REUTERS", "Điền kinh Kenya dẫn đầu thống kê các trường hợp vi phạm doping của AIU"),
        ],
    },

    # 20 (Nữ — THỂ THAO QUỐC TẾ)
    {
        "id": 20,
        "art_id": "art_20",
        "group": "THỂ THAO QUỐC TẾ",
        "title": "Bi kịch cử tạ Malaysia: Nhà vô địch Khối Thịnh vượng chung 21 tuổi mất cánh tay phải sau tai nạn",
        "summary": (
            "Thể thao Đông Nam Á bàng hoàng trước bi kịch vừa giáng xuống đô cử trẻ tài năng bậc nhất của Malaysia là Muhammad Hafizuddin Roslin. "
            "Sau vụ tai nạn xe máy nghiêm trọng tối ngày 16 tháng 11 trên đường cao tốc tại Kuala Lumpur khiến xương tay gãy nát và tổn thương mạch máu nặng, các bác sĩ dù nỗ lực suốt ca phẫu thuật gần bảy tiếng vẫn buộc phải cắt cụt cánh tay phải trên khuỷu để cứu lấy mạng sống cho chàng trai 21 tuổi. "
            "Trước tai nạn thương tâm này, Hafizuddin từng giành huy chương vàng lịch sử hạng 88 kg nam tại Đại hội Khối Thịnh vượng chung hồi tháng 7 ở Glasgow với tổng cử 345 kg và là niềm hy vọng lớn cho SEA Games lẫn Olympic Los Angeles 2028. "
            "Hiện thể trạng của anh đã tỉnh táo, trong khi Chính phủ Malaysia và các cơ quan an sinh cam kết lo toàn bộ viện phí, lắp tay giả, trợ cấp suốt đời và mở đường đưa anh sang công tác huấn luyện."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / AP / AFP",
        "stat_badges": {
            "2": {"label": "CA MỔ KHẨN CẤP", "value": "GẦN 7 TIẾNG", "sub": "Phải cắt tay phải để giữ tính mạng"},
            "3": {"label": "KỶ LỤC ĐẠI HỘI", "value": "345 KG", "sub": "HCV hạng 88 kg Glasgow 2026"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_MALAY_1)], "VNEXPRESS / AP", "Hafizuddin Roslin trên bục nhận HCV hạng 88 kg Khối Thịnh vượng chung"),
            _slot("title", 0, [_url(VNE_MALAY_2)], "VNEXPRESS / AFP", "Bộ trưởng Thể thao Malaysia tới bệnh viện thăm hỏi và cầu nguyện cho đô cử 21 tuổi"),
            _slot("title", 0, [_ddgs("weightlifting Commonwealth Games barbell lift")], "AP PHOTO", "Tương lai thi đấu đỉnh cao của tài năng cử tạ Malaysia bất ngờ khép lại"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(VNE_MALAY_1)], "VNEXPRESS / AP", "Hafizuddin là niềm tự hào lớn của thể thao bang Perlis và Malaysia"),
            _slot("sentence", 1, [_ddgs("Bukit Jalil National Sports Complex Kuala Lumpur")], "BERNAMA", "Chuyến đi từ Ampang tới Bukit Jalil đêm 16/11 đã dẫn tới biến cố đau lòng"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(VNE_MALAY_2)], "VNEXPRESS / AFP", "Chủ tịch Liên đoàn Cử tạ Malaysia xác nhận ca mổ kéo dài gần 7 tiếng"),
            _slot("sentence", 2, [_ddgs("Kuala Lumpur Hospital Malaysia building")], "THE STAR", "Đội ngũ y bác sĩ buộc phải cắt cụt trên khuỷu để ngăn biến chứng nguy hiểm"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_ddgs("Glasgow Commonwealth Games weightlifting arena")], "REUTERS", "Tháng 7 vừa qua anh lập kỷ lục đại hội với 162 kg cử giật và 183 kg cử đẩy"),
            _slot("sentence", 3, [_ddgs("Malaysia national weightlifting team athlete")], "BERNAMA", "HLV trưởng Edmund Yeo bật khóc khi hay tin dữ về cậu học trò cưng"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_url(VNE_MALAY_2)], "VNEXPRESS / AFP", "Chính phủ Malaysia tài trợ trọn gói phục hồi chức năng và chuyên gia tâm lý"),
            _slot("sentence", 4, [_ddgs("olympic weightlifting coaching barbell gym")], "REUTERS", "Liên đoàn Cử tạ Malaysia sẽ hỗ trợ anh chuyển hướng làm huấn luyện viên"),
        ],
    },

    # 21 (Nam — QUẦN VỢT QUỐC TẾ)
    {
        "id": 21,
        "art_id": "art_21",
        "group": "THỂ THAO QUỐC TẾ",
        "title": "ATP Finals 2026 tại Turin: Alexander Zverev toàn thắng vòng bảng, Ben Shelton lần đầu vào bán kết",
        "summary": (
            "Khép lại bản tin hôm nay là những diễn biến nóng bỏng tại giải quần vợt danh giá cuối năm ATP Finals 2026 trên sân cứng trong nhà tại Turin, Italy. "
            "Ở lượt trận cuối bảng John McEnroe đêm ngày 19 tháng 11, hạt giống số một Alexander Zverev đánh bại tay vợt Pháp Arthur Fils sau hai set căng thẳng với tỷ số 6-4 và 7-6 để hoàn tất thành tích 3 trận toàn thắng tuyệt đối. "
            "Trong trận đấu còn lại của bảng đấu này, tay vợt người Mỹ Ben Shelton vượt qua tài năng Tây Ban Nha Rafael Jodar với các tỷ số 7-6 và 7-5 để cán đích ở vị trí 2 thắng 1 thua, qua đó lần đầu tiên trong sự nghiệp giành vé vào bán kết ATP Finals. "
            "Hai tấm vé đi tiếp này hứa hẹn những cặp đấu bán kết nảy lửa vào cuối tuần khi ở bảng Ivan Lendl bên kia, ngôi sao Carlos Alcaraz dù gặp đôi chút vấn đề ở gân kheo đùi trái vẫn sớm chắc suất sau hai chiến thắng áp đảo trước Tiafoe và Medvedev."
        ),
        "source": "ATP Tour / VnExpress",
        "news_source": "ATP TOUR / VNEXPRESS",
        "credit": "ATP TOUR / REUTERS",
        "stat_badges": {
            "2": {"label": "BẢNG JOHN MCENROE", "value": "6-4, 7-6", "sub": "Zverev toàn thắng 3-0 vòng bảng"},
            "3": {"label": "CỘT MỐC SỰ NGHIỆP", "value": "7-6, 7-5", "sub": "Ben Shelton lần đầu vào bán kết"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Alexander Zverev ATP Finals Turin tennis match")], "ATP TOUR", "Alexander Zverev khép lại vòng bảng ATP Finals 2026 với thành tích toàn thắng"),
            _slot("title", 0, [_ddgs("Ben Shelton tennis serve celebration ATP")], "ATP TOUR", "Ben Shelton lần đầu tiên góp mặt ở bán kết giải đấu quy tụ 8 tay vợt hay nhất năm"),
            _slot("title", 0, [_local(DAILY_19 / "Tin_15_1.jpg")], "DÂN TRÍ / ATP TOUR", "Carlos Alcaraz sớm giành vé đi tiếp ở bảng Ivan Lendl"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_ddgs("Inalpi Arena Turin ATP Finals tennis court")], "ATP TOUR", "Không khí cuồng nhiệt tại nhà thi đấu Inalpi Arena ở Turin"),
            _slot("sentence", 1, [_ddgs("ATP Finals Turin trophy court indoor")], "ATP TOUR", "Các tay vợt hàng đầu thế giới bước vào giai đoạn quyết định tranh cúp cuối năm"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_ddgs("Alexander Zverev forehand tennis match")], "REUTERS", "Hạt giống số một Alexander Zverev thắng thuyết phục 6-4, 7-6"),
            _slot("sentence", 2, [_ddgs("Arthur Fils French tennis player action")], "ATP TOUR", "Tay vợt trẻ Arthur Fils gây nhiều khó khăn ở set hai nhưng vẫn gục ngã ở tie-break"),
            _slot("sentence", 2, [_ddgs("Alexander Zverev celebration indoor hard court")], "REUTERS", "Zverev duy trì phong độ ổn định nhất giải với 3 trận toàn thắng"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Ben Shelton tennis forehand indoor court")], "ATP TOUR", "Ben Shelton cứu nhiều điểm số quan trọng để thắng 7-6, 7-5"),
            _slot("sentence", 3, [_ddgs("Rafael Jodar Spanish tennis player")], "ATP TOUR", "Rafael Jodar khép lại lần đầu dự giải cuối năm với nhiều bài học quý"),
            _slot("sentence", 3, [_ddgs("Ben Shelton smiling post match tennis")], "REUTERS", "Ngôi sao người Mỹ mở ra cột mốc bán kết đầu tiên tại ATP Finals"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_15_1.jpg")], "DÂN TRÍ / ATP TOUR", "Carlos Alcaraz đang sở hữu chuỗi 11 trận thắng liên tiếp ấn tượng"),
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_15_5.jpg")], "ATP TOUR", "Tay vợt Tây Ban Nha theo dõi sát tình trạng cơ đùi trái trước bán kết"),
            _slot("sentence", 4, [_local(DAILY_19 / "Tin_15_6.jpg")], "REUTERS", "Medvedev và Tiafoe cạnh tranh tấm vé còn lại của bảng Ivan Lendl"),
        ],
    },
]
