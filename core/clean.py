#!/usr/bin/env python3
"""
clean.py — DỌN DẸP THƯ MỤC LÀM VIỆC TẠM NGOÀI DRIVE CHO ĐIỂM ĐỌC
================================================================
Quét thư mục work_dir (mặc định ~/Library/Caches/DiemDoc),
chuyển các tệp/thư mục tạm cũ hơn retention_days vào ~/.Trash/.
TUYỆT ĐỐI KHÔNG ĐỤNG ĐẾN DD-The-thao/outputs/!

Cách dùng:
  python3 core/clean.py                  # Chế độ xem thử (dry-run, mặc định)
  python3 core/clean.py --apply          # Thực hiện dọn dẹp thật
  python3 core/clean.py --days 7         # Dọn file cũ hơn 7 ngày
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import os
import shutil
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.log import banner, log, ok, warn


def send_to_trash(target_path: str) -> bool:
    """Di chuyển file/folder vào ~/.Trash an toàn thay vì rm -rf."""
    trash_dir = os.path.expanduser("~/.Trash")
    os.makedirs(trash_dir, exist_ok=True)
    base_name = os.path.basename(target_path)
    dest = os.path.join(trash_dir, f"{base_name}_{int(time.time())}")
    try:
        shutil.move(target_path, dest)
        return True
    except Exception as e:
        warn(f"Không thể chuyển vào Trash: {e}")
        return False


def main() -> None:
    ap = argparse.ArgumentParser(description="clean.py — Dọn dẹp cache tạm cho Điểm Đọc")
    ap.add_argument("--days", type=int, default=14, help="Số ngày lưu giữ (mặc định 14)")
    ap.add_argument("--apply", action="store_true", help="Thực thi xóa (nếu không có cờ này, chỉ chạy dry-run)")
    args = ap.parse_args()

    banner("DỌN DẸP THƯ MỤC TẠM", "Điểm Đọc")

    work_dir = paths.WORK
    if not os.path.exists(work_dir):
        ok(f"Thư mục làm việc tạm rỗng hoặc chưa tạo: {work_dir}")
        return

    now = time.time()
    cutoff_sec = args.days * 86400

    items = os.listdir(work_dir)
    to_delete = []

    for item in items:
        ip = os.path.join(work_dir, item)
        try:
            mtime = os.path.getmtime(ip)
            age_days = (now - mtime) / 86400.0
            if (now - mtime) > cutoff_sec:
                to_delete.append((ip, age_days))
        except Exception:
            pass

    log(f"Thư mục kiểm tra: {work_dir}")
    log(f"Tổng số mục tìm thấy: {len(items)} | Mục cũ hơn {args.days} ngày: {len(to_delete)}")

    if not to_delete:
        ok("Không có tệp tạm nào quá hạn cần dọn.")
        return

    for path, age in to_delete:
        tag_str = "[THƯ MỤC]" if os.path.isdir(path) else "[TỆP]"
        if args.apply:
            if send_to_trash(path):
                log(f"Đã chuyển vào Trash: {tag_str} {os.path.basename(path)} ({age:.1f} ngày tuổi)")
        else:
            log(f"[DRY-RUN] Sẽ chuyển vào Trash: {tag_str} {os.path.basename(path)} ({age:.1f} ngày tuổi)")

    if not args.apply:
        print()
        warn("Đây là chế độ xem thử (Dry-run). Thêm cờ '--apply' để thực hiện chuyển vào ~/.Trash.")
    else:
        print()
        ok("Đã hoàn tất dọn dẹp an toàn.")


if __name__ == "__main__":
    main()
