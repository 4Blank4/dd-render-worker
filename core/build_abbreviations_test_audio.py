#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_abbreviations_test_audio.py — Tạo file âm thanh kiểm tra phát âm từ viết tắt thể thao
cho mô hình ViTTS Minh Quân Pro (Điểm Đọc).
"""
import sys
sys.dont_write_bytecode = True

import os
import time
from pydub import AudioSegment

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from vieneu import Vieneu
from diemdoc import paths
from diemdoc.audio import apply_voice_standard
from diemdoc.log import banner, ok, step, log

# Danh sách từ viết tắt thể thao thường gặp
ABBREVIATIONS = [
    # Nhóm 1: Thuật ngữ & Danh xưng cơ bản
    ("VĐQG", "Vô địch quốc gia", "Giải đấu cấp cao nhất quốc gia"),
    ("CLB", "Câu lạc bộ", "Đơn vị câu lạc bộ bóng đá / thể thao"),
    ("HLV", "Huấn luyện viên", "Người dẫn dắt đội bóng"),
    ("VĐV", "Vận động viên", "Người tham gia thi đấu thể thao"),
    ("ĐTQG", "Đội tuyển quốc gia", "Đại diện cấp quốc gia"),
    ("ĐT", "Đội tuyển", "Đội tuyển nói chung (ĐT Việt Nam...)"),
    ("BHL", "Ban huấn luyện", "Tập thể ban huấn luyện đội bóng"),
    ("BTC", "Ban tổ chức", "Đơn vị điều hành giải đấu"),
    ("BLV", "Bình luận viên", "Người bình luận trận đấu"),
    ("CĐV", "Cổ động viên", "Người hâm mộ trên khán đài"),
    ("BXH", "Bảng xếp hạng", "Bảng thứ bậc điểm số giải đấu"),
    ("TTCN", "Thị trường chuyển nhượng", "Giai đoạn mua bán cầu thủ"),
    ("HCV", "Huy chương vàng", "Giải nhất đại hội thể thao"),
    ("HCB", "Huy chương bạc", "Giải nhì đại hội thể thao"),
    ("HCĐ", "Huy chương đồng", "Giải ba đại hội thể thao"),
    ("VĐTG", "Vô địch thế giới", "Danh hiệu quán quân thế giới"),
    ("CK", "Chung kết", "Trận đấu tranh cúp vô địch"),
    ("BK", "Bán kết", "Vòng đấu tranh vé vào chung kết"),
    ("TK", "Tứ kết", "Vòng 8 đội mạnh nhất"),

    # Nhóm 2: Vị trí thi đấu & Kỹ thuật
    ("TM", "Thủ môn", "Người gác đền"),
    ("HV", "Hậu vệ", "Cầu thủ phòng ngự"),
    ("TV", "Tiền vệ", "Cầu thủ tuyến giữa"),
    ("TĐ", "Tiền đạo", "Cầu thủ hàng công săn bàn"),
    ("VAR", "Công nghệ hỗ trợ trọng tài", "Video Assistant Referee"),
    ("KO", "Knockout / Nốc ao", "Đo ván trong đối kháng"),
    ("vs", "Đối đầu (Versus)", "Từ nối giữa 2 đội thi đấu"),
    ("VS", "Đối đầu (Versus viết hoa)", "Từ nối giữa 2 đội thi đấu"),

    # Nhóm 3: Tổ chức & Giải đấu Việt Nam
    ("VFF", "Liên đoàn Bóng đá Việt Nam", "Vietnam Football Federation"),
    ("VPF", "Công ty CP Bóng đá Chuyên nghiệp Việt Nam", "Vietnam Professional Football"),
    ("V-League", "Giải VĐQG Việt Nam", "V.League 1"),
    ("VBA", "Giải bóng rổ chuyên nghiệp Việt Nam", "Vietnam Basketball Association"),
    ("Cúp QG", "Cúp Quốc gia", "Giải đấu cúp tại Việt Nam"),
    ("HNQG", "Hạng Nhất Quốc gia", "Giải hạng Nhất bóng đá Việt Nam"),
    ("ĐHTT", "Đại hội Thể thao", "Đại hội thể dục thể thao toàn quốc"),
    ("TDTT", "Thể dục Thể thao", "Ngành thể dục thể thao"),

    # Nhóm 4: Các CLB Việt Nam hay viết tắt
    ("CAHN", "Công an Hà Nội", "CLB Công an Hà Nội"),
    ("SLNA", "Sông Lam Nghệ An", "CLB Sông Lam Nghệ An"),
    ("HAGL", "Hoàng Anh Gia Lai", "CLB Hoàng Anh Gia Lai"),
    ("TP.HCM", "Thành phố Hồ Chí Minh", "CLB hoặc địa phương"),
    ("TPHCM", "Thành phố Hồ Chí Minh (không dấu chấm)", "CLB hoặc địa phương"),
    ("SHB", "SHB Đà Nẵng", "Tên nhà tài trợ gắn liền CLB"),
    ("PVF", "Trung tâm đào tạo trẻ PVF", "Học viện bóng đá"),

    # Nhóm 5: Các lứa tuổi trẻ
    ("U23", "U hai mươi ba", "Đội tuyển U23"),
    ("U21", "U hai mươi mốt", "Đội tuyển U21"),
    ("U19", "U mười chín", "Đội tuyển U19"),
    ("U17", "U mười bảy", "Đội tuyển U17"),
    ("U16", "U mười sáu", "Đội tuyển U16"),
    ("U15", "U mười lăm", "Đội tuyển U15"),

    # Nhóm 6: Tổ chức & Giải đấu Quốc tế
    ("FIFA", "Liên đoàn Bóng đá Thế giới", "Fédération Internationale de Football Association"),
    ("UEFA", "Liên đoàn Bóng đá Châu Âu", "Union of European Football Associations"),
    ("AFC", "Liên đoàn Bóng đá Châu Á", "Asian Football Confederation"),
    ("AFF", "Liên đoàn Bóng đá Đông Nam Á", "ASEAN Football Federation"),
    ("C1", "Cúp C1 Châu Âu", "UEFA Champions League"),
    ("C2", "Cúp C2 Châu Âu", "UEFA Europa League"),
    ("C3", "Cúp C3 Châu Âu", "UEFA Conference League"),
    ("WC", "World Cup", "Cúp bóng đá thế giới"),
    ("PBA", "Hiệp hội Bi-a Chuyên nghiệp", "Professional Billiards Association"),
    ("UMB", "Liên đoàn Bi-a Thế giới", "Union Mondiale de Billard"),
    ("ATP", "Hiệp hội Quần vợt Nam", "Association of Tennis Professionals"),
    ("WTA", "Hiệp hội Quần vợt Nữ", "Women's Tennis Association"),
    ("NBA", "Giải Bóng rổ Nhà nghề Mỹ", "National Basketball Association"),
    ("MMA", "Võ thuật tổng hợp", "Mixed Martial Arts"),
    ("UFC", "Giải Đấu Võ thuật Đỉnh cao", "Ultimate Fighting Championship"),
    ("F1", "Đua xe Công thức 1", "Formula 1"),
    ("SEA Games", "Đại hội Thể thao Đông Nam Á", "South East Asian Games"),
    ("ASIAD", "Đại hội Thể thao Châu Á", "Asian Games"),
    ("Olympic", "Thế vận hội Mùa hè / Mùa đông", "Olympic Games")
]


def generate_audio_test():
    banner("TẠO FILE AUDIO KIỂM TRA PHÁT ÂM TỪ VIẾT TẮT THỂ THAO", f"Tổng cộng {len(ABBREVIATIONS)} từ")
    
    out_dir = os.path.join(paths.OUTPUTS, "02.11.2026")
    os.makedirs(out_dir, exist_ok=True)
    
    cache_dir = paths.work_file("vitts_cache_abbr")
    os.makedirs(cache_dir, exist_ok=True)
    
    step("1. Khởi tạo mô hình ViTTS v3turbo Minh Quân Pro...")
    model = Vieneu(mode="v3turbo")
    
    pause_between = AudioSegment.silent(duration=1200, frame_rate=44100).set_channels(2)
    intro_seg = None
    
    # Đoạn giới thiệu đầu
    intro_text = "Bản kiểm tra phát âm các từ viết tắt thể thao thường gặp trên kênh Điểm Đọc. Sau đây là danh sách chi tiết từng từ."
    intro_wav = os.path.join(cache_dir, "intro.wav")
    if not os.path.exists(intro_wav):
        from m3_voice import render_chunk_vitts
        seg_intro, _ = render_chunk_vitts(model, intro_text, voice="Minh Quân Pro", temperature=0.5, speed=1.15, pitch=0.85, cache_dir=cache_dir)
        seg_intro = seg_intro.set_frame_rate(44100).set_channels(2)
        seg_intro.export(intro_wav, format="wav")
    intro_seg = AudioSegment.from_file(intro_wav)
    
    master_audio = intro_seg + AudioSegment.silent(duration=1500, frame_rate=44100).set_channels(2)
    
    timeline_records = []
    
    step(f"2. Bắt đầu tổng hợp {len(ABBREVIATIONS)} từ viết tắt nguyên bản...")
    from m3_voice import render_chunk_vitts
    
    for idx, (abbr, full_mean, note) in enumerate(ABBREVIATIONS, 1):
        cur_pos_ms = len(master_audio)
        mins = int((cur_pos_ms / 1000) // 60)
        secs = int((cur_pos_ms / 1000) % 60)
        ts_str = f"{mins:02d}:{secs:02d}"
        
        # Câu đọc thuần: "Số 1: VĐQG." (giữ nguyên gốc không phiên âm, để TTS đọc trực tiếp)
        phrase = f"Số {idx}: {abbr}."
        
        chunk_file = os.path.join(cache_dir, f"abbr_{idx:02d}_{abbr.replace('.', '_').replace('/', '_')}.wav")
        if not os.path.exists(chunk_file):
            seg, _ = render_chunk_vitts(model, phrase, voice="Minh Quân Pro", temperature=0.5, speed=1.15, pitch=0.85, cache_dir=cache_dir)
            seg = seg.set_frame_rate(44100).set_channels(2)
            seg.export(chunk_file, format="wav")
        else:
            seg = AudioSegment.from_file(chunk_file)
            
        master_audio += seg + pause_between
        timeline_records.append((idx, ts_str, abbr, full_mean, note))
        log(f"  [{idx:02d}/{len(ABBREVIATIONS)}] ({ts_str}) '{phrase}' -> {len(seg)/1000:.2f}s")

    # Chuẩn hoá âm lượng master
    step("3. Chuẩn hóa âm lượng EBU R128 (-16 LUFS)...")
    master_audio = apply_voice_standard(master_audio)
    
    wav_out = os.path.join(out_dir, "kiem_tra_tu_viet_tat.wav")
    mp3_out = os.path.join(out_dir, "kiem_tra_tu_viet_tat.mp3")
    
    master_audio.export(wav_out, format="wav")
    master_audio.export(mp3_out, format="mp3", bitrate="192k")
    
    ok(f"  -> Đã xuất file WAV: {paths.rel_to_root(wav_out)} ({len(master_audio)/1000:.1f}s)")
    ok(f"  -> Đã xuất file MP3: {paths.rel_to_root(mp3_out)} ({os.path.getsize(mp3_out)/1024:.1f} KB)")
    
    # Tạo file markdown đối soát chi tiết
    step("4. Tạo bảng đối soát danh_sach_tu_viet_tat.md...")
    md_path = os.path.join(out_dir, "danh_sach_tu_viet_tat.md")
    
    md_content = [
        "# BẢNG ĐỐI SOÁT & ĐÁNH GIÁ PHÁT ÂM TỪ VIẾT TẮT THỂ THAO (TTS ViTTS Minh Quân Pro)",
        "",
        f"- **File âm thanh nghe thử**: [`kiem_tra_tu_viet_tat.mp3`](file://{mp3_out}) (hoặc [`kiem_tra_tu_viet_tat.wav`](file://{wav_out}))",
        f"- **Thời lượng**: **{len(master_audio)/60000:.1f} phút** ({len(master_audio)/1000:.1f} giây)",
        f"- **Tổng số từ kiểm tra**: **{len(ABBREVIATIONS)} từ**",
        "- **Quy chuẩn đọc**: ViTTS Minh Quân Pro đọc nguyên văn chuỗi dạng `\"Số X: [TỪ_VIẾT_TẮT].\"` (tốc độ 1.15, cao độ 0.85, nghỉ 1.2s giữa các từ).",
        "",
        "> **HƯỚNG DẪN DÀNH CHO CHỦ KÊNH:**",
        "> - Bật file audio nghe lần lượt từng từ theo mốc thời gian.",
        "> - Nếu từ nào TTS đọc **ĐÚNG & TỰ NHIÊN** (ví dụ CLB đọc thành 'câu lạc bộ' hoặc đọc tên chuẩn): để nguyên hoặc đánh dấu `[x]`.",
        "> - Nếu từ nào TTS đọc **SAI / BỊ VẤP / BỊ NUỐT TỪ** (ví dụ VĐQG bị đọc sai): ghi chú lại.",
        "> - Hệ thống sẽ tự động tổng hợp các từ sai vào danh sách `abbreviations_map.json` để tự động chuẩn hóa sang lời đọc chuẩn về sau mà màn hình hiển thị vẫn giữ nguyên từ viết tắt!",
        "",
        "---",
        "",
        "| STT | Mốc Thời Gian | Từ Viết Tắt | Ý Nghĩa Chuẩn | Kết Quả Nghe Thực Tế | Ghi Chú Cách Đọc Mong Muốn |",
        "| :---: | :---: | :---: | :--- | :---: | :--- |"
    ]
    
    for idx, ts_str, abbr, full_mean, note in timeline_records:
        md_content.append(f"| {idx:02d} | `{ts_str}` | **{abbr}** | {full_mean} ({note}) | [ ] Đạt / [ ] Chưa đạt |  |")
        
    md_content.extend([
        "",
        "---",
        "### Ghi chú tổng hợp sau khi nghe:",
        "- Từ cần bổ sung phiên âm ngay: ...",
        "- Từ đọc tốt không cần chỉnh: ..."
    ])
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))
        
    ok(f"  -> Đã tạo bảng checklist: {paths.rel_to_root(md_path)}")
    banner("HOÀN TẤT TẠO FILE KIỂM TRA PHÁT ÂM TỪ VIẾT TẮT")


if __name__ == "__main__":
    generate_audio_test()
