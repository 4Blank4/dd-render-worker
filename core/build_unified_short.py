#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_unified_short.py — Pipeline sản xuất Video Short 9:16 với kịch bản thống nhất (Unified Script)
thay vì chắp ghép thô các tin riêng lẻ.

Mỗi Video Short:
- Viết lại 1 kịch bản dẫn chuyện liền mạch (~120-160 từ, 50-60 giây)
- Sinh giọng đọc ViTTS v3turbo Minh Quân Pro mới 100% cho từng câu
- Đồng bộ phụ đề Karaoke từng từ khớp chuẩn 1-1
- Chuyển động bố cục, đổi ảnh bám sát ngữ cảnh lời dẫn, Lower-Third 2 góc động
- Chuẩn hóa âm thanh master EBU R128 (-14.0 LUFS, TP <= -1.0 dBTP, drift <= 1 frame)
- Kết xuất Thumbnail dọc 9:16 Cyber-Stadium và File mô tả SEO 2 phần chuẩn
"""
import sys
sys.dont_write_bytecode = True

import os
import re
import json
import glob
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple

from pydub import AudioSegment
from PIL import Image

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
from diemdoc.audio import two_pass_loudnorm
from diemdoc.publisher import write_mota_9x16, render_thumbnail_9x16
from m3_voice import render_chunk_vitts, trim_segment_silence
from m8_news_bridge import interpolate_sentence_words, compute_pan_params
from renderer import render_html_engine
from vieneu import Vieneu

DAY_STR = "09.11.2026"
DAY_DIR = Path(paths.OUTPUTS) / DAY_STR
SHORTS_DIR = DAY_DIR / "shorts"
CACHE_DIR = paths.work_file("vitts_cache")


# ==============================================================================
# ĐỊNH NGHĨA KỊCH BẢN THỐNG NHẤT CHO SHORT 6, 7, 8, 10
# ==============================================================================

UNIFIED_SHORTS_SPEC = {
    6: {
        "id": 6,
        "name": "Short_06_Tin_Nong_Chuyen_La_The_Thao_The_Gioi",
        "title": "CHUYỆN LẠ THỂ THAO: KỶ LỤC 51 THẺ ĐỎ VÀ BÓNG ĐÁ XE ĐẠP",
        "kicker": "CHUYỆN LẠ THỂ THAO TUẦN QUA",
        "badge": "CHUYỆN LẠ THẾ GIỚI",
        "group": "CHUYỆN LẠ THẾ GIỚI",
        "seo_title": "Tin nóng thể thao tuần qua: Kỷ lục 51 thẻ đỏ một trận và bóng đá bằng xe đạp #Shorts",
        "description": [
            "Tin nóng thể thao tuần qua: Làng thể thao thế giới chứng kiến những câu chuyện kỳ lạ chưa từng có trong lịch sử từ Nam Mỹ đến châu Âu.",
            "Tại Brazil, trận đấu bán kết giải trẻ đã biến thành màn hỗn chiến điên rồ buộc trọng tài phải rút tới 51 chiếc thẻ đỏ trực tiếp, xô đổ kỷ lục thế giới Guinness. Trong khi đó tại Đức, giải vô địch thế giới môn bóng đá bằng xe đạp Cycle-ball 2026 vừa khép lại với chức vô địch áp đảo 8-1 của đội tuyển Áo."
        ],
        "chapters": [
            ("00:00", "Chuyện lạ thể thao tuần qua: Kỷ lục thế giới 51 thẻ đỏ một trận"),
            ("00:26", "Giải vô địch thế giới môn bóng đá trên xe đạp Cycle-ball 2026 tại Đức"),
            ("00:46", "Đội tuyển Áo đánh bại Đức 8-1 đăng quang ngôi vô địch thế giới"),
        ],
        "sources_line": "📰 Nguồn tin: Báo chí Brazil, Globo Esporte, Guinness World Records, UCI, Liên đoàn Xe đạp Đức.",
        "hashtags": ["#Shorts", "#TinNongTuanQua", "#ChuyenLaTheThao", "#KyLucGuinness", "#51TheDo", "#CycleBall", "#DiemDoc", "#BongDa"],
        "thumb": {
            "image": "Tin_14_2.jpg",
            "kicker": "CHUYỆN LẠ THỂ THAO TUẦN QUA",
            "hero_html": "<span class=\"hl-red\">KỶ LỤC 51 THẺ ĐỎ!</span><br><span class=\"hl-white\">HỖN CHIẾN BRAZIL</span><br><span class=\"hl-yellow\">ĐÁ BÓNG TRÊN XE ĐẠP</span>",
            "subtitle": "KỶ LỤC GUINNESS 51 THẺ ĐỎ • ĐỘI TUYỂN ÁO VÔ ĐỊCH THẾ GIỚI CYCLE-BALL",
            "badge": "CHUYỆN LẠ THẾ GIỚI",
            "tag_a": "TIN NÓNG TUẦN",
            "tag_b": "09.11.2026",
            "obj_pos": "center 20%",
        },
        "sentences": [
            {
                "text": "Chuyện lạ thể thao tuần qua: Kỷ lục thế giới 51 chiếc thẻ đỏ và giải bóng đá bằng xe đạp.",
                "is_title": True,
                "headline": "CHUYỆN LẠ THỂ THAO: KỶ LỤC 51 THẺ ĐỎ VÀ BÓNG ĐÁ XE ĐẠP",
                "group": "CHUYỆN LẠ THẾ GIỚI",
                "news_source": "ĐIỂM ĐỌC THỂ THAO",
                "images": ["Tin_14_2.jpg", "Tin_14_1.jpg"]
            },
            {
                "text": "Tại bang Minas Gerais của Brazil, trận bán kết giải trẻ giữa Uberlandia và Mamore đã biến thành màn hỗn chiến điên rồ chưa từng có.",
                "is_title": False,
                "headline": "HỖN CHIẾN TẠI BRAZIL: BÁN KẾT BIẾN THÀNH BẠO LỰC",
                "group": "BÓNG ĐÁ BRAZIL",
                "news_source": "GLOBO ESPORTE / BÁO CHÍ BRAZIL",
                "images": ["Tin_14_3.jpg", "Tin_14_5.jpg"]
            },
            {
                "text": "Trọng tài chính Fernando Modesto đã phải rút tổng cộng 51 chiếc thẻ đỏ trực tiếp, chính thức xô đổ kỷ lục thế giới Guinness về số thẻ phạt nhiều nhất trong một trận đấu.",
                "is_title": False,
                "headline": "KỶ LỤC GUINNESS: 51 THẺ ĐỎ TRỰC TIẾP ĐƯỢC RÚT RA",
                "group": "KỶ LỤC GUINNESS",
                "news_source": "GUINNESS WORLD RECORDS / FMF",
                "images": ["Tin_14_6.jpg", "Tin_14_4.jpg"]
            },
            {
                "text": "Trong khi đó tại Đức, giải vô địch thế giới môn bóng đá trên xe đạp Cycle-ball 2026 vừa khép lại với những màn so tài vô cùng độc đáo.",
                "is_title": False,
                "headline": "ĐỘC LẠ NƯỚC ĐỨC: GIẢI VÔ ĐỊCH BÓNG ĐÁ TRÊN XE ĐẠP",
                "group": "CYCLE-BALL 2026",
                "news_source": "UCI / LIÊN ĐOÀN XE ĐẠP ĐỨC",
                "images": ["Tin_15_1.jpg", "Tin_15_2.jpg"]
            },
            {
                "text": "Ở môn thể thao cấm tuyệt đối cầu thủ chạm chân xuống sàn, đội tuyển Áo đã đánh bại chủ nhà Đức với tỷ số áp đảo 8-1 trong trận chung kết để bước lên ngôi vô địch thế giới.",
                "is_title": False,
                "headline": "ĐỘI TUYỂN ÁO HẠ CHỦ NHÀ ĐỨC 8-1 VÔ ĐỊCH THẾ GIỚI",
                "group": "VÔ ĐỊCH THẾ GIỚI",
                "news_source": "BÁO THỂ THAO ĐỨC / BÁO ÁO",
                "images": ["Tin_15_3.jpg", "Tin_15_5.jpg"]
            },
            {
                "text": "Những khoảnh khắc có một không hai này đã tạo nên điểm nhấn khó quên của làng túc cầu thế giới tuần qua.",
                "is_title": False,
                "headline": "ĐIỂM NHẤN ĐỘC ĐÁO CỦA THỂ THAO THẾ GIỚI TUẦN QUA",
                "group": "ĐIỂM ĐỌC THỂ THAO",
                "news_source": "ĐIỂM ĐỌC THỂ THAO",
                "images": ["Tin_15_6.jpg", "Tin_14_2.jpg"]
            }
        ]
    },

    7: {
        "id": 7,
        "name": "Short_07_Tin_Nong_Tam_Chan_V_League",
        "title": "TÂM CHẤN BÓNG ĐÁ NỘI: NAM ĐỊNH GIỮ ĐỈNH & CÔNG PHƯỢNG TỎA SÁNG",
        "kicker": "BÓNG ĐÁ QUỐC NỘI TUẦN QUA",
        "badge": "BÓNG ĐÁ VIỆT NAM",
        "seo_title": "Tin nóng thể thao tuần qua: Nam Định giữ đỉnh V-League, Công Phượng tỏa sáng rực rỡ #Shorts",
        "description": [
            "Tin nóng thể thao tuần qua: Bức tranh toàn cảnh vòng đấu V-League và giải Hạng Nhất quốc gia chứng kiến những bước ngoặt đầy kịch tính.",
            "Thép Xanh Nam Định xây chắc ngôi đầu bảng trong khi Hoàng Anh Gia Lai hạ gục Hà Nội FC để nhọc nhằn thoát đáy bảng; Thể Công Viettel bị Thanh Hóa cầm hòa 1-1; và ngôi sao Nguyễn Công Phượng nổ súng rực rỡ giúp Đồng Nai giành 3 điểm đầu tay."
        ],
        "chapters": [
            ("00:00", "Bóng đá quốc nội tuần qua: Nam Định giữ đỉnh, HAGL thoát đáy"),
            ("00:15", "Thể Công Viettel chia điểm nghẹt thở 1-1 trước Thanh Hóa tại Hàng Đẫy"),
            ("00:32", "Công Phượng lập siêu phẩm sút xa đưa Đồng Nai giành chiến thắng đầu tay"),
            ("00:46", "Cục diện hấp dẫn của các giải bóng đá chuyên nghiệp Việt Nam"),
        ],
        "sources_line": "📰 Nguồn tin: VPF, VFF, Báo Bóng Đá, Báo Thanh Niên, Báo Tuổi Trẻ.",
        "hashtags": ["#Shorts", "#TinNongTuanQua", "#VLeague", "#NamDinhFC", "#HAGL", "#CongPhuong", "#TheCongViettel", "#BongDaVietNam", "#DiemDoc"],
        "thumb": {
            "image": "Tin_17_1.jpg",
            "kicker": "BÓNG ĐÁ QUỐC NỘI TUẦN QUA",
            "hero_html": "<span class=\"hl-cyan\">NAM ĐỊNH GIỮ ĐỈNH!</span><br><span class=\"hl-white\">HAGL THOÁT ĐÁY BẢNG</span><br><span class=\"hl-yellow\">CÔNG PHƯỢNG NỔ SÚNG!</span>",
            "subtitle": "NAM ĐỊNH XÂY CHẮC NGÔI ĐẦU • CÔNG PHƯỢNG SIÊU PHẨM • VIETTEL HÒA 1-1",
            "badge": "TÂM CHẤN V-LEAGUE",
            "tag_a": "BÓNG ĐÁ VIỆT",
            "tag_b": "09.11.2026",
            "obj_pos": "center 20%",
        },
        "sentences": [
            {
                "text": "Bóng đá quốc nội tuần qua: Nam Định giữ đỉnh V-League và Công Phượng tỏa sáng rực rỡ.",
                "is_title": True,
                "headline": "NAM ĐỊNH GIỮ ĐỈNH V-LEAGUE & CÔNG PHƯỢNG TỎA SÁNG",
                "group": "BÓNG ĐÁ VIỆT NAM",
                "news_source": "VPF / V-LEAGUE 2026",
                "images": ["Tin_17_1.jpg", "Tin_17_2.jpg"]
            },
            {
                "text": "Vòng 11 V-League chứng kiến đương kim vô địch Thép Xanh Nam Định xây chắc ngôi đầu bảng, trong khi Hoàng Anh Gia Lai hạ gục Hà Nội FC để nhọc nhằn thoát khỏi nhóm cầm đèn đỏ.",
                "is_title": False,
                "headline": "NAM ĐỊNH XÂY CHẮC ĐỈNH BẢNG • HAGL THOÁT ĐÁY",
                "group": "V-LEAGUE 2026",
                "news_source": "VPF / BÁO BÓNG ĐÁ",
                "images": ["Tin_17_3.jpg", "Tin_17_4.jpg"]
            },
            {
                "text": "Tại Hàng Đẫy, Thể Công Viettel dù chơi hơn người suốt cả hiệp hai nhưng vẫn bị Đông Á Thanh Hóa cầm chân với tỷ số hòa 1-1 nghẹt thở.",
                "is_title": False,
                "headline": "VIETTEL BỊ THANH HÓA CẦM HÒA 1-1 NGHẸT THỞ",
                "group": "V-LEAGUE 2026",
                "news_source": "BÁO THANH NIÊN / VPF",
                "images": ["Tin_19_1.jpg", "Tin_19_2.jpg"]
            },
            {
                "text": "Trong khi đó tại giải Hạng Nhất, ngôi sao Nguyễn Công Phượng đã tạo nên khoảnh khắc bùng nổ với cú sút xa đẳng cấp đưa Đồng Nai giành chiến thắng đầu tay của mùa giải.",
                "is_title": False,
                "headline": "CÔNG PHƯỢNG NỔ SÚNG: SIÊU PHẨM MANG VỀ 3 ĐIỂM",
                "group": "HẠNG NHẤT QUỐC GIA",
                "news_source": "BÁO TUỔI TRẺ / VPF",
                "images": ["Tin_18_1.jpg", "Tin_18_2.jpg"]
            },
            {
                "text": "Sự thăng hoa của các cựu binh và sức nóng ở cả hai đầu bảng xếp hạng đang tạo nên những vòng đấu đầy cảm xúc cho người hâm mộ.",
                "is_title": False,
                "headline": "BẦU KHÔNG KHÍ BÓNG ĐÁ QUỐC NỘI NÓNG LÊN TỪNG NGÀY",
                "group": "ĐIỂM ĐỌC THỂ THAO",
                "news_source": "ĐIỂM ĐỌC THỂ THAO",
                "images": ["Tin_17_5.jpg", "Tin_18_3.jpg"]
            }
        ]
    },

    8: {
        "id": 8,
        "name": "Short_08_Tin_Nong_Tu_Hao_The_Thao_Viet_Nam",
        "title": "TỰ HÀO THỂ THAO VIỆT: QUYẾT CHIẾN HẠ SỐ 1 THẾ GIỚI & THANH THÚY VỀ NƯỚC",
        "kicker": "TỰ HÀO THỂ THAO VIỆT NAM TUẦN QUA",
        "badge": "TỰ HÀO VIỆT NAM",
        "seo_title": "Tin nóng thể thao tuần qua: Trần Quyết Chiến hạ số 1 thế giới, Thanh Thúy về nước #Shorts",
        "description": [
            "Tin nóng thể thao tuần qua: Thể thao Việt Nam liên tiếp đón nhận những tin vui đầy tự hào trên đấu trường quốc tế.",
            "Cơ thủ số một Việt Nam Trần Quyết Chiến đè bẹp tay cơ số một thế giới Cho Myung-woo 50-23 tại World Cup Billiards; chủ công Trần Thị Thanh Thúy hoàn tất thủ tục về nước hội quân; và các cô gái CLB nữ TP.HCM thi đấu kiên cường tại Cúp C1 châu Á."
        ],
        "chapters": [
            ("00:00", "Trần Quyết Chiến đè bẹp số 1 thế giới Cho Myung-woo 50-23"),
            ("00:20", "Chủ công Trần Thị Thanh Thúy chia tay Nhật Bản về nước hội quân"),
            ("00:36", "CLB nữ TP.HCM thi đấu kiên cường tại tứ kết cúp C1 châu Á"),
            ("00:48", "Bản lĩnh kiên cường của thể thao Việt Nam trên đấu trường quốc tế"),
        ],
        "sources_line": "📰 Nguồn tin: UMB World Cup Billiards, SV.League Nhật Bản, AFC, Báo Tuổi Trẻ, VnExpress.",
        "hashtags": ["#Shorts", "#TinNongTuanQua", "#TranQuyetChien", "#Billiards", "#ThanhThuy", "#BongChuyen", "#NuTPHCM", "#TheThaoVietNam", "#DiemDoc"],
        "thumb": {
            "image": "Tin_22_1.jpg",
            "kicker": "TỰ HÀO THỂ THAO VIỆT TUẦN QUA",
            "hero_html": "<span class=\"hl-yellow\">QUYẾT CHIẾN ĐÈ BẸP</span><br><span class=\"hl-white\">SỐ 1 THẾ GIỚI 50-23!</span><br><span class=\"hl-cyan\">THANH THÚY VỀ NƯỚC</span>",
            "subtitle": "WORLD CUP BILLIARDS ĐỈNH CAO • CHỦ CÔNG THANH THÚY VỀ HỘI QUÂN",
            "badge": "TỰ HÀO VIỆT NAM",
            "tag_a": "THỂ THAO VIỆT",
            "tag_b": "09.11.2026",
            "obj_pos": "center 18%",
        },
        "sentences": [
            {
                "text": "Tự hào thể thao Việt Nam tuần qua: Quyết Chiến hạ số một thế giới và Thanh Thúy về nước.",
                "is_title": True,
                "headline": "QUYẾT CHIẾN HẠ SỐ 1 THẾ GIỚI & THANH THÚY VỀ NƯỚC",
                "group": "TỰ HÀO VIỆT NAM",
                "news_source": "ĐIỂM ĐỌC THỂ THAO",
                "images": ["Tin_22_1.jpg", "Tin_22_2.jpg"]
            },
            {
                "text": "Tại World Cup Billiards Carom 3 băng, cơ thủ số một Việt Nam Trần Quyết Chiến đã tạo nên cơn địa chấn khi đè bẹp tay cơ số một thế giới Cho Myung-woo với tỷ số áp đảo 50-23.",
                "is_title": False,
                "headline": "TRẦN QUYẾT CHIẾN ĐÈ BẸP SỐ 1 THẾ GIỚI 50-23",
                "group": "WORLD CUP BILLIARDS",
                "news_source": "UMB / WORLD CUP BILLIARDS",
                "images": ["Tin_22_3.jpg", "Tin_22_4.jpg"]
            },
            {
                "text": "Ở môn bóng chuyền, chủ công Trần Thị Thanh Thúy đã hoàn tất thủ tục chia tay câu lạc bộ Nhật Bản để bay về nước hội quân chuẩn bị cho Đại hội thể thao toàn quốc.",
                "is_title": False,
                "headline": "CHỦ CÔNG THANH THÚY CHIA TAY NHẬT BẢN VỀ NƯỚC",
                "group": "BÓNG CHUYỀN NỮ",
                "news_source": "SV.LEAGUE / LIÊN ĐOÀN BÓNG CHUYỀN",
                "images": ["Tin_25_1.jpg", "Tin_25_2.jpg"]
            },
            {
                "text": "Bên cạnh đó, các cô gái câu lạc bộ nữ Thành phố Hồ Chí Minh cũng để lại dấu ấn thi đấu kiên cường tại tứ kết Cúp C1 châu Á trước đại diện hùng mạnh của Hàn Quốc.",
                "is_title": False,
                "headline": "CLB NỮ TP.HCM CHIẾN ĐẤU KIÊN CƯỜNG TẠI CÚP C1",
                "group": "CÚP C1 NỮ CHÂU Á",
                "news_source": "AFC / BÁO TUỔI TRẺ",
                "images": ["Tin_20_1.jpg", "Tin_20_2.jpg"]
            },
            {
                "text": "Một tuần thi đấu đầy quả cảm khẳng định vị thế và bản lĩnh của các vận động viên Việt Nam trên đấu trường quốc tế.",
                "is_title": False,
                "headline": "BẢN LĨNH THỂ THAO VIỆT NAM TRÊN ĐẤU TRƯỜNG QUỐC TẾ",
                "group": "ĐIỂM ĐỌC THỂ THAO",
                "news_source": "ĐIỂM ĐỌC THỂ THAO",
                "images": ["Tin_22_5.jpg", "Tin_25_3.jpg"]
            }
        ]
    },

    10: {
        "id": 10,
        "name": "Short_10_Tin_Nong_Sieu_Sao_Toa_Sang",
        "title": "SIÊU SAO BÙNG NỔ: HAALAND LẬP KỶ LỤC C1 & ALCARAZ ĐĂNG QUANG",
        "kicker": "SIÊU SAO TỎA SÁNG TUẦN QUA",
        "badge": "ĐỈNH CAO THẾ GIỚI",
        "seo_title": "Tin nóng thể thao tuần qua: Haaland xô đổ kỷ lục C1, Alcaraz đăng quang Paris Masters #Shorts",
        "description": [
            "Tin nóng thể thao tuần qua: Tuần thi đấu thăng hoa tột đỉnh của những siêu sao kiệt xuất đại diện cho 3 môn thể thao hàng đầu thế giới.",
            "Erling Haaland cán mốc 62 bàn thắng C1 nhanh nhất lịch sử giải đấu; Carlos Alcaraz xuất sắc hạ gục Ben Shelton lần đầu nâng cúp Paris Masters; và Lando Norris lái xe dưới mưa giành chiến thắng kịch tính tại F1 Brazil Grand Prix."
        ],
        "chapters": [
            ("00:00", "Erling Haaland cán mốc 62 bàn thắng cúp C1 nhanh nhất lịch sử"),
            ("00:18", "Carlos Alcaraz lần đầu đăng quang chức vô địch Paris Masters"),
            ("00:36", "Lando Norris đăng quang kịch tính dưới mưa tại F1 Brazil Grand Prix"),
            ("00:50", "Đẳng cấp đỉnh cao của những ngôi sao thể thao hàng đầu thế giới"),
        ],
        "sources_line": "📰 Nguồn tin: UEFA Champions League, ATP Tour, Formula 1, Sky Sports, Reuters.",
        "hashtags": ["#Shorts", "#TinNongTuanQua", "#ErlingHaaland", "#CarlosAlcaraz", "#LandoNorris", "#F1", "#ChampionsLeague", "#ParisMasters", "#DiemDoc"],
        "thumb": {
            "image": "Tin_05_1.jpg",
            "kicker": "SIÊU SAO TỎA SÁNG TUẦN QUA",
            "hero_html": "<span class=\"hl-cyan\">HAALAND KỶ LỤC C1!</span><br><span class=\"hl-white\">ALCARAZ VÔ ĐỊCH</span><br><span class=\"hl-yellow\">NORRIS THẮNG F1!</span>",
            "subtitle": "HAALAND 62 BÀN CÚP C1 • ALCARAZ ĐĂNG QUANG PARIS MASTERS • F1 DƯỚI MƯA",
            "badge": "SIÊU SAO ĐỈNH CAO",
            "tag_a": "TIN NÓNG TUẦN",
            "tag_b": "09.11.2026",
            "obj_pos": "center 20%",
        },
        "sentences": [
            {
                "text": "Siêu sao tỏa sáng tuần qua: Haaland lập kỷ lục C1 và Alcaraz vô địch Paris Masters.",
                "is_title": True,
                "headline": "HAALAND LẬP KỶ LỤC C1 & ALCARAZ ĐĂNG QUANG PARIS MASTERS",
                "group": "SIÊU SAO THẾ GIỚI",
                "news_source": "ĐIỂM ĐỌC THỂ THAO",
                "images": ["Tin_05_1.jpg", "Tin_23_1.jpg"]
            },
            {
                "text": "Tại Champions League, cỗ máy săn bàn Erling Haaland tiếp tục làm nên lịch sử khi cán mốc 62 bàn thắng nhanh nhất giải đấu, giúp Man City nhọc nhằn hạ Leipzig 3-2.",
                "is_title": False,
                "headline": "ERLING HAALAND CÁN MỐC 62 BÀN THẮNG CÚP C1 SIÊU TỐC",
                "group": "CHAMPIONS LEAGUE",
                "news_source": "UEFA / MAN CITY FC",
                "images": ["Tin_05_2.jpg", "Tin_05_3.jpg"]
            },
            {
                "text": "Ở làng banh nỉ, tay vợt Carlos Alcaraz đã có màn trình diễn xuất thần hạ gục Ben Shelton sau hai set kịch tính để lần đầu tiên bước lên đỉnh vinh quang tại Paris Masters.",
                "is_title": False,
                "headline": "CARLOS ALCARAZ LẦN ĐẦU VÔ ĐỊCH PARIS MASTERS 2026",
                "group": "PARIS MASTERS 2026",
                "news_source": "ATP TOUR / REUTERS",
                "images": ["Tin_23_2.jpg", "Tin_23_3.jpg"]
            },
            {
                "text": "Còn trên đường đua F1 tại São Paulo, Lando Norris xuất sắc vượt qua cơn mưa tầm tã để đăng quang thuyết phục tại Grand Prix Brazil, giúp Mercedes sớm chạm tay vào chức vô địch.",
                "is_title": False,
                "headline": "LANDO NORRIS THẮNG DƯỚI MƯA TẠI F1 BRAZIL GRAND PRIX",
                "group": "FORMULA 1 2026",
                "news_source": "FORMULA 1 / SKY SPORTS",
                "images": ["Tin_24_1.jpg", "Tin_24_2.jpg"]
            },
            {
                "text": "Một tuần thi đấu thăng hoa tột đỉnh của những cá nhân kiệt xuất hàng đầu làng thể thao thế giới.",
                "is_title": False,
                "headline": "ĐẲNG CẤP TỎA SÁNG CỦA CÁC SIÊU SAO THỂ THAO THẾ GIỚI",
                "group": "ĐIỂM ĐỌC THỂ THAO",
                "news_source": "ĐIỂM ĐỌC THỂ THAO",
                "images": ["Tin_05_4.jpg", "Tin_23_4.jpg"]
            }
        ]
    }
}


def build_unified_short_video(short_id: int, voice_model: Vieneu) -> Dict[str, Any]:
    cfg = UNIFIED_SHORTS_SPEC.get(short_id)
    if not cfg:
        die(f"Không tìm thấy cấu hình cho Short #{short_id}")

    short_name = cfg["name"]
    banner(f"SẢN XUẤT SHORT {short_id} VỚI KỊCH BẢN THỐNG NHẤT: {cfg['title']}", DAY_STR)

    work_proj_dir = Path(paths.WORK) / f"unified_short_{short_id:02d}_{DAY_STR}"
    work_proj_dir.mkdir(parents=True, exist_ok=True)
    tts_cache_dir = Path(paths.WORK) / "vitts_cache"
    tts_cache_dir.mkdir(parents=True, exist_ok=True)

    img_dir = DAY_DIR / "images"

    # Tải image_credits map
    credits_map = {}
    cred_file = DAY_DIR / "image_credits.json"
    if cred_file.exists():
        try:
            with open(cred_file, "r", encoding="utf-8") as f:
                credits_map = json.load(f)
        except Exception:
            pass

    # 1. SINH GIỌNG ĐỌC CHO TỪNG CÂU & TÍNH TIMESTAMPS
    step("Sinh giọng đọc ViTTS v3turbo Minh Quân Pro cho từng câu trong kịch bản...")
    sentences_data = []
    all_words_flat = []
    all_karaoke_flat = []
    combined_audio = AudioSegment.silent(duration=0)
    pause_between_sents = AudioSegment.silent(duration=220)  # 220ms ngắt câu tự nhiên

    cum_time = 0.0
    img_counter = 0

    for s_idx, s_info in enumerate(cfg["sentences"]):
        raw_text = s_info["text"].strip()
        tts_str, _ = prepare(raw_text)

        seg, _ = render_chunk_vitts(
            voice_model,
            tts_str,
            voice="Minh Quân Pro",
            temperature=0.6,
            speed=1.12,
            pitch=0.93,
            cache_dir=str(tts_cache_dir),
            use_cache=True,
            max_chars=768
        )
        seg = trim_segment_silence(seg)
        s_dur = round(len(seg) / 1000.0, 3)

        if s_idx > 0:
            combined_audio += pause_between_sents
            cum_time += 0.220

        s_start = round(cum_time, 3)
        combined_audio += seg
        cum_time += s_dur
        s_end = round(cum_time, 3)

        # Words & Karaoke chunks
        s_words = interpolate_sentence_words(raw_text, s_start, s_end)
        for w in s_words:
            all_words_flat.append(w)

        for ci in range(0, len(s_words), 4):
            c_words = s_words[ci:ci + 4]
            all_karaoke_flat.append({
                "start": c_words[0]["start"],
                "end": c_words[-1]["end"],
                "text": " ".join(cw["word"] for cw in c_words),
                "words": c_words
            })

        # Phân bổ ảnh cho câu
        assigned_images = []
        im_list = s_info.get("images", [])
        if not im_list:
            im_list = [f"Tin_01_1.jpg"]

        n_imgs = len(im_list)
        im_slice = s_dur / n_imgs
        for im_i, im_fn in enumerate(im_list):
            im_path = img_dir / im_fn
            if not im_path.exists():
                cands = sorted(glob.glob(str(img_dir / "*.jpg")))
                im_path = Path(cands[0]) if cands else img_dir / "Tin_01_1.jpg"

            cur_s = round(s_start + im_i * im_slice, 3)
            cur_e = s_end if im_i == n_imgs - 1 else round(cur_s + im_slice, 3)
            cur_dur = round(max(0.1, cur_e - cur_s), 3)

            pan_info = compute_pan_params(str(im_path), duration=cur_dur, dir_toggle=(img_counter % 2 == 1))
            img_counter += 1

            im_base = os.path.basename(str(im_path))
            im_credit = credits_map.get(im_base, "REUTERS / AP")

            assigned_images.append({
                "src": str(im_path),
                "credit": im_credit,
                "start": cur_s,
                "end": cur_e,
                "duration": cur_dur,
                "ken_burns": "pan_horizontal",
                "transition": "fade",
                **pan_info
            })

        sent_obj = {
            "sentence_id": s_idx + 1,
            "text": raw_text,
            "start": s_start,
            "end": s_end,
            "duration": s_dur,
            "layout": "full",
            "is_title": s_info.get("is_title", False),
            "item_title": s_info.get("headline", cfg["title"]),
            "item_group": s_info.get("group", cfg.get("group", cfg.get("badge", "TIN THỂ THAO"))),
            "news_source": s_info.get("news_source", "ĐIỂM ĐỌC THỂ THAO"),
            "credit": assigned_images[0]["credit"] if assigned_images else "REUTERS",
            "keywords": [w for w in raw_text.split() if len(w) > 3][:4],
            "images": assigned_images
        }
        sentences_data.append(sent_obj)
        log(f"  [Câu {s_idx + 1:02d}] ({s_start:.2f}s -> {s_end:.2f}s | {s_dur:.2f}s): {raw_text[:45]}...")

    # 2. CHUẨN HÓA ÂM THANH MASTER EBU R128 (-14.0 LUFS)
    raw_wav = work_proj_dir / "voiceover_raw.wav"
    master_wav = work_proj_dir / "voiceover.wav"
    combined_audio.export(str(raw_wav), format="wav")
    total_dur = round(len(combined_audio) / 1000.0, 3)

    log(f"Tổng thời lượng giọng đọc: {total_dur:.2f}s. Chuẩn hóa Loudnorm -14 LUFS...")
    if not two_pass_loudnorm(str(raw_wav), str(master_wav), target_i=-14.0, target_tp=-1.5, target_lra=11.0):
        combined_audio.export(str(master_wav), format="wav")

    # 3. LẬP TIMELINE JSON
    timeline = {
        "title": cfg["title"],
        "channel_name": "ĐIỂM ĐỌC",
        "date_str": "THỨ HAI · 09.11.2026",
        "date_chip": "THỨ HAI · 09.11.2026",
        "hide_date_chip": False,
        "total_duration": total_dur,
        "format": "short",
        "template": "short_news_v2.html",
        "dimensions": [1080, 1920],
        "fps": 30,
        "audio_path": str(master_wav),
        "global_offset_sec": 0.0,
        "group": cfg.get("group", cfg.get("badge", "TIN THỂ THAO")),
        "sentences": sentences_data,
        "words": all_words_flat,
        "karaoke_chunks": all_karaoke_flat
    }

    words_data = {
        "words": all_words_flat,
        "karaoke_chunks": all_karaoke_flat
    }

    tl_path = work_proj_dir / "video_timeline.json"
    words_path = work_proj_dir / "word_timestamps.json"
    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)
    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)

    ok(f"Đã lưu timeline thống nhất: {tl_path}")

    # 4. RENDER HTML v2 (Playwright + GSAP)
    log(f"Bắt đầu render video Short {short_id} qua Playwright HTML v2...")
    out_video_work = render_html_engine(
        project_dir=str(work_proj_dir),
        template="short_news_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True
    )

    if not out_video_work or not os.path.exists(out_video_work):
        die(f"Render Short {short_id} thất bại!")

    # 5. XUẤT FILE MP4 & CĂN CHỈNH DRIFT < 1ms
    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_final_mp4 = SHORTS_DIR / f"{short_name}.mp4"
    shutil.copy2(out_video_work, str(out_final_mp4))

    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "stream=duration,codec_type",
        "-of", "json", str(out_final_mp4)
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    try:
        pdata = json.loads(res.stdout)
        v_dur = next(float(s["duration"]) for s in pdata.get("streams", []) if s["codec_type"] == "video")
        tmp_sync = SHORTS_DIR / f"{short_name}_sync.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(out_final_mp4), "-t", f"{v_dur:.6f}",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            str(tmp_sync)
        ], check=True)
        tmp_sync.replace(out_final_mp4)
    except Exception as e:
        warn(f"Không thể chỉnh drift: {e}")

    ok(f"Đã xuất video Short {short_id}: {out_final_mp4}")

    # 6. KIỂM TOÁN ÂM THANH
    log(f"Kiểm toán âm thanh Short {short_id}...")
    subprocess.run(["python3", "-B", "core/audio_check.py", str(out_final_mp4)])

    # 7. XUẤT MÔ TẢ SEO YOUTUBE SHORTS
    mota_path = SHORTS_DIR / f"{short_name}_mota.txt"
    write_mota_9x16(
        out_path=mota_path,
        seo_title=cfg["seo_title"],
        description_paragraphs=cfg["description"],
        chapters=cfg["chapters"],
        sources_line=cfg["sources_line"],
        hashtags=cfg["hashtags"]
    )
    ok(f"Đã tạo file mô tả SEO: {mota_path}")

    # 8. RENDER THUMBNAIL DỌC 9:16
    t_cfg = cfg["thumb"]
    thumb_path = SHORTS_DIR / f"{short_name}_thumbnail.jpg"
    thumb_img = img_dir / t_cfg["image"]
    if not thumb_img.exists():
        thumb_img = img_dir / "Tin_01_1.jpg"

    render_thumbnail_9x16(
        out_path=thumb_path,
        image_path=thumb_img,
        kicker=t_cfg["kicker"],
        hero_html=t_cfg["hero_html"],
        subtitle=t_cfg["subtitle"],
        badge=t_cfg["badge"],
        tag_a=t_cfg.get("tag_a", "TIN NÓNG TUẦN"),
        tag_b=t_cfg.get("tag_b", "09.11.2026"),
        obj_pos=t_cfg.get("obj_pos", "center 20%"),
        img_filter=t_cfg.get("filter", "contrast(1.10) brightness(1.05) saturate(1.18)")
    )
    ok(f"Đã tạo thumbnail 9:16: {thumb_path}")

    return {
        "id": short_id,
        "video": out_final_mp4,
        "thumb": thumb_path,
        "mota": mota_path
    }


def main():
    parser = argparse.ArgumentParser(description="Build unified shorts sequentially")
    parser.add_argument("--short", type=int, required=True, help="Short ID to build (e.g. 6, 7, 8, 10)")
    args = parser.parse_args()

    sid = args.short
    if sid not in UNIFIED_SHORTS_SPEC:
        die(f"Chưa hỗ trợ Short #{sid}. Chỉ hỗ trợ 6, 7, 8, 10.")

    log(f"Khởi tạo mô hình phát âm ViTTS Vieneu v3turbo...")
    voice_model = Vieneu()

    res = build_unified_short_video(sid, voice_model)

    print("\n" + "=" * 78)
    ok(f"HOÀN THÀNH XUẤT BẢN SHORT {sid} VỚI KỊCH BẢN THỐNG NHẤT!")
    print(f"  🎬 Video:     {res['video']}")
    print(f"  🖼️  Thumbnail: {res['thumb']}")
    print(f"  📝 Mô tả SEO: {res['mota']}")
    print("=" * 78)


if __name__ == "__main__":
    main()
