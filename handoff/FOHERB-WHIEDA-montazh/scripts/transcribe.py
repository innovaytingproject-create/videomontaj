#!/usr/bin/env python3
"""Transcribe a video/audio file to word-level timestamps for cuts and captions.

Usage: python3 scripts/transcribe.py media/source.mp4 [--model large-v3-turbo] [--lang ru]
Writes <input>.words.json (per-word timings) and <input>.srt next to the input.
"""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

from faster_whisper import WhisperModel


def srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def load_audio(path: Path) -> np.ndarray:
    # Decode with ffmpeg directly: faster-whisper's PyAV decoder breaks on some PyAV versions.
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
        check=True,
        capture_output=True,
    ).stdout
    return np.frombuffer(raw, np.float32)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--model", default="large-v3-turbo")
    p.add_argument("--lang", default="ru")
    args = p.parse_args()

    src = Path(args.input)
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(
        load_audio(src), language=args.lang, word_timestamps=True, vad_filter=True
    )

    words, srt = [], []
    for i, seg in enumerate(segments, 1):
        srt.append(f"{i}\n{srt_time(seg.start)} --> {srt_time(seg.end)}\n{seg.text.strip()}\n")
        for w in seg.words or []:
            words.append({"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})

    src.with_suffix(".words.json").write_text(json.dumps(words, ensure_ascii=False, indent=1))
    src.with_suffix(".srt").write_text("\n".join(srt))
    print(f"{len(words)} words -> {src.with_suffix('.words.json')}")


if __name__ == "__main__":
    main()
