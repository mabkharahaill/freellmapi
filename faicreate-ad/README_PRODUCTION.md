# FAI CREATE — 120s Cinematic Commercial (v3)

Final deliverable: `FAI_CREATE_CINEMATIC_AD_120S_1080x1920.mp4` (120.00 s, 1080×1920,
H.264 + AAC, ~77 MB). Public copy on Google Drive (see session delivery message).
The build intermediates (`build/`, `build3/`) are git-ignored and are regenerated
by the pipeline below.

## Timeline (fixed by the narration)

| Scene | Time  | VO line (Saudi Arabic) |
|-------|-------|------------------------|
| S1 | 00:00–00:12 | تخيّل أن أفكارك تتحول إلى واقع! … مرحباً بك في FAI CREATE! |
| S2 | 00:12–00:27 | مع FAI CREATE، أدوات الإبداع أصبحت في مكان واحد. … |
| S3 | 00:27–00:43 | اكتب فكرتك وحوّلها إلى صورة مميزة. … |
| S4 | 00:43–01:00 | خلّ أفكارك تتحرك! … |
| S5 | 01:00–01:16 | استكشف استوديو القصص والأفلام … |
| S6 | 01:16–01:33 | عندك متجر أو مشروع؟ … |
| S7 | 01:33–01:46 | الإبداع ما له حدود! … |
| S8 | 01:46–01:54 | سجّل حسابك الآن … |
| S9 | 01:54–02:00 | FAI CREATE — خيالك يصنع المستقبل! ابدأ الآن عبر faicreate.co. |

VO start times: 0 / 12 / 27 / 43 / 60 / 76 / 93 / 106 / 113.6 (s, vo9 ×1.03 atempo).
Subtitles: `build/substrack/` (3600 RGBA frames, 1080×1920, 30 fps) — built once by
`sub_render.py` / `sub_track.py` and reused verbatim by v3 (timings match the VO).

## v3 pipeline (reproducible stages)

1. **`ui_phone3.py`** — renders the FAI CREATE phone-UI system at true 9:19.5
   (1080×2340): 13 static screens in `build/uiq/` and 12 animated sequences in
   `build/uiseq3/` (typing with RTL Arabic shaping via `ui_kit.shape`, scrolling,
   tap dot + ripple, page blends, image-creation progress, video player).
2. **`photo_composite3.py`** — detects the phone screen quadrilateral in the two
   hand-holding photos (bright-blob density peak + flood fill + rotated-rect fit;
   TR = max(x−y), BL = min(x−y) for clockwise tilt), then perspective-warps every
   UI frame onto the glass (PIL PERSPECTIVE, 8-coeff solve), with dark screen-off
   rim, screen grade, screen-aligned glare, inner shadow, and finger
   occlusion re-pasted on top. Output: `build/comp3/{beat}/frame_%04d.png`
   (1080×1920, 30 fps).
3. **`sfx_gen3.py`** — synthesizes `build/sfx3.wav`: tap clicks at
   15.0 / 20.4 / 32.5 / 45.0 / 78.5 / 95.0 / 107.8 / 110.5 s, scene whooshes at the
   8 blend centers, reveal whooshes+hits (36.0/47.5/81.0), typing ticks 27.4–30.4,
   logo riser 114.0.
4. **`build_ad3.py`** — assembles the film:
   - `beats`: 24 beats. `cine` = AI plate + zoompan motion (push / push_fast /
     drift / drift2 / slow_push / reveal-from-black) + FAI watermark on plates;
     `phone` = composite sequence + gentle handheld zoompan (taps are already
     animated inside the composites).
   - `clips`: scene = beats joined with 0.5 s xfade (scene lengths
     12.0/15.5/16.5/17.5/16.5/17.5/13.5/8.5/6.5).
   - `joins`: **replay-free scene joins** — `seg_k` = scene k minus its
     head/tail 0.5 s, `blend_k` = xfade(last 0.5 s of scene k, first 0.5 s of
     scene k+1) with varied transitions. Final = seg01+bl01+…+seg09 = exactly
     120.0 s; VO scene boundaries land on 12/27/43/60/76/93/106/114.
   - `video`: fade in/out + subtitle overlay.
   - `audio`: 9 VOs + music bed (sidechain-ducked) + sfx3, loudnorm −14 LUFS.
   - `mux`: h264 copy + aac 192k, faststart. **No `-shortest`** — both streams
     are asserted 120.0 s first (v2 lesson).

## Key lesson-learned notes (v1→v3)

- v1 was rejected as a "static-image slideshow" → v2/v3 must move every beat.
- xfade on trimmed segments needs `setpts=PTS-STARTPTS,fps=30` after each trim.
- A whole-clip xfade outputs offset+len(clip2) — assert intermediate durations.
- Single-frame PNG overlays need `-loop 1 -framerate 30` or alpha fades hold frame 0.
- zoompan `on` is the global output frame counter; trig (sin) is allowed in x/y.
- Corner labeling for a tilted screen: TL=min(x+y), BR=max(x+y),
  TR=max(x−y), BL=min(x−y) (swapping TR/BL folds the warp diagonally).
- Verify PIL image patches numerically (pixel diff / edge energy); preview
  renders of blurred regions can look deceptively crisp.

## Non-regenerable sources (committed)

- `video/*.png` — AI cinematic plates (v2 + v3) and v2 UI card shots.
- `assets/` — supplied brand references, logo, Tajawal/Noto fonts.
- `audio/` — approved Saudi-Arabic VO lines (voice "voice-00") + synthesized
  music bed (rebuildable via `music_gen.py`).
