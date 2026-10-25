# B360.387 — S9c4b bounded UNIT_VIEW consumer

## Plan and Runtime Impact Contract

Accepted U1/D15,S9/F25; base B359.386/3fff36c. UnitPanel VIEW requests now opt into the fixed independent Views endpoint. It no longer reads global UnitActionView replies; Gameplay still maintains that global for DEV/legacy compatibility. Targets/presentation are unchanged. No transaction,qualification,amount,save or preview-owner authority moves into UI.

A single view expectation stores only owner/unitID/token and Lua backend/parent/port/method/epoch identity. Has is a scalar lookup on existing publish/playback boundaries; one Take removes the private message before native selected-unit stamp reads. Envelope and inner view tokens/owner/unit/version/epoch are checked,then the original short-circuit current owner/id/turn/x/y checks,and finally the current parent/port/method/epoch plus not-stopped fence. Sender reads only the original owner/id,without an extra position/turn sample. Selected-unit continuity is still rechecked by the existing renderer. These continuous reads are not an engine atomic snapshot.

Each old cause sends once. Selection/movement/new turn,dirty input,action start,backend/port change,existing2s timeout and shutdown discard only the matching view expectation; they do not clear ACTION pending or its terminal ring. A new endpoint identity is a reliable availability cause on the existing publish boundary. Sending against that endpoint records it immediately,so a service already observed during action-result handling does not cause another view read next publish. No periodic retry or elapsed-time recovery is added. False/throw/lost/evicted/stale data do not resend.

Fixed FailView delivers only VIEW_UNAVAILABLE and no view when a valid typed request cannot publish a positive/negative owner view and the same service remains current. It is bounded/correlated and cannot grant zero values,permission or a plan. UI consumes that negative envelope once and ends waiting. This preserves the old malformed-stamp once-only behavior instead of waiting for timeout and doing a later native render; invalid publication itself still does not evict an earlier valid entry. ReadView executes once and retains original preview invalidation even when transport fails.

Independent review reproduced native GetX triggering Shutdown after Take but before the final stamp. Without a close fence the old stack restored its view and a retained button callback could send an operation. Final consume fences now reject stopped contexts,refresh returns after a close during read,and dispatch checks stopped before any native getter plus again before send. A late button after shutdown performs0 getters/requests. The earlier exact-attempt send guard remains. No additional listener,timer,scan,GC strategy or native object cache.

Work: six exact B359/current cases preserve all tooltips/icons,request counts and native getter counts (crew/settler,prepared/confirmed and P4 cap). The number/crewTips/investmentTips block is byte-identical. Each valid view adds only fixed payload checks/bounded Has/Take/Discard; idle adds0 native unit/city/district reads or requests. ACTION8 and VIEW8 remain independent,total16. Only one view expectation/cached detached scalar projection is retained,with explicit lifecycle release.

T04/T05/T08:13 new tests cover the6-case differential,unchanged formatting helpers,global matching-token spoof rejection,outer/inner wrong metadata,service replacement during final native stamp,shutdown during stamp with zero late-button work,VIEW timeout/selection/shutdown not deleting ACTION records,late endpoint availability exactly once,negative delivery ending wait,observed-port coalescing,and actual failed publication preserving once-only owner work. All32 current S6h Panel/Markers and S9c3 Consumer/real Crew COMMITTED/HELD assertions passed before full validation.

During local editing the initial ReadView replacement range also removed adjacent formatting helpers; they were restored byte-for-byte and now have an explicit golden regression. The current backend-replacement fixture retains the real reply service required by the new protocol while all old expectations remain unchanged. Initial reentry tests installed Take wrappers after capture and thus only proved method-replacement rejection; they were corrected to install before the request so GetX/GetY actually exercise the final native-read fence. No assertion was weakened. No deployment,main promotion,game launch or native PASS. Targets/presentation/training/applied display/adjacency,S10 and exact D7/D5 proof boundaries remain OPEN.

The first inherited896 PASS remains local. Subsequent independent review found one additional dirty-cause/Shutdown path: after rejecting the old view,the same readView stack could send a new VIEW. Close fences now also cover consume return,sender native identity reads and renderer native boundaries. A new exact reentry regression proves no follow-up VIEW or late button work; final2 includes this correction.

Independent read-only final review:13 focused tests and diff whitespace check PASS; the new dirty-cause/Shutdown regression executes native reentry and proves zero follow-up requests/late-button getters. No remaining blocking finding in the three runtime files.

### Machine validation evidence

- Stage/status: `S9c4b` / `LOCAL_SIMULATION_PASS`; tests=897, passing=897, registered-open=0.
- Source: base `3fff36c98042fac622e502ca00842f810d5a2f25`; dirty=True; input SHA256 `0340457cdef9de1eeb0bd9c00f6cf385cbcf63a5fa7e644d16bd43ecd7704930`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9c4b --output local/refactor/S9c4b-B360-final2/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9c4b-B360-final2/closure.json`; SHA256 `e6e3247576e41f1edbfd337841f333b913a8ce03cbce423ac81641e5e2b049d2`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 198; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9c4b_valid_UI_differential": {"baseline": "3fff36c", "cases": 6, "current_transport": "UNIT_VIEW", "extra_native_sampling": 0, "same_tooltips_icons_requests_native_getters": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 387}
