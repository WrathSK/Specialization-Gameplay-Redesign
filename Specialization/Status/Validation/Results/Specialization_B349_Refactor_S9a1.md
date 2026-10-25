# B349.376 — S9a1 fixed production-panel adapter registry

## Plan and Runtime Impact Contract

Accepted U1/D15,S9/F16/PROP-N3; base B348.375/cffee6a. Registration remains in original constructor order. Each existing SafeAdapters.Add now optionally declares fixed scalar rank/method metadata for Render,Before,Publish,Pulse,Warm,Queue and Connect. Each phase has its own sorted order; no inference from constructor order. Only seven declared phases,rank1–100,maximum16 steps per phase; no dynamic discovery. Metadata is copied,validated before construction and installed only after that constructor/exports handling completes,so reentrant construction cannot publish its own incomplete phase.

Render retains Training→protected Restructuring ObserveTraining→Crew→Capital→Development→Commerce→Claim/Dialogue/Engineering Sync→TimedDisplay. Before retains Capital→Development→Commerce→Crew→Engineering→Dialogue→Claim→queued overflow guard→TimedSelection→native. Native queue checks retain their exact per-step count,short circuit and live-function lookup; native errors still propagate at the same boundary. Publish/Pulse/Warm/Queue each retain their different adapter ordering. Hooks remain individual native callbacks installed at the same locations,including event-major queue registration. Connect is still last,Claim→Dialogue→Engineering. Unit wrappers,icon decoration,crew sorting/owned filtering and original shutdown stay intact.

Existing Items/Call/Before/Hook preserve list rollback,SPC fail-closed/native fail-open,exports identity cleanup,failed listener quarantine and individual errors. Native selection parameters and multiple return values pass through unchanged. Gameplay startup and dependencies are untouched. Owner revision migration is a separate pending S9 slice; no refresh policy is changed here.

No new native read,event,timer,poll,cache,request,save field or automatic consumer. Phase tables live only inside the existing production-panel adapter instance,holding existing adapter references and fixed scalar descriptors. Small declaration checks/insertion sort occur once at existing registration; render/selection traverse the same fixed steps and make the same native calls/copies. No performance gain claim. Errors/missing backends still take original recovery paths.

T04/T08:8 focused cases run actual previous/current production-panel and SafeAdapters with trace-equivalent native-shaped backends,covering complete constructor/render/selection/publish/warm/queue/connect/close ordering,all8 Before failures,selected constructor failures,render observer error,queued sink/direct native failure,and a native queue function replaced by an earlier callback. Registry tests cover detached phase metadata,phase/rank/method/duplicate rejection before constructor,and reentrant construction. Existing S3 adapter/listener shutdown checks and real S7d project UI combinations remain inherited.

## Scoped remaining D7 proof boundary

Nine owner groups have session isolation,not a permanent-irrecoverability classifier. A validation exception/repetition/time/UNKNOWN is insufficient. Known marker reconstruction is complete; complete independently valid template ledgers and strict already-completed Claim identity may support further deterministic metadata/terminal cleanup,which remain separately pending. Age/pause history,Dialogue used eras/serials,Engineering completion receipts,Expedition city archives,and Capital/Development unmatched native money outcomes lack independent complete substitutes. A total/count mismatch does not prove which side lost history;current buildings/gold/works cannot replace those authorities. Preserve affected data and report exact limitations; do not label permanent HELD a finished normal policy or reset a guessed zero. These boundaries do not block this independent behavior-neutral UI registry slice. D5 attributable native completion proof remains OPEN.

No deployment/main/game launch or native PASS.

Independent read-only review reran all8 focused differential/registry cases and confirmed each rank,listener count/order,reentrant construction boundary and identity-safe shutdown. No blocking discrepancy remained.

### Machine validation evidence

- Stage/status: `S9a1` / `LOCAL_SIMULATION_PASS`; tests=728, passing=728, registered-open=0.
- Source: base `cffee6a7cdd203e5de5204ab830e6f49b95c89d8`; dirty=True; input SHA256 `e63d43fb05a1d64540d76597f298b1772a992e33676943cd57bdcd9d5ec831ac`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S9a1 --output local/refactor/S9a1-B349-final/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S9a1-B349-final/closure.json`; SHA256 `4e33f1fe8dd49792c2f1b844d88bf90e10ad5e48f20ff88f8704a9c2556e7ed8`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 174; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S9a1_actual_UI_phase_differential": {"baseline": "cffee6a", "listener_merging": false, "native_parameters_returns": true, "same_construct_render_before_event_connect_shutdown_order": true}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 209, "XML": 25, "package_files": 331, "modinfo": 376}
