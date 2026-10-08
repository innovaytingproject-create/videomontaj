#!/usr/bin/env python3
"""Word-level transcription + draft captions.

Usage: python3 pipeline/transcribe.py <name> [--lang uz] [--model large-v3]

Speech in this client's videos is UZBEK (with Russian words mixed in).
Auto-detect fails on it -> always pass the language. large-v3 is noticeably
better than turbo on Uzbek; first run downloads ~3 GB from Hugging Face.

Writes work/words.json (every word with start/end), work/source.srt and
work/captions_draft.json — phrases of 2-6 words in project.json format.
The draft is RAW whisper text: you must proof-read it (spelling of Uzbek,
brand name WHIEDA — whisper writes "MEDA"/"VIDA"), add *accents* and paste
into project.json "captions".
"""
import argparse, json, subprocess
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

KIT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("name")
ap.add_argument("--lang", default="uz")
ap.add_argument("--model", default="large-v3")
a = ap.parse_args()
P = KIT / "projects" / a.name
src = P / "work" / "voice.wav"
if not src.exists():
    raise SystemExit("run pipeline/prepare.py first")

# decode with ffmpeg (PyAV inside faster-whisper crashes on some versions)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                     check=True, capture_output=True).stdout
audio = np.frombuffer(raw, np.float32)
model = WhisperModel(a.model, device="cpu", compute_type="int8")
segs, _ = model.transcribe(audio, language=a.lang, word_timestamps=True, vad_filter=True, beam_size=5)


def ts(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


words, srt = [], []
for i, s in enumerate(segs, 1):
    srt.append(f"{i}\n{ts(s.start)} --> {ts(s.end)}\n{s.text.strip()}\n")
    for w in s.words or []:
        words.append({"text": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)})
    print(f"{s.start:7.2f} {s.text.strip()}")

# draft phrases: break on punctuation, pauses > .35 s, or 6 words
caps, cur = [], []
for k, w in enumerate(words):
    cur.append(w)
    nxt = words[k + 1] if k + 1 < len(words) else None
    gap = (nxt["start"] - w["end"]) if nxt else 9
    if len(cur) >= 6 or gap > .35 or w["text"][-1:] in ".,!?:;" or (len(cur) >= 3 and sum(len(x["text"]) for x in cur) > 26):
        caps.append([round(cur[0]["start"], 2), round(min(w["end"] + .15, nxt["start"] - .05 if nxt else w["end"] + .3), 2),
                     " ".join(x["text"] for x in cur)])
        cur = []
(P / "work" / "words.json").write_text(json.dumps(words, ensure_ascii=False, indent=0))
(P / "work" / "source.srt").write_text("\n".join(srt))
(P / "work" / "captions_draft.json").write_text(json.dumps(caps, ensure_ascii=False, indent=1))
print(f"{len(words)} words, {len(caps)} draft captions -> work/captions_draft.json")
