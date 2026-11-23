# -*- coding: utf-8 -*-
"""
prepare_digest_23_11.py — Sinh cấu hình `outputs/23.11.2026/shorts/digest_specs.json`
cho Video Short Tin Nhanh 16 Tin (9:16, < 180s) ngày 23.11.2026.
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
DAY_STR = "23.11.2026"
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
SHORTS_DIR = DAY_DIR / "shorts"
SPEC_PATH = SHORTS_DIR / "digest_specs.json"


DIGEST_SPECS = {
    "day": DAY_STR,
    "title": "TIN NHANH THỂ THAO 23.11",
    "hide_date_chip": False,
    "out_video_name": "Short_Tin_Nhanh_16_Tin.mp4",
    "gap_ms": 220,
    "seo_title": "Tin nhanh 23/11: Liverpool thắng MU 4-0, Ánh Viên giành HCB & Alcaraz vô địch",
    "description": [
        "Điểm đọc nhanh 16 tin tức thể thao nóng nhất ngày 23/11/2026 từ Đại hội Thể thao toàn quốc 2026, V-League, Ngoại hạng Anh tới La Liga, Serie A, ATP Finals, F1 và MotoGP.",
        "Nổi bật mưa kỷ lục đường đua bơi với HCB tái xuất của Nguyễn Thị Ánh Viên và Watson Nguyễn phá kỷ lục quốc gia, Hoàng Đức đưa Ninh Bình lên nhì bảng V-League, Liverpool vùi dập Manchester United 4-0, Barcelona thắng ngược Villarreal 3-2, Carlos Alcaraz vô địch ATP Finals và Marc Márquez san bằng kỷ lục tám lần vô địch MotoGP.",
    ],
    "fb_hook": "🔥 16 TIN THỂ THAO NÓNG NHẤT 23/11 TRONG CHƯA ĐẦY 3 PHÚT!",
    "tiktok_caption": "Điểm nhanh 16 tin nóng thể thao 23/11: Liverpool đè bẹp Man Utd 4-0 ở trận ra mắt của Pochettino, Ánh Viên tái xuất giành HCB Đại hội, Carlos Alcaraz vô địch ATP Finals và Marc Márquez cân bằng kỷ lục 8 ngôi vương MotoGP!",
    "sources_line": "📰 Nguồn tin: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, ESPN, Sky Sports, The Guardian.",
    "hashtags": [
        "#Shorts",
        "#TinNhanh",
        "#DiemDoc",
        "#DiemDocTheThao",
        "#Liverpool",
        "#ManUtd",
        "#DaiHoiTheThaoToanQuoc",
        "#AnhVien",
        "#CarlosAlcaraz",
        "#MarcMarquez",
    ],
    "thumb": {
        "image": "Tin_07_1.jpg",
        "kicker": "ĐIỂM NHANH 16 TIN THỂ THAO 23.11",
        "hero_html": '<span class="hl-cyan">16 TIN NHANH!</span><br><span class="hl-white">LIVERPOOL HỦY DIỆT</span><br><span class="hl-yellow">MAN UNITED 4-0!</span>',
        "subtitle": "ĐẠI HỘI 2026 • LA LIGA • SERIE A • F1 • MOTOGP",
        "badge": "16 TIN NHANH",
        "tag_a": "VN & QUỐC TẾ",
        "tag_b": "23.11.2026",
        "hero_size": "76",
        "obj_pos": "center 20%",
    },
    "items": [
        {
            "id": 1,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_01_1.jpg",
            "title": "Ánh Viên giành HCB tái xuất, Watson Nguyễn phá kỷ lục quốc gia",
            "digest_line": "Võ Thị Mỹ Tiên phá kỷ lục Đại hội đánh bại Ánh Viên ở 200 mét hỗn hợp, còn Watson Nguyễn vượt Phạm Thanh Bảo lập kỷ lục quốc gia 50 mét ếch.",
        },
        {
            "id": 2,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_02_1.jpg",
            "title": "TP.HCM chạm mốc 109 huy chương, Hoàng Sao bị loại sốc",
            "digest_line": "Đoàn Thành phố Hồ Chí Minh đạt 41 huy chương vàng dẫn đầu Đại hội, trong khi Hoàng Sao thua ngược 8-9 và Phạm Văn Mách giành huy chương bạc.",
        },
        {
            "id": 3,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_03_1.jpg",
            "title": "V-League Vòng 8: Hoàng Đức ghi bàn, Nhật Minh đi cấp cứu",
            "digest_line": "Hoàng Đức ghi bàn duy nhất giúp Ninh Bình thắng Đà Nẵng 1-0 chiếm ngôi nhì, còn Hà Tĩnh hạ Công an Thành phố Hồ Chí Minh 2-1 khi Nhật Minh phải cấp cứu.",
        },
        {
            "id": 4,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_04_2.jpg",
            "title": "22h30 tối nay: U17 Việt Nam quyết đấu U17 New Zealand",
            "digest_line": "Huấn luyện viên Cristiano Roland rèn kỹ phương án chống bóng bổng trước trận U17 Việt Nam gặp U17 New Zealand lúc 22 giờ 30 tối nay.",
        },
        {
            "id": 5,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_05_1.jpg",
            "title": "Bùi Đình Khải TKO nhà vô địch Muay thế giới Lê Hoàng Đức",
            "digest_line": "Tại Bắc Ninh, võ sĩ Bùi Đình Khải tung loạt đòn chỏ hạ knock-out kỹ thuật nhà vô địch Muay thế giới Lê Hoàng Đức ngay hiệp một giành đai 52 kilôgam.",
        },
        {
            "id": 6,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_06_1.jpg",
            "title": "Lê Quang Liêm dự siêu giải 250000 USD, Minh Vương tái xuất",
            "digest_line": "Lê Quang Liêm bước vào giải cờ nhanh Jerusalem Masters quỹ thưởng 250000 USD, trong khi Trần Minh Vương tái xuất kiến tạo giúp Công an Nhân dân thắng trận.",
        },
        {
            "id": 7,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_07_1.jpg",
            "title": "Liverpool vùi dập Man Utd 4-0, Pochettino lập kỷ lục buồn",
            "digest_line": "Sau thẻ đỏ phút thứ tám của Leny Yoro, Liverpool đè bẹp Manchester United 4-0 đẩy Quỷ đỏ xuống hạng 19 và khiến Pochettino ra mắt tệ nhất 100 năm.",
        },
        {
            "id": 8,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_08_1.jpg",
            "title": "Hull City tạo địa chấn hạ Brighton 2-0 phút bù giờ",
            "digest_line": "Thủ môn Konstantinos Tzolakis cản phá xuất sắc trước khi Oli McBurnie lập cú đúp phút bù giờ giúp Hull City quật ngã 10 người của Brighton 2-0.",
        },
        {
            "id": 9,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_09_1.jpg",
            "title": "Yamal hỏng 11m, Barcelona ngược dòng hạ Villarreal 3-2",
            "digest_line": "Dù Lamine Yamal sút phạt đền dội cột dọc và bị dẫn hai bàn, Barcelona vẫn thắng ngược Villarreal 3-2 để giữ vững ngôi đầu bảng La Liga.",
        },
        {
            "id": 10,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_10_1.jpg",
            "title": "Atalanta hòa Inter 4-4, PSG mất Désiré Doué hết mùa",
            "digest_line": "Esposito lập hat-trick nhưng Inter Milan vẫn bị Atalanta cầm hòa 4-4 ở phút bù giờ, AC Milan thắng 5-1, còn PSG mất Désiré Doué vì đứt dây chằng chéo trước.",
        },
        {
            "id": 11,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_11_1.jpg",
            "title": "U17 Hàn Quốc thắng 6-0, Anh sắp đăng cai World Cup nữ 2035",
            "digest_line": "U17 Hàn Quốc đè bẹp New Caledonia 6-0, Pháp thua sốc Saudi Arabia 0-1, còn Vương quốc Anh chuẩn bị được FIFA trao quyền đăng cai World Cup nữ 2035.",
        },
        {
            "id": 12,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_12_2.jpg",
            "title": "Carlos Alcaraz đánh bại Zverev lần đầu vô địch ATP Finals",
            "digest_line": "Cứu ba set-point ở tie-break set hai, Carlos Alcaraz đánh bại số một thế giới Alexander Zverev 6-2, 7-6 để lần đầu đoạt chức vô địch ATP Finals.",
        },
        {
            "id": 13,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_13_1.jpg",
            "title": "F1 Las Vegas: Verstappen vô địch, Ferrari nội chiến tông nhau",
            "digest_line": "Max Verstappen thắng chặng F1 Las Vegas có 35 lần đổi ngôi đầu, trong khi hai tay đua Ferrari va chạm ở vòng 38 và George Russell đâm rào cuối chặng.",
        },
        {
            "id": 14,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_14_1.jpg",
            "title": "Marc Márquez san bằng kỷ lục tám lần vô địch MotoGP",
            "digest_line": "Cán đích thứ tám tại chặng Bồ Đào Nha trong ngày Bezzecchi về nhất, Marc Márquez chính thức san bằng kỷ lục tám lần vô địch MotoGP của huyền thoại Agostini.",
        },
        {
            "id": 15,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_15_1.jpg",
            "title": "Jeeno Thitikul & Tarik Skubal lập hai kỷ lục tiền thưởng",
            "digest_line": "Golfer Jeeno Thitikul thắng Tour Championship năm thứ ba nhận bốn triệu USD, còn tay ném bóng Tarik Skubal ký hợp đồng kỷ lục 450 triệu USD với Mets.",
        },
        {
            "id": 16,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_16_1.jpg",
            "title": "Paredes ngất xỉu khi phỏng vấn, Neymar thắng giải poker",
            "digest_line": "Tiền vệ Leandro Paredes đổ gục khi phỏng vấn sau cúp Nam Mỹ nhưng đã ổn định, Neymar thắng giải poker hơn 63000 USD và Gerwyn Price vô địch Grand Slam of Darts.",
        },
    ],
}


def validate_specs(cfg: dict) -> None:
    items = cfg["items"]
    assert len(items) == 16, f"Expected 16 items, got {len(items)}"
    total_words = 0
    seen_imgs = set()

    full_seo = f"{cfg['seo_title']} | Điểm Đọc #Shorts"
    assert len(full_seo) <= 100, f"SEO title too long ({len(full_seo)}): {full_seo}"

    t_img = IMAGES_DIR / cfg["thumb"]["image"]
    assert t_img.exists(), f"Missing thumb image: {t_img}"

    for idx, it in enumerate(items, 1):
        img_p = IMAGES_DIR / it["image_file"]
        assert img_p.exists(), f"Missing image {img_p}"
        assert it["image_file"] not in seen_imgs, f"Duplicate image in digest: {it['image_file']}"
        seen_imgs.add(it["image_file"])
        line = it["digest_line"]
        if re.search(r"\d\.\d{3}", line):
            raise AssertionError(f"Item {idx} has dot in thousand number: {line}")
        wc = len(line.split())
        total_words += wc
        print(f"  [{idx:02d}] ({it['voice_gender']:3s}) {wc:2d}w | {it['image_file']:12s} | {line}")

    est_body = total_words / 4.0 + (len(items) - 1) * 0.22
    print(f"\nTổng số từ: {total_words} từ | Ước lượng body: ~{est_body:.1f}s (+Outro ~6.5s = ~{est_body+6.5:.1f}s < 180s)")
    print(f"SEO Title ({len(full_seo)} chars): {full_seo}")


def main() -> None:
    validate_specs(DIGEST_SPECS)
    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    SPEC_PATH.write_text(json.dumps(DIGEST_SPECS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] Đã xuất {SPEC_PATH}")


if __name__ == "__main__":
    main()
