# B183 Spy0 native review — timer accepted, exact arrival failed

Date: 2026-10-10. Package **B183.210 / modinfo210**, implementation `219c4e7030f3427ec484c4716da3dc90deca9515`. **N1 partial: exact arrival FAIL; harmless coexistence not established.** This review records five screenshots and the user's own-city overlap observation. It authorizes no Spy1 prototype, Design change, formal N1 or N2/N3 work.

## Native observations

All five originals were visually reviewed in order. The selected foreign target is Sparta / 斯巴达.

| Image | Observation | Evidence boundary |
|---|---|---|
| 1, 11:18:38, T84 | Own unit3145757 at(62,33), source Edinburgh (Test), city393220; count1/1; Spy maximum5→5; other units on tile0 | Creation/source/count readback, not an overlap test |
| 2, 11:18:47, T84 | Travel2 + establishment0 =2; native Spy operation eligibility rejected without a reason | Duration getter works for this fixture; does not prove native Spy-operation eligibility or execution |
| 3, 11:18:54, T84 | Independent dispatch accepted; travelling; dueT86, remaining2 | **USER_GAME_TEST_PASS for accepting/scheduling this dispatch.** The old pre-timer API failure was passed |
| 4–5, 11:21:35/38, T86 | `EXACT_PLACEMENT_REJECTED`, failed stage“到达位置与其它单位核对”; same own unit3145757 now at(25,11); count1/1, Spy maximum5→5, other units0; HELD, source shown as recorded | **USER_GAME_TEST_FAIL for exact arrival.** The unit moved, but the exact-target assertion failed; selected destination coordinates are not shown, so “adjacent tile” is not established |

Separately, the user reports that the prototype cannot overlap other units even in an own city. Record **USER_REPORTED_FAIL for that tested own-city overlap**, not a screenshot-proven matrix of military/civilian/foreign/war combinations. The screenshots show zero other units on the current tile. Harmless foreign/hostile coexistence, END and cold-load behavior are **NOT_TESTED** in this submission. Do not request a repeat of this failed route merely to complete the old checklist.

## What the failure establishes

[ExpeditionGate.lua](../../../../Mod/ExpeditionGate.lua) `arrive` first validates the target, invokes `PlaceUnit`, then reads the exact owned unit and asserts its coordinates equal the target (line118 in this implementation). The report's stage/detail identifies this assertion. Subsequent source/occupant checks are after that assertion: **a displayed recorded source is retained session evidence, not a newly validated post-arrival binding**. No claim is made that the target's other occupants were independently verified unchanged after the failure.

The context fix therefore reached a different boundary: native placement rather than the old Gameplay/UI capital getter mismatch. Keeping the failed state HELD and exposing the error is correct diagnostic behavior; it is not successful travel. No retry, automatic nearby-tile acceptance, guessed identity or resurrection was added.

The current configured read-only Gameplay database confirms the exact prototype has **Spy0, Stackable1, IgnoreMoves1**, civilian formation, no Spy promotion class and retreat0. These flags did not suffice for the requested placement/coexistence in this fixture. This does not prove every possible non-Spy implementation impossible, identify the entire engine collision rule, or prove Spy1 works.

Capacity remains1/1 and the same native unit ID is visible. Spy maximum5→5 is only the maximum, not native used slots or ordinary-Spy trainability. No formal persisted journey or save-schema result is involved; the gate is session-only.

## Follow-up investigation and stop

The [existing movement/coexistence report](../../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md#b183-native-failure-and-spy1-isolation-reassessment) records the bounded installed-code/DB/API review answering the user's questions. `Spy`, `Stackable`, `IgnoreMoves`, TypeTags and PromotionClass are separate surfaces; native Spy travel/collision is not exposed as detachable Lua modules. The known diplomacy chain is detection-gated. Displayed mission success includes detected success, so increasing success odds is not an immunity guarantee.

**Recommended candidate, not implemented:** custom Spy1 shell/native travel plus our own deterministic Expedition tasks, capacity and archive binding. Do not repurpose Gain Sources/Listening Post as neutral timers, alter global diplomatic penalties, remove HD listeners or infer immunity from UI filtering. The candidate must first establish native used-slot isolation, eligible ally/war destinations, custom type/reference continuity, harmless coexistence and absence of unintended native/HD task hooks. Native target restrictions may require adapted UI even if its visual components are reused. Formal mission-specific district/Wonder positioning remains a separate unresolved requirement.

**Current stop:** no new code, deployment or user test. Await a concrete next-route decision; no automatic Spy1 switch. Earlier B180 retreat, B182 pre-timer failure and B183 local repair evidence remain unchanged and scoped.

The user's follow-up about **获取情报源 / Gain Sources** is addressed in the same technical report. Native text explicitly promises automatic completion and no risk to the Spy; this is stronger evidence than merely boosting risky-mission odds. Its intelligence-source state and HD completion effects are not a neutral task framework. Whether those effects can be isolated for a custom unit while retaining the native safe task remains UNKNOWN; no new experiment is performed here.

## Source and archive integrity

Current configured read-only `DebugGameplay.sqlite` SHA256: `9046f2543ae731f5bc043a0f631227ddcedb018030e5fb8c94c201e13f10c72e`. This identifies the queried configuration, not a native API implementation. Installed source references and public API limitations are in the linked technical report; local-only Investigation originals were consulted read-only and are not published by this batch.

Originals moved without renaming or overwriting to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B183/2026-10-10/`; local manifest records size/hash. All five pre/post hashes match. Images are not committed. No source/gameplay tests were rerun for this evidence-only review; prior81 local methods remain inherited local evidence, not native PASS.

| Original filename | SHA256 |
|---|---|
| Screenshot 2026-10-10 at 11.18.38 AM.png | `7868701d964153eea6eea97dd8f528a3f04937301e40e7c32aa5d48cff89b8cc` |
| Screenshot 2026-10-10 at 11.18.47 AM.png | `e4ea2f78e0f9e74ea5fbd3c3fbbe24469e90d1f02ffc8f49383c4243bdc7c6bf` |
| Screenshot 2026-10-10 at 11.18.54 AM.png | `9f846ea8fd25f8ebe17983a3fb049b5553959459d425ac82cce4781e6abf2dca` |
| Screenshot 2026-10-10 at 11.21.35 AM.png | `ea410ec32e3b90db40cfd5894c43d6a9f86eadb207b69e74b76d32fa7a358a5c` |
| Screenshot 2026-10-10 at 11.21.38 AM.png | `af58c018b39ff82183cc8e56128cc52568120e5a1497f1751dab272a6e657159` |
