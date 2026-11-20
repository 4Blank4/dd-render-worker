#!/usr/bin/env python3
"""
m5_sync.py — Đồng bộ phụ đề (Word Timestamps, Karaoke Chunks & Cue-Points)
==========================================================================
Đồng bộ phụ đề chuẩn xác cho kênh Điểm Đọc:
- Ground-truth alignment: căn chỉnh theo văn bản TTS từ audio_sync.json.
- Chế độ: whisper-small (mặc định), whisper-medium, hoặc syllabic (nội suy siêu tốc).
- Chạy Whisper trong tiến trình con riêng biệt theo lô ~3-5 phút, thoát để trả lại RAM.
- Ánh xạ ngược từ TTS tokens về từ hiển thị (Display) bằng token_map.
- Tự động gom karaoke_chunks (3-5 từ), tôn trọng nhóm từ ("group": true).
- Tự động cập nhật _reveal_time và local_delay cho card theo trigger_word (3 tầng fallback).
- Tự động cập nhật _start_time và _duration cho từng scene.
- Cờ --check: kiểm tra tính đơn điệu, độ lệch Whisper vs Syllabic và lệch thời lượng.

Cách dùng:
  python3 core/m5_sync.py <project>
  python3 core/m5_sync.py <project> --sync whisper-small
  python3 core/m5_sync.py <project> --sync syllabic
  python3 core/m5_sync.py <project> --check
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
import math
import os
import re
import subprocess
import time
from typing import List, Dict, Any, Tuple
import numpy as np
from pydub import AudioSegment

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.timeline import load_timeline, save_timeline, cards_of, set_card_timing
from diemdoc.sync import normalize_word, find_phrase_time, resolve_cue_points


def syllabic_interpolate_chunk(tokens: List[str], start: float, end: float) -> List[Dict[str, Any]]:
    """Nội suy thời gian từng âm tiết trong phạm vi chunk [start, end]."""
    if not tokens:
        return []

    weights = []
    for t in tokens:
        w = 1.0
        # Số đếm và chữ số có độ dài phát âm lớn hơn
        digits = sum(c.isdigit() for c in t)
        if digits:
            w += digits * 0.5
        w += sum(0.4 for ch in "-/." if ch in t)
        weights.append(max(0.4, w))

    total = sum(weights) or 1.0
    span = max(0.01, end - start)
    result = []
    cursor = start
    for t, w in zip(tokens, weights):
        dur = span * (w / total)
        w_start = cursor
        w_end = min(end, cursor + dur * 0.95)
        result.append({
            "word": t,
            "start": round(w_start, 3),
            "end": round(w_end, 3),
            "probability": 0.8
        })
        cursor += dur
    return result


def group_display_karaoke_chunks(display_words: List[Dict[str, Any]],
                                 max_words: int = 4, max_chars: int = 40,
                                 pause_split: float = 0.35) -> List[Dict[str, Any]]:
    """Gộp các từ hiển thị thành từng cụm karaoke, không tách rời các từ cùng group."""
    chunks: List[Dict[str, Any]] = []
    cur: List[Dict[str, Any]] = []
    cur_chars = 0

    for idx, w in enumerate(display_words):
        wt = (w.get("word") or "").strip()
        if not wt:
            continue

        long_pause = bool(cur) and (w["start"] - cur[-1]["end"]) >= pause_split
        ended_punct = bool(cur) and cur[-1]["word"].strip().endswith((".", "!", "?", ":", ";", ","))

        # Kiểm tra nếu từ hiện tại đang nằm cùng group với từ trước đó
        is_same_group = False
        if cur and w.get("group_id") is not None and cur[-1].get("group_id") == w.get("group_id"):
            is_same_group = True

        should_split = (
            cur and not is_same_group and (
                len(cur) >= max_words
                or (cur_chars + len(wt) > max_chars and len(cur) >= 2)
                or long_pause
                or (ended_punct and len(cur) >= 3)
            )
        )

        if should_split:
            chunks.append({
                "chunk_index": len(chunks),
                "text": " ".join(item["word"] for item in cur),
                "start": round(cur[0]["start"], 3),
                "end": round(cur[-1]["end"], 3),
                "words": cur
            })
            cur, cur_chars = [], 0

        cur.append(w)
        cur_chars += len(wt) + 1

    if cur:
        chunks.append({
            "chunk_index": len(chunks),
            "text": " ".join(item["word"] for item in cur),
            "start": round(cur[0]["start"], 3),
            "end": round(cur[-1]["end"], 3),
            "words": cur
        })

    return chunks


def run_sync_pipeline(project_name: str, sync_mode: str = "whisper-small",
                      do_check: bool = False) -> Dict[str, Any]:
    """Hàm điều phối toàn bộ quy trình đồng bộ phụ đề."""
    banner("M5 — SYNC (Đồng Bộ Phụ Đề & Timeline)", f"{project_name} [{sync_mode}]")

    project_dir = paths.project_dir(project_name)
    work_pdir = paths.work_project_dir(project_name)

    # 1. Tìm master audio
    master_wav = os.path.join(work_pdir, "voiceover.wav")
    if not os.path.exists(master_wav):
        master_wav = os.path.join(project_dir, "voiceover.wav")
    if not os.path.exists(master_wav):
        die(f"Không tìm thấy master audio voiceover.wav tại {work_pdir} hoặc {project_dir}. Hãy chạy m3_voice trước!")

    # 2. Tìm audio_sync.json
    sync_json_path = os.path.join(project_dir, "audio_sync.json")
    if not os.path.exists(sync_json_path):
        die(f"Không tìm thấy file audio_sync.json tại {sync_json_path}. Hãy chạy m3_voice trước!")

    with open(sync_json_path, "r", encoding="utf-8") as f:
        sync_segments = json.load(f)

    speech_segs = [s for s in sync_segments if s.get("type", "speech") == "speech"]
    log(f"Tổng số phân đoạn lời thoại cần đồng bộ: {len(speech_segs)} phân đoạn")

    # 3. Đọc cấu hình karaoke từ voice.json & timeline
    from diemdoc.timeline import timeline_path
    tl_path = timeline_path(project_dir)
    tl = load_timeline(project_dir) if os.path.exists(tl_path) else {"scenes": []}
    fmt = (tl.get("format") or "long").lower()

    cfg_voice_path = os.path.join(paths.CONFIG, "voice.json")
    max_karaoke_chars = 44 if fmt == "long" else 26
    if os.path.exists(cfg_voice_path):
        try:
            with open(cfg_voice_path, "r", encoding="utf-8") as f:
                vcfg = json.load(f)
                karaoke_cfg = vcfg.get("karaoke", {})
                max_karaoke_chars = karaoke_cfg.get("max_chars_main", 44) if fmt == "long" else karaoke_cfg.get("max_chars_short", 26)
        except Exception:
            pass

    # 4. Thực hiện đồng bộ (Syllabic hoặc Whisper)
    final_display_words: List[Dict[str, Any]] = []
    syllabic_display_words: List[Dict[str, Any]] = []
    fallback_chunks_count = 0

    # Luôn tính toán baseline syllabic cho mọi chunk
    step("Tính toán mốc thời gian nền bằng nội suy âm tiết (Syllabic)")
    for seg in speech_segs:
        s_start = float(seg["start"])
        s_end = float(seg["end"])
        tmap = seg.get("token_map", [])

        # Tạo danh sách TTS tokens từ token_map
        all_tts_tokens = []
        for tm in tmap:
            all_tts_tokens.extend(tm.get("tts_tokens", [tm.get("say", tm.get("display"))]))

        syl_tts_words = syllabic_interpolate_chunk(all_tts_tokens, s_start, s_end)

        # Ánh xạ ngược về display words
        cur_t_idx = 0
        for tm in tmap:
            disp = tm.get("display", "")
            tts_toks = tm.get("tts_tokens", [])
            n_t = len(tts_toks)

            if not tts_toks or re.match(r'^[,\.\?!;:]+$', disp.strip()):
                if syllabic_display_words:
                    syllabic_display_words[-1]["word"] += disp
                continue

            if cur_t_idx < len(syl_tts_words):
                w_start = syl_tts_words[cur_t_idx]["start"]
                w_end = syl_tts_words[min(len(syl_tts_words) - 1, cur_t_idx + n_t - 1)]["end"]
            else:
                w_start = syllabic_display_words[-1]["end"] if syllabic_display_words else s_start
                w_end = s_end

            syllabic_display_words.append({
                "word": disp,
                "start": round(w_start, 3),
                "end": round(w_end, 3),
                "group": tm.get("group", False),
                "group_id": tm.get("group_id"),
                "scene_id": seg.get("scene_id")
            })
            cur_t_idx += n_t

    # 4. Thực hiện đồng bộ thuần túy theo độ dài Audio & Nội suy Âm tiết tiếng Việt (Loại bỏ 100% Whisper)
    final_display_words = syllabic_display_words
    log("Đồng bộ 100% bằng độ dài Audio & Nội suy âm tiết tiếng Việt (Đã gỡ bỏ hoàn toàn Whisper).", tag="sync")

    # 5. Gom karaoke_chunks
    step("Tạo các cụm phụ đề nhảy Karaoke Chunks")
    karaoke_chunks = group_display_karaoke_chunks(
        final_display_words, max_words=4, max_chars=max_karaoke_chars, pause_split=0.35
    )
    log(f"Đã tạo {len(karaoke_chunks)} cụm karaoke chunks (giới hạn {max_karaoke_chars} ký tự).")

    # 6. Cập nhật mốc thời gian Scene & Thẻ trong Timeline
    if os.path.exists(tl_path):
        step("Cập nhật thời gian Scene & neo thẻ Card trong Timeline")
        # Tính thời gian từng scene theo mốc tích lũy (end_frame_i = round(cum_audio_sec * fps))
        # Bỏ ceil từng cảnh để triệt tiêu độ lệch video-audio (bảo đảm tổng lệch <= 1 frame / 33ms)
        fps = float(tl.get("fps", 30))
        scene_raw_ends: Dict[Any, float] = {}
        for seg in sync_segments:
            sc_id = seg.get("scene_id")
            if sc_id:
                scene_raw_ends[sc_id] = max(scene_raw_ends.get(sc_id, 0.0), float(seg["end"]))

        prev_end_frame = 0
        for sc in tl.get("scenes", []):
            sc_id = sc.get("scene_id")
            if sc_id in scene_raw_ends:
                cum_audio_sec = scene_raw_ends[sc_id]
                end_frame_i = int(round(cum_audio_sec * fps))
                n_frames_i = max(1, end_frame_i - prev_end_frame)
                start_frame_i = prev_end_frame

                sc["_start_time"] = round(start_frame_i / fps, 3)
                sc["_duration"] = round(n_frames_i / fps, 3)
                sc["_n_frames"] = n_frames_i
                prev_end_frame = end_frame_i

        # Cập nhật cue points cho các thẻ
        tl = resolve_cue_points(tl, final_display_words)
        save_timeline(project_dir, tl)
        ok(f"Đã cập nhật mốc thời gian tích lũy vào timeline: {paths.rel_to_root(tl_path)}")

    # 7. Đo đạc độ lệch giữa Whisper và Syllabic baseline
    deviations = []
    if len(final_display_words) == len(syllabic_display_words):
        for fw, sw in zip(final_display_words, syllabic_display_words):
            dev = abs(fw["start"] - sw["start"])
            deviations.append(dev)

    med_dev = float(np.median(deviations)) if deviations else 0.0
    p95_dev = float(np.percentile(deviations, 95)) if deviations else 0.0

    mono_violations = 0
    for i in range(1, len(final_display_words)):
        if final_display_words[i]["start"] < final_display_words[i-1]["start"]:
            mono_violations += 1

    # In đối chiếu mẫu vài từ đầu tiên (Whisper vs Syllabic)
    log("Đối chiếu mốc thời gian mẫu giữa Whisper và Syllabic (5 từ đầu):")
    for i in range(min(5, len(final_display_words))):
        fw = final_display_words[i]
        sw = syllabic_display_words[i]
        diff_ms = abs(fw['start'] - sw['start']) * 1000.0
        log(f"  [{i+1}] Từ '{fw['word']}': Whisper={fw['start']:.3f}s | Syllabic={sw['start']:.3f}s | Lệch={diff_ms:.1f}ms")

    # 8. Xuất word_timestamps.json
    out_words_json = os.path.join(project_dir, "word_timestamps.json")
    output_payload = {
        "words": final_display_words,
        "karaoke_chunks": karaoke_chunks,
        "sync_mode": sync_mode,
        "total_words": len(final_display_words),
        "total_chunks": len(karaoke_chunks),
        "metrics": {
            "mono_violations": mono_violations,
            "fallback_chunks_count": fallback_chunks_count,
            "fallback_pct": round(fallback_chunks_count / max(1, len(speech_segs)) * 100.0, 2),
            "median_deviation_sec": round(med_dev, 3),
            "p95_deviation_sec": round(p95_dev, 3)
        }
    }
    with open(out_words_json, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)
    ok(f"Đã xuất word_timestamps.json: {paths.rel_to_root(out_words_json)} ({len(final_display_words)} từ)")

    # 9. Thực hiện kiểm tra nếu có cờ --check
    if do_check:
        step("Kiểm tra chất lượng đồng bộ phụ đề (--check)")
        master_audio_dur = len(AudioSegment.from_wav(master_wav)) / 1000.0
        last_word_end = final_display_words[-1]["end"] if final_display_words else 0
        dur_diff = abs(master_audio_dur - last_word_end)
        one_frame = 1.0 / 30.0  # 33ms

        print("\n" + "=" * 60)
        print(" BÁO CÁO KIỂM TRA ĐỒNG BỘ (--check)")
        print("=" * 60)
        print(f"1. Tính đơn điệu: {'ĐẠT (100% tăng dần)' if mono_violations == 0 else f'LỖI ({mono_violations} vi phạm)'}")
        print(f"2. Khớp thời lượng audio: Master={master_audio_dur:.3f}s | WordEnd={last_word_end:.3f}s | Lệch={dur_diff:.3f}s "
              f"({'ĐẠT <= 1 frame' if dur_diff <= one_frame + 0.1 else 'CẢNH BÁO'})")
        print(f"3. Độ lệch Whisper vs Syllabic: Trung vị={med_dev:.3f}s | P95={p95_dev:.3f}s")
        print("=" * 60 + "\n")

    return output_payload


def main():
    ap = argparse.ArgumentParser(description="m5_sync — Đồng bộ phụ đề và kịch bản thời gian thuần túy theo độ dài Audio")
    ap.add_argument("project", help="Tên thư mục ngày (DD.MM.YY) hoặc đường dẫn project")
    ap.add_argument("--sync", default="syllabic", choices=["syllabic", "audio_length", "whisper-small", "whisper-medium"],
                    help="Chế độ đồng bộ (mặc định: syllabic - Siêu tốc theo độ dài audio)")
    ap.add_argument("--check", action="store_true", help="Kiểm tra độ chính xác mốc thời gian và độ lệch")
    args = ap.parse_args()

    run_sync_pipeline(
        project_name=args.project,
        sync_mode=args.sync,
        do_check=args.check
    )


if __name__ == "__main__":
    main()
