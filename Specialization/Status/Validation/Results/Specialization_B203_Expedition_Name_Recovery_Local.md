# B203.230 — panel-independent training name confirmation

2026-10-11. User approved the [B202 repair proposal](Specialization_B202_Expedition_Training_Native_Review.md). **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED**. No gameplay or source-binding redesign.

## Applied boundary

The normal-training observer now initializes through the same UI lifecycle entry used by the established activity bridge. It owns one team-keyed transient record and, only while confirming, one update callback. Publication/load/selected-team/player-turn events can discover NAMING without opening a window. The first wait is10 seconds, sampled at0.25-second intervals. Only unsent PENDING readiness may retry on load/local-player-turn/exact-team selection; at most3 attempts per observer session. Ordinary publish bursts do not restart a timed-out attempt. No idle frame updates or city scan is added.

Once NAME is sent, a separate10-second acknowledgement window applies. Unknown send/ack outcomes and invalid identity stop, retain capacity, and do not replay. A later exact authoritative CREATED transition with the expected name can establish completion without replay. A reply with no error alone cannot establish success. Native reads and UI notifications are followed by job/identity rechecks; stale callbacks cannot send for another team. Shutdown removes owned subscriptions and clears only transient diagnostic state. Saved NAMING can start a fresh observer on cold load; no new persistent fields or migration.

The existing Gameplay NAME validator still verifies source reference, exact unit/owner, current native name/pool and collision evidence. Gate snapshot adds the existing trainingToken only as a diagnostic discriminator; capacity, source, schema, queue, travel and task writers are unchanged. Normally trained READ replies no longer invoke the diagnostic window's separate name-confirmation writer. Legacy explicit prototype CREATE/read naming remains available. P0 is therefore not the normal-training recovery mechanism.

Normal unit-action tooltips distinguish pending, bounded wait and stopped/error, keyed to the exact team. New localization pairs: `LOC_SPC_EXPEDITION_SPY_NAME_PENDING`, `NAME_WAITING`, `NAME_STOPPED`, `TRAINED_COUNT` (same prefix). Trained-team reports say city-trained instead of the stale free-prototype label. Selection auto-opening remains non-blocking; no new task/UI capability is added.

## Validation and limits

**457 distinct targeted tests PASS**, the existing23-module B202 closure plus `test_expedition_training_name_recovery` (20 new cases). Actual Lua observer/Gate/Store/UI fixtures cover late readiness, three-attempt exhaustion,100-event bursts, exact selection, absent/stale/wrong-owner acknowledgements, delayed authoritative success, invalid/read/send failures, reentry, new generation, shutdown, cold-loaded NAMING, source loss, ordinary action feedback and P0 READ without NAME. Existing normal training, persistence, activity, arrival/task and ordinary-Spy isolation tests remain in the closure. Local success does not prove native event delivery/rendering.

The retained Lupa2.8/lua55 environment was found at `/tmp/spc-l2c-python`; use `PYTHONPATH=/tmp/spc-l2c-python` with the existing Python3.14. This resolves the previous review's unavailable-environment observation; no dependency installation or historical evidence rewrite. The external current gameplay DB is read-only and copied into memory. Its B202 training marker already existed; fixture setup now removes only this package's exact Unit/marker/prerequisite definitions in memory before applying the same SQL. All original comparison assertions remain; no external DB or SQL behavior changed. Modinfo expectation updated to230.

Raw local result and SHA256 are in ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B203/local/`. Context/schema/selectors, package SQL/localization/XML, changed Markdown links and diff checks are separate static checks. The exact initial B202 native failure trigger remains UNKNOWN; the observed panel dependency and provable terminal retry gap are addressed, not retroactively diagnosed as a measured timeout.

## Minimal native delta

1. Use the normal city production **人文考察团** entry in the supported test civilization. Keep P0 closed from training completion through selecting the new team. Allow a brief identity-confirmation wait; **派遣到新城市** should become usable. If it says native name not ready, reselect once; do not repeatedly create teams.
2. Dispatch through **派遣到新城市** and confirm arrival with the original source. You may open **人文考察·验证 → 刷新报告** afterward to inspect it. Stop and capture the ordinary tooltip if confirmation stops. No repeat queued-save/cold-load or no-reward-task campaign is required for this delta; inherited B202 results remain scoped.

User decision: none. User testing: this single panel-independent training/arrival check. Codex next: guarded deployment under existing authorization when automatic game-exit/hash checks permit, then review evidence. No later Expedition implementation authorized.

## Deployment

B203.230 / modinfo230 **DEVELOP_ACTIVE**, source `aec8c412ac087dce79f071f850d7f9a224215c67`, receipt `B203.230-aec8c41-playtest.json`. Fresh automatic OS exit checks before both guarded switches; source/runtime218/218 MATCH, B202/stable recovery hashes verified, no pending transaction. Main and game configuration unchanged; no game launch or native PASS. The single native delta above is next.
