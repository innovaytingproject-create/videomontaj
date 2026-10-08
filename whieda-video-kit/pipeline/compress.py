#!/usr/bin/env python3
"""Two-pass compress to fit a size limit (Telegram/chat). Default 28 MB.

Usage: python3 pipeline/compress.py <file.mp4> [MB]
Writes <file>-small.mp4. Keep the full-quality file for Instagram upload.
"""
import subprocess, sys, tempfile
from pathlib import Path

src = Path(sys.argv[1]); mb = float(sys.argv[2]) if len(sys.argv) > 2 else 28
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                           capture_output=True, text=True, check=True).stdout)
vk = int(mb * 8192 / dur - 160)  # kbit/s for video, 128k audio + container slack
out = src.with_name(src.stem + "-small.mp4")
with tempfile.TemporaryDirectory() as d:
    base = ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-c:v", "libx264", "-preset", "slow", "-b:v", f"{vk}k",
            "-pix_fmt", "yuv420p", "-passlogfile", f"{d}/p"]
    subprocess.run(base + ["-pass", "1", "-an", "-f", "mp4", "/dev/null"], check=True)
    subprocess.run(base + ["-pass", "2", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out)], check=True)
print(f"{out}  {out.stat().st_size / 1e6:.1f} MB  (video {vk} kbit/s)")
