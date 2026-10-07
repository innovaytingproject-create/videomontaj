#!/usr/bin/env python3
"""Office-tour video in the approved Apple style. CSS comes from foherb-full."""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = (ROOT.parent / "foherb-full" / "index.html").read_text()

DUR = 90.5
VID_END = 88.8
j = lambda t: f"{t:.2f}"

css = re.search(r"<style>(.*?)</style>", SRC, re.S).group(1)
extra_css = """
      /* iMessage-style testimonial bubbles */
      .bub { position: absolute; left: 70px; }
      .bub0 { top: 960px; } .bub1 { top: 1092px; } .bub2 { top: 1224px; }
      .bub-in { display: inline-block; background: rgba(243,244,246,.97); border-radius: 38px; padding: 22px 38px;
                box-shadow: 0 14px 40px rgba(7,20,40,.28); font-weight: 600; font-size: 40px; color: var(--ink); }
      /* №1 card */
      .onec { position: absolute; left: 0; right: 0; top: 940px; display: flex; justify-content: center; }
      .onec-in { background: rgba(250,252,255,.97); border-radius: 56px; padding: 36px 90px 46px; text-align: center;
                 box-shadow: 0 36px 80px rgba(7,20,40,.32); }
      .o-num { font-weight: 900; font-size: 210px; line-height: 1; color: var(--blue); letter-spacing: -0.02em; }
      .o-lab { margin-top: 6px; font-weight: 600; font-size: 40px; color: var(--gray); }
"""

A = "’"
CAPTIONS = [
    (2.60, 5.30, f"Bugun biz *MEDA assotsiatsiyasining* Toshkentdagi ofisidamiz"),
    (5.40, 9.60, "Men shu assotsiatsiya bilan *hamkorlik qilaman* — yuring!"),
    (9.80, 15.00, f"Ko{A}pchilik so{A}raydi: *ofisingiz bormi*, rasmiy ishlaydimi?"),
    (15.20, 20.10, f"Albatta! Mana — *sertifikatlarimiz*"),
    (20.30, 23.40, "har bir mahsulot uchun *alohida sertifikat*"),
    (23.50, 30.40, f"Eng muhimi — bu yerda *o{A}z biznesingizni* boshlashingiz mumkin"),
    (30.50, 36.20, "Mana — *onlayn platformamizdagi* barcha mahsulotlar"),
    (36.30, 40.70, "ularning hammasi *inson salomatligi* uchun foydali"),
    (40.90, 47.70, f"Oyoq, bel, bosh og{A}riydimi — *farqi yo{A}q*"),
    (47.80, 53.00, "hammasini *uyda o&#8217;tirib* hal qilasiz".replace("&#8217;", A)),
    (53.05, 57.70, f"o{A}zingizni *o{A}zingiz davolaysiz*"),
    (57.80, 60.20, "Hamma menga aytadi:"),
    (64.00, 68.70, "Bularning bari — *ajoyib xitoy tibbiyoti*"),
    (68.80, 72.70, f"eng so{A}nggi *texnologiyalar* asosida"),
    (72.75, 74.60, f"an{A}anaviy *xitoy tabobati* bilan"),
    (74.80, 78.20, f"Bugun biz *yangiliklar bo{A}yicha*"),
    (78.25, 81.40, f"*birinchi o{A}rinda* turibmiz"),
    (81.45, 85.20, f"aynan tabobat bo{A}yicha — ko{A}rib turibsiz"),
    (85.25, 88.00, "*zo&#8217;r natija* beradigan mahsulotlar".replace("&#8217;", A)),
]
SECTIONS = [(15.3, "01", "Sertifikatlar"), (30.6, "02", "Mahsulotlar"), (47.9, "03", "Uyda davolanish"),
            (57.9, "04", "Natijalar"), (64.1, "05", "Xitoy tabobati")]
BUBBLES = [(59.5, "Yosharibsiz!"), (61.0, f"Salomatligingiz zo{A}r!"), (62.5, f"Figurangiz yaxshi bo{A}libdi!")]

clips, tl = [], []


def rich(text):
    parts = re.split(r"(\*[^*]+\*)", text)
    out = []
    for part in parts:
        hot = part.startswith("*")
        for w in part.strip("*").split():
            out.append(f'<span class="w{" hot" if hot else ""}">{html.escape(w)}</span>')
    return " ".join(out)


for i, (a, b, text) in enumerate(CAPTIONS):
    clips.append(f'<div id="cap{i}" class="clip cap" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="4">'
                 f'<p class="cap-card">{rich(text)}</p></div>')
    tl.append(f'tl.fromTo("#cap{i} .cap-card", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .4, ease: "power3.out" }}, {j(a)});')
    tl.append(f'tl.fromTo("#cap{i} .w", {{ opacity: 0 }}, {{ opacity: 1, duration: .25, ease: "power1.out", stagger: .04 }}, {j(a + .08)});')
    tl.append(f'tl.to("#cap{i} .cap-card", {{ y: 24, opacity: 0, duration: .25, ease: "power2.in" }}, {j(b - .28)});')

for n, (a, num, label) in enumerate(SECTIONS):
    clips.append(f'<div id="sec{n}" class="clip sec" data-start="{j(a)}" data-duration="2.6" data-track-index="2">'
                 f'<div class="sec-in"><b>{num}</b><span>{html.escape(label)}</span></div></div>')
    tl.append(f'tl.fromTo("#sec{n} .sec-in", {{ y: -150, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .5, ease: "back.out(1.2)" }}, {j(a)});')
    tl.append(f'tl.to("#sec{n} .sec-in", {{ y: -130, opacity: 0, duration: .3, ease: "power3.in" }}, {j(a + 2.25)});')

for n, (a, text) in enumerate(BUBBLES):
    clips.append(f'<div id="bub{n}" class="clip bub bub{n}" data-start="{j(a)}" data-duration="{j(64.0 - a)}" data-track-index="2">'
                 f'<span class="bub-in">{html.escape(text)}</span></div>')
    tl.append(f'tl.fromTo("#bub{n} .bub-in", {{ scale: .5, opacity: 0, y: 24 }}, {{ scale: 1, opacity: 1, y: 0, duration: .45, ease: "back.out(1.9)" }}, {j(a)});')
    tl.append(f'tl.to("#bub{n} .bub-in", {{ y: -20, opacity: 0, duration: .25, ease: "power2.in" }}, {j(63.6 + n * .05)});')

clips.append('<div id="onec" class="clip onec" data-start="78.3" data-duration="3.3" data-track-index="2">'
             '<div class="onec-in" id="onein"><div class="o-num">&#8470;1</div>'
             f'<div class="o-lab">yangiliklar bo{A}yicha</div></div></div>')
tl.append('tl.fromTo("#onein", { scale: .6, opacity: 0, y: 40 }, { scale: 1, opacity: 1, y: 0, duration: .55, ease: "back.out(1.4)" }, 78.35);')
tl.append('tl.to("#onein", { scale: .92, opacity: 0, duration: .3, ease: "power2.in" }, 81.3);')

# Living camera.
PUNCH = [9.8, 15.3, 23.5, 30.6, 40.9, 47.9, 57.9, 64.1, 74.8, 78.3]
tl.append('tl.fromTo("#vz", { scale: 1.12 }, { scale: 1.035, duration: 1.0, ease: "power2.out" }, 2.35);')
for t, nxt in zip(PUNCH, PUNCH[1:] + [88.3]):
    relax = max(0.8, nxt - t - 0.65)
    tl.append(f'tl.to("#vz", {{ scale: 1.095, duration: .45, ease: "power2.out" }}, {j(t)});')
    tl.append(f'tl.to("#vz", {{ scale: 1.035, duration: {j(relax)}, ease: "sine.inOut" }}, {j(t + .55)});')

tl_fixed = """
      tl.fromTo("#tagin", { y: -40, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "power3.out" }, 0.08);
      tl.fromTo("#hsub", { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .45, ease: "power2.out" }, 0.22);
      tl.fromTo("#hmain .ltr", { opacity: 0, y: 14, filter: "blur(6px)" },
                { opacity: 1, y: 0, filter: "blur(0px)", duration: .4, ease: "power2.out", stagger: .04 }, 0.38);
      tl.fromTo("#hl", { scaleX: 0 }, { scaleX: 1, duration: .45, ease: "power3.inOut" }, 0.95);
      tl.fromTo("#hd1, #hd2", { scale: 0 }, { scale: 1, duration: .35, ease: "back.out(2)", stagger: .08 }, 1.15);
      tl.fromTo("#widgetin", { y: 90, opacity: 0, scale: .88 }, { y: 0, opacity: 1, scale: 1, duration: .6, ease: "back.out(1.35)" }, 0.55);
      tl.to("#widgetin", { y: -10, duration: 1.3, ease: "sine.inOut" }, 1.2);
      tl.to("#introin", { opacity: 0, scale: 1.035, duration: .45, ease: "power2.inOut" }, 2.28);
      tl.fromTo("#wf", { opacity: 1 }, { opacity: 0, duration: .75, ease: "power2.out" }, 2.42);

      tl.fromTo("#bannerin", { y: -260, opacity: 0, scale: .96 }, { y: 0, opacity: 1, scale: 1, duration: .6, ease: "back.out(1.2)" }, 9.95);
      tl.to("#bannerin", { y: -14, duration: 1.3, ease: "sine.inOut" }, 10.6);
      tl.to("#bannerin", { y: -260, opacity: 0, duration: .4, ease: "power3.in" }, 12.6);

      tl.fromTo("#payin", { scale: .4, opacity: 0 }, { scale: 1, opacity: 1, duration: .55, ease: "back.out(1.9)" }, 17.2);
      tl.fromTo("#paydone .p-check", { scale: 0, rotation: -40 }, { scale: 1, rotation: 0, duration: .45, ease: "back.out(2.4)" }, 17.38);
      tl.to("#payin", { scale: .9, opacity: 0, duration: .22, ease: "power2.in" }, 19.3);

      tl.fromTo("#endbg", { opacity: 0 }, { opacity: 1, duration: .6, ease: "power2.inOut" }, 88.1);
      tl.fromTo("#esub", { y: 26, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power2.out" }, 88.6);
      tl.fromTo("#elogo", { yPercent: 115 }, { yPercent: 0, duration: .55, ease: "power4.out" }, 88.72);
      tl.fromTo("#eline", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power2.out" }, 89.0);
      tl.fromTo("#epill", { scale: .7, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, ease: "back.out(1.6)" }, 89.15);
"""

page = f"""<!doctype html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <!-- Generated by edit/build_tour.py — edit that script, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <style>{css}{extra_css}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{j(DUR)}" data-width="1080" data-height="1920">

      <div id="vid" class="vidwrap">
        <div class="vidzoom" id="vz">
          <video id="aroll" class="clip" src="assets/tour.mp4" playsinline muted data-start="0" data-duration="{j(VID_END)}" data-track-index="0"></video>
        </div>
      </div>
      <div class="grad"></div>
      <div id="wf" class="clip whitefade" data-start="2.3" data-duration="1.1" data-track-index="1"></div>

      <div id="intro" class="clip intro" data-start="0" data-duration="2.75" data-track-index="3">
        <div class="intro-in" id="introin">
          <div class="tag"><div class="tag-in" id="tagin"><i></i><b>MEDA</b><span>&middot;</span>Toshkent</div></div>
          <div class="hgroup">
            <div class="hsub" id="hsub">Xush kelibsiz!</div>
            <div class="hrow"><div class="hmain" id="hmain"><span class="hl" id="hl"></span><i class="hdot hd1" id="hd1"></i><i class="hdot hd2" id="hd2"></i></div></div>
          </div>
          <div class="widget" id="widget">
            <div class="widget-in" id="widgetin">
              <img src="assets/office.jpg" alt="" />
              <div class="wcap"><b>Rasmiy ofis</b> &middot; Toshkent</div>
            </div>
          </div>
        </div>
      </div>

      <div id="banner" class="clip banner" data-start="9.9" data-duration="3.2" data-track-index="2">
        <div class="banner-in" id="bannerin">
          <div class="b-icon">M</div>
          <div class="b-body"><div class="b-title">Savol</div><div class="b-text">Sizning ofisingiz bormi?</div></div>
          <div class="b-time">hozir</div>
        </div>
      </div>

      <div id="paydone" class="clip paydone" data-start="17.15" data-duration="2.4" data-track-index="3">
        <div class="pay-in" id="payin"><div class="p-check">&#10003;</div><span>Rasmiy sertifikatlar</span></div>
      </div>

      {chr(10).join('      ' + c for c in clips)}

      <div id="end" class="clip endcard" data-start="88.05" data-duration="{j(DUR - 88.05)}" data-track-index="5">
        <div class="end-bg" id="endbg"></div>
        <div class="end-in">
          <div class="end-sub" id="esub">Xalqaro assotsiatsiya</div>
          <div class="end-logo-mask"><div class="end-logo" id="elogo">MEDA</div></div>
          <div class="end-line" id="eline">Toshkent&nbsp;&middot;&nbsp;rasmiy ofis</div>
          <div class="end-pill" id="epill">Batafsil&nbsp;&mdash;&nbsp;profilda</div>
        </div>
      </div>
    </div>

    <script>
      const word = "MEDA ofisi";
      const hmain = document.getElementById("hmain");
      for (const ch of word) {{
        const s = document.createElement("span");
        s.className = "ltr";
        s.textContent = ch;
        hmain.appendChild(s);
      }}

      const tl = gsap.timeline({{ paused: true }});
{tl_fixed}
      {chr(10).join('      ' + l for l in tl)}

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(page)
print(f"index.html: {len(clips) + 5} clips, duration {DUR}s")
