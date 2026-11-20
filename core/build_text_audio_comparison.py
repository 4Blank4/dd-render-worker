#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True

import os, json, subprocess
from pydub import AudioSegment

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_ROOT, "engines", "html"))

from diemdoc import paths
from vieneu import Vieneu
from m3_voice import render_chunk_vitts, trim_segment_silence

OUT_DIR = os.path.join(_ROOT, "outputs", "22.10.2026", "text-audio")
os.makedirs(OUT_DIR, exist_ok=True)
TTS_CACHE = paths.work_file("vitts_cache")

# Danh sách 54 tên / thuật ngữ trong kịch bản ngày 22.10.2026
# (display, say_with_hyphens [lúc đầu], say_without_hyphens [không gạch], category, context)
TERMS_DATA = [
    # Cảnh 1: Địa điểm & Nhân vật gala
    ("Palladium", "Pa - la - di - um", "Pa la đi um", "Địa điểm / Nhà hát", "Cảnh 01: Nhà hát tổ chức Gala tại London"),
    ("London Palladium", "Lân-đơn Pa-la-di-um", "Lân đơn Pa la đi um", "Địa điểm / Nhà hát", "Cảnh 01: Tên đầy đủ nhà hát London Palladium"),
    ("France Football", "Phrăng Phút-bo", "Phrăng Phút bo", "Tạp chí / Ban tổ chức", "Cảnh 01: Đơn vị sáng lập Quả bóng Vàng"),
    ("UEFA", "U-ê-pha", "U ê pha", "Liên đoàn bóng đá", "Cảnh 01: Đồng tổ chức Gala"),
    ("Sir Stanley Matthews", "Xơ Xtan-li Mát-thiu", "Xơ Xtan li Mát thiu", "Huyền thoại", "Cảnh 01: Chủ nhân Quả bóng Vàng đầu tiên 1956"),
    ("Stanley Matthews", "Xtan-li Mát-thiu", "Xtan li Mát thiu", "Huyền thoại", "Cảnh 01: Tên cố huyền thoại người Anh"),
    ("Blackpool", "B-lắc-pun", "B lắc pun", "Câu lạc bộ", "Cảnh 01: CLB của Stanley Matthews năm 1956"),
    ("Thierry Henry", "Ti-ê-ri Ăng-ri", "Ti ê ri Ăng ri", "Danh thủ / MC", "Cảnh 01: Người dẫn chương trình gala"),
    ("Kate Scott", "Két Xcốt", "Két Xcốt", "Nhà báo / MC", "Cảnh 01: Nữ MC dẫn dắt đêm gala"),
    ("DAZN", "Đa-zôn", "Đa zôn", "Truyền thông", "Cảnh 01: Nền tảng phát sóng trực tiếp gala"),

    # Cảnh 2: Thể thức & Giải đấu
    ("World Cup", "Uôn Cúp", "Uôn Cúp", "Giải đấu", "Cảnh 02: VCK bóng đá thế giới 2026 tại Bắc Mỹ"),
    ("FIFA", "Phi-pha", "Phi pha", "Liên đoàn thế giới", "Cảnh 02: Bảng xếp hạng FIFA của ban giám khảo"),

    # Cảnh 3: Harry Kane & Bayern Munich
    ("Harry Kane", "Ha-ri Kên", "Ha ri Kên", "Cầu thủ", "Cảnh 03: Tiền đạo ứng viên số 1, ghi 61 bàn"),
    ("Bayern Munich", "Bay-ơn Mu-ních", "Bay ơn Mu ních", "Câu lạc bộ", "Cảnh 03: CLB chủ quản của Harry Kane"),
    ("Bundesliga", "Bun-đét-xli-ga", "Bun đét xli ga", "Giải đấu", "Cảnh 03: Giải VĐQG Đức"),
    ("Vincent Kompany", "Vanh-xăng Côm-pa-ni", "Vanh xăng Côm pa ni", "Huấn luyện viên", "Cảnh 03: HLV trưởng Bayern Munich"),

    # Cảnh 4: Lamine Yamal & Kỷ lục
    ("Lamine Yamal", "La-min Gia-man", "La min Gia man", "Cầu thủ", "Cảnh 04: Thần đồng 19 tuổi Barcelona & TBN"),
    ("Barcelona", "Bát-xê-lô-na", "Bát xê lô na", "Câu lạc bộ", "Cảnh 04: CLB Barcelona"),
    ("Ronaldo Nazário", "Rô-nan-đô Na-da-ri-ô", "Rô nan đô Na da ri ô", "Huyền thoại", "Cảnh 04: Người giữ kỷ lục trẻ nhất năm 1997"),
    ("Pau Cubarsí", "Pao Cu-bác-xi", "Pao Cu bác xi", "Cầu thủ", "Cảnh 04: Trung vệ trẻ đồng đội Yamal"),
    ("Hansi Flick", "Han-xi Phơ-lích", "Han xi Phơ lích", "Huấn luyện viên", "Cảnh 04: HLV trưởng Barcelona"),
    ("Kopa Trophy", "Cúp Cô-pa", "Cúp Cô pa", "Giải thưởng", "Cảnh 04 & 06: Giải cầu thủ trẻ xuất sắc nhất"),

    # Cảnh 5: Mbappé & Messi
    ("Kylian Mbappé", "Ki-li-an Em-ba-pê", "Ki li an Em ba pê", "Cầu thủ", "Cảnh 05: Tiền đạo số 9 Real Madrid & Pháp"),
    ("Lionel Messi", "Li-ô-nen Méc-xi", "Li ô nen Méc xi", "Cầu thủ", "Cảnh 05: Huyền thoại 8 Quả bóng Vàng"),
    ("Real Madrid", "Rê-an Ma-đrít", "Rê an Ma đrít", "Câu lạc bộ", "Cảnh 05: Đội bóng Hoàng gia Tây Ban Nha"),
    ("La Liga", "La Li-ga", "La Li ga", "Giải đấu", "Cảnh 05: Giải VĐQG Tây Ban Nha"),
    ("Champions League", "Cúp Cê một", "Cúp Cê một", "Giải đấu", "Cảnh 05: Cúp C1 châu Âu"),
    ("Carlo Ancelotti", "Cát-lô An-chê-lốt-ti", "Cát lô An chê lốt ti", "Huấn luyện viên", "Cảnh 05: HLV trưởng Real Madrid"),
    ("Onze d'Or", "Ông-dơ Đò", "Ông dơ Đò", "Giải thưởng", "Cảnh 05: Giải thưởng cá nhân của báo Pháp"),
    ("Les Bleus", "Lê B-lơ", "Lê B lơ", "Biệt danh", "Cảnh 05: Biệt danh đội tuyển Pháp"),
    ("Inter Miami", "In-tơ Mai-a-mi", "In tơ Mai a mi", "Câu lạc bộ", "Cảnh 05: CLB của Messi tại Mỹ"),
    ("MLS", "Em-en-ét", "Em en ét", "Giải đấu", "Cảnh 05: Giải Nhà nghề Mỹ"),
    ("El Pulga", "En Pun-ga", "En Pun ga", "Biệt danh", "Cảnh 05: Biệt danh của Lionel Messi"),

    # Cảnh 6: Yashin Trophy & Thủ môn
    ("Yashin Trophy", "Cúp Y-a-sin", "Cúp Y a sin", "Giải thưởng", "Cảnh 06: Găng tay vàng thế giới"),
    ("Gianluigi Donnarumma", "Gian-lui-gi Đôn-na-rum-ma", "Gian lui gi Đôn na rum ma", "Thủ môn", "Cảnh 06: Đương kim giữ cúp Yashin"),
    ("Unai Simón", "U-nai Xi-môn", "U nai Xi môn", "Thủ môn", "Cảnh 06: Thủ môn vô địch World Cup 2026"),
    ("Joan García", "Ho-an Gác-xi-a", "Ho an Gác xi a", "Thủ môn", "Cảnh 06: Thủ môn đoạt giải Zamora"),
    ("David Raya", "Đa-vít Ray-a", "Đa vít Ray a", "Thủ môn", "Cảnh 06: Thủ môn Arsenal"),
    ("Arsenal", "Ác-sơ-nân", "Ác sơ nân", "Câu lạc bộ", "Cảnh 06: CLB Arsenal"),
    ("Zamora", "Da-mô-ra", "Da mô ra", "Giải thưởng", "Cảnh 06: Giải thủ môn ít thủng lưới nhất La Liga"),
    ("Vozinha", "Vô-din-nha", "Vô din nha", "Thủ môn", "Cảnh 06: Thủ môn kỳ cựu Cape Verde"),

    # Cảnh 7: Bóng vàng nữ & Putellas
    ("Aitana Bonmatí", "Ai-ta-na Bôn-ma-ti", "Ai ta na Bôn ma ti", "Cầu thủ nữ", "Cảnh 07: Vô địch 3 năm vắng mặt do chấn thương"),
    ("Alexia Putellas", "A-lếch-xi-a Pu-tê-giát", "A lếch xi a Pu tê giát", "Cầu thủ nữ", "Cảnh 07: Đứng trước Quả bóng Vàng nữ thứ 3"),
    ("Liga F", "Li-ga Ép", "Li ga Ép", "Giải đấu nữ", "Cảnh 07: Giải VĐQG nữ Tây Ban Nha"),
    ("London City Lionesses", "Lân-đơn Xi-ti Lai-ơn-nét", "Lân đơn Xi ti Lai ơn nét", "Câu lạc bộ nữ", "Cảnh 07: CLB mới của Putellas tại Anh"),
    ("Ewa Pajor", "Ê-va Pa-gió", "Ê va Pa gió", "Cầu thủ nữ", "Cảnh 07: Sát thủ Ba Lan của Barcelona"),
    ("Khadija Shaw", "Kha-đi-gia Xo", "Kha đi gia Xo", "Cầu thủ nữ", "Cảnh 07: Sát thủ Manchester City"),
    ("Manchester City", "Man-che-xtơ Xi-ti", "Man che xtơ Xi ti", "Câu lạc bộ", "Cảnh 07: CLB Man City"),
    ("Melchie Dumornay", "Men-chi Đuy-mo-nây", "Men chi Đuy mo nây", "Cầu thủ nữ", "Cảnh 07: Ngôi sao trẻ Lyon"),
    ("Olympique Lyon", "Ô-lim-pích Li-ông", "Ô lim pích Li ông", "Câu lạc bộ nữ", "Cảnh 07: CLB Lyon nước Pháp"),
    ("Socrates Award", "Giải thưởng Xô-cơ-rát", "Giải thưởng Xô cơ rát", "Giải thưởng", "Cảnh 07: Giải cống hiến thiện nguyện"),

    # Cảnh 8: Tổng kết & Biểu tượng
    ("Ballon d'Or", "Ba-lông Đo", "Ba lông Đo", "Giải thưởng", "Cảnh 08: Giải thưởng Quả bóng Vàng"),
    ("Cristiano Ronaldo", "Cờ-rít-ti-a-nô Rô-nan-đô", "Cờ rít ti a nô Rô nan đô", "Huyền thoại", "Cảnh 08: Huyền thoại 5 Quả bóng Vàng"),
    ("Johan Cruyff", "Giô-han Cờ-rúp", "Giô han Cờ rúp", "Huyền thoại", "Cảnh 08: Huyền thoại 3 Quả bóng Vàng"),
    ("Inter Milan", "In-tơ Mi-lan", "In tơ Mi lan", "Câu lạc bộ", "Cảnh 08: CLB Inter Milan")
]

def generate_danh_sach_txt():
    txt_path = os.path.join(OUT_DIR, "danh-sach.txt")
    print(f"-> Tạo file danh mục so sánh: {txt_path}")
    
    lines = []
    lines.append("=" * 100)
    lines.append("     BẢNG ĐỐI CHIẾU CÁC TÊN RIÊNG & THUẬT NGỮ ĐƯỢC PHIÊN ÂM CHO GIỌNG ĐỌC TTS")
    lines.append("                  KỊCH BẢN BẢN TIN THỂ THAO NGÀY 22.10.2026")
    lines.append("=" * 100)
    lines.append("")
    lines.append("MỤC ĐÍCH:")
    lines.append("File này dùng để đối chiếu 3 phương pháp đọc tên ngoại quốc trên mô hình ViTTS Minh Quân Pro:")
    lines.append("  1. Phiên âm lúc đầu (có dấu gạch): Đọc ngắt âm từng âm tiết (Ví dụ: Pa - la - di - um). Nhịp đọc chậm và rõ ràng từng âm.")
    lines.append("  2. Phiên âm không gạch (viết liền): Đọc liền mạch tự nhiên (Ví dụ: Pa la đi um). Tốc độ đọc nhanh, trôi chảy, không khựng giữa âm.")
    lines.append("  3. Đọc thô (để nguyên gốc tiếng Anh/quốc tế): Để nguyên từ gốc ngoại quốc cho TTS tự đọc trực tiếp (Ví dụ: Palladium).")
    lines.append("")
    lines.append("CÁC FILE AUDIO KÈM THEO TRONG THƯ MỤC text-audio/ (Có khoảng nghỉ 0.9s giữa các từ để dễ phân biệt):")
    lines.append("  - 01_phien_am_co_gach_luc_dau.wav   (.mp3): Đọc toàn bộ theo Phiên Âm Có Gạch Nối")
    lines.append("  - 02_phien_am_khong_gach_lien_mach.wav (.mp3): Đọc toàn bộ theo Phiên Âm Không Gạch (Viết Liền)")
    lines.append("  - 03_doc_tho_nguyen_ban.wav         (.mp3): Đọc toàn bộ theo Từ Gốc Nguyên Bản (Đọc Thô)")
    lines.append("")
    lines.append("-" * 100)
    lines.append(f"{'STT':<4} | {'TỪ GỐC (ĐỌC THÔ)':<25} | {'PHIÊN ÂM CÓ GẠCH (LÚC ĐẦU)':<30} | {'PHIÊN ÂM KHÔNG GẠCH':<28} | {'PHÂN LOẠI'}")
    lines.append("-" * 100)

    for idx, (disp, say_hyphen, say_no_hyphen, cat, ctx) in enumerate(TERMS_DATA, start=1):
        lines.append(f"{idx:<4} | {disp:<25} | {say_hyphen:<30} | {say_no_hyphen:<28} | {cat}")

    lines.append("-" * 100)
    lines.append("")
    lines.append("=" * 100)
    lines.append("CHI TIẾT NGỮ CẢNH XUẤT HIỆN TRONG KỊCH BẢN:")
    lines.append("=" * 100)
    for idx, (disp, say_hyphen, say_no_hyphen, cat, ctx) in enumerate(TERMS_DATA, start=1):
        lines.append(f"[{idx:02d}] {disp} -> {say_no_hyphen} ({cat})")
        lines.append(f"     + Phiên âm lúc đầu : \"{say_hyphen}\"")
        lines.append(f"     + Phiên âm không gạch: \"{say_no_hyphen}\"")
        lines.append(f"     + Đọc thô nguyên bản : \"{disp}\"")
        lines.append(f"     + Ngữ cảnh trong bài : {ctx}")
        lines.append("")

    content = "\n".join(lines)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✨ Đã lưu danh sách: {txt_path} ({len(content):,} ký tự)")

def render_comparison_audios():
    print("\n-> Khởi tạo mô hình ViTTS v3turbo Minh Quân Pro...")
    model = Vieneu(mode="v3turbo")

    pause_audio = AudioSegment.silent(duration=900, frame_rate=44100) # 0.9s khoảng nghỉ giữa các từ

    streams = {
        "01_phien_am_co_gach_luc_dau": {
            "title": "Bản 01: Phiên âm có dấu gạch (lúc đầu)",
            "words": [item[1] for item in TERMS_DATA]
        },
        "02_phien_am_khong_gach_lien_mach": {
            "title": "Bản 02: Phiên âm viết liền không dấu gạch",
            "words": [item[2] for item in TERMS_DATA]
        },
        "03_doc_tho_nguyen_ban": {
            "title": "Bản 03: Đọc thô để nguyên từ gốc tiếng Anh/quốc tế",
            "words": [item[0] for item in TERMS_DATA]
        }
    }

    for key, sdata in streams.items():
        print(f"\n==================================================")
        print(f"Bắt đầu tổng hợp âm thanh: {sdata['title']}")
        print(f"==================================================")

        combined = AudioSegment.empty()
        words_list = sdata["words"]
        total = len(words_list)

        for i, word in enumerate(words_list, start=1):
            seg, _ = render_chunk_vitts(model, word, "Minh Quân Pro", temperature=0.5, speed=1.15, pitch=1.0, cache_dir=TTS_CACHE, use_cache=False)
            seg = trim_segment_silence(seg)
            combined += seg

            # Thêm khoảng nghỉ nhỏ giữa các từ (trừ từ cuối cùng)
            if i < total:
                combined += pause_audio

            if i % 10 == 0 or i == total:
                print(f"  ... Đã đọc {i}/{total} từ ({len(combined)/1000.0:.1f}s)")

        dur_sec = len(combined) / 1000.0
        mins = int(dur_sec // 60)
        secs = int(dur_sec % 60)
        print(f"  -> Hoàn thành track: {dur_sec:.1f}s ({mins:02d}:{secs:02d})")

        # Xuất file WAV
        wav_path = os.path.join(OUT_DIR, f"{key}.wav")
        combined.set_frame_rate(44100).set_channels(2).normalize(headroom=0.1).export(wav_path, format="wav")
        print(f"  ✨ Xuất file WAV: {wav_path} ({os.path.getsize(wav_path):,} bytes)")

        # Xuất thêm file MP3 tiện nghe trên mọi thiết bị
        mp3_path = os.path.join(OUT_DIR, f"{key}.mp3")
        try:
            combined.export(mp3_path, format="mp3", bitrate="192k")
            print(f"  ✨ Xuất file MP3: {mp3_path} ({os.path.getsize(mp3_path):,} bytes)")
        except Exception as e:
            # Fallback ffmpeg
            cmd = ["ffmpeg", "-y", "-i", wav_path, "-b:a", "192k", mp3_path]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(mp3_path):
                print(f"  ✨ Xuất file MP3 (ffmpeg): {mp3_path} ({os.path.getsize(mp3_path):,} bytes)")

def main():
    generate_danh_sach_txt()
    render_comparison_audios()
    print("\n🎉 HOÀN TẤT TẤT CẢ FILE SO SÁNH TRONG:", OUT_DIR)

if __name__ == "__main__":
    main()
