#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True

import os
from playwright.sync_api import sync_playwright

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

shorts_dir = os.path.join(_ROOT, "outputs", "22.10.2026", "shorts")
assets_url = "file://" + os.path.join(_ROOT, "assets")
logo_url = "file://" + os.path.join(_ROOT, "assets", "logo", "diem-doc-logo-1.png")

thumbs_spec = [
    {
        "file_out": "Short_01_thumbnail.jpg",
        "image": "file://" + os.path.join(_ROOT, "outputs", "22.10.2026", "images", "Tin_04_1.jpg"),
        "kicker": "ĐẠI CHIẾN QUẢ BÓNG VÀNG",
        "hero": "KANE VS YAMAL",
        "hero_size": "115",
        "subtitle": "AI SẼ LÊN ĐỈNH THẾ GIỚI Ở TUỔI 19?",
        "tag_a": "BALLON D'OR 2026",
        "tag_b": "GALA 26.10"
    },
    {
        "file_out": "Short_02_thumbnail.jpg",
        "image": "file://" + os.path.join(_ROOT, "outputs", "22.10.2026", "images", "Tin_06_2.jpg"),
        "kicker": "GĂNG TAY VÀNG THẾ GIỚI",
        "hero": "YASHIN TROPHY",
        "hero_size": "115",
        "subtitle": "ĐẠI CHIẾN THỦ MÔN TÂY BAN NHA",
        "tag_a": "YASHIN & KOPA",
        "tag_b": "ZAMORA VS WC"
    },
    {
        "file_out": "Short_03_thumbnail.jpg",
        "image": "file://" + os.path.join(_ROOT, "outputs", "22.10.2026", "images", "Tin_01_1.jpg"),
        "kicker": "CÚ SỐC LỊCH SỬ 70 NĂM",
        "hero": "RỜI PARIS!",
        "hero_size": "125",
        "subtitle": "GALA TỚI LONDON PALLADIUM",
        "tag_a": "BALLON D'OR 2026",
        "tag_b": "TRI ÂN MATTHEWS"
    }
]

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
    filter: contrast(1.15) brightness(1.02) saturate(1.18);
  }
  .top::after {
    content:''; position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(5,7,12,0.2) 0%, transparent 20%, rgba(5,7,12,0.65) 70%, #05070C 100%);
  }

  .badge {
    position:absolute; top:56px; left:56px; z-index:5;
    display:flex; align-items:center; gap:16px;
    padding:16px 28px; border-radius:999px;
    background:rgba(5,7,12,0.75); border:2px solid rgba(255,194,77,0.8);
    box-shadow: 0 4px 20px rgba(0,0,0,0.6), 0 0 15px rgba(255,194,77,0.3);
    backdrop-filter:blur(12px);
  }
  .badge img { height:40px; width:auto; border-radius:50%; }
  .badge span {
    font-family:'Oswald'; font-weight:700; font-size:24px;
    letter-spacing:4px; color:#FFC24D; text-transform:uppercase;
  }

  /* NỬA DƯỚI: SÂN KHẤU 42% */
  .bottom {
    position:absolute; bottom:0; left:0; right:0; height:43%;
    background:#05070C; padding:40px 70px 70px;
    display:flex; flex-direction:column; justify-content:center;
    border-top: 1px solid rgba(255,194,77,0.15);
  }
  .kicker {
    font-family:'PlexMono'; font-weight:700; font-size:26px;
    letter-spacing:5px; color:#28E0D0; margin-bottom:14px;
    text-transform:uppercase;
    text-shadow: 0 0 12px rgba(40,224,208,0.4);
  }
  .hero {
    font-family:'Anton'; font-size:__THUMB_HERO_SIZE__px; line-height:0.95;
    letter-spacing:1px;
    color:#FFFFFF; white-space:nowrap;
    text-shadow:0 0 50px rgba(255,194,77,0.4), 0 4px 10px rgba(0,0,0,0.8);
  }
  .hero .accent { color:#FFC24D; }
  .sub {
    font-family:'Oswald'; font-weight:700; font-size:46px; line-height:1.15;
    color:#F3F6FF; margin-top:16px; text-transform:uppercase; letter-spacing:1px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
  }
  .rule {
    height:6px; width:180px;
    background:linear-gradient(90deg, #FFC24D 0%, #28E0D0 100%);
    margin:24px 0 20px; border-radius:3px;
    box-shadow: 0 0 10px rgba(255,194,77,0.5);
  }
  .meta {
    display:flex; gap:36px; align-items:center;
    font-family:'PlexMono'; font-size:22px; font-weight:700; letter-spacing:2px;
    color:#94A0BE;
  }
  .meta b { color:#FFC24D; }
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
</html>
"""

def main():
    print("=== TẠO LẠI BỘ 3 ẢNH THUMBNAIL DỌC 9:16 THEO ĐÚNG BẢN CHUẨN THIẾT KẾ ĐẸP TRƯỚC ĐÓ ===")
    os.makedirs(shorts_dir, exist_ok=True)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        page = br.new_page(viewport={"width": 1080, "height": 1920})

        for spec in thumbs_spec:
            html = tpl_html.replace("__ASSETS__", assets_url)
            html = html.replace("__LOGO__", logo_url)
            html = html.replace("__THUMB_IMAGE__", spec["image"])
            html = html.replace("__THUMB_KICKER__", spec["kicker"])
            html = html.replace("__THUMB_HERO__", spec["hero"])
            html = html.replace("__THUMB_HERO_SIZE__", spec["hero_size"])
            html = html.replace("__THUMB_SUBTITLE__", spec["subtitle"])
            html = html.replace("__THUMB_TAG_A__", spec["tag_a"])
            html = html.replace("__THUMB_TAG_B__", spec["tag_b"])

            tmp_html = f"/tmp/{spec['file_out']}.html"
            with open(tmp_html, "w", encoding="utf-8") as f:
                f.write(html)

            out_path = os.path.join(shorts_dir, spec["file_out"])
            page.goto("file://" + tmp_html, wait_until="networkidle")
            page.screenshot(path=out_path, type="jpeg", quality=95)
            print(f"  ✨ Đã khôi phục thumbnail chuẩn: {spec['file_out']} ({os.path.getsize(out_path):,} bytes)")

        br.close()

if __name__ == "__main__":
    main()
