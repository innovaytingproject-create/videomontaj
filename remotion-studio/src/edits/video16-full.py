#!/usr/bin/env python3
"""Generates video16-full.json (full "Pro maqsad" reel). Times are in the cut reel
(pieces from find_pieces.py, words re-transcribed on public/video16-full/voice.wav).
Run: python src/edits/video16-full.py
"""
import json
from pathlib import Path

C = [
    (0.04, 1.20, [("Men", 0.06), ("*Feruza*", 0.28), ("Sabitovaman,", 0.64)]),
    (1.24, 2.52, [("qariyb", 1.30), ("*30*", 1.58), ("*yildan*", 1.84), ("beri", 2.32)]),
    (2.58, 3.68, [("kino", 2.58), ("sohasida", 2.84), ("*aktrisa*", 3.32)]),
    (3.72, 4.84, [("bo’lib", 3.72), ("ishlab", 4.04), ("kelyapman.", 4.34)]),
    (4.90, 6.40, [("*Yuzdan*", 4.90), ("*ortiq*", 5.54), ("filmlarda", 6.02)]),
    (6.46, 7.66, [("rol", 6.46), ("ijro", 6.80), ("etganman.", 7.00)]),
    (7.72, 8.88, [("Va", 7.72), ("so’nggi", 7.92), ("yillarda", 8.56)]),
    (8.94, 10.56, [("men", 8.94), ("o’z", 9.68), ("ustimda", 10.12)]),
    (10.62, 11.90, [("*chuqur*", 10.62), ("ishlab", 11.00), ("kelyapman.", 11.34)]),
    (11.96, 13.48, [("Va", 11.96), ("bir", 12.24), ("narsani", 12.80), ("*angladim*:", 12.96)]),
    (13.54, 14.74, [("men", 13.54), ("o’z", 13.86), ("*qadrimni*,", 14.08)]),
    (14.80, 16.24, [("*ichki*", 14.80), ("*kuchimni*", 15.64)]),
    (16.30, 17.70, [("va", 16.30), ("o’zimda", 16.62), ("*ayollik*", 17.20)]),
    (17.76, 19.30, [("*energiyasini*", 17.76), ("ochishni", 18.42), ("boshladim.", 18.80)]),
    (19.36, 20.56, [("Va", 19.36), ("bir", 19.52), ("narsani", 19.84), ("angladim:", 20.02)]),
    (20.62, 21.28, [("bu", 20.62), ("narsa —", 20.90)]),
    (21.32, 22.84, [("har", 21.32), ("bir", 22.32), ("*ayol*", 22.44)]),
    (22.90, 24.42, [("o’zini", 22.90), ("*namoyon*", 23.24), ("qilishi", 23.70), ("kerak.", 24.14)]),
    (24.48, 25.92, [("O’zining", 24.48), ("*qadrini*", 24.80), ("bilish,", 25.36)]),
    (25.98, 27.56, [("o’zining", 25.98), ("*ichki*", 26.26), ("*kuchini*", 26.58), ("topish,", 26.90)]),
    (27.62, 29.24, [("o’ziga", 27.62), ("*ishonch*", 28.50)]),
    (29.30, 31.88, [("bilan", 29.30), ("gapira", 31.10), ("olish.", 31.42)]),
    (31.94, 33.56, [("Ya’ni,", 31.94), ("*katta*", 32.28)]),
    (33.62, 34.32, [("*daromad*", 33.62), ("topish", 33.94)]),
    (34.38, 35.64, [("va", 34.38), ("*baxtli*", 34.58), ("yashash", 35.00), ("kerak.", 35.36)]),
    (35.70, 37.22, [("Shuning", 35.70), ("uchun,", 35.90), ("*go’zal*", 36.32), ("ayollar,", 36.70)]),
    (37.28, 38.48, [("*noyabr*", 37.28), ("oyida", 37.78), ("men", 38.06)]),
    (38.54, 39.74, [("birinchi", 38.54), ("marotaba", 39.34)]),
    (39.80, 41.48, [("«*Ayollik*", 39.80), ("namoyonligi»", 40.70)]),
    (41.54, 43.50, [("nomli", 41.54), ("*master-klass*", 41.98), ("o’tkazaman.", 42.96)]),
    (43.56, 44.90, [("*Barcha*", 43.56), ("*ayollarni*", 43.92), ("taklif", 44.36), ("qilaman.", 44.60)]),
    (44.96, 46.20, [("Tez", 44.96), ("orada", 45.10), ("*sanasi*,", 45.40), ("joyi", 45.70)]),
    (46.26, 47.60, [("va", 46.26), ("barcha", 46.52), ("ma’lumotlarini", 47.00)]),
    (47.66, 48.64, [("sizga", 47.66), ("*e’lon*", 47.92), ("qilaman.", 48.20)]),
    (48.70, 50.58, [("Agar", 48.70), ("sizga", 49.00), ("*ayollik*", 49.28), ("*xarizmasi*,", 50.08)]),
    (50.64, 52.10, [("*o’z*", 50.64), ("*qadri*", 50.90), ("va", 51.48), ("*liderlik*", 51.60)]),
    (52.16, 53.18, [("mavzulari", 52.16), ("qiziq", 52.52), ("bo’lsa,", 52.92)]),
    (53.24, 54.42, [("mening", 53.24), ("*Instagram*", 53.88)]),
    (54.48, 55.84, [("akkauntimga", 54.48), ("*obuna*", 55.00), ("*bo’ling!*", 55.30)]),
]


def words(ws):
    return [{"t": t, "text": txt.replace("*", ""), **({"hot": True} if "*" in txt else {})} for txt, t in ws]


edit = {
    "name": "video16-full", "duration": 58.3, "accent": "#FFD60A",
    "framing": {"originX": 540, "originY": 720, "scale": 1.35, "shiftY": -110},
    "cuts": [{"t": 7.72, "type": "whip"}, {"t": 11.96, "type": "zoomblur"}, {"t": 19.36, "type": "spin"},
             {"t": 25.98, "type": "punch"}, {"t": 35.70, "type": "whip"}, {"t": 46.26, "type": "spin"},
             {"t": 53.24, "type": "zoomblur"}],
    "punches": [1.58, 10.62, 14.08, 22.44, 26.26, 36.32, 45.40, 50.64],
    "captions": [{"start": a, "end": b, "words": words(w)} for a, b, w in C],
    "brolls": [
        {"file": "01_pexels_film-camera-monitor_1440p_50fps.mp4", "start": 2.58, "end": 4.86, "from": 6.6, "enter": "whip"},
        {"file": "02_pexels_woman-rocks-sunset_1080p_60fps.mp4", "start": 14.80, "end": 17.72, "from": 0.5, "enter": "zoomblur"},
        {"file": "03_pexels_woman-speaker-microphone_1440p_25fps.mp4", "start": 28.40, "end": 31.45, "from": 1.0, "enter": "whip"},
        {"file": "04_pexels_woman-money-fan_1440p_25fps.mp4", "start": 33.60, "end": 35.66, "from": 15.6, "enter": "spin"},
        {"file": "05_pexels_woman-clapping-event_1080p_24fps.mp4", "start": 41.50, "end": 44.92, "from": 1.2, "enter": "zoomblur"},
    ],
    "cards": [
        {"start": 4.88, "end": 6.44, "thin": "Yuzdan ortiq", "big": "*100+*|film", "theme": "white", "icon": "i7555",
         "numeric": True, "enter": "circle", "exit": "slide"},
        {"start": 22.88, "end": 24.46, "thin": "Har bir ayol o’zini", "big": "*namoyon*|qilishi kerak", "theme": "black",
         "icon": "i7571", "enter": "wipe", "exit": "zoom"},
        {"start": 37.28, "end": 41.50, "thin": "Noyabr · birinchi marotaba", "big": "«Ayollik|*namoyonligi*»|master-klass",
         "theme": "white", "icon": "i7556", "enter": "circle", "exit": "slide"},
        {"start": 48.70, "end": 52.12, "thin": "Sizga qiziqmi?", "big": "Xarizma|O’z qadri|*Liderlik*", "theme": "black",
         "enter": "wipe", "exit": "zoom"},
    ],
    "pills": [
        {"start": 8.94, "end": 11.90, "text": "O’z ustida ishlash", "icon": "i7565"},
        {"start": 17.76, "end": 19.30, "text": "Ayollik energiyasi", "icon": "i7561"},
        {"start": 24.48, "end": 25.94, "text": "O’z qadrini bilish"},
        {"start": 25.98, "end": 27.58, "text": "Ichki kuchini topish"},
        {"start": 44.96, "end": 46.22, "text": "Tez orada e’lon", "icon": "i7569"},
        {"start": 53.24, "end": 55.84, "text": "@sabitova_akademiyasi", "icon": "i7582"},
    ],
    "badges": [
        {"start": 1.26, "end": 2.56, "icon": "i7575", "label": "30 yil", "theme": "white", "x": 155, "y": 560, "size": 220, "rot": -6},
        {"start": 13.54, "end": 14.76, "icon": "i7566", "label": "O’z qadri", "theme": "black", "x": 155, "y": 580, "size": 220, "rot": 6},
        {"start": 19.36, "end": 20.58, "icon": "i7557", "label": "Angladim", "theme": "white", "x": 155, "y": 580, "size": 220, "rot": -5},
        {"start": 20.62, "end": 22.86, "icon": "i7562", "label": "Har bir ayol", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 5},
        {"start": 46.26, "end": 48.66, "icon": "i7556", "label": "Sana · joy", "theme": "white", "x": 155, "y": 580, "size": 220, "rot": -6},
        {"start": 54.48, "end": 55.84, "icon": "i7582", "label": "Obuna!", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 6},
    ],
    "stickers": [
        {"file": "s4098", "start": 6.50, "end": 7.66, "x": 870, "y": 540, "w": 260, "rot": 8},
        {"file": "s4043", "start": 11.96, "end": 13.48, "x": 880, "y": 560, "w": 200, "rot": 10},
        {"file": "s4051", "start": 13.54, "end": 14.76, "x": 885, "y": 570, "w": 220, "rot": 8},
        {"file": "s3900", "start": 17.76, "end": 19.30, "x": 890, "y": 610, "w": 230, "rot": 6},
        {"file": "s4040", "start": 25.98, "end": 27.58, "x": 880, "y": 600, "w": 240, "rot": 10},
        {"file": "s3935", "start": 32.28, "end": 33.56, "x": 870, "y": 600, "w": 270, "rot": -6},
        {"file": "s3901", "start": 35.72, "end": 37.24, "x": 885, "y": 610, "w": 220, "rot": 7},
        {"file": "s4046", "start": 46.26, "end": 48.66, "x": 870, "y": 580, "w": 260, "rot": -8},
        {"file": "s3885", "start": 53.24, "end": 55.84, "x": 880, "y": 600, "w": 200, "rot": 8},
    ],
    "endCard": {"start": 55.86, "title": "Feruza *Sabitova*", "sub": "@sabitova_akademiyasi", "cta": "Obuna bo’ling"},
    "music": "dreaming-big", "musicDb": -13, "musicFrom": 1.5,
}
joins = [1.38, 5.0, 7.8, 9.26, 12.48, 13.66, 14.94, 19.42, 21.48, 21.88, 24.56, 26.02, 31.98, 32.42, 35.78, 36.44,
         37.32, 38.82, 40.1, 43.56, 44.64, 44.96, 48.78, 49.56, 50.78]
cover = [(x["start"] - 0.05, x["end"] + 0.05) for x in edit["cards"] + edit["brolls"]]
edit["jumps"] = [j for j in joins if not any(a <= j <= b for a, b in cover)
                 and not any(abs(j - c["t"]) < 0.3 for c in edit["cuts"])]
# two jump cuts closer than 0.6 s would flicker the framing: keep the first
thin = []
for j in edit["jumps"]:
    if not thin or j - thin[-1] >= 0.6:
        thin.append(j)
edit["jumps"] = thin
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(edit, ensure_ascii=False, indent=1), encoding="utf-8")
print("written", out.name, "jumps", edit["jumps"])
