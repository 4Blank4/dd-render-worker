#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_digest_09_11.py — Dựng 1 Video Shorts 9:16 Tin Nhanh Thể Thao (25 Tin) ngày 09.11.2026
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

DAY_STR = "09.11.2026"
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
    thumb_img = os.path.join(DAY_DIR, "images", "Tin_01_4.jpg")

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

  .top-stage {{
    position:absolute; top:0; left:0; width:1080px; height:1120px;
    background:#070B14; overflow:hidden;
  }}
  .top-stage img {{
    width:100%; height:100%; object-fit:cover; object-position:50% 15%;
    filter:contrast(1.12) brightness(1.06) saturate(1.18);
  }}
  .vignette {{
    position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(7,11,20,0.3) 0%, rgba(7,11,20,0.1) 40%, rgba(5,7,12,0.95) 90%, #05070C 100%),
               radial-gradient(ellipse at center, transparent 40%, rgba(5,7,12,0.6) 100%);
  }}

  .channel-pill {{
    position:absolute; top:54px; left:50%; transform:translateX(-50%);
    display:flex; align-items:center; gap:14px;
    background:rgba(7,11,20,0.85); border:1.5px solid rgba(0,229,255,0.6);
    padding:10px 26px; border-radius:999px;
    box-shadow:0 0 25px rgba(0,229,255,0.35); backdrop-filter:blur(10px);
  }}
  .channel-pill img {{ width:36px; height:36px; border-radius:50%; }}
  .channel-pill span {{
    font-family:'Oswald'; font-weight:700; font-size:24px;
    letter-spacing:3px; color:#FFFFFF; text-transform:uppercase;
  }}
  .channel-pill .sub {{ color:#00E5FF; margin-left:6px; }}

  .hero-badge {{
    position:absolute; bottom:40px; left:50%; transform:translateX(-50%);
    background:#E50914; color:#FFFFFF; font-family:'Oswald'; font-weight:700;
    font-size:32px; letter-spacing:4px; padding:12px 36px; border-radius:8px;
    box-shadow:0 0 35px rgba(229,9,20,0.6), inset 0 0 10px rgba(255,255,255,0.3);
    text-transform:uppercase; text-shadow:0 2px 4px rgba(0,0,0,0.8);
  }}

  .bottom-stage {{
    position:absolute; top:1120px; left:0; width:1080px; height:800px;
    padding:40px 60px; display:flex; flex-direction:column; justify-content:space-between;
    background:linear-gradient(180deg, #05070C 0%, #080D18 100%);
    border-top:2px solid rgba(0,229,255,0.4);
    box-shadow:0 -20px 40px rgba(0,229,255,0.15);
  }}

  .kicker {{
    font-family:'PlexMono'; font-size:26px; color:#00E5FF;
    letter-spacing:3px; text-transform:uppercase; display:flex; align-items:center; gap:12px;
  }}
  .kicker::before {{
    content:''; display:inline-block; width:10px; height:10px;
    background:#00E5FF; border-radius:50%; box-shadow:0 0 12px #00E5FF;
  }}

  .headline {{
    font-family:'Anton'; font-size:98px; line-height:1.02;
    text-transform:uppercase; letter-spacing:1px;
    color:#FFFFFF; text-shadow:0 4px 20px rgba(0,0,0,0.9);
  }}
  .hl-cyan {{ color:#00E5FF; text-shadow:0 0 30px rgba(0,229,255,0.5); }}
  .hl-yellow {{ color:#FFD200; text-shadow:0 0 30px rgba(255,210,0,0.5); }}

  .subdeck {{
    font-size:34px; font-weight:700; color:#CBD5E1;
    letter-spacing:1px; text-transform:uppercase; line-height:1.25;
  }}

  .footer-row {{
    display:flex; justify-content:space-between; align-items:center;
    padding-top:20px; border-top:1px solid rgba(255,255,255,0.12);
  }}
  .footer-tag {{
    font-family:'PlexMono'; font-size:22px; color:#94A3B8; letter-spacing:2px;
  }}
  .footer-cta {{
    font-family:'Oswald'; font-weight:700; font-size:26px; color:#00E5FF;
    letter-spacing:2px; text-transform:uppercase; display:flex; align-items:center; gap:8px;
  }}
</style>
</head>
<body>
  <div class="top-stage">
    <img src="{paths.file_url(thumb_img)}" alt="Hero">
    <div class="vignette"></div>
    <div class="channel-pill">
      <img src="{logo_url}" alt="Logo">
      <span>ĐIỂM ĐỌC<span class="sub">THỂ THAO</span></span>
    </div>
    <div class="hero-badge">TỔNG HỢP TUẦN</div>
  </div>

  <div class="bottom-stage">
    <div class="kicker">BẢN TIN NHANH • 25 SỰ KIỆN NÓNG BỎNG</div>
    <div class="headline">
      <span class="hl-yellow">25 TIN NÓNG:</span><br>
      <span class="hl-cyan">RONALDO GIÃ TỪ</span><br>
      <span style="color:#FFF">MU CHÌM ĐÁY!</span>
    </div>
    <div class="subdeck">
      COMO 9-1 LỊCH SỬ • MAN CITY THUA SỐC • VIỆT NAM GỌI OLAHA
    </div>
    <div class="footer-row">
      <div class="footer-tag">TUẦN 02.11 – 08.11.2026</div>
      <div class="footer-cta">XEM NGAY ▶</div>
    </div>
  </div>
</body>
</html>
"""
    tmp_html = os.path.join(DIGEST_WORK, "thumb_digest.html")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(tpl_html)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(paths.file_url(tmp_html), wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=OUT_THUMB, type="jpeg", quality=95)
        browser.close()

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

#TinNhanh #DiemDoc #TheThao #Shorts #BongDa #Ronaldo #ManCity #ManUtd #VLeague #ChampionsLeague
"""
    with open(OUT_MOTA, "w", encoding="utf-8") as f:
        f.write(content)

    ok(f"👉 Đã ghi file mô tả SEO: {paths.rel_to_root(OUT_MOTA)}")


def render_digest_video(force: bool = False) -> str:
    banner("DỰNG VIDEO SHORTS TIN NHANH 25 TIN 9:16", DAY_STR)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(DIGEST_WORK, exist_ok=True)

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
    render_digest_video(force=True)
    ok("🎉 HOÀN THÀNH VIDEO TIN NHANH 25 TIN VÀ TOÀN BỘ TÀI NGUYÊN!")


if __name__ == "__main__":
    main()
