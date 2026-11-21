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

DEFAULT_DAY_STR = "09.11.2026"
TPL_PATH = os.path.join(paths.TEMPLATES, "thumbnail_16x9_sports.html")
LOGO_PATH = os.path.join(paths.ASSETS, "logo", "diem-doc-logo-1.png")


def render_thumbnails(day_str: str = DEFAULT_DAY_STR):
    day_dir = os.path.join(paths.OUTPUTS, day_str)
    work_dir = paths.work_project_dir(day_str)
    plan_path = os.path.join(day_dir, "thumbnails_plan.json")

    banner(f"RENDER BỘ 3 THUMBNAIL 16:9 ĐIỂM ĐỌC TUẦN {day_str}", day_str)

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

    with open(TPL_PATH, "r", encoding="utf-8") as f:
        tpl_code = f.read()

    tpl_code = tpl_code.replace("__ASSETS__", paths.file_url(paths.ASSETS))
    tpl_code = tpl_code.replace("__LOGO_URL__", paths.file_url(LOGO_PATH))

    temp_html_dir = os.path.join(work_dir, "thumbnails_render")
    os.makedirs(temp_html_dir, exist_ok=True)
    os.makedirs(day_dir, exist_ok=True)

    w, h = 1920, 1080
    rendered = []

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=[
            "--no-sandbox",
            "--allow-file-access-from-files",
            "--disable-dev-shm-usage"
        ])
        page = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)

        for var in variants:
            sfx = str(var["suffix"]).lstrip("_")
            img_rel = var.get("image_file", "")
            img_abs = os.path.join(_ROOT, img_rel) if not os.path.isabs(img_rel) else img_rel
            if not os.path.exists(img_abs):
                alt_abs = os.path.join(day_dir, "images", os.path.basename(img_rel))
                if os.path.exists(alt_abs):
                    img_abs = alt_abs

            if not os.path.exists(img_abs):
                raise FileNotFoundError(f"Không tìm thấy ảnh: {img_abs}")

            step(f"Rendering Thumbnail {sfx} (Badge: {var.get('badge')})...")

            html_content = tpl_code
            html_content = html_content.replace("__THUMB_IMAGE__", paths.file_url(img_abs))
            html_content = html_content.replace("__THUMB_BADGE__", var.get("badge", "TÂM ĐIỂM"))
            html_content = html_content.replace("__THUMB_KICKER__", var.get("kicker", ""))
            html_content = html_content.replace("__THUMB_HEADLINE__", var.get("headline", ""))
            html_content = html_content.replace("__THUMB_SUBTITLE__", var.get("subtitle", ""))
            html_content = html_content.replace("__THUMB_FOOTER_TAG__", var.get("footer_tag", "TỔNG HỢP TUẦN QUA"))
            html_content = html_content.replace("__THUMB_OBJ_POS__", var.get("obj_pos", "center 20%"))
            html_content = html_content.replace("__THUMB_FILTER__", var.get("filter", "contrast(1.10) brightness(1.05) saturate(1.18)"))

            html_file = os.path.join(temp_html_dir, f"thumbnail_{sfx}.html")
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            out_jpg = os.path.join(day_dir, f"thumbnail_{sfx}.jpg")
            page.goto(paths.file_url(html_file), wait_until="networkidle")
            page.wait_for_timeout(800)
            page.screenshot(path=out_jpg, type="jpeg", quality=95)

            sz_kb = os.path.getsize(out_jpg) / 1024
            ok(f"Đã xuất thumbnail {sfx}: {paths.rel_to_root(out_jpg)} ({sz_kb:.1f} KB)")
            rendered.append(out_jpg)

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
