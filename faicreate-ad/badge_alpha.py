#!/usr/bin/env python3
"""Convert the black-background FAI Create badge into alpha PNGs for overlay compositing."""
import numpy as np
from PIL import Image

BADGE = "assets/Futuristic FAI Create Neon Badge.png"


def to_alpha(path, size):
    img = Image.open(BADGE).convert("RGB").resize((size, size), Image.LANCZOS)
    b = np.array(img).astype(np.float32)
    a = b.max(axis=2)  # black -> 0, neon glow -> high
    rgba = np.dstack([b, a]).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(path)
    print(path, "ok")


to_alpha("build/wm_badge170.png", 170)
to_alpha("build/logo_badge640.png", 640)
