# B326.353 — S7d3a fixed project-reader initialization

## Plan and Runtime Impact Contract

Accepted S7d/D4 and D15, base B325.352/59f1a7e. Build the narrow prerequisite for removing pulse-count SYNC retries, not a generic event bus or module discovery system. Three fixed slots are ClaimProjects→Claim queue reader, DialogueProjects→Dialogue reader and EngineeringStudy→Engineering reader. The UI/default request flow is intentionally not connected until S7d3b; existing SYNC retry debt remains explicit, and this intermediate candidate is not deployed.

TimedProjectReaders is an explicit Gameplay composition entry after the Store and before Claim. Existing owner Start ordering is unchanged. Owners Attach only at the end of successful Start; composition Seal is separate from actual Store readiness. Current export identity and exact StartStatus OK are rechecked before every new wake, including EngineeringStudyProjects startup/export alias. A late failed constructor cannot publish an orphan backend. Store FRESH/EXISTING is required; WAITING uses the existing one-time StartReady scalar initialization latch, with its LoadScreenClose/publish/local-activation boundaries. HELD/failed/unknown status never grants readiness. The latch itself is not an authority or a business retry. Once latched, idle events perform no further initialization reads. A new handshake also checks current Store scalar status rather than treating a historical ready epoch as current reliability.

Registration is restricted to the current ExposedMembers fixed slot and exact reader function. Each immutable row has a positive exact-integer session serial; each kind stores only its highest serial, current row/binding and latest delivery. Unregister releases callback references while keeping the scalar serial, so old close cannot erase a newer context and A→B→A cannot resurrect an old callback. New serial requires a new row identity. No expanding delivery history, native objects, Properties, saves, timers, city enumeration, eligibility calculation or automatic action sends. Wake is latched before protected cross-context callback execution; exception diagnostics cannot cause a replay or break a sibling.

EngineeringStudy.Sync is a new dormant request route for the next UI availability integration. It refreshes only the requested city and advances only that city's existing saved round under the original qualification/ended/start+1/armed/completion rules. It never creates a round, awards an inferred completion or replays CALLING. ACK is session-only processing acknowledgement, not gameplay success. The added onlyID filter prevents synchronizing one city from advancing all active cities. Claim and Dialogue completion/cancellation policies stay independent.

T01/T02/T04/T05/T08: fixed-slot UI-first/GP-first/WAITING initialization, seal ordering, current HELD, failed/skipped and late-failed composition, invalid or mutable serials, same-tuple/old-row restoration, old close/new reader, malformed callback error object, no reader invocation and no native city access. Actual Store/IndustryHistory/FactChanges/Bindings/Engineering tests cover zero new round/write on rehydrate, exactly-once saved due completion, unknown/failed native no replay, qualification UNKNOWN, exact two-city sync scope and actual request routing. Startup fixtures import this real new foundation, preserving existing order/failure assertions. All previous S7d2/controller regression remains selected.

Native limits: cross-context function registration and real event/reader delivery still require U5; local simulations are not native PASS. The future UI connector must register only after adapter construction and hooks succeed, wake only mark work, send once per backend/epoch/reader context at a safe publish boundary and never resend a missing ACK or old BEGIN. Missing silent availability changes cannot be replaced with polling. No deployment/main/game launch or gameplay/save-format change.

### Machine validation evidence

- Stage/status: `S7d3a` / `LOCAL_SIMULATION_PASS`; tests=411, passing=411, registered-open=0.
- Source: base `59f1a7e842015f01a132eb7b83980fa0dd84d558`; dirty=True; input SHA256 `7597b8b2efc258c67d892e43c31b7957f8374905a748a3322547a849ae2868d2`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7d3a --output local/refactor/S7d3a-B326-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7d3a-B326-first/closure.json`; SHA256 `335fc1d76d441d250e7200978c2ecef1ecc342555376ef6191419140bea87633`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 107; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S7d3a_study_sync_scope": {"actual": "Store/FC/Bindings/IndustryHistory/EngineeringStudy", "due_cities": 2, "other_city_target_reads_during_first_sync": 0, "replayed_native_calls": 0, "separate_receipts": 2}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 204, "XML": 25, "package_files": 326, "modinfo": 353}
