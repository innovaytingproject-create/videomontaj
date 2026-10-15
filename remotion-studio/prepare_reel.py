#!/usr/bin/env python3
"""Cut a fragment of a kit project for the Remotion reel and sync kit assets.

Usage: python prepare_reel.py <kit-project> <start:end> [<start:end> ...]
  pieces (seconds of work/video.mp4) are joined in order — pauses cut out;
  put the reel's camera cuts on the joins to hide them.

Takes whieda-video-kit/projects/<name>/work/video.mp4 + voice.wav (made by the
kit's prepare.py: graded picture, cleaned voice) and writes
public/<name>/clip.mp4 + voice.wav; copies fonts, icons, stickers, sfx, music
into public/assets/. public/ is not in git — rerun this script on a new computer.
Then write src/edits/<name>.json and render:  npx remotion render <Id> out/<name>.mp4
"""
import shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KIT = ROOT.parent / "whieda-video-kit"
name = sys.argv[1]
pieces = [tuple(map(float, a.split(":"))) for a in sys.argv[2:]]
W = KIT / "projects" / name / "work"
OUT = ROOT / "public" / name
OUT.mkdir(parents=True, exist_ok=True)

n = len(pieces)
trim_v = ";".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]" for i, (a, b) in enumerate(pieces))
trim_a = ";".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b - a - 0.03:.3f}:d=0.03[a{i}]"
                  for i, (a, b) in enumerate(pieces))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "video.mp4"), "-filter_complex",
                trim_v + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]", "-map", "[v]",
                "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", str(OUT / "clip.mp4")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "voice.wav"), "-filter_complex",
                trim_a + ";" + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a]", "-map", "[a]",
                "-ar", "48000", str(OUT / "voice.wav")], check=True)
joins, acc = [], 0.0
for a, b in pieces[:-1]:
    acc += b - a
    joins.append(round(acc, 2))
print("total:", round(sum(b - a for a, b in pieces), 2), "s; joins at", joins)

A = ROOT / "public" / "assets"
if not (KIT / "assets" / "sfx" / "boom.wav").exists():  # *.wav is not in git
    subprocess.run([sys.executable, str(KIT / "pipeline" / "gen_sfx.py")], check=True)
for src, dst in (("assets/fonts", "fonts"), ("assets/icons", "icons"), ("assets/stickers_all", "stickers"),
                 ("assets/sfx", "sfx"), ("assets/music", "music")):
    shutil.copytree(KIT / src, A / dst, dirs_exist_ok=True)
print("ok:", OUT / "clip.mp4", "+ voice.wav; assets ->", A)
