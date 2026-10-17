#!/usr/bin/env python3
"""Synthesize SFX track (120s stereo 48k): whooshes, UI clicks, typing ticks,
low hits, logo riser. Writes build/sfx.wav."""
import numpy as np

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
    # simple bandpass-ish: multiply by sine sweep
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

rng = np.random.default_rng(7)

# --- scene whooshes (cuts) ---
whooshes = [7.0, 11.75, 21.0, 26.75, 36.0, 42.75, 47.5, 53.0, 59.75, 75.75, 92.75, 105.75, 113.75]
for t in whooshes:
    put(whoosh(0.55), t)
# --- reveal hits ---
put(hit(0.5), 36.2)      # s3 result materializes
put(hit(0.4), 47.7)      # s4 cinematic cut
put(hit(0.45), 86.2)     # s6 product reveal
# --- UI tap clicks (scene time) ---
clicks = [14.2, 18.5, 45.0, 83.0, 95.0, 107.6, 111.0]
for t in clicks:
    put(click(), t)
    put(whoosh(0.35, gain=0.12), t + 0.02)  # soft transition swell
# --- typing ticks during scene 3 prompt (scene 27-32) ---
t = 28.4
for _ in range(14):
    put(tick(), t)
    t += float(rng.uniform(0.28, 0.44))
# --- logo riser (scene 9) ---
put(riser(1.5), 114.0)
put(whoosh(0.8, gain=0.25, f0=200, f1=1200), 114.6)

mix = np.stack([L, R], axis=1)
peak = np.abs(mix).max()
mix = mix / peak * 0.9
pcm = (mix * 32767).astype(np.int16)
import wave
with wave.open("build/sfx.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("sfx.wav written 120.0 s")
