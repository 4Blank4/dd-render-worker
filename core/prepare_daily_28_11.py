# -*- coding: utf-8 -*-
"""
prepare_daily_28_11.py — Thu thập ảnh sạch HD không logo/watermark, đối chứng từng câu,
xuất kịch bản chuẩn hóa, 3 Thumbnail 16:9 (1 ảnh -> 3 ảnh -> 2 ảnh khớp 2 tin Option C)
và Contact Sheet QA cho bản tin ngày 28.11.2026.
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
from build_thumbnails_09_11 import render_thumbnails
import daily_28_11_data as d28
import prepare_daily_22_11 as p22

DAY_STR = "28.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR

# Cắt nhẹ mép dưới nếu có logo báo góc dưới
TRIM_BOTTOM_FILES: dict[str, float] = {}

# Bộ 3 Thumbnail 16:9 đồng nhất 100% với 3 Option Tiêu đề:
#   - Option A (cyber_split): 1 sự kiện (Chelsea thua Nottingham Forest 2-3)
#   - Option B (magazine_bento): 3 sự kiện (Chelsea thua Forest / Márquez giải nghệ / Nam Định hòa CAHN)
#   - Option C (clash_diagonal): 2 sự kiện (Nam Định hòa CAHN 0-0 & Nottingham Forest hạ Chelsea 3-2)
THUMBS_PLAN_28_11 = [
    {
        "suffix": "A",
        "style": "cyber_split",
        "badge": "BẢN TIN 28.11.2026",
        "kicker": "NGOẠI HẠNG ANH • VÒNG 12",
        "headline": "CHELSEA THUA SỐC 2-3<br>ALONSO LÚN SÂU",
        "subtitle": "Nottingham Forest hạ gục Chelsea ngay tại City Ground • Trận thua thứ 3 liên tiếp",
        "footer_tag": "TIN NÓNG • 28.11",
        "image_file": "outputs/28.11.2026/images/Tin_10_1.jpg",
        "obj_pos": "center 20%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
    {
        "suffix": "B",
        "style": "magazine_bento",
        "badge": "TOÀN CẢNH 28.11.2026",
        "kicker": "NGOẠI HẠNG ANH • MOTOGP • V-LEAGUE",
        "headline": "CHELSEA THUA THỨ 3<br>MÁRQUEZ GIẢI NGHỆ",
        "subtitle": "Chelsea thua Forest 2-3 • Marc Márquez chia tay MotoGP • Nam Định hòa CAHN 0-0",
        "footer_tag": "TIN NÓNG • 28.11",
        "image_file": "outputs/28.11.2026/images/Tin_10_1.jpg",
        "cards": [
            {"file": "outputs/28.11.2026/images/Tin_10_1.jpg", "tag": "CHELSEA THUA FOREST 2-3", "pos": "center 20%"},
            {"file": "outputs/28.11.2026/images/Tin_17_1.jpg", "tag": "MÁRQUEZ GIẢI NGHỆ MOTOGP", "pos": "center 20%"},
            {"file": "outputs/28.11.2026/images/Tin_01_1.jpg", "tag": "NAM ĐỊNH HÒA CAHN 0-0", "pos": "center 22%"},
        ],
        "obj_pos": "center 20%",
        "filter": "contrast(1.06) saturate(1.1)",
    },
    {
        "suffix": "C",
        "style": "clash_diagonal",
        "badge": "TÂM ĐIỂM ĐỐI ĐẦU",
        "kicker": "V-LEAGUE • NGOẠI HẠNG ANH",
        "headline": "NAM ĐỊNH HÒA CAHN<br>CHELSEA THUA FOREST",
        "subtitle": "Nam Định chia điểm Công an Hà Nội 0-0 • Nottingham Forest hạ gục Chelsea 3-2",
        "footer_tag": "TIN NÓNG • 28.11",
        "image_file": "outputs/28.11.2026/images/Tin_01_1.jpg",
        "right_image": "outputs/28.11.2026/images/Tin_10_1.jpg",
        "left_pos": "center 20%",
        "right_pos": "center 20%",
        "obj_pos": "center 20%",
        "filter": "contrast(1.06) saturate(1.08)",
    },
]


def main() -> None:
    p22.DAY_STR = DAY_STR
    p22.OUT_DIR = OUT_DIR
    p22.IMG_DIR = OUT_DIR / "images"
    p22.QA_DIR = OUT_DIR / "qa"
    p22.CACHE_DIR = Path(paths.WORK) / "img_cache_28_11"
    p22.data_22_11 = d28

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
            all_specs = {int(sp["id"]): sp for sp in [d28.INTRO_DATA] + list(d28.NEWS_SPECS)}
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
            p22.render_overview_sheet(overview_records, len(d28.NEWS_SPECS), qa_dir / "contact_overview.jpg")

    (OUT_DIR / "thumbnails_plan.json").write_text(
        json.dumps(THUMBS_PLAN_28_11, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[ok] Đã cập nhật thumbnails_plan.json chuẩn ngày {DAY_STR}.")
    render_thumbnails(DAY_STR)


if __name__ == "__main__":
    main()
