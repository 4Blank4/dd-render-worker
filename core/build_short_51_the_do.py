#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_short_51_the_do.py — Dựng Video Short 9:16 về trận đấu 51 thẻ đỏ tại Brazil
kèm 1 Thumbnail dọc (1080x1920) chuẩn Cyber-Stadium và file mô tả SEO YouTube/TikTok.
"""
import sys
sys.dont_write_bytecode = True

import os
import shutil
import time
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
from m8_news_bridge import export_bridge_project
from renderer import render_html_engine

DAY_STR = "04.11.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, "Orther", DAY_STR)
WORK_DIR = paths.work_project_dir(os.path.join("Orther", DAY_STR))

SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
SHORTS_WORK = os.path.join(WORK_DIR, "shorts_render")

SHORT_CFG = {
    "id": 1,
    "item_id": 1,
    "slug": "Short_Tran_Dau_51_The_Do_Brazil",
    "file_name": "Short_Tran_Dau_51_The_Do_Brazil.mp4",
    "thumb_name": "Short_Tran_Dau_51_The_Do_thumbnail.jpg",
    "mota_name": "Short_Tran_Dau_51_The_Do_mota.txt",
    "thumb_image": os.path.join(DAY_DIR, "images", "Tin_01_1.jpg"),
    "thumb_kicker": "KỶ LỤC THẾ GIỚI · BRAZIL",
    "thumb_hero": "51 THẺ ĐỎ!",
    "thumb_hero_size": "130",
    "thumb_sub": "MÀN HỖN CHIẾN ĐIÊN RỒ NHẤT LỊCH SỬ",
    "thumb_tag_a": "XÔ ĐỔ GUINNESS",
    "thumb_tag_b": "UBERLANDIA VS MAMORE",
    "title": "Trận đấu 51 thẻ đỏ điên rồ tại Brazil: Kỷ lục thế giới mới bị phá vỡ! #Shorts",
    "desc": (
        "Một trận đấu bóng đá tại giải U20 bang Minas Gerais ở Brazil vừa chứng kiến màn ẩu đả điên rồ "
        "chưa từng có trong lịch sử, buộc trọng tài phải rút tới 51 chiếc thẻ đỏ (43 cầu thủ và 8 thành viên ban huấn luyện). "
        "Con số kinh hoàng này chính thức xô đổ kỷ lục thế giới 36 thẻ đỏ của Guinness từng được thiết lập tại Argentina năm 2011. "
        "Sau trận, phòng thay đồ của sân vận động còn bị đập phá tan hoang với 14 cánh cửa và bồn tắm thủy lực bị hư hại nặng nề!"
    ),
    "tags": "#Shorts #DiemDoc #BongDaBrazil #TheDo #KyLucGuinness #Uberlandia #Mamore #TinTheThao"
}


def render_short_video(force: bool = False) -> Optional[str]:
    banner("DỰNG VIDEO SHORT 9:16 (51 THẺ ĐỎ BRAZIL)", DAY_STR)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(SHORTS_WORK, exist_ok=True)

    t0 = time.time()
    out_path = os.path.join(SHORTS_OUT, SHORT_CFG["file_name"])

    if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
        ok(f"Short đã có sẵn: {paths.rel_to_root(out_path)}")
        return out_path

    step("Xuất timeline short cho Tin 01...")
    pdir, _, _ = export_bridge_project(
        DAY_DIR,
        item_id=1,
        format_type="short",
        work_proj_dir=os.path.join(SHORTS_WORK, "short_51_the_do"),
        global_offset_sec=0.0
    )

    step("Render 9:16 trên template short_news_v2.html (30fps)...")
    v = render_html_engine(
        pdir,
        template="short_news_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True
    )

    if v and os.path.exists(v):
        shutil.copy2(v, out_path)
        ok(f"🎉 Hoàn thành Short: {paths.rel_to_root(out_path)} ({os.path.getsize(out_path)/(1024*1024):.1f} MB)")
        banner(f"HOÀN THÀNH VIDEO SHORT ({time.time()-t0:.1f}s)")
        return out_path
    else:
        log("!! Render Short thất bại", tag="shorts")
        return None


def render_short_thumbnail():
    banner("TẠO ẢNH THUMBNAIL DỌC 9:16 CHO SHORT", DAY_STR)
    assets_url = paths.file_url(paths.ASSETS)
    logo_url = paths.file_url(os.path.join(paths.ASSETS, "logo", "diem-doc-logo-1.png"))

    tpl_html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  @font-face { font-family:'Anton'; src:url('__ASSETS__/fonts/Anton/Anton-Regular.ttf'); font-weight:400; }
  @font-face { font-family:'Oswald'; src:url('__ASSETS__/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; }
  @font-face { font-family:'Oswald'; src:url('__ASSETS__/fonts/Oswald/static/Oswald-SemiBold.ttf'); font-weight:600; }
  @font-face { font-family:'PlexMono'; src:url('__ASSETS__/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'); font-weight:700; }

  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1080px; height:1920px; overflow:hidden; background:#05070C; }
  body { font-family:'Oswald', sans-serif; position:relative; }

  /* NỬA TRÊN: ẢNH 58% */
  .top {
    position:absolute; top:0; left:0; right:0; height:58%;
    overflow:hidden; background:#080B12;
  }
  .top img.hero-bg {
    width:100%; height:100%; object-fit:cover; object-position:center 20%;
    filter: contrast(1.15) brightness(1.05) saturate(1.2);
  }
  .top::after {
    content:''; position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(5,7,12,0.15) 0%, transparent 25%, rgba(5,7,12,0.7) 70%, #05070C 100%);
  }

  .badge {
    position:absolute; top:56px; left:56px; z-index:5;
    display:flex; align-items:center; gap:16px;
    padding:16px 28px; border-radius:999px;
    background:rgba(5,7,12,0.85); border:2px solid rgba(0,229,255,0.7);
    box-shadow: 0 4px 20px rgba(0,0,0,0.6), 0 0 15px rgba(0,229,255,0.3);
    backdrop-filter:blur(12px);
  }
  .badge img { height:40px; width:auto; border-radius:50%; }
  .badge span {
    font-family:'Oswald'; font-weight:700; font-size:24px;
    letter-spacing:4px; color:#00E5FF; text-transform:uppercase;
  }

  /* NỬA DƯỚI: SÂN KHẤU 42% */
  .bottom {
    position:absolute; bottom:0; left:0; right:0; height:43%;
    background:#05070C; padding:40px 70px 70px;
    display:flex; flex-direction:column; justify-content:center;
    border-top: 1px solid rgba(0,229,255,0.25);
  }
  .kicker {
    font-family:'PlexMono'; font-weight:700; font-size:26px;
    letter-spacing:5px; color:#00E5FF; margin-bottom:14px;
    text-transform:uppercase;
    text-shadow: 0 0 12px rgba(0,229,255,0.4);
  }
  .hero {
    font-family:'Anton'; font-size:__THUMB_HERO_SIZE__px; line-height:0.95;
    letter-spacing:1px;
    color:#FFFFFF; white-space:nowrap;
    text-shadow:0 0 40px rgba(0,229,255,0.35), 0 4px 10px rgba(0,0,0,0.8);
  }
  .hero .accent { color:#FFC24D; }
  .sub {
    font-family:'Oswald'; font-weight:700; font-size:46px; line-height:1.15;
    color:#F3F6FF; margin-top:16px; text-transform:uppercase; letter-spacing:1px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
  }
  .rule {
    height:6px; width:180px;
    background:linear-gradient(90deg, #00E5FF 0%, #38BDF8 100%);
    margin:24px 0 20px; border-radius:3px;
    box-shadow: 0 0 10px rgba(0,229,255,0.5);
  }
  .meta {
    display:flex; gap:36px; align-items:center;
    font-family:'PlexMono'; font-size:22px; font-weight:700; letter-spacing:2px;
    color:#94A0BE;
  }
  .meta b { color:#00E5FF; }
</style>
</head>
<body>
  <div class="top">
    <div class="badge">
      <img src="__LOGO__" alt="Logo">
      <span>ĐIỂM ĐỌC</span>
    </div>
    <img class="hero-bg" src="__THUMB_IMAGE__" alt="">
  </div>

  <div class="bottom">
    <div class="kicker">__THUMB_KICKER__</div>
    <div class="hero">__THUMB_HERO__</div>
    <div class="sub">__THUMB_SUBTITLE__</div>
    <div class="rule"></div>
    <div class="meta">
      <span>__THUMB_TAG_A__</span>
      <span><b>__THUMB_TAG_B__</b></span>
    </div>
  </div>
</body>
</html>"""

    tpl_html = tpl_html.replace("__ASSETS__", assets_url).replace("__LOGO__", logo_url)
    thumb_html_dir = os.path.join(WORK_DIR, "shorts_thumbnails_render")
    os.makedirs(thumb_html_dir, exist_ok=True)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=[
            "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"
        ])
        page = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)

        out_thumb = os.path.join(SHORTS_OUT, SHORT_CFG["thumb_name"])
        step(f"Render thumbnail dọc: {paths.rel_to_root(out_thumb)}...")

        img_path = SHORT_CFG["thumb_image"]
        h_content = tpl_html
        h_content = h_content.replace("__THUMB_IMAGE__", paths.file_url(img_path))
        h_content = h_content.replace("__THUMB_KICKER__", SHORT_CFG["thumb_kicker"])
        h_content = h_content.replace("__THUMB_HERO__", SHORT_CFG["thumb_hero"])
        h_content = h_content.replace("__THUMB_HERO_SIZE__", SHORT_CFG.get("thumb_hero_size", "120"))
        h_content = h_content.replace("__THUMB_SUBTITLE__", SHORT_CFG["thumb_sub"])
        h_content = h_content.replace("__THUMB_TAG_A__", SHORT_CFG["thumb_tag_a"])
        h_content = h_content.replace("__THUMB_TAG_B__", SHORT_CFG["thumb_tag_b"])

        hfile = os.path.join(thumb_html_dir, "thumb_short_51_the_do.html")
        with open(hfile, "w", encoding="utf-8") as hf:
            hf.write(h_content)

        page.goto(paths.file_url(hfile), wait_until="networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=out_thumb, type="jpeg", quality=95)
        ok(f"  👉 Đã xuất Thumbnail dọc: {paths.rel_to_root(out_thumb)}")

        br.close()


def write_short_metadata():
    banner("XUẤT BẢN FILE MÔ TẢ SEO CHO SHORT", DAY_STR)
    mota_file = os.path.join(SHORTS_OUT, SHORT_CFG["mota_name"])
    content = (
        f"=== TIÊU ĐỀ SHORTS ===\n"
        f"{SHORT_CFG['title']}\n\n"
        f"=== MÔ TẢ SHORTS ===\n"
        f"{SHORT_CFG['desc']}\n\n"
        f"👉 Nhấn Đăng ký kênh Điểm Đọc để không bỏ lỡ các tin tức thể thao đỉnh cao mỗi ngày!\n\n"
        f"{SHORT_CFG['tags']}\n"
    )
    with open(mota_file, "w", encoding="utf-8") as f:
        f.write(content)
    ok(f"  👉 Đã ghi file mô tả SEO: {paths.rel_to_root(mota_file)}")


def main():
    write_short_metadata()
    render_short_thumbnail()
    render_short_video(force=True)


if __name__ == "__main__":
    main()
