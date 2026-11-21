#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/qa_precheck.py — Bộ Kiểm Duyệt Tự Động Trước Khi Render (Auto-QA Gate)
==========================================================================
Quét nhanh (< 2 giây) toàn bộ dữ liệu ngày `outputs/<DD.MM.YYYY>/` trước khi chạy TTS/Render:
  1. Kiểm tra ngôn từ máy móc / hậu trường bị cấm (AGENTS.md 5.1) trong kịch bản, thumbnail & mota.txt.
  2. Kiểm tra chuẩn số tiếng Việt (không dùng dấu chấm phân cách hàng nghìn kiểu 1.400).
  3. Kiểm tra toàn bộ ảnh trong image_plan.json: tồn tại, kích thước HD (>= 800x450, W/H >= 1.18), chống trùng hash cùng cảnh.
  4. Kiểm tra độ dài từng dòng tiêu đề trên thumbnails_plan.json (<= 21 ký tự/dòng chống tràn) & tiêu đề SEO <= 100 ký tự.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc.log import banner, ok, warn

ROOT = Path(_ROOT)

BANNED_PUBLIC_RE = re.compile(
    r"(?:giọng\s+đọc|giọng\s+(?:nam|nữ)|cảnh\s+quay|khung\s+hình|hiệu\s+ứng\s+(?:hình\s+ảnh|hiển\s+thị)"
    r"|thời\s+gian\s+tạo\s+video|thước\s+phim\s+phân\s+tích|minh\s+quân\s+pro|ngọc\s+huyền"
    r"|\[(?:nam|nữ|nu|tin\s*\d+)\]"
    r"|\((?:mẫu\s*\d+|mau\s*\d+)\)"
    r"|từ\s+12\s*(?:giờ|h)(?:\s*trưa)?)",
    flags=re.IGNORECASE,
)

# Số kiểu 1.400, 32.000 (tránh bắt nhầm ngày dd.mm.yyyy)
BAD_THOUSANDS_RE = re.compile(r"(?<!\d\.)\b\d{1,3}\.\d{3}\b(?!\.\d{2,4})")


def _ahash(img: Image.Image) -> int:
    g = img.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
    px = list(g.tobytes())
    avg = sum(px) / len(px)
    bits = 0
    for i, v in enumerate(px):
        if v >= avg:
            bits |= 1 << i
    return bits


def _hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()


def run_qa(day_str: str) -> Tuple[int, int]:
    day_dir = ROOT / "outputs" / day_str
    if not day_dir.exists():
        print(f"[FAIL] Không tìm thấy thư mục: {day_dir}")
        return 1, 0

    banner(f"AUTO-QA PRECHECK — NGÀY {day_str}")
    errors = 0
    warnings = 0

    # 1. Kiểm tra văn bản kịch bản (intro_hook.json + thethao.json)
    for fname in ("intro_hook.json", "thethao.json"):
        p = day_dir / fname
        if not p.exists():
            continue
        data = json.loads(p.read_text(encoding="utf-8"))
        entries = data if isinstance(data, list) else [data]
        for idx, item in enumerate(entries, 1):
            label = f"{fname}#{item.get('id', idx)}"
            for field in ("title", "summary"):
                txt = str(item.get(field) or "")
                m_bad = BANNED_PUBLIC_RE.search(txt)
                if m_bad:
                    print(f"[FAIL] {label}.{field} chứa cụm từ máy móc/cấm: '{m_bad.group(0)}'")
                    errors += 1
                m_num = BAD_THOUSANDS_RE.search(txt)
                if m_num:
                    print(f"[WARN] {label}.{field} có dấu chấm hàng nghìn (ViTTS dễ đọc nhầm): '{m_num.group(0)}'")
                    warnings += 1

    # 2. Kiểm tra ảnh trong image_plan.json
    plan_p = day_dir / "image_plan.json"
    img_dir = day_dir / "images"
    if plan_p.exists():
        records = json.loads(plan_p.read_text(encoding="utf-8")).get("records", [])
        scene_hashes: Dict[int, List[Tuple[str, int]]] = {}
        missing_cnt = 0
        lowres_cnt = 0
        dup_cnt = 0
        for rec in records:
            fn = rec.get("file_name", "")
            sc_id = int(rec.get("scene_id", 0))
            fp = img_dir / fn
            if not fp.exists():
                print(f"[FAIL] Thiếu file ảnh: {fn} (scene {sc_id})")
                missing_cnt += 1
                errors += 1
                continue
            with Image.open(fp) as im:
                w, h = im.size
                ratio = w / max(1, h)
                if w < 800 or h < 450 or ratio < 1.15:
                    print(f"[WARN] Ảnh dưới chuẩn HD ngang: {fn} ({w}x{h}, r={ratio:.2f})")
                    lowres_cnt += 1
                    warnings += 1
                hv = _ahash(im)
                prev_list = scene_hashes.setdefault(sc_id, [])
                if prev_list and _hamming(hv, prev_list[-1][1]) <= 4:
                    print(f"[FAIL] Ảnh trùng lặp liên tiếp (Adjacent Duplicate) trong Scene {sc_id:02d}: {fn} == {prev_list[-1][0]}")
                    errors += 1
                    dup_cnt += 1
                else:
                    for prev_fn, prev_h in prev_list[:-1]:
                        if _hamming(hv, prev_h) <= 4:
                            dup_cnt += 1
                            break
                prev_list.append((fn, hv))
        ok(f"Ảnh image_plan.json: {len(records)} ảnh | thiếu={missing_cnt} | thấp={lowres_cnt} | xen kẽ hợp lệ={dup_cnt}")

    # 3. Kiểm tra thumbnails_plan.json
    tp = day_dir / "thumbnails_plan.json"
    if tp.exists():
        t_items = json.loads(tp.read_text(encoding="utf-8"))
        for it in t_items:
            suf = it.get("suffix", "?")
            for fld in ("badge", "kicker", "headline", "subtitle"):
                raw = str(it.get(fld) or "")
                plain = _strip_html(raw)
                m_bad = BANNED_PUBLIC_RE.search(plain)
                if m_bad:
                    print(f"[FAIL] Thumbnail {suf}.{fld} chứa cụm từ cấm: '{m_bad.group(0)}'")
                    errors += 1
            hl_lines = [_strip_html(seg) for seg in str(it.get("headline") or "").split("<br>")]
            for li, ln in enumerate(hl_lines, 1):
                if len(ln) > 21:
                    print(f"[WARN] Thumbnail {suf} dòng {li} dài {len(ln)} ký tự (>21, dễ tràn dòng): '{ln}'")
                    warnings += 1
        ok(f"Đã kiểm tra {len(t_items)} cấu hình thumbnail 16:9.")

    # 4. Kiểm tra mota.txt & shorts/*_mota.txt
    mota_files: List[Path] = []
    if (day_dir / "mota.txt").exists():
        mota_files.append(day_dir / "mota.txt")
    if (day_dir / "shorts").exists():
        mota_files.extend(sorted((day_dir / "shorts").glob("*_mota.txt")))

    for mf in mota_files:
        txt = mf.read_text(encoding="utf-8")
        m_bad = BANNED_PUBLIC_RE.search(txt)
        if m_bad:
            print(f"[FAIL] {mf.name} chứa cụm từ máy móc/cấm: '{m_bad.group(0)}'")
            errors += 1
        for line in txt.splitlines():
            if line.startswith("Option "):
                title_part = line.split(":", 1)[1].strip()
                if len(title_part) > 100:
                    print(f"[FAIL] {mf.name} tiêu đề vượt 100 ký tự ({len(title_part)}): {title_part}")
                    errors += 1
                if not re.search(r"\|\s*Điểm\s*Đọc(?:\s+Tuần|\s+\d{1,2}/\d{1,2})?\s*$", title_part):
                    print(f"[WARN] {mf.name} tiêu đề chưa có hậu tố chuẩn '| Điểm Đọc ...': {title_part}")
                    warnings += 1
        if mf.name.endswith("_mota.txt"):
            for req_sec in ("[1. YOUTUBE SHORTS", "[2. FACEBOOK REELS", "[3. TIKTOK"):
                if req_sec not in txt:
                    print(f"[WARN] {mf.name} thiếu khối mô tả đa nền tảng '{req_sec}'")
                    warnings += 1
        ok(f"Đã kiểm tra mô tả SEO: {mf.name}")

    print("-" * 70)
    if errors == 0:
        ok(f"AUTO-QA HOÀN TẤT: 0 lỗi nghiêm trọng | {warnings} cảnh báo nhẹ.")
    else:
        warn(f"AUTO-QA PHÁT HIỆN: {errors} lỗi nghiêm trọng | {warnings} cảnh báo.")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Chạy Auto-QA Precheck cho dữ liệu bản tin ngày")
    parser.add_argument("--day", required=True, help="Ngày định dạng DD.MM.YYYY (VD: 19.11.2026)")
    args = parser.parse_args()
    errs, _ = run_qa(args.day)
    sys.exit(1 if errs > 0 else 0)


if __name__ == "__main__":
    main()
