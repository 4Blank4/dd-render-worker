#!/usr/bin/env python3
"""
m2 — TIMELINE BUILDER (Chế độ Chuẩn Hóa & Xác Thực Timeline cho Điểm Đọc)
========================================================================
Chuẩn hóa/validate timeline có sẵn:
- Tự gán engine, sfx, slot, span theo spec/schema.py
- Đổi 'steps' -> 'cards' nếu timeline dùng cấu trúc Thethao cũ
- Tự phát hiện type lạ và gợi ý fallback
- Tự động điền trigger_word thiếu và tính toán thời gian sơ bộ
- Hỗ trợ xuất JSON Schema cho timeline
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))

from diemdoc import paths
from diemdoc.jsonio import load_json, save_json
from diemdoc.log import banner, die, err, log, ok, step, warn
from diemdoc.timeline import cards_of, load_timeline, save_timeline, word_count

sys.path.insert(0, paths.SPEC)
import schema as S

# ==========================================================================
# Normalization & repair (không cần LLM)
# ==========================================================================

_ENGINE_FOR_TYPE = {n: s["engine"] for n, s in S.COMPONENTS.items()}
_SFX_FOR_TYPE = {n: s.get("sfx", "pop_card.mp3") for n, s in S.COMPONENTS.items()}
_SLOT_FOR_TYPE = {n: s.get("slot", "any") for n, s in S.COMPONENTS.items()}
_SPAN_FOR_SLOT = {"full": 12, "half": 6, "third": 4, "any": 6}


def normalize(tl: dict, fmt: str | None = None) -> tuple[dict, list[str]]:
    """
    Chuẩn hóa timeline: điền trường thiếu, chuyển 'steps'->'cards',
    gán engine/sfx/span theo registry. Trả về (tl, notes).
    """
    notes: list[str] = []
    tl.setdefault("schema_version", S.SCHEMA_VERSION)
    fmt = fmt or tl.get("format") or "short"
    tl["format"] = fmt
    tl.setdefault("channel_name", "Điểm Đọc")
    tl.setdefault("bgm", "bgm_editorial.mp3")
    tl.setdefault("bgm_volume", 0.08)
    tl.setdefault("enable_sfx", True)
    tl.setdefault("karaoke_enabled", True)
    tl.setdefault("voice_config", {"voice": "Minh Quân Pro", "speed": 1.20, "pitch": 0.85})
    tl.setdefault("template", "short_cinematic.html" if fmt == "short" else "long_cinematic.html")
    tl.setdefault("brand", "cinematic-dark")

    out_fn = tl.get("output_filename", "")
    if not out_fn or not out_fn.endswith(".mp4"):
        base = re.sub(r"[^A-Za-z0-9]+", "-", re.sub(r"\.[a-zA-Z0-9]+$", "", out_fn or tl.get("topic") or tl.get("project_name") or "video")).strip("-")
        tl["output_filename"] = f"{base or 'video'}.mp4"
        notes.append(f"Chuẩn hóa output_filename: {tl['output_filename']}")

    for si, sc in enumerate(tl.get("scenes", [])):
        sc.setdefault("scene_id", si + 1)
        if "cards" not in sc and "steps" in sc:
            sc["cards"] = sc.pop("steps")
            notes.append(f"Scene {sc['scene_id']}: đổi 'steps' -> 'cards' (chuẩn hóa).")
        sc.setdefault("cards", [])
        sc.setdefault("transition", "wipe" if si > 0 else "none")
        sc.setdefault("layout", "grid")

        script_txt = sc.get("script_text", "")

        seen_types: list[str] = []
        for ci, c in enumerate(sc["cards"]):
            c.setdefault("id", f"s{sc['scene_id']}_c{ci + 1}")
            ctype = c.get("type")
            if ctype not in S.COMPONENTS:
                # thử đoán từ tên gần đúng
                guess = _fuzzy_type(ctype)
                if guess:
                    notes.append(f"Card '{c['id']}': type '{ctype}' không có → đổi thành '{guess}'.")
                    c["type"] = ctype = guess
                else:
                    notes.append(f"Card '{c['id']}': type '{ctype}' KHÔNG TỒN TẠI → fallback 'fact-list'.")
                    c["type"] = ctype = "fact-list"

            # Parse các trường JSON bị LLM stringify
            for field in ["items", "data", "cards", "values", "pillars", "rows", "parts", "bars", "points", "heroes", "lines"]:
                if isinstance(c.get(field), str):
                    try:
                        c[field] = json.loads(c[field])
                        notes.append(f"Card '{c['id']}': tự động parse chuỗi JSON sang cấu trúc dữ liệu cho trường '{field}'.")
                    except Exception:
                        pass

            # Chuẩn hóa trường dữ liệu bắt buộc cho từng component type
            if ctype == "kinetic-statement":
                if not isinstance(c.get("lines"), list) or not c.get("lines"):
                    val = c.get("title") or c.get("text") or c.get("statement") or c.get("emphasis") or "ĐIỂM ĐỌC"
                    c["lines"] = [val] if isinstance(val, str) else list(val)
                    notes.append(f"Card '{c['id']}': tự động điền trường 'lines' cho kinetic-statement.")
            elif ctype == "stat-bento-trio":
                items = c.get("items")
                if not isinstance(items, list):
                    items = []
                while len(items) < 3:
                    items.append({"value": str(len(items) + 1), "title": f"Thông số {len(items) + 1}", "sub": ""})
                c["items"] = items[:3]
            elif ctype == "three-pillars":
                p = c.get("pillars")
                if not isinstance(p, list):
                    p = []
                while len(p) < 3:
                    p.append({"icon": "star", "title": f"Trọng tâm {len(p) + 1}", "sub": ""})
                c["pillars"] = p[:3]
            elif ctype == "fact-list":
                if not isinstance(c.get("items"), list) or not c.get("items"):
                    val = c.get("text") or c.get("lines") or [script_txt[:50]]
                    c["items"] = val if isinstance(val, list) else [str(val)]
            elif ctype == "quote-card":
                if not c.get("quote") and not c.get("text"):
                    c["quote"] = c.get("content") or c.get("quote_text") or "Trích dẫn tin tức."
            elif ctype == "photo-card":
                if not c.get("image") and c.get("src"):
                    c["image"] = c.pop("src")
                if not c.get("image"):
                    c["image"] = "images_ready/art_01_cover.jpg"
                if not c.get("credit"):
                    c["credit"] = "Điểm Đọc / Tổng hợp"
            elif ctype in ("stat-callout", "giant-number-spotlight"):
                if not c.get("value") and c.get("number"):
                    c["value"] = str(c["number"])
                elif not c.get("value"):
                    c["value"] = "100"
            elif ctype == "bar-chart":
                if not isinstance(c.get("bars"), list) or not c.get("bars"):
                    c["bars"] = c.get("items") or [{"label": "A", "value": 10}, {"label": "B", "value": 20}]
            elif ctype == "line-chart":
                if not isinstance(c.get("points"), list) or not c.get("points"):
                    c["points"] = [{"x": 1, "y": 10}, {"x": 2, "y": 20}]
            elif ctype == "lineup-grid":
                if not isinstance(c.get("heroes"), list) or not c.get("heroes"):
                    c["heroes"] = c.get("items") or [{"name": "Cầu thủ 1", "number": "10", "role": "Tiền đạo"}]

            c.setdefault("engine", _ENGINE_FOR_TYPE.get(ctype, "html"))
            if not c.get("sfx"):
                c["sfx"] = _SFX_FOR_TYPE.get(ctype, "pop_card.mp3")
            if "span" not in c:
                c["span"] = _SPAN_FOR_SLOT.get(_SLOT_FOR_TYPE.get(ctype, "any"), 6)
            if not c.get("role"):
                c["role"] = _infer_role(ctype, ci, len(sc["cards"]))
            if "trigger_word" not in c and "trigger_phrase" not in c and not c.get("lock_timing"):
                tw = _pick_trigger(c, script_txt)
                if tw:
                    c["trigger_word"] = tw
            else:
                scene_words = {S._norm(w) for w in script_txt.split()}
                tw = c.get("trigger_word")
                if tw and not c.get("lock_timing") and scene_words:
                    tokens = [S._norm(t) for t in str(tw).split() if S._norm(t)]
                    if tokens and not all(t in scene_words for t in tokens):
                        matching_tokens = [t for t in str(tw).split() if S._norm(t) in scene_words]
                        if matching_tokens:
                            c["trigger_word"] = " ".join(matching_tokens)
                            notes.append(f"Card '{c['id']}': sửa trigger_word '{tw}' -> '{c['trigger_word']}' để khớp script_text.")
                        else:
                            new_tw = _pick_trigger(c, script_txt)
                            if new_tw:
                                c["trigger_word"] = new_tw
                                notes.append(f"Card '{c['id']}': trigger_word '{tw}' không khớp -> đổi thành '{new_tw}'.")
                            else:
                                c["lock_timing"] = True
                                c.pop("trigger_word", None)
                                notes.append(f"Card '{c['id']}': trigger_word '{tw}' không khớp -> đặt lock_timing=true.")
            seen_types.append(ctype)

            if len(seen_types) >= 2 and seen_types[-1] == seen_types[-2]:
                notes.append(
                    f"Card '{c['id']}': hai card liên tiếp cùng type '{ctype}' → kém đa dạng thị giác."
                )

        # Sắp xếp các card theo thứ tự xuất hiện của trigger_word trong script_text
        if script_txt and len(sc["cards"]) > 1:
            def _card_order_key(card):
                tw = card.get("trigger_word") or card.get("trigger_phrase")
                if tw and tw in script_txt:
                    return script_txt.index(tw)
                return 99999
            sc["cards"].sort(key=_card_order_key)

    _ensure_scene_times(tl)
    return tl, notes


def _ensure_scene_times(tl: dict) -> None:
    """
    Đảm bảo timeline LUÔN render được, kể cả trước khi chạy TTS.
    """
    scenes = tl.get("scenes", [])
    if not scenes:
        return

    starts = [float(s.get("_start_time", s.get("start_time", 0)) or 0) for s in scenes]
    if len(set(starts)) > 1 or (starts and starts[0] > 0):
        return

    cursor = 0.0
    for sc in scenes:
        words = len((sc.get("script_text") or "").split())
        dur = max(3.0, round(words / 2.5, 2))
        sc["_start_time"] = sc["start_time"] = round(cursor, 2)
        sc["_duration"] = sc["duration"] = dur

        cards = cards_of(sc)
        n = len(cards)
        for i, c in enumerate(cards):
            if c.get("lock_timing") and "local_delay" in c:
                d = float(c["local_delay"])
            elif "local_delay" in c and c.get("trigger_word") is None:
                d = float(c["local_delay"])
            else:
                d = round(0.15 + (i * (dur * 0.72) / max(1, n)), 2)
            c["local_delay"] = d
            c["reveal_time"] = round(cursor + d, 2)
            c["_reveal_time"] = c["reveal_time"]
        cursor += dur

    tl["total_duration"] = round(cursor, 2)


_ALIASES_TYPE = {
    "hero-number": "giant-number-spotlight",
    "number-takeover": "giant-number-spotlight",
    "big-number-hero": "giant-number-spotlight",
    "stat-callout-card": "stat-callout",
    "digit-tiles": "grid-matrix",
    "trio": "stat-bento-trio",
    "eight-lineup-grid": "lineup-grid",
    "text-card": "fact-list",
    "photo-hero": "photo-card",
    "quote": "quote-card",
}


def _fuzzy_type(name: str | None) -> str | None:
    if not name:
        return None
    if name in _ALIASES_TYPE:
        return _ALIASES_TYPE[name]
    n = re.sub(r"[^a-z0-9]", "", str(name).lower())
    for cand in S.COMPONENTS:
        if re.sub(r"[^a-z0-9]", "", cand) == n:
            return cand
    for cand in S.COMPONENTS:
        if n and (n in re.sub(r"[^a-z0-9]", "", cand) or re.sub(r"[^a-z0-9]", "", cand) in n):
            return cand
    return None


def _infer_role(ctype: str, idx: int, total: int) -> str:
    if idx == 0:
        return "hook"
    if idx == total - 1:
        return "payoff"
    return "evidence"


def _pick_trigger(card: dict, script: str) -> str:
    """Chọn trigger_word: ưu tiên số trong dữ liệu card, rồi danh từ riêng trong script."""
    blob = json.dumps(card, ensure_ascii=False)
    for num in re.findall(r"\b\d[\d,\.]*\b", blob):
        for form in {num, num.replace(",", ""), num.rstrip(".")}:
            if form and re.search(rf"\b{re.escape(form)}\b", script):
                return form
    words = [w.strip(".,!?;:\"'()") for w in script.split()]
    cands = [w for w in words if len(w) > 5 and w[0:1].isupper()]
    if cands:
        return cands[0]
    long_words = sorted({w for w in words if len(w) > 6}, key=len, reverse=True)
    return long_words[0] if long_words else ""


# ==========================================================================
# CLI
# ==========================================================================

def main() -> None:
    ap = argparse.ArgumentParser(description="m2 — Timeline Normalizer cho Điểm Đọc")
    ap.add_argument("project", nargs="?", default="", help="Tên project, ví dụ 'project_demo'")
    ap.add_argument("--normalize", action="store_true", help="Chuẩn hóa timeline có sẵn (không cần LLM)")
    ap.add_argument("--format", choices=list(S.FORMATS.keys()), default=None)
    ap.add_argument("--json-schema", action="store_true", help="In JSON Schema rồi thoát")
    args = ap.parse_args()

    if args.json_schema:
        print(json.dumps(S.to_json_schema(), indent=2, ensure_ascii=False))
        return

    if not args.project:
        ap.print_help()
        return

    banner("M2 — TIMELINE BUILDER", "Điểm Đọc")
    pdir = paths.project_dir(args.project)

    step("Chuẩn hóa timeline có sẵn")
    tl = load_timeline(pdir)
    tl, notes = normalize(tl, args.format)
    for n in notes:
        log(n, tag="m2")
    errs, warns = S.validate_timeline(tl)
    for w in warns:
        if not w.startswith("__info__"):
            warn(w)
    if errs:
        err("Vẫn còn lỗi:")
        for e in errs[:20]:
            err(f"  - {e}")
        die("Chuẩn hóa xong nhưng timeline chưa hợp lệ.")
    save_timeline(pdir, tl)
    ok(f"Đã chuẩn hóa & lưu: {paths.rel_to_root(os.path.join(pdir, 'video_timeline.json'))}")


if __name__ == "__main__":
    main()