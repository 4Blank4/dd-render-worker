#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_digest_19_11.py — Sản xuất Video Short "Bản Tin Nhanh 18 Tin" Ngày 19.11.2026
======================================================================================
- Viết mới 100% lời thoại tin nhanh cô đọng (không dùng lại câu/audio của bản tin dài).
- Phân giọng theo khu vực:
    + Việt Nam (01..06, 14, 16, 17): Giọng Nữ Ngọc Huyền (Mẫu 14).
    + Quốc tế (07..13, 15, 18): Giọng Nam chính Minh Quân Pro (Mẫu 15).
- Tuyển chọn 1 ảnh ngang HD sắc nét nhất cho mỗi tin từ kho đã QA & xuất bảng đối chứng QA.
- Ràng buộc cứng tổng thời lượng < 180.0 giây (< 3 phút) BAO GỒM LUÔN Outro 9:16.
- Render 9:16 (1080x1920 @ 30fps) qua templates/short_digest_v2.html, ghép Outro Nữ qua short_outro.py,
  xuất kèm Thumbnail 9:16 & file mô tả SEO _mota.txt (tuyệt đối không dùng từ ngữ máy móc/hậu trường).
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List

from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
if os.path.join(_HERE, "vendor") not in sys.path:
    sys.path.insert(0, os.path.join(_HERE, "vendor"))
engines_html = os.path.join(_ROOT, "engines", "html")
if engines_html not in sys.path:
    sys.path.insert(0, engines_html)

from diemdoc import paths
from diemdoc.audio import apply_voice_standard, measure_loudness
from diemdoc.log import banner, die, log, ok, step
from diemdoc.publisher import load_voice_preset, render_thumbnail_9x16, write_mota_9x16
from diemdoc.short_outro import append_short_outro
from diemdoc.tts_text import prepare
from m3_voice import render_chunk_vitts, trim_segment_silence
from m8_news_bridge import compute_pan_params, interpolate_sentence_words
from renderer import render_html_engine
from vieneu import Vieneu

DAY_STR = "19.11.2026"
ROOT = Path(_ROOT)
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
QA_DIR = DAY_DIR / "qa"
SHORTS_DIR = DAY_DIR / "shorts"
DIGEST_AUDIO_DIR = SHORTS_DIR / "digest_audio"
WORK_DIR = Path(paths.WORK) / "digest_short_19_11"
TTS_CACHE_DIR = Path(paths.WORK) / "tts_cache_digest_19_11"

OUT_VIDEO_NAME = "Short_Tin_Nhanh_18_Tin.mp4"
OUT_THUMB_NAME = "Short_Tin_Nhanh_18_Tin_thumbnail.jpg"
OUT_MOTA_NAME = "Short_Tin_Nhanh_18_Tin_mota.txt"
OUT_SCRIPT_NAME = "digest_script_19_11.json"

MAX_TOTAL_SEC_WITH_OUTRO = 179.0
GAP_MS = 220

# Kịch bản tin nhanh 18 tin viết mới hoàn toàn, phân vùng Việt Nam (Nữ) / Quốc tế (Nam)
DIGEST_SPECS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_01_1.jpg",
        "title": "Đình Bắc đa chấn thương đầu gối, nghỉ hết năm 2026",
        "digest_line": "Chân sút Nguyễn Đình Bắc rách bán phần dây chằng gối phải sau trận thứ 48 trong năm, buộc phải nghỉ thi đấu hết năm 2026.",
    },
    {
        "id": 2,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_02_1.jpg",
        "title": "Tuyển Việt Nam chốt hạng 99 FIFA, giữ nhóm hạt giống số 2",
        "digest_line": "Bị trừ 5,3 điểm sau trận thua Kyrgyzstan, tuyển Việt Nam chốt năm 2026 ở hạng 99 FIFA nhưng vẫn giữ hạt giống số 2 World Cup 2030.",
    },
    {
        "id": 3,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_03_1.jpg",
        "title": "Công an TP.HCM hạ gục ĐKVĐ Buriram United 1-0 tại Shopee Cup",
        "digest_line": "Nhờ siêu phẩm phút 88 của Quốc Cường và màn cản phá xuất thần từ Lê Giang Patrik, Công an TP.HCM hạ gục Buriram United 1-0.",
    },
    {
        "id": 4,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_04_1.jpg",
        "title": "Công an Hà Nội quyết chiến Johor Darul Ta'zim tại Hàng Đẫy",
        "digest_line": "Tối nay tại Hàng Đẫy, Công an Hà Nội đại chiến Johor Darul Ta'zim ở bảng B Shopee Cup dù thiếu vắng cả Đình Bắc lẫn Quang Hải.",
    },
    {
        "id": 5,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_05_1.jpg",
        "title": "FIFA U17 World Cup 2026 khai mạc hôm nay tại Qatar",
        "digest_line": "FIFA U17 World Cup 2026 khai mạc hôm nay tại Qatar, nơi HLV Cristiano Roland lần đầu được quyền yêu cầu trọng tài xem lại video FVS.",
    },
    {
        "id": 6,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_06_1.jpg",
        "title": "U17 Bỉ mất 4 trụ cột Anderlecht trước ngày gặp U17 Việt Nam",
        "digest_line": "Ngay trước trận ra quân gặp U17 Việt Nam tối mai, á quân châu Âu U17 Bỉ mất liền bốn cầu thủ chủ chốt vì Anderlecht từ chối nhả quân.",
    },
    {
        "id": 7,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_07_1.jpg",
        "title": "Lionel Messi cắt đứt liên hệ và dọa kiện Liên đoàn Argentina",
        "digest_line": "Rạn nứt đỉnh điểm vì bị tự ý khai thác hình ảnh cho hãng bia, Lionel Messi đã thuê luật sư yêu cầu AFA ngừng sử dụng tên tuổi của anh.",
    },
    {
        "id": 8,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_08_1.jpg",
        "title": "Ronaldo vắng đề cử Globe Soccer Awards 2026",
        "digest_line": "Cristiano Ronaldo vắng mặt ở hạng mục Cầu thủ xuất sắc nhất Globe Soccer Awards 2026, còn Bồ Đào Nha đã thủng lưới sáu bàn sau hai trận vắng anh.",
    },
    {
        "id": 9,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_09_1.jpg",
        "title": "Pochettino làm việc tại Carrington, thay 5 trợ lý Man Utd",
        "digest_line": "Tân HLV Mauricio Pochettino chính thức làm việc tại Carrington với hợp đồng đến năm 2029, thay năm trợ lý và siết kỷ luật trước trận gặp Liverpool.",
    },
    {
        "id": 10,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_10_1.jpg",
        "title": "UEFA chỉ định Philippe Diallo thách thức Gianni Infantino",
        "digest_line": "Chủ tịch UEFA Aleksander Ceferin chọn người đứng đầu bóng đá Pháp Philippe Diallo ra tranh cử, đối đầu trực diện Gianni Infantino ở ghế Chủ tịch FIFA.",
    },
    {
        "id": 11,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_11_2.jpg",
        "title": "Haaland chạm mốc 399 bàn thắng ở tuổi 26",
        "digest_line": "Erling Haaland đã ghi 399 bàn thắng ở tuổi 26, bỏ xa kỷ lục 234 bàn của Ronaldo cùng độ tuổi và vượt Mbappé ở cấp độ đội tuyển quốc gia.",
    },
    {
        "id": 12,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_12_1.jpg",
        "title": "Arsenal ba lần chịu phạt đền oan; Ancelotti đáp trả Romario",
        "digest_line": "Hội đồng KMI xác nhận Arsenal ba lần chịu oan sai phạt đền sau 10 vòng Ngoại hạng Anh, còn HLV Carlo Ancelotti đáp trả gay gắt huyền thoại Romario.",
    },
    {
        "id": 13,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_13_1.jpg",
        "title": "Bóng đá Indonesia nội loạn, gửi đơn khiếu nại lên FIFA",
        "digest_line": "Bóng đá Indonesia dậy sóng khi Chủ tịch Liên đoàn Futsal bị bãi nhiệm đã gửi đơn tố cáo Chủ tịch PSSI Erick Thohir thẳng tới FIFA và AFC.",
    },
    {
        "id": 14,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_14_1.jpg",
        "title": "Lê Quang Liêm tranh hạng 7 thế giới gặp Ian Nepomniachtchi",
        "digest_line": "Thua Hans Niemann ở bán kết nhánh dưới giải vô địch cờ vua toàn năng 2026, Lê Quang Liêm bước vào trận tranh hạng bảy gặp Ian Nepomniachtchi.",
    },
    {
        "id": 15,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_15_1.jpg",
        "title": "Carlos Alcaraz thắng áp đảo Daniil Medvedev tại ATP Finals",
        "digest_line": "Carlos Alcaraz chỉ mất 72 phút để hạ Daniil Medvedev 6-2, 6-4 tại Turin, nối dài mạch 11 trận thắng liên tiếp trên sân cứng trong nhà.",
    },
    {
        "id": 16,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_16_1.jpg",
        "title": "Nữ võ sĩ Vovinam Kim Lụa đoạt HCV kiếm tiền chữa bệnh cho em",
        "digest_line": "Võ sĩ Vovinam Nguyễn Thị Kim Lụa xúc động giành HCV Đại hội Thể thao toàn quốc để có chi phí phẫu thuật thay khớp háng cho cô em gái.",
    },
    {
        "id": 17,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_17_1.jpg",
        "title": "Tuyển bóng bàn Việt Nam thưởng 400 triệu đồng; Quyết Chiến vắng mặt",
        "digest_line": "Tuyển bóng bàn Việt Nam nhận thưởng nóng 400 triệu đồng sau năm huy chương Đông Nam Á, còn Trần Quyết Chiến bất ngờ vắng Đại hội toàn quốc.",
    },
    {
        "id": 18,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_18_1.jpg",
        "title": "Tay vợt gốc Việt lập địa chấn cầu lông; Thompson chia tay UFC",
        "digest_line": "Tay vợt Mỹ gốc Việt Allison Quynh Lee loại hạt giống số 7 tại Hong Kong Open, còn huyền thoại Stephen Thompson chia tay UFC bằng cú đá knock-out.",
    },
]


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for cand in (
        ROOT / "assets" / "fonts" / "Be_Vietnam_Pro" / "BeVietnamPro-Bold.ttf",
        ROOT / "assets" / "fonts" / "Be_Vietnam_Pro" / "BeVietnamPro-SemiBold.ttf",
    ):
        if cand.exists():
            return ImageFont.truetype(str(cand), size=size)
    return ImageFont.load_default()


def build_digest_contact_sheet(records: List[Dict[str, Any]], out_path: Path) -> None:
    """Tạo bảng đối chứng 18 ảnh đã chọn cho Digest Short (lưu trong outputs/19.11.2026/qa/)."""
    cols = 4
    rows = (len(records) + cols - 1) // cols
    cell_w, cell_h = 460, 340
    thumb_w, thumb_h = 432, 238
    margin = 20
    header_h = 72
    canvas_w = cols * cell_w + margin * 2
    canvas_h = rows * cell_h + margin * 2 + header_h

    sheet = Image.new("RGB", (canvas_w, canvas_h), (8, 13, 24))
    draw = ImageDraw.Draw(sheet)
    f_hdr = _load_font(26)
    f_lbl = _load_font(16)
    f_sub = _load_font(13)

    draw.text(
        (margin, 22),
        f"KIỂM DUYỆT 18 ẢNH DIGEST SHORT ({DAY_STR}) — VIỆT NAM: NỮ | QUỐC TẾ: NAM",
        fill=(0, 229, 255),
        font=f_hdr,
    )

    for idx, rec in enumerate(records):
        r, c = divmod(idx, cols)
        x0 = margin + c * cell_w
        y0 = header_h + margin + r * cell_h
        img_p = Path(rec["image"])
        with Image.open(img_p) as im:
            iw, ih = im.size
            im_rgb = im.convert("RGB")
            im_rgb.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            tw, th = im_rgb.size
            px = x0 + 14 + (thumb_w - tw) // 2
            py = y0 + 6 + (thumb_h - th) // 2
            sheet.paste(im_rgb, (px, py))

        tag_color = (56, 189, 248) if rec["voice_gender"] == "Nam" else (244, 114, 182)
        draw.rectangle([x0 + 10, y0 + 4, x0 + cell_w - 10, y0 + thumb_h + 8], outline=tag_color, width=2)
        draw.text(
            (x0 + 12, y0 + thumb_h + 14),
            f"[{int(rec['id']):02d}] {rec['region']} ({rec['voice_gender']}) · {img_p.name} ({iw}x{ih})",
            fill=tag_color,
            font=f_lbl,
        )
        draw.text(
            (x0 + 12, y0 + thumb_h + 38),
            f"📷 {rec['credit']} | {rec['digest_line'][:44]}...",
            fill=(226, 232, 240),
            font=f_sub,
        )
        draw.text(
            (x0 + 12, y0 + thumb_h + 58),
            f"📰 {rec['news_source']}",
            fill=(148, 163, 184),
            font=f_sub,
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(str(out_path), quality=92)
    ok(f"Đã xuất bảng đối chứng QA Digest: {paths.rel_to_root(str(out_path))}")


def _probe_stream_duration(mp4_path: Path, selector: str = "v:0") -> float:
    res = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            selector,
            "-show_entries",
            "stream=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(mp4_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(res.stdout.strip().splitlines()[0])


def main() -> None:
    parser = argparse.ArgumentParser(description=f"Dựng Video Short Bản Tin Nhanh 18 Tin (<3p gồm Outro) — {DAY_STR}")
    parser.add_argument("--prep-only", action="store_true", help="Chỉ sinh script, QA ảnh và giọng đọc (chưa render video)")
    parser.add_argument("--force-tts", action="store_true", help="Sinh lại toàn bộ giọng đọc mới bỏ qua cache")
    args = parser.parse_args()

    for d in (WORK_DIR, TTS_CACHE_DIR, SHORTS_DIR, DIGEST_AUDIO_DIR, QA_DIR):
        d.mkdir(parents=True, exist_ok=True)

    thethao_items = {int(it["id"]): it for it in json.loads((DAY_DIR / "thethao.json").read_text(encoding="utf-8"))}
    credits_map = json.loads((DAY_DIR / "image_credits.json").read_text(encoding="utf-8"))

    male_preset = load_voice_preset("primary")
    female_preset = load_voice_preset("secondary")
    total_items = len(DIGEST_SPECS)

    banner(
        f"SẢN XUẤT BẢN TIN NHANH {total_items} TIN (< 3 PHÚT GỒM OUTRO) — {DAY_STR}",
        f"Việt Nam: {female_preset['voice_label']} | Quốc tế: {male_preset['voice_label']}",
    )

    if args.force_tts and TTS_CACHE_DIR.exists():
        shutil.rmtree(TTS_CACHE_DIR, ignore_errors=True)
        TTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    step(f"1. Kiểm tra {total_items} ảnh chọn lọc và tổng hợp giọng đọc ViTTS v3turbo...")
    model = Vieneu(mode="v3turbo")

    gap_seg = AudioSegment.silent(duration=GAP_MS, frame_rate=44100).set_channels(2)
    combined_voice = AudioSegment.silent(duration=0, frame_rate=44100).set_channels(2)

    items_data: List[Dict[str, Any]] = []
    script_export: List[Dict[str, Any]] = []
    all_words: List[Dict[str, Any]] = []
    all_karaoke: List[Dict[str, Any]] = []
    raw_sfx: List[Dict[str, Any]] = []
    cum_sec = 0.0

    for idx, spec in enumerate(DIGEST_SPECS, 1):
        sc_id = int(spec["id"])
        orig_item = thethao_items[sc_id]
        img_path = IMAGES_DIR / spec["image_file"]
        if not img_path.exists():
            die(f"Thiếu ảnh cho tin #{sc_id:02d}: {img_path}")

        preset = male_preset if spec["voice_preset"] == "primary" else female_preset
        digest_text = spec["digest_line"].strip()
        tts_str, _ = prepare(digest_text)

        wav_out = DIGEST_AUDIO_DIR / f"tin_{sc_id:02d}.wav"
        seg, _ = render_chunk_vitts(
            model,
            tts_str,
            preset["voice_id"],
            temperature=preset["temperature"],
            speed=preset["speed"],
            pitch=preset["pitch"],
            cache_dir=str(TTS_CACHE_DIR),
            use_cache=(not args.force_tts),
            max_chars=768,
        )
        seg = trim_segment_silence(seg).set_frame_rate(44100).set_channels(2)
        seg = apply_voice_standard(seg)
        seg.export(str(wav_out), format="wav")
        it_dur = round(len(seg) / 1000.0, 3)

        if idx > 1:
            combined_voice += gap_seg
            cum_sec += GAP_MS / 1000.0
            raw_sfx.append({
                "sfx": "whoosh_cinematic_short.mp3",
                "time": round(cum_sec, 3),
                "volume": 0.20,
            })

        it_start = round(cum_sec, 3)
        combined_voice += seg
        cum_sec += len(seg) / 1000.0
        it_end = round(cum_sec, 3)

        s_words = interpolate_sentence_words(digest_text, 0.0, it_dur)
        abs_words: List[Dict[str, Any]] = []
        for w in s_words:
            aw = {
                "word": w["word"],
                "start": round(it_start + w["start"], 3),
                "end": round(it_start + w["end"], 3),
                "matched": True,
            }
            abs_words.append(aw)
            all_words.append(aw)

        for ci in range(0, len(abs_words), 4):
            c_words = abs_words[ci : ci + 4]
            all_karaoke.append({
                "start": c_words[0]["start"],
                "end": c_words[-1]["end"],
                "text": " ".join(cw["word"] for cw in c_words),
                "words": c_words,
            })

        pan_info = compute_pan_params(str(img_path), duration=it_dur, dir_toggle=(idx % 2 == 1))
        photo_credit = credits_map.get(spec["image_file"]) or orig_item.get("credit", "REUTERS")
        news_source = orig_item.get("news_source") or orig_item.get("source") or "VNEXPRESS"

        item_rec: Dict[str, Any] = {
            "id": str(sc_id),
            "title": spec["title"],
            "digest_line": digest_text,
            "region": spec["region"],
            "voice_gender": spec["voice_gender"],
            "voice_label": preset["voice_label"],
            "image": str(img_path),
            "credit": photo_credit,
            "news_source": news_source,
            "start": it_start,
            "end": it_end,
            "duration": it_dur,
            **pan_info,
        }
        items_data.append(item_rec)
        script_export.append({
            "id": sc_id,
            "region": spec["region"],
            "voice_gender": spec["voice_gender"],
            "voice_label": preset["voice_label"],
            "title": spec["title"],
            "digest_line": digest_text,
            "word_count": len(digest_text.split()),
            "image_file": spec["image_file"],
            "credit": photo_credit,
            "news_source": news_source,
            "audio_wav": paths.rel_to_root(str(wav_out)),
            "start": it_start,
            "duration": it_dur,
        })
        log(f"  [{idx:02d}/{total_items}] ({spec['region']} | {spec['voice_gender']}) {it_dur:.2f}s | {spec['title']}")

    voiceover_wav = WORK_DIR / "voiceover.wav"
    combined_voice.export(str(voiceover_wav), format="wav")
    body_dur = round(len(combined_voice) / 1000.0, 3)

    # Tin 18 (cuối) là giọng Nam ("primary") nên Outro tự chọn đối xứng giọng Nữ (~5.4-6.5s)
    max_expected_with_outro = body_dur + 6.55
    ok(f"Thời lượng phần thân {total_items} tin: {body_dur:.2f}s | Dự kiến cả Outro: <= {max_expected_with_outro:.2f}s (Ngưỡng < 180.00s)")
    if max_expected_with_outro >= MAX_TOTAL_SEC_WITH_OUTRO:
        die(f"Vượt trần thời lượng cho phép ({max_expected_with_outro:.2f}s >= 180.0s)! Hãy rút gọn thoại.")

    build_digest_contact_sheet(items_data, QA_DIR / "contact_digest_19_11.jpg")
    (SHORTS_DIR / OUT_SCRIPT_NAME).write_text(
        json.dumps(
            {
                "day": DAY_STR,
                "total_items": len(items_data),
                "body_duration_sec": body_dur,
                "estimated_with_outro_sec": round(max_expected_with_outro, 2),
                "items": script_export,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    ok(f"Đã lưu kịch bản Digest JSON: {paths.rel_to_root(str(SHORTS_DIR / OUT_SCRIPT_NAME))}")

    if args.prep_only:
        ok("Hoàn tất chế độ --prep-only.")
        return

    fx_cfg: Dict[str, Any] = {}
    fx_path = Path(paths.CONFIG) / "fx.json"
    if fx_path.exists():
        fx_cfg = json.loads(fx_path.read_text(encoding="utf-8"))

    timeline = {
        "title": "TIN NHANH THỂ THAO 19.11",
        "channel_name": "ĐIỂM ĐỌC",
        "date_str": "THỨ NĂM · 19.11.2026",
        "date_chip": "THỨ NĂM · 19.11.2026",
        "hide_date_chip": False,
        "total_duration": body_dur,
        "format": "short",
        "template": "short_digest_v2.html",
        "dimensions": [1080, 1920],
        "fps": 30,
        "bgm": "bgm_editorial_2_momentum.mp3",
        "bgm_volume": 0.06,
        "audio_path": str(voiceover_wav),
        "global_offset_sec": 0.0,
        "fx": fx_cfg,
        "sfx_events": raw_sfx,
        "items": items_data,
        "karaoke_chunks": all_karaoke,
    }
    words_data = {"words": all_words, "karaoke_chunks": all_karaoke}

    (WORK_DIR / "video_timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    (WORK_DIR / "word_timestamps.json").write_text(json.dumps(words_data, ensure_ascii=False, indent=2), encoding="utf-8")

    step("2. Render video 9:16 qua templates/short_digest_v2.html...")
    rendered_body = render_html_engine(
        project_dir=str(WORK_DIR),
        template="short_digest_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        use_cache=False,
        force=True,
    )
    if not rendered_body or not os.path.exists(rendered_body):
        die("Render HTML v2 thất bại cho Digest Short!")

    out_video = SHORTS_DIR / OUT_VIDEO_NAME
    final_path, chosen_outro = append_short_outro(
        rendered_body,
        voice_hint="primary",
        out_path=out_video,
        seed="digest_19_11_v1",
        enabled=True,
    )

    v_dur = _probe_stream_duration(final_path, "v:0")
    a_dur = _probe_stream_duration(final_path, "a:0")
    drift_ms = abs(v_dur - a_dur) * 1000.0
    stats = measure_loudness(str(final_path))

    if v_dur >= 180.0:
        die(f"Video sau Outro dài {v_dur:.2f}s >= 180.0s (vi phạm trần < 3 phút)!")
    if drift_ms > 33.3:
        die(f"Lệch A/V vượt ngưỡng 33.3ms: {drift_ms:.2f}ms")

    thumb_path = SHORTS_DIR / OUT_THUMB_NAME
    render_thumbnail_9x16(
        out_path=thumb_path,
        image_path=IMAGES_DIR / "Tin_01_1.jpg",
        kicker="ĐIỂM NHANH 18 TIN THỂ THAO 19.11",
        hero_html='<span class="hl-cyan">18 TIN NHANH!</span><br><span class="hl-white">ĐÌNH BẮC HẾT NĂM</span><br><span class="hl-yellow">MESSI DỌA KIỆN AFA!</span>',
        subtitle="SHOPEE CUP • U17 WORLD CUP • NGOẠI HẠNG ANH • ATP FINALS",
        badge="18 TIN NHANH",
        tag_a="VN & QUỐC TẾ",
        tag_b=DAY_STR,
        obj_pos="62% 20%",
    )

    chapters_list = []
    for it in items_data:
        sec_i = int(it["start"])
        m, s = divmod(sec_i, 60)
        chapters_list.append((f"{m:02d}:{s:02d}", it["title"]))

    mota_path = SHORTS_DIR / OUT_MOTA_NAME
    write_mota_9x16(
        out_path=mota_path,
        seo_title="Tin nhanh 19/11: Đình Bắc nghỉ hết năm, Công an TP.HCM hạ Buriram, Messi dọa kiện AFA #Shorts",
        description_paragraphs=[
            "Điểm đọc nhanh 18 tin tức thể thao nóng nhất ngày 19/11/2026 từ sân cỏ Việt Nam tới các đấu trường quốc tế, cờ vua, quần vợt và võ thuật.",
            "Cập nhật chấn thương của Nguyễn Đình Bắc, chiến thắng 1-0 của Công an TP.HCM trước Buriram United, ngày khai mạc FIFA U17 World Cup 2026, mâu thuẫn giữa Lionel Messi với AFA, Mauricio Pochettino ra mắt Man Utd và bước tiến của Erling Haaland.",
        ],
        chapters=chapters_list,
        sources_line="📰 Nguồn tin: VnExpress, Thanh Niên, Tuổi Trẻ, Dân Trí, Reuters, AP, FIFA, UEFA, ATP Tour, FIDE.",
        hashtags=["#Shorts", "#TinNhanh", "#DiemDoc", "#DiemDocTheThao", "#NguyenDinhBac", "#CongAnTPHCM", "#U17WorldCup", "#LionelMessi", "#ManUtd", "#Haaland"],
    )

    ok("=" * 72)
    ok(f"HOÀN TẤT DIGEST SHORT {total_items} TIN -> {paths.rel_to_root(str(final_path))}")
    ok(f"Thời lượng: Video={v_dur:.2f}s (Audio={a_dur:.2f}s, Drift={drift_ms:.2f}ms) | Outro: {chosen_outro.name if chosen_outro else 'None'}")
    if stats:
        ok(f"Âm lượng: I={stats.get('input_i')} LUFS | TP={stats.get('input_tp')} dBTP")
    ok("=" * 72)


if __name__ == "__main__":
    main()
