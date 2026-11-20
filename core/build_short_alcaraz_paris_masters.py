#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_short_alcaraz_paris_masters.py — Sản xuất Video Short 9:16:
Carlos Alcaraz lần đầu vô địch Paris Masters: Đòi nợ ngọt ngào Ben Shelton
Nguồn: VnExpress / ATP Tour (09.11.2026)
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

DAY_STR = "09.11.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, "Orther", DAY_STR)
WORK_DIR = paths.work_project_dir(os.path.join("Orther", DAY_STR))

IMG_DIR = os.path.join(DAY_DIR, "images")
AUDIO_DIR = os.path.join(DAY_DIR, "audio")
AUDIO_TITLE_DIR = os.path.join(DAY_DIR, "audio-title")
SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
QA_DIR = os.path.join(DAY_DIR, "qa")
SHORTS_WORK = os.path.join(WORK_DIR, "shorts_render")
CACHE_DIR = paths.work_file("vitts_cache")

MIN_RATIO = 1.18
MIN_WIDTH = 600
MIN_HEIGHT = 380

BLOCKED_HOSTS = [
    "alamy", "istockphoto", "shutter", "dreamstime", "123rf",
    "depositphotos", "stock.adobe", "freepik", "pinterest",
    "vecteezy", "bigstock", "ebay", "etsy", "redbubble", "teepublic",
    "society6", "displate", "ytimg", "pngtree", "cgtrader", "footyheadlines",
    "twimg", "huggingface", "hf.co", "pond5", "mixkit", "motionarray", "pinimg"
]

ITEM_DATA = {
    "id": 3,
    "art_id": "art_03",
    "slug": "Short_Alcaraz_Vo_Dich_Paris_Masters",
    "file_name": "Short_Alcaraz_Vo_Dich_Paris_Masters.mp4",
    "thumb_name": "Short_Alcaraz_Vo_Dich_Paris_Masters_thumbnail.jpg",
    "mota_name": "Short_Alcaraz_Vo_Dich_Paris_Masters_mota.txt",
    "group": "Nhóm: Quần vợt đỉnh cao",
    "title": "Carlos Alcaraz lần đầu vô địch Paris Masters: Đòi nợ ngọt ngào Ben Shelton",
    "summary": (
        "Đêm chung kết Paris Masters rạng sáng nay đã chứng kiến khoảnh khắc lịch sử khi Carlos Alcaraz xuất sắc đánh bại Ben Shelton "
        "sau hai set kịch tính để lần đầu tiên bước lên đỉnh vinh quang tại giải đấu! "
        "Trận đấu tại Nanterre diễn ra vô cùng nghẹt thở ngay từ set đầu, nơi Alcaraz thể hiện bản lĩnh thép khi cứu liên tiếp bốn break-point "
        "ở game thứ ba trước khi thắng 7-5 trong loạt tie-break căng thẳng. "
        "Sang set hai, dù bị Shelton bẻ giao bóng dẫn trước, ngôi sao 23 tuổi người Tây Ban Nha đã xuất sắc đòi lại break ở game 8 "
        "rồi tung cú trái tay winner quyết định ở match-point thứ hai để ấn định thắng lợi 7-5. "
        "Chiến thắng này giúp Alcaraz thanh toán sòng phẳng món nợ trước Shelton tại Mỹ Mở rộng, "
        "đồng thời nối dài chuỗi phong độ hủy diệt với 19 chiến thắng sau 21 trận kể từ khi trở lại sau chấn thương cổ tay. "
        "Đây là danh hiệu Masters 1000 thứ 9 trong sự nghiệp của Alcaraz, giúp anh sánh ngang Novak Djokovic và Rafael Nadal "
        "khi trở thành tay vợt thứ ba trong lịch sử vô địch Masters ít nhất một lần suốt năm mùa liên tiếp. "
        "Chức vô địch thứ năm trong năm 2026 không chỉ đưa Alcaraz trở thành tay vợt Tây Ban Nha thứ hai đăng quang Paris Masters sau 40 năm, "
        "mà còn là bước chạy đà hoàn hảo cho anh trước thềm ATP Finals tại Turin!"
    ),
    "digest_line": "Carlos Alcaraz đánh bại Ben Shelton 7-6, 7-5 để lần đầu tiên đăng quang chức vô địch Paris Masters.",
    "digest_title": "Carlos Alcaraz lần đầu vô địch Paris Masters: Đòi nợ ngọt ngào Ben Shelton",
    "source": "VnExpress / ATP Tour",
    "news_source": "VnExpress / ATP Tour",
    "thumb_kicker": "PARIS MASTERS 2026 · CHUNG KẾT",
    "thumb_hero": "ALCARAZ LÊN ĐỈNH!",
    "thumb_hero_size": "110",
    "thumb_sub": "HẠ SHELTON ĐOẠT DANH HIỆU MASTERS 1000 THỨ 9 TRONG SỰ NGHIỆP",
    "thumb_tag_a": "ĐÒI NỢ SHELTON",
    "thumb_tag_b": "9 MASTERS 1000",
    "seo_title": "Carlos Alcaraz lần đầu vô địch Paris Masters: Đòi nợ ngọt ngào Ben Shelton #Shorts",
    "seo_desc": (
        "Chiến thắng nghẹt thở 7-6(5), 7-5 trước Ben Shelton ở trận chung kết ngày 8/11/2026 đã đưa Carlos Alcaraz "
        "lần đầu tiên đăng quang tại Paris Masters!\n\n"
        "Cứu ngoạn mục 4 break-point ở set một rồi lội ngược dòng đòi lại break ở set hai, ngôi sao 23 tuổi người Tây Ban Nha "
        "đã đòi lại món nợ trước đối thủ Mỹ sau thất bại tại US Open. "
        "Đây là danh hiệu Masters 1000 thứ 9 trong sự nghiệp của Alcaraz, giúp anh gia nhập hàng ngũ huyền thoại cùng Novak Djokovic "
        "và Rafael Nadal khi vô địch ít nhất một giải Masters trong 5 mùa giải liên tiếp!\n\n"
        "Chức vô địch thứ năm trong năm 2026 cũng là bước đệm hoàn hảo để Alcaraz hướng tới vinh quang tại ATP Finals diễn ra ở Turin!"
    ),
    "seo_tags": "#Shorts #DiemDoc #CarlosAlcaraz #BenShelton #ParisMasters #Tennis #ATPFinals #Masters1000 #TinTheThao"
}

IMAGE_QUERIES = [
    ("Tin_03_1.jpg", "Carlos Alcaraz trophy Paris Masters 2026 celebration", "AP PHOTO"),
    ("Tin_03_2.jpg", "Carlos Alcaraz vs Ben Shelton Paris Masters 2026 match action", "REUTERS"),
    ("Tin_03_3.jpg", "Carlos Alcaraz forehand winner Paris Masters 2026 Nanterre", "GETTY IMAGES / ATP TOUR"),
    ("Tin_03_4.jpg", "Ben Shelton serve action Paris Masters 2026", "ACTION IMAGES / REUTERS"),
    ("Tin_03_5.jpg", "Carlos Alcaraz break point save celebration fist pump 2026", "AP PHOTO"),
    ("Tin_03_6.jpg", "Ben Shelton disappointed reaction Paris Masters 2026", "AFP / GETTY IMAGES"),
    ("Tin_03_7.jpg", "Carlos Alcaraz Ben Shelton net handshake Paris Masters 2026", "REUTERS"),
    ("Tin_03_8.jpg", "Carlos Alcaraz backhand winner indoor hard court 2026", "AP PHOTO"),
    ("Tin_03_9.jpg", "Carlos Alcaraz lifting trophy Paris Masters 2026 ceremony", "GETTY IMAGES / ATP TOUR"),
    ("Tin_03_10.jpg", "Carlos Alcaraz Rafael Nadal Novak Djokovic Masters 1000 record", "VNEXPRESS / ATP TOUR"),
    ("Tin_03_11.jpg", "Carlos Alcaraz kissing Paris Masters trophy 2026", "AP PHOTO"),
    ("Tin_03_12.jpg", "Carlos Alcaraz celebrating victory with crowd Paris 2026", "ATP TOUR"),
]


def download_image(url: str, min_w=MIN_WIDTH, min_h=MIN_HEIGHT, min_ratio=MIN_RATIO) -> Optional[Image.Image]:
    low = url.lower()
    if any(b in low for b in BLOCKED_HOSTS) or "watermark" in low:
        return None
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code != 200 or len(r.content) < 20_000:
            return None
        im = Image.open(io.BytesIO(r.content))
        im.load()
        w, h = im.size
        if w < min_w or h < min_h or (w / h) < min_ratio:
            return None
        if im.mode != "RGB":
            im = im.convert("RGB")
        return im
    except Exception:
        return None


def fetch_images():
    banner("THU THẬP VÀ CHUẨN HÓA 12 ẢNH CHO TIN 3 (ALCARAZ VÔ ĐỊCH PARIS MASTERS)", DAY_STR)
    os.makedirs(IMG_DIR, exist_ok=True)

    # 1. Tải ảnh gốc từ bài báo VnExpress cho Tin_03_1.jpg nếu chưa có
    target_1 = os.path.join(IMG_DIR, "Tin_03_1.jpg")
    vne_img_url = "https://i1-thethao.vnecdn.net/2026/11/09/ap26312562810624-1794157406-7515-1794157424.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=U3K3SEYjHq6OZLUOmtmvSA"
    if not os.path.exists(target_1) or os.path.getsize(target_1) < 20_000:
        im1 = download_image(vne_img_url)
        if im1:
            im1.save(target_1, "JPEG", quality=95, optimize=True)
            ok(f"  [VNEXPRESS AP] Tin_03_1.jpg: {im1.width}x{im1.height}")

    with DDGS() as ddgs:
        for fname, query, _ in IMAGE_QUERIES:
            target_path = os.path.join(IMG_DIR, fname)
            if os.path.exists(target_path) and os.path.getsize(target_path) > 30_000:
                ok(f"  [ĐÃ CÓ] {fname}")
                continue

            step(f"Tìm kiếm ảnh cho {fname}: \"{query}\"...")
            found_img = None
            try:
                res = list(ddgs.images(query, region="wt-wt", safesearch="off", size="Large", layout="Wide", max_results=20))
            except Exception as e:
                warn(f"Lỗi DDGS: {e}, thử lại...")
                time.sleep(2)
                try:
                    res = list(ddgs.images(query, region="wt-wt", safesearch="off", max_results=15))
                except Exception:
                    res = []

            for item in res:
                img_url = item.get("image")
                if not img_url:
                    continue
                im = download_image(img_url)
                if im:
                    found_img = im
                    break

            if not found_img:
                fallback_q = "Carlos Alcaraz Paris Masters 2026 tennis"
                step(f"  -> Thử fallback query: {fallback_q}")
                try:
                    res_fb = list(ddgs.images(fallback_q, region="wt-wt", safesearch="off", layout="Wide", max_results=15))
                    for item in res_fb:
                        im = download_image(item.get("image"))
                        if im:
                            found_img = im
                            break
                except Exception:
                    pass

            if found_img:
                found_img.save(target_path, "JPEG", quality=92, optimize=True)
                ok(f"  -> Lưu thành công {fname} ({found_img.width}x{found_img.height})")
            else:
                warn(f"  -> Không tải được {fname}, sẽ dùng ảnh dự phòng.")
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

    for fn, _, cr in IMAGE_QUERIES:
        credits_map[fn] = cr

    with open(cred_file, "w", encoding="utf-8") as f:
        json.dump(credits_map, f, ensure_ascii=False, indent=2)
    ok("Đã cập nhật image_credits.json với 12 ảnh mới!")

    # 2. image_plan.json
    plan_file = os.path.join(DAY_DIR, "image_plan.json")
    plan_data = {"metadata": {"day": DAY_STR, "total_scenes": 3}, "records": []}
    if os.path.exists(plan_file):
        with open(plan_file, "r", encoding="utf-8") as f:
            plan_data = json.load(f)

    # Lọc bỏ records scene 3 cũ nếu có
    plan_data["records"] = [r for r in plan_data.get("records", []) if r.get("scene_id") != 3]
    plan_data["metadata"]["total_scenes"] = 3

    # Thêm records cho scene 3
    plan_data["records"].append({"scene_id": 3, "type": "title", "index": 1, "file_name": "Tin_03_1.jpg", "credit": "AP PHOTO", "description": "Carlos Alcaraz lần đầu vô địch Paris Masters"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 1, "file_name": "Tin_03_1.jpg", "credit": "AP PHOTO", "description": "Alcaraz đánh bại Shelton sau 2 set kịch tính"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 1, "file_name": "Tin_03_2.jpg", "credit": "REUTERS", "description": "Khoảnh khắc đăng quang Paris Masters 2026"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 2, "file_name": "Tin_03_3.jpg", "credit": "GETTY IMAGES / ATP TOUR", "description": "Alcaraz cứu liên tiếp 4 break-point ở game thứ 3"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 2, "file_name": "Tin_03_4.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Ben Shelton giao bóng uy lực tại chảo lửa Nanterre"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 3, "file_name": "Tin_03_5.jpg", "credit": "AP PHOTO", "description": "Alcaraz đòi lại break ở game 8 cân bằng 4-4"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 3, "file_name": "Tin_03_6.jpg", "credit": "AFP / GETTY IMAGES", "description": "Cú trái tay winner quyết định ở match-point thứ hai"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 4, "file_name": "Tin_03_7.jpg", "credit": "REUTERS", "description": "Màn bắt tay đầy tôn trọng giữa Alcaraz và Shelton"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 4, "file_name": "Tin_03_8.jpg", "credit": "AP PHOTO", "description": "Chuỗi 19 chiến thắng sau 21 trận trở lại sau chấn thương"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 5, "file_name": "Tin_03_9.jpg", "credit": "GETTY IMAGES / ATP TOUR", "description": "Danh hiệu Masters 1000 thứ 9 trong sự nghiệp Alcaraz"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 5, "file_name": "Tin_03_10.jpg", "credit": "VNEXPRESS / ATP TOUR", "description": "Sánh ngang Novak Djokovic và Rafael Nadal với kỷ lục 5 năm liên tiếp"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 6, "file_name": "Tin_03_11.jpg", "credit": "AP PHOTO", "description": "Danh hiệu thứ 5 mùa giải 2026 và tay vợt TBN thứ 2 sau Ferrer"})
    plan_data["records"].append({"scene_id": 3, "type": "sentence", "index": 6, "file_name": "Tin_03_12.jpg", "credit": "ATP TOUR", "description": "Bước chạy đà hoàn hảo cho Alcaraz trước thềm ATP Finals Turin"})

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
    ok("Đã cập nhật thethao.json bổ sung Tin 3 (Carlos Alcaraz)!")


def synthesize_audio_for_text(model: Vieneu, text: str, voice: str = "Minh Quân Pro", speed: float = 1.12, pitch: float = 0.93) -> AudioSegment:
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
        seg, _ = render_chunk_vitts(model, c_text, voice, temperature=0.6, speed=speed, pitch=pitch, cache_dir=CACHE_DIR, use_cache=True, max_chars=768)
        seg = trim_segment_silence(seg)
        combined += seg
    return combined


def synthesize_audio(force: bool = False):
    banner("SINH GIỌNG ĐỌC VITTS V3TURBO MINH QUÂN PRO CHO TIN 3 (ALCARAZ)", DAY_STR)
    sc_num = "03"
    target_audio = os.path.join(AUDIO_DIR, f"audio_{sc_num}.wav")
    target_title = os.path.join(AUDIO_TITLE_DIR, f"audio_title_{sc_num}.wav")

    if not force and os.path.exists(target_audio) and os.path.exists(target_title) and os.path.getsize(target_audio) > 100_000:
        ok(f"Audio tin {sc_num} đã có sẵn — bỏ qua.")
        return

    model = Vieneu(mode="v3turbo")
    silence_08 = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)

    step(f"Đang đọc Tiêu đề Tin 3: \"{ITEM_DATA['title']}\"...")
    seg_title = synthesize_audio_for_text(model, ITEM_DATA["title"])
    seg_title = seg_title.set_frame_rate(44100).set_channels(2)
    seg_title.export(target_title, format="wav")
    ok(f"  -> Đã lưu audio tiêu đề: {paths.rel_to_root(target_title)} ({len(seg_title)/1000:.2f}s)")

    step(f"Đang đọc Nội dung chi tiết Tin 3 (~{len(ITEM_DATA['summary'].split())} từ)...")
    seg_summary = synthesize_audio_for_text(model, ITEM_DATA["summary"])

    combined = seg_title + silence_08 + seg_summary
    combined = apply_voice_standard(combined)
    combined = combined.set_frame_rate(44100).set_channels(2)
    combined.export(target_audio, format="wav")
    ok(f"  -> Đã lưu master audio: {paths.rel_to_root(target_audio)} ({len(combined)/1000:.2f}s)")


def generate_contact_sheet():
    sc_num = "03"
    out_contact = os.path.join(QA_DIR, f"contact_scene_{sc_num}.jpg")
    banner(f"TẠO BẢNG ẢNH ĐỐI CHỨNG QA CHO TIN {sc_num} (ALCARAZ)", DAY_STR)

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
    topic = "CARLOS ALCARAZ LẦN ĐẦU VÔ ĐỊCH PARIS MASTERS 2026"
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
    banner("TẠO ẢNH THUMBNAIL DỌC 9:16 CHO SHORT ALCARAZ", DAY_STR)
    tpl_html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  @font-face { font-family:'Anton'; src:url('__ASSETS__/fonts/Anton/Anton-Regular.ttf'); font-weight:400; }
  @font-face { font-family:'Oswald'; src:url('__ASSETS__/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; }
  @font-face { font-family:'PlexMono'; src:url('__ASSETS__/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'); font-weight:700; }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    width: 1080px;
    height: 1920px;
    overflow: hidden;
    background: #060911;
    font-family: 'Oswald', sans-serif;
    color: #fff;
    position: relative;
  }
  .bg-img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 58%;
    background-image: url('__THUMB_IMAGE__');
    background-size: cover;
    background-position: center top;
    filter: brightness(0.9) contrast(1.18);
  }
  .bg-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg,
      rgba(6,9,17,0.4) 0%,
      transparent 25%,
      rgba(6,9,17,0.7) 48%,
      #060911 58%,
      #060911 100%
    );
  }
  .glow-cyan {
    position: absolute;
    width: 850px;
    height: 850px;
    background: radial-gradient(circle, rgba(0,229,255,0.22) 0%, transparent 70%);
    top: 55%;
    left: 50%;
    transform: translate(-50%, -30%);
    filter: blur(90px);
    pointer-events: none;
  }
  .header-badge {
    position: absolute;
    top: 70px;
    left: 60px;
    right: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }
  .logo-box {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(15, 23, 42, 0.9);
    padding: 14px 28px;
    border-radius: 999px;
    border: 2px solid rgba(0, 229, 255, 0.5);
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.7), 0 0 15px rgba(0, 229, 255, 0.3);
  }
  .logo-dot {
    width: 18px;
    height: 18px;
    background: #00E5FF;
    border-radius: 50%;
    box-shadow: 0 0 14px #00E5FF;
  }
  .logo-text {
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #fff;
    text-transform: uppercase;
  }
  .kicker-tag {
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
  }
  .stage-bottom {
    position: absolute;
    bottom: 90px;
    left: 65px;
    right: 65px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    z-index: 10;
  }
  .hero-title {
    font-family: 'Anton', sans-serif;
    font-size: __THUMB_HERO_SIZE__px;
    font-weight: 400;
    line-height: 0.96;
    text-transform: uppercase;
    color: #FFFFFF;
    text-shadow: 0 0 35px rgba(0, 229, 255, 0.55), 0 4px 15px rgba(0,0,0,0.9);
    letter-spacing: 1px;
  }
  .sub-title {
    font-family: 'Oswald', sans-serif;
    font-size: 38px;
    font-weight: 700;
    line-height: 1.25;
    color: #E2E8F0;
    background: rgba(15, 23, 42, 0.92);
    padding: 20px 28px;
    border-radius: 18px;
    border-left: 8px solid #00E5FF;
    backdrop-filter: blur(10px);
    letter-spacing: 0.5px;
  }
  .rule-bar {
    height: 6px;
    width: 220px;
    background: linear-gradient(90deg, #00E5FF 0%, #38BDF8 100%);
    border-radius: 3px;
    box-shadow: 0 0 12px rgba(0, 229, 255, 0.6);
  }
  .tag-row {
    display: flex;
    gap: 18px;
  }
  .stat-pill {
    background: rgba(30, 41, 59, 0.95);
    border: 1px solid rgba(0, 229, 255, 0.35);
    padding: 14px 28px;
    border-radius: 14px;
    font-family: 'PlexMono', monospace;
    font-size: 24px;
    font-weight: 700;
    color: #38BDF8;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
</style>
</head>
<body>
  <div class="bg-img"></div>
  <div class="bg-overlay"></div>
  <div class="glow-cyan"></div>

  <div class="header-badge">
    <div class="logo-box">
      <div class="logo-dot"></div>
      <div class="logo-text">ĐIỂM ĐỌC THỂ THAO</div>
    </div>
    <div class="kicker-tag">__THUMB_KICKER__</div>
  </div>

  <div class="stage-bottom">
    <div class="hero-title">__THUMB_HERO__</div>
    <div class="rule-bar"></div>
    <div class="sub-title">__THUMB_SUBTITLE__</div>
    <div class="tag-row">
      <div class="stat-pill">__THUMB_TAG_A__</div>
      <div class="stat-pill">__THUMB_TAG_B__</div>
    </div>
  </div>
</body>
</html>
"""
    thumb_img_p = os.path.join(IMG_DIR, "Tin_03_1.jpg")
    out_thumb = os.path.join(SHORTS_OUT, ITEM_DATA["thumb_name"])

    h_content = tpl_html
    h_content = h_content.replace("__ASSETS__", paths.file_url(paths.ASSETS))
    h_content = h_content.replace("__THUMB_IMAGE__", paths.file_url(thumb_img_p))
    h_content = h_content.replace("__THUMB_KICKER__", ITEM_DATA["thumb_kicker"])
    h_content = h_content.replace("__THUMB_HERO__", ITEM_DATA["thumb_hero"])
    h_content = h_content.replace("__THUMB_HERO_SIZE__", ITEM_DATA.get("thumb_hero_size", "110"))
    h_content = h_content.replace("__THUMB_SUBTITLE__", ITEM_DATA["thumb_sub"])
    h_content = h_content.replace("__THUMB_TAG_A__", ITEM_DATA["thumb_tag_a"])
    h_content = h_content.replace("__THUMB_TAG_B__", ITEM_DATA["thumb_tag_b"])

    tmp_html_file = os.path.join(WORK_DIR, "thumb_tin_03.html")
    with open(tmp_html_file, "w", encoding="utf-8") as f:
        f.write(h_content)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=[
            "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"
        ])
        page = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(paths.file_url(tmp_html_file), wait_until="networkidle")
        page.wait_for_timeout(350)
        page.screenshot(path=out_thumb, type="jpeg", quality=95)
        br.close()

    ok(f"Đã lưu thumbnail #03: {paths.rel_to_root(out_thumb)} ({os.path.getsize(out_thumb)/(1024):.1f} KB)")


def write_short_metadata():
    out_mota = os.path.join(SHORTS_OUT, ITEM_DATA["mota_name"])
    banner("XUẤT FILE MÔ TẢ SEO YOUTUBE CHO SHORT #03 (1 TIÊU ĐỀ DUY NHẤT)", DAY_STR)

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
    banner(f"DỰNG VIDEO SHORT 9:16 (TIN #03: {ITEM_DATA['slug']})", DAY_STR)

    t0 = time.time()
    out_path = os.path.join(SHORTS_OUT, ITEM_DATA["file_name"])

    if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
        ok(f"Short đã có sẵn: {paths.rel_to_root(out_path)}")
        return out_path

    step("Xuất timeline short cho Tin #03 qua m8_news_bridge...")
    pdir, _, _ = export_bridge_project(
        DAY_DIR,
        item_id=3,
        format_type="short",
        work_proj_dir=os.path.join(SHORTS_WORK, "short_03"),
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
        ok(f"🎉 Hoàn thành Short #03: {paths.rel_to_root(out_path)} ({os.path.getsize(out_path)/(1024*1024):.1f} MB)")
        banner(f"HOÀN THÀNH VIDEO SHORT #03 ({time.time() - t0:.1f}s)", DAY_STR)
        return out_path
    else:
        die("Render Short #03 thất bại!")
        return None


def main():
    force = "--force" in sys.argv
    fetch_images()
    update_metadata_jsons()
    synthesize_audio(force=force)
    generate_contact_sheet()
    render_thumbnail()
    write_short_metadata()
    render_short_video(force=force)

    banner("TỔNG KẾT XUẤT BẢN SHORT CARLOS ALCARAZ HOÀN TẤT", DAY_STR)
    log(f"  📱 Video:     {paths.rel_to_root(os.path.join(SHORTS_OUT, ITEM_DATA['file_name']))}")
    log(f"  🖼️ Thumbnail: {paths.rel_to_root(os.path.join(SHORTS_OUT, ITEM_DATA['thumb_name']))}")
    log(f"  📝 Mô tả:     {paths.rel_to_root(os.path.join(SHORTS_OUT, ITEM_DATA['mota_name']))}")


if __name__ == "__main__":
    main()
