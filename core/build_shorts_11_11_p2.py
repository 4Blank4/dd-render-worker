#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dựng 2 Video Short 9:16 bổ sung cho ngày 11.11.2026 tại outputs/Orther/11.11.2026/shorts/:
  - Tin #05 (Giọng Nữ — Ngọc Huyền Mẫu 14): VFF đình chỉ vô thời hạn nhóm bán độ của CLB Long An
  - Tin #06 (Giọng Nam — Minh Quân Pro Mẫu 15): 5 ứng viên sáng giá kế nhiệm Michael Carrick tại Man Utd

Quy trình chuẩn DiemDoc:
  - Giữ nguyên 100% Tin 01..04 đã xuất bản trước đó.
  - Chuẩn TTS via core/diemdoc/tts_text.py + config/voice.json (load_voice_preset).
  - Kiểm tra ảnh HD sạch từ kho ảnh đã kiểm chứng + tạo bảng QA Contact Sheet.
  - Export timeline HTML v2 via m8_news_bridge.export_bridge_project -> renderer.render_html_engine.
  - Chuẩn hóa loudnorm -14 LUFS (TP <= -1.0 dBTP), kiểm tra drift <= 1 frame, xuất _thumbnail.jpg & _mota.txt via publisher.py.
"""

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import glob
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR / "core") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "core"))
if str(ROOT_DIR / "engines" / "html") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "engines" / "html"))

from diemdoc import paths
from diemdoc.audio import apply_voice_standard, measure_loudness
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.publisher import load_voice_preset, render_thumbnail_9x16, write_mota_9x16
from diemdoc.tts_text import prepare
from m3_voice import build_chunks_from_text, render_chunk_vitts, trim_segment_silence
from m8_news_bridge import export_bridge_project
from renderer import render_html_engine

DAY_DIR = Path(paths.ROOT) / "outputs" / "Orther" / "11.11.2026"
SHORTS_DIR = DAY_DIR / "shorts"
IMAGES_DIR = DAY_DIR / "images"
AUDIO_DIR = DAY_DIR / "audio"
AUDIO_TITLE_DIR = DAY_DIR / "audio-title"
QA_DIR = DAY_DIR / "qa"

INSPECT_DIR = Path.home() / "Library" / "Caches" / "DiemDoc" / "inspect_11_11"
CACHE_DIR = os.path.join(paths.WORK, "tts_cache_11_11")
WORK_SHORTS_DIR = os.path.join(paths.WORK, "11_11_shorts")

for _d in (SHORTS_DIR, IMAGES_DIR, AUDIO_DIR, AUDIO_TITLE_DIR, QA_DIR):
    _d.mkdir(parents=True, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(WORK_SHORTS_DIR, exist_ok=True)


NEWS_DATA_P2: List[Dict[str, Any]] = [
    {
        "id": 5,
        "slug": "Short_VFF_Dinh_Chi_Nhom_Ban_Do_CLB_Long_An",
        "voice_preset": "secondary",  # Giọng Nữ: Ngọc Huyền (Mẫu 14)
        "group": "BÓNG ĐÁ VIỆT NAM",
        "title": "VFF đình chỉ vô thời hạn nhóm bán độ của CLB Long An",
        "summary": (
            "Ban kỷ luật Liên đoàn Bóng đá Việt Nam vừa ra quyết định đình chỉ vô thời hạn sáu cá nhân liên quan vụ án dàn xếp tỷ số tại CLB Long An. "
            "Án phạt áp dụng từ ngày 17 tháng 9 cho bốn cầu thủ Nguyễn Thanh Hải, Nguyễn Anh Tài, Lê Văn Hưng, Bùi Hoàng Mỹ cùng cặp song sinh cựu tuyển thủ U23 Hoàng Nhật Nam và Hoàng Danh Ngọc. "
            "Theo hồ sơ từ Cục Cảnh sát hình sự Bộ Công an, cả sáu người nằm trong tổng số 21 bị can bị khởi tố trong đường dây cá độ do Vũ Chí Công cầm đầu. "
            "Cơ quan điều tra xác định nhóm này đã móc nối và chỉ đạo các cầu thủ đá dưới sức trong trận thua 1-4 trước Quy Nhơn và thất bại 0-2 trước Nam Định để trục lợi. "
            "Trước khi mùa giải Hạng Nhất mới khởi tranh, ban lãnh đạo đội bóng miền Tây đã chủ động thanh lý hợp đồng toàn bộ những cái tên nhúng chàm. "
            "Từng hai lần đăng quang V-League cùng HLV Henrique Calisto, cựu vương Long An nay chật vật đứng thứ 12 với vỏn vẹn bốn điểm sau bảy vòng đấu."
        ),
        "source": "VnExpress / VFF",
        "news_source": "VnExpress / VFF",
        "credit": "VNEXPRESS / VFF",
        "hide_date_chip": True,
        "seo_title": "VFF đình chỉ vô thời hạn nhóm bán độ của CLB Long An #Shorts",
        "description": [
            "Ban kỷ luật Liên đoàn Bóng đá Việt Nam (VFF) chính thức ban hành quyết định đình chỉ vô thời hạn hoạt động bóng đá đối với 6 thành viên liên quan vụ dàn xếp tỷ số tại CLB Long An.",
            "Danh sách gồm 4 cầu thủ Nguyễn Thanh Hải, Nguyễn Anh Tài, Lê Văn Hưng, Bùi Hoàng Mỹ cùng hai anh em song sinh cựu tuyển thủ U23 Việt Nam Hoàng Nhật Nam và Hoàng Danh Ngọc — đều nằm trong số 21 bị can bị Cục Cảnh sát hình sự (C02) Bộ Công an khởi tố.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#VFF", "#CLBLongAn", "#BongDaVietNam",
            "#HoangDanhNgoc", "#BanDo", "#DanXepTySo", "#VLeague", "#TinBongDa",
        ],
        "thumb": {
            "image": "Tin_05_1.jpg",
            "badge": "TIN NÓNG VFF",
            "kicker": "BÓNG ĐÁ VIỆT NAM",
            "hero_html": 'VFF ĐÌNH CHỈ <span class="hl">VÔ THỜI HẠN</span> NHÓM BÁN ĐỘ LONG AN',
            "subtitle": "6 thành viên Long An, gồm cặp song sinh Danh Ngọc - Nhật Nam, bị cấm hoạt động bóng đá sau án C02",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "11.11.2026",
            "obj_pos": "center 22%",
        },
        "images": [
            # Title (2 ảnh đầu)
            {"dest": "Tin_05_3.jpg", "src": "candidates/t5_vff_1.jpg", "credit": "VFF", "desc": "Trụ sở Liên đoàn Bóng đá Việt Nam (VFF)"},
            {"dest": "Tin_05_1.jpg", "src": "vne_5_2.jpg", "credit": "CỤC CẢNH SÁT HÌNH SỰ / VNEXPRESS", "desc": "4 cầu thủ CLB Long An tại Cục Cảnh sát hình sự"},
            # Câu 1: Ban kỷ luật VFF...
            {"dest": "Tin_05_4.jpg", "src": "candidates2/t5_vff_press_2.jpg", "credit": "VFF", "desc": "Hội trường ban chấp hành VFF"},
            {"dest": "Tin_05_5.jpg", "src": "candidates2/t5_vff_press_1.jpg", "credit": "VFF", "desc": "Họp báo công bố quyết định tại VFF"},
            # Câu 2: 4 cầu thủ & cặp song sinh Danh Ngọc - Nhật Nam
            {"dest": "Tin_05_6.jpg", "src": "candidates/t5_danh_ngoc_1.jpg", "credit": "THỂ THAO VĂN HÓA", "desc": "Hoàng Danh Ngọc thi đấu trên sân cỏ"},
            {"dest": "Tin_05_2.jpg", "src": "vne_5_1.jpg", "credit": "VNEXPRESS", "desc": "Hai anh em sinh đôi Hoàng Danh Ngọc và Hoàng Nhật Nam"},
            # Câu 3: C02 Bộ Công an / 21 bị can / Vũ Chí Công
            {"dest": "Tin_05_7.jpg", "src": "candidates/t5_c02_2.jpg", "credit": "BỘ CÔNG AN", "desc": "Đại diện Cục Cảnh sát hình sự (C02) Bộ Công an"},
            {"dest": "Tin_05_8.jpg", "src": "candidates/t5_c02_1.jpg", "credit": "BÁO GIAO THÔNG / BỘ CÔNG AN", "desc": "Toàn cảnh thông tin vụ án tại Bộ Công an"},
            # Câu 4: Trận thua 1-4 Quy Nhơn & 0-2 Nam Định
            {"dest": "Tin_05_9.jpg", "src": "candidates/t5_long_an_2_2.jpg", "credit": "THANH NIÊN", "desc": "Cầu thủ CLB Long An thi đấu trên sân"},
            {"dest": "Tin_05_10.jpg", "src": "candidates/t5_nam_dinh_2.jpg", "credit": "TUỔI TRẺ", "desc": "Đội bóng Nam Định ăn mừng danh hiệu vô địch quốc nội"},
            # Câu 5: Thanh lý hợp đồng trước giải Hạng Nhất
            {"dest": "Tin_05_11.jpg", "src": "candidates/t5_long_an_1_2.jpg", "credit": "SÀI GÒN GIẢI PHÓNG", "desc": "Đội hình ra sân của CLB Long An tại giải Hạng Nhất"},
            {"dest": "Tin_05_12.jpg", "src": "candidates/t5_long_an_2_1.jpg", "credit": "ZNEWS", "desc": "Pha tranh chấp bóng của các cầu thủ Long An"},
            # Câu 6: Hai lần V-League Calisto -> hạng 12
            {"dest": "Tin_05_13.jpg", "src": "candidates/t5_calisto_1.jpg", "credit": "LAO ĐỘNG", "desc": "Đồng Tâm Long An và HLV Henrique Calisto vô địch V-League 2006"},
            {"dest": "Tin_05_14.jpg", "src": "candidates/t5_svdl_1.jpg", "credit": "LAO ĐỘNG", "desc": "Khán đài Sân vận động Long An"},
        ],
        "plan_slots": [
            ("title", 0, "Tin_05_3.jpg"),
            ("title", 0, "Tin_05_1.jpg"),
            ("sentence", 1, "Tin_05_4.jpg"),
            ("sentence", 1, "Tin_05_5.jpg"),
            ("sentence", 2, "Tin_05_6.jpg"),
            ("sentence", 2, "Tin_05_2.jpg"),
            ("sentence", 3, "Tin_05_7.jpg"),
            ("sentence", 3, "Tin_05_8.jpg"),
            ("sentence", 4, "Tin_05_9.jpg"),
            ("sentence", 4, "Tin_05_10.jpg"),
            ("sentence", 5, "Tin_05_11.jpg"),
            ("sentence", 5, "Tin_05_12.jpg"),
            ("sentence", 6, "Tin_05_13.jpg"),
            ("sentence", 6, "Tin_05_14.jpg"),
        ],
    },
    {
        "id": 6,
        "slug": "Short_5_Ung_Vien_Ke_Nhiem_Carrick_Man_Utd",
        "voice_preset": "primary",  # Giọng Nam: Minh Quân Pro (Mẫu 15)
        "group": "BÓNG ĐÁ ANH",
        "title": "5 ứng viên sáng giá kế nhiệm Michael Carrick tại Man Utd",
        "summary": (
            "Giữa áp lực sa thải Michael Carrick, ban lãnh đạo Man Utd đang cân nhắc năm gương mặt thay thế hàng đầu theo đánh giá của BBC. "
            "Ứng viên đầu tiên là Mauricio Pochettino, người mới đưa tuyển Mỹ vào vòng 16 đội World Cup 2026 và có điều khoản giải phóng trị giá 10 triệu USD. "
            "Tiếp theo là Julian Nagelsmann với tỷ lệ thắng 83,3 phần trăm tại Champions League cùng Bayern Munich và từng làm việc ăn ý với giám đốc Christopher Vivell. "
            "Tại nước Anh, Eddie Howe nổi lên nhờ mức phí bồi thường thấp sau khi giúp Newcastle chấm dứt cơn khát danh hiệu kéo dài từ năm 1955. "
            "Cái tên giàu thành tích nhất là Antonio Conte với năm chức vô địch Serie A và tỷ lệ thắng 62,9 phần trăm cao nhất nhóm ứng viên tại Ngoại hạng Anh. "
            "Cuối cùng, Unai Emery gây ấn tượng mạnh khi đưa Aston Villa vô địch Europa League, nhưng ông lại sắp gia hạn hợp đồng mới. "
            "Dù đều sở hữu bảng thành tích ấn tượng, ban lãnh đạo Quỷ đỏ vẫn phải cân nhắc giữa cá tính mạnh của Conte và việc Nagelsmann chưa từng dẫn dắt tại Ngoại hạng Anh."
        ),
        "source": "VnExpress / BBC",
        "news_source": "VnExpress / BBC",
        "credit": "VNEXPRESS / BBC",
        "hide_date_chip": True,
        "seo_title": "5 ứng viên sáng giá kế nhiệm Michael Carrick tại Man Utd #Shorts",
        "description": [
            "Trước sức ép sa thải Michael Carrick tại Old Trafford, ban lãnh đạo Man Utd đang cân nhắc 5 HLV hàng đầu theo phân tích của BBC.",
            "Từ Mauricio Pochettino (phí giải phóng 10 triệu USD), Julian Nagelsmann (83,3% thắng C1 cùng Bayern), Eddie Howe (cựu HLV Newcastle), Antonio Conte (5 danh hiệu Serie A, 62,9% thắng Ngoại hạng Anh) đến Unai Emery vừa vô địch Europa League cùng Aston Villa.",
        ],
        "hashtags": [
            "#Shorts", "#DiemDoc", "#ManUtd", "#MichaelCarrick", "#Pochettino",
            "#Nagelsmann", "#EddieHowe", "#AntonioConte", "#UnaiEmery", "#NgoaiHangAnh",
        ],
        "thumb": {
            "image": "Tin_06_1.jpg",
            "badge": "NGOẠI HẠNG ANH",
            "kicker": "ĐIỂM NÓNG OLD TRAFFORD",
            "hero_html": '5 ỨNG VIÊN <span class="hl">KẾ NHIỆM</span> CARRICK Ở MAN UTD',
            "subtitle": "Pochettino, Nagelsmann, Eddie Howe, Antonio Conte hay Unai Emery sẽ ngồi ghế nóng Quỷ đỏ?",
            "tag_a": "ĐIỂM ĐỌC SHORTS",
            "tag_b": "11.11.2026",
            "obj_pos": "center 18%",
        },
        "images": [
            # Title (2 ảnh đầu)
            {"dest": "Tin_06_1.jpg", "src": "candidates/t6_carrick_2.jpg", "credit": "MIRROR", "desc": "HLV Michael Carrick trầm ngâm bên đường pitch"},
            {"dest": "Tin_06_2.jpg", "src": "candidates/t6_old_trafford_1.jpg", "credit": "USA TODAY / REUTERS", "desc": "Sân vận động Old Trafford lung linh ánh đèn"},
            # Câu 1: Áp lực sa thải Carrick, BLĐ Man Utd cân nhắc 5 ứng viên
            {"dest": "Tin_06_3.jpg", "src": "candidates/t6_ratcliffe_2.jpg", "credit": "TALKSPORT", "desc": "Tỷ phú Sir Jim Ratcliffe trên khán đài Old Trafford"},
            {"dest": "Tin_06_4.jpg", "src": "candidates/t6_carrick_1.jpg", "credit": "FOOTBALL BLOG", "desc": "HLV Michael Carrick trong phòng họp báo Man Utd"},
            # Câu 2: Mauricio Pochettino
            {"dest": "Tin_06_5.jpg", "src": "vne_6_1.jpg", "credit": "VNEXPRESS / REUTERS", "desc": "HLV Mauricio Pochettino vẫy tay chỉ đạo"},
            {"dest": "Tin_06_6.jpg", "src": "candidates2/t6_poch_clean_1.jpg", "credit": "MARCA / AP", "desc": "Cận cảnh Mauricio Pochettino bên đường biên"},
            # Câu 3: Julian Nagelsmann & Christopher Vivell
            {"dest": "Tin_06_7.jpg", "src": "vne_6_2.jpg", "credit": "VNEXPRESS / AP", "desc": "HLV Julian Nagelsmann hò hét chỉ đạo trên sân"},
            {"dest": "Tin_06_8.jpg", "src": "candidates/t6_vivell_2.jpg", "credit": "MANCHESTER EVENING NEWS", "desc": "Giám đốc tuyển dụng Christopher Vivell tại sân tập"},
            # Câu 4: Eddie Howe
            {"dest": "Tin_06_9.jpg", "src": "vne_6_3.jpg", "credit": "VNEXPRESS / REUTERS", "desc": "Eddie Howe nâng cúp Liên đoàn cùng Newcastle"},
            {"dest": "Tin_06_10.jpg", "src": "candidates/t6_howe_2.jpg", "credit": "CHRONICLE LIVE", "desc": "HLV Eddie Howe quan sát trận đấu Ngoại hạng Anh"},
            # Câu 5: Antonio Conte
            {"dest": "Tin_06_11.jpg", "src": "candidates/t6_conte_napoli_2.jpg", "credit": "FOOTBALL ITALIA", "desc": "Antonio Conte hôn cúp vô địch Serie A cùng Napoli"},
            {"dest": "Tin_06_12.jpg", "src": "vne_6_4.jpg", "credit": "VNEXPRESS / AP", "desc": "HLV Antonio Conte đầy cảm xúc bên đường pitch"},
            # Câu 6: Unai Emery
            {"dest": "Tin_06_13.jpg", "src": "vne_6_5.jpg", "credit": "VNEXPRESS / REUTERS", "desc": "Unai Emery được học trò công kênh ăn mừng cúp Europa League"},
            {"dest": "Tin_06_14.jpg", "src": "candidates/t6_emery_2.jpg", "credit": "SPORT WITNESS", "desc": "HLV Unai Emery giơ nắm đấm ăn mừng chiến thắng"},
            # Câu 7: Cân nhắc Conte / Nagelsmann tại Old Trafford
            {"dest": "Tin_06_15.jpg", "src": "candidates/t6_nagelsmann_2.jpg", "credit": "VOV", "desc": "Julian Nagelsmann từng dẫn dắt Bayern Munich và tuyển Đức"},
            {"dest": "Tin_06_16.jpg", "src": "candidates/t6_old_trafford_2.jpg", "credit": "OLD TRAFFORD", "desc": "Toàn cảnh sân vận động Old Trafford của Man Utd"},
        ],
        "plan_slots": [
            ("title", 0, "Tin_06_1.jpg"),
            ("title", 0, "Tin_06_2.jpg"),
            ("sentence", 1, "Tin_06_3.jpg"),
            ("sentence", 1, "Tin_06_4.jpg"),
            ("sentence", 2, "Tin_06_5.jpg"),
            ("sentence", 2, "Tin_06_6.jpg"),
            ("sentence", 3, "Tin_06_7.jpg"),
            ("sentence", 3, "Tin_06_8.jpg"),
            ("sentence", 4, "Tin_06_9.jpg"),
            ("sentence", 4, "Tin_06_10.jpg"),
            ("sentence", 5, "Tin_06_11.jpg"),
            ("sentence", 5, "Tin_06_12.jpg"),
            ("sentence", 6, "Tin_06_13.jpg"),
            ("sentence", 6, "Tin_06_14.jpg"),
            ("sentence", 7, "Tin_06_15.jpg"),
            ("sentence", 7, "Tin_06_16.jpg"),
        ],
    },
]


def has_getty_watermark(pil_img: Image.Image) -> bool:
    """Phát hiện dấu chữ watermark chìm nhẹ trên vùng giữa ảnh."""
    w, h = pil_img.size
    crop = pil_img.crop((int(w * 0.25), int(h * 0.35), int(w * 0.75), int(h * 0.65))).convert("L")
    arr = np.array(crop, dtype=np.float32)
    if arr.shape[0] < 2 or arr.shape[1] < 2:
        return False
    gx = np.abs(np.diff(arr, axis=1))[:-1, :]
    gy = np.abs(np.diff(arr, axis=0))[:, :-1]
    sharp_ratio = float(np.mean((gx > 25) | (gy > 25)))
    # Ảnh tư liệu thể thao thật có chi tiết bình thường; hàm dùng để lọc banner chữ chìm quá dày
    return sharp_ratio > 0.65


def copy_and_verify_images(item: Dict[str, Any]) -> Dict[str, str]:
    """Sao chép ảnh sạch đã kiểm duyệt từ INSPECT_DIR vào DAY_DIR/images/ và trả về credit map."""
    credits_map: Dict[str, str] = {}
    for spec in item["images"]:
        src_path = INSPECT_DIR / spec["src"]
        if not src_path.exists():
            die(f"Thiếu ảnh nguồn đã kiểm duyệt: {src_path}")
        with Image.open(src_path) as im:
            im = im.convert("RGB")
            w, h = im.size
            if w < 600 or h < 350:
                die(f"Ảnh {src_path} độ phân giải quá thấp: {w}x{h}")
            if has_getty_watermark(im):
                warn(f"Cảnh báo mật độ cạnh cao trên {spec['src']} ({w}x{h}) — giữ vì đã duyệt thị giác.")
            dest_path = IMAGES_DIR / spec["dest"]
            im.save(dest_path, format="JPEG", quality=95, optimize=True)
        credits_map[spec["dest"]] = spec["credit"]
        ok(f"Đã nạp ảnh sạch: {spec['dest']} ({w}x{h}, {spec['credit']})")
    return credits_map


def build_contact_sheet(item: Dict[str, Any]) -> Path:
    """Xuất bảng ảnh đối chứng QA (Contact Sheet) lưu tại qa/contact_scene_XX.jpg."""
    sc_id = item["id"]
    out_sheet = QA_DIR / f"contact_scene_{sc_id:02d}.jpg"
    imgs = item["images"]
    cols = 4
    rows = (len(imgs) + cols - 1) // cols
    cell_w, cell_h = 460, 340
    header_h = 84
    canvas = Image.new("RGB", (cols * cell_w + 40, rows * cell_h + header_h + 20), (10, 14, 24))
    draw = ImageDraw.Draw(canvas)

    try:
        font_hdr = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 19)
        font_lbl = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
        font_cap = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
    except Exception:
        font_hdr = font_sub = font_lbl = font_cap = ImageFont.load_default()

    draw.text((20, 14), f"QA CONTACT SHEET — TIN #{sc_id:02d}: {item['title']}", fill=(0, 229, 255), font=font_hdr)
    draw.text((20, 50), f"Tong so anh: {len(imgs)} | Nguon tin: {item['news_source']} | Voice preset: {item['voice_preset']}", fill=(190, 205, 225), font=font_sub)

    for idx, spec in enumerate(imgs):
        r, c = divmod(idx, cols)
        x0 = 20 + c * cell_w + 10
        y0 = header_h + r * cell_h + 8
        draw.rectangle([x0 - 2, y0 - 2, x0 + 440, y0 + 322], outline=(0, 180, 216), width=2, fill=(18, 24, 38))
        p = IMAGES_DIR / spec["dest"]
        with Image.open(p) as im:
            im_rgb = im.convert("RGB")
            orig_size = f"{im_rgb.width}x{im_rgb.height}"
            im_rgb.thumbnail((432, 240), Image.Resampling.LANCZOS)
            px = x0 + (436 - im_rgb.width) // 2
            py = y0 + (244 - im_rgb.height) // 2
            canvas.paste(im_rgb, (px, py))
        draw.text((x0 + 8, y0 + 250), f"{spec['dest']} ({orig_size})", fill=(0, 229, 255), font=font_lbl)
        draw.text((x0 + 8, y0 + 272), f"Nguon: {spec['credit']}", fill=(250, 204, 21), font=font_cap)
        desc = spec["desc"][:48] + ("..." if len(spec["desc"]) > 48 else "")
        draw.text((x0 + 8, y0 + 294), desc, fill=(220, 230, 245), font=font_cap)

    canvas.save(out_sheet, format="JPEG", quality=92)
    ok(f"Đã tạo bảng đối chứng QA: {out_sheet}")
    return out_sheet


def synthesize_item_audio(model: Any, item: Dict[str, Any]) -> Dict[str, Any]:
    """Sinh audio tiêu đề & audio đầy đủ chuẩn -14 LUFS với giọng đọc được chỉ định."""
    sc_id = item["id"]
    preset_info = load_voice_preset(item["voice_preset"])
    voice_name = preset_info["voice_id"]
    spd = preset_info["speed"]
    pch = preset_info["pitch"]
    temp = preset_info["temperature"]
    step(f"Tin #{sc_id:02d} — Tổng hợp giọng: {preset_info['voice_label']} (spd={spd}, pch={pch}, temp={temp})")

    title_out = AUDIO_TITLE_DIR / f"audio_title_{sc_id:02d}.wav"
    clean_title, _ = prepare(item["title"])
    raw_title_seg, _ = render_chunk_vitts(
        model, clean_title, voice_name,
        temperature=temp, speed=spd, pitch=pch,
        cache_dir=CACHE_DIR, use_cache=True, max_chars=768,
    )
    raw_title_seg = trim_segment_silence(raw_title_seg)
    std_title_seg = apply_voice_standard(raw_title_seg)
    std_title_seg.export(str(title_out), format="wav")

    clean_summary, _ = prepare(item["summary"])
    chunks = build_chunks_from_text(clean_summary, max_words_per_chunk=60, inter_sentence_pause=0.25)
    summary_seg = AudioSegment.empty()
    for ch in chunks:
        c_seg, _ = render_chunk_vitts(
            model, ch["text"], voice_name,
            temperature=temp, speed=spd, pitch=pch,
            cache_dir=CACHE_DIR, use_cache=True, max_chars=768,
        )
        c_seg = trim_segment_silence(c_seg)
        summary_seg += c_seg
        pause_ms = int(round(ch.get("pause_after", 0.25) * 1000))
        if pause_ms > 0:
            summary_seg += AudioSegment.silent(duration=pause_ms)

    full_out = AUDIO_DIR / f"audio_{sc_id:02d}.wav"
    combined_raw = raw_title_seg + AudioSegment.silent(duration=350) + summary_seg
    std_full_seg = apply_voice_standard(combined_raw)
    std_full_seg.export(str(full_out), format="wav")

    dur_sec = round(AudioSegment.from_wav(str(full_out)).duration_seconds, 2)
    title_dur = round(AudioSegment.from_wav(str(title_out)).duration_seconds, 2)
    ok(f"Audio Tin #{sc_id:02d} hoàn tất: full={dur_sec}s, title={title_dur}s -> {full_out.name}")
    return {"audio_path": str(full_out), "audio_title": str(title_out), "duration": dur_sec}


def merge_day_metadata(new_credits: Dict[str, str], audio_meta: Dict[int, Dict[str, Any]]) -> None:
    """Cập nhật image_credits.json, image_plan.json và thethao.json mà không làm hỏng Tin 01..04."""
    credits_path = DAY_DIR / "image_credits.json"
    existing_credits: Dict[str, str] = {}
    if credits_path.exists():
        existing_credits = json.loads(credits_path.read_text(encoding="utf-8"))
    for k in list(existing_credits.keys()):
        if k.startswith("Tin_05_") or k.startswith("Tin_06_"):
            del existing_credits[k]
    existing_credits.update(new_credits)
    credits_path.write_text(json.dumps(existing_credits, ensure_ascii=False, indent=2), encoding="utf-8")

    plan_path = DAY_DIR / "image_plan.json"
    existing_records: List[Dict[str, Any]] = []
    if plan_path.exists():
        existing_records = json.loads(plan_path.read_text(encoding="utf-8")).get("records", [])
    kept_records = [r for r in existing_records if int(r.get("scene_id", 0)) not in (5, 6)]
    for item in NEWS_DATA_P2:
        sc_id = item["id"]
        spec_by_dest = {sp["dest"]: sp for sp in item["images"]}
        for slot_type, sent_idx, fname in item["plan_slots"]:
            sp = spec_by_dest[fname]
            kept_records.append({
                "scene_id": sc_id,
                "type": slot_type,
                "index": 1 if slot_type == "title" else sent_idx,
                "sentence_idx": 0 if slot_type == "title" else sent_idx,
                "file_name": fname,
                "credit": sp["credit"],
                "description": sp["desc"],
            })
    plan_path.write_text(json.dumps({"records": kept_records}, ensure_ascii=False, indent=2), encoding="utf-8")

    tt_path = DAY_DIR / "thethao.json"
    existing_tt: List[Dict[str, Any]] = []
    if tt_path.exists():
        existing_tt = json.loads(tt_path.read_text(encoding="utf-8"))

    dedup_tt: List[Dict[str, Any]] = []
    seen_ids = set()
    for row in existing_tt:
        rid = int(row.get("id", 0))
        if rid in (5, 6) or rid in seen_ids:
            continue
        seen_ids.add(rid)
        dedup_tt.append(row)

    for item in NEWS_DATA_P2:
        sc_id = item["id"]
        am = audio_meta[sc_id]
        entry: Dict[str, Any] = {
            "id": sc_id,
            "slug": item["slug"],
            "group": item["group"],
            "title": item["title"],
            "summary": item["summary"],
            "source": item["source"],
            "news_source": item["news_source"],
            "credit": item["credit"],
            "hide_date_chip": item["hide_date_chip"],
            "audio_path": am["audio_path"],
            "audio_title": am["audio_title"],
            "duration": am["duration"],
        }
        for idx, sp in enumerate(item["images"], start=1):
            entry[f"image_{idx}"] = str(IMAGES_DIR / sp["dest"])
        entry["image_path"] = entry["image_1"]
        dedup_tt.append(entry)

    tt_path.write_text(json.dumps(dedup_tt, ensure_ascii=False, indent=2), encoding="utf-8")
    ok("Đã đồng bộ an toàn image_credits.json, image_plan.json và thethao.json (giữ nguyên Tin 01..04).")


def trim_video_audio_drift(mp4_path: Path, item_id: int) -> None:
    """Cắt chính xác luồng audio theo duration của video stream nếu lệch > 25ms (drift <= 1 frame 30fps)."""
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=duration,codec_type", "-of", "json", str(mp4_path)],
        capture_output=True, text=True, check=True,
    )
    streams = json.loads(probe.stdout).get("streams", [])
    v_dur = next(float(s["duration"]) for s in streams if s.get("codec_type") == "video")
    a_dur = next(float(s["duration"]) for s in streams if s.get("codec_type") == "audio")
    if abs(v_dur - a_dur) <= 0.025:
        return
    tmp_sync = Path(WORK_SHORTS_DIR) / f"short_{item_id}_sync.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(mp4_path), "-t", f"{v_dur:.6f}",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            str(tmp_sync),
        ],
        check=True,
    )
    shutil.copy2(str(tmp_sync), str(mp4_path))


def build_and_publish_short(item: Dict[str, Any]) -> None:
    """Export timeline bridge, render HTML v2, kiểm âm thanh, xuất thumbnail 9:16 và mota SEO."""
    sc_id = item["id"]
    slug = item["slug"]
    banner(f"RENDER & XUẤT BẢN TIN #{sc_id:02d}: {slug}")

    work_proj_dir = os.path.join(WORK_SHORTS_DIR, f"short_{sc_id}")
    if os.path.exists(work_proj_dir):
        shutil.move(work_proj_dir, os.path.join(Path.home(), ".Trash", f"short_{sc_id}_{os.getpid()}"))

    pdir, _, _ = export_bridge_project(
        day_dir=str(DAY_DIR),
        item_id=str(sc_id),
        format_type="short",
        work_proj_dir=work_proj_dir,
        global_offset_sec=0.0,
    )

    out_work_mp4 = render_html_engine(
        project_dir=str(pdir),
        template="short_news_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True,
    )
    if not out_work_mp4 or not os.path.exists(out_work_mp4):
        die(f"Render HTML engine thất bại cho Tin #{sc_id:02d}")

    out_mp4 = SHORTS_DIR / f"{slug}.mp4"
    shutil.copy2(out_work_mp4, str(out_mp4))
    trim_video_audio_drift(out_mp4, sc_id)

    loud = measure_loudness(str(out_mp4))
    if loud:
        ok(f"Xuất MP4 thành công: {out_mp4.name} | I={loud['input_i']} LUFS | TP={loud['input_tp']} dBTP")
    else:
        ok(f"Xuất MP4 thành công: {out_mp4.name}")
    chk = subprocess.run(["python3", "-B", str(ROOT_DIR / "core" / "audio_check.py"), str(out_mp4)], check=False)
    if chk.returncode != 0:
        warn(f"audio_check trả về mã {chk.returncode} cho {out_mp4.name} — cần kiểm tra lại!")

    mota_path = SHORTS_DIR / f"{slug}_mota.txt"
    write_mota_9x16(
        out_path=mota_path,
        seo_title=item["seo_title"],
        description_paragraphs=item["description"],
        chapters=None,
        sources_line=item["news_source"],
        hashtags=item["hashtags"],
    )
    ok(f"Đã tạo mô tả SEO: {mota_path.name}")

    t_cfg = item["thumb"]
    thumb_path = SHORTS_DIR / f"{slug}_thumbnail.jpg"
    render_thumbnail_9x16(
        out_path=thumb_path,
        image_path=IMAGES_DIR / t_cfg["image"],
        kicker=t_cfg["kicker"],
        hero_html=t_cfg["hero_html"],
        subtitle=t_cfg["subtitle"],
        badge=t_cfg["badge"],
        tag_a=t_cfg["tag_a"],
        tag_b=t_cfg["tag_b"],
        obj_pos=t_cfg["obj_pos"],
    )
    ok(f"Đã tạo Thumbnail 9:16: {thumb_path.name}")


def main() -> None:
    banner("SẢN XUẤT 2 VIDEO SHORTS BỔ SUNG NGÀY 11.11.2026 (TIN #05 & TIN #06)")

    all_credits: Dict[str, str] = {}
    for item in NEWS_DATA_P2:
        all_credits.update(copy_and_verify_images(item))
        build_contact_sheet(item)

    step("Khởi tạo Vieneu v3turbo TTS engine...")
    from vieneu import Vieneu
    tts_model = Vieneu(mode="v3turbo")

    audio_meta: Dict[int, Dict[str, Any]] = {}
    for item in NEWS_DATA_P2:
        audio_meta[item["id"]] = synthesize_item_audio(tts_model, item)

    merge_day_metadata(all_credits, audio_meta)

    for item in NEWS_DATA_P2:
        build_and_publish_short(item)

    banner("HOÀN TẤT XUẤT BẢN TIN #05 & TIN #06")


if __name__ == "__main__":
    main()
