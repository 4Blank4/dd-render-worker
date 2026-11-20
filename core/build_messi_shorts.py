#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_messi_shorts.py — Dựng 2 Video Shorts 9:16 cho Tin 1 và Tin 2 (Lionel Messi 30.10.2026)
kèm 2 thumbnail dọc (1080x1920) và 2 file mô tả SEO.
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
sys.path.insert(0, os.path.join(_HERE, "vendor"))

engines_html = os.path.join(_ROOT, "engines", "html")
if engines_html not in sys.path:
    sys.path.insert(0, engines_html)

from diemdoc import paths
from diemdoc.log import banner, ok, step, log
from m8_news_bridge import export_bridge_project
from renderer import render_html_engine

DAY_STR = "30.10.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, DAY_STR)
WORK_DIR = paths.work_project_dir(DAY_STR)

SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
SHORTS_WORK = os.path.join(WORK_DIR, "special_shorts")

SHORTS_CONFIG = [
    {
        "id": 1,
        "slug": "Messi_Tuoi_39_48_Danh_Hieu",
        "file_name": "Short_01_Messi_Tuoi_39_48_Danh_Hieu.mp4",
        "thumb_name": "Short_01_thumbnail.jpg",
        "mota_name": "Short_01_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_01_1.jpg"),
        "thumb_kicker": "LIONEL MESSI • TUỔI 39",
        "thumb_hero": "48 CHIẾC CÚP!",
        "thumb_hero_size": "115",
        "thumb_sub": "ĐỈNH CAO CÔ ĐỘC LỊCH SỬ",
        "thumb_tag_a": "936 BÀN THẮNG",
        "thumb_tag_b": "1402 LẦN IN DẤU GIÀY",
        "titles": [
            "Messi Tuổi 39: 48 Chiếc Cúp Và Đỉnh Cao Cô Độc Của Lịch Sử! 🏆 #Shorts",
            "1402 Lần In Dấu Giày: Kỷ Lục Bất Tử Của Lionel Messi! ⚡ #Shorts",
            "Ở Tuổi 39, Lionel Messi Vẫn Khiến Cả Thế Giới Ngả Mũ! 👑 #Shorts"
        ],
        "desc": (
            "Tháng 10 năm 2026, Lionel Messi bước sang tuổi 39 nhưng vẫn đứng trên một đỉnh cao cô độc mà thế giới bóng đá chưa từng chứng kiến. "
            "Với 48 danh hiệu tập thể, 936 bàn thắng và 1402 lần in dấu giày trực tiếp vào bàn thắng, người đàn ông ấy đã biến mọi giới hạn thành dĩ vãng! "
            "Cùng Điểm Đọc nhìn lại kỷ lục vĩ đại nhất lịch sử túc cầu của El Pulga!"
        ),
        "tags": "#LionelMessi #Messi #InterMiami #MLS #Argentina #DiemDoc #Shorts #BongDaQuocTe #KyLuc"
    },
    {
        "id": 2,
        "slug": "Ky_Luc_8_Ballon_dOr_Khong_Doi_Thu",
        "file_name": "Short_02_Ky_Luc_8_Ballon_dOr_Khong_Doi_Thu.mp4",
        "thumb_name": "Short_02_thumbnail.jpg",
        "mota_name": "Short_02_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_02_8.jpg"),
        "thumb_kicker": "KỶ LỤC VÔ TIỀN KHOÁNG HẬU",
        "thumb_hero": "8 BALLON D'OR!",
        "thumb_hero_size": "110",
        "thumb_sub": "BỨC TƯỜNG BẤT TỬ CỦA BÓNG ĐÁ",
        "thumb_tag_a": "6 GIÀY VÀNG CHÂU ÂU",
        "thumb_tag_b": "14 NĂM THỐNG TRỊ",
        "titles": [
            "8 Quả Bóng Vàng: Bức Tường Bất Tử Của Lionel Messi! 🌕 #Shorts",
            "Vì Sao Kỷ Lục 8 Ballon d'Or Của Messi Sẽ Không Bao Giờ Bị Phá? ⚡ #Shorts",
            "Từ 22 Tuổi Đến 36 Tuổi: 14 Năm Thống Trị Quả Bóng Vàng Của Messi! 👑 #Shorts"
        ],
        "desc": (
            "Nếu có một thước đo phản ánh sự thống trị tuyệt đối của một cá nhân, thì đó chính là Quả Bóng Vàng — Ballon d'Or. "
            "Khi những huyền thoại vĩ đại nhất chỉ dừng lại ở con số 3 hay 5, Lionel Messi đã đẩy giới hạn lên một tầng cao không tưởng: 8 Quả Bóng Vàng và 6 Chiếc Giày Vàng Châu Âu! "
            "Bức tường kiệt xuất ấy trải dài suốt 14 năm rực rỡ từ Barcelona đến vinh quang cúp vàng thế giới!"
        ),
        "tags": "#LionelMessi #BallondOr #QuaBongVang #GoldenShoe #Barcelona #Argentina #DiemDoc #Shorts"
    }
]


def render_shorts_videos(force: bool = False):
    banner("DỰNG 2 VIDEO SHORTS 9:16 (TIN 1 & TIN 2)", DAY_STR)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(SHORTS_WORK, exist_ok=True)

    t0 = time.time()
    results = []

    for cfg in SHORTS_CONFIG:
        item_id = cfg["id"]
        out_path = os.path.join(SHORTS_OUT, cfg["file_name"])

        if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
            ok(f"Short #{item_id:02d} đã có sẵn: {paths.rel_to_root(out_path)}")
            results.append(out_path)
            continue

        step(f"Xuất timeline short cho Tin {item_id:02d}...")
        pdir, _, _ = export_bridge_project(
            DAY_DIR,
            item_id=item_id,
            format_type="short",
            work_proj_dir=os.path.join(SHORTS_WORK, f"short_{item_id:02d}"),
            global_offset_sec=0.0
        )

        step(f"Render 9:16 cho Tin {item_id:02d} trên template short_news_v2.html (30fps)...")
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
            ok(f"🎉 Hoàn thành Short {item_id:02d}: {paths.rel_to_root(out_path)} ({os.path.getsize(out_path)/(1024*1024):.1f} MB)")
            results.append(out_path)
        else:
            log(f"!! Render Short {item_id:02d} thất bại", tag="shorts")

    banner(f"HOÀN THÀNH {len(results)}/2 VIDEO SHORTS ({time.time()-t0:.1f}s)")
    return results


def render_shorts_thumbnails():
    banner("TẠO BỘ 2 ẢNH THUMBNAIL DỌC 9:16 CHO SHORTS", DAY_STR)
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
    filter: contrast(1.12) brightness(1.05) saturate(1.18);
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
            "--no-sandbox",
            "--allow-file-access-from-files",
            "--disable-dev-shm-usage"
        ])
        page = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)

        for cfg in SHORTS_CONFIG:
            step(f"Render thumbnail dọc cho {cfg['slug']}...")
            c_html = tpl_html
            c_html = c_html.replace("__THUMB_IMAGE__", paths.file_url(cfg["thumb_image"]))
            c_html = c_html.replace("__THUMB_KICKER__", cfg["thumb_kicker"])
            c_html = c_html.replace("__THUMB_HERO__", cfg["thumb_hero"])
            c_html = c_html.replace("__THUMB_HERO_SIZE__", cfg["thumb_hero_size"])
            c_html = c_html.replace("__THUMB_SUBTITLE__", cfg["thumb_sub"])
            c_html = c_html.replace("__THUMB_TAG_A__", cfg["thumb_tag_a"])
            c_html = c_html.replace("__THUMB_TAG_B__", cfg["thumb_tag_b"])

            fn_html = os.path.join(thumb_html_dir, f"{cfg['slug']}_thumb.html")
            with open(fn_html, "w", encoding="utf-8") as f:
                f.write(c_html)

            fn_out = os.path.join(SHORTS_OUT, cfg["thumb_name"])
            page.goto(paths.file_url(fn_html), wait_until="networkidle")
            page.wait_for_timeout(600)
            page.screenshot(path=fn_out, type="jpeg", quality=95)
            ok(f"Thumbnail dọc: {paths.rel_to_root(fn_out)} ({os.path.getsize(fn_out)/1024:.1f} KB)")

        br.close()


def write_shorts_mota():
    banner("TẠO FILE MÔ TẢ SEO CHO 2 SHORTS", DAY_STR)
    for cfg in SHORTS_CONFIG:
        mp4_path = os.path.join(SHORTS_OUT, cfg["file_name"])
        dur_str = "81s"
        if os.path.exists(mp4_path):
            try:
                from diemdoc.audio import _get_media_duration
                dur = _get_media_duration(mp4_path)
                dur_str = f"{dur:.2f}s"
            except Exception:
                pass

        mota_path = os.path.join(SHORTS_OUT, cfg["mota_name"])
        lines = [
            f"Tệp tin: {cfg['file_name']} ({dur_str})",
            f"Thumbnail: {cfg['thumb_name']}",
            "",
            "=== TIÊU ĐỀ GỢI Ý (CHỌN 1) ===",
        ]
        for i, t in enumerate(cfg["titles"], start=1):
            lines.append(f"{i}. {t}")

        lines.extend([
            "",
            "=== MÔ TẢ (DESCRIPTION) ===",
            cfg["desc"],
            "",
            "👇 Theo bạn, ai có thể phá được kỷ lục này của Messi trong 50 năm tới? Để lại bình luận bên dưới nhé!",
            "👉 Bấm Like, Đăng ký kênh Điểm Đọc và bật chuông thông báo để không bỏ lỡ chuyên đề thể thao sâu!",
            "",
            "=== HASHTAGS ===",
            cfg["tags"],
            ""
        ])

        with open(mota_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        ok(f"Mô tả SEO: {paths.rel_to_root(mota_path)}")


def main():
    force = "--force" in sys.argv[1:]
    render_shorts_videos(force=force)
    render_shorts_thumbnails()
    write_shorts_mota()
    banner("TẤT CẢ 2 VIDEO SHORTS + THUMBNAILS + MÔ TẢ ĐÃ HOÀN TẤT!")


if __name__ == "__main__":
    main()
