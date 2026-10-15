#!/usr/bin/env python3
"""Cut a fragment of a kit project for the Remotion reel and sync kit assets.

Usage: python prepare_reel.py <kit-project> [--grade neutral] <start:end> [<start:end> ...]
  pieces (seconds of work/video.mp4) are joined in order — pauses cut out;
  put the reel's camera cuts on the joins to hide them.
  --grade kit      (default) the kit's approved bright, saturated "WHIEDA" look
  --grade neutral  re-grade from the source: cooler, natural skin, no brown/orange
                   cast (use when warm wood/skin makes the kit look too brown)

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
args = sys.argv[1:]
grade = "kit"
if "--grade" in args:
    i = args.index("--grade")
    grade = args[i + 1]
    del args[i:i + 2]
name = args[0]
pieces = [tuple(map(float, a.split(":"))) for a in args[1:]]
W = KIT / "projects" / name / "work"

# Same timeline as work/video.mp4: prepare.py never cuts. joined.mov exists for multi-part projects.
GRADES = {
    "kit": None,
    "neutral": ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,"
                "hqdn3d=1.5:1.5:4:4,colorbalance=rm=-0.05:bm=0.04:rh=-0.03:bh=0.03,huesaturation=saturation=-0.22:colors=r+y,"
                "eq=brightness=0.06:contrast=1.07:saturation=1.08:gamma=1.06,unsharp=5:5:0.6:5:5:0"),
}
if grade not in GRADES:
    raise SystemExit(f"unknown --grade {grade}; one of {list(GRADES)}")
if GRADES[grade]:
    src = W / "joined.mov"
    if not src.exists():
        src = sorted(p for p in (W.parent / "source").iterdir() if p.suffix.lower() in (".mov", ".mp4", ".m4v", ".mkv"))[0]
    pre = GRADES[grade] + ","
else:
    src, pre = W / "video.mp4", ""
OUT = ROOT / "public" / name
OUT.mkdir(parents=True, exist_ok=True)

n = len(pieces)
trim_v = f"[0:v]{pre}split={n}" + "".join(f"[s{i}]" for i in range(n)) + ";" + ";".join(
    f"[s{i}]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]" for i, (a, b) in enumerate(pieces))
trim_a = ";".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b - a - 0.03:.3f}:d=0.03[a{i}]"
                  for i, (a, b) in enumerate(pieces))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-filter_complex",
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
