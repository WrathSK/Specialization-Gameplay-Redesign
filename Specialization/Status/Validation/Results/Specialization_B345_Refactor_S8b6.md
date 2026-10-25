# B345.372 — S8b6 ClaimTimer isolation

## Plan and Runtime Impact Contract

Accepted U1/D7 and S8/C005; base B344.371/e789909. Extend only the fixed reviewed owners to ClaimTimer's single existing field. Existing full remaining-parent validation and exact preserved-field native CAS/readback apply; no saved schema/key, project/timer/receipt controller, event, cadence or recovery rule is added. Failed restore checks seven fixed owners/eleven owned fields; healthy path remains unchanged. Sidecars remain bounded scalar observations.

ClaimState,WriteClaimTimer,ClaimComplete reject isolated timer history before interpreting or committing a new receipt. Confirmed loss skips clearing only that invalid timer so the existing core loss and other capabilities can commit while preserving original evidence. Independent Complete does not read ClaimTimer and remains available for ordinary first specialization. Its existing early returns for LEGACY_CLAIM and nonempty restructuring candidates remain exact, so this does not bypass Claim eligibility. Healthy Claim's existing reliable native-completion/no-timer exception is preserved; no new requirement for CALLING or a timer is invented.

Actual ClaimProjects keep their established unknown-authority handling: withdraw all four access markers, display STOPPED, block new timer/finish/receipt work. Invalid ACTIVE/CALLING survives reload,three turns,native completion notification and1000 idle publications with zero new native finishes or permanent writes. Public Store guards and generic preservation tests use actual Store; core lifecycle and ordinary investment remain independent. Existing origin-ID session cleanup is not expanded into a new changed-ID ownership guarantee.

T04/T05/T06/T08:10 focused cases cover core/sibling abilities, all three APIs, exact field preservation, rejected deletion, investment, loss/return, independent first specialization, healthy no-timer native completion, actual schema3 acquisition/Claim receipt failure, original strict remaining Commerce/template/core guards, and actual ClaimProjects no replay. The first test draft put acquisition/Claim fields on a schema2 record where the original validator does not interpret those optional fields; the corrected test uses actual schema3 authority and keeps current validation rules unchanged. Prior B344 timer-outside-scope matrix executes unchanged on exact B344 source. All other inherited assertions remain.

Permanent recovery remains OPEN: an invalid timer cannot be reconstructed from a current queue,elapsed time or an unassociated completion event. No zero baseline,replayed FinishProgress,guessed receipt or player repair UI is introduced. Acquisition legacySet,Claim receipt,restructuring and base/reference remain part of full strict parent validation,not timer isolation. Commerce/reputation,templates and D5 native attribution continue. No deployment/main/game launch/native PASS.

### Machine validation evidence

- Stage/status: `S8b6` / `LOCAL_SIMULATION_PASS`; tests=681, passing=681, registered-open=0.
- Source: base `e78990960a48f092fd79df8e5131b4615711327b`; dirty=True; input SHA256 `64f3734a161517246d4c4c15509891610123830c2b8724536c643952dbc63816`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8b6 --output local/refactor/S8b6-B345-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8b6-B345-final/closure.json`; SHA256 `c0305d86ebe20b35cb867deeb67442eae43260bf577fbfc2a36e9cd07a81271c`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 165; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8b6_actual_Claim_isolation": {"access": "existing_UNKNOWN_withdrawal", "corrupt_timer_preserved": true, "idle_history_writes": 0, "new_Claim_receipts": 0, "new_native_completions": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 372}
