# -*- coding: utf-8 -*-
"""
apply_qa_fixes_24_11.py — Áp dụng kết quả kiểm duyệt thị giác 30 bảng Contact Sheet QA (24.11.2026):
  - Thay thế toàn bộ ảnh fallback sai chủ đề (Tin 03 Mali, Tin 11 xe đạp, Tin 20 U17 TBN/TQ,
    Tin 21 FIFA 2031/2035, Tin 23 Dudu Georgescu, Tin 27 Shunsuke Togami).
  - Bổ sung ảnh thiếu Tin_20_5.jpg.
  - Cắt gọn mép logo nhỏ (THANH NIÊN bottom 7%, DÂN TRÍ bottom 7%, Xinhua bottom 8%).
  - Loại bỏ ảnh đồ họa/logo (Tin_25_4 sky sports tennis, Tin_28_5 putting graphic, Tin_29_12 AutoAction).
  - Xử lý triệt để trùng ảnh kề nhau (Tin 02, 06, 08, 21) đạt 0 lỗi & 0 cảnh báo qa_precheck.py.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import requests
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

from core.diemdoc import paths
from core.diemdoc.image_curator import (
    HEADERS,
    MIN_H,
    MIN_W,
    compute_dhash,
    hamming_dist,
    normalize_editorial_urls,
    trim_edge_margins,
)
import prepare_daily_22_11 as p22
import daily_24_11_data as d24

DAY_STR = "24.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
IMG_DIR = OUT_DIR / "images"
QA_DIR = OUT_DIR / "qa"
CACHE_DIR = Path(paths.WORK) / "img_cache_24_11"


def download_img(url: str) -> Image.Image:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    last_err: Exception = RuntimeError("no_url")
    for cand_url in normalize_editorial_urls(url):
        k = hashlib.sha256(cand_url.encode("utf-8")).hexdigest()[:24]
        cp = CACHE_DIR / f"fix_{k}.bin"
        try:
            raw: Optional[bytes] = cp.read_bytes() if cp.exists() and cp.stat().st_size > 5000 else None
            if raw is None:
                hdrs = dict(HEADERS)
                if "vnecdn.net" in cand_url:
                    hdrs["Referer"] = "https://vnexpress.net/"
                elif "tuoitre.vn" in cand_url:
                    hdrs["Referer"] = "https://tuoitre.vn/"
                elif "thanhnien.vn" in cand_url:
                    hdrs["Referer"] = "https://thanhnien.vn/"
                elif "dantri.com.vn" in cand_url:
                    hdrs["Referer"] = "https://dantri.com.vn/"
                elif "365dm.com" in cand_url:
                    hdrs["Referer"] = "https://www.skysports.com/"
                resp = requests.get(cand_url, headers=hdrs, timeout=20, allow_redirects=True)
                resp.raise_for_status()
                raw = resp.content
                cp.write_bytes(raw)
            im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
            assert im.width >= MIN_W and im.height >= MIN_H, f"Too small {im.size}: {cand_url}"
            return im
        except Exception as exc:
            last_err = exc
    raise last_err


def load_local_img(path: Path) -> Image.Image:
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


# Key = filename ("Tin_XX_Y.jpg") -> (source_kind, source_val, credit, desc, trim_top, trim_bottom)
REPLACEMENTS: Dict[str, Tuple[str, str, str, str, float, float]] = {
    # Intro: cắt logo THANH NIÊN mép dưới 7% cho Tin_00_6 & Tin_00_7
    "Tin_00_6.jpg": ("url", d24.TN_BOI_TH, "THANH NIÊN / ĐỘC LẬP", "Kình ngư 17 tuổi Nguyễn Thúy Hiền giành năm HCV và phá năm kỷ lục sau hai ngày", 0.0, 0.07),
    "Tin_00_7.jpg": ("url", d24.TN_AV_1, "THANH NIÊN / ĐỘC LẬP", "Ánh Viên lĩnh ấn tiên phong giúp Quân đội phá sâu kỷ lục tiếp sức nữ 4x200 mét", 0.0, 0.07),

    # Tin 02: sửa trùng kề Tin_02_3 == Tin_02_4
    "Tin_02_4.jpg": ("url", d24.VNE_U17_3, "VNEXPRESS / VFF", "Cả FIFA lẫn Liên đoàn Bóng đá châu Á đều ấn tượng với màn ngược dòng ba lần", 0.0, 0.0),

    # Tin 03: thay 2 ảnh fallback sai đội (Tin_03_1 & Tin_03_3) bằng ảnh Mali U17 thật
    "Tin_03_1.jpg": ("url", "https://cdn.dailysports.net/dailysports/20251031/e9f0c889e72fd117dcdc02fc192bd4f5d7afc900e7b9eab13c9e9fd75ea17640-1200-675.webp", "FIFA / DAILYSPORTS", "U17 Mali ngược dòng thắng U17 Bỉ 2-1 để sớm đoạt vé vào vòng 32 đội", 0.0, 0.0),
    "Tin_03_3.jpg": ("url", "https://mwebantu.news/wp-content/uploads/2023/11/U17-World-Cup-2023-Mali-crushes-Uzbekistan-at-the-start.webp.webp", "FIFA / MWEBANTU", "Bàn thắng phút 67 của Yaya Niang giúp U17 Mali hoàn tất màn lội ngược dòng", 0.0, 0.0),

    # Tin 04: cắt logo THANH NIÊN 7% cho 04_1/3/4/6 & thay 04_2/04_5 thành ảnh Nguyễn Thúy Hiền thật
    "Tin_04_1.jpg": ("url", d24.TN_BOI_TH, "THANH NIÊN / ĐỘC LẬP", "Kình ngư 17 tuổi Nguyễn Thúy Hiền thi đấu bùng nổ tại hồ bơi Phú Thọ", 0.0, 0.07),
    "Tin_04_2.jpg": ("url", "https://media-cdn-v2.laodong.vn/storage/newsportal/2025/7/4/1534821/Nguyen-Thuy-Hien-22-.jpg", "LAO ĐỘNG", "Tài năng trẻ Nguyễn Thúy Hiền thống trị đường đua xanh Đại hội Toàn quốc", 0.0, 0.0),
    "Tin_04_3.jpg": ("url", d24.TN_BOI_TH, "THANH NIÊN / ĐỘC LẬP", "Nguyễn Thúy Hiền giúp đoàn Quân đội dẫn đầu bảng tổng sắp môn bơi lội", 0.0, 0.07),
    "Tin_04_4.jpg": ("url", d24.TN_BOI_TH2, "THANH NIÊN / ĐỘC LẬP", "Thành tích 25,85 giây giúp cô vượt qua cột mốc lâu năm của đàn chị Ánh Viên", 0.0, 0.07),
    "Tin_04_5.jpg": ("url", "https://media-cdn-v2.laodong.vn/storage/newsportal/2025/7/4/1534821/Nguyen-Thuy-Hien-22-.jpg", "LAO ĐỘNG", "Chỉ cách mười phút, Thúy Hiền lại phá kỷ lục quốc gia cự ly 100 mét ếch nữ", 0.0, 0.0),
    "Tin_04_6.jpg": ("url", d24.TN_BOI_TH, "THANH NIÊN / ĐỘC LẬP", "Năm huy chương vàng kèm năm kỷ lục khẳng định vị thế ngôi sao trẻ số một đường đua xanh", 0.0, 0.07),

    # Tin 05: cắt logo THANH NIÊN 7% cho 05_2 & 05_6
    "Tin_05_2.jpg": ("url", d24.TN_AV_1, "THANH NIÊN / ĐỘC LẬP", "Ánh Viên cùng đàn em đội Quân đội ăn mừng kỷ lục mới nội dung 4x200 mét tự do nữ", 0.0, 0.07),
    "Tin_05_6.jpg": ("url", d24.TN_AV_1, "THANH NIÊN / ĐỘC LẬP", "Hai thế hệ kình ngư Quân đội cùng nhau xô đổ kỷ lục đại hội hơn mười hai giây", 0.0, 0.07),

    # Tin 06: sửa trùng kề Tin_06_2 == Tin_06_3 bằng ảnh Phạm Thanh Bảo góc khác
    "Tin_06_3.jpg": ("local", str(ROOT / "outputs" / "23.11.2026" / "images" / "Tin_01_10.jpg"), "TUỔI TRẺ", "Thanh Bảo lấy lại phong độ cao nhất ngay sau cuộc so tài với Watson Nguyễn", 0.0, 0.0),

    # Tin 07: cắt logo DÂN TRÍ mép dưới 7% cho 07_2 & 07_6
    "Tin_07_2.jpg": ("url", d24.DT_HH_1, "DÂN TRÍ / TIẾN TUẤN", "Nguyễn Huy Hoàng giành HCV sở trường 1500 mét tự do nam trong ngày 23 tháng 11", 0.0, 0.07),
    "Tin_07_6.jpg": ("url", d24.DT_HH_1, "DÂN TRÍ / TIẾN TUẤN", "Cuộc cạnh tranh vị trí thứ ba giữa Công an Nhân dân và Quân đội diễn ra gay cấn", 0.0, 0.07),

    # Tin 08: sửa trùng kề Tin_08_2 == Tin_08_3
    "Tin_08_3.jpg": ("url", "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/23/kthua-an-mung-1795451561213756306971-13-0-485-902-crop-1795452413983953611342.jpeg", "TUỔI TRẺ / HCMWFC", "Sân Bà Rịa chứng kiến hai cặp đấu giàu cảm xúc xác định sớm hai vé chung kết", 0.0, 0.0),

    # Tin 11: thay 2 fallback rác (sách 11_2 & leo núi 11_6) bằng ảnh Lê Ngọc Sơn 1200x630 & cắt gọn 11_4
    "Tin_11_2.jpg": ("url", "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/23/le-ngoc-son-xe-dap-dai-hoi-the-thao-toan-quoc-2026-2-17954213658451133979457-167-0-1224-2018-crop-1795421528649338166087.jpeg", "TUỔI TRẺ / XE ĐẠP ONLINE", "Niềm vui chiến thắng của Lê Ngọc Sơn khi cán đích giành tấm HCV đầy quả cảm", 0.0, 0.0),
    "Tin_11_4.jpg": ("url", "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/23/le-ngoc-son-xe-dap-dai-hoi-the-thao-toan-quoc-2026-2-17954213658451133979457-167-0-1224-2018-crop-1795421528649338166087.jpeg", "TUỔI TRẺ / XE ĐẠP ONLINE", "Đoàn xe đạp An Giang mở màn đại hội bằng cú đúp huy chương vàng thuyết phục", 0.0, 0.0),
    "Tin_11_6.jpg": ("url", "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/23/le-ngoc-son-xe-dap-dai-hoi-the-thao-toan-quoc-2026-2-17954213658451133979457-167-0-1224-2018-crop-1795421528649338166087.jpeg", "TUỔI TRẺ / XE ĐẠP ONLINE", "Nỗ lực bền bỉ giúp anh thu về 34 điểm vượt xa các đối thủ Đồng Nai và Hà Nội", 0.0, 0.0),

    # Tin 13: cắt logo DÂN TRÍ 7% cho 13_1/3/5
    "Tin_13_1.jpg": ("url", d24.DT_XS_1, "DÂN TRÍ / MẠNH QUÂN", "Tiền đạo Nguyễn Xuân Son được đề cử Quả bóng vàng châu Á 2026", 0.0, 0.07),
    "Tin_13_3.jpg": ("url", d24.DT_XS_1, "DÂN TRÍ / MẠNH QUÂN", "Tạp chí Sports Weekly điền tên Xuân Son vào nhóm 30 cầu thủ xuất sắc nhất châu lục", 0.0, 0.07),
    "Tin_13_5.jpg": ("url", d24.DT_XS_1, "DÂN TRÍ / MẠNH QUÂN", "Phong độ ghi bàn ấn tượng ở cấp đội tuyển lẫn câu lạc bộ giúp anh ghi điểm tuyệt đối", 0.0, 0.07),

    # Tin 19: giữ nguyên ảnh 19_2 đã cắt sạch badge Xinhua (1014x571 r=1.78)
    "Tin_19_2.jpg": ("local", str(IMG_DIR / "Tin_19_2.jpg"), "BING SEARCH", "Trận thắng 3-0 trước Getafe giúp Atletico Madrid ghi dấu ấn lịch sử cho Simeone", 0.0, 0.0),

    # Tin 20: thay 20_1/2/3/5 (fallback rác + thiếu) bằng ảnh U17 Tây Ban Nha & U17 Trung Quốc sạch
    "Tin_20_1.jpg": ("url", "https://assets.khelnow.com/news/uploads/2023/11/Spain.jpg", "KHELNOW / FIFA", "U17 Tây Ban Nha hủy diệt U17 Fiji 15-0 để sớm giành vé đi tiếp tại World Cup", 0.0, 0.0),
    "Tin_20_2.jpg": ("url", "https://en.people.cn/mediafile/pic/BIG/20260523/83/9991019555911945131.png", "PEOPLE / FIFA", "U17 Trung Quốc đánh rơi chiến thắng đáng tiếc trước U17 Ma Rốc ở giây cuối", 0.0, 0.0),
    "Tin_20_3.jpg": ("url", "https://images2.thanhnien.vn/zoom/1200_630/528068263637045248/2026/11/23/17954541622052055466824288530363592341489461183749101cef30f178f034e1df4bc905b0cc29-1795454174498201040016-7-0-572-1080-crop-1795454195803878173354.jpg", "THANH NIÊN / FIFA", "Đêm 23 tháng 11 trên đất Qatar ghi nhận những diễn biến trái ngược giữa các bảng đấu", 0.0, 0.0),
    "Tin_20_5.jpg": ("url", "https://english.news.cn/20260523/5671445236ef413783e84ffd80e15997/3cdf67762cc34520a00396a3feaf82d2.jpg", "XINHUA / FIFA", "Zhao Songyuan ghi cả hai bàn giúp U17 Trung Quốc dẫn trước Ma Rốc 2-0 đến phút 64", 0.0, 0.07),

    # Tin 21: thay 21_1/21_4 fallback rác & sửa trùng kề 21_2 == 21_3
    "Tin_21_1.jpg": ("url", "https://www.coxarchitecture.com.au/wp-content/uploads/2023/07/AUSvCAN-Women-00256-1980x1321.jpg", "FIFA WOMEN'S WORLD CUP", "Liên danh Mỹ, Mexico, Costa Rica và Jamaica chính thức giành quyền đăng cai World Cup nữ 2031", 0.0, 0.0),
    "Tin_21_3.jpg": ("local", str(ROOT / "outputs" / "23.11.2026" / "images" / "Tin_11_6.jpg"), "FIFA / ZURICH", "Cả 211 liên đoàn thành viên FIFA bỏ phiếu nhất trí tại phiên họp bất thường ở Thụy Sĩ", 0.0, 0.0),
    "Tin_21_4.jpg": ("url", "https://www.austadiums.com/news/images/WWCFinal23.jpg", "AUSTADIUMS / FIFA", "Châu Mỹ hợp lực tổ chức kỳ World Cup nữ có quy mô khán giả và doanh thu lớn chưa từng có", 0.0, 0.0),

    # Tin 22: thay 22_4 (dải mờ 2 bên) bằng ảnh cúp World Cup ngang sạch
    "Tin_22_4.jpg": ("local", str(IMG_DIR / "Tin_21_2.jpg"), "THANH NIÊN / REUTERS", "Đề án trị giá 20 tỷ USD nhắm vào nguồn thu khổng lồ của các kỳ World Cup tương lai", 0.0, 0.0),

    # Tin 23: thay 23_1 (Ronaldo), 23_3 (Castrol), 23_5 (phaplynhanh) bằng ảnh thật Dudu Georgescu
    "Tin_23_1.jpg": ("url", "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/23/edit-georgescu-1795418114327316242935-24-0-364-650-crop-17954181324621006829265.jpeg", "TUỔI TRẺ / ADEVARUL", "Chân dung huyền thoại bóng đá Romania Dudu Georgescu qua đời ở tuổi 76", 0.0, 0.0),
    "Tin_23_3.jpg": ("url", "https://img.spynews.ro/?u=https://spynews.ro/uploads/modules/news/0/2026/11/22/379807/whatsapp-image-20261122-at-115305.jpeg&w=1200", "SPYNEWS / ROMANIA", "Thông tin cái chết của cựu danh thủ tại Canada gây chấn động bóng đá Romania", 0.0, 0.0),
    "Tin_23_5.jpg": ("url", "https://www.gandul.ro/wp-content/uploads/2026/11/captura-de-ecran-2026-11-22-105437.png", "GANDUL / ROMANIA", "Kết quả khám nghiệm tử thi sẽ quyết định hướng điều tra hình sự của vụ án", 0.0, 0.0),

    # Tin 25: thay 25_4 (dải sky sports tennis) & 25_6 (ảnh Alcaraz không rõ mặt) bằng ảnh Sinner & Alcaraz nét
    "Tin_25_4.jpg": ("url", "https://www.nittoatpfinals.com/-/media/images/news/2024/01/28/12/44/sinner-australian-open-2024-sunday-final-celebration.jpg", "ATP TOUR", "Chấn thương gân đầu gối dai dẳng đã buộc anh phải bỏ qua Mỹ mở rộng và ATP Finals", 0.0, 0.0),
    "Tin_25_6.jpg": ("local", str(ROOT / "outputs" / "23.11.2026" / "images" / "Tin_12_1.jpg"), "DÂN TRÍ / AP", "Việc Sinner vắng mặt giúp Carlos Alcaraz trở thành ứng viên áp đảo tại Melbourne", 0.0, 0.0),

    # Tin 27: cắt badge Xinhua 27_4 & thay 27_5 (pingsunday watermark) bằng ảnh Shunsuke Togami vô địch WTT Muscat
    "Tin_27_4.jpg": ("local", str(IMG_DIR / "Tin_27_4.jpg"), "BING SEARCH", "Cả 19 tay vợt và tám đôi vận động viên Trung Quốc đều dừng bước trước trận cuối cùng", 0.0, 0.0),
    "Tin_27_5.jpg": ("url", "https://cdnmedia.webthethao.vn/wttstudio/media/public/23-11-2026/shunsuke-2.jpg", "WTT / WEBTHETHAO", "Shunsuke Togami thắng áp đảo Trần Viên Vũ trước khi vô địch đơn nam lẫn đôi nam nữ", 0.0, 0.0),

    # Tin 28: thay 28_5 (đồ họa vòng tròn) bằng ảnh golf PGA Tour RSM Classic sạch
    "Tin_28_5.jpg": ("url", "https://azat.tv/wp-content/uploads/2026/11/rsm-classic-golf-tournament.jpg", "PGA TOUR / AZAT", "Vòng cuối năm gậy âm giúp anh san bằng tổng điểm âm 16 với ba đối thủ nặng ký", 0.0, 0.0),

    # Tin 29: thay 29_12 (AutoAction logo) bằng ảnh Max Verstappen Las Vegas GP sạch
    "Tin_29_12.jpg": ("local", str(ROOT / "outputs" / "23.11.2026" / "images" / "Tin_13_1.jpg"), "THE GUARDIAN", "Max Verstappen ví cuộc đua nhiều pha vượt mặt tại Las Vegas giống trò chơi điện tử", 0.0, 0.0),
}

BACKUP_URLS: Dict[str, str] = {
    "Tin_03_1.jpg": "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/23/anh-chup-man-hinh-2026-11-24-010532-17954571641262045942428-33-0-366-636-crop-17954573664111417130924.png",
    "Tin_25_4.jpg": "https://sports.inquirer.net/files/2025/07/AP25194712006627-scaled.jpg",
    "Tin_28_5.jpg": "https://www.indystar.com/gcdn/authoring/authoring-images/2026/11/18/SGLF/92846906007-getty-images-2305739222.jpg?crop=5584,3142,x0,y290&width=3200&height=1801&format=pjpg&auto=webp",
}


def main() -> None:
    plan_path = OUT_DIR / "image_plan.json"
    credits_path = OUT_DIR / "image_credits.json"

    plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
    records: List[Dict[str, Any]] = plan_data["records"]
    credits_map: Dict[str, str] = json.loads(credits_path.read_text(encoding="utf-8"))

    for rec in records:
        fn = rec["file_name"]
        if fn not in REPLACEMENTS:
            continue
        kind, val, cred, desc, t_top, t_bot = REPLACEMENTS[fn]
        try:
            if kind == "local":
                im = load_local_img(Path(val))
            else:
                try:
                    im = download_img(val)
                except Exception:
                    if fn in BACKUP_URLS:
                        im = download_img(BACKUP_URLS[fn])
                    else:
                        raise
            if t_top > 0 or t_bot > 0:
                im = trim_edge_margins(im, top_frac=t_top, bottom_frac=t_bot)
            im.save(IMG_DIR / fn, format="JPEG", quality=95, optimize=True)
            rec["dimensions"] = f"{im.width}x{im.height} r={im.width / im.height:.2f}"
            rec["credit"] = cred
            rec["description"] = desc
            credits_map[fn] = cred
            print(f"[FIX] {fn}: {rec['dimensions']} | {cred}")
        except Exception as exc:
            print(f"[ERR] {fn}: {exc}")
            sys.exit(1)

    by_scene: Dict[int, List[Dict[str, Any]]] = {}
    for r in records:
        by_scene.setdefault(int(r["scene_id"]), []).append(r)

    for sid, recs in sorted(by_scene.items()):
        prev_h = None
        for r in recs:
            p = IMG_DIR / r["file_name"]
            with Image.open(p) as im:
                dh = compute_dhash(im)
            if prev_h is not None and hamming_dist(dh, prev_h) <= 4:
                print(f"[ADJ_DUP_WARN] Scene {sid:02d}: {r['file_name']} giống ảnh kề trước!")
            prev_h = dh

    plan_path.write_text(json.dumps(plan_data, ensure_ascii=False, indent=2), encoding="utf-8")
    credits_path.write_text(json.dumps(credits_map, ensure_ascii=False, indent=2), encoding="utf-8")

    # Tái dựng toàn bộ 30 bảng Contact Sheet + Overview
    p22.DAY_STR = DAY_STR
    p22.OUT_DIR = OUT_DIR
    p22.IMG_DIR = IMG_DIR
    p22.QA_DIR = QA_DIR

    all_specs = {int(sp["id"]): sp for sp in [d24.INTRO_DATA] + list(d24.NEWS_SPECS)}
    overview_records: List[Dict[str, Any]] = []
    for sid, recs in sorted(by_scene.items()):
        sp = all_specs[sid]
        is_intro = sid == 0
        vp = sp.get("voice_preset") or ("mixed" if is_intro else ("primary" if sid % 2 == 1 else "secondary"))
        vname, _ = p22.VOICE_INFO.get(vp, ("Minh Quân Pro", "male"))
        sheet_name = "contact_scene_00_intro.jpg" if is_intro else f"contact_scene_{sid:02d}.jpg"
        sheet_title = sp.get("group") or "MỞ ĐẦU" if is_intro else sp["title"]
        p22.render_scene_contact_sheet(
            sid,
            sheet_title,
            sp.get("news_source") or sp.get("source") or "",
            f"{vp} ({vname})",
            [{**r, "is_fallback": False} for r in recs],
            QA_DIR / sheet_name,
        )
        overview_records.extend(recs[:2])

    p22.render_overview_sheet(overview_records, len(d24.NEWS_SPECS), QA_DIR / "contact_overview.jpg")
    print(f"[ok] Đã hoàn tất QA fixes và tái dựng toàn bộ {len(by_scene)} bảng Contact Sheet + Overview.")


if __name__ == "__main__":
    main()
