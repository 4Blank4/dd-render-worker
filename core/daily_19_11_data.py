# -*- coding: utf-8 -*-
"""
daily_19_11_data.py — Dữ liệu kịch bản & kế hoạch hình ảnh bản tin 16:9 ngày 19.11.2026
(Tổng hợp tin nổi bật từ 12h trưa 18.11 đến sáng 19.11.2026 — Việt Nam + Thế giới).
Phân bổ giọng đọc luân phiên Nam (primary) / Nữ (secondary) và 2–5 ảnh ngang HD sạch logo mỗi câu.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent
DAILY_18 = ROOT / "outputs" / "18.11.2026" / "images"
WEEKLY_16 = ROOT / "outputs" / "16.11.2026" / "images"
ORTHER = ROOT / "outputs" / "Orther"


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


# ── URL ảnh sạch (không logo/watermark) từ báo chí chính thống 18–19.11.2026 ──
# 01. Đình Bắc & ĐTQG / CAHN
VNE_DINHBAC_INJ = "https://i1-thethao.vnecdn.net/2026/11/18/photo2026-jpeg-1795010566-6125-1795010856.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=TiJ-9GWUXA1bgyVgmSdZFw"
TT_DINHBAC_G = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/base64-17950083251741982167254.jpeg"
TN_DINHBAC_2G = "https://images2.thanhnien.vn/528068263637045248/2026/11/16/ndb7-17948520096001628464892.jpg"
TN_DINHBAC_17 = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/dinh-bac-lap-sieu-pham-de-mo-ty-so-cho-doi-tuyen-viet-nam-1-17949243494651768177852.jpg"
TN_DINHBAC_17B = "https://images2.thanhnien.vn/528068263637045248/2026/11/17/dinh-bac-linh-xuong-hang-cong-17949231844561085987617.jpg"

# 02. Tuyển VN FIFA 99 & thể hình/thể lực
TT_DTVN_FIFA = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/11/0c883411-66fb-46f2-b391-8cb45cf69cdb-17944131189301340084885.jpeg"
TN_QV_KGZ = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/quang-vinh-27-luon-thua-thiet-trong-tranh-chap-bong-voi-cac-cau-thu-kyrgyzstan-1795015010980479511945.jpg"
TN_DINHDUONG = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/bua-an-cua-vdv-mot-doi-tuyen-tre-vn-179501501094330811282.jpg"

# 03. CA TP.HCM 1-0 Buriram United
VNE_QC_CELEB = "https://i1-thethao.vnecdn.net/2026/11/18/1795006128070-g875518108444767-3890-1462-1795006824.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=gC6NWT75Nu8BEp7K2-1SbQ"
TN_QC_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/17950061064333576294910078915045g785497520087887266a2762e7d5df38607118f13d7690294f6-17950277100921875617975.jpg"
TN_QC_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/17950013804903576294910078915045g785497520087887266792b29c98f6907631b777295fc924f68-17950088949371153803921.jpg"
TN_LEGIANG = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/le-giang-patrik-clb-1795012357656175496269.jpg"
TN_QC_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/quoc-cuogn-clb-buriramjpg--1795012357814890944577.jpg"
TN_ARTHUR = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/arthur-clb-buriram-1795011286895645918601.jpg"
TN_OLAHA = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/olaha-clb-buriram-17950114881732024041631.jpg"
TN_QC_4 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/quoc-cuong-clb--17950115767301076736216.jpg"
TN_TLINH_BUR = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/17950013876646545867982648638204g7030313285398070971042c17947e14c8ec782db036f5b46e9d-17950034570381788641187.jpg"
TN_QC_5 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/17950009036166545867982648638204g703031328539807097171b54c0b8fa04a7d6433e3881fa7e1fe-1795003446037702794528.jpg"
TT_BUR = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/17950000491292976936011512605144g1111883354470740454c68014757ba9a421b81c303c62166ab8-17950102831571500842413.jpg"
DT_CATP_1 = "https://cdnphoto.dantri.com.vn/hKWacKd6TJvtdlxu1r8EsHYMOG8=/thumb_w/1020/2026/11/18/catp4da18-11-26-1795010506033.jpeg"
DT_CATP_2 = "https://cdnphoto.dantri.com.vn/nsMTQRX5lWtLwfw-pevpa6HTG8I=/thumb_w/1020/2026/11/18/catp1da18-11-26-1795010503507.jpeg"

# 04. CAHN vs JDT
TN_VANHAU_CAHN = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/van-hau-trai-can-phai-khoa-chat-duoc-nhung-ngoi-no-nguy-hiem-ben-phia-jdt-1795015384445682617548.jpg"

# 05 & 06. U17 World Cup 2026 & U17 Bỉ
TN_U17_FIFA_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/doan-cong-tac-cua-fifa-kiem-tra-quy-chuan-quoc-ky-viet-nam-17949902059501148707084.jpg"
TN_U17_FIFA_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/doan-cong-tac-kiem-tra-giay-to-cua-cac-thanh-vien-17949902059811652147590.jpg"
TN_U17_HOP_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/dai-dien-doi-tuyen-u17-viet-nam-tham-du-cuoc-hop-ky-thuat-do-fifa-to-chuc-tai-super-dome-auditorium-17950005522395513536.jpg"
TN_U17_HOP_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/cuoc-hop-quy-tu-gan-200-dai-bieu-dai-dien-cho-48-doi-tuyen-gop-mat-tai-fifa-u17-world-cup-2026-17950025994511778600031.jpg"
TN_U17_ASPIRE_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/cac-doan-khao-sat-mat-san-va-dieu-kien-thi-dau-truoc-khi-buoc-vao-nhung-tran-dau-dau-tien-tai-world-cup-u17-1795002583564535744055.jpg"
TN_U17_ASPIRE_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/aspire-zone-la-dia-diem-to-chuc-cac-tran-dau-tu-vong-bang-den-vong-32-doi-tran-chung-ket-dien-ra-tai-san-khalifa-international-17950026098211947688394.jpg"
TN_ROLAND_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/4/hlv-cristiano-roland-cung-cac-hoc-tro-trong-mot-buoi-tap-1793770051495678282747.jpg"
TN_ROLAND_2 = "https://images2.thanhnien.vn/528068263637045248/2026/5/7/u17-vn-1-0-u17-yemen-vff4-17781680892141185002843.jpg"
TT_ROLAND_Q = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/hlv-crisrtiano-roland-1795017933044349081719.jpg"
TT_XUANHOA = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/thu-mon-ly-xuan-hoa-1795017128820896326038.jpg"
TN_XUANHOA_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/xuan-hoa-1-17950181960821947659715.jpeg"
TN_XUANHOA_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/xuan-hoa-3-1795018196144926359713.jpeg"
TN_XUANHOA_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/xuan-hoa-4-17950181961491613696889.jpeg"
TN_U17_BI = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/u17-bi-17950017573521623475442.jpg"
DT_U17_1 = "https://cdnphoto.dantri.com.vn/ztf-6zgP5fRn890LU7pXbfNuo24=/thumb_w/1020/2026/11/18/061316d1-b0af-4f11-b0ff-022bffaedb4e-1795020232488.jpg"
DT_U17_2 = "https://cdnphoto.dantri.com.vn/-koLSNKxh38rDXu3u_JvCiF195Q=/thumb_w/1020/2026/11/18/u17vietnam-17912984996211707659232-1791877409431-1795002765328.jpg"
DT_U17_3 = "https://cdnphoto.dantri.com.vn/icpxt7XEHj1gsw0jgEEM4gFyK7M=/thumb_w/1020/2026/11/18/u17-01-1795005101906.jpg"
DT_U17_4 = "https://cdnphoto.dantri.com.vn/LQ6emP2mg4xELNQB8yONkJ8-vHM=/thumb_w/1020/2026/11/18/1794708035216699-202611150737201-1795005141586.jpeg"
VNE_RONALDINHO = "https://i1-thethao.vnecdn.net/2026/11/19/71515156-2390841171010970-2037-8264-7714-1795024181.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=121m82biQzR01hBP_LfckA"

# 07. Messi dọa kiện AFA
DT_MESSI_AFA_1 = "https://cdnphoto.dantri.com.vn/WiQpCDY2ySKIaCr_86liPY3xAdg=/thumb_w/1020/2026/11/18/moi-quan-he-ran-nut-messi-doa-kien-lien-doan-bong-da-argentina-edited-1794981563918.jpg"
DT_MESSI_AFA_2 = "https://cdnphoto.dantri.com.vn/Gxts62HGmvLfsP1PeQnXYN0XBJI=/thumb_w/1020/2026/11/18/20260622t191201z1511394735up1em6m1hbzo7rtrmadp3soccerworldcupargaut-1794981618889.jpg"

# 08. Ronaldo Globe Soccer & BĐN hậu CR7
VNE_CR7_WARM = "https://i1-thethao.vnecdn.net/2026/11/18/AP26267835562100-6596-1794999957.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=M3cKhCwVDq1RU4kHjCKFjg"
VNE_MESSI_IM = "https://i1-thethao.vnecdn.net/2026/11/18/AP26302084631285-8446-1794999958.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=YmeAXd8Ak5hhuM8P1iTWFg"
TN_BDN_WALES = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/doi-tuyen-bo-dao-nha-phai-da-de-thung-luoi-2-ban-trong-chien-thang-truoc-xu-wales-179501538441346918482.jpg"

# 09. Pochettino tại Man Utd
VNE_POCH_CARR = "https://i1-thethao.vnecdn.net/2026/11/19/lcimg-dab46a27-01ee-484b-b3f7-8873-5610-1795045341.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=NGD-6ykHwcCgokvGjE7UHw"
VNE_POCH_CARR2 = "https://iv1.vnecdn.net/thethao/images/web/2026/11/18/pochettino-bat-dau-lam-viec-o-man-utd-1795020751.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=klB7oleJgExCQNk-nfhLuA"
VNE_POCH_CHEL = "https://i1-thethao.vnecdn.net/2026/11/18/2024-04-04T210008Z-1765136885-2620-5377-1794990593.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=DGm_cdBmQRv9E-vw-xTXwg"
VNE_DALOT_MU = "https://i1-thethao.vnecdn.net/2026/11/18/2026-11-08T000000Z-17682264-MT-2449-9051-1794990594.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=dySium3mlhnpQOpmT2C7uQ"

# 10. Philippe Diallo vs Gianni Infantino
VNE_DIALLO_INF = "https://i1-thethao.vnecdn.net/2026/11/18/6e95a5bf-674a-41cc-b438-5b7105-3472-4575-1794998687.png?w=0&h=0&q=100&dpr=1&fit=crop&s=N64HlxtHVT-2tE6PHBPMAA"
VNE_WENGER = "https://i1-thethao.vnecdn.net/2026/11/18/2026-05-30T160538Z-1333956989-6488-7088-1794998687.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=tw4EmqhzZsIpgn5MX6zE_A"
VNE_DIALLO_STAD = "https://i1-thethao.vnecdn.net/2026/11/18/a100b309-aab4-4a2b-a39d-8d5e2e-5389-3392-1794998688.png?w=0&h=0&q=100&dpr=1&fit=crop&s=ycfJmIR80fJ0UPCm3ADKIw"
VNE_DIALLO_SP1 = "https://i1-thethao.vnecdn.net/2026/11/18/Screenshot-2026-11-18-172903-1-5321-2377-1794998687.png?w=0&h=0&q=100&dpr=1&fit=crop&s=O-xqgmzHWz685Wyef87Y2A"
VNE_DIALLO_SP2 = "https://i1-thethao.vnecdn.net/2026/11/18/Screenshot-2026-11-18-172616-1-5855-9836-1794998688.png?w=0&h=0&q=100&dpr=1&fit=crop&s=qU7Q-m1dPOOY2zXBnbaoMg"
VNE_DIALLO_PR = "https://i1-thethao.vnecdn.net/2026/11/19/58e90840-ac69-4554-9ed2-75cf36-8683-9666-1795044687.png?w=0&h=0&q=100&dpr=1&fit=crop&s=zc7OlPtnR9kgaONNH5sOzQ"
VNE_TASHIMA = "https://i1-thethao.vnecdn.net/2026/11/18/Screenshot-2026-11-18-173115-1-6049-8372-1794998688.png?w=0&h=0&q=100&dpr=1&fit=crop&s=WLdZlw-N2DsldFbAFiji_g"
TN_U17_KIT = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/ao-dau-cua-cac-doi-tai-giai-1795002625901750625144.jpg"
DT_U17_5 = "https://cdnphoto.dantri.com.vn/3cPE6mMm9jUxJiOAGKfCHcD2E9U=/thumb_w/1020/2026/11/18/b7c403ab-6e9d-4722-a38e-5f8ac122dd31-1795002789297.png"

# 11. Haaland 399 bàn
VNE_HAALAND_CELEB = "https://i1-thethao.vnecdn.net/2026/11/18/AP26186836239001-7944-1794973066.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=jC-1Kn0DzhKDs-5-D1jbtg"
DT_HAALAND_1 = "https://cdnphoto.dantri.com.vn/h6kkbEZfGs1g7I6fEgcph9_9DWA=/thumb_w/1020/2026/11/18/179b8deb-a890-48be-895d-b5bb549084f5-1795017626507.jpg"
DT_CR7_MU = "https://cdnphoto.dantri.com.vn/OW1xUbtXB5sE_KprqPETxI73cP4=/thumb_w/1020/2026/10/29/cristiano-ronaldo-manchester-united-celebrates-571947451-1793234216345.jpg"

# 12. Arsenal KMI & Ancelotti vs Romario
VNE_ARS_KAI = "https://i1-thethao.vnecdn.net/2026/11/19/kai-1795023920-5056-1795024268.webp?w=1020&h=0&q=100&dpr=1&fit=crop&s=NgL-PrvTfbViP0ptxQ4gEQ"
VNE_ARS_TIMBER = "https://i1-thethao.vnecdn.net/2026/11/19/timber-1795024197-6474-1795024268.webp?w=1020&h=0&q=100&dpr=1&fit=crop&s=gR5J8Kr7HkihkJVFZPtnnA"
DT_BRA_SIN = "https://cdnphoto.dantri.com.vn/IOr3635wRGanG0o9a7Ug6JU6lkA=/thumb_w/1020/2026/11/18/2026-round-16-match-brazil-1093404563-1794978699570.jpg"
DT_ANCELLOTTI = "https://cdnphoto.dantri.com.vn/8nPx8tMb0nL8SKc11ZLwht7HEcg=/thumb_w/1020/2026/11/18/brazil-team-head-coach-carlo-1123675004-1794978739363.jpg"

# 13. Indonesia PSSI Erick Thohir
TT_THOHIR = "https://cdn2.tuoitre.vn/471584752817336320/2026/10/7/antino-meets-with-indonesian-football-association-president-erick-thohir-at-1694336064533611952610-119-0-1166-2000-crop-17858950450881592076654-1791385743008312519673.jpg"
TT_SIANIPAR = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/17/images-31-1794917244607266516885.jpg"

# 14. Lê Quang Liêm & Lại Lý Huynh
TN_LQL_GS = "https://images2.thanhnien.vn/528068263637045248/2023/8/7/le-quang-liem-grand-swiss-1-chesscom-3485-16914216839481444893007.jpg"
TT_LLH = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/15/edit-lai-ly-huynh-ngu-duong-boi-4-17947246704061363702036.png"

# 15. Alcaraz vs Medvedev ATP Finals
DT_ALCARAZ = "https://cdnphoto.dantri.com.vn/Q9vd63ZoRXi9ywm_zmo_0SCI2Mo=/thumb_w/1020/2026/11/18/alcaraz-1795014593017.jpg"
DT_MEDVEDEV = "https://cdnphoto.dantri.com.vn/lkxJxGa6heiak494prh-wxWmdEg=/thumb_w/1020/2026/11/18/medvedev-1795014676101.jpg"

# 16. Võ sĩ Vovinam Kim Lụa & Cầu lông Thùy Linh
TT_KIMLUA_1 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/nu-vo-si-17949941131022141339759.jpg"
TT_KIMLUA_2 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/quan-doi-17949942843381408235155.jpg"

# 17. Bóng bàn VN 400 triệu & Billiards Quyết Chiến
TN_BONGBAN_1 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/179499218148671473839597338316537147383959733831653dffd7aa00af6a0d2c09e44c0cb7fde43-1794996601915788749984.jpg"
TN_BONGBAN_2 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/91290973314935083862090081789292195619014272n-17949968280302033818980.jpg"
TN_BONGBAN_3 = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/9072789951489746053251908909001125149009315n-17949969205251294406902.jpg"
TT_BONGBAN_1 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/base64-17949840931862104741796.jpeg"
TT_BONGBAN_2 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/base64-17949840932131994166720.jpeg"
TN_QUYETCHIEN = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/dsc2606-2-1794994483003778905732.jpeg"
TN_HOANTAT = "https://images2.thanhnien.vn/528068263637045248/2026/11/18/0r1a0295-17949944583971019270298.jpeg"

# 18. Allison Quynh Lee, Dylan Kerr, Stephen Thompson
TT_ALLISON_1 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/allison-3-1795012772299371990787.jpeg"
TT_ALLISON_2 = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/allison-2-17950131017991184917863.jpg"
TT_DYLAN = "https://cdn2.tuoitre.vn/471584752817336320/2026/11/18/dylan-17949963692272112005667.jpeg"


INTRO_DATA: Dict[str, Any] = {
    "id": 0,
    "art_id": "art_00",
    "group": "TÂM ĐIỂM THỂ THAO 19.11.2026",
    "title": "",
    "hide_title": True,
    "summary": (
        "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 19 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất từ 12 giờ trưa hôm qua đến sáng nay. "
        "Ở trong nước, tiền đạo Nguyễn Đình Bắc dính đa chấn thương đầu gối và phải nghỉ thi đấu hết năm 2026, nhưng câu lạc bộ Công an TP.HCM vừa tạo nên chiến thắng lịch sử 1-0 trước đương kim vô địch Buriram United, còn U17 Việt Nam đã sẵn sàng cho FIFA U17 World Cup 2026 khởi tranh hôm nay tại Qatar. "
        "Trên đấu trường quốc tế, Lionel Messi cắt đứt liên hệ và dọa kiện Liên đoàn bóng đá Argentina, Cristiano Ronaldo vắng mặt ở đề cử lớn Globe Soccer Awards, còn HLV Mauricio Pochettino đã chính thức đặt chân tới Carrington để vực dậy Manchester United. "
        "Cùng màn so tài tranh hạng bảy của Lê Quang Liêm gặp Ian Nepomniachtchi, tấm vé áp sát bán kết ATP Finals của Carlos Alcaraz và câu chuyện xúc động của nữ võ sĩ Vovinam Kim Lụa, hãy điểm lại 18 tin nóng ngay sau đây."
    ),
    "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí",
    "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
    "credit": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
    "hide_date_chip": False,
    "voice_preset": "mixed",
    "voice_segments": [
        {
            "voice_preset": "secondary",
            "text": "Chào mừng quý vị đến với Điểm Đọc trong bản tin tổng hợp thể thao ngày 19 tháng 11 năm 2026, cập nhật những diễn biến nóng nhất từ 12 giờ trưa hôm qua đến sáng nay.",
        },
        {
            "voice_preset": "primary",
            "text": "Ở trong nước, tiền đạo Nguyễn Đình Bắc dính đa chấn thương đầu gối và phải nghỉ thi đấu hết năm 2026, nhưng câu lạc bộ Công an TP.HCM vừa tạo nên chiến thắng lịch sử 1-0 trước đương kim vô địch Buriram United, còn U17 Việt Nam đã sẵn sàng cho FIFA U17 World Cup 2026 khởi tranh hôm nay tại Qatar.",
        },
        {
            "voice_preset": "secondary",
            "text": "Trên đấu trường quốc tế, Lionel Messi cắt đứt liên hệ và dọa kiện Liên đoàn bóng đá Argentina, Cristiano Ronaldo vắng mặt ở đề cử lớn Globe Soccer Awards, còn HLV Mauricio Pochettino đã chính thức đặt chân tới Carrington để vực dậy Manchester United.",
        },
        {
            "voice_preset": "primary",
            "text": "Cùng màn so tài tranh hạng bảy của Lê Quang Liêm gặp Ian Nepomniachtchi, tấm vé áp sát bán kết ATP Finals của Carlos Alcaraz và câu chuyện xúc động của nữ võ sĩ Vovinam Kim Lụa, hãy điểm lại 18 tin nóng ngay sau đây.",
        },
    ],
    "slots": [
        # Câu 1 (4 ảnh — Triptych/Multi-image hook)
        _slot("sentence", 1, [_url(VNE_QC_CELEB)], "VNEXPRESS", "Nguyễn Thái Quốc Cường ăn mừng bàn thắng lịch sử trước Buriram United"),
        _slot("sentence", 1, [_url(DT_U17_1)], "DÂN TRÍ / VFF", "Đội tuyển U17 Việt Nam sẵn sàng bước vào chiến dịch U17 World Cup 2026"),
        _slot("sentence", 1, [_url(DT_MESSI_AFA_1)], "DÂN TRÍ / REUTERS", "Lionel Messi trong tâm điểm tranh chấp pháp lý với Liên đoàn bóng đá Argentina"),
        _slot("sentence", 1, [_url(VNE_POCH_CARR)], "VNEXPRESS / MAN UTD", "HLV Mauricio Pochettino chính thức có mặt tại đại bản doanh Carrington"),
        # Câu 2 (4 ảnh)
        _slot("sentence", 2, [_url(TN_DINHBAC_17)], "THANH NIÊN", "Nguyễn Đình Bắc dính đa chấn thương đầu gối sau 48 trận trong năm 2026"),
        _slot("sentence", 2, [_url(TN_QC_1)], "THANH NIÊN", "Công an TP.HCM hạ gục nhà vô địch Thái Lan Buriram United 1-0"),
        _slot("sentence", 2, [_url(TN_LEGIANG)], "THANH NIÊN", "Thủ môn Lê Giang Patrik xuất sắc giữ sạch lưới trước Buriram United"),
        _slot("sentence", 2, [_url(TN_U17_ASPIRE_2)], "THANH NIÊN / FIFA", "Khu phức hợp Aspire Zone tại Qatar sẵn sàng cho U17 World Cup 2026"),
        # Câu 3 (4 ảnh)
        _slot("sentence", 3, [_url(DT_MESSI_AFA_2)], "REUTERS", "Quan hệ giữa Lionel Messi và Liên đoàn bóng đá Argentina rạn nứt nghiêm trọng"),
        _slot("sentence", 3, [_url(VNE_CR7_WARM)], "AP PHOTO", "Cristiano Ronaldo vắng tên ở hạng mục Cầu thủ hay nhất năm Globe Soccer Awards"),
        _slot("sentence", 3, [_url(VNE_POCH_CHEL)], "REUTERS", "Mauricio Pochettino bắt tay ngay vào công việc tại Manchester United"),
        _slot("sentence", 3, [_url(DT_HAALAND_1)], "DÂN TRÍ / AP PHOTO", "Erling Haaland tiến sát cột mốc 400 bàn thắng ở tuổi 26"),
        # Câu 4 (4 ảnh)
        _slot("sentence", 4, [_url(TN_LQL_GS)], "THANH NIÊN / CHESS.COM", "Kỳ thủ Lê Quang Liêm bước vào trận tranh hạng bảy tại Budapest"),
        _slot("sentence", 4, [_url(DT_ALCARAZ)], "DÂN TRÍ / ATP TOUR", "Carlos Alcaraz đánh bại Daniil Medvedev 2-0 tại ATP Finals 2026"),
        _slot("sentence", 4, [_url(TT_KIMLUA_1)], "TUỔI TRẺ", "Nữ võ sĩ Vovinam Nguyễn Thị Kim Lụa giành huy chương vàng Đại hội toàn quốc"),
        _slot("sentence", 4, [_url(TT_ALLISON_1)], "TUỔI TRẺ / BWF", "Tay vợt cầu lông Mỹ gốc Việt Allison Quynh Lee liên tiếp lập địa chấn"),
    ],
}


NEWS_SPECS: List[Dict[str, Any]] = [
    # 01 (Nam — Tâm điểm 1: Đình Bắc)
    {
        "id": 1,
        "art_id": "art_01",
        "group": "Nhóm: Tâm điểm bóng đá Việt Nam",
        "title": "Đình Bắc dính đa chấn thương đầu gối, nghỉ thi đấu hết năm 2026 sau trận thứ 48",
        "summary": (
            "Tối ngày 18 tháng 11, bóng đá Việt Nam đón nhận tin dữ khi tiền đạo chủ lực Nguyễn Đình Bắc được chẩn đoán dính đa chấn thương nặng ở vùng đầu gối phải. "
            "Kết quả kiểm tra y tế xác nhận chân sút sinh năm 2004 bị rách bán phần dây chằng bên ngoài, tổn thương sụn chêm và phù dây chằng chéo trước lẫn chéo sau, buộc anh phải nghỉ điều trị ít nhất sáu tuần đến hai tháng và chính thức khép lại năm 2026. "
            "Đây là hệ quả trực tiếp của mật độ thi đấu dày đặc khi trận thua Kyrgyzstan vừa qua đã là lần ra sân thứ 48 của Đình Bắc trong năm 2026 trên cả ba mặt trận câu lạc bộ Công an Hà Nội, U23 và đội tuyển quốc gia. "
            "Chỉ vài giờ trước khi kết quả chụp chiếu được công bố, HLV Mano Polking đã tỏ rõ sự xót xa trong phòng họp báo khi khẳng định Đình Bắc dù rất khỏe nhưng không phải một cỗ máy và cần được nghỉ ngơi. "
            "Sự vắng mặt của ngôi sao ghi nhiều bàn thắng nhất tuyển Việt Nam năm 2026 với 10 pha lập công là tổn thất cực lớn cho câu lạc bộ Công an Hà Nội trước chuỗi 10 trận trong 40 ngày tới."
        ),
        "source": "VnExpress / Tuổi Trẻ / Thanh Niên",
        "news_source": "VNEXPRESS / TUỔI TRẺ",
        "credit": "VNEXPRESS / THANH NIÊN",
        "slots": [
            _slot("title", 0, [_url(TN_DINHBAC_17)], "THANH NIÊN", "Nguyễn Đình Bắc dính đa chấn thương đầu gối sau trận gặp Kyrgyzstan"),
            _slot("title", 0, [_url(TN_DINHBAC_17B)], "THANH NIÊN", "Chân sút 22 tuổi vừa ghi hai bàn cho tuyển Việt Nam trong tháng 11"),
            _slot("title", 0, [_url(TN_DINHBAC_2G)], "THANH NIÊN", "Đình Bắc là ngôi sao tấn công nổi bật nhất của tuyển Việt Nam năm 2026"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_02_1.jpg")], "THANH NIÊN", "Tiền đạo Nguyễn Đình Bắc được xác nhận chấn thương gối phải sau FIFA Days"),
            _slot("sentence", 1, [_ddgs("Nguyen Dinh Bac Vietnam striker goal")], "THANH NIÊN", "Pha lập công cuối cùng trong năm 2026 của Đình Bắc vào lưới Kyrgyzstan"),
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_01_13.jpg")], "THANH NIÊN", "Nỗi lo thể trạng sau trận đấu vắt kiệt sức lực trên sân Thiên Trường"),
            # Câu 2 (4 ảnh — câu quan trọng về chi tiết đa chấn thương)
            _slot("sentence", 2, [_ddgs("Nguyen Dinh Bac CAHN V-League football")], "THANH NIÊN", "Đình Bắc tổn thương sụn chêm và dây chằng, nghỉ thi đấu ít nhất sáu tuần"),
            _slot("sentence", 2, [_ddgs("Nguyen Dinh Bac Vietnam football match action")], "VNEXPRESS", "Chấn thương buộc tiền đạo 22 tuổi phải nói lời chia tay sân cỏ hết năm 2026"),
            _slot("sentence", 2, [_ddgs("soccer player knee injury medical pitch")], "REUTERS", "Các tổn thương nhỏ tích tụ ở đầu gối đã chuyển biến nặng sau quá tải"),
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_01_7.jpg")], "VNEXPRESS", "Người hâm mộ gửi lời động viên tới Đình Bắc sau thông báo trên trang cá nhân"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Vietnam national football team players training")], "THANH NIÊN", "Tiền đạo xứ Nghệ cày ải liên tục từ cấp độ U23, ĐTQG đến câu lạc bộ"),
            _slot("sentence", 3, [_local(DAILY_18 / "Tin_01_6.jpg")], "THANH NIÊN", "Anh vừa đá trọn vẹn 94 phút ở trận gặp Kyrgyzstan hôm 17/11"),
            _slot("sentence", 3, [_ddgs("Cong An Ha Noi football club players match")], "VNEXPRESS", "Mật độ thi đấu dày đặc bào mòn thể lực của chân sút trẻ"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("Mano Polking coach Vietnam football press conference")], "THANH NIÊN", "HLV Mano Polking lo ngại sâu sắc về việc học trò bị quá tải"),
            _slot("sentence", 4, [_ddgs("Mano Polking Alexandre Polking coach CAHN")], "VNEXPRESS", "Nhà cầm quân người Brazil khẳng định Đình Bắc không phải là cỗ máy"),
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_03_1.jpg")], "VNEXPRESS", "Câu chuyện sử dụng nhân sự giữa đội tuyển và câu lạc bộ lại nóng lên"),
            # Câu 5 (3 ảnh)
            _slot("sentence", 5, [_ddgs("Cong An Ha Noi FC football team Vietnam V-League")], "THANH NIÊN", "Công an Hà Nội mất mũi nhọn chủ lực trước chuỗi 10 trận trong 40 ngày"),
            _slot("sentence", 5, [_url(TN_VANHAU_CAHN)], "THANH NIÊN", "Đội bóng ngành công an phải tính phương án thay thế cho cả sân chơi châu Á"),
            _slot("sentence", 5, [_local(DAILY_18 / "Tin_02_5.jpg")], "THANH NIÊN", "Đình Bắc khép lại năm 2026 với tư cách chân sút số một của tuyển Việt Nam"),
        ],
    },

    # 02 (Nữ — Tâm điểm 2: Tuyển VN tụt hạng 99 FIFA & bài toán thể hình/thể lực)
    {
        "id": 2,
        "art_id": "art_02",
        "group": "Nhóm: Tâm điểm bóng đá Việt Nam",
        "title": "Tuyển Việt Nam chốt hạng 99 FIFA năm 2026, giữ lợi thế hạt giống số 2 vòng loại World Cup 2030",
        "summary": (
            "Sau loạt trận FIFA Days tháng 11 khép lại vào rạng sáng ngày 18 tháng 11, bảng xếp hạng bóng đá thế giới chính thức định hình vị trí kết thúc năm 2026 của các đội tuyển. "
            "Với việc bị trừ 5,3 điểm xuống còn 1228,34 điểm sau trận thua Kyrgyzstan cùng chiến thắng của Mozambique trước Ethiopia, đội tuyển Việt Nam tụt một bậc xuống hạng 99 thế giới, xếp thứ hai Đông Nam Á sau Thái Lan ở hạng 90. "
            "Dù đánh rơi một bậc, việc giữ vững vị trí trong tốp 100 thế giới và tốp 18 châu Á giúp thầy trò HLV Kim Sang-sik chắc chắn nằm ở nhóm hạt giống số 2 tại lễ bốc thăm vòng loại thứ hai World Cup 2030 vào giữa tháng 12, qua đó tránh được loạt đối thủ khó chịu như Jordan, Oman, Syria hay Thái Lan. "
            "Tuy vậy, giới chuyên môn cảnh báo thất bại trước Kyrgyzstan một lần nữa phơi bày điểm yếu cố hữu về thể hình, khả năng tranh chấp tay đôi và sự suy giảm thể lực ở những phút cuối của cầu thủ Việt Nam. "
            "Để thu hẹp khoảng cách với các nền bóng đá hàng đầu châu lục, bóng đá Việt Nam buộc phải đầu tư căn cơ hơn từ khâu dinh dưỡng, khoa học thể thao đến chiều sâu tuyến giữa."
        ),
        "source": "Dân Trí / Tuổi Trẻ / Thanh Niên",
        "news_source": "DÂN TRÍ / TUỔI TRẺ / THANH NIÊN",
        "credit": "TUỔI TRẺ / THANH NIÊN",
        "slots": [
            _slot("title", 0, [_url(TT_DTVN_FIFA)], "TUỔI TRẺ", "Đội tuyển Việt Nam giữ vị trí trong tốp 100 FIFA khi khép lại năm 2026"),
            _slot("title", 0, [_url(TN_QV_KGZ)], "THANH NIÊN", "Điểm yếu tranh chấp và thể hình bộc lộ rõ trước đối thủ Trung Á"),
            _slot("title", 0, [_local(DAILY_18 / "Tin_02_11.jpg")], "THANH NIÊN", "Việt Nam vẫn nằm ở nhóm hạt giống số 2 vòng loại World Cup 2030"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_01_1.jpg")], "THANH NIÊN", "FIFA Days tháng 11 khép lại lịch thi đấu đội tuyển quốc gia năm 2026"),
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_01_4.jpg")], "THANH NIÊN", "Các trận đấu cuối năm định hình bảng xếp hạng FIFA trước thềm năm mới"),
            # Câu 2 (4 ảnh — nhiều số liệu)
            _slot("sentence", 2, [_ddgs("Vietnam national football team players lineup")], "THANH NIÊN", "Trừ 5,3 điểm khiến Việt Nam rơi xuống hạng 99 thế giới với 1228,34 điểm"),
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_10_1.jpg")], "THANH NIÊN", "Thái Lan vô địch King's Cup và vươn lên dẫn đầu Đông Nam Á trên BXH FIFA"),
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_02_12.jpg")], "THANH NIÊN", "Kyrgyzstan được cộng điểm và áp sát ngay sau Việt Nam ở ngoài tốp 100"),
            _slot("sentence", 2, [_ddgs("FIFA world ranking football trophy globe stadium")], "FIFA", "Khoảng cách giữa nhóm Đông Nam Á với châu Á vẫn cần nhiều nỗ lực thu hẹp"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Vietnam national football team lineup stadium")], "THANH NIÊN", "Vị trí tốp 18 châu Á giúp tuyển Việt Nam nắm lợi thế lớn ở lễ bốc thăm"),
            _slot("sentence", 3, [_ddgs("Kim Sang Sik Vietnam football coach")], "THANH NIÊN", "Thầy trò HLV Kim Sang-sik tránh được nhiều đối thủ cứng cựa ở nhóm hai"),
            _slot("sentence", 3, [_ddgs("FIFA World Cup trophy draw ceremony stage")], "FIFA", "Vòng loại thứ hai World Cup 2030 khu vực châu Á sẽ bốc thăm vào tháng 12"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_01_5.jpg")], "THANH NIÊN", "Quang Vinh và hàng tiền vệ gặp khó trước sức mạnh tranh chấp của Kyrgyzstan"),
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_01_9.jpg")], "THANH NIÊN", "Thể hình hạn chế khiến đội tuyển bất lợi trong các pha bóng bổng và tay đôi"),
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_03_9.jpg")], "THANH NIÊN", "Thể lực suy giảm cuối trận là nguyên nhân dẫn tới hai bàn thua chóng vánh"),
            # Câu 5 (2 ảnh)
            _slot("sentence", 5, [_url(TN_DINHDUONG)], "THANH NIÊN", "Bữa ăn khoa học cho vận động viên được nhấn mạnh là gốc rễ cải thiện tầm vóc"),
            _slot("sentence", 5, [_local(DAILY_18 / "Tin_03_7.jpg")], "VNEXPRESS", "Đầu tư khoa học thể thao là bước đi bắt buộc nếu muốn vươn tầm châu lục"),
        ],
    },

    # 03 (Nam — Tâm điểm 3: Công an TP.HCM 1-0 Buriram United — Câu quan trọng 4-5 ảnh!)
    {
        "id": 3,
        "art_id": "art_03",
        "group": "Nhóm: Tâm điểm bóng đá Việt Nam",
        "title": "Công an TP.HCM hạ gục ĐKVĐ Buriram United 1-0 tại Shopee Cup, báo Thái Lan sững sờ",
        "summary": (
            "Tối ngày 18 tháng 11 trên sân Bình Dương ở lượt hai bảng A Cúp các câu lạc bộ Đông Nam Á 2026-2027, câu lạc bộ Công an TP.HCM đã tạo nên cơn địa chấn khi đánh bại đương kim vô địch Buriram United với tỷ số 1-0. "
            "Suốt trận đấu, đội bóng giàu truyền thống nhất Thái Lan tạo ra sức ép lớn với nhiều pha dứt điểm nguy hiểm của các ngoại binh, nhưng đều bị thủ thành Lê Giang Patrik xuất sắc hóa giải để giữ sạch mành lưới. "
            "Bước ngoặt lịch sử xảy ra ở phút 88, khi tân binh vừa ra mắt đội tuyển Việt Nam là Nguyễn Thái Quốc Cường đi bóng từ biên trái ngoặt vào trung lộ rồi tung cú cứa lòng trái phá găm thẳng vào góc chữ A, đánh bại hoàn toàn thủ môn Neil Etheridge. "
            "Ba điểm trọn vẹn giúp thầy trò HLV Arthur Diles vươn lên nhì bảng A với 4 điểm, đồng thời đẩy nhà vô địch Buriram United xuống áp chót bảng khi mới có 1 điểm và chưa ghi nổi bàn thắng nào sau hai lượt trận. "
            "Ngay sau trận đấu, hàng loạt tờ báo thể thao Thái Lan như Siamsport hay Khaosod đồng loạt bày tỏ sự sững sờ trước cú sẩy chân của đội nhà và dành lời thán phục cho siêu phẩm của Quốc Cường cùng chốt chặn Lê Giang Patrik."
        ),
        "source": "Thanh Niên / VnExpress / Tuổi Trẻ / Dân Trí",
        "news_source": "THANH NIÊN / VNEXPRESS / TUỔI TRẺ",
        "credit": "THANH NIÊN / VNEXPRESS",
        "slots": [
            _slot("title", 0, [_url(VNE_QC_CELEB)], "VNEXPRESS", "Nguyễn Thái Quốc Cường cởi áo ăn mừng bàn thắng phút 88"),
            _slot("title", 0, [_url(TN_LEGIANG)], "THANH NIÊN", "Lê Giang Patrik chơi xuất thần và nhận danh hiệu Cầu thủ hay nhất trận"),
            _slot("title", 0, [_url(TN_ARTHUR)], "THANH NIÊN", "HLV Arthur Diles tự hào với chiến thắng lịch sử trước Buriram United"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TT_BUR)], "TUỔI TRẺ", "Cuộc đối đầu kịch tính giữa Công an TP.HCM và Buriram United trên sân Bình Dương"),
            _slot("sentence", 1, [_ddgs("Cong An TPHCM football club Buriram United")], "DÂN TRÍ", "Đại diện Việt Nam chơi bản lĩnh trước nhà đương kim vô địch Shopee Cup"),
            _slot("sentence", 1, [_url(TN_TLINH_BUR)], "THANH NIÊN", "Tiến Linh và hàng công chủ nhà tạo ra nhiều pha lên bóng tốc độ"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_12_1.jpg")], "THANH NIÊN", "Thủ môn Lê Giang Patrik bay người cản phá nhiều cơ hội mười mươi của đội khách"),
            _slot("sentence", 2, [_url(TN_OLAHA)], "THANH NIÊN", "Hàng thủ và tuyến giữa Công an TP.HCM chiến đấu kiên cường suốt trận"),
            _slot("sentence", 2, [_url(DT_CATP_2)], "DÂN TRÍ", "Lối chơi kỷ luật giúp đội chủ nhà đứng vững trước sức ép của đội bóng Thái Lan"),
            # Câu 3 (5 ảnh — khoảnh khắc siêu phẩm phút 88 bùng nổ!)
            _slot("sentence", 3, [_url(TN_QC_1)], "THANH NIÊN", "Nguyễn Thái Quốc Cường đi bóng xộc vào trung lộ ở phút 88"),
            _slot("sentence", 3, [_url(TN_QC_4)], "THANH NIÊN", "Cú sút trái phá đưa bóng găm thẳng vào góc cao đánh bại Neil Etheridge"),
            _slot("sentence", 3, [_local(DAILY_18 / "Tin_12_3.jpg")], "THANH NIÊN", "Khoảnh khắc Quốc Cường vỡ òa cảm xúc sau bàn thắng định đoạt trận đấu"),
            _slot("sentence", 3, [_url(TN_QC_2)], "THANH NIÊN", "Các đồng đội ùa tới chia vui cùng người hùng sinh năm 2003"),
            _slot("sentence", 3, [_url(TN_QC_3)], "THANH NIÊN", "Siêu phẩm nối tiếp phong độ ấn tượng sau khi Quốc Cường vừa lên tuyển Việt Nam"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_12_2.jpg")], "THANH NIÊN", "HLV Arthur Diles ca ngợi các học trò đã chiến đấu như những chiến binh"),
            _slot("sentence", 4, [_url(TN_QC_5)], "THANH NIÊN", "Chiến thắng đưa Công an TP.HCM vươn lên vị trí nhì bảng A với 4 điểm"),
            _slot("sentence", 4, [_ddgs("Buriram United football team Thai League stadium")], "SHOPEE CUP", "Buriram United rơi vào thế báo động khi mới có 1 điểm sau hai lượt trận"),
            # Câu 5 (3 ảnh)
            _slot("sentence", 5, [_ddgs("Thai League football newspaper Buriram United")], "SIAMSPORT", "Truyền thông Thái Lan bất ngờ khi Buriram nhận trái đắng trên đất Việt Nam"),
            _slot("sentence", 5, [_ddgs("Patrik Le Giang Vietnam goalkeeper football")], "THANH NIÊN", "Tờ Khaosod đánh giá Lê Giang Patrik là chốt chặn làm nản lòng hàng công Thái Lan"),
            _slot("sentence", 5, [_ddgs("Ho Chi Minh City football fans stadium night")], "THANH NIÊN", "Tờ Siamsport gọi Nguyễn Thái Quốc Cường là người hùng kết liễu trận đấu"),
        ],
    },

    # 04 (Nữ — Tâm điểm 4: CAHN quyết chiến Johor Darul Ta'zim tối 19/11)
    {
        "id": 4,
        "art_id": "art_04",
        "group": "Nhóm: Tâm điểm bóng đá Việt Nam",
        "title": "Công an Hà Nội quyết chiến Johor Darul Ta'zim tối nay tại Hàng Đẫy trong thế vắng Đình Bắc và Quang Hải",
        "summary": (
            "Tiếp nối chiến thắng của Công an TP.HCM, vào lúc 19 giờ 15 tối nay ngày 19 tháng 11 trên sân Hàng Đẫy, câu lạc bộ Công an Hà Nội sẽ bước vào trận cầu đinh bảng B Shopee Cup gặp gã khổng lồ Malaysia là Johor Darul Ta'zim. "
            "Đội khách đang tạm dẫn đầu bảng nhờ trận thắng đậm 6-0 ở lượt mở màn và sở hữu dàn ngôi sao có tổng giá trị 14,08 triệu euro, gấp hơn hai lần định giá 6,45 triệu euro của đội chủ nhà. "
            "Khó khăn càng chồng chất với HLV Mano Polking khi đội trưởng Nguyễn Quang Hải chưa bình phục hoàn toàn còn chân sút đang vào phom là Nguyễn Đình Bắc vừa phải nghỉ thi đấu hết năm vì chấn thương đầu gối. "
            "Dù vậy, Công an Hà Nội vẫn đón tin vui khi hàng loạt trụ cột như Bùi Hoàng Việt Anh, Đoàn Văn Hậu, Cao Pendant Quang Vinh và Lê Phạm Thành Long không phải dự đợt tập trung đội tuyển vừa qua nên giữ được nền tảng thể lực sung mãn nhất để hướng tới ngôi đầu bảng."
        ),
        "source": "Thanh Niên / VnExpress",
        "news_source": "THANH NIÊN / VNEXPRESS",
        "credit": "THANH NIÊN",
        "slots": [
            _slot("title", 0, [_url(TN_VANHAU_CAHN)], "THANH NIÊN", "Đoàn Văn Hậu và hàng thủ Công an Hà Nội sẵn sàng đại chiến Johor Darul Ta'zim"),
            _slot("title", 0, [_ddgs("Hang Day stadium Hanoi football night match")], "THANH NIÊN", "Sân Hàng Đẫy chờ đợi màn so tài đỉnh cao tối 19/11 ở bảng B Shopee Cup"),
            _slot("title", 0, [_ddgs("Johor Darul Ta'zim football club match Malaysia")], "SHOPEE CUP", "Johor Darul Ta'zim là thế lực hàng đầu khu vực với 12 chức vô địch Malaysia"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_ddgs("ASEAN Club Championship Shopee Cup football match")], "SHOPEE CUP", "Trận đấu tối 19/11 quyết định ngôi đầu bảng B giữa hai ứng viên vô địch"),
            _slot("sentence", 1, [_ddgs("Cong An Ha Noi football club players training")], "THANH NIÊN", "Công an Hà Nội đặt mục tiêu giành trọn 3 điểm trên sân nhà Hàng Đẫy"),
            _slot("sentence", 1, [_ddgs("Johor Darul Ta'zim players football pitch")], "SHOPEE CUP", "Đại diện Malaysia từng vào tới tứ kết AFC Champions League Elite mùa trước"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_ddgs("Arif Aiman Johor Darul Ta'zim football")], "SHOPEE CUP", "Dàn sao ngoại binh và tuyển thủ đắt giá của Johor Darul Ta'zim"),
            _slot("sentence", 2, [_ddgs("football stadium floodlights night crowd Asia")], "AFC", "Khoảng cách giá trị đội hình không làm giảm quyết tâm của đại diện V-League"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Nguyen Dinh Bac Cong An Ha Noi injury match")], "VNEXPRESS", "Chấn thương bất ngờ khiến Nguyễn Đình Bắc lỡ hẹn trận đại chiến tối nay"),
            _slot("sentence", 3, [_ddgs("Nguyen Quang Hai Cong An Ha Noi football")], "THANH NIÊN", "Đội trưởng Quang Hải cũng chưa đạt thể trạng tốt nhất để gánh vác tuyến giữa"),
            _slot("sentence", 3, [_ddgs("Mano Polking coach football pitch")], "THANH NIÊN", "HLV Mano Polking đứng trước bài toán xoay tua nhân sự hóc búa"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("Doan Van Hau Vietnam football defender")], "THANH NIÊN", "Nhóm trụ cột như Văn Hậu và Việt Anh có trọn quãng nghỉ FIFA Days để hồi phục"),
            _slot("sentence", 4, [_ddgs("Bui Hoang Viet Anh football Vietnam defender")], "THANH NIÊN", "Hàng thủ sung sức sẽ là điểm tựa để Công an Hà Nội khóa chặt ngòi nổ JDT"),
            _slot("sentence", 4, [_ddgs("Vietnam football fans cheering stadium flags")], "THANH NIÊN", "Cổ động viên thủ đô kỳ vọng vào một đêm bùng nổ tại Hàng Đẫy"),
        ],
    },

    # 05 (Nam — U17 World Cup 2026: Khai mạc hôm nay & quyền lực FVS của HLV Roland)
    {
        "id": 5,
        "art_id": "art_05",
        "group": "Nhóm: Sẵn sàng FIFA U17 World Cup 2026",
        "title": "FIFA U17 World Cup 2026 khai mạc hôm nay tại Qatar, HLV Roland có quyền yêu cầu xem lại video",
        "summary": (
            "Hôm nay ngày 19 tháng 11, vòng chung kết FIFA U17 World Cup 2026 chính thức khởi tranh tại Qatar với sự góp mặt của 48 đội tuyển chia thành 12 bảng đấu, kéo dài tới ngày 13 tháng 12. "
            "Lần đầu tiên trong lịch sử giành vé dự sân chơi thế giới ở lứa tuổi này và cũng là đại diện duy nhất của Đông Nam Á, đội tuyển U17 Việt Nam vừa hoàn tất khâu kiểm tra trang phục, quốc kỳ nghiêm ngặt và được FIFA trao bằng chứng nhận tham dự giải. "
            "Đặc biệt, HLV Cristiano Roland sẽ lần đầu tiên sở hữu quyền lực mới thông qua hệ thống hỗ trợ trọng tài video mang tên Football Video Support hay gọi tắt là FVS ngay từ trận ra quân. "
            "Khác với công nghệ VAR truyền thống, FVS cho phép HLV trưởng chủ động xoay ngón tay trên không và trao thẻ yêu cầu trọng tài xem lại video ở bốn tình huống trọng yếu gồm bàn thắng, phạt đền, thẻ đỏ trực tiếp và phạt nhầm cầu thủ. "
            "Tất cả các trận đấu từ vòng bảng đến bán kết sẽ diễn ra tại khu phức hợp Aspire Zone ở Doha, nơi thầy trò HLV Cristiano Roland lần lượt chạm trán Bỉ ngày 20 tháng 11, New Zealand ngày 23 tháng 11 và Mali ngày 26 tháng 11."
        ),
        "source": "VnExpress / Tuổi Trẻ / Thanh Niên",
        "news_source": "VNEXPRESS / TUỔI TRẺ / THANH NIÊN",
        "credit": "THANH NIÊN / VFF",
        "slots": [
            _slot("title", 0, [_url(TN_U17_FIFA_1)], "THANH NIÊN", "Đoàn công tác FIFA kiểm tra trang phục và quốc kỳ của U17 Việt Nam"),
            _slot("title", 0, [_url(TT_ROLAND_Q)], "TUỔI TRẺ / VFF", "HLV Cristiano Roland và các học trò sẵn sàng bước ra sân chơi thế giới"),
            _slot("title", 0, [_url(TN_U17_ASPIRE_2)], "THANH NIÊN", "Khu phức hợp thể thao Aspire Zone tại Doha đăng cai giải đấu 48 đội"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(DT_U17_1)], "DÂN TRÍ / FIFA", "Vòng chung kết FIFA U17 World Cup 2026 khai mạc ngày 19/11 tại Qatar"),
            _slot("sentence", 1, [_url(TN_U17_HOP_2)], "THANH NIÊN", "Cuộc họp kỹ thuật quy mô gần 200 đại biểu từ 48 đội tuyển tham dự"),
            _slot("sentence", 1, [_url(VNE_RONALDINHO)], "VNEXPRESS / FIFA", "Đấu trường U17 World Cup từng là bệ phóng của hàng loạt huyền thoại như Ronaldinho"),
            # Câu 2 (4 ảnh)
            _slot("sentence", 2, [_url(TN_U17_KIT)], "THANH NIÊN", "Chuyên gia FIFA đo đạc tỉ mỉ từng thông số áo đấu và quốc kỳ Việt Nam"),
            _slot("sentence", 2, [_url(TN_U17_FIFA_2)], "THANH NIÊN", "Kiểm tra hồ sơ nhận diện trước khi trao bằng chứng nhận lịch sử cho U17 Việt Nam"),
            _slot("sentence", 2, [_url(TN_U17_HOP_1)], "THANH NIÊN", "Đại diện U17 Việt Nam tham dự buổi phổ biến điều lệ giải đấu của FIFA"),
            _slot("sentence", 2, [_url(DT_U17_2)], "DÂN TRÍ / VFF", "Việt Nam là đại diện duy nhất của Đông Nam Á góp mặt tại Qatar lần này"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(DT_U17_5)], "DÂN TRÍ / VFF", "HLV Cristiano Roland lần đầu tiếp cận công nghệ hỗ trợ trọng tài FVS tại World Cup"),
            _slot("sentence", 3, [_url(TN_ROLAND_1)], "THANH NIÊN", "Nhà cầm quân người Brazil giúp học trò vượt qua tâm lý e ngại trước các đội lớn"),
            _slot("sentence", 3, [_ddgs("FIFA referee pitchside monitor video review football")], "FIFA", "Hệ thống Football Video Support trao quyền chủ động khiếu nại cho HLV trưởng"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("football referee VAR screen review stadium")], "FIFA", "HLV có thể yêu cầu xem lại bàn thắng, phạt đền, thẻ đỏ trực tiếp và nhầm người"),
            _slot("sentence", 4, [_url(TN_ROLAND_2)], "THANH NIÊN", "Cơ chế mới giúp ban huấn luyện U17 Việt Nam bảo vệ công bằng cho cầu thủ trẻ"),
            _slot("sentence", 4, [_ddgs("football coach gesturing touchline fourth official")], "REUTERS", "HLV xoay ngón tay ra hiệu và gửi thẻ yêu cầu trực tiếp cho trọng tài thứ tư"),
            # Câu 5 (3 ảnh)
            _slot("sentence", 5, [_url(TN_U17_ASPIRE_1)], "THANH NIÊN", "Các đoàn khảo sát mặt cỏ tại tổ hợp 8 sân thi đấu của Học viện Aspire"),
            _slot("sentence", 5, [_ddgs("Ahmad bin Ali Stadium Qatar football night")], "FIFA", "Trận chung kết giải đấu sẽ diễn ra trên sân Ahmad bin Ali 45000 chỗ ngồi"),
            _slot("sentence", 5, [_url(DT_U17_3)], "DÂN TRÍ / VFF", "Thầy trò HLV Roland lần lượt đối đầu Bỉ, New Zealand và Mali ở bảng G"),
        ],
    },

    # 06 (Nữ — U17 Bỉ sứt mẻ & sự chuẩn bị của U17 Việt Nam)
    {
        "id": 6,
        "art_id": "art_06",
        "group": "Nhóm: Sẵn sàng FIFA U17 World Cup 2026",
        "title": "Đối thủ ra quân U17 Bỉ mất 4 trụ cột từ Anderlecht, truyền thông Bỉ dè chừng U17 Việt Nam",
        "summary": (
            "Trước trận ra quân bảng G lúc 20 giờ tối mai ngày 20 tháng 11, đối thủ lớn nhất của U17 Việt Nam là đương kim á quân châu Âu U17 Bỉ bất ngờ đón tin không vui về lực lượng. "
            "Do giải U17 World Cup diễn ra ngoài lịch thi đấu bắt buộc của FIFA, câu lạc bộ giàu truyền thống Anderlecht đã từ chối nhả bốn cầu thủ chủ chốt gồm ngôi sao chạy cánh từng được FIFA điểm danh là Jayden Onia Seke cùng bộ ba Joshua Nga Kana, Noa Ojea và Noah Kalonji. "
            "Bên cạnh đó, báo chí Bỉ như tờ VoetbalPrimeur cũng đồng loạt nhắc nhở thầy trò HLV Sven Vermant không được phép chủ quan trước tinh thần kỷ luật của U17 Việt Nam. "
            "Về phía đại diện Việt Nam, thủ môn Lý Xuân Hòa nhận xét đối thủ châu Âu áp sát rất nhanh và sở hữu chiều cao trung bình tới 1,85 mét so với mức 1,73 mét của chúng ta, nhưng toàn đội đã phân tích kỹ băng hình và hoàn toàn tự tin tạo nên bất ngờ."
        ),
        "source": "Thanh Niên / Dân Trí / Tuổi Trẻ",
        "news_source": "THANH NIÊN / DÂN TRÍ / TUỔI TRẺ",
        "credit": "THANH NIÊN / VFF",
        "slots": [
            _slot("title", 0, [_url(TN_U17_BI)], "THANH NIÊN", "U17 Bỉ tham dự giải với tư cách đương kim á quân U17 châu Âu 2026"),
            _slot("title", 0, [_url(TN_XUANHOA_1)], "THANH NIÊN", "Thủ môn Lý Xuân Hòa và đồng đội phân tích kỹ lối đá áp sát của U17 Bỉ"),
            _slot("title", 0, [_url(DT_U17_4)], "DÂN TRÍ / VFF", "U17 Việt Nam miệt mài tập luyện trước trận mở màn bảng G tối 20/11"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_ddgs("Belgium U17 football team UEFA Euro match")], "UEFA", "U17 Bỉ được đánh giá cao nhất bảng G nhưng gặp tổn thất lực lượng sát giờ G"),
            _slot("sentence", 1, [_ddgs("Belgium youth national football team match")], "UEFA", "Á quân châu Âu phải điều chỉnh phương án tấn công cho ngày ra quân"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_ddgs("RSC Anderlecht youth academy football stadium")], "THANH NIÊN", "CLB Anderlecht giữ lại 4 tài năng trẻ phục vụ đội một và giải hạng nhì Bỉ"),
            _slot("sentence", 2, [_ddgs("Belgium football youth player winger action")], "FIFA", "Sự vắng mặt của Jayden Onia Seke làm giảm đáng kể sức đột phá biên của Bỉ"),
            _slot("sentence", 2, [_ddgs("Club Brugge Genk youth football training Belgium")], "UEFA", "Trong danh sách 21 cầu thủ sang Qatar, Anderlecht chỉ góp hai gương mặt"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(DT_U17_3)], "DÂN TRÍ", "Truyền thông Bỉ đánh giá U17 Việt Nam sở hữu lối chơi kỷ luật và gắn kết"),
            _slot("sentence", 3, [_ddgs("U17 Vietnam national football team Qatar training")], "VFF", "Báo VoetbalPrimeur cảnh báo đội nhà không được phép chủ quan trước tân binh Đông Nam Á"),
            _slot("sentence", 3, [_url(TN_XUANHOA_3)], "THANH NIÊN", "Các cầu thủ trẻ Việt Nam duy trì sự tập trung cao độ trên sân tập tại Doha"),
            # Câu 4 (4 ảnh)
            _slot("sentence", 4, [_url(TT_XUANHOA)], "TUỔI TRẺ / VFF", "Thủ môn Lý Xuân Hòa đánh giá rất cao tốc độ áp sát của U17 Bỉ"),
            _slot("sentence", 4, [_ddgs("Vietnam youth football goalkeeper training save")], "THANH NIÊN", "Chênh lệch chiều cao trung bình 1,73 mét và 1,85 mét là thử thách lớn nhất"),
            _slot("sentence", 4, [_url(TN_XUANHOA_2)], "THANH NIÊN", "Xuân Hòa khẳng định sự chuẩn bị kỹ lưỡng giúp toàn đội tự tin thi đấu hết mình"),
            _slot("sentence", 4, [_url(TN_ROLAND_1)], "THANH NIÊN", "HLV Cristiano Roland tin tưởng vào bản lĩnh của lứa cầu thủ lịch sử"),
        ],
    },

    # 07 (Nam — Quốc tế 1: Messi dọa kiện AFA — Câu quan trọng 4 ảnh)
    {
        "id": 7,
        "art_id": "art_07",
        "group": "Nhóm: Tâm điểm bóng đá quốc tế",
        "title": "Rạn nứt đỉnh điểm, Lionel Messi cắt đứt liên hệ và dọa kiện Liên đoàn bóng đá Argentina",
        "summary": (
            "Làng bóng đá Nam Mỹ chấn động vào trưa ngày 18 tháng 11 khi tờ Clarin của Argentina tiết lộ siêu sao Lionel Messi đã cắt đứt mọi liên hệ với Liên đoàn bóng đá Argentina và sẵn sàng bước vào cuộc chiến pháp lý. "
            "Cụ thể, Messi đã thuê đội ngũ luật sư riêng yêu cầu cơ quan quản lý bóng đá xứ Tango lập tức ngừng khai thác tên tuổi và hình ảnh của anh cho các chiến dịch thương mại khi chưa được phép. "
            "Nguồn cơn xuất phát từ việc Chủ tịch Claudio Tapia tự ý cấp phép cho một hãng bia Argentina sử dụng hình ảnh Messi tại World Cup 2026 khiến anh gặp rắc rối lớn với đối tác độc quyền tại Mỹ, bên cạnh hàng loạt hợp đồng giao hữu nhận tiền cam kết Messi ra sân mà không hỏi ý kiến anh. "
            "Giọt nước tràn ly đến sau loạt bê bối tài chính của ban lãnh đạo liên đoàn và những sự cố âm thanh, ánh sáng đáng quên trong trận đấu chia tay đội tuyển của El Pulga trước Benin trên sân Monumental."
        ),
        "source": "Dân Trí / Clarin",
        "news_source": "DÂN TRÍ / CLARIN",
        "credit": "DÂN TRÍ / REUTERS",
        "slots": [
            _slot("title", 0, [_url(DT_MESSI_AFA_1)], "DÂN TRÍ / REUTERS", "Lionel Messi cắt đứt liên hệ với Liên đoàn bóng đá Argentina sau khi chia tay ĐTQG"),
            _slot("title", 0, [_url(DT_MESSI_AFA_2)], "DÂN TRÍ / REUTERS", "Siêu sao Argentina thuê luật sư bảo vệ bản quyền hình ảnh cá nhân"),
            _slot("title", 0, [_ddgs("Claudio Tapia AFA president Argentina football")], "REUTERS", "Chủ tịch AFA Claudio Tapia đối mặt làn sóng chỉ trích và điều tra tài chính"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_ddgs("Lionel Messi Argentina national team jersey match")], "REUTERS", "Tờ Clarin phanh phui rạn nứt không thể hàn gắn giữa Messi và AFA"),
            _slot("sentence", 1, [_ddgs("Lionel Messi Argentina national team sad match")], "REUTERS", "Mâu thuẫn bùng phát ngay sau khi El Pulga khép lại hành trình quốc tế"),
            _slot("sentence", 1, [_ddgs("Argentina Football Association AFA logo stadium Buenos Aires")], "AP PHOTO", "Bóng đá Argentina chao đảo bởi xung đột chưa từng có với biểu tượng lớn nhất"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(VNE_MESSI_IM)], "AP PHOTO", "Đội ngũ luật sư của Messi yêu cầu AFA chấm dứt sử dụng hình ảnh trái phép"),
            _slot("sentence", 2, [_ddgs("Lionel Messi Inter Miami press conference portrait")], "AP PHOTO", "Bảo vệ quyền lợi thương mại là ranh giới đỏ của chân sút 39 tuổi"),
            _slot("sentence", 2, [_ddgs("legal contract gavel court football sports law")], "REUTERS", "Hai bên sẵn sàng đưa tranh chấp ra tòa nếu không đạt được thỏa thuận"),
            # Câu 3 (4 ảnh)
            _slot("sentence", 3, [_ddgs("Claudio Tapia Lionel Messi Argentina celebration")], "AP PHOTO", "Chủ tịch Claudio Tapia bị tố tự ý cấp phép hình ảnh Messi cho hãng bia nội địa"),
            _slot("sentence", 3, [_ddgs("Lionel Messi World Cup 2026 Argentina jersey")], "REUTERS", "Vụ việc khiến Messi phải giải trình với nhà tài trợ bia độc quyền ở Mỹ"),
            _slot("sentence", 3, [_ddgs("Lionel Messi playing friendly match crowd stadium")], "AP PHOTO", "AFA còn bị tố nhận tiền giao hữu kèm cam kết Messi ra sân mà chưa được đồng thuận"),
            _slot("sentence", 3, [_ddgs("Buenos Aires football fans protest stadium Argentina")], "REUTERS", "Áp lực từ công chúng và các nhà tài trợ đẩy mâu thuẫn lên đỉnh điểm"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("Estadio Monumental Buenos Aires night football match")], "REUTERS", "Sự cố âm thanh ánh sáng ở trận chia tay gặp Benin trở thành giọt nước tràn ly"),
            _slot("sentence", 4, [_ddgs("River Plate Monumental stadium Argentina")], "AP PHOTO", "CLB River Plate thẳng thừng bác bỏ việc AFA đổ lỗi cho ban quản lý sân"),
            _slot("sentence", 4, [_ddgs("Lionel Messi waving fans Argentina national team")], "REUTERS", "Triều đại của Claudio Tapia đang bị bủa vây bởi nhiều nghi vấn tài chính"),
        ],
    },

    # 08 (Nữ — Quốc tế 2: Ronaldo vắng đề cử Globe Soccer & Bồ Đào Nha hậu CR7)
    {
        "id": 8,
        "art_id": "art_08",
        "group": "Nhóm: Tâm điểm bóng đá quốc tế",
        "title": "Ronaldo vắng mặt ở đề cử Globe Soccer Awards 2026, thống kê đáng lo của Bồ Đào Nha thời hậu CR7",
        "summary": (
            "Ngày 18 tháng 11, ban tổ chức giải thưởng Globe Soccer Awards hay còn gọi là Quả bóng vàng Dubai chính thức công bố danh sách đề cử kỳ thứ 17 và mở cổng bình chọn toàn cầu. "
            "Trong khi Lionel Messi trở lại danh sách 26 ứng viên Cầu thủ nam hay nhất năm cùng những ngôi sao như Ousmane Dembele, Lamine Yamal, Kylian Mbappé hay Erling Haaland, Cristiano Ronaldo lại hoàn toàn vắng mặt ở cả hạng mục Cầu thủ nam lẫn Tiền đạo hay nhất năm và chỉ góp mặt tại giải Cầu thủ hay nhất Trung Đông. "
            "Ở một diễn biến liên quan, truyền thông vừa công bố thống kê gây bất ngờ về đội tuyển Bồ Đào Nha ngay sau khi Ronaldo giã từ sự nghiệp quốc tế vào đầu tháng 11. "
            "Dù vừa thắng Xứ Wales 3-2 để lọt vào tứ kết Nations League, Bồ Đào Nha đã để thủng lưới tới 6 bàn chỉ sau hai trận không còn Ronaldo, đẩy tỷ lệ nhận bàn thua lên mức trung bình 3 bàn mỗi trận — cao gần gấp năm lần so với con số 0,63 bàn mỗi trận thời điểm anh còn làm thủ quân sau World Cup 2022."
        ),
        "source": "VnExpress / Thanh Niên",
        "news_source": "VNEXPRESS / THANH NIÊN",
        "credit": "AP PHOTO / THANH NIÊN",
        "slots": [
            _slot("title", 0, [_url(VNE_CR7_WARM)], "AP PHOTO", "Cristiano Ronaldo vắng mặt ở hạng mục lớn nhất của Globe Soccer Awards 2026"),
            _slot("title", 0, [_url(VNE_MESSI_IM)], "AP PHOTO", "Lionel Messi tái xuất trong tốp 26 ứng viên Cầu thủ nam hay nhất năm"),
            _slot("title", 0, [_url(TN_BDN_WALES)], "THANH NIÊN", "Bồ Đào Nha lộ lỗ hổng phòng ngự đáng lo trong hai trận đầu hậu Ronaldo"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_ddgs("Globe Soccer Awards Dubai trophy ceremony")], "GLOBE SOCCER", "Lễ trao giải Quả bóng vàng Dubai lần thứ 17 sẽ diễn ra ngày 28/12 tại UAE"),
            _slot("sentence", 1, [_ddgs("Dubai Atlantis Palm awards stage night")], "GLOBE SOCCER", "Cổng bình chọn toàn cầu chính thức mở đến hết ngày 30/11"),
            # Câu 2 (4 ảnh)
            _slot("sentence", 2, [_ddgs("Cristiano Ronaldo Al Nassr Saudi Pro League match")], "AP PHOTO", "Ronaldo chỉ có tên ở hạng mục Cầu thủ hay nhất Trung Đông cùng Mane và Joao Felix"),
            _slot("sentence", 2, [_ddgs("Ousmane Dembele PSG Champions League trophy")], "REUTERS", "Đương kim chủ nhân danh hiệu Ousmane Dembele dẫn đầu dàn sao PSG được đề cử"),
            _slot("sentence", 2, [_ddgs("Lamine Yamal Spain World Cup 2026 trophy")], "AP PHOTO", "Lamine Yamal, Mbappé và Haaland là những đối thủ nặng ký của Lionel Messi"),
            _slot("sentence", 2, [_ddgs("Lionel Messi Inter Miami celebration MLS goal")], "AP PHOTO", "Messi trở lại đường đua danh hiệu cá nhân cao nhất của giải sau hơn một thập kỷ"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_local(DAILY_18 / "Tin_04_4.jpg")], "UEFA", "Hàng thủ Bồ Đào Nha đánh mất sự tập trung sau ngày Ronaldo chia tay đội tuyển"),
            _slot("sentence", 3, [_local(DAILY_18 / "Tin_04_8.jpg")], "REUTERS", "Carlos Forbs khoác áo số 7 theo quy định đánh số liên tiếp của giải đấu quốc tế"),
            _slot("sentence", 3, [_local(DAILY_18 / "Tin_04_11.jpg")], "REUTERS", "HLV Jorge Jesus đối mặt bài toán tinh thần trước vòng tứ kết Nations League"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_04_1.jpg")], "AP PHOTO", "Thua Đan Mạch 1-4 và thắng Xứ Wales 3-2 khiến Bồ Đào Nha thủng lưới 6 bàn sau 2 trận"),
            _slot("sentence", 4, [_ddgs("Cristiano Ronaldo Portugal national team captain")], "REUTERS", "Giai đoạn sau World Cup 2022 có Ronaldo, Bồ Đào Nha chỉ thủng lưới 0,63 bàn mỗi trận"),
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_04_10.jpg")], "UEFA", "Những trận thua đậm trên sân nhà cho thấy giá trị thủ lĩnh tinh thần của CR7"),
        ],
    },

    # 09 (Nam — Quốc tế 3: Pochettino chính thức làm việc tại Carrington, Man Utd)
    {
        "id": 9,
        "art_id": "art_09",
        "group": "Nhóm: Tâm điểm bóng đá quốc tế",
        "title": "Pochettino chính thức làm việc tại Carrington, thay 5 trợ lý và siết kỷ luật chạy chỗ ở Man Utd",
        "summary": (
            "Rạng sáng ngày 19 tháng 11 theo giờ Việt Nam, trang chủ Manchester United công bố những hình ảnh đầu tiên của tân HLV Mauricio Pochettino tại trung tâm huấn luyện Carrington. "
            "Ngay sau khi hạ cánh xuống Manchester bằng chuyên cơ riêng vào trưa ngày 18 tháng 11, chiến lược gia 54 tuổi lập tức bắt tay vào công việc với hợp đồng kéo dài tới năm 2029 thay cho Michael Carrick. "
            "Pochettino mang theo năm cộng sự thân tín gồm Jesus Perez, Miguel D'Agostino, Toni Jimenez, Alec Scott và con trai Sebastiano Pochettino, đồng thời chia tay năm thành viên ban huấn luyện cũ trong đó có Jonny Evans và Steve Holland. "
            "Trước thềm trận ra mắt đầy bão táp gặp đại kình địch Liverpool tại Anfield ngày 22 tháng 11 khi Quỷ đỏ đang đối mặt nguy cơ rơi xuống đáy bảng Ngoại hạng Anh, ông Pochettino nhấn mạnh các học trò phải chạy có mục đích và chạy cùng nhau thay vì bị đối thủ vượt mặt về cường độ."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / MAN UTD",
        "slots": [
            _slot("title", 0, [_url(VNE_POCH_CARR)], "VNEXPRESS / MAN UTD", "Mauricio Pochettino rạng rỡ trong ngày đầu tiên tại đại bản doanh Carrington"),
            _slot("title", 0, [_ddgs("Mauricio Pochettino Manchester United Carrington training")], "VNEXPRESS", "Chiến lược gia người Argentina bắt tay ngay vào chuẩn bị cho trận gặp Liverpool"),
            _slot("title", 0, [_url(VNE_DALOT_MU)], "REUTERS", "Manchester United bước vào cuộc cải tổ toàn diện từ ban huấn luyện đến lối chơi"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_08_8.jpg")], "REUTERS", "Trang chủ Man Utd phát video chào đón tân HLV trưởng Mauricio Pochettino"),
            _slot("sentence", 1, [_ddgs("Mauricio Pochettino Manchester United manager portrait")], "MAN UTD", "Nhà cầm quân 54 tuổi gọi đây là vinh dự và đặc ân lớn trong sự nghiệp"),
            _slot("sentence", 1, [_ddgs("Manchester United Carrington training ground badge")], "REUTERS", "Không khí khẩn trương tại trung tâm huấn luyện Carrington chiều 18/11"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_08_7.jpg")], "REUTERS", "Chuyên cơ của Man Utd đưa ông Pochettino hạ cánh xuống sân bay Manchester lúc 11h30"),
            _slot("sentence", 2, [_url(VNE_POCH_CHEL)], "REUTERS", "Pochettino ký hợp đồng tới năm 2029 sau khi chia tay đội tuyển Mỹ"),
            _slot("sentence", 2, [_ddgs("Old Trafford stadium Manchester United night")], "AP PHOTO", "Áp lực vực dậy đội bóng trong giai đoạn khởi đầu tệ nhất 40 năm qua"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Jesus Perez Mauricio Pochettino assistant coach training")], "AP PHOTO", "Trợ lý lâu năm Jesus Perez cùng 4 cộng sự thân tín tái hợp Pochettino"),
            _slot("sentence", 3, [_ddgs("Jonny Evans Manchester United coach pitch")], "REUTERS", "Quỷ đỏ xác nhận chia tay 5 thành viên cũ gồm Jonny Evans và Steve Holland"),
            _slot("sentence", 3, [_ddgs("Manchester United players training session Carrington")], "MAN UTD", "Ban huấn luyện mới đã liên lạc trao đổi 20 cuộc gọi mỗi ngày trước khi hội quân"),
            # Câu 4 (4 ảnh)
            _slot("sentence", 4, [_ddgs("Anfield stadium Liverpool vs Manchester United match")], "REUTERS", "Thử thách đầu tiên mang tên Liverpool tại chảo lửa Anfield ngày 22/11"),
            _slot("sentence", 4, [_ddgs("Manchester United players Premier League match")], "REUTERS", "Man Utd nằm trong nhóm hai đội di chuyển ít nhất giải sau 10 vòng đầu"),
            _slot("sentence", 4, [_ddgs("Mauricio Pochettino shouting touchline football")], "REUTERS", "Pochettino yêu cầu cầu thủ chạy hiệu quả, có mục đích và phối hợp đồng đội"),
            _slot("sentence", 4, [_ddgs("Premier League football match tactical intensity")], "AP PHOTO", "Sau Anfield, Man Utd sẽ đá liên tục 10 trận trong vòng 39 ngày"),
        ],
    },

    # 10 (Nữ — Quốc tế 4: UEFA chỉ định Philippe Diallo lật đổ Gianni Infantino)
    {
        "id": 10,
        "art_id": "art_10",
        "group": "Nhóm: Tâm điểm bóng đá quốc tế",
        "title": "UEFA chỉ định Philippe Diallo làm ứng viên đối đầu Gianni Infantino tranh ghế Chủ tịch FIFA",
        "summary": (
            "Sáng ngày 19 tháng 11, truyền thông quốc tế đồng loạt phân tích canh bạc quyền lực lịch sử của Liên đoàn bóng đá châu Âu nhằm chấm dứt triều đại của Chủ tịch FIFA Gianni Infantino. "
            "Sau khi hàng loạt ứng viên nặng ký như Arsene Wenger, Nasser al-Khelaifi hay Victor Montagliani lần lượt từ chối ra tranh cử, Chủ tịch UEFA Aleksander Ceferin đã quyết định chọn Chủ tịch Liên đoàn bóng đá Pháp Philippe Diallo vào phút chót. "
            "Nhà lãnh đạo 63 tuổi gốc Senegal công khai cáo buộc ông Infantino đưa ra hàng loạt quyết định đơn phương gây chia rẽ từ thương vụ bán cổ phần World Cup đến việc ưu ái các đồng minh thân cận, khiến niềm tin trong ngôi nhà chung bóng đá hoàn toàn sụp đổ. "
            "Để giành chiến thắng tại Đại hội FIFA lần thứ 77 ở Morocco vào tháng 3 năm sau, ông Diallo phải vượt qua bài toán 106 trên tổng số 211 lá phiếu trước thế lực tài trợ 3,4 tỷ USD mà ông Infantino đang rải khắp châu Phi và châu Á."
        ),
        "source": "VnExpress",
        "news_source": "VNEXPRESS",
        "credit": "VNEXPRESS / REUTERS",
        "slots": [
            _slot("title", 0, [_url(VNE_DIALLO_INF)], "VNEXPRESS / REUTERS", "Gianni Infantino và Philippe Diallo từ đồng minh trở thành đối thủ trực tiếp"),
            _slot("title", 0, [_url(VNE_DIALLO_STAD)], "VNEXPRESS", "Chủ tịch Liên đoàn bóng đá Pháp Philippe Diallo phát động chiến dịch tranh cử FIFA"),
            _slot("title", 0, [_url(VNE_WENGER)], "VNEXPRESS / REUTERS", "Arsene Wenger rút lui khiến UEFA chốt phương án Philippe Diallo"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(VNE_DIALLO_SP1)], "VNEXPRESS", "Cuộc đối đầu quyền lực nóng nhất thượng tầng bóng đá thế giới nhiệm kỳ 2027-2031"),
            _slot("sentence", 1, [_ddgs("FIFA headquarters Zurich building football")], "REUTERS", "UEFA tìm cách phá vỡ thế độc tôn của Gianni Infantino qua hai nhiệm kỳ gần nhất"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_url(VNE_TASHIMA)], "VNEXPRESS", "Arsene Wenger từ chối đối đầu trực tiếp dù từng chỉ trích thương vụ cổ phần World Cup"),
            _slot("sentence", 2, [_ddgs("Aleksander Ceferin UEFA president conference")], "UEFA", "Chủ tịch UEFA Aleksander Ceferin triệu tập họp khẩn và chọn Philippe Diallo"),
            _slot("sentence", 2, [_url(VNE_DIALLO_SP2)], "VNEXPRESS", "Ông Diallo được đánh giá là lá phiếu ôn hòa và có lợi thế gốc gác châu Phi"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_url(VNE_DIALLO_PR)], "VNEXPRESS", "Philippe Diallo tuyên chiến mạnh mẽ với các quyết định đơn phương của FIFA"),
            _slot("sentence", 3, [_ddgs("Gianni Infantino FIFA president speech stage")], "AP PHOTO", "Liên đoàn Na Uy đã gửi đơn khiếu nại đạo đức nhắm vào người đứng đầu FIFA"),
            _slot("sentence", 3, [_ddgs("Zinedine Zidane Emmanuel Macron football France")], "REUTERS", "Chiến dịch của Diallo nhận được sự hậu thuẫn từ Tổng thống Pháp và Zinedine Zidane"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("FIFA Congress voting hall international delegates")], "FIFA", "211 liên đoàn thành viên sẽ bỏ phiếu kín tại Rabat, Morocco vào tháng 3 năm sau"),
            _slot("sentence", 4, [_ddgs("Gianni Infantino World Cup trophy FIFA")], "REUTERS", "Infantino dùng gói tài trợ 3,4 tỷ USD để giữ chặt phiếu bầu từ châu Phi và châu Á"),
            _slot("sentence", 4, [_ddgs("Morocco football stadium Rabat night")], "AP PHOTO", "Cuộc đua cần ít nhất 106 phiếu hứa hẹn vô cùng khốc liệt trong bốn tháng tới"),
        ],
    },

    # 11 (Nam — Quốc tế 5: Erling Haaland 399 bàn vượt xa Ronaldo tuổi 26 & vượt Mbappé)
    {
        "id": 11,
        "art_id": "art_11",
        "group": "Nhóm: Tâm điểm bóng đá quốc tế",
        "title": "Erling Haaland chạm mốc 399 bàn ở tuổi 26, bỏ xa Ronaldo cùng độ tuổi và vượt Mbappé ở ĐTQG",
        "summary": (
            "Sau cú đúp đưa đội tuyển Na Uy ngược dòng hạ Đan Mạch 3-2 để vào tứ kết Nations League, cỗ máy ghi bàn Erling Haaland tiếp tục khiến truyền thông thế giới choáng ngợp với hàng loạt kỷ lục thống kê mới công bố rạng sáng ngày 19 tháng 11. "
            "Ở tuổi 26 và bốn tháng, tiền đạo của Manchester City đã chạm mốc 399 bàn thắng chỉ sau 473 trận chính thức và chỉ còn cách cột mốc 400 bàn đúng một pha lập công. "
            "Khi đặt lên bàn cân với Cristiano Ronaldo ở cùng độ tuổi 26, siêu sao Bồ Đào Nha khi đó đá nhiều hơn tới 24 trận nhưng chỉ ghi được 234 bàn, kém Haaland tới 165 bàn thắng với hiệu suất 0,47 bàn mỗi trận so với 0,84 của chân sút Na Uy. "
            "Không chỉ bỏ xa thành tích của đàn anh ở tuổi đôi mươi, Haaland còn chính thức vượt qua Kylian Mbappé ở cấp độ đội tuyển quốc gia với 68 bàn sau 61 trận, nhiều hơn đối thủ người Pháp một bàn dù thi đấu ít hơn tới 47 trận."
        ),
        "source": "Dân Trí / VnExpress",
        "news_source": "DÂN TRÍ / VNEXPRESS",
        "credit": "DÂN TRÍ / AP PHOTO",
        "slots": [
            _slot("title", 0, [_url(VNE_HAALAND_CELEB)], "VNEXPRESS / AP", "Erling Haaland đạt hiệu suất ghi bàn khủng khiếp nhất thế kỷ 21"),
            _slot("title", 0, [_url(DT_HAALAND_1)], "DÂN TRÍ", "Tiền đạo 26 tuổi chỉ còn thiếu một bàn để chạm mốc 400 bàn thắng sự nghiệp"),
            _slot("title", 0, [_url(DT_CR7_MU)], "DÂN TRÍ", "So sánh thống kê của Haaland và Cristiano Ronaldo ở tuổi 26 gây sốt mạng xã hội"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_05_1.jpg")], "REUTERS", "Cú đúp vào lưới Đan Mạch đưa Na Uy vào tứ kết Nations League"),
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_05_3.jpg")], "AP PHOTO", "Haaland đang dẫn đầu danh sách ghi bàn mọi thời đại tại Nations League với 23 bàn"),
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_05_8.jpg")], "REUTERS", "Pha sút phạt đền phút 90+6 khẳng định bản lĩnh của trung phong số một thế giới"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_ddgs("Erling Haaland Norway national team celebration")], "AP PHOTO", "399 bàn thắng sau 473 trận ở tuổi 26 năm 4 tháng là tốc độ săn bàn không tưởng"),
            _slot("sentence", 2, [_ddgs("Erling Haaland Manchester City goal celebration")], "AP PHOTO", "Anh cũng giữ kỷ lục chạm mốc 60 bàn tại Champions League nhanh nhất lịch sử"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Cristiano Ronaldo Manchester United 2008 goal")], "REUTERS", "Ở tuổi 26, Cristiano Ronaldo từng chơi thiên về biên và đạt 234 bàn sau 497 trận"),
            _slot("sentence", 3, [_ddgs("Cristiano Ronaldo Real Madrid 2011 football")], "REUTERS", "Từ sau tuổi 26, Ronaldo bùng nổ ngoạn mục để tiến tới mốc 985 bàn ở tuổi 41"),
            _slot("sentence", 3, [_ddgs("Erling Haaland Premier League Etihad Stadium")], "AP PHOTO", "Hiệu suất 0,84 bàn mỗi trận của Haaland gấp gần đôi Ronaldo thời điểm cùng tuổi"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("Kylian Mbappe France national team match")], "REUTERS", "Kylian Mbappé hiện có 67 bàn sau 108 lần khoác áo đội tuyển Pháp"),
            _slot("sentence", 4, [_ddgs("Erling Haaland Champions League Manchester City")], "REUTERS", "Haaland vượt lên với 68 bàn sau 61 trận, hiệu suất cao nhất thế giới trong 100 năm qua"),
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_05_6.jpg")], "REUTERS", "Hai siêu sao thế hệ mới tiếp tục cuộc đua phá vỡ mọi giới hạn ghi bàn"),
        ],
    },

    # 12 (Nữ — Quốc tế 6: Arsenal 3 lần chịu phạt đền oan & Ancelotti đấu khẩu Romario)
    {
        "id": 12,
        "art_id": "art_12",
        "group": "Nhóm: Tâm điểm bóng đá quốc tế",
        "title": "Arsenal lần thứ ba chịu phạt đền oan sau 10 vòng Ngoại hạng Anh; HLV Ancelotti đáp trả gắt Romario",
        "summary": (
            "Rạng sáng ngày 19 tháng 11, Hội đồng thẩm định các tình huống trọng yếu KMI của Ngoại hạng Anh công bố kết luận xác nhận đội đầu bảng Arsenal đã bị từ chối một quả phạt đền hợp lệ ở trận thắng Hull City hôm 7 tháng 11. "
            "Hội đồng khẳng định hậu vệ Nobel Mendy đã kéo ngã Kai Havertz trước khi tiền đạo người Đức tham gia tình huống, nâng tổng số sai sót phạt đền gây bất lợi cho Pháo thủ lên con số ba chỉ sau 10 vòng đầu tiên, bên cạnh hai pha bóng trước Aston Villa và Sunderland. "
            "Ở một diễn biến nóng khác tại Nam Mỹ, HLV Carlo Ancelotti đã đáp trả gay gắt sau khi huyền thoại Brazil Romario đăng bài công khai đòi Liên đoàn bóng đá nước này sa thải ông vì trận thua Nhật Bản. "
            "Chiến lược gia người Italy thẳng thắn tuyên bố Romario nói quá nhiều và chỉ biết ngồi ngoài bình luận ngớ ngẩn, trước khi các học trò của ông trút giận bằng trận đại thắng Singapore 7-0."
        ),
        "source": "VnExpress / Dân Trí",
        "news_source": "VNEXPRESS / DÂN TRÍ",
        "credit": "VNEXPRESS / DÂN TRÍ",
        "slots": [
            _slot("title", 0, [_url(VNE_ARS_KAI)], "VNEXPRESS", "Tình huống Kai Havertz bị kéo ngã trong vòng cấm nhưng Arsenal mất oan phạt đền"),
            _slot("title", 0, [_url(DT_ANCELLOTTI)], "DÂN TRÍ", "HLV Carlo Ancelotti nổi giận trước lời kêu gọi sa thải từ huyền thoại Romario"),
            _slot("title", 0, [_url(VNE_ARS_TIMBER)], "VNEXPRESS", "Công tác trọng tài và VAR tại Ngoại hạng Anh tiếp tục gây tranh cãi dữ dội"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_ddgs("Arsenal Emirates Stadium Premier League match")], "REUTERS", "KMI xác nhận trọng tài Farai Hallam đã sai lầm khi từ chối phạt đền cho Arsenal"),
            _slot("sentence", 1, [_ddgs("Mikel Arteta Arsenal manager touchline Emirates")], "REUTERS", "Dù chịu thiệt thòi, Arsenal vẫn giữ ngôi đầu bảng nhờ bàn thắng của Martin Odegaard"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_ddgs("Arsenal Martin Odegaard goal celebration Premier League")], "AP PHOTO", "Trọng tài cũng từng bỏ sót lỗi ở trận gặp Liverpool khiến tranh cãi thêm gay gắt"),
            _slot("sentence", 2, [_ddgs("Kai Havertz Arsenal football match action")], "AP PHOTO", "Mikel Arteta từng bức xúc khi phải xem lại tới 20 lần một tình huống phạt đền sai"),
            _slot("sentence", 2, [_ddgs("Premier League VAR referee screen football")], "REUTERS", "Vòng 10 Ngoại hạng Anh ghi nhận tới 6 quyết định trọng yếu bị KMI kết luận sai"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Carlo Ancelotti Brazil coach press conference")], "REUTERS", "Huyền thoại Romario kêu gọi sa thải Carlo Ancelotti dù ông mới dẫn dắt Brazil"),
            _slot("sentence", 3, [_ddgs("Romario Brazil football legend World Cup 1994")], "REUTERS", "Nhà vô địch World Cup 1994 cho rằng Ancelotti chỉ giỏi ở cấp độ câu lạc bộ"),
            _slot("sentence", 3, [_url(DT_BRA_SIN)], "DÂN TRÍ", "Căng thẳng bùng phát sau thất bại của Brazil trước Nhật Bản hôm 14/11"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("Carlo Ancelotti Brazil national team touchline")], "AP PHOTO", "Ancelotti thẳng thắn phản pháo trong buổi họp báo trước trận gặp Singapore"),
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_06_2.jpg")], "AP PHOTO", "Đội tuyển Brazil lập tức đáp trả bằng chiến thắng hủy diệt 7-0 trên sân khách"),
            _slot("sentence", 4, [_local(DAILY_18 / "Tin_06_1.jpg")], "AP PHOTO", "Liên đoàn bóng đá Brazil vẫn giữ trọn niềm tin với Ancelotti tới World Cup 2030"),
        ],
    },

    # 13 (Nam — Quốc tế 7: Bóng đá Indonesia nội loạn, Erick Thohir bị khiếu nại lên FIFA)
    {
        "id": 13,
        "art_id": "art_13",
        "group": "Nhóm: Tâm điểm bóng đá quốc tế",
        "title": "Làng bóng đá Indonesia nội loạn, Chủ tịch Futsal gửi đơn khiếu nại ông Erick Thohir tới FIFA và AFC",
        "summary": (
            "Bóng đá Đông Nam Á bất ngờ rúng động trước cuộc khủng hoảng thượng tầng tại Indonesia khi Chủ tịch Liên đoàn Futsal nước này là ông Michael Victor Sianipar gửi đơn khiếu nại chính thức lên Ủy ban Đạo đức Liên đoàn Bóng đá Indonesia PSSI. "
            "Căng thẳng bùng phát sau khi Chủ tịch PSSI kiêm Bộ trưởng Thể thao Erick Thohir và Tổng thư ký Yunus Nusi ký quyết định bãi nhiệm ông Sianipar vào ngày 12 tháng 11 để đưa bà Vivin Cahyani lên làm quyền chủ tịch. "
            "Phía ông Sianipar cáo buộc lãnh đạo PSSI lạm quyền, vi phạm điều lệ đại hội bầu cử và gây sức ép lên các tổ chức cấp tỉnh nhằm thâu tóm quyền lực, đồng thời gửi bản sao đơn tố cáo thẳng tới FIFA và AFC để yêu cầu điều tra độc lập. "
            "Đáp lại, PSSI khẳng định đã nhận đủ 48 văn bản đề nghị đại hội bất thường và tuyên bố sẽ tiến hành kiểm toán toàn diện nguồn tiền ngoài ngân sách của Liên đoàn Futsal."
        ),
        "source": "Tuổi Trẻ / Antara",
        "news_source": "TUỔI TRẺ / ANTARA",
        "credit": "TUỔI TRẺ / REUTERS",
        "slots": [
            _slot("title", 0, [_url(TT_THOHIR)], "TUỔI TRẺ", "Chủ tịch PSSI kiêm Bộ trưởng Erick Thohir đối mặt đơn khiếu nại lên Ủy ban Đạo đức"),
            _slot("title", 0, [_url(TT_SIANIPAR)], "TUỔI TRẺ / JANALOKA", "Chủ tịch Liên đoàn Futsal Indonesia Michael Victor Sianipar phản công quyết liệt"),
            _slot("title", 0, [_ddgs("Indonesia national football team stadium supporters")], "REUTERS", "Nội bộ bóng đá xứ vạn đảo rơi vào làn sóng đấu đá căng thẳng chưa từng có"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_ddgs("Indonesia Futsal Federation FFI Jakarta")], "ANTARA", "Ông Sianipar gửi đơn yêu cầu kiểm tra độc lập quy trình bãi nhiệm của PSSI"),
            _slot("sentence", 1, [_ddgs("Gelora Bung Karno stadium Jakarta Indonesia")], "REUTERS", "Vụ việc gây xôn xao dư luận thể thao Đông Nam Á từ tối 18/11"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_ddgs("Erick Thohir PSSI chairman press conference Indonesia")], "ANTARA", "Ông Erick Thohir ký quyết định chấm dứt công nhận ban lãnh đạo Futsal từ ngày 12/11"),
            _slot("sentence", 2, [_ddgs("Erick Thohir Indonesia minister PSSI press")], "ANTARA", "Thành viên ban chấp hành Vivin Cahyani được bổ nhiệm làm quyền chủ tịch"),
            _slot("sentence", 2, [_ddgs("Indonesia futsal national team match indoor")], "AFC", "Cuộc đối đầu bắt nguồn từ bất đồng tài chính và tiền trợ cấp cho các câu lạc bộ"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("PSSI Indonesia football association press conference")], "REUTERS", "Đơn khiếu nại cáo buộc một số lãnh đạo PSSI gây sức ép không công bố xung đột lợi ích"),
            _slot("sentence", 3, [_ddgs("FIFA headquarters flag football administration")], "FIFA", "Bản sao đơn tố cáo đã được gửi đồng thời tới FIFA và Liên đoàn bóng đá châu Á AFC"),
            _slot("sentence", 3, [_ddgs("Asian Football Confederation AFC Kuala Lumpur")], "AFC", "Giới quan sát lo ngại nguy cơ can thiệp hành chính có thể ảnh hưởng tới bóng đá Indonesia"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_ddgs("Indonesia football supporters national stadium")], "REUTERS", "PSSI khẳng định quyết định chuyển tiếp dựa trên 48 văn bản đề nghị từ CLB và các tỉnh"),
            _slot("sentence", 4, [_ddgs("Erick Thohir Inter Milan PSSI Indonesia")], "REUTERS", "Tổng thư ký Yunus Nusi thông báo sẽ kiểm toán nguồn tiền của Liên đoàn Futsal"),
        ],
    },

    # 14 (Nữ — Tinh hoa 1: Lê Quang Liêm tranh hạng 7 gặp Ian Nepomniachtchi & Elo Lại Lý Huynh)
    {
        "id": 14,
        "art_id": "art_14",
        "group": "Nhóm: Tinh hoa thể thao VN & thế giới",
        "title": "Lê Quang Liêm thua Hans Niemann ở bán kết nhánh 5-8, tranh hạng 7 gặp Ian Nepomniachtchi",
        "summary": (
            "Rạng sáng ngày 19 tháng 11 tại Giải vô địch cờ vua toàn năng thế giới 2026 ở Hungary, kỳ thủ số một Việt Nam Lê Quang Liêm đã khép lại trận lượt về bán kết nhánh tranh hạng 5 đến 8 trước đối thủ Mỹ Hans Moke Niemann. "
            "Dù khởi đầu rực sáng khi thắng hai, hòa một ở bốn ván cờ chớp, Quang Liêm lại sảy chân ở ván cờ nhanh và ván cờ tiêu chuẩn quyết định để chấp nhận thua chung cuộc với điểm số 4,5-15,5. "
            "Với kết quả này, kỳ thủ Việt Nam sẽ bước vào loạt trận tranh hạng bảy kéo dài hai ngày gặp siêu đại kiện tướng Nga Ian Nepomniachtchi, nơi người thắng nhận 34000 USD còn người thua nhận 32000 USD trước khi anh trở về khoác áo TP.HCM dự Đại hội Thể thao toàn quốc. "
            "Ở môn cờ tướng, giới chuyên môn vừa giải mã nghịch lý vì sao đương kim á quân thế giới cờ nhanh Lại Lý Huynh chỉ xếp hạng 37 trên bảng Elo Quảng Tượng Võng với 2572 điểm trong khi đứng thứ 15 bảng CXA, nguyên nhân là do anh thi đấu ít giải tại Trung Quốc và bảng Elo này gộp chung cả các nữ cao thủ như Đường Đan."
        ),
        "source": "Thanh Niên / Tuổi Trẻ",
        "news_source": "THANH NIÊN / TUỔI TRẺ",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "slots": [
            _slot("title", 0, [_url(TN_LQL_GS)], "THANH NIÊN / CHESS.COM", "Lê Quang Liêm bước vào trận tranh hạng bảy giải cờ vua toàn năng thế giới 2026"),
            _slot("title", 0, [_ddgs("Ian Nepomniachtchi chess grandmaster FIDE")], "FIDE", "Nhà vô địch cờ chớp thế giới 2024 Ian Nepomniachtchi là đối thủ cuối cùng của Quang Liêm"),
            _slot("title", 0, [_url(TT_LLH)], "TUỔI TRẺ", "Kỳ thủ Lại Lý Huynh vừa tăng từ hạng 42 lên hạng 37 trên bảng Elo Quảng Tượng Võng"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_14_1.jpg")], "THANH NIÊN", "Lê Quang Liêm khép lại lượt về trước Hans Niemann vào rạng sáng 19/11"),
            _slot("sentence", 1, [_local(DAILY_18 / "Tin_14_3.jpg")], "FIDE", "Kỳ thủ Mỹ Hans Moke Niemann giành quyền vào chơi trận tranh hạng 5"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_14_4.jpg")], "THANH NIÊN", "Quang Liêm thắng 2, hòa 1, thua 1 trong 4 ván cờ chớp đầy hưng phấn"),
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_14_8.jpg")], "FIDE", "Thất bại ở ván cờ tiêu chuẩn tính 8 điểm khiến đại diện Việt Nam thua 4,5-15,5"),
            _slot("sentence", 2, [_local(DAILY_18 / "Tin_14_5.jpg")], "WIKIMEDIA COMMONS", "Dù dừng bước, Quang Liêm vẫn có giải đấu thành công khi áp sát tốp 10 thế giới"),
            # Câu 3 (4 ảnh)
            _slot("sentence", 3, [_ddgs("Ian Nepomniachtchi FIDE chess match portrait")], "FIDE", "Ian Nepomniachtchi thi đấu dưới màu áo FIDE là thử thách đẳng cấp cao"),
            _slot("sentence", 3, [_local(DAILY_18 / "Tin_14_7.jpg")], "VNEXPRESS", "Trận tranh hạng 7 mang về tối thiểu 32000 USD và tối đa 34000 USD tiền thưởng"),
            _slot("sentence", 3, [_ddgs("Budapest Hungary chess tournament hall")], "TOTAL CHESS", "Thể thức hai ngày gồm cờ chớp, cờ nhanh và cờ tiêu chuẩn đầy kịch tính"),
            _slot("sentence", 3, [_ddgs("Le Quang Liem Vietnam chess grandmaster")], "THANH NIÊN", "Sau giải tại Hungary, Lê Quang Liêm sẽ về nước dự Đại hội Thể thao toàn quốc"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("Lai Ly Huynh co tuong Vietnam xiangqi")], "TUỔI TRẺ", "Lại Lý Huynh hiện xếp hạng 15 bảng CXA và hạng 37 bảng Quảng Tượng Võng"),
            _slot("sentence", 4, [_ddgs("xiangqi chinese chess board tournament")], "TUỔI TRẺ", "Thứ hạng Elo bị ảnh hưởng vì kỳ thủ Việt Nam ít tham dự các giải địa phương Trung Quốc"),
            _slot("sentence", 4, [_ddgs("xiangqi chess grandmaster competition China")], "TUỔI TRẺ", "Hai hệ thống tính điểm khác biệt không phản ánh hết thực lực của Nam phương công tử"),
        ],
    },

    # 15 (Nam — Tinh hoa 2: Carlos Alcaraz thắng áp đảo Daniil Medvedev 6-2, 6-4)
    {
        "id": 15,
        "art_id": "art_15",
        "group": "Nhóm: Tinh hoa thể thao VN & thế giới",
        "title": "Carlos Alcaraz thắng áp đảo Daniil Medvedev 6-2, 6-4, chạm tay vào vé bán kết ATP Finals 2026",
        "summary": (
            "Tại lượt trận thứ hai bảng Ivan Lendl giải quần vợt ATP Finals 2026 ở Turin đêm ngày 18 tháng 11, hạt giống số hai Carlos Alcaraz có màn trình diễn hủy diệt để đánh bại Daniil Medvedev với tỷ số 6-2 và 6-4 chỉ sau 72 phút. "
            "Tay vợt 23 tuổi người Tây Ban Nha thi đấu thăng hoa đến mức không phải đối mặt với bất kỳ điểm break-point nào trong suốt trận đấu, nối dài mạch toàn thắng lên con số 11 trận liên tiếp trên sân cứng trong nhà châu Âu. "
            "Dù có khoảnh khắc phải nhờ đội ngũ y tế chăm sóc vùng đùi trái khi đang dẫn 2-1 ở set hai, Alcaraz vẫn hoàn toàn làm chủ cuộc chơi nhờ những cú trả giao bóng hai sâu và hiểm hóc, qua đó nâng thành tích đối đầu trước Medvedev lên 8-3. "
            "Với hai trận toàn thắng, Alcaraz sẽ chính thức đoạt vé sớm vào bán kết ngay trong sáng nay nếu trận đấu giữa Frances Tiafoe và tay vợt chủ nhà Flavio Cobolli có lợi thế cho đại diện Mỹ."
        ),
        "source": "Dân Trí / ATP Tour",
        "news_source": "DÂN TRÍ / ATP TOUR",
        "credit": "DÂN TRÍ / ATP TOUR",
        "slots": [
            _slot("title", 0, [_url(DT_ALCARAZ)], "DÂN TRÍ", "Carlos Alcaraz thể hiện phong độ hủy diệt tại Inalpi Arena ở Turin"),
            _slot("title", 0, [_url(DT_MEDVEDEV)], "DÂN TRÍ", "Daniil Medvedev hoàn toàn bất lực trước những cú trả giao bóng của Alcaraz"),
            _slot("title", 0, [_ddgs("ATP Finals Turin Inalpi Arena tennis court")], "ATP TOUR", "Ngôi sao Tây Ban Nha tiến sát tấm vé bán kết giải đấu quy tụ 8 tay vợt hay nhất năm"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_ddgs("Carlos Alcaraz Daniil Medvedev ATP Finals match")], "ATP TOUR", "Alcaraz giải quyết gọn cựu số một thế giới Medvedev chỉ trong 72 phút thi đấu"),
            _slot("sentence", 1, [_ddgs("Daniil Medvedev tennis serve indoor hard court")], "REUTERS", "Medvedev giao bóng một tốt nhưng liên tục bị khai thác ở lượt giao bóng hai"),
            _slot("sentence", 1, [_ddgs("Carlos Alcaraz forehand tennis ATP Finals")], "ATP TOUR", "Tỷ số 6-2 và 6-4 giúp Alcaraz dẫn đầu tuyệt đối tại bảng Ivan Lendl"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_ddgs("Carlos Alcaraz backhand tennis action court")], "REUTERS", "Tay vợt 23 tuổi không để đối thủ có nổi một cơ hội bẻ game giao bóng nào"),
            _slot("sentence", 2, [_ddgs("Carlos Alcaraz celebrating indoor hard court tennis")], "REUTERS", "Chuỗi 11 trận thắng liên tiếp khẳng định sự thích nghi hoàn hảo trên sân cứng trong nhà"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Carlos Alcaraz medical timeout leg tennis match")], "ATP TOUR", "Đội ngũ y tế kiểm tra đùi trái cho Alcaraz ở đầu set hai nhưng không đáng ngại"),
            _slot("sentence", 3, [_ddgs("Daniil Medvedev frustrated tennis court ATP")], "REUTERS", "Alcaraz nâng tỷ số đối đầu trước Medvedev lên 8 thắng và chỉ 3 thua"),
            _slot("sentence", 3, [_ddgs("Carlos Alcaraz smiling post match interview tennis")], "REUTERS", "Anh đã thắng tới 5 trong 6 lần chạm trán các tay vợt tốp 5 thế giới mùa này"),
            # Câu 4 (2 ảnh)
            _slot("sentence", 4, [_ddgs("Frances Tiafoe tennis ATP match")], "ATP TOUR", "Kết quả cặp đấu giữa Frances Tiafoe và Flavio Cobolli sẽ chốt vé sớm cho Alcaraz"),
            _slot("sentence", 4, [_ddgs("Inalpi Arena Turin ATP Finals tennis crowd")], "ATP TOUR", "Medvedev sẽ phải quyết đấu sinh tử với Tiafoe ở lượt cuối vòng bảng"),
        ],
    },

    # 16 (Nữ — Tinh hoa 3: Nữ võ sĩ Vovinam Kim Lụa & Thùy Linh tại Đại hội TDTT toàn quốc)
    {
        "id": 16,
        "art_id": "art_16",
        "group": "Nhóm: Tinh hoa thể thao VN & thế giới",
        "title": "Xúc động nữ võ sĩ Vovinam Kim Lụa giành HCV kiếm tiền chữa bệnh cho em; Thùy Linh lỡ chung kết cầu lông",
        "summary": (
            "Tại Đại hội Thể thao toàn quốc lần thứ X năm 2026 đang sôi động ở TP.HCM, câu chuyện phía sau tấm huy chương vàng Vovinam hạng cân 45-50kg nữ của nữ võ sĩ Nguyễn Thị Kim Lụa đoàn Quân đội khiến người hâm mộ không khỏi xúc động. "
            "Suốt hơn một năm qua, cô gái 30 tuổi vừa miệt mài tập luyện đỉnh cao và đi dạy giáo dục thể chất kiếm thu nhập, vừa túc trực ăn ngủ trong bệnh viện chăm sóc cô em gái bị tai nạn giao thông nặng khiến cô mất khả năng đi lại. "
            "Với Kim Lụa, tấm huy chương vàng danh giá này không chỉ là vinh quang thể thao mà còn mang về nguồn tiền thưởng quý giá giúp gia đình chuẩn bị cho ca phẫu thuật thay khớp háng của em gái vào đầu năm 2027. "
            "Cũng tại đại hội ở môn cầu lông diễn ra chiều ngày 18 tháng 11, đội nữ Đồng Nai của tay vợt số một Việt Nam Nguyễn Thùy Linh bất ngờ để thua Hà Nội 1-3 tại bán kết đồng đội và chỉ giành huy chương đồng, trong khi chủ nhà TP.HCM khẳng định sức mạnh khi tiến vào cả hai trận chung kết đồng đội nam và nữ ngày 19 tháng 11."
        ),
        "source": "Tuổi Trẻ / Dân Trí",
        "news_source": "TUỔI TRẺ / DÂN TRÍ",
        "credit": "TUỔI TRẺ / DÂN TRÍ",
        "slots": [
            _slot("title", 0, [_url(TT_KIMLUA_1)], "TUỔI TRẺ", "Nữ võ sĩ Nguyễn Thị Kim Lụa rạng rỡ với tấm HCV Vovinam hạng cân 45-50kg"),
            _slot("title", 0, [_url(TT_KIMLUA_2)], "TUỔI TRẺ", "Kim Lụa thi đấu kiên cường để mang vinh quang về cho đoàn Quân đội"),
            _slot("title", 0, [_ddgs("Nguyen Thuy Linh badminton Vietnam player")], "DÂN TRÍ", "Tay vợt số một Việt Nam Nguyễn Thùy Linh cùng Đồng Nai nhận HCĐ đồng đội"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_ddgs("Vovinam gold medal podium Vietnam games")], "TUỔI TRẺ", "Kim Lụa vượt qua 18 đối thủ mạnh nhất cả nước để bước lên bục cao nhất"),
            _slot("sentence", 1, [_ddgs("Vovinam martial arts sparring match Vietnam")], "TUỔI TRẺ", "Gắn bó 11 năm với thể thao Quân đội, nữ võ sĩ luôn xem mỗi trận đấu là chung kết"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_ddgs("Vovinam female athlete coach Vietnam training")], "TUỔI TRẺ", "Biến cố tai nạn tháng 3/2025 của em gái khiến Kim Lụa phải gánh vác nhiều hơn"),
            _slot("sentence", 2, [_ddgs("Vietnamese martial arts Vovinam training hall")], "TUỔI TRẺ", "Cô vừa tập luyện cho đại hội vừa đi dạy để trang trải chi phí điều trị"),
            _slot("sentence", 2, [_ddgs("Vovinam martial arts Vietnam tournament competition")], "TUỔI TRẺ", "Ý chí thép giúp nữ võ sĩ Quân khu 7 đứng vững trước nghịch cảnh gia đình"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_ddgs("gold medal sports victory celebration Vietnam")], "TUỔI TRẺ", "Tiền thưởng từ tấm HCV tiếp thêm hy vọng cho ca phẫu thuật đầu năm 2027 của em gái"),
            _slot("sentence", 3, [_local(DAILY_18 / "Tin_13_1.jpg")], "THANH NIÊN", "Đại hội Thể thao toàn quốc 2026 quy tụ 12000 VĐV ở 48 môn thi đấu"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("Nguyen Thuy Linh Vietnam badminton smash")], "DÂN TRÍ", "Thùy Linh thắng trận đơn mở màn nhưng Đồng Nai vẫn thua ngược Hà Nội 1-3"),
            _slot("sentence", 4, [_ddgs("badminton womens doubles indoor court tournament")], "TUỔI TRẺ", "Cặp Thùy Linh và Ngọc Thúy để thua 1-2 ở trận đôi quyết định"),
            _slot("sentence", 4, [_ddgs("Ho Xuan Huong gymnasium Ho Chi Minh City badminton")], "TUỔI TRẺ", "Đoàn chủ nhà TP.HCM đối đầu Hà Nội và Quân đội ở chung kết đồng đội ngày 19/11"),
        ],
    },

    # 17 (Nam — Tinh hoa 4: Bóng bàn VN thưởng 400 triệu & Lý do Quyết Chiến, Phương Vinh vắng Đại hội)
    {
        "id": 17,
        "art_id": "art_17",
        "group": "Nhóm: Tinh hoa thể thao VN & thế giới",
        "title": "Tuyển bóng bàn Việt Nam nhận thưởng 400 triệu đồng; lý do Quyết Chiến và Phương Vinh vắng Đại hội toàn quốc",
        "summary": (
            "Trưa ngày 18 tháng 11 tại Hà Nội, Liên đoàn Bóng bàn Việt Nam cùng các nhà tài trợ đã tổ chức lễ mừng công và trao thưởng tổng cộng 400 triệu đồng cho đội tuyển bóng bàn quốc gia sau thành tích 2 huy chương vàng, 1 huy chương bạc và 2 huy chương đồng tại giải vô địch Đông Nam Á ở Malaysia. "
            "Ngoài phần thưởng nóng của liên đoàn với ngôi sao Nguyễn Anh Tú góp công lớn ở cú đúp huy chương vàng đơn nam và đồng đội nam, các tuyển thủ còn nhận thêm tiền thưởng theo chế độ nhà nước để hướng tới mục tiêu SEA Games 34 năm 2027. "
            "Ở môn billiards, ban tổ chức lý giải nguyên nhân bất ngờ khiến hai cơ thủ hàng đầu thế giới là Trần Quyết Chiến và Bao Phương Vinh đều vắng mặt tại Đại hội Thể thao toàn quốc năm nay. "
            "Theo quy định giới hạn suất mỗi địa phương, hai ngôi sao này đã không vượt qua đợt đấu vòng tròn sát hạch nội bộ của TP.HCM hồi tháng 8 trước phong độ ổn định hơn của Trần Thanh Lực và Nguyễn Hoàn Tất, qua đó dồn toàn lực chuẩn bị cho chặng World Cup billiards tại Ai Cập vào đầu tháng 12."
        ),
        "source": "Tuổi Trẻ / Thanh Niên",
        "news_source": "TUỔI TRẺ / THANH NIÊN",
        "credit": "THANH NIÊN / TUỔI TRẺ",
        "slots": [
            _slot("title", 0, [_url(TN_BONGBAN_1)], "THANH NIÊN", "Liên đoàn Bóng bàn Việt Nam trao thưởng nóng 400 triệu đồng trưa 18/11"),
            _slot("title", 0, [_url(TN_QUYETCHIEN)], "THANH NIÊN", "Trần Quyết Chiến bất ngờ lỡ hẹn Đại hội Thể thao toàn quốc vì trượt sát hạch nội bộ"),
            _slot("title", 0, [_url(TT_BONGBAN_2)], "TUỔI TRẺ", "Nguyễn Anh Tú và đồng đội mang về 5 tấm huy chương từ giải Đông Nam Á"),
            # Câu 1 (3 ảnh)
            _slot("sentence", 1, [_url(TT_BONGBAN_1)], "TUỔI TRẺ", "Chủ tịch Nguyễn Xuân Vũ chúc mừng thắng lợi của đội tuyển bóng bàn tại Hà Nội"),
            _slot("sentence", 1, [_url(TN_BONGBAN_3)], "THANH NIÊN", "Đội tuyển giành 2 HCV, 1 HCB và 2 HCĐ tại Kuala Lumpur"),
            _slot("sentence", 1, [_ddgs("Nguyen Anh Tu table tennis Vietnam player")], "THANH NIÊN", "Toàn đội nhận tổng thưởng nóng 400 triệu đồng từ liên đoàn và nhà tài trợ"),
            # Câu 2 (2 ảnh)
            _slot("sentence", 2, [_url(TN_BONGBAN_2)], "THANH NIÊN", "HLV Vũ Văn Trung khẳng định toàn đội không ngủ quên trên chiến thắng"),
            _slot("sentence", 2, [_ddgs("Vietnam table tennis team SEA Games match")], "THANH NIÊN", "Các tuyển thủ hướng tới Giải các cây vợt xuất sắc quốc gia tại Cao Bằng tháng 12"),
            # Câu 3 (2 ảnh)
            _slot("sentence", 3, [_ddgs("Tran Quyet Chien billiards carom 3 cushion")], "UMB", "Sự vắng mặt của Trần Quyết Chiến và Bao Phương Vinh gây bất ngờ cho người hâm mộ"),
            _slot("sentence", 3, [_ddgs("Bao Phuong Vinh billiards carom 3 cushion")], "THANH NIÊN", "Billiards Việt Nam có cuộc cạnh tranh suất dự đại hội cực kỳ khốc liệt"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_url(TN_HOANTAT)], "THANH NIÊN", "Nguyễn Hoàn Tất và Trần Thanh Lực là hai đại diện giành vé của TP.HCM"),
            _slot("sentence", 4, [_ddgs("Tran Thanh Luc billiards World Cup 3 cushion")], "UMB", "Trần Quyết Chiến sẽ phải đấu từ vòng loại thứ tư tại World Cup Ai Cập đầu tháng 12"),
            _slot("sentence", 4, [_ddgs("carom 3 cushion billiards table tournament match")], "UMB", "Môn billiards Đại hội toàn quốc tranh tài 10 nội dung tại nhà thi đấu Nguyễn Du"),
        ],
    },

    # 18 (Nữ — Tinh hoa 5: Allison Quynh Lee, Dylan Kerr trở lại Hải Phòng & Wonderboy Thompson)
    {
        "id": 18,
        "art_id": "art_18",
        "group": "Nhóm: Tinh hoa thể thao VN & thế giới",
        "title": "Tay vợt gốc Việt Allison Quynh Lee lập địa chấn cầu lông; Hải Phòng đón lại HLV Dylan Kerr và màn chia tay của Thompson",
        "summary": (
            "Khép lại bản tin hôm nay là loạt điểm nhấn đáng chú ý trên các đấu trường cầu lông, V-League và võ thuật tổng hợp vừa được cập nhật tới sáng ngày 19 tháng 11. "
            "Tại giải cầu lông Hong Kong Open, tay vợt nữ 21 tuổi người Mỹ gốc Việt Allison Quynh Lee cùng đồng đội Lauren Lam xuất sắc đánh bại cặp hạt giống số bảy của Indonesia là Kusuma và Puspita sau ba set với tỷ số 21-16, 13-21 và 21-15, đánh dấu lần thứ ba chỉ trong 35 ngày họ loại đôi vợt hàng đầu thế giới này. "
            "Ở V-League, câu lạc bộ Hải Phòng chính thức đưa người cũ Dylan Kerr trở lại sau hơn một thập kỷ với chức danh Giám đốc kỹ thuật thay thế ông Đặng Văn Thành, chuẩn bị cho trận ra mắt gặp Thép Xanh Nam Định vào ngày 21 tháng 11. "
            "Còn tại đấu trường UFC ở New York, huyền thoại 43 tuổi Stephen Wonderboy Thompson vừa khép lại sự nghiệp 14 năm lừng lẫy bằng cú đá xoay trúng đầu hạ knock-out mãn nhãn đối thủ Charles Radtke ngay tại Madison Square Garden."
        ),
        "source": "Tuổi Trẻ",
        "news_source": "TUỔI TRẺ",
        "credit": "TUỔI TRẺ / BWF / UFC",
        "slots": [
            _slot("title", 0, [_url(TT_ALLISON_1)], "TUỔI TRẺ / BWF", "Tay vợt gốc Việt Allison Quynh Lee vỡ òa ăn mừng chiến thắng tại Hong Kong Open"),
            _slot("title", 0, [_url(TT_DYLAN)], "TUỔI TRẺ / ERIK TUNG", "Ông Dylan Kerr trở lại dẫn dắt câu lạc bộ Hải Phòng sau hơn một thập kỷ"),
            _slot("title", 0, [_ddgs("Stephen Wonderboy Thompson UFC octagon kick")], "UFC", "Huyền thoại Stephen Thompson kết thúc sự nghiệp bằng đòn đá knock-out đẹp mắt"),
            # Câu 1 (2 ảnh)
            _slot("sentence", 1, [_url(TT_ALLISON_2)], "TUỔI TRẺ / BWF", "Cầu lông quốc tế và V-League đón nhận nhiều chuyển biến thú vị"),
            _slot("sentence", 1, [_ddgs("V-League Vietnam football match stadium")], "V-LEAGUE", "Các câu lạc bộ V-League tích cực chỉnh đốn nhân sự trong quãng nghỉ FIFA Days"),
            # Câu 2 (3 ảnh)
            _slot("sentence", 2, [_ddgs("Allison Lee Lauren Lam badminton BWF")], "BWF", "Allison Quynh Lee và Lauren Lam xếp hạng 14 thế giới nhưng liên tiếp hạ tốp 10"),
            _slot("sentence", 2, [_ddgs("BWF World Tour badminton doubles rally match")], "BWF", "Cặp đôi Mỹ gốc Việt tiến gần tấm vé dự BWF World Tour Finals tại Hàng Châu"),
            _slot("sentence", 2, [_ddgs("Kai Tak Sports Park Hong Kong badminton arena")], "BWF", "Chiến thắng sau 61 phút kịch tính đưa đôi vợt Mỹ vào vòng 16 đội mạnh nhất"),
            # Câu 3 (3 ảnh)
            _slot("sentence", 3, [_ddgs("Dylan Kerr football coach Hai Phong")], "TUỔI TRẺ", "Ông Dylan Kerr từng giúp Hải Phòng vô địch Cúp quốc gia 2014"),
            _slot("sentence", 3, [_ddgs("Hai Phong FC Lach Tray stadium V-League football")], "V-LEAGUE", "Hải Phòng hiện đứng thứ 6 V-League và sẽ làm khách trên sân Thiên Trường ngày 21/11"),
            _slot("sentence", 3, [_ddgs("Thien Truong stadium Nam Dinh football match")], "V-LEAGUE", "Đội bóng đất cảng đăng ký ông làm Giám đốc kỹ thuật do thủ tục bằng cấp"),
            # Câu 4 (3 ảnh)
            _slot("sentence", 4, [_ddgs("Stephen Thompson UFC spinning wheel kick")], "UFC", "Stephen Thompson tung cú đá xoay giò lái hạ gục Charles Radtke ở hiệp ba"),
            _slot("sentence", 4, [_ddgs("Madison Square Garden UFC MMA octagon night")], "UFC", "Chiến thắng thứ 18 ở MMA khép lại hành trình 14 năm đầy cảm xúc tại UFC"),
            _slot("sentence", 4, [_ddgs("Stephen Wonderboy Thompson karate MMA fighter")], "UFC", "Võ sĩ 43 tuổi từng sở hữu chuỗi 57 trận bất bại ở đấu trường kickboxing"),
        ],
    },
]
