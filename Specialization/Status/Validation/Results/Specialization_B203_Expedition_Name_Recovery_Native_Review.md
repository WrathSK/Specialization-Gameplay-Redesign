# B203.230 — trained-team confirmation still blocked

2026-10-11. **USER_REPORTED_FAIL; investigation only.** The user reports that the normally trained team still cannot dispatch after B203. The tooltip was approximately “please wait for identity confirmation”; waiting did not resolve it. The user did **not** open P0 in this B203 run. Do not carry the B202 panel-assisted recovery forward as a B203 observation. No new screenshot was available to inspect in this review.

The [B203 local result](Specialization_B203_Expedition_Name_Recovery_Local.md) and [B202 native evidence](Specialization_B202_Expedition_Training_Native_Review.md) remain unchanged. This report supersedes their pending next-step wording for the current investigation, not their original observations. Runtime remains B203.230; no patch or deployment is part of this review.

## What the code actually does

[Training](../../../../Mod/ExpeditionTraining.lua) already uses `UnitAddedToMap` and `CityProductionCompleted`, not an elapsed-time guess, to establish completion. The saved queue reservation, matching source-city/type completion and exact new unit receipt are reconciled at publication. [Gate.Training.Finish](../../../../Mod/ExpeditionSpyGate.lua) then saves the source, exact unit ID and team key in `NAMING`. The existing source binding and capacity reservation are not created by opening a report.

The remaining transition is:

`confirmed source/unit → NAMING → UI native-name/collision read → Gameplay NAME validation → CREATED → dispatch enabled`

The name establishes continuity across native Spy travel's observed unit-ID replacement. Gameplay remains the only binding writer; the UI supplies the current native name and off-map collision evidence. An event reporting unit birth does not by itself prove that all those UI facts are already readable. However, there is no gameplay requirement to wait before trying to read them.

P0 has two different paths:

- Explicit **创建验证团** invokes the legacy prototype CREATE path: reserve source/capacity, call `UnitManager.InitUnit`, then confirm the returned unit's native name. It is separate from normal city training.
- In **B202**, merely opening P0 sent READ; its NAMING reply automatically entered `prepareName`, which attempted the native read immediately and sent NAME when ready. It did not produce another unit.
- In **B203**, trained READ replies carry `trainingToken` and explicitly skip that diagnostic naming writer. The legacy CREATE path remains. Opening P0 is therefore not the designed B203 recovery route; whether it has any incidental effect in the failed session is unobserved.

## Confirmed implementation difference and local counterexample

| Path | First readiness attempt | If data is pending |
|---|---|---|
| Earlier working P0 `prepareName` | Calls `checkName()` immediately | A bounded update callback follows |
| Existing independent activity bridge | Event pump calls `evaluate()` directly | A bounded update callback follows |
| B203 independent training-name observer | Event `pulse()` publishes PENDING and installs `SetUpdate`; it does not call the reader | The first read and all elapsed-time accounting depend on `tick()` executing |

The [observer](../../../../Mod/UI/ExpeditionTrainingName.lua) uses 0.25-second samples, a 10-second readiness window and a separate 10-second acknowledgement window. Only unsent pending readiness can retry on the specified events, at most three times per observer session. These are technical wait/timeout controls, not production time or mission time. They do not provide an independent watchdog if the update callback itself is not delivered.

A minimal local reproduction executes the actual current observer, native-name reader, Gate and Store with the existing native-API fixtures. It does not modify runtime source or formal tests:

| Controlled condition | Observed local result |
|---|---|
| Name is already READY; run 100 publication/selection/turn cycles, deliberately withhold the frame callback | NAMING / PENDING; zero reader calls, zero NAME requests; one observer attempt |
| Same unit, source and facts; deliver the first 0.25-second callback | One real reader call, one NAME request, CREATED, original source retained |
| Native name remains the default; deliver callbacks through the deadline | WAITING, no NAME request; not perpetual PENDING |
| Current B203 trained P0 READ with a ready name | NAMING, zero NAME requests, as intended by its trained-READ exclusion |

**Evidence limit:** withholding a callback is an injected condition. This proves the callback dependency and a matching failure mode, not that Civ VI withheld that callback in the user's session. Existing tests manually invoke the init/update handlers and the observer fixture substitutes NativeName; they cannot establish native UI lifecycle delivery. This reproduction uses the real reader but still mocks native API results. The prior 457 targeted PASS remain local evidence, not a native success claim.

## What is and is not known about this run

**STATIC_CONFIRMED:** [ordinary button feedback](../../../../Mod/ExpeditionSpyUI.lua) returns NAME_PENDING for matching NAMING not only while the observer is PENDING/CONFIRMING, but also when there is no matching observer status at all. Thus the remembered message cannot distinguish “observer not running” from “name not ready” or “acknowledgement pending.” A stalled or not-yet-refreshed UI label is also not a live trace.

Read-only comparison of the six direct package files (name observer Lua/XML, P0 window, reader, Gate and modinfo) found source/live byte equality. The current Modding.log contains “Applying Component - SPC_ExpeditionTrainingName (AddUserInterfaces)”. This demonstrates component application was attempted, not that its Lua init, event handler or frame callback ran for the failed team. The available logs provide no observer stage/name-read/NAME-ack trace. No current Lua.log was available. Existing activity UI uses the same empty-Context/SetInitHandler pattern, so there is no basis to declare that pattern universally unsupported.

**UNRESOLVED_NATIVE_BOUNDARY:** observer startup/discovery, actual callback execution, native reader result, and request/ack stage cannot yet be distinguished for this failure. Name assignment delay is not established as the root cause. An inadequate timeout is not established either; increasing it would not address the demonstrated first-read dependency.

Ignored evidence: `local/legacy-workspace/Specialization/Status/Validation/Evidence/B203/investigation/`. The minimal reproduction, its raw output, exact source/live hash comparison and narrow log excerpts are retained there with checksums. No raw evidence is added to Git.

## Recommended next repair — not implemented or newly authorized here

1. Make the existing exact-team observer event-first: after discovering a valid NAMING transition, attempt current name confirmation immediately; directly re-evaluate on the relevant existing publication/selection/load/turn wake-up while genuinely pending. Keep reentrancy protection, exact source/unit/name checks, bounded work and one owner for NAME submission. Do not make the first useful action depend on a frame timer or a diagnostic window.
2. Keep a short bounded deferred check only for genuinely unreadable native facts and asynchronous acknowledgement. Preserve terminal invalid identity and uncertain-send/no-replay rules; do not remove protection or add a per-frame world/city scan.
3. Record one replaceable, bounded stage diagnostic: observer initialized/discovered, first read and exact pending reason, NAME submitted, authoritative confirmation or stop. Separate “confirmation has not responded” from “native name is not ready” in normal feedback. Trace stage changes only, not every frame; P0 remains a reader for normal training.
4. Add targeted real-reader/event-driven local counterexamples with frame delivery absent, delayed readiness, event bursts/reentry, stale source and uncertain acknowledgement. Retain the relevant existing regressions. The native delta remains one normally trained team with P0 closed → usable **派遣到新城市** → source retained on arrival; if it fails, the same run should identify the exact stalled stage. No repeated save/load/task campaign.

This proposal repairs the event-to-confirmation path without changing the accepted training cost or capacity/source contract. If startup evidence shows the separate addin never initialized, repair that registration/lifecycle boundary before treating any name-read retry as meaningful. No specific engine root cause is asserted before that evidence exists.

## Fixed-one-turn city project backup

A project whose completion handler explicitly creates the unit would give that writer the exact returned unit ID and known source, like prototype CREATE. It can simplify production-to-instance correlation. It would still need valid native-name/travel continuity and UI confirmation, so it does not automatically solve the current blocked transition. Changing normal Spy-formula training into a fixed 1T project is a separate gameplay/cost decision; the user has offered it as a backup, not authorized that replacement. No project, production-rule or Design change is made.

Document checks: current P0-N1 context/integrity PASS (218 runtime files,631 guarded references);338 local Markdown paths/anchors checked; diff whitespace/scope, unchanged runtime review hashes, frozen Status history, and ignored reproduction checksums PASS. The prior457 gameplay tests were not rerun for this documentation-only investigation.

User decision: review the event-first repair proposal. User testing: none requested during this investigation. Codex next: implement only after approval; keep later Expedition batches held.
