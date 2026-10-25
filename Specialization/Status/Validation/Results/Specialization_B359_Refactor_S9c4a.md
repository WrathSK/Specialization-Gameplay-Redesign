# B359.386 — S9c4a fixed UNIT_VIEW projection and independent producer

## Plan and Runtime Impact Contract

Accepted U1/D15,S9/F25; base B358.385/7c407fb. The existing bounded ring implementation now accepts only two explicit roles: UNIT_ACTION(default) and UNIT_VIEW. UNIT_VIEW admits only UNIT_ACTION_VIEW. It exposes PublishView for a fixed19-field projection; ACTION Publish cannot write a view port and vice versa. This is a fixed protocol extension,not generic object serialization,automatic discovery or an event bus. Target/presentation ports are not added here.

The existing producer factory constructs ACTION plus its .Views service using one validated epoch/version and shuts both old services together. No startup step/order/output declaration changes: both endpoints belong to the existing PlayerActionReplies owner. Each port has its own8-slot ring and index: total maximum16 records across players. VIEW traffic cannot consume or evict ACTION terminal evidence,even with identical owner/token. Current UI VIEW still uses its old global reply and does not opt into this port yet.

View fields are owner,unitID,token,turn,x,y,legal,prepared,reason,amount,progress,cost,baseInput,baseUnused,targetName,planToken,specialization,potential,nextPotential. Owner/unit/token must match the admitted request; legal/prepared are booleans. Number fields retain original finite numeric precision/range with no rounding or recomputation. In particular potential4/nextPotential5 in the existing cap rejection is legal transport. An explicit negative view may have no x/y; no zero coordinates or successful facts are synthesized. Strings are bounded(token/plan256,specialization128,reason200000,target name20000); target names retain a finite numeric metadata key when supplied. Objects/metatables/nonfinite/wrong scalar data reject without evicting valid evidence. Extra native/receipt/plan fields are never copied.

The typed Gameplay VIEW branch validates the exact endpoint/epoch before invoking original UnitActions.ReadView once. It then publishes only to the same current parent/view service. Legacy global UnitActionView and direct return value are retained for DEV/old callers. ReadView's real side effects remain: stale unit/investment plans and previews are cleared as before,and UnitTargetSnapshot save/restore is unchanged. Transport failure cannot undo this owner work or trigger another read. No change to confirmation authority,qualification,amount,save schema or financial history.

Cost is one extra empty fixed view ring at the existing startup factory; at most19 scalar field validations/copies plus O(1) storage per explicitly typed existing view request. No additional native unit/city/district/treasury reads,request,timer,hook or scan. Worst retained text references are bounded to roughly1.8MB for eight maximally sized view messages,plus the pre-existing ACTION1.6MB ceiling and fixed metadata; normal current names/reasons are much smaller. This is an explicit maximum bound,not a native memory benchmark. No native object cache or GC strategy change.

T04/T05/T08:11 new tests cover raw precision,nextPotential5,negative view without coordinates,detached fixed fields,invalid reference/role/port/scalar/metatable/limits,independent capacity under100 view publications,factory epoch+shutdown,actual producer exactly-once reads,legacy global preservation,stale admission before read,service replacement and transport failure without reversing preview cleanup. Actual Crew ReadView states before preparation,prepared and stale-progress invalidation match the existing global exactly and grant0 progress. The prior real ambiguous-grant UI test is strengthened to require the HELD: label,not merely nonnil text. No assertion was weakened.

Next migrate the UnitPanel VIEW consumer with existing source/turn/x/y/selection and service-identity fences,explicit consumption/discard and unchanged2s no-resend timeout. ACTION pending is separate and must survive VIEW cancellation. Global compatibility and targets remain until their own migration. No deployment,main promotion,game launch or native PASS. Other S9/S10 and exact D7/D5 proof limits remain OPEN.

Independent read-only review ran11 focused tests and confirmed field precision/negative states,independent capacity,same-epoch startup/shutdown and preserved ReadView side effects. No remaining concrete blocker; no full rerun by the reviewer.

### Machine validation evidence

- Stage/status: `S9c4a` / `LOCAL_SIMULATION_PASS`; tests=884, passing=884, registered-open=0.
- Source: base `7c407fbe1ce4c92d17ae0b057fb837ca45346113`; dirty=True; input SHA256 `7ad17e33f37f52e3c31fe8de8f5b2f038445e717b6fadee4cd83316d858f8633`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9c4a --output local/refactor/S9c4a-B359-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9c4a-B359-final/closure.json`; SHA256 `98b429e6e4666422320aa2e1476ff212f914ef5970464da2b60c403975a9e198`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 197; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9c4a_fixed_view_capacity": {"UI_migrated": false, "extra_native_reads_per_view": 0, "ports": 2, "slots_per_port": 8, "total_max_slots": 16, "view_fields": 19, "views_cannot_evict_action_ACK": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 386}
