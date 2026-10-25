# B311.338 — S6g scoped Culture receiver discovery

Base B310.337/f712097. Stable/live/main remains B307.334. No deployment, promotion or native game launch.

## Runtime Impact Contract

Each accepted private Bridge view now builds one Culture scalar source-to-receiver reverse index using the existing bounded helper (2048 targets/65536 edges). It is replaced or discarded with that view, never keyed by historical versions. Capacity failure disables scoped copying only; complete accepted topology and effects remain valid. No additional native reads, events, timers, retries, persisted fields or business authority.

CultureNetwork snapshots old dependents before reading topology. A changed-city batch requests those targets plus current topology receivers. Bridge returns detached candidates and each selected receiver's FULL source set. Only explicit scoped success skips full records/recipient discovery; legal self membership is unchanged. Full owner/load/turn/transfer, cold/UNKNOWN/unavailable index and legacy adapter paths retain original full discovery. Std retains its required live census/unrecorded recovery behavior. Existing currentView epoch/signature/generation checks and input availability/provenance remain unchanged.

Work shifts from repeated all-records/all-Culture-graph discovery and copying to changed-source reverse edges plus candidate source rows. Index construction is O(E) once per new view; full Input provenance copies remain, so this is not a claim of eliminating every O(city) operation. Real reconciliation, D2 source retention, negative facts, readback, exact owned health and same-turn changes remain unchanged. T01/T03/T04/T05/T08: real Bridge Receive/view replacement and CN plus retained pending/negative/old edge/capacity/health tests.

## Validation and limits

Compare full compatibility adapter to scoped path on 37 actual fixture cities in two disjoint route components, instrumenting actual scalar table iterations and asserting identical final effects. New topology builds and native facts are not bypassed. All native city/district/events and Store/history values are explicit doubles. No CPU, heap, save-load or USER_GAME_TEST_PASS claim. Old whole-file/version-fixed tests are not relabeled as current package acceptance.

### Machine validation evidence

- Stage/status: `S6g` / `LOCAL_SIMULATION_PASS`; tests=110, passing=110, registered-open=0.
- Source: base `f7120970e909f153b760e929f0b93e96f8520025`; dirty=True; input SHA256 `89dfc38417ce3bd1ed16b03040541b17815c1b2ce557751bb49bcdddcb5cb4fb`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6g --output local/refactor/S6g-B311-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S6g-B311-first/closure.json`; SHA256 `3e97ca8dfeb2a01e596437f96b1beb23bf0dc0e8c0abdedf425905777a391062`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 57; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5c2_busy_refresh_budget": {"initial_captures": 1, "ten_reentrant_causes_additional_captures": 1, "thousand_idle_additional_captures": 0}, "S5d4c9_receiver_health": {"receiver_facts": 1, "source_history_reads": 1, "thousand_idle_writes": 0, "unrelated_receiver_reads": 0}, "S6d_reverse_index_bound": {"capacity_failure": "UNAVAILABLE; original consumer scan fallback until new context", "edges": 2048, "native_reads": 0, "single_source_returned_targets": 1, "targets": 2048, "timers": 0}, "S6g_Culture_scalar_discovery": {"after": {"edges": 3, "graph": 0, "records": 0}, "before": {"edges": 34, "graph": 34, "records": 36}, "cities": 37, "components": 2, "remaining": "new topology O(E) index build; Input full provenance copy unchanged; no CPU/native heap claim", "same_effects": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 196, "XML": 25, "package_files": 318, "modinfo": 338}
