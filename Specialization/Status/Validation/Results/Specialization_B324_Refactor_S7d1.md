# B324.351 — S7d1 explicit queue observation

## Plan and Runtime Impact Contract

Accepted S7d/D4 strict event-driven constraints; base B323.350/324df73. Inventory actual ClaimProjects, DialogueProjects and EngineeringStudyProjects, not retired Dialogue/TimedProject experiments. Extract only detached queue classification and synchronous observation, no Start, retained cities, listeners, timer, pending queue, retries, automatic consumers or global project competition. Calls remain at their original explicit requests, related city events and existing active boundaries. Full event-driven recovery/UI retry work remains S7d2; this slice does not claim complete D4 closure.

CurrentlyBuilding failure/non-string/ambiguous nil is UNKNOWN. A nonempty known other target returns OTHER without adding a size read. Target=project still needs exact size1, preserving each owner's existing UI reference/turn checks and single-current requirement; invalid current counts now report the read-unknown reason instead of the old uniqueness wording. Native nil/empty string is only an empty candidate; GetSize=0 proves EMPTY, positive/missing/inconsistent size is UNKNOWN. An existing UI fallback may prove empty only after owner/reference/turn validation and matching empty target. Technical evidence Full_Turn.md section16 confirms nil/empty candidate plus size proof, not every native empty shape/event ordering. USER_GAME_TEST_REQUIRED remains for native availability/recovery.

New work is at most one GetSize on the formerly unchecked empty-target path (and the already-established fallback when that getter is unavailable); no owner/city enumeration. Unknown never invokes cancel/FinishProgress/completion. Claim may accept a legitimate completion without a timer; Dialogue forced completion samples works once; Engineering needs full ended/next-turn plus armed CALLING proof. All remain independent. No save shape, amount, project eligibility, native replay, startup or deployment change.

T01/T02/T04/T05/T08: raw current/other/empty/unknown/multi count matrix and read order; all three real controllers hold pending on ambiguous empty, recover on the same city's real production event, distinguish confirmed empty, preserve actual completion and no-completion/throw/UNKNOWN safeguards; source differential normal outcomes and unrelated-city/idle bounds. Legacy completed doubles already clear target/count consistently, so their assertions need no weakening. No main/deployment/game launch.
Historical-fixture adaptation: the B235 Study fixture omitted the current typed FactChanges/Bindings replacement. Two original methods fail identically on base324df73 and current before composition (missing notification and stale E/entry marker). The profile now composes actual Store/FactChanges/IndustryHistory/Bindings at the production drain boundary, rebuilt per FC instance after load, and observes committed ENGINEERING instead of the retired direct SourceChanged counter. All original Study assertions are unchanged; 22/22 methods pass independently on both versions. StandardizationEffects itself remains the fixture projection stub, not a claimed physical-effect integration. This is a fixture correction, not weakened completion/UNKNOWN proof.

### Machine validation evidence

- Stage/status: `S7d1` / `LOCAL_SIMULATION_PASS`; tests=374, passing=374, registered-open=0.
- Source: base `324df7375e170c3942bdf80350ab042df8d44ead`; dirty=True; input SHA256 `121c59aec558007cd2a698b91d46454aefed510c9459978d4195bce8e8083665`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7d1 --output local/refactor/S7d1-B324-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7d1-B324-first/closure.json`; SHA256 `cfee8f62a16312319e3208c3f19055c000aa4ec63b033c6bd9150de0aa567095`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 93; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S7d1_actual_unknown_recovery": {"ambiguous_nil_cancel_or_complete": 0, "idle_publishes": 1000, "owners": 3, "recovery": "same-city CityProductionChanged", "then_full_turn": "original independent receipts"}, "S7d1_normal_differential": {"actual_owners": 3, "baseline": "324df73", "full_turn_and_other_target": "identical complete Store record", "native_or_save_format_change": false}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 202, "XML": 25, "package_files": 324, "modinfo": 351}
