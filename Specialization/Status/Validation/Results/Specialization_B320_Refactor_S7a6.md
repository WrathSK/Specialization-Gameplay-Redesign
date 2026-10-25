# B320.347 — S7a6 exact owned registries

## Plan and Runtime Impact Contract

Accepted S7a F11/F34/C019; base B319.346/84ac7ae. Extract only immutable names and exact-ID ownership mechanics. Registry copies only caller-validated scalar IDs/names; no new schema policy, native read, event, cache of cities/native handles or recovery path. Publish a replacement only after the owner's entire validation succeeds. Load-time invalidation of definitions must not clear last good health ownership. Existing CarrierSet.Define delegates its owned map to the same primitive.

AP/Infrastructure validated exact names feed exit, with the original static fallback before successful validation; installed presence/location/pillage reads remain in owner order. Chair validation remains atomic and its exit deliberately re-reads the current target catalogue without requiring full validation. Wonder validation supplies its exact exit/health roster; its single Buildings handle per observation/write and asymmetric fresh remove/add UNKNOWN handling are retained, rather than replaced with a superficially similar generic Apply. No eligibility, amount, persistent format, retirement, startup or event scope changes; no deployment/main/game launch.

Worst work stays the same carrier-bound loops (AP25, Infra4 plus existing tombstones, Chair catalogue*8, Wonder catalogue). Registry construction is definition-only; no automatic consumers or wider scans. T01/T03/T04/T05/T08: detached registry, duplicate-name/ID policy unchanged, atomic validation failure retains health ownership, exact/fresh exits, real four-owner historical differential including native calls/readback, malformed-definition isolation, Wonder unknown/failure/reentry/idle closure and previous carrier modes. New campaigns remain the final integration support boundary; this mechanical slice does not migrate saves.

S7a checkpoint: shared Define/Observe/Apply/Exit covers presence owners; located mutations cover Apply/Infrastructure/Chair; sequential IndustrySupport and exact owned registries cover remaining mechanical duplication. Owner-specific schema/observation/qualification/legacy policies intentionally stay outside the kernel, including Wonder's distinct write protocol and Chair's fresh exit roster. No claim that every writer should share one transaction policy.

### Machine validation evidence

- Stage/status: `S7a6` / `LOCAL_SIMULATION_PASS`; tests=178, passing=178, registered-open=0.
- Source: base `84ac7aeac3a4d161e03d179cb21ad0079d5d519f`; dirty=True; input SHA256 `2aff282e15d20e09eeaee640054fe1b3ea1398db580a5ad51bd48b46763ced3b`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7a6 --output local/refactor/S7a6-B320-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7a6-B320-first/closure.json`; SHA256 `b111b322eb205dfa9ec0abeec951cd8de01f6cf6e6304a398daee636351badaa`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 77; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5d4c8_exact_health": {"city_fact_reads": 1, "sibling_fact_reads": 0, "thousand_idle_extra_reads": 0}, "S7a6_Wonder_registry_differential": {"baseline": "84ac7ae", "same_single_handle_calls_exit_list_and_writes": true}, "S7a6_located_registry_differential": {"baseline": "84ac7ae", "owners": 3, "same_native_calls_values_write_counts": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 198, "XML": 25, "package_files": 320, "modinfo": 347}
