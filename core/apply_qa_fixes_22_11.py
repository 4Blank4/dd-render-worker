# -*- coding: utf-8 -*-
"""
apply_qa_fixes_22_11.py — Sửa triệt để toàn bộ ảnh lỗi phát hiện qua kiểm duyệt thị giác
Contact Sheet ngày 22.11.2026:
  1. Xóa sạch 3 lỗi trùng lặp liên tiếp (Scene 04, 08, 18).
  2. Thay thế dứt điểm ảnh sai chủ thể / dính watermark stock / graphic overlay:
     - Tin_02_5, Tin_02_7 (Adobe Stock), Tin_02_10 (Vovinam -> Phạm Thanh Bảo bơi lội)
     - Tin_04_11 (Messi -> Công Phượng), Tin_05_9 (Messi -> Ninh Bình / V-League)
     - Tin_06_9 (ảnh giống 06_8 -> U17 VN), Tin_07_9 (Futsal -> CAHN FC)
     - Tin_09_2 (Chính trị gia fallback -> Bóng đá Indonesia/ĐNA)
     - Tin_13_11 (U17 VN fallback -> Bournemouth)
     - Tin_15_7 (Ferran Torres áo Barca -> PSG), Tin_16_6 (Atalanta -> AS Roma)
     - Tin_16_8 (BREAKING NEWS graphic -> RB Leipzig), Tin_16_9 (Thủ môn -> Dortmund)
     - Tin_17_9 (Graphic vòng tròn -> Inter Miami), Tin_20_6 (UFC 311 text -> Procházka)
     - Tin_23_12 (Ảnh ghép đôi -> Stamford Bridge / Chelsea)
  3. Cắt sạch viền logo nhỏ ở mép đáy (Thanh Niên / Dân Trí / Tuổi Trẻ / VPF / Tribunnews).
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

from core.diemdoc.image_curator import trim_edge_margins
import prepare_daily_22_11 as prep22

OUT_DIR = ROOT / "outputs" / "22.11.2026"
IMG_DIR = OUT_DIR / "images"
QA_DIR = OUT_DIR / "qa"

# Ảnh thay thế trực tiếp bằng URL / local / search đã kiểm lọc sạch watermark
REPLACEMENTS: Dict[str, Tuple[str, str, str]] = {
    # Scene 02: Watson Nguyễn & Phạm Thanh Bảo
    "Tin_02_5.jpg": ("ddgs", "swimming competition pool starting blocks lane water", "BƠI LỘI"),
    "Tin_02_7.jpg": ("ddgs", "swimmer breaststroke race olympic pool water", "USA SWIMMING"),
    "Tin_02_10.jpg": ("url", "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2025/12/12/pham-thanh-bao-hcv-100m-ech-sea-games-17655436837691165389098.jpg", "TUỔI TRẺ"),
    # Scene 04: Adjacent dup + Công Phượng
    "Tin_04_4.jpg": ("url", "https://cdnphoto.dantri.com.vn/3W6q8AXaicBfYQEUQvOk3TW_Esc=/thumb_w/1020/2026/11/21/91636813615051656215867976517213770345737337n-1795269114812.jpg", "DÂN TRÍ"),
    "Tin_04_11.jpg": ("url", "https://images2.thanhnien.vn/528068263637045248/2026/10/22/cong-phuong-01-tpdn-1792650099713605292842.jpeg", "THANH NIÊN"),
    # Scene 05: Ninh Bình V-League
    "Tin_05_9.jpg": ("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/21/bia-8-1-17952684444251049430774.jpg", "THANH NIÊN"),
    # Scene 06: U17 VN
    "Tin_06_9.jpg": ("url", "https://i1-thethao.vnecdn.net/2026/11/21/IMG-6616-3001-1795256854.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=EUVmzdNwF5u1LREjNsZmIw", "VNEXPRESS"),
    # Scene 07: CAHN FC
    "Tin_07_9.jpg": ("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/21/81222402616683429615368702912982825507861103n-1795257148392887621472.jpg", "THANH NIÊN"),
    # Scene 08: Adjacent dup Quang Liêm
    "Tin_08_2.jpg": ("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/20/91616462815711706441323192638443400349788233n-17951979092701279880446.jpg", "THANH NIÊN"),
    # Scene 09: ĐNA 2027
    "Tin_09_2.jpg": ("url", "https://cdnphoto.dantri.com.vn/3l312QS7RyRnoacu6C3jwfdoFTQ=/thumb_w/1020/2026/11/21/img17951805073731795181994940-2048x1236-edited-1795244308936.jpg", "DÂN TRÍ / VFF"),
    # Scene 13: Bournemouth
    "Tin_13_11.jpg": ("ddgs", "AFC Bournemouth players celebrating goal Premier League", "BBC SPORT"),
    # Scene 15: PSG
    "Tin_15_7.jpg": ("ddgs", "Paris Saint Germain PSG players Ligue 1 stadium match", "REUTERS"),
    # Scene 16: AS Roma, RB Leipzig, Borussia Dortmund
    "Tin_16_6.jpg": ("ddgs", "AS Roma players Serie A Stadio Olimpico celebration", "AS ROMA"),
    "Tin_16_8.jpg": ("ddgs", "RB Leipzig Red Bull Arena football players action", "BUNDESLIGA"),
    "Tin_16_9.jpg": ("ddgs", "Borussia Dortmund players yellow jersey Signal Iduna Park celebration", "BUNDESLIGA"),
    # Scene 17: Inter Miami
    "Tin_17_9.jpg": ("ddgs", "Inter Miami CF stadium Chase Stadium soccer match", "MLS"),
    # Scene 18: Adjacent dup ATP Finals
    "Tin_18_4.jpg": ("url", "https://cdnphoto.dantri.com.vn/CgV5RY9hBAMQG-kmUtKicsOSqWQ=/thumb_w/1020/2026/11/22/zverev-1795299868170.jpg", "DÂN TRÍ / GETTY"),
    # Scene 20: Jiri Prochazka clean fight photo
    "Tin_20_6.jpg": ("ddgs", "Jiri Prochazka fighting octagon MMA UFC", "UFC"),
    # Scene 23: Chelsea Stamford Bridge clean photo
    "Tin_23_12.jpg": ("ddgs", "Stamford Bridge Chelsea football stadium London", "GUARDIAN"),
}

# Các ảnh cần cắt sạch viền đáy logo báo chí / watermark góc
TRIM_BOTTOM: Dict[str, float] = {
    "Tin_00_1.jpg": 0.08,
    "Tin_00_6.jpg": 0.08,
    "Tin_01_1.jpg": 0.08,
    "Tin_01_3.jpg": 0.08,
    "Tin_01_5.jpg": 0.08,
    "Tin_01_6.jpg": 0.08,
    "Tin_01_7.jpg": 0.08,
    "Tin_01_9.jpg": 0.08,
    "Tin_05_10.jpg": 0.09,
    "Tin_07_7.jpg": 0.08,
    "Tin_09_7.jpg": 0.09,
    "Tin_15_11.jpg": 0.08,
    "Tin_23_3.jpg": 0.08,
    "Tin_23_13.jpg": 0.08,
}


def main() -> None:
    curator = prep22.ImageCurator22()

    plan_path = OUT_DIR / "image_plan.json"
    credits_path = OUT_DIR / "image_credits.json"
    thethao_path = OUT_DIR / "thethao.json"
    intro_path = OUT_DIR / "intro_hook.json"

    plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
    records: List[Dict[str, Any]] = plan_data["records"]
    credits: Dict[str, str] = json.loads(credits_path.read_text(encoding="utf-8"))
    thethao: List[Dict[str, Any]] = json.loads(thethao_path.read_text(encoding="utf-8"))
    intro: Dict[str, Any] = json.loads(intro_path.read_text(encoding="utf-8"))

    by_scene: Dict[int, List[Dict[str, Any]]] = {}
    for rec in records:
        fn = rec["file_name"]
        fp = IMG_DIR / fn

        if fn in REPLACEMENTS:
            kind, val, new_credit = REPLACEMENTS[fn]
            slot_stub = {
                "type": rec["type"],
                "sentence_idx": rec["sentence_idx"],
                "sources": [(kind, val)],
                "credit": new_credit,
                "desc": rec["description"],
            }
            img, info, is_fb = curator.acquire_slot(int(rec["scene_id"]), 99, slot_stub)
            if img is not None:
                img.save(fp, format="JPEG", quality=95, optimize=True)
                rec["dimensions"] = f"{img.width}x{img.height} r={img.width / img.height:.2f}"
                rec["credit"] = new_credit
                credits[fn] = new_credit
                print(f"[REPLACED] {fn} -> {info} ({rec['dimensions']})")
            else:
                print(f"[WARN] Không thay được {fn}: {info}")

        if fn in TRIM_BOTTOM and fp.exists():
            with Image.open(fp) as im:
                trimmed = trim_edge_margins(im.convert("RGB"), bottom_frac=TRIM_BOTTOM[fn])
                trimmed.save(fp, format="JPEG", quality=95, optimize=True)
                rec["dimensions"] = f"{trimmed.width}x{trimmed.height} r={trimmed.width / trimmed.height:.2f}"
                print(f"[TRIMMED] {fn} -> {rec['dimensions']}")

        by_scene.setdefault(int(rec["scene_id"]), []).append(rec)

    # Xuất lại toàn bộ Contact Sheets của các cảnh có chỉnh sửa + overview
    touched_scenes = set()
    for fn in list(REPLACEMENTS.keys()) + list(TRIM_BOTTOM.keys()):
        m = re.match(r"Tin_(\d+)_", fn)
        if m:
            touched_scenes.add(int(m.group(1)))

    entry_map: Dict[int, Dict[str, Any]] = {0: intro}
    for it in thethao:
        entry_map[int(it["id"])] = it

    overview_records: List[Dict[str, Any]] = []
    for sc_id in sorted(by_scene.keys()):
        recs = by_scene[sc_id]
        for ov in recs[:2]:
            overview_records.append(ov)
        if sc_id in touched_scenes and sc_id in entry_map:
            ent = entry_map[sc_id]
            sheet_name = "contact_scene_00_intro.jpg" if sc_id == 0 else f"contact_scene_{sc_id:02d}.jpg"
            sheet_title = ent.get("group") if sc_id == 0 else ent.get("title", "")
            prep22.render_scene_contact_sheet(
                sc_id,
                str(sheet_title or ""),
                str(ent.get("news_source") or ent.get("source") or ""),
                f"{ent.get('voice_preset', '')} ({ent.get('voice', '')})",
                recs,
                QA_DIR / sheet_name,
            )

    prep22.render_overview_sheet(overview_records, len(thethao), QA_DIR / "contact_overview.jpg")

    plan_path.write_text(json.dumps({"total_slots": len(records), "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    credits_path.write_text(json.dumps(credits, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] Hoàn tất sửa {len(REPLACEMENTS)} ảnh thay thế & {len(TRIM_BOTTOM)} ảnh cắt viền.")


if __name__ == "__main__":
    main()
