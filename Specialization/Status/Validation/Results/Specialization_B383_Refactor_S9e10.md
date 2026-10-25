# B383.410 — S9e10 / R19 Dialogue presentation roles

Read-only source trace:Base ProductionPanel.lua862–889 renders candidate ProjectItems from TurnsLeft;RefreshQueue2677–2706 calls ProductionHelper.CreateQueueInstance83–177 for later entries. That helper sets the project icon/name and queue index,with no TurnsLeft/status field. HD DL_ProductionPanel changes data/item decoration and retains those native queue roles. This Mod's CrewProjectOrder native queue wrapper only adds the existing Claim icon decoration;TimedProjectDisplay.Items instead affects the candidate list,and Current affects the current header/banner. No third-party/game file was modified.

A concrete display conflation exists in that candidate overlay:a known noncurrent Dialogue item can borrow ACTIVE/CALLING/HELD text from the city's current timer view because Items always calls DialogueProjectUI.Text. It now uses a pure fixed-duration preview when native IsCurrentProduction is explicitly false. Missing flags retain the original conservative path. No timer/history/current-queue read is needed for that known preview;unrelated project models stay unchanged.

For the native-current Dialogue with no confirmed timer,the ambiguous 确认中 becomes 待计时. Its tooltip explains the existing requirement to occupy the production queue alone for a full turn and wait for Gameplay confirmation. Current ACTIVE=1,CALLING=待确认,HELD=已暂停 and their authoritative reasons remain exact. This introduces no project state,selection,queue mutation,cancellation,Begin,completion,retry or polling. A multi-item queue is still rejected;silently becoming size1 cannot rearm an old intent.

Runtime Impact/T01/T02/T03/T05/T08:static text and one pure preview function,existing disposable item fields only,no new dependency/cache/listener/save or native sampling. Seven targeted tests run actual UI/controllers and the exact native wrapper fragment,plus maintained project-reader/selection/recovery and fresh work-slot interpretation regressions. They cover known noncurrent vs native-current,missing native flag,all three current states,queued selection rejection,no display-triggered Begin,1000 idle publications,and unchanged native wrapper arguments/return identity.

Evidence limit:source and local simulation do not establish the exact UI cell from the original reported screenshot. Native queued cells cannot display this string through the inspected path;actual screenshot placement/rendering stays U5. This correction addresses the verified candidate/current ambiguity without fabricating an extra queue status or changing project rules.

User decision:none. User testing:U5 distinguish a later queue icon,a candidate list row and the current project header/banner. Primary next:accepted R05/R02/applied-owner/U4/S10 work. No deployment,main promotion or game launch.

Selection correction:the initial865-execution artifact at local/refactor/S9e10-B383-final/closure.json remains FAIL because an unrelated Crew transaction measurement ran twice through inherited S9b2 profiles and direct S7d5. All other cases passed. The final selection names the relevant current UI/selection/handshake/completion classes directly;it keeps all new presentation checks and original strict project guards without rerunning unrelated cumulative history or altering the duplicate-measurement assertion.

### Machine validation evidence

- Stage/status: `S9e10` / `LOCAL_SIMULATION_PASS`; tests=48, passing=48, registered-open=0.
- Source: base `6581d5ec55e5d4e023b72fa7eb9b2c6156e3370a`; dirty=True; input SHA256 `266bc879d78fd1f1cc9663391c7510a8e77ef30720b0bb2c331756638aae9cb9`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9e10 --output local/refactor/S9e10-B383-scoped/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9e10-B383-scoped/closure.json`; SHA256 `e0b17cb00023f812ffa79513a362cf9764aebae01e92c8f09418b5134bfbf34b`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 49; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Current-batch measurement: `{"S9e10_presentation_roles": {"automatic_begin_or_completion_added": false, "current_status_without_timer": "待计时", "known_noncurrent_queue_reads": 0, "native_queue_cell": "existing icon-only wrapper unchanged", "original_reported_location": "USER_GAME_TEST_REQUIRED"}}`. Prior measurements remain in their original reports and identified local artifact.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 410}
