#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_shorts_09_11.py — Sản xuất 2 Video Shorts 9:16 ngày 09.11.2026:
1. Màn rượt đuổi tỷ số 4-4 điên rồ giữa Man Utd và Aston Villa tại Old Trafford
2. Dư chấn đại chiến 4-4: Emery bỏ về, tranh cãi bàn gỡ và tương lai Michael Carrick
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

DAY_STR = "09.11.2026"
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
        "slug": "Short_Man_Utd_Aston_Villa_4_4",
        "file_name": "Short_Man_Utd_Aston_Villa_4_4.mp4",
        "thumb_name": "Short_Man_Utd_Aston_Villa_4_4_thumbnail.jpg",
        "mota_name": "Short_Man_Utd_Aston_Villa_4_4_mota.txt",
        "group": "Nhóm: Ngoại hạng Anh rực lửa",
        "title": "Màn rượt đuổi tỷ số 4-4 điên rồ giữa Man Utd và Aston Villa tại Old Trafford",
        "summary": (
            "Sân Old Trafford rạng sáng nay đã bùng nổ với màn rượt đuổi tỷ số 4-4 điên rồ bậc nhất lịch sử Ngoại hạng Anh "
            "giữa Manchester United và Aston Villa! "
            "Đội khách Aston Villa khiến cầu trường câm lặng khi vươn lên dẫn trước 2-0 chỉ sau bốn phút đầu trận "
            "nhờ các pha lập công chớp nhoáng của Alysson và Nicolas Jackson. "
            "Bị dồn vào chân tường, Quỷ đỏ vùng lên mạnh mẽ để gỡ hòa 2-2 trước giờ nghỉ giải lao "
            "nhờ quả phạt đền của Bruno Fernandes và cú sút hiểm hóc của Youri Tielemans. "
            "Kịch tính đẩy lên đỉnh điểm trong hiệp hai khi Aston Villa một lần nữa vượt lên dẫn 4-2 "
            "sau quả phạt đền của John McGinn và pha lập công của Leon Goretzka. "
            "Tưởng chừng chiến thắng đã nằm chắc trong tay đội khách, những phút bù giờ nghẹt thở đã chứng kiến điều kỳ diệu "
            "khi Joshua Zirkzee rút ngắn cách biệt 3-4 ở phút 90+2. "
            "Đến phút 90+6, hậu vệ vào sân thay người Patrick Dorgu bật cao đánh đầu dũng mãnh tung nóc lưới sau quả phạt góc, "
            "ấn định tỷ số hòa 4-4 không tưởng cho Manchester United!"
        ),
        "digest_line": "Màn rượt đuổi 8 bàn thắng điên rồ giữa Man Utd và Aston Villa khép lại với tỷ số 4-4 nhờ bàn gỡ phút 90+6 của Dorgu.",
        "digest_title": "Màn rượt đuổi tỷ số 4-4 điên rồ giữa Man Utd và Aston Villa tại Old Trafford",
        "source": "VnExpress / NBC Sports",
        "news_source": "VnExpress / NBC Sports",
        "thumb_kicker": "NGOẠI HẠNG ANH · ĐẠI CHIẾN ĐIÊN RỒ",
        "thumb_hero": "RƯỢT ĐUỔI 4-4!",
        "thumb_hero_size": "115",
        "thumb_sub": "MAN UTD HÒA ĐIÊN RỒ ASTON VILLA · DORGU GỠ HÒA PHÚT 90+6",
        "thumb_tag_a": "OLD TRAFFORD VỠ ÒA",
        "thumb_tag_b": "BÙ GIỜ ĐIÊN RỒ",
        "seo_title": "Màn rượt đuổi tỷ số 4-4 điên rồ giữa Man Utd và Aston Villa tại Old Trafford #Shorts",
        "seo_desc": (
            "Trận cầu điên rồ nhất mùa giải Ngoại hạng Anh 2026/27 đã diễn ra tại chảo lửa Old Trafford rạng sáng 9/11/2026, "
            "khi Manchester United và Aston Villa cống hiến cơn mưa 8 bàn thắng không tưởng!\n\n"
            "Bị dẫn trước 0-2 chỉ sau 4 phút bởi Alysson và Nicolas Jackson, MU gỡ hòa 2-2 nhờ Bruno Fernandes và Youri Tielemans. "
            "Đầu hiệp hai, John McGinn và Leon Goretzka tái lập cách biệt hai bàn đưa Villa dẫn 4-2.\n\n"
            "Thế nhưng trong thời gian bù giờ nghẹt thở, Joshua Zirkzee nhen nhóm hy vọng ở phút 90+2, "
            "trước khi Patrick Dorgu đóng vai người hùng với cú đánh đầu sấm sét phút 90+6 giật lại 1 điểm cảm xúc cho Quỷ đỏ!"
        ),
        "seo_tags": "#Shorts #DiemDoc #ManUtd #AstonVilla #OldTrafford #BrunoFernandes #Dorgu #Zirkzee #Emery #Carrick #NgoaiHangAnh #TinBongDa"
    },
    {
        "id": 2,
        "art_id": "art_02",
        "slug": "Short_Ben_Le_Man_Utd_Aston_Villa_Carrick",
        "file_name": "Short_Ben_Le_Man_Utd_Aston_Villa_Carrick.mp4",
        "thumb_name": "Short_Ben_Le_Man_Utd_Aston_Villa_Carrick_thumbnail.jpg",
        "mota_name": "Short_Ben_Le_Man_Utd_Aston_Villa_Carrick_mota.txt",
        "group": "Nhóm: Hậu trường & Tranh cãi",
        "title": "Dư chấn đại chiến 4-4: Emery bỏ về, tranh cãi bàn gỡ và tương lai Michael Carrick",
        "summary": (
            "Trận hòa điên rồ 4-4 tại Old Trafford đã để lại những dư chấn dữ dội cùng làn sóng tranh cãi gay gắt từ cả hai câu lạc bộ! "
            "Quá tức giận vì đánh rơi chiến thắng ở giây cuối cùng, huấn luyện viên Unai Emery đã lủi thủi đi thẳng vào đường hầm "
            "ở phút 96 khi trận đấu chưa kết thúc và tuyên bố cay đắng coi trận hòa này như một thất bại! "
            "Phía Aston Villa kịch liệt phản đối bàn gỡ hòa 4-4, tố cáo thủ môn Senne Lammens của Man Utd dâng cao đã va chạm trái phép "
            "làm mất đà thủ thành Zion Suzuki trong vòng cấm, dù VAR vẫn giữ nguyên quyết định công nhận bàn thắng. "
            "Trong phòng họp báo rực lửa sau trận, huấn luyện viên Michael Carrick đối mặt với áp lực ngàn cân "
            "khi các phóng viên liên tục chất vấn về tương lai và khả năng từ chức. "
            "Tuy nhiên, Carrick đã kiên quyết bác bỏ tin đồn, khẳng định sẽ không từ chức và tự tin tiếp tục dẫn dắt đội bóng "
            "sau đợt tập trung đội tuyển quốc gia. "
            "Dù giật lại 1 điểm hú vía, Manchester United vẫn dậm chân ở vị trí thứ 18 trong nhóm cầm đèn đỏ với chỉ 8 điểm sau 10 vòng, "
            "đẩy phòng thay đồ Old Trafford bước vào chuỗi ngày giông bão nhất mùa giải!"
        ),
        "digest_line": "Hậu đại chiến 4-4: Emery bực tức bỏ vào đường hầm, tranh cãi va chạm thủ môn Suzuki và Carrick tuyên bố không từ chức.",
        "digest_title": "Dư chấn đại chiến 4-4: Emery bỏ về, tranh cãi bàn gỡ và tương lai Michael Carrick",
        "source": "VnExpress / Sky Sports",
        "news_source": "VnExpress / Sky Sports",
        "thumb_kicker": "HẬU ĐẠI CHIẾN 4-4 · BÃO DƯ LUẬN",
        "thumb_hero": "EMERY BỎ ĐƯỜNG HẦM!",
        "thumb_hero_size": "100",
        "thumb_sub": "TRANH CÃI BÀN GỠ 4-4 · CARRICK TUYÊN BỐ KHÔNG TỪ CHỨC",
        "thumb_tag_a": "SUZUKI BỊ PHẠM LỖI?",
        "thumb_tag_b": "MU VẪN ĐỨNG THỨ 18",
        "seo_title": "Dư chấn đại chiến 4-4: Emery bỏ về, tranh cãi bàn gỡ và tương lai Carrick #Shorts",
        "seo_desc": (
            "Dư chấn sau trận cầu điên rồ Manchester United 4-4 Aston Villa đang bùng nổ dữ dội!\n\n"
            "HLV Unai Emery không giấu nổi sự giận dữ khi lủi thủi đi thẳng vào đường hầm Old Trafford ở phút 96 mà không thèm bắt tay đồng nghiệp, "
            "trong khi ban lãnh đạo Aston Villa bức xúc cáo buộc thủ môn Lammens đã phạm lỗi với Zion Suzuki ở bàn thua quyết định.\n\n"
            "Ở chiều ngược lại, HLV Michael Carrick cứng rắn tuyên bố kiên quyết không từ chức bất chấp áp lực dồn dập từ truyền thông. "
            "Dù thoát thua nghẹt thở, vị trí thứ 18 nằm trong nhóm xuống hạng vẫn đang là cơn ác mộng bủa vây Quỷ đỏ!"
        ),
        "seo_tags": "#Shorts #DiemDoc #ManUtd #AstonVilla #Emery #Carrick #ZionSuzuki #Lammens #VAR #PremierLeague #NgoaiHangAnh #TinBongDa"
    }
]

IMAGE_QUERIES_TIN_1 = [
    ("Tin_01_1.jpg", "Manchester United vs Aston Villa Old Trafford match 2026", "PREMIER LEAGUE"),
    ("Tin_01_2.jpg", "Manchester United vs Aston Villa action scoreboard Old Trafford 2026", "ACTION IMAGES / REUTERS"),
    ("Tin_01_3.jpg", "Aston Villa goal celebration Old Trafford Alysson 2026", "AP PHOTO"),
    ("Tin_01_4.jpg", "Nicolas Jackson Aston Villa goal celebration 2026", "REUTERS"),
    ("Tin_01_5.jpg", "Bruno Fernandes penalty goal Manchester United 2026", "GETTY IMAGES / PREMIER LEAGUE"),
    ("Tin_01_6.jpg", "Youri Tielemans goal celebration Manchester United 2026", "ACTION IMAGES / REUTERS"),
    ("Tin_01_7.jpg", "John McGinn Aston Villa penalty goal celebration 2026", "AP PHOTO"),
    ("Tin_01_8.jpg", "Leon Goretzka Aston Villa goal celebration 2026", "THE GUARDIAN / REUTERS"),
    ("Tin_01_9.jpg", "Joshua Zirkzee goal Manchester United Old Trafford 2026", "ACTION IMAGES"),
    ("Tin_01_10.jpg", "Joshua Zirkzee celebration Manchester United 2026", "GETTY IMAGES"),
    ("Tin_01_11.jpg", "Patrick Dorgu header goal celebration Manchester United 2026", "AP PHOTO"),
    ("Tin_01_12.jpg", "Manchester United players celebrating 4-4 draw Old Trafford 2026", "PREMIER LEAGUE"),
]

IMAGE_QUERIES_TIN_2 = [
    ("Tin_02_1.jpg", "Manchester United Aston Villa post match tension players 2026", "PREMIER LEAGUE"),
    ("Tin_02_2.jpg", "Unai Emery Michael Carrick touchline Premier League 2026", "ACTION IMAGES / REUTERS"),
    ("Tin_02_3.jpg", "Unai Emery walking off tunnel disappointed Aston Villa 2026", "AP PHOTO"),
    ("Tin_02_4.jpg", "Unai Emery frustrated angry press conference Aston Villa", "REUTERS"),
    ("Tin_02_5.jpg", "Zion Suzuki Aston Villa goalkeeper incident goal 2026", "GETTY IMAGES / PREMIER LEAGUE"),
    ("Tin_02_6.jpg", "Premier League VAR review referee screen monitor 2026", "ACTION IMAGES / REUTERS"),
    ("Tin_02_7.jpg", "Michael Carrick post match press conference Manchester United 2026", "AP PHOTO"),
    ("Tin_02_8.jpg", "Michael Carrick press conference microphone serious face", "SKY SPORTS"),
    ("Tin_02_9.jpg", "Michael Carrick determined portrait Manchester United", "ACTION IMAGES"),
    ("Tin_02_10.jpg", "Manchester United training Carrington ground 2026", "MAN UTD / GETTY IMAGES"),
    ("Tin_02_11.jpg", "Premier League table standings relegation zone 2026", "VNEXPRESS / OPTA"),
    ("Tin_02_12.jpg", "Old Trafford stadium Manchester United rain fans gloomy", "PREMIER LEAGUE"),
]


def setup_directories():
    step("Khởi tạo cấu trúc thư mục outputs/Orther/09.11.2026...")
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


def fetch_images_for_list(query_list: List[Tuple[str, str, str]], label: str):
    banner(f"THU THẬP VÀ CHUẨN HÓA 12 ẢNH CHO {label}", DAY_STR)
    with DDGS() as ddgs:
        for fname, query, _ in query_list:
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
                parts = query.split()
                fallback_q = parts[0] + " " + parts[1] + " football match 2026"
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
                prefix = fname.split("_")[0] + "_" + fname.split("_")[1]
                first_img = os.path.join(IMG_DIR, f"{prefix}_1.jpg")
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
    plan_records.append({"scene_id": 1, "type": "title", "index": 1, "file_name": "Tin_01_1.jpg", "credit": "PREMIER LEAGUE", "description": "Man Utd vs Aston Villa 4-4 Old Trafford"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 1, "file_name": "Tin_01_1.jpg", "credit": "PREMIER LEAGUE", "description": "Old Trafford rạng sáng nay bùng nổ với màn rượt đuổi 4-4"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 1, "file_name": "Tin_01_2.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Toàn cảnh sân Old Trafford và bảng tỷ số 4-4 rực lửa"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 2, "file_name": "Tin_01_3.jpg", "credit": "AP PHOTO", "description": "Aston Villa dẫn trước 2-0 chỉ sau 4 phút"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 2, "file_name": "Tin_01_4.jpg", "credit": "REUTERS", "description": "Nicolas Jackson ăn mừng bàn nhân đôi cách biệt"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 3, "file_name": "Tin_01_5.jpg", "credit": "GETTY IMAGES / PREMIER LEAGUE", "description": "Bruno Fernandes sút phạt đền rút ngắn 1-2"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 3, "file_name": "Tin_01_6.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Youri Tielemans sút hiểm hóc gỡ hòa 2-2"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 4, "file_name": "Tin_01_7.jpg", "credit": "AP PHOTO", "description": "John McGinn sút phạt đền nâng tỷ số lên 3-2 cho Villa"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 4, "file_name": "Tin_01_8.jpg", "credit": "THE GUARDIAN / REUTERS", "description": "Leon Goretzka nới rộng cách biệt lên 4-2"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 5, "file_name": "Tin_01_9.jpg", "credit": "ACTION IMAGES", "description": "Joshua Zirkzee rút ngắn 3-4 ở phút 90+2"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 5, "file_name": "Tin_01_10.jpg", "credit": "GETTY IMAGES", "description": "Zirkzee ăn mừng cùng CĐV Man Utd nhen nhóm hy vọng"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 6, "file_name": "Tin_01_11.jpg", "credit": "AP PHOTO", "description": "Patrick Dorgu bật cao đánh đầu gỡ hòa 4-4 phút 90+6"})
    plan_records.append({"scene_id": 1, "type": "sentence", "index": 6, "file_name": "Tin_01_12.jpg", "credit": "PREMIER LEAGUE", "description": "Old Trafford vỡ òa với bàn thắng phút cuối của Dorgu"})

    # Tin 2: 6 sentences x 2 images + 1 title
    plan_records.append({"scene_id": 2, "type": "title", "index": 1, "file_name": "Tin_02_1.jpg", "credit": "PREMIER LEAGUE", "description": "Dư chấn đại chiến 4-4: Emery và Carrick"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 1, "file_name": "Tin_02_1.jpg", "credit": "PREMIER LEAGUE", "description": "Trận hòa 4-4 để lại những dư chấn dữ dội và tranh cãi"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 1, "file_name": "Tin_02_2.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Căng thẳng ngoài đường pitch giữa ban huấn luyện hai đội"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 2, "file_name": "Tin_02_3.jpg", "credit": "AP PHOTO", "description": "Unai Emery bực tức bỏ thẳng vào đường hầm phút 96"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 2, "file_name": "Tin_02_4.jpg", "credit": "REUTERS", "description": "Emery tuyên bố coi trận hòa 4-4 như một thất bại"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 3, "file_name": "Tin_02_5.jpg", "credit": "GETTY IMAGES / PREMIER LEAGUE", "description": "Aston Villa tố cáo Lammens va chạm với thủ môn Suzuki"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 3, "file_name": "Tin_02_6.jpg", "credit": "ACTION IMAGES / REUTERS", "description": "Màn hình VAR kiểm tra và công nhận bàn thắng hợp lệ"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 4, "file_name": "Tin_02_7.jpg", "credit": "AP PHOTO", "description": "Michael Carrick đối mặt với áp lực ngàn cân trong phòng họp báo"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 4, "file_name": "Tin_02_8.jpg", "credit": "SKY SPORTS", "description": "Các phóng viên liên tục chất vấn Carrick về khả năng từ chức"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 5, "file_name": "Tin_02_9.jpg", "credit": "ACTION IMAGES", "description": "Carrick kiên quyết khẳng định sẽ không từ chức"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 5, "file_name": "Tin_02_10.jpg", "credit": "MAN UTD / GETTY IMAGES", "description": "Carrick tự tin tiếp tục dẫn dắt MU sau quãng nghỉ quốc tế"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 6, "file_name": "Tin_02_11.jpg", "credit": "VNEXPRESS / OPTA", "description": "Man Utd vẫn dậm chân ở vị trí thứ 18 nhóm cầm đèn đỏ"})
    plan_records.append({"scene_id": 2, "type": "sentence", "index": 6, "file_name": "Tin_02_12.jpg", "credit": "PREMIER LEAGUE", "description": "Phòng thay đồ Old Trafford bước vào chuỗi ngày giông bão"})

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
    topic = "MAN UTD 4-4 ASTON VILLA ĐẠI CHIẾN ĐIÊN RỒ" if tin_id == 1 else "DƯ CHẤN HẬU ĐẠI CHIẾN: EMERY & CARRICK"
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
    fetch_images_for_list(IMAGE_QUERIES_TIN_1, "TIN 1 (MAN UTD 4-4 ASTON VILLA)")
    fetch_images_for_list(IMAGE_QUERIES_TIN_2, "TIN 2 (DƯ CHẤN HẬU ĐẠI CHIẾN: EMERY & CARRICK)")
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
