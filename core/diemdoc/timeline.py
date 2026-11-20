"""
Timeline access layer.
======================
Mọi module đọc/ghi timeline đều đi qua đây. Không module nào tự ý
hiểu cấu trúc timeline theo cách riêng (đó là nguồn gốc của "type hell").

Quy ước:
  - Card nằm trong sc["cards"]. Nếu gặp sc["steps"] (timeline cũ), tự migrate.
  - Thời gian do sync ghi vào: card["_reveal_time"], scene["_start_time"], scene["_duration"].
"""

from __future__ import annotations

import os
from typing import Iterator

from .jsonio import load_json, save_json


# --------------------------------------------------------------------------
# Load / save
# --------------------------------------------------------------------------

def timeline_path(project_dir: str) -> str:
    """Trả về đường dẫn file timeline JSON. Ưu tiên thethao.json nếu có."""
    p_thethao = os.path.join(project_dir, "thethao.json")
    if os.path.exists(p_thethao):
        return p_thethao
    p_vt = os.path.join(project_dir, "video_timeline.json")
    if os.path.exists(p_vt):
        return p_vt
    # Mặc định theo chuẩn mới: thethao.json
    return p_thethao


def load_timeline(project_or_path: str) -> dict:
    """
    Nhận vào tên project / thư mục ngày HOẶC đường dẫn trực tiếp tới file .json.
    Tự migrate timeline cũ (steps -> cards) nếu cần.
    """
    path = project_or_path
    if not path.endswith(".json"):
        path = timeline_path(path)
    tl = load_json(path)
    if tl is None:
        raise FileNotFoundError(f"Không tìm thấy timeline: {path}")
    return migrate(tl)


def save_timeline(project_dir: str, tl: dict, path: str | None = None) -> str:
    return save_json(path or timeline_path(project_dir), tl)


def migrate(tl: Any) -> dict:
    """Chuẩn hóa timeline: 'steps' -> 'cards'; bổ sung schema_version."""
    if isinstance(tl, list):
        return {"schema_version": "1.0.0", "scenes": [], "items": tl}
    tl.setdefault("schema_version", "1.0.0")
    for sc in tl.get("scenes", []):
        if "cards" not in sc and "steps" in sc:
            sc["cards"] = sc.pop("steps")
        sc.setdefault("cards", [])
        # chuẩn hóa tên trường derived
        if "start_time" in sc and "_start_time" not in sc:
            sc["_start_time"] = sc["start_time"]
        if "duration" in sc and "_duration" not in sc:
            sc["_duration"] = sc["duration"]
        for c in sc["cards"]:
            if "reveal_time" in c and "_reveal_time" not in c:
                c["_reveal_time"] = c["reveal_time"]
    return tl


# --------------------------------------------------------------------------
# Truy vấn
# --------------------------------------------------------------------------

def scenes_of(tl: dict) -> list[dict]:
    return tl.get("scenes", [])


def cards_of(scene: dict) -> list[dict]:
    return scene.get("cards", scene.get("steps", []))


def iter_cards(tl: dict) -> Iterator[tuple[dict, dict]]:
    """Yield (scene, card) cho toàn timeline."""
    for sc in scenes_of(tl):
        for c in cards_of(sc):
            yield sc, c


def scene_start(scene: dict) -> float:
    return float(scene.get("_start_time", scene.get("start_time", 0.0)) or 0.0)


def scene_duration(scene: dict) -> float:
    d = scene.get("_duration", scene.get("duration"))
    if d is None:
        return 8.0
    return float(d)


def scene_end(scene: dict) -> float:
    return scene_start(scene) + scene_duration(scene)


def total_duration(tl: dict) -> float:
    explicit = float(tl.get("total_duration") or 0)
    scenes = scenes_of(tl)
    if not scenes:
        return explicit
    calc = max(scene_end(s) for s in scenes)
    return max(explicit, calc)


def card_reveal(scene: dict, card: dict) -> float:
    """Thời điểm card xuất hiện (tuyệt đối)."""
    if "_reveal_time" in card:
        return float(card["_reveal_time"])
    if "reveal_time" in card:
        return float(card["reveal_time"])
    return scene_start(scene) + float(card.get("local_delay", 0.3))


def set_card_timing(card: dict, reveal_time: float, local_delay: float | None = None) -> None:
    """Ghi thời gian vào card (cả tên mới và tên cũ để tương thích template)."""
    card["_reveal_time"] = round(float(reveal_time), 3)
    card["reveal_time"] = round(float(reveal_time), 3)
    if local_delay is not None:
        card["local_delay"] = round(float(local_delay), 3)


def set_scene_timing(scene: dict, start: float, duration: float) -> None:
    scene["_start_time"] = round(float(start), 3)
    scene["_duration"] = round(float(duration), 3)
    scene["start_time"] = round(float(start), 3)
    scene["duration"] = round(float(duration), 3)


# --------------------------------------------------------------------------
# Tiện ích cho builder / QA
# --------------------------------------------------------------------------

def find_scene(tl: dict, scene_id: int) -> dict | None:
    for sc in scenes_of(tl):
        if int(sc.get("scene_id", 0)) == int(scene_id):
            return sc
    scenes = scenes_of(tl)
    if 1 <= scene_id <= len(scenes):
        return scenes[scene_id - 1]
    return None


def full_script(tl: dict) -> str:
    return " ".join((sc.get("script_text") or "").strip() for sc in scenes_of(tl)).strip()


def word_count(tl: dict) -> int:
    return len(full_script(tl).split())


def estimated_read_minutes(tl: dict, wpm: float = 150.0) -> float:
    return word_count(tl) / wpm