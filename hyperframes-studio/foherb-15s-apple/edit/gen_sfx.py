#!/usr/bin/env python3
"""Synthesize minimal iOS-flavored UI sounds: clean sines, soft noise, fast decays."""
import numpy as np, wave
from pathlib import Path

SR = 44100
OUT = Path(__file__).resolve().parents[1] / "assets" / "sfx"

def save(name, x, gain=0.9):
    x = x / (np.abs(x).max() + 1e-9) * gain
    with wave.open(str(OUT / f"{name}.wav"), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def t(d): return np.linspace(0, d, int(SR * d), False)
def env(n, a, r):
    e = np.ones(n); na, nr = int(SR*a), int(SR*r)
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e

rng = np.random.default_rng(7)

# tick: tiny woodblock-ish click (keyboard tick)
d = 0.09; x = np.sin(2*np.pi*1900*t(d)) * np.exp(-t(d)*90) + 0.4*np.sin(2*np.pi*950*t(d))*np.exp(-t(d)*70)
save("tick", x, 0.7)

# pop: soft bubble pop (widget bounce)
d = 0.18; f = 520*np.exp(-t(d)*14)+180
x = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t(d)*26)
save("pop", x, 0.8)

# ding: two-tone notification chime (E6+G6, soft)
d = 0.9; x = (np.sin(2*np.pi*1318.5*t(d)) + 0.6*np.sin(2*np.pi*1568*t(d)) + 0.25*np.sin(2*np.pi*2637*t(d)))
x *= np.exp(-t(d)*6.5); save("ding", x, 0.55)

# paydone: Apple-Pay-ish success (quick low->high two notes)
d = 0.55; n1 = np.sin(2*np.pi*740*t(0.16))*np.exp(-t(0.16)*18)
n2 = (np.sin(2*np.pi*1175*t(0.42)) + 0.5*np.sin(2*np.pi*2350*t(0.42)))*np.exp(-t(0.42)*9)
x = np.concatenate([n1, n2]); save("paydone", x, 0.6)

# whoosh: band-swept noise, airy
d = 0.6; noise = rng.standard_normal(int(SR*d))
from numpy.fft import rfft, irfft
N = len(noise); X = rfft(noise); freqs = np.fft.rfftfreq(N, 1/SR)
sweep = np.exp(-((freqs-1400)/900)**2)
x = irfft(X*sweep); x *= env(len(x), 0.22, 0.3) * np.hanning(len(x))
save("whoosh", x, 0.5)

# boom: soft sub thump (card lands)
d = 0.7; f = 120*np.exp(-t(d)*9)+42
x = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t(d)*7); save("boom", x, 0.85)

# riser: airy noise swell into the end card
d = 1.1; noise = rng.standard_normal(int(SR*d))
X = rfft(noise); freqs = np.fft.rfftfreq(len(noise), 1/SR)
x = irfft(X*np.exp(-((freqs-2600)/1600)**2))
x *= np.linspace(0, 1, len(x))**2.2; save("riser", x, 0.4)

print("sfx:", sorted(p.name for p in OUT.glob("*.wav")))
