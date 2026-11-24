#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_thumbnails_09_11.py — Render lại bộ 3 Thumbnail 16:9 chuẩn Cyber-Stadium
cho Bản tin tổng hợp thể thao tuần 09.11.2026 qua Playwright + HTML template.
"""
import sys
sys.dont_write_bytecode = True

import argparse
import os
import json
import shutil
from pathlib import Path
from playwright.sync_api import sync_playwright

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from diemdoc import paths
from diemdoc.log import banner, ok, step, log
from diemdoc.publisher import DEFAULT_LONG_ABC_STYLES, render_thumbnail_16x9_single

DEFAULT_DAY_STR = "09.11.2026"


def _resolve_plan_img(img_rel: str, day_dir: str) -> Path:
    if not img_rel:
        return Path("")
    cand = Path(img_rel) if os.path.isabs(img_rel) else (Path(_ROOT) / img_rel)
    if cand.exists():
        return cand
    alt = Path(day_dir) / "images" / os.path.basename(img_rel)
    return alt


def render_thumbnails(day_str: str = DEFAULT_DAY_STR):
    day_dir = os.path.join(paths.OUTPUTS, day_str)
    plan_path = os.path.join(day_dir, "thumbnails_plan.json")

    banner(f"RENDER BỘ 3 THUMBNAIL 16:9 (3 KIỂU ĐA DẠNG) — {day_str}", day_str)

    if not os.path.exists(plan_path):
        raise FileNotFoundError(f"Không tìm thấy file kế hoạch: {plan_path}")

    variants = None
    for attempt in range(3):
        try:
            with open(plan_path, "r", encoding="utf-8") as f:
                variants = json.loads(f.read())
            break
        except Exception as e:
            if attempt == 2:
                raise e
            import time
            time.sleep(0.35 * (attempt + 1))

    os.makedirs(day_dir, exist_ok=True)
    rendered = []

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=[
            "--no-sandbox",
            "--allow-file-access-from-files",
            "--disable-dev-shm-usage"
        ])
        page = br.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)

        for idx, var in enumerate(variants):
            sfx = str(var["suffix"]).lstrip("_")
            img_abs = _resolve_plan_img(var.get("image_file", ""), day_dir)
            if not img_abs.exists():
                raise FileNotFoundError(f"Không tìm thấy ảnh: {img_abs}")

            chosen_style = str(var.get("style") or DEFAULT_LONG_ABC_STYLES[idx % len(DEFAULT_LONG_ABC_STYLES)])
            right_img = _resolve_plan_img(var.get("right_image", ""), day_dir) if var.get("right_image") else None
            extra_imgs = [_resolve_plan_img(x, day_dir) for x in (var.get("extra_images") or []) if x]
            cards = None
            if var.get("cards"):
                cards = []
                for c in var["cards"]:
                    cp = _resolve_plan_img(c.get("file", ""), day_dir)
                    cards.append({**c, "file": str(cp) if cp.exists() else ""})

            step(f"Rendering Thumbnail {sfx} [{chosen_style}] (Badge: {var.get('badge')})...")
            out_jpg = Path(day_dir) / f"thumbnail_{sfx}.jpg"

            render_thumbnail_16x9_single(
                out_path=out_jpg,
                image_path=img_abs,
                kicker=var.get("kicker", ""),
                hero_html=var.get("headline", ""),
                subtitle=var.get("subtitle", ""),
                badge=var.get("badge", "TÂM ĐIỂM"),
                tag_a=var.get("tag_a") or var.get("footer_tag", "ĐIỂM ĐỌC"),
                tag_b=var.get("tag_b", "CHUẨN 1080P"),
                hero_size=str(var.get("hero_size", "86")).replace("px", ""),
                obj_pos=var.get("obj_pos", "center 20%"),
                img_filter=var.get("filter", "contrast(1.10) brightness(1.05) saturate(1.18)"),
                page=page,
                style=chosen_style,
                extra_images=[e for e in extra_imgs if e.exists()],
                cards=cards,
                right_image=right_img if (right_img and right_img.exists()) else None,
                line1=var.get("line1"),
                line2=var.get("line2"),
                left_pos=var.get("left_pos"),
                right_pos=var.get("right_pos"),
                l1_size=var.get("l1_size"),
                l2_size=var.get("l2_size"),
            )

            sz_kb = out_jpg.stat().st_size / 1024
            ok(f"Đã xuất thumbnail {sfx} ({chosen_style}): {paths.rel_to_root(str(out_jpg))} ({sz_kb:.1f} KB)")
            rendered.append(str(out_jpg))

        br.close()

    # Mặc định copy A thành thumbnail.jpg
    thumb_default = os.path.join(day_dir, "thumbnail.jpg")
    shutil.copy2(os.path.join(day_dir, "thumbnail_A.jpg"), thumb_default)
    ok(f"Mặc định YouTube: {paths.rel_to_root(thumb_default)}")

    banner(f"HOÀN THÀNH RENDER BỘ 3 THUMBNAIL 16:9 TUẦN {day_str}")
    return rendered


render_thumbnails_09_11 = render_thumbnails


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--day", default=DEFAULT_DAY_STR, help="Thư mục ngày (vd: 16.11.2026)")
    args = ap.parse_args()
    render_thumbnails(args.day)
