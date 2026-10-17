# B224 — Current Great Works and Expedition idle controls

**LOCAL validation recorded below; USER_GAME_TEST_REQUIRED.** User explicitly authorized simultaneous investigation and narrow repair of the Expedition availability fault and Culture empty-collection withdrawal. Source B224.251 / modinfo251. No Design, capacity, binding, permanent schema, mission duration/reward, movement, GC, main or game-configuration change. No new timer or polling loop.

## B223 native evidence retained

Three ignored collector sessions were read: `session-20261017T190940Z-1cd41e`, `session-20261017T192134Z-4e99bb`, `session-20261017T192959Z-92c04a`, under `local/diagnostics/B205/`. Their records.log SHA256 values are respectively:

- `56659c2627f804aee2130808c2dd96225b23d6308aaa6ae0078eaf7e25fd27cd`
- `9899d8c76eeeb41f19b9acb60a1dcca3c1c77ef7f4c564b0722a496df6121958`
- `6430e19123f22659d8f6e6ede2f32b06abcc8321d0313cfeb612e1644af643d3`

Raw evidence remains unchanged and ignored. Session3 replays session2 snapshots: deduplication by context+seq yields95 trace rows, seven dispatch/arrival sequences, four ACTIVITY_START records, zero ACTIVITY_FAILURE records. These are not seven complete mission tests. Four PEOPLE attempts reach confirmed ASLEEP/TASK_RUNNING; one captured two-turn-later RELEASED receipt confirms release, without independently certifying its reward. Several departures are SLEEP and arrive AWAKE with4/4 movement. Repeated manual sleep does not deterministically reproduce the prior Ottawa denial.

The user reports a London arrival with missing Skip/Sleep controls and an unusable task, followed by many non-reproducing rounds. The sole captured failed task at(19,37), T72 is WORKS: `MISSION_WORK_READER_UNAVAILABLE`, before activity admission. Its final receipt remains confirmed ARRIVED revision121 with no task clock or activity ownership. The adjacent idle-control log has six false eligibility values. Both the task failure and disappearing controls are actionable defects; later successes do not close them. B223 has no native REJECTED-ack case, so it does not newly certify B222's denial unwind. Collector GAME_EXITED after its30-second idle threshold is not independent process-exit evidence during reload.

## Repairs and reproduced boundaries

### Reliable empty collection

`UI/DialogueRefresh` previously sent `FactsData=''` when the last nationally held work departed. `GreatWorkFacts` requires a string. A transport that omits empty strings makes that sample UNKNOWN; the same-reference Culture writers deliberately retain their last confirmed projection. This reproduces the user's lingering Tourism symptom without any0-to1 arithmetic.

Actual Lua counterexample, including three real consumers: initial Aesthetic projection9, Meaning3 carriers and Inspiration3%; removing the empty payload field while count=0 leaves those values with `GW_SAMPLE_SIZE`. A valid empty sample removes all three. This is a demonstrated transport-shape vulnerability; the native failed packet was not directly captured, so it is not a claim of observed engine serialization internals.

Producer now sends explicit nonempty `EMPTY`; receiver accepts it only with exact numeric count0 and all existing reference/completeness/epoch/turn checks. Legacy empty strings remain readable; missing/malformed data stays UNKNOWN. Per-city UNKNOWN is not converted to zero. No calculation, effect ownership or permanent history changes. Local-city zero with another city still holding works clears only the changed city. Three consumers share the corrected facts; no separate scans were added.

### Exact fresh work read in the correct context

The old WORKS validator directly called slot/type getters on the Gameplay city building object. Existing location browsing and shared Great Work collection use those readers in UI. Startup and completion both used the wrong assumption; passing a selected UI work label alone would not repair completion.

`ExpeditionSpyRead.WorkSlot` reads exactly the requested city/building/slot in UI and returns detached scalars. Always-loaded `ExpeditionSpyActivity` installs the synchronous endpoint independently of P0 or mission-window visibility and removes only its own function on shutdown. `ExpeditionSpyGate` calls it at each existing validation boundary, checks endpoint/turn/building/slot and still compares the saved exact work ID/type. This reuses the fresh synchronous completion-read pattern in `UI/DialogueProjectUI` / `DialogueProjects`; no new bus, saved inventory or UI reward authority.

Empty slot(-1) and same-type replacement invalidate the selected work; instance0 is valid. Missing/throwing readers, nil and stale samples stay UNKNOWN and cannot grant rewards. Existing bounded same-turn retry/due-time protection remains unchanged. PEOPLE/PLACES keep their original readers. The dedicated fixture now provides work APIs only in an isolated UI environment; Gameplay deliberately lacks them.

### Idle controls use the current unit through execution

The wrapper previously sampled the head-selected proxy, while native Refresh reacquired FindID; native travel replaces unit identity. It also flattened false/nil/errors to false and silently removed controls. Reacquire the exact selected owner/id for rendering, signature and click; keep ALLOWED/DENIED/UNAVAILABLE/READ_ERROR distinct. Relevant idle rows remain disabled with a short explanation if native permission is unavailable. Native activity selects Skip/Sleep versus Wake; running/locked tasks still expose none.

For these three no-interface native rows only, click uses the same fresh object, global native turn-processing guard, exact current selection/Gate state and fresh native eligibility before RequestOperation/RequestCommand. Ordinary units and all other actions retain the original callbacks. No automatic Wake, restored movement or permission bypass. Existing publication/selection/activity/operation events refresh controls; no added timer. This fixes silent disappearance and stale-object handling, without claiming the engine can never legitimately deny an action.

Read-only source basis: `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua` lines28,281–290,2347–2362,2493–2542 and turn guard updates; `HD/Lua/DL_UnitPanel.lua` lines998–1012. CIV_ASSETS/HD denote installed source roots, not public links. The inspected idle rows have no InterfaceMode; HD's extra generic-click handling concerns Great Person activation. Existing third argument `currentMode` was valid and is not classified as a bug.

New localization keys, both zh_Hans_CN and en_US: `LOC_SPC_EXPEDITION_IDLE_DENIED`, `_UNAVAILABLE`, `_READ_ERROR`.

## Validation

**490 targeted tests PASS.** Actual Lua suites cover the empty-wire roundtrip, all three Culture consumers, wrong/missing samples, same-type instance replacement, due-time re-read, reader registration/shutdown without P0, fresh-object button clicks, native denial/error/nil transitions, turn guard, stale callbacks, mission/activity rejection and recovery, Store, location/selection UI and retained diagnostics. The external DB was read-only; existing Python/Lupa were reused. Current modinfo251 file references and both localization languages pass.

Three historical package-only checks still pin193/199/200 and were excluded from the maintained current run, not rewritten or counted as PASS. The old standalone Aesthetic SQL bootstrap assumes a pre-Aesthetic database and fails on the already-installed bit table; it was not rerun as a current fixture. Its actual model/writer is instead exercised through the maintained shared three-consumer integration, including zero/UNKNOWN/city isolation. The first exploratory run exposed these fixture-version mismatches; no gameplay assertion was weakened to hide them.

Independent read-only reviews checked bridge context/lifetime, zero-versus-UNKNOWN, and current-unit rendering/request continuity. The latter found a callback re-fetch gap; it was fixed and covered before the490-test result. Source diff shows no new timer, permanent field or ordinary-Spy override. Context/schema/hash/selector and changed-document links are checked before commit.

Read-only consumer/source review and targeted simulations do not certify native mission settlement or native serialization. Original B223/B222 evidence and frozen results are unchanged. No unrelated gameplay regression or stress campaign was run.

## Minimal combined native flow

Use the currently authorized test campaign and existing manual collector; no separate save/reload ritual:

1. In a Culture city with active 风雅熏陶, record its current contribution, then remove its last eligible works. Verify 馆藏/巨作事实 reports0 eras and 风雅熏陶 contribution becomes0. If naturally practical, leave no works in any owned city to exercise the nationally empty payload. Reintroduce one eligible work to verify the contribution returns. Other-city holdings must remain unaffected.
2. With an idle Expedition, use **派遣到新城市** and check **跳过回合／休眠** after arrival without opening P0. In a city with an available work, select **任务 → 艺文采撷 → 开始任务** once and let it finish. This checks the new fresh reader at admission and completion. Existing PEOPLE/PLACES acceptance is inherited, not a required repeat of all missions. If no target exists, defer only WORKS; do not manufacture a long scenario.

The collector remains the primary evidence. One screenshot is useful only if the visible disabled reason or displayed yield disagrees with the record; no repeated London sleep cycle requested. Native denial stays an explicit disabled state, never a hidden control or forced operation.

## Delivery

B224.251 deployed from `ceb883b` after fresh automatic process-exit checks and both receipt/hash-guarded switches. Receipt `B224.251-ceb883b-playtest.json`; **224/224 MATCH**; source/runtime digest `274b584d0eb919b14c44e8c91ad99abf78bb849a72b22557145b01d430bf5ca0`. B223 and stable recovery retained, no pending transaction. Main/configuration unchanged; game not launched. Deployment integrity is not native acceptance. User decision: none. User testing: the two small deltas above. Primary next: review those results; no unrelated feature batch or audit repair authorized.
