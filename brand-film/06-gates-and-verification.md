# 06 — Gates, verification and the link directory

Verification run: **2026-09-27**. Methods are stated so they can be repeated. `generated/vo-budget.csv` and `generated/caption-timing-*.csv` carry the gated elements as `ALTERNATE` / `GATED` rows, so nothing disappears when a gate is closed.

## 1. Live verification results

| # | Item | Result | Evidence | Consequence |
|---|---|---|---|---|
| V1 | `mabkhrahaill.com` | **Live.** Salla storefront, redirects to `/ar`, page title carries "من خشب الأثل" | direct fetch | The Scene 9 descriptor «متجرنا الرسمي عبر منصة سلة» is accurate. One store, not two — confirmed. |
| V2 | `linktr.ee/mabkharahaill` | **Live but incomplete** — lists only TikTok and Snapchat | direct fetch | Card 3's «كل الروابط» and the six-platform list are not yet true. **Gate I.** |
| V3 | `trendyol.com/en/sr?mid=1159743` | **Live, passes through a country-selection gate** (`/en/select-country`) without a country cookie | direct fetch | Record from a Saudi-geo browser after the gate; prefer a product deep link. **A14.** |
| V4 | Store offer state | **National-day offers live right now**, with strikethrough prices (e.g. 720 against 900) on most products | direct fetch | Any screen recording captures them; they expire within days. **Gate K.** |
| V5 | Catalogue content | نجدي / نجدي ملكي / نجدي رشم / حايلي families at 18, 20, 29 and 42 cm; «حايلي شكلٍ جميلي تراثي حجم ٤٢ سم»; gift boxes including «بوكس باب حائل»; a 29 cm gift box containing «أوقية عود ودهن عود كمبودي ربع تولة»; sets of three; incense boxes «صناعة يدوية باكستان» and طلح-wood items; a saffron category | direct fetch of two category pages | Validates the product vocabulary and the contents caveat; produces **A17, A18, A19, A24**. |
| V6 | Instagram profile | **403 to automated fetch** — could not be verified | direct fetch | Manual check required. **A21.** |
| V7 | Other social handles | Not probed in this session | — | Run `node brand-film/tools/probe-links.mjs` from a machine with open network. **A21.** |
| V8 | WhatsApp number, Amazon.sa, Noon listings, free-shipping offer, per-product sizes | **Still unconfirmed** | — | Gates A, B, C, D stay in their default state. Nothing on screen changes. |
| V9 | Founding year | "منذ 1998" not yet checked against a source document; the Linktree account dates from April 2023 | direct fetch | No conflict, but confirm the basis (1998 CE vs 1418/1419 H) before the lockup is burned. **A20.** |

## 2. Gates

Default state is what the film renders **today**, with no further input.

| Gate | Item | Default state (as shipped) | Action to clear | Owner |
|---|---|---|---|---|
| **A** | WhatsApp number | Card 2 renders email only. No placeholder on screen or in VO. | Supply a confirmed active number → one extra line in Card 2 at the email line's size, plus a WhatsApp alternate of V12b recorded. | Owner |
| **B** | Free shipping | C24 + V11: «اطّلعوا على خيارات الشحن والعروض الحالية في متجرنا.» | Confirm the offer is live on the day of publication → swap to C24b + V11b (+1.8 s runtime, Gate L). Re-verify before every re-post; a claims-free wording dates gracefully, an offer does not. | Owner |
| **C** | Amazon.sa / Noon | Omitted from caption and VO. | Confirm live listings → add the Scene 9 card and place V9b. **Costs 4.4 s and breaks the ±3 s target on its own** (Gate L). Recommended alternative: keep them out of the master and put them in the post text and the 30 s paid cut. | Owner |
| **D** | Product sizes on screen | Omitted everywhere. | Per-item written confirmation of the exact dimension for the exact product in that frame. Then, and only then, add a label. | Owner |
| **E** | Gift-box contents | No caption implies contents; C12 «المحتويات حسب الباقة» runs over the gift block. | Contents shown must equal contents photographed. Verified live: some packages include oud and oud oil, some do not — the existing wording is correct. | Producer |
| **F** | Branch exteriors | Card over shop B-roll for all three branches. | Supply BR-01/02/03 photographs to show real exteriors. Until then no exterior is shown and none is implied. | Owner |
| **G** | Website depiction | Real screen recording only. | If WEB-01 cannot be made, Scene 9 shows the domain as a text card over product footage. A simulated interface is never an option. | Producer |
| **H** | Personalisation mock-ups | Badge C13b «نموذج توضيحي للتخصيص» runs continuously across 68.0–80.5 s. | Supply real produced examples to remove the badge. | Owner |
| **I** | Link integrity | Not in the original package. | Complete the Linktree, then re-run the probe and clear every 404, redirect, expired offer and dead handle — including the numeric Facebook page id, which must resolve to the brand page and not a personal profile. | Owner |
| **J** | Making provenance | Craft captions and workshop VO only over genuinely workshop-made items. | Keep imported goods (the «صناعة يدوية باكستان» incense boxes, طلح-wood items) out of S2 and S3, or out of the film. «صناعة يدوية» over an imported box is a false claim with a paper trail. | Producer |
| **K** | Transient commerce content | No price, discount, offer badge, countdown or stale UI state in any frame. | Re-record or mask. Check the recording frame by frame before it enters Scene 9 — the offers visible today will be gone, and a price frozen in a brand film is a claim that outlives its truth. | Producer |
| **L** | Runtime budget | Base master 2:22.0. Optional content totals 8.7 s against a 3.0 s allowance. | Choose at most one optional element (≤3.0 s), or renegotiate the runtime target in writing before the cut locks. | Owner + Editor |

## 3. Link directory — burn status and verification

Burn into frame: **`mabkhrahaill.com`**, **`info@mabkhrahaill.com`**, **`@mabkharahaill`**, **`linktr.ee/mabkharahaill`** (the last only when Gate I clears). Platform **names** as text. Everything else lives in the post text.

| # | Label | URL | Burned | Verified 2026-09-27 |
|---|---|---|---|---|
| 1 | الموقع الرسمي (منصة سلة) | `https://mabkhrahaill.com/` | yes | ✅ live |
| 2 | البريد | `info@mabkhrahaill.com` | yes | ⚠️ mail link — cannot be probed by HTTP. Send a test mail from an external account. |
| 3 | كل الروابط | `https://linktr.ee/mabkharahaill` | yes | ⚠️ live but incomplete (TikTok + Snapchat only) |
| 4 | إنستغرام | `https://www.instagram.com/mabkharahaill` | no | ⚠️ 403 to automated probe |
| 5 | سناب شات | `https://www.snapchat.com/add/Mabkharahaill` | no | ⚠️ not probed |
| 6 | تيك توك | `https://www.tiktok.com/@Mabkharahaill` | no | ⚠️ not probed |
| 7 | فيسبوك | `https://www.facebook.com/100059037517881/` | no | ⚠️ numeric id — confirm it lands on the brand page |
| 8 | إكس | `https://x.com/Mabkharahaill` | no | ⚠️ not probed |
| 9 | يوتيوب | `https://www.youtube.com/@mabkharahaill` | no | ⚠️ not probed |
| 10 | تيليجرام | `https://t.me/mabkharahaill` | no | ⚠️ post text only, not in the film |
| 11 | ترينديول | `https://www.trendyol.com/en/sr?mid=1159743` | no | ⚠️ country gate; prefer a product deep link |
| 12 | أمازون السعودية · نون · واتساب | — | no | ⛔ held pending owner verification (Gates A, C) |

Probe them all with:

```bash
node brand-film/tools/probe-links.mjs             # all links, follows redirects, reports the final URL
node brand-film/tools/probe-links.mjs --json      # machine-readable
node brand-film/tools/probe-links.mjs --only=instagram,x,tiktok
```

The probe exits **2** with an explicit "no outbound network from this machine" message when it cannot reach the internet at all, so a sandboxed run can never be mistaken for twelve broken links. Exit **1** means at least one link needs attention.

## 4. The three answers the editor needs, and the one the owner needs

**Editor:** frame rate (30 recommended, A6) · scene order (VO-led as shipped, or the brief-led swap, which re-keys both blocks) · which optional elements, if any, are enabled (Gate L).

**Owner:** the four unconfirmed facts — WhatsApp number, free shipping, Amazon/Noon listings, per-product sizes — plus a decision on the Linktree (A15) and the mirror domains (A16).

## 5. Never stated anywhere in this film

Prices · discounts · reviews · awards · certifications · delivery-time guarantees · stock availability · "never cracks / never warps" · free international shipping · a fourth retail branch · drying, laser or machinery specifics not visible in supplied footage · any product, branch or service that has not been photographed or confirmed.

Agreed and re-checked on this build. Every caption and VO line in `tools/film-data.mjs` was read against that list; the only additions the audit made are the three new gate defaults (I, J, K) and one wording change — the lockup separator, for bidi safety.
