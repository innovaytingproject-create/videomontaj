#!/usr/bin/env python3
"""Generates video18.json — "Odamlar nima deydi" (4. Что скажут люди), Feruza's blog.
Times are in the cut reel (3 "eh" + pauses cut; off-camera chatter after 101.7 s dropped).
The Russian notes at the end of the source are cut (client: "those were just notes"). Run: python src/edits/video18.py
"""
import json
from pathlib import Path

C = [
    (0.04, 1.82, [("Bilasizmi,", 0.04), ("nima", 0.58), ("uchun", 0.84), ("odamlar", 1.16)]),
    (1.86, 3.20, [("*orzularga*", 1.86), ("erisha", 2.54), ("olmaydi,", 2.84)]),
    (3.24, 4.72, [("va", 3.24), ("bu", 3.42), ("*armon*", 3.56), ("bo’lib", 4.08), ("qoladi?", 4.42)]),
    (4.76, 5.82, [("Chunki", 4.76), ("ular", 4.96), ("odamlarning", 5.24)]),
    (5.86, 6.98, [("*gapiga*", 5.86), ("qarab", 6.04), ("qolishadi.", 6.22)]),
    (11.12, 11.92, [("*uddalay*", 11.12), ("olmasam»", 11.50)]),
    (11.96, 13.32, [("degan", 11.96), ("*to’siqlar*", 12.20), ("qo’yiladi.", 12.88)]),
    (13.36, 14.68, [("O’zimda", 13.36), ("ham", 13.60), ("shunday", 13.98), ("bo’lgan,", 14.34)]),
    (14.72, 15.76, [("ko’p", 14.72), ("*ikkilanganman*.", 15.12)]),
    (15.80, 17.40, [("Agar", 15.80), ("men", 16.06), ("«odamlar", 16.28), ("nima", 16.86), ("deydi»", 17.04)]),
    (17.44, 18.90, [("deb", 17.44), ("o’sha", 17.56), ("paytda", 17.90), ("deganimda,", 18.30)]),
    (18.94, 20.74, [("o’sha", 18.94), ("payt", 19.25), ("*san’atkor*", 19.60), ("bo’lgan,", 20.34)]),
    (20.78, 22.32, [("ko’p", 20.78), ("*to’siqlar*", 21.36), ("bo’lardi,", 21.96)]),
    (22.36, 24.12, [("hatto", 22.36), ("o’zimning", 22.80), ("*qarindoshlarim*", 23.02), ("tomonidan.", 23.66)]),
    (26.82, 28.72, [("Shuning", 26.82), ("uchun,", 27.16), ("azizlar,", 27.46), ("odamlar", 27.88)]),
    (28.76, 30.08, [("*gapirgan*", 28.76), ("va", 29.38), ("gapiradi.", 29.58)]),
    (32.76, 33.64, [("*Muhimi*,", 32.76), ("siz", 33.24)]),
    (37.88, 40.00, [("Agar", 37.88), ("siz", 38.20), ("odamlarning", 38.32), ("*gapi*", 38.96), ("bilan", 39.10), ("yashasangiz,", 39.36)]),
    (40.04, 43.24, [("agar", 40.04), ("«odamlar", 40.36), ("nima", 41.20), ("deydi»", 42.14), ("deb", 42.44), ("yashasangiz,", 42.68)]),
    (43.28, 44.02, [("bir", 43.28), ("kun", 43.50), ("kelib", 43.74)]),
    (44.06, 45.36, [("siz", 44.06), ("bir", 44.16), ("narsani", 44.46), ("*anglaysiz*:", 44.84)]),
    (45.40, 46.76, [("siz", 45.40), ("*boshqalarning*,", 45.82)]),
    (49.92, 52.30, [("*Muhimi* —", 49.92), ("qo’rqsangiz", 50.54), ("ham", 50.76), ("*harakat*", 51.48), ("qilish.", 51.82)]),
    (52.34, 54.42, [("Qo’rquv", 52.34), ("sizni", 53.02), ("*to’xtatmasligi*", 53.16), ("kerak.", 53.86)]),
    (56.40, 58.40, [("Asosan,", 56.40), ("*omadli*", 56.88), ("insonlar", 57.94)]),
    (61.74, 63.50, [("Va", 61.74), ("eng", 61.92), ("*muhimi*,", 62.42), ("sizning", 62.92)]),
    (63.54, 65.00, [("hayotingizni", 63.54), ("ham,", 64.38), ("sizning", 64.72)]),
    (65.02, 67.40, [("*orzuingizni*", 65.02), ("ham", 65.70), ("boshqa", 66.06), ("siz", 66.58), ("uchun", 66.98)]),
    (67.44, 68.50, [("hech", 67.44), ("kim", 67.58), ("*yashab*", 67.72), ("*bermaydi*.", 67.92)]),
]
# captions over B-rolls (voice keeps playing)
C += [
    (7.02, 8.18, [("«Odamlar", 7.02), ("nima", 7.58), ("*deydi*,", 7.74)]),
    (8.22, 9.72, [("*kulishadi*", 8.22), ("ustimdan,", 9.22)]),
    (9.76, 11.08, [("men", 9.76), ("buni", 9.98), ("eplay", 10.24), ("olmasam,", 10.60)]),
    (33.68, 35.76, [("agar", 33.68), ("o’zingizning", 34.78), ("*fikringiz*", 35.20), ("bilan,", 35.56)]),
    (35.80, 37.84, [("o’zingizning", 35.80), ("*orzularingiz*", 36.50), ("bilan", 36.90), ("yashashingiz", 37.10), ("kerak.", 37.56)]),
    (46.80, 48.58, [("boshqalar", 46.80), ("sizga", 47.38), ("gapirgan", 47.74), ("*hayot*", 48.12), ("bilan", 48.40)]),
    (48.62, 49.88, [("yashaganingizni", 48.62), ("tushunib", 49.16), ("qolasiz.", 49.40)]),
    (54.46, 56.36, [("Muhimi —", 54.46), ("*qo’rqsangiz*", 54.92), ("*ham*", 55.28), ("harakat", 55.66), ("qilish.", 56.00)]),
    (58.44, 60.12, [("qo’rqsa", 58.44), ("ham", 58.96), ("*harakat*", 59.40), ("qilganda", 59.70)]),
    (60.16, 61.70, [("*muvaffaqiyatga*", 60.16), ("erishgan.", 61.18)]),
]
C.sort()


def words(ws):
    return [{"t": t, "text": txt.replace("*", ""), **({"hot": True} if "*" in txt else {})} for txt, t in ws]


edit = {
    "name": "video18", "duration": 76.9, "accent": "#FFD60A", "captionBottom": 520,
    "framing": {"originX": 540, "originY": 720, "scale": 1.35, "shiftY": -110},
    "cuts": [{"t": 4.76, "type": "whip"}, {"t": 13.36, "type": "zoomblur"}, {"t": 18.94, "type": "spin"},
             {"t": 22.36, "type": "punch"}, {"t": 37.88, "type": "whip"}, {"t": 43.28, "type": "zoomblur"},
             {"t": 52.34, "type": "spin"}, {"t": 63.54, "type": "whip"}],
    "punches": [1.86, 5.86, 12.20, 15.12, 19.60, 28.76, 38.96, 44.84, 50.54, 62.42, 67.72],
    "captions": [{"start": a, "end": b, "words": words(w)} for a, b, w in C],
    "brolls": [
        {"file": "01_pexels_hands-cover-woman-eyes_1440p_25fps.mp4", "start": 7.00, "end": 11.10, "from": 11.5, "enter": "whip"},
        {"file": "02_pexels_woman-mountain-peak_1080p_60fps.mp4", "start": 33.66, "end": 37.86, "from": 6.0, "enter": "zoomblur"},
        {"file": "03_pexels_sad-woman-window_1080p_30fps.mp4", "start": 46.78, "end": 49.90, "from": 0.3, "enter": "spin"},
        {"file": "04_pexels_skydiver-sunset_1440p_25fps.mp4", "start": 54.44, "end": 56.38, "from": 2.0, "enter": "whip"},
        {"file": "05_pexels_summit-arms-outstretched_1440p_60fps.mp4", "start": 58.42, "end": 61.72, "from": 0.2, "enter": "zoomblur"},
    ],
    "cards": [
        {"start": 24.14, "end": 26.80, "thin": "Aks holda", "big": "men bugun|*Feruza Sabitova*|bo’lmasdim", "theme": "white",
         "icon": "i7575", "enter": "circle", "exit": "slide"},
        {"start": 30.10, "end": 32.74, "thin": "Harakat qilsangiz ham, qilmasangiz ham", "big": "odamlar|*gapiradi*", "theme": "black",
         "icon": "i7567", "enter": "wipe", "exit": "zoom"},
        {"start": 68.54, "end": 71.72, "thin": "Bilasizmi?", "big": "*Qo’rquv*|orzuni|o’ldirmaydi", "theme": "black",
         "enter": "wipe", "exit": "zoom"},
        {"start": 71.72, "end": 74.50, "thin": "Qo’rquv sabab", "big": "*harakat*|*qilmaslik*|orzuni o’ldiradi", "theme": "white",
         "icon": "i7574", "enter": "circle", "exit": "slide"},
    ],
    "pills": [
        {"start": 0.04, "end": 3.20, "text": "Nega orzu armonga aylanadi?", "icon": "i7557"},
        {"start": 49.92, "end": 52.30, "text": "Qo’rqsang ham — harakat qil", "icon": "i7565"},
        {"start": 63.54, "end": 68.50, "text": "Hech kim siz uchun yashab bermaydi", "icon": "i7582"},
    ],
    "badges": [
        {"start": 3.24, "end": 4.72, "icon": "i7568", "label": "Armon", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 6},
        {"start": 4.76, "end": 6.98, "icon": "i7567", "label": "Odamlar gapi", "theme": "white", "x": 160, "y": 590, "size": 230, "rot": -5},
        {"start": 11.12, "end": 13.32, "icon": "i7570", "label": "To’siqlar", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 5},
        {"start": 13.36, "end": 15.76, "icon": "i7558", "label": "Ikkilanish", "theme": "white", "x": 155, "y": 590, "size": 220, "rot": -6},
        {"start": 18.94, "end": 20.74, "icon": "i7575", "label": "San’atkor", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 6},
        {"start": 22.36, "end": 24.12, "icon": "i7562", "label": "Qarindoshlar", "theme": "white", "x": 160, "y": 590, "size": 230, "rot": -5},
        {"start": 37.88, "end": 40.00, "icon": "i7567", "label": "Odamlar gapi", "theme": "black", "x": 160, "y": 590, "size": 230, "rot": 5},
        {"start": 45.40, "end": 46.76, "icon": "i7555", "label": "Boshqalar", "theme": "white", "x": 155, "y": 590, "size": 220, "rot": -6},
        {"start": 52.34, "end": 54.42, "icon": "i7578", "label": "Qo’rquv", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 6},
        {"start": 56.40, "end": 58.40, "icon": "i7571", "label": "Omad", "theme": "white", "x": 155, "y": 590, "size": 220, "rot": -5},
        {"start": 61.74, "end": 63.50, "icon": "i7561", "label": "Hayotingiz", "theme": "black", "x": 155, "y": 590, "size": 220, "rot": 5},
    ],
    "stickers": [
        {"file": "s4046", "start": 4.76, "end": 6.98, "x": 925, "y": 640, "w": 210, "rot": -8},
        {"file": "s4055", "start": 11.12, "end": 13.32, "x": 925, "y": 640, "w": 200, "rot": 8},
        {"file": "s3899", "start": 13.36, "end": 15.76, "x": 925, "y": 640, "w": 200, "rot": 8},
        {"file": "s3942", "start": 18.94, "end": 20.74, "x": 925, "y": 640, "w": 210, "rot": 10},
        {"file": "s4047", "start": 26.82, "end": 30.08, "x": 925, "y": 640, "w": 210, "rot": -6},
        {"file": "s4043", "start": 43.28, "end": 45.36, "x": 925, "y": 640, "w": 190, "rot": 10},
        {"file": "s4051", "start": 65.02, "end": 67.40, "x": 925, "y": 640, "w": 200, "rot": 8},
    ],
    "endCard": {"start": 74.52, "title": "Feruza *Sabitova*", "sub": "@sabitova_akademiyasi", "cta": "Obuna bo’ling"},
    "music": "dreaming-big", "musicDb": -18, "musicFrom": 1.5,
}
joins = [4.84, 8.4, 13.38, 14.84, 15.84, 19.72, 20.96, 21.3, 22.48, 26.92, 32.8, 33.4, 34.44, 34.88, 41.06, 46.96,
         49.98, 52.28, 54.48, 56.44, 61.8, 66.18, 68.46, 70.48, 71.82]
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
