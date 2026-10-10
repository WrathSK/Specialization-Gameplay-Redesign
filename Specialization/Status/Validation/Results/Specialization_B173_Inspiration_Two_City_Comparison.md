# B173.200 — Revised source estimates and two-city 6% / 9% comparison

Date: 2026-10-09. User source corrections, explicit city-B clarification and one new E2 screenshot. **PARTIAL attribution; no new implementation or universal native PASS.** Earlier [initial evidence](Specialization_B173_Inspiration_Native_Feedback.md) and [E3 calculations](Specialization_B173_Inspiration_E3_Feedback.md) retain their original data and stated assumptions. This follow-up supersedes the Merchant base estimate of 6/7; it does not rewrite those historical observations.

## New facts and limits

- User now reports city A Merchant base `6 + 4 working Commercial Hub specialists × 4 = 22`, plus a player-wide Merchant +10%. These replace the earlier incomplete base estimate; the native eligibility of each component and the +10% stacking layer are not independently inventoried here.
- City A Scientist estimate remains `7 + 6`, with uncertain bonus eligibility for the separate +6.
- Another city B is Culture ACTIVE IV, has one eligible collection era, no Garden, and estimated Scientist base 3. In answer to the timing question, the user explicitly confirms **city B stayed at one era in both the 6% and 9% runs**.
- No city-B native report was submitted. Its E1 is user-confirmed; the report cannot independently establish its exact credited contribution or an unchanged source inventory beyond the user's statements.

## New screenshot

Original `Screenshot 2026-10-09 at 6.55.23 PM.png` shows B173.200, selected EDINBURGH (TEST), T71, E2 / +6%. Its nine rates repeat the earlier T71 E2 rates exactly. The Police Station is queued for one turn; that does not establish any new completed building. National API readings:

| Class | GPP/turn | Accumulated total |
|---|---:|---:|
| General | 5.039062 | 231.414062 |
| Admiral | 21.515625 | 135.890625 |
| Engineer | 36.292969 | 153.894531 |
| Merchant | 34.078125 | 307.296875 |
| Prophet | 10.078125 | 96.859375 |
| Scientist | 52.246094 | 472.640625 |
| Writer | 52.257812 | 234.242188 |
| Artist | 65.656250 | 483.562500 |
| Musician | 45.675781 | 277.472656 |

Use the rates to compare this E2 run with the previously submitted E3 run; do not compare accumulated totals across reloads/recruitment/Pass actions as if they were consecutive turns.

## Per-city scope: static confirmation

The [current model](../../../../Mod/CultureInspirationModel.lua) requires Culture Identity, Potential IV, known ACTIVE IV and a confirmed eligible current collection. It computes `3 × this city's eraCount`. [Runtime reconciliation](../../../../Mod/CultureInspiration.lua) reads `GreatWorkFacts.Summary(pid, cityID)`, creates the selected carrier on that city's own queue/buildings, and audits eligible supported-player cities. The report reads existing results; it is not an activation switch. [SQL](../../../../Mod/Data/CultureInspiration.sql) attaches the city GPP-percentage effect to each local carrier.

Therefore the implementation applies independently to **every eligible Culture IV city**, not only the selected city: city A E2/E3 gets +6%/+9%; city B E1 gets +3%. A's +9% is not intentionally broadcast to B, and B does not increase its percentage merely because A gains another era. This is STATIC_CONFIRMED implementation scope, not direct native proof of B's result.

With B's declared Scientist base 3 and no other relevant multiplier, its own E1 contribution is `3 × 1.03 = 3.09`, or an increment of +0.09 over E0. The earlier illustrative one-final-step quantization model would show 3.08984375. No Garden dilution is expected there; other unknown modifiers would still need separate treatment.

## What the 3-percentage-point difference isolates

Since B remains E1 in both runs, its contribution cancels **provided its base and other relevant state also remain unchanged**. It must not be added again to the A E2→E3 delta.

| National class | E2 / 6% in A | E3 / 9% in A | Displayed difference |
|---|---:|---:|---:|
| Scientist | 52.246094 | 52.726562 | +0.480468 |
| Merchant | 34.078125 | 34.691406 | +0.613281 |

At the observed 1/256 resolution these differences are `123/256 = 0.48046875` and `157/256 = 0.61328125`, respectively. This comparison avoids treating the stale T70 reading as a settled E0 control, but is still across separate runs and relies on the stated stable inputs.

### Merchant: corrected base 22 and player +10%

| Conditional stacking model | A at 6% | A at 9% | Expected change | Observed minus expected |
|---|---:|---:|---:|---:|
| Garden20 + player10 + Inspiration share one additive pool | `22 × 1.36 = 29.92` | `22 × 1.39 = 30.58` | +0.66 | -0.04671875 |
| Garden + Inspiration add locally; player10 multiplies that result | `22 × 1.26 × 1.10 = 30.492` | `22 × 1.29 × 1.10 = 31.218` | +0.726 | -0.11271875 |

The revised base makes the prediction substantially closer than the old base-6 prediction (+0.18 across three percentage points), but **neither simple model exactly fits**. The name “player +10%” alone does not choose a stacking model. A stable player bonus cannot simply be appended to the observed delta without establishing its scope/aggregation layer.

The residuals are approximately 12 or 29 increments of 1/256, not a last displayed decimal. They are not explained by the earlier single-final-quantization illustration. This does not rule out more complex per-source rounding or establish a bug; source coverage, actual stacking and other contribution changes remain unresolved. Do not invent a new eligible base merely to force a fit.

### Scientist: city B does not account for the residual

If A's eligible base is 13 and Inspiration shares the Garden pool, E2→E3 predicts `13 × 0.03 = 0.39`; eligibility of the separate +6 for Garden does not change that increment. If only base 7 receives Inspiration, the prediction is +0.21. Observed +0.48046875 differs from those by +0.09046875 or +0.27046875.

The +0.09046875 residual is numerically close to B's +0.09, but **B is already E1 in both runs**. Counting its unchanged bonus again would be double-counting. Likewise, `(13 + 3) × 0.03 = 0.48` is not a valid explanation unless B's bonus or another relevant contribution actually changed, contrary to the era-count control. The data does not prove a player-wide leak either: city bases, other modifiers and runtime source state are not fully isolated.

Dividing the observed delta by 0.03 gives an *apparent response coefficient* about 16.016, not a demonstrated actual Scientist base of 16. It neither proves nor disproves the separate +6's eligibility by itself. Do not overwrite the user's base estimate with a fitted value or subtract a guessed historical +1.

## Conclusion and boundary

- Confirmed in the new image: the E2 report and all nine rates repeat the prior E2 observation.
- Confirmed statically: independent city-local eligibility and percent projection for all supported Culture IV cities; report selection is not required to activate the ability.
- Native numerical support from General/Prophet and fractional accumulated readings remains valid within its earlier scope.
- Revised Merchant sources reduce the unexplained gap, but exact Merchant/Scientist attribution remains open. City B's unchanged E1 cannot close that differential gap.
- No Design, gameplay, tests, GC, runtime, deployment, main or original evidence changes. No new diagnostic, save/load ritual or larger investigation is started. This record does not declare B173 complete or authorize another batch.

## Original archive

The reviewed original was moved unchanged from ignored `ScreenShots/` to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B173/2026-10-09/`. Earlier originals remain unchanged. SHA256 verified before/after; no image committed.

| Original filename | SHA256 |
|---|---|
| `Screenshot 2026-10-09 at 6.55.23 PM.png` | `f6a2fdbb9eaa396c3daefb552440c0a43b7e83929f622360af73c3e6aebbc5f2` |
