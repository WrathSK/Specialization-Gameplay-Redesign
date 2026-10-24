# B306.333 — S6d detached reverse dependencies

Source base: B305.332 `8bfe732`. LOCAL_SIMULATION / STATIC_CONFIRMED only. W0004 L3; T02/T04/T05/T07/T08 at the actual CultureNetwork/Standardization/Bridge/startup closure. No deployment/native PASS.

## Runtime Impact Contract

- Owner: each writer owns one private ReverseDependencies instance. It stores only scalar owner/target/source ID sets. It does not read native objects, interpret eligibility/provenance/reference, write carrier/Property state or subscribe to events. New helper is included and packaged explicitly; no startup ordering/dependency-contract change. Commerce's existing reverse mechanism is retained; no unnecessary migration.
- Publication: CN updates after successful record publication and removes only after actual reference/record clear (including destructive failure, missing city, experimental withdrawal and Store exit). Std updates after its existing sources commit and resets on successful reference replacement, missing city or confirmed exit. Failed planning/non-destructive writes keep the old record edges. Option A/retained aggregate sources, self and empty/UNKNOWN sources remain indexed by key even when their value is false or they contribute no current maximum.
- Scope: take a detached old-dependency union for every true changed source before any record mutation; add changed self and current topology's receiver matches. Existing candidate loops are retained, including CN old records and Std `not old` recovery. This slice removes repeated inspection of old source sets in warm selection; it does not yet claim removal of full city candidate enumeration or full topology traversal. Those must be narrowed with separate discovery proof.
- Bounds/failure: maximum2048 targets and65536 scalar edges. Replace validates and checks the total delta before mutating any old edge. Failure retains the old graph but makes queries explicitly UNAVAILABLE, never an empty-success set; a scalar `dependencyIndexError` exposes degradation without masking business errors or adding native counter reads. Remove cannot falsely restore completeness. This context then uses the original source scan, without an added topology prepass or automatic recovery attempts. A previously valid pre-loop snapshot remains complete for that loop even if a later Replace overflows; later lookups fall back.
- Work and compatibility: valid single-source query returns only that source's detached dependent IDs. No new timer, frame work, irreversible operation, save format, network fact promotion or rule change. Cold/owner-wide/turn/transfer/load discovery and recovery remain unchanged. This is bounded metadata reuse, not measured native CPU/heap improvement.
- Tests:15 new cases cover false-valued source membership, immutable copies, exact replacement/remove/owner scope,2048 warm targets, atomic target/edge/input failure with latched unavailable, actual CN/Std old edge disconnect and new edge addition, all-source/UNKNOWN/retained membership, Option A event recovery, unrecorded Std bootstrap, failure fallback equivalence, failed reference clearing/physical writing and false changed values. Existing real engine-shaped consumer assertions remain unchanged.

## Remaining boundary

Full machine artifact/transcripts remain local ignored outputs, with explicit source/environment/hash in the compact summary; they are not a permanent backup. Current received facts and provenance remain governed by their existing authorities.

- User decision: none.
- User testing: U5 source disconnect/reconnect, pending retention and native installed values.
- Primary next: S6 remaining scoped discovery and bounded hot paths, then S7–S10.

### Machine validation evidence

- Stage/status: `S6d` / `LOCAL_SIMULATION_PASS`; tests=109, passing=109, registered-open=0.
- Source: base `8bfe732e524d9b910cbd39f0c629ea28783f223c`; dirty=True; input SHA256 `61b551b8b4668be5ace9620089ef12da7a5b37c5409ac8dd7b724d3b2e7f55ff`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6d --output local/refactor/S6d-B306/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "e7c9f6186921ef5839135b274452d998782a710770ada6eb5d7c624b5f6fed3a"}}`.
- Full artifact: `local/refactor/S6d-B306/closure.json`; SHA256 `192790f1e21dcfc498bcdacfa76aee4180cd918d77e4a4e45baa3b1d83d07a87`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 60; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5d4c10_commerce_health": {"permanent_writes": 0, "repair_writes": 1, "thousand_idle_reads": 0}, "S5d4c11_SQL_health_budget": {"all_definitions": 1750, "full_level_scan": false, "ordinary_equal_plan_presence_reads": 0, "presence_reads": 7, "thousand_idle_reads": 0, "wanted_targets": 5}, "S5d4c9_receiver_health": {"receiver_facts": 1, "source_history_reads": 1, "thousand_idle_writes": 0, "unrelated_receiver_reads": 0}, "S6d_reverse_index_bound": {"capacity_failure": "UNAVAILABLE; original consumer scan fallback until new context", "edges": 2048, "native_reads": 0, "single_source_returned_targets": 1, "targets": 2048, "timers": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 196, "XML": 25, "package_files": 318, "modinfo": 333}
