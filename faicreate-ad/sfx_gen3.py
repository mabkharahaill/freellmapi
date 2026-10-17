#!/usr/bin/env python3
"""v3 SFX track (120s stereo 48k) — tap clicks on the composite timeline,
page whooshes, reveal hits/whooshes, typing ticks, logo riser."""
import numpy as np
import wave

SR = 48000
DUR = 120.0
N = int(SR * DUR)
L = np.zeros(N)
R = np.zeros(N)


def put(sig, t0, gain=1.0):
    i0 = int(t0 * SR)
    i1 = min(N, i0 + len(sig))
    if i0 < 0:
        return
    seg = sig[: i1 - i0]
    L[i0:i1] += seg * gain
    R[i0:i1] += seg * gain


def noise(n):
    return np.random.randn(n)


def whoosh(dur=0.6, gain=0.35, f0=120, f1=900):
    n = int(SR * dur)
    t = np.arange(n) / SR
    sig = noise(n)
    phase = 2 * np.pi * (f0 * t + (f1 - f0) * t ** 2 / (2 * dur))
    env = np.sin(np.pi * t / dur) ** 2
    sig = np.tanh(2.2 * sig) * env * 0.5 + np.sin(phase) * env * 0.35
    return sig * gain


def click(gain=0.30):
    n = int(SR * 0.07)
    t = np.arange(n) / SR
    f = 1150 - 500 * t / 0.07
    sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 55)
    return sig * gain


def tick(gain=0.22):
    n = int(SR * 0.028)
    t = np.arange(n) / SR
    sig = noise(n) * np.exp(-t * 160) * 2.2
    return sig * gain


def hit(gain=0.5):
    n = int(SR * 0.35)
    t = np.arange(n) / SR
    sig = np.sin(2 * np.pi * (75 - 30 * t / 0.35) * t) * np.exp(-t * 9)
    sig += noise(n) * np.exp(-t * 30) * 0.4
    return sig * gain


def riser(dur=1.4, gain=0.30):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 220 + 620 * (t / dur) ** 2
    sig = (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + noise(n) * 0.25)
    env = (t / dur) ** 1.6
    return sig * env * gain


rng = np.random.default_rng(11)

# scene-boundary whooshes (blends centered on VO scene changes)
for t in [11.25, 26.75, 42.75, 59.75, 75.75, 92.75, 105.75, 113.75]:
    put(whoosh(0.55), t)

# UI tap clicks (final-timeline times, from composite frame taps)
for t in [15.0, 20.4, 32.5, 45.0, 78.5, 95.0, 107.8, 110.5]:
    put(click(), t)
    put(whoosh(0.35, gain=0.12), t + 0.02)

# full-screen "reality" reveals
put(whoosh(0.55, gain=0.4), 36.0)   # riyadh night
put(hit(0.5), 36.2)
put(whoosh(0.55, gain=0.4), 47.5)   # supercar burst
put(hit(0.4), 47.7)
put(whoosh(0.45, gain=0.32), 65.0)  # storyboard
put(whoosh(0.45, gain=0.32), 70.0)  # music studio
put(whoosh(0.55, gain=0.4), 81.0)   # perfume ad
put(hit(0.45), 81.2)

# typing ticks during S3a prompt (final time 27.4 -> 30.4)
t = 27.4
for _ in range(14):
    put(tick(), t)
    t += float(rng.uniform(0.18, 0.3))

# logo riser (scene 9)
put(riser(1.5), 114.0)
put(whoosh(0.8, gain=0.25, f0=200, f1=1200), 114.6)

mix = np.stack([L, R], axis=1)
peak = np.abs(mix).max()
mix = mix / peak * 0.9
pcm = (mix * 32767).astype(np.int16)
with wave.open("build/sfx3.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("sfx3.wav written 120.0 s")
