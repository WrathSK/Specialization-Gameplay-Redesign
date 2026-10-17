# B217 — Event-driven initial Expedition position confirmation

State: LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED. Source B217.244; live remains B216.243 until guarded deployment below.

## Authority and scope

The user approved the narrow repair proposed in [B216 native review](Specialization_B216_Native_Review.md), then explicitly prohibited timers for this position-confirmation path and requested event-driven updates. The initial uncommitted seconds-based draft was discarded before publication/deployment. No new wall-clock deadline, polling loop or event-count threshold handles initial placement.

Only `Mod/UI/ExpeditionSpyActivity.lua` behavior changes, plus package labels and direct tests. Training/capacity/source binding, Gameplay task/placement/reward logic, Store/permanent fields, Tourism, GC and native espionage remain unchanged. The previously validated native SLEEP/WAKE operation-confirmation mechanism remains intact after initial position agreement; task duration remains the accepted game-turn duration. This is not a migration of all historical activity handling.

## Implementation and lifecycle

Exact owner/unit/type/name and absence of a native Spy mission are checked before considering a position discrepancy. Only TASK_PREPARING/SLEEP, before any owned/requested sleep or prior confirmed position for this attempt, can wait for UI position visibility. Waiting keeps one session job and last coordinate sample; there is no ContextPtr update callback in this state. Existing GameCoreEventPublishComplete/UnitActivityChanged and exact-unit UnitMoveComplete trigger fresh reads. The new movement subscription is removed on shutdown.

Matching coordinates resume the existing sleep handshake; Gameplay still starts the task timer only after ASLEEP. A changed attempt/phase/owner/selection mirror cancels stale work. Wrong identity, unreadable coordinates, native mission, displacement after position confirmation, and running/recovery/release displacement remain protected failures. At LocalPlayerTurnBegin, fresh evidence is read once: if the initial position remains unresolved, ACTIVITY_POSITION_UNCONFIRMED_AT_TURN stops the attempt rather than carrying an unresolved transaction indefinitely. This is an event/lifecycle boundary, not a time or notification-count budget.

Existing collector-compatible N1_TASK lines record WAITING, CONVERGED, REJECTED or TURN_BOUNDARY_STOP with exact expected/actual coordinates, owner/unit and task key. They do not log each notification or introduce a new collector protocol. At most one WAITING and one convergence/stop line per initial wait; no new permanent ledger or global scan.

## Reproduction and local validation

The new actual-UI-module delayed-position test failed against unmodified B216: the first stale UI coordinate immediately generated FAILED instead of remaining pending. This reproduces a sufficient cause of the observed stop; it does not prove B216's native discrepancy was transient rather than persistent. Native logs must distinguish those outcomes.

191 targeted tests PASS after the event repair, including9 new tests. Coverage: movement/publication-driven convergence without Update callbacks, no early SLEEP/ACK, unrelated-unit event isolation, many notifications without arbitrary failure, unresolved turn-boundary stop and no later stale resume, identity/native-mission failure while waiting, attempt cancellation, running/recovery/release protection, post-confirmation displacement, unknown coordinates, collector compatibility, and actual Gate plus independently delayed UI view through completion/release. Existing OPERATION/SLEEP, recovery, fault, diagnostic and package suites remain included.

Two existing initial-position assertions now require the same protected failure at the player-turn boundary and assert no actions or diagnostic queries during the wait; all other identity/error assertions remain. Package version assertion is244. Evidence: ignored `local/diagnostics/B217/position-before.log` and `event-validation.log`. No whole-game regression or native PASS inferred.

## One minimal native check

Start the collector manually. Use a save before the failed 奇观巡礼, not the already HELD attempt (this patch does not silently revive held state). Select one valid wonder, start **奇观巡礼**, and confirm preparation proceeds to the ordinary task state. After its normal duration, confirm completion, return to the city centre and new Insight if that civilization/category was previously unused. Existing +4% Tourism evidence remains; rounding and numerical accumulation stay deferred, and WORKS requires no manufactured target.

If it still stops, stop there and provide the collector output. Expected/actual coordinates and whether CONVERGED or TURN_BOUNDARY_STOP occurred distinguish transient visibility from a persistent placement mismatch. No repeated cold-load campaign or performance test is requested.

## Deployment

Pending clean committed source, automatic game-exit check and existing receipt-bound transaction. No configuration change or game launch.
