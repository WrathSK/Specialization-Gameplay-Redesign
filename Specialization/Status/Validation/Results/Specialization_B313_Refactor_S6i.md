# B313.340 — S6i current-site locality

## Plan and Runtime Impact Contract

S2–S10 continuing authority; base B312.339/fe8e6c4. Stable/live/main remains B307.334. No deployment or native game launch.

Extract one static read-only UnitSiteFacts helper, with no Start, listener, cache or saved state. Prefer known-city district enumeration; native district/purchase-city location identifies only a candidate city, never authority to consume. Keep original full owner discovery when a locator is unavailable/unknown and preserve unsupported legacy doubles. Known-city raw district read failure remains UNKNOWN/rejected, not an empty successful collection. No new startup dependency or reordering: InvestmentAction still starts before UnitTargets.

UnitTargets full Refresh continues to discover every legitimate target across the owner. A separate disposable ReadAtSite narrows collection to a proven candidate city; every city's original qualification, queue stability, HD GetCityPlots/wonder marker/purchase-city proof and EXACTLY ONE candidate remain unchanged. ReadAtSite never overwrites the marker reply. UnitActions retains its old full-Refresh compatibility fallback for old dependencies/doubles. Settler ReadView preserves the dedicated cap tooltip by locating the district city before invoking InvestmentAction.ReadView. Known-city InvestmentAction only changes its raw district reader; it keeps original first ID/type/completion/coordinates and independent owner checks, without adding ACTIVE/pillage/purchase-city eligibility. Confirm still rereads after INTENT and before unit reservation/consumption.

T01/T03/T04/T05/T08: real Store/Crew/Investment/UnitActions and target candidate collection; cold/UNKNOWN/legacy fallback; no full owner iterator on proven current-city paths; 8/32/64-city growth; original complete marker enumeration, ambiguous two sites, duplicate HD indexes, wrong marker/owner/queue/first anchor, target changes/reused grant, failure after INTENT and no replay. Native district/purchase-city locator behavior remains U5, not local engine PASS. No changes to amounts, qualifications, Properties, receipts, ownership policy, timers, GC or irreversible operation order.

Known existing presentation limitation: UnitActions maps a nested investment HELD caused by changed site to its friendly REJECTED text. The test observes the real nested return and durable INTENT, UNKNOWN receipt, no reservation/debit and no replay; this batch does not alter message classification. Track with S9 presentation work, not a transaction-success claim.

### Machine validation evidence

- Stage/status: `S6i` / `LOCAL_SIMULATION_PASS`; tests=83, passing=83, registered-open=0.
- Source: base `fe8e6c4da5ea0690b4ad1dc1010189d71aa88b3e`; dirty=True; input SHA256 `7ec0575c2809ffa7fa4bc42dc4d7c47fbcfd1f736da0179029e5ebcc30272f4c`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6i --output local/refactor/S6i-B313-first/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S6i-B313-first/closure.json`; SHA256 `d376e16fa4dcfb5677c4aecc279cc629b3a88fa8e3a9771b5301bd8444a312f1`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 61; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S6i_Crew_current_site": {"actual_Store_Crew_UnitActions": true, "cities": [8, 32, 64], "marker_slot_untouched": true, "native_AddProgress_calls": 1, "work": [{"cities": 2, "localDistricts": 2, "ownerCities": 0, "ownerDistricts": 0}, {"cities": 2, "localDistricts": 2, "ownerCities": 0, "ownerDistricts": 0}, {"cities": 2, "localDistricts": 2, "ownerCities": 0, "ownerDistricts": 0}]}, "S6i_investment_current_site": {"actual_Store": true, "cities": [8, 32, 64], "same_potential": 2, "single_unit_consumed": true, "work": [{"cities": 1, "localDistricts": 5, "ownerCities": 0, "ownerDistricts": 0}, {"cities": 1, "localDistricts": 5, "ownerCities": 0, "ownerDistricts": 0}, {"cities": 1, "localDistricts": 5, "ownerCities": 0, "ownerDistricts": 0}]}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 197, "XML": 25, "package_files": 319, "modinfo": 340}
