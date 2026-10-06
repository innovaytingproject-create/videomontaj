#!/usr/bin/env python3
"""Generate index.html: cut footage + Russian subtitles + brand graphics, all timed in output seconds."""
import html, json, re
from pathlib import Path

import script as S

ROOT = Path(__file__).resolve().parents[1]
pieces = json.load(open(Path(__file__).with_name("pieces.json")))
for p in pieces:
    p["out_end"] = p["out_start"] + p["src_out"] - p["src_in"]
CUT_LEN = pieces[-1]["out_end"]


def out(t, is_end=False):
    """Map a source time to output time; times inside removed stretches snap to the nearest kept edge."""
    for p in pieces:
        if p["src_in"] <= t <= p["src_out"]:
            return p["out_start"] + t - p["src_in"]
    if is_end:
        return max((p["out_end"] for p in pieces if p["src_out"] <= t), default=0.0)
    return min((p["out_start"] for p in pieces if p["src_in"] >= t), default=CUT_LEN)


def rich(text):
    """*word* → orange highlight; every word wrapped for the pop-in stagger."""
    parts = re.split(r"(\*[^*]+\*)", text)
    words = []
    for part in parts:
        hot = part.startswith("*")
        for w in part.strip("*").split():
            cls = "w hot" if hot else "w"
            words.append(f'<span class="{cls}">{html.escape(w)}</span>')
    return " ".join(words)


r = lambda x: f"{x:.3f}"
END = CUT_LEN + S.END_TAIL
clips, tl = [], []

# Subtitles (one track) and hook titles.
for i, (a, b, kind, text) in enumerate(S.CAPTIONS):
    s, e = out(a), out(b, True)
    if e - s < 0.2 or kind == "skip":
        continue
    if kind == "cap":
        clips.append(f'<div id="cap{i}" class="clip cap" data-start="{r(s)}" data-duration="{r(e - s)}" data-track-index="5">'
                     f'<p class="cap-in">{rich(text)}</p></div>')
        tl.append(f'tl.fromTo("#cap{i} .w", {{y: 26, opacity: 0, scale: .92}}, {{y: 0, opacity: 1, scale: 1, duration: .26, ease: "back.out(2.2)", stagger: .045}}, {r(s)});')

# Hook title 1: "Любите массаж?" as two slabs.
s, e = out(0.0), out(2.9, True)
clips.append(f'<div id="t1" class="clip title" data-start="{r(s)}" data-duration="{r(e - s + .25)}" data-track-index="4">'
             '<div class="slab dark"><span>Massajni</span></div><div class="slab orange tilt"><span>sevasizmi?</span></div></div>')
tl.append(f'tl.fromTo("#t1 .slab", {{scaleX: 0}}, {{scaleX: 1, duration: .38, ease: "expo.out", stagger: .16}}, {r(s + .05)});')
tl.append(f'tl.fromTo("#t1 .slab span", {{yPercent: 110}}, {{yPercent: 0, duration: .42, ease: "back.out(1.8)", stagger: .16}}, {r(s + .2)});')
tl.append(f'tl.to("#t1 .slab", {{xPercent: -120, duration: .3, ease: "power3.in", stagger: .06}}, {r(e - .1)});')

# Product name tag.
s, e = out(S.PRODUCT_TAG[0]), out(S.PRODUCT_TAG[1], True)
clips.append(f'<div id="tag" class="clip tag" data-start="{r(s)}" data-duration="{r(e - s + .3)}" data-track-index="3">'
             '<div class="tag-in"><span class="logo">FOHERB</span><span class="tag-sep"></span><span>Biomassajyor</span></div></div>')
tl.append(f'tl.fromTo("#tag .tag-in", {{x: -80, opacity: 0}}, {{x: 0, opacity: 1, duration: .45, ease: "expo.out"}}, {r(s)});')
tl.append(f'tl.to("#tag .tag-in", {{x: -60, opacity: 0, duration: .25, ease: "power2.in"}}, {r(e)});')

# Hook title 2: "Это просто ЧУДО" with sparkles.
s, e = out(11.30), out(13.15, True)
clips.append(f'<div id="t2" class="clip title" data-start="{r(s)}" data-duration="{r(e - s)}" data-track-index="4">'
             '<div class="slab dark small"><span>Bu shunchaki</span></div><div class="miracle">mo’jiza'
             '<i class="spark s1"></i><i class="spark s2"></i><i class="spark s3"></i></div></div>')
tl.append(f'tl.fromTo("#t2 .slab", {{scaleX: 0}}, {{scaleX: 1, duration: .3, ease: "expo.out"}}, {r(s)});')
tl.append(f'tl.fromTo("#t2 .slab span", {{yPercent: 110}}, {{yPercent: 0, duration: .35, ease: "back.out(1.8)"}}, {r(s + .1)});')
tl.append(f'tl.fromTo("#t2 .miracle", {{scale: .3, opacity: 0, rotation: -8}}, {{scale: 1, opacity: 1, rotation: -3, duration: .55, ease: "back.out(2.6)"}}, {r(s + .22)});')
tl.append(f'tl.fromTo("#t2 .spark", {{scale: 0, rotation: -90}}, {{scale: 1, rotation: 0, duration: .5, ease: "back.out(3)", stagger: .09}}, {r(s + .45)});')
tl.append(f'tl.to("#t2 .spark", {{rotation: 90, duration: 1.4, ease: "none"}}, {r(s + .95)});')
tl.append(f'tl.to("#t2 .miracle, #t2 .slab", {{scale: .8, opacity: 0, duration: .22, ease: "power2.in"}}, {r(e - .24)});')

# Numbered block chips.
for i, (a, num, label) in enumerate(S.CHIPS):
    s = out(a)
    d = 3.0
    clips.append(f'<div id="chip{i}" class="clip chip" data-start="{r(s)}" data-duration="{r(d)}" data-track-index="3">'
                 f'<div class="chip-in"><b>{num}</b><span>{html.escape(label)}</span></div></div>')
    tl.append(f'tl.fromTo("#chip{i} .chip-in", {{xPercent: -110}}, {{xPercent: 0, duration: .5, ease: "expo.out"}}, {r(s)});')
    tl.append(f'tl.fromTo("#chip{i} b", {{scale: 0}}, {{scale: 1, duration: .4, ease: "back.out(3)"}}, {r(s + .2)});')
    tl.append(f'tl.to("#chip{i} .chip-in", {{xPercent: -110, duration: .32, ease: "power3.in"}}, {r(s + d - .34)});')

# Big "5".
s, e = out(S.BIG_FIVE[0]), out(S.BIG_FIVE[1], True)
clips.append(f'<div id="five" class="clip five" data-start="{r(s)}" data-duration="{r(e - s + .5)}" data-track-index="4">'
             '<div class="five-in"><span class="five-n">5</span><span class="five-l">funksiya</span></div></div>')
tl.append(f'tl.fromTo("#five .five-n", {{scale: 2.4, opacity: 0}}, {{scale: 1, opacity: 1, duration: .45, ease: "expo.out"}}, {r(s)});')
tl.append(f'tl.fromTo("#five .five-l", {{y: 40, opacity: 0}}, {{y: 0, opacity: 1, duration: .35, ease: "power3.out"}}, {r(s + .2)});')
tl.append(f'tl.to("#five .five-in", {{scale: .85, opacity: 0, duration: .3, ease: "power2.in"}}, {r(e + .2)});')

# Function pills, revealed as she names them.
fend = out(S.FUNC_END, True)
for i, (a, label) in enumerate(S.FUNCS):
    s = out(a)
    clips.append(f'<div id="fn{i}" class="clip fn fn{i}" data-start="{r(s)}" data-duration="{r(fend - s + .4)}" data-track-index="3">'
                 f'<div class="fn-in"><i></i><span>{html.escape(label)}</span></div></div>')
    tl.append(f'tl.fromTo("#fn{i} .fn-in", {{x: -60, opacity: 0, scale: .9}}, {{x: 0, opacity: 1, scale: 1, duration: .4, ease: "back.out(2)"}}, {r(s)});')
    tl.append(f'tl.to("#fn{i} .fn-in", {{x: -40, opacity: 0, duration: .25, ease: "power2.in"}}, {r(fend + .1 + i * .05)});')

# Stat card "1 = 10".
s, e = out(S.STAT[0]), out(S.STAT[1], True)
d = e - s
clips.append(f'<div id="stat" class="clip stat" data-start="{r(s)}" data-duration="{r(d)}" data-track-index="4">'
             '<div class="stat-in"><div class="stat-row"><span class="stat-1">1</span><span class="stat-eq">=</span>'
             '<span class="stat-10" id="statnum">10</span></div>'
             '<div class="stat-l1">biomassajyor</div><div class="stat-l2">o’nta qo’l massaji o’rnini bosadi</div></div></div>')
tl.append(f'tl.fromTo("#stat .stat-in", {{y: 120, opacity: 0}}, {{y: 0, opacity: 1, duration: .5, ease: "expo.out"}}, {r(s)});')
tl.append(f'tl.fromTo("#stat .stat-1, #stat .stat-eq", {{scale: 0}}, {{scale: 1, duration: .4, ease: "back.out(2.5)", stagger: .1}}, {r(s + .15)});')
tl.append(f'tl.fromTo(counter, {{v: 1}}, {{v: 10, duration: 1.1, ease: "power2.out", onUpdate: () => {{ document.getElementById("statnum").textContent = Math.round(counter.v); }}}}, {r(s + .35)});')
tl.append(f'tl.fromTo("#stat .stat-10", {{scale: .6}}, {{scale: 1, duration: 1.1, ease: "power2.out"}}, {r(s + .35)});')
tl.append(f'tl.fromTo("#stat .stat-l1, #stat .stat-l2", {{y: 30, opacity: 0}}, {{y: 0, opacity: 1, duration: .35, stagger: .12, ease: "power3.out"}}, {r(s + .55)});')
tl.append(f'tl.to("#stat .stat-in", {{y: 80, opacity: 0, duration: .3, ease: "power2.in"}}, {r(s + d - .32)});')

# CTA slab, then the end card.
s = out(S.CTA_START)
ecs = out(194.35)
clips.append(f'<div id="cta" class="clip title cta" data-start="{r(s)}" data-duration="{r(ecs - s)}" data-track-index="4">'
             '<div class="slab dark small"><span>Fiziokabinet</span></div><div class="slab orange tilt"><span>ochmoqchimisiz?</span></div></div>')
tl.append(f'tl.fromTo("#cta .slab", {{scaleX: 0}}, {{scaleX: 1, duration: .4, ease: "expo.out"}}, {r(s)});')
tl.append(f'tl.fromTo("#cta .slab span", {{yPercent: 110}}, {{yPercent: 0, duration: .4, ease: "back.out(1.8)"}}, {r(s + .15)});')
clips.append(f'<div id="end" class="clip endcard" data-start="{r(ecs)}" data-duration="{r(END - ecs)}" data-track-index="6">'
             '<div class="end-bg"></div><div class="end-in"><div class="end-rec">Tavsiya qilaman!</div>'
             '<div class="end-logo">FOHERB</div><div class="end-line"></div><div class="end-sub">Biomassajyor · 5 funksiya</div></div></div>')
tl.append(f'tl.fromTo("#end .end-bg", {{clipPath: "inset(100% 0 0 0)"}}, {{clipPath: "inset(0% 0 0 0)", duration: .55, ease: "expo.inOut"}}, {r(ecs)});')
tl.append(f'tl.fromTo("#end .end-rec", {{y: 60, opacity: 0}}, {{y: 0, opacity: 1, duration: .45, ease: "back.out(2)"}}, {r(ecs + .3)});')
tl.append(f'tl.fromTo("#end .end-logo", {{scale: 1.35, opacity: 0}}, {{scale: 1, opacity: 1, duration: .7, ease: "expo.out"}}, {r(ecs + .5)});')
tl.append(f'tl.fromTo("#end .end-line", {{scaleX: 0}}, {{scaleX: 1, duration: .5, ease: "expo.out"}}, {r(ecs + .8)});')
tl.append(f'tl.fromTo("#end .end-sub", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: .4, ease: "power3.out"}}, {r(ecs + .95)});')

page = (ROOT / "edit" / "template.html").read_text()
page = page.replace("{{DURATION}}", r(END)).replace("{{CUT_LEN}}", r(CUT_LEN))
page = page.replace("{{CLIPS}}", "\n      ".join(clips)).replace("{{TIMELINE}}", "\n      ".join(tl))
(ROOT / "index.html").write_text(page)
print(f"index.html: {len(clips)} clips, duration {END:.2f}s")
