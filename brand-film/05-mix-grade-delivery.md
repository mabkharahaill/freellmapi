# 05 — Sound, colour and delivery

## 1. Sound

### Buses

| Bus | Treatment | Level | Notes |
|---|---|---|---|
| VO | HPF 80 Hz · de-esser · compressor 3:1 with 3–4 dB gain reduction · light 3 kHz presence | −16 to −14 LUFS short-term, peaks −6 dBFS | Centre-weighted. Dialogue is the loudest thing in the film by design. |
| Music | Sparse oud, light qanun/nay. No percussion hits, no build-drops. Enters `00:00:02`. | **−24 LUFS pre-duck** | Sidechain duck −7 dB under VO, 250 ms release, 40 ms attack. |
| Ambience | Shop room tone (S1, S8, S11) · workshop room tone (S2, S3) | **−30 to −26 LUFS** where music plays, −32 LUFS where it does not | Recording the ambience at −32 under a −24 bed makes it inaudible — 8 LU is a waste of a bus. Ride it. |
| SFX | **Only where the action is on screen.** One event per shot, maximum. | −28 to −24 LUFS | Saw stroke, sanding, one wood-on-bench contact at `00:00:21`, a single stud tap, tissue/card/tape in packing, one tape sound at `00:01:56:15`. Nothing else. |
| Master | −14 LUFS integrated, true peak −1.5 dBTP | | Social standard, applied per deliverable, not once for all of them. |

**All quoted bus levels are pre-duck.** The duck is applied on top. This is stated because the brief quoted "−26 LUFS" at entry and "−24 LUFS" in the table without saying which side of the duck either number sat on (A8).

### Prohibited

No risers, no cinematic booms, no reverse-cymbal swells, no whooshes on transitions, no riser-into-logo, no crowd, no fire crackle that is not in the footage, no musical sting on the product reveals. Silence between blocks is permitted and desirable — the film already gives the mix 58 % of its length as non-speech time; use it rather than filling it.

### Deliverable mixes

| Deliverable | Mix |
|---|---|
| Master (2:22) | Full mix as specified. |
| Clean master | Identical mix, no burned captions. |
| Social 60 / 30 / 15 | Re-bounced from the master stems, **re-normalised to −14 LUFS / −1.5 dBTP independently**. Bolting a loud master onto a short cut and trusting the platform's limiter is how social cuts end up 3 dB down. |
| VO stem | 18 placed takes, top-and-tailed, slates removed, 48 kHz / 24-bit WAV, plus the 6 held alternates in the same folder under `/alternates`. |

## 2. Colour

- **Palette:** athal brown `#8A5A34` · sand beige `#E8DCC8` · brass `#B08A4A` · deep ground `#1C120E` · cream text `#F2E7D5`.
- Warm but restrained. Do not push orange. Wood must read as wood and brass as brass — not gold-plated, not teal-shadowed.
- Soft highlight roll-off; protect the brass speculars from clipping. The stud macro (3F) is the shot that will clip first — expose it for the stud, let the surround sit low.
- Light film grain 1–2 % for photographic texture. No vignette beyond 8 %.
- **Still animation:** maximum 4 % scale move over 3 s, plus subtle parallax only where a clean cut-out exists. No 3D flythrough, no fake depth on flat product shots.
- **Prohibited:** CGI sheen, sparkle/glitter, light leaks, magical assembly, invented smoke, lens flares, invented crowds, speed ramps, whip transitions.

### Gamma, and the one thing the spec could not cover

The brief specifies Rec.709 with gamma 2.4. That is the right working space for the grade bay and the right master. It is not what a phone does with a social file: handsets display SDR closer to 2.2 and the platforms strip or re-tag metadata unpredictably.

**Do both:**
1. Grade and monitor at gamma 2.4, Rec.709, for the master and the archive.
2. Export an additional **social variant tagged 2.2** and judge it on a phone at ~50 % brightness, in daylight, before publishing. If the two disagree, trust the phone for the social cut and keep 2.4 for the master library.

## 3. Export matrix

| Deliverable | Container | Codec | Resolution | FPS | Bitrate | Text |
|---|---|---|---|---|---|---|
| Master | MOV | ProRes 422 HQ | 2160×3840 if sources allow, else 1080×1920 | 30 (or 25) | — | burned captions |
| Clean master | MOV | ProRes 422 HQ | same as master | same | — | none |
| Social 60 | MP4 | H.264 High | 1080×1920 | 30 | 30 Mbps | burned |
| Social 30 | MP4 | H.264 High | 1080×1920 | 30 | 30 Mbps | burned |
| Teaser 15 | MP4 | H.264 High | 1080×1920 | 30 | 30 Mbps | burned |
| Website / YouTube | MP4 | H.264 High | 1920×1080 | 30 | 20 Mbps | burned, re-laid out |
| Stills | PNG | — | 1080×1920 ×3 | — | — | as composed |

- Audio 48 kHz / 24-bit stereo in every deliverable; AAC 320 kbps in the MP4s.
- Colour tag every H.264 export `bt709` with the chosen transfer; do not let the encoder write `unspecified`.
- Burn no caption closer than 480 px to the bottom edge and none under 2.0 s on screen (2.8 s with a URL) — the capture list is in `04-caption-and-graphics-spec.md`.

## 4. The 16:9 reframe (added — the original package had none)

A 9:16 master cannot serve the website or a non-Shorts YouTube upload as written (A22). The reframe is a **reposition, not a letterbox**:

1. Re-grade is not needed; reuse the 2160-wide master and crop to 1920×1080 with a per-shot pan that follows the subject.
2. Every product still and branch card is re-laid out for the wider frame — the graphic layer is regenerated from the same text layers, never scaled from the vertical burn.
3. The lower-third captions move up to a 60 %-height baseline; the 480 px bottom-safe rule does not apply in 16:9.
4. Branch cards and contact cards are centred as blocks, unchanged in wording.
5. The 2:22 runtime is identical by construction: same EDL, same frames, different crop map. Note the crop map per shot in the export sheet.

## 5. File naming

```
MabkhraHaill_BrandFilm_MASTER_2160x3840_30p_ProRes422HQ.mov
MabkhraHaill_BrandFilm_CLEAN_2160x3840_30p_ProRes422HQ.mov
MabkhraHaill_BrandFilm_MASTER_1080x1920_30p_H264_30Mbps.mp4
MabkhraHaill_BrandFilm_SOCIAL60_1080x1920_30p_H264_30Mbps.mp4
MabkhraHaill_BrandFilm_SOCIAL30_1080x1920_30p_H264_30Mbps.mp4
MabkhraHaill_BrandFilm_TEASER15_1080x1920_30p_H264_30Mbps.mp4
MabkhraHaill_BrandFilm_16x9_1920x1080_30p_H264_20Mbps.mp4
MabkhraHaill_BrandFilm_VO_AR_48k24b.wav
MabkhraHaill_BrandFilm_SUBS_AR.srt          ← clean master only
MabkhraHaill_BrandFilm_SUBS_EN.srt
MabkhraHaill_BrandFilm_STILL_endframe.png
MabkhraHaill_BrandFilm_STILL_logo.png
MabkhraHaill_BrandFilm_STILL_hero.png
```

Versioning: `_v01`, `_v02` before the extension; never `final`, `final2`, `final-v3-REAL`. Every export carries the same 2:22 (or the option-set runtime) — if a runtime drifts, the file name must say so.

## 6. Deliverables table (supersedes the brief's Section 10)

| Cut | Runtime | Scope | Use |
|---|---|---|---|
| Master | 2:22 | Full film, burned captions, 9:16 | Website, Linktree |
| Clean master | 2:22 | No burned captions | Re-versioning, other languages |
| **16:9 reframe** | 2:22 | Repositioned crop, captions re-laid out | Website embed, YouTube (non-Shorts), presentations |
| Social 60 | 0:60 | S1 → S3 → S4 → S5 → S8 → S9/S10 (map in `07-social-cuts.md`) | Reels, TikTok, Snapchat |
| Social 30 | 0:30 | Craft + collection + branches + website | Paid / retargeting |
| Teaser 15 | 0:15 | Brass stud macro → hero product → logo + domain | Hooks, Stories |
| VO stem | — | 18 placed takes + 6 alternates, 48/24 WAV | Archive |
| Subtitles | — | AR verbatim (clean master) + EN (either) | Accessibility, Gulf expat reach |
| Stills | 3 | 1080×1920: end frame, logo lockup, hero product | Thumbnails / covers |

## 7. Before delivery

- [ ] `node brand-film/tools/build-files.mjs` passes for the option set actually used.
- [ ] Runtime matches the file name and the option-set table in `generated/qa-report.md`.
- [ ] Every deliverable independently normalised to −14 LUFS / −1.5 dBTP.
- [ ] Spot-check three frames per deliverable against the timing CSV (first frame of fade-in, midpoint, last frame of fade-out).
- [ ] No price, discount, offer badge, dead UI state or country-gate interstitial anywhere in the picture (Gates K, I).
- [ ] Both Latin strings proofed at 100 %: `mabkhrahaill.com` and `@mabkharahaill`.
- [ ] The AR SRT went out with the clean master, not under the burned captions.
