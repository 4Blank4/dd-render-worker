#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/prepare_weekly_23_11.py — Tuyển Chọn Kho Ảnh HD & Sinh Kịch Bản Bản Tin Tuần Weekly-23.11.2026
==================================================================================================
Tái sử dụng kho ảnh HD đã qua kiểm duyệt thị giác từ 6 ngày trong tuần (18.11 – 23.11.2026):
  - Tổng hợp 16 ảnh cho Intro (4 đoạn song giọng) + 15–17 ảnh độc lập cho mỗi trong 21 chuyên đề.
  - Ánh xạ ảnh sát ngữ cảnh từng câu nói (sentence_refs) và chống trùng lặp perceptual hash
    (ahash + dhash) tuyệt đối trong cùng một cảnh.
  - Xuất đầy đủ dữ liệu chuẩn tại `outputs/Weekly-23.11.2026/`:
      intro_hook.json, thethao.json, image_plan.json, image_credits.json,
      thumbnails_plan.json, thethao.txt, kich_ban_tung_cau.txt,
      qa/contact_scene_00_intro.jpg, qa/contact_scene_01..21.jpg, qa/contact_overview.jpg.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
import math
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont, ImageOps

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc.image_curator import compute_dhash, hamming_dist
from diemdoc.log import banner, ok, step, warn
from weekly_23_11_data import INTRO_DATA, WEEKLY_ITEMS

ROOT = Path(_ROOT)
DAY_STR = "Weekly-23.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
IMG_DIR = OUT_DIR / "images"
QA_DIR = OUT_DIR / "qa"

SOURCE_DAYS = ["18.11.2026", "19.11.2026", "20.11.2026", "21.11.2026", "22.11.2026", "23.11.2026"]


def _ahash(img: Image.Image) -> int:
    g = img.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
    px = list(g.tobytes())
    avg = sum(px) / len(px)
    bits = 0
    for i, v in enumerate(px):
        if v >= avg:
            bits |= 1 << i
    return bits


def _center_crop_ahash(img: Image.Image) -> int:
    """Hash vùng trung tâm 76% ảnh để phát hiện ảnh crop tỷ lệ khác từ cùng 1 khung hình."""
    w, h = img.size
    dx, dy = int(w * 0.12), int(h * 0.12)
    cropped = img.crop((dx, dy, max(dx + 16, w - dx), max(dy + 16, h - dy)))
    return _ahash(cropped)


def _split_sentences(summary: str) -> List[str]:
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", (summary or "").strip()) if p.strip()]
    return parts


def _pick_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates: List[Path] = []
    fonts_dir = ROOT / "assets" / "fonts"
    if fonts_dir.exists():
        pattern = "*Bold*.ttf" if bold else "*Regular*.ttf"
        candidates.extend(sorted(fonts_dir.rglob(pattern)))
        candidates.extend(sorted(fonts_dir.rglob("*.ttf")))
    candidates.extend([
        Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/Library/Fonts/Arial Unicode.ttf"),
    ])
    for fp in candidates:
        if fp.exists():
            try:
                return ImageFont.truetype(str(fp), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap_text(txt: str, max_chars: int = 38) -> str:
    words = (txt or "").split()
    lines: List[str] = []
    cur = ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= max_chars:
            cur = f"{cur} {w}".strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return "\n".join(lines[:3])


def load_source_pools() -> Dict[Tuple[str, int], List[Dict[str, Any]]]:
    """Đọc toàn bộ ảnh HD đã kiểm duyệt từ 6 ngày trong tuần, gom theo (day, scene_id)."""
    pools: Dict[Tuple[str, int], List[Dict[str, Any]]] = {}
    for day in SOURCE_DAYS:
        day_dir = ROOT / "outputs" / day
        pl_path = day_dir / "image_plan.json"
        cr_path = day_dir / "image_credits.json"
        img_dir = day_dir / "images"
        if not pl_path.exists():
            warn(f"Bỏ qua {day}: thiếu image_plan.json")
            continue
        plan = json.loads(pl_path.read_text(encoding="utf-8"))
        credits = json.loads(cr_path.read_text(encoding="utf-8")) if cr_path.exists() else {}

        seen_files: Dict[Tuple[str, int], set] = {}
        for rec in plan.get("records", []):
            src_sc = int(rec.get("scene_id", 0))
            fn = rec.get("file_name", "")
            key = (day, src_sc)
            seen = seen_files.setdefault(key, set())
            if not fn or fn in seen:
                continue
            fp = img_dir / fn
            if not fp.exists():
                continue
            try:
                with Image.open(fp) as im:
                    w, h = im.size
                    ratio = w / max(1, h)
                    if w < 800 or h < 450 or ratio < 1.15:
                        continue
                    ah = _ahash(im)
                    cah = _center_crop_ahash(im)
                    dh = compute_dhash(im)
            except Exception:
                continue
            seen.add(fn)
            cr = (credits.get(fn) or rec.get("credit") or "TƯ LIỆU BÁO CHÍ").strip()
            desc = (rec.get("description") or "").strip()
            pools.setdefault(key, []).append({
                "src_day": day,
                "src_scene": src_sc,
                "src_file": fp,
                "src_name": fn,
                "w": w,
                "h": h,
                "ratio": ratio,
                "ahash": ah,
                "cahash": cah,
                "dhash": dh,
                "credit": cr,
                "description": desc,
                "score": w * h,
            })
    return pools


# Bộ lọc chống lẫn chủ đề trên các nguồn gộp đa tin & loại ảnh crop trùng
SCENE_EXCLUDES: Dict[int, Dict[str, Any]] = {
    6: {"files": {("23.11.2026", "Tin_01_5.jpg")}},
    7: {"keywords": ["minh vương", "quy nhơn", "công an nhân dân", "văn hiến"]},
    8: {
        "keywords": [
            "hải phòng", "dylan kerr", "quyết chiến", "thanh lực",
            "hoàn tất", "billiards", "stephen thompson", "kickboxing", "radtke",
        ]
    },
    10: {"keywords": ["ancelotti", "romario", "brazil", "singapore"]},
    12: {
        "files": {
            ("21.11.2026", "Tin_13_1.jpg"),
            ("21.11.2026", "Tin_13_7.jpg"),
            ("21.11.2026", "Tin_13_10.jpg"),
            ("21.11.2026", "Tin_13_11.jpg"),
        },
        "keywords": ["giã từ sự nghiệp quốc tế", "bất đồng", "rời phòng họp báo"],
    },
    17: {
        "files": {("23.11.2026", "Tin_12_3.jpg")},
    },
    19: {
        "keywords": [
            "hải phòng", "dylan kerr", "allison", "quynh lee", "cầu lông",
            "v-league", "lauren lam", "pochettino", "anfield", "man utd",
            "ghe ngo", "bầu dục", "coventry", "nhật bản", "elon musk",
        ],
    },
    21: {
        "keywords": ["pochettino", "anfield", "bezzecchi", "motogp", "portimão"],
    },
}

# Bộ lọc bắt buộc (OR keyword match trên description) theo từng (scene_id, sentence_idx)
SENTENCE_INCLUDE_KEYWORDS: Dict[Tuple[int, int], List[str]] = {
    (8, 1): ["đình khải", "hoàng đức", "lion championship", "muay", "52 kg"],
    (8, 2): ["đình khải", "hoàng đức", "lion championship", "đòn chỏ", "hiệp"],
    (8, 3): ["esports", "free fire", "bangkok"],
    (8, 4): ["allison", "quynh lee", "hong kong", "bóng bàn", "anh tú", "400 triệu", "kuala lumpur", "vũ văn trung"],
    (8, 5): ["bách khoa", "đông hòa", "thaco", "sinh viên", "rmit"],
    (12, 2): ["yamal", "barca", "barcelona", "camp nou", "villarreal"],
    (19, 0): ["thitikul", "skubal", "stirling", "procházka", "lauren price", "lpga", "ufc"],
    (19, 1): ["hai môn", "thitikul", "skubal", "lpga", "korda"],
    (19, 2): ["thitikul", "golf", "bogey", "sörenstam", "cme group", "korda", "a-lim kim"],
    (19, 3): ["skubal", "mets", "cy young", "pitcher", "450 triệu", "bóng chày"],
    (19, 4): ["stirling", "procházka", "ufc", "doha", "stephen thompson", "mma", "kickboxing", "hooker"],
    (19, 5): ["lauren price", "quyền anh", "kotaskova", "bán trung", "xứ wales", "đai"],
    (20, 1): ["paredes", "boca juniors"],
    (20, 2): ["paredes", "boca juniors", "phòng khám", "cúp nam mỹ"],
    (20, 3): ["neymar", "poker", "bsop", "gerwyn price", "darts", "van veen", "são paulo"],
    (20, 4): ["u17 hàn quốc", "kim ji-woo", "u17 australia", "akon", "kansas", "saudi arabia", "nwsl"],
    (20, 5): ["wembley", "world cup nữ 2035", "zurich", "vương quốc anh"],
    (21, 1): ["werder bremen", "hamburger", "marseille", "le mans", "coventry", "celtic"],
    (21, 2): ["herro", "76ers", "sixers", "bucks", "nba"],
    (21, 3): ["bóng bầu dục", "pháp", "england", "anh thắng", "scotland", "twickenham"],
    (21, 4): ["ghe ngo", "vĩnh long", "pickleball", "sophia"],
    (21, 5): ["nhật bản", "colombia", "musk", "brady", "carlsen", "lại lý huynh", "lang kỳ kỳ"],
}

# Các scene không được fallback sang pool hỗn hợp nếu câu đã có bộ lọc riêng
STRICT_SENTENCE_POOL_SCENES = {7, 8, 12, 19, 20, 21}


def _filter_for_scene(cands: List[Dict[str, Any]], sc_id: int, s_idx: int = 0) -> List[Dict[str, Any]]:
    ex = SCENE_EXCLUDES.get(sc_id, {})
    ex_files = ex.get("files", set())
    ex_kws = ex.get("keywords", [])
    inc_kws = SENTENCE_INCLUDE_KEYWORDS.get((sc_id, s_idx), [])
    out: List[Dict[str, Any]] = []
    for c in cands:
        if (c["src_day"], c["src_name"]) in ex_files:
            continue
        dl = (c.get("description") or "").lower()
        if any(kw in dl for kw in ex_kws):
            continue
        if inc_kws and not any(kw in dl for kw in inc_kws):
            continue
        out.append(c)
    return out


def _is_dup_candidate(cand: Dict[str, Any], picked: List[Dict[str, Any]], threshold: int = 4) -> bool:
    for idx_p, p in enumerate(picked):
        if p["src_file"] == cand["src_file"]:
            return True
        adj_th = 6 if idx_p == len(picked) - 1 else threshold
        if hamming_dist(cand["ahash"], p["ahash"]) <= adj_th:
            return True
        if hamming_dist(cand["dhash"], p["dhash"]) <= adj_th:
            return True
        # Kiểm tra chéo full <-> center-crop để loại biến thể crop khác khung hình
        if (
            hamming_dist(cand["ahash"], p["cahash"]) <= 4
            or hamming_dist(cand["cahash"], p["ahash"]) <= 4
            or hamming_dist(cand["cahash"], p["cahash"]) <= 4
        ):
            return True
    return False


def _gather_interleaved_candidates(
    refs: List[Tuple[str, int]], pools: Dict[Tuple[str, int], List[Dict[str, Any]]]
) -> List[Dict[str, Any]]:
    """Trộn xen kẽ ứng viên từ nhiều (day, scene_id) để ảnh đa dạng góc chụp và sự kiện."""
    buckets = [list(pools.get(r, [])) for r in refs if pools.get(r)]
    out: List[Dict[str, Any]] = []
    idx = 0
    while True:
        added = False
        for b in buckets:
            if idx < len(b):
                out.append(b[idx])
                added = True
        if not added:
            break
        idx += 1
    return out


def _pick_distinct(
    candidates: List[Dict[str, Any]],
    picked_in_scene: List[Dict[str, Any]],
    count: int,
    allow_relaxed: bool = True,
) -> List[Dict[str, Any]]:
    chosen: List[Dict[str, Any]] = []
    # Pass 1: nghiêm ngặt không trùng ahash/dhash <= 4 (<= 6 với ảnh liền kề)
    for c in candidates:
        if len(chosen) >= count:
            break
        if not _is_dup_candidate(c, picked_in_scene, threshold=4):
            chosen.append(c)
            picked_in_scene.append(c)
    # Pass 2: nếu thiếu hiếm hoi, nới threshold xuống 2 nhưng vẫn tránh trùng file tuyệt đối
    if allow_relaxed and len(chosen) < count:
        for c in candidates:
            if len(chosen) >= count:
                break
            if not _is_dup_candidate(c, picked_in_scene, threshold=2):
                chosen.append(c)
                picked_in_scene.append(c)
    return chosen


def render_contact_sheet(
    scene_id: int,
    title: str,
    news_source: str,
    voice_label: str,
    records: List[Dict[str, Any]],
    out_path: Path,
) -> None:
    cols = 4
    rows = max(1, math.ceil(len(records) / cols))
    tw, th = 420, 236
    pad = 22
    header_h = 112
    card_h = th + 88
    W = cols * tw + (cols + 1) * pad
    H = header_h + rows * card_h + pad

    canvas = Image.new("RGB", (W, H), (10, 14, 24))
    draw = ImageDraw.Draw(canvas)
    f_title = _pick_font(26, bold=True)
    f_sub = _pick_font(18, bold=False)
    f_cap = _pick_font(14, bold=True)
    f_desc = _pick_font(13, bold=False)

    draw.rectangle([(0, 0), (W, header_h - 10)], fill=(15, 23, 42))
    draw.rectangle([(0, header_h - 12), (W, header_h - 9)], fill=(0, 229, 255))
    lbl = f"SCENE {scene_id:02d} • {len(records)} ẢNH" if scene_id > 0 else f"INTRO 00 • {len(records)} ẢNH"
    draw.text((pad, 16), f"{lbl}  |  {voice_label}  |  NGUỒN: {news_source}", font=f_sub, fill=(0, 229, 255))
    draw.text((pad, 48), title[:112], font=f_title, fill=(248, 250, 252))

    for i, rec in enumerate(records):
        r = i // cols
        c = i % cols
        x0 = pad + c * (tw + pad)
        y0 = header_h + r * card_h
        img_fp = IMG_DIR / rec["file_name"]
        try:
            with Image.open(img_fp) as im:
                thumb = ImageOps.fit(im.convert("RGB"), (tw, th), method=Image.Resampling.LANCZOS)
                canvas.paste(thumb, (x0, y0))
        except Exception:
            draw.rectangle([(x0, y0), (x0 + tw, y0 + th)], fill=(60, 20, 20))

        draw.rectangle([(x0, y0 + th), (x0 + tw, y0 + card_h - 8)], fill=(18, 26, 44))
        tag = "[T]" if rec["type"] == "title" else f"[S{rec['sentence_idx']}]"
        draw.text(
            (x0 + 8, y0 + th + 6),
            f"{rec['file_name']} {tag} | {rec['dimensions']} | 📷 {rec['credit'][:20]}",
            font=f_cap,
            fill=(56, 189, 248),
        )
        desc_wrapped = _wrap_text(rec.get("description", ""), max_chars=52)
        draw.multiline_text((x0 + 8, y0 + th + 28), desc_wrapped, font=f_desc, fill=(203, 213, 225), spacing=3)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, "JPEG", quality=88)


def render_overview_sheet(lead_records: List[Dict[str, Any]], total_imgs: int, out_path: Path) -> None:
    cols = 4
    rows = max(1, math.ceil(len(lead_records) / cols))
    tw, th = 400, 225
    pad = 20
    header_h = 96
    card_h = th + 64
    W = cols * tw + (cols + 1) * pad
    H = header_h + rows * card_h + pad

    canvas = Image.new("RGB", (W, H), (8, 12, 22))
    draw = ImageDraw.Draw(canvas)
    f_title = _pick_font(28, bold=True)
    f_sub = _pick_font(18, bold=False)
    f_cap = _pick_font(15, bold=True)

    draw.rectangle([(0, 0), (W, header_h - 8)], fill=(15, 23, 42))
    draw.rectangle([(0, header_h - 10), (W, header_h - 7)], fill=(0, 229, 255))
    draw.text((pad, 16), f"TỔNG QUAN BẢNG KIỂM DUYỆT THỊ GIÁC — {DAY_STR}", font=f_title, fill=(0, 229, 255))
    draw.text((pad, 54), f"22 Cảnh (Intro 00 + 21 Chuyên đề tuần) • Tổng cộng {total_imgs} ảnh HD độc lập", font=f_sub, fill=(226, 232, 240))

    for i, item in enumerate(lead_records):
        r = i // cols
        c = i % cols
        x0 = pad + c * (tw + pad)
        y0 = header_h + r * card_h
        img_fp = IMG_DIR / item["lead_file"]
        try:
            with Image.open(img_fp) as im:
                thumb = ImageOps.fit(im.convert("RGB"), (tw, th), method=Image.Resampling.LANCZOS)
                canvas.paste(thumb, (x0, y0))
        except Exception:
            draw.rectangle([(x0, y0), (x0 + tw, y0 + th)], fill=(60, 20, 20))
        draw.rectangle([(x0, y0 + th), (x0 + tw, y0 + card_h - 6)], fill=(18, 26, 44))
        draw.text((x0 + 8, y0 + th + 6), f"SCENE {item['scene_id']:02d} ({item['count']} ảnh) • {item['credit'][:22]}", font=f_cap, fill=(56, 189, 248))
        draw.text((x0 + 8, y0 + th + 30), item["title"][:44], font=f_sub, fill=(241, 245, 249))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out_path, "JPEG", quality=88)


def main() -> None:
    banner(f"CHUẨN BỊ DỮ LIỆU BẢN TIN TUẦN — {DAY_STR}", DAY_STR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)

    # Xóa ảnh Tin_* cũ trong OUT_DIR/images nếu chạy lại để tránh file thừa
    for old_f in IMG_DIR.glob("*.jpg"):
        old_f.unlink()

    step("Đang quét kho ảnh HD & hash thị giác từ 6 bản tin ngày (18–23.11.2026)...")
    pools = load_source_pools()
    total_avail = sum(len(v) for v in pools.values())
    ok(f"Đã nạp {total_avail} ảnh ứng viên sạch từ {len(pools)} cụm sự kiện nguồn.")

    all_records: List[Dict[str, Any]] = []
    image_credits: Dict[str, str] = {}
    overview_items: List[Dict[str, Any]] = []

    # --------------------------------------------------------------------------
    # 1. XỬ LÝ INTRO (SCENE 00 — 16 ẢNH ĐA DIỆN, 4 ẢNH/ĐOẠN)
    # --------------------------------------------------------------------------
    step("Xử lý Intro 00 (4 đoạn song giọng x 4 ảnh = 16 ảnh)...")
    intro_picked: List[Dict[str, Any]] = []
    intro_records: List[Dict[str, Any]] = []
    intro_slot_idx = 1
    for seg_idx, refs in enumerate(INTRO_DATA["segment_sources"], 1):
        cands = _gather_interleaved_candidates(refs, pools)
        picked = _pick_distinct(cands, intro_picked, 4)
        for p in picked:
            dest_name = f"Tin_00_{intro_slot_idx}.jpg"
            shutil.copy2(p["src_file"], IMG_DIR / dest_name)
            rec = {
                "scene_id": 0,
                "type": "sentence",
                "index": seg_idx,
                "sentence_idx": seg_idx,
                "file_name": dest_name,
                "dimensions": f"{p['w']}x{p['h']} r={p['ratio']:.2f}",
                "credit": p["credit"],
                "description": p["description"] or f"Điểm nhấn tuần — đoạn {seg_idx}",
            }
            intro_records.append(rec)
            all_records.append(rec)
            image_credits[dest_name] = p["credit"]
            intro_slot_idx += 1

    intro_summary = " ".join(s["text"] for s in INTRO_DATA["voice_segments"])
    intro_json: Dict[str, Any] = {
        "id": 0,
        "art_id": "art_00",
        "group": INTRO_DATA["group"],
        "title": INTRO_DATA["title"],
        "summary": intro_summary,
        "total_images": len(intro_records),
        "hide_date_chip": False,
        "source": INTRO_DATA["source"],
        "news_source": INTRO_DATA["news_source"],
        "credit": " • ".join(dict.fromkeys(r["credit"] for r in intro_records[:4]))[:60],
        "voice": "Song giọng Nữ & Nam",
        "voice_gender": "mixed",
        "voice_preset": "mixed",
        "audio_path": str(OUT_DIR / "audio" / "audio_intro.wav"),
        "audio_title": "",
        "image_path": str(IMG_DIR / "Tin_00_1.jpg"),
        "hide_title": True,
        "voice_segments": INTRO_DATA["voice_segments"],
        "stat_badges": {},
    }
    for k, rec in enumerate(intro_records, 1):
        intro_json[f"image_{k}"] = str(IMG_DIR / rec["file_name"])

    render_contact_sheet(
        0,
        INTRO_DATA["title"],
        INTRO_DATA["news_source"],
        "Song giọng Nữ & Nam",
        intro_records,
        QA_DIR / "contact_scene_00_intro.jpg",
    )
    overview_items.append({
        "scene_id": 0,
        "count": len(intro_records),
        "lead_file": intro_records[0]["file_name"],
        "credit": intro_records[0]["credit"],
        "title": "INTRO TỔNG HỢP TUẦN 23.11.2026",
    })

    # --------------------------------------------------------------------------
    # 2. XỬ LÝ 21 CHUYÊN ĐỀ CHÍNH (01..21 — 15-17 ẢNH/CẢNH SÁT TỪNG CÂU)
    # --------------------------------------------------------------------------
    step("Xử lý 21 chuyên đề tuần (ánh xạ sentence_refs & lọc trùng perceptual hash)...")
    thethao_items: List[Dict[str, Any]] = []

    for item in WEEKLY_ITEMS:
        sc_id = int(item["id"])
        sents = _split_sentences(item["summary"])
        n_sents = len(sents)
        all_pool_cands = _filter_for_scene(_gather_interleaved_candidates(item["source_refs"], pools), sc_id, 0)
        picked_in_scene: List[Dict[str, Any]] = []

        # Phân bổ số ảnh mỗi slot: 3 ảnh cho Title + 2-3 ảnh cho mỗi câu (~16-17 ảnh/cảnh)
        if n_sents == 6:
            quotas = [3, 2, 3, 2, 3, 2, 2]  # = 17 ảnh
        elif n_sents == 5:
            quotas = [3, 3, 2, 3, 2, 3]     # = 16 ảnh
        else:
            quotas = [3] + [2] * n_sents

        scene_records: List[Dict[str, Any]] = []
        img_counter = 1

        # Slot Title (type='title', index=0, sentence_idx=0)
        title_picks = _pick_distinct(all_pool_cands, picked_in_scene, quotas[0])
        for p in title_picks:
            dest_name = f"Tin_{sc_id:02d}_{img_counter}.jpg"
            shutil.copy2(p["src_file"], IMG_DIR / dest_name)
            rec = {
                "scene_id": sc_id,
                "type": "title",
                "index": 0,
                "sentence_idx": 0,
                "file_name": dest_name,
                "dimensions": f"{p['w']}x{p['h']} r={p['ratio']:.2f}",
                "credit": p["credit"],
                "description": p["description"] or item["title"],
            }
            scene_records.append(rec)
            all_records.append(rec)
            image_credits[dest_name] = p["credit"]
            img_counter += 1

        # Slots cho từng câu 1..N
        sent_refs_map: Dict[int, List[Tuple[str, int]]] = item.get("sentence_refs", {})
        for s_idx in range(1, n_sents + 1):
            q = quotas[s_idx]
            specific_refs = sent_refs_map.get(s_idx) or item["source_refs"]
            raw_spec = _gather_interleaved_candidates(specific_refs, pools)
            spec_cands = _filter_for_scene(raw_spec, sc_id, s_idx)
            s_picks = _pick_distinct(spec_cands, picked_in_scene, q, allow_relaxed=True)
            if len(s_picks) < q:
                # Nếu câu không có filter riêng thì mở rộng sang pool chung của chuyên đề; nếu có thì thử lọc từ toàn bộ pool nguồn
                fallback_pool = (
                    _filter_for_scene(all_pool_cands, sc_id, s_idx)
                    if (sc_id, s_idx) in SENTENCE_INCLUDE_KEYWORDS or sc_id in STRICT_SENTENCE_POOL_SCENES
                    else all_pool_cands
                )
                extra = _pick_distinct(fallback_pool, picked_in_scene, q - len(s_picks), allow_relaxed=True)
                s_picks.extend(extra)
                # Nếu câu hoàn toàn chưa có ảnh nào (0 ảnh) vì nguồn chỉ có 2 góc chụp xoay vòng, cho phép xen kẽ không liền kề
                if not s_picks and spec_cands and picked_in_scene:
                    last_p = picked_in_scene[-1]
                    for c in spec_cands:
                        if hamming_dist(c["ahash"], last_p["ahash"]) > 5:
                            s_picks.append(c)
                            picked_in_scene.append(c)
                            break
            for p in s_picks:
                dest_name = f"Tin_{sc_id:02d}_{img_counter}.jpg"
                shutil.copy2(p["src_file"], IMG_DIR / dest_name)
                rec = {
                    "scene_id": sc_id,
                    "type": "sentence",
                    "index": s_idx,
                    "sentence_idx": s_idx,
                    "file_name": dest_name,
                    "dimensions": f"{p['w']}x{p['h']} r={p['ratio']:.2f}",
                    "credit": p["credit"],
                    "description": p["description"] or sents[s_idx - 1][:90],
                }
                scene_records.append(rec)
                all_records.append(rec)
                image_credits[dest_name] = p["credit"]
                img_counter += 1

        is_primary = (sc_id % 2 == 1)
        voice_preset = "primary" if is_primary else "secondary"
        voice_name = "Minh Quân Pro" if is_primary else "Ngọc Huyền"
        voice_gender = "male" if is_primary else "female"

        row: Dict[str, Any] = {
            "id": sc_id,
            "art_id": f"art_{sc_id:02d}",
            "group": item["group"],
            "title": item["title"],
            "summary": item["summary"],
            "total_images": len(scene_records),
            "hide_date_chip": False,
            "source": item["source"],
            "news_source": item["news_source"],
            "credit": " / ".join(dict.fromkeys(r["credit"] for r in scene_records[:3]))[:50],
            "voice": voice_name,
            "voice_gender": voice_gender,
            "voice_preset": voice_preset,
            "audio_path": str(OUT_DIR / "audio" / f"audio_{sc_id:02d}.wav"),
            "audio_title": str(OUT_DIR / "audio-title" / f"audio_title_{sc_id:02d}.wav"),
            "image_path": str(IMG_DIR / scene_records[0]["file_name"]),
            "stat_badges": item.get("stat_badges", {}),
        }
        for k, rec in enumerate(scene_records, 1):
            row[f"image_{k}"] = str(IMG_DIR / rec["file_name"])
        thethao_items.append(row)

        render_contact_sheet(
            sc_id,
            item["title"],
            item["news_source"],
            voice_name,
            scene_records,
            QA_DIR / f"contact_scene_{sc_id:02d}.jpg",
        )
        overview_items.append({
            "scene_id": sc_id,
            "count": len(scene_records),
            "lead_file": scene_records[0]["file_name"],
            "credit": scene_records[0]["credit"],
            "title": item["title"],
        })

    render_overview_sheet(overview_items, len(all_records), QA_DIR / "contact_overview.jpg")

    # --------------------------------------------------------------------------
    # 3. SAO CHÉP 3 ẢNH HERO CHO THUMBNAILS VÀ GHI CÁC FILE JSON/TXT
    # --------------------------------------------------------------------------
    # Thumb A: Liverpool 4-0 Man Utd (Pochettino & Anfield)
    thumb_src_a = pools[("23.11.2026", 7)][0]["src_file"]
    # Thumb B: U17 Việt Nam (Tin 02 lead image)
    thumb_src_b = IMG_DIR / "Tin_02_1.jpg"
    # Thumb C: Ánh Viên & Bơi lội Đại hội toàn quốc (Tin 06 lead image)
    thumb_src_c = IMG_DIR / "Tin_06_1.jpg"

    shutil.copy2(thumb_src_a, IMG_DIR / "Thumb_A.jpg")
    shutil.copy2(thumb_src_b, IMG_DIR / "Thumb_B.jpg")
    shutil.copy2(thumb_src_c, IMG_DIR / "Thumb_C.jpg")

    thumbnails_plan = [
        {
            "suffix": "A",
            "badge": "BẢN TIN TUẦN • 23.11",
            "kicker": "NGOẠI HẠNG ANH • ĐẠI HỘI 2026",
            "headline": "MAN UTD THẢM BẠI<br>0-4 TẠI ANFIELD!",
            "subtitle": "Pochettino lập kỷ lục tệ nhất 100 năm • Barca ngược dòng • Alcaraz vô địch",
            "footer_tag": "BẢN TIN TUẦN 23/11",
            "image_file": f"outputs/{DAY_STR}/images/Thumb_A.jpg",
            "obj_pos": "center 22%",
            "filter": "contrast(1.06) saturate(1.1)",
        },
        {
            "suffix": "B",
            "badge": "U17 WORLD CUP 2026",
            "kicker": "BÓNG ĐÁ VIỆT NAM • TIN TUẦN",
            "headline": "U17 VIỆT NAM GHI<br>2 SIÊU PHẨM BỈ!",
            "subtitle": "Sỹ Bách đánh gót & Nguyễn Lực đá phạt góc • Đình Bắc nghỉ hết năm",
            "footer_tag": "TÂM ĐIỂM TUẦN 23/11",
            "image_file": f"outputs/{DAY_STR}/images/Thumb_B.jpg",
            "obj_pos": "center 20%",
            "filter": "contrast(1.08) saturate(1.12)",
        },
        {
            "suffix": "C",
            "badge": "ĐẠI HỘI TOÀN QUỐC 2026",
            "kicker": "THỂ THAO VIỆT NAM & THẾ GIỚI",
            "headline": "MƯA KỶ LỤC BƠI!<br>ÁNH VIÊN ĐOẠT HCB",
            "subtitle": "Watson Nguyễn phá KLQG • Alcaraz vô địch ATP Finals • Marc Márquez lần 8",
            "footer_tag": "TỔNG HỢP TUẦN 23/11",
            "image_file": f"outputs/{DAY_STR}/images/Thumb_C.jpg",
            "obj_pos": "center 22%",
            "filter": "contrast(1.07) saturate(1.1)",
        },
    ]

    (OUT_DIR / "intro_hook.json").write_text(json.dumps(intro_json, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "thethao.json").write_text(json.dumps(thethao_items, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "image_plan.json").write_text(
        json.dumps({"total_slots": len(all_records), "records": all_records}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "image_credits.json").write_text(json.dumps(image_credits, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT_DIR / "thumbnails_plan.json").write_text(json.dumps(thumbnails_plan, ensure_ascii=False, indent=2), encoding="utf-8")

    # Xuất thethao.txt & kich_ban_tung_cau.txt để dễ kiểm tra
    txt_lines = [f"BẢN TIN TỔNG HỢP THỂ THAO TUẦN — {DAY_STR}", "=" * 72, ""]
    txt_lines.append(f"[00] INTRO: {intro_json['summary']}\n")
    sent_lines = [f"KỊCH BẢN TỪNG CÂU — {DAY_STR}", "=" * 72, ""]
    for idx_s, seg in enumerate(INTRO_DATA["voice_segments"], 1):
        sent_lines.append(f"[00.S{idx_s}] {seg['text']}")
    sent_lines.append("")

    for it in thethao_items:
        txt_lines.append(f"[{it['id']:02d}] ({it['group']}) {it['title']}")
        txt_lines.append(f"    Nguồn: {it['source']}")
        txt_lines.append(f"    {it['summary']}\n")
        sent_lines.append(f"[{it['id']:02d}] {it['title']}")
        for si, s in enumerate(_split_sentences(it["summary"]), 1):
            sent_lines.append(f"  S{si}: {s}")
        sent_lines.append("")

    (OUT_DIR / "thethao.txt").write_text("\n".join(txt_lines), encoding="utf-8")
    (OUT_DIR / "kich_ban_tung_cau.txt").write_text("\n".join(sent_lines), encoding="utf-8")

    ok(f"Hoàn tất chuẩn bị {len(thethao_items)} chuyên đề + Intro 00 = {len(all_records)} ảnh HD!")
    ok(f"Thư mục đầu ra: {OUT_DIR}")


if __name__ == "__main__":
    main()
