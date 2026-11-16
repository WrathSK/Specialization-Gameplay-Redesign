# B315.342 — S7a1 presence-only carrier kernel

## Plan and Runtime Impact Contract

Accepted S2–S10; base B314.341/77b8c14, U3 local checkpoint complete. No deployment/main/game launch/persisted shape or gameplay change.

First kernel slice: ResearchSupport and Lv2Housing only. Static CarrierSet Define/Owns/Observe/Apply/Exit keeps an exact ordered descriptor list. Definition resolution remains lazy and atomic; health Owns never resolves database rows. Housing uses dense descriptors with explicit keys 0–8. Each owner retains its existing database checks/error tokens. Observe reads every carrier before writing; Apply removes before adding through existing NativeHealth, confirms each write immediately and reports confirmed changes one at a time. No city presence cache, event registration, native object retention, generic eligibility or shared pending worker.

Support retains eligibility/INDUSTRY exclusion and SpecialistSupport retirement before effect work. Housing retains actual anchor, ACTIVE II, ordinary building completeness/pillage/Tier deduplication and proof-specific investment path. Native hooks, StartReady/NewAudit/NewTargets errors and exact health witness stay where they are. Exact exit names come from the same descriptors and still go through Store.RemoveOwned plus the existing targets.Exit loss guard. Existing InternalOnly metadata remains the ordinary-building exclusion authority; no new classification or prefix filter. No pillage-rebuild branch exists in these two presence-only owners, so none is invented/deleted in this slice; other carrier owners follow in later S7a batches.

T01/T03/T04/T05/T08: retained real owner/health/D/shared anchor fixtures plus independent kernel preflight UNKNOWN, readback failure, partial success count, definition failure/recovery, key zero, detached lists and exact exit. Compare old/new real owner carrier sets and native call order. No timers, added scans or production consumer fanout; descriptor sizes remain 3 and 9. U5 native validation remains pending.

### Machine validation evidence

- Stage/status: `S7a1` / `LOCAL_SIMULATION_PASS`; tests=94, passing=94, registered-open=0.
- Source: base `77b8c14c11953c6813259ed22e9703b3fd625355`; dirty=True; input SHA256 `06b4807eaffd1a36e26fc0ea50b2db07248aa06cdc2c537e297060a9afccd0ca`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7a1 --output local/refactor/S7a1-B315-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7a1-B315-first/closure.json`; SHA256 `40377ec6dc168e871fc9eba4353b3903fba4be000f91e4d4da5e2ce5d2d86514`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 60; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S6c_actual_support_housing_GPP": {"foundation": "actual EF overlay plus explicit foundation/Store-stamp doubles", "geometry": "one separate city-local lookup included; full D census not used for anchor", "independent_city_index_reads": 4, "independent_state_samples": 3, "owner_district_enumerations": 0, "same_carriers": true, "shared_city_index_reads": 2, "shared_state_samples": 1, "writes": 0}, "S7a1_real_owners_differential": {"baseline": "77b8c14", "presence_only": true, "same_carriers": true, "same_native_order_and_counts": true, "source_owners": ["ResearchSupport", "Lv2Housing"], "states": 5}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 198, "XML": 25, "package_files": 320, "modinfo": 342}
