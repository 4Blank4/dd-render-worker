#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_weekly_16_11_qa.py — Bước 1 Giai đoạn 2:
Sửa triệt để toàn bộ ảnh lỗi phát hiện khi kiểm duyệt 27 bảng Contact Sheet tuần 16.11.2026:
- Nhóm A: Cắt bỏ sạch viền chứa logo báo chí/nút mạng xã hội ở mép ảnh (lưu bản gốc raw_backups để idempotent).
- Nhóm B: Thay thế hoàn toàn ảnh dính watermark giữa ảnh, bảng biểu infographic, poster chữ, ảnh ghép, sai người/môn.
- Cập nhật image_credits.json, image_plan.json, thethao.json, intro_hook.json và tái xuất Contact Sheet QA.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc.log import banner, ok, step, warn
from diemdoc.publisher import load_voice_preset
from prepare_weekly_16_11 import (
    CACHE_DIR,
    DAY_DIR,
    IMG_DIR,
    QA_DIR,
    ImageCurator,
    ahash,
    hamming,
    has_getty_watermark,
    is_blocked_url,
    passes_visual_stats,
    render_overview_sheet,
    render_scene_contact_sheet,
)

RAW_BACKUP_DIR = CACHE_DIR / "raw_backups"
ORTHER = Path(_ROOT) / "outputs" / "Orther"
DAY_09 = Path(_ROOT) / "outputs" / "09.11.2026"

# Nhóm A: Cắt mép ảnh sạch (l, t, r, b) theo tỷ lệ [0..1]
GROUP_A_CROPS: Dict[str, Tuple[float, float, float, float]] = {
    "Tin_00_12.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_11_11.jpg": (0.0, 0.0, 0.0, 0.085),
    "Tin_15_9.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_15_11.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_16_1.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_16_2.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_16_3.jpg": (0.0, 0.0, 0.0, 0.22),  # Loại bỏ dải CHAMPIONS + THANH NIÊN ở đáy
    "Tin_16_4.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_16_5.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_16_8.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_16_9.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_16_10.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_16_11.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_1.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_2.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_3.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_4.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_5.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_6.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_7.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_8.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_9.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_10.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_17_11.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_18_8.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_18_10.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_18_11.jpg": (0.0, 0.0, 0.0, 0.08),
    "Tin_19_4.jpg": (0.0, 0.0, 0.0, 0.095),
    "Tin_20_4.jpg": (0.0, 0.0, 0.0, 0.105),
    "Tin_20_6.jpg": (0.0, 0.15, 0.0, 0.0),   # Cắt logo góc trên phải (đủ headroom an toàn)
    "Tin_20_8.jpg": (0.13, 0.0, 0.0, 0.0),   # Cắt logo Canon góc trên trái không chạm đầu cầu thủ
    "Tin_21_11.jpg": (0.0, 0.0, 0.0, 0.145),
    "Tin_24_7.jpg": (0.0, 0.0, 0.0, 0.105),
    "Tin_24_8.jpg": (0.0, 0.08, 0.0, 0.115),
    "Tin_25_3.jpg": (0.0, 0.0, 0.0, 0.10),
}

# Nhóm B: Thay thế hoàn toàn các ảnh sai ngữ cảnh / infographic / poster / watermark giữa ảnh
GROUP_B_REPLACEMENTS: Dict[str, Dict[str, Any]] = {
    "Tin_01_11.jpg": {
        "credit": "FA / REUTERS",
        "sources": [
            ("local", str(ORTHER / "16.11.2026" / "images" / "v3_tuchel_touch.jpg")),
            ("ddgs", "Thomas Tuchel England manager touchline Wembley"),
        ],
    },
    "Tin_02_4.jpg": {
        "credit": "UEFA / BRAGA",
        "sources": [
            ("ddgs", "Estadio Municipal de Braga stadium quarry rock wall match"),
            ("ddgs", "Braga stadium Portugal night aerial view"),
        ],
    },
    "Tin_02_5.jpg": {
        "credit": "UEFA / REUTERS",
        "sources": [
            ("ddgs", "Bruno Fernandes Portugal national team match action 2024"),
            ("ddgs", "Portugal national football team lineup stadium pitch"),
        ],
    },
    "Tin_04_8.jpg": {
        "credit": "KNVB / REUTERS",
        "sources": [
            ("ddgs", "Jurrien Timber Netherlands national team orange shirt match"),
            ("ddgs", "Netherlands football team orange goal celebration pitch"),
        ],
    },
    "Tin_04_12.jpg": {
        "credit": "KNVB / DIARIO AS",
        "sources": [
            ("ddgs", "Netherlands national football team team huddle orange pitch"),
            ("ddgs", "Xavi Hernandez press conference suit portrait -barcelona -badge"),
        ],
    },
    "Tin_05_4.jpg": {
        "credit": "REUTERS",
        "sources": [
            ("ddgs", "Argentina national football team 2024 match pitch action"),
            ("ddgs", "Julian Alvarez Argentina national team match action"),
        ],
    },
    "Tin_06_8.jpg": {
        "credit": "JFA / REUTERS",
        "sources": [
            ("ddgs", "Japan national football team Samurai Blue celebration blue jersey"),
            ("ddgs", "Tatsuhiro Sakamoto Japan national team blue shirt"),
        ],
    },
    "Tin_06_9.jpg": {
        "credit": "AP PHOTO",
        "sources": [
            ("ddgs", "Raphinha Brazil national football team match yellow shirt"),
            ("ddgs", "Brazil national football team players protest referee match"),
        ],
    },
    "Tin_07_5.jpg": {
        "credit": "FA / UEFA",
        "sources": [
            ("ddgs", "Wembley Stadium England fans flags crowd match night"),
            ("ddgs", "England football team Wembley crowd stadium pitch"),
        ],
    },
    "Tin_07_9.jpg": {
        "credit": "FA / REUTERS",
        "sources": [
            ("ddgs", "Harry Kane England captain Wembley applause waving pitch"),
            ("ddgs", "Harry Kane England national team jersey celebration Wembley"),
        ],
    },
    "Tin_08_3.jpg": {
        "credit": "REUTERS",
        "sources": [
            ("local", str(ORTHER / "11.11.2026" / "images" / "Tin_06_1.jpg")),
            ("local", str(ORTHER / "11.11.2026" / "images" / "Tin_01_12.jpg")),
        ],
    },
    "Tin_08_9.jpg": {
        "credit": "PREMIER LEAGUE / REUTERS",
        "sources": [
            ("ddgs", "Manchester United vs Liverpool Old Trafford Premier League action"),
            ("local", str(DAY_09 / "images" / "Tin_01_2.jpg")),
        ],
    },
    "Tin_08_10.jpg": {
        "credit": "REUTERS",
        "sources": [
            ("ddgs", "Paul Merson football pundit suit interview -sky -banner"),
            ("local", str(ORTHER / "11.11.2026" / "images" / "Tin_01_10.jpg")),
        ],
    },
    "Tin_08_11.jpg": {
        "credit": "MAN UTD / REUTERS",
        "sources": [
            ("ddgs", "Rio Ferdinand portrait studio pundit -sky -logo"),
            ("local", str(ORTHER / "11.11.2026" / "images" / "Tin_06_4.jpg")),
        ],
    },
    "Tin_09_3.jpg": {
        "credit": "REUTERS",
        "sources": [
            ("local", str(ORTHER / "16.11.2026" / "images" / "v3_kane_cel.jpg")),
            ("ddgs", "Harry Kane England striker celebration goal Wembley"),
        ],
    },
    "Tin_09_9.jpg": {
        "credit": "REUTERS / ARCHIVE",
        "sources": [
            ("local", str(ORTHER / "12.11.2026" / "images" / "Tin_03_4.jpg")),
            ("ddgs", "Cristiano Ronaldo Lionel Messi Argentina Portugal match together"),
        ],
    },
    "Tin_10_1.jpg": {
        "credit": "FC BARCELONA / REUTERS",
        "sources": [
            ("ddgs", "Pau Cubarsi Barcelona defender Champions League action"),
            ("ddgs", "Pau Cubarsi Spain national team football"),
        ],
    },
    "Tin_11_3.jpg": {
        "credit": "REAL MADRID CF / REUTERS",
        "sources": [
            ("ddgs", "Real Madrid men football team celebration Santiago Bernabeu"),
            ("ddgs", "Real Madrid players hugging goal Santiago Bernabeu"),
        ],
    },
    "Tin_11_6.jpg": {
        "credit": "AFP / REUTERS",
        "sources": [
            ("ddgs", "Jose Mourinho Real Madrid touchline shouting match -getty"),
            ("ddgs", "Jose Mourinho coach Real Madrid bench stadium"),
        ],
    },
    "Tin_11_10.jpg": {
        "credit": "AP PHOTO",
        "sources": [
            ("ddgs", "Jose Mourinho Real Madrid press conference microphone -sk -logo"),
            ("ddgs", "Jose Mourinho manager celebration Real Madrid"),
        ],
    },
    "Tin_12_6.jpg": {
        "credit": "FC BARCELONA / REUTERS",
        "sources": [
            ("ddgs", "Lionel Messi Barcelona number 19 2006 young dribbling action"),
            ("ddgs", "Lionel Messi 2007 Barcelona Getafe goal young"),
        ],
    },
    "Tin_12_9.jpg": {
        "credit": "UEFA / FC BARCELONA",
        "sources": [
            ("ddgs", "Lamine Yamal Spain Euro 2024 trophy celebration medal"),
            ("ddgs", "Lamine Yamal Barcelona trophy celebration La Liga"),
        ],
    },
    "Tin_14_7.jpg": {
        "credit": "RAVENNA FC",
        "sources": [
            ("ddgs", "Ravenna FC stadium Stadio Bruno Benelli football pitch"),
            ("ddgs", "Serie C Italy football match stadium pitch celebration"),
        ],
    },
    "Tin_15_10.jpg": {
        "credit": "VFF / VNEXPRESS",
        "sources": [
            ("local", str(ORTHER / "13.11.2026" / "images" / "short_2_u23_lineup.jpg")),
            ("local", str(ORTHER / "11.11.2026" / "images" / "Tin_04_7.jpg")),
        ],
    },
    "Tin_16_6.jpg": {
        "credit": "VFF / ĐỨC CƯỜNG",
        "crop": (0.0, 0.0, 0.0, 0.075),
        "sources": [
            ("local", str(ORTHER / "11.11.2026" / "images" / "Tin_04_5.jpg")),
            ("ddgs", "U23 Viet Nam thi dau tran bong da san Pleiku"),
        ],
    },
    "Tin_16_7.jpg": {
        "credit": "VFF / KHÁNH VY",
        "crop": (0.0, 0.0, 0.0, 0.075),
        "sources": [
            ("local", str(ORTHER / "11.11.2026" / "images" / "Tin_04_6.jpg")),
            ("local", str(ORTHER / "11.11.2026" / "images" / "Tin_04_17.jpg")),
        ],
    },
    "Tin_18_2.jpg": {
        "credit": "THANH NIÊN / VFF",
        "crop": (0.0, 0.0, 0.0, 0.08),
        "sources": [
            ("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/14/90245124918031301109939638752536811766823148n-17946708341662110546405.jpg"),
            ("ddgs", "U17 Viet Nam tap luyen san bong da HLV Cristiano Roland"),
        ],
    },
    "Tin_18_6.jpg": {
        "credit": "FIFA / REUTERS",
        "sources": [
            ("ddgs", "Dominican Republic national football team match players"),
            ("ddgs", "Al Bayt Stadium Qatar World Cup pitch aerial"),
        ],
    },
    "Tin_18_9.jpg": {
        "credit": "THANH NIÊN / VFF",
        "crop": (0.0, 0.0, 0.0, 0.08),
        "sources": [
            ("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/14/doi-hinh-xuat-phat-cua-u17-viet-nam-truoc-panama-17946709182771468303340.jpg"),
            ("ddgs", "doi tuyen U17 Viet Nam thi dau bong da"),
        ],
    },
    "Tin_21_4.jpg": {
        "credit": "VNEXPRESS / ISSF",
        "sources": [
            ("local", str(ORTHER / "11.11.2026" / "images" / "Tin_03_11.jpg")),
            ("ddgs", "Trinh Thu Vinh xa thu ban sung thi dau Olympic"),
        ],
    },
    "Tin_21_6.jpg": {
        "credit": "REUTERS / ISSF",
        "sources": [
            ("ddgs", "Trinh Thu Vinh ban sung sung ngan Olympic Paris"),
            ("ddgs", "woman air pistol shooting Olympics finals target range"),
        ],
    },
    "Tin_21_9.jpg": {
        "credit": "AP PHOTO / ISSF",
        "sources": [
            ("ddgs", "Yang Ji-in shooting Olympic pistol champion gold medal"),
            ("ddgs", "ISSF World Championship shooting pistol women final action"),
        ],
    },
    "Tin_22_2.jpg": {
        "credit": "THANH NIÊN / LIÊN ĐOÀN CỜ TƯỚNG",
        "sources": [
            ("ddgs", "Lai Ly Huynh co tuong thi dau ban co"),
            ("ddgs", "ky thu Lai Ly Huynh co tuong Viet Nam"),
        ],
    },
    "Tin_22_5.jpg": {
        "credit": "LIÊN ĐOÀN CỜ TƯỚNG VN",
        "sources": [
            ("ddgs", "Phan Huy Hoang ky thu co tuong Viet Nam"),
            ("ddgs", "giai vo dich co tuong the gioi thi dau ban co go"),
        ],
    },
    "Tin_22_11.jpg": {
        "credit": "THANH NIÊN / VOV",
        "sources": [
            ("ddgs", "xiangqi Chinese chess tournament players board competition"),
            ("ddgs", "co tuong giai dau quoc te ky thu thi dau"),
        ],
    },
    "Tin_23_7.jpg": {
        "credit": "TOTAL CHESS / REUTERS",
        "sources": [
            ("ddgs", "Le Quang Liem chess tournament grandmaster playing"),
            ("ddgs", "Le Quang Liem Biel chess grandmaster board"),
        ],
    },
    "Tin_23_9.jpg": {
        "credit": "TOTAL CHESS / FIDE",
        "sources": [
            ("ddgs", "Le Quang Liem chess grandmaster thinking board match"),
            ("ddgs", "FIDE chess tournament hall grandmasters Budapest playing"),
        ],
    },
    "Tin_24_3.jpg": {
        "credit": "DÂN TRÍ / LIÊN ĐOÀN BÓNG BÀN VN",
        "sources": [
            ("ddgs", "Nguyen Anh Tu bong ban Viet Nam thi dau SEA Games"),
            ("ddgs", "table tennis championship final arena rally blue table"),
        ],
    },
    "Tin_25_1.jpg": {
        "credit": "THE NORTH FACE",
        "sources": [
            ("ddgs", "Stephanie Case runner ultramarathon mountains trail -collage -split"),
            ("ddgs", "Antarctic ultra marathon runner snow white landscape"),
        ],
    },
    "Tin_25_9.jpg": {
        "credit": "THE NORTH FACE / ANTARCTIC ULTRA",
        "sources": [
            ("ddgs", "Antarctica ice desert marathon runners snow blizzard"),
            ("ddgs", "Antarctic Ice Marathon runner cold snow landscape"),
        ],
    },
}


def apply_crop(im: Image.Image, crop_fracs: Tuple[float, float, float, float]) -> Image.Image:
    l_f, t_f, r_f, b_f = crop_fracs
    w, h = im.size
    x0 = int(round(w * l_f))
    y0 = int(round(h * t_f))
    x1 = int(round(w * (1.0 - r_f)))
    y1 = int(round(h * (1.0 - b_f)))
    cropped = im.crop((x0, y0, x1, y1))
    # Đảm bảo đạt chuẩn tối thiểu ngang >= 800x450 nếu bị hụt nhẹ sau crop
    cw, ch = cropped.size
    if cw < 800 or ch < 450:
        scale = max(800.0 / cw, 450.0 / ch)
        cropped = cropped.resize(
            (int(round(cw * scale)), int(round(ch * scale))),
            Image.Resampling.LANCZOS,
        )
    return cropped


def pick_replacement_image(
    curator: ImageCurator,
    fname: str,
    spec_entry: Dict[str, Any],
    scene_hashes: List[int],
) -> Image.Image:
    chosen: Optional[Image.Image] = None
    for kind, val in spec_entry["sources"]:
        if kind == "local":
            p = Path(val)
            if p.exists() and p.stat().st_size >= 18_000:
                with Image.open(p) as raw_im:
                    im = raw_im.convert("RGB")
                if "crop" in spec_entry:
                    im = apply_crop(im, spec_entry["crop"])
                ok_v, _ = passes_visual_stats(im, check_overlay=False)
                if ok_v and not has_getty_watermark(im, curator.template):
                    h = ahash(im)
                    if not any(hamming(h, eh) <= 5 for eh in scene_hashes):
                        chosen = im
                        break
        elif kind == "url":
            im = curator.fetch_url_image(val, check_overlay=False)
            if im is not None:
                if "crop" in spec_entry:
                    im = apply_crop(im, spec_entry["crop"])
                ok_v, _ = passes_visual_stats(im, check_overlay=False)
                h = ahash(im)
                if ok_v and not any(hamming(h, eh) <= 5 for eh in scene_hashes):
                    chosen = im
                    break
        elif kind == "ddgs":
            results = curator.search_ddgs(val)
            for r in results:
                u = r.get("image") or ""
                if not u or u in curator.used_urls or is_blocked_url(u):
                    continue
                im = curator.fetch_url_image(u, check_overlay=True)
                if im is None:
                    continue
                if "crop" in spec_entry:
                    im = apply_crop(im, spec_entry["crop"])
                ok_v, _ = passes_visual_stats(im, check_overlay=True)
                if not ok_v:
                    continue
                h = ahash(im)
                if any(hamming(h, eh) <= 5 for eh in scene_hashes):
                    continue
                curator.used_urls.add(u)
                chosen = im
                break
            if chosen is not None:
                break

    if chosen is None:
        raise RuntimeError(f"Không tìm được ảnh thay thế sạch cho {fname}")
    return chosen


def build_fixed_only_sheets(fixed_recs: List[Dict[str, Any]], out_dir: Path) -> List[Path]:
    """Tạo bảng QA tổng hợp chỉ chứa các ảnh vừa được cắt mép / thay thế để kiểm duyệt trực tiếp."""
    per_page = 28
    out_paths: List[Path] = []
    from prepare_weekly_16_11 import _load_fonts
    from PIL import ImageDraw

    f_hdr, f_sub, f_lbl, f_cap = _load_fonts()
    for p_idx in range(0, len(fixed_recs), per_page):
        batch = fixed_recs[p_idx : p_idx + per_page]
        cols = 4
        rows = (len(batch) + cols - 1) // cols
        cell_w, cell_h, header_h = 470, 360, 88
        canvas = Image.new("RGB", (cols * cell_w + 40, rows * cell_h + header_h + 24), (8, 12, 22))
        draw = ImageDraw.Draw(canvas)
        page_num = p_idx // per_page + 1
        total_pages = (len(fixed_recs) + per_page - 1) // per_page
        draw.text(
            (22, 14),
            f"QA KIỂM DUYỆT LẠI CÁC ẢNH ĐÃ SỬA (TRANG {page_num}/{total_pages})",
            fill=(0, 229, 255),
            font=f_hdr,
        )
        draw.text(
            (22, 50),
            f"Hiển thị {len(batch)}/{len(fixed_recs)} ảnh vừa Cắt viền logo [CROP] hoặc Thay mới [NEW]",
            fill=(190, 208, 228),
            font=f_sub,
        )
        for idx, rec in enumerate(batch):
            r, c = divmod(idx, cols)
            x0 = 20 + c * cell_w + 8
            y0 = header_h + r * cell_h + 8
            tag_color = (56, 189, 248) if rec["fix_tag"] == "CROP" else (34, 197, 94)
            draw.rectangle([x0 - 2, y0 - 2, x0 + 448, y0 + 342], outline=tag_color, width=2, fill=(16, 22, 36))
            with Image.open(IMG_DIR / rec["file_name"]) as raw_im:
                im_rgb = raw_im.convert("RGB")
                sz = f"{im_rgb.width}x{im_rgb.height} ({im_rgb.width / max(1, im_rgb.height):.2f})"
                im_rgb.thumbnail((440, 246), Image.Resampling.LANCZOS)
                canvas.paste(im_rgb, (x0 + (446 - im_rgb.width) // 2, y0 + (250 - im_rgb.height) // 2))
            draw.text((x0 + 8, y0 + 256), f"[{rec['fix_tag']}] {rec['file_name']} • {sz}", fill=(0, 229, 255), font=f_lbl)
            draw.text((x0 + 8, y0 + 280), f"Nguồn: {rec['credit'][:46]}", fill=(250, 204, 21), font=f_cap)
            desc = rec["description"]
            draw.text((x0 + 8, y0 + 302), desc[:56], fill=(225, 234, 246), font=f_cap)
            if len(desc) > 56:
                draw.text((x0 + 8, y0 + 320), desc[56:110], fill=(185, 198, 218), font=f_cap)
        out_p = out_dir / f"contact_fixed_page_{page_num:02d}.jpg"
        canvas.save(out_p, format="JPEG", quality=92)
        out_paths.append(out_p)
    return out_paths


def run_step1b() -> None:
    """Tinh chỉnh dứt điểm 12 ảnh còn sót từ kiểm duyệt contact_fixed_page_01..03.jpg."""
    banner("BƯỚC 1B GIAI ĐOẠN 2 — TINH CHỈNH DỨT ĐIỂM 12 ẢNH CÒN SÓT")
    STEP1B_BAK = CACHE_DIR / "step1b_backups"
    STEP1B_BAK.mkdir(parents=True, exist_ok=True)

    step1b_specs: Dict[str, Dict[str, Any]] = {
        "Tin_06_8.jpg": {
            "mode": "external",
            "path": IMG_DIR / "Tin_06_2.jpg",
            "crop": (0.08, 0.06, 0.04, 0.08),
            "credit": "AP PHOTO",
            "tag": "CROP",
        },
        "Tin_07_5.jpg": {
            "mode": "current",
            "crop": (0.0, 0.0, 0.0, 0.14),
            "credit": "FA / UEFA",
            "tag": "CROP",
        },
        "Tin_08_9.jpg": {
            "mode": "external",
            "path": DAY_09 / "images" / "Tin_08_9.jpg",
            "credit": "PREMIER LEAGUE / REUTERS",
            "tag": "NEW",
        },
        "Tin_11_3.jpg": {
            "mode": "external",
            "path": DAY_09 / "images" / "Tin_04_9.jpg",
            "credit": "REAL MADRID CF / REUTERS",
            "tag": "NEW",
        },
        "Tin_20_4.jpg": {
            "mode": "raw_backup",
            "crop": (0.0, 0.0, 0.0, 0.16),
            "credit": "FA THAILAND",
            "tag": "CROP",
        },
        "Tin_20_8.jpg": {
            "mode": "raw_backup",
            "crop": (0.18, 0.11, 0.0, 0.0),
            "credit": "KANCHANABURI POWER FC",
            "tag": "CROP",
        },
        "Tin_21_6.jpg": {
            "mode": "external",
            "path": ORTHER / "11.11.2026" / "images" / "Tin_03_1.jpg",
            "crop": (0.36, 0.04, 0.0, 0.18),
            "credit": "VNEXPRESS / ISSF",
            "tag": "NEW",
        },
        "Tin_21_9.jpg": {
            "mode": "current",
            "crop": (0.0, 0.0, 0.0, 0.14),
            "credit": "AP PHOTO / ISSF",
            "tag": "CROP",
        },
        "Tin_22_5.jpg": {
            "mode": "current",
            "crop": (0.0, 0.0, 0.0, 0.26),
            "credit": "LIÊN ĐOÀN CỜ TƯỚNG VN",
            "tag": "CROP",
        },
        "Tin_22_11.jpg": {
            "mode": "external",
            "path": ORTHER / "14.11.2026" / "images" / "s3_lailyhuynh_1.jpg",
            "crop": (0.0, 0.06, 0.0, 0.22),
            "credit": "THANH NIÊN / VOV",
            "tag": "NEW",
        },
        "Tin_24_8.jpg": {
            "mode": "raw_backup",
            "crop": (0.0, 0.14, 0.0, 0.17),
            "credit": "VNEXPRESS",
            "tag": "CROP",
        },
        "Tin_25_9.jpg": {
            "mode": "current",
            "crop": (0.0, 0.0, 0.0, 0.10),
            "credit": "THE NORTH FACE / ANTARCTIC ULTRA",
            "tag": "CROP",
        },
    }

    plan_path = DAY_DIR / "image_plan.json"
    credits_path = DAY_DIR / "image_credits.json"
    intro_path = DAY_DIR / "intro_hook.json"
    tt_path = DAY_DIR / "thethao.json"

    plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
    records: List[Dict[str, Any]] = plan_data["records"]
    credits_map: Dict[str, str] = json.loads(credits_path.read_text(encoding="utf-8"))
    intro_obj: Dict[str, Any] = json.loads(intro_path.read_text(encoding="utf-8"))
    news_objs: List[Dict[str, Any]] = json.loads(tt_path.read_text(encoding="utf-8"))

    rec_by_fn = {r["file_name"]: r for r in records}
    modified_scenes: set[int] = set()
    fixed_recs: List[Dict[str, Any]] = []

    for fn, sp in step1b_specs.items():
        dest = IMG_DIR / fn
        mode = sp["mode"]
        bak_1b = STEP1B_BAK / fn
        if mode == "current":
            if not bak_1b.exists() and dest.exists():
                shutil.copy2(dest, bak_1b)
            src_p = bak_1b
        elif mode == "raw_backup":
            src_p = RAW_BACKUP_DIR / fn
            if not src_p.exists():
                src_p = dest
        else:
            src_p = Path(sp["path"])

        with Image.open(src_p) as raw_im:
            im = raw_im.convert("RGB")
        if "crop" in sp:
            im = apply_crop(im, sp["crop"])
        ok_v, reason = passes_visual_stats(im, check_overlay=False)
        if not ok_v:
            raise RuntimeError(f"Step 1B {fn} không đạt chuẩn: {reason}")
        im.save(dest, format="JPEG", quality=94, optimize=True)
        ok(f"[1B-{sp['tag']}] {fn} -> {im.size} ({im.width / im.height:.2f}) | {sp['credit']}")

        rec = rec_by_fn[fn]
        rec["credit"] = sp["credit"]
        credits_map[fn] = sp["credit"]
        modified_scenes.add(int(rec["scene_id"]))
        fixed_recs.append({**rec, "fix_tag": sp["tag"]})

    credits_path.write_text(json.dumps(credits_map, ensure_ascii=False, indent=2), encoding="utf-8")
    plan_path.write_text(json.dumps({"total_slots": len(records), "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")

    scene_recs_map: Dict[int, List[Dict[str, Any]]] = {}
    for rec in records:
        scene_recs_map.setdefault(int(rec["scene_id"]), []).append(rec)

    p_male = load_voice_preset("primary")
    p_female = load_voice_preset("secondary")
    all_items = [intro_obj] + news_objs
    for it in all_items:
        sc_id = int(it["id"])
        if sc_id in modified_scenes:
            sc_recs = scene_recs_map.get(sc_id, [])
            is_intro = (sc_id == 0)
            v_lbl = (
                "Song giọng Nữ (Ngọc Huyền) + Nam (Minh Quân Pro)"
                if is_intro
                else (p_male["voice_id"] if sc_id % 2 == 1 else p_female["voice_id"])
            )
            qa_name = "contact_scene_00_intro.jpg" if is_intro else f"contact_scene_{sc_id:02d}.jpg"
            render_scene_contact_sheet(sc_id, it["title"], v_lbl, sc_recs, QA_DIR / qa_name)
            ok(f"Đã cập nhật QA: {qa_name}")

    # Xuất bảng 12 ảnh Step 1B để kiểm duyệt trực tiếp
    from prepare_weekly_16_11 import _load_fonts
    from PIL import ImageDraw

    f_hdr, f_sub, f_lbl, f_cap = _load_fonts()
    cols = 4
    rows = (len(fixed_recs) + cols - 1) // cols
    cell_w, cell_h, header_h = 470, 360, 88
    canvas = Image.new("RGB", (cols * cell_w + 40, rows * cell_h + header_h + 24), (8, 12, 22))
    draw = ImageDraw.Draw(canvas)
    draw.text((22, 14), "QA KIỂM DUYỆT DỨT ĐIỂM 12 ẢNH BƯỚC 1B", fill=(0, 229, 255), font=f_hdr)
    draw.text((22, 50), "Xác nhận sạch 100% logo/banner/nội dung trước khi Render", fill=(190, 208, 228), font=f_sub)
    for idx, rec in enumerate(fixed_recs):
        r, c = divmod(idx, cols)
        x0 = 20 + c * cell_w + 8
        y0 = header_h + r * cell_h + 8
        draw.rectangle([x0 - 2, y0 - 2, x0 + 448, y0 + 342], outline=(34, 197, 94), width=2, fill=(16, 22, 36))
        with Image.open(IMG_DIR / rec["file_name"]) as raw_im:
            im_rgb = raw_im.convert("RGB")
            sz = f"{im_rgb.width}x{im_rgb.height} ({im_rgb.width / max(1, im_rgb.height):.2f})"
            im_rgb.thumbnail((440, 246), Image.Resampling.LANCZOS)
            canvas.paste(im_rgb, (x0 + (446 - im_rgb.width) // 2, y0 + (250 - im_rgb.height) // 2))
        draw.text((x0 + 8, y0 + 256), f"[{rec['fix_tag']}] {rec['file_name']} • {sz}", fill=(0, 229, 255), font=f_lbl)
        draw.text((x0 + 8, y0 + 280), f"Nguồn: {rec['credit'][:46]}", fill=(250, 204, 21), font=f_cap)
        draw.text((x0 + 8, y0 + 302), rec["description"][:56], fill=(225, 234, 246), font=f_cap)
    out_1b = QA_DIR / "contact_step1b_only.jpg"
    canvas.save(out_1b, format="JPEG", quality=92)
    ok(f"Đã xuất bảng kiểm duyệt 12 ảnh Bước 1B: {out_1b}")


def main() -> None:
    if "--step1b" in sys.argv:
        run_step1b()
        return
    banner("BƯỚC 1 GIAI ĐOẠN 2 — SỬA TOÀN BỘ ẢNH LỖI QA TUẦN 16.11.2026")
    RAW_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    curator = ImageCurator()

    plan_path = DAY_DIR / "image_plan.json"
    credits_path = DAY_DIR / "image_credits.json"
    intro_path = DAY_DIR / "intro_hook.json"
    tt_path = DAY_DIR / "thethao.json"

    plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
    records: List[Dict[str, Any]] = plan_data["records"]
    credits_map: Dict[str, str] = json.loads(credits_path.read_text(encoding="utf-8"))
    intro_obj: Dict[str, Any] = json.loads(intro_path.read_text(encoding="utf-8"))
    news_objs: List[Dict[str, Any]] = json.loads(tt_path.read_text(encoding="utf-8"))

    # Thu thập hash hiện tại của các ảnh ĐÃ ĐẠT trong từng scene để chống trùng khi chọn ảnh thay thế
    scene_recs_map: Dict[int, List[Dict[str, Any]]] = {}
    for rec in records:
        scene_recs_map.setdefault(int(rec["scene_id"]), []).append(rec)

    fixed_records: List[Dict[str, Any]] = []
    modified_scenes: set[int] = set()

    for sc_id, sc_recs in sorted(scene_recs_map.items()):
        scene_hashes: List[int] = []
        # Trước tiên nạp hash các ảnh không nằm trong Group B
        for rec in sc_recs:
            fn = rec["file_name"]
            if fn in GROUP_B_REPLACEMENTS:
                continue
            p = IMG_DIR / fn
            if p.exists():
                with Image.open(p) as raw_im:
                    scene_hashes.append(ahash(raw_im.convert("RGB")))

        for rec in sc_recs:
            fn = rec["file_name"]
            dest = IMG_DIR / fn

            # 1) Nhóm A: Edge Crop (idempotent nhờ raw_backups)
            if fn in GROUP_A_CROPS:
                bak = RAW_BACKUP_DIR / fn
                if not bak.exists() and dest.exists():
                    shutil.copy2(dest, bak)
                src_p = bak if bak.exists() else dest
                with Image.open(src_p) as raw_im:
                    orig_im = raw_im.convert("RGB")
                cropped_im = apply_crop(orig_im, GROUP_A_CROPS[fn])
                cropped_im.save(dest, format="JPEG", quality=94, optimize=True)
                ok(f"[CROP] {fn}: {orig_im.size} -> {cropped_im.size}")
                modified_scenes.add(sc_id)
                fixed_records.append({**rec, "fix_tag": "CROP"})

            # 2) Nhóm B: Replace hoàn toàn
            elif fn in GROUP_B_REPLACEMENTS:
                bak = RAW_BACKUP_DIR / fn
                if not bak.exists() and dest.exists():
                    shutil.copy2(dest, bak)
                rep_spec = GROUP_B_REPLACEMENTS[fn]
                step(f"[REPLACE] {fn} ({rec['description'][:48]})...")
                new_im = pick_replacement_image(curator, fn, rep_spec, scene_hashes)
                new_im.save(dest, format="JPEG", quality=94, optimize=True)
                scene_hashes.append(ahash(new_im))
                new_cred = rep_spec["credit"]
                rec["credit"] = new_cred
                credits_map[fn] = new_cred
                ok(f"  -> Đã thay thế {fn}: {new_im.size} | Nguồn: {new_cred}")
                modified_scenes.add(sc_id)
                fixed_records.append({**rec, "fix_tag": "NEW"})

    # Đồng bộ JSON
    credits_path.write_text(json.dumps(credits_map, ensure_ascii=False, indent=2), encoding="utf-8")
    plan_path.write_text(json.dumps({"total_slots": len(records), "records": records}, ensure_ascii=False, indent=2), encoding="utf-8")
    intro_path.write_text(json.dumps(intro_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    tt_path.write_text(json.dumps(news_objs, ensure_ascii=False, indent=2), encoding="utf-8")

    # Tái xuất Contact Sheets cho các scene đã sửa + contact_overview.jpg
    p_male = load_voice_preset("primary")
    p_female = load_voice_preset("secondary")
    all_items = [intro_obj] + news_objs
    overview_entries: List[Tuple[int, str, Path]] = []

    for it in all_items:
        sc_id = int(it["id"])
        sc_recs = scene_recs_map.get(sc_id, [])
        if sc_recs:
            overview_entries.append((sc_id, it["title"], IMG_DIR / sc_recs[0]["file_name"]))
        if sc_id in modified_scenes:
            is_intro = (sc_id == 0)
            v_lbl = (
                "Song giọng Nữ (Ngọc Huyền) + Nam (Minh Quân Pro)"
                if is_intro
                else (p_male["voice_id"] if sc_id % 2 == 1 else p_female["voice_id"])
            )
            qa_name = "contact_scene_00_intro.jpg" if is_intro else f"contact_scene_{sc_id:02d}.jpg"
            render_scene_contact_sheet(sc_id, it["title"], v_lbl, sc_recs, QA_DIR / qa_name)
            ok(f"Đã cập nhật QA: {qa_name}")

    render_overview_sheet(overview_entries, QA_DIR / "contact_overview.jpg")
    fixed_pages = build_fixed_only_sheets(fixed_records, QA_DIR)
    ok(f"Hoàn tất sửa {len(fixed_records)} ảnh ({len(modified_scenes)} cảnh)!")
    for fp in fixed_pages:
        ok(f"  Bảng kiểm duyệt ảnh đã sửa: {fp}")


if __name__ == "__main__":
    main()
