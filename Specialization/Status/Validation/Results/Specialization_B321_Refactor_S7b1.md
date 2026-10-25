# B321.348 — S7b1 Property write/readback observation

## Plan and Runtime Impact Contract

Accepted S7b F26/C073/ST-02; base B320.347/69acc27. Add a stateless helper with no Start, events, timers, objects retained, schema, retries, repair or acceptance policy. It calls the supplied setter once under pcall and the supplied post-read once under pcall, returning separate status/value/reason observations. Caller CAS/pre-read remains unchanged; no extra Property read or write. One small observation table and two call-local closures per write are bounded, never cached.

Modern Store keeps its full collection checks, committed-vs-candidate visibility, PREWRITE observer, structural uniqueness guard, writing lock through readback, exact equality, failed-reference reservations and post-success commit. Setter throw-after-apply still holds rather than promoting. Legacy collection and worker writes stay unchanged. Expedition keeps owner/envelope/phase/sequence/generation validation and CAS; actual validated postread decides success even after setter throw/false. Unexpected reader exceptions preserve original exception propagation rather than become invented recovery rules. No Expedition mission, save-format, gameplay, numeric conversion or GC change.

T01/T04/T05/T08: helper matrix with before/after throw, false/nil/read exceptions and one call each; both real storage owners preserve different success policies; old/third/corrupt/unreadable/absent/stale/target-sibling/reference reservations; exact pre1/post1 counts; real Store/EF mutation barriers and reentry; unchanged Expedition store/gate/persistence regression under Lua51 doubles. VFS registration only, no startup ordering change. Crew/numeric extraction follows separately. No deployment/main/game launch, no native save-file PASS; final U5 uses current-version new campaign.

### Machine validation evidence

- Stage/status: `S7b1` / `LOCAL_SIMULATION_PASS`; tests=137, passing=137, registered-open=0.
- Source: base `69acc27f54095126497ab64ca0e42758ba06c08c`; dirty=True; input SHA256 `2ccc8962b46bf8845e271239562a20d226a8a90068c8abeb776fe81bd3cbc3a0`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7b1 --output local/refactor/S7b1-B321-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7b1-B321-first/closure.json`; SHA256 `0fae990d41f01f842d8ccffc40e96952170fd3d0e6fd6f76dda067d99b94a6f3`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 63; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5b_real_Store_and_writers": {"native_doubles": "catalogue and carrier presence; actual Store/Flow/EffectiveFacts/Housing/GPP/Probe", "no_write_captures": 1, "real_removal_captures": 2}, "S7b1_city_property_policy": {"baseline": "69acc27", "modes": 8, "post_reads": 1, "pre_reads": 1, "same_commit_protection_and_physical_record": true, "setter_attempts": 1}, "S7b1_expedition_property_policy": {"baseline": "69acc27", "modes": 8, "post_reads": 1, "pre_reads": 1, "same_validated_readback_policy": true, "setter_attempts": 1}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 199, "XML": 25, "package_files": 321, "modinfo": 348}
