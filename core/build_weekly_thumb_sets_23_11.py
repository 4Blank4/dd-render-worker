#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_weekly_thumb_sets_23_11.py — Dựng 2 Bộ Thumbnail & Mô Tả Hoàn Toàn Mới Cho Video Tuần (Weekly-23.11.2026)
=================================================================================================================
Không ghi đè bất kỳ tệp nào đã xuất bản trong `outputs/Weekly-23.11.2026/`.
Lưu 2 bộ lựa chọn độc lập vào `outputs/Weekly-23.11.2026/thumbnails_options/`:
  - `bo_1_weekly_magazine/`: Phong cách Tạp Chí Thể Thao Tuần (Gold/Navy, ghép 3 ảnh đa sự kiện tuần).
  - `bo_2_clash_impact/`: Phong cách Đối Đầu Tương Phản Mạnh (Diagonal Split 50/50 Đỏ/Trắng Bạc/Đen Carbon).
Mỗi bộ gồm đầy đủ: 3 thumbnail ngang 16:9 (`thumbnail_A/B/C.jpg`), 1 thumbnail dọc 9:16 (`short_thumbnail.jpg`),
và bộ tiêu đề + mô tả SEO tách biệt (`mota_long.txt`, `mota_short.txt`) chuẩn tuần `16–22/11 (cập nhật 23/11)`.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple
from playwright.sync_api import sync_playwright

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc import paths
from diemdoc.log import banner, ok, step
from diemdoc.publisher import write_mota_16x9, write_mota_9x16

ROOT = Path(_ROOT)
DAY_STR = "Weekly-23.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
IMG_DIR = OUT_DIR / "images"
OPT_ROOT = OUT_DIR / "thumbnails_options"
SET1_DIR = OPT_ROOT / "bo_1_weekly_magazine"
SET2_DIR = OPT_ROOT / "bo_2_clash_impact"
LOGO_URL = paths.file_url(str(ROOT / "assets" / "logo" / "diem-doc-logo-1.png"))
ASSETS_URL = paths.file_url(paths.ASSETS)


def _img_url(fn: str) -> str:
    p = IMG_DIR / fn
    if not p.exists():
        raise FileNotFoundError(f"Thiếu ảnh nguồn: {p}")
    return paths.file_url(str(p))


# ==============================================================================
# HTML BỘ 1: WEEKLY SPORTS MAGAZINE (BENTO 3 KHUNG + VÀNG GOLD & NAVY)
# ==============================================================================
def _html_set1_16x9(var: Dict[str, Any]) -> str:
    cards_html = ""
    for i, card in enumerate(var["cards"]):
        accent = ["#FACC15", "#38BDF8", "#F43F5E"][i % 3]
        cards_html += f"""
        <div class="m-card" style="border-color: {accent};">
          <img src="{_img_url(card['file'])}" style="object-position: {card.get('pos', 'center 20%')};">
          <div class="m-card-grad"></div>
          <div class="m-card-tag" style="background: {accent};">{card['tag']}</div>
        </div>
        """
    return f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8">
<style>
  @font-face {{ font-family:'Anton'; src:url('{ASSETS_URL}/fonts/Anton/Anton-Regular.ttf'); font-weight:400; font-display:block; }}
  @font-face {{ font-family:'Oswald'; src:url('{ASSETS_URL}/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; font-display:block; }}
  @font-face {{ font-family:'Montserrat'; src:url('{ASSETS_URL}/fonts/Montserrat/static/Montserrat-Bold.ttf'); font-weight:700; font-display:block; }}
  @font-face {{ font-family:'PlexMono'; src:url('{ASSETS_URL}/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'); font-weight:700; font-display:block; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{
    width:1920px; height:1080px; overflow:hidden;
    background: radial-gradient(circle at 50% 0%, #172554 0%, #090F24 58%, #040711 100%);
    color:#FFF; font-family:'Oswald',sans-serif;
  }}
  .wrap {{ width:1920px; height:1080px; padding:34px 48px 36px; display:flex; flex-direction:column; justify-content:space-between; position:relative; }}
  .top-strip {{
    display:flex; align-items:center; justify-content:space-between; height:64px;
  }}
  .top-left {{ display:flex; align-items:center; gap:18px; }}
  .week-ribbon {{
    background: linear-gradient(90deg, #FACC15 0%, #F59E0B 100%);
    color:#070B14; font-family:'Oswald',sans-serif; font-weight:700; font-size:29px;
    letter-spacing:2px; padding:10px 26px; border-radius:10px;
    box-shadow: 0 6px 24px rgba(250,204,21,0.35);
    text-transform:uppercase;
  }}
  .pill-sub {{
    background: rgba(15,23,42,0.88); border:2px solid rgba(56,189,248,0.65);
    color:#38BDF8; font-family:'PlexMono',monospace; font-weight:700; font-size:21px;
    letter-spacing:1.5px; padding:10px 20px; border-radius:10px; text-transform:uppercase;
  }}
  .brand-pill {{
    display:flex; align-items:center; gap:12px; background:rgba(10,16,32,0.92);
    border:2px solid rgba(250,204,21,0.55); border-radius:999px; padding:8px 24px 8px 12px;
  }}
  .brand-pill img {{ width:40px; height:40px; border-radius:50%; }}
  .brand-pill span {{ font-size:24px; font-weight:700; letter-spacing:3px; color:#FACC15; }}

  .cards-row {{
    display:grid; grid-template-columns: repeat(3, 1fr); gap:24px; height:575px; margin-top:14px;
  }}
  .m-card {{
    position:relative; border-radius:20px; overflow:hidden; border:4px solid #FACC15;
    box-shadow: 0 18px 40px rgba(0,0,0,0.65); background:#0B1224;
  }}
  .m-card img {{ width:100%; height:100%; object-fit:cover; filter:contrast(1.07) saturate(1.12); }}
  .m-card-grad {{
    position:absolute; inset:0;
    background: linear-gradient(180deg, transparent 58%, rgba(4,7,17,0.90) 100%);
  }}
  .m-card-tag {{
    position:absolute; left:18px; bottom:18px; color:#050812; font-family:'Oswald',sans-serif;
    font-weight:700; font-size:24px; letter-spacing:1.5px; padding:6px 18px; border-radius:8px;
    text-transform:uppercase; box-shadow:0 4px 14px rgba(0,0,0,0.5);
  }}

  .typo-stage {{
    background: linear-gradient(135deg, rgba(15,23,42,0.96) 0%, rgba(10,16,34,0.96) 100%);
    border: 2.5px solid rgba(250,204,21,0.45);
    border-left: 14px solid #FACC15;
    border-radius: 18px;
    padding: 24px 36px 26px;
    display:flex; flex-direction:column; gap:10px;
    box-shadow: 0 18px 44px rgba(0,0,0,0.7);
  }}
  .hl-line-1 {{
    font-family:'Anton',sans-serif; font-size:{var.get('l1_size', 94)}px; line-height:1.05;
    letter-spacing:1.5px; text-transform:uppercase; color:#FACC15;
    text-shadow: 0 6px 20px rgba(0,0,0,0.7);
  }}
  .hl-line-2 {{
    font-family:'Anton',sans-serif; font-size:{var.get('l2_size', 78)}px; line-height:1.06;
    letter-spacing:1px; text-transform:uppercase; color:#FFFFFF;
  }}
  .sub-line {{
    font-family:'Montserrat',sans-serif; font-weight:700; font-size:27px; color:#CBD5E1;
    letter-spacing:0.6px; text-transform:uppercase; margin-top:4px;
  }}
</style></head>
<body>
<div class="wrap">
  <div class="top-strip">
    <div class="top-left">
      <div class="week-ribbon">{var['ribbon']}</div>
      <div class="pill-sub">{var['pill']}</div>
    </div>
    <div class="brand-pill">
      <img src="{LOGO_URL}">
      <span>ĐIỂM ĐỌC TUẦN</span>
    </div>
  </div>
  <div class="cards-row">{cards_html}</div>
  <div class="typo-stage">
    <div class="hl-line-1">{var['line1']}</div>
    <div class="hl-line-2">{var['line2']}</div>
    <div class="sub-line">{var['subtitle']}</div>
  </div>
</div>
</body></html>"""


def _html_set1_9x16() -> str:
    return f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8">
<style>
  @font-face {{ font-family:'Anton'; src:url('{ASSETS_URL}/fonts/Anton/Anton-Regular.ttf'); font-weight:400; font-display:block; }}
  @font-face {{ font-family:'Oswald'; src:url('{ASSETS_URL}/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; font-display:block; }}
  @font-face {{ font-family:'Montserrat'; src:url('{ASSETS_URL}/fonts/Montserrat/static/Montserrat-Bold.ttf'); font-weight:700; font-display:block; }}
  @font-face {{ font-family:'PlexMono'; src:url('{ASSETS_URL}/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'); font-weight:700; font-display:block; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{
    width:1080px; height:1920px; overflow:hidden;
    background: radial-gradient(circle at 50% 10%, #1E3A8A 0%, #091026 55%, #040711 100%);
    color:#FFF; font-family:'Oswald',sans-serif;
  }}
  .wrap {{ width:1080px; height:1920px; padding:48px 42px; display:flex; flex-direction:column; justify-content:space-between; }}
  .hdr {{ display:flex; justify-content:space-between; align-items:center; }}
  .ribbon {{
    background:linear-gradient(90deg,#FACC15,#F59E0B); color:#070B14; font-size:28px;
    font-weight:700; padding:10px 24px; border-radius:10px; letter-spacing:1.8px;
  }}
  .brand {{
    display:flex; align-items:center; gap:10px; background:rgba(10,16,32,0.92);
    border:2px solid rgba(250,204,21,0.6); border-radius:999px; padding:8px 20px 8px 10px;
  }}
  .brand img {{ width:38px; height:38px; border-radius:50%; }}
  .brand span {{ font-size:22px; font-weight:700; letter-spacing:2px; color:#FACC15; }}

  .grid-3 {{ display:flex; flex-direction:column; gap:18px; height:1060px; margin:20px 0; }}
  .tile {{
    position:relative; flex:1; border-radius:20px; overflow:hidden; border:4px solid #FACC15;
    box-shadow:0 16px 36px rgba(0,0,0,0.65);
  }}
  .tile img {{ width:100%; height:100%; object-fit:cover; filter:contrast(1.07) saturate(1.12); }}
  .tile::after {{ content:''; position:absolute; inset:0; background:linear-gradient(90deg,rgba(4,7,17,0.72) 0%, transparent 55%); }}
  .t-badge {{
    position:absolute; left:20px; bottom:20px; z-index:3; padding:8px 20px; border-radius:8px;
    font-size:26px; font-weight:700; color:#050812; letter-spacing:1.2px;
  }}

  .panel {{
    background:rgba(10,16,34,0.96); border:3px solid rgba(250,204,21,0.55);
    border-left:14px solid #FACC15; border-radius:20px; padding:28px 32px;
    display:flex; flex-direction:column; gap:16px;
  }}
  .kicker {{ font-family:'PlexMono',monospace; font-size:23px; color:#38BDF8; letter-spacing:1.5px; margin-bottom:2px; }}
  .h1 {{ font-family:'Anton',sans-serif; font-size:88px; line-height:1.10; padding-top:4px; color:#FACC15; }}
  .h2 {{ font-family:'Anton',sans-serif; font-size:74px; line-height:1.08; color:#FFFFFF; }}
  .sub {{ font-family:'Montserrat',sans-serif; font-size:25px; font-weight:700; color:#CBD5E1; margin-top:2px; }}
</style></head>
<body>
<div class="wrap">
  <div class="hdr">
    <div class="ribbon">TỔNG HỢP TUẦN • 16–22/11</div>
    <div class="brand"><img src="{LOGO_URL}"><span>ĐIỂM ĐỌC</span></div>
  </div>
  <div class="grid-3">
    <div class="tile" style="border-color:#FACC15;">
      <img src="{_img_url('Tin_02_1.jpg')}" style="object-position:center 18%;">
      <div class="t-badge" style="background:#FACC15;">U17 VIỆT NAM 2-3 BỈ</div>
    </div>
    <div class="tile" style="border-color:#EF4444;">
      <img src="{_img_url('Tin_13_1.jpg')}" style="object-position:center 28%;">
      <div class="t-badge" style="background:#EF4444; color:#FFF;">HARRY KANE CHẤN THƯƠNG NẶNG</div>
    </div>
    <div class="tile" style="border-color:#38BDF8;">
      <img src="{_img_url('Tin_17_4.jpg')}" style="object-position:center 68%;">
      <div class="t-badge" style="background:#38BDF8;">ALCARAZ VÔ ĐỊCH ATP FINALS</div>
    </div>
  </div>
  <div class="panel">
    <div class="kicker">20 TIN NÓNG TUẦN QUA • MỞ ĐẦU ĐẶC BIỆT</div>
    <div class="h1">TOÀN CẢNH TUẦN QUA</div>
    <div class="h2">VIỆT NAM & THẾ GIỚI</div>
    <div class="sub">ĐẠI HỘI 2026 • ĐÌNH BẮC • MÁRQUEZ • CẬP NHẬT 23/11</div>
  </div>
</div>
</body></html>"""


# ==============================================================================
# HTML BỘ 2: HIGH-CONTRAST DIAGONAL CLASH (ĐỐI KHÁNG ĐỎ/TRẮNG BẠC/ĐEN CARBON)
# ==============================================================================
def _html_set2_16x9(var: Dict[str, Any]) -> str:
    return f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8">
<style>
  @font-face {{ font-family:'Anton'; src:url('{ASSETS_URL}/fonts/Anton/Anton-Regular.ttf'); font-weight:400; font-display:block; }}
  @font-face {{ font-family:'Oswald'; src:url('{ASSETS_URL}/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; font-display:block; }}
  @font-face {{ font-family:'Montserrat'; src:url('{ASSETS_URL}/fonts/Montserrat/static/Montserrat-Bold.ttf'); font-weight:700; font-display:block; }}
  @font-face {{ font-family:'PlexMono'; src:url('{ASSETS_URL}/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'); font-weight:700; font-display:block; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1920px; height:1080px; overflow:hidden; background:#090B10; color:#FFF; font-family:'Oswald',sans-serif; }}
  .stage {{ position:relative; width:1920px; height:1080px; overflow:hidden; }}

  .left-pane {{
    position:absolute; inset:0; width:56%; height:100%;
    clip-path: polygon(0 0, 100% 0, 82% 100%, 0 100%);
    overflow:hidden; background:#111827;
  }}
  .right-pane {{
    position:absolute; top:0; right:0; width:56%; height:100%;
    clip-path: polygon(18% 0, 100% 0, 100% 100%, 0 100%);
    overflow:hidden; background:#1F1215;
  }}
  .left-pane img, .right-pane img {{
    width:100%; height:100%; object-fit:cover; filter:contrast(1.10) saturate(1.16);
  }}
  .shade-bot {{
    position:absolute; left:0; right:0; bottom:0; height:520px; z-index:4;
    background: linear-gradient(180deg, transparent 0%, rgba(9,11,16,0.72) 45%, rgba(9,11,16,0.98) 100%);
  }}
  .shade-top {{
    position:absolute; left:0; right:0; top:0; height:180px; z-index:4;
    background: linear-gradient(180deg, rgba(9,11,16,0.88) 0%, transparent 100%);
  }}
  .slash-beam {{
    position:absolute; top:-60px; bottom:-60px; left:50%; width:14px; z-index:5;
    transform: translateX(-50%) rotate(9.8deg);
    background: linear-gradient(180deg, #FFFFFF 0%, #EF4444 50%, #FACC15 100%);
    box-shadow: 0 0 32px rgba(239,68,68,0.95), 0 0 14px rgba(255,255,255,0.9);
  }}

  .top-bar {{
    position:absolute; top:38px; left:54px; right:54px; z-index:10;
    display:flex; justify-content:space-between; align-items:center;
  }}
  .week-stamp {{
    display:flex; align-items:center; gap:14px;
  }}
  .stamp-red {{
    background:#DC2626; color:#FFFFFF; font-size:30px; font-weight:700; letter-spacing:2px;
    padding:10px 26px; border-radius:8px; border:2px solid rgba(255,255,255,0.85);
    box-shadow:0 8px 24px rgba(220,38,38,0.65); text-transform:uppercase;
  }}
  .stamp-white {{
    background:#F8FAFC; color:#090B10; font-family:'PlexMono',monospace; font-size:23px;
    font-weight:700; padding:10px 20px; border-radius:8px; letter-spacing:1px;
  }}
  .brand-box {{
    display:flex; align-items:center; gap:12px; background:rgba(9,11,16,0.90);
    border:2px solid rgba(255,255,255,0.75); border-radius:999px; padding:8px 24px 8px 12px;
  }}
  .brand-box img {{ width:38px; height:38px; border-radius:50%; }}
  .brand-box span {{ font-size:23px; font-weight:700; letter-spacing:2.5px; color:#FFFFFF; }}

  .center-cta {{
    position:absolute; left:54px; right:54px; bottom:40px; z-index:10;
    display:flex; flex-direction:column; align-items:center; text-align:center; gap:12px;
  }}
  .block-row-1 {{
    display:inline-block; background:#F8FAFC; color:#090B10;
    font-family:'Anton',sans-serif; font-size:{var.get('l1_size', 92)}px; line-height:1.03;
    padding:10px 38px; border-radius:10px; transform:skewX(-6deg);
    box-shadow: 0 14px 34px rgba(0,0,0,0.75); text-transform:uppercase;
  }}
  .block-row-2 {{
    display:inline-block; background: linear-gradient(90deg, #DC2626 0%, #B91C1C 100%); color:#FFFFFF;
    font-family:'Anton',sans-serif; font-size:{var.get('l2_size', 84)}px; line-height:1.05;
    padding:10px 42px; border-radius:10px; border:3px solid #FACC15; transform:skewX(-6deg);
    box-shadow: 0 14px 36px rgba(220,38,38,0.55); text-transform:uppercase;
  }}
  .unskew {{ display:inline-block; transform:skewX(6deg); }}
  .sub-strip {{
    font-family:'Montserrat',sans-serif; font-weight:700; font-size:26px; letter-spacing:1.2px;
    color:#FACC15; background:rgba(9,11,16,0.88); padding:8px 26px; border-radius:8px;
    border:1.5px solid rgba(250,204,21,0.45); text-transform:uppercase;
  }}
</style></head>
<body>
<div class="stage">
  <div class="left-pane"><img src="{_img_url(var['left_img'])}" style="object-position:{var.get('left_pos','center 20%')};"></div>
  <div class="right-pane"><img src="{_img_url(var['right_img'])}" style="object-position:{var.get('right_pos','center 20%')};"></div>
  <div class="shade-top"></div>
  <div class="shade-bot"></div>
  <div class="slash-beam"></div>

  <div class="top-bar">
    <div class="week-stamp">
      <div class="stamp-red">BẢN TIN TUẦN • 16–22/11</div>
      <div class="stamp-white">CẬP NHẬT 23/11</div>
    </div>
    <div class="brand-box"><img src="{LOGO_URL}"><span>ĐIỂM ĐỌC</span></div>
  </div>

  <div class="center-cta">
    <div class="block-row-1"><span class="unskew">{var['line1']}</span></div>
    <div class="block-row-2"><span class="unskew">{var['line2']}</span></div>
    <div class="sub-strip">{var['subtitle']}</div>
  </div>
</div>
</body></html>"""


def _html_set2_9x16() -> str:
    return f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="UTF-8">
<style>
  @font-face {{ font-family:'Anton'; src:url('{ASSETS_URL}/fonts/Anton/Anton-Regular.ttf'); font-weight:400; font-display:block; }}
  @font-face {{ font-family:'Oswald'; src:url('{ASSETS_URL}/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; font-display:block; }}
  @font-face {{ font-family:'Montserrat'; src:url('{ASSETS_URL}/fonts/Montserrat/static/Montserrat-Bold.ttf'); font-weight:700; font-display:block; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1080px; height:1920px; overflow:hidden; background:#090B10; color:#FFF; font-family:'Oswald',sans-serif; }}
  .stage {{ position:relative; width:1080px; height:1920px; overflow:hidden; }}
  .top-img {{ position:absolute; top:0; left:0; width:100%; height:52%; overflow:hidden; }}
  .bot-img {{ position:absolute; bottom:0; left:0; width:100%; height:52%; overflow:hidden; }}
  .top-img img, .bot-img img {{ width:100%; height:100%; object-fit:cover; filter:contrast(1.10) saturate(1.16); }}
  .top-grad {{ position:absolute; top:0; left:0; right:0; height:240px; z-index:4; background:linear-gradient(180deg,rgba(9,11,16,0.92),transparent); }}
  .mid-mask {{ position:absolute; top:38%; left:0; right:0; height:26%; z-index:5; background:linear-gradient(180deg,transparent 0%, rgba(9,11,16,0.94) 30%, rgba(9,11,16,0.94) 70%, transparent 100%); }}
  .hdr {{ position:absolute; top:48px; left:40px; right:40px; z-index:10; display:flex; justify-content:space-between; align-items:center; }}
  .badge {{ background:#DC2626; color:#FFF; font-size:28px; font-weight:700; padding:10px 24px; border-radius:8px; border:2px solid #FFF; letter-spacing:1.5px; }}
  .brand {{ display:flex; align-items:center; gap:10px; background:rgba(9,11,16,0.92); border:2px solid #FFF; border-radius:999px; padding:8px 20px 8px 10px; }}
  .brand img {{ width:38px; height:38px; border-radius:50%; }}
  .brand span {{ font-size:22px; font-weight:700; letter-spacing:2px; }}

  .mid-cta {{
    position:absolute; top:50%; left:32px; right:32px; transform:translateY(-50%); z-index:12;
    display:flex; flex-direction:column; align-items:center; text-align:center; gap:14px;
  }}
  .row1 {{
    background:#F8FAFC; color:#090B10; font-family:'Anton',sans-serif; font-size:84px; line-height:1.05;
    padding:12px 32px; border-radius:10px; transform:skewX(-5deg); box-shadow:0 12px 30px rgba(0,0,0,0.8);
    white-space:nowrap;
  }}
  .row2 {{
    background:#DC2626; color:#FFFFFF; font-family:'Anton',sans-serif; font-size:64px; line-height:1.06;
    padding:12px 28px; border-radius:10px; border:3px solid #FACC15; transform:skewX(-5deg); box-shadow:0 12px 32px rgba(220,38,38,0.65);
    white-space:nowrap;
  }}
  .unskew {{ display:inline-block; transform:skewX(5deg); }}
  .sub {{
    font-family:'Montserrat',sans-serif; font-weight:700; font-size:25px; color:#FACC15;
    background:rgba(9,11,16,0.92); padding:8px 22px; border-radius:8px; border:1.5px solid rgba(250,204,21,0.5);
  }}
</style></head>
<body>
<div class="stage">
  <div class="top-img"><img src="{_img_url('Tin_14_1.jpg')}" style="object-position:32% 18%;"></div>
  <div class="bot-img"><img src="{_img_url('Tin_02_1.jpg')}" style="object-position:62% 20%;"></div>
  <div class="top-grad"></div>
  <div class="mid-mask"></div>
  <div class="hdr">
    <div class="badge">TIN TUẦN • 16–22/11</div>
    <div class="brand"><img src="{LOGO_URL}"><span>ĐIỂM ĐỌC</span></div>
  </div>
  <div class="mid-cta">
    <div class="row1"><span class="unskew">20 SỰ KIỆN ĐỊA CHẤN!</span></div>
    <div class="row2"><span class="unskew">RONALDO 986 BÀN • U17 VN BÙNG NỔ</span></div>
    <div class="sub">MAN UTD THUA 0-4 • ALCARAZ • MÁRQUEZ • 23/11</div>
  </div>
</div>
</body></html>"""


def _render_html(page, html_str: str, out_jpg: Path) -> None:
    tmp_html = paths.work_project_dir("weekly_thumb_sets")
    os.makedirs(tmp_html, exist_ok=True)
    hp = Path(tmp_html) / f"{out_jpg.parent.name}_{out_jpg.stem}.html"
    hp.write_text(html_str, encoding="utf-8")
    page.goto(paths.file_url(str(hp)), wait_until="load", timeout=60000)
    page.evaluate("() => document.fonts.ready")
    page.wait_for_timeout(150)
    out_jpg.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out_jpg), type="jpeg", quality=92)
    ok(f"Đã xuất {paths.rel_to_root(str(out_jpg))} ({out_jpg.stat().st_size / 1024:.1f} KB)")


def _build_descriptions() -> None:
    chap_long = json.loads((OUT_DIR / "_preview_v2" / "chapters_Weekly_23_11.json").read_text(encoding="utf-8")).get("chapters", [])
    chapters_16x9: List[Tuple[str, str]] = []
    for i, ch in enumerate(chap_long):
        lbl = "Nhập cuộc & Toàn cảnh thể thao tuần qua (16–22/11)" if i == 0 else str(ch["label"]).strip()
        chapters_16x9.append((str(ch["time"]).strip(), lbl))

    short_script = json.loads((OUT_DIR / "shorts" / "digest_script_Weekly-23_11.json").read_text(encoding="utf-8"))
    chapters_9x16: List[Tuple[str, str]] = [
        (f"{int(it['start']) // 60:02d}:{int(it['start']) % 60:02d}", str(it["title"]).strip())
        for it in short_script.get("items", [])
    ]

    sources_16x9 = "Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian, ESPN, Formula 1, ATP Tour, FIFA, AFC"
    hashtags_16x9 = [
        "#DiemDoc", "#TongHopTuan", "#TinTheThaoTuan", "#BongDaVietNam",
        "#U17WorldCup", "#DaiHoiTheThaoToanQuoc2026", "#NgoaiHangAnh", "#Alcaraz", "#MarcMarquez",
    ]
    sources_9x16 = "📰 Nguồn tin: Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí, BBC Sport, Sky Sports, The Guardian, ESPN."
    hashtags_9x16 = [
        "#Shorts", "#TongHopTuan", "#DiemDoc", "#DiemDocTheThao",
        "#U17VietNam", "#Liverpool", "#ManUtd", "#DaiHoiTheThaoToanQuoc", "#MarcMarquez",
    ]

    # Bộ 1 SEO: Nhấn mạnh Toàn Cảnh 7 Ngày / Tạp Chí Tuần
    write_mota_16x9(
        out_path=SET1_DIR / "mota_long.txt",
        titles_abc=[
            "Toàn cảnh thể thao tuần 16–22/11: U17 Việt Nam gây sốt, Đại hội 2026 & Man Utd 0-4",
            "Bản tin tuần 16–22/11: Bơi lội mưa kỷ lục, Alcaraz lên đỉnh & Liverpool 4-0 Man Utd",
            "21 sự kiện tuần 16–22/11: Đình Bắc chấn thương, Márquez lần 8 & Barca giữ đỉnh",
        ],
        chapters=chapters_16x9,
        video_type="weekly_digest",
        intro_paragraphs=[
            "Điểm Đọc Tổng Hợp Tuần (16–22/11/2026, cập nhật 23/11/2026): Toàn cảnh 21 sự kiện thể thao Việt Nam và quốc tế nổi bật nhất xuyên suốt tuần qua.",
            "Khác với các bản tin ngày lẻ, số tổng hợp tuần kết nối trọn vẹn diễn biến từ đầu tuần đến kết quả chung cuộc cuối tuần trên tất cả đấu trường.",
        ],
        highlight_bullets=[
            "Đội tuyển Việt Nam & U17 World Cup 2026: Chấn thương của Đình Bắc, hai siêu phẩm lịch sử vào lưới U17 Bỉ và chiến thắng 1-0 của Công an TP.HCM trước Buriram.",
            "Đại hội Thể thao toàn quốc 2026: Khai mạc rực rỡ bên sông Sài Gòn, TP.HCM dẫn đầu bảng vàng, Ánh Viên giành HCB và Watson Nguyễn phá kỷ lục quốc gia.",
            "Sân cỏ châu Âu: Liverpool đè bẹp Man Utd 4-0 trong ngày ra mắt của Pochettino, Chelsea thua Leeds 1-4, Real Madrid và Barcelona rượt đuổi nghẹt thở.",
            "Đỉnh cao thế giới: Carlos Alcaraz vô địch ATP Finals 2026, Max Verstappen thắng F1 Las Vegas và Marc Márquez cân bằng tám chức vô địch MotoGP.",
        ],
        sources_line=sources_16x9,
        hashtags=hashtags_16x9,
        day_str=DAY_STR,
    )
    write_mota_9x16(
        out_path=SET1_DIR / "mota_short.txt",
        seo_title="Toàn cảnh tuần 16–22/11: U17 Việt Nam, Đại hội 2026 & Man Utd 0-4",
        description_paragraphs=[
            "Toàn cảnh 20 sự kiện thể thao nổi bật nhất tuần qua (16–22/11/2026, cập nhật 23/11/2026) gói gọn trong chưa đầy 3 phút.",
        ],
        chapters=chapters_9x16,
        sources_line=sources_9x16,
        hashtags=hashtags_9x16,
        tiktok_caption="Toàn cảnh 20 tin nóng thể thao tuần 16–22/11: U17 Việt Nam ghi 2 siêu phẩm World Cup, Đại hội Toàn quốc mưa kỷ lục, Man Utd thua Liverpool 0-4 và Carlos Alcaraz vô địch ATP Finals!",
        fb_hook="📰 TOÀN CẢNH 20 SỰ KIỆN THỂ THAO TUẦN 16–22/11 TRONG CHƯA ĐẦY 3 PHÚT!",
    )

    # Bộ 2 SEO: Nhấn mạnh Địa Chấn & Đối Lập Căng Thẳng
    write_mota_16x9(
        out_path=SET2_DIR / "mota_long.txt",
        titles_abc=[
            "Địa chấn tuần 16–22/11: Pochettino lập kỷ lục tệ, U17 VN bùng nổ & Kane nghỉ dài",
            "Vui buồn tuần 16–22/11: Đình Bắc nghỉ hết năm, Ánh Viên tái xuất & Alcaraz vô địch",
            "Tổng hợp chấn động tuần 16–22/11: Man Utd rơi áp chót, Ronaldo 986 bàn & F1 hỗn loạn",
        ],
        chapters=chapters_16x9,
        video_type="weekly_digest",
        intro_paragraphs=[
            "Điểm Đọc Tổng Hợp Tuần (16–22/11/2026, cập nhật 23/11/2026): Những cú sốc, kỷ lục và bước ngoặt lớn nhất của thể thao Việt Nam lẫn thế giới suốt tuần qua.",
        ],
        highlight_bullets=[
            "Ngoại hạng Anh dậy sóng: Man Utd thua Liverpool 0-4 rơi xuống thứ 19, Chelsea thảm bại 1-4 trước Leeds, Man City bị từ chối bàn thắng trước Fulham.",
            "Tin vui và nỗi lo bóng đá Việt Nam: U17 Việt Nam ghi hai siêu phẩm trước Bỉ, Công an TP.HCM quật ngã Buriram, nhưng Đình Bắc nghỉ hết năm vì chấn thương gối.",
            "Mưa kỷ lục Đại hội Toàn quốc & thế giới: Ánh Viên đoạt HCB tái xuất, Watson Nguyễn xô đổ kỷ lục quốc gia, Carlos Alcaraz và Marc Márquez cùng đi vào lịch sử.",
        ],
        sources_line=sources_16x9,
        hashtags=hashtags_16x9,
        day_str=DAY_STR,
    )
    write_mota_9x16(
        out_path=SET2_DIR / "mota_short.txt",
        seo_title="Địa chấn tuần 16–22/11: Man Utd rơi áp chót, U17 VN & Bão chấn thương",
        description_paragraphs=[
            "Điểm nhanh 20 cú sốc và kỷ lục thể thao nóng nhất tuần 16–22/11/2026 (cập nhật 23/11/2026) chỉ trong 2 phút 30 giây.",
        ],
        chapters=chapters_9x16,
        sources_line=sources_9x16,
        hashtags=hashtags_9x16,
        tiktok_caption="20 cú sốc thể thao tuần 16–22/11: Man Utd rơi áp chót Ngoại hạng Anh, Đình Bắc & Harry Kane chấn thương nặng, U17 Việt Nam gây sốt World Cup và Marc Márquez 8 lần vô địch MotoGP!",
        fb_hook="⚡ 20 CÚ SỐC & KỶ LỤC THỂ THAO TUẦN 16–22/11 (CẬP NHẬT 23/11)!",
    )


def main() -> None:
    banner("DỰNG 2 BỘ THUMBNAIL & MÔ TẢ ĐỘC LẬP CHO VIDEO TUẦN (Weekly-23.11.2026)", DAY_STR)
    SET1_DIR.mkdir(parents=True, exist_ok=True)
    SET2_DIR.mkdir(parents=True, exist_ok=True)

    set1_variants = [
        {
            "suffix": "A",
            "ribbon": "TỔNG HỢP TUẦN • 16–22/11",
            "pill": "21 SỰ KIỆN • CẬP NHẬT 23/11",
            "line1": "TOÀN CẢNH BÓNG ĐÁ TUẦN QUA",
            "line2": "U17 VN GÂY SỐT • MAN UTD THẢM BẠI 0-4",
            "subtitle": "V-LEAGUE CĂNG THẲNG • CA TP.HCM HẠ BURIRAM • BARCA & REAL RƯỢT ĐUỔI",
            "l1_size": 90,
            "l2_size": 74,
            "cards": [
                {"file": "Tin_02_1.jpg", "tag": "U17 VIỆT NAM 2-3 BỈ", "pos": "center 18%"},
                {"file": "Tin_09_9.jpg", "tag": "POCHETTINO THUA 0-4", "pos": "center 18%"},
                {"file": "Tin_12_2.jpg", "tag": "LA LIGA HỎNG 11M", "pos": "center 16%"},
            ],
        },
        {
            "suffix": "B",
            "ribbon": "TỔNG HỢP TUẦN • 16–22/11",
            "pill": "THỂ THAO VIỆT NAM & ĐẠI HỘI 2026",
            "line1": "TUẦN BÙNG NỔ THỂ THAO VIỆT NAM",
            "line2": "ĐẠI HỘI MƯA KỶ LỤC • ÁNH VIÊN HCB",
            "subtitle": "U17 VIỆT NAM WORLD CUP • ĐÌNH BẮC NGHỈ HẾT NĂM • QUỐC CƯỜNG HẠ BURIRAM",
            "l1_size": 86,
            "l2_size": 74,
            "cards": [
                {"file": "Tin_06_1.jpg", "tag": "ÁNH VIÊN TÁI XUẤT HCB", "pos": "center 25%"},
                {"file": "Tin_04_1.jpg", "tag": "CA TP.HCM 1-0 BURIRAM", "pos": "center 20%"},
                {"file": "Tin_01_2.jpg", "tag": "ĐÌNH BẮC NGHỈ HẾT NĂM", "pos": "center 16%"},
            ],
        },
        {
            "suffix": "C",
            "ribbon": "TỔNG HỢP TUẦN • 16–22/11",
            "pill": "ĐỈNH CAO QUỐC TẾ & KỶ LỤC",
            "line1": "TUẦN LỄ CỦA NHỮNG KỶ LỤC GIA",
            "line2": "ALCARAZ • MÁRQUEZ LẦN 8 • BÃO CHẤN THƯƠNG",
            "subtitle": "VERSTAPPEN THẮNG F1 LAS VEGAS • HARRY KANE NGHỈ DÀI • SKUBAL 450 TRIỆU USD",
            "l1_size": 86,
            "l2_size": 70,
            "cards": [
                {"file": "Tin_17_4.jpg", "tag": "ALCARAZ VÔ ĐỊCH ATP", "pos": "center 18%"},
                {"file": "Tin_18_2.jpg", "tag": "MÁRQUEZ 8 LẦN VÔ ĐỊCH", "pos": "center 18%"},
                {"file": "Tin_13_1.jpg", "tag": "KANE CHẤN THƯƠNG NẶNG", "pos": "center 18%"},
            ],
        },
    ]

    set2_variants = [
        {
            "suffix": "A",
            "left_img": "Tin_09_9.jpg",
            "left_pos": "center 18%",
            "right_img": "Tin_02_1.jpg",
            "right_pos": "center 18%",
            "line1": "TUẦN ĐỊA CHẤN! U17 VN BÙNG NỔ",
            "line2": "MAN UNITED THUA LIVERPOOL 0-4!",
            "subtitle": "POCHETTINO TỆ NHẤT 100 NĂM • ĐẠI HỘI 2026 • ALCARAZ & MÁRQUEZ",
            "l1_size": 84,
            "l2_size": 80,
        },
        {
            "suffix": "B",
            "left_img": "Tin_01_2.jpg",
            "left_pos": "center 18%",
            "right_img": "Tin_17_4.jpg",
            "right_pos": "center 18%",
            "line1": "ĐÌNH BẮC & KANE CÙNG NGHỈ DÀI HẠN!",
            "line2": "ALCARAZ LÊN ĐỈNH • BƠI LỘI KỶ LỤC",
            "subtitle": "TUẦN VUI BUỒN LẪN LỘN • ÁNH VIÊN ĐOẠT HCB • CHELSEA THUA 1-4",
            "l1_size": 80,
            "l2_size": 76,
        },
        {
            "suffix": "C",
            "left_img": "Tin_14_1.jpg",
            "left_pos": "22% 18%",
            "right_img": "Tin_18_1.jpg",
            "right_pos": "center 20%",
            "line1": "RONALDO 986 BÀN • MESSI THUA 0-3",
            "line2": "F1 HỖN LOẠN • QUANG LIÊM TOP 15",
            "subtitle": "21 CHUYÊN ĐỀ ĐẶC SẮC • VERSTAPPEN • SKUBAL 450 TRIỆU USD",
            "l1_size": 82,
            "l2_size": 78,
        },
    ]

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=["--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"])

        # Render 16:9
        step("Đang render Bộ 1 (Weekly Magazine) & Bộ 2 (Diagonal Clash) bản ngang 16:9...")
        page_16 = br.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        for v in set1_variants:
            _render_html(page_16, _html_set1_16x9(v), SET1_DIR / f"thumbnail_{v['suffix']}.jpg")
        for v in set2_variants:
            _render_html(page_16, _html_set2_16x9(v), SET2_DIR / f"thumbnail_{v['suffix']}.jpg")
        page_16.close()

        # Render 9:16
        step("Đang render Short Thumbnail dọc 9:16 cho cả 2 bộ...")
        page_9 = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        _render_html(page_9, _html_set1_9x16(), SET1_DIR / "short_thumbnail.jpg")
        _render_html(page_9, _html_set2_9x16(), SET2_DIR / "short_thumbnail.jpg")
        page_9.close()

        br.close()

    step("Đang xuất mô tả & tiêu đề SEO riêng biệt cho cả 2 bộ...")
    _build_descriptions()
    ok(f"Hoàn tất 2 bộ lựa chọn độc lập tại: {OPT_ROOT}")


if __name__ == "__main__":
    main()
