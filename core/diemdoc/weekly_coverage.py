#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/diemdoc/weekly_coverage.py — Kiểm Toán Khung Thời Gian & Độ Phủ Dữ Liệu Video Tuần
=======================================================================================
Chuẩn hóa bất biến Video Tuần kênh Điểm Đọc (UTC+7 / ICT):
  1. Khung thời gian tuần: luôn tính từ **00:01 Thứ Hai tuần trước** đến **23:59:59 Chủ Nhật tuần trước**.
     Ví dụ khi làm Video Tuần vào Thứ Hai 23.11.2026:
       - Tuần được tổng hợp: **16–22/11/2026** (Thứ Hai 16.11 -> Chủ Nhật 22.11).
       - Ngày cập nhật/xuất bản: **23/11/2026**.
       - Tuyệt đối KHÔNG ghi khoảng tuần bắt đầu từ Thứ Ba/Thứ Tư hay gộp ngày 23/11 vào tuần trước.
  2. Tận dụng dữ liệu ngày có sẵn + Bù ngày thiếu từ Internet:
     - Quét `outputs/<DD.MM.YYYY>/` để kiểm tra 7 ngày từ Thứ Hai đến Chủ Nhật.
     - Quy định riêng cho bản tin ngày gần nhất: Video ngày tạo từ `12:00 Chủ Nhật` đến `sáng Thứ Hai`
       (nằm ở thư mục ngày Thứ Hai, VD `outputs/23.11.2026/`) **được chấp nhận hợp lệ là dữ liệu của
       buổi chiều–đêm Chủ Nhật tuần trước (22/11)**.
     - Nếu bất kỳ ngày hoặc nửa ngày nào trong 7 ngày còn thiếu (như 16/11 và sáng 17/11),
       xuất danh sách cửa sổ thời gian cần tìm kiếm/cào bổ sung từ Internet (Báo VN + Thế Giới).
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.dirname(_HERE)
_ROOT = os.path.dirname(_CORE)

VI_WEEKDAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


def _extract_date_from_str(day_str: str) -> dt.date:
    cleaned = os.path.basename((day_str or "").rstrip("/")).strip()
    m = re.search(r"(\d{1,2})[._\-/](\d{1,2})[._\-/](\d{4})", cleaned)
    if not m:
        m = re.search(r"(\d{1,2})[._\-/](\d{1,2})[._\-/](\d{4})", day_str or "")
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return dt.date(y, mo, d)
    m_iso = re.search(r"(\d{4})[._\-/](\d{1,2})[._\-/](\d{1,2})", day_str or "")
    if m_iso:
        y, mo, d = int(m_iso.group(1)), int(m_iso.group(2)), int(m_iso.group(3))
        return dt.date(y, mo, d)
    return dt.date.today()


def resolve_weekly_dates(day_str_or_date: str) -> Dict[str, Any]:
    """
    Tính toán toàn bộ mốc ngày chuẩn của Video Tuần dựa trên ngày cập nhật (VD: Weekly-23.11.2026):
      - update_date: 2026-11-23
      - monday_date: 2026-11-16 (00:01:00)
      - sunday_date: 2026-11-22 (23:59:59)
      - week_range_slash: '16–22/11'
      - week_range_dot: '16–22.11'
      - date_chip: 'TUẦN 16–22.11 · CN 23.11.2026'
    """
    update_date = _extract_date_from_str(day_str_or_date)
    mon_this_week = update_date - dt.timedelta(days=update_date.weekday())
    monday_date = mon_this_week - dt.timedelta(days=7)
    sunday_date = monday_date + dt.timedelta(days=6)

    if monday_date.month == sunday_date.month and monday_date.year == sunday_date.year:
        range_slash = f"{monday_date.day:02d}–{sunday_date.day:02d}/{sunday_date.month:02d}"
        range_dot = f"{monday_date.day:02d}–{sunday_date.day:02d}.{sunday_date.month:02d}"
    else:
        range_slash = f"{monday_date.day:02d}/{monday_date.month:02d}–{sunday_date.day:02d}/{sunday_date.month:02d}"
        range_dot = f"{monday_date.day:02d}.{monday_date.month:02d}–{sunday_date.day:02d}.{sunday_date.month:02d}"

    return {
        "update_date": update_date,
        "update_str_dot": update_date.strftime("%d.%m.%Y"),
        "update_str_slash": update_date.strftime("%d/%m/%Y"),
        "monday_date": monday_date,
        "sunday_date": sunday_date,
        "since_dt": dt.datetime(monday_date.year, monday_date.month, monday_date.day, 0, 1, 0),
        "until_dt": dt.datetime(sunday_date.year, sunday_date.month, sunday_date.day, 23, 59, 59),
        "week_range_slash": range_slash,
        "week_range_dot": range_dot,
        "date_chip": f"TUẦN {range_dot} · CN {update_date.strftime('%d.%m.%Y')}",
    }


def format_weekly_date_chip(day_str: str) -> str:
    """Trả về chuỗi chip ngày chuẩn cho giao diện Video Tuần: `TUẦN DD–DD.MM · CN DD.MM.YYYY`."""
    return resolve_weekly_dates(day_str)["date_chip"]


def _is_valid_daily_folder(folder: Path) -> Tuple[bool, str]:
    """
    Kiểm tra thư mục `outputs/<DD.MM.YYYY>/` có phải bản tin ngày hợp lệ hay không
    (loại trừ trường hợp thư mục đó là video tổng hợp tuần cũ gắn `| Điểm Đọc Tuần`).
    """
    if not folder.exists() or not (folder / "thethao.json").exists():
        return False, "không tồn tại"
    mota_p = folder / "mota.txt"
    if mota_p.exists():
        try:
            txt = mota_p.read_text(encoding="utf-8")
            if "| Điểm Đọc Tuần" in txt or "VIDEO TỔNG HỢP TUẦN" in txt.upper():
                return False, "là video tổng hợp tuần trước (không phải bản tin ngày)"
        except Exception:
            pass
    try:
        items = json.loads((folder / "thethao.json").read_text(encoding="utf-8"))
        if isinstance(items, list) and len(items) > 0:
            return True, f"có {len(items)} tin ngày"
    except Exception:
        pass
    return False, "thethao.json rỗng hoặc lỗi"


def audit_weekly_local_coverage(day_str: str, outputs_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Kiểm tra độ phủ 7 ngày (Thứ Hai -> Chủ Nhật tuần trước) trong `outputs/`.
    - Mỗi bản tin ngày `<D>.MM.YYYY` mặc định phủ cửa sổ `[D-1 12:00 -> D 12:00]`.
    - Bản tin ngày của Thứ Hai đầu tuần này (`sunday_date + 1`, VD `23.11.2026`, cào từ
      12:00 Chủ Nhật tới sáng Thứ Hai) được chấp nhận hợp lệ là dữ liệu cho **Chủ Nhật**!
    - Trả về danh sách ngày/giờ đã phủ và ngày/giờ còn thiếu cần tìm thêm từ Internet.
    """
    out_dir = outputs_root or (Path(_ROOT) / "outputs")
    info = resolve_weekly_dates(day_str)
    mon: dt.date = info["monday_date"]
    sun: dt.date = info["sunday_date"]

    # Bản tin ngày có khả năng đóng góp từ [mon .. sun + 1]
    daily_status: Dict[dt.date, Tuple[bool, str, str]] = {}
    for offset in range(8):
        cur_d = mon + dt.timedelta(days=offset)
        f_name = cur_d.strftime("%d.%m.%Y")
        ok_daily, reason = _is_valid_daily_folder(out_dir / f_name)
        daily_status[cur_d] = (ok_daily, f_name, reason)

    reusable_folders: List[str] = [
        daily_status[mon + dt.timedelta(days=offset)][1]
        for offset in range(8)
        if daily_status[mon + dt.timedelta(days=offset)][0]
    ]

    day_reports: List[Dict[str, Any]] = []
    missing_intervals: List[Tuple[dt.datetime, dt.datetime, str]] = []
    covered_days: List[str] = []
    missing_days: List[str] = []

    for offset in range(7):
        cur_d = mon + dt.timedelta(days=offset)
        next_d = cur_d + dt.timedelta(days=1)
        am_ok, am_folder, am_reason = daily_status[cur_d]
        pm_ok, pm_folder, pm_reason = daily_status[next_d]

        label_vi = f"{VI_WEEKDAYS[cur_d.weekday()]} {cur_d.strftime('%d.%m.%Y')}"
        sources_used: List[str] = []
        if am_ok:
            sources_used.append(f"{am_folder} (00:01–12:00)")
        if pm_ok:
            note = " [bản tin 12h CN–sáng T2, hợp lệ cho CN]" if cur_d == sun else ""
            sources_used.append(f"{pm_folder} (12:00–23:59){note}")

        if am_ok and pm_ok:
            status = "FULL"
            covered_days.append(label_vi)
        elif am_ok or pm_ok:
            status = "PARTIAL"
            covered_days.append(f"{label_vi} (một phần)")
            missing_days.append(label_vi)
            if not am_ok:
                s_dt = dt.datetime(cur_d.year, cur_d.month, cur_d.day, 0, 1, 0)
                e_dt = dt.datetime(cur_d.year, cur_d.month, cur_d.day, 12, 0, 0)
                missing_intervals.append((s_dt, e_dt, f"Thiếu sáng {label_vi} ({am_folder}: {am_reason})"))
            if not pm_ok:
                s_dt = dt.datetime(cur_d.year, cur_d.month, cur_d.day, 12, 0, 0)
                e_dt = dt.datetime(cur_d.year, cur_d.month, cur_d.day, 23, 59, 59)
                missing_intervals.append((s_dt, e_dt, f"Thiếu chiều–tối {label_vi} ({pm_folder}: {pm_reason})"))
        else:
            status = "MISSING"
            missing_days.append(label_vi)
            s_dt = dt.datetime(cur_d.year, cur_d.month, cur_d.day, 0, 1, 0)
            e_dt = dt.datetime(cur_d.year, cur_d.month, cur_d.day, 23, 59, 59)
            missing_intervals.append((s_dt, e_dt, f"Thiếu trọn {label_vi}"))

        day_reports.append({
            "date": cur_d.strftime("%d.%m.%Y"),
            "weekday": VI_WEEKDAYS[cur_d.weekday()],
            "status": status,
            "sources": sources_used,
            "am_note": am_reason if not am_ok else "",
            "pm_note": pm_reason if not pm_ok else "",
        })

    # Gộp các khoảng thiếu liên tiếp nhau thành cửa sổ cào Internet gọn
    merged_windows: List[Dict[str, str]] = []
    for s_dt, e_dt, reason in missing_intervals:
        if merged_windows:
            prev_end = dt.datetime.strptime(merged_windows[-1]["to"], "%Y-%m-%d %H:%M")
            if (s_dt - prev_end).total_seconds() <= 120:
                merged_windows[-1]["to"] = e_dt.strftime("%Y-%m-%d %H:%M")
                merged_windows[-1]["reasons"].append(reason)
                continue
        merged_windows.append({
            "from": s_dt.strftime("%Y-%m-%d %H:%M"),
            "to": e_dt.strftime("%Y-%m-%d %H:%M"),
            "reasons": [reason],
        })

    return {
        **info,
        "reusable_daily_folders": reusable_folders,
        "day_reports": day_reports,
        "covered_week_days": covered_days,
        "missing_week_days": missing_days,
        "internet_fetch_windows": merged_windows,
        "is_full_week_covered_locally": len(merged_windows) == 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Kiểm toán độ phủ 7 ngày (00:01 Thứ Hai -> 23:59 Chủ Nhật) cho Video Tuần")
    parser.add_argument("--day", required=True, help="Mã dự án hoặc ngày xuất bản (VD: Weekly-23.11.2026 hoặc 23.11.2026)")
    args = parser.parse_args()

    rep = audit_weekly_local_coverage(args.day)
    print("=" * 74)
    print(f"KIỂM TOÁN KHUNG TUẦN CHUẨN — {args.day}")
    print("=" * 74)
    print(f"• Khoảng tuần tổng hợp : {rep['week_range_slash']} ({rep['monday_date'].strftime('%d/%m/%Y')} 00:01 -> {rep['sunday_date'].strftime('%d/%m/%Y')} 23:59)")
    print(f"• Ngày cập nhật        : {rep['update_str_slash']}")
    print(f"• Date-Chip chuẩn      : {rep['date_chip']}")
    print(f"• Dữ liệu ngày có sẵn  : {', '.join(rep['reusable_daily_folders']) or 'Không có'}")
    print("-" * 74)
    for dr in rep["day_reports"]:
        src_str = " + ".join(dr["sources"]) if dr["sources"] else f"TRỐNG ({dr['am_note']}; {dr['pm_note']})"
        print(f"  [{dr['status']:7s}] {dr['weekday']:8s} {dr['date']} -> {src_str}")
    print("-" * 74)
    if rep["internet_fetch_windows"]:
        print("[!] CẦN BỔ SUNG TỪ INTERNET (Báo VN + Thế Giới) cho đủ tuần Thứ Hai -> Chủ Nhật:")
        for mw in rep["internet_fetch_windows"]:
            print(f"    -> --since \"{mw['from']}\" --until \"{mw['to']}\" | Lý do: {'; '.join(mw['reasons'])}")
    else:
        print("[ok] ĐÃ PHỦ ĐỦ 100% CẢ 7 NGÀY TUẦN TRƯỚC TỪ DỮ LIỆU LOCAL.")


if __name__ == "__main__":
    main()
