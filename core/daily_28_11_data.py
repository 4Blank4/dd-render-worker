# -*- coding: utf-8 -*-
"""
daily_28_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 28.11.2026
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


# ── URL ảnh báo chí sạch gốc 27–28.11.2026 (Việt Nam & Thế giới) ──

# 1. V-League vòng 9 & Bóng đá Việt Nam
TN_ND_CAHN_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/photo-1795790226871-17957902277051494171577.jpeg"
TN_ND_CAHN_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/nam-dinh-cahn-2-17957824550531721103327.jpg"
TN_ND_CAHN_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/nam-dinh-cahn-1-17957824550161892782924.jpg"
TN_CAIO_ND = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/caio-cesar-clb-17957830789061316937783.jpg"
DT_ND_CAHN_1 = "https://cdnphoto.dantri.com.vn/mo-VaxbAkUwqX44wE3TimZ1dRxk=/thumb_w/1020/2026/11/27/clb-cahn-6-1795786652453.jpg"
DT_ND_CAHN_HAU = "https://cdnphoto.dantri.com.vn/JACHAxvDOFiIP1PAANqDzsHoCbU=/thumb_w/1020/2026/11/27/doan-van-hau-2-edited-1795786736894.jpg"
DT_ND_CAHN_3 = "https://cdnphoto.dantri.com.vn/bfn6X-s1sUsvSs--xTl_NFcB0Y0=/thumb_w/1020/2026/11/27/clb-cahn3-1795786651212.jpg"
TT_ND_CAHN = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/17957789894978973244394868833818g140387812580018941482a0a503a9ef1bc547649664d1560062-17957790244711030981136-262-0-1334-2048-crop-1795779119676735757495.jpg"

TT_QUANGHAI = "https://cdn2.tuoitre.vn/471584752817336320/2026/8/10/quang-hai-1786362402265391573806.jpeg"
TN_SLNA_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/slna-1-0-ninh-binh-minh-tu-1795783396948696439306.jpg"
TN_SLNA_LUIZ = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/93468941632713359865902995624027485904900745n-1795781131146469245370.jpg"
TN_SLNA_JOY = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/92822474917255932891633764344148380866920955n-17957811310681148671397.jpg"
VNE_SLNA_GOAL = "https://i1-thethao.vnecdn.net/2026/11/27/1795779805487-g428685043937662-7204-5890-1795788270.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=FS07jfXGGRyZhAP435q8yA"
VNE_SLNA_LAM = "https://i1-thethao.vnecdn.net/2026/11/27/1795779805487-4284159376153925-1837-3236-1795788269.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=etr_n87M-d9WOPlTiSEEjQ"
VNE_HOANGDUC = "https://i1-thethao.vnecdn.net/2026/11/27/1795779331727-g428685043937662-8665-9123-1795788270.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=ydex2zO_nBoV3t0cEsWcwg"
TT_SLNA_2 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/slna-2-17957853115241747303936.jpeg"

TN_VL_DANANG = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/4-32-1795793660697948670595.jpg"
TN_VL_CATPHCM = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/10-4-1920x1280-17957937507731565091844.jpg"
TN_VL_HANOI = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/bia-42-17957938283391281419369.jpg"

# 2. U17 World Cup 2026 & Bóng đá trẻ
TN_U17_MALI_FIG = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/photo-1795790008079-1795790008811419098812.jpeg"
TN_U17_LUC_10 = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/photo-1795789776540-17957897780001026102775.jpeg"
VNE_U17_LUC = "https://i1-thethao.vnecdn.net/2026/11/27/img-1795754320-3633-1795754484.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=MmyAI42KyNAb_W8E5NqJew"
VNE_U17_LUC_2 = "https://i1-thethao.vnecdn.net/2026/11/27/img-1795754476-7715-1795754484.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=wDJGPFv0m796SKXC2gt9kw"
VNE_U17_KHOA = "https://i1-thethao.vnecdn.net/2026/11/27/7-2638-1795754484.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=c8W3bNG12aXjfpreMkbKLg"
DT_U17_1 = "https://cdnphoto.dantri.com.vn/E0NEFCCaC_3xnxOlNe8eq5RFKu4=/thumb_w/980/2026/11/28/u17-vietnam-1795701658290-1795799615709.jpg"
DT_U17_2 = "https://cdnphoto.dantri.com.vn/Fauc3hBtt-n3lrxKdDxUsrlf7IU=/thumb_w/980/2026/11/28/u17-vietnam-11-1795706175637-1795799663462.jpg"
DT_ROLAND = "https://cdnphoto.dantri.com.vn/8QMZSVISLGClNI5yai9TukUEIMY=/thumb_w/980/2026/11/28/roland2-edited-1795733764779-1795799724021.jpg"
DT_U17_LUC_VFF = "https://cdnphoto.dantri.com.vn/PqDWh_pYwncF2UEc1Owsdqi-Nac=/thumb_w/1020/2026/11/27/92268025646620881574459045913116145137857858n-1795764604272.jpg"

# 3. Đại hội Thể thao toàn quốc 2026 (Bơi lội, Điền kinh, Taekwondo, Xe đạp, Billiards, Cờ tướng)
TN_ANHVIEN_7 = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/tnw-17955250975574951488922155853666495148892215585366672af66bb65f9151f83e09cb44f046dfe-17957862389831419456196.jpg"
TN_MYTIEN_9 = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/tnw-1795696155702495148892215585366649514889221558536664718af4b0bfcba4dc12a6cbccf04eb8d-1795786238625814213057.jpg"
TN_THUYHIEN_8 = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/tnw-179534611450749514889221558536664951488922155853666207551919ce4f840ff0e0ca0bf49cd6f-17957862389221492881520.jpg"
VNE_AV_SWIM = "https://i1-thethao.vnecdn.net/2026/11/27/1795524615635-g860152096863999-4567-5422-1795796436.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=yTT4PyWlaUgeia5sM2ZP1w"
VNE_AV_MT_HUG = "https://i1-thethao.vnecdn.net/2026/11/27/1795693961346-6473522765579845-5330-3676-1795796436.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=vrKqz0v1hCMi80vA2aNAmw"
VNE_AV_SMILE = "https://i1-thethao.vnecdn.net/2026/11/27/1795524615635-6473522765579845-1344-9047-1795796436.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=wbjQiOv0J52mVymVZ1VWdA"
TN_JEREMIE = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/crb51965-17957844210811418509658.jpg"

TT_CAMTU_1 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/le-thi-cam-tu-dien-kinh-dai-hoi-the-thao-toan-quoc-17957887710691873963293.jpg"
TT_CAMTU_2 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/le-thi-cam-tu-dien-kinh-dai-hoi-the-thao-toan-quoc-2-17957887710671488909017.jpg"
TT_NGAN_NGHIA_1 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/ngan-ngoc-nghia-dien-kinh-dai-hoi-the-thao-toan-quoc-1-17957564392021924552921.jpg"
TT_NGAN_NGHIA_2 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/ngan-ngoc-nghia-dien-kinh-dai-hoi-the-thao-toan-quoc-2-1795756439211414779271.jpeg"
TT_OANH_RUN = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/26/nguyen-thi-oanh-dien-kinh-17549737253041732114910-95-0-723-1200-crop-179571011411010621503.jpg"

TN_CTV = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/img8924-17957863707681153518167-0-0-617-987-crop-17957863752541215651736.jpeg"
TN_KHOIMINH = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/tnw-photo-1795790487154-1795790488368958406881-17957904991392099179367.jpeg"
TN_BILLIARDS_55 = "https://images2.thanhnien.vn/528068263637045248/2026/11/27/mai-phuoc-1795781994656139811420.jpg"
TT_HAVANTIEN = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/ha-van-tien-4-edit-1795779712561245207623.jpg"
TT_MINHVUONG = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/minh-vuong-an-mung-ban-thang-cho-cand-1-17957939786641167384366.jpg"
TT_MINHHIEU = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/minh-hieu-2-edit-17957960338461865314264.jpg"
TT_PITCHAMON = "https://cdn2.tuoitre.vn/471584752817336320/2026/5/13/pitchamon-3-1778682083678210315278.jpg"
DT_RALLY = "https://cdnphoto.dantri.com.vn/jHpvZHWw7-r4jnEKSxyPpaKw6lE=/thumb_w/990/2026/11/27/giai-dua-xe-quoc-te-len-chotdocx-1795784164549.jpeg"
TN_VN_EAFF = "https://images2.thanhnien.vn/528068263637045248/2026/11/14/vn-179462195373183157185.jpg"
TT_TPHCM_SPAIN = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/27/phung-ba-duc-anh-1795768722052562826180-145-0-1086-1797-crop-17957693025881093418934.jpg"

# 4. Bóng đá & Thể thao Thế giới 27–28.11.2026
SKY_FOREST_ALONSO = "https://e0.365dm.com/26/11/1920x1080/skysports-chelsea-forest_7418332.jpg?20261127231744"
SKY_FOREST_GIBBS = "https://e2.365dm.com/26/11/1920x1080/skysports-morgan-gibbs-white_7418255.jpg?20261127214157"
SKY_FOREST_IGOR = "https://e1.365dm.com/26/11/1920x1080/skysports-igor-jesus-forest_7418204.jpg?20261127204534"
SKY_CHELSEA_ALONSO = "https://e0.365dm.com/26/11/1920x1080/skysports-chelsea-alonso_7418316.jpg?20261127222742"
SKY_CHELSEA_FOREST_2 = "https://e1.365dm.com/26/11/1920x1080/skysports-chelsea-forest_7418280.jpg?20261127220106"
DT_FOREST_CELEB = "https://cdnphoto.dantri.com.vn/357fkevATdGYZGIii7k-RkDLLHM=/thumb_w/1020/2026/11/28/chelsea-1-1795823184021.jpg"
DT_CHELSEA_GLOOM = "https://cdnphoto.dantri.com.vn/SWciCu8MuqbtqbxYuIMhWgIo7Lk=/thumb_w/1020/2026/11/28/chelsea-2-1795823287844.jpg"
VNE_FOFANA_GIBBS = "https://i1-thethao.vnecdn.net/2026/11/28/AFP-20261127-D8VB2TR-v1-MidRes-4687-4734-1795824017.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Daf6gzajW1WWV4hV9CSjvg"
VNE_ALONSO_SAD = "https://i1-thethao.vnecdn.net/2026/11/28/AFP-20261127-D8VE4JM-v1-HighRe-4226-7713-1795824017.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=TUNtoUgPyoUBudUumXw3cQ"

VNE_BRUNO_1 = "https://i1-thethao.vnecdn.net/2026/11/28/bruno-fernandes-1795824664-9100-1795824833.jpg?w=1200&h=675&q=100&dpr=1&fit=crop&s=bTwz9vF3uGl5O2E-mhA-1Q"
VNE_BRUNO_2 = "https://i1-thethao.vnecdn.net/2026/11/28/bruno-fernandes-8606-1795824833.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=-Mx0O83RzAi6qK8UBNTRJQ"
TT_ARS_MC = "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/27/britain-soccer-premier-league-2025-26-arsenal-vs-manchester-city-match-pics411zon-17957946847391830048370-31-0-450-801-crop-1795794740034276713376.jpg"
SKY_F1_LECLERC = "https://e1.365dm.com/26/11/1920x1080/skysports-f1-charles-leclerc_7418175.jpg?20261127200429"
SKY_F1_QATAR = "https://e1.365dm.com/26/11/1920x1080/skysports-motorsport-f1_7418111.jpg?20261127182826"
SKY_FURY = "https://e2.365dm.com/26/08/1920x1080/skysports-boxing-tyson-fury_7329017.jpg?20260823125152"
SKY_STEELERS = "https://e1.365dm.com/26/11/1920x1080/skysports-pittsburgh-steelers_7418315.jpg?20261127222738"
DT_CR7_PORTUGAL = "https://cdnphoto.dantri.com.vn/KwLBF9Cqy1BZGHDBvaoA5D2xbBk=/thumb_w/1020/2026/11/27/ronaldo-bat-ngo-roi-tuyen-bo-dao-nha-2-edited-1795781838497.jpg"
DT_JESUS_POR = "https://cdnphoto.dantri.com.vn/dzcGsJLFKArwIjOqu0tPPyWFqVs=/thumb_w/1020/2026/11/27/images-5-1795781920958.jpg"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 28.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 28 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất của thể thao Việt Nam và thế giới. "
        "Tại sân cỏ quốc nội, trận cầu tâm điểm vòng chín V-League giữa Thép Xanh Nam Định và Công an Hà Nội khép lại với tỷ số hòa 0-0, trong khi Sông Lam Nghệ An đánh bại Ninh Bình 1-0 để nối dài mạch bất bại. "
        "Ở Đại hội Thể thao toàn quốc 2026, kình ngư Nguyễn Thị Ánh Viên khép lại hành trình tái xuất với bảy huy chương vàng, còn Võ Thị Mỹ Tiên thống trị đường đua xanh với chín ngôi vô địch cá nhân. "
        "Trên đấu trường quốc tế, Chelsea gục ngã 2-3 trước Nottingham Forest khiến áp lực đè nặng lên huấn luyện viên Xabi Alonso, Manchester United gia hạn hợp đồng với Bruno Fernandes đến năm 2028 và huyền thoại MotoGP Marc Márquez bất ngờ tuyên bố giải nghệ."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí / BBC Sport / Sky Sports / The Guardian",
    "news_source": "VIỆT NAM & THẾ GIỚI",
    "credit": "ĐIỂM ĐỌC TỔNG HỢP",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 28 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất của thể thao Việt Nam và thế giới.",
        },
        {
            "voice_preset": "primary",
            "text": "Tại sân cỏ quốc nội, trận cầu tâm điểm vòng chín V-League giữa Thép Xanh Nam Định và Công an Hà Nội khép lại với tỷ số hòa 0-0, trong khi Sông Lam Nghệ An đánh bại Ninh Bình 1-0 để nối dài mạch bất bại.",
        },
        {
            "voice_preset": "secondary",
            "text": "Ở Đại hội Thể thao toàn quốc 2026, kình ngư Nguyễn Thị Ánh Viên khép lại hành trình tái xuất với bảy huy chương vàng, còn Võ Thị Mỹ Tiên thống trị đường đua xanh với chín ngôi vô địch cá nhân.",
        },
        {
            "voice_preset": "primary",
            "text": "Trên đấu trường quốc tế, Chelsea gục ngã 2-3 trước Nottingham Forest khiến áp lực đè nặng lên huấn luyện viên Xabi Alonso, Manchester United gia hạn hợp đồng với Bruno Fernandes đến năm 2028 và huyền thoại MotoGP Marc Márquez bất ngờ tuyên bố giải nghệ.",
        },
    ],
    "stat_badges": {
        "1": {"label": "BẢN TIN NGÀY", "value": "28.11.2026", "sub": "Toàn cảnh Việt Nam & Thế giới"},
        "2": {"label": "VÒNG 9 V-LEAGUE", "value": "NAM ĐỊNH 0-0 CAHN", "sub": "SLNA thắng Ninh Bình 1-0 giữ hạng nhì"},
        "3": {"label": "ĐẠI HỘI TDTT 2026", "value": "ÁNH VIÊN 7 • MỸ TIÊN 9", "sub": "TP.HCM dẫn đầu với 96 huy chương vàng"},
        "4": {"label": "TÂM ĐIỂM QUỐC TẾ", "value": "CHELSEA THUA 2-3", "sub": "Marc Márquez giải nghệ ở tuổi 33"},
    },
    "slots": [
        # Câu 1 (4 ảnh)
        _slot("sentence", 1, [_url(TN_ND_CAHN_1)], "THANH NIÊN / CLB NAM ĐỊNH", "Màn so tài căng thẳng giữa Nam Định và Công an Hà Nội tại Thiên Trường"),
        _slot("sentence", 1, [_url(VNE_AV_SWIM)], "VNEXPRESS / BÙI LƯỢNG", "Kình ngư Nguyễn Thị Ánh Viên tỏa sáng tại Đại hội Thể thao toàn quốc 2026"),
        _slot("sentence", 1, [_url(SKY_FOREST_GIBBS)], "SKY SPORTS", "Morgan Gibbs-White lập cú đúp nhấn chìm Chelsea tại City Ground"),
        _slot("sentence", 1, [_ddgs("Marc Marquez Ducati MotoGP 2026 Valencia")], "BING SEARCH", "Tay đua Marc Márquez gây sốc với quyết định giã từ đường đua MotoGP"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(DT_ND_CAHN_HAU)], "DÂN TRÍ / QUANG ĐƯƠNG", "Đoàn Văn Hậu và Công an Hà Nội chia điểm trên sân Thiên Trường"),
        _slot("sentence", 2, [_url(TN_ND_CAHN_2)], "THANH NIÊN / CLB NAM ĐỊNH", "Nam Định duy trì khoảng cách năm điểm trước Công an Hà Nội"),
        _slot("sentence", 2, [_url(VNE_SLNA_GOAL)], "VNEXPRESS / VPF", "Luiz Guilherme ghi bàn duy nhất giúp Sông Lam Nghệ An thắng Ninh Bình 1-0"),
        _slot("sentence", 2, [_url(TN_SLNA_JOY)], "THANH NIÊN / CLB SLNA", "Niềm vui chiến thắng của Sông Lam Nghệ An sau chín vòng bất bại"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url(TN_ANHVIEN_7)], "THANH NIÊN / ĐỘC LẬP", "Nguyễn Thị Ánh Viên hoàn tất bộ sưu tập bảy huy chương vàng tại Đại hội"),
        _slot("sentence", 3, [_url(TN_MYTIEN_9)], "THANH NIÊN / ĐỘC LẬP", "Võ Thị Mỹ Tiên là vận động viên xuất sắc nhất môn bơi với chín HCV cá nhân"),
        _slot("sentence", 3, [_url(VNE_AV_MT_HUG)], "VNEXPRESS / BÙI LƯỢNG", "Khoảnh khắc đẹp giữa Ánh Viên và đàn em Võ Thị Mỹ Tiên trên đường đua xanh"),
        _slot("sentence", 3, [_url(TN_JEREMIE)], "THANH NIÊN / SỞ VHTT TP.HCM", "Kình ngư Lương Jérémie Loic Nino phá kỷ lục quốc gia giúp TP.HCM tăng tốc"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_url(SKY_CHELSEA_ALONSO)], "SKY SPORTS", "Huấn luyện viên Xabi Alonso đối mặt áp lực nặng nề sau thất bại thứ ba liên tiếp"),
        _slot("sentence", 4, [_url(SKY_FOREST_IGOR)], "SKY SPORTS", "Igor Jesus ăn mừng bàn mở tỷ số vào lưới Chelsea ngay phút thứ năm"),
        _slot("sentence", 4, [_url(VNE_BRUNO_1)], "VNEXPRESS / AP", "Bruno Fernandes được Manchester United kích hoạt gia hạn đến năm 2028"),
        _slot("sentence", 4, [_ddgs("Marc Marquez celebration Ducati MotoGP")], "BING SEARCH", "Nhà vô địch tám lần thế giới Marc Márquez nói lời chia tay MotoGP ở tuổi 33"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — NAM ĐỊNH HÒA CÔNG AN HÀ NỘI 0-0, GIỮ VỮNG NGÔI ĐẦU V-LEAGUE)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "VÒNG 9 V-LEAGUE",
        "title": "Nam Định hòa không bàn thắng CLB Công an Hà Nội, giữ vững ngôi đầu V-League",
        "summary": (
            "Trận cầu tâm điểm vòng chín V-League tối ngày 27 tháng 11 trên sân Thiên Trường giữa Thép Xanh Nam Định và Công an Hà Nội khép lại với tỷ số hòa 0-0. "
            "Hành quân đến thành Nam chỉ ba ngày sau thắng lợi tại cúp châu Á, đội khách chịu tổn thất lực lượng nặng nề khi huấn luyện viên Alexandre Polking chỉ có 17 cầu thủ đăng ký vì chấn thương. "
            "Điểm nhấn đáng chú ý nhất xảy ra ở phút 76 khi phía Công an Hà Nội khiếu nại bóng chạm tay tiền vệ Nguyễn Tuấn Anh trong vòng cấm, nhưng trọng tài từ chối phạt đền sau khi tham khảo VAR. "
            "Kết quả chia điểm giúp Nam Định tiếp tục dẫn đầu bảng xếp hạng và duy trì khoảng cách năm điểm nhiều hơn chính đối thủ."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / DÂN TRÍ",
        "credit": "THANH NIÊN / QUANG ĐƯƠNG",
        "stat_badges": {
            "1": {"label": "TÂM ĐIỂM THIÊN TRƯỜNG", "value": "NAM ĐỊNH 0-0 CAHN", "sub": "Vòng 9 V-League tối 27/11"},
            "3": {"label": "TÌNH HUỐNG PHÚT 76", "value": "VAR TỪ CHỐI PHẠT ĐỀN", "sub": "Tranh cãi bóng chạm tay Nguyễn Tuấn Anh"},
            "4": {"label": "CỤC DIỆN NGÔI ĐẦU", "value": "CÁCH BIỆT 5 ĐIỂM", "sub": "Nam Định giữ đỉnh trước CAHN"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_ND_CAHN_1)], "THANH NIÊN / CLB NAM ĐỊNH", "Trận đại chiến giữa Nam Định và Công an Hà Nội diễn ra chặt chẽ trên sân Thiên Trường"),
            _slot("title", 0, [_url(DT_ND_CAHN_1)], "DÂN TRÍ / QUANG ĐƯƠNG", "Công an Hà Nội nhập cuộc chủ động trong hiệp một nhưng không thể xuyên phá hàng thủ chủ nhà"),
            _slot("sentence", 1, [_url(TT_ND_CAHN)], "TUỔI TRẺ / NAM ĐỊNH FC", "Hai đội chia điểm không bàn thắng trong trận đấu sớm vòng chín V-League"),
            _slot("sentence", 2, [_url(TN_ND_CAHN_2)], "THANH NIÊN / CLB NAM ĐỊNH", "Đội hình Công an Hà Nội bị bào mòn thể lực và thiếu hụt nhân sự vì chấn thương"),
            _slot("sentence", 2, [_url(DT_ND_CAHN_HAU)], "DÂN TRÍ / QUANG ĐƯƠNG", "Đoàn Văn Hậu thi đấu xông xáo bên hành lang cánh của đội khách"),
            _slot("sentence", 3, [_url(TN_ND_CAHN_3)], "THANH NIÊN / CLB NAM ĐỊNH", "Trọng tài tham khảo công nghệ VAR ở phút 76 và xác định không có lỗi phạt đền"),
            _slot("sentence", 4, [_url(TN_CAIO_ND), _url(DT_ND_CAHN_3)], "THANH NIÊN / DÂN TRÍ", "Thép Xanh Nam Định giữ chắc ngôi đầu bảng xếp hạng sau vòng đấu thứ chín"),
        ],
    },

    # 02 (Nữ — HLV POLKING BÁC TIN ĐỒN QUANG HẢI CHIA TAY ĐỘI TUYỂN VIỆT NAM)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "ĐỘI TUYỂN VIỆT NAM",
        "title": "HLV Alexandre Polking khẳng định tin đồn Quang Hải chia tay tuyển Việt Nam là giả",
        "summary": (
            "Ngay sau trận hòa trên sân Thiên Trường tối 27 tháng 11, huấn luyện viên trưởng Công an Hà Nội Alexandre Polking chính thức lên tiếng về tương lai của tiền vệ Nguyễn Quang Hải. "
            "Trước thông tin cho rằng đội trưởng tuyển Việt Nam có nguyện vọng giã từ sự nghiệp quốc tế, nhà cầm quân người Đức gốc Brazil bác bỏ gay gắt và khẳng định đó hoàn toàn là tin giả. "
            "Ông Polking nhấn mạnh Quang Hải vẫn đang ở độ tuổi sung sức, giàu khát khao thi đấu và còn nhiều năm đỉnh cao để đóng góp cho màu áo đội tuyển quốc gia. "
            "Phát biểu dứt khoát này phần nào giải tỏa tâm lý người hâm mộ sau khi xuất hiện nhiều đồn đoán trái chiều về nội bộ đội tuyển trong những ngày qua."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / NAM TRẦN",
        "stat_badges": {
            "1": {"label": "HỌP BÁO SAU TRẬN", "value": "HLV POLKING LÊN TIẾNG", "sub": "Phản hồi dứt khoát tại sân Thiên Trường"},
            "2": {"label": "PHỦ NHẬN TIN ĐỒN", "value": "100% LÀ TIN GIẢ", "sub": "Bác bỏ tin Quang Hải muốn rời ĐTQG"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_QUANGHAI)], "TUỔI TRẺ / NAM TRẦN", "Đội trưởng Nguyễn Quang Hải trong màu áo đội tuyển quốc gia Việt Nam"),
            _slot("title", 0, [_ddgs("Alexandre Polking Cong An Ha Noi coach V-League")], "BING SEARCH", "Huấn luyện viên Alexandre Polking phản bác thông tin sai sự thật về học trò"),
            _slot("sentence", 1, [_url(DT_ND_CAHN_1)], "DÂN TRÍ / QUANG ĐƯƠNG", "Ông Alexandre Polking trả lời truyền thông ngay sau trận Nam Định gặp CAHN"),
            _slot("sentence", 2, [_url(TT_QUANGHAI)], "TUỔI TRẺ / NAM TRẦN", "Thuyền trưởng của CAHN gọi tin đồn Quang Hải rời tuyển là hoàn toàn bịa đặt"),
            _slot("sentence", 3, [_ddgs("Nguyen Quang Hai Cong An Ha Noi V-League")], "BING SEARCH", "Quang Hải được khẳng định vẫn còn nguyên động lực cống hiến cho tuyển Việt Nam"),
            _slot("sentence", 4, [_url(DT_ND_CAHN_3)], "DÂN TRÍ / QUANG ĐƯƠNG", "Tuyên bố của HLV Polking giúp dẹp tan làn sóng hoang mang của cổ động viên"),
        ],
    },

    # 03 (Nam — SLNA ĐÁNH BẠI NINH BÌNH 1-0, NỐI DÀI MẠCH 9 TRẬN BẤT BẠI)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "VÒNG 9 V-LEAGUE",
        "title": "Sông Lam Nghệ An tạo địa chấn thắng Ninh Bình 1-0, nối dài mạch 9 trận bất bại",
        "summary": (
            "Trên sân Vinh tối 27 tháng 11, Sông Lam Nghệ An tiếp tục trở thành hiện tượng lớn nhất V-League 2026-2027 khi quật ngã ứng viên vô địch Ninh Bình với tỷ số 1-0. "
            "Bước ngoặt trận đấu đến ở phút 22 khi tiền đạo ngoại binh Luiz Guilherme thoát xuống tinh tế, vượt qua thủ môn Đặng Văn Lâm để ghi bàn thắng duy nhất. "
            "Trong thời gian còn lại, dù tiền vệ Nguyễn Hoàng Đức cùng dàn sao đội khách dồn lực tấn công, hàng phòng ngự kỷ luật của đội bóng xứ Nghệ vẫn đứng vững. "
            "Chiến thắng ấn tượng giúp Sông Lam Nghệ An trở thành câu lạc bộ duy nhất bất bại sau chín vòng và vượt mặt chính Ninh Bình để chiếm ngôi nhì bảng."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ",
        "news_source": "THANH NIÊN / VNEXPRESS",
        "credit": "VNEXPRESS / VPF",
        "stat_badges": {
            "1": {"label": "HIỆN TƯỢNG V-LEAGUE", "value": "SLNA 1-0 NINH BÌNH", "sub": "Chiến thắng thuyết phục trên sân Vinh"},
            "2": {"label": "KHOẢNH KHẮC PHÚT 22", "value": "LUIZ GUILHERME GHI BÀN", "sub": "Vượt qua thủ môn Đặng Văn Lâm"},
            "4": {"label": "CỘT MỐC ĐỘC TÔN", "value": "9 TRẬN BẤT BẠI • HẠNG 2", "sub": "Đội duy nhất chưa thua tại V-League"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_SLNA_GOAL)], "VNEXPRESS / VPF", "Luiz Guilherme vượt qua Đặng Văn Lâm ghi bàn quyết định cho Sông Lam Nghệ An"),
            _slot("title", 0, [_url(TN_SLNA_1)], "THANH NIÊN / THANH NIÊN", "Các cầu thủ Sông Lam Nghệ An thi đấu gắn kết trước dàn sao Ninh Bình"),
            _slot("sentence", 1, [_url(TT_SLNA_2)], "TUỔI TRẺ / SLNA", "Đội bóng xứ Nghệ tạo bất ngờ lớn nhất mùa giải khi đứng vững ở nhóm đầu"),
            _slot("sentence", 2, [_url(VNE_SLNA_LAM)], "VNEXPRESS / VPF", "Tình huống dứt điểm sắc bén của Luiz Guilherme ở phút 22 trên sân Vinh"),
            _slot("sentence", 2, [_url(TN_SLNA_LUIZ)], "THANH NIÊN / CLB SLNA", "Ngoại binh Luiz Guilherme là mũi nhọn nguy hiểm nhất bên phía đội chủ nhà"),
            _slot("sentence", 3, [_url(VNE_HOANGDUC)], "VNEXPRESS / VPF", "Quả bóng vàng Nguyễn Hoàng Đức không thể giúp Ninh Bình tránh khỏi thất bại"),
            _slot("sentence", 4, [_url(TN_SLNA_JOY)], "THANH NIÊN / CLB SLNA", "Niềm vui vỡ òa của tập thể Sông Lam Nghệ An khi vươn lên vị trí thứ hai"),
        ],
    },

    # 04 (Nữ — TÂM ĐIỂM V-LEAGUE HÔM NAY 28/11: HÀ NỘI ĐẤU HÀ TĨNH, CA TP.HCM TIẾP HAGL)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "LỊCH ĐẤU V-LEAGUE 28/11",
        "title": "Tâm điểm V-League hôm nay 28/11: Hà Nội FC đụng độ Hà Tĩnh, Công an TP.HCM tiếp HAGL",
        "summary": (
            "Vòng chín V-League chiều tối nay ngày 28 tháng 11 tiếp tục diễn ra sôi động với ba cặp đấu có tính chất quan trọng đối với cả cuộc đua tốp đầu lẫn nhóm trụ hạng. "
            "Lúc 18 giờ trên sân Thống Nhất, câu lạc bộ Công an TP.HCM cùng thủ thành Lê Giang Patrik tiếp đón Hoàng Anh Gia Lai đang khát điểm thoát khỏi nhóm cuối bảng. "
            "Cùng giờ, tân binh Bắc Ninh chạm trán SHB Đà Nẵng của huấn luyện viên Lee Young-jin trong trận đấu cân tài cân sức ở khu vực giữa bảng xếp hạng. "
            "Tâm điểm muộn nhất lúc 19 giờ 15 tại sân Hàng Đẫy chứng kiến Hà Nội FC đang có 12 điểm quyết tâm đánh bại Hồng Lĩnh Hà Tĩnh để vượt mặt chính đối thủ trên bảng tổng sắp."
        ),
        "source": "Thanh Niên",
        "news_source": "THANH NIÊN",
        "credit": "THANH NIÊN / VPF",
        "stat_badges": {
            "2": {"label": "18H00 • SÂN THỐNG NHẤT", "value": "CA TP.HCM VS HAGL", "sub": "Thử thách khó cho đội bóng phố Núi"},
            "4": {"label": "19H15 • SÂN HÀNG ĐẪY", "value": "HÀ NỘI FC VS HÀ TĨNH", "sub": "Cơ hội bứt phá vào nhóm dẫn đầu"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_VL_HANOI)], "THANH NIÊN / VPF", "Hà Nội FC đặt mục tiêu giành trọn ba điểm trên sân nhà Hàng Đẫy tối nay"),
            _slot("title", 0, [_url(TN_VL_CATPHCM)], "THANH NIÊN / VPF", "Công an TP.HCM chuẩn bị tiếp đón Hoàng Anh Gia Lai lúc 18 giờ"),
            _slot("sentence", 1, [_url(TN_VL_DANANG)], "THANH NIÊN / VPF", "Loạt trận ngày thứ Bảy hứa hẹn làm thay đổi cục diện bảng xếp hạng V-League"),
            _slot("sentence", 2, [_url(TN_VL_CATPHCM)], "THANH NIÊN / VPF", "Công an TP.HCM cần chiến thắng trước Hoàng Anh Gia Lai để giải tỏa áp lực"),
            _slot("sentence", 3, [_url(TN_VL_DANANG)], "THANH NIÊN / VPF", "SHB Đà Nẵng hướng tới kết quả tích cực trong chuyến làm khách trước Bắc Ninh"),
            _slot("sentence", 4, [_url(TN_VL_HANOI)], "THANH NIÊN / VPF", "Màn so tài giữa Hà Nội FC và Hồng Lĩnh Hà Tĩnh khép lại ngày thi đấu hôm nay"),
        ],
    },

    # 05 (Nam — U17 WORLD CUP 2026 XÁC ĐỊNH ĐỦ 32 ĐỘI ĐI TIẾP, NHẬT BẢN ĐẤU HÀN QUỐC)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "U17 WORLD CUP 2026",
        "title": "U17 World Cup 2026 xác định đủ 32 đội vào vòng 1/16, Nhật Bản gặp Hàn Quốc",
        "summary": (
            "Rạng sáng ngày 28 tháng 11 theo giờ Việt Nam, vòng bảng U17 World Cup 2026 tại Qatar chính thức hạ màn, qua đó xác định trọn vẹn 32 đội bóng góp mặt ở vòng đấu loại trực tiếp. "
            "Ở lượt cuối bảng L, U17 Nhật Bản thị uy sức mạnh bằng chiến thắng hủy diệt 7-0 trước Honduras để đi tiếp cùng đội nhất bảng Serbia, đội vừa hạ Colombia 1-0. "
            "Tổng kết sau vòng bảng, bóng đá châu Á gây ấn tượng mạnh với bảy trên chín đại diện giành quyền đi tiếp gồm Hàn Quốc, Nhật Bản, Uzbekistan, Trung Quốc, Saudi Arabia, Australia và Tajikistan, trong khi chỉ có chủ nhà Qatar và U17 Việt Nam dừng bước. "
            "Theo phân nhánh vòng 32 đội diễn ra từ ngày 30 tháng 11, hai đại diện hàng đầu châu lục là U17 Hàn Quốc và U17 Nhật Bản sẽ chạm trán trực tiếp để tranh vé vào vòng 1/8."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "TUỔI TRẺ / FIFA",
        "stat_badges": {
            "1": {"label": "KHÉP LẠI VÒNG BẢNG", "value": "ĐỦ 32 ĐỘI VÀO VÒNG 1/16", "sub": "Loạt trận knock-out khởi tranh 30/11"},
            "2": {"label": "LƯỢT CUỐI BẢNG L", "value": "NHẬT BẢN 7-0 HONDURAS", "sub": "Serbia thắng Colombia 1-0 giữ ngôi đầu"},
            "4": {"label": "CHÂU Á ÁP ĐẢO", "value": "7/9 ĐẠI DIỆN ĐI TIẾP", "sub": "Siêu đại chiến Hàn Quốc vs Nhật Bản"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Japan U17 football team national celebration")], "BING SEARCH", "U17 Nhật Bản thắng đậm 7-0 trước Honduras để tiến vào vòng 32 đội"),
            _slot("title", 0, [_ddgs("FIFA U17 World Cup Qatar stadium match")], "BING SEARCH", "32 đội tuyển trẻ xuất sắc nhất thế giới bước vào vòng loại trực tiếp tại Qatar"),
            _slot("sentence", 1, [_ddgs("Italy U17 national football team match")], "BING SEARCH", "Vòng bảng U17 World Cup 2026 chính thức khép lại vào rạng sáng 28 tháng 11"),
            _slot("sentence", 2, [_ddgs("Japan national youth football players goal")], "BING SEARCH", "Các cầu thủ trẻ Nhật Bản phô diễn hiệu suất ghi bàn đáng nể ở lượt trận cuối"),
            _slot("sentence", 3, [_ddgs("South Korea U17 football team Asia")], "BING SEARCH", "Bóng đá châu Á có tới bảy đại diện góp mặt trong nhóm 32 đội mạnh nhất"),
            _slot("sentence", 4, [_ddgs("South Korea vs Japan football youth match")], "BING SEARCH", "Cuộc đối đầu giữa Hàn Quốc và Nhật Bản đảm bảo cho châu Á một suất vòng 1/8"),
        ],
    },

    # 06 (Nữ — BÁO ĐÔNG NAM Á ĐÁNH GIÁ CAO U17 VIỆT NAM & DẤU ẤN NGUYỄN LỰC)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "U17 VIỆT NAM",
        "title": "Báo Đông Nam Á khen ngợi bản lĩnh U17 Việt Nam, Chu Ngọc Nguyễn Lực ghi dấu ấn đậm nét",
        "summary": (
            "Sáng nay ngày 28 tháng 11, thầy trò huấn luyện viên Cristiano Roland đã lên đường về nước sau hành trình không cam chịu phận lót đường tại U17 World Cup 2026. "
            "Các tờ báo lớn của Thái Lan và Indonesia đồng loạt dành lời khen ngợi khi đại diện duy nhất của Đông Nam Á dám chơi sòng phẳng trước Bỉ, hòa New Zealand 3-3 và chỉ chịu thua Mali về thể trạng. "
            "Chuyên gia bóng đá Mali Balla Sanogo cũng thừa nhận tinh thần chiến đấu kỷ luật của U17 Việt Nam đã gây ra rất nhiều khó khăn cho nhà vô địch châu Phi trong suốt hiệp một. "
            "Trên phương diện cá nhân, tiền vệ Chu Ngọc Nguyễn Lực ghi tên vào lịch sử khi trở thành cầu thủ Việt Nam đầu tiên ghi hai bàn thắng ở một kỳ World Cup bóng đá 11 người."
        ),
        "source": "Dân Trí / Thanh Niên / VnExpress",
        "news_source": "DÂN TRÍ / VNEXPRESS",
        "credit": "VNEXPRESS / ĐOÀN CA",
        "stat_badges": {
            "1": {"label": "CHIA TAY QATAR", "value": "U17 VIỆT NAM VỀ NƯỚC", "sub": "Khép lại giải đấu nhiều cảm xúc"},
            "4": {"label": "DẤU ẤN LỊCH SỬ", "value": "NGUYỄN LỰC GHI 2 BÀN", "sub": "Cầu thủ Việt Nam đầu tiên lập cú đúp ở World Cup"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_U17_1)], "DÂN TRÍ / VFF", "Tập thể U17 Việt Nam để lại hình ảnh quả cảm trong lần đầu góp mặt tại World Cup"),
            _slot("title", 0, [_url(VNE_U17_LUC)], "VNEXPRESS / ĐOÀN CA", "Chu Ngọc Nguyễn Lực trở thành cầu thủ Việt Nam đầu tiên ghi hai bàn ở World Cup"),
            _slot("sentence", 1, [_url(DT_ROLAND)], "DÂN TRÍ / VFF", "Huấn luyện viên Cristiano Roland tự hào về thái độ thi đấu của các học trò"),
            _slot("sentence", 2, [_url(DT_U17_2)], "DÂN TRÍ / VFF", "Truyền thông Thái Lan và Indonesia đánh giá cao màn trình diễn của U17 Việt Nam"),
            _slot("sentence", 3, [_url(TN_U17_MALI_FIG)], "THANH NIÊN / VFF", "Giới chuyên môn Mali ấn tượng với khả năng tổ chức phòng ngự của U17 Việt Nam"),
            _slot("sentence", 4, [_url(TN_U17_LUC_10), _url(DT_U17_LUC_VFF)], "THANH NIÊN / DÂN TRÍ", "Tiền vệ Chu Ngọc Nguyễn Lực lọt nhóm cầu thủ châu Á ghi bàn nhiều nhất giải"),
            _slot("sentence", 4, [_url(VNE_U17_KHOA)], "VNEXPRESS / ĐOÀN CA", "Lứa cầu thủ trẻ như Đăng Khoa và Nguyễn Lực được kỳ vọng tiến xa trong tương lai"),
        ],
    },

    # 07 (Nam — ÁNH VIÊN KHÉP LẠI ĐẠI HỘI VỚI 7 HCV, MỸ TIÊN THỐNG TRỊ ĐƯỜNG ĐUA XANH)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "ĐẠI HỘI TDTT 2026",
        "title": "Ánh Viên khép lại Đại hội với 7 HCV, Võ Thị Mỹ Tiên thống trị đường đua xanh",
        "summary": (
            "Ngày thi đấu cuối cùng môn bơi Đại hội Thể thao toàn quốc 2026 khép lại tối 27 tháng 11 chứng kiến màn chia tay hoàn hảo của tượng đài Nguyễn Thị Ánh Viên. "
            "Hai tấm huy chương vàng ở nội dung 200m ngửa nữ và tiếp sức 4x100m tự do nữ giúp kình ngư đoàn Quân Đội kết thúc kỳ Đại hội tái xuất đầy cảm xúc với bảy huy chương vàng. "
            "Trong khi đó, tài năng 21 tuổi Võ Thị Mỹ Tiên của đoàn Tây Ninh bước lên ngôi vị vận động viên xuất sắc nhất môn bơi khi giành thêm ngôi vô địch 200m bướm để nâng thành tích cá nhân lên chín huy chương vàng. "
            "Cũng tại đường đua xanh Phú Thọ, kình ngư Trần Duy Khôi trở thành vận động viên đầu tiên của Thành phố Hồ Chí Minh chạm mốc 30 huy chương lịch sử qua các kỳ Đại hội, còn Lương Jérémie phá kỷ lục quốc gia 50m bướm."
        ),
        "source": "Thanh Niên / VnExpress",
        "news_source": "THANH NIÊN / VNEXPRESS",
        "credit": "THANH NIÊN / ĐỘC LẬP",
        "stat_badges": {
            "2": {"label": "MÀN TÁI XUẤT RỰC RỠ", "value": "ÁNH VIÊN ĐOẠT 7 HCV", "sub": "3 HCV cá nhân và 4 HCV tiếp sức"},
            "3": {"label": "NỮ HOÀNG ĐƯỜNG ĐUA XANH", "value": "VÕ THỊ MỸ TIÊN 9 HCV", "sub": "VĐV xuất sắc nhất môn bơi Đại hội 2026"},
            "4": {"label": "CỘT MỐC TP.HCM", "value": "TRẦN DUY KHÔI 30 HC", "sub": "Lương Jérémie phá Kỷ lục Quốc gia 50m bướm"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_ANHVIEN_7)], "THANH NIÊN / ĐỘC LẬP", "Nguyễn Thị Ánh Viên có màn kết rực rỡ với bảy huy chương vàng tại Đại hội 2026"),
            _slot("title", 0, [_url(TN_MYTIEN_9)], "THANH NIÊN / ĐỘC LẬP", "Võ Thị Mỹ Tiên thống trị đường đua xanh với chín huy chương vàng cá nhân"),
            _slot("sentence", 1, [_url(VNE_AV_SWIM)], "VNEXPRESS / BÙI LƯỢNG", "Bầu không khí sôi động trong ngày thi đấu cuối cùng môn bơi tại CLB Phú Thọ"),
            _slot("sentence", 2, [_url(VNE_AV_SMILE)], "VNEXPRESS / BÙI LƯỢNG", "Nụ cười rạng rỡ của Ánh Viên khi hoàn thành trọn vẹn bảy tấm huy chương vàng"),
            _slot("sentence", 3, [_url(VNE_AV_MT_HUG)], "VNEXPRESS / BÙI LƯỢNG", "Cái ôm ấm áp giữa Ánh Viên và đàn em xuất sắc Võ Thị Mỹ Tiên"),
            _slot("sentence", 3, [_url(TN_THUYHIEN_8)], "THANH NIÊN / ĐỘC LẬP", "Bên cạnh Mỹ Tiên, tài năng trẻ Nguyễn Thúy Hiền cũng ghi dấu ấn với tám huy chương vàng"),
            _slot("sentence", 4, [_url(TN_JEREMIE)], "THANH NIÊN / SỞ VHTT TP.HCM", "Lương Jérémie Loic Nino góp công lớn cho bơi lội chủ nhà với những kỷ lục mới"),
        ],
    },

    # 08 (Nữ — ĐIỀN KINH ĐẠI HỘI BÙNG NỔ KỶ LỤC, VUA TỐC ĐỘ NGẦN NGỌC NGHĨA BỊ LOẠI SỐC)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "ĐẠI HỘI TDTT 2026",
        "title": "Điền kinh Đại hội bùng nổ kỷ lục, vua tốc độ Ngần Ngọc Nghĩa bị thẻ đỏ loại sốc",
        "summary": (
            "Đường chạy sân vận động Thống Nhất ngày 27 tháng 11 chứng kiến nhiều kỷ lục Đại hội bị xô đổ cùng những diễn biến nghẹt thở của môn điền kinh. "
            "Ở chung kết 100m rào nữ, Bùi Thị Nguyên xuất sắc vượt qua Huỳnh Thị Mỹ Tiên với thông số 13,37 giây để giành huy chương vàng và phá sâu kỷ lục Đại hội tồn tại từ năm 2010. "
            "Trước đó vào buổi sáng, Nguyễn Thị Oanh dễ dàng giành vàng nội dung 3000m vượt chướng ngại vật, còn Lê Thị Cẩm Tú đoạt huy chương vàng 100m nữ với 11,60 giây khi hơn Phùng Thị Huệ đúng ba phần trăm giây. "
            "Trái ngược niềm vui phá kỷ lục, cú sốc lớn nhất thuộc về nam vương tốc độ Ngần Ngọc Nghĩa khi anh bị trọng tài rút thẻ đỏ loại ngay từ bán kết 100m nam vì lỗi xuất phát sớm."
        ),
        "source": "Tuổi Trẻ / TDTT",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / QUÝ LƯỢNG",
        "stat_badges": {
            "2": {"label": "PHÁ KỶ LỤC 100M RÀO", "value": "BÙI THỊ NGUYÊN 13,37 GIÂY", "sub": "Phá kỷ lục Đại hội tồn tại suốt 16 năm"},
            "3": {"label": "CHUNG KẾT 100M NỮ", "value": "CẨM TÚ 11,60S VS HUỆ 11,63S", "sub": "Nguyễn Thị Oanh giành vàng 3000m chướng ngại vật"},
            "4": {"label": "CÚ SỐC BÁN KẾT", "value": "NGẦN NGỌC NGHĨA THẺ ĐỎ", "sub": "Bị truất quyền thi đấu vì xuất phát sớm"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_CAMTU_1)], "TUỔI TRẺ / QUÝ LƯỢNG", "Lê Thị Cẩm Tú bứt tốc ngoạn mục trên đường chạy chung kết 100m nữ"),
            _slot("title", 0, [_url(TT_NGAN_NGHIA_1)], "TUỔI TRẺ / ĐỨC LONG", "Kỷ lục gia Ngần Ngọc Nghĩa ôm đầu tiếc nuối khi bị loại sốc ở bán kết"),
            _slot("sentence", 1, [_url(TT_OANH_RUN)], "TUỔI TRẺ / TTO", "Sân vận động Thống Nhất rực lửa với hàng loạt nội dung chung kết điền kinh"),
            _slot("sentence", 2, [_ddgs("Bui Thi Nguyen 100m hurdles Vietnam athletics")], "BING SEARCH", "Bùi Thị Nguyên bứt phá giành huy chương vàng và phá kỷ lục Đại hội 100m rào"),
            _slot("sentence", 3, [_url(TT_CAMTU_2)], "TUỔI TRẺ / ĐỨC KHUÊ", "Chân chạy An Giang Lê Thị Cẩm Tú giành huy chương vàng 100m nữ đầy kịch tính"),
            _slot("sentence", 4, [_url(TT_NGAN_NGHIA_2)], "TUỔI TRẺ / ĐỨC LONG", "Ngần Ngọc Nghĩa đánh rơi cơ hội bảo vệ huy chương vàng vì lỗi xuất phát"),
        ],
    },

    # 09 (Nam — CHÂU TUYẾT VÂN GIÀNH HCV THỨ 5 LIÊN TIẾP, TP.HCM BỨT TỐC ĐẠI HỘI)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "ĐẠI HỘI TDTT 2026",
        "title": "Châu Tuyết Vân giành HCV thứ 5 liên tiếp, TP.HCM dẫn đầu Đại hội với 96 huy chương vàng",
        "summary": (
            "Tại môn Taekwondo Đại hội Thể thao toàn quốc 2026, hoa khôi làng võ Châu Tuyết Vân ở tuổi 36 vẫn chứng tỏ bản lĩnh khi cùng đồng đội Hồ Thanh Ân giành huy chương vàng quyền đôi nam nữ. "
            "Thành tích này đánh dấu tấm huy chương vàng Đại hội thứ năm liên tiếp trong sự nghiệp của Châu Tuyết Vân, tròn hai mươi năm kể từ lần đầu cô góp mặt ở sân chơi lớn nhất cả nước. "
            "Sự bùng nổ ở Taekwondo, bơi lội và xe đạp nữ giúp đoàn chủ nhà Thành phố Hồ Chí Minh giành thêm mười huy chương vàng trong ngày 27 tháng 11 để chạm mốc 96 huy chương vàng. "
            "Trên bảng tổng sắp tính đến tối qua, Thành phố Hồ Chí Minh tạo cách biệt an toàn tới 20 huy chương vàng trước đoàn nhì bảng Hà Nội và bỏ xa đội xếp thứ ba là Quân Đội."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / SỞ VHTT TP.HCM",
        "stat_badges": {
            "1": {"label": "TƯỢNG ĐÀI TAEKWONDO", "value": "CHÂU TUYẾT VÂN 5 KỲ HCV", "sub": "Vô địch quyền đôi nam nữ ở tuổi 36"},
            "4": {"label": "BẢNG TỔNG SẮP 27/11", "value": "TP.HCM 96 • HÀ NỘI 76 HCV", "sub": "Đoàn Quân Đội giữ hạng ba với 41 HCV"},
        },
        "slots": [
            _slot("title", 0, [_url(TN_CTV)], "THANH NIÊN / SỞ VHTT TP.HCM", "Châu Tuyết Vân rạng rỡ ở tuổi 36 sau khi giành huy chương vàng Taekwondo"),
            _slot("title", 0, [_url(TN_JEREMIE)], "THANH NIÊN / SỞ VHTT TP.HCM", "Đoàn thể thao Thành phố Hồ Chí Minh bứt phá mạnh mẽ trên bảng tổng sắp"),
            _slot("sentence", 1, [_url(TN_CTV)], "THANH NIÊN / SỞ VHTT TP.HCM", "Châu Tuyết Vân và Hồ Thanh Ân mang về tấm huy chương vàng quý giá cho chủ nhà"),
            _slot("sentence", 2, [_ddgs("Chau Tuyet Van Taekwondo Vietnam gold medal")], "BING SEARCH", "Cô gái vàng Taekwondo nối dài mạch vô địch qua năm kỳ Đại hội liên tiếp"),
            _slot("sentence", 3, [_url(TN_ANHVIEN_7)], "THANH NIÊN / ĐỘC LẬP", "Đoàn Thành phố Hồ Chí Minh tiến sát cột mốc 100 huy chương vàng"),
            _slot("sentence", 4, [_url(VNE_AV_SWIM)], "VNEXPRESS / BÙI LƯỢNG", "Khoảng cách giữa Thành phố Hồ Chí Minh và Hà Nội được nới rộng lên 20 HCV"),
        ],
    },

    # 10 (Nữ — NOTTINGHAM FOREST QUẬT NGÃ CHELSEA 3-2 TẠI CITY GROUND)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "NGOẠI HẠNG ANH",
        "title": "Nottingham Forest quật ngã Chelsea 3-2, đẩy The Blues vào chuỗi 3 trận thua liên tiếp",
        "summary": (
            "Rạng sáng ngày 28 tháng 11 ở trận đấu sớm vòng 12 Ngoại hạng Anh, Nottingham Forest tạo nên cơn địa chấn khi đánh bại Chelsea 3-2 ngay trên sân nhà City Ground. "
            "Tiền đạo Igor Jesus sớm đưa đội chủ nhà vượt lên ngay phút thứ năm bằng cú vô-lê đẹp mắt, trước khi đội trưởng Morgan Gibbs-White tỏa sáng rực rỡ với cú đúp ở phút 51 và phút 72. "
            "Những nỗ lực muộn màng của tiền đạo vào sân thay người Emmanuel Emegha với hai bàn thắng ở các phút 54 và 89 chỉ giúp Chelsea rút ngắn cách biệt chứ không thể giữ lại điểm số. "
            "Đây là thắng lợi sân nhà đầu tiên của Nottingham Forest trước Chelsea kể từ năm 1997, đồng thời đẩy đội bóng thành London vào chuỗi ba thất bại liên tiếp tại Ngoại hạng Anh."
        ),
        "source": "BBC Sport / Sky Sports / Dân Trí",
        "news_source": "SKY SPORTS / BBC SPORT",
        "credit": "SKY SPORTS",
        "stat_badges": {
            "1": {"label": "VÒNG 12 NGOẠI HẠNG ANH", "value": "FOREST 3-2 CHELSEA", "sub": "Chiến thắng sân nhà đầu tiên từ năm 1997"},
            "2": {"label": "NGƯỜI HÙNG CITY GROUND", "value": "GIBBS-WHITE LẬP CÚ ĐÚP", "sub": "Igor Jesus mở tỷ số ngay phút thứ 5"},
            "4": {"label": "BÁO ĐỘNG ĐỎ", "value": "CHELSEA THUA 3 TRẬN LIỀN", "sub": "Trượt dài trên bảng xếp hạng"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_FOREST_GIBBS)], "SKY SPORTS", "Morgan Gibbs-White ăn mừng cú đúp nhấn chìm Chelsea tại City Ground"),
            _slot("title", 0, [_url(DT_FOREST_CELEB)], "DÂN TRÍ / GETTY", "Nottingham Forest bùng nổ ngay từ phút thứ năm nhờ bàn thắng của Igor Jesus"),
            _slot("sentence", 1, [_url(SKY_FOREST_ALONSO)], "SKY SPORTS", "Thất bại 2-3 khiến Chelsea lún sâu vào khủng hoảng tại Ngoại hạng Anh"),
            _slot("sentence", 2, [_url(SKY_FOREST_IGOR)], "SKY SPORTS", "Igor Jesus lập công sớm trước khi Morgan Gibbs-White kết liễu đối thủ"),
            _slot("sentence", 3, [_url(SKY_CHELSEA_FOREST_2)], "SKY SPORTS", "Cú đúp của Emmanuel Emegha không đủ giúp Chelsea thoát khỏi trắng tay"),
            _slot("sentence", 4, [_url(DT_CHELSEA_GLOOM)], "DÂN TRÍ / GETTY", "Các cầu thủ Chelsea rời sân trong nỗi thất vọng sau trận thua thứ ba liên tiếp"),
        ],
    },

    # 11 (Nam — FOFANA BỊ CĐV CHELSEA LA Ó, HLV XABI ALONSO KÊU GỌI ĐOÀN KẾT)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "NGOẠI HẠNG ANH",
        "title": "Wesley Fofana bị chính cổ động viên Chelsea la ó, HLV Xabi Alonso thừa nhận khủng hoảng",
        "summary": (
            "Thất bại trước Nottingham Forest còn chứng kiến bầu không khí căng thẳng tột độ bên trong nội bộ Chelsea khi trung vệ Wesley Fofana trở thành tâm điểm chỉ trích của chính khán giả nhà. "
            "Ngay từ đầu trận, cầu thủ người Pháp liên tục bị cổ động viên Chelsea huýt sáo la ó dữ dội vì cuộc phỏng vấn tự phát trên YouTube gây tranh cãi trước đó. "
            "Áp lực tâm lý nặng nề khiến Fofana thi đấu thiếu tập trung, phạm lỗi dẫn đến quả phạt đền đầu hiệp hai, nhận thẻ vàng và bị huấn luyện viên Xabi Alonso rút khỏi sân sớm. "
            "Phát biểu sau trận khi Chelsea tụt xuống vị trí thứ tám, ông Alonso thừa nhận đội bóng đang trải qua giai đoạn khó khăn và kêu gọi học trò phải siết chặt đội ngũ ngay lập tức."
        ),
        "source": "BBC Sport / ESPN / Tuổi Trẻ",
        "news_source": "BBC SPORT / ESPN",
        "credit": "VNEXPRESS / AFP",
        "stat_badges": {
            "2": {"label": "CƠN GIẬN KHÁN ĐÀI", "value": "FOFANA BỊ FAN NHÀ LA Ó", "sub": "Phạm lỗi phạt đền rồi bị thay ra sớm"},
            "4": {"label": "ÁP LỰC ĐÈ NẶNG", "value": "CHELSEA RƠI XUỐNG HẠNG 8", "sub": "HLV Xabi Alonso kêu gọi toàn đội đoàn kết"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_FOFANA_GIBBS)], "VNEXPRESS / AFP", "Wesley Fofana có ngày thi đấu thảm họa khi bị chính cổ động viên Chelsea la ó"),
            _slot("title", 0, [_url(VNE_ALONSO_SAD)], "VNEXPRESS / AFP", "Huấn luyện viên Xabi Alonso đượm buồn nhìn Chelsea tụt xuống hạng tám"),
            _slot("sentence", 1, [_url(SKY_CHELSEA_ALONSO)], "SKY SPORTS", "Nội bộ Chelsea đối mặt sóng gió lớn sau chuỗi ba trận toàn thua"),
            _slot("sentence", 2, [_url(VNE_FOFANA_GIBBS)], "VNEXPRESS / AFP", "Khán giả Chelsea giận dữ phản ứng dữ dội mỗi khi Wesley Fofana chạm bóng"),
            _slot("sentence", 3, [_url(SKY_FOREST_ALONSO)], "SKY SPORTS", "Sai lầm dẫn đến quả phạt đền khiến Fofana sớm phải nhường chỗ trên sân"),
            _slot("sentence", 4, [_url(VNE_ALONSO_SAD)], "VNEXPRESS / AFP", "Xabi Alonso đứng trước bài toán nan giải để vực dậy tinh thần Chelsea"),
        ],
    },

    # 12 (Nữ — MANCHESTER UNITED GIA HẠN HỢP ĐỒNG VỚI BRUNO FERNANDES ĐẾN NĂM 2028)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "NGOẠI HẠNG ANH",
        "title": "Manchester United kích hoạt điều khoản gia hạn hợp đồng Bruno Fernandes đến năm 2028",
        "summary": (
            "Đêm ngày 27 tháng 11, ban lãnh đạo Manchester United chính thức kích hoạt điều khoản tự động gia hạn thêm một năm trong hợp đồng của đội trưởng Bruno Fernandes. "
            "Động thái dứt khoát này giúp Quỷ đỏ giữ chân ngôi sao 32 tuổi ở lại sân Old Trafford ít nhất tới mùa hè năm 2028. "
            "Việc kích hoạt điều khoản ngay lúc này giúp Manchester United khóa chặt nguy cơ bị các câu lạc bộ nước ngoài tiếp cận và ký thỏa thuận trước với Bruno Fernandes khi kỳ chuyển nhượng tháng Giêng mở cửa. "
            "Theo truyền thông Anh, hai bên sẽ tạm hoãn đàm phán hợp đồng dài hạn mới để toàn đội dồn toàn lực cải thiện phong độ dưới thời huấn luyện viên Mauricio Pochettino."
        ),
        "source": "BBC Sport / The Guardian / VnExpress",
        "news_source": "THE GUARDIAN / VNEXPRESS",
        "credit": "VNEXPRESS / AP",
        "stat_badges": {
            "2": {"label": "GIỮ CHÂN THỦ QUÂN", "value": "GIA HẠN ĐẾN HÈ 2028", "sub": "Kích hoạt điều khoản thêm 12 tháng"},
            "3": {"label": "CHẶN NGUY CƠ MẤT TRẮNG", "value": "KHÓA CỬA CHUYỂN NHƯỢNG", "sub": "Ngăn các đội bóng ngoài Anh tiếp cận"},
        },
        "slots": [
            _slot("title", 0, [_url(VNE_BRUNO_1)], "VNEXPRESS / AP", "Bruno Fernandes tiếp tục gắn bó với Manchester United tới mùa hè năm 2028"),
            _slot("title", 0, [_url(VNE_BRUNO_2)], "VNEXPRESS / AP", "Đội trưởng 32 tuổi vẫn là hạt nhân lối chơi không thể thay thế tại Old Trafford"),
            _slot("sentence", 1, [_url(VNE_BRUNO_1)], "VNEXPRESS / AP", "Manchester United kích hoạt điều khoản gia hạn hợp đồng với Bruno Fernandes"),
            _slot("sentence", 2, [_ddgs("Bruno Fernandes Manchester United Old Trafford 2026")], "BING SEARCH", "Tiền vệ người Bồ Đào Nha được đảm bảo tương lai thêm một năm tại Old Trafford"),
            _slot("sentence", 3, [_url(VNE_BRUNO_2)], "VNEXPRESS / AP", "Quyết định kịp thời ngăn chặn các đối thủ châu Âu chèo kéo Bruno Fernandes"),
            _slot("sentence", 4, [_ddgs("Mauricio Pochettino Manchester United coach")], "BING SEARCH", "Huấn luyện viên Mauricio Pochettino cần sự ổn định từ thủ quân để vực dậy đội bóng"),
        ],
    },

    # 13 (Nam — ÁP LỰC BUỘC CHỦ SỞ HỮU MAN CITY BÁN CLB TRƯỚC ĐẠI CHIẾN ARSENAL)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "NGOẠI HẠNG ANH",
        "title": "Các CLB Ngoại hạng Anh đề xuất buộc chủ sở hữu Man City bán đội bóng trước đại chiến Arsenal",
        "summary": (
            "Theo tiết lộ độc quyền từ BBC Sport ngày 27 tháng 11, lãnh đạo cấp cao của ba câu lạc bộ đối thủ tại Ngoại hạng Anh đang thúc đẩy phương án buộc chủ sở hữu Manchester City phải bán đội bóng. "
            "Đề xuất cứng rắn này được đưa ra sau những bê bối vi phạm quy tắc tài chính giai đoạn 2009 đến 2018 cùng làn sóng chuẩn bị hồ sơ kiện đòi bồi thường của nhiều ông lớn. "
            "Sóng gió pháp lý ập đến đúng lúc thầy trò huấn luyện viên Enzo Maresca rơi vào chuỗi bốn trận liên tiếp không thắng và đối mặt chuyến làm khách đầy giông bão tới sân của đội đầu bảng Arsenal cuối tuần này. "
            "Với 28 điểm và khoảng cách sáu điểm nhiều hơn Man City, Arsenal dưới sự dẫn dắt của Mikel Arteta thậm chí tuyên bố hướng tới cột mốc 100 điểm mùa giải năm nay."
        ),
        "source": "BBC Sport / The Guardian / Tuổi Trẻ",
        "news_source": "BBC SPORT / THE GUARDIAN",
        "credit": "TUỔI TRẺ / AP",
        "stat_badges": {
            "1": {"label": "SỨC ÉP THƯỢNG TẦNG", "value": "ĐỀ XUẤT BUỘC BÁN MAN CITY", "sub": "Lãnh đạo 3 CLB đối thủ lên tiếng với BBC"},
            "4": {"label": "ĐẠI CHIẾN EMIRATES", "value": "ARSENAL HƠN MAN CITY 6 ĐIỂM", "sub": "Thầy trò Enzo Maresca sa sút 4 trận liền"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_ARS_MC)], "TUỔI TRẺ / AP", "Arsenal sẵn sàng tiếp đón Manchester City đang chịu áp lực bủa vây"),
            _slot("title", 0, [_ddgs("Etihad Stadium Manchester City Premier League")], "BING SEARCH", "Tương lai giới chủ Manchester City trở thành đề tài nóng tại Ngoại hạng Anh"),
            _slot("sentence", 1, [_ddgs("Manchester City football club Etihad")], "BING SEARCH", "Các đối thủ tại Ngoại hạng Anh đòi áp dụng chế tài mạnh nhất với Man City"),
            _slot("sentence", 2, [_ddgs("Erling Haaland Manchester City Premier League")], "BING SEARCH", "Ồn ào tài chính kéo dài suốt gần một thập kỷ khiến Man City đứng trước sức ép lớn"),
            _slot("sentence", 3, [_ddgs("Enzo Maresca Manchester City manager")], "BING SEARCH", "Huấn luyện viên Enzo Maresca loay hoay chặn đà sa sút trước đại chiến Arsenal"),
            _slot("sentence", 4, [_url(TT_ARS_MC)], "TUỔI TRẺ / AP", "Arsenal đang dẫn đầu bảng đầy tự tin với tham vọng chinh phục 100 điểm"),
        ],
    },

    # 14 (Nữ — TOTTENHAM NHẬN HUNG TIN SAVIO NGHỈ TỚI 80 NGÀY)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "NGOẠI HẠNG ANH",
        "title": "Tottenham tổn thất nặng khi ngôi sao chạy cánh Savio có nguy cơ nghỉ tới 80 ngày",
        "summary": (
            "Câu lạc bộ Tottenham Hotspur vừa đón nhận thông tin không vui về lực lượng trước giai đoạn thi đấu dày đặc nhất mùa giải. "
            "Huấn luyện viên trưởng Roberto De Zerbi xác nhận cầu thủ chạy cánh người Brazil Savio đã tái phát chấn thương gân kheo ngay sau khi vừa bình phục để góp mặt ở trận thắng Ipswich Town 2-0. "
            "Trước đó, ngôi sao trẻ này từng phải ngồi ngoài suốt sáu tuần, nhưng lần tái phát mới nhất nghiêm trọng hơn dự kiến ban đầu rất nhiều. "
            "Ông De Zerbi cho biết Savio chắc chắn bỏ lỡ toàn bộ loạt trận dịp Giáng sinh và có thể phải rời xa sân cỏ từ 50 đến 80 ngày."
        ),
        "source": "BBC Football",
        "news_source": "BBC FOOTBALL",
        "credit": "BING SEARCH",
        "stat_badges": {
            "2": {"label": "TÁI PHÁT GÂN KHEO", "value": "SAVIO LỠ DỊP GIÁNG SINH", "sub": "Vừa trở lại sau 6 tuần dưỡng thương"},
            "4": {"label": "THỜI GIAN VẮNG MẶT", "value": "NGHỈ TỪ 50 ĐẾN 80 NGÀY", "sub": "Tổn thất lớn cho HLV Roberto De Zerbi"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Savinho Savio Tottenham Hotspur football")], "BING SEARCH", "Savio đối mặt nguy cơ ngồi ngoài tới 80 ngày vì tái phát chấn thương"),
            _slot("title", 0, [_ddgs("Roberto De Zerbi manager football touchline")], "BING SEARCH", "Huấn luyện viên Roberto De Zerbi đau đầu bài toán nhân sự dịp Giáng sinh"),
            _slot("sentence", 1, [_ddgs("Tottenham Hotspur Stadium Premier League")], "BING SEARCH", "Tottenham chịu tổn thất nghiêm trọng trên hàng công trước lịch thi đấu cuối năm"),
            _slot("sentence", 2, [_ddgs("Savio Brazil football winger match")], "BING SEARCH", "Cầu thủ người Brazil vừa tái xuất ở trận thắng Ipswich đã lập tức đổ gục"),
            _slot("sentence", 3, [_ddgs("football injury hamstring pitch medical")], "BING SEARCH", "Chấn thương gân kheo dai dẳng khiến quá trình hồi phục bị kéo dài"),
            _slot("sentence", 4, [_ddgs("Roberto De Zerbi Tottenham coach")], "BING SEARCH", "Chiến lược gia người Italy phải tìm phương án thay thế trong ít nhất hai tháng tới"),
        ],
    },

    # 15 (Nam — BẠO LOẠN SÂN CỎ CHÂU ÂU KHIẾN TỔNG THỐNG PHÁP MACRON LÊN TIẾNG)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "BÓNG ĐÁ CHÂU ÂU",
        "title": "Bạo loạn sân cỏ châu Âu khiến Tổng thống Pháp Emmanuel Macron lên tiếng",
        "summary": (
            "Loạt trận cúp châu Âu vừa qua bị phủ bóng đen bởi những cuộc đụng độ bạo lực nghiêm trọng trên khán đài lẫn bên ngoài sân vận động. "
            "Nghiêm trọng nhất là tình trạng hỗn loạn giữa cổ động viên tại sân Vélodrome trong trận Marseille tiếp đón đại diện Bulgaria Levski Sofia khiến nhiều người phải nhập viện cấp cứu. "
            "Trước tính chất nghiêm trọng của vụ việc, Tổng thống Pháp Emmanuel Macron đã lên tiếng chỉ trích gay gắt, khẳng định bạo lực hoàn toàn không có chỗ đứng trong thể thao và xã hội văn minh. "
            "Ngoài nước Pháp, trận đấu giữa Besiktas và Hapoel Be'er-Sheva tại Georgia cũng bị gián đoạn tạm thời sau xô xát giữa cảnh sát với nhóm cổ động viên quá khích."
        ),
        "source": "BBC Sport",
        "news_source": "BBC SPORT",
        "credit": "BING SEARCH",
        "stat_badges": {
            "2": {"label": "CHẢO LỬA VÉLODROME", "value": "NHIỀU CĐV NHẬP VIỆN", "sub": "Hỗn loạn tại trận Marseille vs Levski Sofia"},
            "3": {"label": "PHẢN ỨNG CẤP CAO", "value": "TỔNG THỐNG MACRON LÊN ÁN", "sub": "Kiên quyết bài trừ bạo lực sân cỏ"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Stade Velodrome Marseille fans football match")], "BING SEARCH", "Sân Vélodrome xảy ra cảnh hỗn loạn đáng tiếc trong khuôn khổ Europa League"),
            _slot("title", 0, [_ddgs("Emmanuel Macron France president press")], "BING SEARCH", "Tổng thống Pháp Emmanuel Macron lên tiếng mạnh mẽ trước nạn bạo lực bóng đá"),
            _slot("sentence", 1, [_ddgs("Europa League football stadium night fans")], "BING SEARCH", "Nhiều trận đấu tại đấu trường châu Âu bị ảnh hưởng bởi cổ động viên quá khích"),
            _slot("sentence", 2, [_ddgs("Olympique Marseille fans stadium flares")], "BING SEARCH", "Cảnh sát đã phải can thiệp vất vả trong cuộc đối đầu Marseille và Levski Sofia"),
            _slot("sentence", 3, [_ddgs("Emmanuel Macron Elysee speech")], "BING SEARCH", "Nhà lãnh đạo nước Pháp yêu cầu xử lý nghiêm hành vi gây rối trên khán đài"),
            _slot("sentence", 4, [_ddgs("Besiktas stadium fans football match")], "BING SEARCH", "Căng thẳng cũng xảy ra tại Georgia trong trận đấu của đại diện Thổ Nhĩ Kỳ"),
        ],
    },

    # 16 (Nữ — WERDER BREMEN GỠ HÒA 3-3 TRƯỚC GLADBACH Ở PHÚT BÙ GIỜ 90+2)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "BUNDESLIGA ĐỨC",
        "title": "Bundesliga kịch tính: Werder Bremen gỡ hòa 3-3 trước Mönchengladbach ở phút 90+2",
        "summary": (
            "Trận đấu sớm vòng 11 Bundesliga rạng sáng 28 tháng 11 tại sân Weser-Stadion mang đến bữa tiệc sáu bàn thắng nghẹt thở giữa Werder Bremen và đội bét bảng Borussia Mönchengladbach. "
            "Gladbach tưởng như đã nắm chắc chiến thắng khi vượt lên dẫn trước 3-1 đến phút 78 nhờ quả phạt đền của Kevin Diks cùng cú đúp từ Franck Honorat. "
            "Tuy nhiên, tinh thần không bỏ cuộc giúp đội chủ nhà vùng lên mạnh mẽ với bàn rút ngắn của Eren Dinkçi ở phút 85 để hoàn tất cú đúp cá nhân. "
            "Đúng phút bù giờ thứ hai của hiệp hai, tiền đạo kỳ cựu Niclas Füllkrug tỏa sáng ấn định trận hòa 3-3 điên rồ, giữ Bremen đứng hạng sáu còn Gladbach tiếp tục chôn chân cuối bảng."
        ),
        "source": "BBC Sport / Bundesliga",
        "news_source": "BBC SPORT",
        "credit": "BING SEARCH",
        "stat_badges": {
            "1": {"label": "VÒNG 11 BUNDESLIGA", "value": "BREMEN 3-3 GLADBACH", "sub": "Rượt đuổi 6 bàn thắng tại Weser-Stadion"},
            "4": {"label": "NGƯỜI HÙNG PHÚT 90+2", "value": "FÜLLKRUG GIẬT LẠI 1 ĐIỂM", "sub": "Gladbach đánh rơi chiến thắng dù dẫn 3-1"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Werder Bremen Niclas Fullkrug Bundesliga goal")], "BING SEARCH", "Niclas Füllkrug ghi bàn phút bù giờ giúp Werder Bremen giật lại một điểm"),
            _slot("title", 0, [_ddgs("Werder Bremen Weserstadion Bundesliga match")], "BING SEARCH", "Weser-Stadion bùng nổ với màn rượt đuổi tỷ số sáu bàn thắng"),
            _slot("sentence", 1, [_ddgs("Borussia Monchengladbach Bundesliga football")], "BING SEARCH", "Đội cuối bảng Mönchengladbach tạo thế trận sòng phẳng ngay trên sân khách"),
            _slot("sentence", 2, [_ddgs("Franck Honorat Borussia Monchengladbach")], "BING SEARCH", "Franck Honorat lập cú đúp tưởng chừng mang về thắng lợi cho đội khách"),
            _slot("sentence", 3, [_ddgs("Eren Dinkci Werder Bremen football")], "BING SEARCH", "Eren Dinkçi thắp lại hy vọng cho Bremen bằng cú đúp vào lưới đối thủ"),
            _slot("sentence", 4, [_ddgs("Niclas Fullkrug Germany football celebration")], "BING SEARCH", "Pha lập công phút 90+2 của Füllkrug khiến đội bét bảng tiếp tục lún sâu"),
        ],
    },

    # 17 (Nam — MARC MÁRQUEZ BẤT NGỜ TUYÊN BỐ GIẢI NGHỆ MOTOGP Ở TUỔI 33)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "CHẤN ĐỘNG MOTOGP",
        "title": "Huyền thoại Marc Márquez bất ngờ tuyên bố giải nghệ MotoGP ở tuổi 33",
        "summary": (
            "Làng đua xe mô tô thế giới rúng động trong ngày 27 tháng 11 khi ngôi sao Marc Márquez bất ngờ thông báo sẽ giải nghệ ngay sau khi chặng cuối Valencia Grand Prix khép lại. "
            "Quyết định chấn động được tay đua 33 tuổi đưa ra ngay trong garage đội Ducati trước buổi tập đầu tiên, chỉ ít ngày sau khi anh cân bằng kỷ lục tám chức vô địch MotoGP thế giới tại Bồ Đào Nha. "
            "Márquez thừa nhận anh đã ấp ủ ý định dừng lại từ sau chặng Nhật Bản hồi tháng mười, bởi những di chứng nặng nề ở vai tay phải cùng chứng nhìn đôi tái phát sau các vụ tai nạn tại Indonesia và Le Mans khiến anh thực sự cảm thấy sợ hãi. "
            "Sự rút lui trên đỉnh cao vinh quang của huyền thoại người Tây Ban Nha đánh dấu cái kết cho một trong những sự nghiệp vĩ đại nhất lịch sử đường đua tốc độ hai bánh."
        ),
        "source": "BBC Sport / MotoGP / Motorsport",
        "news_source": "BBC SPORT / MOTOGP",
        "credit": "BING SEARCH",
        "stat_badges": {
            "2": {"label": "CHIA TAY TRÊN ĐỈNH CAO", "value": "8 LẦN VÔ ĐỊCH MOTOGP", "sub": "Thông báo bất ngờ trước chặng Valencia GP"},
            "3": {"label": "NỖI ÁM ẢNH CHẤN THƯƠNG", "value": "VAI PHẢI & CHỨNG NHÌN ĐÔI", "sub": "Márquez quyết định giải nghệ ở tuổi 33"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Marc Marquez Ducati MotoGP 2026")], "BING SEARCH", "Marc Márquez tuyên bố chia tay MotoGP sau mùa giải 2026 trên đỉnh vinh quang"),
            _slot("title", 0, [_ddgs("Marc Marquez MotoGP world champion trophy")], "BING SEARCH", "Tay đua người Tây Ban Nha vừa chạm mốc tám danh hiệu vô địch hạng đua cao nhất"),
            _slot("sentence", 1, [_ddgs("Marc Marquez Valencia MotoGP press")], "BING SEARCH", "Thông báo của Márquez trước chặng Valencia khiến giới mộ điệu toàn cầu sửng sốt"),
            _slot("sentence", 2, [_ddgs("Marc Marquez Ducati garage MotoGP")], "BING SEARCH", "Anh chia sẻ bức thông điệp chia tay ngay tại garage của đội đua Ducati"),
            _slot("sentence", 3, [_ddgs("Marc Marquez crash injury MotoGP")], "BING SEARCH", "Nỗi lo về chấn thương vai tay và chứng nhìn đôi buộc Márquez phải dừng lại"),
            _slot("sentence", 4, [_ddgs("Marc Marquez waving fans MotoGP")], "BING SEARCH", "Chặng Valencia cuối tuần này sẽ là lần cuối người hâm mộ thấy số 93 thi đấu"),
        ],
    },

    # 18 (Nữ — F1 QATAR GP: KIMI ANTONELLI VÀ MERCEDES THỐNG TRỊ NGÀY TẬP ĐẦU)
    {
        "id": 18,
        "art_id": "art_18",
        "group": "FORMULA 1 • QATAR GP",
        "title": "F1 Qatar GP: Kimi Antonelli và Mercedes thống trị ngày tập đầu, Hamilton gặp sự cố",
        "summary": (
            "Chặng đua áp chót Qatar Grand Prix rạng sáng 28 tháng 11 khởi tranh với sự áp đảo tuyệt đối từ đội đua Mercedes trên đường chạy Losail dưới ánh đèn đêm. "
            "Tân vương trẻ Kimi Antonelli lập thành tích nhanh nhất ở cả hai phiên tập đầu tiên với thông số 1 phút 23,077 giây ở phiên hai, xếp ngay trên đồng đội George Russell và tay đua Lando Norris của McLaren. "
            "Buổi tập hai liên tục bị gián đoạn bởi hai lá cờ đỏ sau tình huống xoay xe của Charles Leclerc và pha sa lầy xuống bãi sỏi tốc độ cao của Pierre Gasly. "
            "Đáng lo hơn cả cho Ferrari, tay đua Lewis Hamilton gặp trục trặc kỹ thuật nghi liên quan tới bộ phận động lực cuối buổi tập, đứng trước nguy cơ bị phạt bậc xuất phát cho cuộc đua chính."
        ),
        "source": "BBC Sport / Sky Sports / Formula 1",
        "news_source": "BBC SPORT / SKY SPORTS",
        "credit": "SKY SPORTS",
        "stat_badges": {
            "2": {"label": "NHẤT CẢ 2 PHIÊN TẬP", "value": "ANTONELLI 1:23.077", "sub": "Mercedes chiếm trọn 2 vị trí dẫn đầu trước Norris"},
            "4": {"label": "ÁM ẢNH FERRARI", "value": "HAMILTON LỖI ĐỘNG CƠ", "sub": "Charles Leclerc xoay xe gây gián đoạn FP2"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_F1_QATAR)], "SKY SPORTS", "Các xe đua Formula 1 bước vào ngày chạy thử nóng bỏng tại Qatar Grand Prix"),
            _slot("title", 0, [_ddgs("Kimi Antonelli Mercedes F1 car 2026")], "BING SEARCH", "Kimi Antonelli thể hiện tốc độ vượt trội để dẫn đầu cả hai phiên tập tại Losail"),
            _slot("sentence", 1, [_ddgs("Lusail International Circuit Qatar F1 night")], "BING SEARCH", "Mercedes hoàn toàn làm chủ đường đua Losail trong điều kiện thi đấu ban đêm"),
            _slot("sentence", 2, [_ddgs("George Russell Mercedes F1 2026")], "BING SEARCH", "George Russell bám sát ngay sau Antonelli giúp đội đua Đức tạo cách biệt lớn"),
            _slot("sentence", 3, [_url(SKY_F1_LECLERC)], "SKY SPORTS", "Charles Leclerc mất lái xoay xe khiến phiên tập hai xuất hiện cờ đỏ gián đoạn"),
            _slot("sentence", 4, [_ddgs("Lewis Hamilton Ferrari F1 2026")], "BING SEARCH", "Lewis Hamilton đối diện nguy cơ nhận án phạt sau sự cố kỹ thuật cuối ngày"),
        ],
    },

    # 19 (Nam — TYSON FURY ĐƯỢC CẤP PHÉP THƯỢNG ĐÀI ĐẠI CHIẾN ANTHONY JOSHUA)
    {
        "id": 19,
        "art_id": "art_19",
        "group": "QUYỀN ANH HẠNG NẶNG",
        "title": "Tyson Fury chính thức được cấp phép thượng đài đại chiến Anthony Joshua tháng 12",
        "summary": (
            "Ủy ban Quản lý Quyền anh Vương quốc Anh vừa xác nhận tay đấm Tyson Fury đủ điều kiện sức khỏe để thượng đài trận siêu kinh điển hạng nặng gặp Anthony Joshua vào ngày 11 tháng 12 tại Cardiff. "
            "Trước đó ít ngày, trận đấu bom tấn đứng trước nguy cơ đổ bể khi bộ phim tài liệu mới hé lộ phát ngôn của vợ Fury cho rằng anh từng mắc chứng tâm thần phân liệt sau chiến thắng năm 2015. "
            "Ngay khi cơ quan chuyên môn vào cuộc rà soát giấy phép thi đấu, bà Paris Fury đã chính thức đính chính và rút lại tuyên bố trên vì khẳng định chồng mình chưa từng nhận chẩn đoán bệnh lý đó. "
            "Quản lý của Tyson Fury cho biết chính Anthony Joshua đã gọi điện hỏi thăm trực tiếp và cả hai phía hiện hoàn toàn yên tâm chuẩn bị cho cuộc so găng lịch sử."
        ),
        "source": "BBC Sport / Sky Sports / The Guardian",
        "news_source": "BBC SPORT / SKY SPORTS",
        "credit": "SKY SPORTS",
        "stat_badges": {
            "1": {"label": "ĐÈN XANH TỪ ỦY BAN ANH", "value": "FURY VS JOSHUA DIỄN RA", "sub": "Ấn định thượng đài ngày 11/12 tại Cardiff"},
            "3": {"label": "KHÉP LẠI SÓNG GIÓ", "value": "ĐÍNH CHÍNH HỒ SƠ Y TẾ", "sub": "Paris Fury rút lại thông tin gây hiểu lầm"},
        },
        "slots": [
            _slot("title", 0, [_url(SKY_FURY)], "SKY SPORTS", "Tyson Fury nhận giấy phép y tế để bước vào trận đấu mong chờ với Anthony Joshua"),
            _slot("title", 0, [_ddgs("Anthony Joshua boxing heavyweight")], "BING SEARCH", "Anthony Joshua sẵn sàng cho cuộc so găng lịch sử của quyền anh xứ sương mù"),
            _slot("sentence", 1, [_url(SKY_FURY)], "SKY SPORTS", "Trận đại chiến ngày 11 tháng 12 tại Cardiff chính thức được bảo đảm tổ chức"),
            _slot("sentence", 2, [_ddgs("Tyson Fury Paris Fury documentary")], "BING SEARCH", "Chi tiết nhạy cảm trong phim tài liệu từng khiến giới quyền anh xôn xao"),
            _slot("sentence", 3, [_ddgs("Tyson Fury boxing training gym")], "BING SEARCH", "Gia đình Fury kịp thời đính chính nhằm làm rõ tình trạng sức khỏe của võ sĩ"),
            _slot("sentence", 4, [_ddgs("Tyson Fury Anthony Joshua face off boxing")], "BING SEARCH", "Người hâm mộ toàn cầu chờ đợi màn chạm trán nảy lửa giữa hai cựu vương"),
        ],
    },

    # 20 (Nữ — DAVIS CUP 2026: ITALY HẠ CH SÉC 2-1, LẦN THỨ 4 LIÊN TIẾP VÀO CHUNG KẾT)
    {
        "id": 20,
        "art_id": "art_20",
        "group": "QUẦN VỢT DAVIS CUP",
        "title": "Davis Cup 2026: Đương kim vô địch Italy hạ CH Séc 2-1, lần thứ 4 liên tiếp vào chung kết",
        "summary": (
            "Tại trận bán kết thứ nhất Davis Cup Final 8 diễn ra ở Bologna tối ngày 27 tháng 11, đội tuyển quần vợt chủ nhà Italy xuất sắc vượt qua Cộng hòa Séc với tỷ số 2-1. "
            "Lorenzo Musetti giúp đội đương kim vô địch vươn lên dẫn trước bằng chiến thắng 6-3, 6-4 trước Jakub Menšík, trước khi Jiří Lehečka hạ Flavio Cobolli sau ba set để đưa cặp đấu vào trận đôi quyết định. "
            "Dưới sự cổ vũ cuồng nhiệt của khán giả quê nhà, cặp Lorenzo Musetti và Andrea Vavassori bản lĩnh thắng ngược Jiří Lehečka và Tomáš Macháč với tỷ số 3-6, 6-1, 7-6. "
            "Chiến thắng nghẹt thở ở loạt tie-break set ba đưa Italy có lần thứ tư liên tiếp góp mặt trong trận chung kết tranh đĩa bạc danh giá."
        ),
        "source": "Davis Cup / TennisNow",
        "news_source": "DAVIS CUP",
        "credit": "BING SEARCH",
        "stat_badges": {
            "1": {"label": "BÁN KẾT 1 TẠI BOLOGNA", "value": "ITALY THẮNG CH SÉC 2-1", "sub": "Vào chung kết Davis Cup năm thứ 4 liên tiếp"},
            "3": {"label": "TRẬN ĐÔI NGHẸT THỞ", "value": "MUSETTI / VAVASSORI 7-6(4)", "sub": "Ngược dòng đánh bại Lehečka / Macháč"},
        },
        "slots": [
            _slot("title", 0, [_ddgs("Lorenzo Musetti Italy Davis Cup tennis")], "BING SEARCH", "Lorenzo Musetti ghi dấu ấn ở cả nội dung đơn lẫn đôi đưa Italy vào chung kết"),
            _slot("title", 0, [_ddgs("Andrea Vavassori Lorenzo Musetti Davis Cup")], "BING SEARCH", "Cặp đôi Italy ăn mừng vỡ òa sau chiến thắng tie-break set quyết định"),
            _slot("sentence", 1, [_ddgs("Davis Cup Bologna Italy tennis stadium")], "BING SEARCH", "Chủ nhà Italy tiếp tục chuỗi thống trị ấn tượng tại đấu trường Davis Cup"),
            _slot("sentence", 2, [_ddgs("Jiri Lehecka Czech Republic Davis Cup")], "BING SEARCH", "Jiří Lehečka thắp lại hy vọng cho Cộng hòa Séc bằng thắng lợi ở trận đơn thứ hai"),
            _slot("sentence", 3, [_ddgs("Italy Davis Cup team celebration Bologna")], "BING SEARCH", "Bản lĩnh ở loạt tie-break set ba giúp bộ đôi chủ nhà khuất phục đối thủ"),
            _slot("sentence", 4, [_ddgs("Davis Cup trophy tennis final")], "BING SEARCH", "Italy tiến gần hơn tới mục tiêu bảo vệ ngôi vương Davis Cup ngay trên sân nhà"),
        ],
    },

    # 21 (Nam — BỒ ĐÀO NHA CÂN NHẮC THAY HLV TRONG TRẬN TRI ÂN RONALDO & CHIA SẺ CỦA GUARDIOLA)
    {
        "id": 21,
        "art_id": "art_21",
        "group": "BÓNG ĐÁ THẾ GIỚI",
        "title": "Bồ Đào Nha có thể thay HLV trưởng ở trận tri ân Cristiano Ronaldo, Guardiola chia sẻ góc khuất",
        "summary": (
            "Theo nguồn tin từ ESPN, Liên đoàn Bóng đá Bồ Đào Nha đang tính phương án đặc biệt là không để huấn luyện viên Jorge Jesus cầm quân trong trận đấu chia tay chính thức của siêu sao Cristiano Ronaldo. "
            "Nguyên nhân xuất phát từ mối quan hệ rạn nứt sâu sắc giữa đôi bên khiến tiền đạo 41 tuổi bất ngờ tuyên bố giã từ đội tuyển quốc gia hồi đầu tháng và vắng mặt trong buổi lễ vinh danh. "
            "Cựu thuyền trưởng Luiz Felipe Scolari, người từng trao cơ hội ra mắt đội tuyển cho Ronaldo vào năm 2003, đang được cân nhắc mời trở lại dẫn dắt một trận giao hữu tri ân trọn vẹn. "
            "Cũng bàn về cái kết của Ronaldo ở đội tuyển khi trả lời phỏng vấn kênh Romario TV, huấn luyện viên Pep Guardiola bày tỏ sự trân trọng dành cho huyền thoại này và khẳng định bóng đá luôn cần khép lại bằng sự tôn vinh xứng đáng."
        ),
        "source": "ESPN / Dân Trí / VnExpress",
        "news_source": "ESPN / DÂN TRÍ / VNEXPRESS",
        "credit": "DÂN TRÍ / GETTY",
        "stat_badges": {
            "1": {"label": "TRẬN TRI ÂN CRISTIANO RONALDO", "value": "KHÔNG DÙNG HLV JORGE JESUS", "sub": "Mâu thuẫn nội bộ khiến đôi bên xa cách"},
            "3": {"label": "PHƯƠNG ÁN ĐẶC BIỆT", "value": "MỜI LẠI LUIZ FELIPE SCOLARI", "sub": "Người trao cơ hội ra mắt cho CR7 năm 2003"},
        },
        "slots": [
            _slot("title", 0, [_url(DT_CR7_PORTUGAL)], "DÂN TRÍ / GETTY", "Cristiano Ronaldo vẫn chờ trận đấu chia tay trọn vẹn cùng đội tuyển Bồ Đào Nha"),
            _slot("title", 0, [_url(DT_JESUS_POR)], "DÂN TRÍ / GETTY", "Mâu thuẫn với huấn luyện viên Jorge Jesus là nguyên nhân khiến CR7 giã từ đội tuyển"),
            _slot("sentence", 1, [_url(DT_CR7_PORTUGAL)], "DÂN TRÍ / GETTY", "Bồ Đào Nha muốn tổ chức trận tri ân êm đẹp cho cầu thủ ghi bàn vĩ đại nhất lịch sử"),
            _slot("sentence", 2, [_url(DT_JESUS_POR)], "DÂN TRÍ / GETTY", "Sự căng thẳng giữa Ronaldo và Jorge Jesus khiến phương án thay tướng được tính tới"),
            _slot("sentence", 3, [_ddgs("Luiz Felipe Scolari coach Cristiano Ronaldo Portugal")], "BING SEARCH", "Cựu huấn luyện viên Luiz Felipe Scolari là ứng viên giàu ý nghĩa cho trận chia tay"),
            _slot("sentence", 4, [_ddgs("Pep Guardiola Romario interview football")], "BING SEARCH", "Pep Guardiola lần đầu trải lòng sau khi rời Man City trên kênh Romario TV"),
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
            "Ở vòng chín giải hạng Nhất Quốc gia tối 27 tháng 11, câu lạc bộ Công An Nhân Dân hạ Đại học Văn Hiến 1-0 nhờ bàn thắng phút 87 của Trần Minh Vương, còn tiền đạo Vũ Minh Hiếu kiến tạo giúp câu lạc bộ Hưng Yên thắng Thái Nguyên 1-0 để vươn lên đầu bảng với 20 điểm. "
            "Tại các môn khác của Đại hội Thể thao toàn quốc, nhà vô địch cờ tướng thế giới Lại Lý Huynh để thua kỳ thủ Hà Văn Tiến ở nội dung cờ nhanh đôi nam, cơ thủ 55 tuổi Trần Lê Anh Tuấn giành huy chương vàng English Billiards sau gần bảy giờ thi đấu, trong khi nam sinh lớp 10 Trần Khởi Minh đoạt cú đúp huy chương vàng môn xe đạp. "
            "Trong nước và khu vực, câu lạc bộ Thành phố Hồ Chí Minh hoàn tất thủ tục đưa 18 cầu thủ trẻ sang đào tạo ba năm tại Celta Vigo ở Tây Ban Nha, Indonesia lên kế hoạch đăng cai giải vô địch Đông Á dự kiến mời đội tuyển Việt Nam, còn giải đua xe Rally quốc tế chuẩn FIA đầu tiên mang tên Trường Sơn Rally công bố khởi tranh đầu tháng 12 tại Quảng Trị. "
            "Tại đấu trường bóng đá nữ Anh, huấn luyện viên Renée Slegers chính thức chia tay đội nữ Arsenal chỉ 18 tháng sau chức vô địch Champions League vì chuỗi sáu trận hòa liên tiếp trên sân nhà. "
            "Ở môn cầu lông, tay vợt nổi tiếng Thái Lan Pitchamon Opatniputh nhận án cấm thi đấu ba tháng do mẫu thử dương tính với chất cấm trước thềm ASIAD 20. "
            "Tại Mỹ, Pittsburgh Steelers thắng Denver Broncos 27-5 ở trận NFL Black Friday sau khi thanh lý hợp đồng Aaron Rodgers, còn Golden State Warriors xác nhận Stephen Curry phải nghỉ thêm ít nhất ba trận vì chấn thương cơ chéo bụng. "
            "Khép lại bản tin, tiền đạo người Brazil Helinho tại giải vô địch Mexico nhận cơn mưa lời khen về tinh thần fair-play khi chủ động đá bóng ra biên trong pha đối mặt, từ bỏ cơ hội lập hat-trick để đối thủ chấn thương được chăm sóc y tế kịp thời."
        ),
        "source": "Thanh Niên / Tuổi Trẻ / Dân Trí / Sky Sports / ESPN",
        "news_source": "ĐIỂM ĐỌC TỔNG HỢP",
        "credit": "TUỔI TRẺ / SKY SPORTS",
        "stat_badges": {
            "1": {"label": "HẠNG NHẤT QUỐC GIA", "value": "CAND & HƯNG YÊN THẮNG 1-0", "sub": "Minh Vương lập công phút 87; Hưng Yên dẫn đầu"},
            "2": {"label": "ĐẠI HỘI TDTT 2026", "value": "LÃI LÝ HUYNH THUA CỜ NHANH", "sub": "Trần Khởi Minh 15 tuổi đoạt 2 HCV xe đạp"},
            "5": {"label": "ÁN PHẠT CẦU LÔNG", "value": "PITCHAMON CẤM 3 THÁNG", "sub": "Vi phạm kiểm tra doping trước ASIAD 20"},
            "6": {"label": "NFL & NBA", "value": "STEELERS 27-5 • CURRY NGHỈ", "sub": "Stephen Curry lỡ ít nhất 3 trận tiếp theo"},
        },
        "slots": [
            _slot("title", 0, [_url(TT_MINHVUONG)], "TUỔI TRẺ / VPF", "Minh Vương tỏa sáng phút 87 giúp Công An Nhân Dân giành trọn ba điểm"),
            _slot("title", 0, [_url(TT_HAVANTIEN)], "TUỔI TRẺ / LĐCTVN", "Kỳ thủ Hà Văn Tiến gây bất ngờ khi đánh bại nhà vô địch thế giới Lại Lý Huynh"),
            _slot("title", 0, [_url(SKY_STEELERS)], "SKY SPORTS", "Pittsburgh Steelers đánh bại Denver Broncos 27-5 ở ngày hội Black Friday"),
            # Câu 1: Hạng Nhất (Minh Vương + Vũ Minh Hiếu)
            _slot("sentence", 1, [_url(TT_MINHVUONG)], "TUỔI TRẺ / VPF", "Trần Minh Vương ăn mừng bàn thắng muộn cho Công An Nhân Dân"),
            _slot("sentence", 1, [_url(TT_MINHHIEU)], "TUỔI TRẺ / HYFC", "Vũ Minh Hiếu kiến tạo giúp câu lạc bộ Hưng Yên chiếm đỉnh bảng giải hạng Nhất"),
            # Câu 2: Đại hội (Hà Văn Tiến / Trần Lê Anh Tuấn / Trần Khởi Minh)
            _slot("sentence", 2, [_url(TT_HAVANTIEN)], "TUỔI TRẺ / LĐCTVN", "Hà Văn Tiến xuất sắc đánh bại Lại Lý Huynh ở nội dung cờ nhanh đôi nam"),
            _slot("sentence", 2, [_url(TN_BILLIARDS_55)], "THANH NIÊN / P", "Cơ thủ 55 tuổi Trần Lê Anh Tuấn giải cơn khát vàng cho Billiards TP.HCM"),
            _slot("sentence", 2, [_url(TN_KHOIMINH)], "THANH NIÊN / PHẠM HUY", "Nam sinh lớp 10 Trần Khởi Minh lập kỳ tích với hai HCV xe đạp Đại hội"),
            # Câu 3: Celta Vigo / EAFF / Trường Sơn Rally
            _slot("sentence", 3, [_url(TT_TPHCM_SPAIN)], "TUỔI TRẺ / CAO TOÀN", "CLB TP.HCM đưa 18 cầu thủ trẻ sang Tây Ban Nha đào tạo bài bản tại Celta Vigo"),
            _slot("sentence", 3, [_url(TN_VN_EAFF)], "THANH NIÊN / MINH HOÀNG", "Tuyển Việt Nam có cơ hội tham dự giải vô địch Đông Á nếu Indonesia đăng cai"),
            _slot("sentence", 3, [_url(DT_RALLY)], "DÂN TRÍ / BTC", "Giải đua xe địa hình quốc tế Trường Sơn Rally chính thức nhận chứng nhận của FIA"),
            # Câu 4: Renée Slegers
            _slot("sentence", 4, [_ddgs("Renee Slegers Arsenal Women manager")], "BING SEARCH", "Huấn luyện viên Renée Slegers chia tay đội nữ Arsenal sau chuỗi trận bết bát"),
            # Câu 5: Pitchamon
            _slot("sentence", 5, [_url(TT_PITCHAMON)], "TUỔI TRẺ / BAT", "Tay vợt Thái Lan Pitchamon Opatniputh nhận án treo vợt ba tháng vì doping"),
            # Câu 6: Steelers & Curry
            _slot("sentence", 6, [_url(SKY_STEELERS)], "SKY SPORTS", "Hàng thủ Pittsburgh Steelers ghi dấu ấn đậm nét trước Denver Broncos"),
            _slot("sentence", 6, [_ddgs("Stephen Curry Golden State Warriors injury")], "BING SEARCH", "Stephen Curry tiếp tục vắng mặt ba trận tới của Golden State Warriors"),
            # Câu 7: Helinho fair-play
            _slot("sentence", 7, [_ddgs("Helinho Toluca Liga MX football")], "BING SEARCH", "Tiền đạo Brazil Helinho được ca ngợi hết lời vì hành động fair-play tại Mexico"),
        ],
    },
]
