# -*- coding: utf-8 -*-
"""
daily_27_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 27.11.2026
Tuân thủ quy chuẩn Anti-Bundling (1 sự kiện / 1 vấn đề = 1 tin, 3–5 câu súc tích):
  - Intro (00): Song giọng Nữ & Nam, hide_title=True
  - 21 bản tin chính độc lập (01–21): mỗi tin 1 vấn đề rõ ràng, luân phiên Nam/Nữ
  - Mục 22 (CÁC TIN THỂ THAO KHÁC): 100% Giọng Nữ điểm nhanh tin bên lề
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


# ── URL ảnh báo chí sạch gốc 26–27.11.2026 (Việt Nam & Thế giới) ──

# 1. U17 Việt Nam & U17 World Cup 2026
TT_MALI_TEAM = "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/26/u17-mali-5-1795660880098392922759.jpg"
TN_U17_DAINHAN_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/photo-1795706855785-17957068567951282793158.jpeg"
TN_U17_TEAM_MALI = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/u17-vn-0-3-u17-mali-vff-17957048557991315051017.jpg"
TN_U17_SYBACH_MALI = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/u17-vn-0-2-u17-mali-vff01-17957072909981212806523.jpg"
TN_U17_DAINHAN_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/dai-nhan-u17-vn-0-2-u17-mali-vff2-1795707290659744240748.jpg"
TN_U17_MALI_H2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/u17-mali-to-ra-vuot-troi-ve-the-luc-khi-buoc-vao-hiep-2-1795704462330626240150.jpg"
VNE_U17_MALI = "https://i1-thethao.vnecdn.net/2026/11/26/179570284074428560458903111777-2172-2567-1795703102.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=b_VYK5QtyfU3MVNYKJEeGA"
TT_U17_MALI = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/u17-viet-nam-u17-mali-u117-world-cup-3-1795701363621847108530-182-0-1145-1840-crop-17957013986101653251644.jpeg"
DT_U17_MALI_H2 = "https://cdnphoto.dantri.com.vn/_XNXP0wK-9D-XrAHU9ijkoSjfqM=/thumb_w/1020/2026/11/26/u17-viet-nam-3-1795705469080.jpg"
TN_U17_LUC_CRY = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/17956997605117038654571401170666g8366964996231194713fdb0084cfe60d8008c46dcfc9bad6836-17957109376261295135427.jpg"
TN_U17_KHOA = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/17956997605337038654571401170666g83669649962311947139cff7c996406d37b8159fefe38a0bc0d-1795710975627418178896.jpg"
TN_U17_ROL_TEAM = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/u17-vietnam-u17-mali-1-17957080512781509554269.jpeg"
TN_U17_CDV = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/cac-cdv-viet-nam-tren-khan-dai-17957044622391673478618.jpg"
VNE_ROLAND_CRY = "https://iv1.vnecdn.net/thethao/images/web/2026/11/26/hlv-roland-khoc-khi-viet-nam-dung-buoc-o-u17-world-cup-2026-1795710041.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=uOW3Y4vEolGhhXnne5713Q"
VNE_ROLAND_HUD = "https://i1-thethao.vnecdn.net/2026/11/26/1795709747589-2144279344441617-4076-9633-1795710197.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=BjpFHDVq7v8PZOiklQcBVA"
DT_ROLAND_1 = "https://cdnphoto.dantri.com.vn/RkzpezSmlvJslVXgEe7Nqwgno9w=/zoom/1200_630/2026/11/27/roland1-cropped-1795733911917.jpg"
DT_U17_HIST = "https://cdnphoto.dantri.com.vn/eZ3-tL1VDZKQD80eD84Vqk_H-xs=/thumb_w/1020/2026/11/26/img9516-2048x1438-1795707548239.jpeg"
TN_U17_CHN = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/81af9bde-93b4-4d3a-af94-73c498034f7bpng-1795711647290349047853.jpg"
TT_U17_CHN = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/u17-trung-quoc-17957132157511041881646-236-0-1576-2560-crop-1795713404350551355070.jpg"
VNE_U17_CHN = "https://i1-thethao.vnecdn.net/2026/11/26/trie-u-tu-ng-nguye-n-u17-17957-1674-8247-1795710251.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=GoQ8rHvje9yzQXZNpeQjbw"

# 2. Bóng đá Việt Nam, Đại hội TDTT, Billiards & Campuchia
TT_QUANGHAI_VFF = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/75370742710429058349924175514341459899184511n-17858275906201131146247-219-172-1201-2048-crop-17956738752491360275783.jpeg"
TN_DINHBAC_CV = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/edit-dinh-bac-dtvn-4-2-pakistna-ngoc-linh-1795685497218283582434.jpeg"
TN_CONGVINH = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/tnw-cong-vinh-dl-1795685584648236959552.jpg"
TN_CAHN_QH = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/edit-92656265416838212167530973135923093449342200n-17957200933501828764139.jpeg"
TN_SLNA_BINH = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/tnw-photo-1795704315018-17957043160332101824944-1795704353955570784604.jpeg"
TT_SLNA_FAN = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/img5128-1795667989105787332509-98-0-1438-2560-crop-17956680223281075936853.jpg"
TN_MYTIEN_8 = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/tnw-photo-1795707041371-1795707042697780029926-1795707063636666704982.jpeg"
TN_MYTIEN_AV = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/tnw-179569446707849514889221558536664951488922155853666a6f448816a5ee8cf20f8a8fad0c15ed9-1795696620160536933903.jpg"
TN_MYTIEN_GOLD = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/tnw-17956944670954951488922155853666495148892215585366655081506d30693d7eb426f98d830a4d8-17956966202911744353271.jpg"
TN_MYTIEN_JOY = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/tnw-17956953955334951488922155853666495148892215585366606a91f4ea75bfd24220eefc4b65a5fdb-17956966203121345646888.jpg"
TT_COTUONG_LLH = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/lai-ly-huynh-2-17726860528441871190965-72-436-1184-2560-crop-17956869385152045973908.jpg"
TT_TAEKWONDO = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/khoi0830-17957102088541926390188-54-0-1394-2560-crop-17957108321831404192355.jpg"
TN_GOLF_TA_CA = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/golf-4-1795706080081874346452.jpg"
TN_GOLF_CHUCAN = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/golf-1-179570607999983562157.jpg"
TT_BXH_DAIHOI = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/rin01790-17957101304742116663998-725-0-3649-5584-crop-1795710166330725725524.jpg"
TN_MMC_PBA = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/mmc-1-1795709142251383069123.jpeg"
VNE_SVAY_1 = "https://i1-thethao.vnecdn.net/2026/11/27/svay-rieng-1795713633-5328-1795714023.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=5JzdUkAlkAoS23JaNl_oFQ"
VNE_SVAY_CELEB = "https://i1-thethao.vnecdn.net/2026/11/27/svay-rieng-jpeg-1795713766-7801-1795714023.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Lmuv_-bjW9W4FtkiCfhxhQ"
VNE_PPC = "https://i1-thethao.vnecdn.net/2026/11/27/phnom-penh-crown-1795713858-8465-1795714023.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=G4jHU6Flc-VqdF02reOH8w"

# 3. Bóng đá & Thể thao Thế giới 26–27.11.2026
SKY_BOURNE_RAYAN = "https://e0.365dm.com/26/11/1600x900/skysports-bournemouth-rayan_7417392.jpg?20261126193347&outputformat=webp"
BBC_BOURNE_ROSE = "https://ichef.bbci.co.uk/ace/standard/1024/cpsprodpb/278c/live/15481e30-e9e0-11f1-9361-cd8ed0157587.jpg"
SKY_PALACE_FRANK = "https://e0.365dm.com/26/11/1600x900/skysports-thomas-frank-crystal-palace_7417513.jpg?20261126223357&outputformat=webp"
SKY_CELTIC_DURAN = "https://e0.365dm.com/26/11/1600x900/skysports-camilo-duran-celtic_7417468.jpg?20261126215611&outputformat=webp"
SKY_SUNDERLAND = "https://e0.365dm.com/26/11/1600x900/skysports-timur-tutierov-sunderland_7417480.jpg?20261126220852&outputformat=webp"
SKY_HEARTS_MON = "https://e0.365dm.com/26/11/1600x900/skysports-wouter-vrancken-hearts_7417524.jpg?20261126225203&outputformat=webp"
TN_MU_LAMMENS = "https://images2.thanhnien.vn/528068263637045248/2026/11/26/photo-1795703456483-17957034572881652977289.jpeg"
VNE_MU_POCH = "https://i1-thethao.vnecdn.net/2026/11/26/pochettino-man-utd-1795699269-7270-1795699503.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=dXG9H_C4s_M0NACoXSjgsg"
VNE_MU_LIS = "https://i1-thethao.vnecdn.net/2026/11/26/Lisandro-Martinez-7800-1795699503.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=fBphfxrs1Y8X6L_uodxhAw"
BBC_MU_LAMMENS = "https://ichef.bbci.co.uk/ace/standard/1024/cpsprodpb/482e/live/b53f8050-e971-11f1-a094-5fdc692f3e33.jpg"
VNE_MC_HAALAND = "https://i1-thethao.vnecdn.net/2026/11/26/ap26328795529791-1795654059-9214-1795670242.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=DDNdu02aOTyOSoufJOrGxA"
VNE_MC_MARESCA = "https://i1-thethao.vnecdn.net/2026/11/26/AFP-20261028-D4QN9X6-v1-HighRe-6377-4887-1795670241.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Y_6DIzta5kgI0WPuWuen-g"
BBC_CHELSEA_FOF = "https://ichef.bbci.co.uk/ace/standard/1024/cpsprodpb/93e3/live/fe294b10-fd89-11ee-a9f7-4d961743aa47.jpg"
SKY_CHELSEA_FOF = "https://e0.365dm.com/26/11/1600x900/skysports-chelsea-wesley-fofana_7417301.png?20261126174459&outputformat=webp"
BBC_F1_RUSSELL = "https://ichef.bbci.co.uk/ace/standard/3840/cpsprodpb/8256/live/ae2c5130-e9ad-11f1-859a-37130cd3a1d7.jpg"
SKY_F1_FERRARI = "https://e0.365dm.com/26/11/1600x900/skysports-charles-leclerc-lewis-hamilton_7399379.jpg?20261106184758&outputformat=webp"
SKY_NFL_BEARS = "https://e0.365dm.com/26/11/1600x900/skysports-rome-odunze-chicago-bears_7417474.jpg?20261126220202&outputformat=webp"
TT_OANH = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/nguyen-thi-oanh-dien-kinh-17549737253041732114910-95-0-723-1200-crop-179571011411010621503.jpg"
TT_U21_QD = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/ark4881-1795699520043823641202-241-0-1581-2560-crop-1795699822237774743333.jpg"
TT_XE_DAP = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/edit-tran-trong-phuc-xe-dap-dong-nai-dai-hoi-the-thao-toan-quoc-2026-17956688793611150254785-158-0-1230-2048-crop-17956689095861707463399.jpeg"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 27.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 27 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất của thể thao Việt Nam và thế giới. "
        "Tại Qatar, đội tuyển U17 Việt Nam khép lại hành trình lịch sử ở vòng bảng U17 World Cup 2026 sau trận thua U17 Mali 0-2 trong đêm giàu cảm xúc của thầy trò huấn luyện viên Cristiano Roland. "
        "Ở đấu trường quốc nội, kình ngư Võ Thị Mỹ Tiên lần thứ hai đánh bại Nguyễn Thị Ánh Viên để chạm mốc tám huy chương vàng cá nhân tại Đại hội Thể thao toàn quốc 2026, còn đội trưởng Nguyễn Quang Hải gây chú ý với nguyện vọng chia tay đội tuyển Việt Nam. "
        "Trên sân cỏ châu Âu rạng sáng nay, AC Milan và Juventus đồng loạt ngược dòng thắng đậm tại Europa League, Bournemouth lập kỳ tích bóng đá Anh dù chơi thiếu người, trong khi Jannik Sinner lỡ hẹn Australian Open vì phẫu thuật đầu gối."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí / BBC Sport / Sky Sports / The Guardian",
    "news_source": "VIỆT NAM & THẾ GIỚI",
    "credit": "ĐIỂM ĐỌC TỔNG HỢP",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 27 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất của thể thao Việt Nam và thế giới.",
        },
        {
            "voice_preset": "primary",
            "text": "Tại Qatar, đội tuyển U17 Việt Nam khép lại hành trình lịch sử ở vòng bảng U17 World Cup 2026 sau trận thua U17 Mali 0-2 trong đêm giàu cảm xúc của thầy trò huấn luyện viên Cristiano Roland.",
        },
        {
            "voice_preset": "secondary",
            "text": "Ở đấu trường quốc nội, kình ngư Võ Thị Mỹ Tiên lần thứ hai đánh bại Nguyễn Thị Ánh Viên để chạm mốc tám huy chương vàng cá nhân tại Đại hội Thể thao toàn quốc 2026, còn đội trưởng Nguyễn Quang Hải gây chú ý với nguyện vọng chia tay đội tuyển Việt Nam.",
        },
        {
            "voice_preset": "primary",
            "text": "Trên sân cỏ châu Âu rạng sáng nay, AC Milan và Juventus đồng loạt ngược dòng thắng đậm tại Europa League, Bournemouth lập kỳ tích bóng đá Anh dù chơi thiếu người, trong khi Jannik Sinner lỡ hẹn Australian Open vì phẫu thuật đầu gối.",
        },
    ],
    "stat_badges": {
        "1": {"label": "BẢN TIN NGÀY", "value": "27.11.2026", "sub": "Toàn cảnh Việt Nam & Thế giới"},
        "2": {"label": "U17 WORLD CUP", "value": "VIỆT NAM 0-2 MALI", "sub": "Khép lại giải với cột mốc lịch sử"},
        "3": {"label": "ĐẠI HỘI TDTT 2026", "value": "MỸ TIÊN ĐẠT 8 HCV", "sub": "Vượt Ánh Viên, phá kỷ lục 200m tự do"},
        "4": {"label": "EUROPA LEAGUE", "value": "MILAN 4-2 • JUVE 4-1", "sub": "Bournemouth thắng 5/5 lượt mở màn"},
    },
    "slots": [
        # Câu 1 (4 ảnh)
        _slot("sentence", 1, [_url(TN_U17_TEAM_MALI)], "THANH NIÊN / VFF", "Đội tuyển U17 Việt Nam trong lượt trận cuối bảng G U17 World Cup 2026"),
        _slot("sentence", 1, [_url(TN_MYTIEN_8)], "THANH NIÊN / ĐỘC LẬP", "Kình ngư Võ Thị Mỹ Tiên tỏa sáng rực rỡ tại Đại hội Thể thao toàn quốc 2026"),
        _slot("sentence", 1, [_url(SKY_BOURNE_RAYAN)], "SKY SPORTS", "Rayan ăn mừng bàn thắng lịch sử giúp Bournemouth toàn thắng năm trận Europa League"),
        _slot("sentence", 1, [_ddgs("Jannik Sinner tennis Melbourne Australian Open")], "BING SEARCH", "Tay vợt số hai thế giới Jannik Sinner chính thức vắng mặt tại Australian Open 2027"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(VNE_U17_MALI)], "VNEXPRESS / ĐOÀN CA", "U17 Việt Nam chiến đấu kiên cường trước dàn cầu thủ giàu thể lực của U17 Mali"),
        _slot("sentence", 2, [_url(TN_U17_DAINHAN_1)], "THANH NIÊN / VFF", "Tiền đạo Đại Nhân bỏ lỡ cơ hội đối mặt đáng tiếc trong hiệp một"),
        _slot("sentence", 2, [_url(VNE_ROLAND_CRY)], "VNEXPRESS / ĐOÀN CA", "Huấn luyện viên Cristiano Roland rơi nước mắt cảm ơn học trò sau trận đấu"),
        _slot("sentence", 2, [_url(TN_U17_LUC_CRY)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực để lại dấu ấn đậm nét ở sân chơi U17 World Cup"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url(TN_MYTIEN_AV)], "THANH NIÊN / ĐỘC LẬP", "Võ Thị Mỹ Tiên vượt qua đàn chị Nguyễn Thị Ánh Viên ở chung kết 200m tự do"),
        _slot("sentence", 3, [_url(TN_MYTIEN_JOY)], "THANH NIÊN / ĐỘC LẬP", "Võ Thị Mỹ Tiên dẫn đầu bảng vàng cá nhân với tám huy chương vàng bơi lội"),
        _slot("sentence", 3, [_url(TT_QUANGHAI_VFF)], "TUỔI TRẺ / BTC", "Thông tin về nguyện vọng chia tay tuyển Việt Nam của Nguyễn Quang Hải thu hút sự chú ý"),
        _slot("sentence", 3, [_url(TN_CAHN_QH)], "THANH NIÊN / CAHN", "Quang Hải chuẩn bị cùng Công an Hà Nội đối đầu Nam Định ở vòng chín V-League"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_ddgs("AC Milan football celebration Europa League 2026")], "BING SEARCH", "AC Milan lội ngược dòng thắng Olympiacos 4-2 ngay tại Athens"),
        _slot("sentence", 4, [_ddgs("Juventus football players celebration goal")], "BING SEARCH", "Juventus ngược dòng thắng Omonia Nicosia 4-1 để vươn lên nhì bảng Europa League"),
        _slot("sentence", 4, [_url(BBC_BOURNE_ROSE)], "BBC SPORT", "Huấn luyện viên Marco Rose giúp Bournemouth đạt chuỗi mười trận thắng liên tiếp"),
        _slot("sentence", 4, [_ddgs("Jannik Sinner knee injury tennis")], "BING SEARCH", "Jannik Sinner vừa trải qua ca tiểu phẫu đầu gối phải tại Phần Lan"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — U17 VIỆT NAM THUA MALI 0-2, CHÍNH THỨC DỪNG BƯỚC)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Việt Nam thua U17 Mali 0-2, chính thức dừng bước tại vòng bảng U17 World Cup 2026",
        "summary": (
            "Ở lượt trận cuối bảng G U17 World Cup 2026 tối ngày 26 tháng 11 tại Qatar, đội tuyển U17 Việt Nam nhận thất bại 0-2 trước đội đầu bảng U17 Mali. "
            "Dù đối thủ xoay tua năm vị trí trong đội hình xuất phát, U17 Việt Nam vẫn phải căng mình phòng ngự trước 27 cú sút và bỏ lỡ cơ hội đối mặt đáng tiếc của tiền đạo Đại Nhân trong hiệp một. "
            "Bước sang hiệp hai khi thể lực suy giảm, hàng thủ áo đỏ không thể đứng vững trước các pha dứt điểm của Sanaba Keita ở phút 56 và Djigui Koita ở phút 82. "
            "Cùng giờ ở bảng G, U17 Bỉ thắng đậm U17 New Zealand 6-0 để cùng đội toàn thắng Mali giành vé đi tiếp, còn U17 Việt Nam kết thúc ở hạng ba với một điểm."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / VFF",
        "stat_badges": {
            "1": {"label": "LƯỢT CUỐI BẢNG G", "value": "U17 VIỆT NAM 0-2 MALI", "sub": "Sân Aspire Zone, Qatar tối 26/11"},
            "2": {"label": "SỨC ÉP VƯỢT TRỘI", "value": "MALI TUNG 27 CÚ SÚT", "sub": "Đại Nhân lỡ cơ hội vàng hiệp 1"},
            "4": {"label": "XẾP HẠNG BẢNG G", "value": "MALI 9Đ • BỈ 6Đ • VN 1Đ", "sub": "Bỉ thắng New Zealand 6-0 ở trận cùng giờ"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_U17_TEAM_MALI)], "THANH NIÊN / VFF", "Đội hình xuất phát của U17 Việt Nam trong trận đấu quyết định với U17 Mali"),
            _slot("title", 0, [_url(TT_U17_MALI)], "TUỔI TRẺ / VFF", "Các cầu thủ U17 Việt Nam nỗ lực tranh chấp trước đối thủ giàu sức mạnh từ châu Phi"),
            _slot("sentence", 1, [_url(VNE_U17_MALI)], "VNEXPRESS / ĐOÀN CA", "U17 Việt Nam chia tay U17 World Cup 2026 sau trận thua 0-2 trước U17 Mali"),
            _slot("sentence", 2, [_url(TN_U17_DAINHAN_1)], "THANH NIÊN / VFF", "Pha bỏ lỡ đáng tiếc của Đại Nhân trong tình huống đối mặt thủ môn đầu trận"),
            _slot("sentence", 2, [_url(TN_U17_DAINHAN_2)], "THANH NIÊN / VFF", "Hàng thủ U17 Việt Nam đã thi đấu tập trung để giữ sạch lưới suốt hiệp một"),
            _slot("sentence", 3, [_url(TT_MALI_TEAM), _ddgs("Mali U17 football team World Cup")], "TUỔI TRẺ / FIFA", "U17 Mali gia tăng sức ép trong hiệp hai và ghi hai bàn thắng quyết định"),
            _slot("sentence", 4, [_url(TN_U17_SYBACH_MALI)], "THANH NIÊN / VFF", "U17 Việt Nam xếp thứ ba bảng G, trên U17 New Zealand sau ba lượt trận"),
        ],
    },

    # 02 (Nữ — CỘT MỐC LỊCH SỬ & NƯỚC MẮT CỦA HLV ROLAND, NGUYỄN LỰC)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "U17 WORLD CUP 2026",
        "title": "Cột mốc lịch sử của U17 Việt Nam và nước mắt cảm xúc từ thầy trò HLV Cristiano Roland",
        "summary": (
            "Dù dừng bước ngay từ vòng bảng, U17 Việt Nam vẫn thiết lập cột mốc lịch sử khi đạt thứ hạng và số bàn thắng cao nhất trong số các đội tuyển Việt Nam từng dự World Cup bóng đá 11 người. "
            "Với vị trí thứ ba bảng đấu cùng năm pha lập công, đoàn quân của huấn luyện viên Cristiano Roland vượt qua thành tích đứng cuối bảng và không ghi bàn của U20 Việt Nam năm 2017 lẫn đội tuyển nữ năm 2023. "
            "Sau tiếng còi mãn cuộc, chiến lược gia người Brazil bật khóc, chắp tay cảm ơn các học trò đã chiến đấu quả cảm và khẳng định đây là tương lai của bóng đá Việt Nam. "
            "Tiền vệ Chu Ngọc Nguyễn Lực cũng không giấu được những giọt nước mắt tiếc nuối, đồng thời gửi lời tri ân tới người hâm mộ đã cổ vũ đội tuyển tại Qatar."
        ),
        "source": "Dân Trí / Thanh Niên / VnExpress",
        "news_source": "DÂN TRÍ / THANH NIÊN",
        "credit": "VNEXPRESS / DÂN TRÍ",
        "stat_badges": {
            "1": {"label": "CỘT MỐC WORLD CUP", "value": "5 BÀN • HẠNG 3 BẢNG G", "sub": "Thành tích tốt nhất của bóng đá VN sân 11 người"},
            "3": {"label": "CẢM XÚC SAU TRẬN", "value": "HLV ROLAND RƠI NƯỚC MẮT", "sub": "Chắp tay cảm ơn toàn đội U17 Việt Nam"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_U17_HIST)], "DÂN TRÍ / VFF", "Tập thể U17 Việt Nam nhận nhiều lời khen ngợi trong lần đầu dự World Cup"),
            _slot("title", 0, [_url(DT_ROLAND_1)], "DÂN TRÍ / VFF", "Huấn luyện viên Cristiano Roland tự hào về màn trình diễn của các học trò"),
            _slot("sentence", 1, [_url(TN_U17_ROL_TEAM)], "THANH NIÊN / HƯƠNG NGUYỄN", "U17 Việt Nam tạo cột mốc đáng nhớ với năm bàn thắng sau ba trận vòng bảng"),
            _slot("sentence", 2, [_url(TN_U17_CDV)], "THANH NIÊN / VFF", "Thành tích của lứa U17 năm nay vượt qua các lần dự World Cup trước đây của Việt Nam"),
            _slot("sentence", 3, [_url(VNE_ROLAND_CRY)], "VNEXPRESS / ĐOÀN CA", "Khoảnh khắc xúc động khi huấn luyện viên Cristiano Roland khóc cảm ơn cầu thủ"),
            _slot("sentence", 3, [_url(VNE_ROLAND_HUD)], "VNEXPRESS / ĐOÀN CA", "Nhà cầm quân người Brazil tin tưởng lứa cầu thủ trẻ sẽ tiến xa trong tương lai"),
            _slot("sentence", 4, [_url(TN_U17_LUC_CRY)], "THANH NIÊN / VFF", "Chu Ngọc Nguyễn Lực xúc động sau trận đấu cuối cùng tại vòng bảng"),
            _slot("sentence", 4, [_url(TN_U17_KHOA)], "THANH NIÊN / VFF", "Đội trưởng Đăng Khoa và đồng đội nhìn nhận thẳng thắn bài học thể lực trước đối thủ mạnh"),
        ],
    },

    # 03 (Nam — U17 TRUNG QUỐC THẮNG ĐẬM FIJI 8-0 GIÀNH VÉ VỚT, XÁC ĐỊNH 27 ĐỘI VÒNG 32)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 Trung Quốc thắng đậm Fiji 8-0 giành vé vớt, xác định 27 đội vào vòng 32 đội U17 World Cup",
        "summary": (
            "Ở lượt trận cuối bảng H rạng sáng 27 tháng 11, U17 Trung Quốc đánh bại U17 Fiji với tỷ số đậm 8-0 để lách qua khe cửa hẹp tiến vào vòng 32 đội U17 World Cup 2026. "
            "Chỉ có một điểm sau hai trận đầu, đội bóng trẻ xứ tỷ dân đã nã bốn bàn ngay trong hiệp một trước khi ghi thêm bốn bàn ở hiệp hai để đạt bốn điểm và chiếm suất vé vớt dành cho nhóm đội hạng ba xuất sắc nhất. "
            "Trong trận đấu còn lại của bảng H, U17 Tây Ban Nha vượt qua U17 Ma Rốc 2-0 để giữ vững ngôi đầu bảng. "
            "Tính đến sáng nay, giải đấu tại Qatar đã xác định 27 đội vào vòng loại trực tiếp, trong đó khu vực châu Á góp mặt năm đại diện gồm Nhật Bản, Hàn Quốc, Uzbekistan, Tajikistan và Trung Quốc."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "LƯỢT CUỐI BẢNG H", "value": "TRUNG QUỐC 8-0 FIJI", "sub": "Đạt 4 điểm để đoạt vé vớt hạng 3"},
            "4": {"label": "ĐẠI DIỆN CHÂU Á", "value": "5 ĐỘI VÀO VÒNG 32 ĐỘI", "sub": "Nhật, Hàn, Uzbekistan, Tajikistan, Trung Quốc"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_U17_CHN)], "TUỔI TRẺ / SOHU", "Các cầu thủ U17 Trung Quốc ăn mừng chiến thắng đậm 8-0 trước U17 Fiji"),
            _slot("title", 0, [_url(VNE_U17_CHN)], "VNEXPRESS / TÂN HOA XÃ", "U17 Trung Quốc bứt phá ở lượt trận cuối để giành quyền vào vòng 32 đội"),
            _slot("sentence", 1, [_url(TT_U17_CHN)], "TUỔI TRẺ / SOHU", "Chiến thắng trước U17 Fiji giúp U17 Trung Quốc lách qua khe cửa hẹp bảng H"),
            _slot("sentence", 2, [_url(VNE_U17_CHN)], "VNEXPRESS / TÂN HOA XÃ", "Ngôi sao trẻ Triệu Tùng Nguyên góp công giúp U17 Trung Quốc vượt qua vòng bảng"),
            _slot("sentence", 3, [_ddgs("Spain national football team match celebration")], "BING SEARCH", "U17 Tây Ban Nha thắng U17 Ma Rốc 2-0 để giành ngôi nhất bảng H"),
            _slot("sentence", 4, [_ddgs("China U17 football team FIFA World Cup")], "BING SEARCH", "Châu Á đã có năm đại diện góp mặt tại vòng 32 đội U17 World Cup 2026"),
        ],
    },

    # 04 (Nữ — QUANG HẢI CÓ NGUYỆN VỌNG CHIA TAY TUYỂN VN, CÔNG VINH CHỌN ĐÌNH BẮC)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "BÓNG ĐÁ VIỆT NAM",
        "title": "Đội trưởng Quang Hải có nguyện vọng chia tay tuyển Việt Nam, HLV Kim Sang Sik chưa đồng ý",
        "summary": (
            "Tại buổi họp báo công bố giải thưởng Quả bóng vàng Việt Nam 2026 sáng 26 tháng 11, Phó Chủ tịch Liên đoàn Bóng đá Việt Nam Trần Anh Tú tiết lộ đội trưởng Nguyễn Quang Hải đang có nguyện vọng chia tay đội tuyển quốc gia. "
            "Theo ông Trần Anh Tú, tiền vệ sinh năm 1997 muốn rút lui để tập trung thi đấu cho câu lạc bộ Công an Hà Nội, nhưng huấn luyện viên Kim Sang Sik chưa đồng ý và vẫn muốn tổ chức một trận đấu tri ân xứng đáng. "
            "Đại diện liên đoàn nhấn mạnh đây mới chỉ là mong muốn cá nhân của Quang Hải chứ chưa phải quyết định chính thức vì anh vừa vắng mặt ở đợt tập trung gần nhất do chấn thương. "
            "Cũng tại sự kiện này, cựu danh thủ Lê Công Vinh cho rằng Nguyễn Đình Bắc là ứng viên xứng đáng nhất cho danh hiệu Quả bóng vàng Việt Nam 2026."
        ),
        "source": "Tuổi Trẻ / Thanh Niên",
        "news_source": "TUỔI TRẺ / THANH NIÊN",
        "credit": "TUỔI TRẺ / THANH NIÊN",
        "stat_badges": {
            "1": {"label": "HỌP BÁO QBV 2026", "value": "QUANG HẢI MUỐN RỜI TUYỂN", "sub": "Phó Chủ tịch VFF Trần Anh Tú xác nhận"},
            "2": {"label": "PHẢN HỒI BAN HUẤN LUYỆN", "value": "KIM SANG SIK CHƯA ĐỒNG Ý", "sub": "Dự kiến tổ chức trận đấu tri ân đội trưởng"},
            "4": {"label": "ĐỀ CỬ TỪ CÔNG VINH", "value": "CHỌN ĐÌNH BẮC CHO QBV", "sub": "Đánh giá cao đóng góp ở CLB và đội tuyển"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_QUANGHAI_VFF)], "TUỔI TRẺ / BTC", "Phó Chủ tịch VFF Trần Anh Tú chia sẻ về trường hợp của đội trưởng Nguyễn Quang Hải"),
            _slot("title", 0, [_url(TN_CAHN_QH)], "THANH NIÊN / CAHN", "Quang Hải muốn tập trung cống hiến cho câu lạc bộ Công an Hà Nội"),
            _slot("sentence", 1, [_url(TT_QUANGHAI_VFF)], "TUỔI TRẺ / BTC", "Thông tin về nguyện vọng của Quang Hải được công bố tại lễ ra mắt Quả bóng vàng 2026"),
            _slot("sentence", 2, [_url(TN_CAHN_QH)], "THANH NIÊN / CAHN", "Huấn luyện viên Kim Sang Sik vẫn trân trọng vai trò và muốn tri ân Quang Hải"),
            _slot("sentence", 3, [_ddgs("Kim Sang Sik Vietnam football coach")], "BING SEARCH", "Đội tuyển Việt Nam đang trong giai đoạn chuyển giao lực lượng dưới thời ông Kim Sang Sik"),
            _slot("sentence", 4, [_url(TN_DINHBAC_CV)], "THANH NIÊN", "Tiền đạo Nguyễn Đình Bắc được cựu danh thủ Lê Công Vinh chọn cho Quả bóng vàng 2026"),
            _slot("sentence", 4, [_url(TN_CONGVINH)], "THANH NIÊN", "Lê Công Vinh phát biểu tại sự kiện công bố giải thưởng Quả bóng vàng Việt Nam"),
        ],
    },

    # 05 (Nam — ĐẠI CHIẾN NHÓM ĐẦU V-LEAGUE CHIỀU NAY: NAM ĐỊNH VS CAHN, SLNA VS NINH BÌNH)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "V-LEAGUE 2026-2027",
        "title": "Đại chiến nhóm đầu V-League chiều nay: Nam Định đấu Công an Hà Nội, SLNA tiếp Ninh Bình",
        "summary": (
            "Hai trận đấu mở màn vòng chín V-League 2026-2027 diễn ra cùng lúc 18 giờ chiều nay ngày 27 tháng 11 hứa hẹn tạo ra bước ngoặt lớn khi bốn đội dẫn đầu bảng đối đầu trực tiếp. "
            "Trên sân Thiên Trường, đội đầu bảng Nam Định đang có 19 điểm tiếp đón Công an Hà Nội, đội xếp thứ tư với 14 điểm nhưng còn một trận chưa đấu và vừa có bước chạy đà hưng phấn ở đấu trường châu Á. "
            "Cùng giờ tại sân Vinh, đội bóng duy nhất còn bất bại mùa này là Sông Lam Nghệ An với 14 điểm và chốt chặn vững chắc Cao Văn Bình sẽ chạm trán đội nhì bảng Ninh Bình đang sở hữu 16 điểm cùng ngôi sao Nguyễn Hoàng Đức. "
            "Trước giờ bóng lăn, ban tổ chức sân Vinh cũng đã hoàn tất việc đổi và tặng thêm vé cho khoảng 300 khán giả từng gặp sự cố không thể vào sân ở vòng đấu trước."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "stat_badges": {
            "1": {"label": "18H HÔM NAY (27/11)", "value": "ĐẠI CHIẾN TOP 4 V-LEAGUE", "sub": "Mở màn vòng 9 đầy kịch tính"},
            "2": {"label": "SÂN THIÊN TRƯỜNG", "value": "NAM ĐỊNH (19Đ) VS CAHN (14Đ)", "sub": "CAHN có cơ hội rút ngắn cách biệt còn 2 điểm"},
            "3": {"label": "SÂN VINH", "value": "SLNA (14Đ) VS NINH BÌNH (16Đ)", "sub": "Cao Văn Bình đọ sức hàng công Hoàng Đức"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_CAHN_QH)], "THANH NIÊN / CAHN", "Công an Hà Nội hướng tới chiến thắng trên sân Thiên Trường của Nam Định"),
            _slot("title", 0, [_url(TN_SLNA_BINH)], "THANH NIÊN", "Thủ môn Cao Văn Bình là điểm tựa giúp Sông Lam Nghệ An duy trì mạch bất bại"),
            _slot("sentence", 1, [_url(TN_CAHN_QH)], "THANH NIÊN / CAHN", "Cuộc đua nhóm đầu V-League 2026-2027 nóng lên ngay ở lượt trận sớm vòng chín"),
            _slot("sentence", 2, [_ddgs("Nam Dinh FC football V-League stadium")], "BING SEARCH", "Nam Định đang dẫn đầu bảng với 19 điểm sau tám vòng đấu"),
            _slot("sentence", 3, [_url(TN_SLNA_BINH)], "THANH NIÊN", "Cao Văn Bình gánh vác trọng trách giữ sạch lưới trước Ninh Bình của Hoàng Đức"),
            _slot("sentence", 4, [_url(TT_SLNA_FAN)], "TUỔI TRẺ / DOÃN HÒA", "Sông Lam Nghệ An đổi và tặng thêm vé tri ân 300 cổ động viên tại sân Vinh"),
        ],
    },

    # 06 (Nữ — VÕ THỊ MỸ TIÊN LẦN THỨ HAI ĐÁNH BẠI ÁNH VIÊN, CHẠM MỐC 8 HCV CÁ NHÂN)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "ĐẠI HỘI TDTT TOÀN QUỐC 2026",
        "title": "Kình ngư Võ Thị Mỹ Tiên lần thứ hai đánh bại Ánh Viên, chạm mốc 8 HCV cá nhân",
        "summary": (
            "Đường đua xanh tại Đại hội Thể thao toàn quốc 2026 tối ngày 26 tháng 11 tiếp tục chứng kiến màn bứt phá ấn tượng của kình ngư 21 tuổi Võ Thị Mỹ Tiên. "
            "Ở chung kết 200m tự do nữ, dù Nguyễn Thị Ánh Viên dẫn đầu phần lớn quãng đường, sức trẻ của Mỹ Tiên đã giúp cô vượt lên ở những mét cuối để giành huy chương vàng với thành tích 2 phút 01 giây 29, phá sâu kỷ lục đại hội cũ. "
            "Đây là lần thứ hai tại đại hội năm nay Mỹ Tiên đánh bại đàn chị Ánh Viên, trước khi kình ngư đoàn Tây Ninh thắng tiếp nội dung 200m ếch để nâng tổng thành tích lên tám huy chương vàng cá nhân. "
            "Ngay sau khi chạm đích, Ánh Viên vẫn nở nụ cười rạng rỡ, ôm chúc mừng đàn em trong khoảnh khắc chuyển giao đầy cảm xúc của bơi lội Việt Nam."
        ),
        "source": "Thanh Niên / Dân Trí",
        "news_source": "THANH NIÊN / DÂN TRÍ",
        "credit": "THANH NIÊN / ĐỘC LẬP",
        "stat_badges": {
            "2": {"label": "200M TỰ DO NỮ", "value": "2 PHÚT 01 GIÂY 29 • KỶ LỤC", "sub": "Mỹ Tiên vượt Ánh Viên ở mét cuối"},
            "3": {"label": "DẪN ĐẦU BƠI LỘI", "value": "MỸ TIÊN ĐẠT 8 HCV CÁ NHÂN", "sub": "Thúy Hiền 7 HCV • Ánh Viên 5 HCV"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_MYTIEN_8)], "THANH NIÊN / ĐỘC LẬP", "Võ Thị Mỹ Tiên chạm mốc tám huy chương vàng cá nhân tại Đại hội 2026"),
            _slot("title", 0, [_url(TN_MYTIEN_AV)], "THANH NIÊN / ĐỘC LẬP", "Võ Thị Mỹ Tiên lần thứ hai vượt qua đàn chị Nguyễn Thị Ánh Viên"),
            _slot("sentence", 1, [_url(TN_MYTIEN_JOY)], "THANH NIÊN / ĐỘC LẬP", "Kình ngư 21 tuổi đoàn Tây Ninh thi đấu bùng nổ trên đường đua xanh"),
            _slot("sentence", 2, [_url(TN_MYTIEN_GOLD)], "THANH NIÊN / ĐỘC LẬP", "Mỹ Tiên phá kỷ lục đại hội cự ly 200m tự do nữ với 2 phút 01 giây 29"),
            _slot("sentence", 3, [_url(TN_MYTIEN_8)], "THANH NIÊN / ĐỘC LẬP", "Mỹ Tiên đoạt thêm huy chương vàng 200m ếch ngay sau đó"),
            _slot("sentence", 4, [_url(TN_MYTIEN_AV)], "THANH NIÊN / ĐỘC LẬP", "Hình ảnh đẹp khi Ánh Viên chúc mừng đàn em sau cuộc đua kịch tính"),
        ],
    },

    # 07 (Nam — CỜ TƯỚNG SIÊU KINH ĐIỂN, GOLF & BẢNG TỔNG SẮP ĐẠI HỘI TDTT 2026)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "ĐẠI HỘI TDTT TOÀN QUỐC 2026",
        "title": "Lại Lý Huynh - Nhật Quang thắng siêu kinh điển cờ tướng, TP. HCM nới rộng ngôi đầu Đại hội",
        "summary": (
            "Tính đến khuya ngày 26 tháng 11, đoàn thể thao Thành phố Hồ Chí Minh nâng tổng thành tích lên 86 huy chương vàng, tiếp tục dẫn đầu bảng tổng sắp Đại hội Thể thao toàn quốc 2026 và nới rộng cách biệt với đoàn Hà Nội lên 20 huy chương vàng. "
            "Điểm nhấn nổi bật là trận chung kết cờ tướng tiêu chuẩn đôi nam được ví như siêu kinh điển, nơi Lại Lý Huynh cầm hòa Hà Văn Tiến để Nguyễn Minh Nhật Quang đánh bại Nguyễn Thành Bảo, giúp chủ nhà thắng Đồng Nai 1,5 - 0,5. "
            "Trong ngày thi đấu thành công, các võ sĩ taekwondo Thành phố Hồ Chí Minh cũng giành thêm ba huy chương vàng đối kháng bên cạnh ba ngôi vô địch bắn cung. "
            "Ở chiều ngược lại, đoàn Hà Nội gặt hái cú đúp huy chương vàng môn golf nhờ màn trình diễn kỷ lục âm 10 gậy của Nguyễn Tuấn Anh và chức vô địch lần thứ tư liên tiếp của Lê Chúc An."
        ),
        "source": "Tuổi Trẻ / Thanh Niên",
        "news_source": "TUỔI TRẺ / THANH NIÊN",
        "credit": "TUỔI TRẺ / THANH NIÊN",
        "stat_badges": {
            "1": {"label": "BẢNG TỔNG SẮP 26/11", "value": "TP. HCM 86 HCV • HÀ NỘI 66 HCV", "sub": "Quân đội 37 HCV • CAND 29 HCV • Hải Phòng 25 HCV"},
            "2": {"label": "CỜ TƯỚNG ĐÔI NAM", "value": "TP. HCM THẮNG ĐỒNG NAI 1,5-0,5", "sub": "Lại Lý Huynh & Nhật Quang đoạt HCV"},
            "4": {"label": "GOLF QUỐC GIA 2026", "value": "TUẤN ANH & CHÚC AN VÔ ĐỊCH", "sub": "Mang về cú đúp HCV cho đoàn Hà Nội"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_COTUONG_LLH)], "TUỔI TRẺ / TLKĐ", "Lại Lý Huynh góp công lớn giúp cờ tướng Thành phố Hồ Chí Minh đoạt huy chương vàng"),
            _slot("title", 0, [_url(TT_TAEKWONDO)], "TUỔI TRẺ / N.K", "Đoàn thể thao Thành phố Hồ Chí Minh củng cố vững chắc ngôi đầu với 86 huy chương vàng"),
            _slot("sentence", 1, [_url(TT_BXH_DAIHOI)], "TUỔI TRẺ", "Các môn thế mạnh góp phần giúp Thành phố Hồ Chí Minh nới rộng cách biệt lên 20 HCV"),
            _slot("sentence", 2, [_url(TT_COTUONG_LLH)], "TUỔI TRẺ / TLKĐ", "Trận chung kết cờ tướng đôi nam quy tụ bốn kỳ thủ hàng đầu Việt Nam"),
            _slot("sentence", 3, [_url(TT_TAEKWONDO)], "TUỔI TRẺ / N.K", "Taekwondo Thành phố Hồ Chí Minh giành ba huy chương vàng ngày đầu thi đấu đối kháng"),
            _slot("sentence", 4, [_url(TN_GOLF_TA_CA)], "THANH NIÊN / BTC", "Nguyễn Tuấn Anh và Lê Chúc An đoạt cú đúp huy chương vàng golf cho Hà Nội"),
            _slot("sentence", 4, [_url(TN_GOLF_CHUCAN)], "THANH NIÊN / BTC", "Golfer nữ Lê Chúc An thống trị giải vô địch quốc gia với bốn lần đăng quang liên tiếp"),
        ],
    },

    # 08 (Nữ — BILLIARDS PBA TOUR: MÃ MINH CẨM NGƯỢC DÒNG HẠ CỰU SỐ 1 THẾ GIỚI KIM JUN-TAE)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "BILLIARDS QUỐC TẾ",
        "title": "Billiards PBA Tour: Mã Minh Cẩm ngược dòng ngoạn mục hạ cựu số 1 thế giới Kim Jun-tae",
        "summary": (
            "Tại vòng 32 cơ thủ chặng thứ sáu giải billiards chuyên nghiệp Hàn Quốc PBA Tour tối 26 tháng 11, đại diện duy nhất của Việt Nam là Mã Minh Cẩm tạo nên màn lội ngược dòng giàu cảm xúc trước cựu số 1 thế giới Kim Jun-tae. "
            "Đối đầu tay cơ từng giữ kỷ lục thế giới sê-ri 28 điểm, Minh Cẩm để thua chóng vánh 4-15 trong ván mở màn trước khi bình tĩnh điều chỉnh nhịp độ để thắng lại hai ván liên tiếp với cùng tỷ số 15-11. "
            "Kịch tính lên tới đỉnh điểm ở ván thứ tư khi Kim Jun-tae chạm mốc 14 điểm và chỉ còn cách chiến thắng đúng một điểm, nhưng bản lĩnh thép đã giúp cơ thủ Việt Nam cứu thua thành công để ngược dòng khép lại trận đấu. "
            "Chiến thắng ấn tượng này đưa Mã Minh Cẩm tiến vào vòng 16 cơ thủ thi đấu trong ngày hôm nay 27 tháng 11."
        ),
        "source": "Thanh Niên",
        "news_source": "THANH NIÊN",
        "credit": "THANH NIÊN / PBA",
        "stat_badges": {
            "1": {"label": "PBA TOUR CHẶNG 6", "value": "MÃ MINH CẨM VÀO VÒNG 16", "sub": "Đại diện Việt Nam duy nhất còn lại"},
            "3": {"label": "NGƯỢC DÒNG BẢN LĨNH", "value": "CỨU MATCH-POINT Ở VÁN 4", "sub": "Hạ cựu số 1 thế giới UMB Kim Jun-tae"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_MMC_PBA)], "THANH NIÊN / PBA", "Cơ thủ Mã Minh Cẩm khẳng định bản lĩnh tại chặng sáu PBA Tour 2026-2027"),
            _slot("title", 0, [_ddgs("Ma Minh Cam billiards PBA Tour Korea")], "BING SEARCH", "Đại diện Việt Nam ngược dòng ấn tượng trước đối thủ mạnh Hàn Quốc"),
            _slot("sentence", 1, [_url(TN_MMC_PBA)], "THANH NIÊN / PBA", "Mã Minh Cẩm là tay cơ Việt Nam duy nhất góp mặt ở vòng 32 chặng đấu lần này"),
            _slot("sentence", 2, [_ddgs("Kim Jun Tae billiards carom 3 cushion")], "BING SEARCH", "Kim Jun-tae từng đứng số một thế giới UMB trước khi chuyển sang hệ thống PBA"),
            _slot("sentence", 3, [_url(TN_MMC_PBA)], "THANH NIÊN / PBA", "Bản lĩnh ở thời khắc quyết định giúp Minh Cẩm vượt qua ngưỡng cửa sinh tử"),
            _slot("sentence", 4, [_ddgs("3 cushion carom billiards tournament match")], "BING SEARCH", "Mã Minh Cẩm tiếp tục hành trình tại vòng 16 cơ thủ trong ngày 27 tháng 11"),
        ],
    },

    # 09 (Nam — ĐỊA CHẤN CÚP C2 CHÂU Á: CLB CAMPUCHIA SVAY RIENG HẠ ĐỘI NHẬT MACHIDA ZELVIA)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "AFC CHAMPIONS LEAGUE TWO",
        "title": "Địa chấn Cúp C2 châu Á: CLB Svay Rieng của Campuchia quật ngã Machida Zelvia 2-0",
        "summary": (
            "Làng bóng đá Đông Nam Á chứng kiến cú sốc lớn ở lượt trận thứ năm vòng bảng AFC Champions League Two tối 26 tháng 11 khi Preah Khan Reach Svay Rieng của Campuchia đánh bại Machida Zelvia 2-0. "
            "Hai pha lập công trong hiệp hai của Martins Junior và Tiago Alves giúp chủ nhà cắt đứt mạch 15 trận bất bại của đại diện Nhật Bản, đội vốn toàn thắng cả bốn lượt đầu tiên. "
            "Kết quả này đưa Svay Rieng lên 10 điểm và đứng nhì bảng G, nắm quyền tự quyết suất vào vòng knock-out trước lượt cuối gặp Thượng Hải Thân Hoa. "
            "Trong khi đó, một câu lạc bộ Campuchia khác là Phnom Penh Crown dù thua Kuching City 0-3 trên sân khách vẫn giữ ngôi đầu bảng H với chín điểm."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / SVAY RIENG FC",
        "stat_badges": {
            "1": {"label": "CÚP C2 CHÂU Á • BẢNG G", "value": "SVAY RIENG 2-0 MACHIDA", "sub": "Chấm dứt chuỗi 15 trận bất bại của đội Nhật"},
            "3": {"label": "CƠ HỘI ĐI TIẾP", "value": "SVAY RIENG 10Đ • PPC 9Đ", "sub": "Cả 2 CLB Campuchia sáng cửa vào knock-out"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_SVAY_1)], "VNEXPRESS / SVAY RIENG FC", "Svay Rieng thi đấu đầy tự tin trước đại diện Nhật Bản Machida Zelvia"),
            _slot("title", 0, [_url(VNE_SVAY_CELEB)], "VNEXPRESS / SVAY RIENG FC", "Cầu thủ Svay Rieng ăn mừng chiến thắng gây chấn động sân Morodok Techo"),
            _slot("sentence", 1, [_url(VNE_SVAY_1)], "VNEXPRESS / SVAY RIENG FC", "Đại diện Campuchia tạo địa chấn ở lượt trận thứ năm AFC Champions League Two"),
            _slot("sentence", 2, [_url(VNE_SVAY_CELEB)], "VNEXPRESS / SVAY RIENG FC", "Martins Junior và Tiago Alves tỏa sáng trong hiệp hai để định đoạt trận đấu"),
            _slot("sentence", 3, [_url(VNE_SVAY_1)], "VNEXPRESS / SVAY RIENG FC", "Svay Rieng chỉ cần không thua Thượng Hải Thân Hoa ở lượt cuối để đi tiếp"),
            _slot("sentence", 4, [_url(VNE_PPC)], "VNEXPRESS / PHNOM PENH CROWN", "Phnom Penh Crown dù thua 0-3 trước Kuching City vẫn dẫn đầu bảng H với chín điểm"),
        ],
    },

    # 10 (Nữ — BOURNEMOUTH LẬP KỲ TÍCH BÓNG ĐÁ ANH TẠI EUROPA LEAGUE DÙ MẤT NGƯỜI)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "UEFA EUROPA LEAGUE",
        "title": "Bournemouth viết nên lịch sử bóng đá Anh ở Europa League dù mất người từ hiệp một",
        "summary": (
            "Rạng sáng 27 tháng 11, Bournemouth tạo nên màn ngược dòng phi thường khi đánh bại Celta Vigo 2-1 ngay trên đất Tây Ban Nha dù phải chơi thiếu người từ phút 23. "
            "Sau khi để Iago Aspas mở tỷ số và Bafode Diakite nhận thẻ đỏ rời sân, đội bóng của huấn luyện viên Marco Rose bùng nổ trong hiệp hai nhờ cú đánh đầu của Alvaro Rodriguez và bàn ấn định từ pha phản công của Rayan ở phút 78. "
            "Chiến thắng này giúp Bournemouth trở thành câu lạc bộ Anh đầu tiên trong lịch sử toàn thắng cả năm trận mở màn tại một giải đấu lớn của châu Âu. "
            "Đồng thời, họ cũng nối dài mạch toàn thắng trên mọi đấu trường lên con số 10 và độc chiếm ngôi đầu bảng xếp hạng Europa League."
        ),
        "source": "BBC Sport / Sky Sports / The Guardian",
        "news_source": "BBC SPORT / SKY SPORTS",
        "credit": "SKY SPORTS / BBC SPORT",
        "stat_badges": {
            "1": {"label": "EUROPA LEAGUE • LƯỢT 5", "value": "CELTA VIGO 1-2 BOURNEMOUTH", "sub": "Thắng ngược dù mất người từ phút 23"},
            "3": {"label": "KỶ LỤC BÓNG ĐÁ ANH", "value": "TOÀN THẮNG 5 TRẬN MỞ MÀN", "sub": "Nối dài mạch 10 trận thắng liên tiếp, dẫn đầu bảng"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_BOURNE_RAYAN)], "SKY SPORTS", "Tiền đạo Rayan ăn mừng bàn thắng quyết định cho Bournemouth tại Tây Ban Nha"),
            _slot("title", 0, [_url(BBC_BOURNE_ROSE)], "BBC SPORT", "Huấn luyện viên Marco Rose dẫn dắt Bournemouth tạo nên kỳ tích châu Âu"),
            _slot("sentence", 1, [_url(SKY_BOURNE_RAYAN)], "SKY SPORTS", "Bournemouth quật ngã Celta Vigo dù chịu bất lợi quân số từ sớm"),
            _slot("sentence", 2, [_ddgs("Iago Aspas Celta Vigo")], "BING SEARCH", "Iago Aspas mở tỷ số nhưng Celta Vigo không thể bảo toàn lợi thế trước 10 người"),
            _slot("sentence", 3, [_url(BBC_BOURNE_ROSE)], "BBC SPORT", "Bournemouth đi vào lịch sử bóng đá Anh với chuỗi năm trận toàn thắng đầu mùa châu Âu"),
            _slot("sentence", 4, [_url(SKY_BOURNE_RAYAN)], "SKY SPORTS", "Đội bóng nước Anh chạm mốc 10 chiến thắng liên tiếp và tiến sát vòng 16 đội"),
        ],
    },

    # 11 (Nam — AC MILAN LỘI NGƯỢC DÒNG 4-2, JUVENTUS THẮNG ĐẬM 4-1, BENFICA THUA SỐC 0-4)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "UEFA EUROPA LEAGUE",
        "title": "AC Milan lội ngược dòng ngoạn mục 4-2 trên sân Olympiacos, Juventus đại thắng 4-1",
        "summary": (
            "Loạt trận thứ năm Europa League rạng sáng 27 tháng 11 chứng kiến màn lội ngược dòng đầy bản lĩnh của AC Milan khi đánh bại Olympiacos 4-2 ngay tại Athens. "
            "Bị dẫn trước hai bàn sau pha phản lưới của thủ thành Mike Maignan và cú dứt điểm của Jota Silva, đoàn quân của huấn luyện viên Ruben Amorim bùng nổ từ phút 56 nhờ các bàn thắng liên tiếp của Omari Hutchinson, Alphadjo Cisse, Christian Pulisic và Diego Moreira. "
            "Tại Turin, Juventus cũng ngược dòng đè bẹp Omonia Nicosia 4-1 nhờ bốn người lập công khác nhau là Jeff Ekhator, Andrea Cambiaso, Francisco Conceicao và Jeremie Boga để vươn lên nhì bảng với 13 điểm. "
            "Ở chiều ngược lại, cú sốc lớn nhất thuộc về Benfica khi đại diện Bồ Đào Nha thảm bại 0-4 trên sân của Viktoria Plzen."
        ),
        "source": "Dân Trí / UEFA",
        "news_source": "DÂN TRÍ / UEFA",
        "credit": "BING SEARCH",
        "stat_badges": {
            "1": {"label": "EUROPA LEAGUE • ATHENS", "value": "OLYMPIACOS 2-4 AC MILAN", "sub": "Bị dẫn 0-2, Milan ghi liền 4 bàn thắng ngược"},
            "3": {"label": "VƯƠN LÊN NHÌ BẢNG", "value": "JUVENTUS 4-1 OMONIA NICOSIA", "sub": "Bà đầm già đạt 13 điểm sau 5 lượt"},
            "4": {"label": "ĐỊA CHẤN TẠI SÉC", "value": "VIKTORIA PLZEN 4-0 BENFICA", "sub": "Benfica nhận thất bại nặng nề trên sân khách"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("AC Milan team celebration Serie A")], "BING SEARCH", "AC Milan tạo màn ngược dòng ấn tượng với bốn bàn thắng tại Athens"),
            _slot("title", 0, [_ddgs("Juventus players match Allianz Stadium")], "BING SEARCH", "Juventus duy trì vị trí nhì bảng Europa League sau chiến thắng 4-1"),
            _slot("sentence", 1, [_ddgs("Ruben Amorim AC Milan manager football")], "BING SEARCH", "Huấn luyện viên Ruben Amorim giúp AC Milan thắp lại hy vọng đi tiếp"),
            _slot("sentence", 2, [_ddgs("Christian Pulisic AC Milan goal celebration")], "BING SEARCH", "Christian Pulisic tung cú vô lê đẹp mắt đưa AC Milan vượt lên dẫn 3-2"),
            _slot("sentence", 3, [_ddgs("Francisco Conceicao Juventus goal celebration")], "BING SEARCH", "Juventus dễ dàng áp đảo Omonia Nicosia tại sân Allianz"),
            _slot("sentence", 4, [_ddgs("Benfica football team disappointed Champions Europa")], "BING SEARCH", "Benfica gây thất vọng lớn khi thua đậm 0-4 trước Viktoria Plzen"),
        ],
    },

    # 12 (Nữ — CRYSTAL PALACE THẮNG REAL SOCIEDAD 2-1, CELTIC THẮNG PHÚT 85, SUNDERLAND HÒA)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "CÚP CHÂU ÂU",
        "title": "Thomas Frank thắng trận đầu cùng Crystal Palace, Celtic thoát hiểm phút 85",
        "summary": (
            "Tại London rạng sáng 27 tháng 11, huấn luyện viên Thomas Frank giành chiến thắng đầu tiên trên cương vị thuyền trưởng Crystal Palace khi ngược dòng hạ Real Sociedad 2-1 ở Europa League. "
            "Sau khi để Mamadou Sarr chọc thủng lưới và hưởng lợi từ thẻ đỏ của Jon Martin, Jean-Philippe Mateta gỡ hòa trên chấm phạt đền trước khi Dwight McNeil ghi bàn ấn định ở phút 82. "
            "Cùng vòng đấu này, Celtic giữ lại hy vọng đi tiếp nhờ cú đánh đầu phút 85 của cầu thủ vào sân thay người Camilo Duran để thắng Torreense 2-1, trong khi sai lầm chuyền về của Reinildo khiến Sunderland bị Jagiellonia Bialystok cầm hòa 1-1. "
            "Còn tại Conference League, đại diện Scotland là Hearts để thua đáng tiếc 2-3 trước AS Monaco sau bàn quyết định ở phút bù giờ của Folarin Balogun."
        ),
        "source": "Sky Sports / The Guardian",
        "news_source": "SKY SPORTS / THE GUARDIAN",
        "credit": "SKY SPORTS",
        "stat_badges": {
            "1": {"label": "EUROPA LEAGUE", "value": "PALACE 2-1 REAL SOCIEDAD", "sub": "Chiến thắng đầu tay của HLV Thomas Frank"},
            "3": {"label": "NHỊP ĐẬP CÁC ĐỘI ANH-SCOTLAND", "value": "CELTIC 2-1 • SUNDERLAND 1-1", "sub": "Conference League: Hearts thua Monaco 2-3"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_PALACE_FRANK)], "SKY SPORTS", "Crystal Palace có chiến thắng giải tỏa dưới thời tân huấn luyện viên Thomas Frank"),
            _slot("title", 0, [_url(SKY_CELTIC_DURAN)], "SKY SPORTS", "Camilo Duran ghi bàn thắng vàng ở phút 85 cho Celtic tại Bồ Đào Nha"),
            _slot("sentence", 1, [_url(SKY_PALACE_FRANK)], "SKY SPORTS", "Đội chủ sân Selhurst Park ngược dòng đánh bại đại diện Tây Ban Nha Real Sociedad"),
            _slot("sentence", 2, [_ddgs("Jean-Philippe Mateta Crystal Palace celebration")], "BING SEARCH", "Crystal Palace hoàn tất màn ngược dòng ấn tượng ngay trên sân Selhurst Park"),
            _slot("sentence", 3, [_url(SKY_CELTIC_DURAN)], "SKY SPORTS", "Camilo Duran tỏa sáng với pha lập công thứ 15 từ đầu mùa cho Celtic"),
            _slot("sentence", 3, [_url(SKY_SUNDERLAND)], "SKY SPORTS", "Sunderland đánh rơi chiến thắng sau pha mắc lỗi đáng tiếc của Reinildo"),
            _slot("sentence", 4, [_url(SKY_HEARTS_MON)], "SKY SPORTS", "Huấn luyện viên Wouter Vrancken tiếc nuối khi Hearts thua Monaco ở phút bù giờ"),
        ],
    },

    # 13 (Nam — BÁO ĐỘNG ĐỎ TẠI MAN UTD: THỦ MÔN SENNE LAMMENS & 5 THAY ĐỔI CỦA POCHETTINO)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "NGOẠI HẠNG ANH & CHAMPIONS LEAGUE",
        "title": "Báo động đỏ tại Man Utd: Thủ môn Senne Lammens gây lo ngại, Pochettino siết chặt kỷ luật",
        "summary": (
            "Dư âm trận hòa Sporting Lisbon 2-2 khiến thủ môn Senne Lammens trở thành tâm điểm chỉ trích khi truyền thông Anh cảnh báo anh đang lặp lại hình ảnh thiếu ổn định của Andre Onana. "
            "Hai tình huống xử lý lỗi trực tiếp dẫn tới bàn thua tại Bồ Đào Nha nối dài chuỗi sai sót từ trận thua Liverpool 0-4, buộc huấn luyện viên Mauricio Pochettino phải cân nhắc bài toán nhân sự trong khung gỗ. "
            "Dù tuần lễ đầu tiên tại Old Trafford đầy sóng gió, nhà cầm quân người Argentina đã bắt đầu thực hiện năm thay đổi rõ rệt nhằm tái thiết đội bóng. "
            "Ông yêu cầu các cầu thủ nâng cường độ pressing tầm cao, siết chặt cự ly phòng ngự, đẩy mạnh tập thể lực cho nhóm dự bị và khuyến khích tuyến hai xâm nhập vòng cấm."
        ),
        "source": "VnExpress / BBC Sport / Thanh Niên",
        "news_source": "VNEXPRESS / BBC SPORT",
        "credit": "VNEXPRESS / BBC SPORT",
        "stat_badges": {
            "1": {"label": "VỊ TRÍ GÂY LO NGẠI", "value": "LAMMENS MẮC HÀNG LOẠT LỖI", "sub": "Truyền thông Anh đặt dấu hỏi về suất bắt chính"},
            "3": {"label": "DẤU ẤN POCHETTINO", "value": "5 ĐIỀU CHỈNH TẠI OLD TRAFFORD", "sub": "Tăng pressing tầm cao và cường độ tập luyện"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_MU_LAMMENS)], "THANH NIÊN / AFP", "Thủ thành Senne Lammens hứng chịu nhiều chỉ trích sau các sai lầm liên tiếp"),
            _slot("title", 0, [_url(VNE_MU_POCH)], "VNEXPRESS / AP", "Huấn luyện viên Mauricio Pochettino đối mặt nhiều thử thách ngay tuần đầu tại Man Utd"),
            _slot("sentence", 1, [_url(BBC_MU_LAMMENS)], "BBC SPORT", "Phong độ của Senne Lammens khiến ban huấn luyện Man Utd không khỏi lo lắng"),
            _slot("sentence", 2, [_url(TN_MU_LAMMENS)], "THANH NIÊN / AFP", "Sai lầm trong khung gỗ làm hỏng công sức hàng công của Quỷ đỏ tại Champions League"),
            _slot("sentence", 3, [_url(VNE_MU_POCH)], "VNEXPRESS / AP", "Mauricio Pochettino từng bước áp dụng triết lý mới tại sân Old Trafford"),
            _slot("sentence", 4, [_url(VNE_MU_LIS)], "VNEXPRESS / AP", "Các cầu thủ Man Utd được yêu cầu gây áp lực đồng bộ và quyết liệt hơn"),
        ],
    },

    # 14 (Nữ — 4 ÔNG LỚN NGOẠI HẠNG ANH BẮT TAY KIỆN MAN CITY ĐÒI BỒI THƯỜNG)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "NGOẠI HẠNG ANH",
        "title": "Bốn ông lớn Ngoại hạng Anh thuê luật sư chuẩn bị kiện đòi bồi thường Man City",
        "summary": (
            "Theo tiết lộ từ báo giới Anh, Manchester United, Liverpool và Tottenham vừa cùng thuê chung hãng luật chuyên ngành Wiggin để chuẩn bị hồ sơ khởi kiện đòi Manchester City bồi thường thiệt hại hàng trăm triệu bảng. "
            "Trong khi đó, Arsenal cũng làm việc với hãng luật riêng HFS Kramer nhằm theo đuổi vụ kiện độc lập liên quan đến những cáo buộc vi phạm quy tắc tài chính của đội chủ sân Etihad. "
            "Các câu lạc bộ thậm chí đã sử dụng chung nhóm chuyên gia phân tích tài chính để tính toán tổn thất từ các danh hiệu và doanh thu bị ảnh hưởng qua nhiều mùa giải. "
            "Sức ép pháp lý bủa vây giữa lúc Man City đang sa sút chuyên môn khi chỉ giành đúng một điểm qua bốn vòng Ngoại hạng Anh gần nhất dưới thời huấn luyện viên Enzo Maresca."
        ),
        "source": "The Guardian Sport / VnExpress",
        "news_source": "THE GUARDIAN / VNEXPRESS",
        "credit": "VNEXPRESS / THE GUARDIAN",
        "stat_badges": {
            "1": {"label": "SÓNG GIÓ PHÁP LÝ", "value": "4 ÔNG LỚN KIỆN MAN CITY", "sub": "MU, Liverpool, Spurs dùng chung hãng luật Wiggin"},
            "4": {"label": "PHONG ĐỘ SA SÚT", "value": "1 ĐIỂM / 4 VÒNG GẦN NHẤT", "sub": "Hàng thủ Man City thủng lưới 20 bàn sau 10 trận"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Premier League Manchester City Etihad Stadium trophy")], "BING SEARCH", "Bốn đội bóng lớn Ngoại hạng Anh chuẩn bị kịch bản kiện đòi Man City bồi thường"),
            _slot("title", 0, [_url(VNE_MC_HAALAND)], "VNEXPRESS / AP", "Manchester City vừa đối mặt áp lực pháp lý vừa sa sút phong độ trên sân cỏ"),
            _slot("sentence", 1, [_ddgs("Manchester United Liverpool Premier League match")], "BING SEARCH", "Manchester United, Liverpool và Tottenham cùng hợp tác về mặt pháp lý"),
            _slot("sentence", 2, [_ddgs("Arsenal Emirates Stadium Premier League")], "BING SEARCH", "Arsenal thuê hãng luật HFS Kramer theo đuổi hồ sơ yêu cầu bồi thường riêng"),
            _slot("sentence", 3, [_url(VNE_MC_HAALAND)], "VNEXPRESS / AP", "Erling Haaland và đồng đội vừa trải qua trận hòa 2-2 thất vọng trước Napoli"),
            _slot("sentence", 4, [_url(VNE_MC_MARESCA)], "VNEXPRESS / AFP", "Huấn luyện viên Enzo Maresca phải tìm cách chặn đà sa sút của hàng thủ Man City"),
        ],
    },

    # 15 (Nam — HLV XABI ALONSO XÁC NHẬN WESLEY FOFANA ĐÃ XIN LỖI TẠI CHELSEA)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "NGOẠI HẠNG ANH",
        "title": "HLV Xabi Alonso xác nhận Wesley Fofana đã xin lỗi sau cuộc phỏng vấn gây bão tại Chelsea",
        "summary": (
            "Trước chuyến làm khách trên sân Nottingham Forest, huấn luyện viên trưởng Chelsea Xabi Alonso xác nhận trung vệ Wesley Fofana đã gửi lời xin lỗi chính thức tới toàn đội. "
            "Cầu thủ người Pháp hứng chịu làn sóng chỉ trích dữ dội từ người hâm mộ khi tự ý thực hiện cuộc phỏng vấn dài hai giờ trên YouTube ngay sau trận Chelsea thua đậm kình địch Leeds United 1-4. "
            "Trong buổi trò chuyện không được câu lạc bộ cấp phép này, Fofana thậm chí còn đùa cợt về cú đá luân lưu hỏng của bản thân trong thất bại trước Liverpool tại Cúp Liên đoàn. "
            "Ông Xabi Alonso khẳng định ban huấn luyện đã xử lý nội bộ nghiêm túc, đồng thời tuyên bố khép lại sự việc để toàn đội tập trung cho chặng đường sắp tới."
        ),
        "source": "BBC Sport / Sky Sports",
        "news_source": "BBC SPORT / SKY SPORTS",
        "credit": "BBC SPORT / SKY SPORTS",
        "stat_badges": {
            "1": {"label": "CHELSEA LẬP LẠI KỶ CƯƠNG", "value": "FOFANA XIN LỖI NỘI BỘ", "sub": "HLV Xabi Alonso tuyên bố khép lại ồn ào"},
            "2": {"label": "NGUỒN CƠN CHỈ TRÍCH", "value": "PHỎNG VẤN YOUTUBE KHÔNG PHÉP", "sub": "Xảy ra ngay sau thất bại 1-4 trước Leeds"},
        },
        "slots": [
            _slot("title", 0, [_url(BBC_CHELSEA_FOF)], "BBC SPORT", "Wesley Fofana vấp phải phản ứng gay gắt từ cổ động viên Chelsea"),
            _slot("title", 0, [_ddgs("Xabi Alonso press conference manager")], "BING SEARCH", "Huấn luyện viên Xabi Alonso thẳng thắn chấn chỉnh kỷ luật phòng thay đồ"),
            _slot("sentence", 1, [_url(SKY_CHELSEA_FOF)], "SKY SPORTS", "Xabi Alonso xác nhận trung vệ người Pháp nhận thức được sai lầm"),
            _slot("sentence", 2, [_url(BBC_CHELSEA_FOF)], "BBC SPORT", "Cuộc phỏng vấn tự phát khiến Fofana chịu sức ép lớn sau trận thua Leeds"),
            _slot("sentence", 3, [_ddgs("Chelsea football Stamford Bridge fans")], "BING SEARCH", "Nội dung đùa cợt về thất bại ở Cúp Liên đoàn khiến người hâm mộ Chelsea phẫn nộ"),
            _slot("sentence", 4, [_ddgs("Xabi Alonso coach touchline football")], "BING SEARCH", "Chelsea cần nhanh chóng ổn định tâm lý trước cuộc đối đầu Nottingham Forest"),
        ],
    },

    # 16 (Nữ — TRỌNG TÀI AFC CHAMPIONS LEAGUE TWO BÁC BỎ CÁO BUỘC SAY XỈN KHI BỊ THAY GIỮA TRẬN)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "BÓNG ĐÁ CHÂU Á",
        "title": "Trọng tài AFC Champions League Two bác bỏ cáo buộc say xỉn sau khi bị thay giữa trận",
        "summary": (
            "Một sự cố hy hữu vừa gây xôn xao tại AFC Champions League Two khi trọng tài người Syria Hanna Hattab bất ngờ bị thay thế ngay sau giờ nghỉ giữa hai hiệp trận đấu giữa Gol Gohar và Al Jazira. "
            "Sau hàng loạt quyết định gây tranh cãi ở hiệp một, một số thành viên phía câu lạc bộ Iran cho rằng vị vua áo đen không ở trạng thái bình thường, làm bùng lên tin đồn ông bị say rượu trên mạng xã hội. "
            "Trọng tài thứ tư đã phải vào sân điều hành phần còn lại của trận đấu với chiến thắng chung cuộc thuộc về đại diện Các Tiểu vương quốc Ả Rập Thống nhất. "
            "Ngay sau đó, ông Hanna Hattab cùng giới chức liên đoàn bác bỏ hoàn toàn tin đồn vô căn cứ này và tuyên bố sẵn sàng khởi kiện vì hành vi bôi nhọ danh dự."
        ),
        "source": "BBC Sport",
        "news_source": "BBC SPORT",
        "credit": "BING SEARCH",
        "stat_badges": {
            "1": {"label": "SỰ CỐ CÚP C2 CHÂU Á", "value": "THAY TRỌNG TÀI GIỮA HIỆP", "sub": "Trận Gol Gohar vs Al Jazira gây xôn xao"},
            "4": {"label": "PHẢN ỨNG CHÍNH THỨC", "value": "BÁC BỎ TIN ĐỒN SAY XỈN", "sub": "Trọng tài Hanna Hattab dọa khởi kiện"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("football referee stadium match")], "BING SEARCH", "Trọng tài Syria Hanna Hattab trở thành tâm điểm tranh cãi tại AFC Champions League Two"),
            _slot("title", 0, [_ddgs("Asian Champions League football referee")], "BING SEARCH", "Quyết định thay trọng tài ở giờ nghỉ giữa hai hiệp làm dấy lên nhiều đồn đoán"),
            _slot("sentence", 1, [_ddgs("AFC Champions League football match stadium")], "BING SEARCH", "Trận đấu giữa đại diện Iran và câu lạc bộ UAE chứng kiến sự cố hiếm gặp"),
            _slot("sentence", 2, [_ddgs("football referee red yellow card argument")], "BING SEARCH", "Những tiếng còi gây tranh cãi ở hiệp một khiến cầu thủ và ban huấn luyện phản ứng"),
            _slot("sentence", 3, [_ddgs("Al Jazira UAE football club match")], "BING SEARCH", "Trọng tài thứ tư tiếp quản trận đấu trong hiệp hai khi Al Jazira giành thắng lợi"),
            _slot("sentence", 4, [_ddgs("Hanna Hattab referee AFC")], "BING SEARCH", "Giới chức khẳng định cáo buộc say rượu là hoàn toàn bịa đặt và vô căn cứ"),
        ],
    },

    # 17 (Nam — JANNIK SINNER PHẪU THUẬT ĐẦU GỐI, LỠ HẸN AUSTRALIAN OPEN 2027)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "QUẦN VỢT THẾ GIỚI",
        "title": "Cú sốc quần vợt: Jannik Sinner phẫu thuật đầu gối, chính thức lỡ hẹn Australian Open 2027",
        "summary": (
            "Làng banh nỉ thế giới đón nhận thông tin gây sốc khi tay vợt số hai thế giới Jannik Sinner chính thức rút lui khỏi Grand Slam đầu năm Australian Open 2027. "
            "Giám đốc điều hành Liên đoàn Quần vợt Australia ông Andrew Abdo xác nhận đội ngũ của ngôi sao người Italy đã thông báo anh không kịp bình phục cho giải đấu khởi tranh ngày 17 tháng 1 tại Melbourne. "
            "Kể từ sau khi bảo vệ thành công danh hiệu Wimbledon hồi tháng bảy, Sinner bị hành hạ bởi chấn thương gân đầu gối phải và vừa phải tiến hành ca tiểu phẫu tại Phần Lan hôm 24 tháng 11. "
            "Theo truyền thông Italy, nhà vô địch Australian Open hai lần liên tiếp năm 2024 và 2025 có thể cần từ ba đến bốn tháng hồi phục trước khi trở lại sân cứng."
        ),
        "source": "The Guardian Sport",
        "news_source": "THE GUARDIAN SPORT",
        "credit": "BING SEARCH",
        "stat_badges": {
            "1": {"label": "AUSTRALIAN OPEN 2027", "value": "JANNIK SINNER VẮNG MẶT", "sub": "BTC Melbourne xác nhận hôm 26/11"},
            "3": {"label": "CA PHẪU THUẬT TẠI PHẦN LAN", "value": "NGHỈ THI ĐẤU 3 ĐẾN 4 THÁNG", "sub": "Chấn thương đầu gối phải dai dẳng từ tháng 7"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Jannik Sinner Australian Open champion trophy")], "BING SEARCH", "Jannik Sinner từng hai lần vô địch Australian Open liên tiếp vào các năm 2024 và 2025"),
            _slot("title", 0, [_ddgs("Jannik Sinner Wimbledon forehand action")], "BING SEARCH", "Tay vợt người Italy không thi đấu kể từ sau chức vô địch Wimbledon"),
            _slot("sentence", 1, [_ddgs("Jannik Sinner Melbourne Park tennis")], "BING SEARCH", "Người hâm mộ tại Melbourne sẽ thiếu vắng một trong những ứng viên nặng ký nhất"),
            _slot("sentence", 2, [_ddgs("Australian Open Rod Laver Arena stadium")], "BING SEARCH", "Ban tổ chức Australian Open gửi lời chúc Sinner sớm bình phục cho mùa giải 2028"),
            _slot("sentence", 3, [_ddgs("Jannik Sinner knee injury tennis match")], "BING SEARCH", "Phương pháp điều trị bảo tồn không hiệu quả buộc Sinner phải lên bàn mổ"),
            _slot("sentence", 4, [_ddgs("Jannik Sinner tennis player portrait")], "BING SEARCH", "Ngôi sao 25 tuổi dự kiến trở lại vào giai đoạn sân cứng mùa xuân năm sau"),
        ],
    },

    # 18 (Nữ — DAVIS CUP 2026: TUYỂN ANH LỘI NGƯỢC DÒNG HẠ ĐỨC 2-1 VÀO BÁN KẾT)
    {
        "id": 18,
        "art_id": "art_18",
        "group": "QUẦN VỢT DAVIS CUP",
        "title": "Davis Cup 2026: Tuyển Anh ngược dòng hạ Đức 2-1, lần đầu vào bán kết sau bảy năm",
        "summary": (
            "Tại vòng tứ kết Davis Cup Final 8 diễn ra ở Bologna đêm 26 tháng 11, đội tuyển quần vợt Vương quốc Anh xuất sắc đánh bại Đức với tỷ số 2-1 để giành quyền vào bán kết lần đầu tiên kể từ năm 2019. "
            "Cameron Norrie mở màn thuận lợi bằng chiến thắng sau ba set kịch tính trước Jan-Lennard Struff, trước khi tay vợt số một thế giới Alexander Zverev hạ gục Arthur Fery để quân bình tỷ số 1-1 cho tuyển Đức. "
            "Trận đấu buộc phải định đoạt bằng màn so tài đôi nam quyết định, nơi cặp Henry Patten và Neal Skupski chơi thăng hoa đánh bại Kevin Krawietz và Tim Puetz 6-2, 7-6. "
            "Chiến thắng nghẹt thở ở loạt tie-break set hai giúp tuyển Anh khép lại bảy năm chờ đợi để tiến vào nhóm bốn đội mạnh nhất giải."
        ),
        "source": "BBC Sport",
        "news_source": "BBC SPORT",
        "credit": "BING SEARCH",
        "stat_badges": {
            "1": {"label": "TỨ KẾT DAVIS CUP", "value": "ANH THẮNG ĐỨC 2-1", "sub": "Lần đầu vào bán kết kể từ năm 2019"},
            "3": {"label": "TRẬN ĐÔI QUYẾT ĐỊNH", "value": "PATTEN / SKUPSKI THẮNG 2-0", "sub": "Vượt qua Krawietz / Puetz với tỷ số 6-2, 7-6"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Neal Skupski Henry Patten tennis Davis Cup")], "BING SEARCH", "Henry Patten và Neal Skupski mang về điểm số quyết định cho tuyển Anh tại Bologna"),
            _slot("title", 0, [_ddgs("Cameron Norrie Great Britain Davis Cup tennis")], "BING SEARCH", "Cameron Norrie giành chiến thắng mở màn quan trọng trước Jan-Lennard Struff"),
            _slot("sentence", 1, [_ddgs("Great Britain Davis Cup tennis team celebration")], "BING SEARCH", "Đội tuyển Anh vỡ òa khi trở lại bán kết Davis Cup sau bảy năm"),
            _slot("sentence", 2, [_ddgs("Alexander Zverev Germany Davis Cup tennis")], "BING SEARCH", "Alexander Zverev thắng chóng vánh trận đơn thứ hai để níu giữ hy vọng cho Đức"),
            _slot("sentence", 3, [_ddgs("Henry Patten Neal Skupski tennis")], "BING SEARCH", "Bộ đôi Patten và Skupski thể hiện bản lĩnh ở loạt tie-break cân não"),
            _slot("sentence", 4, [_ddgs("Great Britain Davis Cup tennis")], "BING SEARCH", "Vương quốc Anh tiếp tục hành trình chinh phục chiếc cúp bạc danh giá tại Italy"),
        ],
    },

    # 19 (Nam — CHUNG KẾT CỜ VUA THẾ GIỚI 2026: SINDAROV THOÁT HIỂM TRONG VÁN 3 GẦN 5 GIỜ)
    {
        "id": 19,
        "art_id": "art_19",
        "group": "CỜ VUA THẾ GIỚI",
        "title": "Chung kết Cờ vua Thế giới 2026: Sindarov thoát hiểm nghẹt thở trong ván 3 gần 5 giờ trước Gukesh",
        "summary": (
            "Sau hai ván mở màn êm ả, trận Chung kết Cờ vua Thế giới 2026 tại Thụy Sĩ thực sự bùng nổ ở ván thứ ba đêm 26 tháng 11 với màn đấu trí căng thẳng kéo dài gần năm giờ đồng hồ. "
            "Cầm quân đen đối đầu người thách đấu Javokhir Sindarov, đương kim vô địch Gukesh Dommaraju gây bất ngờ ngay từ nước thứ năm trong khai cuộc Berlin, tạo ra lợi thế thời gian lên tới gần 40 phút. "
            "Ở thời điểm ngặt nghèo nhất khi đồng hồ chỉ còn đúng tám giây trước giờ kiểm tra nước thứ 40, đại kiện tướng Uzbekistan vẫn phòng ngự chính xác để giữ lại thế cân bằng sau 60 nước đi. "
            "Kết quả hòa thứ ba liên tiếp đưa tổng tỷ số trận tranh ngôi vương quỹ thưởng 2,5 triệu USD về mức 1,5 - 1,5 trước ngày nghỉ đầu tiên hôm nay."
        ),
        "source": "The Guardian Sport / FIDE",
        "news_source": "THE GUARDIAN / FIDE",
        "credit": "BING SEARCH",
        "stat_badges": {
            "1": {"label": "VÁN 3 TẠI THỤY SĨ", "value": "HÒA SAU 60 NƯỚC • 4H49P", "sub": "Ván đấu căng thẳng nhất từ đầu trận"},
            "4": {"label": "TỔNG TỶ SỐ TẠM THỜI", "value": "GUKESH 1,5 - 1,5 SINDAROV", "sub": "Bước vào ngày nghỉ đầu tiên hôm 27/11"},
        },
        "slots": [
            _slot("title", 0, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_1.jpg"))], "BING SEARCH", "Đương kim vô địch Gukesh Dommaraju tạo áp lực lớn ngay từ khai cuộc ván ba"),
            _slot("title", 0, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_2.jpg"))], "BING SEARCH", "Javokhir Sindarov đối mặt áp lực thời gian cực lớn ở trung cuộc"),
            _slot("sentence", 1, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_3.jpg"))], "BING SEARCH", "Hai kỳ thủ trẻ cống hiến ván cờ kéo dài gần năm giờ tại Geneva"),
            _slot("sentence", 2, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_5.jpg"))], "BING SEARCH", "Lựa chọn biến thể sắc bén giúp Gukesh dẫn trước đối thủ rất nhiều thời gian"),
            _slot("sentence", 3, [_local(str(ROOT / "outputs" / "25.11.2026" / "images" / "Tin_23_6.jpg"))], "BING SEARCH", "Sindarov thoát hiểm ở ngưỡng tám giây cuối cùng để chia điểm sau 60 nước"),
            _slot("sentence", 4, [_ddgs("FIDE World Chess Championship match board")], "BING SEARCH", "Hai kỳ thủ tạm nghỉ ngày 27 tháng 11 trước khi Gukesh cầm quân trắng ở ván bốn"),
        ],
    },

    # 20 (Nữ — CĂNG THẲNG NỘI BỘ FERRARI TRƯỚC QATAR GP & MÀN ĐÁP TRẢ CỦA RUSSELL)
    {
        "id": 20,
        "art_id": "art_20",
        "group": "FORMULA 1 • QATAR GP",
        "title": "Nội bộ Ferrari sóng gió trước Qatar GP: Hamilton cảnh báo thử thách lớn, Leclerc phủ nhận đặc quyền",
        "summary": (
            "Trước thềm chặng áp chót Qatar Grand Prix cuối tuần này, Lewis Hamilton thừa nhận Ferrari đang trải qua giai đoạn vô cùng thử thách sau hàng loạt va chạm trên đường đua với đồng đội Charles Leclerc. "
            "Hồi cuối tuần trước tại Las Vegas, tay đua người Monaco bị phạt 10 giây vì gây ra cú va chạm khi tấn công Hamilton, buộc cả hai phải tổ chức cuộc họp đối thoại thẳng thắn. "
            "Chia sẻ với truyền thông, Charles Leclerc khẳng định hợp đồng của anh không có điều khoản ưu tiên tay đua số một và cả hai vẫn được tự do cạnh tranh sòng phẳng. "
            "Ở một diễn biến khác tại đường đua Losail, tay đua Mercedes George Russell tỏ ra điềm tĩnh và gọi những lời chỉ trích từ Max Verstappen sau chặng Las Vegas là khá hài hước."
        ),
        "source": "BBC Sport / Sky Sports",
        "news_source": "BBC SPORT / SKY SPORTS",
        "credit": "SKY SPORTS / BBC SPORT",
        "stat_badges": {
            "1": {"label": "TRƯỚC CHẶNG QATAR GP", "value": "FERRARI ĐỐI THOẠI NỘI BỘ", "sub": "Sau va chạm giữa Leclerc & Hamilton ở Las Vegas"},
            "4": {"label": "KHẨU CHIẾN F1", "value": "RUSSELL ĐÁP TRẢ VERSTAPPEN", "sub": "Khẳng định không cần làm bạn thân trên đường đua"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_F1_FERRARI)], "SKY SPORTS", "Charles Leclerc và Lewis Hamilton đối thoại thẳng thắn trước chặng Qatar GP"),
            _slot("title", 0, [_url(BBC_F1_RUSSELL)], "BBC SPORT", "George Russell giữ thái độ điềm tĩnh trước lời chỉ trích từ Max Verstappen"),
            _slot("sentence", 1, [_url(SKY_F1_FERRARI)], "SKY SPORTS", "Lewis Hamilton cảnh báo những khó khăn hiện tại trong nội bộ đội đua Ferrari"),
            _slot("sentence", 2, [_ddgs("Ferrari F1 car Las Vegas Grand Prix night")], "BING SEARCH", "Án phạt 10 giây ở Las Vegas khiến mối quan hệ hai tay lái Ferrari bị soi xét kỹ"),
            _slot("sentence", 3, [_url(SKY_F1_FERRARI)], "SKY SPORTS", "Leclerc phủ nhận tin đồn được ưu tiên hơn Hamilton trong đội đua Italy"),
            _slot("sentence", 4, [_url(BBC_F1_RUSSELL)], "BBC SPORT", "George Russell và Max Verstappen tiếp tục tâm điểm chú ý bên ngoài đường đua"),
        ],
    },

    # 21 (Nam — NFL LỄ TẠ ƠN KỊCH TÍNH: CHICAGO BEARS HẠ DETROIT LIONS Ở 3 GIÂY CUỐI)
    {
        "id": 21,
        "art_id": "art_21",
        "group": "BÓNG BẦU DỤC MỸ NFL",
        "title": "NFL Lễ Tạ Ơn kịch tính: Chicago Bears ngược dòng hạ Detroit Lions ở 3 giây cuối",
        "summary": (
            "Trận đấu truyền thống dịp Lễ Tạ Ơn giải NFL rạng sáng 27 tháng 11 khép lại theo kịch bản không tưởng khi Chicago Bears đánh bại Detroit Lions 39-35 đúng ba giây trước khi hết giờ. "
            "Dù để Detroit dẫn trước suốt hơn 53 phút và bị bỏ xa tới 11 điểm trong hiệp cuối sau pha bứt tốc ghi điểm 70 yard của Jahmyr Gibbs, đội khách vẫn không bỏ cuộc. "
            "Tiền vệ Caleb Williams tung đường chuyền quyết định cho Rome Odunze bắt bóng sát vạch cuối sân để hoàn tất cú lội ngược dòng, đưa Bears vươn lên chiếm ngôi đầu bảng NFC North. "
            "Ở một diễn biến khác của NFL, chủ sở hữu Pittsburgh Steelers Art Rooney lên tiếng bảo vệ huấn luyện viên Mike McCarthy và chỉ trích thái độ thiếu kỷ luật của Aaron Rodgers."
        ),
        "source": "Sky Sports / The Guardian Sport",
        "news_source": "SKY SPORTS / THE GUARDIAN",
        "credit": "SKY SPORTS",
        "stat_badges": {
            "1": {"label": "NFL LỄ TẠ ƠN", "value": "BEARS THẮNG LIONS 39-35", "sub": "Ghi touchdown quyết định ở 3 giây cuối"},
            "3": {"label": "NGÔI ĐẦU NFC NORTH", "value": "ROME ODUNZE LẬP CÚ ĐÚP", "sub": "Nối dài mạch 6 trận thắng của Chicago Bears"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_NFL_BEARS)], "SKY SPORTS", "Rome Odunze thực hiện pha bắt bóng quyết định ở ba giây cuối cho Chicago Bears"),
            _slot("title", 0, [_ddgs("Caleb Williams Chicago Bears quarterback NFL")], "BING SEARCH", "Caleb Williams dẫn dắt Chicago Bears chiếm ngôi đầu bảng NFC North"),
            _slot("sentence", 1, [_url(SKY_NFL_BEARS)], "SKY SPORTS", "Khoảnh khắc vỡ òa của Chicago Bears trong trận cầu nghẹt thở dịp Lễ Tạ Ơn"),
            _slot("sentence", 2, [_ddgs("Detroit Lions Jahmyr Gibbs NFL running back")], "BING SEARCH", "Detroit Lions đánh rơi chiến thắng dù dẫn trước tới 11 điểm ở hiệp bốn"),
            _slot("sentence", 3, [_url(SKY_NFL_BEARS)], "SKY SPORTS", "Chiến thắng thứ sáu liên tiếp giúp Chicago Bears tạo bước ngoặt lớn mùa giải"),
            _slot("sentence", 4, [_ddgs("Pittsburgh Steelers Mike McCarthy NFL coach")], "BING SEARCH", "Chủ sở hữu Steelers công khai ủng hộ Mike McCarthy sau ồn ào với Aaron Rodgers"),
        ],
    },

    # 22 (100% Giọng Nữ — MỤC TIN VẮN CUỐI VIDEO: CÁC TIN THỂ THAO KHÁC)
    {
        "id": 22,
        "art_id": "art_22",
        "group": "CÁC TIN THỂ THAO KHÁC",
        "title": "Điểm nhanh các tin thể thao đáng chú ý khác",
        "voice_preset": "secondary",
        "summary": (
            "Tại đấu trường quốc nội, môn điền kinh Đại hội Thể thao toàn quốc 2026 sáng nay chứng kiến ngôi sao Nguyễn Thị Oanh bước vào thi đấu chung kết nội dung 3000m chướng ngại vật nữ lúc 9 giờ 40, trong khi đội U21 Thành phố Hồ Chí Minh thua đậm U21 Quân Đội ở trận ra quân bóng đá nam. "
            "Cũng tại Đại hội, môn xe đạp đường trường gây tranh cãi trên nhiều diễn đàn khi tay đua Trần Trọng Phúc chủ động phanh lại sát vạch đích để nhường đồng đội Nguyễn Hướng vượt lên giành điểm cạnh tranh huy chương đồng. "
            "Ở bóng đá nữ thế giới, tuyển thủ Đức Laura Freigang vừa nhận án cấm thi đấu 16 tháng vì liên quan tới ba lần vi phạm quy trình kiểm tra doping. "
            "Tại đấu trường châu Âu, trận Besiktas gặp câu lạc bộ Israel Hapoel Be'er-Sheva ở Europa League bị gián đoạn và làm dấy lên căng thẳng ngoại giao giữa Thổ Nhĩ Kỳ và Georgia sau sự cố biểu ngữ trên khán đài. "
            "Cùng lúc, Quốc hội Mỹ đã gửi thư triệu tập một số nhân viên FIFA để điều tra dự án thương mại gây tranh cãi FIFA Forward Enterprise của chủ tịch Gianni Infantino. "
            "Khép lại bản tin, ở môn snooker, nhà vô địch thế giới bốn lần Mark Selby chuẩn bị mở màn hành trình bảo vệ danh hiệu UK Championship bằng cuộc chạm trán đầy thử thách trước Matt Selt tại York."
        ),
        "source": "Tuổi Trẻ / BBC Sport / The Guardian",
        "news_source": "ĐIỂM ĐỌC TỔNG HỢP",
        "credit": "TUỔI TRẺ / THE GUARDIAN",
        "stat_badges": {
            "1": {"label": "ĐẠI HỘI TDTT 2026", "value": "NGUYỄN THỊ OANH XUẤT TRẬN", "sub": "Chung kết 3000m vượt chướng ngại vật sáng 27/11"},
            "3": {"label": "ÁN PHẠT DOPING", "value": "LAURA FREIGANG BỊ CẤM 16 THÁNG", "sub": "Tuyển thủ nữ Đức vi phạm 3 lần kiểm tra"},
            "6": {"label": "SNOOKER UK CHAMPIONSHIP", "value": "MARK SELBY BẢO VỆ NGÔI VƯƠNG", "sub": "Mở màn gặp Matt Selt tại York cuối tuần này"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_OANH)], "TUỔI TRẺ / TTO", "Nguyễn Thị Oanh bước vào tranh tài chung kết điền kinh sáng 27 tháng 11"),
            _slot("title", 0, [_url(TT_U21_QD)], "TUỔI TRẺ / ANH KHOA", "U21 Quân Đội khởi đầu ấn tượng trước U21 Thành phố Hồ Chí Minh"),
            _slot("title", 0, [_url(TT_XE_DAP)], "TUỔI TRẺ / HUY PHẠM", "Tình huống nhường đồng đội gây tranh cãi ở môn xe đạp đường trường"),
            # Câu 1: Nguyễn Thị Oanh & U21 Quân Đội
            _slot("sentence", 1, [_url(TT_OANH)], "TUỔI TRẺ / TTO", "Nguyễn Thị Oanh được kỳ vọng giành huy chương vàng đầu tiên tại Đại hội 2026"),
            _slot("sentence", 1, [_url(TT_U21_QD)], "TUỔI TRẺ / ANH KHOA", "Hoàng Công Hậu và U21 Quân Đội thắng đậm trong ngày ra quân bảng A"),
            # Câu 2: Xe đạp Trần Trọng Phúc
            _slot("sentence", 2, [_url(TT_XE_DAP)], "TUỔI TRẺ / HUY PHẠM", "Pha giảm tốc sát vạch đích của Trần Trọng Phúc tạo nhiều ý kiến trái chiều"),
            # Câu 3: Laura Freigang
            _slot("sentence", 3, [_ddgs("Laura Freigang Germany women football")], "BING SEARCH", "Tiền đạo Laura Freigang nhận án treo giò 16 tháng vì lỗi quy trình kiểm tra"),
            # Câu 4: Besiktas vs Hapoel
            _slot("sentence", 4, [_ddgs("Besiktas stadium fans Europa League football")], "BING SEARCH", "Cảnh sát Georgia và cổ động viên Besiktas xảy ra xô xát quanh biểu ngữ trên khán đài"),
            # Câu 5: FIFA Infantino investigation
            _slot("sentence", 5, [_ddgs("Gianni Infantino FIFA president conference")], "BING SEARCH", "Ủy ban Tư pháp Hạ viện Mỹ mở cuộc điều tra liên quan dự án thương mại của FIFA"),
            # Câu 6: Mark Selby snooker
            _slot("sentence", 6, [_ddgs("Mark Selby snooker UK Championship trophy")], "BING SEARCH", "Nhà đương kim vô địch Mark Selby đối đầu thử thách mang tên Matt Selt tại York"),
        ],
    },
]
