# B362.389 — S9c5b bounded target Marker consumption

## Plan and Runtime Impact Contract

Accepted S9/F25,D15; base B361.388/a19bff2. UnitTargetMarkers opts into the independent UNIT_TARGETS endpoint and stops reading UnitTargetSnapshot as its reply. Original full global DTO,ReadAtSite,UnitSiteFacts fallback and CrewPrecision/UnitActions snapshot preservation remain. No business qualification,amount,unit operation or save changes.

One expected reply captures owner/unit/token,builder preview and backend/parent/port/epoch/Has/Take/Discard identities. Scalar Has runs only on existing publication; Take removes the private slot before native selected-unit continuity and original owner/id/turn/xy checks. Envelope and inner token/stamps are exact. The same service/methods,selection/cause generation,builder mode and open context must still hold after native visibility and lens boundaries. Projection stays in Gameplay; UI preserves its original visibility filter,sorting,colors and lens.

Selection/move/turn/mode/toggle/new dirty input,backend change,old10s timeout and shutdown discard only this expectation. Other ACTION/VIEW slots and other target tokens remain independent. New endpoint identity is one reliable availability cause; absent/failed/evicted/late/malformed/negative replies never retry on elapsed time or unchanged publication. Fixed TARGETS_UNAVAILABLE has no synthetic successful empty or partial map. Old send frames cannot clear newer expectations or resume after shutdown. Only detached bounded scalar DTOs and one expectation are retained,not native units/cities. No new native listener,frame read,timer,scan or GC policy.

Independent review reproduced two old lens-retirement reentry gaps: GetType can select a GreatPerson before returning the old unit kind,and ClearLayerHexes can do so before ToggleLayerOff. The old stack then cleared/disabled the new native layer. clear now releases its ownership first and fences both native boundaries with existing cause/selection generation. A new selection cause during old ineligible sampling is retained for the next existing publish instead of being overwritten by dirty=false. GP/Naturalist lens protection remains; no second native resample is added. Shutdown during stamp,visibility or paint cannot issue another request or reopen a layer.

T04/T05/T08,L3 for session/reentry transport:16 new focused tests include6 exact B361/current comparisons of status,visible sorted plots,requests,native getters/selected calls and lens operations; no differences. Additional cases cover same-token global spoof,another reply overwrite,outer/inner mismatch,explicit negative/4097 overflow,selection/toggle cleanup isolated from ACTION/VIEW,eviction/late timeout,new endpoint once,native closure/service reentry,GP/Naturalist protection and both retirement boundaries. Actual UnitTargets+Gameplay+transport+Marker with32 cities performs one original scan/request/paint;1000 idle publications add0 scans/requests/Store writes. All36 new+existing S6h UI assertions pass.

The first combined fixture lacked Probe.Scalar required by the actual Gameplay request boundary; added the explicit pure fixture stub,without changing production or original assertions. A nested vararg test closure was corrected for Lua5.1 lexical rules. No deployment/main/game launch/native PASS. Presentation dual-consumer/channel and applied-owner outputs,training owner signals,adjacency and S10 remain; exact D7/D5 proof limits stay OPEN.

The first924 PASS artifact remains local. Final independent review found a remaining nil-key cleanup reentry: clear could receive a new legal selection,then its old caller overwrote dirty=false. Added the same post-clear cause/close fence and an exact regression. Final2 includes16 new tests; reviewer initially passing15 tests was not treated as unconditional release.

Final independent read-only review reran all16 focused tests and diff whitespace check:PASS,with nil-key cleanup cause preservation explicitly confirmed; no remaining blocking issue in the reviewed scope.

### Machine validation evidence

- Stage/status: `S9c5b` / `LOCAL_SIMULATION_PASS`; tests=925, passing=925, registered-open=0.
- Source: base `a19bff2edb883aa9719e16ad90f030b97e21b2d7`; dirty=True; input SHA256 `2b0625c98a3b32d756e8fddb1ff77a142dadddeb441c2b456926180db47e6db1`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9c5b --output local/refactor/S9c5b-B362-final2/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9c5b-B362-final2/closure.json`; SHA256 `019fa27dcc3c801e8e4b320f475345aa948282892bb6b9732e6fd6c3af76034e`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 200; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9c5b_actual_marker_idle": {"Store_writes": 0, "cities": 32, "real_UnitTargets_Gameplay_transport_and_UI": true, "requests": 1, "scans": 1, "thousand_idle_extra_requests_or_scans": 0}, "S9c5b_marker_differential": {"baseline": "a19bff2", "cases": 6, "global_reply_consumed": false, "same_status_visible_sorted_plots_requests_native_getters_lens_operations": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 212, "XML": 25, "package_files": 334, "modinfo": 389}
