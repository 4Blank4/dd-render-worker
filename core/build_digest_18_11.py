#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_digest_18_11.py — Sản xuất Video Short "Bản Tin Nhanh 17 Tin" Ngày 18.11.2026
======================================================================================
- Viết mới 100% lời thoại tin nhanh cô đọng (không dùng lại câu/audio của bản tin dài).
- Phân giọng theo khu vực:
    + Việt Nam (01..03, 11..14): Giọng Nữ Ngọc Huyền (Mẫu 14).
    + Quốc tế (04..10, 15..17): Giọng Nam chính Minh Quân Pro (Mẫu 15).
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
from diemdoc.log import banner, die, log, ok, step
from diemdoc.publisher import load_voice_preset, render_thumbnail_9x16, write_mota_9x16
from diemdoc.short_outro import append_short_outro
from diemdoc.tts_text import prepare
from m3_voice import render_chunk_vitts, trim_segment_silence
from m8_news_bridge import compute_pan_params, interpolate_sentence_words
from renderer import render_html_engine
from vieneu import Vieneu

DAY_STR = "18.11.2026"
ROOT = Path(_ROOT)
DAY_DIR = ROOT / "outputs" / DAY_STR
IMAGES_DIR = DAY_DIR / "images"
QA_DIR = DAY_DIR / "qa"
SHORTS_DIR = DAY_DIR / "shorts"
DIGEST_AUDIO_DIR = SHORTS_DIR / "digest_audio"
WORK_DIR = Path(paths.WORK) / "digest_short_18_11"
TTS_CACHE_DIR = Path(paths.WORK) / "tts_cache_digest_18_11"

OUT_VIDEO_NAME = "Short_Tin_Nhanh_17_Tin.mp4"
OUT_THUMB_NAME = "Short_Tin_Nhanh_17_Tin_thumbnail.jpg"
OUT_MOTA_NAME = "Short_Tin_Nhanh_17_Tin_mota.txt"
OUT_SCRIPT_NAME = "digest_script_18_11.json"

MAX_TOTAL_SEC_WITH_OUTRO = 179.0
GAP_MS = 220

# Kịch bản tin nhanh 17 tin viết mới hoàn toàn, phân giọng Việt Nam (Nữ) / Quốc tế (Nam)
DIGEST_SPECS: List[Dict[str, Any]] = [
    {
        "id": 1,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_01_1.jpg",
        "title": "Tuyển Việt Nam thua ngược Kyrgyzstan 1-2 phút cuối",
        "digest_line": "Nhận liền hai bàn thua từ phút 86 trên sân Thiên Trường, đội tuyển Việt Nam thua ngược Kyrgyzstan 1-2 và lỡ ngôi vô địch Casper Cup.",
    },
    {
        "id": 2,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_02_1.jpg",
        "title": "Đình Bắc chạm mốc Công Phượng, Việt Nam mất 5,3 điểm FIFA",
        "digest_line": "Nguyễn Đình Bắc chạm mốc 12 bàn ngang bằng Công Phượng, nhưng tuyển Việt Nam bị trừ 5,3 điểm FIFA dù thay tám người đúng luật mới.",
    },
    {
        "id": 3,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_03_1.jpg",
        "title": "HLV Kim Sang-sik nhận lỗi, bảo vệ Trần Trung Kiên",
        "digest_line": "HLV Kim Sang-sik gửi lời xin lỗi người hâm mộ, đồng thời bảo vệ thủ môn trẻ Trần Trung Kiên trước áp lực sau bàn thua từ cự ly 60 mét.",
    },
    {
        "id": 4,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_04_1.jpg",
        "title": "Bồ Đào Nha thắng kịch tính Xứ Wales 3-2 dù thiếu người",
        "digest_line": "Dù Pedro Neto nhận thẻ đỏ hiệp hai, Bồ Đào Nha vẫn thắng nghẹt thở Xứ Wales 3-2 để khép lại vòng bảng với 15 điểm tuyệt đối.",
    },
    {
        "id": 5,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_05_1.jpg",
        "title": "Haaland lập cú đúp đưa Na Uy vào tứ kết Nations League",
        "digest_line": "Lập cú đúp cùng quả phạt đền phút 96, Erling Haaland giúp Na Uy thắng ngược Đan Mạch 3-2, chốt đủ tám đội vào tứ kết Nations League.",
    },
    {
        "id": 6,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_06_1.jpg",
        "title": "Vinícius lập hat-trick trong 21 phút, Brazil thắng 7-0",
        "digest_line": "Vinícius Júnior bùng nổ với cú hat-trick chỉ trong 21 phút, giúp đội tuyển Brazil đè bẹp Singapore 7-0 để thắng đậm nhất sau 14 năm.",
    },
    {
        "id": 7,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_07_1.jpg",
        "title": "Nico Paz và Álvarez tỏa sáng, Argentina thắng 7-0",
        "digest_line": "Truyền nhân Messi là Nico Paz cùng Julián Álvarez đồng loạt lập cú đúp, đưa Argentina vùi dập Costa Rica tới 7-0 trên sân nhà.",
    },
    {
        "id": 8,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_08_1.jpg",
        "title": "Pochettino chia tay tuyển Mỹ, bay sang Manchester United",
        "digest_line": "Sau trận hòa Haiti 0-0 đưa tuyển Mỹ vào bán kết, HLV Mauricio Pochettino lập tức lên chuyên cơ xuyên đêm sang tiếp quản Manchester United.",
    },
    {
        "id": 9,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_09_1.jpg",
        "title": "Nhật Bản thua sốc Paraguay, Ireland thắng đậm Kosovo",
        "digest_line": "Đội tuyển Nhật Bản bất ngờ thua Paraguay 1-2 ngay trên sân nhà, trong khi Cộng hòa Ireland thắng đậm Kosovo 3-0 tại Nations League.",
    },
    {
        "id": 10,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_10_1.jpg",
        "title": "Supachok tỏa sáng, Thái Lan lần thứ 17 vô địch King's Cup",
        "digest_line": "Supachok ghi bàn mở tỷ số và kiến tạo giúp Thái Lan thắng đậm Tajikistan 3-0, nâng cao chiếc cúp King's Cup lần thứ 17 trong lịch sử.",
    },
    {
        "id": 11,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_11_1.jpg",
        "title": "U19 Việt Nam hòa U19 Tajikistan 2-2 khép lại Panda Cup",
        "digest_line": "Tiền đạo Hoàng Công Hậu tỏa sáng với cú đúp, giúp U19 Việt Nam cầm hòa U19 Tajikistan 2-2 trong ngày chia tay giải Panda Cup 2026.",
    },
    {
        "id": 12,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_12_1.jpg",
        "title": "CLB Công an TP.HCM tự tin chơi tấn công trước Buriram",
        "digest_line": "Hướng tới lượt đấu tối nay tại Shopee Cup, HLV Arthur Diles khẳng định CLB Công an TP.HCM sẽ chơi tấn công trước đương kim vô địch Buriram United.",
    },
    {
        "id": 13,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_13_1.jpg",
        "title": "TP.HCM sơ duyệt sân khấu gần 2000 chỗ Đại hội TDTT 2026",
        "digest_line": "TP.HCM đang gấp rút sơ duyệt sân khấu gần 2000 chỗ ngồi bên bờ sông Sài Gòn, sẵn sàng cho Lễ khai mạc Đại hội Thể thao toàn quốc 2026.",
    },
    {
        "id": 14,
        "region": "Việt Nam",
        "voice_preset": "secondary",
        "voice_gender": "Nữ",
        "image_file": "Tin_14_1.jpg",
        "title": "Lê Quang Liêm leo hạng 12 thế giới, bỏ túi 32000 USD",
        "digest_line": "Lê Quang Liêm tăng 10,4 điểm Elo vươn lên hạng 12 thế giới cùng tối thiểu 32000 USD tiền thưởng dù tạm thất thế trước Hans Niemann ở lượt đi.",
    },
    {
        "id": 15,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_15_1.jpg",
        "title": "Alexander Zverev sớm vào bán kết ATP Finals 2026",
        "digest_line": "Đánh bại Ben Shelton sau hai set đấu, tay vợt số một thế giới Alexander Zverev trở thành người đầu tiên đoạt vé bán kết ATP Finals tại Turin.",
    },
    {
        "id": 16,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_16_1.jpg",
        "title": "Bóng đá Argentina bàng hoàng vì sự ra đi của Abel Nunez",
        "digest_line": "Bóng đá trẻ Argentina bàng hoàng tiếc thương tiền vệ 16 tuổi Abel Nunez qua đời sau bốn ngày cấp cứu vì chấn thương đầu trên sân cỏ.",
    },
    {
        "id": 17,
        "region": "Quốc tế",
        "voice_preset": "primary",
        "voice_gender": "Nam",
        "image_file": "Tin_17_2.jpg",
        "title": "Wayne Rooney tiết lộ góc khuất tâm lý gây sốc tại Man Utd",
        "digest_line": "Cựu thủ quân tuyển Anh Wayne Rooney khiến làng bóng đá chấn động khi thừa nhận từng rơi vào khủng hoảng tâm lý nặng nề thời đỉnh cao ở Man Utd.",
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
    """Tạo bảng đối chứng 17 ảnh đã chọn cho Digest Short (lưu trong outputs/18.11.2026/qa/)."""
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
        f"KIỂM DUYỆT 17 ẢNH DIGEST SHORT ({DAY_STR}) — VIỆT NAM: NỮ | QUỐC TẾ: NAM",
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
    parser = argparse.ArgumentParser(description=f"Dựng Video Short Bản Tin Nhanh 17 Tin (<3p gồm Outro) — {DAY_STR}")
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

    step(f"1. Kiểm tra {total_items} ảnh chọn lọc và tổng hợp giọng đọc ViTTS v3turbo hoàn toàn mới...")
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

    # Tin 17 (cuối) là giọng Nam ("primary") nên Outro tự chọn đối xứng giọng Nữ (~5.4-6.5s)
    max_expected_with_outro = body_dur + 6.55
    ok(f"Thời lượng phần thân {total_items} tin: {body_dur:.2f}s | Dự kiến cả Outro: <= {max_expected_with_outro:.2f}s (Ngưỡng < 180.00s)")
    if max_expected_with_outro >= MAX_TOTAL_SEC_WITH_OUTRO:
        die(f"Vượt trần thời lượng cho phép ({max_expected_with_outro:.2f}s >= 180.0s)! Hãy rút gọn thoại.")

    build_digest_contact_sheet(items_data, QA_DIR / "contact_digest_18_11.jpg")
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
        "title": "TIN NHANH THỂ THAO 18.11",
        "channel_name": "ĐIỂM ĐỌC",
        "date_str": "THỨ TƯ · 18.11.2026",
        "date_chip": "THỨ TƯ · 18.11.2026",
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
        seed="digest_18_11_v1",
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
        image_path=IMAGES_DIR / "Tin_02_1.jpg",
        kicker="ĐIỂM NHANH 17 TIN THỂ THAO 18.11",
        hero_html='<span class="hl-cyan">17 TIN NHANH!</span><br><span class="hl-white">VN THUA NGƯỢC 1-2</span><br><span class="hl-yellow">MU ĐÓN POCHETTINO!</span>',
        subtitle="VIỆT NAM GIỌNG NỮ • QUỐC TẾ GIỌNG NAM • TÓM TẮT NHANH DƯỚI 3 PHÚT",
        badge="17 TIN NHANH",
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
        seo_title="Tin nhanh thể thao 18/11: Việt Nam thua ngược 1-2, Haaland cứu Na Uy, MU đón Pochettino #Shorts",
        description_paragraphs=[
            "Điểm đọc nhanh 17 tin tức thể thao nóng nhất sáng ngày 18/11/2026 gói gọn trong hơn 2 phút — từ tâm điểm bóng đá Việt Nam tới sân cỏ quốc tế, cờ vua và quần vợt đỉnh cao.",
            "Cập nhật liên tiếp trận thua ngược đầy tiếc nuối của tuyển Việt Nam trước Kyrgyzstan, cột mốc 12 bàn của Đình Bắc, màn lội ngược dòng của Bồ Đào Nha và Na Uy tại Nations League, chiến thắng 7-0 của Brazil và Argentina cùng bước ngoặt Pochettino dẫn dắt Man Utd.",
        ],
        chapters=chapters_list,
        sources_line="📰 Nguồn tin: VnExpress, Thanh Niên, Dân Trí, Reuters, AP, UEFA, FIFA, FAT, ATP Tour, FIDE.",
        hashtags=["#Shorts", "#TinNhanh", "#DiemDoc", "#DiemDocTheThao", "#DTQGVietNam", "#NguyenDinhBac", "#NationsLeague", "#ManUtd", "#LeQuangLiem", "#Haaland"],
    )

    ok("=" * 72)
    ok(f"HOÀN TẤT DIGEST SHORT {total_items} TIN -> {paths.rel_to_root(str(final_path))}")
    ok(f"Thời lượng: Video={v_dur:.2f}s (Audio={a_dur:.2f}s, Drift={drift_ms:.2f}ms) | Outro: {chosen_outro.name if chosen_outro else 'None'}")
    if stats:
        ok(f"Âm lượng: I={stats.get('input_i')} LUFS | TP={stats.get('input_tp')} dBTP")
    ok("=" * 72)


if __name__ == "__main__":
    main()
