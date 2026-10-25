# B325.352 — S7d2 explicit UI queue-read causes

## Plan and Runtime Impact Contract

Accepted S7d/D4, base B324.351/d1cf0a3. Share one panel-local TimedProjectSelectionClient mechanism for the three separate project UIs: exact pending-intent permit, consume-before-getter, post-getter current-intent/turn/new-cause guard, nonrecursive drain and Close. Each UI retains its own selection, error text, timer/ACK presentation and request action. No project eligibility/completion/save/native irreversible policy moves to UI. No new game loop, timer or periodic retry.

An explicit Before or native CityProductionChanged/CityProductionQueueChanged/CityProductionUpdated(owner,cityID) grants a single read to an already-existing matching intent. Nine protected adapter callbacks are added (three clients × three related event names), removed by existing SafeAdapters.Close. With no exact pending city they do no qualification/clock/native lookup; no event creates an intent. The UI signatures are verified in the base ProductionPanel/CityPanel and native banner sources, with evidence limitations retained in Full_Turn.md section16. A size0/UNKNOWN followed by silent native recovery without any related event stays pending; this native delivery gap is USER_GAME_TEST_REQUIRED, not compensated by polling.

Getter UNKNOWN or OTHER consumes the permit without cancellation or rearm. Getter-time new facts invalidate the old result and preserve the next drain's permit. Getter-time ordinary/new selection or turn change cannot send or erase the new intent. BEGIN locks sent/clears its exact intent before native reentry; exceptions never auto-resend. Drain guard releases on presentation errors; Close invalidates in-flight reads and future drains. Cached view/revision/ACK reads remain lightweight. The pre-existing SYNC publish-count retries and startup availability work are deliberately next S7d3; do not deploy this intermediate package or claim D4 complete.

Workload T01/T02/T04/T05/T08: actual Store/controllers with native UI-shaped readers and real backend ACK/BEGIN, UNKNOWN/OTHER after 1000 idle publishes, exact-city recovery, unrelated/foreign events, multi-queue rejection, intent replacement, new fact during read, getter/send reentry, close/error/turn boundaries and actual adapter wiring/shutdown. The old silent queue-size transition assertions are frozen on exact d1cf0a3 UI source with original assertions unchanged and the current real dependency shapes; current tests demand a new relevant event. All S7d1 independent completion/UNKNOWN/Store tests remain selected. No deployment/main/game launch or native CPU/heap/UI rendering claim.

Independent review found two concrete issues before closure: a getter-time native change could send stale CURRENT; now any new permit invalidates that result. Empty-event path initially read player eligibility; now exact pending lookup precedes eligibility and clock reads. Both have explicit counterexamples, including all three real clients. Historical Claim fixture receives its actual sibling UI definitions and city Members iterator, not replacement assertions.

### Machine validation evidence

- Stage/status: `S7d2` / `LOCAL_SIMULATION_PASS`; tests=391, passing=391, registered-open=0.
- Source: base `d1cf0a35f52bbb7b1f5f0378a44f00f98ae149ae`; dirty=True; input SHA256 `026810f189a10db92b5cf13ba8d6c345f9cb11b48df5e2dc8a20eadfb05061ed`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7d2 --output local/refactor/S7d2-B325-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7d2-B325-first/closure.json`; SHA256 `5e91f3297f8f668671f24554e843aa491394fd5c68de10d3aacbed65cb3ba407`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 106; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S7d2_UI_queue_work": {"after_reads": [1, 1, 1], "baseline": "d1cf0a3", "before_reads": [1001, 1001, 1001], "idle_publications": 1000, "native_CPU_or_memory_claim": false, "owners": ["Claim", "Dialogue", "Engineering"]}, "S7d2_empty_event_work": {"clock_reads": 0, "events": 3000, "native_qualification_reads": 0, "new_intents": 0}, "S7d2_frozen_polling": {"current": "silent native-size change cannot grant new read permit", "no_historical_report_rewrite": true, "original_assertions": 3, "source": "d1cf0a3"}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 203, "XML": 25, "package_files": 325, "modinfo": 352}
