# B361.388 — S9c5a bounded UNIT_TARGETS publication

## Plan and Runtime Impact Contract

Accepted S9/F25,D15; base B360.387/08d1771. Add only the fixed UNIT_TARGETS scope to PlayerActionReplies,with an independent8-slot ring beside ACTION8 and VIEW8,total maximum24 retained reply positions. Same epoch allocation/startup order and parent shutdown close all three original private instances. No generic serializer,automatic consumer,transaction authority or save data.

Gameplay admits explicit UNIT_TARGETS/epoch at the existing UNIT_TARGETS_READ boundary,invokes the original Refresh exactly once,and publishes its direct local return. Refresh still assigns the identical full DTO to UnitTargetSnapshot for legacy/DEV and internal save/restore readers. No-channel requests retain original behavior. ReadAtSite,global fallback and current-site/missing-hint scopes are unchanged. Current Marker UI is not migrated yet.

Projection whitelists stamp/mode/error,plots[{plot}],unknown[{cityID,reason}]. It discards plot cityID/cityName and arbitrary/native extensions; Marker does not consume those fields. Plain dense arrays and finite exact integer indexes/stamps are required. Two arrays together allow4096 rows; reasons/error allow20000 bytes each,mode128,with262144 total retained payload text bytes. These are new transport budgets,not pre-existing discovery scan limits: existing full discovery still visits actual player cities/districts without an added cap,and one city supplies at most one plot or unknown. Over-budget/malformed projection produces fixed TARGETS_UNAVAILABLE without fake empty/partial success. No truncation. Failed publication cannot overwrite earlier retained evidence; parent/child replacement prevents delivery into the successor session.

Work and lifetime: one bounded Lua-only copy of the already collected result,no additional native reads/enumeration/request. Worst retained target space is8 replies each<=4096 row tables and<=262144 text bytes,plus fixed metadata/ring indexes; this is a static bound,not a native heap measurement. Take/Discard/shutdown explicitly release it. Existing ACTION/VIEW capacities and lookup behavior remain independent. No new listener,timer,retry,GC policy,amount,qualification or irreversible operation.

T04/T05/T08:12 new focused tests cover fixed/detached projection,negative pre-stamp DTO,protocol/stamp/types/plain dense arrays,combined row/cumulative text overflow,exact4096-row boundary,cross-port same token and capacity,epoch/shutdown,once-only producer,legacy global,service reentry,explicit failure,and actual32-city collection plus internal site/snapshot preservation. All44 selected new+existing target/view assertions pass. The original S9c4a unsupported-scope assertion now uses OTHER because UNIT_TARGETS is the explicitly added fixed successor scope; unsupported rejection remains strict. Its two-port measurement is historical to that preparatory slice,not the current capacity claim.

The first actual-Store projection fixture incorrectly called Start without that isolated fixture's ExposedMembers; corrected to the real pure New factory,without changing runtime or native-work assertions. Independent read-only review of the three runtime files found no blocking issue and diff whitespace check passed. No deployment/main/game launch/native PASS. Next migrate Marker consumer,then remaining presentation/training/applied display/adjacency and S10; exact D7/D5 limits remain OPEN.

### Machine validation evidence

- Stage/status: `S9c5a` / `LOCAL_SIMULATION_PASS`; tests=909, passing=909, registered-open=0.
- Source: base `08d177175821fe5dee84b92cce31879c5ac909e0`; dirty=True; input SHA256 `76ca5899d6f395886c90942e649fe1fefe40f91fb82b98124d4963ca61b05944`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9c5a --output local/refactor/S9c5a-B361-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9c5a-B361-final/closure.json`; SHA256 `1aa32d97a5cbd14b9d536fcadacf3c82358cd25458541e60e8e57eff62e0181c`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 198; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9c5a_actual_marker_scope": {"cities": 32, "original_owner_city_enumerations": 1, "original_owner_district_enumerations": 1, "projection_extra_native_work": 0, "targets": 32}, "S9c5a_fixed_target_transport": {"UI_migrated": false, "extra_native_reads": 0, "ports": 3, "rows_per_target_reply": 4096, "slots_per_port": 8, "text_budget_per_target_reply": 262144, "total_max_slots": 24, "transport_limit_is_not_scan_limit": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 388}
