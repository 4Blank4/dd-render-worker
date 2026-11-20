#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_daily_19_11_qa.py — Pha 1 (QA Fix & Polish):
Cắt viền logo báo chí ở mép ảnh và thay thế toàn bộ các ảnh bị watermark,
sai ngữ cảnh, đồ họa rối hoặc e-commerce đã phát hiện trên Contact Sheet 19.11.2026.
Xuất lại Contact Sheet từng cảnh bị sửa + bảng tổng hợp qa/contact_fixed_19_11.jpg.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from daily_19_11_data import (
    DAILY_18,
    DT_CATP_1,
    INTRO_DATA,
    NEWS_SPECS,
    TN_BONGBAN_1,
    TN_BONGBAN_2,
    TN_BONGBAN_3,
    TN_DINHBAC_17,
    TN_DINHBAC_2G,
    TN_QC_2,
    TN_QC_5,
    TN_ROLAND_1,
    TN_U17_ASPIRE_1,
    TN_XUANHOA_2,
    WEEKLY_16,
)
from diemdoc.log import banner, ok, step, warn
from diemdoc.publisher import load_voice_preset
from prepare_daily_19_11 import (
    DAY_DIR,
    IMG_DIR,
    QA_DIR,
    ImageCurator,
    ahash,
    hamming,
    is_blocked_url,
    render_overview_sheet,
    render_scene_contact_sheet,
    _load_fonts,
)

# Cắt viền sạch cho các ảnh gốc chất lượng cao có chữ báo nhỏ ở mép
CROPS: Dict[str, Tuple[float, float, float, float]] = {
    "Tin_00_1.jpg": (0.0, 0.0, 1.0, 0.94),
    "Tin_03_1.jpg": (0.0, 0.0, 1.0, 0.94),
    "Tin_04_12.jpg": (0.0, 0.0, 1.0, 0.93),
    "Tin_16_11.jpg": (0.10, 0.0, 0.90, 1.0),
    "Tin_17_4.jpg": (0.0, 0.0, 1.0, 0.92),
}

# Các slot cần thay ảnh mới hoàn toàn (không lấy lại ảnh cũ trong cùng scene)
REPLACEMENTS: Dict[str, Tuple[List[Tuple[str, str]], str]] = {
    "Tin_01_11.jpg": (
        [
            ("local", str(WEEKLY_16 / "Tin_17_1.jpg")),
            ("ddgs", "Vietnam national soccer team training pitch players"),
            ("ddgs", "Cong An Ha Noi V-League soccer match"),
        ],
        "THANH NIÊN",
    ),
    "Tin_01_12.jpg": (
        [
            ("local", str(DAILY_18 / "Tin_01_6.jpg")),
            ("local", str(DAILY_18 / "Tin_02_10.jpg")),
            ("ddgs", "Vietnam soccer team player Kyrgyzstan match"),
        ],
        "THANH NIÊN",
    ),
    "Tin_01_19.jpg": (
        [
            ("local", str(DAILY_18 / "Tin_02_5.jpg")),
            ("local", str(WEEKLY_16 / "Tin_17_6.jpg")),
            ("ddgs", "Nguyen Dinh Bac Vietnam football celebration"),
        ],
        "THANH NIÊN",
    ),
    "Tin_02_11.jpg": (
        [
            ("local", str(DAILY_18 / "Tin_03_8.jpg")),
            ("ddgs", "Vietnam national soccer team lineup stadium match"),
            ("ddgs", "Asian Cup AFC soccer match stadium"),
        ],
        "THANH NIÊN",
    ),
    "Tin_02_12.jpg": (
        [
            ("local", str(DAILY_18 / "Tin_03_10.jpg")),
            ("ddgs", "FIFA World Cup draw stage ceremony trophy"),
            ("ddgs", "AFC Asian Qualifiers soccer match action"),
        ],
        "FIFA / AFC",
    ),
    "Tin_03_11.jpg": (
        [
            ("url", DT_CATP_1),
            ("local", str(DAILY_18 / "Tin_12_5.jpg")),
            ("ddgs", "V-League Vietnam soccer goal celebration players"),
        ],
        "DÂN TRÍ / THANH NIÊN",
    ),
    "Tin_03_16.jpg": (
        [
            ("local", str(DAILY_18 / "Tin_12_6.jpg")),
            ("local", str(DAILY_18 / "Tin_12_7.jpg")),
            ("ddgs", "Binh Duong stadium Vietnam soccer match"),
        ],
        "THANH NIÊN",
    ),
    "Tin_04_8.jpg": (
        [
            ("local", str(DAILY_18 / "Tin_12_4.jpg")),
            ("ddgs", "Johor Darul Tazim AFC Champions League soccer match"),
            ("ddgs", "AFC Champions League Elite soccer match action"),
        ],
        "AFC",
    ),
    "Tin_04_14.jpg": (
        [
            ("ddgs", "Hang Day stadium Hanoi soccer fans crowd"),
            ("ddgs", "Vietnam soccer fans red flags stadium cheering"),
            ("local", str(WEEKLY_16 / "Tin_18_1.jpg")),
        ],
        "THANH NIÊN",
    ),
    "Tin_05_11.jpg": (
        [
            ("url", TN_ROLAND_1),
            ("ddgs", "Cristiano Roland U17 Vietnam soccer coach"),
            ("ddgs", "U17 Vietnam national soccer team training"),
        ],
        "THANH NIÊN / VFF",
    ),
    "Tin_05_17.jpg": (
        [
            ("ddgs", "Aspire Zone Doha Qatar sports complex stadium"),
            ("ddgs", "Qatar soccer training pitch Aspire Academy"),
            ("url", TN_U17_ASPIRE_1),
        ],
        "THANH NIÊN / FIFA",
    ),
    "Tin_06_12.jpg": (
        [
            ("ddgs", "Vietnam youth soccer goalkeeper save training"),
            ("ddgs", "soccer goalkeeper diving save pitch match"),
            ("local", str(DAILY_18 / "Tin_01_8.jpg")),
        ],
        "VFF / THANH NIÊN",
    ),
    "Tin_07_6.jpg": (
        [
            ("ddgs", "Argentina national soccer team fans Buenos Aires"),
            ("ddgs", "Lionel Messi Argentina Copa America trophy celebration"),
            ("local", str(DAILY_18 / "Tin_07_1.jpg")),
        ],
        "AP PHOTO",
    ),
    "Tin_08_8.jpg": (
        [
            ("ddgs", "Lamine Yamal Spain Euro 2024 celebration"),
            ("ddgs", "Lamine Yamal Barcelona Champions League match"),
            ("ddgs", "Kylian Mbappe Real Madrid goal celebration"),
        ],
        "REUTERS",
    ),
    "Tin_09_11.jpg": (
        [
            ("ddgs", "Jonny Evans Manchester United training Carrington"),
            ("ddgs", "Manchester United coaching staff Old Trafford bench"),
            ("ddgs", "Erik ten Hag Ruud van Nistelrooy Manchester United"),
        ],
        "REUTERS",
    ),
    "Tin_09_14.jpg": (
        [
            ("ddgs", "Manchester United players Premier League pitch action"),
            ("ddgs", "Bruno Fernandes Manchester United Old Trafford"),
            ("ddgs", "Manchester United team lineup Premier League"),
        ],
        "REUTERS",
    ),
    "Tin_13_2.jpg": (
        [
            ("ddgs", "Indonesia futsal team players court match"),
            ("ddgs", "Erick Thohir PSSI Jakarta press conference"),
            ("ddgs", "Indonesia national soccer team press conference"),
        ],
        "ANTARA / AFC",
    ),
    "Tin_13_8.jpg": (
        [
            ("ddgs", "AFC Futsal Asian Cup Indonesia match action"),
            ("ddgs", "futsal match indoor court stadium Asia"),
            ("ddgs", "Indonesia Liga 1 soccer match pitch"),
        ],
        "AFC",
    ),
    "Tin_13_12.jpg": (
        [
            ("ddgs", "PSSI Erick Thohir Indonesia soccer federation"),
            ("ddgs", "Jakarta Indonesia national soccer team match"),
            ("ddgs", "Indonesia football fans red jersey stadium"),
        ],
        "REUTERS",
    ),
    "Tin_13_13.jpg": (
        [
            ("ddgs", "Erick Thohir Indonesia minister sports event"),
            ("ddgs", "Erick Thohir speaking microphone press conference"),
            ("ddgs", "PSSI Jakarta Indonesia press conference"),
        ],
        "ANTARA",
    ),
    "Tin_15_5.jpg": (
        [
            ("ddgs", "Daniil Medvedev ATP tennis serve match"),
            ("ddgs", "Daniil Medvedev ATP Finals Turin tennis"),
            ("ddgs", "Carlos Alcaraz ATP Finals Turin court"),
        ],
        "ATP TOUR",
    ),
    "Tin_16_9.jpg": (
        [
            ("ddgs", "Vietnam athlete gold medal podium SEA Games celebration"),
            ("ddgs", "Vovinam martial arts gold medal Vietnam"),
            ("ddgs", "athlete biting gold medal podium celebration"),
        ],
        "TUỔI TRẺ",
    ),
    "Tin_16_13.jpg": (
        [
            ("ddgs", "badminton tournament indoor arena court match"),
            ("ddgs", "badminton championship podium Vietnam"),
            ("ddgs", "Ho Chi Minh City indoor sports arena badminton"),
        ],
        "TUỔI TRẺ",
    ),
    "Tin_17_3.jpg": (
        [
            ("ddgs", "Vietnam table tennis player match SEA Games"),
            ("ddgs", "table tennis tournament Asian championship match"),
            ("ddgs", "Nguyen Anh Tu Vietnam table tennis"),
        ],
        "THANH NIÊN",
    ),
    "Tin_17_5.jpg": (
        [
            ("ddgs", "table tennis doubles match indoor sports hall"),
            ("ddgs", "table tennis players medal podium tournament"),
            ("ddgs", "ping pong championship arena match"),
        ],
        "THANH NIÊN",
    ),
    "Tin_18_2.jpg": (
        [
            ("ddgs", "Dylan Kerr coach soccer manager"),
            ("ddgs", "Hai Phong FC V-League soccer match"),
            ("ddgs", "V-League Vietnam soccer coach touchline"),
        ],
        "V-LEAGUE",
    ),
    "Tin_18_9.jpg": (
        [
            ("ddgs", "Dylan Kerr Gor Mahia soccer coach"),
            ("ddgs", "Lach Tray stadium Hai Phong soccer match"),
            ("ddgs", "Vietnam V-League football players celebration"),
        ],
        "V-LEAGUE",
    ),
}


def render_fixed_summary_sheet(changed_files: List[Tuple[str, str, str]], out_path: Path) -> None:
    cols = 5
    rows = (len(changed_files) + cols - 1) // cols
    cell_w, cell_h, header_h = 390, 270, 76
    canvas = Image.new("RGB", (cols * cell_w + 30, rows * cell_h + header_h + 20), (8, 12, 22))
    draw = ImageDraw.Draw(canvas)
    f_hdr, f_sub, f_lbl, f_cap = _load_fonts()

    draw.text((20, 14), f"QA FIX SUMMARY — {len(changed_files)} ẢNH ĐÃ CẮT VIỀN / THAY MỚI (19.11.2026)", fill=(0, 229, 255), font=f_hdr)
    draw.text((20, 48), "Kiểm chứng lại toàn bộ ảnh sau khi xử lý logo góc, watermark và ảnh lệch chủ đề", fill=(190, 208, 228), font=f_sub)

    for idx, (fname, action_tag, credit) in enumerate(changed_files):
        r, c = divmod(idx, cols)
        x0 = 15 + c * cell_w + 6
        y0 = header_h + r * cell_h + 6
        draw.rectangle([x0 - 2, y0 - 2, x0 + 372, y0 + 252], outline=(0, 180, 216), width=2, fill=(16, 22, 36))
        p = IMG_DIR / fname
        with Image.open(p) as raw_im:
            im_rgb = raw_im.convert("RGB")
            sz = f"{im_rgb.width}x{im_rgb.height}"
            im_rgb.thumbnail((364, 198), Image.Resampling.LANCZOS)
            canvas.paste(im_rgb, (x0 + (370 - im_rgb.width) // 2, y0 + (202 - im_rgb.height) // 2))
        draw.text((x0 + 8, y0 + 208), f"{fname} • {sz} [{action_tag}]", fill=(0, 229, 255), font=f_lbl)
        draw.text((x0 + 8, y0 + 230), f"Nguồn: {credit}", fill=(250, 204, 21), font=f_cap)

    canvas.save(out_path, format="JPEG", quality=92)


def main() -> None:
    banner("PHA 1 (QA FIX) — CẮT VIỀN LOGO & THAY MỚI ẢNH LỖI 19.11.2026")
    curator = ImageCurator()

    plan_path = DAY_DIR / "image_plan.json"
    credits_path = DAY_DIR / "image_credits.json"
    plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
    records: List[Dict[str, Any]] = plan_data.get("records", [])
    credits_map: Dict[str, str] = json.loads(credits_path.read_text(encoding="utf-8"))

    # Thu thập hash các ảnh sạch giữ nguyên trong từng scene để không trùng khi thay thế
    scene_hashes: Dict[int, List[int]] = {}
    for rec in records:
        fn = rec["file_name"]
        sc_id = int(rec["scene_id"])
        if fn in REPLACEMENTS:
            continue
        p = IMG_DIR / fn
        if p.exists():
            with Image.open(p) as im:
                scene_hashes.setdefault(sc_id, []).append(ahash(im.convert("RGB")))

    changed_summary: List[Tuple[str, str, str]] = []
    dirty_scenes: set[int] = set()

    # 1. Cắt viền logo mép ảnh
    for fn, (x0f, y0f, x1f, y1f) in CROPS.items():
        p = IMG_DIR / fn
        if not p.exists():
            warn(f"Không thấy {fn} để crop")
            continue
        with Image.open(p) as raw_im:
            im = raw_im.convert("RGB")
            w, h = im.size
            cropped = im.crop((int(w * x0f), int(h * y0f), int(w * x1f), int(h * y1f)))
        cropped.save(p, format="JPEG", quality=94, optimize=True)
        dims = f"{cropped.width}x{cropped.height}"
        for rec in records:
            if rec["file_name"] == fn:
                rec["dimensions"] = dims
                dirty_scenes.add(int(rec["scene_id"]))
                changed_summary.append((fn, "CROPPED", rec.get("credit", "")))
                break
        ok(f"[Crop] {fn} -> {dims}")

    # 2. Thay mới các ảnh sai chủ đề / dính watermark
    for fn, (sources, new_credit) in REPLACEMENTS.items():
        rec_match = next((r for r in records if r["file_name"] == fn), None)
        if not rec_match:
            warn(f"Không thấy record cho {fn}")
            continue
        sc_id = int(rec_match["scene_id"])
        seen = scene_hashes.setdefault(sc_id, [])
        chosen_im: Optional[Image.Image] = None

        for kind, val in sources:
            if kind == "local":
                im = curator.try_local(val, seen)
                if im is not None:
                    chosen_im = im
                    break
            elif kind == "url":
                im = curator.fetch_url_image(val, check_overlay=False)
                if im is not None:
                    h_val = ahash(im)
                    if not any(hamming(h_val, eh) <= 6 for eh in seen):
                        chosen_im = im
                        break
            elif kind == "ddgs":
                results = curator.search_ddgs(val)
                for r in results:
                    u = r.get("image") or ""
                    if not u or u in curator.used_ddgs_urls or is_blocked_url(u):
                        continue
                    im = curator.fetch_url_image(u, check_overlay=True)
                    if im is None:
                        continue
                    h_val = ahash(im)
                    if any(hamming(h_val, eh) <= 6 for eh in seen):
                        continue
                    curator.used_ddgs_urls.add(u)
                    chosen_im = im
                    break
                if chosen_im is not None:
                    break

        if chosen_im is None:
            raise RuntimeError(f"Không tìm được ảnh thay thế đạt chuẩn cho {fn}")

        dest = IMG_DIR / fn
        chosen_im.save(dest, format="JPEG", quality=94, optimize=True)
        seen.append(ahash(chosen_im))
        dims = f"{chosen_im.width}x{chosen_im.height}"
        rec_match["dimensions"] = dims
        rec_match["credit"] = new_credit
        credits_map[fn] = new_credit
        dirty_scenes.add(sc_id)
        changed_summary.append((fn, "REPLACED", new_credit))
        ok(f"[Replace] {fn} ({dims}) | {new_credit}")

    # Cập nhật metadata JSON & Contact Sheets của các scene đã sửa
    plan_data["records"] = records
    plan_path.write_text(json.dumps(plan_data, ensure_ascii=False, indent=2), encoding="utf-8")
    credits_path.write_text(json.dumps(credits_map, ensure_ascii=False, indent=2), encoding="utf-8")

    p_male = load_voice_preset("primary")
    p_female = load_voice_preset("secondary")
    all_specs = [INTRO_DATA] + NEWS_SPECS
    overview_entries: List[Tuple[int, str, Path]] = []

    for spec in all_specs:
        sc_id = int(spec["id"])
        sc_recs = [r for r in records if int(r["scene_id"]) == sc_id]
        if sc_recs:
            overview_entries.append((sc_id, spec["title"] or spec["group"], IMG_DIR / sc_recs[0]["file_name"]))
        if sc_id in dirty_scenes:
            if sc_id == 0:
                v_label = "Song giọng Nữ (Ngọc Huyền) + Nam (Minh Quân Pro)"
            elif sc_id % 2 == 1:
                v_label = p_male["voice_id"]
            else:
                v_label = p_female["voice_id"]
            qa_name = "contact_scene_00_intro.jpg" if sc_id == 0 else f"contact_scene_{sc_id:02d}.jpg"
            render_scene_contact_sheet(sc_id, spec["title"] or spec["group"], v_label, sc_recs, QA_DIR / qa_name)
            ok(f"[QA Sheet] Đã cập nhật {qa_name}")

    if overview_entries:
        render_overview_sheet(overview_entries, QA_DIR / "contact_overview.jpg")
    if changed_summary:
        render_fixed_summary_sheet(changed_summary, QA_DIR / "contact_fixed_19_11.jpg")
        ok(f"Đã xuất bảng đối chứng sau sửa lỗi -> {QA_DIR / 'contact_fixed_19_11.jpg'}")


if __name__ == "__main__":
    main()
