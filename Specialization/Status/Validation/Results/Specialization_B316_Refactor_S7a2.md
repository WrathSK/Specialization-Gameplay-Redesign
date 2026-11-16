# B316.343 — S7a2 GPP bit carriers

## Plan and Runtime Impact Contract

Authorized S2–S10; base B315.342/d99a413. No deployment/main/game launch, save schema, amount, role, eligibility or reward change.

Use CarrierSet's exact ordered descriptors for Lv2GPP (four classes × eight bits). Keep its existing full GPP database row validation lazy; publish health ownership only after complete success. CarrierSet initialization resolves the already-validated immutable building indices; hot reconciles no longer repeatedly resolve those same definition rows. Existing Describe remains unchanged.

Unlike the first two owners, GPP must retain a fresh presence read immediately before each changed-bit operation, and the same building handle for its post-write readback. Add an explicit Apply option for this existing behavior. Unchanged bits are not newly read for mutation; all 32 bits are still preflighted before any write. Skip a scheduled write if reliable pre-write evidence already matches its target. Remove-before-add and individually confirmed change counts remain. ResearchSupport/Housing retain their original default policy with no new pre-write read. NativeHealth owns self-feedback and new sibling causes; no new listeners, pending queues, global registry, scan or timer.

Worker limit255, ACTIVE II, all four professions and their exact point-class definitions stay in Lv2GPP; no cumulative point grant, location or carrier pillage policy is added. Exact names/health ownership/exit share descriptors. Targeted gates T01/T03/T04/T05/T08: actual GPP/worker/shared-anchor regressions, historical-source differential, fresh pre-write reentry convergence, unknown presence and partial confirmed counts; first kernel owner behavior/cost remains identical. Location-sensitive owners and their redundant D4 repair branches are subsequent S7a work, not claimed complete here.

### Machine validation evidence

- Stage/status: `S7a2` / `LOCAL_SIMULATION_PASS`; tests=98, passing=98, registered-open=0.
- Source: base `d99a413c7c55f4610199d314df24fb02a30e1d95`; dirty=True; input SHA256 `148dc7e11ed2fc1d69dbc0c6bda7a0e651971d71b4742946e072aadbc26bed08`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7a2 --output local/refactor/S7a2-B316-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7a2-B316-first/closure.json`; SHA256 `558501936f272d633bebdf5b67c71a8263bab4906967378e3bb4b3688b01e73c`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 62; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5d4b2_UI_idle": {"governor_requests": 0, "initial_requests": 1, "thousand_idle_extra_requests": 0, "worker_requests": 1}, "S7a2_GPP_differential": {"baseline": "d99a413", "definition_lookup": "immutable indices resolved once after original schema validation; not a gameplay/native-point measurement", "same_confirmed_changes": true, "same_native_presence_and_write_order": true, "workers": [0, 1, 2, 3, 7, 255, 1]}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 198, "XML": 25, "package_files": 320, "modinfo": 343}
