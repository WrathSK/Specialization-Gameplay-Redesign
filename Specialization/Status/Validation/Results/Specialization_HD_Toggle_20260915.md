# HD Core toggle：独立进程0城市对照

Document Owner: Codex
Build: B072.99 / modinfo99 (unchanged)
Evidence: user-provided14 screenshots, individually reviewed; memory association observed, root cause UNKNOWN.

## Configuration / evidence boundary

User labels first4 pairs HD enabled and last3 disabled, following fixed BASE+TITLE+AREA+Cheat protocol. Intended third-party sets: OFF=SPC+BTS+EMM+TITLE+AREA+Cheat; ON=OFF+HD Civ6 Plus. No new enabled-list log in this delivery; membership based on user protocol/context, not independently re-extracted UUID list. Cheat visible both sides. HD settings screenshot confirms GS, Robert the Bruce(Test), Prince, Standard speed, Continents/Small, disaster2, Monopolies ON. OFF setting page absent; maintain prior fixed-mode contract but do not claim screenshot independently confirms it. Maps differ; seeds/AI roster not independently established.

First extra pair05:18:25 is CREATE GAME settings, Memory4.74GB,PID66765,threads32,ports875. Exclude it from idle baseline: subsequent jump includes world loading, not leakage measurement.

## Timeline

Activity Monitor Memory/GB as displayed, not RSS. All in-game samplesTurn1/0city, unit callbacks0. Distinct PIDs eliminate prior same-process comparison limitation.

|State|Time|Elapsed sec|Memory GB|PID|Threads|Ports|audit_standard|send_inflight|
|---|---|---:|---:|---:|---:|---:|---:|---:|
|HD ON start|05:19:09|0|9.12|66765|33|1461|617|371|
|HD ON middle|05:21:42|153|9.30|66765|33|1463|9474|9505|
|HD ON end|05:24:16|307|9.51|66765|33|1463|18405|18715|
|HD OFF start|05:30:08|0|8.89|67538|32|1392|500|197|
|HD OFF middle|05:32:48|160|8.86|67538|33|1392|9832|9811|
|HD OFF end|05:35:23|315|8.88|67538|33|1400|18795|19046|

ON first153sec+0.18GB, next154sec+0.21GB; total307sec+0.39GB≈0.0762GB/min. OFF first160sec−0.03GB, next155sec+0.02GB;315sec net−0.01GB, observed8.86–8.89GB. Three points support growth at each ON sample and near-flat OFF window; not proof continuously monotonic every second or indefinite stability. No crash in photographed windows; no new crash report delivered.

Both runs all3 samples: facts/city_scan/district_scan/building_check/building_create/building_remove/property_write=0; full derive0, derive_requested3; routes0,revision0,inflight1,peak1,network send1/receive0; route_scan3,revalidate2,same_snapshot2. Lv3/Boost/Commerce/Copy audit8/3/1/7 unchanged. busy_skip ON544 and OFF650 constant. Runtime audit FILE_API_UNAVAILABLE on both sides.

ON audit delta17788/307=57.94/s; OFF18295/315=58.08/s. Network wait suppressions18344 vs18849; single flight, not queue lengths. Network counters do not cover every module's requests.

## Interpretation

This is stronger evidence of HD-Core-enabled association than previous mixed-turn/city/process runs. At0city the measured C² city workload is absent, and approximately same Audit entry frequency exists both ON/OFF; neither city scans nor Audit frequency alone explains memory contrast. Does NOT exclude different work inside callbacks, uncounted UI/native allocations, initialization interactions or HD-independent background effects. Do not assume Discount root cause, exonerate all Specialization paths, or attribute solely HD bug.

Within this controlled protocol OFF six-Mod set is a known non-reproducing observation window; ON seven-Mod set is a reproducing observation window. Prior six-Mod positive set withoutCheat remains a smaller known growth-observed set, but different protocol; retain both, do not claim irreducible/global minimum. The original112 set remains historical. No addon testing needed now.

Next minimal step: re-enable only CORE, retain the six fixed companions/settings; fresh process, newTurn1/0city, same307-ish/300sec with0/150/300second screenshots. This completes ON→OFF→ON withdrawal/rechallenge. If growth returns, move to read-only CORE/interaction-boundary investigation; no formal optimization or instrumentation implicitly authorized. No need repeat OFF or add other HD modules now.

## Archive / workflow

W/Specialization/Status/Validation/Evidence/HD-Toggle-20260915-0518/:14PNG92182239bytes, original subfolder/names, SHA256 before/after match, manifest.json. W is external application-support workspace. Raw evidence not in Git. Only develop docs changed; source/runtime/main/Design/config untouched. No game started/attached, no tests claiming engine PASS.
