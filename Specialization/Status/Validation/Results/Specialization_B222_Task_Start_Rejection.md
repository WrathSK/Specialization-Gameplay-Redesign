# B222 — Shared mission-start rejection handling

State: **LOCAL_SIMULATION_PASS; native SLEEP denial remains unresolved.** B222.249 / modinfo249. The user authorized the bounded repair after the [B221 native review](Specialization_B221_Activity_Native_Review.md) and the request to reuse the PEOPLE task path. This repairs the confirmed terminal-lock response to an unexecuted denial; it does not claim the engine now permits SLEEP or that missions have passed natively.

## Scope and evidence

PEOPLE, WORKS and PLACES already converge on the same Gate/activity bridge. The exact B194 no-reward and B214 PEOPLE sources use the same database-hash permission call. B214's same-centre relocation returns before any native movement call. There is no evidence that restoring that call or bypassing denied permission would repair the native cause. B221 proves AWAKE / exact centre / native DENIED / no request, followed by unnecessary HELD; it does not prove a move-count, occupied-tile, Spy or timing cause. Earlier native successes/failures remain unchanged.

## Changes and ownership

- The UI bridge can return **REJECTED** only for exact current SLEEP / TASK_PREPARING, clean boolean DENIED, no ownership/ARMED/request attempt, followed by fresh matching identity, native mission, position and AWAKE/HOLD reads. It submits no native operation. Missing/throwing/non-boolean permission and changed state keep the existing FAILED protection.
- Gameplay independently checks the current attempt, phase, current-turn sample, no saved ownership or clock, no request/attempt, source/target references, exact unit/name/centre and available native mission reader. Only then does it discard this unstarted mission draft and save ARRIVED. Failed readback remains HELD/BLOCKED. Duplicate/stale replies cannot cancel a new attempt. Existing HELD saves are not automatically cleared.
- Binding, capacity, generation, accumulated task count and city Insights remain intact. No Store schema/field or gameplay rule is added. The existing session-only activityFailure supplies feedback; a new explicit task/dispatch clears it, and ordinary load reconstructs idle from the existing saved authority. There is no automatic task retry.
- The unchanged actual boolean-only CanStartOperation guard explicitly requests no results (native UnitPanel lines609/615). On DENIED only, make one protected read-only query with the native NO_TARGETS hint and capture at most four localization-key FAILURE_REASONS from its second return. Missing hints are explicit; the second query's boolean is logged separately and cannot override the original denial. Preserve hash, unit type, shape, explicit absent/empty/malformed/unreadable status and truncation. Non-key text is redacted. No extra query on success, native request, automatic retry, arbitrary native string, native object or unbounded history is added. Native UnitPanel uses this result surface in `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua`, lines673–702; CIV_ASSETS denotes the installed read-only game asset root. Whether this build returns a useful SLEEP explanation is still unknown.
- Reuse the schema205 64-entry ring / 96-record producer budget and existing collector. Chinese/English `LOC_SPC_EXPEDITION_SPY_ACTIVITY_START_DECLINED` explains that no task started and logs should be retained. This is not a binding-loss or completion message.

The successful native sleep → observed ASLEEP → two-turn task → completion/release pipeline is unchanged for all three categories. Their real target qualification, completion-time validation and unique rewards remain separate. No task-site/return movement, timer/retry, global scan, capacity/binding/Insight/GC change, ordinary Spy edit, Design change, main or game-configuration change. The inherited B194 activity watcher is not expanded by this batch.

## Local validation

**381 targeted tests PASS** (350 Gate/mission/activity/Store/UI/collector tests, plus31 package/SQL tests against the explicit read-only loaded DB copied into memory). Actual current Lua runs through existing Lupa fixtures; no game/live Lua query. Commands use the existing Lupa environment and DevelopmentTests import path:

- `python3 -m unittest test_expedition_task_rejection test_expedition_missions test_expedition_spy_activity test_expedition_activity_trace test_expedition_spy_activity_ui test_expedition_spy_activity_diagnostic test_expedition_spy_activity_pending test_expedition_spy_activity_failure test_expedition_spy_activity_report test_expedition_trace_reader test_expedition_trace_collector test_expedition_spy_activity_integration test_expedition_spy_task test_expedition_spy_persistence test_expedition_training_diagnostics`
- `python3 -m unittest test_expedition_spy_gate` with the existing `SPC_DEBUG_GAMEPLAY_DB` configuration.

New counterexamples cover all three categories' denial and successful pipeline, explicit new-attempt keys, stale replies, refusal after ARMED, identity/activity changes during denial, source loss, Store no-op/malformed/throwing writes, local idle reconstruction, unchanged held saves, readable localized feedback, bounded/redacted native reasons, missing result hints, disagreement between the decision and diagnostic query, and diagnostic failure isolation. Shared cleanup/load evidence is inherited; no new user cold-load loop. Initial local failures were a new-test quoting error and using the wrong fixture field for native operation; both corrected. Existing denial assertions change only from terminal FAILED to the approved clean REJECTED outcome; uncertain/owned-action assertions remain.

Local checks do not explain native denial, prove engine readiness, or establish performance/memory improvement. Context/selector, package, staged publication and diff checks accompany delivery.

## One bounded native continuation

Use the existing manual collector and a healthy ARRIVED team before a task attempt in the approved test campaign. Do not use an already HELD team as automatic recovery evidence. Select one available mission and click **开始任务** once.

- If declined: stop after that click. Confirm the team remains available and the UI says the task did not start; retain the collector log. No turn, repeated click, P0 screenshot, save/reload or permission bypass is requested. The new information is the actual native denial result and whether the confirmed lock defect is fixed. If reasons are absent/redacted, report that limitation rather than claim a cause or request another blind loop.
- If started: complete the existing two-turn task and check one Insight and released controls. This is a conditional continuation of the same attempt, not proof that the cause of the B221 denial was eliminated.

User decision: none for this bounded repair; any different activity/native-mission route needs a concrete new proposal. User testing: one logged attempt after verified deployment. Primary next: review that result; no further batch, broader UI change or speculative native reset.

## Deployment

Source locally validated; live remains B221.248 until the guarded W0003 deployment is verified. No native PASS claimed.
