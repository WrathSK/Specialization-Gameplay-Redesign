# B184.211 — Spy1 native travel review and mission-isolation boundary

Date: 2026-10-10. **PARTIAL native result.** Travel/arrival and one co-located unit are observed, but the arrival report contradicts its own binding state. Mission execution/isolation remains **NOT_TESTED / BLOCKED**. The user reports the run looks normal and identifies mission rewriting/isolation as the next key question; this does not authorize a new implementation batch.

Source: B184.211/modinfo211, implementation commit `3e9092c`; reviewed worktree `a64f322`. The [frozen local result](Specialization_B184_Expedition_Spy1_Isolation_Local.md) remains unchanged. [Current slice](../../../Architecture/v2/P0_N_Expedition.md#current-slice--n1-travel-and-protection-gate) · [Next bounded plan](../../../Reports/Technical/Specialization_Expedition_Movement_Coexistence.md#next-proposed-batch--continuity-and-mission-isolation).

## Submitted observations

Five original images were individually read. Times below identify their original filenames, all dated 2026-10-10. Raw images and the SHA256 manifest are local, Git-ignored evidence under `local/legacy-workspace/Specialization/Status/Validation/Evidence/B184/2026-10-10/`, relative to the develop root; they are not public repository attachments.

| Image / time | Native observation | Evidence limit |
|---|---|---|
| 1 / 12.02.14 PM / T84 | Created team `3145757` at `(62,33)`; source Edinburgh(Test), city `393220`; own count1/1; other occupants0. Native maximum5→5, ordinary Spies0→0, source-city Spy trainability yes→yes. Native classification reads0 immediately after create. | Initial source readback is present. This fixture has no ordinary Spy; unchanged maximum/trainability does not prove all occupied-slot behavior. |
| 2 / 12.02.41 PM / T84 | Same team/source; Sparta selected. Travel2T + establishment0T, native allowed. Sources0T; Gain Sources eligible; raw success-undetected1, success-must-escape0. Native classification now1. Execution remains explicitly blocked. | Getter/probability evidence for this actual fixture, not completed Gain Sources or zero side-effect proof. |
| 3 / 12.02.51 PM / T84 | Native travel starts, dueT86. Same reported ID/source, own count1/1, coordinates `(-9999,-9999)` while travelling. | Native off-map state, not failed map placement. No manual teleport is inferred. Previously read mission values are not a fresh arrival sample. |
| 4 / 12.03.52 PM / T86 | Headline says original unit reached target center; report now shows team `3211293` at `(23,15)`, count1/1 and one other unit on the tile. It also says **旧团或未绑定团：只计入容量，可明确结束，不自动接回来源。** The source line is absent. | Arrival is a positive travel observation; original-ID/source continuity is not PASS. One co-located unit is observed, not a complete hostile-contact/civilian-type immunity test. |
| 5 / 12.04.06 PM / T86 | END reports0/1 and removal; maximum5→5, ordinary0→0, trainability yes→yes. Native classification still reads1. | Gameplay readback supports scoped removal. The immediate UI classification does not establish whether publication is stale or native residue remains. No claim of complete native-slot cleanup or a proven leak. |

Images1–4 show player-level Spy completion count0 / lastNONE during the observation window. No completion event was observed; this is not a guarantee for all travel, idle or mission paths. Gain Sources was not executed. No new save/load, source-loss, ally/war-target, task-building/Wonder placement or formal reward evidence was submitted.

## Identity discrepancy and report defect

**USER_GAME_TEST evidence:** the displayed ID changes from `3145757` to `3211293`; the arrival report marks the team unbound. Thus the local result's intended original-ID arrival guard was not established in this native run. The native reason for ID replacement/aliasing is not proved by screenshots alone. No unit is adopted by matching its name, position or sole presence.

**STATIC_CONFIRMED:** [Gate `owned`, `observe`, `snapshot`](../../../../Mod/ExpeditionSpyGate.lua) verify the object returned by `FindID(oldID)` for owner/type, but omit the explicit equality `returned:GetID() == oldID`. `snapshot` independently compares the collection member's current ID to the stored ID when setting `unbound`. Therefore `sameUnit`/ARRIVED can contradict `unbound`; [window rendering](../../../../Mod/UI/ExpeditionSpyWindow.lua) prints the phase headline before the unbound warning and hides the source line when unbound. This is a real verification/reporting gap, not proof that the saved source record was deleted.

**Controlled local counterexample, actual unmodified B184 module:** the existing Lupa fixture creates ID40, dispatches, then exposes the arrival object as ID41 in `Members()` while a mocked `FindID(40)` still resolves that object. At the target and due turn, readback is:

```text
phase=ARRIVED, unitID=41, createdID=40,
sameUnit=true, unbound=true, bound=false, sourceCity=1, count=1, stop=nil
```

This reproduces the contradiction and missing equality guard. The lookup alias is an injected condition, **not a measured explanation of the native engine**. Reproduction used `gate()` from `DevelopmentTests/test_expedition_spy_gate.py`, changed only the in-memory fixture's unit ID/collection lookup, and called `ownTurn`/`READ`; no repository tests or runtime were edited. Existing changed-ID tests model disappearance of the old lookup; they do not cover this alias condition. Prior 41 local methods remain their original evidence, not a new all-tests result.

Installed HD `Gameplay/UnitAbilities.lua` around530–539 already comments that native Spy travel changes IDs. Its adjacent Local Informant path filters exact `UNIT_SPY`, and its name-based workaround is not a safe identity contract for this prototype. This corroborates a reason to investigate native continuity; it does not prove what happened internally in this run or authorize name-based reattachment.

## Gate classification

| Gate | Result |
|---|---|
| Spy1 native request / off-map travel / reported destination arrival | Scoped positive native observation; Spy0 placement failure is not repeated |
| One-unit co-location at arrival | Observed; comprehensive harmless coexistence/hostile contact NOT_TESTED |
| Own capacity count and source at creation | Observed1/1 and correct source readback |
| Reliable logical-team/source continuity after native travel | **NOT_PASSED — TECHNICAL_IDENTITY_BOUNDARY**; changed ID and unbound state, with confirmed report-verification gap |
| Explicit END | Own Gameplay count0/1 observed; post-publication native classification unresolved |
| Ordinary Spy independence | Readable fields unchanged in a zero-ordinary-Spy fixture; full used-slot/mission isolation NOT_PROVED |
| Gain Sources raw eligibility / odds / source getter | Observed before travel; execution BLOCKED, native/HD reward isolation NOT_TESTED |

The immediate0→later1 classification after create and the1 after END are compatible with a Gameplay/UI publication delay, but do not prove it. A future narrow repair should sample after publication and label freshness; no additional test of the unchanged package is requested now.

## Remaining mission work

The next proposed boundary is **reliable travel continuity plus one independently timed, no-reward task**; see the linked plan. Native Gain Sources is an available safe-success reference, not an isolated blank task. Its city-addressed source duration and HD completion bridge remain the concrete obstacles. Prefer retaining the verified part of Spy1 travel while our own code owns task completion, rather than sending Gain Sources and trying to remove other systems' effects afterwards. This recommendation still requires review/authorization and evidence about native idle/operation behavior.

No formal N1 completeness, N2/N3, era UI, archive/insight rewards or Design change. The user need not repeat the unchanged travel test, save/load ritual or ordinary Spy failure scenarios. Any next native session must distinguish the new continuity/mission-isolation delta; no session is dispatched by this evidence record.

## Archive and maintenance checks

All five original filenames/bytes are retained; pre/post SHA256 equality was checked, with no overwrite or duplicate inbox copy. The local manifest holds the full hashes:

| Image | SHA256 |
|---|---|
| 1 | `0fdfa0704de49ebedac3c2f8fa86cd414d0170575925746f4ac7d240c1b5bfd1` |
| 2 | `c7dadb5bb8ffe50aaaa3a29abb6b494d0f7b17544c222b761621c398d5d94004` |
| 3 | `e637ba346e03338a936bc80bc4bde7550d86306e4be7ae48ba59e2af68fa1747` |
| 4 | `0ff1b0333223e350689ee73f986638cc1e13a4a7201f2f852da8b2f51175a97c` |
| 5 | `5208f6470c51f8f35da6ddc95f5aca15af28be338fbf6e095efde52e94c0dccb` |

Only evidence/current documentation and named review hashes change. Active links/anchors, current selectors, P0-N1 context/integrity and diff scope are checked. No gameplay regression, runtime/deployment/configuration/HD/Design/test change, main edit or game launch. Source/live remains the previously verified B184 receipt; this review does not re-verify the external package.
