#!/usr/bin/env python3
"""Final audio mix onto the rendered picture (out/pic.mp4 -> out/<name>.mp4).

Usage: python3 pipeline/mix.py <name> [--sample]

Voice is the boss (-13 LUFS integrated for the whole mix); music bed
(assets/music/<music>.mp3) at -17 dB and ducked 4:1 under the voice; SFX are
derived from project.json: whoosh+boom on every camera transition, boom on
accent cards, pop on logos/icons/bubbles, tick on pills and cover, ding on
the banner, riser+pop on the end card, plus anything listed in "sfx".
"""
import argparse, json, subprocess
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("name")
ap.add_argument("--sample", action="store_true")
a = ap.parse_args()
P = KIT / "projects" / a.name
cfg = json.loads((P / "project.json").read_text())
tm = json.loads((P / "work" / "timing.json").read_text())
LEN = tm["duration"]

ev = []  # (sfx, time, gain dB)
for t in tm["transitions"]:
    ev += [("whoosh", t - .35, 0), ("boom", t, -6)]
for c in cfg.get("cards", []):
    ev.append(("boom", c["start"] + .26, -3))
    if c.get("icon"):
        ev.append(("pop", c["start"] + .6, -2))
ev += [("pop", s, 0) for s, _ in cfg.get("logos", [])]
if cfg.get("cover"):
    ev += [("pop", cfg["cover"]["start"] + .03, 0), ("tick", cfg["cover"]["start"] + .4, 0)]
ev += [("ding", b["start"] + .05, -4) for b in cfg.get("banners", [])]
ev += [("tick", p["start"], 0) for p in cfg.get("pills", [])]
if cfg.get("bubbles"):
    ev += [("pop", t, -1) for t, _ in cfg["bubbles"]["items"]]
if tm.get("end_card_at"):
    e = tm["end_card_at"]
    ev += [("riser", e - 1.15, -5), ("pop", e + .95, 0)]
ev += [tuple(x) for x in cfg.get("sfx", [])]
ev = [e for e in ev if 0 <= e[1] < LEN - .1]

music = KIT / "assets" / "music" / f'{cfg.get("music", "chronos")}.mp3'
inputs = ["-i", str(P / "out" / "pic.mp4"), "-i", str(P / "work" / "voice.wav"), "-stream_loop", "-1", "-i", str(music)]
lift = f"volume='1+min(max(t-{tm['end_card_at'] - .15:.2f},0)/0.5,1)*0.55':eval=frame," if tm.get("end_card_at") else ""
fc = [f"[1:a]aresample=48000,atrim=0:{LEN},apad=whole_dur={LEN},volume=2dB,asplit=2[voice][key]",
      f"[2:a]aresample=48000,atrim=0:{LEN},asetpts=PTS-STARTPTS,volume=-17dB,{lift}afade=t=in:d=0.5,afade=t=out:st={LEN - 1.6:.2f}:d=1.6[bed]",
      "[bed][key]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=400:makeup=1[ducked]"]
labels = []
for i, (f, t, g) in enumerate(ev):
    inputs += ["-i", str(KIT / "assets" / "sfx" / f"{f}.wav")]
    fc.append(f"[{3 + i}:a]aresample=48000,adelay={int(t * 1000)}:all=1,volume={g}dB[e{i}]")
    labels.append(f"[e{i}]")
if labels:
    fc.append("".join(labels) + f"amix=inputs={len(labels)}:duration=longest:normalize=0,volume=-14dB,apad=whole_dur={LEN}[sfx]")
    fc.append("[voice][ducked][sfx]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-13:TP=-1.0:LRA=9[mix]")
else:
    fc.append("[voice][ducked]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-13:TP=-1.0:LRA=9[mix]")
out = P / "out" / (f"{a.name}-15s.mp4" if a.sample else f"{a.name}.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[mix]",
                "-t", f"{LEN:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)], check=True)
print(f"mix: {len(ev)} sfx events -> {out}")
