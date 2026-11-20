#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_10_ky_luc_images.py — Thu thập ảnh tư liệu & sinh Contact Sheet QA
cho dự án '10 kỷ lục bóng đá gần như không thể phá' (Điểm Đọc)

Quy trình chuẩn:
  1. 108 slots ảnh phân bổ đều cho 12 scenes (10 kỷ lục + Intro + Outro).
  2. Tìm kiếm qua DDGS (size=Large, layout=Wide).
  3. Lọc sạch:
     - Chặn miền stock dính watermark (Alamy, Getty, Shutterstock, iStock, Dreamstime...)
     - Lọc kích thước: Chiều rộng >= 800px, tỷ lệ W/H >= 1.15
     - Khử trùng lặp ảnh bằng aHash (Hamming distance <= 6)
  4. Xuất kết quả:
     - outputs/10_ky_luc_bong_da/images/Tin_XX_N.jpg
     - projects/10_ky_luc_bong_da/images/Tin_XX_N.jpg
     - outputs/10_ky_luc_bong_da/image_plan.json & image_credits.json
     - outputs/10_ky_luc_bong_da/qa/contact_scene_XX.jpg & contact_overview.jpg
"""

import sys
sys.dont_write_bytecode = True

import io
import json
import os
import shutil
import time
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont
from ddgs import DDGS

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent
PROJECT_NAME = "10_ky_luc_bong_da"

OUT_DIR = ROOT / "outputs" / PROJECT_NAME
IMG_DIR = OUT_DIR / "images"
QA_DIR = OUT_DIR / "qa"
PROJ_IMG_DIR = ROOT / "projects" / PROJECT_NAME / "images"
CACHE_DIR = Path.home() / "Library" / "Caches" / "DiemDoc" / PROJECT_NAME
QCACHE_PATH = CACHE_DIR / "query_cache.json"

for d in (OUT_DIR, IMG_DIR, QA_DIR, PROJ_IMG_DIR, CACHE_DIR):
    d.mkdir(parents=True, exist_ok=True)

BLOCKED_DOMAINS = {
    "alamy.com", "alamy.de", "gettyimages.com", "gettyimages.co.uk",
    "shutterstock.com", "istockphoto.com", "dreamstime.com",
    "123rf.com", "stock.adobe.com", "depositphotos.com",
    "vectorstock.com", "vecteezy.com", "freepik.com",
    "canstockphoto.com", "bigstockphoto.com", "lookphotos.com",
    "masterfile.com", "inmagine.com", "pond5.com",
    "ebay.com", "amazon.com", "aliexpress.com", "shopee.vn"
}

NEG_KW = " -alamy -shutterstock -istock -getty -dreamstime -vector -cartoon -wallpaper -drawing -shirt -ebay -amazon"
MIN_WIDTH = 800
MIN_RATIO = 1.15

# Danh sách slots ảnh cho 12 cảnh
IMAGE_SLOTS = [
    # Scene 1: Intro (4 ảnh)
    {"scene": 1, "idx": 1, "query": "football trophies history golden cup celebration", "label": "Intro: Bộ sưu tập danh hiệu"},
    {"scene": 1, "idx": 2, "query": "football stadium crowd dramatic lights night match", "label": "Intro: Chảo lửa bóng đá đêm"},
    {"scene": 1, "idx": 3, "query": "FIFA world cup golden trophy podium ceremony", "label": "Intro: Cúp vàng World Cup"},
    {"scene": 1, "idx": 4, "query": "Lionel Messi Cristiano Ronaldo celebration football legends", "label": "Intro: Các tượng đài vĩ đại"},

    # Scene 2: Messi 91 bàn 2012 (10 ảnh)
    {"scene": 2, "idx": 1, "query": "Lionel Messi Barcelona 2012 goal celebration match", "label": "Messi: Ăn mừng bàn thắng 2012"},
    {"scene": 2, "idx": 2, "query": "Lionel Messi 91 goals record 2012 Barcelona match", "label": "Messi: Kỷ lục 91 bàn thắng"},
    {"scene": 2, "idx": 3, "query": "Lionel Messi pointing fingers to the sky 2012", "label": "Messi: Màn chỉ tay lên trời 2012"},
    {"scene": 2, "idx": 4, "query": "Gerd Muller 1972 Bayern Munich match goal historical", "label": "Gerd Müller: 85 bàn thắng 1972"},
    {"scene": 2, "idx": 5, "query": "Gerd Muller West Germany national team striker vintage", "label": "Gerd Müller: Huyền thoại sát thủ Đức"},
    {"scene": 2, "idx": 6, "query": "Lionel Messi Argentina friendly hat-trick Brazil 2012", "label": "Messi: Hat-trick vào lưới Brazil 2012"},
    {"scene": 2, "idx": 7, "query": "Lionel Messi 5 goals Bayer Leverkusen Champions League 2012", "label": "Messi: 5 bàn vào lưới Leverkusen"},
    {"scene": 2, "idx": 8, "query": "Lionel Messi Barcelona number 10 jersey running match 2012", "label": "Messi: Số 10 ma thuật 2012"},
    {"scene": 2, "idx": 9, "query": "Lionel Messi Ballon d'Or 2012 trophy gala suit", "label": "Messi: Quả bóng Vàng 2012"},
    {"scene": 2, "idx": 10, "query": "Lionel Messi smiling lifting trophy Barcelona 2012", "label": "Messi: Nụ cười vô địch 2012"},

    # Scene 3: Ronaldo 985 bàn (10 ảnh)
    {"scene": 3, "idx": 1, "query": "Cristiano Ronaldo celebration siuu Al Nassr stadium", "label": "Ronaldo: Màn ăn mừng Siuu"},
    {"scene": 3, "idx": 2, "query": "Cristiano Ronaldo Real Madrid goal celebration white shirt", "label": "Ronaldo: Cỗ máy ghi bàn Real Madrid"},
    {"scene": 3, "idx": 3, "query": "Cristiano Ronaldo Portugal national team goal celebration passion", "label": "Ronaldo: Tỏa sáng cùng Bồ Đào Nha"},
    {"scene": 3, "idx": 4, "query": "Cristiano Ronaldo 900 goals career milestone match", "label": "Ronaldo: Cột mốc 900+ bàn thắng"},
    {"scene": 3, "idx": 5, "query": "Cristiano Ronaldo Juventus header goal match celebration", "label": "Ronaldo: Bàn thắng đánh đầu Juventus"},
    {"scene": 3, "idx": 6, "query": "Cristiano Ronaldo Manchester United celebration red devils", "label": "Ronaldo: Ngôi sao Manchester United"},
    {"scene": 3, "idx": 7, "query": "Cristiano Ronaldo free kick match stance focus", "label": "Ronaldo: Tư thế sút phạt trứ danh"},
    {"scene": 3, "idx": 8, "query": "Cristiano Ronaldo lifting Champions League trophy celebration", "label": "Ronaldo: Nâng cúp C1 Champions League"},
    {"scene": 3, "idx": 9, "query": "Cristiano Ronaldo screaming celebration victory", "label": "Ronaldo: Tiếng hét chiến thắng"},
    {"scene": 3, "idx": 10, "query": "Cristiano Ronaldo training fitness longevity match action", "label": "Ronaldo: Ý chí rèn luyện phi thường"},

    # Scene 4: Just Fontaine 13 bàn World Cup 1958 (10 ảnh)
    {"scene": 4, "idx": 1, "query": "Just Fontaine France 1958 World Cup goal celebration", "label": "Fontaine: 13 bàn World Cup 1958"},
    {"scene": 4, "idx": 2, "query": "Just Fontaine 1958 World Cup match Sweden action", "label": "Fontaine: Pha bóng World Cup 1958"},
    {"scene": 4, "idx": 3, "query": "Just Fontaine 4 goals West Germany 1958 match", "label": "Fontaine: 4 bàn vào lưới Tây Đức"},
    {"scene": 4, "idx": 4, "query": "Just Fontaine portrait vintage France football legend", "label": "Fontaine: Chân dung huyền thoại Pháp"},
    {"scene": 4, "idx": 5, "query": "Sandor Kocsis Hungary 1954 World Cup match goal", "label": "Sándor Kocsis: 11 bàn World Cup 1954"},
    {"scene": 4, "idx": 6, "query": "Sandor Kocsis Mighty Magyars Hungary celebration vintage", "label": "Sándor Kocsis: Thế hệ vàng Hungary"},
    {"scene": 4, "idx": 7, "query": "World Cup 1958 France team stadium Sweden", "label": "World Cup 1958: Đội tuyển Pháp"},
    {"scene": 4, "idx": 8, "query": "Just Fontaine scoring vintage black white football match", "label": "Fontaine: Khoảnh khắc xé lưới 1958"},
    {"scene": 4, "idx": 9, "query": "Just Fontaine golden boot trophy award presentation", "label": "Fontaine: Nhận Vua phá lưới World Cup"},
    {"scene": 4, "idx": 10, "query": "France national team 1958 World Cup celebration vintage", "label": "Fontaine: Ăn mừng hạng 3 World Cup 1958"},

    # Scene 5: Rogério Ceni 131 bàn thủ môn (10 ảnh)
    {"scene": 5, "idx": 1, "query": "Rogerio Ceni Sao Paulo free kick goal match", "label": "Ceni: Sút phạt hàng rào siêu đẳng"},
    {"scene": 5, "idx": 2, "query": "Rogerio Ceni celebration running goalkeeper goal Sao Paulo", "label": "Ceni: Thủ môn chạy ăn mừng bàn thắng"},
    {"scene": 5, "idx": 3, "query": "Rogerio Ceni penalty kick goal Sao Paulo match", "label": "Ceni: Đá phạt đền chuẩn xác"},
    {"scene": 5, "idx": 4, "query": "Rogerio Ceni lifting Copa Libertadores trophy Sao Paulo", "label": "Ceni: Đội trưởng nâng cúp Libertadores"},
    {"scene": 5, "idx": 5, "query": "Jose Luis Chilavert Paraguay goalkeeper free kick goal vintage", "label": "Chilavert: Thủ môn huyền thoại Paraguay"},
    {"scene": 5, "idx": 6, "query": "Jose Luis Chilavert celebration goalkeeper goal match", "label": "Chilavert: 67 bàn thắng sự nghiệp"},
    {"scene": 5, "idx": 7, "query": "Rogerio Ceni goalkeeper great save match action Sao Paulo", "label": "Ceni: Pha cứu thua xuất sắc"},
    {"scene": 5, "idx": 8, "query": "Rogerio Ceni 100th goal milestone match Sao Paulo", "label": "Ceni: Cột mốc 100 bàn thắng lịch sử"},
    {"scene": 5, "idx": 9, "query": "Rogerio Ceni cheering fans stadium Morumbi Sao Paulo", "label": "Ceni: Biểu tượng sân Morumbi"},
    {"scene": 5, "idx": 10, "query": "Rogerio Ceni captain armband trophy celebration", "label": "Ceni: Đội trưởng huyền thoại"},

    # Scene 6: Lewandowski 5 bàn trong 9 phút (10 ảnh)
    {"scene": 6, "idx": 1, "query": "Robert Lewandowski 5 goals 9 minutes Wolfsburg 2015", "label": "Lewandowski: 5 bàn trong 9 phút"},
    {"scene": 6, "idx": 2, "query": "Lewandowski showing 5 fingers Bayern Wolfsburg 2015 celebration", "label": "Lewandowski: Giơ 5 ngón tay lịch sử"},
    {"scene": 6, "idx": 3, "query": "Robert Lewandowski bicycle kick volley goal Wolfsburg 2015", "label": "Lewandowski: Siêu phẩm vô lê phút 60"},
    {"scene": 6, "idx": 4, "query": "Pep Guardiola shock holding head Lewandowski 5 goals", "label": "Pep Guardiola: Ôm đầu sững sờ"},
    {"scene": 6, "idx": 5, "query": "Ole Gunnar Solskjaer 4 goals Nottingham Forest 1999 Manchester United", "label": "Solskjær: 4 bàn trong 12 phút 1999"},
    {"scene": 6, "idx": 6, "query": "Lewandowski Bayern Munich teammates celebrating 5 goals 2015", "label": "Lewandowski: Đồng đội Bayern chia vui"},
    {"scene": 6, "idx": 7, "query": "Robert Lewandowski Guinness World Records certificates 2015", "label": "Lewandowski: 4 kỷ lục Guinness"},
    {"scene": 6, "idx": 8, "query": "Allianz Arena scoreboard Bayern 5-1 Wolfsburg 2015", "label": "Allianz Arena: Bảng tỷ số 5-1"},
    {"scene": 6, "idx": 9, "query": "Robert Lewandowski substitute entering pitch second half 2015", "label": "Lewandowski: Vào sân từ phút 46"},
    {"scene": 6, "idx": 10, "query": "Robert Lewandowski smiling holding match ball Wolfsburg 2015", "label": "Lewandowski: Ôm bóng kỷ niệm trận đấu"},

    # Scene 7: Messi 46 danh hiệu (10 ảnh)
    {"scene": 7, "idx": 1, "query": "Lionel Messi World Cup 2022 trophy lift Qatar Lusail", "label": "Messi: Nâng cúp vàng World Cup 2022"},
    {"scene": 7, "idx": 2, "query": "Lionel Messi Copa America 2021 trophy celebration Argentina Maracana", "label": "Messi: Vô địch Copa America 2021"},
    {"scene": 7, "idx": 3, "query": "Lionel Messi Inter Miami Supporters Shield 2024 trophy celebration", "label": "Messi: Danh hiệu thứ 46 cùng Inter Miami"},
    {"scene": 7, "idx": 4, "query": "Dani Alves trophies career celebration Barcelona Brazil", "label": "Dani Alves: 43 danh hiệu sự nghiệp"},
    {"scene": 7, "idx": 5, "query": "Lionel Messi Barcelona Champions League 2015 trophy Berlin", "label": "Messi: Champions League 2015"},
    {"scene": 7, "idx": 6, "query": "Lionel Messi Barcelona treble celebration trophies 2009 2015", "label": "Messi: Cú ăn ba vĩ đại Barcelona"},
    {"scene": 7, "idx": 7, "query": "Lionel Messi kissing World Cup trophy golden ball Qatar", "label": "Messi: Nụ hôn cúp vàng thế giới"},
    {"scene": 7, "idx": 8, "query": "Lionel Messi Dani Alves celebration hug Barcelona match", "label": "Messi và Dani Alves: Bộ đôi ăn ý"},
    {"scene": 7, "idx": 9, "query": "Lionel Messi lifting Copa del Rey trophy Barcelona", "label": "Messi: Cúp Nhà Vua Tây Ban Nha"},
    {"scene": 7, "idx": 10, "query": "Lionel Messi smiling trophy collection career medals", "label": "Messi: Bộ sưu tập 46 cúp vô địch"},

    # Scene 8: Sir Alex Ferguson 49 danh hiệu (10 ảnh)
    {"scene": 8, "idx": 1, "query": "Sir Alex Ferguson lifting Premier League trophy Manchester United", "label": "Sir Alex: Nâng cúp Premier League"},
    {"scene": 8, "idx": 2, "query": "Sir Alex Ferguson Champions League 1999 trophy celebration Camp Nou", "label": "Sir Alex: Cú ăn ba lịch sử 1999"},
    {"scene": 8, "idx": 3, "query": "Sir Alex Ferguson Champions League 2008 Moscow trophy rain", "label": "Sir Alex: Vô địch Champions League 2008"},
    {"scene": 8, "idx": 4, "query": "Pep Guardiola Manchester City trophies celebration Premier League", "label": "Pep Guardiola: 40 danh hiệu cầm quân"},
    {"scene": 8, "idx": 5, "query": "Sir Alex Ferguson Aberdeen European Cup Winners Cup 1983 vintage", "label": "Sir Alex: Vô địch châu Âu cùng Aberdeen"},
    {"scene": 8, "idx": 6, "query": "Sir Alex Ferguson Old Trafford statue applause retirement 2013", "label": "Sir Alex: Bức tượng đài Old Trafford"},
    {"scene": 8, "idx": 7, "query": "Sir Alex Ferguson chewing gum dugout Manchester United match", "label": "Sir Alex: Thói quen nhai kẹo cao su"},
    {"scene": 8, "idx": 8, "query": "Sir Alex Ferguson lifting 20th league title Manchester United 2013", "label": "Sir Alex: Danh hiệu Ngoại hạng thứ 13"},
    {"scene": 8, "idx": 9, "query": "Sir Alex Ferguson hugging Wayne Rooney Cristiano Ronaldo United", "label": "Sir Alex: Tình thầy trò với các học trò"},
    {"scene": 8, "idx": 10, "query": "Sir Alex Ferguson smiling trophy showcase Manchester United", "label": "Sir Alex: Di sản 49 danh hiệu"},

    # Scene 9: Messi 21 trận liên tiếp nổ súng (10 ảnh)
    {"scene": 9, "idx": 1, "query": "Lionel Messi Barcelona 2012-2013 goal celebration La Liga", "label": "Messi: Chuỗi ghi bàn La Liga 2012-13"},
    {"scene": 9, "idx": 2, "query": "Lionel Messi scoring streak Barcelona 2013 match action", "label": "Messi: 21 trận liên tiếp nổ súng"},
    {"scene": 9, "idx": 3, "query": "Lionel Messi free kick goal Barcelona 2013 match", "label": "Messi: Sút phạt thần sầu 2013"},
    {"scene": 9, "idx": 4, "query": "Gerd Muller scoring Bayern Munich 1969 1970 16 matches vintage", "label": "Gerd Müller: Kỷ lục 16 trận 1969-70"},
    {"scene": 9, "idx": 5, "query": "Lionel Messi celebration teammates Xavi Iniesta Barcelona 2013", "label": "Messi: Chia vui cùng Xavi, Iniesta"},
    {"scene": 9, "idx": 6, "query": "Lionel Messi dribbling past defenders La Liga 2013 match", "label": "Messi: Pha rê dắt ma thuật La Liga"},
    {"scene": 9, "idx": 7, "query": "Lionel Messi sliding knees celebration Camp Nou 2013", "label": "Messi: Trượt cỏ ăn mừng Camp Nou"},
    {"scene": 9, "idx": 8, "query": "Lionel Messi pointing to sky Barcelona jersey 2013", "label": "Messi: Ăn mừng quen thuộc 2013"},
    {"scene": 9, "idx": 9, "query": "Barcelona La Liga champions 2012-2013 celebration 100 points", "label": "Barcelona: Vô địch La Liga 100 điểm"},
    {"scene": 9, "idx": 10, "query": "Lionel Messi golden shoe award 2013 presentation", "label": "Messi: Chiếc giày Vàng châu Âu 2013"},

    # Scene 10: Pelé 3 World Cup (10 ảnh)
    {"scene": 10, "idx": 1, "query": "Pele 1958 World Cup Sweden young crying champion Brazil vintage", "label": "Pelé: 17 tuổi vô địch World Cup 1958"},
    {"scene": 10, "idx": 2, "query": "Pele lifted by teammates 1970 World Cup Mexico final stadium", "label": "Pelé: Được kênh kiệu tại Mexico 1970"},
    {"scene": 10, "idx": 3, "query": "Pele Brazil 1970 World Cup final goal celebration jump Jairzinho", "label": "Pelé: Nhảy lên ôm Jairzinho 1970"},
    {"scene": 10, "idx": 4, "query": "Pele holding Jules Rimet trophy 1970 World Cup Brazil", "label": "Pelé: Nâng cúp Nữ thần Vàng Jules Rimet"},
    {"scene": 10, "idx": 5, "query": "Pele 1962 World Cup Chile Brazil squad vintage", "label": "Pelé: Vô địch World Cup lần 2 năm 1962"},
    {"scene": 10, "idx": 6, "query": "Pele bicycle kick famous photo Brazil football stadium vintage", "label": "Pelé: Cú móc bóng xe đạp chổng ngược"},
    {"scene": 10, "idx": 7, "query": "Pele Carlos Alberto 1970 World Cup Brazil dream team celebration", "label": "Pelé: Đội hình vĩ đại Brazil 1970"},
    {"scene": 10, "idx": 8, "query": "Pele smiling with three World Cup trophies vintage", "label": "Pelé: 3 cúp vàng World Cup vô tiền khoáng hậu"},
    {"scene": 10, "idx": 9, "query": "Pele 1958 header goal Sweden vintage football match", "label": "Pelé: Bàn thắng chung kết 1958"},
    {"scene": 10, "idx": 10, "query": "Pele yellow jersey number 10 Brazil national team classic", "label": "Pelé: Số 10 vàng kim cương Brazil"},

    # Scene 11: Kazuyoshi Miura 59 tuổi (10 ảnh)
    {"scene": 11, "idx": 1, "query": "Kazuyoshi Miura playing 2024 2025 match action King Kazu", "label": "King Kazu: Thi đấu ở tuổi 58-59"},
    {"scene": 11, "idx": 2, "query": "King Kazu Kazuyoshi Miura Kazu dance goal celebration Japan", "label": "King Kazu: Điệu nhảy ăn mừng Kazu dance"},
    {"scene": 11, "idx": 3, "query": "Kazuyoshi Miura Yokohama FC jersey veteran match", "label": "King Kazu: Màu áo Yokohama FC"},
    {"scene": 11, "idx": 4, "query": "Sir Stanley Matthews vintage match Stoke City black white", "label": "Sir Stanley Matthews: Thi đấu tuổi 50"},
    {"scene": 11, "idx": 5, "query": "Sir Stanley Matthews 50 years old playing match vintage football", "label": "Sir Stanley Matthews: Quả bóng Vàng đầu tiên"},
    {"scene": 11, "idx": 6, "query": "Kazuyoshi Miura Oliveirense Portugal match action", "label": "King Kazu: Chơi bóng tại Bồ Đào Nha"},
    {"scene": 11, "idx": 7, "query": "Kazuyoshi Miura Japan national team 1990s match vintage", "label": "King Kazu: Đội tuyển Nhật Bản thập niên 90"},
    {"scene": 11, "idx": 8, "query": "Kazuyoshi Miura training fitness exercise longevity soccer", "label": "King Kazu: Bài tập thể lực phi thường"},
    {"scene": 11, "idx": 9, "query": "Kazuyoshi Miura smiling press conference King Kazu interview", "label": "King Kazu: Tinh thần bất tử với bóng đá"},
    {"scene": 11, "idx": 10, "query": "Kazuyoshi Miura match action stadium grass Japan 2026", "label": "King Kazu: Bước chạy bền bỉ 40 năm"},

    # Scene 12: Outro (4 ảnh)
    {"scene": 12, "idx": 1, "query": "football stadium lights night dramatic cinematic wide view", "label": "Outro: Toàn cảnh sân vận động rực sáng"},
    {"scene": 12, "idx": 2, "query": "champions league golden trophy stadium podium bokeh lights", "label": "Outro: Chiếc cúp vinh quang"},
    {"scene": 12, "idx": 3, "query": "football fans cheering flares stadium celebration passion", "label": "Outro: Ngọn lửa đam mê của người hâm mộ"},
    {"scene": 12, "idx": 4, "query": "football ball on center spot stadium lights grass night", "label": "Outro: Trái bóng tròn trên thảm cỏ"},
]


def ahash(img: Image.Image) -> int:
    """Tính 64-bit Average Hash để khử trùng lặp."""
    gray = img.convert("L").resize((8, 8), Image.Resampling.LANCZOS)
    pixels = list(gray.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join("1" if p >= avg else "0" for p in pixels)
    return int(bits, 2)


def hamming_distance(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def is_host_blocked(url: str) -> bool:
    try:
        from urllib.parse import urlparse
        host = urlparse(url).netloc.lower()
        for b in BLOCKED_DOMAINS:
            if b in host:
                return True
        return False
    except Exception:
        return True


class ImageDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        })
        self.qcache = {}
        if QCACHE_PATH.exists():
            try:
                with open(QCACHE_PATH, "r", encoding="utf-8") as f:
                    self.qcache = json.load(f)
            except Exception:
                self.qcache = {}

    def search_queries(self, query: str) -> list[dict]:
        full_query = query + NEG_KW
        if full_query in self.qcache and self.qcache[full_query]:
            return self.qcache[full_query]

        for attempt in range(3):
            try:
                with DDGS() as ddgs:
                    results = ddgs.images(
                        full_query,
                        region="us-en",
                        safesearch="off",
                        size="Large",
                        layout="Wide",
                        max_results=25
                    )
                res_list = list(results)
                if res_list:
                    self.qcache[full_query] = res_list
                    with open(QCACHE_PATH, "w", encoding="utf-8") as f:
                        json.dump(self.qcache, f, ensure_ascii=False)
                return res_list
            except Exception as e:
                wait = 4 * (attempt + 1)
                print(f"    [search retry {attempt+1}] {e} -> đợi {wait}s...", flush=True)
                time.sleep(wait)
        return []

    def fetch_image(self, url: str) -> Image.Image | None:
        if is_host_blocked(url):
            return None
        low_url = url.lower().split("?")[0]
        if low_url.endswith((".svg", ".gif")):
            return None

        try:
            resp = self.session.get(url, timeout=12, stream=False)
            if resp.status_code != 200 or len(resp.content) < 20_000:
                return None
            img = Image.open(io.BytesIO(resp.content))
            img.load()
            w, h = img.size
            if w < MIN_WIDTH or h == 0 or (w / h) < MIN_RATIO:
                return None
            if img.mode != "RGB":
                img = img.convert("RGB")
            return img
        except Exception:
            return None


def run():
    print("=" * 66)
    print("  PHASE 1A — THU THẬP ẢNH TƯ LIỆU CHO 10 KỶ LỤC BÓNG ĐÁ")
    print("=" * 66)

    fetcher = ImageDownloader()
    hashes: dict[str, int] = {}
    plan_records = []
    credits_map = {}

    total = len(IMAGE_SLOTS)
    downloaded = 0
    skipped = 0

    for idx, slot in enumerate(IMAGE_SLOTS, 1):
        sid = slot["scene"]
        sidx = slot["idx"]
        fname = f"Tin_{sid:02d}_{sidx}.jpg"
        out_file = IMG_DIR / fname
        proj_file = PROJ_IMG_DIR / fname

        print(f"[{idx:03d}/{total:03d}] Scene {sid:02d} #{sidx:02d} ({fname}): '{slot['query']}'")

        # Resume nếu ảnh đã tồn tại
        if out_file.exists() and out_file.stat().st_size > 15_000:
            try:
                img = Image.open(out_file)
                h_val = ahash(img)
                hashes[fname] = h_val
                if not proj_file.exists():
                    shutil.copyfile(out_file, proj_file)
                print(f"  -> [TỒN TẠI] {img.size[0]}x{img.size[1]} ({out_file.stat().st_size // 1024} KB)")
                skipped += 1
                plan_records.append({
                    "file": fname,
                    "scene": sid,
                    "index": sidx,
                    "label": slot["label"],
                    "query": slot["query"],
                    "status": "cached"
                })
                continue
            except Exception:
                pass

        cands = fetcher.search_queries(slot["query"])
        success = False

        for c in cands:
            img_url = c.get("image")
            if not img_url:
                continue

            img = fetcher.fetch_image(img_url)
            if img is None:
                continue

            h_val = ahash(img)
            # Kiểm tra trùng lặp
            is_dup = False
            for prev_fname, prev_h in hashes.items():
                if hamming_distance(h_val, prev_h) <= 6:
                    is_dup = True
                    break
            if is_dup:
                continue

            # Lưu ảnh
            img.save(out_file, "JPEG", quality=92, optimize=True)
            shutil.copyfile(out_file, proj_file)
            hashes[fname] = h_val

            w, h = img.size
            credit_title = c.get("title", "").strip()
            source_domain = c.get("domain", "").strip() or "Wikimedia / Sports Archive"

            credits_map[fname] = {
                "source": source_domain.upper(),
                "title": credit_title,
                "url": img_url
            }

            plan_records.append({
                "file": fname,
                "scene": sid,
                "index": sidx,
                "label": slot["label"],
                "query": slot["query"],
                "url": img_url,
                "source": source_domain,
                "dimensions": f"{w}x{h}",
                "size_kb": out_file.stat().st_size // 1024,
                "status": "downloaded"
            })

            print(f"  -> [OK] {w}x{h} ({out_file.stat().st_size // 1024} KB) từ {source_domain}")
            downloaded += 1
            success = True
            time.sleep(0.3)
            break

        if not success:
            print(f"  -> [CẢNH BÁO] Không tìm được ảnh phù hợp cho slot {fname}. Sẽ tạo ảnh màu nền Cyber-Stadium tạm thời.")
            # Tạo ảnh placeholder Cyber-Stadium chất lượng cao
            bg = Image.new("RGB", (1920, 1080), (7, 11, 20))
            draw = ImageDraw.Draw(bg)
            draw.rectangle([(20, 20), (1900, 1060)], outline=(0, 229, 255), width=4)
            bg.save(out_file, "JPEG", quality=90)
            shutil.copyfile(out_file, proj_file)
            plan_records.append({
                "file": fname,
                "scene": sid,
                "index": sidx,
                "label": slot["label"],
                "query": slot["query"],
                "status": "placeholder"
            })

    # Lưu image_plan.json và image_credits.json
    with open(OUT_DIR / "image_plan.json", "w", encoding="utf-8") as f:
        json.dump(plan_records, f, ensure_ascii=False, indent=2)
    with open(ROOT / "projects" / PROJECT_NAME / "image_plan.json", "w", encoding="utf-8") as f:
        json.dump(plan_records, f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "image_credits.json", "w", encoding="utf-8") as f:
        json.dump(credits_map, f, ensure_ascii=False, indent=2)
    with open(ROOT / "projects" / PROJECT_NAME / "image_credits.json", "w", encoding="utf-8") as f:
        json.dump(credits_map, f, ensure_ascii=False, indent=2)

    print(f"\n[XONG] Tải mới: {downloaded}, Đã có: {skipped}, Tổng: {len(hashes)}/{total} ảnh.")

    # Sinh Contact Sheet QA
    generate_contact_sheets()


def generate_contact_sheets():
    print("\n--- SINH CONTACT SHEET QA CHO TỪNG CẢNH ---")
    files = sorted(IMG_DIR.glob("Tin_*.jpg"), key=lambda p: (int(p.stem.split("_")[1]), int(p.stem.split("_")[2])))

    by_scene = {}
    for f in files:
        sid = int(f.stem.split("_")[1])
        by_scene.setdefault(sid, []).append(f)

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    scene_titles = {
        1: "Intro: Màn Chào Sân",
        2: "Kỷ lục #1: Messi 91 Bàn (2012)",
        3: "Kỷ lục #2: Ronaldo 985 Bàn Sự Nghiệp",
        4: "Kỷ lục #3: Just Fontaine 13 Bàn World Cup 1958",
        5: "Kỷ lục #4: Rogério Ceni 131 Bàn Thủ Môn",
        6: "Kỷ lục #5: Lewandowski 5 Bàn Trong 9 Phút",
        7: "Kỷ lục #6: Messi 46 Danh Hiệu Tập Thể",
        8: "Kỷ lục #7: Sir Alex Ferguson 49 Danh Hiệu HLV",
        9: "Kỷ lục #8: Messi Chuỗi 21 Trận Ghi Bàn",
        10: "Kỷ lục #9: Pelé 3 Lần Vô Địch World Cup",
        11: "Kỷ lục #10: Kazuyoshi Miura 59 Tuổi (2026)",
        12: "Outro: Kết Thúc & Kêu Gọi",
    }

    overview_thumbs = []

    for sid, fs in by_scene.items():
        cols = 5
        tw, th = 340, 191
        rows = (len(fs) + cols - 1) // cols
        header_h = 50
        sheet_w = cols * (tw + 12) + 12
        sheet_h = header_h + rows * (th + 36) + 12

        sheet = Image.new("RGB", (sheet_w, sheet_h), (7, 11, 20))
        draw = ImageDraw.Draw(sheet)

        # Header
        stitle = scene_titles.get(sid, f"Scene {sid:02d}")
        draw.text((16, 12), f"QA SCENE {sid:02d} — {stitle.upper()} ({len(fs)} ẢNH)", fill=(0, 229, 255), font=title_font)
        draw.line([(16, 42), (sheet_w - 16, 42)], fill=(0, 229, 255), width=2)

        for i, f in enumerate(fs):
            r, c = divmod(i, cols)
            x = 12 + c * (tw + 12)
            y = header_h + r * (th + 36)
            try:
                im = Image.open(f)
                im.thumbnail((tw, th), Image.Resampling.LANCZOS)
                # Dán căn giữa
                ox = x + (tw - im.size[0]) // 2
                oy = y + (th - im.size[1]) // 2
                sheet.paste(im, (ox, oy))
                draw.rectangle([(x, y), (x + tw, y + th)], outline=(30, 41, 59), width=1)
            except Exception:
                pass

            label_txt = f.name
            draw.text((x + 2, y + th + 6), label_txt, fill=(255, 210, 90), font=font)

        out_qa = QA_DIR / f"contact_scene_{sid:02d}.jpg"
        sheet.save(out_qa, "JPEG", quality=88)
        print(f"  [OK] Đã lưu: {out_qa.name}")

        # Lưu ảnh thumb cho overview
        thumb_im = sheet.copy()
        thumb_im.thumbnail((600, 400), Image.Resampling.LANCZOS)
        overview_thumbs.append((sid, thumb_im))

    # Sinh contact_overview.jpg
    if overview_thumbs:
        ocols = 3
        orows = (len(overview_thumbs) + ocols - 1) // ocols
        otw, oth = 600, 400
        ov_w = ocols * (otw + 16) + 16
        ov_h = 60 + orows * (oth + 40) + 16
        ov_sheet = Image.new("RGB", (ov_w, ov_h), (7, 11, 20))
        ov_draw = ImageDraw.Draw(ov_sheet)

        ov_draw.text((20, 16), "TỔNG HỢP KIỂM DUYỆT THỊ GIÁC QA — 10 KỶ LỤC BÓNG ĐÁ (12 SCENES)", fill=(0, 229, 255), font=title_font)
        ov_draw.line([(20, 48), (ov_w - 20, 48)], fill=(0, 229, 255), width=2)

        for i, (sid, tim) in enumerate(overview_thumbs):
            r, c = divmod(i, ocols)
            x = 16 + c * (otw + 16)
            y = 60 + r * (oth + 40)
            ov_sheet.paste(tim, (x, y))
            stitle = scene_titles.get(sid, f"Scene {sid:02d}")
            ov_draw.text((x + 4, y + tim.size[1] + 6), f"SCENE {sid:02d}: {stitle}", fill=(255, 210, 90), font=font)

        ov_out = QA_DIR / "contact_overview.jpg"
        ov_sheet.save(ov_out, "JPEG", quality=85)
        print(f"  [OK] Đã lưu bảng tổng hợp: {ov_out.name}")

    print("--- HOÀN THÀNH TẤT CẢ CONTACT SHEETS QA ---")


if __name__ == "__main__":
    run()
