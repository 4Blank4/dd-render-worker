# -*- coding: utf-8 -*-
"""
prepare_digest_28_11.py — Sinh cấu hình `outputs/28.11.2026/shorts/digest_specs.json`
cho Video Short Tin Nhanh 21 Tin (9:16, < 180s) ngày 28.11.2026.
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

DAY_STR = "28.11.2026"
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
SHORTS_DIR = DAY_DIR / "shorts"
SPEC_PATH = SHORTS_DIR / "digest_specs.json"


DIGEST_SPECS = {
    "day": DAY_STR,
    "title": "TIN NHANH THỂ THAO 28.11",
    "hide_date_chip": False,
    "out_video_name": "Short_Tin_Nhanh_21_Tin.mp4",
    "gap_ms": 200,
    "seo_title": "Tin nhanh 28/11: Nam Định hòa CAHN 0-0 & Chelsea thua sốc Nottingham 2-3",
    "description": [
        "Điểm đọc nhanh 21 tin tức thể thao nóng nhất ngày 28/11/2026 từ V-League 2026-2027, Đội tuyển Việt Nam, U17 World Cup 2026, Đại hội Thể thao toàn quốc 2026 tới Ngoại hạng Anh, Bundesliga, MotoGP, Formula 1 Qatar GP, Quyền anh và Davis Cup 2026.",
        "Nổi bật trận hòa không bàn thắng giữa Thép Xanh Nam Định và Công an Hà Nội tại Thiên Trường, phát biểu bác tin đồn Quang Hải của huấn luyện viên Polking, Sông Lam Nghệ An thắng Ninh Bình 1-0, Ánh Viên giành bảy HCV, Mỹ Tiên đạt chín HCV cá nhân, Nottingham Forest hạ Chelsea 3-2 và huyền thoại Marc Márquez bất ngờ tuyên bố giải nghệ MotoGP.",
    ],
    "fb_hook": "🔥 21 TIN THỂ THAO NÓNG NHẤT 28/11 TRONG HƠN 2 PHÚT!",
    "tiktok_caption": "Điểm nhanh 21 tin nóng thể thao 28/11: Nam Định hòa Công an Hà Nội 0-0, SLNA nối dài mạch 9 trận bất bại, Ánh Viên khép lại Đại hội với 7 HCV, Chelsea thua sốc Nottingham Forest 2-3 và huyền thoại MotoGP Marc Márquez bất ngờ giải nghệ ở tuổi 33!",
    "sources_line": "📰 Nguồn tin: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian, ESPN.",
    "hashtags": [
        "#Shorts",
        "#TinNhanh",
        "#DiemDoc",
        "#DiemDocTheThao",
        "#VLeague",
        "#NamDinh",
        "#CAHN",
        "#DaiHoiTheThaoToanQuoc2026",
        "#Chelsea",
        "#MarcMarquez",
    ],
    "thumb": {
        "style": "clash_diagonal",
        "image": "Tin_01_1.jpg",
        "bottom_image": "Tin_10_1.jpg",
        "kicker": "21 TIN NHANH THỂ THAO 28.11",
        "hero_html": '<span class="hl-cyan">21 TIN NHANH!</span><br><span class="hl-white">NAM ĐỊNH HÒA CAHN 0-0</span><br><span class="hl-yellow">CHELSEA THUA FOREST 2-3!</span>',
        "line1": "NAM ĐỊNH HÒA CAHN 0-0",
        "line2": "CHELSEA THUA FOREST 2-3",
        "subtitle": "ÁNH VIÊN 7 HCV • SLNA BẤT BẠI • MÁRQUEZ GIẢI NGHỆ",
        "badge": "21 TIN NHANH",
        "tag_a": "VN & QUỐC TẾ",
        "tag_b": "28.11.2026",
        "hero_size": "70",
        "obj_pos": "center 20%",
        "top_pos": "center 20%",
        "bot_pos": "center 20%",
    },
    "items": [
        # 8 Tin Việt Nam — Giọng Nữ Ngọc Huyền (secondary)
        {
            "id": 1,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_01_1.jpg",
            "title": "Nam Định hòa Công an Hà Nội 0-0, giữ vững ngôi đầu V-League",
            "digest_line": "Tại Thiên Trường tối qua, Nam Định hòa Công an Hà Nội 0-0 để tiếp tục giữ vững ngôi đầu hơn đối thủ năm điểm.",
        },
        {
            "id": 2,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_02_1.jpg",
            "title": "HLV Polking bác tin đồn Quang Hải chia tay tuyển Việt Nam",
            "digest_line": "Huấn luyện viên Alexandre Polking khẳng định thông tin Quang Hải muốn rời đội tuyển Việt Nam hoàn toàn là tin giả.",
        },
        {
            "id": 3,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_03_1.jpg",
            "title": "SLNA thắng Ninh Bình 1-0, nối dài mạch 9 trận bất bại",
            "digest_line": "Bàn thắng của Luiz Guilherme giúp Sông Lam Nghệ An đánh bại Ninh Bình 1-0 và nối dài mạch chín trận bất bại.",
        },
        {
            "id": 4,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_04_1.jpg",
            "title": "Tâm điểm V-League hôm nay: Hà Nội đấu Hà Tĩnh, CA TP.HCM gặp HAGL",
            "digest_line": "Chiều tối nay ở vòng chín V-League, Công an TP.HCM tiếp đón Hoàng Anh Gia Lai còn Hà Nội FC chạm trán Hà Tĩnh.",
        },
        {
            "id": 6,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_06_2.jpg",
            "title": "Báo khu vực khen bản lĩnh U17 Việt Nam, Nguyễn Lực ghi dấu ấn",
            "digest_line": "Thầy trò Cristiano Roland về nước trong lời khen từ báo khu vực, còn Chu Ngọc Nguyễn Lực lập cột mốc hai bàn World Cup.",
        },
        {
            "id": 7,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_07_1.jpg",
            "title": "Ánh Viên khép lại Đại hội với 7 HCV, Mỹ Tiên đạt 9 HCV cá nhân",
            "digest_line": "Nguyễn Thị Ánh Viên khép lại Đại hội với bảy huy chương vàng, trong khi Võ Thị Mỹ Tiên thống trị với chín ngôi vô địch cá nhân.",
        },
        {
            "id": 8,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_08_1.jpg",
            "title": "Điền kinh Đại hội phá kỷ lục 100m rào, Ngần Ngọc Nghĩa bị thẻ đỏ",
            "digest_line": "Bùi Thị Nguyên phá kỷ lục Đại hội 100 mét rào, còn vua tốc độ Ngần Ngọc Nghĩa nhận thẻ đỏ xuất phát sớm ở bán kết.",
        },
        {
            "id": 9,
            "region": "Việt Nam",
            "voice_preset": "secondary",
            "voice_gender": "Nữ",
            "image_file": "Tin_09_1.jpg",
            "title": "Châu Tuyết Vân đoạt HCV thứ 5 liên tiếp, TP.HCM đạt 96 HCV",
            "digest_line": "Châu Tuyết Vân giành huy chương vàng Taekwondo thứ năm liên tiếp, đưa đoàn Thành phố Hồ Chí Minh chạm mốc 96 huy chương vàng.",
        },
        # 13 Tin Quốc tế — Giọng Nam Minh Quân Pro (primary)
        {
            "id": 5,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_05_1.jpg",
            "title": "U17 World Cup đủ 32 đội vào vòng 1/16, Nhật Bản gặp Hàn Quốc",
            "digest_line": "Nhật Bản thắng Honduras 7-0 khi vòng bảng U17 World Cup khép lại với 32 đội đi tiếp và hẹn gặp Hàn Quốc ở vòng sau.",
        },
        {
            "id": 10,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_10_1.jpg",
            "title": "Nottingham Forest hạ gục Chelsea 3-2 tại City Ground",
            "digest_line": "Morgan Gibbs-White lập cú đúp giúp Nottingham Forest thắng Chelsea 3-2, đẩy The Blues vào chuỗi ba thất bại liên tiếp.",
        },
        {
            "id": 11,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_11_2.jpg",
            "title": "Fofana bị fan Chelsea la ó, HLV Xabi Alonso thừa nhận khủng hoảng",
            "digest_line": "Wesley Fofana bị chính khán giả Chelsea la ó vì phạm lỗi phạt đền, còn Xabi Alonso thừa nhận đội bóng đang gặp khó.",
        },
        {
            "id": 12,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_12_1.jpg",
            "title": "Man Utd gia hạn hợp đồng đội trưởng Bruno Fernandes tới năm 2028",
            "digest_line": "Manchester United kích hoạt điều khoản gia hạn hợp đồng thêm một năm, giữ chân đội trưởng Bruno Fernandes đến mùa hè 2028.",
        },
        {
            "id": 13,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_13_1.jpg",
            "title": "Các CLB Ngoại hạng Anh đề xuất buộc chủ Man City bán đội bóng",
            "digest_line": "Ba đội bóng đối thủ đề xuất buộc chủ sở hữu Man City bán câu lạc bộ ngay trước thềm đại chiến gặp Arsenal cuối tuần này.",
        },
        {
            "id": 14,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_14_1.jpg",
            "title": "Tottenham tổn thất nặng khi Savio có thể nghỉ tới 80 ngày",
            "digest_line": "Huấn luyện viên Roberto De Zerbi xác nhận cầu thủ chạy cánh Savio tái phát gân kheo và có thể nghỉ tới 80 ngày.",
        },
        {
            "id": 15,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_15_1.jpg",
            "title": "Bạo loạn sân cỏ châu Âu khiến Tổng thống Pháp Macron lên tiếng",
            "digest_line": "Bạo loạn nghiêm trọng quanh trận Marseille gặp Levski Sofia khiến nhiều người nhập viện, buộc Tổng thống Macron phải lên án.",
        },
        {
            "id": 16,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_16_1.jpg",
            "title": "Bundesliga: Werder Bremen gỡ hòa 3-3 trước Gladbach phút 90+2",
            "digest_line": "Niclas Füllkrug ghi bàn ở phút bù giờ 90 cộng hai giúp Werder Bremen giật lại trận hòa 3-3 kịch tính trước Gladbach.",
        },
        {
            "id": 17,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_17_1.jpg",
            "title": "Huyền thoại Marc Márquez bất ngờ tuyên bố giải nghệ MotoGP ở tuổi 33",
            "digest_line": "Nhà vô địch tám lần thế giới Marc Márquez gây chấn động khi thông báo giải nghệ MotoGP sau mùa 2026 vì nỗi lo chấn thương.",
        },
        {
            "id": 18,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_18_2.jpg",
            "title": "F1 Qatar GP: Kimi Antonelli dẫn đầu ngày tập đầu, Hamilton gặp sự cố",
            "digest_line": "Tay đua trẻ Kimi Antonelli dẫn đầu cả hai phiên tập đầu Qatar Grand Prix, còn Lewis Hamilton gặp trục trặc động cơ.",
        },
        {
            "id": 19,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_19_1.jpg",
            "title": "Tyson Fury chính thức được cấp phép đấu Anthony Joshua tháng 12",
            "digest_line": "Ủy ban Quyền anh Anh cấp phép cho Tyson Fury thượng đài gặp Anthony Joshua ngày 11 tháng 12 sau khi đính chính hồ sơ y tế.",
        },
        {
            "id": 20,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_20_1.jpg",
            "title": "Davis Cup 2026: Italy thắng CH Séc 2-1, lần thứ 4 vào chung kết",
            "digest_line": "Đương kim vô địch Italy thắng nghẹt thở Cộng hòa Séc 2-1 để lần thứ tư liên tiếp vào chung kết Davis Cup.",
        },
        {
            "id": 21,
            "region": "Quốc tế",
            "voice_preset": "primary",
            "voice_gender": "Nam",
            "image_file": "Tin_21_2.jpg",
            "title": "Bồ Đào Nha cân nhắc thay HLV trưởng ở trận tri ân Cristiano Ronaldo",
            "digest_line": "Bồ Đào Nha xem xét mời lại Scolari dẫn dắt trận chia tay Cristiano Ronaldo thay cho Jorge Jesus vì mâu thuẫn nội bộ.",
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
    if cfg["thumb"].get("bottom_image"):
        b_img = IMAGES_DIR / cfg["thumb"]["bottom_image"]
        assert b_img.exists(), f"Missing thumb bottom_image: {b_img}"

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
        prepare(line)
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
