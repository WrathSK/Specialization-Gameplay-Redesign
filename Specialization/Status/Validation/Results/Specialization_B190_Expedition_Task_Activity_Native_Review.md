# B190.217 — task activity constant preflight failure

Date: 2026-10-10. **USER_GAME_TEST_FAIL: task activity startup.** The submitted two images show a stop before native sleep eligibility or submission. **Native SLEEP permission, needs-orders suppression, completion/release: NOT_REACHED.** B189 name/source/task observations remain valid in their original scope; no formal N1 completion or new lifecycle PASS.

Source/runtime last recorded B190.217/modinfo217, source `4c577a40ee4deae383c2085c4f32efc215076751`, receipt `B190.217-4c577a4-playtest.json`,213/213 MATCH. Documentation baseline `a7255b0`. This review does not reverify or modify the external runtime.

## Individually viewed evidence

| Screenshot | Visible evidence | Conclusion |
|---|---|---|
| 1 / 9.07.15 PM / T88 | Experiment paused; ACTIVITY_READBACK_STOP; team3342365 at(23,15), cap1/1; accepted/current name艾莉森; original sourceEdinburgh (Test), city393220 retained; candidate/exact lookup name and source reference MATCH. The panel also calls it old/unbound. | Activity attempt stopped. The shown identity/reference evidence still matches; the unbound label alone does not demonstrate lost binding. |
| 2 / 9.07.18 PM / T88 | Scrolled detail: created3276829/current3342365; exact lookup3342365 MATCH; native maximum5→5/ordinary count0→0; custom Spy count1; observed mission-completion events0; failure stepACTIVITY; technical detail ACTIVITY_READBACK_STOP: ACTIVITY_SLEEP_CONSTANTS_UNAVAILABLE. | Identifies the startup constant guard, before the sleep request. No task completion or END is pictured. |

[Gate](../../../../Mod/ExpeditionSpyGate.lua) deliberately sets phaseHELD on the failed activity acknowledgement; its snapshot marks boundfalse when HELD even if the retained name/source checks still match. That explains the misleading generic unbound wording. Source/capacity records were not cleared by this branch. Do not infer a new continuity failure or remove the guard merely to change the wording.

## Root cause and certainty

[Activity bridge](../../../../Mod/UI/ExpeditionSpyActivity.lua):81 requires `UnitOperationTypes`, `.SLEEP`, `OperationResultsTypes` and `.NO_TARGETS` together. The exact screenshot error proves this combined requirement failed. **Which individual symbol was absent remains UNKNOWN** because this error combines the checks. It is a B190 integration assumption failure, not evidence that Spy=1 cannot sleep.

This guard precedes `CanStartOperation`, `n.requested/owned`, and `RequestOperation`. The emitted failure therefore reports ownedfalse; Gameplay holds before timer start. No B190 sleep/wake request or native mission is issued on this failing route. This is a source-trace conclusion paired with the screenshot error, not an instrumented native operation-count measurement.

Native source alias `CIV_ASSETS` means the installed Civ6.app/Contents/Assets; no public/local file URL is required. Direct read-only references:

- `Base/Assets/UI/Panels/UnitPanel.lua:227–233`,407–409,548–550 resolves command/operation **GameInfo row.Hash**;2513/2535 submits those hashes.
- Same file609/615 uses `CanStartOperation(unit, actionHash, nil, false, false)` for a real eligibility check with no results. The optional NO_TARGETS performance hint at677 need not become an availability requirement.
- `Base/Assets/Gameplay/Data/UnitOperations.xml:103` defines UNITOPERATION_SLEEP; `UnitCommands.xml:35` defines UNITCOMMAND_WAKE. Both exact rows also exist in the configured read-only DebugGameplay DB (VisibleInUI1, categoryINPLACE). The SQLite schema does not expose a Hash column; runtime row.Hash is established by native Lua usage, not a fabricated SQLite value.

The existing [bridge fixture](../../../../DevelopmentTests/test_expedition_spy_activity_ui.py):33 supplies all assumed aliases/hints. It tested transitions and ownership under that model, not actual constant exposure in the new context. The179 local-method record remains unchanged; it did not establish this native precondition.

Three in-memory counterexamples executed against the actual bridge, using that existing fixture: remove only SLEEP; remove the OperationResultsTypes table; remove only NO_TARGETS. Each reproduces the same guard error, with sleepRequests0/wakeRequests0/Ownedfalse. This proves the diagnostic ambiguity and early writer-free failure; it cannot identify the live missing symbol. No formal test/source change, external write or game call occurred.

## Proposed narrow repair — needs approval

1. Resolve the exact `GameInfo.UnitOperations['UNITOPERATION_SLEEP'].Hash` and `GameInfo.UnitCommands['UNITCOMMAND_WAKE'].Hash`, validating row/hash availability. Do not hardcode native numeric IDs or invent enum aliases.
2. Use the native boolean-result eligibility call `CanStartOperation(unit, hash, nil, false, false)`; retain eligibility checks and the one-request/readback/owned-release contract.
3. Distinguish missing row/hash, unavailable API, native denial and readback failure. Present the specific cause near the top of the report; distinguish a held task with matching retained source from an actual source mismatch.
4. Update targeted fixtures to expose DB rows but omit the assumed aliases/hint; cover missing/invalid row/hash and ensure no writes. Retain existing pending-command, identity, delayed-acknowledgement, cleanup and ordinary-Spy isolation checks.
5. After approval/local checks/deployment, repeat only the unreached activity delta: bound arrival → **④ 无奖励任务（2回合）**, no manual idle → normal turns with window closed → completion/owned release → **结束并移除验证团**. No new save/load campaign or repeat naming investigation.

No implementation or deployment in this review. Do not retest unchanged B190. This evidence does not justify native Gain Sources, global end-turn bypass, altered capacity/source semantics or N2/N3 expansion.

## Archive and validation

Both originals visually inspected, moved without renaming/overwriting to ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B190/2026-10-10/`, and verified by pre/post SHA256; local manifest associates this report. No screenshot/raw log enters Git.

- `Screenshot 2026-10-10 at 9.07.15 PM.png`: 12953773 bytes; SHA256 `04bfc0277cac0450e95a6cfe99f2a4e5dbf6a5b5db457970a61369510e0ccdf1`.
- `Screenshot 2026-10-10 at 9.07.18 PM.png`: 13065033 bytes; SHA256 `4dd0377167379dbf77faeab5bfe66a4aeaeae467a2f71dc1d130b56ae70e9883`.

Checks: three targeted in-memory counterexamples, read-only native source/DB lookup, changed/new Markdown links and anchors, current selector/context/schema/hash consistency, protected-path and diff review. Existing local evidence, Design, Mod, tests, main, GC and runtime remain unchanged. No game launch or deployment.
