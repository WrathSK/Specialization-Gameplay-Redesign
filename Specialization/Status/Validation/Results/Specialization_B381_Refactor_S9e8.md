# B381.408 — S9e8 / R13 Capital confirmation continuity

The observed chain is Capital.Request -> successful original receipt/debit -> full explicit response -> later TreasuryChanged (or its two existing alternatives) -> Mark(owner) -> quote-free automatic Refresh. The last step discarded the freshly read balance and marked all terms stale even though the notification reported the same balance. Existing coverage receipts correctly handled causes already present during the explicit request,but not this later independent notification.

At the existing Treasury producer callbacks,one guarded GetTreasury/GetGoldBalance pair now samples a finite scalar. Existing known-view entries are compared without city/district/building/source collection. Only differing or unavailable sampled balances are marked. No-index/unreadable/reentrant delivery retains conservative owner invalidation. Other role/network/Commerce/source and reentrant causes are never cleared;source scope and current reference/save authority remain unchanged. A fresh same-balance notification is not a new fact and does not force new speculative pricing.

This changes display invalidation only. Confirmation still requires current revision/token,its original new selected-domain prepare,current native funds,exact Store receipts and the same irreversible order. No old quote is promoted merely because balance matches. A real treasury change or unknown reading still invalidates;new signing cannot bypass fresh revalidation. No new cache,Property/schema,listener,timer,periodic retry,automatic signing or money rounding.

Runtime Impact: one balance read per delivered accepted-player Treasury event plus traversal of the existing scalar known-view index. Foreign notifications and idle publication perform0 new balance/source/depth reads. The additional fact read is explicit;this is not a zero-native-work event or a measured native CPU/heap improvement. Auto drains still never construct speculative quotes.

T01/T02/T03/T04/T05/T06/T08,L3:ten focused test methods compare exact B380 Capital source with current production,compose actual Store/Capital and actual panel in separate Lua51 contexts,and cover all three Treasury names,mixed-view invalidation,before/during/after debit notifications,new same-turn balance changes,independent marks,unknown/native reentry,no-initial-index discovery,1000 idle boundaries and strict stale rejection without RNG or another debit. Existing Capital transactions/native-money readback/reentry/HELD/sidebar/observer and S6 shared-fact gates remain selected unchanged.

The first test draft attempted a second Start on the same Store and correctly hit EXIT_REGISTRATION_CONFLICT. The final no-index case uses original startup without its fixture's optional initial Refresh;the runtime registration guard is unchanged.

User decision:none. User testing:U5 N12 same native callback continuity and actual rendering. Primary next:accepted remaining R19/R05/Store/applied-owner/U4/S10 work. No deployment,main promotion or game launch.

### Machine validation evidence

- Stage/status: `S9e8` / `LOCAL_SIMULATION_PASS`; tests=124, passing=124, registered-open=0.
- Source: base `db42d26201c2db285c8b35672890e8fb27e4d04c`; dirty=True; input SHA256 `0ff3fe8d32f1abf5cb4fe72f66afb6827bf3a9ba71e7c2f4184df8de19209fb5`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9e8 --output local/refactor/S9e8-B381-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9e8-B381-final/closure.json`; SHA256 `5b8dace5e0346805f7a324cc7e3003bde37825a6646204f26632e90d2c8b53ec`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 56; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Current-batch measurement: `{"S9e8_Capital_delayed_Treasury": {"after": {"balance": 750.09375, "depthReads": 0, "money": 1, "nativeBalanceReads": 1, "revisionChanged": false, "sourceReads": 0, "stale": false}, "baseline": "B380", "before": {"depthReads": 0, "money": 1, "nativeBalanceReads": 0, "revisionChanged": true, "sourceReads": 0, "stale": true}, "native_CPU_or_heap_claim": false, "native_order": "simulated independent delivery"}}`. Prior measurements remain at their original reports and in the identified local artifact.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 408}
