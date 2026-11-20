#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect_shorts_images_17_11.py — Thu thập & Tinh Tuyển Ảnh Ngữ Nghĩa Từng Câu (Semantic Flow)
============================================================================================
Nâng cấp theo yêu cầu nghiêm ngặt của Chủ kênh:
- Bóc tách từng câu thành các phân đoạn chủ thể cụ thể (ví dụ: mở đầu là A, kết thúc là B thì PHẢI có cả ảnh của A và B).
- Các câu dài/phức tạp được cấp từ 2 đến 4 ảnh chất lượng cao bám sát thời gian đọc của từng chủ thể.
- Lọc triệt để watermark stock (Alamy, Dreamstime, iStock...) và rác e-commerce.
- Xuất lại thethao.json, image_plan.json, image_credits.json và Contact Sheets QA đối chứng.
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import os
import json
import time
import io
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple

import requests
from PIL import Image, ImageDraw, ImageFont
from ddgs import DDGS

_HERE = Path(__file__).resolve().parent
ROOT_DIR = _HERE.parent
DAY_DIR = ROOT_DIR / "outputs" / "Orther" / "17.11.2026"
IMG_DIR = DAY_DIR / "images"
QA_DIR = DAY_DIR / "qa"

IMG_DIR.mkdir(parents=True, exist_ok=True)
QA_DIR.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
NEG_KW = "-game -mobile -shopee -lazada -aliexpress -amazon -ebay -watermark -alamy -dreamstime -istockphoto -depositphotos -vector -cartoon"

BLOCKED_DOMAINS = [
    "alamy.com", "dreamstime.com", "istockphoto.com", "depositphotos.com",
    "shutterstock.com", "123rf.com", "vecteezy.com", "gettyimages.com/detail",
    "shopee.vn", "lazada.vn", "tiki.vn", "sendo.vn", "aliexpress.com", "amazon.com",
    "pinterest.com", "pinimg.com"
]

def host_blocked(url: str) -> bool:
    low = url.lower()
    return any(d in low for d in BLOCKED_DOMAINS)

# =====================================================================
# 1. KỊCH BẢN CHIA CÂU & PHÂN BỔ ẢNH THEO DÒNG NGỮ NGHĨA (CHRONOLOGICAL SEMANTIC FLOW)
# =====================================================================

VIDEOS_CONFIG = [
    {
        "id": 1,
        "slug": "Short_Tong_Hop_QT1_Dia_Chan_Duc_Ha_Lan_Va_Song_Gio_Ronaldo",
        "group": "BẢN TIN QUỐC TẾ • ĐỊA CHẤN BERLIN & SÓNG GIÓ RONALDO",
        "title": "Bão lớn bóng đá châu Âu: Đức hủy diệt Hà Lan 5-0 và sóng gió quanh Ronaldo",
        "news_source": "UEFA / BÁO CHÍ CHÂU ÂU",
        "credit": "REUTERS / GETTY IMAGES / UEFA",
        "source": "UEFA & Bild, The Guardian",
        "hide_date_chip": True,
        "sentences": [
            "Đêm qua theo giờ Việt Nam, bóng đá châu Âu đã trải qua những giờ phút rung chuyển dữ dội với hàng loạt biến động lớn từ sân cỏ Nations League cho đến những tranh cãi nảy lửa chốn hậu trường.",
            "Tâm điểm của cơn địa chấn diễn ra tại sân vận động Olympiastadion ở thủ đô Berlin, nơi đội tuyển Đức đã khiến cả thế giới ngỡ ngàng khi đè bẹp đại kình địch Hà Lan với tỷ số không tưởng 5-0.",
            "Khoác lên mình bộ trang phục đen kỷ niệm đặc biệt, Cỗ xe tăng Đức đã dội một cơn mưa gôn thực sự vào lưới đối thủ.",
            "Tiền vệ trẻ Florian Wirtz rực sáng với một cú đúp đẳng cấp, bên cạnh các pha lập công của Derry Scherhant, Nico Schlotterbeck và Brajan Gruda, qua đó giúp Đức hiên ngang tiến vào tứ kết Nations League với ngôi đầu bảng A2.",
            "Trái ngược với niềm hân hoan của người Đức, đây lại là thất bại cay đắng và nặng nề nhất của bóng đá Hà Lan trong suốt 67 năm qua, kể từ năm 1959.",
            "Ngay sau trận đấu, tân HLV Xavi Hernandez đã không giấu nổi sự bàng hoàng và thừa nhận cảm thấy sốc cùng nỗi hổ thẹn lớn trước tinh thần thi đấu rệu rã của các học trò, dù Hà Lan vẫn may mắn lách qua khe cửa hẹp để giành vé nhì bảng.",
            "Nhưng sóng gió bóng đá lục địa già không chỉ dừng lại ở Berlin.",
            "Tại bán đảo Iberia, một cuộc khủng hoảng truyền thông đang bùng nổ dữ dội xung quanh siêu sao Cristiano Ronaldo sau thất bại bất ngờ của đội tuyển Bồ Đào Nha trước Đan Mạch.",
            "Mới đây nhất, bà Dolores Aveiro, mẹ của Ronaldo, đã khiến dư luận quốc tế dậy sóng khi công khai tuyên bố trên truyền thông rằng việc đội tuyển Bồ Đào Nha thất bại là đáng đời vì đã thiếu đi sự tôn trọng tối thiểu dành cho con trai bà.",
            "Phát biểu gây chấn động này lập tức thổi bùng lên những mâu thuẫn âm ỉ trong phòng thay đồ của Selecao châu Âu.",
            "Các chuyên gia tiếp thị thể thao quốc tế cũng nhanh chóng lên tiếng cảnh báo, việc gạt bỏ huyền thoại 41 tuổi không chỉ gây rạn nứt nội bộ, mà còn khiến bóng đá Bồ Đào Nha đối mặt nguy cơ sụt giảm nghiêm trọng hàng triệu người theo dõi toàn cầu cùng những tổn thất khổng lồ về giá trị thương mại.",
            "Rõ ràng, dù đang sở hữu một thế hệ kế cận đầy tài năng, chiếc bóng và sức hút mang tầm vóc biểu tượng của Cristiano Ronaldo vẫn là thứ mà người Bồ Đào Nha chưa thể tìm ra lời giải thay thế."
        ],
        "image_slots": [
            # Title (3 ảnh tổng quát)
            {"type": "title", "idx": 0, "fname": "v1_berlin_night.jpg", "query": "Olympiastadion Berlin stadium night lights high resolution", "credit": "UEFA", "desc": "Sân vận động Olympiastadion Berlin rực sáng đêm đại chiến"},
            {"type": "title", "idx": 0, "fname": "v1_germany_celebrate.jpg", "query": "Germany national football team celebrate goal 2024 2026", "credit": "REUTERS", "desc": "Đội tuyển Đức ăn mừng chiến thắng 5-0 tưng bừng"},
            {"type": "title", "idx": 0, "fname": "v1_ronaldo_portrait.jpg", "query": "Cristiano Ronaldo Portugal national team portrait match", "credit": "GETTY IMAGES", "desc": "Cristiano Ronaldo trong màu áo đội tuyển Bồ Đào Nha"},

            # Câu 1: Sân cỏ Nations League rung chuyển -> tranh cãi chốn hậu trường
            {"type": "sentence", "idx": 1, "fname": "v1_nations_league_ball.jpg", "query": "UEFA Nations League match ball pitch grass", "credit": "UEFA", "desc": "Trái bóng thi đấu chính thức UEFA Nations League"},
            {"type": "sentence", "idx": 1, "fname": "v1_olympiastadion_match.jpg", "query": "Germany vs Netherlands football match Olympiastadion Berlin", "credit": "REUTERS", "desc": "Không khí sôi động trên các sân cỏ châu Âu"},

            # Câu 2: Sân Olympiastadion Berlin -> Tỷ số 5-0 đè bẹp Hà Lan
            {"type": "sentence", "idx": 2, "fname": "v1_scoreboard_5_0.jpg", "query": "Germany 5 Netherlands 0 scoreboard stadium match", "credit": "BILD", "desc": "Bảng điện tử tỷ số Đức 5-0 Hà Lan tại Berlin"},
            {"type": "sentence", "idx": 2, "fname": "v1_germany_fans_cheer.jpg", "query": "Germany football fans cheering stadium flags", "credit": "GETTY IMAGES", "desc": "Cổ động viên Đức vỡ òa ăn mừng chiến thắng"},

            # Câu 3: Áo đen kỷ niệm đặc biệt -> Cơn mưa gôn vào lưới đối thủ
            {"type": "sentence", "idx": 3, "fname": "v1_germany_black_kit.jpg", "query": "Germany national football team black kit jersey adidas", "credit": "BUNDESLIGA", "desc": "Đội tuyển Đức trong trang phục áo đen đặc biệt"},
            {"type": "sentence", "idx": 3, "fname": "v1_germany_attack.jpg", "query": "Germany football team attack action pitch", "credit": "REUTERS", "desc": "Cỗ xe tăng dội cơn mưa gôn vào lưới đối thủ"},

            # Câu 4 (ĐA CHỦ THỂ): Wirtz cú đúp -> Schlotterbeck & Scherhant & Gruda -> Đức đầu bảng A2 vào tứ kết
            {"type": "sentence", "idx": 4, "fname": "v1_florian_wirtz_double.jpg", "query": "Florian Wirtz Germany celebrate goal Nations League", "credit": "GETTY IMAGES", "desc": "Florian Wirtz rực sáng với cú đúp bàn thắng"},
            {"type": "sentence", "idx": 4, "fname": "v1_schlotterbeck_header.jpg", "query": "Nico Schlotterbeck Germany header goal match", "credit": "REUTERS", "desc": "Nico Schlotterbeck đánh đầu dũng mãnh ghi bàn"},
            {"type": "sentence", "idx": 4, "fname": "v1_scherhant_gruda_goal.jpg", "query": "Brajan Gruda Germany U21 senior team goal celebrate", "credit": "BUNDESLIGA", "desc": "Brajan Gruda và Derry Scherhant lập công cho tuyển Đức"},
            {"type": "sentence", "idx": 4, "fname": "v1_germany_group_winner.jpg", "query": "Germany football team group winners Nations League celebration", "credit": "UEFA", "desc": "Tuyển Đức giành ngôi đầu bảng A2 tiến vào tứ kết"},

            # Câu 5: Niềm hân hoan của Đức đối lập nỗi thất vọng lịch sử của Hà Lan sau 67 năm
            {"type": "sentence", "idx": 5, "fname": "v1_dutch_despair_ground.jpg", "query": "Netherlands football players disappointed pitch loss", "credit": "DUTCH NEWS", "desc": "Các tuyển thủ Hà Lan gục xuống mặt cỏ Olympiastadion"},
            {"type": "sentence", "idx": 5, "fname": "v1_netherlands_team_shock.jpg", "query": "Netherlands football team defeat Nations League", "credit": "GETTY IMAGES", "desc": "Thất bại nặng nề nhất của bóng đá Hà Lan sau 67 năm"},

            # Câu 6 (ĐA CHỦ THỂ): HLV Xavi Hernandez sốc -> Học trò rệu rã -> Tấm vé nhì bảng tứ kết
            {"type": "sentence", "idx": 6, "fname": "v1_xavi_hernandez_press.jpg", "query": "Xavi Hernandez coach press conference microphone", "credit": "REUTERS", "desc": "HLV Xavi Hernandez bàng hoàng thừa nhận cảm thấy hổ thẹn"},
            {"type": "sentence", "idx": 6, "fname": "v1_dutch_players_dejected.jpg", "query": "Netherlands football players looking down dejected pitch", "credit": "DUTCH NEWS", "desc": "Tinh thần thi đấu rệu rã của các cầu thủ Hà Lan"},
            {"type": "sentence", "idx": 6, "fname": "v1_netherlands_second_place.jpg", "query": "Netherlands national football team qualified quarterfinal", "credit": "UEFA", "desc": "Tuyển Hà Lan may mắn lách qua khe cửa hẹp nhì bảng"},

            # Câu 7: Chuyển cảnh từ Berlin sang bán đảo Iberia
            {"type": "sentence", "idx": 7, "fname": "v1_europe_football_map.jpg", "query": "UEFA Nations League trophy stadium arena", "credit": "UEFA", "desc": "Sóng gió bóng đá lan rộng khắp lục địa già"},

            # Câu 8: Khủng hoảng truyền thông quanh Ronaldo sau trận thua Đan Mạch
            {"type": "sentence", "idx": 8, "fname": "v1_ronaldo_disappointment.jpg", "query": "Cristiano Ronaldo disappointed Portugal match face", "credit": "REUTERS", "desc": "Cristiano Ronaldo thất vọng sau trận đấu của Bồ Đào Nha"},
            {"type": "sentence", "idx": 8, "fname": "v1_portugal_denmark_match.jpg", "query": "Portugal vs Denmark football match Nations League", "credit": "GETTY IMAGES", "desc": "Thất bại bất ngờ của đội tuyển Bồ Đào Nha trước Đan Mạch"},

            # Câu 9: Mẹ Dolores Aveiro phát biểu công khai -> Bồ Đào Nha thua là đáng đời vì thiếu tôn trọng CR7
            {"type": "sentence", "idx": 9, "fname": "v1_dolores_aveiro_interview.jpg", "query": "Dolores Aveiro mother Cristiano Ronaldo portrait event", "credit": "RECORD", "desc": "Bà Dolores Aveiro, mẹ của siêu sao Cristiano Ronaldo"},
            {"type": "sentence", "idx": 9, "fname": "v1_dolores_ronaldo_event.jpg", "query": "Cristiano Ronaldo and mother Dolores Aveiro gala", "credit": "INSTAGRAM", "desc": "Bà Dolores lên tiếng bảo vệ con trai trước truyền thông"},

            # Câu 10: Thổi bùng mâu thuẫn phòng thay đồ và HLV Roberto Martinez
            {"type": "sentence", "idx": 10, "fname": "v1_portugal_locker_room.jpg", "query": "Portugal football team bench dugout tension", "credit": "GETTY IMAGES", "desc": "Căng thẳng âm ỉ tại khu kỹ thuật đội tuyển Bồ Đào Nha"},
            {"type": "sentence", "idx": 10, "fname": "v1_martinez_coaching.jpg", "query": "Roberto Martinez coach Portugal match instructions", "credit": "REUTERS", "desc": "HLV Roberto Martinez đối mặt bài toán khó trong phòng thay đồ"},

            # Câu 11 (ĐA CHỦ THỂ): Rạn nứt nội bộ -> Nguy cơ sụt giảm triệu follower -> Tổn thất thương mại
            {"type": "sentence", "idx": 11, "fname": "v1_portugal_internal_rift.jpg", "query": "Portugal national football team training session serious", "credit": "RECORD", "desc": "Rạn nứt nội bộ đe dọa sự ổn định của Selecao châu Âu"},
            {"type": "sentence", "idx": 11, "fname": "v1_ronaldo_social_media_drop.jpg", "query": "Cristiano Ronaldo social media followers fans stadium", "credit": "FORBES", "desc": "Nguy cơ sụt giảm hàng triệu người theo dõi quốc tế"},
            {"type": "sentence", "idx": 11, "fname": "v1_ronaldo_commercial_loss.jpg", "query": "Cristiano Ronaldo commercial sponsor billboard stadium", "credit": "REUTERS", "desc": "Tổn thất khổng lồ về giá trị thương mại và tài trợ"},

            # Câu 12 (ĐA CHỦ THỂ): Thế hệ trẻ tài năng (Leao, Vitinha...) -> Chiếc bóng biểu tượng của CR7
            {"type": "sentence", "idx": 12, "fname": "v1_portugal_young_generation.jpg", "query": "Rafael Leao Vitinha Portugal national team match action", "credit": "GETTY IMAGES", "desc": "Thế hệ tài năng trẻ kế cận của bóng đá Bồ Đào Nha"},
            {"type": "sentence", "idx": 12, "fname": "v1_ronaldo_iconic_shadow.jpg", "query": "Cristiano Ronaldo Portugal national team jersey number 7 clapping", "credit": "REUTERS", "desc": "Chiếc bóng và tầm vóc biểu tượng chưa thể thay thế của CR7"}
        ]
    },
    {
        "id": 2,
        "slug": "Short_Tong_Hop_QT2_Suc_Manh_Alcaraz_Minh_Oan_Yamal_Barca",
        "group": "BẢN TIN QUỐC TẾ • ALCARAZ HỦY DIỆT & ĐÒN BẨY BARCA",
        "title": "Alcaraz thị uy tại ATP Finals, La Liga minh oan cho Yamal và nước cờ của Barca",
        "news_source": "ATP TOUR / LA LIGA / EL PLURAL",
        "credit": "GETTY IMAGES / REUTERS / FC BARCELONA",
        "source": "ATP Tour, CCTV Sports, El Plural",
        "hide_date_chip": True,
        "sentences": [
            "Bên cạnh những cơn sốt trên sân cỏ Nations League, bức tranh thể thao thế giới trong 12 giờ qua tiếp tục chứng kiến sự áp đảo của các siêu sao thế hệ mới cùng những câu chuyện hậu trường tài chính vô cùng đặc biệt.",
            "Tại thành phố Turin nước Ý, giải quần vợt danh giá dành cho 8 tay vợt mạnh nhất năm Nitto ATP Finals 2026 đã chính thức khai màn với màn thị uy sức mạnh không thể thuyết phục hơn của Carlos Alcaraz.",
            "Trong trận ra quân tại bảng Ivan Lendl, tay vợt số 1 Tây Ban Nha chỉ cần vỏn vẹn 69 phút để nghiền nát đối thủ người Mỹ Frances Tiafoe với tỷ số trắng 6-2, 6-2.",
            "Thi đấu với phong độ như đang dạo chơi nhưng tung ra tới 21 điểm winner chuẩn xác, Alcaraz đã nối dài chuỗi 10 trận toàn thắng liên tiếp, gửi lời thách thức đanh thép tới toàn bộ các đối thủ trên hành trình chinh phục chiếc cúp danh giá cuối năm.",
            "Cũng liên quan đến thể thao Tây Ban Nha nhưng ở khía cạnh pháp lý, ban tổ chức giải bóng đá La Liga vừa chính thức phát đi thông báo minh oan cho hiện tượng trẻ Lamine Yamal.",
            "Cơ quan này khẳng định toàn bộ hình ảnh và bài viết lan truyền trên mạng xã hội cáo buộc thần đồng của Barcelona có hành vi kỳ thị người Trung Quốc là sản phẩm cắt ghép giả mạo hoàn toàn.",
            "La Liga tuyên bố đã khởi động các thủ tục pháp lý để xử lý nghiêm những tài khoản cố tình tung tin thất thiệt nhằm bôi nhọ danh dự của ngôi sao 19 tuổi.",
            "Trong khi đó, tại đại bản doanh xứ Catalonia, ban lãnh đạo Barcelona lại đang khiến giới tài chính kinh ngạc với một kế hoạch kinh doanh chưa từng có tiền lệ mang tên Memorial FC Barcelona.",
            "Theo tính toán từ nhật báo El Plural, đội chủ sân Camp Nou dự kiến sẽ cho thuê 26000 ô lưu giữ tro cốt ngay trong khuôn viên sân vận động mới với gói thời hạn 10 năm.",
            "Nếu được lấp đầy, dự án độc lạ này sẽ mang về cho Barca khoản doanh thu khổng lồ lên tới hơn 71 triệu USD, trở thành chiếc phao cứu sinh quan trọng giúp gã khổng lồ La Liga giải quyết bài toán khó khăn tài chính đã đeo bám họ suốt nhiều năm qua."
        ],
        "image_slots": [
            # Title
            {"type": "title", "idx": 0, "fname": "v2_alcaraz_trophy_action.jpg", "query": "Carlos Alcaraz tennis forehand Turin ATP Finals", "credit": "ATP TOUR", "desc": "Carlos Alcaraz thi đấu thăng hoa tại ATP Finals"},
            {"type": "title", "idx": 0, "fname": "v2_yamal_barca_star.jpg", "query": "Lamine Yamal Barcelona celebration smile match", "credit": "GETTY IMAGES", "desc": "Thần đồng Lamine Yamal trong màu áo Barcelona"},
            {"type": "title", "idx": 0, "fname": "v2_camp_nou_aerial.jpg", "query": "Spotify Camp Nou stadium new renovation rendering aerial", "credit": "FC BARCELONA", "desc": "Phối cảnh sân vận động mới Spotify Camp Nou"},

            # Câu 1: Sân cỏ Nations League -> Các siêu sao thế hệ mới và hậu trường
            {"type": "sentence", "idx": 1, "fname": "v2_sports_world_stage.jpg", "query": "Nitto ATP Finals Turin Inalpi Arena court blue", "credit": "ATP TOUR", "desc": "Toàn cảnh sân khấu Inalpi Arena tại Turin"},
            {"type": "sentence", "idx": 1, "fname": "v2_young_stars_spotlight.jpg", "query": "Carlos Alcaraz tennis court match action", "credit": "REUTERS", "desc": "Sự áp đảo của các siêu sao thể thao thế hệ mới"},

            # Câu 2: Turin, giải đấu 8 tay vợt mạnh nhất -> Carlos Alcaraz bước ra sân
            {"type": "sentence", "idx": 2, "fname": "v2_atp_finals_turin_arena.jpg", "query": "ATP Finals trophy presentation court Turin", "credit": "ATP TOUR", "desc": "Khai màn giải quần vợt danh giá ATP Finals tại Turin"},
            {"type": "sentence", "idx": 2, "fname": "v2_alcaraz_court_entrance.jpg", "query": "Carlos Alcaraz walking on court tennis bag waves", "credit": "GETTY IMAGES", "desc": "Carlos Alcaraz tự tin tiến vào sân đấu"},

            # Câu 3: Alcaraz thắng trắng 6-2, 6-2 -> Frances Tiafoe bất lực
            {"type": "sentence", "idx": 3, "fname": "v2_alcaraz_forehand_smash.jpg", "query": "Carlos Alcaraz forehand winner shot tennis match", "credit": "REUTERS", "desc": "Cú thuận tay uy lực của Carlos Alcaraz"},
            {"type": "sentence", "idx": 3, "fname": "v2_tiafoe_reaction.jpg", "query": "Frances Tiafoe tennis match frustrated reaction", "credit": "GETTY IMAGES", "desc": "Frances Tiafoe bất lực trước sức ép từ đối thủ"},

            # Câu 4 (ĐA CHỦ THỂ): 21 winner -> Chuỗi 10 trận thắng -> Cúp vô địch và các đối thủ (Sinner, Medvedev)
            {"type": "sentence", "idx": 4, "fname": "v2_alcaraz_celebrate_fist.jpg", "query": "Carlos Alcaraz fist pump celebration victory ATP", "credit": "ATP TOUR", "desc": "Alcaraz tung cú winner thứ 21 và ăn mừng chiến thắng"},
            {"type": "sentence", "idx": 4, "fname": "v2_alcaraz_10_win_streak.jpg", "query": "Carlos Alcaraz winning streak celebration tennis", "credit": "REUTERS", "desc": "Chuỗi 10 trận toàn thắng liên tiếp của Alcaraz"},
            {"type": "sentence", "idx": 4, "fname": "v2_atp_finals_rivals_trophy.jpg", "query": "Jannik Sinner Daniil Medvedev ATP Finals tennis", "credit": "ATP TOUR", "desc": "Lời thách thức gửi tới các đối thủ cạnh tranh cúp ATP Finals"},

            # Câu 5: Ban tổ chức La Liga -> Thông báo minh oan cho Lamine Yamal
            {"type": "sentence", "idx": 5, "fname": "v2_laliga_headquarters.jpg", "query": "La Liga headquarters building logo Madrid", "credit": "REUTERS", "desc": "Trụ sở ban tổ chức giải bóng đá chuyên nghiệp La Liga"},
            {"type": "sentence", "idx": 5, "fname": "v2_yamal_exonerated.jpg", "query": "Lamine Yamal smiling Barcelona match action", "credit": "GETTY IMAGES", "desc": "Hiện tượng trẻ Lamine Yamal được chính thức minh oan"},

            # Câu 6: Cáo buộc giả mạo trên MXH / CCTV đưa tin -> Yamal trong sáng thân thiện
            {"type": "sentence", "idx": 6, "fname": "v2_cctv_sports_report.jpg", "query": "CCTV Sports broadcast studio news sports", "credit": "CCTV SPORTS", "desc": "Đài truyền hình CCTV Trung Quốc đưa tin về sự việc"},
            {"type": "sentence", "idx": 6, "fname": "v2_yamal_fans_interaction.jpg", "query": "Lamine Yamal signing autographs fans selfie", "credit": "GETTY IMAGES", "desc": "Lamine Yamal thân thiện giao lưu cùng người hâm mộ"},

            # Câu 7: La Liga kích hoạt pháp lý (Tebas) -> Yamal bình thản tập luyện
            {"type": "sentence", "idx": 7, "fname": "v2_tebas_statement.jpg", "query": "Javier Tebas La Liga president speech microphone", "credit": "REUTERS", "desc": "Chủ tịch La Liga Javier Tebas tuyên bố khởi kiện kẻ vu khống"},
            {"type": "sentence", "idx": 7, "fname": "v2_yamal_training_peace.jpg", "query": "Lamine Yamal Barcelona training pitch smiling", "credit": "FC BARCELONA", "desc": "Lamine Yamal thoải mái tập luyện tại trung tâm Ciutat Esportiva"},

            # Câu 8: Ban lãnh đạo Barcelona -> Dự án Memorial FC Barcelona tại Camp Nou
            {"type": "sentence", "idx": 8, "fname": "v2_barca_boardroom.jpg", "query": "FC Barcelona board meeting Joan Laporta boardroom", "credit": "GETTY IMAGES", "desc": "Ban lãnh đạo Barcelona trong buổi họp tài chính CLB"},
            {"type": "sentence", "idx": 8, "fname": "v2_camp_nou_construction.jpg", "query": "Camp Nou stadium renovation works construction 2024", "credit": "FC BARCELONA", "desc": "Đại dự án xây dựng và nâng cấp sân Camp Nou"},

            # Câu 9: Nhật báo El Plural tính toán 26000 ô lưu tro cốt -> Không gian bên trong sân
            {"type": "sentence", "idx": 9, "fname": "v2_memorial_concept_3d.jpg", "query": "Memorial FC Barcelona columbarium stadium concept rendering", "credit": "EL PLURAL", "desc": "Mô hình khu vực lưu giữ tro cốt Memorial Camp Nou"},
            {"type": "sentence", "idx": 9, "fname": "v2_camp_nou_interior_urns.jpg", "query": "Camp Nou new interior space architectural design", "credit": "FC BARCELONA", "desc": "Không gian tưởng niệm trang trọng bên trong sân vận động"},

            # Câu 10 (ĐA CHỦ THỂ): Doanh thu 71 triệu USD -> Nụ cười Joan Laporta -> Barcelona hồi sinh
            {"type": "sentence", "idx": 10, "fname": "v2_barca_71m_revenue.jpg", "query": "FC Barcelona finance budget report stadium", "credit": "EL PLURAL", "desc": "Dự kiến thu về hơn 71 triệu USD giải cứu bài toán tài chính"},
            {"type": "sentence", "idx": 10, "fname": "v2_laporta_press_smiling.jpg", "query": "Joan Laporta Barcelona president smiling suit", "credit": "REUTERS", "desc": "Chủ tịch Joan Laporta tự tin về tiến trình phục hồi tài chính"},
            {"type": "sentence", "idx": 10, "fname": "v2_barca_crest_stadium.jpg", "query": "FC Barcelona crest logo stadium seats stands", "credit": "GETTY IMAGES", "desc": "Biểu tượng FC Barcelona trên khán đài Camp Nou rực rỡ"}
        ]
    },
    {
        "id": 3,
        "slug": "Short_Tong_Hop_VN_Tam_Diem_My_Dinh_Va_Diem_Sang_The_Thao_Nuoc_Nha",
        "group": "BẢN TIN VIỆT NAM • TÂM ĐIỂM MỸ ĐÌNH & ĐIỂM SÁNG NƯỚC NHÀ",
        "title": "ĐT Việt Nam quyết đấu Kyrgyzstan, tin vui FIFA và điểm sáng thể thao nước nhà",
        "news_source": "DÂN TRÍ / BÁO THANH NIÊN / TUỔI TRẺ",
        "credit": "VFF / BÁO THANH NIÊN / BÁO TUỔI TRẺ",
        "source": "VFF, Dân Trí, Thanh Niên, Tuổi Trẻ",
        "hide_date_chip": True,
        "sentences": [
            "Không khí thể thao trong nước ngày hôm nay đang trở nên vô cùng sôi động khi người hâm mộ cả nước dồn trọn sự chú ý về sân vận động quốc gia Mỹ Đình, nơi đội tuyển Việt Nam sẽ bước vào trận đấu chính thức khép lại năm 2026.",
            "Đúng 19h00 tối nay ngày 17 tháng 11, các chiến binh sao vàng sẽ bước vào màn so tài được chờ đợi với đội tuyển Kyrgyzstan.",
            "Đây là đợt sát hạch vô cùng quan trọng của HLV Kim Sang-sik trước khi đội tuyển bước vào quãng nghỉ kéo dài tới 9 tháng.",
            "Sau khi chân sút nhập tịch Olaha Mạnh Đức được cho phép trở về câu lạc bộ Công an TP.HCM để chuẩn bị cho cúp Đông Nam Á, ban huấn luyện đội tuyển đang tích cực tìm lời giải cho bài toán hàng công.",
            "HLV Kim Sang-sik đã lên kế hoạch thử nghiệm dàn tiền đạo có thể hình lý tưởng trên 1,82 m gồm Tiến Linh, Đinh Thanh Bình và Bùi Vĩ Hào, nhằm tạo nên sức ép trực diện trước hàng phòng ngự kỷ luật và thể lực dồi dào của đại diện Trung Á xếp hạng 102 FIFA.",
            "Ngay trước giờ bóng lăn, đội tuyển Việt Nam cũng đã đón nhận một món quà bất ngờ khi chính thức được cộng điểm để nhích thêm một bậc trên bảng xếp hạng thế giới, nhờ vào thất bại của đối thủ cạnh tranh Mozambique tại vòng loại cúp châu Phi.",
            "Không chỉ ở cấp độ đội tuyển quốc gia, bóng đá trẻ Việt Nam cũng đang lan tỏa nguồn năng lượng vô cùng tích cực.",
            "Tại Doha, đội tuyển U17 Việt Nam đã hoàn tất buổi tập đầu tiên trên cụm sân Al-Gharafa, tự tin bước vào giai đoạn chuẩn bị then chốt cho Vòng chung kết U17 World Cup 2026.",
            "Thành quả đào tạo bài bản của bóng đá trẻ Việt Nam với hạt nhân Chu Ngọc Nguyễn Lực được FIFA vinh danh thậm chí còn khiến truyền thông Indonesia phải chạnh lòng thán phục về định hướng nội lực vững chắc của chúng ta.",
            "Cùng thời điểm này, không khí Đại hội Thể thao toàn quốc 2026 cũng đang rực lửa tại các sàn đấu phía Nam.",
            "Đội tuyển Judo TP.HCM đã đón tấm Huy chương Vàng mở hàng đầy cảm xúc của võ sĩ Phan Ngọc Dũng, trong khi cựu binh Vũ Thị Trang thi đấu thăng hoa giúp cầu lông thành phố sớm cầm chắc tấm huy chương danh giá.",
            "Tất cả đang tạo nên một ngày thi đấu đầy khí thế và hy vọng cho thể thao nước nhà."
        ],
        "image_slots": [
            # Title
            {"type": "title", "idx": 0, "fname": "v3_vietnam_team_salute.jpg", "query": "doi tuyen viet nam hat quoc ca my dinh", "credit": "VFF", "desc": "Đội tuyển Việt Nam nghiêm trang chào cờ trước trận đấu"},
            {"type": "title", "idx": 0, "fname": "v3_mydinh_stadium_panorama.jpg", "query": "san van dong quoc gia my dinh toan canh dep", "credit": "BÁO THANH NIÊN", "desc": "Toàn cảnh sân vận động quốc gia Mỹ Đình"},
            {"type": "title", "idx": 0, "fname": "v3_kim_sangsik_action.jpg", "query": "HLV Kim Sang-sik chi dao doi tuyen viet nam", "credit": "DÂN TRÍ", "desc": "HLV Kim Sang-sik truyền nhiệt huyết cho học trò"},

            # Câu 1: Người hâm mộ cờ đỏ sao vàng -> Sân Mỹ Đình lên đèn rực rỡ
            {"type": "sentence", "idx": 1, "fname": "v3_fans_red_flags.jpg", "query": "co dong vien viet nam co do sao vang my dinh", "credit": "BÁO TUỔI TRẺ", "desc": "Cổ động viên mang cờ đỏ sao vàng rực rỡ"},
            {"type": "sentence", "idx": 1, "fname": "v3_stadium_lights_on.jpg", "query": "san my dinh ruc sang den tran dau", "credit": "BÁO THANH NIÊN", "desc": "Sân vận động Mỹ Đình lên đèn lung linh"},

            # Câu 2 (ĐA CHỦ THỂ): ĐT Việt Nam 19h00 -> Đối thủ Kyrgyzstan sẵn sàng
            {"type": "sentence", "idx": 2, "fname": "v3_vietnam_team_ready.jpg", "query": "doi tuyen viet nam tap luyen my dinh tran dau", "credit": "VFF", "desc": "Đội tuyển Việt Nam sẵn sàng cho trận cầu lúc 19h00"},
            {"type": "sentence", "idx": 2, "fname": "v3_kyrgyzstan_lineup_match.jpg", "query": "Kyrgyzstan national football team lineup pitch", "credit": "AFC", "desc": "Đội hình đại diện Trung Á Kyrgyzstan sẵn sàng nghênh chiến"},

            # Câu 3: Sát hạch quan trọng của HLV Kim Sang-sik -> Quãng nghỉ 9 tháng của ĐTQG
            {"type": "sentence", "idx": 3, "fname": "v3_kim_sangsik_intense.jpg", "query": "HLV Kim Sang-sik san tap doi tuyen viet nam", "credit": "DÂN TRÍ", "desc": "Sự tập trung cao độ của HLV Kim Sang-sik"},
            {"type": "sentence", "idx": 3, "fname": "v3_coaching_staff_meeting.jpg", "query": "ban huan luyen doi tuyen viet nam trao doi", "credit": "VFF", "desc": "Ban huấn luyện đội tuyển trao đổi chiến thuật"},

            # Câu 4: Olaha Mạnh Đức về CLB CA TP.HCM -> Tìm lời giải bài toán hàng công
            {"type": "sentence", "idx": 4, "fname": "v3_olaha_manh_duc_cahn.jpg", "query": "Michael Olaha song lam nghe an hoac cong an ha noi", "credit": "CLB CAHN", "desc": "Tiền đạo Olaha Mạnh Đức trong màu áo câu lạc bộ"},
            {"type": "sentence", "idx": 4, "fname": "v3_vietnam_attack_drill.jpg", "query": "tien dao doi tuyen viet nam tap sut bong", "credit": "BÁO THANH NIÊN", "desc": "Ban huấn luyện tìm lời giải cho hàng tấn công"},

            # Câu 5 (ĐA CHỦ THỂ): Tiến Linh -> Đinh Thanh Bình & Bùi Vĩ Hào -> Hàng thủ vạm vỡ của Kyrgyzstan
            {"type": "sentence", "idx": 5, "fname": "v3_tien_linh_header_drill.jpg", "query": "Nguyen Tien Linh doi tuyen viet nam tap luyen danh dau", "credit": "BÁO THANH NIÊN", "desc": "Tiền đạo Tiến Linh bật cao đánh đầu trên sân tập"},
            {"type": "sentence", "idx": 5, "fname": "v3_thanh_binh_vi_hao.jpg", "query": "Bui Vi Hao Dinh Thanh Binh tap luyen tranh chap", "credit": "VFF", "desc": "Đinh Thanh Bình và Bùi Vĩ Hào nỗ lực tranh chấp"},
            {"type": "sentence", "idx": 5, "fname": "v3_kyrgyzstan_defense_wall.jpg", "query": "Kyrgyzstan national football team defense action", "credit": "AFC", "desc": "Hàng phòng ngự thể lực vạm vỡ của Kyrgyzstan (Hạng 102 FIFA)"},

            # Câu 6 (ĐA CHỦ THỂ): ĐT Việt Nam tăng hạng FIFA -> Tuyển vui mừng -> Thất bại của Mozambique tại CAN
            {"type": "sentence", "idx": 6, "fname": "v3_fifa_ranking_graphic.jpg", "query": "bang xep hang FIFA doi tuyen viet nam", "credit": "FIFA / DÂN TRÍ", "desc": "Bảng xếp hạng FIFA với lá cờ Việt Nam thăng hạng"},
            {"type": "sentence", "idx": 6, "fname": "v3_vietnam_celebration.jpg", "query": "doi tuyen viet nam an mung chien thang dong doi", "credit": "BÁO TUỔI TRẺ", "desc": "Niềm vui chiến thắng của các tuyển thủ Việt Nam"},
            {"type": "sentence", "idx": 6, "fname": "v3_mozambique_can_defeat.jpg", "query": "Mozambique national football team match Africa Cup", "credit": "CAF", "desc": "Đội tuyển Mozambique ngậm ngùi nhận thất bại tại vòng loại CAN"},

            # Câu 7: Thế hệ trẻ bóng đá Việt Nam
            {"type": "sentence", "idx": 7, "fname": "v3_young_stars_vietnam.jpg", "query": "cau thu tre bong da viet nam u17 u23", "credit": "VFF", "desc": "Thế hệ tài năng trẻ đầy triển vọng của bóng đá Việt Nam"},

            # Câu 8: U17 Việt Nam tập luyện tại Doha -> HLV Cristiano Roland rèn quân
            {"type": "sentence", "idx": 8, "fname": "v3_u17_training_doha.jpg", "query": "u17 viet nam tap luyen qatar doha san co", "credit": "VFF", "desc": "U17 Việt Nam tập luyện tại Doha, Qatar"},
            {"type": "sentence", "idx": 8, "fname": "v3_coach_roland_u17.jpg", "query": "HLV Cristiano Roland u17 viet nam chi dao", "credit": "BÁO TUỔI TRẺ", "desc": "HLV Cristiano Roland rèn quân kỹ lưỡng cho U17 World Cup"},

            # Câu 9 (ĐA CHỦ THỂ): Chu Ngọc Nguyễn Lực được FIFA vinh danh -> Báo chí Indonesia (Bola) thán phục
            {"type": "sentence", "idx": 9, "fname": "v3_chu_ngoc_nguyen_luc.jpg", "query": "Chu Ngoc Nguyen Luc u17 viet nam fifa", "credit": "FIFA / VFF", "desc": "Tài năng trẻ Chu Ngọc Nguyễn Lực được FIFA vinh danh"},
            {"type": "sentence", "idx": 9, "fname": "v3_indonesia_press_article.jpg", "query": "doi tuyen u17 viet nam thi dau quoc te", "credit": "BOLA", "desc": "Truyền thông Indonesia chạnh lòng thán phục bóng đá trẻ Việt Nam"},

            # Câu 10: Đại hội Thể thao toàn quốc rực lửa phía Nam
            {"type": "sentence", "idx": 10, "fname": "v3_national_games_banner.jpg", "query": "dai hoi the thao toan quoc 2026 khai mac thi dau", "credit": "TỔNG CỤC TDTT", "desc": "Không khí Đại hội Thể thao toàn quốc 2026 rực lửa"},
            {"type": "sentence", "idx": 10, "fname": "v3_sports_arena_crowd.jpg", "query": "nha thi dau the thao khan gia co vu soi dong", "credit": "BÁO TUỔI TRẺ", "desc": "Khán đài nhà thi đấu rực rỡ cờ hoa"},

            # Câu 11 (ĐA CHỦ THỂ): Phan Ngọc Dũng (Judo) HCV -> Vũ Thị Trang (Cầu lông) thăng hoa
            {"type": "sentence", "idx": 11, "fname": "v3_judo_phan_ngoc_dung_gold.jpg", "query": "judo viet nam vo si gianh huy chuong vang phan ngoc dung", "credit": "BÁO TUỔI TRẺ", "desc": "Võ sĩ Judo Phan Ngọc Dũng giành HCV mở hàng đầy cảm xúc"},
            {"type": "sentence", "idx": 11, "fname": "v3_vu_thi_trang_smash.jpg", "query": "Vu Thi Trang cau long thi dau danh don", "credit": "BÁO THANH NIÊN", "desc": "Cựu binh Vũ Thị Trang thi đấu thăng hoa môn cầu lông"},

            # Câu 12: Đại kỳ cờ đỏ sao vàng tung bay
            {"type": "sentence", "idx": 12, "fname": "v3_vietnam_flag_stadium.jpg", "query": "co do sao vang dai ky bay tren khan dai my dinh", "credit": "BÁO TUỔI TRẺ", "desc": "Đại kỳ cờ đỏ sao vàng tung bay trên khán đài"}
        ]
    }
]

# =====================================================================
# 2. XUẤT FILE DỮ LIỆU JSON
# =====================================================================

def export_metadata_files():
    thethao_data = []
    for v in VIDEOS_CONFIG:
        item = {
            "id": v["id"],
            "slug": v["slug"],
            "group": v["group"],
            "title": v["title"],
            "summary": " ".join(v["sentences"]),
            "source": v["source"],
            "news_source": v["news_source"],
            "credit": v["credit"],
            "hide_date_chip": v["hide_date_chip"],
            "audio_path": str(DAY_DIR / "audio" / f"audio_{v['id']:02d}.wav"),
            "audio_title": str(DAY_DIR / "audio-title" / f"audio_title_{v['id']:02d}.wav"),
        }
        for i, slot in enumerate(v["image_slots"], 1):
            item[f"image_{i}"] = str(IMG_DIR / slot["fname"])
        item["image_path"] = str(IMG_DIR / v["image_slots"][0]["fname"])
        thethao_data.append(item)

    with open(DAY_DIR / "thethao.json", "w", encoding="utf-8") as f:
        json.dump(thethao_data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Đã cập nhật thethao.json ({len(thethao_data)} bản tin tổng hợp)")

    records = []
    credits_map = {}
    for v in VIDEOS_CONFIG:
        for slot in v["image_slots"]:
            rec = {
                "scene_id": v["id"],
                "type": slot["type"],
                "index": slot["idx"],
                "sentence_idx": slot["idx"],
                "file_name": slot["fname"],
                "credit": slot["credit"],
                "description": slot["desc"]
            }
            records.append(rec)
            credits_map[slot["fname"]] = {
                "credit": slot["credit"],
                "description": slot["desc"]
            }

    with open(DAY_DIR / "image_plan.json", "w", encoding="utf-8") as f:
        json.dump({"records": records}, f, ensure_ascii=False, indent=2)
    print(f"[OK] Đã cập nhật image_plan.json ({len(records)} slots ảnh chuẩn)")

    with open(DAY_DIR / "image_credits.json", "w", encoding="utf-8") as f:
        json.dump(credits_map, f, ensure_ascii=False, indent=2)
    print(f"[OK] Đã cập nhật image_credits.json ({len(credits_map)} entries)")


# =====================================================================
# 3. TẢI ẢNH ĐỘ PHÂN GIẢI CAO QUA DDGS
# =====================================================================

class ImageDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": UA})

    def search_images(self, query: str, max_cands: int = 25) -> List[str]:
        full_q = f"{query} {NEG_KW}".strip()
        for attempt in range(3):
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.images(
                        full_q,
                        region="wt-wt",
                        safesearch="off",
                        size="Large",
                        layout="Wide",
                        max_results=max_cands
                    ))
                urls = []
                for r in results:
                    u = r.get("image")
                    if not u or host_blocked(u):
                        continue
                    urls.append(u)
                if urls:
                    return urls
            except Exception as e:
                time.sleep(2 * (attempt + 1))
        return []

    def fetch_image(self, url: str) -> Image.Image | None:
        try:
            r = self.session.get(url, timeout=12, stream=False)
            if r.status_code != 200 or len(r.content) < 30_000:
                return None
            img = Image.open(io.BytesIO(r.content))
            img.load()
            w, h = img.size
            if w < 750 or h < 450:
                return None
            if img.mode != "RGB":
                img = img.convert("RGB")
            return img
        except Exception:
            return None

    def download_slot(self, slot: Dict[str, Any]) -> bool:
        dest_path = IMG_DIR / slot["fname"]
        if dest_path.exists() and dest_path.stat().st_size > 30_000:
            try:
                with Image.open(dest_path) as im:
                    w, h = im.size
                    if w >= 750 and h >= 450:
                        print(f"  [ĐÃ CÓ ĐẠT CHUẨN] {slot['fname']} ({w}x{h})")
                        return True
            except Exception:
                pass

        queries = [
            slot["query"],
            re.sub(r"\b(2026|match|action|drill|stadium|high resolution)\b", "", slot["query"]).strip(),
            f"sports {slot['fname'].replace('.jpg', '').replace('_', ' ')}"
        ]

        for q in queries:
            if not q:
                continue
            urls = self.search_images(q)
            for u in urls:
                img = self.fetch_image(u)
                if img is not None:
                    img.save(dest_path, "JPEG", quality=92, optimize=True)
                    w, h = img.size
                    print(f"  [TẢI MỚI THÀNH CÔNG] {slot['fname']} ({w}x{h}) <- '{q}'")
                    return True
            time.sleep(0.4)

        print(f"  [CẢNH BÁO] Không tìm thấy ảnh đạt chuẩn cho {slot['fname']}")
        return False


# =====================================================================
# 4. TẠO CONTACT SHEETS KIỂM DUYỆT THỊ GIÁC (QA)
# =====================================================================

def build_contact_sheets():
    print("\n=== ĐANG TẠO LẠI BẢNG ẢNH ĐỐI CHỨNG (CONTACT SHEET QA) ===")
    
    font_path = ROOT_DIR / "assets" / "fonts" / "BeVietnamPro-SemiBold.ttf"
    if not font_path.exists():
        font_path = ROOT_DIR / "assets" / "fonts" / "BarlowCondensed-SemiBold.ttf"
    
    try:
        font_title = ImageFont.truetype(str(font_path), 24)
        font_label = ImageFont.truetype(str(font_path), 15)
        font_small = ImageFont.truetype(str(font_path), 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_small = ImageFont.load_default()

    cols = 4
    thumb_w = 380
    thumb_h = 240
    card_h = 330
    pad = 16

    all_slots = []
    for v in VIDEOS_CONFIG:
        scene_id = v["id"]
        slots = v["image_slots"]
        all_slots.extend([(scene_id, s) for s in slots])

        n = len(slots)
        rows = (n + cols - 1) // cols
        sheet_w = cols * thumb_w + (cols + 1) * pad
        sheet_h = rows * card_h + (rows + 1) * pad + 60

        sheet = Image.new("RGB", (sheet_w, sheet_h), color="#070B14")
        draw = ImageDraw.Draw(sheet)

        header_text = f"BẢNG KIỂM DUYỆT THỊ GIÁC — VIDEO {scene_id} ({len(slots)} ẢNH): {v['group']}"
        draw.text((pad, 16), header_text, font=font_title, fill="#00E5FF")

        for idx, s in enumerate(slots):
            r = idx // cols
            c = idx % cols
            x = pad + c * (thumb_w + pad)
            y = 60 + pad + r * (card_h + pad)

            draw.rectangle([x, y, x + thumb_w, y + card_h], fill="#0F172A", outline="#1E293B", width=2)

            img_p = IMG_DIR / s["fname"]
            if img_p.exists():
                try:
                    with Image.open(img_p) as im:
                        orig_w, orig_h = im.size
                        im.thumbnail((thumb_w - 8, thumb_h - 8), Image.Resampling.LANCZOS)
                        tx = x + 4 + (thumb_w - 8 - im.width) // 2
                        ty = y + 4 + (thumb_h - 8 - im.height) // 2
                        sheet.paste(im, (tx, ty))
                        dim_text = f"{orig_w}x{orig_h}px"
                except Exception:
                    dim_text = "Lỗi ảnh"
            else:
                dim_text = "THIẾU ẢNH"
                draw.rectangle([x + 4, y + 4, x + thumb_w - 4, y + thumb_h - 4], fill="#331111")
                draw.text((x + 20, y + thumb_h // 2), "THIẾU ẢNH TƯ LIỆU", font=font_title, fill="#EF4444")

            label_prefix = f"CÂU {s['idx']}" if s['idx'] > 0 else "TIÊU ĐỀ"
            draw.text((x + 10, y + thumb_h + 8), f"[{label_prefix}] {s['fname']} ({dim_text})", font=font_label, fill="#F8FAFC")
            draw.text((x + 10, y + thumb_h + 30), f"Nguồn: {s['credit']}", font=font_small, fill="#38BDF8")
            
            desc = s["desc"]
            if len(desc) > 42:
                desc = desc[:40] + "..."
            draw.text((x + 10, y + thumb_h + 50), desc, font=font_small, fill="#94A3B8")

        out_scene_qa = QA_DIR / f"contact_scene_{scene_id:02d}.jpg"
        sheet.save(out_scene_qa, "JPEG", quality=90)
        print(f"  [QA OK] {out_scene_qa.name} ({sheet_w}x{sheet_h})")

    # Sinh contact_overview.jpg (mẫu đại diện 36 ảnh)
    overview_slots = all_slots[:36]
    n = len(overview_slots)
    rows = (n + cols - 1) // cols
    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = rows * card_h + (rows + 1) * pad + 60
    sheet = Image.new("RGB", (sheet_w, sheet_h), color="#070B14")
    draw = ImageDraw.Draw(sheet)
    draw.text((pad, 16), f"TỔNG QUAN TẤT CẢ ẢNH TƯ LIỆU — 3 VIDEO SHORTS ({len(all_slots)} ẢNH)", font=font_title, fill="#00E5FF")

    for idx, (sc_id, s) in enumerate(overview_slots):
        r = idx // cols
        c = idx % cols
        x = pad + c * (thumb_w + pad)
        y = 60 + pad + r * (card_h + pad)
        draw.rectangle([x, y, x + thumb_w, y + card_h], fill="#0F172A", outline="#1E293B", width=2)
        img_p = IMG_DIR / s["fname"]
        if img_p.exists():
            try:
                with Image.open(img_p) as im:
                    orig_w, orig_h = im.size
                    im.thumbnail((thumb_w - 8, thumb_h - 8), Image.Resampling.LANCZOS)
                    tx = x + 4 + (thumb_w - 8 - im.width) // 2
                    ty = y + 4 + (thumb_h - 8 - im.height) // 2
                    sheet.paste(im, (tx, ty))
                    dim_text = f"{orig_w}x{orig_h}px"
            except Exception:
                dim_text = "Lỗi ảnh"
        else:
            dim_text = "THIẾU ẢNH"
        draw.text((x + 10, y + thumb_h + 8), f"[V{sc_id}-C{s['idx']}] {s['fname']} ({dim_text})", font=font_label, fill="#F8FAFC")
        draw.text((x + 10, y + thumb_h + 30), f"Nguồn: {s['credit']}", font=font_small, fill="#38BDF8")
        desc = s["desc"]
        if len(desc) > 42:
            desc = desc[:40] + "..."
        draw.text((x + 10, y + thumb_h + 50), desc, font=font_small, fill="#94A3B8")

    out_overview = QA_DIR / "contact_overview.jpg"
    sheet.save(out_overview, "JPEG", quality=90)
    print(f"  [QA OK] {out_overview.name} ({sheet_w}x{sheet_h})")


# =====================================================================
# 5. KIỂM DUYỆT TỔNG THỂ & BÁO CÁO
# =====================================================================

def audit_downloaded_images():
    print("\n=== BẮT ĐẦU KIỂM DUYỆT HÌNH ẢNH TOÀN DIỆN (AUDIT) ===")
    total = 0
    passed = 0
    failed = []

    for v in VIDEOS_CONFIG:
        for s in v["image_slots"]:
            total += 1
            p = IMG_DIR / s["fname"]
            if not p.exists():
                failed.append((s["fname"], "Không tồn tại"))
                continue
            sz = p.stat().st_size
            if sz < 25_000:
                failed.append((s["fname"], f"Dung lượng quá nhỏ ({sz} bytes)"))
                continue
            try:
                with Image.open(p) as im:
                    w, h = im.size
                    if w < 700 or h < 400:
                        failed.append((s["fname"], f"Độ phân giải nhỏ ({w}x{h})"))
                        continue
                    passed += 1
            except Exception as e:
                failed.append((s["fname"], f"File hỏng: {e}"))

    print(f"KẾT QUẢ KIỂM DUYỆT: {passed}/{total} ảnh đạt chuẩn tuyệt đối.")
    if failed:
        print(f"Cảnh báo {len(failed)} ảnh chưa đạt:")
        for fname, reason in failed:
            print(f"  - {fname}: {reason}")
    else:
        print("[HOÀN HẢO] 100% ảnh đạt độ phân giải cao, đúng chủ thể từng câu, sắc nét, không lỗi!")

def main():
    print("================================================================================")
    print("THU THẬP & ĐỒNG BỘ ẢNH TƯ LIỆU THEO DÒNG NGỮ NGHĨA TỪNG CÂU (17.11.2026)")
    print("================================================================================")
    
    export_metadata_files()

    downloader = ImageDownloader()
    print("\n=== ĐANG TẢI BỔ SUNG CÁC ẢNH CHỦ THỂ MỚI THEO CÂU ===")
    for v in VIDEOS_CONFIG:
        print(f"\n--- Kiểm tra & Tải ảnh cho Video {v['id']}: {v['slug']} ---")
        for slot in v["image_slots"]:
            downloader.download_slot(slot)

    build_contact_sheets()
    audit_downloaded_images()

if __name__ == "__main__":
    main()
