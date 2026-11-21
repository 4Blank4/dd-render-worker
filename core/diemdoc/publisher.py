#!/usr/bin/env python3
"""
core/diemdoc/publisher.py — Trung tâm Chuẩn Hóa Xuất Bản cho Kênh "Điểm Đọc" (DD-The-thao)

Đảm bảo tính thống nhất 100% giữa 3 Loại Video của hệ thống:
1. Loại 1 (`weekly_digest` — 16:9): Video tổng hợp thông tin thể thao hằng tuần / hằng ngày (20-25 tin).
2. Loại 2 (`thematic_long` — 16:9): Video dài chuyên đề nhân vật / sự kiện / thống kê dữ liệu theo yêu cầu riêng.
3. Loại 3 (`short_news` — 9:16): Video ngắn dạng tin tức hằng ngày (1 tin đột xuất `outputs/Orther/...`,
   Focus Short gộp 2-5 tin từ bản tin dài, hoặc Digest Short 25 tin đọc nhanh).

Chuẩn hóa đồng bộ:
- Cấu hình giọng đọc chuẩn từ `config/voice.json` (Nam: Minh Quân Pro spd 1.12, pch 0.93, temp 0.6;
  Nữ: Ngọc Huyền spd 1.12, pch 1.10, temp 0.5).
- Cấu trúc `mota.txt` 2 phần duy nhất (`=== TIÊU ĐỀ YOUTUBE ===` và `=== MÔ TẢ VIDEO ===`),
  tuân thủ chuẩn chính tả tiếng Việt Sentence Case <= 100 ký tự.
- Ảnh bìa ngang 16:9 (`templates/thumbnail_16x9_sports.html` — 3 phương án A/B/C) và
  Ảnh bìa dọc 9:16 (`templates/thumbnail_9x16_sports.html`) đồng bộ nhận diện Cyber-Stadium Electric Cyan (`#00E5FF`).
"""
import sys
sys.dont_write_bytecode = True

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from . import paths
from .jsonio import load_json
from .log import ok, warn


# ─────────────────────────────────────────────────────────────────────────────
# 1. CHUẨN HÓA CẤU HÌNH GIỌNG ĐỌC TỪ config/voice.json
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_PRIMARY_VOICE = {
    "voice_id": "Minh Quân Pro",
    "voice_label": "Minh Quân Pro (Mẫu 15)",
    "speed": 1.12,
    "pitch": 0.93,
    "temperature": 0.6,
}

DEFAULT_SECONDARY_VOICE = {
    "voice_id": "Ngọc Huyền",
    "voice_label": "Ngọc Huyền (Mẫu 14)",
    "speed": 1.12,
    "pitch": 1.10,
    "temperature": 0.5,
}


def load_voice_preset(preset: str = "primary") -> Dict[str, Any]:
    """
    Đọc cấu hình giọng đọc chuẩn từ `config/voice.json`.
    - `preset="primary"` (mặc định): Nam chính Minh Quân Pro (Mẫu 15) — speed 1.12, pitch 0.93, temp 0.6.
    - `preset="secondary"` (hoặc `"female"`): Nữ Ngọc Huyền (Mẫu 14) — speed 1.12, pitch 1.10, temp 0.5.
    """
    cfg_path = Path(paths.ROOT) / "config" / "voice.json"
    if cfg_path.exists():
        try:
            cfg = load_json(cfg_path)
            presets = cfg.get("presets", {})
            if preset in ("secondary", "female", "nu"):
                sec = presets.get("secondary") or cfg.get("secondary_female_preset") or {}
                return {
                    "voice_id": sec.get("voice", sec.get("voice_id", DEFAULT_SECONDARY_VOICE["voice_id"])),
                    "voice_label": sec.get("voice_label", DEFAULT_SECONDARY_VOICE["voice_label"]),
                    "speed": float(sec.get("speed", DEFAULT_SECONDARY_VOICE["speed"])),
                    "pitch": float(sec.get("pitch", DEFAULT_SECONDARY_VOICE["pitch"])),
                    "temperature": float(sec.get("temperature", DEFAULT_SECONDARY_VOICE["temperature"])),
                }
            pri = presets.get("primary") or {}
            return {
                "voice_id": pri.get("voice", cfg.get("voice", DEFAULT_PRIMARY_VOICE["voice_id"])),
                "voice_label": pri.get("voice_label", cfg.get("voice_label", DEFAULT_PRIMARY_VOICE["voice_label"])),
                "speed": float(pri.get("speed", cfg.get("speed", DEFAULT_PRIMARY_VOICE["speed"]))),
                "pitch": float(pri.get("pitch", cfg.get("pitch", DEFAULT_PRIMARY_VOICE["pitch"]))),
                "temperature": float(pri.get("temperature", cfg.get("temperature", DEFAULT_PRIMARY_VOICE["temperature"]))),
            }
        except Exception as e:
            warn(f"Không đọc được config/voice.json ({e}), dùng mặc định chuẩn.")
    return dict(DEFAULT_SECONDARY_VOICE if preset in ("secondary", "female", "nu") else DEFAULT_PRIMARY_VOICE)


# ─────────────────────────────────────────────────────────────────────────────
# 2. CHUẨN HÓA TIÊU ĐỀ SENTENCE CASE & MÔ TẢ YOUTUBE (mota.txt)
# ─────────────────────────────────────────────────────────────────────────────

FORBIDDEN_PHRASES = [
    "thước phim phân tích",
    "thước phim",
]

# Các mẫu dữ liệu rác kỹ thuật nội bộ TUYỆT ĐỐI CẤM xuất hiện trong mô tả YouTube công khai
_INTERNAL_PREFIX_TAG_RE = re.compile(
    r"^(?:\[(?:nam|nữ|nu|tin\s*\d+|\d+|intro|outro|hook|primary|secondary)\]"
    r"|\((?:nam|nữ|nu|mẫu\s*\d+|mau\s*\d+|primary|secondary)\)"
    r"|(?:tin\s*\d+\s*[:\-–]))\s*",
    flags=re.IGNORECASE,
)
_INTERNAL_INLINE_TAG_RE = re.compile(
    r"\[(?:nam|nữ|nu|tin\s*\d+|\d+|primary|secondary)\]"
    r"|\((?:mẫu\s*\d+|mau\s*\d+|primary|secondary)\)",
    flags=re.IGNORECASE,
)
_INTERNAL_VOICE_NOTE_RE = re.compile(
    r"\s*(?:với|cùng)?\s*(?:giọng\s+(?:đọc\s+)?(?:nam|nữ)(?:\s+chính)?(?:\s+dẫn\s+[^.,;]+)?(?:\s+(?:và|lẫn|cùng)\s+giọng\s+(?:đọc\s+)?(?:nam|nữ)(?:\s+dẫn\s+[^.,;]+)?)?)"
    r"|\s*\b(?:minh\s+quân\s+pro|ngọc\s+huyền|giọng\s+đọc|thời\s+gian\s+tạo\s+video|cảnh\s+quay|hiệu\s+ứng\s+(?:hình\s+ảnh|hiển\s+thị))\b",
    flags=re.IGNORECASE,
)
_SCRAPER_WINDOW_META_RE = re.compile(
    r",?\s*(?:cập\s+nhật\s+(?:toàn\s+cảnh\s+)?diễn\s+biến\s+nóng\s+nhất\s+)?từ\s+12\s*(?:giờ|h)(?:\s*trưa)?(?:\s*(?:ngày\s+)?hôm\s+qua)?(?:\s*(?:đến|tới)\s*(?:sáng\s+nay|hiện\s+tại|nay))?",
    flags=re.IGNORECASE,
)


def sanitize_chapter_label(label: str) -> str:
    """Loại bỏ triệt để tag nội bộ ([Nữ], [Nam], [TIN 01], [01]...) khỏi nhãn Chapter YouTube."""
    s = re.sub(r"\s+", " ", (label or "").strip())
    while True:
        nxt = _INTERNAL_PREFIX_TAG_RE.sub("", s).strip()
        if nxt == s:
            break
        s = nxt
    s = _INTERNAL_INLINE_TAG_RE.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def sanitize_public_text(text: str) -> str:
    """Làm sạch mô tả công khai: khử tag kỹ thuật, chú thích hậu trường/máy móc và cụm từ cấm."""
    s = re.sub(r"\s+", " ", (text or "").strip())
    for bad in FORBIDDEN_PHRASES:
        s = re.sub(re.escape(bad), "bản tin tổng hợp", s, flags=re.IGNORECASE)
    s = _SCRAPER_WINDOW_META_RE.sub("", s)
    s = _INTERNAL_INLINE_TAG_RE.sub("", s)
    s = _INTERNAL_VOICE_NOTE_RE.sub("", s)
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    s = re.sub(r"\s*•\s*(?=•|$)", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def format_mmss(sec: float) -> str:
    sec_i = max(0, int(round(sec)))
    return f"{sec_i // 60:02d}:{sec_i % 60:02d}"


def clean_seo_title(title: str, max_len: int = 100) -> str:
    """
    Đảm bảo tiêu đề không vượt quá `max_len` ký tự, sạch tag nội bộ và không chứa cụm từ cấm.
    """
    t = sanitize_chapter_label(sanitize_public_text(title))
    if len(t) > max_len:
        t = t[: max_len - 1].rsplit(" ", 1)[0].rstrip(",;:-") + "…"
    return t


def _extract_dd_mm(day_str: str) -> str:
    m = re.match(r"^(\d{1,2})[./\-](\d{1,2})", (day_str or "").strip())
    if m:
        return f"{int(m.group(1)):02d}/{int(m.group(2)):02d}"
    return ""


def format_long_title_with_suffix(
    title: str,
    video_type: str = "weekly_digest",
    day_str: str = "",
    brand_suffix: Optional[str] = None,
    max_len: int = 100,
) -> str:
    """
    Chuẩn hóa tiêu đề Video Dài 16:9 (Sentence Case <= 100 ký tự) kèm hậu tố thương hiệu thống nhất:
      - daily_digest  -> "| Điểm Đọc DD/MM"
      - weekly_digest -> "| Điểm Đọc Tuần"
      - thematic_long -> "| Điểm Đọc"
    """
    t = sanitize_chapter_label(sanitize_public_text(title))
    # Gỡ hậu tố "| Điểm Đọc..." cũ nếu có để tránh lặp
    t = re.sub(r"\s*[\|–\-]\s*Điểm\s*Đọc(?:\s+Tuần|\s+\d{1,2}[/.\-]\d{1,2})?\s*$", "", t, flags=re.IGNORECASE).strip()

    if brand_suffix is not None:
        sfx = brand_suffix.strip()
    else:
        dd_mm = _extract_dd_mm(day_str)
        if video_type == "daily_digest" and dd_mm:
            sfx = f"| Điểm Đọc {dd_mm}"
        elif video_type == "weekly_digest":
            sfx = "| Điểm Đọc Tuần"
        elif video_type == "thematic_long":
            sfx = "| Điểm Đọc"
        else:
            sfx = f"| Điểm Đọc {dd_mm}" if dd_mm else "| Điểm Đọc"

    if not sfx:
        return clean_seo_title(t, max_len)

    # Nếu tiêu đề bắt đầu bằng "Tin thể thao DD/MM:" hoặc "Bản tin thể thao DD/MM:" và bị vượt 100 ký tự khi gắn đuôi "| Điểm Đọc DD/MM",
    # tự động rút gọn tiền tố lặp ngày để giữ trọn nội dung chính.
    if len(f"{t} {sfx}") > max_len:
        t_trimmed = re.sub(
            r"^(?:Bản\s+tin\s+thể\s+thao|Tin\s+thể\s+thao|Điểm\s+Đọc\s+thể\s+thao)\s+\d{1,2}[/.\-]\d{1,2}(?:/\d{2,4})?\s*:\s*",
            "",
            t,
            flags=re.IGNORECASE,
        ).strip()
        if t_trimmed:
            t = t_trimmed[0].upper() + t_trimmed[1:]

    avail = max_len - len(sfx) - 1
    if len(t) > avail:
        t = t[: avail - 1].rsplit(" ", 1)[0].rstrip(",;:-") + "…"
    return f"{t} {sfx}"


def write_mota_16x9(
    out_path: Path,
    titles_abc: List[str],
    chapters: List[Tuple[str, str]],
    video_type: str = "weekly_digest",
    intro_paragraphs: Optional[List[str]] = None,
    highlight_bullets: Optional[List[str]] = None,
    sources_line: Optional[str] = None,
    hashtags: Optional[List[str]] = None,
    day_str: str = "",
    brand_suffix: Optional[str] = None,
) -> Path:
    """
    Xuất file `mota.txt` chuẩn thống nhất cho Video 16:9 (chỉ đăng YouTube):
      - `daily_digest`  : Đuôi `| Điểm Đọc DD/MM`
      - `weekly_digest` : Đuôi `| Điểm Đọc Tuần`
      - `thematic_long` : Đuôi `| Điểm Đọc`
    Cấu trúc bắt buộc chỉ gồm 2 phần:
      1. `=== TIÊU ĐỀ YOUTUBE (ĐỘ DÀI CHUẨN <= 100 KÝ TỰ) ===` (3 phương án A/B/C Sentence Case có hậu tố thương hiệu)
      2. `=== MÔ TẢ VIDEO ===` (Lời dẫn + Điểm nhấn + `⏱️ MỐC THỜI GIAN (CHAPTERS):` + Nguồn + Lời kêu gọi + Dòng `#DiemDoc...` cuối)
    """
    raw_titles = [t for t in (titles_abc or []) if t and t.strip()]
    clean_titles = [
        format_long_title_with_suffix(t, video_type=video_type, day_str=day_str, brand_suffix=brand_suffix, max_len=100)
        for t in raw_titles
    ]
    while len(clean_titles) < 3:
        fallback = raw_titles[0] if raw_titles else "Toàn cảnh sự kiện bóng đá và thể thao đáng chú ý"
        clean_titles.append(
            format_long_title_with_suffix(fallback, video_type=video_type, day_str=day_str, brand_suffix=brand_suffix, max_len=100)
        )

    lines: List[str] = [
        "=== TIÊU ĐỀ YOUTUBE (ĐỘ DÀI CHUẨN <= 100 KÝ TỰ) ===",
        f"Option A (Khuyên dùng): {clean_titles[0]}",
        f"Option B: {clean_titles[1]}",
        f"Option C: {clean_titles[2]}",
        "",
        "=== MÔ TẢ VIDEO ===",
    ]

    if intro_paragraphs:
        for p in intro_paragraphs:
            p_clean = sanitize_public_text(p)
            if p_clean:
                lines.append(p_clean)
                lines.append("")
    else:
        if video_type == "daily_digest":
            d_label = f" ngày {day_str}" if day_str else ""
            lines.append(
                f"Bản tin Điểm Đọc Thể Thao{d_label} tổng hợp những diễn biến nóng nhất của thể thao Việt Nam "
                "và quốc tế trong ngày với đầy đủ số liệu, kết quả thi đấu và phân tích chuyên môn."
            )
            lines.append("")
        elif video_type == "weekly_digest":
            d_label = f" ngày {day_str}" if day_str else ""
            lines.append(
                f"Bản tin Điểm Đọc Thể Thao{d_label} tổng hợp những chuyển động nóng nhất của thể thao Việt Nam "
                "và quốc tế trong tuần qua với đầy đủ số liệu, kết quả thi đấu và diễn biến chuyên môn."
            )
            lines.append("")
        else:
            lines.append(
                "Chuyên đề đặc biệt trên kênh Điểm Đọc Thể Thao: Tổng hợp số liệu, cột mốc lịch sử "
                "và những góc nhìn chuyên môn sâu sắc nhất."
            )
            lines.append("")

    if highlight_bullets:
        header_bullet = (
            "🔥 Tâm điểm đáng chú ý trong video:"
            if video_type in ("weekly_digest", "daily_digest")
            else "📊 Nội dung trọng tâm trong video:"
        )
        lines.append(header_bullet)
        for b in highlight_bullets:
            b_str = sanitize_public_text(b)
            if not b_str:
                continue
            if not b_str.startswith("-"):
                b_str = f"- {b_str}"
            lines.append(b_str)
        lines.append("")

    if chapters:
        lines.append("⏱️ MỐC THỜI GIAN (CHAPTERS):")
        for ts, ch_title in chapters:
            clean_ch = sanitize_chapter_label(ch_title)
            if clean_ch:
                lines.append(f"{ts} {clean_ch}")
        lines.append("")

    if sources_line and sources_line.strip():
        lines.append(sources_line.strip())
        lines.append("")

    lines.append("🔔 Đừng quên nhấn LIKE, SHARE và ĐĂNG KÝ kênh ĐIỂM ĐỌC để cập nhật tin tức và chuyên đề thể thao chuẩn xác mỗi ngày!")
    lines.append("")

    default_tags = ["#DiemDoc", "#DiemDocTheThao", "#TinTheThao", "#BongDa", "#TheThaoVietNam"]
    tag_list = hashtags if hashtags else default_tags
    lines.append(" ".join(t if t.startswith("#") else f"#{t}" for t in tag_list))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


def write_mota_9x16(
    out_path: Path,
    seo_title: str,
    description_paragraphs: List[str],
    chapters: Optional[List[Tuple[str, str]]] = None,
    sources_line: Optional[str] = None,
    hashtags: Optional[List[str]] = None,
    tiktok_caption: Optional[str] = None,
    fb_hook: Optional[str] = None,
) -> Path:
    """
    Xuất file `_mota.txt` chuẩn thống nhất Đa Nền Tảng cho Video Shorts 9:16:
      - Chỉ dùng 1 Tiêu đề chuẩn Sentence Case (<= 100 ký tự) cho YouTube Shorts.
      - Tách sẵn nội dung mô tả/caption tối ưu riêng cho cả 3 mạng xã hội:
        1. `=== 1. YOUTUBE SHORTS (TIÊU ĐỀ + MÔ TẢ) ===`
        2. `=== 2. FACEBOOK REELS (CHỈ MÔ TẢ / CAPTION) ===`
        3. `=== 3. TIKTOK (CHỈ MÔ TẢ / CAPTION TỐI ƯU TÌM KIẾM) ===`
    """
    base_title = sanitize_chapter_label(sanitize_public_text(seo_title))
    base_title_no_tag = re.sub(r"\s*#shorts\b", "", base_title, flags=re.IGNORECASE).strip()
    base_title_no_tag = re.sub(r"\s*[\|–\-]\s*Điểm\s*Đọc.*$", "", base_title_no_tag, flags=re.IGNORECASE).strip()

    yt_suffix = "| Điểm Đọc #Shorts"
    if len(f"{base_title_no_tag} {yt_suffix}") <= 100:
        yt_title = f"{base_title_no_tag} {yt_suffix}"
    elif len(f"{base_title_no_tag} #Shorts") <= 100:
        yt_title = f"{base_title_no_tag} #Shorts"
    else:
        avail = 100 - len(" #Shorts")
        trimmed = base_title_no_tag[: avail - 1].rsplit(" ", 1)[0].rstrip(",;:-") + "…"
        yt_title = f"{trimmed} #Shorts"

    clean_paras = [sanitize_public_text(p) for p in (description_paragraphs or []) if sanitize_public_text(p)]
    clean_chapters: List[Tuple[str, str]] = []
    for ts, ch_title in (chapters or []):
        c_lbl = sanitize_chapter_label(ch_title)
        if c_lbl:
            clean_chapters.append((ts, c_lbl))

    raw_tags = [x if x.startswith("#") else f"#{x}" for x in (hashtags or ["#DiemDoc", "#DiemDocTheThao", "#TinTheThao", "#BongDa"])]
    core_tags = [x for x in raw_tags if x.lower() not in ("#shorts", "#reels", "#tiktok", "#xuhuong")]

    yt_tags = ["#Shorts"] + [x for x in core_tags if x.lower() != "#shorts"]
    fb_tags = list(dict.fromkeys(core_tags + ["#Reels", "#TheThaoVietNam"]))
    tt_tags = list(dict.fromkeys(core_tags + ["#TheThao247", "#XuHuong"]))

    # ── 1. Khối YouTube Shorts ──
    lines: List[str] = [
        "=== TIÊU ĐỀ YOUTUBE (ĐỘ DÀI CHUẨN <= 100 KÝ TỰ) ===",
        yt_title,
        "",
        "=== MÔ TẢ VIDEO ===",
        "[1. YOUTUBE SHORTS — MÔ TẢ]",
    ]
    for p in clean_paras:
        lines.append(p)
        lines.append("")

    if clean_chapters:
        lines.append("⏱️ MỐC THỜI GIAN (CHAPTERS):")
        for ts, c_lbl in clean_chapters:
            lines.append(f"{ts} {c_lbl}")
        lines.append("")

    if sources_line and sources_line.strip():
        lines.append(sources_line.strip())
        lines.append("")

    lines.append("🔔 Nhấn LIKE và ĐĂNG KÝ kênh ĐIỂM ĐỌC để cập nhật tin nóng thể thao mỗi ngày!")
    lines.append(" ".join(yt_tags))
    lines.append("")

    # ── 2. Khối Facebook Reels (Chỉ Mô Tả / Caption, không dùng mốc 00:00 & không gắn #Shorts) ──
    lines.append("-" * 70)
    lines.append("[2. FACEBOOK REELS — CHỈ MÔ TẢ / CAPTION]")
    hook_line = sanitize_public_text(fb_hook) if fb_hook else f"🔥 {base_title_no_tag}"
    lines.append(hook_line)
    lines.append("")
    for p in clean_paras:
        lines.append(p)
        lines.append("")

    if len(clean_chapters) > 1:
        lines.append("📌 Các nội dung chính trong video:")
        for _, c_lbl in clean_chapters:
            if c_lbl.lower().startswith("mở đầu"):
                continue
            lines.append(f"• {c_lbl}")
        lines.append("")

    if sources_line and sources_line.strip():
        lines.append(sources_line.strip())
        lines.append("")

    lines.append("👉 Theo dõi fanpage ĐIỂM ĐỌC để không bỏ lỡ nhịp đập thể thao mỗi ngày!")
    lines.append(" ".join(fb_tags))
    lines.append("")

    # ── 3. Khối TikTok (Chỉ Mô Tả / Caption gọn tối ưu tìm kiếm & gợi tương tác) ──
    lines.append("-" * 70)
    lines.append("[3. TIKTOK — CHỈ MÔ TẢ / CAPTION]")
    if tiktok_caption and sanitize_public_text(tiktok_caption):
        tt_body = sanitize_public_text(tiktok_caption)
    elif clean_paras:
        tt_body = clean_paras[0]
    else:
        tt_body = base_title_no_tag
    lines.append(tt_body)
    lines.append("💬 Bạn ấn tượng nhất với thông tin nào? Cùng để lại bình luận bên dưới nhé!")
    lines.append("")
    lines.append(" ".join(tt_tags))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# 3. RENDER ẢNH BÌA CHUẨN THỐNG NHẤT (16:9 & 9:16) QUA PLAYWRIGHT
# ─────────────────────────────────────────────────────────────────────────────

def compute_16x9_hero_font_size(hero_html: str) -> str:
    """
    Tự động tính cỡ chữ Anton tối ưu (số nguyên, không kèm 'px') cho Thumbnail 16:9
    nhằm tránh rớt chữ lẻ sang dòng phụ khi có các chữ cái rộng (M, U, N, G, Đ).
    """
    parts = re.split(r"<br\s*/?>", hero_html or "", flags=re.IGNORECASE)
    plain_lines = [re.sub(r"<[^>]+>", "", p).strip() for p in parts if p.strip()]
    max_chars = max((len(line) for line in plain_lines), default=12)
    if max_chars <= 13:
        return "88"
    if max_chars <= 16:
        return "82"
    if max_chars <= 18:
        return "74"
    if max_chars <= 21:
        return "66"
    return "58"


def compute_9x16_hero_font_size(hero_html: str) -> str:
    """
    Tự động tính cỡ chữ Anton tối ưu (số nguyên, không kèm 'px') cho Thumbnail 9:16 dựa trên độ dài dòng dài nhất.
    """
    parts = re.split(r"<br\s*/?>", hero_html or "", flags=re.IGNORECASE)
    plain_lines = [re.sub(r"<[^>]+>", "", p).strip() for p in parts if p.strip()]
    max_chars = max((len(line) for line in plain_lines), default=12)
    if max_chars <= 13:
        return "88"
    if max_chars <= 16:
        return "78"
    if max_chars <= 19:
        return "70"
    if max_chars <= 22:
        return "64"
    return "58"


def render_thumbnail_9x16(
    out_path: Path,
    image_path: Path,
    kicker: str,
    hero_html: str,
    subtitle: str,
    badge: str = "TIN NÓNG",
    tag_a: str = "ĐIỂM ĐỌC",
    tag_b: str = "CHUẨN 1080P",
    hero_size: Optional[str] = None,
    obj_pos: str = "center 20%",
    img_filter: str = "contrast(1.10) brightness(1.04) saturate(1.18)",
    page: Optional[Any] = None,
) -> bool:
    """
    Render ảnh bìa dọc 9:16 (`1080x1920`) chuẩn thống nhất từ `templates/thumbnail_9x16_sports.html`.
    Nếu đã có sẵn `page` của Playwright thì tái sử dụng, ngược lại tự mở browser headless.
    """
    tpl_path = Path(paths.TEMPLATES) / "thumbnail_9x16_sports.html"
    if not tpl_path.exists():
        warn(f"Không tìm thấy template {tpl_path}")
        return False

    tpl_html = tpl_path.read_text(encoding="utf-8")
    assets_url = paths.file_url(str(paths.ASSETS))
    logo_file = Path(paths.ASSETS) / "logo" / "diem-doc-logo-1.png"
    if not logo_file.exists():
        logo_file = Path(paths.LOGO) / "logo.png"
    logo_url = paths.file_url(str(logo_file))
    img_p = Path(image_path) if image_path else None
    photo_url = paths.file_url(str(img_p)) if img_p and img_p.exists() else ""
    computed_size = str(hero_size or compute_9x16_hero_font_size(hero_html)).replace("px", "")

    html = (
        tpl_html.replace("__ASSETS__", assets_url)
        .replace("__LOGO_URL__", logo_url)
        .replace("__LOGO__", logo_url)
        .replace("__THUMB_IMAGE__", photo_url)
        .replace("__PHOTO__", photo_url)
        .replace("__THUMB_OBJ_POS__", obj_pos)
        .replace("__OBJ_POS__", obj_pos)
        .replace("__THUMB_FILTER__", img_filter)
        .replace("__THUMB_BADGE__", badge)
        .replace("__BADGE__", badge)
        .replace("__THUMB_KICKER__", kicker)
        .replace("__KICKER__", kicker)
        .replace("__THUMB_HERO_SIZE__", computed_size)
        .replace("__HERO_SIZE__", f"{computed_size}px")
        .replace("__THUMB_HERO__", hero_html)
        .replace("__HERO_HTML__", hero_html)
        .replace("__THUMB_SUBTITLE__", subtitle)
        .replace("__SUBTITLE__", subtitle)
        .replace("__THUMB_TAG_A__", tag_a)
        .replace("__TAG_A__", tag_a)
        .replace("__THUMB_TAG_B__", tag_b)
        .replace("__TAG_B__", tag_b)
    )

    out_p = Path(out_path)
    tmp_dir = Path(paths.WORK) / "_thumbnails_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_html = tmp_dir / f"thumb_9x16_{out_p.stem}.html"
    tmp_html.write_text(html, encoding="utf-8")
    out_p.parent.mkdir(parents=True, exist_ok=True)

    if page is not None:
        page.set_viewport_size({"width": 1080, "height": 1920})
        page.goto(paths.file_url(str(tmp_html)), wait_until="networkidle")
        page.wait_for_timeout(200)
        page.screenshot(path=str(out_p), type="jpeg", quality=95)
        return True

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(paths.file_url(str(tmp_html)), wait_until="networkidle")
        pg.wait_for_timeout(250)
        pg.screenshot(path=str(out_p), type="jpeg", quality=95)
        browser.close()
    return True


def render_thumbnail_16x9_single(
    out_path: Path,
    image_path: Path,
    kicker: str,
    hero_html: str,
    subtitle: str,
    badge: str = "TÂM ĐIỂM",
    tag_a: str = "ĐIỂM ĐỌC",
    tag_b: str = "CHUẨN 1080P",
    hero_size: str = "86",
    obj_pos: str = "center top",
    img_filter: str = "contrast(1.10) brightness(1.04) saturate(1.18)",
    page: Optional[Any] = None,
) -> bool:
    """
    Render 1 phương án ảnh bìa ngang 16:9 (`1920x1080`) chuẩn thống nhất từ `templates/thumbnail_16x9_sports.html`.
    """
    tpl_path = Path(paths.TEMPLATES) / "thumbnail_16x9_sports.html"
    if not tpl_path.exists():
        warn(f"Không tìm thấy template {tpl_path}")
        return False

    tpl_html = tpl_path.read_text(encoding="utf-8")
    assets_url = paths.file_url(str(paths.ASSETS))
    logo_file = Path(paths.ASSETS) / "logo" / "diem-doc-logo-1.png"
    if not logo_file.exists():
        logo_file = Path(paths.LOGO) / "logo.png"
    logo_url = paths.file_url(str(logo_file))
    img_p = Path(image_path) if image_path else None
    photo_url = paths.file_url(str(img_p)) if img_p and img_p.exists() else ""
    auto_sz = compute_16x9_hero_font_size(hero_html)
    raw_sz = str(hero_size or auto_sz).replace("px", "")
    clean_size = str(min(int(raw_sz), int(auto_sz))) if raw_sz.isdigit() and auto_sz.isdigit() else auto_sz

    html = (
        tpl_html.replace("__ASSETS__", assets_url)
        .replace("__LOGO_URL__", logo_url)
        .replace("__LOGO__", logo_url)
        .replace("__THUMB_IMAGE__", photo_url)
        .replace("__PHOTO__", photo_url)
        .replace("__THUMB_OBJ_POS__", obj_pos)
        .replace("__OBJ_POS__", obj_pos)
        .replace("__THUMB_FILTER__", img_filter)
        .replace("__THUMB_BADGE__", badge)
        .replace("__BADGE__", badge)
        .replace("__THUMB_KICKER__", kicker)
        .replace("__KICKER__", kicker)
        .replace("__THUMB_HERO_SIZE__", clean_size)
        .replace("__HERO_SIZE__", f"{clean_size}px")
        .replace("__THUMB_HEADLINE__", hero_html)
        .replace("__HERO_HTML__", hero_html)
        .replace("__THUMB_SUBTITLE__", subtitle)
        .replace("__SUBTITLE__", subtitle)
        .replace("__THUMB_FOOTER_TAG__", tag_a)
        .replace("__TAG_A__", tag_a)
        .replace("__TAG_B__", tag_b)
    )

    out_p = Path(out_path)
    tmp_dir = Path(paths.WORK) / "_thumbnails_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_html = tmp_dir / f"thumb_16x9_{out_p.stem}.html"
    tmp_html.write_text(html, encoding="utf-8")
    out_p.parent.mkdir(parents=True, exist_ok=True)

    if page is not None:
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto(paths.file_url(str(tmp_html)), wait_until="networkidle")
        page.wait_for_timeout(200)
        page.screenshot(path=str(out_p), type="jpeg", quality=95)
        return True

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pg = browser.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(paths.file_url(str(tmp_html)), wait_until="networkidle")
        pg.wait_for_timeout(250)
        pg.screenshot(path=str(out_p), type="jpeg", quality=95)
        browser.close()
    return True
