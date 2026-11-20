#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_script_09_11.py — Khởi tạo kịch bản 25 bản tin cho tuần 02.11 - 08.11.2026
Xuất bản: Thứ Hai 09.11.2026 tại outputs/09.11.2026/
"""

import sys
sys.dont_write_bytecode = True

import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAY_DIR = ROOT / "outputs" / "09.11.2026"
DAY_DIR.mkdir(parents=True, exist_ok=True)

ITEMS = [
    {
        "id": 1,
        "art_id": "art_01",
        "group": "Nhóm: Sự kiện lịch sử",
        "title": "Cristiano Ronaldo giã từ đội tuyển Bồ Đào Nha sau 23 năm",
        "summary": "Chiều ngày 5 tháng 11, cả thế giới bóng đá bàng hoàng khi siêu sao 41 tuổi Cristiano Ronaldo chính thức đăng tải video thông báo giã từ đội tuyển quốc gia Bồ Đào Nha, khép lại hành trình 23 năm huyền thoại với 234 trận đấu và 146 bàn thắng kỷ lục. Trong thông điệp chia tay đầy xúc động, thủ quân mang áo số 7 khẳng định đây là thời điểm hoàn hảo để nhường lại sân khấu cho thế hệ đàn em tài năng. Anh cũng chủ động từ chối đề nghị tổ chức trận đấu tri ân riêng của Liên đoàn bóng đá Bồ Đào Nha để toàn đội giữ sự tập trung cao nhất cho chiến dịch Nations League. Quyết định của Ronaldo đánh dấu sự kết thúc của một kỷ nguyên vĩ đại, nơi anh đưa bóng đá Bồ Đào Nha chạm đỉnh vinh quang với chức vô địch Euro 2016 và 2 danh hiệu Nations League.",
        "digest_line": "Ở tuổi 41, Cristiano Ronaldo chính thức tuyên bố giã từ đội tuyển Bồ Đào Nha sau 23 năm cống hiến với kỷ lục 234 trận và 146 bàn thắng.",
        "digest_title": "Cristiano Ronaldo giã từ đội tuyển Bồ Đào Nha sau 23 năm",
        "total_images": 12,
        "hide_date_chip": False
    },
    {
        "id": 2,
        "art_id": "art_02",
        "group": "Nhóm: Sự kiện lịch sử",
        "title": "Góc khuất Ronaldo phớt lờ HLV Jorge Jesus và làn sóng tri ân",
        "summary": "Quyết định giã từ đội tuyển Bồ Đào Nha của Cristiano Ronaldo không chỉ gây chấn động mà còn hé lộ những góc khuất rạn nứt gay gắt với huấn luyện viên trưởng Jorge Jesus. Theo các nguồn tin uy tín từ truyền thông Bồ Đào Nha, Ronaldo đã chủ động cắt đứt liên lạc và phớt lờ mọi cuộc gọi của ban huấn luyện trước ngày công bố danh sách tập trung. Chủ tịch câu lạc bộ thời thơ ấu Andorinha đã công khai lên tiếng chỉ trích huấn luyện viên Jorge Jesus phản bội biểu tượng vĩ đại của bóng đá nước nhà. Trong khi đó, các câu lạc bộ Al Hilal, Real Madrid, Sporting Lisbon, Manchester United cùng hàng loạt đồng đội như Rafael Leao và Bruno Fernandes đã đồng loạt gửi những thông điệp tri ân sâu sắc, khẳng định di sản của CR7 sẽ mãi trường tồn cùng lịch sử túc cầu.",
        "digest_line": "Ronaldo hé lộ rạn nứt gay gắt với HLV Jorge Jesus khi chia tay đội tuyển, trong khi các CLB cũ và đồng đội đồng loạt gửi lời tri ân sâu sắc.",
        "digest_title": "Góc khuất rạn nứt của Ronaldo và HLV Jorge Jesus khi chia tay ĐTQG",
        "total_images": 10,
        "hide_date_chip": False
    },
    {
        "id": 3,
        "art_id": "art_03",
        "group": "Nhóm: Sôi động Champions League",
        "title": "Đội bóng của Cesc Fabregas thắng 9-1 lập kỷ lục cúp C1",
        "summary": "Địa chấn lịch sử đã bùng nổ tại Champions League khi tân binh Como dưới trướng huấn luyện viên Cesc Fabregas hủy diệt chủ nhà Lens với tỷ số không tưởng 9-1 ngay tại thánh địa Stade Bollaert-Delelis. Đây là chiến thắng sân khách đậm nhất trong lịch sử Champions League, đồng thời cân bằng kỷ lục cách biệt 8 bàn thắng của Liverpool năm 2007 và Real Madrid năm 2015. Tiền đạo Anastasios Douvikas rực sáng với một cú hat-trick để vươn lên dẫn đầu danh sách Vua phá lưới cúp C1 mùa này với 6 bàn. Khoảnh khắc xúc động nhất trận diễn ra khi Nico Paz giơ cao chiếc áo đấu tri ân người đàn anh vừa qua đời Jesús de Miguel, trong khi tài năng trẻ 18 tuổi Matteo Papaccioli cũng kịp ghi dấu ấn bằng bàn thắng ấn định tỷ số 9-1 ngay trong ngày ra mắt.",
        "digest_line": "Como của HLV Cesc Fabregas tạo địa chấn lịch sử cúp C1 khi vùi dập Lens 9-1, thiết lập chiến thắng sân khách đậm nhất giải đấu.",
        "digest_title": "Đội bóng của Cesc Fabregas thắng 9-1 lập kỷ lục lịch sử cúp C1",
        "total_images": 12,
        "hide_date_chip": False
    },
    {
        "id": 4,
        "art_id": "art_04",
        "group": "Nhóm: Sôi động Champions League",
        "title": "Siêu phẩm phút 90+2 của Valverde giúp Real Madrid thắng 3-2",
        "summary": "Chuyến hành quân đến Hy Lạp của Real Madrid tại lượt 4 Champions League đã trở thành một đêm nghẹt thở đến điên rồ, khi đội bóng Hoàng gia Tây Ban Nha hai lần bị AEK Athens dẫn trước trên sân OPAP Arena. Sau khi Jude Bellingham đánh gót tinh tế gỡ hòa 1-1 và Kylian Mbappé đệm bóng san bằng 2-2 ở phút 78 để có bàn thắng thứ 16 trên mọi đấu trường mùa này, người hâm mộ Real Madrid đã vỡ òa cảm xúc ở phút bù giờ thứ 2. Đội trưởng Federico Valverde tung cú nã đại bác sấm sét từ cự ly 22 mét, đưa bóng găm thẳng vào góc chữ A ấn định chiến thắng ngược dòng 3-2. Ba điểm nghẹt thở giúp thầy trò Carlo Ancelotti duy trì mạch 4 trận toàn thắng để củng cố vững chắc ngôi nhì bảng xếp hạng tổng Champions League.",
        "digest_line": "Siêu phẩm nã đại bác phút 90+2 của Federico Valverde giúp Real Madrid lội ngược dòng nghẹt thở 3-2 trước AEK Athens tại Champions League.",
        "digest_title": "Siêu phẩm phút 90+2 của Valverde giúp Real Madrid thắng ngược 3-2",
        "total_images": 12,
        "hide_date_chip": False
    },
    {
        "id": 5,
        "art_id": "art_05",
        "group": "Nhóm: Sôi động Champions League",
        "title": "Haaland cán mốc 62 bàn cúp C1 giúp Man City hạ Leipzig 3-2",
        "summary": "Tại Red Bull Arena, Erling Haaland một lần nữa chứng minh bản năng săn bàn thượng hạng khi đệm bóng cận thành ấn định thắng lợi 3-2 nghẹt thở cho Manchester City trước RB Leipzig ở phút 78. Bàn thắng quý giá này không chỉ giúp Man City bỏ túi trọn vẹn 3 điểm mà còn đưa Haaland cán mốc 62 bàn thắng chỉ sau 61 trận đấu tại Champions League.",
        "digest_line": "Erling Haaland tỏa sáng ở phút 78 giúp Man City thắng kịch tính Leipzig 3-2, cán mốc 62 bàn thắng sau 61 trận tại Champions League.",
        "digest_title": "Haaland cán mốc 62 bàn cúp C1 giúp Man City hạ Leipzig 3-2",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 6,
        "art_id": "art_06",
        "group": "Nhóm: Sôi động Champions League",
        "title": "Thảm họa bóng chết khiến Liverpool thua ngược Fenerbahce 2-3",
        "summary": "Dù dẫn trước 2 bàn nhờ công của sao mai 19 tuổi Trey Nyoni và Alexander Isak, Liverpool đã trải qua cơn ác mộng bóng chết tại chảo lửa Sukru Saracoglu. Fenerbahce dưới sự chỉ đạo của huấn luyện viên tạm quyền Dirk Kuyt tận dụng triệt để sai lầm phòng ngự để lội ngược dòng thắng lại 3-2 nhờ cú đánh đầu của Vedat Muriqi ở phút 84.",
        "digest_line": "Dẫn trước 2 bàn nhưng hàng thủ mắc sai lầm bóng chết tai hại, Liverpool thua ngược sốc 2-3 trước Fenerbahce tại Thổ Nhĩ Kỳ.",
        "digest_title": "Hàng thủ bóng chết thảm họa khiến Liverpool thua ngược Fenerbahce 2-3",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 7,
        "art_id": "art_07",
        "group": "Nhóm: Tâm chấn Ngoại hạng Anh",
        "title": "Nottingham Forest hạ gục Man City 3-1, Arsenal bỏ xa 6 điểm",
        "summary": "Chảo lửa City Ground rạng sáng cuối tuần đã chứng kiến cơn địa chấn lớn nhất vòng 10 Ngoại hạng Anh khi Nottingham Forest quật ngã gã khổng lồ Manchester City với tỷ số thuyết phục 3-1. Trận đấu bắt đầu bằng sai lầm chuyền về tai hại của Josko Gvardiol, tạo điều kiện cho Jair Cunha thoát xuống mở tỷ số ngay phút thứ 6. Sau đó, chính cựu tiền đạo trẻ của Man City là Liam Delap đã gieo sầu cho đội bóng cũ bằng một cú đúp đẳng cấp ở phút 18 và phút 73. Bàn volley rút ngắn cách biệt của Rayan Cherki không thể cứu vãn một ngày thi đấu bạc nhược của nhà đương kim vô địch. Trận thua thứ 3 liên tiếp trên mọi đấu trường khiến Man City bị Arsenal nới rộng khoảng cách lên thành 6 điểm trên đường đua vô địch, sau khi Pháo thủ hạ Hull City 1-0 nhờ bàn duy nhất của Martin Odegaard.",
        "digest_line": "Nottingham Forest quật ngã Man City 3-1 nhờ cú đúp của Liam Delap, khiến The Citizens bị Arsenal bỏ xa 6 điểm trên bảng xếp hạng.",
        "digest_title": "Nottingham Forest hạ gục Man City 3-1, Arsenal nới rộng cách biệt",
        "total_images": 12,
        "hide_date_chip": False
    },
    {
        "id": 8,
        "art_id": "art_08",
        "group": "Nhóm: Tâm chấn Ngoại hạng Anh",
        "title": "Man Utd hòa điên rồ Aston Villa 4-4 nhưng rơi vào nhóm đèn đỏ",
        "summary": "Manchester United tiếp tục lún sâu vào cuộc khủng hoảng phong độ tồi tệ bậc nhất lịch sử câu lạc bộ kể từ mùa giải 1986. Sau khi bị Nottingham Forest vượt mặt đẩy xuống vị trí thứ 18, Quỷ đỏ bước vào trận tiếp đón Aston Villa tại Old Trafford với sức ép nghẹt thở đè nặng lên chiếc ghế của huấn luyện viên Michael Carrick. Trận cầu diễn ra điên rồ với màn rượt đuổi tỷ số khó tin khi Man Utd bị đối thủ dẫn 4-2 đến tận những phút bù giờ cuối cùng. Hai bàn thắng muộn của Joshua Zirkzee và Patrick Dorgu ở phút 90+6 chỉ giúp Quỷ đỏ giật lại 1 điểm trong trận hòa 4-4 đầy kịch tính. Tuy nhiên, với vỏn vẹn 8 điểm sau 10 vòng đấu, Manchester United vẫn chính thức chìm trong nhóm cầm đèn đỏ rớt hạng trước khi bước vào đợt tập trung đội tuyển quốc gia.",
        "digest_line": "Hòa điên rồ Aston Villa 4-4 nhờ 2 bàn phút bù giờ, Manchester United vẫn ngậm ngùi rơi vào nhóm cầm đèn đỏ ở vị trí thứ 18 Ngoại hạng Anh.",
        "digest_title": "Man Utd hòa điên rồ Aston Villa 4-4 nhưng rơi xuống vị trí thứ 18",
        "total_images": 12,
        "hide_date_chip": False
    },
    {
        "id": 9,
        "art_id": "art_09",
        "group": "Nhóm: Sôi động sân cỏ châu Âu",
        "title": "Barcelona thắng ngược Atletico Madrid 2-1, đòi lại đỉnh bảng",
        "summary": "Cuộc đua vô địch La Liga tuần qua bùng nổ nghẹt thở đến những giây cuối cùng. Sau khi Real Madrid thắng áp đảo Valencia 3-0 nhờ sự tỏa sáng của Federico Valverde, Arda Guler và Kylian Mbappé để tạm thời leo lên ngôi đầu bảng, Barcelona đã có chuyến làm khách đầy cạm bẫy tới sân Metropolitano của Atletico Madrid. Dù bị Giuliano Simeone trừng phạt từ pha phản công mở tỷ số sớm cho đội chủ nhà, bản lĩnh của thầy trò Hansi Flick đã lên tiếng đúng lúc. Cú đúp bàn thắng đẳng cấp của tiền vệ trẻ Fermin Lopez trong hiệp hai đã giúp Barcelona lội ngược dòng ngoạn mục với thắng lợi 2-1, qua đó chính thức dập tắt tham vọng bứt phá của Atletico và đòi lại vị trí dẫn đầu bảng xếp hạng La Liga nhờ hơn Real Madrid chỉ số phụ.",
        "digest_line": "Bị dẫn trước tại Metropolitano, Barcelona ngược dòng ngoạn mục hạ Atletico Madrid 2-1 nhờ cú đúp của Fermin Lopez để đòi lại ngôi đầu La Liga.",
        "digest_title": "Barcelona thắng ngược Atletico Madrid 2-1, đòi lại ngôi đầu La Liga",
        "total_images": 10,
        "hide_date_chip": False
    },
    {
        "id": 10,
        "art_id": "art_10",
        "group": "Nhóm: Sôi động sân cỏ châu Âu",
        "title": "Chelsea thua sốc Sunderland 0-1 giữa tâm bão tranh cãi VAR",
        "summary": "Cơn khủng hoảng của nhóm đại gia London tiếp tục lan rộng khi Chelsea bất ngờ ngã ngựa 0-1 trước Sunderland tại vòng 10 Ngoại hạng Anh. Trận đấu kết thúc trong sự phẫn nộ dữ dội của cổ động viên The Blues khi tổ trọng tài và công nghệ VAR đưa ra hàng loạt phán quyết gây tranh cãi làm thay đổi cục diện.",
        "digest_line": "Chelsea nhận thất bại cay đắng 0-1 trước Sunderland tại vòng 10 Ngoại hạng Anh giữa tâm bão chỉ trích dữ dội về các quyết định của VAR.",
        "digest_title": "Chelsea thua sốc Sunderland 0-1 giữa bão tranh cãi trọng tài VAR",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 11,
        "art_id": "art_11",
        "group": "Nhóm: Sôi động sân cỏ châu Âu",
        "title": "RB Leipzig hủy diệt Frankfurt 6-0, Dortmund sảy chân ở Đức",
        "summary": "Tại vòng 8 giải vô địch quốc gia Đức Bundesliga, RB Leipzig đã có màn thị uy sức mạnh khủng khiếp khi đè bẹp Eintracht Frankfurt với tỷ số của một set tennis 6-0 để bám đuổi ngôi đầu. Ở chiều ngược lại, Borussia Dortmund tiếp tục chuỗi trận bất ổn khi để Werder Bremen cầm chân 2-2 đầy tiếc nuối.",
        "digest_line": "RB Leipzig vùi dập Eintracht Frankfurt 6-0 để củng cố nhóm đầu Bundesliga, trong khi Borussia Dortmund đánh rơi điểm số trước Werder Bremen.",
        "digest_title": "RB Leipzig vùi dập Frankfurt 6-0, Dortmund sảy chân tại Bundesliga",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 12,
        "art_id": "art_12",
        "group": "Nhóm: Góc khuất sân cỏ",
        "title": "Bi kịch tiền đạo Jesús de Miguel qua đời và kiến nghị đổi luật",
        "summary": "Bóng đá Tây Ban Nha và thế giới vừa trải qua một nỗi đau vô hạn khi tiền đạo 30 tuổi Jesús de Miguel của câu lạc bộ Tenerife đột ngột qua đời sau pha va chạm kinh hoàng vùng đầu với thủ môn Jesus Owono của FC Andorra tại giải hạng Nhì Tây Ban Nha. Dù được đội ngũ y tế sơ cứu khẩn cấp và chuyển thẳng đến bệnh viện, chấn thương sọ não quá nặng đã khiến anh không thể qua khỏi. Mọi trận đấu tại La Liga cuối tuần qua đều dành một phút mặc niệm trang nghiêm, trong khi Kylian Mbappé, Pedri và Rafael Nadal đồng loạt gửi lời chia buồn sâu sắc. Bi kịch này đã thôi thúc cựu thủ môn Colombia Nelson Ramos cùng các trọng tài quốc tế gửi đơn kiến nghị khẩn cấp lên FIFA và IFAB, yêu cầu sửa đổi Điều 12 Luật bóng đá để xử lý nghiêm các pha lao ra nguy hiểm của thủ môn.",
        "digest_line": "Sự ra đi thương tâm của tiền đạo Jesús de Miguel sau va chạm trên sân đã khiến bóng đá thế giới tiếc thương và thúc đẩy kiến nghị đổi luật FIFA.",
        "digest_title": "Bi kịch tiền đạo Jesús de Miguel qua đời và làn sóng kiến nghị đổi luật",
        "total_images": 10,
        "hide_date_chip": False
    },
    {
        "id": 13,
        "art_id": "art_13",
        "group": "Nhóm: Góc khuất sân cỏ",
        "title": "Những bi kịch va chạm đau lòng nhất lịch sử bóng đá thế giới",
        "summary": "Sự ra đi đột ngột của tiền đạo Jesús de Miguel tại Tây Ban Nha đang làm nhói lòng người hâm mộ, đồng thời gợi lại những bi kịch va chạm đẫm nước mắt trong lịch sử bóng đá thế giới. Đó là tai nạn của Raul Ramirez năm 2025, thủ môn Serhiy Perkhun năm 2001, thủ môn huyền thoại Choirul Huda năm 2017 và tiền đạo Akli Fairuz năm 2014.",
        "digest_line": "Nhìn lại những thảm kịch va chạm trên sân cỏ thế giới cướp đi sinh mạng của các cầu thủ, nhắc nhở bài toán an toàn tính mạng trong bóng đá.",
        "digest_title": "Những bi kịch va chạm đau lòng nhất lịch sử bóng đá thế giới",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 14,
        "art_id": "art_14",
        "group": "Nhóm: Chuyện lạ thế giới",
        "title": "Trận đấu 51 thẻ đỏ điên rồ tại Brazil phá kỷ lục Guinness",
        "summary": "Một trận đấu bóng đá trẻ tại bang Minas Gerais của Brazil đã chứng kiến màn ẩu đả tập thể hỗn loạn chưa từng có trong lịch sử, buộc trọng tài chính Fernando Modesto phải rút tổng cộng 51 chiếc thẻ đỏ trực tiếp. Trận bán kết giữa Uberlandia và Mamore chính thức xô đổ kỷ lục thế giới Guinness về số thẻ phạt nhiều nhất lịch sử.",
        "digest_line": "Hỗn chiến kinh hoàng tại giải trẻ Brazil buộc trọng tài rút tới 51 chiếc thẻ đỏ, chính thức phá vỡ kỷ lục Guinness thế giới.",
        "digest_title": "Trận cầu 51 thẻ đỏ điên rồ tại Brazil xô đổ kỷ lục Guinness thế giới",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 15,
        "art_id": "art_15",
        "group": "Nhóm: Chuyện lạ thế giới",
        "title": "Đội tuyển Áo vô địch thế giới môn bóng đá trên xe đạp tại Đức",
        "summary": "Giải vô địch thế giới môn bóng đá trên xe đạp Cycle-ball 2026 vừa khép lại đầy kịch tính tại Ludwigsburg, Đức. Trong môn thể thao độc đáo cấm tuyệt đối cầu thủ chạm chân xuống mặt sân, đội tuyển Áo đã xuất sắc đánh bại đội chủ nhà Đức với tỷ số áp đảo 8-1 trong trận chung kết để bước lên ngôi vô địch thế giới.",
        "digest_line": "Đội tuyển Áo xuất sắc vùi dập chủ nhà Đức 8-1 ở chung kết để đăng quang giải vô địch thế giới môn bóng đá trên xe đạp Cycle-ball 2026.",
        "digest_title": "Đội tuyển Áo vô địch thế giới môn bóng đá trên xe đạp tại Đức",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 16,
        "art_id": "art_16",
        "group": "Nhóm: Bóng đá Việt Nam",
        "title": "Đội tuyển Việt Nam triệu tập Olaha Mạnh Đức đấu Casper Cup",
        "summary": "Chuẩn bị cho giải giao hữu quốc tế Casper Cup 2026 diễn ra trên sân vận động Thiên Trường vào trung tuần tháng 11, đội tuyển Việt Nam dưới sự dẫn dắt của huấn luyện viên Kim Sang-sik đã chính thức công bố danh sách triệu tập với nhiều nét đổi mới mang tính đột phá. Trước sự vắng mặt đáng tiếc của chân sút chủ lực Nguyễn Xuân Son và thủ môn Đặng Văn Lâm vì lý do chấn thương, chiến lược gia người Hàn Quốc đã trao cơ hội ra mắt lịch sử cho tiền đạo nhập tịch gốc Nigeria Olaha Mạnh Đức, cùng trung vệ Việt kiều Mỹ sở hữu chiều cao 1m88 Lương Chí Khải. Theo lịch trình, đội tuyển Việt Nam sẽ có trận thử lửa đầu tiên gặp đội tuyển Đài Bắc Trung Hoa vào ngày 11 tháng 11, trước khi bước vào cuộc so tài đỉnh cao với đối thủ mạnh Kyrgyzstan vào ngày 17 tháng 11.",
        "digest_line": "HLV Kim Sang-sik triệu tập tân binh nhập tịch Olaha Mạnh Đức và trung vệ Việt kiều Lương Chí Khải lên tuyển Việt Nam dự Casper Cup 2026.",
        "digest_title": "Đội tuyển Việt Nam triệu tập Olaha Mạnh Đức chuẩn bị cho Casper Cup",
        "total_images": 10,
        "hide_date_chip": False
    },
    {
        "id": 17,
        "art_id": "art_17",
        "group": "Nhóm: Tâm chấn V-League",
        "title": "Nam Định giữ vững ngôi đầu, HAGL thoát đáy bảng V-League",
        "summary": "Vòng 7 giải vô địch quốc gia V-League 2026 chứng kiến những biến động vô cùng kịch tính trên bảng xếp hạng. Trên thánh địa Thiên Trường, dù không có được sự phục vụ của chân sút hàng đầu Nguyễn Xuân Son, nhà đương kim vô địch Thép Xanh Nam Định vẫn thể hiện bản lĩnh của ứng viên số một khi đánh bại Hồng Lĩnh Hà Tĩnh với tỷ số 2-1, qua đó tiếp tục duy trì mạch bất bại và ngự trị vững chắc trên đỉnh bảng. Trong khi đó ở nhóm cầm đèn đỏ, Hoàng Anh Gia Lai đã tạo nên một cơn địa chấn tại chảo lửa Pleiku khi xuất sắc quật ngã đại kình địch Hà Nội FC với tỷ số 2-1. Ba điểm quý giá trước đối thủ mạnh giúp đội bóng phố núi chính thức thoát khỏi vị trí đáy bảng trong niềm hân hoan tột độ của người hâm mộ Gia Lai.",
        "digest_line": "Thép Xanh Nam Định đánh bại Hà Tĩnh 2-1 để củng cố ngôi đầu bảng, trong khi HAGL hạ Hà Nội FC để chính thức thoát đáy bảng V-League.",
        "digest_title": "Nam Định xây chắc ngôi đầu, HAGL đánh bại Hà Nội FC thoát đáy bảng",
        "total_images": 10,
        "hide_date_chip": False
    },
    {
        "id": 18,
        "art_id": "art_18",
        "group": "Nhóm: Sân cỏ V-League",
        "title": "Công Phượng tỏa sáng giúp Đồng Nai giành chiến thắng đầu tay",
        "summary": "Tại giải hạng Nhất quốc gia, tiền đạo Nguyễn Công Phượng tiếp tục chứng minh phẩm chất ngôi sao khi có pha đi bóng lắt léo kiếm về quả phạt đền quyết định. Bàn thắng duy nhất trên chấm 11 mét giúp câu lạc bộ Đồng Nai đánh bại SHB Đà Nẵng 1-0, mang về chiến thắng đầu tiên tại mùa giải năm nay.",
        "digest_line": "Nguyễn Công Phượng tỏa sáng rực rỡ khi mang về quả phạt đền quyết định giúp Đồng Nai hạ Đà Nẵng 1-0, có chiến thắng đầu tay mùa này.",
        "digest_title": "Công Phượng tỏa sáng giúp Đồng Nai giành chiến thắng đầu tay",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 19,
        "art_id": "art_19",
        "group": "Nhóm: Sân cỏ V-League",
        "title": "Thể Công Viettel hòa Thanh Hóa 1-1 dù chơi hơn người từ hiệp 1",
        "summary": "Trên sân vận động Hàng Đẫy tối 8 tháng 11, Thể Công Viettel có lợi thế cực lớn khi được thi đấu hơn người từ hiệp 1 sau tấm thẻ đỏ trực tiếp của tiền vệ Nguyễn Bá Tiến bên phía Thanh Hóa vì pha đạp bóng nguy hiểm. Dù vậy, đội bóng áo lính lại bế tắc và chấp nhận chia điểm với trận hòa 1-1.",
        "digest_line": "Được chơi hơn người trong phần lớn thời gian trận đấu, Thể Công Viettel vẫn bất lực chia điểm 1-1 trước Đông Á Thanh Hóa trên sân Hàng Đẫy.",
        "digest_title": "Thể Công Viettel bị Thanh Hóa cầm hòa 1-1 dù thi đấu hơn người",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 20,
        "art_id": "art_20",
        "group": "Nhóm: Bóng đá Việt Nam",
        "title": "CLB nữ TP.HCM dừng bước trước đại diện Hàn Quốc tại cúp C1",
        "summary": "Đại diện ưu tú của bóng đá nữ Việt Nam là câu lạc bộ nữ Thành phố Hồ Chí Minh đã chính thức dừng bước tại cúp C1 nữ châu Á sau trận thua đáng tiếc trước câu lạc bộ Hwacheon KSPO của Hàn Quốc. Dù thi đấu kiên cường, các cô gái Việt Nam đành khép lại chuyến phiêu lưu lịch sử ở vòng tứ kết châu lục.",
        "digest_line": "Thi đấu nỗ lực nhưng trước đối thủ vượt trội từ Hàn Quốc, CLB nữ TP.HCM chính thức dừng bước tại vòng tứ kết cúp C1 nữ châu Á 2026.",
        "digest_title": "CLB nữ TP.HCM dừng bước trước đại diện Hàn Quốc tại cúp C1",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 21,
        "art_id": "art_21",
        "group": "Nhóm: Bóng đá Việt Nam",
        "title": "Xúc động trận cầu chia tay chảo lửa Long An trước ngày tháo dỡ",
        "summary": "Chiều 7 tháng 11, hàng ngàn cổ động viên bóng đá miền Tây đã đổ về sân vận động Long An để chứng kiến trận cầu chia tay đầy xúc động. Đây là trận thi đấu chính thức cuối cùng tại chảo lửa từng gắn liền với thời kỳ hoàng kim của Đồng Tâm Long An trước khi công trình được bàn giao để tháo dỡ quy hoạch.",
        "digest_line": "Hàng ngàn người hâm mộ miền Tây xúc động dự khán trận cầu cuối cùng tại sân vận động Long An trước khi chảo lửa lịch sử này bị tháo dỡ.",
        "digest_title": "Xúc động trận cầu chia tay chảo lửa Long An trước ngày tháo dỡ",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 22,
        "art_id": "art_22",
        "group": "Nhóm: Thể thao Việt Nam",
        "title": "Trần Quyết Chiến hạ số 1 thế giới tại World Cup Billiards",
        "summary": "Tại giải Carom 3 băng World Cup Yanggu 2026 diễn ra ở Hàn Quốc, cơ thủ số một Việt Nam Trần Quyết Chiến đã tạo nên một cơn địa chấn thực sự tại vòng 1/8. Thi đấu với phong độ xuất thần và những đường cơ chuẩn xác đến từng milimét, Quyết Chiến đã hủy diệt cơ thủ số một thế giới của chủ nhà là Cho Myung-woo với tỷ số cách biệt 50-23 chỉ sau 19 lượt cơ. Mặc dù sau đó phải dừng bước tại tứ kết trước huyền thoại Dick Jaspers, màn hạ gục ngoạn mục tay cơ đỉnh chóp thế giới của Trần Quyết Chiến vẫn là điểm sáng rực rỡ nhất của thể thao Việt Nam trên đấu trường quốc tế tuần qua.",
        "digest_line": "Trần Quyết Chiến thi đấu thăng hoa đè bẹp cơ thủ số một thế giới Cho Myung-woo 50-23 tại vòng 1/8 World Cup Billiards ở Hàn Quốc.",
        "digest_title": "Trần Quyết Chiến đè bẹp cơ thủ số 1 thế giới Cho Myung-woo 50-23",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 23,
        "art_id": "art_23",
        "group": "Nhóm: Thể thao đỉnh cao",
        "title": "Carlos Alcaraz hạ Ben Shelton, lần đầu vô địch Paris Masters",
        "summary": "Đêm 8 tháng 11 tại Pháp, trận chung kết giải quần vợt Paris Masters 2026 đã chứng kiến màn đăng quang lịch sử của tay vợt người Tây Ban Nha Carlos Alcaraz. Đối đầu với hiện tượng người Mỹ Ben Shelton sở hữu những cú giao bóng sấm sét, Alcaraz đã thể hiện đẳng cấp vượt trội ở các thời khắc quyết định để giành chiến thắng kịch tính với tỷ số 7-6 và 7-5 sau hai set đấu nghẹt thở. Danh hiệu này đánh dấu lần đầu tiên trong sự nghiệp Carlos Alcaraz nâng cao cúp vô địch tại Paris Masters, tạo đà tâm lý hưng phấn tột độ trước khi bước vào giải đấu tổng kết năm ATP Finals tại Turin.",
        "digest_line": "Đánh bại Ben Shelton với tỷ số 7-6 và 7-5 ở chung kết, Carlos Alcaraz lần đầu tiên trong sự nghiệp giành chức vô địch Paris Masters 2026.",
        "digest_title": "Carlos Alcaraz lần đầu đăng quang chức vô địch Paris Masters 2026",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 24,
        "art_id": "art_24",
        "group": "Nhóm: Thể thao đỉnh cao",
        "title": "F1 Brazil GP: Lando Norris thắng dưới mưa, Mercedes vô địch sớm",
        "summary": "Chặng đua Công thức 1 Sao Paulo Grand Prix tại trường đua Interlagos của Brazil đã diễn ra dưới cơn mưa tầm tã đầy biến động. Bất chấp điều kiện đường trơn trượt nguy hiểm, tay đua Lando Norris của đội McLaren đã có màn trình diễn xuất sắc khi dẫn đầu đoàn đua để cán đích đầu tiên giành chiến thắng chặng. Trong khi đó, đội đua Mercedes cũng chính thức ăn mừng chức vô địch Đội đua thế giới sớm trước các chặng cuối.",
        "digest_line": "Lando Norris xuất sắc chiến thắng dưới cơn mưa tầm tã tại Brazil GP, trong khi đội đua Mercedes chính thức đăng quang ngôi vô địch thế giới.",
        "digest_title": "Lando Norris thắng kịch tính tại F1 Brazil GP, Mercedes vô địch sớm",
        "total_images": 6,
        "hide_date_chip": False
    },
    {
        "id": 25,
        "art_id": "art_25",
        "group": "Nhóm: Thể thao Việt Nam",
        "title": "Trần Thị Thanh Thúy chuẩn bị rời Nhật Bản về dự Đại hội toàn quốc",
        "summary": "Chủ công số một của bóng chuyền nữ Việt Nam Trần Thị Thanh Thúy đang chuẩn bị khép lại thời gian thi đấu tại giải vô địch quốc gia Nhật Bản trong màu áo câu lạc bộ Gunma Green Wings vào cuối tháng 11. Thanh Thúy sẽ trở về nước hội quân cùng đội bóng chuyền Tây Ninh để sẵn sàng chinh phục tấm huy chương vàng danh giá tại Đại hội Thể thao toàn quốc lần thứ 10 tổ chức ở Thành phố Hồ Chí Minh.",
        "digest_line": "Chủ công Trần Thị Thanh Thúy sắp khép lại mùa giải tại Nhật Bản để về nước tranh tài tại Đại hội Thể thao toàn quốc lần thứ 10.",
        "digest_title": "Trần Thị Thanh Thúy chuẩn bị rời Nhật Bản về dự Đại hội toàn quốc",
        "total_images": 6,
        "hide_date_chip": False
    }
]

def main():
    print(f"=== KHỞI TẠO KỊCH BẢN 25 BẢN TIN TUẦN 09.11.2026 ===")
    
    # 1. Bổ sung đường dẫn ảnh và audio vào items
    for item in ITEMS:
        idx = item["id"]
        sc_num = f"{idx:02d}"
        item["audio_path"] = str(DAY_DIR / "audio" / f"audio_{sc_num}.wav")
        item["audio_title"] = str(DAY_DIR / "audio-title" / f"audio_title_{sc_num}.wav")
        item["image_path"] = str(DAY_DIR / "images" / f"Tin_{sc_num}_1.jpg")
        
        tot = item["total_images"]
        for i in range(1, tot + 1):
            item[f"image_{i}"] = str(DAY_DIR / "images" / f"Tin_{sc_num}_{i}.jpg")

    # 2. Ghi thethao.json
    json_path = DAY_DIR / "thethao.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(ITEMS, f, ensure_ascii=False, indent=2)
    print(f"[OK] Đã ghi thethao.json: {json_path} ({len(ITEMS)} items)")

    # 3. Ghi thethao.txt
    txt_path = DAY_DIR / "thethao.txt"
    lines = []
    total_words = 0
    for item in ITEMS:
        idx = item["id"]
        sc_num = f"{idx:02d}"
        words = len(item["summary"].split())
        total_words += words
        block = [
            f"[TIN {sc_num}] - {item['group']}",
            f"ID: {item['art_id']}",
            f"Tiêu đề: {item['title']}",
            f"Chi tiết: {item['summary']}",
            "---"
        ]
        lines.append("\n".join(block))
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(lines) + "\n")
    print(f"[OK] Đã ghi thethao.txt: {txt_path} (Tổng số từ: {total_words} từ)")

    # Kiểm tra quy tắc bất biến:
    # Không có dấu chấm phân cách hàng nghìn kiểu 2.026 hay 1.400
    import re
    has_err = False
    for item in ITEMS:
        text = item["summary"]
        m = re.findall(r"\b\d{1,3}\.\d{3}\b", text)
        if m:
            print(f"[CẢNH BÁO LỖI SỐ] Phát hiện số có dấu chấm hàng nghìn trong Tin {item['id']}: {m}")
            has_err = True
        
        # Tiêu đề quá dài
        if len(item["title"]) > 65:
            print(f"[CẢNH BÁO TIÊU ĐỀ DÀI] Tin {item['id']}: {len(item['title'])} ký tự: {item['title']}")
            has_err = True

    if not has_err:
        print("[CHECK PASS] 100% quy tắc bất biến về số viết liền mạch và tiêu đề đạt chuẩn!")

if __name__ == "__main__":
    main()
