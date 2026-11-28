# -*- coding: utf-8 -*-
"""
apply_qa_fixes_28_11.py — Thay thế toàn bộ ảnh đồ họa/watermark/lạc đề/trùng lặp
được phát hiện qua kiểm duyệt trực quan Contact Sheets ngày 28.11.2026,
cắt viền logo Thanh Niên (7%), dựng lại Contact Sheets và bộ 3 Thumbnail.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "core") not in sys.path:
    sys.path.insert(0, str(ROOT / "core"))

from PIL import Image
from core.diemdoc import paths
from core.diemdoc.image_curator import trim_edge_margins
from build_thumbnails_09_11 import render_thumbnails
import daily_28_11_data as d28
import prepare_daily_22_11 as p22
import prepare_daily_28_11 as p28

DAY_STR = "28.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
IMG_DIR = OUT_DIR / "images"
QA_DIR = OUT_DIR / "qa"

# Ảnh cần cắt mép dưới 7% để loại bỏ logo góc dưới phải Thanh Niên
TRIM_BOTTOM: Dict[str, float] = {
    "Tin_00_9.jpg": 0.07,
    "Tin_00_10.jpg": 0.07,
    "Tin_07_1.jpg": 0.07,
    "Tin_07_2.jpg": 0.07,
    "Tin_07_6.jpg": 0.07,
    "Tin_09_5.jpg": 0.07,
    "Tin_22_8.jpg": 0.07,
}

# Các slot cần thay thế ảnh sạch thực tế
REPLACEMENTS: Dict[str, Tuple[List[Tuple[str, str]], str, str]] = {
    "Tin_00_13.jpg": (
        [("url", d28.VNE_ALONSO_SAD)],
        "VNEXPRESS / AFP",
        "Huấn luyện viên Xabi Alonso đối mặt áp lực nặng nề sau thất bại thứ ba liên tiếp",
    ),
    "Tin_02_2.jpg": (
        [("ddgs", "Alexandre Polking football coach touchline"), ("url", d28.DT_ND_CAHN_1)],
        "BING SEARCH",
        "Huấn luyện viên Alexandre Polking phản bác thông tin sai sự thật về học trò",
    ),
    "Tin_02_5.jpg": (
        [("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/26/edit-92656265416838212167530973135923093449342200n-17957200933501828764139.jpeg")],
        "THANH NIÊN / CAHN",
        "Quang Hải được khẳng định vẫn còn nguyên động lực cống hiến cho tuyển Việt Nam",
    ),
    "Tin_05_1.jpg": (
        [("ddgs", "Japan national football team match celebration World Cup")],
        "BING SEARCH",
        "U17 Nhật Bản thắng đậm 7-0 trước Honduras để tiến vào vòng 32 đội",
    ),
    "Tin_05_5.jpg": (
        [("url", "https://cdn2.tuoitre.vn/zoom/1200_630/471584752817336320/2026/11/26/u17-trung-quoc-17957132157511041881646-236-0-1576-2560-crop-1795713404350551355070.jpg")],
        "TUỔI TRẺ / FIFA",
        "Bóng đá châu Á có tới bảy đại diện góp mặt trong nhóm 32 đội mạnh nhất",
    ),
    "Tin_07_3.jpg": (
        [("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/26/tnw-17956953955334951488922155853666495148892215585366606a91f4ea75bfd24220eefc4b65a5fdb-17956966203121345646888.jpg")],
        "THANH NIÊN / ĐỘC LẬP",
        "Bầu không khí sôi động trong ngày thi đấu cuối cùng môn bơi tại CLB Phú Thọ",
    ),
    "Tin_08_4.jpg": (
        [("ddgs", "Nguyen Thi Oanh Vietnam athletics running")],
        "BING SEARCH",
        "Bùi Thị Nguyên bứt phá giành huy chương vàng và phá kỷ lục Đại hội 100m rào",
    ),
    "Tin_09_6.jpg": (
        [("url", "https://images2.thanhnien.vn/528068263637045248/2026/11/26/tnw-17956944670954951488922155853666495148892215585366655081506d30693d7eb426f98d830a4d8-17956966202911744353271.jpg")],
        "THANH NIÊN / ĐỘC LẬP",
        "Khoảng cách giữa Thành phố Hồ Chí Minh và Hà Nội được nới rộng lên 20 HCV",
    ),
    "Tin_10_5.jpg": (
        [("url", d28.SKY_CHELSEA_ALONSO)],
        "SKY SPORTS",
        "Cú đúp của Emmanuel Emegha không đủ giúp Chelsea thoát khỏi trắng tay",
    ),
    "Tin_11_3.jpg": (
        [("url", d28.DT_CHELSEA_GLOOM)],
        "DÂN TRÍ / GETTY",
        "Nội bộ Chelsea đối mặt sóng gió lớn sau chuỗi ba trận toàn thua",
    ),
    "Tin_12_2.jpg": (
        [("ddgs", "Bruno Fernandes Manchester United captain celebration")],
        "BING SEARCH",
        "Đội trưởng 32 tuổi vẫn là hạt nhân lối chơi không thể thay thế tại Old Trafford",
    ),
    "Tin_12_3.jpg": (
        [("ddgs", "Old Trafford stadium Manchester United Premier League")],
        "BING SEARCH",
        "Manchester United kích hoạt điều khoản gia hạn hợp đồng với Bruno Fernandes",
    ),
    "Tin_12_6.jpg": (
        [("ddgs", "Mauricio Pochettino football coach press conference")],
        "BING SEARCH",
        "Huấn luyện viên Mauricio Pochettino cần sự ổn định từ thủ quân để vực dậy đội bóng",
    ),
    "Tin_14_1.jpg": (
        [("ddgs", "Savinho Savio Brazil football match")],
        "BING SEARCH",
        "Savio đối mặt nguy cơ ngồi ngoài tới 80 ngày vì tái phát chấn thương",
    ),
    "Tin_14_5.jpg": (
        [("ddgs", "football soccer player injured on pitch match")],
        "BING SEARCH",
        "Chấn thương gân kheo dai dẳng khiến quá trình hồi phục bị kéo dài",
    ),
    "Tin_14_6.jpg": (
        [("ddgs", "Roberto De Zerbi Brighton touchline match")],
        "BING SEARCH",
        "Chiến lược gia người Italy phải tìm phương án thay thế trong ít nhất hai tháng tới",
    ),
    "Tin_16_5.jpg": (
        [("ddgs", "Werder Bremen football team celebration Bundesliga")],
        "BING SEARCH",
        "Werder Bremen bùng nổ cuối trận để giật lại một điểm kịch tính",
    ),
    "Tin_17_1.jpg": (
        [("ddgs", "Marc Marquez Ducati MotoGP racing track")],
        "BING SEARCH",
        "Marc Márquez tuyên bố chia tay MotoGP sau mùa giải 2026 trên đỉnh vinh quang",
    ),
    "Tin_17_6.jpg": (
        [("ddgs", "Marc Marquez helmet waving MotoGP paddock")],
        "BING SEARCH",
        "Chặng Valencia cuối tuần này sẽ là lần cuối người hâm mộ thấy số 93 thi đấu",
    ),
    "Tin_18_1.jpg": (
        [("ddgs", "Mercedes F1 Formula 1 car night track")],
        "BING SEARCH",
        "Các xe đua Formula 1 bước vào ngày chạy thử nóng bỏng tại Qatar Grand Prix",
    ),
    "Tin_18_2.jpg": (
        [("ddgs", "Kimi Antonelli Formula 1 Mercedes driver")],
        "BING SEARCH",
        "Kimi Antonelli thể hiện tốc độ vượt trội để dẫn đầu cả hai phiên tập tại Losail",
    ),
    "Tin_18_6.jpg": (
        [("ddgs", "Lewis Hamilton Ferrari Formula 1 driver")],
        "BING SEARCH",
        "Lewis Hamilton đối diện nguy cơ nhận án phạt sau sự cố kỹ thuật cuối ngày",
    ),
    "Tin_19_1.jpg": (
        [("ddgs", "Tyson Fury boxing heavyweight fighter ring")],
        "BING SEARCH",
        "Tyson Fury nhận giấy phép y tế để bước vào trận đấu mong chờ với Anthony Joshua",
    ),
    "Tin_21_5.jpg": (
        [("ddgs", "Luiz Felipe Scolari football manager coach")],
        "BING SEARCH",
        "Cựu huấn luyện viên Luiz Felipe Scolari là ứng viên giàu ý nghĩa cho trận chia tay",
    ),
    "Tin_21_6.jpg": (
        [("url", "https://i1-thethao.vnecdn.net/2026/11/27/2010-10-05T120000Z-561254099-G-3224-5595-1795760466.jpg?w=0&h=0&q=100&dpr=1&fit=crop&s=jxO_4Y80F_JPNnEyTMl0Fw")],
        "VNEXPRESS / REUTERS",
        "Pep Guardiola lần đầu trải lòng sau khi rời Man City trên kênh Romario TV",
    ),
}


def main() -> None:
    p22.DAY_STR = DAY_STR
    p22.OUT_DIR = OUT_DIR
    p22.IMG_DIR = IMG_DIR
    p22.QA_DIR = QA_DIR
    p22.CACHE_DIR = Path(paths.WORK) / "img_cache_28_11"

    curator = p22.ImageCurator22()
    plan_p = OUT_DIR / "image_plan.json"
    credits_p = OUT_DIR / "image_credits.json"
    plan_data = json.loads(plan_p.read_text(encoding="utf-8"))
    credits_map = json.loads(credits_p.read_text(encoding="utf-8"))
    records = plan_data.get("records", [])

    touched_scenes = set()

    for rec in records:
        fn = rec["file_name"]
        sid = int(rec["scene_id"])

        if fn in REPLACEMENTS:
            srcs, new_credit, new_desc = REPLACEMENTS[fn]
            slot = {"type": rec["type"], "sentence_idx": rec["sentence_idx"], "sources": srcs, "credit": new_credit, "desc": new_desc}
            img, src_info, is_fb = curator.acquire_slot(sid, int(rec["index"]), slot)
            if img is None:
                raise RuntimeError(f"Không lấy được ảnh thay thế cho {fn}: {src_info}")
            if is_fb:
                print(f"[WARN] {fn} dùng fallback: {src_info}")
            fp = IMG_DIR / fn
            img.save(fp, format="JPEG", quality=95, optimize=True)
            rec["dimensions"] = f"{img.width}x{img.height} r={img.width / img.height:.2f}"
            rec["credit"] = new_credit
            rec["description"] = new_desc
            credits_map[fn] = new_credit
            touched_scenes.add(sid)
            print(f"[replace] {fn} -> {src_info} ({rec['dimensions']})")

        if fn in TRIM_BOTTOM:
            fp = IMG_DIR / fn
            with Image.open(fp) as im:
                cropped = trim_edge_margins(im.convert("RGB"), top_frac=0.0, bottom_frac=TRIM_BOTTOM[fn])
            cropped.save(fp, format="JPEG", quality=95, optimize=True)
            rec["dimensions"] = f"{cropped.width}x{cropped.height} r={cropped.width / cropped.height:.2f}"
            touched_scenes.add(sid)
            print(f"[trim] {fn} -> {rec['dimensions']}")

    plan_p.write_text(json.dumps(plan_data, ensure_ascii=False, indent=2), encoding="utf-8")
    credits_p.write_text(json.dumps(credits_map, ensure_ascii=False, indent=2), encoding="utf-8")

    # Cập nhật credit trong intro_hook.json & thethao.json nếu có ảnh đầu đại diện đổi nguồn
    all_specs = {int(sp["id"]): sp for sp in [d28.INTRO_DATA] + list(d28.NEWS_SPECS)}
    by_scene = {}
    for r in records:
        by_scene.setdefault(int(r["scene_id"]), []).append(r)

    overview_records = []
    for sid, recs in sorted(by_scene.items()):
        overview_records.extend(recs[:2])
        if sid in touched_scenes:
            sp = all_specs[sid]
            is_intro = sid == 0
            vp = sp.get("voice_preset") or ("mixed" if is_intro else ("primary" if sid % 2 == 1 else "secondary"))
            vname, _ = p22.VOICE_INFO.get(vp, ("Minh Quân Pro", "male"))
            sheet_name = "contact_scene_00_intro.jpg" if is_intro else f"contact_scene_{sid:02d}.jpg"
            sheet_title = sp.get("group") or "MỞ ĐẦU BẢN TIN" if is_intro else sp["title"]
            p22.render_scene_contact_sheet(
                sid,
                sheet_title,
                sp.get("news_source") or sp.get("source") or "",
                f"{vp} ({vname})",
                [{**r, "is_fallback": False} for r in recs],
                QA_DIR / sheet_name,
            )

    p22.render_overview_sheet(overview_records, len(d28.NEWS_SPECS), QA_DIR / "contact_overview.jpg")
    render_thumbnails(DAY_STR)
    print(f"[ok] Đã cập nhật xong {len(touched_scenes)} cảnh và re-render 3 thumbnail.")


if __name__ == "__main__":
    main()
