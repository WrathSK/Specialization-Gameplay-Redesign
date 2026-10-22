# B072.99 Runtime Performance Audit

Document Owner: Codex
Implementation: develop only; no deployment; D0025 unchanged
Evidence: STATIC_CONFIRMED / LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED for native filesystem capability and actual turn delivery
Milestone: instrumentation implementation candidate, NOT yet a confirmed long-play logging candidate

## User conclusion

Low-frequency bounded collection and a standard-Lua file sink are implemented. Native Civ VI Lua file access is NOT established. This is a capability-gated implementation, not a claim that Civ VI exposes io/os. If unavailable, the observer reports DISABLED once and never retries this counter session. Until an actual file is obtained in one authorized test, do not promise a full-game history or call this requirement fully validated. No print/database/Property fallback hides that gap. Main and live B071.98 remain unchanged.

## Filesystem evidence / remaining blocker

Read-only searches of installed base-game and HD/Workshop Lua found no usable native independent writer/rotation precedent. HD tools/maptest io.open calls run offline, not in the game. Native Automation.Log exists but has no verified independent file retention contract; not used. Executable strings are not proof of Lua API availability. Current Mac Logs directory exists; no directory creation or game configuration change is performed.

The adapter requires io.open and os.getenv in UI context. It resolves HOME and appends the existing native Mac log directory. If either API or directory permission is unavailable, it fails closed. os.time is optional; no shell, RSS, RNG or gameplay request is used. Other platforms are not claimed supported. Native file capability is an IMPLEMENTATION_LIMITATION / USER_GAME_TEST_REQUIRED, not a Gameplay Design decision. If absent, this batch is not sufficient for the user's automatic long-play evidence objective; a separate collection transport needs investigation/authorization.

## Output

Current machine target, only after approved deployment and native capability success:
`~/Library/Application Support/Sid Meier's Civilization VI/Firaxis Games/Sid Meier's Civilization VI/Logs/SpecializationRuntimeAudit-01.tsv` through `-08.tsv`; `SpecializationRuntimeAudit.index` is the bounded serial index.

TSV schema 1: comment header contains session/segment serial, optional start Unix time, build B072.99, modinfo99, starting turn and source_base=407717c (parent source commit, explicitly NOT this implementation commit). Serial index identifies sessions even when clock unavailable. Each load/new Gameplay counters instance starts a new session; segment rotation retains that session id. Current file and state appear in existing Performance Counters / Snapshot output. No new UI buttons.

Exactly one successful row per engine turn at Events.LocalPlayerTurnEnd. Native TradeOverview uses this event (static registration precedent, not live proof). Counters are cumulative differences between two local-player end-turn boundaries, including AI processing between them; initial row is marked partial. This is NOT solely that player's action time. Existing counters are Mod-wide; city/routes/version metadata is local-player scope. No per-event data or payload stored.

Columns: session/build/modinfo/turn/interval start/partial/optional elapsed seconds; player/city count/current verified route count/input and derived revisions/validity; current inflight/session peak inflight; network player bucket count/local input-presence count/diagnostic event entry count. These three shallow table measures are memory proxies, NOT RAM or complete heap accounting. City count uses GetCities():GetCount(), not enumeration. No derive/read-effective-facts/audit calls.

All 40 existing fixed counters are recorded as interval delta, cumulative total, peak observed interval delta: unit callbacks and ignored; revalidation/scans/publications/same snapshot; derive/facts/city/district/building checks/writes/property writes/send/receive; Lv3/Boost/Standardization/Commerce/Copy audits; busy/duplicate/inflight skips/timeouts/failures/invalidations/manual snapshots; fact and input versions/duplicate/publications/withdrawal/revalidation unchanged/stale inputs; requested/executed/cache hit/miss/input version changes/derived invalidations. Timeout is NOT labelled retry count: a separate retry counter is unavailable. Native internal Modifier writes remain unobservable. No Crew Property dump or scan of large receipt tables; no expensive private cache traversal to invent missing metrics. Manual read count is not incremented by logging.

## Anomalies / boundedness

One anomalies column per summary, one entry per fixed type/turn: derive>128, derive>32 and zero cache hits, combined building create/remove>256, current inflight>1, send timeouts>3, any confirmed withdrawal (review marker, not necessarily error), route failures>3. Counts retained as type:count, no exception payload/stack history, no generic error-listener added. Thresholds are diagnostic, not balance. Current interval may be lost on mid-turn crash; errors before summary or native allocation sites cannot be reconstructed from this log alone.

Eight circular segment files, each <=4 MiB, total <=32 MiB plus <=32-byte index. At session start/size rollover overwrite only the next owned filename; never inspect/delete other Logs. Long sessions can span segments; more than eight segments/sessions overwrite oldest evidence. Copy all eight files after an incident, before subsequent repeated loads. File cap is enforced before append. Rotation writes a header separately; ordinary completed turn appends/closes once. Close flushes the Lua stream, not a guarantee of OS fsync/power-loss durability. No persistent open handle. Header/index initialization is once per session; no idle timer. Any read/open/write/close failure disables this session without unbounded retry or queued buffer.

Memory: <=64 fixed counter keys accepted, currently40; previous totals and interval peaks, scalar session metadata. Temporary row/delta/flags created only on turn end, never retained as history. No per-event hook added. No runtime table size grows with turns. Only ExposedMembers diagnostic state is set, never Game/Player/City Properties or Building state.

## Local validation

`DevelopmentTests/test_runtime_audit.py`: 1,000,000 actual counter increments produce zero additional file writes and same node count. 10,000 stress turns use real Lua stdio to a temporary directory:12,745,257 bytes across4 segments, fixed395 retained nodes (logger+counter test structure), rotate at4MiB; 12 more sessions leave exactly8 bounded segments+index. Anomalies deduplicate; duplicate turn ignored; disk failure disables; absent io/os reports DISABLED; event observer unregisters; no idle loop; all Lua compiles / modinfo references valid. Unknown values serialize NA.

`DevelopmentTests/test_runtime_audit_regression.py`: preserves B069/A/B behavioral assertions with only current manifest stamp adaptation; 168 three-way Network outputs, cold/warm cache and previous native-write models pass. Additional20 actual Network input transitions yield identical full Network output, Building/Property writes and all counters with logger ON versus OFF. Not a native game test or evidence that55GB memory incident is fixed.

## Minimal native gate (only after user authorizes temporary deployment)

Load a disposable copy of a save. Read Performance Counters once: Runtime audit must be ACTIVE and provide a file path. End one normal turn. Confirm a new TSV has a header and one row; another read alone must not append. If DISABLED, provide reason and stop this validation; no long game is needed to establish missing file API. No claim that logging works until this gate passes. After a long game/incident provide the eight prefixed TSVs and index, approximate turn and symptom; no full game Logs directory required. Mid-turn native crash may leave no final row.
