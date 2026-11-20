#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True

import os, json, time, shutil, subprocess, random
from typing import List, Dict, Any
from pydub import AudioSegment

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
WORK_DIR = os.path.expanduser("~/Library/Caches/DiemDoc/22.10.2026/shorts_remake_v2")
os.makedirs(SHORTS_OUT_DIR, exist_ok=True)
os.makedirs(WORK_DIR, exist_ok=True)

TTS_CACHE = paths.work_file("vitts_cache")
KB_POOL = ["zoom_in", "zoom_out", "pan_left", "pan_right", "tilt_up", "tilt_down"]

SHORTS_DEFS = [
    {
        "id": "short_01",
        "out_name": "Short_01_Dai_Chien_Harry_Kane_vs_Lamine_Yamal.mp4",
        "title": "Harry Kane hay Lamine Yamal sẽ bước lên đỉnh thế giới tại London?",
        "group": "QUẢ BÓNG VÀNG 2026",
        "credit": "REUTERS / GETTY IMAGES",
        "sentences": [
            {
                "text": "Cuộc đua Quả bóng Vàng 2026 đang chứng kiến màn so tài nảy lửa nhất lịch sử giữa cỗ máy Ha-ri Kên và thần đồng La-min Gia-man.",
                "display": "Cuộc đua Quả bóng Vàng 2026 đang chứng kiến màn so tài nảy lửa nhất lịch sử giữa cỗ máy Harry Kane và thần đồng Lamine Yamal.",
                "images": ["Tin_03_1.jpg", "Tin_04_1.jpg"],
                "keywords": ["Quả bóng Vàng", "Harry Kane", "Lamine Yamal"]
            },
            {
                "text": "Tiền đạo đội trưởng đội tuyển Anh Ha-ri Kên đang nổi lên như ứng viên số một sáng giá nhất cho danh hiệu Quả bóng Vàng nam 2026, nhận được sự ủng hộ áp đảo từ các nhà cái quốc tế.",
                "display": "Tiền đạo đội trưởng đội tuyển Anh Harry Kane đang nổi lên như ứng viên số một sáng giá nhất cho danh hiệu Quả bóng Vàng nam 2026, nhận được sự ủng hộ áp đảo từ các nhà cái quốc tế.",
                "images": ["Tin_03_4.jpg", "Tin_03_5.jpg"],
                "keywords": ["Harry Kane", "ứng viên số một", "nhà cái quốc tế"]
            },
            {
                "text": "Ngôi sao 33 tuổi vừa trải qua một mùa giải hủy diệt bậc nhất trong toàn bộ sự nghiệp khi ghi tới 61 bàn thắng và đóng góp hàng loạt đường kiến tạo sau 51 lần ra sân trên mọi đấu trường cho Bayern Munich.",
                "display": "Ngôi sao 33 tuổi vừa trải qua một mùa giải hủy diệt bậc nhất trong toàn bộ sự nghiệp khi ghi tới 61 bàn thắng và đóng góp hàng loạt đường kiến tạo sau 51 lần ra sân trên mọi đấu trường cho Bayern Munich.",
                "images": ["Tin_03_6.jpg", "Tin_03_7.jpg"],
                "keywords": ["61 bàn thắng", "sự nghiệp", "Bayern Munich"]
            },
            {
                "text": "Sự thăng hoa rực rỡ của chân sút người Anh đã giúp gã khổng lồ xứ Bavaria thâu tóm trọn vẹn cú ăn ba quốc nội, đồng thời cá nhân Kên ẵm trọn danh hiệu Chiếc giày vàng châu Âu với số bàn thắng kỷ lục.",
                "display": "Sự thăng hoa rực rỡ của chân sút người Anh đã giúp gã khổng lồ xứ Bavaria thâu tóm trọn vẹn cú ăn ba quốc nội, đồng thời cá nhân Kane ẵm trọn danh hiệu Chiếc giày vàng châu Âu với số bàn thắng kỷ lục.",
                "images": ["Tin_03_8.jpg", "Tin_03_9.jpg"],
                "keywords": ["cú ăn ba", "Chiếc giày vàng", "kỷ lục"]
            },
            {
                "text": "Việc được xướng tên bước lên đỉnh cao thế giới ngay tại quê nhà London sẽ là cái kết ngọt ngào nhất, đập tan mọi định kiến hoài nghi để khắc tên Ha-ri Kên vào ngôi đền của những huyền thoại bóng đá bất tử.",
                "display": "Việc được xướng tên bước lên đỉnh cao thế giới ngay tại quê nhà London sẽ là cái kết ngọt ngào nhất, đập tan mọi định kiến hoài nghi để khắc tên Harry Kane vào ngôi đền của những huyền thoại bóng đá bất tử.",
                "images": ["Tin_03_15.jpg", "Tin_03_16.jpg"],
                "keywords": ["quê nhà London", "đập tan hoài nghi", "huyền thoại"]
            },
            {
                "text": "Tuy nhiên, đối trọng lớn nhất đe dọa trực tiếp vị trí của Ha-ri Kên chính là thần đồng La-min Gia-man của Bác-xa và đội tuyển Tây Ban Nha, người đang đứng trước ngưỡng cửa thiết lập một trong những kỳ tích vĩ đại nhất mọi thời đại.",
                "display": "Tuy nhiên, đối trọng lớn nhất đe dọa trực tiếp vị trí của Harry Kane chính là thần đồng Lamine Yamal của Barcelona và đội tuyển Tây Ban Nha, người đang đứng trước ngưỡng cửa thiết lập một trong những kỳ tích vĩ đại nhất mọi thời đại.",
                "images": ["Tin_04_4.jpg", "Tin_04_5.jpg"],
                "keywords": ["Lamine Yamal", "Barcelona", "Tây Ban Nha", "kỳ tích"]
            },
            {
                "text": "Nếu được vinh danh vào đêm 26 tháng 10 tới, Gia-man khi mới 19 tuổi sẽ chính thức xô đổ kỷ lục lịch sử tồn tại suốt 29 năm qua của huyền thoại người Bra-xin Rô-nan-đô Đê Li-ma năm 1997.",
                "display": "Nếu được vinh danh vào đêm 26 tháng 10 tới, Yamal khi mới 19 tuổi sẽ chính thức xô đổ kỷ lục lịch sử tồn tại suốt 29 năm qua của huyền thoại người Brazil Ronaldo de Lima năm 1997.",
                "images": ["Tin_04_6.jpg", "Tin_04_7.jpg"],
                "keywords": ["19 tuổi", "kỷ lục 29 năm", "Ronaldo de Lima"]
            },
            {
                "text": "La-min Gia-man đã trải qua một mùa giải kỳ diệu đến khó tin khi trở thành hạt nhân trung tâm không thể thay thế, dẫn dắt đội tuyển Tây Ban Nha đăng quang chức vô địch World Cup 2026 bằng thứ bóng đá mê hoặc và những pha xử lý thiên tài làm nổ tung cầu trường.",
                "display": "Lamine Yamal đã trải qua một mùa giải kỳ diệu đến khó tin khi trở thành hạt nhân trung tâm không thể thay thế, dẫn dắt đội tuyển Tây Ban Nha đăng quang chức vô địch World Cup 2026 bằng thứ bóng đá mê hoặc và những pha xử lý thiên tài làm nổ tung cầu trường.",
                "images": ["Tin_04_9.jpg", "Tin_04_10.jpg"],
                "keywords": ["hạt nhân trung tâm", "vô địch World Cup 2026", "thiên tài"]
            },
            {
                "text": "Một chiến thắng lịch sử tại London không chỉ biến La-min Gia-man thành cầu thủ tuổi teen đầu tiên nhận Quả bóng Vàng mà còn chính thức mở ra một kỷ nguyên mới thống trị đỉnh cao bóng đá thế giới.",
                "display": "Một chiến thắng lịch sử tại London không chỉ biến Lamine Yamal thành cầu thủ tuổi teen đầu tiên nhận Quả bóng Vàng mà còn chính thức mở ra một kỷ nguyên mới thống trị đỉnh cao bóng đá thế giới.",
                "images": ["Tin_04_15.jpg", "Tin_04_16.jpg"],
                "keywords": ["tuổi teen", "Quả bóng Vàng", "kỷ nguyên mới"]
            },
            {
                "text": "Một bên là cỗ máy ghi bàn vĩ đại, một bên là thần đồng làm nên lịch sử. Ai sẽ bước lên đỉnh thế giới tại thánh đường Pa la đi um? Hãy để lại bình luận dự đoán của bạn nhé!",
                "display": "Một bên là cỗ máy ghi bàn vĩ đại, một bên là thần đồng làm nên lịch sử. Ai sẽ bước lên đỉnh thế giới tại thánh đường London Palladium? Hãy để lại bình luận dự đoán của bạn nhé!",
                "images": ["Tin_03_2.jpg", "Tin_04_2.jpg"],
                "keywords": ["đỉnh thế giới", "London Palladium", "bình luận"]
            }
        ]
    },
    {
        "id": "short_02",
        "out_name": "Short_02_Cuoc_Dua_Yashin_Trophy_Gang_Tay_Vang.mp4",
        "title": "Đại chiến găng tay vàng Yashin Trophy giữa các thủ môn Tây Ban Nha",
        "group": "HẠNG MỤC PHỤ",
        "credit": "REUTERS / GETTY IMAGES",
        "sentences": [
            {
                "text": "Bên cạnh danh hiệu Quả bóng Vàng nam, các hạng mục giải thưởng cá nhân danh giá khác do France Football trao tặng cũng đang chứng kiến những màn so kè vô cùng khốc liệt giữa các ngôi sao hàng đầu.",
                "display": "Bên cạnh danh hiệu Quả bóng Vàng nam, các hạng mục giải thưởng cá nhân danh giá khác do France Football trao tặng cũng đang chứng kiến những màn so kè vô cùng khốc liệt giữa các ngôi sao hàng đầu.",
                "images": ["Tin_06_4.jpg"],
                "keywords": ["giải thưởng cá nhân", "France Football", "khốc liệt"]
            },
            {
                "text": "Ở giải thưởng Cúp Cô-pa dành cho cầu thủ dưới 21 tuổi xuất sắc nhất hành tinh, La-min Gia-man gần như nắm chắc chiến thắng trong tay để đi vào lịch sử với tư cách cầu thủ đầu tiên hai lần liên tiếp nhận giải thưởng này.",
                "display": "Ở giải thưởng Kopa Trophy dành cho cầu thủ dưới 21 tuổi xuất sắc nhất hành tinh, Lamine Yamal gần như nắm chắc chiến thắng trong tay để đi vào lịch sử với tư cách cầu thủ đầu tiên hai lần liên tiếp nhận giải thưởng này.",
                "images": ["Tin_06_5.jpg", "Tin_06_6.jpg"],
                "keywords": ["Kopa Trophy", "dưới 21 tuổi", "hai lần liên tiếp"]
            },
            {
                "text": "Người duy nhất có thể tạo ra đôi chút áp lực cho Gia-man chính là người đồng đội thân thiết tại Bác-xa và đội tuyển Tây Ban Nha, trung vệ tài năng Pau Cu-bác-xi, người đã xây dựng bức tường phòng ngự kiên cố suốt mùa giải qua.",
                "display": "Người duy nhất có thể tạo ra đôi chút áp lực cho Yamal chính là người đồng đội thân thiết tại Barcelona và đội tuyển Tây Ban Nha, trung vệ tài năng Pau Cubarsi, người đã xây dựng bức tường phòng ngự kiên cố suốt mùa giải qua.",
                "images": ["Tin_06_7.jpg", "Tin_06_8.jpg"],
                "keywords": ["Pau Cubarsi", "Barcelona", "phòng ngự kiên cố"]
            },
            {
                "text": "Trong khi đó, cuộc đua giành găng tay vàng Cúp Y-a-sin lại là sàn đấu nội bộ đầy tự hào của bóng đá xứ sở bò tót.",
                "display": "Trong khi đó, cuộc đua giành găng tay vàng Yashin Trophy lại là sàn đấu nội bộ đầy tự hào của bóng đá xứ sở bò tót.",
                "images": ["Tin_06_9.jpg"],
                "keywords": ["găng tay vàng", "Yashin Trophy", "Tây Ban Nha"]
            },
            {
                "text": "Với việc đương kim chủ nhân Gianluigi Donnarumma không có tên trong danh sách đề cử, thủ thành Giô-an Gác-xi-a của Bác-xa đang dẫn đầu cuộc đua sau khi giành giải thưởng Da-mô-ra cho thủ môn để lọt lưới ít nhất tại La Li-ga.",
                "display": "Với việc đương kim chủ nhân Gianluigi Donnarumma không có tên trong danh sách đề cử, thủ thành Joan Garcia của Barcelona đang dẫn đầu cuộc đua sau khi giành giải thưởng Zamora cho thủ môn để lọt lưới ít nhất tại La Liga.",
                "images": ["Tin_06_10.jpg", "Tin_06_11.jpg"],
                "keywords": ["Joan Garcia", "giải thưởng Zamora", "La Liga"]
            },
            {
                "text": "Anh phải cạnh tranh gắt gao với U-nai Xi-môn, người hùng bắt chính giữ sạch lưới giúp Tây Ban Nha vô địch thế giới, cùng Đa-vít Ray-a, người gác đền sở hữu phản xạ xuất thần trong khung gỗ A-xê-nôn tại Ngoại Hạng Anh.",
                "display": "Anh phải cạnh tranh gắt gao với Unai Simon, người hùng bắt chính giữ sạch lưới giúp Tây Ban Nha vô địch thế giới, cùng David Raya, người gác đền sở hữu phản xạ xuất thần trong khung gỗ Arsenal tại Ngoại Hạng Anh.",
                "images": ["Tin_06_12.jpg", "Tin_06_13.jpg"],
                "keywords": ["Unai Simon", "vô địch thế giới", "David Raya", "Arsenal"]
            },
            {
                "text": "Bảng đề cử năm nay còn ghi nhận hiện tượng kỳ thú mang tên Vô-din-nha, thủ môn kỳ cựu 40 tuổi đã viết nên câu chuyện cổ tích đưa quốc đảo Cáp Ve-đê tiến thẳng vào vòng loại trực tiếp của World Cup 2026.",
                "display": "Bảng đề cử năm nay còn ghi nhận hiện tượng kỳ thú mang tên Vozinha, thủ môn kỳ cựu 40 tuổi đã viết nên câu chuyện cổ tích đưa quốc đảo Cape Verde tiến thẳng vào vòng loại trực tiếp của World Cup 2026.",
                "images": ["Tin_06_14.jpg", "Tin_06_15.jpg"],
                "keywords": ["Vozinha", "40 tuổi", "Cape Verde", "World Cup 2026"]
            },
            {
                "text": "Bất ngờ chấn động nhất xuất hiện ở hạng mục nữ, khi nhà đương kim vô địch ba năm liên tiếp Ai-ta-na Bôn-ma-ti hoàn toàn vắng mặt trong danh sách đề cử vì chấn thương gãy xương mác nghiêm trọng.",
                "display": "Bất ngờ chấn động nhất xuất hiện ở hạng mục nữ, khi nhà đương kim vô địch ba năm liên tiếp Aitana Bonmati hoàn toàn vắng mặt trong danh sách đề cử vì chấn thương gãy xương mác nghiêm trọng.",
                "images": ["Tin_07_4.jpg", "Tin_07_6.jpg"],
                "keywords": ["Aitana Bonmati", "vắng mặt", "chấn thương"]
            },
            {
                "text": "Sự vắng bóng của tiền vệ số một thế giới đã mở toang cánh cửa cho người đồng đội A-lếch-xi-a Pu-tê-giát đứng trước cơ hội lịch sử giành Quả bóng Vàng nữ thứ ba trong sự nghiệp.",
                "display": "Sự vắng bóng của tiền vệ số một thế giới đã mở toang cánh cửa cho người đồng đội Alexia Putellas đứng trước cơ hội lịch sử giành Quả bóng Vàng nữ thứ ba trong sự nghiệp.",
                "images": ["Tin_07_10.jpg", "Tin_07_11.jpg"],
                "keywords": ["Alexia Putellas", "Quả bóng Vàng nữ", "lịch sử"]
            },
            {
                "text": "Buổi lễ cũng sẽ dành những tràng pháo tay trang trọng nhất cho giải thưởng Xô-cơ-ra-tét nhằm tôn vinh những cầu thủ có đóng góp nhân đạo và thiện nguyện nổi bật cho cộng đồng toàn cầu.",
                "display": "Buổi lễ cũng sẽ dành những tràng pháo tay trang trọng nhất cho giải thưởng Socrates Award nhằm tôn vinh những cầu thủ có đóng góp nhân đạo và thiện nguyện nổi bật cho cộng đồng toàn cầu.",
                "images": ["Tin_07_15.jpg"],
                "keywords": ["Socrates Award", "nhân đạo", "toàn cầu"]
            },
            {
                "text": "Liệu người gác đền nào sẽ được vinh danh tại thánh đường Pa la đi um? Hãy để lại bình luận dự đoán của bạn nhé!",
                "display": "Liệu người gác đền nào sẽ được vinh danh tại London Palladium? Hãy để lại bình luận dự đoán của bạn nhé!",
                "images": ["Tin_06_1.jpg", "Tin_06_2.jpg"],
                "keywords": ["người gác đền", "London Palladium", "bình luận"]
            }
        ]
    },
    {
        "id": "short_03",
        "out_name": "Short_03_Cu_Soc_Qua_Bong_Vang_Roi_Paris.mp4",
        "title": "Cú sốc 70 năm: Gala Quả bóng Vàng rời Paris sang London Palladium",
        "group": "CÚ SỐC BẤT NGỜ",
        "credit": "REUTERS / GETTY IMAGES",
        "sentences": [
            {
                "text": "Lễ trao giải Quả bóng Vàng lần thứ 70 chuẩn bị chính thức khởi tranh vào tối thứ Hai ngày 26 tháng 10 năm 2026 tại nhà hát Pa la đi um danh tiếng ở thủ đô London của nước Anh.",
                "display": "Lễ trao giải Quả bóng Vàng lần thứ 70 chuẩn bị chính thức khởi tranh vào tối thứ Hai ngày 26 tháng 10 năm 2026 tại nhà hát London Palladium danh tiếng ở thủ đô London của nước Anh.",
                "images": ["Tin_01_4.jpg"],
                "keywords": ["Quả bóng Vàng lần thứ 70", "London Palladium", "26 tháng 10"]
            },
            {
                "text": "Đây là cột mốc mang tính bước ngoặt vĩ đại nhất kể từ ngày danh hiệu cá nhân cao quý này ra đời, khi France Football và UEFA lần đầu tiên trong lịch sử 7 thập kỷ quyết định mang buổi gala danh giá rời khỏi kinh đô ánh sáng Paris.",
                "display": "Đây là cột mốc mang tính bước ngoặt vĩ đại nhất kể từ ngày danh hiệu cá nhân cao quý này ra đời, khi ban tổ chức France Football cùng UEFA lần đầu tiên trong lịch sử 7 thập kỷ quyết định mang buổi gala danh giá rời khỏi kinh đô ánh sáng Paris.",
                "images": ["Tin_01_5.jpg", "Tin_01_6.jpg"],
                "keywords": ["bước ngoặt vĩ đại", "France Football", "UEFA", "rời khỏi Paris"]
            },
            {
                "text": "Quyết định lịch sử này mang ý nghĩa vô cùng sâu sắc, là sự tri ân đặc biệt đối với cố huyền thoại bóng đá người Anh Xtan-li Mát-thiu, người đầu tiên vinh dự nâng cao danh hiệu Quả bóng Vàng vào năm 1956, vừa tròn đúng 70 năm về trước.",
                "display": "Quyết định lịch sử này mang ý nghĩa vô cùng sâu sắc, là sự tri ân đặc biệt đối với cố huyền thoại bóng đá người Anh Sir Stanley Matthews, người đầu tiên vinh dự nâng cao danh hiệu Quả bóng Vàng vào năm 1956, vừa tròn đúng 70 năm về trước.",
                "images": ["Tin_01_7.jpg", "Tin_01_8.jpg"],
                "keywords": ["Sir Stanley Matthews", "Quả bóng Vàng 1956", "70 năm"]
            },
            {
                "text": "Đêm gala vinh danh năm nay sẽ được điều phối bởi cặp đôi người dẫn chương trình lừng danh gồm huyền thoại bóng đá Pháp Thi-ê-ri Hen-ri cùng nữ nhà báo truyền hình sắc sảo Két Xcót.",
                "display": "Đêm gala vinh danh năm nay sẽ được điều phối bởi cặp đôi người dẫn chương trình lừng danh gồm huyền thoại bóng đá Pháp Thierry Henry cùng nữ nhà báo truyền hình sắc sảo Kate Scott.",
                "images": ["Tin_01_9.jpg", "Tin_01_10.jpg"],
                "keywords": ["Thierry Henry", "Kate Scott", "người dẫn chương trình"]
            },
            {
                "text": "Không gian tráng lệ của khán phòng Pa la đi um với sức chứa hơn hai nghìn hai trăm chỗ ngồi hứa hẹn sẽ chứng kiến những khoảnh khắc bùng nổ cảm xúc khi toàn bộ các danh thủ bóng đá thế giới tề tựu đông đủ.",
                "display": "Không gian tráng lệ của khán phòng London Palladium với sức chứa hơn hai nghìn hai trăm chỗ ngồi hứa hẹn sẽ chứng kiến những khoảnh khắc bùng nổ cảm xúc khi toàn bộ các danh thủ bóng đá thế giới tề tựu đông đủ.",
                "images": ["Tin_01_11.jpg", "Tin_01_12.jpg"],
                "keywords": ["London Palladium", "hai nghìn hai trăm chỗ ngồi", "danh thủ thế giới"]
            },
            {
                "text": "Về mặt thể thức và quy chuẩn đánh giá chuyên môn, Quả bóng Vàng 2026 tiếp tục duy trì khung thời gian xét duyệt dựa trên trọn vẹn mùa giải bóng đá, và điểm mấu chốt tạo nên khác biệt khổng lồ chính là việc bao trọn vòng chung kết World Cup 2026 tại Bắc Mỹ.",
                "display": "Về mặt thể thức và quy chuẩn đánh giá chuyên môn, Quả bóng Vàng 2026 tiếp tục duy trì khung thời gian xét duyệt dựa trên trọn vẹn mùa giải bóng đá, và điểm mấu chốt tạo nên khác biệt khổng lồ chính là việc bao trọn vòng chung kết World Cup 2026 tại Bắc Mỹ.",
                "images": ["Tin_02_4.jpg", "Tin_02_6.jpg"],
                "keywords": ["quy chuẩn", "trọn vẹn mùa giải", "World Cup 2026"]
            },
            {
                "text": "Đây là ngày hội bóng đá quy mô nhất lịch sử nhân loại với 48 đội tuyển tranh tài, nơi đội tuyển Tây Ban Nha đã xuất sắc bước lên đỉnh vinh quang thế giới sau những màn trình diễn áp đảo hoàn toàn các đối thủ.",
                "display": "Đây là ngày hội bóng đá quy mô nhất lịch sử nhân loại với 48 đội tuyển tranh tài, nơi đội tuyển Tây Ban Nha đã xuất sắc bước lên đỉnh vinh quang thế giới sau những màn trình diễn áp đảo hoàn toàn các đối thủ.",
                "images": ["Tin_02_8.jpg", "Tin_02_9.jpg"],
                "keywords": ["48 đội tuyển", "Tây Ban Nha", "đỉnh vinh quang thế giới"]
            },
            {
                "text": "Kết quả chung cuộc được quyết định bởi hội đồng 100 nhà báo thể thao quốc tế dựa trên màn trình diễn cá nhân xuất sắc, thành tích tập thể danh giá cùng sự mẫu mực về đẳng cấp và tinh thần fair-play.",
                "display": "Kết quả chung cuộc được quyết định bởi hội đồng 100 nhà báo thể thao quốc tế dựa trên màn trình diễn cá nhân xuất sắc, thành tích tập thể danh giá cùng sự mẫu mực về đẳng cấp và tinh thần fair-play.",
                "images": ["Tin_02_10.jpg", "Tin_02_12.jpg"],
                "keywords": ["100 nhà báo", "màn trình diễn cá nhân", "fair-play"]
            },
            {
                "text": "Sức nặng của chiếc cúp vàng thế giới tại Bắc Mỹ chắc chắn sẽ là cán cân quyết định, làm thay đổi hoàn toàn cục diện cuộc đua trước thềm gala London.",
                "display": "Sức nặng của chiếc cúp vàng thế giới tại Bắc Mỹ chắc chắn sẽ là cán cân quyết định, làm thay đổi hoàn toàn cục diện cuộc đua trước thềm gala London.",
                "images": ["Tin_02_14.jpg"],
                "keywords": ["cúp vàng thế giới", "cán cân quyết định", "gala London"]
            },
            {
                "text": "Bạn có ủng hộ quyết định đưa Quả bóng Vàng ra khỏi Paris hay không? Hãy chia sẻ ý kiến của bạn nhé!",
                "display": "Bạn có ủng hộ quyết định đưa Quả bóng Vàng ra khỏi Paris hay không? Hãy chia sẻ ý kiến của bạn nhé!",
                "images": ["Tin_01_1.jpg", "Tin_01_2.jpg"],
                "keywords": ["Quả bóng Vàng", "rời khỏi Paris", "ý kiến"]
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
            pause_ms = int(c.get("pause_sec", 0.25) * 1000)
            if pause_ms > 0:
                combined += AudioSegment.silent(duration=pause_ms, frame_rate=44100)
            continue
        c_text = c.get("text", "").strip()
        if not c_text:
            continue
        seg, _ = render_chunk_vitts(model, c_text, voice, temperature=0.5, speed=speed, pitch=pitch, cache_dir=TTS_CACHE, use_cache=False, max_chars=768)
        seg = trim_segment_silence(seg)
        combined += seg
    return combined

def main():
    print("=== SẢN XUẤT 3 SHORTS CHUẨN THỜI LƯỢNG 1:30 - 2:30 (FULL CHIỀU NGANG, CAO 1280PX, GIỌNG PITCH 1.0) ===")
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

        # Title intro audio (~5s)
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
            "keywords": ["Quả bóng Vàng 2026"],
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

            # Randomize Ken Burns from pool
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

        dest_mp4 = os.path.join(SHORTS_OUT_DIR, out_name)
        shutil.copy2(rendered_mp4, dest_mp4)
        print(f"  🎉 XUẤT THÀNH CÔNG: {dest_mp4} ({os.path.getsize(dest_mp4)} bytes, {mins:02d}:{secs:02d})")

if __name__ == "__main__":
    main()
