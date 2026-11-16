# B347.374 — S8b7b Commerce partial reputation availability

## Plan and Runtime Impact Contract

Accepted U1/D6/D7 and S8/C005; base B346.373/c589f5b. Configuration failures isolate the fixed commerceKnown/commerce family; independently valid configuration with invalid reputation exposes a detached configuration-only projection plus reputationKnown=false. The raw reputation and its original Known marker remain in the authoritative root. No fake zero history, new storage field, permanent-corruption verdict or repair/reset is introduced. Other independently valid abilities keep operating.

Restoration uses the existing bounded pure copy and full validator before fixed eight-owner checks. Partial validation omits reputation and supplies its redundant Known marker only in the validation copy. Save compares the entire preserved raw reputation and marker before masked full-parent validation; native CAS and readback still use the complete original root. Projection writers cannot supply replacement/false/zero reputation. Configuration transitions retain their original rules while opaque reputation is untouched; admission/ticks/history fallback skip unavailable reputation before native reads. Healthy read/write copy work and saved bytes match exact B346 source.

No new hook,timer,poll,scan,consumer,cache or native read. Partial projection copies only configuration and existing bounded fields; it never copies the unusable archive into a disposable read view. Native writes remain existing explicit Store transactions. No event registration or normal healthy startup order changes.

T04/T05/T08:20 focused Lua5.1 cases cover raw preservation,Known marker repair isolation,forged/metatable/stale candidates,uncertain full CAS,firstP4,ticks,restructuring,loss/return,base strictness and bad configuration. Actual Store+Commerce establishes Gold16,then unavailable reputation gives independently confirmed15; disabling/re-enabling the domain gives0/15 with raw history exact. A thousand idle publish events cause zero writes. Warm PENDING uses existing retained source samples and R0 clamp; cold PENDING without decomposition retains installed16,labels it retained and forbids new trade. Current UI/summary and restructuring views show UNKNOWN rather than a historical zero; Describe does not mislabel retained totals as newly confirmed R0.

Two previous assertions that Commerce was outside reviewed isolation scope are executed unchanged against exact B346 Store; current strict base/template counterexamples replace only those superseded scope expectations. All other inherited assertions remain selected. Independent read-only review reran the20 focused cases. A new copy-work test initially expected1 instead of2 because the native-shape fixture copies the token in GetProperty; the old/new equality assertion already passed. Corrected the measurement expectation,without changing production copy strategy. Reviewer found a non-Commerce restructuring view falsely presenting unknown reputation as0; fixed the default unobserved view and added a real regression.

Full D7 permanent recovery remains OPEN: exceptions/UNKNOWN do not prove irrecoverability. Template-family isolation and D5 native attribution remain OPEN. No deployment/main/game launch or native PASS.

### Machine validation evidence

- Stage/status: `S8b7b` / `LOCAL_SIMULATION_PASS`; tests=703, passing=703, registered-open=0.
- Source: base `c589f5bf747c5960ed5fc868a1122cb7b0f321e7`; dirty=True; input SHA256 `e634b01d6f8cfc547295f67ff5a06923894dc8ff330bd401bdd9147215c3d834`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S8b7b --output local/refactor/S8b7b-B347-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S8b7b-B347-final/closure.json`; SHA256 `7576b4e4193994e5dcf3c295fa700c4e7d2b65e35a9714ab90007c8594837c35`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 169; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S8b7b_actual_Store_Commerce": {"configuration_off_on_gold": [0, 15], "confirmed_gold_without_unknown_bonus": 15, "prior_confirmed_gold": 16, "raw_bad_reputation_unchanged": true, "thousand_idle_writes": 0}, "S8b7b_healthy_copy_work": {"same_as_B346": true, "same_saved_bytes": true, "state_copies": 2, "write_copies": 13}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 374}
