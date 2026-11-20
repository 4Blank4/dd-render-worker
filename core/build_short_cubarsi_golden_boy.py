#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_short_cubarsi_golden_boy.py — Sản xuất Video Short 9:16:
Pau Cubarsi đoạt giải Cậu bé Vàng 2026 sau chức vô địch World Cup
Nguồn: VnExpress / Tuttosport (10.11.2026)
"""
import sys
sys.dont_write_bytecode = True

import io
import json
import os
import re
import shutil
import time
from typing import List, Dict, Any, Optional, Tuple
import requests
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
from playwright.sync_api import sync_playwright
from ddgs import DDGS

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "vendor"))

engines_html = os.path.join(_ROOT, "engines", "html")
if engines_html not in sys.path:
    sys.path.insert(0, engines_html)

from diemdoc import paths
from diemdoc.log import banner, ok, step, log, warn, die
from diemdoc.tts_text import prepare
from diemdoc.audio import apply_voice_standard, measure_loudness
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from m8_news_bridge import export_bridge_project
from renderer import render_html_engine
from vieneu import Vieneu

DAY_STR = "10.11.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, "Orther", DAY_STR)
WORK_DIR = paths.work_project_dir(os.path.join("Orther", DAY_STR))

IMG_DIR = os.path.join(DAY_DIR, "images")
AUDIO_DIR = os.path.join(DAY_DIR, "audio")
AUDIO_TITLE_DIR = os.path.join(DAY_DIR, "audio-title")
SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
QA_DIR = os.path.join(DAY_DIR, "qa")
SHORTS_WORK = os.path.join(WORK_DIR, "shorts_render")
CACHE_DIR = paths.work_file("vitts_cache")

MIN_RATIO = 1.10
MIN_WIDTH = 600
MIN_HEIGHT = 380

BLOCKED_HOSTS = [
    "alamy", "istockphoto", "shutter", "dreamstime", "123rf",
    "depositphotos", "stock.adobe", "freepik", "pinterest",
    "getty", "gettyimages", "vectorstock", "bigstock", "canstock",
    "pond5", "envato", "dailymail", "thesun", "pxhere", "wallpaper",
    "shopee", "tiki", "lazada", "shopify", "susercontent", "hstatic"
]

ITEM_DATA = {
    "id": 3,
    "art_id": "art_03",
    "slug": "Pau_Cubarsi_Doat_Giai_Cau_Be_Vang",
    "group": "Nhóm: Giải thưởng & Ngôi sao thế giới",
    "title": "Pau Cubarsi đoạt giải Cậu bé Vàng 2026 sau chức vô địch World Cup",
    "summary": "Báo thể thao hàng đầu Italy Tuttosport vừa chính thức công bố chủ nhân giải thưởng Cậu bé Vàng Golden Boy 2026, và vinh dự lớn nhất đã thuộc về trung vệ 19 tuổi Pau Cubarsi của Barcelona! Đây là phần thưởng hoàn toàn xứng đáng sau một năm thi đấu thăng hoa tột bậc, khi ngôi sao sinh năm 2007 cùng Barca vô địch La Liga và đưa đội tuyển Tây Ban Nha đăng quang ngôi vương World Cup 2026. Trong cuộc bầu chọn của 50 nhà báo thể thao châu Âu uy tín, Cubarsi đã vượt qua 24 đối thủ sừng sỏ như Warren Zaire-Emery của PSG hay Ayyoub Bouaddi của Man City để cán đích ở vị trí số một. Thành tích này đưa Cubarsi trở thành hậu vệ thứ hai trong 24 kỳ trao giải đoạt danh hiệu danh giá này sau Matthijs de Ligt năm 2018, đồng thời là cầu thủ Tây Ban Nha thứ sáu được vinh danh sau những đàn anh như Cesc Fabregas, Pedri và Gavi. Ở cấp câu lạc bộ, lò đào tạo La Masia của Barcelona tiếp tục thống trị lịch sử với cầu thủ thứ năm chiến thắng sau Lionel Messi, Pedri, Gavi và Lamine Yamal, sở hữu tới 4 người đoạt giải trong 6 kỳ gần nhất. Từ pha cắt bóng quyết định chặn đứng cơ hội gỡ hòa của Argentina trong trận chung kết World Cup đến danh hiệu cầu thủ trẻ hay nhất giải, Pau Cubarsi đã khẳng định vững chắc vị thế thủ lĩnh tương lai nơi hàng phòng ngự toàn cầu!",
    "digest_line": "Trung vệ 19 tuổi Pau Cubarsi đoạt giải Cậu bé Vàng 2026 của Tuttosport sau cú đúp danh hiệu cùng Barca và Tây Ban Nha.",
    "digest_title": "Pau Cubarsi đoạt giải Cậu bé Vàng 2026 sau chức vô địch World Cup",
    "source": "VnExpress / Tuttosport",
    "news_source": "VnExpress / Tuttosport",
    "file_name": "Short_Pau_Cubarsi_Doat_Giai_Cau_Be_Vang.mp4",
    "thumb_name": "Short_Pau_Cubarsi_Doat_Giai_Cau_Be_Vang_thumbnail.jpg",
    "mota_name": "Short_Pau_Cubarsi_Doat_Giai_Cau_Be_Vang_mota.txt",
    "thumb_hero": "CẬU BÉ VÀNG 2026",
    "thumb_hero_sub": "PAU CUBARSÍ ĐOẠT GIẢI GOLDEN BOY!",
    "thumb_kicker": "LỊCH SỬ GOLDEN BOY 2026",
    "thumb_hero_size": 105,
    "thumb_bg_img": "Tin_03_1.jpg",
    "seo_title": "Pau Cubarsi đoạt giải Cậu bé Vàng 2026 sau chức vô địch World Cup #Shorts",
    "seo_desc": """Trung vệ 19 tuổi Pau Cubarsi của Barcelona chính thức được vinh danh là chủ nhân giải thưởng Cậu bé Vàng (Golden Boy 2026) do tờ báo thể thao Italy Tuttosport tổ chức!

Sau cú đúp vô địch La Liga cùng Barcelona và đăng quang World Cup 2026 cùng đội tuyển Tây Ban Nha, Cubarsi đã vượt qua 24 ứng viên sáng giá hàng đầu châu Âu để về nhất trong cuộc bầu chọn của 50 nhà báo thể thao quốc tế.

Ngôi sao sinh năm 2007 trở thành hậu vệ thứ hai trong lịch sử đoạt giải sau Matthijs de Ligt (2018), đồng thời đưa Barcelona độc chiếm kỷ lục 5 lần có cầu thủ giành Golden Boy (sau Messi, Pedri, Gavi và Lamine Yamal)!""",
    "seo_tags": "#Shorts #DiemDoc #PauCubarsi #Cubarsi #GoldenBoy #GoldenBoy2026 #Barcelona #LaMasia #Tuttosport #TayBanNha #WorldCup2026 #TinBongDa"
}

IMAGE_QUERIES = [
    (
        "Tin_03_1.jpg",
        "https://i1-thethao.vnecdn.net/2026/11/10/barca-jpeg-1794251094-9114-1794251464.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=3H9TmrqY5usI3vGxEMPajw",
        "FC BARCELONA",
        "Barca đăng ảnh thông báo Pau Cubarsi đoạt giải Cậu bé Vàng 2026"
    ),
    (
        "Tin_03_2.jpg",
        "https://barcauniversal.com/wp-content/uploads/2024/03/fc-barcelona-v-ssc-napoli-round-of-16-second-leg-uefa-champions-league-2023-24-13-2048x1366.jpg",
        "BARCA UNIVERSAL / REUTERS",
        "Pau Cubarsi thi đấu chắc chắn nơi hàng thủ Barcelona tại Champions League"
    ),
    (
        "Tin_03_3.jpg",
        "https://i1-thethao.vnecdn.net/2026/11/10/A-nh-ma-n-hi-nh-2026-11-10-lu-2575-6026-1794251464.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=dQqBXOW9wINBSuYJtJAQEA",
        "REUTERS",
        "Pau Cubarsi hôn cúp vàng World Cup 2026 cùng Tây Ban Nha"
    ),
    (
        "Tin_03_4.jpg",
        "https://www.fcbarcelona.com/photo-resources/2024/05/09/fbce29df-4ab4-4239-a8c7-5074cb24134e/_SGB9223.jpg?width=3200&height=2000",
        "FC BARCELONA",
        "Pau Cubarsi ăn mừng danh hiệu vô địch La Liga cùng Barca"
    ),
    (
        "Tin_03_5.jpg",
        "https://i1-thethao.vnecdn.net/2026/11/10/curbasi-1794251458-4188-1794251464.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=Sm0lZ5yiEkHRr1d_6EQeew",
        "VNEXPRESS / TUTTOSPORT",
        "Đồ họa thống kê cuộc bầu chọn Golden Boy của Tuttosport"
    ),
    (
        "Tin_03_6.jpg",
        "https://icdn.psgtalk.com/wp-content/uploads/2023/03/Warren-Zaire-Emery-PSG-vs-Toulouse-Ligue-1-2023.jpg",
        "PSG TALK / ICON SPORT",
        "Warren Zaire-Emery trong màu áo PSG cạnh tranh danh hiệu"
    ),
    (
        "Tin_03_7.jpg",
        "https://assets.goal.com/images/v3/bltddb6436312265c60/5496d2dfa1f96ad85f1f816e6bc542fbaff8b9a1.jpg",
        "GOAL.COM / TUTTOSPORT",
        "Matthijs de Ligt nâng cao danh hiệu Golden Boy năm 2018"
    ),
    (
        "Tin_03_8.jpg",
        "Pedri Gavi Golden Boy Tuttosport",
        "TUTTOSPORT / FC BARCELONA",
        "Pedri và Gavi hai tiền bối Tây Ban Nha từng đoạt Golden Boy"
    ),
    (
        "Tin_03_9.jpg",
        "https://images.t-online.de/2021/07/86320120v3/0x0:1920x1280/fit-in/1920x0/das-hat-lionel-messi-seinem-ewigen-konkurrenten-cristiano-ronaldo-voraus-der-argentinier-wurde-zum-golden-boy-gewaehlt-ronaldo-nie-2005-spielte-messi-wie-schon-fast-immer-und-ueberhaupt-beim-fc-barcelona-blieb-ihm-der-wm-titel-mit-argentinien-bisher-verwehrt-hat-er-sonst-alles-gewonnen-vier-mal-die-champions-league-zehn-mal-die-spanische-meisterschaft-sechs-mal-den-pokal.jpg",
        "FC BARCELONA / TUTTOSPORT",
        "Lionel Messi mở đầu kỷ nguyên Golden Boy cho Barcelona năm 2005"
    ),
    (
        "Tin_03_10.jpg",
        "Pau Cubarsi Lamine Yamal Barcelona football",
        "REUTERS / FC BARCELONA",
        "Pau Cubarsi và Lamine Yamal bộ đôi vàng của lò La Masia"
    ),
    (
        "Tin_03_11.jpg",
        "Pau Cubarsi Spain Euro World Cup match",
        "ACTION IMAGES / REUTERS",
        "Pau Cubarsi xoạc bóng cản phá quyết định chung kết World Cup 2026"
    ),
    (
        "Tin_03_12.jpg",
        "Pau Cubarsi Spain celebration trophy",
        "REUTERS / FIFA",
        "Pau Cubarsi rực sáng đưa Tây Ban Nha lên đỉnh thế giới"
    )
]


def setup_directories():
    for d in [DAY_DIR, IMG_DIR, AUDIO_DIR, AUDIO_TITLE_DIR, SHORTS_OUT, QA_DIR, SHORTS_WORK]:
        os.makedirs(d, exist_ok=True)
    ok(f"Thư mục làm việc: {paths.rel_to_root(DAY_DIR)}")


def download_and_verify_image(url: str, min_w=MIN_WIDTH, min_h=MIN_HEIGHT, min_ratio=MIN_RATIO) -> Optional[Image.Image]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=12)
        if resp.status_code != 200:
            return None
        im = Image.open(io.BytesIO(resp.content))
        im.load()
        if im.mode != "RGB":
            im = im.convert("RGB")
        w, h = im.size
        if w < min_w or h < min_h:
            return None
        # Bỏ qua ảnh vuông hoặc dọc quá mức trừ khi là ảnh trực tiếp
        ratio = w / h
        if ratio < 0.7:  # Quá hẹp
            return None
        return im
    except Exception:
        return None


def fetch_images_tin_3(force: bool = False):
    banner("THU THẬP VÀ KIỂM DUYỆT 12 ẢNH HD CHO TIN 3 (PAU CUBARSÍ)", DAY_STR)
    ddg = DDGS()

    template_path = os.path.expanduser("~/.gemini/antigravity/brain/7e88202f-ec65-4572-a9c3-e602e2904d70/.user_uploaded/media_1794277963250_04e9947d.png")
    getty_word = None
    if os.path.exists(template_path):
        import cv2, numpy as np
        tmpl = cv2.imread(template_path)
        if tmpl is not None:
            gh, gw = tmpl.shape[:2]
            getty_word = tmpl[int(gh*0.3):int(gh*0.65), int(gw*0.15):int(gw*0.9)]

    def has_watermark(im: Image.Image) -> bool:
        if getty_word is None:
            return False
        import cv2, numpy as np
        arr = np.array(im.convert("RGB"))
        h, w = arr.shape[:2]
        for scale in [0.4, 0.5, 0.7]:
            tw = int(getty_word.shape[1] * scale)
            th = int(getty_word.shape[0] * scale)
            if th >= h or tw >= w: continue
            t_scaled = cv2.resize(getty_word, (tw, th))
            roi = arr[h//2:, :]
            res = cv2.matchTemplate(roi, t_scaled, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > 0.60:
                return True
        return False

    for idx, (fname, query_or_url, credit, desc) in enumerate(IMAGE_QUERIES, start=1):
        target_path = os.path.join(IMG_DIR, fname)
        if (not force) and os.path.exists(target_path) and os.path.getsize(target_path) > 30_000:
            ok(f"[{idx}/12] Đã có sẵn: {fname}")
            continue

        step(f"[{idx}/12] Đang tải {fname} ({credit})...")
        found_img = None

        if query_or_url.startswith("http://") or query_or_url.startswith("https://"):
            found_img = download_and_verify_image(query_or_url, min_w=400, min_h=300, min_ratio=0.7)
            if found_img and has_watermark(found_img):
                warn(f"  -> Bị chặn do phát hiện watermark stock trên {query_or_url}")
                found_img = None

        if not found_img:
            # Tìm kiếm qua DDGS
            q = query_or_url
            try:
                results = list(ddg.images(q, max_results=20))
                for r in results:
                    img_url = r.get("image") or ""
                    if any(blocked in img_url.lower() for blocked in BLOCKED_HOSTS):
                        continue
                    im = download_and_verify_image(img_url, min_w=MIN_WIDTH, min_h=MIN_HEIGHT, min_ratio=1.1)
                    if im:
                        if has_watermark(im):
                            warn(f"  -> Bị loại do phát hiện watermark stock: {img_url}")
                            continue
                        found_img = im
                        break
            except Exception as e:
                warn(f"Lỗi tìm kiếm DDGS cho '{q}': {e}")

        if found_img:
            found_img.save(target_path, "JPEG", quality=95, optimize=True)
            ok(f"  -> Lưu thành công {fname} ({found_img.width}x{found_img.height})")
        else:
            warn(f"  -> Không tải được {fname}, sẽ dùng ảnh dự phòng từ Tin_03_1.jpg")
            first_img = os.path.join(IMG_DIR, "Tin_03_1.jpg")
            if os.path.exists(first_img):
                shutil.copy2(first_img, target_path)


def update_metadata_jsons():
    banner("CẬP NHẬT DỮ LIỆU: THETHAO.JSON, IMAGE_CREDITS.JSON, IMAGE_PLAN.JSON", DAY_STR)

    # 1. image_credits.json
    cred_file = os.path.join(DAY_DIR, "image_credits.json")
    credits_map = {}
    if os.path.exists(cred_file):
        with open(cred_file, "r", encoding="utf-8") as f:
            credits_map = json.load(f)

    for fn, _, cr, _ in IMAGE_QUERIES:
        credits_map[fn] = cr

    with open(cred_file, "w", encoding="utf-8") as f:
        json.dump(credits_map, f, ensure_ascii=False, indent=2)
    ok("Đã cập nhật image_credits.json bổ sung Tin 3!")

    # 2. image_plan.json
    plan_file = os.path.join(DAY_DIR, "image_plan.json")
    plan_data = {"metadata": {"day": DAY_STR, "total_scenes": 3}, "records": []}
    if os.path.exists(plan_file):
        with open(plan_file, "r", encoding="utf-8") as f:
            plan_data = json.load(f)

    # Lọc bỏ records scene 3 cũ nếu có
    plan_data["records"] = [r for r in plan_data.get("records", []) if r.get("scene_id") != 3]
    plan_data["metadata"]["total_scenes"] = max(3, plan_data.get("metadata", {}).get("total_scenes", 3))

    # Thêm records cho scene 3 với credit chuẩn sạch 100% không stock watermark
    plan_data["records"].append({"scene_id": 3, "type": "title", "index": 1, "file_name": "Tin_03_1.jpg", "credit": "FC BARCELONA", "description": "Pau Cubarsi đoạt giải Cậu bé Vàng 2026"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 1, "file_name": "Tin_03_1.jpg", "credit": "FC BARCELONA", "description": "Tuttosport công bố Pau Cubarsi đoạt Golden Boy 2026"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 1, "file_name": "Tin_03_2.jpg", "credit": "BARCA UNIVERSAL / REUTERS", "description": "Pau Cubarsi thi đấu chắc chắn nơi hàng thủ Barcelona tại Champions League"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 2, "file_name": "Tin_03_3.jpg", "credit": "REUTERS / FIFA", "description": "Cubarsi hôn cúp vàng World Cup 2026"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 2, "file_name": "Tin_03_4.jpg", "credit": "FC BARCELONA", "description": "Cubarsi ăn mừng chức vô địch La Liga cùng Barca"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 3, "file_name": "Tin_03_5.jpg", "credit": "VNEXPRESS / TUTTOSPORT", "description": "Đồ họa 50 nhà báo thể thao châu Âu bầu chọn"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 3, "file_name": "Tin_03_6.jpg", "credit": "PSG TALK / ICON SPORT", "description": "Warren Zaire-Emery trong màu áo PSG cạnh tranh danh hiệu"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 4, "file_name": "Tin_03_7.jpg", "credit": "GOAL.COM / TUTTOSPORT", "description": "Matthijs de Ligt nâng cúp Golden Boy 2018"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 4, "file_name": "Tin_03_8.jpg", "credit": "TUTTOSPORT / FC BARCELONA", "description": "Pedri và Gavi hai tiền bối Tây Ban Nha từng đoạt giải"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 5, "file_name": "Tin_03_9.jpg", "credit": "FC BARCELONA / TUTTOSPORT", "description": "Lionel Messi mở đầu kỷ nguyên Golden Boy cho Barca"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 5, "file_name": "Tin_03_10.jpg", "credit": "REUTERS / FC BARCELONA", "description": "Cubarsi và Yamal bộ đôi vàng của lò La Masia"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 6, "file_name": "Tin_03_11.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Cubarsi cản phá bóng quyết định chung kết World Cup 2026"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 6, "file_name": "Tin_03_12.jpg", "credit": "REUTERS / FIFA", "description": "Cubarsi khẳng định vững chắc vị thế thủ lĩnh phòng ngự"})

    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump(plan_data, f, ensure_ascii=False, indent=2)
    ok("Đã cập nhật image_plan.json cho Scene 3!")

    # 3. thethao.json
    thethao_file = os.path.join(DAY_DIR, "thethao.json")
    thethao_items = []
    if os.path.exists(thethao_file):
        with open(thethao_file, "r", encoding="utf-8") as f:
            thethao_items = json.load(f)

    # Lọc bỏ item 3 cũ nếu có
    thethao_items = [it for it in thethao_items if str(it.get("id")) != "3"]

    sc_num = "03"
    td = {
        "id": 3,
        "art_id": ITEM_DATA["art_id"],
        "group": ITEM_DATA["group"],
        "title": ITEM_DATA["title"],
        "summary": ITEM_DATA["summary"],
        "digest_line": ITEM_DATA["digest_line"],
        "digest_title": ITEM_DATA["digest_title"],
        "total_images": 12,
        "hide_date_chip": True,
        "source": ITEM_DATA["source"],
        "news_source": ITEM_DATA["news_source"],
        "audio_path": os.path.join(AUDIO_DIR, f"audio_{sc_num}.wav"),
        "audio_title": os.path.join(AUDIO_TITLE_DIR, f"audio_title_{sc_num}.wav"),
    }
    for i in range(1, 13):
        td[f"image_{i}"] = os.path.join(IMG_DIR, f"Tin_{sc_num}_{i}.jpg")

    thethao_items.append(td)
    with open(thethao_file, "w", encoding="utf-8") as f:
        json.dump(thethao_items, f, ensure_ascii=False, indent=2)
    ok("Đã cập nhật thethao.json bổ sung Tin 3 (Pau Cubarsí)!")


def synthesize_audio_for_text(model: Vieneu, text: str, voice: str = "Minh Quân Pro", speed: float = 1.12, pitch: float = 0.93, force: bool = False) -> AudioSegment:
    clean_text, _ = prepare(text)
    chunks = build_chunks_from_text(clean_text, max_words_per_chunk=60, inter_sentence_pause=0.25)
    combined = AudioSegment.empty()
    for c in chunks:
        if c.get("type") == "pause":
            pause_ms = int(c.get("pause_sec", 0.25) * 1000)
            if pause_ms > 0:
                combined += AudioSegment.silent(duration=pause_ms, frame_rate=44100)
            continue
        c_text = c.get("text", "").strip()
        if not c_text:
            continue
        seg, is_hit = render_chunk_vitts(model, c_text, voice, temperature=0.6, speed=speed, pitch=pitch, cache_dir=CACHE_DIR, use_cache=not force, max_chars=768)
        seg = trim_segment_silence(seg)
        combined += seg
    return combined


def synthesize_audio(force: bool = False):
    banner("SINH GIỌNG ĐỌC VITTS V3TURBO MINH QUÂN PRO CHO TIN 3 (CUBARSÍ)", DAY_STR)
    sc_num = "03"
    target_audio = os.path.join(AUDIO_DIR, f"audio_{sc_num}.wav")
    target_title = os.path.join(AUDIO_TITLE_DIR, f"audio_title_{sc_num}.wav")

    if not force and os.path.exists(target_audio) and os.path.exists(target_title) and os.path.getsize(target_audio) > 100_000:
        ok(f"Audio tin {sc_num} đã có sẵn — bỏ qua.")
        return

    model = Vieneu(mode="v3turbo")
    silence_08 = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)

    step(f"Đang đọc Tiêu đề Tin 3: \"{ITEM_DATA['title']}\"...")
    seg_title = synthesize_audio_for_text(model, ITEM_DATA["title"], force=force)
    seg_title = seg_title.set_frame_rate(44100).set_channels(2)
    seg_title.export(target_title, format="wav")
    ok(f"  -> Đã lưu audio tiêu đề: {paths.rel_to_root(target_title)} ({len(seg_title)/1000:.2f}s)")

    step(f"Đang đọc Nội dung chi tiết Tin 3 (~{len(ITEM_DATA['summary'].split())} từ)...")
    seg_summary = synthesize_audio_for_text(model, ITEM_DATA["summary"], force=force)

    combined = seg_title + silence_08 + seg_summary
    combined = apply_voice_standard(combined)
    combined = combined.set_frame_rate(44100).set_channels(2)
    combined.export(target_audio, format="wav")
    ok(f"  -> Đã lưu master audio: {paths.rel_to_root(target_audio)} ({len(combined)/1000:.2f}s)")


def generate_contact_sheet():
    sc_num = "03"
    out_contact = os.path.join(QA_DIR, f"contact_scene_{sc_num}.jpg")
    banner(f"TẠO BẢNG ẢNH ĐỐI CHỨNG QA CHO TIN {sc_num} (CUBARSÍ)", DAY_STR)

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
    topic = "PAU CUBARSÍ ĐOẠT GIẢI CẬU BÉ VÀNG GOLDEN BOY 2026"
    draw.text((pad, 22), f"QA CONTACT SHEET — TIN {sc_num}: {topic}", fill=(0, 229, 255))

    for idx in range(1, 13):
        r = (idx - 1) // cols
        c = (idx - 1) % cols
        x = pad + c * (thumb_w + pad)
        y = header_h + pad + r * (thumb_h + footer_h + pad)

        fn = f"Tin_{sc_num}_{idx}.jpg"
        img_p = os.path.join(IMG_DIR, fn)
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


def render_thumbnail():
    banner("RENDER ẢNH BÌA DỌC 9:16 (THUMBNAIL ANTON CYBER-STADIUM)", DAY_STR)
    sc_num = "03"
    out_thumb = os.path.join(SHORTS_OUT, ITEM_DATA["thumb_name"])

    bg_img_path = os.path.join(IMG_DIR, ITEM_DATA["thumb_bg_img"])
    if not os.path.exists(bg_img_path):
        bg_img_path = os.path.join(IMG_DIR, "Tin_03_1.jpg")

    bg_img_url = paths.file_url(bg_img_path)

    font_anton_url = paths.file_url(os.path.join(paths.FONTS, "Anton", "Anton-Regular.ttf"))
    font_oswald_url = paths.file_url(os.path.join(paths.FONTS, "Oswald", "static", "Oswald-Bold.ttf"))
    font_plex_url = paths.file_url(os.path.join(paths.FONTS, "IBM_Plex_Mono", "IBMPlexMono-Bold.ttf"))

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @font-face {{ font-family: 'Anton'; src: url('{font_anton_url}'); }}
  @font-face {{ font-family: 'Oswald'; src: url('{font_oswald_url}'); font-weight: 700; }}
  @font-face {{ font-family: 'PlexMono'; src: url('{font_plex_url}'); font-weight: 700; }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px;
    height: 1920px;
    background: #060911;
    overflow: hidden;
    font-family: 'Anton', sans-serif;
  }}
  .thumb-root {{
    position: relative;
    width: 1080px;
    height: 1920px;
    background: #060911;
  }}
  .bg-image {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1080px;
    height: 1400px;
    object-fit: cover;
    object-position: center 25%;
    filter: brightness(0.95) contrast(1.08);
  }}
  .gradient-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg,
      rgba(6,9,17,0.3) 0%,
      transparent 25%,
      rgba(6,9,17,0.7) 48%,
      #060911 58%,
      #060911 100%
    );
  }}
  .glow-cyan {{
    position: absolute;
    width: 850px;
    height: 850px;
    background: radial-gradient(circle, rgba(0,229,255,0.22) 0%, transparent 70%);
    top: 55%;
    left: 50%;
    transform: translate(-50%, -30%);
    filter: blur(90px);
    pointer-events: none;
  }}
  .header-badge {{
    position: absolute;
    top: 70px;
    left: 60px;
    right: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }}
  .logo-box {{
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(15, 23, 42, 0.9);
    padding: 14px 28px;
    border-radius: 999px;
    border: 2px solid rgba(0, 229, 255, 0.5);
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.7), 0 0 15px rgba(0, 229, 255, 0.3);
  }}
  .logo-dot {{
    width: 18px;
    height: 18px;
    background: #00E5FF;
    border-radius: 50%;
    box-shadow: 0 0 14px #00E5FF;
  }}
  .logo-text {{
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #fff;
    text-transform: uppercase;
  }}
  .kicker-tag {{
    background: rgba(0, 229, 255, 0.15);
    border: 2px solid #00E5FF;
    padding: 12px 28px;
    border-radius: 999px;
    font-family: 'PlexMono', monospace;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #00E5FF;
    text-transform: uppercase;
  }}
  .stage-bottom {{
    position: absolute;
    bottom: 90px;
    left: 65px;
    right: 65px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    z-index: 10;
  }}
  .hero-title {{
    font-family: 'Anton', sans-serif;
    font-size: {ITEM_DATA['thumb_hero_size']}px;
    font-weight: 400;
    line-height: 0.96;
    text-transform: uppercase;
    color: #FFFFFF;
    text-shadow: 0 0 35px rgba(0, 229, 255, 0.55), 0 4px 15px rgba(0,0,0,0.9);
    letter-spacing: 1px;
  }}
  .sub-title {{
    font-family: 'Oswald', sans-serif;
    font-size: 38px;
    font-weight: 700;
    line-height: 1.25;
    color: #00E5FF;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-left: 6px solid #00E5FF;
    padding-left: 20px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.8);
  }}
  .channel-pill {{
    display: inline-flex;
    align-items: center;
    gap: 12px;
    font-family: 'PlexMono', monospace;
    font-size: 22px;
    color: #94A3B8;
    letter-spacing: 2px;
    text-transform: uppercase;
  }}
</style>
</head>
<body>
<div class="thumb-root">
  <img class="bg-image" src="{bg_img_url}" alt="Hero Image">
  <div class="gradient-overlay"></div>
  <div class="glow-cyan"></div>

  <div class="header-badge">
    <div class="logo-box">
      <div class="logo-dot"></div>
      <div class="logo-text">ĐIỂM ĐỌC THỂ THAO</div>
    </div>
    <div class="kicker-tag">{ITEM_DATA['thumb_kicker']}</div>
  </div>

  <div class="stage-bottom">
    <div class="hero-title">{ITEM_DATA['thumb_hero']}</div>
    <div class="sub-title">{ITEM_DATA['thumb_hero_sub']}</div>
    <div class="channel-pill">KÊNH ĐIỂM ĐỌC // BẢN TIN THỜI SỰ CHÍNH THỨC</div>
  </div>
</div>
</body>
</html>
"""
    tmp_html_file = os.path.join(WORK_DIR, f"thumb_cubarsi_{int(time.time())}.html")
    with open(tmp_html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        page = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(paths.file_url(tmp_html_file), wait_until="networkidle")
        page.wait_for_timeout(350)
        page.screenshot(path=out_thumb, type="jpeg", quality=95)
        br.close()

    ok(f"Đã lưu thumbnail: {paths.rel_to_root(out_thumb)} ({os.path.getsize(out_thumb)/(1024):.1f} KB)")


def write_short_metadata():
    out_mota = os.path.join(SHORTS_OUT, ITEM_DATA["mota_name"])
    banner("XUẤT FILE MÔ TẢ SEO YOUTUBE CHO TIN 3 (1 TIÊU ĐỀ DUY NHẤT)", DAY_STR)

    content = f"""=== TIÊU ĐỀ YOUTUBE ===
{ITEM_DATA['seo_title']}

=== MÔ TẢ VIDEO ===
{ITEM_DATA['seo_desc']}

Đăng ký kênh Điểm Đọc để cập nhật những diễn biến thời sự và câu chuyện thể thao nổi bật mỗi ngày.

{ITEM_DATA['seo_tags']}
"""
    with open(out_mota, "w", encoding="utf-8") as f:
        f.write(content)
    ok(f"Đã lưu mô tả: {paths.rel_to_root(out_mota)}")


def render_short_video(force: bool = False) -> Optional[str]:
    tin_id = 3
    sc_num = "03"
    banner(f"DỰNG VIDEO SHORT 9:16 (TIN #{sc_num}: {ITEM_DATA['slug']})", DAY_STR)

    t0 = time.time()
    out_path = os.path.join(SHORTS_OUT, ITEM_DATA["file_name"])

    if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
        ok(f"Short đã có sẵn: {paths.rel_to_root(out_path)}")
        return out_path

    step(f"Xuất timeline short cho Tin #{sc_num} qua m8_news_bridge...")
    pdir, _, _ = export_bridge_project(
        DAY_DIR,
        item_id=tin_id,
        format_type="short",
        work_proj_dir=os.path.join(SHORTS_WORK, f"short_{sc_num}"),
        global_offset_sec=0.0
    )

    step(f"Render 9:16 trên template short_news_v2.html (30fps)...")
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
        ok(f"🎉 Hoàn thành Short #{sc_num}: {paths.rel_to_root(out_path)} ({os.path.getsize(out_path)/(1024*1024):.1f} MB)")
        banner(f"HOÀN THÀNH VIDEO SHORT #{sc_num} ({time.time() - t0:.1f}s)", DAY_STR)

        # Kiểm toán âm thanh
        res = measure_loudness(out_path)
        ok(f"Kiểm toán âm lượng: I={res.get('input_i')} LUFS, TP={res.get('input_tp')} dBTP, LRA={res.get('input_lra')} LU")
        return out_path
    else:
        die(f"Render Short #{sc_num} thất bại!")
        return None


def main():
    force = "--force" in sys.argv
    setup_directories()
    fetch_images_tin_3()
    update_metadata_jsons()
    synthesize_audio(force=force)
    generate_contact_sheet()
    render_thumbnail()
    write_short_metadata()
    render_short_video(force=force)

    banner("TỔNG KẾT XUẤT BẢN VIDEO SHORT PAU CUBARSÍ HOÀN TẤT", DAY_STR)
    log(f"  📱 Video:     {paths.rel_to_root(os.path.join(SHORTS_OUT, ITEM_DATA['file_name']))}")
    log(f"  🖼️ Thumbnail: {paths.rel_to_root(os.path.join(SHORTS_OUT, ITEM_DATA['thumb_name']))}")
    log(f"  📝 Mô tả:     {paths.rel_to_root(os.path.join(SHORTS_OUT, ITEM_DATA['mota_name']))}")


if __name__ == "__main__":
    main()
