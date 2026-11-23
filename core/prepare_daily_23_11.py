# -*- coding: utf-8 -*-
"""
prepare_daily_23_11.py — Thu thập ảnh sạch HD không logo/watermark, đối chứng từng câu,
xuất kịch bản chuẩn hóa và dựng Contact Sheet QA cho bản tin ngày 23.11.2026
(Intro + 16 tin chính Việt Nam & Thế giới + Mục 17 Các tin thể thao khác).
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
import daily_23_11_data as d23
import prepare_daily_22_11 as p22

DAY_STR = "23.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR

THUMBS_PLAN_23_11 = [
    {
        "suffix": "A",
        "badge": "BẢN TIN 23.11.2026",
        "kicker": "NGOẠI HẠNG ANH • ĐẠI HỘI 2026",
        "headline": "LIVERPOOL HỦY DIỆT<br>MAN UNITED 4-0!",
        "subtitle": "Thảm họa ra mắt của Pochettino • Barca ngược dòng • Alcaraz vô địch",
        "footer_tag": "TIN NÓNG • 23.11",
        "image_file": "outputs/23.11.2026/images/Tin_07_1.jpg",
        "obj_pos": "center 22%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
    {
        "suffix": "B",
        "badge": "CHẤN ĐỘNG ANFIELD",
        "kicker": "KỶ LỤC 100 NĂM • LA LIGA",
        "headline": "THẢM BẠI ANFIELD!<br>BARCA NGƯỢC DÒNG",
        "subtitle": "MU tụt xuống hạng 19 • Yamal hỏng 11m • Márquez 8 lần vô địch MotoGP",
        "footer_tag": "TIN NÓNG • 23.11",
        "image_file": "outputs/23.11.2026/images/Tin_07_2.jpg",
        "obj_pos": "center 20%",
        "filter": "contrast(1.06) saturate(1.08)",
    },
    {
        "suffix": "C",
        "badge": "TÂM ĐIỂM THỂ THAO",
        "kicker": "ĐẠI HỘI TOÀN QUỐC 2026",
        "headline": "ÁNH VIÊN TÁI XUẤT<br>ĐẠI HỘI MƯA KỶ LỤC",
        "subtitle": "Mỹ Tiên thắng 200m • Watson Nguyễn phá KLQG • Hoàng Đức đưa Ninh Bình nhì bảng",
        "footer_tag": "TIN NÓNG • 23.11",
        "image_file": "outputs/23.11.2026/images/Tin_01_1.jpg",
        "obj_pos": "center 22%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
]


def main() -> None:
    p22.DAY_STR = DAY_STR
    p22.OUT_DIR = OUT_DIR
    p22.IMG_DIR = OUT_DIR / "images"
    p22.QA_DIR = OUT_DIR / "qa"
    p22.CACHE_DIR = Path(paths.WORK) / "img_cache_23_11"
    p22.data_22_11 = d23

    p22.main()

    (OUT_DIR / "thumbnails_plan.json").write_text(
        json.dumps(THUMBS_PLAN_23_11, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[ok] Đã cập nhật thumbnails_plan.json chuẩn ngày {DAY_STR}.")


if __name__ == "__main__":
    main()
