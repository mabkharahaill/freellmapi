# 04 — Captions, cards and the graphic layer

Every caption is a separate text layer over the footage. Never generated inside a moving image, never burned in by a tool that does not shape Arabic. 27 graphic layers in the base cut; the timing of each is in `generated/caption-timing-25fps.csv` and `generated/caption-timing-30fps.csv`.

## 1. Direction and shaping

- **RTL enforced at the text-engine level.** After Effects with the Middle-Eastern text engine enabled, or Premiere with Arabic shaping, or a dedicated RTL compositor. Arabic typed into a non-shaping tool produces disconnected letterforms — this is not a stylistic choice, it is a broken file.
- **Isolate the Latin runs.** Any Latin string inside an Arabic layer (`mabkhrahaill.com`, `info@mabkhrahaill.com`, `@mabkharahaill`, `linktr.ee/mabkharahaill`) needs an explicit LTR isolate (RLM/LRM or the engine's direction override). Without it, the trailing `.com` and `@` migrate to the wrong end of the line in mixed-direction paragraphs.
- **No vertical bar as a separator.** The brief's lockup `مبخرة حائل | منذ 1998` uses `|`, which is direction-neutral and can flip the year to the Arabic side. Use `·` (as shipped) or a full RTL-safe layout with the year on its own line.
- **Numerals.** Arabic-Indic (٣٠٠, ١٨, ٢٩, ٤٢) inside Arabic sentences. Latin digits in URLs, emails and handles. Keep **1998** in Latin digits in the lockup, matching the logo's own Latin line.
- **No positive tracking.** Arabic letterforms join; positive tracking breaks the joins. Use 0 to −5.
- **Ellipsis.** Use the single-character `…`, never three full stops — the Arabic renderer will space the dots unevenly.

## 2. Type

| Role | Typeface | Size @1080×1920 |
|---|---|---|
| Primary (titles, product labels, branch cards) | 29LT Zarid Display or 29LT Bukra (licensed) · free fallback **Almarai ExtraBold** | 82–92 px |
| Subtitle / card body | Almarai Bold | 50–58 px |
| Caption / label | Almarai Regular | 44–48 px |
| Contact and social card lines | Almarai Regular | 42–46 px, line-height 1.6 |
| Latin (URL, email, handle) | the same family's Latin cut, or Inter / Proxima Nova — never a mismatched system default | same size as its Arabic line |
| Micro-label / badge | Almarai Bold | 34–38 px |

Weights: Arabic never below Regular; hairline Arabic disintegrates at phone scale. Never letterspace a Latin URL that sits inside an RTL paragraph — isolate it, then space only within the Latin run.

## 3. Colour and plates

| Element | Value |
|---|---|
| Cream text (on dark) | `#F2E7D5` |
| Espresso text (on light) | `#2B1A14` |
| Brass accent rule | `#B08A4A` |
| Deep ground | `#1C120E` |
| Athal brown | `#8A5A34` |
| Sand beige | `#E8DCC8` |

- On busy imagery the text sits on a **bottom-anchored scrim**: 28 px blur, 55–65 % opacity gradient, fading to nothing at the top edge. Never a hard-edged plate behind type.
- One accent only: an optional 2 px brass rule, 120–200 px wide, above a title. It never animates.
- Cards (K1–K3) may use a single soft radial darkening behind the text block at ≤45 % — the plate is not a box.

## 4. Placement and safe areas

- Title-safe: top 220 px, sides 90 px.
- **Bottom safe for all text: 480 px** (the brief's 420 px is kept for the scrim edge and non-text elements). TikTok and Snapchat UI can reach past 420 px.
- Lower thirds (captions and labels): baseline group centred horizontally, its lowest pixel at y = 1440 (i.e. 480 px above the bottom edge).
- Branch cards: centred block, optical centre slightly above true centre (y ≈ 880–960).
- Product labels: lower third, same baseline as captions.
- Badges: fixed corner, top-right (x = 990, y = 260), always the same corner for the whole film.
- Logo lockups: optically centred, 560–640 px wide, clear space on all sides equal to the Arabic wordmark height. Minimum on-screen width anywhere: 380 px.

## 5. Animation

- Opacity fade 8 frames in, 8 frames out, plus a 12 px vertical drift upward (or downward, once chosen, never both in one film).
- **Fades live inside the stated window.** A caption's `end` in the timing CSV is the last frame of its fade-out; a window that ends on a cut is fully faded by that cut. This is the ruling that resolves the brief's ambiguity (A7), and the builder enforces a minimum 0.25 s of full-opacity hold between the fades.
- No typewriter, no scale-bounce, no glow, no particles, no blur-in, no per-letter animation.
- Minimum dwell 2.0 s; **minimum 2.8 s for anything carrying a URL or handle.**

## 6. The three contact-card builds (S11, over the 35 %-brightness product plate)

**K1 · Card 1 · `00:02:03:00 → 00:02:07:18` (base cut, 30 fps)**
```
              مبخرة حائل · منذ 1998            ← 82 px, cream
        من حائل… نصنع الطيب ونهديه              ← 52 px, cream 80 %
                                            ──── brass rule 160 px
              mabkhrahaill.com                ← 46 px, isolated LTR
```
**K2 · Card 2 · `00:02:07:18 → 00:02:12:12`**
```
        للتواصل والطلبات الخاصة                  ← 52 px, cream
           البريد الإلكتروني                     ← 46 px, cream 80 %
      info@mabkhrahaill.com                   ← 46 px, isolated LTR
```
No WhatsApp line. The number is unconfirmed (Gate A) and the placeholder is never rendered.

**K3 · Card 3 · `00:02:12:12 → 00:02:18:00`**
```
   إنستغرام · سناب شات · تيك توك                 ← 46 px, cream
      فيسبوك · إكس · يوتيوب                       ← 46 px, cream
              @mabkharahaill                  ← 46 px, isolated LTR, centred once
        كل الروابط: linktr.ee/mabkharahaill    ← 38 px, cream 70 % — GATE I
```
The Linktree line renders **only** when the Linktree actually lists the site and all six platforms (A15). Until then, drop it: the handle alone is true, the claim would not be. Never put all the links on one frame; full URLs belong in the post text, not in the picture.

## 7. Wordmarks, badges and marks

- **LOGO-01 as supplied.** No redraw, no recolour, no outline, no gradient, no emblem animation, no separating the emblem from the wordmark. On dark backgrounds use the cream/white knockout version — **not** a filter-inverted brown version.
- Opening and closing lockups: 560–640 px wide, optically centred. Opening hold ≥2.5 s; closing hold 3.0 s with the last 0.6 s fading to warm black.
- **Gate H badge** «نموذج توضيحي للتخصيص» runs continuously for the whole personalisation block (68.0–80.5 s) if any of the three shots is a mock-up rather than a produced item. Top-right corner, 34 px, cream on a 45 % espresso pill, 70 % opacity. It is a badge, not a caption: it does not fade with the shots.
- **Micro-label** C12 «المحتويات حسب الباقة» at 38 px, same lower-third baseline, cream at 75 %. It is the one label allowed to sit under a caption.
- Platform names on Card 3 are set as **text**, not as platform logos. If logos are used later, use each platform's official unmodified asset, and keep the lockup to a single row per line — no tinting, no outlines, no rearranging.

## 8. Proofing before export

1. Render one still per graphic layer at 100 % zoom and read it aloud against the Arabic text.
2. Check every join: `مبخرة`, `الأثل`, `مسامير النحاس`, `دهن العود`, `منتزه الأدهم`, `السوق الشعبي`, `برزان`. Disconnected letters are the most common failure and are invisible at fit-to-window.
3. Check the Latin runs against the live URLs — `mabkhrahaill.com` (store, one **a** after "kh") versus `@mabkharahaill` (handles, two). Both are correct; a swapped letter sends traffic nowhere (A16).
4. Check the year: `1998` in the lockup, Latin digits, no Arabic-Indic substitution.
5. Check that no price, discount, offer badge, cart state or rating has leaked in from a screen capture (Gate K).
6. Check every caption's first and last frame against the timing CSV: first frame of the fade-in, last frame of the fade-out.
7. Watch the whole film once at 100 % size on a phone, in portrait, with the platform UI visible — that is the only check that catches safe-area mistakes.

## 9. Per-block caption order (base cut)

| Block | Layers | Notes |
|---|---|---|
| S1 | C1 lockup | in `00:00:08:27` (30 fps), out on the cut |
| S2 | C2 | over 2A/2B |
| S3 | C3, C4, C5 | one at a time; C5 clears before the S4 cut |
| S4 | C6, C7, C9, C10 | 4C carries no label |
| S5 | C11 + C12 micro | C12 is the contents disclaimer |
| S6 | C13, C14 + C13b badge | badge spans the block |
| S7 | C15, C16 | over the packing shots |
| S8 | C17, C18, C19 | branch cards, centred |
| S9 | C21 url-card, C22 | C21 is the only card with a Latin line in this block |
| S10 | C23, C24 (or C24b) | shipping line, mutually exclusive pair |
| S11 | K1, K2, K3 | never two cards on screen at once |
| S12 | C25 lockup | fades with the closing logo |

Exact frames, durations and the URL-dwell check for every one of these are in `generated/caption-timing-*.csv`; the QA gate re-verifies them on every build.
