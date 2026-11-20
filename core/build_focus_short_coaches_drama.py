#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_focus_short_coaches_drama.py — Sản xuất Video Focus Short 5 (9:16)
"Biến Động Băng Ghế HLV: Man Utd Hỗn Loạn, Mourinho Lập Kỷ Lục Lịch Sử"
(BẢN LIỀN MẠCH — UNIFIED SEAMLESS NARRATIVE)

Quy chuẩn kỹ thuật:
1. Liền mạch 100% nội dung (Unified Storytelling Narrative):
   - Kịch bản dẫn chuyện một mạch từ đầu đến cuối không chia vụn tin, không Hero Title ở giữa.
   - Thanh tiêu đề cố định (#fixed-headline-bar) hiển thị trang nhã trên đỉnh khung hình.
2. An toàn từ ngữ & Subtitle Karaoke:
   - Dùng 100% từ gốc nguyên bản của kịch bản (interpolate_sentence_words), tuyệt đối không lấy text từ Whisper.
   - Giữ nguyên tên riêng quốc tế (Michael Carrick, Mauricio Pochettino, Jim Ratcliffe, Bruno Fernandes, Jose Mourinho, Pep Guardiola, Park Hang-seo, John Baggio...).
   - Đơn vị tiền tệ 10 triệu USD (đọc 10 triệu đô, hiển thị 10 triệu USD).
   - Gom cụm phụ đề thông minh (3-5 từ), không bẻ đôi từ ghép tiếng Việt.
3. Phân bổ hình ảnh động:
   - 14 ảnh hiện trường HD lia ngang (Pan) mượt mà bám sát từng câu.
   - Lower-Third 2 góc động: Nguồn bài viết bên trái + Nguồn ảnh bên phải đổi tức thời theo từng ảnh.
4. Thời lượng: ~49s audio + 5.4s Outro = ~55s (chuẩn YouTube Shorts).
"""

import sys
sys.dont_write_bytecode = True

import os
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "core"))

from diemdoc import paths
from diemdoc.tts_text import prepare
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from diemdoc.audio import apply_voice_standard
from diemdoc.short_outro import append_short_outro
from diemdoc.publisher import load_voice_preset, render_thumbnail_9x16, write_mota_9x16
from m8_news_bridge import interpolate_sentence_words, compute_pan_params
from engines.html.renderer import render_html_engine
from core.vendor.vieneu import Vieneu


def ok(msg: str):
    print(f"\033[32m[ok]\033[0m {msg}")


def step(msg: str):
    print(f"\n\033[36m──────────────────────────────────────────────────────────────────\033[0m")
    print(f"  \033[1;36m{msg}\033[0m")
    print(f"\033[36m──────────────────────────────────────────────────────────────────\033[0m")


def banner(title: str, sub: str = ""):
    print(f"\n\033[1;33m══════════════════════════════════════════════════════════════════\033[0m")
    print(f"  \033[1;37m{title}\033[0m")
    if sub:
        print(f"  \033[33m{sub}\033[0m")
    print(f"\033[1;33m══════════════════════════════════════════════════════════════════\033[0m")


def die(msg: str):
    print(f"\033[31m[die]\033[0m {msg}", file=sys.stderr)
    sys.exit(1)


def build_smart_karaoke_chunks(words_data: List[Dict[str, Any]], target_size: int = 4) -> List[Dict[str, Any]]:
    """
    Gom nhóm từ hiển thị thành các cụm Karaoke 3-5 từ tự nhiên,
    tuyệt đối không bẻ đôi các từ ghép (như 'huấn luyện', 'sa thải', 'hợp đồng', 'kỷ lục'...).
    """
    if not words_data:
        return []

    no_end_words = {
        "đầy", "nhưng", "và", "của", "trong", "khi", "với", "ở", "tại", "lên", "cho",
        "bị", "được", "vừa", "lại", "huấn", "sa", "hợp", "kỷ", "chiến", "người", "đại",
        "tỷ", "triệu", "học", "bảo", "thầy", "án", "phạt"
    }
    no_start_words = {
        "luyện", "thải", "đồng", "lục", "lược", "đặc", "kình", "phú", "trò", "vệ", "viên", "biệt", "địch", "USD"
    }

    chunks = []
    i = 0
    n = len(words_data)

    while i < n:
        size = target_size
        if i + size > n:
            size = n - i
        else:
            last_w = words_data[i + size - 1]["word"].lower().strip(".,!?:;")
            if last_w in no_end_words and (i + size) < n:
                size += 1
            elif (i + size) < n:
                next_w = words_data[i + size]["word"].lower().strip(".,!?:;")
                if next_w in no_start_words:
                    size += 1

            rem = n - (i + size)
            if rem == 1 and (i + size) < n:
                size += 1

        c_slice = words_data[i:i + size]
        chunks.append({
            "start": c_slice[0]["start"],
            "end": c_slice[-1]["end"],
            "text": " ".join(w["word"] for w in c_slice),
            "words": c_slice
        })
        i += size

    return chunks


def create_qa_contact_sheet(qa_dir: Path, image_records: List[Dict[str, str]], output_path: Path):
    """Tạo Contact Sheet QA đối chứng ảnh cho Focus Short."""
    cols = 4
    rows = (len(image_records) + cols - 1) // cols
    card_w, card_h = 440, 310
    pad = 16
    total_w = cols * card_w + (cols + 1) * pad
    total_h = rows * card_h + (rows + 1) * pad + 60

    canvas = Image.new("RGB", (total_w, total_h), (8, 12, 22))
    draw = ImageDraw.Draw(canvas)

    font_title = ImageFont.truetype(str(_ROOT / "assets" / "fonts" / "Be_Vietnam_Pro" / "BeVietnamPro-Bold.ttf"), 30)
    font_lbl = ImageFont.truetype(str(_ROOT / "assets" / "fonts" / "Montserrat" / "Montserrat-VariableFont_wght.ttf"), 17)
    font_cap = ImageFont.truetype(str(_ROOT / "assets" / "fonts" / "Montserrat" / "Montserrat-VariableFont_wght.ttf"), 14)

    draw.text((pad, 16), "BẢNG ĐỐI CHỨNG HÌNH ẢNH — SHORT 5: BIẾN ĐỘNG BĂNG GHẾ HUẤN LUYỆN", fill=(0, 229, 255), font=font_title)

    for idx, rec in enumerate(image_records):
        r = idx // cols
        c = idx % cols
        x0 = pad + c * (card_w + pad)
        y0 = 60 + pad + r * (card_h + pad)

        draw.rectangle([x0, y0, x0 + card_w, y0 + card_h], fill=(14, 20, 34), outline=(30, 45, 75), width=1)

        p = Path(rec["path"])
        orig_size = "N/A"
        if p.exists():
            try:
                im = Image.open(p).convert("RGB")
                orig_size = f"{im.width}x{im.height}"
                im.thumbnail((card_w - 8, 220), Image.Resampling.LANCZOS)
                canvas.paste(im, (x0 + (card_w - im.width) // 2, y0 + (224 - im.height) // 2))
            except Exception:
                pass

        draw.text((x0 + 8, y0 + 230), f"{rec['name']} ({orig_size})", fill=(0, 229, 255), font=font_lbl)
        draw.text((x0 + 8, y0 + 252), f"Nguồn: {rec['credit']}", fill=(250, 204, 21), font=font_cap)
        desc = rec["desc"][:45] + ("..." if len(rec["desc"]) > 45 else "")
        draw.text((x0 + 8, y0 + 274), desc, fill=(220, 230, 245), font=font_cap)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="JPEG", quality=92)
    ok(f"Đã xuất bảng đối chứng QA: {output_path}")


def main():
    day_str = "16.11.2026"
    day_dir = _ROOT / "outputs" / day_str
    shorts_dir = day_dir / "shorts"
    qa_dir = day_dir / "qa"
    shorts_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)

    banner("SẢN XUẤT SHORT 5 (BẢN LIỀN MẠCH): BIẾN ĐỘNG BĂNG GHẾ HUẤN LUYỆN (9:16)", day_str)

    work_proj_dir = Path.home() / "Library" / "Caches" / "DiemDoc" / "focus_short_05_coaches"
    work_proj_dir.mkdir(parents=True, exist_ok=True)
    cache_tts_dir = str(paths.work_file("vitts_cache"))

    # Đọc overrides nếu có
    say_overrides = {}
    ov_path = day_dir / "manual_overrides.json"
    if ov_path.exists():
        try:
            say_overrides = json.loads(ov_path.read_text(encoding="utf-8"))
        except Exception:
            say_overrides = {}

    # Danh mục nguồn ảnh chuẩn cho từng file ảnh
    IMG_CREDITS_MAP = {
        "Tin_08_1.jpg": "REUTERS",
        "Tin_08_3.jpg": "REUTERS",
        "Tin_08_4.jpg": "TALKSPORT",
        "Tin_08_6.jpg": "REUTERS",
        "Tin_08_12.jpg": "REUTERS",
        "Tin_11_1.jpg": "AFP",
        "Tin_11_5.jpg": "AFP",
        "Tin_11_6.jpg": "AFP / REUTERS",
        "Tin_11_8.jpg": "LA LIGA",
        "Tin_11_9.jpg": "AP PHOTO",
        "Tin_20_1.jpg": "BERNY ZIMMER",
        "Tin_20_2.jpg": "THANH NIÊN",
        "Tin_20_6.jpg": "BANGKOK POST",
        "Tin_20_10.jpg": "KANCHANABURI FC",
        "Tin_20_11.jpg": "KANCHANABURI FC"
    }

    # 1. KỊCH BẢN DẪN CHUYỆN LIỀN MẠCH DUY NHẤT (7 CÂU — UNIFIED STORYTELLING NARRATIVE)
    story_sentences = [
        {
            "id": 1,
            "text": "Băng ghế huấn luyện viên tuần qua chưa bao giờ nóng bỏng đến thế: kẻ mất việc trong cay đắng, người ngạo nghễ lập kỷ lục lịch sử, và một người thầy chấp nhận chịu phạt để bảo vệ học trò.",
            "group": "BIẾN ĐỘNG GHẾ NÓNG",
            "news_source": "THE ATHLETIC / LA LIGA",
            "credit": "REUTERS / AFP",
            "images": ["Tin_08_3.jpg", "Tin_11_1.jpg"]
        },
        {
            "id": 2,
            "text": "Tại Old Trafford, cuộc khủng hoảng đưa Man Utd xuống nhóm cầm đèn đỏ đã chấm dứt bằng trát sa thải nghiệt ngã dành cho Michael Carrick, sau cuộc họp khẩn của tỷ phú Jim Ratcliffe.",
            "group": "KHỦNG HOẢNG OLD TRAFFORD",
            "news_source": "THE ATHLETIC / REUTERS",
            "credit": "TALKSPORT / REUTERS",
            "images": ["Tin_08_4.jpg", "Tin_08_6.jpg"]
        },
        {
            "id": 3,
            "text": "Quỷ đỏ lập tức chi 10 triệu USD giải phóng hợp đồng của Mauricio Pochettino trước đại chiến Liverpool, bất chấp bức tâm thư 142 từ bị chỉ trích gay gắt và đội trưởng Bruno Fernandes hai lần từ chối gia hạn.",
            "group": "TRIỀU ĐẠI POCHETTINO",
            "news_source": "REUTERS / MARCA",
            "credit": "REUTERS",
            "images": ["Tin_08_1.jpg", "Tin_08_12.jpg"]
        },
        {
            "id": 4,
            "text": "Trái ngược với sự hỗn loạn tại nước Anh, Người Đặc Biệt Jose Mourinho lại làm nên lịch sử tại La Liga khi chính thức vượt qua đại kình địch Pep Guardiola về tỷ lệ thắng cao nhất giải đấu.",
            "group": "NGƯỜI ĐẶC BIỆT",
            "news_source": "LA LIGA / AFP",
            "credit": "AFP / REUTERS",
            "images": ["Tin_11_5.jpg", "Tin_11_6.jpg"]
        },
        {
            "id": 5,
            "text": "Với tỷ lệ thắng 77 phần trăm cùng chuỗi 8 trận toàn thắng để đoạt giải HLV xuất sắc nhất tháng 10, chiến lược gia 63 tuổi khẳng định ông chỉ hướng về phía trước thay vì sống bằng quá khứ.",
            "group": "KỶ LỤC LỊCH SỬ",
            "news_source": "LA LIGA / AP PHOTO",
            "credit": "LA LIGA / AP PHOTO",
            "images": ["Tin_11_8.jpg", "Tin_11_9.jpg"]
        },
        {
            "id": 6,
            "text": "Trong khi đó tại Đông Nam Á, HLV Park Hang-seo lại nhận án phạt cấm chỉ đạo hai trận tại Thái Lan vì lao vào sân bảo vệ học trò John Baggio trước những lời miệt thị chủng tộc.",
            "group": "BẢN LĨNH THẦY PARK",
            "news_source": "BANGKOK POST / DÂN TRÍ",
            "credit": "THANH NIÊN / BANGKOK POST",
            "images": ["Tin_20_2.jpg", "Tin_20_6.jpg"]
        },
        {
            "id": 7,
            "text": "Tuyên bố không bao giờ im lặng khi học trò bị lăng mạ, ông Park lập tức cùng đội bóng thắng trận để lọt vào top 4, khắc họa trọn vẹn bản lĩnh và cái tâm của một người thầy thực thụ.",
            "group": "TÂM HUYẾT NGƯỜI THẦY",
            "news_source": "VNEXPRESS / KANCHANABURI FC",
            "credit": "KANCHANABURI FC",
            "images": ["Tin_20_10.jpg", "Tin_20_11.jpg"]
        }
    ]

    # 2. TỔNG HỢP ÂM THANH GIỌNG ĐỌC LIỀN MẠCH (1 TRACK MASTER VOICEOVER DUY NHẤT)
    step("Kiểm tra và tổng hợp giọng Nam Minh Quân Pro liền một mạch...")
    preset = load_voice_preset("primary")
    voice = preset["voice_id"]
    speed = preset["speed"]
    pitch = preset["pitch"]
    temp = preset["temperature"]

    model = Vieneu(mode="v3turbo")
    full_audio = AudioSegment.empty()
    sent_audio_segments = []

    for s_idx, sent_info in enumerate(story_sentences):
        raw_text = sent_info["text"]
        clean_text, _ = prepare(raw_text, manual_overrides=say_overrides)
        chunks = build_chunks_from_text(clean_text, max_words_per_chunk=60, inter_sentence_pause=0.20)

        s_audio = AudioSegment.empty()
        for ch in chunks:
            if ch.get("type") == "pause":
                p_ms = int(ch.get("pause_sec", 0.20) * 1000)
                if p_ms > 0:
                    s_audio += AudioSegment.silent(duration=p_ms, frame_rate=44100).set_channels(2)
                continue

            c_text = ch.get("text", "").strip()
            if not c_text:
                continue

            c_seg, _ = render_chunk_vitts(
                model, c_text, voice,
                temperature=temp, speed=speed, pitch=pitch,
                cache_dir=cache_tts_dir, use_cache=False, max_chars=768
            )
            s_audio += trim_segment_silence(c_seg).set_frame_rate(44100).set_channels(2)

        # Khoảng nghỉ nhẹ 200ms giữa các câu để nhịp kể tự nhiên
        if s_idx < len(story_sentences) - 1:
            s_audio += AudioSegment.silent(duration=200, frame_rate=44100).set_channels(2)

        sent_audio_segments.append(s_audio)
        full_audio += s_audio

    # Chuẩn hóa âm lượng EBU R128 (-16 LUFS voice standard)
    master_voice = apply_voice_standard(full_audio).set_frame_rate(44100).set_channels(2)
    voice_dest = work_proj_dir / "voiceover.wav"
    master_voice.export(str(voice_dest), format="wav")
    total_audio_sec = round(len(master_voice) / 1000.0, 3)
    ok(f"Đã tạo file thoại liền mạch duy nhất: {total_audio_sec}s")

    # 3. ĐỒNG BỘ MỐC THỜI GIAN TỪNG TỪ THEO TỪ GỐC NGUYÊN BẢN (KHÔNG DÙNG WHISPER TRANSCRIBE)
    step("Đồng bộ mốc thời gian từng từ theo từ gốc nguyên bản của kịch bản...")
    cum_time = 0.0
    timeline_sentences = []
    all_final_words = []
    img_dir = day_dir / "images"

    for s_idx, sent_info in enumerate(story_sentences):
        s_dur = round(len(sent_audio_segments[s_idx]) / 1000.0, 3)
        s_start = round(cum_time, 3)
        s_end = round(cum_time + s_dur, 3)
        cum_time = s_end

        # Nội suy mốc thời gian từng từ chính xác theo từ gốc nguyên bản
        s_words = interpolate_sentence_words(sent_info["text"], s_start, s_end)
        all_final_words.extend(s_words)

        # Chuẩn bị ảnh và thông số lia cho câu
        assigned_images = []
        img_names = sent_info["images"]
        n_imgs = max(1, len(img_names))
        img_slice = s_dur / n_imgs

        for im_idx, im_name in enumerate(img_names):
            im_path = str(img_dir / im_name)
            src_url = paths.file_url(im_path)
            im_start = round(s_start + im_idx * img_slice, 3)
            im_end = s_end if im_idx == n_imgs - 1 else round(im_start + img_slice, 3)
            im_dur = round(max(0.1, im_end - im_start), 3)

            im_credit = IMG_CREDITS_MAP.get(im_name, sent_info["credit"])
            pan_info = compute_pan_params(im_path, duration=im_dur, dir_toggle=(im_idx % 2 == 1))
            assigned_images.append({
                "src": src_url,
                "file_url": src_url,
                "path": im_path,
                "name": im_name,
                "credit": im_credit,
                "start": im_start,
                "end": im_end,
                "duration": im_dur,
                **pan_info
            })

        timeline_sentences.append({
            "sentence_id": s_idx + 1,
            "text": sent_info["text"],
            "start": s_start,
            "end": s_end,
            "duration": s_dur,
            "layout": "full",
            "is_title": False,  # Tiêu đề cố định trên thanh #fixed-headline-bar
            "item_title": "BIẾN ĐỘNG BĂNG GHẾ HLV: MAN UTD HỖN LOẠN, MOURINHO LẬP KỶ LỤC",
            "item_group": sent_info["group"],
            "news_source": sent_info["news_source"],
            "credit": sent_info["credit"],
            "keywords": ["Man Utd", "Mauricio Pochettino", "Michael Carrick", "Jose Mourinho", "Pep Guardiola", "Park Hang-seo", "Old Trafford", "La Liga"],
            "images": assigned_images
        })

    # Gom nhóm phụ đề Karaoke thông minh (không bẻ đôi từ ghép)
    smart_chunks = build_smart_karaoke_chunks(all_final_words, target_size=4)

    # 4. XUẤT TIMELINE VÀ WORD TIMESTAMPS
    timeline_data = {
        "title": "BIẾN ĐỘNG BĂNG GHẾ HLV: MAN UTD HỖN LOẠN, MOURINHO LẬP KỶ LỤC",
        "group": "TÂM ĐIỂM NGÔI SAO THẾ GIỚI",
        "channel_name": "ĐIỂM ĐỌC",
        "hide_date_chip": False,
        "total_duration": total_audio_sec,
        "format": "9:16",
        "template": "short_news_v2.html",
        "dimensions": {"width": 1080, "height": 1920},
        "fps": 30,
        "audio_path": paths.file_url(str(voice_dest)),
        "news_source": "THE ATHLETIC / LA LIGA / BANGKOK POST",
        "credit": "REUTERS / AFP / AP PHOTO / THANH NIÊN",
        "global_offset_sec": 0.0,
        "sentences": timeline_sentences,
        "karaoke_chunks": smart_chunks
    }

    words_output_data = {
        "words": all_final_words,
        "karaoke_chunks": smart_chunks
    }

    tl_path = work_proj_dir / "video_timeline.json"
    words_path = work_proj_dir / "word_timestamps.json"

    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline_data, f, ensure_ascii=False, indent=2)

    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words_output_data, f, ensure_ascii=False, indent=2)

    ok(f"Đã lưu timeline liền mạch: {tl_path}")

    # 5. RENDER VIDEO QUA HTML V2 ENGINE (PLAYWRIGHT + GSAP)
    short_base_name = "Short_05_Bien_Dong_Ghe_HLV_Man_Utd_Mourinho_Thay_Park"
    out_final_mp4 = shorts_dir / f"{short_base_name}.mp4"

    step("Render video 9:16 liền mạch bằng engine HTML v2...")
    out_video_work = render_html_engine(
        project_dir=str(work_proj_dir),
        template="short_news_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True
    )

    if not out_video_work or not os.path.exists(out_video_work):
        die("Render HTML v2 thất bại!")

    # 6. KIỂM TRA ĐỘ LỆCH VIDEO-AUDIO
    step("Kiểm tra và chuẩn hóa độ lệch Video-Audio...")
    out_main_mp4 = shorts_dir / f"{short_base_name}_main.mp4"
    shutil.copy2(out_video_work, str(out_main_mp4))

    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "stream=duration,codec_type",
        "-of", "json", str(out_main_mp4)
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    pdata = json.loads(res.stdout)
    v_dur = next(float(s["duration"]) for s in pdata.get("streams", []) if s["codec_type"] == "video")
    a_dur = next(float(s["duration"]) for s in pdata.get("streams", []) if s["codec_type"] == "audio")
    drift_ms = abs(v_dur - a_dur) * 1000.0
    ok(f"Độ lệch A/V phần thân: {drift_ms:.2f} ms (Video: {v_dur:.2f}s, Audio: {a_dur:.2f}s)")

    # 7. GHÉP OUTRO 9:16 TƯƠNG PHẢN (OUTRO NỮ CYBER PULSE)
    step("Ghép Outro 9:16 tạo tương phản...")
    shutil.copy2(str(out_main_mp4), str(out_final_mp4))
    append_short_outro(out_final_mp4, voice_hint="primary")

    if out_main_mp4.exists():
        out_main_mp4.unlink()

    # Kiểm tra thời lượng video cuối cùng
    res_final = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", str(out_final_mp4)
    ], capture_output=True, text=True)
    final_dur = float(json.loads(res_final.stdout)["format"]["duration"])
    ok(f"Tổng thời lượng video thành phẩm (gồm Outro): {final_dur:.2f}s ({int(final_dur//60)}p {final_dur%60:.2f}s)")

    # 8. TẠO THUMBNAIL DỌC 9:16 CYBER-STADIUM
    step("Tạo Thumbnail dọc 9:16 chuẩn thương hiệu...")
    out_thumb = shorts_dir / f"{short_base_name}_thumbnail.jpg"
    thumb_img_cand = day_dir / "images" / "Tin_11_1.jpg"
    if not thumb_img_cand.exists():
        thumb_img_cand = day_dir / "images" / "Tin_08_1.jpg"

    thumb_success = render_thumbnail_9x16(
        out_path=out_thumb,
        image_path=thumb_img_cand,
        kicker="ĐIỂM ĐỌC THỂ THAO",
        hero_html="BIẾN ĐỘNG<br><span style='color:#00E5FF'>GHẾ HUẤN LUYỆN</span>",
        subtitle="MAN UTD SA THẢI CARRICK · MOURINHO PHÁ KỶ LỤC PEP",
        badge="TÂM ĐIỂM BÓNG ĐÁ",
        tag_a="ĐIỆN ẢNH THỂ THAO",
        tag_b="CHUẨN 1080P",
        hero_size="100px"
    )
    if thumb_success and out_thumb.exists():
        ok(f"Ảnh bìa 9:16 đã render: {out_thumb.name} ({out_thumb.stat().st_size // 1024} KB)")

    # 9. TẠO CONTACT SHEET QA
    step("Tạo Contact Sheet QA đối chứng ảnh...")
    qa_images = [
        {"path": str(day_dir / "images" / "Tin_08_3.jpg"), "name": "Tin_08_3.jpg", "credit": "REUTERS", "desc": "Michael Carrick chia tay Man Utd sau chuỗi bết bát"},
        {"path": str(day_dir / "images" / "Tin_11_1.jpg"), "name": "Tin_11_1.jpg", "credit": "AFP", "desc": "Jose Mourinho ngạo nghễ lập kỷ lục tại La Liga"},
        {"path": str(day_dir / "images" / "Tin_08_4.jpg"), "name": "Tin_08_4.jpg", "credit": "TALKSPORT", "desc": "Sir Jim Ratcliffe triệu tập họp khẩn tại Monaco"},
        {"path": str(day_dir / "images" / "Tin_08_6.jpg"), "name": "Tin_08_6.jpg", "credit": "REUTERS", "desc": "Carrick bất lực khi Man Utd rớt xuống nhóm đèn đỏ"},
        {"path": str(day_dir / "images" / "Tin_08_1.jpg"), "name": "Tin_08_1.jpg", "credit": "REUTERS", "desc": "Mauricio Pochettino đồng ý ngồi vào ghế nóng Man Utd"},
        {"path": str(day_dir / "images" / "Tin_08_12.jpg"), "name": "Tin_08_12.jpg", "credit": "REUTERS", "desc": "Bruno Fernandes hai lần từ chối gia hạn hợp đồng"},
        {"path": str(day_dir / "images" / "Tin_11_5.jpg"), "name": "Tin_11_5.jpg", "credit": "AFP", "desc": "Ký ức những trận El Clasico rực lửa Mourinho vs Pep"},
        {"path": str(day_dir / "images" / "Tin_11_6.jpg"), "name": "Tin_11_6.jpg", "credit": "AFP / REUTERS", "desc": "Tỷ lệ thắng 77% của Mourinho xô đổ 76,3% của Guardiola"},
        {"path": str(day_dir / "images" / "Tin_11_8.jpg"), "name": "Tin_11_8.jpg", "credit": "LA LIGA", "desc": "Mourinho nhận giải HLV xuất sắc nhất tháng 10"},
        {"path": str(day_dir / "images" / "Tin_11_9.jpg"), "name": "Tin_11_9.jpg", "credit": "AP PHOTO", "desc": "Chuỗi 8 trận toàn thắng giúp Real Madrid thăng hoa"},
        {"path": str(day_dir / "images" / "Tin_20_2.jpg"), "name": "Tin_20_2.jpg", "credit": "THANH NIÊN", "desc": "Thầy Park lao vào sân bảo vệ học trò bị lăng mạ"},
        {"path": str(day_dir / "images" / "Tin_20_6.jpg"), "name": "Tin_20_6.jpg", "credit": "BANGKOK POST", "desc": "Tiền đạo John Baggio bị miệt thị chủng tộc"},
        {"path": str(day_dir / "images" / "Tin_20_10.jpg"), "name": "Tin_20_10.jpg", "credit": "KANCHANABURI FC", "desc": "Cổ động viên ủng hộ hành động trượng nghĩa của thầy Park"},
        {"path": str(day_dir / "images" / "Tin_20_11.jpg"), "name": "Tin_20_11.jpg", "credit": "KANCHANABURI FC", "desc": "Kanchanaburi thắng 1-0 vươn lên vị trí thứ tư"}
    ]
    out_qa_contact = qa_dir / "contact_focus_05_bien_dong_hlv.jpg"
    create_qa_contact_sheet(qa_dir, qa_images, out_qa_contact)

    # 10. XUẤT FILE MÔ TẢ SEO YOUTUBE
    step("Xuất bản file mô tả SEO chuẩn quy chuẩn...")
    out_mota = shorts_dir / f"{short_base_name}_mota.txt"
    seo_title = "Biến động băng ghế HLV: Man Utd sa thải Carrick, Mourinho phá kỷ lục của Pep Guardiola #Shorts"
    desc_paragraphs = [
        "Những biến động rung chuyển băng ghế chỉ đạo bóng đá thế giới tuần qua:",
        "- Cơn hỗn loạn Old Trafford: Man Utd sa thải Michael Carrick trong cay đắng, chấp nhận chi 10 triệu USD giải phóng hợp đồng của Mauricio Pochettino trước đại chiến Liverpool giữa lúc Bruno Fernandes từ chối gia hạn.",
        "- Người Đặc Biệt đi vào lịch sử: Jose Mourinho chính thức xô đổ kỷ lục của đại kình địch Pep Guardiola với tỷ lệ thắng 77% tại La Liga sau chuỗi 8 trận thắng liên tiếp cùng Real Madrid.",
        "- Cái tâm của người thầy: HLV Park Hang-seo nhận án phạt cấm chỉ đạo hai trận tại Thái Lan vì lao vào sân bảo vệ học trò trước nạn phân biệt chủng tộc, rồi kiên cường dẫn dắt đội bóng lọt vào top 4."
    ]
    chapters = [
        ("00:00", "Biến động băng ghế chỉ đạo bóng đá thế giới"),
        ("00:07", "Man Utd sa thải Carrick và chiêu mộ Pochettino"),
        ("00:23", "Jose Mourinho xô đổ kỷ lục tỷ lệ thắng của Pep Guardiola"),
        ("00:37", "HLV Park Hang-seo nhận án phạt vì bảo vệ học trò")
    ]
    sources_line = "📰 Nguồn tin: VnExpress, The Athletic, La Liga, Reuters, Bangkok Post, Dân Trí, Thanh Niên, Kanchanaburi FC."
    hashtags = [
        "#Shorts", "#ManUtd", "#Pochettino", "#Carrick", "#JoseMourinho",
        "#PepGuardiola", "#ParkHangSeo", "#RealMadrid", "#DiemDoc", "#DiemDocTheThao"
    ]

    write_mota_9x16(
        out_path=out_mota,
        seo_title=seo_title,
        description_paragraphs=desc_paragraphs,
        chapters=chapters,
        sources_line=sources_line,
        hashtags=hashtags
    )
    ok(f"Đã xuất file mô tả SEO: {out_mota.name}")

    banner("HOÀN THÀNH XUẤT BẢN SHORT 5 BẢN LIỀN MẠCH", "ALL SUCCESS")
    print(f"  🎬 Video:     {out_final_mp4}")
    print(f"  🖼️ Thumbnail: {out_thumb}")
    print(f"  📝 Mô tả:     {out_mota}")
    print(f"  📋 QA Sheet:  {out_qa_contact}")


if __name__ == "__main__":
    main()
