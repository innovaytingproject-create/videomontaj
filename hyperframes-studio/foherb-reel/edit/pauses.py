#!/usr/bin/env python3
"""Find pauses inside kept ranges from the speech-band loudness envelope (Whisper word times smear over pauses)."""
import subprocess, sys
import numpy as np
from pathlib import Path

MEDIA = Path(__file__).resolve().parents[3] / "media"
SR, HOP = 16000, 0.02


def envelope():
    # Speech band only (250-3500 Hz) so packaging rustle and hum weigh less.
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(MEDIA / "clean.wav"), "-af",
                          "highpass=f=250,lowpass=f=3500", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    a = np.frombuffer(raw, np.float32)
    n = int(SR * HOP)
    frames = a[: len(a) // n * n].reshape(-1, n)
    db = 20 * np.log10(np.sqrt((frames ** 2).mean(1)) + 1e-9)
    return np.convolve(db, np.ones(5) / 5, mode="same")  # 100 ms smoothing


def pauses(db, a, b, thresh, min_len):
    i0, i1 = int(a / HOP), int(b / HOP)
    quiet = db[i0:i1] < thresh
    out, start = [], None
    for k, q in enumerate(quiet):
        if q and start is None:
            start = k
        if (not q or k == len(quiet) - 1) and start is not None:
            if (k - start) * HOP >= min_len:
                out.append((round(a + start * HOP, 2), round(a + k * HOP, 2)))
            start = None
    return out


if __name__ == "__main__":
    db = envelope()
    speech = np.percentile(db, 75)
    print(f"p10={np.percentile(db,10):.1f} p50={np.percentile(db,50):.1f} p75={speech:.1f} p95={np.percentile(db,95):.1f}")
    thresh = speech - float(sys.argv[1]) if len(sys.argv) > 1 else speech - 14
    np.save("env.npy", db)
    print("threshold", round(thresh, 1))
