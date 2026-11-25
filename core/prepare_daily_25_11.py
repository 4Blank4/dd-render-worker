# -*- coding: utf-8 -*-
"""
prepare_daily_25_11.py — Thu thập ảnh sạch HD không logo/watermark, đối chứng từng câu,
xuất kịch bản chuẩn hóa và dựng Contact Sheet QA cho bản tin ngày 25.11.2026
(Intro + 23 tin độc lập Việt Nam & Thế giới + Mục 24 Các tin thể thao khác).
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

from PIL import Image
from core.diemdoc import paths
from core.diemdoc.image_curator import trim_edge_margins
import daily_25_11_data as d25
import prepare_daily_22_11 as p22

TRIM_BOTTOM_FILES = {
    "Tin_00_9.jpg": 0.07,
    "Tin_00_10.jpg": 0.07,
    "Tin_01_5.jpg": 0.07,
    "Tin_01_6.jpg": 0.07,
    "Tin_01_9.jpg": 0.07,
    "Tin_02_2.jpg": 0.07,
    "Tin_02_5.jpg": 0.07,
    "Tin_02_6.jpg": 0.07,
    "Tin_04_4.jpg": 0.08,
    "Tin_07_1.jpg": 0.07,
    "Tin_07_4.jpg": 0.07,
    "Tin_08_1.jpg": 0.07,
    "Tin_08_3.jpg": 0.07,
    "Tin_23_4.jpg": 0.07,
    "Tin_24_12.jpg": 0.07,
}

DAY_STR = "25.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR

THUMBS_PLAN_25_11 = [
    {
        "suffix": "A",
        "badge": "BẢN TIN 25.11.2026",
        "kicker": "CÚP C1 CHÂU Á • ĐẠI HỘI 2026",
        "headline": "CAHN HẠ KOBE 3-1<br>REAL THẮNG ĐẬM 5-1",
        "subtitle": "Ánh Viên phá kỷ lục sau 8 năm • U17 Việt Nam tăng bậc • Man City hòa 2-2",
        "footer_tag": "TIN NÓNG • 25.11",
        "image_file": "outputs/25.11.2026/images/Tin_01_1.jpg",
        "obj_pos": "center 22%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
    {
        "suffix": "B",
        "badge": "CHẤN ĐỘNG BÓNG ĐÁ",
        "kicker": "CÚP C1 CHÂU Á • AFCON 2025",
        "headline": "CAHN HẠ KOBE 3-1<br>SENEGAL ĐÒI LẠI CÚP",
        "subtitle": "Ronaldo ghi bàn 987 & nhại trọng tài • CAS tước cúp Morocco",
        "footer_tag": "TIN NÓNG • 25.11",
        "image_file": "outputs/25.11.2026/images/Tin_01_1.jpg",
        "cards": [
            {"file": "outputs/25.11.2026/images/Tin_01_1.jpg", "tag": "CAHN HẠ KOBE 3-1", "pos": "center 20%"},
            {"file": "outputs/25.11.2026/images/Tin_17_1.jpg", "tag": "RONALDO GHI BÀN 987", "pos": "center 18%"},
            {"file": "outputs/25.11.2026/images/Tin_18_1.jpg", "tag": "SENEGAL ĐÒI LẠI CÚP", "pos": "center 22%"},
        ],
        "obj_pos": "center 20%",
        "filter": "contrast(1.06) saturate(1.08)",
    },
    {
        "suffix": "C",
        "badge": "CHAMPIONS LEAGUE",
        "kicker": "REAL MADRID • MAN CITY",
        "headline": "REAL THẮNG ĐẬM 5-1<br>DE BRUYNE TÁI NGỘ",
        "subtitle": "Bellingham & Mbappé tỏa sáng • U17 Việt Nam lên hạng 7 nhóm thứ ba",
        "footer_tag": "TIN NÓNG • 25.11",
        "image_file": "outputs/25.11.2026/images/Tin_13_1.jpg",
        "right_image": "outputs/25.11.2026/images/Tin_14_1.jpg",
        "obj_pos": "center 22%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
]


def main() -> None:
    p22.DAY_STR = DAY_STR
    p22.OUT_DIR = OUT_DIR
    p22.IMG_DIR = OUT_DIR / "images"
    p22.QA_DIR = OUT_DIR / "qa"
    p22.CACHE_DIR = Path(paths.WORK) / "img_cache_25_11"
    p22.data_22_11 = d25

    p22.main()

    # Cắt gọn mép logo nhỏ (7%) trên các ảnh Thanh Niên / Tuổi Trẻ / bản quyền góc dưới
    img_dir = OUT_DIR / "images"
    qa_dir = OUT_DIR / "qa"
    plan_p = OUT_DIR / "image_plan.json"
    plan_data = json.loads(plan_p.read_text(encoding="utf-8"))
    records = plan_data.get("records", [])
    trimmed_sids = set()
    for rec in records:
        fn = rec["file_name"]
        frac = TRIM_BOTTOM_FILES.get(fn)
        if frac:
            fp = img_dir / fn
            if fp.exists():
                with Image.open(fp) as im:
                    cropped = trim_edge_margins(im.convert("RGB"), top_frac=0.0, bottom_frac=frac)
                cropped.save(fp, format="JPEG", quality=95, optimize=True)
                rec["dimensions"] = f"{cropped.width}x{cropped.height} r={cropped.width / cropped.height:.2f}"
                trimmed_sids.add(int(rec["scene_id"]))
                print(f"[trim] Đã cắt mép dưới {int(frac * 100)}%: {fn} -> {rec['dimensions']}")

    if trimmed_sids:
        plan_p.write_text(json.dumps(plan_data, ensure_ascii=False, indent=2), encoding="utf-8")
        all_specs = {int(sp["id"]): sp for sp in [d25.INTRO_DATA] + list(d25.NEWS_SPECS)}
        by_scene = {}
        for r in records:
            by_scene.setdefault(int(r["scene_id"]), []).append(r)
        overview_records = []
        for sid, recs in sorted(by_scene.items()):
            overview_records.extend(recs[:2])
            if sid in trimmed_sids:
                sp = all_specs[sid]
                is_intro = sid == 0
                vp = sp.get("voice_preset") or ("mixed" if is_intro else ("primary" if sid % 2 == 1 else "secondary"))
                vname, _ = p22.VOICE_INFO.get(vp, ("Minh Quân Pro", "male"))
                sheet_name = "contact_scene_00_intro.jpg" if is_intro else f"contact_scene_{sid:02d}.jpg"
                sheet_title = sp.get("group") or "MỞ ĐẦU BẢN TIN" if is_intro else sp["title"]
                p22.render_scene_contact_sheet(
                    sid, sheet_title, sp.get("news_source") or sp.get("source") or "",
                    f"{vp} ({vname})", [{**r, "is_fallback": False} for r in recs], qa_dir / sheet_name,
                )
        p22.render_overview_sheet(overview_records, len(d25.NEWS_SPECS), qa_dir / "contact_overview.jpg")

    (OUT_DIR / "thumbnails_plan.json").write_text(
        json.dumps(THUMBS_PLAN_25_11, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[ok] Đã cập nhật thumbnails_plan.json chuẩn ngày {DAY_STR}.")


if __name__ == "__main__":
    main()
