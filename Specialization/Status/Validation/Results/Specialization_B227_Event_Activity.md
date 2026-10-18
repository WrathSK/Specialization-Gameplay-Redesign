# B227 — Event-driven Expedition activity and unarmed startup exit

Status: LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED. Source B227.254 / modinfo254. Deployment is recorded separately in Status.

## Approved boundary and evidence

User approved event-driven processing, reliably unarmed startup exit and necessary diagnostics, with no new timer. Capacity, source binding, permanent Insight, reward semantics, Store schema and GC are unchanged. No site movement or native espionage mission is introduced.

[B226 native evidence](Specialization_B226_Native_Review_Advisor_Handoff.md) contains two accepted WORKS requests remaining TASK_PREPARING, without captured Activity evaluation/ACK. The Stable Advisor review in `Specialization/Reports/Advisory/Expedition_Task_Lifecycle/Expedition_Task_Lifecycle_Review.md` identified the hidden-context refresh dependency and missing unarmed liveness exit. Its independent older native-denial finding remains open; publication/event delivery does not override native eligibility.

STATIC_CONFIRMED: B226 Activity only scheduled RequestRefresh; its hidden InGame context depended on refresh delivery to evaluate requests. A local counterexample using exact source `45b28fb:Mod/UI/ExpeditionSpyActivity.lua` and actual bridge fixtures withheld frames:21 publications,0 ARM requests,0 Sleep requests,0 ACKs. This establishes the code dependency, not universal engine behavior for every hidden context. B226 constructor/continuous trace records support this as the current regression; logs alone cannot exclude pre-append diagnostic errors.

## Implementation

- Real publication, exact-unit activity/movement/operation events, local turn and initialization run one Activity pass. Nested callbacks only mark pending; a subsequent real callback resumes. No recursive drain, SetUpdate, RequestRefresh or frame handler in the hidden Activity bridge.
- ARMED still requires confirmed Gameplay Store readback before one Sleep request. A writer cannot acknowledge its own native result in its call stack. Fresh exact-unit reads and native guards remain authoritative; persistent intent is not SLEEP evidence.
- Pending native readback uses subsequent events. A later local-player turn checks the current state before reporting unresolved operation/recovery/release failure; ownership uncertainty stays protected. The previous quarter-second poll/ten-second deadline is removed, not supplemented.
- Gameplay independently expires TASK_PREPARING/SLEEP only when unowned, unconfirmed, without task clock, and its exact Store envelope reads back unchanged. Fresh source, destination and named-unit/position checks precede the saved return to ARRIVED. No native wake, reward, quota consumption or historical deletion. Failed read/write or changed references remain held/protected.
- The expiry observation is a single replaceable session key/turn. New attempts start it at admission. Loaded unarmed attempts receive a fresh observation interval; LoadScreenClose itself cannot expire them. No new saved field or inferred historical start time. Late ACKs fail exact attempt-key matching and cannot advance a replacement attempt.
- Existing bounded trace records ACTIVITY_EVENT (entry/core-busy/mode), ACTIVITY_START/FAILURE/RELEASE, final GATE_RESULT and ACTIVITY_UNARMED_EXIT. Selected idle action eligibility prints only on signature changes. No new sampling loop or persistent log system.
- New bilingual key: `LOC_SPC_EXPEDITION_SPY_ACTIVITY_START_EXPIRED`. Ordinary visible UnitPanel deferred rendering remains native-owned; it does not drive task progress.

## Local verification

353 targeted tests PASS:234 Gate/Store/mission/UI/current-facts tests plus119 pending/recovery/diagnostic/rejection/position tests. Python3.14 / Lupa2.8 Lua55; the configured external Gameplay DB is opened read-only where required. No gameplay stress or full historical suite.

`DevelopmentTests/test_b227_event_activity.py`:19 differential tests, explicitly no frames and no automatic fixture publications; covers one pass per callback, durable arm ordering, busy core, denial, OPERATION, later-turn protected failure, unowned manual Sleep, owner/shutdown, trace, next-turn unarmed exit, late ACK/new attempt, corrupt Store/readback, load observation grace, changed reference and combined completion/release.

Existing lifecycle fixtures explicitly supply later native publications for ordinary tests. They are not evidence that the engine guarantees that timing. B227 differential tests disable that convenience and provide each event individually. Nine superseded B225 frame-scheduling expectations are replaced by the B227 suite; independent B225 completion/Works/sale regressions remain. Previous wall-clock tests now exercise event/turn boundaries, retaining ownership/no-retry/failure assertions. Frozen historical results are unchanged.

Context/schema/runtime integrity and helper selector self-tests PASS;7 added/changed Markdown links/anchors resolve; diff whitespace check PASS. A whole-file historical Status link scan encounters a pre-existing retired N1 anchor; this batch does not rewrite historical navigation.

Validation does not establish native event eligibility, performance improvement or universal task reliability. B226 Great Work refresh acceptance is retained; Culture Network native yield/source withdrawal remains pending.

## Minimal combined native check

Use the existing automatic collector manually; do not open P0 to make the task progress. One continuous session:

1. With an arrived, idle Expedition and an available category, open **任务**, select the category and start. Confirm task occupancy without an extra manual **休眠**; logs must show arm/readback and TASK_RUNNING.
2. Complete its normal two turns. Confirm one Insight award, task/relocation controls return, and choose another eligible task or **派遣到新城市**. This tests release and reuse, not just one-shot startup.
3. If a startup fails naturally, stop repeating it. Keep the log; a reliably unarmed attempt should return idle at the next normal player-turn boundary. Do not force repeated failures or replay old save/load loops.

The existing Culture Network specialist-yield/source-withdrawal check may join when its prerequisites are available. No repeat of accepted Great Work sale refresh. No new Design decision required; native denial remaining after this repair must be classified from event/guard/final-state evidence rather than another blind retry.
