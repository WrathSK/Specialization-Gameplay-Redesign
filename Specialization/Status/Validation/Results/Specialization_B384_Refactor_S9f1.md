# B384.411 — S9f1 / A0183 deferred-lifecycle pure prerequisite

The user explicitly approved both minimal saved-evidence extensions;A0183/Workflow were committed first at5445226. This batch introduces only the bounded pure mechanics for the deferred-lifecycle extension. Production Store/Gameplay do not include or call it yet;no live or saved record gains a field from this batch.

The optional version1 envelope carries a supported parent token/origin and a fixed map of the existing nine ability owners,at most one pending episode per owner. Confirmed caller-supplied loss records its turn,target and owner-change epoch. Later pending episodes coalesce while preserving the earliest unresolved turn and latest loss/reference. Return adds only the confirmed current return boundary. A return-only witness has no invented lossTurn. Repeated notifications preserve the first recorded boundary;reused/reversed epochs,references and time are rejected.

Entry returns a detached witness bound to ability key,parent token and complete episode. Clear requires an exact current witness and matching supported parent,removes only that owner,and returns nil when empty. The model rejects unknown owner/fields,unsupported versions,metatables,bad finite/integer/reference/size constraints and stale/cross-owner/cross-token witnesses. It does not validate or replace ability payloads,prove native outcomes,read a game/save object,emit events,register callbacks,retry or grant recovery authority outside the future Store CAS.

Runtime Impact:one fixed nine-key schema at module load,explicit O(9) validation/copy when called,no cache or unbounded history. ImportFiles merely packages the source;there is no production include or automatic caller. Field encoding and actual persistence/parent validation,Store loss/return ordering and real damaged-ability transforms remain the next cutover,not a claimed completed recovery feature.

T01/T02/T03/T04/T08,L2:fifteen tests cover all nine owners,zero timestamps,duplicate boundaries,multiple pending cycles,return-only,no-work nil,independent clear,detached keys/references,witness drift,versions/unknown fields/owner limits,parent epoch/stage/reference,nonnumeric/nonfinite/reversed time,native-surface guards and a detached JSON/object roundtrip into a new Lua51 context. That roundtrip is a pure model test,not a native Property or game save/load test. Static package compilation/manifest checks cover the new import. The first fixture used the wrong Context wrapper attribute for table construction;correcting it changes no runtime assertions.

User decision:none pending for approved scope. User testing:final U5 after actual Store/network cutover. Primary next:actual deferred-lifecycle capture and recovery,then network source attribution and remaining S9/U4/S10. No deployment,main promotion or game launch.

### Machine validation evidence

- Stage/status: `S9f1` / `LOCAL_SIMULATION_PASS`; tests=15, passing=15, registered-open=0.
- Source: base `5445226fe1eff032f9303621a9a381f9ff8ffe6c`; dirty=True; input SHA256 `179c5265e76fdd26cb872cc327092a725bc30d841270440be73f3c49ed1f4d2f`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9f1 --output local/refactor/S9f1-B384-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9f1-B384-final/closure.json`; SHA256 `604f95bf87782360e7e61dadb48231e5ef5596a06f7e74629504eb6568b89601`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 1; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9f1_deferred_model_bound": {"Store_wired": false, "automatic_calls": 0, "episodes_per_owner": 1, "native_or_Property_access": 0, "owners": 9}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 213, "XML": 25, "package_files": 335, "modinfo": 411}
