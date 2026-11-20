#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng 2 Video Shorts 9:16 cho ngày 12.11.2026 tại outputs/Orther/12.11.2026/shorts/:
  - Tin #01 (Giọng Nam — Minh Quân Pro Mẫu 15): Đội tuyển Việt Nam thắng thuyết phục Đài Loan 2-0 (tập trung trận đấu)
  - Tin #02 (Giọng Nữ — Ngọc Huyền Mẫu 14): HLV Park Hang-seo nhận án phạt dù bị miệt thị ở Thái Lan

Dùng chung bộ pipeline chuẩn tại core/diemdoc/short_batch.py.
"""

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR / "core") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "core"))

from diemdoc import paths
from diemdoc.short_batch import ShortDayContext, run_short_batch

CTX = ShortDayContext(
    day_dir=Path(paths.ROOT) / "outputs" / "Orther" / "12.11.2026",
    inspect_dir=Path.home() / "Library" / "Caches" / "DiemDoc" / "inspect_12_11",
    work_tag="12_11",
)


NEWS_DATA_12_11: List[Dict[str, Any]] = [
    {
        "id": 1,
        "slug": "Short_Viet_Nam_Ha_Dai_Loan_2_0_Giao_Huu",
        "voice_preset": "primary",  # Giọng Nam: Minh Quân Pro (Mẫu 15)
        "group": "ĐỘI TUYỂN VIỆT NAM",
        "title": "Đội tuyển Việt Nam thắng thuyết phục Đài Loan 2-0 trên sân Thiên Trường",
        "summary": (
            "Tối ngày 11 tháng 11, đội tuyển Việt Nam đánh bại Đài Loan với tỷ số 2-0 trong trận giao hữu FIFA trên sân vận động Thiên Trường. "
            "HLV Kim Sang-sik gây bất ngờ khi trao cơ hội đá chính cho năm tân binh gồm Nguyễn Hồng Phúc, Phạm Minh Phúc, Quốc Cường, Trần Ngọc Sơn và Olaha Mạnh Đức. "
            "Sau hai mươi phút thăm dò, Việt Nam khai thông bế tắc từ pha phối hợp sắc nét bên cánh phải để Olaha Mạnh Đức đệm bóng cận thành mở tỷ số. "
            "Sang hiệp hai, thầy trò HLV Kim Sang-sik tiếp tục làm chủ thế trận trước khi Khuất Văn Khang chọc khe giúp Nguyễn Đình Bắc lập công ở phút 58. "
            "HLV Matthew Ross của Đài Loan thừa nhận tỷ số 2-0 chưa phản ánh hết sự áp đảo từ lối chơi kỷ luật và luân chuyển linh hoạt bên phía chủ nhà. "
            "Chiến thắng giàu năng lượng trẻ này giúp đoàn quân áo đỏ có bước chạy đà hoàn hảo trước khi chạm trán Kyrgyzstan vào ngày 17 tháng 11."
        ),
        "source": "VnExpress",
        "news_source": "VnExpress",
        "credit": "VNEXPRESS / HIẾU LƯƠNG",
        "hide_date_chip": True,
        "seo_title": "Đội tuyển Việt Nam thắng thuyết phục Đài Loan 2-0 trên sân Thiên Trường #Shorts",
        "description": [
            "Đội tuyển Việt Nam giành chiến thắng thuyết phục 2-0 trước Đài Loan trong trận giao hữu FIFA tối 11/11 trên sân Thiên Trường (Ninh Bình) dưới sự dẫn dắt của HLV Kim Sang-sik.",
            "Năm gương mặt lần đầu đá chính gồm Nguyễn Hồng Phúc, Phạm Minh Phúc, Nguyễn Thái Quốc Cường, Trần Ngọc Sơn và Olaha Mạnh Đức chơi đầy tự tin. Olaha mở tỷ số sau đường kiến tạo của Hồng Phúc, trước khi Nguyễn Đình Bắc ấn định thắng lợi 2-0 ở phút 58 từ pha chọc khe của Khuất Văn Khang.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#DoiTuyenVietNam", "#VietNamDaiLoan", "#KimSangSik",
            "#NguyenDinhBac", "#OlahaManhDuc", "#SanThienTruong", "#BongDaVietNam",
        ],
        "thumb": {
            "image": "Tin_01_8.jpg",
            "badge": "ĐỘI TUYỂN VIỆT NAM",
            "kicker": "GIAO HỮU CASPER CUP 2026",
            "hero_html": 'VIỆT NAM HẠ ĐÀI LOAN <span class="hl">2-0</span> THUYẾT PHỤC',
            "subtitle": "Olaha Mạnh Đức và Đình Bắc lập công, 5 tân binh ghi dấu ấn rực rỡ trên sân Thiên Trường",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "12.11.2026",
            "obj_pos": "center 15%",
        },
        "images": [
            # Title (2 ảnh đầu)
            {"dest": "Tin_01_1.jpg", "src": "vn_dl_tongthuat_2.jpg", "credit": "VNEXPRESS", "desc": "Trần Ngọc Sơn, Olaha Mạnh Đức và Đình Bắc trên sân Thiên Trường"},
            {"dest": "Tin_01_2.jpg", "src": "vne1_off_1.jpg", "credit": "VNEXPRESS", "desc": "Đội tuyển Việt Nam hát Quốc ca trước trận gặp Đài Loan"},
            # Câu 1: Trận giao hữu VN 2-0 Đài Loan trên sân Thiên Trường
            {"dest": "Tin_01_3.jpg", "src": "vn_dl_tongthuat_3.jpg", "credit": "VNEXPRESS", "desc": "Diễn biến trận giao hữu Việt Nam vs Đài Loan tại Casper Cup 2026"},
            {"dest": "Tin_01_4.jpg", "src": "vne1_off_2.jpg", "credit": "VNEXPRESS", "desc": "Hàng công Việt Nam tổ chức lên bóng gây sức ép lên Đài Loan"},
            # Câu 2: HLV Kim Sang-sik trao cơ hội cho 5 tân binh
            {"dest": "Tin_01_5.jpg", "src": "vn_dl_extra_2.jpg", "credit": "VNEXPRESS", "desc": "HLV Kim Sang-sik theo dõi và chỉ đạo học trò ngoài khu kỹ thuật"},
            {"dest": "Tin_01_6.jpg", "src": "vne1_off_8.jpg", "credit": "VNEXPRESS", "desc": "Tân binh Trần Ngọc Sơn thi đấu năng nổ trong lần đầu lên tuyển"},
            # Câu 3: Bàn mở tỷ số của Olaha từ pha phối hợp cánh phải
            {"dest": "Tin_01_7.jpg", "src": "vne1_off_3.jpg", "credit": "VNEXPRESS", "desc": "Pha dứt điểm cận thành mở tỷ số 1-0 cho đội tuyển Việt Nam"},
            {"dest": "Tin_01_8.jpg", "src": "vne1_off_4.jpg", "credit": "VNEXPRESS", "desc": "Niềm vui ăn mừng bàn thắng của các tuyển thủ Việt Nam"},
            # Câu 4: Hiệp 2 Văn Khang kiến tạo, Đình Bắc ghi bàn phút 58
            {"dest": "Tin_01_9.jpg", "src": "vne1_off_9.jpg", "credit": "VNEXPRESS", "desc": "Nguyễn Đình Bắc đi bóng tốc độ bên hành lang cánh"},
            {"dest": "Tin_01_10.jpg", "src": "vne1_off_10.jpg", "credit": "VNEXPRESS", "desc": "Nguyễn Đình Bắc ăn mừng bàn thắng ấn định tỷ số 2-0"},
            # Câu 5: HLV Matthew Ross thừa nhận sự áp đảo của Việt Nam
            {"dest": "Tin_01_11.jpg", "src": "vn_dl_extra_1.jpg", "credit": "VNEXPRESS", "desc": "HLV Matthew Ross của Đài Loan chỉ đạo ngoài đường biên"},
            {"dest": "Tin_01_12.jpg", "src": "vn_dl_tongthuat_1.jpg", "credit": "VNEXPRESS", "desc": "Tuyển Việt Nam dồn ép đội khách bằng lối chơi kỷ luật"},
            # Câu 6: Chạy đà trước trận gặp Kyrgyzstan ngày 17/11
            {"dest": "Tin_01_13.jpg", "src": "vne1_off_5.jpg", "credit": "VNEXPRESS", "desc": "Các cầu thủ áo đỏ tranh chấp quyết liệt giành lại bóng"},
            {"dest": "Tin_01_14.jpg", "src": "vne1_off_6.jpg", "credit": "VNEXPRESS", "desc": "Ban huấn luyện bắt tay cầu thủ khép lại chiến thắng 2-0"},
        ],
        "plan_slots": [
            ("title", 0, "Tin_01_1.jpg"),
            ("title", 0, "Tin_01_2.jpg"),
            ("sentence", 1, "Tin_01_3.jpg"),
            ("sentence", 1, "Tin_01_4.jpg"),
            ("sentence", 2, "Tin_01_5.jpg"),
            ("sentence", 2, "Tin_01_6.jpg"),
            ("sentence", 3, "Tin_01_7.jpg"),
            ("sentence", 3, "Tin_01_8.jpg"),
            ("sentence", 4, "Tin_01_9.jpg"),
            ("sentence", 4, "Tin_01_10.jpg"),
            ("sentence", 5, "Tin_01_11.jpg"),
            ("sentence", 5, "Tin_01_12.jpg"),
            ("sentence", 6, "Tin_01_13.jpg"),
            ("sentence", 6, "Tin_01_14.jpg"),
        ],
    },
    {
        "id": 2,
        "slug": "Short_HLV_Park_Hang_Seo_Nhan_An_Phat_Tai_Thai_Lan",
        "voice_preset": "secondary",  # Giọng Nữ: Ngọc Huyền (Mẫu 14) theo yêu cầu
        "group": "BÓNG ĐÁ ĐÔNG NAM Á",
        "title": "HLV Park Hang-seo nhận án phạt dù bị miệt thị ở Thái Lan",
        "summary": (
            "Ngày 11 tháng 11, Ban kỷ luật Liên đoàn Bóng đá Thái Lan bất ngờ ra án cấm chỉ đạo hai trận và phạt 13333 baht, khoảng 10 triệu đồng, đối với HLV Park Hang-seo. "
            "Biến cố nổ ra cuối trận Kanchanaburi FC hòa chủ nhà Pattaya United 2-2 tại Thai League 2, khi nhóm khán giả quá khích buông lời miệt thị chủng tộc nhắm vào ông Park và tiền đạo John Baggio. "
            "Do phản ứng gay gắt và bước vào khu vực không được phép để bảo vệ học trò khỏi lời thóa mạ Kimchi Man, nhà cầm quân Hàn Quốc vẫn bị quy lỗi làm gia tăng xung đột. "
            "Ở chiều ngược lại, đội chủ nhà Pattaya United phải chịu mức phạt 40000 baht sau khi video hiện trường xác nhận hành vi xúc phạm từ khán đài. "
            "Chiến lược gia người Hàn Quốc khẳng định bản thân không bận tâm công kích cá nhân, nhưng không thể im lặng khi học trò bị lăng mạ thô tục. "
            "Dù vắng mặt trên băng ghế chỉ đạo hai vòng tới, HLV Park vừa cùng Kanchanaburi đánh bại Nakhon Ratchasima 1-0 và vươn lên hạng tư."
        ),
        "source": "VnExpress / FAT",
        "news_source": "VnExpress / FAT",
        "credit": "VNEXPRESS / KANCHANABURI FC",
        "hide_date_chip": True,
        "seo_title": "HLV Park Hang-seo nhận án phạt dù bị miệt thị ở Thái Lan #Shorts",
        "description": [
            "Ban kỷ luật và đạo đức Liên đoàn Bóng đá Thái Lan (FAT) quyết định cấm chỉ đạo 2 trận và phạt 13.333 baht (khoảng 10 triệu đồng) đối với HLV Park Hang-seo sau sự cố ở vòng 9 Thai League 2.",
            "Dù ông Park và tiền đạo John Baggio bị CĐV Pattaya United buông lời miệt thị chủng tộc (khiến chủ nhà bị phạt 40.000 baht), FAT vẫn xử phạt vì phản ứng nóng nảy của nhà cầm quân người Hàn Quốc. HLV Park khẳng định không thể làm ngơ khi học trò bị xúc phạm.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#ParkHangSeo", "#ThaiLeague2", "#KanchanaburiFC",
            "#PattayaUnited", "#BongDaThaiLan", "#JohnBaggio", "#TinBongDa",
        ],
        "thumb": {
            "image": "Tin_02_1.jpg",
            "badge": "THAI LEAGUE 2",
            "kicker": "LĐBĐ THÁI LAN PHẠT NGUỘI",
            "hero_html": 'HLV PARK HANG-SEO BỊ PHẠT<br><span class="hl">DÙ BỊ MIỆT THỊ</span>',
            "subtitle": "Cấm chỉ đạo 2 trận sau vụ CĐV Pattaya United lăng mạ vì đứng ra bảo vệ học trò ở Thái Lan",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "12.11.2026",
            "obj_pos": "center 18%",
        },
        "images": [
            # Title (2 ảnh đầu)
            {"dest": "Tin_02_1.jpg", "src": "vne_2_1.jpg", "credit": "FACEBOOK / BERNY ZIMMER", "desc": "HLV Park Hang-seo ra hiệu im lặng trước CĐV trên sân Nong Prue"},
            {"dest": "Tin_02_2.jpg", "src": "candidates/p_kan_coach_1.jpg", "credit": "KANCHANABURI POWER FC", "desc": "HLV Park Hang-seo ra mắt dẫn dắt Kanchanaburi Power FC"},
            # Câu 1: FAT cấm chỉ đạo 2 trận và phạt 13333 baht
            {"dest": "Tin_02_3.jpg", "src": "candidates/p_fat_thai_2.jpg", "credit": "FA THAILAND", "desc": "Họp báo tại Liên đoàn Bóng đá Thái Lan FAT"},
            {"dest": "Tin_02_4.jpg", "src": "candidates/p_fat_hq_2.jpg", "credit": "DER FARANG", "desc": "Trụ sở Liên đoàn Bóng đá Thái Lan tại Bangkok"},
            # Câu 2: Kanchanaburi hòa Pattaya United 2-2, miệt thị Park & John Baggio
            {"dest": "Tin_02_5.jpg", "src": "candidates/p_park_kan_3.jpg", "credit": "ZNEWS", "desc": "CLB Kanchanaburi FC thi đấu tại giải quốc nội Thái Lan"},
            {"dest": "Tin_02_6.jpg", "src": "candidates/p_baggio2_1.jpg", "credit": "BANGKOK POST", "desc": "Tiền đạo John Baggio thi đấu trên sân cỏ Thái Lan"},
            # Câu 3: Phản ứng gay gắt bảo vệ học trò khỏi lời thóa mạ Kimchi Man
            {"dest": "Tin_02_7.jpg", "src": "candidates/p_kan_coach_2.jpg", "credit": "THANH NIÊN", "desc": "HLV Park Hang-seo phản ứng gay gắt bên đường biên"},
            {"dest": "Tin_02_8.jpg", "src": "candidates/p_kan_fc_2.jpg", "credit": "KANCHANABURI POWER FC", "desc": "Các cầu thủ Kanchanaburi tranh chấp quyết liệt trên sân"},
            # Câu 4: Pattaya United bị phạt 40000 baht sau bằng chứng video khán đài
            {"dest": "Tin_02_9.jpg", "src": "candidates/p_pattaya_1.jpg", "credit": "DER FARANG", "desc": "Khán đài sân vận động Nong Prue của CLB Pattaya United"},
            {"dest": "Tin_02_10.jpg", "src": "candidates/p_fat_thai_1.jpg", "credit": "ASEAN FOOTBALL", "desc": "Đại diện LĐBĐ Thái Lan FAT trong cuộc họp điều hành"},
            # Câu 5: Không bận tâm công kích cá nhân nhưng bảo vệ cầu thủ
            {"dest": "Tin_02_11.jpg", "src": "candidates/p_park_vn_2.jpg", "credit": "BÁO AN GIANG", "desc": "Chân dung HLV Park Hang-seo giàu cảm xúc bên đường pitch"},
            {"dest": "Tin_02_12.jpg", "src": "candidates/p_kan_fc_3.jpg", "credit": "KANCHANABURI POWER FC", "desc": "Biểu trưng chính thức của CLB Kanchanaburi Power FC"},
            # Câu 6: Thắng Nakhon Ratchasima 1-0, vươn lên hạng tư
            {"dest": "Tin_02_13.jpg", "src": "vne_2_2.jpg", "credit": "KANCHANABURI FC", "desc": "CĐV Kanchanaburi vẽ tranh ủng hộ HLV Park Hang-seo trận thắng 1-0"},
            {"dest": "Tin_02_14.jpg", "src": "candidates/p_kan_fc_1.jpg", "credit": "KANCHANABURI FC", "desc": "Toàn cảnh sân vận động tỉnh Kanchanaburi, Thái Lan"},
        ],
        "plan_slots": [
            ("title", 0, "Tin_02_1.jpg"),
            ("title", 0, "Tin_02_2.jpg"),
            ("sentence", 1, "Tin_02_3.jpg"),
            ("sentence", 1, "Tin_02_4.jpg"),
            ("sentence", 2, "Tin_02_5.jpg"),
            ("sentence", 2, "Tin_02_6.jpg"),
            ("sentence", 3, "Tin_02_7.jpg"),
            ("sentence", 3, "Tin_02_8.jpg"),
            ("sentence", 4, "Tin_02_9.jpg"),
            ("sentence", 4, "Tin_02_10.jpg"),
            ("sentence", 5, "Tin_02_11.jpg"),
            ("sentence", 5, "Tin_02_12.jpg"),
            ("sentence", 6, "Tin_02_13.jpg"),
            ("sentence", 6, "Tin_02_14.jpg"),
        ],
    },
]


def main() -> None:
    run_short_batch(
        ctx=CTX,
        items=NEWS_DATA_12_11,
        title_banner="SẢN XUẤT 2 VIDEO SHORTS NGÀY 12.11.2026 (VIỆT NAM 2-0 ĐÀI LOAN & HLV PARK HANG-SEO)",
    )


if __name__ == "__main__":
    main()
