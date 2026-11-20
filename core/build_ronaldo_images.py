#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_ronaldo_images.py — Bộ thu thập ảnh tư liệu cho video chuyên đề Cristiano Ronaldo (25.10.2026)

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
     - outputs/25.10.2026/kich_ban_tung_cau.txt  (kế hoạch từng câu, chuẩn 22.10)
     - outputs/25.10.2026/thethao.txt, thethao.json
     - outputs/25.10.2026/image_plan.json (nhật ký nguồn từng ảnh)
     - outputs/25.10.2026/images/Tin_XX_N.jpg
     - Contact sheet QA: ~/Library/Caches/DiemDoc/ronaldo_2510/qa/

Cách chạy:
  python3 -B core/build_ronaldo_images.py            # chạy chính (resume tự động)
  python3 -B core/build_ronaldo_images.py --force    # tải lại toàn bộ
  python3 -B core/build_ronaldo_images.py --sheets   # chỉ sinh lại contact sheet
"""
import sys
import os
import json
import time
import io
import re
from pathlib import Path

sys.dont_write_bytecode = True

import requests
from PIL import Image, ImageDraw, ImageFont
from ddgs import DDGS

# ------------------------------------------------------------------ ĐƯỜNG DẪN
ROOT = Path(__file__).resolve().parent.parent
DAY = ROOT / "outputs" / "25.10.2026"
IMG_DIR = DAY / "images"
CACHE = Path.home() / "Library" / "Caches" / "DiemDoc" / "ronaldo_2510"
STAGING = CACHE / "staging"
QA_DIR = CACHE / "qa"
QCACHE = CACHE / "query_cache.json"

for d in (DAY, IMG_DIR, STAGING, QA_DIR):
    d.mkdir(parents=True, exist_ok=True)

VIDEO_TITLE = ("Ronaldo 41 Tuổi: Bỏ Đội Tuyển, Hỏng Phạt Đền, "
               "Cuộc Đua 1000 Bàn")

# ------------------------------------------------------------------ DỮ LIỆU KỊCH BẢN
# Mỗi cảnh: group, title (tiêu đề hero), title_queries (3 ảnh mở cảnh),
# sentences: text + queries (số ảnh lấy theo luật từ; script tự chốt số lượng).
SCENES = [
    {
        "id": 1,
        "group": "Nhóm: Mở Màn — Cơn Sốc",
        "title": "Ronaldo bỏ về giữa đêm: Án treo giò 30 ngày của vua bóng đá 41 tuổi",
        "title_queries": [
            "Cristiano Ronaldo Al Nassr 2026 serious portrait",
            "Cristiano Ronaldo Portugal 2026 national team kit",
            "Cristiano Ronaldo night stadium dramatic light",
        ],
        "sentences": [
            {"text": "Đêm 30 tháng 9 năm 2026, tại trung tâm tập luyện của đội tuyển Bồ Đào Nha, một người đàn ông 41 tuổi lặng lẽ thu dọn đồ đạc, kéo chiếc vali ra cửa, lên xe và biến mất vào bóng đêm — không một lời chào, không một lời giải thích.",
             "queries": ["Cristiano Ronaldo leaving training ground suitcase", "Portugal national team training center Cidade do Futebol"]},
            {"text": "Người đàn ông ấy là Cristiano Ronaldo — huyền thoại sống của bóng đá thế giới, người khoác áo đội tuyển Bồ Đào Nha nhiều nhất lịch sử với 233 trận đấu, chân sút đang tiến sát cột mốc 1000 bàn thắng mà chưa một cầu thủ nào trong lịch sử chạm tới.",
             "queries": ["Cristiano Ronaldo Portugal captain armband", "Cristiano Ronaldo Al Nassr goal celebration 2026"]},
            {"text": "Và anh vừa... bỏ về.",
             "queries": ["Cristiano Ronaldo walking away stadium night"]},
            {"text": "Hình ảnh ấy lan nhanh như cháy rừng trên mọi mặt báo, từ Lisbon tới Riyadh, và theo báo Ngôi Sao, Liên đoàn bóng đá Bồ Đào Nha buộc phải lên tiếng chính thức: hành vi 'tự ý rời đội tuyển' của Ronaldo là vi phạm kỷ luật nghiêm trọng.",
             "queries": ["Portuguese sports newspaper headlines Ronaldo", "Lisbon Portugal football fans street"]},
            {"text": "Ba tuần sau, ngày 19 tháng 10, bản án được tuyên: treo giò 30 ngày, phạt 255 euro — theo báo 24h.com.vn, tương đương khoảng 7,4 triệu đồng.",
             "queries": ["Cristiano Ronaldo Portugal suspension news"]},
            {"text": "Con số nghe có vẻ nhẹ nhàng, nhưng các bạn ạ, đây là Cristiano Ronaldo — biểu tượng quốc gia — bị chính liên đoàn của mình đình chỉ vì... bỏ về.",
             "queries": ["Cristiano Ronaldo serious face portrait close up"]},
            {"text": "Câu hỏi đặt ra: điều gì có thể đẩy huyền thoại vĩ đại nhất hành tinh này đến mức rời bỏ đội tuyển quốc gia của chính mình — thứ anh đã đổ mồ hôi nước mắt bảo vệ từ năm 18 tuổi?",
             "queries": ["young Cristiano Ronaldo Sporting CP 2003", "Cristiano Ronaldo Portugal debut 2003"]},
            {"text": "Hôm nay, Điểm Đọc sẽ đưa các bạn đi qua từng lớp sự thật của cơn bão mang tên Ronaldo: lời hứa bị phá vỡ, cuộc chiến quyền lực với HLV Jorge Jesus, bản án gây tranh cãi, và hành trình truy đuổi cột mốc 1000 bàn đầy nước mắt.",
             "queries": ["Jorge Jesus Portugal head coach touchline", "Cristiano Ronaldo 1000 goals celebration"]},
            {"text": "Hãy thắt dây an toàn — câu chuyện này kịch tính hơn cả điện ảnh.",
             "queries": ["Cristiano Ronaldo intense eyes close up"]},
        ],
    },
    {
        "id": 2,
        "group": "Nhóm: Cuộc Chiến Quyền Lực",
        "title": "Lời hứa bị phá vỡ: Jorge Jesus xếp Ronaldo ngồi dự bị trước trận Na Uy",
        "title_queries": [
            "Jorge Jesus Portugal national team coach",
            "Jorge Jesus press conference coach",
            "Cristiano Ronaldo Portugal bench substitute",
        ],
        "sentences": [
            {"text": "Mọi chuyện bắt đầu từ một lời hứa.",
             "queries": ["Jorge Jesus coach portrait serious"]},
            {"text": "Sau World Cup 2026, bóng đá Bồ Đào Nha bước sang trang mới, và trên ghế HLV trưởng là Jorge Jesus — viên tướng già nổi tiếng với kỷ luật thép và cái tôi cực lớn.",
             "queries": ["Jorge Jesus coach touchline shouting"]},
            {"text": "Tháng 9, Jesus công bố đội hình đầu tiên dưới thời mình, và cái tên Cristiano Ronaldo vẫn có mặt — kèm theo đó, theo lời Ronaldo kể lại, là một thỏa thuận: siêu sao 41 tuổi sẽ trở lại đội hình xuất phát, đội trưởng sẽ dẫn dắt đội tuyển như thủa nào.",
             "queries": ["Cristiano Ronaldo Portugal training 2026", "Portugal national team squad training 2026"]},
            {"text": "Rồi đến đợt tập trung cuối tháng 9, trước trận gặp Na Uy tại Nations League, Jorge Jesus đưa ra quyết định của mình: Ronaldo... dự bị.",
             "queries": ["Cristiano Ronaldo bench Portugal jacket"]},
            {"text": "Các bạn hãy nhớ giùm tôi bối cảnh này: đây không phải một cầu thủ bình thường bị xoay tua — đây là chủ nhân 233 trận khoác áo, người từng nâng hai chiếc cúp lớn nhất lịch sử đội tuyển: EURO 2016 và Nations League 2019.",
             "queries": ["Portugal EURO 2016 trophy celebration Ronaldo", "Portugal Nations League 2019 trophy Ronaldo"]},
            {"text": "Theo Al Jazeera, Ronaldo coi đó là sự phản bội — lời hứa đã cho, lời hứa bị rút lại — anh đến tập trung với tư cách đội trưởng, rồi bị báo hiệu sẽ không được đá chính.",
             "queries": ["Cristiano Ronaldo frustrated angry pitch", "Cristiano Ronaldo sitting bench thoughtful"]},
            {"text": "Và trong đêm 30 tháng 9, Ronaldo ra đi — không tranh cãi ồn ào, không họp báo — chỉ một chiếc vali, một cánh cửa đóng lại sau lưng, và một đội tuyển chìm trong bàng hoàng.",
             "queries": ["Cristiano Ronaldo airport luggage leaving", "empty football dressing room lockers"]},
            {"text": "Ngay hôm sau, The Guardian chạy bài với tiêu đề khiến cả nước Bồ Đào Nha lạnh gáy: cuộc bỏ đi của Ronaldo đang chia rẽ cả một quốc gia.",
             "queries": ["Portugal football fans crowd flags"]},
        ],
    },
    {
        "id": 3,
        "group": "Nhóm: Cuộc Chiến Quyền Lực",
        "title": "Một quốc gia bị chia rẽ và lời xin lỗi ngày 6 tháng 10",
        "title_queries": [
            "Portugal fans divided Ronaldo debate",
            "Jorge Jesus press conference 2026",
            "Cristiano Ronaldo statement interview Portugal",
        ],
        "sentences": [
            {"text": "Tin Ronaldo bỏ về lan tới đâu, nước Bồ Đào Nha nứt toạc tới đó.",
             "queries": ["Lisbon Portugal streets football supporters"]},
            {"text": "Phe thứ nhất đứng về Jorge Jesus — với họ, không ai, kể cả Ronaldo, được phép lớn hơn đội tuyển, và bỏ về giữa chừng là phá vỡ nguyên tắc thiêng liêng nhất của phòng thay đồ.",
             "queries": ["Jorge Jesus coach stern face"]},
            {"text": "Chính Jorge Jesus cũng lên tiếng dứt khoát khi được hỏi: anh toàn quyền quyết định đội hình, và Cristiano Ronaldo không điều hành đội bóng này.",
             "queries": ["Jorge Jesus Portugal press conference"]},
            {"text": "Phe thứ hai bênh vực Ronaldo — họ đặt câu hỏi ngược: một cầu thủ cống hiến 23 năm, 233 trận, từng nâng EURO 2016 và Nations League, liệu có xứng đáng bị đối xử theo kiểu 'hứa rồi lật kèo'?",
             "queries": ["Cristiano Ronaldo Portugal fans banner", "Cristiano Ronaldo EURO 2016 final trophy"]},
            {"text": "Nếu HLV thất hứa trước, ai mới là người phá vỡ lòng tin trước?",
             "queries": ["Cristiano Ronaldo disappointed looking down pitch"]},
            {"text": "Giữa hai phe, ngày 6 tháng 10, Ronaldo lên tiếng.",
             "queries": ["Cristiano Ronaldo interview camera serious"]},
            {"text": "Theo Al Jazeera, anh gửi lời xin lỗi vì đã bỏ về — hành động mà chính anh thừa nhận là sai.",
             "queries": ["Cristiano Ronaldo sad regretful expression"]},
            {"text": "Nhưng ngay câu tiếp theo, Ronaldo xoay lưỡi: lỗi không thuộc về một mình anh — Jorge Jesus đã phá vỡ lời hứa, anh đến với tư cách đội trưởng, với cam kết được đá chính, rồi tất cả sụp đổ chỉ sau một cuộc nói chuyện.",
             "queries": ["Cristiano Ronaldo speaking interview intense", "Jorge Jesus Ronaldo Portugal training conversation"]},
            {"text": "Ronaldo còn hé mở một chi tiết đau hơn: theo ESPN, anh chờ một lời xin lỗi công khai từ HLV tại họp báo — lời xin lỗi mà theo anh, hai bên đã thống nhất trước — nhưng Jorge Jesus đã không nói, không một từ.",
             "queries": ["press conference microphone football media", "Cristiano Ronaldo alone players tunnel"]},
            {"text": "Cánh cửa vừa hé rồi đóng sầm — vết nứt thành vực thẳm.",
             "queries": ["stadium tunnel door light darkness"]},
        ],
    },
    {
        "id": 4,
        "group": "Nhóm: Án Phạt & Trở Lại Sân Cỏ",
        "title": "Bản án 30 ngày, 255 euro và con số 40 giây phi lý",
        "title_queries": [
            "Portugal Football Federation FPF building",
            "football disciplinary red card referee",
            "Cristiano Ronaldo suspension news",
        ],
        "sentences": [
            {"text": "Ngày 10 tháng 10, Liên đoàn bóng đá Bồ Đào Nha ra quyết định đình chỉ tạm thời Cristiano Ronaldo, và giới truyền thông lập tức đề cập kịch bản tồi tệ nhất: theo VnExpress, siêu sao này có nguy cơ bị treo giò tới 6 tháng.",
             "queries": ["Cristiano Ronaldo banned news October 2026", "football red card referee showing"]},
            {"text": "Sáu tháng — nghĩa là vắng mặt tới tận cuối mùa giải, và với một cầu thủ 41 tuổi, mỗi tháng trôi qua đều là điều xa xỉ.",
             "queries": ["Cristiano Ronaldo veteran pitch older player"]},
            {"text": "Nhưng bản án cuối cùng, công bố ngày 19 tháng 10, lại khiến cả thế giới tròn mắt: 30 ngày đình chỉ, phạt 255 euro — khoảng 7,4 triệu đồng.",
             "queries": ["football sanction news newspaper headline"]},
            {"text": "Vì sao nhẹ hơn kịch bản?",
             "queries": ["Cristiano Ronaldo emotional interview"]},
            {"text": "Theo Yahoo Sports, Hội đồng kỷ luật Liên đoàn thừa nhận đã tính đến sự hối lỗi mà Ronaldo thể hiện trong tuyên bố ngày 6 tháng 10 — lời xin lỗi đã giúp giảm một nửa hình phạt.",
             "queries": ["Portuguese football federation Lisbon office building"]},
            {"text": "Nhưng khoan đã — 255 euro, với một Cristiano Ronaldo?",
             "queries": ["Cristiano Ronaldo surprised disbelief face"]},
            {"text": "Truyền thông quốc tế nhanh chóng bốc đơn giá cho các bạn dễ hình dung: mức thu nhập của Ronaldo tại Al Nassr tương đương khoảng 6,34 euro mỗi giây — nghĩa là khoản phạt 255 euro, anh kiếm lại chỉ sau 40 giây.",
             "queries": ["Al Nassr stadium Riyadh night lights", "euro banknotes money close up"]},
            {"text": "Bốn mươi giây, các bạn ạ — chưa kịp hết một hiệp đấu.",
             "queries": ["Cristiano Ronaldo hands on head pitch"]},
            {"text": "Một câu hỏi được ném ra khắp các trang báo: bản án này là để trừng phạt, hay chỉ để làm cho có?",
             "queries": ["sports newspapers stack front pages"]},
            {"text": "Dù thế nào, thông điệp của liên đoàn đã rõ: kỷ luật là kỷ luật — ngay cả với vua bóng đá.",
             "queries": ["football referee strict card match"]},
        ],
    },
    {
        "id": 5,
        "group": "Nhóm: Án Phạt & Trở Lại Sân Cỏ",
        "title": "Trận đấu trở lại: Ronaldo sút hỏng phạt đền trước Neom SC",
        "title_queries": [
            "Cristiano Ronaldo penalty Al Nassr 2026",
            "Al Nassr vs Neom SC Saudi Pro League",
            "Cristiano Ronaldo penalty miss reaction",
        ],
        "sentences": [
            {"text": "Bão tố trên đất Bồ Đào Nha, nhưng cuộc sống phải tiếp tục — Ronaldo quay về Al Nassr, nơi anh vẫn là vua, và nơi mùa giải 2026-27 là mùa giải chuyên nghiệp thứ 25 trong sự nghiệp.",
             "queries": ["Cristiano Ronaldo Al Nassr training 2026", "Cristiano Ronaldo Al Nassr yellow jersey 2026"]},
            {"text": "Ngày 20 tháng 10, Al Nassr tiếp Neom SC tại Saudi Pro League — trong bối cảnh đội bóng áo vàng xanh đang bám sát Al Hilal trên đỉnh bảng xếp hạng — trận đấu đầu tiên của Ronaldo sau cơn địa chấn, và người hâm mộ chờ một câu trả lời bằng bàn thắng.",
             "queries": ["Al Nassr stadium crowd Saudi Pro League 2026", "Saudi Pro League stadium atmosphere fans"]},
            {"text": "Cơ hội đến: quả phạt đền cho Al Nassr.",
             "queries": ["football penalty spot referee pointing whistle"]},
            {"text": "Ronaldo đặt bóng, chạy đà, sút — và thủ môn Neom SC đọc đúng hướng.",
             "queries": ["goalkeeper penalty save dive"]},
            {"text": "Theo ESPN, đó là lần thứ tư Ronaldo bỏ lỡ chấm 11 mét tại Saudi Pro League — cú sút lẽ ra là bàn thắng thứ 982 trong sự nghiệp, một bước nữa tới cột mốc thần thánh 1000, và nó bay đi trong câm lặng.",
             "queries": ["Cristiano Ronaldo penalty miss disappointed", "Cristiano Ronaldo miss reaction hands head"]},
            {"text": "May thay, Al Nassr vẫn thắng 1-0 — phút 61, người đồng hương João Félix ghi bàn duy nhất của trận, giữ vững vị trí thứ hai cho đội chủ nhà.",
             "queries": ["Joao Felix Al Nassr goal celebration"]},
            {"text": "Ba điểm được bảo toàn, nhưng cái giá tinh thần thì không đong đếm được — ở tuổi 41, sau tuần tồi tệ nhất sự nghiệp, ngay cả chấm phạt đền, thứ từng như cơm bữa, cũng tạm biệt Cristiano Ronaldo.",
             "queries": ["Cristiano Ronaldo walking pitch alone", "Cristiano Ronaldo night pitch reflection"]},
        ],
    },
    {
        "id": 6,
        "group": "Nhóm: Án Phạt & Trở Lại Sân Cỏ",
        "title": "Bàn thắng thứ 982 và cuộc tranh cãi giữa Opta và trọng tài",
        "title_queries": [
            "Cristiano Ronaldo goal celebration Al Nassr 2026",
            "Cristiano Ronaldo shot Al Faisaly goal",
            "Al Nassr Al Faisaly Saudi Pro League match",
        ],
        "sentences": [
            {"text": "Ba ngày sau, Al Nassr hành quân tới sân của Al Faisaly — và drama trở lại.",
             "queries": ["Al Faisaly Al Nassr match stadium"]},
            {"text": "Phút 49, Cristiano Ronaldo dứt điểm, bóng chạm chân hậu vệ Al Faisaly, đổi hướng và lăn vào lưới — Al Nassr thắng chung cuộc 3-1.",
             "queries": ["Cristiano Ronaldo striking goal shot Al Nassr"]},
            {"text": "Ronaldo ăn mừng như thể vừa ghi bàn thắng chung kết World Cup — với anh, đó là bàn thứ 982 của sự nghiệp, bàn thắng khép lại tuần đau đớn nhất cuộc đời.",
             "queries": ["Cristiano Ronaldo passionate celebration Al Nassr"]},
            {"text": "Nhưng rồi truyền thông thế giới bùng nổ.",
             "queries": ["sports news studio broadcast screens"]},
            {"text": "Theo Yahoo Sports, hãng thống kê Opta xác nhận đó không phải bàn của Ronaldo — mà là phản lưới nhà của cầu thủ Al Faisaly, với SofaScore và Flashscore ghi nhận tương tự.",
             "queries": ["football deflected goal net own goal"]},
            {"text": "Trên mạng xã hội, một bộ phận người hâm mộ không ngần ngại chế giễu 'bàn thắng ảo' của siêu sao 41 tuổi.",
             "queries": ["football fans smartphones social media stadium"]},
            {"text": "Chuyện chưa dừng ở đó — theo Goal.com, để chấm dứt tranh cãi, báo cáo của trọng tài trận đấu, ông Abdullah Al Owaidan, được đem ra làm phán quyết cuối cùng.",
             "queries": ["football referee notebook writing report"]},
            {"text": "Và trong biên bản chính thức, bàn thắng được ghi tên Cristiano Ronaldo — Saudi Pro League xác nhận bàn thứ 982 hợp lệ, cuộc đua tới 1000 tiếp tục.",
             "queries": ["Cristiano Ronaldo match ball record Al Nassr"]},
            {"text": "Một bàn thắng phải nhờ trọng tài phân xử mới thuộc về mình — với bất kỳ cầu thủ nào, đó là chuyện khó chịu, nhưng với Ronaldo ở khoảnh khắc này, nó giống một ẩn dụ cho cả chặng đường cuối sự nghiệp: bị nghi ngờ, bị cười cợt, rồi cuối cùng, theo cách này hay cách khác, con số vẫn thuộc về anh.",
             "queries": ["Cristiano Ronaldo determined face close up", "Cristiano Ronaldo celebration roar crowd", "Cristiano Ronaldo statistics scoreboard stadium"]},
        ],
    },
    {
        "id": 7,
        "group": "Nhóm: Hoài Niệm World Cup 2026",
        "title": "World Cup 2026: kỳ cuối cùng, kỷ lục 6 kỳ ghi bàn và giọt nước mắt",
        "title_queries": [
            "Cristiano Ronaldo Portugal World Cup 2026",
            "FIFA World Cup 2026 stadium crowd",
            "Cristiano Ronaldo World Cup 2026 celebration",
        ],
        "sentences": [
            {"text": "Để hiểu vì sao cơn bão tháng 10 này dữ dội đến vậy, chúng ta phải ngược thời gian về mùa hè năm 2026.",
             "queries": ["FIFA World Cup 2026 stadium atmosphere"]},
            {"text": "FIFA World Cup 2026 trên đất Bắc Mỹ — kỳ World Cup thứ sáu, cũng là kỳ cuối cùng, của Cristiano Ronaldo — 41 tuổi, anh đến không phải để ngắm cảnh.",
             "queries": ["Cristiano Ronaldo Portugal kit World Cup 2026"]},
            {"text": "Ngày 23 tháng 6, Bồ Đào Nha đè bẹp Uzbekistan 5-0, Ronaldo ghi hai bàn — và viết vào lịch sử một dòng không ai có thể xóa: cầu thủ đầu tiên trong lịch sử ghi bàn tại 6 kỳ World Cup, từ 2006 tới 2026, hai mươi năm, sáu kỳ World Cup, không một gián đoạn.",
             "queries": ["Cristiano Ronaldo goal Uzbekistan World Cup 2026", "Portugal Uzbekistan World Cup 2026 match", "Cristiano Ronaldo record celebration World Cup"]},
            {"text": "Hãy thử nghĩ xem: trong hai mươi năm ấy, bóng đá thế giới thay máu không biết bao nhiêu thế hệ cầu thủ — nhưng bảng ghi bàn luôn có một cái tên không đổi: Cristiano Ronaldo.",
             "queries": ["Cristiano Ronaldo stadium scoreboard screen"]},
            {"text": "Rồi vòng 32 đội, đối thủ Croatia — Bồ Đào Nha bị dẫn trước, lội ngược dòng và thắng 2-1 ngay trong giờ bù giờ, với bàn thắng knock-out đầu tiên trong sự nghiệp World Cup của Ronaldo.",
             "queries": ["Portugal Croatia World Cup 2026", "Cristiano Ronaldo knockout goal celebration"]},
            {"text": "Nghĩa là toàn bộ 8 bàn trước đó suốt 5 kỳ giải đều chỉ đến ở vòng bảng.",
             "queries": ["Cristiano Ronaldo World Cup 2018 hat trick Spain"]},
            {"text": "Tổng cộng tại World Cup 2026, anh rời giải với 3 bàn thắng, nâng tổng số bàn sự nghiệp tại các kỳ World Cup lên 11.",
             "queries": ["Cristiano Ronaldo World Cup 2026 walking pitch"]},
            {"text": "Nhưng định mệnh thì không phân biệt huyền thoại.",
             "queries": ["dramatic sky football stadium rain"]},
            {"text": "Ngày 6 tháng 7, vòng 16 đội, Tây Ban Nha — chín mươi phút chiến đấu, và một bàn thua duy nhất ở những phút cuối từ Mikel Merino, Bồ Đào Nha ra về.",
             "queries": ["Spain Portugal World Cup 2026 match"]},
            {"text": "World Cup cuối cùng của Cristiano Ronaldo khép lại không cùng cúp vàng, mà cùng... nước mắt.",
             "queries": ["Cristiano Ronaldo crying emotional"]},
            {"text": "Camera bắt khoảnh khắc anh bước xuống sân, tay che mặt.",
             "queries": ["Cristiano Ronaldo covering face tears"]},
            {"text": "Nhưng ngay sau trận, anh nói một câu đến giờ vẫn khiến người nghe rùng mình: 'Tôi ra về với lương tâm trong sáng.'",
             "queries": ["Cristiano Ronaldo post match interview World Cup"]},
            {"text": "Lương tâm trong sáng — các bạn ghi nhớ câu này, vì chỉ ba tháng sau, chính người mang 'lương tâm trong sáng' ấy sẽ bỏ về giữa đêm khỏi đội tuyển của mình, và đến giờ, cả thế giới vẫn đang tranh cãi: đêm 30 tháng 9 ấy, lương tâm đã đứng về phía ai?",
             "queries": ["Cristiano Ronaldo night leaving stadium", "Cristiano Ronaldo thoughtful portrait"]},
        ],
    },
    {
        "id": 8,
        "group": "Nhóm: Cuộc Đua 1000 Bàn",
        "title": "Cuộc đua 1000 bàn: 982 bàn đã có, 18 bàn nữa thôi",
        "title_queries": [
            "Cristiano Ronaldo Al Nassr trophy champions 2026",
            "Al Nassr Saudi Pro League champions celebration",
            "Cristiano Ronaldo goal record Al Nassr",
        ],
        "sentences": [
            {"text": "Giờ thì hãy nói về con số định mệnh: 1000.",
             "queries": ["Cristiano Ronaldo number 7 Al Nassr back"]},
            {"text": "Tính đến hôm nay, Cristiano Ronaldo đã ghi 982 bàn thắng chính thức trong sự nghiệp — chưa từng có cầu thủ nào trong lịch sử bóng đá chạm tới cột mốc 1000 bàn chính thức, và khoảng cách còn lại chỉ là 18 bàn.",
             "queries": ["Cristiano Ronaldo career goals record", "Cristiano Ronaldo goal statistics big screen stadium"]},
            {"text": "Mười tám bàn — với Ronaldo của mười năm trước là công việc của nửa mùa giải, nhưng với Ronaldo 41 tuổi, mùa giải thứ 25, mỗi bàn thắng đều là một trận chiến.",
             "queries": ["Cristiano Ronaldo training veteran fitness"]},
            {"text": "Nhưng đừng vội nghĩ cuộc đua đã kết thúc — hãy nhìn lại những gì anh làm tại Ả Rập Xê Út.",
             "queries": ["Riyadh Saudi Arabia skyline night"]},
            {"text": "Tháng 5 năm 2026, Ronaldo ghi hai bàn trong chiến thắng 4-1 trước Damac — bàn thứ 972 và 973 — đưa Al Nassr lên ngôi vô địch Saudi Pro League lần đầu tiên trong lịch sử CLB, và người nâng cúp lên chính là ông vua 41 tuổi.",
             "queries": ["Al Nassr Saudi Pro League champions trophy 2026", "Cristiano Ronaldo trophy lift Al Nassr"]},
            {"text": "Tháng 8 năm 2026, bàn thắng thứ 104 tại giải vô địch quốc gia Saudi giúp anh chính thức trở thành chân sút số một lịch sử Al Nassr — tổng cộng 135 bàn sau 160 trận khoác áo đội bóng áo vàng xanh.",
             "queries": ["Cristiano Ronaldo Al Nassr top scorer record", "Cristiano Ronaldo Al Nassr goal night celebration"]},
            {"text": "Mùa này, Al Nassr đang đứng thứ hai, bám sát Al Hilal — cuộc bảo vệ ngôi vô địch còn dài, và Ronaldo vẫn là niềm hy vọng số một của Riyadh.",
             "queries": ["Al Hilal Al Nassr match Saudi Pro League"]},
            {"text": "Với nhịp ghi bàn hiện tại, 18 bàn chỉ là chuyện của vài tháng — vậy câu hỏi không còn là 'Ronaldo có đủ khả năng ghi 18 bàn nữa không', mà là: cơ thể 41 tuổi ấy còn chịu đựng thêm bao nhiêu cú sốc, như cú sốc vừa qua, trước khi cột mốc 1000 đến?",
             "queries": ["Cristiano Ronaldo sprint run fast", "Cristiano Ronaldo injury pain pitch", "Cristiano Ronaldo pointing sky celebration"]},
        ],
    },
    {
        "id": 9,
        "group": "Nhóm: Cuộc Đua 1000 Bàn & Kết Cục",
        "title": "Ai sẽ nhíu mặt trước: ba kịch bản cho chương cuối",
        "title_queries": [
            "Jorge Jesus and Cristiano Ronaldo Portugal",
            "Portugal national team 2026 squad",
            "Cristiano Ronaldo future question",
        ],
        "sentences": [
            {"text": "Và bây giờ, quả bóng nằm ở... không ai biết rõ bên nào.",
             "queries": ["football on penalty spot grass night"]},
            {"text": "Cổng đội tuyển đóng với Ronaldo suốt 30 ngày — gần như chắc chắn anh vắng mặt ở đợt tập trung tháng 11, khi Bồ Đào Nha tiếp tục chiến dịch Nations League mà không có đội trưởng của mình.",
             "queries": ["Portugal national team squad 2026 Nations League", "Nations League Portugal match stadium"]},
            {"text": "Phía Jorge Jesus, cánh cửa 'vẫn mở' — nhưng kèm điều kiện thép, theo World Soccer Talk: Ronaldo phải chấp nhận vai trò mới, đôi khi đá chính, đôi khi vào sân từ ghế dự bị, đôi khi... không ra sân.",
             "queries": ["Jorge Jesus Portugal training session", "Cristiano Ronaldo substitute bench watching"]},
            {"text": "'Có trận anh sẽ chơi, có trận anh sẽ không' — và Jorge Jesus tuyên bố không nhún nhường một li nào.",
             "queries": ["Jorge Jesus arms crossed confident"]},
            {"text": "Phía Ronaldo — theo các nguồn gần cầu thủ — câu trả lời cứng không kém: anh sẽ không trở lại chừng nào Jorge Jesus còn ngồi ghế nóng.",
             "queries": ["Cristiano Ronaldo determined serious portrait"]},
            {"text": "Một bên đòi câu xin lỗi công khai, một bên đòi sự khuất phục hoàn toàn.",
             "queries": ["chess pieces confrontation strategy board"]},
            {"text": "Ba kịch bản mở ra.",
             "queries": ["stadium tunnel three paths light"]},
            {"text": "Một — Ronaldo cúi đầu, chấp nhận ghế dự bị, và biến nó thành màn chia tay đẹp với đội tuyển.",
             "queries": ["Cristiano Ronaldo farewell wave fans"]},
            {"text": "Hai — Jorge Jesus thất bại với kết quả nghèo nàn và ra đi, Ronaldo trở về như người hùng.",
             "queries": ["football hero welcome fans celebration"]},
            {"text": "Ba — không ai nhún nhường, sự nghiệp đội tuyển của Cristiano Ronaldo khép lại ở con số 233 trận, với dấu chấm lửng lớn nhất lịch sử bóng đá Bồ Đào Nha.",
             "queries": ["Cristiano Ronaldo Portugal jersey sunset pitch"]},
            {"text": "Còn với chúng ta, những người yêu bóng đá, câu hỏi cuối cùng chắc chắn không phải 'ai đúng ai sai' — mà là: khi nhắm mắt nghĩ về Cristiano Ronaldo, bạn muốn nhớ đêm anh bỏ về, hay nhớ cậu bé 18 tuổi chạy như gió, hai mươi năm ghi bàn tại 6 kỳ World Cup, và 982 bàn thắng chưa từng dừng lại?",
             "queries": ["young Cristiano Ronaldo Sporting Lisbon 2003", "Cristiano Ronaldo running sprint Portugal", "Cristiano Ronaldo siu celebration iconic"]},
            {"text": "Cuộc đua 1000 bàn vẫn tiếp tục, cơn bão vẫn chưa qua — và ở nơi đâu đó trên sân tập Al Nassr, một người đàn ông 41 tuổi vẫn đang tập sút.",
             "queries": ["Cristiano Ronaldo training shooting practice"]},
            {"text": "Nếu bạn muốn theo dõi chương tiếp theo của huyền thoại này, cùng tin nóng thể thao mỗi sáng và chuyên đề sâu mỗi tuần, hãy đăng ký kênh Điểm Đọc, bấm chuông thông báo, và để lại suy nghĩ ở phần bình luận: bạn đứng về Ronaldo hay Jorge Jesus?",
             "queries": ["Cristiano Ronaldo fans crowd support", "Jorge Jesus Portugal supporters"]},
            {"text": "Điểm Đọc — đọc tin, hiểu chuyện, thấy tinh thần — hẹn gặp lại!",
             "queries": ["football stadium night lights atmosphere crowd"]},
        ],
    },
]

# ------------------------------------------------------------------ CẤU HÌNH LỌC ẢNH
MIN_RATIO = 1.18        # ảnh ngang chuẩn 16:9
MIN_WIDTH = 800         # độ phân giải tối thiểu
NEG_KW = " -game -mobile -esports -wallpaper"
BLOCKED_HOSTS = [
    "alamy", "gettyimages", "istockphoto", "shutter", "dreamstime", "123rf",
    "depositphotos", "stock.adobe", "freepik", "pinterest", "facebook.",
    "instagram.", "tiktok", "wallpaper", "alphacoders", "deviantart",
    "futbin", "futhead", "sofifa", "vectorstock", "storyblocks", "picfair",
    # Nguồn rác phát hiện qua QA vòng 1-5 (watermark / đồ họa / 3D / collage):
    "vecteezy", "bigstock", "ebay", "etsy", "redbubble", "teepublic",
    "society6", "displate", "ytimg", "pngtree", "cgtrader", "footyheadlines",
    "webcamsus", "twimg", "idman.biz", "hudl", "videoblocks", "ftcdn",
    "fotolia", "huggingface", "hf.co", "pond5", "mixkit", "motionarray",
    "collage", "forum", "pinimg",
]
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
    px = list(g.getdata())
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
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                    encoding="utf-8")


def host_blocked(url):
    low = url.lower()
    return any(b in low for b in BLOCKED_HOSTS) or "watermark" in low

# ------------------------------------------------------------------ KẾ HOẠCH ẢNH
def build_plan():
    """Sinh danh sách slot ảnh theo luật độ dài câu."""
    plan = []  # mỗi slot: dict(scene, sent_idx, kind, label, query, fname, wc)
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
                qs.append(qs[len(qs) % max(1, len(s["queries"]))] + " football photo")
            for j in range(n):
                plan.append(dict(scene=sid, sent_idx=i, kind="sentence",
                                 label=lab, query=qs[j], fname=fname(), wc=words))
    return plan


def write_kich_ban(plan):
    lines = []
    lines.append("=" * 80)
    lines.append("KỊCH BẢN PHÂN TÁCH TỪNG CÂU & KẾ HOẠCH HÌNH ẢNH — NGÀY 25.10.2026")
    lines.append(f"Chủ đề: Chuyên đề Cristiano Ronaldo — \"{VIDEO_TITLE}\"")
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
    lines = [f"BẢN TIN THỂ THAO — CHUYÊN ĐỀ CRISTIANO RONALDO — 25.10.2026",
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
        self.used_hashes = []      # [(fname, hash)]
        self.plan_log = []         # provenance từng slot
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": UA})

    # ---- tìm kiếm (có cache đĩa + retry) ----
    def search(self, query):
        key = query + "|" + NEG_KW
        if key in self.qcache:
            return self.qcache[key]
        for attempt in range(4):
            try:
                with DDGS() as ddgs:
                    res = ddgs.images(key, region="wt-wt",
                                      safesearch="off", size="Large",
                                      layout="Wide", max_results=28)
                res = list(res)
                self.qcache[key] = res
                save_json(QCACHE, self.qcache)
                return res
            except Exception as e:
                wait = 12 * (attempt + 1)
                print(f"    [search retry {attempt+1}] {type(e).__name__}: {e} -> sleep {wait}s", flush=True)
                time.sleep(wait)
        return []

    # ---- tải 1 ứng viên, trả về (PIL.Image, url) hoặc None ----
    def fetch(self, url):
        if host_blocked(url):
            return None
        low = url.lower().split("?")[0]
        if low.endswith((".svg", ".gif")):
            return None
        try:
            r = self.session.get(url, timeout=18, stream=False)
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

    # ---- tải 1 slot: duyệt ứng viên tới khi đạt ----
    def fill_slot(self, slot, used_map):
        out_path = IMG_DIR / slot["fname"]
        if out_path.exists():
            return "kept"
        query = slot["query"]
        cands = self.search(query)
        # Ưu tiên ứng viên có metadata ngang & lớn
        def rank(c):
            try:
                w = int(c.get("width") or 0); h = int(c.get("height") or 0)
                return (0 if (w and w / max(h, 1) >= MIN_RATIO) else 1, -w)
            except Exception:
                return (1, 0)
        cands = sorted(cands, key=rank)
        for c in cands:
            url = c.get("image") or ""
            if not url.startswith("http"):
                continue
            img = self.fetch(url)
            if img is None:
                continue
            h_val = ahash(img)
            dup = None
            for fn, uh in used_map:
                if hamming(h_val, uh) <= 6:
                    dup = fn
                    break
            if dup:
                continue
            out_path.write_bytes(b"")
            img.save(out_path, "JPEG", quality=88)
            used_map.append((slot["fname"], h_val))
            self.plan_log.append(dict(
                fname=slot["fname"], scene=slot["scene"],
                sent_idx=slot["sent_idx"], kind=slot["kind"],
                query=query, source=url,
                source_site=c.get("source", ""),
                width=img.size[0], height=img.size[1]))
            return "ok"
        return "MISSING"

# ------------------------------------------------------------------ CONTACT SHEET
def make_sheets():
    files = sorted(IMG_DIR.glob("Tin_*.jpg"))
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
        cols, tw = 5, 300
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
        sheet.save(out, "JPEG", quality=82)
        print(f"  sheet: {out.name} ({len(fs)} ảnh)")

# ------------------------------------------------------------------ MAIN
def main():
    args = sys.argv[1:]
    if "--sheets" in args:
        make_sheets()
        return

    force = "--force" in args
    if force:
        for f in IMG_DIR.glob("Tin_*.jpg"):
            f.unlink()

    plan = build_plan()
    total = write_kich_ban(plan)
    write_thethao_txt()
    print(f"[PLAN] {total} slot ảnh | kich_ban_tung_cau.txt + thethao.txt đã ghi", flush=True)

    hunter = Hunter()
    # Khôi phục bảng hash từ ảnh đã tải (resume)
    used_map = []
    for f in sorted(IMG_DIR.glob("Tin_*.jpg")):
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
        time.sleep(0.35)

    # Ghi nhật ký nguồn ảnh + thethao.json skeleton (gộp với log cũ, không ghi đè)
    plan_path = DAY / "image_plan.json"
    prev = load_json(plan_path, {})
    prev_slots = {s["fname"]: s for s in prev.get("slots", [])}
    for s in hunter.plan_log:
        prev_slots[s["fname"]] = s
    save_json(plan_path, dict(
        video_title=VIDEO_TITLE, day="25.10.2026",
        total_slots=len(plan), downloaded=ok, kept=kept, missing=miss,
        slots=list(prev_slots.values())))

    items = []
    for sc in SCENES:
        sid = sc["id"]
        imgs = [f for f in sorted(IMG_DIR.glob(f"Tin_{sid:02d}_*.jpg"))]
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

    make_sheets()
    print(f"[DONE] ok={ok} kept={kept} missing={miss} / {len(plan)} "
          f"trong {time.time()-t0:.0f}s", flush=True)
    print(f"[ARTIFACT] {DAY / 'kich_ban_tung_cau.txt'}")
    print(f"[ARTIFACT] {DAY / 'thethao.json'} + thethao.txt + image_plan.json")
    print(f"[QA] Contact sheets: {QA_DIR}")


if __name__ == "__main__":
    main()
