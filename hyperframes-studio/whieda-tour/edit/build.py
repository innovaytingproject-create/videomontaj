#!/usr/bin/env python3
"""WHIEDA office tour (full, 1:29) in the approved v3 style — see handoff TZ.

CSS is lifted verbatim from ../whieda-15s/index.html (approved v3). Everything
is timed to the source (no cuts). Edit this script, not index.html.
"""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V3 = (ROOT.parent / "whieda-15s" / "index.html").read_text()
css = re.search(r"<style>(.*?)</style>", V3, re.S).group(1)
css = re.sub(r"\.grad \{.*?\}\n", "", css, flags=re.S)  # no bottom gradient in v3

A = "’"
VID = 88.8
DUR = 90.6
j = lambda t: f"{t:.2f}"

extra_css = """
      /* pills above the head (check, section with icon) */
      .pill { position: absolute; top: 160px; left: 0; right: 0; display: flex; justify-content: center; }
      .pill-in { display: flex; align-items: center; gap: 18px; background: rgba(255,255,255,.97); border-radius: 60px;
                 padding: 14px 34px 14px 16px; box-shadow: 0 14px 40px rgba(10,20,40,.28); }
      .pill-in .dot { width: 64px; height: 64px; border-radius: 50%; flex: none; display: flex; align-items: center; justify-content: center;
                      background: var(--blue); color: #fff; font-weight: 800; font-size: 34px; }
      .pill-in .dot img { display: block; height: 46px; width: auto; }
      .pill-in span { font-weight: 700; font-size: 34px; color: var(--ink); }
      /* iMessage-style quotes, stacked above the head */
      .bub { position: absolute; left: 70px; }
      .bub0 { top: 150px; } .bub1 { top: 240px; } .bub2 { top: 330px; }
      .bub-in { display: inline-block; background: rgba(255,255,255,.97); border-radius: 30px; padding: 14px 28px;
                box-shadow: 0 12px 34px rgba(10,20,40,.26); font-weight: 700; font-size: 32px; color: var(--ink); }
      .bub-in em { font-style: normal; color: var(--blue); }
      .wc-ico { margin-top: 30px; height: 250px; width: auto; }
      .wc-big.num { font-size: 230px; }
      /* end card */
      .endcard { position: absolute; inset: 0; z-index: 11; }
      .end-bg { position: absolute; inset: 0; opacity: 0; background:
        radial-gradient(1000px 800px at 50% 20%, #ffffff 0%, rgba(255,255,255,0) 60%),
        radial-gradient(1100px 1000px at 50% 110%, var(--sky) 0%, rgba(191,217,255,0) 60%), var(--ice); }
      .end-in { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; padding-bottom: 160px; }
      .end-in img { width: 200px; height: auto; }
      .end-logo { margin-top: 14px; font-weight: 700; font-size: 120px; line-height: 1; color: #ba7a08; letter-spacing: .03em; }
      .end-sub { margin-top: 18px; font-weight: 400; font-size: 40px; color: #5d6066; }
      .end-pill { margin-top: 40px; background: var(--blue); color: #fff; border-radius: 60px; padding: 22px 52px 26px;
                  font-weight: 700; font-size: 42px; box-shadow: 0 18px 44px rgba(10,132,255,.35); }
"""

# ---------- captions (word-synced, Uzbek Latin; *x* = blue accent) ----------
CAPS = [
    (0.05, 1.35, "Assalomu alaykum, *azizlar!*"),
    (1.40, 3.48, "Bugun biz xalqaro *WHIEDA* assotsiatsiyasining"),
    (3.50, 5.35, "Toshkentdagi *ofisidamiz*"),
    (5.40, 7.75, "Bilasiz, men mana shu assotsiatsiya bilan"),
    (7.80, 9.70, "*hamkorlik qilaman.* Qani, ketdik!"),
    # 9.8-12.1 accent card 1
    (12.20, 15.10, "Bu *rasmiy* ishlaydimi?"),
    (15.20, 16.85, "Ha, albatta, ko" + A + "rib turibsiz:"),
    (16.90, 20.20, "mana, bizda *sertifikatlar* bor"),
    (20.30, 23.30, "har bir mahsulot uchun *sertifikat*"),
    (23.40, 25.95, "Eng muhimi — *WHIEDA* xalqaro assotsiatsiyasi"),
    (26.00, 28.55, "siz ham o" + A + "z faoliyatingizni"),
    # 28.6-30.8 accent card 2
    (30.90, 32.65, "Ana bu yerda, ko" + A + "rib turibsiz,"),
    (32.70, 35.90, "*onlayn platformamizdagi* barcha mahsulotlar"),
    (36.30, 38.15, "Bu mahsulotlarning hammasi"),
    # 38.2-40.7 accent card 3
    (40.90, 43.35, "Sizda *muammo* bormi:"),
    (43.40, 45.70, "oyoqda, belda, panjada,"),
    (45.80, 47.75, "boshda, qo" + A + "lda — *farqi yo" + A + "q*"),
    (47.80, 50.15, "hamma narsani hozir"),
    # 50.2-52.6 accent card 4
    (52.70, 56.20, "o" + A + "zingizga o" + A + "zingiz qarab,"),
    (56.30, 57.75, "*yordam bera olasiz*"),
    (57.80, 59.25, "Hamma menga aytadi:"),
    # 59.3-63.9 quote bubbles carry the speech
    (64.00, 66.15, "Bularning hammasi — *WHIEDA* assotsiatsiyasining"),
    (66.20, 68.75, "ajoyib *xitoy tibbiyoti*"),
    (68.80, 71.15, "tabobati bo" + A + "yicha ishlab chiqarilgan"),
    (71.20, 72.65, "yangi *texnologiya*, mahsulotlar"),
    # 72.7-74.9 accent card 5
    (74.95, 78.15, "Hozir biz yangiliklar bo" + A + "yicha"),
    # 78.2-80.6 accent card 6 (No1)
    (80.65, 81.35, "barcha sohalarda"),
    (81.40, 83.55, "va aynan tabobat bo" + A + "yicha"),
    (83.60, 85.15, "mana, ko" + A + "rib turibsiz —"),
    (85.20, 87.95, "*zo" + A + "r natija* beradigan mahsulotlar"),
]

# ---------- accent cards: one per 15 s window ----------
CARDS = [  # (start, end, thin line, big html, icon or None, numeric)
    (9.80, 12.10, "Ko" + A + "pchilik so" + A + "raydi", "<em>Ofisingiz</em><br>bormi?", "i7557-blue.png", False),
    (28.60, 30.85, "Eng muhimi", "O" + A + "z<br><em>biznesingiz</em>", "i7565-blue.png", False),
    (38.20, 40.75, "Juda-juda foydali", "Inson<br><em>salomatligi</em> uchun", None, False),
    (50.20, 52.65, "Hamma narsani", "<em>Uyda</em><br>o" + A + "tirib", None, False),
    (72.70, 74.90, "An" + A + "anaviy", "<em>Xitoy</em><br>tabobati", None, False),
    (78.20, 80.60, "Yangiliklar bo" + A + "yicha", "<em>№1</em>", "i7575-blue.png", True),
]

# ---------- inserts above the head ----------
LOGOS = [(1.34, 3.48), (23.60, 25.95), (64.00, 66.15)]  # every time she says WHIEDA / the association

# camera: transition every 7 s, skipped when it would land on/near an accent card
TRANS = [t for t in range(7, 88, 7)
         if all(not (a - 0.8 <= t <= b + 0.3) for a, b, *_ in CARDS)]

clips, tl = [], []


def rich(text):
    out = []
    for part in re.split(r"(\*[^*]+\*)", text):
        hot = part.startswith("*")
        for w in part.strip("*").split():
            out.append(f'<span class="w{" hot" if hot else ""}">{html.escape(w)}</span>')
    return " ".join(out)


for i, (a, b, text) in enumerate(CAPS):
    clips.append(f'<div id="c{i}" class="clip cap" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="4"><p class="cap-t">{rich(text)}</p></div>')
    tl.append(f'tl.fromTo("#c{i} .w", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .28, ease: "back.out(1.8)", stagger: .05 }}, {j(a)});')
    tl.append(f'tl.to("#c{i} .cap-t", {{ opacity: 0, y: -10, duration: .16, ease: "power2.in" }}, {j(b - .17)});')

for n, (a, b) in enumerate(LOGOS):
    clips.append(f'<div id="lg{n}" class="clip logo" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="3">'
                 '<div class="logo-in"><img src="assets/whieda-emblem.png" alt="" />'
                 '<div><div class="logo-w">WHIEDA</div><div class="logo-s">XALQARO ASSOTSIATSIYA</div></div></div></div>')
    tl.append(f'tl.fromTo("#lg{n} .logo-in", {{ y: -40, opacity: 0, scale: .88 }}, {{ y: 0, opacity: 1, scale: 1, duration: .5, ease: "back.out(1.6)" }}, {j(a)});')
    tl.append(f'tl.fromTo("#lg{n} img", {{ rotation: -90, scale: .6 }}, {{ rotation: 0, scale: 1, duration: .6, ease: "back.out(1.8)" }}, {j(a + .06)});')
    tl.append(f'tl.to("#lg{n} .logo-in", {{ y: -30, opacity: 0, duration: .25, ease: "power2.in" }}, {j(b - .27)});')

# cover, banner (approved)
clips.append('<div id="cover" class="clip cover" data-start="3.50" data-duration="1.85" data-track-index="3"><div class="cover-in" id="coverin">'
             '<div class="cover-k">WHIEDA &middot; TOSHKENT</div><div class="cover-t">Ofisimizga <em>sayohat</em></div>'
             '<div class="cover-line" id="cline"></div></div></div>')
tl += ['tl.fromTo("#coverin", { y: -40, opacity: 0, scale: .9 }, { y: 0, opacity: 1, scale: 1, duration: .5, ease: "back.out(1.5)" }, 3.53);',
       'tl.fromTo("#cline", { scaleX: 0 }, { scaleX: 1, duration: .5, ease: "power3.inOut" }, 3.9);',
       'tl.to("#coverin", { y: -30, opacity: 0, duration: .26, ease: "power2.in" }, 5.07);']
clips.append('<div id="banner" class="clip banner" data-start="7.75" data-duration="1.95" data-track-index="3"><div class="banner-in" id="bannerin">'
             '<div class="b-icon logo-ic"><img src="assets/whieda-emblem.png" alt="" /></div>'
             '<div class="b-body"><div class="b-title">WHIEDA</div><div class="b-text">Feruza &mdash; rasmiy hamkor</div></div>'
             '<div class="b-time">hozir</div></div></div>')
tl += ['tl.fromTo("#bannerin", { y: -200, opacity: 0, scale: .96 }, { y: 0, opacity: 1, scale: 1, duration: .5, ease: "back.out(1.25)" }, 7.8);',
       'tl.to("#bannerin", { y: -200, opacity: 0, duration: .32, ease: "power3.in" }, 9.36);']

# pills: certificates check, problem areas with icon
PILLS = [(16.90, 20.20, '<div class="dot">&#10003;</div><span>Rasmiy sertifikatlar</span>'),
         (32.70, 35.90, '<div class="dot">&#10003;</div><span>Onlayn platforma</span>'),
         (43.40, 47.75, '<div class="dot"><img src="assets/icons/i7568-white.png" alt="" /></div><span>Oyoq &middot; bel &middot; bosh &middot; qo&#8217;l</span>')]
for n, (a, b, inner) in enumerate(PILLS):
    clips.append(f'<div id="pl{n}" class="clip pill" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="3"><div class="pill-in">{inner}</div></div>')
    tl.append(f'tl.fromTo("#pl{n} .pill-in", {{ y: -150, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .5, ease: "back.out(1.3)" }}, {j(a)});')
    tl.append(f'tl.fromTo("#pl{n} .dot", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: .45, ease: "back.out(2.4)" }}, {j(a + .18)});')
    tl.append(f'tl.to("#pl{n} .pill-in", {{ y: -130, opacity: 0, duration: .3, ease: "power3.in" }}, {j(b - .32)});')

# quote bubbles: "Yosharibsiz! / Salomatligingiz zo'r! / Figurangiz yaxshi bo'libdi!"
BUBS = [(59.30, "<em>Yosharibsiz!</em>"), (60.20, "Salomatligingiz <em>zo&#8217;r!</em>"), (62.00, "Figurangiz <em>yaxshi</em> bo&#8217;libdi!")]
for n, (a, txt) in enumerate(BUBS):
    clips.append(f'<div id="bb{n}" class="clip bub bub{n}" data-start="{j(a)}" data-duration="{j(63.95 - a)}" data-track-index="3"><span class="bub-in">{txt}</span></div>')
    tl.append(f'tl.fromTo("#bb{n} .bub-in", {{ scale: .5, opacity: 0, y: 20 }}, {{ scale: 1, opacity: 1, y: 0, duration: .45, ease: "back.out(1.9)" }}, {j(a)});')
    tl.append(f'tl.to("#bb{n} .bub-in", {{ y: -16, opacity: 0, duration: .22, ease: "power2.in" }}, {j(63.68 + n * .04)});')

# accent cards
for n, (a, b, thin, big, icon, num) in enumerate(CARDS):
    parts = big.split("<br>")
    masks = "".join(f'<div class="wc-mask"><div class="wc-big{" num" if num else ""}" id="wb{n}_{k}">{p}</div></div>' for k, p in enumerate(parts))
    ico = f'<img class="wc-ico" id="wi{n}" src="assets/icons/{icon}" alt="" />' if icon else ""
    clips.append(f'<div id="wc{n}" class="clip wcard" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="6">'
                 f'<div class="wc-bg" id="wbg{n}"></div><div class="wc-in" id="win{n}"><div class="wc-sub" id="ws{n}">{thin}</div>{masks}{ico}</div></div>')
    tl.append(f'tl.fromTo("#wbg{n}", {{ opacity: 0 }}, {{ opacity: 1, duration: .3, ease: "power2.out" }}, {j(a)});')
    tl.append(f'tl.fromTo("#ws{n}", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .38, ease: "power2.out" }}, {j(a + .16)});')
    for k in range(len(parts)):
        tl.append(f'tl.fromTo("#wb{n}_{k}", {{ yPercent: 115 }}, {{ yPercent: 0, duration: .5, ease: "power4.out" }}, {j(a + .26 + k * .16)});')
    if icon:
        tl.append(f'tl.fromTo("#wi{n}", {{ scale: 0, rotation: -12 }}, {{ scale: 1, rotation: 0, duration: .5, ease: "back.out(2)" }}, {j(a + .6)});')
        tl.append(f'tl.to("#wi{n}", {{ y: -10, duration: {j(max(.6, b - a - 1.4))}, ease: "sine.inOut" }}, {j(a + 1.1)});')
    tl.append(f'tl.to("#win{n}", {{ opacity: 0, scale: 1.04, filter: "blur(8px)", duration: .3, ease: "power2.in" }}, {j(b - .32)});')
    tl.append(f'tl.to("#wbg{n}", {{ opacity: 0, duration: .3, ease: "power2.in" }}, {j(b - .32)});')

# end card with the logo
clips.append(f'<div id="end" class="clip endcard" data-start="88.05" data-duration="{j(DUR - 88.05)}" data-track-index="7">'
             '<div class="end-bg" id="ebg"></div><div class="end-in">'
             '<img id="eimg" src="assets/whieda-emblem.png" alt="" /><div class="wc-mask"><div class="end-logo" id="elogo">WHIEDA</div></div>'
             '<div class="end-sub" id="esub">Toshkent &middot; rasmiy ofis</div>'
             '<div class="end-pill" id="epill">Bepul sinab ko&#8217;ring &mdash; profilda</div></div></div>')
tl += ['tl.fromTo("#ebg", { opacity: 0 }, { opacity: 1, duration: .4, ease: "power2.out" }, 88.05);',
       'tl.fromTo("#eimg", { scale: .5, rotation: -90, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: .6, ease: "back.out(1.7)" }, 88.25);',
       'tl.fromTo("#elogo", { yPercent: 115 }, { yPercent: 0, duration: .55, ease: "power4.out" }, 88.5);',
       'tl.fromTo("#esub", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power2.out" }, 88.8);',
       'tl.fromTo("#epill", { scale: .7, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, ease: "back.out(1.6)" }, 89.0);']

# camera: alternate push-in / pull-out between 7 s transitions
marks = [0.0] + TRANS + [VID]
zoom_in = True
tl.append('tl.fromTo("#cam", { scale: 1.0, rotation: 0, filter: "blur(0px)" }, { scale: 1.0, duration: .01 }, 0);')
for k in range(len(marks) - 1):
    a, b = marks[k], marks[k + 1]
    start = a + (0.32 if k else 0)
    end_s = 1.14 if zoom_in else 1.0
    seg_from = (1.0 if k == 0 else (1.2 if not zoom_in else 1.04))
    if k:
        # landing half of the transition at `a`
        tl.append(f'tl.fromTo("#cam", {{ scale: {seg_from + .22:.2f}, rotation: {(-2.5 if k % 2 else 2.5)}, filter: "blur(18px)" }}, '
                  f'{{ scale: {seg_from:.2f}, rotation: 0, filter: "blur(0px)", duration: .32, ease: "expo.out", immediateRender: false }}, {j(a)});')
    out_t = b - 0.18 if b < VID else b
    tl.append(f'tl.to("#cam", {{ scale: {end_s:.2f}, duration: {j(max(.5, out_t - start))}, ease: "sine.inOut" }}, {j(start)});')
    if b < VID:
        tl.append(f'tl.to("#cam", {{ scale: {end_s + .3:.2f}, rotation: {(2.5 if k % 2 else -2.5)}, filter: "blur(18px)", duration: .18, ease: "power3.in" }}, {j(b - .18)});')
        tl.append(f'tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: .6, duration: .12, ease: "power1.in", immediateRender: false }}, {j(b - .1)});')
        tl.append(f'tl.to("#flash", {{ opacity: 0, duration: .3, ease: "power2.out" }}, {j(b + .02)});')
        tl.append(f'tl.fromTo("#tint", {{ opacity: 0 }}, {{ opacity: 1, duration: .15, ease: "power1.in", immediateRender: false }}, {j(b - .12)});')
        tl.append(f'tl.to("#tint", {{ opacity: 0, duration: .45, ease: "power2.out" }}, {j(b + .03)});')
    zoom_in = not zoom_in

page = f"""<!doctype html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <!-- Generated by edit/build.py — edit that script, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="vendor/fonts.css" />
    <style>{css}{extra_css}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{j(DUR)}" data-width="1080" data-height="1920">
      <div class="vidwrap"><div class="cam" id="cam">
        <video id="aroll" class="clip" src="assets/tour-graded.mp4" playsinline muted data-start="0" data-duration="{j(VID)}" data-track-index="0"></video>
      </div></div>
      <div class="tint" id="tint"></div>
      <div class="flash" id="flash"></div>
{chr(10).join('      ' + c for c in clips)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join('      ' + l for l in tl)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(page)
(ROOT / "edit" / "transitions.txt").write_text(" ".join(map(str, TRANS)))
print(f"index.html: {len(clips)} clips, transitions at {TRANS}")
