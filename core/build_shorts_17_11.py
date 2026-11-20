#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_shorts_17_11.py — Dựng trọn gói 3 Video Shorts Tin Tổng Hợp (17.11.2026)
=============================================================================
- Quy chuẩn:
  + Video 1 (Quốc tế 1): Giọng Nam Minh Quân Pro (Mẫu #15 - primary)
  + Video 2 (Quốc tế 2): Giọng Nam Minh Quân Pro (Mẫu #15 - primary)
  + Video 3 (Việt Nam): Giọng Nữ Ngọc Huyền (Mẫu #14 - secondary)
- Dạng kịch bản: Viết liền tổng thể (~510 - 550 từ, thời lượng thực tế ~2m15s - 2m35s dưới 3 phút bao gồm outro).
- Đồng bộ chuyển động thị giác: 82 ảnh tư liệu sạch, phân bổ chronologically theo từng phân đoạn câu.
- Engine: HTML v2 deterministic (Playwright Virtual Clock + GSAP), template short_news_v2.html.
- Tự động gắn Outro 9:16 kênh Điểm Đọc (5s).
- Render Thumbnail 9:16 chuẩn Cyber-Stadium và xuất mô tả SEO YouTube mota.txt.
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import os
import json
import argparse
from pathlib import Path
from typing import Any, Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR / "core") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "core"))

from diemdoc import paths
from diemdoc.short_batch import ShortDayContext, run_short_batch

DAY_DIR = ROOT_DIR / "outputs" / "Orther" / "17.11.2026"
CTX = ShortDayContext(
    day_dir=DAY_DIR,
    inspect_dir=DAY_DIR / "images",
    work_tag="17_11",
)

COLOR_CYAN = "#00E5FF"
COLOR_GOLD = "#F59E0B"
COLOR_ROSE = "#EF4444"


def _make_item(
    item_id: int,
    slug: str,
    voice_preset: str,
    group: str,
    title: str,
    summary_text: str,
    source: str,
    news_source: str,
    credit: str,
    seo_title: str,
    description: List[str],
    hashtags: List[str],
    hook: Dict[str, Any],
    thumb: Dict[str, Any],
    images: List[Dict[str, str]],
    plan_slots: List[tuple],
) -> Dict[str, Any]:
    return {
        "id": item_id,
        "slug": slug,
        "voice_preset": voice_preset,
        "group": group,
        "title": title,
        "summary": summary_text,
        "source": source,
        "news_source": news_source,
        "credit": credit,
        "hide_date_chip": True,
        "seo_title": seo_title,
        "description": description,
        "hashtags": hashtags,
        "hook": hook,
        "thumb": thumb,
        "images": images,
        "plan_slots": plan_slots,
    }


# =====================================================================
# DỮ LIỆU 3 BẢN TIN TỔNG HỢP (17.11.2026)
# =====================================================================

# ----------------- VIDEO 1: QUỐC TẾ 1 (GIỌNG NAM) -----------------
V1_SUMMARY = (
    "Đêm qua theo giờ Việt Nam, bóng đá châu Âu đã trải qua những giờ phút rung chuyển dữ dội với hàng loạt biến động lớn từ sân cỏ Nations League cho đến những tranh cãi nảy lửa chốn hậu trường. "
    "Tâm điểm của cơn địa chấn diễn ra tại sân vận động Olympiastadion ở thủ đô Berlin, nơi đội tuyển Đức đã khiến cả thế giới ngỡ ngàng khi đè bẹp đại kình địch Hà Lan với tỷ số không tưởng 5-0. "
    "Khoác lên mình bộ trang phục đen kỷ niệm đặc biệt, Cỗ xe tăng Đức đã dội một cơn mưa gôn thực sự vào lưới đối thủ. "
    "Tiền vệ trẻ Florian Wirtz rực sáng với một cú đúp đẳng cấp, bên cạnh các pha lập công của Derry Scherhant, Nico Schlotterbeck và Brajan Gruda, qua đó giúp Đức hiên ngang tiến vào tứ kết Nations League với ngôi đầu bảng A2. "
    "Trái ngược với niềm hân hoan của người Đức, đây lại là thất bại cay đắng và nặng nề nhất của bóng đá Hà Lan trong suốt 67 năm qua, kể từ năm 1959. "
    "Ngay sau trận đấu, tân HLV Xavi Hernandez đã không giấu nổi sự bàng hoàng và thừa nhận cảm thấy sốc cùng nỗi hổ thẹn lớn trước tinh thần thi đấu rệu rã của các học trò, dù Hà Lan vẫn may mắn lách qua khe cửa hẹp để giành vé nhì bảng. "
    "Nhưng sóng gió bóng đá lục địa già không chỉ dừng lại ở Berlin. "
    "Tại bán đảo Iberia, một cuộc khủng hoảng truyền thông đang bùng nổ dữ dội xung quanh siêu sao Cristiano Ronaldo sau thất bại bất ngờ của đội tuyển Bồ Đào Nha trước Đan Mạch. "
    "Mới đây nhất, bà Dolores Aveiro, mẹ của Ronaldo, đã khiến dư luận quốc tế dậy sóng khi công khai tuyên bố trên truyền thông rằng việc đội tuyển Bồ Đào Nha thất bại là đáng đời vì đã thiếu đi sự tôn trọng tối thiểu dành cho con trai bà. "
    "Phát biểu gây chấn động này lập tức thổi bùng lên những mâu thuẫn âm ỉ trong phòng thay đồ của Selecao châu Âu. "
    "Các chuyên gia tiếp thị thể thao quốc tế cũng nhanh chóng lên tiếng cảnh báo, việc gạt bỏ huyền thoại 41 tuổi không chỉ gây rạn nứt nội bộ, mà còn khiến bóng đá Bồ Đào Nha đối mặt nguy cơ sụt giảm nghiêm trọng hàng triệu người theo dõi toàn cầu cùng những tổn thất khổng lồ về giá trị thương mại. "
    "Rõ ràng, dù đang sở hữu một thế hệ kế cận đầy tài năng, chiếc bóng và sức hút mang tầm vóc biểu tượng của Cristiano Ronaldo vẫn là thứ mà người Bồ Đào Nha chưa thể tìm ra lời giải thay thế."
)

# ----------------- VIDEO 2: QUỐC TẾ 2 (GIỌNG NAM) -----------------
V2_SUMMARY = (
    "Bên cạnh những cơn sốt trên sân cỏ Nations League, bức tranh thể thao thế giới trong 12 giờ qua tiếp tục chứng kiến sự áp đảo của các siêu sao thế hệ mới cùng những câu chuyện hậu trường tài chính vô cùng đặc biệt. "
    "Tại thành phố Turin nước Ý, giải quần vợt danh giá dành cho 8 tay vợt mạnh nhất năm Nitto ATP Finals 2026 đã chính thức khai màn với màn thị uy sức mạnh không thể thuyết phục hơn của Carlos Alcaraz. "
    "Trong trận ra quân tại bảng Ivan Lendl, tay vợt số 1 Tây Ban Nha chỉ cần vỏn vẹn 69 phút để nghiền nát đối thủ người Mỹ Frances Tiafoe với tỷ số trắng 6-2, 6-2. "
    "Thi đấu với phong độ như đang dạo chơi nhưng tung ra tới 21 điểm winner chuẩn xác, Alcaraz đã nối dài chuỗi 10 trận toàn thắng liên tiếp, gửi lời thách thức đanh thép tới toàn bộ các đối thủ trên hành trình chinh phục chiếc cúp danh giá cuối năm. "
    "Cũng liên quan đến thể thao Tây Ban Nha nhưng ở khía cạnh pháp lý, ban tổ chức giải bóng đá La Liga vừa chính thức phát đi thông báo minh oan cho hiện tượng trẻ Lamine Yamal. "
    "Cơ quan này khẳng định toàn bộ hình ảnh và bài viết lan truyền trên mạng xã hội cáo buộc thần đồng của Barcelona có hành vi kỳ thị người Trung Quốc là sản phẩm cắt ghép giả mạo hoàn toàn. "
    "La Liga tuyên bố đã khởi động các thủ tục pháp lý để xử lý nghiêm những tài khoản cố tình tung tin thất thiệt nhằm bôi nhọ danh dự của ngôi sao 19 tuổi. "
    "Trong khi đó, tại đại bản doanh xứ Catalonia, ban lãnh đạo Barcelona lại đang khiến giới tài chính kinh ngạc với một kế hoạch kinh doanh chưa từng có tiền lệ mang tên Memorial FC Barcelona. "
    "Theo tính toán từ nhật báo El Plural, đội chủ sân Camp Nou dự kiến sẽ cho thuê 26000 ô lưu giữ tro cốt ngay trong khuôn viên sân vận động mới với gói thời hạn 10 năm. "
    "Nếu được lấp đầy, dự án độc lạ này sẽ mang về cho Barca khoản doanh thu khổng lồ lên tới hơn 71 triệu USD, trở thành chiếc phao cứu sinh quan trọng giúp gã khổng lồ La Liga giải quyết bài toán khó khăn tài chính đã đeo bám họ suốt nhiều năm qua."
)

# ----------------- VIDEO 3: VIỆT NAM (GIỌNG NỮ) -----------------
V3_SUMMARY = (
    "Không khí thể thao trong nước ngày hôm nay đang trở nên vô cùng sôi động khi người hâm mộ cả nước dồn trọn sự chú ý về sân vận động quốc gia Mỹ Đình, nơi đội tuyển Việt Nam sẽ bước vào trận đấu chính thức khép lại năm 2026. "
    "Đúng 19h00 tối nay ngày 17 tháng 11, các chiến binh sao vàng sẽ bước vào màn so tài được chờ đợi với đội tuyển Kyrgyzstan. "
    "Đây là đợt sát hạch vô cùng quan trọng của HLV Kim Sang-sik trước khi đội tuyển bước vào quãng nghỉ kéo dài tới 9 tháng. "
    "Sau khi chân sút nhập tịch Olaha Mạnh Đức được cho phép trở về câu lạc bộ Công an TP.HCM để chuẩn bị cho cúp Đông Nam Á, ban huấn luyện đội tuyển đang tích cực tìm lời giải cho bài toán hàng công. "
    "HLV Kim Sang-sik đã lên kế hoạch thử nghiệm dàn tiền đạo có thể hình lý tưởng trên 1,82 m gồm Tiến Linh, Đinh Thanh Bình và Bùi Vĩ Hào, nhằm tạo nên sức ép trực diện trước hàng phòng ngự kỷ luật và thể lực dồi dào của đại diện Trung Á xếp hạng 102 FIFA. "
    "Ngay trước giờ bóng lăn, đội tuyển Việt Nam cũng đã đón nhận một món quà bất ngờ khi chính thức được cộng điểm để nhích thêm một bậc trên bảng xếp hạng thế giới, nhờ vào thất bại của đối thủ cạnh tranh Mozambique tại vòng loại cúp châu Phi. "
    "Không chỉ ở cấp độ đội tuyển quốc gia, bóng đá trẻ Việt Nam cũng đang lan tỏa nguồn năng lượng vô cùng tích cực. "
    "Tại Doha, đội tuyển U17 Việt Nam đã hoàn tất buổi tập đầu tiên trên cụm sân Al-Gharafa, tự tin bước vào giai đoạn chuẩn bị then chốt cho Vòng chung kết U17 World Cup 2026. "
    "Thành quả đào tạo bài bản của bóng đá trẻ Việt Nam với hạt nhân Chu Ngọc Nguyễn Lực được FIFA vinh danh thậm chí còn khiến truyền thông Indonesia phải chạnh lòng thán phục về định hướng nội lực vững chắc của chúng ta. "
    "Cùng thời điểm này, không khí Đại hội Thể thao toàn quốc 2026 cũng đang rực lửa tại các sàn đấu phía Nam. "
    "Đội tuyển Judo TP.HCM đã đón tấm Huy chương Vàng mở hàng đầy cảm xúc của võ sĩ Phan Ngọc Dũng, trong khi cựu binh Vũ Thị Trang thi đấu thăng hoa giúp cầu lông thành phố sớm cầm chắc tấm huy chương danh giá. "
    "Tất cả đang tạo nên một ngày thi đấu đầy khí thế và hy vọng cho thể thao nước nhà."
)


def _load_images_for_video(video_id: int) -> Tuple[List[Dict[str, str]], List[tuple]]:
    """Đọc image_plan.json để nạp danh sách images và plan_slots chính xác 100%."""
    plan_path = DAY_DIR / "image_plan.json"
    with open(plan_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    records = [r for r in data.get("records", []) if r["scene_id"] == video_id]

    images = []
    plan_slots = []
    seen = set()
    for r in records:
        fname = r["file_name"]
        slot_type = r["type"]
        s_idx = r["sentence_idx"]
        plan_slots.append((slot_type, s_idx, fname))
        if fname not in seen:
            seen.add(fname)
            images.append({
                "dest": fname,
                "abs_src": str(DAY_DIR / "images" / fname),
                "credit": r["credit"],
                "desc": r["description"],
            })
    return images, plan_slots


v1_imgs, v1_slots = _load_images_for_video(1)
v2_imgs, v2_slots = _load_images_for_video(2)
v3_imgs, v3_slots = _load_images_for_video(3)


NEWS_DATA_17_11: List[Dict[str, Any]] = [
    _make_item(
        item_id=1,
        slug="Short_Tong_Hop_QT1_Dia_Chan_Duc_Ha_Lan_Va_Song_Gio_Ronaldo",
        voice_preset="primary",  # Giọng Nam Minh Quân Pro
        group="BẢN TIN QUỐC TẾ • ĐỊA CHẤN BERLIN & SÓNG GIÓ RONALDO",
        title="Bão lớn bóng đá châu Âu: Đức hủy diệt Hà Lan 5-0 và sóng gió quanh Ronaldo",
        summary_text=V1_SUMMARY,
        source="UEFA & Bild, The Guardian",
        news_source="UEFA / BÁO CHÍ CHÂU ÂU",
        credit="REUTERS / GETTY IMAGES / UEFA",
        seo_title="Bão lớn bóng đá châu Âu: Đức hủy diệt Hà Lan 5-0 và sóng gió quanh Ronaldo #Shorts",
        description=[
            "Cơn địa chấn làm rung chuyển bóng đá châu Âu đêm qua: Đội tuyển Đức vùi dập đại kình địch Hà Lan 5-0 tại Berlin, khiến tân HLV Xavi Hernandez bàng hoàng thừa nhận hổ thẹn sau thất bại nặng nề nhất của bóng đá Hà Lan sau 67 năm.",
            "Trong khi đó, sóng gió bùng nổ quanh siêu sao Cristiano Ronaldo sau thất bại của Bồ Đào Nha: Mẹ CR7 (bà Dolores Aveiro) tuyên bố đội nhà thua là đáng đời, các chuyên gia cảnh báo nguy cơ sụt giảm triệu người xem toàn cầu.",
        ],
        hashtags=["#Shorts", "#DiemDoc", "#BongDa", "#NationsLeague", "#Ronaldo"],
        hook={
            "kicker": "UEFA NATIONS LEAGUE • BERLIN 16/11",
            "vs_badge": "ĐỨC vs HÀ LAN",
            "stat_val": 5,
            "stat_unit": "- 0",
            "stat_label": "CƠN ĐỊA CHẤN TẠI BERLIN",
            "stat_sub": "ĐỨC VÙI DẬP HÀ LAN 5-0 • SÓNG GIÓ QUANH RONALDO",
            "opp_val": 0,
            "count_dur": 0.65,
            "pills": [
                {"text": "ĐỨC 5-0 HÀ LAN", "style": "cyan", "delay": 1.15},
                {"text": "XAVI THỪA NHẬN HỔ THẸN", "style": "gold", "delay": 1.85},
                {"text": "MẸ RONALDO LÊN TIẾNG", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        thumb={
            "image": "v1_germany_celebrate.jpg",
            "badge": "ĐỨC vs HÀ LAN • 5-0",
            "kicker": "NATIONS LEAGUE • ĐỊA CHẤN BERLIN",
            "hero_html": 'ĐỨC HỦY DIỆT <span class="hl">HÀ LAN 5-0</span>',
            "subtitle": "Cơn địa chấn lịch sử tại Berlin; sóng gió phòng thay đồ Cristiano Ronaldo",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "17.11.2026",
            "obj_pos": "center 20%",
        },
        images=v1_imgs,
        plan_slots=v1_slots,
    ),
    _make_item(
        item_id=2,
        slug="Short_Tong_Hop_QT2_Suc_Manh_Alcaraz_Minh_Oan_Yamal_Barca",
        voice_preset="primary",  # Giọng Nam Minh Quân Pro
        group="BẢN TIN QUỐC TẾ • ALCARAZ HỦY DIỆT & ĐÒN BẨY BARCA",
        title="Alcaraz thị uy tại ATP Finals, La Liga minh oan cho Yamal và nước cờ của Barca",
        summary_text=V2_SUMMARY,
        source="ATP Tour, CCTV Sports, El Plural",
        news_source="ATP TOUR / LA LIGA / EL PLURAL",
        credit="GETTY IMAGES / REUTERS / FC BARCELONA",
        seo_title="Alcaraz thị uy tại ATP Finals, La Liga minh oan cho Yamal và nước cờ của Barca #Shorts",
        description=[
            "Carlos Alcaraz ra quân thần tốc tại Nitto ATP Finals 2026: Đè bẹp Frances Tiafoe 6-2, 6-2 chỉ sau 69 phút với 21 điểm winner, nối dài chuỗi 10 trận toàn thắng.",
            "La Liga chính thức phát đi thông báo minh oan cho Lamine Yamal sau tin đồn cắt ghép kỳ thị; Barcelona gây sốc với dự án lưu tro cốt Camp Nou dự kiến thu về hơn 71 triệu USD.",
        ],
        hashtags=["#Shorts", "#DiemDoc", "#Tennis", "#Alcaraz", "#Barcelona", "#Yamal"],
        hook={
            "kicker": "NITTO ATP FINALS • TURIN 2026",
            "vs_badge": "ALCARAZ vs TIAFOE",
            "stat_val": 6,
            "stat_unit": "- 2, 6 - 2",
            "stat_label": "THỊ UY SỨC MẠNH VŨ BÃO",
            "stat_sub": "ALCARAZ HỦY DIỆT TIAFOE • MINH OAN CHO LAMINE YAMAL",
            "opp_val": 2,
            "count_dur": 0.65,
            "pills": [
                {"text": "ALCARAZ THẮNG 69 PHÚT", "style": "cyan", "delay": 1.15},
                {"text": "LA LIGA MINH OAN YAMAL", "style": "gold", "delay": 1.85},
                {"text": "BARCA THU 71 TRIỆU USD", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        thumb={
            "image": "v2_alcaraz_celebrate_fist.jpg",
            "badge": "ATP FINALS • ALCARAZ",
            "kicker": "TURIN 2026 • ĐẲNG CẤP VŨ BÃO",
            "hero_html": 'ALCARAZ THỊ UY <span class="hl">TẠI ATP FINALS</span>',
            "subtitle": "Hạ Tiafoe sau 69 phút; La Liga minh oan cho Yamal và nước cờ 71 triệu USD của Barca",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "17.11.2026",
            "obj_pos": "center 20%",
        },
        images=v2_imgs,
        plan_slots=v2_slots,
    ),
    _make_item(
        item_id=3,
        slug="Short_Tong_Hop_VN_Tam_Diem_My_Dinh_Va_Diem_Sang_The_Thao_Nuoc_Nha",
        voice_preset="secondary",  # Giọng Nữ Ngọc Huyền
        group="BẢN TIN VIỆT NAM • TÂM ĐIỂM MỸ ĐÌNH & ĐIỂM SÁNG NƯỚC NHÀ",
        title="ĐT Việt Nam quyết đấu Kyrgyzstan, tin vui FIFA và điểm sáng thể thao nước nhà",
        summary_text=V3_SUMMARY,
        source="VFF, Dân Trí, Thanh Niên, Tuổi Trẻ",
        news_source="DÂN TRÍ / BÁO THANH NIÊN / TUỔI TRẺ",
        credit="VFF / BÁO THANH NIÊN / BÁO TUỔI TRẺ",
        seo_title="ĐT Việt Nam quyết đấu Kyrgyzstan, tin vui FIFA và điểm sáng thể thao nước nhà #Shorts",
        description=[
            "Tâm điểm 19h00 hôm nay trên sân Mỹ Đình: ĐT Việt Nam chạm trán Kyrgyzstan trong trận cầu khép lại năm 2026. HLV Kim Sang-sik thử nghiệm bộ ba tiền đạo cao trên 1,82 m (Tiến Linh, Đinh Thanh Bình, Bùi Vĩ Hào).",
            "Tin vui tiếp sức: Tuyển Việt Nam bất ngờ tăng hạng FIFA; U17 Việt Nam hoàn tất buổi tập đầu tiên tại Qatar cho U17 World Cup 2026; võ sĩ Phan Ngọc Dũng mở hàng HCV Judo cho TP.HCM tại Đại hội Thể thao toàn quốc.",
        ],
        hashtags=["#Shorts", "#DiemDoc", "#BongDaVietNam", "#MyDinh", "#KimSangSik"],
        hook={
            "kicker": "GIAO HỮU QUỐC TẾ • MỸ ĐÌNH 17/11",
            "vs_badge": "VIỆT NAM vs KYRGYZSTAN",
            "stat_val": 19,
            "stat_unit": "h00",
            "stat_label": "TÂM ĐIỂM SÂN MỸ ĐÌNH",
            "stat_sub": "THẦY TRÒ KIM SANG-SIK XUẤT TRẬN • TIN VUI THĂNG HẠNG FIFA",
            "opp_val": 0,
            "count_dur": 0.65,
            "pills": [
                {"text": "19H00 HÔM NAY", "style": "cyan", "delay": 1.15},
                {"text": "HÀNG TIỀN ĐẠO 1M82", "style": "gold", "delay": 1.85},
                {"text": "ĐỘI TUYỂN TĂNG HẠNG FIFA", "style": "", "delay": 2.50},
            ],
            "fast_cut": True,
        },
        thumb={
            "image": "v3_vietnam_team_salute.jpg",
            "badge": "VIỆT NAM vs KYRGYZSTAN",
            "kicker": "19H00 MỸ ĐÌNH • LỜI CHIA TAY 2026",
            "hero_html": 'ĐT VIỆT NAM <span class="hl">QUYẾT ĐẤU KYRGYZSTAN</span>',
            "subtitle": "Hàng công 1,82 m của HLV Kim Sang-sik; tin vui thăng hạng FIFA và điểm sáng thể thao",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "17.11.2026",
            "obj_pos": "center 20%",
        },
        images=v3_imgs,
        plan_slots=v3_slots,
    ),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Dựng tuần tự Shorts Tin Tổng Hợp 17.11.2026")
    parser.add_argument("--only", type=int, nargs="+", help="Chỉ chạy các ID tin chỉ định (vd: --only 1)")
    args = parser.parse_args()

    items = NEWS_DATA_17_11
    if args.only:
        target = set(args.only)
        items = [it for it in NEWS_DATA_17_11 if it["id"] in target]
    if not items:
        raise SystemExit("Không tìm thấy item nào phù hợp với --only")

    run_short_batch(
        CTX,
        items,
        f"XUẤT BẢN 3 VIDEO SHORTS TIN TỔNG HỢP 17.11.2026 (TIN {','.join(str(i['id']) for i in items)} — NAM #15 / NỮ #14)",
    )


if __name__ == "__main__":
    main()
