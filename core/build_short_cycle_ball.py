#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_short_cycle_ball.py — Dựng Video Short 9:16 về môn thể thao độc lạ
Cycle-ball (Bóng đá trên xe đạp) vừa tổ chức giải vô địch thế giới 2026 tại Đức.
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
    "id": 1,
    "item_id": 1,
    "slug": "Short_Bong_Da_Xe_Dap_Cycle_Ball",
    "file_name": "Short_Bong_Da_Xe_Dap_Cycle_Ball.mp4",
    "thumb_name": "Short_Bong_Da_Xe_Dap_Cycle_Ball_thumbnail.jpg",
    "mota_name": "Short_Bong_Da_Xe_Dap_Cycle_Ball_mota.txt",
    "thumb_image": os.path.join(DAY_DIR, "images", "Tin_01_2.jpg"),
    "thumb_kicker": "THỂ THAO ĐỘC LẠ · CYCLE-BALL",
    "thumb_hero": "ĐÁ BÓNG TRÊN XE ĐẠP!",
    "thumb_hero_size": "115",
    "thumb_sub": "CẤM CHẠM CHÂN XUỐNG ĐẤT · SÚT BÓNG BẰNG BÁNH XE",
    "thumb_tag_a": "LỊCH SỬ 140 NĂM",
    "thumb_tag_b": "GIẢI VÔ ĐỊCH THẾ GIỚI",
    "title": "Bóng đá trên xe đạp: Môn thể thao kỳ lạ cấm cầu thủ chạm chân xuống đất #Shorts",
    "desc": (
        "Không cần giày đinh và tuyệt đối không được chạm chân xuống đất, giải vô địch thế giới môn bóng đá trên xe đạp "
        "vừa khép lại đầy nghẹt thở tại nước Đức với chiến thắng 8-1 của đội tuyển Áo!\n\n"
        "Môn thể thao độc lạ này có tên quốc tế là Cycle-ball, hay Radball, nơi mỗi đội gồm hai cầu thủ ngồi trên những chiếc "
        "xe đạp không phanh chuyên dụng. Thay vì dùng chân, họ phải liên tục giữ thăng bằng và dùng bánh xe để rê dắt, chuyền bóng "
        "và nã đại bác vào khung thành đối phương.\n\n"
        "Luật chơi vô cùng khắc nghiệt: nếu bất kỳ ai để chân chạm xuống sàn, họ sẽ bị tước quyền tranh bóng và buộc phải đạp xe "
        "lùi về sau đường biên ngang sân nhà mới được tiếp tục thi đấu!\n\n"
        "Dù trông như một màn xiếc kỳ ảo, môn thể thao này thực chất đã có lịch sử hơn 140 năm và được Liên đoàn Xe đạp Quốc tế UCI công nhận!"
    ),
    "tags": "#Shorts #DiemDoc #CycleBall #Radball #BongDaXeDap #UCI #TheThaoDocLa #WorldChampionship #TinBongDa"
}


def generate_contact_sheet():
    banner("TẠO BẢNG ẢNH ĐỐI CHỨNG QA CHO CYCLE-BALL", DAY_STR)
    os.makedirs(QA_DIR, exist_ok=True)
    out_contact = os.path.join(QA_DIR, "contact_scene_01.jpg")

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
    title_text = "QA CONTACT SHEET — BÓNG ĐÁ TRÊN XE ĐẠP (CYCLE-BALL / RADBALL 2026)"
    draw.text((pad, 22), title_text, fill=(0, 229, 255))

    for idx in range(1, 13):
        r = (idx - 1) // cols
        c = (idx - 1) % cols
        x = pad + c * (thumb_w + pad)
        y = header_h + pad + r * (thumb_h + footer_h + pad)

        fn = f"Tin_01_{idx}.jpg"
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
    banner("TẠO ẢNH THUMBNAIL DỌC 9:16 CHO SHORT (CYCLE-BALL)", DAY_STR)
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
    background-position: center 25%;
    filter: brightness(0.90) contrast(1.15);
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
        h_content = h_content.replace("__THUMB_HERO_SIZE__", SHORT_CFG.get("thumb_hero_size", "115"))
        h_content = h_content.replace("__THUMB_SUBTITLE__", SHORT_CFG["thumb_sub"])
        h_content = h_content.replace("__THUMB_TAG_A__", SHORT_CFG["thumb_tag_a"])
        h_content = h_content.replace("__THUMB_TAG_B__", SHORT_CFG["thumb_tag_b"])

        tmp_html_file = os.path.join(thumb_html_dir, "thumb_cycle_ball.html")
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
    banner("DỰNG VIDEO SHORT 9:16 (CYCLE-BALL: BÓNG ĐÁ TRÊN XE ĐẠP)", DAY_STR)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(SHORTS_WORK, exist_ok=True)

    t0 = time.time()
    out_path = os.path.join(SHORTS_OUT, SHORT_CFG["file_name"])

    if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
        ok(f"Short đã có sẵn: {paths.rel_to_root(out_path)}")
        return out_path

    step("Xuất timeline short cho Tin 01 (Cycle-ball)...")
    pdir, _, _ = export_bridge_project(
        DAY_DIR,
        item_id=1,
        format_type="short",
        work_proj_dir=os.path.join(SHORTS_WORK, "short_cycle_ball"),
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
