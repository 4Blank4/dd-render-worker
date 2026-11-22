# -*- coding: utf-8 -*-
"""
prepare_daily_22_11.py — Thu thập ảnh sạch HD không logo/watermark, đối chứng từng câu,
xuất kịch bản chuẩn hóa và dựng Contact Sheet QA cho bản tin ngày 22.11.2026
(Intro + 22 tin chính Việt Nam & Thế giới + Mục 23 Các tin thể thao khác).
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import numpy as np
import requests
from ddgs import DDGS
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

from core.diemdoc import paths
from core.diemdoc.image_curator import (
    HEADERS,
    MAX_RATIO,
    MIN_H,
    MIN_RATIO,
    MIN_W,
    compute_dhash,
    hamming_dist,
    has_white_ecommerce_or_letterbox_border,
    is_blocked_url,
    normalize_editorial_urls,
    search_bing_filtered,
    search_wikimedia_commons,
    trim_edge_margins,
)
from core.diemdoc.short_batch import has_dense_edge_overlay
import daily_22_11_data as data_22_11

DAY_STR = "22.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
IMG_DIR = OUT_DIR / "images"
QA_DIR = OUT_DIR / "qa"
CACHE_DIR = Path(paths.WORK) / "img_cache_22_11"

VOICE_INFO = {
    "primary": ("Minh Quân Pro", "male"),
    "secondary": ("Ngọc Huyền", "female"),
    "mixed": ("Song giọng Nữ & Nam", "mixed"),
}


def validate_and_load_image(
    raw_bytes: bytes,
    strict_search: bool = False,
) -> Tuple[Optional[Image.Image], str]:
    try:
        im = Image.open(io.BytesIO(raw_bytes))
        im = ImageOps.exif_transpose(im)
        if strict_search and im.mode in ("RGBA", "LA"):
            alpha = np.asarray(im.getchannel("A"))
            transparent_ratio = float(np.mean(alpha < 200))
            if transparent_ratio > 0.12:
                return None, f"transparent_cutout({transparent_ratio:.2f})"
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


class ImageCurator22:
    def __init__(self) -> None:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.search_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.used_dhashes: List[int] = []
        self.used_sha256: Set[str] = set()
        self.fallback_warnings: List[str] = []
        self.failures: List[str] = []

    def _download_cached(self, url: str, timeout: int = 18) -> Optional[bytes]:
        key = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
        cache_path = CACHE_DIR / f"url_{key}.bin"
        if cache_path.exists() and cache_path.stat().st_size > 8000:
            return cache_path.read_bytes()

        hdrs = dict(HEADERS)
        if "vnecdn.net" in url:
            hdrs["Referer"] = "https://vnexpress.net/"
        elif "tuoitre.vn" in url:
            hdrs["Referer"] = "https://tuoitre.vn/"
        elif "thanhnien.vn" in url:
            hdrs["Referer"] = "https://thanhnien.vn/"
        elif "dantri.com.vn" in url:
            hdrs["Referer"] = "https://dantri.com.vn/"
        elif "365dm.com" in url:
            hdrs["Referer"] = "https://www.skysports.com/"

        try:
            resp = self.session.get(url, headers=hdrs, timeout=timeout, allow_redirects=True)
            if resp.status_code != 200 or len(resp.content) < 8000:
                return None
            ctype = (resp.headers.get("Content-Type") or "").lower()
            if "html" in ctype or "xml" in ctype or "svg" in ctype:
                return None
            cache_path.write_bytes(resp.content)
            return resp.content
        except Exception:
            return None

    def _search_curated(self, query: str) -> List[Dict[str, Any]]:
        if query in self.search_cache:
            return self.search_cache[query]
        q_key = hashlib.sha256(query.encode("utf-8")).hexdigest()[:20]
        json_cache = CACHE_DIR / f"search_{q_key}.json"
        if json_cache.exists():
            try:
                res = json.loads(json_cache.read_text(encoding="utf-8"))
                self.search_cache[query] = res
                return res
            except Exception:
                pass

        combined: List[Dict[str, Any]] = []
        seen_urls: Set[str] = set()

        for item in search_bing_filtered(query, max_results=16):
            u = (item.get("image") or "").strip()
            if u and u not in seen_urls:
                seen_urls.add(u)
                combined.append(item)

        if len(combined) < 6:
            for item in search_wikimedia_commons(query, max_results=8):
                u = (item.get("image") or "").strip()
                if u and u not in seen_urls:
                    seen_urls.add(u)
                    combined.append(item)

        if len(combined) < 4:
            words = [w.lower() for w in re.findall(r"[A-Za-zÀ-ỹ0-9\-]{4,}", query)]
            stop = {"football", "soccer", "match", "player", "action", "stadium", "coach", "team", "national", "world", "league"}
            req_tokens = [w for w in words if w not in stop][:4]
            for attempt in range(2):
                try:
                    raw = DDGS().images(query, region="wt-wt", safesearch="moderate", max_results=20)
                    for r in raw or []:
                        u = (r.get("image") or "").strip()
                        if not u or is_blocked_url(u) or u in seen_urls:
                            continue
                        hay = ((r.get("title") or "") + " " + u).lower()
                        if req_tokens and not any(tok in hay for tok in req_tokens):
                            continue
                        seen_urls.add(u)
                        combined.append(r)
                    if combined:
                        break
                except Exception:
                    time.sleep(0.6 * (attempt + 1))

        if combined:
            json_cache.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")
        self.search_cache[query] = combined
        return combined

    def _is_duplicate_for_search(self, img: Image.Image, raw_bytes: bytes) -> bool:
        sha = hashlib.sha256(raw_bytes).hexdigest()
        if sha in self.used_sha256:
            return True
        dh = compute_dhash(img)
        for prev in self.used_dhashes:
            if hamming_dist(dh, prev) <= 5:
                return True
        return False

    def _mark_used(self, img: Image.Image, raw_bytes: bytes) -> None:
        self.used_sha256.add(hashlib.sha256(raw_bytes).hexdigest())
        self.used_dhashes.append(compute_dhash(img))

    def _try_search_query(self, query: str) -> Tuple[Optional[Image.Image], str]:
        candidates = self._search_curated(query)
        reasons: List[str] = []
        for item in candidates:
            u = (item.get("image") or "").strip()
            if not u or is_blocked_url(u):
                continue
            pw = int(item.get("width") or 0)
            ph = int(item.get("height") or 0)
            if (pw > 0 and pw < MIN_W) or (ph > 0 and ph < MIN_H):
                continue
            raw = self._download_cached(u, timeout=14)
            if not raw:
                continue
            img, reason = validate_and_load_image(raw, strict_search=True)
            if img is None:
                reasons.append(reason)
                continue
            if self._is_duplicate_for_search(img, raw):
                reasons.append("dup")
                continue
            self._mark_used(img, raw)
            return img, f"search:{u[:70]}"
        return None, f"search_exhausted({len(candidates)}):{','.join(reasons[:4])}"

    def acquire_slot(
        self, scene_id: int, slot_idx: int, slot: Dict[str, Any]
    ) -> Tuple[Optional[Image.Image], str, bool]:
        sources: List[Tuple[str, str]] = slot.get("sources") or []
        fail_notes: List[str] = []

        for src_kind, src_val in sources:
            if src_kind == "local":
                p = Path(src_val)
                if not p.exists():
                    fail_notes.append(f"local_missing:{p.name}")
                    continue
                raw = p.read_bytes()
                img, reason = validate_and_load_image(raw, strict_search=False)
                if img is None:
                    fail_notes.append(f"local_invalid({reason}):{p.name}")
                    continue
                self._mark_used(img, raw)
                return img, f"local:{p.name}", False

            elif src_kind == "url":
                if is_blocked_url(src_val):
                    fail_notes.append(f"url_blocked:{src_val[:60]}")
                    continue
                for cand_url in normalize_editorial_urls(src_val):
                    raw = self._download_cached(cand_url)
                    if not raw:
                        fail_notes.append(f"http_fail:{cand_url[:60]}")
                        continue
                    img, reason = validate_and_load_image(raw, strict_search=False)
                    if img is None:
                        fail_notes.append(f"img_reject({reason}):{cand_url[:60]}")
                        continue
                    self._mark_used(img, raw)
                    return img, f"url:{cand_url[:70]}", False

            elif src_kind == "ddgs":
                img, info = self._try_search_query(src_val)
                if img is not None:
                    return img, info, False
                fail_notes.append(f"search_fail({src_val}):{info}")

        desc = (slot.get("desc") or "").strip()
        fallback_q = re.sub(
            r"[^\w\s\-àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
            " ",
            desc,
        )
        fallback_q = " ".join(fallback_q.split()[:8])
        if fallback_q:
            img, info = self._try_search_query(fallback_q)
            if img is not None:
                warn_msg = (
                    f"[FALLBACK_WARN] Scene {scene_id:02d} slot {slot_idx}: "
                    f"nguồn gốc lỗi ({'; '.join(fail_notes)}), đã fallback '{fallback_q}'"
                )
                print(warn_msg)
                self.fallback_warnings.append(warn_msg)
                return img, info, True

        err_msg = f"[SLOT_FAIL] Scene {scene_id:02d} slot {slot_idx}: {'; '.join(fail_notes)}"
        print(err_msg)
        self.failures.append(err_msg)
        return None, err_msg, True


def _load_fonts() -> Tuple[Any, Any, Any, Any]:
    try:
        return (
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28),
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 19),
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16),
            ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15),
        )
    except Exception:
        d = ImageFont.load_default()
        return d, d, d, d


def render_scene_contact_sheet(
    scene_id: int,
    title: str,
    news_source: str,
    voice_preset: str,
    records: List[Dict[str, Any]],
    out_path: Path,
) -> None:
    cols = 4
    rows = max(1, (len(records) + cols - 1) // cols)
    cell_w, cell_h, header_h = 460, 344, 88
    canvas = Image.new("RGB", (cols * cell_w + 40, rows * cell_h + header_h + 24), (10, 14, 24))
    draw = ImageDraw.Draw(canvas)
    f_hdr, f_sub, f_lbl, f_cap = _load_fonts()

    hdr_prefix = "INTRO" if scene_id == 0 else f"TIN #{scene_id:02d}"
    hdr_txt = f"QA CONTACT SHEET — {hdr_prefix}: {title[:78]}"
    draw.text((20, 14), hdr_txt, fill=(0, 229, 255), font=f_hdr)
    draw.text(
        (20, 50),
        f"Tong so anh: {len(records)} | Nguon: {news_source} | Voice: {voice_preset}",
        fill=(190, 205, 225),
        font=f_sub,
    )

    for idx, rec in enumerate(records):
        r, c = divmod(idx, cols)
        x0 = 20 + c * cell_w + 10
        y0 = header_h + r * cell_h + 8
        is_fb = rec.get("is_fallback", False)
        outline = (249, 115, 22) if is_fb else (0, 180, 216)
        draw.rectangle([x0 - 2, y0 - 2, x0 + 440, y0 + 324], outline=outline, width=2, fill=(18, 24, 38))
        img_path = IMG_DIR / rec["file_name"]
        if img_path.exists():
            with Image.open(img_path) as im:
                rgb = im.convert("RGB")
                rgb.thumbnail((432, 238), Image.Resampling.LANCZOS)
                canvas.paste(rgb, (x0 + (436 - rgb.width) // 2, y0 + (242 - rgb.height) // 2))

        tag = " [FALLBACK]" if is_fb else ""
        lbl_color = (249, 115, 22) if is_fb else (0, 229, 255)
        slot_tag = "T" if rec["type"] == "title" else f"S{rec['sentence_idx']}"
        draw.text((x0 + 8, y0 + 248), f"[{slot_tag}] {rec['file_name']} ({rec['dimensions']}){tag}", fill=lbl_color, font=f_lbl)
        draw.text((x0 + 8, y0 + 271), f"Nguon: {rec['credit']}", fill=(250, 204, 21), font=f_cap)
        desc = rec["description"]
        if len(desc) > 52:
            desc = desc[:49] + "..."
        draw.text((x0 + 8, y0 + 294), desc, fill=(220, 230, 245), font=f_cap)

    canvas.save(out_path, format="JPEG", quality=92)


def render_overview_sheet(overview_records: List[Dict[str, Any]], total_news: int, out_path: Path) -> None:
    cols = 4
    rows = max(1, (len(overview_records) + cols - 1) // cols)
    cell_w, cell_h, header_h = 460, 324, 84
    canvas = Image.new("RGB", (cols * cell_w + 40, rows * cell_h + header_h + 24), (10, 14, 24))
    draw = ImageDraw.Draw(canvas)
    f_hdr, f_sub, f_lbl, f_cap = _load_fonts()

    draw.text((20, 14), f"OVERVIEW QA CONTACT SHEET — NGAY {DAY_STR}", fill=(0, 229, 255), font=f_hdr)
    draw.text(
        (20, 50),
        f"Tong hop {len(overview_records)} anh dai dien tu Intro & {total_news} muc noi dung (VN & The Gioi)",
        fill=(190, 205, 225),
        font=f_sub,
    )

    for idx, rec in enumerate(overview_records):
        r, c = divmod(idx, cols)
        x0 = 20 + c * cell_w + 10
        y0 = header_h + r * cell_h + 8
        draw.rectangle([x0 - 2, y0 - 2, x0 + 440, y0 + 306], outline=(0, 180, 216), width=2, fill=(18, 24, 38))
        img_path = IMG_DIR / rec["file_name"]
        if img_path.exists():
            with Image.open(img_path) as im:
                rgb = im.convert("RGB")
                rgb.thumbnail((432, 228), Image.Resampling.LANCZOS)
                canvas.paste(rgb, (x0 + (436 - rgb.width) // 2, y0 + (232 - rgb.height) // 2))
        draw.text((x0 + 8, y0 + 238), f"Scene {rec['scene_id']:02d} | {rec['file_name']} ({rec['dimensions']})", fill=(0, 229, 255), font=f_lbl)
        draw.text((x0 + 8, y0 + 260), f"Nguon: {rec['credit']}", fill=(250, 204, 21), font=f_cap)
        desc = rec["description"]
        draw.text((x0 + 8, y0 + 281), desc[:52] + ("..." if len(desc) > 52 else ""), fill=(220, 230, 245), font=f_cap)

    canvas.save(out_path, format="JPEG", quality=90)


def split_sentences_for_log(text: str) -> List[str]:
    return [p.strip() for p in re.split(r"(?<=[.!?])\s+", (text or "").strip()) if p.strip()]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    QA_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "audio").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "audio-title").mkdir(parents=True, exist_ok=True)

    curator = ImageCurator22()
    all_specs = [data_22_11.INTRO_DATA] + list(data_22_11.NEWS_SPECS)

    search_queries: List[str] = []
    for sp in all_specs:
        for sl in sp["slots"]:
            for kind, val in sl["sources"]:
                if kind == "ddgs" and val not in search_queries:
                    search_queries.append(val)
    print(f"Đang nạp trước {len(search_queries)} truy vấn ảnh có lọc chủ thể...")
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = [pool.submit(curator._search_curated, q) for q in search_queries]
        for fut in as_completed(futs):
            fut.result()

    credits_map: Dict[str, str] = {}
    plan_records: List[Dict[str, Any]] = []
    overview_records: List[Dict[str, Any]] = []
    intro_entry: Optional[Dict[str, Any]] = None
    thethao_entries: List[Dict[str, Any]] = []
    script_log_lines: List[str] = []
    thethao_txt_lines: List[str] = []

    for spec in all_specs:
        sc_id = int(spec["id"])
        is_intro = sc_id == 0
        default_vp = "mixed" if is_intro else ("primary" if sc_id % 2 == 1 else "secondary")
        vp = spec.get("voice_preset") or default_vp
        voice_name, voice_gender = VOICE_INFO.get(vp, ("Minh Quân Pro", "male"))

        scene_records: List[Dict[str, Any]] = []
        image_files: List[str] = []

        for idx, sl in enumerate(spec["slots"], start=1):
            img, src_info, is_fb = curator.acquire_slot(sc_id, idx, sl)
            fn = f"Tin_{sc_id:02d}_{idx}.jpg"
            out_img = IMG_DIR / fn

            if img is not None:
                img.save(out_img, format="JPEG", quality=95, optimize=True)
                dims = f"{img.width}x{img.height} r={img.width / img.height:.2f}"
            else:
                dims = "MISSING"

            rec = {
                "scene_id": sc_id,
                "type": sl["type"],
                "index": int(sl["sentence_idx"]),
                "sentence_idx": int(sl["sentence_idx"]),
                "file_name": fn,
                "dimensions": dims,
                "credit": sl["credit"],
                "description": sl["desc"],
                "source_resolved": src_info,
                "is_fallback": is_fb,
            }
            scene_records.append(rec)
            plan_records.append({k: v for k, v in rec.items() if k not in ("source_resolved", "is_fallback")})
            credits_map[fn] = sl["credit"]
            image_files.append(str(out_img))

        for ov in scene_records[:2]:
            overview_records.append(ov)

        sheet_name = "contact_scene_00_intro.jpg" if is_intro else f"contact_scene_{sc_id:02d}.jpg"
        sheet_title = spec.get("group") or "MỞ ĐẦU BẢN TIN" if is_intro else spec["title"]
        render_scene_contact_sheet(
            sc_id,
            sheet_title,
            spec.get("news_source") or spec.get("source") or "",
            f"{vp} ({voice_name})",
            scene_records,
            QA_DIR / sheet_name,
        )

        item_entry: Dict[str, Any] = {
            "id": sc_id,
            "art_id": spec.get("art_id") or f"art_{sc_id:02d}",
            "group": spec["group"],
            "title": spec.get("title", ""),
            "summary": spec["summary"],
            "total_images": len(image_files),
            "hide_date_chip": bool(spec.get("hide_date_chip", False)),
            "source": spec["source"],
            "news_source": spec.get("news_source") or spec["source"].upper(),
            "credit": spec["credit"],
            "voice": voice_name,
            "voice_gender": voice_gender,
            "voice_preset": vp,
            "audio_path": str(OUT_DIR / "audio" / f"audio_{sc_id:02d}.wav"),
            "audio_title": "" if (is_intro or spec.get("hide_title")) else str(OUT_DIR / "audio-title" / f"audio_title_{sc_id:02d}.wav"),
            "image_path": image_files[0] if image_files else "",
        }
        if spec.get("hide_title"):
            item_entry["hide_title"] = True
        if spec.get("voice_segments"):
            item_entry["voice_segments"] = spec["voice_segments"]
        if spec.get("stat_badges"):
            item_entry["stat_badges"] = spec["stat_badges"]
        for k, fp in enumerate(image_files, start=1):
            item_entry[f"image_{k}"] = fp

        if is_intro:
            intro_entry = item_entry
            script_log_lines.append("=== INTRO (ID 00) | Song giọng Nữ (Ngọc Huyền) + Nam (Minh Quân Pro) ===")
            for s_idx, sent in enumerate(split_sentences_for_log(spec["summary"]), start=1):
                script_log_lines.append(f"Câu {s_idx}: {sent}")
                for r in scene_records:
                    if r["type"] == "sentence" and r["sentence_idx"] == s_idx:
                        script_log_lines.append(f"  -> {r['file_name']} ({r['dimensions']}) | {r['credit']} | {r['description']}")
            script_log_lines.append("")
        else:
            thethao_entries.append(item_entry)
            script_log_lines.append(f"=== TIN #{sc_id:02d} | {spec['group']} | {voice_name} ===")
            script_log_lines.append(f"Tiêu đề: {spec['title']}")
            for r in scene_records:
                if r["type"] == "title":
                    script_log_lines.append(f"  [Ảnh Tiêu đề] {r['file_name']} ({r['dimensions']}) | {r['credit']} | {r['description']}")
            for s_idx, sent in enumerate(split_sentences_for_log(spec["summary"]), start=1):
                script_log_lines.append(f"Câu {s_idx}: {sent}")
                for r in scene_records:
                    if r["type"] == "sentence" and r["sentence_idx"] == s_idx:
                        script_log_lines.append(f"  -> {r['file_name']} ({r['dimensions']}) | {r['credit']} | {r['description']}")
            script_log_lines.append("")

            thethao_txt_lines.extend([
                f"### TIN {sc_id:02d} [{spec['group']}]",
                f"Tiêu đề: {spec['title']}",
                f"Nội dung: {spec['summary']}",
                f"Nguồn: {spec['source']}",
                "",
            ])

    render_overview_sheet(overview_records, len(thethao_entries), QA_DIR / "contact_overview.jpg")

    if intro_entry is not None:
        (OUT_DIR / "intro_hook.json").write_text(
            json.dumps(intro_entry, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    (OUT_DIR / "thethao.json").write_text(
        json.dumps(thethao_entries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT_DIR / "image_credits.json").write_text(
        json.dumps(credits_map, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT_DIR / "image_plan.json").write_text(
        json.dumps({"total_slots": len(plan_records), "records": plan_records}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (OUT_DIR / "kich_ban_tung_cau.txt").write_text("\n".join(script_log_lines), encoding="utf-8")
    (OUT_DIR / "thethao.txt").write_text("\n".join(thethao_txt_lines), encoding="utf-8")

    # 3 Phương án Thumbnail 16:9 A/B Test (cùng trục tin nóng nhất, <= 21 ký tự/dòng)
    thumbs_plan = [
        {
            "suffix": "A",
            "badge": "BẢN TIN 22.11.2026",
            "kicker": "NGOẠI HẠNG ANH • ĐẠI HỘI 2026",
            "headline": "MAN CITY MẤT ĐIỂM<br>CHELSEA THẢM BẠI 1-4",
            "subtitle": "VAR hủy bàn Haaland • Arsenal hòa Newcastle • Khai mạc Đại hội",
            "footer_tag": "TIN NÓNG • 22.11",
            "image_file": "outputs/22.11.2026/images/Tin_10_1.jpg",
            "obj_pos": "center 22%",
            "filter": "contrast(1.06) saturate(1.1)",
        },
        {
            "suffix": "B",
            "badge": "CHẤN ĐỘNG ĐÊM QUA",
            "kicker": "VAR TRANH CÃI • MLS PLAY-OFF",
            "headline": "HỦY BÀN HAALAND!<br>MESSI THUA ĐẬM 0-3",
            "subtitle": "Chelsea thua Leeds 1-4 • Real Madrid thắng ngược dù Mbappé hỏng 11m",
            "footer_tag": "TIN NÓNG • 22.11",
            "image_file": "outputs/22.11.2026/images/Tin_11_1.jpg",
            "obj_pos": "center 22%",
            "filter": "contrast(1.06) saturate(1.08)",
        },
        {
            "suffix": "C",
            "badge": "TÂM ĐIỂM THỂ THAO",
            "kicker": "ĐẠI HỘI THỂ THAO TOÀN QUỐC",
            "headline": "ĐẠI HỘI TOÀN QUỐC<br>KHAI MẠC RỰC RỠ",
            "subtitle": "TP.HCM dẫn đầu 40 HCV • Nam Định giữ đỉnh bảng • UFC Qatar địa chấn",
            "footer_tag": "TIN NÓNG • 22.11",
            "image_file": "outputs/22.11.2026/images/Tin_01_1.jpg",
            "obj_pos": "center 22%",
            "filter": "contrast(1.06) saturate(1.1)",
        },
    ]
    (OUT_DIR / "thumbnails_plan.json").write_text(
        json.dumps(thumbs_plan, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("=" * 70)
    print(f"HOÀN TẤT PREPARE NGÀY {DAY_STR}: {len(thethao_entries)} mục + Intro | Tổng ảnh: {len(plan_records)}")
    print(f"Fallback warnings: {len(curator.fallback_warnings)} | Lỗi thiếu ảnh: {len(curator.failures)}")
    if curator.failures:
        for fl in curator.failures:
            print("  FAIL:", fl)
        sys.exit(1)


if __name__ == "__main__":
    main()
