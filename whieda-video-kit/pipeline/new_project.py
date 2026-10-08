#!/usr/bin/env python3
"""Create projects/<name>/ and fetch the source video.

Usage:
  python3 pipeline/new_project.py <name> <google-drive-link-or-local-file>

Drive links: file links (…/file/d/<ID>/…) and "open?id=<ID>" both work; the
file must be shared "Anyone with the link". Result: projects/<name>/source/<file>
and a starter project.json (copy of examples/project.example.json).
"""
import re, shutil, subprocess, sys, json
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
if len(sys.argv) != 3:
    raise SystemExit(__doc__)
name, src = sys.argv[1], sys.argv[2]
P = KIT / "projects" / name
(P / "source").mkdir(parents=True, exist_ok=True)
for d in ("work", "out"):
    (P / d).mkdir(exist_ok=True)

if Path(src).exists():
    shutil.copy(src, P / "source" / Path(src).name)
else:
    m = re.search(r"/d/([\w-]{20,})", src) or re.search(r"[?&]id=([\w-]{20,})", src)
    if "/folders/" in src:
        subprocess.run([sys.executable, "-m", "gdown", "--folder", src, "-O", str(P / "source")], check=True)
    elif m:
        subprocess.run([sys.executable, "-m", "gdown", m.group(1), "-O", str(P / "source") + "/"], check=True)
    else:
        raise SystemExit("Не понял ссылку. Нужна ссылка Google Drive на файл (…/file/d/<ID>/…) или папку.")

pj = P / "project.json"
if not pj.exists():
    tpl = json.loads((KIT / "examples" / "project.example.json").read_text())
    tpl["name"] = name
    pj.write_text(json.dumps(tpl, ensure_ascii=False, indent=2))
print("source:", *sorted(p.name for p in (P / "source").iterdir()))
print("next: python3 pipeline/prepare.py", name)
