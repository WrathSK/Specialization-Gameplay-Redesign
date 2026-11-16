# B340.367 — S8c5c production composite legacy cleanup

## Plan and Runtime Impact Contract

Accepted S8/F08/C009/D12/D15; base B339.366/49eee15. At the old YieldCarrierExit startup position, after Store and before BindingProbe, register the mandatory LegacyCleanup thunk before including or starting its owner. RuntimeComposition keeps the thunk guarded if startup fails; export rollback cannot silently remove the responsibility. The core itself has no new hook, timer, scan or saved state.

The ten original Start callers explicitly receive centralExit=true. Seven pure building exits stop only individual registration; the exact catalogue owns their physical cleanup even if those Starts fail. Lv3Support and Lv3Effects register fixed runner factories using their actual existing RuntimeWork target sets, original pending-slot handling and recovery events. Neither group may ACK the aggregate alone. Dialogue registers the identical precise carrierTest/meaningOverride/meaningQualification cleanup as a required post after physical readback; its existing Return callback remains. These three actual callers declare the new startup dependency. Existing relative startup order, retired/retireCommerce flags and later Dialogue retirement remain exact.

Default/isolated Start profiles retain original registrations for compatibility and historical comparisons. CopyYields, StandardizationDiscount and CultureInspirationProbe already-retired branches remain unchanged. Existing production WithdrawCulture/Withdraw/Init, manual probe APIs, SQL and package files stay in place; no S10 deletion is performed. Failed/missing participant remains incomplete, but other physical groups continue. Callback/metadata failure never becomes absence or completion.

Working set remains the same exact1409 IDs plus two plot flags, held only by explicit confirmed Store loss work. One aggregate registry entry replaces11 production legacy entries; fixed weak-ticket subgroup progress and bounded Store/target recovery are unchanged from B339. No positive effect, native money/unit operation, eligibility, persistent key or cleanup retry frequency is added. No native CPU/heap savings claim.

T04/T05/T06/T08 use actual Store, current Gameplay composition entries/options, real ten participant modules and real target recovery. Verify mandatory failure gate before include/Start, late failure quarantine, exact registrations/removals, independent Lv3 recovery after Store budget, Dialogue hold matching and post order, preserved Return reset, ordinary/other-city data and live APIs. Inherited B339 tests remain strict. The two source assertions explicitly superseded by this authorized wiring (no LegacyCleanup/unchanged full Start list) are executed unchanged against exact pre-cutover B339 Gameplay; new current tests prove one insertion with every original relative Start position unchanged. No assertion is weakened. Old S8c4 and S8c5b measurements describe their isolated/default/pre-wiring fixtures, not the current production owner count.

First focused test found the new fixture had erased its original district catalogue while substituting legacy metadata; actual Store correctly rejected return with RETURN_DISTRICT_UNAVAILABLE. Retaining original non-building metadata makes the unchanged strict return assertion pass; no runtime change or guard relaxation was used. A standalone historical test also correctly required explicit read-only DB configuration; full runner supplies the existing configured input.

Native ownership/cleanup/save-load remain U5 USER_GAME_TEST_REQUIRED. D5 and full D7 remain OPEN. No deployment, main promotion or game launch.

### Machine validation evidence

- Stage/status: `S8c5c` / `LOCAL_SIMULATION_PASS`; tests=588, passing=588, registered-open=0.
- Source: base `49eee1579bb584d7df2410841ca5bb8b9176fb45`; dirty=True; input SHA256 `87d0c8f8ca4d83bc59591a6b4f783443a943323a2309f4e9eb6594dcda00eb4a`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8c5c --output local/refactor/S8c5c-B340-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8c5c-B340-final/closure.json`; SHA256 `1adedc5292742d5cccb6716b86fc6865212cb5445217e0b8644ed46ae4f52dfb`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 160; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8c5c_actual_production_cleanup": {"building_removals": 1409, "current_legacy_exit_gates": 1, "native_effect_cleanup": "USER_GAME_TEST_REQUIRED", "new_events_timers": 0, "plot_writes": 2, "prior_legacy_exits": 11}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 367}
