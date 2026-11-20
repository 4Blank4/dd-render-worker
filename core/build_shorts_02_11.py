#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_shorts_02_11.py — Dựng 4 Video Shorts 9:16 (Chủ đề 1, 2, 3, 4)
kèm 4 Thumbnail dọc (1080x1920) chuẩn Cyber-Stadium và 4 file mô tả SEO.
"""
import sys
sys.dont_write_bytecode = True

import os
import shutil
import time
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "vendor"))

engines_html = os.path.join(_ROOT, "engines", "html")
if engines_html not in sys.path:
    sys.path.insert(0, engines_html)

from diemdoc import paths
from diemdoc.log import banner, ok, step, log
from m8_news_bridge import export_bridge_project
from renderer import render_html_engine

DAY_STR = "02.11.2026"
DAY_DIR = os.path.join(paths.OUTPUTS, DAY_STR)
WORK_DIR = paths.work_project_dir(DAY_STR)

SHORTS_OUT = os.path.join(DAY_DIR, "shorts")
SHORTS_WORK = os.path.join(WORK_DIR, "shorts_render")

SHORTS_CONFIG = [
    {
        "id": 1,
        "item_id": 1,
        "slug": "Short_01_Harry_Kane_Doat_Qua_Bong_Vang_2026",
        "file_name": "Short_01_Harry_Kane_Doat_Qua_Bong_Vang_2026.mp4",
        "thumb_name": "Short_01_thumbnail.jpg",
        "mota_name": "Short_01_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_01_6.jpg"),
        "thumb_kicker": "QUẢ BÓNG VÀNG 2026",
        "thumb_hero": "HARRY KANE!",
        "thumb_hero_size": "115",
        "thumb_sub": "KỶ LỤC 61 BÀN THẮNG",
        "thumb_tag_a": "CHẤM DỨT 38 NĂM",
        "thumb_tag_b": "VƯỢT QUA MBAPPÉ",
        "title": "Harry Kane đoạt Quả bóng vàng 2026: Chấm dứt 38 năm chờ đợi! #Shorts",
        "desc": (
            "Sau một mùa giải bùng nổ hủy diệt với 61 bàn thắng, tiền đạo 33 tuổi Harry Kane đã chính thức "
            "bước lên đỉnh cao danh vọng khi được xướng tên ở giải thưởng Quả bóng vàng nam 2026 tại London, "
            "đập tan mọi hoài nghi về danh hiệu tập thể để khẳng định vị thế số 9 toàn diện nhất lịch sử!"
        ),
        "tags": "#HarryKane #BallondOr #QuaBongVang #BayernMunich #DiemDoc #Shorts #BongDaQuocTe"
    },
    {
        "id": 2,
        "item_id": 2,
        "slug": "Short_02_Tranh_Cai_Messi_Top_5_Vinh_Danh_Ronaldo",
        "file_name": "Short_02_Tranh_Cai_Messi_Top_5_Vinh_Danh_Ronaldo.mp4",
        "thumb_name": "Short_02_thumbnail.jpg",
        "mota_name": "Short_02_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_02_12.jpg"),
        "thumb_kicker": "GALA BALLON D'OR 2026",
        "thumb_hero": "VINH DANH CR7!",
        "thumb_hero_size": "110",
        "thumb_sub": "TRANH CÃI TOP 5 CỦA MESSI",
        "thumb_tag_a": "QBV MỌI THỜI ĐẠI",
        "thumb_tag_b": "907+ BÀN THẮNG",
        "title": "Tranh cãi Messi lọt top 5 thế giới & Ronaldo nhận Quả bóng vàng Vĩ đại nhất! #Shorts",
        "desc": (
            "Đêm Gala Quả bóng vàng 2026 châm ngòi tranh cãi nảy lửa khi Lionel Messi vẫn đứng trong Top 5 cầu thủ xuất sắc nhất "
            "dù đang thi đấu tại giải MLS, trong khi Cristiano Ronaldo được ban tổ chức vinh danh đặc biệt với danh hiệu "
            "Quả bóng vàng Mọi thời đại, ghi nhận sự nghiệp ghi bàn vĩ đại nhất lịch sử túc cầu!"
        ),
        "tags": "#CristianoRonaldo #CR7 #LionelMessi #Messi #BallondOr #DiemDoc #Shorts #BongDa"
    },
    {
        "id": 3,
        "item_id": 7,
        "slug": "Short_03_Be_Boi_Nhap_Tich_Malaysia_Xoa_An",
        "file_name": "Short_03_Be_Boi_Nhap_Tich_Malaysia_Xoa_An.mp4",
        "thumb_name": "Short_03_thumbnail.jpg",
        "mota_name": "Short_03_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_07_1.jpg"),
        "thumb_kicker": "BÓNG ĐÁ ĐÔNG NAM Á",
        "thumb_hero": "BÊ BỐI MALAYSIA!",
        "thumb_hero_size": "105",
        "thumb_sub": "7 CẦU THỦ ĐƯỢC XÓA ÁN",
        "thumb_tag_a": "GIAN LẬN GỐC GÁC",
        "thumb_tag_b": "HẾT ÁN PHẠT FIFA",
        "title": "Bê bối 7 cầu thủ gian lận nhập tịch của Malaysia được FIFA xóa án! #Shorts",
        "desc": (
            "Làng bóng đá Đông Nam Á rúng động trước thông tin 7 cầu thủ gốc Nam Mỹ và châu Âu làm giả hồ sơ nguồn gốc "
            "để nhập tịch khoác áo đội tuyển quốc gia Malaysia. Sau 1 năm nhận án phạt cấm thi đấu nghiêm khắc từ FIFA, "
            "toàn bộ nhóm cầu thủ này đã chính thức hết hạn treo giò và được Liên đoàn Bóng đá Malaysia mở cửa trở lại, "
            "làm bùng lên làn sóng phản ứng kịch liệt từ người hâm mộ khu vực vì tính công bằng thể thao!"
        ),
        "tags": "#Malaysia #AFFCup #DTVietnam #FIFA #DiemDoc #Shorts #BongDaDongNamA"
    },
    {
        "id": 4,
        "item_id": 8,
        "slug": "Short_04_Man_Utd_Cham_Day_38_Nam_The_Do_Martinez",
        "file_name": "Short_04_Man_Utd_Cham_Day_38_Nam_The_Do_Martinez.mp4",
        "thumb_name": "Short_04_thumbnail.jpg",
        "mota_name": "Short_04_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_08_2.jpg"),
        "thumb_kicker": "NGOẠI HẠNG ANH · VÒNG 9",
        "thumb_hero": "MAN UTD CHẠM ĐÁY!",
        "thumb_hero_size": "100",
        "thumb_sub": "THẢM HỌA 38 NĂM LỊCH SỬ",
        "thumb_tag_a": "THẺ ĐỎ MARTINEZ",
        "thumb_tag_b": "CHUỖI 9 TRẬN BẾT BÁT",
        "title": "Man Utd chạm đáy 38 năm: Thua 0-2 & thẻ đỏ Martinez! #Shorts",
        "desc": (
            "Cơn ác mộng tồi tệ nhất sau 38 năm lịch sử giáng xuống Quỷ đỏ Man Utd sau trận thua cay đắng 0-2 trước Chelsea "
            "và tấm thẻ đỏ trực tiếp thô bạo của Lisandro Martinez. Chuỗi 9 trận liên tiếp không thắng đẩy đội bóng vào "
            "cuộc khủng hoảng trầm trọng trước bờ vực sa thải HLV!"
        ),
        "tags": "#ManUtd #MU #LisandroMartinez #BrunoFernandes #PremierLeague #DiemDoc #Shorts"
    },
    {
        "id": 5,
        "item_id": 9,
        "slug": "Short_05_Con_Dia_Chan_Man_City_Arsenal",
        "file_name": "Short_05_Con_Dia_Chan_Man_City_Arsenal.mp4",
        "thumb_name": "Short_05_thumbnail.jpg",
        "mota_name": "Short_05_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_09_1.jpg"),
        "thumb_kicker": "NGOẠI HẠNG ANH & CÚP LIÊN ĐOÀN",
        "thumb_hero": "ĐỊA CHẤN NƯỚC ANH!",
        "thumb_hero_size": "100",
        "thumb_sub": "MAN CITY GỤC NGÃ, ARSENAL BỊ LOẠI",
        "thumb_tag_a": "PEP GUARDIOLA BẾ TẮC",
        "thumb_tag_b": "THẢM HỌA ARTETA",
        "title": "Cơn địa chấn nước Anh: Man City thua trận thứ 2, Arsenal bị đội hạng 4 loại sốc! #Shorts",
        "desc": (
            "Ngoại hạng Anh và Cúp Liên Đoàn Anh tuần qua chứng kiến cơn địa chấn không tưởng khi đương kim vô địch "
            "Manchester City bất ngờ gục ngã 1-2 trước Brighton vì lỗ hổng hàng phòng ngự, trong khi Arsenal trải qua "
            "thảm họa bẽ bàng bị đội bóng hạng 4 loại cay đắng sau loạt sút luân lưu nghẹt thở!"
        ),
        "tags": "#ManCity #Arsenal #PepGuardiola #MikelArteta #PremierLeague #CarabaoCup #DiemDoc #Shorts"
    },
    {
        "id": 6,
        "item_id": 17,
        "slug": "Short_06_Tam_Chan_VLeague_HLV_Popov_Tu_Chuc",
        "file_name": "Short_06_Tam_Chan_VLeague_HLV_Popov_Tu_Chuc.mp4",
        "thumb_name": "Short_06_thumbnail.jpg",
        "mota_name": "Short_06_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_17_1.jpg"),
        "thumb_kicker": "TÂM CHẤN V-LEAGUE · VÒNG 6",
        "thumb_hero": "HLV POPOV TỪ CHỨC!",
        "thumb_hero_size": "100",
        "thumb_sub": "ĐẬP BÀN TRONG PHÒNG HỌP BÁO",
        "thumb_tag_a": "THỂ CÔNG VIETTEL",
        "thumb_tag_b": "CÚ SỐC V-LEAGUE",
        "title": "Tâm chấn V-League: HLV Popov đập bàn tuyên bố từ chức Thể Công Viettel! #Shorts",
        "desc": (
            "Cơn địa chấn lớn nhất bóng đá nội tuần qua đã nổ ra ngay sau hồi còi mãn cuộc trận đấu giữa Thể Công Viettel "
            "và Thép Xanh Nam Định tại vòng 6 V-League. Dù có bàn dẫn trước từ sớm, Thể Công Viettel lại thi đấu bạc nhược "
            "trong hiệp hai và để đối thủ lội ngược dòng đánh bại 2-1, đẩy đội bóng áo lính rơi tự do xuống vị trí thứ 12 trên BXH. "
            "Trong phòng họp báo sau trận, HLV cá tính người Bulgaria Velizar Popov đã khiến toàn bộ giới truyền thông bàng hoàng "
            "khi tuyên bố nộp đơn từ chức ngay lập tức vì cảm thấy hoàn toàn bất lực trước phong độ sa sút của học trò!"
        ),
        "tags": "#VLeague #TheCongViettel #VelizarPopov #NamDinh #DiemDoc #Shorts #BongDaVietNam"
    },
    {
        "id": 7,
        "item_id": 20,
        "slug": "Short_07_CAHN_Quat_Nga_Dan_Sao_Trieu_Do_C1_Chau_A",
        "file_name": "Short_07_CAHN_Quat_Nga_Dan_Sao_Trieu_Do_C1_Chau_A.mp4",
        "thumb_name": "Short_07_thumbnail.jpg",
        "mota_name": "Short_07_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_20_1.jpg"),
        "thumb_kicker": "C1 CHÂU Á · AFC CHAMPIONS LEAGUE",
        "thumb_hero": "ĐỊA CHẤN CHÂU Á!",
        "thumb_hero_size": "100",
        "thumb_sub": "CAHN QUẬT NGÃ DÀN SAO TRIỆU ĐÔ",
        "thumb_tag_a": "VƯỢT MẶT THÁI LAN",
        "thumb_tag_b": "BXH CHÂU LỤC",
        "title": "CLB Công an Hà Nội quật ngã dàn sao triệu đô Trung Quốc tại C1 châu Á! #Shorts",
        "desc": (
            "Tại đấu trường danh giá AFC Champions League Cúp C1 châu Á, bóng đá Việt Nam đã có một đêm thăng hoa rực rỡ "
            "nhờ màn trình diễn đỉnh cao của CLB Công An Hà Nội. Tiếp đón một đối thủ sừng sỏ và sở hữu dàn ngoại binh triệu đô "
            "đến từ Chinese Super League của Trung Quốc, đại diện thủ đô đã thi đấu vô cùng kỷ luật, tự tin và bản lĩnh, "
            "giúp bóng đá Việt Nam chính thức vượt qua Thái Lan trên bảng xếp hạng hệ số AFC!"
        ),
        "tags": "#CAHN #QuangHai #AFCChampionsLeague #DiemDoc #Shorts #BongDaVietNam"
    },
    {
        "id": 8,
        "item_id": 3,
        "slug": "Short_08_U17_Viet_Nam_Huy_Diet_Cheonan_FC_5_0",
        "file_name": "Short_08_U17_Viet_Nam_Huy_Diet_Cheonan_FC_5_0.mp4",
        "thumb_name": "Short_08_thumbnail.jpg",
        "mota_name": "Short_08_mota.txt",
        "thumb_image": os.path.join(DAY_DIR, "images", "Tin_03_1.jpg"),
        "thumb_kicker": "TẬP HUẤN HÀN QUỐC · WORLD CUP U17",
        "thumb_hero": "U17 VN HỦY DIỆT 5-0!",
        "thumb_hero_size": "100",
        "thumb_sub": "MÀN THỊ UY TẠI HÀN QUỐC",
        "thumb_tag_a": "CRISTIANO ROLAND",
        "thumb_tag_b": "CƠN LỐC ĐỎ",
        "title": "U17 Việt Nam hủy diệt Cheonan FC 5-0: Màn thị uy khủng khiếp tại Hàn Quốc! #Shorts",
        "desc": (
            "Tại chuyến tập huấn ở xứ sở kim chi, đội tuyển U17 Việt Nam dưới sự dẫn dắt của HLV Cristiano Roland "
            "đã có màn thị uy sức mạnh khủng khiếp khi đè bẹp U17 Cheonan FC với tỷ số đậm đà 5-0. Đây là thắng lợi thứ 2 "
            "liên tiếp, tạo đà tâm lý hoàn hảo hướng đến VCK World Cup U17 2026!"
        ),
        "tags": "#U17VietNam #CristianoRoland #WorldCupU17 #VFF #DiemDoc #Shorts #BongDaVietNam"
    }
]


def render_shorts_videos(force: bool = False, target_ids: Optional[List[int]] = None) -> List[str]:
    banner("DỰNG VIDEO SHORTS 9:16", DAY_STR)
    os.makedirs(SHORTS_OUT, exist_ok=True)
    os.makedirs(SHORTS_WORK, exist_ok=True)

    t0 = time.time()
    results = []

    configs = [c for c in SHORTS_CONFIG if target_ids is None or c["id"] in target_ids]

    for cfg in configs:
        short_num = cfg["id"]
        item_id = cfg["item_id"]
        out_path = os.path.join(SHORTS_OUT, cfg["file_name"])

        if os.path.exists(out_path) and os.path.getsize(out_path) > 1_000_000 and not force:
            ok(f"Short #{short_num:02d} (Tin {item_id:02d}) đã có sẵn: {paths.rel_to_root(out_path)}")
            results.append(out_path)
            continue

        step(f"Xuất timeline short cho Tin {item_id:02d} (Short #{short_num:02d})...")
        pdir, _, _ = export_bridge_project(
            DAY_DIR,
            item_id=item_id,
            format_type="short",
            work_proj_dir=os.path.join(SHORTS_WORK, f"short_{short_num:02d}_tin_{item_id:02d}"),
            global_offset_sec=0.0
        )

        step(f"Render 9:16 cho Short #{short_num:02d} trên template short_news_v2.html (30fps)...")
        v = render_html_engine(
            pdir,
            template="short_news_v2.html",
            scene_number=None,
            fps=30,
            preview=False,
            force=True
        )

        if v and os.path.exists(v):
            shutil.copy2(v, out_path)
            ok(f"🎉 Hoàn thành Short #{short_num:02d}: {paths.rel_to_root(out_path)} ({os.path.getsize(out_path)/(1024*1024):.1f} MB)")
            results.append(out_path)
        else:
            log(f"!! Render Short #{short_num:02d} thất bại", tag="shorts")

    banner(f"HOÀN THÀNH {len(results)}/{len(configs)} VIDEO SHORTS ({time.time()-t0:.1f}s)")
    return results


def render_shorts_thumbnails(target_ids: Optional[List[int]] = None):
    banner("TẠO BỘ ẢNH THUMBNAIL DỌC 9:16 CHO SHORTS", DAY_STR)
    assets_url = paths.file_url(paths.ASSETS)
    logo_url = paths.file_url(os.path.join(paths.ASSETS, "logo", "diem-doc-logo-1.png"))
    configs = [c for c in SHORTS_CONFIG if target_ids is None or c["id"] in target_ids]

    tpl_html = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<style>
  @font-face { font-family:'Anton'; src:url('__ASSETS__/fonts/Anton/Anton-Regular.ttf'); font-weight:400; }
  @font-face { font-family:'Oswald'; src:url('__ASSETS__/fonts/Oswald/static/Oswald-Bold.ttf'); font-weight:700; }
  @font-face { font-family:'Oswald'; src:url('__ASSETS__/fonts/Oswald/static/Oswald-SemiBold.ttf'); font-weight:600; }
  @font-face { font-family:'PlexMono'; src:url('__ASSETS__/fonts/IBM_Plex_Mono/IBMPlexMono-Bold.ttf'); font-weight:700; }

  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1080px; height:1920px; overflow:hidden; background:#05070C; }
  body { font-family:'Oswald', sans-serif; position:relative; }

  /* NỬA TRÊN: ẢNH 58% */
  .top {
    position:absolute; top:0; left:0; right:0; height:58%;
    overflow:hidden; background:#080B12;
  }
  .top img.hero-bg {
    width:100%; height:100%; object-fit:cover; object-position:center 20%;
    filter: contrast(1.12) brightness(1.05) saturate(1.18);
  }
  .top::after {
    content:''; position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(5,7,12,0.15) 0%, transparent 25%, rgba(5,7,12,0.7) 70%, #05070C 100%);
  }

  .badge {
    position:absolute; top:56px; left:56px; z-index:5;
    display:flex; align-items:center; gap:16px;
    padding:16px 28px; border-radius:999px;
    background:rgba(5,7,12,0.85); border:2px solid rgba(0,229,255,0.7);
    box-shadow: 0 4px 20px rgba(0,0,0,0.6), 0 0 15px rgba(0,229,255,0.3);
    backdrop-filter:blur(12px);
  }
  .badge img { height:40px; width:auto; border-radius:50%; }
  .badge span {
    font-family:'Oswald'; font-weight:700; font-size:24px;
    letter-spacing:4px; color:#00E5FF; text-transform:uppercase;
  }

  /* NỬA DƯỚI: SÂN KHẤU 42% */
  .bottom {
    position:absolute; bottom:0; left:0; right:0; height:43%;
    background:#05070C; padding:40px 70px 70px;
    display:flex; flex-direction:column; justify-content:center;
    border-top: 1px solid rgba(0,229,255,0.25);
  }
  .kicker {
    font-family:'PlexMono'; font-weight:700; font-size:26px;
    letter-spacing:5px; color:#00E5FF; margin-bottom:14px;
    text-transform:uppercase;
    text-shadow: 0 0 12px rgba(0,229,255,0.4);
  }
  .hero {
    font-family:'Anton'; font-size:__THUMB_HERO_SIZE__px; line-height:0.95;
    letter-spacing:1px;
    color:#FFFFFF; white-space:nowrap;
    text-shadow:0 0 40px rgba(0,229,255,0.35), 0 4px 10px rgba(0,0,0,0.8);
  }
  .hero .accent { color:#FFC24D; }
  .sub {
    font-family:'Oswald'; font-weight:700; font-size:46px; line-height:1.15;
    color:#F3F6FF; margin-top:16px; text-transform:uppercase; letter-spacing:1px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
  }
  .rule {
    height:6px; width:180px;
    background:linear-gradient(90deg, #00E5FF 0%, #38BDF8 100%);
    margin:24px 0 20px; border-radius:3px;
    box-shadow: 0 0 10px rgba(0,229,255,0.5);
  }
  .meta {
    display:flex; gap:36px; align-items:center;
    font-family:'PlexMono'; font-size:22px; font-weight:700; letter-spacing:2px;
    color:#94A0BE;
  }
  .meta b { color:#00E5FF; }
</style>
</head>
<body>
  <div class="top">
    <div class="badge">
      <img src="__LOGO__" alt="Logo">
      <span>ĐIỂM ĐỌC</span>
    </div>
    <img class="hero-bg" src="__THUMB_IMAGE__" alt="">
  </div>

  <div class="bottom">
    <div class="kicker">__THUMB_KICKER__</div>
    <div class="hero">__THUMB_HERO__</div>
    <div class="sub">__THUMB_SUBTITLE__</div>
    <div class="rule"></div>
    <div class="meta">
      <span>__THUMB_TAG_A__</span>
      <span><b>__THUMB_TAG_B__</b></span>
    </div>
  </div>
</body>
</html>"""

    tpl_html = tpl_html.replace("__ASSETS__", assets_url).replace("__LOGO__", logo_url)
    thumb_html_dir = os.path.join(WORK_DIR, "shorts_thumbnails_render")
    os.makedirs(thumb_html_dir, exist_ok=True)

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=[
            "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"
        ])
        page = br.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)

        for cfg in configs:
            out_thumb = os.path.join(SHORTS_OUT, cfg["thumb_name"])
            step(f"Render thumbnail dọc cho Short #{cfg['id']:02d}: {paths.rel_to_root(out_thumb)}...")

            img_path = cfg["thumb_image"]
            if not os.path.exists(img_path):
                img_path = os.path.join(DAY_DIR, "images", f"Tin_{cfg['item_id']:02d}_1.jpg")

            h_content = tpl_html
            h_content = h_content.replace("__THUMB_IMAGE__", paths.file_url(img_path))
            h_content = h_content.replace("__THUMB_KICKER__", cfg["thumb_kicker"])
            h_content = h_content.replace("__THUMB_HERO__", cfg["thumb_hero"])
            h_content = h_content.replace("__THUMB_HERO_SIZE__", cfg.get("thumb_hero_size", "110"))
            h_content = h_content.replace("__THUMB_SUBTITLE__", cfg["thumb_sub"])
            h_content = h_content.replace("__THUMB_TAG_A__", cfg["thumb_tag_a"])
            h_content = h_content.replace("__THUMB_TAG_B__", cfg["thumb_tag_b"])

            hfile = os.path.join(thumb_html_dir, f"thumb_short_{cfg['id']:02d}.html")
            with open(hfile, "w", encoding="utf-8") as hf:
                hf.write(h_content)

            page.goto(paths.file_url(hfile), wait_until="networkidle")
            page.wait_for_timeout(500)
            page.screenshot(path=out_thumb, type="jpeg", quality=95)
            ok(f"  👉 Đã xuất Thumbnail dọc: {paths.rel_to_root(out_thumb)}")

        br.close()


def write_shorts_metadata(target_ids: Optional[List[int]] = None):
    banner("XUẤT BẢN FILE MÔ TẢ SEO CHO CÁC SHORTS", DAY_STR)
    configs = [c for c in SHORTS_CONFIG if target_ids is None or c["id"] in target_ids]
    for cfg in configs:
        mota_file = os.path.join(SHORTS_OUT, cfg["mota_name"])
        content = (
            f"=== TIÊU ĐỀ SHORTS ===\n"
            f"{cfg['title']}\n\n"
            f"=== MÔ TẢ SHORTS ===\n"
            f"{cfg['desc']}\n\n"
            f"👉 Nhấn Đăng ký kênh Điểm Đọc để không bỏ lỡ các tin tức thể thao đỉnh cao mỗi ngày!\n\n"
            f"{cfg['tags']}\n"
        )
        with open(mota_file, "w", encoding="utf-8") as f:
            f.write(content)
        ok(f"  👉 Đã ghi file mô tả SEO: {paths.rel_to_root(mota_file)}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dựng video Shorts 9:16 Điểm Đọc")
    parser.add_argument("ids", nargs="*", type=int, help="Các ID Shorts cần dựng (ví dụ: 6 7 8)")
    parser.add_argument("--force", action="store_true", help="Bắt buộc dựng lại dù file đã tồn tại")
    args = parser.parse_args()

    targets = args.ids if args.ids else None
    force_mode = args.force or bool(targets)

    os.makedirs(SHORTS_OUT, exist_ok=True)
    # 1. Xuất file mô tả
    write_shorts_metadata(target_ids=targets)
    # 2. Render thumbnails dọc
    render_shorts_thumbnails(target_ids=targets)
    # 3. Render video shorts 9:16
    render_shorts_videos(force=force_mode, target_ids=targets)
    ok("🎉 HOÀN THÀNH TOÀN BỘ VIDEO SHORTS VÀ BỘ TÀI NGUYÊN!")


if __name__ == "__main__":
    main()
