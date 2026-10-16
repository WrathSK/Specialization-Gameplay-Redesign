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
