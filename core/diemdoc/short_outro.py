# -*- coding: utf-8 -*-
"""
Tiện ích chọn ngẫu nhiên & ghép nối Outro 9:16 cho video Short (Điểm Đọc).
===========================================================================
Quy tắc chọn Outro mặc định (`opposite_gender_random`):
- Video giọng Nam (`primary`, `male`, `nam`, `Minh Quân Pro`) -> Chọn ngẫu nhiên Outro giọng Nữ
  (`Outro_Short_1_Cyber_Pulse.mp4` hoặc `Outro_Short_3_Kinetic_Slam.mp4`).
- Video giọng Nữ (`secondary`, `female`, `nu`, `Ngọc Huyền`) -> Chọn ngẫu nhiên Outro giọng Nam
  (`Outro_Short_2_Tactical_Broadcast.mp4`).
- Video giọng hỗn hợp / không rõ giới tính -> Chọn ngẫu nhiên trong toàn bộ 3 mẫu.
"""

from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
import random
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from . import paths
from .log import log, ok, warn

DEFAULT_OUTRO_CATALOG: List[Dict[str, Any]] = [
    {
        "id": 1,
        "file": "Outro_Short_1_Cyber_Pulse.mp4",
        "voice_gender": "female",
        "voice_preset": "secondary",
        "style": "cyber_pulse",
    },
    {
        "id": 2,
        "file": "Outro_Short_2_Tactical_Broadcast.mp4",
        "voice_gender": "male",
        "voice_preset": "primary",
        "style": "tactical_broadcast",
    },
    {
        "id": 3,
        "file": "Outro_Short_3_Kinetic_Slam.mp4",
        "voice_gender": "female",
        "voice_preset": "secondary",
        "style": "kinetic_slam",
    },
]


def load_short_outro_config() -> Dict[str, Any]:
    """Đọc cấu hình outro từ `config/shorts.json`."""
    cfg_path = Path(paths.CONFIG) / "shorts.json"
    default_cfg: Dict[str, Any] = {
        "enabled": True,
        "mode": "opposite_gender_random",
        "dir": "logo/short_outros",
        "catalog": list(DEFAULT_OUTRO_CATALOG),
    }
    if not cfg_path.exists():
        return default_cfg
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        outro_cfg = data.get("outro", {})
        if not isinstance(outro_cfg, dict):
            return default_cfg
        return {**default_cfg, **outro_cfg}
    except Exception as e:
        warn(f"Không đọc được config/shorts.json[outro] ({e}), dùng mặc định.")
        return default_cfg


def normalize_voice_gender(voice_hint: Optional[str]) -> Optional[str]:
    """Chuẩn hóa định danh giọng đọc về `'male'`, `'female'`, hoặc `None` (hỗn hợp/không rõ)."""
    if not voice_hint:
        return None
    val = str(voice_hint).strip().lower()
    if any(k in val for k in ("mixed", "dual", "both", "song song", "auto")):
        return None
    if val in ("primary", "male", "nam", "15", "male_15", "minh_quan", "minh quân", "minh quân pro") or "minh" in val or "male" in val:
        return "male"
    if val in ("secondary", "female", "nu", "nữ", "14", "female_14", "ngoc_huyen", "ngọc huyền") or "huyền" in val or "huyen" in val or "female" in val:
        return "female"
    return None


def pick_short_outro(
    voice_hint: Optional[str] = None,
    seed: Optional[str | int] = None,
) -> Optional[Dict[str, Any]]:
    """
    Chọn ngẫu nhiên 1 mẫu Short Outro phù hợp trong `logo/short_outros/`.
    Nếu `voice_hint` là giọng Nam -> chọn ngẫu nhiên Outro giọng Nữ (và ngược lại).
    Trả về dict `{id, file, path, voice_gender, style}` hoặc `None` nếu chưa có file.
    """
    cfg = load_short_outro_config()
    outro_dir = Path(paths.ROOT) / cfg.get("dir", "logo/short_outros")
    catalog = cfg.get("catalog") or DEFAULT_OUTRO_CATALOG

    available: List[Dict[str, Any]] = []
    for entry in catalog:
        fpath = outro_dir / str(entry.get("file", ""))
        if fpath.is_file() and fpath.stat().st_size > 10_000:
            item = dict(entry)
            item["path"] = fpath
            available.append(item)

    if not available:
        warn(f"Không tìm thấy mẫu Short Outro nào trong {outro_dir}")
        return None

    mode = str(cfg.get("mode", "opposite_gender_random")).lower()
    src_gender = normalize_voice_gender(voice_hint)

    candidates = available
    if mode == "opposite_gender_random" and src_gender in ("male", "female"):
        target_gender = "female" if src_gender == "male" else "male"
        opposite = [e for e in available if str(e.get("voice_gender", "")).lower() == target_gender]
        if opposite:
            candidates = opposite

    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    return rng.choice(candidates)


def _probe_durations(mp4_path: Path) -> Tuple[float, float]:
    """Đo thời lượng video stream và audio stream bằng ffprobe."""
    r = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=codec_type,duration",
            "-of", "json", str(mp4_path),
        ],
        capture_output=True, text=True, check=True,
    )
    streams = json.loads(r.stdout).get("streams", [])
    v_dur = next((float(s["duration"]) for s in streams if s.get("codec_type") == "video" and s.get("duration")), 0.0)
    a_dur = next((float(s["duration"]) for s in streams if s.get("codec_type") == "audio" and s.get("duration")), 0.0)
    return v_dur, a_dur


def append_short_outro(
    video_path: Path | str,
    voice_hint: Optional[str] = None,
    out_path: Optional[Path | str] = None,
    seed: Optional[str | int] = None,
    enabled: Optional[bool] = None,
) -> Tuple[Path, Optional[Path]]:
    """
    Ghép nối mượt mà 1 Short Outro 9:16 vào cuối `video_path` (giữ chuẩn 1080x1920 @ 30fps,
    yuv420p, stereo 44.1kHz, drift <= 1 frame).
    Trả về `(final_path, chosen_outro_path)`.
    """
    src_path = Path(video_path)
    dst_path = Path(out_path) if out_path else src_path

    if not src_path.exists():
        raise FileNotFoundError(f"Không tìm thấy video Short nguồn: {src_path}")

    cfg = load_short_outro_config()
    is_enabled = bool(cfg.get("enabled", True)) if enabled is None else bool(enabled)
    if not is_enabled:
        if dst_path != src_path:
            shutil.copy2(str(src_path), str(dst_path))
        return dst_path, None

    chosen = pick_short_outro(voice_hint=voice_hint, seed=seed)
    if not chosen:
        if dst_path != src_path:
            shutil.copy2(str(src_path), str(dst_path))
        return dst_path, None

    outro_path = Path(chosen["path"])
    src_gender = normalize_voice_gender(voice_hint) or "auto"
    log(
        f"Gắn Outro Short (voice={src_gender} -> outro={chosen.get('voice_gender')}): {outro_path.name}",
        tag="outro",
    )

    tmp_dir = Path(paths.WORK) / "short_outro_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    uid = uuid.uuid4().hex[:8]
    tmp_merged = tmp_dir / f"merged_{uid}.mp4"
    tmp_sync = tmp_dir / f"synced_{uid}.mp4"

    try:
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v0];"
            "[1:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
            "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v1];"
            "[0:a]aresample=44100,aformat=channel_layouts=stereo[a0];"
            "[1:a]aresample=44100,aformat=channel_layouts=stereo[a1];"
            "[v0][a0][v1][a1]concat=n=2:v=1:a=1[vout][aout]"
        )
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", str(src_path),
                "-i", str(outro_path),
                "-filter_complex", filter_complex,
                "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                "-movflags", "+faststart",
                str(tmp_merged),
            ],
            check=True,
        )

        v_dur, a_dur = _probe_durations(tmp_merged)
        final_tmp = tmp_merged
        if v_dur > 0 and abs(v_dur - a_dur) > 0.025:
            subprocess.run(
                [
                    "ffmpeg", "-y", "-loglevel", "error",
                    "-i", str(tmp_merged),
                    "-t", f"{v_dur:.6f}",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                    "-movflags", "+faststart",
                    str(tmp_sync),
                ],
                check=True,
            )
            final_tmp = tmp_sync

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(final_tmp), str(dst_path))
        ok(f"Đã ghép Outro {outro_path.name} -> {dst_path.name} ({v_dur:.2f}s)")
        return dst_path, outro_path
    finally:
        for p in (tmp_merged, tmp_sync):
            if p.exists():
                try:
                    p.unlink()
                except OSError:
                    pass
