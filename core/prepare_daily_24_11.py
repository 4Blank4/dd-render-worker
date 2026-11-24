# -*- coding: utf-8 -*-
"""
prepare_daily_24_11.py — Thu thập ảnh sạch HD không logo/watermark, đối chứng từng câu,
xuất kịch bản chuẩn hóa và dựng Contact Sheet QA cho bản tin ngày 24.11.2026
(Intro + 28 tin độc lập Việt Nam & Thế giới + Mục 29 Các tin thể thao khác).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

from core.diemdoc import paths
import daily_24_11_data as d24
import prepare_daily_22_11 as p22

DAY_STR = "24.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR

THUMBS_PLAN_24_11 = [
    {
        "suffix": "A",
        "badge": "BẢN TIN 24.11.2026",
        "kicker": "U17 WORLD CUP • ĐẠI HỘI 2026",
        "headline": "U17 VIỆT NAM 3-3 NZ<br>THÚY HIỀN 5 KỶ LỤC!",
        "subtitle": "Duy Khang gỡ hòa 90+2' • Ánh Viên giành HCV • Brentford thắng 4-0",
        "footer_tag": "TIN NÓNG • 24.11",
        "image_file": "outputs/24.11.2026/images/Tin_01_1.jpg",
        "obj_pos": "center 22%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
    {
        "suffix": "B",
        "badge": "ĐẠI HỘI TOÀN QUỐC",
        "kicker": "BƠI LỘI • NGOẠI HẠNG ANH",
        "headline": "ÁNH VIÊN GIÀNH HCV<br>BRENTFORD THẮNG 4-0",
        "subtitle": "Thúy Hiền 5 HCV • Phạm Thanh Bảo phá KLQG • MU kháng cáo thẻ đỏ Yoro",
        "footer_tag": "TIN NÓNG • 24.11",
        "image_file": "outputs/24.11.2026/images/Tin_05_1.jpg",
        "cards": [
            {"file": "outputs/24.11.2026/images/Tin_04_1.jpg", "tag": "ÁNH VIÊN GIÀNH HCV", "pos": "center 18%"},
            {"file": "outputs/24.11.2026/images/Tin_15_1.jpg", "tag": "THÚY HIỀN 5 KỶ LỤC", "pos": "center 22%"},
            {"file": "outputs/24.11.2026/images/Tin_15_1.jpg", "tag": "BRENTFORD THẮNG 4-0", "pos": "center 22%"},
        ],
        "obj_pos": "center 20%",
        "filter": "contrast(1.06) saturate(1.08)",
    },
    {
        "suffix": "C",
        "badge": "TÂM ĐIỂM THẾ GIỚI",
        "kicker": "NGOẠI HẠNG ANH • QUẦN VỢT",
        "headline": "BRENTFORD ĐÈ BẸP 4-0<br>SINNER MỔ ĐẦU GỐI",
        "subtitle": "Gary Neville tự tát mặt • Simeone lập kỷ lục • Trung Quốc thua sốc",
        "footer_tag": "TIN NÓNG • 24.11",
        "image_file": "outputs/24.11.2026/images/Tin_15_1.jpg",
        "right_image": "outputs/24.11.2026/images/Tin_25_1.jpg",
        "obj_pos": "center 22%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
]


def main() -> None:
    p22.DAY_STR = DAY_STR
    p22.OUT_DIR = OUT_DIR
    p22.IMG_DIR = OUT_DIR / "images"
    p22.QA_DIR = OUT_DIR / "qa"
    p22.CACHE_DIR = Path(paths.WORK) / "img_cache_24_11"
    p22.data_22_11 = d24

    p22.main()

    (OUT_DIR / "thumbnails_plan.json").write_text(
        json.dumps(THUMBS_PLAN_24_11, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[ok] Đã cập nhật thumbnails_plan.json chuẩn ngày {DAY_STR}.")


if __name__ == "__main__":
    main()
