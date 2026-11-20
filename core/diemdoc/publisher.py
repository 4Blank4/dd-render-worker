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
) -> Path:
    """
    Xuất file `mota.txt` chuẩn thống nhất cho Video 16:9 (cả Loại 1: Bản tin tổng hợp & Loại 2: Chuyên đề riêng).
    Cấu trúc bắt buộc chỉ gồm 2 phần:
      1. `=== TIÊU ĐỀ YOUTUBE (ĐỘ DÀI CHUẨN <= 100 KÝ TỰ) ===` (3 phương án A/B/C Sentence Case)
      2. `=== MÔ TẢ VIDEO ===` (Lời dẫn + Điểm nhấn / Thông tin + `⏱️ MỐC THỜI GIAN (CHAPTERS):` + Lời kêu gọi + Dòng `#DiemDoc...` cuối)
    Tuyệt đối không có mục `=== HASHTAGS ===` rời rạc hay từ ngữ phi thời sự.
    """
    clean_titles = [clean_seo_title(t, 100) for t in (titles_abc or []) if t and t.strip()]
    while len(clean_titles) < 3:
        fallback = clean_titles[0] if clean_titles else f"Điểm Đọc thể thao {day_str}: Toàn cảnh sự kiện bóng đá và thể thao đáng chú ý"
        clean_titles.append(clean_seo_title(fallback, 100))

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
        if video_type == "weekly_digest":
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
        header_bullet = "🔥 Tâm điểm đáng chú ý trong video:" if video_type == "weekly_digest" else "📊 Nội dung trọng tâm trong video:"
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
) -> Path:
    """
    Xuất file `_mota.txt` chuẩn thống nhất cho Video Shorts 9:16 (Loại 3: Tin ngắn hằng ngày, Focus Short 2-5 tin, Digest Short).
    Cấu trúc bắt buộc gồm 2 phần:
      1. `=== TIÊU ĐỀ YOUTUBE (ĐỘ DÀI CHUẨN <= 100 KÝ TỰ) ===` (1 dòng tiêu đề Sentence Case kèm `#Shorts`)
      2. `=== MÔ TẢ VIDEO ===` (Đoạn tóm tắt + `⏱️ MỐC THỜI GIAN:` nếu gộp nhiều tin + Nguồn + Lời kêu gọi + Dòng `#Shorts #DiemDoc...`)
    """
    t = clean_seo_title(seo_title, 100)
    if "#shorts" not in t.lower() and len(t) <= 92:
        t = f"{t} #Shorts"

    lines: List[str] = [
        "=== TIÊU ĐỀ YOUTUBE (ĐỘ DÀI CHUẨN <= 100 KÝ TỰ) ===",
        t,
        "",
        "=== MÔ TẢ VIDEO ===",
    ]

    for p in (description_paragraphs or []):
        p_clean = sanitize_public_text(p)
        if p_clean:
            lines.append(p_clean)
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

    lines.append("🔔 Nhấn LIKE và ĐĂNG KÝ kênh ĐIỂM ĐỌC để cập nhật tin nóng thể thao mỗi ngày!")
    lines.append("")

    default_tags = ["#Shorts", "#DiemDoc", "#DiemDocTheThao", "#TinTheThao", "#BongDa"]
    tag_list = hashtags if hashtags else default_tags
    if not any(x.lower() == "#shorts" for x in tag_list):
        tag_list = ["#Shorts"] + list(tag_list)
    lines.append(" ".join(x if x.startswith("#") else f"#{x}" for x in tag_list))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# 3. RENDER ẢNH BÌA CHUẨN THỐNG NHẤT (16:9 & 9:16) QUA PLAYWRIGHT
# ─────────────────────────────────────────────────────────────────────────────

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
    clean_size = str(hero_size).replace("px", "")

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
