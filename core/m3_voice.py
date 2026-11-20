#!/usr/bin/env python3
"""
m3 — VOICE (ViTTS Provider cho kênh Điểm Đọc)
=============================================
Tạo file giọng đọc master (voiceover.wav) và dữ liệu đồng bộ audio_sync.json.
- Sử dụng mô hình ViTTS v3turbo với chất giọng bản địa Minh Quân Pro.
- Hỗ trợ cả 2 chế độ: Timeline video chính (16:9) và Units JSON cho video phụ (9:16).
- Tách chunk thông minh (tối đa 45-60 từ), tích hợp cache cấp chunk bằng SHA-256.
- Áp dụng bộ lọc thể thao: rubberband=pitch:tempo qua FFmpeg.
- Mốc thời gian chính xác theo SỐ LƯỢNG MẪU (sample-accurate), triệt tiêu trôi dạt mili-giây.

Cách dùng:
  python3 core/m3_voice.py <project>
  python3 core/m3_voice.py <project> --scene 2
  python3 core/m3_voice.py <project> --units units.json
  python3 core/m3_voice.py <project> --speed 1.25
  python3 core/m3_voice.py <project> --no-cache
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
from typing import List, Dict, Any, Tuple
import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_leading_silence

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core", "vendor"))
sys.path.insert(1, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.timeline import load_timeline
from diemdoc.tts_text import prepare

CODE_VERSION = "v4.1_diemdoc_nocut"


def _split_into_sentences(text: str) -> List[str]:
    """Tách văn bản thành các câu dựa trên dấu chấm, chấm than, hỏi, chấm phẩy và ngắt dòng."""
    raw = re.split(r'([\.!\?;\n]+)', text)
    sentences = []
    for i in range(0, len(raw) - 1, 2):
        s = raw[i].strip() + (raw[i+1].strip() if i+1 < len(raw) else "")
        s = s.strip()
        if s:
            sentences.append(s)
    if len(raw) % 2 == 1 and raw[-1].strip():
        sentences.append(raw[-1].strip())
    return sentences if sentences else ([text.strip()] if text.strip() else [])


def _split_long_sentence(sentence: str, max_words: int = 60) -> List[str]:
    """
    Tách câu dài (>max_words từ) tại các ranh giới cú pháp an toàn:
    1. Dấu hai chấm (:), chấm phẩy (;), gạch ngang (—, -)
    2. Dấu phẩy (,)
    3. Liên từ phụ thuộc / đẳng lập (đồng thời, và, nhưng, trong khi, bởi vì)
    Tuyệt đối không cắt ngang cụm từ hoặc chém đôi từ ngữ.
    """
    words = sentence.split()
    if len(words) <= max_words:
        return [sentence]

    # 1. Thử tách tại dấu chấm phẩy hoặc gạch ngang dài
    for sep in [";", " — ", " - "]:
        if sep in sentence:
            parts = sentence.split(sep)
            if all(len(p.split()) <= max_words for p in parts if p.strip()):
                return [p.strip() + (sep if sep == ";" else "") for p in parts if p.strip()]

    # 2. Thử tách theo dấu phẩy
    comma_parts = sentence.split(",")
    if len(comma_parts) > 1:
        chunks = []
        cur = ""
        for cp in comma_parts:
            cp_str = cp.strip()
            if not cp_str:
                continue
            if not cur:
                cur = cp_str
            elif len(cur.split()) + len(cp_str.split()) <= max_words:
                cur += ", " + cp_str
            else:
                chunks.append(cur + ",")
                cur = cp_str
        if cur:
            chunks.append(cur)
        if all(len(c.split()) <= max_words + 15 for c in chunks):
            return chunks

    # 3. Thử tách tại liên từ tự nhiên
    conjunctions = [" đồng thời ", " và ", " nhưng ", " trong khi ", " bởi vì "]
    for conj in conjunctions:
        if conj in sentence:
            idx = sentence.find(conj)
            left = sentence[:idx].strip()
            right = sentence[idx:].strip()
            if len(left.split()) <= max_words + 10 and len(right.split()) <= max_words + 10:
                return [left, right]

    # 4. Fallback: Tách tại khoảng trắng giữa câu
    mid = len(words) // 2
    return [" ".join(words[:mid]), " ".join(words[mid:])]


def build_chunks_from_text(raw_text: str, max_words_per_chunk: int = 60, inter_sentence_pause: float = 0.25) -> List[Dict[str, Any]]:
    """
    Phân tích văn bản kịch bản thành các chunk TTS tự nhiên:
    - Bóc tách các thẻ [PAUSE x.xs]
    - Giữ nguyên vẹn từng câu hoàn chỉnh (<= max_words_per_chunk từ) để ViTTS phát âm tự nhiên 100%
    - Bổ sung khoảng thở tự nhiên (0.25s) giữa các câu để giọng đọc có nhịp điệu chuyên nghiệp
    - Trả về danh sách dict {type: 'speech'|'pause', text: str, pause_sec: float}
    """
    pattern = r'\[PAUSE\s+([0-9.]+)s?\]'
    parts = re.split(pattern, raw_text)

    chunks: List[Dict[str, Any]] = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            try:
                pause_val = float(part)
                chunks.append({"type": "pause", "text": "", "pause_sec": pause_val})
            except ValueError:
                pass
            continue

        text_block = part.strip()
        if not text_block:
            continue

        sentences = _split_into_sentences(text_block)
        for s in sentences:
            sub_s_list = _split_long_sentence(s, max_words=max_words_per_chunk)
            for sub_s in sub_s_list:
                s_str = sub_s.strip()
                if not s_str:
                    continue
                chunks.append({"type": "speech", "text": s_str, "pause_sec": 0.0})
                # Bổ sung khoảng thở tự nhiên nếu câu kết thúc bằng dấu chấm / chấm than / chấm hỏi
                if inter_sentence_pause > 0 and s_str[-1] in ".!?":
                    chunks.append({"type": "pause", "text": "", "pause_sec": inter_sentence_pause})

    # Dọn khoảng pause thừa ở cuối cùng của đoạn text nếu có
    if chunks and chunks[-1].get("type") == "pause":
        chunks.pop()

    return chunks


def trim_segment_silence(audio: AudioSegment, silence_threshold_db: float = -42.0) -> AudioSegment:
    """Cắt khoảng lặng ở đầu và cuối phân đoạn audio."""
    start_trim = detect_leading_silence(audio, silence_threshold=silence_threshold_db)
    end_trim = detect_leading_silence(audio.reverse(), silence_threshold=silence_threshold_db)
    duration = len(audio)
    if start_trim >= duration:
        return audio
    return audio[start_trim:duration - end_trim]


def compute_chunk_hash(text_tts: str, voice: str, mode: str, temp: float, speed: float, pitch: float, max_chars: int = 768) -> str:
    """Tạo khóa hash duy nhất cho chunk TTS phục vụ cache."""
    key_str = f"{text_tts.strip()}|{voice}|{mode}|{temp:.2f}|{speed:.2f}|{pitch:.2f}|{max_chars}|{CODE_VERSION}"
    return hashlib.sha256(key_str.encode("utf-8")).hexdigest()


def render_chunk_vitts(model: Any, text_tts: str, voice: str, temperature: float,
                       speed: float, pitch: float, cache_dir: str, use_cache: bool = True,
                       max_chars: int = 768) -> Tuple[AudioSegment, bool]:
    """
    Sinh audio cho một chunk đơn lẻ với cơ chế cache cấp chunk và xử lý FFmpeg filter.
    Bắt buộc truyền max_chars=768 (hoặc cao hơn) để ViTTS không tự ý bẻ gãy câu ở tầng phoneme.
    """
    h = compute_chunk_hash(text_tts, voice, "v3turbo", temperature, speed, pitch, max_chars=max_chars)
    cache_wav = os.path.join(cache_dir, f"{h}.wav")
    cache_meta = os.path.join(cache_dir, f"{h}.json")

    if use_cache and os.path.exists(cache_wav) and os.path.getsize(cache_wav) > 1000:
        try:
            seg = AudioSegment.from_wav(cache_wav)
            return seg, True
        except Exception:
            pass

    # Cache miss: chạy sinh giọng qua vieneu với max_chars=768 tránh cắt ngang câu
    last_err = None
    for attempt in range(2):
        try:
            audio_data = model.infer(text_tts, voice=voice, temperature=temperature, max_chars=max_chars)
            break
        except Exception as e:
            last_err = e
            if attempt == 1:
                die(f"Lỗi sinh ViTTS chunk: '{text_tts[:40]}...' sau 2 lần thử: {last_err}")

    raw_tmp = os.path.join(cache_dir, f"tmp_raw_{h}.wav")
    fx_tmp = os.path.join(cache_dir, f"tmp_fx_{h}.wav")
    model.save(audio_data, raw_tmp)

    # Lọc qua rubberband của FFmpeg
    if abs(pitch - 1.0) > 0.01:
        filter_str = f"rubberband=pitch={pitch}:tempo={speed}"
    else:
        filter_str = f"atempo={speed}"

    res = subprocess.run(
        ["ffmpeg", "-y", "-i", raw_tmp, "-filter:a", filter_str, fx_tmp],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    if res.returncode != 0 or not os.path.exists(fx_tmp):
        # Fallback sang atempo
        subprocess.run(
            ["ffmpeg", "-y", "-i", raw_tmp, "-filter:a", f"atempo={speed}", fx_tmp],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )

    seg = AudioSegment.from_wav(fx_tmp)
    seg = trim_segment_silence(seg)

    # Lưu vào cache chính thức
    seg.export(cache_wav, format="wav")
    meta = {
        "text_tts": text_tts, "voice": voice, "speed": speed, "pitch": pitch,
        "temperature": temperature, "duration_ms": len(seg), "hash": h
    }
    with open(cache_meta, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False)

    # Dọn file tạm
    for p in (raw_tmp, fx_tmp):
        if os.path.exists(p):
            try: os.remove(p)
            except Exception: pass

    return seg, False


def resolve_voice_preset(requested: str | None, vcfg: dict) -> dict:
    """Ánh xạ alias hoặc tên yêu cầu sang cấu hình giọng đọc chuẩn."""
    presets = vcfg.get("presets", {})
    primary = presets.get("primary", {
        "voice": vcfg.get("voice", "Minh Quân Pro"),
        "speed": vcfg.get("speed", 1.12),
        "pitch": vcfg.get("pitch", 0.93),
        "temperature": vcfg.get("temperature", 0.6)
    })
    secondary = presets.get("secondary", {
        "voice": "Ngọc Huyền",
        "speed": 1.12,
        "pitch": 1.10,
        "temperature": 0.5
    })

    if not requested:
        return primary

    req_str = str(requested).strip().lower()
    if req_str in ["secondary", "female", "nu", "nữ", "ngoc_huyen", "ngọc huyền", "14"]:
        return secondary
    if req_str in ["primary", "male", "nam", "minh_quan", "minh quân", "minh quân pro", "15", "default"]:
        return primary

    if req_str in presets:
        return presets[req_str]

    return {
        "voice": str(requested).strip(),
        "speed": primary.get("speed", 1.12),
        "pitch": primary.get("pitch", 1.0),
        "temperature": primary.get("temperature", 0.6)
    }


def run_voice_pipeline(project_name: str, scene_filter: int | None = None,
                       units_path: str | None = None, speed_override: float | None = None,
                       voice_override: str | None = None,
                       no_cache: bool = False) -> str:
    """Hàm điều phối toàn bộ quy trình sinh giọng đọc cho project."""
    project_dir = paths.project_dir(project_name)
    work_pdir = paths.work_project_dir(project_name)
    tts_cache_dir = paths.work_file("tts_cache")
    os.makedirs(tts_cache_dir, exist_ok=True)

    # 1. Đọc cấu hình từ config/voice.json và project/voice.json
    cfg_voice_path = os.path.join(paths.CONFIG, "voice.json")
    vcfg = {}
    if os.path.exists(cfg_voice_path):
        try:
            with open(cfg_voice_path, "r", encoding="utf-8") as f:
                vcfg = json.load(f)
        except Exception:
            pass

    proj_voice_path = os.path.join(project_dir, "voice.json")
    if os.path.exists(proj_voice_path):
        try:
            with open(proj_voice_path, "r", encoding="utf-8") as f:
                pvcfg = json.load(f)
                vcfg.update(pvcfg)
        except Exception:
            pass

    tl_voice_req = None
    if not units_path:
        try:
            tl_temp = load_timeline(project_dir)
            tl_vc = tl_temp.get("voice_config", {})
            if isinstance(tl_vc, dict):
                tl_voice_req = tl_vc.get("preset") or tl_vc.get("voice")
        except Exception:
            pass

    effective_req = voice_override or tl_voice_req or vcfg.get("default_preset")
    chosen = resolve_voice_preset(effective_req, vcfg)

    voice_name = chosen.get("voice", "Minh Quân Pro")
    speed = speed_override or chosen.get("speed", 1.12)
    pitch = chosen.get("pitch", 0.93)
    temperature = chosen.get("temperature", 0.6)
    max_words_per_chunk = vcfg.get("max_words_per_chunk", 60)

    banner(f"M3 — VOICE ({voice_name} | spd={speed} | pch={pitch})", project_name)

    step("Thu thập phân đoạn kịch bản")
    items_to_render: List[Dict[str, Any]] = []

    if units_path:
        # Chế độ Units JSON (dành cho video phụ 9:16)
        u_full = os.path.abspath(units_path) if os.path.exists(units_path) else os.path.join(project_dir, units_path)
        if not os.path.exists(u_full):
            die(f"Không tìm thấy file units: {u_full}")
        with open(u_full, "r", encoding="utf-8") as f:
            units_data = json.load(f)
        for u in units_data:
            u_id = u.get("id", "unit")
            u_text = u.get("text", "").strip()
            p_after = float(u.get("pause_after", 0.3))
            chunks = build_chunks_from_text(u_text, max_words_per_chunk)
            if p_after > 0 and chunks and chunks[-1].get("type") == "pause":
                chunks.pop()
            for c in chunks:
                c["item_id"] = u_id
                c["scene_id"] = u_id
                items_to_render.append(c)
            if p_after > 0:
                items_to_render.append({"type": "pause", "text": "", "pause_sec": p_after, "item_id": u_id, "scene_id": u_id})
    else:
        # Chế độ Timeline video chính (16:9)
        tl = load_timeline(project_dir)
        scenes = tl.get("scenes", [])
        if not scenes:
            die(f"Timeline không có scenes nào: {project_dir}")

        for sc_idx, sc in enumerate(scenes, 1):
            sc_id = sc.get("scene_id", f"scene_{sc_idx:02d}")
            if scene_filter is not None and sc_idx != scene_filter:
                continue
            script = sc.get("script_text", "").strip()
            if not script:
                warn(f"Cảnh {sc_id} không có script_text.")
                continue

            chunks = build_chunks_from_text(script, max_words_per_chunk)
            if chunks and chunks[-1].get("type") == "pause":
                chunks.pop()
            for c in chunks:
                c["item_id"] = sc_id
                c["scene_id"] = sc_id
                items_to_render.append(c)

            # Thêm khoảng nghỉ tự nhiên 0.8s giữa các cảnh để tránh dính chữ giữa các tin
            items_to_render.append({
                "type": "pause",
                "text": "",
                "pause_sec": 0.8,
                "item_id": sc_id,
                "scene_id": sc_id
            })

    speech_chunks = [it for it in items_to_render if it["type"] == "speech"]
    log(f"Tổng số chunk giọng đọc cần sinh: {len(speech_chunks)} chunks (Giọng: {voice_name}, speed={speed}, pitch={pitch})")

    # 2. Khởi tạo ViTTS
    step("Nạp mô hình ViTTS v3turbo")
    from vieneu import Vieneu
    model = Vieneu(mode="v3turbo")

    # 3. Sinh từng chunk và nối sample-accurate
    step("Sinh giọng đọc & đồng bộ từng đoạn")
    master_audio = AudioSegment.empty()
    sync_records: List[Dict[str, Any]] = []
    chunk_loudness_list: List[float] = []

    # Giả định sample rate chuẩn là 44100 hoặc theo segment
    sample_rate = 44100
    accumulated_samples = 0
    total_hits = 0
    total_misses = 0

    for idx, item in enumerate(items_to_render):
        item_id = item.get("item_id", f"item_{idx}")
        scene_id = item.get("scene_id", "scene_01")

        if item["type"] == "pause":
            pause_ms = int(item["pause_sec"] * 1000)
            if pause_ms > 0:
                silence_seg = AudioSegment.silent(duration=pause_ms, frame_rate=sample_rate)
                silence_samples = len(silence_seg.get_array_of_samples()) // silence_seg.channels
                start_sec = accumulated_samples / sample_rate
                accumulated_samples += silence_samples
                end_sec = accumulated_samples / sample_rate

                sync_records.append({
                    "id": f"pause_{idx}",
                    "scene_id": scene_id,
                    "type": "pause",
                    "text_display": "",
                    "text_tts": "",
                    "start": round(start_sec, 3),
                    "end": round(end_sec, 3),
                    "duration": round(item["pause_sec"], 3),
                    "cache_hit": True
                })
                master_audio += silence_seg
            continue

        # Speech chunk
        display_raw = item["text"]
        tts_clean, token_map = prepare(display_raw)

        seg, is_hit = render_chunk_vitts(
            model, tts_clean, voice_name, temperature, speed, pitch,
            tts_cache_dir, use_cache=not no_cache
        )
        if is_hit:
            total_hits += 1
            hit_str = "[hit]"
        else:
            total_misses += 1
            hit_str = "[miss]"

        # Khớp 0.00s cho câu đầu tiên của toàn video
        if idx == 0:
            lead_ms = detect_leading_silence(seg)
            if lead_ms > 0:
                seg = seg[lead_ms:]

        seg_sr = seg.frame_rate
        if seg_sr != sample_rate:
            seg = seg.set_frame_rate(sample_rate)
        if seg.channels != 1:
            seg = seg.set_channels(1)

        # Đo mức dBFS để kiểm tra độ đồng đều
        if seg.dBFS != -float('inf'):
            chunk_loudness_list.append(seg.dBFS)

        seg_samples = len(seg.get_array_of_samples())
        start_sec = accumulated_samples / sample_rate
        accumulated_samples += seg_samples
        end_sec = accumulated_samples / sample_rate
        dur_sec = seg_samples / sample_rate

        log(f"  {hit_str} [{idx+1:02d}/{len(items_to_render):02d}] {display_raw[:35]}... ({dur_sec:.2f}s)")

        sync_records.append({
            "id": f"chunk_{idx:03d}",
            "scene_id": scene_id,
            "type": "speech",
            "text_display": display_raw,
            "text_tts": tts_clean,
            "token_map": token_map,
            "start": round(start_sec, 3),
            "end": round(end_sec, 3),
            "duration": round(dur_sec, 3),
            "cache_hit": is_hit
        })

        master_audio += seg

    # 4. Kiểm tra độ lệch mức âm lượng
    if chunk_loudness_list:
        median_db = float(np.median(chunk_loudness_list))
        for rec in sync_records:
            if rec["type"] == "speech":
                # Đo lại nếu cần
                pass
        log(f"Mức âm lượng trung vị các chunk: {median_db:.1f} dBFS (Cache hits: {total_hits}, Misses: {total_misses})")

    # 5. Xuất master voiceover.wav vào WORK/<project>/ và audio_sync.json vào projects/<project>/
    step("Xuất bản tệp âm thanh và mốc thời gian")
    out_master_wav = paths.work_project_file(project_name, "voiceover.wav")
    master_audio.export(out_master_wav, format="wav")
    total_dur_sec = len(master_audio) / 1000.0

    # Sao chép thêm một bản vào project_dir để mọi engine/module đều tiếp cận trực tiếp được
    proj_wav = os.path.join(project_dir, "voiceover.wav")
    try:
        shutil.copy2(out_master_wav, proj_wav)
    except Exception:
        pass

    out_sync_json = os.path.join(project_dir, "audio_sync.json")
    with open(out_sync_json, "w", encoding="utf-8") as f:
        json.dump(sync_records, f, ensure_ascii=False, indent=2)

    ok(f"Đã xuất master audio: {paths.rel_to_root(out_master_wav)} ({total_dur_sec:.2f}s, {total_dur_sec/60:.2f} phút)")
    ok(f"Đã xuất audio sync: {paths.rel_to_root(out_sync_json)} ({len(sync_records)} phân đoạn)")

    return out_master_wav


def main() -> None:
    ap = argparse.ArgumentParser(description="m3 — Sinh giọng đọc ViTTS v3turbo cho Điểm Đọc")
    ap.add_argument("project", help="Tên dự án hoặc đường dẫn project")
    ap.add_argument("--scene", type=int, default=None, help="Chỉ render 1 cảnh cụ thể")
    ap.add_argument("--units", default=None, help="File JSON danh sách tin vắn (dành cho video phụ)")
    ap.add_argument("--voice", default=None, help="Chọn giọng đọc hoặc preset: 'female'/'secondary' (Ngọc Huyền #14), 'male'/'primary' (Minh Quân Pro #15), hoặc tên cụ thể")
    ap.add_argument("--speed", type=float, default=None, help="Ghi đè tốc độ đọc (ví dụ 1.25)")
    ap.add_argument("--no-cache", action="store_true", help="Bỏ qua cache TTS cấp chunk")
    args = ap.parse_args()

    run_voice_pipeline(
        project_name=args.project,
        scene_filter=args.scene,
        units_path=args.units,
        speed_override=args.speed,
        voice_override=args.voice,
        no_cache=args.no_cache
    )


if __name__ == "__main__":
    main()
