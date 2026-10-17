#!/usr/bin/env python3
"""Render Arabic subtitle cue PNGs + scene-9 logo text PNGs (transparent blocks)."""
import os
import arabic_reshaper
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_B = "assets/Tajawal-Bold.ttf"
FONT_M = "assets/Tajawal-Medium.ttf"
OUT = "build/subs"
os.makedirs(OUT, exist_ok=True)

CUES = [
    (1, "تخيّل أن أفكارك تتحول إلى واقع!"),
    (1, "صورة من كلماتك، فيديو من خيالك، وتصميم يعكس إبداعك. مرحباً بك في FAI CREATE!"),
    (2, "مع FAI CREATE، أدوات الإبداع أصبحت في مكان واحد."),
    (2, "منصة ذكية تجمع التصميم، صناعة المحتوى، الفيديو والمشاريع الرقمية. ابدأ رحلتك الإبداعية اليوم!"),
    (3, "اكتب فكرتك وحوّلها إلى صورة مميزة."),
    (3, "استكشف تصميم الصور، تحسين الجودة، واستوديو المنتجات والإعلانات. أدوات تساعدك على صناعة محتوى يلفت الأنظار."),
    (4, "خلّ أفكارك تتحرك!"),
    (4, "اكتشف أدوات تحويل الصور والنصوص إلى فيديو، وصناعة المقاطع القصيرة والمؤثرات السينمائية لمحتواك."),
    (5, "استكشف استوديو القصص والأفلام، تخطيط المشاهد، واستوديو الموسيقى لكتابة كلمات الأغاني."),
    (5, "بعض ميزات التوليد المتقدمة قيد مراجعة الخصوصية."),
    (6, "عندك متجر أو مشروع؟ جهّز أفكاراً إعلانية، محتوى المنتجات ومنشورات التواصل الاجتماعي."),
    (6, "واستفد من المساعد الذكي وأدوات بناء المشاريع."),
    (7, "الإبداع ما له حدود!"),
    (7, "استكشف أدوات تدعم العربية والإنجليزية ولغات أخرى بحسب إمكانيات كل أداة. واكتشف الألعاب والترفيه!"),
    (8, "سجّل حسابك الآن، واستكشف الأدوات المتاحة للتجربة، والباقات والعملات المناسبة لاحتياجاتك."),
]

import unicodedata

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


def _fix(s: str) -> str:
    """Map presentation forms missing from the font back to base letters."""
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
            if base in _BASE_BY_NAME:
                out.append(chr(_BASE_BY_NAME[base]))
            else:
                out.append(c)
        else:
            out.append(c)
    return "".join(out)


def shape(text: str) -> str:
    return get_display(_fix(arabic_reshaper.reshape(text)))


def wrap_lines(draw, text, font, maxw):
    """Wrap in LOGICAL order, then shape each line.

    Wrapping the bidi-shaped (visually reversed) string reverses the line
    order of multi-line cues — the first logical line must stay on top.
    """
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if not cur or draw.textlength(shape(t), font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return [shape(l) for l in lines]


def render_cue(idx, text, font_size=50, maxw=860):
    font = ImageFont.truetype(FONT_B, font_size)
    tmp = Image.new("RGBA", (16, 16))
    d = ImageDraw.Draw(tmp)
    lines = wrap_lines(d, text, font, maxw)
    if len(lines) > 3:  # shrink
        font = ImageFont.truetype(FONT_B, 44)
        lines = wrap_lines(d, text, font, maxw)
    lw = [d.textlength(l, font=font) for l in lines]
    asc, desc = font.getmetrics()
    lh = int(font.size * 1.58)
    pad = 30
    w = int(max(lw)) + pad * 2
    h = lh * len(lines) + pad * 2 - (lh - (asc + desc))
    W, H = w + 120, h + 120
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i, l in enumerate(lines):
        gd.text(((W - d.textlength(l, font=font)) / 2, 60 + pad - 10 + i * lh), l,
                font=font, fill=(138, 60, 255, 235))
    glow = glow.filter(ImageFilter.GaussianBlur(15))
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas = Image.alpha_composite(canvas, glow)
    cd = ImageDraw.Draw(canvas)
    cd.rounded_rectangle([60, 60, 60 + w, 60 + h], radius=26,
                         fill=(10, 8, 32, 168), outline=(152, 104, 255, 120), width=2)
    for i, l in enumerate(lines):
        x = (W - d.textlength(l, font=font)) / 2
        y = 60 + pad - 10 + i * lh
        cd.text((x + 3, y + 4), l, font=font, fill=(0, 0, 0, 210))
        cd.text((x, y), l, font=font, fill=(255, 255, 255, 255))
    path = f"{OUT}/cue{idx:02d}.png"
    canvas.save(path)
    return path, W, H


def render_plain(text, font, y_center_pad=0, glow_color=(140, 70, 255, 255),
                 text_color=(255, 255, 255, 255), glow_blur=12, box=False):
    tmp = Image.new("RGBA", (16, 16))
    d = ImageDraw.Draw(tmp)
    shaped = shape(text)
    tw = d.textlength(shaped, font=font)
    asc, desc = font.getmetrics()
    pad = 26
    W = int(tw) + pad * 2 + 100
    H = asc + desc + pad * 2 + 100
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.text(((W - tw) / 2, pad + 50 + y_center_pad), shaped, font=font, fill=glow_color)
    glow = glow.filter(ImageFilter.GaussianBlur(glow_blur))
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    canvas = Image.alpha_composite(canvas, glow)
    cd = ImageDraw.Draw(canvas)
    if box:
        cd.rounded_rectangle([50, 50, 50 + int(tw) + pad * 2, 50 + asc + desc + pad * 2],
                             radius=22, fill=(10, 8, 32, 150), outline=(152, 104, 255, 110), width=2)
    cd.text(((W - tw) / 2 + 2, pad + 50 + y_center_pad + 3), shaped, font=font, fill=(0, 0, 0, 200))
    cd.text(((W - tw) / 2, pad + 50 + y_center_pad), shaped, font=font, fill=text_color)
    return canvas


def verify(font_path, texts):
    from fontTools.ttLib import TTFont
    cmap = TTFont(font_path).getBestCmap()
    for t in texts:
        for c in shape(t):
            if ord(c) not in cmap:
                raise SystemExit(f"GLYPH MISSING: {hex(ord(c))} in {t!r}")
    print("all glyphs covered")


def main():
    import json
    meta = {}
    for i, (sc, text) in enumerate(CUES, start=1):
        p, W, H = render_cue(i, text)
        meta[f"cue{i:02d}"] = {"scene": sc, "w": W, "h": H}
        print("cue", i, sc, W, H)

    tag = render_plain("خيالك يصنع المستقبل!", ImageFont.truetype(FONT_B, 64),
                       glow_blur=14)
    tag.save(f"{OUT}/tagline.png")
    meta["tagline"] = {"w": tag.width, "h": tag.height}
    dom = render_plain("faicreate.co", ImageFont.truetype(FONT_M, 62),
                       glow_color=(120, 90, 255, 230), glow_blur=10,
                       text_color=(226, 224, 255, 255))
    dom.save(f"{OUT}/domain.png")
    meta["domain"] = {"w": dom.width, "h": dom.height}
    with open(f"{OUT}/meta.json", "w") as f:
        json.dump(meta, f)
    print("done")


if __name__ == "__main__":
    verify(FONT_B, [t for _, t in CUES] + ["خيالك يصنع المستقبل!", "faicreate.co"])
    main()
