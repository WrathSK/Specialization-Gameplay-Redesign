# B307.334 — Disable B271 timing probes on the stable candidate

Source base: main `25327e7`; isolated implementation commit `95310ac`. User authorized this narrow fix after reporting worse lag since B271. This is not a general performance fix or a develop promotion.

## Runtime Impact Contract

- `EventTimingDiagnostics.ENABLED=false` gates Start before trace allocation, shared observation state, native getters and event subscriptions. Both Gameplay and BackgroundRoutes UI use the same gate. A disabled Start clears stale scalar timing state and observer references; the right-click sequence action cannot re-enable it.
- No timing native callbacks are installed, including after the former six-turn window. PerformanceCounters sees no automatic timing accumulator; NetworkBridge sees no timing observer. Existing business event registration/order and the optional manually requested memory attribution remain.
- No new scan, consumer, timer, retry, native write, Property field, dependency, persistent schema or gameplay rule. Only two runtime code files and two build stamps differ from B271. InternalCarrierPillage.sql, Buildings_XP2 load order, original GC policy, CarrierHealthTrace, D3 Commerce records, OTHER labels and collector code are byte-identical to the base.
- This is a load-time disable. It takes effect after an approved package replacement with the game exited and a fresh game process; it does not remove callbacks from an already running B271 process. Existing native event costs and old business scans still exist. A/B lag causality and the magnitude of improvement remain UNKNOWN until the user's comparison.

## Local validation

`LOCAL_SIMULATION_PASS`:43 selected tests,0 failures/errors. Selection: new `test_b307_probe_disable`, B271 Diagnostics/Evidence/RealInputPillage/load order, B269 memory and B270 event scope. Actual Lua5.1 exercises default-off before all dependencies, both context start orders, stale scalar cleanup,12 turn transitions/6,000 worker and publish events with original callback order, disabled right-click, no automatic counter accumulation and retained manual counters. The original B271 diagnostic assertions are unchanged and run with explicit test opt-in.

Read-only engine DB -> disposable memory copy:4557 internal SPC target rows already have Pillage=0. Recreating only the pre-SPC XP2 state in that memory copy, executing the unchanged SQL and reapplying it confirms all4557 targets, idempotence and byte-for-byte row equality for non-targets.

One original B271 SQL test still FAILS its historical precondition that the external DB has zero SPC XP2 rows; the current DB already contains4557. Its assertion was not weakened and the failure is excluded from PASS. The independent loaded/fresh-copy test above provides current evidence. Full original failure transcript and selected results stay ignored under `local/hotfix/B307/`; these local files are not a permanent backup. Legacy failure SHA256: `bdcf9ed6756633d4bbe7f45cb1158c113a4eb65e39cd87a0118b90a2a5391b83`.

Reproduction: with test dependencies and explicit read-only DB configuration, run `python3 -m unittest test_b307_probe_disable test_b271_diagnostics.Diagnostics test_b271_diagnostics.Evidence test_b271_diagnostics.RealInputPillage test_b271_diagnostics.CarrierSQL.test_load_order test_b269_memory test_b270_event_scope` with `DevelopmentTests` on PYTHONPATH. Environment: CPython3.10.13/Lupa2.8; new/B271 runtime tests use Lua5.1, inherited B269/B270 use their authored backends.

Static compilation, XML/package closure and current context content/hash checks are recorded below after final stamping. The literal context CLI is develop-only; this candidate's hotfix branch is checked explicitly without changing the helper. No blanket context rehash, prior evidence rewrite, main merge or deployment is authorized by this result.

## User comparison and handoff

After separately approved merge/deployment: load a copy of the same B271 campaign from the same turn and perform the same actions/turn transitions; retain the original save. New TREASURY_POINT, TURN_EVENT_COUNTS, TIMING_NETWORK_VERIFIED and EVENT_ORDER records should be absent. Older Commerce/memory/carrier diagnostics remain. Compare responsiveness and turn duration; continued lag should lead to the user's planned playtest pause while develop refactoring completes. This bounded comparison adds no general cross-version save support or gameplay/native PASS.

- User decision: merge/main promotion and deployment require separate approval.
- User testing: performance comparison after activation; USER_GAME_TEST_REQUIRED.
- Primary next: forward-port only the implementation commit through Git into develop; retain S6d progress and remaining S6–S10 scope. No bulk promotion.

## Final static result

STATIC_CONFIRMED: {"Lua51": 189, "XML": 25, "context_content": "PASS", "literal_context_cli": "DEVELOP_ONLY_NOT_APPLICABLE_TO_HOTFIX_BRANCH", "modinfo": "334", "package_files": 312, "unchanged_other_runtime_files": 308}. All other308 runtime files, including D4 SQL and original GC/counter/collector modules, are byte-identical to main25327e7. Source/candidate is separate from liveB271.

## S0759 — Approved main merge and stable deployment

User approved PR7 merge followed by stable deployment and stop. PR7 merged normally; B307.334 from main19d51bd is deployed with312/312 source/live MATCH. B271.298 recovery package verified; no pending transaction. B271 A/B/C are disabled for the next game load; D4 and original gameplay/diagnostics remain. Actual lag improvement is USER_GAME_TEST_REQUIRED. No game launch or further refactor work. Receipt: `B307.334-19d51bd-stable-deploy.json`; source commit `19d51bd8cdb520af7d35f2eeade34fc86d8361f4`; package SHA256 `b9aa4ad7aeeae7a3584c5d8a9b0dfb6ca6f5918095789a46e3e87871cc026146`. Both worktrees retain the source-only forward-port; deploying develop was not authorized. Earlier candidate approval wording above is superseded by this explicit user authorization and completed transaction. Stop after recording; no native performance PASS.
