#!/usr/bin/env python3
"""v3 phone composites: detect the phone screen quadrilateral in each photo,
perspective-warp every UI sequence frame onto it (with screen grade + glare),
and emit full 1080x1920 RGB frames per beat."""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

PHOTOS = {
    "hand": "video/v3_hand_phone.png",
    "desk": "video/v3_phone_desk.png",
}
UIW, UIH = 1080, 2340
OUTW, OUTH = 1080, 1920
COMP = "build/comp3"
os.makedirs(COMP, exist_ok=True)


def detect_quad(path, win=(90, 200), search_box=None):
    """Find the bright phone screen: density peak (optionally restricted to a
    box) -> flood fill from that seed -> rotated-rect fit. Height comes from
    width / 9:19.5 when the bottom is occluded by a hand."""
    from collections import deque
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im)
    H, W, _ = arr.shape
    m = (arr.mean(axis=2) > 150)
    if search_box is not None:
        sx0, sy0, sx1, sy1 = [int(p * s) for p, s in zip(search_box, (W, H, W, H))]
        m2 = np.zeros_like(m)
        m2[sy0:sy1, sx0:sx1] = m[sy0:sy1, sx0:sx1]
        m = m2
    # integral image for O(1) box sums
    M = np.pad(m.astype(np.int32), ((1, 0), (1, 0)))
    I = M.cumsum(0).cumsum(1)
    wh, ww = win
    hh, hw = H - wh, W - ww
    D = (I[wh:wh + hh, ww:ww + hw] - I[0:hh, ww:ww + hw]
         - I[wh:wh + hh, 0:hw] + I[0:hh, 0:hw])
    cy, cx = np.unravel_index(int(np.argmax(D)), D.shape)
    seed = (cx + ww // 2, cy + wh // 2)
    lab = np.zeros(m.shape, np.int32)
    q = deque([seed])
    lab[seed[1], seed[0]] = 1
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and m[ny, nx] and not lab[ny, nx]:
                lab[ny, nx] = 1
                q.append((nx, ny))
    ys, xs = np.where(lab)
    if len(ys) < 2000:
        raise RuntimeError(f"screen blob too small in {path} ({len(ys)} px)")
    pts = np.column_stack([xs, ys]).astype(float)
    c = pts.mean(axis=0)
    cov = np.cov((pts - c).T)
    evals, evecs = np.linalg.eigh(cov)
    u = evecs[:, int(np.argmax(evals))]          # principal axis = height dir
    if u[1] < 0:
        u = -u                                    # point "down"
    v = np.array([-u[1], u[0]])
    w_ext = (pts @ v).max() - (pts @ v).min()
    h_ext = (pts @ u).max() - (pts @ u).min()
    h_want = w_ext * (2340 / 1080)
    if h_ext > 0.85 * h_want:                     # full screen visible
        h = h_ext
        center = c
    else:                                         # bottom occluded: align top
        top_off = (pts - c) @ u
        center = c + u * (h_want / 2 + top_off.min())
        h = h_want
    c1 = center - u * h / 2 - v * w_ext / 2
    c2 = center - u * h / 2 + v * w_ext / 2
    c3 = center + u * h / 2 + v * w_ext / 2
    c4 = center + u * h / 2 - v * w_ext / 2
    cs = [c1, c2, c3, c4]
    tl = min(cs, key=lambda p: p[0] + p[1])
    br = max(cs, key=lambda p: p[0] + p[1])
    # for a clockwise-tilted screen TR has the LARGEST x-y, BL the smallest
    tr = max(cs, key=lambda p: p[0] - p[1])
    bl = min(cs, key=lambda p: p[0] - p[1])
    return im, [tl, tr, br, bl]


def inset_quad(quad, frac):
    tl, tr, br, bl = quad
    cxm = sum(p[0] for p in quad) / 4
    cym = sum(p[1] for p in quad) / 4
    diag = float(np.hypot(br[0] - tl[0], br[1] - tl[1]))
    k = frac * diag

    def ins(p):
        dx, dy = p[0] - cxm, p[1] - cym
        mm = (dx * dx + dy * dy) ** 0.5 or 1
        return (p[0] - dx / mm * k, p[1] - dy / mm * k)
    return [ins(p) for p in quad]


def quad_coeffs(quad):
    """8 coefficients mapping DEST->SRC for Image.transform PERSPECTIVE."""
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = quad
    src = [(0, 0), (UIW, 0), (UIW, UIH), (0, UIH)]
    A, b = [], []
    for (u, v), (x, y) in zip(src, quad):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y]]
        b.append(u)
        A += [[0, 0, 0, x, y, 1, -v * x, -v * y]]
        b.append(v)
    return np.linalg.solve(np.array(A, float), np.array(b, float)).tolist()


def build_screen_layer(quad, coeffs):
    """Full-frame RGBA: warped UI placeholder (black) + alpha mask + glare."""
    mask = Image.new("L", (OUTW, OUTH), 0)
    ImageDraw.Draw(mask).polygon(quad, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(1.6))
    return mask, coeffs


def make_glare(quad):
    """Screen-aligned diagonal glare band + corner sheen."""
    tl, tr, br, bl = [np.array(c, float) for c in quad]
    u = (tr - tl) / max(1e-6, np.linalg.norm(tr - tl))
    d = (bl - tl) / max(1e-6, np.linalg.norm(bl - tl))
    w = np.linalg.norm(tr - tl)
    h = np.linalg.norm(bl - tl)
    def P(fu, fd):
        p = tl + u * (fu * w) + d * (fd * h)
        return (float(p[0]), float(p[1]))
    g = Image.new("L", (OUTW, OUTH), 0)
    ImageDraw.Draw(g).polygon([P(0.0, 0.10), P(1.0, 0.02), P(0.78, 0.30), P(0.12, 0.38)], fill=24)
    g = g.filter(ImageFilter.GaussianBlur(40))
    g2 = Image.new("L", (OUTW, OUTH), 0)
    c = np.array(P(0.16, 0.14))
    r = 0.42 * w
    ImageDraw.Draw(g2).ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=13)
    g2 = g2.filter(ImageFilter.GaussianBlur(70))
    return g, g2


GLARES = {}


SEARCH_BOXES = {
    "hand": (0.35, 0.40, 0.72, 0.70),
    "desk": (0.50, 0.28, 0.92, 0.62),
}
QUADS = {}


def get_photo_quad(photo_key):
    if photo_key not in QUADS:
        QUADS[photo_key] = detect_quad(PHOTOS[photo_key], search_box=SEARCH_BOXES[photo_key])
    return QUADS[photo_key]


def composite_beat(photo_key, beat, frames_in, out_dir):
    photo, glass = get_photo_quad(photo_key)
    W0, H0 = photo.size
    sx, sy = OUTW / W0, OUTH / H0
    base = photo.convert("RGB").resize((OUTW, OUTH), Image.LANCZOS)
    glass = [(c[0] * sx, c[1] * sy) for c in glass]
    W, H = OUTW, OUTH
    arr = np.asarray(base)
    # masks + static layers (built once per photo)
    glass_m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glass_m).polygon(glass, fill=255)
    glass_m = glass_m.filter(ImageFilter.GaussianBlur(1.2))
    ui_quad = inset_quad(glass, 0.012)
    ui_m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(ui_m).polygon(ui_quad, fill=255)
    ui_m = ui_m.filter(ImageFilter.GaussianBlur(1.5))
    # screen-off dark glass (visible as the thin rim around the UI)
    dark = (arr * 0.26).astype(np.uint8)
    dark = np.maximum(dark, np.array([16, 16, 30], np.uint8))
    screen_off = Image.fromarray(dark)
    # occluders crossing the glass (fingers, camera dot): non-bright pixels inside it
    bright = (arr.mean(axis=2) > 150)
    gm = np.asarray(glass_m, bool)
    occl = gm & ~bright
    occl = Image.fromarray(occl.astype(np.uint8) * 255)
    occl = occl.filter(ImageFilter.MaxFilter(5))
    occl = occl.filter(ImageFilter.GaussianBlur(2.5))
    # inner shadow: thin band hugging the inside of the glass edge
    g_soft = glass_m.filter(ImageFilter.GaussianBlur(10))
    from PIL import ImageChops
    band = ImageChops.subtract(glass_m, g_soft)
    band = band.point(lambda v: min(255, v * 3))
    edge = band.filter(ImageFilter.GaussianBlur(2.5))
    if photo_key not in GLARES:
        g1, g2 = make_glare(glass)
        GLARES[photo_key] = Image.fromarray(
            np.minimum(255, np.asarray(g1, np.int16) + np.asarray(g2, np.int16))
            .astype(np.uint8))
    glare = GLARES[photo_key]
    coeffs = quad_coeffs(ui_quad)
    os.makedirs(f"{COMP}/{out_dir}", exist_ok=True)
    grade = (236, 246, 264)  # slight cool tint on the UI
    white = Image.new("RGB", (W, H), (255, 255, 255))
    black = Image.new("RGB", (W, H), (8, 8, 18))
    n = 0
    for i, name in enumerate(frames_in):
        ui = Image.open(name).convert("RGB")
        warped = ui.transform((W, H), Image.PERSPECTIVE, coeffs, fillcolor=(0, 0, 0))
        a = np.asarray(warped, np.int16)
        a = (a * np.array(grade, np.int16) // 255).astype(np.uint8)
        warped = Image.fromarray(a)
        frame = base
        frame = Image.composite(screen_off, frame, glass_m)   # dark glass
        frame = frame.copy()
        frame.paste(warped, (0, 0), ui_m)                     # UI
        frame = Image.composite(white, frame, glare)          # glare
        frame = Image.composite(black, frame, edge)           # inner shadow rim
        frame.paste(base, (0, 0), occl)                       # fingers back on top
        frame.save(f"{COMP}/{out_dir}/frame_{i:04d}.png")
        n += 1
    print(f"comp {out_dir}: {n} frames ok")


def seq_names(beat, n):
    return [f"build/uiseq3/{beat}/frame_{i:04d}.png" for i in range(n)]


BEATS = [
    ("hand", "home_p", 105, "b1c_home"),
    ("desk", "home_tap", 150, "b2a_home_tap"),
    ("desk", "tools_scroll", 150, "b2b_tools"),
    ("desk", "image_type", 150, "b3a_type"),
    ("desk", "image_create", 150, "b3b_create"),
    ("hand", "img2vid", 150, "b4a_vid"),
    ("desk", "storyfilm", 165, "b5a_story"),
    ("desk", "ads", 165, "b6a_ads"),
    ("hand", "lang", 135, "b7a_lang"),
    ("desk", "gaming", 120, "b7c_game"),
    ("hand", "account", 105, "b8a_acct"),
    ("hand", "plans", 120, "b8b_plans"),
]


def main():
    # dump quads for visual check
    for pk in PHOTOS:
        _, q = get_photo_quad(pk)
        print(pk, "quad:", [(round(a), round(b)) for a, b in q])
    for pk, beat, n, out in BEATS:
        composite_beat(pk, beat, seq_names(beat, n), out)
    print("ALL COMPOSITES DONE")


if __name__ == "__main__":
    main()
