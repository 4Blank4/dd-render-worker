"""
Điểm Đọc — Core Data Contract (IR = Intermediate Representation)
=======================================================================
ĐÂY LÀ NGUỒN CHÂN LÝ DUY NHẤT của toàn hệ thống.

Mọi thứ khác — validator, timeline builder, render router, engines, QA —
đều đọc từ file này. Không module nào được phép định nghĩa lại schema.

Triết lý thiết kế:
  1. Timeline mô tả Ý ĐỊNH (intent), không mô tả DOM/CSS.
  2. Mọi thẻ (card) phải neo vào một từ thật trong script (semantic anchoring).
  3. Mọi thẻ phải khai báo engine render → cho phép lai HTML/Manim/GSAP.
  4. Schema là dữ liệu (dict), không phải class cứng → Agent đọc được,
     serialize ra JSON Schema được, và diff được giữa các version.

Cấu trúc file:
  - FORMATS / ENGINES / ROLES      : các enum hợp lệ
  - COMPONENTS                     : registry component (single source of truth)
  - TIMELINE_SCHEMA                : cấu trúc timeline
  - helpers: component_names(), component(), validate_*()
"""

from __future__ import annotations

SCHEMA_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# ENUMS — mọi giá trị hợp lệ trong hệ thống
# ---------------------------------------------------------------------------

# Định dạng khung hình
FORMATS = {
    "short": {"width": 1080, "height": 1920, "aspect": "9:16"},
    "long": {"width": 1920, "height": 1080, "aspect": "16:9"},
}

# Engine render. Mỗi card chọn 1 engine.
ENGINES = {
    "html": {
        "desc": "HTML/CSS + virtual-time shim. Engine mặc định, nhanh, đã kiểm chứng.",
        "renderer": "engines/html/renderer.py",
        "speed": "fast",
        "tua_duoc": True,
    },
    "gsap": {
        "desc": "HTML + GSAP timeline (seekable). Dùng cho animation phức tạp: morph, draw, stagger.",
        "renderer": "engines/html/renderer.py",
        "speed": "fast",
        "tua_duoc": True,
    },
    "d3": {
        "desc": "D3.js trong HTML. Dùng cho biểu đồ dữ liệu phức tạp.",
        "renderer": "engines/html/renderer.py",
        "speed": "fast",
        "tua_duoc": True,
    },
}

# Vai trò của một card trong nhịp kể chuyện (dùng cho pacing & QA)
ROLES = ("hook", "setup", "evidence", "turn", "payoff", "outro", "connective")

# Mức độ ưu tiên khi QA phát hiện quá tải thị giác
DENSITY = ("sparse", "normal", "dense")


# ---------------------------------------------------------------------------
# COMPONENTS — Registry component (single source of truth, thay "type hell")
# ---------------------------------------------------------------------------
# Mỗi component khai báo:
#   engine    : engine render mặc định (có thể override ở card)
#   roles     : vai trò kể chuyện phù hợp
#   fields    : lược đồ trường dữ liệu. {"name": FieldSpec}
#   required  : trường bắt buộc
#   density   : độ dày thị giác mặc định
#   sfx       : sfx mặc định khi reveal
#   min_gap   : khoảng cách tối thiểu (giây) so với card trước (chống dồn dập)
#   slot      : gợi ý vị trí trong bố cục ("full" | "half" | "third" | "any")
#
# FieldSpec = (type, required, ghi_chú)
#   type ∈ {str, int, float, bool, list, dict, "number", "colorname", "image"}
# ---------------------------------------------------------------------------

def _f(type_, required=True, note=""):
    return {"type": type_, "required": required, "note": note}


COMPONENTS: dict[str, dict] = {

    # ===================== KHUNG & NHỊP =====================
    "title-banner": {
        "engine": "html",
        "roles": ("setup", "connective"),
        "density": "sparse",
        "sfx": "whoosh_page.mp3",
        "min_gap": 0.3,
        "slot": "full",
        "fields": {
            "kicker": _f("str", False, "Nhãn nhỏ phía trên, ví dụ 'MATHEMATICAL ANOMALY'"),
            "tag": _f("str", False, "Alias của kicker"),
            "badge": _f("str", False, "Nhãn phụ cạnh kicker, ví dụ 'D. R. KAPREKAR • 1949'"),
            "title": _f("str", True, "Tiêu đề chính. Hỗ trợ *highlight* giữa hai dấu sao."),
            "pill_number": _f("str", False, "Số lớn hiển thị trong viên thuốc bên phải"),
        },
    },

    "kinetic-statement": {
        "engine": "gsap",
        "roles": ("hook", "turn", "payoff"),
        "density": "sparse",
        "sfx": "sub_drop_boom.mp3",
        "min_gap": 1.0,
        "slot": "full",
        "fields": {
            "lines": _f("list", True, "Danh sách dòng chữ, hiện lần lượt (stagger)"),
            "emphasis": _f("str", False, "Từ/dòng được nhấn mạnh cực đại"),
            "sub": _f("str", False, "Dòng phụ nhỏ bên dưới"),
        },
    },

    # ===================== CON SỐ =====================
    "giant-number-spotlight": {
        "engine": "html",
        "roles": ("hook", "evidence", "payoff"),
        "density": "sparse",
        "sfx": "tick_counter.mp3",
        "min_gap": 0.8,
        "slot": "half",
        "fields": {
            "value": _f("str", True, "Con số khổng lồ, ví dụ '6174' hoặc '99.94'"),
            "number": _f("str", False, "Alias của value"),
            "unit": _f("str", False, "Đơn vị, ví dụ 'YEARS' — hiển thị cạnh số"),
            "kicker": _f("str", False, "Nhãn nhỏ phía trên"),
            "badge": _f("str", False, "Nhãn phụ cạnh kicker"),
            "description": _f("str", False, "Mô tả 1-2 câu bên dưới con số"),
            "accent": _f("colorname", False, "gold | teal | ember (theo theme)"),
        },
    },

    "stat-callout": {
        "engine": "html",
        "roles": ("evidence", "payoff"),
        "density": "sparse",
        "sfx": "tick_counter.mp3",
        "min_gap": 0.8,
        "slot": "half",
        "fields": {
            "value": _f("str", True, "Số trung tâm"),
            "badge": _f("str", False, "Nhãn trên cùng"),
            "unit": _f("str", False, "Dòng giải thích ngay dưới số"),
            "subtitle": _f("str", False, "Mô tả dài hơn"),
            "accent": _f("colorname", False, ""),
        },
    },

    "stat-bento-trio": {
        "engine": "html",
        "roles": ("evidence", "setup"),
        "density": "normal",
        "sfx": "pop_card.mp3",
        "min_gap": 1.2,
        "slot": "full",
        "fields": {
            "items": _f("list", True, "Đúng 3 phần tử: [{value, title, sub, accent}]"),
        },
    },

    "dual-number-clash": {
        "engine": "html",
        "roles": ("turn", "evidence"),
        "density": "normal",
        "sfx": "whoosh_clean_1.mp3",
        "min_gap": 1.0,
        "slot": "full",
        "fields": {
            "left": _f("dict", True, "{label, value, sub, highlight}"),
            "right": _f("dict", True, "{label, value, sub, highlight}"),
            "verdict": _f("str", False, "Kết luận giữa hai bên"),
        },
    },

    "comparison-split": {
        "engine": "html",
        "roles": ("evidence", "turn"),
        "density": "normal",
        "sfx": "whoosh_clean_1.mp3",
        "min_gap": 1.0,
        "slot": "full",
        "fields": {
            "left": _f("dict", True, "{label, value, sub, highlight, valid_green}"),
            "right": _f("dict", True, "{label, value, sub, highlight}"),
        },
    },

    # ===================== TOÁN HỌC (đất diễn của Manim) =====================

    "math-pipeline": {
        "engine": "html",
        "roles": ("evidence",),
        "density": "normal",
        "sfx": "tick_counter.mp3",
        "min_gap": 1.5,
        "slot": "full",
        "fields": {
            "rows": _f("list", True, "[{step, equation, result, final}]"),
            "title": _f("str", False, ""),
        },
    },

    "math-equation-board": {
        "engine": "html",
        "roles": ("evidence", "setup"),
        "density": "normal",
        "sfx": "pop_card.mp3",
        "min_gap": 1.2,
        "slot": "full",
        "fields": {
            "parts": _f("list", True, "[{lhs, op, rhs}] hoặc chuỗi công thức"),
            "description": _f("str", False, ""),
        },
    },

    # ===================== BIỂU ĐỒ (D3) =====================
    "bar-chart": {
        "engine": "d3",
        "roles": ("evidence",),
        "density": "normal",
        "sfx": "pop_card.mp3",
        "min_gap": 1.2,
        "slot": "half",
        "fields": {
            "bars": _f("list", True, "[{label, value, highlight}]"),
            "unit": _f("str", False, "Đơn vị trục tung"),
        },
    },

    "line-chart": {
        "engine": "d3",
        "roles": ("evidence",),
        "density": "normal",
        "sfx": "pop_card.mp3",
        "min_gap": 1.2,
        "slot": "half",
        "fields": {
            "points": _f("list", True, "[{x, y, label}]"),
            "unit": _f("str", False, ""),
        },
    },

    "scale-ladder": {
        "engine": "html",
        "roles": ("evidence", "turn"),
        "density": "normal",
        "sfx": "tick_counter.mp3",
        "min_gap": 1.2,
        "slot": "half",
        "fields": {
            "rungs": _f("list", True, "[{label, value, active}]"),
        },
    },

    "progress-ring": {
        "engine": "html",
        "roles": ("evidence",),
        "density": "sparse",
        "sfx": "beep_retro_digital.mp3",
        "min_gap": 1.0,
        "slot": "third",
        "fields": {
            "percent": _f("float", True, "0..100"),
            "value": _f("str", False, "Nhãn giữa vòng"),
            "label": _f("str", False, ""),
        },
    },

    # ===================== SO SÁNH / XẾP HẠNG =====================
    "rank-table": {
        "engine": "html",
        "roles": ("evidence", "setup"),
        "density": "dense",
        "sfx": "strike_line.mp3",
        "min_gap": 1.5,
        "slot": "full",
        "fields": {
            "rows": _f("list", True, "[{rank, name, value, highlight}]"),
            "title": _f("str", False, ""),
        },
    },

    "grid-matrix": {
        "engine": "html",
        "roles": ("setup", "evidence"),
        "density": "normal",
        "sfx": "pop_card.mp3",
        "min_gap": 1.2,
        "slot": "full",
        "fields": {
            "items": _f("list", True, "[{value, hint, label}] — tối đa 6 ô"),
        },
    },

    "lineup-grid": {
        "engine": "html",
        "roles": ("evidence", "setup"),
        "density": "dense",
        "sfx": "pop_card.mp3",
        "min_gap": 1.5,
        "slot": "full",
        "fields": {
            "heroes": _f("list", True, "[{name, number, role, image}]"),
            "kicker": _f("str", False, ""),
        },
    },

    # ===================== NHÂN VẬT =====================
    "portrait-hero-card": {
        "engine": "html",
        "roles": ("setup", "payoff"),
        "density": "sparse",
        "sfx": "chimes_reveal.mp3",
        "min_gap": 1.0,
        "slot": "half",
        "fields": {
            "name": _f("str", True, ""),
            "kicker": _f("str", False, ""),
            "subtitle": _f("str", False, ""),
            "stamp_number": _f("str", False, "Số đóng dấu lên ảnh"),
            "stamp_label": _f("str", False, ""),
            "image": _f("image", True, "Đường dẫn tương đối trong project, ví dụ 'images_ready/a.jpg'"),
            "caption_tag": _f("str", False, ""),
            "footer_left": _f("str", False, ""),
            "footer_right": _f("str", False, ""),
        },
    },

    "photo-card": {
        "engine": "html",
        "roles": ("evidence", "setup"),
        "density": "sparse",
        "sfx": "paper_slide_page.mp3",
        "min_gap": 1.0,
        "slot": "half",
        "fields": {
            "image": _f("image", True, ""),
            "kicker": _f("str", False, ""),
            "title": _f("str", False, ""),
            "number": _f("str", False, ""),
            "caption": _f("str", False, ""),
            "credit": _f("str", False, "Nguồn ảnh — BẮT BUỘC điền nếu ảnh không tự tạo"),
        },
    },

    # ===================== VĂN BẢN =====================
    "fact-list": {
        "engine": "html",
        "roles": ("setup", "evidence"),
        "density": "dense",
        "sfx": "pop_card.mp3",
        "min_gap": 1.2,
        "slot": "half",
        "fields": {
            "items": _f("list", True, "Danh sách chuỗi hoặc {text, highlight}"),
            "title": _f("str", False, ""),
        },
    },

    "quote-card": {
        "engine": "html",
        "roles": ("turn", "payoff"),
        "density": "sparse",
        "sfx": "chimes_reveal.mp3",
        "min_gap": 1.2,
        "slot": "half",
        "fields": {
            "quote": _f("str", True, ""),
            "text": _f("str", False, "Alias của quote"),
            "author": _f("str", False, ""),
            "role": _f("str", False, ""),
        },
    },

    "three-pillars": {
        "engine": "html",
        "roles": ("setup", "connective"),
        "density": "normal",
        "sfx": "pop_card.mp3",
        "min_gap": 1.2,
        "slot": "full",
        "fields": {
            "pillars": _f("list", True, "Đúng 3 phần tử: [{icon, title, sub}]"),
        },
    },
}


def component_names() -> list[str]:
    return sorted(COMPONENTS.keys())


def component(name: str) -> dict | None:
    return COMPONENTS.get(name)


def components_for_engine(engine: str) -> list[str]:
    return sorted(n for n, c in COMPONENTS.items() if c.get("engine") == engine)


# ---------------------------------------------------------------------------
# TIMELINE SCHEMA
# ---------------------------------------------------------------------------

TIMELINE_SCHEMA = {
    "type": "object",
    "required": ["schema_version", "format", "template", "output_filename", "scenes"],
    "properties": {
        "schema_version": {"type": "str", "note": "Phiên bản contract, hiện tại " + SCHEMA_VERSION},
        "project_name": {"type": "str"},
        "channel_name": {"type": "str"},
        "topic": {"type": "str", "note": "Chủ đề gốc — dùng cho metadata & SEO"},
        "format": {"type": "enum", "values": list(FORMATS.keys())},
        "template": {"type": "str", "note": "Tên file trong templates/, ví dụ 'short_swiss.html'"},
        "brand": {"type": "str", "note": "Tên brand/theme trong design/brands/"},
        "output_filename": {"type": "str", "note": "Tên file ra, KHÔNG dấu, nối gạch ngang"},
        "bgm": {"type": "str", "note": "Tên file trong assets/bgm/"},
        "bgm_volume": {"type": "float", "note": "Mặc định 0.08"},
        "enable_sfx": {"type": "bool"},
        "karaoke_enabled": {"type": "bool"},
        "voice_config": {
            "type": "dict",
            "note": "{voice, speed} — xem assets/voice_samples/",
        },
        "chapter_ribbon": {
            "type": "list",
            "note": "[{chap_id, name, number}] — dải chương cho long-form",
        },
        "scenes": {"type": "list", "note": "Danh sách Scene (xem SCENE_SCHEMA)"},
        "sources": {"type": "list", "note": "[{title, url}] — nguồn tham khảo, cho fact-check"},
    },
}

SCENE_SCHEMA = {
    "type": "object",
    "required": ["scene_id", "script_text", "cards"],
    "properties": {
        "scene_id": {"type": "int"},
        "title": {"type": "str", "note": "Tiêu đề nội bộ, không hiển thị"},
        "script_text": {"type": "str", "note": "Lời thoại tiếng Anh. Hỗ trợ [PAUSE 0.5]"},
        "chapter_id": {"type": "int", "note": "Thuộc chương nào (long-form)"},
        "transition": {
            "type": "enum",
            "values": ["wipe", "slit", "iris", "fade", "glitch", "none"],
        },
        "wipe_label": {"type": "str"},
        "layout": {"type": "enum", "values": ["grid", "full", "stack"]},
        "portrait": {"type": "dict", "note": "Cột ảnh nhân vật (long-form): xem portrait-hero-card"},
        "cards": {"type": "list", "note": "Danh sách Card (xem CARD_SCHEMA)"},
        # --- các trường do audio/sync GHI NGƯỢC, không viết tay ---
        "_start_time": {"type": "float", "note": "[derived] do m3/m5 ghi"},
        "_duration": {"type": "float", "note": "[derived] do m3/m5 ghi"},
    },
}

CARD_SCHEMA = {
    "type": "object",
    "required": ["id", "type", "trigger_word"],
    "properties": {
        "id": {"type": "str", "note": "Định danh duy nhất trong scene, ví dụ 's1_tiles'"},
        "type": {"type": "enum", "values": component_names()},
        "engine": {"type": "enum", "values": list(ENGINES.keys()), "note": "Override engine mặc định của component"},
        "role": {"type": "enum", "values": list(ROLES)},
        "trigger_word": {
            "type": "str",
            "note": "TỪ KHÓA NEO THỜI GIAN — bắt buộc, phải tồn tại nguyên văn trong script_text",
        },
        "local_delay": {"type": "float", "note": "Fallback nếu không khớp trigger_word (giây, tính từ đầu scene)"},
        "lock_timing": {"type": "bool", "note": "true = tôn trọng local_delay tuyệt đối"},
        "sfx": {"type": "str", "note": "Override sfx mặc định của component"},
        "span": {"type": "enum", "values": [4, 6, 8, 12], "note": "Số cột trong lưới 12 (long-form)"},
        "accent": {"type": "colorname"},
        # --- dữ liệu riêng của component nằm ở đây ---
        "_data": {"type": "any", "note": "Các trường còn lại theo COMPONENTS[type].fields"},
        # --- do sync ghi ngược ---
        "_reveal_time": {"type": "float", "note": "[derived]"},
    },
}


# ---------------------------------------------------------------------------
# VALIDATION HELPERS — dùng chung cho m0 (schema) và m2 (builder)
# ---------------------------------------------------------------------------

def validate_card(card: dict, scene_words: set[str] | None = None) -> list[str]:
    """Trả về danh sách lỗi (rỗng = hợp lệ). Không raise."""
    errors: list[str] = []
    cid = card.get("id", "?")

    ctype = card.get("type")
    if not ctype:
        errors.append(f"Card '{cid}': thiếu 'type'.")
        return errors

    spec = COMPONENTS.get(ctype)
    if spec is None:
        errors.append(
            f"Card '{cid}': type '{ctype}' không tồn tại trong registry. "
            f"Hợp lệ: {', '.join(component_names())}"
        )
        return errors

    # 1. Trường bắt buộc của component
    for fname, fspec in spec["fields"].items():
        if fspec["required"] and not card.get(fname) and not card.get("_" + fname):
            # alias: 'number' là alias của 'value', 'text' của 'quote', 'tag' của 'kicker'
            if not _alias_present(card, fname):
                errors.append(f"Card '{cid}' ({ctype}): thiếu trường bắt buộc '{fname}'.")

    # 2. Semantic anchoring
    tw = card.get("trigger_word")
    if not tw and not card.get("lock_timing"):
        errors.append(
            f"Card '{cid}' ({ctype}): thiếu 'trigger_word'. "
            f"Mọi card phải neo vào một từ trong script (hoặc đặt lock_timing=true)."
        )
    elif tw and scene_words is not None:
        tokens = [_norm(t) for t in str(tw).split() if _norm(t)]
        if tokens and not all(t in scene_words for t in tokens):
            missing = [t for t in tokens if t not in scene_words]
            errors.append(
                f"Card '{cid}' ({ctype}): trigger_word '{tw}' chứa từ không có trong script_text: "
                f"{', '.join(missing)}"
            )

    # 3. Engine hợp lệ
    eng = card.get("engine", spec.get("engine", "html"))
    if eng not in ENGINES:
        errors.append(f"Card '{cid}': engine '{eng}' không hợp lệ.")

    # 4. Kiểm tra số phần tử của list có ràng buộc
    if ctype == "stat-bento-trio":
        items = card.get("items") or []
        if len(items) != 3:
            errors.append(f"Card '{cid}' (stat-bento-trio): 'items' phải có đúng 3 phần tử, đang có {len(items)}.")
    if ctype == "three-pillars":
        p = card.get("pillars") or []
        if len(p) != 3:
            errors.append(f"Card '{cid}' (three-pillars): 'pillars' phải có đúng 3 phần tử, đang có {len(p)}.")
    if ctype == "grid-matrix":
        items = card.get("items") or []
        if len(items) > 6:
            errors.append(f"Card '{cid}' (grid-matrix): tối đa 6 ô, đang có {len(items)}.")

    # 5. Ảnh phải là đường dẫn tương đối trong project
    for fname, fspec in spec["fields"].items():
        if fspec["type"] == "image" and card.get(fname):
            val = str(card[fname])
            if val.startswith(("http://", "https://", "/")):
                errors.append(
                    f"Card '{cid}': ảnh phải là đường dẫn tương đối trong project "
                    f"(ví dụ 'images_ready/x.jpg'), đang là '{val}'."
                )

    # 6. Ảnh nhân vật nên có credit nếu không tự tạo
    if ctype == "photo-card" and card.get("image") and not card.get("credit"):
        errors.append(f"Card '{cid}' (photo-card): nên có 'credit' (nguồn ảnh) để tránh rủi ro bản quyền.")

    return errors


_ALIASES = {
    "value": ("number",),
    "number": ("value",),
    "quote": ("text",),
    "text": ("quote",),
    "kicker": ("tag",),
    "tag": ("kicker",),
    "description": ("subtitle", "sub"),
}


def _alias_present(card: dict, fname: str) -> bool:
    return any(card.get(a) for a in _ALIASES.get(fname, ()))


def _norm(w: str) -> str:
    import re
    import unicodedata
    return unicodedata.normalize("NFC", re.sub(r"^[^\w\d]+|[^\w\d]+$", "", str(w).strip(), flags=re.UNICODE).lower())


def validate_timeline(tl: dict) -> tuple[list[str], list[str]]:
    """Trả về (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    for key in TIMELINE_SCHEMA["required"]:
        if not tl.get(key):
            errors.append(f"Timeline: thiếu trường bắt buộc '{key}'.")

    fmt = tl.get("format")
    if fmt and fmt not in FORMATS:
        errors.append(f"Timeline: format '{fmt}' không hợp lệ (dùng 'short' hoặc 'long').")

    ofn = tl.get("output_filename", "")
    if ofn and (not ofn.endswith(".mp4") or " " in ofn or any(ord(c) > 127 for c in ofn)):
        warnings.append(
            f"Timeline: output_filename '{ofn}' nên là ASCII không dấu, không khoảng trắng, kết thúc .mp4."
        )

    scenes = tl.get("scenes") or []
    if not scenes:
        errors.append("Timeline: không có scene nào.")
        return errors, warnings

    seen_ids: set[str] = set()
    total_words = 0

    for i, sc in enumerate(scenes):
        sid = sc.get("scene_id", i + 1)
        script = (sc.get("script_text") or "").strip()
        words = script.split()
        total_words += len(words)

        if len(words) < 3:
            warnings.append(f"Scene {sid}: script quá ngắn (<3 từ), TTS dễ lỗi.")

        cards_key = "cards" if "cards" in sc else "steps"
        cards = sc.get(cards_key) or []
        if not cards:
            warnings.append(f"Scene {sid}: không có card nào.")

        # mật độ
        est_dur = len(words) / 2.5 if words else 0
        if cards and est_dur > 0:
            sec_per_card = est_dur / len(cards)
            if sec_per_card < 1.5:
                warnings.append(
                    f"Scene {sid}: mật độ card quá dày ({len(cards)} card / ~{est_dur:.1f}s). "
                    f"Khán giả không kịp đọc."
                )

        scene_words = {_norm(w) for w in words}
        prev_trigger_idx = -1
        for c in cards:
            cid = c.get("id", "?")
            if cid in seen_ids:
                errors.append(f"Scene {sid}: id card '{cid}' bị trùng trong toàn timeline.")
            seen_ids.add(cid)
            errors.extend(f"Scene {sid}: {e}" for e in validate_card(c, scene_words))

            # kiểm tra thứ tự trigger_word khớp thứ tự xuất hiện trong script
            tw = c.get("trigger_word")
            if tw:
                idx = _find_phrase_index(words, tw)
                if idx is not None:
                    if idx < prev_trigger_idx:
                        warnings.append(
                            f"Scene {sid}, card '{cid}': trigger_word '{tw}' xuất hiện TRƯỚC card liền trước "
                            f"trong script → thẻ sẽ hiện sai thứ tự."
                        )
                    prev_trigger_idx = max(prev_trigger_idx, idx)

    est_min = total_words / 150 if total_words else 0
    if est_min > 0:
        warnings.append(f"__info__ Tổng {total_words} từ (~{est_min:.1f} phút đọc).")

    return errors, warnings


def _find_phrase_index(words: list[str], phrase: str) -> int | None:
    toks = [_norm(t) for t in str(phrase).split() if _norm(t)]
    if not toks:
        return None
    nwords = [_norm(w) for w in words]
    for i in range(len(nwords) - len(toks) + 1):
        if nwords[i:i + len(toks)] == toks:
            return i
    return None


# ---------------------------------------------------------------------------
# JSON SCHEMA EXPORT — cho LLM structured output
# ---------------------------------------------------------------------------

def to_json_schema() -> dict:
    """
    Sinh JSON Schema (draft-07) từ registry.
    Dùng để ép LLM (Claude structured output) chỉ sinh timeline hợp lệ.
    """
    card_props: dict = {
        "id": {"type": "string"},
        "type": {"type": "string", "enum": component_names()},
        "engine": {"type": "string", "enum": list(ENGINES.keys())},
        "role": {"type": "string", "enum": list(ROLES)},
        "trigger_word": {"type": "string"},
        "local_delay": {"type": "number"},
        "lock_timing": {"type": "boolean"},
        "sfx": {"type": "string"},
        "span": {"type": "integer", "enum": [4, 6, 8, 12]},
        "accent": {"type": "string"},
    }
    # gộp toàn bộ field của mọi component (union) — LLM thấy được mọi trường có thể dùng
    union_fields: dict = {}
    for cname, spec in COMPONENTS.items():
        for fname, fspec in spec["fields"].items():
            union_fields.setdefault(fname, fspec["note"])
    for fname, note in union_fields.items():
        if fname not in card_props:
            card_props[fname] = {"type": "string", "description": note}

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "By-DD-The-thao Timeline",
        "type": "object",
        "required": TIMELINE_SCHEMA["required"],
        "properties": {
            "schema_version": {"type": "string"},
            "project_name": {"type": "string"},
            "channel_name": {"type": "string"},
            "topic": {"type": "string"},
            "format": {"type": "string", "enum": list(FORMATS.keys())},
            "template": {"type": "string"},
            "brand": {"type": "string"},
            "output_filename": {"type": "string"},
            "bgm": {"type": "string"},
            "bgm_volume": {"type": "number"},
            "enable_sfx": {"type": "boolean"},
            "karaoke_enabled": {"type": "boolean"},
            "voice_config": {
                "type": "object",
                "properties": {"voice": {"type": "string"}, "speed": {"type": "number"}},
            },
            "chapter_ribbon": {"type": "array"},
            "sources": {"type": "array"},
            "scenes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["scene_id", "script_text", "cards"],
                    "properties": {
                        "scene_id": {"type": "integer"},
                        "title": {"type": "string"},
                        "script_text": {"type": "string"},
                        "chapter_id": {"type": "integer"},
                        "transition": {"type": "string", "enum": ["wipe", "slit", "iris", "fade", "glitch", "none"]},
                        "wipe_label": {"type": "string"},
                        "layout": {"type": "string", "enum": ["grid", "full", "stack"]},
                        "portrait": {"type": "object"},
                        "cards": {"type": "array", "items": {"type": "object", "properties": card_props}},
                    },
                },
            },
        },
    }


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--json-schema":
        print(json.dumps(to_json_schema(), indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "--list":
        by_engine: dict[str, list[str]] = {}
        for name, spec in sorted(COMPONENTS.items()):
            by_engine.setdefault(spec["engine"], []).append(name)
        for eng, names in sorted(by_engine.items()):
            print(f"\n[{eng}] ({len(names)})")
            for n in names:
                print(f"  - {n:28s} slot={COMPONENTS[n]['slot']:6s} density={COMPONENTS[n]['density']}")
        print(f"\nTổng: {len(COMPONENTS)} component / {len(ENGINES)} engine")
    else:
        print(f"By-DD-The-thao schema v{SCHEMA_VERSION}")
        print(f"  {len(COMPONENTS)} components, {len(ENGINES)} engines, {len(FORMATS)} formats")
        print("  --list         liệt kê component theo engine")
        print("  --json-schema  xuất JSON Schema cho LLM")