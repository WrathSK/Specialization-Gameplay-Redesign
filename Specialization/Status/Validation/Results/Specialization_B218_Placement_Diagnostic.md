# B218 — Bounded mission-placement diagnostic

State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. Source/live B218.245; deployment verified below.

## B217 native stop and competing explanations

The user reports B217 failure and suspects a civilian at the mission tile. Ignored collector session `local/diagnostics/B205/session-20261017T052234Z-f31075/` contains 26 records, ending INTERRUPTED. At 05:24:49, MISSION_MOVE raises EXACT_PLACEMENT_REJECTED and the team enters HELD. This is the Gameplay immediate-readback assertion, not an engine-provided occupancy rejection reason. The B217 UI initial-position wait was not reached. Earlier B216 activity-position failure is a different boundary. Source binding/travel reached this attempt; this does not accept all remaining mission behavior.

Requested/actual placement coordinates and target occupants were absent from B217 evidence. Occupancy rejection, displacement and delayed visibility remain competing hypotheses. The loaded DB has Spy=1, Stackable=1, IgnoreMoves=1 and CIVILIAN formation for both ordinary Spy and Expedition. User clarification: ordinary Spy missions such as technology theft move to an occupied Campus without blocking. Record this as user-provided native behavior, not as independent verification of generic UnitManager.PlaceUnit semantics. Native Spy task placement and our generic placement path may differ; no conclusion that civilians must block either path.

## Authorized delta

Only Gameplay Gate diagnostics plus build labels and direct tests change. Before each actual mission/return placement, record requested coordinates, exact owner/unit ID, current coordinates and native Spy operation if readable. Immediately after the call (including a throwing call), record fresh readback. Target-tile enumeration records at most eight units, their owner/ID/type/coordinates and configured Spy/Stackable values; overflow is explicitly TRUNCATED, failed reads UNKNOWN. API errors retain their original protected failure. Diagnostics cannot bypass the exact-placement assertion, resume HELD, start a timer or award an Insight.

One scalar session watch observes only the same owner/unit's UnitMoveComplete events, including synchronous events inside PlaceUnit. At most six matching events are sampled. The watch closes on the cap, next owner turn, removal, load close, explicit END/STOP/CREATE/DISPATCH, or is replaced by the next placement. This is a diagnostic observation limit, never a task timeout. No timer, Update callback, periodic sampling, persistent fields, global unit scan or cached native unit objects. Diagnostics are protected so unavailable readers cannot change gameplay outcomes. A channel line identifies whether the event surface exists; absence of subsequent events cannot prove the engine never moved the unit.

Lines reuse collector-accepted N1_TASK framing; no collector changes or raw private paths. Existing B217 UI behavior, native sleep handling, accepted game-turn task duration, training/capacity/source binding, Store, Tourism, GC, Design and main are unchanged.

## Local validation

282 targeted tests PASS using the existing Lupa environment and explicitly configured read-only external DB. Eight new actual-Gate tests cover failed immediate readback followed by movement without resuming, occupied target evidence, synchronous success, synchronous removal with preserved POST sample, native throw preservation, unavailable occupant reads, unrelated-event exclusion, bounded observations, watch closure, truncated lists, and no diagnostic persistence. Existing mission, Gate, task, persistence/recovery and UI-position/activity suites remain included. Collector regex accepts diagnostic lines. Native occupancy/placement cause remains UNKNOWN; local tests do not establish native success.

## Minimal native capture

Start the existing collector manually. Use the established test campaign at a point before the failed mission. Select the same available **奇观巡礼** target and start it once, preferably without changing the suspected target occupancy. This is a diagnostic build: a protected stop may still occur. Do not retry repeatedly or move/delete the other unit to force success. Allow the ordinary UI/action to settle, then stop the test and provide the log. No need to end another turn, save/reload, or manufacture a WORKS target. PRE/POST and any matching movement events distinguish immediate no-op/displacement from later position change; absent events or UNKNOWN reads will be reported as missing evidence, not repaired by inference.

The user decision is diagnostic-only. Primary next: review this one capture before proposing a behavior repair. No new gameplay or automatic retry is authorized.

## Deployment

B218.245/modinfo245 DEVELOP_ACTIVE; source 0638eb5035b121c8f921eaac01b301c4c7bf18b5; receipt B218.245-0638eb5-playtest.json;221/221 MATCH. Fresh automatic OS exit checks before both guarded switches; B217/stable recovery retained; no pending transaction or configuration change.

Source/runtime digest: `81e28397a7d5b3822d6584a48c2394a6bde2585cc8998fad3d7f1b5b0d681a1e`. Context/selector self-test,372 local links, diff and staged publication checks PASS. No game launch, native PASS or main change.
