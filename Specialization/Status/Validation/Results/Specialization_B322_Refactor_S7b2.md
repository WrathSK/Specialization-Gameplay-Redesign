# B322.349 — S7b2 Crew observations and scoped numeric policy

## Plan and Runtime Impact Contract

Accepted S7b F26/C073/ST-02; base B321.348/f0c0827. Crew save/receiptSave retain CAS pre-read, then clone outside setter pcall, exactly one setter attempt, exactly one postread and exact equality. The save function still separately returns whether setter pcall returned; receiptSave still has no return. Postread exceptions rethrow their original object; clone failure still causes zero attempt and zero postread. Orders, grants, receipts, native creation/binding, completion attribution and retries are unchanged. One call-local observation table per actual write, no retained state/events/timers/new scans. Unit binding stays unchanged for S7d.

The central numeric policy is intentionally scoped: existing nonnegative-finite predicate and strict canonical decimal17 parser move to PropertyCell. Capital keeps its field whitelist, required/optional map and errors; Development keeps its own map/errors and unchanged Encode checks. DECIMAL17_V1 payload bytes and raw Store comparison remain exact. No universal binary32 rounding, structural integer cap, epsilon equality or automatic old-format recovery. The observed Mac binary32 Property behavior is simulated only on already-selected fractional investment fields; no claim about all Properties, hashes, Treasury arithmetic or native save files. MoneyMatches direction/nonzero/.01 allowance remains the existing user-approved policy.

T01/T04/T05/T08: clone/read/throw/false/stale one-attempt matrix; original Crew formation/grant failure/no-replay regressions and actual source differential; pure canonical/extreme/nonfinite boundaries; Capital/Development raw encode/decode source differential; retained binary32 simulation, actual Store/service receipt/reentry/failed writes under Lua51; previous cell two-owner policies retained. No gameplay, amount, eligibility or persistent shape change. No deployment/main/game launch; native acceptance remains U5.

### Machine validation evidence

- Stage/status: `S7b2` / `LOCAL_SIMULATION_PASS`; tests=251, passing=251, registered-open=0.
- Source: base `f0c082750aee92b4d373fcc1aeab18cf652182ba`; dirty=True; input SHA256 `a8fd56791b4022794bf70f9bee5b95adc6e0155e0636fa00d032d6475a5fe534`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S7b2 --output local/refactor/S7b2-B322-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S7b2-B322-first/closure.json`; SHA256 `ca9f9e9ec7ca927cdb0ad60c6ef421e8f074a5509b07edde299d5546b45be5fd`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 78; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S7b2_Crew_differential": {"attempt_replay": false, "baseline": "f0c0827", "modes": 5, "same_order_receipt_grant_and_setter_order": true}, "S7b2_decimal_wire_differential": {"baseline": "f0c0827", "rounding": false, "same_raw_DECIMAL17_V1_payloads": true, "scope": "fractional investment whitelist only"}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 199, "XML": 25, "package_files": 321, "modinfo": 349}
