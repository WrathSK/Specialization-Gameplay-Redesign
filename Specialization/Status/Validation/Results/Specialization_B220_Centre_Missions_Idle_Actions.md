# B220 — City-centre missions and arrival idle actions

State: LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED. Source B220.247/modinfo247. User explicitly authorized implementation and guarded deployment; live state is recorded separately below.

## User decision and B219 evidence

The user stopped B219 because the PlaceUnit/MoveUnit controls were not available in the test UI. Collector sessions `session-20261017T060603Z-b255e8` and `session-20261017T060936Z-123e03` contain ARRIVED READ and END, but no movementProbe trial. This is an unsuccessful test entry, not a negative or positive movement-interface result. Exact UI failure remains UNKNOWN. No repeat comparison is requested. Existing B218/B219 reports and raw logs remain unchanged.

The user accepts an interim implementation: 艺文采撷 and 奇观巡礼 execute at the destination city centre. Moving the unit onto the work/wonder plot is deferred and nonblocking. The selected real site still governs eligibility and completion evidence. No design-wide revision or new reward rule is inferred.

## Implementation boundary

- Gate TASK retains missionX/Y, selected building/work ID, completion-time validation, cancellation and first-success city history. The unit's expected x/y stay at the exact destination centre; there is no task-site placement and no return teleport. Actual displacement still stops the task; invalid or UNKNOWN target facts are not made valid by being at the centre. Existing two-turn task progression and SLEEP acknowledgement remain unchanged. No new timer or polling.
- Native between-city travel and the existing entry-city continuation are unchanged. This batch does not claim to solve generic placement on occupied plots, including that separate continuation path.
- UnitPanel now checks only the selected owned team's three native idle-action permissions at game publication, selection, exact-unit activity/operation-deactivation and existing task-view notification events. One disposable identity/revision/permission signature suppresses unchanged rebuilds. No world/unit collection scan, frame callback, timer, diagnostic request, automatic wake or persistent UI state. Current locks and callback-time native permission checks remain. Shutdown removes owned subscriptions.
- Static diagnosis: previous rebuilding depended on task-view changes, whereas native visibility/eligibility can change independently. Local tests reproduce that mismatch. The native cause of the reported late buttons remains a hypothesis until user validation; permissions that are truly unavailable remain unavailable.
- B219 comparison UI registration, P0 right-click entry and Gameplay startup are disabled. Research source/tests remain available but are not active or part of default task reads. No ordinary Spy changes.
- Capacity, source binding, training, saved schema, earned Insights, Tourism writer, GC, main and external configuration are unchanged. No compatibility migration for an interrupted prior-build mission is introduced.

## Local validation

**284 targeted tests PASS** using actual Lua with Lupa lua55 and the configured DB opened read-only for existing package/SQL checks. Modules: idle_actions, missions, placement_diagnostic, spy_task, spy_persistence, spy_activity, spy_activity_pending, position_wait, movement_probe, spy_gate, spy_activity_integration, spy_actions_ui and spy_relocation_ui (each with the test_expedition_ prefix).

New/delta cases cover native permissions changing without a Gate revision; arrival unit-ID replacement; sleep/wake changes; ordinary-unit isolation; unchanged publication bursts; shutdown and reentrancy; both site categories completing with no PlaceUnit even when civilians occupy the site/centre; exact selected evidence, disappearance cancellation, duplicate rewards and displacement rejection. Existing placement diagnostic tests now exercise the still-active entry-city continuation, retaining failure/readback/event bounds, rather than expecting the removed mission movement. One test invocation named a nonexistent window module and failed discovery; the corrected final invocation above passed. No assertion was weakened to hide a runtime failure.

Local tests do not prove native rendering/permission timing, Tourism rounding or generic movement coexistence. No gameplay full regression, stress test, game launch or configuration change.

## Minimal combined native test

Use an eligible test city and a healthy team, without an interrupted old mission/HELD experiment. Start the existing collector manually. No new save/load exercise is required by this delta.

1. Dispatch normally. On arrival select the idle team without opening P0 or completing another task. Check native 跳过回合 / 休眠 controls; try 休眠 then 唤醒 once. This tests native action refresh independently of mission completion.
2. Start an available, not-yet-completed 奇观巡礼 (or 艺文采撷). The team stays at the city centre while the task card still identifies the real eligible site. After the existing two turns confirm completion, one new Insight and restored idle controls. No return teleport or displacement stop is expected. Already recorded civilization/category Insights are not reset for testing.
3. If both categories have legitimate targets, run the other in the same session; otherwise leave that category native-pending for a later batch. No target fabrication or repeated cold-load gate. Logs capture execution centre/evidence coordinates, changed idle-action signatures and completion. A screenshot is useful only if visible controls disagree with logs.

User decision: interim centre execution accepted; site movement deferred. User testing: one combined arrival/control/task session. Primary next: review the submitted delta evidence, not another movement experiment or automatic next batch.

## Checks and deployment

Context check PASS (224 runtime / 669 guarded files), self-test PASS,11 current-slice/report links and anchors PASS, diff check/review PASS and staged publication check PASS.

B220.247/modinfo247 DEVELOP_ACTIVE; source 3b7530e975e278ec7a600067cfb00da6a4868edf; receipt B220.247-3b7530e-playtest.json;224/224 MATCH. Fresh automatic OS exit checks before both guarded switches; B219/stable recovery retained; no pending transaction, configuration or main change.

Source commit `3b7530e`; deployment-record checkpoint follows. No native PASS is implied.
