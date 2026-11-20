#!/usr/bin/env python3
"""
whisper_batch_worker.py — Tiến trình con chạy Whisper theo từng lô âm thanh (Batch Worker)
========================================================================================
Chạy trong tiến trình con độc lập để giải phóng 100% RAM sau khi hoàn tất lô âm thanh.
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
import time
import os
import whisper


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="small", choices=["small", "medium"])
    ap.add_argument("--wav", required=True)
    ap.add_argument("--prompt", default="")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    if not os.path.exists(args.wav):
        print(f"Error: wav not found: {args.wav}", file=sys.stderr)
        sys.exit(1)

    t0 = time.time()
    model = whisper.load_model(args.model)
    res = model.transcribe(
        args.wav,
        language="vi",
        word_timestamps=True,
        initial_prompt=args.prompt,
        verbose=False
    )

    words = []
    for s in res.get("segments", []):
        for w in s.get("words", []):
            words.append({
                "word": w.get("word", "").strip(),
                "start": round(float(w.get("start", 0)), 3),
                "end": round(float(w.get("end", 0)), 3),
                "probability": round(float(w.get("probability", 1.0)), 3)
            })

    output_data = {
        "text": res.get("text", "").strip(),
        "words": words,
        "elapsed_sec": round(time.time() - t0, 3)
    }

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
