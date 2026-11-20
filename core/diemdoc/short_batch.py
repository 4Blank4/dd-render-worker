# -*- coding: utf-8 -*-
"""
Trình hỗ trợ dựng hàng loạt video Short 9:16 độc lập (Điểm Đọc).

Gom các bước lặp lại: kiểm tra & sao chép ảnh sạch, xuất Contact Sheet QA,
tổng hợp audio chuẩn -14 LUFS qua ViTTS + config/voice.json, ghi metadata ngày,
export bridge timeline, render HTML v2, căn chỉnh A/V drift <= 1 frame,
và xuất Thumbnail 9:16 + Mô tả SEO YouTube qua publisher.py.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment

from . import paths
from .audio import apply_voice_standard, measure_loudness
from .log import banner, die, ok, step, warn
from .publisher import load_voice_preset, render_thumbnail_9x16, write_mota_9x16
from .short_outro import append_short_outro
from .tts_text import prepare

ROOT_DIR = Path(paths.ROOT)
if str(ROOT_DIR / "core") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "core"))
if str(ROOT_DIR / "engines" / "html") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "engines" / "html"))

from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from m8_news_bridge import export_bridge_project
from renderer import render_html_engine


@dataclass
class ShortDayContext:
    """Bối cảnh thư mục cho một ngày sản xuất video Shorts độc lập."""

    day_dir: Path
    inspect_dir: Path
    work_tag: str

    @property
    def shorts_dir(self) -> Path:
        return self.day_dir / "shorts"

    @property
    def images_dir(self) -> Path:
        return self.day_dir / "images"

    @property
    def audio_dir(self) -> Path:
        return self.day_dir / "audio"

    @property
    def audio_title_dir(self) -> Path:
        return self.day_dir / "audio-title"

    @property
    def qa_dir(self) -> Path:
        return self.day_dir / "qa"

    @property
    def cache_dir(self) -> str:
        return os.path.join(paths.WORK, f"tts_cache_{self.work_tag}")

    @property
    def work_shorts_dir(self) -> str:
        return os.path.join(paths.WORK, f"{self.work_tag}_shorts")

    def ensure_dirs(self) -> None:
        for d in (self.shorts_dir, self.images_dir, self.audio_dir, self.audio_title_dir, self.qa_dir):
            d.mkdir(parents=True, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.work_shorts_dir, exist_ok=True)


def has_dense_edge_overlay(pil_img: Image.Image) -> bool:
    """Kiểm tra mật độ cạnh cao vùng giữa ảnh nhằm cảnh báo chữ watermark chìm."""
    w, h = pil_img.size
    crop = pil_img.crop((int(w * 0.25), int(h * 0.35), int(w * 0.75), int(h * 0.65))).convert("L")
    arr = np.array(crop, dtype=np.float32)
    if arr.shape[0] < 2 or arr.shape[1] < 2:
        return False
    gx = np.abs(np.diff(arr, axis=1))[:-1, :]
    gy = np.abs(np.diff(arr, axis=0))[:, :-1]
    return float(np.mean((gx > 25) | (gy > 25))) > 0.65


def copy_and_verify_images(ctx: ShortDayContext, item: Dict[str, Any]) -> Dict[str, str]:
    """Sao chép và kiểm tra ảnh đã duyệt từ inspect_dir vào images/ của ngày."""
    credits_map: Dict[str, str] = {}
    for spec in item["images"]:
        src_path = Path(spec["abs_src"]) if spec.get("abs_src") else (ctx.inspect_dir / spec["src"])
        if not src_path.exists():
            die(f"Thiếu ảnh nguồn: {src_path}")
        with Image.open(src_path) as im:
            im = im.convert("RGB")
            w, h = im.size
            if w < 550 or h < 320:
                die(f"Ảnh {src_path} độ phân giải quá thấp: {w}x{h}")
            if has_dense_edge_overlay(im):
                warn(f"Cảnh báo mật độ cạnh cao trên {src_path.name} ({w}x{h}) — giữ vì đã duyệt thị giác.")
            im.save(ctx.images_dir / spec["dest"], format="JPEG", quality=95, optimize=True)
        credits_map[spec["dest"]] = spec["credit"]
        ok(f"Đã nạp ảnh sạch: {spec['dest']} ({w}x{h}, {spec['credit']})")
    return credits_map


def build_contact_sheet(ctx: ShortDayContext, item: Dict[str, Any]) -> Path:
    """Xuất bảng đối chứng hình ảnh QA tại qa/contact_scene_XX.jpg."""
    sc_id = item["id"]
    out_sheet = ctx.qa_dir / f"contact_scene_{sc_id:02d}.jpg"
    imgs = item["images"]
    cols = 4
    rows = (len(imgs) + cols - 1) // cols
    cell_w, cell_h, header_h = 460, 340, 84
    canvas = Image.new("RGB", (cols * cell_w + 40, rows * cell_h + header_h + 20), (10, 14, 24))
    draw = ImageDraw.Draw(canvas)
    try:
        font_hdr = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 19)
        font_lbl = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
        font_cap = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    except Exception:
        font_hdr = font_sub = font_lbl = font_cap = ImageFont.load_default()

    draw.text((20, 14), f"QA CONTACT SHEET — TIN #{sc_id:02d}: {item['title']}", fill=(0, 229, 255), font=font_hdr)
    draw.text((20, 50), f"Tong so anh: {len(imgs)} | Nguon: {item['news_source']} | Voice: {item['voice_preset']}", fill=(190, 205, 225), font=font_sub)

    for idx, spec in enumerate(imgs):
        r, c = divmod(idx, cols)
        x0, y0 = 20 + c * cell_w + 10, header_h + r * cell_h + 8
        draw.rectangle([x0 - 2, y0 - 2, x0 + 440, y0 + 322], outline=(0, 180, 216), width=2, fill=(18, 24, 38))
        with Image.open(ctx.images_dir / spec["dest"]) as im:
            im_rgb = im.convert("RGB")
            orig_size = f"{im_rgb.width}x{im_rgb.height}"
            im_rgb.thumbnail((432, 240), Image.Resampling.LANCZOS)
            canvas.paste(im_rgb, (x0 + (436 - im_rgb.width) // 2, y0 + (244 - im_rgb.height) // 2))
        draw.text((x0 + 8, y0 + 250), f"{spec['dest']} ({orig_size})", fill=(0, 229, 255), font=font_lbl)
        draw.text((x0 + 8, y0 + 272), f"Nguon: {spec['credit']}", fill=(250, 204, 21), font=font_cap)
        desc = spec["desc"][:48] + ("..." if len(spec["desc"]) > 48 else "")
        draw.text((x0 + 8, y0 + 294), desc, fill=(220, 230, 245), font=font_cap)

    canvas.save(out_sheet, format="JPEG", quality=92)
    ok(f"Đã tạo bảng đối chứng QA: {out_sheet}")
    return out_sheet


def _synth_text_with_preset(ctx: ShortDayContext, model: Any, text: str, preset_key: str) -> AudioSegment:
    """Tổng hợp một đoạn văn bản theo preset giọng chỉ định và chuẩn hóa âm lượng giọng."""
    preset_info = load_voice_preset(preset_key)
    voice_name = preset_info["voice_id"]
    spd, pch, temp = preset_info["speed"], preset_info["pitch"], preset_info["temperature"]
    clean_text, _ = prepare(text)
    chunks = build_chunks_from_text(clean_text, max_words_per_chunk=60, inter_sentence_pause=0.25)
    seg = AudioSegment.empty()
    for ch in chunks:
        c_seg, _ = render_chunk_vitts(
            model, ch["text"], voice_name,
            temperature=temp, speed=spd, pitch=pch,
            cache_dir=ctx.cache_dir, use_cache=True, max_chars=768,
        )
        seg += trim_segment_silence(c_seg)
        pause_ms = int(round(ch.get("pause_after", 0.25) * 1000))
        if pause_ms > 0:
            seg += AudioSegment.silent(duration=pause_ms)
    return apply_voice_standard(seg)


def synthesize_item_audio(ctx: ShortDayContext, model: Any, item: Dict[str, Any]) -> Dict[str, Any]:
    """Sinh audio tiêu đề & audio đầy đủ chuẩn -16 LUFS giọng đọc trước khi hòa trộn BGM (hỗ trợ đa giọng theo đoạn)."""
    sc_id = item["id"]
    title_out = ctx.audio_title_dir / f"audio_title_{sc_id:02d}.wav"
    full_out = ctx.audio_dir / f"audio_{sc_id:02d}.wav"

    voice_segments = item.get("voice_segments")
    if voice_segments:
        first_preset = voice_segments[0]["voice_preset"]
        p_title = load_voice_preset(first_preset)
        step(f"Tin #{sc_id:02d} — Tổng hợp song giọng: tiêu đề & đoạn đầu [{p_title['voice_label']}]")
        clean_title, _ = prepare(item["title"])
        raw_title_seg, _ = render_chunk_vitts(
            model, clean_title, p_title["voice_id"],
            temperature=p_title["temperature"], speed=p_title["speed"], pitch=p_title["pitch"],
            cache_dir=ctx.cache_dir, use_cache=True, max_chars=768,
        )
        title_std = apply_voice_standard(trim_segment_silence(raw_title_seg))
        title_std.export(str(title_out), format="wav")

        summary_seg = AudioSegment.empty()
        for idx, vs in enumerate(voice_segments):
            vp = vs["voice_preset"]
            p_info = load_voice_preset(vp)
            step(f"Tin #{sc_id:02d} — Đoạn {idx + 1}/{len(voice_segments)} [{p_info['voice_label']}]")
            seg_std = _synth_text_with_preset(ctx, model, vs["text"], vp)
            if idx > 0:
                summary_seg += AudioSegment.silent(duration=350)
            summary_seg += seg_std

        (title_std + AudioSegment.silent(duration=350) + summary_seg).export(str(full_out), format="wav")
    else:
        preset_info = load_voice_preset(item["voice_preset"])
        voice_name = preset_info["voice_id"]
        spd, pch, temp = preset_info["speed"], preset_info["pitch"], preset_info["temperature"]
        step(f"Tin #{sc_id:02d} — Tổng hợp giọng: {preset_info['voice_label']} (spd={spd}, pch={pch}, temp={temp})")

        clean_title, _ = prepare(item["title"])
        raw_title_seg, _ = render_chunk_vitts(
            model, clean_title, voice_name,
            temperature=temp, speed=spd, pitch=pch,
            cache_dir=ctx.cache_dir, use_cache=True, max_chars=768,
        )
        raw_title_seg = trim_segment_silence(raw_title_seg)
        apply_voice_standard(raw_title_seg).export(str(title_out), format="wav")

        clean_summary, _ = prepare(item["summary"])
        chunks = build_chunks_from_text(clean_summary, max_words_per_chunk=60, inter_sentence_pause=0.25)
        summary_seg = AudioSegment.empty()
        for ch in chunks:
            c_seg, _ = render_chunk_vitts(
                model, ch["text"], voice_name,
                temperature=temp, speed=spd, pitch=pch,
                cache_dir=ctx.cache_dir, use_cache=True, max_chars=768,
            )
            summary_seg += trim_segment_silence(c_seg)
            pause_ms = int(round(ch.get("pause_after", 0.25) * 1000))
            if pause_ms > 0:
                summary_seg += AudioSegment.silent(duration=pause_ms)

        apply_voice_standard(raw_title_seg + AudioSegment.silent(duration=350) + summary_seg).export(str(full_out), format="wav")

    dur_sec = round(AudioSegment.from_wav(str(full_out)).duration_seconds, 2)
    title_dur = round(AudioSegment.from_wav(str(title_out)).duration_seconds, 2)
    ok(f"Audio Tin #{sc_id:02d} hoàn tất: full={dur_sec}s, title={title_dur}s -> {full_out.name}")
    return {"audio_path": str(full_out), "audio_title": str(title_out), "duration": dur_sec}


def merge_day_metadata(ctx: ShortDayContext, items: List[Dict[str, Any]], new_credits: Dict[str, str], audio_meta: Dict[int, Dict[str, Any]]) -> None:
    """Cập nhật image_credits.json, image_plan.json và thethao.json cho danh sách items."""
    target_ids = {int(it["id"]) for it in items}

    credits_path = ctx.day_dir / "image_credits.json"
    existing_credits = json.loads(credits_path.read_text(encoding="utf-8")) if credits_path.exists() else {}
    existing_credits.update(new_credits)
    credits_path.write_text(json.dumps(existing_credits, ensure_ascii=False, indent=2), encoding="utf-8")

    plan_path = ctx.day_dir / "image_plan.json"
    existing_records = json.loads(plan_path.read_text(encoding="utf-8")).get("records", []) if plan_path.exists() else []
    kept_records = [r for r in existing_records if int(r.get("scene_id", 0)) not in target_ids]
    for item in items:
        sc_id = item["id"]
        spec_by_dest = {sp["dest"]: sp for sp in item["images"]}
        for slot_type, sent_idx, fname in item["plan_slots"]:
            sp = spec_by_dest[fname]
            kept_records.append({
                "scene_id": sc_id,
                "type": slot_type,
                "index": 1 if slot_type == "title" else sent_idx,
                "sentence_idx": 0 if slot_type == "title" else sent_idx,
                "file_name": fname,
                "credit": sp["credit"],
                "description": sp["desc"],
            })
    plan_path.write_text(json.dumps({"records": kept_records}, ensure_ascii=False, indent=2), encoding="utf-8")

    tt_path = ctx.day_dir / "thethao.json"
    existing_tt = json.loads(tt_path.read_text(encoding="utf-8")) if tt_path.exists() else []
    kept_tt = []
    seen = set()
    for row in existing_tt:
        rid = int(row.get("id", 0))
        if rid in target_ids or rid in seen:
            continue
        seen.add(rid)
        kept_tt.append(row)

    for item in items:
        sc_id = item["id"]
        am = audio_meta[sc_id]
        entry: Dict[str, Any] = {
            "id": sc_id,
            "slug": item["slug"],
            "group": item["group"],
            "title": item["title"],
            "summary": item["summary"],
            "source": item["source"],
            "news_source": item["news_source"],
            "credit": item["credit"],
            "hide_date_chip": item.get("hide_date_chip", True),
            "audio_path": am["audio_path"],
            "audio_title": am["audio_title"],
            "duration": am["duration"],
        }
        if item.get("sentence_charts"):
            entry["sentence_charts"] = item["sentence_charts"]
        if item.get("hook"):
            entry["hook"] = item["hook"]
        for idx, sp in enumerate(item["images"], start=1):
            entry[f"image_{idx}"] = str(ctx.images_dir / sp["dest"])
        entry["image_path"] = entry["image_1"]
        kept_tt.append(entry)

    tt_path.write_text(json.dumps(kept_tt, ensure_ascii=False, indent=2), encoding="utf-8")
    ok("Đã ghi/cập nhật image_credits.json, image_plan.json và thethao.json.")


def trim_video_audio_drift(ctx: ShortDayContext, mp4_path: Path, item_id: int) -> None:
    """Căn chỉnh độ dài luồng audio khớp video stream (drift <= 1 frame 30fps)."""
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=duration,codec_type", "-of", "json", str(mp4_path)],
        capture_output=True, text=True, check=True,
    )
    streams = json.loads(probe.stdout).get("streams", [])
    v_dur = next(float(s["duration"]) for s in streams if s.get("codec_type") == "video")
    a_dur = next(float(s["duration"]) for s in streams if s.get("codec_type") == "audio")
    if abs(v_dur - a_dur) <= 0.025:
        return
    tmp_sync = Path(ctx.work_shorts_dir) / f"short_{item_id}_sync.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4_path), "-t", f"{v_dur:.6f}", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", str(tmp_sync)],
        check=True,
    )
    shutil.copy2(str(tmp_sync), str(mp4_path))


def build_and_publish_short(ctx: ShortDayContext, item: Dict[str, Any]) -> None:
    """Export timeline bridge, render HTML v2, kiểm toán âm thanh, xuất Thumbnail & _mota.txt."""
    sc_id, slug = item["id"], item["slug"]
    banner(f"RENDER & XUẤT BẢN TIN #{sc_id:02d}: {slug}")

    work_proj_dir = os.path.join(ctx.work_shorts_dir, f"short_{sc_id}")
    if os.path.exists(work_proj_dir):
        shutil.move(work_proj_dir, os.path.join(Path.home(), ".Trash", f"{ctx.work_tag}_s{sc_id}_{os.getpid()}"))

    pdir, _, _ = export_bridge_project(
        day_dir=str(ctx.day_dir),
        item_id=str(sc_id),
        format_type="short",
        work_proj_dir=work_proj_dir,
        global_offset_sec=0.0,
    )

    out_work_mp4 = render_html_engine(
        project_dir=str(pdir),
        template="short_news_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True,
    )
    if not out_work_mp4 or not os.path.exists(out_work_mp4):
        die(f"Render HTML engine thất bại cho Tin #{sc_id:02d}")

    out_mp4 = ctx.shorts_dir / f"{slug}.mp4"
    shutil.copy2(out_work_mp4, str(out_mp4))
    trim_video_audio_drift(ctx, out_mp4, sc_id)

    if item.get("include_outro", True):
        append_short_outro(
            out_mp4,
            voice_hint=item.get("voice_preset"),
        )
        trim_video_audio_drift(ctx, out_mp4, sc_id)

    loud = measure_loudness(str(out_mp4))
    if loud:
        ok(f"Xuất MP4 thành công: {out_mp4.name} | I={loud['input_i']} LUFS | TP={loud['input_tp']} dBTP")
    chk = subprocess.run(["python3", "-B", str(ROOT_DIR / "core" / "audio_check.py"), str(out_mp4)], check=False)
    if chk.returncode != 0:
        warn(f"audio_check trả về mã {chk.returncode} cho {out_mp4.name}")

    mota_path = ctx.shorts_dir / f"{slug}_mota.txt"
    write_mota_9x16(
        out_path=mota_path,
        seo_title=item["seo_title"],
        description_paragraphs=item["description"],
        chapters=None,
        sources_line=item["news_source"],
        hashtags=item["hashtags"],
    )
    ok(f"Đã tạo mô tả SEO: {mota_path.name}")

    t_cfg = item["thumb"]
    thumb_path = ctx.shorts_dir / f"{slug}_thumbnail.jpg"
    render_thumbnail_9x16(
        out_path=thumb_path,
        image_path=ctx.images_dir / t_cfg["image"],
        kicker=t_cfg["kicker"],
        hero_html=t_cfg["hero_html"],
        subtitle=t_cfg["subtitle"],
        badge=t_cfg["badge"],
        tag_a=t_cfg["tag_a"],
        tag_b=t_cfg["tag_b"],
        obj_pos=t_cfg["obj_pos"],
    )
    ok(f"Đã tạo Thumbnail 9:16: {thumb_path.name}")


def run_short_batch(ctx: ShortDayContext, items: List[Dict[str, Any]], title_banner: str, cloud: Optional[bool] = None) -> None:
    """
    Chạy toàn bộ pipeline dựng danh sách video Shorts độc lập trong 1 ngày.
    - Bước nhẹ (kiểm tra & nạp ảnh, xuất Contact Sheet QA) luôn chạy trực tiếp trên máy Mac.
    - Bước nặng (ViTTS v3turbo + Render HTML v2 + Thumbnail) ưu tiên đẩy lên GitHub Actions Matrix
      khi `cloud=True` hoặc có cờ `--cloud` / `DD_USE_CLOUD=1`, và tự động fallback về máy Mac nếu dùng `--local`.
    """
    banner(title_banner)
    ctx.ensure_dirs()

    all_credits: Dict[str, str] = {}
    for item in items:
        all_credits.update(copy_and_verify_images(ctx, item))
        build_contact_sheet(ctx, item)

    # Xác định chế độ chạy Cloud hay Local (mặc định giữ tương thích 100%, bật Cloud khi truyền --cloud hoặc DD_USE_CLOUD=1)
    if cloud is None:
        if "--local" in sys.argv:
            use_cloud = False
        elif "--cloud" in sys.argv or os.environ.get("DD_USE_CLOUD", "0") == "1":
            use_cloud = True
        else:
            use_cloud = False
    else:
        use_cloud = bool(cloud)

    # Luôn lưu shorts_spec.json chuẩn hóa trong day_dir để có thể đẩy lên GitHub Cloud bất cứ lúc nào
    spec_out = ctx.day_dir / "shorts_spec.json"
    spec_out.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    if use_cloud:
        step(f"Chuyển giao {len(items)} Video Shorts lên GitHub Cloud Matrix (0% tải máy Mac)...")
        is_orther = "Orther" in ctx.day_dir.parts
        cmd = [
            sys.executable, "-B", str(ROOT_DIR / "core" / "cloud_runner.py"),
            "--day", ctx.day_dir.name,
            "--mode", "short_batch",
            "--shards", str(max(1, min(10, len(items)))),
        ]
        if is_orther:
            cmd.append("--orther")
        res = subprocess.run(cmd)
        if res.returncode == 0:
            banner(f"HOÀN TẤT XUẤT BẢN ĐÁM MÂY {len(items)} VIDEO SHORTS ({ctx.day_dir.name})")
            return
        warn("Cloud Render gặp sự cố, tự động chuyển về chạy trực tiếp trên máy Mac (Local Fallback)...")

    step("Khởi tạo Vieneu v3turbo TTS engine (Local)...")
    from vieneu import Vieneu
    tts_model = Vieneu(mode="v3turbo")

    audio_meta: Dict[int, Dict[str, Any]] = {}
    for item in items:
        audio_meta[item["id"]] = synthesize_item_audio(ctx, tts_model, item)

    merge_day_metadata(ctx, items, all_credits, audio_meta)

    for item in items:
        build_and_publish_short(ctx, item)

    banner(f"HOÀN TẤT XUẤT BẢN {len(items)} VIDEO SHORTS ({ctx.day_dir.name})")
