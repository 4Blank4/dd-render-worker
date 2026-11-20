#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

"""
m0 — VALIDATE (schema gate)
============================
Cổng kiểm tra nhanh TRƯỚC khi tốn thời gian render.
Chỉ kiểm tra tĩnh (schema + semantic anchoring + nhịp). Không mở trình duyệt.
Muốn kiểm tra layout/ảnh → dùng m5_qa.py.

Cách dùng:
  python3 m0_validate.py <project>
  python3 m0_validate.py <project> --strict   # coi cảnh báo là lỗi
"""

import argparse
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core"))
sys.path.insert(0, os.path.join(_ROOT, "spec"))

from diemdoc import paths
from diemdoc.log import banner, err as _err, log, ok, step, warn
from diemdoc.timeline import cards_of, load_timeline

import schema as S


def main() -> None:
    ap = argparse.ArgumentParser(description="m0 — validate timeline")
    ap.add_argument("project")
    ap.add_argument("--strict", action="store_true", help="Cảnh báo cũng tính là lỗi")
    args = ap.parse_args()

    banner("M0 — VALIDATE", args.project)
    pdir = paths.project_dir(args.project)

    try:
        tl = load_timeline(pdir)
    except FileNotFoundError as e:
        _err(str(e))
        sys.exit(1)

    step(f"Kiểm tra timeline ({tl.get('format', '?').upper()})")
    errors, warnings = S.validate_timeline(tl)

    info = [w for w in warnings if w.startswith("__info__")]
    real = [w for w in warnings if not w.startswith("__info__")]

    for e in errors:
        _err("  " + e)
    for w in real:
        warn("  " + w)
    for i in info:
        log("  " + i.replace("__info__ ", ""))

    n_cards = sum(len(cards_of(sc)) for sc in tl.get("scenes", []))
    engines: dict[str, int] = {}
    for sc in tl.get("scenes", []):
        for c in cards_of(sc):
            e = c.get("engine") or S.COMPONENTS.get(c.get("type", ""), {}).get("engine", "html")
            engines[e] = engines.get(e, 0) + 1

    print()
    log(f"Cảnh: {len(tl.get('scenes', []))}   Card: {n_cards}   "
        f"Engine: {', '.join(f'{k}={v}' for k, v in sorted(engines.items()))}", tag="m0")

    if errors:
        print()
        _err(f"THẤT BẠI: {len(errors)} lỗi.")
        sys.exit(1)
    if real and args.strict:
        _err(f"THẤT BẠI (--strict): {len(real)} cảnh báo.")
        sys.exit(1)

    ok(f"HỢP LỆ{f' ({len(real)} cảnh báo)' if real else ''}.")


if __name__ == "__main__":
    main()