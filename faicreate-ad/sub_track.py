#!/usr/bin/env python3
"""Bake the whole 120s subtitle track as an RGBA PNG sequence (one frame per video frame)."""
import json
import os

import numpy as np
from PIL import Image

from sub_render import CUES

FPS = 30
W, H = 1080, 1920
BOTTOM_MARGIN = 235
FADE = 0.22
B = [0, 12, 27, 43, 60, 76, 93, 106, 114, 120]
OUT = "build/substrack"


def clip01(x):
    return max(0.0, min(1.0, x))


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))

    meta = json.load(open("build/subs/meta.json"))

    from build_video import cue_timing, ff_dur
    voice_durs = [ff_dur(f"audio/vo{i}.mp3") for i in range(1, 10)]
    timings = cue_timing(voice_durs)

    scene_cues = {sc: [] for sc in range(1, 10)}
    for idx, a, b in timings:
        sc = meta[f"cue{idx:02d}"]["scene"]
        scene_cues[sc].append((idx, a, b))

    loaded = {}
    for sc, cues in scene_cues.items():
        for idx, a, b in cues:
            img = np.array(Image.open(f"build/subs/cue{idx:02d}.png").convert("RGBA"))
            x = (W - img.shape[1]) // 2
            y = H - BOTTOM_MARGIN - img.shape[0]
            loaded[idx] = (img, x, y)

    tag = np.array(Image.open("build/subs/tagline.png").convert("RGBA"))
    dom = np.array(Image.open("build/subs/domain.png").convert("RGBA"))
    tag_pos = ((W - tag.shape[1]) // 2, 1315)
    dom_pos = ((W - dom.shape[1]) // 2, 1555)
    tag_win = (114.55, 120.5)
    dom_win = (115.15, 120.5)

    blank = np.zeros((H, W, 4), dtype=np.uint8)
    frame_no = 0
    for sc in range(1, 10):
        t0 = B[sc - 1]
        seg = B[sc] - t0
        n = int(round(seg * FPS))
        cues = scene_cues[sc]
        for f in range(n):
            t = t0 + f / FPS
            frame = blank.copy()
            if sc == 9:
                for img, pos, win, fd in ((tag, tag_pos, tag_win, 0.7),
                                          (dom, dom_pos, dom_win, 0.7)):
                    a0 = win[0]
                    e = clip01((t - a0) / fd)
                    if e > 0:
                        lay = img.copy()
                        lay[..., 3] = (img[..., 3].astype(np.float32) * e).astype(np.uint8)
                        frame[pos[1]:pos[1] + img.shape[0], pos[0]:pos[0] + img.shape[1]] = lay
            else:
                for idx, a, b in cues:
                    if not (a - 0.001 <= t <= b + 0.001):
                        continue
                    e = clip01((t - a) / FADE) * clip01((b - t) / FADE)
                    if e <= 0:
                        continue
                    img, x, y = loaded[idx]
                    lay = img.copy()
                    lay[..., 3] = (img[..., 3].astype(np.float32) * e).astype(np.uint8)
                    frame[y:y + img.shape[0], x:x + img.shape[1]] = lay
            Image.fromarray(frame, "RGBA").save(f"{OUT}/frame_{frame_no:04d}.png")
            frame_no += 1

    print("subtitle frames:", frame_no)


if __name__ == "__main__":
    main()
