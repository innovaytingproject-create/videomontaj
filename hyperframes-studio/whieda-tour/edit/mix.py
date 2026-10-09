#!/usr/bin/env python3
"""Final mix for the WHIEDA tour: voice -13 LUFS, Chronos bed ducked, SFX on every event."""
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
LEN = 90.6
trans = [float(x) for x in (ROOT / "edit" / "transitions.txt").read_text().split()]
cards = [9.8, 28.6, 38.2, 50.2, 72.7, 78.2]
ev = []  # (file, time, gain_db)
for t in trans:
    ev += [("whoosh", t - .35, 0), ("boom", t, -6)]
for a in cards:
    ev += [("boom", a + .26, -3)]
ev += [("pop", a + .6, -2) for a in (9.8, 28.6, 78.2)]           # icons on cards
ev += [("pop", t, 0) for t in (1.34, 23.6, 64.0, 3.53)]           # logo plates, cover
ev += [("tick", 3.9, 0), ("ding", 7.8, -4)]
ev += [("tick", t, 0) for t in (16.9, 32.7, 43.4)]                # pills
ev += [("pop", t, -1) for t in (59.3, 60.2, 62.0)]                # bubbles
ev += [("riser", 86.9, -5), ("pop", 89.0, 0), ("paydone", 17.08, -6)]
inputs = ["-i", "out/pic.mp4", "-i", "assets/voice.wav", "-i", "assets/music-chronos.mp3"]
fc = [f"[1:a]aresample=48000,atrim=0:{LEN},apad=whole_dur={LEN},volume=2dB,asplit=2[voice][key]",
      f"[2:a]aresample=48000,atrim=0:{LEN},asetpts=PTS-STARTPTS,volume=-17dB,"
      f"volume='1+min(max(t-87.9,0)/0.5,1)*0.55':eval=frame,afade=t=in:d=0.5,afade=t=out:st={LEN-1.6}:d=1.6[bed]",
      "[bed][key]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400:makeup=1[ducked]"]
labels = []
for i, (f, t, g) in enumerate(ev):
    inputs += ["-i", f"assets/sfx/{f}.wav"]
    fc.append(f"[{3+i}:a]aresample=48000,adelay={int(max(t,0)*1000)}:all=1,volume={g}dB[e{i}]")
    labels.append(f"[e{i}]")
fc.append("".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0,volume=-14dB,apad=whole_dur={LEN}[sfx]")
fc.append("[voice][ducked][sfx]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-13:TP=-1.0:LRA=9[mix]")
cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[mix]",
       "-t", str(LEN), "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "out/whieda-tur-po-ofisu.mp4"]
subprocess.run(cmd, check=True, cwd=ROOT)
print("events:", len(ev))
