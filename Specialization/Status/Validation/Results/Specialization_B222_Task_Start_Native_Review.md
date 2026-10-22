# B222 — Three completed missions and Ottawa admission failure

**USER_GAME_TEST_PASS for the three captured PEOPLE/PLACES completions; USER_GAME_TEST_FAIL for the later Ottawa task start.** These are scoped outcomes, not full Expedition acceptance. Baseline: B222.249 / modinfo249, source `ac321eb`, last verified deployment receipt `B222.249-ac321eb-playtest.json`. This review changes records only. [Implementation and local evidence](Specialization_B222_Task_Start_Rejection.md) remain unchanged.

## Submitted evidence

Ignored collector session `session-20261017T184054Z-1760e9` contains 32 consecutive trace records and 48 captured Gate prints. The collector ended with `INTERRUPTED`; that does not establish a game crash. `alerts: none` covers the collector's existing training/population alerts, not mission acceptance. UTC times below are capture times; snapshot times can follow the actual event.

| Record / capture time | Observed outcome | Evidence boundary |
|---|---|---|
| records.log28–39; 18:41:03–18:41:36; start T53 | Khmer PLACES: centre20,13 / wonder evidence18,13; AWAKE, ready, SLEEP allowed; TASK_RUNNING → SUCCESS, Insight NEW → ARRIVED, idle controls available | 奇观巡礼 completed without task-site movement |
| records.log45–56; 18:42:23–18:43:07; start T57 | Gaul PEOPLE: centre71,28; SLEEP allowed; TASK_RUNNING → SUCCESS, Insight NEW → ARRIVED | 风土考察 completed after native redispatch/arrival |
| records.log57–63; 18:43:16–18:43:56; start T59 | Same Gaul unit/centre: SLEEP allowed; TASK_RUNNING → PLACES SUCCESS, Insight NEW → ARRIVED, idle controls available | Another successful task in the same city; initial direct TASK print fell outside capture, but the activity snapshot and completion identify the successful path |
| records.log65–71; 18:44:09 | Archive city owner0/city65536: historical5/effective5; Gaul PEOPLE+PLACES, Hungary PEOPLE, Khmer PEOPLE+PLACES; Tourism projection10% | Reported ledger/projection agrees with five effective records. This is not new evidence of native fractional Tourism settlement |
| records.log64,72–78; 18:43:57–18:48:25 | Gaul idle signature changes from available Skip/Sleep to available Wake; later dispatch accepted, replacement unit1966086 reaches ARRIVED at56,34, all six native idle-action eligibility bits false | Unit IDs change through native travel; task traces retain teamKey E0-1B0006-8. No binding-loss error is captured |
| records.log79–80; snapshot18:48:34; start T64 | Ottawa: exact expected/actual56,34; AWAKE, ready=true; startup eligibility DENIED; actual guard DENIED; requested=false / attempted=false; reason query also DENIED | Failure before ARMED/native SLEEP/task clock, not at reward calculation or task-site placement |

The final city name is supplied by the user; the bounded trace records coordinates, not the name. Its mission category is **not captured** and is not guessed. Reaching this exact TASK_PREPARING activity lease requires the current Gate's target/unique-quota/source/centre admission checks; no corresponding target-invalid or source-binding failure appears.

## User clarification and leading hypothesis

From memory, without a retest, the user reports manually sleeping for several turns in Gaul before redispatch; Ottawa failed in the arrival turn, during the user's own turn. The user identifies manual sleep as the noticed difference, not as a controlled isolation of every variable.

This is consistent with the idle signature. In [the UnitPanel adapter](../../../../Mod/UI/ExpeditionSpyUnitPanel.lua), each pair is visible/eligible for Skip, Sleep, then Wake. Gaul changes from `true:true:true:true:false:false` to `false:false:false:false:true:true` before departure. Ottawa shows `false:false:false:false:false:false` before task admission. Native eligibility is read under protected calls; these bits are not a saved activity enum. The task-start reader itself directly confirms AWAKE at Ottawa.

**Leading, provisional hypothesis:** manual SLEEP → native redispatch → replacement-unit arrival leaves some native admission condition different from the prior successful arrivals. This is more specific than “PLACES is broken” but is not a proven engine defect. The observed post-arrival activity is AWAKE, so do not say the arrived unit literally remained asleep. No remaining-moves, native arrival bookkeeping or full turn-processing sample was recorded. The user's own-turn recollection excludes a simple “the user intentionally started it during an AI turn” account, but not every internal processing condition.

Read-only comparison:

- [SubmitTravel](../../../../Mod/ExpeditionSpyRead.lua) checks and requests native SPY_TRAVEL_NEW_CITY; it does not explicitly wake a manually sleeping unit first. [Gate arrival](../../../../Mod/ExpeditionSpyGate.lua) rebinds the exact native-name candidate and preserves source history; the selected target may use a separate entry-city placement path. The latter is not demonstrated for Ottawa by this capture.
- Native `CIV_ASSETS/Base/Assets/UI/Choosers/EspionageChooser.lua:610–618` also directly checks/requests SPY_TRAVEL_NEW_CITY, with no explicit Wake in that dispatch function. Expansion1/2 chooser replacements include it and contain no overriding travel request. Thus absence of an explicit Wake alone is **not** proof that our implementation omitted a vanilla step. CIV_ASSETS denotes the installed read-only game asset root; no external source is edited.
- Native `CIV_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua:544–546` considers remaining moves when presenting operations. Its action handler also has a turn-processing guard. Ready=true is not a substitute for either complete native admission context or a successful CanStartOperation. Their role in this failure remains unknown.
- The B222 permission guard and reason query both return false. The latter successfully returns a table but no FAILURE_REASONS entry: `reasonQueryStatus=READ_OK`, `reasonResultHint=2`, `nativeReasonStatus=NO_REASONS`, count0, not truncated. This is not a missing API, diagnostic exception, redacted explanation or parsing failure; the queried engine surface supplies no explanation here.

The three captured successes support the common centre-based task pipeline. They do not prove WORKS, every destination, or the manual-sleep redispatch boundary. Retain B221's earlier denial and all frozen results.

## What this log cannot certify

The collector repeatedly completes a 30-second listening period, encounters `SOCKET_UNAVAILABLE` while connecting again, and reconnects about5–6 seconds later. The final gap is18:48:29.516–18:48:34.728. The bounded trace preserves startup/failure records31/32 across reconnection; direct Gate prints are not retained in that ring.

No final `admission=REJECTED`, corresponding ACTIVITY acknowledgement, verified ARRIVED save, HELD error or post-denial READ is present. Therefore **B222's new clean-rejection unwind remains USER_GAME_TEST_REQUIRED**, even though the failure itself and zero native requests are captured. Do not infer the final phase from the pre-attempt ARRIVED record or from expected source behavior. The log also cannot distinguish the final selected category or certify unchanged Insight state after that failure by direct readback. Static code establishes that no completion/reward path is entered by the recorded pre-request branch.

The socket gaps limit evidence; they are not evidence that the game loaded a save, that gameplay failed during every gap, or that the socket caused native permission denial. No new collector behavior is implemented in this review.

## Narrow continuation proposal — not implementation authorization

1. Focus the next bounded investigation on **manual idle sleep → dispatch → arrival admission**, comparing the current native and custom routing rather than changing mission eligibility, reward or task duration. Keep the previously working PEOPLE/PLACES pipeline.
2. If a diagnostic delta is approved, record one bounded scalar sample at the existing dispatch/arrival/task events: actual activity, remaining moves, native Spy operation/end-turn and available turn-processing context; distinguish direct arrival from entry-city placement. Record the actual Gameplay rejection/save outcome in the existing reconnect-readable trace. Unavailable readers remain UNKNOWN. No timer, automatic retry, forced Sleep/Wake, extra permanent state or global scan.
3. A repair must follow the result: normalize a demonstrated transition defect through the native operation and its confirmation, or explain a demonstrated admission restriction. Do not assume that a longer wait, blindly waking on arrival, restoring PlaceUnit, or bypassing a false permission result is a fix. Any wake ownership/re-dispatch behavior change needs a separately approved scope and targeted local counterexamples.
4. No new native test is requested now. Only if needed after the specific evidence/fix is prepared, a bounded awake-departure versus manually-slept-departure comparison at the same destination would distinguish the leading hypothesis. Do not repeat all three mission types, prior save/load coverage or a long session merely for completeness.

WORKS target availability, Tourism rounding/settlement, source-loss reattachment and other deferred work remain separate. No new batch is authorized by this review.

## Preservation and checks

Original collector files remain ignored and unmoved at their session path:

- `records.log`: `ff85ca0e6e8f6ff69abdafe156473a560d03f7947f27871b286941981f06b882`
- `events.jsonl`: `0721aae72dcbb34d21bb225ee0ff09fb50528bfa3176b7858b273950e1ce371a`
- `summary.txt`: `826968b602328ab1106086a0f04643f6697497bf0c079b44dc7d79ae6c2aaeec`

Read scope: current authority/slice, B222 local and B221 native reports, submitted session, direct activity/Gate/idle-action/travel sources, exact native chooser/UnitPanel entries, and collector capture/reconnect handling. No gameplay/test/Design/Architecture change, live query, deployment, configuration change or game launch. Existing381 local tests are inherited, not rerun or promoted to native PASS. Context/selector, changed-document links, publication and diff checks validate this documentation checkpoint.

User decision: whether to authorize the narrow transition investigation/diagnostic proposal. User testing: none requested now. Primary next: wait for that boundary; no implementation or new deployment.
