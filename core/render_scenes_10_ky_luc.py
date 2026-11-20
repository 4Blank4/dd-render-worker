#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import subprocess
import time
import os

project = "10_ky_luc_bong_da"
scenes = list(range(2, 13))

print("=" * 60)
print(f"BẮT ĐẦU RENDER BATCH CẢNH 02 -> 12 CHO DỰ ÁN {project}")
print("=" * 60)

t_start = time.time()

for sc in scenes:
    t0 = time.time()
    print(f"\n>>> [RENDER SCENE {sc:02d}/12] Bắt đầu lúc {time.strftime('%H:%M:%S')}...")
    cmd = [sys.executable, "-B", "core/m4_render.py", project, "--scene", str(sc)]
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print(f"\n❌ LỖI TẠI CẢNH {sc:02d}! Dừng tiến trình.")
        sys.exit(res.returncode)
    el = time.time() - t0
    print(f"✅ [SCENE {sc:02d}/12 XONG] Thời gian: {el:.1f}s")

total_el = time.time() - t_start
print("\n" + "=" * 60)
print(f"🎉 TẤT CẢ 12 CẢNH ĐÃ RENDER XONG TRONG {total_el/60:.2f} PHÚT!")
print("=" * 60)
