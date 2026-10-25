# B352.379 — S9a2 selected owner-view production refresh

## Plan and Runtime Impact Contract

Accepted U1/D15,S9/F16/PROP-N3; base B351.378/b72caae. Existing CapitalInvestment/DevelopmentInvestment/Commerce producers already publish per-city view.revision. Only the production-list adapters receive a new optional observer via their existing CrewProjectOrder registration. Standalone constructors without it retain the original module-revision behavior; independent dashboards/lastRequest/ack/token handling are untouched. Crew/Claim/Dialogue/Engineering handshakes and Expedition training are separate pending scopes.

Each observer keeps exactly one backend Lua table reference plus one fixed scalar header: selected owner:id,row presence/revision,token and reference scalars. rawequal source replacement resets the slot even with identical numeric versions. No City handle,complete view/reference table,receipt or list is retained. Invalid/unknown row version/reference is not cached as confirmed; recovery is observed at the next existing owner publication/render boundary. Reference/token changes and same-turn second changes cannot reuse an old header. Existing module revision remains the cheap Publish gate,so idle Publish adds no UI.GetHeadSelectedCity read. On a real owner change,the existing selected-city lookup and already published view select whether to notify; other-city changes no longer cause redundant selected-city refresh. No new selection listener is needed: native selection/open already invokes Items.

Only successful Items filtering/writeback records a rendered row. Protected rendering errors leave the prior observation and SafeAdapters list rollback intact. Publish latches before synchronous notify reentry. Each production adapter owns a distinct observer; Close releases its backend and disables late observer Publish work. Lifecycle/capacity is fixed per existing panel instance,not a growing cache or new authority.

Development previously deleted views directly without advancing its output revision. Its existing publish now accepts nil,compares old/new exactly,and increments only for a real removal; the no-city Refresh path uses it while preserving quote/open-view cleanup. Capital and Commerce already publish deletion this way. This fixes the UI version contract only: amounts,eligibility,transactions,physical carriers and saved history are unchanged.

No new native facts,event,timer,poll,request,business calculation or saved field. Observers read existing published scalar output only; declaration allocates3 bounded observers once. Unchanged module revisions cause zero extra native selection reads; changed module revisions read the selected city as before. Fixed scalar comparisons replace unnecessary Refresh broadcasts. No native performance claim; only measured simulated work scope.

T04/T05/T08:13 focused Lua5.1 cases run all3 actual UI modules,real production registry injection and actual Development producer. Cover other-city suppression,1000 idle Publish0 head reads,same-turn changes,deletion/reappearance,selection via Items,backend restart at identical revision,changed token/reference,unknown-to-known recovery,failed Locale rendering/list rollback,synchronous notify reentry,legacy constructor behavior,Close and weak-collection proof (no complete view/reference or closed backend retained). Actual Development deletion advances output once,repeat deletion advances0,and money calls/balance/Store writes stay unchanged. All previous actual UI/adapter/handshake regressions remain inherited.

Read-only preparation identified both the existing Development deletion gap and a candidate render-cache error. The latter was reproduced with actual CommerceUI/SafeAdapters: observing before Locale failure suppressed recovery. Observe is now after successful list writeback,with a targeted regression for all3 modules. No existing assertions were weakened or frozen for this slice.

D7 permanent history/money proof boundaries and D5 native attribution remain OPEN. Remaining S9 training owner revisions,target rules,channels,applied display and adjacency are not claimed complete. No deployment/main/game launch or native PASS.

Independent read-only review reran all13 focused actual UI/observer/producer cases and confirmed the failed-render fix,scalar reference boundary,backend generation reset,Close release and nil-safe Development publication. No blocking discrepancy remained.

### Machine validation evidence

- Stage/status: `S9a2` / `LOCAL_SIMULATION_PASS`; tests=760, passing=760, registered-open=0.
- Source: base `b72caae691c42a40d88fa0c3ec167404f8dc1211`; dirty=True; input SHA256 `7ce1b461e24b33b492c0c2ccdb52ce6ca937f64082f270da323d5654bc427f96`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9a2 --output local/refactor/S9a2-B352-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9a2-B352-final/closure.json`; SHA256 `f04bcc2b127ad1d432f049d55bb1d9e1f38c7c9b3367c239344ca80fd4a1b97e`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 180; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9a2_selected_owner_view": {"production_adapters": 3, "request_or_native_queue_change": false, "same_city_change_notifications": 1, "thousand_idle_extra_head_reads": 0, "unrelated_city_refresh_notifications": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 379}
