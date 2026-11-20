#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True

import os, json, time, shutil, subprocess, random
from typing import List, Dict, Any
from pydub import AudioSegment
from playwright.sync_api import sync_playwright

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_ROOT, "engines", "html"))

from diemdoc import paths
from diemdoc.tts_text import prepare
from diemdoc.sync import syllabic_estimate, group_karaoke_chunks
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from vieneu import Vieneu
from renderer import render_html_engine

DAY_DIR = os.path.join(_ROOT, "outputs", "22.10.2026")
SHORTS_OUT_DIR = os.path.join(DAY_DIR, "shorts")
WORK_DIR = os.path.expanduser("~/Library/Caches/DiemDoc/22.10.2026/shorts_04_05")
os.makedirs(SHORTS_OUT_DIR, exist_ok=True)
os.makedirs(WORK_DIR, exist_ok=True)

TTS_CACHE = paths.work_file("vitts_cache")
KB_POOL = ["zoom_in", "zoom_out", "pan_left", "pan_right", "tilt_up", "tilt_down"]

SHORTS_DEFS = [
    {
        "id": "short_04",
        "out_name": "Short_04_Doi_Trong_Kylian_Mbappe_vs_Lionel_Messi.mp4",
        "title": "Kylian Mbappé và Lionel Messi tiếp tục khẳng định vị thế đối trọng nặng ký trong đêm vinh danh",
        "group": "QUẢ BÓNG VÀNG 2026",
        "credit": "REUTERS / GETTY IMAGES",
        "sentences": [
            {
                "text": "Cuộc đua danh giá tới danh hiệu Quả bóng Vàng 2026 sẽ không thể trọn vẹn nếu thiếu đi sự hiện diện đầy uy quyền của hai siêu sao kiệt xuất là Ki-li-an Em-ba-pê và huyền thoại sống Li-ô-nen Méc-xi.",
                "display": "Cuộc đua danh giá tới danh hiệu Quả bóng Vàng 2026 sẽ không thể trọn vẹn nếu thiếu đi sự hiện diện đầy uy quyền của hai siêu sao kiệt xuất là Kylian Mbappe và huyền thoại sống Lionel Messi.",
                "images": ["Tin_05_4.jpg"],
                "keywords": ["Quả bóng Vàng 2026", "Kylian Mbappe", "Lionel Messi"]
            },
            {
                "text": "Sau mùa giải ra mắt thăng hoa rực rỡ trong màu áo trắng Rê-an Ma-đrít, Em-ba-pê tiếp tục khẳng định vị thế cỗ máy săn bàn hàng đầu hành tinh với hiệu suất nhả đạn hủy diệt tại cả La Li-ga lẫn đấu trường cúp Cê một danh giá.",
                "display": "Sau mùa giải ra mắt thăng hoa rực rỡ trong màu áo trắng Real Madrid, Mbappe tiếp tục khẳng định vị thế cỗ máy săn bàn hàng đầu hành tinh với hiệu suất nhả đạn hủy diệt tại cả La Liga lẫn đấu trường UEFA Champions League.",
                "images": ["Tin_05_5.jpg", "Tin_05_6.jpg"],
                "keywords": ["Real Madrid", "Mbappe", "La Liga", "Champions League"]
            },
            {
                "text": "Dưới sự nhào nặn tài tình của huấn luyện viên Cát-lô An-chê-lốt-ti, tiền đạo người Pháp đã hoàn thiện bộ kỹ năng dứt điểm sắc bén, lĩnh xướng hàng công và mang về danh hiệu Siêu cúp châu Âu cho đội bóng Hoàng gia Tây Ban Nha.",
                "display": "Dưới sự nhào nặn tài tình của huấn luyện viên Carlo Ancelotti, tiền đạo người Pháp đã hoàn thiện bộ kỹ năng dứt điểm sắc bén, lĩnh xướng hàng công và mang về danh hiệu Siêu cúp châu Âu cho đội bóng Hoàng gia Tây Ban Nha.",
                "images": ["Tin_05_7.jpg"],
                "keywords": ["Carlo Ancelotti", "tiền đạo người Pháp", "Siêu cúp châu Âu"]
            },
            {
                "text": "Không chỉ vậy, danh hiệu cá nhân cao quý Ông-dơ Đò 2026 mà Em-ba-pê vừa nhận được từ tạp chí uy tín của Pháp ngay trước thềm gala chính là minh chứng rõ nét nhất cho đẳng cấp và sự bùng nổ không ngừng nghỉ của anh.",
                "display": "Không chỉ vậy, danh hiệu cá nhân cao quý Onze d'Or 2026 mà Mbappe vừa nhận được từ tạp chí uy tín của Pháp ngay trước thềm gala chính là minh chứng rõ nét nhất cho đẳng cấp và sự bùng nổ không ngừng nghỉ của anh.",
                "images": ["Tin_05_8.jpg"],
                "keywords": ["Onze d'Or 2026", "tạp chí uy tín", "bùng nổ"]
            },
            {
                "text": "Dù đội tuyển Pháp phải ngậm ngùi dừng bước trước Tây Ban Nha tại bán kết World Cup, tiền đạo số 9 vẫn kịp thiết lập cột mốc lịch sử khi trở thành chân sút vĩ đại nhất mọi thời đại của Lê B-lơ trên đấu trường quốc tế.",
                "display": "Dù đội tuyển Pháp phải ngậm ngùi dừng bước trước Tây Ban Nha tại bán kết World Cup, tiền đạo số 9 vẫn kịp thiết lập cột mốc lịch sử khi trở thành chân sút vĩ đại nhất mọi thời đại của Les Bleus trên đấu trường quốc tế.",
                "images": ["Tin_05_9.jpg", "Tin_05_10.jpg"],
                "keywords": ["đội tuyển Pháp", "World Cup", "chân sút vĩ đại", "Les Bleus"]
            },
            {
                "text": "Trong khi đó, ở tuổi 39 trong màu áo In-tơ Mai-a-mi, Li-ô-nen Méc-xi vẫn chứng minh đẳng cấp thiên tài vượt qua mọi giới hạn thời gian khi tiếp tục góp mặt đầy trang trọng trong danh sách 30 đề cử rút gọn cuối cùng.",
                "display": "Trong khi đó, ở tuổi 39 trong màu áo Inter Miami, Lionel Messi vẫn chứng minh đẳng cấp thiên tài vượt qua mọi giới hạn thời gian khi tiếp tục góp mặt đầy trang trọng trong danh sách 30 đề cử rút gọn cuối cùng.",
                "images": ["Tin_05_11.jpg"],
                "keywords": ["tuổi 39", "Inter Miami", "Lionel Messi", "30 đề cử"]
            },
            {
                "text": "Dù đang thi đấu tại giải Nhà nghề Mỹ Em-en-ét, En Pun-ga vẫn tỏa sáng rực rỡ, mê hoặc hàng triệu khán giả và đưa đội tuyển Argentina tiến sâu tại ngày hội bóng đá Bắc Mỹ bằng những đường chuyền ma thuật cùng những khoảnh khắc xoay chuyển cục diện xuất thần.",
                "display": "Dù đang thi đấu tại giải Nhà nghề Mỹ MLS, El Pulga vẫn tỏa sáng rực rỡ, mê hoặc hàng triệu khán giả và đưa đội tuyển Argentina tiến sâu tại ngày hội bóng đá Bắc Mỹ bằng những đường chuyền ma thuật cùng những khoảnh khắc xoay chuyển cục diện xuất thần.",
                "images": ["Tin_05_12.jpg"],
                "keywords": ["MLS", "El Pulga", "Argentina", "Bắc Mỹ"]
            },
            {
                "text": "Với bộ sưu tập kỷ lục 8 Quả bóng Vàng vô tiền khoáng hậu, Méc-xi vẫn là tượng đài bất tử, trong khi Em-ba-pê đang khát khao cháy bỏng có lần đầu tiên bước lên đỉnh vinh quang thế giới.",
                "display": "Với bộ sưu tập kỷ lục 8 Quả bóng Vàng vô tiền khoáng hậu, Messi vẫn là tượng đài bất tử, trong khi Mbappe đang khát khao cháy bỏng có lần đầu tiên bước lên đỉnh vinh quang thế giới.",
                "images": ["Tin_05_3.jpg"],
                "keywords": ["8 Quả bóng Vàng", "tượng đài bất tử", "đỉnh vinh quang"]
            },
            {
                "text": "Sự xuất hiện của Méc-xi và Em-ba-pê trên hàng ghế danh dự tại London Pa la đi um không chỉ mang lại sức hút truyền thông nghẹt thở cho buổi lễ mà còn là biểu tượng hoàn hảo cho sự giao thoa lịch sử giữa di sản trường tồn của quá khứ và đỉnh cao quyền lực bóng đá đương đại.",
                "display": "Sự xuất hiện của Messi và Mbappe trên hàng ghế danh dự tại London Palladium không chỉ mang lại sức hút truyền thông nghẹt thở cho buổi lễ mà còn là biểu tượng hoàn hảo cho sự giao thoa lịch sử giữa di sản trường tồn của quá khứ và đỉnh cao quyền lực bóng đá đương đại.",
                "images": ["Tin_05_13.jpg", "Tin_05_14.jpg"],
                "keywords": ["London Palladium", "truyền thông", "di sản trường tồn"]
            },
            {
                "text": "Liệu Em-ba-pê có lần đầu chạm tay vào Quả bóng Vàng, hay huyền thoại Méc-xi sẽ tạo nên bất ngờ lớn nhất tại thánh đường Pa la đi um? Hãy để lại bình luận dự đoán của bạn và đăng ký kênh Điểm Đọc nhé!",
                "display": "Liệu Mbappe có lần đầu chạm tay vào Quả bóng Vàng, hay huyền thoại Messi sẽ tạo nên bất ngờ lớn nhất tại thánh đường London Palladium? Hãy để lại bình luận dự đoán của bạn và đăng ký kênh Điểm Đọc nhé!",
                "images": ["Tin_05_1.jpg", "Tin_05_2.jpg"],
                "keywords": ["London Palladium", "Quả bóng Vàng", "bình luận"]
            }
        ]
    },
    {
        "id": "short_05",
        "out_name": "Short_05_Cu_Soc_Qua_Bong_Vang_Nu_Bonmati_vs_Putellas.mp4",
        "title": "Aitana Bonmatí vắng bóng sau 3 năm thống trị và cơ hội vàng mở ra cho Alexia Putellas",
        "group": "QUẢ BÓNG VÀNG NỮ",
        "credit": "REUTERS / GETTY IMAGES",
        "sentences": [
            {
                "text": "Bất ngờ chấn động và gây tiếc nuối sâu sắc nhất tại lễ trao giải Quả bóng Vàng năm nay xuất hiện ở hạng mục dành cho nữ, khi nhà đương kim vô địch ba năm liên tiếp Ai-ta-na Bôn-ma-ti hoàn toàn vắng bóng trong danh sách 30 đề cử cuối cùng.",
                "display": "Bất ngờ chấn động và gây tiếc nuối sâu sắc nhất tại lễ trao giải Quả bóng Vàng năm nay xuất hiện ở hạng mục dành cho nữ, khi nhà đương kim vô địch ba năm liên tiếp Aitana Bonmati hoàn toàn vắng bóng trong danh sách 30 đề cử cuối cùng.",
                "images": ["Tin_07_4.jpg", "Tin_07_5.jpg"],
                "keywords": ["Quả bóng Vàng", "Aitana Bonmati", "vắng bóng", "30 đề cử"]
            },
            {
                "text": "Chấn thương gãy xương mác nghiêm trọng trong một buổi tập vào tháng 11 năm ngoái đã buộc nhạc trưởng tài hoa của Bác-xa phải trải qua ca phẫu thuật phức tạp và bước vào quãng thời gian điều trị phục hồi suốt hơn nửa năm ròng rã.",
                "display": "Chấn thương gãy xương mác nghiêm trọng trong một buổi tập vào tháng 11 năm ngoái đã buộc nhạc trưởng tài hoa của Barcelona phải trải qua ca phẫu thuật phức tạp và bước vào quãng thời gian điều trị phục hồi suốt hơn nửa năm ròng rã.",
                "images": ["Tin_07_6.jpg", "Tin_07_7.jpg"],
                "keywords": ["chấn thương", "Barcelona", "phẫu thuật", "nghỉ thi đấu"]
            },
            {
                "text": "Dù kịp nỗ lực trở lại sân cỏ vào tháng 5 để cùng câu lạc bộ xứ Catalan hoàn tất cú ăn bốn lịch sử ngoạn mục gồm cúp Cê một nữ và Li-ga Ép, nhưng thời lượng thi đấu ít ỏi đã không đủ giúp Bôn-ma-ti bảo vệ ngai vàng cá nhân danh giá của mình.",
                "display": "Dù kịp nỗ lực trở lại sân cỏ vào tháng 5 để cùng câu lạc bộ xứ Catalan hoàn tất cú ăn bốn lịch sử ngoạn mục gồm UEFA Women's Champions League và Liga F, nhưng thời lượng thi đấu ít ỏi đã không đủ giúp Bonmati bảo vệ ngai vàng cá nhân danh giá của mình.",
                "images": ["Tin_07_8.jpg", "Tin_07_9.jpg"],
                "keywords": ["cú ăn bốn", "Champions League nữ", "Liga F", "Bonmati"]
            },
            {
                "text": "Sự vắng bóng đầy tiếc nuối của tiền vệ số một thế giới đã mở toang cánh cửa vinh quang cho người đồng đội thân thiết A-lếch-xi-a Pu-tê-giát, người đang đứng trước cơ hội lịch sử giành Quả bóng Vàng nữ thứ ba trong sự nghiệp lẫy lừng sau khi chuyển sang khoác áo câu lạc bộ Lân-đơn Xi-ti Lai-ơn-nét tại giải bóng đá nữ nước Anh.",
                "display": "Sự vắng bóng đầy tiếc nuối của tiền vệ số một thế giới đã mở toang cánh cửa vinh quang cho người đồng đội thân thiết Alexia Putellas, người đang đứng trước cơ hội lịch sử giành Quả bóng Vàng nữ thứ ba trong sự nghiệp lẫy lừng sau khi chuyển sang khoác áo câu lạc bộ London City Lionesses tại giải bóng đá nữ nước Anh.",
                "images": ["Tin_07_10.jpg", "Tin_07_11.jpg"],
                "keywords": ["Alexia Putellas", "Quả bóng Vàng nữ", "London City Lionesses"]
            },
            {
                "text": "Pu-tê-giát sẽ phải cạnh tranh vô cùng quyết liệt với những cỗ máy săn bàn thượng thặng gồm tiền đạo người Ba Lan Ê-va Pa-gió, chân sút đã ghi hàng loạt bàn thắng quyết định cho Bác-xa tại đấu trường cúp Cê một nữ, cùng sát thủ cự phách Kha-đi-gia Xo của Man-che-xtơ Xi-ti, người vừa phá kỷ lục ghi bàn tại giải Vô địch Quốc gia Anh.",
                "display": "Putellas sẽ phải cạnh tranh vô cùng quyết liệt với những cỗ máy săn bàn thượng thặng gồm tiền đạo người Ba Lan Ewa Pajor, chân sút đã ghi hàng loạt bàn thắng quyết định cho Barcelona tại đấu trường Champions League nữ, cùng sát thủ cự phách Khadija Shaw của Manchester City, người vừa phá kỷ lục ghi bàn tại giải Vô địch Quốc gia Anh.",
                "images": ["Tin_07_12.jpg", "Tin_07_13.jpg"],
                "keywords": ["Ewa Pajor", "Barcelona", "Khadija Shaw", "Manchester City"]
            },
            {
                "text": "Bên cạnh đó, tiền vệ trẻ đầy bùng nổ Men-chi Đuy-mo-nây của Ô-lim-pích Li-ông cũng được giới chuyên môn đánh giá là ứng viên vô cùng nặng ký sau một mùa giải thi đấu thăng hoa rực rỡ tại giải vô địch nước Pháp.",
                "display": "Bên cạnh đó, tiền vệ trẻ đầy bùng nổ Melchie Dumornay của Olympique Lyon cũng được giới chuyên môn đánh giá là ứng viên vô cùng nặng ký sau một mùa giải thi đấu thăng hoa rực rỡ tại giải vô địch nước Pháp.",
                "images": ["Tin_07_14.jpg"],
                "keywords": ["Melchie Dumornay", "Olympique Lyon", "ứng viên nặng ký"]
            },
            {
                "text": "Bên cạnh giải thưởng chính, đêm gala cũng sẽ dành những tràng pháo tay trang trọng nhất cho giải thưởng Xô-cơ-ra-tét nhằm tôn vinh những cầu thủ bóng đá nữ có đóng góp nhân đạo và hoạt động thiện nguyện nổi bật cho cộng đồng toàn cầu.",
                "display": "Bên cạnh giải thưởng chính, đêm gala cũng sẽ dành những tràng pháo tay trang trọng nhất cho giải thưởng Socrates Award nhằm tôn vinh những cầu thủ bóng đá nữ có đóng góp nhân đạo và hoạt động thiện nguyện nổi bật cho cộng đồng toàn cầu.",
                "images": ["Tin_07_15.jpg", "Tin_07_3.jpg"],
                "keywords": ["Socrates Award", "nhân đạo", "thiện nguyện"]
            },
            {
                "text": "Sự thống trị của bóng đá nữ Tây Ban Nha suốt nửa thập kỷ qua đang đứng trước bước ngoặt mới khi các đối thủ từ Anh và Pháp ngày càng bám đuổi quyết liệt, khiến cuộc đua năm nay trở nên nghẹt thở hơn bao giờ hết.",
                "display": "Sự thống trị của bóng đá nữ Tây Ban Nha suốt nửa thập kỷ qua đang đứng trước bước ngoặt mới khi các đối thủ từ Anh và Pháp ngày càng bám đuổi quyết liệt, khiến cuộc đua năm nay trở nên nghẹt thở hơn bao giờ hết.",
                "images": ["Tin_07_2.jpg"],
                "keywords": ["Tây Ban Nha", "bước ngoặt", "nghẹt thở"]
            },
            {
                "text": "Liệu Pu-tê-giát có lần thứ ba nâng cao Quả bóng Vàng, hay danh hiệu sẽ thuộc về một gương mặt mới tại thánh đường Pa la đi um? Hãy để lại bình luận dự đoán của bạn và đăng ký kênh Điểm Đọc nhé!",
                "display": "Liệu Putellas có lần thứ ba nâng cao Quả bóng Vàng, hay danh hiệu sẽ thuộc về một gương mặt mới tại thánh đường London Palladium? Hãy để lại bình luận dự đoán của bạn và đăng ký kênh Điểm Đọc nhé!",
                "images": ["Tin_07_1.jpg"],
                "keywords": ["London Palladium", "Quả bóng Vàng nữ", "bình luận"]
            }
        ]
    }
]

def synthesize_sentence(model: Vieneu, text: str, voice="Minh Quân Pro", speed=1.15, pitch=1.0) -> AudioSegment:
    clean_text, _ = prepare(text)
    chunks = build_chunks_from_text(clean_text, max_words_per_chunk=60, inter_sentence_pause=0.25)
    combined = AudioSegment.empty()
    for c in chunks:
        if c.get("type") == "pause":
            pause_ms = int(c.get("pause_sec", 0.3) * 1000)
            if pause_ms > 0:
                combined += AudioSegment.silent(duration=pause_ms, frame_rate=44100)
            continue
        c_text = c.get("text", "").strip()
        if not c_text:
            continue
        seg, _ = render_chunk_vitts(model, c_text, voice, temperature=0.5, speed=speed, pitch=pitch, cache_dir=TTS_CACHE, use_cache=False)
        seg = trim_segment_silence(seg)
        combined += seg
    return combined

def build_thumbnails():
    print("\n=== TẠO BỘ 2 ẢNH THUMBNAIL DỌC 9:16 CHO SHORT 04 VÀ SHORT 05 ===")
    assets_url = "file://" + os.path.join(_ROOT, "assets")
    logo_url = "file://" + os.path.join(_ROOT, "assets", "logo", "diem-doc-logo-1.png")

    thumbs_spec = [
        {
            "file_out": "Short_04_thumbnail.jpg",
            "image": "file://" + os.path.join(DAY_DIR, "images", "Tin_05_1.jpg"),
            "kicker": "ĐỐI TRỌNG CẠNH TRANH",
            "hero": "MBAPPÉ VS MESSI",
            "hero_size": "105",
            "subtitle": "VỊ THẾ SIÊU SAO ĐÊM VINH DANH",
            "tag_a": "BALLON D'OR 2026",
            "tag_b": "REAL & INTER MIAMI"
        },
        {
            "file_out": "Short_05_thumbnail.jpg",
            "image": "file://" + os.path.join(DAY_DIR, "images", "Tin_07_1.jpg"),
            "kicker": "CÚ SỐC BÓNG VÀNG NỮ",
            "hero": "VẮNG BONMATÍ!",
            "hero_size": "115",
            "subtitle": "CƠ HỘI VÀNG CHO PUTELLAS",
            "tag_a": "BALLON D'OR 2026",
            "tag_b": "LỊCH SỬ NỮ 2026"
        }
    ]

    tpl_html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  @font-face { font-family:'Anton'; src:url('__ASSETS__/fonts/Anton/Anton-Regular.ttf'); font-weight:400; }
  @font-face { font-family:'Oswald'; src:url('__ASSETS__/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; }
  @font-face { font-family:'Oswald'; src:url('__ASSETS__/fonts/Oswald/static/Oswald-SemiBold.ttf'); font-weight:600; }
  @font-face { font-family:'PlexMono'; src:url('__ASSETS__/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'); font-weight:700; }

  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1080px; height:1920px; overflow:hidden; background:#05070C; }
  body { font-family:'Oswald', sans-serif; position:relative; }

  /* NỬA TRÊN: ẢNH 58% */
  .top {
    position:absolute; top:0; left:0; right:0; height:58%;
    overflow:hidden; background:#080B12;
  }
  .top img.hero-bg {
    width:100%; height:100%; object-fit:cover; object-position:center 20%;
    filter: contrast(1.15) brightness(1.02) saturate(1.18);
  }
  .top::after {
    content:''; position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(5,7,12,0.2) 0%, transparent 20%, rgba(5,7,12,0.65) 70%, #05070C 100%);
  }

  .badge {
    position:absolute; top:56px; left:56px; z-index:5;
    display:flex; align-items:center; gap:16px;
    padding:16px 28px; border-radius:999px;
    background:rgba(5,7,12,0.75); border:2px solid rgba(255,194,77,0.8);
    box-shadow: 0 4px 20px rgba(0,0,0,0.6), 0 0 15px rgba(255,194,77,0.3);
    backdrop-filter:blur(12px);
  }
  .badge img { height:40px; width:auto; border-radius:50%; }
  .badge span {
    font-family:'Oswald'; font-weight:700; font-size:24px;
    letter-spacing:4px; color:#FFC24D; text-transform:uppercase;
  }

  /* NỬA DƯỚI: SÂN KHẤU 42% */
  .bottom {
    position:absolute; bottom:0; left:0; right:0; height:43%;
    background:#05070C; padding:40px 70px 70px;
    display:flex; flex-direction:column; justify-content:center;
    border-top: 1px solid rgba(255,194,77,0.15);
  }
  .kicker {
    font-family:'PlexMono'; font-weight:700; font-size:26px;
    letter-spacing:5px; color:#28E0D0; margin-bottom:14px;
    text-transform:uppercase;
    text-shadow: 0 0 12px rgba(40,224,208,0.4);
  }
  .hero {
    font-family:'Anton'; font-size:__THUMB_HERO_SIZE__px; line-height:0.95;
    letter-spacing:1px;
    color:#FFFFFF; white-space:nowrap;
    text-shadow:0 0 50px rgba(255,194,77,0.4), 0 4px 10px rgba(0,0,0,0.8);
  }
  .hero .accent { color:#FFC24D; }
  .sub {
    font-family:'Oswald'; font-weight:700; font-size:46px; line-height:1.15;
    color:#F3F6FF; margin-top:16px; text-transform:uppercase; letter-spacing:1px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
  }
  .rule {
    height:6px; width:180px;
    background:linear-gradient(90deg, #FFC24D 0%, #28E0D0 100%);
    margin:24px 0 20px; border-radius:3px;
    box-shadow: 0 0 10px rgba(255,194,77,0.5);
  }
  .meta {
    display:flex; gap:36px; align-items:center;
    font-family:'PlexMono'; font-size:22px; font-weight:700; letter-spacing:2px;
    color:#94A0BE;
  }
  .meta b { color:#FFC24D; }
</style>
</head>
<body>
  <div class="top">
    <div class="badge">
      <img src="__LOGO__" alt="Logo">
      <span>ĐIỂM ĐỌC</span>
    </div>
    <img class="hero-bg" src="__THUMB_IMAGE__" alt="">
  </div>

  <div class="bottom">
    <div class="kicker">__THUMB_KICKER__</div>
    <div class="hero">__THUMB_HERO__</div>
    <div class="sub">__THUMB_SUBTITLE__</div>
    <div class="rule"></div>
    <div class="meta">
      <span>__THUMB_TAG_A__</span>
      <span><b>__THUMB_TAG_B__</b></span>
    </div>
  </div>
</body>
</html>
"""

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        page = br.new_page(viewport={"width": 1080, "height": 1920})

        for spec in thumbs_spec:
            html = tpl_html.replace("__ASSETS__", assets_url)
            html = html.replace("__LOGO__", logo_url)
            html = html.replace("__THUMB_IMAGE__", spec["image"])
            html = html.replace("__THUMB_KICKER__", spec["kicker"])
            html = html.replace("__THUMB_HERO__", spec["hero"])
            html = html.replace("__THUMB_HERO_SIZE__", spec["hero_size"])
            html = html.replace("__THUMB_SUBTITLE__", spec["subtitle"])
            html = html.replace("__THUMB_TAG_A__", spec["tag_a"])
            html = html.replace("__THUMB_TAG_B__", spec["tag_b"])

            tmp_html = f"/tmp/{spec['file_out']}.html"
            with open(tmp_html, "w", encoding="utf-8") as f:
                f.write(html)

            out_path = os.path.join(SHORTS_OUT_DIR, spec["file_out"])
            page.goto("file://" + tmp_html, wait_until="networkidle")
            page.screenshot(path=out_path, type="jpeg", quality=95)
            print(f"  ✨ Đã tạo thumbnail chuẩn: {spec['file_out']} ({os.path.getsize(out_path):,} bytes)")

        br.close()

def main():
    print("=== SẢN XUẤT SHORT 04 (CẢNH 05) & SHORT 05 (CẢNH 07) CHUẨN THỜI LƯỢNG 1:30 - 2:30 ===")
    model = Vieneu(mode="v3turbo")
    img_dir = os.path.join(DAY_DIR, "images")

    for s_def in SHORTS_DEFS:
        sid = s_def["id"]
        out_name = s_def["out_name"]
        title = s_def["title"]
        group = s_def["group"]
        credit = s_def["credit"]
        sents_def = s_def["sentences"]

        dest_mp4 = os.path.join(SHORTS_OUT_DIR, out_name)
        proj_dir = os.path.join(WORK_DIR, sid)
        os.makedirs(proj_dir, exist_ok=True)

        print(f"\n==================================================")
        print(f"Xử lý {sid}: {title}")
        print(f"==================================================")

        full_audio = AudioSegment.silent(duration=0, frame_rate=44100)
        gap_audio = AudioSegment.silent(duration=350, frame_rate=44100)

        # Title intro audio (~4-5s)
        t_clean, _ = prepare(title)
        seg_title = synthesize_sentence(model, t_clean, speed=1.15, pitch=1.0)
        full_audio += seg_title + AudioSegment.silent(duration=450, frame_rate=44100)

        title_dur = len(full_audio) / 1000.0

        built_sentences = []
        all_words = []
        cum_sec = title_dur

        # Sentence 0 (Title stage)
        t_words = syllabic_estimate(title, 0.0, title_dur)
        all_words.extend(t_words)

        s0_imgs = [os.path.join(img_dir, sents_def[0]["images"][0])]
        built_sentences.append({
            "sentence_id": 0,
            "text": title,
            "layout": "full",
            "start": 0.0,
            "end": round(title_dur, 3),
            "duration": round(title_dur, 3),
            "keywords": [group],
            "images": [{"src": s0_imgs[0], "start": 0.0, "end": round(title_dur, 3), "duration": round(title_dur, 3), "ken_burns": "zoom_in"}]
        })

        for idx, s in enumerate(sents_def, start=1):
            disp = s["display"]
            txt = s["text"]
            im_names = s["images"]
            kws = s.get("keywords", [])

            seg = synthesize_sentence(model, txt, speed=1.15, pitch=1.0)
            seg_dur = len(seg) / 1000.0

            s_start = cum_sec
            s_end = round(s_start + seg_dur, 3)

            full_audio += seg
            if idx < len(sents_def):
                full_audio += gap_audio
                cum_sec = round(s_end + 0.35, 3)
            else:
                cum_sec = s_end

            w_list = syllabic_estimate(disp, s_start, s_end)
            all_words.extend(w_list)

            im_objs = []
            if len(im_names) == 1:
                p = os.path.join(img_dir, im_names[0])
                kb_chosen = random.choice(KB_POOL)
                im_objs.append({
                    "src": p, "start": s_start, "end": s_end, "duration": round(seg_dur, 3),
                    "ken_burns": kb_chosen
                })
            else:
                half = round(seg_dur / 2.0, 3)
                p1 = os.path.join(img_dir, im_names[0])
                p2 = os.path.join(img_dir, im_names[1])
                kb1 = random.choice(["zoom_in", "pan_left", "tilt_up"])
                kb2 = random.choice(["zoom_out", "pan_right", "tilt_down"])
                im_objs.append({
                    "src": p1, "start": s_start, "end": round(s_start + half, 3), "duration": half,
                    "ken_burns": kb1
                })
                im_objs.append({
                    "src": p2, "start": round(s_start + half, 3), "end": s_end, "duration": round(seg_dur - half, 3),
                    "ken_burns": kb2
                })

            built_sentences.append({
                "sentence_id": idx,
                "text": disp,
                "layout": "full",
                "start": s_start,
                "end": s_end,
                "duration": round(seg_dur, 3),
                "keywords": kws,
                "images": im_objs
            })

        total_dur = cum_sec
        mins = int(total_dur // 60)
        secs = int(total_dur % 60)
        print(f"  -> Tổng thời lượng audio: {total_dur:.2f}s ({mins:02d}:{secs:02d})")
        assert 90.0 <= total_dur <= 150.0, f"Thời lượng {total_dur:.1f}s nằm ngoài dải 1:30 - 2:30 (90s - 150s)"

        voice_wav = os.path.join(proj_dir, "voiceover.wav")
        full_audio.set_frame_rate(44100).set_channels(2).normalize(headroom=0.1).export(voice_wav, format="wav")

        karaoke_chunks = group_karaoke_chunks(all_words, max_chars=26)

        words_data = {
            "words": all_words,
            "karaoke_chunks": karaoke_chunks
        }
        words_path = os.path.join(proj_dir, "word_timestamps.json")
        with open(words_path, "w", encoding="utf-8") as f:
            json.dump(words_data, f, ensure_ascii=False, indent=2)

        timeline = {
            "title": title,
            "group": group,
            "channel_name": "ĐIỂM ĐỌC",
            "date_chip": "THỨ NĂM · 22.10.2026",
            "date_str": "22.10.2026",
            "total_duration": total_dur,
            "format": "short",
            "template": "short_news_v2.html",
            "dimensions": {"width": 1080, "height": 1920},
            "fps": 30,
            "audio_path": voice_wav,
            "credit": credit,
            "global_offset_sec": 0.0,
            "bgm": "bgm_pulse_dark_full.mp3",
            "bgm_volume": 0.05,
            "fx": {
                "sparkles": {"enabled": True, "count": 22, "speed": 0.35, "color": "#F59E0B"},
                "dust": {"enabled": True, "count": 14, "speed": 0.18, "color": "#94A3B8"}
            },
            "sentences": built_sentences,
            "karaoke_chunks": karaoke_chunks
        }
        tl_path = os.path.join(proj_dir, "video_timeline.json")
        with open(tl_path, "w", encoding="utf-8") as f:
            json.dump(timeline, f, ensure_ascii=False, indent=2)

        print(f"  -> Bắt đầu render Playwright Chromium...")
        rendered_mp4 = render_html_engine(proj_dir, template="short_news_v2.html", scene_number=None,
                                          fps=30, preview=False, force=True)

        if not rendered_mp4 or not os.path.exists(rendered_mp4):
            raise RuntimeError(f"Render thất bại cho {sid}")

        shutil.copy2(rendered_mp4, dest_mp4)
        print(f"  🎉 XUẤT THÀNH CÔNG: {dest_mp4} ({os.path.getsize(dest_mp4)} bytes, {mins:02d}:{secs:02d})")

    # Tạo thumbnails typographic chuẩn
    build_thumbnails()

if __name__ == "__main__":
    main()
