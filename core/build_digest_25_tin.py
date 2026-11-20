#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_digest_25_tin.py — Dựng 1 Video Shorts 9:16 Tin Nhanh Thể Thao (25 Tin)
kèm Thumbnail dọc chuẩn Cyber-Stadium và File mô tả SEO đầy đủ 25 Chapters.
"""
import sys
sys.dont_write_bytecode = True

import os
import shutil
import time
import json
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "vendor"))

engines_html = os.path.join(_ROOT, "engines", "html")
if engines_html not in sys.path:
    sys.path.insert(0, engines_html)

from diemdoc import paths
from diemdoc.log import banner, ok, step, log
from m8_news_bridge import export_digest_short_project
from renderer import render_html_engine

DAY_STR = "02.11.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, DAY_STR)
WORK_DIR = paths.work_project_dir(DAY_STR)

SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
DIGEST_WORK = os.path.join(WORK_DIR, "digest_short_25_tin")

OUT_VIDEO = os.path.join(SHORTS_OUT, "Short_Tin_Nhanh_25_Tin_The_Thao.mp4")
OUT_THUMB = os.path.join(SHORTS_OUT, "Short_Tin_Nhanh_25_Tin_thumbnail.jpg")
OUT_MOTA = os.path.join(SHORTS_OUT, "Short_Tin_Nhanh_25_Tin_mota.txt")


def render_digest_thumbnail():
    banner("TẠO THUMBNAIL DỌC 9:16 CHO TIN NHANH 25 TIN", DAY_STR)
    assets_url = paths.file_url(paths.ASSETS)
    logo_url = paths.file_url(os.path.join(paths.ASSETS, "logo", "diem-doc-logo-1.png"))
    thumb_img = os.path.join(DAY_DIR, "images", "Tin_01_6.jpg")

    tpl_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  @font-face {{ font-family:'Anton'; src:url('{assets_url}/fonts/Anton/Anton-Regular.ttf'); font-weight:400; }}
  @font-face {{ font-family:'Oswald'; src:url('{assets_url}/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; }}
  @font-face {{ font-family:'PlexMono'; src:url('{assets_url}/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'); font-weight:700; }}

  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html,body {{ width:1080px; height:1920px; overflow:hidden; background:#05070C; }}
  body {{ font-family:'Oswald', sans-serif; position:relative; }}

  /* NỬA TRÊN: ẢNH 58% */
  .top {{
    position:absolute; top:0; left:0; right:0; height:58%;
    overflow:hidden; background:#080B12;
  }}
  .top img.hero-bg {{
    width:100%; height:100%; object-fit:cover; object-position:center 20%;
    filter: contrast(1.12) brightness(1.05) saturate(1.18);
  }}
  .top::after {{
    content:''; position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(5,7,12,0.15) 0%, transparent 25%, rgba(5,7,12,0.7) 70%, #05070C 100%);
  }}

  .badge {{
    position:absolute; top:56px; left:56px; z-index:5;
    display:flex; align-items:center; gap:16px;
    padding:16px 28px; border-radius:999px;
    background:rgba(5,7,12,0.85); border:2px solid rgba(0,229,255,0.7);
    box-shadow: 0 4px 20px rgba(0,0,0,0.6), 0 0 15px rgba(0,229,255,0.3);
    backdrop-filter:blur(12px);
  }}
  .badge img {{ height:40px; width:auto; border-radius:50%; }}
  .badge span {{
    font-family:'Oswald'; font-weight:700; font-size:24px;
    letter-spacing:4px; color:#00E5FF; text-transform:uppercase;
  }}

  /* NỬA DƯỚI: SÂN KHẤU 42% */
  .bottom {{
    position:absolute; bottom:0; left:0; right:0; height:43%;
    background:#05070C; padding:40px 70px 70px;
    display:flex; flex-direction:column; justify-content:center;
    border-top: 1px solid rgba(0,229,255,0.25);
  }}
  .kicker {{
    font-family:'PlexMono'; font-weight:700; font-size:26px;
    letter-spacing:5px; color:#00E5FF; margin-bottom:14px;
    text-transform:uppercase;
    text-shadow: 0 0 12px rgba(0,229,255,0.4);
  }}
  .hero {{
    font-family:'Anton'; font-size:110px; line-height:0.95;
    letter-spacing:1px;
    color:#FFFFFF; white-space:nowrap;
    text-shadow:0 0 40px rgba(0,229,255,0.35), 0 4px 10px rgba(0,0,0,0.8);
  }}
  .sub {{
    font-family:'Oswald'; font-weight:700; font-size:46px; line-height:1.15;
    color:#F3F6FF; margin-top:16px; text-transform:uppercase; letter-spacing:1px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
  }}
  .rule {{
    height:6px; width:180px;
    background:linear-gradient(90deg, #00E5FF 0%, #38BDF8 100%);
    margin:24px 0 20px; border-radius:3px;
    box-shadow: 0 0 10px rgba(0,229,255,0.5);
  }}
  .meta {{
    display:flex; gap:36px; align-items:center;
    font-family:'PlexMono'; font-size:22px; font-weight:700; letter-spacing:2px;
    color:#94A0BE;
  }}
  .meta b {{ color:#00E5FF; }}
</style>
</head>
<body>
  <div class="top">
    <div class="badge">
      <img src="{logo_url}" alt="Logo">
      <span>ĐIỂM ĐỌC</span>
    </div>
    <img class="hero-bg" src="{paths.file_url(thumb_img)}" alt="">
  </div>

  <div class="bottom">
    <div class="kicker">BẢN TIN THỂ THAO TỔNG HỢP</div>
    <div class="hero">25 TIN NHANH!</div>
    <div class="sub">TOÀN CẢNH THỂ THAO TUẦN QUA</div>
    <div class="rule"></div>
    <div class="meta">
      <span>25 SỰ KIỆN NÓNG</span>
      <span><b>ĐỌC LƯỚT 2 PHÚT</b></span>
    </div>
  </div>
</body>
</html>"""

    thumb_html_path = os.path.join(WORK_DIR, "thumb_digest_25_tin.html")
    with open(thumb_html_path, "w", encoding="utf-8") as f:
        f.write(tpl_html)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=[
            "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"
        ])
        page = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(paths.file_url(thumb_html_path), wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=OUT_THUMB, type="jpeg", quality=95)
        br.close()

    ok(f"👉 Đã xuất Thumbnail dọc: {paths.rel_to_root(OUT_THUMB)}")


def write_digest_metadata(tl_path: str):
    banner("XUẤT BẢN FILE MÔ TẢ SEO CHO TIN NHANH 25 TIN", DAY_STR)
    with open(tl_path, "r", encoding="utf-8") as f:
        tl = json.load(f)

    items = tl.get("items", [])
    chapters = []
    for it in items:
        sec = int(it.get("start", 0))
        m = sec // 60
        s = sec % 60
        time_str = f"{m}:{s:02d}"
        it_id = int(it.get("id", 1))
        chapters.append(f"{time_str} - [{it_id:02d}] {it.get('title')}")

    chapters_str = "\n".join(chapters)

    content = f"""=== TIÊU ĐỀ SHORTS ===
Tin nhanh thể thao: Toàn cảnh 25 sự kiện chấn động tuần qua! #Shorts

=== MÔ TẢ SHORTS ===
Bản tin Điểm Đọc đọc lướt nhanh toàn cảnh 25 sự kiện thể thao nổi bật và kịch tính nhất tuần qua trong chưa đầy 3 phút:

{chapters_str}

👉 Nhấn Đăng ký kênh Điểm Đọc để không bỏ lỡ các tin tức thể thao đỉnh cao mỗi ngày!

#TinNhanh #DiemDoc #TheThao #Shorts #BongDa #HarryKane #Messi #Ronaldo #ManUtd #VLeague #U17VietNam
"""
    with open(OUT_MOTA, "w", encoding="utf-8") as f:
        f.write(content)

    ok(f"👉 Đã ghi file mô tả SEO: {paths.rel_to_root(OUT_MOTA)}")


def render_digest_video(force: bool = False) -> str:
    banner("DỰNG VIDEO SHORTS TIN NHANH 25 TIN 9:16", DAY_STR)
    os.makedirs(SHORTS_OUT, exist_ok=True)

    if os.path.exists(OUT_VIDEO) and os.path.getsize(OUT_VIDEO) > 1_000_000 and not force:
        ok(f"Video Tin Nhanh 25 tin đã có sẵn: {paths.rel_to_root(OUT_VIDEO)}")
        return OUT_VIDEO

    step("Xuất project Digest Short cho toàn bộ 25 tin...")
    pdir, tl_path, words_path = export_digest_short_project(
        DAY_DIR,
        item_ids=list(range(1, 26)),
        work_proj_dir=DIGEST_WORK,
        global_offset_sec=0.0
    )

    # Viết file mô tả với chapters thời gian
    write_digest_metadata(tl_path)

    # Render thumbnail dọc
    render_digest_thumbnail()

    step("Render 9:16 trên template short_digest_v2.html (30fps)...")
    v = render_html_engine(
        pdir,
        template="short_digest_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True
    )

    if v and os.path.exists(v):
        shutil.copy2(v, OUT_VIDEO)
        ok(f"🎉 Hoàn thành Video Tin Nhanh: {paths.rel_to_root(OUT_VIDEO)} ({os.path.getsize(OUT_VIDEO)/(1024*1024):.1f} MB)")
        return OUT_VIDEO
    else:
        log("!! Render Video Tin Nhanh thất bại", tag="digest")
        return ""


def main():
    os.makedirs(SHORTS_OUT, exist_ok=True)
    render_digest_thumbnail()
    render_digest_video(force=True)
    ok("🎉 HOÀN THÀNH VIDEO TIN NHANH 25 TIN VÀ TOÀN BỘ TÀI NGUYÊN!")


if __name__ == "__main__":
    main()
