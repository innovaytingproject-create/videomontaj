#!/usr/bin/env python3
"""Grade the footage + clean the voice (the client-approved settings).

Usage: python3 pipeline/prepare.py <name> [source-file]

Writes projects/<name>/work/video.mp4  (1080x1920, 30 fps, graded, no audio)
       projects/<name>/work/voice.wav  (denoised, compressed, -16 LUFS)
Nothing is cut: the source is used start-to-finish (client rule).
"""
import subprocess, sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
name = sys.argv[1]
P = KIT / "projects" / name
srcs = [Path(sys.argv[2])] if len(sys.argv) > 2 else sorted(p for p in (P / "source").iterdir() if p.suffix.lower() in (".mov", ".mp4", ".m4v", ".mkv"))
if not srcs:
    raise SystemExit("в source/ нет видео")
src = srcs[0]
(P / "work").mkdir(exist_ok=True)

# Approved "WHIEDA bright": denoise, brighter, saturated, light S-curve, sharpen.
GRADE = ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,"
         "hqdn3d=1.5:1.5:4:4,eq=brightness=0.045:contrast=1.08:saturation=1.32:gamma=1.04,"
         "colorbalance=rm=0.02:bm=-0.01:rh=0.01,curves=master='0/0.01 0.25/0.24 0.75/0.8 1/1',unsharp=5:5:0.7:5:5:0")
VOICE = ("highpass=f=90,afftdn=nf=-25,equalizer=f=3000:t=q:w=1.2:g=2.5,"
         "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,loudnorm=I=-16:TP=-1.5:LRA=9")

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", GRADE, "-an", "-c:v", "libx264",
                "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(P / "work" / "video.mp4")], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-af", VOICE, "-ar", "48000", "-ac", "2",
                str(P / "work" / "voice.wav")], check=True)
print("ok:", P / "work" / "video.mp4", "+ voice.wav")
print("next: python3 pipeline/transcribe.py", name)
