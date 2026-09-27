# 02 — The edit decision list

Generated, not typed. The numbers live in `tools/film-data.mjs` and are re-emitted by `node tools/build-files.mjs`, so the EDL, the caption sheet and the QA report can never disagree with each other.

## Files

| File | Use |
|---|---|
| `generated/edl-30fps.csv` | **Recommended master.** Zero frame-grid drift. |
| `generated/edl-25fps.csv` | The brief's headline rate, quantised to whole frames. |
| `generated/timeline-{fps}.md` | Human-readable: shots, captions and VO per block, with sync marks. |
| `generated/caption-timing-{fps}.csv` | Every graphic layer, frame-exact, with its Arabic and English text. |
| `generated/vo-budget.csv` | Every VO line: in-point, word count, budget at 3 w/s, window, slack, status. |
| `generated/qa-report.md` | The pass/fail record and the runtime arithmetic by option set. |
| `generated/captions-ar.srt`, `generated/captions-en.srt` | Verbatim VO subtitles — for the **clean master** (A23). |

## Columns

`edl-*.csv`: `scene, brief_scene, shot, asset, nominal_start_s, nominal_end_s, start_tc, end_tc, start_frame, end_frame, duration_s, duration_f, direction`

- `scene` is execution order (S1–S12); `brief_scene` is the brief's own name for the block.
- `nominal_*_s` is the client's grid in seconds — what the brief asked for. `*_tc/frame` is what the edit actually does after rounding to whole frames. Keeping both means a half-second intention is never lost.
- `asset` gives asset IDs. `A|B` means "either, depending on what was shot". `A+B` means "both in one composed frame". The manifest in `generated/asset-manifest.csv` carries the status of every id.

## Block map — execution order versus the brief

| Timeline block | Brief name | Label | Timecode (base cut, 30 fps) |
|---|---|---|---|
| S1 | Scene 1 | حائل والهوية | `00:00:00:00 → 00:00:12:15` |
| S2 | Scene 2 | خشب الأثل | `00:00:12:15 → 00:00:26:15` |
| S3 | Scene 3 | الصناعة | `00:00:26:15 → 00:00:41:00` |
| S4 | Scene 4 | المجموعة | `00:00:41:00 → 00:00:54:15` |
| S5 | **Scene 6** | الهدايا والبوكسات | `00:00:54:15 → 00:01:08:00` |
| S6 | **Scene 5** | التخصيص | `00:01:08:00 → 00:01:20:15` |
| S7 | Scene 8A | الطلبات والتجهيز | `00:01:20:15 → 00:01:30:15` |
| S8 | Scene 7 | المعرض والفروع | `00:01:30:15 → 00:01:42:15` |
| *(8E)* | — | ورشتنا — optional, +2.5 s | `00:01:42:15 → 00:01:45:00` |
| S9 | Scene 9 | قنوات الشراء | `00:01:42:15 → 00:01:51:15` |
| S10 | Scene 8B | التوصيل والشحن | `00:01:51:15 → 00:02:03:00` |
| S11 | Scene 10A | التواصل | `00:02:03:00 → 00:02:18:00` |
| S12 | Scene 10B | الختام | `00:02:18:00 → 00:02:22:00` |

The brief's Scene 5 and Scene 6 are swapped in execution order, because the voiceover speaks gifts first and the brief states the VO governs the cut. Scene 8A/8B are split around Scene 7/9 in both systems — same layout, two numberings. Carry both; never say "Scene 6" without saying which numbering.

The timecodes above are the **base cut** (no optional elements enabled). With the workshop beat enabled, everything from S9 onward shifts +2.5 s (S9 starts `00:01:45:00`); with Gate C enabled, everything from S10 onward shifts a further +4.4 s. Never hand-edit these — regenerate with the flag and the shift is applied everywhere at once.

## Runtime budget (Gate L)

Target 2:22 ±3 s → **145.0 s ceiling**.

| Option set | Runtime | Inside |
|---|---|---|
| Base master | 142.0 s (2:22.0) | yes |
| + workshop beat 2.5 s | 144.5 s (2:24.5) | yes |
| + Gate B free-shipping line 1.8 s | 143.8 s (2:23.8) | yes |
| + Gate C Amazon/Noon 4.4 s | 146.4 s (2:26.4) | **no** |
| + workshop + Gate B | 146.3 s (2:26.3) | **no** |
| + everything optional | 150.7 s (2:30.7) | **no** |

**Rule: the sum of enabled optional elements must stay ≤ 3.0 s.** One addition, never two. If two are commercially unavoidable, the runtime target has to be renegotiated in writing before the cut is locked — do not quietly run 2:30 and discover it at delivery.

## Frame rate

At 25 fps the brief's half-second grid is not frame-legal: 48 cut times fall between frames, worst error 0.02 s. At 30 fps the same grid is exact.

**Recommendation: 30 fps master.** Phone-shot footage, 60 fps screen captures for Scene 9, and Instagram/TikTok delivery all sit naturally at 30. If 25 is chosen for other reasons, the quantised 25 fps EDL shipped here is already legal — shoot 25, cut 25, and shoot the screen captures at 25 too so Scene 9 does not need conversion.

## Aspect, safe areas and text

- Master 1080×1920, title-safe top 220 px, sides 90 px.
- **Bottom safe: 480 px for all burned text** (the brief's 420 px is used for the plate and for non-text elements). TikTok and Snapchat UI can reach past 420 px; text that survives is worth more than text that is 60 px lower.
- Every Arabic caption is a separate text layer over the footage. Never baked into a moving image, never generated inside one.

## Transitions

- Straight cuts throughout.
- 8–12 frame dissolves between stills in **S4, S5 and S6** only (the brief's rule, restated by execution order — see A10).
- One 16-frame dip-to-warm-black into the closing logo at `00:02:18:00`.
- No speed ramps, no whip transitions, no flashes, no whip-pans.

## Conform procedure, after the VO is recorded

1. **Place the 18 primary takes** on their sheet in-points (`generated/vo-budget.csv`), unlocked, unmuted, on the master timeline.
2. **Check the sync-mark lines against the picture** (V4, V8, V12c). If a name lands more than ±0.3 s from its mark, either nudge the shot or re-cut the alternate take — the tolerance exists so this is a 5-minute job, not a re-record.
3. **Where the VO and the cut disagree on a named item, move the cut** — not the sound. The audio leads; that is the brief's own rule and it is the right one for a film whose subject is a product line.
4. **Cap the movement at ±20 frames (0.67 s at 30 fps) per cut**, and never move a block boundary: S4→S5 at 54.5 s, S5→S6 at 68.0 s, and so on stay welded. Slides inside a block are free; the block grid is what keeps the runtime.
5. **Re-run the QA gate** after any timing edit — `node brand-film/tools/build-files.mjs` must pass before the cut goes to grade.
6. **Lock and export a reference frame at each block boundary** for the sound designer and the grader: `00:00:12:15, 00:00:26:15, 00:00:41:00, 00:00:54:15, 00:01:08:00, 00:01:20:15, 00:01:30:15, 00:01:42:15, 00:01:51:15, 00:02:03:00, 00:02:18:00` (30 fps).

## What still blocks the cut

Forty of the forty-one film-bearing asset ids are missing — see `generated/asset-manifest.csv`. Scene 9 in particular cannot be cut without the two screen recordings (Gate G), and Scene 1 cannot open on a location that is not Hail (the fallback is to open on the storefront alone, then go straight to the logo lockup).
