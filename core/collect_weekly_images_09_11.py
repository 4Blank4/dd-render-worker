#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect_weekly_images_09_11.py — Kế thừa và thu thập trọn bộ ~202 ảnh cho 25 bản tin tuần 09.11.2026
Đồng thời tạo Contact Sheet QA 25 cảnh và 5 bảng Overview tổng hợp.
"""

import sys
sys.dont_write_bytecode = True

import os
import io
import time
import json
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import requests
from PIL import Image, ImageDraw, ImageFont
from ddgs import DDGS

ROOT = Path(__file__).resolve().parent.parent
DAY_DIR = ROOT / "outputs" / "09.11.2026"
IMG_DIR = DAY_DIR / "images"
QA_DIR = DAY_DIR / "qa"
CACHE_DIR = Path.home() / "Library" / "Caches" / "DiemDoc" / "weekly_0911"
QCACHE_PATH = CACHE_DIR / "query_cache.json"

for d in (DAY_DIR, IMG_DIR, QA_DIR, CACHE_DIR):
    d.mkdir(parents=True, exist_ok=True)

MIN_RATIO = 1.15
MIN_WIDTH = 750
NEG_KW = " -game -mobile -esports -wallpaper -pes -fifa23 -eafc -vecteezy -shutterstock -alamy -gettyimages -dreamstime -istockphoto -cartoon -drawing -render -collage -logo -banner -shopee -lazada -tiki -product -shop"

BLOCKED_HOSTS = [
    "alamy", "gettyimages", "istockphoto", "shutter", "dreamstime", "123rf",
    "depositphotos", "stock.adobe", "freepik", "pinterest", "facebook.",
    "instagram.", "tiktok", "wallpaper", "alphacoders", "deviantart",
    "futbin", "futhead", "sofifa", "vectorstock", "storyblocks", "picfair",
    "vecteezy", "bigstock", "ebay", "etsy", "redbubble", "teepublic",
    "society6", "displate", "ytimg", "pngtree", "cgtrader", "footyheadlines",
    "webcamsus", "twimg", "idman.biz", "hudl", "videoblocks", "ftcdn",
    "fotolia", "huggingface", "hf.co", "pond5", "mixkit", "motionarray",
    "collage", "forum", "pinimg", "chatgpt", "screen_shot", "screenshot",
    "illustration", "sequence", "givemesportimages", "static-media.fox.com",
    "the18.com", "motionbgs", "watermark", "shopee", "lazada", "tiki",
    "susercontent", "alicdn", "taobao", "amazon"
]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")


def ahash(img: Image.Image) -> int:
    g = img.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
    px = list(g.tobytes())
    m = sum(px) / 64.0
    bits = 0
    for p in px:
        bits = (bits << 1) | (1 if p > m else 0)
    return bits


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def load_json(path: Path, default: Any) -> Any:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default


def save_json(path: Path, data: Any):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def host_blocked(url: str) -> bool:
    low = url.lower()
    return any(b in low for b in BLOCKED_HOSTS) or "watermark" in low


def is_valid_image(p: Path) -> bool:
    if not p.exists() or p.stat().st_size < 25_000:
        return False
    try:
        with Image.open(p) as img:
            w, h = img.size
            if w < MIN_WIDTH or h == 0 or (w / h) < MIN_RATIO:
                return False
        return True
    except Exception:
        return False


class ImageCollector:
    def __init__(self):
        self.qcache = load_json(QCACHE_PATH, {})
        self.lock = threading.Lock()
        self.scene_hashes: Dict[int, List[int]] = {}

    def search(self, query: str) -> List[Dict[str, Any]]:
        clean_q = query.strip()
        key = clean_q + "|" + NEG_KW
        with self.lock:
            if key in self.qcache and self.qcache[key]:
                return self.qcache[key]
        
        for attempt in range(3):
            try:
                time.sleep(0.3)
                with DDGS() as ddgs:
                    res = ddgs.images(
                        clean_q + NEG_KW,
                        region="us-en",
                        safesearch="off",
                        size="Large",
                        layout="Wide",
                        max_results=30
                    )
                res = list(res)
                if res:
                    with self.lock:
                        self.qcache[key] = res
                        save_json(QCACHE_PATH, self.qcache)
                    return res
                time.sleep(1.0)
            except Exception:
                time.sleep(1.5 * (attempt + 1))
        return []

    def fetch(self, url: str) -> Optional[Image.Image]:
        if host_blocked(url):
            return None
        low = url.lower().split("?")[0]
        if low.endswith((".svg", ".gif")):
            return None
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=12)
            if r.status_code != 200 or len(r.content) < 25_000:
                return None
            img = Image.open(io.BytesIO(r.content))
            img.load()
            w, h = img.size
            if w < MIN_WIDTH or h == 0 or (w / h) < MIN_RATIO:
                return None
            if img.mode != "RGB":
                img = img.convert("RGB")
            return img
        except Exception:
            return None

    def collect_slot(self, record: Dict[str, Any]) -> bool:
        sc_id = record["scene_id"]
        fname = record["file_name"]
        out_path = IMG_DIR / fname

        if is_valid_image(out_path):
            try:
                with Image.open(out_path) as im:
                    h = ahash(im)
                    with self.lock:
                        self.scene_hashes.setdefault(sc_id, []).append(h)
                return True
            except Exception:
                pass

        queries = [record["query"]]
        words = record["query"].split()
        if len(words) > 4:
            queries.append(" ".join(words[:4]) + " match action editorial")
            queries.append(" ".join(words[:3]) + " high resolution photo")

        for q in queries:
            cands = self.search(q)
            cands.sort(key=lambda c: int(c.get("width") or 0), reverse=True)

            for cand in cands[:25]:
                u = cand.get("image")
                if not u or host_blocked(u):
                    continue
                img = self.fetch(u)
                if img is None:
                    continue

                h = ahash(img)
                with self.lock:
                    existing_hashes = self.scene_hashes.get(sc_id, [])
                    is_duplicate = any(hamming(h, eh) <= 6 for eh in existing_hashes)
                    if is_duplicate:
                        continue
                    existing_hashes.append(h)
                    self.scene_hashes[sc_id] = existing_hashes

                img.save(out_path, format="JPEG", quality=95, optimize=True)
                return True

        return False


def copy_inherited_images():
    """Kế thừa ảnh đã duyệt QA từ outputs/Orther/."""
    print("=== [BƯỚC 1] KẾ THỪA ẢNH TỪ OUTPUTS/ORTHER ===")
    
    inherited_map = {
        # Tin 1: Ronaldo giã từ ĐTQG (12 ảnh từ 06.11.2026 Tin_01)
        1: [ROOT / "outputs" / "Orther" / "06.11.2026" / "images" / f"Tin_01_{i}.jpg" for i in range(1, 13)],
        # Tin 2: Góc khuất Ronaldo Jorge Jesus (10 ảnh từ 06.11.2026 Tin_02)
        2: [ROOT / "outputs" / "Orther" / "06.11.2026" / "images" / f"Tin_02_{i}.jpg" for i in range(1, 11)],
        # Tin 3: Como 9-1 Lens (12 ảnh từ 05.11.2026 Tin_02)
        3: [ROOT / "outputs" / "Orther" / "05.11.2026" / "images" / f"Tin_02_{i}.jpg" for i in range(1, 13)],
        # Tin 4: Real Madrid 3-2 AEK Athens (12 ảnh từ 05.11.2026 Tin_01)
        4: [ROOT / "outputs" / "Orther" / "05.11.2026" / "images" / f"Tin_01_{i}.jpg" for i in range(1, 13)],
        # Tin 5: Haaland Leipzig 3-2 (6 ảnh từ 05.11.2026 Tin_03)
        5: [ROOT / "outputs" / "Orther" / "05.11.2026" / "images" / f"Tin_03_{i}.jpg" for i in range(1, 7)],
        # Tin 6: Liverpool Fenerbahce 2-3 (6 ảnh từ 05.11.2026 Tin_04)
        6: [ROOT / "outputs" / "Orther" / "05.11.2026" / "images" / f"Tin_04_{i}.jpg" for i in range(1, 7)],
        # Tin 7: Nottingham 3-1 Man City (12 ảnh từ 08.11.2026 Tin_01)
        7: [ROOT / "outputs" / "Orther" / "08.11.2026" / "images" / f"Tin_01_{i}.jpg" for i in range(1, 13)],
        # Tin 8: Man Utd thứ 18 (9 ảnh từ 08.11.2026 Tin_02)
        8: [ROOT / "outputs" / "Orther" / "08.11.2026" / "images" / f"Tin_02_{i}.jpg" for i in range(1, 10)],
        # Tin 12: Jesús de Miguel qua đời (10 ảnh từ 04.11.2026 Tin_02 & 03)
        12: [
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_02_1.jpg",
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_02_2.jpg",
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_02_3.jpg",
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_02_4.jpg",
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_02_5.jpg",
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_03_1.jpg",
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_03_2.jpg",
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_03_3.jpg",
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_03_4.jpg",
            ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / "Tin_03_5.jpg",
        ],
        # Tin 13: Bi kịch va chạm sân cỏ (6 ảnh từ 04.11.2026 Tin_04)
        13: [ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / f"Tin_04_{i}.jpg" for i in range(1, 7)],
        # Tin 14: 51 thẻ đỏ Brazil (6 ảnh từ 04.11.2026 Tin_01)
        14: [ROOT / "outputs" / "Orther" / "04.11.2026" / "images" / f"Tin_01_{i}.jpg" for i in range(1, 7)],
        # Tin 15: Bóng đá xe đạp Cycle-ball (6 ảnh từ 07.11.2026 Tin_01)
        15: [ROOT / "outputs" / "Orther" / "07.11.2026" / "images" / f"Tin_01_{i}.jpg" for i in range(1, 7)],
    }

    copied = 0
    for sc_id, src_list in inherited_map.items():
        for i, src in enumerate(src_list, 1):
            dst = IMG_DIR / f"Tin_{sc_id:02d}_{i}.jpg"
            if src.exists():
                shutil.copy2(src, dst)
                copied += 1
            else:
                print(f"  [CẢNH BÁO] Không tìm thấy ảnh nguồn: {src}")
    print(f"[OK] Đã kế thừa thành công {copied} ảnh sạch từ outputs/Orther/\n")


def build_plan_and_collect_new():
    """Lập danh sách truy vấn tìm ảnh mới và thu thập qua DDGS."""
    queries_for_new = {
        # Tin 8 bổ sung 3 ảnh: trận MU 4-4 Aston Villa
        (8, 10): "Joshua Zirkzee goal Aston Villa 4-4 2026 Manchester United",
        (8, 11): "Patrick Dorgu equalizer 90+6 Manchester United Aston Villa",
        (8, 12): "Manchester United vs Aston Villa 4-4 Old Trafford celebration",

        # Tin 9: Barcelona thắng ngược Atletico Madrid 2-1 (10 ảnh)
        (9, 1): "Fermin Lopez celebration Atletico Madrid Barcelona 2-1 Metropolitano",
        (9, 2): "Fermin Lopez goal Atletico Madrid vs Barcelona La Liga",
        (9, 3): "Atletico Madrid vs Barcelona Metropolitano 2026 match action",
        (9, 4): "Giuliano Simeone goal celebration Atletico Madrid Barcelona",
        (9, 5): "Hansi Flick Barcelona coach Metropolitano match",
        (9, 6): "Diego Simeone Atletico Madrid match Barcelona",
        (9, 7): "Lamine Yamal match action Atletico Madrid vs Barcelona",
        (9, 8): "Real Madrid vs Valencia Mestalla 3-0 2026 match",
        (9, 9): "Kylian Mbappe goal celebration Valencia Real Madrid 3-0",
        (9, 10): "Arda Guler Federico Valverde Valencia Real Madrid",

        # Tin 10: Chelsea thua sốc Sunderland 0-1 (6 ảnh)
        (10, 1): "Chelsea vs Sunderland 0-1 Premier League 2026 match",
        (10, 2): "Sunderland goal celebration Chelsea Stamford Bridge",
        (10, 3): "Cole Palmer Chelsea vs Sunderland disappointed",
        (10, 4): "VAR check controversy Premier League Chelsea Sunderland",
        (10, 5): "Enzo Fernandez Chelsea vs Sunderland action",
        (10, 6): "Sunderland players celebration victory Chelsea",

        # Tin 11: RB Leipzig 6-0 Frankfurt, Dortmund 2-2 Bremen (6 ảnh)
        (11, 1): "RB Leipzig 6-0 Eintracht Frankfurt Bundesliga celebration",
        (11, 2): "Benjamin Sesko RB Leipzig vs Frankfurt match",
        (11, 3): "Xavi Simons RB Leipzig vs Eintracht Frankfurt action",
        (11, 4): "Borussia Dortmund vs Werder Bremen 2-2 Signal Iduna Park",
        (11, 5): "Serhou Guirassy Borussia Dortmund vs Werder Bremen",
        (11, 6): "Dortmund players disappointed Werder Bremen draw",

        # Tin 16: ĐT Việt Nam triệu tập Olaha Mạnh Đức đấu Casper Cup (10 ảnh)
        (16, 1): "HLV Kim Sang-sik doi tuyen Viet Nam luyen tap",
        (16, 2): "Michael Olaha SLNA thi dau V-League",
        (16, 3): "Michael Olaha an mung ban thang SLNA",
        (16, 4): "Kyle Colonna Lương Chí Khải Ha Noi FC V-League",
        (16, 5): "Luong Chi Khai Kyle Colonna trung ve Viet kieu",
        (16, 6): "Doi tuyen Viet Nam tap luyen chuan bi Casper Cup",
        (16, 7): "San van dong Thien Truong Nam Dinh khan dai",
        (16, 8): "Nguyen Tien Linh doi tuyen Viet Nam tap luyen",
        (16, 9): "Quang Hai doi tuyen Viet Nam tap luyen",
        (16, 10): "Kim Sang-sik hop bao doi tuyen Viet Nam",

        # Tin 17: Nam Định giữ vững ngôi đầu, HAGL thoát đáy bảng (10 ảnh)
        (17, 1): "Thep Xanh Nam Dinh an mung chien thang Thien Truong",
        (17, 2): "CLB Nam Dinh vs Hong Linh Ha Tinh 2-1 V-League",
        (17, 3): "HLV Vu Hong Viet Thep Xanh Nam Dinh chi dao",
        (17, 4): "Hoang Anh Gia Lai an mung chien thang Pleiku",
        (17, 5): "HAGL vs Ha Noi FC 2-1 Pleiku V-League",
        (17, 6): "Chau Ngoc Quang HAGL thi dau Ha Noi FC",
        (17, 7): "Tran Minh Vuong HAGL thi dau Pleiku",
        (17, 8): "Cau thu Ha Noi FC that vong Pleiku",
        (17, 9): "Co dong vien Thep Xanh Nam Dinh Thien Truong",
        (17, 10): "Co dong vien HAGL san van dong Pleiku",

        # Tin 18: Công Phượng tỏa sáng giúp Đồng Nai thắng đầu tay (6 ảnh)
        (18, 1): "Nguyen Cong Phuong thi dau Dong Nai Truong Tuoi",
        (18, 2): "Cong Phuong an mung ban thang phat den",
        (18, 3): "Cong Phuong di bong giai hang Nhat",
        (18, 4): "CLB Dong Nai an mung chien thang SHB Da Nang",
        (18, 5): "Cong Phuong ao dau cau lac bo moi",
        (18, 6): "Nguyen Cong Phuong tap luyen san co",

        # Tin 19: Thể Công Viettel hòa Thanh Hóa 1-1 (6 ảnh)
        (19, 1): "The Cong Viettel vs Dong A Thanh Hoa 1-1 Hang Day",
        (19, 2): "Thu mon Nguyen Van Viet The Cong Viettel",
        (19, 3): "The do Nguyen Ba Tien Thanh Hoa The Cong Viettel",
        (19, 4): "Khuat Van Khang The Cong Viettel thi dau",
        (19, 5): "HLV Velizar Popov Thanh Hoa chi dao Hang Day",
        (19, 6): "Cau thu The Cong Viettel that vong chia diem",

        # Tin 20: CLB nữ TP.HCM dừng bước trước đại diện Hàn Quốc cúp C1 (6 ảnh)
        (20, 1): "CLB nu TP Ho Chi Minh AFC Women Champions League",
        (20, 2): "Huynh Nhu thi dau CLB nu TP Ho Chi Minh cup C1",
        (20, 3): "Hwacheon KSPO vs Ho Chi Minh City Women match",
        (20, 4): "Huynh Nhu an mung ban thang nu TP HCM",
        (20, 5): "Doi hinh CLB nu TP Ho Chi Minh chau A",
        (20, 6): "Co dong vien CLB bong da nu TP Ho Chi Minh",

        # Tin 21: Chia tay chảo lửa Long An trước ngày tháo dỡ (6 ảnh)
        (21, 1): "San van dong Long An khan dai co dong vien",
        (21, 2): "San van dong Long An chao lua mien Tay",
        (21, 3): "Tran cau chia tay san van dong Long An",
        (21, 4): "Co dong vien Dong Tam Long An tren khan dai",
        (21, 5): "San van dong Long An nhin tu tren cao",
        (21, 6): "Hinh anh lich su CLB Dong Tam Long An san nha",

        # Tin 22: Trần Quyết Chiến hạ Cho Myung-woo 50-23 (6 ảnh)
        (22, 1): "Tran Quyet Chien World Cup 3 Cushion Yanggu 2026",
        (22, 2): "Tran Quyet Chien danh bai Cho Myung-woo 50-23",
        (22, 3): "Cho Myung-woo World Cup Yanggu Korea Billiards",
        (22, 4): "Tran Quyet Chien carom 3 bang the gioi",
        (22, 5): "Tran Quyet Chien an mung chien thang billiards",
        (22, 6): "Dick Jaspers vs Tran Quyet Chien World Cup",

        # Tin 23: Carlos Alcaraz vô địch Paris Masters 2026 (6 ảnh)
        (23, 1): "Carlos Alcaraz champion Paris Masters 2026 trophy",
        (23, 2): "Carlos Alcaraz vs Ben Shelton final Paris Masters",
        (23, 3): "Carlos Alcaraz celebration Paris Masters 2026",
        (23, 4): "Ben Shelton Paris Masters final 2026 tennis",
        (23, 5): "Carlos Alcaraz forehand Paris Masters indoor",
        (23, 6): "Carlos Alcaraz trophy ceremony Paris Masters",

        # Tin 24: F1 Brazil GP: Lando Norris thắng dưới mưa, Mercedes vô địch sớm (6 ảnh)
        (24, 1): "Lando Norris McLaren winner Brazil GP 2026 Interlagos",
        (24, 2): "Lando Norris wet race celebration Brazil Grand Prix",
        (24, 3): "Mercedes F1 team World Constructors Championship 2026",
        (24, 4): "Interlagos rain race Brazil GP 2026 Formula 1",
        (24, 5): "Lando Norris podium champagne Brazil Grand Prix",
        (24, 6): "George Russell Lewis Hamilton Mercedes celebration 2026",

        # Tin 25: Trần Thị Thanh Thúy chuẩn bị rời Nhật Bản (6 ảnh)
        (25, 1): "Tran Thi Thanh Thuy Gunma Green Wings Japan",
        (25, 2): "Tran Thi Thanh Thuy bong chuyen nu Viet Nam",
        (25, 3): "Thanh Thuy đập bóng Gunma Green Wings",
        (25, 4): "Tran Thi Thanh Thuy an mung Gunma Green Wings",
        (25, 5): "Thanh Thuy doi tuyen bong chuyen nu Viet Nam",
        (25, 6): "Tran Thi Thanh Thuy VTV Binh Dien Long An",
    }

    records = []
    for (sc_id, idx), q in queries_for_new.items():
        records.append({
            "scene_id": sc_id,
            "image_index": idx,
            "file_name": f"Tin_{sc_id:02d}_{idx}.jpg",
            "query": q
        })

    # Lưu image_plan.json
    plan_path = DAY_DIR / "image_plan.json"
    save_json(plan_path, {"total_slots": len(records), "records": records})
    print(f"=== [BƯỚC 2] THU THẬP {len(records)} ẢNH MỚI QUA DDGS ===")

    collector = ImageCollector()
    success = 0
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_map = {executor.submit(collector.collect_slot, r): r for r in records}
        for f in as_completed(f_map):
            r = f_map[f]
            sc_id, fname = r["scene_id"], r["file_name"]
            try:
                ok = f.result()
                if ok:
                    success += 1
                    print(f"  [OK] Scene {sc_id:02d} -> {fname}", flush=True)
                else:
                    print(f"  [FAIL] Scene {sc_id:02d} -> {fname} (query: {r['query']})", flush=True)
            except Exception as e:
                print(f"  [ERR] Scene {sc_id:02d} -> {fname} ({e})", flush=True)

    print(f"[HOÀN THÀNH BƯỚC 2] Tải thành công {success}/{len(records)} ảnh mới.\n")


def generate_contact_sheets():
    """Tạo Contact Sheet QA cho 25 cảnh và 5 bảng Overview tổng hợp."""
    print("=== [BƯỚC 3] TẠO CONTACT SHEET QA (25 SCENES & 5 OVERVIEWS) ===")
    
    thethao_path = DAY_DIR / "thethao.json"
    items = load_json(thethao_path, [])
    titles_map = {it["id"]: it["title"] for it in items}

    # Font setup
    font_path = ROOT / "assets" / "fonts" / "Be_Vietnam_Pro" / "BeVietnamPro-Bold.ttf"
    if not font_path.exists():
        font_path = ROOT / "assets" / "fonts" / "Roboto" / "Roboto-Bold.ttf"
    
    try:
        title_font = ImageFont.truetype(str(font_path), 22)
        font = ImageFont.truetype(str(font_path), 14)
        ov_title_font = ImageFont.truetype(str(font_path), 28)
    except Exception:
        title_font = font = ov_title_font = ImageFont.load_default()

    overview_scenes = {}

    for sid in range(1, 26):
        imgs = sorted(list(IMG_DIR.glob(f"Tin_{sid:02d}_*.jpg")), key=lambda p: int(p.stem.split("_")[-1]))
        if not imgs:
            continue

        cols = 4 if len(imgs) >= 8 else 3
        rows = (len(imgs) + cols - 1) // cols
        tw, th = 320, 180
        header_h = 56
        sheet_w = cols * (tw + 12) + 12
        sheet_h = header_h + rows * (th + 36) + 12

        sheet = Image.new("RGB", (sheet_w, sheet_h), (7, 11, 20))
        draw = ImageDraw.Draw(sheet)

        stitle = titles_map.get(sid, f"Scene {sid:02d}")
        draw.text((16, 12), f"QA SCENE {sid:02d} — {stitle.upper()} ({len(imgs)} ẢNH)", fill=(0, 229, 255), font=title_font)
        draw.line([(16, 44), (sheet_w - 16, 44)], fill=(0, 229, 255), width=2)

        for i, f in enumerate(imgs):
            r, c = divmod(i, cols)
            x = 12 + c * (tw + 12)
            y = header_h + r * (th + 36)
            try:
                im = Image.open(f)
                orig_size = f"{im.size[0]}x{im.size[1]}"
                im.thumbnail((tw, th), Image.Resampling.LANCZOS)
                ox = x + (tw - im.size[0]) // 2
                oy = y + (th - im.size[1]) // 2
                sheet.paste(im, (ox, oy))
                draw.rectangle([(x, y), (x + tw, y + th)], outline=(30, 41, 59), width=1)
            except Exception:
                orig_size = "Error"

            label_txt = f"{f.name} ({orig_size})"
            draw.text((x + 2, y + th + 6), label_txt, fill=(255, 210, 90), font=font)

        out_qa = QA_DIR / f"contact_scene_{sid:02d}.jpg"
        sheet.save(out_qa, "JPEG", quality=88)
        print(f"  [OK] Đã lưu bảng cảnh: {out_qa.name}")

        # Thumbnail cho Overview
        thumb_im = sheet.copy()
        thumb_im.thumbnail((620, 420), Image.Resampling.LANCZOS)
        overview_scenes[sid] = thumb_im

    # Sinh 5 bảng Overview (Mỗi bảng 5 scenes: 1-5, 6-10, 11-15, 16-20, 21-25)
    ranges = [
        (1, 5, "overview_scenes_01_05.jpg"),
        (6, 10, "overview_scenes_06_10.jpg"),
        (11, 15, "overview_scenes_11_15.jpg"),
        (16, 20, "overview_scenes_16_20.jpg"),
        (21, 25, "overview_scenes_21_25.jpg")
    ]

    for start_s, end_s, out_name in ranges:
        scenes_in_range = [overview_scenes[s] for s in range(start_s, end_s + 1) if s in overview_scenes]
        if not scenes_in_range:
            continue

        ocols = 3
        orows = 2
        otw, oth = 620, 420
        ov_w = ocols * (otw + 16) + 16
        ov_h = 70 + orows * (oth + 30) + 16
        ov_sheet = Image.new("RGB", (ov_w, ov_h), (7, 11, 20))
        ov_draw = ImageDraw.Draw(ov_sheet)

        ov_draw.text((20, 18), f"TỔNG HỢP KIỂM DUYỆT THỊ GIÁC QA — CẢNH {start_s:02d} ĐẾN {end_s:02d} (TUẦN 09.11.2026)", fill=(0, 229, 255), font=ov_title_font)
        ov_draw.line([(20, 56), (ov_w - 20, 56)], fill=(0, 229, 255), width=2)

        for i, tim in enumerate(scenes_in_range):
            r, c = divmod(i, ocols)
            x = 16 + c * (otw + 16)
            y = 70 + r * (oth + 30)
            ox = x + (otw - tim.size[0]) // 2
            oy = y + (oth - tim.size[1]) // 2
            ov_sheet.paste(tim, (ox, oy))
            ov_draw.rectangle([(x, y), (x + otw, y + oth)], outline=(30, 41, 59), width=1)

        out_ov = QA_DIR / out_name
        ov_sheet.save(out_ov, "JPEG", quality=85)
        print(f"[OK] Đã lưu Overview Contact Sheet: {out_ov.name}")


def main():
    copy_inherited_images()
    build_plan_and_collect_new()
    generate_contact_sheets()


if __name__ == "__main__":
    main()
