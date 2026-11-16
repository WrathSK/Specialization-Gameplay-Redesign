# B346.373 — S8b7a pure Commerce validation split

## Plan and Runtime Impact Contract

Accepted U1/D6/D7 and S8/C005; base B345.372/1bffe3b. Preparatory behavior-neutral slice only. Extract the exact existing configuration/selection/owner assertions into ValidateConfiguration and existing reputation/qualification assertions into ValidateReputation. Full Validate calls them in original order and returns the identical original value. No assertion removed,reordered or changed; no production partial reader,State/Write change,Commerce isolation or current Gold behavior is introduced.

Both new entry points are fixed pure explicit-input validation observations. They do not prove permanent corruption,repair a value or grant qualification. Existing full validation remains required by every current caller; there is no automatic new consumer,cache,native read,hook,timer,scan or saved structure. Same original loops and validation scope with two fixed function calls; no performance benefit claim.

This prepares the remaining D6/D7 requirement: malformed/unknown reputation must not be mistaken for a reliable bonus or silently stop independently confirmed commercial Gold. Wiring that behavior needs separate preserved-raw-history and configuration/lifecycle/known-marker proofs; this slice does not claim it complete or expose a sanitized value as permanent authority.

T04/T05/T08:4 focused Lua5.1 cases execute exact previous CommerceModel source and current source.24 valid/invalid inputs compare success/error code ordering and unchanged value bytes,including simultaneous bad selection+bad reputation.9 business sequences compare Select,capacity,Advances,Exit,OwnerChanged,Resume and existing full-invalid failures. Pure checks read no native surfaces and full Validate returns the same object. All existing actual Store/Commerce/other ability regressions remain selected.

Commerce/template isolation and safe permanent recovery remain OPEN,as does D5 native attribution. No deployment/main/game launch or native PASS.

### Machine validation evidence

- Stage/status: `S8b7a` / `LOCAL_SIMULATION_PASS`; tests=685, passing=685, registered-open=0.
- Source: base `1bffe3b0def1404d905050a30f18959e7b9eab28`; dirty=True; input SHA256 `3b29672c280cc6eea9d9e13e41e4beb54aff0fb8527740ed608fc8beef8e26a8`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8b7a --output local/refactor/S8b7a-B346-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8b7a-B346-final/closure.json`; SHA256 `ceb97ca7c9cfb24d8825aa32c5fc5a61317221fc1457d1301635160d983cac5e`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 166; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8b7a_Commerce_validation_differential": {"cases": 24, "production_partial_consumer": "NOT_YET_WIRED", "same_result_error_order_bytes": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 373}
