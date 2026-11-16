# B308.335 — Forward-port the B271 probe disable

User approved disabling only B271 timing probes while retaining the current main-based campaign and all other B271 behavior. Source implementation `95310ac` was cherry-picked as `988e94d` without conflict; no main/develop bulk merge or source copying. B307.334 is the separate stable candidate, B308.335 identifies this different develop runtime.

## Runtime Impact Contract

The load-time `EventTimingDiagnostics.ENABLED=false` gate executes before any trace allocation, native read, observation counter state or added event subscription, in both contexts. It clears stale scalar observation state/references. The existing right-click diagnostic request returns a Chinese disabled message and cannot re-enable C. Other Gameplay requests, original callbacks, PerformanceCounters, D3 records, GC coordination, carrier health, collector and InternalCarrierPillage.sql remain. No new automatic consumer, sampling scope, save schema, timer, retry or gameplay change.

The original B271 assertions run with explicit fixture opt-in. New tests cover disabled dependencies, both context startup orders, stale state,6,000 worker/publish notifications over12 transitions, native-read/trace/listener absence, callback order, right-click and original manual counters. Loaded/fresh SQL states use only a read-only external DB copied into disposable memory; original historical pre-SPC DB assertion remains unchanged.

Selected current source regressions and static/context gates are recorded below. Full machine artifacts stay ignored/local, not permanent backups. No local result proves native CPU, memory, save compatibility or user acceptance. Source instrumentation is now different, so old and new native measurements must label the build.

- User decision: main candidate merge/deployment remain separate; no new program decision.
- User testing: original final U5 remains; the optional main-based lag comparison is separate.
- Primary next: continue S6 scoped receiver discovery, remaining workers/capital/UI/target/network hot paths, then S7–S10. Preserve completed S6d and all accepted contracts.

## Local evidence

LOCAL_SIMULATION_PASS:20 probe/current B271 tests and109 current S6d composition regressions. The first20-test attempt had19 passes/1 configuration error because develop intentionally has no local DB config; supplying the explicit read-only DB setting resolved it without code/assertion changes. The legacy B271 pre-SPC XP2 assertion is excluded for the already-applied current database, as documented by the independent loaded/fresh-copy SQL test.

### Machine validation evidence

- Stage/status: `S6d` / `LOCAL_SIMULATION_PASS`; tests=109, passing=109, registered-open=0.
- Source: base `988e94d977baa7c7f97bdecffc1d13758edbbf40`; dirty=True; input SHA256 `425cc73e2cd41478a99583833efe7c1ec53f8bcfbf4c851d3334d298317598b5`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6d --output local/refactor/B308-probe-disable/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "e7c9f6186921ef5839135b274452d998782a710770ada6eb5d7c624b5f6fed3a"}}`.
- Full artifact: `local/refactor/B308-probe-disable/closure.json`; SHA256 `be4ec794ee7bcc63a3db5fde6c1ee38d56924acec372c99a5793d7ab2ba3f1c2`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 60; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (selected run): `{"S5d4c10_commerce_health": {"permanent_writes": 0, "repair_writes": 1, "thousand_idle_reads": 0}, "S5d4c11_SQL_health_budget": {"all_definitions": 1750, "full_level_scan": false, "ordinary_equal_plan_presence_reads": 0, "presence_reads": 7, "thousand_idle_reads": 0, "wanted_targets": 5}, "S5d4c9_receiver_health": {"receiver_facts": 1, "source_history_reads": 1, "thousand_idle_writes": 0, "unrelated_receiver_reads": 0}, "S6d_reverse_index_bound": {"capacity_failure": "UNAVAILABLE; original consumer scan fallback until new context", "edges": 2048, "native_reads": 0, "single_source_returned_targets": 1, "targets": 2048, "timers": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.


STATIC_CONFIRMED:196 Lua5.1 compilations,25 XML parses,319-file exact package including modinfo335; normal develop Context Lock check PASS.
