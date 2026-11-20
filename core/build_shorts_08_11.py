#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_shorts_08_11.py — Sản xuất 2 Video Shorts 9:16 ngày 08.11.2026:
1. Nottingham Forest thắng sốc Man City 3-1
2. MU rơi xuống nhóm cầm đèn đỏ Ngoại hạng Anh sau chiến thắng của Nottingham Forest
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
from diemdoc.audio import apply_voice_standard
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from m8_news_bridge import export_bridge_project
from renderer import render_html_engine
from vieneu import Vieneu

DAY_STR = "08.11.2026"
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
        "slug": "Short_Nottingham_Thang_Man_City_3_1",
        "file_name": "Short_Nottingham_Thang_Man_City_3_1.mp4",
        "thumb_name": "Short_Nottingham_Thang_Man_City_3_1_thumbnail.jpg",
        "mota_name": "Short_Nottingham_Thang_Man_City_3_1_mota.txt",
        "group": "Nhóm: Địa chấn Ngoại hạng Anh",
        "title": "Nottingham Forest thắng sốc Man City 3-1: Địa chấn rung chuyển Ngoại hạng Anh",
        "summary": (
            "Chảo lửa City Ground rạng sáng nay đã chứng kiến cơn địa chấn lớn nhất vòng 10 Ngoại hạng Anh, "
            "khi Nottingham Forest xuất sắc quật ngã gã khổng lồ Manchester City với tỷ số 3-1! "
            "Ngay phút thứ 6, trung vệ Josko Gvardiol mắc sai lầm tai hại khi chuyền bóng thẳng vào chân đối thủ, "
            "tạo điều kiện cho Jair Cunha thoát xuống dứt điểm chìm mở tỷ số 1-0 cho Nottingham Forest. "
            "Cơn ác mộng của Man City tiếp tục ở phút 18 khi cựu tiền đạo của chính họ là Liam Delap thực hiện pha độc diễn "
            "dũng mãnh từ giữa sân rồi tung cú sút sấm sét nhân đôi cách biệt. "
            "Dù tân binh Rayan Cherki thắp lại hy vọng cho Man City bằng pha bắt volley tuyệt đẹp ở phút 52 rút ngắn xuống 1-2, "
            "bản lĩnh phòng ngự kiên cường của đội chủ nhà đã dập tắt mọi nỗ lực của các vị khách. "
            "Đến phút 73, từ pha chọc khe thông minh của Morgan Gibbs-White, lại là Liam Delap bứt tốc đánh bại thủ môn Ederson "
            "để hoàn tất cú đúp ngoạn mục, ấn định thắng lợi lịch sử 3-1! "
            "Thất bại cay đắng thứ ba liên tiếp khiến Man City bị Arsenal bỏ xa tới 6 điểm, "
            "trong khi 3 điểm quý như vàng giúp Nottingham Forest tạm thoát khỏi nhóm nguy hiểm để leo lên vị trí thứ 16!"
        ),
        "digest_line": "Nottingham Forest gây sốc lớn khi đè bẹp Man City 3-1 tại City Ground nhờ cú đúp của Liam Delap.",
        "digest_title": "Nottingham Forest thắng sốc Man City 3-1: Địa chấn rung chuyển Ngoại hạng Anh",
        "source": "VnExpress / Bóng Đá Plus",
        "news_source": "VnExpress / Bóng Đá Plus",
        "thumb_kicker": "NGOẠI HẠNG ANH · VÒNG 10",
        "thumb_hero": "ĐỊA CHẤN 3-1!",
        "thumb_hero_size": "115",
        "thumb_sub": "NOTTINGHAM FOREST ĐÈ BẸP MAN CITY · CÚ ĐÚP CỦA LIAM DELAP",
        "thumb_tag_a": "CITY GROUND BÙNG NỔ",
        "thumb_tag_b": "DELAP HẠ ĐỘI CŨ",
        "seo_title": "Nottingham Forest hạ gục Man City 3-1: Cơn địa chấn rung chuyển Ngoại hạng Anh #Shorts",
        "seo_desc": (
            "Chảo lửa City Ground rạng sáng 8/11/2026 đã chứng kiến một trong những bất ngờ lớn nhất mùa giải Ngoại hạng Anh 2026/27, "
            "khi Nottingham Forest đánh bại Manchester City với tỷ số thuyết phục 3-1!\n\n"
            "Sai lầm chết người của Josko Gvardiol ở phút thứ 6 đã mở toang cánh cửa để Jair Cunha mở tỷ số. "
            "Sau đó, người cũ của Man City là Liam Delap đã có ngày thi đấu thăng hoa tột bậc với cú đúp bàn thắng ngoạn mục ở các phút 18 và 73, "
            "biến pha bắt volley rút ngắn tỷ số của Rayan Cherki trở thành vô nghĩa.\n\n"
            "Trận thua thứ ba liên tiếp tại giải Ngoại hạng Anh khiến Man City bị đội đầu bảng Arsenal nới rộng khoảng cách lên 6 điểm, "
            "trong khi thầy trò Nottingham Forest giành 3 điểm vô giá để tạm thời thoát khỏi nhóm nguy hiểm!"
        ),
        "seo_tags": "#Shorts #DiemDoc #NottinghamForest #ManCity #LiamDelap #Gvardiol #Cherki #NgoaiHangAnh #PremierLeague #TinBongDa"
    },
    {
        "id": 2,
        "art_id": "art_02",
        "slug": "Short_Man_Utd_Roi_Xuong_Khom_Nguy_Hiem",
        "file_name": "Short_Man_Utd_Roi_Xuong_Khom_Nguy_Hiem.mp4",
        "thumb_name": "Short_Man_Utd_Roi_Xuong_Khom_Nguy_Hiem_thumbnail.jpg",
        "mota_name": "Short_Man_Utd_Roi_Xuong_Khom_Nguy_Hiem_mota.txt",
        "group": "Nhóm: Ngoại hạng Anh khủng hoảng",
        "title": "MU rơi xuống nhóm cầm đèn đỏ Ngoại hạng Anh sau chiến thắng của Nottingham Forest",
        "summary": (
            "Chiến thắng địa chấn của Nottingham Forest trước Man City rạng sáng nay đã tạo nên một cơn chấn động dây chuyền, "
            "trực tiếp đẩy Manchester United chìm sâu vào nhóm cầm đèn đỏ của giải Ngoại hạng Anh! "
            "Việc Nottingham Forest bỏ túi ba điểm để vươn lên 9 điểm và leo lên vị trí thứ 16 đã gián tiếp đẩy Quỷ đỏ tụt xuống vị trí thứ 18, "
            "chính thức rơi vào nhóm ba đội có nguy cơ rớt hạng! "
            "Sau chín vòng đấu, đoàn quân của huấn luyện viên Michael Carrick mới chỉ giành được vỏn vẹn 7 điểm với hiệu số âm 5, "
            "chạm mốc khởi đầu tồi tệ bậc nhất trong lịch sử hiện đại của câu lạc bộ. "
            "Nghịch lý cay đắng nhất là MU đang dẫn đầu toàn bộ giải đấu với 167 cú dứt điểm, "
            "nhưng hàng công lại chỉ ghi được đúng 10 bàn thắng do sự vô duyên khó hiểu trước khung thành đối phương. "
            "Áp lực ngàn cân đang đè nặng lên vai Michael Carrick trước chuyến làm khách đầy giông bão tới sân của Aston Villa ở trận đấu muộn vòng 10. "
            "Nếu không thể giành trọn ba điểm để tự giải cứu mình, Manchester United hoàn toàn có thể lún sâu hơn vào cuộc khủng hoảng tồi tệ chưa từng thấy tại Old Trafford!"
        ),
        "digest_line": "Chiến thắng của Nottingham Forest đẩy MU chính thức rơi xuống vị trí thứ 18, lọt vào nhóm xuống hạng.",
        "digest_title": "MU rơi xuống nhóm cầm đèn đỏ Ngoại hạng Anh sau chiến thắng của Nottingham Forest",
        "source": "VnExpress / Sky Sports",
        "news_source": "VnExpress / Sky Sports",
        "thumb_kicker": "NGOẠI HẠNG ANH · BÁO ĐỘNG ĐỎ",
        "thumb_hero": "MU RƠI XUỐNG THỨ 18!",
        "thumb_hero_size": "100",
        "thumb_sub": "NOTTINGHAM THẮNG ĐẨY QUỶ ĐỎ CHÍNH THỨC RƠI VÀO NHÓM CẦM ĐÈN ĐỎ",
        "thumb_tag_a": "VỊ TRÍ THỨ 18",
        "thumb_tag_b": "CHỈ 7 ĐIỂM SAU 9 TRẬN",
        "seo_title": "MU chính thức rơi vào nhóm cầm đèn đỏ Ngoại hạng Anh sau chiến thắng của Nottingham #Shorts",
        "seo_desc": (
            "Cơn ác mộng tại Old Trafford đang trở nên tồi tệ hơn bao giờ hết!\n\n"
            "Chiến thắng 3-1 bất ngờ của Nottingham Forest trước Man City rạng sáng 8/11/2026 đã gián tiếp đẩy Manchester United "
            "tụt xuống vị trí thứ 18 trên bảng xếp hạng Ngoại hạng Anh, chính thức rơi vào nhóm ba đội cầm đèn đỏ có nguy cơ xuống hạng.\n\n"
            "Với vỏn vẹn 7 điểm sau 9 trận đã đấu, chiếc ghế huấn luyện viên trưởng của Michael Carrick đang lung lay dữ dội. "
            "Nghịch lý lớn nhất là Quỷ đỏ dẫn đầu giải với 167 pha dứt điểm nhưng chỉ có được 10 bàn thắng do sự yếu kém khó tin của hàng tiền đạo.\n\n"
            "Liệu Man Utd có thể tự giải cứu mình trong chuyến hành quân đầy hiểm nguy tới sân của Aston Villa?"
        ),
        "seo_tags": "#Shorts #DiemDoc #ManUtd #ManchesterUnited #MU #Carrick #PremierLeague #NottinghamForest #NgoaiHangAnh #TinBongDa"
    }
]

IMAGE_QUERIES_TIN_1 = [
    ("Tin_01_1.jpg", "Nottingham Forest vs Manchester City City Ground Premier League 2026", "PREMIER LEAGUE"),
    ("Tin_01_2.jpg", "Nottingham Forest City Ground stadium atmosphere fans 2026", "ACTION IMAGES / REUTERS"),
    ("Tin_01_3.jpg", "Josko Gvardiol Manchester City mistake disappointed 2026", "AP PHOTO"),
    ("Tin_01_4.jpg", "Jair Cunha Nottingham Forest goal celebration 2026", "REUTERS"),
    ("Tin_01_5.jpg", "Liam Delap Nottingham Forest goal run shot 2026", "GETTY IMAGES / PREMIER LEAGUE"),
    ("Tin_01_6.jpg", "Liam Delap goal celebration Nottingham Forest 2026", "ACTION IMAGES / REUTERS"),
    ("Tin_01_7.jpg", "Rayan Cherki Manchester City goal celebration volley 2026", "AP PHOTO"),
    ("Tin_01_8.jpg", "Nottingham Forest tackle defence Manchester City 2026", "THE GUARDIAN / REUTERS"),
    ("Tin_01_9.jpg", "Morgan Gibbs-White Nottingham Forest pass assist 2026", "ACTION IMAGES"),
    ("Tin_01_10.jpg", "Liam Delap second goal Nottingham Forest vs Man City Ederson", "GETTY IMAGES"),
    ("Tin_01_11.jpg", "Manchester City players disappointed Erling Haaland defeat", "AP PHOTO"),
    ("Tin_01_12.jpg", "Nottingham Forest players celebrating victory 3-1 City Ground", "PREMIER LEAGUE"),
]

IMAGE_CREDITS_TIN_2 = {
    "Tin_02_1.jpg": "PREMIER LEAGUE",
    "Tin_02_2.jpg": "AP PHOTO",
    "Tin_02_3.jpg": "VNEXPRESS / OPTA",
    "Tin_02_4.jpg": "AP PHOTO",
    "Tin_02_5.jpg": "AP PHOTO",
    "Tin_02_6.jpg": "ACTION IMAGES / REUTERS",
    "Tin_02_7.jpg": "AP PHOTO",
    "Tin_02_8.jpg": "MAN UTD / GETTY IMAGES",
    "Tin_02_9.jpg": "VNEXPRESS / SKY SPORTS",
    "Tin_02_10.jpg": "AP PHOTO",
    "Tin_02_11.jpg": "PREMIER LEAGUE",
    "Tin_02_12.jpg": "VNEXPRESS",
}


def setup_directories():
    step("Khởi tạo cấu trúc thư mục outputs/Orther/08.11.2026...")
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


def fetch_tin_1_images():
    banner("THU THẬP VÀ CHUẨN HÓA 12 ẢNH CHO TIN 1 (NOTTINGHAM FOREST 3-1 MAN CITY)", DAY_STR)
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
                # Fallback query
                fallback_q = query.split()[0] + " " + query.split()[1] + " football match 2026"
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
                warn(f"  -> Không tải được {fname}, sẽ dùng ảnh dự phòng.")
                # Nếu thiếu ảnh, copy từ ảnh đầu tiên
                first_img = os.path.join(IMG_DIR, "Tin_01_1.jpg")
                if os.path.exists(first_img):
                    shutil.copy2(first_img, target_path)


def copy_tin_2_images():
    banner("NẠP VÀ ĐỒNG BỘ 12 ẢNH CHO TIN 2 (MANCHESTER UNITED KHỦNG HOẢNG)", DAY_STR)
    src_07 = os.path.join(paths.OUTPUTS, "Orther", "07.11.2026", "images")
    for fname in IMAGE_CREDITS_TIN_2.keys():
        dest_p = os.path.join(IMG_DIR, fname)
        src_p = os.path.join(src_07, fname)
        if not os.path.exists(dest_p) or os.path.getsize(dest_p) < 10_000:
            if os.path.exists(src_p):
                shutil.copy2(src_p, dest_p)
                ok(f"  [COPY 07.11] {fname} ({os.path.getsize(dest_p)/(1024):.1f} KB)")
            else:
                warn(f"Không tìm thấy nguồn: {src_p}")
        else:
            ok(f"  [ĐÃ CÓ] {fname}")


def build_metadata_jsons():
    banner("XUẤT CÁC FILE HỢP ĐỒNG DỮ LIỆU: THETHAO.JSON, IMAGE_CREDITS.JSON, IMAGE_PLAN.JSON", DAY_STR)

    # 1. image_credits.json
    credits_map = {}
    for fn, _, cr in IMAGE_QUERIES_TIN_1:
        credits_map[fn] = cr
    for fn, cr in IMAGE_CREDITS_TIN_2.items():
        credits_map[fn] = cr

    with open(os.path.join(DAY_DIR, "image_credits.json"), "w", encoding="utf-8") as f:
        json.dump(credits_map, f, ensure_ascii=False, indent=2)
    ok(f"Đã lưu: {paths.rel_to_root(os.path.join(DAY_DIR, 'image_credits.json'))}")

    # 2. image_plan.json
    plan_records = []
    # Tin 1: 6 sentences x 2 images + 1 title
    plan_records.append({"scene_id": 1, "type": "title", "index": 1, "file_name": "Tin_01_1.jpg", "credit": "PREMIER LEAGUE", "description": "Nottingham Forest vs Manchester City 3-1"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 1, "file_name": "Tin_01_1.jpg", "credit": "PREMIER LEAGUE", "description": "Chảo lửa City Ground chứng kiến địa chấn lớn nhất vòng 10"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 1, "file_name": "Tin_01_2.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Toàn cảnh sân City Ground và CĐV Nottingham bùng nổ"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 2, "file_name": "Tin_01_3.jpg", "credit": "AP PHOTO", "description": "Josko Gvardiol mắc sai lầm tai hại chuyền bóng hỏng"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 2, "file_name": "Tin_01_4.jpg", "credit": "REUTERS", "description": "Jair Cunha mở tỷ số 1-0 cho Nottingham Forest"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 3, "file_name": "Tin_01_5.jpg", "credit": "GETTY IMAGES / PREMIER LEAGUE", "description": "Liam Delap độc diễn dũng mãnh từ giữa sân"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 3, "file_name": "Tin_01_6.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Liam Delap sút sấm sét nhân đôi cách biệt 2-0"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 4, "file_name": "Tin_01_7.jpg", "credit": "AP PHOTO", "description": "Rayan Cherki bắt volley rút ngắn tỷ số 1-2 cho Man City"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 4, "file_name": "Tin_01_8.jpg", "credit": "THE GUARDIAN / REUTERS", "description": "Hàng thủ Nottingham Forest kiên cường lăn xả cản phá"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 5, "file_name": "Tin_01_9.jpg", "credit": "ACTION IMAGES", "description": "Morgan Gibbs-White chọc khe thông minh phản công"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 5, "file_name": "Tin_01_10.jpg", "credit": "GETTY IMAGES", "description": "Liam Delap hoàn tất cú đúp ấn định chiến thắng 3-1"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 6, "file_name": "Tin_01_11.jpg", "credit": "AP PHOTO", "description": "Man City nhận trận thua thứ 3 liên tiếp bị Arsenal bỏ xa"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 6, "file_name": "Tin_01_12.jpg", "credit": "PREMIER LEAGUE", "description": "Nottingham Forest vươn lên thứ 16 thoát nhóm nguy hiểm"})

    # Tin 2: 6 sentences x 2 images + 1 title
    plan_records.append({"scene_id": 2, "type": "title", "index": 1, "file_name": "Tin_02_1.jpg", "credit": "PREMIER LEAGUE", "description": "MU rơi xuống nhóm cầm đèn đỏ Ngoại hạng Anh"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 1, "file_name": "Tin_02_1.jpg", "credit": "PREMIER LEAGUE", "description": "Hiệu ứng Nottingham thắng Man City đẩy MU xuống đáy"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 1, "file_name": "Tin_02_2.jpg", "credit": "AP PHOTO", "description": "Cầu thủ Man Utd thất vọng chìm sâu vào khủng hoảng"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 2, "file_name": "Tin_02_3.jpg", "credit": "VNEXPRESS / OPTA", "description": "Bảng xếp hạng Ngoại hạng Anh vòng 10 MU rơi xuống thứ 18"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 2, "file_name": "Tin_02_4.jpg", "credit": "AP PHOTO", "description": "Chiếc ghế của Michael Carrick chịu sức ép ngàn cân"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 3, "file_name": "Tin_02_5.jpg", "credit": "AP PHOTO", "description": "MU chỉ có 7 điểm sau 9 vòng đấu khởi đầu tồi tệ nhất"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 3, "file_name": "Tin_02_6.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Khủng hoảng phòng thay đồ và phong độ bết bát của Quỷ đỏ"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 4, "file_name": "Tin_02_7.jpg", "credit": "AP PHOTO", "description": "Nghịch lý 167 cú sút dẫn đầu giải nhưng chỉ có 10 bàn"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 4, "file_name": "Tin_02_8.jpg", "credit": "MAN UTD / GETTY IMAGES", "description": "Bruno Fernandes và hàng công vô duyên trước khung thành"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 5, "file_name": "Tin_02_9.jpg", "credit": "VNEXPRESS / SKY SPORTS", "description": "Thách thức sinh tử trước chuyến làm khách Aston Villa"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 5, "file_name": "Tin_02_10.jpg", "credit": "AP PHOTO", "description": "Buổi tập căng như dây đàn tại trung tâm huấn luyện Carrington"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 6, "file_name": "Tin_02_11.jpg", "credit": "PREMIER LEAGUE", "description": "Nguy cơ trượt dài vào thảm họa xuống hạng lịch sử"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 6, "file_name": "Tin_02_12.jpg", "credit": "VNEXPRESS", "description": "Old Trafford u ám và nỗi thất vọng cùng cực của người hâm mộ"})

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


def synthesize_audio_for_text(model: Vieneu, text: str, voice: str = "Minh Quân Pro", speed: float = 1.12, pitch: float = 0.93) -> AudioSegment:
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
        seg, _ = render_chunk_vitts(model, c_text, voice, temperature=0.6, speed=speed, pitch=pitch, cache_dir=CACHE_DIR, use_cache=True)
        seg = trim_segment_silence(seg)
        combined += seg
    return combined


def synthesize_all_audios(force: bool = False):
    banner("SINH GIỌNG ĐỌC VITTS V3TURBO MINH QUÂN PRO MẪU 15 CHO CẢ 2 BẢN TIN", DAY_STR)
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
        seg_title = synthesize_audio_for_text(model, item["title"])
        seg_title = seg_title.set_frame_rate(44100).set_channels(2)
        seg_title.export(target_title, format="wav")
        ok(f"  -> Đã lưu audio tiêu đề: {paths.rel_to_root(target_title)} ({len(seg_title)/1000:.2f}s)")

        step(f"Đang đọc Nội dung chi tiết Tin {sc_num} (~{len(item['summary'].split())} từ)...")
        seg_summary = synthesize_audio_for_text(model, item["summary"])

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
    topic = "NOTTINGHAM FOREST 3-1 MAN CITY" if tin_id == 1 else "MANCHESTER UNITED KHỦNG HOẢNG THỨ 18"
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
    fetch_tin_1_images()
    copy_tin_2_images()
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
