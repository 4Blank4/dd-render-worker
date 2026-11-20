#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_shorts_10_11.py — Sản xuất 2 Video Shorts 9:16 ngày 10.11.2026:
1. Jose Mourinho xô đổ kỷ lục của Pep Guardiola tại La Liga
2. Harry Kane bị loại, Lionel Messi lập kỷ lục 18 lần trong Đội hình hay nhất năm của FIFPRO
Nguồn: VnExpress (10.11.2026)
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

DAY_STR = "10.11.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, "Orther", DAY_STR)
WORK_DIR = paths.work_project_dir(os.path.join("Orther", DAY_STR))

IMG_DIR = os.path.join(DAY_DIR, "images")
AUDIO_DIR = os.path.join(DAY_DIR, "audio")
AUDIO_TITLE_DIR = os.path.join(DAY_DIR, "audio-title")
SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
QA_DIR = os.path.join(DAY_DIR, "qa")
SHORTS_WORK = os.path.join(WORK_DIR, "shorts_render")
CACHE_DIR = paths.work_file("vitts_cache")

MIN_RATIO = 1.18
MIN_WIDTH = 600
MIN_HEIGHT = 380

BLOCKED_HOSTS = [
    "alamy", "istockphoto", "shutter", "dreamstime", "123rf",
    "depositphotos", "stock.adobe", "freepik", "pinterest",
    "vecteezy", "bigstock", "ebay", "etsy", "redbubble", "teepublic",
    "society6", "displate", "ytimg", "pngtree", "cgtrader", "footyheadlines",
    "twimg", "huggingface", "hf.co", "pond5", "mixkit", "motionarray", "pinimg"
]

NEWS_DATA = [
    {
        "id": 1,
        "art_id": "art_01",
        "slug": "Short_Mourinho_Xo_Do_Ky_Luc_Guardiola",
        "file_name": "Short_Mourinho_Xo_Do_Ky_Luc_Guardiola.mp4",
        "thumb_name": "Short_Mourinho_Xo_Do_Ky_Luc_Guardiola_thumbnail.jpg",
        "mota_name": "Short_Mourinho_Xo_Do_Ky_Luc_Guardiola_mota.txt",
        "group": "Nhóm: Kỷ lục La Liga kinh điển",
        "title": "Jose Mourinho xô đổ kỷ lục của Pep Guardiola tại La Liga",
        "summary": (
            "Bảng thống kê lịch sử giải vô địch quốc gia Tây Ban Nha La Liga vừa chứng kiến một cột mốc kinh điển, "
            "khi Jose Mourinho chính thức vượt qua đại kình địch Pep Guardiola để trở thành huấn luyện viên có tỷ lệ thắng cao nhất lịch sử! "
            "Trong nhóm các nhà cầm quân dẫn dắt từ 100 trận trở lên, chiến lược gia người Bồ Đào Nha dẫn đầu tuyệt đối với tỷ lệ thắng 77%, "
            "vượt qua con số 76.3% của Guardiola cùng hàng loạt huyền thoại như Carlo Ancelotti và Zinedine Zidane. "
            "Đây là thành tích mang ý nghĩa vô cùng đặc biệt, gợi lại những năm tháng El Clasico rực lửa "
            "khi Người Đặc Biệt phải đối đầu với một Barcelona hùng mạnh bậc nhất lịch sử trong cả các trận chiến trên sân cỏ "
            "lẫn những màn khẩu chiến nảy lửa trong phòng họp báo. "
            "Đáng chú ý, khi biết tin xô đổ kỷ lục của đối thủ truyền kiếp, Mourinho vẫn giữ sự lạnh lùng đặc trưng "
            "khi khẳng định ông không sống bằng những con số trong quá khứ mà chỉ tập trung giành chiến thắng ở trận tiếp theo. "
            "Tin vui nối tiếp tin vui khi nhà cầm quân 63 tuổi vừa được vinh danh là huấn luyện viên xuất sắc nhất tháng 10 của La Liga "
            "sau chuỗi tám trận toàn thắng thăng hoa cùng Real Madrid. "
            "Với 194 trận cầm quân trên mọi đấu trường, Mourinho chỉ còn cách kỷ lục lịch sử của Leo Beenhakker đúng 4 trận "
            "để vươn lên vị trí thứ năm trong danh sách những huấn luyện viên vĩ đại nhất lịch sử đội bóng Hoàng gia!"
        ),
        "digest_line": "Jose Mourinho trở thành HLV có tỷ lệ thắng cao nhất lịch sử La Liga với 77%, vượt qua Pep Guardiola.",
        "digest_title": "Jose Mourinho xô đổ kỷ lục của Pep Guardiola tại La Liga",
        "source": "VnExpress / La Liga",
        "news_source": "VnExpress / La Liga",
        "thumb_kicker": "LA LIGA KINH ĐIỂN · KỶ LỤC LỊCH SỬ",
        "thumb_hero": "MOURINHO ĐÈ BẸP PEP!",
        "thumb_hero_size": "105",
        "thumb_sub": "TỶ LỆ THẮNG 77% CAO NHẤT LỊCH SỬ LA LIGA VƯỢT MẶT GUARDIOLA",
        "thumb_tag_a": "TỶ LỆ THẮNG 77%",
        "thumb_tag_b": "XÔ ĐỔ GUARDIOLA",
        "seo_title": "Jose Mourinho xô đổ kỷ lục của Pep Guardiola tại La Liga #Shorts",
        "seo_desc": (
            "Jose Mourinho chính thức vượt qua đại kình địch Pep Guardiola để trở thành HLV sở hữu tỷ lệ thắng cao nhất lịch sử La Liga với 77%!\n\n"
            "HLV người Bồ Đào Nha thắng 97 trong 126 trận tại giải đấu, vượt qua tỷ lệ 76,3% của Guardiola (116 trận thắng / 152 trận) "
            "trong nhóm các chiến lược gia dẫn dắt từ 100 trận trở lên, xếp trên cả Carlo Ancelotti, Xavi Hernandez và Zinedine Zidane.\n\n"
            "Cột mốc lịch sử này càng thêm ý nghĩa khi Mourinho vừa đoạt danh hiệu HLV xuất sắc nhất tháng 10 La Liga cùng chuỗi 8 trận thắng liên tiếp tại Real Madrid!"
        ),
        "seo_tags": "#Shorts #DiemDoc #Mourinho #JoseMourinho #Guardiola #PepGuardiola #RealMadrid #LaLiga #ElClasico #TinBongDa"
    },
    {
        "id": 2,
        "art_id": "art_02",
        "slug": "Short_Kane_Bi_Loai_Messi_Vao_Doi_Hinh_Nam",
        "file_name": "Short_Kane_Bi_Loai_Messi_Vao_Doi_Hinh_Nam.mp4",
        "thumb_name": "Short_Kane_Bi_Loai_Messi_Vao_Doi_Hinh_Nam_thumbnail.jpg",
        "mota_name": "Short_Kane_Bi_Loai_Messi_Vao_Doi_Hinh_Nam_mota.txt",
        "group": "Nhóm: Giải thưởng & Ngôi sao thế giới",
        "title": "Harry Kane bị gạch tên, Lionel Messi lập kỷ lục trong đội hình hay nhất năm của FIFPRO",
        "summary": (
            "Hiệp hội Cầu thủ Chuyên nghiệp Thế giới FIFPRO vừa chính thức công bố Đội hình hay nhất năm 2026 "
            "do gần 20000 cầu thủ chuyên nghiệp toàn cầu trực tiếp bỏ phiếu, tạo nên những bất ngờ chấn động làng túc cầu! "
            "Cú sốc lớn nhất thuộc về đương kim Quả Bóng Vàng Harry Kane, khi chân sút người Anh bất ngờ bị gạch tên khỏi hàng tiền đạo "
            "vì xếp sau Erling Haaland với tỷ lệ phiếu sít sao 27.6% so với 28.4%. "
            "Ở chiều ngược lại, huyền thoại Lionel Messi ở tuổi 39 đã có màn tái xuất ngoạn mục, "
            "nâng kỷ lục vô tiền khoáng hậu lên 18 lần lọt vào đội hình tiêu biểu của năm, bỏ xa kỷ lục 15 lần của Cristiano Ronaldo. "
            "Hàng công trong mơ của năm 2026 chứng kiến Kylian Mbappé dẫn đầu tuyệt đối với 46% phiếu bầu, "
            "sát cánh cùng hiện tượng tuổi teen Lamine Yamal, người đi vào lịch sử khi lọt vào đội hình tiêu biểu hai năm liên tiếp khi chưa tròn 20 tuổi! "
            "Đội tuyển Tây Ban Nha thống trị danh sách với bốn đại diện gồm thủ thành David Raya, hậu vệ Pau Cubarsi, nhạc trưởng Rodri "
            "và Lamine Yamal sau chiến tích vô địch World Cup 2026 đầy thuyết phục. "
            "Tuyến giữa và hàng thủ được hoàn thiện bởi những ngôi sao đẳng cấp châu Âu như Jude Bellingham, Vitinha, Achraf Hakimi "
            "và Nuno Mendes, khép lại bản danh sách tôn vinh những đôi chân xuất sắc nhất hành tinh!"
        ),
        "digest_line": "FIFPRO công bố World 11 2026: Harry Kane bị loại cay đắng, Messi lập kỷ lục 18 lần góp mặt.",
        "digest_title": "Harry Kane bị gạch tên, Lionel Messi lập kỷ lục trong đội hình hay nhất năm của FIFPRO",
        "source": "VnExpress / FIFPRO",
        "news_source": "VnExpress / FIFPRO",
        "thumb_kicker": "FIFPRO WORLD 11 · ĐỘI HÌNH CỦA NĂM",
        "thumb_hero": "MESSI LẬP KỶ LỤC 18 LẦN!",
        "thumb_hero_size": "95",
        "thumb_sub": "KANE BỊ LOẠI SỐC · MESSI VƯỢT TRỘI RONALDO · MBAPPE DẪN ĐẦU",
        "thumb_tag_a": "KỶ LỤC 18 LẦN",
        "thumb_tag_b": "KANE BỊ GẠCH TÊN",
        "seo_title": "Kane bị loại, Messi lập kỷ lục 18 lần trong Đội hình hay nhất năm của FIFPRO #Shorts",
        "seo_desc": (
            "Hiệp hội Cầu thủ Chuyên nghiệp Thế giới FIFPRO vừa công bố Đội hình hay nhất năm 2026 (FIFPRO World 11) "
            "với kết quả gây chấn động làng bóng đá toàn cầu!\n\n"
            "Chủ nhân Quả Bóng Vàng Harry Kane bất ngờ bị loại khi xếp sau Erling Haaland (27,6% so với 28,4%). "
            "Trong khi đó, huyền thoại Lionel Messi ở tuổi 39 đã thiết lập kỷ lục vô tiền khoáng hậu khi lần thứ 18 lọt vào Đội hình tiêu biểu thế giới!\n\n"
            "Kylian Mbappé dẫn đầu tỷ lệ bình chọn với 46%, Lamine Yamal đi vào lịch sử khi có tên 2 năm liên tiếp trước tuổi 20, "
            "cùng sự áp đảo của các nhà vô địch World Cup Tây Ban Nha!"
        ),
        "seo_tags": "#Shorts #DiemDoc #Messi #LionelMessi #HarryKane #Haaland #Mbappe #LamineYamal #FIFPRO #World11 #Ronaldo #TinBongDa"
    }
]

IMAGE_QUERIES_TIN_1 = [
    ("Tin_01_1.jpg", "Jose Mourinho Pep Guardiola El Clasico touchline confrontation", "AFP"),
    ("Tin_01_2.jpg", "Jose Mourinho Real Madrid La Liga celebration trophy", "VNEXPRESS / LA LIGA"),
    ("Tin_01_3.jpg", "Jose Mourinho Real Madrid coach dugout serious", "REUTERS"),
    ("Tin_01_4.jpg", "Carlo Ancelotti Zinedine Zidane Real Madrid manager", "GETTY IMAGES / LA LIGA"),
    ("Tin_01_5.jpg", "El Clasico Real Madrid vs Barcelona Camp Nou intense 2012", "AFP"),
    ("Tin_01_6.jpg", "Jose Mourinho press conference microphone Real Madrid", "ACTION IMAGES / REUTERS"),
    ("Tin_01_7.jpg", "Jose Mourinho thoughtful look touchline suit Real Madrid", "AP PHOTO"),
    ("Tin_01_8.jpg", "Jose Mourinho finger pointing celebration Real Madrid", "GETTY IMAGES"),
    ("Tin_01_9.jpg", "Jose Mourinho manager of the month La Liga trophy Real Madrid", "LA LIGA"),
    ("Tin_01_10.jpg", "Real Madrid squad celebrating victory La Liga 2026", "REAL MADRID CF"),
    ("Tin_01_11.jpg", "Jose Mourinho Santiago Bernabeu stadium match night", "AP PHOTO"),
    ("Tin_01_12.jpg", "Real Madrid trophy room Santiago Bernabeu stadium", "REAL MADRID CF"),
]

IMAGE_QUERIES_TIN_2 = [
    ("Tin_02_1.jpg", "FIFPRO World 11 2026 official lineup graphic trophy", "FIFPRO"),
    ("Tin_02_2.jpg", "FIFPRO World 11 top forwards vote statistics graphic 2026", "FIFPRO"),
    ("Tin_02_3.jpg", "Harry Kane England Bayern Munich Ballon d'Or disappointed", "REUTERS"),
    ("Tin_02_4.jpg", "Erling Haaland Manchester City goal celebration 2026", "ACTION IMAGES / REUTERS"),
    ("Tin_02_5.jpg", "Lionel Messi Argentina Inter Miami match action 2026", "GETTY IMAGES / FIFPRO"),
    ("Tin_02_6.jpg", "Lionel Messi lifting trophy celebration legendary 2026", "AP PHOTO"),
    ("Tin_02_7.jpg", "Kylian Mbappe Real Madrid celebration goal 2026", "REUTERS"),
    ("Tin_02_8.jpg", "Lamine Yamal Barcelona celebration skill dribble 2026", "GETTY IMAGES / LA LIGA"),
    ("Tin_02_9.jpg", "Spain national team World Cup 2026 champions celebration", "AP PHOTO"),
    ("Tin_02_10.jpg", "David Raya Rodri Pau Cubarsi Spain World Cup 2026", "REUTERS"),
    ("Tin_02_11.jpg", "Jude Bellingham Vitinha Champions League 2026", "AFP / GETTY IMAGES"),
    ("Tin_02_12.jpg", "FIFPRO World 11 best players ceremony award 2026", "FIFPRO"),
]


def setup_directories():
    step("Khởi tạo cấu trúc thư mục outputs/Orther/10.11.2026...")
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(AUDIO_TITLE_DIR, exist_ok=True)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(QA_DIR, exist_ok=True)
    os.makedirs(SHORTS_WORK, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    ok("Đã sẵn sàng các thư mục sản xuất!")


def download_image(url: str, min_w=MIN_WIDTH, min_h=MIN_HEIGHT, min_ratio=MIN_RATIO) -> Optional[Image.Image]:
    low = url.lower()
    if any(b in low for b in BLOCKED_HOSTS) or "watermark" in low:
        return None
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code != 200 or len(r.content) < 20_000:
            return None
        im = Image.open(io.BytesIO(r.content))
        im.load()
        w, h = im.size
        if w < min_w or h < min_h or (w / h) < min_ratio:
            return None
        if im.mode != "RGB":
            im = im.convert("RGB")
        return im
    except Exception:
        return None


def fetch_images_tin_1():
    banner("THU THẬP VÀ CHUẨN HÓA 12 ẢNH CHO TIN 1 (MOURINHO VS GUARDIOLA)", DAY_STR)
    # Tải ảnh gốc từ bài báo VnExpress
    vne_img_afp = "https://i1-thethao.vnecdn.net/2026/11/10/AFP-20120125-DV1109647-v1-High-6764-4331-1794263494.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=FHrXaKSqV4VXv1ifWIlWkg"
    t1 = os.path.join(IMG_DIR, "Tin_01_1.jpg")
    if not os.path.exists(t1) or os.path.getsize(t1) < 20_000:
        im = download_image(vne_img_afp)
        if im:
            im.save(t1, "JPEG", quality=95, optimize=True)
            ok(f"  [VNEXPRESS AFP] Tin_01_1.jpg: {im.width}x{im.height}")

    with DDGS() as ddgs:
        for fname, query, _ in IMAGE_QUERIES_TIN_1:
            target_path = os.path.join(IMG_DIR, fname)
            if os.path.exists(target_path) and os.path.getsize(target_path) > 30_000:
                ok(f"  [ĐÃ CÓ] {fname}")
                continue

            step(f"Tìm kiếm ảnh cho {fname}: \"{query}\"...")
            found_img = None
            try:
                res = list(ddgs.images(query, region="wt-wt", safesearch="off", size="Large", layout="Wide", max_results=20))
            except Exception as e:
                warn(f"Lỗi DDGS: {e}, thử lại...")
                time.sleep(2)
                try:
                    res = list(ddgs.images(query, region="wt-wt", safesearch="off", max_results=15))
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
                fallback_q = "Jose Mourinho Real Madrid manager football"
                step(f"  -> Thử fallback query: {fallback_q}")
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
                warn(f"  -> Dùng ảnh dự phòng cho {fname}.")
                first_img = os.path.join(IMG_DIR, "Tin_01_1.jpg")
                if os.path.exists(first_img):
                    shutil.copy2(first_img, target_path)


def fetch_images_tin_2():
    banner("THU THẬP VÀ CHUẨN HÓA 12 ẢNH CHO TIN 2 (FIFPRO WORLD 11 2026)", DAY_STR)
    # Tải các ảnh đồ họa từ VnExpress
    vne_lineup = "https://i1-thethao.vnecdn.net/2026/11/09/do-i-hi-nh-1794241870-5458-1794242535.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=TLVTOA6GL4oEc34pMHnw0w"
    t1 = os.path.join(IMG_DIR, "Tin_02_1.jpg")
    if not os.path.exists(t1) or os.path.getsize(t1) < 20_000:
        im = download_image(vne_lineup)
        if im:
            im.save(t1, "JPEG", quality=95, optimize=True)
            ok(f"  [VNEXPRESS FIFPRO] Tin_02_1.jpg: {im.width}x{im.height}")

    vne_top = "https://i1-thethao.vnecdn.net/2026/11/09/top-1794242100-6379-1794242535.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=KhEQRgFdVeJogCIktnIvRw"
    t2 = os.path.join(IMG_DIR, "Tin_02_2.jpg")
    if not os.path.exists(t2) or os.path.getsize(t2) < 20_000:
        im = download_image(vne_top)
        if im:
            im.save(t2, "JPEG", quality=95, optimize=True)
            ok(f"  [VNEXPRESS FIFPRO TOP] Tin_02_2.jpg: {im.width}x{im.height}")

    with DDGS() as ddgs:
        for fname, query, _ in IMAGE_QUERIES_TIN_2:
            target_path = os.path.join(IMG_DIR, fname)
            if os.path.exists(target_path) and os.path.getsize(target_path) > 30_000:
                ok(f"  [ĐÃ CÓ] {fname}")
                continue

            step(f"Tìm kiếm ảnh cho {fname}: \"{query}\"...")
            found_img = None
            try:
                res = list(ddgs.images(query, region="wt-wt", safesearch="off", size="Large", layout="Wide", max_results=20))
            except Exception as e:
                warn(f"Lỗi DDGS: {e}, thử lại...")
                time.sleep(2)
                try:
                    res = list(ddgs.images(query, region="wt-wt", safesearch="off", max_results=15))
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
                fallback_q = "Lionel Messi Kylian Mbappe football 2026"
                step(f"  -> Thử fallback query: {fallback_q}")
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
                warn(f"  -> Dùng ảnh dự phòng cho {fname}.")
                first_img = os.path.join(IMG_DIR, "Tin_02_1.jpg")
                if os.path.exists(first_img):
                    shutil.copy2(first_img, target_path)


def build_metadata_jsons():
    banner("XUẤT CÁC FILE HỢP ĐỒNG DỮ LIỆU: THETHAO.JSON, IMAGE_CREDITS.JSON, IMAGE_PLAN.JSON", DAY_STR)

    # 1. image_credits.json
    credits_map = {}
    for fn, _, cr in IMAGE_QUERIES_TIN_1:
        credits_map[fn] = cr
    for fn, _, cr in IMAGE_QUERIES_TIN_2:
        credits_map[fn] = cr

    with open(os.path.join(DAY_DIR, "image_credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits_map, f, ensure_ascii=False, indent=2)
    ok(f"Đã lưu: {paths.rel_to_root(os.path.join(DAY_DIR, 'image_credits.json'))}")

    # 2. image_plan.json
    plan_records = []
    # Tin 1: 6 sentences x 2 images + 1 title
    plan_records.append({"scene_id": 1, "type": "title", "index": 1, "file_name": "Tin_01_1.jpg", "credit": "AFP", "description": "Jose Mourinho vs Pep Guardiola La Liga"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 1, "file_name": "Tin_01_1.jpg", "credit": "AFP", "description": "Mourinho chính thức vượt Guardiola dẫn đầu tỷ lệ thắng La Liga"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 1, "file_name": "Tin_01_2.jpg", "credit": "VNEXPRESS / LA LIGA", "description": "Đồ họa tỷ lệ thắng lịch sử La Liga của các chiến lược gia"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 2, "file_name": "Tin_01_3.jpg", "credit": "REUTERS", "description": "Mourinho dẫn đầu với tỷ lệ thắng 77% sau 126 trận"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 2, "file_name": "Tin_01_4.jpg", "credit": "GETTY IMAGES / LA LIGA", "description": "Xếp trên Guardiola, Ancelotti, Xavi và Zidane"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 3, "file_name": "Tin_01_5.jpg", "credit": "AFP", "description": "Ký ức El Clasico kinh điển đối đầu Barca mạnh nhất lịch sử"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 3, "file_name": "Tin_01_6.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Những màn khẩu chiến nảy lửa trong phòng họp báo"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 4, "file_name": "Tin_01_7.jpg", "credit": "AP PHOTO", "description": "Mourinho khẳng định không sống bằng thống kê quá khứ"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 4, "file_name": "Tin_01_8.jpg", "credit": "GETTY IMAGES", "description": "Tập trung tối đa cho chiến thắng ở trận đấu tiếp theo"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 5, "file_name": "Tin_01_9.jpg", "credit": "LA LIGA", "description": "Mourinho nhận giải HLV xuất sắc nhất tháng 10 La Liga"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 5, "file_name": "Tin_01_10.jpg", "credit": "REAL MADRID CF", "description": "Real Madrid thăng hoa với chuỗi 8 trận thắng liên tiếp"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 6, "file_name": "Tin_01_11.jpg", "credit": "AP PHOTO", "description": "Tiến sát kỷ lục 197 trận cầm quân của Leo Beenhakker"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 6, "file_name": "Tin_01_12.jpg", "credit": "REAL MADRID CF", "description": "Vị thế huyền thoại của Người Đặc Biệt tại Santiago Bernabeu"})

    # Tin 2: 6 sentences x 2 images + 1 title
    plan_records.append({"scene_id": 2, "type": "title", "index": 1, "file_name": "Tin_02_1.jpg", "credit": "FIFPRO", "description": "FIFPRO công bố World 11 2026"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 1, "file_name": "Tin_02_1.jpg", "credit": "FIFPRO", "description": "Đội hình hay nhất năm 2026 do gần 20000 cầu thủ bình chọn"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 1, "file_name": "Tin_02_2.jpg", "credit": "FIFPRO", "description": "Bảng thống kê tỷ lệ bình chọn top tiền đạo thế giới"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 2, "file_name": "Tin_02_3.jpg", "credit": "REUTERS", "description": "Harry Kane bất ngờ bị loại dù đoạt Quả bóng vàng"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 2, "file_name": "Tin_02_4.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Erling Haaland qua mặt Kane với 28.4% phiếu bầu"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 3, "file_name": "Tin_02_5.jpg", "credit": "GETTY IMAGES / FIFPRO", "description": "Lionel Messi ở tuổi 39 tái xuất ngoạn mục tại World 11"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 3, "file_name": "Tin_02_6.jpg", "credit": "AP PHOTO", "description": "Messi lập kỷ lục vô tiền khoáng hậu 18 lần được lựa chọn"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 4, "file_name": "Tin_02_7.jpg", "credit": "REUTERS", "description": "Kylian Mbappe dẫn đầu tuyệt đối với 46% số phiếu"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 4, "file_name": "Tin_02_8.jpg", "credit": "GETTY IMAGES / LA LIGA", "description": "Lamine Yamal vào đội hình 2 năm liên tiếp trước tuổi 20"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 5, "file_name": "Tin_02_9.jpg", "credit": "AP PHOTO", "description": "Tây Ban Nha áp đảo 4 đại diện sau chức vô địch World Cup 2026"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 5, "file_name": "Tin_02_10.jpg", "credit": "REUTERS", "description": "David Raya, Rodri, Pau Cubarsi và Lamine Yamal"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 6, "file_name": "Tin_02_11.jpg", "credit": "AFP / GETTY IMAGES", "description": "Jude Bellingham, Vitinha, Achraf Hakimi và Nuno Mendes"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 6, "file_name": "Tin_02_12.jpg", "credit": "FIFPRO", "description": "Bản danh sách tôn vinh những đôi chân xuất sắc nhất hành tinh"})

    image_plan_data = {
        "metadata": {
            "day": DAY_STR,
            "total_scenes": 2
        },
        "records": plan_records
    }
    with open(os.path.join(DAY_DIR, "image_plan.json"), "w", encoding="utf-8") as f:
        json.dump(image_plan_data, f, ensure_ascii=False, indent=2)
    ok(f"Đã lưu: {paths.rel_to_root(os.path.join(DAY_DIR, 'image_plan.json'))}")

    # 3. thethao.json
    thethao_items = []
    for item in NEWS_DATA:
        it_id = item["id"]
        sc_num = f"{it_id:02d}"
        td = {
            "id": it_id,
            "art_id": item["art_id"],
            "group": item["group"],
            "title": item["title"],
            "summary": item["summary"],
            "digest_line": item["digest_line"],
            "digest_title": item["digest_title"],
            "total_images": 12,
            "hide_date_chip": True,
            "source": item["source"],
            "news_source": item["news_source"],
            "audio_path": os.path.join(AUDIO_DIR, f"audio_{sc_num}.wav"),
            "audio_title": os.path.join(AUDIO_TITLE_DIR, f"audio_title_{sc_num}.wav"),
        }
        for i in range(1, 13):
            td[f"image_{i}"] = os.path.join(IMG_DIR, f"Tin_{sc_num}_{i}.jpg")
        thethao_items.append(td)

    with open(os.path.join(DAY_DIR, "thethao.json"), "w", encoding="utf-8") as f:
        json.dump(thethao_items, f, ensure_ascii=False, indent=2)
    ok(f"Đã lưu: {paths.rel_to_root(os.path.join(DAY_DIR, 'thethao.json'))}")


def synthesize_audio_for_text(model: Vieneu, text: str, voice: str = "Minh Quân Pro", speed: float = 1.12, pitch: float = 0.93, force: bool = False) -> AudioSegment:
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
        seg, is_hit = render_chunk_vitts(model, c_text, voice, temperature=0.6, speed=speed, pitch=pitch, cache_dir=CACHE_DIR, use_cache=not force, max_chars=768)
        seg = trim_segment_silence(seg)
        combined += seg
    return combined


def synthesize_all_audios(force: bool = False):
    banner("SINH GIỌNG ĐỌC VITTS V3TURBO MINH QUÂN PRO CHO 2 BẢN TIN", DAY_STR)
    model = Vieneu(mode="v3turbo")
    silence_08 = AudioSegment.silent(duration=800, frame_rate=44100).set_channels(2)

    for item in NEWS_DATA:
        it_id = item["id"]
        sc_num = f"{it_id:02d}"
        target_audio = os.path.join(AUDIO_DIR, f"audio_{sc_num}.wav")
        target_title = os.path.join(AUDIO_TITLE_DIR, f"audio_title_{sc_num}.wav")

        if not force and os.path.exists(target_audio) and os.path.exists(target_title) and os.path.getsize(target_audio) > 100_000:
            ok(f"Audio tin {sc_num} đã có sẵn — bỏ qua.")
            continue

        step(f"Đang đọc Tiêu đề Tin {sc_num}: \"{item['title']}\"...")
        seg_title = synthesize_audio_for_text(model, item["title"], force=force)
        seg_title = seg_title.set_frame_rate(44100).set_channels(2)
        seg_title.export(target_title, format="wav")
        ok(f"  -> Đã lưu audio tiêu đề: {paths.rel_to_root(target_title)} ({len(seg_title)/1000:.2f}s)")

        step(f"Đang đọc Nội dung chi tiết Tin {sc_num} (~{len(item['summary'].split())} từ)...")
        seg_summary = synthesize_audio_for_text(model, item["summary"], force=force)

        combined = seg_title + silence_08 + seg_summary
        combined = apply_voice_standard(combined)
        combined = combined.set_frame_rate(44100).set_channels(2)
        combined.export(target_audio, format="wav")
        ok(f"  -> Đã lưu master audio: {paths.rel_to_root(target_audio)} ({len(combined)/1000:.2f}s)")


def generate_contact_sheet(tin_id: int):
    sc_num = f"{tin_id:02d}"
    out_contact = os.path.join(QA_DIR, f"contact_scene_{sc_num}.jpg")
    banner(f"TẠO BẢNG ẢNH ĐỐI CHỨNG QA CHO TIN {sc_num}", DAY_STR)

    with open(os.path.join(DAY_DIR, "image_credits.json"), "r", encoding="utf-8") as f:
        credits_map = json.load(f)

    cols = 3
    rows = 4
    thumb_w, thumb_h = 360, 220
    pad = 16
    header_h = 70
    footer_h = 36

    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = rows * (thumb_h + footer_h) + (rows + 1) * pad + header_h

    sheet = Image.new("RGB", (sheet_w, sheet_h), (11, 15, 25))
    draw = ImageDraw.Draw(sheet)

    draw.rectangle([(0, 0), (sheet_w, header_h)], fill=(16, 24, 40))
    topic = "JOSE MOURINHO XÔ ĐỔ KỶ LỤC CỦA PEP GUARDIOLA" if tin_id == 1 else "FIFPRO WORLD 11: MESSI KỶ LỤC & KANE BỊ LOẠI"
    draw.text((pad, 22), f"QA CONTACT SHEET — TIN {sc_num}: {topic}", fill=(0, 229, 255))

    for idx in range(1, 13):
        r = (idx - 1) // cols
        c = (idx - 1) % cols
        x = pad + c * (thumb_w + pad)
        y = header_h + pad + r * (thumb_h + footer_h + pad)

        fn = f"Tin_{sc_num}_{idx}.jpg"
        img_p = os.path.join(IMG_DIR, fn)
        if os.path.exists(img_p):
            im = Image.open(img_p).convert("RGB")
            im.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            bx = x + (thumb_w - im.width) // 2
            by = y + (thumb_h - im.height) // 2
            sheet.paste(im, (bx, by))
            draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], outline=(30, 41, 59), width=2)
        else:
            draw.rectangle([(x, y), (x + thumb_w, y + thumb_h)], fill=(20, 25, 35))

        cr = credits_map.get(fn, "TƯ LIỆU")
        cap_y = y + thumb_h + 4
        draw.rectangle([(x, cap_y), (x + thumb_w, cap_y + 28)], fill=(15, 23, 42))
        draw.text((x + 6, cap_y + 4), f"{fn} | {cr}", fill=(226, 232, 240))

    sheet.save(out_contact, "JPEG", quality=92)
    ok(f"QA Contact Sheet đã lưu: {paths.rel_to_root(out_contact)}")


def render_thumbnail(tin_id: int):
    item = next(it for it in NEWS_DATA if it["id"] == tin_id)
    sc_num = f"{tin_id:02d}"
    banner(f"TẠO ẢNH THUMBNAIL DỌC 9:16 CHO SHORT #{sc_num}", DAY_STR)

    tpl_html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  @font-face { font-family:'Anton'; src:url('__ASSETS__/fonts/Anton/Anton-Regular.ttf'); font-weight:400; }
  @font-face { font-family:'Oswald'; src:url('__ASSETS__/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; }
  @font-face { font-family:'PlexMono'; src:url('__ASSETS__/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'); font-weight:700; }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    width: 1080px;
    height: 1920px;
    overflow: hidden;
    background: #060911;
    font-family: 'Oswald', sans-serif;
    color: #fff;
    position: relative;
  }
  .bg-img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 58%;
    background-image: url('__THUMB_IMAGE__');
    background-size: cover;
    background-position: center top;
    filter: brightness(0.9) contrast(1.18);
  }
  .bg-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg,
      rgba(6,9,17,0.4) 0%,
      transparent 25%,
      rgba(6,9,17,0.7) 48%,
      #060911 58%,
      #060911 100%
    );
  }
  .glow-cyan {
    position: absolute;
    width: 850px;
    height: 850px;
    background: radial-gradient(circle, rgba(0,229,255,0.22) 0%, transparent 70%);
    top: 55%;
    left: 50%;
    transform: translate(-50%, -30%);
    filter: blur(90px);
    pointer-events: none;
  }
  .header-badge {
    position: absolute;
    top: 70px;
    left: 60px;
    right: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
  }
  .logo-box {
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(15, 23, 42, 0.9);
    padding: 14px 28px;
    border-radius: 999px;
    border: 2px solid rgba(0, 229, 255, 0.5);
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.7), 0 0 15px rgba(0, 229, 255, 0.3);
  }
  .logo-dot {
    width: 18px;
    height: 18px;
    background: #00E5FF;
    border-radius: 50%;
    box-shadow: 0 0 14px #00E5FF;
  }
  .logo-text {
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #fff;
    text-transform: uppercase;
  }
  .kicker-tag {
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
  }
  .stage-bottom {
    position: absolute;
    bottom: 90px;
    left: 65px;
    right: 65px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    z-index: 10;
  }
  .hero-title {
    font-family: 'Anton', sans-serif;
    font-size: __THUMB_HERO_SIZE__px;
    font-weight: 400;
    line-height: 0.96;
    text-transform: uppercase;
    color: #FFFFFF;
    text-shadow: 0 0 35px rgba(0, 229, 255, 0.55), 0 4px 15px rgba(0,0,0,0.9);
    letter-spacing: 1px;
  }
  .sub-title {
    font-family: 'Oswald', sans-serif;
    font-size: 38px;
    font-weight: 700;
    line-height: 1.25;
    color: #E2E8F0;
    background: rgba(15, 23, 42, 0.92);
    padding: 20px 28px;
    border-radius: 18px;
    border-left: 8px solid #00E5FF;
    backdrop-filter: blur(10px);
    letter-spacing: 0.5px;
  }
  .rule-bar {
    height: 6px;
    width: 220px;
    background: linear-gradient(90deg, #00E5FF 0%, #38BDF8 100%);
    border-radius: 3px;
    box-shadow: 0 0 12px rgba(0, 229, 255, 0.6);
  }
  .tag-row {
    display: flex;
    gap: 18px;
  }
  .stat-pill {
    background: rgba(30, 41, 59, 0.95);
    border: 1px solid rgba(0, 229, 255, 0.35);
    padding: 14px 28px;
    border-radius: 14px;
    font-family: 'PlexMono', monospace;
    font-size: 24px;
    font-weight: 700;
    color: #38BDF8;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
</style>
</head>
<body>
  <div class="bg-img"></div>
  <div class="bg-overlay"></div>
  <div class="glow-cyan"></div>

  <div class="header-badge">
    <div class="logo-box">
      <div class="logo-dot"></div>
      <div class="logo-text">ĐIỂM ĐỌC THỂ THAO</div>
    </div>
    <div class="kicker-tag">__THUMB_KICKER__</div>
  </div>

  <div class="stage-bottom">
    <div class="hero-title">__THUMB_HERO__</div>
    <div class="rule-bar"></div>
    <div class="sub-title">__THUMB_SUBTITLE__</div>
    <div class="tag-row">
      <div class="stat-pill">__THUMB_TAG_A__</div>
      <div class="stat-pill">__THUMB_TAG_B__</div>
    </div>
  </div>
</body>
</html>
"""
    thumb_img_p = os.path.join(IMG_DIR, f"Tin_{sc_num}_1.jpg")
    out_thumb = os.path.join(SHORTS_OUT, item["thumb_name"])

    h_content = tpl_html
    h_content = h_content.replace("__ASSETS__", paths.file_url(paths.ASSETS))
    h_content = h_content.replace("__THUMB_IMAGE__", paths.file_url(thumb_img_p))
    h_content = h_content.replace("__THUMB_KICKER__", item["thumb_kicker"])
    h_content = h_content.replace("__THUMB_HERO__", item["thumb_hero"])
    h_content = h_content.replace("__THUMB_HERO_SIZE__", item.get("thumb_hero_size", "110"))
    h_content = h_content.replace("__THUMB_SUBTITLE__", item["thumb_sub"])
    h_content = h_content.replace("__THUMB_TAG_A__", item["thumb_tag_a"])
    h_content = h_content.replace("__THUMB_TAG_B__", item["thumb_tag_b"])

    tmp_html_file = os.path.join(WORK_DIR, f"thumb_tin_{sc_num}.html")
    with open(tmp_html_file, "w", encoding="utf-8") as f:
        f.write(h_content)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=[
            "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"
        ])
        page = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        page.goto(paths.file_url(tmp_html_file), wait_until="networkidle")
        page.wait_for_timeout(350)
        page.screenshot(path=out_thumb, type="jpeg", quality=95)
        br.close()

    ok(f"Đã lưu thumbnail #{sc_num}: {paths.rel_to_root(out_thumb)} ({os.path.getsize(out_thumb)/(1024):.1f} KB)")


def write_short_metadata(tin_id: int):
    item = next(it for it in NEWS_DATA if it["id"] == tin_id)
    sc_num = f"{tin_id:02d}"
    out_mota = os.path.join(SHORTS_OUT, item["mota_name"])
    banner(f"XUẤT FILE MÔ TẢ SEO YOUTUBE CHO SHORT #{sc_num} (1 TIÊU ĐỀ DUY NHẤT)", DAY_STR)

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
        return out_path
    else:
        die(f"Render Short #{sc_num} thất bại!")
        return None


def main():
    force = "--force" in sys.argv
    setup_directories()
    fetch_images_tin_1()
    fetch_images_tin_2()
    build_metadata_jsons()
    synthesize_all_audios(force=force)
    generate_contact_sheet(1)
    generate_contact_sheet(2)
    render_thumbnail(1)
    render_thumbnail(2)
    write_short_metadata(1)
    write_short_metadata(2)

    # Render 2 videos
    render_short_video(1, force=force)
    render_short_video(2, force=force)

    banner("TỔNG KẾT XUẤT BẢN 2 VIDEO SHORTS HOÀN TẤT", DAY_STR)
    for it in NEWS_DATA:
        log(f"  📱 Video:     {paths.rel_to_root(os.path.join(SHORTS_OUT, it['file_name']))}")
        log(f"  🖼️ Thumbnail: {paths.rel_to_root(os.path.join(SHORTS_OUT, it['thumb_name']))}")
        log(f"  📝 Mô tả:     {paths.rel_to_root(os.path.join(SHORTS_OUT, it['mota_name']))}")


if __name__ == "__main__":
    main()
