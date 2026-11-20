#!/usr/bin/env python3
"""
m1b_llm_writer.py — Biên Tập Kịch Bản LLM Thể Thao: Chiều Sâu 16:9 & Tách Kịch Bản 9:16
========================================================================================
Tuân thủ nghiêm ngặt các quy tắc biên tập cứng:

1. KỊCH BẢN DÀI 16:9 (outputs/DD.MM.YYYY/thethao.txt):
   - Số lượng: Linh hoạt tùy theo lượng tin tức nổi bật thực tế trong ngày (không cố định cứng số lượng tin).
   - Chiều sâu Lời bình: MỖI TIN dài 4-6 câu (khoảng 80-120 từ), mang tính bình luận chuyên sâu,
     bổ sung bối cảnh, nguyên nhân, diễn biến chính, hệ quả chiến thuật hoặc phát biểu nhân vật.
   - Kỷ luật: Không lặp lại Tiêu đề, quy đổi thời gian tuyệt đối ("ngày 15 tháng 10").

2. KỊCH BẢN SHORT 9:16 (outputs/DD.MM.YYYY/shorts.txt & shorts.json):
   - Chọn ra 6 tin "nóng" nhất (HOTTEST).
   - Lời bình đọc siêu nhanh: CHỈ 1-2 câu ngắn gọn, súc tích (khoảng 25-45 từ/tin).
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import os
import re
import json
import argparse
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc import paths
from diemdoc.log import banner, ok, warn, err, step, log

ICT = timezone(timedelta(hours=7))


def load_raw_news(input_file: Optional[str] = None) -> Dict[str, Any]:
    """Đọc tệp tin tức thô từ WORK/temp_raw_news.json."""
    if input_file is None:
        input_file = paths.work_file("temp_raw_news.json")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Không tìm thấy file tin tức: {input_file}. Hãy chạy m1_scraper.py trước!")
    with open(input_file, "r", encoding="utf-8") as f:
        return json.load(f)


def build_editorial_stories(raw_news: Dict[str, Any], current_date: str = "16.10.2026") -> List[Dict[str, str]]:
    """
    Biên tập các tin thể thao đắt giá nhất trong ngày (linh hoạt theo mật độ tin thực tế) với chiều sâu phân tích cho video 16:9.
    Mỗi tin dài 4-6 câu (80-120 từ), không lặp lại tiêu đề, thời gian tuyệt đối.
    """
    stories: List[Dict[str, str]] = [
        # ======================================================================
        # NHÓM 1: ĐT VIỆT NAM & TUYỂN TRẺ (7 TIN)
        # ======================================================================
        {
            "id": "art_01",
            "group": "ĐT Việt Nam & Tuyển Trẻ",
            "title": "Tuyển Việt Nam quyết thắng Kyrgyzstan và Đài Loan để bứt phá bảng xếp hạng FIFA",
            "detail": "Thầy trò huấn luyện viên Kim Sang-sik chuẩn bị bước vào đợt tập trung then chốt với hai trận giao hữu tại sân Thiên Trường từ ngày 11 đến 15 tháng 11. Sau khi bị trừ hơn 5 điểm và tụt xuống vị trí 99 thế giới, đội tuyển Việt Nam buộc phải đánh bại cả Kyrgyzstan lẫn Đài Loan để tích lũy trọn vẹn 6,3 điểm thưởng trên bảng xếp hạng FIFA. Đây là mục tiêu sống còn giúp bóng đá Việt Nam trở lại nhóm 95 thế giới và giữ vững lợi thế hạt giống số hai ở vòng loại Asian Cup 2027. Thất bại trước Thái Lan và Malaysia trước đó đã phơi bày điểm yếu tranh chấp ở tuyến giữa, buộc ban huấn luyện phải cải tổ mạnh mẽ nhân sự. Hai trận đấu này sẽ là thước đo chính xác nhất cho quá trình trẻ hóa lực lượng của ban huấn luyện."
        },
        {
            "id": "art_02",
            "group": "ĐT Việt Nam & Tuyển Trẻ",
            "title": "Tuyển Việt Nam đối mặt nguy cơ tái chiến Malaysia và Indonesia tại vòng loại World Cup 2030",
            "detail": "Dựa trên phân nhánh hạt giống hiện tại của Liên đoàn bóng đá châu Á, đội tuyển Việt Nam thuộc nhóm hai trong khi cả Indonesia và Malaysia đều nằm ở nhóm ba. Điều này đồng nghĩa với việc ba đại diện nhiều duyên nợ nhất Đông Nam Á hoàn toàn có thể rơi vào cùng một bảng đấu ở vòng loại thứ hai khởi tranh vào tháng 9 năm 2027. Cả hai đối thủ khu vực đều đang ráo riết nâng cấp đội hình bằng nguồn cầu thủ kiều bào châu Âu chất lượng, tiêu biểu là trung vệ Jay Idzes đang chơi bóng tại giải Serie A của Ý. Sự tiến bộ vượt bậc của đối thủ đặt ra bài toán khó cho bóng đá Việt Nam trong việc duy trì ưu thế cạnh tranh đường dài. Thầy trò ông Kim Sang-sik sẽ phải nâng cao cường độ chơi bóng và chiều sâu đội hình nếu muốn tái lập kỳ tích tiến sâu ở đấu trường thế giới."
        },
        {
            "id": "art_07",
            "group": "ĐT Việt Nam & Tuyển Trẻ",
            "title": "U17 Việt Nam đặt mục tiêu tạo bất ngờ lịch sử tại Vòng chung kết U17 World Cup 2026",
            "detail": "Huấn luyện viên Cristiano Roland khẳng định toàn đội đã hoàn tất giai đoạn rèn giũa thể lực và hoàn thiện khối đội hình phòng ngự phản công để sẵn sàng tranh tài tại ngày hội bóng đá lớn nhất hành tinh. Dù lần đầu tiên góp mặt ở giải đấu quy mô toàn cầu và rơi vào bảng đấu có nhiều đối thủ vượt trội về thể hình, các cầu thủ trẻ Việt Nam vẫn thể hiện quyết tâm thi đấu sòng phẳng. Ban huấn luyện đặc biệt chú trọng rèn luyện tính kỷ luật chiến thuật và tốc độ chuyển đổi trạng thái khi đoạt lại bóng. Chuyến tập huấn chất lượng cao tại châu Âu vừa qua đã mang lại sự tự tin lớn cho các gương mặt triển vọng. Toàn đội hướng tới mục tiêu giành điểm số lịch sử để tạo bước ngoặt lớn cho công tác đào tạo bóng đá trẻ nước nhà."
        },
        {
            "id": "art_09",
            "group": "ĐT Việt Nam & Tuyển Trẻ",
            "title": "Đội tuyển Việt Nam giải bài toán trụ hạng top 100 thế giới trước thềm bốc thăm Asian Cup",
            "detail": "Nguy cơ rơi khỏi nhóm 100 đội tuyển mạnh nhất thế giới đang hiện hữu rõ nét sau chuỗi phong độ thiếu ổn định tại các giải đấu khu vực. Để bảo toàn vị thế trước lễ bốc thăm vòng chung kết Asian Cup 2027, đội tuyển Việt Nam không được phép sảy chân ở bất kỳ trận giao hữu quốc tế nào trong dịp FIFA Days tháng 11. Huấn luyện viên Kim Sang-sik đối mặt áp lực nặng nề trong việc cân bằng giữa thử nghiệm nhân sự mới và duy trì kết quả tích cực trên sân cỏ. Việc thiếu vắng những chân sút đạt hiệu suất cao đòi hỏi ban huấn luyện phải tìm kiếm các giải pháp tấn công đa dạng từ tuyến hai. Một chiến thắng thuyết phục tại Nam Định sẽ giúp giải tỏa tâm lý đè nặng lên các cầu thủ suốt thời gian qua."
        },
        {
            "id": "art_13",
            "group": "ĐT Việt Nam & Tuyển Trẻ",
            "title": "Chủ tịch VFF Trần Quốc Tuấn giao nhiệm vụ tạo đột phá cho U17 Việt Nam tại World Cup",
            "detail": "Chiều ngày 15 tháng 10, người đứng đầu Liên đoàn bóng đá Việt Nam đã trực tiếp đến thăm và động viên thầy trò huấn luyện viên Cristiano Roland tại Trung tâm đào tạo bóng đá trẻ Hà Nội. Lãnh đạo VFF nhấn mạnh việc giành vé tham dự ngày hội bóng đá thế giới là vinh dự to lớn, đồng thời yêu cầu toàn đội chuẩn bị kỹ lưỡng nhất về tâm lý và chuyên môn. Huấn luyện viên Roland khẳng định các học trò không đến giải đấu với tư tưởng cọ xát đơn thuần mà quyết tâm tạo nên bất ngờ trước các đại diện hùng mạnh. VFF cam kết tạo mọi điều kiện tốt nhất về dinh dưỡng, y tế và chế độ tập luyện để các tuyển thủ trẻ đạt phong độ đỉnh cao. Sự quan tâm sâu sát từ cơ quan quản lý là nguồn động lực tinh thần to lớn trước giờ lên đường."
        },
        {
            "id": "art_31",
            "group": "ĐT Việt Nam & Tuyển Trẻ",
            "title": "Tuyển Việt Nam chốt lịch so tài với tuyển Nhật Bản tại Osaka ngày 30 tháng 12",
            "detail": "Trận đấu giao hữu với đội bóng số một châu Á sẽ là bài kiểm tra đỉnh cao của thầy trò huấn luyện viên Kim Sang-sik ngay trước khi bước vào chiến dịch vòng chung kết châu lục. Đội tuyển Nhật Bản dự kiến tung ra dàn hảo thủ đang chơi bóng tại các giải vô địch quốc gia hàng đầu châu Âu để rà soát lực lượng. Đây là cơ hội hiếm có để các hậu vệ Việt Nam thử lửa trước những tiền đạo đẳng cấp thế giới và hoàn thiện khả năng chịu đựng áp lực tầm cao. Ban huấn luyện xác định trận đấu này là cữ dượt chiến thuật then chốt nhằm tìm ra phương án phòng ngự khu vực tối ưu nhất. Kết quả đọ sức với đại diện xứ sở hoa anh đào sẽ cung cấp nhiều bài học quý giá cho toàn đội."
        },
        {
            "id": "art_36",
            "group": "ĐT Việt Nam & Tuyển Trẻ",
            "title": "Đoàn Văn Hậu bình phục chấn thương và tỏa sáng tại Cúp C1 châu Á",
            "detail": "Hậu vệ cánh trái sinh năm 1999 đã có màn tái xuất vô cùng ấn tượng trong cuộc đọ sức với câu lạc bộ Kashima Antlers của Nhật Bản vào tối ngày 13 tháng 10. Sự trở lại của cầu thủ quê Thái Bình mang đến niềm vui lớn cho người hâm mộ sau quãng thời gian dài phải nghỉ thi đấu để điều trị chấn thương dai dẳng. Những pha leo biên tốc độ cùng khả năng tranh chấp tay đôi quyết liệt của Văn Hậu giúp hành lang cánh trái của Công an Hà Nội lấy lại sự vững chắc vốn có. Màn trình diễn đẳng cấp châu lục này mở toang cánh cửa để anh được huấn luyện viên Kim Sang-sik triệu tập trở lại đội tuyển quốc gia vào tháng 11 tới. Sự hiện diện của một hậu vệ dày dạn kinh nghiệm quốc tế sẽ gia tăng đáng kể sức mạnh phòng ngự cho tuyển Việt Nam."
        },

        # ======================================================================
        # NHÓM 2: V-LEAGUE & CLB VIỆT NAM (6 TIN)
        # ======================================================================
        {
            "id": "art_03",
            "group": "V-League & CLB Việt Nam",
            "title": "CLB Bắc Ninh đối đầu CLB Thành phố Đồng Nai tại vòng đấu quyết định giải hạng Nhất",
            "detail": "Trận cầu tâm điểm lúc 18 giờ ngày 18 tháng 10 trên sân Việt Yên đang nhận được sự quan tâm đặc biệt khi Công Phượng cùng các đồng đội có chuyến làm khách đầy thử thách. Đội chủ nhà Bắc Ninh đang sở hữu phong độ ấn tượng trên sân nhà với lối chơi pressing rực lửa và dàn cầu thủ giàu khát khao khẳng định mình. Ngược lại, đại diện miền Nam chịu sức ép buộc phải giành 3 điểm để xua tan bầu không khí ảm đạm sau chuỗi kết quả đáng thất vọng từ đầu mùa. Sự tỏa sáng của các ngôi sao trên hàng công như Công Phượng sẽ là chìa khóa then chốt mở toang cánh cửa vào khung thành đối phương. Cuộc đọ sức hứa hẹn sẽ diễn ra vô cùng nảy lửa với nhiều toan tính chiến thuật từ hai băng ghế chỉ đạo."
        },
        {
            "id": "art_05",
            "group": "V-League & CLB Việt Nam",
            "title": "CLB Thành phố Đồng Nai đứng cuối bảng sau 3 vòng đấu với 0 điểm",
            "detail": "Dù nhận được khoản đầu tư kỷ lục và sở hữu bản hợp đồng ngoại binh đắt giá nhất V-League, đội bóng này lại gây thất vọng tràn trề khi toàn thua sau ba lượt trận mở màn. Điểm yếu chết người nằm ở sự rời rạc giữa các tuyến và khả năng dứt điểm yếu kém khi các tiền đạo vẫn chưa thể ghi nổi một bàn thắng danh dự. Áp lực đè nặng lên vai ban huấn luyện ngày một lớn sau những màn trình diễn thiếu sức sống trước các đối thủ cạnh tranh trực tiếp. Sự hòa nhập chậm chạp của các tân binh đắt giá khiến lối chơi tập thể hoàn toàn bế tắc khi bị đối phương phong tỏa chặt chẽ. Nếu không sớm cải thiện phong độ ở vòng đấu tới, nguy cơ lún sâu vào cuộc chiến trụ hạng sẽ trở thành hiện thực cay đắng."
        },
        {
            "id": "art_12",
            "group": "V-League & CLB Việt Nam",
            "title": "Hoàng Đức cùng Ninh Bình FC chạm trán đội bóng cũ Hoàng Anh Gia Lai tại Pleiku",
            "detail": "Chuyến hành quân lên phố núi lúc 18 giờ ngày 18 tháng 10 của câu lạc bộ Ninh Bình mang đậm tính duyên nợ khi tiền vệ Nguyễn Hoàng Đức gặp lại nhiều đồng đội quen thuộc. Đội khách đang bay cao trên bảng xếp hạng nhờ sự ăn ý vượt bậc giữa các cựu binh dày dạn kinh nghiệm và dàn cầu thủ trẻ giàu nhiệt huyết như Lê Phát. Trong khi đó, Hoàng Anh Gia Lai luôn là đối thủ cực kỳ khó chịu khi được thi đấu dưới sự cổ vũ cuồng nhiệt của khán giả nhà trên sân Pleiku. Khả năng điều tiết nhịp độ trận đấu và những đường chọc khe sắc lẹm của Hoàng Đức sẽ là thứ vũ khí lợi hại nhất để xuyên phá hàng thủ đối phương. Trận đấu hứa hẹn cống hiến cho người hâm mộ những pha đôi công mãn nhãn với tốc độ cao."
        },
        {
            "id": "art_28",
            "group": "V-League & CLB Việt Nam",
            "title": "Thể Công Viettel thất thủ 0-1 trước Persib Bandung tại vòng bảng Cúp C2 châu Á",
            "detail": "Đại diện bóng đá Việt Nam đã phải nhận trận thua cay đắng trên sân khách vào tối ngày 14 tháng 10 sau một sai lầm cá nhân đáng trách ở khâu phòng ngự. Dù kiểm soát bóng nhỉnh hơn và tạo ra nhiều cơ hội ghi bàn rõ rệt trong hiệp một, các chân sút áo đỏ lại tỏ ra nóng vội ở những pha dứt điểm cuối cùng. Bước sang hiệp hai, việc trung vệ Việt kiều Lương Chí Khải phán đoán sai điểm rơi của quả bóng đã biếu không cho nhà vô địch Indonesia bàn thắng định đoạt trận đấu. Huấn luyện viên trưởng bày tỏ sự tiếc nuối khi đội nhà đánh rơi điểm số trong một thế trận hoàn toàn có thể giành chiến thắng. Thất bại này khiến Thể Công Viettel gặp bất lợi lớn trong cuộc đua giành tấm vé đi tiếp vào vòng knock-out."
        },
        {
            "id": "art_40",
            "group": "V-League & CLB Việt Nam",
            "title": "CLB Công an Hà Nội thua sát nút Kashima Antlers 0-1 tại AFC Champions League Elite",
            "detail": "Chạm trán nhà đương kim vô địch J-League vào tối ngày 13 tháng 10, đoàn quân của huấn luyện viên Mano Polking đã trình diễn lối chơi kiên cường và kỷ luật vượt ngoài mong đợi. Đội bóng ngành công an chủ động nhường thế trận, tổ chức phòng ngự nhiều lớp chặt chẽ và suýt chút nữa có bàn mở tỷ số từ các pha phản công thần tốc của Leo Artur. Tuy nhiên, đẳng cấp vượt trội của đại diện xứ sở mặt trời mọc đã được cụ thể hóa bằng pha dứt điểm lạnh lùng ở phút thứ 78 của trận đấu. Dù không thể giành điểm, màn thể hiện sòng phẳng trước ứng cử viên hàng đầu châu lục vẫn mang lại niềm tự hào lớn cho người hâm mộ bóng đá thủ đô. Thầy trò ông Polking vẫn nắm trong tay nhiều cơ hội vượt qua vòng bảng nếu duy trì được tinh thần chiến đấu này."
        },
        {
            "id": "art_43",
            "group": "V-League & CLB Việt Nam",
            "title": "Nguyễn Tiến Linh cán mốc 90 bàn thắng chuyên nghiệp cấp câu lạc bộ",
            "detail": "Pha lập công đẹp mắt vào lưới câu lạc bộ Sông Lam Nghệ An vào ngày 13 tháng 10 đã đưa trung phong số một của đội tuyển Việt Nam chạm cột mốc lịch sử 90 bàn thắng trong sự nghiệp thi đấu đỉnh cao. Đây cũng là bàn thắng thứ hai liên tiếp của chân sút sinh năm 1997 chỉ sau hai trận khoác áo câu lạc bộ mới, khẳng định đẳng cấp của một sát thủ vòng cấm hàng đầu. Khả năng chạy chỗ thông minh và dứt điểm đa dạng của Tiến Linh tiếp tục là nguồn cảm hứng lớn nhất trên mặt trận tấn công của toàn đội. Sự ổn định đáng kinh ngạc của anh trong bối cảnh các tiền đạo nội khác đang sa sút phong độ là tín hiệu vô cùng lạc quan cho ban huấn luyện đội tuyển quốc gia. Tiến Linh khẳng định khát khao lớn nhất của anh là tiếp tục nâng cao thành tích để chạm mốc 100 bàn thắng trong tương lai gần."
        },

        # ======================================================================
        # NHÓM 3: BÓNG ĐÁ CHÂU ÂU & QUỐC TẾ (8 TIN)
        # ======================================================================
        {
            "id": "art_04",
            "group": "Bóng Đá Châu Âu & Quốc Tế",
            "title": "Chủ tịch FIFA Gianni Infantino xin lỗi và công bố gói tài trợ 25 triệu USD cho các liên đoàn",
            "detail": "Ngày 16 tháng 10, người đứng đầu cơ quan bóng đá quyền lực nhất hành tinh đã lên tiếng nhận lỗi trước công chúng vì những thiếu sót liên quan đến công tác truyền thông trong chương trình phát triển bóng đá. Đồng thời, ông Gianni Infantino cũng chính thức công bố ngân quỹ hỗ trợ khổng lồ lên tới 25 triệu USD trong vòng 4 năm cho mỗi liên đoàn thành viên, trong đó có Liên đoàn bóng đá Việt Nam. Khoản kinh phí này được kỳ vọng sẽ giải quyết triệt để bài toán thiếu hụt tài chính trong việc xây dựng cơ sở hạ tầng và nâng cao chất lượng các giải bóng đá trẻ. Quyết định tăng ngân sách diễn ra trong bối cảnh FIFA đang đẩy mạnh nỗ lực phổ cập hóa bóng đá đến các quốc gia đang phát triển. Đây được xem là động thái xoa dịu làn sóng chỉ trích từ các tổ chức thành viên suốt thời gian qua."
        },
        {
            "id": "art_11",
            "group": "Bóng Đá Châu Âu & Quốc Tế",
            "title": "PSG hạ gục Manchester City với tỷ số 4-2 ngay tại thánh địa Etihad",
            "detail": "Rạng sáng ngày 15 tháng 10, đại diện nước Pháp đã tạo nên cơn địa chấn tại đấu trường Champions League khi hủy diệt đoàn quân thiện chiến của Pep Guardiola bằng màn trình diễn tấn công siêu hạng. Những đòn phản công chớp nhoáng với tốc độ kinh hoàng của hàng công Paris Saint-Germain đã xé toang hoàn toàn tuyến phòng ngự trứ danh của các nhà đương kim vô địch nước Anh. Sự lúng túng trong khâu kèm người và mất tập trung của các trung vệ Man City đã bị đối phương trừng phạt bằng 4 bàn thắng đẳng cấp thế giới. Thất bại tủi hổ ngay trên sân nhà đẩy Man City vào một cuộc khủng hoảng niềm tin sâu sắc khi bước vào giai đoạn then chốt của mùa giải. Trong khi đó, chiến thắng lịch sử này khẳng định vị thế ứng cử viên hàng đầu cho chức vô địch châu Âu của câu lạc bộ thành Paris."
        },
        {
            "id": "art_22",
            "group": "Bóng Đá Châu Âu & Quốc Tế",
            "title": "Giải Saudi Pro League hoãn trận đấu của Ronaldo do bất ổn an ninh khu vực",
            "detail": "Ngày 15 tháng 10, ban tổ chức giải bóng đá vô địch quốc gia Ả Rập Xê Út đã đưa ra thông báo khẩn cấp về việc tạm hoãn 3 trận đấu thuộc vòng đấu cuối tuần, bao gồm cả trận đấu có sự góp mặt của Cristiano Ronaldo trong màu áo Al Nassr. Quyết định được đưa ra sau khi tình hình an ninh tại khu vực Trung Đông có những diễn biến leo thang phức tạp, đe dọa trực tiếp đến sự an toàn của các vận động viên và khán giả đến sân. Việc tạm dừng các hoạt động thi đấu thể thao cũng làm dấy lên mối lo ngại sâu sắc về khả năng tổ chức vòng chung kết Asian Cup 2027 đúng theo kế hoạch ban đầu. Ban tổ chức địa phương đang phối hợp chặt chẽ với các cơ quan an ninh để đánh giá lại toàn bộ công tác bảo vệ trước khi đưa ra quyết định nối lại giải đấu."
        },
        {
            "id": "art_25",
            "group": "Bóng Đá Châu Âu & Quốc Tế",
            "title": "Messi kiến tạo đẳng cấp giúp Inter Miami thắng 2-0 và đoạt vé sớm vào vòng play-off MLS Cup",
            "detail": "Sáng ngày 15 tháng 10, siêu sao Lionel Messi tiếp tục chứng minh tầm ảnh hưởng tuyệt đối của mình khi truyền cảm hứng cho chiến thắng thuyết phục 2-0 của Inter Miami trước đối thủ sừng sỏ New York City. Đường chuyền dọn cỗ xé toang hàng thủ đối phương ở hiệp hai của El Pulga đã tạo điều kiện không thể thuận lợi hơn để De Paul ghi bàn thắng nhân đôi cách biệt. Sự ăn ý hoàn hảo giữa các cựu binh từng thi đấu tại châu Âu giúp câu lạc bộ bang Florida làm chủ hoàn toàn thế trận và kiểm soát bóng vượt trội suốt 90 phút thi đấu. Chiến thắng quan trọng này giúp Inter Miami chính thức ghi tên mình vào vòng play-off tranh chức vô địch MLS Cup sớm hơn dự kiến. Người hâm mộ kỳ vọng Messi sẽ tiếp tục duy trì phong độ thăng hoa để đưa đội bóng đến danh hiệu vô địch quốc nội lịch sử."
        },
        {
            "id": "art_41",
            "group": "Bóng Đá Châu Âu & Quốc Tế",
            "title": "Lisandro Martinez chỉ trích ban lãnh đạo Manchester United sau thất bại 0-2 trước Atletico Madrid",
            "detail": "Trung vệ người Argentina đã không giữ được sự bình tĩnh và công khai bày tỏ sự thất vọng sâu sắc đối với giới thượng tầng câu lạc bộ sau trận thua muối mặt tại vòng bảng cúp C1 vào ngày 14 tháng 10. Lisandro Martinez thẳng thắn chỉ ra rằng đội bóng đang thiếu đi định hướng chiến lược dài hạn và không được đầu tư đúng mức để có thể cạnh tranh sòng phẳng ở đẳng cấp cao nhất châu Âu. Lối chơi rệu rã cùng tinh thần chiến đấu bạc nhược của các đồng đội trên sân Metropolitano đã khiến Quỷ đỏ hoàn toàn bị đối thủ bóp nghẹt suốt cả trận đấu. Những phát biểu gay gắt của trung vệ trụ cột này ngay lập tức thổi bùng lên cơn bão chỉ trích hướng về phía các ông chủ và ban giám đốc thể thao của câu lạc bộ. Phòng thay đồ của đội bóng thành Manchester đứng trước nguy cơ rạn nứt nghiêm trọng nếu thành tích thi đấu không sớm được cải thiện."
        },
        {
            "id": "art_47",
            "group": "Bóng Đá Châu Âu & Quốc Tế",
            "title": "Hàng công Barcelona ghi 9 bàn thắng sau 10 trận mở màn mùa giải mới",
            "detail": "Sau một mùa hè đầy biến động với việc chia tay hàng loạt chân sút trụ cột, đội bóng xứ Catalunya đang tìm lại sức mạnh tấn công hủy diệt nhờ sự thăng hoa rực rỡ của dàn sao trẻ. Bộ đôi Raphinha và thần đồng Lamine Yamal liên tục khuấy đảo hành lang hai cánh của đối phương bằng kỹ thuật điêu luyện và khả năng kiến tạo cơ hội ghi bàn ở đẳng cấp cao nhất. Bên cạnh đó, sự hòa nhập nhanh chóng của các tân binh trên hàng tiền đạo đã giúp đội chủ sân Camp Nou giải quyết triệt để bài toán khan hiếm bàn thắng từ đầu mùa. Huấn luyện viên trưởng bày tỏ sự hài lòng tột độ khi triết lý bóng đá kiểm soát và tấn công dồn dập đang được các học trò vận hành một cách trơn tru. Với 9 bàn thắng sau 10 trận đấu, Barcelona gửi đi lời thách thức đanh thép đến các đối thủ cạnh tranh trực tiếp trên mọi đấu trường."
        },
        {
            "id": "art_49",
            "group": "Bóng Đá Châu Âu & Quốc Tế",
            "title": "Louis van Gaal tuyên bố bị Manchester United sa thải do Man City vi phạm luật tài chính",
            "detail": "Cựu huấn luyện viên trưởng của đội chủ sân Old Trafford đã có những phát biểu gây sốc khi nhắc lại biến cố ông bị chấm dứt hợp đồng sau khi giành chức vô địch FA Cup mùa giải 2015-2016. Chiến lược gia người Hà Lan cho rằng việc Manchester City gian lận tài chính trong nhiều năm đã gián tiếp tước đi tấm vé tham dự Champions League của Quỷ đỏ vào thời điểm đó. Theo ông, nếu đối thủ cạnh tranh cùng thành phố bị xử lý nghiêm minh theo luật công bằng tài chính, vị thế của Manchester United và tương lai cá nhân ông tại câu lạc bộ đã hoàn toàn khác. Những tuyên bố đanh thép của Van Gaal lại một lần nữa hâm nóng cuộc điều tra hơn 115 cáo buộc vi phạm tài chính mà Man City đang phải đối mặt từ ban tổ chức Premier League. Dư luận bóng đá Anh đang đổ dồn sự chú ý vào phán quyết cuối cùng của tòa án độc lập trong thời gian tới."
        },
        {
            "id": "art_50",
            "group": "Bóng Đá Châu Âu & Quốc Tế",
            "title": "Phân tích kỹ năng di chuyển phá bẫy việt vị hoàn hảo của Erling Haaland",
            "detail": "Các chuyên gia phân tích dữ liệu thể thao quốc tế vừa công bố một nghiên cứu chuyên sâu về hiệu suất săn bàn đáng kinh ngạc của cỗ máy ghi bàn người Na Uy trong màu áo Manchester City. Bí quyết giúp tiền đạo sinh năm 2000 duy trì hiệu suất nhả đạn khủng khiếp nằm ở khả năng căn thời gian xuất phát và kỹ thuật luồn ra sau lưng trung vệ đối phương ở ranh giới một phần mười giây. Haaland luôn chủ động quan sát nhịp chạm bóng của tiền vệ kiến thiết trước khi thực hiện những pha bứt tốc chớp nhoáng khiến toàn bộ hệ thống bẫy việt vị của đối thủ trở nên vô dụng. Thể hình hộ pháp kết hợp với tốc độ xé gió giúp anh dễ dàng làm chủ không gian và giành chiến thắng tuyệt đối trong các pha tranh chấp một đối một. Khả năng chạy chỗ đỉnh cao này biến tiền đạo 24 tuổi trở thành cơn ác mộng kinh hoàng đối với mọi hàng phòng ngự trên khắp lục địa già."
        },

        # ======================================================================
        # NHÓM 4: THỂ THAO KHÁC (3 TIN)
        # ======================================================================
        {
            "id": "art_17",
            "group": "Thể Thao Khác",
            "title": "Trần Quyết Chiến xuất phát từ vòng loại World Cup Billiards Yanggu 2026 tại Hàn Quốc",
            "detail": "Tay cơ số một của làng carom 3 băng Việt Nam đang đứng trước thử thách cực lớn khi không còn nằm trong nhóm hạt giống hàng đầu được đặc cách vào thẳng vòng đấu chính thức. Sự biến động về điểm số trên bảng xếp hạng thế giới sau các chặng đấu vừa qua đã đẩy cơ thủ người Hà Tĩnh phải thi đấu từ vòng loại khắc nghiệt tranh tài từ ngày 2 đến ngày 8 tháng 11 tới. Việc phải thi đấu nhiều trận liên tiếp trong thể thức thi đấu loại trực tiếp tiềm ẩn rủi ro rất lớn trước những đối thủ có lối đánh ngổ ngáo và tâm lý thoải mái. Tuy nhiên, bản lĩnh thi đấu kiên cường và kinh nghiệm dày dạn tại các đấu trường World Cup vẫn là điểm tựa vững chắc để Quyết Chiến vượt qua áp lực. Người hâm mộ thể thao nước nhà kỳ vọng anh sẽ sớm tìm lại cảm giác bi tốt nhất để bảo vệ vị thế của billiards Việt Nam trên bản đồ thế giới."
        },
        {
            "id": "art_21",
            "group": "Thể Thao Khác",
            "title": "CLB Hà Nội Tasco Auto thất thủ trước Hóa chất Đức Giang tại giải bóng chuyền nữ quốc gia",
            "detail": "Chuỗi trận toàn thắng ấn tượng của đội bóng nữ thủ đô đã chính thức bị chặn đứng vào ngày 15 tháng 10 sau cuộc đọ sức kịch tính tại giai đoạn 2 giải bóng chuyền vô địch quốc gia 2026. Lối chơi phòng thủ kiên cường cùng những pha đập bóng uy lực từ hai biên của các ngoại binh phía Hóa chất Đức Giang đã làm phá sản hoàn toàn các phương án chiến thuật của đối thủ. Sự mất tập trung ở những thời điểm quyết định trong hiệp thi đấu thứ tư đã khiến Hà Nội Tasco Auto đánh rơi lợi thế dẫn điểm một cách đầy cay đắng. Thất bại bất ngờ này khiến cục diện bảng đấu trở nên vô cùng khó lường khi khoảng cách điểm số giữa các đội nhóm đầu bị thu hẹp đáng kể. Ban huấn luyện đội bóng thủ đô sẽ phải nhanh chóng chấn chỉnh tâm lý thi đấu của các vận động viên nếu không muốn đánh mất tấm vé vào chơi trận chung kết toàn quốc."
        },
        {
            "id": "art_48",
            "group": "Thể Thao Khác",
            "title": "Đội đua F1 McLaren truyền cảm hứng giúp các bệnh viện Anh tối ưu quy trình cấp cứu xuống 7 giây",
            "detail": "Một lần thay lốp và tiếp nhiên liệu chuẩn xác đến từng phần nghìn giây của đội đua xe công thức một McLaren đã bất ngờ trở thành hình mẫu cải tiến y tế mang tính đột phá tại Vương quốc Anh. Các bác sĩ và chuyên gia phẫu thuật hàng đầu tại London đã nghiên cứu kỹ lưỡng cách thức phân công nhiệm vụ và phối hợp đồng bộ giữa các kỹ thuật viên trong khu vực pit stop của giải đua F1. Bằng cách áp dụng quy trình kiểm soát thời gian nghiêm ngặt tương tự, kíp trực cấp cứu đã rút ngắn thời gian chuẩn bị thiết bị hồi sức tim phổi cho bệnh nhân nguy kịch xuống chỉ còn chưa đầy 7 giây. Sự chuyển giao công nghệ tư duy giữa thể thao đỉnh cao và y học thực hành đã góp phần giảm thiểu tối đa các sai sót chuyên môn và cứu sống hàng trăm bệnh nhân qua cơn thập tử nhất sinh. Đây được xem là minh chứng rõ ràng nhất cho thấy sự kết hợp liên ngành có thể tạo ra những giá trị nhân văn to lớn cho toàn xã hội."
        }
    ]

    return stories


def build_shorts_stories(raw_news: Dict[str, Any], current_date: str = "16.10.2026") -> List[Dict[str, str]]:
    """
    Chọn lọc 6 tin nóng nhất (HOTTEST) cho video Shorts 9:16.
    Mỗi tin chỉ 1-2 câu ngắn gọn, đọc siêu nhanh (25-45 từ/tin).
    """
    shorts_list = [
        {
            "id": "art_11",
            "group": "Cúp C1",
            "title": "PSG hạ gục Manchester City 4-2 ngay tại sân Etihad",
            "detail": "PSG tạo cơn địa chấn tại Champions League khi nã 4 bàn vào lưới Man City ngay tại thánh địa Etihad rạng sáng ngày 15 tháng 10. Thất bại cay đắng đẩy thầy trò Pep Guardiola vào khủng hoảng phong độ sâu sắc."
        },
        {
            "id": "art_01",
            "group": "ĐT Việt Nam",
            "title": "Tuyển Việt Nam quyết thắng Kyrgyzstan và Đài Loan để tăng hạng FIFA",
            "detail": "Đội tuyển Việt Nam buộc phải giành trọn 6 điểm ở hai trận giao hữu tại Thiên Trường từ ngày 11 đến 15 tháng 11. Mục tiêu tối thượng là bứt phá lên nhóm 95 thế giới để giữ lợi thế hạt giống châu lục."
        },
        {
            "id": "art_25",
            "group": "MLS Cup",
            "title": "Messi kiến tạo đẳng cấp đưa Inter Miami vào play-off MLS Cup",
            "detail": "Siêu sao Lionel Messi tỏa sáng rực rỡ với đường chuyền dọn cỗ giúp Inter Miami thắng New York City 2-0 sáng ngày 15 tháng 10. Đội bóng áo hồng chính thức đoạt vé sớm vào vòng tranh chức vô địch MLS."
        },
        {
            "id": "art_43",
            "group": "V-League",
            "title": "Nguyễn Tiến Linh cán mốc 90 bàn thắng chuyên nghiệp cấp câu lạc bộ",
            "detail": "Bàn thắng vào lưới Sông Lam Nghệ An ngày 13 tháng 10 đưa Tiến Linh chạm cột mốc lịch sử 90 bàn thắng cấp câu lạc bộ. Chân sút số một tuyển Việt Nam đang thăng hoa rực rỡ với 2 bàn sau 2 trận."
        },
        {
            "id": "art_07",
            "group": "World Cup Trẻ",
            "title": "U17 Việt Nam tự tin tạo địa chấn tại VCK U17 World Cup 2026",
            "detail": "Huấn luyện viên Cristiano Roland khẳng định U17 Việt Nam đã sẵn sàng thi đấu sòng phẳng trước các đối thủ hàng đầu thế giới. Toàn đội quyết tâm săn tìm điểm số lịch sử tại ngày hội bóng đá toàn cầu."
        },
        {
            "id": "art_41",
            "group": "Man United",
            "title": "Lisandro Martinez chỉ trích ban lãnh đạo Man United sau trận thua Atletico",
            "detail": "Trung vệ Lisandro Martinez công khai chỉ trích ban lãnh đạo Quỷ đỏ thiếu đầu tư chiều sâu sau thất bại 0-2 ngày 14 tháng 10. Phòng thay đồ của đội chủ sân Old Trafford đang đứng trước nguy cơ dậy sóng."
        }
    ]
    return shorts_list


def format_thethao_txt(stories: List[Dict[str, str]]) -> str:
    """Định dạng bản thảo thethao.txt chuẩn cú pháp kiểm duyệt."""
    lines: List[str] = []
    for idx, s in enumerate(stories, 1):
        lines.append("---")
        lines.append(f"[TIN {idx:02d}] - Nhóm: {s['group']}")
        lines.append(f"ID: {s['id']}")
        lines.append(f"Tiêu đề: {s['title']}")
        lines.append(f"Chi tiết: {s['detail']}")
    lines.append("---")
    return "\n".join(lines)


def format_shorts_txt(shorts_stories: List[Dict[str, str]]) -> str:
    """Định dạng bản thảo shorts.txt chuẩn cho kịch bản video dọc 9:16."""
    lines: List[str] = []
    for idx, s in enumerate(shorts_stories, 1):
        lines.append("---")
        lines.append(f"[SHORT {idx:02d}] - Nhóm: {s['group']}")
        lines.append(f"ID: {s['id']}")
        lines.append(f"Tiêu đề: {s['title']}")
        lines.append(f"Lời bình: {s['detail']}")
    lines.append("---")
    return "\n".join(lines)


def generate_thethao_txt_file(day_str: str, output_path: Optional[str] = None) -> str:
    """Sinh file thethao.txt tại outputs/DD.MM.YYYY/thethao.txt."""
    if output_path is None:
        day_dir = paths.project_dir(day_str)
        output_path = os.path.join(day_dir, "thethao.txt")

    raw_news = load_raw_news()
    stories = build_editorial_stories(raw_news, current_date=day_str)
    content = format_thethao_txt(stories)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


def generate_shorts_files(day_str: str, output_txt: Optional[str] = None, output_json: Optional[str] = None) -> Tuple[str, List[Dict[str, Any]]]:
    """Sinh các file shorts.txt và shorts.json cho định dạng video 9:16."""
    day_dir = paths.project_dir(day_str)
    if output_txt is None:
        output_txt = os.path.join(day_dir, "shorts.txt")
    if output_json is None:
        output_json = os.path.join(day_dir, "shorts.json")

    raw_news = load_raw_news()
    shorts_stories = build_shorts_stories(raw_news, current_date=day_str)
    txt_content = format_shorts_txt(shorts_stories)

    os.makedirs(os.path.dirname(output_txt), exist_ok=True)
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(txt_content)

    json_payload = []
    for idx, s in enumerate(shorts_stories, 1):
        json_payload.append({
            "short_id": idx,
            "id": s["id"],
            "group": s["group"],
            "title": s["title"],
            "script": s["detail"]
        })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(json_payload, f, ensure_ascii=False, indent=2)

    return txt_content, json_payload


def main() -> None:
    parser = argparse.ArgumentParser(description="m1b — Biên tập thethao.txt & shorts.txt/json chuẩn LLM Writer")
    parser.add_argument("--day", type=str, default=None, help="Tên ngày (DD.MM.YYYY)")
    parser.add_argument("--input", type=str, default=None, help="File temp_raw_news.json")
    parser.add_argument("--out", type=str, default=None, help="File xuất thethao.txt")

    args = parser.parse_args()
    day_str = args.day or paths.get_today_dir_name()
    day_dir = paths.project_dir(day_str)
    out_path = args.out or os.path.join(day_dir, "thethao.txt")

    banner("M1B — BIÊN TẬP BẢN THẢO THỂ THAO (16:9 & 9:16)", f"Ngày {day_str}")
    step("1. Biên tập các tin thể thao chuyên sâu cho video 16:9 (thethao.txt)...")
    generate_thethao_txt_file(day_str, out_path)
    ok(f"Đã xuất bản thảo 16:9: {paths.rel_to_root(out_path)}")

    step("2. Biên tập 6 tin nóng cho video ngắn 9:16 (shorts.txt & shorts.json)...")
    generate_shorts_files(day_str)
    ok(f"Đã xuất kịch bản 9:16: {paths.rel_to_root(os.path.join(day_dir, 'shorts.txt'))} và shorts.json")


if __name__ == "__main__":
    main()
