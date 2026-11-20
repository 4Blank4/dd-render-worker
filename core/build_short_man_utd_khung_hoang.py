#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_short_man_utd_khung_hoang.py — Dựng Video Short 9:16 về cuộc khủng hoảng phong độ
của Manchester United: Dẫn đầu giải về số cú sút nhưng chỉ ghi 10 bàn và đứng thứ 17.
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

DAY_STR = "07.11.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, "Orther", DAY_STR)
WORK_DIR = paths.work_project_dir(os.path.join("Orther", DAY_STR))

SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
SHORTS_WORK = os.path.join(WORK_DIR, "shorts_render")
QA_DIR = os.path.join(DAY_DIR, "qa")

SHORT_CFG = {
    "id": 2,
    "item_id": 2,
    "slug": "Short_Man_Utd_Khung_Hoang_Phong_Do",
    "file_name": "Short_Man_Utd_Khung_Hoang_Phong_Do.mp4",
    "thumb_name": "Short_Man_Utd_Khung_Hoang_Phong_Do_thumbnail.jpg",
    "mota_name": "Short_Man_Utd_Khung_Hoang_Phong_Do_mota.txt",
    "thumb_image": os.path.join(DAY_DIR, "images", "Tin_02_1.jpg"),
    "thumb_kicker": "NGOẠI HẠNG ANH · BÁO ĐỘNG",
    "thumb_hero": "NGHỊCH LÝ MAN UTD!",
    "thumb_hero_size": "110",
    "thumb_sub": "SÚT NHIỀU NHẤT GIẢI NHƯNG ĐỨNG THỨ 17 ÁP SÁT NHÓM ĐÈN ĐỎ",
    "thumb_tag_a": "167 CÚ SÚT · 10 BÀN",
    "thumb_tag_b": "LIÊN HỆ DESCHAMPS",
    "title": "Nghịch lý Man Utd: Sút nhiều nhất Ngoại hạng Anh nhưng chạm đáy khủng hoảng #Shorts",
    "desc": (
        "Dẫn đầu Ngoại hạng Anh với 167 cú dứt điểm sau chín vòng đấu nhưng mới chỉ ghi được 10 bàn thắng, "
        "Manchester United đang trải qua một trong những cuộc khủng hoảng phong độ tồi tệ nhất lịch sử hiện đại!\n\n"
        "Vị trí thứ 17 áp sát nhóm xuống hạng đã phơi bày sự bế tắc khó tin của hàng công Quỷ đỏ. Dù thắng ngược Roma 3-2 "
        "tại Champions League tạm thời cứu chiếc ghế của Michael Carrick, nhưng ban lãnh đạo Old Trafford được cho đã bí mật "
        "thăm dò cựu HLV tuyển Pháp Didier Deschamps đúng dịp kỷ niệm 40 năm ngày Sir Alex Ferguson tiếp quản đội bóng.\n\n"
        "Giữa tâm bão, phát ngôn của đồng sở hữu Avram Glazer ví MU như đội bóng Mỹ vẫn hái ra tiền dù không có danh hiệu "
        "càng khiến các cổ động viên tại Manchester vô cùng phẫn nộ!"
    ),
    "tags": "#Shorts #DiemDoc #ManUtd #ManchesterUnited #MU #Carrick #Ferguson #Deschamps #Glazer #NgoaiHangAnh #TinBongDa"
}


def generate_contact_sheet():
    banner("TẠO BẢNG ẢNH ĐỐI CHỨNG QA CHO MAN UTD", DAY_STR)
    os.makedirs(QA_DIR, exist_ok=True)
    out_contact = os.path.join(QA_DIR, "contact_scene_02.jpg")

    with open(os.path.join(DAY_DIR, "image_credits.json"), "r", encoding="utf-8") as f:
        credits_map = json.load(f)

    cols = 3
    rows = 4
    thumb_w, thumb_h = 360, 220
    pad = 16
    header_h = 70
    footer_h = 36

    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = rows * (thumb_h + footer_h) + (rows + 1) * pad + header_h

    sheet = Image.new("RGB", (sheet_w, sheet_h), (11, 15, 25))
    draw = ImageDraw.Draw(sheet)

    draw.rectangle([(0, 0), (sheet_w, header_h)], fill=(16, 24, 40))
    title_text = "QA CONTACT SHEET — TIN 02: MANCHESTER UNITED KHỦNG HOẢNG PHONG ĐỘ"
    draw.text((pad, 22), title_text, fill=(0, 229, 255))

    for idx in range(1, 13):
        r = (idx - 1) // cols
        c = (idx - 1) % cols
        x = pad + c * (thumb_w + pad)
        y = header_h + pad + r * (thumb_h + footer_h + pad)

        fn = f"Tin_02_{idx}.jpg"
        img_p = os.path.join(DAY_DIR, "images", fn)
        if os.path.exists(img_p):
            im = Image.open(img_p).convert("RGB")
            im.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            bx = x + (thumb_w - im.width) // 2
            by = y + (thumb_h - im.height) // 2
            sheet.paste(im, (bx, by))
            draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], outline=(30, 41, 59), width=2)
        else:
            draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], fill=(20, 25, 35))

        cr = credits_map.get(fn, "TƯ LIỆU")
        cap_y = y + thumb_h + 4
        draw.rectangle([(x, cap_y), (x + thumb_w, cap_y + 28)], fill=(15, 23, 42))
        draw.text((x + 6, cap_y + 4), f"{fn} | {cr}", fill=(226, 232, 240))

    sheet.save(out_contact, "JPEG", quality=92)
    ok(f"QA Contact Sheet đã lưu: {paths.rel_to_root(out_contact)}")


def render_short_thumbnail():
    banner("TẠO ẢNH THUMBNAIL DỌC 9:16 CHO SHORT (MAN UTD)", DAY_STR)
    tpl_html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1080px;
    height: 1920px;
    background: #060911;
    font-family: 'Barlow', 'Be Vietnam Pro', sans-serif;
    position: relative;
    overflow: hidden;
    color: #fff;
  }
  .bg-img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('__THUMB_IMAGE__');
    background-size: cover;
    background-position: center top;
    filter: brightness(0.85) contrast(1.15);
  }
  .gradient-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg,
      rgba(6,9,17,0.75) 0%,
      rgba(6,9,17,0.05) 25%,
      rgba(6,9,17,0.25) 50%,
      rgba(6,9,17,0.92) 78%,
      #060911 100%
    );
  }
  .glow-cyan {
    position: absolute;
    width: 800px;
    height: 800px;
    background: radial-gradient(circle, rgba(0,229,255,0.25) 0%, transparent 70%);
    top: 50%;
    left: 50%;
    transform: translate(-50%, -35%);
    filter: blur(80px);
    pointer-events: none;
  }
  .header-badge {
    position: absolute;
    top: 90px;
    left: 60px;
    right: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .logo-box {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(15, 23, 42, 0.85);
    padding: 12px 24px;
    border-radius: 999px;
    border: 1px solid rgba(0, 229, 255, 0.4);
    box-shadow: 0 4px 20px rgba(0, 229, 255, 0.2);
  }
  .logo-dot {
    width: 16px;
    height: 16px;
    background: #00E5FF;
    border-radius: 50%;
    box-shadow: 0 0 12px #00E5FF;
  }
  .logo-text {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #fff;
  }
  .kicker-tag {
    background: rgba(0, 229, 255, 0.15);
    border: 1px solid #00E5FF;
    padding: 10px 24px;
    border-radius: 999px;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #00E5FF;
    text-transform: uppercase;
  }
  .content-bottom {
    position: absolute;
    bottom: 120px;
    left: 60px;
    right: 60px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  .hero-title {
    font-size: __THUMB_HERO_SIZE__px;
    font-weight: 900;
    line-height: 1.02;
    text-transform: uppercase;
    color: #FFFFFF;
    text-shadow: 0 0 35px rgba(0, 229, 255, 0.65), 0 4px 20px rgba(0,0,0,0.9);
    letter-spacing: -1px;
  }
  .sub-title {
    font-size: 36px;
    font-weight: 700;
    line-height: 1.3;
    color: #E2E8F0;
    background: rgba(15, 23, 42, 0.88);
    padding: 18px 24px;
    border-radius: 16px;
    border-left: 6px solid #00E5FF;
    backdrop-filter: blur(8px);
  }
  .tag-row {
    display: flex;
    gap: 16px;
  }
  .stat-pill {
    background: rgba(30, 41, 59, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 12px 24px;
    border-radius: 12px;
    font-size: 26px;
    font-weight: 800;
    color: #38BDF8;
    letter-spacing: 1px;
  }
</style>
</head>
<body>
  <div class="bg-img"></div>
  <div class="gradient-overlay"></div>
  <div class="glow-cyan"></div>

  <div class="header-badge">
    <div class="logo-box">
      <div class="logo-dot"></div>
      <div class="logo-text">ĐIỂM ĐỌC THỂ THAO</div>
    </div>
    <div class="kicker-tag">__THUMB_KICKER__</div>
  </div>

  <div class="content-bottom">
    <div class="hero-title">__THUMB_HERO__</div>
    <div class="sub-title">__THUMB_SUBTITLE__</div>
    <div class="tag-row">
      <div class="stat-pill">__THUMB_TAG_A__</div>
      <div class="stat-pill">__THUMB_TAG_B__</div>
    </div>
  </div>
</body>
</html>
"""
    thumb_html_dir = os.path.join(WORK_DIR, "thumb_render")
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
        h_content = h_content.replace("__THUMB_HERO_SIZE__", SHORT_CFG.get("thumb_hero_size", "110"))
        h_content = h_content.replace("__THUMB_SUBTITLE__", SHORT_CFG["thumb_sub"])
        h_content = h_content.replace("__THUMB_TAG_A__", SHORT_CFG["thumb_tag_a"])
        h_content = h_content.replace("__THUMB_TAG_B__", SHORT_CFG["thumb_tag_b"])

        tmp_html_file = os.path.join(thumb_html_dir, "thumb_man_utd.html")
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


def render_short_video(force: bool = False) -> Optional[str]:
    banner("DỰNG VIDEO SHORT 9:16 (MANCHESTER UNITED KHỦNG HOẢNG)", DAY_STR)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(SHORTS_WORK, exist_ok=True)

    t0 = time.time()
    out_path = os.path.join(SHORTS_OUT, SHORT_CFG["file_name"])

    if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
        ok(f"Short đã có sẵn: {paths.rel_to_root(out_path)}")
        return out_path

    step("Xuất timeline short cho Tin 02 (Man Utd)...")
    pdir, _, _ = export_bridge_project(
        DAY_DIR,
        item_id=2,
        format_type="short",
        work_proj_dir=os.path.join(SHORTS_WORK, "short_man_utd"),
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
        banner(f"HOÀN THÀNH VIDEO SHORT ({time.time() - t0:.1f}s)", DAY_STR)
        return out_path
    else:
        log("❌ Render thất bại!")
        return None


def main():
    generate_contact_sheet()
    render_short_thumbnail()
    write_short_metadata()
    render_short_video(force=True)


if __name__ == "__main__":
    main()
