# -*- coding: utf-8 -*-
"""
apply_qa_fixes_20_11.py — Áp dụng danh sách ảnh thay thế đã kiểm duyệt thị giác 100%,
cắt gọn viền logo góc trên một số ảnh báo chí, cập nhật toàn bộ JSON/TXT và tái dựng Contact Sheets.
"""

from __future__ import annotations

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

import prepare_daily_20_11 as prep20

DAY_STR = "20.11.2026"
OUT_DIR = ROOT / "outputs" / DAY_STR
IMG_DIR = OUT_DIR / "images"
QA_DIR = OUT_DIR / "qa"
CAND_DIR = Path("/Users/phamminhtrieu/Library/Caches/DiemDoc/cand_20_11")
DAILY_19 = ROOT / "outputs" / "19.11.2026" / "images"

DANTRI_ROLAND_URL = (
    "https://cdnphoto.dantri.com.vn/4Cuf32eXO9QCnN8ZFcmVpXY3izo=/"
    "thumb_w/1020/2026/11/20/img20241025220807-1795107878353.jpg"
)
DANTRI_U17_URL = (
    "https://cdnphoto.dantri.com.vn/9PZ1SjETABnX-qiDZeMuByrp14U=/"
    "thumb_w/980/2026/11/20/afc-nhac-ve-dieu-dac-biet-cua-u17-viet-nam-"
    "khi-tham-du-world-cup-edited-1795063901561-1795112350977.jpg"
)

# (scene_id, 1-based slot_idx) -> (source_spec, optional new credit)
# source_spec: Path (copy), str URL, or ("SELF", "Tin_XX_Y.jpg")
REPLACEMENTS: Dict[Tuple[int, int], Tuple[Any, Optional[str]]] = {
    # Scene 00 Intro
    (0, 15): (("SELF", "Tin_16_1.jpg"), "TUỔI TRẺ"),
    (0, 16): (CAND_DIR / "zverev_2__1.jpg", "ATP TOUR"),
    # Scene 01 CAHN 1-3 JDT
    (1, 4): (DAILY_19 / "Tin_04_5.jpg", "THANH NIÊN"),
    (1, 14): (CAND_DIR / "jdt_team__1.jpg", "AFC"),
    (1, 15): (DAILY_19 / "Tin_04_1.jpg", "THANH NIÊN"),
    (1, 16): (("SELF", "Tin_03_7.jpg"), "THANH NIÊN"),
    (1, 17): (DAILY_19 / "Tin_01_18.jpg", "DÂN TRÍ"),
    # Scene 02 Shopee Cup
    (2, 6): (CAND_DIR / "port_asean.jpg", "ASEAN FOOTBALL"),
    (2, 12): (DAILY_19 / "Tin_03_2.jpg", "THANH NIÊN"),
    (2, 14): (CAND_DIR / "tampines__1.jpg", "AFC"),
    # Scene 03 Quốc Cường / Olaha / Kim Sang-sik
    (3, 1): (DAILY_19 / "Tin_03_10.jpg", "THANH NIÊN"),
    (3, 4): (DAILY_19 / "Tin_03_12.jpg", "THANH NIÊN"),
    (3, 5): (DAILY_19 / "Tin_03_14.jpg", "THANH NIÊN"),
    (3, 9): (CAND_DIR / "olaha__1.jpg", "BÓNG ĐÁ PLUS"),
    (3, 10): (CAND_DIR / "hong_phuc__2.jpg", "VFF"),
    (3, 12): (DAILY_19 / "Tin_02_11.jpg", "VFF"),
    # Scene 04 V-League R8
    (4, 2): (DAILY_19 / "Tin_18_9.jpg", "TUỔI TRẺ"),
    (4, 3): (CAND_DIR / "cong_phuong__1.jpg", "THANH NIÊN"),
    (4, 5): (CAND_DIR / "thanh_hoa_vne.jpg", "VNEXPRESS"),
    (4, 9): (DAILY_19 / "Tin_18_10.jpg", "TUỔI TRẺ"),
    (4, 12): (CAND_DIR / "hoang_duc_tn2.jpg", "THANH NIÊN"),
    (4, 13): (CAND_DIR / "cong_phuong__2.jpg", "THANH NIÊN"),
    (4, 14): (CAND_DIR / "kewell_vne.jpg", "VNEXPRESS"),
    # Scene 05 U17 VN vs Bỉ
    (5, 11): (DANTRI_ROLAND_URL, "DÂN TRÍ / VFF"),
    (5, 15): (DANTRI_U17_URL, "DÂN TRÍ / AFC"),
    # Scene 06 U17 Bỉ
    (6, 9): (CAND_DIR / "belgium_u17__1.jpg", "RBFA / UEFA"),
    # Scene 07 U17 Australia 2-0 U17 Argentina
    (7, 2): (CAND_DIR / "joeys_u17.jpg", "FOOTBALL AUSTRALIA"),
    (7, 3): (CAND_DIR / "akon_aus_cover.jpg", "THANH NIÊN / FIFA"),
    (7, 4): (DAILY_19 / "Tin_00_8.jpg", "THANH NIÊN / FIFA"),
    (7, 5): (CAND_DIR / "argentina_u17__2.jpg", "FIFA"),
    (7, 8): (CAND_DIR / "carl_veart_aus.jpg", "FOOTBALL AUSTRALIA"),
    (7, 9): (("SELF", "Tin_07_1.jpg"), "TUỔI TRẺ / AUSTRALIA FOOTBALL"),
    (7, 12): (CAND_DIR / "korea_u17__2.jpg", "KFA / FIFA"),
    (7, 13): (CAND_DIR / "uruguay_u17__1.jpg", "AUF / FIFA"),
    (7, 14): (CAND_DIR / "france_u17__2.jpg", "FFF"),
    # Scene 08 Man Utd Flycam & Mbeumo
    (8, 4): (DAILY_19 / "Tin_09_1.jpg", "VNEXPRESS / MAN UTD"),
    (8, 15): (CAND_DIR / "amad_diallo__2.jpg", "REUTERS"),
    # Scene 09 MLS Salary & Nico Paz
    (9, 7): (CAND_DIR / "lewandowski__2.jpg", "REUTERS"),
    (9, 8): (CAND_DIR / "son_heung_min__2.jpg", "AP PHOTO"),
    (9, 13): (CAND_DIR / "nico_paz__1.jpg", "SERIE A"),
    # Scene 10 Real Madrid Tchouameni & Courtois
    (10, 2): (CAND_DIR / "courtois_save.jpg", "REAL MADRID"),
    (10, 3): (CAND_DIR / "real_madrid_squad__1.jpg", "REUTERS"),
    (10, 8): (CAND_DIR / "tchouameni_2__2.jpg", "AP PHOTO"),
    (10, 9): (CAND_DIR / "arda_guler__1.jpg", "REUTERS"),
    (10, 10): (CAND_DIR / "bellingham__2.jpg", "REAL MADRID"),
    (10, 11): (CAND_DIR / "arda_guler__2.jpg", "REAL MADRID"),
    (10, 12): (("SELF", "Tin_10_2.jpg"), "AP PHOTO"),
    (10, 13): (CAND_DIR / "real_madrid_squad__2.jpg", "UEFA"),
    # Scene 11 Nhà Esposito
    (11, 4): (CAND_DIR / "esposito_pio__1.jpg", "GAZZETTA DELLO SPORT"),
    (11, 5): (CAND_DIR / "esposito_seb__1.jpg", "SERIE A"),
    (11, 11): (CAND_DIR / "baresi_duo__2.jpg", "SERIE A"),
    (11, 12): (CAND_DIR / "italy_nt__2.jpg", "FIGC"),
    (11, 13): (CAND_DIR / "brescia_stadium__2.jpg", "FIGC"),
    # Scene 12 Cassano & Pique
    (12, 5): (CAND_DIR / "gerard_pique__2.jpg", "LA LIGA"),
    (12, 10): (CAND_DIR / "tenerife_stadium__2.jpg", "LA LIGA 2"),
    (12, 13): (CAND_DIR / "gerard_pique__1.jpg", "RFEF"),
    # Scene 13 Mudryk & Ecuador
    (13, 5): (CAND_DIR / "mudryk_ukraine__1.jpg", "UAF"),
    (13, 7): (CAND_DIR / "mudryk_club__1.jpg", "PREMIER LEAGUE"),
    (13, 8): (CAND_DIR / "cas_lausanne__1.jpg", "CAS"),
    (13, 9): (CAND_DIR / "referee_red_card__2.jpg", "FEF"),
    (13, 12): (CAND_DIR / "fifa_zurich__2.jpg", "FIFA"),
    # Scene 14 Alireza Beiranvand
    (14, 2): (CAND_DIR / "beiranvand_1__2.jpg", "AFC"),
    (14, 3): (CAND_DIR / "lee_kang_in__2.jpg", "AFC"),
    (14, 5): (CAND_DIR / "beiranvand_2__1.jpg", "REUTERS"),
    (14, 6): (CAND_DIR / "beiranvand_2__2.jpg", "AFC"),
    (14, 8): (CAND_DIR / "de_bruyne__1.jpg", "REUTERS"),
    (14, 10): (CAND_DIR / "lee_kang_in__1.jpg", "KFA / REUTERS"),
    # Scene 15 Sân Thống Nhất & Khai mạc
    (15, 15): (CAND_DIR / "vn_shooting__1.jpg", "CỤC TDTT"),
    # Scene 18 Làng cờ
    (18, 2): (CAND_DIR / "xiangqi_pair__1.jpg", "TUỔI TRẺ / CTNN"),
    (18, 6): (CAND_DIR / "lai_ly_huynh__1.jpg", "TUỔI TRẺ"),
    (18, 7): (CAND_DIR / "lai_ly_huynh__2.jpg", "LĐCTVN"),
    (18, 13): (CAND_DIR / "harry_kane_chess__1.jpg", "REUTERS"),
    (18, 14): (CAND_DIR / "levy_rozman__1.jpg", "CHESS.COM"),
    # Scene 19 Điền kinh Peres Jepchirchir
    (19, 3): (CAND_DIR / "jepchirchir__2.jpg", "AP PHOTO"),
    (19, 7): (CAND_DIR / "cas_lausanne__2.jpg", "AIU / REUTERS"),
    (19, 8): (CAND_DIR / "sydney_marathon__1.jpg", "AP PHOTO"),
    (19, 11): (CAND_DIR / "jepchirchir__1.jpg", "REUTERS"),
    # Scene 20 Cử tạ Hafizuddin
    (20, 3): (CAND_DIR / "weightlifting_clean__1.jpg", "AP PHOTO"),
    # Scene 21 ATP Finals Turin
    (21, 5): (CAND_DIR / "atp_arena__1.jpg", "ATP TOUR"),
    (21, 6): (CAND_DIR / "zverev_1__1.jpg", "REUTERS"),
    (21, 7): (CAND_DIR / "arthur_fils__2.jpg", "ATP TOUR"),
    (21, 8): (CAND_DIR / "zverev_2__1.jpg", "REUTERS"),
}

# Cắt viền logo góc mỏng (top_frac, bottom_frac) -> giữ trọn chủ thể, xóa hoàn toàn chữ/logo sát mép
EDGE_CROPS: Dict[Tuple[int, int], Tuple[float, float]] = {
    (0, 14): (0.0, 0.085),
    (4, 12): (0.055, 0.0),
    (15, 1): (0.0, 0.085),
    (15, 3): (0.0, 0.085),
    (15, 4): (0.0, 0.085),
    (15, 7): (0.0, 0.085),
    (15, 8): (0.0, 0.085),
    (15, 9): (0.0, 0.085),
    (15, 10): (0.0, 0.085),
    (20, 7): (0.075, 0.0),
}
for _i in range(1, 14):
    if _i != 12:
        EDGE_CROPS[(17, _i)] = (0.0, 0.055)


def load_source_image(src: Any, snap_self: Dict[str, bytes]) -> Image.Image:
    if isinstance(src, tuple) and src[0] == "SELF":
        raw = snap_self[src[1]]
        return ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
    if isinstance(src, Path):
        if not src.exists():
            raise FileNotFoundError(f"Missing replacement file: {src}")
        return ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if isinstance(src, str) and src.startswith("http"):
        resp = requests.get(
            src,
            headers={"User-Agent": "Mozilla/5.0 Chrome/131.0.0.0", "Referer": "https://dantri.com.vn/"},
            timeout=15,
        )
        resp.raise_for_status()
        return ImageOps.exif_transpose(Image.open(io.BytesIO(resp.content))).convert("RGB")
    raise ValueError(f"Unsupported replacement source: {src}")


def main() -> None:
    # Lưu bản chụp các file ảnh hiện có trong images/ trước khi ghi đè để ("SELF", fn) an toàn tuyệt đối
    snap_self: Dict[str, bytes] = {
        p.name: p.read_bytes() for p in IMG_DIR.glob("Tin_*.jpg")
    }

    plan_path = OUT_DIR / "image_plan.json"
    credits_path = OUT_DIR / "image_credits.json"
    intro_path = OUT_DIR / "intro_hook.json"
    thethao_path = OUT_DIR / "thethao.json"

    plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
    credits_map: Dict[str, str] = json.loads(credits_path.read_text(encoding="utf-8"))
    intro_entry = json.loads(intro_path.read_text(encoding="utf-8"))
    thethao_entries = json.loads(thethao_path.read_text(encoding="utf-8"))

    # Nhóm bản ghi theo scene_id giữ nguyên thứ tự slot
    by_scene: Dict[int, List[Dict[str, Any]]] = {}
    for rec in plan_data["records"]:
        by_scene.setdefault(int(rec["scene_id"]), []).append(rec)

    touched_scenes = set()
    replaced_cnt = 0
    cropped_cnt = 0

    for sc_id, recs in sorted(by_scene.items()):
        for idx, rec in enumerate(recs, start=1):
            fn = rec["file_name"]
            out_p = IMG_DIR / fn
            key = (sc_id, idx)

            if key in REPLACEMENTS:
                src_spec, new_credit = REPLACEMENTS[key]
                im = load_source_image(src_spec, snap_self)
                if key in EDGE_CROPS:
                    t_f, b_f = EDGE_CROPS[key]
                    im = im.crop((0, int(im.height * t_f), im.width, int(im.height * (1.0 - b_f))))
                    cropped_cnt += 1
                im.save(out_p, format="JPEG", quality=95, optimize=True)
                rec["dimensions"] = f"{im.width}x{im.height} r={im.width / im.height:.2f}"
                if new_credit:
                    rec["credit"] = new_credit
                    credits_map[fn] = new_credit
                replaced_cnt += 1
                touched_scenes.add(sc_id)
            elif key in EDGE_CROPS and out_p.exists():
                t_f, b_f = EDGE_CROPS[key]
                with Image.open(out_p) as orig:
                    im = orig.convert("RGB")
                    im = im.crop((0, int(im.height * t_f), im.width, int(im.height * (1.0 - b_f))))
                im.save(out_p, format="JPEG", quality=95, optimize=True)
                rec["dimensions"] = f"{im.width}x{im.height} r={im.width / im.height:.2f}"
                cropped_cnt += 1
                touched_scenes.add(sc_id)

            assert rec["dimensions"] != "MISSING", f"Còn ảnh MISSING: {fn}"

    # Tái dựng Contact Sheets cho mọi scene đã sửa + overview
    all_items_map: Dict[int, Dict[str, Any]] = {0: intro_entry}
    for it in thethao_entries:
        all_items_map[int(it["id"])] = it

    overview_records: List[Dict[str, Any]] = []
    for sc_id in sorted(by_scene.keys()):
        recs = by_scene[sc_id]
        overview_records.extend(recs[:2])
        if sc_id in touched_scenes:
            it = all_items_map[sc_id]
            vp = it.get("voice_preset", "primary")
            vn = it.get("voice", "")
            sheet_name = "contact_scene_00_intro.jpg" if sc_id == 0 else f"contact_scene_{sc_id:02d}.jpg"
            sheet_title = it.get("group") if sc_id == 0 else it.get("title", "")
            prep20.render_scene_contact_sheet(
                sc_id,
                sheet_title,
                it.get("news_source") or it.get("source") or "",
                f"{vp} ({vn})",
                recs,
                QA_DIR / sheet_name,
            )

    prep20.render_overview_sheet(overview_records, QA_DIR / "contact_overview.jpg")

    plan_path.write_text(json.dumps(plan_data, ensure_ascii=False, indent=2), encoding="utf-8")
    credits_path.write_text(json.dumps(credits_map, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"HOÀN TẤT CẬP NHẬT QA ẢNH: Thay {replaced_cnt} ảnh | Crop sạch viền {cropped_cnt} ảnh | Đã tái dựng {len(touched_scenes)} bảng QA + Overview.")


if __name__ == "__main__":
    main()
