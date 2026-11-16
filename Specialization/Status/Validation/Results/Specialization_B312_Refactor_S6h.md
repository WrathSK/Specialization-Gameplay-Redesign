# B312.339 — S6h event-driven unit UI

Base B311.338/0e1b20f. Continued S2–S10 authority. Stable/live/main remains B307.334. No deployment/main promotion/game launch.

## Runtime Impact Contract

UnitPanelActions and UnitTargetMarkers stop .2/.25-second native unit/reply polling. Publish/Playback consumes matching reply slots; selected-unit UI/selection/mode/local-player/load events act immediately because UI events need not cause GameCore publication. Production, district and unit events preserve conservative unknown scopes, ignore proven foreign/other-unit signals, and coalesce work until publish. RuntimeUIRevision remains a scalar compatibility invalidation, so a genuinely new global revision may still request a selected-unit read; owner-scoped shared transport is S9.

Existing SetUpdate callbacks now ONLY advance scalar elapsed time and expire existing 2s/10s warnings. They read no game facts/replies, render no controls/lens, dispatch no request and never re-arm work based on elapsed time. No new timer, periodic native work, cache, persistent field or gameplay rule. Actual backend replacement, token/owner/unit/turn/position and selection must agree; UnitTargets appends only presentation turn/x/y to its response. Synchronous replies, pure UI changes and callback reentry are handled without auto-replaying actions. Existing generic action ACK and separate read slots remain until S9; prepare/confirm payloads and irreversible Gameplay checks are unchanged. Owned marker cleanup preserves a newly selected native Great Person/Naturalist lens.

T01/T04/T05/T08: actual UI scripts with explicit native/control/lens/request receiver doubles, actual Store/Crew/UnitActions consumption and original actual target assertions, plus retained Capital, D-filter and other-SPC health closure. Idle publish+scalar-clock work is measured separately from one necessary request/ACK render. Parent hierarchy readiness, actual UnitMoveComplete/selection delivery, cross-context reply timing and native pixels remain final U5 checks. Recovery after local control/lens errors requires a real new UI/fact/load cause, never idle retry. No native performance PASS.

## Current finding recheck

- Ext-F11: CHANGED/resolved by B309 elimination of automatic multi-recipient quotes. The original scan §190 concerned several commercial destinations repeatedly reading the same source. Automatic flush now exits before all D/balance/source/history reads. Explicit OPEN is one destination; confirmation intentionally refreshes one domain and funds/contracts. Existing private currentView(true) does not Capture/Refresh; a new cross-request snapshot would add complexity and stale-fact risk with no current automatic shared-work hotspot. Retained S6e tests and a real Bridge no-Capture/no-derive proof cover this closure; no shared snapshot implementation is claimed.
- F32: original D feedback path already fixed in S5d4a; exact health ownership and OTHER-SPC yield dependencies remain necessary. Retained real tests protect both. Dead CityBuildingsChanged in CultureMeaningProbe is S10 probe-duty cleanup, not a newly diagnosed production loop.
- F33 remains open: full marker discovery, UnitActions current-site lookup and InvestmentAction site checks still enumerate owner districts/cities. This batch adds response stamps only and does not mislabel those scans as eliminated.

Event scope note: optional UnitTeleported payload remains unverified and is conservatively treated as a UI context change, without assuming player/unit parameters. A scalar cause version preserves actual reentrant signals even when native control/lens calls throw; absent a new cause, exceptions do not retry.

### Machine validation evidence

- Stage/status: `S6h` / `LOCAL_SIMULATION_PASS`; tests=147, passing=147, registered-open=0.
- Source: base `0e1b20f9adf3a6e6f8e701f82660f82a3745f1cb`; dirty=True; input SHA256 `71f12aaca2243d824b354945c7688b4cbe2d4e4b51a7a92638542b326cd26898`; stable=True.
- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.
- Command: `python3 DevelopmentTests/run_refactor.py --stage S6h --output local/refactor/S6h-B312-final2/closure.json`.
- Environment: `{"backend": "Lua 5.1", "implementation": "CPython", "lupa": "2.8", "machine": "arm64", "platform": "Darwin", "python": "3.10.13", "python_hash_seed": "UNSET", "sqlite": "3.43.2"}`.
- External input: `{"configured": true, "recovery": "EXTERNAL_INPUT_NOT_ARCHIVED", "sha256": {"database": "fa7578c3c2e2f19dee918b3801c627ce6edf526ce6d94e04c71a83038c2c215b"}}`.
- Full artifact: `local/refactor/S6h-B312-final2/closure.json`; SHA256 `f1ce2ca9bf47e780968adc011bff3ab52945407fa3b983883998b82e5dff45e6`; stdout/stderr alongside it.
- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.
- Executed modules/fragments: 71; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.
- Measurements (changed from prior artifact): `{"S5d4c10_commerce_health": {"permanent_writes": 0, "repair_writes": 1, "thousand_idle_reads": 0}, "S6e_Capital_automatic_quotes": {"background_balance": 0, "background_depth": 0, "background_history": 0, "background_sources": 0, "idle_extra_work": 0, "idle_publishes": 1000, "original_background": "full3-domain quote per qualified tracked city"}, "S6e_Capital_confirmation_sources": {"after_validation": 1, "balance_and_contract_fresh": true, "before_validation": 3, "post_response": 3, "total_after": 4, "total_before": 6}, "S6h_markers_idle": {"idle_publishes": 1000, "lens_operations": 0, "requests": 0, "scalar_ticks": 1000, "unit_getters": 0}, "S6h_panel_idle": {"idle_publishes": 1000, "known_foreign_signals": 2000, "layout": 0, "requests": 0, "scalar_ticks": 1000, "unit_getters": 0}}`.
- Limits/mocks: `{"exclusions": {"historical_unrelated_suites": "Selected program scenarios only; inherited stage regressions are named when selected. No old assertions modified."}, "native_mocks": ["synthetic owner/city/district/building methods", "explicit catalogue stub for D workload fixtures", "B270 seven real writers with native doubles"]}`; LOCAL_SIMULATION only.

Static package: {"Lua51": 196, "XML": 25, "package_files": 318, "modinfo": 339}
