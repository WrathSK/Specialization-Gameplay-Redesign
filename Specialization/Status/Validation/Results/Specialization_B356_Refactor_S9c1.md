# B356.383 — S9c1 bounded player-action terminal reply primitive

## Plan and Runtime Impact Contract

Accepted U1/D15,S9/F25; base B355.382/12dac60. This prerequisite introduces only the pure PlayerActionReplies module and its package references. There is no include/caller in UnitActions,Gameplay or UI yet. Existing player buttons still use their original reply path; DEV,UnitActionView,UnitTargetSnapshot,UnitSiteFacts and CrewPrecision are untouched. No production behavior or startup order is changed by this slice.

New(epoch,version) takes explicit finite session allocation metadata; it performs no native/exposed-state allocation. Fixed scope UNIT_ACTION admits only PREPARE/CONFIRM,with exact reply epoch,nonnegative integral owner/unitID,nonempty token<=256 and version<=128. Reply payload is detached fixed scalar owner/token/action/unitID/epoch/version/text plus a fresh outcome projection containing only status/kind/phase. No native object,amount,plan,full financial receipt,callback or command is retained. Unknown extensions in the input do not become payload. No Property/schema,source qualification or transaction rule.

The eight-slot publication ring has O(1) Has/Take/Discard and a fixed owner+token index. It retains the last8 publication positions minus explicit consumption,not necessarily eight unconsumed results. A duplicate currently retained key does not replace the first terminal evidence. Take removes private storage before returning its detached record. Discard affects only the exact owner/token. Shutdown empties the service and rejects old operations. New services are independent. Strings are immutable Lua values; text<=200000,outcome fields<=128 bound the rare worst case to eight bounded messages (up to1.6MB text references plus fixed metadata),with normal current action text much smaller. Has allocates no payload copies.

Retention is a bounded session delivery window,not a permanent backup or a transaction deduplication authority. An evicted/consumed/closed-session result is unavailable; it must never imply cancellation,rollback,success or permission to replay an irreversible action. No instruction/action callback exists in the module,so it cannot retry or execute anything. After consumption/eviction the same key may be published again as another message; only the original action owners' persistent receipts/guards decide transaction legality. The future UI must generate unique tokens,match owner/unit/action/version/epoch/current backend,and preserve existing no-auto-resend timeouts. No FIFO eviction will erase authoritative transaction state because none is stored here.

T04/T05/T08:12 focused tests cover detached payloads/no native extensions,cross-player same token,two delayed tokens,first retained terminal wins,1000 publications never exceeding8,exact Take/Discard,old service shutdown,new epoch isolation,invalid scopes/actions/IDs/epochs/tokens/sessions/limits,oversize rejection without silent truncation or valid-evidence eviction,and10000 scalar Has calls without consuming. A test removes all Game/Players/Map/Events/GameEvents/ExposedMembers/Property/GC globals and still uses the full kernel. No timer,poll,new hook,scan,automatic consumer or native-object cache is added.

Next: instantiate at the actual Gameplay owner result boundary,declare its startup output and failure cleanup,then migrate only UnitPanel prepare/confirm ACK. Keep native transaction owners,three Run return values,reply-before-fact-observer order,DEV compatibility,view/target/scoped-site duties and scalar timeout semantics. Actual owner/consumer composition,DEV interleaving,observer failure and backend/reentry tests are required before claiming the player migration complete. No deployment,main promotion,game launch or native PASS. Remaining S9/S10 and exact D7/D5 limits stay OPEN.

Independent read-only review reran12 focused tests and found no blocker. Capacity8 is per service instance across all players,not8 per player; cross-player eviction is allowed within this transport window. First terminal wins applies only while retained; authoritative transaction receipts are never in this ring.

### Machine validation evidence

- Stage/status: `S9c1` / `LOCAL_SIMULATION_PASS`; tests=848, passing=848, registered-open=0.
- Source: base `12dac60499dab9a05e6fac1c8160fb747cf41ede`; dirty=True; input SHA256 `f6efee2eefe5c4da15bea2387426abffa4613218b0c0dc430ac7c3462d8b5a7d`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9c1 --output local/refactor/S9c1-B356-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9c1-B356-final/closure.json`; SHA256 `a0ce92bded9ebd9a1b8f729ad3bb348cadb5f7c2ecf25938e10ec820c23dc662`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 196; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9c1_reply_capacity": {"capacity": 8, "maximum_retained": 8, "production_wiring": false, "publications": 1000, "retention": "last8 publications minus explicit consumption", "transaction_or_replay_authority": false}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 383}
