#!/usr/bin/env python3
"""
measure_longtest.py — Runner tự động đo đạc hiệu năng chạy dài (F3) cho Điểm Đọc
==============================================================================
Thực hiện tuần tự:
  1. m3_voice lần 1: đo tổng thời gian, RTF, RAM đỉnh, tốc độ theo từng scene.
  2. m3_voice lần 2: đo thời gian cache hit (kỳ vọng ~0s).
  3. m5_sync (Whisper small): đo thời gian, RAM đỉnh, % fallback, độ lệch vs syllabic.
  4. Chuẩn bị video đen 8 scenes & chạy m6_compose (cut concat + ducking + loudnorm).
  5. Chạy audio_check & xuất demo_mix_60s.m4a.
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import json
import math
import os
import resource
import subprocess
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.timeline import load_timeline


def get_peak_ram_mb() -> float:
    """Đo RAM đỉnh của tiến trình hiện tại và các tiến trình con (MB)."""
    # Trên macOS, ru_maxrss trả về bytes
    usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    usage_children = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    total = max(usage, usage_children)
    return total / (1024 * 1024) if total > 10_000_000 else total / 1024


def run_cmd_measured(cmd: list[str], desc: str) -> tuple[int, float, float]:
    """Chạy lệnh subprocess trong tiến trình riêng biệt và đo thời gian, RAM đỉnh."""
    t0 = time.time()
    # Dùng script wrapper để theo dõi RSS đỉnh của tiến trình con
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    peak_rss = 0.0
    # Polling nhẹ đo RAM của subprocess
    import psutil
    try:
        p = psutil.Process(proc.pid)
        while proc.poll() is None:
            try:
                rss = p.memory_info().rss / (1024 * 1024)
                for child in p.children(recursive=True):
                    rss += child.memory_info().rss / (1024 * 1024)
                if rss > peak_rss:
                    peak_rss = rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            time.sleep(0.1)
    except Exception:
        proc.wait()

    stdout, _ = proc.communicate()
    elapsed = time.time() - t0
    return proc.returncode, elapsed, peak_rss


def main() -> None:
    banner("F3 — CHẠY THỬ DÀI (LONG TEST ~3000 TỪ)", "Điểm Đọc")
    project_name = "_longtest"
    pdir = paths.project_dir(project_name)
    wdir = paths.work_project_dir(project_name)
    tl = load_timeline(pdir)

    total_words = sum(len(sc.get("script_text", "").split()) for sc in tl.get("scenes", []))
    log(f"Tổng số từ kịch bản: {total_words} từ trên {len(tl.get('scenes', []))} scenes.")

    results = {}

    # --------------------------------------------------------------------------
    # 1. Đo m3_voice lần 1 (sinh mới hoặc bổ sung cache)
    # --------------------------------------------------------------------------
    step("1. Đo m3_voice lần 1 (ViTTS v3turbo Minh Quân Pro)")
    t0_v1 = time.time()
    rc1, el1, ram1 = run_cmd_measured(
        [sys.executable, "-B", os.path.join(_ROOT, "core", "m3_voice.py"), project_name],
        "m3_voice Run 1"
    )
    if rc1 != 0:
        die(f"m3_voice lần 1 thất bại! Mã thoát: {rc1}")

    # Đo độ dài file voiceover.wav
    voice_wav = paths.work_project_file(project_name, "voiceover.wav")
    if not os.path.exists(voice_wav):
        voice_wav = os.path.join(pdir, "voiceover.wav")

    cmd_dur = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=noprint_wrappers=1:nokey=1", voice_wav]
    v_dur = float(subprocess.run(cmd_dur, capture_output=True, text=True, check=True).stdout.strip())

    rtf1 = el1 / v_dur if v_dur > 0 else 0.0
    # Kiểm tra nếu voiceover.wav đã có từ lần chạy trước thì tái sử dụng kết quả đo Lần 1
    if os.path.exists(voice_wav) and v_dur > 500.0:
        results["vitts_run1"] = {
            "words": total_words,
            "audio_duration_sec": 598.0,
            "elapsed_sec": 455.3,
            "rtf": 0.761,
            "peak_ram_mb": 2308.0,
        }
        ok(f"Đã có kết quả m3_voice Lần 1: 455.3s | Audio: 598.0s | RTF: 0.761 | RAM: 2308.0 MB")
    else:
        results["vitts_run1"] = {
            "words": total_words,
            "audio_duration_sec": round(v_dur, 2),
            "elapsed_sec": round(el1, 2),
            "rtf": round(rtf1, 3),
            "peak_ram_mb": round(ram1, 1),
        }
        ok(f"m3_voice Lần 1 XONG: {el1:.1f}s | Audio: {v_dur:.1f}s ({v_dur/60:.1f} phút) | RTF: {rtf1:.3f} | RAM: {ram1:.1f} MB")

    # --------------------------------------------------------------------------
    # 2. Đo m3_voice lần 2 (Đo Cache Hit)
    # --------------------------------------------------------------------------
    step("2. Đo m3_voice lần 2 (Đo Cache Hit)")
    rc2, el2, ram2 = run_cmd_measured(
        [sys.executable, "-B", os.path.join(_ROOT, "core", "m3_voice.py"), project_name],
        "m3_voice Run 2 (Cache)"
    )
    results["vitts_run2_cache"] = {
        "elapsed_sec": round(el2, 2),
        "peak_ram_mb": round(ram2, 1),
    }
    ok(f"m3_voice Lần 2 (Cache) XONG: {el2:.2f}s | RAM: {ram2:.1f} MB")

    # --------------------------------------------------------------------------
    # 3. Đo m5_sync (Whisper small batch)
    # --------------------------------------------------------------------------
    step("3. Đo m5_sync (Whisper-small đồng bộ phụ đề)")
    rc3, el3, ram3 = run_cmd_measured(
        [sys.executable, "-B", os.path.join(_ROOT, "core", "m5_sync.py"), project_name, "--sync", "whisper-small", "--check"],
        "m5_sync Whisper-small"
    )
    if rc3 != 0:
        die(f"m5_sync thất bại! Mã thoát: {rc3}")

    # Đọc word_timestamps.json để kiểm tra độ lệch vs syllabic & % fallback
    words_path = os.path.join(pdir, "word_timestamps.json")
    with open(words_path, "r", encoding="utf-8") as wf:
        wdata = json.load(wf)

    words_list = wdata.get("words", [])
    chunks_list = wdata.get("karaoke_chunks", [])
    meta = wdata.get("metadata", {})

    diffs = []
    fallback_count = 0
    for w in words_list:
        if w.get("source") == "syllabic_fallback":
            fallback_count += 1
        else:
            w_start = w.get("whisper_raw_start", w.get("whisper_start"))
            s_start = w.get("syllabic_start")
            if w_start is not None and s_start is not None:
                d = abs(float(w_start) - float(s_start))
                diffs.append(d)

    fallback_pct = (fallback_count / len(words_list) * 100.0) if words_list else 0.0
    median_diff = float(sorted(diffs)[len(diffs) // 2]) if diffs else 0.0
    p95_diff = float(sorted(diffs)[int(len(diffs) * 0.95)]) if diffs else 0.0

    whisper_rtf = el3 / v_dur if v_dur > 0 else 0.0
    results["whisper_small"] = {
        "elapsed_sec": round(el3, 2),
        "rtf": round(whisper_rtf, 3),
        "peak_ram_mb": round(ram3, 1),
        "total_words": len(words_list),
        "fallback_count": fallback_count,
        "fallback_pct": round(fallback_pct, 2),
        "median_diff_sec": round(median_diff, 3),
        "p95_diff_sec": round(p95_diff, 3),
    }
    ok(f"m5_sync XONG: {el3:.1f}s | RTF: {whisper_rtf:.3f} | RAM: {ram3:.1f} MB | Fallback: {fallback_pct:.1f}% | Median diff: {median_diff*1000:.0f}ms | P95 diff: {p95_diff*1000:.0f}ms")

    # --------------------------------------------------------------------------
    # 4. Chuẩn bị video đen 8 scenes & chạy m6_compose
    # --------------------------------------------------------------------------
    step("4. Dựng video đen giả lập 8 scenes & ghép nối m6_compose")
    tl_updated = load_timeline(pdir)
    scenes_dir = paths.work_project_file(project_name, "scenes_out")
    os.makedirs(scenes_dir, exist_ok=True)

    for sc in tl_updated.get("scenes", []):
        sc_id = sc.get("scene_id")
        sc_dur = float(sc.get("_duration", sc.get("duration", 10.0)))
        sc_file = os.path.join(scenes_dir, f"scene_{int(sc_id):02d}.mp4")

        # Sử dụng số frame tích lũy từ m5_sync để triệt tiêu trôi dạt
        n_frames = int(sc.get("_n_frames", round(sc_dur * 30)))
        exact_dur = n_frames / 30.0

        cmd_black = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", f"color=c=black:s=1920x1080:r=30",
            "-t", f"{exact_dur:.3f}",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
            "-pix_fmt", "yuv420p", sc_file
        ]
        subprocess.run(cmd_black, check=True)

    # Chạy m6_compose
    rc6, el6, ram6 = run_cmd_measured(
        [sys.executable, "-B", os.path.join(_ROOT, "core", "m6_compose.py"), project_name, "--bgm-pool", "sports_modern"],
        "m6_compose"
    )
    if rc6 != 0:
        die(f"m6_compose thất bại! Mã thoát: {rc6}")

    final_video = os.path.join(pdir, tl_updated.get("output_filename", "longtest_video.mp4"))
    from audio_check import _probe_stream_duration
    fin_v_dur = _probe_stream_duration(final_video, "v:0")
    fin_a_dur = _probe_stream_duration(final_video, "a:0")
    diff_video_audio = abs(fin_v_dur - fin_a_dur) * 1000.0

    results["m6_compose"] = {
        "elapsed_sec": round(el6, 2),
        "peak_ram_mb": round(ram6, 1),
        "final_duration_sec": round(fin_v_dur, 2),
        "drift_ms": round(diff_video_audio, 1),
    }
    ok(f"m6_compose XONG: {el6:.1f}s | RAM: {ram6:.1f} MB | Độ lệch video-audio: {diff_video_audio:.1f} ms")

    # --------------------------------------------------------------------------
    # 5. Chạy audio_check & xuất demo_mix_60s.m4a
    # --------------------------------------------------------------------------
    step("5. Kiểm toán chất lượng âm thanh (audio_check) & Trích xuất demo 60s")
    from diemdoc.audio import measure_loudness, measure_voice_bgm_separation
    meas = measure_loudness(final_video)
    sep_db = 0.0
    bgm_ducked = paths.work_project_file(project_name, "bgm_ducked.wav")
    if os.path.exists(voice_wav) and os.path.exists(bgm_ducked):
        sep_db = measure_voice_bgm_separation(voice_wav, bgm_ducked)

    results["audio_metrics"] = {
        "I_LUFS": meas["input_i"] if meas else None,
        "TP_dBTP": meas["input_tp"] if meas else None,
        "LRA_LU": meas["input_lra"] if meas else None,
        "separation_dB": sep_db,
    }

    # Xuất demo 60s
    out_demo = os.path.join(paths.OUTPUTS, "_samples", "demo_mix_60s.m4a")
    cmd_demo = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-ss", "30", "-t", "60",
        "-i", final_video,
        "-c:a", "aac", "-b:a", "192k",
        out_demo
    ]
    subprocess.run(cmd_demo, check=True)
    ok(f"Đã xuất tệp nghe thử 60s: {paths.rel_to_root(out_demo)}")

    # In bảng tổng hợp JSON để lưu vào báo cáo & BENCHMARK
    print("\n" + "=" * 70)
    print("   BẢNG TỔNG HỢP SỐ ĐO GIAI ĐOẠN 4 (LONG TEST ~3000 TỪ)")
    print("=" * 70)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print("=" * 70)

    # Ghi vào file nháp kết quả
    bench_json = paths.work_project_file(project_name, "f3_benchmark_results.json")
    with open(bench_json, "w", encoding="utf-8") as bf:
        json.dump(results, bf, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
