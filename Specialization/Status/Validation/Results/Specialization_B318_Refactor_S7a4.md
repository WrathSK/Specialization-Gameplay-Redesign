# B318.345 — S7a4 located carrier mutation mechanics

## Plan and Runtime Impact Contract

Authorized S7a, base B317.344/55106b4. No deployment/main/game launch, persisted shape or gameplay change. Extract only the repeated remove-before-add mutation loops of ResearchApply/Infrastructure/Chair into static CarrierSet.ApplyLocated. Every owner's original installed/preflight, eligibility/model, database validation, read-only report, health ownership and exact exit remain in place this slice.

Owners compute their desired bits and keep complete presence/location/IsPillaged preflight before mutation. Kernel checks existing location mismatch and calls the same NativeHealth helpers, then verifies each removal and each created carrier's presence/location/unpillaged status. Keep the original error tokens and per-success change counts. Apply/Chair pass the already observed removal plot; Infrastructure deliberately asks NativeHealth to read its removal location again, as before. Do not silently widen exact self-feedback suppression using a stale plot. No added caching, listener, registry, retry or timer. D4 own-pillage-only rebuild remains removed; actual building/district pillage still belongs to the owners. Infrastructure retired cleanup stays before new writes and is not merged into current-bit mutation.

T01/T03/T04/T05/T08: historical-source native-call/value differential under D4, wrong location replacement, preflight UNKNOWN, failed removal/create/readback/partial changes, exact health/sibling/idle and full shared-worker guards. Current D4 behavioral tests remain; the B317 exact-four-line source-diff test is a batch-specific frozen proof, not an invariant forbidding later authorized refactoring. It is not selected as a current B318 behavior gate; old frozen source/results are untouched. Further definition/observation/Industry kernel migration remains subsequent work.

### Machine validation evidence

- Stage/status: `S7a4` / `LOCAL_SIMULATION_PASS`; tests=129, passing=129, registered-open=0.
- Source: base `55106b4d8ca6cb8d1dc398377d83d62e44131b0a`; dirty=True; input SHA256 `25b6a393f636aaef04fbc5aaca56a836e37a21019fc7b563693c9a0fb2e744af`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7a4 --output local/refactor/S7a4-B318-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7a4-B318-first/closure.json`; SHA256 `3aec1931e80f9153f5b1be1de5a83d7ea22e588f2e66fdb45a6a446d58b43170`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 67; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S6b_actual_Store_full_guard_leaf_cost": {"after": {"leaf": {"Game.GetCurrentGameTurn": 7, "city.GetID": 24, "city.GetOwner": 24, "city.GetProperty": 9, "city.GetX": 34, "city.GetY": 34, "plot": 1, "workers": 1}, "stamps": 7}, "before": {"leaf": {"Game.GetCurrentGameTurn": 7, "city.GetID": 24, "city.GetOwner": 24, "city.GetProperty": 9, "city.GetX": 34, "city.GetY": 34, "plot": 3, "workers": 3}, "stamps": 7}, "scope": "actual Store/Flow/EF/Probe; plot and governor native doubles; no CPU/native-heap claim"}, "S6b_three_real_research_writers": {"after_worker_reads": 1, "before_worker_reads": 3, "carrier_writes": 0, "foundation": "explicit foundation/Stamp double; actual EF/DC/Infrastructure/Apply/Chair and SQL", "same_carriers": true}, "S7a4_located_differential": {"baseline": "55106b4", "includes_wrong_location": true, "native_objects": "doubles only", "owners": ["ResearchApply", "ResearchInfrastructure", "ResearchChair"], "same_values_order_native_presence_and_counts": true, "states": 5}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 198, "XML": 25, "package_files": 320, "modinfo": 345}
