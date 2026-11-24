# -*- coding: utf-8 -*-
"""
daily_24_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 24.11.2026
(Tổng hợp song hành báo Việt Nam & Thế Giới: 12:00 ngày 23.11 đến 08:55 ngày 24.11.2026).
Tuân thủ quy chuẩn Anti-Bundling (1 sự kiện / 1 vấn đề = 1 tin, 3–5 câu súc tích):
  - Intro (00): Song giọng Nữ (Ngọc Huyền #14) & Nam (Minh Quân Pro #15), hide_title=True
  - 28 bản tin chính độc lập (01–28): mỗi tin 1 vấn đề rõ ràng, luân phiên Nam/Nữ
  - Mục 29 (CÁC TIN THỂ THAO KHÁC): 100% Giọng Nữ (Ngọc Huyền #14) điểm nhanh tin bên lề
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


# ── URL ảnh báo chí sạch gốc 23–24.11.2026 (Việt Nam & Thế Giới) ──

# U17 Việt Nam vs U17 New Zealand & Cục diện Bảng G & Phản ứng FIFA
VNE_U17_1 = "https://i1-thethao.vnecdn.net/2026/11/24/6b-1795456202-1795456519-1795478428.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=8p_pPI4Lthkr9jA_ZGe3xg"
VNE_U17_2 = "https://i1-thethao.vnecdn.net/2026/11/24/9-1795456252-1795456520.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=0wERMuCpOlnwtKRQUr8zOQ"
VNE_U17_3 = "https://i1-thethao.vnecdn.net/2026/11/24/929369171-1132320632848041-4421121707457188554-n-1795457977-1795458042.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=jAWR-DGX1q2AT2niixTUpQ"
VNE_U17_4 = "https://i1-thethao.vnecdn.net/2026/11/24/13-7497-1795460980.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=FoDOelDabuG4RG2ocYij-A"
DT_U17_NL = "https://cdnphoto.dantri.com.vn/08cw1bAImISG1hQdFNoZDIg-9o4=/thumb_w/1020/2026/11/24/nguyenluc-1795478648596.jpg"
DT_U17_DN = "https://cdnphoto.dantri.com.vn/_JfzoX7B3gukuqHXWFrpKG3TG7I=/thumb_w/1020/2026/11/24/u17vn2-edited-1795479007425.jpg"
DT_U17_DK = "https://cdnphoto.dantri.com.vn/VSNnw2SDqHgmU4ly7qobAfMQ_dE=/thumb_w/1020/2026/11/24/u17vn3-1795478581191.jpg"
DT_U17_NZ = "https://cdnphoto.dantri.com.vn/le-YqXuOmt9snyhngL9jOnKAzn0=/thumb_w/1020/2026/11/24/jack-clegg-edited-1795483652873.jpg"
DT_U17_CEL = "https://cdnphoto.dantri.com.vn/xOr2Ry4LwP3rlpNBk-gqvGEWVM0=/thumb_w/1020/2026/11/24/img9482-1536x1000-edited-1795483586989.jpg"
DT_U17_ROL1 = "https://cdnphoto.dantri.com.vn/XTmhHkK4a01xEY7f5_aOi0UMIYM=/thumb_w/1020/2026/11/24/roland1-1795477168317.jpg"
DT_U17_ROL2 = "https://cdnphoto.dantri.com.vn/fTL4PrZ2bKak84DJcDqHD8QDSlE=/thumb_w/1020/2026/11/24/roland2-1795477168780.jpg"
DT_U17_CDV = "https://cdnphoto.dantri.com.vn/QHIQsEY5YC1N6bLrkU903BZZ0Rw=/thumb_w/1020/2026/11/24/cdvvvn-1795477167875.jpg"
TN_U17_FIFA = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/u17-vn-1795481152863397374499.jpg"
TN_U17_ROL = "https://images2.thanhnien.vn/528068263637045248/2026/11/24/hlv-roland-1795481152893536784473.jpg"
TN_U17_NL2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/u17-2-17954563777421047966338.jpeg"
TN_U17_HANG = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/u17-5-17954563777881385896304.jpeg"
TN_U17_TEAM = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/doi-hinh-ra-san-cua-u17-viet-nam-gap-u17-new-zealand-1795453707425515717099.jpg"
TN_U17_VFF4 = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/u17-4-1795456377783795849849.jpeg"
TT_U17_FIFA = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/92192128623367284538157605075562656715891165n-17954526717951599403635.jpg"
TT_U17_MALI = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/anh-chup-man-hinh-2026-11-24-010532-17954571641262045942428.png"

# Đại hội Thể thao toàn quốc 2026 — Bơi lội, Bóng đá nữ, Cờ tướng, Billiards, Xe đạp, Cầu lông, Quần vợt
TN_BOI_TH = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/tnw-179534799825149514889221558536664951488922155853666a347ffbbbd55a2362f37322925fc3a87-179535477696193133095.jpg"
TN_BOI_TH2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/tnw-1795349643091495148892215585366649514889221558536665ef47fc891519928b147ca6e0ad674f4-179535477643170142949.jpg"
TN_AV_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/22/tnw-1795349643099495148892215585366649514889221558536665e4b60650e3e04a322d89545e5e7c46a-1795354776707972330035.jpg"
TN_AV_CDV = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/anh-vien-1795442400544257970151.jpg"
TT_AV_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/179544723414920664181444029384276225853887195716592d7f747b0d6e199c1774b62ae76e5aeb3-1795447645440595355110.jpg"
TT_AV_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/17954472340142066418144402938427622585388719571659206824b563135f548ade6fdd8f38151a4-1795447645455700473198.jpg"
TT_PTB_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/17954535691602066418144402938427622585388719571659234037949dd4c05d0f7466deb52cc538e-1795456095027737714377.jpg"
TT_PTB_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/1795453568986206641814440293842762258538871957165928ab16a51b25cfe118bbba1b8e34a7717-1795456095022784640040.jpg"
TT_NINO_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/179544882040720664181444029384276225853887195716592711e44fe7bdc1dca401c88d512ca9589-1795452316661123029415.jpg"
DT_HH_1 = "https://cdnphoto.dantri.com.vn/MDCmy_gA_kbnS06SQf8R53D8Gsc=/thumb_w/1020/2026/11/23/huyhoang2t23-11-26-1795450220840.png"
VNE_BOI_1 = "https://i1-thethao.vnecdn.net/2026/11/22/asdasd-1795352556-9014-1795352600.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=xRabAcyB_YF23g0KVJgPkA"
TT_KTHUA_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/kthua-an-mung--1795451561213756306971.jpeg"
TT_TN_HN_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/thai-nguyen-ao-vang-va-ha-noi-17954522731462072038990.jpg"
TT_CT_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/lai-ly-huynh-thanh-bao-ha-van-tien-1795444414304427020755.png"
TT_CVH_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/chu-viet-hoang-billiards-pool-9-bi-dai-hoi-the-thao-toan-quoc-1-17954277434861921965514.jpg"
TT_CVH_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/chu-viet-hoang-billiards-pool-9-bi-dai-hoi-the-thao-toan-quoc-2-17954277435011526584009.jpg"
TT_CVH_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/chu-viet-hoang-billiards-pool-9-bi-dai-hoi-the-thao-toan-quoc-3-1795427743504900211180.jpg"
TN_CVH_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/17954261826076144854729594737154g515009901787652961c16f15bb3d9ef9422592b1b0b437f589-17954279222651360970145.jpeg"
TT_XD_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/le-ngoc-son-xe-dap-dai-hoi-the-thao-toan-quoc-2026-1795421365849206369162.jpeg"
TT_XD_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/le-ngoc-son-xe-dap-dai-hoi-the-thao-toan-quoc-2026-2-17954213658451133979457.jpeg"
TT_XD_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/base64-17954235086871584892998.jpeg"
TT_TH_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/nguyen-thi-thu-huyen-cau-long-dai-hoi-the-thao-toan-quoc-179544824848967928788.jpeg"
TT_QV_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/quan-vot-tphcm-dai-hoi-the-thao-toan-quoc-2026-1795439323869612468751.jpg"

# CAHN vs Vissel Kobe, Xuân Son, Lê Quang Liêm
TN_CAHN_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/hlv-polking-17954326016001545730894.jpg"
DT_XS_1 = "https://cdnphoto.dantri.com.vn/E7dyu_oB1viLSAmblLhJ7m88cyI=/thumb_w/1020/2026/11/23/z61532945829297fd85ab5ee3bdfb6fbb75a223c1da542-1734869456613-1737014878500-1738950746169-1795436255356.jpg"
DT_SON_1 = "https://cdnphoto.dantri.com.vn/gRDbtbpuvTUG90Fw_BaAJjUjtsg=/thumb_w/1020/2026/11/23/son-1-1782816185403434201202-1795436322973.jpeg"
TT_LQL_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/le-quang-liem-edit-1795224090141452811307-17954776027781377089516.jpg"
TT_LQL_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/20/5566283729987d247869ck-17951359908931000528429.jpg"
TT_LQL_3 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/nhanhchop20131-1795478689770833099208.jpg"

# Quốc tế sạch từ Sky Sports (1600x900), VnExpress, Thanh Niên, Tuổi Trẻ, Dân Trí
SKY_BRE_1 = "https://e0.365dm.com/26/11/1600x900/skysports-lewis-potter-outarra_7414942.jpg?20261123231353"
VNE_YORO_1 = "https://i1-thethao.vnecdn.net/2026/11/23/a-nh-ma-n-hi-nh-lu-c-179539758-4474-6867-1795397649.png?w=1200&h=675&q=100&dpr=1&fit=crop&s=7b_KzA9NsraqlzXTFWxEkA"
VNE_YORO_2 = "https://i1-thethao.vnecdn.net/2026/11/23/A-nh-ma-n-hi-nh-2026-11-23-lu-2171-9189-1795397649.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=phywvmASYwYarpX7fA1Ehw"
SKY_YORO_1 = "https://e2.365dm.com/26/11/1600x900/skysports-leny-yoro-alexander-isak_7413680.jpg?20261122164441"
VNE_NEV_1 = "https://iv1.vnecdn.net/thethao/images/web/2026/11/23/neville-tu-tat-lien-tiep-vao-mat-khi-binh-luan-ve-man-utd-1795426476.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=H0zv58q_85SPvw4r5AAZzQ"
VNE_NEV_2 = "https://i1-thethao.vnecdn.net/2026/11/23/Man-Utd-9819-1795426746.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=LZZXLF2sF2z7uxU_QTMxZw"
SKY_RAYA_1 = "https://e0.365dm.com/26/11/1600x900/skysports-david-raya-arsenal_7412827.jpg?20261121190915"
VNE_BAY_1 = "https://i1-thethao.vnecdn.net/2026/11/23/Musiala-8835-1795411972.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=yyXDCA9F7LlM9_Sp9XiaHw"
VNE_BAY_2 = "https://i1-thethao.vnecdn.net/2026/11/23/Hoeness-9593-1795411973.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=h-diB9bgWan3QoZ4gOq-MQ"
VNE_BAY_3 = "https://i1-thethao.vnecdn.net/2026/11/23/Musiala-2-6094-1795411973.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=r0VSf4AQBv84IyOhf5uz1Q"
VNE_BAY_4 = "https://i1-thethao.vnecdn.net/2026/11/23/2023-09-20T190632Z-538629172-M-6939-7793-1795419961.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Q5HBLpf5Ud-gcyvrecO6ZQ"
TN_U17_CHN = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/img8831-1795454626656508551597.jpeg"
TN_U17_ESP = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/17954541622052055466824288530363592341489461183749101cef30f178f034e1df4bc905b0cc29-1795454216483802974620.jpg"
TT_U17_CHN = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/24/29302-17954798356481500874174-346-66-864-1055-crop-17954798650641398682382.png"
TN_WWC_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/17954497183082055466824288530363592341489461183749b1328e9cef52e9145d4983d21fe6dfaa-17954497400181251329826.jpg"
TN_WWC_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/23/179544969343320554668242885303635923414894611837490f9152d9b3d1dd68d4bf89a1a89de37a-1795449783243524531481.jpg"
TT_WWC_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/anh-chup-man-hinh-2026-11-24-luc-063702-17954770422371908172446.png"
TT_GEO_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/edit-georgescu-1795418114327316242935.jpeg"
TT_GEO_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/georgescu-2-179541846575321126515.jpg"
DT_MES_1 = "https://cdnphoto.dantri.com.vn/bVADEhqyx4uFXh-MQcwHjB7KrfY=/thumb_w/1020/2026/11/23/img0737-1795425661333.jpeg"
DT_MES_2 = "https://cdnphoto.dantri.com.vn/sDB3MWbAxVlAv8eIZMEb64eCaa8=/thumb_w/1020/2026/11/23/img0738-1795425661078.jpeg"
SKY_SIN_1 = "https://e0.365dm.com/26/07/1600x900/skysports-tennis-jannik-sinner_7294862.jpg?20260710182746"
TT_WTT_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/tran-vien-vu-1-1795436266589266554896.jpg"
TT_WTT_2 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/vobdnidqk2a8-jklabevvhntnda-vvingl3jtsa1-iehf6-yl02uuigvlmqxvbd1bw6p6vg1j6lj2rhn4xpphvkyajhxvjnn46r57xl8dm5imnjhbdzsu1qga-sigecbjgzo9tg5c7jgwt-17954364575621629377495.jpg"
SKY_PEN_1 = "https://e0.365dm.com/26/11/1600x900/skysports-marco-penge-golf_7414755.jpg?20261123195744"
TT_MMA_1 = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/23/chris-leben-2-1795417430771455516977.jpg"
SKY_BAK_1 = "https://e0.365dm.com/25/02/1600x900/skysports-martin-bakole-boxing_6838083.jpg?20250224162953"
SKY_LPGA_1 = "https://e0.365dm.com/24/09/1600x900/skysports-megan-khang-golf_6686863.jpg?20240915183508"
SKY_NFL_1 = "https://e0.365dm.com/26/11/1600x900/skysports-dk-metcalf-pittsburgh-steelers_7414686.jpg?20261123175053"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 24.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 24 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất tại Việt Nam và trên toàn thế giới. "
        "Ở đấu trường quốc nội, đội tuyển U17 Việt Nam tạo nên cuộc rượt đuổi cảm xúc hòa U17 New Zealand 3-3 để giành điểm số World Cup đầu tiên trong lịch sử, trong khi đường đua bơi Đại hội Thể thao toàn quốc chứng kiến Nguyễn Thúy Hiền phá năm kỷ lục, Nguyễn Thị Ánh Viên giành huy chương vàng tái xuất cùng kỷ lục quốc gia mới của Phạm Thanh Bảo. "
        "Trên sân cỏ châu Âu, Brentford đè bẹp Everton 4-0 tại Ngoại hạng Anh, Manchester United kháng cáo thẻ đỏ của Leny Yoro giữa cơn thịnh nộ của Gary Neville, còn Bayern Munich đối mặt khủng hoảng kép quanh Harry Kane và Jamal Musiala. "
        "Bên cạnh đó là bước ngoặt đăng cai World Cup nữ của FIFA, ca phẫu thuật đầu gối khiến Jannik Sinner nguy cơ lỡ giải Úc mở rộng, cú sốc bóng bàn Trung Quốc cùng nhiều tin tức thể thao đáng chú ý khác ngay sau đây."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí / BBC Sport / Sky Sports / The Guardian",
    "news_source": "VIỆT NAM & THẾ GIỚI",
    "credit": "ĐIỂM ĐỌC TỔNG HỢP",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 24 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất tại Việt Nam và trên toàn thế giới.",
        },
        {
            "voice_preset": "primary",
            "text": "Ở đấu trường quốc nội, đội tuyển U17 Việt Nam tạo nên cuộc rượt đuổi cảm xúc hòa U17 New Zealand 3-3 để giành điểm số World Cup đầu tiên trong lịch sử, trong khi đường đua bơi Đại hội Thể thao toàn quốc chứng kiến Nguyễn Thúy Hiền phá năm kỷ lục, Nguyễn Thị Ánh Viên giành huy chương vàng tái xuất cùng kỷ lục quốc gia mới của Phạm Thanh Bảo.",
        },
        {
            "voice_preset": "secondary",
            "text": "Trên sân cỏ châu Âu, Brentford đè bẹp Everton 4-0 tại Ngoại hạng Anh, Manchester United kháng cáo thẻ đỏ của Leny Yoro giữa cơn thịnh nộ của Gary Neville, còn Bayern Munich đối mặt khủng hoảng kép quanh Harry Kane và Jamal Musiala.",
        },
        {
            "voice_preset": "primary",
            "text": "Bên cạnh đó là bước ngoặt đăng cai World Cup nữ của FIFA, ca phẫu thuật đầu gối khiến Jannik Sinner nguy cơ lỡ giải Úc mở rộng, cú sốc bóng bàn Trung Quốc cùng nhiều tin tức thể thao đáng chú ý khác ngay sau đây.",
        },
    ],
    "stat_badges": {
        "1": {"label": "BẢN TIN NGÀY", "value": "24.11.2026", "sub": "Toàn cảnh Việt Nam & Thế giới"},
        "2": {"label": "U17 WORLD CUP", "value": "VIỆT NAM 3-3 NZ", "sub": "Điểm số lịch sử • VFF thưởng 400 triệu"},
        "3": {"label": "NGOẠI HẠNG ANH", "value": "BRENTFORD 4-0", "sub": "Everton vỡ trận vì thẻ đỏ Tarkowski"},
    },
    "slots": [
        # Câu 1 (4 ảnh)
        _slot("sentence", 1, [_url(DT_U17_CEL)], "DÂN TRÍ / VFF", "Các cầu thủ U17 Việt Nam ăn mừng điểm số đầu tiên trong lịch sử dự U17 World Cup"),
        _slot("sentence", 1, [_url(TT_AV_1)], "TUỔI TRẺ", "Nguyễn Thị Ánh Viên rạng rỡ nhận HCV tiếp sức đầu tiên sau gần bốn năm giải nghệ"),
        _slot("sentence", 1, [_url(SKY_BRE_1)], "SKY SPORTS", "Keane Lewis-Potter tỏa sáng giúp Brentford đè bẹp Everton 4-0 ở Ngoại hạng Anh"),
        _slot("sentence", 1, [_url(SKY_SIN_1)], "SKY SPORTS", "Jannik Sinner chuẩn bị phẫu thuật đầu gối và có nguy cơ vắng mặt tại Úc mở rộng"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(VNE_U17_2)], "VNEXPRESS", "Duy Khang đánh đầu phút 90+2 mang về trận hòa 3-3 giàu cảm xúc trước New Zealand"),
        _slot("sentence", 2, [_url(TN_BOI_TH)], "THANH NIÊN", "Kình ngư 17 tuổi Nguyễn Thúy Hiền giành năm HCV và phá năm kỷ lục sau hai ngày"),
        _slot("sentence", 2, [_url(TN_AV_1)], "THANH NIÊN", "Ánh Viên lĩnh ấn tiên phong giúp Quân đội phá sâu kỷ lục tiếp sức nữ 4x200 mét"),
        _slot("sentence", 2, [_url(TT_PTB_1)], "TUỔI TRẺ", "Phạm Thanh Bảo giành HCV 100 mét ếch nam và phá kỷ lục quốc gia của chính mình"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url(VNE_YORO_1)], "VNEXPRESS / AP", "Manchester United quyết định kháng cáo chiếc thẻ đỏ sớm của trung vệ Leny Yoro"),
        _slot("sentence", 3, [_url(VNE_NEV_1)], "VNEXPRESS / SKY SPORTS", "Cựu đội trưởng Gary Neville hai lần tự tát vào mặt khi bình luận về Man United"),
        _slot("sentence", 3, [_url(VNE_BAY_1)], "VNEXPRESS / AFP", "Jamal Musiala giữa tâm bão tranh cãi đãi ngộ tại câu lạc bộ Bayern Munich"),
        _slot("sentence", 3, [_url(SKY_RAYA_1)], "SKY SPORTS", "Thủ thành David Raya tránh được phẫu thuật vai nhưng lỡ trận gặp Dortmund"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_url(TN_WWC_1)], "THANH NIÊN / REUTERS", "FIFA chính thức phê duyệt hai liên danh bốn quốc gia đăng cai World Cup nữ 2031 và 2035"),
        _slot("sentence", 4, [_url(TT_WTT_1)], "TUỔI TRẺ / WTT", "Bóng bàn Trung Quốc bất ngờ trắng tay ở cả năm trận chung kết tại Muscat"),
        _slot("sentence", 4, [_url(SKY_PEN_1)], "SKY SPORTS", "Tay golf Marco Penge thắng play-off nghẹt thở để giữ thẻ PGA Tour năm 2027"),
        _slot("sentence", 4, [_url(TT_LQL_1)], "TUỔI TRẺ / FIDE", "Kỳ thủ Lê Quang Liêm chuẩn bị tái ngộ đại kiện tướng Nga Ian Nepomniachtchi"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — U17 VIỆT NAM 3-3 NEW ZEALAND: DIỄN BIẾN TRẬN ĐẤU)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Việt Nam hòa nghẹt thở U17 New Zealand 3-3 với bàn gỡ phút bù giờ của Duy Khang",
        "summary": (
            "Đêm ngày 23 tháng 11 tại Qatar, đội tuyển U17 Việt Nam đã cống hiến một màn rượt đuổi tỷ số không tưởng để cầm hòa U17 New Zealand 3-3 ở lượt trận thứ hai bảng G U17 World Cup 2026. "
            "Dù ba lần bị đối thủ vượt lên dẫn trước nhờ các pha lập công của Jack Clegg ở phút 19, John Woldegiorgis ở phút 52 và Ethan Dyer ở phút 66, các học trò huấn luyện viên Cristiano Roland vẫn không hề nao núng. "
            "Lần lượt Chu Ngọc Nguyễn Lực sút phạt góc hẹp ghi bàn phút 49 và Lê Trọng Đại Nhân phá bẫy việt vị gỡ hòa phút 60 sau khi khiếu nại công nghệ FVS thành công. "
            "Đỉnh điểm vỡ òa đến ở phút bù giờ 90+2 khi Trương Nguyễn Duy Khang bay người đánh đầu dũng mãnh ấn định tỷ số 3-3, mang về điểm số đầu tiên trong lịch sử bóng đá 11 người Việt Nam tại một vòng chung kết World Cup."
        ),
        "source": "Thanh Niên / VnExpress / Dân Trí",
        "news_source": "THANH NIÊN / VNEXPRESS / DÂN TRÍ",
        "credit": "VNEXPRESS / DÂN TRÍ / VFF",
        "stat_badges": {
            "1": {"label": "LỊCH SỬ WORLD CUP", "value": "U17 VN 3-3 NZ", "sub": "Điểm số đầu tiên ở sân chơi 11 người"},
            "3": {"label": "NGUYỄN LỰC & ĐẠI NHÂN", "value": "49' • 60' (FVS)", "sub": "Hai lần san bằng cách biệt cực nhanh"},
            "4": {"label": "PHÚT BÙ GIỜ VÀNG", "value": "DUY KHANG 90+2'", "sub": "Đánh đầu quý giá giữ lại 1 điểm"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_U17_2)], "VNEXPRESS / VFF", "Khoảnh khắc Duy Khang đánh đầu gỡ hòa 3-3 phút 90+2 cho U17 Việt Nam"),
            _slot("title", 0, [_url(DT_U17_NL)], "DÂN TRÍ / VFF", "Chu Ngọc Nguyễn Lực ăn mừng bàn gỡ hòa 1-1 từ cú đá phạt trực tiếp táo bạo"),
            _slot("title", 0, [_url(VNE_U17_1)], "VNEXPRESS / VFF", "Các cầu thủ U17 Việt Nam vỡ òa khi trọng tài công nhận bàn thắng thứ hai qua FVS"),
            _slot("sentence", 1, [_url(TN_U17_TEAM)], "THANH NIÊN / VFF", "Đội hình xuất phát U17 Việt Nam bước vào trận then chốt gặp New Zealand tại Doha"),
            _slot("sentence", 2, [_url(DT_U17_NZ)], "DÂN TRÍ / FIFA", "U17 New Zealand tận dụng ưu thế thể hình để ba lần vươn lên dẫn trước"),
            _slot("sentence", 3, [_url(DT_U17_NL)], "DÂN TRÍ / VFF", "Nguyễn Lực ghi bàn thứ hai liên tiếp tại giải từ tình huống đá phạt góc hẹp"),
            _slot("sentence", 3, [_url(DT_U17_DN)], "DÂN TRÍ / VFF", "Đại Nhân lập công gỡ hòa 2-2 sau quyết định công nhận bàn thắng từ hệ thống FVS"),
            _slot("sentence", 4, [_url(DT_U17_DK)], "DÂN TRÍ / VFF", "Duy Khang đánh đầu tung lưới đối phương trong niềm hân hoan của toàn đội"),
            _slot("sentence", 4, [_url(VNE_U17_3)], "VNEXPRESS / VFF", "Tuyển U17 Việt Nam tri ân khán giả nhà sau điểm số lịch sử tại Qatar"),
        ],
    },

    # 02 (Nữ — PHẢN ỨNG FIFA, BÁO CHÍ QUỐC TẾ & THƯỞNG NÓNG VFF)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "U17 WORLD CUP 2026",
        "title": "FIFA ca ngợi tinh thần không bỏ cuộc của U17 Việt Nam, VFF thưởng nóng 400 triệu đồng",
        "summary": (
            "Ngay sau trận hòa 3-3 đầy quả cảm trước U17 New Zealand, trang chủ FIFA cùng Liên đoàn Bóng đá châu Á đồng loạt đăng tải lời khen ngợi đặc biệt dành cho bản lĩnh không chấp nhận thất bại của U17 Việt Nam. "
            "FIFA thậm chí trích dẫn phát biểu của huấn luyện viên Cristiano Roland nhấn mạnh rằng các cầu thủ trẻ Việt Nam đã cho cả thế giới thấy chất lượng chuyên môn và ý chí chiến đấu phi thường. "
            "Đội trưởng U17 New Zealand cùng truyền thông Đông Nam Á cũng bày tỏ sự thán phục trước tinh thần thi đấu quật cường của đội bóng áo đỏ cho tới giây bù giờ cuối cùng. "
            "Ghi nhận cột mốc lịch sử này, Thường trực Liên đoàn Bóng đá Việt Nam đã gọi điện chúc mừng toàn đội và quyết định thưởng nóng ngay số tiền 400 triệu đồng."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / FIFA",
        "news_source": "THANH NIÊN / TUỔI TRẺ / FIFA",
        "credit": "THANH NIÊN / DÂN TRÍ / FIFA",
        "stat_badges": {
            "1": {"label": "TRANG CHỦ FIFA", "value": "KHÔNG BỎ CUỘC", "sub": "Ca ngợi bản lĩnh của U17 Việt Nam"},
            "4": {"label": "VFF ĐỘNG VIÊN", "value": "THƯỞNG 400 TRIỆU", "sub": "Ghi nhận điểm số lịch sử World Cup"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_U17_FIFA)], "THANH NIÊN / FIFA", "U17 Việt Nam nhận sự tán dương lớn từ FIFA và người hâm mộ sau trận hòa 3-3"),
            _slot("title", 0, [_url(TN_U17_ROL)], "THANH NIÊN / FIFA", "Huấn luyện viên Cristiano Roland được trang chủ FIFA trích dẫn lời khen học trò"),
            _slot("title", 0, [_url(TT_U17_FIFA)], "TUỔI TRẺ / FIFA", "Dòng trạng thái đặc biệt của FIFA tôn vinh bàn thắng và ý chí của tuyển trẻ Việt Nam"),
            _slot("sentence", 1, [_url(TT_U17_FIFA)], "TUỔI TRẺ / FIFA", "Cả FIFA lẫn Liên đoàn Bóng đá châu Á đều ấn tượng với màn ngược dòng ba lần"),
            _slot("sentence", 2, [_url(DT_U17_ROL1)], "DÂN TRÍ / VFF", "Ông Cristiano Roland tự hào vì học trò đã chứng minh năng lực trước bạn bè quốc tế"),
            _slot("sentence", 3, [_url(DT_U17_CDV)], "DÂN TRÍ / VFF", "Cổ động viên và truyền thông khu vực dõi theo từng bước chạy của U17 Việt Nam"),
            _slot("sentence", 4, [_url(DT_U17_ROL2)], "DÂN TRÍ / VFF", "Thường trực VFF thưởng nóng 400 triệu đồng tiếp thêm động lực cho toàn đội"),
        ],
    },

    # 03 (Nam — CỤC DIỆN BẢNG G & KỊCH BẢN ĐẤU MALI)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "U17 WORLD CUP 2026",
        "title": "Cục diện bảng G và cánh cửa đi tiếp của U17 Việt Nam trước đại chiến U17 Mali",
        "summary": (
            "Ở trận đấu cùng giờ tại bảng G tối ngày 23 tháng 11, đại diện Tây Phi là U17 Mali đã xuất sắc lội ngược dòng đánh bại á quân châu Âu U17 Bỉ với tỷ số 2-1 nhờ hai bàn thắng của Djigui Koita và Yaya Niang. "
            "Kết quả này giúp U17 Mali chắc chắn giành ngôi nhất bảng với sáu điểm tuyệt đối sau hai lượt trận, còn U17 Bỉ xếp thứ hai với ba điểm. "
            "Với một điểm đầu tiên cùng hiệu số bàn thắng bại âm 1, tốt hơn âm 3 của U17 New Zealand, đội tuyển U17 Việt Nam tạm chiếm vị trí thứ ba bảng G và đứng thứ tám trên bảng xếp hạng các đội hạng ba xuất sắc nhất. "
            "Thầy trò huấn luyện viên Cristiano Roland vẫn còn nguyên cơ hội tự quyết vé vào vòng 32 đội nếu đánh bại đối thủ mạnh U17 Mali ở lượt trận cuối lúc 20 giờ ngày 26 tháng 11."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "credit": "TUỔI TRẺ / VNEXPRESS / THANH NIÊN",
        "stat_badges": {
            "1": {"label": "BẢNG G LƯỢT 2", "value": "MALI 2-1 BỈ", "sub": "Mali đạt 6 điểm sớm nhất bảng"},
            "3": {"label": "XẾP HẠNG TẠM", "value": "TOP 8 HẠNG BA", "sub": "Việt Nam 1 điểm (HS -1) xếp trên NZ"},
            "4": {"label": "TRẬN QUYẾT ĐỊNH", "value": "20H NGÀY 26/11", "sub": "U17 Việt Nam đối đầu U17 Mali"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_U17_MALI)], "TUỔI TRẺ / FIFA", "U17 Mali ngược dòng thắng U17 Bỉ 2-1 để sớm đoạt vé vào vòng 32 đội"),
            _slot("title", 0, [_url(VNE_U17_4)], "VNEXPRESS / ĐOÀN CA", "Nguyễn Lực và đồng đội giữ lại hy vọng vượt qua vòng bảng U17 World Cup"),
            _slot("sentence", 1, [_url(TT_U17_MALI)], "TUỔI TRẺ / FIFA", "Bàn thắng phút 67 của Yaya Niang giúp U17 Mali hoàn tất màn lội ngược dòng"),
            _slot("sentence", 2, [_url(TN_U17_VFF4)], "THANH NIÊN / VFF", "Việc Mali đã chắc ngôi đầu có thể giúp đội bóng châu Phi tính toán xoay vòng nhân sự"),
            _slot("sentence", 3, [_url(TN_U17_NL2)], "THANH NIÊN / VFF", "U17 Việt Nam tạm đứng thứ ba bảng G và nằm trong nhóm tám đội hạng ba đi tiếp"),
            _slot("sentence", 4, [_url(TN_U17_HANG)], "THANH NIÊN / VFF", "Toàn đội quyết tâm khắc phục sai sót phòng ngự trước cuộc chạm trán Mali ngày 26 tháng 11"),
        ],
    },

    # 04 (Nữ — NGUYỄN THÚY HIỀN 5 HCV PHÁ 5 KỶ LỤC)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Kình ngư 17 tuổi Nguyễn Thúy Hiền giành năm HCV và phá năm kỷ lục tại Đại hội Toàn quốc",
        "summary": (
            "Đường đua xanh Đại hội Thể thao toàn quốc 2026 chứng kiến sự thống trị rực rỡ của tài năng 17 tuổi Nguyễn Thúy Hiền thuộc đoàn Quân đội chỉ sau hai ngày thi đấu. "
            "Tối ngày 23 tháng 11 tại hồ bơi Phú Thọ, cô gái sinh năm 2009 xuất sắc về nhất cự ly 50 mét tự do nữ với thông số 25,85 giây, xô đổ kỷ lục đại hội tồn tại suốt 12 năm của đàn chị Ánh Viên. "
            "Chỉ mười phút sau, Thúy Hiền tiếp tục chiến thắng ở nội dung 100 mét ếch nữ với thành tích 1 phút 10,24 giây, phá cả kỷ lục đại hội lẫn kỷ lục quốc gia trước khi hoàn tất cú hat-trick vàng trong ngày ở nội dung tiếp sức. "
            "Với bốn huy chương vàng cá nhân và một huy chương vàng đồng đội đều gắn liền với năm kỷ lục mới, Nguyễn Thúy Hiền đang là vận động viên giàu thành tích nhất Đại hội năm nay."
        ),
        "source": "VnExpress / Thanh Niên",
        "news_source": "VNEXPRESS / THANH NIÊN",
        "credit": "THANH NIÊN / ĐỘC LẬP",
        "stat_badges": {
            "2": {"label": "50M TỰ DO NỮ", "value": "25,85 GIÂY", "sub": "Phá kỷ lục 2014 của Ánh Viên"},
            "3": {"label": "100M ẾCH NỮ", "value": "1 PHÚT 10,24", "sub": "Phá cả KL Đại hội lẫn KL Quốc gia"},
            "4": {"label": "THỐNG TRỊ ĐƯỜNG BƠI", "value": "5 HCV • 5 KỶ LỤC", "sub": "Chỉ sau 2 ngày tranh tài đầu tiên"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_BOI_TH)], "THANH NIÊN / ĐỘC LẬP", "Kình ngư 17 tuổi Nguyễn Thúy Hiền thi đấu bùng nổ tại hồ bơi Phú Thọ"),
            _slot("title", 0, [_url(VNE_BOI_1)], "VNEXPRESS", "Các đường bơi chung kết Đại hội Thể thao toàn quốc 2026 diễn ra đầy sôi động"),
            _slot("sentence", 1, [_url(TN_BOI_TH)], "THANH NIÊN / ĐỘC LẬP", "Nguyễn Thúy Hiền giúp đoàn Quân đội dẫn đầu bảng tổng sắp môn bơi lội"),
            _slot("sentence", 2, [_url(TN_BOI_TH2)], "THANH NIÊN / ĐỘC LẬP", "Thành tích 25,85 giây giúp cô vượt qua cột mốc lâu năm của đàn chị Ánh Viên"),
            _slot("sentence", 3, [_url(VNE_BOI_1)], "VNEXPRESS", "Chỉ cách mười phút, Thúy Hiền lại phá kỷ lục quốc gia cự ly 100 mét ếch nữ"),
            _slot("sentence", 4, [_url(TN_BOI_TH)], "THANH NIÊN / ĐỘC LẬP", "Năm huy chương vàng kèm năm kỷ lục khẳng định vị thế ngôi sao trẻ số một đường đua xanh"),
        ],
    },

    # 05 (Nam — NGUYỄN THỊ ÁNH VIÊN HCV ĐẦU TIÊN SAU 1437 NGÀY)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Nguyễn Thị Ánh Viên giành HCV đầu tiên sau 1437 ngày tuyên bố giải nghệ",
        "summary": (
            "Sau tấm huy chương bạc cá nhân trong ngày mở màn, tượng đài bơi lội Nguyễn Thị Ánh Viên đã chính thức bước lên bục cao nhất tại Đại hội Thể thao toàn quốc 2026 vào tối ngày 23 tháng 11. "
            "Lĩnh ấn tiên phong ở lượt bơi đầu tiên nội dung tiếp sức 4x200 mét tự do nữ, Ánh Viên nhanh chóng tạo khoảng cách an toàn cho đội Quân đội trước các đối thủ cạnh tranh từ Thành phố Hồ Chí Minh, Đà Nẵng và Hà Nội. "
            "Cùng các đồng đội Tú Uyên, Thúy An và Nguyễn Thúy Hiền giữ vững ưu thế đến khi chạm đích, đội Quân đội giành huy chương vàng với thành tích 8 phút 22,28 giây, phá kỷ lục đại hội cũ tới 12,22 giây. "
            "Khoảnh khắc đăng quang ở tuổi 30 đánh dấu đúng 1437 ngày kể từ lần cuối Ánh Viên giành huy chương vàng đại hội hồi tháng 12 năm 2022."
        ),
        "source": "Tuổi Trẻ / Thanh Niên / Dân Trí",
        "news_source": "TUỔI TRẺ / THANH NIÊN",
        "credit": "TUỔI TRẺ / THANH NIÊN",
        "stat_badges": {
            "2": {"label": "TIẾP SỨC 4X200M NỮ", "value": "8 PHÚT 22,28", "sub": "Phá kỷ lục Đại hội tới 12,22 giây"},
            "4": {"label": "CỘT MỐC TRỞ LẠI", "value": "1437 NGÀY", "sub": "Tấm HCV đầu tiên từ tháng 12/2022"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_AV_1)], "TUỔI TRẺ / THANH ĐỊNH", "Nụ cười rạng rỡ của Nguyễn Thị Ánh Viên trên bục nhận HCV tiếp sức tối 23 tháng 11"),
            _slot("title", 0, [_url(TN_AV_1)], "THANH NIÊN / ĐỘC LẬP", "Ánh Viên cùng đàn em đội Quân đội ăn mừng kỷ lục mới nội dung 4x200 mét tự do nữ"),
            _slot("title", 0, [_url(TT_AV_2)], "TUỔI TRẺ / THANH ĐỊNH", "Ánh Viên bơi lượt đầu tiên xuất sắc tạo lợi thế cho đội tiếp sức Quân đội"),
            _slot("sentence", 1, [_url(TN_AV_CDV)], "THANH NIÊN", "Ánh Viên nhận sự cổ vũ nồng nhiệt từ người hâm mộ tại hồ bơi Phú Thọ"),
            _slot("sentence", 2, [_url(TT_AV_2)], "TUỔI TRẺ / THANH ĐỊNH", "Cú xuất phát mạnh mẽ của cựu tuyển thủ quốc gia giúp Quân đội sớm dẫn đầu"),
            _slot("sentence", 3, [_url(TN_AV_1)], "THANH NIÊN / ĐỘC LẬP", "Hai thế hệ kình ngư Quân đội cùng nhau xô đổ kỷ lục đại hội hơn mười hai giây"),
            _slot("sentence", 4, [_url(TT_AV_1)], "TUỔI TRẺ / THANH ĐỊNH", "Tấm HCV sau gần bốn năm rời đỉnh cao mang lại nhiều cảm xúc cho người hâm mộ"),
        ],
    },

    # 06 (Nữ — PHẠM THANH BẢO PHÁ KỶ LỤC QUỐC GIA 100M ẾCH)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Phạm Thanh Bảo giành HCV bơi ếch 100 mét nam và phá sâu kỷ lục quốc gia",
        "summary": (
            "Chỉ một ngày sau thất bại sít sao trước kình ngư Việt kiều Watson Nguyễn ở cự ly 50 mét ếch, hoàng tử ếch Phạm Thanh Bảo đã có màn đáp trả đanh thép vào tối ngày 23 tháng 11. "
            "Xuất phát ở làn bơi số bốn chung kết 100 mét ếch nam, đại diện đoàn Vĩnh Long bứt tốc mạnh mẽ từ nửa sau đường đua để chạm đích đầu tiên với thông số 1 phút 00,47 giây. "
            "Thành tích ấn tượng bỏ xa người về nhì Tạ Minh Hiếu tới 3,48 giây, đồng thời giúp Phạm Thanh Bảo phá sâu kỷ lục quốc gia 1 phút 00,85 giây do chính anh thiết lập tại Asiad 20 cách đây hai tháng. "
            "Ngoài ra, thông số mới cũng xô đổ luôn kỷ lục Đại hội Thể thao toàn quốc cũ là 1 phút 01,76 giây."
        ),
        "source": "Tuổi Trẻ / Thanh Niên",
        "news_source": "TUỔI TRẺ / THANH NIÊN",
        "credit": "TUỔI TRẺ / THANH ĐỊNH",
        "stat_badges": {
            "2": {"label": "100M ẾCH NAM", "value": "1 PHÚT 00,47", "sub": "Vượt á quân Tạ Minh Hiếu 3,48 giây"},
            "3": {"label": "KỶ LỤC QUỐC GIA", "value": "RÚT NGẮN 0,38S", "sub": "Phá kỷ lục cũ lập tại Asiad 20"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_PTB_1)], "TUỔI TRẺ / THANH ĐỊNH", "Phạm Thanh Bảo bứt phá ngoạn mục trên đường bơi 100 mét ếch nam tối 23 tháng 11"),
            _slot("title", 0, [_url(TT_PTB_2)], "TUỔI TRẺ / THANH ĐỊNH", "Hoàng tử ếch Vĩnh Long khẳng định vị thế thống trị ở cự ly 100 mét sở trường"),
            _slot("sentence", 1, [_url(TT_PTB_2)], "TUỔI TRẺ / THANH ĐỊNH", "Thanh Bảo lấy lại phong độ cao nhất ngay sau cuộc so tài với Watson Nguyễn"),
            _slot("sentence", 2, [_url(TT_PTB_1)], "TUỔI TRẺ / THANH ĐỊNH", "Anh chạm đích sau 1 phút 00,47 giây và bỏ xa hoàn toàn nhóm bám đuổi"),
            _slot("sentence", 3, [_url(TT_PTB_2)], "TUỔI TRẺ / THANH ĐỊNH", "Thông số mới vượt xa kỷ lục quốc gia anh từng lập tại Nhật Bản hồi tháng chín"),
            _slot("sentence", 4, [_url(TT_PTB_1)], "TUỔI TRẺ / THANH ĐỊNH", "Chiến thắng kép vừa mang về HCV vừa ghi dấu cột mốc mới cho bơi lội Vĩnh Long"),
        ],
    },

    # 07 (Nam — BẢNG XẾP HẠNG HUY CHƯƠNG ĐẠI HỘI NGÀY 23/11)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Bảng xếp hạng Đại hội Toàn quốc ngày 23 tháng 11: Thành phố Hồ Chí Minh bỏ xa Hà Nội 16 HCV",
        "summary": (
            "Kết thúc ngày thi đấu 23 tháng 11, đoàn chủ nhà Thành phố Hồ Chí Minh tiếp tục bứt tốc mạnh mẽ trên bảng tổng sắp huy chương Đại hội Thể thao toàn quốc 2026 khi giành thêm 13 huy chương vàng. "
            "Thành tích mới nâng tổng số huy chương của đoàn dẫn đầu lên 54 vàng, 35 bạc và 52 đồng, trong đó nổi bật là tấm huy chương vàng 50 mét tự do nam của Lương Jeremie Loic Nino với 22,84 giây. "
            "Đoàn Hà Nội giữ vững vị trí thứ hai với 38 huy chương vàng nhưng đã bị đối thủ nới rộng khoảng cách từ bảy lên thành 16 huy chương vàng chỉ sau một ngày. "
            "Ở nhóm bám đuổi, Quân đội tăng tốc lên 26 huy chương vàng nhờ sự tỏa sáng của đội bơi cùng chiến thắng 1500 mét tự do của Nguyễn Huy Hoàng cho Quảng Trị, thu hẹp cách biệt xuống còn đúng một vàng so với đoàn Công an Nhân dân."
        ),
        "source": "Tuổi Trẻ / Dân Trí",
        "news_source": "TUỔI TRẺ / DÂN TRÍ",
        "credit": "TUỔI TRẺ / DÂN TRÍ",
        "stat_badges": {
            "2": {"label": "DẪN ĐẦU TOÀN ĐOÀN", "value": "TP.HCM 54 HCV", "sub": "Tổng cộng 141 huy chương các loại"},
            "3": {"label": "KHOẢNG CÁCH", "value": "HƠN HÀ NỘI 16 HCV", "sub": "Hà Nội 38 HCV • Quân đội 26 HCV"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_NINO_1)], "TUỔI TRẺ / THANH ĐỊNH", "Lương Jeremie Loic Nino mang về HCV bơi 50m tự do nam cho đoàn Thành phố Hồ Chí Minh"),
            _slot("title", 0, [_url(DT_HH_1)], "DÂN TRÍ / TIẾN TUẤN", "Nguyễn Huy Hoàng giành HCV sở trường 1500 mét tự do nam trong ngày 23 tháng 11"),
            _slot("sentence", 1, [_url(TT_NINO_1)], "TUỔI TRẺ / THANH ĐỊNH", "Đoàn chủ nhà bội thu thêm 13 HCV để củng cố vững chắc ngôi đầu bảng tổng sắp"),
            _slot("sentence", 2, [_url(VNE_BOI_1)], "VNEXPRESS", "Các nội dung tốc độ trên đường bơi tiếp tục mang lại nhiều huy chương cho TP.HCM"),
            _slot("sentence", 3, [_url(TT_QV_1)], "TUỔI TRẺ / HTPF", "Khoảng cách giữa Thành phố Hồ Chí Minh và Hà Nội tăng gấp đôi sau ngày 23 tháng 11"),
            _slot("sentence", 4, [_url(DT_HH_1)], "DÂN TRÍ / TIẾN TUẤN", "Cuộc cạnh tranh vị trí thứ ba giữa Công an Nhân dân và Quân đội diễn ra gay cấn"),
        ],
    },

    # 08 (Nữ — BÓNG ĐÁ NỮ ĐẠI HỘI TOÀN QUỐC)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Bóng đá nữ Đại hội Toàn quốc: Thành phố Hồ Chí Minh hẹn Thái Nguyên ở chung kết",
        "summary": (
            "Lượt trận thứ hai môn bóng đá nữ Đại hội Thể thao toàn quốc 2026 tối ngày 23 tháng 11 tại sân Bà Rịa đã sớm xác định hai cái tên góp mặt ở trận tranh huy chương vàng. "
            "Chủ nhà Thành phố Hồ Chí Minh bị Ninh Bình dẫn trước trong hiệp một nhưng kịp bùng nổ ở hiệp hai nhờ cú đúp ấn tượng của K'Thủa để lội ngược dòng giành chiến thắng 2-1. "
            "Ở trận đấu cùng ngày, các cô gái Thái Nguyên cũng tái hiện kịch bản ngược dòng kịch tính trước Hà Nội khi Dương Thị Vân gỡ hòa và Ngọc Minh Chuyên ghi bàn quyết định 2-1 ngay phút bù giờ 90+1. "
            "Cùng có trọn vẹn sáu điểm sau hai lượt trận và hơn hai đội xếp sau sáu điểm, Thành phố Hồ Chí Minh và Thái Nguyên chắc chắn bước vào chung kết ngày 1 tháng 12."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / HCMWFC / THÁI NGUYÊN T&T",
        "stat_badges": {
            "2": {"label": "TP.HCM 2-1 NINH BÌNH", "value": "CÚ ĐÚP K'THỦA", "sub": "Chủ nhà ngược dòng trong hiệp hai"},
            "3": {"label": "THÁI NGUYÊN 2-1 HÀ NỘI", "value": "MINH CHUYÊN 90+1'", "sub": "Hai đội sớm hẹn nhau chung kết 1/12"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_KTHUA_1)], "TUỔI TRẺ / HCMWFC", "K'Thủa ăn mừng cú đúp bàn thắng giúp đội nữ Thành phố Hồ Chí Minh thắng Ninh Bình 2-1"),
            _slot("title", 0, [_url(TT_TN_HN_1)], "TUỔI TRẺ / THÁI NGUYÊN T&T", "Các cầu thủ Thái Nguyên lội ngược dòng ngoạn mục đánh bại Hà Nội ở phút bù giờ"),
            _slot("sentence", 1, [_url(TT_TN_HN_1)], "TUỔI TRẺ / THÁI NGUYÊN T&T", "Sân Bà Rịa chứng kiến hai cặp đấu giàu cảm xúc xác định sớm hai vé chung kết"),
            _slot("sentence", 2, [_url(TT_KTHUA_1)], "TUỔI TRẺ / HCMWFC", "Cú đúp hiệp hai của K'Thủa giúp thầy trò huấn luyện viên Đoàn Thị Kim Chi giữ mạch toàn thắng"),
            _slot("sentence", 3, [_url(TT_TN_HN_1)], "TUỔI TRẺ / THÁI NGUYÊN T&T", "Ngọc Minh Chuyên ghi bàn thắng vàng ở phút 90+1 mang về chiến thắng 2-1 cho Thái Nguyên"),
            _slot("sentence", 4, [_url(TT_KTHUA_1)], "TUỔI TRẺ / HCMWFC", "Hai đội đầu bảng sẽ gặp nhau ở trận tranh huy chương vàng ngày 1 tháng 12 tới"),
        ],
    },

    # 09 (Nam — SIÊU KINH ĐIỂN CỜ TƯỚNG ĐẠI HỘI)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Lại Lý Huynh và Nguyễn Minh Nhật Quang thắng siêu kinh điển cờ tướng Đại hội",
        "summary": (
            "Nội dung đôi nam cờ tiêu chuẩn môn cờ tướng tại Đại hội Thể thao toàn quốc ngày 23 tháng 11 thu hút sự chú ý đặc biệt với cuộc đối đầu đỉnh cao giữa đoàn Thành phố Hồ Chí Minh và Đồng Nai. "
            "Phía Thành phố Hồ Chí Minh sở hữu nhà vô địch thế giới Lại Lý Huynh kết hợp cùng Nguyễn Minh Nhật Quang, chạm trán cặp đặc cấp quốc tế đại sư Nguyễn Thành Bảo và đương kim kỳ vương Việt Nam Hà Văn Tiến. "
            "Trên bàn đầu tiên, dù phải cầm quân đen đi hậu trước đàn anh kỳ cựu Nguyễn Thành Bảo, Lại Lý Huynh vẫn thi đấu chắc chắn để giành kết quả hòa cân bằng. "
            "Bước ngoặt quyết định đến ở bàn còn lại khi Nguyễn Minh Nhật Quang tận dụng triệt để lợi thế đi tiên đánh bại kỳ vương Hà Văn Tiến, ấn định thắng lợi chung cuộc 1,5 - 0,5 cho Thành phố Hồ Chí Minh."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / BING",
        "stat_badges": {
            "2": {"label": "ĐÔI NAM TIÊU CHUẨN", "value": "TP.HCM 1,5 - 0,5", "sub": "Bốn danh thủ hàng đầu Việt Nam so tài"},
            "4": {"label": "BÀN QUYẾT ĐỊNH", "value": "NHẬT QUANG THẮNG", "sub": "Hạ đương kim kỳ vương Hà Văn Tiến"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_CT_1)], "TUỔI TRẺ", "Cuộc đấu trí cân não giữa bốn cao thủ Lại Lý Huynh, Thành Bảo, Nhật Quang và Hà Văn Tiến"),
            _slot("title", 0, [_ddgs("Lại Lý Huynh cờ tướng thi đấu")], "BING SEARCH", "Nhà vô địch Lại Lý Huynh giữ thế trận vững vàng khi cầm quân đen đi hậu"),
            _slot("sentence", 1, [_url(TT_CT_1)], "TUỔI TRẺ", "Cuộc chạm trán ở vòng bốn được xem là trận chung kết sớm của nội dung đôi nam"),
            _slot("sentence", 2, [_ddgs("Nguyễn Thành Bảo cờ tướng Việt Nam")], "BING SEARCH", "Bộ đôi Đồng Nai gồm Nguyễn Thành Bảo và Hà Văn Tiến nhập cuộc với quyết tâm cao"),
            _slot("sentence", 3, [_ddgs("Lại Lý Huynh cờ tướng Việt Nam")], "BING SEARCH", "Lại Lý Huynh chia điểm hợp lý trước kỳ thủ kỳ cựu Nguyễn Thành Bảo"),
            _slot("sentence", 4, [_url(TT_CT_1)], "TUỔI TRẺ", "Chiến thắng của Nguyễn Minh Nhật Quang trước Hà Văn Tiến định đoạt tỷ số cho TP.HCM"),
        ],
    },

    # 10 (Nữ — CHU VIỆT HOÀNG VÔ ĐỊCH POOL 9 BI ĐẠI HỘI)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Cựu tài xế taxi Chu Việt Hoàng vô địch pool 9 bi Đại hội Thể thao toàn quốc",
        "summary": (
            "Chiều ngày 23 tháng 11 tại nhà thi đấu Nguyễn Du, cơ thủ Chu Việt Hoàng của đoàn Bắc Ninh đã viết nên câu chuyện cổ tích đẹp nhất môn billiards Đại hội Thể thao toàn quốc 2026. "
            "Sau cú sốc lội ngược dòng đánh bại ngôi sao số một Việt Nam Dương Quốc Hoàng với tỷ số 9-8 ở vòng 16, Chu Việt Hoàng tiếp tục thể hiện phong độ ổn định để tiến thẳng vào chung kết. "
            "Dù bị Nguyễn Hoàng Phong của Đà Nẵng dẫn trước 2-1, cơ thủ từng có thời gian chạy xe taxi mưu sinh trước khi theo đuổi chuyên nghiệp đã ghi liền bốn ván thắng để lật ngược thế cờ và khép lại trận đấu với thắng lợi 9-6. "
            "Tấm huy chương vàng đầu tiên của môn billiards đại hội giúp Chu Việt Hoàng hoàn tất cú đúp danh hiệu lớn trong năm 2026 sau chức vô địch quốc gia pool 10 bi."
        ),
        "source": "Tuổi Trẻ / Thanh Niên",
        "news_source": "TUỔI TRẺ / THANH NIÊN",
        "credit": "TUỔI TRẺ / THANH NIÊN",
        "stat_badges": {
            "3": {"label": "CHUNG KẾT POOL 9 BI", "value": "VIỆT HOÀNG 9-6", "sub": "Vượt qua Hoàng Phong sau khi bị dẫn 1-2"},
            "4": {"label": "CÚ ĐÚP NĂM 2026", "value": "HCV ĐẦU TIÊN", "sub": "Sau chức VĐQG pool 10 bi"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_CVH_1)], "TUỔI TRẺ / ĐỨC PHONG", "Chu Việt Hoàng ăn mừng vỡ òa sau chiến thắng 9-6 ở chung kết pool 9 bi đơn nam"),
            _slot("title", 0, [_url(TT_CVH_3)], "TUỔI TRẺ / ĐỨC PHONG", "Cơ thủ Bắc Ninh rạng rỡ trên bục nhận HCV đầu tiên môn billiards đại hội"),
            _slot("sentence", 1, [_url(TN_CVH_1)], "THANH NIÊN", "Hành trình từ tài xế taxi đến nhà vô địch Đại hội của Chu Việt Hoàng gây xúc động"),
            _slot("sentence", 2, [_url(TT_CVH_2)], "TUỔI TRẺ / ĐỨC PHONG", "Trước trận chung kết, anh từng gây chấn động khi hạ Dương Quốc Hoàng 9-8"),
            _slot("sentence", 3, [_url(TT_CVH_1)], "TUỔI TRẺ / ĐỨC PHONG", "Chuỗi bốn ván thắng liên tiếp giúp Việt Hoàng lật ngược thế trận trước Hoàng Phong"),
            _slot("sentence", 4, [_url(TT_CVH_3)], "TUỔI TRẺ / ĐỨC PHONG", "Danh hiệu năm 2026 ghi nhận phần thưởng xứng đáng cho quyết định theo đuổi đam mê"),
        ],
    },

    # 11 (Nam — XE ĐẠP ĐẠI HỘI: LÊ NGỌC SƠN TÉ XE VẪN ĐOẠT VÀNG & NGUYỄN THỊ THẬT)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "ĐẠI HỘI TOÀN QUỐC 2026",
        "title": "Té xe giữa đường đua, cua-rơ Lê Ngọc Sơn vẫn giành HCV xe đạp cùng Nguyễn Thị Thật",
        "summary": (
            "Ngày khai màn môn xe đạp tại Đại hội Thể thao toàn quốc 2026 sáng ngày 23 tháng 11 chứng kiến màn thống trị tuyệt đối của đoàn An Giang ở cả hai nội dung tính điểm nam và nữ. "
            "Tại cự ly 41,52 kilômét tính điểm cá nhân nam, tay đua được mệnh danh thần núi Lê Ngọc Sơn bất ngờ vướng vào xe đối thủ và ngã xuống đường ở vòng thứ tư. "
            "Không hề nao núng, anh lập tức bật dậy nhặt xe, siết lại guồng chân bắt kịp nhóm đầu rồi bứt phá giành hàng loạt điểm số để đoạt huy chương vàng chung cuộc với 34 điểm. "
            "Ngay sau đó ở nội dung 27,58 kilômét tính điểm nữ, tay đua số một Việt Nam Nguyễn Thị Thật cũng dễ dàng thắng áp đảo với 36 điểm để hoàn tất ngày thi đấu hoàn hảo cho xe đạp An Giang."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / XE ĐẠP ONLINE",
        "stat_badges": {
            "2": {"label": "BIẾN CỐ VÒNG 4", "value": "LÊ NGỌC SƠN 34Đ", "sub": "Té xe vẫn bật dậy giành HCV tính điểm"},
            "4": {"label": "CỰ LY NỮ 27,58KM", "value": "NGUYỄN THỊ THẬT", "sub": "Thắng áp đảo với 36 điểm cho An Giang"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_XD_1)], "TUỔI TRẺ / XE ĐẠP ONLINE", "Khoảnh khắc cua-rơ Lê Ngọc Sơn gặp tai nạn té xe ở vòng thứ tư vẫn vùng dậy đua tiếp"),
            _slot("title", 0, [_url(TT_XD_2)], "TUỔI TRẺ / XE ĐẠP ONLINE", "Niềm vui chiến thắng của Lê Ngọc Sơn khi cán đích giành tấm HCV đầy quả cảm"),
            _slot("title", 0, [_url(TT_XD_3)], "TUỔI TRẺ / XE ĐẠP ONLINE", "Nguyễn Thị Thật vượt trội phần còn lại để giành HCV tính điểm cá nhân nữ"),
            _slot("sentence", 1, [_url(TT_XD_2)], "TUỔI TRẺ / XE ĐẠP ONLINE", "Đoàn xe đạp An Giang mở màn đại hội bằng cú đúp huy chương vàng thuyết phục"),
            _slot("sentence", 2, [_url(TT_XD_1)], "TUỔI TRẺ / XE ĐẠP ONLINE", "Pha va chạm ở vòng bốn tưởng chừng khiến Lê Ngọc Sơn lỡ cơ hội tranh huy chương"),
            _slot("sentence", 3, [_url(TT_XD_2)], "TUỔI TRẺ / XE ĐẠP ONLINE", "Nỗ lực bền bỉ giúp anh thu về 34 điểm vượt xa các đối thủ Đồng Nai và Hà Nội"),
            _slot("sentence", 4, [_url(TT_XD_3)], "TUỔI TRẺ / XE ĐẠP ONLINE", "Tay đua số một Việt Nam Nguyễn Thị Thật dễ dàng mang về thêm tấm HCV cho An Giang"),
        ],
    },

    # 12 (Nữ — CLB CAHN VS VISSEL KOBE TỐI NAY 24/11)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "AFC CHAMPIONS LEAGUE ELITE",
        "title": "Câu lạc bộ Công an Hà Nội sẵn sàng đại chiến đội đầu bảng Vissel Kobe tối nay tại Hàng Đẫy",
        "summary": (
            "Vào lúc 19 giờ 15 tối nay ngày 24 tháng 11 trên sân Hàng Đẫy, câu lạc bộ Công an Hà Nội bước vào thử thách cực đại trước đội đầu bảng Vissel Kobe tại lượt trận thứ năm AFC Champions League Elite. "
            "Đại diện V-League hiện chỉ có bốn điểm và xếp thứ 11 trên 16 đội sau lịch thi đấu dày đặc 15 trận từ đầu mùa khiến lực lượng bị bào mòn vì chấn thương. "
            "Ngược lại, nhà vô địch Nhật Bản đang thể hiện sức mạnh áp đảo với bốn trận toàn thắng tuyệt đối, dẫn đầu bảng với 12 điểm và được đánh giá rất cao về đẳng cấp. "
            "Dẫu rơi vào thế gọng kìm, huấn luyện viên Alexandre Polking cùng thủ thành Nguyễn Filip vẫn giữ tinh thần lạc quan, đặt mục tiêu chơi sòng phẳng để phá dớp chưa thắng các câu lạc bộ Nhật Bản."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / CLB CAHN / BING",
        "stat_badges": {
            "1": {"label": "HÀNG ĐẪY 19H15 HÔM NAY", "value": "CAHN VS VISSEL KOBE", "sub": "Lượt 5 AFC Champions League Elite"},
            "3": {"label": "ĐỐI THỦ NHẬT BẢN", "value": "12 ĐIỂM TOÀN THẮNG", "sub": "CAHN xếp hạng 11/16 với 4 điểm"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_CAHN_1)], "THANH NIÊN / CLB CAHN", "HLV Alexandre Polking và thủ môn Nguyễn Filip sẵn sàng trước trận tiếp Vissel Kobe"),
            _slot("title", 0, [_ddgs("Vissel Kobe AFC Champions League football")], "BING SEARCH", "Vissel Kobe hành quân tới Hà Nội với chuỗi bốn trận toàn thắng tại bảng A"),
            _slot("sentence", 1, [_url(TN_CAHN_1)], "THANH NIÊN / CLB CAHN", "Trận đấu tối 24 tháng 11 mang tính bản lề cho cơ hội lọt vào nhóm tám đội đi tiếp"),
            _slot("sentence", 2, [_ddgs("Cong An Ha Noi FC V-League football")], "BING SEARCH", "Đội bóng ngành công an đang chịu áp lực lớn từ mật độ thi đấu dày đặc ba đấu trường"),
            _slot("sentence", 3, [_ddgs("Vissel Kobe J-League football match")], "BING SEARCH", "Đại diện Nhật Bản dẫn đầu bảng tuyệt đối với 12 điểm và hiệu số dương năm"),
            _slot("sentence", 4, [_url(TN_CAHN_1)], "THANH NIÊN / CLB CAHN", "Thủ môn Nguyễn Filip khẳng định toàn đội sẽ chơi cống hiến để hướng tới chiến thắng"),
        ],
    },

    # 13 (Nam — NGUYỄN XUÂN SON LỌT TOP 30 QUẢ BÓNG VÀNG CHÂU Á 2026)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "BÓNG ĐÁ VIỆT NAM",
        "title": "Tiền đạo Nguyễn Xuân Son lọt danh sách đề cử Quả bóng vàng châu Á 2026 cùng Son Heung-min",
        "summary": (
            "Ngày 23 tháng 11, tạp chí Sports Weekly chính thức công bố danh sách 30 cầu thủ tranh giải thưởng Quả bóng vàng châu Á năm 2026 với sự góp mặt đầy tự hào của tiền đạo Nguyễn Xuân Son. "
            "Chân sút sinh năm 1997 là đại diện duy nhất của đội tuyển Việt Nam được vinh danh bên cạnh các ngôi sao đẳng cấp thế giới như Son Heung-min, Lee Kang-in hay Daichi Kamada. "
            "Đề cử danh giá ghi nhận một năm thi đấu bùng nổ của Xuân Son khi anh góp công lớn vào chức vô địch ASEAN Cup, đồng thời chia sẻ danh hiệu vua phá lưới Cúp Câu lạc bộ Đông Nam Á với bảy bàn sau năm trận. "
            "Cùng với Xuân Son, khu vực Đông Nam Á năm nay chỉ có thêm hai cái tên đang thi đấu tại Đức là Kevin Diks của Indonesia và Nicolas Mickelson của Thái Lan."
        ),
        "source": "Dân Trí",
        "news_source": "DÂN TRÍ",
        "credit": "DÂN TRÍ / MẠNH QUÂN / GETTY",
        "stat_badges": {
            "2": {"label": "TOP 30 CHÂU Á 2026", "value": "XUÂN SON ĐỀ CỬ", "sub": "Cầu thủ Việt Nam duy nhất góp mặt"},
            "3": {"label": "DẤU ẤN NỔI BẬT", "value": "VUA PHÁ LƯỚI", "sub": "7 bàn ở Cúp CLB ĐNA • Vô địch ASEAN Cup"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_XS_1)], "DÂN TRÍ / MẠNH QUÂN", "Tiền đạo Nguyễn Xuân Son được đề cử Quả bóng vàng châu Á 2026"),
            _slot("title", 0, [_url(DT_SON_1)], "DÂN TRÍ / GETTY", "Ngôi sao Hàn Quốc Son Heung-min từng 10 lần giành danh hiệu Quả bóng vàng châu Á"),
            _slot("sentence", 1, [_url(DT_XS_1)], "DÂN TRÍ / MẠNH QUÂN", "Tạp chí Sports Weekly điền tên Xuân Son vào nhóm 30 cầu thủ xuất sắc nhất châu lục"),
            _slot("sentence", 2, [_url(DT_SON_1)], "DÂN TRÍ / GETTY", "Chân sút Việt Nam đứng chung danh sách với hàng loạt trụ cột đang chơi tại châu Âu"),
            _slot("sentence", 3, [_url(DT_XS_1)], "DÂN TRÍ / MẠNH QUÂN", "Phong độ ghi bàn ấn tượng ở cấp đội tuyển lẫn câu lạc bộ giúp anh ghi điểm tuyệt đối"),
            _slot("sentence", 4, [_ddgs("Kevin Diks Borussia Monchengladbach football")], "BING SEARCH", "Đông Nam Á còn có sự góp mặt của hai tuyển thủ Kevin Diks và Nicolas Mickelson"),
        ],
    },

    # 14 (Nữ — LÊ QUANG LIÊM TÁI ĐẤU IAN NEPOMNIACHTCHI)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "CỜ VUA THẾ GIỚI",
        "title": "Lê Quang Liêm chuẩn bị tái đấu vua cờ nước Nga Ian Nepomniachtchi tại Jerusalem Masters",
        "summary": (
            "Chuyên trang cờ vua hàng đầu thế giới Chess.com vừa đưa tin nhấn mạnh màn chạm trán tâm điểm giữa đại kiện tướng Lê Quang Liêm và kỳ thủ số một nước Nga Ian Nepomniachtchi tại giải Jerusalem Masters vào ngày 25 tháng 11. "
            "Sức nóng của cặp đấu đến từ việc hai kỳ thủ vừa tạo nên màn so tài nghẹt thở tại Budapest ở giải Total Chess World Championship Tour cách đây ít ngày. "
            "Sau khi thua 6-14 ở ngày thi đấu đầu tiên, Lê Quang Liêm đã vùng lên thắng ngược 14-6 ở ngày thứ hai để cân bằng điểm số và chỉ chịu thua sát nút kỳ thủ hai lần á quân thế giới sau ván Armageddon kéo dài 55 nước. "
            "Phong độ thăng hoa trước đối thủ có Elo 2719 mở ra cơ hội vàng để kỳ thủ số một Việt Nam giành chiến thắng thuyết phục trong cuộc tái đấu ngày mai."
        ),
        "source": "Tuổi Trẻ / FIDE",
        "news_source": "TUỔI TRẺ / FIDE",
        "credit": "TUỔI TRẺ / FIDE",
        "stat_badges": {
            "1": {"label": "JERUSALEM MASTERS", "value": "QUANG LIÊM VS NEPO", "sub": "Tái đấu vào ngày 25 tháng 11"},
            "3": {"label": "MÀN RƯỢT ĐUỔI BUDAPEST", "value": "ARMAGEDDON 55 NƯỚC", "sub": "Quang Liêm thắng ngược 14-6 ngày hai"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_LQL_1)], "TUỔI TRẺ / FIDE", "Lê Quang Liêm và Ian Nepomniachtchi chuẩn bị có thêm màn đấu trí tại Jerusalem Masters"),
            _slot("title", 0, [_url(TT_LQL_2)], "TUỔI TRẺ / FIDE", "Hai đại kiện tướng từng cống hiến màn rượt đuổi kịch tính tại Budapest tuần trước"),
            _slot("sentence", 1, [_url(TT_LQL_1)], "TUỔI TRẺ / FIDE", "Chess.com dành nhiều chú ý cho cuộc đối đầu ngày 25 tháng 11 giữa hai kỳ thủ hàng đầu"),
            _slot("sentence", 2, [_url(TT_LQL_2)], "TUỔI TRẺ / FIDE", "Màn tái đấu diễn ra ngay sau trận phân định thứ bậc đầy kịch tính ở Hungary"),
            _slot("sentence", 3, [_url(TT_LQL_3)], "TUỔI TRẺ / FIDE", "Quang Liêm buộc tay cờ hàng đầu nước Nga phải giải quyết thắng thua bằng ván Armageddon"),
            _slot("sentence", 4, [_url(TT_LQL_1)], "TUỔI TRẺ / FIDE", "Giới chuyên môn đánh giá khoảng cách giữa Quang Liêm và nhóm siêu đại kiện tướng Nga đang thu hẹp"),
        ],
    },

    # 15 (Nam — NGOẠI HẠNG ANH: BRENTFORD 4-0 EVERTON)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "NGOẠI HẠNG ANH",
        "title": "Brentford đè bẹp Everton 4-0 trong đêm kỷ lục buồn của huấn luyện viên David Moyes",
        "summary": (
            "Trận đấu muộn vòng 11 Ngoại hạng Anh rạng sáng ngày 24 tháng 11 chứng kiến chiến thắng tưng bừng 4-0 của Brentford trước Everton trên sân Gtech Community. "
            "Tiền vệ Keane Lewis-Potter rực sáng với cú đúp chớp nhoáng ở các phút 23 và 25, trong đó pha mở tỷ số cũng đánh dấu bàn thắng thứ 300 của Brentford tại Ngoại hạng Anh. "
            "Khó khăn chồng chất cho đội khách khi đội trưởng James Tarkowski nhận thẻ đỏ trực tiếp đầu tiên trong sự nghiệp Ngoại hạng Anh ở phút 40, tạo điều kiện để Vitaly Janelt và Fábio Carvalho ghi thêm hai bàn thắng trong hiệp hai. "
            "Thất bại nặng nề biến trận đấu thứ 593 kỷ lục dẫn dắt Everton của huấn luyện viên David Moyes thành ác mộng, đồng thời đưa Brentford vươn lên vị trí thứ sáu."
        ),
        "source": "BBC Sport / Sky Sports / The Guardian",
        "news_source": "BBC SPORT / SKY SPORTS / GUARDIAN",
        "credit": "SKY SPORTS / BING",
        "stat_badges": {
            "2": {"label": "CÚ ĐÚP CHỚP NHOÁNG", "value": "LEWIS-POTTER 23' 25'", "sub": "Bàn thắng thứ 300 của Brentford ở NHA"},
            "3": {"label": "BƯỚC NGOẶT PHÚT 40", "value": "TARKOWSKI THẺ ĐỎ", "sub": "Thẻ đỏ NHA đầu tiên của đội trưởng Everton"},
            "4": {"label": "BRENTFORD 4-0 EVERTON", "value": "TRẬN THỨ 593 MOYES", "sub": "Brentford vượt Everton lên hạng sáu"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_BRE_1)], "SKY SPORTS", "Keane Lewis-Potter ăn mừng bàn thắng mở màn cho chiến thắng 4-0 của Brentford"),
            _slot("title", 0, [_ddgs("Brentford Everton Premier League Vitaly Janelt")], "BING SEARCH", "Vitaly Janelt lập siêu phẩm giúp Brentford nhấn chìm Everton thiếu người"),
            _slot("sentence", 1, [_url(SKY_BRE_1)], "SKY SPORTS", "Brentford hoàn toàn làm chủ thế trận trong trận cầu muộn vòng 11 Ngoại hạng Anh"),
            _slot("sentence", 2, [_ddgs("Keane Lewis-Potter Brentford Everton 2026")], "BING SEARCH", "Hai bàn thắng cách nhau hai phút của Lewis-Potter giúp đội chủ nhà định đoạt sớm cục diện"),
            _slot("sentence", 3, [_ddgs("James Tarkowski red card Everton Brentford")], "BING SEARCH", "Tấm thẻ đỏ trực tiếp của James Tarkowski ở phút 40 dập tắt hy vọng gỡ hòa của Everton"),
            _slot("sentence", 4, [_ddgs("David Moyes Everton manager 2026")], "BING SEARCH", "Huấn luyện viên David Moyes đón cột mốc 593 trận dẫn dắt Everton trong nỗi thất vọng"),
        ],
    },

    # 16 (Nữ — MAN UTD KHÁNG CÁO THẺ ĐỎ LENY YORO & GARY NEVILLE)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "NGOẠI HẠNG ANH",
        "title": "Manchester United kháng cáo thẻ đỏ Leny Yoro giữa cơn thịnh nộ của Gary Neville",
        "summary": (
            "Sau trận thảm bại 0-4 trước Liverpool khiến đội nhà giậm chân ở vị trí áp chót bảng xếp hạng, ban lãnh đạo Manchester United đã chính thức thông báo với Liên đoàn Bóng đá Anh về việc kháng cáo thẻ đỏ của Leny Yoro. "
            "Tân huấn luyện viên Mauricio Pochettino lập luận rằng tiền đạo Alexander Isak đã mất quyền kiểm soát bóng ở phút thứ tám và thủ môn Senne Lammens đủ khả năng băng ra làm chủ tình hình. "
            "Tuy nhiên, cựu trọng tài Ngoại hạng Anh Dermot Gallagher vẫn bảo vệ quyết định phạt thẻ đỏ trực tiếp của trọng tài trên sân vì lỗi ngăn cản cơ hội ghi bàn rõ rệt. "
            "Trên sóng truyền hình Sky Sports, cựu đội trưởng Gary Neville thậm chí gây sốc khi hai lần tự tát vào mặt để cảnh tỉnh thái độ thi đấu thiếu tập trung của các cầu thủ đàn em."
        ),
        "source": "VnExpress / Sky Sports / BBC Sport",
        "news_source": "VNEXPRESS / SKY SPORTS / BBC",
        "credit": "VNEXPRESS / SKY SPORTS / AP",
        "stat_badges": {
            "1": {"label": "ĐƠN LÊN FA", "value": "KHÁNG CÁO YORO", "sub": "Phản đối thẻ đỏ phút thứ 8 tại Anfield"},
            "4": {"label": "PHẢN ỨNG GÂY SỐT", "value": "NEVILLE TỰ TÁT MẶT", "sub": "Chỉ trích thái độ thi đấu của cầu thủ MU"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_YORO_1)], "VNEXPRESS / AP", "Tình huống Leny Yoro phạm lỗi với Alexander Isak dẫn tới thẻ đỏ trực tiếp phút thứ 8"),
            _slot("title", 0, [_url(VNE_NEV_1)], "VNEXPRESS / SKY SPORTS", "Cựu danh thủ Gary Neville hai lần tự tát vào mặt khi bình luận về Manchester United"),
            _slot("title", 0, [_url(SKY_YORO_1)], "SKY SPORTS", "Trung vệ trẻ người Pháp trở thành tâm điểm tranh cãi sau trận thua Liverpool 0-4"),
            _slot("sentence", 1, [_url(VNE_YORO_2)], "VNEXPRESS / AP", "Manchester United gửi hồ sơ lên FA hy vọng xóa án treo giò cho Leny Yoro"),
            _slot("sentence", 2, [_url(VNE_NEV_2)], "VNEXPRESS / AP", "Huấn luyện viên Mauricio Pochettino cho rằng trọng tài đã quá nặng tay ở Anfield"),
            _slot("sentence", 3, [_url(SKY_YORO_1)], "SKY SPORTS", "Cựu trọng tài Dermot Gallagher nhận định thẻ đỏ dành cho Yoro hoàn toàn có cơ sở"),
            _slot("sentence", 4, [_url(VNE_NEV_1)], "VNEXPRESS / SKY SPORTS", "Gary Neville không giấu nổi sự thất vọng trước sự sụp đổ tinh thần của đội bóng cũ"),
        ],
    },

    # 17 (Nam — DAVID RAYA THOÁT PHẪU THUẬT NHƯNG LỠ TRẬN DORTMUND)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "CHAMPIONS LEAGUE",
        "title": "Thủ môn David Raya thoát ca phẫu thuật nhưng lỡ đại chiến Arsenal gặp Borussia Dortmund",
        "summary": (
            "Huấn luyện viên Mikel Arteta vừa mang lại tin vui cho cổ động viên Arsenal khi xác nhận chấn thương vai của thủ môn số một David Raya không nghiêm trọng như lo ngại ban đầu. "
            "Người gác đền 31 tuổi dính chấn thương phải rời sân sớm trong trận hòa 2-2 với Newcastle cuối tuần qua, làm dấy lên nỗi lo anh phải nghỉ thi đấu dài hạn. "
            "Kết quả kiểm tra y tế chuyên sâu ngày 23 tháng 11 cho thấy David Raya không cần phải lên bàn mổ và có thể sớm trở lại tập luyện trong thời gian tới. "
            "Dù vậy, anh vẫn chắc chắn vắng mặt trong cuộc tiếp đón Borussia Dortmund tại lượt năm Champions League đêm nay 24 tháng 11, nhường khung gỗ cho Kepa Arrizabalaga hoặc Illan Meslier."
        ),
        "source": "BBC Sport / Sky Sports / The Guardian",
        "news_source": "BBC SPORT / SKY SPORTS / GUARDIAN",
        "credit": "SKY SPORTS / BING",
        "stat_badges": {
            "3": {"label": "TIN VUI PHÁO THỦ", "value": "RAYA KHÔNG CẦN MỔ", "sub": "Chấn thương vai nhẹ hơn dự đoán"},
            "4": {"label": "CHAMPIONS LEAGUE", "value": "ARSENAL VS DORTMUND", "sub": "Lượt 5 đêm nay tại sân Emirates"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_RAYA_1)], "SKY SPORTS", "Thủ thành David Raya dính chấn thương vai trong trận Arsenal hòa Newcastle cuối tuần qua"),
            _slot("title", 0, [_ddgs("Mikel Arteta Arsenal press conference Champions League")], "BING SEARCH", "HLV Mikel Arteta trấn an người hâm mộ về tình hình chấn thương của David Raya"),
            _slot("sentence", 1, [_url(SKY_RAYA_1)], "SKY SPORTS", "Đội ngũ y tế Arsenal xác nhận chấn thương của thủ môn Tây Ban Nha không quá nghiêm trọng"),
            _slot("sentence", 2, [_ddgs("David Raya Arsenal goalkeeper injury")], "BING SEARCH", "Khoảnh khắc Raya rời sân khiến cổ động viên Pháo thủ nín thở lo lắng"),
            _slot("sentence", 3, [_ddgs("Arsenal Emirates Stadium Champions League night")], "BING SEARCH", "Việc tránh được ca phẫu thuật giúp Arsenal bớt âu lo cho chặng đường dài mùa giải"),
            _slot("sentence", 4, [_ddgs("Kepa Arrizabalaga Arsenal goalkeeper")], "BING SEARCH", "Kepa Arrizabalaga sẵn sàng bắt chính trước Borussia Dortmund đêm 24 tháng 11"),
        ],
    },

    # 18 (Nữ — BAYERN MUNICH KHỦNG HOẢNG KÉP: KANE & MUSIALA)
    {
        "id": 18,
        "art_id": "art_18",
        "group": "BÓNG ĐÁ ĐỨC",
        "title": "Bayern Munich khủng hoảng kép khi mất Harry Kane ba tháng và tranh cãi quanh Jamal Musiala",
        "summary": (
            "Đội bóng số một nước Đức Bayern Munich đang trải qua tuần lễ sóng gió cả về nhân sự trên sân lẫn lùm xùm ứng xử bên ngoài hậu trường. "
            "Chân sút chủ lực Harry Kane vừa phải lên bàn phẫu thuật để nối lại dây chằng mắt cá chân sau trận hòa 1-1 với Cologne và dự kiến phải nghỉ thi đấu khoảng ba tháng đến đầu năm 2027. "
            "Không dừng lại ở đó, ban lãnh đạo Bayern gồm những nhân vật quyền lực như Uli Hoeness còn gây phẫn nộ khi công khai đặt dấu hỏi về mức đãi ngộ 27 triệu USD mỗi năm của Jamal Musiala. "
            "Phát ngôn này lập tức vấp phải sự chỉ trích dữ dội từ Hiệp hội Cầu thủ chuyên nghiệp quốc tế FIFPRO vì thiếu cảm thông trong lúc tiền vệ 23 tuổi đang điều trị chứng rối loạn thần kinh tái diễn."
        ),
        "source": "VnExpress / The Guardian",
        "news_source": "VNEXPRESS / THE GUARDIAN",
        "credit": "VNEXPRESS / AFP / AP / BING",
        "stat_badges": {
            "2": {"label": "TỔN THẤT HÀNG CÔNG", "value": "HARRY KANE NGHỈ 3 THÁNG", "sub": "Phẫu thuật dây chằng mắt cá chân"},
            "3": {"label": "BÃO DƯ LUẬN", "value": "MUSIALA 27 TRIỆU USD", "sub": "FIFPRO chỉ trích cách ứng xử của Bayern"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_BAY_1)], "VNEXPRESS / AFP", "HLV Vincent Kompany trao đổi cùng Jamal Musiala trước khi tung anh vào sân trận hòa Cologne"),
            _slot("title", 0, [_ddgs("Harry Kane Bayern Munich ankle injury Cologne")], "BING SEARCH", "Tiền đạo Harry Kane phải nghỉ thi đấu khoảng ba tháng sau ca phẫu thuật mắt cá"),
            _slot("title", 0, [_url(VNE_BAY_2)], "VNEXPRESS / AP", "Chủ tịch danh dự Uli Hoeness gây tranh cãi với phát ngôn nhắm vào hợp đồng Musiala"),
            _slot("sentence", 1, [_url(VNE_BAY_3)], "VNEXPRESS / AP", "Bayern Munich chịu sức ép nặng nề giữa cơn bão chấn thương và tranh cãi nội bộ"),
            _slot("sentence", 2, [_ddgs("Harry Kane Bayern Munich injured pitch")], "BING SEARCH", "Sự vắng mặt của chủ nhân Quả bóng vàng Harry Kane là đòn giáng mạnh vào tham vọng của Bayern"),
            _slot("sentence", 3, [_url(VNE_BAY_2)], "VNEXPRESS / AP", "Lãnh đạo cấp cao Bayern bị cho là thiếu tinh tế khi công khai soi xét thu nhập của cầu thủ"),
            _slot("sentence", 4, [_url(VNE_BAY_4)], "VNEXPRESS / REUTERS", "Hiệp hội cầu thủ FIFPRO lên tiếng bảo vệ Jamal Musiala trước áp lực từ ban lãnh đạo"),
        ],
    },

    # 19 (Nam — DIEGO SIMEONE PHÁ KỶ LỤC LA LIGA)
    {
        "id": 19,
        "art_id": "art_19",
        "group": "LA LIGA",
        "title": "Huấn luyện viên Diego Simeone phá kỷ lục 345 chiến thắng mọi thời đại tại La Liga",
        "summary": (
            "Chiến thắng thuyết phục 3-0 trên sân Getafe ở vòng đấu cuối tuần qua đã đưa huấn luyện viên Diego Simeone đi vào ngôi đền huyền thoại của giải vô địch Tây Ban Nha. "
            "Nhà cầm quân người Argentina chính thức chạm mốc 345 chiến thắng tại La Liga cùng Atletico Madrid, vượt qua kỷ lục cũ 344 trận do cố danh thủ và huấn luyện viên Luis Aragonés nắm giữ. "
            "Đáng nể hơn, Simeone chỉ cần 567 trận dẫn dắt một câu lạc bộ duy nhất để xác lập cột mốc lịch sử, ít hơn tới 189 trận so với hành trình qua tám đội bóng của ông Aragonés. "
            "Trong buổi họp báo ngày 23 tháng 11, Simeone cũng thẳng thắn đáp trả định kiến cho rằng ông chỉ biết phòng ngự khi khẳng định không đội bóng phòng thủ thuần túy nào có thể thắng tới 345 trận."
        ),
        "source": "BBC Sport / Atlético de Madrid",
        "news_source": "BBC SPORT / ATLETICO MADRID",
        "credit": "BING SEARCH",
        "stat_badges": {
            "2": {"label": "KỶ LỤC LA LIGA", "value": "345 CHIẾN THẮNG", "sub": "Vượt cột mốc 344 trận của Luis Aragonés"},
            "3": {"label": "HIỆU SUẤT ĐỈNH CAO", "value": "SAU 567 TRẬN", "sub": "Ít hơn kỷ lục cũ tới 189 trận đấu"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Diego Simeone Atletico Madrid touchline celebration")], "BING SEARCH", "HLV Diego Simeone trở thành nhà cầm quân thắng nhiều trận nhất lịch sử La Liga"),
            _slot("title", 0, [_ddgs("Atletico Madrid Getafe football match celebration")], "BING SEARCH", "Trận thắng 3-0 trước Getafe giúp Atletico Madrid ghi dấu ấn lịch sử cho Simeone"),
            _slot("sentence", 1, [_ddgs("Diego Simeone Atletico Madrid 2026")], "BING SEARCH", "Ba bàn thắng của Baena, Cardoso và Grimaldo đưa Simeone lên đỉnh cao kỷ lục"),
            _slot("sentence", 2, [_ddgs("Diego Simeone Atletico Madrid trophy")], "BING SEARCH", "Chiến lược gia 56 tuổi vượt qua tượng đài Luis Aragonés bằng tất cả lòng trung thành với Atletico"),
            _slot("sentence", 3, [_ddgs("Atletico Madrid team celebration La Liga")], "BING SEARCH", "Tỷ lệ thắng xấp xỉ 60 phần trăm sau 567 trận là minh chứng cho sự ổn định phi thường"),
            _slot("sentence", 4, [_ddgs("Diego Simeone press conference Atletico Madrid")], "BING SEARCH", "Ông Simeone phản pháo đanh thép những chỉ trích nhắm vào triết lý bóng đá của mình"),
        ],
    },

    # 20 (Nữ — U17 WORLD CUP: TÂY BAN NHA 15-0 FIJI & TRUNG QUỐC HÒA MA RỐC PHÚT 90+9)
    {
        "id": 20,
        "art_id": "art_20",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Tây Ban Nha thắng Fiji 15-0, U17 Trung Quốc đánh rơi chiến thắng ở phút 90+9",
        "summary": (
            "Loạt trận tối ngày 23 tháng 11 tại vòng bảng U17 World Cup 2026 chứng kiến nhiều kết quả cực kỳ chênh lệch lẫn những kịch bản đảo chiều khó tin. "
            "Ở trận thắng đậm nhất từ đầu giải, U17 Tây Ban Nha phô diễn sức mạnh hủy diệt khi đè bẹp U17 Fiji tới 15 bàn không gỡ, trong đó riêng chân sút Rafa Cruz ghi năm bàn thắng để sớm đưa đội nhà vào vòng 32 đội. "
            "Ngược lại ở bảng H, U17 Trung Quốc tạo bất ngờ lớn khi dẫn trước U17 Ma Rốc 2-0 nhờ cú đúp của Zhao Songyuan và giữ lợi thế suốt hơn một giờ thi đấu. "
            "Tuy nhiên, bước ngoặt phạt đền phút 64 cùng bàn gỡ cận thành của Rami Lougmani ở phút bù giờ thứ chín đã khiến đại diện Đông Á mất thắng lợi ngay trước ngưỡng cửa thiên đường."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / TUỔI TRẺ / FIFA",
        "stat_badges": {
            "2": {"label": "KỶ LỤC TỶ SỐ GIẢI", "value": "TÂY BAN NHA 15-0 FIJI", "sub": "Rafa Cruz ghi 5 bàn • Sớm vào vòng 32 đội"},
            "4": {"label": "BI KỊCH BẢNG H", "value": "TRUNG QUỐC 2-2 MA RỐC", "sub": "Mất 3 điểm ở phút bù giờ 90+9"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_U17_ESP)], "THANH NIÊN / FIFA", "U17 Tây Ban Nha hủy diệt U17 Fiji 15-0 để sớm giành vé đi tiếp tại World Cup"),
            _slot("title", 0, [_url(TN_U17_CHN)], "THANH NIÊN / FIFA", "U17 Trung Quốc đánh rơi chiến thắng đáng tiếc trước U17 Ma Rốc ở giây cuối"),
            _slot("sentence", 1, [_url(TN_U17_ESP)], "THANH NIÊN / FIFA", "Đêm 23 tháng 11 trên đất Qatar ghi nhận những diễn biến trái ngược giữa các bảng đấu"),
            _slot("sentence", 2, [_ddgs("Spain U17 national football team celebration")], "BING SEARCH", "Cơn mưa 15 bàn thắng vào lưới Fiji khẳng định sức mạnh ứng cử viên vô địch của Tây Ban Nha"),
            _slot("sentence", 3, [_url(TN_U17_CHN)], "THANH NIÊN / FIFA", "Zhao Songyuan ghi cả hai bàn giúp U17 Trung Quốc dẫn trước Ma Rốc 2-0 đến phút 64"),
            _slot("sentence", 4, [_url(TT_U17_CHN)], "TUỔI TRẺ / FIFA", "Pha lập công phút 90+9 của Ma Rốc khiến các cầu thủ Trung Quốc đổ gục xuống sân"),
        ],
    },

    # 21 (Nam — FIFA CHỐT CHỦ NHÀ WORLD CUP NỮ 2031 & 2035)
    {
        "id": 21,
        "art_id": "art_21",
        "group": "BÓNG ĐÁ THẾ GIỚI",
        "title": "FIFA chính thức phê duyệt hai liên danh bốn quốc gia đăng cai World Cup nữ 2031 và 2035",
        "summary": (
            "Tại Đại hội bất thường diễn ra ở Zurich ngày 23 tháng 11, tất cả 211 liên đoàn thành viên FIFA đã nhất trí thông qua hai hồ sơ đăng cai World Cup nữ năm 2031 và 2035. "
            "Theo đó, liên danh gồm Mỹ, Mexico, Costa Rica và Jamaica sẽ lần đầu tiên đưa ngày hội bóng đá nữ lớn nhất hành tinh tới bốn quốc gia cùng lúc vào năm 2031. "
            "Kỳ giải này cũng đánh dấu cột mốc lịch sử khi quy mô được mở rộng từ 32 lên thành 48 đội tuyển với tổng cộng 104 trận đấu, mở thêm nhiều cơ hội góp mặt cho đội tuyển nữ Việt Nam. "
            "Trong khi đó, World Cup nữ 2035 được trao cho bốn quốc gia thuộc Vương quốc Anh gồm Anh, Scotland, Xứ Wales và Bắc Ireland, đánh dấu lần đầu nước Anh đón cúp thế giới sau gần 70 năm."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / BBC Sport",
        "news_source": "THANH NIÊN / TUỔI TRẺ / BBC SPORT",
        "credit": "THANH NIÊN / TUỔI TRẺ / REUTERS",
        "stat_badges": {
            "2": {"label": "WORLD CUP NỮ 2031", "value": "MỸ • MEXICO • 4 NƯỚC", "sub": "Mở rộng kỷ lục lên 48 đội & 104 trận"},
            "4": {"label": "WORLD CUP NỮ 2035", "value": "VƯƠNG QUỐC ANH", "sub": "Anh, Scotland, Xứ Wales & Bắc Ireland"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_WWC_1)], "TUỔI TRẺ / AP", "Liên danh Mỹ, Mexico, Costa Rica và Jamaica chính thức giành quyền đăng cai World Cup nữ 2031"),
            _slot("title", 0, [_url(TN_WWC_1)], "THANH NIÊN / REUTERS", "Đại hội FIFA thông qua thể thức mở rộng 48 đội cho World Cup nữ từ năm 2031"),
            _slot("sentence", 1, [_url(TN_WWC_1)], "THANH NIÊN / REUTERS", "Cả 211 liên đoàn thành viên FIFA bỏ phiếu nhất trí tại phiên họp bất thường ở Thụy Sĩ"),
            _slot("sentence", 2, [_url(TT_WWC_1)], "TUỔI TRẺ / AP", "Châu Mỹ hợp lực tổ chức kỳ World Cup nữ có quy mô khán giả và doanh thu lớn chưa từng có"),
            _slot("sentence", 3, [_url(TN_WWC_2)], "THANH NIÊN / REUTERS", "Việc nâng số đội tham dự lên 48 mở rộng thêm cánh cửa lịch sử cho các đội bóng châu Á"),
            _slot("sentence", 4, [_ddgs("England women football Wembley Stadium crowd")], "BING SEARCH", "Vương quốc Anh lần đầu đồng tổ chức một kỳ World Cup bóng đá vào mùa hè năm 2035"),
        ],
    },

    # 22 (Nữ — TÀI LIỆU MẬT KẾ HOẠCH BÁN QUYỀN WORLD CUP 96 NĂM)
    {
        "id": 22,
        "art_id": "art_22",
        "group": "HẬU TRƯỜNG FIFA",
        "title": "Tài liệu mật phanh phui kế hoạch bán quyền thương mại World Cup 96 năm của Chủ tịch FIFA",
        "summary": (
            "Bên cạnh tin vui về các kỳ World Cup nữ, bóng đá thế giới ngày 23 tháng 11 chấn động trước loạt tài liệu nội bộ bị tờ The Guardian phanh phui về đề án FIFA Forward Enterprise. "
            "Hồ sơ cho thấy Chủ tịch Gianni Infantino cùng quỹ đầu tư Thrive Capital từng vạch ra kế hoạch chuyển giao toàn bộ quyền khai thác thương mại các kỳ World Cup vào một công ty con trị giá tới 20 tỷ USD. "
            "Đáng chú ý hơn, thỏa thuận dự kiến có thể khóa chặt quyền thương mại bóng đá thế giới qua các kỳ gia hạn lên tới tối đa 96 năm, kèm điều khoản thưởng năm phần trăm giá trị cho nhóm điều hành. "
            "Dù kế hoạch này đã bị hủy bỏ sau làn sóng phản ứng dữ dội từ các liên đoàn châu Âu, sự việc tiếp tục phủ bóng lên chiếc ghế của ông Infantino trước cuộc bầu cử nhiệm kỳ mới."
        ),
        "source": "The Guardian",
        "news_source": "THE GUARDIAN",
        "credit": "BING SEARCH",
        "stat_badges": {
            "2": {"label": "ĐỀ ÁN MẬT FIFA", "value": "TRỊ GIÁ 20 TỶ USD", "sub": "Chuyển giao quyền thương mại World Cup"},
            "3": {"label": "THỜI HẠN GÂY SỐC", "value": "TỐI ĐA 96 NĂM", "sub": "Thưởng 5% cho ban điều hành dự án"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Gianni Infantino FIFA president speech Zurich")], "BING SEARCH", "Chủ tịch FIFA Gianni Infantino đối mặt làn sóng chất vấn từ tài liệu mật của The Guardian"),
            _slot("title", 0, [_ddgs("FIFA headquarters building Zurich Switzerland")], "BING SEARCH", "Trụ sở Liên đoàn Bóng đá Thế giới tại Zurich trước thềm các cuộc tranh luận thương mại"),
            _slot("sentence", 1, [_ddgs("Gianni Infantino press conference FIFA")], "BING SEARCH", "Hồ sơ đánh giá rủi ro nội bộ phơi bày tham vọng tài chính gây tranh cãi của FIFA"),
            _slot("sentence", 2, [_ddgs("FIFA World Cup trophy gold stadium")], "BING SEARCH", "Đề án trị giá 20 tỷ USD nhắm vào nguồn thu khổng lồ của các kỳ World Cup tương lai"),
            _slot("sentence", 3, [_ddgs("Gianni Infantino FIFA congress")], "BING SEARCH", "Thời hạn khóa quyền khai thác tới gần một thế kỷ khiến dư luận bóng đá phẫn nộ"),
            _slot("sentence", 4, [_ddgs("UEFA FIFA football meeting Europe")], "BING SEARCH", "Các liên đoàn thành viên châu Âu từng phản đối quyết liệt buộc kế hoạch phải dừng lại"),
        ],
    },

    # 23 (Nam — HUYỀN THOẠI DUDU GEORGESCU QUA ĐỜI BÍ ẨN)
    {
        "id": 23,
        "art_id": "art_23",
        "group": "BÓNG ĐÁ THẾ GIỚI",
        "title": "Huyền thoại hai lần đoạt Chiếc giày vàng châu Âu Dudu Georgescu qua đời bí ẩn",
        "summary": (
            "Làng bóng đá Romania và châu Âu ngày 23 tháng 11 bàng hoàng trước thông tin cựu tiền đạo lừng danh Dudu Georgescu qua đời ở tuổi 76 tại Toronto, Canada với nhiều tình tiết nghi vấn. "
            "Theo nhân chứng địa phương, lực lượng chức năng phát hiện thi thể ông trong căn hộ cùng vết máu và một con dao, khiến cảnh sát phải phong tỏa hiện trường và thẩm vấn người vợ. "
            "Cơ quan cảnh sát Toronto xác nhận đã tiến hành khám nghiệm tử thi để xác định chính xác đây là vụ án mạng hay tự sát trước khi quyết định khởi tố hình sự. "
            "Thời đỉnh cao trong màu áo Dinamo Bucharest, ông Dudu Georgescu từng ghi kỷ lục 252 bàn thắng và hai lần giành Chiếc giày vàng châu Âu vào các năm 1975 và 1977."
        ),
        "source": "Tuổi Trẻ / ProTV Romania",
        "news_source": "TUỔI TRẺ / PROTV",
        "credit": "TUỔI TRẺ / ADEVARUL / UEFA",
        "stat_badges": {
            "1": {"label": "VĨNH BIỆT HUYỀN THOẠI", "value": "GEORGESCU 76 TUỔI", "sub": "Nghi vấn án mạng tại Toronto, Canada"},
            "4": {"label": "DI SẢN BẤT HỦ", "value": "2 CHIẾC GIÀY VÀNG", "sub": "252 bàn thắng tại giải VĐQG Romania"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_GEO_1)], "TUỔI TRẺ / ADEVARUL", "Chân dung huyền thoại bóng đá Romania Dudu Georgescu qua đời ở tuổi 76"),
            _slot("title", 0, [_url(TT_GEO_2)], "TUỔI TRẺ / UEFA", "Ông Dudu Georgescu thời đỉnh cao từng hai lần giành Chiếc giày vàng châu Âu"),
            _slot("sentence", 1, [_url(TT_GEO_1)], "TUỔI TRẺ / ADEVARUL", "Thông tin cái chết của cựu danh thủ tại Canada gây chấn động bóng đá Romania"),
            _slot("sentence", 2, [_ddgs("Toronto police crime scene apartment investigation")], "BING SEARCH", "Cảnh sát Toronto phong tỏa căn hộ để làm rõ nguyên nhân tử vong bất thường"),
            _slot("sentence", 3, [_url(TT_GEO_1)], "TUỔI TRẺ / ADEVARUL", "Kết quả khám nghiệm tử thi sẽ quyết định hướng điều tra hình sự của vụ án"),
            _slot("sentence", 4, [_url(TT_GEO_2)], "TUỔI TRẺ / UEFA", "Liên đoàn Bóng đá Romania đã tổ chức phút mặc niệm tưởng nhớ chân sút vĩ đại"),
        ],
    },

    # 24 (Nữ — GONZALO TAPIA & NGUY CƠ ÁN PHẠT CHỜ LIONEL MESSI)
    {
        "id": 24,
        "art_id": "art_24",
        "group": "BÓNG ĐÁ MỸ MLS",
        "title": "Gonzalo Tapia lên tiếng vụ bị Lionel Messi ném bóng vào mặt trước nguy cơ án phạt MLS",
        "summary": (
            "Tiền đạo Gonzalo Tapia của Columbus Crew vừa lên tiếng xoa dịu dư luận sau tình huống va chạm gây tranh cãi với siêu sao Lionel Messi ở trận play-off MLS hôm cuối tuần. "
            "Khi Tapia nhảy lên chắn ngang pha ném biên nhanh cuối hiệp một, thủ quân Inter Miami đã mất bình tĩnh ném thẳng trái bóng vào mặt đối thủ ở cự ly gần và chỉ nhận thẻ vàng. "
            "Dù tiền đạo 24 tuổi người Chile khẳng định anh không muốn làm lớn chuyện, huấn luyện viên trưởng Columbus Crew lại tỏ ra bức xúc và yêu cầu giải đấu phải xem xét lại băng hình. "
            "Theo truyền thông Nam Mỹ, Ủy ban Kỷ luật MLS hoàn toàn có thể ra án phạt nguội treo giò Messi trước trận lượt về sống còn vào ngày 27 tháng 11 sau khi Inter Miami đã thua 0-3 ở lượt đi."
        ),
        "source": "Dân Trí / TyC Sports",
        "news_source": "DÂN TRÍ / TYC SPORTS",
        "credit": "DÂN TRÍ / GETTY / BING",
        "stat_badges": {
            "2": {"label": "TRANH CÃI PLAY-OFF MLS", "value": "MESSI CHỈ THẺ VÀNG", "sub": "Ném bóng vào mặt Gonzalo Tapia"},
            "4": {"label": "LƯỢT VỀ 27/11", "value": "NGUY CƠ TREO GIÒ", "sub": "Inter Miami đang bị dẫn 0-3 ở lượt đi"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_MES_1)], "DÂN TRÍ / GETTY", "Lionel Messi nhận thẻ vàng sau pha ném bóng vào mặt tiền đạo Gonzalo Tapia"),
            _slot("title", 0, [_url(DT_MES_2)], "DÂN TRÍ / GETTY", "Siêu sao Argentina đứng trước nguy cơ nhận án phạt nguội từ Ủy ban Kỷ luật MLS"),
            _slot("sentence", 1, [_url(DT_MES_1)], "DÂN TRÍ / GETTY", "Gonzalo Tapia giữ thái độ điềm tĩnh khi được hỏi về va chạm trên sân"),
            _slot("sentence", 2, [_url(DT_MES_2)], "DÂN TRÍ / GETTY", "Pha xử lý nóng nảy của Messi ở phút bù giờ hiệp một không bị VAR phạt thẻ đỏ"),
            _slot("sentence", 3, [_ddgs("Columbus Crew soccer match stadium MLS")], "BING SEARCH", "Ban huấn luyện Columbus Crew không hài lòng khi đối thủ thoát án truất quyền thi đấu"),
            _slot("sentence", 4, [_url(DT_MES_2)], "DÂN TRÍ / GETTY", "Nếu Messi bị treo giò ngày 27 tháng 11, Inter Miami rất khó lật ngược thế thua 0-3"),
        ],
    },

    # 25 (Nam — JANNIK SINNER PHẪU THUẬT ĐẦU GỐI)
    {
        "id": 25,
        "art_id": "art_25",
        "group": "QUẦN VỢT ATP",
        "title": "Jannik Sinner phẫu thuật đầu gối tại Phần Lan, nguy cơ lỡ hẹn Australian Open 2027",
        "summary": (
            "Làng quần vợt thế giới đón nhận thông tin gây sốc ngày 23 tháng 11 khi cựu số một thế giới Jannik Sinner bay sang Phần Lan chuẩn bị lên bàn phẫu thuật đầu gối phải. "
            "Kể từ sau chức vô địch Wimbledon hồi tháng bảy, ngôi sao người Ý đã phải nghỉ thi đấu suốt cuối mùa giải vì hội chứng viêm gân dải chậu chày dai dẳng nhưng điều trị bảo tồn không hiệu quả. "
            "Ca phẫu thuật do bác sĩ hàng đầu Lasse Lempainen trực tiếp thực hiện dự kiến khiến Sinner phải mất từ ba đến bốn tháng để hồi phục hoàn toàn. "
            "Điều này đồng nghĩa tay vợt 25 tuổi đối mặt nguy cơ rất lớn phải bỏ lỡ Grand Slam đầu năm Australian Open vào tháng 1 năm 2027, mở toang đường thống trị cho Carlos Alcaraz."
        ),
        "source": "Sky Sports / Olympics",
        "news_source": "SKY SPORTS / OLYMPICS",
        "credit": "SKY SPORTS / BING",
        "stat_badges": {
            "2": {"label": "NGHỈ TỪ THÁNG 7", "value": "VIÊM GÂN ĐẦU GỐI", "sub": "Điều trị bảo tồn không đạt kết quả"},
            "3": {"label": "THỜI GIAN HỒI PHỤC", "value": "NGHỈ 3 ĐẾN 4 THÁNG", "sub": "Nguy cơ vắng mặt tại Australian Open"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_SIN_1)], "SKY SPORTS", "Jannik Sinner chuẩn bị sang Phần Lan phẫu thuật dứt điểm chấn thương đầu gối"),
            _slot("title", 0, [_ddgs("Jannik Sinner Wimbledon 2026 champion trophy")], "BING SEARCH", "Tay vợt người Ý chưa thể thi đấu thêm trận nào kể từ khi vô địch Wimbledon"),
            _slot("sentence", 1, [_url(SKY_SIN_1)], "SKY SPORTS", "Quyết định phẫu thuật chấm dứt hy vọng tái xuất cuối năm nay của Jannik Sinner"),
            _slot("sentence", 2, [_ddgs("Jannik Sinner tennis knee injury")], "BING SEARCH", "Chấn thương gân đầu gối dai dẳng đã buộc anh phải bỏ qua Mỹ mở rộng và ATP Finals"),
            _slot("sentence", 3, [_ddgs("Jannik Sinner tennis court practice")], "BING SEARCH", "Bác sĩ chuyên khoa Lasse Lempainen dự kiến cần ba đến bốn tháng theo dõi hậu phẫu"),
            _slot("sentence", 4, [_ddgs("Carlos Alcaraz Australian Open tennis")], "BING SEARCH", "Việc Sinner vắng mặt giúp Carlos Alcaraz trở thành ứng viên áp đảo tại Melbourne"),
        ],
    },

    # 26 (Nữ — TYSON FURY TIẾT LỘ TÂM THẦN PHÂN LIỆT)
    {
        "id": 26,
        "art_id": "art_26",
        "group": "QUYỀN ANH THẾ GIỚI",
        "title": "Tyson Fury lần đầu tiết lộ từng được chẩn đoán tâm thần phân liệt trước đại chiến Anthony Joshua",
        "summary": (
            "Trước thềm trận đại chiến toàn Anh lịch sử gặp Anthony Joshua vào ngày 11 tháng 12 tại Cardiff, cựu vô địch hạng nặng Tyson Fury bất ngờ tiết lộ góc khuất tâm lý gây rúng động. "
            "Chia sẻ trên truyền thông ngày 23 tháng 11, tay đấm người Anh lần đầu công khai rằng sau khi đánh bại Wladimir Klitschko năm 2015, anh từng bị chẩn đoán mắc chứng tâm thần phân liệt nhẹ cùng rối loạn lưỡng cực. "
            "Fury kể lại quãng thời gian đen tối năm 2016 khi anh liên tục nghe thấy những tiếng nói đe dọa trong đầu và phải nhập viện điều trị tâm thần sau cơn hoảng loạn dữ dội. "
            "Việc dũng cảm đối diện với căn bệnh tâm lý để trở lại đỉnh cao quyền Anh giúp Tyson Fury nhận được nhiều sự đồng cảm trước trận đấu lớn nhất sự nghiệp vào tháng tới."
        ),
        "source": "BBC Sport / CNN / BoxingScene",
        "news_source": "BBC SPORT / CNN",
        "credit": "BING SEARCH",
        "stat_badges": {
            "2": {"label": "TIẾT LỘ GÂY RÚNG ĐỘNG", "value": "TÂM THẦN PHÂN LIỆT", "sub": "Chẩn đoán cùng rối loạn lưỡng cực"},
            "4": {"label": "CARDIFF 11/12/2026", "value": "FURY VS JOSHUA", "sub": "Đại chiến hạng nặng tại Xứ Wales"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Tyson Fury boxing press conference 2026")], "BING SEARCH", "Tyson Fury lần đầu trải lòng về cuộc chiến chống lại căn bệnh tâm thần phân liệt"),
            _slot("title", 0, [_ddgs("Tyson Fury Anthony Joshua boxing face off")], "BING SEARCH", "Tiết lộ được đưa ra ngay trước thềm trận so găng thế kỷ với Anthony Joshua"),
            _slot("sentence", 1, [_ddgs("Tyson Fury boxing champion belt")], "BING SEARCH", "Trận đấu ngày 11 tháng 12 tại sân Principality thu hút sự chú ý toàn cầu"),
            _slot("sentence", 2, [_ddgs("Tyson Fury Wladimir Klitschko boxing")], "BING SEARCH", "Sau đỉnh cao năm 2015, Fury rơi vào khủng hoảng trầm cảm và lạm dụng chất kích thích"),
            _slot("sentence", 3, [_ddgs("Tyson Fury Paris Fury documentary")], "BING SEARCH", "Gia đình đóng vai trò điểm tựa giúp tay đấm Anh vượt qua cơn ác mộng tâm lý"),
            _slot("sentence", 4, [_ddgs("Tyson Fury boxing training ring")], "BING SEARCH", "Người hâm mộ kỳ vọng màn đối đầu giữa hai ngôi sao hạng nặng Anh sẽ bùng nổ tháng tới"),
        ],
    },

    # 27 (Nam — CÚ SỐC BÓNG BÀN TRUNG QUỐC Ở WTT MUSCAT)
    {
        "id": 27,
        "art_id": "art_27",
        "group": "BÓNG BÀN THẾ GIỚI",
        "title": "Bóng bàn Trung Quốc gây sốc khi cử 19 tay vợt dự WTT Muscat nhưng sạch bóng ở chung kết",
        "summary": (
            "Làng bóng bàn thế giới vừa chứng kiến cú sốc lớn tại giải WTT Star Contender Muscat 2026 tổng thưởng 300000 USD vừa khép lại ở Oman. "
            "Dù cử lực lượng đông đảo gồm 11 tay vợt nam, tám tay vợt nữ và tám cặp đánh đôi, cường quốc số một thế giới Trung Quốc lại không có nổi một đại diện vào chung kết ở cả năm nội dung. "
            "Niềm hy vọng cuối cùng là tay vợt 21 tuổi Trần Viên Vũ cũng gục ngã chóng vánh 0-3 trước Shunsuke Togami của Nhật Bản ở bán kết đơn nam, thậm chí chỉ ghi được ba điểm ở ván quyết định. "
            "Đây là giải thứ ba liên tiếp bóng bàn Trung Quốc trắng tay vé chung kết sau Frankfurt và Istanbul, nhìn Nhật Bản thâu tóm bốn trong năm ngôi vô địch."
        ),
        "source": "Tuổi Trẻ / Tân Hoa Xã",
        "news_source": "TUỔI TRẺ / TÂN HOA XÃ",
        "credit": "TUỔI TRẺ / WTT / BING",
        "stat_badges": {
            "2": {"label": "WTT MUSCAT 300000 USD", "value": "19 VĐV • 0 CHUNG KẾT", "sub": "Thất bại toàn diện ở cả 5 nội dung"},
            "4": {"label": "NHẬT BẢN ÁP ĐẢO", "value": "4/5 CHỨC VÔ ĐỊCH", "sub": "Giải thứ 3 liên tiếp Trung Quốc hụt chung kết"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_WTT_1)], "TUỔI TRẺ / WTT", "Tay vợt Trần Viên Vũ thua chóng vánh 0-3 ở bán kết đơn nam WTT Muscat"),
            _slot("title", 0, [_url(TT_WTT_2)], "TUỔI TRẺ / WTT", "Các tay vợt Nhật Bản áp đảo giải đấu ở Oman khi giành bốn trên năm danh hiệu"),
            _slot("sentence", 1, [_url(TT_WTT_1)], "TUỔI TRẺ / WTT", "Giải đấu 300000 USD tại Oman chứng kiến sự thống trị bất ngờ của các tay vợt Nhật Bản"),
            _slot("sentence", 2, [_ddgs("China table tennis team WTT tournament")], "BING SEARCH", "Cả 19 tay vợt và tám đôi vận động viên Trung Quốc đều dừng bước trước trận cuối cùng"),
            _slot("sentence", 3, [_ddgs("Shunsuke Togami table tennis WTT")], "BING SEARCH", "Shunsuke Togami thắng áp đảo Trần Viên Vũ trước khi vô địch đơn nam lẫn đôi nam nữ"),
            _slot("sentence", 4, [_url(TT_WTT_2)], "TUỔI TRẺ / WTT", "Chuỗi 12 chặng WTT không vô địch đơn nam đặt dấu hỏi lớn về lớp kế cận của Trung Quốc"),
        ],
    },

    # 28 (Nữ — GOLF MARCO PENGE VÔ ĐỊCH PGA TOUR RSM CLASSIC)
    {
        "id": 28,
        "art_id": "art_28",
        "group": "GOLF PGA TOUR",
        "title": "Marco Penge thắng play-off bốn người để vô địch PGA Tour RSM Classic và giữ thẻ 2027",
        "summary": (
            "Tay golf người Anh Marco Penge vừa tạo nên màn giải cứu sự nghiệp ngoạn mục tại giải hạ màn mùa giải PGA Tour RSM Classic ở bang Georgia, Mỹ. "
            "Bước vào giải với nguy cơ rớt hạng mất thẻ thi đấu sau một năm khốn đốn vì bệnh virus, tay golf 28 tuổi buộc phải nằm trong nhóm bốn người dẫn đầu mới giữ được suất dự mùa sau. "
            "Đánh xuất sắc 65 gậy ở vòng cuối để cân bằng tổng điểm âm 16 cùng Lý Hạo Đồng, Michael Thorbjornsen và Max Greyserman, Penge đưa cả bốn vào loạt đấu play-off cân não. "
            "Ngay ở hố phụ đầu tiên, anh gạt birdie chuẩn xác từ khoảng cách mười feet để đoạt danh hiệu PGA Tour đầu tiên sự nghiệp kèm tấm thẻ miễn trừ mùa giải 2027."
        ),
        "source": "Sky Sports / BBC Sport",
        "news_source": "SKY SPORTS / BBC SPORT",
        "credit": "SKY SPORTS / BING",
        "stat_badges": {
            "2": {"label": "ÁP LỰC GIỮ THẺ", "value": "BUỘC PHẢI TOP 4", "sub": "Vượt khủng hoảng bệnh virus trong năm 2026"},
            "4": {"label": "PLAY-OFF 4 NGƯỜI", "value": "BIRDIE HỐ PHỤ 18", "sub": "Danh hiệu PGA Tour đầu tiên sự nghiệp"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_PEN_1)], "SKY SPORTS", "Tay golf Marco Penge xuất sắc giành danh hiệu PGA Tour đầu tiên tại giải RSM Classic"),
            _slot("title", 0, [_ddgs("RSM Classic Sea Island Golf Club PGA Tour")], "BING SEARCH", "Sân golf Sea Island chứng kiến loạt play-off bốn tay golf đầy kịch tính"),
            _slot("sentence", 1, [_url(SKY_PEN_1)], "SKY SPORTS", "Chức vô địch hạ màn mùa giải mang ý nghĩa sống còn với sự nghiệp của tay golf người Anh"),
            _slot("sentence", 2, [_ddgs("Marco Penge golfer DP World Tour")], "BING SEARCH", "Từng ba lần vô địch DP World Tour nhưng Penge suýt mất thẻ PGA Tour vì ốm nặng"),
            _slot("sentence", 3, [_ddgs("golf playoff putting green PGA Tour")], "BING SEARCH", "Vòng cuối năm gậy âm giúp anh san bằng tổng điểm âm 16 với ba đối thủ nặng ký"),
            _slot("sentence", 4, [_url(SKY_PEN_1)], "SKY SPORTS", "Cú birdie quyết định ở hố phụ đầu tiên giúp Marco Penge chính thức trụ lại PGA Tour 2027"),
        ],
    },

    # 29 (100% Giọng Nữ — MỤC TIN VẮN CUỐI VIDEO: CÁC TIN THỂ THAO KHÁC)
    {
        "id": 29,
        "art_id": "art_29",
        "group": "CÁC TIN THỂ THAO KHÁC",
        "title": "Điểm nhanh các tin thể thao đáng chú ý khác",
        "voice_preset": "secondary",
        "summary": (
            "Tại Đại hội Thể thao toàn quốc 2026 ngày 23 tháng 11, tài năng cầu lông 15 tuổi Nguyễn Thị Thu Huyền xuất sắc vào bán kết đơn nữ để chắc chắn có huy chương, còn tuyển quần vợt Thành phố Hồ Chí Minh thắng Hà Nội 2-1 sau tám tiếng tranh tài đoạt huy chương vàng đồng đội nam. "
            "Trên sàn võ thuật, võ sĩ MMA 46 tuổi Chris Leben gây kinh ngạc khi lãnh trọn cú đá vào đầu đến mất trí nhớ tạm thời vẫn thắng điểm Yoshihiro Akiyama ở Seoul, Martin Bakole nhận lời thay Jai Opetaia đấu Deontay Wilder ở sự kiện Fury gặp Joshua, còn tay đấm James Gallagher tuyên bố giải nghệ ở tuổi 30. "
            "Ở môn golf nữ, Megha Ganne vô địch vòng loại cuối LPGA Q-Series trong khi ngôi sao năm lần dự Solheim Cup Megan Khang giành lại thẻ thi đấu năm 2027. "
            "Tại các giải bóng đá châu Âu, Sevilla cầm hòa kình địch Real Betis 1-1 nhờ bàn thắng phút bù giờ của Kike Salas, còn đội nữ Tottenham gây sốc đánh bại đương kim vô địch Manchester City 3-1 ở giải Ngoại hạng nữ Anh. "
            "Khép lại bản tin hôm nay, ngôi sao bầu dục Mỹ DK Metcalf thoát án treo giò dù bị truất quyền thi đấu trận Steelers thua Eagles 16-19, còn nhà vô địch F1 Max Verstappen bất ngờ chỉ trích chặng đua Las Vegas có quá nhiều pha vượt mặt nên không giống Công thức 1 thực thụ."
        ),
        "source": "Tuổi Trẻ / Sky Sports / BBC Sport / The Guardian",
        "news_source": "ĐIỂM ĐỌC TỔNG HỢP",
        "credit": "TUỔI TRẺ / SKY SPORTS / BING",
        "stat_badges": {
            "1": {"label": "ĐẠI HỘI 2026", "value": "THU HUYỀN 15 TUỔI", "sub": "Chắc chắn có HC cầu lông • TP.HCM vô địch quần vợt"},
            "2": {"label": "VÕ THUẬT THẾ GIỚI", "value": "CHRIS LEBEN 46 TUỔI", "sub": "Mất trí nhớ tạm thời vẫn thắng điểm ở Seoul"},
            "4": {"label": "BÓNG ĐÁ NỮ & LA LIGA", "value": "SPURS NỮ 3-1 MAN CITY", "sub": "Sevilla hòa Betis 1-1 phút bù giờ"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_TH_1)], "TUỔI TRẺ / ĐỨC KHUÊ", "Tài năng cầu lông 15 tuổi Nguyễn Thị Thu Huyền giành vé bán kết Đại hội Toàn quốc"),
            _slot("title", 0, [_url(TT_MMA_1)], "TUỔI TRẺ / UFC", "Võ sĩ MMA kỳ cựu Chris Leben tạo chiến thắng khó tin ở tuổi 46 tại Hàn Quốc"),
            _slot("title", 0, [_url(SKY_BAK_1)], "SKY SPORTS", "Martin Bakole nhận kèo đấu Deontay Wilder ở sự kiện quyền Anh ngày 11 tháng 12"),
            # Câu 1: Thu Huyền & Quần vợt TP.HCM
            _slot("sentence", 1, [_url(TT_TH_1)], "TUỔI TRẺ / ĐỨC KHUÊ", "Nguyễn Thị Thu Huyền gây ấn tượng mạnh trong lần đầu dự Đại hội Thể thao toàn quốc"),
            _slot("sentence", 1, [_url(TT_QV_1)], "TUỔI TRẺ / HTPF", "Tuyển quần vợt TP.HCM nâng cúp vàng đồng đội nam sau trận chung kết kéo dài tám tiếng"),
            # Câu 2: MMA & Boxing
            _slot("sentence", 2, [_url(TT_MMA_1)], "TUỔI TRẺ / UFC", "Chris Leben chịu cú đá cực mạnh vào vùng đầu ở hiệp một vẫn lội ngược dòng thắng điểm"),
            _slot("sentence", 2, [_url(SKY_BAK_1)], "SKY SPORTS", "Martin Bakole thế chỗ Jai Opetaia chạm trán cựu vô địch WBC Deontay Wilder"),
            # Câu 3: LPGA Q-Series
            _slot("sentence", 3, [_url(SKY_LPGA_1)], "SKY SPORTS", "Megan Khang lấy lại thẻ thi đấu LPGA Tour mùa 2027 sau khi vượt qua vòng loại Q-Series"),
            # Câu 4: Sevilla-Betis & Tottenham Women
            _slot("sentence", 4, [_ddgs("Tottenham Women football Manchester City WSL 2026")], "BING SEARCH", "Đội nữ Tottenham giành chiến thắng ấn tượng 3-1 ngay trên sân Manchester City"),
            _slot("sentence", 4, [_ddgs("Sevilla Real Betis La Liga football derby")], "BING SEARCH", "Kike Salas ghi bàn gỡ hòa kịch tính phút 90+1 giúp Sevilla chia điểm Real Betis"),
            # Câu 5: NFL Metcalf & F1 Verstappen
            _slot("sentence", 5, [_url(SKY_NFL_1)], "SKY SPORTS", "DK Metcalf tránh được án treo giò từ NFL dù bị đuổi khỏi sân ở trận gặp Eagles"),
            _slot("sentence", 5, [_ddgs("Max Verstappen Las Vegas Grand Prix 2026 F1")], "BING SEARCH", "Max Verstappen ví cuộc đua nhiều pha vượt mặt tại Las Vegas giống trò chơi điện tử"),
        ],
    },
]
