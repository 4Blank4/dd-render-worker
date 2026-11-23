# -*- coding: utf-8 -*-
"""
apply_qa_fixes_23_11.py — Áp dụng kết quả kiểm duyệt thị giác 18 bảng Contact Sheet QA (23.11.2026):
  - Xử lý 2 ảnh thiếu & 8 ảnh fallback lạc đề/ảnh bảng cũ/ảnh screenshot.
  - Loại bỏ ảnh chứa graphic YouTube/TV (Sky Sports ATP/LPGA/Darts/F1 Australia) & logo ZNews.
  - Cắt gọn mép logo nhỏ (THANH NIÊN bottom 7% ở Tin #01, sky sports NFL bottom 11% ở Tin #17).
  - Loại bỏ toàn bộ trùng ảnh kề nhau trong cùng scene để đạt 0 lỗi & 0 cảnh báo qa_precheck.py.
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
import daily_23_11_data as d23

DAY_STR = "23.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
IMG_DIR = OUT_DIR / "images"
QA_DIR = OUT_DIR / "qa"
CACHE_DIR = Path(paths.WORK) / "img_cache_23_11"


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


# Bảng thay thế chính xác từng slot đã soi trên Contact Sheet:
# Key = filename ("Tin_XX_Y.jpg") -> (source_kind, source_val, credit, desc, trim_top, trim_bottom)
REPLACEMENTS: Dict[str, Tuple[str, str, str, str, float, float]] = {
    # Intro: thay SKY_ATP_1 (chứa bảng text Sky Sports) bằng ảnh nâng cúp sạch VnExpress
    "Tin_00_3.jpg": ("url", d23.VNE_ATP_1, "VNEXPRESS / AP", "Carlos Alcaraz nâng cúp vô địch ATP Finals 2026 lần đầu tiên trong sự nghiệp", 0.0, 0.0),

    # Tin 01: tránh trùng kề [T] Tin_01_2 == [S1] Tin_01_4, cắt logo THANH NIÊN mép dưới, đổi Tin_01_12 khác Tin_01_5
    "Tin_01_4.jpg": ("url", d23.DT_BOI_AV, "DÂN TRÍ", "Hàng loạt kỷ lục quốc gia và Đại hội được thiết lập ngay tối 22 tháng 11", 0.0, 0.0),
    "Tin_01_9.jpg": ("url", d23.TN_BOI_2, "THANH NIÊN", "Watson Nguyễn khẳng định đẳng cấp nhà vô địch 50m ếch quốc gia Mỹ", 0.0, 0.07),
    "Tin_01_11.jpg": ("url", d23.TN_BOI_3, "THANH NIÊN", "Kình ngư trẻ Nguyễn Thúy Hiền xô đổ cả kỷ lục quốc gia lẫn đại hội ở cự ly 50m ếch nữ", 0.0, 0.07),
    "Tin_01_12.jpg": ("url", d23.TT_BOI_MT, "TUỔI TRẺ", "Lần đầu tiên sau nhiều năm nội dung 100m tự do nam chứng kiến hai VĐV cùng đoạt HCV", 0.0, 0.0),

    # Tin 02: thay thế 3 fallback lạc đề (bảng cũ 19/11, vovinam trẻ, xe mô tô diễu binh) bằng ảnh Đại hội 2026 thật & ảnh 171721 của Phạm Văn Mách
    "Tin_02_1.jpg": ("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/22/tnw-17952685381277103495586065056191g37645463608123056850739556e5830c0844433496a6caae259-1795324791237286460172.jpg", "THANH NIÊN", "Ngày hội thể thao lớn nhất cả nước sôi động tại TP.HCM tối 22 tháng 11", 0.0, 0.0),
    "Tin_02_4.jpg": ("local", str(ROOT / "outputs" / "22.11.2026" / "images" / "Tin_01_1.jpg"), "THANH NIÊN", "Canoeing và vovinam đóng góp gần một nửa số HCV của đoàn TP.HCM", 0.0, 0.0),
    "Tin_02_5.jpg": ("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/22/tnw-1795270330166612143628429328725g376454636081230568524a674fe6e853cb23c2dfaf8578b4e36-17953247915141738866178.jpg", "THANH NIÊN", "Hà Nội, Công an Nhân dân và Quân Đội bám đuổi quyết liệt trong nhóm đầu", 0.0, 0.0),
    "Tin_02_8.jpg": ("url", d23.TN_MACH_1, "THANH NIÊN", "Lực sĩ sinh năm 1976 Phạm Văn Mách giành HCB trước đối thủ trẻ Phạm Văn Phước", 0.0, 0.0),

    # Tin 06: sửa trùng kề Tin_06_4 == Tin_06_5 bằng ảnh Lê Quang Liêm ở Budapest ngày 22.11
    "Tin_06_5.jpg": ("local", str(ROOT / "outputs" / "22.11.2026" / "images" / "Tin_08_1.jpg"), "VNEXPRESS", "Jerusalem Masters 2026 là cuộc đọ trí của 12 kỳ thủ hàng đầu thế giới", 0.0, 0.0),

    # Tin 09: sửa trùng kề Tin_09_3 == Tin_09_4 bằng ảnh Yamal/Barca góc khác
    "Tin_09_4.jpg": ("url", d23.VNE_BAR_2, "VNEXPRESS / AFP", "Trận đấu trên sân Spotify Camp Nou diễn ra cởi mở với năm bàn thắng được ghi", 0.0, 0.0),

    # Tin 10: thay Tin_10_6 bằng ảnh AC Milan thắng Frosinone 5-1 & sửa trùng kề Tin_10_7 == Tin_10_8
    "Tin_10_6.jpg": ("url", "https://assets-eu-01.kc-usercontent.com:443/006f7528-416b-01e4-8ef2-ab6ab3f4e177/bc13eb8b-2f70-469a-9842-79d2d0123b84/MilanFrosinone_12.jpg", "AC MILAN", "AC Milan thắng đậm Frosinone 5-1 còn Juventus vượt qua Venezia 4-0", 0.0, 0.0),
    "Tin_10_8.jpg": ("local", str(ROOT / "outputs" / "22.11.2026" / "images" / "Tin_15_1.jpg"), "SKY SPORTS", "Trước Doué, nhà vô địch nước Pháp cũng mất Khvicha Kvaratskhelia vì chấn thương", 0.0, 0.0),

    # Tin 11: thay ảnh fallback sai U17 VN, thay ảnh thiếu, xóa ảnh chụp web FIFA, sửa trùng kề NWSL
    "Tin_11_1.jpg": ("url", "https://assets.the-afc.com/2023_AFC_U17_Asian_Cup/Finals/Matches/Q-finals/Thailand_v_Korea_Republic/Match/AFC-U17-ASIAN-CUP-2023---Post-Match-(4).jpg", "AFC / FIFA", "U17 Hàn Quốc áp đảo hoàn toàn để sớm giành quyền vào vòng knock-out World Cup", 0.0, 0.0),
    "Tin_11_4.jpg": ("url", "https://assets.khelnow.com/news/uploads/2023/11/South-Korea.jpg", "KFA / FIFA", "Kim Ji-woo ghi ba bàn đưa U17 Hàn Quốc đạt sáu điểm tuyệt đối đứng đầu bảng B", 0.0, 0.0),
    "Tin_11_5.jpg": ("url", "https://assets.goal.com/images/v3/blta2461cff8ac7dde5/South+Korea.jpg", "GOAL / FIFA", "Saudi Arabia tạo cú sốc khi hạ U17 Pháp 1-0 còn Argentina thắng Mozambique 2-1", 0.0, 0.0),
    "Tin_11_8.jpg": ("url", "https://footballgroundguide.com/thumbor/iWbflubpyStbY9doONwNtR0x56Q=/2507x2006/smart/filters:format(webp)/https://media.footballgroundguide.com/main/2026/11/imago1076069568h.jpg", "FIFA / WEMBLEY", "Vương quốc Anh kỳ vọng tạo kỳ World Cup nữ bùng nổ khán giả vào năm 2035", 0.0, 0.0),

    # Tin 12: xóa 2 ảnh bảng graphic Sky Sports ATP Highlights
    "Tin_12_1.jpg": ("url", d23.DT_ATP_2, "DÂN TRÍ / AP", "Carlos Alcaraz lần đầu bước lên bục vinh quang tại ATP Finals ở Turin", 0.0, 0.0),
    "Tin_12_7.jpg": ("url", d23.DT_ATP_1, "DÂN TRÍ / AP", "Danh hiệu ATP Finals bổ sung mảnh ghép còn thiếu vào bộ sưu tập đồ sộ của Alcaraz", 0.0, 0.0),

    # Tin 13: thay ảnh Australian GP 2026 text card bằng xe F1 Max Verstappen Las Vegas; sửa trùng kề Ferrari Tin_13_6 == Tin_13_7
    "Tin_13_4.jpg": ("url", "https://motorcyclesports.net/wp-content/uploads/2026/11/max-verstappen-wins-las-vegas-grand-prix-after-intense-50-lap-battle-1024x683.webp", "MOTORCYCLE SPORTS", "Đường đua tốc độ cao tại Las Vegas chứng kiến 35 lần đổi ngôi đầu nghẹt thở", 0.0, 0.0),
    "Tin_13_7.jpg": ("url", "https://cdn-1.motorsport.com/images/mgl/63QaDqb2/s1000/lewis-hamilton-ferrari-charles.jpg", "MOTORSPORT", "Lãnh đội Fred Vasseur triệu tập gấp cuộc họp khẩn phê bình Charles Leclerc", 0.0, 0.0),

    # Tin 15: xóa 2 ảnh bảng graphic Sky Sports Golf, sửa trùng kề Tarik Skubal
    "Tin_15_3.jpg": ("url", "https://bostonglobe-prod.cdn.arcpublishing.com/resizer/v2/6YUQSHUFKNE2XDPKH246NVIDSU.jpg?auth=3cff3a03bb8ff76d474ebf8fdccc696ddd20d3961d90b477353ff1a6ec4d5ac1&width=1440", "LPGA", "Hai môn thể thao đỉnh cao cùng chứng kiến những con số tiền thưởng choáng ngợp", 0.0, 0.0),
    "Tin_15_4.jpg": ("url", "https://www.lpga.com/-/media/images/lpga/tournaments/lpga-mediheal-championship/2022/rd1/thitikula_1431166442_2000x1124.jpg?h=1125&la=en&w=2000&hash=4FA21B9EF7B3352559DBB1C998A0FEEEFEE79BFA", "LPGA", "Vòng cuối 65 gậy không lỗi bogey giúp Thitikul bỏ xa các đối thủ bám đuổi", 0.0, 0.0),
    "Tin_15_6.jpg": ("url", "https://www.mlive.com/resizer/v2/ETORSHCJVVARTB4NWRDWAKDAK4.jpg?auth=9f4e700680c046c0634f60bfc4ddbd94d138cb892aa341ba84fab9a89145473a&width=1280&smart=true", "MLIVE / AP", "New York Mets kích nổ bom tấn chiêu mộ ngôi sao ném bóng từng hai lần đoạt Cy Young", 0.0, 0.0),

    # Tin 16: thay ảnh logo Znews, thay ảnh Enzo nhầm thành Paredes, sửa thiếu 16_6, xóa bảng graphic Darts 16_8
    "Tin_16_2.jpg": ("url", d23.VNE_NEY_2, "VNEXPRESS / AP", "Tiền đạo Neymar bất ngờ giành chức vô địch giải poker BSOP Millions", 0.0, 0.0),
    "Tin_16_5.jpg": ("url", "https://www.rtl.de/img/31563509/1795342582/c16_9/2304/leandro-paredes-of-argentinas-boca-juniors-holds-up-the-trophy-as-he-celebrates-after-winning-the-copa-sudamericana-final-soccer-match-against-brazils-atletico-mineiro-in-barranquilla-colombia-saturday-nov-21-2026ap-photofernando-vergara.webp", "AP PHOTO", "Trước đó, cựu tiền vệ tuyển Argentina vừa cùng Boca Juniors nâng cao cúp Nam Mỹ", 0.0, 0.0),
    "Tin_16_6.jpg": ("url", "https://altavoz.pe/wp-content/uploads/2026/04/boca.jpg", "BOCA JUNIORS", "Paredes nhanh chóng đăng ảnh từ phòng khám trấn an người hâm mộ rằng mình đã ổn", 0.0, 0.0),
    "Tin_16_7.jpg": ("url", "https://irishpokeropen.com/wp-content/uploads/2026/03/30_Deaf_High_Roller_Final_Table_MOB-2.jpg", "POKER HIGH ROLLER", "Neymar đánh bại người bạn thân Gilmar Araújo để nhận 380000 real tại São Paulo", 0.0, 0.0),
    "Tin_16_8.jpg": ("url", "https://i2-prod.mirror.co.uk/article36408123.ece/ALTERNATES/s1200f/0_Price.jpg", "MIRROR", "Gerwyn Price vượt qua Gian van Veen để hướng thẳng tới Giải vô địch thế giới", 0.0, 0.0),

    # Tin 17: cắt dải "sky sports NFL" 11% mép dưới cho Tin_17_2 & Tin_17_9
    "Tin_17_2.jpg": ("url", d23.SKY_NFL_MET, "SKY SPORTS", "Ngôi sao NFL DK Metcalf bị truất quyền thi đấu sau tình huống va chạm căng thẳng", 0.0, 0.11),
    "Tin_17_9.jpg": ("url", d23.SKY_NFL_MET, "SKY SPORTS", "Cầu thủ DK Metcalf bị trọng tài đuổi khỏi sân vì va chạm với Cooper DeJean của Eagles", 0.0, 0.11),
}

# Fallback thay thế cho Tin_11_8 nếu footballgroundguide tiếp tục chặn HTTP:
BACKUP_URLS: Dict[str, str] = {
    "Tin_11_8.jpg": "https://thefa.shorthandstories.com/all-together/assets/SPvCanLRIB/fa-updated-title-cover-1.png",
}


def main() -> None:
    plan_path = OUT_DIR / "image_plan.json"
    credits_path = OUT_DIR / "image_credits.json"
    thethao_path = OUT_DIR / "thethao.json"
    intro_path = OUT_DIR / "intro_hook.json"

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

    # Kiểm tra chắc chắn không còn ảnh kề nhau trùng dHash trong cùng scene
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

    # Cập nhật lại toàn bộ QA Contact Sheets cho từng scene + overview
    p22.DAY_STR = DAY_STR
    p22.OUT_DIR = OUT_DIR
    p22.IMG_DIR = IMG_DIR
    p22.QA_DIR = QA_DIR

    all_specs = {int(sp["id"]): sp for sp in [d23.INTRO_DATA] + list(d23.NEWS_SPECS)}
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

    p22.render_overview_sheet(overview_records, len(d23.NEWS_SPECS), QA_DIR / "contact_overview.jpg")
    print(f"[ok] Đã hoàn tất QA fixes và tái dựng toàn bộ {len(by_scene)} bảng Contact Sheet + Overview.")


if __name__ == "__main__":
    main()
