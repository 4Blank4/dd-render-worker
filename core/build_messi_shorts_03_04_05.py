#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_messi_shorts_03_04_05.py — Dựng 3 Video Shorts 9:16 cho Tin 3, Tin 4, Tin 5
(Lionel Messi 30.10.2026) kèm 3 thumbnail dọc (1080x1920) và 3 file mô tả SEO.
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
        "id": 3,
        "slug": "672_Ban_Thang_Di_San_Camp_Nou",
        "file_name": "Short_03_672_Ban_Thang_Di_San_Camp_Nou.mp4",
        "thumb_name": "Short_03_thumbnail.jpg",
        "mota_name": "Short_03_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_03_7.jpg"),
        "thumb_kicker": "KỶ NGUYÊN VÀNG SON CAMP NOU",
        "thumb_hero": "672 BÀN THẮNG!",
        "thumb_hero_size": "105",
        "thumb_sub": "35 DANH HIỆU BẤT DIỆT BARCA",
        "thumb_tag_a": "4 CHAMPIONS LEAGUE",
        "thumb_tag_b": "10 CHỨC VÔ ĐỊCH LA LIGA",
        "titles": [
            "672 Bàn Thắng, 35 Chiếc Cúp: Di Sản Bất Tử Của Messi Tại Camp Nou! 🔵🔴 #Shorts",
            "Vì Sao Kỷ Lục 672 Bàn Của Messi Sẽ Không Bao Giờ Bị Phá Vỡ? ⚡ #Shorts",
            "Cú Ăn 6 Huyền Thoại 2009: Khi Messi & Barcelona Thống Trị Địa Cầu! 👑 #Shorts"
        ],
        "desc": (
            "672 bàn thắng chính thức, 35 chiếc cúp vô địch và một kỷ nguyên vàng son kéo dài 17 năm tại Camp Nou! "
            "Lionel Messi không chỉ chơi bóng cho Barcelona, anh đã định nghĩa lại sự vĩ đại của câu lạc bộ xứ Catalunya. "
            "Cùng Điểm Đọc lật lại di sản bất diệt mà có lẽ hàng thế kỷ nữa bóng đá thế giới cũng khó lòng tái hiện!"
        ),
        "tags": "#LionelMessi #Messi #Barcelona #CampNou #LaLiga #ChampionsLeague #DiemDoc #Shorts #BongDaQuocTe"
    },
    {
        "id": 4,
        "slug": "Ky_Tich_91_Ban_Thang_2012",
        "file_name": "Short_04_Ky_Tich_91_Ban_Thang_2012.mp4",
        "thumb_name": "Short_04_thumbnail.jpg",
        "mota_name": "Short_04_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_04_1.jpg"),
        "thumb_kicker": "KỶ LỤC GUINNESS VÔ TIỀN KHOÁNG HẬU",
        "thumb_hero": "91 BÀN THẮNG!",
        "thumb_hero_size": "110",
        "thumb_sub": "NĂM 2012 ĐIÊN RỒ CỦA LIONEL MESSI",
        "thumb_tag_a": "69 TRẬN ĐẤU",
        "thumb_tag_b": "62 CÚ HAT-TRICK",
        "titles": [
            "91 Bàn Thắng Trong 1 Năm: Kỷ Lục Điên Rồ Nhất Lịch Sử Của Messi! 🤯 #Shorts",
            "Xô Đổ Gerd Müller: Năm 2012 Siêu Nhiên Của Quái Kiệt Lionel Messi! ⚡ #Shorts",
            "62 Cú Hat-trick Suốt Sự Nghiệp: Cơn Ác Mộng Của Mọi Thủ Môn! ⚽ #Shorts"
        ],
        "desc": (
            "91 bàn thắng chỉ trong 69 trận đấu của năm dương lịch 2012! Hiệu suất không tưởng 1.32 bàn/trận đã giúp Lionel Messi "
            "xô đổ kỷ lục tồn tại suốt 40 năm của huyền thoại Gerd Müller, thiết lập kỷ lục Guinness thế giới mà không một tiền đạo nào có thể chạm tới. "
            "Cùng nhìn lại năm thi đấu điên rồ nhất lịch sử túc cầu!"
        ),
        "tags": "#LionelMessi #Messi #91Goals #2012 #HatTrick #Guinness #DiemDoc #Shorts #BongDaQuocTe"
    },
    {
        "id": 5,
        "slug": "936_Ban_466_Kien_Tao_Sieu_Pham_Da_Phat",
        "file_name": "Short_05_936_Ban_466_Kien_Tao_Sieu_Pham_Da_Phat.mp4",
        "thumb_name": "Short_05_thumbnail.jpg",
        "mota_name": "Short_05_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_05_12.jpg"),
        "thumb_kicker": "ÔNG VUA TOÀN DIỆN MỌI THỜI ĐẠI",
        "thumb_hero": "1402 DẤU GIÀY!",
        "thumb_hero_size": "105",
        "thumb_sub": "936 BÀN • 466 KIẾN TẠO • 76 ĐÁ PHẠT",
        "thumb_tag_a": "76 BÀN ĐÁ PHẠT",
        "thumb_tag_b": "VƯỢT TRỘI JUNINHO",
        "titles": [
            "936 Bàn, 466 Kiến Tạo: Vì Sao Messi Là Cầu Thủ Toàn Diện Nhất? 🎯 #Shorts",
            "76 Siêu Phẩm Đá Phạt: Messi Sắp Xô Đổ Kỷ Lục Của Vua Đá Phạt Juninho! ⚡ #Shorts",
            "1402 Lần Ghi Dấu Giày: Con Số Bất Tử Của Huyền Thoại Messi! 👑 #Shorts"
        ],
        "desc": (
            "936 bàn thắng của một số 9 săn bàn hủy diệt kết hợp cùng 466 đường kiến tạo của một số 10 thiên tài kiến thiết! "
            "Chưa dừng lại ở đó, 76 siêu phẩm đá phạt trực tiếp đưa Lionel Messi áp sát cột mốc mọi thời đại của Juninho Pernambucano. "
            "Đó là lý do vì sao thế giới gọi anh là cầu thủ hoàn hảo nhất từng bước ra sân cỏ!"
        ),
        "tags": "#LionelMessi #Messi #FreeKick #Assists #Playmaker #Juninho #DiemDoc #Shorts #BongDaQuocTe"
    }
]


def render_shorts_videos(force: bool = False):
    banner("DỰNG 3 VIDEO SHORTS 9:16 (TIN 3, 4, 5)", DAY_STR)
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

    banner(f"HOÀN THÀNH {len(results)}/3 VIDEO SHORTS ({time.time()-t0:.1f}s)")
    return results


def render_shorts_thumbnails():
    banner("TẠO BỘ 3 ẢNH THUMBNAIL DỌC 9:16 CHO SHORTS 03, 04, 05", DAY_STR)
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
    banner("TẠO FILE MÔ TẢ SEO CHO 3 SHORTS", DAY_STR)
    for cfg in SHORTS_CONFIG:
        mp4_path = os.path.join(SHORTS_OUT, cfg["file_name"])
        dur_str = "80s"
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
            "👇 Bạn ấn tượng nhất với kỷ lục nào của Messi? Hãy để lại bình luận bên dưới nhé!",
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
    banner("TẤT CẢ 3 VIDEO SHORTS + THUMBNAILS + MÔ TẢ ĐÃ HOÀN TẤT!")


if __name__ == "__main__":
    main()
