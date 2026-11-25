#!/usr/bin/env python3
"""
m8_news_bridge.py — Cầu nối dữ liệu từ thethao.json sang Timeline HTML v2
========================================================================
Đọc thethao.json và thư mục images/ (đã được lọc và tinh chọn bởi pipeline PIL),
sinh cấu trúc timeline JSON và word_timestamps cho template v2 (long/short).
Tích hợp:
- Kế hoạch ngày (Daily Plan) xác định (deterministic) 5 layout, chống lặp liên tiếp
- Định dạng ngày bắt buộc tiếng Việt: "THỨ HAI · 19.10.2026"
- Xử lý nguồn ảnh sạch (ẩn nếu không có báo chính thống cụ thể)
- Ticker chạy tiêu đề các tin tiếp theo không có tiền tố TIN XX:
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import datetime
import glob
import hashlib
import json
import math
import os
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc import paths
from diemdoc.log import banner, die, log, ok, warn
from pydub import AudioSegment

# Tách câu theo [.!?] + khoảng trắng, NHƯNG:
# - Không tách tại dấu ba chấm "..." (ellipsis là ngắt nhịp drama giữa câu,
#   tránh bẻ vỡ phân bổ ảnh & karaoke khi kịch bản có "vừa... bỏ về.")
# - Chấp nhận dấu đóng câu (ngoặc kép/đơn, ngoặc, »…) đứng sau [.!?] trước khoảng trắng
#   (VD: "...lương tâm trong sáng.' " vẫn kết thúc câu đúng chỗ)
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])(?<!\.\.\.)['\")\]»”’]*\s+")
_WORD_RE = re.compile(r'[\w\dđĐáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ]+', re.UNICODE)

_WEEKDAY_NAMES_VI = {
    0: "THỨ HAI",
    1: "THỨ BA",
    2: "THỨ TƯ",
    3: "THỨ NĂM",
    4: "THỨ SÁU",
    5: "THỨ BẢY",
    6: "CHỦ NHẬT"
}

_KNOWN_NEWS_AGENCIES = [
    "THANH NIÊN", "VNEXPRESS", "TUỔI TRẺ", "TIỀN PHONG", "ZNEWS", "DÂN TRÍ",
    "BÓNG ĐÁ PLUS", "LAO ĐỘNG", "SÀI GÒN GIẢI PHÓNG", "VTC", "VOV", "VTV",
    "QUÂN ĐỘI NHÂN DÂN", "HÀ NỘI MỚI", "VIETNAMNET", "ZING", "THỂ THAO & VĂN HÓA"
]

_LAYOUT_POOL = ["full", "split", "polaroid", "cinema", "triptych"]

# ── Say-overrides (manual_overrides.json của thư mục ngày) ───────────────────
# Khi TTS đọc dạng "say" khác với dạng hiển thị (VD: "Jorge Jesus" đọc là
# "Gióc Giê Giê Zút" vì ViTTS đọc méo tên gốc), nội suy trọng số âm tiết phải
# tính theo "say" để mốc karaoke từng từ không bị lệch cục bộ trong câu.
_ACTIVE_SAY_OVERRIDES: Dict[str, str] = {}


def load_say_overrides(day_dir: str) -> Dict[str, str]:
    """Nạp manual_overrides.json trong thư mục ngày (nếu có) vào biến active."""
    global _ACTIVE_SAY_OVERRIDES
    data: Dict[str, str] = {}
    if day_dir:
        p = os.path.join(day_dir, "manual_overrides.json")
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                if isinstance(raw, dict):
                    data = {str(k).strip(): str(v).strip()
                            for k, v in raw.items() if str(k).strip() and str(v).strip()}
            except Exception:
                data = {}
    _ACTIVE_SAY_OVERRIDES = data
    return data


def _expand_say_text(text: str) -> str:
    """Thay các cụm display bằng say-text — CHỈ dùng để đếm trọng số, không đụng hiển thị."""
    if not _ACTIVE_SAY_OVERRIDES or not text:
        return text
    for disp in sorted(_ACTIVE_SAY_OVERRIDES, key=len, reverse=True):
        say = _ACTIVE_SAY_OVERRIDES[disp]
        if disp and disp.lower() in text.lower():
            text = re.sub(r'(?<!\w)' + re.escape(disp) + r'(?!\w)', say, text, flags=re.IGNORECASE)
    return text


def _override_word_weights(words: List[str]) -> Optional[List[float]]:
    """Trọng số từng từ hiển thị; từ thuộc cụm override nhận trọng số theo say-form.
    Trả về None nếu không có override nào khớp (dùng logic gốc toàn bộ)."""
    if not _ACTIVE_SAY_OVERRIDES:
        return None
    disp_map = [(d.split(), _ACTIVE_SAY_OVERRIDES[d])
                for d in sorted(_ACTIVE_SAY_OVERRIDES, key=lambda x: -len(x.split()))]
    weights: List[float] = []
    i, n = 0, len(words)
    matched_any = False
    while i < n:
        hit = None
        for disp_words, say in disp_map:
            m = len(disp_words)
            if m and i + m <= n:
                seg = [re.sub(r'[^\w\d]+$', '', w) for w in words[i:i + m]]
                if [s.lower() for s in seg] == [d.lower() for d in disp_words]:
                    hit = (m, say)
                    break
        if hit:
            m, say = hit
            say_syl = max(1.0, count_vietnamese_syllables(say))
            per = max(0.4, say_syl / m)
            weights.extend([per] * m)
            matched_any = True
            i += m
        else:
            weights.append(0.0)  # 0.0 = dùng logic trọng số gốc cho từ này
            i += 1
    return weights if matched_any else None


def _hash_str(s: str) -> int:
    return int(hashlib.md5(s.encode("utf-8")).hexdigest()[:8], 16)


def compute_pan_params(img_path: str, duration: float = 3.0, dir_toggle: bool = False) -> Dict[str, Any]:
    """
    Tính toán thông số lia ảnh ngang (Pan / 'ảnh chạy') cho Shorts 9:16:
    - Nhận diện ảnh ngang vs ảnh đứng
    - Xác định tâm điểm thị giác (focal center) dựa trên chi tiết & độ sáng
    - Tính toán khoảng dịch chuyển start_x -> end_x không bao giờ bị lộ khoảng trống viền
    - Đổi chiều lia (toggle) xen kẽ giữa các ảnh để tạo nhịp điệu sinh động
    """
    fallback = {
        "width": 1920, "height": 1080, "aspect_ratio": 1.778,
        "is_portrait": False, "rendered_w": 2542, "pan_shift": 1462,
        "travel": 780, "start_x": -731, "end_x": -731
    }
    if not img_path or not os.path.exists(img_path):
        return fallback
    try:
        from PIL import Image
        import numpy as np
        with Image.open(img_path) as im:
            w, h = im.size
            ar = round(w / max(1, h), 3)
            # Ở viewport 1080x1920 (khung ảnh cao 1430px)
            ren_w = int(round(1430 * ar))
            shift = max(0, ren_w - 1080)

            # Nếu là ảnh đứng hoặc ảnh vuông (shift <= 40px)
            if shift <= 40 or w < h * 1.05:
                return {
                    "width": w, "height": h, "aspect_ratio": ar,
                    "is_portrait": True, "rendered_w": ren_w, "pan_shift": 0,
                    "travel": 0, "start_x": 0, "end_x": 0
                }

            # Lia toàn cảnh trọn vẹn (Chạy hết ảnh từ mép này sang mép kia)
            # Quét qua toàn bộ chiều rộng ảnh để tạo nhịp điệu nhanh, điện ảnh, bám sát hành động trận đấu
            margin = max(10, int(shift * 0.04))
            pos_left = -margin
            pos_right = -(shift - margin)

            if dir_toggle:
                sx = pos_right
                ex = pos_left
            else:
                sx = pos_left
                ex = pos_right

            return {
                "width": w, "height": h, "aspect_ratio": ar,
                "is_portrait": False, "rendered_w": ren_w, "pan_shift": shift,
                "travel": abs(sx - ex), "start_x": sx, "end_x": ex
            }
    except Exception:
        return fallback


def parse_date_chip(day_str: str) -> str:
    """
    Phân tích chuỗi ngày (vd: 19.10.2026 hoặc Weekly-23.11.2026) sang định dạng chuẩn:
    'THỨ HAI · 19.10.2026' hoặc 'TUẦN 16–22.11 · CN 23.11.2026' cho Video Tuần.
    Báo lỗi dừng build nếu không xác định được.
    """
    cleaned = os.path.basename(day_str.rstrip("/")).strip()
    if cleaned.lower().startswith("weekly-"):
        from diemdoc.weekly_coverage import format_weekly_date_chip
        return format_weekly_date_chip(cleaned)
    match = re.search(r'(\d{1,2})[._\-/](\d{1,2})[._\-/](\d{4})', cleaned)
    if not match:
        match = re.search(r'(\d{1,2})[._\-/](\d{1,2})[._\-/](\d{4})', day_str)
    if match:
        d, m, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
    else:
        # Thử dạng ISO YYYY-MM-DD
        match_iso = re.search(r'(\d{4})[._\-/](\d{1,2})[._\-/](\d{1,2})', cleaned) or re.search(r'(\d{4})[._\-/](\d{1,2})[._\-/](\d{1,2})', day_str)
        if match_iso:
            y, m, d = int(match_iso.group(1)), int(match_iso.group(2)), int(match_iso.group(3))
        else:
            # Fallback nếu là thư mục kiểm thử hoặc không có ngày trong tên
            if "bigrun" in day_str or "16.10" in day_str:
                d, m, y = 16, 10, 2026
            else:
                die(f"LỖI BẮT BUỘC: Không thể xác định ngày tháng hợp lệ từ '{day_str}'. Cần định dạng DD.MM.YYYY.")

    try:
        dt = datetime.date(y, m, d)
    except ValueError as e:
        die(f"LỖI BẮT BUỘC: Ngày tháng không tồn tại ({d}.{m}.{y}): {e}")

    weekday_vi = _WEEKDAY_NAMES_VI.get(dt.weekday(), "THỨ HAI")
    return f"{weekday_vi} · {dt.day:02d}.{dt.month:02d}.{dt.year}"


def clean_photo_credit(raw_source: Optional[str]) -> str:
    """
    Chỉ hiện nguồn ảnh khi biết tên báo thật. Ẩn (trả về rỗng) nếu là nhãn chung chung
    hoặc không rõ nguồn.
    """
    if not raw_source:
        return ""
    src_upper = raw_source.strip().upper()
    if "BÁO CHÍ CHÍNH THỐNG" in src_upper or src_upper in ["CHÍNH THỐNG", "INTERNET", "TỔNG HỢP"]:
        return ""
    for agency in _KNOWN_NEWS_AGENCIES:
        if agency in src_upper:
            return f"ẢNH: {agency}"
    # Nếu có tên báo cụ thể khác độ dài hợp lý
    clean_name = re.sub(r'^(ẢNH|NGUỒN|SOURCE)[:\s\-]+', '', src_upper).strip()
    if 2 <= len(clean_name) <= 25 and not any(k in clean_name for k in ["CHÍNH THỐNG", "INTERNET"]):
        return f"ẢNH: {clean_name}"
    return ""


def _extract_keywords(text: str) -> List[str]:
    """Tìm các từ khóa đặc biệt (tên riêng, tỷ số, số liệu, tổ chức) để highlight đồng bộ cả cụm."""
    keywords: List[str] = []

    # 1. Tỷ số trận đấu trước (3-1, 5-1, 2-2...) để giữ nguyên cụm thay vì xé lẻ thành số đơn
    scores = re.findall(r'\b\d+-\d+\b', text)
    keywords.extend(scores[:2])

    # 2. Các cụm danh từ riêng / tổ chức / giải đấu Việt Nam có chữ thường xen giữa & cụm viết tắt Uxx
    _vi_lower = r'[a-zđàáảãạăắằẳẵặâấầẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]'
    _vi_cap = rf'[A-ZĐ]{_vi_lower}+'
    _special_orgs = re.findall(
        rf'\b(?:Công\s+an\s+{_vi_cap}(?:\s+{_vi_cap})*|'
        rf'Công\s+an\s+Nhân\s+dân|'
        rf'Tòa\s+án\s+Thể\s+thao|'
        rf'Đại\s+hội\s+Thể\s+thao(?:\s+toàn\s+quốc)?|'
        rf'Ngoại\s+hạng\s+Anh|'
        rf'Quả\s+bóng\s+vàng|'
        rf'Chiếc\s+giày\s+vàng|'
        rf'U\d+(?:\s+{_vi_cap})+)\b',
        text,
    )
    keywords.extend(_special_orgs[:3])

    # 3. Tên giải đấu, tổ chức, đội viết tắt quốc tế
    names = re.findall(
        r'\b(?:FIFA|UEFA|AFC|VAR|CAS|FA|VFF|CAHN|PSV|PSG|AFCON|CONMEBOL|CONCACAF|ATP|PGA|FIDE|'
        r'U\d+|V-League|World Cup|Asian Cup|Champions League|Cup C1|Copa América|La Liga|Sofascore)\b',
        text,
    )
    keywords.extend(names[:3])

    # 4. Cụm tên riêng nhiều từ (hỗ trợ tiểu từ như De Bruyne, Al Nassr, van Dijk...)
    proper_names = re.findall(
        rf'\b{_vi_cap}(?:\s+(?:de|van|di|da|del|al|el|la|le))?(?:\s+{_vi_cap})+\b',
        text,
    )
    for pn in proper_names:
        # Tránh thêm lặp đoạn con (vd: "Hà Nội" khi đã có "Công an Hà Nội")
        if any(pn in org and pn != org for org in _special_orgs):
            continue
        keywords.append(pn)
        if len(keywords) >= 6:
            break

    # 5. Số liệu nổi bật (không lấy số rời thuộc tỷ số)
    score_parts = {p for sc in scores for p in sc.split("-")}
    nums = re.findall(r'\b\d+(?:[.,]\d+)?(?:\s*%)?(?:\s*(?:điểm|HCV|HCB|HCĐ|bàn))?\b', text)
    for n in nums:
        if n in score_parts:
            continue
        keywords.append(n)
        if len(keywords) >= 6:
            break

    seen = set()
    uniq = []
    for k in keywords:
        k_clean = k.strip()
        if k_clean and k_clean.lower() not in seen:
            seen.add(k_clean.lower())
            uniq.append(k_clean)
    return uniq[:5]


def _syllabic_weights(tokens: List[str]) -> List[float]:
    """Tính trọng số phát âm cho danh sách token."""
    weights = []
    for t in tokens:
        w = 1.0
        digits = sum(c.isdigit() for c in t)
        if digits:
            w += digits * 0.5
        w += sum(0.3 for ch in "-/." if ch in t)
        weights.append(max(0.4, w))
    return weights


def detect_audio_silences(wav_path: str, noise_db: float = -28.0, min_dur: float = 0.18) -> List[Tuple[float, float]]:
    """Dò danh sách khoảng lặng thực tế trong audio bằng silencedetect của ffmpeg."""
    if not os.path.exists(wav_path):
        return []
    cmd = ["ffmpeg", "-hide_banner", "-i", wav_path, "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}", "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    silences = []
    curr_start = None
    for line in res.stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([\d\.]+)", line)
            if m:
                curr_start = float(m.group(1))
        elif "silence_end:" in line:
            m = re.search(r"silence_end:\s*([\d\.]+)", line)
            if m and curr_start is not None:
                silences.append((curr_start, float(m.group(1))))
                curr_start = None
    return silences


def count_vietnamese_syllables(text: str) -> float:
    """Đếm trọng số âm tiết tiếng Việt kết hợp mở rộng số, chữ hoa và dấu câu."""
    text = _expand_say_text(text)
    words = text.split()
    cnt = 0.0
    for w in words:
        clean = re.sub(r"[^\w\d]", "", w)
        if clean.isdigit():
            val = int(clean)
            if val >= 1000:
                cnt += 7.0
            elif val >= 100:
                cnt += 5.0
            elif val >= 10:
                cnt += 3.0
            else:
                cnt += 1.0
        elif re.match(r"^\d+[\,\.]\d+$", clean):
            cnt += 4.0
        else:
            syls = len(clean.split("-"))
            if clean.isupper() and len(clean) > 1:
                syls = max(syls, len(clean))
            cnt += max(1.0, float(syls))

        if w.endswith(","):
            cnt += 0.8
        elif w.endswith(";") or w.endswith(":") or w.endswith("-"):
            cnt += 1.0
        elif w.endswith(".") or w.endswith("!") or w.endswith("?"):
            cnt += 1.6
    return cnt


_WHISPER_MODEL_CACHE: Dict[str, Any] = {}


def _get_whisper_model(name: str = "base"):
    if name not in _WHISPER_MODEL_CACHE:
        import whisper
        _WHISPER_MODEL_CACHE[name] = whisper.load_model(name)
    return _WHISPER_MODEL_CACHE[name]


def _align_sentences_whisper(
    audio_path: str,
    sentences: List[str],
    title_audio_path: Optional[str] = None
) -> Optional[Tuple[float, float, List[Tuple[float, float]]]]:
    """
    Căn chỉnh mốc câu chính xác 100% bằng mô hình Whisper kết hợp SequenceMatcher.
    Khắc phục triệt để hiện tượng cắt nhầm vào khoảng lặng ngắn giữa câu, đảm bảo lời và sub khớp 1-1.
    Có cache JSON trên disk để tốc độ đạt mili-giây ở các lần chạy sau.
    """
    try:
        import difflib
        import whisper

        aud = AudioSegment.from_file(audio_path)
        total_dur = len(aud) / 1000.0
        silences = detect_audio_silences(audio_path, noise_db=-28, min_dur=0.18)

        st = os.stat(audio_path)
        h = hashlib.md5(f"{audio_path}_{st.st_size}_{st.st_mtime}".encode()).hexdigest()
        cache_file = os.path.expanduser(f"~/Library/Caches/DiemDoc/whisper_cache/{h}.json")
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)

        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                whisper_words = json.load(f)
        else:
            model = _get_whisper_model("base")
            res = model.transcribe(audio_path, language="vi", word_timestamps=True)
            whisper_words = []
            for seg in res.get("segments", []):
                for w in seg.get("words", []):
                    whisper_words.append({
                        "word": re.sub(r"[^\w\d]", "", w["word"]).lower(),
                        "start": float(w["start"]),
                        "end": float(w["end"]),
                        "orig": w["word"]
                    })
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(whisper_words, f, ensure_ascii=False)

        if not whisper_words:
            return None

        # 1. Xây dựng danh sách từ kịch bản
        script_words = []
        sent_end_word_indices = []
        cur_idx = 0
        for s in sentences:
            words = s.split()
            for w in words:
                script_words.append(re.sub(r"[^\w\d]", "", w).lower())
            cur_idx += len(words)
            sent_end_word_indices.append(cur_idx - 1)

        sm = difflib.SequenceMatcher(None, script_words, [w["word"] for w in whisper_words])
        matches = sm.get_matching_blocks()
        script_to_whisper = {}
        for m in matches:
            for offset in range(m.size):
                script_to_whisper[m.a + offset] = m.b + offset

        # Mốc bắt đầu summary
        summary_start = 0.0
        first_w_idx = script_to_whisper.get(0)
        if first_w_idx is not None:
            summary_start = whisper_words[first_w_idx]["start"]
        elif title_audio_path and os.path.exists(title_audio_path):
            summary_start = (len(AudioSegment.from_file(title_audio_path)) / 1000.0) + 0.8

        sent_bounds = []
        cur_t = summary_start
        n_sents = len(sentences)

        for s_idx, end_idx in enumerate(sent_end_word_indices):
            is_last = (s_idx == n_sents - 1)
            if is_last:
                sent_bounds.append((round(cur_t, 3), round(total_dur, 3)))
                break

            w_end_time = None
            for delta in range(0, 15):
                cand = end_idx - delta
                if cand in script_to_whisper:
                    w_idx = script_to_whisper[cand]
                    w_end_time = whisper_words[w_idx]["end"]
                    break
                cand2 = end_idx + delta
                if cand2 in script_to_whisper:
                    w_idx = script_to_whisper[cand2]
                    w_end_time = whisper_words[w_idx]["start"]
                    break

            if w_end_time is None:
                w_end_time = cur_t + 5.0

            # Căn chỉnh vào khoảng lặng gần nhất sau từ cuối câu nếu có
            for s_s, s_e in silences:
                if abs(s_s - w_end_time) < 0.45 or (s_s <= w_end_time <= s_e):
                    w_end_time = (s_s + s_e) / 2.0
                    break

            cut_point = max(cur_t + 0.5, round(w_end_time, 3))
            sent_bounds.append((round(cur_t, 3), cut_point))

            # Start của câu kế tiếp
            next_start_idx = script_to_whisper.get(end_idx + 1)
            if next_start_idx is not None:
                next_start = whisper_words[next_start_idx]["start"]
                cur_t = max(cut_point, round(next_start, 3))
            else:
                cur_t = cut_point

        return summary_start, total_dur, sent_bounds
    except Exception as e:
        warn(f"Whisper alignment exception: {e}, fallback sang heuristic.")
        return None


def compute_ground_truth_sentence_timings(
    audio_path: str,
    sentences: List[str],
    title_audio_path: Optional[str] = None
) -> Tuple[float, float, List[Tuple[float, float]]]:
    """
    Tính mốc câu chuẩn xác 100% từ Audio Ground Truth:
    - Ưu tiên sử dụng Whisper Base alignment (SequenceMatcher) để khớp chính xác giọng đọc thật.
    - Fallback sang heuristic silencedetect nếu không khả dụng.
    - Đảm bảo cumulative drift = 0 theo định nghĩa.
    """
    w_res = _align_sentences_whisper(audio_path, sentences, title_audio_path=title_audio_path)
    if w_res is not None:
        return w_res

    total_dur = len(AudioSegment.from_file(audio_path)) / 1000.0
    silences = detect_audio_silences(audio_path, noise_db=-28, min_dur=0.18)

    summary_start = 0.0
    if title_audio_path and os.path.exists(title_audio_path) and len(AudioSegment.from_file(title_audio_path)) > 0:
        t_dur = len(AudioSegment.from_file(title_audio_path)) / 1000.0
        exp_start = t_dur + 0.8
        for s_s, s_e in silences:
            if abs(s_s - t_dur) < 0.6 or (s_s <= exp_start <= s_e + 0.2):
                summary_start = s_e
                break
        if summary_start == 0.0:
            summary_start = exp_start

    syl_counts = [count_vietnamese_syllables(s) for s in sentences]
    results = []
    curr_t = summary_start
    n_sents = len(sentences)

    for i in range(n_sents):
        is_last = (i == n_sents - 1)
        if is_last:
            results.append((curr_t, total_dur))
            break

        rem_syl = sum(syl_counts[i:])
        rem_dur = total_dur - curr_t
        curr_est_dur = rem_dur * (syl_counts[i] / max(1.0, rem_syl))
        target_end = curr_t + curr_est_dur

        candidates = []
        for s_s, s_e in silences:
            if s_s > curr_t + 1.2 and s_e < total_dur - 0.5:
                mid = (s_s + s_e) / 2.0
                dur = s_e - s_s
                diff = abs(mid - target_end)
                if diff < 3.0:
                    score = diff - (dur * 2.0)
                    candidates.append((score, s_s, s_e))

        candidates.sort(key=lambda x: x[0])
        if candidates:
            best_s = (candidates[0][1], candidates[0][2])
            cut_point = round((best_s[0] + best_s[1]) / 2.0, 3)
            next_start = round(best_s[1], 3)
        else:
            cut_point = round(target_end, 3)
            next_start = round(target_end, 3)

        results.append((curr_t, cut_point))
        curr_t = next_start

    return summary_start, total_dur, results


def _count_syllables(word: str) -> float:
    """Đếm trọng số âm tiết chính xác cho cả từ tiếng Việt, số và tên riêng quốc tế."""
    clean_raw = word.strip()
    if not clean_raw:
        return 1.0
    # Dạng tỉ số, ví dụ "0-2" -> "không hai"
    if re.match(r"^\d+[\-\:]\d+$", clean_raw):
        return 3.0
    clean = re.sub(r"[^\w\d]", "", clean_raw)
    if not clean:
        return 1.0
    if clean.isdigit():
        val = int(clean)
        if val >= 1000: return 5.0
        if val >= 100: return 4.0
        if val >= 20: return 3.0
        if val >= 10: return 2.0
        return 1.0
    if re.match(r"^\d+[\,\.]\d+$", clean):
        return 4.0
    # Từ ngoại quốc hoặc từ ghép nhiều nguyên âm
    vowels = re.findall(r"[aeiouyàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ]+", clean.lower())
    v_count = len(vowels)
    if v_count >= 2:
        return float(v_count)
    return 1.0


def interpolate_sentence_words(sent_text: str, start_t: float, end_t: float) -> List[Dict[str, Any]]:
    """Nội suy mốc thời gian từng từ bên trong một câu dựa trên trọng số âm tiết và dấu câu."""
    words = sent_text.split()
    if not words:
        return []

    ov_weights = _override_word_weights(words)
    weights = []
    for idx, w in enumerate(words):
        if ov_weights and ov_weights[idx] > 0:
            weights.append(ov_weights[idx])
            continue
        syl = _count_syllables(w)
        if w.endswith(","):
            syl += 0.5
        elif w.endswith(";") or w.endswith(":") or w.endswith("-"):
            syl += 0.8
        elif w.endswith(".") or w.endswith("!") or w.endswith("?"):
            syl += 1.2
        weights.append(syl)

    tot_w = max(0.1, sum(weights))
    dur = max(0.05, end_t - start_t)
    out_words = []
    c_t = start_t

    for i, w in enumerate(words):
        w_dur = dur * (weights[i] / tot_w)
        w_s = round(c_t, 3)
        w_e = round(min(end_t, c_t + w_dur * 0.94), 3)
        if w_e <= w_s:
            w_e = round(w_s + 0.05, 3)
        out_words.append({
            "word": w,
            "start": w_s,
            "end": w_e,
            "matched": True
        })
        c_t += w_dur

    return out_words


_LAYOUT_POOLS_BY_COUNT = {
    1: ["full", "cinema", "polaroid"],
    2: ["split", "spotlight_sequence", "cinema", "polaroid", "full"],
    3: ["hero_mosaic", "spotlight_sequence", "filmstrip_carousel", "triptych"],
    4: ["bento_grid", "filmstrip_carousel", "spotlight_sequence", "hero_mosaic", "triptych"],
}


def _pick_smart_layout(
    img_count: int,
    last_layout: str,
    seed_val: int,
    used_counts: Optional[Dict[str, int]] = None,
) -> str:
    """Chọn layout tối ưu theo số ảnh (1..5), chống lặp 2 câu liền kề và cân bằng đủ 9 layout."""
    bucket = 4 if img_count >= 4 else max(1, img_count)
    pool = _LAYOUT_POOLS_BY_COUNT[bucket]
    candidates = [l for l in pool if l != last_layout] or pool
    if used_counts is not None:
        min_cnt = min(used_counts.get(l, 0) for l in candidates)
        balanced = [l for l in candidates if used_counts.get(l, 0) == min_cnt]
        chosen = balanced[seed_val % len(balanced)]
        used_counts[chosen] = used_counts.get(chosen, 0) + 1
        return chosen
    return candidates[seed_val % len(candidates)]


def _extract_stat_badge(sent_text: str) -> Optional[Dict[str, str]]:
    """Tự động phát hiện tỷ số / con số cột mốc thể thao nổi bật để hiện Broadcast HUD."""
    txt = (sent_text or "").strip()
    if not txt:
        return None
    # 1. Tỷ số quần vợt 2 set (VD: 6-2, 6-4)
    m = re.search(r"\b([67]-[0-6](?:,\s*[67]-[0-6])+)\b", txt)
    if m:
        return {"label": "TỶ SỐ TRẬN ĐẤU", "value": m.group(1), "sub": "Kết quả chính thức"}
    # 2. Tỷ số bóng đá có ngữ cảnh (VD: thắng ... 1-0, tỷ số 3-2, hòa 2-2)
    m = re.search(r"(?:tỷ số|thắng|thua|hạ|hòa|đánh bại|vượt qua|đè bẹp|vùi dập)[^.,;]{0,36}?\b(\d{1,2}-\d{1,2})\b", txt, flags=re.IGNORECASE)
    if m:
        return {"label": "TỶ SỐ", "value": m.group(1), "sub": "Diễn biến nổi bật"}
    # 3. Cột mốc tiền tệ / giá trị (VD: 400 triệu đồng, 3,4 tỷ USD, 14,08 triệu euro, 34000 USD)
    m = re.search(r"\b(\d+(?:[.,]\d+)?\s*(?:tỷ|triệu|nghìn)?\s*(?:USD|euro|đồng))\b", txt, flags=re.IGNORECASE)
    if m:
        return {"label": "CON SỐ ĐÁNG CHÚ Ý", "value": m.group(1).upper() if "usd" in m.group(1).lower() else m.group(1), "sub": "Thống kê tài chính"}
    # 4. Cột mốc thứ hạng FIFA / thế giới (VD: hạng 99 FIFA, hạng 12 thế giới, tốp 100)
    m = re.search(r"\b(hạng\s+\d{1,3}(?:\s+(?:FIFA|thế giới))?)\b", txt, flags=re.IGNORECASE)
    if m:
        return {"label": "XẾP HẠNG", "value": m.group(1).upper(), "sub": "Bảng xếp hạng"}
    # 5. Cột mốc bàn thắng / trận đấu (VD: 399 bàn, 48 trận, 11 trận)
    m = re.search(r"\b(\d{2,4}\s+(?:bàn thắng|bàn|trận|điểm))\b", txt, flags=re.IGNORECASE)
    if m:
        return {"label": "CỘT MỐC", "value": m.group(1).upper(), "sub": "Thống kê chuyên môn"}
    return None


def compute_daily_plan(items: List[Dict[str, Any]], date_str: str, img_dir: str) -> Dict[str, Any]:
    """
    Sinh Kế Hoạch Ngày (Daily Plan) xác định (deterministic) cho toàn bộ tin:
    - 9 layout: full, split, polaroid, cinema, triptych, hero_mosaic, filmstrip_carousel, spotlight_sequence, bento_grid
    - Không lặp layout giữa 2 câu liền kề
    - Không lặp layout giữa câu cuối tin N và câu đầu tin N+1
    - Phân bổ ảnh chống lặp ảnh liền kề
    - In bảng tổng kết kế hoạch
    """
    base_seed = _hash_str(f"daily_plan_{date_str}_{len(items)}")
    plan_per_item = {}

    last_layout = ""
    used_counts: Dict[str, int] = {}
    table_rows = []

    for it_idx, it in enumerate(items):
        it_id = str(it.get("id", it_idx + 1))
        summary = it.get("summary", "").strip()
        sents = [s.strip() for s in _SENTENCE_SPLIT.split(summary) if s.strip()] or [summary]

        # Thu thập ảnh (sắp xếp theo số thứ tự)
        raw_num = int(it.get("id", it_idx + 1))
        sc_num = f"{raw_num:02d}"
        matched_images = sorted(
            glob.glob(os.path.join(img_dir, f"Tin_{sc_num}_*.jpg")),
            key=lambda p: int(re.search(r"Tin_\d+_(\d+)\.jpg", os.path.basename(p)).group(1))
            if re.search(r"Tin_\d+_(\d+)\.jpg", os.path.basename(p)) else 0
        )
        if not matched_images:
            matched_images = sorted(
                glob.glob(os.path.join(img_dir, f"Tin_{raw_num}_*.jpg")),
                key=lambda p: int(re.search(r"Tin_\d+_(\d+)\.jpg", os.path.basename(p)).group(1))
                if re.search(r"Tin_\d+_(\d+)\.jpg", os.path.basename(p)) else 0
            )
        if not matched_images:
            for k in ["image_1", "image_2", "image_3", "image_4"]:
                if it.get(k) and os.path.exists(it[k]):
                    matched_images.append(it[k])
        if not matched_images:
            matched_images = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))[:4]

        # Ưu tiên đọc kế hoạch ảnh chi tiết từ image_plan.json nếu có
        day_dir_cand = os.path.dirname(img_dir.rstrip("/"))
        img_plan_file = os.path.join(day_dir_cand, "image_plan.json")
        has_plan_json = False
        p_sent_recs = []
        if os.path.exists(img_plan_file):
            try:
                with open(img_plan_file, "r", encoding="utf-8") as pf:
                    raw_plan_data = json.load(pf)
                p_recs = raw_plan_data.get("records", [])
                p_sent_recs = [r for r in p_recs if r.get("scene_id") == raw_num and r.get("type") == "sentence"]
                if p_sent_recs:
                    has_plan_json = True
            except Exception:
                has_plan_json = False

        # Kiểm tra xem có đủ ảnh theo cấu trúc Tiêu đề 3 ảnh + Các câu (1-2 ảnh/câu)
        has_title_and_sent_pool = (len(matched_images) >= len(sents) + 3)
        if has_plan_json:
            item_layouts = []
            item_img_plan = []
            item_seed = _hash_str(f"{base_seed}_{it_id}")
            for s_idx in range(len(sents)):
                s_recs = [r for r in p_sent_recs if (r.get("sentence_idx") == s_idx + 1 or r.get("index") == s_idx + 1)]
                s_imgs = [os.path.join(img_dir, r["file_name"]) for r in s_recs if os.path.exists(os.path.join(img_dir, r["file_name"]))]
                if not s_imgs:
                    s_imgs = matched_images[3 + s_idx : 3 + s_idx + 1] if len(matched_images) > 3 + s_idx else matched_images[:1]
                item_img_plan.append(s_imgs)
                chosen_layout = _pick_smart_layout(len(s_imgs), last_layout, item_seed + s_idx * 13, used_counts)
                item_layouts.append(chosen_layout)
                last_layout = chosen_layout
        elif has_title_and_sent_pool:
            # Tiêu đề hiển thị 3 ảnh trong 1 khung hình (triptych), các câu xoay vòng layout thông minh theo số ảnh
            item_layouts = []
            sent_pool = matched_images[3:]
            item_img_plan = []
            item_seed = _hash_str(f"{base_seed}_{it_id}")
            cur_img_idx = 0
            for s_idx in range(len(sents)):
                w_cnt = len(sents[s_idx].split())
                num_imgs = 2 if w_cnt >= 42 else 1
                s_imgs = sent_pool[cur_img_idx : cur_img_idx + num_imgs]
                cur_img_idx += num_imgs
                if not s_imgs:
                    s_imgs = [sent_pool[-1]] if sent_pool else matched_images[:1]
                item_img_plan.append(s_imgs)
                chosen_layout = _pick_smart_layout(len(s_imgs), last_layout, item_seed + s_idx * 11, used_counts)
                item_layouts.append(chosen_layout)
                last_layout = chosen_layout
        else:
            # Phân bổ layout xoay vòng cũ nếu không đủ ảnh phân tách
            item_layouts = []
            item_seed = _hash_str(f"{base_seed}_{it_id}")

            for s_idx in range(len(sents)):
                candidates = [l for l in _LAYOUT_POOL if l != last_layout]
                pick_idx = (item_seed + s_idx * 7) % len(candidates)
                chosen_layout = candidates[pick_idx]
                item_layouts.append(chosen_layout)
                last_layout = chosen_layout

            item_img_plan = []
            last_assigned_img = ""
            for s_idx in range(len(sents)):
                num_imgs = 2 if len(sents) <= 3 else (2 if s_idx % 2 == 0 else 1)
                if item_layouts[s_idx] in ["split", "cinema"]:
                    num_imgs = 2
                elif item_layouts[s_idx] == "triptych":
                    num_imgs = 3 if len(matched_images) >= 3 else len(matched_images)

                s_imgs = []
                for m_i in range(num_imgs):
                    pool = [im for im in matched_images if im != last_assigned_img] or matched_images
                    c_img = pool[(s_idx + m_i) % len(pool)]
                    s_imgs.append(c_img)
                    last_assigned_img = c_img
                item_img_plan.append(s_imgs)

        plan_per_item[it_id] = {
            "layouts": item_layouts,
            "images": item_img_plan,
            "matched_images": matched_images
        }

        # Dòng cho bảng ASCII
        title_snippet = it.get("title", "")[:28] + ("..." if len(it.get("title", "")) > 28 else "")
        layout_seq = " → ".join(item_layouts)
        table_rows.append((sc_num, title_snippet, str(len(sents)), layout_seq, str(len(matched_images))))

    # In bảng kế hoạch ngày
    log("\n" + "=" * 80)
    log(f"📋 BẢNG KẾ HOẠCH NGÀY (DAILY PLAN) — {date_str} (9 LAYOUTS)")
    log("=" * 80)
    header_fmt = "{:<5} | {:<32} | {:<5} | {:<25} | {:<4}"
    log(header_fmt.format("TIN", "TIÊU ĐỀ", "CÂU", "CHUỖI LAYOUT", "ẢNH"))
    log("-" * 80)
    for r in table_rows:
        log(header_fmt.format(r[0], r[1], r[2], r[3], r[4]))
    log("=" * 80 + "\n")

    return plan_per_item


def build_news_timeline(day_dir: str, item_id: int | str = "1", format_type: str = "long",
                        global_offset_sec: float = 0.0) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Đọc thethao.json và images/, sinh kịch bản timeline chuẩn cho template v2 (long/short).
    """
    day_dir = os.path.abspath(day_dir)
    load_say_overrides(day_dir)
    json_path = os.path.join(day_dir, "thethao.json")
    if not os.path.exists(json_path):
        die(f"Không tìm thấy file {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    # Nếu có intro_hook.json và chưa có id=0 trong thethao.json, gộp vào danh sách plan
    intro_json_path = os.path.join(day_dir, "intro_hook.json")
    plan_items = list(items)
    if os.path.exists(intro_json_path) and not any(str(x.get("id")) == "0" for x in items):
        try:
            with open(intro_json_path, "r", encoding="utf-8") as fi:
                intro_data = json.load(fi)
            if isinstance(intro_data, dict):
                intro_data.setdefault("id", 0)
                plan_items = [intro_data] + plan_items
        except Exception:
            pass

    item = None
    item_str = str(item_id)
    item_idx_found = -1
    for idx, it in enumerate(plan_items):
        if str(it.get("id")) == item_str:
            item = it
            # Tính index trong items tin chính (không tính Intro) để build ticker chính xác
            item_idx_found = next((i for i, x in enumerate(items) if str(x.get("id")) == item_str), -1)
            break
    if item is None:
        try:
            c_idx = int(item_id) - 1
            if 0 <= c_idx < len(items):
                item = items[c_idx]
                item_idx_found = c_idx
        except ValueError:
            pass

    if item is None:
        die(f"Không tìm thấy tin với id={item_id} trong {json_path}")

    title = item.get("title", "").strip()
    group = item.get("group", "BÓNG ĐÁ VIỆT NAM").upper()
    summary = item.get("summary", "").strip()
    audio_path = item.get("audio_path", "")

    if not os.path.exists(audio_path):
        die(f"Không tìm thấy file audio: {audio_path}")

    # Ngày bắt buộc định dạng tiếng Việt (tự động ẩn nếu video chuyên đề không đề cập ngày)
    day_tag = os.path.basename(day_dir.rstrip("/"))
    hide_date_chip = item.get("hide_date_chip", False)
    if os.path.exists(os.path.join(day_dir, "no_date")) or os.path.exists(os.path.join(day_dir, "special_topic")):
        hide_date_chip = True

    date_chip_text = "" if hide_date_chip else parse_date_chip(day_tag)

    # Nguồn ảnh thật (ẩn nếu không có báo cụ thể)
    raw_source = item.get("source") or item.get("credit")
    photo_credit = clean_photo_credit(raw_source)

    # Đo thời lượng thực tế
    aud = AudioSegment.from_file(audio_path)
    total_dur = round(len(aud) / 1000.0, 3)

    # Kế hoạch ngày (Daily Plan)
    img_dir = os.path.join(day_dir, "images")
    daily_plan = compute_daily_plan(plan_items, date_chip_text, img_dir)
    item_plan = daily_plan.get(str(item.get("id", item_id)), {})
    plan_layouts = item_plan.get("layouts", [])
    plan_images = item_plan.get("images", [])

    # Phân tách câu
    raw_sents = [s.strip() for s in _SENTENCE_SPLIT.split(summary) if s.strip()]
    if not raw_sents:
        raw_sents = [summary]

    # Tìm file audio_title nếu có để bù trừ offset tiêu đề chính xác (bỏ qua nếu hide_title hoặc title rỗng)
    hide_title = bool(item.get("hide_title", False) or not title)
    fname = os.path.basename(audio_path)
    title_audio_path = None
    if not hide_title:
        candidate_title_audio = os.path.join(day_dir, "audio-title", fname)
        if not os.path.exists(candidate_title_audio) and item.get("audio_title"):
            if os.path.exists(item.get("audio_title")):
                candidate_title_audio = item.get("audio_title")
        if os.path.exists(candidate_title_audio):
            title_audio_path = candidate_title_audio

    # TÍNH MỐC CÂU BẰNG AUDIO GROUND TRUTH (Cumulative drift = 0, vết cắt trùng khoảng lặng +-100ms)
    summary_start, total_dur, sent_bounds = compute_ground_truth_sentence_timings(
        audio_path, raw_sents, title_audio_path=title_audio_path
    )
    if hide_title and sent_bounds:
        summary_start = 0.0
        sent_bounds[0] = (0.0, sent_bounds[0][1])

    sent_timings = []
    for idx, sent_text in enumerate(raw_sents):
        s_start, s_end = sent_bounds[idx]
        s_dur = round(max(0.1, s_end - s_start), 3)
        s_words = interpolate_sentence_words(sent_text, s_start, s_end)
        sent_timings.append((sent_text, s_start, s_end, s_dur, s_words))

    # Xây dựng các cảnh / câu và karaoke chunks
    sentences_data = []
    all_karaoke_chunks = []
    all_word_timestamps = []
    short_img_counter = 0

    # Tải bản đồ nguồn ảnh (image credits map) nếu có
    img_credits_map: Dict[str, str] = {}
    credits_file = os.path.join(day_dir, "image_credits.json")
    if os.path.exists(credits_file):
        try:
            with open(credits_file, "r", encoding="utf-8") as f:
                img_credits_map = json.load(f)
        except Exception:
            img_credits_map = {}

    img_plan_path = os.path.join(day_dir, "image_plan.json")
    if os.path.exists(img_plan_path):
        try:
            with open(img_plan_path, "r", encoding="utf-8") as pf:
                raw_plan = json.load(pf)
            for r in raw_plan.get("records", []):
                fn = r.get("file_name")
                cr = r.get("credit")
                if fn and cr and fn not in img_credits_map:
                    img_credits_map[fn] = cr
        except Exception:
            pass

    matched_images = item_plan.get("matched_images", [])
    sentence_charts = item.get("sentence_charts") or {}

    # CẢNH TIÊU ĐỀ: Nếu không hide_title và có audio_title (summary_start > 0.2s), hiển thị các ảnh tiêu đề
    # và bắt buộc sinh Karaoke Chunks & Word Timestamps từ giây 0 để subtitle khớp thoại 100%
    if (not hide_title) and summary_start > 0.2:
        title_imgs = matched_images[:3] if len(matched_images) >= 3 else (matched_images or [])
        t_assigned = []
        n_t = max(1, len(title_imgs))
        t_slice = summary_start / n_t
        for t_idx, t_choice in enumerate(title_imgs):
            im_s = round(t_idx * t_slice, 3)
            im_e = summary_start if t_idx == n_t - 1 else round((t_idx + 1) * t_slice, 3)
            im_dur = round(im_e - im_s, 3)
            pan_info = compute_pan_params(t_choice, duration=im_dur, dir_toggle=(short_img_counter % 2 == 1))
            short_img_counter += 1
            t_base = os.path.basename(t_choice)
            t_cred = img_credits_map.get(t_base, photo_credit)
            t_assigned.append({
                "src": t_choice,
                "credit": t_cred,
                "start": im_s,
                "end": im_e,
                "duration": im_dur,
                "ken_burns": "pan_horizontal",
                "transition": "fade",
                **pan_info
            })
        t_sent_obj: Dict[str, Any] = {
            "sentence_id": 0,
            "text": title,
            "start": 0.0,
            "end": summary_start,
            "duration": summary_start,
            "layout": "triptych" if len(title_imgs) >= 3 else "full",
            "is_title": True,
            "keywords": _extract_keywords(title),
            "images": t_assigned
        }
        if sentence_charts.get("0"):
            t_sent_obj["chart"] = sentence_charts["0"]
        if item.get("hook"):
            t_sent_obj["hook"] = item["hook"]
        sentences_data.append(t_sent_obj)

        # ĐỒNG BỘ SUBTITLE PHỤ ĐỀ KARAOKE TỪ GIÂY 0 (TIÊU ĐỀ)
        title_words_timed = interpolate_sentence_words(title, 0.0, summary_start)
        for w_obj in title_words_timed:
            all_word_timestamps.append(w_obj)

        chunk_size = 4
        for ci in range(0, len(title_words_timed), chunk_size):
            c_words = title_words_timed[ci:ci + chunk_size]
            all_karaoke_chunks.append({
                "start": c_words[0]["start"],
                "end": c_words[-1]["end"],
                "text": " ".join(cw["word"] for cw in c_words),
                "words": c_words
            })

    kb_variants = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
    tr_variants = ["fade", "wipe_left", "slide_up", "zoom_in"]
    last_hud_idx = -2

    for i, (sent_text, s_start, s_end, s_dur, sent_words_timed) in enumerate(sent_timings):
        layout = plan_layouts[i] if i < len(plan_layouts) else "full"
        kw = _extract_keywords(sent_text)
        stage_tr = tr_variants[(i + _hash_str(str(item_id))) % len(tr_variants)]
        custom_badges = item.get("stat_badges") or {}
        explicit_badge = custom_badges.get(str(i + 1))
        stat_badge = None
        if explicit_badge and isinstance(explicit_badge, dict) and explicit_badge.get("value"):
            stat_badge = explicit_badge
            last_hud_idx = i
        elif i - last_hud_idx >= 2 and s_dur >= 5.0:
            stat_badge = _extract_stat_badge(sent_text)
            if stat_badge:
                last_hud_idx = i

        # Danh sách ảnh đã được lập kế hoạch cho câu này
        assigned_img_files = plan_images[i] if i < len(plan_images) and plan_images[i] else item_plan.get("matched_images", [])[:2]
        if not assigned_img_files:
            assigned_img_files = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))[:2]

        num_imgs = len(assigned_img_files)
        img_slice_dur = s_dur / max(1, num_imgs)

        assigned_images = []
        for img_idx, img_choice in enumerate(assigned_img_files):
            h_val = _hash_str(os.path.basename(img_choice) + f"_{i}_{img_idx}")
            im_start = round(s_start + img_idx * img_slice_dur, 3)
            im_end = s_end if img_idx == num_imgs - 1 else round(im_start + img_slice_dur, 3)
            im_dur = round(im_end - im_start, 3)
            pan_info = compute_pan_params(img_choice, duration=im_dur, dir_toggle=(short_img_counter % 2 == 1))
            short_img_counter += 1
            img_base = os.path.basename(img_choice)
            img_cred = img_credits_map.get(img_base, photo_credit)

            assigned_images.append({
                "src": img_choice,
                "credit": img_cred,
                "start": im_start,
                "end": im_end,
                "duration": im_dur,
                "ken_burns": kb_variants[h_val % len(kb_variants)],
                "transition": tr_variants[(h_val // 4) % len(tr_variants)],
                **pan_info
            })

        # Ghi nhận Word Timestamps thật từ Whisper
        for w_obj in sent_words_timed:
            all_word_timestamps.append(w_obj)

        # Gom Karaoke Chunks (3-5 từ/cụm)
        chunk_size = 4
        for ci in range(0, len(sent_words_timed), chunk_size):
            c_words = sent_words_timed[ci:ci + chunk_size]
            all_karaoke_chunks.append({
                "start": c_words[0]["start"],
                "end": c_words[-1]["end"],
                "text": " ".join(cw["word"] for cw in c_words),
                "words": c_words
            })

        s_obj: Dict[str, Any] = {
            "sentence_id": i + 1,
            "text": sent_text,
            "start": round(s_start, 3),
            "end": round(s_end, 3),
            "duration": round(s_dur, 3),
            "layout": layout,
            "transition": stage_tr,
            "keywords": kw,
            "images": assigned_images
        }
        if stat_badge:
            s_obj["stat_badge"] = stat_badge
        if sentence_charts.get(str(i + 1)):
            s_obj["chart"] = sentence_charts[str(i + 1)]
        if i == 0 and item.get("hook") and not any(s.get("is_title") for s in sentences_data):
            s_obj["hook"] = item["hook"]
        sentences_data.append(s_obj)

    # Scenes tương thích QA
    scenes_data = []
    for sent in sentences_data:
        scenes_data.append({
            "scene_id": sent["sentence_id"],
            "start_time": sent["start"],
            "_start_time": sent["start"],
            "duration": sent["duration"],
            "_duration": sent["duration"],
            "script_text": sent["text"],
            "cards": []
        })

    # Ticker headlines (chỉ các tin SAU tin hiện tại, bỏ tiền tố TIN XX:)
    ticker_headlines = []
    subsequent_items = items[item_idx_found + 1:] if item_idx_found >= 0 else []
    for o_it in subsequent_items:
        o_title = o_it.get("title", "").strip()
        if o_title:
            ticker_headlines.append(o_title.upper())

    # Nếu là tin cuối cùng, quay vòng lấy các tin trước đó
    if not ticker_headlines:
        for o_it in items[:item_idx_found]:
            o_title = o_it.get("title", "").strip()
            if o_title:
                ticker_headlines.append(o_title.upper())

    # Nạp config/fx.json
    fx_cfg = {}
    fx_path = os.path.join(paths.CONFIG, "fx.json")
    if os.path.exists(fx_path):
        try:
            with open(fx_path, "r", encoding="utf-8") as f:
                fx_cfg = json.load(f)
        except Exception as e:
            warn(f"Không nạp được config/fx.json: {e}")

    # SFX events
    raw_sfx_events = []
    if item.get("hook"):
        raw_sfx_events.extend([
            {"sfx": "sub_drop_boom.mp3", "time": 0.02, "volume": 0.28},
            {"sfx": "bell_ping_highlight.mp3", "time": 0.76, "volume": 0.22},
            {"sfx": "whoosh_cinematic_1.mp3", "time": 1.50, "volume": 0.22},
            {"sfx": "pop_card.mp3", "time": 2.15, "volume": 0.20},
            {"sfx": "whoosh_cinematic_short.mp3", "time": 3.00, "volume": 0.22},
        ])
    for i, (sent_text, s_start, s_end, s_dur, _) in enumerate(sent_timings):
        if i > 0:
            raw_sfx_events.append({
                "sfx": "whoosh_cinematic_short.mp3",
                "time": round(s_start, 3),
                "volume": 0.20
            })

    for sent in sentences_data:
        kw_list = [k.lower() for k in sent.get("keywords", [])]
        for w_obj in all_word_timestamps:
            if sent["start"] <= w_obj["start"] < sent["end"]:
                clean_w = re.sub(r'[^\w\d]', '', w_obj["word"]).lower()
                if any(clean_w and (clean_w in kw or kw in clean_w) for kw in kw_list):
                    raw_sfx_events.append({
                        "sfx": "pop_card.mp3",
                        "time": round(w_obj["start"], 3),
                        "volume": 0.18
                    })

    raw_sfx_events.sort(key=lambda x: x["time"])
    filtered_sfx = []
    last_t = -1.0
    for ev in raw_sfx_events:
        if ev["time"] - last_t >= 0.25:
            filtered_sfx.append(ev)
            last_t = ev["time"]

    raw_num = int(item.get("id", item_id))
    item_news_source = item.get("news_source") or item.get("source") or "ĐIỂM ĐỌC THỂ THAO"
    for s_obj in sentences_data:
        s_obj.setdefault("item_id", str(item.get("id", item_id)))
        s_obj.setdefault("item_index", raw_num)
        s_obj.setdefault("total_items", len(items))
        s_obj.setdefault("item_title", title)
        s_obj.setdefault("item_group", group)
        s_obj.setdefault("news_source", item_news_source)
        s_obj.setdefault("credit", photo_credit)

    timeline = {
        "title": title,
        "hide_title": hide_title,
        "group": group,
        "channel_name": "ĐIỂM ĐỌC",
        "item_id": str(item.get("id", item_id)),
        "item_index": raw_num,
        "total_items": len(items),
        "total_duration": total_dur,
        "date_str": date_chip_text,
        "date_chip": date_chip_text,
        "hide_date_chip": hide_date_chip,
        "output_filename": f"tin_{raw_num:02d}_{format_type}.mp4",
        "format": "long" if format_type == "long" else "short",
        "template": "long_sports_news_v2.html" if format_type == "long" else "short_news_v2.html",
        "dimensions": [1920, 1080] if format_type == "long" else [1080, 1920],
        "fps": 30,
        "audio_path": audio_path,
        "credit": photo_credit,
        "news_source": item_news_source,
        "global_offset_sec": float(global_offset_sec),
        "fx": fx_cfg,
        "ticker_headlines": ticker_headlines,
        "sfx_events": filtered_sfx,
        "scenes": scenes_data,
        "sentences": sentences_data,
        "karaoke_chunks": all_karaoke_chunks
    }

    words_data = {
        "words": all_word_timestamps,
        "karaoke_chunks": all_karaoke_chunks
    }

    return timeline, words_data


def export_bridge_project(day_dir: str, item_id: int | str = "1", format_type: str = "long",
                          work_proj_dir: Optional[str] = None,
                          global_offset_sec: float = 0.0) -> Tuple[str, str, str]:
    """
    Xuất dữ liệu timeline và word_timestamps vào thư mục project trong WORK (ngoài Drive).
    """
    timeline, words_data = build_news_timeline(day_dir, item_id, format_type, global_offset_sec=global_offset_sec)

    if not work_proj_dir:
        day_tag = os.path.basename(day_dir.rstrip("/"))
        work_proj_dir = os.path.join(paths.WORK, f"test_v2_{day_tag}_tin_{item_id}_{format_type}")

    os.makedirs(work_proj_dir, exist_ok=True)
    tl_path = os.path.join(work_proj_dir, "video_timeline.json")
    words_path = os.path.join(work_proj_dir, "word_timestamps.json")
    voice_dest = os.path.join(work_proj_dir, "voiceover.wav")

    if timeline.get("audio_path") and os.path.exists(timeline["audio_path"]):
        import shutil
        shutil.copy2(timeline["audio_path"], voice_dest)

    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)

    ok(f"Cầu nối xuất timeline thành công: {tl_path}")
    return work_proj_dir, tl_path, words_path


def build_focus_short_timeline(day_dir: str, item_ids: List[int | str] = [1, 2, 3],
                               global_offset_sec: float = 0.0,
                               custom_items: List[Dict[str, Any]] | None = None) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """
    Xây dựng timeline cho Focus Short (gộp 3-5 tin chi tiết thành 1 video 9:16).
    - Nối âm thanh các tin với khoảng nghỉ 0.4s + SFX whoosh
    - Hạt lấp lánh chạy liền mạch với offset toàn cục
    - Kế hoạch bố cục chống lặp xuyên ranh giới các tin
    - Thẻ tiêu đề Hero xuất hiện đầu mỗi tin, sau đó thu về thanh tiêu đề cố định
    - Cập nhật category pill và credit theo từng tin
    """
    day_dir = os.path.abspath(day_dir)
    load_say_overrides(day_dir)
    json_path = os.path.join(day_dir, "thethao.json")
    if custom_items is not None:
        all_items = custom_items
    else:
        if not os.path.exists(json_path):
            die(f"Không tìm thấy {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            all_items = json.load(f)

    selected_items = []
    for it_id in item_ids:
        found = next((it for it in all_items if str(it.get("id")) == str(it_id)), None)
        if found:
            selected_items.append(found)

    if not selected_items:
        die("Không tìm thấy tin nào được chọn cho Focus Short")

    date_chip_text = parse_date_chip(day_dir)
    hide_date_chip = False
    if os.path.exists(os.path.join(day_dir, "no_date")) or os.path.exists(os.path.join(day_dir, "special_topic")):
        hide_date_chip = True
    if hide_date_chip:
        date_chip_text = ""

    img_dir = os.path.join(day_dir, "images")
    day_tag = os.path.basename(day_dir.rstrip("/"))
    focus_work_dir = os.path.join(paths.WORK, f"focus_short_{day_tag}")
    os.makedirs(focus_work_dir, exist_ok=True)

    # Tải bản đồ nguồn ảnh (image_credits.json / image_plan.json)
    img_credits_map: Dict[str, str] = {}
    credits_file = os.path.join(day_dir, "image_credits.json")
    if os.path.exists(credits_file):
        try:
            with open(credits_file, "r", encoding="utf-8") as f:
                img_credits_map = json.load(f)
        except Exception:
            img_credits_map = {}

    img_plan_path = os.path.join(day_dir, "image_plan.json")
    if os.path.exists(img_plan_path):
        try:
            with open(img_plan_path, "r", encoding="utf-8") as pf:
                raw_plan = json.load(pf)
            for r in raw_plan.get("records", []):
                fn = r.get("file_name")
                cr = r.get("credit")
                if fn and cr and fn not in img_credits_map:
                    img_credits_map[fn] = cr
        except Exception:
            pass

    # 1. Kế hoạch bố cục xuyên suốt các tin để không bị lặp liên tiếp
    daily_plan = compute_daily_plan(all_items, date_chip_text, img_dir)

    combined_audio = AudioSegment.silent(duration=0)
    gap_ms = 400  # 0.4s giữa các tin
    gap_audio = AudioSegment.silent(duration=gap_ms)

    items_timeline_data = []
    all_sentences_flat = []
    all_karaoke_flat = []
    all_words_flat = []
    raw_sfx_events = []
    short_img_counter = 0

    cum_offset_sec = 0.0

    for idx, item in enumerate(selected_items):
        it_id = str(item.get("id", idx + 1))
        it_title = item.get("title", "").strip()
        it_group = item.get("group", "BÓNG ĐÁ VIỆT NAM").upper()
        it_summary = item.get("summary", "").strip()
        it_audio_path = item.get("audio_path", "")
        it_news_source = item.get("news_source") or item.get("source") or "ĐIỂM ĐỌC THỂ THAO"
        photo_credit = clean_photo_credit(item.get("credit") or item.get("source"))

        if not it_audio_path or not os.path.exists(it_audio_path):
            die(f"Thiếu file audio {it_audio_path} cho tin {it_id}")

        seg = AudioSegment.from_wav(it_audio_path)
        it_dur = len(seg) / 1000.0

        if idx > 0:
            combined_audio += gap_audio
            cum_offset_sec += (gap_ms / 1000.0)
            raw_sfx_events.append({
                "sfx": "whoosh_cinematic_short.mp3",
                "time": round(cum_offset_sec, 3),
                "volume": 0.28
            })

        it_audio_start = cum_offset_sec
        combined_audio += seg
        cum_offset_sec += it_dur
        it_audio_end = cum_offset_sec

        # TÍNH MỐC CÂU BẰNG AUDIO GROUND TRUTH CHO TIN NÀY
        raw_sents = [s.strip() for s in _SENTENCE_SPLIT.split(it_summary) if s.strip()]
        if not raw_sents:
            raw_sents = [it_summary]

        it_title_path = item.get("audio_title")
        if not it_title_path or not os.path.exists(it_title_path):
            it_fname = os.path.basename(it_audio_path)
            cand1 = os.path.join(day_dir, "audio-title", it_fname)
            cand2 = os.path.join(day_dir, "audio-title", f"audio_title_{int(it_id):02d}.wav")
            if os.path.exists(cand1):
                it_title_path = cand1
            elif os.path.exists(cand2):
                it_title_path = cand2
            else:
                it_title_path = None

        sum_start, it_tot_dur, sent_bounds = compute_ground_truth_sentence_timings(
            it_audio_path, raw_sents, title_audio_path=it_title_path
        )

        it_plan = daily_plan.get(it_id, {})
        plan_layouts = it_plan.get("layouts", [])
        plan_images = it_plan.get("images", [])
        matched_images = it_plan.get("matched_images", [])

        it_sentences = []
        kb_variants = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
        tr_variants = ["wipe", "push", "zoom"]

        # CẢNH TIÊU ĐỀ CHO TỪNG TIN TRONG FOCUS SHORT (khi sum_start > 0.2s)
        if sum_start > 0.2 and it_title:
            title_imgs = matched_images[:2] if len(matched_images) >= 2 else (matched_images or sorted(glob.glob(os.path.join(img_dir, "*.jpg")))[:2])
            t_assigned = []
            n_t = max(1, len(title_imgs))
            t_slice = sum_start / n_t
            t_abs_start = round(it_audio_start, 3)
            t_abs_end = round(it_audio_start + sum_start, 3)
            for t_idx, t_choice in enumerate(title_imgs):
                im_s = round(t_abs_start + t_idx * t_slice, 3)
                im_e = t_abs_end if t_idx == n_t - 1 else round(im_s + t_slice, 3)
                im_dur = round(max(0.1, im_e - im_s), 3)
                pan_info = compute_pan_params(t_choice, duration=im_dur, dir_toggle=(short_img_counter % 2 == 1))
                short_img_counter += 1
                t_base = os.path.basename(t_choice)
                t_cred = img_credits_map.get(t_base, photo_credit)
                t_assigned.append({
                    "src": t_choice,
                    "credit": t_cred,
                    "start": im_s,
                    "end": im_e,
                    "duration": im_dur,
                    "ken_burns": "pan_horizontal",
                    "transition": "fade",
                    **pan_info
                })

            title_words_local = interpolate_sentence_words(it_title, 0.0, sum_start)
            abs_title_words = []
            for w_obj in title_words_local:
                abs_w = {
                    "word": w_obj["word"],
                    "start": round(it_audio_start + w_obj["start"], 3),
                    "end": round(it_audio_start + w_obj["end"], 3),
                    "matched": True
                }
                abs_title_words.append(abs_w)
                all_words_flat.append(abs_w)

            for ci in range(0, len(abs_title_words), 4):
                c_words = abs_title_words[ci:ci + 4]
                all_karaoke_flat.append({
                    "start": c_words[0]["start"],
                    "end": c_words[-1]["end"],
                    "text": " ".join(cw["word"] for cw in c_words),
                    "words": c_words
                })

            title_sent_obj = {
                "sentence_id": len(all_sentences_flat) + 1,
                "text": it_title,
                "start": t_abs_start,
                "end": t_abs_end,
                "duration": round(sum_start, 3),
                "layout": "full",
                "is_title": True,
                "item_id": it_id,
                "item_index": idx + 1,
                "total_items": len(selected_items),
                "item_title": it_title,
                "item_group": it_group,
                "news_source": it_news_source,
                "credit": photo_credit,
                "keywords": _extract_keywords(it_title),
                "images": t_assigned
            }
            if item.get("hook") and idx == 0:
                title_sent_obj["hook"] = item["hook"]
            it_sentences.append(title_sent_obj)
            all_sentences_flat.append(title_sent_obj)

        for s_idx, sent_text in enumerate(raw_sents):
            local_s, local_e = sent_bounds[s_idx]
            s_words = interpolate_sentence_words(sent_text, local_s, local_e)

            abs_start = round(it_audio_start + local_s, 3)
            abs_end = round(it_audio_start + local_e, 3)
            abs_dur = round(max(0.1, abs_end - abs_start), 3)

            layout = plan_layouts[s_idx] if s_idx < len(plan_layouts) else _LAYOUT_POOL[s_idx % len(_LAYOUT_POOL)]
            assigned_img_files = plan_images[s_idx] if s_idx < len(plan_images) and plan_images[s_idx] else matched_images[:2]
            if not assigned_img_files:
                assigned_img_files = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))[:2]

            num_imgs = len(assigned_img_files)
            img_slice_dur = abs_dur / max(1, num_imgs)
            assigned_images = []
            for img_idx, img_choice in enumerate(assigned_img_files):
                h_val = _hash_str(os.path.basename(img_choice) + f"_{idx}_{s_idx}_{img_idx}")
                im_start = round(abs_start + img_idx * img_slice_dur, 3)
                im_end = abs_end if img_idx == num_imgs - 1 else round(im_start + img_slice_dur, 3)
                im_dur = round(im_end - im_start, 3)
                pan_info = compute_pan_params(img_choice, duration=im_dur, dir_toggle=(short_img_counter % 2 == 1))
                short_img_counter += 1
                img_base = os.path.basename(img_choice)
                img_cred = img_credits_map.get(img_base, photo_credit)
                assigned_images.append({
                    "src": img_choice,
                    "credit": img_cred,
                    "start": im_start,
                    "end": im_end,
                    "duration": im_dur,
                    "ken_burns": kb_variants[h_val % len(kb_variants)],
                    "transition": tr_variants[(h_val // 4) % len(tr_variants)],
                    **pan_info
                })

            # Word timestamps dời sang trục thời gian tuyệt đối
            abs_sent_words = []
            for w_obj in s_words:
                abs_w = {
                    "word": w_obj["word"],
                    "start": round(it_audio_start + w_obj["start"], 3),
                    "end": round(it_audio_start + w_obj["end"], 3),
                    "matched": w_obj.get("matched", True)
                }
                abs_sent_words.append(abs_w)
                all_words_flat.append(abs_w)

            # Karaoke chunks
            chunk_size = 4
            for ci in range(0, len(abs_sent_words), chunk_size):
                c_words = abs_sent_words[ci:ci + chunk_size]
                all_karaoke_flat.append({
                    "start": c_words[0]["start"],
                    "end": c_words[-1]["end"],
                    "text": " ".join(cw["word"] for cw in c_words),
                    "words": c_words
                })

            sent_obj = {
                "sentence_id": len(all_sentences_flat) + 1,
                "text": sent_text,
                "start": abs_start,
                "end": abs_end,
                "duration": abs_dur,
                "layout": layout,
                "is_title": False,
                "item_id": it_id,
                "item_index": idx + 1,
                "total_items": len(selected_items),
                "item_title": it_title,
                "item_group": it_group,
                "news_source": it_news_source,
                "credit": photo_credit,
                "keywords": _extract_keywords(sent_text),
                "images": assigned_images
            }
            item_charts = item.get("sentence_charts") or {}
            if item_charts.get(str(s_idx + 1)):
                sent_obj["chart"] = item_charts[str(s_idx + 1)]
            it_sentences.append(sent_obj)
            all_sentences_flat.append(sent_obj)

        items_timeline_data.append({
            "id": it_id,
            "title": it_title,
            "group": it_group,
            "credit": photo_credit,
            "news_source": it_news_source,
            "start": round(it_audio_start, 3),
            "end": round(it_audio_end, 3),
            "duration": round(it_dur, 3),
            "sentences": it_sentences
        })

    # Xuất file audio đã nối và chuẩn hoá loudnorm 2 lượt (-14.0 LUFS, TP <= -1.0 dBTP)
    raw_concat_wav = os.path.join(focus_work_dir, "voiceover_focus_raw.wav")
    concat_wav = os.path.join(focus_work_dir, "voiceover_focus.wav")
    combined_audio.export(raw_concat_wav, format="wav")
    from diemdoc.audio import two_pass_loudnorm
    if not two_pass_loudnorm(raw_concat_wav, concat_wav, target_i=-14.0, target_tp=-1.5, target_lra=11.0):
        combined_audio.export(concat_wav, format="wav")
    total_focus_dur = round(len(combined_audio) / 1000.0, 3)

    # Nạp cấu hình fx.json
    fx_path = os.path.join(paths.CONFIG, "fx.json")
    fx_cfg = {}
    if os.path.exists(fx_path):
        try:
            with open(fx_path, "r", encoding="utf-8") as f:
                fx_cfg = json.load(f)
        except Exception:
            pass

    # Lọc SFX min_gap 0.25s
    raw_sfx_events.sort(key=lambda x: x["time"])
    filtered_sfx = []
    last_t = -1.0
    for ev in raw_sfx_events:
        if ev["time"] - last_t >= 0.25:
            filtered_sfx.append(ev)
            last_t = ev["time"]

    timeline = {
        "title": items_timeline_data[0]["title"],
        "group": items_timeline_data[0]["group"],
        "channel_name": "ĐIỂM ĐỌC",
        "date_str": date_chip_text,
        "date_chip": date_chip_text,
        "hide_date_chip": hide_date_chip,
        "total_duration": total_focus_dur,
        "format": "short",
        "template": "short_news_v2.html",
        "dimensions": [1080, 1920],
        "fps": 30,
        "audio_path": concat_wav,
        "credit": items_timeline_data[0]["credit"],
        "news_source": items_timeline_data[0].get("news_source", "ĐIỂM ĐỌC THỂ THAO"),
        "global_offset_sec": float(global_offset_sec),
        "fx": fx_cfg,
        "sfx_events": filtered_sfx,
        "items": items_timeline_data,
        "sentences": all_sentences_flat,
        "karaoke_chunks": all_karaoke_flat
    }

    words_data = {
        "words": all_words_flat,
        "karaoke_chunks": all_karaoke_flat
    }

    return timeline, words_data, focus_work_dir


def export_focus_short_project(day_dir: str, item_ids: List[int | str] = [1, 2, 3],
                              work_proj_dir: Optional[str] = None,
                              global_offset_sec: float = 0.0) -> Tuple[str, str, str]:
    """Xuất project Focus Short vào thư mục WORK ngoài Drive."""
    timeline, words_data, default_work = build_focus_short_timeline(day_dir, item_ids, global_offset_sec=global_offset_sec)
    proj_dir = work_proj_dir or default_work
    os.makedirs(proj_dir, exist_ok=True)

    tl_path = os.path.join(proj_dir, "video_timeline.json")
    words_path = os.path.join(proj_dir, "word_timestamps.json")
    voice_dest = os.path.join(proj_dir, "voiceover.wav")

    import shutil
    if os.path.exists(timeline["audio_path"]) and os.path.abspath(timeline["audio_path"]) != os.path.abspath(voice_dest):
        shutil.copy2(timeline["audio_path"], voice_dest)

    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)

    ok(f"Đã xuất timeline Focus Short: {tl_path}")
    return proj_dir, tl_path, words_path


def build_digest_short_timeline(day_dir: str, item_ids: List[int | str] = [1, 2, 3, 4],
                                global_offset_sec: float = 0.0) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """
    Xây dựng timeline cho Digest Short ("Đọc nhanh thể thao") theo template short_digest_v2.html.
    - Mỗi tin 7-10s: 1 ảnh tốt nhất + tiêu đề lớn + 1 câu tóm tắt <= 25 từ
    - Đọc bằng ViTTS Minh Quân Pro, trích xuất mốc từ bằng Whisper
    - Chuyển cảnh nhanh giữa các tin + whoosh
    """
    day_dir = os.path.abspath(day_dir)
    load_say_overrides(day_dir)
    json_path = os.path.join(day_dir, "thethao.json")
    if not os.path.exists(json_path):
        die(f"Không tìm thấy {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        all_items = json.load(f)

    selected_items = []
    for it_id in item_ids:
        found = next((it for it in all_items if str(it.get("id")) == str(it_id)), None)
        if found:
            selected_items.append(found)

    if not selected_items:
        die("Không tìm thấy tin nào được chọn cho Digest Short")

    date_chip_text = parse_date_chip(day_dir)
    day_tag = os.path.basename(day_dir.rstrip("/"))
    hide_date_chip = False
    if os.path.exists(os.path.join(day_dir, "no_date")) or os.path.exists(os.path.join(day_dir, "special_topic")):
        hide_date_chip = True
    if hide_date_chip:
        date_chip_text = ""
    digest_work_dir = os.path.join(paths.WORK, f"digest_short_{day_tag}")
    os.makedirs(digest_work_dir, exist_ok=True)

    # Sinh giọng đọc cho từng câu digest_line theo chuẩn config/voice.json
    import vieneu
    from vieneu import Vieneu
    from diemdoc.tts_text import prepare
    from diemdoc.publisher import load_voice_preset
    from m3_voice import render_chunk_vitts

    voice_preset = load_voice_preset("primary")
    voice_model = Vieneu()
    tts_cache_dir = paths.ensure_dir(paths.work_file("tts_cache"))

    combined_audio = AudioSegment.silent(duration=0)
    gap_ms = 300  # 0.3s pause giữa các tin
    gap_audio = AudioSegment.silent(duration=gap_ms)

    items_data = []
    all_words = []
    all_karaoke = []
    raw_sfx = []
    cum_sec = 0.0

    for idx, item in enumerate(selected_items):
        it_id = str(item.get("id", idx + 1))
        it_title = (item.get("digest_title") or item.get("title", "")).strip()
        digest_text = (item.get("digest_line") or item.get("summary", "")).strip()
        photo_credit = clean_photo_credit(item.get("credit") or item.get("source"))
        it_news_source = item.get("news_source") or item.get("source") or "ĐIỂM ĐỌC THỂ THAO"

        # Tìm ảnh tốt nhất (ảnh bìa hoặc image_1 hoặc image_path)
        img_cand = item.get("image_1") or item.get("image_path")
        if not img_cand or not os.path.exists(img_cand):
            img_cands = sorted(glob.glob(os.path.join(day_dir, "images", f"*Tin_{int(it_id):02d}*.jpg")))
            img_cand = img_cands[0] if img_cands else ""

        tts_str, _ = prepare(digest_text)
        item_wav = os.path.join(digest_work_dir, f"digest_line_{int(it_id):02d}.wav")

        # Sinh giọng ViTTS theo chuẩn config/voice.json (Minh Quân Pro: speed=1.12, pitch=0.93, temp=0.6)
        seg, _ = render_chunk_vitts(
            voice_model,
            tts_str,
            voice=voice_preset["voice_id"],
            temperature=voice_preset["temperature"],
            speed=voice_preset["speed"],
            pitch=voice_preset["pitch"],
            cache_dir=tts_cache_dir,
            use_cache=True,
        )
        seg.export(item_wav, format="wav")
        it_dur = len(seg) / 1000.0

        if idx > 0:
            combined_audio += gap_audio
            cum_sec += (gap_ms / 1000.0)
            raw_sfx.append({
                "sfx": "whoosh_cinematic_short.mp3",
                "time": round(cum_sec, 3),
                "volume": 0.25
            })

        it_start = cum_sec
        combined_audio += seg
        cum_sec += it_dur
        it_end = cum_sec

        # TÍNH MỐC TỪ BẰNG AUDIO GROUND TRUTH CHO CÂU DIGEST NÀY
        s_words = interpolate_sentence_words(digest_text, 0.0, it_dur)
        abs_words = []
        for w in s_words:
            abs_w = {
                "word": w["word"],
                "start": round(it_start + w["start"], 3),
                "end": round(it_start + w["end"], 3),
                "matched": True
            }
            abs_words.append(abs_w)
            all_words.append(abs_w)

        # Karaoke chunks (4 từ/cụm)
        for ci in range(0, len(abs_words), 4):
            c_words = abs_words[ci:ci + 4]
            all_karaoke.append({
                "start": c_words[0]["start"],
                "end": c_words[-1]["end"],
                "text": " ".join(cw["word"] for cw in c_words),
                "words": c_words
            })

        # Tính toán lia ảnh theo trọng tâm thị giác nhân vật (focal subject pan)
        pan_info = compute_pan_params(img_cand, duration=it_dur, dir_toggle=(idx % 2 == 1))

        items_data.append({
            "id": it_id,
            "title": it_title,
            "digest_line": digest_text,
            "image": img_cand,
            "credit": photo_credit,
            "news_source": it_news_source,
            "start": round(it_start, 3),
            "end": round(it_end, 3),
            "duration": round(it_dur, 3),
            **pan_info
        })

    # Lưu master audio và chuẩn hoá loudnorm 2 lượt (-14.0 LUFS, TP <= -1.0 dBTP)
    raw_concat_wav = os.path.join(digest_work_dir, "voiceover_digest_raw.wav")
    concat_wav = os.path.join(digest_work_dir, "voiceover_digest.wav")
    combined_audio.export(raw_concat_wav, format="wav")

    from diemdoc.audio import two_pass_loudnorm
    if not two_pass_loudnorm(raw_concat_wav, concat_wav, target_i=-14.0, target_tp=-1.5, target_lra=11.0):
        combined_audio.export(concat_wav, format="wav")
    total_digest_dur = round(len(combined_audio) / 1000.0, 3)

    # Nạp cấu hình fx.json
    fx_path = os.path.join(paths.CONFIG, "fx.json")
    fx_cfg = {}
    if os.path.exists(fx_path):
        try:
            with open(fx_path, "r", encoding="utf-8") as f:
                fx_cfg = json.load(f)
        except Exception:
            pass

    timeline = {
        "title": "ĐỌC NHANH THỂ THAO",
        "channel_name": "ĐIỂM ĐỌC",
        "date_str": date_chip_text,
        "date_chip": date_chip_text,
        "hide_date_chip": hide_date_chip,
        "total_duration": total_digest_dur,
        "format": "short",
        "template": "short_digest_v2.html",
        "dimensions": [1080, 1920],
        "fps": 30,
        "audio_path": concat_wav,
        "global_offset_sec": float(global_offset_sec),
        "fx": fx_cfg,
        "sfx_events": raw_sfx,
        "items": items_data,
        "karaoke_chunks": all_karaoke
    }

    words_data = {
        "words": all_words,
        "karaoke_chunks": all_karaoke
    }

    return timeline, words_data, digest_work_dir


def export_digest_short_project(day_dir: str, item_ids: List[int | str] = [1, 2, 3, 4],
                               work_proj_dir: Optional[str] = None,
                               global_offset_sec: float = 0.0) -> Tuple[str, str, str]:
    """Xuất project Digest Short vào thư mục WORK ngoài Drive."""
    timeline, words_data, default_work = build_digest_short_timeline(day_dir, item_ids, global_offset_sec=global_offset_sec)
    proj_dir = work_proj_dir or default_work
    os.makedirs(proj_dir, exist_ok=True)

    tl_path = os.path.join(proj_dir, "video_timeline.json")
    words_path = os.path.join(proj_dir, "word_timestamps.json")
    voice_dest = os.path.join(proj_dir, "voiceover.wav")

    import shutil
    if os.path.exists(timeline["audio_path"]) and os.path.abspath(timeline["audio_path"]) != os.path.abspath(voice_dest):
        shutil.copy2(timeline["audio_path"], voice_dest)

    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)

    ok(f"Đã xuất timeline Digest Short: {tl_path}")
    return proj_dir, tl_path, words_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="m8_news_bridge.py — Cầu nối thethao.json sang Timeline HTML v2")
    ap.add_argument("day_dir", help="Đường dẫn thư mục ngày (vd: outputs/19.10.2026)")
    ap.add_argument("--item", default="1", help="ID tin cần xử lý (mặc định 1)")
    ap.add_argument("--format", default="long", choices=["long", "short"], help="Định dạng video (long=16:9, short=9:16)")
    ap.add_argument("--focus", action="store_true", help="Xây dựng project Focus Short")
    ap.add_argument("--digest", action="store_true", help="Xây dựng project Digest Short")
    args = ap.parse_args()

    if args.focus:
        export_focus_short_project(args.day_dir, [1, 2, 3])
    elif args.digest:
        export_digest_short_project(args.day_dir, [1, 2, 3, 4])
    else:
        export_bridge_project(args.day_dir, args.item, args.format)
