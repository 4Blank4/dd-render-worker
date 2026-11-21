#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/cloud_runner.py — Bộ Điều Phối Đám Mây GitHub Actions (Zero-RAM Local Orchestrator)
========================================================================================
Cho phép đẩy riêng 2 khâu NẶNG NHẤT (Tổng hợp Giọng đọc ViTTS + Render Video HTML v2)
lên dàn máy ảo GitHub Actions (Matrix 1–15 máy ảo x 16 GB RAM chạy song song),
giải phóng 100% CPU và RAM cho máy Mac của Chủ kênh.

Sau khi GitHub hoàn tất:
  1. Tự động tải toàn bộ thành phẩm (`.mp4`, `.wav`, `thumbnail*.jpg`, `_mota.txt`, `chapters*.json`)
     về đúng thư mục `outputs/<DD.MM.YYYY>/` hoặc `outputs/Orther/<DD.MM.YYYY>/` trên Google Drive.
  2. Tự động XÓA SẠCH gói dữ liệu `_cloud_job/` trên GitHub và xóa luôn các GitHub Artifacts/Run logs
     để kho GitHub luôn rỗng, không lưu dữ liệu và không tốn dung lượng.
  3. Giữ nguyên 100% cấu trúc local (`daily_runner.py`, `short_batch.py`) để bất cứ lúc nào cũng
     có thể chạy local hoặc fallback về máy Mac nếu muốn.

Cách dùng:
  # 0. Khởi tạo & kết nối GitHub Repo lần đầu (hoặc kiểm tra trạng thái):
  python3 -B core/cloud_runner.py --init-repo

  # 1. Chạy Video Bản Tin Dài 16:9 hằng ngày / hằng tuần trên GitHub (chia 8 máy ảo song song):
  python3 -B core/cloud_runner.py --day 20.11.2026 --mode daily_long --shards 8

  # 2. Chạy lô Video Shorts 9:16 chuyên đề riêng lẻ (outputs/Orther/<DD.MM.YYYY>/):
  python3 -B core/cloud_runner.py --day 20.11.2026 --mode short_batch --orther --shards 3

  # 3. Chạy Video Short Bản Tin Nhanh (Digest Short 18-26 tin < 3 phút):
  python3 -B core/cloud_runner.py --day 20.11.2026 --mode digest_short

  # 4. Chỉ dọn sạch dữ liệu & artifacts trên GitHub ngay lập tức:
  python3 -B core/cloud_runner.py --cleanup-only
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse
import datetime as dt
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc import paths
from diemdoc.log import banner, die, log, ok, step, warn
from qa_precheck import run_qa

ROOT = Path(_ROOT)
CLOUD_CFG_PATH = ROOT / "config" / "cloud.json"
JOB_DIR = ROOT / "_cloud_job"

DEFAULT_CLOUD_CONFIG = {
    "github_owner": "4Blank4",
    "repo_name": "dd-render-worker",
    "visibility": "public",
    "branch": "main",
    "workflow_file": "cloud_render.yml",
    "default_shards_daily": 8,
    "default_shards_short": 3,
    "workers_per_shard": 2,
    "auto_cleanup_github": True,
}


def load_cloud_config() -> Dict[str, Any]:
    if CLOUD_CFG_PATH.exists():
        try:
            cfg = dict(DEFAULT_CLOUD_CONFIG)
            cfg.update(json.loads(CLOUD_CFG_PATH.read_text(encoding="utf-8")))
            return cfg
        except Exception:
            pass
    CLOUD_CFG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLOUD_CFG_PATH.write_text(json.dumps(DEFAULT_CLOUD_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")
    return dict(DEFAULT_CLOUD_CONFIG)


def _run_cmd(cmd: List[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    res = subprocess.run(cmd, cwd=str(ROOT), capture_output=capture, text=True)
    if check and res.returncode != 0:
        err_out = (res.stderr or res.stdout or "").strip()
        die(f"Lệnh thất bại: {' '.join(cmd)}\n{err_out[-1200:]}")
    return res


def _safe_trash(target: Path) -> None:
    """Di chuyển file/thư mục tạm vào ~/.Trash theo đúng Safe Trash Policy của AGENTS.md."""
    if not target.exists():
        return
    trash_dir = Path.home() / ".Trash"
    trash_dir.mkdir(parents=True, exist_ok=True)
    stamp = f"{target.name}_{int(time.time())}_{os.getpid()}"
    shutil.move(str(target), str(trash_dir / stamp))


def ensure_github_repo(cfg: Dict[str, Any]) -> str:
    """
    Đảm bảo thư mục DD-The-thao đã được khởi tạo Git và kết nối với repo Public trên GitHub
    (chỉ đẩy bộ khung Engine nhẹ, hoàn toàn bỏ qua outputs/, projects/, _ref/ nhờ .gitignore).
    """
    owner = cfg["github_owner"]
    repo = cfg["repo_name"]
    full_repo = f"{owner}/{repo}"
    branch = cfg.get("branch", "main")

    step(f"Kiểm tra kết nối GitHub Repository: {full_repo} ({cfg['visibility']})...")
    chk_gh = _run_cmd(["gh", "auth", "status"], check=False)
    if chk_gh.returncode != 0:
        die("Chưa đăng nhập GitHub CLI (`gh`). Hãy chạy `gh auth login` trước.")

    if not (ROOT / ".git").exists():
        step("Khởi tạo Git repository cục bộ...")
        _run_cmd(["git", "init", "-b", branch])

    # Kiểm tra repo trên GitHub đã tồn tại chưa
    repo_view = _run_cmd(["gh", "repo", "view", full_repo, "--json", "name,visibility"], check=False)
    if repo_view.returncode != 0:
        step(f"Tạo repository mới trên GitHub: {full_repo} (--{cfg['visibility']})...")
        vis_flag = "--public" if cfg.get("visibility", "public") == "public" else "--private"
        _run_cmd([
            "gh", "repo", "create", full_repo, vis_flag,
            "--description", "DiemDoc Ephemeral Media Render Worker (Auto-cleaned after each job)",
        ])
        ok(f"Đã tạo repo GitHub: https://github.com/{full_repo}")

    remote_url = f"https://github.com/{full_repo}.git"
    rem = _run_cmd(["git", "remote"], check=False)
    if "origin" not in (rem.stdout or "").split():
        _run_cmd(["git", "remote", "add", "origin", remote_url])
    else:
        _run_cmd(["git", "remote", "set-url", "origin", remote_url])

    # Đảm bảo _cloud_job có file giữ chỗ trống khi khởi tạo
    JOB_DIR.mkdir(parents=True, exist_ok=True)
    keep = JOB_DIR / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")

    step("Đồng bộ bộ khung Engine lên GitHub (bỏ qua toàn bộ outputs/ & dữ liệu riêng)...")
    _run_cmd(["git", "add", "-A"])
    status = _run_cmd(["git", "status", "--porcelain"])
    if (status.stdout or "").strip():
        _run_cmd(["git", "commit", "-m", "chore: sync DiemDoc cloud render engine"])
    _run_cmd(["git", "branch", "-M", branch])
    _run_cmd(["git", "push", "-u", "origin", branch, "--force"])
    ok(f"Kho Engine trên GitHub đã sẵn sàng: https://github.com/{full_repo}")
    return full_repo


def stage_job_payload(day_str: str, mode: str, is_orther: bool) -> Tuple[Path, Dict[str, Any]]:
    """
    Đóng gói đúng dữ liệu đầu vào cần thiết của ngày chỉ định vào `_cloud_job/payload/` (~15–30 MB).
    Không sao chép các video `.mp4` cũ để gói tải lên nhẹ nhất có thể.
    """
    rel_day_dir = f"outputs/Orther/{day_str}" if is_orther else f"outputs/{day_str}"
    day_dir = ROOT / rel_day_dir
    if not day_dir.exists():
        die(f"Thư mục dữ liệu ngày không tồn tại: {day_dir}")

    _safe_trash(JOB_DIR)
    payload_dir = JOB_DIR / "payload"
    payload_dir.mkdir(parents=True, exist_ok=True)

    # Các file JSON cấu hình kịch bản
    for jf in (
        "thethao.json",
        "intro_hook.json",
        "image_plan.json",
        "image_credits.json",
        "thumbnails_plan.json",
        "manual_overrides.json",
        "shorts_spec.json",
        "digest_specs.json",
    ):
        src = day_dir / jf
        if src.exists():
            shutil.copy2(src, payload_dir / jf)

    if (day_dir / "shorts" / "digest_specs.json").exists():
        (payload_dir / "shorts").mkdir(parents=True, exist_ok=True)
        shutil.copy2(day_dir / "shorts" / "digest_specs.json", payload_dir / "shorts" / "digest_specs.json")

    # Thư mục ảnh đã duyệt QA (bắt buộc cho render)
    if (day_dir / "images").exists():
        if mode == "digest_short":
            # Chỉ đóng gói đúng những ảnh được dùng trong digest_specs.json + thumbnail để giữ Payload siêu nhẹ (~5-10 MB)
            spec_p = day_dir / "shorts" / "digest_specs.json"
            if not spec_p.exists():
                spec_p = day_dir / "digest_specs.json"
            needed_imgs = set()
            if spec_p.exists():
                cfg_d = json.loads(spec_p.read_text(encoding="utf-8"))
                d_items = cfg_d["items"] if isinstance(cfg_d, dict) and "items" in cfg_d else cfg_d
                for it in d_items:
                    if it.get("image_file"):
                        needed_imgs.add(it["image_file"])
                if isinstance(cfg_d, dict) and isinstance(cfg_d.get("thumb"), dict) and cfg_d["thumb"].get("image"):
                    needed_imgs.add(cfg_d["thumb"]["image"])
            if needed_imgs:
                (payload_dir / "images").mkdir(parents=True, exist_ok=True)
                for fn in sorted(needed_imgs):
                    src_img = day_dir / "images" / fn
                    if src_img.exists():
                        shutil.copy2(src_img, payload_dir / "images" / fn)
            else:
                shutil.copytree(day_dir / "images", payload_dir / "images")
        else:
            shutil.copytree(day_dir / "images", payload_dir / "images")

    # Với daily_long / short_batch: gửi kèm audio có sẵn để tận dụng cache; với digest_short thì không gửi (~800MB audio dài)
    if mode != "digest_short":
        for af in ("audio", "audio-title"):
            if (day_dir / af).exists():
                shutil.copytree(day_dir / af, payload_dir / af)

    manifest = {
        "job_id": f"{mode}_{day_str.replace('.', '_')}_{int(time.time())}",
        "day": day_str,
        "mode": mode,
        "is_orther": is_orther,
        "rel_day_dir": rel_day_dir,
        "created_at": dt.datetime.now().isoformat(),
    }
    (JOB_DIR / "job_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # Tính dung lượng gói payload
    total_bytes = sum(f.stat().st_size for f in JOB_DIR.rglob("*") if f.is_file())
    ok(f"Đã đóng gói Payload vào _cloud_job/ ({total_bytes / (1024 * 1024):.2f} MB)")
    return day_dir, manifest


def cleanup_github_job_and_runs(cfg: Dict[str, Any], run_id: Optional[str] = None) -> None:
    """
    Xóa sạch hoàn toàn dữ liệu bài viết/hình ảnh trong `_cloud_job/` trên GitHub
    và xóa luôn các Artifacts / Workflow Run để GitHub không lưu giữ bất kỳ dữ liệu nào.
    """
    full_repo = f"{cfg['github_owner']}/{cfg['repo_name']}"
    branch = cfg.get("branch", "main")
    step("Dọn sạch dữ liệu tạm `_cloud_job/` và Artifacts trên GitHub...")

    _safe_trash(JOB_DIR)
    JOB_DIR.mkdir(parents=True, exist_ok=True)
    (JOB_DIR / ".gitkeep").write_text("", encoding="utf-8")

    _run_cmd(["git", "add", "_cloud_job"])
    st = _run_cmd(["git", "status", "--porcelain", "_cloud_job"])
    if (st.stdout or "").strip():
        # Amend hoặc commit đè rồi force push để xóa cả lịch sử chứa ảnh/kịch bản của job vừa chạy
        _run_cmd(["git", "commit", "-m", "chore: wipe ephemeral _cloud_job payload after completion"])
        _run_cmd(["git", "push", "origin", branch, "--force"])
        ok("Đã xóa sạch `_cloud_job/` trên nhánh GitHub.")

    if run_id:
        # Xóa workflow run (bao gồm toàn bộ artifacts gắn với run đó)
        _run_cmd(["gh", "run", "delete", str(run_id), "--repo", full_repo], check=False)
        ok(f"Đã xóa Workflow Run & Artifacts #{run_id} trên GitHub.")


def trigger_and_wait_workflow(cfg: Dict[str, Any], shards: int, workers_per_shard: int) -> str:
    full_repo = f"{cfg['github_owner']}/{cfg['repo_name']}"
    branch = cfg.get("branch", "main")
    wf = cfg.get("workflow_file", "cloud_render.yml")

    step("Đẩy gói `_cloud_job/` lên GitHub...")
    _run_cmd(["git", "add", "-A"])
    st = _run_cmd(["git", "status", "--porcelain"])
    if (st.stdout or "").strip():
        _run_cmd(["git", "commit", "-m", "job: dispatch ephemeral render payload"])
    _run_cmd(["git", "push", "origin", branch, "--force"])

    step(f"Kích hoạt GitHub Actions Matrix ({shards} máy ảo song song x {workers_per_shard} workers)...")
    _run_cmd([
        "gh", "workflow", "run", wf,
        "--repo", full_repo,
        "--ref", branch,
        "-f", f"total_shards={shards}",
        "-f", f"workers_per_shard={workers_per_shard}",
    ])

    # Chờ vài giây để GitHub đăng ký Run ID mới
    time.sleep(5)
    run_id = ""
    for _ in range(12):
        res = _run_cmd([
            "gh", "run", "list",
            "--repo", full_repo,
            "--workflow", wf,
            "--limit", "1",
            "--json", "databaseId,status,conclusion",
        ])
        runs = json.loads(res.stdout or "[]")
        if runs:
            run_id = str(runs[0]["databaseId"])
            break
        time.sleep(3)

    if not run_id:
        die("Không tìm thấy Workflow Run vừa kích hoạt trên GitHub.")

    ok(f"Đã khởi chạy Cloud Job trên GitHub! Run ID: #{run_id}")
    log(f"Theo dõi tiến độ (0% tải máy Mac): https://github.com/{full_repo}/actions/runs/{run_id}")

    # Vòng lặp theo dõi nhẹ nhàng (mỗi 15 giây hỏi trạng thái 1 lần, tốn 0% CPU)
    t0 = time.time()
    while True:
        res = _run_cmd([
            "gh", "run", "view", run_id,
            "--repo", full_repo,
            "--json", "status,conclusion,jobs",
        ], check=False)
        if res.returncode == 0 and res.stdout:
            data = json.loads(res.stdout)
            status = data.get("status")
            conclusion = data.get("conclusion")
            jobs = data.get("jobs") or []
            done_jobs = sum(1 for j in jobs if j.get("status") == "completed")
            elapsed = int(time.time() - t0)
            mm, ss = divmod(elapsed, 60)
            print(f"\r  ⏳ [GitHub Cloud #{run_id}] Thời gian: {mm:02d}p{ss:02d}s | Trạng thái: {status} | Hoàn tất: {done_jobs}/{len(jobs)} máy ảo...", end="", flush=True)

            if status == "completed":
                print()
                if conclusion != "success":
                    die(f"GitHub Actions Run #{run_id} kết thúc với trạng thái: {conclusion}. Xem chi tiết bằng: gh run view {run_id} --repo {full_repo} --log-failed")
                ok(f"GitHub Cloud hoàn tất xuất sắc sau {mm:02d}p{ss:02d}s!")
                break
        time.sleep(15)

    return run_id


def _list_run_artifacts(cfg: Dict[str, Any], run_id: str) -> Dict[str, float]:
    """Trả về map {tên_artifact: size_mb} của một GitHub Actions Run."""
    full_repo = f"{cfg['github_owner']}/{cfg['repo_name']}"
    res = _run_cmd([
        "gh", "api", f"repos/{full_repo}/actions/runs/{run_id}/artifacts",
        "--jq", ".artifacts[] | [.name, .size_in_bytes] | @tsv",
    ], check=False)
    out: Dict[str, float] = {}
    if res.returncode == 0 and res.stdout:
        for line in res.stdout.splitlines():
            parts = line.strip().split("\t")
            if len(parts) == 2:
                try:
                    out[parts[0]] = int(parts[1]) / (1024.0 * 1024.0)
                except Exception:
                    out[parts[0]] = 0.0
    return out


def _copy_extracted_tier(src_dir: Path, day_dir: Path, mode: str) -> List[str]:
    copied: List[str] = []
    for item in src_dir.rglob("*"):
        if not item.is_file() or item.name == ".tier_root":
            continue
        rel = item.relative_to(src_dir)
        dest = day_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest)
        copied.append(str(rel))

    if mode != "digest_short":
        for jf in ("thethao.json", "intro_hook.json"):
            jp = day_dir / jf
            if jp.exists() and jf in copied:
                data = json.loads(jp.read_text(encoding="utf-8"))
                from cloud_worker import _fix_day_paths
                data = _fix_day_paths(data, day_dir)
                jp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return copied


def download_and_merge_deliverable(
    cfg: Dict[str, Any], run_id: str, day_dir: Path, mode: str = "daily_long", skip_extras: bool = False
) -> None:
    full_repo = f"{cfg['github_owner']}/{cfg['repo_name']}"
    dl_tmp = Path(paths.WORK) / f"cloud_dl_{run_id}"
    _safe_trash(dl_tmp)
    dl_tmp.mkdir(parents=True, exist_ok=True)

    avail = _list_run_artifacts(cfg, run_id)
    tiers: List[Tuple[str, str]] = []
    if "dd-meta-thumbs" in avail or "dd-video-deliverable" in avail:
        if "dd-meta-thumbs" in avail:
            tiers.append(("dd-meta-thumbs", "[1/3] Ưu tiên 1: Ảnh Thumbnail, Mô tả SEO & Metadata"))
        if "dd-video-deliverable" in avail:
            tiers.append(("dd-video-deliverable", "[2/3] Ưu tiên 2: Video thành phẩm (.mp4)"))
        if "dd-audio-extras" in avail:
            if skip_extras:
                warn(f"Bỏ qua tải dd-audio-extras ({avail['dd-audio-extras']:.2f} MB) theo cờ --skip-extras.")
            else:
                tiers.append(("dd-audio-extras", "[3/3] Phần phụ: Âm thanh thô (.wav)"))
    elif "dd-final-deliverable" in avail or not avail:
        tiers.append(("dd-final-deliverable", "Tải toàn bộ thành phẩm (legacy single artifact)"))

    copied_files: List[str] = []
    for art_name, label in tiers:
        sz_mb = avail.get(art_name, 0.0)
        tier_tmp = dl_tmp / art_name
        tier_tmp.mkdir(parents=True, exist_ok=True)
        step(f"{label} ({sz_mb:.2f} MB) từ Run #{run_id}...")
        _run_cmd([
            "gh", "run", "download", run_id,
            "--repo", full_repo,
            "-n", art_name,
            "-D", str(tier_tmp),
        ])
        tier_copied = _copy_extracted_tier(tier_tmp, day_dir, mode=mode)
        copied_files.extend(tier_copied)
        ok(f"Xong {label}: đã lưu {len(tier_copied)} file vào {paths.rel_to_root(str(day_dir))}")
        for cf in sorted(tier_copied):
            if cf.endswith((".mp4", ".jpg", ".txt", ".json")):
                log(f"  + {cf}")

    _safe_trash(dl_tmp)
    ok(f"Hoàn tất tải theo thứ tự ưu tiên ({len(copied_files)} file) -> {paths.rel_to_root(str(day_dir))}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bộ điều phối Render Đám Mây GitHub Actions (Điểm Đọc)")
    parser.add_argument("--init-repo", action="store_true", help="Khởi tạo & đồng bộ bộ khung Engine lên GitHub Repo")
    parser.add_argument("--cleanup-only", action="store_true", help="Xóa sạch dữ liệu trong _cloud_job/ trên GitHub")
    parser.add_argument("--day", help="Ngày sản xuất định dạng DD.MM.YYYY (VD: 20.11.2026)")
    parser.add_argument("--mode", choices=["daily_long", "short_batch", "digest_short"], default="daily_long",
                        help="Loại video cần xử lý trên GitHub (daily_long | short_batch | digest_short)")
    parser.add_argument("--orther", action="store_true", help="Dùng thư mục outputs/Orther/<DD.MM.YYYY>/ (cho video Shorts/chuyên đề lẻ)")
    parser.add_argument("--shards", type=int, default=0, help="Số máy ảo GitHub chạy song song (mặc định: 8 cho daily_long, 3 cho short_batch, 1 cho digest_short)")
    parser.add_argument("--workers", type=int, default=2, help="Số luồng Playwright trên mỗi máy ảo GitHub (mặc định: 2)")
    parser.add_argument("--skip-qa", action="store_true", help="Bỏ qua bước kiểm tra qa_precheck.py trên máy trước khi gửi")
    parser.add_argument("--skip-extras", action="store_true", help="Chỉ tải Thumbnail/Mô tả và Video chính (.mp4), bỏ qua tải file âm thanh thô (.wav)")
    parser.add_argument("--keep-cloud-data", action="store_true", help="Không tự xóa Artifact sau khi tải về (dùng khi cần debug)")
    args = parser.parse_args()

    cfg = load_cloud_config()

    if args.init_repo:
        banner("KHỞI TẠO & KẾT NỐI TRẠM RENDER GITHUB ACTIONS (ĐIỂM ĐỌC)")
        ensure_github_repo(cfg)
        return

    if args.cleanup_only:
        banner("DỌN SẠCH DỮ LIỆU TẠM TRÊN GITHUB")
        ensure_github_repo(cfg)
        cleanup_github_job_and_runs(cfg)
        return

    if not args.day:
        die("Vui lòng chỉ định `--day DD.MM.YYYY` (hoặc `--init-repo` / `--cleanup-only`).")

    if args.mode == "daily_long" and not args.skip_qa and not args.orther:
        errs, _ = run_qa(args.day)
        if errs > 0:
            die("Dừng đẩy lên Cloud vì Auto-QA phát hiện lỗi cần sửa trước.")

    shards = args.shards
    if shards <= 0:
        if args.mode == "daily_long":
            shards = int(cfg.get("default_shards_daily", 8))
        elif args.mode == "short_batch":
            shards = int(cfg.get("default_shards_short", 3))
        else:
            shards = 1

    banner(
        f"ĐẨY TÁC VỤ NẶNG (TTS + RENDER) LÊN GITHUB CLOUD — {args.day}",
        f"Chế độ: {args.mode} | Số máy ảo song song: {shards} | Thư mục: {'outputs/Orther/' if args.orther else 'outputs/'}{args.day}",
    )

    ensure_github_repo(cfg)
    day_dir, _ = stage_job_payload(args.day, args.mode, args.orther)
    run_id = trigger_and_wait_workflow(cfg, shards=shards, workers_per_shard=args.workers)

    try:
        download_and_merge_deliverable(cfg, run_id, day_dir, mode=args.mode, skip_extras=args.skip_extras)
    finally:
        if cfg.get("auto_cleanup_github", True) and not args.keep_cloud_data:
            cleanup_github_job_and_runs(cfg, run_id=run_id)

    banner(f"HOÀN TẤT XUẤT BẢN ĐÁM MÂY NGÀY {args.day} — DỮ LIỆU GITHUB ĐÃ XÓA SẠCH 100%")


if __name__ == "__main__":
    main()
