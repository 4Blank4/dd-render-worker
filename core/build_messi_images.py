#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_messi_images.py — Bộ thu thập ảnh tư liệu cho video chuyên đề Lionel Messi (30.10.2026)

Quy trình:
  1. Chia kịch bản 9 cảnh thành từng câu, sinh kế hoạch ảnh:
     - Tiêu đề cảnh  = 3 ảnh
     - Câu  < 42 từ  = 1 ảnh
     - Câu 42-65 từ  = 2 ảnh
     - Câu  > 65 từ  = 3 ảnh
  2. Tìm ảnh qua DDGS (size=Large, layout=Wide) cho từng slot, lọc:
     - Ảnh ngang W/H >= 1.18, chiều rộng >= 800px
     - Chặn kho ảnh stock hay dính watermark (alamy, getty, shutterstock...)
     - Khử trùng lặp bằng aHash (Hamming <= 6)
  3. Xuất artefact:
     - outputs/30.10.2026/kich_ban_tung_cau.txt
     - outputs/30.10.2026/thethao.txt, thethao.json
     - outputs/30.10.2026/image_plan.json (nhật ký nguồn từng ảnh)
     - outputs/30.10.2026/images/Tin_XX_N.jpg
     - Contact sheet QA: ~/Library/Caches/DiemDoc/messi_3010/qa/

Cách chạy:
  python3 -B core/build_messi_images.py            # chạy chính (resume tự động)
  python3 -B core/build_messi_images.py --force    # chuyển ảnh cũ vào Trash và tải lại
  python3 -B core/build_messi_images.py --sheets   # chỉ sinh lại contact sheet
"""
import sys
import os
import json
import time
import io
import shutil
from pathlib import Path

sys.dont_write_bytecode = True

import requests
from PIL import Image, ImageDraw, ImageFont
from ddgs import DDGS

# ------------------------------------------------------------------ ĐƯỜNG DẪN
ROOT = Path(__file__).resolve().parent.parent
DAY = ROOT / "outputs" / "30.10.2026"
IMG_DIR = DAY / "images"
CACHE = Path.home() / "Library" / "Caches" / "DiemDoc" / "messi_3010"
STAGING = CACHE / "staging"
QA_DIR = CACHE / "qa"
QCACHE = CACHE / "query_cache.json"
TRASH_DIR = Path.home() / ".Trash"

for d in (DAY, IMG_DIR, STAGING, QA_DIR):
    d.mkdir(parents=True, exist_ok=True)

VIDEO_TITLE = "Lionel Messi Tuổi 39: 48 Danh Hiệu, 936 Bàn Thắng Và Đế Chế Bất Tử"

# ------------------------------------------------------------------ DỮ LIỆU KỊCH BẢN
SCENES = [
    {
        "id": 1,
        "group": "Nhóm: Mở Màn",
        "title": "Lionel Messi tuổi 39: 48 danh hiệu tập thể và bức tranh vĩ đại nhất lịch sử",
        "title_queries": [
            "Lionel Messi Inter Miami 2026 celebration",
            "Lionel Messi Argentina World Cup trophy kiss",
            "Lionel Messi Ballon d'Or trophy ceremony",
        ],
        "sentences": [
            {
                "text": "Tháng 10 năm 2026, trên thảm cỏ rực nắng của sân vận động mới Nu Stadium tại Miami, một người đàn ông 39 tuổi vẫn lướt qua hàng phòng ngự đối phương nhẹ nhàng như một cơn gió.",
                "queries": [
                    "Lionel Messi Inter Miami dribbling match 2025",
                    "Lionel Messi Inter Miami pink jersey stadium",
                ],
            },
            {
                "text": "Người đàn ông ấy là Lionel Messi — huyền thoại sống của bóng đá đương đại, người vừa khép lại mùa giải chính thức MLS 2026 với 25 bàn thắng và 15 đường kiến tạo chỉ sau 29 trận đấu.",
                "queries": [
                    "Lionel Messi Inter Miami goal celebration arms wide",
                    "Lionel Messi MLS captain armband Inter Miami",
                ],
            },
            {
                "text": "Ở độ tuổi mà hầu hết những ngôi sao lớn nhất đã giải nghệ, Lionel Messi vẫn tạo ra trung bình hơn một bàn thắng hoặc kiến tạo trong mỗi lần ra sân.",
                "queries": [
                    "Lionel Messi smiling pitch Inter Miami close up",
                ],
            },
            {
                "text": "Tính đến tháng 10 năm 2026, cái tên Lionel Messi đang đứng trên một đỉnh cao cô độc mà có lẽ phải hàng thế kỷ nữa nhân loại mới dám mơ có người chạm tới.",
                "queries": [
                    "Lionel Messi spotlight stadium night dramatic",
                ],
            },
            {
                "text": "Theo thống kê từ FIFA và BeIN Sports, sau hơn 1.180 trận đấu chính thức, Messi sở hữu tổng cộng 48 danh hiệu tập thể — trở thành cầu thủ giàu thành tích nhất lịch sử bóng đá thế giới.",
                "queries": [
                    "Lionel Messi lifting trophy celebration Argentina",
                    "Lionel Messi Barcelona trophy celebration Camp Nou",
                ],
            },
            {
                "text": "Bên cạnh 48 chiếc cúp ấy là 936 bàn thắng và 466 đường kiến tạo, tức tổng cộng 1.402 lần in dấu giày trực tiếp vào bàn thắng — kỷ lục vô tiền khoáng hậu của lịch sử túc cầu.",
                "queries": [
                    "Lionel Messi pointing to sky celebration iconic",
                    "Lionel Messi striking ball shot match",
                ],
            },
            {
                "text": "Mùa hè năm 2026 vừa qua còn chứng kiến chương cuối đầy kiêu hãnh của anh cùng đội tuyển Argentina tại FIFA World Cup 2026, nơi anh phá vỡ kỷ lục ghi bàn mọi thời đại của giải đấu.",
                "queries": [
                    "Lionel Messi Argentina captain World Cup match",
                    "Lionel Messi Argentina national team celebration crowd",
                ],
            },
            {
                "text": "Hôm nay, Điểm Đọc sẽ cùng các bạn lật mở biên niên sử thành tích đồ sộ của Lionel Messi tính đến hiện tại: từ 8 Quả Bóng Vàng, kỷ nguyên Barcelona, kỳ tích 91 bàn năm 2012, đỉnh cao cùng Argentina cho đến cuộc cách mạng trên đất Mỹ.",
                "queries": [
                    "Lionel Messi 8 Ballon d'Or trophies stage",
                    "Lionel Messi FC Barcelona number 10 iconic",
                ],
            },
        ],
    },
    {
        "id": 2,
        "group": "Nhóm: Đế Chế Cá Nhân Độc Tôn",
        "title": "Kỷ lục 8 Ballon d'Or và 6 Chiếc Giày Vàng Châu Âu không đối thủ",
        "title_queries": [
            "Lionel Messi Ballon d'Or 2023 Paris trophy",
            "Lionel Messi 6 European Golden Shoe trophies",
            "Lionel Messi FIFA The Best award trophy",
        ],
        "sentences": [
            {
                "text": "Nếu có một thước đo phản ánh sự thống trị tuyệt đối của một cá nhân trước phần còn lại của thế giới bóng đá, thì đó chính là danh hiệu Quả Bóng Vàng — Ballon d'Or.",
                "queries": [
                    "Ballon d'Or golden trophy close up stage",
                ],
            },
            {
                "text": "Trong suốt lịch sử từ năm 1956 đến nay, những huyền thoại kiệt xuất nhất như Johan Cruyff, Michel Platini hay Marco van Basten cũng chỉ dừng lại ở con số 3 lần đăng quang.",
                "queries": [
                    "Johan Cruyff Ballon d'Or trophy vintage",
                ],
            },
            {
                "text": "Cristiano Ronaldo, đối thủ lớn nhất sự nghiệp của Messi, đã tạo nên cuộc đua thế kỷ để vươn tới cột mốc 5 danh hiệu cao quý.",
                "queries": [
                    "Lionel Messi and Cristiano Ronaldo UEFA gala",
                ],
            },
            {
                "text": "Nhưng Lionel Messi đã đẩy giới hạn ấy lên một tầng cao hoàn toàn khác: 8 danh hiệu Ballon d'Or vào các năm 2009, 2010, 2011, 2012, 2015, 2019, 2021 và 2023.",
                "queries": [
                    "Lionel Messi winning 8th Ballon d'Or 2023",
                    "Lionel Messi holding Ballon d'Or smiling",
                ],
            },
            {
                "text": "Tám Quả Bóng Vàng — trải dài suốt 14 năm từ khi anh mới là chàng trai 22 tuổi rực sáng tại châu Âu cho đến khi trở thành nhà vô địch thế giới ở tuổi 36.",
                "queries": [
                    "Lionel Messi Ballon d'Or 2015 ceremony trophy stage",
                ],
            },
            {
                "text": "Theo France Football, khoảng cách 3 Quả Bóng Vàng giữa Messi và người xếp thứ hai lớn tương đương với toàn bộ sự nghiệp của một huyền thoại hàng đầu lịch sử.",
                "queries": [
                    "Lionel Messi Ballon d'Or trophies collection Camp Nou",
                ],
            },
            {
                "text": "Song hành cùng 8 Ballon d'Or là kỷ lục 8 lần được vinh danh Cầu thủ xuất sắc nhất năm của FIFA — bao gồm FIFA World Player, FIFA Ballon d'Or và FIFA The Best.",
                "queries": [
                    "Lionel Messi FIFA The Best award ceremony suit",
                ],
            },
            {
                "text": "Nhiều người thường ca ngợi Messi như một nhạc trưởng hào hoa, nhưng đôi khi họ quên mất rằng anh còn là cỗ máy săn bàn đáng sợ bậc nhất lục địa già.",
                "queries": [
                    "Lionel Messi Barcelona powerful shot goal",
                ],
            },
            {
                "text": "Bằng chứng đanh thép nằm ở bộ sưu tập kỷ lục 6 Chiếc Giày Vàng Châu Âu — European Golden Shoe — cùng kỷ lục 8 danh hiệu Vua phá lưới La Liga Pichichi.",
                "queries": [
                    "Lionel Messi European Golden Shoe trophy presentation",
                    "Lionel Messi Pichichi trophy La Liga top scorer",
                ],
            },
            {
                "text": "Vừa giữ kỷ lục nhận nhiều Quả Bóng Vàng nhất, vừa giữ kỷ lục giành nhiều Chiếc Giày Vàng Châu Âu nhất — đó chính là sự thống trị tuyệt đối của Lionel Messi.",
                "queries": [
                    "Lionel Messi Ballon d'Or Camp Nou fans ovation",
                ],
            },
        ],
    },
    {
        "id": 3,
        "group": "Nhóm: Kỷ Nguyên Vàng Son Barcelona",
        "title": "672 bàn thắng, 35 danh hiệu và di sản bất diệt tại Camp Nou",
        "title_queries": [
            "Lionel Messi FC Barcelona Camp Nou iconic celebration",
            "Lionel Messi UEFA Champions League trophy Barcelona",
            "Lionel Messi 35 trophies FC Barcelona farewell",
        ],
        "sentences": [
            {
                "text": "Để hiểu được nền móng vĩ đại của đế chế Lionel Messi, chúng ta phải quay về thánh đường Camp Nou — nơi anh cống hiến 17 mùa giải liên tiếp trong màu áo FC Barcelona từ năm 2004 đến năm 2021.",
                "queries": [
                    "Camp Nou stadium FC Barcelona full crowd night",
                    "Lionel Messi Barcelona captain walking pitch Camp Nou",
                ],
            },
            {
                "text": "Theo thống kê chính thức từ FC Barcelona, Messi đã ra sân tổng cộng 778 trận đấu — nhiều nhất lịch sử hơn một thế kỷ của gã khổng lồ xứ Catalonia.",
                "queries": [
                    "Lionel Messi Barcelona celebrating goal Camp Nou",
                ],
            },
            {
                "text": "Trong 778 trận đấu ấy, anh ghi tới 672 bàn thắng và thực hiện 303 đường kiến tạo thành bàn.",
                "queries": [
                    "Lionel Messi Barcelona goal celebration Bernabeu shirt",
                ],
            },
            {
                "text": "Con số 672 bàn thắng giúp Messi xô đổ kỷ lục tồn tại nhiều thập kỷ của Vua bóng đá Pelé trong màu áo Santos để trở thành cầu thủ ghi nhiều bàn thắng nhất lịch sử cho một câu lạc bộ duy nhất.",
                "queries": [
                    "Lionel Messi 644 goals Pele record Barcelona celebration",
                    "Lionel Messi Barcelona dribbling past defenders",
                ],
            },
            {
                "text": "Tại La Liga, anh giữ kỷ lục ghi bàn mọi thời đại với 474 bàn thắng chỉ sau 520 trận đấu — đạt hiệu suất trung bình hơn 0,91 bàn mỗi trận.",
                "queries": [
                    "Lionel Messi La Liga trophy celebration Barcelona",
                ],
            },
            {
                "text": "Những bàn thắng và kiến tạo của Messi đã trực tiếp mang về cho phòng truyền thống sân Camp Nou tổng cộng 35 danh hiệu chính thức.",
                "queries": [
                    "Lionel Messi 35 trophies FC Barcelona photo",
                ],
            },
            {
                "text": "Bộ sưu tập ấy bao gồm 10 chức vô địch La Liga, 7 Cúp Nhà vua Copa del Rey, 8 Siêu cúp Tây Ban Nha, 3 Siêu cúp châu Âu, 3 FIFA Club World Cup và 4 chiếc cúp bạc danh giá UEFA Champions League vào các năm 2006, 2009, 2011 và 2015.",
                "queries": [
                    "Lionel Messi Champions League final 2011 Wembley goal",
                    "Lionel Messi Copa del Rey trophy 2021 Barcelona",
                ],
            },
            {
                "text": "Đỉnh cao rực rỡ nhất là năm 2009 dưới thời Pep Guardiola, khi Messi dẫn dắt Barcelona giành cú ăn sáu lịch sử đầu tiên của bóng đá thế giới, trước khi cùng Luis Suárez và Neymar tái lập cú ăn ba huyền thoại năm 2015.",
                "queries": [
                    "Lionel Messi Pep Guardiola FC Barcelona 2009 Champions League",
                    "Messi Suarez Neymar MSN Barcelona 2015 celebration",
                ],
            },
        ],
    },
    {
        "id": 4,
        "group": "Nhóm: Kỳ Tích Siêu Phàm",
        "title": "Năm 2012 lịch sử với 91 bàn thắng và kỷ lục 62 cú hat-trick",
        "title_queries": [
            "Lionel Messi 2012 91 goals Barcelona celebration",
            "Lionel Messi 5 goals Bayer Leverkusen 2012 match ball",
            "Lionel Messi hat trick match ball Barcelona",
        ],
        "sentences": [
            {
                "text": "Trong toàn bộ sự nghiệp lẫy lừng của Lionel Messi, nếu phải chọn ra một năm dương lịch thách thức mọi định luật vật lý của môn bóng đá, đó chắc chắn là năm 2012.",
                "queries": [
                    "Lionel Messi Barcelona 2012 jersey celebration",
                ],
            },
            {
                "text": "Suốt 40 năm trước đó, kỷ lục ghi 85 bàn thắng trong năm dương lịch 1972 của huyền thoại người Đức Gerd Müller được giới chuyên môn coi là cột mốc bất khả xâm phạm.",
                "queries": [
                    "Gerd Muller Bayern Munich 1972 striker",
                ],
            },
            {
                "text": "Thế nhưng vào năm 2012, ở tuổi 25, Lionel Messi đã đập tan cột mốc ấy bằng con số khiến cả thế giới ngả mũ kinh ngạc: 91 bàn thắng chính thức chỉ trong vòng 12 tháng.",
                "queries": [
                    "Lionel Messi 91 goals 2012 Real Betis celebration",
                ],
            },
            {
                "text": "Theo sách Kỷ lục Guinness Thế giới và Opta, trong 69 trận đấu của năm 2012, Messi đã ghi 79 bàn cho FC Barcelona và 12 bàn cho đội tuyển quốc gia Argentina, kèm theo 22 đường kiến tạo.",
                "queries": [
                    "Lionel Messi Argentina dribbling past defenders match",
                    "Lionel Messi Barcelona 2012 goal celebration fingers sky",
                ],
            },
            {
                "text": "Chỉ riêng 91 bàn thắng tương đương hiệu suất 1,31 bàn mỗi trận — nghĩa là cứ mỗi 66 phút trên sân, Messi lại bắt thủ môn đối phương vào lưới nhặt bóng một lần.",
                "queries": [
                    "Lionel Messi chip goal goalkeeper Barcelona",
                ],
            },
            {
                "text": "Trong năm 2012 kỳ diệu ấy, anh lập kỷ lục ghi 50 bàn trong một mùa giải La Liga, ghi bàn vào lưới cả 19 đội bóng đối thủ liên tiếp, và trở thành cầu thủ đầu tiên trong lịch sử UEFA Champions League ghi 5 bàn trong một trận knock-out trước Bayer Leverkusen.",
                "queries": [
                    "Lionel Messi Bayer Leverkusen 5 goals Champions League 2012",
                    "Lionel Messi 50 goals La Liga 2012 celebration",
                ],
            },
            {
                "text": "Nhìn rộng ra toàn sự nghiệp tính đến tháng 10 năm 2026, theo BolaVIP và The Stats Zone, Messi đã lập tổng cộng 62 cú hat-trick chính thức — gồm 48 cho Barcelona, 11 cho Argentina và 3 cho Inter Miami.",
                "queries": [
                    "Lionel Messi holding hat trick match ball Argentina",
                    "Lionel Messi hat trick Inter Miami celebration",
                ],
            },
            {
                "text": "Những con số ấy chứng minh một sự thật: khi đạt trạng thái thăng hoa cao nhất, Lionel Messi là một thế lực siêu nhiên không thể ngăn cản.",
                "queries": [
                    "Lionel Messi surrounded by defenders dribbling",
                ],
            },
        ],
    },
    {
        "id": 5,
        "group": "Nhóm: Thống Kê Toàn Sự Nghiệp",
        "title": "936 bàn thắng, 466 kiến tạo và cuộc rượt đuổi kỷ lục đá phạt mọi thời đại",
        "title_queries": [
            "Lionel Messi free kick goal Liverpool 2019 Camp Nou",
            "Lionel Messi free kick Inter Miami Cruz Azul debut",
            "Lionel Messi passing vision playmaker Argentina",
        ],
        "sentences": [
            {
                "text": "Nếu chỉ nhìn vào 936 bàn thắng chính thức tính đến tháng 10 năm 2026, người ta sẽ thấy một chân sút vĩ đại; nhưng khi đặt cạnh 466 đường kiến tạo, chúng ta mới thấy trọn vẹn sự độc nhất vô nhị của Lionel Messi.",
                "queries": [
                    "Lionel Messi assist pass Argentina World Cup",
                ],
            },
            {
                "text": "Trong lịch sử bóng đá thế giới, chưa từng có cầu thủ nào chạm tới mốc 400 kiến tạo chính thức, ngoại trừ duy nhất Lionel Messi với 466 lần dọn cỗ cho đồng đội lập công.",
                "queries": [
                    "Lionel Messi celebrating with teammates Argentina hug",
                ],
            },
            {
                "text": "Cộng gộp cả hai chỉ số, Messi đạt mốc 1.402 lần đóng góp trực tiếp vào bàn thắng sau hơn 1.180 trận đấu — bỏ xa mọi huyền thoại từ Pelé, Diego Maradona cho tới Cristiano Ronaldo.",
                "queries": [
                    "Lionel Messi Diego Maradona Argentina tribute",
                ],
            },
            {
                "text": "Nhưng có một thống kê khác ở nửa sau sự nghiệp của Messi còn khiến giới phân tích kinh ngạc hơn gấp bội: nghệ thuật sút phạt hàng rào trực tiếp.",
                "queries": [
                    "Lionel Messi preparing free kick ball grass",
                ],
            },
            {
                "text": "Theo thống kê từ LiveScore, vào năm 2017, Messi mới chỉ có 34 bàn đá phạt trực tiếp, kém rất xa con số 53 bàn của Cristiano Ronaldo thời điểm đó.",
                "queries": [
                    "Lionel Messi Cristiano Ronaldo El Clasico match",
                ],
            },
            {
                "text": "Thế nhưng nhờ khổ luyện hoàn thiện kỹ thuật cứa lòng đưa bóng cuộn qua hàng rào, Messi đã tạo nên màn bứt tốc ngoạn mục nhất lịch sử các tình huống cố định.",
                "queries": [
                    "Lionel Messi free kick over defensive wall goal",
                ],
            },
            {
                "text": "Tính đến cuối tháng 10 năm 2026, sau những siêu phẩm liên tiếp cho Inter Miami và Argentina, tổng số bàn thắng đá phạt trực tiếp của Messi đã lên tới 76 bàn — vượt xa 63 bàn của Ronaldo để độc chiếm vị trí thứ hai lịch sử thế giới.",
                "queries": [
                    "Lionel Messi free kick goal Argentina Ecuador",
                    "Lionel Messi Inter Miami free kick goal celebration",
                ],
            },
            {
                "text": "Theo Wisevoter, trước mắt Messi chỉ còn duy nhất kỷ lục thế giới 78 bàn đá phạt của cựu danh thủ Brazil Marcelinho Carioca — nghĩa là chỉ cần 2 cú sút phạt nữa, Messi sẽ san bằng kỷ lục vĩ đại nhất mọi thời đại.",
                "queries": [
                    "Lionel Messi free kick follow through shot",
                ],
            },
        ],
    },
    {
        "id": 6,
        "group": "Nhóm: Vinh Quang Albiceleste",
        "title": "Từ nước mắt thất bại đến chuỗi 4 danh hiệu lớn liên tiếp cùng Argentina",
        "title_queries": [
            "Lionel Messi World Cup 2022 trophy Lusail Argentina",
            "Lionel Messi Copa America 2021 trophy Maracana",
            "Lionel Messi Finalissima 2022 Wembley trophy",
        ],
        "sentences": [
            {
                "text": "Dù thâu tóm mọi vinh quang cấp câu lạc bộ, nhưng suốt hơn một thập kỷ đầu sự nghiệp, màu áo xanh trắng Albiceleste của đội tuyển Argentina từng là nỗi đau dai dẳng nhất trong tim Lionel Messi.",
                "queries": [
                    "Lionel Messi walking past World Cup trophy 2014 final",
                ],
            },
            {
                "text": "Anh từng gục ngã trong ba trận chung kết lớn liên tiếp chỉ trong ba năm: chung kết World Cup 2014 trước đội tuyển Đức, rồi hai trận chung kết Copa América 2015 và 2016 trước Chile trên chấm luân lưu.",
                "queries": [
                    "Lionel Messi sad Copa America 2016 final Chile",
                ],
            },
            {
                "text": "Đã có những giọt nước mắt rơi xuống vào năm 2016 khi anh nghẹn ngào nói lời chia tay đội tuyển vì nghĩ rằng vinh quang cùng Tổ quốc không dành cho mình.",
                "queries": [
                    "Lionel Messi emotional tears Argentina jersey",
                ],
            },
            {
                "text": "Nhưng một huyền thoại thực thụ không bao giờ đầu hàng — Messi quay trở lại, đeo băng đội trưởng và cùng tập thể chiến binh của huấn luyện viên Lionel Scaloni viết lại lịch sử.",
                "queries": [
                    "Lionel Messi and Lionel Scaloni hug Argentina",
                ],
            },
            {
                "text": "Tháng 7 năm 2021, ngay tại thánh địa Maracanã của đại kình địch Brazil, Argentina giành chiến thắng 1-0 để vô địch Copa América 2021 — giải tỏa cơn khát danh hiệu kéo dài 28 năm của cả dân tộc.",
                "queries": [
                    "Lionel Messi lifting Copa America 2021 trophy Brazil",
                ],
            },
            {
                "text": "Tháng 6 năm 2022 tại Wembley, Messi tỏa sáng với 2 kiến tạo giúp Argentina đè bẹp nhà vô địch châu Âu Italia 3-0 để đoạt cúp liên lục địa Finalissima.",
                "queries": [
                    "Argentina Finalissima 2022 Wembley celebration Messi",
                ],
            },
            {
                "text": "Và ngày 18 tháng 12 năm 2022 tại Qatar, trận chung kết vĩ đại nhất lịch sử bóng đá khép lại với chiến thắng nghẹt thở của Argentina trước Pháp sau loạt luân lưu định mệnh.",
                "queries": [
                    "Argentina World Cup 2022 final celebration Qatar Messi",
                ],
            },
            {
                "text": "Messi ghi 7 bàn, 3 kiến tạo, lập cú đúp ở chung kết và trở thành cầu thủ duy nhất trong lịch sử hai lần giành Quả Bóng Vàng World Cup — FIFA World Cup Golden Ball năm 2014 và 2022.",
                "queries": [
                    "Lionel Messi Golden Ball World Cup 2022 trophy kiss",
                ],
            },
            {
                "text": "Mùa hè năm 2024 trên đất Mỹ, anh tiếp tục cùng đồng đội đánh bại Colombia để bảo vệ ngôi vương Copa América 2024, hoàn tất chuỗi 4 danh hiệu lớn liên tiếp cùng đội tuyển quốc gia.",
                "queries": [
                    "Argentina Copa America 2024 trophy celebration Miami",
                ],
            },
        ],
    },
    {
        "id": 7,
        "group": "Nhóm: Khúc Tráng Ca World Cup 2026",
        "title": "Kỳ World Cup thứ 6, kỷ lục 21 bàn thắng và lời chia tay vĩ đại",
        "title_queries": [
            "Lionel Messi Argentina captain national anthem",
            "Lionel Messi World Cup goal celebration Argentina",
            "Lionel Messi waving goodbye Argentina fans",
        ],
        "sentences": [
            {
                "text": "Nhiều người từng nghĩ Copa América 2024 là giải đấu lớn cuối cùng của Lionel Messi trong màu áo đội tuyển, nhưng mùa hè năm 2026 trên đất Bắc Mỹ đã chứng kiến một khúc tráng ca còn hào hùng hơn thế.",
                "queries": [
                    "Argentina national team fans stadium blue white flags",
                ],
            },
            {
                "text": "Bước vào FIFA World Cup 2026 ở tuổi 39, Lionel Messi đi vào lịch sử khi góp mặt tại 6 kỳ World Cup liên tiếp từ năm 2006 đến năm 2026.",
                "queries": [
                    "Lionel Messi young World Cup 2006 Serbia goal",
                ],
            },
            {
                "text": "Anh đến Bắc Mỹ không phải để đóng vai biểu tượng tinh thần trên ghế dự bị, mà vẫn là nhạc trưởng dẫn dắt nhà đương kim vô địch thế giới tiến thẳng tới trận chung kết World Cup thứ hai liên tiếp.",
                "queries": [
                    "Lionel Messi dribbling Argentina World Cup match",
                ],
            },
            {
                "text": "Ngay tại vòng bảng gặp Algeria, theo Fox Sports, Messi đã làm nổ tung cầu trường khi lập cú hat-trick đầu tiên trong sự nghiệp tại đấu trường World Cup.",
                "queries": [
                    "Lionel Messi passionate goal celebration Argentina",
                ],
            },
            {
                "text": "Khép lại hành trình 7 trận đấu tại World Cup 2026, dù Argentina dừng bước ở vị trí Á quân sau trận chung kết kinh điển với Tây Ban Nha, màn trình diễn của người đội trưởng 39 tuổi vẫn khiến cả hành tinh nghiêng mình.",
                "queries": [
                    "Lionel Messi applauding Argentina fans stadium",
                    "Argentina national team lineup huddle Messi",
                ],
            },
            {
                "text": "Theo dữ liệu từ FIFA và FotMob, chỉ riêng tại World Cup 2026, Messi đã ghi tới 8 bàn thắng và đóng góp 4 đường kiến tạo — tổng cộng 12 lần in dấu giày vào bàn thắng.",
                "queries": [
                    "Lionel Messi celebration arms out Argentina crowd",
                ],
            },
            {
                "text": "Tám bàn thắng ấy đã nâng tổng số pha lập công của Messi qua 6 kỳ World Cup lên con số 21 bàn thắng sau 34 trận đấu.",
                "queries": [
                    "Lionel Messi kissing Argentina badge celebration",
                ],
            },
            {
                "text": "Với cột mốc này, Lionel Messi chính thức vượt qua kỷ lục 16 bàn của huyền thoại người Đức Miroslav Klose để độc chiếm ngôi vị Chân sút vĩ đại nhất lịch sử FIFA World Cup, trước khi khép lại sự nghiệp quốc tế ở kỷ lục 208 trận, 126 bàn thắng và 68 kiến tạo cho Argentina.",
                "queries": [
                    "Miroslav Klose World Cup goal record Germany",
                    "Lionel Messi emotional farewell Argentina Monumental",
                ],
            },
        ],
    },
    {
        "id": 8,
        "group": "Nhóm: Cơn Địa Chấn Nước Mỹ",
        "title": "Cải tổ Inter Miami, vô địch MLS Cup 2025, Golden Boot và sức hút tại Nu Stadium",
        "title_queries": [
            "Lionel Messi Inter Miami Supporters Shield trophy",
            "Lionel Messi Leagues Cup 2023 trophy lift Inter Miami",
            "Lionel Messi MLS MVP award Inter Miami",
        ],
        "sentences": [
            {
                "text": "Khi Lionel Messi rời Paris Saint-Germain mùa hè năm 2023 sau 2 chức vô địch Ligue 1 và 1 Siêu cúp Pháp để gia nhập Inter Miami CF, không ít ý kiến cho rằng anh đến nước Mỹ chỉ để dưỡng già.",
                "queries": [
                    "Lionel Messi Paris Saint Germain Ligue 1 celebration",
                    "Lionel Messi Inter Miami presentation unveiling rain",
                ],
            },
            {
                "text": "Thực tế diễn ra ngược lại: Messi tạo ra cuộc cách mạng lớn nhất lịch sử bóng đá Bắc Mỹ và biến đội bóng từng đứng chót bảng thành một đế chế chiến thắng.",
                "queries": [
                    "David Beckham and Lionel Messi Inter Miami hug",
                ],
            },
            {
                "text": "Chỉ vài tuần sau khi đến Florida năm 2023, anh ghi 10 bàn sau 7 trận để đưa Inter Miami vô địch Leagues Cup 2023 — danh hiệu đầu tiên trong lịch sử câu lạc bộ.",
                "queries": [
                    "Inter Miami Leagues Cup 2023 champions celebration Messi",
                ],
            },
            {
                "text": "Năm 2024, anh dẫn dắt đội bóng áo hồng giành MLS Supporters' Shield với kỷ lục điểm số lịch sử giải đấu và đoạt giải Cầu thủ xuất sắc nhất mùa.",
                "queries": [
                    "Lionel Messi lifting Supporters Shield 2024 Inter Miami",
                ],
            },
            {
                "text": "Nhưng đỉnh cao rực rỡ nhất của Messi tại Mỹ chính là hai mùa giải 2025 và 2026.",
                "queries": [
                    "Lionel Messi Luis Suarez Inter Miami celebration 2025",
                ],
            },
            {
                "text": "Theo trang chủ Inter Miami CF và Sports Illustrated, mùa giải MLS 2025, Messi ghi tới 29 bàn và 19 kiến tạo sau 28 trận mùa chính, đoạt cú đúp Chiếc Giày Vàng MLS Golden Boot 2025 và giải thưởng Landon Donovan MLS MVP.",
                "queries": [
                    "Lionel Messi MLS MVP trophy presentation Inter Miami",
                    "Lionel Messi shooting goal Inter Miami 2025",
                ],
            },
            {
                "text": "Tại chung kết MLS Cup 2025, Messi tỏa sáng với cú đúp kiến tạo giúp Inter Miami đánh bại Vancouver Whitecaps 3-1, lần đầu tiên nâng cao cúp vô địch MLS Cup và nhận giải MLS Cup Final MVP.",
                "queries": [
                    "Inter Miami trophy celebration confetti pink",
                ],
            },
            {
                "text": "Bước sang năm 2026 trên sân mới Nu Stadium, siêu sao 39 tuổi tiếp tục giành thêm Campeones Cup 2026 và ghi 25 bàn, 15 kiến tạo tại giải quốc nội — nâng tổng thành tích cho Inter Miami lên hơn 86 bàn thắng sau hơn 100 trận.",
                "queries": [
                    "Inter Miami Freedom Park stadium rendering night",
                    "Lionel Messi waving to fans Inter Miami stadium",
                ],
            },
        ],
    },
    {
        "id": 9,
        "group": "Nhóm: Tổng Kết Di Sản",
        "title": "Định nghĩa lại sự toàn diện và vị thế bất tử trong ngôi đền huyền thoại",
        "title_queries": [
            "Lionel Messi kissing World Cup trophy Qatar 2022",
            "Lionel Messi Barcelona Argentina Inter Miami legend",
            "Lionel Messi standing ovation stadium sunset",
        ],
        "sentences": [
            {
                "text": "Nhìn lại chặng đường hơn hai thập kỷ tính đến ngày 30 tháng 10 năm 2026, những gì Lionel Messi đạt được đã vượt xa khuôn khổ của những bảng thống kê thông thường.",
                "queries": [
                    "Lionel Messi looking at World Cup trophy Lusail",
                ],
            },
            {
                "text": "48 danh hiệu tập thể chính thức, 8 Quả Bóng Vàng Ballon d'Or, 8 giải FIFA The Best, 6 Chiếc Giày Vàng Châu Âu, 2 Quả Bóng Vàng World Cup, 1 cúp vàng World Cup, 2 Copa América, 4 Champions League, 10 La Liga và chức vô địch MLS Cup.",
                "queries": [
                    "Lionel Messi carried on shoulders Aguero World Cup",
                    "Lionel Messi Champions League trophy kiss 2015",
                ],
            },
            {
                "text": "936 bàn thắng, 466 đường kiến tạo, 1.402 lần đóng góp bàn thắng, 76 siêu phẩm đá phạt trực tiếp, 62 cú hat-trick và kỷ lục 21 bàn thắng tại FIFA World Cup.",
                "queries": [
                    "Lionel Messi celebration against Netherlands World Cup 2022",
                ],
            },
            {
                "text": "Trước khi Lionel Messi xuất hiện, lịch sử bóng đá luôn phân định rạch ròi: nếu bạn là một số 9 săn bàn vĩ đại như Gerd Müller hay Romário, bạn không phải người làm bóng; còn nếu bạn là một số 10 kiến thiết như Zinedine Zidane hay Andrés Iniesta, bạn không thể ghi 50 đến 90 bàn mỗi năm.",
                "queries": [
                    "Lionel Messi Andres Iniesta Barcelona midfield",
                    "Zinedine Zidane Real Madrid Champions League",
                ],
            },
            {
                "text": "Lionel Messi là người duy nhất xóa nhòa ranh giới ấy — anh vừa là số 9 xuất sắc nhất mọi thời đại trong vòng cấm, vừa là số 10 vĩ đại nhất lịch sử ở khu vực giữa sân, duy trì đỉnh cao suốt hơn 20 năm từ tuổi 17 đến tuổi 39.",
                "queries": [
                    "young Lionel Messi long hair Barcelona Ronaldinho",
                    "Lionel Messi captain Argentina smiling 2024",
                ],
            },
            {
                "text": "Bóng đá tương lai sẽ còn sản sinh ra những tài năng như Kylian Mbappé, Erling Haaland hay Lamine Yamal, nhưng để tìm ra một người thâu tóm 48 chiếc cúp và hơn 1.400 lần tạo ra bàn thắng như Lionel Messi — câu trả lời gần như là không thể.",
                "queries": [
                    "Lionel Messi and Kylian Mbappe World Cup 2022 final",
                    "Lionel Messi Lamine Yamal Barcelona",
                ],
            },
            {
                "text": "Nếu các bạn yêu mến những thước phim phân tích chuyên sâu về các huyền thoại bóng đá, hãy nhấn đăng ký kênh Điểm Đọc, bật chuông thông báo và để lại bình luận: khoảnh khắc nào của Lionel Messi khiến bạn xúc động nhất?",
                "queries": [
                    "Argentina fans celebrating Obelisco Buenos Aires World Cup",
                ],
            },
            {
                "text": "Điểm Đọc — đọc tin, hiểu chuyện, thấy tinh thần — xin chào và hẹn gặp lại!",
                "queries": [
                    "Lionel Messi walking into stadium light tunnel",
                ],
            },
        ],
    },
]

FALLBACK_QUERIES = [
    "Lionel Messi Argentina World Cup 2022 match photo",
    "Lionel Messi FC Barcelona La Liga action photo",
    "Lionel Messi Inter Miami CF MLS match action",
    "Lionel Messi UEFA Champions League Barcelona goal",
    "Lionel Messi Copa America Argentina captain",
    "Lionel Messi Ballon d'Or ceremony Paris",
    "Lionel Messi Camp Nou celebration crowd",
    "Lionel Messi Argentina celebration Lusail Stadium",
]

# ------------------------------------------------------------------ CẤU HÌNH LỌC ẢNH
MIN_RATIO = 1.18        # ảnh ngang chuẩn 16:9
MIN_WIDTH = 800         # độ phân giải tối thiểu
NEG_KW = " -game -mobile -esports -wallpaper -pes -fifa23 -eafc"
BLOCKED_HOSTS = [
    "alamy", "gettyimages", "istockphoto", "shutter", "dreamstime", "123rf",
    "depositphotos", "stock.adobe", "freepik", "pinterest", "facebook.",
    "instagram.", "tiktok", "wallpaper", "alphacoders", "deviantart",
    "futbin", "futhead", "sofifa", "vectorstock", "storyblocks", "picfair",
    "vecteezy", "bigstock", "ebay", "etsy", "redbubble", "teepublic",
    "society6", "displate", "ytimg", "pngtree", "cgtrader", "footyheadlines",
    "webcamsus", "twimg", "idman.biz", "hudl", "videoblocks", "ftcdn",
    "fotolia", "huggingface", "hf.co", "pond5", "mixkit", "motionarray",
    "collage", "forum", "pinimg",
    # Chặn từ vòng QA 1 (ảnh ghép, đồ họa, screenshot, AI, off-topic):
    "chatgpt", "screen_shot", "screenshot", "illustration", "sequence",
    "givemesportimages", "hindustanherald", "soccerleagueclub",
    "futbolchronicle", "amarujala", "brobible", "static-media.fox.com",
    "messi-fifpro.jpg", "origin-imgresizer.eurosport.com", "bnews.com.br",
    "the18.com", "16894585691343", "0f5e1f1b-9bcd-44b5-a597",
    "vantailogistic", "khacdautn", "1cdn.vn", "tapchidongnama",
    "centralretail", "giaoducthoidai",
    "bdo-messi-2009", "messi-xavi-march", "kq2.com", "motionbgs",
    "khelnow", "16713930580033",
]
RELEVANT_TERMS = (
    "messi", "barcelona", "barca", "argentina", "miami", "ballon",
    "world cup", "world-cup", "worldcup", "champions", "camp nou", "camp-nou",
    "cruyff", "muller", "zidane", "iniesta", "klose", "ronaldo", "maradona",
    "scaloni", "beckham", "suarez", "neymar", "guardiola", "copa", "mls",
    "golden shoe", "golden-shoe", "pichichi", "lusail", "wembley", "maracana",
)
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


# ------------------------------------------------------------------ TIỆN ÍCH
def wc(text):
    return len(text.split())


def n_images_for(text):
    n = wc(text)
    if n < 42:
        return 1, "NGẮN", n
    if n <= 65:
        return 2, "VỪA", n
    return 3, "DÀI", n


def ahash(img):
    g = img.convert("L").resize((8, 8), Image.LANCZOS)
    px = list(g.tobytes())
    m = sum(px) / 64.0
    bits = 0
    for p in px:
        bits = (bits << 1) | (1 if p > m else 0)
    return bits


def hamming(a, b):
    return bin(a ^ b).count("1")


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default
    return default


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                    encoding="utf-8")


def host_blocked(url):
    low = url.lower()
    return any(b in low for b in BLOCKED_HOSTS) or "watermark" in low


def safe_trash(path: Path):
    if not path.exists():
        return
    dst = TRASH_DIR / f"{path.stem}_{int(time.time()*1000)}{path.suffix}"
    shutil.move(str(path), str(dst))


def sort_key_tin(path: Path):
    parts = path.stem.split("_")
    try:
        return (int(parts[1]), int(parts[2]))
    except Exception:
        return (999, 999)


# ------------------------------------------------------------------ KẾ HOẠCH ẢNH
def build_plan():
    """Sinh danh sách slot ảnh theo luật độ dài câu."""
    plan = []
    for sc in SCENES:
        sid = sc["id"]
        idx = 1

        def fname():
            nonlocal idx
            f = f"Tin_{sid:02d}_{idx}.jpg"
            idx += 1
            return f

        for q in sc["title_queries"]:
            plan.append(dict(scene=sid, sent_idx=0, kind="title",
                             label="TIÊU ĐỀ", query=q, fname=fname(), wc=0))
        for i, s in enumerate(sc["sentences"], start=1):
            n, lab, words = n_images_for(s["text"])
            qs = list(s["queries"])
            while len(qs) < n:
                qs.append(qs[len(qs) % max(1, len(s["queries"]))] + " football editorial")
            for j in range(n):
                plan.append(dict(scene=sid, sent_idx=i, kind="sentence",
                                 label=lab, query=qs[j], fname=fname(), wc=words))
    return plan


def write_kich_ban(plan):
    lines = []
    lines.append("=" * 80)
    lines.append("KỊCH BẢN PHÂN TÁCH TỪNG CÂU & KẾ HOẠCH HÌNH ẢNH — NGÀY 30.10.2026")
    lines.append(f"Chủ đề: Chuyên đề Lionel Messi — \"{VIDEO_TITLE}\"")
    lines.append("Quy tắc ảnh: Tiêu đề = 3 ảnh | Câu ngắn (< 42 từ) = 1 ảnh | "
                 "Câu vừa (42–65 từ) = 2 ảnh | Câu dài (> 65 từ) = 3 ảnh")
    lines.append("=" * 80)
    by_scene = {}
    for p in plan:
        by_scene.setdefault(p["scene"], []).append(p)
    for sc in SCENES:
        sid = sc["id"]
        lines.append("")
        lines.append("#" * 80)
        lines.append(f"CẢNH {sid:02d}: {sc['group'].upper()}")
        lines.append("#" * 80)
        lines.append("")
        slots = by_scene[sid]
        title_slots = [p for p in slots if p["kind"] == "title"]
        lines.append(f"★ TIÊU ĐỀ: \"{sc['title']}\"")
        lines.append("   - Yêu cầu: 3 ảnh")
        lines.append("   - Tên ảnh: " + ", ".join(p["fname"] for p in title_slots))
        for i, s in enumerate(sc["sentences"], start=1):
            sl = [p for p in slots if p["sent_idx"] == i]
            if not sl:
                continue
            p0 = sl[0]
            lines.append("")
            lines.append(f"▶ CÂU {i:02d} [{p0['label']} ({p0['wc']} từ) — "
                         f"{len(sl)} ảnh]:")
            lines.append(f"   \"{s['text']}\"")
            lines.append("   - Tên ảnh: " + ", ".join(p["fname"] for p in sl))
        lines.append("")
        lines.append(f">>> TỔNG CỘNG CẢNH {sid:02d}: {len(slots)} ẢNH")
    total = len(plan)
    lines.append("")
    lines.append("=" * 80)
    lines.append(f"TỔNG CỘNG TOÀN VIDEO: {total} ẢNH")
    lines.append("=" * 80)
    (DAY / "kich_ban_tung_cau.txt").write_text("\n".join(lines),
                                               encoding="utf-8")
    return total


def write_thethao_txt():
    lines = [f"BẢN TIN THỂ THAO — CHUYÊN ĐỀ LIONEL MESSI — 30.10.2026",
             f"TIÊU ĐỀ VIDEO: {VIDEO_TITLE}", ""]
    for sc in SCENES:
        lines.append("=" * 70)
        lines.append(f"CẢNH {sc['id']:02d} — {sc['group']} — {sc['title']}")
        lines.append("=" * 70)
        for s in sc["sentences"]:
            lines.append(s["text"])
            lines.append("")
    (DAY / "thethao.txt").write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------------ TẢI ẢNH
class Hunter:
    def __init__(self):
        self.qcache = load_json(QCACHE, {})
        self.used_hashes = []
        self.plan_log = []
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": UA})

    def search(self, query):
        key = "usen|" + query + "|" + NEG_KW
        if key in self.qcache and self.qcache[key]:
            return self.qcache[key]
        for attempt in range(4):
            try:
                with DDGS() as ddgs:
                    res = ddgs.images(query + NEG_KW, region="us-en",
                                      safesearch="off", size="Large",
                                      layout="Wide", max_results=35)
                res = list(res)
                if res:
                    self.qcache[key] = res
                    save_json(QCACHE, self.qcache)
                return res
            except Exception as e:
                wait = 6 * (attempt + 1)
                print(f"    [search retry {attempt+1}] {type(e).__name__}: {e} -> sleep {wait}s", flush=True)
                time.sleep(wait)
        return []

    def fetch(self, url):
        if host_blocked(url):
            return None
        low = url.lower().split("?")[0]
        if low.endswith((".svg", ".gif")):
            return None
        try:
            r = self.session.get(url, timeout=14, stream=False)
            if r.status_code != 200 or len(r.content) < 25_000:
                return None
            img = Image.open(io.BytesIO(r.content))
            img.load()
            w, h = img.size
            if w < MIN_WIDTH or h == 0 or (w / h) < MIN_RATIO:
                return None
            if img.mode != "RGB":
                img = img.convert("RGB")
            return img
        except Exception:
            return None

    def try_candidates(self, slot, query, used_map):
        out_path = IMG_DIR / slot["fname"]
        cands = self.search(query)

        def rank(c):
            try:
                w = int(c.get("width") or 0)
                h = int(c.get("height") or 0)
                return (0 if (w and w / max(h, 1) >= MIN_RATIO) else 1, -w)
            except Exception:
                return (1, 0)

        cands = sorted(cands, key=rank)
        for c in cands:
            url = c.get("image") or ""
            if not url.startswith("http"):
                continue
            blob = f"{c.get('title', '')} {url} {c.get('source', '')}".lower()
            if not any(t in blob for t in RELEVANT_TERMS):
                continue
            img = self.fetch(url)
            if img is None:
                continue
            h_val = ahash(img)
            dup = False
            for fn, uh in used_map:
                if hamming(h_val, uh) <= 6:
                    dup = True
                    break
            if dup:
                continue
            img.save(out_path, "JPEG", quality=88)
            used_map.append((slot["fname"], h_val))
            self.plan_log.append(dict(
                fname=slot["fname"], scene=slot["scene"],
                sent_idx=slot["sent_idx"], kind=slot["kind"],
                query=query, source=url,
                source_site=c.get("source", ""),
                width=img.size[0], height=img.size[1]))
            return True
        return False

    def fill_slot(self, slot, used_map):
        out_path = IMG_DIR / slot["fname"]
        if out_path.exists():
            return "kept"
        query = slot["query"]
        if self.try_candidates(slot, query, used_map):
            return "ok"
        for fb in FALLBACK_QUERIES:
            if self.try_candidates(slot, fb, used_map):
                return "ok"
        return "MISSING"


# ------------------------------------------------------------------ CONTACT SHEET
def make_sheets():
    files = sorted(IMG_DIR.glob("Tin_*.jpg"), key=sort_key_tin)
    by_scene = {}
    for f in files:
        sid = int(f.name.split("_")[1])
        by_scene.setdefault(sid, []).append(f)
    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    except Exception:
        font = ImageFont.load_default()
    for sid, fs in by_scene.items():
        cols, tw = 5, 320
        th = int(tw * 9 / 16)
        rows = (len(fs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (tw + 8) + 8,
                                  rows * (th + 30 + 8) + 8), (18, 18, 22))
        d = ImageDraw.Draw(sheet)
        for i, f in enumerate(fs):
            r, c = divmod(i, cols)
            x = 8 + c * (tw + 8)
            y = 8 + r * (th + 30 + 8)
            try:
                im = Image.open(f)
                im.thumbnail((tw, th))
                sheet.paste(im, (x, y))
            except Exception:
                pass
            d.text((x + 2, y + th + 4), f.name, fill=(255, 210, 90), font=font)
        out = QA_DIR / f"contact_C{sid:02d}.jpg"
        sheet.save(out, "JPEG", quality=85)
        print(f"  sheet: {out.name} ({len(fs)} ảnh)")


def sync_thethao_json():
    items = []
    for sc in SCENES:
        sid = sc["id"]
        imgs = sorted(IMG_DIR.glob(f"Tin_{sid:02d}_*.jpg"), key=sort_key_tin)
        item = dict(
            id=sid, art_id=f"art_{sid:02d}", group=sc["group"],
            title=sc["title"],
            summary=" ".join(s["text"] for s in sc["sentences"]),
            audio_path=str(DAY / "audio" / f"audio_{sid:02d}.wav"),
            audio_title=str(DAY / "audio-title" / f"audio_title_{sid:02d}.wav"),
            image_path=str(imgs[0]) if imgs else "",
            digest_line=sc["title"])
        for k, f in enumerate(imgs, 1):
            item[f"image_{k}"] = str(f)
        items.append(item)
    save_json(DAY / "thethao.json", items)


# ------------------------------------------------------------------ MAIN
def main():
    args = sys.argv[1:]
    if "--sheets" in args:
        sync_thethao_json()
        make_sheets()
        return

    force = "--force" in args
    if force:
        for f in IMG_DIR.glob("Tin_*.jpg"):
            safe_trash(f)

    plan = build_plan()
    total = write_kich_ban(plan)
    write_thethao_txt()
    print(f"[PLAN] {total} slot ảnh | kich_ban_tung_cau.txt + thethao.txt đã ghi", flush=True)

    hunter = Hunter()
    used_map = []
    for f in sorted(IMG_DIR.glob("Tin_*.jpg"), key=sort_key_tin):
        try:
            used_map.append((f.name, ahash(Image.open(f))))
        except Exception:
            pass
    print(f"[RESUME] {len(used_map)} ảnh đã có sẵn", flush=True)

    ok = miss = kept = 0
    t0 = time.time()
    for i, slot in enumerate(plan, 1):
        st = hunter.fill_slot(slot, used_map)
        if st == "ok":
            ok += 1
        elif st == "kept":
            kept += 1
        else:
            miss += 1
            print(f"  !! MISSING {slot['fname']} (cảnh {slot['scene']}, "
                  f"câu {slot['sent_idx']}) — query: {slot['query']}", flush=True)
        if i % 10 == 0 or i == len(plan):
            print(f"[{i}/{len(plan)}] ok={ok} kept={kept} missing={miss} "
                  f"({time.time()-t0:.0f}s)", flush=True)
        if st != "kept":
            time.sleep(0.3)

    plan_path = DAY / "image_plan.json"
    prev = load_json(plan_path, {})
    prev_slots = {s["fname"]: s for s in prev.get("slots", [])}
    for s in hunter.plan_log:
        prev_slots[s["fname"]] = s
    save_json(plan_path, dict(
        video_title=VIDEO_TITLE, day="30.10.2026",
        total_slots=len(plan), downloaded=ok, kept=kept, missing=miss,
        slots=list(prev_slots.values())))

    sync_thethao_json()
    make_sheets()
    print(f"[DONE] ok={ok} kept={kept} missing={miss} / {len(plan)} "
          f"trong {time.time()-t0:.0f}s", flush=True)
    print(f"[ARTIFACT] {DAY / 'kich_ban_tung_cau.txt'}")
    print(f"[ARTIFACT] {DAY / 'thethao.json'} + thethao.txt + image_plan.json")
    print(f"[QA] Contact sheets: {QA_DIR}")


if __name__ == "__main__":
    main()
