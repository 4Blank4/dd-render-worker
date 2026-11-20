#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_focus_short_south_america_nightmare.py — Sản xuất Video Focus Short 3 (9:16)
"Đêm Ác Mộng Của Bóng Đá Nam Mỹ: Brazil Gục Ngã, Argentina Hoang Mang"
(BẢN LIỀN MẠCH — UNIFIED SEAMLESS NARRATIVE)

Quy chuẩn kỹ thuật:
1. Liền mạch 100% nội dung (Unified Storytelling Narrative):
   - Kịch bản dẫn chuyện một mạch từ đầu đến cuối không chia vụn tin, không Hero Title ở giữa.
   - Thanh tiêu đề cố định (#fixed-headline-bar) hiển thị trang nhã trên đỉnh khung hình.
2. An toàn từ ngữ & Subtitle Karaoke:
   - Dùng 100% từ gốc nguyên bản của kịch bản (interpolate_sentence_words), tuyệt đối không lấy text từ Whisper.
   - Không tự ý phiên âm, giữ nguyên tên riêng quốc tế (Lionel Messi, La Bombonera, Uruguay, Carlo Ancelotti, Vinicius Junior, Romario, Raphinha, Sakamoto...).
   - Gom cụm phụ đề thông minh (3-5 từ), không bẻ đôi từ ghép tiếng Việt.
3. Phân bổ hình ảnh động:
   - 15 ảnh hiện trường HD lia ngang (Pan) mượt mà bám sát từng câu.
   - Lower-Third 2 góc động: Nguồn bài viết bên trái + Nguồn ảnh bên phải đổi tức thời theo từng ảnh.
4. Thời lượng: ~54s audio + 5.4s Outro = ~60s (chuẩn YouTube Shorts).
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
    tuyệt đối không bẻ đôi các từ ghép (như 'khổng lồ', 'thất bại', 'kỷ nguyên', 'bỏ trống'...).
    """
    if not words_data:
        return []

    no_end_words = {
        "đầy", "nhưng", "và", "của", "trong", "khi", "với", "ở", "tại", "lên", "cho",
        "bị", "được", "vừa", "lại", "gã", "khổng", "thất", "kỷ", "bỏ", "nhà", "chiếc",
        "áo", "đội", "khối", "đoàn", "huấn", "luyện", "thủ", "huyền", "làn", "sóng",
        "hồi", "ngai"
    }
    no_start_words = {
        "lồ", "bại", "nguyên", "trống", "quân", "viên", "thành", "trưởng", "thoại", "chuông", "vàng", "đỏ", "thép", "đúp"
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

    draw.text((pad, 16), "BẢNG ĐỐI CHỨNG HÌNH ẢNH — SHORT 3: ĐÊM ÁC MỘNG BÓNG ĐÁ NAM MỸ", fill=(0, 229, 255), font=font_title)

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

    banner("SẢN XUẤT SHORT 3 (BẢN LIỀN MẠCH): ĐÊM ÁC MỘNG CỦA BÓNG ĐÁ NAM MỸ (9:16)", day_str)

    work_proj_dir = Path.home() / "Library" / "Caches" / "DiemDoc" / "focus_short_03_south_america"
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
        "Tin_05_1.jpg": "PERFIL",
        "Tin_05_2.jpg": "HEADOUT",
        "Tin_05_3.jpg": "REUTERS",
        "Tin_05_4.jpg": "REUTERS",
        "Tin_05_7.jpg": "PROKERALA",
        "Tin_05_9.jpg": "PROKERALA",
        "Tin_05_11.jpg": "SABC SPORT",
        "Tin_06_1.jpg": "AP PHOTO / VNEXPRESS",
        "Tin_06_4.jpg": "REUTERS",
        "Tin_06_5.jpg": "AP PHOTO",
        "Tin_06_6.jpg": "REUTERS",
        "Tin_06_7.jpg": "AP PHOTO",
        "Tin_06_8.jpg": "AP PHOTO",
        "Tin_06_9.jpg": "AP PHOTO",
        "Tin_06_10.jpg": "VNEXPRESS"
    }

    # 1. KỊCH BẢN DẪN CHUYỆN LIỀN MẠCH DUY NHẤT (7 CÂU — UNIFIED STORYTELLING NARRATIVE)
    story_sentences = [
        {
            "id": 1,
            "text": "Chuyện gì đang xảy ra với hai gã khổng lồ Nam Mỹ? Chỉ trong 48 giờ, cả Argentina lẫn Brazil đều nếm mùi thất bại cay đắng.",
            "group": "ĐỊA CHẤN NAM MỸ",
            "news_source": "SKY SPORTS / REUTERS",
            "credit": "REUTERS / AP PHOTO",
            "images": ["Tin_05_4.jpg", "Tin_06_5.jpg"]
        },
        {
            "id": 2,
            "text": "Tại thánh địa La Bombonera, Argentina bước vào kỷ nguyên hậu Lionel Messi với chiếc áo số 10 huyền thoại được bỏ trống để tri ân.",
            "group": "KỶ NGUYÊN HẬU MESSI",
            "news_source": "SKY SPORTS / PERFIL",
            "credit": "PERFIL / REUTERS",
            "images": ["Tin_05_2.jpg", "Tin_05_3.jpg"]
        },
        {
            "id": 3,
            "text": "Dù kiểm soát bóng 72 phần trăm và dứt điểm 17 lần, đoàn quân của Scaloni hoàn toàn bế tắc trước khối phòng ngự thép của Uruguay, nhận thất bại cay đắng 1-2.",
            "group": "BẾ TẮC LA BOMBONERA",
            "news_source": "VNEXPRESS / REUTERS",
            "credit": "SABC SPORT / PROKERALA",
            "images": ["Tin_05_11.jpg", "Tin_05_7.jpg", "Tin_05_9.jpg"]
        },
        {
            "id": 4,
            "text": "Cơn địa chấn chưa dừng lại ở đó khi Brazil của Carlo Ancelotti nếm trải đêm ác mộng tồi tệ trước đội tuyển Nhật Bản tại Singapore.",
            "group": "CÚ SỐC SELECAO",
            "news_source": "AP PHOTO / VNEXPRESS",
            "credit": "REUTERS / AP PHOTO",
            "images": ["Tin_06_4.jpg", "Tin_06_6.jpg"]
        },
        {
            "id": 5,
            "text": "Dù Vinicius Junior lập cú đúp san bằng tỷ số 2-2, nhát kiếm cận thành ở phút bù giờ của Sakamoto đã nhấn chìm Selecao trong cay đắng.",
            "group": "ĐỊA CHẤN PHÚT BÙ GIỜ",
            "news_source": "AP PHOTO / REUTERS",
            "credit": "AP PHOTO",
            "images": ["Tin_06_7.jpg", "Tin_06_8.jpg"]
        },
        {
            "id": 6,
            "text": "Sự ức chế khiến Carlo Ancelotti và thủ quân Raphinha cùng nhận thẻ đỏ trực tiếp, thổi bùng làn sóng giận dữ khi huyền thoại Romario lập tức yêu cầu sa thải.",
            "group": "HỖN LOẠN & THẺ ĐỎ",
            "news_source": "AP PHOTO / VNEXPRESS",
            "credit": "AP PHOTO / VNEXPRESS",
            "images": ["Tin_06_9.jpg", "Tin_06_10.jpg"]
        },
        {
            "id": 7,
            "text": "Thất bại liên tiếp của hai tượng đài vĩ đại đang gióng lên hồi chuông cảnh báo lớn: liệu ngai vàng của bóng đá Nam Mỹ có còn vững chắc trước ngày hội bóng đá lớn nhất hành tinh?",
            "group": "HỒI CHUÔNG CẢNH BÁO",
            "news_source": "VNEXPRESS / REUTERS",
            "credit": "PERFIL / AP PHOTO",
            "images": ["Tin_05_1.jpg", "Tin_06_1.jpg"]
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
            "item_title": "ĐÊM ÁC MỘNG NAM MỸ: BRAZIL VÀ ARGENTINA GỤC NGÃ",
            "item_group": sent_info["group"],
            "news_source": sent_info["news_source"],
            "credit": sent_info["credit"],
            "keywords": ["Argentina", "Brazil", "Lionel Messi", "Carlo Ancelotti", "Vinicius Junior", "Uruguay", "Nhật Bản", "Romario", "Raphinha"],
            "images": assigned_images
        })

    # Gom nhóm phụ đề Karaoke thông minh (không bẻ đôi từ ghép)
    smart_chunks = build_smart_karaoke_chunks(all_final_words, target_size=4)

    # 4. XUẤT TIMELINE VÀ WORD TIMESTAMPS
    timeline_data = {
        "title": "ĐÊM ÁC MỘNG NAM MỸ: BRAZIL VÀ ARGENTINA GỤC NGÃ",
        "group": "ĐỊA CHẤN BÓNG ĐÁ NAM MỸ",
        "channel_name": "ĐIỂM ĐỌC",
        "hide_date_chip": False,
        "total_duration": total_audio_sec,
        "format": "9:16",
        "template": "short_news_v2.html",
        "dimensions": {"width": 1080, "height": 1920},
        "fps": 30,
        "audio_path": paths.file_url(str(voice_dest)),
        "news_source": "SKY SPORTS / AP PHOTO / REUTERS",
        "credit": "REUTERS / AP PHOTO / PERFIL",
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
    short_base_name = "Short_03_Dem_Ac_Mong_Nam_My_Brazil_Argentina"
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
    thumb_img_cand = day_dir / "images" / "Tin_06_1.jpg"
    if not thumb_img_cand.exists():
        thumb_img_cand = day_dir / "images" / "Tin_05_3.jpg"

    thumb_success = render_thumbnail_9x16(
        out_path=out_thumb,
        image_path=thumb_img_cand,
        kicker="ĐIỂM ĐỌC THỂ THAO",
        hero_html="ĐÊM ÁC MỘNG<br><span style='color:#00E5FF'>BÓNG ĐÁ NAM MỸ</span>",
        subtitle="BRAZIL THUA NGƯỢC PHÚT 90+1 · ARGENTINA BẾ TẮC VẮNG MESSI",
        badge="CÚ SỐC LỊCH SỬ",
        tag_a="ĐỊA CHẤN QUỐC TẾ",
        tag_b="CHUẨN 1080P",
        hero_size="105px"
    )
    if thumb_success and out_thumb.exists():
        ok(f"Ảnh bìa 9:16 đã render: {out_thumb.name} ({out_thumb.stat().st_size // 1024} KB)")

    # 9. TẠO CONTACT SHEET QA
    step("Tạo Contact Sheet QA đối chứng ảnh...")
    qa_images = [
        {"path": str(day_dir / "images" / "Tin_05_4.jpg"), "name": "Tin_05_4.jpg", "credit": "REUTERS", "desc": "Argentina kỷ nguyên không còn Lionel Messi"},
        {"path": str(day_dir / "images" / "Tin_05_2.jpg"), "name": "Tin_05_2.jpg", "credit": "HEADOUT", "desc": "Chảo lửa La Bombonera rực sáng"},
        {"path": str(day_dir / "images" / "Tin_05_3.jpg"), "name": "Tin_05_3.jpg", "credit": "REUTERS", "desc": "Chiếc áo số 10 của Messi được bỏ trống tri ân"},
        {"path": str(day_dir / "images" / "Tin_05_11.jpg"), "name": "Tin_05_11.jpg", "credit": "SABC SPORT", "desc": "Diego Forlan xây khối phòng ngự thép cho Uruguay"},
        {"path": str(day_dir / "images" / "Tin_05_7.jpg"), "name": "Tin_05_7.jpg", "credit": "PROKERALA", "desc": "Julian Alvarez ghi bàn rút ngắn 1-2"},
        {"path": str(day_dir / "images" / "Tin_05_9.jpg"), "name": "Tin_05_9.jpg", "credit": "PROKERALA", "desc": "HLV Scaloni bất lực bên đường biên"},
        {"path": str(day_dir / "images" / "Tin_06_5.jpg"), "name": "Tin_06_5.jpg", "credit": "AP PHOTO", "desc": "Brazil chơi thiếu thuyết phục"},
        {"path": str(day_dir / "images" / "Tin_06_4.jpg"), "name": "Tin_06_4.jpg", "credit": "REUTERS", "desc": "Sân Quốc gia Singapore chứng kiến màn so tài"},
        {"path": str(day_dir / "images" / "Tin_06_6.jpg"), "name": "Tin_06_6.jpg", "credit": "REUTERS", "desc": "Kubo và Nakamura giúp Nhật Bản dẫn sớm 2-0"},
        {"path": str(day_dir / "images" / "Tin_06_7.jpg"), "name": "Tin_06_7.jpg", "credit": "AP PHOTO", "desc": "Vinicius Junior lập cú đúp gỡ hòa 2-2"},
        {"path": str(day_dir / "images" / "Tin_06_8.jpg"), "name": "Tin_06_8.jpg", "credit": "AP PHOTO", "desc": "Sakamoto ghi bàn cận thành phút bù giờ 90+1"},
        {"path": str(day_dir / "images" / "Tin_06_9.jpg"), "name": "Tin_06_9.jpg", "credit": "AP PHOTO", "desc": "Raphinha và Ancelotti nhận thẻ đỏ trực tiếp"},
        {"path": str(day_dir / "images" / "Tin_06_10.jpg"), "name": "Tin_06_10.jpg", "credit": "VNEXPRESS", "desc": "Huyền thoại Romario gay gắt đòi sa thải Ancelotti"},
        {"path": str(day_dir / "images" / "Tin_05_1.jpg"), "name": "Tin_05_1.jpg", "credit": "PERFIL", "desc": "Pha tranh chấp quyết liệt Argentina - Uruguay"},
        {"path": str(day_dir / "images" / "Tin_06_1.jpg"), "name": "Tin_06_1.jpg", "credit": "AP PHOTO / VNEXPRESS", "desc": "Ancelotti bức xúc trước thất bại cay đắng"}
    ]
    out_qa_contact = qa_dir / "contact_focus_03_dem_ac_mong_nam_my.jpg"
    create_qa_contact_sheet(qa_dir, qa_images, out_qa_contact)

    # 10. XUẤT FILE MÔ TẢ SEO YOUTUBE
    step("Xuất bản file mô tả SEO chuẩn quy chuẩn...")
    out_mota = shorts_dir / f"{short_base_name}_mota.txt"
    seo_title = "Đêm ác mộng của bóng đá Nam Mỹ: Brazil gục ngã phút bù giờ, Argentina bế tắc vắng Messi #Shorts"
    desc_paragraphs = [
        "Chỉ trong vòng 48 giờ, cả hai gã khổng lồ của bóng đá Nam Mỹ đồng loạt nếm mùi thất bại cay đắng nhất năm 2026:",
        "- Cơn ác mộng La Bombonera: Trong trận đầu tiên kỷ nguyên hậu Lionel Messi với áo số 10 bỏ trống, Argentina kiểm soát bóng 72% nhưng bất lực trước Uruguay của Diego Forlan và gục ngã 1-2.",
        "- Địa chấn Singapore: Brazil dẫn bàn rồi bị Nhật Bản lội ngược dòng 3-2 ở phút bù giờ 90+1 dù Vinicius Junior lập cú đúp.",
        "- Hỗn loạn & Thẻ đỏ: HLV Carlo Ancelotti và thủ quân Raphinha nhận thẻ đỏ trực tiếp, thổi bùng làn sóng giận dữ khi huyền thoại Romario gay gắt đòi sa thải."
    ]
    chapters = [
        ("00:00", "Địa chấn bóng đá Nam Mỹ trong 48 giờ"),
        ("00:08", "Argentina kỷ nguyên hậu Messi gục ngã trước Uruguay"),
        ("00:24", "Brazil thua ngược Nhật Bản 2-3 ở phút bù giờ"),
        ("00:41", "HLV Ancelotti nhận thẻ đỏ và làn sóng đòi sa thải")
    ]
    sources_line = "📰 Nguồn tin: Sky Sports, Reuters, AP Photo, VnExpress, Dân Trí, Perfil, SABC Sport, Headout, Prokerala."
    hashtags = [
        "#Shorts", "#Brazil", "#Argentina", "#LionelMessi", "#ViniciusJunior",
        "#CarloAncelotti", "#Uruguay", "#NhatBan", "#DiemDoc", "#DiemDocTheThao"
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

    banner("HOÀN THÀNH XUẤT BẢN SHORT 3 BẢN LIỀN MẠCH", "ALL SUCCESS")
    print(f"  🎬 Video:     {out_final_mp4}")
    print(f"  🖼️ Thumbnail: {out_thumb}")
    print(f"  📝 Mô tả:     {out_mota}")
    print(f"  📋 QA Sheet:  {out_qa_contact}")


if __name__ == "__main__":
    main()
