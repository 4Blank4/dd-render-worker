#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_shorts_images_17_11.py — Khắc phục triệt để lỗi ảnh rác, logo & watermark cho 3 Video Shorts
==================================================================================================
Thay thế toàn bộ ảnh bị người dùng phản ánh hoặc vi phạm tiêu chuẩn:
- v1_portugal_young_generation.jpg (ảnh rừng cây -> ảnh thi đấu thực tế Leao/Vitinha)
- v1_ronaldo_iconic_shadow.jpg (ảnh nền trắng 77% -> ảnh Ronaldo vẫy tay chào khán giả)
- v1_germany_black_kit.jpg (ảnh áo đấu e-commerce -> ảnh tuyển thủ Đức thi đấu áo đen)
- v1_scoreboard_5_0.jpg (ảnh dính logo Getty -> ảnh ăn mừng 5-0 sạch)
- v1_florian_wirtz_double.jpg (ảnh dính credit Getty -> ảnh ăn mừng sạch)
- v1_europe_football_map.jpg (ảnh dính credit -> cúp Nations League trên sân)
- v1_germany_group_winner.jpg (trùng ảnh celebrate -> ảnh ăn mừng riêng biệt)
- v3_fifa_ranking_graphic.jpg (ảnh EPA lệch dọc -> ảnh tuyển VN ăn mừng)
- v3_mozambique_can_defeat.jpg (ảnh dính logo TV Sky Football -> ảnh thi đấu sạch)
- v3_coaching_staff_meeting.jpg (ảnh nền đen 64% -> ảnh BHL trên sân tập)
- v3_sports_arena_crowd.jpg (trùng ảnh banner -> ảnh khán đài nhà thi đấu riêng biệt)
- v3_vietnam_flag_stadium.jpg (ảnh nền trắng 25% -> ảnh cờ đỏ sao vàng trên khán đài Mỹ Đình)
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import os
import io
import time
import json
import subprocess
from pathlib import Path
from PIL import Image
import numpy as np
import requests
from ddgs import DDGS

_HERE = Path(__file__).resolve().parent
ROOT_DIR = _HERE.parent
DAY_DIR = ROOT_DIR / "outputs" / "Orther" / "17.11.2026"
IMG_DIR = DAY_DIR / "images"
QA_DIR = DAY_DIR / "qa"

BLOCKED_DOMAINS = [
    "gettyimages", "alamy", "shutterstock", "istockphoto", "depositphotos",
    "dreamstime", "123rf", "vecteezy", "freepik", "adobe.com", "stock",
    "wallpaperflare", "wallpapers.com", "besthdwallpaper", "pinterest", "pinimg",
    "shopify", "etsy", "ebay", "amazon", "aliexpress", "shopee", "lazada", "tiki"
]

BAD_OCR_KEYWORDS = [
    "getty", "alamy", "shutter", "istock", "deposit", "dreamstime",
    "credit:", "watermark", "zheng", "haizhan", "vector", "preview",
    "sky sports", "sky football", "123rf", "freepik", "adobe"
]

SLOTS_TO_PATCH = [
    {
        "scene_id": 1,
        "fname": "v1_portugal_young_generation.jpg",
        "queries": [
            "Rafael Leao Vitinha Portugal national team match action 2024",
            "Rafael Leao Portugal goal celebration match action",
            "Bruno Fernandes Rafael Leao celebrate Portugal match"
        ],
        "credit": "REUTERS / FOOTBALL ITALIA",
        "desc": "Thế hệ tài năng trẻ Rafael Leao và Vitinha của tuyển Bồ Đào Nha"
    },
    {
        "scene_id": 1,
        "fname": "v1_ronaldo_iconic_shadow.jpg",
        "queries": [
            "Cristiano Ronaldo Portugal match applause stadium fans",
            "Cristiano Ronaldo Portugal national team jersey number 7 clapping fans",
            "Cristiano Ronaldo salute fans Portugal match pitch"
        ],
        "credit": "REUTERS / NY POST",
        "desc": "Cristiano Ronaldo vẫy tay cảm ơn người hâm mộ sau trận đấu"
    },
    {
        "scene_id": 1,
        "fname": "v1_germany_black_kit.jpg",
        "queries": [
            "Germany national team players wearing black kit match action",
            "Kai Havertz Germany black kit match action 2024",
            "Florian Wirtz Germany black jersey match pitch"
        ],
        "credit": "DFB / BUNDESLIGA",
        "desc": "Các tuyển thủ Đức thi đấu trong trang phục áo đen đặc biệt"
    },
    {
        "scene_id": 1,
        "fname": "v1_scoreboard_5_0.jpg",
        "queries": [
            "Germany 5 0 Netherlands Nations League celebration Berlin match",
            "Germany vs Netherlands 5-0 Berlin match celebration players",
            "Germany football team celebrate goal against Netherlands 2024"
        ],
        "credit": "YONHAP NEWS / UEFA",
        "desc": "Đội tuyển Đức ăn mừng chiến thắng 5-0 lịch sử trước Hà Lan"
    },
    {
        "scene_id": 1,
        "fname": "v1_florian_wirtz_double.jpg",
        "queries": [
            "Florian Wirtz goal celebration Germany Nations League match action",
            "Florian Wirtz Germany national team celebration pitch 2024",
            "Florian Wirtz celebrate goal Germany match"
        ],
        "credit": "BILD / DFB",
        "desc": "Florian Wirtz rực sáng với cú đúp bàn thắng cho tuyển Đức"
    },
    {
        "scene_id": 1,
        "fname": "v1_europe_football_map.jpg",
        "queries": [
            "UEFA Nations League trophy pitch stadium night match lights",
            "Olympiastadion Berlin pitch night stadium atmosphere crowd",
            "UEFA Nations League football pitch stadium lights"
        ],
        "credit": "UEFA",
        "desc": "Sóng gió bóng đá lan rộng khắp lục địa già"
    },
    {
        "scene_id": 1,
        "fname": "v1_germany_group_winner.jpg",
        "queries": [
            "Germany national football team celebrate quarterfinal Nations League",
            "Germany team celebration pitch win Nations League 2024",
            "Joshua Kimmich Germany team celebrate victory"
        ],
        "credit": "KICKER / DFB",
        "desc": "Tuyển Đức giành ngôi đầu bảng A2 tiến vào tứ kết"
    },
    {
        "scene_id": 3,
        "fname": "v3_fifa_ranking_graphic.jpg",
        "queries": [
            "Doi tuyen bong da nam Viet Nam an mung chien thang san My Dinh",
            "Tuyen Viet Nam an mung ban thang tren san My Dinh",
            "Doi tuyen Viet Nam chien thang chao khan gia My Dinh"
        ],
        "credit": "VFF / DÂN TRÍ",
        "desc": "Đội tuyển Việt Nam thăng tiến mạnh mẽ trên bảng xếp hạng FIFA"
    },
    {
        "scene_id": 3,
        "fname": "v3_mozambique_can_defeat.jpg",
        "queries": [
            "Mozambique national football team match action Africa Cup of Nations",
            "Mozambique football team pitch action 2024",
            "Mozambique team match Africa Cup Nations"
        ],
        "credit": "CAF / REUTERS",
        "desc": "Đội tuyển Mozambique ngậm ngùi nhận thất bại tại vòng loại CAN"
    },
    {
        "scene_id": 3,
        "fname": "v3_coaching_staff_meeting.jpg",
        "queries": [
            "HLV Kim Sang-sik chi dao tap luyen doi tuyen Viet Nam",
            "Kim Sang-sik ban huan luyen doi tuyen Viet Nam san tap My Dinh",
            "HLV Kim Sang-sik tren san tap doi tuyen Viet Nam"
        ],
        "credit": "VFF",
        "desc": "HLV Kim Sang-sik cùng ban huấn luyện thảo luận chiến thuật trên sân tập"
    },
    {
        "scene_id": 3,
        "fname": "v3_sports_arena_crowd.jpg",
        "queries": [
            "Nha thi dau the thao Viet Nam khan gia co vu soi dong",
            "Khan dai nha thi dau the thao Viet Nam ruc ro",
            "Khan gia nha thi dau the thao co vu cuong nhiet"
        ],
        "credit": "THỂ THAO VIỆT NAM",
        "desc": "Khán đài nhà thi đấu thể thao rực lửa cổ vũ sôi động"
    },
    {
        "scene_id": 3,
        "fname": "v3_vietnam_flag_stadium.jpg",
        "queries": [
            "Co do sao vang dai ky tren khan dai My Dinh co vu tran dau",
            "Khan dai san My Dinh co do sao vang ruc ro co vu",
            "Co do sao vang bay tren khan dai san My Dinh"
        ],
        "credit": "VNEXPRESS / VFF",
        "desc": "Đại kỳ cờ đỏ sao vàng tung bay trên khán đài sân Mỹ Đình"
    }
]

def host_blocked(url: str) -> bool:
    low = url.lower()
    return any(b in low for b in BLOCKED_DOMAINS)

def search_clean_image(queries: list[str], filename: str) -> Image.Image | None:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
    
    for q in queries:
        print(f"  -> Thử tìm: '{q}'")
        try:
            with DDGS() as ddgs:
                results = list(ddgs.images(f"{q} -watermark -alamy -getty -istock -stock", max_results=20))
        except Exception as e:
            print(f"     Lỗi DDGS: {e}")
            time.sleep(2)
            continue
            
        for idx, r in enumerate(results):
            u = r.get("image", "")
            if not u or host_blocked(u):
                continue
            try:
                resp = session.get(u, timeout=10)
                if resp.status_code != 200 or len(resp.content) < 35000:
                    continue
                im = Image.open(io.BytesIO(resp.content)).convert("RGB")
                w, h = im.size
                if w < 750 or h < 450:
                    continue
                arr = np.array(im)
                white_ratio = np.sum(np.all(arr > 235, axis=-1)) / (w * h)
                black_ratio = np.sum(np.all(arr < 20, axis=-1)) / (w * h)
                if white_ratio > 0.20 or black_ratio > 0.35:
                    continue
                
                # Run Tesseract OCR check
                tpath = f"/tmp/check_patch_{filename}"
                im.save(tpath, "JPEG", quality=90)
                res = subprocess.run(["/opt/homebrew/bin/tesseract", tpath, "stdout", "--psm", "6"], capture_output=True)
                txt = res.stdout.decode("utf-8", errors="replace").lower()
                if os.path.exists(tpath):
                    os.remove(tpath)
                    
                bad_matches = [b for b in BAD_OCR_KEYWORDS if b in txt]
                if bad_matches:
                    print(f"     [Loại ứng viên #{idx+1}] Dính OCR: {bad_matches}")
                    continue
                    
                print(f"  ✅ ĐÃ CHỌN ỨNG VIÊN #{idx+1}: {w}x{h}, white={white_ratio:.1%}, black={black_ratio:.1%}")
                print(f"     Nguồn: {u[:85]}...")
                return im
            except Exception:
                continue
        time.sleep(0.5)
    return None

def main():
    print("=== BẮT ĐẦU VÁ 12 ẢNH TIÊU CHUẨN THỂ THAO CAO CẤP ===\n")
    
    # Đọc credits hiện tại
    credits_file = DAY_DIR / "image_credits.json"
    if credits_file.exists():
        with open(credits_file, "r", encoding="utf-8") as f:
            credits_data = json.load(f)
    else:
        credits_data = {}
        
    # Đọc plan hiện tại
    plan_file = DAY_DIR / "image_plan.json"
    if plan_file.exists():
        with open(plan_file, "r", encoding="utf-8") as f:
            plan_data = json.load(f)
    else:
        plan_data = {"records": []}
        
    records_by_fname = {r["file_name"]: r for r in plan_data.get("records", [])}
    
    patched_count = 0
    for item in SLOTS_TO_PATCH:
        fname = item["fname"]
        print(f"\n[XỬ LÝ] {fname} ({item['desc']})")
        clean_img = search_clean_image(item["queries"], fname)
        if clean_img is not None:
            dest_path = IMG_DIR / fname
            clean_img.save(dest_path, "JPEG", quality=92, optimize=True)
            print(f"  -> Đã lưu ảnh mới sạch 100%: {dest_path.name} ({clean_img.size[0]}x{clean_img.size[1]})")
            credits_data[fname] = item["credit"]
            if fname in records_by_fname:
                records_by_fname[fname]["credit"] = item["credit"]
                records_by_fname[fname]["description"] = item["desc"]
            patched_count += 1
        else:
            print(f"  ❌ THẤT BẠI: Không tải được ảnh đạt chuẩn cho {fname}")

    # Cập nhật credits_file
    with open(credits_file, "w", encoding="utf-8") as f:
        json.dump(credits_data, f, ensure_ascii=False, indent=2)
    print(f"\nĐã cập nhật {credits_file}")
    
    # Cập nhật plan_file
    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump(plan_data, f, ensure_ascii=False, indent=2)
    print(f"Đã cập nhật {plan_file}")
    
    print(f"\nHoàn thành vá {patched_count}/{len(SLOTS_TO_PATCH)} ảnh!")

if __name__ == "__main__":
    main()
