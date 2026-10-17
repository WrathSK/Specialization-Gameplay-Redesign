# B205.232 — bounded Expedition reload/training diagnostics

2026-10-15 local evidence; configuration restoration completed on 2026-10-16 UTC. Authorized diagnostic implementation only. **LOCAL_SIMULATION_PASS; native root cause UNKNOWN; not deployed.** Live package remains B204.231. This patch does not repair population, force the training price, clear retained contexts, change capacity/source/persistence, or change GC.

## B204 native evidence and corrected chronology

B204 normal training can now enable **派遣到新城市** without opening P0. That narrow success is not an overall training PASS: the user reproduced population16→2447 at training completion, cost1 and severe process-memory growth (approximately70–80GB). Further uncontrolled repetition is suspended.

The latest controlled sequence, reported by the user, is:

1. Full game restart → load → train: normal.
2. Full restart → load → train → dispatch/task: normal; then reload within that process → train: approximately80GB and forced exit.
3. Full restart → load → train, without dispatch/task → same-process reload → train: population corruption, without the memory runaway reported in this attempt.

This strengthens the same-process-load association and shows prior travel/task execution is not necessary. It does not prove reload alone is sufficient, every cold start is safe, the two symptoms share one cause, or native memory is being overwritten by this Mod. The three newest screenshots show only the successful T91→93 no-reward task: arrival/source/name confirmed, native mission−1, source turns0→0, native completion events0, completion1/1 and activity released. Later failure branches remain **USER_REPORTED_FAIL**, not pictured in those three images.

The overflow test project was selected after the original population change. It cannot explain that first change. The earlier successful branch involved a pre-existing travelling team arriving, P0 END, then a saved baseline and new training; Forbidden City was selected later. Do not merge these timelines.

Private original evidence remains unchanged under `local/legacy-workspace/Specialization/Status/Validation/Evidence/B204/`: `native-20261015/`, `memory-interruption-20261015-220827/`, `native-followup-20261015-2230/`, and `same-process-reload-20261015/`. The last archive retains3 inspected screenshots and6 selected logs with matching source/archive SHA256, manifest and review. No authentication log, screenshot or raw log is published.

## Static findings and limits

- [Unit definition](../../../../Mod/Data/ExpeditionSpyGate.sql) first inserts a prototype cost1, then the B202 update copies the loaded Spy formula. Current source/live SQL and the latest configured DB read resolve60 with previous-copy progression15. The reported/native log cost1 is therefore a real discrepancy to observe, not permission to change the accepted formula. A current DB is not a timestamped description of every earlier load branch.
- No direct population setter was found in the scoped Mod path. The current [Training](../../../../Mod/ExpeditionTraining.lua) owned access marker and native queue actions remain candidates for boundary observation; their native signatures match the inspected HD usage. NULL PopulationCost also occurs on the ordinary Spy and is not a diagnosis. Native GameInfo Index must not be substituted with SQLite rowid.
- The Gameplay Gate has per-start loaded state; production UI supplies a callable queue reader through ExposedMembers. Their native same-process lifetime is not established by local mocks. Whole old Gate retention alone would normally deny a second training attempt through occupied capacity, so it does not explain the observed sequence by itself. Store expected-current readback guards remain in force.

## Applied diagnostic scope

[ExpeditionTrainingDiagnostics.lua](../../../../Mod/ExpeditionTrainingDiagnostics.lua) adds disposable scalar-only observations at existing context initialization/load, eligible production-row display before training, explicit admission, native build request, matching birth/completion, marker mutation and finish boundaries. It samples owner/city/population, current GameInfo type/index/hash and reverse lookup, definition cost/model/step/PopulationCost, ordinary Spy definition cost, native Expedition cost/progress, queue size/current hash, marker presence, existing reservation/phase/receipt flags and queue-reader provenance. It performs no new Store read and never controls admission or recovery.

The ring contains at most64 records, each line at most4096 characters,96 emitted records per observer context and a bounded stage-dedup map. Repeated identical stage observations do not emit another record. After the budget, sampling stops and a capped suppression count increases. Roles/context markers and observed LoadScreenClose counts describe only these observers, not a canonical engine session identity. If ExposedMembers survives a reload, prior scalar provenance remains visible; if it is recreated, a local trace alone cannot compare the missing old session. No functions/native objects, unbounded history or persistent Properties are stored in the trace. One disposable selected-row key reuses the displayed cost and suppresses redundant diagnostic reads on unchanged renders; cost, observed-load or context changes permit a fresh pre-training sample. No new frame/turn scanner or timer is added.

The existing independent naming UI hosts one diagnostic LuaEvents listener, removes it on shutdown, and attempts bounded `UI.DataError` output (at most128 calls per host). Replacement hosts claim only the diagnostic sink; no production/name bridge is cleared or repaired. Missing/throwing output leaves the ring available; errors lock that sink and never change training outcomes. `CALLS_RETURNED` does not prove disk output. The installed Civ VI/HD CitySupport use confirms the static DataError surface; this specific automatic disk sink remains native-unverified.

The normal player window is unchanged. **人文考察·验证 → 刷新报告** appends a short last-eight-record diagnostic view. Two localization pairs are added: `LOC_SPC_EXPEDITION_TRAIN_DIAG_HEADER` and `LOC_SPC_EXPEDITION_TRAIN_DIAG_STATE`. Technical detail is available from the ring/log, without requiring the panel to initialize collection.

## FireTuner read path — actual native result

The user explicitly authorized backing up configuration, temporarily enabling Tuner, loading and waiting without training/ending a turn, then restoring the setting. One fixed read in advertised `GameCore_Tuner` returned turn88, ExposedMembers=`table`, SPC_P0=`table`. This is native evidence that a loopback query and its printed response work on this Mac. It is **not** evidence of passive background streaming, every Lua context, the B205 ring (not deployed), or the population fault's cause.

After the user exited, an automatic OS process check preceded restoration. EnableTuner is0 again; the entire configuration is byte-identical to its pre-probe backup. No game was launched by Primary, no gameplay command was submitted, and no turn/training was requested. Backup, exact query result and restoration hashes remain in ignored `B205/tuner-preflight-20261015/`.

The independent stdlib [fixed reader](../../../../tools/read_expedition_trace.py) supports only `probe` and `trace`, one localhost4318 connection, exact advertised context selection, a five-second overall deadline, bounded frames/bytes/records and guaranteed socket closure. There is no arbitrary Lua argument, retry/watch loop, automatic configuration change or game launch. It prints only per-request tagged output, never unrelated engine messages. Protocol reference: [civ6-logger architecture](https://github.com/PatrickJYKang/civ6-logger/blob/main/docs/ARCHITECTURE.md); no third-party Mod/client installation or copied client implementation. Its final CLI is offline-tested; the earlier minimal probe supplies the native transport evidence, not a live certification of the full trace reader.

## Local verification

**529 distinct targeted tests PASS**: inherited478 Expedition tests,22 diagnostic-module counterexamples,13 actual Training/Gate/Store integration cases,16 bounded socket-reader cases. The only existing assertion update is the package version231→232. No historical behavioral assertion is weakened.

Diagnostic ON/OFF comparisons preserve saved fields, writes, capacity/source identity, marker operations and final phases across both event orders, duplicates, cancellation, loaded training and failure paths. Synthetic population changes are distinguishable when present before completion versus injected inside marker removal; they do not reproduce the native cause. Tests include definition60/native1, absent markerfalse, read/print/sink exceptions, reentry, bounded rings/sinks, retained ExposedMembers with context recreation in either order, shutdown and failed transport. Throwing optional diagnostics/lookup cannot enter business failure handling or skip recovery. Full native engine population/cost/memory behavior remains unknown.

Python3.14/Lupa2.8 Lua55 used in an isolated temporary dependency directory. The configured external gameplay DB was opened read-only and copied in memory. Raw targeted output and the exact local runner remain in ignored `B205/local/`. Package/import/localization checks PASS:218 declared files plus modinfo=219 source files, one diagnostic import, two matched language/placeholder pairs.29 changed active Markdown links/anchors PASS; current selector/context/hash and diff checks are retained alongside that output. Status frozen history is unchanged. None is native PASS.

## Stop and next distinction

B205 is locally complete only; no deployment in this turn. Capacity, source binding, persistent schema/records, training formula, travel/task semantics, Design, GC, main and external runtime are unchanged. Runtime source has diagnostic hooks only.

Do not request another uninstrumented long test or automatically repeat the80GB reproduction. Once a diagnostic package is separately deployed through the existing gates, first open the eligible production list without selecting training, then compare cold-load and same-process-load observations **before training**, using the fixed reader if the user separately authorizes temporary Tuner for that session. Cost/type/marker/context divergence may already locate the fault without ending a turn. If those observations agree, decide a single bounded training observation from that evidence, with an explicit stop on abnormal population/cost/memory. This is a proposed continuation, not a request to test now or authorization for an automatic reproduction.

User decision: none for this completed diagnostic batch. User testing: on hold. Primary next: review this checkpoint and arrange any deployment/native collection under its applicable authorization; do not begin a gameplay repair or later Expedition slice.

## Deployment and authorized pre-training comparison — 2026-10-15

B205.232/modinfo232 **DEVELOP_ACTIVE**, source `505695dfdb0058c970d4a9fa40f4e45d68f14df6`, receipt `B205.232-505695d-playtest.json`. Fresh automatic OS checks confirmed game exit immediately before both guarded B204→stable→B205 switches.219/219 source/runtime files MATCH; outgoing B204 and stable recovery packages verified and retained; no pending deployment transaction. Main and gameplay semantics unchanged; no game launch or native result claimed. This supersedes the earlier local-only stop for deployment only.

The user authorizes the following no-training comparison and temporary Tuner use. EnableTuner is now1 after a fresh exit check; only that setting changed. Original configuration backup and restoration checkpoint are in ignored `local/legacy-workspace/Specialization/Status/Validation/Evidence/B205/cost-read-preflight-20261015-232136/`. **Restoration is pending until this comparison ends and the user fully exits the game.** Preserve any unrelated later configuration changes when restoring0; verify and record the outcome. Prior completed preflight remains frozen.

1. User cold-starts and loads an existing baseline from before training, with no pending Expedition TRAINING/NAMING recovery transaction. Do not manufacture a new baseline. Open the original qualified Culture ACTIVE IV city's ordinary production list and locate/hover **人文考察团** without clicking it. No P0 or turn. Stay there and notify Primary.
2. Primary captures the fixed `trace` output once, saves it as checkpointA and confirms that UI_ROW describes this city/cost; missing trace or row is UNKNOWN, not a reason to train. Do not start the next load before A is retained.
3. User reloads that same save within the same process, opens the same list/city and notifies Primary. CaptureB once and compare turn/population, definition/native cost, type/index/hash/marker identity and observed context/load provenance. Retain A outside the game because the in-memory ring may be recreated.
4. After the two reads, the user fully exits; Primary restores EnableTuner0 and verifies against the backup.

The list still runs existing qualification SYNC; this is not a claim that no gameplay script executes. It sends no training order. Distinguish one turn from one Production. If actual cost1, population change or obvious memory growth appears, stop at that checkpoint, retain the available read and exit; do not continue the reload sequence or reproduce training. Missing eligibility/trace, stopped budget or context ambiguity is reported without P0 creation/recovery. If no suitable pre-training save exists, report it instead of constructing one. Equal A/B only means no difference was observed before training, not that the B204 fault is repaired or training is safe.

User decision: none. User testing: the two gated no-training observations above. Primary next: captureA, then B, then restore configuration after confirmed exit; no unrelated implementation.

## Checkpoint A, handoff and corrected record — 2026-10-16

Recorded by Primary (Claude, W0005 `4081e49`) after a read-only handoff review. No code, package or game state changed for this section.

**Checkpoint A (cold load, eligible production row, before training).**
- The first `UI_ROW` sample for Edinburgh(Test) city393220 at T88 shows:
  - population16;
  - unit `UNIT_SPC_EXPEDITION_SPY` (index244, reverse lookup matching);
  - definition cost60, `COST_PROGRESSION_PREVIOUS_COPIES` step15, ordinary Spy cost60;
  - **native cost1**, progress0;
  - marker absent.
- This met the stop condition, so checkpoint B (same-process reload) was not collected.
- Population stayed16 in every record.
- Cost1 is therefore present at a cold load. It is not specific to a same-process reload.
- What the trace does not establish:
  - the final charged price;
  - why native cost differs from the loaded definition;
  - any connection to the population or memory faults.

**Trace provenance.**
- The same trace contains two complete click→reserve→marker→build cycles (reservations `:2` and `:7`). Between them, the queue count went1→0 and the current item changed, and an explicit cancellation released capacity.
- The user confirmed these were their own clicks to test whether reading worked. The session's interactive Tuner connection had timed out. There is **no automatic trigger**. These cycles are not part of the no-training comparison.

**Reader defect.**
- The advertised `GameCore_Tuner` context has no `rawget`. The original reader treated the native `ERR` reply as a timeout.
- Commit `8963218` changes only `tools/read_expedition_trace.py` and its test. It does not touch the runtime package, and its tests were not recorded when it was committed.
- Its validation is part of the authorized collector batch.

**Configuration.**
- At handoff, after a fresh OS check that the game had exited, `EnableTuner` was restored to0, byte-identical to the original backup (ignored `B205/cost-read-preflight-20261015-232136/`).
- The user then decided that **during development `EnableTuner` stays1 and the user toggles it from the terminal**. The user set it to1 on 2026-10-16 with the CRLF line ending preserved, and Primary verified it read-only.
- This supersedes the earlier "restore to0 after the session" instruction for future sessions.

**Corrected population chronology** (user report, retained in ignored `B204/same-process-reload-20261015/`):

| Run | Sequence | Result |
|---|---|---|
| 1 | Full restart → load → train | Normal |
| 2 | Full restart → load → train → dispatch/task, then same-process reload → train → end turn | ~80GB memory, forced exit |
| 3 | Full restart → load → train, then same-process reload → train | Population anomaly at training completion; no memory runaway |

Separately:
- Training, then saving, reloading and completing the training, already showed the anomaly at completion.
- Loading, producing something else for one turn, then training did not avoid it.
- The overflow test project was chosen only *after* the first anomaly, and is not a cause. The earlier Advisory attribution to it is withdrawn.
- The cause remains UNKNOWN. The leading boundary to observe is restored or reloaded training state versus fresh training after END.

**Next (authorized 2026-10-16):**
1. this records update;
2. an unattended, read-only Tuner trace collector (tools and local tests only, no runtime package change) that turns the B205 ring into local log evidence, partly replacing screenshots.

No gameplay repair, deployment, user test or later Expedition slice is authorized.

## Unattended trace collector — 2026-10-16

This is an authorized tools-only batch. It changes no runtime package and requires no deployment.

**What the collector does.** [collect_expedition_trace.py](../../../../tools/collect_expedition_trace.py) replaces the interactive "tell Primary when you are in game" flow.
- The user starts it once. It waits quietly for localhost:4318.
- It repeatedly runs the existing fixed read-only `record` capture: one ring snapshot plus a 30 s passive window per connection. It reconnects across loads.
- It deduplicates exact `[SPC][B205][TRAIN]` records and writes ignored `local/diagnostics/B205/session-*/records.log`, `events.jsonl` and `summary.txt`.
- It flags per-city population changes, and each distinct native-versus-definition cost mismatch once.
- It ends when the game has been gone for 30 s (default; was 120 s), on Ctrl-C/SIGTERM, or at a 12-hour cap.
- It builds no command of its own. It sends no gameplay operation, changes no configuration and launches nothing.

**Evidence status.**
- The B205 ring prints every record (`Mod/ExpeditionTrainingDiagnostics.lua:57-59`), so passive capture is the primary path. The repeated snapshot covers prints missed between windows.
- Passive delivery over the socket remains native-unverified; the snapshot path is native-observed.
- The `UI.DataError` sink did not reach `UserInterface.log` in the checkpoint A session (0 B205 lines). Disk output therefore depends on this collector.

**Local verification.**
- Reader: 36 tests PASS under Python 3.14 / Lupa 2.8 (validates `8963218`).
- Collector: 6 offline tests PASS under Python 3.10 and 3.14. They cover record extraction, deduplication, population and cost alerts, waiting and reconnecting, exit after idle, non-fatal trace errors, the duration cap, the local-only directory, and the absence of any command construction.
- Smoke run with the game closed: the collector waited, stopped on SIGTERM and wrote its summary. The smoke artifacts were removed.

None of this is a native PASS. No gameplay repair, deployment or user test is authorized by this batch.

## First collector session — 2026-10-16 (USER_GAME_TEST, diagnostic)

**What the user ran.** Cold start, first load of one save, train once, end turn. The collector ran unattended and ended on `GAME_EXITED`. Its session folder is ignored `local/diagnostics/B205/session-20261016T102624Z-f62c2c/`: 24 unique records from 3 observer contexts.

**Native observations.**
- Passive socket delivery worked: records seq5–14 arrived live. The snapshot also worked: seq1–4 and 15–24.
- Records seq5–14 (T88, cold load, `loads=1`) cover: eligible row → order → reserve (`TRAIN:P0-B-205.232:2`, prior phase ENDED) → marker created → native build → queue count1.
  - Population is 16 throughout.
  - Native cost is 1 against definition 60/15 (the same mismatch checkpoint A recorded).
- The first T89 record is `BIRTH_ENTRY` (seq15, unit 3407901), and it already shows **population 2447**. Completion (seq17–19) and Finish with marker removal (seq21–24) all follow at 2447.
- Engine `Player_Stats.csv` records 54 for the test player at T89 start.
- `City_BuildQueue.csv` T89 records the Expedition completed with 342.3 production added, 1 needed and 107.3 overflow.
- An AI knowledge row for the city records 2447.
- `UserInterface.log` contains no B205 lines, and `Modding.log` shows no load error for this Mod's files.

**What this establishes.**
- The jump happened during the player's T89 city processing, after the T89 stats row and before the first Mod handler that observed the training (unit birth).
- None of the Mod's traced code wrote anything between seq14 (T88) and seq15 (T89).
- This session reproduced the fault on a **cold start's first load**. Same-process reloading is therefore not necessary for it, although which save was used still matters.
- Cost 1 is present from the eligible row onward.

**What it does not establish.**
- Which native step, or which other script, changed population.
- Whether that change was one step or many increments.
- Whether cost 1 is related.

The memory runaway did not occur. Cause remains UNKNOWN.

**Collector maintenance in the same batch.**
- The default idle exit is now 30 s (the user found 120 s too long).
- A deadline during the Tuner context handshake while the game loads now counts as waiting, not as an error.
- 7 offline collector tests PASS.

## B206 population-change and spy-cost diagnostics — 2026-10-16 (local)

**Authorization.** The user said the first collector session's save predates checkpoint A, and that the same save had loaded and trained normally in earlier runs. They then authorized the proposed next step: a diagnostic-only runtime batch deployed through the existing gates, followed by a re-run with the collector. No gameplay repair is authorized.

**Runtime change (B206.233 / modinfo233, diagnostic-only).**
- `Mod/ExpeditionTraining.lua` subscribes to `GameEvents.OnCityPopulationChanged(player, city, delta)` (synchronous; HD's hospital handler uses the same event) and `Events.CityPopulationChanged(player, city, newPopulation)`.
  - Only the test player's reserved source city during `TRAINING` is observed.
  - Each source (`GAME`/`EVENT`) aggregates per turn: event count, last delta/new value, sum, min and max.
  - `POP_CHANGE` is emitted on the 1st, 2nd, 4th, 8th… notification, so 2431 increments cost 12 records per source. Unreported totals are emitted as `POP_SUMMARY` before `BIRTH_ENTRY`, before `COMPLETE_CALLBACK` and at turn boundaries.
  - `PlayerTurnDeactivated` emits `TURN_END` and `PlayerTurnActivated` emits `TURN_BEGIN`, each with the source city's population, while `TRAINING`.
- `Mod/ExpeditionTrainingDiagnostics.lua`: every sampled record also carries `spyNativeCost`, which is `GetUnitCost(UNIT_SPY)` in the same city's queue (comparison only). New whitelisted keys are `spyNativeCost`, `popSource`, `popEvents`, `popDelta`, `popTo`, `popSum`, `popMin`, `popMax` and `popTurn`.
- Ring schema, keep (64), per-context budget (96), dedup, scalar redaction and the print line format are unchanged. Capacity, source, Store, unit formula, admission and GC are unchanged. Every observer path is wrapped in `pcall`, and a failure cannot change progression.

**Tools (not in the runtime package).**
- `tools/read_expedition_trace.py` `record` mode passes a fixed allowlist of HD print shapes as `[SPC][B206][HD] …`. The two shapes are `<name> 人口变化 <int>` and `中心医院 …`.
  - At most 200 are passed per passive window; the rest are counted.
  - `WINDOW_COMPLETE` now reports `hd_records`/`hd_dropped`. All other engine output is still dropped.
- `tools/collect_expedition_trace.py` logs HD lines without dedup (the first 2000 per session) and counts them by kind and amount in the summary.

**Local validation (L2).**
- +7 tests:
  - population aggregation/order with ON/OFF equivalence;
  - other-city/non-training rejection;
  - turn-boundary flush order with equivalence;
  - spy native cost;
  - observer exception equivalence;
  - reader HD allowlist/cap;
  - collector HD count.
- Two reader `WINDOW_COMPLETE` assertions were updated to the extended format, and the package version assertion moved to 233.
- Affected suites: 134 + 5 PASS on Python 3.14/Lupa.
- Full discovery: 2209 tests, of which 488 failures/errors. This is the identical failure set to HEAD `c37de97` in a temporary detached worktree (2202 tests, same 488; legacy/external-DB modules), so there are no new failures.

**Limits.** This is local simulation, not user-game PASS. Whether HD prints reach the Tuner socket from HD's script context is unverified natively. Root cause remains UNKNOWN.

**Deployment.** B206.233/modinfo233 is **DEVELOP_ACTIVE**, source `179228aff1e51ea66da2759c68115bb97763b6b4`, receipt `B206.233-179228a-playtest.json`. A fresh OS check confirmed game exit before both guarded switches (B205 restored to stable via its receipt → B206 activated). 219/219 source/runtime files MATCH. Outgoing B205 and stable recovery packages are retained, and there is no pending transaction. No game launch or native result is claimed.

## B206 collector session — 2026-10-16 (USER_GAME_TEST, diagnostic)

**What the user ran.** B206.233, cold start, first load of the same pre-checkpoint-A save, train once, end turn. The collector ended on `GAME_EXITED`. Session `local/diagnostics/B205/session-20261016T105922Z-ad1e9b/` holds 31 unique records. The user notes that this save loaded and trained normally in earlier runs, but the jump now reproduces on every first load.

**Native observations.**
- T88: eligible row, order, reserve, marker and native build all show population16. Expedition native cost is 1 against definition60. **Ordinary `UNIT_SPY` native cost in the same city is 60** (`spyNativeCost=60`), so cost1 is specific to the Expedition unit, not to the city or production path.
- `TURN_END` (T88, seq15): population16.
- `GameEvents.OnCityPopulationChanged`, which is synchronous:
  - **one notification with delta +2430** (16→2446, seq16);
  - then one with delta +1 (→2447, seq17).
  - There were no other notifications. The jump is a single native population change, not 2431 increments.
- The deferred `Events` queue was published in this order:
  - `UnitAddedToMap` (BIRTH, seq18–19);
  - `CityPopulationChanged` to 2446 (seq20);
  - `CityProductionCompleted` (seq21–23);
  - `CityPopulationChanged` to 2447 (seq24);
  - then `TURN_BEGIN` at 2447.
  - If that queue preserves engine order, the +2430 change occurs right after the Expedition unit is created, and the +1 occurs after production completion.
- `City_BuildQueue.csv` T89 again records production added 342.3, needed 1, overflow 107.3. The final value 2447 is identical to the earlier session.
- No allowlisted HD print arrived (`hd_prints: 0`). It is unverified whether HD script-context prints reach the Tuner socket at all, so this does not prove that HD code was inactive.
- A source search found no `ChangePopulation`/`SetPopulation` in this Mod. In the installed HD and other Workshop scripts, only ±1 calls exist. None can produce +2430.

**What this establishes.**
- The fault is one native +2430 population change during the player's T89 processing, adjacent to creation of the cost-1 Expedition unit.
- It is deterministic for this save on B205/B206: the same final value 2447 appeared in two sessions.
- Cost1 is unit-specific.

**What it does not establish.** Which native rule applies +2430, whether it is caused by the unit's definition (cost/overflow, or some other copied or omitted column), and why earlier runs on this save did not show it. Root cause remains UNKNOWN. No repair is authorized.

## B206 spy comparison and multi-load sessions — 2026-10-16 (USER_GAME_TEST, diagnostic)

**What the user ran.** The same save on B206.233, in several loads within one or more game processes:
- Expedition training from T88;
- ordinary `UNIT_SPY` training in the same city, two or three times;
- Expedition training that completed in the same turn as a spy, through overflow production.

The user reports that ordinary spies never changed population, and that the jump followed Expedition completion. The collector had to be restarted after in-game reloads (see the collector defect below). The game process kept the ring across collector restarts, so the sessions `20261016T110553Z-c21e72`, `…111108Z-2daccd` and `…111234Z-71931b` overlap and show load sequences 1–4.

**Native observations.**
- **Load 1** (normal): training from T88. At T89 `GameEvents.OnCityPopulationChanged` delivered **one notification with delta 0** at the point where the jump otherwise occurs. Birth, completion and finish all stayed at population 16.
- **Load 2** (same process): the same flow gave delta **+2430** and then +1, ending at 2447.
- **Load 4** (same process): the Expedition was ordered at T89 after a spy completed, and it completed in the same turn through overflow. Delta **+2430** occurred just before `BIRTH_ENTRY`, without any turn boundary.
- The Expedition's native cost was 1 in every load. The definition in the read-only `DebugGameplay.sqlite` is identical to `UNIT_SPY` on every cost field: Cost 60, `COST_PROGRESSION_PREVIOUS_COPIES`, Param1 15, PopulationCost NULL. It differs only in name, sight, moves, purchase yield, maintenance, team visibility, advisor, experience, tags, the building prereq and missing `UnitAiInfos`/`Units_XP2` rows. Missing `Units_XP2` rows are common (117 of 245 units), including many normal ones.
- The database has no population-on-creation modifier that applies to this player. The only one is the Janissary −1, which belongs to Suleiman.

**What this establishes.**
- Creating an Expedition unit makes the engine apply one population change to the source city. That change was 0 in one load and +2430 in other loads of the same save, including a cold-start first load in an earlier session.
- The value is **not tied to first load or reload**. It varies between loads, which is consistent with the user's suspicion of a probabilistic or undefined value.
- Ordinary spies did not show it. Native cost1 is Expedition-specific even though the definition rows match.

**What it does not establish.**
- Which native rule produces the change, or why the Expedition's native cost differs from the matching definition. One unverified observation: 2430 = 162 × 15, where 15 is the cost-progression step.
- Root cause remains UNKNOWN. No repair is authorized.

**Collector defect (tools only, not yet fixed).** During an in-game reload, the Tuner connection is unavailable for more than the 30 s idle exit, so the collector ended with `GAME_EXITED` while the game was still running. The waiting error codes are not logged, so whether a loading game refuses connections or only times out on the context is not yet recorded.

## B207 fixed-cost experiment and collector reload fix — 2026-10-16 (local)

**Authorization.** The user authorized both proposed items: the collector reload fix, and a temporary discriminating runtime experiment. The experiment is not a design decision. Whether Expedition cost keeps previous-copy progression remains the user's decision.

**Runtime change (B207.234 / modinfo234, TEMPORARY diagnostic experiment).** `Mod/Data/ExpeditionSpyGate.sql` keeps the Spy base cost (60) for `UNIT_SPC_EXPEDITION_SPY`. It sets `CostProgressionModel='NO_COST_PROGRESSION'` and `CostProgressionParam1=0` instead of copying the Spy's previous-copy progression. All B206 diagnostics, gameplay flow, capacity, source, Store and GC are unchanged.

What each outcome would mean:
- Native cost 60 and no population delta on creation across several loads: this implicates the previous-copy progression on this type.
- Cost1 or the jump persists: the progression is excluded.

**Tools.** `tools/collect_expedition_trace.py` now counts only a refused connection (`SOCKET_UNAVAILABLE`) toward the idle exit. A socket that accepts but closes, or times out in connect/context during an in-game load, keeps the session alive. Each change of waiting code is logged as a `waiting` event.

**Local validation (L2, W0004 v1 minimum sufficient).**
- The targeted training/diagnostics/UI/gate/reader/collector suites pass (171 tests), with the gate SQL test run against the explicit read-only external `DebugGameplay.sqlite`.
- One new collector test covers a 100 s in-game load, reconnect and real exit.
- The gate SQL assertion now states the experiment's fixed-cost values, and the package version assertion is 234.
- No full regression: no concrete cross-module risk was identified.

**Deployment.** B207.234/modinfo234 is **DEVELOP_ACTIVE**, source `1f90648d41f359b8120c3b2b23add24dfc0b542c`, receipt `B207.234-1f90648-playtest.json`. A fresh OS check confirmed game exit before both guarded switches: B206 restored to stable through its receipt, then B207 activated. 219/219 files MATCH, and there is no pending transaction. A shell word-splitting error in the first invocation stopped the run after the verified stable restore and before activation. Activation then ran with explicit reviewed hashes.

## B207 user runs — 2026-10-16 (USER_GAME_TEST, diagnostic)

**What the user ran.** B207.234 with the same save, in three game sessions:
- **Run 1:** ended turn and the game's memory ran away to about 80 GB. The trace stops at `TURN_END` T88 with population 16 (session `…112517Z-932203`).
- **Run 2:** the user repeatedly cleared the Expedition through the P0 panel and retrained it, 4–5 trainings in all. Population never changed. Every Expedition creation produced one `GameEvents.OnCityPopulationChanged` notification with **delta 0** (session `…112930Z-24d9ff`).
- **Run 3:** the first training already jumped, and so did every later one, 4 trainings in all. Each Expedition creation applied exactly **+2430**: 16→2446, 2447→4877, 4877→7307 and 7306→9736. Unrelated ±1 changes occurred in between (session `…113253Z-38c444`).

**Native observations.**
- Every record shows `costModel=NO_COST_PROGRESSION costStep=0`, so the experiment loaded.
- The population delta per Expedition creation is constant within a load: 0 in normal loads, and exactly +2430 in affected loads, in every session observed so far. Whether a load is affected appears to be decided per load.
- `City_BuildQueue.csv`, read-only:
  - The first Expedition completion after a load needs **1** (T89: added 342.3, overflow 107.3).
  - Later ones in the same load need **60** (T89–T91), in both normal and affected loads.
  - The trace's diagnostic `nativeCost` read stays 1 throughout, so that read does not match what the engine log records as needed.
- In run 3, T90 production rose to 14879.1 and 10770.4, which is a consequence of the inflated population.
- During in-game loads the Tuner socket **refuses connections** (`SOCKET_UNAVAILABLE`) for about 2–3 min. The B207 collector change therefore does not cover reloads: it still ends with `GAME_EXITED`.

**What this establishes.**
- Previous-copy cost progression is **excluded** as the cause of the population delta. The jump persists with a fixed cost.
- The delta is a per-load fixed value applied at each Expedition creation: 0 or +2430. It is not a probability per training.
- Cost1 affects only the first training after a load.
- The memory runaway recurred on the same path.

**What it does not establish.** The native mechanism. The Expedition's remaining structural differences from ordinary spies include:
- `Unit_BuildingPrereqs` with `NumSupported=1`, whose only other user is the Archaeologist;
- an InternalOnly marker building that Lua creates and later removes;
- the missing `UnitAiInfos` row.

Root cause remains UNKNOWN. No repair is authorized.

## B208 marker-support experiment — 2026-10-16 (local)

**Authorization.** The user authorized option A after the Design/Architecture re-read and rule check. This is a temporary diagnostic experiment, not a design decision.

**Hypothesis.** The engine links a unit to its supporting prerequisite building. The Expedition is the only unit besides the Archaeologist with `NumSupported=1`, and its transient marker building is removed while the trained unit lives. That removal may leave a stale native reference, which would be consistent with a per-load fixed population delta (0/+2430) at creation and with the memory runaway.

**Runtime change (B208.235 / modinfo235).** In `Mod/Data/ExpeditionSpyGate.sql`, the Expedition's `Unit_BuildingPrereqs.NumSupported` is set to −1 (unlimited, as for every other building-prereq unit except the Archaeologist), instead of 1. The B207 fixed cost is reverted: Cost, model and step are again copied from `UNIT_SPY`, as Design requires. Against B206 the SQL diff is only the `NumSupported` value plus its comment.

The marker, its city gating and its lifecycle are unchanged, as are the Store cap1 reservation and queue checks, the source provenance and all B206 diagnostics.

**Rule check.**
- Kept: cost formula with independent counting, national cap1 and source binding.
- Changed during the experiment: the native per-building guard against a second queued Expedition in the reserved city. A second queue entry would now be detected by `TRAINING_MULTIPLE_QUEUE_ENTRIES` and HELD instead of being natively blocked, and no extra team can be created.
- Open separately: the first-training-after-load cost1 (Design: cost must equal the Spy cost).

**Local validation (L2).** The targeted gate SQL (read-only external DB), training, training UI, diagnostics, trace integration, reader and collector suites pass (171 tests). The gate assertions state the restored Spy cost fields, `NumSupported=-1` and version 235. No full regression.

**Deployment.** B208.235/modinfo235 is **DEVELOP_ACTIVE**, source `3a84a6e4296e727140f59fc709a218f9ce73814f`, receipt `B208.235-3a84a6e-playtest.json`. A fresh OS check confirmed game exit before both guarded switches: B207 restored to stable through its receipt, then B208 activated. 219/219 files MATCH, and there is no pending transaction.

## B208 user runs — 2026-10-16 (USER_GAME_TEST, diagnostic)

**What the user ran.** B208.235, three loads in one game process (session `local/diagnostics/B205/session-20261016T140812Z-a612db`, stopped with Ctrl-C):
- **Load 1:** "Continue game" loaded a T89 autosave with population 4877 and an Expedition TRAINING. The user ended the turn.
- **Load 2:** the base T88 save, two trainings.
- **Load 3:** the base T88 save, one training. The memory ran away at end turn.

**Native observations.**
- **Load 1:** at T90 the Expedition creation applied **+193189** (4877→198066), then +1. Birth, completion and finish followed normally.
- **Load 2:**
  - T88 training: **+2430** at T89 (16→2446), then +1.
  - A second order at T89 read native cost **75**, which is 60+15×1 previous copy. That is the restored Spy formula working after the first copy.
  - That order completed immediately through carried overflow, applying **+2430** (2447→4877). Because birth and completion arrived before our queue confirmation, training went **HELD**. This is a separate state-machine defect.
- **Load 3:** T88 training. The trace stops after `TURN_END`, and the user observed the ~80 GB memory runaway.
- The first training after each load read native cost **1**.

**What this establishes.**
- Per-building support (`NumSupported`) is **excluded**. The delta and the memory runaway persist with −1.
- The delta X is fixed within a load but **differs between saves**: +193189 for a derived autosave, against 0/+2430 for the base save. It is not a constant of the unit definition.
- The first-after-load cost1 followed by 75 indicates that the engine's previous-copies state for this unit type is invalid immediately after a load and becomes valid after one creation.
- New defect: an order that completes immediately through carried overflow can arrive before the queue confirmation and HOLD.

Root cause remains UNKNOWN. A read-only multi-angle investigation is in progress, covering save lineage, unit-type table history, logs, definitions and public engine knowledge.

## B208 city A/B comparison — 2026-10-16 (USER_GAME_TEST, diagnostic)

**What the user ran.** On B208.235 with the same base T88 save, the user trained Expeditions repeatedly in a second Culture ACTIVE IV city:
- **City B:** id 262147, `LOC_CITY_NAME_DUROCORTERON`, population 13.
- **City A:** id 393220, `LOC_SPC_CITY_EDINBURGH`, the city used in all earlier tests.

The sessions are `…142028Z-c8e51a` and `…142347Z-018767`.

**Native observations.**
- **City B:** in 6+ trainings across three loads, every Expedition creation produced `GameEvents.OnCityPopulationChanged` with **delta 0**. Population stayed 13.
- **City A**, in the third load of the same process: **+2430** (16→2446).
- **Both cities:** the first training after each load read native cost **1**, and later trainings **75**. Cost1 is therefore a per-player/per-type issue, independent of the city.
- **Both cities:** a second training ordered in the same turn completed at once and went **HELD**, the same overflow-immediate defect recorded under B208 user runs.

**What this establishes.**
- The population delta is **specific to city A**. It is not a general property of the Expedition unit, of loading, or of this save as a whole.
- Ordinary spies in city A remain unaffected, so the cause needs both the Expedition creation path and something particular to city A.
- B's name suggests a captured city and A's a founded one (INFERENCE). A was also the source city for every earlier Expedition prototype and training.

Root cause remains UNKNOWN. A focused read-only city A/B investigation is in progress.

## Read-only investigations — 2026-10-16 (STATIC / INFERENCE)

Two user-requested read-only multi-agent investigations were run, each with independent skeptic review. Their raw outputs are kept in the session scratchpad and are not committed. Saves were decoded in memory or in scratch; nothing was written to the game, saves or configuration.

**Facts (save decoding, git, logs).**
- **Campaign age.** The campaign began on 2026-09-30 with 242 unit types. GATE, ZERO and SPY were appended on 2026-10-10 at indices 242–244 and never reordered. Save headers do not store the mod version. Type hashes are CRC32 without the final XOR.
- **Per-city arrays.** Every player-0 city, A and B included, holds a count-prefixed per-unit-type int32 array of length 242, fixed when the city was founded. Index 244, the Expedition, is outside it; UNIT_SPY (18) is inside. Cities founded later hold 243/245. Hash-keyed type tables are rewritten at the current size (245 units, 2802 buildings).
- **Stale cost cache.** Player 0's saved per-unit cost cache still holds Expedition = **1** (the pre-B202 definition) in the base save and AutoSave_0089. Later autosaves hold 60 and then 75. This explains the first-after-load cost1, and it is independent of the population fault.
- **The 2430 value.** It equals plot index 2430 = (62,32), city A's Theater Square: map width 74, and the same plot as A's half-built `JNR_MEDIA_CENTER` and A's `BUILDING_MUSEUM_ARTIFACT`. The museum is the Archaeologist's `NumSupported=1` prerequisite, and B has no museum. 193189 is not stored in either city.
- **A/B differences.**

  | | City A | City B |
  |---|---|---|
  | Origin | founded `BY_SETTLER` | captured `BY_COMBAT` from Gaul |
  | Governor | Victor | Magnus (HD base promotion disables settler population consumption) |
  | Museum (Archaeologist) | present | absent |

- **Our stored data.** The only city property our mod writes on these cities is `SPC_DEV_BINDING_B013_TOKEN`, which no native/HD code reads. Store/Expedition records are Game-level Lua tables. No Lua anywhere, in history or now, changes population by more than ±1. This does **not** support a cause in our stored data.
- **HELD defect O11.** The installed Overflow Bug Fix mod (2589004769) calls `AddProgress(0)` on every production change. A second order with carried overflow therefore completes immediately, and our training state machine HOLDs.
- **Correction.** B207 "run 2" and "run 3" were loads 1 and 2 of one process, not separate processes.

**Leading inference.** Completing an Expedition (type index 244, which has a building prerequisite) makes the engine read a per-city or per-type slot that does not hold a valid population amount. In city A, that read lands on data carrying A's Theater plot index. Whether the bad read occurs is decided per load, and a write variant would explain the memory runaway.

The investigations disagree on the exact structure:
- an undersized 242-entry per-city array accessed at index 244 (≈0.6);
- a building-prereq/support read reaching A's theater-plot objects (≈0.45).

Both point to the native completion path for this appended unit type in an older campaign. Refuted:
- the marker building index;
- Expedition definition fields as a per-type constant;
- cost1 as the same mechanism;
- stale Lua or heap residue from earlier prototypes;
- a founded-city-only rule.

**Cheapest discriminating tests (no runtime change).** Each test first confirms a 2430 load in A, and the user must not end the turn in a bad load (memory risk).
1. Train a vanilla Archaeologist in A, which has a museum prerequisite at an in-range index.
2. Train an Expedition in a city founded after 2026-10-10 (245-entry array), or in a fresh campaign.
3. Swap or unassign the governors (Victor/Magnus) to clear that confound.

Fix directions remain options only (`DESIGN_DECISION_REQUIRED` where noted in Status). Root cause remains UNKNOWN (INFERENCE only).

## New-campaign check — 2026-10-16 (USER_GAME_TEST, diagnostic)

**What the user ran.** B208.235 in a **new campaign** started with the current mod. In city Stirling (65536), at turn 3, the user trained several Expeditions across four loads in one process (sessions `…163612Z-ba8c11` and `…164427Z-b45c29`). The user will use this campaign as the base for future tests.

**Native observations.**
- **No population notification at all** occurred at any Expedition creation. In the old campaign, every creation fired one, with delta 0 or X.
- Population stayed at 1.
- Native cost and engine "Production Needed" both followed the Design formula exactly: 60, 75, 90, 105, 120. After a reload the cost reflects the saved copy count, and **cost1 never appeared**.
- No HELD occurred and no memory problem appeared.

**User clarification.** In the old campaign, cities A and B were both founded or conquered, and invested to Culture ACTIVE IV, before any Expedition-related module existed. Founding era and specialization history do not distinguish A from B, which is consistent with both holding 242-entry per-unit arrays.

**What this establishes.**
- The population fault, the population-notification path and the stale cost1 are all **tied to the pre-Expedition campaign**. They did not reproduce in a campaign created with the current unit set.
- This supports the inferred old-save mechanism.
- Scope limit: this check covers one city, early turns and in-process reloads. It does not yet cover multiple cities, Culture ACTIVE IV cities with theater/museum content, or end-turn completion.

Root cause in the old campaign remains INFERENCE. No repair authorized.

## User decisions — 2026-10-16

- **Save scope:** only saves of games started with the current mod build loaded are supported, with no compatibility for updated or older saves ([Playtest Workflow](../../../Architecture/Playtest_Workflow.md#save-scope-and-test-base-user-decision-2026-10-16)). The new campaign is the test base.
- **No population protection** is added. The old-campaign population delta, memory runaway and stale cost1 are closed as out-of-scope old-save faults, not repaired. Recurrence in an in-scope game reopens the investigation.
- **Revert the B208 experiment:** the marker prerequisite returns to `NumSupported=1`, restoring the native per-city guard.
- **Fix the overflow-immediate-completion HELD** if practical. Cap1 makes it rare, but the user asked for it; the plan goes to user review first.

## B209 marker revert and immediate-completion receipt — 2026-10-16 (local)

**Authorization.** On 2026-10-16 the user approved the reviewed plan, including the new evidence rule that a same-turn native completion in the reserved city substitutes for the UI queue confirmation.

**Runtime change (B209.236 / modinfo236).**
- **Marker prerequisite.** `Mod/Data/ExpeditionSpyGate.sql` returns to `NumSupported=1`, which restores the native per-city guard. The file is now identical to B206/Design.
- **Training receipts.** In `Mod/ExpeditionTraining.lua`, a birth or completion in the **reservation turn** (`trainingTurn`) no longer requires a prior queue confirmation. A native completion in the reserved source city that is not cancelled records `trainingQueued` and then `trainingCompleted`. A birth before the completion is recorded and waits for it.
  - Outside the reservation turn, the old requirement stays: an unconfirmed birth or completion still HOLDs.
  - Other-city or cancelled completions still HOLD.
  - Finish still requires queued + completed + exactly one born unit at the source endpoint.
  - A half receipt still HOLDs at the next turn or on recovery.
- **Activity publication.** In `Mod/ExpeditionSpyGate.lua`, the published activity adds a scalar `trainingReceipt`, true while TRAINING once a birth or completion is recorded.
- **Production UI.** In `Mod/UI/ExpeditionTrainingUI.lua`, a pending QUEUE handshake whose reservation already has a receipt, or has left TRAINING, closes without retrying the queue read and without sending CONFIRM. A HELD outcome surfaces the Gameplay error.
- **Unchanged.** Cost formula, cap1, source reference checks, marker lifecycle and B206 diagnostics.

**Local validation (L2).**
- The 8 new or replaced tests cover:
  - same-turn immediate completion in both callback orders;
  - birth without completion holding at the next turn;
  - other-city, cancelled and second-birth holds;
  - cross-turn unconfirmed birth/completion holds;
  - the UI handshake closing silently;
  - the UI surfacing HELD.
- The former `test_unconfirmed_queue_birth_hold` assertion was replaced by its cross-turn form, following the approved contract change.
- Targeted gate SQL (read-only external DB), training, training UI and trace integration: 111 PASS.
- Affected-subsystem regression over all `test_expedition_*` suites (719 tests): 14 failures/errors, **identical to HEAD `130cc0d` without B209** (711 tests, same 14, all in the historical `test_expedition_spy_activity_diagnostic` and `test_expedition_spy_activity_failure` suites). No new failure.

**Deployment.** B209.236/modinfo236 is **DEVELOP_ACTIVE**, source `3060008723d527b6b50501275244f2011aaf27a2`, receipt `B209.236-3060008-playtest.json`. A fresh OS check confirmed game exit before both guarded switches: B208 restored to stable through its receipt, then B209 activated. 219/219 files MATCH, and there is no pending transaction.

The first exit check reported a false "game running": its pattern also matched the Claude process, whose arguments contain the Civ VI directory path. The check now matches only the game executable (`Civ6.app/Contents`), and no package was touched while it reported running.

## B209 user test failure — 2026-10-16 (USER_GAME_TEST_FAIL)

**What the user ran.** B209.236 in the new campaign, city Stirling at turn 3 (session `…20261017T011932Z-b80b90`, screenshot archived under the Evidence path). The user ordered the 人文考察团 (Expedition), then switched production to an Industrial Zone, through map placement, to build up carried overflow, and purchased a building.

**What happened.**
- Reserve, marker and queue evidence were normal (seq7–14).
- The district selection **replaced** the queued Expedition, and the queue read 0 (seq19).
- Under the B202 rule ("empty queue is not cancellation"), Gameplay kept the reservation and removed the marker. The Expedition therefore disappeared from the production list, and the reservation could only be ended through P0.
- The B202 replacement hook (`GetBuildInsertMode` → `CancelQueue`) lives only in the production panel; district map placement issues its operation from another context and bypasses it.
- The P0 `TRAINING_NATIVE_QUEUE_UNCONFIRMED` came from the UI handshake re-reading the replaced queue. It was spurious, because Gameplay already held the queue evidence.
- Population +1 ×3 was ordinary.

## B210 native-removal release — 2026-10-16 (local)

**Authorization.** The user approved the reviewed plan, including the contract change: an empty queue with no birth/completion receipt and no Expedition-family unit on the map counts as native removal or replacement.

**Runtime change (B210.237 / modinfo237).**
- **Training.** In `Mod/ExpeditionTraining.lua` Pulse, when TRAINING with queue evidence, an empty source queue, no receipt, and `T.NoUnits(pid)`, the marker is removed and `T.Cancel` releases the reservation to ENDED. Recovery uses the same rule. With any Expedition-family unit present, the old behaviour stays: keep the reservation live, HOLD `TRAINING_LOADED_QUEUE_MISSING` on recovery. A completed order already has its unit, so late completion events cannot be mistaken for removal.
- **Gate.** In `Mod/ExpeditionSpyGate.lua`, `T.NoUnits(pid)` is a live read of Expedition-family units, and the published activity adds a scalar `trainingQueued`.
- **Production UI.** In `Mod/UI/ExpeditionTrainingUI.lua`, a pending QUEUE handshake closes silently when Gameplay already has the queue evidence or a receipt, or the reservation ended or changed. A HELD error is still surfaced for the same reservation.
- **Unchanged.** Cost formula, cap1, source binding, the B209 same-turn receipt rule, the marker lifecycle otherwise, and B206 diagnostics.

**Local validation (L2).**
- 6 new or updated tests cover:
  - replacement releases, and reordering works afterwards;
  - no release with a receipt;
  - no release with another Expedition-family unit present;
  - an unconfirmed empty queue is not release evidence;
  - a late-event empty queue with the unit present waits;
  - on load, a missing queue with a unit HOLDs and without one releases;
  - the UI stays quiet after a native replacement.
- The two tests that encoded the superseded rule were replaced by their approved forms.
- Targeted gate SQL, training, training UI and trace integration: 117 PASS.
- All `test_expedition_*` suites (725 tests): the failure set is identical to HEAD (the same 14 historical activity-diagnostic failures).

**Deployment.** B210.237/modinfo237 is **DEVELOP_ACTIVE**, source `00d37ccb98f87169c9080133865885cd7f886154`, receipt `B210.237-00d37cc-playtest.json`. A fresh OS check (game executable only) confirmed game exit before both guarded switches: B209 restored to stable, then B210 activated. 219/219 files MATCH, and there is no pending transaction.
