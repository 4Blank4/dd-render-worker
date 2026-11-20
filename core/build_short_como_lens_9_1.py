#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_short_como_lens_9_1.py — Dựng Video Short 9:16 về chiến thắng lịch sử 9-1 của Como
dưới sự dẫn dắt của Cesc Fàbregas trước RC Lens tại Champions League.
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
    "id": 2,
    "item_id": 2,
    "slug": "Short_Como_Thang_Lens_9_1",
    "file_name": "Short_Como_Thang_Lens_9_1.mp4",
    "thumb_name": "Short_Como_Thang_Lens_9_1_thumbnail.jpg",
    "mota_name": "Short_Como_Thang_Lens_9_1_mota.txt",
    "thumb_image": os.path.join(DAY_DIR, "images", "Tin_02_1.jpg"),
    "thumb_kicker": "CHAMPIONS LEAGUE · ĐỊA CHẤN",
    "thumb_hero": "THẮNG 9-1!",
    "thumb_hero_size": "130",
    "thumb_sub": "COMO CỦA FABREGAS LẬP KỶ LỤC LỊCH SỬ CÚP C1",
    "thumb_tag_a": "KỶ LỤC 9 BÀN SÂN KHÁCH",
    "thumb_tag_b": "DOUVIKAS HAT-TRICK",
    "title": "Đội bóng của Cesc Fabregas thắng 9-1 lập kỷ lục Champions League #Shorts",
    "desc": (
        "Địa chấn lịch sử đã bùng nổ tại Champions League khi tân binh Como dưới trướng huấn luyện viên Cesc Fabregas "
        "hủy diệt chủ nhà RC Lens với tỷ số không tưởng 9-1 ngay trên sân khách Bollaert-Delelis.\n\n"
        "Chiến thắng cách biệt tám bàn giúp Como cân bằng kỷ lục thắng đậm nhất lịch sử cúp C1 của Liverpool và Real Madrid, "
        "đồng thời trở thành đội khách đầu tiên ghi tới chín bàn trong một trận đấu. Tiền đạo Anastasios Douvikas rực sáng "
        "với cú hat-trick cùng một kiến tạo, vươn lên dẫn đầu cuộc đua Vua phá lưới Champions League với sáu bàn thắng.\n\n"
        "Đặc biệt, nhạc trưởng Nico Paz tỏa sáng với một bàn và hai kiến tạo, sau đó nghẹn ngào giơ cao chiếc áo in hình "
        "tiền đạo quá cố Jesús de Miguel để tri ân người đàn anh đồng hương Tenerife. Bữa tiệc bàn thắng còn có dấu ấn "
        "của Lucas Da Cunha, Kempf, Baturina, cùng hai tài năng trẻ Mattia Liberali và Matteo Papaccioli 18 tuổi nổ súng "
        "ngay trong trận ra mắt chuyên nghiệp.\n\n"
        "Dưới bàn tay nhào nặn của Cesc Fabregas, Como kiểm soát hoàn toàn với chỉ số 4,27 xG áp đảo. Từ giải hạng Tư Serie D "
        "cách đây mười năm, Como đang viết nên câu chuyện cổ tích kỳ vĩ khi hiên ngang chiếm vị trí thứ tư Champions League "
        "với chín điểm và sở hữu mười chín bàn thắng!"
    ),
    "tags": "#Shorts #DiemDoc #Como #Fabregas #ChampionsLeague #Lens #NicoPaz #Douvikas #DeMiguel #TinBongDa"
}


def generate_contact_sheet():
    banner("TẠO BẢNG ẢNH ĐỐI CHỨNG QA CHO TIN 02 (COMO 9-1 LENS)", DAY_STR)
    os.makedirs(QA_DIR, exist_ok=True)
    img_dir = os.path.join(DAY_DIR, "images")

    credits_map = {}
    cred_file = os.path.join(DAY_DIR, "image_credits.json")
    if os.path.exists(cred_file):
        with open(cred_file, "r", encoding="utf-8") as f:
            credits_map = json.load(f)

    files = [f"Tin_02_{i}.jpg" for i in range(1, 13)]

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
    draw.text((pad, 20), "ĐIỂM ĐỌC QA — BẢNG ĐỐI CHỨNG HÌNH ẢNH: COMO 9-1 RC LENS (05.11.2026)", fill=(0, 229, 255))

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

    out_sheet = os.path.join(QA_DIR, "contact_scene_02.jpg")
    sheet.save(out_sheet, "JPEG", quality=90)
    ok(f"QA Contact Sheet đã lưu: {paths.rel_to_root(out_sheet)}")


def render_short_video(force: bool = False) -> Optional[str]:
    banner("DỰNG VIDEO SHORT 9:16 (COMO 9-1 RC LENS)", DAY_STR)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(SHORTS_WORK, exist_ok=True)

    t0 = time.time()
    out_path = os.path.join(SHORTS_OUT, SHORT_CFG["file_name"])

    if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
        ok(f"Short đã có sẵn: {paths.rel_to_root(out_path)}")
        return out_path

    step("Xuất timeline short cho Tin 02 (Como 9-1 Lens)...")
    pdir, _, _ = export_bridge_project(
        DAY_DIR,
        item_id=2,
        format_type="short",
        work_proj_dir=os.path.join(SHORTS_WORK, "short_como_lens"),
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
    banner("TẠO ẢNH THUMBNAIL DỌC 9:16 CHO SHORT (COMO 9-1)", DAY_STR)
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
    width:100%; height:100%; object-fit:cover; object-position:center 40%;
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

        tmp_html_file = os.path.join(thumb_html_dir, "thumb_como_lens.html")
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
