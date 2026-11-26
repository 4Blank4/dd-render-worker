# -*- coding: utf-8 -*-
"""
prepare_digest_26_11.py — Sinh cấu hình `outputs/26.11.2026/shorts/digest_specs.json`
cho Video Short Tin Nhanh 25 Tin (9:16, < 180s) ngày 26.11.2026.
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
DAY_STR = "26.11.2026"
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
SHORTS_DIR = DAY_DIR / "shorts"
SPEC_PATH = SHORTS_DIR / "digest_specs.json"


DIGEST_SPECS = {
    "day": DAY_STR,
    "title": "TIN NHANH THỂ THAO 26.11",
    "hide_date_chip": False,
    "out_video_name": "Short_Tin_Nhanh_25_Tin.mp4",
    "gap_ms": 200,
    "seo_title": "Tin nhanh 26/11: MU hòa Sporting 2-2, Bayern thua Lille & U17 Việt Nam đấu Mali",
    "description": [
        "Điểm đọc nhanh 25 tin tức thể thao nóng nhất ngày 26/11/2026 từ U17 World Cup 2026, AFC Champions League, Đại hội Thể thao toàn quốc 2026, UEFA Champions League, Ngoại hạng Anh tới Cờ tướng, NFL, Formula 1, Quyền Anh hạng nặng và Cờ vua Thế giới.",
        "Nổi bật giờ G trận quyết đấu U17 Việt Nam gặp U17 Mali lúc 20h, FIFA đề cử siêu phẩm của Lê Sỹ Bách, Thể Công Viettel dừng bước sớm ở Cúp C2 châu Á, Nguyễn Thùy Linh lập hat-trick HCV cầu lông, Võ Thị Mỹ Tiên đạt 6 HCV bơi, Ánh Viên lập kỷ lục quốc gia tiếp sức, Manchester United hòa hỗn loạn Sporting CP 2-2 trong đêm trọng tài bị chỉ trích, Bayern Munich thua sốc Lille 1-2 và Liverpool thắng đậm 3-0.",
    ],
    "fb_hook": "🔥 25 TIN THỂ THAO NÓNG NHẤT 26/11 TRONG CHƯA ĐẦY 3 PHÚT!",
    "tiktok_caption": "Điểm nhanh 25 tin nóng thể thao 26/11: MU hòa hỗn loạn Sporting CP 2-2 và rơi hạng 19, Bayern Munich nhận thất bại đầu mùa trước Lille 1-2, U17 Việt Nam quyết đấu U17 Mali lúc 20h tối nay và Nguyễn Thùy Linh lập hat-trick HCV cầu lông Đại hội!",
    "sources_line": "📰 Nguồn tin: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian.",
    "hashtags": [
        "#Shorts",
        "#TinNhanh",
        "#DiemDoc",
        "#DiemDocTheThao",
        "#ManUtd",
        "#ChampionsLeague",
        "#BayernMunich",
        "#U17VietNam",
        "#DaiHoiTheThaoToanQuoc2026",
        "#ThuyLinh",
    ],
    "thumb": {
        "style": "clash_diagonal",
        "image": "Tin_11_1.jpg",
        "bottom_image": "Tin_13_1.jpg",
        "kicker": "25 TIN NHANH THỂ THAO 26.11",
        "hero_html": '<span class="hl-cyan">25 TIN NHANH!</span><br><span class="hl-white">MU HÒA SPORTING 2-2</span><br><span class="hl-yellow">BAYERN THUA LILLE 1-2!</span>',
        "line1": "MU HÒA SPORTING 2-2",
        "line2": "BAYERN THUA LILLE 1-2",
        "subtitle": "U17 VN ĐẤU MALI • THÙY LINH HAT-TRICK • RONALDO",
        "badge": "25 TIN NHANH",
        "tag_a": "VN & QUỐC TẾ",
        "tag_b": "26.11.2026",
        "hero_size": "72",
        "obj_pos": "center 20%",
        "top_pos": "center 20%",
        "bot_pos": "center 18%",
    },
    "items": [
        {
            "id": 1,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_01_1.jpg",
            "title": "U17 Việt Nam quyết đấu U17 Mali lúc 20h giành vé vòng 32 đội",
            "digest_line": "Lúc 20 giờ tối nay, U17 Việt Nam chạm trán U17 Mali với mục tiêu giành trọn ba điểm để chắc suất vào vòng 32 đội.",
        },
        {
            "id": 2,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_02_1.jpg",
            "title": "U17 Mali cảnh giác Việt Nam, trọng tài vua thẻ châu Âu bắt chính",
            "digest_line": "Huấn luyện viên U17 Mali đánh giá cao Việt Nam, trong khi FIFA cử trọng tài Elchin Masiyev cầm còi trận đấu.",
        },
        {
            "id": 3,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_03_1.jpg",
            "title": "FIFA đề cử siêu phẩm của Lê Sỹ Bách là bàn đẹp nhất giải",
            "digest_line": "FIFA đưa cú vô lê đánh gót của tiền đạo Lê Sỹ Bách vào lưới Bỉ vào đề cử bàn thắng đẹp nhất giải.",
        },
        {
            "id": 4,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_04_1.jpg",
            "title": "Thể Công Viettel hòa Melbourne 0-0, bị loại sớm Cúp C2 châu Á",
            "digest_line": "Hòa Melbourne Victory 0-0 chiều qua, Thể Công Viettel dừng bước sớm ở Cúp C2 châu Á với 12 trận không thắng.",
        },
        {
            "id": 5,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_05_1.jpg",
            "title": "Buriram sa thải HLV lần 3 sau 81 ngày, CAHN bỏ xa Thái Lan",
            "digest_line": "Buriram United sa thải huấn luyện viên thứ ba trong 81 ngày, còn Công an Hà Nội bỏ xa cả ba đội Thái Lan.",
        },
        {
            "id": 6,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_06_1.jpg",
            "title": "Nguyễn Thùy Linh thắng Vũ Thị Trang 2-0 lập hat-trick HCV",
            "digest_line": "Nguyễn Thùy Linh đánh bại Vũ Thị Trang 2-0 để hoàn tất cú hat-trick huy chương vàng cầu lông ba kỳ Đại hội.",
        },
        {
            "id": 7,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_07_1.jpg",
            "title": "Võ Thị Mỹ Tiên chạm mốc sáu huy chương vàng bơi Đại hội",
            "digest_line": "Kình ngư Tây Ninh Võ Thị Mỹ Tiên giành thêm cú đúp 400 mét hỗn hợp và 800 mét tự do để đạt sáu vàng.",
        },
        {
            "id": 8,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_08_1.jpg",
            "title": "Ánh Viên giành HCV thứ năm và phá kỷ lục quốc gia tiếp sức",
            "digest_line": "Ánh Viên thắng 50 mét ngửa hơn đối thủ 0,03 giây và cùng đội Quân Đội phá kỷ lục quốc gia tiếp sức.",
        },
        {
            "id": 9,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_09_1.jpg",
            "title": "Phạm Quang Huy thắng loạt bắn thêm nghẹt thở, đoạt HCV thứ hai",
            "digest_line": "Xạ thủ Phạm Quang Huy vượt qua Trần Công Hiếu 2-1 ở loạt bắn thêm để giành tấm huy chương vàng thứ hai.",
        },
        {
            "id": 10,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_10_1.jpg",
            "title": "Chị em Châu Tuyết Vân cùng có huy chương, TP. HCM dẫn đầu 74 HCV",
            "digest_line": "Chị em Châu Tuyết Vân mang vàng bạc taekwondo về cho Thành phố Hồ Chí Minh, vững ngôi đầu với 74 huy chương vàng.",
        },
        {
            "id": 11,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_11_1.jpg",
            "title": "Manchester United hòa hỗn loạn Sporting CP 2-2 tại Lisbon",
            "digest_line": "Bruno Fernandes lập cú đúp trong hai phút nhưng sai lầm của thủ môn Lammens khiến Man United hòa Sporting CP 2-2.",
        },
        {
            "id": 12,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_12_1.jpg",
            "title": "Trọng tài Marciniak bị tố xử ép, MU rơi hạng 19 hai đấu trường",
            "digest_line": "Trọng tài Szymon Marciniak bị chỉ trích khi hủy hai bàn của Quỷ đỏ, đẩy thầy trò Pochettino đứng hạng 19.",
        },
        {
            "id": 13,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_13_1.jpg",
            "title": "Địa chấn tại Pháp: Bayern Munich thua ngược Lille 1-2",
            "digest_line": "Lille của huấn luyện viên Davide Ancelotti đánh bại Bayern Munich 2-1, chấm dứt mạch bất bại từ đầu mùa.",
        },
        {
            "id": 14,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_14_1.jpg",
            "title": "Liverpool thắng đậm Club Brugge 3-0 sau 48 năm tái ngộ",
            "digest_line": "Cú đúp của Alexander Isak cùng pha lập công của Florian Wirtz giúp Liverpool đè bẹp Club Brugge 3-0.",
        },
        {
            "id": 15,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_15_1.jpg",
            "title": "Barcelona thắng Sabah 4-1 sau chuyến đi kỷ lục 3970 km",
            "digest_line": "Vượt chặng bay kỷ lục 3970 ki-lô-mét tới Baku khi thiếu Lamine Yamal, Barcelona vẫn dễ dàng thắng Sabah 4-1.",
        },
        {
            "id": 16,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_16_1.jpg",
            "title": "PSG lần đầu mất điểm khi bị AS Roma cầm hòa 2-2 tại Paris",
            "digest_line": "Cú đá phạt đền phút 78 của Donyell Malen giúp AS Roma cầm hòa 2-2 ngay trên sân nhà đương kim vô địch PSG.",
        },
        {
            "id": 17,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_17_1.jpg",
            "title": "Ronaldo đối mặt án treo giò 4 trận vì nhại trọng tài",
            "digest_line": "Cristiano Ronaldo có thể bị AFC treo giò ít nhất bốn trận vì cử chỉ che mắt chế nhạo trọng tài biên.",
        },
        {
            "id": 18,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_18_1.jpg",
            "title": "Cơ quan quản lý Anh sẵn sàng điều tra và ép đổi chủ Man City",
            "digest_line": "Cơ quan quản lý độc lập Anh khẳng định có quyền buộc chủ sở hữu Man City bán đội bóng nếu thua kháng cáo.",
        },
        {
            "id": 19,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_19_1.jpg",
            "title": "Quỹ đầu tư Saudi Arabia rao bán 25% cổ phần Newcastle United",
            "digest_line": "Quỹ đầu tư công Saudi Arabia thuê JP Morgan phát hành và bán tới 25% cổ phần Newcastle để đầu tư sân mới.",
        },
        {
            "id": 20,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_20_1.jpg",
            "title": "Raheem Sterling nhận án 12 tháng tù treo vì dùng bóng cười",
            "digest_line": "Cựu tuyển thủ Anh Raheem Sterling nhận án 12 tháng tù treo và bị cấm lái xe hai năm do dùng khí cười.",
        },
        {
            "id": 21,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_21_1.jpg",
            "title": "Kỳ thủ xe lăn Triệu Phàn Vĩ quật ngã nhà vô địch thế giới Mạnh Thần",
            "digest_line": "Kỳ thủ xe lăn Triệu Phàn Vĩ hạ nhà vô địch thế giới Mạnh Thần ở ván cờ chớp để vào tứ kết Trung Quốc.",
        },
        {
            "id": 22,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_22_1.jpg",
            "title": "Steelers sa thải Aaron Rodgers sau khi tố HLV ngủ gật",
            "digest_line": "Pittsburgh Steelers cắt hợp đồng với Aaron Rodgers vài giờ sau khi anh tố huấn luyện viên ngủ gật trong buổi họp.",
        },
        {
            "id": 23,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_23_1.jpg",
            "title": "Williams F1 bị FIA phạt vì vượt trần ngân sách 627000 bảng",
            "digest_line": "Đội đua Williams bị FIA phạt tiền và cắt 1,5% thời gian thử nghiệm hầm gió vì vượt trần ngân sách năm 2025.",
        },
        {
            "id": 24,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_24_1.jpg",
            "title": "Chốt đại chiến hạng nặng Daniel Dubois vs Joseph Parker",
            "digest_line": "Nhà vô địch WBO Daniel Dubois sẽ thượng đài bảo vệ đai trước Joseph Parker tại Manchester vào cuối tháng một năm 2027.",
        },
        {
            "id": 25,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_25_1.jpg",
            "title": "Chung kết Cờ vua Thế giới: Gukesh hòa Sindarov sau 20 nước",
            "digest_line": "Đương kim vô địch Gukesh và Javokhir Sindarov bắt tay hòa chóng vánh chỉ sau 20 nước ván hai, cân bằng 1-1.",
        },
    ],
}


def validate_specs(cfg: dict) -> None:
    items = cfg["items"]
    assert len(items) == 25, f"Expected 25 items, got {len(items)}"
    total_words = 0
    seen_imgs = set()

    full_seo = f"{cfg['seo_title']} | Điểm Đọc #Shorts"
    if len(full_seo) > 100:
        raise AssertionError(f"SEO title too long ({len(full_seo)}): {full_seo}")

    t_img = IMAGES_DIR / cfg["thumb"]["image"]
    assert t_img.exists(), f"Missing thumb image: {t_img}"
    if cfg["thumb"].get("bottom_image"):
        b_img = IMAGES_DIR / cfg["thumb"]["bottom_image"]
        assert b_img.exists(), f"Missing bottom thumb image: {b_img}"

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

    est_body = total_words / 3.85 + (len(items) - 1) * (cfg["gap_ms"] / 1000.0)
    print(f"\nTổng số từ: {total_words} từ | Ước lượng body: ~{est_body:.1f}s (+Outro ~6.5s = ~{est_body+6.5:.1f}s < 180s)")
    print(f"SEO Title ({len(full_seo)} chars): {full_seo}")


def main() -> None:
    validate_specs(DIGEST_SPECS)
    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    SPEC_PATH.write_text(json.dumps(DIGEST_SPECS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] Đã xuất {SPEC_PATH}")


if __name__ == "__main__":
    main()
