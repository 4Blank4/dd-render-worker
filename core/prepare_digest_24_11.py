# -*- coding: utf-8 -*-
"""
prepare_digest_24_11.py — Sinh cấu hình `outputs/24.11.2026/shorts/digest_specs.json`
cho Video Short Tin Nhanh 27 Tin (9:16, < 180s) ngày 24.11.2026.
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
DAY_STR = "24.11.2026"
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
SHORTS_DIR = DAY_DIR / "shorts"
SPEC_PATH = SHORTS_DIR / "digest_specs.json"


DIGEST_SPECS = {
    "day": DAY_STR,
    "title": "TIN NHANH THỂ THAO 24.11",
    "hide_date_chip": False,
    "out_video_name": "Short_Tin_Nhanh_27_Tin.mp4",
    "gap_ms": 200,
    "seo_title": "Tin nhanh 24/11: U17 Việt Nam hòa 3-3, Ánh Viên giành HCV & Brentford thắng 4-0",
    "description": [
        "Điểm đọc nhanh 27 tin tức thể thao nóng nhất ngày 24/11/2026 từ U17 World Cup 2026, Đại hội Thể thao toàn quốc 2026, Ngoại hạng Anh, Champions League, La Liga tới Quần vợt ATP, Quyền Anh và Bóng bàn thế giới.",
        "Nổi bật màn rượt đuổi tỷ số 3-3 của U17 Việt Nam trước U17 New Zealand với bàn gỡ phút bù giờ của Duy Khang, mưa kỷ lục bơi lội của Nguyễn Thúy Hiền, Nguyễn Thị Ánh Viên và Phạm Thanh Bảo, Brentford đè bẹp Everton 4-0, Manchester United kháng cáo thẻ đỏ Leny Yoro và Jannik Sinner phẫu thuật đầu gối.",
    ],
    "fb_hook": "🔥 27 TIN THỂ THAO NÓNG NHẤT 24/11 TRONG CHƯA ĐẦY 3 PHÚT!",
    "tiktok_caption": "Điểm nhanh 27 tin nóng thể thao 24/11: U17 Việt Nam hòa nghẹt thở U17 New Zealand 3-3 ở World Cup, kình ngư 17 tuổi Thúy Hiền phá 5 kỷ lục, Ánh Viên giành HCV sau 1437 ngày giải nghệ, Brentford thắng Everton 4-0 và MU kháng cáo thẻ đỏ Yoro!",
    "sources_line": "📰 Nguồn tin: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, ESPN, Sky Sports, The Guardian.",
    "hashtags": [
        "#Shorts",
        "#TinNhanh",
        "#DiemDoc",
        "#DiemDocTheThao",
        "#U17VietNam",
        "#DaiHoiTheThaoToanQuoc2026",
        "#AnhVien",
        "#NguyenThuyHien",
        "#ManUtd",
        "#Brentford",
    ],
    "thumb": {
        "image": "Tin_01_1.jpg",
        "kicker": "ĐIỂM NHANH 27 TIN THỂ THAO 24.11",
        "hero_html": '<span class="hl-cyan">27 TIN NHANH!</span><br><span class="hl-white">U17 VIỆT NAM 3-3</span><br><span class="hl-yellow">ÁNH VIÊN GIÀNH HCV!</span>',
        "subtitle": "THÚY HIỀN 5 KỶ LỤC • BRENTFORD 4-0 • MU YORO",
        "badge": "27 TIN NHANH",
        "tag_a": "VN & QUỐC TẾ",
        "tag_b": "24.11.2026",
        "hero_size": "74",
        "obj_pos": "center 20%",
    },
    "items": [
        {
            "id": 1,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_01_1.jpg",
            "title": "U17 Việt Nam hòa nghẹt thở U17 New Zealand 3-3 tại World Cup",
            "digest_line": "Duy Khang ghi bàn phút 90 cộng 2 giúp U17 Việt Nam cầm hòa New Zealand 3-3 tại World Cup.",
        },
        {
            "id": 2,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_02_1.jpg",
            "title": "FIFA ca ngợi U17 Việt Nam, VFF thưởng nóng 400 triệu đồng",
            "digest_line": "FIFA ca ngợi tinh thần quả cảm của U17 Việt Nam và VFF thưởng nóng ngay 400 triệu đồng.",
        },
        {
            "id": 3,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_03_1.jpg",
            "title": "Cục diện bảng G trước đại chiến U17 Việt Nam gặp U17 Mali",
            "digest_line": "Tạm xếp thứ ba bảng G, U17 Việt Nam cần thắng U17 Mali tối 26 tháng 11 để tự quyết đi tiếp.",
        },
        {
            "id": 4,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_04_1.jpg",
            "title": "Nguyễn Thúy Hiền giành 5 HCV, phá 5 kỷ lục Đại hội Toàn quốc",
            "digest_line": "Kình ngư 17 tuổi Nguyễn Thúy Hiền bùng nổ giành năm huy chương vàng, phá năm kỷ lục Đại hội.",
        },
        {
            "id": 5,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_05_1.jpg",
            "title": "Nguyễn Thị Ánh Viên giành HCV sau 1437 ngày giải nghệ",
            "digest_line": "Ánh Viên cùng đội Quân đội đoạt huy chương vàng tiếp sức 4 nhân 200 mét tự do sau 1437 ngày giải nghệ.",
        },
        {
            "id": 6,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_06_1.jpg",
            "title": "Phạm Thanh Bảo phá sâu kỷ lục quốc gia 100m ếch nam",
            "digest_line": "Phạm Thanh Bảo đoạt huy chương vàng 100 mét ếch nam với thông số 1 phút 00 giây 47, phá kỷ lục quốc gia.",
        },
        {
            "id": 7,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_07_1.jpg",
            "title": "Bảng tổng sắp Đại hội Toàn quốc: TP.HCM hơn Hà Nội 16 HCV",
            "digest_line": "Thành phố Hồ Chí Minh dẫn đầu Đại hội Toàn quốc với 54 huy chương vàng, bỏ xa Hà Nội 16 vàng.",
        },
        {
            "id": 8,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_08_1.jpg",
            "title": "Bóng đá nữ Đại hội: TP.HCM hẹn Thái Nguyên ở chung kết",
            "digest_line": "Hạ Ninh Bình 2-1, bóng đá nữ Thành phố Hồ Chí Minh hẹn Thái Nguyên ở chung kết ngày 1 tháng 12.",
        },
        {
            "id": 9,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_09_1.jpg",
            "title": "Lại Lý Huynh và Minh Nhật Quang thắng lớn cờ tướng Đại hội",
            "digest_line": "Ở nội dung cờ tiêu chuẩn nam, Lại Lý Huynh và Minh Nhật Quang toàn thắng dẫn đầu giải.",
        },
        {
            "id": 10,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_10_1.jpg",
            "title": "Cựu tài xế taxi Chu Việt Hoàng vô địch pool 9 bi Đại hội",
            "digest_line": "Cựu tài xế Chu Việt Hoàng thắng ngược Nguyễn Hoàng Phong 9-6, đoạt huy chương vàng pool 9 bi.",
        },
        {
            "id": 11,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_11_1.jpg",
            "title": "Té xe giữa đường đua, Lê Ngọc Sơn vẫn giành HCV xe đạp",
            "digest_line": "Cua-rơ Lê Ngọc Sơn nén đau sau cú ngã nặng để về nhất cự ly tính điểm nam cùng Nguyễn Thị Thật.",
        },
        {
            "id": 12,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_12_1.jpg",
            "title": "CLB Công an Hà Nội sẵn sàng đại chiến Vissel Kobe tối nay",
            "digest_line": "Công an Hà Nội quyết tâm tiếp đón đội đầu bảng Vissel Kobe tối nay tại Hàng Đẫy ở cúp châu Á.",
        },
        {
            "id": 13,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_13_1.jpg",
            "title": "Nguyễn Xuân Son lọt Top 30 đề cử Quả bóng vàng châu Á 2026",
            "digest_line": "Tiền đạo Nguyễn Xuân Son lọt danh sách 30 đề cử Quả bóng vàng châu Á 2026 cùng Son Heung-min.",
        },
        {
            "id": 14,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_14_1.jpg",
            "title": "Lê Quang Liêm tái đấu Ian Nepomniachtchi tại Jerusalem Masters",
            "digest_line": "Kỳ thủ Lê Quang Liêm sắp bước vào màn tái đấu Ian Nepomniachtchi tại siêu giải cờ nhanh Jerusalem Masters.",
        },
        {
            "id": 15,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_15_1.jpg",
            "title": "Brentford đè bẹp Everton 4-0 trong đêm kỷ lục buồn của David Moyes",
            "digest_line": "Keane Lewis-Potter lập cú đúp giúp Brentford vùi dập 10 người của Everton với tỷ số đậm 4-0.",
        },
        {
            "id": 16,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_16_1.jpg",
            "title": "Manchester United kháng cáo thẻ đỏ Leny Yoro",
            "digest_line": "Manchester United gửi đơn kháng cáo thẻ đỏ Leny Yoro sau trận thua Liverpool giữa cơn giận của Gary Neville.",
        },
        {
            "id": 17,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_17_1.jpg",
            "title": "Thủ môn David Raya lỡ đại chiến Arsenal gặp Borussia Dortmund",
            "digest_line": "Thủ thành David Raya không phải mổ chấn thương vai nhưng chắc chắn vắng mặt khi Arsenal gặp Dortmund.",
        },
        {
            "id": 18,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_18_1.jpg",
            "title": "Bayern Munich mất Harry Kane ba tháng vì chấn thương mắt cá",
            "digest_line": "Bayern Munich mất Harry Kane ba tháng sau ca mổ mắt cá, đồng thời đối mặt tranh cãi quanh Jamal Musiala.",
        },
        {
            "id": 19,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_19_1.jpg",
            "title": "Diego Simeone phá kỷ lục 345 chiến thắng tại La Liga",
            "digest_line": "Huấn luyện viên Diego Simeone chạm mốc 345 trận thắng, chính thức phá kỷ lục mọi thời đại tại La Liga.",
        },
        {
            "id": 20,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_20_1.jpg",
            "title": "U17 Tây Ban Nha thắng 15-0, U17 Trung Quốc hòa phút 90 cộng 9",
            "digest_line": "U17 Tây Ban Nha thắng Fiji 15-0, còn U17 Trung Quốc bị Ma Rốc gỡ hòa 2-2 ở phút 90 cộng 9.",
        },
        {
            "id": 21,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_21_1.jpg",
            "title": "FIFA phê duyệt chủ nhà World Cup nữ 2031 và 2035",
            "digest_line": "FIFA chốt liên danh bốn nước Bắc Mỹ đăng cai World Cup nữ 2031 và Vương quốc Anh tổ chức năm 2035.",
        },
        {
            "id": 22,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_22_1.jpg",
            "title": "Tài liệu mật phanh phui kế hoạch bán quyền World Cup 96 năm",
            "digest_line": "Chủ tịch FIFA Gianni Infantino bị phanh phui kế hoạch bán quyền thương mại giải đấu đội tuyển tới 96 năm.",
        },
        {
            "id": 23,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_23_1.jpg",
            "title": "Huyền thoại Dudu Georgescu qua đời bí ẩn tại quê nhà",
            "digest_line": "Cựu tiền đạo từng hai lần đoạt Chiếc giày vàng châu Âu Dudu Georgescu qua đời ở tuổi 76 đầy nghi vấn.",
        },
        {
            "id": 24,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_24_1.jpg",
            "title": "Gonzalo Tapia lên tiếng vụ bị Lionel Messi ném bóng vào mặt",
            "digest_line": "Gonzalo Tapia lên tiếng sau pha bị Lionel Messi ném bóng vào mặt khiến thủ quân Inter Miami dễ bị phạt.",
        },
        {
            "id": 25,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_25_1.jpg",
            "title": "Jannik Sinner phẫu thuật đầu gối tại Phần Lan",
            "digest_line": "Jannik Sinner sang Phần Lan phẫu thuật đầu gối, đối diện nguy cơ lỡ giải Grand Slam Australian Open 2027.",
        },
        {
            "id": 26,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_26_1.jpg",
            "title": "Tyson Fury tiết lộ từng được chẩn đoán tâm thần phân liệt",
            "digest_line": "Trước trận gặp Anthony Joshua, Tyson Fury tiết lộ từng được chẩn đoán tâm thần phân liệt và lưỡng cực.",
        },
        {
            "id": 27,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_27_1.jpg",
            "title": "Bóng bàn Trung Quốc vắng bóng ở chung kết WTT Muscat",
            "digest_line": "Cử tới 19 tay vợt dự WTT Muscat nhưng bóng bàn Trung Quốc bất ngờ vắng bóng ở mọi trận chung kết.",
        },
    ],
}


def validate_specs(cfg: dict) -> None:
    items = cfg["items"]
    assert len(items) == 27, f"Expected 27 items, got {len(items)}"
    total_words = 0
    seen_imgs = set()

    full_seo = f"{cfg['seo_title']} | Điểm Đọc #Shorts"
    if len(full_seo) > 100:
        raise AssertionError(f"SEO title too long ({len(full_seo)}): {full_seo}")

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

    est_body = total_words / 3.95
    print(f"\nTổng số từ: {total_words} từ | Ước lượng body: ~{est_body:.1f}s (+Outro ~6.5s = ~{est_body+6.5:.1f}s < 180s)")
    print(f"SEO Title ({len(full_seo)} chars): {full_seo}")


def main() -> None:
    validate_specs(DIGEST_SPECS)
    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    SPEC_PATH.write_text(json.dumps(DIGEST_SPECS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] Đã xuất {SPEC_PATH}")


if __name__ == "__main__":
    main()
