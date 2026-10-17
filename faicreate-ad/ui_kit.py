#!/usr/bin/env python3
"""Render FAI CREATE UI screen frames (1080x1920) from REAL site content,
plus blur-pad brand-card beats and tap/ripple sprites for the cinematic ad."""
import os
import arabic_reshaper
from bidi.algorithm import get_display
import unicodedata
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FB = "assets/Tajawal-Bold.ttf"
FM = "assets/Tajawal-Medium.ttf"
FV = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FH = "assets/NotoSansDevanagari.ttf"
OUT = "build/ui"
os.makedirs(OUT, exist_ok=True)
os.makedirs("build/ripple", exist_ok=True)

# ---------------- Arabic shaping (same pipeline as subtitles) ----------------
_BASE_BY_NAME = {}
for _cp in range(0x0600, 0x0700):
    try:
        _BASE_BY_NAME[unicodedata.name(chr(_cp))] = _cp
    except ValueError:
        pass
_SPECIAL = {
    "ARABIC TATWEEL WITH FATHATAN ABOVE": "\u0640\u064B",
    "ARABIC TAIL FRAGMENT": "",
    "ZERO WIDTH NO-BREAK SPACE": "",
}

def _fix(s):
    out = []
    for c in s:
        cp = ord(c)
        if 0xFE70 <= cp <= 0xFEFF:
            name = unicodedata.name(c, "")
            if name in _SPECIAL:
                out.append(_SPECIAL[name])
                continue
            base = name
            for suffix in (" ISOLATED FORM", " MEDIAL FORM", " FINAL FORM", " INITIAL FORM"):
                base = base.replace(suffix, "")
            out.append(chr(_BASE_BY_NAME[base]) if base in _BASE_BY_NAME else c)
        else:
            out.append(c)
    return "".join(out)

def shape(t):
    return get_display(_fix(arabic_reshaper.reshape(t)))

# ---------------- palette / fonts ----------------
BG_TOP, BG_BOT = (10, 13, 31), (22, 17, 50)
CARD = (22, 27, 58, 255)
CARD_HI = (36, 31, 78, 255)
BORDER = (124, 92, 255, 130)
TXT = (245, 247, 255, 255)
TXT2 = (158, 166, 203, 255)
ACC1, ACC2 = (139, 92, 246), (59, 130, 246)
GOLD = (255, 202, 92, 255)
PINK = (255, 90, 160, 255)
RED = (255, 70, 70, 255)

def F(path, size):
    return ImageFont.truetype(path, size)

_ALL_TEXTS = []

def tstr(s):
    _ALL_TEXTS.append(s)
    return s

# ---------------- helpers ----------------
def bg():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        t = y / H
        c = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y + 4)], fill=c)
    img = img.convert("RGBA")
    g1 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d1 = ImageDraw.Draw(g1)
    d1.ellipse([W // 2 - 620, -620, W // 2 + 620, 360], fill=(109, 40, 217, 66))
    g1 = g1.filter(ImageFilter.GaussianBlur(130))
    g2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d2 = ImageDraw.Draw(g2)
    d2.ellipse([W // 2 - 640, H - 1200, W // 2 + 640, H - 180], fill=(37, 99, 235, 46))
    g2 = g2.filter(ImageFilter.GaussianBlur(130))
    img.alpha_composite(g1)
    img.alpha_composite(g2)
    return img

_badge_cache = {}
def badge(sz):
    if sz not in _badge_cache:
        _badge_cache[sz] = Image.open("build/wm_badge170.png").resize((sz, sz), Image.LANCZOS)
    return _badge_cache[sz]

def txt(d, xy, s, font, fill=TXT, shaped=False, anchor=None):
    d.text(xy, shape(s) if shaped else s, font=font, fill=fill, anchor=anchor)

def txtw(d, s, font, shaped=False):
    return d.textlength(shape(s) if shaped else s, font=font)

def rrect(d, box, r, fill=CARD, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def grad_rrect(canvas, box, r, c1=ACC1, c2=ACC2):
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = x1 - x0, y1 - y0
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for x in range(w):
        t = x / max(1, w - 1)
        c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        gd.line([(x, 0), (x, h)], fill=c + (255,))
    mask = Image.new("L", (w, h))
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    g.putalpha(mask)
    canvas.alpha_composite(g, (x0, y0))

def grad_border(d, box, r, width=3, c1=ACC1, c2=ACC2, alpha=255):
    x0, y0, x1, y1 = [int(v) for v in box]
    w, h = x1 - x0, y1 - y0
    g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for x in range(w):
        t = x / max(1, w - 1)
        c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        gd.line([(x, 0), (x, h)], fill=c + (alpha,))
        gd.line([(x, h - width), (x, h)], fill=c + (alpha,))
    gd.rectangle([0, 0, w - 1, width - 1], fill=c1 + (alpha,))
    gd.rectangle([0, h - width, w - 1, h - 1], fill=c2 + (alpha,))
    mask = Image.new("L", (w, h))
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    # ring = full rounded rect minus inner rounded rect
    inner = Image.new("L", (w, h))
    ImageDraw.Draw(inner).rounded_rectangle([width, width, w - 1 - width, h - 1 - width],
                                            radius=max(1, r - width), fill=255)
    ring = Image.eval(Image.composite(mask, Image.new("L", (w, h), 0), inner), lambda v: 255 - v)
    g.putalpha(Image.composite(g.getchannel("A"), Image.new("L", (w, h), 0), ring))
    # paste at canvas origin via caller; here return layer
    return g

def pill(d, box, r, label, font, active=False, outline_col=BORDER):
    x0, y0, x1, y1 = [int(v) for v in box]
    if active:
        grad_rrect_box = box
        # gradient fill
        w, h = x1 - x0, y1 - y0
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        for x in range(w):
            t = x / max(1, w - 1)
            c = tuple(int(ACC1[i] + (ACC2[i] - ACC1[i]) * t) for i in range(3))
            gd.line([(x, 0), (x, h)], fill=c + (235,))
        m = Image.new("L", (w, h))
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
        g.putalpha(m)
        d._image.alpha_composite(g, (x0, y0))
    else:
        rrect(d, box, r, fill=(16, 20, 44, 220), outline=outline_col, width=2)
    tw = d.textlength(label, font=font)
    d.text(((x0 + x1) / 2, (y0 + y1) / 2), label, font=font,
           fill=TXT, anchor="mm")

def status_bar(d):
    txt(d, (48, 26), "22:32", F(FM, 26), TXT)
    x = W - 48
    d.rounded_rectangle([x - 46 - 6, 30, x - 46, 52], radius=4, outline=TXT2, width=3)
    d.rectangle([x - 43, 34, x - 43 + 28, 48], fill=TXT)
    d.rounded_rectangle([x - 34, 28, x - 28, 54], radius=2, fill=TXT2)
    for i in range(4):
        d.rectangle([x - 120 - i * 12, 52 - [10, 14, 18, 22][i], x - 112 - i * 12, 52], fill=TXT2)
    d.arc([x - 92, 26, x - 56, 62], 200, 340, fill=TXT2, width=4)
    d.arc([x - 84, 34, x - 64, 54], 200, 340, fill=TXT2, width=4)
    d.ellipse([x - 76, 42, x - 68, 50], fill=TXT2)

def app_bar(d, canvas):
    d.rectangle([0, 64, W, 176], fill=(12, 15, 36, 200))
    canvas.alpha_composite(badge(84), (40, 80))
    txt(d, (148, 120), "FAI Create", F(FB, 40), TXT, anchor="lm")
    # coin pill
    rrect(d, (856, 88, 1040, 152), 32, fill=(28, 33, 70, 255), outline=(255, 202, 92, 160), width=2)
    d.ellipse([876, 102, 916, 142], fill=GOLD)
    txt(d, (896, 122), "F", F(FB, 22), (120, 70, 10, 255), anchor="mm")
    txt(d, (1028, 120), "100", F(FB, 32), GOLD, anchor="rm")

def nav(d, active):
    d.rectangle([0, 1810, W, 1920], fill=(10, 12, 30, 235))
    items = [("Home", "home"), ("Tools", "grid"), ("Projects", "folder"),
             ("Plans", "coin"), ("Settings", "gear")]
    cell = W / 5
    for i, (label, kind) in enumerate(items):
        cx = int(cell * i + cell / 2)
        col = TXT if active == label else (110, 118, 155, 255)
        f = F(FM, 22)
        if kind == "home":
            d.polygon([(cx - 20, 1848), (cx, 1828), (cx + 20, 1848)], fill=col)
            d.rectangle([cx - 14, 1848, cx + 14, 1868], fill=col)
        elif kind == "grid":
            for sx in (-1, 1):
                for sy in (-1, 1):
                    d.rounded_rectangle([cx + sx * 9 - 8, 1840 + sy * 9 - 8, cx + sx * 9 + 8, 1840 + sy * 9 + 8],
                                        radius=3, fill=col)
        elif kind == "folder":
            d.rounded_rectangle([cx - 18, 1838, cx + 18, 1864], radius=4, fill=col)
            d.rectangle([cx - 18, 1832, cx + 2, 1842], fill=col)
        elif kind == "coin":
            d.ellipse([cx - 16, 1832, cx + 16, 1864], outline=col, width=4)
            d.ellipse([cx - 7, 1841, cx + 7, 1855], outline=col, width=3)
        else:
            d.ellipse([cx - 14, 1834, cx + 14, 1862], outline=col, width=4)
            for a in range(0, 360, 45):
                import math
                px = cx + 20 * math.cos(math.radians(a))
                py = 1848 + 20 * math.sin(math.radians(a))
                d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
        d.text((cx, 1886), label, font=f, fill=col, anchor="mm")

def icon_image(d, cx, cy, col):
    d.rounded_rectangle([cx - 34, cy - 28, cx + 34, cy + 28], radius=8, outline=col, width=4)
    d.ellipse([cx - 18, cy - 16, cx - 4, cy - 2], fill=col)
    d.polygon([(cx - 28, cy + 22), (cx - 4, cy - 2), (cx + 10, cy + 12), (cx + 18, cy + 4), (cx + 30, cy + 22)], fill=col)

def icon_play(d, cx, cy, col):
    d.rounded_rectangle([cx - 34, cy - 26, cx + 34, cy + 26], radius=8, outline=col, width=4)
    d.polygon([(cx - 8, cy - 14), (cx - 8, cy + 14), (cx + 16, cy)], fill=col)

def icon_note(d, cx, cy, col):
    d.ellipse([cx - 18, cy + 6, cx - 4, cy + 20], fill=col)
    d.ellipse([cx + 10, cy - 2, cx + 24, cy + 12], fill=col)
    d.rectangle([cx - 4, cy - 22, cx + 24, cy - 14], fill=col)
    d.rectangle([cx + 16, cy - 18, cx + 24, cy + 8], fill=col)

def icon_film(d, cx, cy, col):
    d.rounded_rectangle([cx - 30, cy - 24, cx + 30, cy + 26], radius=6, outline=col, width=4)
    d.line([(cx - 30, cy - 8), (cx + 30, cy - 8)], fill=col, width=4)
    for i in range(3):
        d.rectangle([cx - 24 + i * 18, cy - 18, cx - 14 + i * 18, cy - 10], fill=col)

def icon_tag(d, cx, cy, col):
    d.polygon([(cx - 26, cy - 26), (cx + 10, cy - 26), (cx + 28, cy - 8), (cx + 10, cy + 10),
               (cx - 26, cy + 10)], outline=col, width=4)
    d.ellipse([cx - 8, cy - 14, cx, cy - 6], fill=col)

def cover_fit(src, tw, th):
    im = Image.open(src).convert("RGB")
    s = max(tw / im.width, th / im.height)
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = (im.width - tw) // 2
    y = (im.height - th) // 2
    return im.crop((x, y, x + tw, y + th)).convert("RGBA")

def rounded_paste(canvas, src, box, r):
    x0, y0, x1, y1 = [int(v) for v in box]
    im = cover_fit(src, x1 - x0, y1 - y0)
    mask = Image.new("L", (x1 - x0, y1 - y0))
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, x1 - x0 - 1, y1 - y0 - 1], radius=r, fill=255)
    layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    layer.paste(im, (0, 0), mask)
    canvas.alpha_composite(layer, (x0, y0))

def letterspace(d, xy, s, font, fill, dx):
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + dx

# ================= SCREENS =================

def s_home():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Home")
    img.alpha_composite(badge(230), ((W - 230) // 2, 230))
    txt(d, (540, 545), "Welcome to FAI Create", F(FB, 48), TXT, anchor="ma")
    txt(d, (540, 640), tstr("حوّل أفكارك إلى واقع"), F(FB, 62), (219, 183, 255, 255),
        shaped=True, anchor="ma")
    letterspace(d, (540 - 250, 735), "TURN IDEAS INTO REALITY", F(FM, 26), TXT2, 6)
    cards = [
        ("img", "AI Image", "Create from a prompt"),
        ("play", "Photo to Video", "Animate your photo"),
        ("note", "AI Song", "Start a song idea"),
        ("film", "Story to Film", "Build a film project"),
    ]
    cw, chh, gap = 468, 252, 24
    x0s, y0s = 60, 830
    for i, (k, title, sub) in enumerate(cards):
        cx0 = x0s + (i % 2) * (cw + gap)
        cy0 = y0s + (i // 2) * (chh + gap)
        rrect(d, (cx0, cy0, cx0 + cw, cy0 + chh), 26, fill=CARD, outline=BORDER, width=2)
        d.ellipse([cx0 + 34, cy0 + 34, cx0 + 118, cy0 + 118], fill=(30, 36, 78, 255),
                  outline=(139, 92, 246, 200), width=2)
        col = (168, 132, 255, 255)
        icx, icy = cx0 + 76, cy0 + 76
        if k == "img": icon_image(d, icx, icy, col)
        elif k == "play": icon_play(d, icx, icy, col)
        elif k == "note": icon_note(d, icx, icy, col)
        else: icon_film(d, icx, icy, col)
        txt(d, (cx0 + 36, cy0 + 152), title, F(FB, 34), TXT)
        txt(d, (cx0 + 36, cy0 + 198), sub, F(FM, 23), TXT2)
    grad_rrect(img, (270, 1352, 810, 1448), 48)
    txt(d, (540, 1400), "Create now", F(FB, 40), TXT, anchor="mm")
    rrect(d, (270, 1482, 810, 1578), 48, fill=(16, 20, 44, 220), outline=(139, 92, 246, 220), width=3)
    txt(d, (540, 1530), "Explore AI tools", F(FB, 34), TXT, anchor="mm")
    # language pills (real: English العربية اردو हिन्दी)
    langs = ["English", "العربية", "اردو"]
    fonts = [F(FM, 28), F(FM, 28), F(FM, 28)]
    labels = [langs[0], shape(langs[1]), shape(langs[2])]
    widths = [d.textlength(lb, font=ft) + 64 for lb, ft in zip(labels, fonts)]
    widths.append(hindi_width(d, 26) + 64)
    tot = sum(widths) + 16 * 3
    x = (W - tot) // 2
    for i in range(4):
        box = (x, 1646, x + widths[i], 1716)
        if i == 3:
            rrect(d, box, 35, fill=(16, 20, 44, 220), outline=BORDER, width=2)
            draw_hindi(d, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, 26, TXT, anchor="mm")
        else:
            pill(d, box, 35, labels[i], fonts[i], active=(i == 1))
        x += widths[i] + 16
    img.save(f"{OUT}/ui_home.png")
    return (540, 1400)

TOOL_ROWS = [
    ("3D Model Studio", "Geometry • photo relief • 360°", "grid"),
    ("Video Editor Pro", "Multi-track timeline editor", "film"),
    ("AI Ad Studio", tstr("استوديو الإعلانات"), "tag"),
    ("AI Music Studio", "Song ideas, lyrics & briefs", "note"),
    ("AI Image & Design Studio", "Posters, thumbnails, brand visuals", "img"),
    ("Text to Image", tstr("GPT Image 2.5 • نص إلى صورة"), "img"),
    ("Image to Video", tstr("صورة إلى فيديو"), "play"),
    ("Text to Song", tstr("Lyria 3.5 • نص إلى أغنية"), "note"),
    ("FAI AI Chat", tstr("مساعد الذكاء الاصطناعي"), "note"),
]

def s_tools():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Tools")
    txt(d, (60, 262), "Explore AI Tools", F(FB, 52), TXT)
    txt(d, (60, 344), "Find a tool and start in one tap.", F(FM, 28), TXT2)
    chips = ["All", "Image", "Video", "Music", "Film", "Business", "Entertainment"]
    x = 60
    for i, c in enumerate(chips):
        wch = d.textlength(c, font=F(FM, 26)) + 52
        pill(d, (x, 428, x + wch, 492), 32, c, F(FM, 26), active=(i == 0))
        x += wch + 14
    y = 540
    for i, (name, sub, kind) in enumerate(TOOL_ROWS):
        hl = (i == 4)
        rrect(d, (60, y, 1020, y + 118), 24, fill=CARD_HI if hl else CARD,
              outline=(168, 132, 255, 230) if hl else BORDER, width=3 if hl else 2)
        d.rounded_rectangle([84, y + 21, 160, y + 97], radius=18,
                            fill=(30, 36, 78, 255), outline=(139, 92, 246, 200), width=2)
        col = (168, 132, 255, 255)
        icx, icy = 122, y + 59
        if kind == "img": icon_image(d, icx, icy, col)
        elif kind == "play": icon_play(d, icx, icy, col)
        elif kind == "note": icon_note(d, icx, icy, col)
        elif kind == "film": icon_film(d, icx, icy, col)
        elif kind == "tag": icon_tag(d, icx, icy, col)
        else:
            for sx in (-1, 1):
                for sy in (-1, 1):
                    d.rounded_rectangle([icx + sx * 8 - 6, icy + sy * 8 - 6, icx + sx * 8 + 6, icy + sy * 8 + 6],
                                        radius=3, fill=col)
        txt(d, (192, y + 24), name, F(FB, 31), TXT)
        txt(d, (192, y + 70), sub, F(FM, 22), TXT2, shaped=any(ord(c) > 0x0590 for c in sub))
        y += 132
    img.save(f"{OUT}/ui_tools.png")
    return (540, 540 + 4 * 132 + 59)

PROMPT_PARTIAL = tstr("مدينة الرياض ليلية، برج الفيصلية، ألوان")
PROMPT_FULL = tstr("مدينة الرياض ليلية، برج الفيصلية، ألوان بنفسجية سينمائية، إضاءة درامية، جودة عالية")

def _image_common(img, d):
    status_bar(d)
    app_bar(d, img)
    nav(d, "Tools")
    d.polygon([(64, 258), (88, 238), (88, 252), (116, 252), (116, 264), (88, 264), (88, 278)], fill=TXT2)
    txt(d, (140, 258), "AI Image", F(FB, 48), TXT, anchor="lm")
    pill(d, (760, 226, 1020, 290), 32, "GPT Image 2.5 • 1K", F(FM, 24))

def s_image1():
    img = bg()
    d = ImageDraw.Draw(img)
    _image_common(img, d)
    rrect(d, (60, 340, 1020, 1010), 28, fill=(16, 20, 44, 235), outline=BORDER, width=2)
    txt(d, (92, 380), "YOUR PROMPT", F(FM, 24), TXT2)
    f = F(FM, 36)
    shaped = shape(PROMPT_PARTIAL)
    # simple wrap
    words, lines, cur = shaped.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if not cur or d.textlength(t, font=f) <= 880:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    yy = 450
    ex, ey = 92, 450
    for ln in lines:
        d.text((92, yy), ln, font=f, fill=TXT)
        ex = 92 + d.textlength(ln, font=f)
        ey = yy
        yy += 62
    d.rectangle([ex + 10, ey + 6, ex + 16, ey + 52], fill=(255, 255, 255, 235))
    chips = [("More Realistic", False), ("More Cinematic", True), ("More Luxury", False)]
    x = 60
    for label, act in chips:
        wc = d.textlength(label, font=F(FM, 26)) + 56
        pill(d, (x, 1082, x + wc, 1150), 34, label, F(FM, 26), active=act)
        x += wc + 16
    x = 60
    for i, r in enumerate(["9:16", "1:1", "16:9"]):
        wc = d.textlength(r, font=F(FM, 26)) + 48
        pill(d, (x, 1194, x + wc, 1262), 34, r, F(FM, 26), active=(i == 0))
        x += wc + 16
    d.ellipse([60, 1330, 96, 1366], fill=GOLD)
    txt(d, (112, 1348), "22 coins per image", F(FM, 26), TXT2, anchor="lm")
    grad_rrect(img, (270, 1420, 810, 1522), 51)
    txt(d, (540, 1471), "Create", F(FB, 42), TXT, anchor="mm")
    txt(d, (540, 1580), "Charged only when generation starts", F(FM, 22), (110, 118, 155, 255), anchor="mm")
    img.save(f"{OUT}/ui_image1.png")
    return None

def s_image2():
    img = bg()
    d = ImageDraw.Draw(img)
    _image_common(img, d)
    rrect(d, (60, 340, 1020, 1010), 28, fill=(16, 20, 44, 235), outline=BORDER, width=2)
    txt(d, (92, 380), "YOUR PROMPT", F(FM, 24), TXT2)
    f = F(FM, 36)
    shaped = shape(PROMPT_FULL)
    words, lines, cur = shaped.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if not cur or d.textlength(t, font=f) <= 880:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    yy = 450
    for ln in lines:
        d.text((92, yy), ln, font=f, fill=TXT)
        yy += 62
    rrect(d, (60, 1060, 1020, 1330), 28, fill=(16, 20, 44, 235), outline=(168, 132, 255, 220), width=3)
    txt(d, (540, 1130), "Creating your image…", F(FB, 36), TXT, anchor="mm")
    rrect(d, (150, 1200, 930, 1246), 23, fill=(28, 33, 70, 255))
    grad_rrect(img, (150, 1200, int(150 + 780 * 0.62), 1246), 23)
    txt(d, (540, 1292), "GPT Image 2.5 • 1K • 9:16", F(FM, 24), TXT2, anchor="mm")
    rrect(d, (270, 1400, 810, 1502), 51, fill=(24, 28, 60, 255), outline=BORDER, width=2)
    txt(d, (540, 1451), "Creating…", F(FB, 38), TXT2, anchor="mm")
    img.save(f"{OUT}/ui_image2.png")
    return None

def s_img2vid():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Tools")
    txt(d, (60, 258), "Image to Video", F(FB, 48), TXT, anchor="lm")
    txt(d, (1020, 262), tstr("صورة إلى فيديو"), F(FM, 28), TXT2, shaped=True, anchor="rm")
    rounded_paste(img, "video/s6b.png", (80, 360, 1000, 1180), 36)
    d = ImageDraw.Draw(img)
    d.ellipse([466, 696, 614, 844], fill=(8, 10, 26, 160), outline=(255, 255, 255, 230), width=4)
    d.polygon([(524, 740), (524, 800), (576, 770)], fill=(255, 255, 255, 240))
    rrect(d, (856, 1088, 988, 1148), 26, fill=(8, 10, 26, 200))
    txt(d, (922, 1118), "0:04", F(FM, 26), TXT, anchor="mm")
    chips = [("Saudi Arabic male narration", True), ("Epic cinematic soundtrack", False)]
    x = 60
    for label, act in chips:
        wc = d.textlength(label, font=F(FM, 26)) + 56
        pill(d, (x, 1252, x + wc, 1320), 34, label, F(FM, 26), active=act)
        x += wc + 16
    chips2 = [("Cinematic", True), ("Realistic", False), ("Saudi heritage", False)]
    x = 60
    for label, act in chips2:
        wc = d.textlength(label, font=F(FM, 26)) + 56
        pill(d, (x, 1362, x + wc, 1430), 34, label, F(FM, 26), active=act)
        x += wc + 16
    grad_rrect(img, (270, 1484, 810, 1586), 51)
    txt(d, (540, 1535), "Generate Video", F(FB, 40), TXT, anchor="mm")
    img.save(f"{OUT}/ui_img2vid.png")
    return (540, 770)

def s_storyfilm():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Projects")
    txt(d, (60, 258), "Story & Film Studio", F(FB, 46), TXT, anchor="lm")
    txt(d, (60, 322), tstr("قصتك • شخصياتك • فيلمك"), F(FM, 28), TXT2, shaped=True, anchor="lm")
    rrect(d, (60, 380, 1020, 860), 28, fill=(16, 20, 44, 235), outline=BORDER, width=2)
    grad_rrect(img, (92, 416, 268, 478), 30)
    txt(d, (180, 447), "SCENE 01", F(FB, 26), TXT, anchor="mm")
    d = ImageDraw.Draw(img)
    lines = ["A rider crosses the dunes at dusk.",
             "The city lights rise behind him.",
             "He stops — the skyline glows in his hand."]
    yy = 530
    for ln in lines:
        d.text((100, yy), "•  " + ln, font=F(FM, 30), fill=TXT)
        yy += 76
    txt(d, (60, 916), "STORYBOARD", F(FM, 24), TXT2)
    thumbs = [("video/s4c.png", "SCENE 01"), ("video/s3_result.png", "SCENE 02"),
              ("video/s6b.png", "SCENE 03")]
    for i, (src, tag) in enumerate(thumbs):
        x = 60 + i * (292 + 22)
        rounded_paste(img, src, (x, 966, x + 292, 1326), 24)
        d = ImageDraw.Draw(img)
        rrect(d, (x + 16, 1246, x + 16 + d.textlength(tag, font=F(FB, 22)) + 40, 1296),
              24, fill=(8, 10, 26, 210))
        txt(d, (x + 36, 1271), tag, F(FB, 22), TXT, anchor="lm")
    grad_rrect(img, (178, 1408, 658, 1510), 51)
    txt(d, (418, 1459), "Save Story", F(FB, 38), TXT, anchor="mm")
    rrect(d, (682, 1408, 902, 1510), 51, fill=(16, 20, 44, 220), outline=BORDER, width=2)
    txt(d, (792, 1459), "Add Scene", F(FB, 30), TXT, anchor="mm")
    txt(d, (540, 1580), tstr("بعض ميزات التوليد المتقدمة قيد مراجعة الخصوصية"), F(FM, 22),
        (150, 120, 255, 230), shaped=True, anchor="mm")
    img.save(f"{OUT}/ui_storyfilm.png")
    return None

def s_music():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Tools")
    txt(d, (60, 258), "AI Music Studio", F(FB, 46), TXT, anchor="lm")
    txt(d, (60, 322), "Text to Song • Lyria 3.5", F(FM, 28), TXT2, anchor="lm")
    rrect(d, (60, 380, 1020, 720), 28, fill=(16, 20, 44, 235), outline=BORDER, width=2)
    txt(d, (92, 416), "LYRICS", F(FM, 24), TXT2)
    txt(d, (92, 480), tstr("نص بسيط يتحول إلى أغنية كاملة"), F(FM, 34), TXT, shaped=True)
    txt(d, (92, 560), tstr("بكلماتك، بأسلوبك، بلهجتك"), F(FM, 34), (219, 183, 255, 255), shaped=True)
    rrect(d, (60, 760, 1020, 1080), 28, fill=(16, 20, 44, 235), outline=BORDER, width=2)
    import math
    n = 46
    bw, gapx = 12, (880 - n * 12) // (n - 1)
    for i in range(n):
        hgt = 40 + int(110 * abs(math.sin(i * 0.55)) * (0.6 + 0.4 * math.sin(i * 1.7 + 1)))
        t = i / (n - 1)
        c = tuple(int(ACC1[j] + (ACC2[j] - ACC1[j]) * t) for j in range(3))
        x = 100 + i * (bw + gapx)
        d.rounded_rectangle([x, 920 - hgt, x + bw, 920 + hgt], radius=6, fill=c + (235,))
    txt(d, (940, 1010), "03:27", F(FB, 30), TXT, anchor="rm")
    chips = [("Cinematic", True), ("Arabic", False), ("Male Voice", False)]
    x = 60
    for label, act in chips:
        wc = d.textlength(label, font=F(FM, 26)) + 56
        pill(d, (x, 1150, x + wc, 1218), 34, label, F(FM, 26), active=act)
        x += wc + 16
    grad_rrect(img, (270, 1290, 810, 1392), 51)
    txt(d, (540, 1341), "Generate Song", F(FB, 40), TXT, anchor="mm")
    txt(d, (540, 1450), "Lyrics + melody direction in one tool", F(FM, 22),
        (110, 118, 155, 255), anchor="mm")
    img.save(f"{OUT}/ui_music.png")
    return None

def s_ads():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Tools")
    txt(d, (60, 258), "AI Ad Studio", F(FB, 46), TXT, anchor="lm")
    txt(d, (1020, 262), tstr("استوديو الإعلانات"), F(FM, 28), TXT2, shaped=True, anchor="rm")
    rounded_paste(img, "video/s6b.png", (60, 350, 510, 800), 28)
    d = ImageDraw.Draw(img)
    rrect(d, (80, 726, 240, 780), 24, fill=(8, 10, 26, 210))
    txt(d, (110, 753), "PRODUCT", F(FB, 22), TXT, anchor="lm")
    rounded_paste(img, "video/s6b.png", (570, 350, 1020, 800), 28)
    ov = Image.new("RGBA", (450, 450), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.polygon([(0, 450), (450, 0), (450, 180), (180, 450)], fill=(124, 58, 237, 70))
    for (sx, sy, r) in [(360, 90, 5), (410, 140, 3), (60, 380, 4), (330, 400, 3), (40, 120, 3)]:
        od.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255, 220))
    mask = Image.new("L", (450, 450))
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 449, 449], radius=28, fill=255)
    ov.putalpha(mask)
    img.alpha_composite(ov, (570, 350))
    d = ImageDraw.Draw(img)
    rrect(d, (770, 726, 1000, 780), 24, fill=(8, 10, 26, 210))
    txt(d, (800, 753), "AD CREATIVE", F(FB, 22), TXT, anchor="lm")
    # arrow between cards
    d.line([(520, 575), (560, 575)], fill=(200, 200, 255, 200), width=4)
    d.polygon([(556, 556), (556, 594), (588, 575)], fill=(200, 200, 255, 220))
    tools = ["Product Photo Studio", "Hook Generator", "TikTok / Instagram Pack", "AI Brand Campaign"]
    pos = [(60, 880), (540, 880), (60, 980), (540, 980)]
    for (label, (px, py)) in zip(tools, pos):
        wc = d.textlength(label, font=F(FM, 25)) + 48
        pill(d, (px, py, px + wc, py + 68), 34, label, F(FM, 25))
    rrect(d, (60, 1090, 1020, 1330), 28, fill=(16, 20, 44, 235), outline=BORDER, width=2)
    rounded_paste(img, "video/s6b.png", (92, 1122, 212, 1298), 20)
    d = ImageDraw.Draw(img)
    txt(d, (252, 1150), "PRODUCT PHOTO STUDIO", F(FB, 28), TXT)
    txt(d, (252, 1210), tstr("صور منتجات احترافية"), F(FM, 26), TXT2, shaped=True)
    grad_rrect(img, (270, 1420, 810, 1522), 51)
    txt(d, (540, 1471), "Create Ad Creative", F(FB, 38), TXT, anchor="mm")
    img.save(f"{OUT}/ui_ads.png")
    return (540, 1471)

def hindi_width(d, size=40):
    f = F(FH, size)
    return f.getlength("ह") + f.getlength("न") + f.getlength("द")

def draw_hindi(d, x, y, size=40, fill=TXT, anchor="lm"):
    """Draw 'हिन्दी' with manually placed matras (PIL cannot shape Devanagari).
    (x, y) is on the text centerline; anchor lm = x is left edge, mm = x is center."""
    f = F(FH, size)
    w_h, w_n, w_d = f.getlength("ह"), f.getlength("न"), f.getlength("द")
    total = w_h + w_n + w_d
    x0 = x - total / 2 if anchor == "mm" else x
    y0 = y - size * 0.38
    d.text((x0, y0), "ह", font=f, fill=fill)
    d.text((x0 - w_h * 0.68, y0), "ि", font=f, fill=fill)
    x2 = x0 + w_h
    d.text((x2, y0), "न", font=f, fill=fill)
    x3 = x2 + w_n
    d.text((x3, y0), "द", font=f, fill=fill)
    d.text((x3 + w_d * 0.08, y0 - size * 0.62), "ी", font=f, fill=fill)
    return total

def s_lang():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Settings")
    txt(d, (60, 258), "Settings", F(FB, 48), TXT, anchor="lm")
    txt(d, (60, 322), "App language", F(FM, 28), TXT2, anchor="lm")
    note = "Choose your app language. Some studio labels are currently available in English."
    words, lines, cur = note.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if not cur or d.textlength(t, font=F(FM, 26)) <= 900:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    yy = 400
    for ln in lines:
        d.text((60, yy), ln, font=F(FM, 26), fill=TXT2)
        yy += 40
    rows = [("English", "lat"), (tstr("العربية"), "ar"), ("اردو", "ur"), ("हिन्दी", "dev")]
    y = 560
    for i, (label, kind) in enumerate(rows):
        act = (i == 1)
        rrect(d, (60, y, 1020, y + 118), 24, fill=CARD_HI if act else CARD,
              outline=(168, 132, 255, 230) if act else BORDER, width=3 if act else 2)
        if kind == "dev":
            draw_hindi(d, 100, y + 59, 40, TXT, anchor="lm")
        else:
            txt(d, (100, y + 59), label, F(FM, 40), TXT, shaped=(kind != "lat"), anchor="lm")
        if act:
            d.ellipse([930, y + 38, 986, y + 94], fill=(139, 92, 246, 255))
            d.polygon([(944, y + 66), (954, y + 78), (974, y + 50)], fill=(255, 255, 255, 255))
        y += 132
    img.save(f"{OUT}/ui_lang.png")
    return (540, 560 + 132 + 59)

def s_gaming():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Home")
    txt(d, (60, 258), "Gaming & Live", F(FB, 46), TXT, anchor="lm")
    txt(d, (60, 322), "Watch. Stream. Play.", F(FM, 28), TXT2, anchor="lm")
    rrect(d, (60, 380, 1020, 680), 28, fill=(26, 18, 44, 255), outline=(255, 70, 70, 180), width=3)
    rrect(d, (92, 420, 268, 484), 32, fill=(20, 12, 30, 255), outline=RED, width=2)
    d.ellipse([112, 438, 136, 462], fill=RED)
    txt(d, (152, 452), "LIVE", F(FB, 26), RED, anchor="lm")
    txt(d, (92, 540), "FAI LIVE", F(FB, 46), TXT)
    txt(d, (92, 606), "Live video • chat • gifts", F(FM, 26), TXT2)
    for i, (hx, hy, col) in enumerate([(830, 440, PINK), (900, 520, (90, 140, 255, 255)), (850, 610, PINK)]):
        r = 16
        d.ellipse([hx - r, hy - r, hx + r, hy + r], fill=col)
        d.polygon([(hx - r, hy + r - 6), (hx, hy + r + 18), (hx + r, hy + r - 6)], fill=col)
    txt(d, (60, 750), "FAI GAMES", F(FM, 24), TXT2)
    games = [("Quiz", "؟", F(FB, 40)), ("Memory", "◈", F(FV, 34)),
             ("Emoji", "☺", F(FV, 34)), ("Words", "أ", F(FB, 40))]
    for i, (g, ic, ifnt) in enumerate(games):
        x = 60 + (i % 2) * 486
        y = 800 + (i // 2) * 244
        rrect(d, (x, y, x + 462, y + 220), 26, fill=CARD, outline=BORDER, width=2)
        d.ellipse([x + 34, y + 68, x + 122, y + 156], fill=(30, 36, 78, 255),
                  outline=(139, 92, 246, 200), width=2)
        txt(d, (x + 78, y + 112), ic, ifnt, (168, 132, 255, 255),
            shaped=(ic in "أ"), anchor="mm")
        txt(d, (x + 156, y + 78), g, F(FB, 34), TXT)
        txt(d, (x + 156, y + 130), "Ready to play", F(FM, 22), TXT2)
    txt(d, (60, 1330), "FAI ENTERTAINMENT", F(FM, 24), TXT2)
    rrect(d, (60, 1380, 1020, 1700), 28, fill=CARD, outline=BORDER, width=2)
    ents = ["Full Movies", "Arabic Dubbed", "Hindi Action", "FAI Shorts", "Arabic Music", "Turkish"]
    for i, e in enumerate(ents):
        x = 92 + (i % 3) * 300
        y = 1420 + (i // 3) * 110
        pill(d, (x, y, x + 276, y + 80), 40, e, F(FM, 26), active=(i == 1))
    img.save(f"{OUT}/ui_gaming.png")
    return None

def s_account():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Settings")
    txt(d, (60, 258), "My Account", F(FB, 48), TXT, anchor="lm")
    d.ellipse([448, 380, 632, 564], outline=(139, 92, 246, 255), width=8)
    d.ellipse([456, 388, 624, 556], fill=(24, 28, 60, 255))
    txt(d, (540, 472), "F", F(FB, 84), (168, 132, 255, 255), anchor="mm")
    txt(d, (540, 640), "Guest creator", F(FB, 38), TXT, anchor="mm")
    txt(d, (540, 700), "Sign in to sync creations and coins", F(FM, 26), TXT2, anchor="mm")
    stats = [("Coins", "0"), ("Plan", "Free"), ("Projects", "0")]
    for i, (k, v) in enumerate(stats):
        x = 60 + i * (292 + 22)
        rrect(d, (x, 780, x + 292, 950), 26, fill=CARD, outline=BORDER, width=2)
        txt(d, (x + 146, 830), k, F(FM, 24), TXT2, anchor="mm")
        txt(d, (x + 146, 896), v, F(FB, 44), GOLD if k == "Coins" else TXT, anchor="mm")
    grad_rrect(img, (270, 1030, 810, 1132), 51)
    txt(d, (540, 1081), "Sign in to FAI Create", F(FB, 36), TXT, anchor="mm")
    rrect(d, (60, 1210, 1020, 1560), 28, fill=(16, 20, 44, 235), outline=BORDER, width=2)
    txt(d, (92, 1250), "REWARDS & REFERRALS", F(FM, 24), TXT2)
    txt(d, (92, 1306), "Free coins every day", F(FB, 34), TXT)
    d.text((92, 1372), "Claim 10 coins daily. Reach a 7-day streak for 25 coins.",
           font=F(FM, 26), fill=TXT2)
    d.text((92, 1416), "Invite a friend — both accounts get 20 coins.",
           font=F(FM, 26), fill=TXT2)
    d.ellipse([92, 1470, 128, 1506], fill=GOLD)
    txt(d, (148, 1488), "Sign in to claim", F(FB, 26), GOLD, anchor="lm")
    img.save(f"{OUT}/ui_account.png")
    return (540, 1081)

def s_plans():
    img = bg()
    d = ImageDraw.Draw(img)
    status_bar(d)
    app_bar(d, img)
    nav(d, "Plans")
    txt(d, (60, 258), "Plans & Coins", F(FB, 48), TXT, anchor="lm")
    txt(d, (60, 322), "Choose how you want to create", F(FM, 26), TXT2, anchor="lm")
    rrect(d, (60, 380, 1020, 464), 42, fill=(16, 20, 44, 220), outline=BORDER, width=2)
    rrect(d, (548, 388, 1012, 456), 34, fill=(30, 26, 66, 255), outline=(139, 92, 246, 220), width=2)
    txt(d, (300, 422), "Monthly", F(FM, 28), TXT2, anchor="mm")
    txt(d, (660, 422), "Annual", F(FB, 28), TXT, anchor="mm")
    txt(d, (920, 422), "2 months free", F(FB, 22), GOLD, anchor="mm")
    # Free
    rrect(d, (60, 500, 1020, 730), 26, fill=CARD, outline=BORDER, width=2)
    txt(d, (92, 540), "Free", F(FB, 34), TXT)
    txt(d, (990, 552), "0 SAR", F(FB, 40), GOLD, anchor="rm")
    txt(d, (92, 600), "100 signup coins", F(FM, 25), TXT2)
    txt(d, (92, 652), "•  Explore image, voice and creator tools", F(FM, 24), TXT2)
    # Creator (popular)
    rrect(d, (60, 760, 1020, 1050), 26, fill=CARD_HI, outline=(168, 132, 255, 255), width=3)
    grad_rrect(img, (688, 740, 1012, 800), 30)
    d = ImageDraw.Draw(img)
    txt(d, (850, 770), "MOST POPULAR", F(FB, 22), TXT, anchor="mm")
    txt(d, (92, 812), "Creator", F(FB, 34), TXT)
    txt(d, (990, 824), "49 SAR/month", F(FB, 38), GOLD, anchor="rm")
    txt(d, (92, 872), "1,000 coins per 30 days", F(FM, 25), TXT2)
    txt(d, (92, 924), "•  Full saved creation library", F(FM, 24), TXT2)
    txt(d, (92, 968), "•  Priority access to new FAI tools", F(FM, 24), TXT2)
    # Pro
    rrect(d, (60, 1080, 1020, 1370), 26, fill=CARD, outline=BORDER, width=2)
    txt(d, (92, 1122), "Pro", F(FB, 34), TXT)
    txt(d, (990, 1134), "99 SAR/month", F(FB, 38), GOLD, anchor="rm")
    txt(d, (92, 1182), "2,500 coins per 30 days", F(FM, 25), TXT2)
    txt(d, (92, 1234), "•  Larger monthly coin allowance", F(FM, 24), TXT2)
    txt(d, (92, 1278), "•  Best value for high-volume creators", F(FM, 24), TXT2)
    txt(d, (60, 1420), "ONE-TIME TOP UPS", F(FM, 22), TXT2)
    ups = ["200  •  10 SAR", "600  •  25 SAR", "1,500  •  50 SAR"]
    x = 60
    for u in ups:
        wc = d.textlength(u, font=F(FM, 26)) + 52
        pill(d, (x, 1466, x + wc, 1534), 34, u, F(FM, 26))
        x += wc + 16
    grad_rrect(img, (270, 1600, 810, 1702), 51)
    txt(d, (540, 1651), "Start Free", F(FB, 40), TXT, anchor="mm")
    img.save(f"{OUT}/ui_plans.png")
    return (540, 1651)

# ================= CARD BLUR-PAD BEATS =================
def card_pad(src, out):
    im = Image.open(src).convert("RGB")
    s = max(W / im.width, H / im.height)
    bgi = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = (bgi.width - W) // 2
    y = (bgi.height - H) // 2
    bgi = bgi.crop((x, y, x + W, y + H))
    bgi = bgi.filter(ImageFilter.GaussianBlur(26))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 150))
    canvas = bgi.convert("RGBA")
    canvas.alpha_composite(dark)
    s2 = W / im.width
    sharp = im.resize((W, int(im.height * s2)), Image.LANCZOS)
    canvas.alpha_composite(sharp.convert("RGBA"), (0, (H - sharp.height) // 2))
    canvas.save(out)
    print("card", out)

# ================= TAP SPRITES =================
def tap_sprites():
    dot = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dot)
    dd.ellipse([20, 20, 180, 180], fill=(139, 92, 246, 90))
    dd.ellipse([50, 50, 150, 150], fill=(255, 255, 255, 255))
    dd.ellipse([62, 62, 138, 138], fill=(139, 92, 246, 255))
    dot.save("build/dot.png")
    for i in range(18):
        r = 40 + i * 15
        a = int(200 * (1 - i / 18))
        fr = Image.new("RGBA", (520, 520), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fr)
        fd.ellipse([260 - r, 260 - r, 260 + r, 260 + r], outline=(190, 150, 255, a), width=6)
        fr.save(f"build/ripple/ripple_{i:02d}.png")
    print("sprites ok")

# ================= VERIFY + MAIN =================
def verify():
    from fontTools.ttLib import TTFont
    cj = TTFont(FB).getBestCmap()
    cv = TTFont(FV).getBestCmap()
    for t in _ALL_TEXTS:
        for c in shape(t):
            if ord(c) not in cj and ord(c) not in cv:
                raise SystemExit(f"GLYPH MISSING {hex(ord(c))} in {t!r}")
    for c in "•…—→✓●◈☺؟أ0123456789 SAR/:•%":
        if ord(c) not in cj and ord(c) not in cv:
            raise SystemExit(f"GLYPH MISSING direct {hex(ord(c))}")
    print("glyphs covered:", len(_ALL_TEXTS), "strings")

def main():
    verify()
    tap_sprites()
    print("home", s_home())
    print("tools", s_tools())
    print("image1", s_image1())
    print("image2", s_image2())
    print("img2vid", s_img2vid())
    print("storyfilm", s_storyfilm())
    print("music", s_music())
    print("ads", s_ads())
    print("lang", s_lang())
    print("gaming", s_gaming())
    print("account", s_account())
    print("plans", s_plans())
    card_pad("assets/ref_hero.png", f"{OUT}/card_hero.png")
    card_pad("assets/ref_tools.png", f"{OUT}/card_tools.png")
    card_pad("assets/ref_story.png", f"{OUT}/card_story.png")
    card_pad("assets/ref_live.png", f"{OUT}/card_live.png")
    print("done")

if __name__ == "__main__":
    main()
