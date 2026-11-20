"""
Sync — căn chỉnh thời gian từng từ & neo card vào lời thoại.
============================================================
Giữ nguyên hai ý tưởng tốt nhất của hệ thống cũ:
  1. GROUND-TRUTH ALIGNMENT: không tin Whisper tuyệt đối. Lấy audio_sync.json
     (do TTS xuất, biết chắc đoạn nào chứa chữ gì) làm chuẩn, rồi nội suy
     vị trí token thật vào trong khoảng [start, end] của segment.
     → số liệu ("6174", "27.8%") không bao giờ bị Whisper nghe sai.
  2. SEMANTIC ANCHORING: card neo vào trigger_word, không neo vào giây.
  3. FALLBACK 3 TẦNG: trigger_word → local_delay → chia đều.
"""

from __future__ import annotations

import re
import unicodedata

from .log import log, warn
from .timeline import cards_of, scene_duration, scene_start, set_card_timing


# --------------------------------------------------------------------------
# Chuẩn hóa từ
# --------------------------------------------------------------------------

def normalize_word(word: str) -> str:
    if not word:
        return ""
    cleaned = re.sub(r"^[^\w\d]+|[^\w\d]+$", "", str(word).strip(), flags=re.UNICODE)
    return unicodedata.normalize("NFC", cleaned.lower())


def _tokens(text: str) -> list[str]:
    return [t for t in (normalize_word(w) for w in str(text).split()) if t]


# --------------------------------------------------------------------------
# Karaoke chunks — gộp từ thành cụm 4 từ để phụ đề không nhảy
# --------------------------------------------------------------------------

def group_karaoke_chunks(words_list: list[dict], max_words: int = 4,
                         max_chars: int = 30, pause_split: float = 0.35) -> list[dict]:
    chunks: list[dict] = []
    cur: list[dict] = []
    cur_chars = 0

    for w in words_list:
        wt = (w.get("word") or "").strip()
        if not wt:
            continue

        long_pause = bool(cur) and (w["start"] - cur[-1]["end"]) >= pause_split
        ended_punct = bool(cur) and cur[-1]["word"].strip().endswith((".", "!", "?", ":", ";", ","))

        if cur and (len(cur) >= max_words
                    or (cur_chars + len(wt) > max_chars and len(cur) >= 2)
                    or long_pause
                    or (ended_punct and len(cur) >= 3)):
            chunks.append(_mk_chunk(chunks, cur))
            cur, cur_chars = [], 0

        cur.append(w)
        cur_chars += len(wt) + 1

    if cur:
        chunks.append(_mk_chunk(chunks, cur))
    return chunks


def _mk_chunk(chunks: list[dict], items: list[dict]) -> dict:
    return {
        "chunk_index": len(chunks),
        "text": " ".join(i["word"] for i in items),
        "start": round(items[0]["start"], 3),
        "end": round(items[-1]["end"], 3),
        "words": items,
    }


# --------------------------------------------------------------------------
# Ground-truth alignment
# --------------------------------------------------------------------------

def align_words_to_ground_truth(raw_words: list[dict], sync_segments: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    raw_words      : từ Whisper nghe được, kèm timestamp thật
    sync_segments  : [{index, text, start, end}] do TTS xuất — CHÍNH XÁC về mặt chữ

    Trả về (all_words, segments_out) — mỗi token ground-truth có timestamp nội suy.
    """
    all_words: list[dict] = []
    segments_out: list[dict] = []

    for seg in sync_segments:
        s_start = float(seg["start"])
        s_end = float(seg["end"])
        gt_tokens = [t for t in str(seg.get("text", "")).split() if t.strip()]
        if not gt_tokens:
            continue

        seg_w = [w for w in raw_words if w["start"] >= s_start - 0.15 and w["end"] <= s_end + 0.25]
        n_gt, n_sw = len(gt_tokens), len(seg_w)
        aligned: list[dict] = []

        for i, tok in enumerate(gt_tokens):
            if n_sw >= 2:
                # nội suy vị trí token i trong dải từ Whisper
                idx_f = i * (n_sw - 1) / max(1, n_gt - 1)
                lo = int(idx_f)
                hi = min(n_sw - 1, lo + 1)
                frac = idx_f - lo
                w_start = seg_w[lo]["start"] * (1 - frac) + seg_w[hi]["start"] * frac
                w_end = seg_w[lo]["end"] * (1 - frac) + seg_w[hi]["end"] * frac
                if w_end <= w_start:
                    w_end = w_start + 0.12
                prob = seg_w[lo].get("probability", 1.0)
            else:
                dur = (s_end - s_start) / max(1, n_gt)
                w_start = s_start + i * dur
                w_end = w_start + dur * 0.92
                prob = 0.99

            w_start = max(s_start, min(w_start, s_end - 0.04))
            w_end = max(w_start + 0.04, min(w_end, s_end))
            item = {"word": tok, "start": round(w_start, 3), "end": round(w_end, 3),
                    "probability": round(float(prob), 3)}
            aligned.append(item)
            all_words.append(item)

        segments_out.append({
            "id": seg.get("index", len(segments_out)),
            "text": seg.get("text", ""),
            "start": round(s_start, 3),
            "end": round(s_end, 3),
            "words": aligned,
        })

    return all_words, segments_out


# --------------------------------------------------------------------------
# Semantic anchoring
# --------------------------------------------------------------------------

def find_phrase_time(words: list[dict], phrase: str) -> float | None:
    """Tìm thời điểm bắt đầu của cụm từ trong danh sách word-timestamps."""
    toks = _tokens(phrase)
    if not toks or not words:
        return None
    nw = [normalize_word(w.get("word", "")) for w in words]
    n = len(toks)
    for i in range(len(nw) - n + 1):
        if nw[i:i + n] == toks:
            return float(words[i]["start"])
    return None


def resolve_cue_points(tl: dict, words: list[dict], segments: list[dict] | None = None) -> dict:
    """
    Ghi _reveal_time cho mọi card, dùng 3 tầng fallback:
      1. trigger_word khớp trong scene  → neo chính xác (ưu tiên)
      2. local_delay có sẵn             → tôn trọng
      3. chia đều theo tỉ lệ            → cứu cánh
    Cũng ghi subtitles (karaoke) vào timeline.
    """
    if segments and not tl.get("subtitles"):
        tl["subtitles"] = [
            {"start": round(float(s.get("start", 0)), 2),
             "end": round(float(s.get("end", 0)), 2),
             "text": (s.get("text") or "").strip()}
            for s in segments if (s.get("text") or "").strip()
        ]

    stats = {"anchored": 0, "delayed": 0, "auto": 0, "locked": 0}

    for scene in tl.get("scenes", []):
        sc_start = scene_start(scene)
        sc_dur = scene_duration(scene)
        sc_end = sc_start + sc_dur

        scene_words = [w for w in words if (sc_start - 0.15) <= w["start"] <= (sc_end + 0.15)]
        cards = cards_of(scene)
        n = len(cards)

        for idx, card in enumerate(cards):
            if card.get("lock_timing") is True and "local_delay" in card:
                set_card_timing(card, sc_start + float(card["local_delay"]))
                stats["locked"] += 1
                continue

            trigger = card.get("trigger_phrase") or card.get("trigger_word") or ""
            matched = find_phrase_time(scene_words, trigger) if trigger else None

            if matched is not None:
                set_card_timing(card, matched, local_delay=max(0.05, matched - sc_start))
                stats["anchored"] += 1
            elif "local_delay" in card:
                d = float(card["local_delay"])
                set_card_timing(card, sc_start + d, local_delay=d)
                stats["delayed"] += 1
            else:
                d = round(0.12 + (idx * (sc_dur * 0.72) / max(1, n)), 3)
                set_card_timing(card, sc_start + d, local_delay=d)
                stats["auto"] += 1

    tl["sync"] = stats
    log(f"Neo thời gian: {stats['anchored']} chính xác / {stats['delayed']} theo delay / "
        f"{stats['auto']} chia đều / {stats['locked']} khoá", tag="sync")
    if stats["auto"]:
        warn(f"{stats['auto']} card không khớp trigger_word — nên thêm/sửa trigger_word để chính xác hơn.")
    return tl


# --------------------------------------------------------------------------
# Fallback: sync bằng âm tiết (không cần Whisper — chạy < 0.1s)
# --------------------------------------------------------------------------

_DIGIT_WEIGHT = {
    "thousand": 2.2, "million": 2.4, "billion": 2.4, "trillion": 2.6,
    "hundred": 1.8, "percent": 1.6, "point": 1.3, "zero": 1.0,
}


def syllabic_estimate(segment_text: str, start: float, end: float) -> list[dict]:
    """
    Ước lượng thời gian từng từ bằng trọng số âm tiết + trọng số chữ số.
    Tiếng Anh đọc số nhiều âm tiết hơn ký tự viết ("1993" = "nine-teen-nine-three").
    Dùng làm fallback nhanh khi không có Whisper.
    """
    toks = str(segment_text).split()
    if not toks:
        return []

    weights = []
    for t in toks:
        core = normalize_word(t)
        w = 1.0
        digits = sum(c.isdigit() for c in t)
        if digits:
            w += digits * 0.42                       # mỗi chữ số ~0.42 âm tiết thêm
        w += sum(0.5 for ch in "-/." if ch in t)
        for k, v in _DIGIT_WEIGHT.items():
            if k in core:
                w += v * 0.3
        weights.append(max(0.35, w))

    total = sum(weights) or 1.0
    span = max(0.01, end - start)
    out, cursor = [], start
    for t, w in zip(toks, weights):
        dur = span * (w / total)
        out.append({"word": t, "start": round(cursor, 3),
                    "end": round(cursor + dur * 0.94, 3), "probability": 0.7})
        cursor += dur
    return out


def syllabic_sync(sync_segments: list[dict]) -> tuple[list[dict], list[dict]]:
    """Sync toàn bộ bằng phương pháp âm tiết. Trả về (words, segments)."""
    all_words, segments_out = [], []
    for seg in sync_segments:
        ws = syllabic_estimate(seg.get("text", ""), float(seg["start"]), float(seg["end"]))
        all_words.extend(ws)
        segments_out.append({
            "id": seg.get("index", len(segments_out)),
            "text": seg.get("text", ""),
            "start": round(float(seg["start"]), 3),
            "end": round(float(seg["end"]), 3),
            "words": ws,
        })
    return all_words, segments_out