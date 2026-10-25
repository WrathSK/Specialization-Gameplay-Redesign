# B372.399 — S9e1 accepted audit intake / R10 and R22

## Plan and Runtime Impact Contract

The user approved current-HEAD audit reconciliation and continued S9–S10. Base B371/db0cb1a. Existing intake records the exact read-only Advisory input hashes and full scoped R01–R29 disposition, including the Crew/Expedition heading typo. No parallel findings registry or Advisory edits. User R01/R05/R18 decisions are retained; no new Design inferred. Specific source-local/cold authority review remains required before that repair.

Before code, the intake recorded T01/T02/T04/T08,L3: use already accepted route trader-ID maps in both Bridge removal callbacks,background UI and diagnostic callback. Probe takes an optional membership map;complete empty is meaningful,false absence returns before FindID. No new cache,scan,event,source of route authority or object retention. Missing snapshots retain the original conservative lookup;operation/start events do not use old membership and therefore still notice new traders. TradeRoutePlundered absent in native Events remains a U5 fact:accepted trader removal still drives negative evidence and collection. Bridge/UI are separately exercised,including real Probe body rather than a relevance stub.

R10 original→actual chain: removed nontrader is no longer findable→Probe previously returned true→Bridge signal and CheckEvidence plus UI dirty collection→PENDING,city census and consumers. Repair:already accepted snapshot membership short circuits before native lookup.1000 nonsnapshot removals now cause0 unit lookup/city scans/signals and leave transaction current;foreign removal stays ignored. Removed accepted trader still invokes original negative proof and blocks transactions;without a snapshot the conservative path remains. The UI uses its own accepted snapshot,not diagnostic AutoRouteProbe guesses. Existing stale snapshot is routing-only,never reliable permission for a new transaction. U5 N4 still verifies native event delivery/order.

R22 original→actual chain:raw fractional native remainder in receipt amount→binary32 Property readback rounds it→exact recursive Same fails before debit/grant. Store only nearest-integer diagnostic amount (maximum locked Crew capacity is below2^24);native AddProgress receives the exact previous fractional min(capacity,remainder). Existing receipt shape,grant locks,Destroy/grant order and no replay remain. Six nonbinary fractional remainders roundtrip through a binary32 storage double and commit one exact original base grant;tampered amount still HELD before debit,with no grant. Other original destructive failures remain covered. D5 native same-tier multi-city attribution is separate and OPEN under the disclosed U5 restriction.

First focused run had43/44 passing:one new cold-UI test wrongly assumed a city dirty mark clears the accepted snapshot. Current UI deliberately retains it. Corrected the fixture to a genuinely unavailable initial complete collection;no assertion about the product was weakened. Final focused44/44 pass. No production recovery behavior was changed for that test.

Only diagnostic receipt amount is intentionally rounded;no gameplay amount,save field/type,Property key,eligibility,history migration,timer,periodic retry or GC change. These are scoped repairs and not a claim that R15 or all S8 performance findings are closed. Default native/multiplier/receipt delivery remains USER_GAME_TEST_REQUIRED;no native CPU/heap PASS.

User decision:none. User testing:final U5,unless a concrete blocking native fact arises. Primary next:continue R15 producer sampling and the accepted schedule;no deployment/main promotion/game launch.

### Machine validation evidence

- Stage/status: `S9e1` / `LOCAL_SIMULATION_PASS`; tests=64, passing=64, registered-open=0.
- Source: base `db0cb1a05f51f0f4b71bb5f6dfd8682c4235794d`; dirty=True; input SHA256 `9ff66b474ed1c1df885c16099e1e5e690318b58adcddaa5491bcc630b7c7f39f`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9e1 --output local/refactor/S9e1-B372-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9e1-B372-final/closure.json`; SHA256 `334dad5e0616c7eae0cdafb4bd5a2c611a5cacdd396721023e6327d856eb5292`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 56; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5c2_busy_refresh_budget": {"initial_captures": 1, "ten_reentrant_causes_additional_captures": 1, "thousand_idle_additional_captures": 0}, "S9e1_Crew_binary32_receipts": {"actual_base_input_unchanged": true, "fractional_cases": 6, "native_grant_calls_per_use": 1, "receipt_integer": true}, "S9e1_nontrader_removal": {"city_scans": 0, "events": 1000, "native_CPU_claim": false, "route_signals": 0, "transaction_stayed_current": true, "unit_lookups": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 399}
