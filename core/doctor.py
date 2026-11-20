#!/usr/bin/env python3
"""
doctor.py — KIỂM TRA TOÀN DIỆN MÔI TRƯỜNG & HẠ TẦNG KÊNH ĐIỂM ĐỌC
===================================================================
Kiểm tra tất cả các phụ thuộc, công cụ hệ thống, gói thư viện AI,
tài nguyên font/âm thanh/icon, và các quy tắc Google Drive.
Thoát mã 0 nếu tất cả PASS, thoát mã 1 nếu có bất kỳ mục nào FAIL.
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import os
import shutil
import subprocess
import json
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core", "vendor"))
sys.path.insert(1, os.path.join(_ROOT, "core"))

from diemdoc import paths

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
WARN = "\033[93mWARN\033[0m"

checks: list[tuple[str, bool, str]] = []


def record(name: str, passed: bool, detail: str = "") -> None:
    checks.append((name, passed, detail))
    status = PASS if passed else FAIL
    print(f"[{status}] {name}")
    if detail:
        print(f"       -> {detail}")


def main() -> int:
    print("=" * 70)
    print("   BÁC SĨ HỆ THỐNG (DOCTOR) — ĐIỂM ĐỌC (DD-The-thao)")
    print("=" * 70)

    # 1. Python version >= 3.10
    py_ok = sys.version_info >= (3, 10)
    record("Python >= 3.10", py_ok, f"Phiên bản: {sys.version.split()[0]} ({sys.executable})")

    # 2. FFmpeg & Filters
    ffmpeg_bin = shutil.which("ffmpeg")
    ffprobe_bin = shutil.which("ffprobe")
    ff_installed = bool(ffmpeg_bin and ffprobe_bin)
    record("FFmpeg & FFprobe cài đặt", ff_installed, f"ffmpeg: {ffmpeg_bin}, ffprobe: {ffprobe_bin}")

    if ff_installed:
        r = subprocess.run(["ffmpeg", "-filters"], capture_output=True, text=True)
        filters_out = r.stdout
        has_rubberband = "rubberband" in filters_out
        has_loudnorm = "loudnorm" in filters_out
        has_xfade = "xfade" in filters_out
        has_sidechaincompress = "sidechaincompress" in filters_out
        has_acrossfade = "acrossfade" in filters_out
        record("FFmpeg filter: rubberband", has_rubberband, "Hỗ trợ thay đổi pitch và tempo độc lập")
        record("FFmpeg filter: loudnorm", has_loudnorm, "Chuẩn hóa âm lượng EBU R128 (-14 LUFS)")
        record("FFmpeg filter: xfade", has_xfade, "Hỗ trợ nối chuyển cảnh mượt mà giữa các scene")
        record("FFmpeg filter: sidechaincompress", has_sidechaincompress, "Hạ âm lượng BGM tự động khi có giọng nói (Ducking)")
        record("FFmpeg filter: acrossfade", has_acrossfade, "Nối playlist BGM mượt mà với acrossfade d=3s")

    # 3. Playwright & Chromium
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content("<h1>Diem Doc Test</h1>")
            txt = page.inner_text("h1")
            browser.close()
        record("Playwright & Chromium launch", txt == "Diem Doc Test", "Chromium khởi chạy và render DOM bình thường")
    except Exception as e:
        record("Playwright & Chromium launch", False, f"Lỗi khởi chạy: {e}")

    # 4. OpenAI Whisper & Model cache
    try:
        import whisper
        whisper_dir = os.path.expanduser("~/.cache/whisper")
        medium_model = os.path.join(whisper_dir, "medium.pt")
        has_medium = os.path.exists(medium_model) and os.path.getsize(medium_model) > 1_000_000_000
        sz_mb = os.path.getsize(medium_model) / (1024 * 1024) if os.path.exists(medium_model) else 0
        record("OpenAI Whisper & medium.pt cache", has_medium, f"Vị trí: {medium_model} ({sz_mb:.1f} MB)")
    except Exception as e:
        record("OpenAI Whisper & medium.pt cache", False, f"Lỗi: {e}")

    # 5. VieNeu-TTS (ViTTS) & Weights cache
    try:
        import vieneu
        pkg_file = os.path.abspath(vieneu.__file__)
        is_vendored = "core/vendor" in pkg_file or "core\\vendor" in pkg_file

        # Check vendor info / version
        vendor_info = os.path.join(_ROOT, "core", "vendor", "VENDOR_INFO.md")
        has_vendor_info = os.path.exists(vendor_info)

        record(
            "Gói VieNeu-TTS vendored (core/vendor/vieneu)",
            is_vendored and has_vendor_info,
            f"Tải từ: {pkg_file} (vendored={is_vendored})"
        )

        # Kiểm tra model cache HuggingFace (v3-Turbo & Codec)
        hf_dir = os.path.expanduser("~/.cache/huggingface/hub")
        v3_dir = os.path.join(hf_dir, "models--pnnbao-ump--VieNeu-TTS-v3-Turbo")
        codec_dir = os.path.join(hf_dir, "models--pnnbao-ump--VieNeu-Codec")
        has_v3_cache = os.path.exists(v3_dir)
        has_codec_cache = os.path.exists(codec_dir)

        v3_sz_mb = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(v3_dir) for f in fs) / (1024 * 1024) if has_v3_cache else 0
        codec_sz_mb = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(codec_dir) for f in fs) / (1024 * 1024) if has_codec_cache else 0

        weights_ok = has_v3_cache and has_codec_cache and v3_sz_mb > 1000 and codec_sz_mb > 500
        detail_msg = f"v3-Turbo: {v3_sz_mb:.1f} MB | Codec: {codec_sz_mb:.1f} MB"
        record("VieNeu-TTS v3turbo weights cache", weights_ok, detail_msg)
    except Exception as e:
        record("Gói VieNeu-TTS (vieneu)", False, f"Lỗi import: {e}")

    # 6. Các gói hỗ trợ cào tin & xử lý dữ liệu
    required_pkgs = [
        ("trafilatura", "Bóc tách text bài báo"),
        ("bs4", "BeautifulSoup quét DOM ảnh"),
        ("feedparser", "Đọc luồng RSS thể thao"),
        ("requests", "Tải stream HTTP"),
        ("PIL", "Pillow xử lý ảnh"),
        ("pydub", "Xử lý audio segment"),
        ("numpy", "Mảng số ma trận")
    ]
    for pkg_name, role in required_pkgs:
        try:
            __import__(pkg_name)
            record(f"Thư viện {pkg_name}", True, role)
        except ImportError:
            record(f"Thư viện {pkg_name}", False, f"Chưa cài đặt {pkg_name}")

    # 7. Tài nguyên assets (fonts, sfx, bgm, icons, logo)
    font_count = len([d for d in os.listdir(paths.FONTS) if os.path.isdir(os.path.join(paths.FONTS, d))]) if os.path.exists(paths.FONTS) else 0
    sfx_count = len([f for f in os.listdir(paths.SFX) if f.endswith(".mp3")]) if os.path.exists(paths.SFX) else 0
    bgm_count = len([f for f in os.listdir(paths.BGM) if f.endswith(".mp3")]) if os.path.exists(paths.BGM) else 0
    icon_count = len([f for f in os.listdir(paths.ICONS) if f.endswith(".svg")]) if os.path.exists(paths.ICONS) else 0

    logo1 = os.path.join(paths.LOGO, "diem-doc-logo-1.png")
    logo2 = os.path.join(paths.LOGO, "diem-doc-logo-2.png")
    has_logos = os.path.exists(logo1) and os.path.exists(logo2) and os.path.getsize(logo1) > 0 and os.path.getsize(logo2) > 0

    # Kiểm tra 0-byte file trong assets
    zero_files = []
    for root, dirs, files in os.walk(paths.ASSETS):
        for f in files:
            if not f.startswith("."):
                fp = os.path.join(root, f)
                if os.path.getsize(fp) == 0:
                    zero_files.append(os.path.relpath(fp, paths.ASSETS))

    assets_ok = (font_count >= 11 and sfx_count >= 28 and bgm_count >= 36 and icon_count >= 58 and has_logos and len(zero_files) == 0)
    detail_assets = f"Fonts: {font_count}/11 | SFX: {sfx_count}/28 | BGM: {bgm_count}/36 | Icons: {icon_count}/58 | Logos: {'Đủ' if has_logos else 'Thiếu'} | 0-byte: {len(zero_files)}"
    record("Tài nguyên Assets đầy đủ", assets_ok, detail_assets)

    # 8. Thư mục làm việc tạm ngoài Drive (WORK)
    work_ok = os.path.exists(paths.WORK) and os.access(paths.WORK, os.W_OK) and ("CloudStorage" not in paths.WORK)
    record("Thư mục WORK ngoài Drive", work_ok, f"Đường dẫn: {paths.WORK} (Không chứa CloudStorage)")

    # 9. Kiểm tra sạch mã tạm: không __pycache__, không .pyc, không venv trong DD-The-thao
    dirty_items = []
    for root, dirs, files in os.walk(paths.ROOT):
        # bỏ qua thư mục _ref và Thamkhao
        if "_ref" in root or "Thamkhao" in root:
            continue
        for d in dirs:
            p = os.path.join(root, d)
            if d in ("__pycache__", "venv", ".venv"):
                dirty_items.append(p)
            elif d == "node_modules" and not os.path.islink(p):
                dirty_items.append(p)
        for f in files:
            if f.endswith(".pyc"):
                dirty_items.append(os.path.join(root, f))
    clean_ok = len(dirty_items) == 0
    record("Không có __pycache__/.pyc/venv", clean_ok, f"Tệp/thư mục vi phạm: {len(dirty_items)}")

    # 10. Thử nghiệm file_url với đường dẫn thật có dấu cách/tiếng Việt
    test_html = os.path.join(paths.TEMPLATES, "long_cinematic.html")
    url = paths.file_url(test_html)
    url_ok = False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            resp = page.goto(url, wait_until="load")
            title = page.title()
            browser.close()
            url_ok = bool(title)
        record("file_url an toàn với dấu tiếng Việt/khoảng trắng", url_ok, f"URL: {url[:75]}... -> Title: {title}")
    except Exception as e:
        record("file_url an toàn với dấu tiếng Việt/khoảng trắng", False, f"Lỗi mở file:// url: {e}")

    # 11. Dung lượng ổ cứng khả dụng >= 10 GB
    st = os.statvfs(paths.ROOT)
    free_gb = (st.f_bavail * st.f_frsize) / (1024 ** 3)
    disk_ok = free_gb >= 10.0
    record("Dung lượng ổ trống >= 10 GB", disk_ok, f"Khả dụng: {free_gb:.1f} GB")

    # 12. Thư viện client GSAP vendored (tự chứa, không phụ thuộc node_modules)
    gsap_file = os.path.join(paths.ASSETS, "vendor", "js", "gsap.min.js")
    custom_ease = os.path.join(paths.ASSETS, "vendor", "js", "CustomEase.min.js")
    has_gsap = os.path.exists(gsap_file) and os.path.getsize(gsap_file) > 10000
    has_ease = os.path.exists(custom_ease) and os.path.getsize(custom_ease) > 1000
    record("Thư viện GSAP vendored tự chứa", has_gsap and has_ease, f"gsap.min.js ({os.path.getsize(gsap_file) if os.path.exists(gsap_file) else 0} B), CustomEase.min.js")

    # 13. Font tiếng Việt Barlow Condensed & Be Vietnam Pro
    barlow_file = os.path.join(paths.FONTS, "Barlow_Condensed", "BarlowCondensed-Bold.ttf")
    vietnam_file = os.path.join(paths.FONTS, "Be_Vietnam_Pro", "BeVietnamPro-SemiBold.ttf")
    font_vn_ok = False
    try:
        from PIL import Image, ImageDraw, ImageFont
        test_txt = "ĐIỂM ĐỌC — Tuyển Việt Nam quyết thắng Kyrgyzstan và Đài Loan"
        fb = ImageFont.truetype(barlow_file, 36)
        fv = ImageFont.truetype(vietnam_file, 28)
        t_img = Image.new("RGB", (600, 100), (0, 0, 0))
        t_draw = ImageDraw.Draw(t_img)
        t_draw.text((10, 10), test_txt, font=fb, fill=(255, 255, 255))
        t_draw.text((10, 50), test_txt, font=fv, fill=(245, 158, 11))
        font_vn_ok = True
        record("Font tiếng Việt (Barlow & Be Vietnam Pro)", True, "Hỗ trợ đầy đủ dấu thanh tiếng Việt")
    except Exception as e:
        record("Font tiếng Việt (Barlow & Be Vietnam Pro)", False, f"Lỗi render font: {e}")

    # 14. Thư viện overlay tự chứa (dd_overlay.js)
    overlay_file = os.path.join(paths.ASSETS, "overlays", "dd_overlay.js")
    has_overlay = os.path.exists(overlay_file) and os.path.getsize(overlay_file) > 1000
    record("Thư viện DDOverlay tự chứa (dd_overlay.js)", has_overlay, f"assets/overlays/dd_overlay.js ({os.path.getsize(overlay_file) if os.path.exists(overlay_file) else 0} B)")

    print("=" * 70)
    failed_checks = [c for c in checks if not c[1]]
    if failed_checks:
        print(f"\033[91mCÓ {len(failed_checks)} MỤC THẤT BẠI (FAIL)!\033[0m")
        return 1
    else:
        print("\033[92m100% CÁC MỤC KIỂM TRA ĐỀU ĐẠT (ALL PASS)!\033[0m")
        return 0


if __name__ == "__main__":
    sys.exit(main())
