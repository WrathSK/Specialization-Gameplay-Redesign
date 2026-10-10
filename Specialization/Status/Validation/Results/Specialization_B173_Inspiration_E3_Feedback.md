# B173.200 — E3 / +9% native feedback and numerical interpretation

Date: 2026-10-09. Three submitted originals visually reviewed. This supplements the [initial E0/E2/E0 feedback](Specialization_B173_Inspiration_Native_Feedback.md) without replacing its raw observations. **Scoped native support for a fractional percentage response; exact Scientist/Merchant attribution and combined B173 acceptance remain PARTIAL.** No implementation defect, universal rounding rule or full native PASS is declared.

## Observed sequence and user-reported controls

Selected city: EDINBURGH (TEST). The user recruited three additional Great Writers and obtained a work from a third era, producing E3 / +9%. They report changing production queues so no building completes during this turn. They estimate this city's Scientist base as `7 + 6` and Merchant base as `6`; the separate Scientist +6 source's eligibility for Garden and Inspiration is explicitly uncertain. These are source estimates, not a verified city GPP inventory.

| Image | Filename time | Turn | Visible evidence |
|---|---|---:|---|
| 1 | 18:40:14 | 70 | Left-click 巨作启迪报告 shows E3 / +9%, but all national rates still equal the earlier T70 readings; Writer accumulated points now 0.984375 after recruitment |
| 2 | 18:41:26 | 71 | Native Great People screen shows updated one-decimal rates; hovering 放弃 explicitly shows a 48-point Merchant rejection cost |
| 3 | 18:41:38 | 71 | Left-click 巨作启迪报告 still E3 / +9%; updated six-decimal rates and accumulated totals |

Image 1 is already configured E3, not a newly settled E0 control. Its rates matching the earlier baseline is consistent with the known refresh delay. No new post-refresh E0 sample of this revised setup is included. No right-click native-instance inventory was submitted. The non-completion control removes the earlier observed building-completion confound from the user's reported procedure; it does not independently establish every national source or timing contribution.

## National rate readings

These are player-wide API readings, not selected-city base GPP. Image 2 corroborates their rounded UI presentation; calculations use images 1 and 3.

| Class | T70, E3 configured / prior rates | T71, E3 refreshed | Observed change |
|---|---:|---:|---:|
| General | 4.796875 | 5.156250 | +0.359375 |
| Admiral | 18.796875 | 21.632812 | +2.835937 |
| Engineer | 35.339844 | 36.652344 | +1.312500 |
| Merchant | 31.656250 | 34.691406 | +3.035156 |
| Prophet | 9.597656 | 10.316406 | +0.718750 |
| Scientist | 51.199219 | 52.726562 | +1.527343 |
| Writer | 50.398438 | 52.917969 | +2.519531 |
| Artist | 63.218750 | 75.207031 | +11.988281 |
| Musician | 44.000000 | 46.273438 | +2.273438 |

## Accumulated-point readings

| Class | T70 | T71 | Change minus T71 rate |
|---|---:|---:|---:|
| General | 226.375000 | 231.531250 | +0.000000 |
| Admiral | 114.375000 | 136.007812 | +0.000000 |
| Engineer | 117.601562 | 154.253906 | +0.000000 |
| Merchant | 273.218750 | 259.910156 | -48.000000 |
| Prophet | 86.781250 | 97.097656 | +0.000000 |
| Scientist | 420.394531 | 473.121094 | +0.000001 |
| Writer | 0.984375 | 53.902344 | +0.000000 |
| Artist | 417.906250 | 493.113281 | +0.000000 |
| Musician | 231.796875 | 278.070312 | -0.000001 |

Eight classes' increments match the refreshed T71 rate within 0.000001 display precision. Merchant reconciles as `273.218750 + 34.691406 - 48 = 259.910156`, consistent with the 48-point Pass cost now visible in image 2. Hovering alone does not show the click; the matching residual supports that explanation but is not a separate recording of the action. Passing concerns accumulated points, not the per-turn bonus calculation. Writer recruitment happened before image 1; do not compare its new accumulated baseline with the previous session as an unexplained loss.

## What +20% Garden and +9% Inspiration predict

**Conditional common additive pool:** `1.20 × B → 1.29 × B`. Inspiration adds `0.09 × B`, which is `1.29 / 1.20 - 1 = 7.5%` of the already Garden-boosted component. This is relative dilution, not a reduction of the configured nine percentage points. Other cities in the national total dilute the observed national percentage further.

| Assumed source eligibility | City contribution before | City contribution with E3 | Expected increment |
|---|---:|---:|---:|
| Scientist: 7 receives both; separate +6 receives neither | 14.40 | 15.03 | +0.63 |
| Scientist: Garden applies only to 7; Inspiration applies to all 13 | 14.40 | 15.57 | +1.17 |
| Scientist: all 13 receive both percentages | 15.60 | 16.77 | +1.17 |
| Merchant: base 6 receives both | 7.20 | 7.74 | +0.54 |

The user's distinction matters: exclusion of the separate +6 from Garden would not, by itself, prove exclusion from Inspiration. Its hypothetical additional Inspiration contribution is `6 × 0.09 = 0.54`. Native coverage remains unverified.

Actual national changes are Scientist **+1.527343**, Merchant **+3.035156**. They do not equal the stated-base additive predictions. Even a simple separate multiplicative pool gives at most +1.404 for Scientist under these three source assumptions, and +0.648 for Merchant; neither explains the observed changes. This is not a proof of incorrect code: source estimates, unaccounted effects/contributions or refresh-state differences remain unresolved. Do not subtract a guessed historical +1 or treat a per-turn difference as a Pass deduction.

## Strongest numerical support and precision boundary

The cleaner General and Prophet rate sequences, combining the earlier E0/E2 observation with this E3 submission, are:

| Class | Earlier E0 | Earlier E2 / +6% | New E3 / +9% | E0→E3 relative increase |
|---|---:|---:|---:|---:|
| General | 4.796875 | 5.039062 | 5.156250 | about 7.492% |
| Prophet | 9.597656 | 10.078125 | 10.316406 | about 7.489% |

These fit the additive Garden model with inferred eligible bases 4 and 8 and the illustrative quantization function `Q(x) = floor(256 × x) / 256`:

- General: `Q(4 × 1.20) = 4.796875`; `Q(4 × 1.26) = 5.0390625`; `Q(4 × 1.29) = 5.156250`.
- Prophet: `Q(8 × 1.20) = 9.59765625`; `Q(8 × 1.26) = 10.078125`; `Q(8 × 1.29) = 10.31640625`.

The ideal E3 increments +0.36 and +0.72 become the observed +0.359375 and +0.718750. Their stock increases also match their fractional T71 rates. This is meaningful native evidence for percentage-generated fractional GPP, not merely a configured carrier. The bases are inferred for this fit, not independently inventoried; the cross-run comparison does not prove every class or source uses the same pool.

All 36 displayed rate/total readings in this submission lie within 0.0000005 of a multiple of `1/256 = 0.00390625`, matching six-decimal display precision. The current [readout](../../../../Mod/InspirationReadout.lua) directly reads `GetPointsPerTurn` / `GetPointsTotal` and formats six decimals; it does not floor the gameplay GPP value. [Current SQL](../../../../Mod/Data/CultureInspiration.sql) supplies Amount 9 via the same city-percentage family documented for Garden/Pingala in the [B172 static result](Specialization_B172_Inspiration_Automatic_Local.md#结果与范围).

Thus 1/256 quantization is strongly supported for these returned values, and downward quantization exactly fits the two cleaner examples. This does **not** establish the native engine's internal rounding stage, per-source aggregation order, every class's universal formula, or the retired fractional-base primitive's correctness. A single final quantization error is below 0.00390625; it cannot account for the much larger Scientist/Merchant discrepancy under the stated-source model.

## Remaining boundary and next action

E3 updates, fractional accumulation and the +9-percentage-point interpretation have scoped native support. Exact Scientist/Merchant source attribution, all-class coverage and the joint Aesthetic/Meaning acceptance remain open. Do not turn that into a fresh empire-wide source census or new diagnostic implementation. No extra save/load test is requested.

If the user wants to isolate the remaining rate difference, the discriminating comparison is a refreshed E0 versus E3 using the same post-recruitment setup and unchanged GPP sources, rather than treating image 1's stale rate as a separately settled E0 sample. This is the existing acceptance comparison, not a mandatory new batch or permission to modify gameplay. Stop after recording and calculation.

## Original evidence archive

Originals moved byte-for-byte from the ignored `ScreenShots/` inbox to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B173/2026-10-09/`. The inbox directory and earlier four originals remain intact. Filenames retained; 3/3 SHA256 equality verified; no images committed.

| Image | Original filename | SHA256 |
|---|---|---|
| 1 | `Screenshot 2026-10-09 at 6.40.14 PM.png` | `c9c84269cb3d57b0d65565a117d1882431f79a332bfacb0f3b549264dd6f8600` |
| 2 | `Screenshot 2026-10-09 at 6.41.26 PM.png` | `0c858a6688b31e371720009831b961b6e7dedaca2074b59a6395e41e30298a96` |
| 3 | `Screenshot 2026-10-09 at 6.41.38 PM.png` | `b029a641e2e807c4faa68e1396a6278585f3469becf9670bb0d572ea04ca4c82` |
