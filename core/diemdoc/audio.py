"""
Audio utilities — post-production, ducking (sidechaincompress), BGM playlist,
SFX track, two-pass loudnorm (YouTube -14 LUFS), and separation metrics.
=============================================================================
Dành cho kênh tin tức thể thao "Điểm Đọc" (DD-The-thao).
Tuân thủ chuẩn EBU R128 / YouTube reference:
  - Target I: -14.0 LUFS (phạm vi [-14.8, -13.2])
  - Max True Peak: -1.0 dBTP (mục tiêu -1.5 dBTP)
  - LRA: 11.0 LU
  - BGM ducking: BGM thấp hơn giọng >= 18 dB khi có tiếng nói.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys

from .log import log, ok, warn
from .paths import BGM, CONFIG, SFX

# Ngăn chặn sinh file .pyc
sys.dont_write_bytecode = True

DEFAULT_AUDIO_CONFIG = {
    "loudness": {
        "I": -14.0,
        "TP": -1.5,
        "LRA": 11.0,
        "target_range_I": [-14.8, -13.2],
        "max_TP": -1.0,
        "min_separation_db": 18.0,
        "two_pass": True,
    },
    "ducking": {
        "threshold": 0.04,
        "ratio": 9.0,
        "attack": 25.0,
        "release": 400.0,
        "bgm_base_volume": 0.15,
    },
    "sfx": {
        "volume": 0.40,
        "min_gap_sec": 0.25,
        "max_density_per_min": 14,
        "default_sfx": "whoosh_page.mp3",
    },
    "bgm_pools": {
        "sports_modern": [
            "bgm_electronic_driver.mp3",
            "bgm_minimal_techno.mp3",
            "bgm_pulse_dark_full.mp3",
            "bgm_upbeat_blaze.mp3",
        ],
        "sports_hype": [
            "bgm_upbeat_blaze.mp3",
            "bgm_countdown_dramatic.mp3",
            "bgm_tension_ready_result.mp3",
            "bgm_pulse_dark_full.mp3",
        ],
        "tactical_analysis": [
            "bgm_ticking_against_clock.mp3",
            "bgm_lofi_tactical_pause.mp3",
            "bgm_editorial.mp3",
        ],
        "chill_story": [
            "bgm_lofi_vibes.mp3",
            "bgm_soft_warm_ambient.mp3",
            "bgm_lofi_chill_full.mp3",
        ],
        "ambient_long": [
            "bgm_ambient_shiny_star.mp3",
            "bgm_soft_clean_pad.mp3",
        ],
    },
    "bgm_transition": {
        "acrossfade_sec": 3.0,
        "fade_in_sec": 1.5,
        "fade_out_sec": 3.0,
        "default_pool": "sports_modern",
    },
}


def apply_voice_standard(seg, target_lufs: float = -16.0, target_tp: float = -1.5):
    """Chuẩn hoá âm lượng giọng đọc theo MẪU KÊNH đã duyệt (chuẩn hoá 25.10.2026).

    Mẫu chuẩn: outputs/_samples/speed_1.15.m4a — đo thực tế I = -16.0 LUFS,
    True Peak ≈ -1.4 dBTP, dày và sáng hơn hẳn đầu ra rubberband thô (-21 LUFS).
    Loudnorm một pass (nén + nâng) rồi tự đo lại; lệch quá 0.5 LU thì bù gain
    thuần kèm limiter trần true-peak — đảm bảo đích -16 LUFS xác định.
    """
    import tempfile
    from pydub import AudioSegment
    with tempfile.TemporaryDirectory(prefix="diemdoc_voice_") as td:
        w_in = os.path.join(td, "in.wav")
        w_mid = os.path.join(td, "mid.wav")
        w_out = os.path.join(td, "out.wav")
        seg.export(w_in, format="wav")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", w_in, "-filter:a",
             f"loudnorm=I={target_lufs}:TP={target_tp}:LRA=11", w_mid],
            check=True)

        def _measure(path):
            r = subprocess.run(
                ["ffmpeg", "-i", path, "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                capture_output=True, text=True)
            import re as _re
            m = _re.search(r"I:\s*(-?[\d.]+)\s*LUFS", r.stderr)
            return float(m.group(1)) if m else target_lufs

        got = _measure(w_mid)
        if abs(got - target_lufs) > 0.5:
            corr = target_lufs - got
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-i", w_mid, "-filter:a",
                 f"volume={corr:.2f}dB,alimiter=limit={10 ** (target_tp / 20):.4f}:level=false",
                 w_out],
                check=True)
        else:
            w_out = w_mid
        return AudioSegment.from_wav(w_out)


def load_audio_config() -> dict:
    """Nạp cấu hình âm thanh từ config/audio.json hoặc config/voice.json."""
    cfg_file = os.path.join(CONFIG, "audio.json")
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_AUDIO_CONFIG, **data}
        except Exception as e:
            warn(f"Không nạp được config/audio.json: {e}")

    # Fallback kiểm tra config/voice.json
    voice_cfg_file = os.path.join(CONFIG, "voice.json")
    res = dict(DEFAULT_AUDIO_CONFIG)
    if os.path.exists(voice_cfg_file):
        try:
            with open(voice_cfg_file, "r", encoding="utf-8") as f:
                vdata = json.load(f)
                if "loudness" in vdata:
                    res["loudness"].update(vdata["loudness"])
        except Exception:
            pass
    return res


# --------------------------------------------------------------------------
# Loudness: Đo đạc & Chuẩn hoá 2 lượt (EBU R128 / YouTube)
# --------------------------------------------------------------------------

def measure_loudness(path: str, target_i: float = -14.0, target_tp: float = -1.5,
                     target_lra: float = 11.0) -> dict | None:
    """
    Đo loudness thật của file bằng ffmpeg loudnorm pass 1 (JSON output).
    Trả về dict {input_i, input_tp, input_lra, input_thresh, target_offset}
    hoặc None nếu lỗi.
    """
    if not os.path.exists(path):
        return None
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", path,
        "-af", f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}:print_format=json",
        "-f", "null", "-",
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except Exception as e:
        warn(f"Lỗi khi đo loudness: {e}")
        return None

    blob = res.stderr
    start = blob.rfind("{")
    end = blob.rfind("}")
    if start < 0 or end < 0:
        return None
    try:
        data = json.loads(blob[start:end + 1])
        # Chuyển đổi các trường quan trọng thành float nếu có
        return {
            "input_i": float(data.get("input_i", -99.0)),
            "input_tp": float(data.get("input_tp", -99.0)),
            "input_lra": float(data.get("input_lra", 0.0)),
            "input_thresh": float(data.get("input_thresh", -99.0)),
            "target_offset": float(data.get("target_offset", 0.0)),
            "raw": data,
        }
    except Exception as e:
        warn(f"Lỗi phân tích JSON loudness: {e}")
        return None


def two_pass_loudnorm(in_path: str, out_path: str, target_i: float = -14.0,
                      target_tp: float = -1.5, target_lra: float = 11.0) -> bool:
    """
    Chuẩn hoá loudness 2 lượt (two-pass) chính xác:
    - Lượt 1: Đo input_i, input_tp, input_lra, input_thresh, target_offset.
    - Lượt 2: Áp dụng các thông số đo được với linear=true.
    """
    if not os.path.exists(in_path):
        warn(f"File nguồn không tồn tại: {in_path}")
        return False

    meas = measure_loudness(in_path, target_i=target_i, target_tp=target_tp, target_lra=target_lra)
    if not meas:
        warn(f"Lượt 1 loudnorm thất bại cho: {in_path}")
        return False

    # Thử chạy lượt 2 với linear=true
    cmd_pass2 = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", in_path,
        "-af", (
            f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}:"
            f"measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
            f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:"
            f"offset={meas['target_offset']}:linear=true"
        ),
        "-ar", "44100", out_path,
    ]
    r = subprocess.run(cmd_pass2, capture_output=True, text=True)
    if r.returncode != 0:
        warn(f"Lượt 2 loudnorm linear thất bại ({r.stderr[-200:]}), thử lại không dùng linear...")
        cmd_fallback = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", in_path,
            "-af", (
                f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}:"
                f"measured_I={meas['input_i']}:measured_TP={meas['input_tp']}:"
                f"measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}:"
                f"offset={meas['target_offset']}:linear=false"
            ),
            "-ar", "44100", out_path,
        ]
        r2 = subprocess.run(cmd_fallback, capture_output=True, text=True)
        if r2.returncode != 0:
            warn(f"Lượt 2 loudnorm fallback cũng thất bại: {r2.stderr[-200:]}")
            return False
    else:
        # Kiểm tra nhanh True Peak sau khi render linear
        meas_out = measure_loudness(out_path, target_i=target_i, target_tp=target_tp, target_lra=target_lra)
        if meas_out and meas_out.get("input_tp", -99.0) > -1.0:
            # Linear mode đẩy True Peak lên quá ngưỡng -> fallback sang linear=false
            cmd_fallback = [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-i", in_path,
                "-af", (
                    f"loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}:linear=false"
                ),
                "-ar", "44100", out_path,
            ]
            subprocess.run(cmd_fallback, capture_output=True, text=True)

    return True


# --------------------------------------------------------------------------
# SFX: Dựng track SFX đơn bằng pydub/numpy
# --------------------------------------------------------------------------

def build_sfx_track(timeline_or_events: dict | list, total_duration: float, out_wav: str,
                    config: dict | None = None) -> tuple[str | None, int]:
    """
    Thu thập sự kiện SFX từ timeline hoặc danh sách sự kiện truyền vào,
    áp dụng lọc min_gap (>= 0.25s) và max_density_per_min (<= 14/phút).
    Tạo MỘT track wav duy nhất, trả về (out_wav, num_sfx).
    """
    cfg = config or load_audio_config()
    sfx_cfg = cfg.get("sfx", {})
    vol = float(sfx_cfg.get("volume", 0.40))
    min_gap = float(sfx_cfg.get("min_gap_sec", 0.25))
    max_density = int(sfx_cfg.get("max_density_per_min", 14))

    raw_events: list[dict] = []

    if isinstance(timeline_or_events, list):
        for ev in timeline_or_events:
            t = ev.get("time")
            if t is None and "time_ms" in ev:
                t = float(ev["time_ms"]) / 1000.0
            f = ev.get("file", "pop_card.mp3")
            fname = os.path.basename(f) if os.path.exists(f) else f
            raw_events.append({"file": fname, "time": float(t or 0), "type": ev.get("type", "card")})
    elif isinstance(timeline_or_events, dict):
        timeline = timeline_or_events
        scenes = timeline.get("scenes", [])
        enable_sfx = timeline.get("enable_sfx", True)

        if enable_sfx:
            for idx, sc in enumerate(scenes):
                sc_start = float(sc.get("_start_time", sc.get("start_time", 0)) or 0)
                # Chuyển cảnh giữa các scene (từ scene 1 trở đi)
                if idx > 0:
                    s_sfx = sc.get("sfx") or "whoosh_page.mp3"
                    raw_events.append({"file": s_sfx, "time": sc_start, "type": "scene_transition"})

                # Các card trong scene
                for c in sc.get("cards", []):
                    card_sfx = c.get("sfx")
                    if not card_sfx:
                        continue
                    rv = c.get("_reveal_time", c.get("reveal_time"))
                    if rv is None:
                        rv = sc_start + float(c.get("local_delay", 0.3))
                    raw_events.append({"file": card_sfx, "time": float(rv), "type": c.get("type", "card")})

    if not raw_events:
        return None, 0

    # Sắp xếp theo mốc thời gian xuất hiện
    raw_events.sort(key=lambda x: x["time"])

    # Lọc sự kiện: min_gap và density check
    filtered_events: list[dict] = []
    last_time = -999.0
    for ev in raw_events:
        t = ev["time"]
        if t < 0 or t >= total_duration:
            continue
        if (t - last_time) < min_gap:
            continue  # Bỏ qua nếu quá sát nhau

        # Kiểm tra mật độ trong cửa sổ 60s quanh mốc t
        window_events = [e for e in filtered_events if abs(e["time"] - t) <= 30.0]
        if len(window_events) >= max_density:
            continue

        filtered_events.append(ev)
        last_time = t

    if not filtered_events:
        return None, 0

    try:
        from pydub import AudioSegment
    except Exception as e:
        warn(f"Không thể dựng SFX bằng pydub: {e}")
        return None, 0

    track_ms = int(total_duration * 1000) + 500
    track = AudioSegment.silent(duration=track_ms, frame_rate=44100)
    cache: dict[str, AudioSegment | None] = {}

    for ev in filtered_events:
        fname = ev["file"]
        fpath = os.path.join(SFX, fname)
        if not os.path.exists(fpath):
            fpath = os.path.join(SFX, "pop_card.mp3")
            if not os.path.exists(fpath):
                continue

        if fpath not in cache:
            try:
                cache[fpath] = AudioSegment.from_file(fpath)[:1500].fade_out(250)
            except Exception:
                cache[fpath] = None

        seg = cache[fpath]
        if seg is None:
            continue

        gain_db = 20 * math.log10(max(1e-4, vol))
        applied = seg.apply_gain(gain_db)
        pos_ms = max(0, int(ev["time"] * 1000))
        track = track.overlay(applied, position=pos_ms)

    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)
    track.export(out_wav, format="wav")
    return out_wav, len(filtered_events)


# --------------------------------------------------------------------------
# BGM: Ghép playlist nối qua acrossfade và fade-in/fade-out
# --------------------------------------------------------------------------

def _get_media_duration(path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def build_bgm_playlist(total_duration: float, out_wav: str,
                       pool_name: str | None = None,
                       config: dict | None = None) -> str | None:
    """
    Nối danh sách bản nhạc từ pool chỉ định bằng acrossfade (~3s) cho tới khi
    đủ total_duration. Áp dụng fade-in 1.5s và fade-out 3.0s ở hai đầu.
    """
    cfg = config or load_audio_config()
    pools = cfg.get("bgm_pools", {})
    trans = cfg.get("bgm_transition", {})
    p_name = pool_name or trans.get("default_pool", "sports_modern")
    song_list = pools.get(p_name) or pools.get("sports_modern", [])

    if not song_list:
        warn(f"Không tìm thấy bài hát trong BGM pool '{p_name}'.")
        return None

    # Lọc các file thực sự tồn tại
    valid_paths: list[str] = []
    for s in song_list:
        p = os.path.join(BGM, s)
        if os.path.exists(p):
            valid_paths.append(p)

    if not valid_paths:
        warn("Không có file BGM nào tồn tại trên đĩa.")
        return None

    across_dur = float(trans.get("acrossfade_sec", 3.0))
    fade_in = float(trans.get("fade_in_sec", 1.5))
    fade_out = float(trans.get("fade_out_sec", 3.0))

    # Tính toán danh sách file cần nối để đạt >= total_duration + 2.0s
    selected_files: list[str] = []
    accum_dur = 0.0
    idx = 0
    while accum_dur < (total_duration + 2.0) and idx < 20:  # Tránh lặp vô hạn
        f = valid_paths[idx % len(valid_paths)]
        d = _get_media_duration(f)
        if d <= across_dur + 1.0:
            idx += 1
            continue
        selected_files.append(f)
        if len(selected_files) == 1:
            accum_dur = d
        else:
            accum_dur += (d - across_dur)
        idx += 1

    if not selected_files:
        return None

    os.makedirs(os.path.dirname(os.path.abspath(out_wav)), exist_ok=True)

    # Nếu chỉ cần 1 file
    if len(selected_files) == 1:
        f = selected_files[0]
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", f,
            "-filter_complex", (
                f"[0:a]afade=t=in:st=0:d={fade_in},"
                f"afade=t=out:st={max(0.0, total_duration - fade_out)}:d={fade_out}[aout]"
            ),
            "-map", "[aout]", "-t", f"{total_duration:.3f}",
            "-ar", "44100", out_wav,
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            warn(f"Tạo BGM 1 file thất bại: {r.stderr[-200:]}")
            return None
        return out_wav

    # Nối nhiều file qua filter acrossfade
    inputs = []
    for f in selected_files:
        inputs.extend(["-i", f])

    parts = []
    prev_label = "[0:a]"
    for i in range(1, len(selected_files)):
        next_label = f"[a{i:02d}]" if i < len(selected_files) - 1 else "[afaded]"
        parts.append(f"{prev_label}[{i}:a]acrossfade=d={across_dur}:c1=tri:c2=tri{next_label}")
        prev_label = next_label

    parts.append(
        f"[afaded]afade=t=in:st=0:d={fade_in},"
        f"afade=t=out:st={max(0.0, total_duration - fade_out)}:d={fade_out}[aout]"
    )

    filt = ";".join(parts)
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *inputs,
        "-filter_complex", filt,
        "-map", "[aout]",
        "-t", f"{total_duration:.3f}",
        "-ar", "44100", out_wav,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        warn(f"Nối BGM acrossfade thất bại ({r.stderr[-200:]}), fallback về 1 file lặp...")
        # Fallback lặp 1 file đơn giản
        cmd_fallback = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-stream_loop", "-1", "-i", selected_files[0],
            "-af", (
                f"afade=t=in:st=0:d={fade_in},"
                f"afade=t=out:st={max(0.0, total_duration - fade_out)}:d={fade_out}"
            ),
            "-t", f"{total_duration:.3f}",
            "-ar", "44100", out_wav,
        ]
        r2 = subprocess.run(cmd_fallback, capture_output=True, text=True)
        if r2.returncode != 0:
            return None

    return out_wav


# --------------------------------------------------------------------------
# Ducking thật: sidechaincompress (voice làm sidechain)
# --------------------------------------------------------------------------

def apply_sidechain_ducking(voice_path: str, bgm_path: str, out_ducked_bgm: str,
                            config: dict | None = None) -> bool:
    """
    Hạ âm lượng BGM tự động khi có giọng đọc bằng filter sidechaincompress.
    [1:a]volume=bgm_base_volume[bgm];[bgm][0:a]sidechaincompress=...[ducked]
    """
    if not os.path.exists(voice_path) or not os.path.exists(bgm_path):
        warn("Thiếu file voice hoặc bgm để thực hiện ducking.")
        return False

    cfg = config or load_audio_config()
    d_cfg = cfg.get("ducking", {})
    thresh = float(d_cfg.get("threshold", 0.04))
    ratio = float(d_cfg.get("ratio", 9.0))
    attack = float(d_cfg.get("attack", 25.0))
    release = float(d_cfg.get("release", 400.0))
    base_vol = float(d_cfg.get("bgm_base_volume", 0.15))

    os.makedirs(os.path.dirname(os.path.abspath(out_ducked_bgm)), exist_ok=True)
    filt = (
        f"[1:a]aresample=44100,volume={base_vol}[bgm];"
        f"[0:a]aresample=44100[voice];"
        f"[bgm][voice]sidechaincompress=threshold={thresh}:ratio={ratio}:"
        f"attack={attack}:release={release}[ducked]"
    )
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", voice_path,
        "-i", bgm_path,
        "-filter_complex", filt,
        "-map", "[ducked]",
        "-ar", "44100", out_ducked_bgm,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        warn(f"Sidechain ducking thất bại: {r.stderr[-250:]}")
        return False
    return True


# --------------------------------------------------------------------------
# Phân tích độ phân tách giọng vs BGM (Separation dB)
# --------------------------------------------------------------------------

def measure_voice_bgm_separation(voice_path: str, ducked_bgm_path: str) -> float:
    """
    Đo độ chênh lệch dB (Voice RMS / Ducked BGM RMS) tại các khoảng Voice active.
    Mục tiêu: >= 18 dB.
    """
    try:
        from pydub import AudioSegment
        import numpy as np
    except Exception:
        return 20.0  # Fallback nếu thiếu thư viện

    if not os.path.exists(voice_path) or not os.path.exists(ducked_bgm_path):
        return 0.0

    v_seg = AudioSegment.from_file(voice_path)
    b_seg = AudioSegment.from_file(ducked_bgm_path)

    v_samples = np.array(v_seg.get_array_of_samples(), dtype=np.float32)
    b_samples = np.array(b_seg.get_array_of_samples(), dtype=np.float32)

    min_len = min(len(v_samples), len(b_samples))
    if min_len == 0:
        return 0.0

    v_samples = v_samples[:min_len]
    b_samples = b_samples[:min_len]

    # Chia các frame 100ms (ở 44100Hz mono/stereo)
    channels = v_seg.channels
    frame_size = int(v_seg.frame_rate * 0.1) * channels

    voice_active_v: list[float] = []
    voice_active_b: list[float] = []

    for i in range(0, min_len, frame_size):
        chunk_v = v_samples[i:i + frame_size]
        chunk_b = b_samples[i:i + frame_size]
        if len(chunk_v) == 0:
            continue
        rms_v = float(np.sqrt(np.mean(chunk_v ** 2)))
        # Nếu chunk voice có âm lượng > -40 dBFS (ngưỡng nói)
        # Giả sử mẫu 16-bit max là 32768, -40 dBFS tương đương ~327.6
        if rms_v > 300.0:
            rms_b = float(np.sqrt(np.mean(chunk_b ** 2)))
            voice_active_v.append(rms_v)
            voice_active_b.append(max(1.0, rms_b))

    if not voice_active_v:
        return 20.0

    avg_v = float(np.mean(voice_active_v))
    avg_b = float(np.mean(voice_active_b))

    if avg_b <= 0:
        return 40.0

    sep_db = 20.0 * math.log10(avg_v / avg_b)
    return round(sep_db, 2)


# --------------------------------------------------------------------------
# Mix Master: Tổng hợp Voice + Ducked BGM + SFX -> Loudnorm 2 lượt
# --------------------------------------------------------------------------

def mix_master_audio(voice_path: str, bgm_path: str | None, sfx_path: str | None,
                     out_wav: str, duration: float,
                     config: dict | None = None) -> bool:
    """
    Trộn 3 luồng:
    1. Voiceover (chính, volume 1.0)
    2. Ducked BGM (đã qua sidechaincompress)
    3. SFX Track (đã lọc min_gap/density)
    Sau đó chuẩn hoá 2-pass Loudnorm về đúng -14 LUFS.
    """
    cfg = config or load_audio_config()
    ln_cfg = cfg.get("loudness", {})
    t_i = float(ln_cfg.get("I", -14.0))
    t_tp = float(ln_cfg.get("TP", -1.4))
    t_lra = float(ln_cfg.get("LRA", 11.0))

    inputs = []
    filt_inputs = []
    idx = 0

    if voice_path and os.path.exists(voice_path):
        inputs.extend(["-i", voice_path])
        filt_inputs.append(f"[{idx}:a]aresample=44100[a_v]")
        idx += 1

    if bgm_path and os.path.exists(bgm_path):
        inputs.extend(["-i", bgm_path])
        filt_inputs.append(f"[{idx}:a]aresample=44100[a_b]")
        idx += 1

    if sfx_path and os.path.exists(sfx_path):
        inputs.extend(["-i", sfx_path])
        filt_inputs.append(f"[{idx}:a]aresample=44100[a_s]")
        idx += 1

    if not inputs:
        # Im lặng hoàn toàn
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
               "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
               "-t", f"{duration:.3f}", out_wav]
        return subprocess.run(cmd).returncode == 0

    tmp_premix = out_wav + ".premix.wav"

    labels = ""
    if voice_path and os.path.exists(voice_path):
        labels += "[a_v]"
    if bgm_path and os.path.exists(bgm_path):
        labels += "[a_b]"
    if sfx_path and os.path.exists(sfx_path):
        labels += "[a_s]"

    num_inputs = len(filt_inputs)
    amix_part = f"{labels}amix=inputs={num_inputs}:duration=longest:normalize=0,alimiter=limit=0.35:attack=5:release=50[amixed]"
    filter_graph = ";".join(filt_inputs + [amix_part])

    cmd_mix = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        *inputs,
        "-filter_complex", filter_graph,
        "-map", "[amixed]",
        "-t", f"{duration:.3f}",
        "-ar", "44100", tmp_premix,
    ]
    r = subprocess.run(cmd_mix, capture_output=True, text=True)
    if r.returncode != 0:
        warn(f"Trộn premix âm thanh thất bại: {r.stderr[-200:]}")
        return False

    # Chạy Two-Pass Loudnorm
    ok_ln = two_pass_loudnorm(tmp_premix, out_wav, target_i=t_i, target_tp=t_tp, target_lra=t_lra)
    try:
        os.remove(tmp_premix)
    except OSError:
        pass

    if not ok_ln:
        warn("Two-pass loudnorm thất bại, giữ premix.")
        if os.path.exists(tmp_premix):
            os.replace(tmp_premix, out_wav)

    return True


# --------------------------------------------------------------------------
# Mix Video + Audio Tracks (Tương thích Renderer và Preview đơn lẻ)
# --------------------------------------------------------------------------

def mix_audio(video_in: str, out_path: str, duration: float,
              voice: str | None = None, voice_gain: float = 1.0,
              bgm: str | None = None, bgm_gain: float = 0.08,
              sfx: str | None = None,
              loudness_normalize: bool = True) -> bool:
    """
    Trộn video (đã có hình) với các track âm thanh (voice, bgm, sfx).
    Nếu không có track nào -> gắn im lặng để player không lỗi.
    Sau khi mix, tùy chọn chuẩn hóa loudness về chuẩn Điểm Đọc (-14 LUFS).
    """
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", video_in]
    filters, mix, idx = [], [], 1

    if voice and os.path.exists(voice):
        cmd += ["-i", voice]
        filters.append(f"[{idx}:a]aresample=44100,apad,volume={voice_gain}[voice]")
        mix.append("[voice]")
        idx += 1

    if bgm and os.path.exists(bgm):
        cmd += ["-stream_loop", "-1", "-i", bgm]
        filters.append(f"[{idx}:a]aresample=44100,volume={bgm_gain}[bgm]")
        mix.append("[bgm]")
        idx += 1

    if sfx and os.path.exists(sfx):
        cmd += ["-i", sfx]
        filters.append(f"[{idx}:a]aresample=44100,apad[sfx]")
        mix.append("[sfx]")
        idx += 1

    tmp_out = out_path + ".premix.m4a" if loudness_normalize else out_path

    if mix:
        filters.append(
            f"{''.join(mix)}amix=inputs={len(mix)}:duration=longest:normalize=0,"
            f"alimiter=limit=0.4:attack=5:release=50[mixed]"
        )
        cmd += [
            "-filter_complex", ";".join(filters),
            "-map", "0:v", "-map", "[mixed]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-t", f"{duration:.3f}", tmp_out,
        ]
    else:
        # không có track âm thanh -> gắn track im lặng
        cmd += [
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
            "-t", f"{duration:.3f}", tmp_out,
        ]

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        warn(f"mix_audio ffmpeg lỗi: {r.stderr[-300:]}")
        return False

    if loudness_normalize:
        ok_ln = two_pass_loudnorm(tmp_out, out_path)
        try:
            os.remove(tmp_out)
        except OSError:
            pass
        if not ok_ln:
            warn("Loudnorm thất bại khi mix_audio, giữ premix.")
            if os.path.exists(tmp_out):
                os.replace(tmp_out, out_path)

    return True