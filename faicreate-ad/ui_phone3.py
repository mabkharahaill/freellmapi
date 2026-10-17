#!/usr/bin/env python3
"""v3 phone-screen UIs (1080x2340, 9:19.5) rendered from the real 1920 screens
+ real bottom-fold content, plus animated UI frame sequences (tap / scroll /
typing / page-change / progress) for the phone-in-hand composite beats."""
import math
import os

import arabic_reshaper
from bidi.algorithm import get_display
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import ui_kit as K

W, H = 1080, 2340          # phone screen canvas
W19, H19 = 1080, 1920      # existing screen size
NAV_Y = 2230               # nav bar top in 2340 layout
UIQ = "build/uiq"          # static 2340 screens
SEQ = "build/uiseq3"       # animated sequences
os.makedirs(UIQ, exist_ok=True)
os.makedirs(SEQ, exist_ok=True)

# ---------------- geometry helpers ----------------

def bg340():
    """Tall vertical gradient background (same palette as ui_kit.bg)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    top, bot = K.BG_TOP, K.BG_BOT
    px = img.load()
    for y in range(H):
        t = y / H
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for x in range(0, W, 4):
            px[x, y] = c + (255,)
            px[x + 1, y] = c + (255,)
            px[x + 2, y] = c + (255,)
            px[x + 3, y] = c + (255,)
    return img


def base19(name):
    return Image.open(f"build/ui/ui_{name}.png").convert("RGBA")


def nav_strip():
    tmp = Image.new("RGBA", (W19, H19), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    K.nav(d, "Home")
    return tmp.crop((0, 1810, 1080, 1920))


def screen2340(name, ext_fn):
    """top 1810px of existing screen + bottom-fold extension + nav at 2230."""
    b19 = base19(name)
    img = bg340()
    img.alpha_composite(b19.crop((0, 0, 1080, 1810)), (0, 0))
    d = ImageDraw.Draw(img)
    ext_fn(img, d)
    img.alpha_composite(nav_strip(), (0, NAV_Y))
    img.save(f"{UIQ}/uiq_{name}.png")
    return img


def cover_fit(src_path, box, r=24):
    src = Image.open(src_path).convert("RGBA")
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    s = max(tw / src.width, th / src.height)
    src = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.LANCZOS)
    sx = (src.width - tw) // 2
    sy = (src.height - th) // 2
    src = src.crop((sx, sy, sx + tw, sy + th))
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, tw - 1, th - 1], radius=r, fill=255)
    return src, mask


def paste_thumb(img, src_path, box, r=24, tag=None, tag_fsize=22):
    x0, y0, x1, y1 = box
    tw, th = x1 - x0, y1 - y0
    src, mask = cover_fit(src_path, box, r)
    img.paste(src, (x0, y0), mask)
    if tag:
        d = ImageDraw.Draw(img)
        twd = d.textlength(tag, font=K.F(K.FB, tag_fsize))
        K.rrect(d, (x0 + 16, y1 - 66, x0 + 16 + twd + 40, y1 - 16), 24, fill=(8, 10, 26, 210))
        K.txt(d, (x0 + 36, y1 - 41), tag, K.F(K.FB, tag_fsize), K.TXT, anchor="lm")


def icon_circle(d, cx, cy, kind):
    d.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=(30, 36, 78, 255),
              outline=(139, 92, 246, 200), width=2)
    col = (168, 132, 255, 255)
    if kind == "img":
        K.icon_image(d, cx, cy, col)
    elif kind == "play":
        K.icon_play(d, cx, cy, col)
    elif kind == "note":
        K.icon_note(d, cx, cy, col)
    elif kind == "film":
        K.icon_film(d, cx, cy, col)
    elif kind == "tag":
        K.icon_tag(d, cx, cy, col)
    else:
        for sx in (-1, 1):
            for sy in (-1, 1):
                d.rounded_rectangle([cx + sx * 8 - 6, cy + sy * 8 - 6, cx + sx * 8 + 6, cy + sy * 8 + 6],
                                    radius=3, fill=col)


# ---------------- bottom-fold extensions (REAL site content) ----------------

def ext_home(img, d):
    cards = [("img", "Make a voiceover", K.tstr("نص إلى صوت")),
             ("tag", "Make a product ad", K.tstr("استوديو الإعلانات"))]
    cw, chh, gap = 468, 252, 24
    y0 = 1780
    for i, (k, title, sub) in enumerate(cards):
        cx0 = 60 + i * (cw + gap)
        K.rrect(d, (cx0, y0, cx0 + cw, y0 + chh), 26, fill=K.CARD, outline=K.BORDER, width=2)
        icon_circle(d, cx0 + 76, y0 + 76, k)
        K.txt(d, (cx0 + 36, y0 + 152), title, K.F(K.FB, 34), K.TXT)
        K.txt(d, (cx0 + 36, y0 + 198), sub, K.F(K.FM, 23), K.TXT2, shaped=True)


def ext_tools(img, d):
    rows = [("FAI Social Studio", K.tstr("منشورات جاهزة للناشرين"), "tag"),
            ("My Projects Cloud", K.tstr("مشاريعك محفوظة في الغيمة"), "grid"),
            ("FAI Project Builder", "Build Your Shop • Build Your Project", "film")]
    y = 1742
    for name, sub, kind in rows:
        K.rrect(d, (60, y, 1020, y + 118), 24, fill=K.CARD, outline=K.BORDER, width=2)
        d.rounded_rectangle([84, y + 21, 160, y + 97], radius=18,
                            fill=(30, 36, 78, 255), outline=(139, 92, 246, 200), width=2)
        icon_circle(d, 122, y + 59, kind)
        K.txt(d, (192, y + 24), name, K.F(K.FB, 31), K.TXT)
        K.txt(d, (192, y + 70), sub, K.F(K.FM, 22), K.TXT2, shaped=any(ord(c) > 0x0590 for c in sub))
        y += 132


THUMBS_A = [("video/v3_riyadh_night.png", "Riyadh night"),
            ("video/v3_perfume.png", "Perfume studio"),
            ("video/v3_supercar.png", "Neon drift")]


def _thumbs_row(img, d, y, thumbs, label):
    K.txt(d, (60, y - 34), label, K.F(K.FM, 24), K.TXT2)
    for i, (src, tag) in enumerate(thumbs):
        x = 60 + i * (292 + 22)
        paste_thumb(img, src, (x, y, x + 292, y + 340), 24, tag)


def ext_image(img, d):
    _thumbs_row(img, d, 1660, THUMBS_A, "YOUR CREATIONS — SAVED IN MY PROJECTS")


def ext_img2vid(img, d):
    thumbs = [("video/v3_supercar.png", "Supercar Chase"),
              ("video/v3_riyadh_night.png", "City Night Drive"),
              ("video/v3_perfume.png", "Product Reel")]
    _thumbs_row(img, d, 1660, thumbs, "SHORT VIDEO LIBRARY")


def ext_storyfilm(img, d):
    scenes = [("SCENE 02", "The skyline fills the screen."),
              ("SCENE 03", "The product glows in the night.")]
    y = 1660
    for tag, line in scenes:
        K.rrect(d, (60, y, 1020, y + 168), 24, fill=(16, 20, 44, 235), outline=K.BORDER, width=2)
        K.grad_rrect(img, (92, y + 26, 268, y + 88), 30)
        d = ImageDraw.Draw(img)
        K.txt(d, (180, y + 57), tag, K.F(K.FB, 26), K.TXT, anchor="mm")
        K.txt(d, (320, y + 57), line, K.F(K.FM, 27), K.TXT, anchor="lm")
        K.txt(d, (320, y + 108), K.tstr("شخصياتك • مواقعك • إضاءتك"), K.F(K.FM, 22), K.TXT2,
              shaped=True, anchor="lm")
        y += 182


def ext_ads(img, d):
    K.txt(d, (60, 1560), "TEMPLATES", K.F(K.FM, 24), K.TXT2)
    t1 = ["Cinematic Reel", "TikTok Product Ad", "Ramadan Kareem Poster"]
    t2 = ["Saudi National Day", "UGC Review", "Unboxing Reel"]
    x = 60
    for label in t1:
        wc = d.textlength(label, font=K.F(K.FM, 25)) + 48
        K.pill(d, (x, 1596, x + wc, 1664), 34, label, K.F(K.FM, 25))
        x += wc + 16
    x = 60
    for label in t2:
        wc = d.textlength(label, font=K.F(K.FM, 25)) + 48
        K.pill(d, (x, 1684, x + wc, 1752), 34, label, K.F(K.FM, 25))
        x += wc + 16
    paste_thumb(img, "video/v3_perfume.png", (60, 1800, 480, 2160), 24, "Cinematic Reel")
    paste_thumb(img, "video/v3_supercar.png", (510, 1800, 930, 2160), 24, "TikTok Product Ad")


def ext_lang(img, d):
    K.rrect(d, (60, 1200, 1020, 1480), 24, fill=K.CARD, outline=K.BORDER, width=2)
    K.txt(d, (92, 1244), "NOTIFICATIONS", K.F(K.FM, 24), K.TXT2)
    K.txt(d, (92, 1300), "Generation finished", K.F(K.FB, 30), K.TXT)
    K.txt(d, (92, 1352), "Get notified when a creation is ready.", K.F(K.FM, 24), K.TXT2)
    d.rounded_rectangle([866, 1288, 966, 1344], radius=28, fill=(139, 92, 246, 255))
    d.ellipse([912, 1302, 952, 1330], fill=(255, 255, 255, 255))
    K.rrect(d, (60, 1520, 1020, 1800), 24, fill=K.CARD, outline=K.BORDER, width=2)
    K.txt(d, (92, 1564), "ABOUT", K.F(K.FM, 24), K.TXT2)
    K.txt(d, (92, 1620), "FAI CREATE — All-in-one AI Creator", K.F(K.FB, 30), K.TXT)
    K.txt(d, (92, 1672), "Design, content, video and digital projects.", K.F(K.FM, 24), K.TXT2)
    K.txt(d, (92, 1724), "faicreate.co", K.F(K.FM, 24), (168, 132, 255, 255))


def ext_gaming(img, d):
    K.txt(d, (60, 1740), "LIVE NOW", K.F(K.FM, 24), K.TXT2)
    srcs = [("video/s7b.png", "FAI Quiz Night"), ("video/v3_supercar.png", "Neon GP"),
            ("video/v3_riyadh_night.png", "City Stream")]
    for i, (src, tag) in enumerate(srcs):
        x = 60 + i * (292 + 22)
        paste_thumb(img, src, (x, 1776, x + 292, 2036), 24, tag)
        d = ImageDraw.Draw(img)
        K.rrect(d, (x + 16, 1800, x + 118, 1848), 20, fill=(20, 12, 30, 255),
                outline=(255, 70, 70, 220), width=2)
        d.ellipse([x + 32, 1816, x + 48, 1832], fill=(255, 70, 70, 255))
        K.txt(d, (x + 60, 1824), "LIVE", K.F(K.FB, 20), (255, 90, 90, 255), anchor="lm")


def ext_account(img, d):
    K.rrect(d, (60, 1620, 1020, 1900), 24, fill=(16, 20, 44, 235), outline=K.BORDER, width=2)
    K.txt(d, (92, 1664), "MY PROJECTS CLOUD", K.F(K.FM, 24), K.TXT2)
    K.txt(d, (92, 1720), "0 projects", K.F(K.FB, 34), K.TXT)
    K.txt(d, (92, 1776), "Sign in to sync your saved creations.", K.F(K.FM, 24), K.TXT2)
    K.rrect(d, (60, 1940, 1020, 2160), 24, fill=K.CARD, outline=K.BORDER, width=2)
    K.txt(d, (92, 1984), "STORAGE", K.F(K.FM, 24), K.TXT2)
    K.rrect(d, (92, 2040, 988, 2072), 16, fill=(28, 33, 70, 255))
    K.grad_rrect(img, (92, 2040, 260, 2072), 16)
    K.txt(d, (92, 2110), "Free plan — creations keep for 30 days", K.F(K.FM, 22), K.TXT2)


def ext_plans(img, d):
    K.rrect(d, (60, 1740, 1020, 1980), 24, fill=(16, 20, 44, 235), outline=K.BORDER, width=2)
    K.txt(d, (92, 1784), "GOOD TO KNOW", K.F(K.FM, 24), K.TXT2)
    K.txt(d, (92, 1840), "Annual plans include two months free.", K.F(K.FM, 26), K.TXT)
    K.txt(d, (92, 1888), "Opening tools does not start paid generation.", K.F(K.FM, 26), K.TXT2)
    K.rrect(d, (60, 2020, 1020, 2180), 24, fill=K.CARD, outline=K.BORDER, width=2)
    K.txt(d, (92, 2064), "COINS", K.F(K.FM, 24), K.TXT2)
    K.txt(d, (92, 2116), "10 coins daily • 25 for a 7-day streak", K.F(K.FM, 25), K.TXT2)


EXTS = {
    "home": ext_home, "tools": ext_tools, "image1": ext_image, "image2": ext_image,
    "img2vid": ext_img2vid, "storyfilm": ext_storyfilm, "ads": ext_ads,
    "lang": ext_lang, "gaming": ext_gaming, "account": ext_account, "plans": ext_plans,
}


def render_statics():
    for name, fn in EXTS.items():
        screen2340(name, fn)
        print(f"screen {name} ok")


# ---------------- result views (app screens, 2340) ----------------

def header(d, canvas, title, sub_ar=None, chip="GPT Image 2.5 • 1K"):
    K.status_bar(d)
    K.app_bar(d, canvas)
    d.polygon([(64, 258), (88, 238), (88, 252), (116, 252), (116, 264), (88, 264), (88, 278)], fill=K.TXT2)
    K.txt(d, (140, 258), title, K.F(K.FB, 48), K.TXT, anchor="lm")
    if sub_ar:
        K.txt(d, (1020, 262), K.tstr(sub_ar), K.F(K.FM, 28), K.TXT2, shaped=True, anchor="rm")
    K.pill(d, (760, 226, 1020, 290), 32, chip, K.F(K.FM, 24))


def img_result():
    img = K.bg() if False else bg340()
    d = ImageDraw.Draw(img)
    header(d, img, "AI Image", "نص إلى صورة", "GPT Image 2.5 • 1K")
    paste_thumb(img, "video/v3_riyadh_night.png", (60, 340, 1020, 1300), 28)
    d = ImageDraw.Draw(img)
    K.grad_rrect(img, (150, 1380, 650, 1482), 51)
    K.txt(d, (400, 1431), "Save to My Projects", K.F(K.FB, 36), K.TXT, anchor="mm")
    K.rrect(d, (674, 1380, 930, 1482), 51, fill=(16, 20, 44, 220), outline=K.BORDER, width=2)
    K.txt(d, (802, 1431), "New", K.F(K.FB, 34), K.TXT, anchor="mm")
    K.txt(d, (540, 1560), "22 coins used • GPT Image 2.5 • 1K • 9:16", K.F(K.FM, 24), K.TXT2, anchor="mm")
    _thumbs_row(img, d, 1720, THUMBS_A, "RECENTLY SAVED")
    img.alpha_composite(nav_strip(), (0, NAV_Y))
    img.save(f"{UIQ}/uiq_img_result.png")


def vid_player(progress=0.0):
    img = bg340()
    d = ImageDraw.Draw(img)
    header(d, img, "Image to Video", "صورة إلى فيديو")
    paste_thumb(img, "video/v3_supercar.png", (80, 340, 1000, 1160), 36)
    d = ImageDraw.Draw(img)
    d.rectangle([80, 1040, 1000, 1160], fill=(8, 10, 26, 120))
    K.rrect(d, (112, 1076, 968, 1100), 12, fill=(8, 10, 26, 180))
    K.grad_rrect(img, (112, 1076, 112 + int(856 * max(0.02, progress)), 1100), 12)
    K.txt(d, (950, 1038), "0:04", K.F(K.FM, 24), K.TXT, anchor="rm")
    d.ellipse([466, 660, 614, 808], fill=(8, 10, 26, 160), outline=(255, 255, 255, 230), width=4)
    d.polygon([(524, 704), (524, 764), (576, 734)], fill=(255, 255, 255, 240))
    chips = [("Saudi Arabic male narration", True), ("Epic cinematic soundtrack", False)]
    x = 60
    for label, act in chips:
        wc = d.textlength(label, font=K.F(K.FM, 26)) + 56
        K.pill(d, (x, 1230, x + wc, 1298), 34, label, K.F(K.FM, 26), active=act)
        x += wc + 16
    K.grad_rrect(img, (270, 1360, 810, 1462), 51)
    K.txt(d, (540, 1411), "Download", K.F(K.FB, 40), K.TXT, anchor="mm")
    K.rrect(d, (60, 1540, 1020, 1860), 28, fill=(16, 20, 44, 235), outline=K.BORDER, width=2)
    K.txt(d, (92, 1584), "SCENE BRIEF", K.F(K.FM, 24), K.TXT2)
    K.txt(d, (92, 1640), "A supercar drifts through the neon city.", K.F(K.FM, 28), K.TXT)
    K.txt(d, (92, 1692), K.tstr("إضاءة سينمائية، تفاصيل عالية، حركة طبيعية"), K.F(K.FM, 26), K.TXT2,
          shaped=True)
    _thumbs_row(img, d, 1960, [("video/v3_supercar.png", "Supercar Chase"),
                               ("video/v3_riyadh_night.png", "City Night Drive"),
                               ("video/v3_perfume.png", "Product Reel")], "SHORT VIDEO LIBRARY")
    img.alpha_composite(nav_strip(), (0, NAV_Y))
    return img


def ad_preview():
    img = bg340()
    d = ImageDraw.Draw(img)
    header(d, img, "AI Ad Studio", "استوديو الإعلانات")
    paste_thumb(img, "video/v3_perfume.png", (60, 340, 510, 790), 28)
    d = ImageDraw.Draw(img)
    K.rrect(d, (80, 716, 240, 770), 24, fill=(8, 10, 26, 210))
    K.txt(d, (110, 743), "PRODUCT", K.F(K.FB, 22), K.TXT, anchor="lm")
    paste_thumb(img, "video/v3_perfume.png", (570, 340, 1020, 790), 28)
    ov = Image.new("RGBA", (450, 450), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.polygon([(0, 450), (450, 0), (450, 180), (180, 450)], fill=(124, 58, 237, 90))
    od.text((40, 330), "FAI CREATE", font=K.F(K.FB, 34), fill=(255, 255, 255, 235))
    mask = Image.new("L", (450, 450))
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 449, 449], radius=28, fill=255)
    ov.putalpha(mask)
    img.alpha_composite(ov, (570, 340))
    d = ImageDraw.Draw(img)
    K.rrect(d, (770, 716, 1000, 770), 24, fill=(8, 10, 26, 210))
    K.txt(d, (800, 743), "AD CREATIVE", K.F(K.FB, 22), K.TXT, anchor="lm")
    d.line([(520, 565), (560, 565)], fill=(200, 200, 255, 200), width=4)
    d.polygon([(556, 546), (556, 584), (588, 565)], fill=(200, 200, 255, 220))
    tools = ["Cinematic Reel", "TikTok / Instagram Pack", "Hook Generator", "AI Brand Campaign"]
    pos = [(60, 870), (540, 870), (60, 970), (540, 970)]
    for (label, (px, py)) in zip(tools, pos):
        wc = d.textlength(label, font=K.F(K.FM, 25)) + 48
        K.pill(d, (px, py, px + wc, py + 68), 34, label, K.F(K.FM, 25))
    K.grad_rrect(img, (270, 1090, 810, 1192), 51)
    K.txt(d, (540, 1141), "Download Ad Creative", K.F(K.FB, 38), K.TXT, anchor="mm")
    K.rrect(d, (60, 1260, 1020, 1580), 28, fill=(16, 20, 44, 235), outline=K.BORDER, width=2)
    K.txt(d, (92, 1304), "CAMPAIGN BRIEF", K.F(K.FM, 24), K.TXT2)
    K.txt(d, (92, 1360), "Perfume launch — premium night campaign.", K.F(K.FM, 28), K.TXT)
    K.txt(d, (92, 1412), K.tstr("جمهور: السعودية • 9:16 • 15 ثانية"), K.F(K.FM, 26), K.TXT2, shaped=True)
    t1 = ["Cinematic Reel", "TikTok Product Ad", "Ramadan Kareem Poster"]
    x = 60
    for label in t1:
        wc = d.textlength(label, font=K.F(K.FM, 24)) + 44
        K.pill(d, (x, 1468, x + wc, 1530), 31, label, K.F(K.FM, 24))
        x += wc + 14
    K.txt(d, (540, 1660), "Generated with AI Ad Studio • 9:16 vertical", K.F(K.FM, 24), K.TXT2, anchor="mm")
    paste_thumb(img, "video/v3_perfume.png", (60, 1720, 510, 2080), 24, "Cinematic Reel")
    paste_thumb(img, "video/v3_supercar.png", (570, 1720, 1020, 2080), 24, "Neon City Cut")
    img.alpha_composite(nav_strip(), (0, NAV_Y))
    img.save(f"{UIQ}/uiq_ad_preview.png")


# ---------------- typing screen (parameterized) ----------------

PROMPT_RAW = "مدينة الرياض ليلية، برج الفيصلية، ألوان بنفسجية سينمائية، إضاءة درامية، جودة عالية"


def _wrap(d, s, font, maxw, right_x):
    words, lines, cur = s.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if not cur or d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def image_screen(prompt_chars=0, cursor_on=True, creating=False, progress=0.0):
    """image1 layout with a typed prompt; creating=True -> image2-style state."""
    img = bg340()
    d = ImageDraw.Draw(img)
    K.status_bar(d)
    K.app_bar(d, img)
    d.polygon([(64, 258), (88, 238), (88, 252), (116, 252), (116, 264), (88, 264), (88, 278)], fill=K.TXT2)
    K.txt(d, (140, 258), "AI Image", K.F(K.FB, 48), K.TXT, anchor="lm")
    K.pill(d, (760, 226, 1020, 290), 32, "GPT Image 2.5 • 1K", K.F(K.FM, 24))
    K.rrect(d, (60, 340, 1020, 1010), 28, fill=(16, 20, 44, 235), outline=K.BORDER, width=2)
    K.txt(d, (92, 380), "YOUR PROMPT", K.F(K.FM, 24), K.TXT2)
    f = K.F(K.FM, 36)
    if not creating:
        raw = PROMPT_RAW[:prompt_chars]
        shaped = K.shape(raw) if raw else ""
        ex, ey = 988, 450
        if shaped:
            for ln in _wrap(d, shaped, f, 896, 988):
                wln = d.textlength(ln, font=f)
                d.text((988 - wln, ey), ln, font=f, fill=K.TXT)
                ex = 988 - wln
                ey += 62
                if wln > 800:
                    ex = 988 - wln
        else:
            ex, ey = 988, 450
        if cursor_on and (not shaped or (len(shaped) and True)):
            d.rectangle([ex - 16, ey - 44, ex - 10, ey + 2], fill=(255, 255, 255, 235))
    chips = [("More Realistic", False), ("More Cinematic", True), ("More Luxury", False)]
    x = 60
    for label, act in chips:
        wc = d.textlength(label, font=K.F(K.FM, 26)) + 56
        K.pill(d, (x, 1082, x + wc, 1150), 34, label, K.F(K.FM, 26), active=act)
        x += wc + 16
    x = 60
    for i, r in enumerate(["9:16", "1:1", "16:9"]):
        wc = d.textlength(r, font=K.F(K.FM, 26)) + 48
        K.pill(d, (x, 1194, x + wc, x + wc * 0 + 1262), 34, r, K.F(K.FM, 26), active=(i == 0))
        x += wc + 16
    if creating:
        K.rrect(d, (60, 340, 1020, 1010), 28, fill=(16, 20, 44, 235), outline=(168, 132, 255, 220), width=3)
        K.txt(d, (540, 560), "Creating your image…", K.F(K.FB, 36), K.TXT, anchor="mm")
        d = ImageDraw.Draw(img)
        K.rrect(d, (150, 640, 930, 686), 23, fill=(28, 33, 70, 255))
        K.grad_rrect(img, (150, 640, int(150 + 780 * max(0.02, min(1.0, progress))), 686), 23)
        K.txt(d, (540, 760), "GPT Image 2.5 • 1K • 9:16", K.F(K.FM, 24), K.TXT2, anchor="mm")
        K.rrect(d, (270, 1400, 810, 1502), 51, fill=(24, 28, 60, 255), outline=K.BORDER, width=2)
        d = ImageDraw.Draw(img)
        K.txt(d, (540, 1451), "Creating…", K.F(K.FB, 38), K.TXT2, anchor="mm")
    else:
        d.ellipse([60, 1330, 96, 1366], fill=K.GOLD)
        K.txt(d, (112, 1348), "22 coins per image", K.F(K.FM, 26), K.TXT2, anchor="lm")
        K.grad_rrect(img, (270, 1420, 810, 1522), 51)
        d = ImageDraw.Draw(img)
        K.txt(d, (540, 1471), "Create", K.F(K.FB, 42), K.TXT, anchor="mm")
        K.txt(d, (540, 1580), "Charged only when generation starts", K.F(K.FM, 22),
              (110, 118, 155, 255), anchor="mm")
    _thumbs_row(img, d, 1680, THUMBS_A, "YOUR CREATIONS — SAVED IN MY PROJECTS")
    img.alpha_composite(nav_strip(), (0, NAV_Y))
    return img


# ---------------- tap / ripple / press sprites ----------------

def load_dot():
    dot = Image.open("build/dot.png").convert("RGBA")
    dot = dot.resize((140, 140), Image.LANCZOS)
    return dot


def load_ripple(i):
    r = Image.open(f"build/ripple/ripple_{i:02d}.png").convert("RGBA")
    r = r.resize((360, 360), Image.LANCZOS)
    return r


DOT = load_dot()
RIPPLES = [load_ripple(i) for i in range(18)]


def put_tap(img, cx, cy, f_local, tap_start, dot_dur=22, rip_start_off=10):
    """Dot drops for dot_dur frames starting tap_start; ripple from tap_start+rip_start_off."""
    if f_local >= tap_start:
        k = f_local - tap_start
        if k < dot_dur:
            p = k / dot_dur
            y = cy - 120 + 120 * min(1.0, p * 1.15)
            img.alpha_composite(DOT, (int(cx - 70), int(y - 70)))
        rf = f_local - (tap_start + rip_start_off)
        if 0 <= rf < 18:
            img.alpha_composite(RIPPLES[rf], (int(cx - 180), int(cy - 180)))


def press_pill(img, cx, cy, hw, hh, t):
    """Darken a pill (pressed look): t in 0..1"""
    if t <= 0:
        return
    ov = Image.new("RGBA", (hw * 2 + 40, hh * 2 + 40), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle([0, 0, hw * 2 + 39, hh * 2 + 39], radius=hh,
                                         fill=(10, 8, 30, int(90 * t)))
    img.alpha_composite(ov, (cx - hw - 20, cy - hh - 20))


def glow_pulse(img, cx, cy, r, phase, col=(139, 92, 246)):
    a = 26 + int(22 * (0.5 + 0.5 * math.sin(phase)))
    g = Image.new("RGBA", (r * 2, r * 2), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse([0, 0, r * 2 - 1, r * 2 - 1], fill=col + (a,))
    g = g.filter(ImageFilter.GaussianBlur(r / 3))
    img.alpha_composite(g, (cx - r, cy - r))


def ease_in_out(p):
    return p * p * (3 - 2 * p)


def blend(a, b, t):
    return Image.blend(a, b, min(1.0, max(0.0, t)))


# ---------------- beat sequences ----------------

def seq(name, frames):
    d = f"{SEQ}/{name}"
    os.makedirs(d, exist_ok=True)
    for i, fr in enumerate(frames):
        fr.convert("RGB").save(f"{d}/frame_{i:04d}.png")
    print(f"seq {name} {len(frames)}f ok")


def build_home_p(F=105):
    home = Image.open(f"{UIQ}/uiq_home.png").convert("RGBA")
    out = []
    for f in range(F):
        fr = home.copy()
        glow_pulse(fr, 540, 1400, 260, f / 30 * 2 * math.pi / 1.4)
        out.append(fr)
    seq("home_p", out)


def build_home_tap(F=150):
    home = Image.open(f"{UIQ}/uiq_home.png").convert("RGBA")
    tools = Image.open(f"{UIQ}/uiq_tools.png").convert("RGBA")
    out = []
    for f in range(F):
        fr = home.copy()
        if f < 112:
            put_tap(fr, 540, 1530, f, 90)
        else:
            fr = blend(home, tools, (f - 112) / 20)
        out.append(fr)
    seq("home_tap", out)


def build_tools_scroll(F=150):
    full = Image.open(f"{UIQ}/uiq_tools.png").convert("RGBA")
    header = full.crop((0, 0, 1080, 200))
    nav = full.crop((0, NAV_Y, 1080, H))
    content = full.crop((0, 200, 1080, NAV_Y))
    out = []
    for f in range(F):
        if f < 30:
            off = 0.0
        elif f < 105:
            off = 420 * ease_in_out((f - 30) / 75)
        else:
            off = 420.0
        fr = content.copy()
        fr = Image.new("RGBA", (W, H), (10, 13, 31, 255))
        fr.alpha_composite(full.crop((0, int(200 + off), 1080, int(200 + off + 2030))), (0, 200))
        fr.alpha_composite(header, (0, 0))
        fr.alpha_composite(nav, (0, NAV_Y))
        put_tap(fr, 540, 1801 - int(off), f, 118)
        out.append(fr)
    seq("tools_scroll", out)


def build_image_type(F=150):
    n = len(PROMPT_RAW)
    out = []
    for f in range(F):
        if f < 15:
            i = 0
        elif f < 135:
            i = int(n * (f - 15) / 120)
        else:
            i = n
        cursor_on = ((f // 8) % 2 == 0) or f >= 135
        out.append(image_screen(i, cursor_on))
    seq("image_type", out)


def build_image_create(F=150):
    result = Image.open(f"{UIQ}/uiq_img_result.png").convert("RGBA")
    out = []
    for f in range(F):
        if f < 55:
            fr = image_screen(len(PROMPT_RAW), cursor_on=((f // 8) % 2 == 0))
            put_tap(fr, 540, 1471, f, 30)
            if 40 <= f < 60:
                press_pill(fr, 540, 1471, 270, 51, min(1.0, (f - 40) / 6) * (1 if f < 55 else (60 - f) / 5))
            if f >= 50:
                creating = image_screen(0, False, creating=True, progress=(f - 50) / 60)
                fr = blend(fr, creating, (f - 50) / 8)
        elif f < 138:
            fr = image_screen(0, False, creating=True, progress=(f - 50) / 60)
            if f >= 130:
                fr = blend(fr, result, (f - 130) / 8)
        else:
            fr = result.copy()
            glow_pulse(fr, 540, 820, 500, f / 30 * 2 * math.pi / 1.1)
        out.append(fr)
    seq("image_create", out)


def build_img2vid(F=150):
    base = Image.open(f"{UIQ}/uiq_img2vid.png").convert("RGBA")
    out = []
    for f in range(F):
        if f < 80:
            fr = base.copy()
            put_tap(fr, 540, 770, f, 60)
            if 70 <= f < 84:
                press_pill(fr, 540, 855, 400, 61, min(1.0, (f - 70) / 6))
            if f >= 76:
                fr = blend(fr, vid_player(0.0), (f - 76) / 10)
        else:
            fr = vid_player(min(0.75, (f - 80) / 70))
        out.append(fr)
    seq("img2vid", out)


def build_storyfilm(F=165):
    base = Image.open(f"{UIQ}/uiq_storyfilm.png").convert("RGBA")
    out = []
    for f in range(F):
        fr = base.copy()
        glow_pulse(fr, 418, 1459, 250, f / 30 * 2 * math.pi / 1.6)
        out.append(fr)
    seq("storyfilm", out)


def build_ads(F=165):
    base = Image.open(f"{UIQ}/uiq_ads.png").convert("RGBA")
    prev = Image.open(f"{UIQ}/uiq_ad_preview.png").convert("RGBA")
    out = []
    for f in range(F):
        if f < 100:
            fr = base.copy()
            put_tap(fr, 540, 1471, f, 75)
            if 85 <= f < 105:
                press_pill(fr, 540, 1471, 270, 51, min(1.0, (f - 85) / 6))
            if f >= 96:
                fr = blend(fr, prev, (f - 96) / 14)
        else:
            fr = prev.copy()
            glow_pulse(fr, 795, 565, 300, f / 30 * 2 * math.pi / 1.3)
        out.append(fr)
    seq("ads", out)


def build_lang(F=135):
    base = Image.open(f"{UIQ}/uiq_lang.png").convert("RGBA")
    out = []
    for f in range(F):
        fr = base.copy()
        put_tap(fr, 540, 751, f, 60)
        d = ImageDraw.Draw(fr)
        k = f - 88
        if 0 <= k < 14:
            s = 1.35 - 0.35 * ease_in_out(k / 14)
            r = int(28 * s)
            d.ellipse([958 - r, 758 - r, 958 + r, 758 + r],
                      outline=(168, 132, 255, 255), width=6)
        out.append(fr)
    seq("lang", out)


def build_gaming(F=120):
    base = Image.open(f"{UIQ}/uiq_gaming.png").convert("RGBA")
    out = []
    for f in range(F):
        fr = base.copy()
        d = ImageDraw.Draw(fr)
        a = 120 + int(120 * (0.5 + 0.5 * math.sin(f / 30 * 2 * math.pi / 0.9)))
        d.ellipse([112, 438, 136, 462], fill=(255, 70, 70, a))
        for i in range(3):
            x = 60 + i * (292 + 22)
            aa = 120 + int(120 * (0.5 + 0.5 * math.sin(f / 30 * 2 * math.pi / 0.9 + i)))
            d.ellipse([x + 32, 1816, x + 48, 1832], fill=(255, 70, 70, aa))
        out.append(fr)
    seq("gaming", out)


def build_account(F=105):
    base = Image.open(f"{UIQ}/uiq_account.png").convert("RGBA")
    out = []
    for f in range(F):
        fr = base.copy()
        put_tap(fr, 540, 1081, f, 54)
        if 64 <= f < 80:
            press_pill(fr, 540, 1081, 270, 51, min(1.0, (f - 64) / 6))
        out.append(fr)
    seq("account", out)


def build_plans(F=120):
    base = Image.open(f"{UIQ}/uiq_plans.png").convert("RGBA")
    out = []
    for f in range(F):
        fr = base.copy()
        put_tap(fr, 540, 1651, f, 45)
        if 55 <= f < 71:
            press_pill(fr, 540, 1651, 270, 51, min(1.0, (f - 55) / 6))
        out.append(fr)
    seq("plans", out)


def main():
    render_statics()
    img_result()
    ad_preview()
    Image.open(f"{UIQ}/uiq_img_result.png").close()
    print("result views ok")
    build_home_p()
    build_home_tap()
    build_tools_scroll()
    build_image_type()
    build_image_create()
    build_img2vid()
    build_storyfilm()
    build_ads()
    build_lang()
    build_gaming()
    build_account()
    build_plans()
    print("ALL UI SEQUENCES DONE")


if __name__ == "__main__":
    main()
