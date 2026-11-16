# B314.341 — S6j network input increments

## Plan and Runtime Impact Contract

Authorized S2–S10; base B313.340/08db0cb; no deployment/main/game launch. No persisted shape, amount, qualification or transaction policy change.

Keep NetworkInput's full owner city census, native owner/reference reads, capital and every route endpoint/trader/war proof. Add call-local incremental eligibility for the role-fact binding only. Reuse a city's prior scalar role facts only with a matching reference, CONFIRMED provenance and a matching NETWORK_CITY stamp. Direct Refresh, route candidate, startup, queued fallback and replaced FactChanges/EffectiveFacts/Store services and a new turn force full fact reads. UNKNOWN/RETAINED is freshly attempted, never cached as confirmed. Full captures also sample stamps before EF, and duplicate acceptance refreshes stamps without publishing a false value change.

FactChanges keeps one global, one ownerwide and at most 2048 city versions per owner, beside existing bounded state. Every role invalidation updates it synchronously before fallible Emit; whole-owner/global causes invalidate every city. Overflow degrades to ownerwide invalidation before reusing anything, never eviction or a falsely current stamp. No timer, invalidator native read or new listener. Capture reads a current-turn scalar before and after sampling (two reads) to prevent cross-turn reuse. Bindings still make one sample per owner/drain; per-city stamps cover multiple rows and missed notification, rather than treating its first row as a complete scope. Reentrant invalidation still revokes owner transaction proof and waits for the next existing cause/drain; generic busy queue stays full.

Verified owner-first CityBuilt/OnDistrictConstructed hooks may reject known foreign owners before rebuilding; unknown owner stays conservative, and no unverified third argument becomes a city ID. Full UI route protocol remains unchanged.

T01/T02/T03/T04/T05/T08: real Bridge/FactChanges/Bindings/Commerce composition and retained prior network tests; multi-city same drain, same-turn second change, failed Emit, failed capture, UNKNOWN recovery, cold/replaced service, owner/reference change, global/ownerwide/capacity fallback, route candidate/endpoint and reentry. Compare EF sampling at 8/32/64 cities while keeping complete census measured explicitly. No CPU/native heap or USER_GAME_TEST_PASS claim. F36 remains assigned to S10, F32's real-D filtering closed in S5; U3 is an internal local checkpoint per accepted D13.

Reuse additionally requires the existing per-city Store.FactStamp authority witness (same non-nil scalar) on each census row. This preserves in-progress commit, applied-then-throw fault and live record/reference checks before post-commit role notification. Missing/failed witnesses use the original fresh EF path; no legacy reuse is inferred. This retains Store witness/native reads and record validation cost, so the measured reduction is EF deep captures, not all native reads or all city work.

For prior Potential > I, reuse also rereads the existing raw governor gate and requires the same reliable derived ACTIVE. This preserves late native-property availability/changes without assuming native listener order. Gate failure/difference takes the original EF path. Potential I/NONE retain their original lack of governor dependence.

A reuse hit rechecks Store.FactStamp after the raw governor witness. Getter reentry causing an applied-then-throw Store failure cannot publish the old row as confirmed even when no successful commit notification exists. The actual Store fault-in-gate counterexample is part of T05.

## U3 engineering checkpoint — S6 complete locally

S6a business D cache separation/capacity, S6b current-specialization projection, S6c worker/anchor facts, S6d bounded reverse dependencies, S6e lazy Capital quotes, S6f guarded Commerce/Development workers, S6g scoped Culture discovery, S6h event-driven unit UI, S6i current-site locality and S6j network fact increments are complete within their accepted scopes. All are separate develop commits. No persisted schema change in S6.

Retained costs/limits: complete network city/reference/route census remains required; Standardization retains its full live membership recovery; actual automatic worker audits remain separate read phases; full map marker discovery intentionally visits the owner; private index builds/copies still cost work. Ext-F11's former multi-destination Capital quote hotspot was removed by S6e rather than adding an unused shared-source cache. F32's live actual-D/carrier filtering was covered in S5; remaining dead probe hooks and F36 HalfYieldProbe cleanup are explicitly S10 obligations, not silently marked removed here.

U1 D13 makes U3 an internal engineering checkpoint, not a mandatory user interruption. Local real-module/negative-case gates are sufficient to proceed to S7. Native N2 evidence (3–5 turns, counters/unchanged yields/GC/footprint) remains folded into final U5 unless a specific blocking engine fact emerges. No new USER_GAME_TEST_PASS, native performance/memory claim or deployment. The accepted S5b/D15 contract's phase/write barriers, synchronous pre-notification invalidation, UNKNOWN handling and same-turn second changes are preserved and exercised by the selected actual Store/Bridge combination. Primary internal review is not a new Advisor-authored approval.

- User decision: none.
- User testing: final U5; main/live remains B307.334.
- Primary next: S7a carrier mechanism extraction, then S7b–S10 in dependency order.

### Machine validation evidence

- Stage/status: `S6j` / `LOCAL_SIMULATION_PASS`; tests=163, passing=163, registered-open=0.
- Source: base `08db0cba0eaf9359e63f33345b9c62ea52431a33`; dirty=True; input SHA256 `2c244dd1a39a09dbb5baf34831d940ce4cb1babb95268a39563fe06f8f3eff14`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6j --output local/refactor/S6j-B314-final2/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S6j-B314-final2/closure.json`; SHA256 `e91a84c1ec1fd8460283a0d307fd0e9994f4d0cd4f3704b380e039ae12e9b82e`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 61; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5b_real_Store_and_writers": {"native_doubles": "catalogue and carrier presence; actual Store/Flow/EffectiveFacts/Housing/GPP/Probe", "no_write_captures": 1, "real_removal_captures": 2}, "S5c2_busy_refresh_budget": {"initial_captures": 1, "ten_reentrant_causes_additional_captures": 1, "thousand_idle_additional_captures": 0}, "S6d_reverse_index_bound": {"capacity_failure": "UNAVAILABLE; original consumer scan fallback until new context", "edges": 2048, "native_reads": 0, "single_source_returned_targets": 1, "targets": 2048, "timers": 0}, "S6g_Culture_scalar_discovery": {"after": {"edges": 3, "graph": 0, "records": 0}, "before": {"edges": 34, "graph": 34, "records": 36}, "cities": 37, "components": 2, "remaining": "new topology O(E) index build; Input full provenance copy unchanged; no CPU/native heap claim", "same_effects": true}, "S6j_real_Store_network_input": {"after_deep": [1, 1, 1], "before_deep": [8, 32, 64], "remaining": "complete census/ref, Store authority and route endpoint/trader/war checks; governor witness for Potential>1; not all native reads or CPU time", "work": [{"census": 8, "cities": 8, "deep": 1}, {"census": 32, "cities": 32, "deep": 1}, {"census": 64, "cities": 64, "deep": 1}]}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 197, "XML": 25, "package_files": 319, "modinfo": 341}
