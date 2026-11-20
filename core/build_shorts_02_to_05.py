#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/build_shorts_02_to_05.py — Tự động hóa sản xuất trọn bộ 4 Video Shorts (Short 2, 3, 4, 5)
từ Bản tin tổng hợp thể thao tuần 09.11.2026.

Mỗi Video Short:
- Gộp 2-3 tin từ outputs/09.11.2026/thethao.json
- Thể hiện rõ bản chất "TIN NÓNG TUẦN QUA" trên tiêu đề, kicker và nội dung
- Áp dụng template short_news_v2.html:
    + Hero Title lớn ở đầu mỗi bản tin (is_title: True)
    + Thu về #fixed-headline-bar khi vào chi tiết
    + Cập nhật động Category Pill, Lower-Third 2 góc (Nguồn tin & Nguồn ảnh)
    + Phụ đề Karaoke đồng bộ 100% từng từ
    + Âm thanh master EBU R128 (-14.0 LUFS, TP <= -1.0 dBTP, drift <= 33.3 ms)
- Xuất bản trọn bộ:
    + Video: outputs/09.11.2026/shorts/<tên_short>.mp4
    + Thumbnail: outputs/09.11.2026/shorts/<tên_short>_thumbnail.jpg
    + Mô tả SEO: outputs/09.11.2026/shorts/<tên_short>_mota.txt
"""
import sys
sys.dont_write_bytecode = True

import os
import json
import shutil
import argparse
import subprocess
from pathlib import Path

from diemdoc import paths
from diemdoc.log import banner, ok, step, log, die, warn
from diemdoc.publisher import write_mota_9x16, render_thumbnail_9x16
from m8_news_bridge import build_focus_short_timeline

SHORTS_CONFIG = [
    {
        "id": 2,
        "name": "Short_02_Tin_Nong_Dia_Chan_Ngoai_Hang_Anh",
        "items": [7, 8, 10],
        "title": "TIN NÓNG TUẦN QUA: ĐỊA CHẤN NGOẠI HẠNG ANH",
        "group": "ĐỊA CHẤN NGOẠI HẠNG ANH",
        "item_meta": {
            "7": {"group": "MAN CITY GỤC NGÃ", "source": "NOTTINGHAM POST / PREMIER LEAGUE"},
            "8": {"group": "MU RƠI ĐÈN ĐỎ", "source": "MANCHESTER EVENING NEWS / SKY SPORTS"},
            "10": {"group": "CHELSEA THUA SỐC", "source": "THE ATHLETIC / BBC SPORT"},
        },
        "seo_title": "Tin nóng thể thao tuần qua: Man City gục ngã, MU rơi nhóm đèn đỏ, Chelsea thua sốc #Shorts",
        "description": [
            "Tin nóng thể thao tuần qua: Vòng đấu Ngoại hạng Anh chứng kiến những cơn địa chấn liên tiếp khi cả 3 ông lớn Man City, Man United và Chelsea đều đồng loạt sảy chân cay đắng.",
            "Nottingham Forest quật ngã Man City 3-1 giúp Arsenal nới rộng cách biệt 6 điểm; Man United hòa điên rồ Aston Villa 4-4 nhưng chính thức rơi xuống vị trí thứ 18; Chelsea thua sốc Sunderland 0-1 giữa bão tranh cãi VAR."
        ],
        "chapters": [
            ("00:00", "Nottingham Forest quật ngã Man City 3-1, Arsenal nới rộng cách biệt 6 điểm"),
            ("00:42", "Man United hòa Aston Villa 4-4 điên rồ nhưng rơi vào nhóm cầm đèn đỏ"),
            ("01:25", "Chelsea gục ngã 0-1 trước Sunderland giữa tranh cãi nảy lửa về VAR"),
        ],
        "sources": "📰 Nguồn tin: Nottingham Post, Manchester Evening News, The Athletic, Sky Sports, Premier League.",
        "hashtags": ["#Shorts", "#TinNongTuanQua", "#NgoaiHangAnh", "#PremierLeague", "#ManUtd", "#ManCity", "#Chelsea", "#DiemDoc", "#BongDa"],
        "thumb": {
            "image": "Tin_08_4.jpg",
            "kicker": "TIN NÓNG NGOẠI HẠNG ANH TUẦN QUA",
            "hero_html": "<span class=\"hl-red\">MU RƠI ĐÈN ĐỎ!</span><br><span class=\"hl-white\">MAN CITY THUA 1-3</span><br><span class=\"hl-yellow\">CHELSEA GỤC NGÃ</span>",
            "subtitle": "HÒA ĐIÊN RỒ 4-4 • NOTTINGHAM QUẬT NGÃ MAN CITY • TRANH CÃI VAR",
            "badge": "ĐỊA CHẤN PREMIER LEAGUE",
            "tag_a": "TIN NÓNG TUẦN",
            "tag_b": "09.11.2026",
            "obj_pos": "55% 15%",
        }
    },
    {
        "id": 3,
        "name": "Short_03_Tin_Nong_Champions_League_Dien_Ro",
        "items": [3, 4, 5],
        "title": "TIN NÓNG TUẦN QUA: CHAMPIONS LEAGUE ĐIÊN RỒ",
        "group": "CÚP C1 ĐIÊN RỒ",
        "item_meta": {
            "3": {"group": "KỶ LỤC CÚP C1 9-1", "source": "UEFA / GAZZETTA DELLO SPORT"},
            "4": {"group": "REAL MADRID NGƯỢC DÒNG", "source": "MARCA / AS / REAL MADRID TV"},
            "5": {"group": "HAALAND CÁN MỐC 62 BÀN", "source": "MAN CITY FC / SKY SPORTS"},
        },
        "seo_title": "Tin nóng thể thao tuần qua: Como thắng kỷ lục 9-1, Real Madrid ngược dòng phút 92 #Shorts",
        "description": [
            "Tin nóng thể thao tuần qua: Lượt trận vòng bảng UEFA Champions League bùng nổ với những cơn mưa bàn thắng không tưởng và kịch bản nghẹt thở đến giây cuối cùng.",
            "Hiện tượng Como của HLV Cesc Fabregas thắng hủy diệt 9-1 đi vào lịch sử giải đấu; Fede Valverde lập siêu phẩm phút 90+2 cứu Real Madrid; Erling Haaland cán mốc 62 bàn thắng cúp C1 siêu tốc."
        ],
        "chapters": [
            ("00:00", "Hiện tượng Como của Cesc Fabregas thắng 9-1 lập kỷ lục lịch sử cúp C1"),
            ("00:42", "Siêu phẩm phút 90+2 của Valverde giúp Real Madrid ngược dòng hạ Shakhtar 3-2"),
            ("01:21", "Erling Haaland cán mốc 62 bàn cúp C1 siêu tốc giúp Man City vượt qua Leipzig 3-2"),
        ],
        "sources": "📰 Nguồn tin: UEFA Champions League, Marca, AS, Gazzetta dello Sport, Sky Sports.",
        "hashtags": ["#Shorts", "#TinNongTuanQua", "#ChampionsLeague", "#CupC1", "#RealMadrid", "#ErlingHaaland", "#ComoFC", "#DiemDoc"],
        "thumb": {
            "image": "Tin_04_1.jpg",
            "kicker": "TIN NÓNG CÚP C1 TUẦN QUA",
            "hero_html": "<span class=\"hl-cyan\">COMO THẮNG 9-1!</span><br><span class=\"hl-white\">VALVERDE CỨU REAL</span><br><span class=\"hl-yellow\">HAALAND 62 BÀN</span>",
            "subtitle": "KỶ LỤC LỊCH SỬ CÚP C1 • SIÊU PHẨM PHÚT 90+2 • CỖ MÁY GHI BÀN",
            "badge": "CÚP C1 ĐIÊN RỒ",
            "tag_a": "TIN NÓNG TUẦN",
            "tag_b": "09.11.2026",
            "obj_pos": "50% 15%",
        }
    },
    {
        "id": 4,
        "name": "Short_04_Tin_Nong_Doi_Tuyen_Viet_Nam",
        "items": [16, 18, 21],
        "title": "TIN NÓNG TUẦN QUA: ĐỘI TUYỂN VIỆT NAM & BÓNG ĐÁ QUỐC NỘI",
        "group": "ĐỘI TUYỂN VIỆT NAM",
        "item_meta": {
            "16": {"group": "OLAHA LÊN TUYỂN VN", "source": "VFF / BÁO BÓNG ĐÁ / VNEXPRESS"},
            "18": {"group": "CÔNG PHƯỢNG TỎA SÁNG", "source": "VPF / BÁO THANH NIÊN"},
            "21": {"group": "TẠM BIỆT SÂN LONG AN", "source": "BÁO LONG AN / BÁO TUỔI TRẺ"},
        },
        "seo_title": "Tin nóng thể thao tuần qua: Tuyển Việt Nam gọi Olaha Mạnh Đức, Công Phượng tỏa sáng #Shorts",
        "description": [
            "Tin nóng thể thao tuần qua: Bóng đá Việt Nam đón nhận nhiều thông tin tích cực và xúc động từ chiến dịch tập trung ĐTQG đến các giải đấu quốc nội.",
            "HLV Kim Sang-sik triệu tập tiền đạo nhập tịch Olaha Mạnh Đức chuẩn bị cho Casper Cup; Công Phượng lập công giúp Đồng Nai thắng trận đầu tiên; Người hâm mộ nghẹn ngào chia tay chảo lửa Long An trước ngày san phẳng."
        ],
        "chapters": [
            ("00:00", "HLV Kim Sang-sik triệu tập tân binh nhập tịch Olaha Mạnh Đức đấu Casper Cup"),
            ("00:39", "Công Phượng lập siêu phẩm sút xa đưa Đồng Nai giành chiến thắng đầu tay"),
            ("00:55", "Xúc động trận cầu chia tay chảo lửa Long An trước ngày san phẳng tháo dỡ"),
        ],
        "sources": "📰 Nguồn tin: VFF, VPF, Báo Bóng Đá, Báo Thanh Niên, Báo Tuổi Trẻ, VnExpress.",
        "hashtags": ["#Shorts", "#TinNongTuanQua", "#BongDaVietNam", "#DoiTuyenVietNam", "#OlahaManhDuc", "#CongPhuong", "#VLeague", "#DiemDoc"],
        "thumb": {
            "image": "Tin_16_10.jpg",
            "kicker": "BÓNG ĐÁ VIỆT NAM TUẦN QUA",
            "hero_html": "<span class=\"hl-cyan\">OLAHA LÊN TUYỂN!</span><br><span class=\"hl-white\">CÔNG PHƯỢNG NỔ SÚNG</span><br><span class=\"hl-yellow\">TẠM BIỆT LONG AN</span>",
            "subtitle": "TÂN BINH NHẬP TỊCH ĐẤU CASPER CUP • BÀN THẮNG QUÝ NHƯ VÀNG • CHIA TAY CHẢO LỬA",
            "badge": "TUYỂN VIỆT NAM",
            "tag_a": "BÓNG ĐÁ VIỆT",
            "tag_b": "09.11.2026",
            "obj_pos": "50% 15%",
        }
    },
    {
        "id": 5,
        "name": "Short_05_Tin_Nong_Bi_Kich_San_Co",
        "items": [12, 13],
        "title": "TIN NÓNG TUẦN QUA: BI KỊCH SÂN CỎ & TIẾNG CHUÔNG CẢNH TỈNH",
        "group": "CẢNH TỈNH BÓNG ĐÁ",
        "item_meta": {
            "12": {"group": "BI KỊCH DE MIGUEL", "source": "BÁO CHÍ TÂY BAN NHA / EFE / FIFA"},
            "13": {"group": "TIẾNG CHUÔNG BÁO ĐỘNG", "source": "THE GUARDIAN / TƯ LIỆU BÓNG ĐÁ"},
        },
        "seo_title": "Tin nóng thể thao tuần qua: Bi kịch đau lòng sân cỏ và tiếng chuông cảnh tỉnh bóng đá #Shorts",
        "description": [
            "Tin nóng thể thao tuần qua: Làng túc cầu thế giới bàng hoàng trước sự ra đi đột ngột của tiền đạo Jesús de Miguel sau một pha va chạm vùng đầu trên sân cỏ Tây Ban Nha.",
            "Bi kịch đau lòng này làm dấy lên làn sóng kiến nghị khẩn cấp yêu cầu FIFA và IFAB đổi luật chấn thương đầu, đồng thời gợi lại những tai nạn thương tâm trong lịch sử bóng đá thế giới."
        ],
        "chapters": [
            ("00:00", "Bi kịch tiền đạo Jesús de Miguel qua đời và làn sóng kiến nghị FIFA đổi luật"),
            ("00:41", "Nhìn lại những tai nạn va chạm kinh hoàng nhất lịch sử bóng đá thế giới"),
        ],
        "sources": "📰 Nguồn tin: Báo chí Tây Ban Nha, EFE, The Guardian, FIFA.",
        "hashtags": ["#Shorts", "#TinNongTuanQua", "#BongDa", "#JesusDeMiguel", "#TuLieuBongDa", "#BiKichSanCo", "#DiemDoc", "#FIFA"],
        "thumb": {
            "image": "Tin_12_1.jpg",
            "kicker": "TƯ LIỆU BÓNG ĐÁ TUẦN QUA",
            "hero_html": "<span class=\"hl-white\">BI KỊCH SÂN CỎ:</span><br><span class=\"hl-red\">TIẾNG CHUÔNG CẢNH TỈNH</span><br><span class=\"hl-cyan\">VÀ ĐỀ NGHỊ ĐỔI LUẬT!</span>",
            "subtitle": "SỰ RA ĐI CỦA JESÚS DE MIGUEL • NHỮNG TAI NẠN VA CHẠM ĐAU LÒNG NHẤT LỊCH SỬ",
            "badge": "CẢNH TỈNH BÓNG ĐÁ",
            "tag_a": "TƯ LIỆU BÓNG ĐÁ",
            "tag_b": "09.11.2026",
            "obj_pos": "50% 15%",
            "filter": "grayscale(100%) contrast(1.15) brightness(0.95)",
        }
    }
]


def build_single_short(cfg: dict, day_dir: Path, shorts_dir: Path) -> dict:
    short_id = cfg["id"]
    short_name = cfg["name"]
    items = cfg["items"]

    banner(f"SẢN XUẤT SHORT {short_id}: {cfg['title']}", "09.11.2026")
    work_proj_dir = Path(paths.WORK) / f"focus_short_{short_id:02d}_{day_dir.name}"
    work_proj_dir.mkdir(parents=True, exist_ok=True)

    # 1. Timeline qua m8_news_bridge
    log(f"Xây dựng timeline cho các tin {items}...")
    timeline, words_data, _ = build_focus_short_timeline(
        day_dir=str(day_dir),
        item_ids=items,
        global_offset_sec=0.0
    )

    timeline["title"] = cfg["title"]
    timeline["group"] = cfg["group"]

    item_meta = cfg.get("item_meta", {})
    for s in timeline.get("sentences", []):
        sid = str(s.get("item_id"))
        if sid in item_meta:
            m = item_meta[sid]
            if "group" in m:
                s["item_group"] = m["group"]
            if "source" in m:
                s["news_source"] = m["source"]

    tl_path = work_proj_dir / "video_timeline.json"
    words_path = work_proj_dir / "word_timestamps.json"
    voice_dest = work_proj_dir / "voiceover.wav"

    if os.path.exists(timeline["audio_path"]):
        shutil.copy2(timeline["audio_path"], str(voice_dest))

    with open(tl_path, "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)

    with open(words_path, "w", encoding="utf-8") as f:
        json.dump(words_data, f, ensure_ascii=False, indent=2)

    ok(f"Đã lưu timeline: {tl_path}")

    # 2. Render HTML engine
    sys.path.insert(0, str(Path(paths.ROOT) / "engines" / "html"))
    from renderer import render_html_engine

    log(f"Render video HTML v2 (Playwright + GSAP) cho Short {short_id}...")
    out_video_work = render_html_engine(
        project_dir=str(work_proj_dir),
        template="short_news_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True
    )

    if not out_video_work or not os.path.exists(out_video_work):
        die(f"Render Short {short_id} thất bại!")

    # 3. Xuất file mp4 và căn chỉnh Video-Audio sync
    out_final_mp4 = shorts_dir / f"{short_name}.mp4"
    shutil.copy2(out_video_work, str(out_final_mp4))

    # Căn chỉnh duration để Video-Audio drift <= 33.3ms (1 frame 30fps)
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries", "stream=duration,codec_type",
        "-of", "json", str(out_final_mp4)
    ]
    res = subprocess.run(probe_cmd, capture_output=True, text=True)
    try:
        pdata = json.loads(res.stdout)
        v_dur = next(float(s["duration"]) for s in pdata.get("streams", []) if s["codec_type"] == "video")
        tmp_sync = shorts_dir / f"{short_name}_sync.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(out_final_mp4), "-t", f"{v_dur:.6f}",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
            str(tmp_sync)
        ], check=True)
        tmp_sync.replace(out_final_mp4)
    except Exception as e:
        warn(f"Không thể chỉnh duration drift: {e}")

    ok(f"Đã xuất video Short {short_id}: {out_final_mp4}")

    # 4. Kiểm toán âm thanh EBU R128
    log(f"Kiểm toán âm thanh Short {short_id}...")
    subprocess.run(["python3", "-B", "core/audio_check.py", str(out_final_mp4)])

    # 5. Xuất mô tả SEO YouTube Shorts
    mota_path = shorts_dir / f"{short_name}_mota.txt"
    write_mota_9x16(
        out_path=mota_path,
        seo_title=cfg["seo_title"],
        description_paragraphs=cfg["description"],
        chapters=cfg["chapters"],
        sources_line=cfg["sources"],
        hashtags=cfg["hashtags"]
    )
    ok(f"Đã tạo mô tả SEO: {mota_path}")

    # 6. Render Thumbnail 9:16 Cyber-Stadium
    t_cfg = cfg["thumb"]
    thumb_path = shorts_dir / f"{short_name}_thumbnail.jpg"
    thumb_img = day_dir / "images" / t_cfg["image"]
    if not thumb_img.exists():
        thumb_img = day_dir / "images" / "Tin_01_1.jpg"

    render_thumbnail_9x16(
        out_path=thumb_path,
        image_path=thumb_img,
        kicker=t_cfg["kicker"],
        hero_html=t_cfg["hero_html"],
        subtitle=t_cfg["subtitle"],
        badge=t_cfg["badge"],
        tag_a=t_cfg.get("tag_a", "TIN NÓNG TUẦN"),
        tag_b=t_cfg.get("tag_b", "09.11.2026"),
        obj_pos=t_cfg.get("obj_pos", "center 15%"),
        img_filter=t_cfg.get("filter", "contrast(1.10) brightness(1.05) saturate(1.18)")
    )
    ok(f"Đã tạo thumbnail 9:16: {thumb_path}")

    return {
        "id": short_id,
        "video": out_final_mp4,
        "thumb": thumb_path,
        "mota": mota_path
    }


def main():
    parser = argparse.ArgumentParser(description="Render Shorts 2, 3, 4, 5")
    parser.add_argument("--only", type=str, default="2,3,4,5", help="Danh sách ID (vd: 2,3,4,5)")
    args = parser.parse_args()

    day_dir = Path(paths.ROOT) / "outputs" / "09.11.2026"
    shorts_dir = day_dir / "shorts"
    shorts_dir.mkdir(parents=True, exist_ok=True)

    target_ids = [int(x.strip()) for x in args.only.split(",") if x.strip()]
    results = []

    for cfg in SHORTS_CONFIG:
        if cfg["id"] in target_ids:
            res = build_single_short(cfg, day_dir, shorts_dir)
            results.append(res)

    print("\n" + "=" * 78)
    ok(f"HOÀN THÀNH XUẤT BẢN {len(results)} VIDEO SHORTS!")
    for r in results:
        print(f"\n  🎬 SHORT {r['id']}:")
        print(f"     • Video:     {r['video']}")
        print(f"     • Thumbnail: {r['thumb']}")
        print(f"     • Mô tả SEO: {r['mota']}")
    print("=" * 78)


if __name__ == "__main__":
    main()
