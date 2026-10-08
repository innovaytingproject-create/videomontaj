#!/usr/bin/env python3
"""Checks the kit works on this computer: makes a 6-second synthetic clip,
runs prepare -> build -> check -> render (draft) -> mix, verifies the output.

Usage: python3 pipeline/selftest.py      (takes 1-3 minutes)
"""
import json, shutil, subprocess, sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
P = KIT / "projects" / "_selftest"
py = sys.executable
for tool in ("ffmpeg", "ffprobe", "npx", "node"):
    if not shutil.which(tool):
        raise SystemExit(f"НЕ НАЙДЕНО: {tool} — установи его (см. CLAUDE.md, раздел 0)")
shutil.rmtree(P, ignore_errors=True)
(P / "source").mkdir(parents=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=1080x1920:r=30:d=6",
                "-f", "lavfi", "-i", "sine=f=220:d=6", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                "-shortest", str(P / "source" / "test.mp4")], check=True)
cfg = json.loads((KIT / "examples" / "project.example.json").read_text())
cfg.update(name="_selftest", captions=[[0.1, 1.9, "Assalomu alaykum, *azizlar!*"], [4.1, 5.5, "Bu *test* video"]],
           logos=[[0.2, 1.9]], cards=[{"start": 2.0, "end": 4.0, "thin": "Test", "big": "*WHIEDA*|kit", "icon": "i7575"}])
(P / "project.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1))
subprocess.run([py, str(KIT / "pipeline" / "prepare.py"), "_selftest"], check=True)
subprocess.run([py, str(KIT / "pipeline" / "make.py"), "_selftest", "--draft"], check=True)
out = P / "out" / "_selftest.mp4"
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                         capture_output=True, text=True).stdout or 0)
try:
    import faster_whisper, gdown  # noqa: F401
    extra = "python-пакеты: ok"
except ImportError as e:
    extra = f"ВНИМАНИЕ: нет python-пакета ({e.name}) — pip install -r requirements.txt"
print(f"\nSELFTEST {'OK' if d > 7 else 'FAIL'}: {out} ({d:.1f} c). {extra}")
