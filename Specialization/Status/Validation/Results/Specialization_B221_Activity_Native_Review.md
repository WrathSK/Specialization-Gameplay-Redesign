# B221 — Native pre-request SLEEP denial

**USER_GAME_TEST_FAIL for this PLACES task start; diagnostic capture succeeded.** User reports remaining blocked by a unit needing orders. No current PEOPLE retest was performed. Runtime baseline is the recorded B221.248 source `5662871`; this review does not deploy or modify runtime.

## Captured sequence

Ignored collector session `session-20261017T181722Z-2e8cbc`, turn51:

| UTC | Evidence | Meaning |
|---|---|---|
|18:20:26|READ ARRIVED|Bound team available before task request|
|18:20:28|PLACES execution=CENTRE actual20,13; evidence18,13; TASK_PREPARING|Target validation passed; no task-site relocation|
|18:20:28|ACTIVITY_START: activity1797587246 equals AWAKE; ready=true; exact expected/actual20,13; eligibility=false / DENIED|The activity/identity/position readers succeeded; native SLEEP eligibility returned false|
|18:20:28|ACTIVITY_FAILURE: guardStatus=DENIED; ACTIVITY_SLEEP_NOT_ALLOWED; requested=false; attempted=false; READ_OK|The real guard independently denied SLEEP before any native SLEEP request or ARMED handshake|
|18:20:28|ACTIVITY_READBACK_STOP; HELD|Existing failure handler terminally held the team; taskStart was never assigned by this path|

No transport gap spans these events. `alerts:none` concerns the collector's existing population/cost alerts, not mission acceptance. Ring records6/7 provide the actual startup/failure distinction. The legacy gate error includes a local engine traceback path; the raw file remains ignored and is not reproduced in this report.

This rules out a position mismatch, unreadable activity, pre-request OPERATION and post-request OPERATION timeout **for this attempt**. Ready=true is not permission to perform every operation. It does not establish why the engine denies SLEEP.

## Comparison with the working paths

- [B194 no-reward native result](Specialization_B194_Expedition_Pending_Activity_Native_Review.md), source `d447ff5`: task startup had no placement and used the same exact database-hash SLEEP permission check before requesting it. Its native running/completion evidence remains valid; rewards do not implement Sleep.
- [B214 PEOPLE success](Specialization_B214_Expedition_Task_Start.md#native-continuation--2026-10-16), source `2939197`: `relocate` immediately returns when already at the requested centre. In that case it does not call RestoreMovement, PlaceUnit or FinishMoves. Thus moving to the same centre was not a hidden required normalization for this path.
- B220 removes PLACES/WORKS task placement, but does not change the SLEEP permission API or its denial branch. Current task categories converge on the same activity bridge. No current native PEOPLE failure or PASS is inferred.
- A two-case local counterexample used actual B214 and current Gate/activity sources with the existing integration fixture and only native SLEEP eligibility set false. Both produced PEOPLE → HELD, modeNONE, ACTIVITY_SLEEP_NOT_ALLOWED, zero SLEEP requests, no taskStart and native AWAKE. **LOCAL_SIMULATION**, not a native explanation: it shows the failure handling already existed and category/movement removal alone does not explain native denial.
- Current loaded read-only DB: SLEEP/SKIP are visible zero-turn operations without a tech/civic prerequisite. Expedition retains Spy/IgnoreMoves/Stackable flags. No SQL prerequisite newly explains the denial. Native permission internals remain unknown.

## Confirmed handling problem and missing evidence

Current Gate accepts TASK into PREPARING before the UI activity check. A clean negative permission result with no request is routed through the same FAILED → hold path used for ambiguous executed operations. `activityPending` is cleared and mode becomes NONE, but phase remains HELD; CanOpen and idle controls exclude HELD. Native activity stays AWAKE, so a unit-needs-orders blocker can coexist with unavailable custom controls. This is an unnecessarily terminal response to a proven pre-request rejection, separate from the engine's reason for denying SLEEP.

The native `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua` lines673–702 obtains a second result from CanStartOperation and renders `UnitOperationResults.FAILURE_REASONS`; the existing bridge discards that second value. B221 records the boolean/error distinction but not that engine explanation. The public Lua/DB sources inspected do not expose the internal SLEEP predicate. Do not claim a denied boolean proves remaining moves, plot occupation, Spy classification, save corruption or event timing.

## Proposed narrow next batch — not implementation authorization

1. Separate clean pre-request rejection from uncertain/executed activity failure. Only an exact current attempt with verified identity/position, no SLEEP request, no owned/pending native operation and reliable state confirmation may unwind its own PREPARING intent to ARRIVED. Do not wake, erase history, automatically clear existing HELD saves, waive position checks or convert UNKNOWN into success. Preserve terminal protection once a request may have occurred or source/store/reference evidence is unreliable.
2. At the existing permission read, preserve bounded native FAILURE_REASONS plus operation hash/type and explicit unavailable/empty-result labels. Compare the same unit's click/admission sample with the actual guard if needed to identify a phase-dependent denial; use existing action/publication boundaries, not timers, repeated requests or all-unit scans. Preserve current collector and record limits. This is a missing diagnostic surface, not proof of a repair to the engine predicate.
3. Local cases: clean denial yields idle/no reward/no task clock; request-before-error remains protected; duplicate/stale/changed references cannot cancel a later attempt; successful owned sleep/completion/release unchanged; missing native result remains UNKNOWN. No automatic new game test now. Any later one-attempt native gate must be justified by the concrete repair or the missing native reason and captured automatically.

Neither force-requesting denied SLEEP nor restoring PlaceUnit as an undocumented activity reset is recommended. Increasing waits would not address this pre-request denial. Do not substitute a native espionage mission or alter capacity, binding, Insights, GC or task duration.

## Evidence preservation and checks

Raw records stay ignored at their original collector path. SHA256:
- `records.log`: `dbfcb5c0a4b53eaca7c7777d9e68bf240d09f678d76a939eecde0b813b47d023`
- `events.jsonl`: `4476b2924a75c38ab6eb57854226f9b4036630fa5e0262df0dcad6f250782449`
- `summary.txt`: `b408e76f210d6804f826afac70868353c1c596855242acc05d4bd1c6c071eb43`

Read scope: current Gate/activity/UI helper, B194 and B214 exact sources/results, native UnitPanel SLEEP operation presentation, selected loaded DB rows and the submitted collector session. No game launch, live Lua query, gameplay implementation, test-file edit, deployment, main or configuration change. Context/selector/link/diff/publication checks are run for this documentation checkpoint.

User decision: review the proposed narrow admission/failure-reporting batch. User testing: none requested now. Primary next: wait for implementation authorization; no speculative repair or repeated blind test.
