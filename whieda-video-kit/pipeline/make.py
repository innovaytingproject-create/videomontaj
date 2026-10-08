#!/usr/bin/env python3
"""Build -> lint -> render -> mix in one go.

Usage: python3 pipeline/make.py <name> [--sample] [--draft]
  --sample  first 15 s only (always show this to the client first)
  --draft   fast low-quality render for your own checks
Result: projects/<name>/out/<name>.mp4 (or <name>-15s.mp4)
"""
import argparse, subprocess, sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
HF = "hyperframes@0.8.137"
ap = argparse.ArgumentParser()
ap.add_argument("name")
ap.add_argument("--sample", action="store_true")
ap.add_argument("--draft", action="store_true")
a = ap.parse_args()
P = KIT / "projects" / a.name
py = sys.executable
subprocess.run([py, str(KIT / "pipeline" / "build.py"), a.name] + (["--until", "15"] if a.sample else []), check=True)
subprocess.run(["npx", "--yes", HF, "check"], cwd=P, check=True)
subprocess.run(["npx", "--yes", HF, "render", "--quality", "draft" if a.draft else "looks", "--output", "out/pic.mp4"], cwd=P, check=True)
subprocess.run([py, str(KIT / "pipeline" / "mix.py"), a.name] + (["--sample"] if a.sample else []), check=True)
