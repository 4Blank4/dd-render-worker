"""
tts_text.py — Chuẩn hóa văn bản cho mô hình ViTTS (tiếng Việt) & Ánh xạ ngược
=============================================================================
Đặc điểm kỹ thuật cho kênh Điểm Đọc (DD-The-thao):
  1. Thay thế tên cầu thủ, HLV, CLB, giải đấu ngoại quốc sang phiên âm tiếng Việt tự nhiên.
  2. Khớp không phân biệt dấu phụ (accent-insensitive matching, e.g. Mbappe / Mbappé).
  3. Gắn cờ "group": true cho các thực thể để phụ đề Karaoke tô sáng cả cụm.
  4. Trả về token_map ánh xạ 1-1 hoặc 1-n giữa từ hiển thị (display) và token đọc (say).
  5. Dấu câu được đính trực tiếp vào token trước đó, không sinh token rỗng gây lệch mốc giờ.
"""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from typing import List, Dict, Any, Tuple

from .log import log, warn
from .paths import DATA

sys.dont_write_bytecode = True

CHAR_MAP = {
    'a': '[aàáảãạăằắẳẵặâầấẩẫậäåæáàã]',
    'e': '[eèéẻẽẹêềếểễệëéè]',
    'i': '[iìíỉĩịïíì]',
    'o': '[oòóỏõọôồốổỗộơờớởỡợöőøóò]',
    'u': '[uùúủũụưừứửữựüűúù]',
    'y': '[yỳýỷỹỵÿý]',
    'c': '[cç]',
    'n': '[nñ]',
    'd': '[dđð]',
}


def make_accent_insensitive_regex(term: str) -> str:
    """Tạo regex pattern không phân biệt dấu phụ cho tên nước ngoài (e.g. Mbappe -> Mbappé)."""
    base = ''.join(c for c in unicodedata.normalize('NFD', term) if unicodedata.category(c) != 'Mn')
    parts = []
    for ch in base:
        cl = ch.lower()
        if cl in CHAR_MAP:
            v_pat = CHAR_MAP[cl]
            parts.append(v_pat.upper() if ch.isupper() else v_pat)
        else:
            parts.append(re.escape(ch))
    return ''.join(parts)


def load_pronunciation_dict(dict_path: str | None = None) -> List[Dict[str, Any]]:
    """
    Nạp từ điển phát âm thể thao từ data/pronunciation_sports.json.
    File có cấu trúc: {"clubs": [...], "players": [...], "coaches": [...], ...}
    Trả về danh sách phẳng các entry được chuẩn hóa.
    """
    path = dict_path or os.path.join(DATA, "pronunciation_sports.json")
    if not os.path.exists(path):
        warn(f"Không tìm thấy file từ điển tại: {path}")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        warn(f"Lỗi đọc từ điển phát âm {path}: {e}")
        return []

    entries: List[Dict[str, Any]] = []

    # Duyệt qua các nhóm trong JSON (clubs, players, coaches, competitions, terms, acronyms)
    if isinstance(data, dict):
        for category, item_list in data.items():
            if category.startswith("_"):
                continue
            if isinstance(item_list, list):
                for item in item_list:
                    if isinstance(item, dict) and "display" in item and "say" in item:
                        item_copy = dict(item)
                        item_copy.setdefault("category", category)
                        item_copy.setdefault("group", False)
                        item_copy["is_foreign_name"] = True
                        entries.append(item_copy)
    elif isinstance(data, list):
        for e in data:
            if isinstance(e, dict) and "display" in e and "say" in e:
                item_copy = dict(e)
                item_copy["is_foreign_name"] = True
                entries.append(item_copy)

    return entries


def load_abbreviations_dict(dict_path: str | None = None) -> List[Dict[str, Any]]:
    """
    Nạp từ điển viết tắt thể thao & thời sự từ data/abbreviations_map.json.
    Các từ viết tắt này (VĐQG, ĐTQG, Cúp QG, CAHN, SLNA, BXH...) luôn được áp dụng
    để mô hình ViTTS đọc thành tiếng rõ ràng, trong khi trên màn hình vẫn giữ
    nguyên dạng chữ viết tắt gọn gàng.
    """
    path = dict_path or os.path.join(DATA, "abbreviations_map.json")
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        abbrs = data.get("abbreviations", [])
        seen = set()
        deduped = []
        for e in abbrs:
            if isinstance(e, dict) and "display" in e and "say" in e:
                disp = e["display"].strip()
                if disp not in seen:
                    seen.add(disp)
                    item = dict(e)
                    item["is_abbreviation"] = True
                    deduped.append(item)
        return deduped
    except Exception as e:
        warn(f"Lỗi đọc từ điển viết tắt {path}: {e}")
        return []


def is_auto_transliterate_enabled() -> bool:
    """
    Kiểm tra cấu hình tự động phiên âm từ config/voice.json.
    Theo quy chuẩn cập nhật ngày 24.10.2026: Mặc định là FALSE (không tự ý phiên âm,
    giữ nguyên tên gốc tiếng Anh/quốc tế cho ViTTS v3turbo đọc tự nhiên).
    Chỉ phiên âm khi người dùng yêu cầu đích danh cho từ cụ thể.
    """
    try:
        cfg_path = os.path.join(os.path.dirname(DATA), "config", "voice.json")
        if os.path.exists(cfg_path):
            with open(cfg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return bool(data.get("auto_transliterate", False))
    except Exception:
        pass
    return False


def prepare(
    display_text: str,
    dict_path: str | None = None,
    auto_transliterate: bool | None = None,
    manual_overrides: Dict[str, str] | None = None
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Chuẩn hóa văn bản kịch bản cho ViTTS và xây dựng token_map.
    
    Quy tắc cốt lõi (Cập nhật 24.10.2026):
      - auto_transliterate=False (Mặc định): KHÔNG tự ý phiên âm tên cầu thủ, CLB, giải đấu,
        giữ nguyên từ gốc (Kylian Mbappé, Lionel Messi, Real Madrid, Palladium...) để mô hình
        ViTTS đọc trực tiếp chuẩn xác và tự nhiên hơn.
      - manual_overrides: Chỉ phiên âm các từ được người dùng yêu cầu đích danh.
    
    Trả về:
      - tts_text: chuỗi văn bản hoàn chỉnh chuyển cho mô hình ViTTS đọc
      - token_map: danh sách ánh xạ từng phần tử hiển thị sang các token TTS
    """
    if not display_text or not display_text.strip():
        return "", []

    if auto_transliterate is None:
        auto_transliterate = is_auto_transliterate_enabled()

    # Chuẩn hóa quy chuẩn số Việt Nam: 1400, không viết 1.400 (tránh ViTTS đọc sai "chấm" hoặc ngắt câu)
    text = re.sub(r'(?<=\d)\.(?=\d{3}\b)', '', display_text)

    # Chuẩn hóa quy chuẩn tiền tệ USD: $100000 -> 100000 USD, 100000$ -> 100000 USD
    text = re.sub(r'\$(\d+)', r'\1 USD', text)
    text = re.sub(r'(?<=\d)\$', ' USD', text)
    text = re.sub(r'(?<=\d)(USD)\b', r' \1', text, flags=re.IGNORECASE)
    entries: List[Dict[str, Any]] = []

    # 1. Nạp từ điển viết tắt bắt buộc (chuẩn hóa phát âm các từ viết tắt tiếng Việt/thể thao)
    abbr_entries = load_abbreviations_dict()

    # 2. Nạp manual overrides nếu có (người dùng yêu cầu đích danh, ưu tiên cao nhất)
    if manual_overrides and isinstance(manual_overrides, dict):
        override_keys = {k.strip().lower() for k in manual_overrides.keys()}
        abbr_entries = [e for e in abbr_entries if e["display"].strip().lower() not in override_keys]
        for disp_k, say_v in manual_overrides.items():
            entries.append({
                "display": disp_k,
                "say": say_v,
                "group": False,
                "category": "manual_override"
            })

    entries.extend(abbr_entries)

    # 3. Nạp từ điển phiên âm tên riêng nước ngoài (nếu bật)
    if auto_transliterate:
        entries.extend(load_pronunciation_dict(dict_path))

    # Nếu không có từ điển phiên âm nào cần áp dụng, giữ nguyên văn bản gốc
    if not entries:
        token_map: List[Dict[str, Any]] = []
        tts_segments: List[str] = []
        _process_unmatched_span(text, token_map, tts_segments)
        tts_text = " ".join(tts_segments)
        tts_text = re.sub(r'\s+', ' ', tts_text).strip()
        return tts_text, token_map

    # 2. Tìm các vùng khớp từ điển (nếu có overrides hoặc bật auto_transliterate)
    matches = []
    for entry in entries:
        disp = entry["display"]
        is_foreign = entry.get("is_foreign_name", False)

        # 1. Với tên riêng nước ngoài (chỉ nạp khi bật auto_transliterate=True):
        #    Dùng make_accent_insensitive_regex để không phân biệt dấu phụ (e.g. Mbappe -> Mbappé).
        # 2. Với TẤT CẢ từ viết tắt (abbreviations_map.json) và manual_overrides:
        #    TUYỆT ĐỐI KHÔNG dùng make_accent_insensitive_regex (tránh biến 'u' thành '[uùúủũụưừứửữự]'
        #    khiến chữ viết tắt 'MU' bị khớp nhầm sang các từ tiếng Việt như 'mũ', 'mù', 'mủ', 'mu'...).
        if is_foreign:
            disp_regex = make_accent_insensitive_regex(disp)
            flags = re.IGNORECASE
        else:
            disp_regex = re.escape(disp)
            # Với từ viết tắt chữ hoa ngắn (<= 4 ký tự như MU, CK, BK, TK, TM, HV, TV, TĐ, KO, WC, USD, CLB, VFF, HLV...)
            # bắt buộc phân biệt hoa thường (case-sensitive) để không nhận nhầm từ tiếng Việt viết thường (như 'mu bàn chân', 'ko' trong teen code).
            if disp.isupper() and len(disp) <= 4:
                flags = 0
            else:
                flags = re.IGNORECASE

        pattern = re.compile(r'(?<!\w)' + disp_regex + r'(?!\w)', flags)
        for m in pattern.finditer(text):
            matches.append({
                "start": m.start(),
                "end": m.end(),
                "display": text[m.start():m.end()],
                "say": entry["say"],
                "group": entry.get("group", False)
            })

    # Giải quyết xung đột (non-overlapping greedy matches)
    matches.sort(key=lambda x: (x["start"], -(x["end"] - x["start"])))
    filtered_matches = []
    last_end = 0
    for m in matches:
        if m["start"] >= last_end:
            filtered_matches.append(m)
            last_end = m["end"]

    # 3. Xây dựng token_map và chuỗi tts_text
    token_map: List[Dict[str, Any]] = []
    tts_segments: List[str] = []
    cursor = 0
    group_counter = 0

    for m in filtered_matches:
        if m["start"] > cursor:
            interim = text[cursor:m["start"]]
            _process_unmatched_span(interim, token_map, tts_segments)

        say_text = m["say"]
        disp_text = m["display"]
        say_tokens = [w for w in re.split(r'\s+', say_text) if w]
        group_id = None
        if m["group"]:
            group_counter += 1
            group_id = group_counter

        token_map.append({
            "display": disp_text,
            "say": say_text,
            "tts_tokens": say_tokens,
            "group": m["group"],
            "group_id": group_id,
            "is_dict_match": True
        })
        tts_segments.append(say_text)
        cursor = m["end"]

    if cursor < len(text):
        trailing = text[cursor:]
        _process_unmatched_span(trailing, token_map, tts_segments)

    tts_text = " ".join(tts_segments)
    tts_text = re.sub(r'\s+', ' ', tts_text).strip()

    return tts_text, token_map


def _process_unmatched_span(span_text: str, token_map: List[Dict[str, Any]], tts_segments: List[str]) -> None:
    """Xử lý đoạn văn bản không khớp từ điển, đính dấu câu vào token đứng trước nếu có."""
    words = [w for w in re.split(r'\s+', span_text) if w]
    for w in words:
        # Nếu từ thuần là dấu câu (ví dụ "." hoặc "," hoặc ";")
        if re.match(r'^[,\.\?!;:]+$', w):
            if token_map:
                token_map[-1]["display"] += w
                token_map[-1]["say"] += w
                if tts_segments:
                    tts_segments[-1] += w
            continue

        # Tách dấu câu cuối từ nếu có (ví dụ 'Arteta,' -> word='Arteta', punct=',')
        m_punct = re.match(r'^(.*?)([,\.\?!;:]+)$', w)
        if m_punct:
            base_word = m_punct.group(1)
            punct = m_punct.group(2)
        else:
            base_word = w
            punct = ""

        if not base_word:
            if punct and token_map:
                token_map[-1]["display"] += punct
                token_map[-1]["say"] += punct
                if tts_segments:
                    tts_segments[-1] += punct
            continue

        # Kiểm tra đơn vị tiền tệ USD nếu chưa khớp từ điển (quy chuẩn đọc thành 'đô')
        say_word = base_word
        is_grouped = False
        if base_word.upper() == "USD":
            say_word = "đô"
            is_grouped = True
        elif m_score := re.match(r'^(\d+)-(\d+)$', base_word):
            digits_vn = {
                '0': 'không', '1': 'một', '2': 'hai', '3': 'ba', '4': 'bốn',
                '5': 'năm', '6': 'sáu', '7': 'bảy', '8': 'tám', '9': 'chín'
            }
            d1, d2 = m_score.group(1), m_score.group(2)
            w1 = digits_vn.get(d1, d1)
            w2 = digits_vn.get(d2, d2)
            say_word = f"{w1} {w2}"
            is_grouped = True
        else:
            m_pct = re.match(r'^(\d+)%$', base_word)
            if m_pct:
                say_word = f"{m_pct.group(1)} phần trăm"
                is_grouped = True

        say_tokens = [t for t in re.split(r'\s+', say_word) if t]
        token_map.append({
            "display": w,
            "say": say_word + punct,
            "tts_tokens": say_tokens,
            "group": is_grouped,
            "group_id": f"num_{len(token_map)}" if is_grouped else None,
            "is_dict_match": False
        })
        tts_segments.append(say_word + punct)
