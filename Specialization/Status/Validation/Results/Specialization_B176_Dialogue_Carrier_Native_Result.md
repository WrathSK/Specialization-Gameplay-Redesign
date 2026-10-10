# B176.203 — Dialogue carrier comparison: native display result

Date: 2026-10-09. Ten original screenshots reviewed. Package **B176.203 / modinfo203**, recorded source `f139bc2fb22a3eda4563945f3b002c11915d3086`, deployment receipt `B176.203-f139bc2-playtest.json`. Deployment provenance is inherited from the existing record; no new runtime comparison, deployment or game launch was performed for this review.

**USER_GAME_TEST_PASS for the observed Great Works display response and bounded replacement/END behavior.** The five current Meaning additions remain unchanged. **Actual turn settlement and full native-only yield integration remain UNRESOLVED**, because the city Culture reader does not follow the work-display change. This is a partial technical result, not full P0-M acceptance. The frozen [local result/test contract](Specialization_B176_Dialogue_Carrier_Local.md) and [B175 project/history result](Specialization_B175_Dialogue_B174_Native_Result.md) remain unchanged.

## Measured sequence

All images show turn76. The fixture is Culture ACTIVE IV **EDINBURGH (TEST)**, with two Writing works in **古罗马剧场**: **《天问》** / Classical and **《月下独酌》** / Medieval. Reports identify two works/two eligible works and zero themed or unknown-theme buildings. The following are the **combined yields of those two works**, not each work's yield.

| Stage | Images | Works Culture | Works Tourism | Meaning-visible Food / Production / Gold / Science / Faith | City Culture reader |
|---|---|---:|---:|---|---:|
| 0% test baseline | 3–4 | 9 | 15 | 6 / 10 / 18 / 6 / 6 | 76.1992 |
| +100% | 5–6 | 18 | 20 | 6 / 10 / 18 / 6 / 6 | 74.1992 |
| +200% | 7–8 | 27 | 25 | 6 / 10 / 18 / 6 / 6 | 74.1992 |
| END; normal old +25% | 9–10 | 11 | 15 | 6 / 10 / 18 / 6 / 6 | 74.1992 |

The P0 native readout and the Great Works interface agree on the work Culture/Tourism values. The latter's national totals are respectively Culture19/28/37/21 and Tourism30/35/40/30; the visible other-city work rows are unchanged. This supports target-local display behavior, not a census of all cities or credited nationwide income.

Images1–2 show the pre-test building tooltips: 古罗马剧场 adds **+2 Culture and +50% Tourism per Writing work**; 陈列室 includes **+50% Tourism for city Great Works**. Pre-test city Culture displays +74.1, matching the displayed +74.1 after END. There is no pre-test Great Works screenshot, so exact pre-test/post-END work-yield equality is not directly photographed.

## Interpretation and boundaries

1. **Percentage response/replacement:** relative to0%, Culture increases by9 then18; Tourism by5 then10. +200% behaves as a replacement, not accumulated +100% plus +200%, in these readings. This verifies the tested native display response beyond merely finding an attached carrier.
2. **Meaning is not amplified in this fixture:** Food6, Production10, Gold18, Science6 and Faith6 remain constant at every stage, including END. The current [Meaning model](../../../../Mod/CultureMeaningModel.lua) projects these five yields; Culture is still quarantined. The test only applies Culture/Tourism percentages. Therefore it does **not** establish isolation if a future percentage targets the same yield as a Meaning addition, nor restore the deferred Meaning Culture path. Meaning has no Tourism output.
3. **Culture is not limited to the work's database base:** the two works have2+3=5 intrinsic Culture; the Amphitheater adds2+2=4. Observed Culture is `(5+4) × 1/2/3 = 9/18/27`. Thus the HD building's flat Culture is amplified too. A base-only calculation leaving that+4 independent would instead give9/14/19. Do not label this primitive universally native-base-only. The accepted [Culture contract](../../../Design/Content/Culture_D0049.json) explicitly protects Meaning additions; this observation does not authorize editing HD or invent a new rule about other building additions. Clarify the intended treatment if a later implementation depends on that distinction.
4. **Tourism is consistent with an additive percentage contribution:** intrinsic Tourism totals5; the observed15/20/25 equals the existing displayed baseline15 plus0/5/10. It does not mean +100% doubles the already-buffed15. Images1–2 establish two+50% sources; the remaining baseline multiplier is consistent with the user's previously identified Printing environment but is not independently inventoried here. No universal stacking/order conclusion is made.
5. **END restores ordinary AUTO, not the artificial0% state:** image10 reports no active fixture and normal old+25%, matching [DialogueModel](../../../../Mod/DialogueModel.lua)'s `25 × (2 eras − 1)`. The high test yields cease and the five Meaning additions remain. Work yields11/15 and the pre/post displayed city74.1 support ordinary restoration; no direct native instance enumeration was submitted, so do not claim an independent instance-count proof. The saved project history stays+5% with Medieval used. That earned+5% is still not integrated into yields. Exact fractional rounding/order at ordinary+25% is not derived from this sample.
6. **Settlement is not demonstrated:** [the reader](../../../../Mod/UI/BoostGreatWorkRead.lua) uses `GetBuildingYieldFromGreatWorks` / `GetBuildingTourismFromGreatWorks` for work totals and `city:GetYield` for city Culture. They are different engine readings. City Culture is76.1992 at0% and74.1992 at both high settings and END; top-bar Culture stays164.8. All images are within T76. Neither cache delay nor lost actual income is established. Preserve the discrepancy rather than treating the work display as credited Culture/Tourism or declaring a runtime failure.

## Static corroboration

Only the configured read-only `debug_gameplay_db` was queried, via existing local configuration. Snapshot SHA256: `9bed04e6a9ea0cb695f273e8770e169097f85f00148d830d20722a75412ced8e`. Qu Yuan Writing rows have Culture2/Tourism2; Li Bai rows have Culture3/Tourism3, with Classical/Medieval eras. `HD_AMPHITHEATER_WRITING_CULTURE_BOOST` has `YieldChange=2`; its Writing Tourism modifier and the Cabinet Writing Tourism modifier each have `ScalingFactor=150`. B176 Writing Culture test modifiers have factors200/300. These definitions corroborate the displayed arithmetic; they are not a live inventory of every active player effect or turn settlement. No DB or other Mod was modified.

## Next boundary

The requested0/100/200/END comparison has been reviewed and need not be repeated as a shared lifecycle ritual. M1 project/history and B174 acceptance remain intact. This evidence supports the tested Culture/Tourism **display** primitive and unchanged five-yield Meaning output, not a full cumulative writer, all supported work/yield categories, theming combinations or retirement of old Dialogue.

Before treating this path as actual income, the specific missing distinction is **stale same-turn display versus credited yield**. A later minimal check should compare credited turn Culture (and the corresponding Tourism settlement if claimed) with unchanged inputs at0% versus one high setting. Use a reproducible turn boundary and account for normal production/population changes; no need to earn high history, repeat200%, or re-test saved Probe state/END/re-enable. This is a proposed narrow follow-up, not a new implementation or automatically dispatched broad test. No code, Design, GC, main or runtime change in this checkpoint.

## Original evidence archive

All ten original PNGs were visually read, then moved without renaming/re-encoding from ignored `ScreenShots/` to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B176/2026-10-09/`. **10/10 SHA256 equality verified**, 115,936,053 original bytes. No image is committed. This table is the evidence manifest associated with the P0-M2 native result.

| Image | Original filename | SHA256 |
|---|---|---|
| 1 | `Screenshot 2026-10-09 at 9.35.29 PM.png` | `fbc9a40afc715087507a220c813d895a805d670f19e9376130ecf61ec1015abb` |
| 2 | `Screenshot 2026-10-09 at 9.35.31 PM.png` | `18d1f5b6796b6bb492b40c46c7beeba64017c284a053363dd2aebfc7e53ba970` |
| 3 | `Screenshot 2026-10-09 at 9.38.32 PM.png` | `9e2be4ef572fa1ab703ae779c0450f25394a3f0c1c09cd96761f95dd0c2ef489` |
| 4 | `Screenshot 2026-10-09 at 9.38.36 PM.png` | `b6dc115949f50db2b209ceadaf3ddc96090b61ccfff01c20601efcd25208ff4a` |
| 5 | `Screenshot 2026-10-09 at 9.38.42 PM.png` | `194825a695c6426aae801ea31eb709f51bf881f03e8db8d8d09ff15ffd097d13` |
| 6 | `Screenshot 2026-10-09 at 9.38.47 PM.png` | `c5cbac7cf6306eb4d7679b83e94c3acb088b3468c259640e7ec554f66c2a45b0` |
| 7 | `Screenshot 2026-10-09 at 9.38.54 PM.png` | `c4243d165f198b824091b19949d3326bbfb5a3144c7ab3f694c8fd33d0a5d98b` |
| 8 | `Screenshot 2026-10-09 at 9.38.58 PM.png` | `9a35558678b7157dcdccac2e7d724eead72c1f1498c4d270d9b0b511e108fcea` |
| 9 | `Screenshot 2026-10-09 at 9.39.09 PM.png` | `984920510daaa1ce6b4d5b14a892c325a8f71fd8c70a62d56ff6c6fd10312eae` |
| 10 | `Screenshot 2026-10-09 at 9.39.35 PM.png` | `4f21f11ba6f382c7ba2918cc573d8fd1c97ca575bfc379f6be20cfe4fb0f64af` |
