# B230 — Culture network event readiness and read-only diagnostics

Status: LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED. Source B230.257. Deployment recorded separately below.

## Scope and B229 evidence

User approved the Culture network initialization repair, restored read-only network buttons and retained bounded logs. Expedition task/activity, capacity, binding, history/rewards, Research network, Design, GC, configuration and main remain unchanged. No new timer, forced wake or repeated native command.

B229 native originals remain ignored and unchanged:
- `local/diagnostics/B205/session-20261018T013403Z-71ac25/records.log`: SHA256 `18129f134ff21d37a2ae968f25bad6750975a0a60ad5d94d6f78ab128d2d6ebd`.
- `local/diagnostics/B205/session-20261018T013818Z-7f0e5b/records.log`: SHA256 `94feb12d747fc5926cc94d1305012b57050c28c400a1d9115cb680299ed1c3a2`.

Both show Culture consumer ready=false while Bridge ready=true and input/derived versions agree; the first includes VERIFIED/AVAILABLE input. Later NEEDS_REVALIDATION is distinct from never constructing topology. STATIC_CONFIRMED: Culture Audit returned before initialization unless its sole LoadScreenClose setter had run. Actual-Lua counterexample without that notification stayed empty/zero through normal events; supplying the notification yielded a record/coefficient1. The logs establish the stuck readiness state, not the engine's exact event-delivery reason.

Task evidence: one arrival proceeds ARMED→SLEEP→TASK_RUNNING. Another awake/ready/moves4 unit is denied SLEEP before any request; first redispatch remains denied, second recovers. Neither session captures ACTIVITY_RELEASE/ACTIVITY_WAKE_REQUEST. No new task-repair hypothesis is implemented; earlier successful tasks and unresolved release coverage remain separate.

## Implementation and ownership

- First real Audit (existing network publication, source update, or owner-turn dirty/publish path) validates definitions and performs existing exact derived-carrier cleanup once per module context; only then sets ready. It no longer depends exclusively on LoadScreenClose. Duplicate load notifications audit without erasing rebuilt carriers. Failed initialization can retry on a subsequent real event; no polling or timer.
- Existing AVAILABLE topology requirement, copied input, independent source histories, union, UNKNOWN/HOLD and confirmed-loss cleanup stay intact. No permanent state/schema or whole-network forced refresh is added.
- P0 **网络概况** and **网络来源 / 接收** use the two vacant first-row slots. Their actions route to CultureNetwork.Report, never the old NetworkBridge.Read/Refresh or isolation writer. Right click also reads details. The old isolation implementation remains inaccessible from these visible buttons.
- Reports distinguish not-ready, city/module/network error and input revisions. They show the current Culture coefficient, actual working count on request, expected yield and recorded source contributions. These are current configuration observations, not independent native-yield measurements. Names are UI-only, not trace fields.
- Existing bounded trace receives NETWORK_HEALTH on health/input change, NETWORK_STATE on changed projection and explicit report, NETWORK_SOURCE on explicit detail, and NETWORK_WAIT. Existing64-entry ring/96-record producer budget remains. Unchanged repeated successful audits do not consume new records, even across turns. Small scalar signatures are disposable and cannot authorize gameplay. No worker scan/diagnostic string tree on ordinary successful computation; worker count is read only for explicit reports. Diagnostic failure cannot block reconciliation.

## Validation

121 targeted offline checks PASS:16 new B230 cases plus current Culture projection, B228/B229 diagnostics/release, P0 layout/callback and collector reader suites. Coverage includes missing load event with existing input/no new publication, event publication startup, duplicate load zero-write, cleanup isolation, failed definition recovery, wrong owner, UNKNOWN history, unchanged-update log dedup, late collector snapshot, read-only Gameplay dispatch, no added timer and diagnostics failure isolation.

Command: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<LOCAL_LUPA>:DevelopmentTests python3 -m unittest test_b230_culture_network_ready test_culture_network.Projection test_b229_retained_diagnostics test_b228_native_network_diagnostics test_p0_panel_current_layout test_expedition_trace_reader test_expedition_trace_collector`.

Optional expansion to legacy `test_network_bridge` could not import because it still resolves the pre-migration runtime directory. That invocation did not execute the requested expanded suites; no historical fixture/path/assertion was altered. The scoped121-check command was rerun independently and passed. Full historical gameplay regression, native rendering and native yield acceptance were not performed.

## One combined native session

Start the existing collector manually before loading the current campaign. Do not open P0 to initialize the network. Let normal load/player events settle, then select a known recipient city and read **网络概况** and **网络来源 / 接收** once. Initialization must work independently of those reads. If a connected ACTIVE IV Culture source has all three categories for one foreign civilization, the union contributes +1 Culture per matching working specialist; incomplete sets correctly contribute0. No need to manufacture a complete foreign set merely to check readiness. A positive native yield gate remains pending if no eligible set exists.

During the same session, perform one available ordinary Expedition task through completion and attempt the next task or dispatch once. Existing diagnostics capture release branch/state; failure means retain the log and stop that path, not repeated retries. No cold-load loop, screenshot sequence, timer test or new task acceptance claim. User decision: none. User testing: this combined delta. Primary next: review B230 network and inherited release evidence, then stop for the next authorized batch.
