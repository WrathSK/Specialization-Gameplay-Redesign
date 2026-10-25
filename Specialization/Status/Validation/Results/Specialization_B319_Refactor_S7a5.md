# B319.346 — S7a5 sequential Industry support carriers

## Plan and Runtime Impact Contract

Accepted S7a; base B318.345/6e8db27. No deployment/main/game launch, save schema, amount or eligibility change. IndustrySupport is intentionally not converted to the other owners' all-bit preflight/remove-before-add ordering: it originally reads and mutates each bit -1..7 in sequence. Add only this explicit mechanical ApplySequential variant to the exact CarrierSet. Keep same Buildings handle for each bit's read/write/readback, per-success counters and partial writes on later UNKNOWN/error.

The dense descriptor list carries negative food key -1 and bits0–7 without ipairs map loss; the same list supplies immutable lazy definition resolution, health Owns and exact Store exit names. Observe handles existing read-only reporting. No current-city presence is retained by the helper. BASE sampler, reference checks, callbacks, pending/armed/deferred queues, retry budgets, startup, real anchor/pillage rules, retirement and withdrawal count are unchanged in IndustrySupport. No new native reads, event listeners, timer or periodic scan.

T01/T03/T04/T05/T08: raw sequential order/late UNKNOWN/partial success/key -1; historical-source actual Industry/UI/BASE differential including zero and nonzero adjacency, same-turn changes and withdrawal; retained receiver reentry, failed/equal-value availability recovery, exact health, unknown holds and idle budget. Other CarrierSet modes and located owner closure remain protected. Remaining IndustryWonder and owned-definition consolidation follow separately; no blanket claim that every carrier writer is migrated.

Allocation tradeoff: this extracted mode creates one wanted map, one result array and nine call-local row DTOs (11 small tables per visit/report) where the original Industry loop used scalars. Retention is still zero after the call; this batch claims mechanism consolidation and identical native calls, not reduced Lua allocation or CPU time. A future measured optimization can remove result-row allocation without changing sequential semantics.

### Machine validation evidence

- Stage/status: `S7a5` / `LOCAL_SIMULATION_PASS`; tests=157, passing=157, registered-open=0.
- Source: base `6e8db27b442ed3e245b888010b17dd178f354366`; dirty=True; input SHA256 `bb5f3396a783584296cd6d50ddc5eab80d356b545e1015bcb99586f517dd4bab`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7a5 --output local/refactor/S7a5-B319-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7a5-B319-first/closure.json`; SHA256 `5d8787e7edbe74493bb8658fa1339f9b3fcc7f7b3b50d81fa22ab8db0b2829c4`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 71; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5d4b1_role_mark": {"city_visits_at_mark": 0, "native_notifications": 44, "native_owner_listeners": 1, "scoped_deliveries": 1, "thousand_idle_extra_deliveries": 0}, "S7a5_Industry_differential": {"BASE": [6, 0, 255, 1, 4], "baseline": "6e8db27", "idle_extra_writes": 0, "native_source": "actual IndustrySupport/IndustryRefresh/SampleLifecycle with native doubles", "same_values_native_calls_writes_changes_and_sends": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 198, "XML": 25, "package_files": 320, "modinfo": 346}
