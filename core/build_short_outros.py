#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng 3 mẫu Outro cho video Short 9:16 (1080x1920 @ 30fps, 5-8s) — Kênh Điểm Đọc.
==============================================================================
Lấy cảm hứng từ Outro video dài (logo/Outro.mp4) và phát triển thành 3 phong cách
hoàn toàn khác nhau cho Shorts:
  1. Outro_Short_1_Cyber_Pulse.mp4        (~6.5s, Giọng Nữ Ngọc Huyền #14)
  2. Outro_Short_2_Tactical_Broadcast.mp4 (~6.0s, Giọng Nam Minh Quân Pro #15)
  3. Outro_Short_3_Kinetic_Slam.mp4       (~5.8s, Giọng Nữ Ngọc Huyền #14)

Xuất thành phẩm vào: logo/short_outros/
Bảng ảnh đối chứng QA: logo/short_outros/qa/contact_short_outros.jpg
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
sys.path.insert(0, str(_ROOT / "core"))
sys.path.insert(0, str(_ROOT / "engines" / "html"))

from diemdoc import paths
from diemdoc.audio import (
    apply_sidechain_ducking,
    apply_voice_standard,
    build_sfx_track,
    measure_loudness,
    measure_voice_bgm_separation,
    mix_master_audio,
)
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.publisher import load_voice_preset
from diemdoc.tts_text import prepare
from m3_voice import render_chunk_vitts, trim_segment_silence
from renderer import VIRTUAL_TIME_SHIM


OUTRO_SPECS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "slug": "Outro_Short_1_Cyber_Pulse",
        "label": "Mẫu 1: Cyber Pulse & Interactive Tap",
        "template": "short_outro_1_cyber_pulse.html",
        "voice_preset": "secondary",  # Nữ Ngọc Huyền #14
        "voice_text": "Cảm ơn bạn đã xem video! Hãy tặng Điểm Đọc một like và một đăng ký kênh nhé!",
        "target_dur": 6.50,
        "bgm_file": "bgm_upbeat_3_intro_7s.mp3",
        "sfx_events": [
            {"time": 0.04, "file": "whoosh_cinematic_short.mp3"},
            {"time": 1.70, "file": "pop_card.mp3"},
            {"time": 3.68, "file": "click_button_soft.mp3"},
            {"time": 4.00, "file": "bell_ping_highlight.mp3"},
        ],
    },
    {
        "id": 2,
        "slug": "Outro_Short_2_Tactical_Broadcast",
        "label": "Mẫu 2: Tactical Broadcast Scoreboard",
        "template": "short_outro_2_tactical_broadcast.html",
        "voice_preset": "primary",  # Nam Minh Quân Pro #15
        "voice_text": "Theo dõi Điểm Đọc ngay để không bỏ lỡ tin nóng thể thao mỗi ngày!",
        "target_dur": 6.00,
        "bgm_file": "bgm_tech_3_8s.mp3",
        "sfx_events": [
            {"time": 0.04, "file": "sub_drop_boom.mp3"},
            {"time": 1.12, "file": "whoosh_clean_1.mp3"},
            {"time": 2.26, "file": "chimes_reveal.mp3"},
        ],
    },
    {
        "id": 3,
        "slug": "Outro_Short_3_Kinetic_Slam",
        "label": "Mẫu 3: Kinetic Slam & Fast Loop",
        "template": "short_outro_3_kinetic_slam.html",
        "voice_preset": "secondary",  # Nữ Ngọc Huyền #14
        "voice_text": "Thấy hay thì thả tim, bấm theo dõi Điểm Đọc ngay nhé!",
        "target_dur": 5.40,
        "bgm_file": "bgm_upbeat_blaze.mp3",
        "sfx_events": [
            {"time": 0.03, "file": "sub_drop_boom.mp3"},
            {"time": 0.96, "file": "pop_click_clean.mp3"},
            {"time": 1.88, "file": "whoosh_cinematic_short.mp3"},
            {"time": 2.90, "file": "bell_ping_highlight.mp3"},
        ],
    },
]


def synthesize_outro_voice(tts_model: Any, spec: Dict[str, Any], work_dir: Path, cache_dir: Path) -> tuple[Path, float]:
    """Sinh giọng đọc ViTTS, đệm 0.25s mở đầu và căn tổng thời lượng trong khoảng 5-8s."""
    preset = load_voice_preset(spec["voice_preset"])
    voice_id = preset["voice_id"]
    spd, pch, temp = preset["speed"], preset["pitch"], preset["temperature"]
    step(f"Mẫu #{spec['id']} — Giọng {preset['voice_label']} (spd={spd}, pch={pch}, temp={temp})")

    clean_text, _ = prepare(spec["voice_text"])
    raw_seg, _ = render_chunk_vitts(
        tts_model,
        clean_text,
        voice_id,
        temperature=temp,
        speed=spd,
        pitch=pch,
        cache_dir=str(cache_dir),
        use_cache=True,
        max_chars=768,
    )
    raw_seg = trim_segment_silence(raw_seg)
    voice_std = apply_voice_standard(raw_seg)

    lead_ms = 260
    voice_dur = voice_std.duration_seconds
    total_dur = max(float(spec["target_dur"]), round(lead_ms / 1000.0 + voice_dur + 1.0, 2))
    total_dur = min(7.80, max(5.20, total_dur))
    # Làm tròn theo frame 30fps để A/V khớp tuyệt đối
    n_frames = int(round(total_dur * 30))
    total_dur = n_frames / 30.0

    tail_ms = max(200, int(round(total_dur * 1000)) - lead_ms - len(voice_std))
    padded = AudioSegment.silent(duration=lead_ms, frame_rate=44100) + voice_std + AudioSegment.silent(duration=tail_ms, frame_rate=44100)
    padded = padded[: int(round(total_dur * 1000))].set_channels(2).set_frame_rate(44100)

    voice_wav = work_dir / f"voice_{spec['id']}.wav"
    padded.export(str(voice_wav), format="wav")
    ok(f"Voice Mẫu #{spec['id']}: voice={voice_dur:.2f}s -> tổng duration={total_dur:.2f}s ({n_frames} frames)")
    return voice_wav, total_dur


def build_master_audio_for_outro(spec: Dict[str, Any], voice_wav: Path, total_dur: float, work_dir: Path) -> Path:
    """Trộn Voice + Ducked BGM + SFX track và two-pass loudnorm (-14 LUFS)."""
    bgm_src = Path(paths.BGM) / spec["bgm_file"]
    if not bgm_src.exists():
        die(f"Thiếu file BGM: {bgm_src}")

    bgm_cut = work_dir / f"bgm_cut_{spec['id']}.wav"
    fade_out_st = max(0.2, total_dur - 0.9)
    subprocess.run(
        [
            "ffmpeg", "-y", "-v", "error",
            "-stream_loop", "-1", "-i", str(bgm_src),
            "-t", f"{total_dur:.3f}",
            "-af", f"aresample=44100,afade=t=in:st=0:d=0.2,afade=t=out:st={fade_out_st:.3f}:d=0.9",
            "-ac", "2", "-ar", "44100",
            str(bgm_cut),
        ],
        check=True,
    )

    ducked_bgm = work_dir / f"bgm_ducked_{spec['id']}.wav"
    duck_cfg = {
        "ducking": {
            "threshold": 0.035,
            "ratio": 10.0,
            "attack": 20.0,
            "release": 350.0,
            "bgm_base_volume": 0.14,
        }
    }
    if not apply_sidechain_ducking(str(voice_wav), str(bgm_cut), str(ducked_bgm), config=duck_cfg):
        die("Ducking thất bại!")

    sep = measure_voice_bgm_separation(str(voice_wav), str(ducked_bgm))
    log(f"Mẫu #{spec['id']} Separation Voice/BGM = {sep:.2f} dB", tag="audio")

    sfx_wav = work_dir / f"sfx_{spec['id']}.wav"
    sfx_cfg = {"sfx": {"volume": 0.34, "min_gap_sec": 0.25, "max_density_per_min": 40}}
    sfx_path_str, n_sfx = build_sfx_track(spec["sfx_events"], total_dur, str(sfx_wav), config=sfx_cfg)
    log(f"Mẫu #{spec['id']} SFX events = {n_sfx}", tag="audio")

    master_wav = work_dir / f"master_{spec['id']}.wav"
    mix_cfg = {"loudness": {"I": -14.0, "TP": -1.5, "LRA": 11.0}}
    if not mix_master_audio(str(voice_wav), str(ducked_bgm), sfx_path_str, str(master_wav), total_dur, config=mix_cfg):
        die("mix_master_audio thất bại!")

    return master_wav


def render_outro_video(spec: Dict[str, Any], total_dur: float, master_wav: Path, work_dir: Path, out_mp4: Path) -> None:
    """Render template HTML 1080x1920 @ 30fps qua Playwright Virtual Clock -> FFmpeg."""
    from playwright.sync_api import sync_playwright

    tpl_path = Path(paths.TEMPLATES) / spec["template"]
    if not tpl_path.exists():
        die(f"Thiếu template: {tpl_path}")

    html = tpl_path.read_text(encoding="utf-8")
    html = html.replace("__ASSETS__", paths.file_url(paths.ASSETS))
    html = html.replace("__LOGO__", paths.file_url(str(Path(paths.LOGO) / "diem-doc-logo-1.png")))

    inject_js = f"window.VIDEO_DATA = {json.dumps({'duration': total_dur, 'slug': spec['slug']}, ensure_ascii=False)};"
    html = html.replace("// __INJECT_JSON_HERE__", inject_js)

    html_out = work_dir / f"render_{spec['id']}.html"
    html_out.write_text(html, encoding="utf-8")

    fps = 30
    vw, vh = 1080, 1920
    n_frames = int(round(total_dur * fps))
    video_only = work_dir / f"video_only_{spec['id']}.mp4"

    step(f"Render {spec['slug']} ({vw}x{vh} @ {fps}fps, {total_dur:.2f}s / {n_frames} frames)...")
    enc = subprocess.Popen(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
            "-vf", "format=yuv420p",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-r", str(fps), "-movflags", "+faststart",
            str(video_only),
        ],
        stdin=subprocess.PIPE,
    )

    js_errors: List[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--allow-file-access-from-files",
                "--disable-dev-shm-usage",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--font-render-hinting=none",
            ],
        )
        ctx = browser.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=1)
        ctx.add_init_script(VIRTUAL_TIME_SHIM)
        page = ctx.new_page()
        page.on("pageerror", lambda e: js_errors.append(str(e)))
        page.goto(paths.file_url(str(html_out)), wait_until="load")
        page.evaluate(
            """async () => {
                if (document.fonts && document.fonts.ready) await document.fonts.ready;
                const imgs = Array.from(document.images);
                await Promise.all(imgs.map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })));
            }"""
        )
        for i in range(n_frames):
            page.evaluate("ms => window.__vt.advanceTo(ms)", i * 1000.0 / fps)
            buf = page.screenshot(type="jpeg", quality=95, animations="allow", caret="hide")
            enc.stdin.write(buf)
        browser.close()

    enc.stdin.close()
    if enc.wait() != 0:
        die(f"FFmpeg encode thất bại cho {spec['slug']}")
    if js_errors:
        warn(f"JS errors ({spec['slug']}): {js_errors[0]}")

    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(video_only),
            "-i", str(master_wav),
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            "-t", f"{total_dur:.6f}",
            "-movflags", "+faststart",
            str(out_mp4),
        ],
        check=True,
    )

    loud = measure_loudness(str(out_mp4))
    if loud:
        ok(f"Xuất {out_mp4.name} | {total_dur:.2f}s | I={loud['input_i']:.2f} LUFS | TP={loud['input_tp']:.2f} dBTP")


def build_qa_contact_sheet(results: List[Dict[str, Any]], work_dir: Path, qa_dir: Path) -> Path:
    """Trích 6 keyframe mỗi mẫu và ghép thành bảng đối chứng thị giác QA."""
    qa_dir.mkdir(parents=True, exist_ok=True)
    cols = 6
    rows = len(results)
    thumb_w, thumb_h = 270, 480
    pad_x, pad_y = 22, 74
    header_h = 90
    canvas_w = cols * (thumb_w + pad_x) + pad_x
    canvas_h = header_h + rows * (thumb_h + pad_y) + 24

    sheet = Image.new("RGB", (canvas_w, canvas_h), (8, 12, 22))
    draw = ImageDraw.Draw(sheet)
    try:
        f_hdr = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
        f_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
        f_lbl = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 17)
    except Exception:
        f_hdr = f_sub = f_lbl = ImageFont.load_default()

    draw.text((pad_x, 16), "QA CONTACT SHEET — 3 MAU SHORT OUTRO (9:16 | 5-8s)", fill=(0, 229, 255), font=f_hdr)
    draw.text((pad_x, 54), "Kenh Diem Doc | 1080x1920 @ 30fps | Cyber-Stadium Electric Cyan | -14 LUFS", fill=(180, 198, 220), font=f_sub)

    for r_idx, item in enumerate(results):
        mp4 = item["mp4"]
        dur = item["duration"]
        y0 = header_h + r_idx * (thumb_h + pad_y)
        draw.text((pad_x, y0 + 4), f"{item['label']} ({mp4.name} | {dur:.2f}s)", fill=(250, 204, 21), font=f_lbl)

        for c_idx in range(cols):
            t_sec = round((dur - 0.15) * (c_idx / (cols - 1)), 2)
            frame_jpg = work_dir / f"qa_r{r_idx}_c{c_idx}.jpg"
            subprocess.run(
                [
                    "ffmpeg", "-y", "-loglevel", "error",
                    "-ss", f"{t_sec:.2f}", "-i", str(mp4),
                    "-frames:v", "1", "-q:v", "2",
                    str(frame_jpg),
                ],
                check=True,
            )
            x0 = pad_x + c_idx * (thumb_w + pad_x)
            fy = y0 + 32
            draw.rectangle([x0 - 2, fy - 2, x0 + thumb_w + 2, fy + thumb_h + 2], outline=(0, 180, 216), width=2)
            with Image.open(frame_jpg) as im:
                im_rgb = im.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                sheet.paste(im_rgb, (x0, fy))
            draw.text((x0 + 6, fy + thumb_h + 6), f"t = {t_sec:.2f}s", fill=(0, 229, 255), font=f_lbl)

    out_sheet = qa_dir / "contact_short_outros.jpg"
    sheet.save(out_sheet, format="JPEG", quality=92)
    ok(f"Đã tạo Contact Sheet QA: {out_sheet}")
    return out_sheet


def main() -> None:
    banner("DỰNG 3 MẪU SHORT OUTRO (9:16 | 5-8 GIÂY) — ĐIỂM ĐỌC")
    out_dir = _ROOT / "logo" / "short_outros"
    qa_dir = out_dir / "qa"
    work_dir = Path(paths.WORK) / "short_outros_work"
    cache_dir = Path(paths.WORK) / "tts_cache_short_outros"
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    step("Khởi tạo ViTTS v3turbo...")
    from vieneu import Vieneu
    tts_model = Vieneu(mode="v3turbo")

    results: List[Dict[str, Any]] = []
    for spec in OUTRO_SPECS:
        banner(spec["label"])
        voice_wav, total_dur = synthesize_outro_voice(tts_model, spec, work_dir, cache_dir)
        master_wav = build_master_audio_for_outro(spec, voice_wav, total_dur, work_dir)
        out_mp4 = out_dir / f"{spec['slug']}.mp4"
        render_outro_video(spec, total_dur, master_wav, work_dir, out_mp4)
        subprocess.run(["python3", "-B", str(_ROOT / "core" / "audio_check.py"), str(out_mp4)], check=False)
        results.append({"label": spec["label"], "mp4": out_mp4, "duration": total_dur})

    build_qa_contact_sheet(results, work_dir, qa_dir)
    banner("HOÀN TẤT XUẤT BẢN 3 MẪU SHORT OUTRO")


if __name__ == "__main__":
    main()
