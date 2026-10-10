# B173.200 — Initial Inspiration native feedback

Date: 2026-10-09. Evidence: four user screenshots, each visibly reporting B173.200, plus the user's source estimates and follow-up recollection. **PARTIAL observation; combined native acceptance remains USER_GAME_TEST_REQUIRED.** No full PASS or confirmed implementation failure is inferred from this comparison.

The [B173 local result and combined test](Specialization_B173_Great_Work_Notifications_Local.md#与巨作启迪一次验收) and [B172 percentage contract](../../../Architecture/v2/P0_L3_Inspiration.md#当前切片与停止点) remain unchanged. This records submitted evidence; it authorizes no repair, deployment or next ability. The previously deferred user test has resumed with this submission.

## Sequence actually visible

Selected city: EDINBURGH (TEST). Every image is the left-click “巨作启迪报告” summary; no right-click native-instance inventory was submitted.

| Image | Local filename time | Turn | Reported current eras E | Configured Inspiration | Observation |
|---|---|---:|---:|---:|---|
| 1 | 18:20:31 | 70 | 0 | +0% | Initial national rates/totals; Cinema under construction, displayed 2 turns |
| 2 | 18:21:20 | 70 | 2 | +6% | Era/configuration updated; all nine national rates/totals still exactly match image 1; Cinema now displays 1 turn |
| 3 | 18:22:04 | 71 | 2 | +6% | National rates/totals refreshed; city no longer producing anything, consistent with Cinema completion |
| 4 | 18:23:54 | 72 | 0 | +0% | Era/configuration returned to zero; national rates changed; Police Station now queued |

The user confirms that the works were moved to a city that is **not Culture-specialized**, that they did **not** recruit/patronize a Great Merchant, and that no Scientist-GPP-related change is known. Their reminder of an unexplained +1 in earlier saves is preserved as prior uncertainty, not subtracted as a correction from the present figures.

The user estimates this city's Scientist base as `7 + 6`, with a suspicion that the +6 component might not receive percentage bonuses, and Merchant base as approximately 7 (explicitly uncertain). They report Garden +20%. These are user estimates, not a verified city-source inventory or proof of modifier stacking. The [earlier source discussion](Specialization_B168_B169_Native_Feedback.md#用户的516估算) also left the exact source coverage unresolved.

## Displayed native national rates

These are national `GPP/turn` readings, not this city's base production. Image 2 duplicates image 1 for every row.

| Class | T70, E0 / same-turn E2 | T71, E2 | T72, E0 | T71 minus T70 |
|---|---:|---:|---:|---:|
| General | 4.796875 | 5.039062 | 4.796875 | +0.242187 |
| Admiral | 18.796875 | 21.515625 | 21.273438 | +2.718750 |
| Engineer | 35.339844 | 36.292969 | 35.570312 | +0.953125 |
| Merchant | 31.656250 | 34.078125 | 30.457031 | +2.421875 |
| Prophet | 9.597656 | 10.078125 | 9.597656 | +0.480469 |
| Scientist | 51.199219 | 52.246094 | 51.289062 | +1.046875 |
| Writer | 50.398438 | 52.257812 | 58.136719 | +1.859374 |
| Artist | 63.218750 | 65.656250 | 71.714844 | +2.437500 |
| Musician | 44.000000 | 45.675781 | 49.273438 | +1.675781 |

## Displayed native national totals

| Class | T70, images 1 / 2 | T71, image 3 | T72, image 4 |
|---|---:|---:|---:|
| General | 226.375000 | 231.414062 | 236.210938 |
| Admiral | 114.375000 | 135.890625 | 157.164062 |
| Engineer | 117.601562 | 153.894531 | 189.464844 |
| Merchant | 273.218750 | 307.296875 | 289.753906 |
| Prophet | 86.781250 | 96.859375 | 106.457031 |
| Scientist | 420.394531 | 472.640625 | 523.929688 |
| Writer | 181.984375 | 234.242188 | 292.378906 |
| Artist | 417.906250 | 483.562500 | 555.277344 |
| Musician | 231.796875 | 277.472656 | 326.746094 |

All nine T70→T71 total increments equal the T71 displayed rate to within 0.000001, the precision of the displayed values. T71→T72 behaves the same for eight classes. This shows actual changes in accumulated totals in the submitted session; it does **not** isolate how much of each increment came from Inspiration.

Merchant is different: `289.753906 - 307.296875 = -17.542969`, whereas the displayed rate is `+30.457031`. The residual is **-48.000000**. The user explicitly denies recruitment/patronage; its cause remains **UNKNOWN**. Do not relabel it as a recruitment event, a negative Inspiration reward or a carrier defect without evidence.

## Interpreting the Garden and the user's estimate

The current implementation uses the same city-percentage modifier family as the recorded Garden/Pingala definitions; the [B172 static review](Specialization_B172_Inspiration_Automatic_Local.md#结果与范围) is not proof of the active stacking pool or eligible source set in this save. No HD source or external database was changed or reinvestigated in this feedback pass.

**Conditional additive model only:** if Garden +20% and Inspiration +6% apply additively to the same eligible base `B`, the rate changes from `1.20B` to `1.26B`. The new increment is `0.06B`; relative to the already boosted component that is `1.26 / 1.20 - 1 = 5%`. The +6 percentage points are not reduced to +5 percentage points. Nor should 6% be applied to the entire national rate.

| Assumed city source treatment | Before Inspiration | With E2 / +6% | Conditional increment |
|---|---:|---:|---:|
| Scientist: only base 7 eligible; separate +6 unaffected by both percentages | 14.40 | 14.82 | +0.42 |
| Scientist: all 13 eligible for both percentages | 15.60 | 16.38 | +0.78 |
| Merchant: base 7 eligible | 8.40 | 8.82 | +0.42 |

Thus the user's “dilution” intuition is reasonable for the **relative increase over an already boosted total**, conditional on additive stacking. It does not establish whether the separate +6 Scientist source is eligible. These ideal arithmetic examples are not promised exact engine rounding/settlement values.

The observed national increases are Scientist **+1.046875** and Merchant **+2.421875**, which do not match those simple source estimates. Cinema completion makes the overall comparison non-identical, but does not by itself explain a Scientist or Merchant change. The user reports no known Scientist change; that distinction is retained.

General `4.796875 → 5.039062 → 4.796875` and Prophet `9.597656 → 10.078125 → 9.597656` show a reversible response consistent with a roughly 5% relative increase on a Garden-boosted component. This supports a functioning percentage path in the observed session, but national totals and unverified city bases do not independently prove source scope, exact stacking or every class's bonus.

## Evidence scope and next boundary

Observed: E0→E2→E0 report/configuration updates; unchanged same-turn national readings followed by next-turn refresh; accumulated totals matching the new-turn rate in the comparisons described above. These are stronger than configuration-only evidence, but are not a complete attribution of the bonus.

Still unresolved: exact city base/source eligibility and stacking; the Merchant -48 residual; native-instance withdrawal; a positive-era→different-positive-era replacement; and separately identifiable Aesthetic/Meaning correctness during the work moves. Overall city yields change in the background, but no module-specific reports were submitted, so that is not promoted to a joint three-consumer PASS. No cold-load or re-enable ritual is added.

No repeat test or new diagnostic implementation is mandated here. The remaining numerical question is whether a stable, known city source receives the configured percentage and returns to its corresponding baseline. Use the existing bounded combined test and already-observed stable classes where possible; do not expand this into an empire-wide GPP census or reopen the retired fractional-base probe. Further interpretation should preserve the user's recollection and any subsequent evidence rather than force an unexplained baseline to fit a formula.

## Original evidence archive

All four originals were inspected and moved, keeping names and bytes, to ignored local directory `local/legacy-workspace/Specialization/Status/Validation/Evidence/B173/2026-10-09/`. SHA256 was checked before and after each move; **4/4 match**. Images remain outside Git. This table records provenance; the directory is not a public evidence link.

| Image | Original filename | SHA256 |
|---|---|---|
| 1 | `Screenshot 2026-10-09 at 6.20.31 PM.png` | `1d754fb47c8d152153276578510f96f8529528bf59f928f7c6f913ed8fb950dd` |
| 2 | `Screenshot 2026-10-09 at 6.21.20 PM.png` | `8ee72f5f36c864a3793f27c04bf4bb23875039547536a850d478cc1c065f1d52` |
| 3 | `Screenshot 2026-10-09 at 6.22.04 PM.png` | `eac33ae6edcd7bfc785e4d0cb993365ec312587a4b1db5562a11b7c31db334d0` |
| 4 | `Screenshot 2026-10-09 at 6.23.54 PM.png` | `d5bb1c5d2551e977fbae0152f5d44741a4753b6e4af0a14ddac5ebb7efd6012f` |
