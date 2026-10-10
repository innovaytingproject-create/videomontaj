#!/usr/bin/env python3
"""Build a HyperFrames composition (index.html) from projects/<name>/project.json.

Usage:  python3 pipeline/build.py <name> [--until 15]

--until N  builds only the first N seconds (the 15-second sample the client
           approves before the full video). Clips past N are dropped, the end
           card is skipped.

Style = the client-approved "WHIEDA v3" look (template/style.css). Do not
restyle here — change rules in CLAUDE.md first, with the client's approval.
"""
import argparse, html, json, re, shutil, subprocess
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("name")
ap.add_argument("--until", type=float, default=None)
args = ap.parse_args()

P = KIT / "projects" / args.name
cfg = json.loads((P / "project.json").read_text())
video = P / "work" / "video.mp4"
if not video.exists():
    raise SystemExit(f"missing {video} — run pipeline/prepare.py {args.name} first")

VID = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                           capture_output=True, text=True, check=True).stdout.strip())
VID = round(VID - 0.02, 2)
VID = cfg.get("video_duration", VID)  # optional override (exact source length)
SAMPLE = args.until is not None
END = cfg.get("end_card")
DUR = min(args.until, VID) if SAMPLE else (VID + 1.8 if END else VID)
END_AT = VID - 0.75  # end card overlaps the last breath of footage
j = lambda t: f"{t:.2f}"


def within(a, b):
    """Clip [a,b] to the render window; None if it starts after the window."""
    if a >= DUR - 0.05:
        return None
    return a, min(b, DUR)


def rich(text, cls_hot="hot"):
    """*word* -> accent. Returns word-wrapped spans for captions."""
    out = []
    for part in re.split(r"(\*[^*]+\*)", text):
        hot = part.startswith("*")
        for w in part.strip("*").split():
            out.append(f'<span class="w{" " + cls_hot if hot else ""}">{html.escape(w)}</span>')
    return " ".join(out)


def em(text):
    """*word* -> <em>word</em> for plates/cards (escapes the rest)."""
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", html.escape(text))


clips, tl, used_icons = [], [], set()

# ---------- captions ----------
for i, (a, b, text) in enumerate(cfg["captions"]):
    w = within(a, b)
    if not w:
        continue
    a, b = w
    clips.append(f'<div id="c{i}" class="clip cap" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="4"><p class="cap-t">{rich(text)}</p></div>')
    tl.append(f'tl.fromTo("#c{i} .w", {{ y: 26, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .28, ease: "back.out(1.8)", stagger: .05 }}, {j(a)});')
    if b < DUR - .1:
        tl.append(f'tl.to("#c{i} .cap-t", {{ opacity: 0, y: -10, duration: .16, ease: "power2.in" }}, {j(b - .17)});')

# ---------- WHIEDA logo plate (on every mention) ----------
for n, (a, b) in enumerate(cfg.get("logos", [])):
    w = within(a, b)
    if not w:
        continue
    a, b = w
    clips.append(f'<div id="lg{n}" class="clip logo" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="3">'
                 '<div class="logo-in"><img src="assets/whieda-emblem.png" alt="" />'
                 '<div><div class="logo-w">WHIEDA</div><div class="logo-s">XALQARO ASSOTSIATSIYA</div></div></div></div>')
    tl.append(f'tl.fromTo("#lg{n} .logo-in", {{ y: -40, opacity: 0, scale: .88 }}, {{ y: 0, opacity: 1, scale: 1, duration: .5, ease: "back.out(1.6)" }}, {j(a)});')
    tl.append(f'tl.fromTo("#lg{n} img", {{ rotation: -90, scale: .6 }}, {{ rotation: 0, scale: 1, duration: .6, ease: "back.out(1.8)" }}, {j(a + .06)});')
    if b < DUR - .1:
        tl.append(f'tl.to("#lg{n} .logo-in", {{ y: -30, opacity: 0, duration: .25, ease: "power2.in" }}, {j(b - .27)});')

# ---------- cover plate ----------
cv = cfg.get("cover")
if cv and within(cv["start"], cv["end"]):
    a, b = within(cv["start"], cv["end"])
    clips.append(f'<div id="cover" class="clip cover" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="3"><div class="cover-in" id="coverin">'
                 f'<div class="cover-k">{html.escape(cv.get("kicker", "WHIEDA · TOSHKENT"))}</div><div class="cover-t">{em(cv["title"])}</div>'
                 '<div class="cover-line" id="cline"></div></div></div>')
    tl += [f'tl.fromTo("#coverin", {{ y: -40, opacity: 0, scale: .9 }}, {{ y: 0, opacity: 1, scale: 1, duration: .5, ease: "back.out(1.5)" }}, {j(a + .03)});',
           f'tl.fromTo("#cline", {{ scaleX: 0 }}, {{ scaleX: 1, duration: .5, ease: "power3.inOut" }}, {j(a + .4)});']
    if b < DUR - .1:
        tl.append(f'tl.to("#coverin", {{ y: -30, opacity: 0, duration: .26, ease: "power2.in" }}, {j(b - .28)});')

# ---------- iOS-style banners ----------
for n, bn in enumerate(cfg.get("banners", [])):
    w = within(bn["start"], bn["end"])
    if not w:
        continue
    a, b = w
    clips.append(f'<div id="bn{n}" class="clip banner" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="3"><div class="banner-in">'
                 '<div class="b-icon logo-ic"><img src="assets/whieda-emblem.png" alt="" /></div>'
                 f'<div class="b-body"><div class="b-title">{html.escape(bn["title"])}</div><div class="b-text">{html.escape(bn["text"])}</div></div>'
                 '<div class="b-time">hozir</div></div></div>')
    tl.append(f'tl.fromTo("#bn{n} .banner-in", {{ y: -200, opacity: 0, scale: .96 }}, {{ y: 0, opacity: 1, scale: 1, duration: .5, ease: "back.out(1.25)" }}, {j(a + .05)});')
    if b < DUR - .1:
        tl.append(f'tl.to("#bn{n} .banner-in", {{ y: -200, opacity: 0, duration: .32, ease: "power3.in" }}, {j(b - .34)});')

# ---------- pills above the head (check or icon) ----------
for n, pl in enumerate(cfg.get("pills", [])):
    w = within(pl["start"], pl["end"])
    if not w:
        continue
    a, b = w
    ic = pl.get("icon", "check")
    if ic == "check":
        dot = '<div class="dot">&#10003;</div>'
    else:
        used_icons.add(f"{ic}-white.png")
        dot = f'<div class="dot"><img src="assets/icons/{ic}-white.png" alt="" /></div>'
    clips.append(f'<div id="pl{n}" class="clip pill" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="3"><div class="pill-in">{dot}<span>{html.escape(pl["text"])}</span></div></div>')
    tl.append(f'tl.fromTo("#pl{n} .pill-in", {{ y: -150, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .5, ease: "back.out(1.3)" }}, {j(a)});')
    tl.append(f'tl.fromTo("#pl{n} .dot", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: .45, ease: "back.out(2.4)" }}, {j(a + .18)});')
    if b < DUR - .1:
        tl.append(f'tl.to("#pl{n} .pill-in", {{ y: -130, opacity: 0, duration: .3, ease: "power3.in" }}, {j(b - .32)});')

# ---------- iMessage-style quote bubbles ----------
bb = cfg.get("bubbles")
if bb:
    end_b = bb["end"]
    for n, (a, txt) in enumerate(bb["items"][:3]):
        w = within(a, end_b)
        if not w:
            continue
        a, b = w
        clips.append(f'<div id="bb{n}" class="clip bub bub{n}" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="3"><span class="bub-in">{em(txt)}</span></div>')
        tl.append(f'tl.fromTo("#bb{n} .bub-in", {{ scale: .5, opacity: 0, y: 20 }}, {{ scale: 1, opacity: 1, y: 0, duration: .45, ease: "back.out(1.9)" }}, {j(a)});')
        if b < DUR - .1:
            tl.append(f'tl.to("#bb{n} .bub-in", {{ y: -16, opacity: 0, duration: .22, ease: "power2.in" }}, {j(b - .27 + n * .04)});')

# ---------- accent cards (one per 15 s) ----------
cards = cfg.get("cards", [])
for n, cd in enumerate(cards):
    w = within(cd["start"], cd["end"])
    if not w:
        continue
    a, b = w
    parts = cd["big"].split("|")
    num = cd.get("numeric", False)
    masks = "".join(f'<div class="wc-mask"><div class="wc-big{" num" if num else ""}" id="wb{n}_{k}">{em(p)}</div></div>' for k, p in enumerate(parts))
    ico = ""
    if cd.get("icon"):
        used_icons.add(f'{cd["icon"]}-blue.png')
        ico = f'<img class="wc-ico" id="wi{n}" src="assets/icons/{cd["icon"]}-blue.png" alt="" />'
    clips.append(f'<div id="wc{n}" class="clip wcard" data-start="{j(a)}" data-duration="{j(b - a)}" data-track-index="6">'
                 f'<div class="wc-bg" id="wbg{n}"></div><div class="wc-in" id="win{n}"><div class="wc-sub" id="ws{n}">{html.escape(cd["thin"])}</div>{masks}{ico}</div></div>')
    tl.append(f'tl.fromTo("#wbg{n}", {{ opacity: 0 }}, {{ opacity: 1, duration: .3, ease: "power2.out" }}, {j(a)});')
    tl.append(f'tl.fromTo("#ws{n}", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .38, ease: "power2.out" }}, {j(a + .16)});')
    for k in range(len(parts)):
        tl.append(f'tl.fromTo("#wb{n}_{k}", {{ yPercent: 115 }}, {{ yPercent: 0, duration: .5, ease: "power4.out" }}, {j(a + .26 + k * .16)});')
    if ico:
        tl.append(f'tl.fromTo("#wi{n}", {{ scale: 0, rotation: -12 }}, {{ scale: 1, rotation: 0, duration: .5, ease: "back.out(2)" }}, {j(a + .6)});')
        tl.append(f'tl.to("#wi{n}", {{ y: -10, duration: {j(max(.6, b - a - 1.4))}, ease: "sine.inOut" }}, {j(a + 1.1)});')
    if b < DUR - .1:
        tl.append(f'tl.to("#win{n}", {{ opacity: 0, scale: 1.04, filter: "blur(8px)", duration: .3, ease: "power2.in" }}, {j(b - .32)});')
        tl.append(f'tl.to("#wbg{n}", {{ opacity: 0, duration: .3, ease: "power2.in" }}, {j(b - .32)});')

# ---------- end card ----------
if END and not SAMPLE:
    a = END_AT
    clips.append(f'<div id="end" class="clip endcard" data-start="{j(a)}" data-duration="{j(DUR - a)}" data-track-index="7">'
                 '<div class="end-bg" id="ebg"></div><div class="end-in">'
                 '<img id="eimg" src="assets/whieda-emblem.png" alt="" /><div class="wc-mask"><div class="end-logo" id="elogo">WHIEDA</div></div>'
                 f'<div class="end-sub" id="esub">{html.escape(END["sub"])}</div>'
                 f'<div class="end-pill" id="epill">{html.escape(END["pill"])}</div></div></div>')
    tl += [f'tl.fromTo("#ebg", {{ opacity: 0 }}, {{ opacity: 1, duration: .4, ease: "power2.out" }}, {j(a)});',
           f'tl.fromTo("#eimg", {{ scale: .5, rotation: -90, opacity: 0 }}, {{ scale: 1, rotation: 0, opacity: 1, duration: .6, ease: "back.out(1.7)" }}, {j(a + .2)});',
           f'tl.fromTo("#elogo", {{ yPercent: 115 }}, {{ yPercent: 0, duration: .55, ease: "power4.out" }}, {j(a + .45)});',
           f'tl.fromTo("#esub", {{ y: 22, opacity: 0 }}, {{ y: 0, opacity: 1, duration: .4, ease: "power2.out" }}, {j(a + .75)});',
           f'tl.fromTo("#epill", {{ scale: .7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: .5, ease: "back.out(1.6)" }}, {j(a + .95)});']

# ---------- camera: transition every N s, alternate push-in / pull-out ----------
EVERY = cfg.get("transition_every", 7)
cam_end = min(VID, DUR)
trans = [t for t in range(EVERY, int(cam_end - 1), EVERY)
         if all(not (c["start"] - 0.8 <= t <= c["end"] + 0.3) for c in cards)]
if cfg.get("transitions") is not None:  # explicit list overrides the every-N rule
    trans = [t for t in cfg["transitions"] if t < cam_end - 1]
marks = [0.0] + trans + [cam_end]
tl.append('tl.fromTo("#cam", { scale: 1.0, rotation: 0, filter: "blur(0px)" }, { scale: 1.0, duration: .01 }, 0);')
zoom_in = True
for k in range(len(marks) - 1):
    a, b = marks[k], marks[k + 1]
    start = a + (0.32 if k else 0)
    target = 1.14 if zoom_in else 1.0
    land = 1.04 if zoom_in else 1.2
    if k:
        tl.append(f'tl.fromTo("#cam", {{ scale: {land + .22:.2f}, rotation: {(-2.5 if k % 2 else 2.5)}, filter: "blur(18px)" }}, '
                  f'{{ scale: {land:.2f}, rotation: 0, filter: "blur(0px)", duration: .32, ease: "expo.out", immediateRender: false }}, {j(a)});')
    out_t = b - 0.18 if b < cam_end else b
    tl.append(f'tl.to("#cam", {{ scale: {target:.2f}, duration: {j(max(.5, out_t - start))}, ease: "sine.inOut" }}, {j(start)});')
    if b < cam_end:
        tl.append(f'tl.to("#cam", {{ scale: {target + .3:.2f}, rotation: {(2.5 if k % 2 else -2.5)}, filter: "blur(18px)", duration: .18, ease: "power3.in" }}, {j(b - .18)});')
        tl.append(f'tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: .6, duration: .12, ease: "power1.in", immediateRender: false }}, {j(b - .1)});')
        tl.append(f'tl.to("#flash", {{ opacity: 0, duration: .3, ease: "power2.out" }}, {j(b + .02)});')
        tl.append(f'tl.fromTo("#tint", {{ opacity: 0 }}, {{ opacity: 1, duration: .15, ease: "power1.in", immediateRender: false }}, {j(b - .12)});')
        tl.append(f'tl.to("#tint", {{ opacity: 0, duration: .45, ease: "power2.out" }}, {j(b + .03)});')
    zoom_in = not zoom_in

# ---------- materialize the HyperFrames workspace ----------
for d in ("vendor", "assets/icons"):
    (P / d).mkdir(parents=True, exist_ok=True)
shutil.copytree(KIT / "template" / "vendor", P / "vendor", dirs_exist_ok=True)
shutil.copy(KIT / "assets" / "logo" / "whieda-emblem.png", P / "assets" / "whieda-emblem.png")
for f in used_icons:
    shutil.copy(KIT / "assets" / "icons" / f, P / "assets" / "icons" / f)
hf = P / "hyperframes.json"
if not hf.exists():
    hf.write_text(json.dumps({"name": args.name}, indent=2))

css = (KIT / "template" / "style.css").read_text()
if cfg.get("caption_accent"):  # e.g. light blue when the speaker wears red/blue (blue on red is unreadable)
    css += f"      .cap .hot {{ color: {cfg['caption_accent']}; }}\n"
vid_dur = min(VID, DUR)
page = f"""<!doctype html>
<html lang="uz">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <!-- Generated by pipeline/build.py from project.json — edit project.json, not this file. -->
    <script src="vendor/gsap.min.js"></script>
    <link rel="stylesheet" href="vendor/fonts.css" />
    <style>
{css}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{j(DUR)}" data-width="1080" data-height="1920">
      <div class="vidwrap"><div class="cam" id="cam">
        <video id="aroll" class="clip" src="work/video.mp4" playsinline muted data-start="0" data-duration="{j(vid_dur)}" data-track-index="0"></video>
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
(P / "index.html").write_text(page)
(P / "work" / "timing.json").write_text(json.dumps({"duration": DUR, "video": vid_dur, "transitions": trans,
                                                    "end_card_at": END_AT if (END and not SAMPLE) else None}, indent=1))
print(f"[build] {args.name}: {len(clips)} clips, {DUR:.2f}s{' (SAMPLE)' if SAMPLE else ''}, transitions at {trans}")
