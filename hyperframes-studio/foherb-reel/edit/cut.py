#!/usr/bin/env python3
"""Render the cut: 1080x1920 picture with block-alternating framing + cleaned, click-free voice."""
import json, subprocess
from pathlib import Path

MEDIA = Path(__file__).resolve().parents[3] / "media"
OUT = Path(__file__).resolve().parents[1] / "assets"
OUT.mkdir(exist_ok=True)
pieces = json.load(open("pieces.json"))

FADE = 0.025  # per-splice audio fade, kills clicks without audible dips
blocks = list(dict.fromkeys(p["block"] for p in pieces))

args, chains = ["ffmpeg", "-v", "error", "-y"], []
for i, p in enumerate(pieces):
    args += ["-ss", f"{p['src_in']:.3f}", "-t", f"{p['src_out'] - p['src_in']:.3f}", "-i", str(MEDIA / "source.mp4")]
    nf = round((p["src_out"] - p["src_in"]) * 30)  # exact frame count; seeking can add a stray frame
    d = nf / 30
    # Alternate framing per block so jump cuts between blocks read as deliberate punch-ins.
    zoom = 1.12 if blocks.index(p["block"]) % 2 else 1.0
    crop = f"crop=iw/{zoom}:ih/{zoom}:(iw-iw/{zoom})/2:(ih-ih/{zoom})*0.32," if zoom != 1.0 else ""
    chains.append(f"[{i}:v]{crop}scale=1080:1920:flags=lanczos,setsar=1,fps=30,eq=contrast=1.04:saturation=1.08,trim=end_frame={nf},setpts=PTS-STARTPTS[v{i}]")
    # Fade only at real splices; contiguous blocks join seamlessly.
    prev_join = i > 0 and abs(pieces[i - 1]["src_out"] - p["src_in"]) < 1e-3
    next_join = i + 1 < len(pieces) and abs(pieces[i + 1]["src_in"] - p["src_out"]) < 1e-3
    fades = ("" if prev_join else f",afade=t=in:d={FADE}") + ("" if next_join else f",afade=t=out:st={d - FADE:.3f}:d={FADE}")
    chains.append(f"[{i}:a]aresample=48000,pan=mono|c0=0.5*c0+0.5*c1,atrim=duration={d:.4f},asetpts=PTS-STARTPTS{fades}[a{i}]")
n = len(pieces)
chains.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][araw]")
# Voice cleanup: rumble cut, gentle denoise, presence, leveling, then loudness to -16 LUFS.
chains.append("[araw]highpass=f=90,afftdn=nf=-25,equalizer=f=3000:t=q:w=1.2:g=2.5,"
              "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,"
              "loudnorm=I=-16:TP=-1.5:LRA=9[a]")
args += ["-filter_complex", ";".join(chains), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(OUT / "cut.mp4")]
subprocess.run(args, check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(OUT / "cut.mp4"), "-vn", "-c:a", "pcm_s16le",
                str(OUT / "voice.wav")], check=True)
print("ok")
