#!/usr/bin/env python3
"""Find speech pieces without pauses (for prepare_reel.py).

Usage: python find_pieces.py <kit-project> <start:end> [<start:end> ...] [--gap 0.3]

Reads whieda-video-kit/projects/<name>/work/voice.wav, finds silences longer than
--gap seconds (level < -32 dB) inside each range and prints the pieces to keep,
with ~0.06 s of air left around every word. Paste the output into prepare_reel.py.
Check the cuts by ear/level afterwards: a quiet consonant can read as silence.
"""
import subprocess, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
args = sys.argv[1:]
gap = 0.3
if "--gap" in args:
    i = args.index("--gap"); gap = float(args[i + 1]); del args[i:i + 2]
name, ranges = args[0], [tuple(map(float, a.split(":"))) for a in args[1:]]
wav = ROOT.parent / "whieda-video-kit" / "projects" / name / "work" / "voice.wav"
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(wav), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(raw, np.float32); SR = 16000; HOP = 0.02; PAD = 0.06


def level(t):
    x = a[int(t * SR):int((t + HOP) * SR)]
    return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9) if len(x) else -99


pieces = []
for r0, r1 in ranges:
    ts = np.arange(r0, r1, HOP)
    loud = [level(t) > -32 for t in ts]
    # first/last sound in the range
    idx = [i for i, l in enumerate(loud) if l]
    if not idx:
        continue
    start = max(r0, ts[idx[0]] - PAD)
    end = min(r1, ts[idx[-1]] + HOP + PAD)
    cur = start
    i = idx[0]
    while i <= idx[-1]:
        if not loud[i]:
            j = i
            while j <= idx[-1] and not loud[j]:
                j += 1
            if (j - i) * HOP >= gap:
                pieces.append((round(cur, 2), round(ts[i] + PAD, 2)))
                cur = ts[j] - PAD
            i = j
        else:
            i += 1
    pieces.append((round(cur, 2), round(end, 2)))

total = sum(b - a_ for a_, b in pieces)
print(" ".join(f"{p0:.2f}:{p1:.2f}" for p0, p1 in pieces))
print(f"# {len(pieces)} pieces, {total:.2f} s (was {sum(b - a_ for a_, b in ranges):.2f} s)", file=sys.stderr)
