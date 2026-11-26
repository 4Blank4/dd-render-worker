# -*- coding: utf-8 -*-
"""
prepare_daily_26_11.py — Thu thập ảnh sạch HD không logo/watermark, đối chứng từng câu,
xuất kịch bản chuẩn hóa và dựng Contact Sheet QA cho bản tin ngày 26.11.2026
(Intro + 25 tin độc lập Việt Nam & Thế giới + Mục 26 Các tin thể thao khác).
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
import daily_26_11_data as d26
import prepare_daily_22_11 as p22

DAY_STR = "26.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR

# Cắt nhẹ mép logo ở góc dưới trên các ảnh Thanh Niên / Tuổi Trẻ / VTV Times
TRIM_BOTTOM_FILES: dict[str, float] = {
    "Tin_00_9.jpg": 0.07,
    "Tin_00_10.jpg": 0.07,
    "Tin_04_4.jpg": 0.12,
    "Tin_05_6.jpg": 0.07,
    "Tin_06_2.jpg": 0.07,
    "Tin_06_5.jpg": 0.07,
    "Tin_06_6.jpg": 0.07,
    "Tin_07_1.jpg": 0.07,
    "Tin_07_2.jpg": 0.07,
    "Tin_07_3.jpg": 0.07,
    "Tin_07_4.jpg": 0.07,
    "Tin_07_5.jpg": 0.07,
    "Tin_07_6.jpg": 0.07,
    "Tin_10_1.jpg": 0.07,
    "Tin_10_2.jpg": 0.07,
    "Tin_10_3.jpg": 0.07,
    "Tin_10_4.jpg": 0.07,
    "Tin_10_5.jpg": 0.07,
}

THUMBS_PLAN_26_11 = [
    {
        "suffix": "A",
        "badge": "BẢN TIN 26.11.2026",
        "kicker": "CHAMPIONS LEAGUE • U17 WORLD CUP",
        "headline": "MAN UTD HÒA 2-2<br>BAYERN THUA 1-2",
        "subtitle": "MU rơi hạng 19 • U17 Việt Nam quyết đấu Mali 20h • Liverpool thắng 3-0",
        "footer_tag": "TIN NÓNG • 26.11",
        "image_file": "outputs/26.11.2026/images/Tin_11_1.jpg",
        "obj_pos": "center 22%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
    {
        "suffix": "B",
        "badge": "TÂM ĐIỂM 26.11.2026",
        "kicker": "CHAMPIONS LEAGUE • U17 WC • ĐẠI HỘI",
        "headline": "MU RƠI HẠNG 19<br>U17 VN QUYẾT ĐẤU",
        "subtitle": "Man Utd hòa Sporting 2-2 • U17 Việt Nam đấu Mali • Thùy Linh hat-trick HCV",
        "footer_tag": "TIN NÓNG • 26.11",
        "image_file": "outputs/26.11.2026/images/Tin_11_1.jpg",
        "cards": [
            {"file": "outputs/26.11.2026/images/Tin_11_1.jpg", "tag": "MAN UTD RƠI HẠNG 19", "pos": "center 20%"},
            {"file": "outputs/26.11.2026/images/Tin_01_1.jpg", "tag": "U17 VN QUYẾT ĐẤU MALI", "pos": "center 20%"},
            {"file": "outputs/26.11.2026/images/Tin_06_1.jpg", "tag": "THÙY LINH HAT-TRICK", "pos": "center 18%"},
        ],
        "obj_pos": "center 20%",
        "filter": "contrast(1.06) saturate(1.08)",
    },
    {
        "suffix": "C",
        "badge": "CHAMPIONS LEAGUE",
        "kicker": "MAN UTD • BAYERN • RONALDO",
        "headline": "MU HÒA TRANH CÃI<br>BAYERN THUA LILLE",
        "subtitle": "Lammens mắc lỗi, trọng tài gây bão • Ronaldo nguy cơ bị treo giò 4 trận",
        "footer_tag": "TIN NÓNG • 26.11",
        "image_file": "outputs/26.11.2026/images/Tin_11_1.jpg",
        "right_image": "outputs/26.11.2026/images/Tin_13_1.jpg",
        "obj_pos": "center 22%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
]


def main() -> None:
    p22.DAY_STR = DAY_STR
    p22.OUT_DIR = OUT_DIR
    p22.IMG_DIR = OUT_DIR / "images"
    p22.QA_DIR = OUT_DIR / "qa"
    p22.CACHE_DIR = Path(paths.WORK) / "img_cache_26_11"
    p22.data_22_11 = d26

    p22.main()

    if TRIM_BOTTOM_FILES:
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
            all_specs = {int(sp["id"]): sp for sp in [d26.INTRO_DATA] + list(d26.NEWS_SPECS)}
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
            p22.render_overview_sheet(overview_records, len(d26.NEWS_SPECS), qa_dir / "contact_overview.jpg")

    (OUT_DIR / "thumbnails_plan.json").write_text(
        json.dumps(THUMBS_PLAN_26_11, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[ok] Đã cập nhật thumbnails_plan.json chuẩn ngày {DAY_STR}.")


if __name__ == "__main__":
    main()
