#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_focus_short_generation_war_seamless.py — Sản xuất Video Focus Short 9:16
"Cuộc Chiến Thế Hệ: Messi, Lamine Yamal Và Sự Cay Đắng Của Harry Kane"
(BẢN LIỀN MẠCH — UNIFIED SEAMLESS NARRATIVE)

Nâng cấp cốt lõi (Cập nhật theo yêu cầu người dùng):
1. Liền mạch 100% nội dung (Seamless Narrative):
   - Thay vì chia thành 4 mẩu tin rời rạc, ngắt quãng bởi 4 lần đọc tiêu đề + khoảng lặng 0.8s + whoosh SFX,
     toàn bộ video chạy một mạch câu chuyện duy nhất từ đầu đến cuối (54s + Outro).
   - Thanh tiêu đề cố định (#fixed-headline-bar) hiển thị trang nhã, ổn định ở đỉnh khung hình.
2. Định hình lại âm thanh giọng đọc TTS (Zero Awkward Breaks):
   - Soạn thảo văn phong liền mạch, nhịp điệu tự nhiên, loại bỏ các cấu trúc ngữ pháp gây ngắt nhịp sai (như hiểu nhầm "hoặc" trong "mê hoặc").
   - Giọng Nam Minh Quân Pro Mẫu 15 (spd 1.12, pch 0.93) dẫn liền một mạch không đứt đoạn.
3. Gom cụm phụ đề thông minh (Smart Semantic Karaoke Chunks):
   - Thay thế việc cắt cứng mỗi 4 từ bằng thuật toán ngữ nghĩa (3-5 từ/cụm),
     tuyệt đối không bẻ đôi các từ ghép (như "chuyển giao", "thế hệ", "thần đồng", "kỷ lục", "Quả bóng vàng"...).
4. Phân bổ hình ảnh động:
   - Lia ảnh toàn cảnh (Pan) mượt mà bám sát từng chuyển động của câu chuyện: Harry Kane -> Messi -> Cubarsi -> Yamal.
   - Lower-Third 2 góc động cập nhật nguồn báo & nguồn ảnh tức thời.
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
from m8_news_bridge import interpolate_sentence_words

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "core"))
sys.path.insert(1, str(_ROOT / "engines" / "html"))

from vieneu import Vieneu
from diemdoc import paths
from diemdoc.log import banner, ok, step, log, die, warn
from diemdoc.audio import apply_voice_standard
from diemdoc.publisher import load_voice_preset, render_thumbnail_9x16, write_mota_9x16
from diemdoc.short_outro import append_short_outro
from diemdoc.tts_text import prepare
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from m8_news_bridge import compute_pan_params
from renderer import render_html_engine


def build_smart_karaoke_chunks(words_data: List[Dict[str, Any]], target_size: int = 4) -> List[Dict[str, Any]]:
    """
    Gom nhóm từ hiển thị thành các cụm Karaoke 3-5 từ tự nhiên,
    tuyệt đối không bẻ đôi các từ ghép (như 'mê hoặc', 'chuyển giao', 'thế hệ', 'thần đồng'...).
    """
    if not words_data:
        return []

    no_end_words = {
        "đầy", "nhưng", "và", "của", "trong", "khi", "với", "ở", "tại", "lên", "cho",
        "bị", "được", "vừa", "lại", "mê", "chuyển", "thế", "thần", "vô", "kỷ", "bóng",
        "quốc", "tâm", "đỉnh", "cậu", "bé", "trung"
    }
    no_start_words = {
        "hoặc", "giao", "hệ", "đồng", "hậu", "lục", "đá", "gia", "chấn", "điểm", "vàng", "vệ", "non", "tranh"
    }

    chunks = []
    i = 0
    n = len(words_data)

    while i < n:
        # Dự kiến kích thước cụm từ target_size (4 từ)
        size = target_size
        if i + size > n:
            size = n - i
        else:
            # Kiểm tra xem từ cuối cụm có nằm trong danh sách không được đứng cuối không
            last_w = words_data[i + size - 1]["word"].lower().strip(".,!?:;")
            if last_w in no_end_words and (i + size) < n:
                size += 1
            elif (i + size) < n:
                next_w = words_data[i + size]["word"].lower().strip(".,!?:;")
                if next_w in no_start_words:
                    size += 1

            # Đảm bảo phần còn lại không bị mồ côi 1 từ
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
    cw = pad + cols * (card_w + pad)
    ch = pad + rows * (card_h + pad) + 60

    canvas = Image.new("RGB", (cw, ch), (10, 15, 25))
    draw = ImageDraw.Draw(canvas)

    try:
        font_title = ImageFont.truetype(str(_ROOT / "assets" / "fonts" / "Be_Vietnam_Pro" / "BeVietnamPro-Bold.ttf"), 30)
        font_lbl = ImageFont.truetype(str(_ROOT / "assets" / "fonts" / "Montserrat" / "Montserrat-VariableFont_wght.ttf"), 17)
        font_cap = ImageFont.truetype(str(_ROOT / "assets" / "fonts" / "Montserrat" / "Montserrat-VariableFont_wght.ttf"), 14)
    except Exception:
        font_title = font_lbl = font_cap = ImageFont.load_default()

    draw.text((pad, 14), "QA CONTACT SHEET — SHORT 02: CUỘC CHIẾN THẾ HỆ (BẢN LIỀN MẠCH)", fill=(0, 229, 255), font=font_title)

    for i, rec in enumerate(image_records):
        r = i // cols
        c = i % cols
        x0 = pad + c * (card_w + pad)
        y0 = 60 + pad + r * (card_h + pad)

        draw.rectangle([x0, y0, x0 + card_w, y0 + card_h], fill=(16, 24, 40), outline=(30, 41, 59), width=1)

        img_path = rec["path"]
        orig_size = "N/A"
        if os.path.exists(img_path):
            try:
                im = Image.open(img_path).convert("RGB")
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

    banner("SẢN XUẤT SHORT 2 (BẢN LIỀN MẠCH): CUỘC CHIẾN THẾ HỆ — MESSI, YAMAL VÀ HARRY KANE (9:16)", day_str)

    work_proj_dir = Path.home() / "Library" / "Caches" / "DiemDoc" / "focus_short_02_seamless"
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

    # 1. KỊCH BẢN DẪN CHUYỆN LIỀN MẠCH DUY NHẤT (7 CÂU — UNIFIED STORYTELLING NARRATIVE)
    story_sentences = [
        {
            "id": 1,
            "text": "Một tuần lễ đầy nghịch lý và cay đắng của Harry Kane.",
            "group": "KỶ LỤC GIA TAM SƯ",
            "news_source": "VNEXPRESS / UEFA",
            "credit": "REUTERS",
            "images": ["Tin_07_1.jpg"]
        },
        {
            "id": 2,
            "text": "Vừa lập đại công xô đổ kỷ lục 126 trận tồn tại 36 năm của tuyển Anh, chủ nhân Quả bóng vàng lại bất ngờ bị gạch tên khỏi đội hình xuất sắc nhất năm FIFPRO trước sự trỗi dậy của Erling Haaland.",
            "group": "KỶ LỤC GIA TAM SƯ",
            "news_source": "VNEXPRESS / FIFPRO",
            "credit": "UEFA / GETTY IMAGES",
            "images": ["Tin_07_7.jpg", "Tin_09_7.jpg"]
        },
        {
            "id": 3,
            "text": "Trong khi Kane ngậm ngùi đứng ngoài, tượng đài Lionel Messi ở tuổi 39 tiếp tục khiến cả thế giới ngả mũ khi nâng kỷ lục vô tiền khoáng hậu lên 18 lần góp mặt trong đội hình xuất sắc nhất hành tinh, bỏ xa con số 15 lần của Cristiano Ronaldo.",
            "group": "TƯỢNG ĐÀI BẤT TỬ",
            "news_source": "VNEXPRESS / FIFPRO",
            "credit": "REUTERS / FIFPRO",
            "images": ["Tin_09_1.jpg", "Tin_09_4.jpg"]
        },
        {
            "id": 4,
            "text": "Thế nhưng, tâm chấn bóng đá lúc này đang thuộc về thế hệ măng non của Barcelona.",
            "group": "THẾ HỆ MĂNG NON",
            "news_source": "VNEXPRESS / TUTTOSPORT",
            "credit": "REUTERS",
            "images": ["Tin_10_5.jpg"]
        },
        {
            "id": 5,
            "text": "Trung vệ 19 tuổi Pau Cubarsi vừa chính thức ẵm danh hiệu Cậu bé Vàng Golden Boy 2026 sau cú đúp vô địch La Liga và World Cup, giúp lò La Masia độc chiếm kỷ lục 5 lần thống trị giải thưởng danh giá.",
            "group": "CẬU BÉ VÀNG 2026",
            "news_source": "VNEXPRESS / TUTTOSPORT",
            "credit": "TUTTOSPORT / REUTERS",
            "images": ["Tin_10_1.jpg", "Tin_10_3.jpg"]
        },
        {
            "id": 6,
            "text": "Đỉnh điểm tranh cãi bùng nổ khi huyền thoại Steven Gerrard khẳng định Lamine Yamal ở tuổi 19 thậm chí vượt trội hơn cả Messi và Ronaldo thời trẻ.",
            "group": "TRANH LUẬN LỊCH SỬ",
            "news_source": "VNEXPRESS / THE OVERLAP",
            "credit": "THE OVERLAP / GETTY IMAGES",
            "images": ["Tin_12_1.jpg", "Tin_12_3.jpg"]
        },
        {
            "id": 7,
            "text": "Với 142 lần in dấu giày vào bàn thắng và 8 danh hiệu lớn, thần đồng Tây Ban Nha đang tạo nên cuộc chuyển giao thế hệ tàn khốc nhưng đầy cuốn hút của bóng đá thế giới.",
            "group": "THẦN ĐỒNG THẾ GIỚI",
            "news_source": "VNEXPRESS / FC BARCELONA",
            "credit": "REUTERS / FC BARCELONA",
            "images": ["Tin_12_6.jpg", "Tin_12_2.jpg"]
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
            c_txt = ch.get("text", "").strip()
            if not c_txt:
                continue
            c_seg, _ = render_chunk_vitts(
                model, c_txt, voice,
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

    # 3. ĐỒNG BỘ MỐC THỜI GIAN TỪNG TỪ VÀ TỪNG CÂU THEO TỪ GỐC NGUYÊN BẢN (KHÔNG PHIÊN ÂM WHISPER)
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

        # Sử dụng chính xác từ gốc của kịch bản để tránh lỗi Whisper tự phiên âm từ ngoại quốc (như FIFPRO -> F -E -F -V)
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

            pan_info = compute_pan_params(im_path, duration=im_dur, dir_toggle=(im_idx % 2 == 1))
            assigned_images.append({
                "src": src_url,
                "file_url": src_url,
                "path": im_path,
                "name": im_name,
                "credit": sent_info["credit"],
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
            "is_title": False,  # KHÔNG hiển thị Hero Title ngắt quãng
            "item_title": "CUỘC CHIẾN THẾ HỆ: MESSI, YAMAL VÀ HARRY KANE",
            "item_group": sent_info["group"],
            "news_source": sent_info["news_source"],
            "credit": sent_info["credit"],
            "keywords": ["Harry Kane", "Lionel Messi", "Pau Cubarsi", "Lamine Yamal", "Golden Boy", "FIFPRO"],
            "images": assigned_images
        })

    # Gom nhóm phụ đề Karaoke thông minh (không bẻ đôi từ ghép)
    smart_chunks = build_smart_karaoke_chunks(all_final_words, target_size=4)

    # 4. XUẤT TIMELINE VÀ WORD TIMESTAMPS
    timeline_data = {
        "title": "CUỘC CHIẾN THẾ HỆ: MESSI, YAMAL VÀ HARRY KANE",
        "group": "TÂM ĐIỂM NGÔI SAO THẾ GIỚI",
        "channel_name": "ĐIỂM ĐỌC THỂ THAO",
        "hide_date_chip": True,
        "total_duration": total_audio_sec,
        "format": "9:16",
        "template": "short_news_v2.html",
        "dimensions": [1080, 1920],
        "fps": 30,
        "audio_path": str(voice_dest),
        "news_source": "VNEXPRESS / UEFA / FIFPRO / THE OVERLAP",
        "credit": "REUTERS / GETTY IMAGES / FC BARCELONA",
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
    short_base_name = "Short_02_Cuoc_Chien_The_He_Messi_Yamal_Kane"
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
    thumb_img_cand = day_dir / "images" / "Tin_09_1.jpg"
    if not thumb_img_cand.exists():
        thumb_img_cand = day_dir / "images" / "Tin_12_1.jpg"

    thumb_success = render_thumbnail_9x16(
        out_path=out_thumb,
        image_path=thumb_img_cand,
        kicker="ĐIỂM ĐỌC THỂ THAO",
        hero_html="CUỘC CHIẾN<br><span style='color:#00E5FF'>THẾ HỆ</span>",
        subtitle="MESSI KỶ LỤC 18 LẦN · LAMINE YAMAL · KANE BỊ LOẠI",
        badge="TRANH LUẬN LỊCH SỬ",
        tag_a="ĐỈNH CAO THẾ GIỚI",
        tag_b="CHUẨN 1080P",
        hero_size="105px"
    )
    if thumb_success and out_thumb.exists():
        ok(f"Ảnh bìa 9:16 đã render: {out_thumb.name} ({out_thumb.stat().st_size // 1024} KB)")

    # 9. TẠO CONTACT SHEET QA
    step("Tạo Contact Sheet QA đối chứng ảnh...")
    qa_images = [
        {"path": str(day_dir / "images" / "Tin_07_1.jpg"), "name": "Tin_07_1.jpg", "credit": "REUTERS", "desc": "Harry Kane nhận kỷ vật kỷ lục 126 trận"},
        {"path": str(day_dir / "images" / "Tin_07_7.jpg"), "name": "Tin_07_7.jpg", "credit": "UEFA", "desc": "Harry Kane ghi bàn thắng quyết định vào lưới Croatia"},
        {"path": str(day_dir / "images" / "Tin_09_1.jpg"), "name": "Tin_09_1.jpg", "credit": "REUTERS", "desc": "Lionel Messi lập kỷ lục 18 lần vào FIFPRO World 11"},
        {"path": str(day_dir / "images" / "Tin_09_4.jpg"), "name": "Tin_09_4.jpg", "credit": "FIFPRO", "desc": "Đội hình tiêu biểu thế giới FIFPRO World 11 năm 2026"},
        {"path": str(day_dir / "images" / "Tin_09_7.jpg"), "name": "Tin_09_7.jpg", "credit": "GETTY IMAGES", "desc": "Erling Haaland vượt qua Kane trong cuộc bình chọn"},
        {"path": str(day_dir / "images" / "Tin_10_1.jpg"), "name": "Tin_10_1.jpg", "credit": "TUTTOSPORT", "desc": "Pau Cubarsi rạng rỡ với cúp Golden Boy 2026"},
        {"path": str(day_dir / "images" / "Tin_10_5.jpg"), "name": "Tin_10_5.jpg", "credit": "REUTERS", "desc": "Pau Cubarsi thi đấu chắc chắn tại World Cup 2026"},
        {"path": str(day_dir / "images" / "Tin_12_1.jpg"), "name": "Tin_12_1.jpg", "credit": "THE OVERLAP", "desc": "Steven Gerrard nhận định về Lamine Yamal"},
        {"path": str(day_dir / "images" / "Tin_12_3.jpg"), "name": "Tin_12_3.jpg", "credit": "GETTY IMAGES", "desc": "Lamine Yamal đi bóng tốc độ trong màu áo Barca"},
        {"path": str(day_dir / "images" / "Tin_12_6.jpg"), "name": "Tin_12_6.jpg", "credit": "FC BARCELONA", "desc": "Lamine Yamal ăn mừng cúp vô địch đỉnh cao"}
    ]
    out_qa_contact = qa_dir / "contact_focus_02_cuoc_chien_the_he.jpg"
    create_qa_contact_sheet(qa_dir, qa_images, out_qa_contact)

    # 10. XUẤT FILE MÔ TẢ SEO YOUTUBE
    step("Xuất bản file mô tả SEO chuẩn quy chuẩn...")
    out_mota = shorts_dir / f"{short_base_name}_mota.txt"
    seo_title = "Cuộc chiến thế hệ: Messi lập kỷ lục, Lamine Yamal bùng nổ và sự cay đắng của Harry Kane #Shorts"
    desc_paragraphs = [
        "Cuộc chuyển giao thế hệ tàn khốc nhưng đầy cuốn hút của bóng đá thế giới:",
        "- Nghịch lý Harry Kane: Vừa xô đổ kỷ lục 126 trận cho tuyển Anh, chủ nhân Quả bóng vàng bất ngờ bị gạch tên khỏi FIFPRO World 11.",
        "- Tượng đài Lionel Messi: Ở tuổi 39 tiếp tục nối dài kỷ lục vô tiền khoáng hậu với lần thứ 18 góp mặt trong đội hình xuất sắc nhất hành tinh.",
        "- Cậu bé Vàng Pau Cubarsi: Trung vệ 19 tuổi của Barcelona ẵm trọn danh hiệu Golden Boy 2026 sau cú đúp La Liga và World Cup.",
        "- Tranh cãi Lamine Yamal: Steven Gerrard khẳng định thần đồng tuổi 19 xuất sắc hơn cả Messi và Ronaldo thời trẻ với 142 lần in dấu giày vào bàn thắng."
    ]
    chapters = [
        ("00:00", "Nghịch lý Harry Kane và sự trỗi dậy của Erling Haaland"),
        ("00:15", "Tượng đài Lionel Messi lập kỷ lục 18 lần vào World 11"),
        ("00:29", "Pau Cubarsi 19 tuổi giành danh hiệu Cậu bé Vàng 2026"),
        ("00:43", "Steven Gerrard và tranh cãi Lamine Yamal tuổi 19")
    ]
    sources_line = "📰 Nguồn tin: VnExpress, UEFA, FIFPRO, Tuttosport, The Overlap, Reuters, Getty Images, FC Barcelona."
    hashtags = [
        "#Shorts", "#Messi", "#LamineYamal", "#HarryKane", "#PauCubarsi",
        "#GoldenBoy", "#FIFPRO", "#Barcelona", "#DiemDoc", "#DiemDocTheThao"
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

    banner("HOÀN THÀNH XUẤT BẢN SHORT 2 BẢN LIỀN MẠCH", "ALL SUCCESS")
    print(f"  🎬 Video:     {out_final_mp4}")
    print(f"  🖼️ Thumbnail: {out_thumb}")
    print(f"  📝 Mô tả:     {out_mota}")
    print(f"  📋 QA Sheet:  {out_qa_contact}")


if __name__ == "__main__":
    main()
