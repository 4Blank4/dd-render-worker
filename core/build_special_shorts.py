#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_special_shorts.py — Dựng Shorts 9:16 từ các cảnh của video chuyên đề
============================================================================
Mỗi cảnh (thethao.json item) => 1 video 9:16 trên template short_news_v2.html,
thời lượng bằng đúng audio của cảnh (tiêu đề + nội dung, 60–90 giây).

Cách chạy:
  python3 -B core/build_special_shorts.py 25.10.2026 2 3 6 8
  python3 -B core/build_special_shorts.py 25.10.2026 2 3 6 8 --force
"""
import sys
sys.dont_write_bytecode = True

import os
import shutil
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "vendor"))

from diemdoc import paths
from diemdoc.log import banner, ok, step, log
from m8_news_bridge import export_bridge_project


SLUGS = {
    1: "Ronaldo_Bo_Ve_Giua_Dem",
    2: "Loi_Hua_Bi_Pha_Vo",
    3: "Mot_Quoc_Gia_Bi_Chia_Re",
    4: "Ban_An_30_Ngay_255_Euro",
    5: "Hong_Phat_Den_Truoc_Neom_SC",
    6: "Ban_Thu_982_Tranh_Cai",
    7: "World_Cup_2026_Ky_Cuoi_Cung",
    8: "Cuoc_Dua_1000_Ban",
    9: "Ba_Kich_Ban_Cho_Chuong_Cuoi",
}


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)
    day_str = args[0]
    item_ids = [int(x) for x in args[1:]]

    day_dir = paths.project_dir(day_str)
    work_dir = paths.work_project_dir(day_str)
    shorts_out = os.path.join(day_dir, "shorts")
    os.makedirs(shorts_out, exist_ok=True)
    shorts_work = os.path.join(work_dir, "special_shorts")
    os.makedirs(shorts_work, exist_ok=True)

    banner(f"SHORTS CHUYÊN ĐỀ 9:16 — {day_str}", f"Cảnh: {', '.join(map(str, item_ids))}")

    # renderer.py được nạp theo kiểu script (run_day cũng vậy): thêm engines/html vào path
    engines_html = os.path.join(_ROOT, "engines", "html")
    if engines_html not in sys.path:
        sys.path.insert(0, engines_html)
    from renderer import render_html_engine

    t0 = time.time()
    done = []
    for n in item_ids:
        slug = SLUGS.get(n, f"Canh_{n:02d}")
        dest = os.path.join(shorts_out, f"Short_{n:02d}_{slug}.mp4")
        if os.path.exists(dest) and os.path.getsize(dest) > 1_000_000 and not force:
            ok(f"Short #{n:02d} đã có sẵn — bỏ qua (dùng --force để render lại): {dest}")
            done.append(dest)
            continue
        step(f"Xuất timeline short cho cảnh {n:02d}...")
        pdir, _, _ = export_bridge_project(
            day_dir, item_id=n, format_type="short",
            work_proj_dir=os.path.join(shorts_work, f"short_{n:02d}"),
            global_offset_sec=0.0)
        step(f"Render 9:16 cảnh {n:02d} trên short_news_v2.html...")
        v = render_html_engine(pdir, template="short_news_v2.html", scene_number=None,
                               fps=30, preview=False, force=True)
        if v and os.path.exists(v):
            shutil.copy2(v, dest)
            ok(f"🎉 Short {n:02d}: {paths.rel_to_root(dest)}")
            done.append(dest)
        else:
            log(f"!! Render cảnh {n:02d} thất bại", tag="shorts")

    print()
    banner(f"HOÀN TẤT {len(done)}/{len(item_ids)} SHORTS ({time.time()-t0:.0f}s)")
    for d in done:
        log(f"  📱 {paths.rel_to_root(d)}")


if __name__ == "__main__":
    main()
