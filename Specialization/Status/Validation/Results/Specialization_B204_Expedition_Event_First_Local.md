# B204.231 — event-first Expedition confirmation

2026-10-11. User approved the [B203 event-first repair proposal](Specialization_B203_Expedition_Name_Recovery_Native_Review.md). **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED**. This is a confirmation/feedback repair, not a training or binding redesign.

## Applied change and ownership

Production completion and the exact saved training reservation already establish NAMING. The independent UI observer now attempts the real native-name read immediately at initialization and on the existing publication, load, local-player-turn or exact-team-selection wake-up. It no longer waits for a frame callback before its first read. If the native facts are READY, it sends the existing NAME request once; only the unchanged Gameplay Gate can accept the exact source/unit/name and persist CREATED.

A frame callback is installed only while a native read or acknowledgement remains pending. Existing limits remain: three readiness attempts, ten seconds per attempt with 0.25-second deferred checks, and a separate ten-second acknowledgement window after submission. These elapsed-time limits use delivered UI update deltas, not a new wall-clock scheduler. Event wake-ups can read a pending team immediately even when frame delivery is withheld. Ordinary publication cannot restart an expired attempt; exact selection/load/local turn may restart only an unsent PENDING attempt within its budget. Unknown request outcomes, invalid identity and terminal errors do not replay. A later exact authoritative CREATED/name result can establish success without another write.

Scope is one current training team. The observer owns one disposable job/status record, its update callback and its event subscriptions. No diagnostic history, persistent field, city scan, additional GC or P0 writer is added. Repeated unchanged stages do not republish/log; a pending publication burst may still perform one current native read per wake-up. This is not a performance claim. Reentrant notifications, replaced jobs and shutdown are checked before submission. A presentation-notification exception is reported once per observer session and cannot prevent the first native read.

Training costs/formula, capacity, queue reservation, reliable source binding, Store schema, native travel and no-reward task behavior are unchanged. The independent observer supplies evidence to the existing validator; stage feedback cannot authorize an action. P0 READ remains read-only for normally trained name confirmation. Selection auto-opening remains optional/non-blocking.

## Player feedback

The ordinary disabled action tooltip now distinguishes: observer not initialized; initialized but no matching team observed; reading; native facts pending with a specific reason; name checked and awaiting binding confirmation; bounded wait ended; terminal failure. The status is matched by owner, unit ID, team key and training token. A loaded/initialized marker and stage transitions also appear in the existing Lua log, so another failure can be located without assuming that waiting means the observer ran.

New localization pairs under `LOC_SPC_EXPEDITION_SPY_NAME_`: `NOT_STARTED`, `NOT_OBSERVED`, `READING`, `CONFIRMING`, `RETRY_WAIT`, and `REASON_UNASSIGNED/UNIT/OFFMAP/ACK/RETRIES/READ/OBSERVER` (12 new keys). Existing `PENDING` gains a reason argument; existing `STOPPED` is reused. English/Chinese keys and placeholders match. No button, icon or independent panel is added.

## Local validation and evidence limits

**478 distinct targeted tests PASS**: the prior 457-test Expedition closure plus 21 new tests (including three wake-up subcases). Actual observer, native reader, Gate and Store run against mocked native APIs. New cases cover event-only ready/pending/ack transitions with frames withheld, saved NAMING at initialization, missing off-map facts, collision/source rejection, repeat/reentrant notifications, UI-notification failure, late acknowledgement, uncertain send, native name changing before acceptance, stale callbacks, shutdown, idle behavior and exact-token feedback. Existing queue/cost/cap, persistence, source, travel, task/activity and ordinary-Spy isolation tests remain included. Old fixture calls now tolerate the absence of a callback after synchronous completion; no original source/cap/timeout protection was removed.

Retained Lupa 2.8/lua55 and Python 3.14 were used; no dependency installation. The configured current external gameplay DB was read only and copied into memory. Package SQL/localization and XML checks passed: 13 touched localization pairs, unchanged action registration and unchanged package file set (217 declared files plus modinfo = 218 runtime files). Context/schema/selectors and reviewed hashes PASS (218 runtime files, 633 guarded files); 335 affected Markdown links/anchors PASS; diff whitespace/scope checks PASS. Frozen Status history is byte-unchanged. Raw output, the exact test runner and checksums are retained in ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B204/local/`.

B203's native failure remains recorded. The local counterexample proves that B204 no longer requires frame delivery for an event-ready confirmation; it does not prove that missing frame delivery caused the user's native failure. Native observer loading, current engine facts and this repair's end-to-end result remain unverified. No save migration, Design change or broader Expedition acceptance is claimed.

## One minimal native test

1. Use the existing pre-completion test save and finish normally training **人文考察团**. Keep P0 closed through completion and selecting the new team. Click **派遣到新城市** explicitly; it should be usable without opening diagnostics. This tests the repaired automatic confirmation path, not selection auto-opening.
2. Dispatch to the existing legal target and confirm arrival with the original source. Only afterward, if needed, open **人文考察·验证 → 刷新报告** to inspect that source. This checks that the new confirmation still feeds the established binding/travel path. No repeat save/cold-load or no-reward-task sequence is required.

If the button remains unavailable, capture its tooltip once; its exact stage/reason is the evidence needed. Do not wait indefinitely, repeatedly create teams, or use P0 to make this test pass. Existing B202/B201 scoped evidence is inherited where unchanged.

User decision: none. User testing: this one normal-training → dispatch/arrival session. Codex next: guarded deployment under standing W0003 permission if automatic exit/hash checks permit, then review native evidence. Reattachment/repeat tasks, broader civilizations, N2/N3/U2 and rewards remain held.

## Deployment

Source B204.231 / modinfo231 is locally complete. Last verified live remains B203.230, source `aec8c41`, receipt `B203.230-aec8c41-playtest.json`. Source completion is not deployment; the guarded transaction and receipt will be recorded here if completed.
