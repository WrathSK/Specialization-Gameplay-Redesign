# B223 — Native sleep, redispatch and arrival diagnostic

**LOCAL_SIMULATION_PASS; USER_GAME_TEST_REQUIRED.** Authorized diagnostic-only continuation from [B222 native review](Specialization_B222_Task_Start_Native_Review.md). Source package B223.250 / modinfo250. This does not repair or establish the cause of Ottawa's native SLEEP denial.

## Question and preserved behavior

Does manual idle sleep → native redispatch → replacement-unit arrival differ in remaining movement, activity or Spy-operation state from the earlier successful arrivals? Did a denied task finally return to confirmed ARRIVED, or remain protected after an uncertain/failed save?

B222 captured three PEOPLE/PLACES successes and an Ottawa pre-request denial, but not remaining movement or the final acknowledgement/save. The user recalls manual sleep before departure and an arrival-turn attempt in their own turn. The engine reported AWAKE, not continued SLEEP. The missing native predicate remains UNKNOWN. Native `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua` reads `GetMovesRemaining`/`GetMaxMoves` and `GetSpyOperationEndTurn`; the installed chooser requests travel without an explicit Wake. CIV_ASSETS means the installed read-only game assets. Neither observation authorizes forcing movement or waking a unit.

Capacity, source/city binding, identity adoption, target eligibility, centre execution, unique Insight rewards, Store schema, task duration and GC are unchanged. No new timer, polling loop, event registration, operation-permission query, native writer or automatic recovery is introduced. The existing bounded SLEEP confirmation watcher is unchanged. These records are disposable observations, not a second state authority.

## Recorded boundaries

| Existing boundary | Trace stage | New information |
|---|---|---|
| Immediately before native travel permission/request | DISPATCH_BEFORE | Actual departing unit/activity/movement and entry versus requested destination |
| Immediately after RequestOperation returns | DISPATCH_RETURNED | Returned call state, including off-map/zero-move readings; CALL_RETURNED is not arrival success |
| Exact native-name arrival candidate, before optional existing entry-city continuation | ARRIVAL_BEFORE | Direct native arrival versus ENTRY_RELOCATE, pre-continuation movement/activity |
| Arrival state saved with verified Store readback | ARRIVAL_CONFIRMED | Post-continuation sample, confirmed ARRIVED revision and preserved logical team/source |
| Existing idle UI publication, once per revision | IDLE_UI | UI-context native sample after arrival/release/load; not a frame observer |
| Existing task startup and actual failure | ACTIVITY_START / ACTIVITY_FAILURE | Movement/activity sample alongside the separate actual guard, requested/attempted flags and bounded native reasons |
| Request handling, save/failure handling and publication complete | GATE_RESULT | Action/result, exact request/attempt key, mission category where available, current phase/activity ownership, task clock, last confirmed Store revision/phase and state equality |

Each sample reads only optional scalar getters: actual owner/unit/coordinates, remaining/max moves, native activity, ready flag, Spy operation/end turn, owner-turn-active, local player and interface mode. Missing/throwing/nil/invalid getters are explicitly UNAVAILABLE / READ_ERROR / NIL / INVALID_TYPE. They are never guessed as zero or false. Owner-turn-active and interface mode are partial context, not proof of the native UnitPanel's private processing guard. Gameplay and UI readings remain context-labelled and may differ.

`storeStatus=CONFIRMED` refers to the last successfully read-back envelope; `savedMatches=true` additionally establishes that the current saved-field projection matches it. BLOCKED preserves the last confirmed phase and does not claim that the current Property is known. A successful REJECTED acknowledgement means the current, unexecuted task draft was rejected and saved as idle; it does not mean the mission succeeded. TASK and ACTIVITY records can be interleaved by existing synchronous publications; correlate the request key, saved revision, stage and context rather than assuming print order alone.

All stages use the existing schema205 bounded ring and unchanged collector:64 retained rows,96 records per producer, bounded scalar/line output and deduplication. Exhausted producers stop the added native reads. There is no promise of indefinite retention: later events can evict rows; suppressed/error counts remain visible. Final Gate results now survive a short reconnect when still in the ring, even if the original live print was missed. No names, arbitrary engine error bodies, paths or request tokens are added.

## Local validation

**416 targeted tests PASS:**385 runtime/tool fixtures plus31 read-only database/package checks. The385 comprise17 new native-state trace tests,350 prior mission/activity/Store/reader/collector checks and18 existing training-trace integration checks. Python3.14 and the existing temporary Lupa installation were reused; the external gameplay database was opened read-only. Collector fixtures needed permission to create temporary directories under ignored `local/`; rerunning with that access passed all18, without changing assertions or opening a live socket.

The new tests exercise actual Lua modules, not a replacement model:

- Preserve zero/false/-1; sanitize missing, throwing, non-finite and unexpected getter returns; retain failure records when optional unit lookup fails; bound budget and reentrant logging.
- Capture SLEEP before travel, returned native state and changed unit ID at arrival, without any added Wake/travel request. Duplicate permit remains refused.
- Distinguish direct arrival from the existing entry-city PlaceUnit/FinishMoves path. The latter locally shows4→0 moves; **this is a fixture result, not evidence that Ottawa used this path or that it caused native denial**.
- Do not emit ARRIVAL_CONFIRMED on an unconfirmed save. Final rejection distinguishes confirmed idle from HELD/BLOCKED and last-confirmed PREPARING under no-op/malformed/throwing writes. Stale acknowledgements cannot cancel the next attempt.
- Recover the final result through the real fixed offline reader after clearing the live UI mirror, with no live prints or native calls.
- Trace ON/OFF comparison across PEOPLE/WORKS/PLACES gives equal Store writes, one Sleep/one Wake/one unique Insight each, zero task placement, zero Unit Property writes and no extra native travel. Existing training integration also preserves its state/writer equivalence.
- Repeated existing publications do not resample an unchanged idle revision or install a timer. Source diff review confirms no added timer, native operation/command, Property write or GC call.

No native gameplay, performance or cause-closure claim follows from these fixtures. Inherit B222's three successes only within their recorded scope; WORKS availability, Tourism settlement, reattachment and other deferred work remain separate.

## One minimal native capture

Use the current authorized test campaign and a healthy, idle team before the relevant redispatch; do not use a quarantined HELD team or create a legacy-save migration test. Start the existing manual collector from the develop root before the action:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/collect_expedition_trace.py --idle-exit 300
```

1. With the team idle in the current foreign city, use native **休眠**, then **派遣到新城市** using the same path as the failed run. If that UI requires a manual wake, note that fact; do not add an artificial wake as a workaround. This captures the actual departure state instead of assuming that the remembered sleep state survived.
2. On arrival during the user's turn, open **任务**, select one available category, and click **开始任务** once. If denied, stop gameplay testing there and let the collector reconnect/read the ring before Ctrl-C. No repeated blind attempts or forced turn. The new departure/arrival/guard tuple and final Gate receipt distinguish observed state from a missing acknowledgement/save.
3. If accepted, let that single existing task finish, then stop collection. No separate cold-load, all-category or long-run test is requested; the same log captures success and release.

If the path now succeeds, that is a captured successful path, not proof that the original problem is fixed. A controlled awake-versus-manually-slept departure comparison is a later option only if this capture leaves that specific distinction unresolved. No full retest of unchanged lifecycle infrastructure.

## Deployment and stop

Local checkpoint: B223.250 is ready; live remains the last verified B222.249 receipt until the W0003 guarded transaction is recorded below. No configuration change or game launch. Raw collector evidence remains ignored.

User decision: none for this authorized diagnostic batch. User testing: one bounded manual-sleep/redispatch/arrival/task capture after deployment. Primary next: review that evidence and propose a cause-specific repair; no forced Wake, retry or further gameplay implementation is authorized by this report.
