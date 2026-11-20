#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_qa_images_09_11.py — Pha 2 QA Fix: Thay thế toàn bộ ảnh dọc, ảnh trùng lặp và ảnh lệch ngữ cảnh
được phát hiện qua Contact Sheet QA của ngày 09.11.2026.
"""

import sys
sys.dont_write_bytecode = True

import io
import os
import time
import json
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

import requests
from PIL import Image
from ddgs import DDGS

ROOT = Path(__file__).resolve().parent.parent
DAY_DIR = ROOT / "outputs" / "09.11.2026"
IMG_DIR = DAY_DIR / "images"

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

BLOCKED_HOSTS = [
    "alamy", "gettyimages", "istockphoto", "shutter", "dreamstime", "123rf",
    "depositphotos", "stock.adobe", "freepik", "pinterest", "facebook.",
    "instagram.", "tiktok", "wallpaper", "alphacoders", "deviantart",
    "futbin", "futhead", "sofifa", "vectorstock", "storyblocks", "picfair",
    "vecteezy", "bigstock", "ebay", "etsy", "redbubble", "teepublic",
    "society6", "displate", "ytimg", "youtube", "pngtree", "cgtrader",
    "footyheadlines", "twimg", "hudl", "ftcdn", "fotolia", "pond5", "mixkit",
    "collage", "pinimg", "screenshot", "shopee", "lazada", "tiki",
    "susercontent", "alicdn", "taobao", "amazon", "kamito", "volusion", "store"
]


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


def is_clean_horizontal(p: Path, min_w: int = 800, min_ratio: float = 1.20) -> bool:
    if not p.exists() or p.stat().st_size < 25_000:
        return False
    try:
        with Image.open(p) as im:
            w, h = im.size
            return w >= min_w and h > 0 and (w / h) >= min_ratio
    except Exception:
        return False


def get_scene_hashes(sc_id: int, exclude_indices: List[int]) -> List[int]:
    hashes = []
    for p in sorted(IMG_DIR.glob(f"Tin_{sc_id:02d}_*.jpg")):
        idx = int(p.stem.split("_")[-1])
        if idx in exclude_indices:
            continue
        try:
            with Image.open(p) as im:
                hashes.append(ahash(im))
        except Exception:
            pass
    return hashes


def copy_from_pool(sc_id: int, target_indices: List[int], pool_paths: List[Path]):
    existing_hashes = get_scene_hashes(sc_id, target_indices)
    pool_idx = 0
    for idx in target_indices:
        dst = IMG_DIR / f"Tin_{sc_id:02d}_{idx}.jpg"
        placed = False
        while pool_idx < len(pool_paths):
            cand = pool_paths[pool_idx]
            pool_idx += 1
            if not is_clean_horizontal(cand, min_w=750, min_ratio=1.18):
                continue
            try:
                with Image.open(cand) as im:
                    h = ahash(im)
                    if any(hamming(h, eh) <= 6 for eh in existing_hashes):
                        continue
                    existing_hashes.append(h)
                    im.convert("RGB").save(dst, "JPEG", quality=95, optimize=True)
                    print(f"  [POOL COPY] Tin_{sc_id:02d}_{idx}.jpg <- {cand.relative_to(ROOT)} ({im.size[0]}x{im.size[1]})")
                    placed = True
                    break
            except Exception:
                continue
        if not placed:
            print(f"  [WARN] Pool exhausted for Tin_{sc_id:02d}_{idx}.jpg")


def fetch_ddgs_slot(sc_id: int, idx: int, queries: List[str]):
    dst = IMG_DIR / f"Tin_{sc_id:02d}_{idx}.jpg"
    existing_hashes = get_scene_hashes(sc_id, [idx])
    neg = " -alamy -gettyimages -shutterstock -istock -dreamstime -watermark -ytimg -youtube -shopee -lazada -tiki -collage -poster -banner"

    for q in queries:
        try:
            time.sleep(0.3)
            with DDGS() as ddgs:
                res = list(ddgs.images(q + neg, region="us-en", safesearch="off", size="Large", layout="Wide", max_results=30))
        except Exception as e:
            print(f"  [DDGS ERR] {q}: {e}")
            continue

        res.sort(key=lambda c: int(c.get("width") or 0), reverse=True)
        for cand in res[:25]:
            u = cand.get("image") or ""
            low = u.lower()
            if not u or any(b in low for b in BLOCKED_HOSTS):
                continue
            if low.split("?")[0].endswith((".svg", ".gif")):
                continue
            try:
                r = requests.get(u, headers={"User-Agent": UA}, timeout=10)
                if r.status_code != 200 or len(r.content) < 30_000:
                    continue
                im = Image.open(io.BytesIO(r.content))
                im.load()
                w, h = im.size
                if w < 850 or h == 0 or (w / h) < 1.22:
                    continue
                im = im.convert("RGB")
                # Check not white background product photo
                px = list(im.resize((32, 32)).getdata())
                white_cnt = sum(1 for (rv, gv, bv) in px if rv > 240 and gv > 240 and bv > 240)
                if white_cnt > len(px) * 0.35:
                    continue
                ah = ahash(im)
                if any(hamming(ah, eh) <= 6 for eh in existing_hashes):
                    continue
                im.save(dst, "JPEG", quality=95, optimize=True)
                print(f"  [DDGS OK] Tin_{sc_id:02d}_{idx}.jpg ({w}x{h}) <- {q}")
                return True
            except Exception:
                continue
    print(f"  [DDGS FAIL] Tin_{sc_id:02d}_{idx}.jpg")
    return False


def main():
    print("=== BẮT ĐẦU SỬA LỖI HÌNH ẢNH QA PHA 2 (09.11.2026) ===")

    # 1. Scene 01 (Ronaldo giã từ ĐTQG): Thay Tin_01_7..12 bằng ảnh ngang sạch từ outputs/25.10.2026
    r25_pool_1 = sorted((ROOT / "outputs" / "25.10.2026" / "images").glob("Tin_01_*.jpg")) + \
                 sorted((ROOT / "outputs" / "25.10.2026" / "images").glob("Tin_06_*.jpg"))
    copy_from_pool(1, [7, 8, 9, 10, 11, 12], r25_pool_1)

    # 2. Scene 02 (Ronaldo & Jorge Jesus): Thay Tin_02_6, 8, 9, 10 bằng ảnh ngang sạch từ outputs/25.10.2026
    r25_pool_2 = sorted((ROOT / "outputs" / "25.10.2026" / "images").glob("Tin_02_*.jpg")) + \
                 sorted((ROOT / "outputs" / "25.10.2026" / "images").glob("Tin_03_*.jpg"))
    copy_from_pool(2, [6, 8, 9, 10], r25_pool_2)

    # 3. Scene 03 (Como 9-1 Lens): Thay Tin_03_11 (ảnh dọc)
    fetch_ddgs_slot(3, 11, [
        "Cesc Fabregas Como 1907 coach touchline Serie A",
        "Como 1907 players celebrating goal Nico Paz"
    ])

    # 4. Scene 04 (Real Madrid 3-2 AEK): Thay Tin_04_5, 9, 10, 11, 12 (5 ảnh dọc áo đấu)
    fetch_ddgs_slot(4, 5, ["Federico Valverde Real Madrid celebration Champions League", "Valverde shooting Real Madrid"])
    fetch_ddgs_slot(4, 9, ["Jude Bellingham Kylian Mbappe Real Madrid celebration", "Jude Bellingham Real Madrid Champions League"])
    fetch_ddgs_slot(4, 10, ["Kylian Mbappe Real Madrid goal celebration Champions League", "Mbappe Real Madrid match action"])
    fetch_ddgs_slot(4, 11, ["Carlo Ancelotti Real Madrid Champions League touchline", "Ancelotti Valverde Real Madrid"])
    fetch_ddgs_slot(4, 12, ["Real Madrid team celebration Champions League 2025 2026", "Real Madrid players hugging celebration"])

    # 5. Scene 06 (Liverpool 2-3 Fenerbahce): Thay Tin_06_6 (trùng Tin_06_5)
    orther_05_t4 = sorted((ROOT / "outputs" / "Orther" / "05.11.2026" / "images").glob("Tin_04_*.jpg"))
    copy_from_pool(6, [6], orther_05_t4)

    # 6. Scene 07 (Nottingham 3-1 Man City): Thay Tin_07_4 (ảnh MU), Tin_07_10 (trùng 6), Tin_07_12 (trùng 8)
    w02_t9 = sorted((ROOT / "outputs" / "02.11.2026" / "images").glob("Tin_09_*.jpg"))
    copy_from_pool(7, [4, 10, 12], w02_t9)

    # 7. Scene 08 (Man Utd 4-4 Aston Villa & thứ 18): Thay Tin_08_9 (chart dọc nền trắng) & Tin_08_11 (banner đỏ)
    w02_t8 = sorted((ROOT / "outputs" / "02.11.2026" / "images").glob("Tin_08_*.jpg"))
    copy_from_pool(8, [9, 11], w02_t8)

    # 8. Scene 13 (Bi kịch va chạm sân cỏ): Thay Tin_13_4 (collage 4 ô)
    orther_04_t4 = sorted((ROOT / "outputs" / "Orther" / "04.11.2026" / "images").glob("Tin_04_*.jpg"))
    copy_from_pool(13, [4], orther_04_t4)

    # 9. Scene 14 (51 thẻ đỏ Brazil): Thay Tin_14_2 (collage), Tin_14_5, Tin_14_6 (trùng Tin_14_1)
    orther_04_t1 = sorted((ROOT / "outputs" / "Orther" / "04.11.2026" / "images").glob("Tin_01_*.jpg"))
    copy_from_pool(14, [2, 5, 6], orther_04_t1)

    # 10. Scene 15 (Bóng đá xe đạp Cycle-ball): Thay Tin_15_5 (ảnh dọc)
    orther_07_t1 = sorted((ROOT / "outputs" / "Orther" / "07.11.2026" / "images").glob("Tin_01_*.jpg"))
    copy_from_pool(15, [5], orther_07_t1)

    # 11. Scene 16 (ĐT Việt Nam & Olaha Mạnh Đức): Thay Tin_16_5 (lễ trao quốc tịch phòng họp) & Tin_16_7 (banner bongda24h)
    w02_t18 = sorted((ROOT / "outputs" / "02.11.2026" / "images").glob("Tin_18_*.jpg"))
    copy_from_pool(16, [7], w02_t18)
    fetch_ddgs_slot(16, 5, [
        "Doi tuyen Viet Nam Kim Sang Sik tap luyen VFF",
        "Doi tuyen bong da Viet Nam thi dau san Thien Truong"
    ])

    # 12. Scene 17 (Nam Định giữ đỉnh, HAGL hạ Hà Nội FC): Thay Tin_17_1 (banner chữ), Tin_17_3 (cá voi!), Tin_17_7 (boxing!)
    pool_17 = sorted((ROOT / "outputs" / "02.11.2026" / "images").glob("Tin_18_*.jpg")) + \
              sorted((ROOT / "outputs" / "02.11.2026" / "images").glob("Tin_16_*.jpg")) + \
              sorted((ROOT / "outputs" / "02.11.2026" / "images").glob("Tin_13_*.jpg"))
    copy_from_pool(17, [1, 3, 7], pool_17)

    # 13. Scene 18 (Công Phượng giúp Đồng Nai thắng đầu tay): Thay Tin_18_2 (Đảng bộ), Tin_18_3 (sân khấu), Tin_18_5 (bảng size áo)
    fetch_ddgs_slot(18, 2, [
        "Nguyen Cong Phuong Truong Tuoi Binh Phuoc thi dau",
        "Nguyen Cong Phuong ghi ban giai hang Nhat"
    ])
    fetch_ddgs_slot(18, 3, [
        "Nguyen Cong Phuong di bong tren san co",
        "Cong Phuong an mung ban thang V-League"
    ])
    fetch_ddgs_slot(18, 5, [
        "Nguyen Cong Phuong sut phat den ghi ban",
        "Cau thu Nguyen Cong Phuong doi tuyen Viet Nam thi dau"
    ])

    # 14. Scene 19 (Thể Công Viettel hòa Thanh Hóa 1-1): Thay Tin_19_2 (card Viettel Networks) & Tin_19_5 (thuốc Hapacol!)
    w02_t17 = sorted((ROOT / "outputs" / "02.11.2026" / "images").glob("Tin_17_*.jpg"))
    copy_from_pool(19, [2, 5], w02_t17)

    # 15. Scene 20 (CLB nữ TP.HCM dừng bước Cúp C1): Thay Tin_20_3 (bóng stock) & Tin_20_4 (ca sĩ hát!)
    fetch_ddgs_slot(20, 3, [
        "CLB nu TP HCM AFC Women Champions League thi dau",
        "Huynh Nhu CLB nu TP HCM ghi ban"
    ])
    fetch_ddgs_slot(20, 4, [
        "Doi bong da nu TP HCM an mung chien thang Thong Nhat",
        "Huynh Nhu doi tuyen nu Viet Nam thi dau"
    ])

    # 16. Scene 21 (Chia tay chảo lửa Long An): Thay Tin_21_1, 2, 3, 5, 6 (công trường/ruộng lúa/bất động sản/bảo tàng)
    fetch_ddgs_slot(21, 1, [
        "CLB Dong Tam Long An thi dau san Long An",
        "CLB Long An giai hang Nhat san van dong Long An"
    ])
    fetch_ddgs_slot(21, 2, [
        "Bong da Long An san van dong Long An V-League",
        "Cau thu CLB Long An an mung ban thang"
    ])
    fetch_ddgs_slot(21, 3, [
        "Dong Tam Long An vo dich V-League Henrique Calisto",
        "CLB bong da Long An thi dau tren san nha"
    ])
    fetch_ddgs_slot(21, 5, [
        "Khan gia san van dong Long An bong da",
        "Nguyen Minh Phuong Antonio Carlos Dong Tam Long An"
    ])
    fetch_ddgs_slot(21, 6, [
        "Doi bong Long An tap luyen thi dau giai hang Nhat",
        "Phan Van Tai Em Dong Tam Long An bong da"
    ])

    # 17. Scene 25 (Trần Thị Thanh Thúy rời Nhật Bản): Thay Tin_25_5 (chai Oxi Clean!)
    w02_t25 = sorted((ROOT / "outputs" / "02.11.2026" / "images").glob("Tin_25_*.jpg"))
    copy_from_pool(25, [5], w02_t25)

    print("=== HOÀN TẤT THAY THẾ, CẬP NHẬT LẠI CONTACT SHEETS ===")
    from core.collect_weekly_images_09_11 import generate_contact_sheets
    generate_contact_sheets()


if __name__ == "__main__":
    main()
