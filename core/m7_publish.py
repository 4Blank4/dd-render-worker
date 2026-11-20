#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

"""
m7 — PUBLISH PACK (Thumbnail A/B/C + Subtitles + SEO Metadata)
==================================================================
Gộp các tác vụ xuất bản vào một lệnh tự động:

  1. Thumbnail:
     - 16:9 (Long Video): Tự động sinh 3 thumbnail A/B/C (thumbnail_A.jpg,
       thumbnail_B.jpg, thumbnail_C.jpg) phục vụ thử nghiệm A/B/C testing của YouTube.
     - 9:16 (Short Video): Sinh 1 thumbnail dọc (thumbnail.jpg).
     - Tự động xuất vào cả thư mục project và outputs/<project>/.
  2. sub_tieng_viet.txt: Khung kịch bản và phụ đề tiếng Việt chuẩn hoá.
  3. mota.txt: Metadata chuẩn SEO YouTube (3 Options Tiêu đề A/B/C,
     mô tả cuốn hút, Timestamps/Chapters, trích nguồn báo, tags & hashtags).

Cách dùng:
  python3 core/m7_publish.py <project>
  python3 core/m7_publish.py <project> --only thumb
  python3 core/m7_publish.py <project> --only meta
  python3 core/m7_publish.py <project> --only sub
"""

import argparse
import json
import os
import re
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.timeline import cards_of, load_timeline, scene_duration, scene_start
from diemdoc.publisher import (
    compute_9x16_hero_font_size,
    write_mota_16x9,
    write_mota_9x16,
)


def _safe_copy(src: str, dst: str) -> None:
    if os.path.abspath(src) != os.path.abspath(dst):
        try:
            shutil.copy2(src, dst)
        except shutil.SameFileError:
            pass


# ==========================================================================
# 1. THUMBNAIL ENGINE (16:9 A/B/C CHO YOUTUBE & 9:16 DỌC CHO SHORTS)
# ==========================================================================

THUMB_16X9_TEMPLATE = os.path.join(paths.TEMPLATES, "thumbnail_16x9_sports.html")
THUMB_9X16_TEMPLATE = os.path.join(paths.TEMPLATES, "thumbnail_9x16_sports.html")


def _get_project_images(project_dir: str) -> list[str]:
    img_dir = os.path.join(project_dir, "images_ready")
    imgs = []
    if os.path.isdir(img_dir):
        for f in sorted(os.listdir(img_dir)):
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) and f != "logo.png":
                imgs.append(f"images_ready/{f}")
    return imgs


def _scaffold_thumbnail_variants(project_dir: str, tl: dict) -> list[dict]:
    """
    Sinh cấu hình 3 biến thể A/B/C cho thumbnail 16:9 của YouTube:
      - Variant A: Góc Kịch tính (Dramatic / Controversy)
      - Variant B: Góc Ngôi sao & Sự kiện (Star / Big Event)
      - Variant C: Góc Phân tích & Tương lai (Analytical / Future)
    """
    if tl.get("thumbnail_variants"):
        vars_cfg = []
        for v in tl["thumbnail_variants"]:
            v_copy = dict(v)
            img = v_copy.get("image", "")
            if img and not img.startswith(("http://", "https://", "file://", "data:")):
                img_path = os.path.join(project_dir, img)
                if not os.path.exists(img_path):
                    img_path = os.path.join(paths.project_dir(os.path.basename(project_dir)), img)
                if os.path.exists(img_path):
                    v_copy["image"] = paths.file_url(img_path)
            vars_cfg.append(v_copy)
        return vars_cfg

    images = _get_project_images(project_dir)
    scenes = tl.get("scenes", [])

    # Variant A (Kịch tính)
    sc1 = scenes[0] if len(scenes) > 0 else {}
    img_a = images[0] if len(images) > 0 else ""
    # Tìm ảnh trong card photo-card của scene 1
    for c in cards_of(sc1):
        if c.get("type") == "photo-card" and c.get("image"):
            img_a = c.get("image")
            break

    var_a = {
        "suffix": "A",
        "angle_name": "KỊCH TÍNH (DRAMATIC)",
        "badge": "KỊCH TÍNH",
        "kicker": "TIÊU ĐIỂM NÓNG • TRANH CÃI",
        "headline": "MOURINHO NỔI GIẬN: <span class=\"highlight\">VINICIUS</span> BỊ XỬ ÉP?",
        "subtitle": "TREO GIÒ 4 TRẬN BẤT NGỜ CHỈ 2 TIẾNG TRƯỚC GIỜ BÓNG LĂN C1",
        "image": img_a,
    }

    # Variant B (Ngôi sao / Sự kiện)
    sc2 = scenes[1] if len(scenes) > 1 else sc1
    img_b = images[1] if len(images) > 1 else img_a
    for c in cards_of(sc2):
        if c.get("type") == "photo-card" and c.get("image"):
            img_b = c.get("image")
            break

    var_b = {
        "suffix": "B",
        "angle_name": "NGÔI SAO & SỰ KIỆN (STAR / EVENT)",
        "badge": "NGÔI SAO",
        "kicker": "NGÀY HỘI BÓNG ĐÁ THÁNG 11",
        "headline": "ĐẠI CHIẾN <span class=\"highlight\">NGA & THÁI LAN</span> TẠI THIÊN TRƯỜNG",
        "subtitle": "LỘ DIỆN GIỜ ĐẤU CHÍNH THỨC 3 TRẬN ĐỈNH CAO CỦA ĐT VIỆT NAM",
        "image": img_b,
    }

    # Variant C (Phân tích / Chiến thuật)
    sc3 = scenes[2] if len(scenes) > 2 else sc2
    img_c = images[2] if len(images) > 2 else img_b
    for c in cards_of(sc3):
        if c.get("type") == "photo-card" and c.get("image"):
            img_c = c.get("image")
            break

    var_c = {
        "suffix": "C",
        "angle_name": "PHÂN TÍCH CHUYÊN SÂU (ANALYTICAL)",
        "badge": "PHÂN TÍCH",
        "kicker": "CHIẾN DỊCH ASIAN CUP 2027",
        "headline": "ĐÌNH BẮC BỊ TREO GIÒ: <span class=\"highlight\">TIẾN LINH</span> TÁI XUẤT?",
        "subtitle": "BÀI TOÁN HÀNG CÔNG NAN GIẢI CỦA THẦY KIM TRƯỚC GIẢI CHÂU LỤC",
        "image": img_c,
    }

    return [var_a, var_b, var_c]


def make_thumbnail(project_dir: str, tl: dict, out_dir: str | None = None) -> list[str]:
    """
    Render thumbnails tương ứng với định dạng video.
    - Long (16:9): Render 3 thumbnail A/B/C (1920x1080)
    - Short (9:16): Render 1 thumbnail (1080x1920)
    """
    fmt = (tl.get("format") or "short").lower()
    project_name = os.path.basename(project_dir.rstrip("/"))
    if out_dir is None:
        out_dir = os.path.join(paths.OUTPUTS, project_name)
    os.makedirs(out_dir, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        die("Playwright chưa được cài đặt trong môi trường.")

    rendered_files = []

    if fmt == "long":
        # 16:9 Thumbnail Suite
        w, h = 1920, 1080
        tpl_path = THUMB_16X9_TEMPLATE if os.path.exists(THUMB_16X9_TEMPLATE) else THUMB_9X16_TEMPLATE
        with open(tpl_path, "r", encoding="utf-8") as f:
            template_code = f.read()
        template_code = template_code.replace("__ASSETS__", paths.file_url(paths.ASSETS))

        variants = _scaffold_thumbnail_variants(project_dir, tl)

        with sync_playwright() as p:
            br = p.chromium.launch(headless=True, args=[
                "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"])
            page = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)

            for var in variants:
                sfx = var["suffix"]
                html_name = f"thumbnail_{sfx}.html"
                jpg_name = f"thumbnail_{sfx}.jpg"

                html_content = template_code
                logo_path = os.path.join(paths.ASSETS, "logo", "diem-doc-logo-1.png")
                logo_url = paths.file_url(logo_path)
                img_val = var.get("image", "")
                if img_val and not img_val.startswith(("http://", "https://", "file://", "data:")):
                    cand = os.path.join(project_dir, img_val)
                    if os.path.exists(cand):
                        img_val = paths.file_url(cand)
                hero_html = var.get("hero_html") or var.get("headline", "")
                hero_size = var.get("hero_size", "86px")
                obj_pos = var.get("obj_pos", "center top")
                tag_a = var.get("tag_a") or var.get("footer_tag", "ĐIỂM ĐỌC")
                tag_b = var.get("tag_b", "CHUẨN 1080P")

                # Tương thích đồng thời placeholder chuẩn mới (__PHOTO__, __HERO_HTML__...) và cũ
                html_content = (
                    html_content.replace("__LOGO__", logo_url)
                    .replace("__LOGO_URL__", logo_url)
                    .replace("__PHOTO__", img_val)
                    .replace("__THUMB_IMAGE__", img_val)
                    .replace("__OBJ_POS__", obj_pos)
                    .replace("__THUMB_OBJ_POS__", obj_pos)
                    .replace("__BADGE__", var.get("badge", "TÂM ĐIỂM"))
                    .replace("__THUMB_BADGE__", var.get("badge", "TÂM ĐIỂM"))
                    .replace("__KICKER__", var.get("kicker", "ĐIỂM ĐỌC THỂ THAO"))
                    .replace("__THUMB_KICKER__", var.get("kicker", "ĐIỂM ĐỌC THỂ THAO"))
                    .replace("__HERO_SIZE__", hero_size)
                    .replace("__HERO_HTML__", hero_html)
                    .replace("__THUMB_HEADLINE__", hero_html)
                    .replace("__SUBTITLE__", var.get("subtitle", ""))
                    .replace("__THUMB_SUBTITLE__", var.get("subtitle", ""))
                    .replace("__TAG_A__", tag_a)
                    .replace("__THUMB_FOOTER_TAG__", tag_a)
                    .replace("__TAG_B__", tag_b)
                    .replace("__THUMB_FILTER__", var.get("filter", "contrast(1.08) brightness(1.02)"))
                )

                html_file = os.path.join(project_dir, html_name)
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(html_content)

                out_proj = os.path.join(project_dir, jpg_name)
                out_pub = os.path.join(out_dir, jpg_name)

                log(f"Render thumbnail {sfx} ({var['angle_name']}) {w}x{h}...", tag="m7")
                page.goto(paths.file_url(html_file), wait_until="networkidle")
                page.wait_for_timeout(600)
                page.screenshot(path=out_proj, type="jpeg", quality=95)
                _safe_copy(out_proj, out_pub)

                rendered_files.append(out_pub)
                ok(f"Thumbnail {sfx}: {paths.rel_to_root(out_pub)}")

            # Copy variant A thành thumbnail.jpg mặc định
            thumb_def_proj = os.path.join(project_dir, "thumbnail.jpg")
            thumb_def_pub = os.path.join(out_dir, "thumbnail.jpg")
            _safe_copy(os.path.join(project_dir, "thumbnail_A.jpg"), thumb_def_proj)
            _safe_copy(os.path.join(project_dir, "thumbnail_A.jpg"), thumb_def_pub)

            br.close()

    else:
        # 9:16 Vertical Thumbnail (Chuẩn Cyber-Stadium Electric Cyan)
        w, h = 1080, 1920
        with open(THUMB_9X16_TEMPLATE, "r", encoding="utf-8") as f:
            template_code = f.read()
        template_code = template_code.replace("__ASSETS__", paths.file_url(paths.ASSETS))

        logo_path = os.path.join(paths.ASSETS, "logo", "diem-doc-logo-1.png")
        logo_url = paths.file_url(logo_path)
        images = _get_project_images(project_dir)
        img_src = images[0] if images else ""
        if img_src and not img_src.startswith(("http://", "https://", "file://", "data:")):
            cand = os.path.join(project_dir, img_src)
            if os.path.exists(cand):
                img_src = paths.file_url(cand)

        hero_html = tl.get("thumb_hero_html") or "<span class='hl-cyan'>TIN NÓNG</span><br>THỂ THAO 24H"
        hero_size = tl.get("thumb_hero_size") or compute_9x16_hero_font_size(hero_html)
        kicker_txt = tl.get("thumb_kicker") or tl.get("group") or "ĐIỂM ĐỌC THỂ THAO"
        sub_txt = tl.get("thumb_subtitle") or (tl.get("title") or tl.get("topic", "THỂ THAO 24H"))[:75].upper()

        html_content = (
            template_code.replace("__LOGO__", logo_url)
            .replace("__PHOTO__", img_src)
            .replace("__THUMB_IMAGE__", img_src)
            .replace("__OBJ_POS__", tl.get("thumb_obj_pos", "center 20%"))
            .replace("__BADGE__", tl.get("thumb_badge", "TIN NÓNG"))
            .replace("__KICKER__", kicker_txt)
            .replace("__THUMB_KICKER__", kicker_txt)
            .replace("__HERO_SIZE__", str(hero_size))
            .replace("__THUMB_HERO_SIZE__", str(hero_size).replace("px", ""))
            .replace("__HERO_HTML__", hero_html)
            .replace("__THUMB_HERO__", hero_html)
            .replace("__SUBTITLE__", sub_txt)
            .replace("__THUMB_SUBTITLE__", sub_txt)
            .replace("__TAG_A__", tl.get("thumb_tag_a", "ĐIỂM ĐỌC"))
            .replace("__THUMB_TAG_A__", tl.get("thumb_tag_a", "ĐIỂM ĐỌC"))
            .replace("__TAG_B__", tl.get("thumb_tag_b", "CHUẨN 1080P"))
            .replace("__THUMB_TAG_B__", tl.get("thumb_tag_b", "CHUẨN 1080P"))
        )

        html_file = os.path.join(project_dir, "thumbnail.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        out_proj = os.path.join(project_dir, "thumbnail.jpg")
        out_pub = os.path.join(out_dir, "thumbnail.jpg")

        with sync_playwright() as p:
            br = p.chromium.launch(headless=True, args=[
                "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"])
            page = br.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            page.goto(paths.file_url(html_file), wait_until="networkidle")
            page.wait_for_timeout(600)
            page.screenshot(path=out_proj, type="jpeg", quality=95)
            _safe_copy(out_proj, out_pub)
            br.close()

        rendered_files.append(out_pub)
        ok(f"Thumbnail 9:16: {paths.rel_to_root(out_pub)}")

    return rendered_files


# ==========================================================================
# 2. PHỤ ĐỀ TIẾNG VIỆT
# ==========================================================================

def make_vietnamese_sub(project_dir: str, tl: dict, out_dir: str | None = None) -> str:
    """Tạo khung phụ đề kịch bản tiếng Việt có mốc thời lượng từng cảnh."""
    project_name = os.path.basename(project_dir.rstrip("/"))
    if out_dir is None:
        out_dir = os.path.join(paths.OUTPUTS, project_name)
    os.makedirs(out_dir, exist_ok=True)

    out = os.path.join(project_dir, "sub_tieng_viet.txt")
    out_pub = os.path.join(out_dir, "sub_tieng_viet.txt")

    lines = [
        "=" * 78,
        f"KỊCH BẢN & PHỤ ĐỀ TIẾNG VIỆT — {tl.get('output_filename', 'video.mp4')}",
        f"Chủ đề: {tl.get('topic', 'Bản tin thể thao Điểm Đọc')}",
        "=" * 78,
        "",
        "Cấu trúc: Lời thoại đọc chuẩn tiếng Việt & các thẻ đồ hoạ hiển thị.",
        "",
    ]

    for sc in tl.get("scenes", []):
        sid = sc.get("scene_id")
        start_t = scene_start(sc)
        dur = scene_duration(sc)
        lines.append("─" * 78)
        lines.append(f"CẢNH {sid} — {sc.get('title', '')}")
        lines.append(f"  Thời lượng: {start_t:.1f}s → {start_t + dur:.1f}s  ({dur:.1f}s)")
        lines.append("─" * 78)
        lines.append("  LỜI BÌNH (VOICEOVER):")
        script = (sc.get("script_text") or "").strip()
        for sentence in re.split(r"(?<=[.!?])\s+", script):
            if sentence.strip():
                lines.append(f"    {sentence.strip()}")
        lines.append("")
        lines.append("  THẺ ĐỒ HOẠ / DỮ LIỆU HIỂN THỊ:")
        for c in cards_of(sc):
            title = c.get("title") or c.get("headline") or c.get("quote") or c.get("value") or ""
            lines.append(f"    • [{c.get('type')}] {title} (trigger: '{c.get('trigger_word', '')}')")
        lines.append("")

    content = "\n".join(lines)
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    _safe_copy(out, out_pub)

    ok(f"Phụ đề kịch bản: {paths.rel_to_root(out_pub)}")
    return out_pub


# ==========================================================================
# 3. METADATA SEO YOUTUBE & MẠNG XÃ HỘI
# ==========================================================================

def _generate_seo_titles(tl: dict) -> list[tuple[str, str]]:
    """
    Tạo 3 lựa chọn tiêu đề YouTube A/B/C:
      - Option A: Kịch tính (Dramatic / Controversy)
      - Option B: Ngôi sao & Sự kiện (Star / Fixture)
      - Option C: Phân tích chuyên sâu (Analysis / Strategy)
    """
    if tl.get("seo_titles"):
        return tl["seo_titles"]

    return [
        (
            "Phương án A (Kịch tính - Dramatic)",
            "Tranh cãi nảy lửa: Mourinho chất vấn án phạt 4 trận của Vinicius trước giờ G Cúp C1 | Điểm Đọc"
        ),
        (
            "Phương án B (Ngôi sao & Sự kiện - Star / Event)",
            "Đại chiến ĐT Việt Nam vs Nga và Thái Lan: Lộ diện lịch đấu chính thức tại Thiên Trường | Điểm Đọc"
        ),
        (
            "Phương án C (Phân tích chuyên sâu - Analytical)",
            "Đình Bắc bị treo giò, Tiến Linh tái xuất: Bài toán hàng công ĐT Việt Nam thềm Asian Cup | Điểm Đọc"
        ),
    ]


def _format_timestamps(tl: dict) -> list[str]:
    timestamps = []
    for sc in tl.get("scenes", []):
        st = int(scene_start(sc))
        mm = st // 60
        ss = st % 60
        title = sc.get("title", f"Cảnh {sc.get('scene_id')}")
        title = re.sub(r"^\d+\s*[•\-]\s*", "", title)
        timestamps.append(f"{mm:02d}:{ss:02d} - {title}")
    return timestamps


def make_metadata(project_dir: str, tl: dict, out_dir: str | None = None) -> str:
    """
    Sinh file mota.txt chuẩn SEO YouTube thống nhất (2 phần: TIÊU ĐỀ YOUTUBE & MÔ TẢ VIDEO)
    cho cả 3 loại video của kênh Điểm Đọc.
    """
    project_name = os.path.basename(project_dir.rstrip("/"))
    if out_dir is None:
        out_dir = os.path.join(paths.OUTPUTS, project_name)
    os.makedirs(out_dir, exist_ok=True)

    out = os.path.join(project_dir, "mota.txt")
    out_pub = os.path.join(out_dir, "mota.txt")
    fmt = (tl.get("format") or "long").lower()

    raw_titles = _generate_seo_titles(tl)
    titles_abc = []
    for item in raw_titles:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            titles_abc.append(str(item[1]))
        else:
            titles_abc.append(str(item))

    chapters: list[tuple[str, str]] = []
    for sc in tl.get("scenes", []):
        st = int(scene_start(sc))
        mm = st // 60
        ss = st % 60
        title = sc.get("title", f"Phần {sc.get('scene_id')}")
        title = re.sub(r"^\d+\s*[•\-]\s*", "", title).strip()
        chapters.append((f"{mm:02d}:{ss:02d}", title))

    desc_custom = tl.get("seo_description")
    intro_paragraphs = None
    if desc_custom:
        if isinstance(desc_custom, list):
            intro_paragraphs = [str(x) for x in desc_custom if str(x).strip()]
        else:
            intro_paragraphs = [p.strip() for p in str(desc_custom).split("\n\n") if p.strip()]

    raw_tags = tl.get("hashtags")
    hashtags = None
    if isinstance(raw_tags, str) and raw_tags.strip():
        hashtags = raw_tags.strip().split()
    elif isinstance(raw_tags, list):
        hashtags = [str(x) for x in raw_tags]

    sources = tl.get("sources", [])
    sources_line = None
    if sources:
        src_names = []
        for s in sources:
            if isinstance(s, dict):
                src_names.append(s.get("title") or s.get("name") or "")
            else:
                src_names.append(str(s))
        src_names = [x.strip() for x in src_names if x.strip()]
        if src_names:
            sources_line = "📰 Nguồn tin & tư liệu: " + ", ".join(src_names) + "."

    from pathlib import Path
    if fmt == "short":
        seo_title = titles_abc[0] if titles_abc else (tl.get("title") or tl.get("topic") or "Điểm Đọc Thể Thao #Shorts")
        write_mota_9x16(
            out_path=Path(out),
            seo_title=seo_title,
            description_paragraphs=intro_paragraphs or [tl.get("topic") or "Tin nóng thể thao cập nhật trên kênh Điểm Đọc."],
            chapters=chapters if len(chapters) > 1 else None,
            sources_line=sources_line,
            hashtags=hashtags,
        )
    else:
        video_type = "thematic_long" if tl.get("hide_date_chip") else "weekly_digest"
        write_mota_16x9(
            out_path=Path(out),
            titles_abc=titles_abc,
            chapters=chapters,
            video_type=video_type,
            intro_paragraphs=intro_paragraphs,
            highlight_bullets=tl.get("seo_highlights"),
            sources_line=sources_line,
            hashtags=hashtags,
            day_str=tl.get("date_str", ""),
        )

    _safe_copy(out, out_pub)
    ok(f"Metadata SEO chuẩn 2 phần: {paths.rel_to_root(out_pub)}")
    return out_pub


# ==========================================================================
# CLI
# ==========================================================================

def main() -> None:
    ap = argparse.ArgumentParser(description="m7 — publish pack cho Điểm Đọc (Thumbnail A/B/C, Subtitles, SEO)")
    ap.add_argument("project")
    ap.add_argument("--only", choices=["thumb", "sub", "meta"], default=None)
    ap.add_argument("--out-dir", default=None, help="Thư mục xuất bản tùy chọn (mặc định: outputs/<project>)")
    args = ap.parse_args()

    banner("M7 — PUBLISH PACK", "Điểm Đọc")
    pdir = paths.project_dir(args.project)
    tl = load_timeline(pdir)

    out_d = args.out_dir

    if args.only in (None, "thumb"):
        step("1/3 — Thumbnail")
        make_thumbnail(pdir, tl, out_dir=out_d)
    if args.only in (None, "sub"):
        step("2/3 — Phụ đề kịch bản tiếng Việt")
        make_vietnamese_sub(pdir, tl, out_dir=out_d)
    if args.only in (None, "meta"):
        step("3/3 — Metadata SEO YouTube")
        make_metadata(pdir, tl, out_dir=out_d)

    print()
    ok("Xuất bản hoàn tất! File đã sẵn sàng trong cả project và outputs/.")


if __name__ == "__main__":
    main()