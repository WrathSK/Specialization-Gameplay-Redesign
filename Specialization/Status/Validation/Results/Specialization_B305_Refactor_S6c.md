# B305.332 — S6c minimal shared anchor facts

Source base: B304.331 `f12d3ce`. LOCAL_SIMULATION / STATIC_CONFIRMED only; W0004 L3, scoped T02/T03/T04/T05/T07/T08. No native or deployment claim.

## Runtime Impact Contract

- Owner and scope: `SpecialistSupport` captures only the requested city's first-anchor raw state. Indexed CityDistricts is the already-used native contract; legacy profiles without it retain their old batch traversal. This never calls DistrictCompleteness or enumerates ordinary-building definitions. The four existing consumers keep their policy, formulas and carrier writes; Housing continues its independent tier sample.
- Shared phase: EffectiveFacts `Inspect` provides a private anchor reader beside workers. State and geometry are separate scalar DTO parts, with parent row, owner/city/full reference stamp, EF write generation and FactChanges instance plus owner/city versions. RuntimeWork uses the same guarded local reader outside shared phases; project forwarding works both inside and outside. No native object or callback survives the synchronous projection/cache. No additional native events, startup dependencies, timer or retry.
- Ordering: confirmed owner/city mismatch returns before type/state getters; confirmed type/family mismatch returns before completion/pillage; confirmed incomplete/pillaged returns before unknown ACTIVE. Coordinates are requested only by GPP/Industry at their former decision point. Support/Housing are not held by unrelated coordinate failure. Missing anchor remains confirmed ineligible; failed enumeration/state/geometry remains UNKNOWN. Typed changes and real writes invalidate samples, and exception/reentry release is guaranteed.
- Bounds/cost: at most2048 scalar state/geometry parts per phase and at most8 simultaneous raw captures shared with workers; overflow is fresh without evicting warm entries. GPP's own255 guard is still checked after a shared hit. Missing legacy plot GetIndex uses its original fresh worker path. Geometry can require a second city-local indexed lookup; it is counted, not hidden. Actual no-write Support/Housing/GPP composition reduces state samples3→1 and indexed lookups4→2 with equal carriers and0 writes. This is scoped work evidence, not a native CPU/heap claim or a claim that D itself no longer reads district metadata.
- Compatibility: Industry's raw-anchor reference delegates to the same serializer and preserves exact bytes/token source. No Properties, saved shape, qualification, money or transaction rule changed. Future worker consumers (Commerce/Development) remain separately bounded work; no claim that every S6 obligation is complete.
- Proof:16 new cases cover partial negative facts before unknown getters, optional geometry failure isolation, active UNKNOWN after confirmed invalid anchor, missing/repair, double epoch/service recreation, actual writes, geometry reentry, detached/expired readers, scalar retention/capacity, actual three-writer composition, cached GPP limit and legacy GetIndex compatibility, and actual Industry outside-phase reference consistency. Inherited original assertion suites remain unchanged.

## Remaining boundary

Machine artifacts and transcripts are ignored local outputs; a path/hash is not a permanent backup. Final native acceptance remains U5. No new blocking native question was found.

- User decision: none.
- User testing: U5 integrated anchor pillage/repair, specialist reassignment and installed yields.
- Primary next: continue S6 reverse dependencies and remaining bounded hot paths, then S7–S10.

### Machine validation evidence

- Stage/status: `S6c` / `LOCAL_SIMULATION_PASS`; tests=177, passing=177, registered-open=0.
- Source: base `f12d3ce1c478a9faf1df28b0adceb92aaa443ae1`; dirty=True; input SHA256 `36b7d0063f795c77a34ca9ae3d9b23cbc322d49af90cbaa220f90322e395a50b`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6c --output local/refactor/S6c-B305/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "589ba3db7f4b927ab1ff478a9ccbb60ebadfb6fc9fb1cbfabf332955644054f2"}}`.
- Full artifact: `local/refactor/S6c-B305/closure.json`; SHA256 `f37af9e8b99f103d19790d9859d00ad96d367dcb55402f041b01a570efaa530f`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 58; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S6c_actual_support_housing_GPP": {"foundation": "actual EF overlay plus explicit foundation/Store-stamp doubles", "geometry": "one separate city-local lookup included; full D census not used for anchor", "independent_city_index_reads": 4, "independent_state_samples": 3, "owner_district_enumerations": 0, "same_carriers": true, "shared_city_index_reads": 2, "shared_state_samples": 1, "writes": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 195, "XML": 25, "package_files": 317, "modinfo": 332}
