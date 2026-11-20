#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_messi_thumbnails_cinematic.py — Render 3 Thumbnail 16:9 chuẩn Ronaldo 25.10.2026
cho video chuyên đề Lionel Messi (30.10.2026) bằng Playwright + HTML template.
"""
import sys
sys.dont_write_bytecode = True

import os
import shutil
import time
from playwright.sync_api import sync_playwright

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from diemdoc import paths
from diemdoc.log import banner, ok, step, log

DAY_STR = "30.10.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, DAY_STR)
WORK_DIR = paths.work_project_dir(DAY_STR)
TPL_PATH = os.path.join(paths.TEMPLATES, "thumbnail_16x9_sports.html")
LOGO_PATH = os.path.join(paths.ASSETS, "logo", "diem-doc-logo-1.png")

VARIANTS = [
    {
        "suffix": "A",
        "angle_name": "TUỔI 39 & 48 DANH HIỆU (INTER MIAMI / MLS)",
        "badge": "CHUYÊN ĐỀ ĐẶC BIỆT",
        "kicker": "LIONEL MESSI • TUỔI 39",
        "headline": '<span class="hl-cyan">MESSI TUỔI 39:</span><br><span class="hl-white">48 CHIẾC CÚP VÀ</span><br><span class="hl-yellow">ĐỈNH CAO CÔ ĐỘC!</span>',
        "subtitle": "936 BÀN THẮNG • 8 QUẢ BÓNG VÀNG • 1402 LẦN IN DẤU GIÀY",
        "footer_tag": "CHUYÊN ĐỀ SÂU",
        "image_file": os.path.join(DAY_DIR, "images", "Tin_01_5.jpg"),
        "obj_pos": "55% 20%",
        "filter": "contrast(1.10) brightness(1.04) saturate(1.18)",
    },
    {
        "suffix": "B",
        "angle_name": "KỶ LỤC 8 BALLON D'OR & DI SẢN BẤT TỬ",
        "badge": "KỶ LỤC VÔ TIỀN KHOÁNG HẬU",
        "kicker": "8 BALLON D'OR • 6 CHIẾC GIÀY VÀNG",
        "headline": '<span class="hl-yellow">8 QUẢ BÓNG VÀNG!</span><br><span class="hl-white">BỨC TƯỜNG BẤT TỬ</span><br><span class="hl-cyan">CỦA LIONEL MESSI</span>',
        "subtitle": "672 BÀN CHO BARCELONA • CÚ ĂN 6 NĂM 2009 • 91 BÀN NĂM 2012",
        "footer_tag": "HỒ SƠ HUYỀN THOẠI",
        "image_file": os.path.join(DAY_DIR, "images", "Tin_02_7.jpg"),
        "obj_pos": "60% 18%",
        "filter": "contrast(1.12) brightness(1.10) saturate(1.22)",
    },
    {
        "suffix": "C",
        "angle_name": "CÚP VÀNG WORLD CUP & VĨ ĐẠI NHẤT MỌI THỜI ĐẠI",
        "badge": "HUYỀN THOẠI BẤT TỬ",
        "kicker": "CÚP VÀNG THẾ GIỚI • 21 BÀN WORLD CUP",
        "headline": '<span class="hl-white">VÌ SAO MESSI</span><br><span class="hl-red">VĨ ĐẠI NHẤT LỊCH SỬ?</span><br><span class="hl-cyan">CHẤM HẾT TRANH CÃI!</span>',
        "subtitle": "1402 LẦN IN DẤU GIÀY • SỐ 9 SĂN BÀN & SỐ 10 KIẾN THIẾT",
        "footer_tag": "KHOẢNH KHẮC BẤT TỬ",
        "image_file": os.path.join(DAY_DIR, "images", "Tin_06_1.jpg"),
        "obj_pos": "50% 20%",
        "filter": "contrast(1.10) brightness(1.05) saturate(1.18)",
    },
]


def render_messi_thumbnails():
    banner("RENDER 3 THUMBNAIL 16:9 CINEMATIC CHO MESSI", DAY_STR)
    
    with open(TPL_PATH, "r", encoding="utf-8") as f:
        tpl_code = f.read()
    tpl_code = tpl_code.replace("__ASSETS__", paths.file_url(paths.ASSETS))
    tpl_code = tpl_code.replace("__LOGO_URL__", paths.file_url(LOGO_PATH))

    temp_html_dir = os.path.join(WORK_DIR, "thumbnails_render")
    os.makedirs(temp_html_dir, exist_ok=True)
    os.makedirs(DAY_DIR, exist_ok=True)

    w, h = 1920, 1080
    rendered = []

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=[
            "--no-sandbox",
            "--allow-file-access-from-files",
            "--disable-dev-shm-usage"
        ])
        page = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)

        for var in VARIANTS:
            sfx = var["suffix"]
            step(f"Chuẩn bị template Thumbnail {sfx} ({var['angle_name']})...")

            html_content = tpl_code
            html_content = html_content.replace("__THUMB_IMAGE__", paths.file_url(var["image_file"]))
            html_content = html_content.replace("__THUMB_BADGE__", var["badge"])
            html_content = html_content.replace("__THUMB_KICKER__", var["kicker"])
            html_content = html_content.replace("__THUMB_HEADLINE__", var["headline"])
            html_content = html_content.replace("__THUMB_SUBTITLE__", var["subtitle"])
            html_content = html_content.replace("__THUMB_FOOTER_TAG__", var["footer_tag"])

            # Đổi object-position và filter
            html_content = html_content.replace("__THUMB_OBJ_POS__", var.get("obj_pos", "center 20%"))
            html_content = html_content.replace("__THUMB_FILTER__", var.get("filter", "contrast(1.10) brightness(1.05) saturate(1.18)"))

            html_file = os.path.join(temp_html_dir, f"thumbnail_{sfx}.html")
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)

            out_jpg = os.path.join(DAY_DIR, f"thumbnail_{sfx}.jpg")
            page.goto(paths.file_url(html_file), wait_until="networkidle")
            page.wait_for_timeout(800)
            page.screenshot(path=out_jpg, type="jpeg", quality=95)

            ok(f"Đã xuất thumbnail {sfx}: {paths.rel_to_root(out_jpg)} ({os.path.getsize(out_jpg)/1024:.1f} KB)")
            rendered.append(out_jpg)

        br.close()

    # Mặc định copy A thành thumbnail.jpg
    thumb_default = os.path.join(DAY_DIR, "thumbnail.jpg")
    shutil.copy2(os.path.join(DAY_DIR, "thumbnail_A.jpg"), thumb_default)
    ok(f"Mặc định YouTube: {paths.rel_to_root(thumb_default)}")

    banner("HOÀN THÀNH RENDER THUMBNAIL 16:9 CHO LIONEL MESSI")
    return rendered


if __name__ == "__main__":
    render_messi_thumbnails()
