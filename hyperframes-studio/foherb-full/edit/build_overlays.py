#!/usr/bin/env python3
"""Build standalone overlay compositions for the client's own editing.

Each insert gets its own HTML: entrance animation, then a hold (no exit) so the
clip can be trimmed/extended freely. Keyable items sit on pure green #00FF00
with shadows stripped (clean chroma key); intro/end keep their own backgrounds.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "overlays"
OUT.mkdir(exist_ok=True)

css = re.search(r"<style>(.*?)</style>", (ROOT / "index.html").read_text(), re.S).group(1)
# For keyed overlays: kill shadows (they key badly) and the footage gradient.
GREEN_EXTRA = """
      html, body { background: #00ff00 !important; }
      #root { background: #00ff00; }
      * { box-shadow: none !important; text-shadow: none !important; }
"""

A = "’"

ITEMS = {}  # name -> (green, duration, body_html, timeline_js)

ITEMS["banner"] = (True, 3.0, '''
      <div class="banner" style="top:150px"><div class="banner-in" id="el">
        <div class="b-icon">F</div>
        <div class="b-body"><div class="b-title">FOHERB</div><div class="b-text">Biomassajyor &mdash; yangi xarid</div></div>
        <div class="b-time">hozir</div>
      </div></div>''', '''
      tl.fromTo("#el", { y: -260, opacity: 0, scale: .96 }, { y: 0, opacity: 1, scale: 1, duration: .6, ease: "back.out(1.2)" }, 0.25);''')

ITEMS["paydone"] = (True, 2.4, '''
      <div class="paydone" style="top:900px"><div class="pay-in" id="el"><div class="p-check">&#10003;</div><span>Xarid qilindi</span></div></div>''', '''
      tl.fromTo("#el", { scale: .4, opacity: 0 }, { scale: 1, opacity: 1, duration: .55, ease: "back.out(1.9)" }, 0.25);
      tl.fromTo(".p-check", { scale: 0, rotation: -40 }, { scale: 1, rotation: 0, duration: .45, ease: "back.out(2.4)" }, 0.43);''')

ITEMS["mojiza"] = (True, 2.2, '''
      <div class="mojiza" style="top:860px"><div class="mj-card" id="el">
        <div class="mj-sub">bu shunchaki</div>
        <div class="mj-main">Mo&#8217;jiza<em>.</em></div>
      </div></div>''', '''
      tl.fromTo("#el", { scale: .82, opacity: 0, y: 40 }, { scale: 1, opacity: 1, y: 0, duration: .55, ease: "back.out(1.45)" }, 0.25);''')

SECTIONS = [("01", f"O{A}zingiz bilan oling"), ("02", f"Kumush qo{A}lqoplar"),
            ("03", "Biomassajyor"), ("04", "Quloq va burun"), ("05", "Tomirlar uchun")]
for num, label in SECTIONS:
    ITEMS[f"section-{num}"] = (True, 2.6, f'''
      <div class="sec" style="top:150px"><div class="sec-in" id="el"><b>{num}</b><span>{label}</span></div></div>''', '''
      tl.fromTo("#el", { y: -150, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "back.out(1.2)" }, 0.25);''')

ITEMS["five-funksiya"] = (True, 3.0, '''
      <div class="fivew" style="top:540px"><div class="fivew-in" id="el"><div class="f-num">5</div><div class="f-lab">funksiya</div></div></div>''', '''
      tl.fromTo("#el", { scale: .6, opacity: 0, y: 40 }, { scale: 1, opacity: 1, y: 0, duration: .55, ease: "back.out(1.4)" }, 0.25);''')

for n, label in enumerate(["Impuls massaj", "Guasha", "Quruq hijoma"]):
    ITEMS[f"funksiya-pill-{n+1}"] = (True, 2.0, f'''
      <div class="fnp" style="top:900px"><div class="fnp-in" id="el"><i></i><span>{label}</span></div></div>''', '''
      tl.fromTo("#el", { x: -90, opacity: 0 }, { x: 0, opacity: 1, duration: .45, ease: "back.out(1.6)" }, 0.2);''')

ITEMS["stat-1-10"] = (True, 3.6, f'''
      <div class="statc" style="top:900px"><div class="statc-in" id="el"><div class="s-row"><span>1</span><span class="s-eq">=</span>
        <span class="s-ten" id="statnum">10</span></div>
        <div class="s-lab">bitta biomassajyor &mdash; o{A}nta qo{A}l massaji</div></div></div>''', '''
      tl.fromTo("#el", { y: 70, opacity: 0, scale: .9 }, { y: 0, opacity: 1, scale: 1, duration: .5, ease: "back.out(1.3)" }, 0.25);
      tl.fromTo(counter, { v: 1 }, { v: 10, duration: 1.0, ease: "power2.out", onUpdate: () => { document.getElementById("statnum").textContent = Math.round(counter.v); } }, 0.5);''')

ITEMS["intro-card"] = (False, 3.2, '''
      <div class="intro" style="position:absolute;inset:0"><div class="intro-in" id="introin">
        <div class="tag"><div class="tag-in" id="tagin"><i></i><b>FOHERB</b><span>&middot;</span>Biomassajyor</div></div>
        <div class="hgroup">
          <div class="hsub" id="hsub">Massajni</div>
          <div class="hrow"><div class="hmain" id="hmain"><span class="hl" id="hl"></span><i class="hdot hd1" id="hd1"></i><i class="hdot hd2" id="hd2"></i></div></div>
        </div>
        <div class="widget" id="widget"><div class="widget-in" id="widgetin">
          <img src="../assets/product.jpg" alt="" />
          <div class="wcap"><b>5 funksiya</b> &middot; bitta priborda</div>
        </div></div>
      </div></div>''', '''
      tl.fromTo("#tagin", { y: -40, opacity: 0 }, { y: 0, opacity: 1, duration: .5, ease: "power3.out" }, 0.08);
      tl.fromTo("#hsub", { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .45, ease: "power2.out" }, 0.22);
      tl.fromTo("#hmain .ltr", { opacity: 0, y: 14, filter: "blur(6px)" },
                { opacity: 1, y: 0, filter: "blur(0px)", duration: .4, ease: "power2.out", stagger: .04 }, 0.38);
      tl.fromTo("#hl", { scaleX: 0 }, { scaleX: 1, duration: .45, ease: "power3.inOut" }, 0.95);
      tl.fromTo("#hd1, #hd2", { scale: 0 }, { scale: 1, duration: .35, ease: "back.out(2)", stagger: .08 }, 1.15);
      tl.fromTo("#widgetin", { y: 90, opacity: 0, scale: .88 }, { y: 0, opacity: 1, scale: 1, duration: .6, ease: "back.out(1.35)" }, 0.55);''')

ITEMS["end-card"] = (False, 3.0, '''
      <div class="endcard" style="position:absolute;inset:0"><div class="end-bg" style="opacity:1"></div>
        <div class="end-in">
          <div class="end-sub" id="esub">Tavsiya qilaman</div>
          <div class="end-logo-mask"><div class="end-logo" id="elogo">FOHERB</div></div>
          <div class="end-line" id="eline">Biomassajyor&nbsp;&middot;&nbsp;5 funksiya</div>
          <div class="end-pill" id="epill">Batafsil&nbsp;&mdash;&nbsp;profilda</div>
        </div></div>''', '''
      tl.fromTo("#esub", { y: 26, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power2.out" }, 0.3);
      tl.fromTo("#elogo", { yPercent: 115 }, { yPercent: 0, duration: .55, ease: "power4.out" }, 0.42);
      tl.fromTo("#eline", { y: 22, opacity: 0 }, { y: 0, opacity: 1, duration: .4, ease: "power2.out" }, 0.7);
      tl.fromTo("#epill", { scale: .7, opacity: 0 }, { scale: 1, opacity: 1, duration: .5, ease: "back.out(1.6)" }, 0.85);''')

LETTERS = '''
      const word = "Sevasizmi?";
      const hmain = document.getElementById("hmain");
      if (hmain) for (const ch of word) {
        const s = document.createElement("span");
        s.className = "ltr"; s.textContent = ch; hmain.appendChild(s);
      }'''

for name, (green, dur, body, tween) in ITEMS.items():
    page = f"""<!doctype html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="../vendor/gsap.min.js"></script>
    <style>{css}{GREEN_EXTRA if green else ''}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
{body}
    </div>
    <script>{LETTERS}
      const tl = gsap.timeline({{ paused: true }});
      const counter = {{ v: 1 }};
{tween}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    (OUT / f"{name}.html").write_text(page)

print("overlays:", len(ITEMS))
