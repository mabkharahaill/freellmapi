# Source and deltas

The full original brief is not duplicated here — keep your own copy alongside this folder if you want the repo to hold the pristine text. What follows is **every place this package says something different from the supplied brief**, so each change can be accepted or rejected on its own merits. Anything not listed is unchanged.

Reference: supplied *BRAND FILM MASTER PACKAGE*, 2026-09-27, target runtime 2:22 ±3 s, vertical 9:16, Arabic VO.

---

## 1. Timeline changes

| Where | Brief says | This package says | Why |
|---|---|---|---|
| Scene 4, shots 4A/4B/4C/4D/4E | 3.0 / 3.0 / **2.0** / 2.7 / 2.8 s | **2.9 / 2.9 / 2.2** / 2.7 / 2.8 s | 4C was 2.0 s, below the brief's own "each product gets ≥2.2 s" rule. Section still ends at 54.5 s. (A1) |
| Optional workshop beat | "WKS-01, 1.5 s, may be inserted at 01:42.5" | **2.5 s**, inserted as shot 8E at 102.5–105.0 s | 1.5 s cannot carry a caption that must stay on screen 2.0 s. Adds +2.5 s, not +1.5 s. (A2) |
| Every scene after the workshop beat | not stated | **+2.5 s shift** applied automatically (runtime 2:24.5) | The brief noted the insert extends runtime but not that every downstream in-point moves. The builder applies the shift to shots, captions and VO alike. |
| Scene 9, shot 9B | 107.5–111.5 s | unchanged in the base cut; **extends to 8.4 s (+4.4 s)** if Gate C clears | The Amazon/Noon card needs somewhere to live. Cost: runtime becomes 2:26.4, outside tolerance. (A4) |
| Frame grid | half-second boundaries (`x.5 s`) | same nominal grid, **quantised to whole frames**; both 25 and 30 fps EDLs shipped | 0.5 s = 12.5 frames at 25 fps. 48 cut times in the brief fall between frames; the worst is 0.02 s. At 30 fps there is no drift at all. (A6) |
| Scene numbering | Scene 5 = personalisation, Scene 6 = gifts, but the cut runs gifts first | both numbers carried: the EDL has `scene` (execution order, S1–S12) **and** `brief_scene` | Prevents the classic "which Scene 6?" edit-bay error. (A11) |

## 2. Voiceover changes

Everything else in the script is untouched — same words, same register, same Najdi-neutral casting note.

| Brief line | Change | Why |
|---|---|---|
| 2 | Split. The clause *«من تجهيز الخشب وتشكيله، إلى تجميع القطع وتشطيبها»* moves to the head of line 3. Line 2 becomes *«في مبخرة حائل، نختار خشب الأثل الناشف بعناية، ونهتم بكل تفصيلة.»* | Line 2 describes cutting, assembly and finishing, but those shots run at 26.5–34.0 s — the words arrived 7–14 s before the picture. (A3) |
| 3 | Split into 3a (process: shaping → assembly → finishing) and 3b (carving → metal lining → brass studs). | So each craft action is named as it happens rather than three shots early. (A3) |
| 4 | Two short beats added (after «الحائلية» and after «الملكية») and the line re-pointed. | Product names must land on their own shots: «النجدية الملكية» now starts on the 4B cut at 43.9 s. (A3) |
| 5 | Split into 5a (box options, over the box shots) and 5b (oud/bukhoor/oil, over the oud shots at 64.0 s). | In the original the word «العود» was spoken ~9 s before the oud appeared. (A3) |
| 6 | One beat added after «أو الشعار». | So the colour/size clause lands on the options shot (5C). (A3) |
| 10 | Split into 10a («نوصل لجميع مناطق المملكة.») and 10b («ونشحن لدول الخليج.»), at 112.0 s and 117.1 s. | The brief's own caption plan already split these two ideas across the two shots; the VO now matches it. (A3) |
| 11 | Default line kept verbatim; the free-shipping alternate is placed at 118.6 s, not 117.5 s. | 10b now occupies 117.1–118.5 s. The alternate's window is 4.4 s — record it at a slightly quicker pace. (A3, A4) |
| 12 | Split into three takes mapped to the three contact cards: 12a @123.4 (site), 12b @128.0 (email/special orders), 12c @132.8 (the six platforms, verbatim). | The original named the platforms at ~125 s while Card 1 (brand + domain) was on screen; the social card did not appear until 132.0 s. (A5) |
| 12d | New alternate *«وكل الروابط في مكان واحد.»* at 137.0 s. | Only usable if the Linktree actually lists everything (Gate I). (A15) |
| Sync marks | not in the brief | Added to lines 4, 8 and 12c: the frame each name must start on, ±0.3 s. | Enumerations (branch names, platform names, product names) must be recorded to picture, not read blind. (A3) |
| Alternates | brief had 9b and 11b | The original unsplit lines 2, 3 and 5 are also recorded as alternates (V2-orig, V3-orig, V5-orig) | Costs nothing in the session and protects the brief-led edit as a fallback. |

## 3. Caption changes

| Where | Brief says | This package says | Why |
|---|---|---|---|
| Scene 1, 10A Card 1, final lockup | `مبخرة حائل \| منذ 1998` (vertical bar) | `مبخرة حائل · منذ 1998` (middle dot) | A bare `\|` in an RTL run is a bidi hazard: it can reorder the Latin year to the wrong side of the Arabic. The dot is unambiguous. (A7 note in `04`) |
| Scene 2 | in 13.5, out 18.0 | in 13.4, out 18.2 | Matches the spoken words inside V2 after the line was trimmed. |
| Scene 3 «مسامير نحاس» | 38.8 – 41.0 | 38.7 – **41.0 exclusive** | 41.0 is a hard cut. With fades defined inside the window, the caption is fully gone by the cut. (A7) |
| Scene 4 | caption text given, no timings | timings set for C6, C7, C9, C10; **4C carries no label** | 4C's 2.2 s slot cannot hold a 2.0 s label comfortably and it is conditional anyway. |
| Scene 5 (gifts) | «المحتويات حسب الباقة» recommended on 6A/6B | placed 58.0–61.5 as `micro-label` | One clear position instead of two candidates. |
| Scene 6 (personalisation) | badge if any visual is a mock-up | badge C13b spans the whole block 68.0–80.5 when Gate H is open | A badge that appears and disappears invites doubt about which shot it covered. |
| Scene 10A | three cards, timings given | K1 123.0–127.6 · K2 127.6–132.4 · K3 132.4–138.0, each with its own VO take | Cards and voice now move together. |
| Scene 8B shipping line | default + conditional caption | both built as C24 / C24b, mutually exclusive, same window 117.4–122.7 | Guarantees the caption and the VO take swap as a pair. |
| Latin lines | not specified | `mabkhrahaill.com`, `info@mabkhrahaill.com`, `@mabkharahaill`, `linktr.ee/mabkharahaill` set as isolated LTR runs inside the RTL layer | Without isolation, the trailing `.com` elements drift to the wrong end of the line in Arabic text engines. |

## 4. Spec, mix and delivery changes

| Item | Brief says | This package says | Why |
|---|---|---|---|
| Music level | "−26 LUFS" at entry, "−24 LUFS" in the mix table | **−24 LUFS pre-duck**, one number, duck −7 dB on top, 250 ms release | Two different numbers for the same bus. (A8) |
| Ambience | −32 LUFS | **−30 to −26 LUFS**, riding with the music; −32 only where music is absent | At −32 under a −24 bed the ambience is 8 LU down — inaudible, i.e. wasted. (A8) |
| Duck point | "sidechain duck −7 dB" | Levels are stated as **pre-duck**; the duck is applied on top | The brief never said which side of the duck the published number sits on. (A8) |
| Frame rate | "25 fps (or 30 — match dominant source)" | **Recommendation: 30 fps**, both EDLs shipped | 30 removes the frame-grid problem (A6) and matches phone footage, TikTok/Reels delivery and 60 fps screen recordings. |
| Colour | Rec.709, gamma 2.4 | Grade and monitor at 2.4; **also deliver a 2.2-tagged social export** and judge it on a phone | 2.4 read on a handset looks darker than the grade bay. Platform re-encodes ignore metadata, so the eye is the authority. |
| Bottom safe zone | 420 px | **420 px for the master grid, 480 px for the burned-text layer** | TikTok/Snapchat captions and UI can reach past 420 px. Text still clears; the plate can go lower. (A24 note in `04`) |
| Dissolve rule | "between product stills in Scene 4 and 6" | restated by timeline block: **S4 and S5**, and extended to the personalisation block S6 | The brief's "Scene 6" is the gifts block in execution order. Two blocks, one number, again. (A10) |
| Deliverables | 8 cuts, 9:16 master for "Website, YouTube" | + **16:9 reframe** row, and the AR `.srt` moved to the clean master only | A 9:16 master cannot serve a website embed or non-Shorts YouTube as written; and a verbatim AR SRT under burned captions is double text. (A22, A23) |
| Subtitles | "AR .srt (verbatim VO)" | AR verbatim SRT ships with the **clean master**; the burned master ships without an AR sidecar (EN optional) | Same reason. (A23) |
| Blacklist | building, generated craftsmen/hands/interiors/UI, wrong cities, unmatched products | + **prices, discount banners and offer badges; the Trendyol country-gate interstitial; any store UI in a stale state; imported non-workshop items under craft claims; retimed/upscaled hand motion** | All six are reachable in this film's actual source material. (A13, A14, A24) |
| Gates | A–H | + **I link integrity, J making provenance, K transient commerce content, L runtime budget** | Each one blocks something the original gates would have let through. |

## 5. What was not changed

- Every caption and VO line that did not need a timing or sync fix: same words, same register.
- The voiceover order (gifts before personalisation).
- The compliance defaults: no WhatsApp number, no free-shipping claim, no Amazon/Noon, no on-screen sizes, no invented branch exteriors, no simulated website.
- The casting, pace and pronunciation brief — `03-vo-session-sheet.md` carries it forward verbatim, with a target-word table added.
- The logo rules: as supplied, no redraw, no recolour, no emblem animation, clear space = wordmark height, minimum 380 px wide, 560–640 px in the opening and closing lockups.
- The grade palette and the prohibitions list (no CGI sheen, sparkle, light leaks, magical assembly, speed ramps, whip transitions).
