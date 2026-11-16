# B304.331 — S6b guarded raw worker sharing

Source base: B303.330 `b0ded6f`. LOCAL_SIMULATION / STATIC_CONFIRMED only. W0004 L3; select T02/T03/T04/T05/T07/T08 at the affected fact owner, native producer and three real consumers. No deployment or native PASS.

## Runtime Impact Contract

- Ownership: EffectiveFacts remains the authority for identity/progression/ACTIVE. `Inspect` executes only read-only projections inside its existing full Store checks, returning detached values. Infrastructure, Apply and Chair keep their own qualification, unique-Campus, reference, pillage, formula, encoding and writer rules. Their writes happen after the projection. The legacy Shadow still sums its original eligible Campuses.
- Sharing: only the raw worker count is memoized, inside one declared synchronous phase. Parent fact row, full owner/city/reference stamp, detached anchor id/type/plot, EF generation, FactChanges instance and owner/city COMMERCE generations scope reuse. Original read/gate count is preserved; the existing cached governor check now certifies after the read-only body. There is no new authority shortcut, persisted field, startup dependency, native listener, timer, city enumeration or polling/retry.
- Bounds and failure: at most2048 worker samples per phase, eight simultaneous in-flight captures; overflow remains legal/fresh without evicting warm samples. No native objects or callback closures are retained after the call. Reader expires at projection end. UNKNOWN/invalid values are not memoized; new reliable causes and explicit reads retain existing recovery. Writes invalidate both layers, including same-turn second changes. Reentrant base publication cannot be overwritten or double-counted; unknown business projection does not poison independent confirmed base facts.
- Cost: direct native getter observers run only in tests. No new per-worker runtime counter was added, since its turn getter would offset savings. Actual Store/Flow/EF/Probe comparison preserves7 full stamps for3 no-write reads, with all other measured native leaf counts equal and2 plot/worker pairs removed. Actual three-writer composition uses real EF/DC/SQL but an explicit foundation/Stamp native double; it is separate from actual Store proof. This proves work reduction in that window, not native CPU/heap improvement.
- Tests:20 independent cases cover phase lifetime, detached values, exact/owner/other-city changes, exceptions, UNKNOWN numeric values, write barriers, FactChanges replacement, cold same-city reentry, new governor witness, worker capacity2048/2049, foreign/legacy/reference bounds, actual Probe property writes, actual Store cost and three actual writers with unchanged carriers. Inherited strict assertions remain unchanged.

## Result and remaining boundary

Full machine artifacts/transcripts remain ignored local outputs; their hashes are evidence locators rather than permanent backups. No frozen historical report changed. Anchor-only consumers are deliberately not routed through a full D building census; that separate S6 obligation follows.

- User decision: none.
- User testing: U5 integrated native specialist reassignment/ACTIVE and yield smoke, with native CPU/heap still unmeasured.
- Primary next: minimal anchor-only shared samples and the remaining S6 hot paths, then S7–S10.

### Machine validation evidence

- Stage/status: `S6b` / `LOCAL_SIMULATION_PASS`; tests=135, passing=135, registered-open=0.
- Source: base `b0ded6f8c0e21d8d9204c4401da828ce71621458`; dirty=True; input SHA256 `e74e4ff060fcd5253649b0fcbca7dfada7278a15aacbbf13ee2d8c6c7c54d72f`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6b --output local/refactor/S6b-B304-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "589ba3db7f4b927ab1ff478a9ccbb60ebadfb6fc9fb1cbfabf332955644054f2"}}`.
- Full artifact: `local/refactor/S6b-B304-final/closure.json`; SHA256 `859aa85b42bb423554328df0985ed5b4e4f4b7ff1980c4b11eb15792543635b3`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 57; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5b_real_Store_and_writers": {"native_doubles": "catalogue and carrier presence; actual Store/Flow/EffectiveFacts/Housing/GPP/Probe", "no_write_captures": 1, "real_removal_captures": 2}, "S5d4b1_role_mark": {"city_visits_at_mark": 0, "native_notifications": 44, "native_owner_listeners": 1, "scoped_deliveries": 1, "thousand_idle_extra_deliveries": 0}, "S5d4b2_UI_idle": {"governor_requests": 0, "initial_requests": 1, "thousand_idle_extra_requests": 0, "worker_requests": 1}, "S6b_actual_Store_full_guard_leaf_cost": {"after": {"leaf": {"Game.GetCurrentGameTurn": 7, "city.GetID": 24, "city.GetOwner": 24, "city.GetProperty": 9, "city.GetX": 34, "city.GetY": 34, "plot": 1, "workers": 1}, "stamps": 7}, "before": {"leaf": {"Game.GetCurrentGameTurn": 7, "city.GetID": 24, "city.GetOwner": 24, "city.GetProperty": 9, "city.GetX": 34, "city.GetY": 34, "plot": 3, "workers": 3}, "stamps": 7}, "scope": "actual Store/Flow/EF/Probe; plot and governor native doubles; no CPU/native-heap claim"}, "S6b_three_real_research_writers": {"after_worker_reads": 1, "before_worker_reads": 3, "carrier_writes": 0, "foundation": "explicit foundation/Stamp double; actual EF/DC/Infrastructure/Apply/Chair and SQL", "same_carriers": true}, "T01_chair_city_visits": 1, "T04_effective_captures_two_writers": 1, "T05_pending_fact_attempts": 0}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 195, "XML": 25, "package_files": 317, "modinfo": 331}
