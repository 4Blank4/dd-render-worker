#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
clean.py — DỌN DẸP THƯ MỤC LÀM VIỆC TẠM NGOÀI DRIVE CHO ĐIỂM ĐỌC
================================================================
Quét thư mục work_dir (mặc định ~/Library/Caches/DiemDoc),
chuyển toàn bộ (hoặc các tệp/thư mục tạm cũ hơn retention_days) vào ~/.Trash/.
Mặc định --days 0 (dọn sạch toàn bộ cache tạm ngay khi bắt đầu hoặc kết thúc tác vụ).
TUYỆT ĐỐI KHÔNG ĐỤNG ĐẾN DD-The-thao/outputs/!

Cách dùng:
  python3 -B core/clean.py --dry-run        # Chế độ xem thử (mặc định)
  python3 -B core/clean.py --apply          # Thực hiện dọn sạch toàn bộ cache tạm vào ~/.Trash
  python3 -B core/clean.py --days 1 --apply # Dọn các mục cũ hơn 1 ngày
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import os
import shutil
import time
from typing import List, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if os.path.join(_ROOT, "core") not in sys.path:
    sys.path.insert(0, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.log import banner, log, ok, warn


def send_to_trash(target_path: str) -> bool:
    """Di chuyển file/folder vào ~/.Trash an toàn thay vì rm -rf."""
    trash_dir = os.path.expanduser("~/.Trash")
    os.makedirs(trash_dir, exist_ok=True)
    base_name = os.path.basename(target_path.rstrip("/"))
    stamp = f"{int(time.time() * 1000)}"
    dest = os.path.join(trash_dir, f"{base_name}_{stamp}")
    try:
        shutil.move(target_path, dest)
        return True
    except Exception as e:
        warn(f"Không thể chuyển vào Trash ({base_name}): {e}")
        return False


def get_dir_size_mb(path: str) -> float:
    total = 0
    try:
        if os.path.isfile(path) or os.path.islink(path):
            return os.path.getsize(path) / (1024 * 1024)
        for root, _, files in os.walk(path):
            for fn in files:
                fp = os.path.join(root, fn)
                try:
                    if not os.path.islink(fp):
                        total += os.path.getsize(fp)
                except Exception:
                    pass
    except Exception:
        pass
    return total / (1024 * 1024)


def clean_work_dir(
    days: float = 0.0,
    apply: bool = False,
    exclude_names: Optional[List[str]] = None,
    quiet: bool = False,
) -> int:
    work_dir = paths.WORK
    if not os.path.exists(work_dir):
        if not quiet:
            ok(f"Thư mục làm việc tạm rỗng hoặc chưa tạo: {work_dir}")
        return 0

    excl = set(exclude_names or [])
    now = time.time()
    cutoff_sec = max(0.0, float(days)) * 86400.0

    items = sorted(os.listdir(work_dir))
    to_delete = []

    for item in items:
        if item in excl:
            continue
        ip = os.path.join(work_dir, item)
        try:
            mtime = os.path.getmtime(ip)
            age_days = max(0.0, (now - mtime) / 86400.0)
            if days <= 0 or (now - mtime) >= cutoff_sec:
                size_mb = get_dir_size_mb(ip)
                to_delete.append((ip, age_days, size_mb))
        except Exception:
            pass

    total_mb = sum(x[2] for x in to_delete)
    if not quiet:
        log(f"Thư mục kiểm tra: {work_dir}")
        log(
            f"Tổng số mục tìm thấy: {len(items)} | Mục cần dọn (>= {days:g} ngày): "
            f"{len(to_delete)} (~{total_mb:.1f} MB)"
        )

    if not to_delete:
        if not quiet:
            ok("Thư mục tạm đã sạch 100%, không có tệp nào cần dọn.")
        return 0

    moved = 0
    for path, age, sz_mb in to_delete:
        tag_str = "[THƯ MỤC]" if os.path.isdir(path) else "[TỆP]"
        name = os.path.basename(path)
        if apply:
            if send_to_trash(path):
                moved += 1
                if not quiet:
                    log(f"Đã chuyển vào Trash: {tag_str} {name} ({sz_mb:.1f} MB | {age:.1f} ngày)")
        else:
            if not quiet:
                log(f"[DRY-RUN] Sẽ chuyển vào Trash: {tag_str} {name} ({sz_mb:.1f} MB | {age:.1f} ngày)")

    if not quiet:
        print()
        if not apply:
            warn("Đây là chế độ xem thử (Dry-run). Thêm cờ '--apply' để thực hiện chuyển vào ~/.Trash.")
        else:
            ok(f"Đã hoàn tất dọn dẹp an toàn {moved}/{len(to_delete)} mục (~{total_mb:.1f} MB) vào ~/.Trash.")
    return moved if apply else len(to_delete)


def main() -> None:
    ap = argparse.ArgumentParser(description="clean.py — Dọn dẹp cache tạm cho Điểm Đọc")
    ap.add_argument("--days", type=float, default=0.0, help="Số ngày lưu giữ (mặc định 0 = dọn sạch toàn bộ)")
    ap.add_argument("--all", action="store_true", help="Dọn sạch toàn bộ dữ liệu trong ~/Library/Caches/DiemDoc")
    ap.add_argument("--dry-run", action="store_true", help="Chỉ xem thử danh sách file sẽ dọn")
    ap.add_argument("--apply", action="store_true", help="Thực thi chuyển vào ~/.Trash")
    args = ap.parse_args()

    banner("DỌN DẸP THƯ MỤC TẠM", "Điểm Đọc")
    days = 0.0 if args.all else args.days
    apply_flag = bool(args.apply and not args.dry_run)
    clean_work_dir(days=days, apply=apply_flag, quiet=False)


if __name__ == "__main__":
    main()
