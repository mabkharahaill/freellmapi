# 03 — Voiceover session sheet

Record-ready. Print this, mark it up, hand it to the engineer.

## Session

| Item | Spec |
|---|---|
| Talent | Adult male, warm Saudi accent (Najdi / Hail-neutral), 30–50. Confident, welcoming, unhurried. **No announcer energy, no shouting, no upward sell-inflection.** |
| Pace | ~3 words/second. Nothing in this film should sound read. |
| Takes | **24 lines** — 18 that go in the cut, 6 recorded and held (3 are the brief's original unsplit lines, 3 are gated alternates). |
| Mic | Large-diaphragm cardioid, 15–20 cm, pop filter, treated room. |
| Room tone | 10 seconds, silent, same mic position. Needed under every edit point. |
| Format | 48 kHz / 24-bit WAV, one file per line, named `VO_<ID>_<take>.wav` (e.g. `VO_V3a_tk2.wav`). No processing in the booth; deliver flat. |
| Pauses | 0.5–0.8 s between lines. Inside a line, follow the sync marks below exactly. |
| Slate | Say the line ID before each take, then pause 2 s. The editor will strip slates. |
| Do not read | Any URL, any handle, any English word, any bracketed direction, the word "سلة" as an English word (it is *Salla*, the platform, and it stays inside the Arabic sentence). |

**The VO governs the cut — so the enumeration lines are recorded to the picture, not read blind.** Lines 4, 8 and 12c carry sync marks: the frame the named thing must start on. Ask the engineer to run the picture (or a click track derived from it) at 30 fps while these three lines are performed. Tolerance ±0.3 s. Everything else can be read freely.

## Budget

`generated/vo-budget.csv` holds every line: in-point, word count, budget, window, slack. Summary: **≈60.3 s of speech across a 142.0 s film (42 %)**. The tightest window in the cut is V10b (0.50 s of slack across three words) and the longest line is V8 (15 words). Nothing is over-budget, and the film keeps 58 % of its running time for music, ambience and silence — which is the "unhurried" the brief asks for.

Read the budget as a ceiling, not a target: **where a line comes in under budget, leave the extra time as silence at the end of the line**, never as a slower read.

---

## The script

Legend: **⏸** = pause 0.5–0.8 s · **→** = sync mark (the named thing must start on this timecode in the master) · ⚠ = do not place until the gate clears.

### S1 · حائل والهوية — line 1

**V1 · in `00:00:01:00` (30 fps)**

> من حائل، تبدأ حكايتنا… حكاية حرفة وتراث وضيافة، منذ عام ألف وتسعمئة وثمانية وتسعين. ⏸

14 words · budget 4.67 s · window 11.1 s. Read the year slowly and completely — «ألف وتسعمئة وثمانية وتسعين» is the heritage line, give it weight. No sync dependency: shots 1A/1B/1C are already moving.

### S2 · خشب الأثل — line 2 (split)

**V2 · in `00:00:13:00`**

> في مبخرة حائل، نختار خشب الأثل الناشف بعناية، ونهتم بكل تفصيلة. ⏸

11 words · 3.67 s · window 13.1 s. Say **الأثل** with a clean voiceless *th* (as in *think*) — not *s*, not *t*. This is the one word in the film that will be quoted back.

**V2-orig · ⚠ hold** — the brief's original line 2, including «…من تجهيز الخشب وتشكيله، إلى تجميع القطع وتشطيبها». Record it in the same tone. It only gets used if the editor abandons the sync-corrected cut.

### S3 · الصناعة — line 3 (split)

**V3a · in `00:00:27:06`** (30 fps)

> من تجهيز الخشب وتشكيله، إلى تجميع القطع وتشطيبها بأيدي حرفيينا. ⏸

10 words · 3.33 s.

| → | target | over shot |
|---|---|---|
| وتشكيله | `00:00:28:12` | 3A cutting |
| تجميع | `00:00:29:03` | 3B assembly |
| وتشطيبها | `00:00:30:03` | 3C smoothing |
| بأيدي حرفيينا | `00:00:30:18` | 3C |

**V3b · in `00:00:34:06`**

> وتكتمل بتفاصيل النقش، والتلبيس المعدني، ومسامير النحاس، بحسب تصميم كل قطعة. ⏸

11 words · 3.67 s.

| → | target | over shot |
|---|---|---|
| النقش | `00:00:35:09` | 3D carving |
| والتلبيس المعدني | `00:00:36:15` | 3E lining |
| ومسامير النحاس | `00:00:37:18` | 3F studs |
| بحسب تصميم كل قطعة | `00:00:38:21` | 3F studs |

**V3-orig · ⚠ hold** — the brief's original unsplit line 3.

### S4 · المجموعة — line 4

**V4 · in `00:00:41:12`**

> من المباخر الحائلية… إلى النجدية الملكية… تصاميم ومقاسات تناسب استخدامكم، ومجالسكم، وضيافتكم، ومناسباتكم. ⏸

13 words · 4.33 s · window 12.7 s. **Two internal beats** replace the single ellipses: the pauses are what make the product names land.

| → | target | over shot |
|---|---|---|
| الحائلية | `00:00:41:12` | 4A حايلي in |
| النجدية الملكية | `00:00:43:27` | 4B نجدي ملكي in |
| تصاميم ومقاسات | `00:00:46:27` | 4C/4D |
| ومجالسكم | `00:00:48:09` | 4D |
| ومناسباتكم | `00:00:49:03` | 4D/4E |

### S5 · الهدايا والبوكسات — line 5 (split)

**V5a · in `00:00:55:06`**

> ولأن لكل هدية معنى، نجهّز لكم خيارات مميزة من بوكسات المباخر. ⏸

11 words · 3.67 s.

**V5b · in `00:01:04:00`**

> مع العود والبخور ودهن العود، بحسب الباقة المختارة. ⏸

8 words · 2.67 s · window 3.6 s — the tightest line in this block. Slight speed is better than a clipped consonant; do a second take at a marginally quicker pace.

| → | target | over shot |
|---|---|---|
| العود | `00:01:04:00` | 6D oud chips |
| والبخور | `00:01:04:18` | 6D bukhoor |
| ودهن العود | `00:01:05:06` | 6D oud oil |

**V5-orig · ⚠ hold** — the brief's original unsplit line 5.

### S6 · التخصيص — line 6

**V6 · in `00:01:08:15`**

> وتقدرون تضيفون لمستكم الخاصة، بكتابة الاسم أو الشعار… واختيار التصميم واللون والمقاس حسب الطلب. ⏸

14 words · 4.67 s. One beat after «الشعار» sends the options clause onto 5C.

| → | target | over shot |
|---|---|---|
| بكتابة الاسم | `00:01:10:00` | 5A engraved name |
| أو الشعار | `00:01:11:06` | 5B company logo |
| واختيار التصميم واللون والمقاس | `00:01:15:18` | 5C options |

Note the colloquial register: «تقدرون تضيفون» is deliberate. Do not upgrade it to فصحى.

### S7 · الطلبات والتجهيز — line 7

**V7 · in `00:01:21:00`**

> نستقبل طلبات الأفراد والكميات وهدايا الشركات، ونهتم بالتجهيز والتغليف قبل الشحن. ⏸

11 words · 3.67 s. Light beat after «الشركات،» so the packing clause lands on the stacked boxes.

| → | target | over shot |
|---|---|---|
| طلبات الأفراد والكميات | `00:01:21:06` | 8A-1 wrapping |
| وهدايا الشركات | `00:01:22:24` | 8A-2 sealing |
| وبالتجهيز والتغليف | `00:01:26:18` | 8A-3 stacked boxes |

### S8 · المعرض والفروع — line 8 · **record to picture**

**V8 · in `00:01:31:00`**

> حيّاكم في فروعنا الثلاثة بحائل: برزان خلف بنك الراجحي… والسوق الشعبي… وعقدة في منتزه الأدهم. ⏸

15 words · 5.00 s · window 11.1 s. The three branch names are the sync-marked part; the pauses between them are **performance pauses, 0.6–0.8 s**, not edits. «حيّاكم» gets a genuine hospitality tone — a slight smile in the voice.

| → | target | over card |
|---|---|---|
| برزان خلف بنك الراجحي | `00:01:33:18` | C17 |
| والسوق الشعبي | `00:01:36:18` | C18 |
| وعقدة في منتزه الأدهم | `00:01:39:18` | C19 |

### S9 · قنوات الشراء — line 9

**V9 · in `00:01:43:00`**

> وتقدرون تتسوّقون من موقعنا الإلكتروني على سلة، وتطّلعون على منتجاتنا في ترينديول. ⏸

12 words · 4.00 s.

| → | target | over shot |
|---|---|---|
| على سلة | `00:01:45:12` | 9A the store recording |
| في ترينديول | `00:01:46:24` | 9A tail / 9B in |

**V9b · ⚠ Gate C — record and hold**
> وكذلك عبر أمازون السعودية ونون، حسب المنتجات المتاحة.

8 words · 2.67 s. Do not place until the owner confirms live listings — and note that placing it costs 4.4 s of runtime, which currently breaks the 2:22 ±3 s target (Gate L).

### S10 · التوصيل والشحن — lines 10–11

**V10a · in `00:01:52:00`**
> نوصل لجميع مناطق المملكة. ⏸
4 words · 1.33 s · over 8B-1 sealed boxes.

**V10b · in `00:01:57:03`**
> ونشحن لدول الخليج. ⏸
3 words · 1.00 s. **0.50 s of slack — the tightest line in the film.** Over the 8B-2 product still.

**V11 · in `00:01:59:00`** (default)
> وتلقون خيارات الشحن والعروض الحالية في موقعنا. ⏸
7 words · 2.33 s. This is the line that ships unless Gate B is cleared the day of publication.

**V11b · ⚠ Gate B — record and hold**
> والشحن مجاني داخل السعودية للطلبات بقيمة ثلاثمئة ريال فأكثر، حسب شروط المتجر.
12 words · 4.00 s needed in a 4.3 s window — **0.3 s of slack, the second-tightest line in the film.** Record it at a slightly quicker pace or it runs past the 123.0 s cut. Its in-point is set at 118.3 s, immediately after V10b ends at 118.1 s. Say «ثلاثمئة» as a word, not as digits. If the offer is not live on the day of publication, this take stays on the drive.

### S11 · التواصل — line 12 (split into three cards)

**V12a · in `00:02:03:12`** — over Card 1 (brand + domain)
> تابعونا على حساباتنا، واطّلعوا على كل جديد في موقعنا الإلكتروني. ⏸
10 words · 3.33 s.

**V12b · in `00:02:08:00`** — over Card 2 (email)
> وللطلبات الخاصة، تواصلوا معنا عبر البريد الإلكتروني الموضح على الشاشة. ⏸
10 words · 3.33 s. Note: no WhatsApp line. The number is unconfirmed (Gate A) and is never spoken or shown.

**V12c · in `00:02:12:24`** — over Card 3 (socials) · **record to picture**
> وتابعونا على إنستغرام، وسناب شات، وتيك توك، وفيسبوك، وإكس، ويوتيوب.

10 words · 3.33 s. Spread the six names evenly; do not rush the last two into one breath.

| → | target |
|---|---|
| إنستغرام | `00:02:13:12` |
| وسناب شات | `00:02:14:06` |
| وتيك توك | `00:02:14:27` |
| وفيسبوك | `00:02:15:18` |
| وإكس | `00:02:16:06` |
| ويوتيوب | `00:02:16:24` |

**V12d · ⚠ Gate I — record and hold**
> وكل الروابط في مكان واحد.
5 words · 1.67 s. Usable only when the Linktree actually lists everything (see A15).

### S12 · الختام — line 13

**V13 · in `00:02:18:15`**

> مبخرة حائل… من حائل، نصنع الطيب ونهديه.

9 words · 3.00 s. The brand name is spoken warm and slightly slower on every occurrence — this is the last thing in the film.

---

## Pronunciation targets

| Word | Target |
|---|---|
| حائل | *Ḥā-ʾil* — clear hamza, two syllables. **Not** "Hayel", not "Haaeel". |
| الأثل | *al-ʾathl* — voiceless *th* (as in *think*), not *s*, not *t*. |
| حايلي | *ḥā-yi-lī* — with the *y*, distinct from حائل. |
| نجدي | *naj-dī*. |
| رشم | *rashm* — the store's own word for the carved motif; crisp, not *rasm*. |
| برزان | *bar-zān*. |
| عقدة | *ʿugdah* — the Hail district, not *ʿaqdah*. |
| دهن العود | *dihn al-ʿūd*. |
| ألف وتسعمئة وثمانية وتسعين | Fully spoken, unhurried. |
| ثلاثمئة (V11b only) | *thalāth-miʾah* — one word, not three digits. |
| مبخرة حائل | *mab-kha-rat Ḥāʾil* — warm, slightly slower every time. |
| حيّاكم | Genuine hospitality, slight smile in the voice. |

## Before the booth closes

- One full pass of all 18 placed lines, start to finish, no stops — the safety net if a pick-up is ever needed after the talent has flown home.
- Two takes of every sync-marked line (V4, V8, V12c) at the marked pace.
- The three unsplit alternates (V2-orig, V3-orig, V5-orig) in the same tone and pace as their split counterparts.
- The two gated alternates (V9b, V11b).
- 10 s of room tone.
- No processing, no de-essing, no limiting in the booth — the mix stage does that (spec in `05-mix-grade-delivery.md`).
