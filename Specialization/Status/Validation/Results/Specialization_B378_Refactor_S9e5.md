# B378.405 — S9e5 / R11 UI turn and worker relay scope

## Confirmed chain

Previously the known-local PlayerTurnActivated in UI/GPPRefresh called mark(false),even after initial factsDirty cleared. It sent LV2_GPP_DIRTY with WorkerOnly=false. Gameplay treated this as structural recovery and called DistrictCompleteness.MarkDirty(playerID,nil,UI_FACTS_DIRTY),then NativeFacts.Workers owner-wide. MarkDirty itself only invalidates scalar state and emits D. At the existing publication,FC/Bindings invoke the declared consumers;real Research writers call D.ReadFacts,and that now-dirty owner cache really recollects city districts/buildings. This happens even if the normal Gameplay turn already warmed D's new-turn cache. The new test runs this entire chain;it does not infer a scan from the notification name.

A known-local UI turn now carries worker recovery only,so it cannot introduce a redundant structural invalidation. The relay remains until native N5 comparison:initial/load/unknown causes retain conservative D recovery,normal workers remain,no new timer or removal of native safety. D's existing turn key still refreshes the first real read each turn;UNKNOWN is not cached as success. Other native/owner-turn reconciliation is not declared eliminated.

CityWorkerChanged(owner,cityID,...) now preserves one positive scalar city scope through the existing packet. Base UI Panels/CityPanel.lua OnCityWorkerChanged(ownerPlayerID,cityID) and WorldView/PlotInfo.lua OnCityWorkerChanged(owner,cityID,plotX,plotY) establish the UI argument layout. No native city lookup is needed to mark it. Duplicate same-city causes stay narrow;different cities,unknown IDs,focus,load and other conservative inputs widen to the existing owner fallback. This deliberately does not introduce a city queue or new transport array. City zero is preserved. Gameplay admits optional CityID only for WorkerOnly=true,FactsChanged=false and a strict finite integer range;malformed or conservative packets cannot use it to narrow recovery. The native Focus producer remains conservatively owner-scoped;this batch does not claim all worker paths are exact-city.

The UI detaches the pending scalar scope before send. Failure merges the original scope with real reentrant causes without rearming the retry budget by itself. A genuinely new event may rearm as before. Known duplicate turns cannot widen a real queued worker city;load/unknown still can. This is cause transport,not new gameplay or saved authority.

## Evidence and limits

T01/T02/T03/T04/T05/T06/T08,L3. Nine new tests join actual separate UI and Gameplay VMs,copy only scalar packet fields,execute the actual request function and real DC/FC/Bindings/Research writers. The baseline B377/6b6bf00 and current case first run the normal Gameplay turn,then deliver the UI turn. Redundant D captures fall2->0 across two cities while carrier configuration stays equal;worker reconciliation still visits cities and is measured separately. Known single-city worker changes cannot touch a throwing sibling;two real changes in one turn and UNKNOWN->new UI cause recovery retain correct values. Conflicting/invalid/foreign/zero scopes,initial/load/focus/unknown,duplicate turns,reentry and the existing three-attempt transport behavior are covered. Existing observer failure,real GPP/Chair,depth invalidation,network non-invalidation,busy/scoped writers and D reference/availability checks remain.

Native N5 UI/Gameplay event coverage,engine callback order,CPU and heap are USER_GAME_TEST_REQUIRED. No relay removal or claim of zero total native work. No Property/save/GC,eligibility,amount,transaction or startup-order change. The initial local fixture omitted existing Scalar/token setup and assumed a reentrant real cause could not rearm its own retry budget;the corrected fixture follows the unchanged ingress/rearm contract,not weaker product assertions.

User decision:none. User testing:final U5,including N5 coverage. Primary next:accepted remaining source-local/cold/Store/display findings,remaining S9,U4,S10. No deployment,main promotion or game launch.

### Machine validation evidence

- Stage/status: `S9e5` / `LOCAL_SIMULATION_PASS`; tests=49, passing=49, registered-open=0.
- Source: base `6b6bf0046c44cf3a9c7ca767f64b13fd2f878b31`; dirty=True; input SHA256 `c0a6430b023afba2c5f6190333e873cf7214dee2eaf8a0c015a5eeacb5b46614`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9e5 --output local/refactor/S9e5-B378-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9e5-B378-final/closure.json`; SHA256 `012207b83133e18eb311fcf36388d94277250b24e43f7978d057facaf0c8d201`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 45; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5c1_known_city_invalidation": {"affected_city_recaptures": 1, "mark_native_captures": 0, "unrelated_city_recaptures": 0}, "S5d1_two_actual_writers_known_city": {"city_visits": 2, "unrelated_city_visits": 0, "writers": 2}, "S5d4b2_UI_idle": {"governor_requests": 0, "initial_requests": 1, "thousand_idle_extra_requests": 0, "worker_requests": 1}, "S9e5_GP_turn_then_UI_turn": {"after": {"D_captures": 0, "building_checks": 0, "city_visits": 6, "native_double_reads": 244, "writes": 0}, "baseline": "B377", "before": {"D_captures": 2, "building_checks": 682, "city_visits": 6, "native_double_reads": 928, "writes": 0}, "chain": "actual UI packet->Gameplay request->D/FC/Bindings->Research writers", "local_cities": 2, "native_CPU_heap": "USER_GAME_TEST_REQUIRED", "worker_recovery": "retained;not zero all-module work"}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 405}
