#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_shorts_11_11.py — Sản xuất 3 Video Shorts 9:16 ngày 11.11.2026:
1. Man Utd giữ ban lãnh đạo, họp bàn sa thải Carrick & lời cảnh tỉnh của Paul Merson (Giọng Nam: Minh Quân Pro)
2. Người phụ nữ đầu tiên chạy 160 km ở Nam Cực - Stephanie Case (Giọng Nữ: Ngọc Huyền)
3. Trịnh Thu Vinh đoạt vé Olympic 2028 đầu tiên cho thể thao Việt Nam (Giọng Nữ: Ngọc Huyền)
Nguồn: VnExpress (11.11.2026)
"""
import sys
sys.dont_write_bytecode = True

import io
import json
import os
import re
import shutil
import time
from typing import List, Dict, Any, Optional, Tuple
import requests
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
from playwright.sync_api import sync_playwright
from ddgs import DDGS

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "vendor"))

engines_html = os.path.join(_ROOT, "engines", "html")
if engines_html not in sys.path:
    sys.path.insert(0, engines_html)

from diemdoc import paths
from diemdoc.log import banner, ok, step, log, warn, die
from diemdoc.tts_text import prepare
from diemdoc.audio import apply_voice_standard, measure_loudness
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from m8_news_bridge import export_bridge_project
from renderer import render_html_engine
from vieneu import Vieneu

DAY_STR = "11.11.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, "Orther", DAY_STR)
WORK_DIR = paths.work_project_dir(os.path.join("Orther", DAY_STR))

IMG_DIR = os.path.join(DAY_DIR, "images")
AUDIO_DIR = os.path.join(DAY_DIR, "audio")
AUDIO_TITLE_DIR = os.path.join(DAY_DIR, "audio-title")
SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
QA_DIR = os.path.join(DAY_DIR, "qa")
SHORTS_WORK = os.path.join(WORK_DIR, "shorts_render")
CACHE_DIR = paths.work_file("vitts_cache")

MIN_RATIO = 1.15
MIN_WIDTH = 600
MIN_HEIGHT = 380

BLOCKED_HOSTS = [
    "alamy", "istockphoto", "shutter", "dreamstime", "123rf",
    "depositphotos", "stock.adobe", "freepik", "pinterest",
    "vecteezy", "bigstock", "ebay", "etsy", "redbubble", "teepublic",
    "society6", "displate", "ytimg", "pngtree", "cgtrader", "footyheadlines",
    "twimg", "huggingface", "hf.co", "pond5", "mixkit", "motionarray", "pinimg",
    "getty", "gettyimages", "canstock", "envato", "dailymail", "thesun",
    "pxhere", "wallpaper", "shopee", "tiki", "lazada", "shopify", "susercontent", "hstatic"
]

GETTY_TEMPLATE_PATH = "/Users/phamminhtrieu/.gemini/antigravity/brain/7e88202f-ec65-4572-a9c3-e602e2904d70/.user_uploaded/media_1794277963250_04e9947d.png"

NEWS_DATA = [
    {
        "id": 1,
        "art_id": "art_01",
        "slug": "Short_Man_Utd_Hop_Ban_Sa_Thai_Carrick_Merson",
        "file_name": "Short_Man_Utd_Hop_Ban_Sa_Thai_Carrick_Merson.mp4",
        "thumb_name": "Short_Man_Utd_Hop_Ban_Sa_Thai_Carrick_Merson_thumbnail.jpg",
        "mota_name": "Short_Man_Utd_Hop_Ban_Sa_Thai_Carrick_Merson_mota.txt",
        "voice": "Minh Quân Pro",
        "voice_gender": "male",
        "speed": 1.12,
        "pitch": 0.93,
        "temp": 0.6,
        "group": "Nhóm: Khủng hoảng Ngoại hạng Anh",
        "title": "Man Utd họp bàn sa thải Carrick và lời cảnh tỉnh của Paul Merson",
        "summary": (
            "Cuộc khủng hoảng thành tích tại Old Trafford vừa bước vào giai đoạn nóng bỏng nhất, "
            "khi đồng sở hữu Jim Ratcliffe triệu tập Giám đốc bóng đá Jason Wilcox và CEO Omar Berrada tới Monaco "
            "để họp bàn tương lai của huấn luyện viên Michael Carrick! "
            "Sau trận hòa điên rồ 4-4 trước Aston Villa, MU hiện chìm sâu ở vị trí thứ 18 Ngoại hạng Anh với vỏn vẹn 1 chiến thắng sau 10 vòng đấu, "
            "chỉ hơn đội bét bảng đúng 1 điểm mong manh. "
            "Dù Michael Carrick kiên quyết không từ chức, ban lãnh đạo Ineos vẫn nghiêng về phương án bổ nhiệm thuyền trưởng mới ngay trong đợt tập trung đội tuyển tháng 11, "
            "để kịp ra mắt ở đại chiến gặp Liverpool ngày 22 tháng 11. "
            "Nếu trát sa thải được thông qua, Carrick sẽ trở thành huấn luyện viên thứ hai của Quỷ đỏ mất việc chỉ trong năm 2026 sau Ruben Amorim, "
            "và là đời huấn luyện viên thứ tư thời tập đoàn Ineos. "
            "Tuy nhiên, cựu danh thủ Paul Merson trên Sky Sports đã lên tiếng bảo vệ Carrick khi khẳng định ban lãnh đạo MU đang xây một ngôi nhà trên vũng nước, "
            "khi đổ tiền mua tiền đạo và tiền vệ mà bỏ quên hàng phòng ngự. "
            "Với việc để thủng lưới tới 15 bàn chỉ trong 5 trận gần nhất, Merson nhấn mạnh dù có mời Arsene Wenger, Sir Alex Ferguson hay Pep Guardiola về dẫn dắt, "
            "Man Utd cũng không thể thành công nếu nền móng hàng thủ chưa được giải quyết!"
        ),
        "digest_line": "Man Utd họp bàn sa thải Carrick tại Monaco, trong khi Merson cảnh tỉnh MU đang xây nhà trên vũng nước.",
        "digest_title": "Man Utd họp bàn sa thải Carrick và lời cảnh tỉnh của Paul Merson",
        "source": "VnExpress / Sky Sports",
        "news_source": "VnExpress / Sky Sports",
        "thumb_kicker": "NGOẠI HẠNG ANH · BIẾN CĂNG OLD TRAFFORD",
        "thumb_hero": "MU HỌP SA THẢI CARRICK!",
        "thumb_hero_size": "100",
        "thumb_sub": "BAN LÃNH ĐẠO GIỮ GHẾ · MERSON CẢNH TỈNH NGUY CƠ SẬP NỀN MÓNG",
        "thumb_bg_img": "Tin_01_1.jpg",
        "seo_title": "Man Utd họp bàn sa thải Carrick và lời cảnh tỉnh của Paul Merson #Shorts",
        "seo_desc": (
            "Cuộc khủng hoảng thành tích tại Old Trafford bùng nổ khi tỷ phú Jim Ratcliffe triệu tập Giám đốc bóng đá Jason Wilcox "
            "và CEO Omar Berrada tới Monaco để quyết định tương lai của HLV Michael Carrick!\n\n"
            "Chìm sâu ở vị trí thứ 18 Ngoại hạng Anh sau trận hòa 4-4 trước Aston Villa, Carrick đứng trước nguy cơ trở thành HLV thứ 2 bị MU sa thải trong năm 2026 "
            "ngay trước trận đại chiến gặp Liverpool ngày 22/11.\n\n"
            "Tuy nhiên, cựu tiền vệ Paul Merson trên Sky Sports đã đanh thép lên tiếng bảo vệ Carrick: MU đang 'xây nhà trên vũng nước' khi mua tiền đạo, tiền vệ "
            "mà bỏ quên hàng thủ thủng lưới 15 bàn trong 5 trận, và dù có mời Pep Guardiola hay Sir Alex thì cũng khó cứu vãn nếu nền móng phòng ngự rách nát!"
        ),
        "seo_tags": "#Shorts #DiemDoc #ManUtd #MU #MichaelCarrick #Carrick #PaulMerson #JimRatcliffe #OldTrafford #PremierLeague #TinBongDa"
    },
    {
        "id": 2,
        "art_id": "art_02",
        "slug": "Short_Stephanie_Case_Chay_160_km_Nam_Cuc",
        "file_name": "Short_Stephanie_Case_Chay_160_km_Nam_Cuc.mp4",
        "thumb_name": "Short_Stephanie_Case_Chay_160_km_Nam_Cuc_thumbnail.jpg",
        "mota_name": "Short_Stephanie_Case_Chay_160_km_Nam_Cuc_mota.txt",
        "voice": "Ngọc Huyền",
        "voice_gender": "female",
        "speed": 1.12,
        "pitch": 1.10,
        "temp": 0.5,
        "group": "Nhóm: Kỳ tích thể thao thế giới",
        "title": "Người phụ nữ đầu tiên chạy 160 km ở Nam Cực phá kỷ lục lịch sử",
        "summary": (
            "Nữ vận động viên siêu marathon Stephanie Case vừa xác lập một kỳ tích vô tiền khoáng hậu, "
            "khi trở thành người phụ nữ đầu tiên trong lịch sử chinh phục cự ly 100 dặm, tương đương gần 161 km, tại vùng đất khắc nghiệt nhất hành tinh Nam Cực! "
            "Tại giải đấu khắc nghiệt Antarctic Ice Ultra, chân chạy 44 tuổi người Canada đã hoàn thành quãng đường với thời gian 24 giờ 31 phút 44 giây, "
            "xô đổ kỷ lục của nam vận động viên Paul Giblin tới hơn 5 giờ đồng hồ! "
            "Để hoàn tất cự ly, cô phải chạy liên tục 38 vòng quanh trại căn cứ ở ốc đảo Schirmacher giữa nền nhiệt âm 35 độ C, "
            "gió bão gầm rú và tuyết bốc mù mịt bên những bờ vực thẳm. "
            "Ngay sau 8 vòng đầu tiên, chiếc mũ trùm mặt đóng băng cứng ngắc khiến cô không thể thở qua lớp vải, "
            "buộc cô phải thay đổi kế hoạch và vào lều tiếp sức sưởi ấm sớm hơn dự kiến. "
            "Không chỉ là một vận động viên cự phách, Stephanie Case còn là một luật sư nhân quyền và nhà sáng lập tổ chức Free to Run, "
            "kiên trì dùng từng bước chạy để trao quyền cho phụ nữ tại các khu vực xung đột. "
            "Kỳ tích 161 km tại Nam Cực không chỉ là chiến thắng vĩ đại của ý chí trước thiên nhiên dữ dội, "
            "mà còn khẳng định sức mạnh phi thường và tiềm năng không giới hạn của người phụ nữ trên những đỉnh cao thể thao thế giới!"
        ),
        "digest_line": "Stephanie Case trở thành người phụ nữ đầu tiên chạy 160 km ở Nam Cực, phá kỷ lục nam hơn 5 giờ.",
        "digest_title": "Người phụ nữ đầu tiên chạy 160 km ở Nam Cực phá kỷ lục lịch sử",
        "source": "VnExpress / The North Face",
        "news_source": "VnExpress / The North Face",
        "thumb_kicker": "KỶ LỤC THẾ GIỚI · Ý CHÍ PHI THƯỜNG",
        "thumb_hero": "CHẠY 160 KM Ở NAM CỰC!",
        "thumb_hero_size": "105",
        "thumb_sub": "KỶ LỤC LỊCH SỬ ÂM 35 ĐỘ C CỦA NỮ VĐV STEPHANIE CASE",
        "thumb_bg_img": "Tin_02_1.jpg",
        "seo_title": "Người phụ nữ đầu tiên chạy 160 km ở Nam Cực phá kỷ lục lịch sử #Shorts",
        "seo_desc": (
            "Nữ luật sư nhân quyền kiêm VĐV siêu marathon Canada 44 tuổi Stephanie Case đã làm nên lịch sử tại Antarctic Ice Ultra 2026: "
            "trở thành người phụ nữ đầu tiên trên thế giới hoàn thành cự ly 100 dặm (160,93 km) giữa cái lạnh âm 35 độ C và bão tuyết Nam Cực!\n\n"
            "Thành tích phi thường 24 giờ 31 phút 44 giây xô đổ kỷ lục của nam VĐV Paul Giblin tới hơn 5 giờ đồng hồ, "
            "vượt qua 38 vòng chạy nghẹt thở quanh ốc đảo Schirmacher nơi mặt nạ đóng băng không thở nổi.\n\n"
            "Nhà sáng lập tổ chức Free to Run tiếp tục chứng minh sức mạnh phi thường và ý chí bất khuất của phụ nữ trên những đỉnh cao thể thao khắc nghiệt nhất địa cầu!"
        ),
        "seo_tags": "#Shorts #DiemDoc #StephanieCase #NamCuc #Antarctica #UltraMarathon #IceUltra #FreeToRun #TheNorthFace #KyLucTheGioi"
    },
    {
        "id": 3,
        "art_id": "art_03",
        "slug": "Short_Trinh_Thu_Vinh_Doat_Ve_Olympic_2028",
        "file_name": "Short_Trinh_Thu_Vinh_Doat_Ve_Olympic_2028.mp4",
        "thumb_name": "Short_Trinh_Thu_Vinh_Doat_Ve_Olympic_2028_thumbnail.jpg",
        "mota_name": "Short_Trinh_Thu_Vinh_Doat_Ve_Olympic_2028_mota.txt",
        "voice": "Ngọc Huyền",
        "voice_gender": "female",
        "speed": 1.12,
        "pitch": 1.10,
        "temp": 0.5,
        "group": "Nhóm: Bắn súng & Thể thao Việt Nam",
        "title": "Trịnh Thu Vinh đoạt vé Olympic 2028 đầu tiên cho thể thao Việt Nam",
        "summary": (
            "Thể thao Việt Nam vừa đón nhận tin vui chấn động từ Qatar, khi nữ xạ thủ Trịnh Thu Vinh "
            "xuất sắc trở thành vận động viên Việt Nam đầu tiên chính thức giành vé tham dự Thế vận hội Olympic Los Angeles 2028! "
            "Tại giải vô địch bắn súng thế giới 2026, nữ tuyển thủ sinh năm 2000 thuộc đoàn Công an Nhân dân "
            "đã thi đấu thăng hoa để đoạt tấm huy chương bạc lịch sử ở nội dung 25m súng ngắn thể thao nữ. "
            "Vượt qua vòng loại căng thẳng với 585 điểm, Thu Vinh hiên ngang bước vào chung kết "
            "để đối đầu trực diện với những tên tuổi lừng lẫy nhất hành tinh như kỷ lục gia thế giới Esha Singh và nhà vô địch Olympic Yang Ji-in. "
            "Trong bài thi bắn nhanh áp lực ngút ngàn, Thu Vinh thi đấu xuất thần khi liên tục dẫn đầu suốt 9 loạt bắn với 40 điểm, "
            "trước khi chịu thua sít sao 43-44 đầy tiếc nuối trước đối thủ Hàn Quốc ở loạt đạn cuối cùng. "
            "Tấm huy chương bạc cá nhân cùng huy chương đồng đồng đội nữ đã đưa bắn súng Việt Nam vươn lên vị trí thứ 17 thế giới, "
            "khép lại nỗi buồn thất bại tại đấu trường Asiad 2026. "
            "Sau vị trí thứ tư tại Olympic Paris 2024, tấm vé sớm đến Los Angeles 2028 là minh chứng đanh thép cho đẳng cấp thế giới của Trịnh Thu Vinh, "
            "mở ra niềm hy vọng vàng rực sáng cho thể thao nước nhà!"
        ),
        "digest_line": "Trịnh Thu Vinh đoạt HC bạc thế giới 25m súng ngắn, trở thành VĐV Việt Nam đầu tiên giành vé dự Olympic 2028.",
        "digest_title": "Trịnh Thu Vinh đoạt vé Olympic 2028 đầu tiên cho thể thao Việt Nam",
        "source": "VnExpress / ISSF",
        "news_source": "VnExpress / ISSF",
        "thumb_kicker": "BẮN SÚNG THẾ GIỚI · VÉ VÀNG OLYMPIC",
        "thumb_hero": "VÉ ĐẦU TIÊN DỰ OLYMPIC!",
        "thumb_hero_size": "95",
        "thumb_sub": "TRỊNH THU VINH ĐOẠT HC BẠC THẾ GIỚI 2026 ĐẾN LOS ANGELES",
        "thumb_bg_img": "Tin_03_1.jpg",
        "seo_title": "Trịnh Thu Vinh đoạt vé Olympic 2028 đầu tiên cho thể thao Việt Nam #Shorts",
        "seo_desc": (
            "Nữ xạ thủ Trịnh Thu Vinh làm rạng danh thể thao nước nhà khi xuất sắc đoạt tấm huy chương bạc 25m súng ngắn thể thao nữ "
            "tại Giải bắn súng vô địch thế giới 2026 diễn ra ở Doha (Qatar)!\n\n"
            "Với thành tích này, Trịnh Thu Vinh chính thức trở thành vận động viên Việt Nam đầu tiên giành vé chính thức tham dự "
            "Thế vận hội Olympic Los Angeles 2028 (LA28)!\n\n"
            "Thu Vinh liên tục dẫn đầu chung kết và chỉ chịu thua sít sao 43-44 trước nhà vô địch Olympic Yang Ji-in ở loạt đạn cuối cùng, "
            "xác lập chiến tích cao nhất lịch sử bắn súng Việt Nam tại giải vô địch thế giới!"
        ),
        "seo_tags": "#Shorts #DiemDoc #TrinhThuVinh #BanSung #Olympic2028 #LA28 #ISSF #TheThaoVietNam #WorldChampionship #OlympicParis"
    },
    {
        "id": 4,
        "art_id": "art_04",
        "slug": "Short_U23_Viet_Nam_Dai_Thang_Thai_Lan_3_0",
        "file_name": "Short_U23_Viet_Nam_Dai_Thang_Thai_Lan_3_0.mp4",
        "thumb_name": "Short_U23_Viet_Nam_Dai_Thang_Thai_Lan_3_0_thumbnail.jpg",
        "mota_name": "Short_U23_Viet_Nam_Dai_Thang_Thai_Lan_3_0_mota.txt",
        "voice": "Minh Quân Pro",
        "voice_gender": "male",
        "speed": 1.12,
        "pitch": 0.93,
        "temp": 0.6,
        "group": "Nhóm: Bóng đá Việt Nam",
        "title": "U23 Việt Nam đại thắng U23 Thái Lan với tỷ số 3-0 ở cúp quốc tế Gia Lai",
        "summary": (
            "Đội tuyển U23 Việt Nam vừa có màn ra quân tưng bừng tại giải giao hữu quốc tế Gia Lai VTV Cup 2026, "
            "khi xuất sắc đánh bại đại kình địch U23 Thái Lan với tỷ số đậm đà 3-0 ngay trên chảo lửa Pleiku! "
            "Dù chỉ kiểm soát bóng 37%, các học trò của huấn luyện viên Đinh Hồng Vinh đã trình diễn lối chơi phòng ngự phản công sắc bén đến nghẹt thở, "
            "tung ra tới 20 pha dứt điểm với 13 lần trúng đích so với vỏn vẹn 2 lần của đối thủ. "
            "Ngôi sao sáng nhất trận đấu là tiền đạo sinh năm 2005 Nguyễn Minh Tâm, "
            "khi chân sút trẻ của câu lạc bộ HAGL rực sáng với cú đúp đánh đầu đẳng cấp ở phút 17 và phút 45 để xé toang mành lưới đội khách. "
            "Bước sang hiệp hai, U23 Thái Lan dồn đội hình tấn công nhằm tìm kiếm bàn gỡ, "
            "nhưng sự xuất sắc của thủ thành Cao Văn Bình cùng hàng thủ vững chãi đã hóa giải mọi đợt sóng gió. "
            "Đến phút 85, cầu thủ Việt kiều Williams Minh Hoàng ấn định chiến thắng ngọt ngào 3-0 trên chấm phạt đền, "
            "đánh dấu bàn thắng lịch sử đầu tiên của anh trong màu áo U23 Việt Nam. "
            "Khởi đầu như mơ với ngôi đầu bảng và 3 điểm trọn vẹn, U23 Việt Nam tràn trề tự tin trước hai cuộc đối đầu nảy lửa gặp Singapore ngày 12 tháng 11 "
            "và Qatar ngày 14 tháng 11 để hướng tới chức vô địch 100000 USD!"
        ),
        "digest_line": "U23 Việt Nam thắng đậm U23 Thái Lan với tỷ số 3-0 nhờ cú đúp của Minh Tâm và bàn thắng của Williams Minh Hoàng.",
        "digest_title": "U23 Việt Nam đại thắng U23 Thái Lan với tỷ số 3-0 ở cúp quốc tế Gia Lai",
        "source": "VnExpress / VFF",
        "news_source": "VnExpress / VFF",
        "thumb_kicker": "GIA LAI VTV CUP 2026 · ĐẠI CHIẾN PLEIKU",
        "thumb_hero": "VIỆT NAM ĐẠI THẮNG THÁI LAN 3-0!",
        "thumb_hero_size": "88",
        "thumb_sub": "MINH TÂM LẬP CÚ ĐÚP ĐẦU · WILLIAMS MINH HOÀNG MỞ TÀI KHOẢN BÀN THẮNG",
        "thumb_bg_img": "Tin_04_1.jpg",
        "seo_title": "U23 Việt Nam đại thắng U23 Thái Lan với tỷ số 3-0 ở cúp quốc tế Gia Lai #Shorts",
        "seo_desc": (
            "U23 Việt Nam có ngày ra quân rực rỡ tại giải giao hữu quốc tế Gia Lai VTV Cup 2026 khi đánh bại U23 Thái Lan với tỷ số đậm đà 3-0 trên sân Pleiku!\n\n"
            "Tiền đạo trẻ HAGL Nguyễn Minh Tâm tỏa sáng rực rỡ với cú đúp đánh đầu đẳng cấp ở phút 17 và 45, trước khi tân binh Việt kiều Williams Minh Hoàng ấn định chiến thắng 3-0 trên chấm phạt đền phút 85.\n\n"
            "Thầy trò HLV Đinh Hồng Vinh vươn lên dẫn đầu bảng xếp hạng và tràn trề cơ hội chinh phục chức vô địch trước thềm các lượt trận gặp Singapore và Qatar!"
        ),
        "seo_tags": "#Shorts #DiemDoc #U23VietNam #U23ThaiLan #MinhTam #WilliamsMinhHoang #DinhHongVinh #HAGL #GiaLaiVTVCup #BongDaVietNam"
    }
]

IMAGE_QUERIES_TIN_1 = [
    ("Tin_01_1.jpg", "https://i1-thethao.vnecdn.net/2026/11/10/wilcox-berrada-1794329680-2898-1794329785.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=M5EdR_r5yjRAwPhV4jKB8Q", "AFP", "Omar Berrada và Jason Wilcox trên khán đài Old Trafford"),
    ("Tin_01_2.jpg", "Sir Jim Ratcliffe Old Trafford high resolution", "INEOS / MAN UTD", "Sir Jim Ratcliffe họp kín định đoạt tương lai ban huấn luyện"),
    ("Tin_01_3.jpg", "Michael Carrick Manchester United Aston Villa 2026", "ACTION IMAGES / REUTERS", "Michael Carrick trầm ngâm trên đường pitch Old Trafford"),
    ("Tin_01_4.jpg", "https://i1-thethao.vnecdn.net/2026/11/10/Cunha-JPG-1684-1794329785.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=Sh2yH_eBQiPRdZ2n9O90Bg", "REUTERS", "Michael Carrick và Matheus Cunha cãi vã sau trận đấu"),
    ("Tin_01_5.jpg", "https://i1-thethao.vnecdn.net/2026/11/10/Man-Utd-3676-1794329786.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=7H1pZkBZGCF6DxS2bmAZzQ", "VNEXPRESS", "Đồ họa tỷ lệ thắng các HLV Man Utd thời hậu Ferguson"),
    ("Tin_01_6.jpg", "https://i1-thethao.vnecdn.net/2026/11/11/Tielemans-1745-1794354024.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=BFAF3FMrh2Z-D9-J6sjRJg", "AP PHOTO", "Youri Tielemans ăn mừng bàn gỡ hòa trong trận hòa Villa 4-4"),
    ("Tin_01_7.jpg", "https://i1-thethao.vnecdn.net/2026/11/11/image-1794353608-7676-1794354024.jpg?w=1020&h=0&q=100&dpr=1&fit=crop&s=V5AAdUU7RgW-0JSfUn8Crw", "SKY SPORTS", "Paul Merson bình luận trên Sky Sports về khủng hoảng Man Utd"),
    ("Tin_01_8.jpg", "Paul Merson Sky Sports studio football", "SKY SPORTS", "Paul Merson nhấn mạnh MU không thể xây nhà trên vũng nước"),
    ("Tin_01_9.jpg", "Manchester United defenders conceded Aston Villa 2026", "ACTION IMAGES / REUTERS", "Hàng thủ Man Utd rách nát thủng lưới 15 bàn sau 5 trận"),
    ("Tin_01_10.jpg", "Bruno Fernandes Manchester United disappointed 2026", "REUTERS", "Bruno Fernandes và các cầu thủ Quỷ đỏ bất lực trên sân"),
    ("Tin_01_11.jpg", "Old Trafford stadium night match Manchester United", "MAN UTD / WIKIMEDIA", "Sân vận động Old Trafford chìm trong bóng mây khủng hoảng"),
    ("Tin_01_12.jpg", "Michael Carrick press conference Carrington Manchester United", "REUTERS", "Michael Carrick khẳng định kiên quyết không từ chức"),
]

IMAGE_QUERIES_TIN_2 = [
    ("Tin_02_1.jpg", "https://i1-thethao.vnecdn.net/2026/11/10/A-nh-ma-n-hi-nh-2026-11-10-lu-6183-3404-1794298028.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=fnAsZt26JeND3Yz6KlnjZg", "THE NORTH FACE", "Stephanie Case sải bước trên băng tuyết Nam Cực"),
    ("Tin_02_2.jpg", "https://iv1.vnecdn.net/thethao/images/web/2026/11/10/nguoi-phu-nu-dau-tien-chay-het-160-km-o-nam-cuc-1794297943.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=mVKUlLjXA-6XOA1AG1s6Jw", "THE NORTH FACE", "Khoảnh khắc Stephanie Case làm nên lịch sử 100 dặm"),
    ("Tin_02_3.jpg", "Antarctic Ice Ultra landscape snow blizzard 2026", "ANTARCTIC ICE ULTRA", "Khung cảnh băng giá âm 35 độ C mênh mông tại Nam Cực"),
    ("Tin_02_4.jpg", "Schirmacher Oasis Antarctica base camp research station", "WIKIMEDIA COMMONS", "Ốc đảo Schirmacher nơi diễn ra đường chạy 38 vòng"),
    ("Tin_02_5.jpg", "Stephanie Case frozen face mask ice running ultra", "THE NORTH FACE", "Chiếc mũ trùm mặt đóng băng cứng khiến VĐV khó thở"),
    ("Tin_02_6.jpg", "Stephanie Case Ultra-Trail Snowdonia running mountain", "RUNNING MAGAZINE", "Chân chạy siêu marathon 44 tuổi kiên cường bám trụ"),
    ("Tin_02_7.jpg", "Stephanie Case finish line medal Antarctic Ice Ultra", "THE NORTH FACE", "Stephanie Case hoàn thành quãng đường 24 giờ 31 phút 44 giây"),
    ("Tin_02_8.jpg", "Stephanie Case Free to Run Afghanistan women empowerment", "FREE TO RUN", "Stephanie Case và tổ chức Free to Run trao quyền cho phụ nữ"),
    ("Tin_02_9.jpg", "Antarctic Ice Ultra running track snow blizzard runner", "THE NORTH FACE", "Gió bão gầm rú và tuyết bốc mù mịt trên đường chạy"),
    ("Tin_02_10.jpg", "Stephanie Case Alps trail runner training endurance", "IRUNFAR", "Kinh nghiệm chinh phục những giải ultra khắc nghiệt nhất"),
    ("Tin_02_11.jpg", "Stephanie Case Canadian ultra runner smiling trail", "GLORIOUS SPORT", "Nụ cười rạng rỡ của nữ luật sư nhân quyền quả cảm"),
    ("Tin_02_12.jpg", "Stephanie Case celebrating victory Antarctica flag", "THE NORTH FACE / FREE TO RUN", "Kỳ tích 161 km khẳng định sức mạnh phi thường của phụ nữ"),
]

IMAGE_QUERIES_TIN_3 = [
    ("Tin_03_1.jpg", "https://i1-thethao.vnecdn.net/2026/11/10/screenshot-at-1794311281-6802-1794311292.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=hJ-OV-Ri4wynoZsFnVnKWg", "VNEXPRESS / ISSF", "Trịnh Thu Vinh và Yang Ji-in loạt bắn phân định HC vàng"),
    ("Tin_03_2.jpg", "https://i1-thethao.vnecdn.net/2026/11/10/screenshot-at-1794314164-2930-1794314206.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=j_OykHgCB_7TAiaNheyAHg", "VNEXPRESS / ISSF", "Thu Vinh nhận HC bạc, Yang Ji-in HC vàng, Zhang Yueyue HC đồng"),
    ("Tin_03_3.jpg", "https://i1-thethao.vnecdn.net/2026/11/10/Chung-ke-t-25m-su-ng-nga-n-nu-5917-1794314206.png?w=1020&h=0&q=100&dpr=1&fit=crop&s=J5C7SBy_VGRV43_Gn17Qxg", "HIẾU LƯƠNG / VNEXPRESS", "Đồ họa kết quả chung kết 25m súng ngắn thể thao nữ"),
    ("Tin_03_4.jpg", "Trịnh Thu Vinh Olympic Paris 2024 súng ngắn 25m", "REUTERS", "Thu Vinh tập trung cao độ trong từng loạt bắn súng ngắn"),
    ("Tin_03_5.jpg", "Trịnh Thu Vinh ăn mừng bắn súng Việt Nam huy chương", "BÁO VĂN HÓA", "Niềm hạnh phúc vỡ òa của Thu Vinh cùng ban huấn luyện"),
    ("Tin_03_6.jpg", "Yang Ji-in South Korea shooting world championship 2026", "YONHAP / ISSF", "Yang Ji-in ăn mừng kỷ lục thế giới mới 44 điểm nghẹt thở"),
    ("Tin_03_7.jpg", "Bắn súng đồng đội nữ Việt Nam huy chương đồng thế giới 2026", "BÁO LAO ĐỘNG", "Thu Vinh cùng Thùy Trang và Thùy Dung giành HC đồng đồng đội"),
    ("Tin_03_8.jpg", "Trịnh Thu Vinh súng ngắn hơi 10m chung kết Olympic Paris", "AP PHOTO", "Bản lĩnh thi đấu đỉnh cao từng đứng thứ tư tại Paris 2024"),
    ("Tin_03_9.jpg", "Trịnh Thu Vinh SEA Games 4 huy chương vàng bắn súng", "VNEXPRESS / VASC", "Nữ xạ thủ Công an Nhân dân thống trị đấu trường khu vực"),
    ("Tin_03_10.jpg", "Lusail Shooting Range Doha Qatar World Championship 2026", "ISSF / LUSAIL", "Toàn cảnh trường bắn Lusail hiện đại bậc nhất tại Doha Qatar"),
    ("Tin_03_11.jpg", "Trịnh Thu Vinh chân dung nữ xạ thủ Việt Nam rạng rỡ", "BÁO THỂ THAO VIỆT NAM", "Chân dung Trịnh Thu Vinh - niềm tự hào thể thao Việt Nam"),
    ("Tin_03_12.jpg", "Olympic Los Angeles 2028 official logo LA28", "LA28 / IOC", "Biểu trưng Thế vận hội Olympic Los Angeles 2028"),
]

IMAGE_QUERIES_TIN_4 = [
    ("Tin_04_1.jpg", "https://i1-thethao.vnecdn.net/2026/11/10/1794315030531-5273798066751224-2919-8553-1794323175.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=Ss61FL_2feCyiTeO8tfUNQ", "VNEXPRESS / ĐỨC CƯỜNG", "Minh Tâm số 18 ăn mừng cú đúp mở tỷ số vào lưới U23 Thái Lan"),
    ("Tin_04_2.jpg", "https://i1-thethao.vnecdn.net/2026/11/10/1794318819507-5273798066751224-7733-3424-1794323175.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=m4Rxoh-gH5UdNqEQTXcHhw", "VNEXPRESS / ĐỨC CƯỜNG", "Williams Minh Hoàng sút phạt đền hiểm hóc ấn định tỷ số 3-0"),
    ("Tin_04_3.jpg", "https://iv1.vnecdn.net/thethao/images/web/2026/11/10/highlights-viet-nam-3-0-thai-lan-1794323151.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=l5wolNZqQAgmynb1RVq4uA", "VNEXPRESS", "Highlights trận thắng 3-0 của U23 Việt Nam trước Thái Lan"),
    ("Tin_04_4.jpg", "https://vff.org.vn/wp-content/uploads/2026/11/1K732O1RP_3CM1NN.jpeg", "VFF / KHÁNH VY", "Pha đi bóng dũng mãnh của U23 Việt Nam trước hàng thủ Thái Lan"),
    ("Tin_04_5.jpg", "https://vff.org.vn/wp-content/uploads/2026/11/1K732O1RQ_3CM1NN.jpeg", "VFF / KHÁNH VY", "U23 Việt Nam kiểm soát bóng 37% nhưng tung ra tới 20 pha dứt điểm"),
    ("Tin_04_6.jpg", "https://vff.org.vn/wp-content/uploads/2026/11/1K732O1RR_3CM1NN.jpeg", "VFF / KHÁNH VY", "Khán giả phố núi Gia Lai cuồng nhiệt cổ vũ U23 Việt Nam"),
    ("Tin_04_7.jpg", "https://vff.org.vn/wp-content/uploads/2026/11/1K732O1RT_3CM1NN.jpeg", "VFF / KHÁNH VY", "Toàn cảnh cầu trường Pleiku rực lửa trong đêm đại thắng"),
    ("Tin_04_8.jpg", "https://cdnphoto.dantri.com.vn/S7BeMlxaWELjbxfDQbYjv9O9rEs=/thumb_w/1020/2026/11/10/17943144748718636952574752207119g16857354889090214907c07486cc8477cac689c91d9d49f28d-1794329585617.jpg", "DÂN TRÍ / TRẦN HẢO", "Minh Tâm bật cao đánh đầu hiểm hóc đánh bại thủ môn Sirassawut"),
    ("Tin_04_9.jpg", "https://cdnphoto.dantri.com.vn/68tFE1fLpwLiGthx0-UDxDvii94=/thumb_w/1020/2026/11/10/17943180176998636952574752207119g168573548890902149b69b6c4f389a6ee20e9e8144ff6135b2-edited-1794329651065.jpg", "DÂN TRÍ / TRẦN HẢO", "Williams Minh Hoàng ăn mừng bàn thắng đầu tiên trong màu áo U23"),
    ("Tin_04_10.jpg", "https://cdnphoto.dantri.com.vn/DIwmPbAXoDreK0GCfdwRDBsT9BA=/thumb_w/1020/2026/11/10/u23vn-thai5tranhao10-11-26-1794325798961.jpg", "DÂN TRÍ / TRẦN HẢO", "Hàng phòng ngự Việt Nam bọc lót chắc chắn bảo toàn mành lưới"),
    ("Tin_04_11.jpg", "https://cdnphoto.dantri.com.vn/iG_0G8S4Cra54XaNvkJ4HJLdQ1g=/thumb_w/1020/2026/11/10/hlvdinhhongvinh1tranhao10-11-26-1794325796351.jpg", "DÂN TRÍ / TRẦN HẢO", "HLV Đinh Hồng Vinh hài lòng với tinh thần chiến đấu của toàn đội"),
    ("Tin_04_12.jpg", "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/10/17943138014725536399183250272835g44555886359614103715dab3b204924d98f54f5eb65813af707-17943138445501669294931-56-0-856-1280-crop-17943139744892139722363.jpg", "NGUYÊN KHÔI / TUỔI TRẺ", "Cầu thủ U23 Thái Lan bất lực trước sức ép dồn dập của chủ nhà"),
    ("Tin_04_13.jpg", "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/10/khoi7519-17943211168901643781125.jpg", "NGUYÊN KHÔI / TUỔI TRẺ", "Thủ môn Cao Văn Bình bay người xuất thần cản phá cú sút hiểm hóc"),
    ("Tin_04_14.jpg", "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/10/khoi7529-17943211168971874424477.jpg", "NGUYÊN KHÔI / TUỔI TRẺ", "U23 Việt Nam tri ân người hâm mộ cuồng nhiệt trên sân Pleiku"),
    ("Tin_04_15.jpg", "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/10/u23-thai-lan-1794324444781203936121.jpg", "NGUYÊN KHÔI / TUỔI TRẺ", "Nỗi thất vọng não nề của các cầu thủ U23 Thái Lan"),
    ("Tin_04_16.jpg", "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/10/17943188993685536399183250272835g44555886359614103712f9fd60a86d158ada0f36fe53484eeb2-1794320231164275107747-115-121-797-1212-crop-1794320237409134695154.jpg", "TUỔI TRẺ / VTV", "Bảng xếp hạng giải Gia Lai VTV Cup 2026 với ngôi đầu cho Việt Nam"),
    ("Tin_04_17.jpg", "https://cdn.bongdaplus.vn/Assets/Media/2026/11/10/38/minh-tam-11.jpg", "ĐỨC CƯỜNG / BÓNG ĐÁ PLUS", "Minh Tâm tỏa sáng rực rỡ với cú đúp đánh đầu đẳng cấp"),
    ("Tin_04_18.jpg", "https://cdn.bongdaplus.vn/Assets/Media/2026/11/10/38/minh-tam-ghi-ban.jpg", "ĐỨC CƯỜNG / BÓNG ĐÁ PLUS", "Khoảnh khắc bóng bay vào lưới Thái Lan sau cú đánh đầu phút 45"),
    ("Tin_04_19.jpg", "https://cdn.bongdaplus.vn/Assets/Media/2026/11/10/38/minh-tam-480-1.jpg", "ĐỨC CƯỜNG / BÓNG ĐÁ PLUS", "Tài năng trẻ sinh năm 2005 thuộc lò đào tạo HAGL"),
    ("Tin_04_20.jpg", "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/10/williams-minh-hoang-tap-luyen-cung-u23-17941416248761859974255-130-382-1491-2560-crop-17943081292362077754469.jpg", "TUỔI TRẺ", "Williams Minh Hoàng bứt tốc dũng mãnh uy hiếp khung thành"),
    ("Tin_04_21.jpg", "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/9/hlv-dinh-hong-vinh-trai-tai-cuoc-hop-bao-u23-gia-lai-vtv-cup-2026-edit-1794212246218725792753-97-78-1648-2560-crop-17942123436281851058636.jpg", "TUỔI TRẺ", "HLV Đinh Hồng Vinh chia sẻ chiến thuật cùng ban huấn luyện"),
    ("Tin_04_22.jpg", "https://cdn2.tuoitre.vn/thumb_w/730/471584752817336320/2026/11/10/khoi7054-1794308358701324216292-66-0-1029-1540-crop-17943084131351266806192.jpg", "TUỔI TRẺ", "Không khí tranh tài nảy lửa tại cúp tứ hùng quốc tế Gia Lai"),
    ("Tin_04_23.jpg", "https://cdn.bongdaplus.vn/Assets/Media/2026/11/11/56/u23-vietnam-1.jpg", "BÓNG ĐÁ PLUS", "U23 Việt Nam hoàn toàn làm chủ cục diện trận đấu"),
    ("Tin_04_24.jpg", "https://cdn.bongdaplus.vn/Assets/Media/2026/11/11/56/u23-viet-nam-5.jpg", "ĐỨC CƯỜNG / BÓNG ĐÁ PLUS", "Williams Minh Hoàng chia vui cùng đồng đội sau quả phạt đền"),
]


def setup_directories():
    step(f"Khởi tạo cấu trúc thư mục outputs/Orther/{DAY_STR}...")
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(AUDIO_TITLE_DIR, exist_ok=True)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(QA_DIR, exist_ok=True)
    os.makedirs(SHORTS_WORK, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    ok("Đã sẵn sàng các thư mục sản xuất!")


def has_getty_watermark(pil_img: Image.Image) -> bool:
    """Kiểm tra ảnh có dính watermark Getty Images bằng template matching."""
    if not os.path.exists(GETTY_TEMPLATE_PATH):
        return False
    try:
        cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2GRAY)
        template = cv2.imread(GETTY_TEMPLATE_PATH, 0)
        if template is None:
            return False
        th, tw = template.shape[:2]
        for scale in [0.5, 0.75, 1.0, 1.25, 1.5]:
            tw_s, th_s = int(tw * scale), int(th * scale)
            if tw_s > cv_img.shape[1] or th_s > cv_img.shape[0]:
                continue
            tpl_s = cv2.resize(template, (tw_s, th_s))
            res = cv2.matchTemplate(cv_img, tpl_s, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            if max_val > 0.60:
                return True
        return False
    except Exception:
        return False


def download_image(url: str, min_w=MIN_WIDTH, min_h=MIN_HEIGHT, min_ratio=MIN_RATIO) -> Optional[Image.Image]:
    """Tải và thẩm định chất lượng hình ảnh, loại bỏ watermark stock."""
    lower_url = url.lower()
    for b in BLOCKED_HOSTS:
        if b in lower_url:
            return None
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code != 200 or len(resp.content) < 20_000:
            return None
        im = Image.open(io.BytesIO(resp.content))
        im = im.convert("RGB")
        w, h = im.size
        if w < min_w or h < min_h:
            return None
        ratio = w / float(h)
        if ratio < min_ratio:
            return None
        if has_getty_watermark(im):
            warn(f"Phát hiện watermark Getty trong ảnh: {url[:60]}")
            return None
        return im
    except Exception:
        return None


def fetch_images_for_tin(tin_id: int, image_queries: List[Tuple[str, str, str, str]], force: bool = False):
    banner(f"THU THẬP VÀ KIỂM DUYỆT 12 ẢNH HD CHO TIN #{tin_id:02d}", DAY_STR)
    ddgs = DDGS()
    for idx, (fname, query_or_url, credit, desc) in enumerate(image_queries, 1):
        target_path = os.path.join(IMG_DIR, fname)
        if not force and os.path.exists(target_path) and os.path.getsize(target_path) > 30_000:
            ok(f"  [{idx}/12] {fname} đã tồn tại — bỏ qua.")
            continue

        step(f"  [{idx}/12] Đang tải {fname} ({credit})...")
        found_img = None

        if query_or_url.startswith("http://") or query_or_url.startswith("https://"):
            try:
                r = requests.get(query_or_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
                if r.status_code == 200:
                    im = Image.open(io.BytesIO(r.content)).convert("RGB")
                    if not has_getty_watermark(im):
                        found_img = im
            except Exception as e:
                warn(f"Lỗi tải URL trực tiếp {query_or_url}: {e}")

        if not found_img:
            step(f"  -> Tìm kiếm DDGS: \"{query_or_url}\"")
            try:
                res = list(ddgs.images(query_or_url, region="wt-wt", safesearch="off", layout="Wide", max_results=12))
            except Exception:
                res = []

            for item in res:
                img_url = item.get("image")
                if not img_url:
                    continue
                im = download_image(img_url)
                if im:
                    found_img = im
                    break

        if not found_img:
            fallback_q = f"{desc} HD sports photography"
            step(f"  -> Thử fallback query: \"{fallback_q}\"")
            try:
                res_fb = list(ddgs.images(fallback_q, region="wt-wt", safesearch="off", layout="Wide", max_results=15))
                for item in res_fb:
                    im = download_image(item.get("image"))
                    if im:
                        found_img = im
                        break
            except Exception:
                pass

        if found_img:
            found_img.save(target_path, "JPEG", quality=92, optimize=True)
            ok(f"  -> Lưu thành công {fname} ({found_img.width}x{found_img.height})")
        else:
            first_img = os.path.join(IMG_DIR, f"Tin_{tin_id:02d}_1.jpg")
            if os.path.exists(first_img):
                warn(f"  -> Dùng ảnh dự phòng {os.path.basename(first_img)} cho {fname}.")
                shutil.copy2(first_img, target_path)
            else:
                die(f"Không thể thu thập ảnh cho {fname}!")


def update_metadata_jsons():
    banner("XUẤT CÁC FILE HỢP ĐỒNG DỮ LIỆU: THETHAO.JSON, IMAGE_CREDITS.JSON, IMAGE_PLAN.JSON", DAY_STR)

    # 1. image_credits.json
    credits_map = {}
    for fn, _, cr, _ in IMAGE_QUERIES_TIN_1:
        credits_map[fn] = cr
    for fn, _, cr, _ in IMAGE_QUERIES_TIN_2:
        credits_map[fn] = cr
    for fn, _, cr, _ in IMAGE_QUERIES_TIN_3:
        credits_map[fn] = cr
    for fn, _, cr, _ in IMAGE_QUERIES_TIN_4:
        credits_map[fn] = cr

    with open(os.path.join(DAY_DIR, "image_credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits_map, f, ensure_ascii=False, indent=2)
    ok(f"Đã lưu: {paths.rel_to_root(os.path.join(DAY_DIR, 'image_credits.json'))}")

    # 2. image_plan.json
    plan_records = []
    queries_all = [
        (1, IMAGE_QUERIES_TIN_1),
        (2, IMAGE_QUERIES_TIN_2),
        (3, IMAGE_QUERIES_TIN_3),
    ]
    for scene_id, q_list in queries_all:
        plan_records.append({
            "scene_id": scene_id,
            "type": "title",
            "index": 1,
            "sentence_idx": 0,
            "file_name": q_list[0][0],
            "credit": q_list[0][2],
            "description": q_list[0][3]
        })
        for sent_idx in range(1, 7):
            idx_a = (sent_idx - 1) * 2
            idx_b = idx_a + 1
            if idx_a < len(q_list):
                plan_records.append({
                    "scene_id": scene_id,
                    "type": "sentence",
                    "index": sent_idx,
                    "sentence_idx": sent_idx,
                    "file_name": q_list[idx_a][0],
                    "credit": q_list[idx_a][2],
                    "description": q_list[idx_a][3]
                })
            if idx_b < len(q_list):
                plan_records.append({
                    "scene_id": scene_id,
                    "type": "sentence",
                    "index": sent_idx,
                    "sentence_idx": sent_idx,
                    "file_name": q_list[idx_b][0],
                    "credit": q_list[idx_b][2],
                    "description": q_list[idx_b][3]
                })

    # Phân bổ 24 ảnh cho Tin 04 với nhịp cắt nhanh (3-4 ảnh/câu, chuyển mỗi 2.5s)
    q4_map = {fn: (cr, desc) for fn, _, cr, desc in IMAGE_QUERIES_TIN_4}
    # Title 3 ảnh
    for t_fn in ["Tin_04_1.jpg", "Tin_04_2.jpg", "Tin_04_3.jpg"]:
        cr, desc = q4_map[t_fn]
        plan_records.append({
            "scene_id": 4, "type": "title", "index": 1, "sentence_idx": 0,
            "file_name": t_fn, "credit": cr, "description": desc
        })
    # 6 câu với 3-4 ảnh mỗi câu (tổng 21 lượt chuyển cảnh)
    tin_4_sentence_images = [
        # Câu 1 (4 ảnh): đi bóng, toàn cảnh Pleiku, đánh đầu mở tỷ số, Thái Lan bất lực
        ["Tin_04_4.jpg", "Tin_04_7.jpg", "Tin_04_8.jpg", "Tin_04_12.jpg"],
        # Câu 2 (3 ảnh): tranh chấp bóng, hàng thủ bọc lót, Việt Nam kiểm soát
        ["Tin_04_5.jpg", "Tin_04_10.jpg", "Tin_04_23.jpg"],
        # Câu 3 (4 ảnh): Minh Tâm tỏa sáng, khoảnh khắc tung lưới phút 45, sao trẻ HAGL, ăn mừng đúp
        ["Tin_04_17.jpg", "Tin_04_18.jpg", "Tin_04_19.jpg", "Tin_04_1.jpg"],
        # Câu 4 (3 ảnh): Cao Văn Bình xuất thần, Thái Lan thất vọng, HLV Đinh Hồng Vinh chỉ đạo
        ["Tin_04_13.jpg", "Tin_04_15.jpg", "Tin_04_11.jpg"],
        # Câu 5 (4 ảnh): Williams Minh Hoàng bứt tốc, sút penalty, ăn mừng bàn thắng đầu tiên, chia vui
        ["Tin_04_20.jpg", "Tin_04_2.jpg", "Tin_04_9.jpg", "Tin_04_24.jpg"],
        # Câu 6 (3 ảnh): cổ động viên cuồng nhiệt, tri ân khán giả, bảng xếp hạng VTV Cup
        ["Tin_04_6.jpg", "Tin_04_14.jpg", "Tin_04_16.jpg"],
    ]
    for s_idx, f_list in enumerate(tin_4_sentence_images, 1):
        for f_name in f_list:
            cr, desc = q4_map.get(f_name, ("VFF / BÓNG ĐÁ PLUS", "Ảnh diễn biến trận đấu"))
            plan_records.append({
                "scene_id": 4, "type": "sentence", "index": s_idx, "sentence_idx": s_idx,
                "file_name": f_name, "credit": cr, "description": desc
            })

    with open(os.path.join(DAY_DIR, "image_plan.json"), "w", encoding="utf-8") as f:
        json.dump({"records": plan_records}, f, ensure_ascii=False, indent=2)
    ok(f"Đã lưu: {paths.rel_to_root(os.path.join(DAY_DIR, 'image_plan.json'))}")

    # 3. thethao.json
    thethao_items = []
    for it in NEWS_DATA:
        sc_num = f"{it['id']:02d}"
        tot_imgs = 24 if it["id"] == 4 else 12
        td = {
            "id": it["id"],
            "art_id": it["art_id"],
            "group": it["group"],
            "title": it["title"],
            "summary": it["summary"],
            "digest_line": it["digest_line"],
            "digest_title": it["digest_title"],
            "total_images": tot_imgs,
            "hide_date_chip": True,
            "source": it["source"],
            "news_source": it["news_source"],
            "voice": it["voice"],
            "voice_gender": it["voice_gender"],
            "audio_path": os.path.join(AUDIO_DIR, f"audio_{sc_num}.wav"),
            "audio_title": os.path.join(AUDIO_TITLE_DIR, f"audio_title_{sc_num}.wav"),
        }
        for i in range(1, tot_imgs + 1):
            td[f"image_{i}"] = os.path.join(IMG_DIR, f"Tin_{sc_num}_{i}.jpg")
        thethao_items.append(td)
        thethao_items.append(td)

    with open(os.path.join(DAY_DIR, "thethao.json"), "w", encoding="utf-8") as f:
        json.dump(thethao_items, f, ensure_ascii=False, indent=2)
    ok(f"Đã lưu: {paths.rel_to_root(os.path.join(DAY_DIR, 'thethao.json'))}")


def synthesize_audio_for_text(model: Vieneu, text: str, voice: str, speed: float, pitch: float, temp: float, force: bool = False) -> AudioSegment:
    clean_text, _ = prepare(text)
    chunks = build_chunks_from_text(clean_text, max_words_per_chunk=60, inter_sentence_pause=0.25)
    combined = AudioSegment.empty()
    for c in chunks:
        if c.get("type") == "pause":
            pause_ms = int(c.get("pause_sec", 0.25) * 1000)
            if pause_ms > 0:
                combined += AudioSegment.silent(duration=pause_ms, frame_rate=44100)
            continue
        c_text = c.get("text", "").strip()
        if not c_text:
            continue
        seg, is_hit = render_chunk_vitts(
            model, c_text, voice, temperature=temp, speed=speed, pitch=pitch,
            cache_dir=CACHE_DIR, use_cache=not force, max_chars=768
        )
        seg = trim_segment_silence(seg)
        combined += seg
    return combined


def synthesize_audio_all(force: bool = False, target_tin: Optional[int] = None):
    banner("SINH GIỌNG ĐỌC VITTS V3TURBO THEO CHUẨN NAM / NỮ", DAY_STR)
    model = Vieneu(mode="v3turbo")
    silence_08 = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)

    for it in NEWS_DATA:
        if target_tin and it["id"] != target_tin:
            continue
        sc_num = f"{it['id']:02d}"
        target_audio = os.path.join(AUDIO_DIR, f"audio_{sc_num}.wav")
        target_title = os.path.join(AUDIO_TITLE_DIR, f"audio_title_{sc_num}.wav")

        if not force and os.path.exists(target_audio) and os.path.exists(target_title) and os.path.getsize(target_audio) > 100_000:
            ok(f"Audio Tin #{sc_num} ({it['voice']}) đã có sẵn — bỏ qua.")
            continue

        step(f"Đang sinh giọng cho Tin #{sc_num}: {it['title'][:50]}... [Giọng: {it['voice']}]")

        # Tiêu đề
        seg_title = synthesize_audio_for_text(
            model, it["title"], voice=it["voice"], speed=it["speed"], pitch=it["pitch"], temp=it["temp"], force=force
        ).set_frame_rate(44100).set_channels(2)
        seg_title.export(target_title, format="wav")
        ok(f"  -> Đã lưu audio tiêu đề: {paths.rel_to_root(target_title)} ({len(seg_title)/1000:.2f}s)")

        # Nội dung
        seg_summary = synthesize_audio_for_text(
            model, it["summary"], voice=it["voice"], speed=it["speed"], pitch=it["pitch"], temp=it["temp"], force=force
        )

        combined = seg_title + silence_08 + seg_summary
        combined = apply_voice_standard(combined).set_frame_rate(44100).set_channels(2)
        combined.export(target_audio, format="wav")
        ok(f"  -> Đã lưu audio tổng thể: {paths.rel_to_root(target_audio)} ({len(combined)/1000:.2f}s)")


def generate_contact_sheet():
    banner("TẠO BẢNG ẢNH ĐỐI CHỨNG QA CONTACT SHEETS", DAY_STR)
    font_path = os.path.join(paths.FONTS, "IBM_Plex_Mono", "IBMPlexMono-Bold.ttf")
    fnt = ImageFont.truetype(font_path, 16) if os.path.exists(font_path) else ImageFont.load_default()

    queries_all = [
        (1, IMAGE_QUERIES_TIN_1),
        (2, IMAGE_QUERIES_TIN_2),
        (3, IMAGE_QUERIES_TIN_3),
        (4, IMAGE_QUERIES_TIN_4),
    ]

    for tin_id, q_list in queries_all:
        sc_num = f"{tin_id:02d}"
        out_contact = os.path.join(QA_DIR, f"contact_scene_{sc_num}.jpg")
        thumb_w, thumb_h = 360, 240
        if len(q_list) > 12:
            cols, rows = 6, 4
        else:
            cols, rows = 4, 3
        pad = 12
        sheet_w = cols * thumb_w + (cols + 1) * pad
        sheet_h = rows * (thumb_h + 30) + (rows + 1) * pad + 60

        sheet = Image.new("RGB", (sheet_w, sheet_h), (6, 9, 17))
        draw = ImageDraw.Draw(sheet)
        header_text = f"ĐIỂM ĐỌC THỂ THAO — BẢNG ĐỐI CHỨNG THỊ GIÁC QA (TIN #{sc_num}) — {DAY_STR}"
        draw.text((pad, 20), header_text, fill=(0, 229, 255), font=fnt)

        for i, (fn, _, cr, desc) in enumerate(q_list):
            r = i // cols
            c = i % cols
            x = pad + c * (thumb_w + pad)
            y = 60 + pad + r * (thumb_h + 30 + pad)

            img_file = os.path.join(IMG_DIR, fn)
            if os.path.exists(img_file):
                try:
                    im = Image.open(img_file).convert("RGB")
                    im = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                    sheet.paste(im, (x, y))
                except Exception:
                    draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], fill=(30, 41, 59))
            else:
                draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], fill=(30, 41, 59))

            cap_y = y + thumb_h
            draw.rectangle([(x, cap_y), (x + thumb_w, cap_y + 28)], fill=(15, 23, 42))
            draw.text((x + 6, cap_y + 4), f"{fn} | {cr}", fill=(226, 232, 240), font=fnt)

        sheet.save(out_contact, "JPEG", quality=92)
        ok(f"QA Contact Sheet đã lưu: {paths.rel_to_root(out_contact)}")


def render_thumbnail(tin_id: int):
    item = next(it for it in NEWS_DATA if it["id"] == tin_id)
    sc_num = f"{tin_id:02d}"
    banner(f"RENDER ẢNH BÌA DỌC 9:16 (TIN #{sc_num}: {item['slug']})", DAY_STR)

    out_thumb = os.path.join(SHORTS_OUT, item["thumb_name"])
    bg_img_path = os.path.join(IMG_DIR, item["thumb_bg_img"])
    if not os.path.exists(bg_img_path):
        bg_img_path = os.path.join(IMG_DIR, f"Tin_{sc_num}_1.jpg")

    bg_img_url = paths.file_url(bg_img_path)
    font_anton_url = paths.file_url(os.path.join(paths.FONTS, "Anton", "Anton-Regular.ttf"))
    font_oswald_url = paths.file_url(os.path.join(paths.FONTS, "Oswald", "static", "Oswald-Bold.ttf"))
    font_plex_url = paths.file_url(os.path.join(paths.FONTS, "IBM_Plex_Mono", "IBMPlexMono-Bold.ttf"))

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @font-face {{ font-family: 'Anton'; src: url('{font_anton_url}'); }}
  @font-face {{ font-family: 'Oswald'; src: url('{font_oswald_url}'); font-weight: 700; }}
  @font-face {{ font-family: 'PlexMono'; src: url('{font_plex_url}'); font-weight: 700; }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    width: 1080px;
    height: 1920px;
    background: #060911;
    overflow: hidden;
    font-family: 'Anton', sans-serif;
  }}
  .thumb-root {{
    position: relative;
    width: 1080px;
    height: 1920px;
    background: #060911;
  }}
  .bg-image {{
    position: absolute;
    top: 0;
    left: 0;
    width: 1080px;
    height: 1400px;
    object-fit: cover;
    object-position: center 25%;
    filter: brightness(0.95) contrast(1.08);
  }}
  .gradient-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg,
      rgba(6,9,17,0.3) 0%,
      transparent 25%,
      rgba(6,9,17,0.7) 48%,
      #060911 58%,
      #060911 100%
    );
  }}
  .glow-cyan {{
    position: absolute;
    width: 850px;
    height: 850px;
    background: radial-gradient(circle, rgba(0,229,255,0.22) 0%, transparent 70%);
    top: 55%;
    left: 50%;
    transform: translate(-50%, -30%);
    filter: blur(90px);
    pointer-events: none;
  }}
  .header-badge {{
    position: absolute;
    top: 70px;
    left: 60px;
    right: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }}
  .logo-box {{
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(15, 23, 42, 0.9);
    padding: 14px 28px;
    border-radius: 999px;
    border: 2px solid rgba(0, 229, 255, 0.5);
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.7), 0 0 15px rgba(0, 229, 255, 0.3);
  }}
  .logo-dot {{
    width: 18px;
    height: 18px;
    background: #00E5FF;
    border-radius: 50%;
    box-shadow: 0 0 14px #00E5FF;
  }}
  .logo-text {{
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #fff;
    text-transform: uppercase;
  }}
  .kicker-tag {{
    background: rgba(0, 229, 255, 0.15);
    border: 2px solid #00E5FF;
    padding: 12px 28px;
    border-radius: 999px;
    font-family: 'PlexMono', monospace;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #00E5FF;
    text-transform: uppercase;
  }}
  .stage-bottom {{
    position: absolute;
    bottom: 90px;
    left: 65px;
    right: 65px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    z-index: 10;
  }}
  .hero-title {{
    font-family: 'Anton', sans-serif;
    font-size: {item['thumb_hero_size']}px;
    font-weight: 400;
    line-height: 0.96;
    text-transform: uppercase;
    color: #FFFFFF;
    text-shadow: 0 0 35px rgba(0, 229, 255, 0.55), 0 4px 15px rgba(0,0,0,0.9);
    letter-spacing: 1px;
  }}
  .sub-title {{
    font-family: 'Oswald', sans-serif;
    font-size: 38px;
    font-weight: 700;
    line-height: 1.25;
    color: #00E5FF;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-left: 6px solid #00E5FF;
    padding-left: 20px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.8);
  }}
  .channel-pill {{
    display: inline-flex;
    align-items: center;
    gap: 12px;
    font-family: 'PlexMono', monospace;
    font-size: 22px;
    color: #94A3B8;
    letter-spacing: 2px;
    text-transform: uppercase;
  }}
</style>
</head>
<body>
<div class="thumb-root">
  <img class="bg-image" src="{bg_img_url}" alt="Hero Image">
  <div class="gradient-overlay"></div>
  <div class="glow-cyan"></div>

  <div class="header-badge">
    <div class="logo-box">
      <div class="logo-dot"></div>
      <div class="logo-text">ĐIỂM ĐỌC THỂ THAO</div>
    </div>
    <div class="kicker-tag">{item['thumb_kicker']}</div>
  </div>

  <div class="stage-bottom">
    <div class="hero-title">{item['thumb_hero']}</div>
    <div class="sub-title">{item['thumb_sub']}</div>
    <div class="channel-pill">KÊNH ĐIỂM ĐỌC // BẢN TIN THỜI SỰ CHÍNH THỨC</div>
  </div>
</div>
</body>
</html>
"""
    tmp_html_file = os.path.join(WORK_DIR, f"thumb_tin_{sc_num}_{int(time.time())}.html")
    with open(tmp_html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        page = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(paths.file_url(tmp_html_file), wait_until="networkidle")
        page.wait_for_timeout(350)
        page.screenshot(path=out_thumb, type="jpeg", quality=95)
        br.close()

    ok(f"Đã lưu thumbnail: {paths.rel_to_root(out_thumb)} ({os.path.getsize(out_thumb)/(1024):.1f} KB)")


def write_short_metadata(tin_id: int):
    item = next(it for it in NEWS_DATA if it["id"] == tin_id)
    sc_num = f"{tin_id:02d}"
    out_mota = os.path.join(SHORTS_OUT, item["mota_name"])
    banner(f"XUẤT FILE MÔ TẢ SEO YOUTUBE CHO TIN #{sc_num}", DAY_STR)

    content = f"""=== TIÊU ĐỀ YOUTUBE ===
{item['seo_title']}

=== MÔ TẢ VIDEO ===
{item['seo_desc']}

Đăng ký kênh Điểm Đọc để cập nhật những diễn biến thời sự và câu chuyện thể thao nổi bật mỗi ngày.

{item['seo_tags']}
"""
    with open(out_mota, "w", encoding="utf-8") as f:
        f.write(content)
    ok(f"Đã lưu mô tả: {paths.rel_to_root(out_mota)}")


def render_short_video(tin_id: int, force: bool = False) -> Optional[str]:
    item = next(it for it in NEWS_DATA if it["id"] == tin_id)
    sc_num = f"{tin_id:02d}"
    banner(f"DỰNG VIDEO SHORT 9:16 (TIN #{sc_num}: {item['slug']})", DAY_STR)

    t0 = time.time()
    out_path = os.path.join(SHORTS_OUT, item["file_name"])

    if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
        ok(f"Short đã có sẵn: {paths.rel_to_root(out_path)}")
        return out_path

    step(f"Xuất timeline short cho Tin #{sc_num} qua m8_news_bridge...")
    pdir, _, _ = export_bridge_project(
        DAY_DIR,
        item_id=tin_id,
        format_type="short",
        work_proj_dir=os.path.join(SHORTS_WORK, f"short_{sc_num}"),
        global_offset_sec=0.0
    )

    step(f"Render 9:16 trên template short_news_v2.html (30fps)...")
    v = render_html_engine(
        pdir,
        template="short_news_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True
    )

    if v and os.path.exists(v):
        shutil.copy2(v, out_path)
        ok(f"🎉 Hoàn thành Short #{sc_num}: {paths.rel_to_root(out_path)} ({os.path.getsize(out_path)/(1024*1024):.1f} MB)")
        banner(f"HOÀN THÀNH VIDEO SHORT #{sc_num} ({time.time() - t0:.1f}s)", DAY_STR)

        res = measure_loudness(out_path)
        ok(f"Kiểm toán âm lượng: I={res.get('input_i')} LUFS, TP={res.get('input_tp')} dBTP, LRA={res.get('input_lra')} LU")
        return out_path
    else:
        die(f"Render Short #{sc_num} thất bại!")
        return None


def main():
    force = "--force" in sys.argv
    step_flag = None
    target_tin = None
    for arg in sys.argv:
        if arg.startswith("--step="):
            step_flag = arg.split("=")[1]
        elif arg.startswith("--tin="):
            target_tin = int(arg.split("=")[1])

    setup_directories()

    # Bước 1: Tải ảnh
    if not step_flag or step_flag == "fetch":
        tins_to_fetch = [target_tin] if target_tin else [1, 2, 3, 4]
        q_map = {1: IMAGE_QUERIES_TIN_1, 2: IMAGE_QUERIES_TIN_2, 3: IMAGE_QUERIES_TIN_3, 4: IMAGE_QUERIES_TIN_4}
        for t in tins_to_fetch:
            if t in q_map:
                fetch_images_for_tin(t, q_map[t], force=force)

    # Bước 2: Cập nhật metadata json
    if not step_flag or step_flag in ["meta", "fetch"]:
        update_metadata_jsons()

    # Bước 3: Sinh audio
    if not step_flag or step_flag in ["voice", "audio"]:
        synthesize_audio_all(force=force, target_tin=target_tin)

    # Bước 4: Tạo Contact Sheet QA
    if not step_flag or step_flag in ["qa", "sheet"]:
        generate_contact_sheet()

    # Bước 5: Tạo Thumbnail và Mô tả
    if not step_flag or step_flag in ["thumb", "mota"]:
        target_ids = [target_tin] if target_tin else [it["id"] for it in NEWS_DATA]
        for it in NEWS_DATA:
            if it["id"] in target_ids:
                render_thumbnail(it["id"])
                write_short_metadata(it["id"])

    # Bước 6: Render video
    if not step_flag or step_flag in ["render", "video"]:
        tins_to_render = [target_tin] if target_tin else [1, 2, 3, 4]
        for tid in tins_to_render:
            render_short_video(tid, force=force)

    banner("TỔNG KẾT XUẤT BẢN CÁC VIDEO SHORTS HOÀN TẤT", DAY_STR)
    for it in NEWS_DATA:
        log(f"Tin #{it['id']:02d} [{it['voice_gender'].upper()} - {it['voice']}]:")
        log(f"  📱 Video:     {paths.rel_to_root(os.path.join(SHORTS_OUT, it['file_name']))}")
        log(f"  🖼️ Thumbnail: {paths.rel_to_root(os.path.join(SHORTS_OUT, it['thumb_name']))}")
        log(f"  📝 Mô tả:     {paths.rel_to_root(os.path.join(SHORTS_OUT, it['mota_name']))}")


if __name__ == "__main__":
    main()
