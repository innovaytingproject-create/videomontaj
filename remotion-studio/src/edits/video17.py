#!/usr/bin/env python3
"""Generates video17.json — "Orzu, maqsad va niyat" (Feruza's blog, parts 3.1 + 3.2).
Times are in the cut reel (prepare_reel.py pieces), words re-transcribed on
public/video17/voice.wav and proofread (Russian word "upakovka" kept in Latin).
Run: python src/edits/video17.py
"""
import json
from pathlib import Path

C = [
    (0.04, 1.70, [("Bugun", 0.04), ("men", 0.26), ("*orzu*,", 0.42)]),
    (4.64, 5.66, [("Ya’ni,", 4.64), ("eng", 4.90), ("birinchi", 5.06), ("o’rinda", 5.36)]),
    (5.68, 6.70, [("bu", 5.68), ("*niyat*", 5.90), ("turadi.", 6.34)]),
    (6.74, 8.08, [("Ya’ni,", 6.74), ("aytadilar:", 7.00)]),
    (8.12, 9.48, [("«*niyating*", 8.12), ("xolis", 8.58), ("bo’lsin».", 8.92)]),
    (9.52, 11.10, [("Ya’ni,", 9.52), ("qaysi", 9.76), ("*niyat*", 10.68), ("bilan", 10.98)]),
    (11.14, 13.16, [("siz", 11.14), ("boshlayapsiz,", 11.28), ("nima", 12.02), ("turibdi,", 12.40)]),
    (13.20, 14.46, [("mana", 13.20), ("bir", 13.40), ("*maqsad*", 13.58), ("qo’yasiz.", 14.02)]),
    (14.50, 16.40, [("Aslida", 14.50), ("*maqsad*", 14.82), ("— bu", 16.04)]),
    (24.04, 25.56, [("Endi", 24.04), ("qarang,", 24.26), ("ko’p", 24.58), ("odamlarda", 25.00)]),
    (25.60, 26.28, [("*orzu*", 25.60), ("bor,", 26.06)]),
    (26.32, 27.36, [("lekin", 26.32), ("odamlardan", 26.48), ("so’rasangiz,", 26.96)]),
    (27.40, 28.72, [("orzu,", 27.40), ("orzuyingiz", 28.00), ("uchun", 28.54)]),
    (28.76, 29.80, [("siz", 28.76), ("*nima*", 28.92), ("qilyapsiz,", 29.18)]),
    (29.84, 31.46, [("*harakat*", 29.84), ("qilyapsizmi,", 30.12), ("desak,", 30.92)]),
    (31.50, 32.36, [("o’zgaryapsizmi,", 31.50)]),
    (37.14, 38.30, [("Qachonki", 37.14), ("siz", 37.78), ("*haqiqiy*", 37.92)]),
    (38.34, 39.32, [("orzuyingizni", 38.34), ("topsangiz,", 38.90)]),
    (43.32, 44.94, [("keyin", 43.32), ("*rejalarini*", 43.66), ("qilib,", 44.68)]),
    (44.98, 46.06, [("va", 44.98), ("*harakatini*", 45.06), ("qilasiz.", 45.60)]),
    (46.10, 47.26, [("Bu", 46.10), ("juda", 46.30), ("*muhim*", 46.58), ("narsa,", 46.92)]),
    (47.30, 50.00, [("o’rtada", 47.30), ("biz", 47.62), ("*komfort*", 48.54), ("zonadan", 49.08), ("chiqib,", 49.62)]),
    (50.04, 51.82, [("keyingi", 50.04), ("zonaga", 50.90), ("o’tamiz —", 51.28)]),
    (51.86, 53.20, [("bu", 51.86), ("*diskomfort*", 51.96), ("zonasi", 52.52), ("bo’ladi.", 52.88)]),
    (60.72, 61.76, [("Albatta,", 60.72), ("sizga", 61.20), ("buning", 61.52)]),
    (64.38, 66.68, [("buning", 64.38), ("uchun", 64.60), ("orzularingizga", 64.92), ("*xiyonat*", 65.64), ("qilmaslik.", 66.12)]),
    (69.36, 70.44, [("Va", 69.36), ("qanday", 69.50), ("qilib", 69.76), ("*haqiqiy*", 70.10)]),
    (70.48, 71.70, [("*orzuga*", 70.48), ("erishish", 70.92), ("mumkin,", 71.34)]),
    (71.74, 72.74, [("qanday", 71.74), ("qilib", 71.90), ("o’zingizni,", 72.30)]),
    (72.78, 74.42, [("*missiyangizni*", 72.78), ("topishingiz", 73.44), ("mumkin.", 73.98)]),
    (74.46, 75.76, [("Bu", 74.46), ("haqida", 74.72), ("*mini-masterklassimda*", 75.14)]),
    (75.80, 77.06, [("gaplashamiz.", 76.30)]),
]
# captions under B-rolls (voice keeps playing, footage carries captions only)
C += [
    (21.00, 22.60, [("orzuni", 21.00), ("siz", 21.20), ("*maqsadga*", 21.48), ("aylantirasiz,", 22.02)]),
    (22.64, 24.00, [("*maqsaddan*", 22.64), ("keyin", 23.08), ("*reja*", 23.20), ("qilasiz.", 23.46)]),
    (32.40, 34.00, [("*komfort*", 32.40), ("*zonasidan*", 32.96), ("chiqyapsizmi,", 33.40)]),
    (34.04, 35.08, [("desak —", 34.04), ("«yo’q»,", 34.42), ("deydi.", 34.86)]),
    (39.36, 40.96, [("sizni", 39.36), ("bu", 39.60), ("orzu", 39.78), ("*uxlatmaydi*.", 40.20)]),
    (41.00, 43.28, [("Siz", 41.00), ("uni", 41.14), ("*maqsadga*", 41.42), ("aylantirasiz,", 42.18)]),
    (53.24, 54.92, [("O’sha", 53.24), ("diskomfortda —", 53.36), ("*yangi*", 54.08), ("*odatlar*,", 54.48)]),
    (54.96, 56.32, [("*yangi*", 54.96), ("*harakatlar*", 55.36), ("bo’ladi,", 55.92)]),
    (56.36, 57.74, [("ya’ni", 56.36), ("*yangi*", 56.52), ("*daraja*", 57.02), ("bo’ladi.", 57.34)]),
    (61.80, 63.12, [("uchun", 61.80), ("*bilim*", 62.20), ("kerak,", 62.80)]),
    (63.16, 64.34, [("buning", 63.16), ("uchun", 63.40), ("*ustoz*", 63.68), ("kerak,", 64.00)]),
]
C.sort()


def words(ws):
    return [{"t": t, "text": txt.replace("*", ""), **({"hot": True} if "*" in txt else {})} for txt, t in ws]


edit = {
    "name": "video17", "duration": 79.5, "accent": "#FFD60A", "captionBottom": 520,
    "framing": {"originX": 540, "originY": 720, "scale": 1.35, "shiftY": -110},
    "cuts": [{"t": 6.74, "type": "whip"}, {"t": 9.52, "type": "punch"}, {"t": 13.20, "type": "zoomblur"},
             {"t": 24.04, "type": "spin"}, {"t": 27.40, "type": "punch"}, {"t": 37.14, "type": "whip"},
             {"t": 46.10, "type": "zoomblur"}, {"t": 50.04, "type": "spin"}, {"t": 64.38, "type": "whip"},
             {"t": 71.74, "type": "zoomblur"}],
    "punches": [5.90, 10.68, 13.58, 28.92, 29.84, 37.92, 46.58, 48.54, 65.64, 70.10],
    "captions": [{"start": a, "end": b, "words": words(w)} for a, b, w in C],
    "brolls": [
        {"file": "01_pexels_woman-writing-notebook_1440p_25fps.mp4", "start": 20.98, "end": 24.02, "from": 1.0, "enter": "whip"},
        {"file": "02_pexels_woman-lying-couch_1440p_30fps.mp4", "start": 32.38, "end": 35.10, "from": 1.0, "enter": "zoomblur"},
        {"file": "03_pexels_woman-typing-laptop-lamp_1440p_24fps.mp4", "start": 39.34, "end": 43.30, "from": 1.0, "enter": "spin"},
        {"file": "04_pexels_woman-climbing-stairs_1440p_24fps.mp4", "start": 53.22, "end": 57.76, "from": 1.0, "enter": "whip"},
        {"file": "05_pexels_woman-reading-book_1440p_24fps.mp4", "start": 61.78, "end": 64.36, "from": 1.0, "enter": "zoomblur"},
    ],
    "cards": [
        {"start": 1.72, "end": 4.62, "thin": "Bugun gaplashamiz", "big": "*Orzu*|maqsad|niyat", "theme": "white",
         "icon": "i7558", "enter": "circle", "exit": "slide"},
        {"start": 16.44, "end": 20.98, "thin": "Maqsad — bu", "big": "*upakovka*|qilingan|orzu", "theme": "black",
         "enter": "wipe", "exit": "zoom"},
        {"start": 35.10, "end": 37.12, "thin": "Demak, bu", "big": "*haqiqiy*|orzu emas", "theme": "white",
         "icon": "i7557", "enter": "circle", "exit": "slide"},
        {"start": 57.76, "end": 60.70, "thin": "Siz eski fikrlar bilan", "big": "*yangi hayotni*|qura olmaysiz", "theme": "black",
         "enter": "wipe", "exit": "zoom"},
        {"start": 66.70, "end": 69.34, "thin": "Farqi bor:", "big": "Orzu|Maqsad|*Xohish*", "theme": "white",
         "enter": "circle", "exit": "slide"},
    ],
    "pills": [
        {"start": 6.74, "end": 9.48, "text": "Niyat xolis bo’lsin"},
        {"start": 24.04, "end": 26.28, "text": "Ko’pchilikda orzu bor", "icon": "i7555"},
        {"start": 43.32, "end": 46.06, "text": "Reja → Harakat", "icon": "i7556"},
        {"start": 46.10, "end": 47.26, "text": "Juda muhim!", "icon": "i7578"},
        {"start": 72.78, "end": 74.42, "text": "Missiyangizni toping", "icon": "i7569"},
        {"start": 74.46, "end": 77.06, "text": "Mini-masterklass", "icon": "i7556"},
    ],
    "badges": [
        {"start": 4.64, "end": 6.70, "icon": "i7558", "label": "Niyat", "theme": "white", "x": 155, "y": 580, "size": 220, "rot": -6},
        {"start": 13.20, "end": 14.46, "icon": "i7575", "label": "Maqsad", "theme": "black", "x": 155, "y": 580, "size": 220, "rot": 6},
        {"start": 29.84, "end": 31.46, "icon": "i7557", "label": "Harakat?", "theme": "white", "x": 155, "y": 580, "size": 220, "rot": -5},
        {"start": 37.14, "end": 39.32, "icon": "i7561", "label": "Haqiqiy orzu", "theme": "black", "x": 160, "y": 590, "size": 230, "rot": 5},
        {"start": 47.30, "end": 50.00, "icon": "i7558", "label": "Komfort", "theme": "white", "x": 155, "y": 590, "size": 220, "rot": -6},
        {"start": 50.04, "end": 53.20, "icon": "i7578", "label": "Diskomfort", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 6},
        {"start": 64.38, "end": 66.68, "icon": "i7566", "label": "Sodiqlik", "theme": "white", "x": 155, "y": 590, "size": 220, "rot": -5},
        {"start": 69.36, "end": 71.70, "icon": "i7575", "label": "Orzu", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 5},
        {"start": 75.80, "end": 77.06, "icon": "i7582", "label": "Obuna!", "theme": "white", "x": 155, "y": 590, "size": 220, "rot": -6},
    ],
    "stickers": [
        {"file": "s3899", "start": 9.52, "end": 11.10, "x": 925, "y": 640, "w": 210, "rot": 8},
        {"file": "s4072", "start": 14.50, "end": 16.40, "x": 925, "y": 640, "w": 210, "rot": -6},
        {"file": "s4049", "start": 26.32, "end": 29.80, "x": 925, "y": 640, "w": 150, "rot": 10},
        {"file": "s4051", "start": 37.14, "end": 39.32, "x": 925, "y": 640, "w": 210, "rot": 8},
        {"file": "s4073", "start": 47.30, "end": 50.00, "x": 925, "y": 640, "w": 210, "rot": -6},
        {"file": "s4041", "start": 50.04, "end": 53.20, "x": 925, "y": 640, "w": 210, "rot": 8},
        {"file": "s4097", "start": 71.74, "end": 74.42, "x": 925, "y": 640, "w": 210, "rot": -6},
        {"file": "s3885", "start": 74.46, "end": 77.06, "x": 925, "y": 640, "w": 200, "rot": 8},
    ],
    "endCard": {"start": 77.10, "title": "Feruza *Sabitova*", "sub": "@sabitova_akademiyasi", "cta": "Obuna bo’ling"},
    "music": "raising-me-higher", "musicDb": -23, "musicFrom": 2.0,
}
joins = [4.74, 9.52, 14.52, 16.62, 18.96, 21.36, 24.04, 27.54, 28.16, 35.16, 39.42, 41.08, 46.12, 50.54, 55.46,
         61.66, 62.32, 64.98, 66.76, 69.4, 74.56]
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
print("written", out.name, "jumps", edit["jumps"], "captions", len(edit["captions"]))
