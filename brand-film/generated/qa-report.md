# QA report — generated

Generated 2026-09-27 from `tools/film-data.mjs`. Re-run `node tools/build-files.mjs` after any timing edit.

Options: fps=both · workshop=false · gate-b=default · gate-c=false

**Runtime 142.0 s** (ceiling 145.0 s) · **0 failures · 0 warnings**

## Failures

- none

## Warnings

- none

## Notes

- [vo] primary narration ≈ 60.3 s of speech = 42% of a 142.0 s runtime
- [asset] 1 supplied · 40 required and missing · 48 ids in the manifest

## Frame quantisation (nominal half-second grid → whole frames)

| fps | times falling between frames | worst rounding error |
|---|---|---|
| 25 | 48 | 0.500 f (0.020 s) |
| 30 | 0 | 0.000 f (0.000 s) |

## Runtime by option set

| Option set | Runtime | Inside 2:22 ±3 s |
|---|---|---|
| Base master | 142.0 s | yes |
| + workshop beat (2.5 s) | 144.5 s | yes |
| + Gate B free-shipping line (1.8 s) | 143.8 s | yes |
| + Gate C Amazon/Noon card (4.4 s) | 146.4 s | **no** |
| + workshop + Gate B (4.3 s) | 146.3 s | **no** |
| + Gate B + Gate C (6.2 s) | 148.2 s | **no** |
| + every optional element (8.7 s) | 150.7 s | **no** |

## Asset status

| Status | Count |
|---|---|
| supplied | 1 |
| required | 44 |
| not-in-package | 3 |

Referenced by shots but not supplied:

- `HAIL-01` — Hail exterior / Barzan area
- `SHOP-EXT-01` — Storefront with sign & logo
- `SHOP-INT-01` — Shop interior — shelves, lanterns
- `SHOP-INT-02` — Shop interior — second angle
- `SHOP-INT-03` — Shop interior — entrance
- `BR-01` — برزان — خلف بنك الراجحي exterior
- `BR-02` — السوق الشعبي exterior
- `BR-03` — عقدة — منتزه الأدهم exterior
- `WOOD-01` — Dry Athal stock, stacked
- `WOOD-02` — Athal grain macro
- `WOOD-03` — Cut blanks laid out
- `CRAFT-01` — Measuring / marking
- `CRAFT-02` — Cutting / shaping
- `CRAFT-03` — Assembly of body
- `CRAFT-04` — Smoothing / sanding
- `CRAFT-05` — Decorative carving
- `CRAFT-06` — Fitting metal lining
- `CRAFT-07` — Setting brass studs — hero
- `PRD-HAY-01` — حايلي — hero angle
- `PRD-HAY-02` — حايلي — second angle
- `PRD-NAJ-01` — نجدي ملكي — hero angle
- `PRD-JAM-01` — حايلي — شكل جميلي (42 سم class)
- `PRD-SUL-01` — سليماني design
- `PRD-SM-01` — Small portable (8–15 cm band)
- `PRD-MD-01` — Medium 18–29 cm
- `PRD-LG-01` — Large 40–42 cm
- `PRD-MAJ-01` — Large custom majlis piece
- `PERS-01` — Real engraved / applied name
- `PERS-02` — Company logo applied to a product
- `COLR-01` — Colour options, photographed
- `GIFT-01` — Single-burner gift box
- `GIFT-02` — Set of two
- `GIFT-03` — Set of three (طقم ٣ حبه)
- `GIFT-BAB-01` — Bab Hail-style box (بوكس باب حائل)
- `OUD-01` — Oud wood chips
- `OUD-02` — Bukhoor
- `OUD-03` — Oud oil bottles (دهن العود)
- `PACK-01` — Real packing / wrapping / boxing
- `WEB-01` — Screen recording of mabkhrahaill.com (Salla)
- `WEB-02` — Screen recording of the Trendyol store page
