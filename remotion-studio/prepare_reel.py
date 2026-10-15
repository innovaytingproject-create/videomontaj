#!/usr/bin/env python3
"""Cut a fragment of a kit project for the Remotion reel and sync kit assets.

Usage: python prepare_reel.py <kit-project> [--grade cinema] [--as <reel>] <start:end> [<start:end> ...]
  --as <reel>      write to public/<reel>/ instead of public/<kit-project>/ (several
                   reels from one source, e.g. video16 = 15 s, video16-full = full)
  pieces (seconds of work/video.mp4) are joined in order — pauses cut out;
  put the reel's camera cuts on the joins to hide them.
  --grade kit      (default) the kit's approved bright, saturated "WHIEDA" look
  --grade neutral  re-grade from the source: cooler, natural skin, no brown/orange
                   cast (use when warm wood/skin makes the kit look too brown)
  --grade cinema   soft filmic look: bright, face not over-bright, light vignette and grain

Takes whieda-video-kit/projects/<name>/work/video.mp4 + voice.wav (made by the
kit's prepare.py: graded picture, cleaned voice) and writes
public/<name>/clip.mp4 + voice.wav; copies fonts, icons, stickers, sfx, music
into public/assets/. Stock footage from projects/<name>/footage/**/*.mp4 (see the
footage instruction + credits.md there) -> public/<name>/broll/<file>.mp4, 1080x1920 30 fps.
public/ is not in git — rerun this script on a new computer.
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
reel = None
if "--as" in args:
    i = args.index("--as")
    reel = args[i + 1]
    del args[i:i + 2]
name = args[0]
pieces = [tuple(map(float, a.split(":"))) for a in args[1:]]
W = KIT / "projects" / name / "work"

# Same timeline as work/video.mp4: prepare.py never cuts. joined.mov exists for multi-part projects.
GRADES = {
    "kit": None,
    # soft filmic: highlights rolled off (face not over-bright) but still bright overall,
    # natural skin (no brown/orange, no teal), very light vignette and grain
    "cinema": ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,"
               "hqdn3d=1.5:1.5:4:4,colorbalance=rs=-0.02:bs=0.03:rm=-0.04:bm=0.02:rh=-0.01:bh=0.01,"
               "huesaturation=saturation=-0.18:colors=r+y,eq=brightness=0.025:contrast=1.06:saturation=1.0:gamma=1.04,"
               "curves=master='0/0.03 0.25/0.25 0.5/0.53 0.75/0.79 1/0.95',vignette=PI/6,"
               "unsharp=5:5:0.5:5:5:0,noise=alls=3:allf=t"),
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
OUT = ROOT / "public" / (reel or name)
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
                trim_a + ";" + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,"
                # even out the voice so quiet phrases are not lost under music and SFX
                "acompressor=threshold=-26dB:ratio=4:attack=5:release=160:makeup=6,"
                "dynaudnorm=f=250:g=13:p=0.9:m=8,loudnorm=I=-14:TP=-1.5:LRA=5[a]", "-map", "[a]",
                "-ar", "48000", str(OUT / "voice.wav")], check=True)
joins, acc = [], 0.0
for a, b in pieces[:-1]:
    acc += b - a
    joins.append(round(acc, 2))
print("total:", round(sum(b - a for a, b in pieces), 2), "s; joins at", joins)

# Stock footage (B-roll): conform to the reel format; the edit picks the part (brolls[].from).
for f in sorted((W.parent / "footage").glob("**/*.mp4")):
    (OUT / "broll").mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf",
                    "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,"
                    "eq=brightness=0.03:contrast=1.04:saturation=1.02:gamma=1.04,unsharp=5:5:0.4:5:5:0",
                    "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(OUT / "broll" / f.name)], check=True)
    print("broll:", f.name)

A = ROOT / "public" / "assets"
if not (KIT / "assets" / "sfx" / "boom.wav").exists():  # *.wav is not in git
    subprocess.run([sys.executable, str(KIT / "pipeline" / "gen_sfx.py")], check=True)
for src, dst in (("assets/fonts", "fonts"), ("assets/icons", "icons"), ("assets/stickers_all", "stickers"),
                 ("assets/sfx", "sfx"), ("assets/music", "music")):
    shutil.copytree(KIT / src, A / dst, dirs_exist_ok=True)
# The kit icons carry a faint square glow (alpha ~5-30) that shows as a box on
# plain card/badge backgrounds: drop it in the copies (kit originals untouched).
from PIL import Image
for f in (A / "icons").glob("i*-*.png"):
    im = Image.open(f).convert("RGBA")
    a = im.getchannel("A").point(lambda v: 0 if v < 70 else min(255, int((v - 70) * 255 / 185)))
    im.putalpha(a)
    im.save(f)
print("ok:", OUT / "clip.mp4", "+ voice.wav; assets ->", A)
