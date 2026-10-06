#!/usr/bin/env python3
"""Build the cut list from hand-picked source ranges, tightening inner pauses by word timings.

Writes pieces.json: [{src_in, src_out, out_start, block}] and prints the ffmpeg-ready summary.
"""
import json
from pathlib import Path

import numpy as np

from pauses import pauses

MEDIA = Path(__file__).resolve().parents[3] / "media"
ENV = np.load(Path(__file__).with_name("env.npy"))  # built by pauses.py

# (block id, source in, source out) — chosen from the transcript; everything else is drafts/fumbling.
# The whole take is content (the unpacking included): contiguous blocks, nothing removed.
# Blocks only drive framing changes and graphics.
RANGES = [
    ("hook", 0.00, 18.70),
    ("carry", 18.70, 47.20),
    ("gloves", 47.20, 97.50),
    ("device", 97.50, 112.30),
    ("functions", 112.30, 136.10),
    ("stat", 136.10, 165.20),
    ("veins", 165.20, 183.00),
    ("compact", 183.00, 187.80),
    ("cta", 187.80, 197.17),
]
CUT_PAUSES = False  # v1 tightened pauses; the client wants the full take kept
THRESH_DB = -38.0  # speech-band level below which a stretch counts as a pause
MIN_PAUSE = 0.4    # shorter pauses are natural rhythm and stay
PAD = 0.12         # breathing room kept on each side of a cut pause
FPS = 30


def split(block, a, b):
    if not CUT_PAUSES:
        return [(block, round(round(a * FPS) / FPS, 4), round(round(b * FPS) / FPS, 4))]
    cuts, start = [], a
    for x, y in pauses(ENV, a, b, THRESH_DB, MIN_PAUSE):
        if x - a < 0.05:          # leading silence: just start later
            start = y - PAD
            continue
        if b - y < 0.05:          # trailing silence: end earlier
            b = x + PAD
            break
        cuts.append((start, x + PAD))
        start = y - PAD
    cuts.append((start, b))
    # Snap to the 30 fps frame grid so picture and sound pieces have identical lengths.
    snap = lambda t: round(round(t * FPS) / FPS, 4)
    return [(block, snap(x), snap(y)) for x, y in cuts if y - x > 0.3]


pieces, t = [], 0.0
for block, a, b in RANGES:
    for blk, x, y in split(block, a, b):
        pieces.append({"block": blk, "src_in": x, "src_out": y, "out_start": round(t, 4)})
        t += y - x

Path("pieces.json").write_text(json.dumps(pieces, indent=1))
print(f"{len(pieces)} pieces, total {t:.2f}s")
