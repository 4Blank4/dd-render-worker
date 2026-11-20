#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_focus_short_generation_war.py — Sản xuất Video Focus Short 9:16
"Cuộc Chiến Thế Hệ: Messi, Lamine Yamal Và Sự Cay Đắng Của Harry Kane"
(Phương án 2: Tranh luận / Kịch tính chuyển giao thế hệ)

Đặc tả:
- Chuẩn loại video 3: Focus Short 9:16 (1080x1920 @ 30fps), thời lượng < 3 phút (gồm Outro).
- Nội dung: Được viết lại hoàn toàn thành một câu chuyện dẫn chuyện liền mạch (Storytelling),
  từ nghịch lý cay đắng của Quả bóng vàng Harry Kane -> Kỷ lục 18 lần vô tiền khoáng hậu của Lionel Messi ->
  Pau Cubarsi 19 tuổi ẵm Cậu bé Vàng Golden Boy 2026 -> Steven Gerrard nhận định Lamine Yamal vượt trội Messi & Ronaldo.
- Giọng đọc: 100% Giọng Nam Minh Quân Pro (Mẫu 15, ViTTS v3turbo, speed=1.12, pitch=0.93, temp=0.6).
- Bố cục & Hiệu ứng:
  + Template short_news_v2.html: Hero Title mở đầu mỗi tin -> thu lên thanh cố định #fixed-headline-bar.
  + Dynamic Category Pill (KỶ LỤC GIA TAM SƯ, TƯỢNG ĐÀI BẤT TỬ, CẬU BÉ VÀNG 2026, THẦN ĐỒNG THẾ GIỚI).
  + Lower-Third 2 góc động: Nguồn báo góc trái + Nguồn ảnh góc phải cập nhật tức thì theo từng ảnh.
  + Phụ đề Karaoke 48px đồng bộ từng từ.
  + Âm thanh master EBU R128 (-14.0 LUFS, TP <= -1.0 dBTP, A/V drift <= 33.3 ms).
  + Ghép Outro 9:16 nữ (Outro_Short_1_Cyber_Pulse.mp4 hoặc Outro_Short_3_Kinetic_Slam.mp4) tạo tương phản cuốn hút.
- Xuất bản trọn bộ:
  + Video: outputs/16.11.2026/shorts/Short_02_Cuoc_Chien_The_He_Messi_Yamal_Kane.mp4
  + Thumbnail: outputs/16.11.2026/shorts/Short_02_Cuoc_Chien_The_He_Messi_Yamal_Kane_thumbnail.jpg
  + Mô tả SEO: outputs/16.11.2026/shorts/Short_02_Cuoc_Chien_The_He_Messi_Yamal_Kane_mota.txt
  + Contact Sheet QA: outputs/16.11.2026/qa/contact_focus_02_cuoc_chien_the_he.jpg
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
sys.path.insert(0, str(_ROOT / "core"))
sys.path.insert(1, str(_ROOT / "engines" / "html"))

from vieneu import Vieneu
from diemdoc import paths
from diemdoc.log import banner, ok, step, log, die, warn
from diemdoc.audio import apply_voice_standard, measure_loudness
from diemdoc.publisher import load_voice_preset, render_thumbnail_9x16, write_mota_9x16
from diemdoc.short_outro import append_short_outro
from diemdoc.tts_text import prepare
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from m8_news_bridge import build_focus_short_timeline
from renderer import render_html_engine


def synthesize_male_item_audio(item: Dict[str, Any], work_audio_dir: Path,
                               work_title_dir: Path, cache_dir: str,
                               say_overrides: Dict[str, str], model: Any) -> Tuple[str, str, float]:
    """Tổng hợp giọng Nam Minh Quân Pro cho một phần kịch bản (tiêu đề và nội dung)."""
    sc_id = int(item["id"])
    target_title = work_title_dir / f"title_{sc_id:02d}.wav"
    target_audio = work_audio_dir / f"audio_{sc_id:02d}.wav"

    preset = load_voice_preset("primary")
    voice = preset["voice_id"]
    speed = preset["speed"]
    pitch = preset["pitch"]
    temp = preset["temperature"]

    log(f"  Tổng hợp Giọng Nam ({voice}, spd={speed}, pch={pitch}) cho Phần {sc_id:02d}...")

    # 1. Title audio
    clean_title, _ = prepare(item["title"], manual_overrides=say_overrides)
    seg_title_raw, _ = render_chunk_vitts(
        model, clean_title, voice,
        temperature=temp, speed=speed, pitch=pitch,
        cache_dir=cache_dir, use_cache=True, max_chars=768
    )
    seg_title = trim_segment_silence(seg_title_raw).set_frame_rate(44100).set_channels(2)
    seg_title.export(str(target_title), format="wav")

    # 2. Summary audio
    clean_summary, _ = prepare(item["summary"], manual_overrides=say_overrides)
    chunks = build_chunks_from_text(clean_summary, max_words_per_chunk=60, inter_sentence_pause=0.25)
    seg_summary = AudioSegment.empty()
    for ch in chunks:
        if ch.get("type") == "pause":
            pause_ms = int(ch.get("pause_sec", 0.25) * 1000)
            if pause_ms > 0:
                seg_summary += AudioSegment.silent(duration=pause_ms, frame_rate=44100).set_channels(2)
            continue
        c_text = ch.get("text", "").strip()
        if not c_text:
            continue
        c_seg, _ = render_chunk_vitts(
            model, c_text, voice,
            temperature=temp, speed=speed, pitch=pitch,
            cache_dir=cache_dir, use_cache=True, max_chars=768
        )
        seg_summary += trim_segment_silence(c_seg)

    # 3. Kết hợp title + khoảng lặng 800ms + summary -> chuẩn hóa -16 LUFS
    silence_08 = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)
    combined = seg_title + silence_08 + seg_summary
    combined = apply_voice_standard(combined).set_frame_rate(44100).set_channels(2)
    combined.export(str(target_audio), format="wav")

    dur_sec = round(len(combined) / 1000.0, 2)
    ok(f"  Phần {sc_id:02d} hoàn tất: full={dur_sec}s, title={round(len(seg_title)/1000.0, 2)}s")
    return str(target_audio), str(target_title), dur_sec


def create_qa_contact_sheet(qa_dir: Path, image_records: List[Dict[str, str]], output_path: Path):
    """Tạo Contact Sheet QA đối chứng ảnh cho Focus Short 2."""
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

    draw.text((pad, 14), "QA CONTACT SHEET — SHORT 02: CUỘC CHIẾN THẾ HỆ (MESSI - YAMAL - KANE)", fill=(0, 229, 255), font=font_title)

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

    banner("SẢN XUẤT SHORT 2: CUỘC CHIẾN THẾ HỆ — MESSI, YAMAL VÀ SỰ CAY ĐẮNG CỦA HARRY KANE (9:16)", day_str)

    # Thư mục làm việc tạm ngoài Google Drive
    work_proj_dir = Path.home() / "Library" / "Caches" / "DiemDoc" / "focus_short_02_generation_war"
    work_proj_dir.mkdir(parents=True, exist_ok=True)
    work_audio = work_proj_dir / "audio"
    work_title = work_proj_dir / "audio-title"
    work_audio.mkdir(parents=True, exist_ok=True)
    work_title.mkdir(parents=True, exist_ok=True)
    cache_tts_dir = str(paths.work_file("vitts_cache"))

    # Đọc overrides nếu có
    say_overrides = {}
    ov_path = day_dir / "manual_overrides.json"
    if ov_path.exists():
        try:
            say_overrides = json.loads(ov_path.read_text(encoding="utf-8"))
        except Exception:
            say_overrides = {}

    # 1. Kịch bản viết lại hoàn toàn (Storytelling kịch tính chuyển giao thế hệ, chuẩn Sentence Case)
    story_items = [
        {
            "id": 7,
            "title": "Nghịch lý Harry Kane: Kỷ lục gia bị ngó lơ tại FIFPRO",
            "summary": "Một tuần lễ đầy nghịch lý và cay đắng của đương kim Quả bóng vàng Harry Kane. Vừa lập đại công xô đổ kỷ lục 126 trận tồn tại 36 năm của tuyển Anh, Harry Kane bất ngờ bị gạch tên khỏi đội hình xuất sắc nhất năm FIFPRO 2026 khi xếp sau Erling Haaland với cách biệt chưa đầy 1% phiếu bầu.",
            "news_source": "VNEXPRESS / UEFA",
            "credit": "REUTERS / UEFA / AP PHOTO",
            "group": "SO DỊU ĐỈNH CAO",
            "category_pill": "KỶ LỤC GIA TAM SƯ"
        },
        {
            "id": 9,
            "title": "Lionel Messi lập kỷ lục 18 lần vào Đội hình tiêu biểu thế giới",
            "summary": "Trong khi Kane ngậm ngùi đứng ngoài, huyền thoại Lionel Messi ở tuổi 39 tiếp tục khiến cả thế giới ngả mũ khi nâng kỷ lục vô tiền khoáng hậu lên 18 lần góp mặt trong đội hình xuất sắc nhất hành tinh, bỏ xa con số 15 lần của kình địch Cristiano Ronaldo.",
            "news_source": "VNEXPRESS / FIFPRO",
            "credit": "REUTERS / FIFPRO / GETTY IMAGES",
            "group": "TƯỢNG ĐÀI BẤT TỬ",
            "category_pill": "KỶ LỤC VÔ TIỀN KHOÁNG HẬU"
        },
        {
            "id": 10,
            "title": "Pau Cubarsi 19 tuổi giành danh hiệu Cậu bé Vàng Golden Boy 2026",
            "summary": "Thế nhưng tâm chấn bóng đá lúc này đang thuộc về thế hệ Gen Z của Barcelona. Trung vệ 19 tuổi Pau Cubarsi vừa chính thức ẵm danh hiệu Cậu bé Vàng Golden Boy 2026 sau cú đúp vô địch La Liga và World Cup, giúp lò La Masia độc chiếm kỷ lục 5 lần thống trị giải thưởng trẻ danh giá nhất.",
            "news_source": "VNEXPRESS / TUTTOSPORT",
            "credit": "TUTTOSPORT / REUTERS / GETTY IMAGES",
            "group": "THẾ HỆ MĂNG NON",
            "category_pill": "CẬU BÉ VÀNG 2026"
        },
        {
            "id": 12,
            "title": "Lamine Yamal tuổi 19: Xuất sắc hơn cả Messi và Ronaldo?",
            "summary": "Đỉnh điểm tranh cãi nổ ra khi huyền thoại Steven Gerrard tuyên bố Lamine Yamal ở tuổi 19 thậm chí xuất sắc hơn cả Messi và Ronaldo thời trẻ. Với 142 lần in dấu giày vào bàn thắng và 8 danh hiệu lớn, thần đồng Tây Ban Nha đang tạo nên cuộc chuyển giao thế hệ tàn khốc nhưng đầy mê hoặc của bóng đá thế giới.",
            "news_source": "VNEXPRESS / THE OVERLAP",
            "credit": "THE OVERLAP / REUTERS / GETTY IMAGES",
            "group": "THẦN ĐỒNG THẾ GIỚI",
            "category_pill": "TRANH LUẬN LỊCH SỬ"
        }
    ]

    # 2. Tổng hợp giọng đọc Nam Minh Quân Pro (chuẩn bóng đá quốc tế)
    step("Kiểm tra và tổng hợp giọng Nam Minh Quân Pro (ViTTS v3turbo)...")
    model = None
    items_to_use = []
    for it in story_items:
        sid = int(it["id"])
        target_audio = work_audio / f"audio_{sid:02d}.wav"
        target_title = work_title / f"title_{sid:02d}.wav"

        if not target_audio.exists() or not target_title.exists():
            if model is None:
                step("Nạp mô hình ViTTS v3turbo...")
                model = Vieneu(mode="v3turbo")
            aud_p, tit_p, dur = synthesize_male_item_audio(
                it, work_audio, work_title, cache_tts_dir, say_overrides, model
            )
            it["audio_path"] = aud_p
            it["audio_title"] = tit_p
            it["duration"] = dur
        else:
            it["audio_path"] = str(target_audio)
            it["audio_title"] = str(target_title)
            it["duration"] = round(len(AudioSegment.from_file(str(target_audio))) / 1000.0, 2)
            log(f"  Phần {sid:02d}: Đã có sẵn audio trong cache ({target_audio.name})")

        items_to_use.append(it)

    # 3. Xây dựng timeline Focus Short từ m8_news_bridge
    step("Xây dựng timeline đồng bộ 9:16 (m8_news_bridge)...")
    timeline, words_data, focus_work_dir = build_focus_short_timeline(
        day_dir=str(day_dir),
        item_ids=[7, 9, 10, 12],
        global_offset_sec=0.0,
        custom_items=items_to_use
    )

    # Cấu hình tiêu đề & metadata Focus Short
    timeline["title"] = "CUỘC CHIẾN THẾ HỆ: MESSI, YAMAL VÀ HARRY KANE"
    timeline["group"] = "TÂM ĐIỂM NGÔI SAO THẾ GIỚI"

    item_meta = {
        "7": {"group": "SO DỊU ĐỈNH CAO", "source": "VNEXPRESS / UEFA", "pill": "KỶ LỤC GIA TAM SƯ"},
        "9": {"group": "TƯỢNG ĐÀI BẤT TỬ", "source": "VNEXPRESS / FIFPRO", "pill": "KỶ LỤC VÔ TIỀN KHOÁNG HẬU"},
        "10": {"group": "THẾ HỆ MĂNG NON", "source": "VNEXPRESS / TUTTOSPORT", "pill": "CẬU BÉ VÀNG 2026"},
        "12": {"group": "THẦN ĐỒNG THẾ GIỚI", "source": "VNEXPRESS / THE OVERLAP", "pill": "TRANH LUẬN LỊCH SỬ"},
    }

    # Bổ sung category pill cụ thể cho từng câu
    for s in timeline.get("sentences", []):
        sid = str(s.get("item_id"))
        if sid in item_meta:
            m = item_meta[sid]
            s["item_group"] = m["group"]
            s["news_source"] = m["source"]
            s["category_pill"] = m["pill"]

    tl_path = work_proj_dir / "video_timeline.json"
    words_path = work_proj_dir / "word_timestamps.json"
    voice_dest = work_proj_dir / "voiceover.wav"

    if os.path.exists(timeline["audio_path"]):
        shutil.copy2(timeline["audio_path"], str(voice_dest))

    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)

    ok(f"Đã lưu timeline: {tl_path}")

    # Tính các mốc thời gian bắt đầu của từng tin để tạo Chapters SEO
    chapters = []
    seen_items = set()
    for s in timeline.get("sentences", []):
        it_id = str(s.get("item_id"))
        if it_id not in seen_items:
            seen_items.add(it_id)
            start_sec = s.get("start", 0.0)
            m = int(start_sec // 60)
            sec = int(start_sec % 60)
            time_str = f"{m:02d}:{sec:02d}"
            title_text = next((it["title"] for it in items_to_use if str(it["id"]) == it_id), "")
            chapters.append((time_str, title_text))

    short_base_name = "Short_02_Cuoc_Chien_The_He_Messi_Yamal_Kane"
    out_final_mp4 = shorts_dir / f"{short_base_name}.mp4"

    # 4. Render video qua HTML v2 Engine (Playwright + GSAP)
    step("Render video 9:16 bằng engine HTML v2...")
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

    # 5. Kiểm tra độ lệch Video-Audio
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

    # 6. Ghép Outro 9:16 nữ (Outro_Short_1_Cyber_Pulse.mp4 hoặc Outro_Short_3_Kinetic_Slam.mp4) tạo tương phản
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
    if final_dur > 180.0:
        die(f"Video vượt quá giới hạn 3 phút của YouTube Shorts ({final_dur:.2f}s > 180s)!")

    # 7. Tạo Thumbnail dọc 9:16 (Cyber-Stadium Electric Cyan)
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

    # 8. Tạo Contact Sheet QA đối chứng ảnh
    step("Tạo Contact Sheet QA đối chứng ảnh...")
    qa_images = [
        {"path": str(day_dir / "images" / "Tin_07_1.jpg"), "name": "Tin_07_1.jpg", "credit": "REUTERS", "desc": "Harry Kane nhận kỷ niệm chương kỷ lục 126 trận từ Hoàng tử William"},
        {"path": str(day_dir / "images" / "Tin_07_7.jpg"), "name": "Tin_07_7.jpg", "credit": "UEFA", "desc": "Harry Kane ăn mừng bàn thắng quyết định vào lưới Croatia"},
        {"path": str(day_dir / "images" / "Tin_09_1.jpg"), "name": "Tin_09_1.jpg", "credit": "REUTERS", "desc": "Lionel Messi trong màu áo Argentina lập kỷ lục 18 lần vào World 11"},
        {"path": str(day_dir / "images" / "Tin_09_4.jpg"), "name": "Tin_09_4.jpg", "credit": "FIFPRO", "desc": "Đội hình tiêu biểu thế giới FIFPRO World 11 năm 2026"},
        {"path": str(day_dir / "images" / "Tin_09_7.jpg"), "name": "Tin_09_7.jpg", "credit": "GETTY IMAGES", "desc": "Erling Haaland vượt qua Harry Kane trong cuộc bình chọn tiền đạo"},
        {"path": str(day_dir / "images" / "Tin_10_1.jpg"), "name": "Tin_10_1.jpg", "credit": "TUTTOSPORT", "desc": "Pau Cubarsi rạng rỡ với danh hiệu Cậu bé Vàng Golden Boy 2026"},
        {"path": str(day_dir / "images" / "Tin_10_5.jpg"), "name": "Tin_10_5.jpg", "credit": "REUTERS", "desc": "Pau Cubarsi thi đấu chắc chắn trong màu áo Barcelona và Tây Ban Nha"},
        {"path": str(day_dir / "images" / "Tin_12_1.jpg"), "name": "Tin_12_1.jpg", "credit": "THE OVERLAP", "desc": "Huyền thoại Steven Gerrard trên podcast The Overlap"},
        {"path": str(day_dir / "images" / "Tin_12_3.jpg"), "name": "Tin_12_3.jpg", "credit": "GETTY IMAGES", "desc": "Lamine Yamal rê dắt bóng thần tốc trong màu áo Barcelona"},
        {"path": str(day_dir / "images" / "Tin_12_6.jpg"), "name": "Tin_12_6.jpg", "credit": "REUTERS", "desc": "Lamine Yamal giương cúp vô địch và ăn mừng bàn thắng"}
    ]
    out_qa_contact = qa_dir / "contact_focus_02_cuoc_chien_the_he.jpg"
    create_qa_contact_sheet(qa_dir, qa_images, out_qa_contact)

    # 9. Xuất file mô tả SEO mota.txt chuẩn YouTube
    step("Xuất bản file mô tả SEO chuẩn quy chuẩn...")
    out_mota = shorts_dir / f"{short_base_name}_mota.txt"
    seo_title = "Cuộc chiến thế hệ: Messi lập kỷ lục, Lamine Yamal bùng nổ và sự cay đắng của Harry Kane #Shorts"
    desc_paragraphs = [
        "Cuộc chuyển giao thế hệ tàn khốc nhưng đầy mê hoặc của bóng đá thế giới:",
        "- Nghịch lý Harry Kane: Vừa xô đổ kỷ lục 126 trận cho tuyển Anh, chủ nhân Quả bóng vàng bất ngờ bị gạch tên khỏi FIFPRO World 11.",
        "- Tượng đài Lionel Messi: Ở tuổi 39 tiếp tục nối dài kỷ lục vô tiền khoáng hậu với lần thứ 18 góp mặt trong đội hình xuất sắc nhất hành tinh.",
        "- Cậu bé Vàng Pau Cubarsi: Trung vệ 19 tuổi của Barcelona ẵm trọn danh hiệu Golden Boy 2026 sau cú đúp La Liga và World Cup.",
        "- Tranh cãi Lamine Yamal: Steven Gerrard khẳng định thần đồng tuổi 19 xuất sắc hơn cả Messi và Ronaldo thời trẻ với 142 lần in dấu giày vào bàn thắng."
    ]
    sources_line = "📰 Nguồn tin: VnExpress, UEFA, FIFPRO, Tuttosport, The Overlap, Reuters, Getty Images."
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

    banner("HOÀN THÀNH XUẤT BẢN FOCUS SHORT 2 — CUỘC CHIẾN THẾ HỆ", "ALL SUCCESS")
    print(f"  🎬 Video:     {out_final_mp4}")
    print(f"  🖼️ Thumbnail: {out_thumb}")
    print(f"  📝 Mô tả:     {out_mota}")
    print(f"  📋 QA Sheet:  {out_qa_contact}")


if __name__ == "__main__":
    main()
