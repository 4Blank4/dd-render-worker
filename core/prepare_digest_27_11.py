# -*- coding: utf-8 -*-
"""
prepare_digest_27_11.py — Sinh cấu hình `outputs/27.11.2026/shorts/digest_specs.json`
cho Video Short Tin Nhanh 21 Tin (9:16, < 180s) ngày 27.11.2026.
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
sys.path.insert(0, str(ROOT / "core"))

DAY_STR = "27.11.2026"
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
SHORTS_DIR = DAY_DIR / "shorts"
SPEC_PATH = SHORTS_DIR / "digest_specs.json"


DIGEST_SPECS = {
    "day": DAY_STR,
    "title": "TIN NHANH THỂ THAO 27.11",
    "hide_date_chip": False,
    "out_video_name": "Short_Tin_Nhanh_21_Tin.mp4",
    "gap_ms": 200,
    "seo_title": "Tin nhanh 27/11: U17 Việt Nam thua Mali 0-2, Mỹ Tiên 8 HCV & Sinner mổ gối",
    "description": [
        "Điểm đọc nhanh 21 tin tức thể thao nóng nhất ngày 27/11/2026 từ U17 World Cup 2026, Đội tuyển Việt Nam, V-League 2026-2027, Đại hội Thể thao toàn quốc 2026, Billiards PBA Tour, Cúp C2 châu Á, UEFA Europa League tới Ngoại hạng Anh, Quần vợt, Cờ vua Thế giới, Formula 1 và NFL.",
        "Nổi bật hành trình U17 Việt Nam dừng bước trước U17 Mali 0-2 nhưng lập cột mốc năm bàn tại World Cup, nguyện vọng chia tay đội tuyển của đội trưởng Nguyễn Quang Hải, đại chiến nhóm đầu V-League chiều nay, kình ngư Võ Thị Mỹ Tiên lần hai thắng Ánh Viên để chạm mốc tám HCV, cơ thủ Mã Minh Cẩm ngược dòng tại Hàn Quốc, AC Milan thắng Olympiacos 4-2 và cú sốc Jannik Sinner lỡ hẹn Australian Open 2027.",
    ],
    "fb_hook": "🔥 21 TIN THỂ THAO NÓNG NHẤT 27/11 TRONG HƠN 2 PHÚT!",
    "tiktok_caption": "Điểm nhanh 21 tin nóng thể thao 27/11: U17 Việt Nam khép lại hành trình lịch sử ở World Cup, Võ Thị Mỹ Tiên chạm mốc 8 HCV bơi Đại hội, Quang Hải muốn rời tuyển Việt Nam, AC Milan ngược dòng 4-2 ở Europa League và Jannik Sinner lỡ hẹn Australian Open 2027!",
    "sources_line": "📰 Nguồn tin: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian.",
    "hashtags": [
        "#Shorts",
        "#TinNhanh",
        "#DiemDoc",
        "#DiemDocTheThao",
        "#U17VietNam",
        "#U17WorldCup",
        "#DaiHoiTheThaoToanQuoc2026",
        "#VoThiMyTien",
        "#ACMilan",
        "#JannikSinner",
    ],
    "thumb": {
        "style": "cyber_split",
        "image": "Tin_01_1.jpg",
        "kicker": "21 TIN NHANH THỂ THAO 27.11",
        "hero_html": '<span class="hl-cyan">21 TIN NHANH!</span><br><span class="hl-white">U17 VN RỜI WORLD CUP</span><br><span class="hl-yellow">MỸ TIÊN ĐẠT 8 HCV!</span>',
        "subtitle": "QUANG HẢI MUỐN RỜI TUYỂN • AC MILAN 4-2 • SINNER MỔ GỐI",
        "badge": "21 TIN NHANH",
        "tag_a": "VN & QUỐC TẾ",
        "tag_b": "27.11.2026",
        "hero_size": "70",
        "obj_pos": "48% 18%",
    },
    "items": [
        {
            "id": 1,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_01_1.jpg",
            "title": "U17 Việt Nam thua U17 Mali 0-2, dừng bước tại U17 World Cup",
            "digest_line": "Thất bại 0-2 trước U17 Mali ở lượt cuối bảng G khiến U17 Việt Nam khép lại U17 World Cup với một điểm.",
        },
        {
            "id": 2,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_02_1.jpg",
            "title": "U17 Việt Nam lập cột mốc 5 bàn, HLV Roland rơi nước mắt",
            "digest_line": "Dù bị loại, U17 Việt Nam vẫn ghi năm bàn lịch sử, khiến huấn luyện viên Cristiano Roland rơi nước mắt tri ân.",
        },
        {
            "id": 4,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_04_1.jpg",
            "title": "Quang Hải muốn rời tuyển Việt Nam, HLV Kim Sang Sik chưa đồng ý",
            "digest_line": "Đội trưởng Quang Hải có nguyện vọng chia tay đội tuyển Việt Nam, nhưng huấn luyện viên Kim Sang Sik chưa đồng ý.",
        },
        {
            "id": 5,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_05_1.jpg",
            "title": "Đại chiến V-League chiều nay: Nam Định đấu CAHN, SLNA tiếp Ninh Bình",
            "digest_line": "Lúc 18 giờ chiều nay, Nam Định đại chiến Công an Hà Nội còn Sông Lam Nghệ An tiếp đón Ninh Bình ở vòng chín.",
        },
        {
            "id": 6,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_06_3.jpg",
            "title": "Kình ngư Mỹ Tiên lần hai thắng Ánh Viên, chạm mốc 8 HCV",
            "digest_line": "Kình ngư Võ Thị Mỹ Tiên vượt Ánh Viên phá kỷ lục 200 mét tự do và chạm mốc tám huy chương vàng Đại hội.",
        },
        {
            "id": 7,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_07_1.jpg",
            "title": "Lại Lý Huynh - Nhật Quang vô địch cờ tướng, TP. HCM đạt 86 HCV",
            "digest_line": "Lại Lý Huynh cùng Nhật Quang thắng siêu kinh điển cờ tướng, giúp Thành phố Hồ Chí Minh dẫn đầu với 86 huy chương vàng.",
        },
        {
            "id": 8,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_08_1.jpg",
            "title": "Mã Minh Cẩm cứu match-point, hạ cựu số 1 thế giới ở PBA Tour",
            "digest_line": "Tại giải billiards PBA Tour Hàn Quốc, cơ thủ Mã Minh Cẩm cứu thua kịch tính để ngược dòng hạ cựu số một thế giới.",
        },
        {
            "id": 3,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_03_1.jpg",
            "title": "U17 Trung Quốc thắng Fiji 8-0 giành vé vớt vòng 32 đội",
            "digest_line": "Chiến thắng đậm 8-0 trước Fiji giúp U17 Trung Quốc giành vé vớt cùng năm đại diện châu Á dự vòng 32 đội World Cup.",
        },
        {
            "id": 9,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_09_1.jpg",
            "title": "Địa chấn Cúp C2 châu Á: Svay Rieng hạ Machida Zelvia 2-0",
            "digest_line": "Câu lạc bộ Svay Rieng của Campuchia gây chấn động Cúp C2 châu Á khi cắt đứt mạch 15 trận bất bại của Machida Zelvia.",
        },
        {
            "id": 10,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_10_1.jpg",
            "title": "Bournemouth mất người vẫn thắng Celta Vigo 2-1 ở Europa League",
            "digest_line": "Dù mất người từ phút 23, Bournemouth vẫn thắng ngược Celta Vigo 2-1 để độc chiếm ngôi đầu Europa League.",
        },
        {
            "id": 11,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_11_1.jpg",
            "title": "AC Milan ngược dòng thắng Olympiacos 4-2, Juventus đại thắng 4-1",
            "digest_line": "Rạng sáng nay ở Europa League, AC Milan ngược dòng hạ Olympiacos 4-2, còn Juventus đè bẹp Omonia Nicosia 4-1.",
        },
        {
            "id": 12,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_12_1.jpg",
            "title": "Thomas Frank thắng trận đầu cùng Palace, Celtic thoát hiểm phút 85",
            "digest_line": "Huấn luyện viên Thomas Frank có thắng lợi đầu tay giúp Crystal Palace hạ Real Sociedad 2-1 tại Europa League.",
        },
        {
            "id": 13,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_13_1.jpg",
            "title": "Thủ môn Lammens gây lo ngại, Pochettino siết kỷ luật Man Utd",
            "digest_line": "Trước chuỗi sai lầm của thủ thành Senne Lammens, huấn luyện viên Pochettino đã áp dụng năm điều chỉnh mạnh tay tại Man United.",
        },
        {
            "id": 14,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_14_1.jpg",
            "title": "Bốn ông lớn Ngoại hạng Anh chuẩn bị kiện đòi bồi thường Man City",
            "digest_line": "Man United, Liverpool, Tottenham và Arsenal đã thuê hãng luật chuẩn bị hồ sơ kiện đòi Manchester City bồi thường hàng trăm triệu bảng.",
        },
        {
            "id": 15,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_15_1.jpg",
            "title": "Xabi Alonso xác nhận Wesley Fofana xin lỗi nội bộ Chelsea",
            "digest_line": "Huấn luyện viên Xabi Alonso xác nhận trung vệ Wesley Fofana đã xin lỗi sau cuộc phỏng vấn gây sóng gió ở Chelsea.",
        },
        {
            "id": 16,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_16_1.jpg",
            "title": "Trọng tài AFC Champions League Two bác bỏ cáo buộc say xỉn",
            "digest_line": "Trọng tài Syria Hanna Hattab dọa khởi kiện sau khi bị thay giữa hiệp và dính tin đồn thất thiệt tại Cúp C2 châu Á.",
        },
        {
            "id": 17,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_17_2.jpg",
            "title": "Jannik Sinner phẫu thuật đầu gối, lỡ hẹn Australian Open 2027",
            "digest_line": "Tay vợt số hai thế giới Jannik Sinner phải phẫu thuật đầu gối tại Phần Lan và bỏ lỡ Australian Open 2027.",
        },
        {
            "id": 18,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_18_3.jpg",
            "title": "Davis Cup 2026: Tuyển Anh thắng Đức 2-1, vào bán kết sau 7 năm",
            "digest_line": "Cặp đôi Henry Patten và Neal Skupski thắng quyết định giúp tuyển Anh hạ Đức 2-1, vào bán kết Davis Cup sau bảy năm.",
        },
        {
            "id": 19,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_19_1.jpg",
            "title": "Chung kết Cờ vua Thế giới: Sindarov thoát hiểm hòa Gukesh",
            "digest_line": "Javokhir Sindarov thoát thua ngoạn mục ở những giây cuối để hòa Gukesh sau gần năm giờ ván ba giải cờ vua thế giới.",
        },
        {
            "id": 20,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_20_2.jpg",
            "title": "Nội bộ Ferrari sóng gió trước Qatar GP: Hamilton cảnh báo thử thách",
            "digest_line": "Trước chặng đua Qatar cuối tuần này, Lewis Hamilton thừa nhận Ferrari đang đối diện giai đoạn căng thẳng với Charles Leclerc.",
        },
        {
            "id": 21,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_21_1.jpg",
            "title": "NFL Lễ Tạ Ơn: Chicago Bears ngược dòng hạ Detroit Lions ở 3 giây cuối",
            "digest_line": "Chicago Bears hoàn tất màn ngược dòng không tưởng hạ Detroit Lions 39-35 đúng ba giây cuối trận đấu Lễ Tạ Ơn giải NFL.",
        },
    ],
}


def validate_specs(cfg: dict) -> None:
    from diemdoc.tts_text import prepare

    items = cfg["items"]
    assert len(items) == 21, f"Expected 21 items, got {len(items)}"
    total_words = 0
    seen_imgs = set()
    seen_ids = set()

    full_seo = f"{cfg['seo_title']} | Điểm Đọc #Shorts"
    if len(full_seo) > 100:
        raise AssertionError(f"SEO title too long ({len(full_seo)}): {full_seo}")

    t_img = IMAGES_DIR / cfg["thumb"]["image"]
    assert t_img.exists(), f"Missing thumb image: {t_img}"

    for idx, it in enumerate(items, 1):
        assert it["id"] not in seen_ids, f"Duplicate ID: {it['id']}"
        seen_ids.add(it["id"])
        img_p = IMAGES_DIR / it["image_file"]
        assert img_p.exists(), f"Missing image {img_p}"
        assert it["image_file"] not in seen_imgs, f"Duplicate image in digest: {it['image_file']}"
        seen_imgs.add(it["image_file"])
        line = it["digest_line"]
        if re.search(r"\d\.\d{3}", line):
            raise AssertionError(f"Item {idx} has dot in thousand number: {line}")
        tts_str, _ = prepare(line)
        wc = len(line.split())
        total_words += wc
        print(f"  [{idx:02d}] (#{it['id']:02d} {it['voice_gender']:3s}) {wc:2d}w | {it['image_file']:12s} | {line}")

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
