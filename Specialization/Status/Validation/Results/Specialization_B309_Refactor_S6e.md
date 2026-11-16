# B309.336 — S6e lazy Capital quotes

User resumed the accepted S2–S10 program after B307 deployment and record cleanup. Source base efdfaaf/B308.335; stable/live remains B307.334. No automatic main promotion/deployment/game launch.

## Runtime Impact Contract

Capital keeps existing reference/Store/ACTIVE/held-contract qualification for its entry and actual contract state. Background refreshes no longer calculate speculative quotes, network sources, D, history or balance. OPEN/REFRESH and post-confirm window response still calculate the original full quote. Confirmation freshly calculates the selected domain, re-reads balance/contract state and retains original receipt/native money rules. Other-domain failures remain independent.

Refresh preserves its explicit full default for existing direct consumers; only the known automatic flush passes false. Retained public quote terms are marked stale after any automatic update and cannot authorize signing in UI or Gameplay. No new visibility latch, long-lived cache, event, timer, retry or persistent field. A bounded receipt inside the existing dirty queue acknowledges only causes present before a successful explicit quote; siblings and reentrant/new cause versions remain pending, and receipts expire with the queue. Actual receipt/qualification changes still publish. T01/T04/T05/T08: actual quote and UI closures, selected-domain fresh reads, stale terms, exact money and no replay. Existing assertions unchanged; no native performance PASS.

## Scope correction

A first unshipped worker-reader prototype exposed a cold read-phase nested EF call inside the legacy Development D fixture (its anchor decorator called T.control), plus an incomplete synthetic Commerce Store.Investment double. Only Primary-owned experimental source edits were restored after preserving the patch, fixture and precise rejection under ignored local/refactor/S6e-worker-prototype-1/. Read-only reproduction identified these as fixture boundaries, not proof of a production Store defect. Its guard was not weakened; the pending worker migration remains the next S6 obligation with corrected independent fixtures. No earlier committed S6 work was discarded. Full local artifacts are not permanent backups.

## Validation plan

Count quote/source/history/balance reads separately from required entry/contract/reference checks. Actual background dirty flush must do zero speculative quote reads; idle notifications must not retry. Explicit OPEN/REFRESH matches prior amounts; stale UI/direct confirms do not debit, and selected-domain validation does not scan other domains. Confirmation afterward may refresh the full displayed quote and must be measured separately. All real transaction/receipt regressions remain selected by impact.

## Fixture compatibility and observed counterexamples

The first selected run failed 36 receipt subcases because their historical binary32 Property double used string.pack/unpack, unavailable in Lua 5.1. A new test-only profile uses Python struct IEEE binary32 conversion for exactly that expression; old assertions, rawget absence, quantized Treasury and actual Store/service remain unchanged. The second run passed 89 tests. Three added event-order regressions caught and verify the dirty-cause acknowledgement described above; the final selected run passes 92 tests (15 new cases). No assertion was removed or weakened. Legacy whole-file historical-source equality and obsolete UI fixtures are not selected by this runtime cutover; current sidebar and all original transaction/receipt/guard assertions are selected.

### Machine validation evidence

- Stage/status: `S6e` / `LOCAL_SIMULATION_PASS`; tests=92, passing=92, registered-open=0.
- Source: base `efdfaaf132c9676a80c461e94f1d673c8559b1dc`; dirty=True; input SHA256 `e3dfcf9a60a7b4973a2e235cc93b2f109c15dc3f99c23b6954432a5aa66e944c`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6e --output local/refactor/S6e-B309-third/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S6e-B309-third/closure.json`; SHA256 `c918eef856f7d380a2a146ae8f98d99f7728ec69d4848cf276708c27dfd7cfa0`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 52; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S6e_Capital_automatic_quotes": {"background_balance": 0, "background_depth": 0, "background_history": 0, "background_sources": 0, "idle_extra_work": 0, "idle_publishes": 1000, "original_background": "full3-domain quote per qualified tracked city"}, "S6e_Capital_confirmation_sources": {"after_validation": 1, "balance_and_contract_fresh": true, "before_validation": 3, "post_response": 3, "total_after": 4, "total_before": 6}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 196, "XML": 25, "package_files": 318, "modinfo": 336}
