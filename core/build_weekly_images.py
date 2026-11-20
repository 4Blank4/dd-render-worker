#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_weekly_images.py — Thu thập & Kiểm duyệt 214 ảnh cho 25 bản tin tuần qua (02.11.2026)
========================================================================================
- Đọc image_plan.json từ outputs/02.11.2026/
- Tìm ảnh chất lượng cao qua DDGS (size=Large, layout=Wide)
- Đa luồng 3 workers an toàn với rate-limit của DDGS
- Lọc chặt chẽ:
  + Độ rộng tối thiểu >= 800px (ưu tiên >= 1200px)
  + Tỷ lệ ngang W/H >= 1.18 (chuẩn 16:9)
  + Chặn 100% kho ảnh stock watermark (Alamy, Getty, Shutterstock, iStock, Dreamstime...)
  + Khử trùng lặp aHash (Hamming <= 6)
- Lưu vào outputs/02.11.2026/images/Tin_XX_N.jpg
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import os
import io
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import requests
from PIL import Image
from ddgs import DDGS

ROOT = Path(__file__).resolve().parent.parent
DAY_DIR = ROOT / "outputs" / "02.11.2026"
IMG_DIR = DAY_DIR / "images"
CACHE_DIR = Path.home() / "Library" / "Caches" / "DiemDoc" / "weekly_0211"
STAGING_DIR = CACHE_DIR / "staging"
QA_DIR = CACHE_DIR / "qa"
QCACHE_PATH = CACHE_DIR / "query_cache.json"

for d in (DAY_DIR, IMG_DIR, CACHE_DIR, STAGING_DIR, QA_DIR):
    d.mkdir(parents=True, exist_ok=True)

MIN_RATIO = 1.18
MIN_WIDTH = 800
NEG_KW = " -game -mobile -esports -wallpaper -pes -fifa23 -eafc -vecteezy -shutterstock -alamy -gettyimages -dreamstime -istockphoto -cartoon -drawing -render -collage -logo -banner"

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
    "the18.com", "motionbgs", "watermark"
]

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")


def ahash(img: Image.Image) -> int:
    g = img.convert("L").resize((8, 8), Image.LANCZOS)
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
                # Tránh nghẽn DDGS bằng cách sleep ngắn giữa các request mới
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
                time.sleep(2.0 * (attempt + 1))
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

            for cand in cands[:20]:
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

                # Lưu ảnh chất lượng cao 95%
                img.save(out_path, format="JPEG", quality=95, optimize=True)
                return True

        return False


def main():
    plan_path = DAY_DIR / "image_plan.json"
    if not plan_path.exists():
        print(f"Error: {plan_path} does not exist!")
        sys.exit(1)

    plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
    records = plan_data["records"]
    total = len(records)
    print(f"BẮT ĐẦU THU THẬP & KIỂM DUYỆT {total} ẢNH CHO 25 BẢN TIN (NGÀY 02.11.2026)")
    print("=" * 80)

    collector = ImageCollector()
    success_count = 0
    fail_records = []

    # Sử dụng 3 workers để tải song song an toàn
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_rec = {executor.submit(collector.collect_slot, r): r for r in records}
        completed = 0
        for future in as_completed(future_to_rec):
            rec = future_to_rec[future]
            completed += 1
            fname = rec["file_name"]
            sc_id = rec["scene_id"]
            try:
                ok = future.result()
                if ok:
                    success_count += 1
                    status = "[OK]"
                else:
                    fail_records.append(rec)
                    status = "[FAILED]"
            except Exception as e:
                fail_records.append(rec)
                status = f"[ERR: {e}]"

            if completed % 10 == 0 or completed == total or status == "[FAILED]":
                print(f"[{completed:03d}/{total:03d}] Scene {sc_id:02d} -> {fname} {status} (Tổng đạt: {success_count}/{completed})", flush=True)

    print("\n" + "=" * 80)
    print(f"KẾT QUẢ THU THẬP: {success_count}/{total} ảnh thành công ({success_count/total*100:.1f}%)")
    if fail_records:
        print(f"Số ảnh chưa tải được: {len(fail_records)}")
        for fr in fail_records[:15]:
            print(f"  - {fr['file_name']}: {fr['query']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
