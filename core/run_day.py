#!/usr/bin/env python3
"""
run_day.py — Hệ Thống Điều Phối Sản Xuất Video Thể Thao ("Điểm Đọc")
===================================================================
Khôi phục 100% Engine FFmpeg/Pillow nguyên bản từ 1-169.py & 1-916.py:

  1. Lệnh PREPARE:
     python3 -B core/run_day.py prepare [--project/--day DD.MM.YYYY] [--since "YYYY-MM-DD HH:MM"]
     - Cào tin tức thể thao sạch (m1_scraper).
     - Tải ảnh gốc & ảnh phụ vào WORK/<day>/images_ready/ (ngoài Drive).
     - LLM biên tập ra file outputs/DD.MM.YYYY/thethao.txt và shorts.txt/shorts.json.
     - DỪNG LẠI CHO CHỦ KÊNH DUYỆT BẢN THẢO.

  2. Lệnh BUILD:
     python3 -B core/run_day.py build [--project/--day DD.MM.YYYY] [--mock-render]
     - Dọn sạch các thư mục tạm trong WORK_DIR.
     - Kiểm tra bắt buộc font/Roboto-Black.ttf và font/Roboto-Regular.ttf (dừng ngay nếu thiếu).
     - BƯỚC 1: Chuyển thethao.txt sang thethao.json (chuẩn mau.json).
       Tạo và chép ảnh vào outputs/DD.MM.YYYY/images/.
     - BƯỚC 2: Sinh/khớp audio ViTTS Minh Quân Pro vào outputs/DD.MM.YYYY/audio/ & audio-title/.
     - BƯỚC 3: Render từng cảnh bằng engine PIL + FFmpeg (100% logic 1-169.py):
       + Smart Ratio: Background blur + Foreground sắc nét có viền trắng và drop shadow.
       + Hiệu ứng Ken Burns (zoompan) trên toàn bộ khung hình composite.
       + Hiệu ứng xfade chuyển cảnh giữa các ảnh minh họa (nếu có nhiều ảnh).
       + Header overlay vẽ bằng PIL (Logo, Thể loại, Ngày, Tiêu đề).
       + Phụ đề (Subtitles) cắt bằng split_chunks, vẽ nền đen mờ bằng create_subtitle_image,
         overlay trực tiếp lên video khớp với nhịp đọc lời bình.
       + Lưu từng chunk vào WORK_DIR/video_chunks/.
     - BƯỚC 4: Concat toàn bộ chunks + Intro/Outro thành 1 file MP4 dài duy nhất.
       Mix âm thanh tổng với BGM (mức 0.05).
       Sinh đủ 3 Thumbnail A/B/C 16:9 bằng create_static_overlay và mota.txt chuẩn SEO YouTube.
     - BƯỚC 5: Render Video Shorts 9:16 (1-916.py) với is_fast_mode=False và thumbnail shorts vào outputs/DD.MM.YYYY/shorts/.
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import glob
import json
import os
import random
import re
import shutil
import subprocess
import textwrap
import time
import io
import requests
import urllib.request
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
from pydub import AudioSegment

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
if os.path.join(_ROOT, "spec") not in sys.path:
    sys.path.insert(0, os.path.join(_ROOT, "spec"))

from diemdoc import paths
from diemdoc.audio import apply_voice_standard
from diemdoc.log import banner, die, err, log, ok, step, warn
from m1b_llm_writer import generate_thethao_txt_file, generate_shorts_files
from diemdoc.tts_text import prepare
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from vieneu import Vieneu

ICT = timezone(timedelta(hours=7))

# Layout Constants 16:9 (1-169.py)
VIDEO_WIDTH, VIDEO_HEIGHT = 1920, 1080
VIDEO_FPS = 30

HEADER_TOP_PCT = 0.05
HEADER_PAD = 20
LOGO_SIZE = (90, 90)
LOGO_BG_SIDE = LOGO_SIZE[0] + 20
LOGO_BG_LEFT_PCT = 0.02

TITLE_FONT_SIZE = 36
DATE_FONT_SIZE = 32

SUB_FONT_SIZE = 30
SUB_BOTTOM_PCT = 0.08
GRADIENT_HEIGHT_PCT = 0.25

TRANS_DUR = 0.8
TITLE_GAP_SEC = 0.5

INTRO_NAME = "Intro.mp4"
OUTRO_NAMES = ["Outro.mp4", "Ontro.mp4"]
LOGO_IMAGE_CANDS = ["logo/logo.png", "logo/Logo.png", "logo.png"]
PARTICLE_NAME = "Lopphu.mp4"

# Layout Constants 9:16 (1-916.py)
VIDEO_WIDTH_916, VIDEO_HEIGHT_916 = 1080, 1920
TOP_REGION_PCT = 0.15
TOP_SAFE_PCT = 0.05
TOP_REGION_H = int(VIDEO_HEIGHT_916 * TOP_REGION_PCT)
TOP_SAFE_H = int(VIDEO_HEIGHT_916 * TOP_SAFE_PCT)
TOP_CONTENT_H = TOP_REGION_H - TOP_SAFE_H

BOT_REGION_PCT = 0.20
BOT_SAFE_PCT = 0.10
BOT_REGION_H = int(VIDEO_HEIGHT_916 * BOT_REGION_PCT)
BOT_SAFE_H = int(VIDEO_HEIGHT_916 * BOT_SAFE_PCT)
BOT_CONTENT_H = BOT_REGION_H - BOT_SAFE_H

IMG_AREA_H = VIDEO_HEIGHT_916 - TOP_REGION_H - BOT_REGION_H
IMG_AREA_W = VIDEO_WIDTH_916
IMG_AREA_Y = TOP_REGION_H

SUB_FONT_SIZE_916 = 44
TITLE_FONT_SIZE_916 = 48
DATE_FONT_SIZE_916 = 36
MODE_LABEL_FONT_SIZE_916 = 32
TOPIC_FONT_SIZE_916 = 52

# Paths to Fonts
FONT_BOLD = os.path.join(_ROOT, "font", "Roboto-Black.ttf")
FONT_REGULAR = os.path.join(_ROOT, "font", "Roboto-Regular.ttf")

# ==============================================================================
# KIỂM TRA BẮT BUỘC TÀI NGUYÊN (FONTS & LOGOS)
# ==============================================================================

def verify_assets_or_die() -> None:
    """Kiểm tra bắt buộc sự tồn tại của font và logo. Tuyệt đối không fallback font mặc định!"""
    if not os.path.exists(FONT_BOLD):
        die(f"LỖI NGHIÊM TRỌNG: Không tìm thấy font {FONT_BOLD}! Bắt buộc có Roboto-Black.ttf!")
    if not os.path.exists(FONT_REGULAR):
        die(f"LỖI NGHIÊM TRỌNG: Không tìm thấy font {FONT_REGULAR}! Bắt buộc có Roboto-Regular.ttf!")

    logo_file = os.path.join(_ROOT, "logo", "logo.png")
    intro_file = os.path.join(_ROOT, "logo", "Intro.mp4")
    outro_file = os.path.join(_ROOT, "logo", "Outro.mp4")
    particle_file = os.path.join(_ROOT, "logo", "Lopphu.mp4")

    if not os.path.exists(logo_file):
        die(f"LỖI NGHIÊM TRỌNG: Thiếu file {logo_file}!")
    if not os.path.exists(intro_file):
        die(f"LỖI NGHIÊM TRỌNG: Thiếu file {intro_file}!")
    if not os.path.exists(outro_file):
        die(f"LỖI NGHIÊM TRỌNG: Thiếu file {outro_file}!")
    if not os.path.exists(particle_file):
        die(f"LỖI NGHIÊM TRỌNG: Thiếu file {particle_file}!")

    log(f"✅ Đã nạp đầy đủ Assets: Roboto-Black.ttf, Roboto-Regular.ttf, logo.png, Lopphu.mp4, Intro.mp4, Outro.mp4", tag="assets")


# ==============================================================================
# HÀM BỔ TRỢ HỆ THỐNG & ENCODER
# ==============================================================================

def get_encoder_settings() -> Tuple[str, List[str]]:
    ff = shutil.which("ffmpeg")
    if not ff:
        return "libx264", ["-preset", "veryfast"]
    try:
        res = subprocess.check_output([ff, "-hide_banner", "-encoders"], text=True, stderr=subprocess.STDOUT)
    except Exception:
        return "libx264", ["-preset", "veryfast"]
    if "h264_videotoolbox" in res:
        return "h264_videotoolbox", ["-b:v", "6500k", "-allow_sw", "1"]
    if "h264_nvenc" in res:
        return "h264_nvenc", ["-preset", "p4", "-b:v", "6500k"]
    return "libx264", ["-preset", "veryfast", "-crf", "22"]


ENCODER, ENCODER_PARAMS = get_encoder_settings()


def exec_module(module_name: str, args: List[str], check: bool = True) -> int:
    script = os.path.join(_HERE, module_name)
    cmd = [sys.executable, "-B", script] + args
    log(f"Thực thi: python3 -B core/{module_name} {' '.join(args)}", tag="exec")
    p = subprocess.run(cmd)
    if check and p.returncode != 0:
        die(f"Mô-đun {module_name} thất bại (Exit code {p.returncode}). Dừng pipeline!")
    return p.returncode


def get_default_day() -> str:
    return paths.get_today_dir_name()


def resolve_day_str(args: argparse.Namespace) -> str:
    raw = getattr(args, "project", None) or getattr(args, "day", None) or getattr(args, "date", None)
    if not raw:
        return get_default_day()
    raw = str(raw).strip()
    m_iso = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", raw)
    if m_iso:
        y, m, d = int(m_iso.group(1)), int(m_iso.group(2)), int(m_iso.group(3))
        return f"{d:02d}.{m:02d}.{y:04d}"
    m_dd = re.match(r"^(\d{1,2})\.(\d{1,2})\.(\d{4})$", raw)
    if m_dd:
        d, m, y = int(m_dd.group(1)), int(m_dd.group(2)), int(m_dd.group(3))
        return f"{d:02d}.{m:02d}.{y:04d}"
    return raw


def get_audio_duration(path: str) -> float:
    if not path or not os.path.exists(path):
        return 0.0
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path]
    try:
        return float(subprocess.check_output(cmd).strip())
    except Exception:
        try:
            return float(len(AudioSegment.from_file(path)) / 1000.0)
        except Exception:
            return 0.0


def fmt_date_from_day(day_dir: str) -> str:
    n = os.path.basename(day_dir)
    parts = n.split(".")
    if len(parts) >= 3:
        return f"{parts[0]}/{parts[1]}/{parts[2]}"
    return datetime.now().strftime("%d/%m/%Y")


# ==============================================================================
# HÀM XỬ LÝ ẢNH & OVERLAY NGUYÊN BẢN TỪ 1-169.py
# ==============================================================================

_word_re = re.compile(r"\S+")
_sentence_splitter = re.compile(r"(?<!\d)[.!?]+(?!\d)\s+")
_comma_not_numeric = re.compile(r"(?<!\d),(?!\s*\d)")


def split_chunks(text: str) -> List[str]:
    """Cắt văn bản thành các cụm phụ đề ngắn gọn 6-12 từ theo đúng 1-169.py."""
    t = (text or "").strip()
    if not t:
        return []
    sents = re.split(_sentence_splitter, t)
    sents = [s.strip() for s in sents if s.strip()]
    out = []
    for s in sents:
        parts = [p.strip() for p in _comma_not_numeric.split(s) if p.strip()] or [s]
        for p in parts:
            ws = _word_re.findall(p)
            i = 0
            while i < len(ws):
                n = min(12, max(6, len(ws) - i))
                if len(ws) - (i + n) < 6:
                    n = len(ws) - i
                out.append(" ".join(ws[i:i + n]))
                i += n
    return out


def add_drop_shadow(img, offset=(0, 0), background_color=(0, 0, 0, 0), shadow_color=(0, 0, 0, 150), border_width=0):
    w, h = img.size
    if border_width > 0:
        new_w = w + 2 * border_width
        new_h = h + 2 * border_width
        img_border = Image.new("RGBA", (new_w, new_h), (255, 255, 255, 255))
        img_border.paste(img, (border_width, border_width))
        img = img_border
        w, h = img.size

    shadow_blur = 20
    shadow_offset = 10
    total_w = w + shadow_blur * 2 + shadow_offset
    total_h = h + shadow_blur * 2 + shadow_offset

    back = Image.new("RGBA", (total_w, total_h), background_color)
    shadow = Image.new("RGBA", (w, h), shadow_color)

    shadow_left = shadow_blur + shadow_offset // 2
    shadow_top = shadow_blur + shadow_offset // 2
    back.paste(shadow, (shadow_left, shadow_top), mask=shadow)
    back = back.filter(ImageFilter.GaussianBlur(shadow_blur))

    img_left = shadow_blur
    img_top = shadow_blur
    back.paste(img, (img_left, img_top), mask=img if img.mode == "RGBA" else None)
    return back


def create_blur_bg(img_path):
    try:
        img = Image.open(img_path).convert("RGB")
        ratio = max(VIDEO_WIDTH / img.width, VIDEO_HEIGHT / img.height)
        new_size = (int(img.width * ratio) + 1, int(img.height * ratio) + 1)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        left = (img.width - VIDEO_WIDTH) // 2
        top = (img.height - VIDEO_HEIGHT) // 2
        img = img.crop((left, top, left + VIDEO_WIDTH, top + VIDEO_HEIGHT))
        img = img.filter(ImageFilter.GaussianBlur(30))
        img = ImageEnhance.Brightness(img).enhance(0.6)
        return img
    except Exception:
        return Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), (20, 20, 20))


def analyze_and_prepare_image(img_path, temp_dir, index, duration):
    try:
        im = Image.open(img_path).convert("RGBA")
        w_orig, h_orig = im.size
        ratio = w_orig / h_orig

        if w_orig < 600 or h_orig < 400:
            case_id = 6
        elif ratio < 0.5:
            case_id = 5
        elif 0.5 <= ratio < 1.0:
            case_id = 4
        elif 1.0 <= ratio < 1.6:
            case_id = 3
        elif 1.6 <= ratio <= 1.9:
            case_id = 1
        else:
            case_id = 2

        bg_path = os.path.join(temp_dir, f"bg_{index}.jpg")
        fg_path = os.path.join(temp_dir, f"fg_{index}.png")

        bg_img = create_blur_bg(img_path)
        bg_img.save(bg_path, quality=90)

        fg_w, fg_h = 0, 0

        if case_id == 1:
            im_cover = ImageOps.fit(im.convert("RGB"), (VIDEO_WIDTH, VIDEO_HEIGHT), method=Image.Resampling.LANCZOS)
            im_cover.save(fg_path)
            fg_w, fg_h = VIDEO_WIDTH, VIDEO_HEIGHT
        elif case_id == 2:
            new_h = VIDEO_HEIGHT
            new_w = int(w_orig * (VIDEO_HEIGHT / h_orig))
            im_r = im.convert("RGB").resize((new_w, new_h), Image.Resampling.LANCZOS)
            im_r.save(fg_path)
            fg_w, fg_h = new_w, new_h
        elif case_id == 3:
            new_w = VIDEO_WIDTH
            new_h = int(h_orig * (VIDEO_WIDTH / w_orig))
            if (new_h - VIDEO_HEIGHT) < 100:
                case_id = 1
                im_cover = ImageOps.fit(im.convert("RGB"), (VIDEO_WIDTH, VIDEO_HEIGHT), method=Image.Resampling.LANCZOS)
                im_cover.save(fg_path)
                fg_w, fg_h = VIDEO_WIDTH, VIDEO_HEIGHT
            else:
                im_r = im.convert("RGB").resize((new_w, new_h), Image.Resampling.LANCZOS)
                im_r.save(fg_path)
                fg_w, fg_h = new_w, new_h
        elif case_id == 4:
            target_w = int(VIDEO_WIDTH * 0.7)
            new_w = target_w
            new_h = int(h_orig * (target_w / w_orig))
            im_r = im.convert("RGB").resize((new_w, new_h), Image.Resampling.LANCZOS)
            im_shadow = add_drop_shadow(im_r, border_width=4)
            im_shadow.save(fg_path)
            fg_w, fg_h = im_shadow.size
        elif case_id == 5:
            new_w = VIDEO_WIDTH
            new_h = int(h_orig * (VIDEO_WIDTH / w_orig))
            im_r = im.convert("RGB").resize((new_w, new_h), Image.Resampling.LANCZOS)
            im_r.save(fg_path)
            fg_w, fg_h = new_w, new_h
        elif case_id == 6:
            scale = 1.5
            new_w = int(w_orig * scale)
            new_h = int(h_orig * scale)
            im_r = im.convert("RGB").resize((new_w, new_h), Image.Resampling.LANCZOS)
            im_shadow = add_drop_shadow(im_r, border_width=6)
            im_shadow.save(fg_path)
            fg_w, fg_h = im_shadow.size

        return case_id, bg_path, fg_path, fg_w, fg_h
    except Exception:
        return 1, "", "", VIDEO_WIDTH, VIDEO_HEIGHT


def create_static_overlay(day_dir: str, title: str, output_path: str):
    """Vẽ header và vignette chính xác 100% theo 1-169.py."""
    img = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Vignette
    vig_mask = Image.new("L", (VIDEO_WIDTH, VIDEO_HEIGHT), 0)
    v_draw = ImageDraw.Draw(vig_mask)
    cx, cy = VIDEO_WIDTH // 2, VIDEO_HEIGHT // 2
    rx, ry = VIDEO_WIDTH * 0.8, VIDEO_HEIGHT * 0.9
    v_draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=255)
    vig_mask = vig_mask.filter(ImageFilter.GaussianBlur(100))
    vig_arr = np.array(vig_mask)
    alpha_layer = 255 - vig_arr
    alpha_layer = (alpha_layer * 0.4).astype(np.uint8)
    black = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    black.paste((0, 0, 0), [0, 0, VIDEO_WIDTH, VIDEO_HEIGHT])
    black.putalpha(Image.fromarray(alpha_layer))
    img.alpha_composite(black)

    # 2. Gradient mờ đáy
    grad_h = int(VIDEO_HEIGHT * GRADIENT_HEIGHT_PCT)
    grad_y_start = VIDEO_HEIGHT - grad_h
    grad_img = Image.new("L", (VIDEO_WIDTH, grad_h), 0)
    for y in range(grad_h):
        alpha = int(220 * (y / grad_h))
        ImageDraw.Draw(grad_img).line([(0, y), (VIDEO_WIDTH, y)], fill=alpha)
    bottom_overlay = Image.new("RGBA", (VIDEO_WIDTH, grad_h), (0, 0, 0, 0))
    bottom_black = Image.new("RGB", (VIDEO_WIDTH, grad_h), (0, 0, 0))
    bottom_overlay.paste(bottom_black, mask=grad_img)
    img.alpha_composite(bottom_overlay, (0, grad_y_start))

    # 3. Logo box
    y_top = int(HEADER_TOP_PCT * VIDEO_HEIGHT)
    x_bg = int(LOGO_BG_LEFT_PCT * VIDEO_WIDTH)
    draw.rectangle([x_bg, y_top, x_bg + LOGO_BG_SIDE, y_top + LOGO_BG_SIDE], fill=(0, 0, 0, 140))

    logo_path = None
    for p in LOGO_IMAGE_CANDS:
        full_p = os.path.join(_ROOT, p)
        if os.path.exists(full_p):
            logo_path = full_p
            break
    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((LOGO_SIZE[0], LOGO_SIZE[1]), Image.Resampling.BICUBIC)
            lx = x_bg + (LOGO_BG_SIDE - logo.width) // 2
            ly = y_top + (LOGO_BG_SIDE - logo.height) // 2
            img.alpha_composite(logo, (lx, ly))
        except Exception:
            pass

    box_center_y = y_top + LOGO_BG_SIDE // 2

    def draw_txt_centered(txt, font_p, size, x, align, w_lim, center_ref_y):
        font = ImageFont.truetype(font_p, size)
        lines = textwrap.wrap(txt, width=int(w_lim / (size * 0.48)))
        line_heights = []
        line_gap = 6
        for ln in lines:
            bbox = draw.textbbox((0, 0), ln, font=font)
            h = bbox[3] - bbox[1]
            line_heights.append(h)
        total_h = sum(line_heights) + line_gap * (len(lines) - 1)
        lift_px = 8
        start_y = center_ref_y - (total_h // 2) - lift_px
        curr_y = start_y
        for i, ln in enumerate(lines):
            bbox = draw.textbbox((0, 0), ln, font=font)
            w = bbox[2] - bbox[0]
            dx = x
            if align == "right":
                dx = x + w_lim - w
            elif align == "center":
                dx = x + (w_lim - w) // 2
            draw.text((dx + 2, curr_y + 2), ln, font=font, fill=(0, 0, 0, 160))
            draw.text((dx, curr_y), ln, font=font, fill="white")
            curr_y += line_heights[i] + line_gap

    date_str = fmt_date_from_day(day_dir)
    date_w = int(VIDEO_WIDTH * 0.25)
    date_x = VIDEO_WIDTH - date_w - HEADER_PAD
    draw_txt_centered(f"({date_str})", FONT_BOLD, DATE_FONT_SIZE, date_x, "right", date_w, box_center_y)

    x_left = x_bg + LOGO_BG_SIDE + HEADER_PAD
    title_w = VIDEO_WIDTH - x_left - date_w - HEADER_PAD - 20
    draw_txt_centered(title, FONT_BOLD, TITLE_FONT_SIZE, x_left, "left", title_w, box_center_y)
    img.save(output_path)


def create_subtitle_image(text, w, output_path):
    """Vẽ phụ đề chính xác 100% theo 1-169.py."""
    img = Image.new("RGBA", (w, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_REGULAR, SUB_FONT_SIZE)
    lines = textwrap.wrap(text, width=int(w / (SUB_FONT_SIZE * 0.5)))
    y = 0
    total_h = 0
    for ln in lines:
        bbox = d.textbbox((0, 0), ln, font=font)
        lw, lh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (w - lw) // 2
        d.text((x + 2, y + 2), ln, font=font, fill=(0, 0, 0, 200))
        d.text((x, y), ln, font=font, fill="white")
        y += lh + 10
        total_h = y
    if total_h == 0:
        total_h = 10
    final = img.crop((0, 0, w, total_h))
    final.save(output_path)
    return total_h


def collect_images(item: dict) -> List[str]:
    pairs = []
    for k, v in item.items():
        if isinstance(k, str) and k.lower().startswith("image_") and isinstance(v, str) and v.strip():
            try:
                idx = int(k.split("_", 1)[1])
            except Exception:
                continue
            pairs.append((idx, v.strip()))
    if pairs:
        pairs.sort(key=lambda x: x[0])
        valid = [p for _, p in pairs if os.path.exists(p)]
        # Lọc ảnh duy nhất để kích hoạt xfade đúng cách
        unique = []
        for p in valid:
            if p not in unique:
                unique.append(p)
        if unique:
            return unique
    ip = item.get("image_path")
    if isinstance(ip, str) and ip.strip() and os.path.exists(ip):
        return [ip]
    return [os.path.join(_ROOT, "logo", "logo.png")]


# ==============================================================================
# HÀM XỬ LÝ ẢNH & OVERLAY NGUYÊN BẢN TỪ 1-916.py (SHORTS 9:16)
# ==============================================================================

def draw_text_with_style_916(draw, pos, text, font, fill_color="white", stroke_color="black"):
    x, y = pos
    shadow_off = 3
    draw.text((x + shadow_off, y + shadow_off), text, font=font, fill=(0, 0, 0, 120))
    draw.text((x, y), text, font=font, fill=fill_color, stroke_width=2, stroke_fill=stroke_color)


def create_blur_bg_vertical(img_path):
    try:
        img = Image.open(img_path).convert("RGB")
        ratio = max(IMG_AREA_W / img.width, IMG_AREA_H / img.height)
        new_size = (int(img.width * ratio) + 1, int(img.height * ratio) + 1)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        left = (img.width - IMG_AREA_W) // 2
        top = (img.height - IMG_AREA_H) // 2
        img = img.crop((left, top, left + IMG_AREA_W, top + IMG_AREA_H))
        img = img.filter(ImageFilter.GaussianBlur(40))
        img = ImageEnhance.Brightness(img).enhance(0.5)
        return img
    except Exception:
        return Image.new("RGB", (IMG_AREA_W, IMG_AREA_H), (20, 20, 20))


def analyze_and_prepare_image_916(img_path, temp_dir, index, is_fast_mode):
    try:
        im = Image.open(img_path).convert("RGBA")
        w_orig, h_orig = im.size
        ratio = w_orig / h_orig

        if ratio > 1.0:
            case_id = 1
        elif ratio < 0.7:
            case_id = 2
        else:
            case_id = 3

        if is_fast_mode and case_id == 1 and ratio > 1.3:
            case_id = 3

        bg_path = os.path.join(temp_dir, f"bg_{index}.jpg")
        fg_path = os.path.join(temp_dir, f"fg_{index}.png")

        bg_img = create_blur_bg_vertical(img_path)
        bg_img.save(bg_path, quality=90)

        fg_w, fg_h = 0, 0

        if case_id == 1:
            new_h = IMG_AREA_H
            new_w = int(w_orig * (IMG_AREA_H / h_orig))
            im_r = im.convert("RGB").resize((new_w, new_h), Image.Resampling.LANCZOS)
            im_r.save(fg_path)
            fg_w, fg_h = new_w, new_h
        elif case_id == 2:
            new_w = IMG_AREA_W
            new_h = int(h_orig * (IMG_AREA_W / w_orig))
            im_r = im.convert("RGB").resize((new_w, new_h), Image.Resampling.LANCZOS)
            im_r.save(fg_path)
            fg_w, fg_h = new_w, new_h
        elif case_id == 3:
            im_cover = ImageOps.fit(im.convert("RGB"), (IMG_AREA_W, IMG_AREA_H), method=Image.Resampling.LANCZOS)
            im_cover.save(fg_path)
            fg_w, fg_h = IMG_AREA_W, IMG_AREA_H

        return case_id, bg_path, fg_path, fg_w, fg_h
    except Exception:
        return 3, "", "", IMG_AREA_W, IMG_AREA_H


def create_static_overlay_916(day_dir: str, title: str, topic_text: str, mode_label: str, output_path: str):
    """Vẽ overlay tĩnh 9:16 chính xác theo 1-916.py."""
    img = Image.new("RGBA", (VIDEO_WIDTH_916, VIDEO_HEIGHT_916), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    top_grad = Image.new("L", (VIDEO_WIDTH_916, TOP_CONTENT_H), 0)
    g_draw = ImageDraw.Draw(top_grad)
    for i in range(TOP_CONTENT_H):
        alpha = int(200 * (1 - i / TOP_CONTENT_H))
        g_draw.line([(0, i), (VIDEO_WIDTH_916, i)], fill=alpha)

    top_overlay = Image.new("RGBA", (VIDEO_WIDTH_916, TOP_CONTENT_H), (0, 0, 0, 0))
    top_black = Image.new("RGB", (VIDEO_WIDTH_916, TOP_CONTENT_H), (0, 0, 0))
    top_overlay.paste(top_black, mask=top_grad)
    img.paste(top_overlay, (0, TOP_SAFE_H))

    bot_grad = Image.new("L", (VIDEO_WIDTH_916, BOT_CONTENT_H), 0)
    g_draw = ImageDraw.Draw(bot_grad)
    for i in range(BOT_CONTENT_H):
        alpha = int(200 * (i / BOT_CONTENT_H))
        g_draw.line([(0, i), (VIDEO_WIDTH_916, i)], fill=alpha)

    bot_overlay = Image.new("RGBA", (VIDEO_WIDTH_916, BOT_CONTENT_H), (0, 0, 0, 0))
    bot_black = Image.new("RGB", (VIDEO_WIDTH_916, BOT_CONTENT_H), (0, 0, 0))
    bot_overlay.paste(bot_black, mask=bot_grad)
    img.paste(bot_overlay, (0, VIDEO_HEIGHT_916 - BOT_REGION_H))

    header_cy = TOP_SAFE_H + TOP_CONTENT_H // 2

    logo_path = None
    for p in LOGO_IMAGE_CANDS:
        full_p = os.path.join(_ROOT, p)
        if os.path.exists(full_p):
            logo_path = full_p
            break
    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            max_h = int(TOP_CONTENT_H * 0.65)
            ratio = max_h / logo.height
            logo = logo.resize((int(logo.width * ratio), max_h), Image.Resampling.BICUBIC)
            img.alpha_composite(logo, (40, header_cy - max_h // 2))
        except Exception:
            pass

    date_str = fmt_date_from_day(day_dir)
    f_date = ImageFont.truetype(FONT_REGULAR, DATE_FONT_SIZE_916)
    bbox_d = draw.textbbox((0, 0), date_str, font=f_date)
    w_d, h_d = bbox_d[2] - bbox_d[0], bbox_d[3] - bbox_d[1]
    draw_text_with_style_916(draw, (VIDEO_WIDTH_916 - w_d - 40, header_cy - h_d // 2), date_str, f_date)

    f_mode = ImageFont.truetype(FONT_REGULAR, MODE_LABEL_FONT_SIZE_916)
    f_topic = ImageFont.truetype(FONT_BOLD, TOPIC_FONT_SIZE_916)

    bbox_m = draw.textbbox((0, 0), mode_label, font=f_mode)
    h_m = bbox_m[3] - bbox_m[1]
    bbox_t = draw.textbbox((0, 0), topic_text, font=f_topic)
    h_t = bbox_t[3] - bbox_t[1]

    total_h = h_m + h_t + 8
    start_y = header_cy - total_h // 2

    w_m = bbox_m[2] - bbox_m[0]
    draw_text_with_style_916(draw, ((VIDEO_WIDTH_916 - w_m) // 2, start_y), mode_label, f_mode, fill_color="#FFD700")

    w_t = bbox_t[2] - bbox_t[0]
    draw_text_with_style_916(draw, ((VIDEO_WIDTH_916 - w_t) // 2, start_y + h_m + 8), topic_text, f_topic)

    footer_cy = VIDEO_HEIGHT_916 - BOT_REGION_H + BOT_CONTENT_H // 2
    f_title = ImageFont.truetype(FONT_BOLD, TITLE_FONT_SIZE_916)

    max_w = VIDEO_WIDTH_916 - 80
    lines = textwrap.wrap(title, width=int(max_w / (TITLE_FONT_SIZE_916 * 0.5)))[:3]

    line_heights = [draw.textbbox((0, 0), ln, font=f_title)[3] - draw.textbbox((0, 0), ln, font=f_title)[1] for ln in lines]
    total_txt_h = sum(line_heights) + 12 * (len(lines) - 1)

    curr_y = footer_cy - total_txt_h // 2

    for i, ln in enumerate(lines):
        bbox = draw.textbbox((0, 0), ln, font=f_title)
        w = bbox[2] - bbox[0]
        x = (VIDEO_WIDTH_916 - w) // 2
        draw_text_with_style_916(draw, (x, curr_y), ln, f_title)
        curr_y += line_heights[i] + 12

    img.save(output_path)


def create_subtitle_image_916(text, w, output_path):
    """Vẽ phụ đề 9:16 có viền đen mờ 8 hướng chính xác theo 1-916.py."""
    img = Image.new("RGBA", (w, 250), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, SUB_FONT_SIZE_916)

    lines = textwrap.wrap(text, width=int(w / (SUB_FONT_SIZE_916 * 0.5)))[:2]
    y = 0
    total_h = 0
    for ln in lines:
        bbox = d.textbbox((0, 0), ln, font=font)
        lw, lh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (w - lw) // 2

        for off in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
            d.text((x + off[0], y + off[1]), ln, font=font, fill="black")

        d.text((x, y), ln, font=font, fill="white")
        y += lh + 12
        total_h = y

    if total_h == 0:
        total_h = 10
    final = img.crop((0, 0, w, total_h))
    final.save(output_path)
    return total_h


# ==============================================================================
# BƯỚC 1: PREPARE
# ==============================================================================

def cmd_prepare(args: argparse.Namespace) -> None:
    verify_assets_or_die()
    day_str = resolve_day_str(args)
    day_dir = paths.project_dir(day_str)
    work_dir = paths.work_project_dir(day_str)
    os.makedirs(day_dir, exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)

    banner("RUN_DAY: BƯỚC 1 — CHUẨN BỊ NỘI DUNG (PREPARE)", f"Ngày {day_str}")
    t0 = time.time()

    step("1.1. Thu thập & lọc tin tức thể thao (m1_scraper)...")
    raw_news_file = paths.work_file("temp_raw_news.json")
    if getattr(args, "test", False) and os.path.exists(raw_news_file) and os.path.getsize(raw_news_file) > 200:
        ok(f"Chế độ --test: Tái sử dụng dữ liệu tin bài có sẵn tại {raw_news_file}.")
    else:
        scraper_args = []
        if getattr(args, "period", None):
            scraper_args.extend(["--period", args.period])
        if getattr(args, "since", None):
            scraper_args.extend(["--since", args.since])
        if getattr(args, "until", None):
            scraper_args.extend(["--until", args.until])
        if getattr(args, "test", False):
            scraper_args.append("--test")
        exec_module("m1_scraper.py", scraper_args)
        ok("Đã cào và lưu trữ tin bài sạch vào temp_raw_news.json.")

    with open(raw_news_file, "r", encoding="utf-8") as f:
        raw_news = json.load(f)

    articles = raw_news.get("articles", [])
    log(f"Tìm thấy {len(articles)} bài báo thể thao được chọn lọc.")

    step(f"1.2. Tải ảnh bìa & ảnh minh họa HD sạch logo vào WORK/{day_str}/images_ready/...")
    img_dir = os.path.join(work_dir, "images_ready")
    os.makedirs(img_dir, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0"}

    def _download_hd_clean(url_src: Optional[str], dest_path: str) -> None:
        if not url_src or os.path.exists(dest_path):
            return
        low = url_src.lower()
        if any(b in low for b in ("wm1-", "watermark", "gettyimages", "alamy", "shutterstock", "istock", "dreamstime", "logo")):
            return
        try:
            req = urllib.request.Request(get_high_res_url(url_src) or url_src, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw_bytes = resp.read()
            with Image.open(io.BytesIO(raw_bytes)) as im_chk:
                if im_chk.width < 800 or im_chk.height < 450:
                    return
            with open(dest_path, "wb") as f_out:
                f_out.write(raw_bytes)
        except Exception:
            pass

    for idx, art in enumerate(articles, 1):
        art_id = art.get("id") or f"art_{idx:02d}"
        cover = art.get("cover_image", {})
        c_url = cover.get("url") if isinstance(cover, dict) else None
        if c_url:
            _download_hd_clean(c_url, os.path.join(img_dir, f"{art_id}_cover.jpg"))
        for s_idx, s_img in enumerate(art.get("images", [])[:3], 1):
            s_url = s_img.get("url") if isinstance(s_img, dict) else None
            if s_url and s_url != c_url:
                _download_hd_clean(s_url, os.path.join(img_dir, f"{art_id}_sub_{s_idx}.jpg"))

    step(f"1.3. Xuất bản thảo 16:9 (outputs/{day_str}/thethao.txt)...")
    txt_path = os.path.join(day_dir, "thethao.txt")
    generate_thethao_txt_file(day_str, txt_path)

    step(f"1.4. Xuất kịch bản 9:16 (outputs/{day_str}/shorts.txt & shorts.json)...")
    shorts_txt_path = os.path.join(day_dir, "shorts.txt")
    shorts_json_path = os.path.join(day_dir, "shorts.json")
    generate_shorts_files(day_str, shorts_txt_path, shorts_json_path)

    ok(f"BƯỚC CHUẨN BỊ (PREPARE) HOÀN TẤT trong {time.time() - t0:.1f}s!")


def get_high_res_url(url: str) -> str:
    """Loại bỏ các tiền tố thumbnail của các báo VN để lấy ảnh gốc độ phân giải cao (2048x1366 / 2560x1706)."""
    if not url:
        return ""
    # VNExpress: /thumb_w/\d+/ -> /
    url = re.sub(r'/thumb_w/\d+/', '/', url)
    # Dân Trí / Tuổi Trẻ: /zoom/\d+_\d+/ -> /
    url = re.sub(r'/zoom/\d+_\d+/', '/', url)
    return url


def download_image_bytes(url: str, timeout: int = 15) -> bytes:
    """Tải bytes ảnh qua requests với headers đầy đủ."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.content


def open_image_from_bytes(data: bytes) -> Image.Image:
    """Mở PIL Image từ bytes an toàn."""
    return Image.open(io.BytesIO(data))


def extract_search_keyword(title: str) -> str:
    """Trích xuất từ khóa tìm kiếm đại diện cho đội bóng / cầu thủ từ tiêu đề bản tin."""
    known_entities = [
        'Công an Hà Nội', 'CAHN', 'Hà Nội FC', 'Hoàng Anh Gia Lai', 'HAGL', 'Ninh Bình', 'Thể Công Viettel',
        'Viettel', 'Thành phố Đồng Nai', 'Bắc Ninh', 'Nam Định', 'Thanh Hóa', 'Hải Phòng', 'SLNA',
        'Đoàn Văn Hậu', 'Quang Hải', 'Hoàng Đức', 'Công Phượng', 'Tuấn Anh', 'Văn Toàn', 'Tiến Linh',
        'Kim Sang-sik', 'Cristiano Roland', 'Trần Quốc Tuấn', 'Madam Pang', 'Jay Idzes', 'Olaha',
        'Persib Bandung', 'Kashima Antlers', 'Kyrgyzstan', 'Đài Loan', 'Nhật Bản', 'Malaysia', 'Indonesia',
        'U17 Việt Nam', 'Tuyển Việt Nam', 'Việt Nam', 'PSG', 'Manchester City', 'Man City', 'Manchester United',
        'Man Utd', 'Barcelona', 'Inter Miami', 'Messi', 'Ronaldo', 'Al Nassr', 'Erling Haaland', 'Lisandro Martinez',
        'Louis van Gaal', 'Trần Quyết Chiến', 'McLaren', 'F1'
    ]
    found = []
    for ent in known_entities:
        if re.search(r'\b' + re.escape(ent) + r'\b', title, re.IGNORECASE):
            found.append(ent)
    if found:
        return ' '.join(found[:3]) + ' bóng đá'

    words = title.split()
    props = [re.sub(r'[,.\:;!?\"\'\(\)]', '', w) for w in words]
    props = [w for w in props if w and w[0].isupper() and w.lower() not in ['sau', 'khi', 'tại', 'nếu', 'nhưng', 'trong', 'đây', 'dù', 'trước', 'với', 'chi', 'tiết', 'tiêu', 'đề']]
    if props:
        return ' '.join(props[:4]) + ' bóng đá'
    return ' '.join(words[:5]) + ' bóng đá'


def search_ddgs_images(query: str, max_needed: int = 4) -> List[str]:
    """Tìm ảnh chất lượng cao bổ sung qua ddgs (size=Large) khi bài báo có ít hơn 4 ảnh.
    Đã bổ sung negative keywords để loại trừ hoàn toàn ảnh game, mobile, esports, ads."""
    urls: List[str] = []
    clean_kw = query.strip()
    full_query = f"{clean_kw} thể thao -game -mobile -fc -esports -shopee -lazada"
    forbidden_url_tokens = ["game", "mobile", "esports", "shopee", "lazada", "quangcao", "banner", "fptplay", "tv360", "trailer", "gameplay"]
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.images(full_query, size="Large", max_results=max_needed * 4))
            for r in results:
                u = r.get("image")
                if not u:
                    continue
                u_lower = u.lower()
                if any(tok in u_lower for tok in forbidden_url_tokens):
                    continue
                try: w = int(r.get("width") or 0)
                except Exception: w = 0
                try: h = int(r.get("height") or 0)
                except Exception: h = 0
                if (w >= 500 or w == 0) and (h >= 500 or h == 0):
                    if u not in urls:
                        urls.append(u)
                        if len(urls) >= max_needed:
                            break
    except Exception as e:
        warn(f"DDGS search lỗi cho '{full_query}': {e}")
    return urls


def step1_download_and_filter_images(day_str: str, day_dir: str, work_dir: str) -> List[Dict[str, Any]]:
    txt_path = os.path.join(day_dir, "thethao.txt")
    if not os.path.exists(txt_path):
        die(f"Không tìm thấy file: {txt_path}. Vui lòng chạy lệnh prepare trước!")

    images_dir = os.path.join(day_dir, "images")
    audio_dir = os.path.join(day_dir, "audio")
    audio_title_dir = os.path.join(day_dir, "audio-title")
    shorts_dir = os.path.join(day_dir, "shorts")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(audio_title_dir, exist_ok=True)
    os.makedirs(shorts_dir, exist_ok=True)

    with open(txt_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    blocks = re.split(r"\n---\n|^---\n", raw_text)
    items: List[Dict[str, Any]] = []
    idx = 1
    logo_fallback = os.path.join(_ROOT, "logo", "logo.png")

    raw_news_file = paths.work_file("temp_raw_news.json")
    articles_map: Dict[str, Any] = {}
    if os.path.exists(raw_news_file):
        try:
            with open(raw_news_file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                articles_map = {a.get("id"): a for a in raw_data.get("articles", []) if a.get("id")}
        except Exception as e:
            warn(f"Không thể đọc temp_raw_news.json: {e}")

    log(f"  [BƯỚC 1] Bắt đầu gom ảnh từ bài báo, lọc >= 500px và tự động tìm bù qua DDGS...", tag="prepare")

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        tin_m = re.search(r"\[TIN\s*(\d+)\](?:\s*-\s*Nhóm:\s*(.+))?", block)
        id_m = re.search(r"ID:\s*([a-zA-Z0-9_-]+)", block)
        title_m = re.search(r"Tiêu đề:\s*(.+)", block)
        detail_m = re.search(r"Chi tiết:\s*(.+)", block, flags=re.DOTALL)

        if not (id_m or title_m):
            continue

        tin_num = tin_m.group(1) if tin_m else f"{idx:02d}"
        group_name = tin_m.group(2).strip() if (tin_m and tin_m.group(2)) else "Tin Nóng"
        art_id = id_m.group(1).strip() if id_m else f"art_{idx:02d}"
        title = title_m.group(1).strip() if title_m else f"Bản tin {tin_num}"

        detail = ""
        if detail_m:
            detail = detail_m.group(1).strip()
            detail = re.sub(r'[\!\?]+$', '.', detail)

        # 1. Gom tất cả link ảnh từ bài báo gốc và gỡ bỏ thumbnail CDN để lấy ảnh camera gốc
        raw_art = articles_map.get(art_id, {})
        urls_to_download: List[str] = []
        cover_info = raw_art.get("cover_image", {})
        c_url = cover_info.get("url") if isinstance(cover_info, dict) else None
        if c_url:
            urls_to_download.append(get_high_res_url(c_url))
        for img_obj in raw_art.get("images", []):
            u = img_obj.get("url") if isinstance(img_obj, dict) else None
            if u:
                u_hr = get_high_res_url(u)
                if u_hr not in urls_to_download:
                    urls_to_download.append(u_hr)

        # 2. Tải và lọc chất lượng: BẮT BUỘC >= 500px VÀ LÀ ẢNH NGANG (ratio >= 1.18)
        forbidden_tokens = ["game", "mobile", "esports", "shopee", "lazada", "quangcao", "banner", "fptplay", "tv360", "trailer", "gameplay", "anniversary"]
        saved_imgs: List[str] = []
        seq = 1
        for u in urls_to_download:
            if any(tok in u.lower() for tok in forbidden_tokens):
                continue
            target_img_name = f"Tin_{idx:02d}_{seq}.jpg"
            target_path = os.path.join(images_dir, target_img_name)
            if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
                try:
                    with Image.open(target_path) as check_im:
                        w, h = check_im.size
                        if w >= 500 and h >= 500 and (w / h) >= 1.18:
                            saved_imgs.append(target_path)
                            seq += 1
                            continue
                except Exception:
                    pass
            try:
                data = download_image_bytes(u)
                pil_img = open_image_from_bytes(data)
                w, h = pil_img.size
                if w >= 500 and h >= 500 and (w / h) >= 1.18:
                    if pil_img.mode in ("RGBA", "LA", "P", "CMYK"):
                        pil_img = pil_img.convert("RGB")
                    pil_img.save(target_path, "JPEG", quality=92, optimize=True)
                    saved_imgs.append(target_path)
                    seq += 1
            except Exception:
                pass

        # 3. Thuật toán Fallback: Nếu ít hơn 4 ảnh, tự động tìm kiếm bổ sung bằng DDGS (size=Large, CHỈ ẢNH NGANG)
        if len(saved_imgs) < 4:
            needed = 4 - len(saved_imgs)
            kw = extract_search_keyword(title)
            log(f"    [Tin {idx:02d}] Chỉ có {len(saved_imgs)} ảnh ngang >=500px. Đang tìm thêm {needed} ảnh ngang: '{kw}'...", tag="search")
            extra_urls = search_ddgs_images(kw, max_needed=needed * 3)
            for eu in extra_urls:
                if len(saved_imgs) >= 5:
                    break
                if any(tok in eu.lower() for tok in forbidden_tokens):
                    continue
                target_img_name = f"Tin_{idx:02d}_{seq}.jpg"
                target_path = os.path.join(images_dir, target_img_name)
                try:
                    data = download_image_bytes(eu)
                    pil_img = open_image_from_bytes(data)
                    w, h = pil_img.size
                    if w >= 600 and h >= 400 and (w / h) >= 1.18:
                        if pil_img.mode in ("RGBA", "LA", "P", "CMYK"):
                            pil_img = pil_img.convert("RGB")
                        pil_img.save(target_path, "JPEG", quality=92, optimize=True)
                        saved_imgs.append(target_path)
                        seq += 1
                except Exception:
                    pass

        # 4. Alias cover cho Shorts
        cover_alias = os.path.join(images_dir, f"{art_id}_cover.jpg")
        if saved_imgs:
            shutil.copy2(saved_imgs[0], cover_alias)
        else:
            shutil.copy2(logo_fallback, cover_alias)
            saved_imgs.append(cover_alias)

        sc_num = f"{idx:02d}"
        target_audio = os.path.join(audio_dir, f"audio_{sc_num}.wav")
        target_audio_title = os.path.join(audio_title_dir, f"audio_title_{sc_num}.wav")

        item_dict = {
            "id": str(idx),
            "art_id": art_id,
            "group": group_name,
            "title": title,
            "summary": detail,
            "audio_path": target_audio,
            "audio_title": target_audio_title,
            "image_path": saved_imgs[0],
        }
        for s_i, sp in enumerate(saved_imgs[:6], 1):
            item_dict[f"image_{s_i}"] = sp

        items.append(item_dict)
        idx += 1

    ok(f"  [BƯỚC 1] Đã tải và chuẩn hóa toàn bộ ảnh (>=500px) cho {len(items)} bản tin vào {paths.rel_to_root(images_dir)}/")
    return items


def step1b_map_images_to_json(day_str: str, day_dir: str, items_draft: List[Dict[str, Any]]) -> str:
    images_dir = os.path.join(day_dir, "images")
    logo_fallback = os.path.join(_ROOT, "logo", "logo.png")
    final_items: List[Dict[str, Any]] = []

    for item in items_draft:
        idx_str = str(item.get("id", "1"))
        try:
            idx_num = int(idx_str)
        except Exception:
            idx_num = 1

        # Quét lại thư mục images/ để tìm TẤT CẢ các file dạng Tin_{idx:02d}_{seq}.jpg hoặc Tin_{idx}_{seq}.jpg
        pattern = re.compile(rf"^Tin_{idx_num:02d}_(\d+)\.(jpg|jpeg|png)$|^Tin_{idx_num}_(\d+)\.(jpg|jpeg|png)$", re.IGNORECASE)
        available_imgs: List[str] = []
        try:
            matched = []
            for f in os.listdir(images_dir):
                m = pattern.match(f)
                if m:
                    seq_str = m.group(1) or m.group(3)
                    seq = int(seq_str)
                    full_p = os.path.join(images_dir, f)
                    if os.path.exists(full_p) and os.path.getsize(full_p) > 1000:
                        try:
                            with Image.open(full_p) as test_im:
                                if (test_im.width / test_im.height) >= 1.15:
                                    matched.append((seq, full_p))
                        except Exception:
                            pass
            matched.sort(key=lambda x: x[0])
            available_imgs = [p for _, p in matched]
        except Exception as e:
            warn(f"Lỗi quét thư mục images cho Tin {idx_num}: {e}")
            available_imgs = []

        if not available_imgs:
            # Fallback nếu bị xóa hết
            cover_f = os.path.join(images_dir, f"{item.get('art_id', f'art_{idx_num:02d}')}_cover.jpg")
            if os.path.exists(cover_f) and os.path.getsize(cover_f) > 1000:
                available_imgs.append(cover_f)
            else:
                available_imgs.append(logo_fallback)

        # Xóa các key image_ cũ và gán lại theo toàn bộ ảnh thực tế còn lại
        cleaned_item = {k: v for k, v in item.items() if not (isinstance(k, str) and k.startswith("image_"))}
        cleaned_item["image_path"] = available_imgs[0]
        for s_i, sp in enumerate(available_imgs, 1):
            cleaned_item[f"image_{s_i}"] = sp

        final_items.append(cleaned_item)

    json_path = os.path.join(day_dir, "thethao.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(final_items, f, ensure_ascii=False, indent=2)

    ok(f"  [BƯỚC 1B] Đã quét lại ảnh đã duyệt và xuất kịch bản thethao.json (đầy đủ image_1..N): {paths.rel_to_root(json_path)}")
    return json_path


# ==============================================================================
# BƯỚC 2 BUILD: TẠO AUDIO TỪNG TIN ĐỘC LẬP
# ==============================================================================

def synthesize_text(model: Any, text: str, voice: str, speed: float, pitch: float, cache_dir: str,
                    manual_overrides: Optional[Dict[str, str]] = None, force: bool = False) -> AudioSegment:
    clean_text, _ = prepare(text, manual_overrides=manual_overrides)
    chunks = build_chunks_from_text(clean_text, max_words_per_chunk=60, inter_sentence_pause=0.25)
    combined = AudioSegment.empty()
    for c in chunks:
        if c.get("type") == "pause":
            pause_ms = int(c.get("pause_sec", 0.25) * 1000)
            if pause_ms > 0:
                combined += AudioSegment.silent(duration=pause_ms, frame_rate=44100)
            continue
        c_text = c.get("text", "").strip()
        if not c_text:
            continue
        seg, is_hit = render_chunk_vitts(model, c_text, voice, temperature=0.5, speed=speed, pitch=pitch, cache_dir=cache_dir, use_cache=not force, max_chars=768)
        seg = trim_segment_silence(seg)
        combined += seg
    return combined


def step2_generate_audio(day_str: str, day_dir: str, work_dir: str, json_path: str, force: bool = False, voice_name: str = "primary") -> None:
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    # Nạp cấu hình voice presets chuẩn hệ thống từ config/voice.json
    vcfg = {}
    cfg_voice_path = os.path.join(paths.CONFIG, "voice.json")
    if os.path.exists(cfg_voice_path):
        try:
            with open(cfg_voice_path, "r", encoding="utf-8") as f:
                vcfg = json.load(f)
        except Exception:
            pass

    from m3_voice import resolve_voice_preset
    pcfg = resolve_voice_preset(voice_name, vcfg)
    v_voice = pcfg.get("voice", "Minh Quân Pro")
    v_speed = float(pcfg.get("speed", 1.12))
    v_pitch = float(pcfg.get("pitch", 0.93))
    ok(f"  [BƯỚC 2] Áp dụng giọng đọc hệ thống: {v_voice} (speed={v_speed}, pitch={v_pitch}) [preset={voice_name}]")

    # Nạp manual_overrides.json của ngày (nếu có) — bản đồ display -> say cho TTS
    say_overrides: Dict[str, str] = {}
    overrides_path = os.path.join(day_dir, "manual_overrides.json")
    if os.path.exists(overrides_path):
        try:
            with open(overrides_path, "r", encoding="utf-8") as f:
                raw_ov = json.load(f)
            if isinstance(raw_ov, dict):
                say_overrides = {str(k).strip(): str(v).strip() for k, v in raw_ov.items()
                                 if str(k).strip() and str(v).strip()}
        except Exception:
            warn("  [BƯỚC 2] manual_overrides.json sai định dạng — bỏ qua.")
    if say_overrides:
        ok(f"  [BƯỚC 2] Nạp manual_overrides.json ({len(say_overrides)} mục): "
           + "; ".join(f"\"{k}\" → \"{v}\"" for k, v in say_overrides.items()))
    else:
        log("  [BƯỚC 2] Không có manual_overrides.json — giữ nguyên 100% văn bản gốc cho TTS.")

    out_audio_dir = os.path.join(day_dir, "audio")
    out_title_dir = os.path.join(day_dir, "audio-title")
    os.makedirs(out_audio_dir, exist_ok=True)
    os.makedirs(out_title_dir, exist_ok=True)

    work_audio = os.path.join(work_dir, "audio")
    work_title = os.path.join(work_dir, "audio_title")
    cache_dir = paths.work_file("vitts_cache")
    os.makedirs(cache_dir, exist_ok=True)

    silence_08 = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)
    model: Optional[Vieneu] = None

    for idx, item in enumerate(items, 1):
        sc_num = f"{idx:02d}"
        target_audio = os.path.join(out_audio_dir, f"audio_{sc_num}.wav")
        target_title = os.path.join(out_title_dir, f"audio_title_{sc_num}.wav")

        cached_work_audio = os.path.join(work_audio, f"audio_{sc_num}.wav")
        cached_work_title = os.path.join(work_title, f"audio_title_{sc_num}.wav")

        has_audio = (not force) and os.path.exists(target_audio) and os.path.getsize(target_audio) > 1000
        has_title = (not force) and os.path.exists(target_title) and os.path.getsize(target_title) > 1000

        if not has_audio and (not force) and os.path.exists(cached_work_audio) and os.path.getsize(cached_work_audio) > 1000:
            shutil.copy2(cached_work_audio, target_audio)
            has_audio = True

        if not has_title and (not force) and os.path.exists(cached_work_title) and os.path.getsize(cached_work_title) > 1000:
            shutil.copy2(cached_work_title, target_title)
            has_title = True

        if has_audio and has_title:
            item["audio_path"] = target_audio
            item["audio_title"] = target_title
            continue

        if model is None:
            model = Vieneu(mode="v3turbo")

        seg_title = synthesize_text(model, item["title"], voice=v_voice, speed=v_speed, pitch=v_pitch, cache_dir=cache_dir, manual_overrides=say_overrides, force=force)
        seg_title = seg_title.set_frame_rate(44100).set_channels(2)
        seg_title.export(target_title, format="wav")

        seg_summary = synthesize_text(model, item["summary"], voice=v_voice, speed=v_speed, pitch=v_pitch, cache_dir=cache_dir, manual_overrides=say_overrides, force=force)

        # Chuẩn âm lượng theo MẪU KÊNH (-16 LUFS / TP -1.5, đo từ
        # outputs/_samples/speed_1.15.m4a) — áp trên TỔNG THỂ title+silence+summary
        # để mức nhất quán; KHÔNG dùng normalize(headroom) nữa.
        combined = seg_title + silence_08 + seg_summary
        combined = apply_voice_standard(combined)
        combined = combined.set_frame_rate(44100).set_channels(2)
        combined.export(target_audio, format="wav")

        item["audio_path"] = target_audio
        item["audio_title"] = target_title

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    ok("  [BƯỚC 2] Toàn bộ file Audio và Audio-Title đã sẵn sàng!")


# ==============================================================================
# BƯỚC 3 BUILD: RENDER BẰNG ĐÚNG 100% ENGINE 1-169.py
# ==============================================================================

def process_item_ffmpeg_169(item, day_dir, temp_dir, index):
    """Render 1 clip 16:9 chính xác 100% theo process_item_ffmpeg của 1-169.py."""
    ap = item.get("audio_path")
    if not ap or not os.path.exists(ap):
        return None

    dur = get_audio_duration(ap)
    title = (item.get("title") or "").strip()
    summary = (item.get("summary") or "").strip()
    img_paths = collect_images(item)

    if not img_paths:
        return None

    num_imgs = len(img_paths)
    overlap = TRANS_DUR
    clip_dur = (dur + overlap * (num_imgs - 1)) / num_imgs if num_imgs > 0 else dur
    if clip_dur < overlap + 0.1:
        clip_dur = overlap + 0.1

    overlay_path = os.path.join(temp_dir, f"overlay_{index}.png")
    create_static_overlay(day_dir, title, overlay_path)

    fname = os.path.basename(ap)
    title_audio_path = os.path.join(day_dir, "audio-title", fname)
    if not os.path.exists(title_audio_path) and item.get("audio_title"):
        if os.path.exists(item.get("audio_title")):
            title_audio_path = item.get("audio_title")

    real_title_dur = 0.0
    if os.path.exists(title_audio_path):
        real_title_dur = get_audio_duration(title_audio_path)
    else:
        title_words = len(_word_re.findall(title))
        real_title_dur = max(0.8, title_words * 0.35)

    start_t = min(max(0.0, dur - 0.5), real_title_dur + TITLE_GAP_SEC)

    chunks = split_chunks(summary)
    margin_x = int(0.1 * VIDEO_WIDTH)
    sub_w = VIDEO_WIDTH - 2 * margin_x
    sub_y_base = VIDEO_HEIGHT - int(VIDEO_HEIGHT * SUB_BOTTOM_PCT)

    sub_inputs = []
    if chunks:
        w_counts = [len(_word_re.findall(c)) for c in chunks]
        total_w = sum(w_counts) or 1
        avail = max(0.1, dur - start_t)
        per_w = avail / total_w
        curr = start_t
        for i_chk, (txt, wc) in enumerate(zip(chunks, w_counts)):
            d = max(0.6, wc * per_w)
            sub_p = os.path.join(temp_dir, f"sub_{index}_{i_chk}.png")
            h = create_subtitle_image(txt, sub_w, sub_p)
            sub_inputs.append({
                "path": sub_p, "start": curr, "end": curr + d, "dur": d, "y": sub_y_base - h // 2
            })
            curr += d

    inputs = []
    filter_complex = []
    file_index_counter = 0

    inputs.extend(["-i", ap])
    file_index_counter += 1

    v_streams = []

    for i, img_p in enumerate(img_paths):
        case_id, bg_p, fg_p, fg_w, fg_h = analyze_and_prepare_image(img_p, temp_dir, f"{index}_{i}", clip_dur)

        inputs.extend(["-loop", "1", "-t", f"{clip_dur + 5:.3f}", "-i", bg_p])
        idx_bg = file_index_counter
        file_index_counter += 1

        inputs.extend(["-loop", "1", "-t", f"{clip_dur + 5:.3f}", "-i", fg_p])
        idx_fg = file_index_counter
        file_index_counter += 1

        if case_id == 1:
            frames = int((clip_dur + 2) * VIDEO_FPS)
            zp = f"zoompan=z='1.0+0.15*on/{frames}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={VIDEO_FPS},format=yuv420p"
            filter_complex.append(f"[{idx_fg}:v]{zp}[v_part_{i}]")
        elif case_id == 2:
            dist = fg_w - VIDEO_WIDTH
            if random.choice([True, False]):
                expr_x = f"-{dist}*(t/{clip_dur})"
            else:
                expr_x = f"-{dist} + {dist}*(t/{clip_dur})"
            filter_complex.append(f"[{idx_bg}:v][{idx_fg}:v]overlay=x='{expr_x}':y=0:shortest=1,fps={VIDEO_FPS},format=yuv420p[v_part_{i}]")
        elif case_id in (3, 4):
            offset_x = (VIDEO_WIDTH - fg_w) // 2
            offset_y = (VIDEO_HEIGHT - fg_h) // 2
            filter_complex.append(f"[{idx_bg}:v][{idx_fg}:v]overlay=x={offset_x}:y={offset_y}:shortest=1[v_comp_{i}]")
            frames = int((clip_dur + 2) * VIDEO_FPS)
            zp = f"zoompan=z='1.0+0.12*on/{frames}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={VIDEO_FPS},format=yuv420p"
            filter_complex.append(f"[v_comp_{i}]{zp}[v_part_{i}]")
        elif case_id == 5:
            dist = fg_h - VIDEO_HEIGHT
            max_scroll = clip_dur * 150
            real_dist = min(dist, max_scroll)
            expr_y = f"-{real_dist}*(t/{clip_dur})"
            filter_complex.append(f"[{idx_bg}:v][{idx_fg}:v]overlay=x=0:y='{expr_y}':shortest=1,fps={VIDEO_FPS},format=yuv420p[v_part_{i}]")
        elif case_id == 6:
            offset_x = (VIDEO_WIDTH - fg_w) // 2
            offset_y = (VIDEO_HEIGHT - fg_h) // 2
            filter_complex.append(f"[{idx_bg}:v][{idx_fg}:v]overlay=x={offset_x}:y={offset_y}:shortest=1[v_comp_{i}]")
            frames = int((clip_dur + 2) * VIDEO_FPS)
            zp = f"zoompan=z='1.0+0.1*on/{frames}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:fps={VIDEO_FPS},format=yuv420p"
            filter_complex.append(f"[v_comp_{i}]{zp}[v_part_{i}]")

        v_streams.append(f"[v_part_{i}]")

    if len(v_streams) > 1:
        current_v = v_streams[0]
        current_offset = clip_dur - overlap
        for i in range(1, num_imgs):
            next_v = v_streams[i]
            out_v = f"[vm{i}]"
            t_type = random.choice(["fade", "wipeleft", "wiperight", "slideleft", "slideright", "circleclose"])
            filter_complex.append(f"{current_v}{next_v}xfade=transition={t_type}:duration={overlap}:offset={current_offset:.3f}{out_v}")
            current_v = out_v
            current_offset += (clip_dur - overlap)
        final_bg = current_v
    else:
        final_bg = v_streams[0]

    inputs.extend(["-loop", "1", "-i", overlay_path])
    idx_overlay = file_index_counter
    file_index_counter += 1

    particle_path = os.path.join(_ROOT, "logo", PARTICLE_NAME)
    has_particles = os.path.exists(particle_path)
    idx_particle = -1
    if has_particles:
        inputs.extend(["-stream_loop", "-1", "-i", particle_path])
        idx_particle = file_index_counter
        file_index_counter += 1

    idx_subs_start = file_index_counter
    for sub in sub_inputs:
        inputs.extend(["-loop", "1", "-t", f"{sub['dur']:.3f}", "-i", sub["path"]])
        file_index_counter += 1

    layer_before_ui = final_bg
    if has_particles:
        filter_complex.append(f"[{idx_particle}:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},setsar=1,format=gbrp[v_part_rgb]")
        filter_complex.append(f"{final_bg}format=gbrp[v_bg_rgb]")
        filter_complex.append(f"[v_bg_rgb][v_part_rgb]blend=all_mode='screen':shortest=1,format=yuv420p[v_w_particles]")
        layer_before_ui = "[v_w_particles]"

    filter_complex.append(f"{layer_before_ui}[{idx_overlay}:v]overlay=0:0:shortest=1[v_base]")

    last_v = "[v_base]"
    for i, sub in enumerate(sub_inputs):
        s_idx = idx_subs_start + i
        fade_dur = 0.1
        pts_cmd = f"PTS+{sub['start']:.3f}/TB"
        fade_cmd = f"format=rgba,fade=t=in:st=0:d={fade_dur}:alpha=1,fade=t=out:st={sub['dur']-fade_dur:.3f}:d={fade_dur}:alpha=1"
        filter_complex.append(f"[{s_idx}:v]{fade_cmd},setpts={pts_cmd}[subp{i}]")
        next_v = f"[v_sub{i}]"
        enable_expr = f"enable='between(t,{sub['start']:.3f},{sub['end']:.3f})'"
        filter_complex.append(f"{last_v}[subp{i}]overlay={margin_x}:{sub['y']}:{enable_expr}:eof_action=pass{next_v}")
        last_v = next_v

    bar_h = 14
    bg_cmd = f"drawbox=y=ih-{bar_h}:h={bar_h}:w=iw:t=fill:c=black@0.7"
    fg_cmd = f"drawbox=y=ih-{bar_h}:h={bar_h}:w=iw*(t/{dur:.3f}):t=fill:c=white@1.0"
    filter_complex.append(f"{last_v}{bg_cmd},{fg_cmd},trim=duration={dur:.3f}[v_final]")

    output_item_path = os.path.join(temp_dir, f"item_{index}.mp4")
    if os.path.exists(output_item_path):
        os.remove(output_item_path)

    cmd = [
        "ffmpeg", "-y", "-v", "error",
        *inputs,
        "-filter_complex", ";".join(filter_complex),
        "-map", "[v_final]", "-map", "0:a",
        "-c:v", ENCODER, *ENCODER_PARAMS,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-r", str(VIDEO_FPS),
        output_item_path
    ]
    subprocess.run(cmd, check=True)
    return output_item_path


def step3_render_scenes(day_str: str, day_dir: str, work_dir: str, json_path: str, mock: bool = False) -> List[str]:
    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    video_chunks_dir = os.path.join(work_dir, "video_chunks")
    temp_render_dir = os.path.join(work_dir, "temp_render")
    os.makedirs(video_chunks_dir, exist_ok=True)
    os.makedirs(temp_render_dir, exist_ok=True)

    chunk_files: List[str] = []
    total = len(items)

    for idx, item in enumerate(items, 1):
        sc_num = f"{idx:02d}"
        dur = get_audio_duration(item.get("audio_path"))
        log(f"  [{idx}/{total}] Render Clip #{sc_num} ({dur:.1f}s) bằng 1-169.py...", tag="render")

        chunk_path = process_item_ffmpeg_169(item, day_dir, temp_render_dir, sc_num)
        if chunk_path and os.path.exists(chunk_path):
            perm_chunk = os.path.join(video_chunks_dir, f"chunk_{sc_num}.mp4")
            shutil.copy2(chunk_path, perm_chunk)
            chunk_files.append(perm_chunk)

    ok(f"  [BƯỚC 3] Đã hoàn tất render {len(chunk_files)} video clips 16:9!")
    return chunk_files


# ==============================================================================
# BƯỚC 4: GHÉP NỐI CONCAT & HẬU KỲ & THUMBNAIL A/B/C & MOTA.TXT
# ==============================================================================

def create_youtube_thumbnail(img_path: str, title: str, date_str: str, out_path: str) -> None:
    """Render Thumbnail YouTube chuẩn độc lập bằng PIL theo đúng thiết kế gốc:
    1. Cắt ảnh gốc về đúng tỷ lệ 16:9 (1920x1080) sắc nét.
    2. Tạo lớp Gradient Đen (từ trái sang phải, mờ dần) chiếm 60% màn hình bên trái để làm nền nổi chữ.
    3. Vẽ Badge (Hình chữ nhật màu Đỏ #E74C3C) ở góc trên bên trái: 'ĐIỂM ĐỌC • {date_str}'.
    4. Vẽ Tiêu đề (title) bằng font Roboto-Black.ttf siêu to (size 80-100), màu VÀNG (#F1C40F),
       căn lề trái (left-aligned), nằm ở khu vực nửa trên bên trái của ảnh, textwrap hợp lý.
    """
    # 1. Cắt ảnh gốc về 16:9 (1920x1080)
    if img_path and os.path.exists(img_path):
        try:
            raw_im = Image.open(img_path).convert("RGB")
            base_img = ImageOps.fit(raw_im, (VIDEO_WIDTH, VIDEO_HEIGHT), method=Image.Resampling.LANCZOS)
        except Exception:
            base_img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), (25, 28, 36))
    else:
        base_img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), (25, 28, 36))

    # Tăng nhẹ tương phản để ảnh sắc nét, bắt mắt
    base_img = ImageEnhance.Contrast(base_img).enhance(1.08)

    # 2. Tạo lớp Gradient Đen (từ trái sang phải, mờ dần) chiếm 60% màn hình bên trái (~1152px)
    grad_w = int(VIDEO_WIDTH * 0.62)
    grad_mask = Image.new("L", (VIDEO_WIDTH, VIDEO_HEIGHT), 0)
    for x in range(grad_w):
        ratio = x / grad_w
        # Alpha từ 245 giảm dần về 0 theo đường cong phi tuyến
        alpha = int(245 * ((1.0 - ratio) ** 1.3))
        ImageDraw.Draw(grad_mask).line([(x, 0), (x, VIDEO_HEIGHT)], fill=alpha)

    # Thêm nhẹ gradient tối dưới chân để tổng thể vững vàng
    bottom_h = int(VIDEO_HEIGHT * 0.25)
    for y in range(bottom_h):
        ratio = y / bottom_h
        alpha_b = int(140 * ratio)
        y_pos = VIDEO_HEIGHT - bottom_h + y
        curr_row = np.array(grad_mask.crop((0, y_pos, VIDEO_WIDTH, y_pos + 1)))
        new_row = np.maximum(curr_row, alpha_b)
        grad_mask.paste(Image.fromarray(new_row), (0, y_pos))

    black_overlay = Image.new("RGBA", (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))
    black_fill = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), (8, 10, 15))
    black_overlay.paste(black_fill, mask=grad_mask)

    thumb_rgba = base_img.convert("RGBA")
    thumb_rgba.alpha_composite(black_overlay)

    draw = ImageDraw.Draw(thumb_rgba)

    # 3. Vẽ Badge ở góc trên bên trái
    badge_x = 90
    badge_y = 90
    # Nếu là video chuyên đề (không nhắc ngày), dùng badge Chuyên đề Thể thao
    is_special = (not date_str
                  or "chuyên đề" in str(date_str).lower()
                  or os.path.exists(os.path.join(os.path.dirname(out_path), "special_topic"))
                  or os.path.exists(os.path.join(os.path.dirname(out_path), "..", "special_topic")))
    if is_special:
        badge_text = "ĐIỂM ĐỌC  •  CHUYÊN ĐỀ HUYỀN THOẠI"
    else:
        badge_text = f"ĐIỂM ĐỌC  •  {date_str}"
    font_badge = ImageFont.truetype(FONT_BOLD, 36)
    b_box = draw.textbbox((0, 0), badge_text, font=font_badge)
    b_w = b_box[2] - b_box[0]
    b_h = b_box[3] - b_box[1]
    pad_x, pad_y = 28, 14
    badge_rect = [badge_x, badge_y, badge_x + b_w + pad_x * 2, badge_y + b_h + pad_y * 2]
    # Badge màu Xanh Cyan đậm / Electric Blue thay cho màu đỏ cũ
    draw.rounded_rectangle(badge_rect, radius=8, fill=(0, 168, 204))
    # Chữ Trắng trong Badge
    draw.text((badge_x + pad_x, badge_y + pad_y - 2), badge_text, font=font_badge, fill=(255, 255, 255))

    # 4. Vẽ Tiêu đề bằng font Roboto-Black to (size 80-100), màu Electric Cyan (#00E5FF) mát mắt
    title_clean = (title or "").strip()
    title_start_y = badge_rect[3] + 45
    max_title_w = int(VIDEO_WIDTH * 0.56)

    # Tự động co giãn kích thước font từ 96 xuống 80 nếu tiêu đề dài
    chosen_font = None
    lines = []
    for f_sz in [96, 88, 82, 76]:
        cand_font = ImageFont.truetype(FONT_BOLD, f_sz)
        char_per_line = int(max_title_w / (f_sz * 0.52))
        lines_cand = textwrap.wrap(title_clean, width=char_per_line)
        too_wide = any((cand_font.getbbox(ln)[2] - cand_font.getbbox(ln)[0]) > max_title_w for ln in lines_cand)
        if not too_wide and len(lines_cand) <= 4:
            chosen_font = cand_font
            lines = lines_cand
            break

    if not lines or chosen_font is None:
        chosen_font = ImageFont.truetype(FONT_BOLD, 76)
        lines = textwrap.wrap(title_clean, width=int(max_title_w / (76 * 0.52)))

    # Vẽ từng dòng tiêu đề màu Electric Cyan (#00E5FF) với hiệu ứng Drop Shadow đen đậm
    curr_y = title_start_y
    line_gap = 14
    for ln in lines[:4]:
        # Bóng đổ đen đậm
        draw.text((badge_x + 5, curr_y + 5), ln, font=chosen_font, fill=(0, 0, 0, 240))
        # Stroke đen mỏng và chữ màu Electric Cyan #00E5FF
        draw.text((badge_x, curr_y), ln, font=chosen_font, fill=(0, 229, 255), stroke_width=2, stroke_fill=(15, 15, 15))
        bbox = draw.textbbox((0, 0), ln, font=chosen_font)
        curr_y += (bbox[3] - bbox[1]) + line_gap

    # 5. Lưu ảnh Thumbnail
    thumb_rgba.convert("RGB").save(out_path, quality=95, optimize=True)
    log(f"  [THUMBNAIL] Đã xuất {paths.rel_to_root(out_path)}", tag="publish")


def generate_3_thumbnails_169(day_str: str, day_dir: str, items: List[Dict[str, Any]]) -> None:
    """Sinh đủ 3 Thumbnail A/B/C ngang 16:9 chuẩn Cinematic Cyber-Stadium (Ronaldo & Messi style) bằng Playwright."""
    tpl_path = os.path.join(paths.TEMPLATES, "thumbnail_16x9_sports.html")
    logo_path = os.path.join(paths.ASSETS, "logo", "diem-doc-logo-1.png")

    custom_plan_path = os.path.join(day_dir, "thumbnails_plan.json")
    if not os.path.exists(custom_plan_path):
        parent_cand = os.path.join(os.path.dirname(day_dir), "thumbnails_plan.json")
        if os.path.exists(parent_cand):
            custom_plan_path = parent_cand
    custom_plan = []
    if os.path.exists(custom_plan_path):
        try:
            with open(custom_plan_path, "r", encoding="utf-8") as pf:
                custom_plan = json.load(pf)
        except Exception:
            custom_plan = []

    is_spec = (os.path.exists(os.path.join(day_dir, "special_topic"))
               or os.path.exists(os.path.join(day_dir, "..", "special_topic")))
    date_display = "" if is_spec else fmt_date_from_day(day_dir)
    versions = ["A", "B", "C"]

    try:
        from playwright.sync_api import sync_playwright
        with open(tpl_path, "r", encoding="utf-8") as f:
            tpl_code = f.read()
        tpl_code = tpl_code.replace("__ASSETS__", paths.file_url(paths.ASSETS))
        tpl_code = tpl_code.replace("__LOGO_URL__", paths.file_url(logo_path))

        work_dir = paths.work_project_dir(day_str)
        temp_html_dir = os.path.join(work_dir, "thumbnails_render")
        os.makedirs(temp_html_dir, exist_ok=True)

        with sync_playwright() as p:
            br = p.chromium.launch(headless=True, args=[
                "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"
            ])
            page = br.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)

            for idx, ver in enumerate(versions):
                c_item = (custom_plan[idx] if idx < len(custom_plan) else None)
                item = items[idx % len(items)] if items else {}

                # Image selection
                if c_item and c_item.get("image_file") and os.path.exists(c_item["image_file"]):
                    img_src = os.path.abspath(c_item["image_file"])
                else:
                    img_src = item.get("image_path")
                    if not img_src or not os.path.exists(img_src):
                        for s_i in range(1, 15):
                            cand = item.get(f"image_{s_i}")
                            if cand and os.path.exists(cand):
                                img_src = cand
                                break
                    if not img_src or not os.path.exists(img_src):
                        cands = sorted(glob.glob(os.path.join(day_dir, "images", f"*Tin_{idx+1:02d}*.jpg")))
                        img_src = cands[0] if cands else os.path.join(paths.LOGO, "logo.png")
                    img_src = os.path.abspath(img_src)

                # Badge
                badge = (c_item.get("badge") if c_item else None) or item.get("group", "BẢN TIN THỂ THAO").upper()

                # Headline 3 màu tương phản
                raw_title = (c_item.get("headline") if c_item else None)
                if not raw_title:
                    t_str = item.get("title", "BẢN TIN THỂ THAO").strip()
                    words = t_str.split()
                    w1 = " ".join(words[:max(1, len(words)//3)])
                    w2 = " ".join(words[len(words)//3 : 2*len(words)//3])
                    w3 = " ".join(words[2*len(words)//3 :])
                    c1, c2, c3 = ("hl-cyan", "hl-white", "hl-yellow") if idx == 0 else (("hl-yellow", "hl-white", "hl-cyan") if idx == 1 else ("hl-red", "hl-white", "hl-yellow"))
                    raw_title = f'<span class="{c1}">{w1}</span><br><span class="{c2}">{w2}</span><br><span class="{c3}">{w3}</span>'

                kicker = (c_item.get("kicker") if c_item else None) or f"{item.get('title', 'TIN NÓNG')[:35]}..."
                subtitle = (c_item.get("subtitle") if c_item else None) or (item.get("summary", "")[:90] + "...")
                footer_tag = (c_item.get("footer_tag") if c_item else None) or "TỔNG HỢP TUẦN QUA"
                obj_pos = (c_item.get("obj_pos") if c_item else "center 18%")
                filt = (c_item.get("filter") if c_item else "contrast(1.10) brightness(1.05) saturate(1.18)")

                photo_url = paths.file_url(img_src)
                logo_url = paths.file_url(logo_path)
                hero_size = (c_item.get("hero_size") if c_item else None) or "86px"
                tag_a = (c_item.get("tag_a") if c_item else None) or footer_tag
                tag_b = (c_item.get("tag_b") if c_item else None) or (date_display if date_display else "CHUẨN 1080P")

                html_content = (
                    tpl_code.replace("__LOGO__", logo_url)
                    .replace("__LOGO_URL__", logo_url)
                    .replace("__PHOTO__", photo_url)
                    .replace("__THUMB_IMAGE__", photo_url)
                    .replace("__BADGE__", badge)
                    .replace("__THUMB_BADGE__", badge)
                    .replace("__KICKER__", kicker)
                    .replace("__THUMB_KICKER__", kicker)
                    .replace("__HERO_SIZE__", str(hero_size))
                    .replace("__HERO_HTML__", raw_title)
                    .replace("__THUMB_HEADLINE__", raw_title)
                    .replace("__SUBTITLE__", subtitle)
                    .replace("__THUMB_SUBTITLE__", subtitle)
                    .replace("__TAG_A__", tag_a)
                    .replace("__THUMB_FOOTER_TAG__", footer_tag)
                    .replace("__TAG_B__", tag_b)
                    .replace("__OBJ_POS__", obj_pos)
                    .replace("__THUMB_OBJ_POS__", obj_pos)
                    .replace("__THUMB_FILTER__", filt)
                )

                hfile = os.path.join(temp_html_dir, f"thumb_{ver}.html")
                with open(hfile, "w", encoding="utf-8") as hf:
                    hf.write(html_content)

                out_thumb = os.path.join(day_dir, f"thumbnail_{ver}.jpg")
                page.goto(paths.file_url(hfile), wait_until="networkidle")
                page.wait_for_timeout(600)
                page.screenshot(path=out_thumb, type="jpeg", quality=95)

            br.close()
    except Exception as e:
        warn(f"Playwright thumbnail render gặp lỗi ({e}), fallback sang PIL cũ...")
        for idx, ver in enumerate(versions):
            item = items[idx % len(items)] if items else {}
            title = item.get("title", "BẢN TIN THỂ THAO ĐIỂM ĐỌC")
            img_src = item.get("image_path") or os.path.join(paths.LOGO, "logo.png")
            out_thumb = os.path.join(day_dir, f"thumbnail_{ver}.jpg")
            create_youtube_thumbnail(img_src, title, date_display, out_thumb)

    # Bản đại diện chính thumbnail.jpg
    thumb_main = os.path.join(day_dir, "thumbnail.jpg")
    thumb_a = os.path.join(day_dir, "thumbnail_A.jpg")
    if os.path.exists(thumb_a):
        shutil.copy2(thumb_a, thumb_main)


def step4_compose_video(day_str: str, day_dir: str, work_dir: str, chunk_files: List[str], json_path: str) -> str:
    all_segments: List[str] = []
    chapter_list: List[Tuple[str, str]] = []
    current_seconds = 0.0

    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    # 1. Intro
    intro_path = os.path.join(_ROOT, "logo", INTRO_NAME)
    if os.path.exists(intro_path):
        intro_norm = os.path.join(work_dir, "intro_norm.mp4")
        norm_cmd = [
            "ffmpeg", "-y", "-v", "error", "-i", intro_path,
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={VIDEO_FPS},format=yuv420p",
            "-c:v", ENCODER, *ENCODER_PARAMS,
            "-c:a", "aac", "-ar", "44100", "-ac", "2", intro_norm
        ]
        subprocess.run(norm_cmd, check=True)
        all_segments.append(intro_norm)
        intro_dur = get_audio_duration(intro_norm)
        chapter_list.append(("00:00", "Nhập cuộc bản tin"))
        current_seconds += intro_dur

    # 2. Main Chunks
    for idx, (chunk, item) in enumerate(zip(chunk_files, items), 1):
        all_segments.append(chunk)
        c_dur = get_audio_duration(chunk)
        m = int(current_seconds // 60)
        s = int(current_seconds % 60)
        chapter_list.append((f"{m:02d}:{s:02d}", item.get('title', '').strip()))
        current_seconds += c_dur

    # 3. Outro
    outro_path = os.path.join(_ROOT, "logo", OUTRO_NAMES[0])
    if os.path.exists(outro_path):
        outro_norm = os.path.join(work_dir, "outro_norm.mp4")
        norm_cmd = [
            "ffmpeg", "-y", "-v", "error", "-i", outro_path,
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={VIDEO_FPS},format=yuv420p",
            "-c:v", ENCODER, *ENCODER_PARAMS,
            "-c:a", "aac", "-ar", "44100", "-ac", "2", outro_norm
        ]
        subprocess.run(norm_cmd, check=True)
        all_segments.append(outro_norm)

    # 4. Concat demuxer
    list_txt = os.path.join(work_dir, "concat_list.txt")
    with open(list_txt, "w", encoding="utf-8") as f:
        for seg in all_segments:
            safe_p = seg.replace("\\", "/").replace("'", "'\\''")
            f.write(f"file '{safe_p}'\n")

    tmp_concat = os.path.join(work_dir, "tmp_concat.mp4")
    concat_cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", list_txt, "-c", "copy", tmp_concat]
    res = subprocess.run(concat_cmd)
    if res.returncode != 0:
        fallback_cmd = [
            "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", list_txt,
            "-c:v", ENCODER, *ENCODER_PARAMS,
            "-c:a", "aac", "-b:a", "192k", tmp_concat
        ]
        subprocess.run(fallback_cmd, check=True)

    # 5. Mix BGM (mức 0.05)
    bgm_candidates = [
        os.path.join(paths.ASSETS, "bgm", "bgm_editorial_2_momentum.mp3"),
        os.path.join(paths.ASSETS, "bgm", "bgm_upbeat_blaze.mp3"),
        os.path.join(paths.ASSETS, "bgm", "bgm_default.mp3")
    ]
    bgm_file = next((b for b in bgm_candidates if os.path.exists(b)), None)

    parts = day_str.split(".")
    d, m = parts[0], parts[1]
    final_name = f"Tin-The-Thao-{d}-{m}.mp4"
    final_path = os.path.join(day_dir, final_name)

    if bgm_file:
        log(f"  [BƯỚC 4] Mix BGM (volume=0.05): {paths.rel_to_root(bgm_file)}", tag="compose")
        mix_cmd = [
            "ffmpeg", "-y", "-v", "error",
            "-i", tmp_concat,
            "-stream_loop", "-1", "-i", bgm_file,
            "-filter_complex", "[1:a]volume=0.05[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[a_out]",
            "-map", "0:v", "-map", "[a_out]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            final_path
        ]
        subprocess.run(mix_cmd, check=True)
    else:
        shutil.copy2(tmp_concat, final_path)

    # Dọn dẹp file MP4 nháp ngay lập tức để tiết kiệm ổ đĩa
    if os.path.exists(tmp_concat):
        try: os.remove(tmp_concat)
        except Exception: pass

    thethao_alias = os.path.join(day_dir, "thethao.mp4")
    if os.path.exists(thethao_alias):
        try: os.remove(thethao_alias)
        except Exception: pass

    # 6. Thumbnail A/B/C & mota.txt
    generate_3_thumbnails_169(day_str, day_dir, items)

    date_display = f"{d}/{m}/{parts[2] if len(parts) >= 3 else '2026'}"
    top_t1 = items[0]["title"] if len(items) > 0 else "Bản tin thể thao"
    top_t2 = items[1]["title"] if len(items) > 1 else "Diễn biến nóng"
    top_t3 = items[2]["title"] if len(items) > 2 else "Tin tức quốc tế"

    from pathlib import Path
    from diemdoc.publisher import write_mota_16x9
    mota_path = os.path.join(day_dir, "mota.txt")
    titles_abc = [
        f"Điểm Đọc thể thao {date_display}: {top_t1}",
        f"{top_t2} và toàn cảnh tin nóng thể thao ngày {date_display}",
        f"Tổng hợp 25 bản tin thể thao đáng chú ý nhất tuần qua ({date_display}) | Điểm Đọc",
    ]
    write_mota_16x9(
        out_path=Path(mota_path),
        titles_abc=titles_abc,
        chapters=chapter_list,
        video_type="weekly_digest",
        day_str=date_display,
    )
    log(f"  [MÔ TẢ] Đã xuất {paths.rel_to_root(mota_path)}", tag="publish")

    ok(f"  [BƯỚC 4] Đã nối thành 1 file MP4 duy nhất: {paths.rel_to_root(final_path)}")
    return final_path


# ==============================================================================
# BƯỚC 5: RENDER VIDEO DỌC SHORTS 9:16 (CHÍNH THỨC 1-916.py, is_fast_mode=False)
# ==============================================================================

def step5_render_shorts(day_str: str, day_dir: str, work_dir: str) -> None:
    shorts_json_path = os.path.join(day_dir, "shorts.json")
    if not os.path.exists(shorts_json_path):
        return

    with open(shorts_json_path, "r", encoding="utf-8") as f:
        shorts_data = json.load(f)

    shorts_out_dir = os.path.join(day_dir, "shorts")
    shorts_work_dir = os.path.join(work_dir, "shorts_render")
    os.makedirs(shorts_out_dir, exist_ok=True)
    os.makedirs(shorts_work_dir, exist_ok=True)

    cache_dir = paths.work_file("vitts_cache")
    model: Optional[Vieneu] = None
    silence_05 = AudioSegment.silent(duration=500, frame_rate=44100).set_channels(2)

    total = len(shorts_data)
    log(f"  [BƯỚC 5] Bắt đầu sản xuất {total} video Shorts 9:16 (is_fast_mode=False)...", tag="shorts")

    for s_idx, short in enumerate(shorts_data, 1):
        short_id = short.get("short_id", s_idx)
        art_id = short.get("id", f"art_{s_idx:02d}")
        title = short.get("title", "")
        script = short.get("script", "")
        group = short.get("group", "THỂ THAO").upper()

        out_short_mp4 = os.path.join(shorts_out_dir, f"short_{short_id:02d}.mp4")
        out_short_thumb = os.path.join(shorts_out_dir, f"short_{short_id:02d}.jpg")

        # 1. Âm thanh Short
        short_audio_wav = os.path.join(shorts_work_dir, f"audio_short_{short_id:02d}.wav")
        title_audio_wav = os.path.join(shorts_work_dir, f"title_short_{short_id:02d}.wav")
        if not os.path.exists(short_audio_wav) or os.path.getsize(short_audio_wav) < 1000:
            if model is None:
                model = Vieneu(mode="v3turbo")
            seg_t = synthesize_text(model, title, voice="Minh Quân Pro", speed=1.12, pitch=0.93, cache_dir=cache_dir)
            seg_t.set_frame_rate(44100).set_channels(2).export(title_audio_wav, format="wav")

            seg_s = synthesize_text(model, script, voice="Minh Quân Pro", speed=1.12, pitch=0.93, cache_dir=cache_dir)
            comb = (seg_t + silence_05 + seg_s).set_frame_rate(44100).set_channels(2).normalize(headroom=0.1)
            comb.export(short_audio_wav, format="wav")

        dur = get_audio_duration(short_audio_wav)
        if dur <= 1.0:
            continue

        log(f"    [{s_idx}/{total}] Render Short #{short_id} ({dur:.1f}s) bằng 1-916.py...", tag="shorts")

        # 2. Ảnh
        img_cand = os.path.join(day_dir, "images", f"{art_id}_cover.jpg")
        if not os.path.exists(img_cand) or os.path.getsize(img_cand) == 0:
            img_cand = os.path.join(day_dir, "images", f"thethao-{short_id}-1.jpg")
        if not os.path.exists(img_cand) or os.path.getsize(img_cand) == 0:
            img_cand = os.path.join(_ROOT, "logo", "logo.png")

        # 3. Header Overlay 9:16
        overlay_short_path = os.path.join(shorts_work_dir, f"overlay_s_{short_id}.png")
        create_static_overlay_916(day_dir, title, group, "TOP NỔI BẬT", overlay_short_path)

        # 4. Subtitles 9:16 (is_fast_mode = False)
        real_title_dur = get_audio_duration(title_audio_wav) or 2.0
        start_t = min(max(0.0, dur - 0.5), real_title_dur + TITLE_GAP_SEC)
        chunks = split_chunks(script)
        margin_x = 40
        sub_w = VIDEO_WIDTH_916 - 2 * margin_x
        sub_inputs = []
        if chunks:
            w_counts = [len(_word_re.findall(c)) for c in chunks]
            total_w = sum(w_counts) or 1
            avail = max(0.1, dur - start_t)
            per_w = avail / total_w
            curr = start_t
            for i_chk, (txt, wc) in enumerate(zip(chunks, w_counts)):
                d = max(0.6, wc * per_w)
                sub_p = os.path.join(shorts_work_dir, f"sub_s_{short_id}_{i_chk}.png")
                h = create_subtitle_image_916(txt, sub_w, sub_p)
                sub_y = VIDEO_HEIGHT_916 - BOT_REGION_H - 60 - h
                sub_inputs.append({"path": sub_p, "start": curr, "end": curr + d, "dur": d, "y": sub_y})
                curr += d

        # 5. Filter complex theo đúng 1-916.py
        inputs = []
        filter_complex = []
        file_index_counter = 0

        inputs.extend(["-i", short_audio_wav])
        file_index_counter += 1

        case_id, bg_p, fg_p, fg_w, fg_h = analyze_and_prepare_image_916(img_cand, shorts_work_dir, short_id, is_fast_mode=False)
        inputs.extend(["-loop", "1", "-t", f"{dur + 5:.3f}", "-i", bg_p])
        idx_bg = file_index_counter
        file_index_counter += 1

        inputs.extend(["-loop", "1", "-t", f"{dur + 5:.3f}", "-i", fg_p])
        idx_fg = file_index_counter
        file_index_counter += 1

        if case_id == 1:
            dist = fg_w - IMG_AREA_W
            expr_x = f"-{dist}*(t/{dur})"
            filter_complex.append(f"[{idx_bg}:v][{idx_fg}:v]overlay=x='{expr_x}':y=0:shortest=1,fps={VIDEO_FPS},format=yuv420p[v_part_0]")
        elif case_id == 2:
            dist = fg_h - IMG_AREA_H
            expr_y = f"-{dist}*(t/{dur})"
            filter_complex.append(f"[{idx_bg}:v][{idx_fg}:v]overlay=x=0:y='{expr_y}':shortest=1,fps={VIDEO_FPS},format=yuv420p[v_part_0]")
        else:
            frames = int((dur + 2) * VIDEO_FPS)
            zp = f"zoompan=z='1.0+0.15*on/{frames}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={frames}:s={IMG_AREA_W}x{IMG_AREA_H}:fps={VIDEO_FPS},format=yuv420p"
            filter_complex.append(f"[{idx_fg}:v]{zp}[v_part_0]")

        final_img_stream = "[v_part_0]"

        filter_complex.append(f"color=c=black:s={VIDEO_WIDTH_916}x{VIDEO_HEIGHT_916}:d={dur:.3f}[v_canvas]")
        filter_complex.append(f"{final_img_stream}split=3[img_main][blur_top_src][blur_bot_src]")
        filter_complex.append(f"[blur_top_src]crop={IMG_AREA_W}:{TOP_CONTENT_H}:0:0,boxblur=40:10,eq=brightness=-0.1[top_blur]")
        filter_complex.append(f"[blur_bot_src]crop={IMG_AREA_W}:{BOT_CONTENT_H}:0:{IMG_AREA_H - BOT_CONTENT_H},boxblur=40:10,eq=brightness=-0.1[bot_blur]")

        filter_complex.append(f"[v_canvas][img_main]overlay=0:{IMG_AREA_Y}:shortest=1[bg1]")
        filter_complex.append(f"[bg1][top_blur]overlay=0:{TOP_SAFE_H}:shortest=1[bg2]")
        filter_complex.append(f"[bg2][bot_blur]overlay=0:{VIDEO_HEIGHT_916 - BOT_REGION_H}:shortest=1[final_bg]")

        inputs.extend(["-loop", "1", "-i", overlay_short_path])
        idx_overlay = file_index_counter
        file_index_counter += 1

        idx_subs_start = file_index_counter
        for sub in sub_inputs:
            inputs.extend(["-loop", "1", "-t", f"{sub['dur']:.3f}", "-i", sub["path"]])
            file_index_counter += 1

        filter_complex.append(f"[final_bg][{idx_overlay}:v]overlay=0:0:shortest=1[v_base]")

        last_v = "[v_base]"
        for i, sub in enumerate(sub_inputs):
            s_idx = idx_subs_start + i
            fade_dur = 0.1
            pts_cmd = f"PTS+{sub['start']:.3f}/TB"
            fade_cmd = f"format=rgba,fade=t=in:st=0:d={fade_dur}:alpha=1,fade=t=out:st={sub['dur']-fade_dur:.3f}:d={fade_dur}:alpha=1"
            filter_complex.append(f"[{s_idx}:v]{fade_cmd},setpts={pts_cmd}[subp{i}]")
            next_v = f"[v_sub{i}]"
            enable_expr = f"enable='between(t,{sub['start']:.3f},{sub['end']:.3f})'"
            filter_complex.append(f"{last_v}[subp{i}]overlay={margin_x}:{sub['y']}:{enable_expr}:eof_action=pass{next_v}")
            last_v = next_v

        bar_h = 14
        bg_cmd = f"drawbox=y=ih-{bar_h}:h={bar_h}:w=iw:t=fill:c=black@0.7"
        fg_cmd = f"drawbox=y=ih-{bar_h}:h={bar_h}:w=iw*(t/{dur:.3f}):t=fill:c=white@1.0"
        filter_complex.append(f"{last_v}{bg_cmd},{fg_cmd},trim=duration={dur:.3f},format=yuv420p[v_final]")

        cmd = [
            "ffmpeg", "-y", "-v", "error",
            *inputs,
            "-filter_complex", ";".join(filter_complex),
            "-map", "[v_final]", "-map", "0:a",
            "-c:v", ENCODER, *ENCODER_PARAMS,
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
            "-t", f"{dur:.3f}",
            out_short_mp4
        ]
        subprocess.run(cmd, check=True)

        # 6. Thumbnail 9:16
        shutil.copy2(overlay_short_path, out_short_thumb)

    ok(f"  [BƯỚC 5] Đã hoàn tất render toàn bộ Video Shorts vào {paths.rel_to_root(shorts_out_dir)}/!")


def step3_render_scenes_html(day_str: str, day_dir: str, work_dir: str, json_path: str,
                             item_filter: Optional[str] = None,
                             shorts_mode: str = "default",
                             workers: int = 1,
                             force: bool = False) -> List[str]:
    """Render các bản tin bằng engine HTML/Playwright + GSAP v2 (hỗ trợ đa tiến trình Playwright và resume theo tin)."""
    import concurrent.futures
    import threading
    import sys
    sys.path.insert(0, os.path.join(_ROOT, "engines", "html"))
    from m8_news_bridge import export_bridge_project, export_focus_short_project, export_digest_short_project
    from renderer import render_html_engine

    # Giám sát mức RAM đỉnh của toàn bộ cây tiến trình (Python + Playwright Chromium + FFmpeg)
    peak_rss_mb = [0.0]
    stop_mem_monitor = threading.Event()
    def _mem_monitor():
        try:
            import psutil
            proc = psutil.Process()
            while not stop_mem_monitor.is_set():
                try:
                    total_rss = proc.memory_info().rss
                    for child in proc.children(recursive=True):
                        try:
                            total_rss += child.memory_info().rss
                        except Exception:
                            pass
                    mb = total_rss / (1024 * 1024)
                    if mb > peak_rss_mb[0]:
                        peak_rss_mb[0] = mb
                except Exception:
                    pass
                time.sleep(0.5)
        except Exception:
            pass

    t_mem = threading.Thread(target=_mem_monitor, daemon=True)
    t_mem.start()

    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    if item_filter:
        items = [it for it in items if str(it.get("id")) == str(item_filter)]
        if not items:
            die(f"Không tìm thấy tin ID={item_filter} trong {json_path}")

    # Đọc cấu hình shorts.json để lập kế hoạch Short
    shorts_cfg_path = os.path.join(paths.CONFIG, "shorts.json")
    shorts_cfg = {}
    if os.path.exists(shorts_cfg_path):
        try:
            with open(shorts_cfg_path, "r", encoding="utf-8") as f:
                shorts_cfg = json.load(f)
        except Exception as e:
            warn(f"Không đọc được {shorts_cfg_path}: {e}")

    focus_cfg = shorts_cfg.get("focus", {"enabled": True, "items_per_short": [1, 4], "max_seconds": 170})
    digest_cfg = shorts_cfg.get("digest", {"enabled": True, "mode": "all_items", "seconds_per_item": [5, 7], "max_seconds": 120})

    # Đọc shorts.json của thư mục lượt chạy nếu có
    local_shorts_json = os.path.join(day_dir, "shorts.json")
    focus_groups = []
    if os.path.exists(local_shorts_json):
        try:
            with open(local_shorts_json, "r", encoding="utf-8") as f:
                s_data = json.load(f)
            # Map art_id sang id trong thethao.json
            art_map = {it.get("art_id"): str(it.get("id")) for it in items if it.get("art_id")}
            mapped_ids = []
            for s_it in s_data:
                s_art = s_it.get("id")
                if s_art in art_map:
                    mapped_ids.append(art_map[s_art])
                elif str(s_it.get("id")) in [str(x.get("id")) for x in items]:
                    mapped_ids.append(str(s_it.get("id")))

            if mapped_ids:
                # Nhóm theo 3 tin mỗi Focus Short
                chunk_sz = 3
                for i in range(0, len(mapped_ids), chunk_sz):
                    grp = mapped_ids[i:i + chunk_sz]
                    if grp:
                        focus_groups.append(grp)
        except Exception as e:
            warn(f"Không thể phân tích shorts.json địa phương: {e}")

    if not focus_groups:
        focus_groups = [[str(it.get("id")) for it in items[:3]]]

    # LẬP KẾ HOẠCH SHORT VÀ IN RA TERMINAL
    log("\n" + "=" * 80)
    log(f"📱 KẾ HOẠCH SẢN XUẤT SHORT (SHORTS PLAN) — NGÀY {day_str}")
    log("=" * 80)
    log(f"{'LOẠI SHORT':<18} | {'DANH SÁCH TIN':<24} | {'ƯỚC TÍNH (S)':<15} | {'GIỚI HẠN (S)':<14} | {'TRẠNG THÁI'}")
    log("-" * 80)

    # Đo thời lượng thực tế của từng audio tin
    item_durs = {}
    for it in items:
        a_p = it.get("audio_path", "")
        if a_p and os.path.exists(a_p):
            item_durs[str(it.get("id"))] = get_audio_duration(a_p)
        else:
            item_durs[str(it.get("id"))] = 30.0

    # Ước tính các Focus Shorts
    focus_max = focus_cfg.get("max_seconds", 170)
    for g_idx, f_ids in enumerate(focus_groups, 1):
        f_est = sum(item_durs.get(iid, 30.0) for iid in f_ids) + 0.4 * max(0, len(f_ids) - 1)
        f_status = "ĐẠT CHUẨN" if f_est <= focus_max else f"VƯỢT TRẦN (+{f_est - focus_max:.1f}s)"
        label = f"Focus Short #{g_idx:02d}"
        log(f"{label:<18} | {','.join(f_ids):<24} | {f_est:<15.1f} | {focus_max:<14} | {f_status}")
        if f_est > focus_max:
            warn(f"  ⚠️ CẢNH BÁO: {label} ước tính {f_est:.1f}s vượt trần {focus_max}s! Đề xuất giảm bớt tin.")

    # Ước tính Digest Short
    digest_item_ids = [str(it.get("id")) for it in items]
    digest_sec_cfg = digest_cfg.get("seconds_per_item", [5, 7])
    digest_total_est = 0.0
    for iid in digest_item_ids:
        cached_wav = os.path.join(work_dir, "digest_work", f"digest_line_{int(iid):02d}.wav")
        if os.path.exists(cached_wav):
            digest_total_est += get_audio_duration(cached_wav)
        else:
            it_match = next((x for x in items if str(x.get("id")) == str(iid)), None)
            d_text = (it_match.get("digest_line") or it_match.get("summary", "")[:120]).strip() if it_match else ""
            n_words = len(d_text.split()) if d_text else 20
            digest_total_est += max(float(digest_sec_cfg[0]), min(float(digest_sec_cfg[1]), n_words / 4.2))
    digest_est_sec = digest_total_est + 0.3 * max(0, len(digest_item_ids) - 1)
    digest_max = digest_cfg.get("max_seconds", 120)
    digest_status = "ĐẠT CHUẨN" if digest_est_sec <= digest_max else f"VƯỢT TRẦN (+{digest_est_sec - digest_max:.1f}s)"
    log(f"{'Digest Short':<18} | {'Toàn bộ ' + str(len(items)) + ' tin':<24} | {digest_est_sec:<15.1f} | {digest_max:<14} | {digest_status}")
    if digest_est_sec > digest_max:
        warn(f"  ⚠️ CẢNH BÁO: Digest Short ước tính {digest_est_sec:.1f}s vượt trần {digest_max}s! Đề xuất giảm bớt tin.")
    log("=" * 80 + "\n")

    html_out_dir = paths.ensure_dir(os.path.join(work_dir, "html_v2_renders"))
    preview_v2_dir = paths.ensure_dir(os.path.join(day_dir, "_preview_v2"))

    # Quản lý cơ chế Resume cấp tin qua .run_state
    run_state_file = os.path.join(work_dir, ".run_state")
    run_state = {}
    if os.path.exists(run_state_file) and not force:
        try:
            with open(run_state_file, "r", encoding="utf-8") as f:
                run_state = json.load(f)
        except Exception:
            run_state = {}

    completed_169 = set(run_state.get("completed_169", []))
    completed_916 = set(run_state.get("completed_916", []))
    state_lock = threading.Lock()

    def save_state():
        try:
            with open(run_state_file, "w", encoding="utf-8") as f:
                json.dump(run_state, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # Tính toán trước offset thời gian toàn cục tích lũy tất định cho toàn bộ danh sách items
    global_offsets = []
    cum_off = 0.0
    for it in items:
        global_offsets.append(cum_off)
        ap = it.get("audio_path", "")
        cum_off += get_audio_duration(ap) if (ap and os.path.exists(ap)) else 30.0

    # Hàm render từng tin độc lập
    def render_single_item(idx: int, item: dict) -> Tuple[int, Optional[str], Optional[str]]:
        raw_id = item.get("id", str(idx))
        dest_169 = os.path.join(preview_v2_dir, f"tin_{int(raw_id):02d}_long.mp4")
        dest_916 = os.path.join(preview_v2_dir, f"tin_{int(raw_id):02d}_short.mp4")

        is_169_done = (int(raw_id) in completed_169) and os.path.exists(dest_169) and (os.path.getsize(dest_169) > 1000)
        is_916_done = (int(raw_id) in completed_916) and os.path.exists(dest_916) and (os.path.getsize(dest_916) > 1000)

        res_169 = dest_169 if is_169_done else None
        res_916 = dest_916 if is_916_done else None

        # 1. Render 16:9 (luôn render để ghép video dài 16:9)
        if not is_169_done or force:
            g_offset = global_offsets[idx - 1]
            log(f"[{idx}/{len(items)}] Render Tin #{raw_id} 16:9 bằng HTML v2 (offset={g_offset:.2f}s)...", tag="html_v2")
            pdir_long, _, _ = export_bridge_project(day_dir, item_id=raw_id, format_type="long",
                                                   work_proj_dir=os.path.join(html_out_dir, f"tin_{raw_id}_long"),
                                                   global_offset_sec=g_offset)
            v169 = render_html_engine(pdir_long, template="long_sports_news_v2.html", scene_number=None,
                                      fps=VIDEO_FPS, preview=False, force=True)
            if v169 and os.path.exists(v169):
                shutil.copy2(v169, dest_169)
                res_169 = dest_169
                with state_lock:
                    completed_169.add(int(raw_id))
                    run_state["completed_169"] = sorted(list(completed_169))
                    save_state()
                log(f"  👉 Đã lưu bản copy preview 16:9: {paths.rel_to_root(dest_169)}", tag="preview_v2")
        else:
            log(f"Tin #{raw_id} 16:9 đã hoàn tất trước đó (resume từ .run_state), bỏ qua.", tag="resume")

        # 2. Render 9:16 (chỉ khi shorts_mode == 'default')
        if shorts_mode == "default":
            if not is_916_done or force:
                log(f"[{idx}/{len(items)}] Render Tin #{raw_id} 9:16 bằng HTML v2...", tag="html_v2")
                pdir_short, _, _ = export_bridge_project(day_dir, item_id=raw_id, format_type="short",
                                                        work_proj_dir=os.path.join(html_out_dir, f"tin_{raw_id}_short"),
                                                        global_offset_sec=0.0)
                v916 = render_html_engine(pdir_short, template="short_news_v2.html", scene_number=None,
                                          fps=VIDEO_FPS, preview=False, force=True)
                if v916 and os.path.exists(v916):
                    shutil.copy2(v916, dest_916)
                    try:
                        from diemdoc.short_outro import append_short_outro
                        append_short_outro(dest_916, voice_hint=item.get("voice_preset", "primary"))
                    except Exception as e:
                        warn(f"Không thể gắn Short Outro cho Tin #{raw_id}: {e}")
                    res_916 = dest_916
                    with state_lock:
                        completed_916.add(int(raw_id))
                        run_state["completed_916"] = sorted(list(completed_916))
                        save_state()
                    log(f"  👉 Đã lưu bản copy preview 9:16: {paths.rel_to_root(dest_916)}", tag="preview_v2")
            else:
                log(f"Tin #{raw_id} 9:16 đã hoàn tất trước đó (resume từ .run_state), bỏ qua.", tag="resume")

        return idx, res_169, res_916

    # Thực thi render: đơn luồng hoặc đa luồng
    out_vids = []
    chunk_169_files = []

    if workers > 1:
        log(f"🚀 Kích hoạt chế độ đa tiến trình với {workers} workers Playwright song song!", tag="workers")
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_idx = {executor.submit(render_single_item, idx, item): idx for idx, item in enumerate(items, start=1)}
            raw_results = []
            for future in concurrent.futures.as_completed(future_to_idx):
                raw_results.append(future.result())
        raw_results.sort(key=lambda x: x[0])
    else:
        raw_results = [render_single_item(idx, item) for idx, item in enumerate(items, start=1)]

    for idx, r169, r916 in raw_results:
        if r169:
            chunk_169_files.append(r169)
            out_vids.append(r169)
        if r916:
            out_vids.append(r916)

    # 3. RENDER FOCUS SHORT NẾU ĐƯỢC YÊU CẦU
    if shorts_mode in ["focus", "all"] and not item_filter:
        for g_idx, f_ids in enumerate(focus_groups, 1):
            step(f"  [FOCUS SHORT v2] Đang render Focus Short #{g_idx:02d} (gộp tin {','.join(f_ids)})...")
            focus_proj_dir, _, _ = export_focus_short_project(day_dir, f_ids,
                                                              work_proj_dir=os.path.join(html_out_dir, f"short_focus_{g_idx:02d}"),
                                                              global_offset_sec=0.0)
            v_focus = render_html_engine(focus_proj_dir, template="short_news_v2.html", scene_number=None,
                                         fps=VIDEO_FPS, preview=False, force=True)
            if v_focus and os.path.exists(v_focus):
                dest_focus = os.path.join(preview_v2_dir, f"short_focus_{g_idx:02d}.mp4")
                shutil.copy2(v_focus, dest_focus)
                try:
                    from diemdoc.short_outro import append_short_outro
                    append_short_outro(dest_focus, voice_hint="primary")
                except Exception as e:
                    warn(f"Không thể gắn Short Outro cho Focus Short #{g_idx:02d}: {e}")
                out_vids.append(dest_focus)
                ok(f"  🎉 Focus Short #{g_idx:02d} hoàn tất: {paths.rel_to_root(dest_focus)}")

    # 4. RENDER DIGEST SHORT NẾU ĐƯỢC YÊU CẦU
    # (Nếu tất cả các tin đều có digest_line hoặc có file digest_work)
    has_digest_source = any(it.get("digest_line") for it in items)
    if shorts_mode in ["digest", "all"] and not item_filter and has_digest_source:
        step("  [DIGEST SHORT v2] Đang render Digest Short ('Đọc nhanh thể thao')...")
        digest_proj_dir, _, _ = export_digest_short_project(day_dir, [it.get("id") for it in items[:10]],
                                                            work_proj_dir=os.path.join(html_out_dir, "short_digest_01"),
                                                            global_offset_sec=0.0)
        v_digest = render_html_engine(digest_proj_dir, template="short_digest_v2.html", scene_number=None,
                                      fps=VIDEO_FPS, preview=False, force=True)
        if v_digest and os.path.exists(v_digest):
            dest_digest = os.path.join(preview_v2_dir, "short_digest_01.mp4")
            shutil.copy2(v_digest, dest_digest)
            try:
                from diemdoc.short_outro import append_short_outro
                append_short_outro(dest_digest, voice_hint="primary")
            except Exception as e:
                warn(f"Không thể gắn Short Outro cho Digest Short: {e}")
            out_vids.append(dest_digest)
            ok(f"  🎉 Digest Short hoàn tất: {paths.rel_to_root(dest_digest)}")

    # Nếu chạy cả ngày (không filter), ghép nối thành 1 video dài hoàn chỉnh trong _preview_v2
    if not item_filter and chunk_169_files:
        step("  [COMPOSE v2] Ghép nối Video dài 16:9 v2 kèm Intro, Outro và BGM (0.05)...")
        parts = day_str.split(".")
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            d, m = parts[0], parts[1]
        else:
            d, m = "16", "10"
        long_v2_final = os.path.join(preview_v2_dir, f"Tin-The-Thao-{d}-{m}_v2.mp4")

        all_segments = []
        chapter_list = []
        current_seconds = 0.0

        # Intro
        intro_path = os.path.join(_ROOT, "logo", INTRO_NAME)
        if os.path.exists(intro_path):
            intro_norm = os.path.join(work_dir, "intro_norm_v2.mp4")
            norm_cmd = [
                "ffmpeg", "-y", "-v", "error", "-i", intro_path,
                "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={VIDEO_FPS},format=yuv420p",
                "-c:v", ENCODER, *ENCODER_PARAMS,
                "-c:a", "aac", "-ar", "44100", "-ac", "2", intro_norm
            ]
            subprocess.run(norm_cmd, check=True)
            all_segments.append(intro_norm)
            intro_dur = get_audio_duration(intro_norm)
            chapter_list.append(("00:00", "Nhập cuộc bản tin"))
            current_seconds += intro_dur

        # Main Chunks (chuẩn hóa audio sang aac 44100 2ch nếu cần để concat mượt mà)
        for idx, (chunk, item) in enumerate(zip(chunk_169_files, items), 1):
            c_norm = os.path.join(work_dir, f"chunk_{idx:02d}_v2_norm.mp4")
            c_cmd = [
                "ffmpeg", "-y", "-v", "error", "-i", chunk,
                "-c:v", "copy",
                "-c:a", "aac", "-ar", "44100", "-ac", "2", "-b:a", "192k",
                c_norm
            ]
            subprocess.run(c_cmd, check=True)
            all_segments.append(c_norm)
            c_dur = get_audio_duration(chunk)
            minutes = int(current_seconds // 60)
            seconds = int(current_seconds % 60)
            chapter_list.append((f"{minutes:02d}:{seconds:02d}", item.get('title', '').strip()))
            current_seconds += c_dur

        # Outro
        outro_path = os.path.join(_ROOT, "logo", OUTRO_NAMES[0])
        if os.path.exists(outro_path):
            outro_norm = os.path.join(work_dir, "outro_norm_v2.mp4")
            norm_cmd = [
                "ffmpeg", "-y", "-v", "error", "-i", outro_path,
                "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2,fps={VIDEO_FPS},format=yuv420p",
                "-c:v", ENCODER, *ENCODER_PARAMS,
                "-c:a", "aac", "-ar", "44100", "-ac", "2", outro_norm
            ]
            subprocess.run(norm_cmd, check=True)
            all_segments.append(outro_norm)

        # Concat demuxer
        list_txt = os.path.join(work_dir, "concat_list_v2.txt")
        with open(list_txt, "w", encoding="utf-8") as f:
            for seg in all_segments:
                safe_p = seg.replace("\\", "/").replace("'", "'\\''")
                f.write(f"file '{safe_p}'\n")

        tmp_concat = os.path.join(work_dir, "tmp_concat_v2.mp4")
        concat_cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", list_txt, "-c", "copy", tmp_concat]
        res = subprocess.run(concat_cmd)
        if res.returncode != 0:
            fallback_cmd = [
                "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", list_txt,
                "-c:v", ENCODER, *ENCODER_PARAMS,
                "-c:a", "aac", "-b:a", "192k", tmp_concat
            ]
            subprocess.run(fallback_cmd, check=True)

        # Mix BGM (0.05)
        bgm_candidates = [
            os.path.join(paths.ASSETS, "bgm", "bgm_editorial_2_momentum.mp3"),
            os.path.join(paths.ASSETS, "bgm", "bgm_upbeat_blaze.mp3"),
            os.path.join(paths.ASSETS, "bgm", "bgm_default.mp3")
        ]
        bgm_file = next((b for b in bgm_candidates if os.path.exists(b)), None)

        v_dur_concat = get_audio_duration(tmp_concat)
        if bgm_file:
            log(f"  [BGM v2] Mix BGM volume=0.05: {paths.rel_to_root(bgm_file)}", tag="compose")
            mix_cmd = [
                "ffmpeg", "-y", "-v", "error",
                "-i", tmp_concat,
                "-stream_loop", "-1", "-i", bgm_file,
                "-filter_complex", f"[1:a]volume=0.05[bgm];[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0,loudnorm=I=-14:LRA=11:tp=-1.5,atrim=0:{v_dur_concat:.3f}[a_out]",
                "-map", "0:v", "-map", "[a_out]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-t", f"{v_dur_concat:.3f}",
                "-movflags", "+faststart",
                long_v2_final
            ]
            subprocess.run(mix_cmd, check=True)
        else:
            shutil.copy2(tmp_concat, long_v2_final)

        if os.path.exists(tmp_concat):
            try: os.remove(tmp_concat)
            except Exception: pass

        out_vids.append(long_v2_final)
        ok(f"  🎉 Video 16:9 dài hoàn chỉnh v2: {paths.rel_to_root(long_v2_final)}")

        # Tạo Thumbnails A/B/C và mota.txt trong _preview_v2 (tái sử dụng code PIL không ghi đè outputs)
        generate_3_thumbnails_169(day_str, preview_v2_dir, items)

        date_display = f"{d}/{m}/{parts[2] if len(parts) >= 3 else '2026'}"
        top_t1 = items[0]["title"] if len(items) > 0 else "Bản tin thể thao"
        top_t2 = items[1]["title"] if len(items) > 1 else "Diễn biến nóng"
        top_t3 = items[2]["title"] if len(items) > 2 else "Tin tức quốc tế"

        is_spec = (os.path.exists(os.path.join(day_dir, "special_topic"))
                   or os.path.exists(os.path.join(day_dir, "..", "special_topic")))

        existing_mota = os.path.join(day_dir, "mota.txt")
        if os.path.exists(existing_mota) and os.path.getsize(existing_mota) > 100:
            log(f"  [MÔ TẢ] Giữ nguyên mota.txt đã được biên tập sẵn tại {paths.rel_to_root(existing_mota)}")
            shutil.copy2(existing_mota, os.path.join(preview_v2_dir, "mota.txt"))
        else:
            from pathlib import Path
            from diemdoc.publisher import write_mota_16x9
            mota_path = os.path.join(preview_v2_dir, "mota.txt")
            if is_spec:
                titles_abc = [
                    f"{top_t1} | Điểm Đọc Thể Thao",
                    f"{top_t2} | Điểm Đọc Thể Thao",
                    f"{top_t3} | Điểm Đọc Thể Thao",
                ]
                write_mota_16x9(
                    out_path=Path(mota_path),
                    titles_abc=titles_abc,
                    chapters=chapter_list,
                    video_type="thematic_long",
                )
            else:
                titles_abc = [
                    f"Điểm Đọc thể thao {date_display}: {top_t1}",
                    f"{top_t2} và toàn cảnh tin nóng thể thao ngày {date_display}",
                    f"Tổng hợp bản tin thể thao tuần qua ({date_display}) | Điểm Đọc",
                ]
                write_mota_16x9(
                    out_path=Path(mota_path),
                    titles_abc=titles_abc,
                    chapters=chapter_list,
                    video_type="weekly_digest",
                    day_str=date_display,
                )
            shutil.copy2(mota_path, existing_mota)
            log(f"  [MÔ TẢ] Đã xuất {paths.rel_to_root(mota_path)}", tag="publish")
        # Xuất bản trực tiếp vào outputs/<day_str>/ theo đúng chuẩn kênh
        final_main_target = os.path.join(day_dir, f"Tin-The-Thao-{d}-{m}.mp4")
        shutil.copy2(long_v2_final, final_main_target)
        ok(f"  🎬 Đã xuất bản Video Chính 16:9 tại: {paths.rel_to_root(final_main_target)}")

        for t_name in ["thumbnail_A.jpg", "thumbnail_B.jpg", "thumbnail_C.jpg"]:
            t_src = os.path.join(preview_v2_dir, t_name)
            if os.path.exists(t_src):
                shutil.copy2(t_src, os.path.join(day_dir, t_name))

    stop_mem_monitor.set()
    log(f"  📊 Mức RAM đỉnh đo được trong đợt chạy: {peak_rss_mb[0]:.1f} MB", tag="perf")

    return out_vids


# ==============================================================================
# QUY TRÌNH CHÍNH BUILD
# ==============================================================================

def cmd_build(args: argparse.Namespace) -> None:
    verify_assets_or_die()
    day_str = resolve_day_str(args)
    cache_cand = os.path.expanduser(f"~/Library/Caches/DiemDoc/{day_str}")
    outputs_cand = paths.project_dir(day_str)
    if os.path.isabs(day_str) and os.path.exists(day_str):
        day_dir = os.path.abspath(day_str)
        day_str = os.path.basename(day_dir)
    elif os.path.exists(os.path.join(outputs_cand, "thethao.json")) or os.path.exists(os.path.join(outputs_cand, "thethao.txt")):
        day_dir = outputs_cand
    elif os.path.exists(cache_cand):
        day_dir = cache_cand
    else:
        day_dir = outputs_cand
    work_dir = paths.work_project_dir(day_str)
    os.makedirs(day_dir, exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)

    engine = getattr(args, "engine", "html").lower()
    banner(f"RUN_DAY: BƯỚC 2 — SẢN XUẤT VIDEO (BUILD) [ENGINE: {engine.upper()}]", f"Ngày {day_str}")
    t0 = time.time()

    # DỌN SẠCH CÁC THƯ MỤC TẠM TRONG WORK TRƯỚC KHI RENDER
    for sub in ["video_chunks", "temp_render", "shorts_render"]:
        p = os.path.join(work_dir, sub)
        if os.path.exists(p):
            shutil.rmtree(p, ignore_errors=True)
        os.makedirs(p, exist_ok=True)

    json_path = os.path.join(day_dir, "thethao.json")
    audio_dir = os.path.join(day_dir, "audio")
    images_dir = os.path.join(day_dir, "images")
    has_existing_data = os.path.exists(json_path) and os.path.exists(audio_dir) and os.path.exists(images_dir)

    force = getattr(args, "force", False)

    if not has_existing_data:
        # 1. BƯỚC 1: TẢI ẢNH THẬT, LỌC >= 500PX & TỰ ĐỘNG TÌM BỔ SUNG QUA DDGS
        step("1. BƯỚC 1: Tải ảnh thật, lọc kích thước >= 500px & tự động tìm ảnh thiếu qua DDGS...")
        items_draft = step1_download_and_filter_images(day_str, day_dir, work_dir)

        # 2. CHỐT CHẶN KIỂM DUYỆT (MANUAL QA)
        print("\n" + "═" * 78)
        banner("CHỐT CHẶN KIỂM DUYỆT ẢNH (MANUAL QA)", f"outputs/{day_str}/images/")
        print(f"👉 Đã tải xong toàn bộ ảnh chất lượng cao (>= 500px) cho {len(items_draft)} bản tin.")
        print(f"👉 Mời Chủ kênh vào thư mục kiểm tra: outputs/{day_str}/images/")
        print("👉 HƯỚNG DẪN: Hãy mở xem, XÓA những ảnh sai/không khớp nội dung, GIỮ LẠI ảnh đúng.")
        print("👉 Sau khi kiểm duyệt xong, hãy nhấn Enter để hệ thống quét lại ảnh và tiếp tục render...")
        print("═" * 78 + "\n")

        if not getattr(args, "no_pause", False):
            try:
                input("👉 Nhấn Enter để tiếp tục sau khi đã xóa ảnh rác: ")
            except EOFError:
                log(f"Đang dừng chờ Chủ kênh kiểm duyệt ảnh tại: outputs/{day_str}/images/", tag="qa")
                return

        # 3. BƯỚC 1B: QUÉT LẠI THƯ MỤC images/ VÀ LẬP thethao.json CHÍNH THỨC
        step("1b. BƯỚC 1B: Quét lại thư mục images/ sau kiểm duyệt và tạo kịch bản thethao.json...")
        json_path = step1b_map_images_to_json(day_str, day_dir, items_draft)

        # 4. BƯỚC 2: TẠO AUDIO TỪNG TIN ĐỘC LẬP
        step("2. BƯỚC 2: Sinh/Khớp giọng đọc ViTTS Minh Quân Pro từng tin độc lập...")
        step2_generate_audio(day_str, day_dir, work_dir, json_path, force=force)
    else:
        ok(f"Sử dụng dữ liệu có sẵn tại {paths.rel_to_root(day_dir)}/ (thethao.json, images, audio)")
        # Tự động sinh bổ sung nếu có file audio nào bị thiếu hoặc cần cập nhật (nếu force=True thì sinh lại toàn bộ)
        step2_generate_audio(day_str, day_dir, work_dir, json_path, force=force)

    if engine == "html":
        step("3. [ENGINE HTML v2] Render tin tức bằng Engine Playwright + GSAP...")
        item_filter = getattr(args, "item", None)
        shorts_mode = getattr(args, "shorts", "default")
        workers = getattr(args, "workers", 1)
        out_vids = step3_render_scenes_html(day_str, day_dir, work_dir, json_path,
                                            item_filter=item_filter, shorts_mode=shorts_mode,
                                            workers=workers, force=force)
        print()
        ok(f"[ENGINE HTML v2] Render hoàn tất {len(out_vids)} video trong {time.time() - t0:.1f}s!")
        for ov in out_vids:
            log(f"  🎬 Thành phẩm: {ov}")
        return

    # 5. BƯỚC 3: RENDER HÌNH ẢNH TỪNG CẢNH (100% logic 1-169.py)
    step("3. BƯỚC 3: Render từng cảnh video clip Smart Ratio 16:9 + Subtitles bằng FFmpeg...")
    mock = getattr(args, "mock_render", False)
    chunk_files = step3_render_scenes(day_str, day_dir, work_dir, json_path, mock=mock)

    # 6. BƯỚC 4: NỐI FILE VÀ HẬU KỲ (COMPOSE) & THUMBNAIL A/B/C & MOTA.TXT
    step("4. BƯỚC 4: Ghép nối Intro/Outro, Mix BGM (0.05), tạo 3 Thumbnail & mota.txt chuẩn SEO...")
    final_video = step4_compose_video(day_str, day_dir, work_dir, chunk_files, json_path)

    # 7. BƯỚC 5: RENDER VIDEO DỌC SHORTS 9:16 (1-916.py)
    step("5. BƯỚC 5: Render các video dọc Shorts 9:16 bằng engine 1-916.py (is_fast_mode=False)...")
    step5_render_shorts(day_str, day_dir, work_dir)

    dur_final = get_audio_duration(final_video)
    print()
    ok(f"TOÀN BỘ QUY TRÌNH SẢN XUẤT (BUILD) HOÀN TẤT trong {time.time() - t0:.1f}s!")
    print("=" * 80)
    log("🎉 THÀNH PHẨM XUẤT BẢN NGAY TẠI THƯ MỤC NGÀY:")
    log(f"  📁 Thư mục ngày:        {paths.rel_to_root(day_dir)}/")
    log(f"  🎬 Video chính 16:9:    {paths.rel_to_root(final_video)} ({dur_final:.1f}s)")
    log(f"  📱 Thư mục Video Shorts:{paths.rel_to_root(day_dir)}/shorts/")
    log(f"  🖼️  Ảnh Thumbnail (3 cái): thumbnail_A.jpg, thumbnail_B.jpg, thumbnail_C.jpg")
    log(f"  📂 Thư mục con:         images/, audio/, audio-title/")
    log(f"  📝 Kịch bản SEO:        {paths.rel_to_root(day_dir)}/mota.txt")
    print("=" * 80)


# ==============================================================================
# CLI DISPATCHER
# ==============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="run_day.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
══════════════════════════════════════════════════════════════════════════════
  HỆ THỐNG ĐIỀU PHỐI SẢN XUẤT VIDEO THỂ THAO ĐIỂM ĐỌC (run_day.py)
══════════════════════════════════════════════════════════════════════════════
Chuẩn gốc 2 lệnh vận hành:
  1. prepare : Cào tin -> Tải ảnh vào WORK -> LLM tạo thethao.txt, shorts.txt, shorts.json
               -> DỪNG LẠI CHO CHỦ KÊNH DUYỆT BẢN THẢO.
  2. build   : Đọc thethao.txt -> tạo thethao.json -> Voice ViTTS -> Render FFmpeg/Pillow
               (100% 1-169.py & 1-916.py) -> Xuất video 16:9, Shorts, 3 Thumbnail vào outputs/DD.MM.YYYY/
        """
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Lệnh thực thi chính")

    # 1. Prepare
    prep_p = subparsers.add_parser("prepare", help="Bước 1: Cào tin & tạo outputs/DD.MM.YYYY/thethao.txt để duyệt")
    prep_p.add_argument("--project", default=None, help="Bí danh ngày/dự án (VD: 16.10.2026)")
    prep_p.add_argument("--day", default=None, help="Tên thư mục ngày (mặc định: ngày hôm nay theo format DD.MM.YYYY)")
    prep_p.add_argument("--date", default=None, help="Bí danh ngày (chấp nhận YYYY-MM-DD hoặc DD.MM.YYYY)")
    prep_p.add_argument("--period", choices=["weekly", "yesterday"], default=None, help="Cửa sổ chuẩn: weekly (00:01 T2 tuần trước -> 23:59 CN tuần trước) hoặc yesterday (12:00 trưa hôm qua -> nay)")
    prep_p.add_argument("--since", default=None, help="Chỉ lấy tin từ mốc thời gian này trở về sau (VD: '2026-10-15 00:01')")
    prep_p.add_argument("--until", default=None, help="Chỉ lấy tin đến mốc thời gian này trở về trước (VD: '2026-10-21 23:59')")
    prep_p.add_argument("--test", action="store_true", help="Sử dụng dữ liệu test cache để kiểm tra nhanh")

    # 2. Build
    build_p = subparsers.add_parser("build", help="Bước 2: Sản xuất video hoàn chỉnh từ thethao.txt đã duyệt")
    build_p.add_argument("--project", default=None, help="Bí danh ngày/dự án (VD: 16.10.2026)")
    build_p.add_argument("--day", default=None, help="Tên thư mục ngày (mặc định: ngày hôm nay theo format DD.MM.YYYY)")
    build_p.add_argument("--date", default=None, help="Bí danh ngày (chấp nhận YYYY-MM-DD hoặc DD.MM.YYYY)")
    build_p.add_argument("--mock-render", action="store_true", help="Bỏ qua render video chi tiết, test nhanh luồng nối audio")
    build_p.add_argument("--engine", choices=["html", "pil"], default="html", help="Chọn render engine (mặc định: html v2; tùy chọn: pil)")
    build_p.add_argument("--item", type=int, default=None, help="Chỉ render 1 tin cụ thể theo số thứ tự 1-based (áp dụng cho --engine html)")
    build_p.add_argument("--shorts", choices=["default", "focus", "digest", "all", "none"], default="default",
                          help="Chế độ render shorts: default (1 tin/short cũ), focus (gộp 3-5 tin), digest (đọc nhanh), all (cả focus và digest), none (chỉ video chính 16:9)")
    build_p.add_argument("--workers", type=int, default=1, help="Số tiến trình Playwright chạy song song (mặc định: 1)")
    build_p.add_argument("--force", action="store_true", help="Bỏ qua .run_state và render lại từ đầu")

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        sys.exit(0)

    if args.subcommand == "prepare":
        cmd_prepare(args)
    elif args.subcommand == "build":
        cmd_build(args)


if __name__ == "__main__":
    main()
