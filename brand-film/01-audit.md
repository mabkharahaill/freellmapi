# Audit — BRAND FILM MASTER PACKAGE, as supplied 2026-09-27

## Verdict

The drafting is strong where it matters most: it refuses to invent assets, it separates what is confirmed from what is claimed, and its compliance gates are the right shape. Nothing in it would have produced a false claim on screen.

What it does not survive is contact with a timeline or with the live storefront.

- **Timing.** The brief's own rules are broken in three places (A1, A2, A4), and the half-second cut grid is not frame-legal at its own headline frame rate (A6).
- **Sync.** The voiceover names things the picture has not shown yet in eleven measurable places — the products, the oud, the branches and the platforms all arrive seconds after they are spoken. The brief says "VO order governs the cut", but the VO and the shots were written independently (A3, A5).
- **Verification.** The package assumes facts about the brand's own web presence that are partly wrong today: the Linktree does not list what the caption says it lists (A15), the Trendyol link passes through a country gate (A14), and a screen recording of the store will capture national-day prices and offer banners that expire within days (A13).

Severity key: **BLOCKER** = do not shoot or cut until resolved · **FIX** = corrected in this package, needs sign-off · **VERIFY** = needs a human check · **NOTE** = judgement call or polish.

---

## A. Timing and sync

### A1 · BLOCKER · Scene 4's third product slot was 2.0 s, under the brief's own 2.2 s minimum
`4C 47.0–49.0`. Every other product slot in the scene is 2.7–3.0 s, and the brief states "each product gets ≥2.2 s so it is genuinely recognised". The 2.0 s slot is also the conditional one (جميلي / سليماني), i.e. the one an editor is most likely to leave in and least likely to notice.
**Fixed:** 4A and 4B tighten to 2.9 s, 4C takes 2.2 s, section still ends at 54.5 s. No downstream change.

### A2 · BLOCKER · The optional workshop beat could not carry its own caption
The brief inserts WKS-01 at 1.5 s with the caption «ورشتنا». The caption spec requires a 2.0 s minimum dwell, and a 1.5 s shot cannot host it without the text straddling the cut.
**Fixed:** the beat runs **2.5 s** (shot 8E, 102.5–105.0, caption 102.8–104.9) and adds **+2.5 s**, not +1.5 s. The brief noticed the runtime extension but not that every later in-point shifts — the builder applies that shift to shots, captions and VO automatically.

### A3 · BLOCKER · Eleven places where the voiceover is ahead of the picture
Measured against the brief's own timings, at the brief's own pace of ~3 words/second:

| Brief line | Words land | Picture shows it at | Gap |
|---|---|---|---|
| 2 — «من تجهيز الخشب وتشكيله، إلى تجميع القطع وتشطيبها» | 17.0–19.7 s | 3A/3B/3C cutting, assembly, sanding at 26.5–34.0 s | **7–14 s early** |
| 3 — «التلبيس المعدني ومسامير النحاس» | ~31.6–33.2 s | 3E/3F lining and studs at 36.5–41.0 s | **3–8 s early** |
| 4 — «النجدية الملكية» | ~42.9 s | 4B نجدي ملكي cuts at 43.9 s | 1.0 s early |
| 5 — «مع العود والبخور ودهن العود» | ~57.5 s | 6D oud shots at 63.5 s | **6 s early** |
| 6 — «واختيار التصميم واللون والمقاس» | ~72.0 s | 5C colour/options at 76.0 s | **4 s early** |
| 7 — «وبالتجهيز والتغليف» | ~83.8 s | 8A-3 stacked boxes at 87.5 s | 3.7 s early |
| 8 — branch names | evenly spread from 91.0 s | cards cut at 93.5 / 96.5 / 99.5 s | no anchor — luck |
| 9 — «في ترينديول» | ~106.6 s | 9B Trendyol at 107.5 s | fine |
| 10 — «ونشحن لدول الخليج» | ~113.3 s | 8B-2 at 117.0 s | 3.7 s early |
| 12 — platform names | ~125–130 s | social card at 132.0 s | **up to 6.5 s early** |

This is not a nuance. The film's whole credibility rests on the VO and the picture describing the same thing at the same moment; a viewer hears "brass studs" while watching a saw.
**Fixed:** the narrative lines are split and re-pointed (2, 3, 5, 6, 10, 12); the enumeration lines get **sync marks** — the frame each name must start on, tolerance ±0.3 s, recorded to a guide track (4, 8, 12c). Full detail in `03-vo-session-sheet.md`; every sync mark is in `generated/vo-budget.csv` and the timeline tables. The original unsplit lines 2, 3 and 5 are recorded as alternates so this decision stays reversible.

### A4 · BLOCKER · The optional content cannot all fit, and the brief never adds it up
Target: 2:22 ±3 s = **145.0 s maximum**.

| Addition | Cost | Runtime | Inside? |
|---|---|---|---|
| Workshop beat (A2) | +2.5 s | 2:24.5 | yes |
| Gate B free-shipping VO line | +1.8 s | 2:23.8 | yes |
| Gate C Amazon/Noon card + VO | +4.4 s | 2:26.4 | **no** |
| Workshop + Gate B | +4.3 s | 2:26.3 | **no** |
| Gate B + Gate C | +6.2 s | 2:28.2 | **no** |
| everything optional | +8.7 s | 2:30.7 | **no** |

The brief lists a "+4s runtime" cost for the Amazon line, calls the free-shipping swap a straight replacement, and notes the workshop adds 1.5 s — but never checks the sum against its own ±3 s target.
**Fixed:** new **Gate L** states the rule plainly — *the sum of enabled optional elements must stay ≤ 3.0 s*. One addition, never two. `tools/build-files.mjs --gate-c` fails the build on purpose to keep this visible.

### A5 · BLOCKER · Scene 10A named the platforms six seconds before the platform card existed
The brief's VO line 12 opens «تابعونا على إنستغرام، وسناب شات، وتيك توك…» at 123.5 s. That moment is Card 1 — brand lockup and domain. The social card does not appear until 132.0 s, and by then the platforms have already been listed.
**Fixed:** line 12 becomes three takes keyed to the three cards — 12a (site) @123.4, 12b (email and special orders) @128.0, 12c (platforms, verbatim) @132.8. The words "تابعونا على إنستغرام…" now occur while the social card is up.

### A6 · FIX · The half-second cut grid is not frame-legal at 25 fps
0.5 s = 12.5 frames at 25 fps. Forty-eight of the brief's cut times fall between frames; the worst rounding error is 0.02 s (0.5 frame). At 30 fps the same grid is exact — zero drift.

**Recommendation: cut 30 fps.** This is a phone-shot, social-first film: 30 matches typical handset footage, Instagram/TikTok delivery, and 60 fps screen captures for Scene 9. Both EDLs are generated, so the decision is a flag, not a rebuild (`generated/edl-25fps.csv`, `generated/edl-30fps.csv`). If the owner insists on 25 for broadcast-adjacent reasons, the shipped 25 fps EDL is already quantised and legal — the nominal grid is preserved in the `nominal_*_s` columns so nothing is lost.

---

## B. Spec contradictions

### A7 · FIX · The caption fade rule never says whether the fades sit inside or outside the stated window
"Opacity fade 8 frames in / 8 out" plus windows given to the second. If the fades sit outside, every caption that ends on a cut — «مسامير نحاس» out at 41.0, «للهدايا والمناسبات» out at 54.5, the branch cards, the contact cards — bleeds into the next shot.
**Ruling:** fades live **inside** `[start, end)`, end-exclusive. A caption that ends at 41.0 has completed its fade-out on the last frame before the cut. Enforced by the builder: every caption must retain ≥0.25 s of full-opacity hold after both 8-frame fades.

### A8 · FIX · Two different music levels, an inaudible ambience bus, and an undefined side of the duck
Scene 1 says music enters "at −26 LUFS"; the mix table says −24 LUFS. Ambience is set at −32 LUFS, which sits 8 LU under the music bed and will be inaudible. The duck is "−7 dB" with no statement of whether the published bus levels are pre- or post-duck.
**Fixed in `05-mix-grade-delivery.md`:** music −24 LUFS **pre-duck**, sidechain duck −7 dB on top with a 250 ms release; ambience rides −30 to −26 LUFS where music plays and −32 where it does not; all quoted bus levels are pre-duck by definition.

### A9 · FIX · Scene 4's captions had text but no timings
Scenes 1, 2, 3, 5, 6, 7, 8A, 9, 10A and 10B all received in/out times; Scene 4's four product labels were given as text only.
**Fixed:** C6 41.4–43.7, C7 44.3–46.6, C9 49.3–51.5, C10 52.1–54.34. 4C deliberately carries no label (conditional, and 2.2 s cannot hold a 2.0 s dwell comfortably).

### A10 · NOTE · "Dissolves between product stills in Scene 4 and 6" points at the wrong blocks
In execution order the product blocks are S4 (collection) and S5 (gifts); the brief's "Scene 6" is the gifts block, so the instruction is right by accident and wrong to read. The personalisation block (S6) is also stills-heavy and would have been left on hard cuts.
**Fixed:** the rule is restated by timeline block — dissolves 8–12 frames between stills in **S4, S5 and S6**; straight cuts everywhere else.

### A11 · FIX · Two scene-numbering systems in one document
The brief states that the VO governs the cut, then runs gifts (its Scene 6) before personalisation (its Scene 5), which drags every later number out of execution order.
**Fixed:** the EDL carries both columns — `scene` (S1–S12, execution order) and `brief_scene` (the brief's names). The mapping is in `02-edl-master.md`.

---

## C. Verified against the live brand presence (2026-09-27)

Method: direct fetch of the public URLs. Results are recorded in `06-gates-and-verification.md`; `tools/probe-links.mjs` re-runs the whole directory on demand.

### A12 · NOTE · The store claim holds
`mabkhrahaill.com` is live on Salla, serves `/ar`, and the page title carries "من خشب الأثل". The descriptor «متجرنا الرسمي عبر منصة سلة» is accurate, and "one store, not two" is correct — the storefront is the destination, not a second brand site.

### A13 · BLOCKER · A screen recording of the store today will capture prices and offer banners that expire within days
The live catalogue currently shows «عروض خاصة بمناسبة اليوم الوطني السعودي الـ96» with strikethrough prices (e.g. 720 against 900). The film's own rule is that no price or discount is ever stated; and those offers will be gone within days, dating the film on sight.
**Fixed:** new **Gate K** — no price, discount, offer badge or countdown in any frame. Record the screen capture on a page without offers, or mask the elements and re-check the recording frame by frame before it goes into Scene 9.

### A14 · FIX · The Trendyol deep link passes through a country-selection interstitial
`https://www.trendyol.com/en/sr?mid=1159743` redirects to `/en/select-country` when requested without a country cookie. A screen recording made carelessly would open on a country picker — which looks like a dead end in a brand film.
**Fixed:** Gate I requires recording from a Saudi-geo browser **after** the country gate has been passed; prefer a product deep link (`…-p-<id>?merchantId=…`) over a seller listing, and confirm the first frame of the capture shows product, not a gate.

### A15 · BLOCKER · The Linktree does not contain what the film says it contains
`linktr.ee/mabkharahaill` is live but lists **only TikTok and Snapchat**. Card 3 burns «كل الروابط: linktr.ee/mabkharahaill» and names six platforms.
**Fixed:** new **Gate I**. Either complete the Linktree (site + six platforms), or drop the «كل الروابط» line and keep the handle `@mabkharahaill` alone, which is true today. The alternate VO take V12d («وكل الروابط في مكان واحد») is held until this clears.

### A16 · BLOCKER · The domain and the handle differ by one letter, and both are burned into the film
`mabkhrahaill.com` (domain) versus `@mabkharahaill` (handle, Linktree, Instagram, TikTok, Snapchat, X, YouTube). Both are correct; a viewer will not track the difference.

This is the most expensive error available in this film: it either sends traffic to a dead address or makes the brand look careless at the exact moment it asks for an order.

**Action, in order:**
1. Register the obvious mirrors — `mabkharahaill.com`, `mabkhrahaill.…` variants, `mabkhrahail.com` — and 301 them to the Salla store.
2. On screen, treat the two strings differently: the domain always with a label («الموقع» / «متجرنا»), the handle always with `@` and never as a bare word.
3. Proofread both at 100 % zoom against the live URLs, twice, at export.
4. Put the clickable links in the post text — never ask a viewer to type either string.

### A17 · VERIFY · «سليماني» was not visible in the catalogue pages sampled
The live المباخر category shows نجدي, نجدي ملكي, نجدي رشم and حايلي families. «سليماني» did not appear. If no such product exists, 4C has no subject and must fall back to the جميلي slot or be dropped (the timeline already handles a dropped 4C).

### A18 · VERIFY · No 8–15 cm product was visible either
Sampled sizes: **18 / 20 / 29 / 42 سم**. The brief's 4E shot — "small and medium together in one composed frame" — assumes a small band that may not exist.
**Action:** confirm the smallest actual product. If the smallest is 18 cm, recompose 4E as 18 + 29 cm, and keep Gate D's default (sizes omitted on screen) untouched.

### A19 · NOTE · Three things the store sells are missing from the film's asset manifest
The catalogue also carries **زعفران** (its own category), **علبة بخور** (incense boxes) and **طقم / sets** of two and three. The manifest has no saffron asset at all, and bukhoor appears only as OUD-02.
**Action:** decide in or out. If out, that is a defensible scope choice — but make it deliberately, because the 60 s social cut is a better home for a saffron beat than the master.

### A20 · VERIFY · The basis of "منذ 1998"
1998 CE ≈ 1418–1419 H. If the founding year is recorded in Hijri, the Latin "1998" is the conversion and needs one check against the logo lockup and any commercial-registration document. The Linktree account dates from April 2023 — no conflict with a 1998 founding, but it does mean the film must not imply a long history of *online* selling.

### A21 · VERIFY · Social handles could not all be probed
Instagram returns 403 to automated requests; the remaining platforms were not probed in this session. Run `node tools/probe-links.mjs` and clear every 404, redirect and dead numeric Facebook page id before the link directory is published.

### A22 · FIX · No 16:9 deliverable, although the master is designated for website and YouTube
A 9:16 master cannot serve a website embed or non-Shorts YouTube as written. Section 10 lists eight deliverables, all vertical.
**Fixed:** a 16:9 reframe row is added in `05-mix-grade-delivery.md`, with the reframe rule (reposition, do not letterbox the whole film; the graphic layer is layered separately so it re-flows).

### A23 · FIX · A verbatim AR subtitle under burned Arabic captions is double text
The burned captions are excerpts of the VO; the AR `.srt` is the VO verbatim. Shipping both on the same cut shows two different Arabic texts at once.
**Fixed:** the AR `.srt` ships with the **clean master** (and the EN `.srt` optionally with either). The burned master needs no AR sidecar.

### A24 · NOTE · Five additions to the blacklist
The brief's blacklist covers generated material and wrong cities. Add: **prices, discount banners and offer badges** (A13); **the Trendyol country-gate interstitial** (A14); **any store UI captured in a stale state** (empty cart, error toast, half-loaded images); **imported, non-workshop-made items under craft captions** — the catalogue sells «علبة بخور… صناعة يدوية باكستان» and طلح-wood items, which must never sit under «صناعة يدوية» or «بأيدي حرفيينا»; and **retimed or upscaled hand motion**, since optical-flow retiming can invent hand artefacts that read as synthetic even when the source is real.

### A25 · NOTE · Align the on-screen vocabulary with the store's own words
The catalogue says «مباخر حايلي شكلٍ جميلي تراثي», «رشم» for the carved motif, «ملبس ألمنيوم ومسامير نحاس» for the fittings, «بوكس باب حائل» and «طقم ٣ حبه». Where the film's captions differ, viewers cannot find the product they just saw.
Two concrete alignments: the conditional 4C label should read **«حايلي — شكل جميلي»** (جميلي is a حايلي shape variant in the catalogue, not a separate family), and «تفاصيل تراثية» (C4) could optionally become **«نقش رشم»** — the store's own term for the carving shown in 3D.

---

## D. What already holds, and should not be touched

- **The refusal to invent.** The manifest, the blacklist and the "never stated anywhere" list are the strongest part of the document. They survive this audit intact, and the provenance gate (A24) exists only because the live catalogue made one new case reachable — not because the principle was wrong.
- **The gift-box caution.** The live catalogue confirms it: some gift boxes include «أوقية عود ودهن عود كمبودي ربع تولة», others are a mubkhara and a box only. The wording «بحسب الباقة المختارة» and the badge «المحتويات حسب الباقة» are exactly right, and now provably so.
- **The branch discipline.** Three branches, a workshop that is never counted as a fourth, exteriors only when their own photograph exists, no maps or pins. Consistent, and it survives every check.
- **The gate defaults.** Email-only contact, the "see current shipping options" line instead of a free-shipping claim, Amazon/Noon omitted, sizes omitted. Each one is the conservative choice and each one is correct today.
- **The logo rules and the grade palette.** Nothing in them invites a redraw or a colour push. The only addition here is a bidi-safety change to the lockup separator (dot instead of bar) and the recommendation not to grade a social film at gamma 2.4 without a 2.2 check on a handset.
- **The casting note.** "Adult male, warm Saudi accent (Najdi/Hail-neutral), 30–50, unhurried, no announcer energy" is a real casting brief, not a placeholder. It is carried forward verbatim, with a target-word table added for the enumeration lines.

## E. Measured facts this package now asserts

| Fact | Value | Source |
|---|---|---|
| Master runtime, base cut | 142.0 s (2:22.0) | `generated/qa-report.md` |
| Runtime ceiling | 145.0 s (2:22 +3 s) | brief |
| Optional content available | 8.7 s (workshop 2.5 · Gate B 1.8 · Gate C 4.4) | A4 |
| Cuts falling between frames at 25 fps | 48 (worst 0.02 s) | `generated/qa-report.md` |
| Cuts falling between frames at 30 fps | 0 | `generated/qa-report.md` |
| Narration, primary lines only | ≈60.3 s of speech = 42 % of 142.0 s | `generated/vo-budget.csv` |
| Longest VO line | V8, 15 words, 5.00 s budget, 11.1 s window | `generated/vo-budget.csv` |
| Tightest VO window | V10b, 0.50 s of slack | `generated/vo-budget.csv` |
| Required assets still missing | 40 of 41 film-bearing ids | `generated/asset-manifest.csv` |
| Graphic layers in the base cut | 27 = 23 captions/labels + 1 Gate H badge + 3 contact cards | `generated/caption-timing-25fps.csv` |
| VO takes to record | 24 = 18 placed + 6 held alternates | `generated/vo-budget.csv` |
