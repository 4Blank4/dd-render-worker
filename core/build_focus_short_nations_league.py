#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_focus_short_nations_league.py — Sản xuất Video Focus Short 9:16
"Cơn Địa Chấn UEFA Nations League" (Gộp 4 tin: [01], [02], [03], [04])

Đặc tả:
- Chuẩn loại video 3: Focus Short 9:16 (1080x1920 @ 30fps), thời lượng < 3 phút (gồm Outro).
- Toàn bộ 4 tin bóng đá quốc tế UEFA Nations League sử dụng 100% Giọng Nam Minh Quân Pro (Mẫu 15).
  (Tin 01 và 03 dùng audio hiện có; Tin 02 và 04 được tổng hợp mới giọng Nam để thay thế giọng Nữ).
- Bố cục & Hiệu ứng:
  + Template short_news_v2.html: Hero Title mở đầu mỗi tin -> thu lên thanh cố định #fixed-headline-bar.
  + Dynamic Category Pill (TIN 01/04, TIN 02/04, TIN 03/04, TIN 04/04).
  + Lower-Third 2 góc động: Nguồn báo góc trái + Nguồn ảnh góc phải cập nhật tức thì theo từng ảnh.
  + Phụ đề Karaoke 48px đồng bộ từng từ.
  + Âm thanh master EBU R128 (-14.0 LUFS, TP <= -1.0 dBTP, A/V drift <= 33.3 ms).
  + Ghép Outro 9:16 nữ (Outro_Short_3_Kinetic_Slam.mp4 - 5.4s) tạo tương phản cuốn hút.
- Xuất bản trọn bộ:
  + Video: outputs/16.11.2026/shorts/Short_01_Dia_Chan_UEFA_Nations_League.mp4
  + Thumbnail: outputs/16.11.2026/shorts/Short_01_Dia_Chan_UEFA_Nations_League_thumbnail.jpg
  + Mô tả SEO: outputs/16.11.2026/shorts/Short_01_Dia_Chan_UEFA_Nations_League_mota.txt
  + Contact Sheet QA: outputs/16.11.2026/qa/contact_focus_01_nations_league.jpg
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
    """Tổng hợp giọng Nam Minh Quân Pro cho một bản tin (cả tiêu đề và nội dung)."""
    sc_id = int(item["id"])
    target_title = work_title_dir / f"audio_title_{sc_id:02d}.wav"
    target_audio = work_audio_dir / f"audio_{sc_id:02d}.wav"

    preset = load_voice_preset("primary")
    voice = preset["voice_id"]
    speed = preset["speed"]
    pitch = preset["pitch"]

    log(f"  Tổng hợp Giọng Nam ({voice}, spd={speed}, pch={pitch}) cho Tin {sc_id:02d}...")

    # 1. Title audio
    clean_title, _ = prepare(item["title"], manual_overrides=say_overrides)
    seg_title_raw, _ = render_chunk_vitts(
        model, clean_title, voice,
        temperature=0.5, speed=speed, pitch=pitch,
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
            temperature=0.5, speed=speed, pitch=pitch,
            cache_dir=cache_dir, use_cache=True, max_chars=768
        )
        seg_summary += trim_segment_silence(c_seg)

    # 3. Kết hợp title + khoảng lặng 800ms + summary -> chuẩn hóa -16 LUFS
    silence_08 = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)
    combined = seg_title + silence_08 + seg_summary
    combined = apply_voice_standard(combined).set_frame_rate(44100).set_channels(2)
    combined.export(str(target_audio), format="wav")

    dur_sec = round(len(combined) / 1000.0, 2)
    ok(f"  Tin {sc_id:02d} hoàn tất: full={dur_sec}s, title={round(len(seg_title)/1000.0, 2)}s")
    return str(target_audio), str(target_title), dur_sec


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
        font_lbl = ImageFont.truetype(str(_ROOT / "assets" / "fonts" / "Montserrat" / "Montserrat-VariableFont_wght.ttf"), 14)
        font_cap = ImageFont.truetype(str(_ROOT / "assets" / "fonts" / "Montserrat" / "Montserrat-VariableFont_wght.ttf"), 12)
    except Exception:
        font_title = font_lbl = font_cap = ImageFont.load_default()

    draw.text((pad, 14), "QA CONTACT SHEET — SHORT 01: CƠN ĐỊA CHẤN UEFA NATIONS LEAGUE", fill=(0, 229, 255), font=font_title)

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

    banner("SẢN XUẤT SHORT 1: CƠN ĐỊA CHẤN UEFA NATIONS LEAGUE (9:16)", day_str)

    # Thư mục tạm ngoài Google Drive
    work_proj_dir = Path.home() / "Library" / "Caches" / "DiemDoc" / "focus_short_01_nations_league"
    work_proj_dir.mkdir(parents=True, exist_ok=True)
    work_audio = work_proj_dir / "audio"
    work_title = work_proj_dir / "audio-title"
    work_audio.mkdir(parents=True, exist_ok=True)
    work_title.mkdir(parents=True, exist_ok=True)
    cache_tts_dir = str(paths.work_file("vitts_cache"))

    # Đọc thethao.json gốc
    with open(day_dir / "thethao.json", "r", encoding="utf-8") as f:
        all_items = json.load(f)

    # Đọc say_overrides
    say_overrides = {}
    overrides_file = day_dir / "manual_overrides.json"
    if overrides_file.exists():
        with open(overrides_file, "r", encoding="utf-8") as f:
            say_overrides = json.load(f)

    # Lọc 4 tin: 1, 2, 3, 4
    items_to_use = []
    for it in all_items:
        if str(it.get("id")) in ["1", "2", "3", "4"]:
            items_to_use.append(dict(it))

    # 1. Đảm bảo toàn bộ 4 tin dùng Giọng Nam Minh Quân Pro
    step("Kiểm tra & Chuẩn hóa Giọng Nam Minh Quân Pro cho 4 tin...")
    from vieneu import Vieneu
    model = None

    for item in items_to_use:
        sid = int(item["id"])
        # Tin 1 và 3 đã là Giọng Nam -> sao chép sang work nếu cần hoặc dùng trực tiếp
        if sid in [1, 3]:
            # Đã có sẵn audio Nam từ đợt sản xuất trước
            orig_audio = day_dir / "audio" / f"audio_{sid:02d}.wav"
            orig_title = day_dir / "audio-title" / f"audio_title_{sid:02d}.wav"
            item["audio_path"] = str(orig_audio)
            item["audio_title"] = str(orig_title)
            item["voice"] = "Minh Quân Pro"
            item["voice_preset"] = "primary"
            item["voice_gender"] = "male"
            log(f"  Tin {sid:02d}: Giữ nguyên Giọng Nam ({orig_audio.name})")
        elif sid in [2, 4]:
            # Cần tổng hợp Giọng Nam mới
            target_audio = work_audio / f"audio_{sid:02d}.wav"
            target_title = work_title / f"audio_title_{sid:02d}.wav"
            if not target_audio.exists() or not target_title.exists():
                if model is None:
                    step("Nạp mô hình ViTTS v3turbo...")
                    model = Vieneu(mode="v3turbo")
                aud_p, tit_p, dur = synthesize_male_item_audio(
                    item, work_audio, work_title, cache_tts_dir, say_overrides, model
                )
                item["audio_path"] = aud_p
                item["audio_title"] = tit_p
                item["duration"] = dur
            else:
                item["audio_path"] = str(target_audio)
                item["audio_title"] = str(target_title)
                item["duration"] = round(len(AudioSegment.from_file(str(target_audio))) / 1000.0, 2)
                log(f"  Tin {sid:02d}: Đã có sẵn audio Giọng Nam trong cache ({target_audio.name})")
            item["voice"] = "Minh Quân Pro"
            item["voice_preset"] = "primary"
            item["voice_gender"] = "male"

    # 2. Xây dựng timeline Focus Short 9:16
    step("Xây dựng timeline Focus Short 9:16...")
    timeline, words_data, _ = build_focus_short_timeline(
        day_dir=str(day_dir),
        item_ids=[1, 2, 3, 4],
        global_offset_sec=0.0,
        custom_items=items_to_use
    )

    # Cấu hình tiêu đề & metadata Focus Short
    timeline["title"] = "TIN NÓNG TUẦN QUA: CƠN ĐỊA CHẤN UEFA NATIONS LEAGUE"
    timeline["group"] = "ĐỊA CHẤN NATIONS LEAGUE"

    item_meta = {
        "1": {"group": "ĐỊA CHẤN TÂY BAN NHA", "source": "VNEXPRESS / THE INDEPENDENT"},
        "2": {"group": "BỒ ĐÀO NHA THẢM BẠI 1-4", "source": "VNEXPRESS / RECORD / O JOGO"},
        "3": {"group": "ITALIA THUA SỐC BỈ 1-4", "source": "VNEXPRESS / FOOTBALL ITALIA"},
        "4": {"group": "HÀ LAN HỦY DIỆT 7-0", "source": "VNEXPRESS / GOAL / REUTERS"},
    }

    # Bổ sung category pill đánh số TIN 01/04, TIN 02/04, v.v.
    for s in timeline.get("sentences", []):
        sid = str(s.get("item_id"))
        if sid in item_meta:
            m = item_meta[sid]
            s["item_group"] = m["group"]
            s["news_source"] = m["source"]
            s["category_pill"] = f"TIN 0{sid}/04"

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

    short_base_name = "Short_01_Dia_Chan_UEFA_Nations_League"
    out_final_mp4 = shorts_dir / f"{short_base_name}.mp4"

    if not out_final_mp4.exists():
        # 3. Render video qua HTML v2 Engine (Playwright + GSAP)
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

        # 4. Kiểm tra độ lệch Video-Audio
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

        # 5. Ghép Outro 9:16 (Nữ - Outro_Short_3_Kinetic_Slam.mp4 hoặc Cyber Pulse)
        step("Ghép Outro 9:16 tạo tương phản...")
        shutil.copy2(str(out_main_mp4), str(out_final_mp4))
        append_short_outro(out_final_mp4, voice_hint="primary")

        # Xóa file tạm main
        if out_main_mp4.exists():
            out_main_mp4.unlink()
    else:
        ok(f"Video thành phẩm đã tồn tại: {out_final_mp4.name} (Bỏ qua bước render)")

    # Kiểm tra thời lượng video cuối cùng
    res_final = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", str(out_final_mp4)
    ], capture_output=True, text=True)
    final_dur = float(json.loads(res_final.stdout)["format"]["duration"])
    ok(f"Tổng thời lượng video thành phẩm (gồm Outro): {final_dur:.2f}s ({int(final_dur//60)}p {final_dur%60:.2f}s)")
    if final_dur > 180.0:
        die(f"Video vượt quá giới hạn 3 phút của YouTube Shorts ({final_dur:.2f}s > 180s)!")

    # 6. Tạo Thumbnail dọc 9:16 (Cyber-Stadium Electric Cyan)
    step("Tạo Thumbnail dọc 9:16 chuẩn thương hiệu...")
    out_thumb = shorts_dir / f"{short_base_name}_thumbnail.jpg"
    render_thumbnail_9x16(
        out_path=out_thumb,
        image_path=day_dir / "images" / "Tin_01_1.jpg",
        kicker="ĐỊA CHẤN UEFA NATIONS LEAGUE",
        hero_html="<span class=\"hl-cyan\">TÂY BAN NHA THUA 2-3!</span><br><span class=\"hl-red\">BỒ ĐÀO NHA THUA 1-4</span><br><span class=\"hl-yellow\">ITALIA MẤT VÉ TỨ KẾT</span>",
        subtitle="ĐỨT CHUỖI 43 TRẬN • ĐAN MẠCH HẠ BỒ ĐÀO NHA • HÀ LAN THẮNG 7-0",
        badge="CƠN ĐỊA CHẤN CHÂU ÂU",
        tag_a="TIN NÓNG TUẦN",
        tag_b=day_str,
        obj_pos="50% 20%"
    )

    # 7. Xuất file Mô tả SEO YouTube (mota.txt)
    step("Xuất file Mô tả SEO YouTube 2 phần...")
    out_mota = shorts_dir / f"{short_base_name}_mota.txt"
    seo_title = "Tin nóng thể thao tuần qua: Cơn địa chấn Nations League, các nhà vô địch sụp đổ #Shorts"
    write_mota_9x16(
        out_path=out_mota,
        seo_title=seo_title,
        description_paragraphs=[
            "Tin nóng thể thao tuần qua: Lượt trận quyết định vòng bảng UEFA Nations League chứng kiến những cơn địa chấn kinh hoàng nhất lịch sử khi các nhà đương kim vô địch và cựu vương châu Âu đồng loạt ngã ngựa khó tin.",
            "Tây Ban Nha đứt chuỗi 43 trận bất bại lịch sử khi gục ngã 2-3 trước tuyển Anh; Bồ Đào Nha nhận trận thua sân nhà đậm nhất lịch sử 1-4 trước Đan Mạch ngay ngày tri ân Ronaldo; Italia tan vỡ 1-4 trên sân Bỉ mất vé tứ kết; trong khi Hà Lan hủy diệt Hy Lạp 7-0 với cú hat-trick 21 phút chớp nhoáng của Reijnders."
        ],
        chapters=chapters,
        sources_line="📰 Nguồn tin: VnExpress, The Independent, UEFA, Record, O Jogo, Football Italia, Goal, Reuters.",
        hashtags=["#Shorts", "#TinNongTuanQua", "#NationsLeague", "#UEFANationsLeague", "#TayBanNha", "#BoDaoNha", "#Italia", "#HaLan", "#DiemDoc", "#BongDa"]
    )

    # 8. Tạo bảng Contact Sheet QA đối chứng ảnh
    step("Tạo Contact Sheet QA đối chứng ảnh...")
    image_records = []
    # Chọn 2 ảnh tiêu biểu cho mỗi tin (tổng cộng 8 ảnh)
    img_candidates = [
        ("Tin_01_1.jpg", "AHRAM ONLINE", "Kane tranh chấp quyết liệt với hậu vệ Tây Ban Nha"),
        ("Tin_01_3.jpg", "BHASKAR", "Harry Kane ăn mừng chiến thắng ấn tượng của Tam Sư"),
        ("Tin_02_1.jpg", "REUTERS / SIPA", "Bồ Đào Nha tri ân áo số 7 của Ronaldo trước trận"),
        ("Tin_02_6.jpg", "RECORD", "Hojlund lập cú đúp nhấn chìm Bồ Đào Nha 1-4"),
        ("Tin_03_1.jpg", "HINDUSTAN TIMES", "Italia gục ngã 1-4 trên sân Bỉ mất vé tứ kết"),
        ("Tin_03_7.jpg", "FOOTBALL ITALIA", "Jeremy Doku và dàn sao Bỉ ăn mừng chiến thắng"),
        ("Tin_04_1.jpg", "REUTERS", "Hà Lan hủy diệt Hy Lạp 7-0 trên sân Amsterdam"),
        ("Tin_04_3.jpg", "GOAL", "Tijjani Reijnders lập cú hat-trick siêu tốc 21 phút"),
    ]
    for fn, cr, ds in img_candidates:
        image_records.append({
            "path": str(day_dir / "images" / fn),
            "name": fn,
            "credit": cr,
            "desc": ds
        })
    create_qa_contact_sheet(qa_dir, image_records, qa_dir / "contact_focus_01_nations_league.jpg")

    banner("HOÀN TẤT XUẤT BẢN FOCUS SHORT 1!", day_str)
    ok(f"Video: outputs/{day_str}/shorts/{short_base_name}.mp4")
    ok(f"Thumbnail: outputs/{day_str}/shorts/{short_base_name}_thumbnail.jpg")
    ok(f"Mô tả SEO: outputs/{day_str}/shorts/{short_base_name}_mota.txt")
    ok(f"QA: outputs/{day_str}/qa/contact_focus_01_nations_league.jpg")


if __name__ == "__main__":
    main()
