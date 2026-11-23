# -*- coding: utf-8 -*-
"""
core/prepare_digest_weekly_23_11.py — Sinh cấu hình `outputs/Weekly-23.11.2026/shorts/digest_specs.json`
====================================================================================================
Tạo Video Short Tổng Hợp Tuần 9:16 (< 180s) cho Weekly-23.11.2026:
  - Bổ sung đoạn Mở Đầu (Intro Hook ~5 giây) kèm montage 3 ảnh tiêu điểm tuần.
  - Điểm danh 20 sự kiện thể thao nổi bật nhất tuần (01–08 Việt Nam: Nữ Ngọc Huyền;
    09–20 Quốc tế: Nam Minh Quân Pro), đồng bộ 100% với video dài Weekly-23.11.2026.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent
DAY_STR = "Weekly-23.11.2026"
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
SHORTS_DIR = DAY_DIR / "shorts"
SPEC_PATH = SHORTS_DIR / "digest_specs.json"


DIGEST_SPECS = {
    "day": DAY_STR,
    "title": "TIN NHANH TUẦN 23.11",
    "hide_date_chip": False,
    "out_video_name": "Short_Tin_Nhanh_Tuan_23_11.mp4",
    "gap_ms": 190,
    "seo_title": "Tin tuần 23/11: U17 Việt Nam, Liverpool 4-0 Man Utd & Đại hội toàn quốc",
    "description": [
        "Tổng hợp nhanh 20 sự kiện thể thao Việt Nam và thế giới nóng nhất tuần qua (18–23/11/2026) chỉ trong chưa đầy 3 phút.",
        "Tâm điểm tuyển Việt Nam với chấn thương nghỉ hết năm của Đình Bắc, hai siêu phẩm lịch sử của U17 Việt Nam vào lưới U17 Bỉ, mưa kỷ lục bơi lội Đại hội Thể thao toàn quốc 2026, Liverpool vùi dập Manchester United 4-0 trong ngày ra mắt của Pochettino, Carlos Alcaraz vô địch ATP Finals và Marc Márquez san bằng kỷ lục tám lần vô địch MotoGP.",
    ],
    "fb_hook": "🔥 TỔNG HỢP 20 SỰ KIỆN THỂ THAO CHẤN ĐỘNG NHẤT TUẦN QUA (18–23/11) TRONG CHƯA ĐẦY 3 PHÚT!",
    "tiktok_caption": "Một tuần thể thao bùng nổ: U17 Việt Nam ghi 2 siêu phẩm World Cup, Ánh Viên giành HCB Đại hội, Liverpool hủy diệt Man Utd 4-0 khiến Pochettino lập kỷ lục tệ nhất 100 năm, Alcaraz vô địch ATP Finals và Marc Márquez lần thứ 8 vô địch MotoGP!",
    "sources_line": "📰 Nguồn tin: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian, ESPN.",
    "hashtags": [
        "#Shorts",
        "#TinNhanh",
        "#DiemDoc",
        "#DiemDocTheThao",
        "#TongHopTuan",
        "#U17VietNam",
        "#Liverpool",
        "#ManUtd",
        "#DaiHoiTheThaoToanQuoc",
        "#MarcMarquez",
    ],
    "thumb": {
        "image": "Tin_09_1.jpg",
        "kicker": "ĐIỂM NHANH 20 SỰ KIỆN THỂ THAO TUẦN QUA",
        "hero_html": '<span class="hl-cyan">20 TIN NÓNG TUẦN!</span><br><span class="hl-white">LIVERPOOL HỦY DIỆT</span><br><span class="hl-yellow">MAN UNITED 4-0!</span>',
        "subtitle": "U17 VIỆT NAM • ĐẠI HỘI 2026 • ALCARAZ • MÁRQUEZ",
        "badge": "TỔNG HỢP TUẦN",
        "tag_a": "VN & QUỐC TẾ",
        "tag_b": "TUẦN 23.11.2026",
        "hero_size": "74",
        "obj_pos": "center 20%",
    },
    "items": [
        {
            "id": 0,
            "is_intro": True,
            "pill_label": "MỞ ĐẦU • TIN TUẦN",
            "region": "Mở đầu",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_02_1.jpg",
            "extra_images": ["Tin_06_1.jpg", "Tin_09_1.jpg"],
            "news_source": "ĐIỂM ĐỌC • TỔNG HỢP TUẦN",
            "title": "TỔNG HỢP 20 SỰ KIỆN THỂ THAO NÓNG NHẤT TUẦN QUA",
            "digest_line": "Chào mừng đến Điểm Đọc! Một tuần rúng động từ U17 World Cup, Đại hội toàn quốc tới thảm họa Anfield! Bắt đầu ngay!",
        },
        {
            "id": 1,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_01_1.jpg",
            "title": "Tuyển Việt Nam thua Kyrgyzstan, Đình Bắc nghỉ hết năm 2026",
            "digest_line": "Tuyển Việt Nam thua ngược Kyrgyzstan 1-2 xuống hạng 99 FIFA nhưng giữ hạt giống hai World Cup 2030; Đình Bắc chấn thương nghỉ hết năm.",
        },
        {
            "id": 2,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_02_1.jpg",
            "title": "U17 Việt Nam ghi 2 siêu phẩm lịch sử trước khi đấu New Zealand",
            "digest_line": "Lê Sỹ Bách đánh gót và Nguyễn Lực đá phạt góc vào lưới U17 Bỉ, giúp U17 Việt Nam tự tin quyết đấu New Zealand tối 23/11.",
        },
        {
            "id": 3,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_03_1.jpg",
            "title": "V-League Vòng 8: Nam Định đầu bảng, Thanh Hóa phá dớp 8 năm",
            "digest_line": "Nam Định giữ đỉnh bảng 19 điểm, Hoàng Đức giúp Ninh Bình lên nhì, còn Thanh Hóa phá dớp tám năm thắng Hoàng Anh Gia Lai 2-1.",
        },
        {
            "id": 4,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_04_1.jpg",
            "title": "Công an TP.HCM hạ ĐKVĐ Buriram 1-0 tại Shopee Cup",
            "digest_line": "Siêu phẩm phút 88 của Quốc Cường giúp Công an TP.HCM hạ ĐKVĐ Buriram 1-0, trong khi Công an Hà Nội thua Johor 1-3.",
        },
        {
            "id": 5,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_05_1.jpg",
            "title": "Khai mạc Đại hội Toàn quốc: TP.HCM bứt phá 109 huy chương",
            "digest_line": "Đại hội Toàn quốc 2026 khai mạc bên sông Sài Gòn; TP.HCM dẫn đầu với 109 huy chương và 41 vàng dù Hoàng Sao bị loại sốc.",
        },
        {
            "id": 6,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_06_1.jpg",
            "title": "Bơi lội mưa kỷ lục: Ánh Viên HCB, Watson vượt Thanh Bảo",
            "digest_line": "Mỹ Tiên phá kỷ lục đại hội thắng Ánh Viên ở 200 mét hỗn hợp; Watson Nguyễn vượt Thanh Bảo lập kỷ lục quốc gia 50 mét ếch.",
        },
        {
            "id": 7,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_07_2.jpg",
            "title": "Lê Quang Liêm trở lại Top 15 thế giới & dự giải 250000 USD",
            "digest_line": "Lê Quang Liêm thắng Nepomniachtchi 14-6 xếp hạng tám Total Chess, trở lại Top 15 thế giới và bước vào siêu giải 250000 USD.",
        },
        {
            "id": 8,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_08_1.jpg",
            "title": "Bùi Đình Khải hạ knock-out hiệp 1; P Esports vào chung kết thế giới",
            "digest_line": "Bùi Đình Khải hạ knock-out cựu vương Muay Lê Hoàng Đức ngay hiệp một, còn P Esports giành vé vào chung kết Free Fire thế giới.",
        },
        {
            "id": 9,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_09_1.jpg",
            "title": "Liverpool đè bẹp Man Utd 4-0: Pochettino lập kỷ lục tệ nhất 100 năm",
            "digest_line": "Sau thẻ đỏ phút thứ tám của Leny Yoro, Liverpool đè bẹp Man Utd 4-0 tại Anfield khiến Pochettino ra mắt tệ nhất 100 năm.",
        },
        {
            "id": 10,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_10_1.jpg",
            "title": "Ngoại hạng Anh: Chelsea thua Leeds 1-4, Man City hòa Fulham",
            "digest_line": "Chelsea thua đậm Leeds 1-4 tại Stamford Bridge, VAR hủy bàn Haaland khiến Man City hòa Fulham 1-1 còn Arsenal hòa Newcastle 2-2.",
        },
        {
            "id": 11,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_11_1.jpg",
            "title": "Haaland chạm mốc 399 bàn; Tây Ban Nha đụng Pháp tại Nations League",
            "digest_line": "Haaland lập cú đúp đưa Na Uy vào tứ kết Nations League để chạm mốc 399 bàn, nơi Tây Ban Nha tái ngộ Pháp của Zidane.",
        },
        {
            "id": 12,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_12_1.jpg",
            "title": "Yamal & Mbappé cùng hỏng 11m, Barca và Real ngược dòng thắng",
            "digest_line": "Dù Lamine Yamal và Kylian Mbappé cùng hỏng phạt đền, Barcelona vẫn hạ Villarreal 3-2 còn Real Madrid thắng Celta Vigo 2-1 tại La Liga.",
        },
        {
            "id": 13,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_13_1.jpg",
            "title": "Kane & Doué chấn thương dài hạn; Atalanta hòa Inter Milan 4-4",
            "digest_line": "Bayern mất Harry Kane từ hai đến bốn tháng và PSG mất Doué hết mùa, trong khi Atalanta cầm hòa Inter Milan 4-4 phút bù giờ.",
        },
        {
            "id": 14,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_14_1.jpg",
            "title": "Messi dọa kiện AFA, Inter Miami thua 0-3; Ronaldo chạm 986 bàn",
            "digest_line": "Messi dẫn đầu lương MLS 28,33 triệu USD nhưng Inter Miami thua 0-3; Ronaldo ghi bàn thứ 986 trước khi sút hỏng phạt đền.",
        },
        {
            "id": 15,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_15_1.jpg",
            "title": "UEFA cử Diallo tranh ghế FIFA; thủ môn Beiranvand hay nhất châu Á",
            "digest_line": "UEFA chọn Philippe Diallo đối đầu Infantino tranh ghế FIFA, Hàn Quốc nguy cơ bị cấm, còn thủ môn Beiranvand hay nhất châu Á.",
        },
        {
            "id": 16,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_16_1.jpg",
            "title": "Jepchirchir bị cấm 3 năm vì EPO; Mudryk tố cáo Ukraine",
            "digest_line": "ĐKVĐ marathon Olympic Jepchirchir bị cấm ba năm vì EPO, Mudryk tố Ukraine cấp chất cấm và thể thao Indonesia rúng động bốn ca tử vong.",
        },
        {
            "id": 17,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_17_1.jpg",
            "title": "Carlos Alcaraz đánh bại Zverev 6-2, 7-6 lần đầu vô địch ATP Finals",
            "digest_line": "Cứu ba set-point ở tie-break set hai, Carlos Alcaraz đánh bại số một thế giới Zverev 6-2, 7-6 để lần đầu vô địch ATP Finals.",
        },
        {
            "id": 18,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_18_1.jpg",
            "title": "F1 Las Vegas: Verstappen thắng chặng; Márquez 8 lần vô địch MotoGP",
            "digest_line": "Max Verstappen thắng F1 Las Vegas có 35 lần đổi ngôi đầu khi Ferrari tông nhau; Marc Márquez san bằng tám lần vô địch MotoGP.",
        },
        {
            "id": 19,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_19_1.jpg",
            "title": "Thitikul lập kỷ lục LPGA; Skubal ký hợp đồng 450 triệu USD MLB",
            "digest_line": "Golfer Thitikul lập kỷ lục tiền thưởng LPGA, tay ném Skubal ký hợp đồng 450 triệu USD tại MLB và Stirling hạ knock-out Procházka.",
        },
        {
            "id": 20,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_20_1.jpg",
            "title": "Paredes ngất xỉu khi phỏng vấn, Neymar thắng poker & WC nữ 2035",
            "digest_line": "Paredes ổn định sau sự cố ngất khi phỏng vấn, Neymar thắng poker hơn 63000 USD và Anh sắp đăng cai World Cup nữ 2035.",
        },
    ],
}


def validate_specs(cfg: dict) -> None:
    items = cfg["items"]
    intros = [x for x in items if x.get("is_intro")]
    news = [x for x in items if not x.get("is_intro")]
    assert len(intros) == 1, f"Expected 1 intro, got {len(intros)}"
    assert len(news) == 20, f"Expected 20 news items, got {len(news)}"

    total_words = 0
    seen_imgs = set()

    full_seo = f"{cfg['seo_title']} | Điểm Đọc #Shorts"
    assert len(full_seo) <= 100, f"SEO title too long ({len(full_seo)}): {full_seo}"

    t_img = IMAGES_DIR / cfg["thumb"]["image"]
    assert t_img.exists(), f"Missing thumb image: {t_img}"

    for idx, it in enumerate(items, 1):
        img_p = IMAGES_DIR / it["image_file"]
        assert img_p.exists(), f"Missing image {img_p}"
        for ex_fn in (it.get("extra_images") or []):
            ex_p = IMAGES_DIR / ex_fn
            assert ex_p.exists(), f"Missing extra image {ex_p}"
        if not it.get("is_intro"):
            assert it["image_file"] not in seen_imgs, f"Duplicate image in digest news: {it['image_file']}"
            seen_imgs.add(it["image_file"])
        line = it["digest_line"]
        if re.search(r"\d\.\d{3}", line):
            raise AssertionError(f"Item {idx} has dot in thousand number: {line}")
        wc = len(line.split())
        total_words += wc
        tag = "INTRO" if it.get("is_intro") else f"{int(it['id']):02d}"
        print(f"  [{tag:5s}] ({it['voice_gender']:3s}) {wc:2d}w | {it['image_file']:12s} | {line}")

    est_body = total_words / 4.2 + (len(items) - 1) * 0.19
    print(f"\nTổng số từ: {total_words} từ | Ước lượng body: ~{est_body:.1f}s (+Outro ~6.5s = ~{est_body+6.5:.1f}s < 180s)")
    print(f"SEO Title ({len(full_seo)} chars): {full_seo}")


def main() -> None:
    validate_specs(DIGEST_SPECS)
    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    SPEC_PATH.write_text(json.dumps(DIGEST_SPECS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] Đã xuất {SPEC_PATH}")


if __name__ == "__main__":
    main()
