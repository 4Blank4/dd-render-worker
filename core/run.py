#!/usr/bin/env python3
"""
run — BỘ ĐIỀU PHỐI PIPELINE ĐIỂM ĐỌC
=====================================
Chạy trọn chuỗi từ timeline → xuất bản cho kênh Điểm Đọc.
Các bước:
  m2_timeline_builder (nếu cần) → m3_voice → m4_render → m5_qa → m6_compose → m7_publish

Cách dùng:
  python3 core/run.py <project>                     # chạy toàn bộ
  python3 core/run.py <project> --stop-at render    # dừng sau render
  python3 core/run.py <project> --scene 2           # chỉ render & QA cảnh 2
  python3 core/run.py <project> --preview           # render preview nhanh
  python3 core/run.py <project> --only-qa           # chỉ chạy QA (m5)
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import os
import subprocess
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.log import banner, die, err, log, ok, step, warn
from diemdoc.timeline import load_timeline

STEPS = ("timeline", "voice", "render", "qa", "compose", "publish")


def run(module: str, args: list[str], check: bool = True) -> int:
    """Chạy một module con qua subprocess."""
    script = os.path.join(_HERE, module)
    cmd = [sys.executable, script] + args
    log(f"Chạy: {module} {' '.join(args)}", tag="run")
    p = subprocess.run(cmd)
    if check and p.returncode != 0:
        die(f"Bước {module} thất bại (exit {p.returncode}). Dừng pipeline.")
    return p.returncode


def main() -> None:
    ap = argparse.ArgumentParser(description="run — bộ điều phối pipeline Điểm Đọc")
    ap.add_argument("project", help="Tên project (thư mục trong projects/)")
    ap.add_argument("--stop-at", choices=STEPS, default=None, help="Dừng lại SAU bước này")
    ap.add_argument("--scene", type=int, default=None, help="Chỉ làm 1 cảnh (render/compose)")
    ap.add_argument("--format", choices=["short", "long", "main"], default=None)
    ap.add_argument("--preview", action="store_true", help="Render preview (15fps, 50% size)")
    ap.add_argument("--force", action="store_true", help="Bỏ qua cache render")
    ap.add_argument("--sync", choices=["whisper", "syllabic"], default="syllabic")
    ap.add_argument("--voice", default=None)
    ap.add_argument("--xfade", action="store_true", help="Nối cảnh mượt (m6)")
    ap.add_argument("--normalize", action="store_true", help="Chuẩn hóa timeline trước khi chạy")
    ap.add_argument("--qa-shots", action="store_true", help="Xuất contact sheet khi QA")
    ap.add_argument("--only-qa", action="store_true", help="Chỉ chạy QA (m5)")
    ap.add_argument("--skip-voice", action="store_true", help="Bỏ qua bước sinh giọng")
    args = ap.parse_args()

    banner("PIPELINE — ĐIỂM ĐỌC", args.project)
    pdir = paths.project_dir(args.project)
    tl_file = paths.project_file(args.project, "video_timeline.json")
    t0 = time.time()

    markers: dict[str, bool] = {}

    def past(stage: str) -> bool:
        return args.stop_at is not None and STEPS.index(stage) > STEPS.index(args.stop_at)

    # ── m2: TIMELINE ──────────────────────────────────────────────────────
    if not args.only_qa and (args.normalize or not os.path.exists(tl_file)):
        step("BƯỚC 1/6 — TIMELINE (m2)")
        a = [args.project]
        if args.normalize:
            a += ["--normalize"]
        if args.format:
            a += ["--format", args.format]
        run("m2_timeline_builder.py", a)
        markers["timeline"] = True
    else:
        log("Timeline đã có — bỏ qua bước sinh.", tag="run")
        markers["timeline"] = os.path.exists(tl_file)

    if not os.path.exists(tl_file):
        die(f"Không có timeline: {tl_file}")
    tl = load_timeline(pdir)
    n_sc = len(tl.get("scenes", []))
    log(f"Timeline: {n_sc} cảnh, format={tl.get('format')}", tag="run")

    if past("voice"):
        _finish(t0, args)
        return

    # ── m3: VOICE + SYNC ──────────────────────────────────────────────────
    if not args.only_qa and not args.skip_voice:
        m3_script = os.path.join(_HERE, "m3_voice.py")
        if os.path.exists(m3_script):
            step("BƯỚC 2/6 — VOICE & SYNC (m3)")
            a = [args.project, "--sync", args.sync]
            if args.scene:
                a += ["--scene", str(args.scene)]
            if args.voice:
                a += ["--voice", args.voice]
            run("m3_voice.py", a)
        else:
            voice_file = os.path.join(pdir, "voiceover.wav")
            if os.path.exists(voice_file):
                log("Đã có voiceover.wav sẵn — bỏ qua m3.", tag="run")
            else:
                warn("Chưa có m3_voice.py và chưa có voiceover.wav. Tiếp tục render không tiếng.")

    if past("render"):
        _finish(t0, args)
        return

    # ── m4: RENDER ────────────────────────────────────────────────────────
    if not args.only_qa:
        step("BƯỚC 3/6 — RENDER (m4)")
        a = [args.project]
        if args.scene:
            a += ["--scene", str(args.scene)]
        if args.format:
            a += ["--format", args.format]
        if args.preview:
            a += ["--preview"]
        if args.force:
            a += ["--force"]
        run("m4_render.py", a)

    if past("qa"):
        _finish(t0, args)
        return

    # ── m5: QA ────────────────────────────────────────────────────────────
    step("BƯỚC 4/6 — QA (m5)")
    a = [args.project]
    if args.qa_shots:
        a += ["--shots"]
    code = run("m5_qa.py", a, check=False)
    if code != 0:
        warn("QA phát hiện CẢNH BÁO/LỖI. Xem báo cáo ở trên rồi sửa timeline.")

    if past("compose"):
        _finish(t0, args)
        return

    # ── m6: COMPOSE ───────────────────────────────────────────────────────
    if not args.only_qa:
        step("BƯỚC 5/6 — COMPOSE (m6)")
        a = [args.project]
        if args.xfade:
            a += ["--xfade"]
        run("m6_compose.py", a)

    if past("publish"):
        _finish(t0, args)
        return

    # ── m7: PUBLISH PACK ──────────────────────────────────────────────────
    if not args.only_qa:
        step("BƯỚC 6/6 — PUBLISH PACK (m7)")
        a = [args.project]
        run("m7_publish.py", a)

    _finish(t0, args)


def _finish(t0: float, args: argparse.Namespace) -> None:
    dt = time.time() - t0
    print()
    ok(f"HOÀN THÀNH: project '{args.project}' trong {dt:.1f}s.")


if __name__ == "__main__":
    main()