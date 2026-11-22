# -*- coding: utf-8 -*-
"""
image_curator.py — Bộ máy thu thập & kiểm duyệt ảnh thể thao HD sạch dùng chung cho Điểm Đọc
============================================================================================
Tích hợp:
  1. Chuẩn hóa URL báo chí Việt Nam (gỡ /thumb_w/<n>/ trên Tuổi Trẻ & Thanh Niên để lấy ảnh gốc HD).
  2. Tìm kiếm ảnh bổ trợ kết hợp Wikimedia Commons API (100% CC sạch watermark) + Bing Image Search
     có bộ lọc từ khóa chủ thể bắt buộc trong title/URL (tránh tuyệt đối ảnh lạc đề).
  3. Chặn tên miền stock/e-commerce, kiểm tra khung viền trắng/đen (letterbox/screenshot) và mật độ cạnh.
  4. Khử trùng lặp cảm nhận thị giác (Perceptual dHash) và hỗ trợ cắt gọn viền logo sát mép.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

sys.dont_write_bytecode = True

import numpy as np
import requests
from PIL import Image, ImageOps

from . import paths
from .short_batch import has_dense_edge_overlay

MIN_W = 800
MIN_H = 450
MIN_RATIO = 1.18
MAX_RATIO = 2.85

BLOCKED_DOMAINS = (
    "alamy.",
    "gettyimages.",
    "shutterstock.",
    "istockphoto.",
    "dreamstime.",
    "123rf.",
    "depositphotos.",
    "vecteezy.",
    "freepik.",
    "stock.adobe.com",
    "ftcdn.net",
    "lookaside.",
    "fbsbx.com",
    "tiktok.com",
    "pinterest.",
    "pinimg.com",
    "shopee.",
    "lazada.",
    "tiki.",
    "amazon.",
    "ebay.",
    "etsy.",
    "aliexpress.",
    "temu.",
    "walmart.",
    "shopify.",
    "ytimg.com",
    "youtube.com",
    "youtu.be",
    "football-asian.com",
    "footballtribe.",
    "vov.vn",
)

BLOCKED_URL_PATTERNS = (
    "static.thanhnien.com.vn",
    "ava_inter",
    "chan-trang-",
    "banner-dai-hoi",
    "bxh-",
    "lichthidau-",
    "lich-thi-dau-",
    "ewttetw",
    "watermark",
    "/wm1-",
    "wm1-",
    "logo",
    "favicon",
    "placeholder",
    "no-image",
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}


def is_blocked_url(url: str) -> bool:
    low = (url or "").lower()
    if not low.startswith(("http://", "https://")):
        return True
    if any(dom in low for dom in BLOCKED_DOMAINS):
        return True
    if any(pat in low for pat in BLOCKED_URL_PATTERNS):
        return True
    return False


def normalize_editorial_urls(url: str) -> List[str]:
    """Gỡ /thumb_w/<n>/ trên Tuổi Trẻ & Thanh Niên để lấy ảnh gốc HD, giữ URL gốc làm fallback."""
    candidates: List[str] = []
    if "cdn2.tuoitre.vn/" in url or "images2.thanhnien.vn/" in url:
        full_url = re.sub(r"/thumb_w/\d+/", "/", url)
        if full_url != url:
            candidates.append(full_url)
    candidates.append(url)
    return candidates


def compute_dhash(img: Image.Image) -> int:
    gray = img.convert("L").resize((9, 8), Image.Resampling.BILINEAR)
    arr = np.asarray(gray, dtype=np.int16)
    diff = arr[:, 1:] > arr[:, :-1]
    h = 0
    for bit in diff.flatten():
        h = (h << 1) | int(bool(bit))
    return h


def hamming_dist(h1: int, h2: int) -> int:
    return (h1 ^ h2).bit_count()


def has_white_ecommerce_or_letterbox_border(img: Image.Image) -> bool:
    small = img.convert("RGB").resize((120, 80), Image.Resampling.BILINEAR)
    arr = np.asarray(small, dtype=np.uint8)
    top, bot, left, right = arr[:6, :, :], arr[-6:, :, :], arr[:, :6, :], arr[:, -6:, :]
    borders = np.concatenate(
        [top.reshape(-1, 3), bot.reshape(-1, 3), left.reshape(-1, 3), right.reshape(-1, 3)],
        axis=0,
    )
    if float(np.mean(np.all(borders > 240, axis=1))) > 0.72:
        return True
    tb = np.concatenate([top.reshape(-1, 3), bot.reshape(-1, 3)], axis=0)
    if float(np.mean(np.all(tb < 14, axis=1))) > 0.88 or float(np.mean(np.all(tb > 245, axis=1))) > 0.88:
        return True
    return False


def trim_edge_margins(img: Image.Image, top_frac: float = 0.0, bottom_frac: float = 0.0) -> Image.Image:
    """Cắt gọn mép trên/dưới (0.0–0.12) để loại bỏ dải logo nhỏ sát mép ảnh."""
    if top_frac <= 0 and bottom_frac <= 0:
        return img
    y0 = int(round(img.height * max(0.0, min(0.15, top_frac))))
    y1 = int(round(img.height * (1.0 - max(0.0, min(0.15, bottom_frac)))))
    if y1 - y0 >= MIN_H:
        return img.crop((0, y0, img.width, y1))
    return img


def validate_and_load_image(
    raw_bytes: bytes,
    strict_search: bool = False,
) -> Tuple[Optional[Image.Image], str]:
    try:
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw_bytes)))
        if strict_search and im.mode in ("RGBA", "LA"):
            alpha = np.asarray(im.getchannel("A"))
            if float(np.mean(alpha < 200)) > 0.12:
                return None, "transparent_cutout"
        rgb = im.convert("RGB")
    except Exception as exc:
        return None, f"decode_err:{exc}"

    w, h = rgb.size
    if w < MIN_W or h < MIN_H:
        return None, f"too_small:{w}x{h}"
    ratio = w / float(h)
    if ratio < MIN_RATIO or ratio > MAX_RATIO:
        return None, f"bad_ratio:{w}x{h}({ratio:.2f})"
    if strict_search:
        if has_white_ecommerce_or_letterbox_border(rgb):
            return None, "white_or_letterbox_border"
        if has_dense_edge_overlay(rgb):
            return None, "dense_edge_overlay"
    return rgb, "ok"


def search_wikimedia_commons(query: str, max_results: int = 8) -> List[Dict[str, Any]]:
    """Truy vấn ảnh thể thao bản quyền mở (không watermark) từ Wikimedia Commons."""
    out: List[Dict[str, Any]] = []
    try:
        resp = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params={
                "action": "query",
                "generator": "search",
                "gsrsearch": f"filetype:bitmap {query}",
                "gsrnamespace": 6,
                "gsrlimit": max_results,
                "prop": "imageinfo",
                "iiprop": "url|size|mime",
                "iiurlwidth": 1600,
                "format": "json",
            },
            headers={"User-Agent": "DiemDocSportsNewsBot/1.0"},
            timeout=10,
        )
        pages = resp.json().get("query", {}).get("pages", {})
        for p in sorted(pages.values(), key=lambda x: int(x.get("index", 999))):
            iis = p.get("imageinfo") or []
            if not iis:
                continue
            info = iis[0]
            w, h = int(info.get("width") or 0), int(info.get("height") or 0)
            if w < MIN_W or h < MIN_H or (w / float(max(1, h))) < MIN_RATIO:
                continue
            u = info.get("thumburl") or info.get("url")
            if u:
                out.append({
                    "image": u,
                    "title": p.get("title", query),
                    "width": w,
                    "height": h,
                    "source": "Wikimedia Commons",
                })
    except Exception:
        pass
    return out


def search_bing_filtered(
    query: str,
    required_tokens: Optional[List[str]] = None,
    max_results: int = 16,
) -> List[Dict[str, Any]]:
    """Tìm ảnh qua Bing backend với bộ lọc từ khóa bắt buộc trong title/URL nhằm chống ảnh lạc đề."""
    from ddgs import DDGS

    if required_tokens is None:
        # Tự trích các từ khóa danh từ riêng / chữ có độ dài >= 4 từ query
        words = [w.lower() for w in re.findall(r"[A-Za-zÀ-ỹ0-9\-]{4,}", query)]
        stop = {"football", "soccer", "match", "player", "action", "stadium", "coach", "team", "national", "world", "league"}
        required_tokens = [w for w in words if w not in stop][:4]

    results: List[Dict[str, Any]] = []
    try:
        raw = DDGS().images(query, region="us-en", backend="bing", safesearch="moderate", max_results=max_results)
        for r in raw or []:
            u = (r.get("image") or "").strip()
            if not u or is_blocked_url(u):
                continue
            hay = ((r.get("title") or "") + " " + u).lower()
            if required_tokens and not any(tok.lower() in hay for tok in required_tokens):
                continue
            results.append(r)
    except Exception:
        pass
    return results
