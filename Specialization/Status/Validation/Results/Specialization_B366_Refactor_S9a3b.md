# B366.393 — S9a3b pure training capacity input signals

## Plan and Runtime Impact Contract

Accepted S9/F16,D15; base B365.392/1970777. The scoped working plan was recorded before runtime edits. Publisher-only: Training UI still uses its original signature and no SYNC/RESERVE/BUILD call is added. Fresh T.Available/list remains the capacity authority; the new stamp is only an invalidation input,never proof capacity is empty or admission is legal.

Gate.Training.CapacityInputStamp(owner) reads only its already loaded owner,storeBlocked,busy,phase,one unit-event scalar and one observer-failed boolean. It never calls load,Store.Read,Available,list,P.IsTestPlayer,Game clock or native objects. Cold/unmatched owner is explicit. Busy is a live scalar dimension,not an epoch increment on every request,so a completed read-only Gate request does not create endless UI work. Same-service observer state is private; a restarted Gate starts fresh,and old service calls cannot poison its successor.

No new native hook or unit cache. Existing Training.Birth (UnitAdded path) increments capacity observation for the supported owner before its unchanged native unit/type read and original qualification/event correlation. Foreign events retain the original early exit. Because removed unit type cannot be reliably fetched,existing UnitRemoved callback conservatively invalidates this player's capacity without a type lookup,then preserves original placement cleanup/removal counters. Plain local units may consequently cause one later existing SYNC when the UI is migrated; this explicit false-positive scope is not a new scan or unit rule. Units of all three Expedition-family kinds still block via original Available.

Observation errors do not control business work: Birth protects both observer/observer-failure calls; Removed invokes a private scalar function,not a mutable public callback before old cleanup. Error provenance belongs to the original Gate instance only. Healthy cost is fixed Lua scalar update/two protected observer calls per supported Birth and one scalar update per existing removal;0 added native reads,enumerations,Store writes,events,timers or GC work. No persistence schema,unit adoption/creation,qualification,amount,queue or receipt changes.

T02/T05/T08,L3 for shared Gate callback ordering:10 new Capacity tests plus2 wrappers retain all43 original actual Training and17 original UI assertions. The12 selected tests pass. Cover1000 pure reads with forbidden native/Store/clock functions;unreserved birth without Activity.revision change or adoption;three family presence/removal;known foreign0 change;conservative ordinary local event;blocked uncertain save;busy getter visible inside actual READ callback then idle signature unchanged;same-turn second event;observer failure with original birth/completion receipt;old-source restart isolation;and public observer failure not interrupting original Removed duties. No native PASS.

Initial busy test attached to EffectiveFacts even though idle READ actually visits the native unit collection; corrected the seam to the existing GetUnits callback and kept the BUSY→IDLE assertion. Independent review caught public Removed observer failure and cross-source error provenance in the early draft. The final implementation uses private removed observation and private per-source failure,with formal regressions. Final independent review passed11 prior tests and an additional actual NAMING→removed/HELD case; that extra case is now the12th test,also PASS. No assertions weakened.

Complete machine evidence remains local/ignored. No deployment/main/game launch or game-test claim. Next add final binding/facts observation and post-stamp SYNC receipt,then migrate actual Training UI consumption/idle gate before removing only its global refresh dependency. Owner-applied institution fields,adjacency,S10 and exact D7 permanent-history/D5 native-attribution limits remain OPEN.

### Machine validation evidence

- Stage/status: `S9a3b` / `LOCAL_SIMULATION_PASS`; tests=1017, passing=1017, registered-open=0.
- Source: base `19707772debb0b2000f48dc07354e94ef88988f0`; dirty=True; input SHA256 `414aa86560d543055a666fb06edd04ef680e11876e5197230c48c9d7712f96c9`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9a3b --output local/refactor/S9a3b-B366-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9a3b-B366-final/closure.json`; SHA256 `392156045bb5318c90cc2a5e9b2a811a8866ae4351aad7d27db77c73970bb383`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 207; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9a3b_capacity_input": {"Store_writes": 0, "UI_migrated": false, "conservative_owner_unit_event_invalidation": true, "native_reads": 0, "new_native_hooks": 0, "new_unit_cache": 0, "queries": 1000, "unit_enumerations": 0}, "S9a3b_original_training": {"assertions": 43, "current_runtime": true, "native_save_or_admission_rules_changed": false}, "S9a3b_original_training_UI": {"assertions": 17, "current_runtime": true, "global_refresh_still_present": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 393}
