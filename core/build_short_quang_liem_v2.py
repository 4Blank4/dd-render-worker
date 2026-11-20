#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo bản -2 cho Video Short 9:16 Tin #05 ("Quang Liêm thắng ván cờ chính xác 99%"):
  - Xuất: outputs/Orther/12.11.2026/shorts/Short_Le_Quang_Liem_Thang_Van_Co_Chinh_Xac_99_Phan_Tram-2.mp4
  - Giữ nguyên 100% giọng đọc Ngọc Huyền Mẫu 14, nội dung câu 1..5, 2 đồ thị DataViz, Karaoke & BGM.
  - Nâng cấp 3 giây đầu (s0: 0.00s -> 4.48s) với Opening Hook kích thích:
    + Crash-Zoom + Micro-Shake + Cyan Flash + Laser Scanline + 2 vòng Shockwave
    + HUD Score-Slam con số 0% -> 99% (VS 85% Artemiev) + Tactical Pills bật nối nhịp
    + Cắt ảnh nhanh 3 nhịp (Budapest 11/11 -> Nước thí mã 22 -> Quang Liêm nâng huy chương)
    + Đồng bộ tầng SFX: sub_drop_boom (0.02s), bell_ping_highlight (0.76s), whoosh_cinematic_1 (1.50s), pop_card (2.15s).
"""

import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR / "core") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "core"))
if str(ROOT_DIR / "engines" / "html") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "engines" / "html"))

from diemdoc import paths
from diemdoc.audio import measure_loudness
from diemdoc.log import banner, die, ok, step, warn
from diemdoc.short_batch import ShortDayContext, trim_video_audio_drift
from m8_news_bridge import compute_pan_params, export_bridge_project
from renderer import render_html_engine

CTX = ShortDayContext(
    day_dir=Path(paths.ROOT) / "outputs" / "Orther" / "12.11.2026",
    inspect_dir=Path.home() / "Library" / "Caches" / "DiemDoc" / "inspect_12_11_ql_v2",
    work_tag="12_11_ql_v2",
)

OUT_SLUG_V2 = "Short_Le_Quang_Liem_Thang_Van_Co_Chinh_Xac_99_Phan_Tram-2"


def build_v2_opening_hook(tl: dict) -> dict:
    """Nâng cấp s0 (0..sum_start) thành 3-Beat Opening Hook + Score-Slam 99% giữ nguyên phần sau."""
    sents = tl.get("sentences", [])
    if not sents:
        die("Timeline trống, không thể tạo bản -2")

    s0 = sents[0]
    s0_start = float(s0.get("start", 0.0))
    s0_end = float(s0.get("end", 4.48))
    s0_dur = round(s0_end - s0_start, 3)

    # Cắt nhanh 3 nhịp ảnh trên s0: 0..1.50s (đấu trí), 1.50..3.00s (nước thí mã 22), 3.00..s0_end (huy chương)
    beat_specs = [
        ("Tin_05_1.jpg", "VNEXPRESS / TOTAL CHESS", 0.0, 1.50),
        ("Tin_05_5.jpg", "VNEXPRESS", 1.50, 3.00),
        ("Tin_05_2.jpg", "VNEXPRESS", 3.00, s0_end),
    ]
    new_s0_imgs = []
    for idx, (fname, cred, t_a, t_b) in enumerate(beat_specs):
        img_path = str(CTX.images_dir / fname)
        im_s = round(s0_start + min(t_a, s0_dur), 3)
        im_e = round(s0_start + min(t_b, s0_dur), 3) if idx < len(beat_specs) - 1 else s0_end
        im_dur = round(max(0.25, im_e - im_s), 3)
        pan_info = compute_pan_params(img_path, duration=im_dur, dir_toggle=(idx % 2 == 1))
        new_s0_imgs.append({
            "src": img_path,
            "credit": cred,
            "start": im_s,
            "end": im_e,
            "duration": im_dur,
            "ken_burns": "pan_horizontal",
            "transition": "cut",
            **pan_info,
        })

    s0["images"] = new_s0_imgs
    s0["hook"] = {
        "fast_cut": True,
        "kicker": "ĐỘNG CƠ PHÂN TÍCH • BUDAPEST 2026",
        "vs_badge": "VS 85% ARTEMIEV",
        "stat_val": 99,
        "stat_unit": "%",
        "stat_label": "ĐỘ CHÍNH XÁC TUYỆT ĐỐI",
        "stat_sub": "Lê Quang Liêm cầm Quân Trắng • Thắng áp đảo 4–1",
        "opp_val": 85,
        "count_dur": 0.70,
        "exit_at": round(max(3.15, s0_dur - 0.90), 2),
        "pills": [
            {"text": "♞ NƯỚC 22: THÍ MÃ PHÁ THÀNH", "delay": 1.48, "style": ""},
            {"text": "♛ NƯỚC 32: CHIẾU HẾT 1 NƯỚC", "delay": 2.15, "style": "cyan"},
        ],
    }

    # Giữ nguyên mọi SFX từ s0_end trở đi, bổ sung bộ SFX 3s đầu khớp từng beat
    later_sfx = [ev for ev in tl.get("sfx_events", []) if float(ev.get("time", 0.0)) >= (s0_end - 0.1)]
    hook_sfx = [
        {"sfx": "sub_drop_boom.mp3", "time": 0.02, "volume": 0.45},
        {"sfx": "bell_ping_highlight.mp3", "time": 0.76, "volume": 0.28},
        {"sfx": "whoosh_cinematic_1.mp3", "time": 1.50, "volume": 0.28},
        {"sfx": "pop_card.mp3", "time": 2.15, "volume": 0.24},
        {"sfx": "whoosh_cinematic_short.mp3", "time": 3.00, "volume": 0.22},
    ]
    merged_sfx = sorted(hook_sfx + later_sfx, key=lambda x: float(x.get("time", 0.0)))
    filtered_sfx = []
    last_t = -1.0
    for ev in merged_sfx:
        t = float(ev.get("time", 0.0))
        if t - last_t >= 0.25:
            filtered_sfx.append(ev)
            last_t = t
    tl["sfx_events"] = filtered_sfx
    return tl


def main() -> None:
    banner("DỰNG BẢN -2: QUANG LIÊM THẮNG VÁN CỜ CHÍNH XÁC 99% (3S ĐẦU KÍCH THÍCH)")
    CTX.ensure_dirs()

    work_proj_dir = os.path.join(CTX.work_shorts_dir, "short_5_v2")
    if os.path.exists(work_proj_dir):
        shutil.move(work_proj_dir, os.path.join(Path.home(), ".Trash", f"12_11_ql_v2_{os.getpid()}"))

    step("1. Export timeline gốc Tin #05 sang thư mục WORK độc lập...")
    pdir, tl_path, _ = export_bridge_project(
        day_dir=str(CTX.day_dir),
        item_id="5",
        format_type="short",
        work_proj_dir=work_proj_dir,
        global_offset_sec=0.0,
    )

    step("2. Áp dụng Opening Hook 3s đầu (giữ nguyên toàn bộ câu 1..5 & 2 đồ thị DataViz)...")
    with open(tl_path, "r", encoding="utf-8") as fh:
        tl = json.load(fh)
    tl = build_v2_opening_hook(tl)
    with open(tl_path, "w", encoding="utf-8") as fh:
        json.dump(tl, fh, ensure_ascii=False, indent=2)

    step("3. Render MP4 qua HTML engine v2 (short_news_v2.html)...")
    out_work_mp4 = render_html_engine(
        project_dir=str(pdir),
        template="short_news_v2.html",
        scene_number=None,
        fps=30,
        preview=False,
        force=True,
    )
    if not out_work_mp4 or not os.path.exists(out_work_mp4):
        die("Render HTML engine thất bại cho bản -2")

    out_mp4 = CTX.shorts_dir / f"{OUT_SLUG_V2}.mp4"
    shutil.copy2(out_work_mp4, str(out_mp4))
    trim_video_audio_drift(CTX, out_mp4, 52)

    loud = measure_loudness(str(out_mp4))
    if loud:
        ok(f"Xuất bản thành công: {out_mp4.name} | I={loud['input_i']} LUFS | TP={loud['input_tp']} dBTP")
    chk = subprocess.run(["python3", "-B", str(ROOT_DIR / "core" / "audio_check.py"), str(out_mp4)], check=False)
    if chk.returncode != 0:
        warn(f"audio_check trả về mã {chk.returncode} cho {out_mp4.name}")

    banner(f"HOÀN TẤT XUẤT BẢN {out_mp4.name}")


if __name__ == "__main__":
    main()
