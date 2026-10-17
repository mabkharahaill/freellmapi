#!/usr/bin/env python3
"""Energetic electronic music bed (120s) for the FAI CREATE ad. 124 BPM, A minor."""
import numpy as np
import wave
import math

SR = 44100
DUR = 120.0
N = int(SR * DUR)
BPM = 124.0
BEAT = 60.0 / BPM
BAR = BEAT * 4.0
N_BARS = 62  # 62 * BAR == 120.000s exactly
rng = np.random.default_rng(42)

PROG = [
    {"root": 55.00, "tones": [220.00, 261.63, 329.63]},   # Am
    {"root": 43.65, "tones": [174.61, 220.00, 261.63]},   # F
    {"root": 65.41, "tones": [261.63, 329.63, 392.00]},   # C
    {"root": 49.00, "tones": [196.00, 246.94, 293.66]},   # G
]

drumL = np.zeros(N)
drumR = np.zeros(N)
scL = np.zeros(N)
scR = np.zeros(N)
kick_times = []


def place(bufL, bufR, t, s, gain=1.0, stereo="C"):
    i0 = int(t * SR)
    if i0 < 0:
        s = s[-i0:]
        i0 = 0
    i1 = min(N, i0 + len(s))
    sl = s[i0 - int(t * SR):i1 - int(t * SR)]
    if stereo == "C":
        bufL[i0:i1] += sl * gain
        bufR[i0:i1] += sl * gain
    elif stereo == "L":
        bufL[i0:i1] += sl * gain
    elif stereo == "R":
        bufR[i0:i1] += sl * gain
    return i1 <= N


def make_kick():
    n = int(0.32 * SR)
    t = np.arange(n) / SR
    f = 44.0 + 150.0 * np.exp(-t / 0.045)
    phase = 2.0 * math.pi * np.cumsum(f) / SR
    s = np.sin(phase) * np.exp(-t / 0.11)
    click = rng.standard_normal(n) * np.exp(-np.arange(n) / (SR * 0.004)) * 0.4
    s = 0.85 * s + 0.15 * click
    return s * (0.9 / (np.abs(s).max() + 1e-9))


def make_clap():
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    a = math.exp(-2 * math.pi * 1500 / SR)
    y = np.zeros(n)
    py, px = 0.0, 0.0
    for i in range(n):
        py = a * (py + x[i] - px)
        px = x[i]
        y[i] = py
    s = np.zeros(n)
    for off, g in ((0, 0.7), (int(0.012 * SR), 0.5), (int(0.024 * SR), 0.4)):
        env = np.exp(-(t - off / SR) / 0.09)
        s[off:] += g * y[off:] * env[off:]
    return s * (0.8 / (np.abs(s).max() + 1e-9))


def make_hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    a = math.exp(-2 * math.pi * 7000 / SR)
    y = np.zeros(n)
    py, px = 0.0, 0.0
    for i in range(n):
        py = a * (py + x[i] - px)
        px = x[i]
        y[i] = py
    dec = 0.35 if open_ else 0.018
    s = y * np.exp(-t / dec)
    return s * (0.5 / (np.abs(s).max() + 1e-9))


def lp1(x, fc):
    a = 1.0 - math.exp(-2 * math.pi * fc / SR)
    y = np.zeros(len(x))
    yy = 0.0
    for i in range(len(x)):
        yy += a * (x[i] - yy)
        y[i] = yy
    return y


def make_bass(f, length=0.24, octave=False):
    n = int(length * SR)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for h in range(1, 9):
        s += np.sin(2 * math.pi * f * h * t) / h
    if octave:
        for h in range(1, 5):
            s += 0.5 * np.sin(2 * math.pi * f * 2 * h * t) / h
    s = lp1(s, 280.0)
    env = np.minimum(t / 0.006, 1.0) * np.exp(-t / 0.16)
    e = s * env
    return e * (1.0 / (np.abs(e).max() + 1e-9))


def make_pluck(f, gain=1.0, length=0.30):
    n = int(length * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * math.pi * f * t) + 0.35 * np.sin(2 * math.pi * 2 * f * t) + 0.12 * np.sin(2 * math.pi * 3 * f * t)
    env = np.exp(-t / 0.085) * np.minimum(t / 0.003, 1.0)
    s *= env
    return s * (gain * (1.0 / (np.abs(s).max() + 1e-9)))


def make_pad(freqs, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    atk = np.minimum(t / 0.9, 1.0)
    rel = np.minimum(np.clip((dur - t) / 0.7, 0.0, 1.0), 1.0)
    env = atk * rel
    outL = np.zeros(n)
    outR = np.zeros(n)
    for f in freqs:
        ff = f * 0.994
        s = np.zeros(n)
        for h in range(1, 7):
            s += np.sin(2 * math.pi * ff * h * t) / h
        outL += lp1(s, 1100.0)
        ff = f * 1.006
        s = np.zeros(n)
        for h in range(1, 7):
            s += np.sin(2 * math.pi * ff * h * t) / h
        outR += lp1(s, 1100.0)
    peak = max(np.abs(outL).max(), np.abs(outR).max(), 1e-9)
    return outL * env / peak, outR * env / peak


def make_riser(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    p = t / dur
    f = 180.0 + 2200.0 * p * p
    phase = 2 * math.pi * (180.0 * t + (2200.0 / 3.0) * t**3 / (dur * dur))
    s = 0.3 * rng.standard_normal(n) * (p ** 1.6) + 0.35 * np.sin(phase) * (p ** 1.4)
    return s * (0.5 / (np.abs(s).max() + 1e-9))


def make_boom():
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * math.pi * 48.0 * t) * np.exp(-t / 0.5)
    s += 0.3 * rng.standard_normal(n) * np.exp(-t / 0.03)
    return s * (0.9 / (np.abs(s).max() + 1e-9))


KICK = make_kick()
CLAP = make_clap()
HAT = make_hat(False)
HAT_O = make_hat(True)
BOOM = make_boom()
PATTERN = [0, 1, 2, 1]


def section_of(bar):
    if bar <= 5:
        return "intro"
    if bar <= 21:
        return "build1"
    if bar <= 38:
        return "build2"
    if bar <= 53:
        return "drop"
    if bar <= 57:
        return "break"
    return "outro"


def main():
    global scL, scR
    scL = np.zeros(N)
    scR = np.zeros(N)
    for bar in range(N_BARS):
        t0 = bar * BAR
        sec = section_of(bar)
        chord = PROG[bar % 4]
        tones = chord["tones"]
        root = chord["root"]

        if sec != "outro":
            pL, pR = make_pad(tones, BAR + 0.3)
            i0 = int(t0 * SR)
            i1 = min(N, i0 + len(pL))
            scL[i0:i1] += pL[: i1 - i0] * 0.34
            scR[i0:i1] += pR[: i1 - i0] * 0.34
        else:
            pL, pR = make_pad([220.00, 261.63, 329.63, 440.00], DUR - t0 + 1.0)
            i0 = int(t0 * SR)
            i1 = min(N, i0 + len(pL))
            scL[i0:i1] += pL[: i1 - i0] * 0.42
            scR[i0:i1] += pR[: i1 - i0] * 0.42

        if sec in ("build1", "build2", "drop"):
            for b in range(4):
                tk = t0 + b * BEAT
                place(drumL, drumR, tk, KICK, 0.95)
                kick_times.append(tk)
                if sec in ("build2", "drop") and b in (1, 3):
                    place(drumL, drumR, tk, CLAP, 0.55)
        if sec in ("build1", "build2", "drop"):
            for e in range(4):
                th = t0 + (e + 0.5) * BEAT
                if sec == "build1":
                    place(drumL, drumR, th, HAT, 0.4)
                else:
                    place(drumL, drumR, th, HAT, 0.55)
                    if sec == "drop":
                        place(drumL, drumR, t0 + (e + 0.75) * BEAT, HAT, 0.25)
                        if e == 3:
                            place(drumL, drumR, th + BEAT * 0.25, HAT_O, 0.3)
        if sec in ("build1", "build2", "drop"):
            for e in range(8):
                tb = t0 + e * BEAT / 2
                octv = sec in ("build2", "drop") and e % 2 == 1
                place(scL, scR, tb, make_bass(root, 0.24, octv), 0.5)

        if sec == "intro":
            for e in range(4):
                ta = t0 + (e + 0.5) * BEAT
                f = tones[PATTERN[e % 4]] * 2
                place(scL, scR, ta, make_pluck(f, 0.5), 0.3)
        elif sec == "build1":
            for e in range(8):
                ta = t0 + e * BEAT / 2
                f = tones[PATTERN[e % 4]] * 2
                place(scL, scR, ta, make_pluck(f, 0.6), 0.32)
        elif sec in ("build2", "drop"):
            for e in range(16):
                ta = t0 + e * BEAT / 4
                f = tones[PATTERN[e % 4]] * 2
                ch = "L" if e % 2 == 0 else "R"
                place(scL, scR, ta, make_pluck(f, 0.65), 0.34, ch)
            if sec == "drop":
                for e in range(8):
                    tl = t0 + e * BEAT / 2
                    place(scL, scR, tl, make_pluck(tones[PATTERN[e % 4]] * 4, 0.5, 0.45), 0.26)
        elif sec == "break":
            for e in range(4):
                ta = t0 + (e + 0.5) * BEAT
                f = tones[PATTERN[e % 4]] * 2
                place(scL, scR, ta, make_pluck(f, 0.45), 0.28)

        if sec == "intro" and bar == 5:
            place(drumL, drumR, t0 + BAR - 1.4, make_riser(1.4), 0.5)
        if sec == "build1" and bar == 21:
            place(drumL, drumR, t0 + BAR - 1.6, make_riser(1.6), 0.55)
        if sec == "build2" and bar == 38:
            place(drumL, drumR, t0 + BAR - 1.6, make_riser(1.6), 0.6)
        if sec == "break" and bar == 53:
            place(drumL, drumR, t0 + BAR - 1.2, make_riser(1.2), 0.5)
        if bar == 58:
            place(drumL, drumR, t0, BOOM, 0.8)

    g = np.ones(N)
    for tk in kick_times:
        i0 = int(tk * SR)
        i1 = min(N, i0 + int(0.6 * SR))
        tt = np.arange(i1 - i0) / SR
        e = 0.42 + 0.58 * np.exp(-tt / 0.14)
        g[i0:i1] = np.minimum(g[i0:i1], e)
    scL *= g
    scR *= g

    def echo(buf):
        wet = np.zeros(N)
        for d, w in ((int(0.061 * SR), 0.16), (int(0.097 * SR), 0.11), (int(0.131 * SR), 0.06)):
            wet[d:] += buf[:-d] * w
        return wet
    scL = scL + echo(scL)
    scR = scR + echo(scR)

    mixL = 0.85 * drumL + scL
    mixR = 0.85 * drumR + scR
    m = np.stack([mixL, mixR])
    m = np.tanh(1.25 * m) * 0.92
    peak = np.abs(m).max()
    m = m * (0.85 / peak)
    t = np.arange(N) / SR
    m[:, : int(0.4 * SR)] *= (np.arange(int(0.4 * SR)) / (0.4 * SR))[None, :]
    fo = np.minimum(1.0, (DUR - t[-int(1.4 * SR):]) / 1.4)
    m[:, -int(1.4 * SR):] *= fo[None, :]

    pcm = (m * 32767).astype("<i2")
    with wave.open("audio/music.wav", "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print("music.wav written", N / SR, "s")


if __name__ == "__main__":
    main()
