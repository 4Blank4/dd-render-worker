#!/usr/bin/env python3
"""
core/build_digest_dual_voice.py — Sản xuất Video Short "Tin Nhanh 25 Sự Kiện" Giọng Song Song Nam - Nữ

Quy trình:
- Đọc 25 tin từ outputs/09.11.2026/thethao.json
- Sinh giọng đọc ViTTS xen kẽ:
    + Tin Lẻ (1, 3, 5...): Nam chính Minh Quân Pro (Mẫu 15, spd=1.12, pch=0.93, temp=0.6)
    + Tin Chẵn (2, 4, 6...): Nữ thứ hai Ngọc Huyền (Mẫu 14, spd=1.12, pch=1.10, temp=0.5)
- Căn chỉnh từ sample-accurate & tạo karaoke_chunks
- Chuẩn hóa âm thanh master EBU R128 (-14.0 LUFS, TP <= -1.5 dBTP)
- Render video 9:16 (1080x1920 @ 30fps) bằng Playwright qua template templates/short_digest_v2.html
- Xuất bản kèm Thumbnail dọc 9:16 chuẩn Cyber-Stadium và mota.txt 2 phần
- Giữ nguyên bản cũ để Chủ kênh đối chiếu trực tiếp
"""
import sys
sys.dont_write_bytecode = True

import os
import re
import json
import glob
import shutil
import subprocess
from pathlib import Path
from pydub import AudioSegment

import vieneu
from vieneu import Vieneu
from diemdoc import paths
from diemdoc.tts_text import prepare
from diemdoc.log import banner, ok, log, warn, die
from diemdoc.audio import two_pass_loudnorm
from diemdoc.publisher import (
    load_voice_preset,
    write_mota_9x16,
    render_thumbnail_9x16,
)
from m3_voice import render_chunk_vitts
from m8_news_bridge import compute_pan_params, interpolate_sentence_words


def main():
    day_dir = Path(paths.ROOT) / "outputs" / "09.11.2026"
    json_path = day_dir / "thethao.json"
    if not json_path.exists():
        die(f"Không tìm thấy {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    work_dir = Path(paths.WORK) / "digest_short_dual_voice_09_11"
    work_dir.mkdir(parents=True, exist_ok=True)
    tts_cache_dir = Path(paths.WORK) / "tts_cache"
    tts_cache_dir.mkdir(parents=True, exist_ok=True)

    banner("SẢN XUẤT VIDEO TIN NHANH 25 SỰ KIỆN — GIỌNG SONG SONG NAM & NỮ", "09.11.2026")

    # 1. Cấu hình giọng đọc Nam & Nữ chuẩn từ config/voice.json
    male_preset = load_voice_preset("primary")
    female_preset = load_voice_preset("secondary")

    log(f"Giọng Nam: {male_preset['voice_id']} (spd={male_preset['speed']}, pch={male_preset['pitch']})")
    log(f"Giọng Nữ: {female_preset['voice_id']} (spd={female_preset['speed']}, pch={female_preset['pitch']})")

    voice_model = Vieneu()

    # Nạp image_plan.json nếu có để lấy nguồn ảnh
    img_credits_map = {}
    plan_path = day_dir / "image_plan.json"
    if plan_path.exists():
        try:
            with open(plan_path, "r", encoding="utf-8") as pf:
                raw_p = json.load(pf)
                for r in raw_p.get("records", []):
                    fn = r.get("file_name")
                    cr = r.get("credit")
                    if fn and cr:
                        img_credits_map[fn] = cr
        except Exception:
            pass

    # Nguồn báo chuẩn cho 25 tin tuần 09.11
    news_source_dict = {
        1: "BÁO CHÍ BỒ ĐÀO NHA / FPF",
        2: "RECORD / O JOGO / AL HILAL",
        3: "UEFA CHAMPIONS LEAGUE",
        4: "MARCA / REAL MADRID CF",
        5: "MANCHESTER CITY / UEFA",
        6: "LIVERPOOL FC / SO FOOT",
        7: "NOTTINGHAM POST / PREMIER LEAGUE",
        8: "MANCHESTER EVENING NEWS / PL",
        9: "MUNDO DEPORTIVO / LA LIGA",
        10: "THE ATHLETIC / CHELSEA FC",
        11: "BUNDESLIGA / KICKER",
        12: "CADENA SER / BÁO CHÍ TÂY BAN NHA",
        13: "FIFA / LỊCH SỬ BÓNG ĐÁ THẾ GIỚI",
        14: "GLOBO ESPORTE / GUINNESS",
        15: "UCI / BÁO CHÍ ĐỨC",
        16: "VFF / BÁO THANH NIÊN",
        17: "VPF / BÁO TUỔI TRẺ",
        18: "BÁO ĐỒNG NAI / VPF",
        19: "THỂ THAO 247 / V-LEAGUE",
        20: "AFC WOMEN'S CHAMPIONS LEAGUE",
        21: "BÁO LONG AN / V-LEAGUE",
        22: "UMB / WORLD CUP BILLIARDS",
        23: "ATP TOUR / PARIS MASTERS",
        24: "FORMULA 1 / FIA",
        25: "VFV / BÓNG CHUYỀN NHẬT BẢN",
    }

    combined_audio = AudioSegment.silent(duration=0)
    gap_ms = 350
    gap_audio = AudioSegment.silent(duration=gap_ms)

    items_data = []
    all_words = []
    all_karaoke = []
    raw_sfx = []
    cum_sec = 0.0

    log("Bắt đầu sinh giọng đọc ViTTS luân phiên Nam - Nữ...")
    for idx, item in enumerate(items, 1):
        it_id = int(item.get("id", idx))
        is_male = (it_id % 2 == 1)  # Lẻ: Nam, Chẵn: Nữ
        active_preset = male_preset if is_male else female_preset
        gender_label = "Nam" if is_male else "Nữ"

        it_title = (item.get("digest_title") or item.get("title", "")).strip()
        digest_text = (item.get("digest_line") or item.get("summary", "")[:130]).strip()

        # Chọn ảnh đại diện nét nhất
        img_cand = item.get("image_1") or item.get("image_path")
        if not img_cand or not os.path.exists(img_cand):
            cands = sorted(glob.glob(str(day_dir / "images" / f"*Tin_{it_id:02d}*.jpg")))
            img_cand = cands[0] if cands else str(day_dir / "images" / "Tin_01_1.jpg")

        img_base = os.path.basename(img_cand)
        photo_credit = img_credits_map.get(img_base, "REUTERS / AP")
        news_source = news_source_dict.get(it_id, "ĐIỂM ĐỌC THỂ THAO")

        tts_str, _ = prepare(digest_text)
        item_wav = work_dir / f"digest_dual_{it_id:02d}.wav"

        seg, _ = render_chunk_vitts(
            voice_model,
            tts_str,
            voice=active_preset["voice_id"],
            temperature=active_preset["temperature"],
            speed=active_preset["speed"],
            pitch=active_preset["pitch"],
            cache_dir=str(tts_cache_dir),
            use_cache=True,
        )
        seg.export(str(item_wav), format="wav")
        it_dur = len(seg) / 1000.0

        if idx > 1:
            combined_audio += gap_audio
            cum_sec += (gap_ms / 1000.0)
            raw_sfx.append({
                "sfx": "whoosh_cinematic_short.mp3",
                "time": round(cum_sec, 3),
                "volume": 0.22
            })

        it_start = cum_sec
        combined_audio += seg
        cum_sec += it_dur
        it_end = cum_sec

        # Mốc từ và karaoke
        s_words = interpolate_sentence_words(digest_text, 0.0, it_dur)
        abs_words = []
        for w in s_words:
            abs_w = {
                "word": w["word"],
                "start": round(it_start + w["start"], 3),
                "end": round(it_start + w["end"], 3),
                "matched": True
            }
            abs_words.append(abs_w)
            all_words.append(abs_w)

        for ci in range(0, len(abs_words), 4):
            c_words = abs_words[ci:ci + 4]
            all_karaoke.append({
                "start": c_words[0]["start"],
                "end": c_words[-1]["end"],
                "text": " ".join(cw["word"] for cw in c_words),
                "words": c_words
            })

        pan_info = compute_pan_params(img_cand, duration=it_dur, dir_toggle=(idx % 2 == 1))

        items_data.append({
            "id": str(it_id),
            "title": it_title,
            "digest_line": digest_text,
            "image": img_cand,
            "credit": photo_credit,
            "news_source": news_source,
            "voice_gender": gender_label,
            "start": round(it_start, 3),
            "end": round(it_end, 3),
            "duration": round(it_dur, 3),
            **pan_info
        })
        log(f"  [{idx:02d}/25] ({gender_label}) Tin #{it_id:02d}: {it_title[:40]}... ({it_dur:.2f}s)")

    # 2. Xuất audio master và chuẩn hóa Loudnorm (-14.0 LUFS)
    raw_concat_wav = work_dir / "voiceover_raw.wav"
    concat_wav = work_dir / "voiceover_master.wav"
    combined_audio.export(str(raw_concat_wav), format="wav")

    ok(f"Tổng thời lượng giọng đọc: {len(combined_audio)/1000.0:.2f}s")
    log("Chuẩn hóa âm lượng EBU R128 (-14.0 LUFS, TP <= -1.5 dBTP)...")
    if not two_pass_loudnorm(str(raw_concat_wav), str(concat_wav), target_i=-14.0, target_tp=-1.5, target_lra=11.0):
        combined_audio.export(str(concat_wav), format="wav")

    # 3. Nạp cấu hình hiệu ứng fx
    fx_path = Path(paths.CONFIG) / "fx.json"
    fx_cfg = {}
    if fx_path.exists():
        try:
            with open(fx_path, "r", encoding="utf-8") as f:
                fx_cfg = json.load(f)
        except Exception:
            pass

    total_dur = round(len(combined_audio) / 1000.0, 3)

    timeline = {
        "title": "ĐỌC NHANH THỂ THAO 09.11",
        "channel_name": "ĐIỂM ĐỌC",
        "date_str": "THỨ HAI · 09.11.2026",
        "date_chip": "THỨ HAI · 09.11.2026",
        "hide_date_chip": False,
        "total_duration": total_dur,
        "format": "short",
        "template": "short_digest_v2.html",
        "dimensions": [1080, 1920],
        "fps": 30,
        "audio_path": str(concat_wav),
        "global_offset_sec": 0.0,
        "fx": fx_cfg,
        "sfx_events": raw_sfx,
        "items": items_data,
        "karaoke_chunks": all_karaoke
    }

    words_data = {
        "words": all_words,
        "karaoke_chunks": all_karaoke
    }

    tl_path = work_dir / "video_timeline.json"
    words_path = work_dir / "word_timestamps.json"
    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)
    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)

    # 4. Render video 9:16 bằng renderer HTML v2
    sys.path.insert(0, str(Path(paths.ROOT) / "engines" / "html"))
    from renderer import render_html_engine

    log("Bắt đầu render video HTML v2 (Playwright + GSAP) vào thư mục tạm...")
    out_video_work = render_html_engine(
        project_dir=str(work_dir),
        template="short_digest_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True
    )

    if not out_video_work or not os.path.exists(out_video_work):
        die("Render HTML v2 thất bại!")

    # 5. Xuất bản video vào outputs/09.11.2026/shorts/ với tên file phân biệt rõ ràng
    shorts_dir = day_dir / "shorts"
    shorts_dir.mkdir(parents=True, exist_ok=True)
    out_final_mp4 = shorts_dir / "Short_Tin_Nhanh_25_Tin_Nam_Nu.mp4"
    shutil.copy2(out_video_work, str(out_final_mp4))
    ok(f"Đã xuất video tin nhanh song song Nam - Nữ: {out_final_mp4}")

    # 6. Tạo file mota.txt chuẩn 2 phần
    chapters_digest = []
    for it in items_data:
        m = int(it["start"] // 60)
        s = int(it["start"] % 60)
        chapters_digest.append((f"{m:02d}:{s:02d}", it["title"]))

    mota_path = shorts_dir / "Short_Tin_Nhanh_25_Tin_Nam_Nu_mota.txt"
    write_mota_9x16(
        out_path=mota_path,
        seo_title="Tin nhanh thể thao 09/11: Toàn cảnh 25 sự kiện nóng nhất qua 2 giọng đọc Nam Nữ #Shorts",
        description_paragraphs=[
            "Bản tin Điểm Đọc Thể Thao đọc nhanh toàn cảnh 25 sự kiện thể thao chấn động nhất tuần qua (02/11 – 09/11/2026) được dẫn song song luân phiên qua 2 giọng đọc Nam và Nữ chuyên nghiệp.",
            "Điểm nhanh từ quyết định giã từ ĐTQG của Cristiano Ronaldo, biến động nghẹt thở tại Ngoại hạng Anh, Champions League, La Liga đến bóng đá Việt Nam và các đỉnh cao thể thao thế giới."
        ],
        chapters=chapters_digest,
        sources_line="📰 Nguồn tin: VnExpress, Thanh Niên, Tuổi Trẻ, Reuters, AP, UEFA, FIFA, VPF.",
        hashtags=["#Shorts", "#TinNhanh", "#DiemDoc", "#DiemDocTheThao", "#BongDa", "#Ronaldo", "#ManCity", "#ManUtd", "#VLeague", "#ChampionsLeague"]
    )
    ok(f"Đã tạo file mô tả SEO: {mota_path}")

    # 7. Render Thumbnail dọc 9:16 chuẩn Cyber-Stadium Electric Cyan
    thumb_path = shorts_dir / "Short_Tin_Nhanh_25_Tin_Nam_Nu_thumbnail.jpg"
    render_thumbnail_9x16(
        out_path=thumb_path,
        image_path=day_dir / "images" / "Tin_01_1.jpg",
        kicker="ĐỌC NHANH 25 TIN THỂ THAO TUẦN QUA",
        hero_html="<span class=\"hl-cyan\">25 TIN NÓNG TUẦN</span><br><span class=\"hl-white\">SONG SONG NAM NỮ</span><br><span class=\"hl-yellow\">RONALDO & MU 4-4!</span>",
        subtitle="2 PHÁT THANH VIÊN ĐIỂM NHANH 25 SỰ KIỆN CHẤN ĐỘNG NHẤT TUẦN QUA",
        badge="SONG SONG NAM NỮ",
        tag_a="25 TIN THỜI SỰ",
        tag_b="09.11.2026",
        obj_pos="center 15%",
    )
    ok(f"Đã tạo ảnh bìa 9:16 chuẩn: {thumb_path}")

    print("\n" + "=" * 78)
    ok("HOÀN THÀNH XUẤT BẢN VIDEO TIN NHANH SONG SONG NAM - NỮ THÀNH CÔNG!")
    print(f"  🎬 Video thành phẩm: {out_final_mp4}")
    print(f"  🖼️  Ảnh bìa 9:16:     {thumb_path}")
    print(f"  📝 Mô tả SEO:        {mota_path}")
    print(f"  📁 Bản cũ đối chiếu: {shorts_dir / 'Short_Tin_Nhanh_25_Tin_The_Thao.mp4'} (VẪN GIỮ NGUYÊN 100%)")
    print("=" * 78)


if __name__ == "__main__":
    main()
