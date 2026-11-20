#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_short_liverpool_fenerbahce.py — Dựng Video Short 9:16 về thất bại cay đắng 2-3
của Liverpool trước Fenerbahce tại lượt bốn vòng phân hạng Champions League.
"""
import sys
sys.dont_write_bytecode = True

import json
import os
import shutil
import time
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont
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

DAY_STR = "05.11.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, "Orther", DAY_STR)
WORK_DIR = paths.work_project_dir(os.path.join("Orther", DAY_STR))

SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
SHORTS_WORK = os.path.join(WORK_DIR, "shorts_render")
QA_DIR = os.path.join(DAY_DIR, "qa")

SHORT_CFG = {
    "id": 4,
    "item_id": 4,
    "slug": "Short_Liverpool_Thua_Nguoc_Fenerbahce",
    "file_name": "Short_Liverpool_Thua_Nguoc_Fenerbahce.mp4",
    "thumb_name": "Short_Liverpool_Thua_Nguoc_Fenerbahce_thumbnail.jpg",
    "mota_name": "Short_Liverpool_Thua_Nguoc_Fenerbahce_mota.txt",
    "thumb_image": os.path.join(DAY_DIR, "images", "Tin_04_1.jpg"),
    "thumb_kicker": "CHAMPIONS LEAGUE · ĐỊA CHẤN",
    "thumb_hero": "THUA NGƯỢC!",
    "thumb_hero_size": "130",
    "thumb_sub": "LIVERPOOL THỦNG LƯỚI 3 BÀN TỪ BÓNG CHẾT TRÊN ĐẤT THỔ",
    "thumb_tag_a": "ĐỨT MẠCH TOÀN THẮNG C1",
    "thumb_tag_b": "DIRK KUYT QUẬT NGÃ ĐỘI CŨ",
    "title": "Thảm họa bóng chết khiến Liverpool thua ngược cay đắng Fenerbahce 2-3 #Shorts",
    "desc": (
        "Cơn địa chấn kinh hoàng đã làm rung chuyển cúp C1 tại chảo lửa Sukru Saracoglu, "
        "khi Liverpool bất ngờ gục ngã hai ba trước Fenerbahce trong một ngày hàng phòng ngự hoàn toàn sụp đổ.\n\n"
        "Dù hai lần vượt lên dẫn trước nhờ công của tài năng trẻ 19 tuổi Trey Nyoni và Alexander Isak, "
        "The Reds đều để đối thủ gỡ hòa chóng vánh. Bàn thắng bằng đầu của Vedat Muriqi ở phút 79 "
        "đã hoàn tất màn ngược dòng điên rồ cho đội chủ nhà Thổ Nhĩ Kỳ.\n\n"
        "Đáng nói, cả ba bàn thua cay đắng của Liverpool đều xuất phát từ những tình huống cố định: "
        "một quả đá phạt hàng rào, một quả phạt góc và một pha ném biên dài. "
        "Thất bại nghiệt ngã này chính thức chấm dứt mạch toàn thắng của Liverpool tại Champions League "
        "và nối dài chuỗi sáu trận toàn thua đầy ám ảnh trên đất Thổ Nhĩ Kỳ!"
    ),
    "tags": "#Shorts #DiemDoc #Liverpool #Fenerbahce #ChampionsLeague #DirkKuyt #Iraola #Isak #TreyNyoni #TinBongDa"
}


def generate_contact_sheet():
    banner("TẠO BẢNG ẢNH ĐỐI CHỨNG QA CHO TIN 04 (LIVERPOOL 2-3 FENERBAHCE)", DAY_STR)
    os.makedirs(QA_DIR, exist_ok=True)
    img_dir = os.path.join(DAY_DIR, "images")

    credits_map = {}
    cred_file = os.path.join(DAY_DIR, "image_credits.json")
    if os.path.exists(cred_file):
        with open(cred_file, "r", encoding="utf-8") as f:
            credits_map = json.load(f)

    files = [f"Tin_04_{i}.jpg" for i in range(1, 13)]

    cols = 3
    rows = (len(files) + cols - 1) // cols
    cell_w, cell_h = 500, 360
    pad = 18

    sheet_w = cols * cell_w + (cols + 1) * pad
    sheet_h = rows * cell_h + (rows + 1) * pad + 80

    sheet = Image.new("RGB", (sheet_w, sheet_h), color=(15, 23, 42))
    draw = ImageDraw.Draw(sheet)

    # Header
    draw.rectangle([(0, 0), (sheet_w, 70)], fill=(6, 9, 17))
    draw.text((pad, 20), "ĐIỂM ĐỌC QA — BẢNG ĐỐI CHỨNG HÌNH ẢNH: FENERBAHCE 3-2 LIVERPOOL (05.11.2026)", fill=(0, 229, 255))

    for idx, f in enumerate(files):
        r = idx // cols
        c = idx % cols
        x = pad + c * (cell_w + pad)
        y = 80 + pad + r * (cell_h + pad)

        thumb_box_h = cell_h - 60
        im_path = os.path.join(img_dir, f)
        if not os.path.exists(im_path):
            continue
        im = Image.open(im_path).convert("RGB")
        im.thumbnail((cell_w, thumb_box_h), Image.Resampling.LANCZOS)

        px = x + (cell_w - im.size[0]) // 2
        py = y + (thumb_box_h - im.size[1]) // 2
        sheet.paste(im, (px, py))

        draw.rectangle([(x, y), (x + cell_w, y + cell_h)], outline=(56, 189, 248), width=2)
        draw.rectangle([(x, y + thumb_box_h), (x + cell_w, y + cell_h)], fill=(11, 16, 29))

        cred = credits_map.get(f, "")
        cap_text = f"{f} | ẢNH: {cred} ({im.size[0]}x{im.size[1]})"
        draw.text((x + 10, y + thumb_box_h + 18), cap_text, fill=(255, 255, 255))

    out_sheet = os.path.join(QA_DIR, "contact_scene_04.jpg")
    sheet.save(out_sheet, "JPEG", quality=90)
    ok(f"QA Contact Sheet đã lưu: {paths.rel_to_root(out_sheet)}")


def render_short_video(force: bool = False) -> Optional[str]:
    banner("DỰNG VIDEO SHORT 9:16 (FENERBAHCE 3-2 LIVERPOOL)", DAY_STR)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(SHORTS_WORK, exist_ok=True)

    t0 = time.time()
    out_path = os.path.join(SHORTS_OUT, SHORT_CFG["file_name"])

    if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
        ok(f"Short đã có sẵn: {paths.rel_to_root(out_path)}")
        return out_path

    step("Xuất timeline short cho Tin 04 (Liverpool 2-3 Fenerbahce)...")
    pdir, _, _ = export_bridge_project(
        DAY_DIR,
        item_id=4,
        format_type="short",
        work_proj_dir=os.path.join(SHORTS_WORK, "short_liverpool"),
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
    banner("TẠO ẢNH THUMBNAIL DỌC 9:16 CHO SHORT (LIVERPOOL)", DAY_STR)
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
    width:100%; height:100%; object-fit:cover; object-position:center 30%;
    filter: contrast(1.18) brightness(1.05) saturate(1.2);
  }
  .top::after {
    content:''; position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(5,7,12,0.2) 0%, transparent 25%, rgba(5,7,12,0.7) 70%, #05070C 100%);
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
  .sub {
    font-family:'Oswald'; font-weight:700; font-size:44px; line-height:1.15;
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
        h_content = h_content.replace("__THUMB_HERO_SIZE__", SHORT_CFG.get("thumb_hero_size", "130"))
        h_content = h_content.replace("__THUMB_SUBTITLE__", SHORT_CFG["thumb_sub"])
        h_content = h_content.replace("__THUMB_TAG_A__", SHORT_CFG["thumb_tag_a"])
        h_content = h_content.replace("__THUMB_TAG_B__", SHORT_CFG["thumb_tag_b"])

        tmp_html_file = os.path.join(thumb_html_dir, "thumb_liverpool.html")
        with open(tmp_html_file, "w", encoding="utf-8") as f:
            f.write(h_content)

        page.goto(paths.file_url(tmp_html_file), wait_until="networkidle")
        page.wait_for_timeout(300)
        page.screenshot(path=out_thumb, type="jpeg", quality=95)
        ok(f"Đã lưu thumbnail: {paths.rel_to_root(out_thumb)} ({os.path.getsize(out_thumb)/(1024):.1f} KB)")
        br.close()


def write_short_metadata():
    banner("XUẤT FILE MÔ TẢ SEO YOUTUBE CHO SHORT (1 TIÊU ĐỀ DUY NHẤT)", DAY_STR)
    out_mota = os.path.join(SHORTS_OUT, SHORT_CFG["mota_name"])

    content = f"""=== TIÊU ĐỀ YOUTUBE ===
{SHORT_CFG['title']}

=== MÔ TẢ VIDEO ===
{SHORT_CFG['desc']}

Đăng ký kênh Điểm Đọc để cập nhật những diễn biến thời sự và câu chuyện thể thao nổi bật mỗi ngày.

{SHORT_CFG['tags']}
"""
    with open(out_mota, "w", encoding="utf-8") as f:
        f.write(content)
    ok(f"Đã lưu mô tả: {paths.rel_to_root(out_mota)}")


def main():
    generate_contact_sheet()
    render_short_thumbnail()
    write_short_metadata()
    render_short_video(force=True)


if __name__ == "__main__":
    main()
