"""Path resolution — mọi đường dẫn tính từ ROOT của DD-The-thao. Portable 100%."""

from __future__ import annotations

import os
import sys
import json
from urllib.request import pathname2url

# Ngăn chặn sinh file .pyc và thư mục __pycache__ trên Google Drive
sys.dont_write_bytecode = True

# core/diemdoc/paths.py -> core/diemdoc -> core -> ROOT
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ASSETS = os.path.join(ROOT, "assets")
FONTS = os.path.join(ASSETS, "fonts")
SFX = os.path.join(ASSETS, "sfx")
BGM = os.path.join(ASSETS, "bgm")
ICONS = os.path.join(ASSETS, "icons")
LOGO = os.path.join(ASSETS, "logo")

CONFIG = os.path.join(ROOT, "config")
TEMPLATES = os.path.join(ROOT, "templates")
DESIGN = os.path.join(ROOT, "design")
SPEC = os.path.join(ROOT, "spec")
DATA = os.path.join(ROOT, "data")
PROJECTS = os.path.join(ROOT, "projects")
OUTPUTS = os.path.join(ROOT, "outputs")
ENGINES = os.path.join(ROOT, "engines")


def _resolve_work_dir() -> str:
    """Xác định thư mục làm việc tạm ngoài Google Drive."""
    cfg_path = os.path.join(CONFIG, "render.json")
    target_work = "~/Library/Caches/DiemDoc"
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                target_work = cfg.get("work_dir", target_work)
        except Exception:
            pass
    resolved = os.path.abspath(os.path.expanduser(target_work))
    # QUY TẮC DRIVE: Không được đặt WORK trong Google Drive (chứa CloudStorage)
    if "CloudStorage" in resolved:
        fallback = os.path.abspath(os.path.expanduser("~/Library/Caches/DiemDoc"))
        sys.stderr.write(f"[CẢNH BÁO DRIVE] work_dir '{resolved}' nằm trong CloudStorage! Chuyển hướng an toàn về '{fallback}'.\n")
        resolved = fallback
    os.makedirs(resolved, exist_ok=True)
    return resolved


WORK = _resolve_work_dir()


def work_file(*parts: str) -> str:
    """Trả về đường dẫn tệp nằm trong thư mục tạm WORK ngoài Drive."""
    target = os.path.join(WORK, *parts)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    return target


def work_project_dir(name: str) -> str:
    """
    Trả về đường dẫn thư mục tạm cho project trong WORK ngoài Google Drive.
    Dùng để chứa các tệp nhị phân lớn: wav, mp4 cảnh, ảnh render trung gian.
    """
    p_basename = os.path.basename(os.path.normpath(name))
    target = os.path.join(WORK, p_basename)
    os.makedirs(target, exist_ok=True)
    return target


def work_project_file(name: str, *parts: str) -> str:
    """Trả về đường dẫn tệp nằm trong thư mục WORK/<project>/ ngoài Drive."""
    p_dir = work_project_dir(name)
    target = os.path.join(p_dir, *parts)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    return target


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def get_today_dir_name() -> str:
    """Trả về tên thư mục theo ngày chuẩn DD.MM.YYYY (ví dụ: 16.10.2026)."""
    from datetime import datetime, timezone, timedelta
    ict = timezone(timedelta(hours=7))
    return datetime.now(ict).strftime("%d.%m.%Y")


def project_dir(name: str | None = None) -> str:
    """
    Trả về đường dẫn tuyệt đối tới thư mục ngày trong outputs/DD.MM.YYYY/.
    Chuẩn cấu trúc 1 ngày duy nhất: outputs/DD.MM.YYYY/ (Ví dụ: outputs/16.10.2026/).
    Mọi kết quả chính thức của một ngày (thethao.txt, thethao.json, thethao.mp4) lưu tại đây.
    """
    if not name:
        name = get_today_dir_name()

    if os.path.isabs(name):
        return ensure_dir(name)

    normalized = os.path.normpath(name)
    # Nếu đã có prefix outputs/
    if normalized.startswith("outputs" + os.sep) or normalized == "outputs":
        return ensure_dir(os.path.join(ROOT, normalized))

    # Mặc định: nằm trong ROOT/outputs/DD.MM.YYYY/
    return ensure_dir(os.path.join(OUTPUTS, normalized))


def project_file(name: str, *parts: str) -> str:
    return os.path.join(project_dir(name), *parts)


def rel_to_root(path: str) -> str:
    try:
        return os.path.relpath(os.path.abspath(path), ROOT)
    except ValueError:
        return path


def file_url(path: str) -> str:
    """
    Chuyển đường dẫn local thành file:// URL an toàn cho Playwright/Chromium.
    Tự động percent-encode đường dẫn chứa khoảng trắng và dấu tiếng Việt (Drive của tôi).
    """
    abs_path = os.path.abspath(path)
    url_path = pathname2url(abs_path)
    if not url_path.startswith("/"):
        url_path = "/" + url_path
    return "file://" + url_path