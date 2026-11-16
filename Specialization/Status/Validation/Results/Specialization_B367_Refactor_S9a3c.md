# B367.394 — S9a3c passive scoped training fact observations

## Plan and Runtime Impact Contract

Accepted S9/F16,D15; base B366.393/5677cd5. Scoped working plan recorded before runtime edits. This publisher-only step completes base-fact availability metadata for the later Training invalidation consumer; UI/global refresh, admission and SYNC/RESERVE remain unchanged.

Store.active reuses its already verified raw reference. EffectiveFacts observes the existing private capture/cache base tuple before the projector,never a caller-forged projected result. No added native getter,city lookup,second facts sample,audit,enumeration,Property/save write,event,timer or GC policy. TrainingInputStamp and ObserveTrainingFacts share the existing positions/workers routing (O(1) modern index; frozen two-record in-memory legacy fallback). Each worker retains fixed state/reference/issuer/sequence scalars only; the issuer is a tiny session identity,not a native object or service cache.

At most one short-lived frame per observed synchronous read,depth8 maximum; the chain releases on success/error before the original invalidation/rethrow. Protected observation failures do not change returns or thrown objects. The read's original outer failure yields FACTS_UNAVAILABLE only with reliable scope; independent UNKNOWN governor yields FACTS_UNKNOWN. Projector-only exceptions preserve the independently confirmed base. A later-starting same-city observation cannot be overwritten by an older serial. Different-city observations remain independent; service replacement rejects an old issuer.

Depth overflow does not reject the underlying read or allocate further frames. It increments one bounded diagnostic scalar and downgrades only matching pid/city or verified reference/token ancestors to FACTS_BUDGET_UNKNOWN. This conservatively prevents an unobserved caught inner failure being hidden by older outer confirmation; a subsequent real normal read recovers. An overflow source with no matching frame and an early failure before any reliable scope cannot publish a guessed observation. This remains an explicit coverage limit,not a complete recovery guarantee. No periodic retry or city cache compensates for it.

Healthy Lua overhead is one frame with fixed scalar fields,one protected note per existing Store.active visit and one protected observation publication per scoped read. All observations use already acquired values; the existing business authority checks/cache/read behavior remain. No eligibility,amount,capacity,queue,native creation,receipt or persistence schema changes. Training.eligible's final independent binding read and post-stamp SYNC are the next slice; the global UI dependency is retained until complete composition proof.

T02/T04/T05/T08,L3 for shared EF/Store stack semantics. Fourteen new tests cover actual Store+EF+Inspect,base errors and recovery,UNKNOWN vs confirmed zero,projector error/false/forged table,nested same/different cities,old service,observer/reference-note errors,depth13 bounded frame behavior,caught depth9 failure,cross-city overflow and transient reference release in Lua doubles. The B366/current differential asserts identical business values,saved record bytes and exact wrapped native getter counts. Ten prior Store inputs and65 affected shared-read/anchor/worker regressions passed separately. Independent read-only review re-ran24 focused tests and found no new blocker after the overflow correction; no assertion was weakened.

The first overflow draft dropped deeper observations and could let an older confirmed frame hide a caught depth9 same-city failure. The final matching-ancestor BUDGET_UNKNOWN correction and two formal regressions preserve both conservative same-city failure provenance and cross-city isolation. Mock weak-reference release is not a claim about native engine retention.

Full machine evidence is local/ignored,not a permanent backup. No deployment,main promotion,game launch or native PASS. Continue approved S9/S10; exact D7 permanent-history/money and D5 native-attribution limits remain OPEN.

### Machine validation evidence

- Stage/status: `S9a3c` / `LOCAL_SIMULATION_PASS`; tests=1031, passing=1031, registered-open=0.
- Source: base `5677cd50d19bb73028f30cb0b14105d96107a2d6`; dirty=True; input SHA256 `1e818c76146d4c2bf8d6da64b0c3862f32baedd9aae8626ca68db1e50e4b1aea`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9a3c --output local/refactor/S9a3c-B367-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9a3c-B367-final/closure.json`; SHA256 `9c5e0838487f03580ce2c4a902537197931ac950fa0076e68168d562ecc27c5c`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 208; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9a3c_actual_fact_observation": {"UI_global_removed": false, "baseline": "5677cd5", "extra_native_reads": 0, "fact_resamples": 0, "frame_depth": 8, "frame_tables_per_read_at_most": 1, "native_getter_calls_before_after": [150, 150], "new_city_maps": 0, "same_values_native_getters_saved_bytes": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 394}
