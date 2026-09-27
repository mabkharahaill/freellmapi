# Mabkhra Haill — brand film master package (corrected + machine-generated)

**Status: not shootable yet — 40 of 41 required assets are still missing.** Everything in this folder is built so that the moment the footage and photos arrive, the edit is mechanical: the EDL is frame-exact, every caption has an in/out timecode, and every voiceover line has a measured budget and sync marks.

This folder is a corrected, machine-checked version of the *BRAND FILM MASTER PACKAGE* supplied on 2026-09-27. The original drafting is sound — the compliance discipline in particular is strong. What it was missing was arithmetic that survives an actual timeline, sync between the voiceover and the picture, and verification against the live store. Those are the three things fixed here.

## Start here

| File | What it is |
|---|---|
| `01-audit.md` | The review. 25 findings (A1–A25), each with severity, evidence and the fix, plus a short list of what already holds. **Read this first.** |
| `00-source-and-deltas.md` | Every place this package deviates from the supplied brief, side by side, so a change can be accepted or rejected line by line. |
| `02-edl-master.md` | How to read the EDL, the frame-rate ruling, the run-runtime budget, and the conform procedure for after the VO is recorded. |
| `03-vo-session-sheet.md` | Record-ready voiceover sheet: takes, measured budgets, sync marks, alternates, pronunciation, engineering. |
| `04-caption-and-graphics-spec.md` | RTL typography, exact pixel layout, the three contact-card builds, logo rules, bidi traps, proofing procedure. |
| `05-mix-grade-delivery.md` | Sound mix spec with the level contradictions resolved, grade spec, export specs, file naming, deliverables. |
| `06-gates-and-verification.md` | Gates A–L with the live-verification results of 2026-09-27 and the exact owner actions to clear each one. |
| `07-social-cuts.md` | 60 s / 30 s / 15 s cut maps, summed frame-exact against the master. |
| `tools/` | `film-data.mjs` is the single source of truth; `build-files.mjs` generates; `probe-links.mjs` checks the link directory. |
| `generated/` | EDL (25 + 30 fps), timeline, caption timing, VO budget, AR/EN SRT, asset manifest, QA report. |

## Regenerate everything

```bash
node brand-film/tools/build-files.mjs                       # base master, 2:22.0  → PASS
node brand-film/tools/build-files.mjs --workshop             # + workshop beat, 2:24.5 → PASS
node brand-film/tools/build-files.mjs --gate-b=cleared       # + free-shipping line, 2:23.8 → PASS
node brand-film/tools/build-files.mjs --gate-c               # + Amazon/Noon, 2:26.4 → FAILS the ±3 s target on purpose
node brand-film/tools/build-files.mjs --fps=30               # 30 fps leg only (zero rounding drift)
```

The builder refuses to pass a build that breaks any rule the brief sets — shot minimums, the 2.0 s caption dwell, the 2.8 s URL dwell, the fade-and-hold rule, scene tiling, or the 2:22 ±3 s runtime — and prints the reason. `generated/qa-report.md` holds the full pass.

## The five things to decide before the record session

1. **Runtime budget (Gate L).** The optional additions total 8.7 s. The target allows 3.0 s. Workshop alone (2.5 s) is affordable; Gate B alone (1.8 s) is affordable; Gate C (4.4 s) is not, and any two together break the target. Pick one.
2. **Frame rate (A6).** The brief's half-second grid is not frame-legal at 25 fps — 48 cut times land between frames. At 30 fps they are exact. For a phone-shot, social-first film, cut 30.
3. **Scene order.** The timeline follows the voiceover (gifts before personalisation), as the brief's own order note allows. Swapping to the brief's order costs no runtime but re-keys both blocks and every caption in them.
4. **The gates that need the owner**, not the editor: WhatsApp number (A), free shipping (B), Amazon/Noon (C), per-product sizes (D), Linktree completion (I).
5. **Domain vs handle (A16).** `mabkhrahaill.com` and `@mabkharahaill` differ by one letter and are both burned into the film. Register the mirror domains and treat the two strings differently on screen.

## What this package will not do

It will not generate a craftsman, a hand, an interior, a product, a price, a claim, a branch or a website interface. The blacklist in the brief is kept and extended (A24) — including one addition it could not have foreseen: the live store is currently showing national-day offer banners and strikethrough prices, which a screen recording would capture and which expire within days.
