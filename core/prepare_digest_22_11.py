# -*- coding: utf-8 -*-
"""
prepare_digest_22_11.py — Sinh cấu hình `outputs/22.11.2026/shorts/digest_specs.json`
cho Video Short Tin Nhanh 22 Tin (9:16, < 180s) ngày 22.11.2026.
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
DAY_STR = "22.11.2026"
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
SHORTS_DIR = DAY_DIR / "shorts"
SPEC_PATH = SHORTS_DIR / "digest_specs.json"


DIGEST_SPECS = {
    "day": DAY_STR,
    "title": "TIN NHANH THỂ THAO 22.11",
    "hide_date_chip": False,
    "out_video_name": "Short_Tin_Nhanh_22_Tin.mp4",
    "gap_ms": 220,
    "seo_title": "Tin nhanh 22/11: Khai mạc Đại hội toàn quốc, hủy bàn Haaland & Chelsea thua 1-4",
    "description": [
        "Điểm đọc nhanh 22 tin tức thể thao nóng nhất ngày 22/11/2026 từ Đại hội Thể thao toàn quốc 2026, V-League, Ngoại hạng Anh tới La Liga, MLS và UFC.",
        "Nổi bật lễ khai mạc Đại hội Thể thao toàn quốc lần thứ X bên sông Sài Gòn, Nam Định giữ vững ngôi đầu V-League, VAR hủy bàn Haaland khiến Man City hòa Fulham 1-1, Chelsea thảm bại 1-4 trước Leeds, Real Madrid ngược dòng hạ Celta Vigo và cú sốc tại UFC Qatar.",
    ],
    "fb_hook": "🔥 22 TIN THỂ THAO NÓNG NHẤT 22/11 TRONG CHƯA ĐẦY 3 PHÚT!",
    "tiktok_caption": "Điểm nhanh 22 tin nóng thể thao 22/11: Đại hội Thể thao toàn quốc khai mạc rực rỡ, VAR hủy bàn Haaland, Chelsea thảm bại 1-4, Real Madrid ngược dòng và Inter Miami thua sốc 0-3!",
    "sources_line": "📰 Nguồn tin: Thanh Niên, Tuổi Trẻ, VnExpress, Dân Trí, BBC Sport, ESPN, Sky Sports, The Guardian.",
    "hashtags": [
        "#Shorts",
        "#TinNhanh",
        "#DiemDoc",
        "#DiemDocTheThao",
        "#DaiHoiTheThaoToanQuoc",
        "#NgoaiHangAnh",
        "#ManCity",
        "#Chelsea",
        "#RealMadrid",
        "#LionelMessi",
    ],
    "thumb": {
        "image": "Tin_10_1.jpg",
        "kicker": "ĐIỂM NHANH 22 TIN THỂ THAO 22.11",
        "hero_html": '<span class="hl-cyan">22 TIN NHANH!</span><br><span class="hl-white">HỦY BÀN HAALAND</span><br><span class="hl-yellow">CHELSEA THUA 1-4!</span>',
        "subtitle": "ĐẠI HỘI 2026 • NGOẠI HẠNG ANH • REAL MADRID • MLS • UFC",
        "badge": "22 TIN NHANH",
        "tag_a": "VN & QUỐC TẾ",
        "tag_b": "22.11.2026",
        "hero_size": "76",
        "obj_pos": "center 22%",
    },
    "items": [
        {
            "id": 1,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_01_1.jpg",
            "title": "Đại hội Thể thao toàn quốc 2026 khai mạc bên sông Sài Gòn",
            "digest_line": "Đại hội Thể thao toàn quốc 2026 khai mạc rực rỡ bên sông Sài Gòn, đoàn Thành phố Hồ Chí Minh tạm dẫn đầu 40 huy chương vàng.",
        },
        {
            "id": 2,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_02_1.jpg",
            "title": "Kình ngư đội tuyển Mỹ Watson Nguyễn so tài Phạm Thanh Bảo",
            "digest_line": "Tài năng Việt kiều Watson Nguyễn sẽ so tài cùng Phạm Thanh Bảo tại đường đua bơi Đại hội từ ngày 22 đến 27 tháng 11.",
        },
        {
            "id": 3,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_03_1.jpg",
            "title": "Esports lần đầu tranh huy chương ở Đại hội Toàn quốc",
            "digest_line": "Thể thao điện tử lần đầu chính thức tranh huy chương ở Đại hội Toàn quốc với ba bộ môn Liên Quân, Free Fire và Audition.",
        },
        {
            "id": 4,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_04_1.jpg",
            "title": "V-League: Nam Định thắng Hải Phòng 2-1, Hà Nội hạ Đồng Nai",
            "digest_line": "Nam Định thắng Hải Phòng 2-1 giữ ngôi đầu V-League với 19 điểm, còn Hà Nội FC ngược dòng thắng Đồng Nai 3-1.",
        },
        {
            "id": 5,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_05_1.jpg",
            "title": "Tân HLV Lee Young-jin ra mắt CLB Đà Nẵng gặp Ninh Bình",
            "digest_line": "Chiều tối 22 tháng 11, tân huấn luyện viên Lee Young-jin ra mắt Đà Nẵng trong cuộc tiếp đón Ninh Bình tại sân Chi Lăng.",
        },
        {
            "id": 6,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_06_2.jpg",
            "title": "U17 Việt Nam soi điểm yếu New Zealand trước trận 23/11",
            "digest_line": "Trước lượt trận ngày 23 tháng 11, U17 Việt Nam nghiên cứu kỹ lỗ hổng hàng thủ New Zealand để hướng tới chiến thắng quyết định.",
        },
        {
            "id": 7,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_07_1.jpg",
            "title": "Công an Hà Nội bị AFC phạt 2000 USD tại Nhật Bản",
            "digest_line": "AFC vừa phạt câu lạc bộ Công an Hà Nội 2000 USD do cổ động viên trưng biểu tượng cấm trên sân Gamba Osaka.",
        },
        {
            "id": 8,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_08_1.jpg",
            "title": "Lê Quang Liêm hạ Nepomniachtchi, trở lại Top 15 thế giới",
            "digest_line": "Lê Quang Liêm đánh bại Ian Nepomniachtchi chỉ sau 29 nước đi tại Budapest, qua đó đòi lại vị trí trong Top 15 thế giới.",
        },
        {
            "id": 9,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_09_1.jpg",
            "title": "Duy nhất Indonesia dự đủ 4 vòng chung kết châu Á 2027",
            "digest_line": "Indonesia là đội Đông Nam Á duy nhất giành vé dự cả bốn vòng chung kết châu Á 2027, trong khi Việt Nam và Thái Lan có ba suất.",
        },
        {
            "id": 10,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_10_1.jpg",
            "title": "VAR hủy bàn Haaland, Man City hòa Fulham 1-1 trên sân nhà",
            "digest_line": "VAR gây tranh cãi khi tước bàn thắng của Haaland, khiến Manchester City bị Fulham cầm hòa 1-1 và trải qua bốn trận không thắng.",
        },
        {
            "id": 11,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_11_2.jpg",
            "title": "Chelsea thảm bại 1-4 trước Leeds ngay tại Stamford Bridge",
            "digest_line": "Chelsea thua ngược Leeds 1-4 ngay trên sân nhà, rơi xuống hạng tám và khiến ghế huấn luyện viên Xabi Alonso lung lay dữ dội.",
        },
        {
            "id": 12,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_12_1.jpg",
            "title": "Arsenal hòa Newcastle 2-2 và lo âu chấn thương David Raya",
            "digest_line": "Madueke giúp Arsenal giật lại trận hòa 2-2 trên sân Newcastle, nhưng thủ môn David Raya lại dính chấn thương vai đáng lo.",
        },
        {
            "id": 13,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_13_1.jpg",
            "title": "Sao mai 18 tuổi Tottenham tỏa sáng, Bournemouth thắng 9 trận",
            "digest_line": "Tài năng 18 tuổi Luca Williams-Barnett ghi bàn giúp Tottenham thắng Ipswich 2-0, còn Bournemouth lập kỷ lục chín trận thắng liên tiếp.",
        },
        {
            "id": 14,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_14_1.jpg",
            "title": "Real Madrid ngược dòng thắng Celta Vigo 2-1 ở La Liga",
            "digest_line": "Dù Kylian Mbappé đá hỏng phạt đền, anh vẫn kiến tạo cho Bellingham trước khi Carlos Espi ấn định thắng lợi 2-1 cho Real Madrid.",
        },
        {
            "id": 15,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_15_1.jpg",
            "title": "PSG thắng Nice 3-2 nhưng trả giá với chấn thương của Doué",
            "digest_line": "Ferran Torres ghi bàn phút cuối giúp PSG thắng Nice 3-2, nhưng niềm vui không trọn vẹn vì Désiré Doué chấn thương đầu gối nặng.",
        },
        {
            "id": 16,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_16_2.jpg",
            "title": "AS Roma và Leipzig cùng thắng 5-1, Hearts đại thắng 8-0",
            "digest_line": "AS Roma thắng Parma 5-1 nhờ cú poker của Malen, RB Leipzig đè bẹp Union Berlin 5-1 còn Hearts tại Scotland thắng tới 8-0.",
        },
        {
            "id": 17,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_17_1.jpg",
            "title": "Messi nhận Vua phá lưới MLS nhưng Inter Miami thua 0-3",
            "digest_line": "Dù nhận giải Vua phá lưới MLS 2026, Lionel Messi vẫn bất lực nhìn Inter Miami thua sốc Columbus Crew 0-3 ở lượt đi play-off.",
        },
        {
            "id": 18,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_18_1.jpg",
            "title": "Chung kết trong mơ ATP Finals 2026: Alcaraz gặp Zverev",
            "digest_line": "Tối 22 tháng 11, chung kết ATP Finals 2026 là màn đọ sức nảy lửa giữa Carlos Alcaraz và tay vợt số một Alexander Zverev.",
        },
        {
            "id": 19,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_19_1.jpg",
            "title": "F1 Las Vegas GP: Antonelli mất Pole, Russell khẩu chiến Verstappen",
            "digest_line": "Tân binh Kimi Antonelli nhanh nhất Q3 tại Las Vegas nhưng mất Pole vì án phạt động cơ, nhường vị trí đầu cho Max Verstappen.",
        },
        {
            "id": 20,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_20_1.jpg",
            "title": "UFC Qatar: Stirling hạ knock-out Procházka, Price thống nhất đai",
            "digest_line": "Võ sĩ bất bại Navajo Stirling hạ knock-out cựu vương Procházka ở UFC Qatar, còn Lauren Price trở thành nhà vô địch tuyệt đối Xứ Wales.",
        },
        {
            "id": 21,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_21_1.jpg",
            "title": "NBA: Sixers thắng Bucks 132-129 dù Herro ghi 50 điểm",
            "digest_line": "Sixers thoát thua trước Bucks 132-129 dù Herro ghi 50 điểm, còn Bezzecchi về nhất chặng Sprint mưa gió tại MotoGP Bồ Đào Nha.",
        },
        {
            "id": 22,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_22_1.jpg",
            "title": "Thể thao Indonesia rúng động 4 vận động viên tử vong",
            "digest_line": "Làng thể thao Indonesia chấn động khi liên tiếp bốn vận động viên qua đời trong một tháng, buộc Bộ trưởng Erick Thohir vào cuộc điều tra.",
        },
    ],
}


def validate_specs(cfg: dict) -> None:
    items = cfg["items"]
    assert len(items) == 22, f"Expected 22 items, got {len(items)}"
    total_words = 0
    seen_imgs = set()

    # Check title + suffix <= 100
    full_seo = f"{cfg['seo_title']} | Điểm Đọc #Shorts"
    assert len(full_seo) <= 100, f"SEO title too long ({len(full_seo)}): {full_seo}"

    # Check thumb image
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

    est_body = total_words / 3.6 + (len(items) - 1) * 0.22
    print(f"\nTổng số từ: {total_words} từ | Ước lượng body: ~{est_body:.1f}s (+Outro ~6.5s = ~{est_body+6.5:.1f}s < 180s)")
    print(f"SEO Title ({len(full_seo)} chars): {full_seo}")


def main() -> None:
    validate_specs(DIGEST_SPECS)
    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    SPEC_PATH.write_text(json.dumps(DIGEST_SPECS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] Đã xuất {SPEC_PATH}")


if __name__ == "__main__":
    main()
