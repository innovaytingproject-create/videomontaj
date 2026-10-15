#!/usr/bin/env python3
"""Generates video12.json — "Ishonchlar haqida" (Feruza's blog), Remotion version.
Times are in the cut reel (prepare_reel.py pieces, one "eh" cut at source 20.02-20.48);
text proofread from archive/video12 + whisper on public/video12/voice.wav.
Run: python src/edits/video12.py
"""
import json
from pathlib import Path

C = [
    (0.04, 0.90, [("Bugun", 0.04), ("men", 0.24), ("siz", 0.40), ("bilan", 0.64)]),
    (0.94, 2.30, [("*ishonchlar*", 0.94), ("haqida,", 1.70)]),
    (2.34, 4.20, [("ya’ni", 2.34), ("*e’tiqodlar*", 2.46), ("haqida", 3.08), ("gaplashmoqchiman.", 3.40)]),
    (6.78, 8.98, [("Ular", 6.78), ("bizni", 7.02), ("yoki", 7.32), ("*qo’llab-quvvatlaydi*,", 7.76)]),
    (9.04, 10.44, [("xohlagan", 9.04), ("*manzilimizga*,", 9.76)]),
    (10.48, 11.80, [("xohlagan", 10.48), ("*orzularimizga*,", 10.98)]),
    (11.84, 13.10, [("*maqsadlarimizga*", 11.84), ("olib", 12.66), ("boradi,", 12.90)]),
    (13.14, 14.70, [("yoki", 13.14), ("aksincha —", 13.48), ("yo’limizdagi", 14.04)]),
    (14.74, 16.38, [("*to’siq*", 14.74), ("va", 15.24), ("*blokka*", 15.38), ("aylanib", 15.88), ("qoladi.", 16.18)]),
    (16.42, 17.26, [("Bu", 16.42), ("juda", 16.52), ("*muhim*:", 16.76)]),
    (17.30, 19.02, [("agar", 17.30), ("bizning", 17.62), ("ong", 18.08), ("ostimizdagi", 18.30)]),
    (19.08, 20.00, [("o’sha", 19.08), ("ong", 19.64), ("ostimiz,", 19.80)]),
    (20.04, 20.94, [("agar", 20.04), ("*bog’*", 20.34), ("bo’lsa,", 20.58)]),
    (20.98, 22.76, [("o’shandagi", 20.98), ("*urug’lar*", 21.48), ("salbiy", 21.94), ("bo’lsa,", 22.42)]),
    (22.80, 24.80, [("hayotda", 22.80), ("qanchalik", 23.30), ("harakat", 23.82), ("qilmaylik,", 24.28)]),
    (24.84, 26.16, [("qanchalik", 24.84), ("*yugurmaylik*,", 25.46)]),
    (26.20, 28.64, [("baribir", 26.20), ("uning", 27.22), ("natijasi", 27.46), ("*salbiy*", 27.82), ("bo’ladi.", 28.20)]),
    (28.68, 30.80, [("Siz", 28.68), ("o’sha", 28.88), ("maqsadga", 29.20), ("*erisha*", 29.68), ("*olmaysiz*.", 30.08)]),
    (30.84, 32.36, [("Yoki", 30.84), ("agar", 31.28), ("*ijobiy*", 31.60), ("bo’lsa,", 32.02)]),
    (32.40, 33.72, [("unda", 32.40), ("albatta", 32.60), ("*natija*", 33.02), ("bo’ladi.", 33.50)]),
    (39.74, 41.26, [("Lekin", 39.74), ("buning", 40.08), ("uchun", 40.80), ("ular", 41.10)]),
    (41.30, 43.48, [("«ko’proq", 41.30), ("*ishlashim*", 42.34), ("kerak»", 42.74), ("deyishadi.", 43.08)]),
    (43.52, 44.66, [("Lekin", 43.52), ("aslida", 43.62), ("gap", 44.04)]),
    (44.70, 46.00, [("o’sha", 44.70), ("ko’p", 44.96), ("*ishlashda*", 45.22), ("emas,", 45.60)]),
    (46.04, 48.02, [("gap", 46.04), ("o’sha", 46.32), ("*yugurishda*", 46.64), ("emas", 47.18), ("ekan,", 47.64)]),
    (48.06, 49.28, [("gap", 48.06), ("o’sha", 48.44), ("aslida", 48.76)]),
    (49.32, 51.48, [("o’sha", 49.32), ("*ildizga*", 49.66), ("qarashda", 50.30), ("ekan.", 51.18)]),
    (54.50, 55.76, [("Agar", 54.50), ("biz", 54.84), ("o’sha", 54.96), ("*ildizni*", 55.36)]),
    (55.80, 56.60, [("o’zgartirmasak,", 55.80)]),
    (56.64, 59.12, [("unda", 56.64), ("biz", 56.88), ("*yugurib-yugurib*", 57.10)]),
    (59.16, 60.10, [("*charchab*", 59.16), ("qolamiz.", 59.56)]),
    (60.14, 62.20, [("Oqibati —", 60.14), ("yana", 60.82), ("o’sha", 61.12), ("*qarz*,", 61.40)]),
    (62.24, 63.66, [("yana", 62.24), ("o’sha", 62.42), ("*kredit*.", 62.62)]),
    (63.70, 65.88, [("Shuning", 63.70), ("uchun", 63.95), ("*ildiz*", 64.22), ("qayerda", 65.00), ("deysizmi?", 65.40)]),
    (65.92, 67.18, [("Ildiz —", 65.92), ("bu", 66.30), ("bizning", 66.36), ("*fikrimiz*,", 66.62)]),
    (67.22, 68.86, [("ildiz —", 67.22), ("bu", 67.56), ("*ong*", 67.74), ("*ostimiz*,", 68.00)]),
    (72.30, 74.40, [("bo’lgan", 72.30), ("sizning", 72.66), ("*munosabatingiz*", 73.02), ("ekan.", 73.78)]),
]


def words(ws):
    return [{"t": t, "text": txt.replace("*", ""), **({"hot": True} if "*" in txt else {})} for txt, t in ws]


edit = {
    "name": "video12", "duration": 76.9, "accent": "#FFD60A", "captionBottom": 520,
    "framing": {"originX": 540, "originY": 720, "scale": 1.35, "shiftY": -110},
    "cuts": [{"t": 6.78, "type": "whip"}, {"t": 13.14, "type": "zoomblur"}, {"t": 16.42, "type": "spin"},
             {"t": 28.68, "type": "punch"}, {"t": 39.74, "type": "whip"}, {"t": 44.70, "type": "spin"},
             {"t": 46.04, "type": "punch"}, {"t": 54.50, "type": "zoomblur"}, {"t": 63.70, "type": "whip"},
             {"t": 72.30, "type": "spin"}],
    "punches": [0.94, 14.74, 16.76, 20.34, 29.68, 33.02, 42.34, 55.36, 66.62],
    "captions": [{"start": a, "end": b, "words": words(w)} for a, b, w in C],
    "brolls": [
        {"file": "01_pexels_woman-walking-road_1080p_25fps.mp4", "start": 9.00, "end": 12.96, "from": 1.0, "enter": "whip"},
        {"file": "02_pexels_pea-shoots_1440p_30fps.mp4", "start": 20.98, "end": 22.78, "from": 2.0, "enter": "zoomblur"},
        {"file": "03_pexels_jogger-silhouette-sunset_1080p_25fps.mp4", "start": 22.78, "end": 26.18, "from": 3.0, "enter": "whip"},
        {"file": "05_pexels_mossy-tree-roots_1440p_60fps.mp4", "start": 49.30, "end": 51.52, "from": 2.0, "enter": "zoomblur"},
        {"file": "04_pexels_woman-phone-bills_1080p_25fps.mp4", "start": 60.12, "end": 63.68, "from": 2.0, "enter": "spin"},
    ],
    "cards": [
        {"start": 4.22, "end": 6.76, "thin": "Ishonchlar —", "big": "*Ijobiy*|yoki salbiy", "theme": "white",
         "icon": "i7559", "enter": "circle", "exit": "slide"},
        {"start": 33.74, "end": 39.72, "thin": "Ko’p odamlar", "big": "*Qarz* va|kreditda", "theme": "black",
         "icon": "i7564", "enter": "wipe", "exit": "zoom"},
        {"start": 51.52, "end": 54.48, "thin": "Ildizimiz —", "big": "*Ishonchimiz*|e’tiqodimiz", "theme": "white",
         "enter": "circle", "exit": "slide"},
        {"start": 68.88, "end": 72.28, "thin": "Ildiz — bu", "big": "*Pulga*,|muvaffaqiyatga|munosabat", "theme": "black",
         "enter": "wipe", "exit": "zoom"},
    ],
    "pills": [
        {"start": 0.04, "end": 4.20, "text": "Ishonchlar haqida", "icon": "i7557"},
        {"start": 16.42, "end": 17.26, "text": "Juda muhim!", "icon": "i7578"},
        {"start": 44.70, "end": 46.00, "text": "Ko’p ishlash emas", "icon": "i7559"},
        {"start": 46.04, "end": 48.02, "text": "Yugurish emas", "icon": "i7559"},
        {"start": 54.50, "end": 56.60, "text": "Ildizni o’zgartiring", "icon": "i7565"},
        {"start": 65.92, "end": 67.18, "text": "Fikrimiz", "icon": "i7556"},
        {"start": 67.22, "end": 68.86, "text": "Ong ostimiz", "icon": "i7557"},
    ],
    "badges": [
        {"start": 6.78, "end": 8.98, "icon": "i7563", "label": "Tayanch", "theme": "black", "x": 160, "y": 580, "size": 230, "rot": 5},
        {"start": 19.08, "end": 20.94, "icon": "i7557", "label": "Ong osti", "theme": "white", "x": 155, "y": 580, "size": 220, "rot": -6},
        {"start": 26.20, "end": 28.64, "icon": "i7559", "label": "Natija", "theme": "black", "x": 155, "y": 580, "size": 220, "rot": 6},
        {"start": 30.84, "end": 33.72, "icon": "i7571", "label": "Ijobiy", "theme": "white", "x": 155, "y": 580, "size": 220, "rot": -5},
        {"start": 41.30, "end": 43.48, "icon": "i7581", "label": "Ko’p ish", "theme": "black", "x": 160, "y": 590, "size": 230, "rot": 5},
        {"start": 56.64, "end": 60.08, "icon": "i7564", "label": "Charchoq", "theme": "white", "x": 155, "y": 590, "size": 220, "rot": -6},
        {"start": 72.30, "end": 74.40, "icon": "i7566", "label": "Munosabat", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 6},
    ],
    "stickers": [
        {"file": "s4055", "start": 13.14, "end": 16.38, "x": 880, "y": 560, "w": 220, "rot": 8},
        {"file": "s4043", "start": 17.30, "end": 19.02, "x": 880, "y": 560, "w": 200, "rot": 10},
        {"file": "s4051", "start": 30.84, "end": 32.36, "x": 885, "y": 570, "w": 220, "rot": 8},
        {"file": "s4041", "start": 39.74, "end": 41.26, "x": 875, "y": 580, "w": 230, "rot": -8},
        {"file": "s3898", "start": 63.70, "end": 65.88, "x": 880, "y": 580, "w": 220, "rot": 6},
        {"file": "s3935", "start": 72.30, "end": 74.40, "x": 870, "y": 600, "w": 270, "rot": -6},
    ],
    "endCard": {"start": 74.44, "title": "Feruza *Sabitova*", "sub": "@sabitova_akademiyasi", "cta": "Obuna bo’ling"},
    "music": "driving-ambition", "musicDb": -20, "musicFrom": 0.5,
}
joins = [1.12, 4.94, 6.82, 12.0, 16.44, 17.34, 22.98, 26.22, 30.88, 33.82, 34.9, 36.72, 44.2, 46.8, 49.0, 50.46,
         54.56, 56.72, 58.4, 60.04, 61.58, 64.34, 65.98, 67.28, 69.96]
cover = [(x["start"] - 0.05, x["end"] + 0.05) for x in edit["cards"] + edit["brolls"]]
jumps = [j for j in joins if not any(a <= j <= b for a, b in cover)
         and not any(abs(j - c["t"]) < 0.3 for c in edit["cuts"])]
thin = []
for j in jumps:  # two jump cuts closer than 0.6 s would flicker the framing
    if not thin or j - thin[-1] >= 0.6:
        thin.append(j)
edit["jumps"] = thin
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(edit, ensure_ascii=False, indent=1), encoding="utf-8")
print("written", out.name, "jumps", edit["jumps"])
