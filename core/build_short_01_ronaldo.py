#!/usr/bin/env python3
"""
core/build_short_01_ronaldo.py — Sản xuất Video Short 1: Cristiano Ronaldo Giã Từ ĐTQG (Focus Short)

Đặc tả:
- Gộp 2 tin tâm điểm về Ronaldo từ outputs/09.11.2026/thethao.json:
    + Tin 01: Cristiano Ronaldo giã từ đội tuyển Bồ Đào Nha sau 23 năm
    + Tin 02: Góc khuất Ronaldo phớt lờ HLV Jorge Jesus và làn sóng tri ân
- Thể hiện rõ bản chất: "TIN NÓNG TUẦN QUA" trên tiêu đề, kicker và nội dung
- Áp dụng template short_news_v2.html đã nâng cấp:
    + Hero Title lớn ở đầu mỗi bản tin khi đọc tiêu đề (is_title: True)
    + Thu về #fixed-headline-bar khi vào chi tiết
    + Cập nhật động Category Pill, Lower-Third 2 góc (Nguồn tin & Nguồn ảnh)
    + Phụ đề Karaoke 48px đồng bộ 100% từng từ
    + Âm thanh master chuẩn hóa Loudnorm (-14.0 LUFS, TP <= -1.5 dBTP)
- Xuất bản trọn bộ:
    + Video: outputs/09.11.2026/shorts/Short_01_Tin_Nong_Ronaldo_Gia_Tu_DTQG.mp4
    + Thumbnail: Short_01_Tin_Nong_Ronaldo_Gia_Tu_DTQG_thumbnail.jpg
    + Mô tả SEO: Short_01_Tin_Nong_Ronaldo_Gia_Tu_DTQG_mota.txt
"""
import sys
sys.dont_write_bytecode = True

import os
import json
import shutil
from pathlib import Path

from diemdoc import paths
from diemdoc.log import banner, ok, log, die
from diemdoc.publisher import write_mota_9x16, render_thumbnail_9x16
from m8_news_bridge import build_focus_short_timeline


def main():
    day_dir = Path(paths.ROOT) / "outputs" / "09.11.2026"
    work_proj_dir = Path(paths.WORK) / "focus_short_01_ronaldo"
    work_proj_dir.mkdir(parents=True, exist_ok=True)

    banner("SẢN XUẤT SHORT 1: CRISTIANO RONALDO GIÃ TỪ ĐTQG BỒ ĐÀO NHA", "09.11.2026")

    # 1. Xây dựng timeline Focus Short gộp Tin 1 và Tin 2
    log("Xây dựng timeline Focus Short (Tin 1 + Tin 2)...")
    timeline, words_data, default_work = build_focus_short_timeline(
        day_dir=str(day_dir),
        item_ids=[1, 2],
        global_offset_sec=0.0
    )

    # Tùy biến tiêu đề & kicker để làm nổi bật "TIN NÓNG TUẦN QUA"
    timeline["title"] = "TIN NÓNG TUẦN QUA: CRISTIANO RONALDO CHIA TAY ĐỘI TUYỂN BỒ ĐÀO NHA"
    timeline["group"] = "TIN NÓNG TUẦN QUA"

    # Cập nhật news_source cho Tin 1 và Tin 2
    for s in timeline.get("sentences", []):
        if str(s.get("item_id")) == "1":
            s["item_group"] = "TIN NÓNG TUẦN QUA"
            s["news_source"] = "BÁO CHÍ BỒ ĐÀO NHA / FPF"
        elif str(s.get("item_id")) == "2":
            s["item_group"] = "GÓC KHUẤT RẠN NỨT"
            s["news_source"] = "RECORD / O JOGO / AL HILAL"

    tl_path = work_proj_dir / "video_timeline.json"
    words_path = work_proj_dir / "word_timestamps.json"
    voice_dest = work_proj_dir / "voiceover.wav"

    if os.path.exists(timeline["audio_path"]):
        shutil.copy2(timeline["audio_path"], str(voice_dest))

    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)

    ok(f"Đã xuất timeline Focus Short: {tl_path}")

    # 2. Render bằng engine HTML v2 (Playwright + GSAP)
    sys.path.insert(0, str(Path(paths.ROOT) / "engines" / "html"))
    from renderer import render_html_engine

    log("Render video bằng HTML v2 (Playwright + GSAP)...")
    out_video_work = render_html_engine(
        project_dir=str(work_proj_dir),
        template="short_news_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True
    )

    if not out_video_work or not os.path.exists(out_video_work):
        die("Render Focus Short thất bại!")

    # 3. Xuất bản vào outputs/09.11.2026/shorts/
    shorts_dir = day_dir / "shorts"
    shorts_dir.mkdir(parents=True, exist_ok=True)
    out_final_mp4 = shorts_dir / "Short_01_Tin_Nong_Ronaldo_Gia_Tu_DTQG.mp4"
    shutil.copy2(out_video_work, str(out_final_mp4))
    ok(f"Đã xuất video: {out_final_mp4}")

    # 4. Xuất file mô tả SEO YouTube Shorts chuẩn 2 phần
    chapters = [
        ("00:00", "Cristiano Ronaldo giã từ đội tuyển Bồ Đào Nha sau 23 năm huyền thoại"),
        ("00:40", "Góc khuất rạn nứt với HLV Jorge Jesus và làn sóng tri ân toàn cầu"),
    ]
    mota_path = shorts_dir / "Short_01_Tin_Nong_Ronaldo_Gia_Tu_DTQG_mota.txt"
    write_mota_9x16(
        out_path=mota_path,
        seo_title="Tin nóng tuần qua: Cristiano Ronaldo chia tay Bồ Đào Nha và góc khuất rạn nứt #Shorts",
        description_paragraphs=[
            "Tin nóng thể thao tuần qua: Siêu sao 41 tuổi Cristiano Ronaldo chính thức đăng tải video thông báo giã từ đội tuyển quốc gia Bồ Đào Nha sau 23 năm cống hiến với kỷ lục vô tiền khoáng hậu 234 trận đấu và 146 bàn thắng.",
            "Tuy nhiên, quyết định chia tay này cũng hé lộ những góc khuất rạn nứt gay gắt với huấn luyện viên trưởng Jorge Jesus khi Ronaldo chủ động cắt đứt liên lạc trước ngày công bố danh sách tập trung."
        ],
        chapters=chapters,
        sources_line="📰 Nguồn tin: VnExpress, Báo chí Bồ Đào Nha, Record, O Jogo, FPF.",
        hashtags=["#Shorts", "#TinNongTuanQua", "#CristianoRonaldo", "#Ronaldo", "#BoDaoNha", "#DiemDoc", "#DiemDocTheThao", "#BongDa"]
    )
    ok(f"Đã tạo file mô tả SEO: {mota_path}")

    # 5. Render Thumbnail 9:16 chuẩn Cyber-Stadium Electric Cyan
    thumb_path = shorts_dir / "Short_01_Tin_Nong_Ronaldo_Gia_Tu_DTQG_thumbnail.jpg"
    render_thumbnail_9x16(
        out_path=thumb_path,
        image_path=day_dir / "images" / "Tin_01_1.jpg",
        kicker="TIN NÓNG THỂ THAO TUẦN QUA",
        hero_html="<span class=\"hl-cyan\">RONALDO CHIA TAY</span><br><span class=\"hl-white\">BỒ ĐÀO NHA 23 NĂM</span><br><span class=\"hl-yellow\">GÓC KHUẤT RẠN NỨT!</span>",
        subtitle="HÀNH TRÌNH 146 BÀN THẮNG HUYỀN THOẠI VÀ SỰ THẬT VỚI HLV JORGE JESUS",
        badge="TÂM ĐIỂM TUẦN",
        tag_a="TIN NÓNG TUẦN",
        tag_b="09.11.2026",
        obj_pos="center 15%",
    )
    ok(f"Đã tạo thumbnail 9:16 chuẩn: {thumb_path}")

    print("\n" + "=" * 78)
    ok("HOÀN THÀNH XUẤT BẢN SHORT 1 THÀNH CÔNG!")
    print(f"  🎬 Video:     {out_final_mp4}")
    print(f"  🖼️  Thumbnail: {thumb_path}")
    print(f"  📝 Mô tả SEO: {mota_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
