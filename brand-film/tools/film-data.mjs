/**
 * مبخرة حائل — BRAND FILM · SINGLE SOURCE OF TRUTH
 * ------------------------------------------------
 * Every timecode, caption, voiceover line, asset ID and gate in this package
 * is derived from this file. Change it here, re-run `node tools/build-files.mjs`,
 * and the EDL, caption timing sheet, VO budget, SRTs and QA report all follow.
 *
 * Times are SECONDS (the client's own grid). The builder converts to whole
 * frames at the master rate. Half-second boundaries are NOT frame-legal at
 * 25 fps (0.5 s = 12.5 frames) — the builder quantises and reports the error.
 *
 * Conventions
 *   start          inclusive, seconds
 *   end            EXCLUSIVE, seconds
 *   captions       `end` is exclusive; the 8-frame fade-in and 8-frame fade-out
 *                  both live INSIDE [start, end) — see 04-caption-and-graphics-spec
 *   vo.kind        'primary'  = the take that is cut into the master
 *                  'alt'      = recorded and held, not placed until its gate clears
 *   vo.condition   null | 'gate-b' | 'gate-c' | 'workshop'
 */

export const FILM = {
  brand: 'مبخرة حائل',
  brandLatin: 'Mabkhra Haill',
  title: 'Mabkhra Haill — Brand Film',
  slug: 'mabkhra-haill-brand-film',
  masterSeconds: 142.0, // 2:22.0
  runtimeToleranceSeconds: 3.0,
  fpsOptions: [25, 30],
  aspect: '9:16',
  audio: '48 kHz / 24-bit stereo',
  arPaceWordsPerSecond: 3.0, // client's casting brief: ~3 words/second
};

/* ------------------------------------------------------------------ *
 * 1. ASSET MANIFEST
 * ------------------------------------------------------------------ */

export const ASSETS = [
  { id: 'LOGO-01', name: 'Original logo — brown on white', type: 'Vector/PNG', status: 'supplied', note: 'Also need transparent PNG + cream/white knockout' },
  { id: 'HAIL-01', name: 'Hail exterior / Barzan area', type: 'Video 4K', status: 'required', note: 'Must be genuinely Hail' },
  { id: 'SHOP-EXT-01', name: 'Storefront with sign & logo', type: 'Video/Photo', status: 'required', note: 'Opening identity shot' },
  { id: 'SHOP-INT-01', name: 'Shop interior — shelves, lanterns', type: 'Video', status: 'required' },
  { id: 'SHOP-INT-02', name: 'Shop interior — second angle', type: 'Video', status: 'required' },
  { id: 'SHOP-INT-03', name: 'Shop interior — entrance', type: 'Video', status: 'required' },
  { id: 'BR-01', name: 'برزان — خلف بنك الراجحي exterior', type: 'Photo', status: 'required' },
  { id: 'BR-02', name: 'السوق الشعبي exterior', type: 'Photo', status: 'required' },
  { id: 'BR-03', name: 'عقدة — منتزه الأدهم exterior', type: 'Photo', status: 'required' },
  { id: 'WKS-01', name: 'Workshop wide — identified as workshop', type: 'Video', status: 'required', note: 'Never counted as a 4th branch' },
  { id: 'WOOD-01', name: 'Dry Athal stock, stacked', type: 'Video/Photo', status: 'required' },
  { id: 'WOOD-02', name: 'Athal grain macro', type: 'Video/Photo', status: 'required' },
  { id: 'WOOD-03', name: 'Cut blanks laid out', type: 'Video/Photo', status: 'required' },
  { id: 'CRAFT-01', name: 'Measuring / marking', type: 'Video', status: 'required' },
  { id: 'CRAFT-02', name: 'Cutting / shaping', type: 'Video', status: 'required' },
  { id: 'CRAFT-03', name: 'Assembly of body', type: 'Video', status: 'required' },
  { id: 'CRAFT-04', name: 'Smoothing / sanding', type: 'Video', status: 'required' },
  { id: 'CRAFT-05', name: 'Decorative carving', type: 'Video', status: 'required', note: 'Only on models that carry it' },
  { id: 'CRAFT-06', name: 'Fitting metal lining', type: 'Video', status: 'required' },
  { id: 'CRAFT-07', name: 'Setting brass studs — hero', type: 'Video', status: 'required' },
  { id: 'CRAFT-08', name: 'Final finishing / wipe-down', type: 'Video', status: 'required', note: 'Optional — no slot in the 2:22 master' },
  { id: 'PRD-HAY-01', name: 'حايلي — hero angle', type: 'Photo', status: 'required' },
  { id: 'PRD-HAY-02', name: 'حايلي — second angle', type: 'Photo', status: 'required' },
  { id: 'PRD-NAJ-01', name: 'نجدي ملكي — hero angle', type: 'Photo', status: 'required' },
  { id: 'PRD-NAJ-02', name: 'نجدي ملكي — second angle', type: 'Photo', status: 'required' },
  { id: 'PRD-JAM-01', name: 'حايلي — شكل جميلي (42 سم class)', type: 'Photo', status: 'required', note: 'Catalogue calls it "مباخر حايلي شكلٍ جميلي تراثي" — a حايلي shape variant, not a separate family' },
  { id: 'PRD-SUL-01', name: 'سليماني design', type: 'Photo', status: 'required', note: 'NOT visible in the live catalogue page sampled — verify before it goes on screen (audit A17)' },
  { id: 'PRD-SM-01', name: 'Small portable (8–15 cm band)', type: 'Photo', status: 'required', note: 'No 8–15 cm item seen in the live catalogue page sampled — 18/20/29/42 cm only (audit A18)' },
  { id: 'PRD-MD-01', name: 'Medium 18–29 cm', type: 'Photo', status: 'required' },
  { id: 'PRD-LG-01', name: 'Large 40–42 cm', type: 'Photo', status: 'required' },
  { id: 'PRD-MAJ-01', name: 'Large custom majlis piece', type: 'Photo', status: 'required' },
  { id: 'PERS-01', name: 'Real engraved / applied name', type: 'Photo', status: 'required' },
  { id: 'PERS-02', name: 'Company logo applied to a product', type: 'Photo', status: 'required' },
  { id: 'PERS-03', name: 'Third personalisation example', type: 'Photo', status: 'required', note: 'Optional' },
  { id: 'COLR-01', name: 'Colour options, photographed', type: 'Photo', status: 'required', note: 'Real finishes only' },
  { id: 'GIFT-01', name: 'Single-burner gift box', type: 'Photo', status: 'required' },
  { id: 'GIFT-02', name: 'Set of two', type: 'Photo', status: 'required' },
  { id: 'GIFT-03', name: 'Set of three (طقم ٣ حبه)', type: 'Photo', status: 'required' },
  { id: 'GIFT-BAB-01', name: 'Bab Hail-style box (بوكس باب حائل)', type: 'Photo', status: 'required' },
  { id: 'OUD-01', name: 'Oud wood chips', type: 'Photo', status: 'required' },
  { id: 'OUD-02', name: 'Bukhoor', type: 'Photo', status: 'required' },
  { id: 'OUD-03', name: 'Oud oil bottles (دهن العود)', type: 'Photo', status: 'required' },
  { id: 'PACK-01', name: 'Real packing / wrapping / boxing', type: 'Video', status: 'required' },
  { id: 'WEB-01', name: 'Screen recording of mabkhrahaill.com (Salla)', type: 'Screen capture', status: 'required', note: 'Never simulate' },
  { id: 'WEB-02', name: 'Screen recording of the Trendyol store page', type: 'Screen capture', status: 'required' },
  // --- gaps found against the LIVE catalogue (audit R9) ---
  { id: 'SAF-01', name: 'Saffron (زعفران) — sold in the store, absent from the film', type: 'Photo', status: 'not-in-package', note: 'Store category c20806586 — decide in or out (audit A19)' },
  { id: 'BAKH-01', name: 'علبة بخور (incense box) — sold in the store, absent from the film', type: 'Photo', status: 'not-in-package', note: 'Products p804278914 / p1617462754' },
  { id: 'SET-01', name: 'طقم / sets of two and three mubkharas', type: 'Photo', status: 'not-in-package', note: 'Covered by GIFT-02/03 if shot for the gift boxes' },
];

/* ------------------------------------------------------------------ *
 * 2. SCENES  (timeline order — the VO leads, as the brief requires)
 * ------------------------------------------------------------------ */

export const SCENES = [
  {
    id: 'S1',
    briefScene: 'Scene 1',
    labelAr: 'حائل والهوية',
    labelEn: 'Hail & identity',
    start: 0.0,
    end: 12.5,
    shots: [
      { id: '1A', asset: 'HAIL-01', start: 0.0, end: 4.0, direction: 'Slow push-in, real Hail exterior, warm low-angle light. No speed ramp.' },
      { id: '1B', asset: 'SHOP-EXT-01', start: 4.0, end: 8.5, direction: 'Static or 2% drift on the storefront. Sign fully legible, uncropped.' },
      { id: '1C', asset: 'LOGO-01', start: 8.5, end: 12.5, direction: 'Logo fades up over soft-defocused shop interior. Hold 2.5 s minimum.' },
    ],
    captions: [
      { id: 'C1', kind: 'brand-lockup', start: 8.9, end: 12.34, ar: 'مبخرة حائل · منذ 1998', en: 'Mabkhra Haill · Since 1998' },
    ],
    vo: [
      {
        id: 'V1', briefLine: 1, kind: 'primary', start: 1.0,
        ar: 'من حائل، تبدأ حكايتنا… حكاية حرفة وتراث وضيافة، منذ عام ألف وتسعمئة وثمانية وتسعين.',
        en: 'From Hail, our story begins… a story of craft, heritage and hospitality — since 1998.',
        note: 'Narrative line — the picture is already moving, no sync mark needed.',
      },
    ],
    audio: 'Light outdoor ambience, then shop room tone. Music enters at 00:02 at −26 LUFS (pre-duck).',
  },
  {
    id: 'S2',
    briefScene: 'Scene 2',
    labelAr: 'خشب الأثل',
    labelEn: 'Athal wood',
    start: 12.5,
    end: 26.5,
    shots: [
      { id: '2A', asset: 'WOOD-01', start: 12.5, end: 16.5, direction: 'Stacked dry Athal stock, slow lateral slide.' },
      { id: '2B', asset: 'WOOD-02', start: 16.5, end: 20.5, direction: 'Macro grain, shallow DOF, rack focus along the grain.' },
      { id: '2C', asset: 'WOOD-03', start: 20.5, end: 23.5, direction: 'Prepared blanks laid out; a hand enters to turn one piece.' },
      { id: '2D', asset: 'CRAFT-01', start: 23.5, end: 26.5, direction: 'Measuring / pencil marking, one continuous action.' },
    ],
    captions: [
      { id: 'C2', kind: 'lower-third', start: 13.4, end: 18.2, ar: 'خشب أثل ناشف… مختار بعناية', en: 'Dry Athal wood… carefully chosen' },
    ],
    vo: [
      {
        id: 'V2', briefLine: 2, kind: 'primary', start: 13.0,
        ar: 'في مبخرة حائل، نختار خشب الأثل الناشف بعناية، ونهتم بكل تفصيلة.',
        en: 'At Mabkhra Haill we choose dry Athal wood carefully, and we care about every detail.',
        note: 'SPLIT from brief line 2 — the process clause moves to V3a so the craft actions are named as they happen (audit A3).',
      },
      {
        id: 'V2-orig', briefLine: 2, kind: 'alt', start: 13.0,
        ar: 'في مبخرة حائل، نختار خشب الأثل الناشف بعناية، ونهتم بكل تفصيلة، من تجهيز الخشب وتشكيله، إلى تجميع القطع وتشطيبها.',
        en: 'At Mabkhra Haill we choose dry Athal wood carefully, and we care about every detail — from preparing and shaping the wood to assembling and finishing the pieces.',
        note: 'ALTERNATE: the brief\'s original unsplit line. Record it; do not place it unless the editor abandons the sync-corrected cut.',
      },
    ],
    audio: 'Quiet workshop room tone. One soft wood-on-bench contact sound at 00:21.',
  },
  {
    id: 'S3',
    briefScene: 'Scene 3',
    labelAr: 'الصناعة',
    labelEn: 'The making',
    start: 26.5,
    end: 41.0,
    shots: [
      { id: '3A', asset: 'CRAFT-02', start: 26.5, end: 29.0, direction: 'Cutting/shaping — wide enough to read the action.' },
      { id: '3B', asset: 'CRAFT-03', start: 29.0, end: 31.5, direction: 'Assembly: one panel joined to the body.' },
      { id: '3C', asset: 'CRAFT-04', start: 31.5, end: 34.0, direction: 'Smoothing, hand travelling along the surface.' },
      { id: '3D', asset: 'CRAFT-05', start: 34.0, end: 36.5, direction: 'Carving detail, macro.' },
      { id: '3E', asset: 'CRAFT-06', start: 36.5, end: 38.5, direction: 'Metal lining seated into the body.' },
      { id: '3F', asset: 'CRAFT-07', start: 38.5, end: 41.0, direction: 'Brass stud set — hero macro, catch the brass highlight.' },
    ],
    captions: [
      { id: 'C3', kind: 'lower-third', start: 27.1, end: 30.6, ar: 'صناعة يدوية', en: 'Handmade' },
      { id: 'C4', kind: 'lower-third', start: 34.4, end: 37.6, ar: 'تفاصيل تراثية', en: 'Heritage detail' },
      { id: 'C5', kind: 'lower-third', start: 38.7, end: 41.0, ar: 'مسامير نحاس', en: 'Brass studs' },
    ],
    vo: [
      {
        id: 'V3a', briefLine: 3, kind: 'primary', start: 27.2,
        ar: 'من تجهيز الخشب وتشكيله، إلى تجميع القطع وتشطيبها بأيدي حرفيينا.',
        en: 'From preparing and shaping the wood to assembling and finishing the pieces — by our craftsmen\'s hands.',
        note: 'Moved here from line 2 (audit T2). Names the action in 3A/3B/3C as it happens.',
        syncMarks: [
          { word: 'وتشكيله', target: 28.4 },
          { word: 'تجميع', target: 29.1 },
          { word: 'وتشطيبها', target: 30.1 },
          { word: 'بأيدي حرفيينا', target: 30.6 },
        ],
      },
      {
        id: 'V3b', briefLine: 3, kind: 'primary', start: 34.2,
        ar: 'وتكتمل بتفاصيل النقش، والتلبيس المعدني، ومسامير النحاس، بحسب تصميم كل قطعة.',
        en: 'It is completed with carving detail, the metal lining and brass studs — according to each piece\'s design.',
        note: 'SPLIT from brief line 3 so lining/studs are named on 3E/3F (audit A3).',
        syncMarks: [
          { word: 'النقش', target: 35.3 },
          { word: 'والتلبيس المعدني', target: 36.5 },
          { word: 'ومسامير النحاس', target: 37.6 },
          { word: 'بحسب تصميم كل قطعة', target: 38.7 },
        ],
      },
      {
        id: 'V3-orig', briefLine: 3, kind: 'alt', start: 27.0,
        ar: 'وبأيدي حرفيينا، تأخذ المبخرة شكلها، وتكتمل بتفاصيل النقش والتلبيس المعدني ومسامير النحاس، بحسب تصميم كل قطعة.',
        en: 'By our craftsmen\'s hands the mubkhara takes its shape, completed with carving, metal lining and brass studs, according to each piece\'s design.',
        note: 'ALTERNATE: the brief\'s original unsplit line 3.',
      },
    ],
    audio: 'Real and restrained — saw, sanding, a single tap on the stud. All −18 dB under VO. One event per shot.',
  },
  {
    id: 'S4',
    briefScene: 'Scene 4',
    labelAr: 'المجموعة',
    labelEn: 'The collection',
    start: 41.0,
    end: 54.5,
    // Re-timed from the brief (audit A1): 4A/4B 3.0 → 2.9 s so the conditional 4C slot can
    // hold 2.2 s instead of 2.0 s and the section still ends at 54.5 (audit T1).
    shots: [
      { id: '4A', asset: 'PRD-HAY-01', start: 41.0, end: 43.9, direction: 'Hero حايلي, slow push, real silhouette preserved.', minSeconds: 2.2 },
      { id: '4B', asset: 'PRD-NAJ-01', start: 43.9, end: 46.8, direction: 'نجدي ملكي, slow push.', minSeconds: 2.2 },
      { id: '4C', asset: 'PRD-JAM-01|PRD-SUL-01', start: 46.8, end: 49.0, direction: 'Conditional slot — only if the reference exists. Otherwise add 1.0 s to 4A and 1.2 s to 4B.', minSeconds: 2.2 },
      { id: '4D', asset: 'PRD-MAJ-01|PRD-LG-01', start: 49.0, end: 51.7, direction: 'Large piece, low angle for scale.', minSeconds: 2.2 },
      { id: '4E', asset: 'PRD-SM-01+PRD-MD-01', start: 51.7, end: 54.5, direction: 'Small and medium together in one composed frame.', minSeconds: 2.2 },
    ],
    captions: [
      { id: 'C6', kind: 'product-label', start: 41.4, end: 43.7, ar: 'حايلي', en: 'Haili' },
      { id: 'C7', kind: 'product-label', start: 44.3, end: 46.6, ar: 'نجدي ملكي', en: 'Najdi Malaki' },
      { id: 'C9', kind: 'product-label', start: 49.3, end: 51.5, ar: 'للمجالس والضيافة', en: 'For majlis & hospitality' },
      { id: 'C10', kind: 'product-label', start: 52.1, end: 54.34, ar: 'للهدايا والمناسبات', en: 'For gifts & occasions' },
    ],
    vo: [
      {
        id: 'V4', briefLine: 4, kind: 'primary', start: 41.4,
        ar: 'من المباخر الحائلية… إلى النجدية الملكية… تصاميم ومقاسات تناسب استخدامكم، ومجالسكم، وضيافتكم، ومناسباتكم.',
        en: 'From the Haili mubkharas… to the Najdi Malaki… designs and sizes for your use, your majlis, your hospitality and your occasions.',
        note: 'Two internal beats added so the product names land on their shots (audit A3).',
        syncMarks: [
          { word: 'الحائلية', target: 41.4 },
          { word: 'النجدية الملكية', target: 43.9 },
          { word: 'تصاميم ومقاسات', target: 46.9 },
          { word: 'ومجالسكم', target: 48.3 },
          { word: 'ومناسباتكم', target: 49.1 },
        ],
      },
    ],
    audio: 'Music forward here; no SFX. 8–12 frame dissolves between the product stills only.',
  },
  {
    id: 'S5',
    briefScene: 'Scene 6',
    labelAr: 'الهدايا والبوكسات',
    labelEn: 'Gifts & boxes',
    start: 54.5,
    end: 68.0,
    shots: [
      { id: '6A', asset: 'GIFT-01', start: 54.5, end: 57.5, direction: 'Single-burner box, lid at rest. Contents exactly as photographed.' },
      { id: '6B', asset: 'GIFT-02|GIFT-03', start: 57.5, end: 60.5, direction: 'Set of two or three, overhead or ¾.' },
      { id: '6C', asset: 'GIFT-BAB-01', start: 60.5, end: 63.5, direction: 'Bab Hail-style box, slow lateral drift.' },
      { id: '6D', asset: 'OUD-01|OUD-02|OUD-03', start: 63.5, end: 68.0, direction: 'Oud chips, bukhoor, oud-oil bottles — only those actually photographed.' },
    ],
    captions: [
      { id: 'C11', kind: 'lower-third', start: 55.1, end: 59.5, ar: 'هدايا تحمل طابع حائل', en: 'Gifts with the character of Hail' },
      { id: 'C12', kind: 'micro-label', start: 58.0, end: 61.5, ar: 'المحتويات حسب الباقة', en: 'Contents vary by package', recommended: true },
    ],
    vo: [
      {
        id: 'V5a', briefLine: 5, kind: 'primary', start: 55.2,
        ar: 'ولأن لكل هدية معنى، نجهّز لكم خيارات مميزة من بوكسات المباخر.',
        en: 'Because every gift has meaning, we prepare distinctive mubkhara box options for you.',
        note: 'SPLIT from brief line 5 so the oud/contents sentence lands on the 6D shots (audit A3).',
      },
      {
        id: 'V5b', briefLine: 5, kind: 'primary', start: 64.0,
        ar: 'مع العود والبخور ودهن العود، بحسب الباقة المختارة.',
        en: 'With oud, bukhoor and oud oil — according to the package chosen.',
        note: 'SPLIT from brief line 5. Matches the live catalogue, where some gift boxes include oud and some do not.',
        syncMarks: [
          { word: 'العود', target: 64.0 },
          { word: 'والبخور', target: 64.6 },
          { word: 'ودهن العود', target: 65.2 },
        ],
      },
      {
        id: 'V5-orig', briefLine: 5, kind: 'alt', start: 55.0,
        ar: 'ولأن لكل هدية معنى، نجهّز لكم خيارات مميزة من بوكسات المباخر، مع العود والبخور ودهن العود بحسب الباقة المختارة.',
        en: 'Because every gift has meaning, we prepare distinctive mubkhara box options — with oud, bukhoor and oud oil according to the package chosen.',
        note: 'ALTERNATE: the brief\'s original unsplit line 5.',
      },
    ],
    audio: 'Soft tissue/card handling only where visible. No rustle under the VO.',
  },
  {
    id: 'S6',
    briefScene: 'Scene 5',
    labelAr: 'التخصيص',
    labelEn: 'Personalisation',
    start: 68.0,
    end: 80.5,
    shots: [
      { id: '5A', asset: 'PERS-01', start: 68.0, end: 72.0, direction: 'Real engraved/applied name, macro, slow drift across the lettering.' },
      { id: '5B', asset: 'PERS-02', start: 72.0, end: 76.0, direction: 'Company logo on a product — a real example.' },
      { id: '5C', asset: 'COLR-01', start: 76.0, end: 80.5, direction: 'Colour/size options side by side, real finishes only.' },
    ],
    captions: [
      { id: 'C13', kind: 'lower-third', start: 68.7, end: 73.0, ar: 'باسمك… وعلى ذوقك', en: 'In your name… and to your taste' },
      { id: 'C14', kind: 'lower-third', start: 73.6, end: 78.0, ar: 'أسماء وشعارات وتجهيز حسب الطلب', en: 'Names, logos and made-to-order preparation' },
      { id: 'C13b', kind: 'disclaimer-badge', start: 68.0, end: 80.5, ar: 'نموذج توضيحي للتخصيص', en: 'Illustrative personalisation mock-up', conditional: 'gate-h' },
    ],
    vo: [
      {
        id: 'V6', briefLine: 6, kind: 'primary', start: 68.5,
        ar: 'وتقدرون تضيفون لمستكم الخاصة، بكتابة الاسم أو الشعار… واختيار التصميم واللون والمقاس حسب الطلب.',
        en: 'You can add your own touch — your name or logo… and choose the design, colour and size to order.',
        note: 'One beat added after «الشعار» so the colour/size clause lands on 5C (audit A3).',
        syncMarks: [
          { word: 'بكتابة الاسم', target: 70.0 },
          { word: 'أو الشعار', target: 71.2 },
          { word: 'واختيار التصميم واللون والمقاس', target: 75.6 },
        ],
      },
    ],
    audio: 'Room tone only. No music swell.',
  },
  {
    id: 'S7',
    briefScene: 'Scene 8A',
    labelAr: 'الطلبات والتجهيز',
    labelEn: 'Orders & fulfilment',
    start: 80.5,
    end: 90.5,
    shots: [
      { id: '8A-1', asset: 'PACK-01', start: 80.5, end: 84.0, direction: 'Wrapping a burner — real hands, real material.' },
      { id: '8A-2', asset: 'PACK-01', start: 84.0, end: 87.5, direction: 'Box closing / sealing (second angle of the same source).' },
      { id: '8A-3', asset: 'PACK-01', start: 87.5, end: 90.5, direction: 'Finished packed boxes stacked, ready.' },
    ],
    captions: [
      { id: 'C15', kind: 'lower-third', start: 81.0, end: 85.0, ar: 'طلبات أفراد وكميات', en: 'Retail and bulk orders' },
      { id: 'C16', kind: 'lower-third', start: 85.5, end: 89.0, ar: 'هدايا الشركات', en: 'Corporate gifts' },
    ],
    vo: [
      {
        id: 'V7', briefLine: 7, kind: 'primary', start: 81.0,
        ar: 'نستقبل طلبات الأفراد والكميات وهدايا الشركات، ونهتم بالتجهيز والتغليف قبل الشحن.',
        en: 'We take individual, bulk and corporate-gift orders, and we take care of preparation and packing before shipping.',
        note: 'Light beat after «الشركات،» so the packing clause lands on 8A-3.',
        syncMarks: [
          { word: 'طلبات الأفراد والكميات', target: 81.2 },
          { word: 'وهدايا الشركات', target: 82.8 },
          { word: 'وبالتجهيز والتغليف', target: 86.6 },
        ],
      },
    ],
    audio: 'Tissue, card, tape — natural level, no exaggeration. One event per shot maximum.',
  },
  {
    id: 'S8',
    briefScene: 'Scene 7',
    labelAr: 'المعرض والفروع',
    labelEn: 'The showroom & branches',
    start: 90.5,
    end: 102.5,
    contains: 'workshop',
    shots: [
      { id: '7A', asset: 'SHOP-INT-01', start: 90.5, end: 93.5, direction: 'Shop interior, shelves and lanterns as they really are.' },
      { id: '7B', asset: 'BR-01|SHOP-INT-02', start: 93.5, end: 96.5, direction: 'Branch card 1. A branch exterior is shown only if its own photograph exists.' },
      { id: '7C', asset: 'BR-02|SHOP-INT-03', start: 96.5, end: 99.5, direction: 'Branch card 2.' },
      { id: '7D', asset: 'BR-03|SHOP-EXT-01', start: 99.5, end: 102.5, direction: 'Branch card 3.' },
      { id: '8E', asset: 'WKS-01', start: 102.5, end: 105.0, direction: 'OPTIONAL workshop beat — inserted only when WKS-01 exists. Runs 2.5 s (not 1.5 s): a 1.5 s shot cannot carry a caption inside the 2.0 s minimum dwell (audit A2). Shifts every later section +2.5 s.', optional: 'workshop' },
    ],
    captions: [
      { id: 'C17', kind: 'branch-card', start: 93.7, end: 96.3, ar: 'برزان — خلف بنك الراجحي', en: 'Barzan — behind Al Rajhi Bank' },
      { id: 'C18', kind: 'branch-card', start: 96.7, end: 99.3, ar: 'السوق الشعبي', en: 'The popular market' },
      { id: 'C19', kind: 'branch-card', start: 99.7, end: 102.34, ar: 'عقدة — منتزه الأدهم', en: 'Uqdah — Al Adham Park' },
      { id: 'C20', kind: 'lower-third', start: 102.8, end: 104.9, ar: 'ورشتنا', en: 'Our workshop', optional: 'workshop' },
    ],
    vo: [
      {
        id: 'V8', briefLine: 8, kind: 'primary', start: 91.0,
        ar: 'حيّاكم في فروعنا الثلاثة بحائل: برزان خلف بنك الراجحي… والسوق الشعبي… وعقدة في منتزه الأدهم.',
        en: 'Welcome to our three branches in Hail: Barzan behind Al Rajhi Bank… the popular market… and Uqdah in Al Adham Park.',
        note: 'Enumeration line — RECORD TO THE PICTURE. The three branch names must start on the sync marks, tolerance ±0.3 s.',
        syncMarks: [
          { word: 'برزان خلف بنك الراجحي', target: 93.6 },
          { word: 'والسوق الشعبي', target: 96.6 },
          { word: 'وعقدة في منتزه الأدهم', target: 99.6 },
        ],
      },
    ],
    audio: 'Shop room tone. No location SFX invented. No maps, no pins, no addresses beyond the three lines.',
  },
  {
    id: 'S9',
    briefScene: 'Scene 9',
    labelAr: 'قنوات الشراء',
    labelEn: 'Where to buy',
    start: 102.5,
    end: 111.5,
    contains: 'gate-c',
    shots: [
      { id: '9A', asset: 'WEB-01', start: 102.5, end: 107.5, direction: 'Real screen recording of mabkhrahaill.com — scroll a product page, no cursor jitter. MUST NOT contain prices or the current offer banners (audit A13).' },
      { id: '9B', asset: 'WEB-02', start: 107.5, end: 111.5, direction: 'Real Trendyol store capture. Record from a Saudi-geo browser after the country gate has been passed (audit A14). If Gate C clears, this shot extends by 4.4 s to carry the Amazon/Noon card.' },
    ],
    captions: [
      { id: 'C21', kind: 'url-card', start: 102.9, end: 107.34, ar: 'متجرنا الرسمي عبر منصة سلة', en: 'Our official store on Salla', secondLineLatin: 'mabkhrahaill.com' },
      { id: 'C22', kind: 'brand-name', start: 107.9, end: 111.34, ar: 'ترينديول', en: 'Trendyol' },
      { id: 'C22b', kind: 'brand-name', start: 111.7, end: 115.9, ar: 'أمازون السعودية · نون', en: 'Amazon Saudi Arabia · Noon', condition: 'gate-c', inInsert: 'gate-c' },
    ],
    vo: [
      {
        id: 'V9', briefLine: 9, kind: 'primary', start: 103.0,
        ar: 'وتقدرون تتسوّقون من موقعنا الإلكتروني على سلة، وتطّلعون على منتجاتنا في ترينديول.',
        en: 'You can shop from our online store on Salla, and browse our products on Trendyol.',
        syncMarks: [
          { word: 'على سلة', target: 105.4 },
          { word: 'في ترينديول', target: 106.8 },
        ],
      },
      {
        id: 'V9b', briefLine: '9b', kind: 'alt', start: 112.3, condition: 'gate-c', inInsert: 'gate-c',
        ar: 'وكذلك عبر أمازون السعودية ونون، حسب المنتجات المتاحة.',
        en: 'Also through Amazon Saudi Arabia and Noon, depending on available products.',
        note: 'ALTERNATE — do not place until Gate C clears. Adds a Scene 9 card and pushes the master to 2:26.4, outside the ±3 s target (audit A4).',
      },
    ],
    audio: 'Music only. Screen capture audio is muted; never let UI click sounds into the mix.',
  },
  {
    id: 'S10',
    briefScene: 'Scene 8B',
    labelAr: 'التوصيل والشحن',
    labelEn: 'Delivery & shipping',
    start: 111.5,
    end: 123.0,
    shots: [
      { id: '8B-1', asset: 'PACK-01|SHOP-INT-01', start: 111.5, end: 117.0, direction: 'Sealed boxes, calm hold (alternate angle / shop interior).' },
      { id: '8B-2', asset: 'PRD-MD-01', start: 117.0, end: 123.0, direction: 'Beauty product still, slow drift.' },
    ],
    captions: [
      { id: 'C23', kind: 'lower-third', start: 111.9, end: 116.8, ar: 'توصيل لجميع مناطق المملكة', en: 'Delivery to all regions of the Kingdom' },
      { id: 'C24', kind: 'lower-third', start: 117.4, end: 122.7, ar: 'اطّلعوا على خيارات الشحن والعروض الحالية في متجرنا.', en: 'See current shipping options and offers in our store.', condition: 'gate-b-default' },
      { id: 'C24b', kind: 'lower-third', start: 117.4, end: 122.7, ar: 'شحن مجاني داخل السعودية للطلبات بقيمة ٣٠٠ ريال فأكثر، وفق الشروط الموضحة في المتجر.', en: 'Free shipping inside Saudi Arabia on orders of SAR 300 and above, per the terms shown in the store.', condition: 'gate-b-cleared' },
    ],
    vo: [
      { id: 'V10a', briefLine: 10, kind: 'primary', start: 112.0, ar: 'نوصل لجميع مناطق المملكة.', en: 'We deliver to all regions of the Kingdom.', note: 'SPLIT from brief line 10 so the Gulf line lands on the 8B-2 product still (audit A3).' },
      { id: 'V10b', briefLine: 10, kind: 'primary', start: 117.1, ar: 'ونشحن لدول الخليج.', en: 'And we ship to the Gulf countries.', note: 'SPLIT from brief line 10. Never a claim of free international shipping.' },
      { id: 'V11', briefLine: 11, kind: 'primary', start: 119.0, ar: 'وتلقون خيارات الشحن والعروض الحالية في موقعنا.', en: 'You will find the current shipping options and offers on our site.', condition: 'gate-b-default' },
      { id: 'V11b', briefLine: '11b', kind: 'alt', start: 118.3, condition: 'gate-b-cleared', ar: 'والشحن مجاني داخل السعودية للطلبات بقيمة ثلاثمئة ريال فأكثر، حسب شروط المتجر.', en: 'Free shipping inside Saudi Arabia on orders of 300 riyals and above, per the store terms.', note: 'ALTERNATE — only if free shipping is live the day of publication. Re-verify before every re-post. Window is tight (4.3 s usable for a 4.0 s read, 0.3 s of slack): record at a slightly quicker pace or the line runs past the 123.0 s cut.' },
    ],
    audio: 'Music resolves downward. Last SFX at 116.5 (tape), then clean.',
  },
  {
    id: 'S11',
    briefScene: 'Scene 10A',
    labelAr: 'التواصل',
    labelEn: 'Contact',
    start: 123.0,
    end: 138.0,
    shots: [
      { id: '10A', asset: 'PRD-HAY-02', start: 123.0, end: 138.0, direction: 'Three uncluttered cards over a slow-drifting product still at 35% brightness. Never all links on one frame. Cards are text layers with their own in/out — see the card builds in 04-caption-and-graphics-spec.', shotIsPlate: true },
    ],
    captions: [
      { id: 'K1', kind: 'contact-card', start: 123.0, end: 127.6, ar: 'مبخرة حائل · منذ 1998\nمن حائل… نصنع الطيب ونهديه', en: 'Mabkhra Haill · Since 1998\nFrom Hail… we make the good scent and give it', secondLineLatin: 'mabkhrahaill.com' },
      { id: 'K2', kind: 'contact-card', start: 127.6, end: 132.4, ar: 'للتواصل والطلبات الخاصة\nالبريد الإلكتروني', en: 'Contact & special orders\nEmail', secondLineLatin: 'info@mabkhrahaill.com' },
      { id: 'K3', kind: 'social-card', start: 132.4, end: 138.0, ar: 'إنستغرام · سناب شات · تيك توك\nفيسبوك · إكس · يوتيوب\n@mabkharahaill', en: 'Instagram · Snapchat · TikTok\nFacebook · X · YouTube\n@mabkharahaill', secondLineLatin: 'linktr.ee/mabkharahaill', condition: 'gate-i-linktree' },
    ],
    vo: [
      { id: 'V12a', briefLine: 12, kind: 'primary', start: 123.4, ar: 'تابعونا على حساباتنا، واطّلعوا على كل جديد في موقعنا الإلكتروني.', en: 'Follow our accounts and see everything new on our website.', note: 'SPLIT from brief line 12 and re-mapped to Card 1. The brief named the platforms 6.5 s before the social card existed (audit A5).' },
      { id: 'V12b', briefLine: 12, kind: 'primary', start: 128.0, ar: 'وللطلبات الخاصة، تواصلوا معنا عبر البريد الإلكتروني الموضح على الشاشة.', en: 'For special orders, contact us at the email address shown on screen.', note: 'SPLIT from brief line 12 — mapped to the email card. No WhatsApp line: the number is unconfirmed (Gate A).' },
      {
        id: 'V12c', briefLine: 12, kind: 'primary', start: 132.8,
        ar: 'وتابعونا على إنستغرام، وسناب شات، وتيك توك، وفيسبوك، وإكس، ويوتيوب.',
        en: 'Follow us on Instagram, Snapchat, TikTok, Facebook, X and YouTube.',
        note: 'Enumeration line — record to the picture, platform names spread evenly across the card.',
        syncMarks: [
          { word: 'إنستغرام', target: 133.4 },
          { word: 'وسناب شات', target: 134.2 },
          { word: 'وتيك توك', target: 134.9 },
          { word: 'وفيسبوك', target: 135.6 },
          { word: 'وإكس', target: 136.2 },
          { word: 'ويوتيوب', target: 136.8 },
        ],
      },
      { id: 'V12d', briefLine: 12, kind: 'alt', start: 137.0, condition: 'gate-i-linktree', ar: 'وكل الروابط في مكان واحد.', en: 'And all the links in one place.', note: 'ALTERNATE — usable only if linktr.ee/mabkharahaill actually lists the site and all six platforms (audit A15).' },
    ],
    audio: 'Music bed only. Cards fade 8 frames in / 8 out, plus 12 px vertical drift.',
  },
  {
    id: 'S12',
    briefScene: 'Scene 10B',
    labelAr: 'الختام',
    labelEn: 'Close',
    start: 138.0,
    end: 142.0,
    shots: [
      { id: '10B', asset: 'LOGO-01', start: 138.0, end: 142.0, direction: 'Logo over a defocused PRD-HAY-02. Logo fades up centred, holds 3 s. Music resolves. Last 0.6 s fades to warm black (141.4 → 142.0).' },
    ],
    captions: [
      { id: 'C25', kind: 'brand-lockup', start: 138.8, end: 142.0, ar: 'مبخرة حائل · منذ 1998', en: 'Mabkhra Haill · Since 1998' },
    ],
    vo: [
      { id: 'V13', briefLine: 13, kind: 'primary', start: 138.5, ar: 'مبخرة حائل… من حائل، نصنع الطيب ونهديه.', en: 'Mabkhra Haill… from Hail, we make the good scent and give it.' },
    ],
    audio: 'Music resolves on the logo. No riser, no boom, no reverse cymbal.',
  },
];

/* ------------------------------------------------------------------ *
 * 3. GATES
 * ------------------------------------------------------------------ */

export const GATES = [
  { id: 'A', item: 'WhatsApp number', default: 'Card 2 renders email only. Placeholder never appears on screen or in VO.', clear: 'Owner supplies a confirmed active number → add one line to Card 2 at the same type size as the email line, and record a WhatsApp alternate for V12b.' },
  { id: 'B', item: 'Free shipping', default: 'C24 + V11 (the "see current options" line) are used.', clear: 'Owner confirms the offer is live today → swap to C24b + V11b. Re-verify before every re-post.' },
  { id: 'C', item: 'Amazon.sa / Noon', default: 'Omitted from caption and VO.', clear: 'Owner confirms live listings → add a Scene 9 card and place V9b. Costs 4.4 s of runtime (audit T4) — see the runtime budget in 02-edl-master.' },
  { id: 'D', item: 'Product sizes on screen', default: 'Omitted.', clear: 'Per-item written confirmation of the exact dimension for the exact product in that frame.' },
  { id: 'E', item: 'Gift-box contents', default: 'No caption implies contents. C12 badge recommended.', clear: 'Contents shown must equal contents photographed. Live catalogue confirms some boxes include oud/دهن العود and some do not — the VO wording already handles this.' },
  { id: 'F', item: 'Branch exteriors', default: 'Card over shop B-roll.', clear: 'Supply BR-01/02/03 photos to show real exteriors.' },
  { id: 'G', item: 'Website depiction', default: 'Real screen recording only.', clear: 'If WEB-01 is unavailable, Scene 9 shows the domain as a text card over product footage — never a simulated interface.' },
  { id: 'H', item: 'Personalisation mock-ups', default: 'Badge C13b runs for the whole of Scene 5 (68.0–80.5).', clear: 'Supply real produced examples to remove the badge.' },
  { id: 'I', item: 'Link directory integrity', default: 'Not in the original package.', clear: 'Run tooling/probe-links.mjs and clear every 404/redirect. linktr.ee/mabkharahaill currently lists only TikTok + Snapchat (audit V2) — either complete it or drop the "كل الروابط" line.' },
  { id: 'J', item: 'Making provenance', default: 'Craft captions and workshop VO only over genuinely workshop-made items.', clear: 'The live catalogue also sells imported handmade goods (e.g. "علبة بخور… صناعة يدوية باكستان" and طلح-wood items). Those items must never sit under «صناعة يدوية» / «بأيدي حرفيينا» (audit V5).' },
  { id: 'K', item: 'Transient commerce content', default: 'No price, discount, offer banner or countdown in any frame.', clear: 'The live store currently shows "عروض خاصة بمناسبة اليوم الوطني السعودي الـ96" with strikethrough prices. Screen-record a page without them, or mask them; those offers expire and will date the film (audit V4).' },
  { id: 'L', item: 'Runtime budget', default: 'Base master 2:22.0. Optional/conditional content totals +7.9 s.', clear: 'Runtime target is 2:22 ±3 s = 145.0 s maximum. Workshop (+2.5 s) is affordable alone. Gate B (+1.8 s) plus Gate C (+4.4 s) is not — pick one or renegotiate the target (audit T4).' },
];

/* ------------------------------------------------------------------ *
 * 4. LINK DIRECTORY — verified 2026-09-27
 * ------------------------------------------------------------------ */

export const LINKS = [
  { labelAr: 'الموقع الرسمي (منصة سلة)', url: 'https://mabkhrahaill.com/', burn: true, verified: 'live', method: 'fetched 2026-09-27', note: 'Salla storefront, redirects to /ar. One store, not two.' },
  { labelAr: 'البريد', url: 'mailto:info@mabkhrahaill.com', burn: true, verified: 'unverified', method: 'mail link — cannot be probed by HTTP', note: 'Send a test mail from an external account before burning.' },
  { labelAr: 'كل الروابط', url: 'https://linktr.ee/mabkharahaill', burn: true, verified: 'live-incomplete', method: 'fetched 2026-09-27', note: 'Lists only TikTok + Snapchat. "كل الروابط" is not true yet — Gate I.' },
  { labelAr: 'إنستغرام', url: 'https://www.instagram.com/mabkharahaill', burn: false, verified: 'unverified', method: 'HTTP 403 to automated probe', note: 'Open logged out in a private window and confirm the profile resolves.' },
  { labelAr: 'سناب شات', url: 'https://www.snapchat.com/add/Mabkharahaill', burn: false, verified: 'unverified', method: 'not probed' },
  { labelAr: 'تيك توك', url: 'https://www.tiktok.com/@Mabkharahaill', burn: false, verified: 'unverified', method: 'not probed' },
  { labelAr: 'فيسبوك', url: 'https://www.facebook.com/100059037517881/', burn: false, verified: 'unverified', method: 'numeric page id — confirm it resolves to the brand page, not a personal profile' },
  { labelAr: 'إكس', url: 'https://x.com/Mabkharahaill', burn: false, verified: 'unverified', method: 'not probed' },
  { labelAr: 'يوتيوب', url: 'https://www.youtube.com/@mabkharahaill', burn: false, verified: 'unverified', method: 'not probed' },
  { labelAr: 'تيليجرام', url: 'https://t.me/mabkharahaill', burn: false, verified: 'unverified', method: 'listed in the package but not in the film — keep it in the post text only' },
  { labelAr: 'ترينديول', url: 'https://www.trendyol.com/en/sr?mid=1159743', burn: false, verified: 'live-country-gate', method: 'fetched 2026-09-27', note: 'Bounced to /en/select-country when fetched without a country cookie. Record the capture from a Saudi-geo browser, after the country gate, so no interstitial appears in frame.' },
  { labelAr: 'أمازون السعودية / نون / واتساب', url: '', burn: false, verified: 'held', method: '—', note: 'Held pending owner verification. Not published — Gates A and C.' },
];

/* ------------------------------------------------------------------ *
 * 5. DELIVERABLES
 * ------------------------------------------------------------------ */

export const DELIVERABLES = [
  { cut: 'Master', runtime: '2:22', scope: 'Full film, captions burned, 1080×1920', use: 'Website, Linktree, YouTube (see note)' },
  { cut: 'Clean master', runtime: '2:22', scope: 'No burned captions', use: 'Re-versioning, other languages, sidecar subtitles' },
  { cut: 'Social 60', runtime: '0:60', scope: 'Sc 1 → 3 → 4 → 5 → 8 → 9/10', use: 'Reels, TikTok, Snapchat' },
  { cut: 'Social 30', runtime: '0:30', scope: 'Craft + collection + branches + website', use: 'Paid / retargeting' },
  { cut: 'Teaser 15', runtime: '0:15', scope: 'Brass stud macro → hero product → logo + domain', use: 'Hooks, Stories' },
  { cut: 'VO stem', runtime: '—', scope: 'Isolated narration, 48/24 WAV, split takes', use: 'Archive, re-versioning' },
  { cut: 'Subtitles', runtime: '—', scope: 'AR .srt (verbatim VO) + EN .srt', use: 'Accessibility, Gulf expat reach — ship on the CLEAN master, not under burned captions' },
  { cut: 'Stills', runtime: '—', scope: '3 × 1080×1920: end frame, logo lockup, hero product', use: 'Thumbnails / covers' },
  { cut: '16:9 reframe', runtime: '2:22', scope: 'MISSING FROM THE ORIGINAL PACKAGE — a 9:16 master cannot go to website/YouTube use as written', use: 'Website embed, YouTube (non-Shorts), presentations' },
];
