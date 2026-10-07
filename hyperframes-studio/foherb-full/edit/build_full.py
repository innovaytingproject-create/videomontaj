#!/usr/bin/env python3
"""Generate the full 3:17 Apple-style composition from the approved 15s test.

Style (CSS + intro/banner/paydone/mojiza/end blocks) is lifted verbatim from
../foherb-15s-apple/index.html; captions come from foherb-reel/edit/script.py.
No cuts: source time == output time.
"""
import html, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APPLE15 = (ROOT.parent / "foherb-15s-apple" / "index.html").read_text()
sys.path.insert(0, str(ROOT.parent / "foherb-reel" / "edit"))
from script import CAPTIONS  # noqa: E402

DUR = 198.0
VID_END = 197.1
j = lambda t: f"{t:.2f}"

# ---------- style: reuse the approved CSS, add full-video blocks ----------
css = re.search(r"<style>(.*?)</style>", APPLE15, re.S).group(1)
extra_css = """
      /* ---------- section pills ---------- */
      .sec { position: absolute; top: 150px; left: 0; right: 0; display: flex; justify-content: center; }
      .sec-in { display: flex; align-items: center; gap: 22px; background: rgba(250,252,255,.96); border-radius: 60px;
                padding: 16px 40px 16px 18px; box-shadow: 0 18px 50px rgba(7,20,40,.3); }
      .sec-in b { width: 68px; height: 68px; border-radius: 22px; flex: none; display: flex; align-items: center; justify-content: center;
                  background: linear-gradient(150deg, #3f9bff, #0a62e0); color: #fff; font-weight: 800; font-size: 32px; }
      .sec-in span { font-weight: 700; font-size: 36px; color: var(--ink); }

      /* ---------- "5 funksiya" widget ---------- */
      .fivew { position: absolute; left: 0; right: 0; top: 540px; display: flex; justify-content: center; }
      .fivew-in { background: linear-gradient(160deg, #ffffff 0%, var(--tint) 100%); border-radius: 64px;
                  padding: 46px 110px 54px; text-align: center;
                  box-shadow: 0 40px 90px rgba(29,55,97,.18), 0 8px 24px rgba(29,55,97,.08); }
      .f-num { font-weight: 900; font-size: 290px; line-height: .95; color: var(--blue); letter-spacing: -0.02em; }
      .f-lab { margin-top: 2px; font-weight: 600; font-size: 46px; color: var(--gray); }

      /* ---------- function pills ---------- */
      .fnp { position: absolute; left: 60px; }
      .fnp0 { top: 830px; } .fnp1 { top: 962px; } .fnp2 { top: 1094px; }
      .fnp-in { display: flex; align-items: center; gap: 20px; background: rgba(250,252,255,.96); border-radius: 60px;
                padding: 20px 40px; box-shadow: 0 16px 44px rgba(7,20,40,.3); }
      .fnp-in i { display: block; width: 16px; height: 16px; border-radius: 50%; background: var(--blue); }
      .fnp-in span { font-weight: 700; font-size: 38px; color: var(--ink); }

      /* ---------- 1 = 10 stat card ---------- */
      .statc { position: absolute; left: 0; right: 0; top: 960px; display: flex; justify-content: center; }
      .statc-in { background: rgba(250,252,255,.97); border-radius: 56px; padding: 38px 84px 46px; text-align: center;
                  box-shadow: 0 36px 80px rgba(7,20,40,.32); }
      .s-row { display: flex; align-items: center; justify-content: center; gap: 30px;
               font-weight: 900; font-size: 190px; line-height: 1.05; color: var(--ink); letter-spacing: -0.02em; }
      .s-eq { color: var(--blue); font-size: 130px; }
      .s-ten { color: var(--blue); min-width: 225px; text-align: center; }
      .s-lab { margin-top: 8px; font-weight: 600; font-size: 38px; color: var(--gray); }
"""

# ---------- reuse approved markup blocks ----------
body = re.search(r'(<div id="root".*?)\n    </div>\n\n    <script>', APPLE15, re.S).group(1)
blocks = {}
for bid in ("intro", "banner", "paydone", "mojiza", "end"):
    m = re.search(r'(<div id="%s" class="clip.*?)\n\n      <div id="' % bid, body + '\n\n      <div id="', re.S)
    blocks[bid] = m.group(1)
# End card moves to the tail of the full video.
blocks["end"] = blocks["end"].replace('data-start="13.05" data-duration="2.35"',
                                      f'data-start="{j(196.0)}" data-duration="{j(DUR - 196.0)}"')

clips, tl = [], []


def rich(text):
    parts = re.split(r"(\*[^*]+\*)", text)
    out = []
    for part in parts:
        hot = part.startswith("*")
        for w in part.strip("*").split():
            out.append(f'<span class="w{" hot" if hot else ""}">{html.escape(w)}</span>')
    return " ".join(out)


# Captions (kind "cap" only — titles are dedicated Apple cards).
for i, (a, b, kind, text) in enumerate(CAPTIONS):
    if kind != "cap":
        continue
    clips.append(f'<div id="cap{i}" class="clip cap" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="4">'
                 f'<p class="cap-card">{rich(text)}</p></div>')
    tl.append(f'tl.fromTo("#cap{i} .cap-card", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .4, ease: "power3.out" }}, {j(a)});')
    tl.append(f'tl.fromTo("#cap{i} .w", {{ opacity: 0 }}, {{ opacity: 1, duration: .25, ease: "power1.out", stagger: .04 }}, {j(a + .08)});')
    tl.append(f'tl.to("#cap{i} .cap-card", {{ y: 24, opacity: 0, duration: .25, ease: "power2.in" }}, {j(b - .28)});')

# Section pills.
SECTIONS = [(18.8, "01", "O’zingiz bilan oling"), (47.3, "02", "Kumush qo’lqoplar"),
            (97.6, "03", "Biomassajyor"), (136.1, "04", "Quloq va burun"), (165.2, "05", "Tomirlar uchun")]
for n, (a, num, label) in enumerate(SECTIONS):
    clips.append(f'<div id="sec{n}" class="clip sec" data-start="{j(a)}" data-duration="3.0" data-track-index="2">'
                 f'<div class="sec-in"><b>{num}</b><span>{html.escape(label)}</span></div></div>')
    tl.append(f'tl.fromTo("#sec{n} .sec-in", {{ y: -150, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .5, ease: "back.out(1.2)" }}, {j(a)});')
    tl.append(f'tl.to("#sec{n} .sec-in", {{ y: -130, opacity: 0, duration: .3, ease: "power3.in" }}, {j(a + 2.65)});')

# "5 funksiya" widget.
clips.append('<div id="fivew" class="clip fivew" data-start="112.35" data-duration="3.15" data-track-index="2">'
             '<div class="fivew-in" id="fivein"><div class="f-num">5</div><div class="f-lab">funksiya</div></div></div>')
tl.append('tl.fromTo("#fivein", { scale: .6, opacity: 0, y: 40 }, { scale: 1, opacity: 1, y: 0, duration: .55, ease: "back.out(1.4)" }, 112.4);')
tl.append('tl.to("#fivein", { y: -10, duration: 2.0, ease: "sine.inOut" }, 113.0);')
tl.append('tl.to("#fivein", { scale: .92, opacity: 0, duration: .3, ease: "power2.in" }, 115.15);')

# Function pills.
FUNCS = [(123.2, "Impuls massaj"), (126.3, "Guasha"), (127.9, "Quruq hijoma")]
for n, (a, label) in enumerate(FUNCS):
    clips.append(f'<div id="fnp{n}" class="clip fnp fnp{n}" data-start="{j(a)}" data-duration="{j(130.2 - a)}" data-track-index="2">'
                 f'<div class="fnp-in"><i></i><span>{html.escape(label)}</span></div></div>')
    tl.append(f'tl.fromTo("#fnp{n} .fnp-in", {{ x: -90, opacity: 0 }}, {{ x: 0, opacity: 1, duration: .45, ease: "back.out(1.6)" }}, {j(a)});')
    tl.append(f'tl.to("#fnp{n} .fnp-in", {{ x: -70, opacity: 0, duration: .25, ease: "power2.in" }}, {j(129.85 + n * .05)});')

# 1 = 10 stat card with count-up.
clips.append('<div id="statc" class="clip statc" data-start="144.2" data-duration="5.2" data-track-index="2">'
             '<div class="statc-in" id="statin"><div class="s-row"><span>1</span><span class="s-eq">=</span>'
             '<span class="s-ten" id="statnum">10</span></div>'
             '<div class="s-lab">bitta biomassajyor &mdash; o&#8217;nta qo&#8217;l massaji</div></div></div>')
tl.append('tl.fromTo("#statin", { y: 70, opacity: 0, scale: .9 }, { y: 0, opacity: 1, scale: 1, duration: .5, ease: "back.out(1.3)" }, 144.25);')
tl.append('tl.fromTo(counter, { v: 1 }, { v: 10, duration: 1.0, ease: "power2.out", onUpdate: () => { document.getElementById("statnum").textContent = Math.round(counter.v); } }, 144.5);')
tl.append('tl.to("#statin", { y: 50, opacity: 0, duration: .3, ease: "power2.in" }, 149.05);')

# Living camera: gentle drift with soft pushes at story beats.
PUNCH = [11.3, 18.8, 47.3, 97.6, 112.35, 123.1, 136.1, 144.2, 165.2, 183.0]
tl.append('tl.fromTo("#vz", { scale: 1.12 }, { scale: 1.035, duration: 1.0, ease: "power2.out" }, 2.35);')
for t, nxt in zip(PUNCH, PUNCH[1:] + [196.0]):
    relax = max(0.8, nxt - t - 0.65)
    tl.append(f'tl.to("#vz", {{ scale: 1.095, duration: .45, ease: "power2.out" }}, {j(t)});')
    tl.append(f'tl.to("#vz", {{ scale: 1.035, duration: {j(relax)}, ease: "sine.inOut" }}, {j(t + .55)});')

# Intro, banner, paydone, mojiza tweens — same values as the approved 15s.
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

      tl.fromTo("#bannerin", { y: -260, opacity: 0, scale: .96 }, { y: 0, opacity: 1, scale: 1, duration: .6, ease: "back.out(1.2)" }, 5.4);
      tl.to("#bannerin", { y: -14, duration: 1.5, ease: "sine.inOut" }, 6.05);
      tl.to("#bannerin", { y: -260, opacity: 0, duration: .4, ease: "power3.in" }, 7.85);

      tl.fromTo("#payin", { scale: .4, opacity: 0 }, { scale: 1, opacity: 1, duration: .55, ease: "back.out(1.9)" }, 9.0);
      tl.fromTo("#paydone .p-check", { scale: 0, rotation: -40 }, { scale: 1, rotation: 0, duration: .45, ease: "back.out(2.4)" }, 9.18);
      tl.to("#payin", { scale: .9, opacity: 0, duration: .22, ease: "power2.in" }, 10.7);

      tl.fromTo("#mjcard", { scale: .82, opacity: 0, y: 40 }, { scale: 1, opacity: 1, y: 0, duration: .55, ease: "back.out(1.45)" }, 11.34);
      tl.to("#mjcard", { scale: .94, opacity: 0, duration: .25, ease: "power2.in" }, 12.78);

      tl.fromTo("#endbg", { opacity: 0 }, { opacity: 1, duration: .6, ease: "power2.inOut" }, 196.0);
      tl.fromTo("#esub", { y: 26, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power2.out" }, 196.5);
      tl.fromTo("#elogo", { yPercent: 115 }, { yPercent: 0, duration: .55, ease: "power4.out" }, 196.62);
      tl.fromTo("#eline", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power2.out" }, 196.9);
      tl.fromTo("#epill", { scale: .7, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, ease: "back.out(1.6)" }, 197.05);
"""

page = f"""<!doctype html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <!-- Generated by edit/build_full.py — edit that script, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <style>{css}{extra_css}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{j(DUR)}" data-width="1080" data-height="1920">

      <div id="vid" class="vidwrap">
        <div class="vidzoom" id="vz">
          <video id="aroll" class="clip" src="assets/cutfull.mp4" playsinline muted data-start="0" data-duration="{j(VID_END)}" data-track-index="0"></video>
        </div>
      </div>
      <div class="grad"></div>
      <div id="wf" class="clip whitefade" data-start="2.3" data-duration="1.1" data-track-index="1"></div>

      {blocks['intro']}

      {blocks['banner']}

      {blocks['paydone']}

      {blocks['mojiza']}

      {chr(10).join('      ' + c for c in clips)}

      {blocks['end']}
    </div>

    <script>
      const word = "Sevasizmi?";
      const hmain = document.getElementById("hmain");
      for (const ch of word) {{
        const s = document.createElement("span");
        s.className = "ltr";
        s.textContent = ch;
        hmain.appendChild(s);
      }}

      const tl = gsap.timeline({{ paused: true }});
      const counter = {{ v: 1 }};
{tl_fixed}
      {chr(10).join('      ' + l for l in tl)}

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(page)
print(f"index.html: {len(clips) + 6} clips, {len(tl)} generated tweens, duration {DUR}s")
