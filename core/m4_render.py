#!/usr/bin/env python3
"""
m4 — RENDER (Router cho Điểm Đọc)
=================================
Cổng vào duy nhất cho việc render:
  1. Đọc timeline, xác định format + template.
  2. Phân phối cho engine HTML Playwright (đồng hồ ảo virtual-time shim).
  3. Render deterministic từng khung hình và pipe trực tiếp vào FFmpeg.

Cách dùng:
  python3 core/m4_render.py <project>                    # render cả video
  python3 core/m4_render.py <project> --scene 3          # render 1 cảnh
  python3 core/m4_render.py <project> --preview          # duyệt nhanh (15fps, 50%)
  python3 core/m4_render.py <project> --fps 30          # chọn tốc độ khung hình
  python3 core/m4_render.py <project> --force            # bỏ cache
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.timeline import cards_of, load_timeline, total_duration

sys.path.insert(0, os.path.join(_ROOT, "spec"))
import schema as S

GLOBAL_ENGINES = {"html", "gsap", "d3"}          # render bởi engine HTML
CLIP_ENGINES: set[str] = set()                   # Đã loại bỏ Manim hoàn toàn


def plan_engines(tl: dict) -> dict[str, list[dict]]:
    """Nhóm card theo engine để biết cần chạy engine nào."""
    plan: dict[str, list[dict]] = {}
    for sc in tl.get("scenes", []):
        for c in cards_of(sc):
            eng = c.get("engine") or S.COMPONENTS.get(c.get("type", ""), {}).get("engine", "html")
            plan.setdefault(eng, []).append(c)
    return plan


def main() -> None:
    ap = argparse.ArgumentParser(description="m4 — Render router Điểm Đọc (chọn engine & điều phối)")
    ap.add_argument("project")
    ap.add_argument("--scene", type=int, default=None)
    ap.add_argument("--template", default=None)
    ap.add_argument("--format", choices=list(S.FORMATS.keys()), default=None)
    ap.add_argument("--engine", default=None, help="Ép engine HTML cho toàn bộ (html/gsap/d3)")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--force", action="store_true", help="Bỏ qua cache, render lại")
    args = ap.parse_args()

    banner("M4 — RENDER", "Điểm Đọc")
    pdir = paths.project_dir(args.project)
    tl = load_timeline(pdir)

    plan = plan_engines(tl)
    step("Kế hoạch engine")
    for eng, cards in sorted(plan.items()):
        types = sorted({c.get("type") for c in cards})
        tag = "render trực tiếp"
        log(f"{eng:8s} {len(cards):3d} card  [{tag}]  types: {', '.join(types)[:90]}", tag="plan")

    unknown = set(plan) - GLOBAL_ENGINES - CLIP_ENGINES
    if unknown:
        warn(f"Engine chưa hỗ trợ: {', '.join(unknown)} — sẽ bỏ qua (card vẫn render bằng HTML).")

    # ---- 1. Engine HTML (luôn chạy — nó dựng cả nền và các card HTML) ----
    step("Engine HTML")
    html_renderer = _load("engines/html/renderer.py", "html_renderer")
    out = html_renderer.render_html_engine(
        pdir, args.template, args.scene, fps=args.fps,
        preview=args.preview, use_cache=not args.no_cache, force=args.force,
        format_override=args.format)

    print()
    if args.scene:
        ok(f"Cảnh {args.scene} xong. Tiếp: python3 core/m6_compose.py {args.project}")
    else:
        ok("Render xong. Tiếp: python3 core/m5_qa.py " + args.project + " hoặc core/m7_publish.py")


def _load(rel_path: str, name: str):
    """Nạp module từ đường dẫn file (tránh xung đột tên với package)."""
    import importlib.util
    full = os.path.join(_ROOT, rel_path)
    if not os.path.exists(full):
        die(f"Thiếu engine: {rel_path}")
    spec = importlib.util.spec_from_file_location(name, full)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


if __name__ == "__main__":
    main()