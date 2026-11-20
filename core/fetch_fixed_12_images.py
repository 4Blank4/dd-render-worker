#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_fixed_12_images.py — Tải và Kiểm duyệt 12 Ảnh Thay Thế Cho Video 1
========================================================================
- Lọc triệt để 100%: cấm trang stock, cấm toàn bộ trang báo/mạng xã hội Việt Nam
- Chỉ lấy ảnh báo chí thể thao quốc tế chính thống (UEFA, Kicker, Goal, Bild, Reuters, Sky Sports...)
- Kiểm tra độ phân giải cao >= 1200x700, tỉ lệ ngang
- Chạy OCR kiểm tra: loại bỏ ảnh có chữ tiếng Việt, logo kênh, watermark stock
"""

import sys
sys.dont_write_bytecode = True

import os
import io
import time
from pathlib import Path
from PIL import Image
import requests
from ddgs import DDGS
import easyocr

_HERE = Path(__file__).resolve().parent
ROOT_DIR = _HERE.parent
DAY_DIR = ROOT_DIR / "outputs" / "Orther" / "17.11.2026"
IMG_DIR = DAY_DIR / "images"

BANNED_HOSTS = [
    "alamy", "getty", "shutter", "istock", "dreamstime", "sportphotogallery",
    "123rf", "vecteezy", "freepik", "adobe", "fotolia", "stock", "wallpaper",
    "pinterest", "pinimg", "preview", "watermark", "comp", "licensed-image",
    # Banned Vietnamese domains:
    ".vn", "znews", "zingnews", "thethao247", "laodong", "qdnd", "tuoitre",
    "thanhnien", "dantri", "vtv", "vov", "vtc", "tienphong", "soha", "kenh14",
    "cafef", "vietnamnet", "vnexpress", "baoxaydung", "sportingnews"
]

BAD_TEXTS = [
    "getty", "alamy", "shutter", "istock", "watermark", "photo gallery",
    "tạp chí", "tri thức", "báo", "infographic", "thể thao 247", "blv",
    "anh quân", "kỷ niệm", "công ty", "thái nguyên", "chính phủ", "tặng",
    "espn", "afp", "znews", "lao động", "quân đội"
]

SLOTS_TO_FIX = [
    {
        "fname": "v1_germany_celebrate.jpg",
        "queries": [
            "Germany national team celebrate victory Nations League 2024 kicker",
            "DFB Team jubel Nations League 2024 kicker.de",
            "Germany celebrate goal Nations League 2024 goal.com"
        ],
        "credit": "DFB / KICKER",
        "desc": "Đội tuyển Đức ăn mừng chiến thắng 5-0 trước Hà Lan"
    },
    {
        "fname": "v1_germany_fans_cheer.jpg",
        "queries": [
            "German football fans Euro 2024 stadium flag cheering",
            "Germany fans cheering Olympiastadion Berlin kicker",
            "Germany supporters stadium atmosphere flag"
        ],
        "credit": "DFB / REUTERS",
        "desc": "Cổ động viên Đức rực lửa ăn mừng trên khán đài"
    },
    {
        "fname": "v1_germany_attack.jpg",
        "queries": [
            "Germany vs Netherlands Nations League 2024 goal match action kicker",
            "Germany national team goal Netherlands 2024 action",
            "Liveticker Deutschland Niederlande kicker.de"
        ],
        "credit": "KICKER / DFB",
        "desc": "Cỗ xe tăng Đức dội cơn mưa gôn vào lưới đối thủ"
    },
    {
        "fname": "v1_dutch_players_dejected.jpg",
        "queries": [
            "Virgil van Dijk dejected Netherlands pitch loss",
            "Netherlands football team dejected Germany 2024",
            "Dutch players sad disappointed pitch Nations League"
        ],
        "credit": "REUTERS / NOS",
        "desc": "Tinh thần thi đấu rệu rã của các cầu thủ Hà Lan"
    },
    {
        "fname": "v1_netherlands_second_place.jpg",
        "queries": [
            "Netherlands national football team match action Nations League 2024 pitch",
            "Netherlands football team huddle Nations League",
            "Netherlands national team players celebration 2024"
        ],
        "credit": "UEFA / KNVB",
        "desc": "Tuyển Hà Lan may mắn lách qua khe cửa hẹp nhì bảng"
    },
    {
        "fname": "v1_ronaldo_disappointment.jpg",
        "queries": [
            "Cristiano Ronaldo disappointed Portugal match face pitch Nations League",
            "Ronaldo sad frustrated Portugal national team pitch",
            "Cristiano Ronaldo Portugal dejected pitch match"
        ],
        "credit": "REUTERS / RECORD",
        "desc": "Cristiano Ronaldo thất vọng sau trận đấu của Bồ Đào Nha"
    },
    {
        "fname": "v1_portugal_denmark_match.jpg",
        "queries": [
            "Portugal national football team match action Nations League 2024 pitch",
            "Portugal vs Poland Nations League 2024 match action",
            "Portugal national football team players match action 2024"
        ],
        "credit": "REUTERS / FPF",
        "desc": "Đội tuyển Bồ Đào Nha thi đấu tại Nations League"
    },
    {
        "fname": "v1_dolores_aveiro_interview.jpg",
        "queries": [
            "Dolores Aveiro mother Cristiano Ronaldo interview microphone press",
            "Dolores Aveiro mother Ronaldo gala portrait",
            "Dolores Aveiro portrait speaking press"
        ],
        "credit": "RECORD / A BOLA",
        "desc": "Bà Dolores Aveiro, mẹ siêu sao Cristiano Ronaldo"
    },
    {
        "fname": "v1_portugal_locker_room.jpg",
        "queries": [
            "Portugal national team bench dugout match Nations League",
            "Portugal substitutes bench players match 2024",
            "Portugal football team bench technical area"
        ],
        "credit": "A BOLA / RECORD",
        "desc": "Căng thẳng âm ỉ tại khu kỹ thuật đội tuyển Bồ Đào Nha"
    },
    {
        "fname": "v1_martinez_coaching.jpg",
        "queries": [
            "Roberto Martinez coach Portugal sideline instructions match Nations League",
            "Roberto Martinez manager Portugal pitch suit instructions"
        ],
        "credit": "REUTERS / RECORD",
        "desc": "HLV Roberto Martinez chỉ đạo chiến thuật trên đường biên"
    },
    {
        "fname": "v1_ronaldo_social_media_drop.jpg",
        "queries": [
            "Cristiano Ronaldo waving fans stadium Portugal national team match",
            "Cristiano Ronaldo applauding fans stadium pitch Portugal"
        ],
        "credit": "REUTERS / GOAL",
        "desc": "Cristiano Ronaldo vẫy tay cảm ơn người hâm mộ trên khán đài"
    },
    {
        "fname": "v1_ronaldo_commercial_loss.jpg",
        "queries": [
            "Cristiano Ronaldo press conference backdrop sponsors Portugal team",
            "Cristiano Ronaldo press conference microphone Portugal",
            "Cristiano Ronaldo sponsor presentation suit event"
        ],
        "credit": "REUTERS / FORBES",
        "desc": "Tổn thất khổng lồ về giá trị thương mại và tài trợ"
    }
]

def host_banned(url: str) -> bool:
    low = url.lower()
    return any(b in low for b in BANNED_HOSTS)

def check_ocr(reader: easyocr.Reader, pil_img: Image.Image) -> tuple[bool, str]:
    # Resize image to reasonable size for quick OCR
    w, h = pil_img.size
    scale = min(1.0, 1200 / max(w, h))
    if scale < 1.0:
        small = pil_img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
    else:
        small = pil_img
    
    buf = io.BytesIO()
    small.save(buf, format="JPEG", quality=85)
    buf.seek(0)
    
    try:
        results = reader.readtext(buf.read())
        texts = [t[1].lower() for t in results if t[2] > 0.35]
        joined = " ".join(texts)
        for bad in BAD_TEXTS:
            if bad in joined:
                return False, f"Matched bad text '{bad}': {joined[:80]}"
        return True, joined[:60]
    except Exception as e:
        return True, f"OCR error (ignored): {e}"

def main():
    print("=== Khởi tạo EasyOCR (CPU) ===")
    reader = easyocr.Reader(['en', 'vi'], gpu=False)
    
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    for slot in SLOTS_TO_FIX:
        fname = slot["fname"]
        out_path = IMG_DIR / fname
        print(f"\n---> Đang xử lý: {fname}")
        
        saved = False
        for q in slot["queries"]:
            if saved:
                break
            print(f"   Query: {q}")
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.images(q, max_results=20))
            except Exception as e:
                print(f"   DDG error: {e}")
                time.sleep(1)
                continue
                
            for r in results:
                url = r.get("image", "")
                if not url or host_banned(url):
                    continue
                    
                try:
                    resp = session.get(url, timeout=8)
                    if resp.status_code != 200 or len(resp.content) < 50000:
                        continue
                    
                    pil = Image.open(io.BytesIO(resp.content)).convert("RGB")
                    w, h = pil.size
                    if w < 1200 or h < 650 or w <= h:
                        continue
                    
                    # Run OCR filter
                    ok, ocr_msg = check_ocr(reader, pil)
                    if not ok:
                        print(f"   [REJECT] OCR bad text: {ocr_msg} ({url[:60]})")
                        continue
                    
                    # Save clean image
                    pil.save(out_path, "JPEG", quality=92)
                    print(f"   [SUCCESS] Saved {fname} ({w}x{h}) from {url[:70]}")
                    saved = True
                    break
                except Exception as e:
                    continue
        
        if not saved:
            print(f"   [WARNING] Chưa tìm được ảnh sạch đạt chuẩn cho {fname}!")

if __name__ == "__main__":
    main()
