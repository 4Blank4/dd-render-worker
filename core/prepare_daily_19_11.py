#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prepare_daily_19_11.py — Pha 1: Chia kịch bản từng câu (Intro + 18 bản tin ngày 19.11.2026),
thu thập & kiểm lọc 100% ảnh ngang HD sạch logo/watermark (W >= 800, H >= 450, W/H >= 1.18),
và xuất trọn bộ Contact Sheet QA tại outputs/19.11.2026/qa/.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse
import io
import json
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np
import requests
from ddgs import DDGS
from PIL import Image, ImageDraw, ImageFont

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from daily_19_11_data import INTRO_DATA, NEWS_SPECS
from diemdoc.log import banner, ok, step, warn
from diemdoc.publisher import load_voice_preset
from diemdoc.short_batch import has_dense_edge_overlay

DAY_STR = "19.11.2026"
ROOT = Path(_ROOT)
DAY_DIR = ROOT / "outputs" / DAY_STR
IMG_DIR = DAY_DIR / "images"
QA_DIR = DAY_DIR / "qa"
CACHE_DIR = Path.home() / "Library" / "Caches" / "DiemDoc" / "daily_1911"
QCACHE_PATH = CACHE_DIR / "query_cache.json"

GETTY_TEMPLATE_PATH = os.path.expanduser(
    "~/.gemini/antigravity/brain/7e88202f-ec65-4572-a9c3-e602e2904d70/.user_uploaded/media_1794277963250_04e9947d.png"
)

MIN_WIDTH = 800
MIN_HEIGHT = 450
MIN_RATIO = 1.18

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])(?<!\.\.\.)['\")\]»”’]*\s+")

NEG_KW = (
    " -game -mobile -esports -wallpaper -pes -fifa23 -eafc -vecteezy -shutterstock"
    " -alamy -gettyimages -dreamstime -istockphoto -cartoon -drawing -render -collage"
    " -logo -banner -shopee -lazada -tiki -product -shop -screenshot -watermark -infographic"
)

BLOCKED_HOSTS = [
    "alamy", "getty", "gettyimages", "istockphoto", "shutter", "dreamstime", "123rf",
    "depositphotos", "stock.adobe", "freepik", "pinterest", "facebook.",
    "instagram.", "tiktok", "wallpaper", "alphacoders", "deviantart",
    "futbin", "futhead", "sofifa", "vectorstock", "storyblocks", "picfair",
    "vecteezy", "bigstock", "ebay", "etsy", "redbubble", "teepublic",
    "society6", "displate", "ytimg", "youtube", "pngtree", "cgtrader", "footyheadlines",
    "webcamsus", "twimg", "idman.biz", "hudl", "videoblocks", "ftcdn",
    "fotolia", "huggingface", "hf.co", "pond5", "mixkit", "motionarray",
    "collage", "pinimg", "chatgpt", "screen_shot", "screenshot",
    "illustration", "motionbgs", "watermark", "shopee", "lazada", "tiki",
    "susercontent", "alicdn", "taobao", "amazon", "canstock", "envato",
    "pxhere", "kamito", "volusion", "shopify", "hstatic", "dailymail", "thesun",
    "wm1-", "imago-images", "actionplus", "rexfeatures",
    "agefotostock", "bridgemanimages", "megapixl", "colourbox", "panthermedia",
    "zoonar", "pressfoto", "superstock", "topfoto", "chroniclelive", "lookandlearn",
    "europapress", "europa-press", "sportphotogallery", "sport.photo.gallery",
    "nhandan", "vov.vn", "vtv.vn", "vff.org.vn", "scr.vn", "news.cn", "xinhua",
    "powerpoint", "slideshare", "template", "infographic", "hoaphat", "canva",
    "vietnamplus", "baochinhphu", "congly", "siamsport", "thethaovanhoa",
]

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)


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


def load_getty_template() -> Optional[np.ndarray]:
    if not os.path.exists(GETTY_TEMPLATE_PATH):
        return None
    return cv2.imread(GETTY_TEMPLATE_PATH, 0)


def has_getty_watermark(pil_img: Image.Image, template: Optional[np.ndarray]) -> bool:
    if template is None:
        return False
    try:
        cv_img = cv2.cvtColor(np.array(pil_img.convert("RGB")), cv2.COLOR_RGB2GRAY)
        th, tw = template.shape[:2]
        for scale in (0.45, 0.65, 0.85, 1.0, 1.25):
            tw_s, th_s = int(tw * scale), int(th * scale)
            if tw_s < 12 or th_s < 8 or tw_s > cv_img.shape[1] or th_s > cv_img.shape[0]:
                continue
            tpl_s = cv2.resize(template, (tw_s, th_s))
            res = cv2.matchTemplate(cv_img, tpl_s, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > 0.58:
                return True
        return False
    except Exception:
        return False


def passes_visual_stats(pil_img: Image.Image, check_overlay: bool = False) -> Tuple[bool, str]:
    w, h = pil_img.size
    if w < MIN_WIDTH or h < MIN_HEIGHT:
        return False, f"small {w}x{h}"
    ratio = w / float(max(1, h))
    if ratio < MIN_RATIO:
        return False, f"ratio {ratio:.2f} < {MIN_RATIO}"
    arr = np.array(pil_img.convert("RGB"))
    gray = np.mean(arr, axis=2)
    mean_b = float(np.mean(gray))
    std_b = float(np.std(gray))
    dark_r = float(np.mean(gray < 25))
    white_r = float(np.mean(gray > 245))
    if std_b < 15.0:
        return False, f"flat std={std_b:.1f}"
    if dark_r > 0.86 or mean_b < 14.0:
        return False, f"too dark mean={mean_b:.1f}"
    if white_r > 0.50:
        return False, f"white-bg/logo white={white_r:.2f}"
    if check_overlay and has_dense_edge_overlay(pil_img):
        return False, "dense middle edge overlay"
    return True, f"{w}x{h} r={ratio:.2f}"


def is_blocked_url(url: str) -> bool:
    low = (url or "").lower()
    if "watermark=v1" in low or "/zoom/36_36/" in low:
        return True
    return any(b in low for b in BLOCKED_HOSTS) or "watermark" in low or "logo" in low


def url_variants(url: str) -> List[str]:
    cands = []
    if "thanhnien.vn/thumb_w/" in url:
        cands.append(re.sub(r"/thumb_w/\d+/", "/", url))
        cands.append(url)
    else:
        cands.append(url)
    return cands


class ImageCurator:
    def __init__(self) -> None:
        for d in (DAY_DIR, IMG_DIR, QA_DIR, CACHE_DIR):
            d.mkdir(parents=True, exist_ok=True)
        self.template = load_getty_template()
        if QCACHE_PATH.exists():
            try:
                self.qcache = json.loads(QCACHE_PATH.read_text(encoding="utf-8"))
            except Exception:
                self.qcache = {}
        else:
            self.qcache = {}
        self.used_ddgs_urls: set[str] = set()

    def _save_qcache(self) -> None:
        QCACHE_PATH.write_text(json.dumps(self.qcache, ensure_ascii=False, indent=2), encoding="utf-8")

    def search_ddgs(self, query: str) -> List[Dict[str, Any]]:
        clean_q = query.strip()
        key = clean_q + "|" + NEG_KW
        if key in self.qcache and self.qcache[key]:
            return self.qcache[key]
        for attempt in range(4):
            try:
                time.sleep(0.7)
                with DDGS() as ddgs:
                    res = list(
                        ddgs.images(
                            clean_q + NEG_KW,
                            region="us-en",
                            safesearch="off",
                            size="Large",
                            layout="Wide",
                            max_results=25,
                        )
                    )
                if res:
                    self.qcache[key] = res
                    self._save_qcache()
                    return res
                time.sleep(1.5 * (attempt + 1))
            except Exception:
                time.sleep(2.5 * (attempt + 1))
        return []

    def fetch_url_image(self, url: str, check_overlay: bool = False) -> Optional[Image.Image]:
        for cand_u in url_variants(url):
            if is_blocked_url(cand_u):
                continue
            try:
                resp = requests.get(cand_u, headers={"User-Agent": UA}, timeout=12)
                if resp.status_code != 200 or len(resp.content) < 25_000:
                    continue
                im = Image.open(io.BytesIO(resp.content)).convert("RGB")
                ok_v, _ = passes_visual_stats(im, check_overlay=check_overlay)
                if not ok_v:
                    continue
                if has_getty_watermark(im, self.template):
                    warn(f"Loại ảnh dính watermark Getty: {cand_u[:70]}")
                    continue
                return im
            except Exception:
                continue
        return None

    def try_local(self, path_str: str, seen_hashes: List[int]) -> Optional[Image.Image]:
        p = Path(path_str)
        if not p.exists() or p.stat().st_size < 25_000:
            return None
        try:
            with Image.open(p) as raw_im:
                im = raw_im.convert("RGB")
            ok_v, reason = passes_visual_stats(im, check_overlay=False)
            if not ok_v:
                warn(f"Bỏ ảnh cục bộ {p.name}: {reason}")
                return None
            if has_getty_watermark(im, self.template):
                warn(f"Bỏ ảnh cục bộ dính watermark Getty: {p.name}")
                return None
            h = ahash(im)
            if any(hamming(h, eh) <= 6 for eh in seen_hashes):
                return None
            return im
        except Exception:
            return None

    def resolve_slot(
        self,
        sc_id: int,
        slot_num: int,
        slot: Dict[str, Any],
        seen_hashes: List[int],
        fallback_title: str,
        force: bool = False,
    ) -> Tuple[Path, str, str, str]:
        fname = f"Tin_{sc_id:02d}_{slot_num}.jpg"
        dest = IMG_DIR / fname

        if (not force) and dest.exists() and dest.stat().st_size >= 25_000:
            try:
                with Image.open(dest) as raw_im:
                    im = raw_im.convert("RGB")
                ok_v, dims = passes_visual_stats(im, check_overlay=False)
                if ok_v and not has_getty_watermark(im, self.template):
                    h = ahash(im)
                    if not any(hamming(h, eh) <= 6 for eh in seen_hashes):
                        seen_hashes.append(h)
                        return dest, slot["credit"], slot["desc"], dims
            except Exception:
                pass

        chosen_im: Optional[Image.Image] = None
        chosen_credit = slot["credit"]

        seen_urls_scene: set[str] = set()
        for kind, val in slot["sources"]:
            if kind == "local":
                im = self.try_local(val, seen_hashes)
                if im is not None:
                    chosen_im = im
                    break
            elif kind == "url":
                if val in seen_urls_scene:
                    continue
                im = self.fetch_url_image(val, check_overlay=False)
                if im is not None:
                    h = ahash(im)
                    if not any(hamming(h, eh) <= 6 for eh in seen_hashes):
                        seen_urls_scene.add(val)
                        chosen_im = im
                        break
            elif kind == "ddgs":
                results = self.search_ddgs(val)
                for r in results:
                    u = r.get("image") or ""
                    if not u or u in self.used_ddgs_urls or is_blocked_url(u):
                        continue
                    im = self.fetch_url_image(u, check_overlay=True)
                    if im is None:
                        continue
                    h = ahash(im)
                    if any(hamming(h, eh) <= 6 for eh in seen_hashes):
                        continue
                    self.used_ddgs_urls.add(u)
                    chosen_im = im
                    break
                if chosen_im is not None:
                    break

        if chosen_im is None:
            warn(f"[{fname}] Primary source không đạt, tìm dự phòng cho: {slot['desc'][:60]}")
            fb_queries = []
            if slot["sources"] and slot["sources"][0][0] == "ddgs":
                base_q = slot["sources"][0][1]
                fb_queries.append(f"{base_q} soccer")
                fb_queries.append(" ".join(base_q.split()[:4]) + " match")
            fb_queries.extend([
                "soccer stadium floodlights pitch match",
                "professional soccer players action stadium",
                "sports arena stadium lights night",
                "football pitch goal celebration crowd",
                "international soccer match ball grass",
                "athletic sports competition stadium arena",
            ])
            for fq in fb_queries:
                results = self.search_ddgs(fq)
                for r in results:
                    u = r.get("image") or ""
                    if not u or u in self.used_ddgs_urls or is_blocked_url(u):
                        continue
                    im = self.fetch_url_image(u, check_overlay=True)
                    if im is None:
                        continue
                    h = ahash(im)
                    if any(hamming(h, eh) <= 6 for eh in seen_hashes):
                        continue
                    self.used_ddgs_urls.add(u)
                    chosen_im = im
                    break
                if chosen_im is not None:
                    break

        if chosen_im is None:
            raise RuntimeError(f"Không tìm được ảnh ngang HD sạch cho {fname} ({slot['desc']})")

        seen_hashes.append(ahash(chosen_im))
        chosen_im.save(dest, format="JPEG", quality=94, optimize=True)
        dims = f"{chosen_im.width}x{chosen_im.height}"
        return dest, chosen_credit, slot["desc"], dims


def _load_fonts() -> Tuple[Any, Any, Any, Any]:
    bold_p = ROOT / "assets" / "fonts" / "Be_Vietnam_Pro" / "BeVietnamPro-Bold.ttf"
    reg_p = ROOT / "assets" / "fonts" / "Be_Vietnam_Pro" / "BeVietnamPro-Regular.ttf"
    try:
        return (
            ImageFont.truetype(str(bold_p), 28),
            ImageFont.truetype(str(reg_p), 18),
            ImageFont.truetype(str(bold_p), 15),
            ImageFont.truetype(str(reg_p), 14),
        )
    except Exception:
        d = ImageFont.load_default()
        return d, d, d, d


def render_scene_contact_sheet(
    sc_id: int,
    title: str,
    voice_label: str,
    records: List[Dict[str, Any]],
    out_path: Path,
) -> None:
    cols = 4
    rows = (len(records) + cols - 1) // cols
    cell_w, cell_h, header_h = 470, 360, 92
    canvas_w = cols * cell_w + 40
    canvas_h = rows * cell_h + header_h + 24
    canvas = Image.new("RGB", (canvas_w, canvas_h), (8, 12, 22))
    draw = ImageDraw.Draw(canvas)
    f_hdr, f_sub, f_lbl, f_cap = _load_fonts()

    hdr_tag = "INTRO MỞ MÀN (~30s)" if sc_id == 0 else f"TIN #{sc_id:02d}"
    draw.text((22, 14), f"QA CONTACT SHEET — {hdr_tag}: {title[:76]}", fill=(0, 229, 255), font=f_hdr)
    draw.text(
        (22, 52),
        f"Tổng số ảnh: {len(records)} | Ngang >= {MIN_WIDTH}x{MIN_HEIGHT} (W/H >= {MIN_RATIO}) | Giọng: {voice_label}",
        fill=(190, 208, 228),
        font=f_sub,
    )

    for idx, rec in enumerate(records):
        r, c = divmod(idx, cols)
        x0 = 20 + c * cell_w + 8
        y0 = header_h + r * cell_h + 8
        draw.rectangle([x0 - 2, y0 - 2, x0 + 448, y0 + 342], outline=(0, 180, 216), width=2, fill=(16, 22, 36))
        img_p = IMG_DIR / rec["file_name"]
        with Image.open(img_p) as raw_im:
            im_rgb = raw_im.convert("RGB")
            orig_sz = f"{im_rgb.width}x{im_rgb.height} ({im_rgb.width / max(1, im_rgb.height):.2f})"
            im_rgb.thumbnail((440, 246), Image.Resampling.LANCZOS)
            canvas.paste(im_rgb, (x0 + (446 - im_rgb.width) // 2, y0 + (250 - im_rgb.height) // 2))

        slot_tag = "Tiêu đề" if rec["type"] == "title" else f"Câu {rec['sentence_idx']}"
        draw.text((x0 + 8, y0 + 256), f"{rec['file_name']} [{slot_tag}] • {orig_sz}", fill=(0, 229, 255), font=f_lbl)
        draw.text((x0 + 8, y0 + 280), f"Nguồn: {rec['credit'][:46]}", fill=(250, 204, 21), font=f_cap)
        desc = rec["description"]
        line1 = desc[:56]
        line2 = desc[56:110] + ("..." if len(desc) > 110 else "")
        draw.text((x0 + 8, y0 + 302), line1, fill=(225, 234, 246), font=f_cap)
        if line2:
            draw.text((x0 + 8, y0 + 320), line2, fill=(185, 198, 218), font=f_cap)

    canvas.save(out_path, format="JPEG", quality=92)


def render_overview_sheet(all_scene_entries: List[Tuple[int, str, Path]], out_path: Path) -> None:
    cols = 5
    rows = (len(all_scene_entries) + cols - 1) // cols
    cell_w, cell_h, header_h = 390, 270, 76
    canvas = Image.new("RGB", (cols * cell_w + 30, rows * cell_h + header_h + 20), (8, 12, 22))
    draw = ImageDraw.Draw(canvas)
    f_hdr, f_sub, f_lbl, f_cap = _load_fonts()

    draw.text((20, 14), f"TỔNG QUAN ẢNH ĐẠI DIỆN — BẢN TIN {DAY_STR} (INTRO + 18 BẢN TIN)", fill=(0, 229, 255), font=f_hdr)
    draw.text((20, 48), "Ảnh đại diện chuẩn ngang HD sạch logo/watermark", fill=(190, 208, 228), font=f_sub)

    for idx, (sc_id, title, img_p) in enumerate(all_scene_entries):
        r, c = divmod(idx, cols)
        x0 = 15 + c * cell_w + 6
        y0 = header_h + r * cell_h + 6
        draw.rectangle([x0 - 2, y0 - 2, x0 + 372, y0 + 252], outline=(0, 180, 216), width=2, fill=(16, 22, 36))
        with Image.open(img_p) as raw_im:
            im_rgb = raw_im.convert("RGB")
            im_rgb.thumbnail((364, 200), Image.Resampling.LANCZOS)
            canvas.paste(im_rgb, (x0 + (370 - im_rgb.width) // 2, y0 + (204 - im_rgb.height) // 2))
        tag = "INTRO" if sc_id == 0 else f"TIN {sc_id:02d}"
        draw.text((x0 + 8, y0 + 210), f"[{tag}] {title[:36]}", fill=(0, 229, 255), font=f_lbl)
        draw.text((x0 + 8, y0 + 232), img_p.name, fill=(220, 230, 245), font=f_cap)

    canvas.save(out_path, format="JPEG", quality=92)


def main() -> None:
    parser = argparse.ArgumentParser(description="Chuẩn bị kịch bản từng câu, ảnh ngang HD sạch logo & QA ngày 19.11.2026")
    parser.add_argument("--force", action="store_true", help="Tải và xử lý lại toàn bộ ảnh")
    parser.add_argument("--only", type=int, nargs="+", help="Chỉ xử lý các scene_id chỉ định (0=Intro, 1..18)")
    args = parser.parse_args()

    banner(f"PHA 1 — CHIA CÂU & TÌM ẢNH NGANG HD SẠCH LOGO ({DAY_STR})", "Intro + 18 Tin")
    curator = ImageCurator()
    p_male = load_voice_preset("primary")
    p_female = load_voice_preset("secondary")

    only_set = set(args.only) if args.only else None
    all_specs = [INTRO_DATA] + NEWS_SPECS

    existing_plan_path = DAY_DIR / "image_plan.json"
    existing_records = []
    if existing_plan_path.exists() and only_set is not None:
        existing_records = json.loads(existing_plan_path.read_text(encoding="utf-8")).get("records", [])

    kept_records = [r for r in existing_records if only_set is not None and int(r.get("scene_id", -1)) not in only_set]
    credits_path = DAY_DIR / "image_credits.json"
    all_credits: Dict[str, str] = (
        json.loads(credits_path.read_text(encoding="utf-8")) if (credits_path.exists() and only_set is not None) else {}
    )

    intro_obj: Dict[str, Any] = {}
    news_objs: List[Dict[str, Any]] = []
    overview_entries: List[Tuple[int, str, Path]] = []
    sentence_txt_blocks: List[str] = []

    for spec in all_specs:
        sc_id = int(spec["id"])
        is_intro = (sc_id == 0)

        if is_intro:
            voice_preset = "mixed"
            voice_name = "Song giọng Nữ (Ngọc Huyền) + Nam (Minh Quân Pro)"
            voice_gender = "mixed"
        elif sc_id % 2 == 1:
            voice_preset = "primary"
            voice_name = p_male["voice_id"]
            voice_gender = "male"
        else:
            voice_preset = "secondary"
            voice_name = p_female["voice_id"]
            voice_gender = "female"

        sents = [s.strip() for s in _SENTENCE_SPLIT.split(spec["summary"]) if s.strip()]
        max_s_idx = max((int(sl["sentence_idx"]) for sl in spec["slots"]), default=0)
        if len(sents) != max_s_idx:
            warn(f"[Scene {sc_id:02d}] Số câu split={len(sents)} khác max sentence_idx={max_s_idx}")

        scene_records: List[Dict[str, Any]] = []
        if only_set is not None and sc_id not in only_set:
            scene_records = [r for r in kept_records if int(r.get("scene_id", -1)) == sc_id]
        else:
            step(f"[Scene {sc_id:02d}] Xử lý {len(spec['slots'])} ảnh: {(spec['title'] or spec['group'])[:56]}...")
            seen_hashes: List[int] = []
            for s_idx, slot in enumerate(spec["slots"], start=1):
                dest, cred, desc, dims = curator.resolve_slot(
                    sc_id, s_idx, slot, seen_hashes, spec["title"] or spec["group"],
                    force=args.force,
                )
                all_credits[dest.name] = cred
                rec = {
                    "scene_id": sc_id,
                    "type": slot["type"],
                    "index": 1 if slot["type"] == "title" else slot["sentence_idx"],
                    "sentence_idx": 0 if slot["type"] == "title" else slot["sentence_idx"],
                    "file_name": dest.name,
                    "dimensions": dims,
                    "credit": cred,
                    "description": desc,
                }
                scene_records.append(rec)
                kept_records.append(rec)

            qa_name = "contact_scene_00_intro.jpg" if is_intro else f"contact_scene_{sc_id:02d}.jpg"
            render_scene_contact_sheet(sc_id, spec["title"] or spec["group"], voice_name, scene_records, QA_DIR / qa_name)
            ok(f"  -> Đã xuất {len(scene_records)} ảnh & QA {qa_name}")

        img_paths = [str(IMG_DIR / r["file_name"]) for r in scene_records]
        if img_paths:
            overview_entries.append((sc_id, spec["title"] or spec["group"], Path(img_paths[0])))

        header_line = f"=== INTRO (ID 00) | {voice_name} ===" if is_intro else f"=== TIN #{sc_id:02d} | {spec['group']} | {voice_name} ==="
        lines = [header_line]
        if not is_intro:
            lines.append(f"Tiêu đề: {spec['title']}")
            t_recs = [r for r in scene_records if r["type"] == "title"]
            for r in t_recs:
                lines.append(f"  [Ảnh Tiêu đề] {r['file_name']} ({r.get('dimensions', '')}) | {r['credit']} | {r['description']}")
        for idx_s, s_text in enumerate(sents, start=1):
            lines.append(f"Câu {idx_s}: {s_text}")
            s_recs = [r for r in scene_records if r["type"] == "sentence" and int(r["sentence_idx"]) == idx_s]
            for r in s_recs:
                lines.append(f"  -> {r['file_name']} ({r.get('dimensions', '')}) | {r['credit']} | {r['description']}")
        sentence_txt_blocks.append("\n".join(lines))

        item_entry: Dict[str, Any] = {
            "id": sc_id,
            "art_id": spec["art_id"],
            "group": spec["group"],
            "title": spec["title"],
            "summary": spec["summary"],
            "total_images": len(img_paths),
            "hide_date_chip": False,
            "source": spec["source"],
            "news_source": spec["news_source"],
            "credit": spec["credit"],
            "voice": voice_name,
            "voice_gender": voice_gender,
            "voice_preset": voice_preset,
        }
        if is_intro:
            item_entry["hide_title"] = True
            item_entry["voice_segments"] = spec["voice_segments"]
            item_entry["audio_path"] = str(DAY_DIR / "audio" / "audio_intro.wav")
            item_entry["audio_title"] = ""
        else:
            item_entry["audio_path"] = str(DAY_DIR / "audio" / f"audio_{sc_id:02d}.wav")
            item_entry["audio_title"] = str(DAY_DIR / "audio-title" / f"audio_title_{sc_id:02d}.wav")

        if img_paths:
            item_entry["image_path"] = img_paths[0]
        for idx_i, p_str in enumerate(img_paths, start=1):
            item_entry[f"image_{idx_i}"] = p_str

        if is_intro:
            intro_obj = item_entry
        else:
            news_objs.append(item_entry)

    kept_records.sort(key=lambda r: (int(r.get("scene_id", 0)), 0 if r.get("type") == "title" else int(r.get("sentence_idx", 0))))

    (DAY_DIR / "image_credits.json").write_text(json.dumps(all_credits, ensure_ascii=False, indent=2), encoding="utf-8")
    (DAY_DIR / "image_plan.json").write_text(
        json.dumps({"total_slots": len(kept_records), "records": kept_records}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (DAY_DIR / "intro_hook.json").write_text(json.dumps(intro_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    (DAY_DIR / "thethao.json").write_text(json.dumps(news_objs, ensure_ascii=False, indent=2), encoding="utf-8")
    (DAY_DIR / "kich_ban_tung_cau.txt").write_text("\n\n".join(sentence_txt_blocks) + "\n", encoding="utf-8")

    txt_blocks = []
    for it in news_objs:
        txt_blocks.append(
            f"ID: {it['id']}\nNhóm: {it['group']}\nTiêu đề: {it['title']}\nGiọng: {it['voice']}\nNguồn: {it['source']}\nTóm tắt: {it['summary']}"
        )
    (DAY_DIR / "thethao.txt").write_text("\n\n---\n\n".join(txt_blocks) + "\n", encoding="utf-8")

    if overview_entries:
        render_overview_sheet(overview_entries, QA_DIR / "contact_overview.jpg")

    ok(f"HOÀN TẤT: {len(kept_records)} ảnh ngang HD sạch logo tại {IMG_DIR}")
    ok(f"Kịch bản từng câu: {DAY_DIR / 'kich_ban_tung_cau.txt'}")
    ok(f"QA Contact Sheets: {QA_DIR}")


if __name__ == "__main__":
    main()
