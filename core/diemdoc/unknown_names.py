#!/usr/bin/env python3
"""
unknown_names.py — Quét kịch bản phát hiện các tên riêng thể thao chưa có trong từ điển
======================================================================================
Dùng hằng ngày để Agent tự động rà soát kịch bản và kiến nghị bổ sung từ điển phát âm.
Tiêu chí phát hiện:
- Token viết hoa không nằm ở đầu câu
- Chứa ký tự ngoại lai đặc trưng (w, z, j, f)
- Chứa ký tự có dấu đặc biệt ngoài bảng chữ tiếng Việt (é, ö, ü, ñ, ç, ø, å, etc.)
- Cụm từ viết hoa liền nhau chưa có trong data/pronunciation_sports.json
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import os
import re
from typing import List, Dict, Set

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.dirname(_HERE)
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from diemdoc import paths
from diemdoc.tts_text import load_pronunciation_dict

FOREIGN_LETTERS = set("wzjfWZJF")
EXTENDED_LATIN = set("àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệđìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ"
                     "ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆĐÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ")


def scan_unknown_names(text: str, dict_path: str | None = None) -> List[Dict[str, str]]:
    """Quét văn bản và trả về danh sách các tên riêng nghi ngờ chưa có trong từ điển."""
    entries = load_pronunciation_dict(dict_path)
    known_displays: Set[str] = {e["display"].strip().lower() for e in entries}

    # Tách các câu
    sentences = re.split(r'[\.\?!;\n]+', text)
    flagged: Dict[str, str] = {}

    for s in sentences:
        s_clean = s.strip()
        if not s_clean:
            continue
        words = [w for w in re.split(r'\s+', s_clean) if w]
        if not words:
            continue

        # Quét từng từ bắt đầu từ từ thứ 2 (bỏ qua từ đầu câu vì mặc định viết hoa)
        for i in range(len(words)):
            raw_w = words[i]
            w = re.sub(r'^[^\w]+|[^\w]+$', '', raw_w)
            if not w:
                continue

            # Bỏ qua từ đã có trong từ điển
            if w.lower() in known_displays:
                continue

            # Kiểm tra 1: Có chứa chữ cái ngoại lai (w, z, j, f)
            has_foreign = any(c in FOREIGN_LETTERS for c in w)
            
            # Kiểm tra 2: Viết hoa không phải đầu câu
            is_capitalized = (i > 0 and w[0].isupper() and not w.isupper())

            # Kiểm tra 3: Ký tự ngoài bảng chữ cái tiếng Việt cơ bản (ví dụ tiếng Bắc Âu/Tây Ban Nha: ö, ü, ñ, ø...)
            has_extended = any(ord(c) > 127 and c not in EXTENDED_LATIN for c in w)

            if has_foreign or is_capitalized or has_extended:
                reason = []
                if has_foreign:
                    reason.append("chứa ký tự w/z/j/f")
                if is_capitalized:
                    reason.append("viết hoa giữa câu")
                if has_extended:
                    reason.append("ký tự Latin mở rộng")
                flagged[w] = ", ".join(reason)

    result = [{"name": k, "reason": v} for k, v in sorted(flagged.items())]
    return result


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python3 unknown_names.py \"Văn bản kịch bản cần quét\"")
        print("      hoặc: python3 unknown_names.py path/to/script.txt")
        sys.exit(0)

    arg = sys.argv[1]
    if os.path.exists(arg):
        with open(arg, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = arg

    unknowns = scan_unknown_names(content)
    print(f"Phát hiện {len(unknowns)} từ nghi vấn chưa có trong từ điển:")
    for item in unknowns:
        print(f"  - {item['name']}: {item['reason']}")


if __name__ == "__main__":
    main()
