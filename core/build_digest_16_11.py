#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_digest_16_11.py — Sản xuất Video Short "Bản Tin Nhanh 26 Tin" Tuần 16.11.2026
======================================================================================
- Viết mới 100% lời thoại tin nhanh cô đọng (không dùng lại câu/audio của bản tin dài).
- Phân giọng theo khu vực:
    + Tin Quốc tế (01..14, 25..26): Giọng Nam chính Minh Quân Pro (Mẫu 15).
    + Tin Việt Nam (15..24): Giọng Nữ Ngọc Huyền (Mẫu 14).
- Tuyển chọn 1 ảnh ngang HD sắc nét nhất cho mỗi tin từ kho đã QA & xuất bảng đối chứng QA.
- Ràng buộc cứng tổng thời lượng < 180.0 giây (< 3 phút) BAO GỒM LUÔN Outro 9:16.
- Render 9:16 (1080x1920 @ 30fps) qua templates/short_digest_v2.html, ghép Outro Nữ qua short_outro.py,
  xuất kèm Thumbnail 9:16 & file mô tả SEO _mota.txt.
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
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.publisher import load_voice_preset, render_thumbnail_9x16, write_mota_9x16
from diemdoc.short_outro import append_short_outro
from diemdoc.tts_text import prepare
from m3_voice import render_chunk_vitts, trim_segment_silence
from m8_news_bridge import compute_pan_params, interpolate_sentence_words
from renderer import render_html_engine
from vieneu import Vieneu

DAY_STR = "16.11.2026"
ROOT = Path(_ROOT)
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
QA_DIR = DAY_DIR / "qa"
SHORTS_DIR = DAY_DIR / "shorts"
DIGEST_AUDIO_DIR = SHORTS_DIR / "digest_audio"
WORK_DIR = Path(paths.WORK) / "digest_short_16_11"
TTS_CACHE_DIR = Path(paths.WORK) / "tts_cache_digest_16_11"

OUT_VIDEO_NAME = "Short_Tin_Nhanh_26_Tin.mp4"
OUT_THUMB_NAME = "Short_Tin_Nhanh_26_Tin_thumbnail.jpg"
OUT_MOTA_NAME = "Short_Tin_Nhanh_26_Tin_mota.txt"
OUT_SCRIPT_NAME = "digest_script_16_11.json"

MAX_TOTAL_SEC_WITH_OUTRO = 179.0
GAP_MS = 220

# Kịch bản tin nhanh 26 tin viết mới hoàn toàn, gán rõ khu vực (Quốc tế=Nam / Việt Nam=Nữ) và ảnh chọn lọc
DIGEST_SPECS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_01_1.jpg",
        "title": "Anh hạ Tây Ban Nha 3-2, đứt mạch 43 trận bất bại",
        "digest_line": "Tuyển Anh hạ gục Tây Ban Nha 3-2 ngay tại Madrid, chấm dứt chuỗi 43 trận bất bại của La Roja.",
    },
    {
        "id": 2,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_02_3.jpg",
        "title": "Bồ Đào Nha thảm bại 1-4 trước Đan Mạch",
        "digest_line": "Trận đầu vắng Cristiano Ronaldo sau 23 năm, Bồ Đào Nha thua đậm Đan Mạch 1-4 trên sân nhà.",
    },
    {
        "id": 3,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_03_1.jpg",
        "title": "Bỉ thắng đậm Italia 4-1 ở Nations League",
        "digest_line": "Nhận ba bàn thua chỉ trong 11 phút, Italia thua Bỉ 1-4 và mất vé tứ kết Nations League.",
    },
    {
        "id": 4,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_04_1.jpg",
        "title": "Hà Lan đè bẹp Hy Lạp với tỷ số 7-0",
        "digest_line": "Tijjani Reijnders lập hat-trick trong 21 phút, giúp Hà Lan hủy diệt Hy Lạp 7-0 tại Amsterdam.",
    },
    {
        "id": 5,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_05_4.jpg",
        "title": "Argentina thua Uruguay 1-2 thời hậu Messi",
        "digest_line": "Cất trống chiếc áo số 10 tri ân Messi, tuyển Argentina bất ngờ gục ngã 1-2 trước Uruguay tại Bombonera.",
    },
    {
        "id": 6,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_06_2.jpg",
        "title": "Nhật Bản thắng ngược Brazil 3-2 phút bù giờ",
        "digest_line": "Nhật Bản thắng ngược Brazil 3-2 phút bù giờ đầu tiên, khiến HLV Carlo Ancelotti nhận thẻ đỏ trực tiếp.",
    },
    {
        "id": 7,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_07_1.jpg",
        "title": "Harry Kane lập kỷ lục 126 trận cho tuyển Anh",
        "digest_line": "Ghi bàn hạ Croatia 2-1, Harry Kane chạm mốc 126 trận, phá kỷ lục tồn tại 36 năm của tuyển Anh.",
    },
    {
        "id": 8,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_08_1.jpg",
        "title": "Man Utd sa thải Carrick, ký hợp đồng Pochettino",
        "digest_line": "Man Utd sa thải Michael Carrick và chi 10 triệu USD giải phóng hợp đồng đón HLV Pochettino đến hè 2029.",
    },
    {
        "id": 9,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_09_2.jpg",
        "title": "FIFPRO World 11 gọi tên Messi, gạch tên Kane",
        "digest_line": "Quả Bóng Vàng Harry Kane bị gạch tên khỏi FIFPRO World 11, còn Messi lập kỷ lục 18 lần góp mặt.",
    },
    {
        "id": 10,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_10_1.jpg",
        "title": "Pau Cubarsi giành Cậu bé Vàng Golden Boy 2026",
        "digest_line": "Trung vệ 19 tuổi Pau Cubarsi của Barcelona xuất sắc đoạt giải thưởng Cậu bé Vàng Golden Boy 2026.",
    },
    {
        "id": 11,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_11_1.jpg",
        "title": "Mourinho phá kỷ lục tỷ lệ thắng của Guardiola",
        "digest_line": "Jose Mourinho đạt tỷ lệ thắng 77% cùng Real Madrid, chính thức xô đổ kỷ lục lịch sử của Pep Guardiola.",
    },
    {
        "id": 12,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_12_1.jpg",
        "title": "Gerrard khen Yamal vượt trội Messi, Ronaldo tuổi 19",
        "digest_line": "Steven Gerrard đánh giá Lamine Yamal vượt xa Messi lẫn Ronaldo ở tuổi 19 với dấu giày 142 bàn thắng.",
    },
    {
        "id": 13,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_13_2.jpg",
        "title": "Thủ môn Owono bị treo giò kịch khung 12 trận",
        "digest_line": "Thủ môn Jesus Owono bị treo giò 12 trận sau pha va chạm khiến tiền đạo Jesus de Miguel qua đời.",
    },
    {
        "id": 14,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_14_1.jpg",
        "title": "Huyền thoại Ronaldinho tái xuất Serie C tuổi 46",
        "digest_line": "Ở tuổi 46, huyền thoại Ronaldinho gây sốt khi tái xuất đá chính cho câu lạc bộ Ravenna tại Serie C.",
    },
    {
        "id": 15,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_15_1.jpg",
        "title": "U23 Việt Nam thắng Thái Lan 3-0, hạ Singapore 1-0",
        "digest_line": "Tại giải Gia Lai, U23 Việt Nam thắng đậm U23 Thái Lan 3-0 rồi hạ gọn U23 Singapore 1-0.",
    },
    {
        "id": 16,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_16_1.jpg",
        "title": "Hòa Qatar 1-1, U23 Việt Nam vô địch Gia Lai Cup",
        "digest_line": "Cầm hòa U23 Qatar 1-1, U23 Việt Nam bất bại lên ngôi vô địch Gia Lai và nhận 2,6 tỷ đồng.",
    },
    {
        "id": 17,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_17_2.jpg",
        "title": "Tuyển Việt Nam thắng Đài Loan 2-0, lên hạng 98",
        "digest_line": "Đội tuyển Việt Nam thắng Đài Loan 2-0 nhờ công Olaha Mạnh Đức và Đình Bắc, vươn lên hạng 98 FIFA.",
    },
    {
        "id": 18,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_18_2.jpg",
        "title": "Mỹ rút World Cup, U17 Việt Nam chốt 21 cầu thủ",
        "digest_line": "Mỹ rút khỏi U17 World Cup nhường suất cho Dominica, còn U17 Việt Nam chốt 21 tuyển thủ sang Qatar.",
    },
    {
        "id": 19,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_19_4.jpg",
        "title": "VFF đình chỉ vô thời hạn sáu cầu thủ Long An",
        "digest_line": "Ban kỷ luật VFF quyết định đình chỉ vô thời hạn sáu thành viên câu lạc bộ Long An dàn xếp tỷ số.",
    },
    {
        "id": 20,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_20_2.jpg",
        "title": "HLV Park Hang-seo bị phạt vì bảo vệ học trò",
        "digest_line": "Bức xúc lên tiếng bảo vệ học trò bị miệt thị chủng tộc, HLV Park Hang-seo vẫn bị phạt tại Thái Lan.",
    },
    {
        "id": 21,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_21_1.jpg",
        "title": "Trịnh Thu Vinh đoạt HCB thế giới, vé Olympic 2028",
        "digest_line": "Xạ thủ Trịnh Thu Vinh giành HCB bắn súng thế giới, mang về vé Olympic 2028 đầu tiên cho Việt Nam.",
    },
    {
        "id": 22,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_22_1.jpg",
        "title": "Phan Huy Hoàng đoạt HCV cờ tướng thế giới 2026",
        "digest_line": "Kỳ thủ 18 tuổi Phan Huy Hoàng bất bại đoạt HCV cờ tướng thế giới, còn Lại Lý Huynh giành hai HCB.",
    },
    {
        "id": 23,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_23_1.jpg",
        "title": "Lê Quang Liêm thắng ván cờ chính xác 99%",
        "digest_line": "Đạt độ chính xác 99% khi hạ Artemiev, Lê Quang Liêm bất bại bảng B tử thần tại giải thế giới.",
    },
    {
        "id": 24,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_24_3.jpg",
        "title": "Bóng bàn Việt Nam giành cú đúp HCV Đông Nam Á",
        "digest_line": "Nguyễn Anh Tú đoạt HCV đơn nam cùng chức vô địch đồng đội, giúp bóng bàn Việt Nam đại thắng Đông Nam Á.",
    },
    {
        "id": 25,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_25_1.jpg",
        "title": "Nữ luật sư chạy 161 km ở Nam Cực phá kỷ lục",
        "digest_line": "Bất chấp cái lạnh âm 35 độ, Stephanie Case chạy 161 kilômét ở Nam Cực, phá kỷ lục nam hơn 5 giờ.",
    },
    {
        "id": 26,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_26_2.jpg",
        "title": "ATP Finals 2026 khởi tranh rực lửa tại Turin",
        "digest_line": "Giải quần vợt cuối mùa ATP Finals 2026 khởi tranh tại Turin với cuộc đua nảy lửa giữa Alcaraz và Zverev.",
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
    """Tạo bảng đối chứng 26 ảnh đã chọn cho Digest Short (lưu trong outputs/16.11.2026/qa/)."""
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
        "KIỂM DUYỆT 26 ẢNH DIGEST SHORT (16.11.2026) — QUỐC TẾ: NAM | VIỆT NAM: NỮ",
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
    parser = argparse.ArgumentParser(description="Dựng Video Short Bản Tin Nhanh 26 Tin (<3p gồm Outro) — 16.11.2026")
    parser.add_argument("--prep-only", action="store_true", help="Chỉ sinh script, QA ảnh và giọng đọc (chưa render video)")
    parser.add_argument("--force-tts", action="store_true", help="Sinh lại toàn bộ giọng đọc mới bỏ qua cache")
    args = parser.parse_args()

    for d in (WORK_DIR, TTS_CACHE_DIR, SHORTS_DIR, DIGEST_AUDIO_DIR, QA_DIR):
        d.mkdir(parents=True, exist_ok=True)

    thethao_items = {int(it["id"]): it for it in json.loads((DAY_DIR / "thethao.json").read_text(encoding="utf-8"))}
    credits_map = json.loads((DAY_DIR / "image_credits.json").read_text(encoding="utf-8"))

    male_preset = load_voice_preset("primary")
    female_preset = load_voice_preset("secondary")

    banner(
        f"SẢN XUẤT BẢN TIN NHANH 26 TIN (< 3 PHÚT GỒM OUTRO) — {DAY_STR}",
        f"Quốc tế: {male_preset['voice_label']} | Việt Nam: {female_preset['voice_label']}",
    )

    if args.force_tts and TTS_CACHE_DIR.exists():
        shutil.rmtree(TTS_CACHE_DIR, ignore_errors=True)
        TTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

    step("1. Kiểm tra 26 ảnh chọn lọc và tổng hợp giọng đọc ViTTS v3turbo hoàn toàn mới...")
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

        # Đồng bộ từng từ Karaoke theo độ dài audio thật vừa sinh
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
        log(f"  [{idx:02d}/26] ({spec['region']} | {spec['voice_gender']}) {it_dur:.2f}s | {spec['title']}")

    # Xuất voiceover.wav trực tiếp trong WORK_DIR để renderer.py trộn BGM + SFX + loudnorm
    voiceover_wav = WORK_DIR / "voiceover.wav"
    combined_voice.export(str(voiceover_wav), format="wav")
    body_dur = round(len(combined_voice) / 1000.0, 3)

    # Outro đối xứng Nữ (vì 2 tin cuối 25-26 là giọng Nam) khoảng 5.4s - 6.5s
    max_expected_with_outro = body_dur + 6.55
    ok(f"Thời lượng phần thân 26 tin: {body_dur:.2f}s | Dự kiến cả Outro: <= {max_expected_with_outro:.2f}s (Ngưỡng < 180.00s)")
    if max_expected_with_outro >= MAX_TOTAL_SEC_WITH_OUTRO:
        die(f"Vượt trần thời lượng cho phép ({max_expected_with_outro:.2f}s >= 180.0s)! Hãy rút gọn thoại.")

    # Lưu bảng đối chứng QA 26 ảnh và file kịch bản JSON
    build_digest_contact_sheet(items_data, QA_DIR / "contact_digest_16_11.jpg")
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
        ok("Hoàn tất chế độ --prep-only (đã tạo script, kiểm tra ảnh QA và sinh 26 file giọng đọc).")
        return

    # 2. Dựng timeline JSON chuẩn templates/short_digest_v2.html
    fx_cfg: Dict[str, Any] = {}
    fx_path = Path(paths.CONFIG) / "fx.json"
    if fx_path.exists():
        fx_cfg = json.loads(fx_path.read_text(encoding="utf-8"))

    timeline = {
        "title": "TIN NHANH THỂ THAO TUẦN QUA",
        "channel_name": "ĐIỂM ĐỌC",
        "date_str": "THỨ HAI · 16.11.2026",
        "date_chip": "THỨ HAI · 16.11.2026",
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

    # 3. Render phần thân 9:16 qua Playwright + GSAP
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

    # 4. Ghép Outro giọng Nữ đối xứng sau Tin 25-26 giọng Nam (voice_hint="primary")
    out_video = SHORTS_DIR / OUT_VIDEO_NAME
    final_path, chosen_outro = append_short_outro(
        rendered_body,
        voice_hint="primary",
        out_path=out_video,
        seed="digest_16_11_v1",
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

    # 5. Render Thumbnail 9:16 & File mô tả SEO _mota.txt
    thumb_path = SHORTS_DIR / OUT_THUMB_NAME
    render_thumbnail_9x16(
        out_path=thumb_path,
        image_path=IMAGES_DIR / "Tin_01_1.jpg",
        kicker="ĐIỂM NHANH 26 SỰ KIỆN NÓNG TUẦN QUA",
        hero_html='<span class="hl-cyan">26 TIN NHANH!</span><br><span class="hl-white">TÂY BAN NHA - ANH</span><br><span class="hl-yellow">U23 VN VÔ ĐỊCH!</span>',
        subtitle="QUỐC TẾ GIỌNG NAM • VIỆT NAM GIỌNG NỮ • TÓM TẮT TRỌN VẸN DƯỚI 3 PHÚT",
        badge="26 TIN NHANH",
        tag_a="QUỐC TẾ & VN",
        tag_b="16.11.2026",
        obj_pos="center 20%",
    )

    chapters_list = []
    for it in items_data:
        sec_i = int(it["start"])
        m, s = divmod(sec_i, 60)
        chapters_list.append((f"{m:02d}:{s:02d}", it["title"]))

    mota_path = SHORTS_DIR / OUT_MOTA_NAME
    write_mota_9x16(
        out_path=mota_path,
        seo_title="Tin nhanh thể thao 16/11: 26 sự kiện nóng nhất tuần qua — Anh hạ TBN, U23 Việt Nam vô địch #Shorts",
        description_paragraphs=[
            "Bản tin Điểm Đọc đọc nhanh trọn bộ 26 sự kiện thể thao chấn động tuần qua (09/11 – 15/11/2026) dưới 3 phút với giọng Nam dẫn tin quốc tế và giọng Nữ dẫn tin Việt Nam.",
            "Điểm lướt từ địa chấn Nations League, Man Utd đón Pochettino, Messi lập kỷ lục FIFPRO tới chức vô địch Gia Lai của U23 Việt Nam, vé Olympic 2028 của Trịnh Thu Vinh và HCV cờ tướng thế giới.",
        ],
        chapters=chapters_list,
        sources_line="📰 Nguồn tin: VnExpress, Thanh Niên, Dân Trí, Reuters, AP, UEFA, FIFA, ISSF, VFF.",
        hashtags=["#Shorts", "#TinNhanh", "#DiemDoc", "#DiemDocTheThao", "#BongDa", "#U23VietNam", "#NationsLeague", "#ManUtd", "#HarryKane", "#TrinhThuVinh"],
    )

    ok("=" * 72)
    ok(f"HOÀN TẤT DIGEST SHORT 26 TIN -> {paths.rel_to_root(str(final_path))}")
    ok(f"Thời lượng: Video={v_dur:.2f}s (Audio={a_dur:.2f}s, Drift={drift_ms:.2f}ms) | Outro: {chosen_outro.name if chosen_outro else 'None'}")
    if stats:
        ok(f"Âm lượng: I={stats.get('input_i')} LUFS | TP={stats.get('input_tp')} dBTP")
    ok("=" * 72)


if __name__ == "__main__":
    main()
