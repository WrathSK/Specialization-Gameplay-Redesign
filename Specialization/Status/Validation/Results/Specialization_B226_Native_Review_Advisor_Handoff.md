# B226 native review and open-topic Advisor handoff

**USER_GAME_TEST_PASS: user-confirmed Great Work refresh only. USER_GAME_TEST_FAIL: Expedition task startup in this session. Culture Network native arithmetic/withdrawal remains USER_GAME_TEST_REQUIRED.** This is an evidence record and advisory commission, not repair authorization.

Basis: clean `develop` HEAD `158c11f`; runtime B226.253 / modinfo253, deployed source `fee812f5a142b40d9585f291f208b15791d6ebbb`. The [B226 implementation/deployment record](Specialization_B226_Culture_Network.md) records receipt `B226.253-fee812f-playtest.json`,226/226 MATCH and digest `33fd04da7945deaa1758cab42810bdd5283a7a241affbe0ec6b3557859c8f8a1`. Deployment is inherited from that verified record, not re-certified by this review. No implementation, tests, configuration or external runtime was changed for this handoff.

## Accepted result and latest trace

The user confirms that Great Work refresh now works and Expedition missions still fail. Record the former as scoped user acceptance; the submitted trace has no dedicated Aesthetic/native-yield sample independently proving it. Do not repeat that already accepted test. No Culture Network native result is supplied; Insight history/Tourism output is not specialist network-yield evidence.

Ignored local evidence: `local/diagnostics/B205/session-20261017T233523Z-64ba2a/` (the B205 directory/prefix identifies the shared collector, not the deployed build). Raw files remain unchanged and outside Git.

| Original | SHA256 |
|---|---|
| `records.log` | `cf484c39c6ebdefba25a325cc9370af2e2c47f26172fad43e03f207932607935` |
| `events.jsonl` | `0f91e2d7f037bd7fbbb1202642ed9861a55e6ae6d05dd7d7e628a2d1b9c513a8` |
| `summary.txt` | `a541572e0cfeb8521b2e4d6ee7c76fb2a913204966dbbb9acf84694a1ce5ec23` |

57 physical log lines contain36 unique TRAIN records and21 Gate prints. Use `seq` and turn for transition order: reconnect snapshots can appear physically after later live records. Wall-clock stamps are capture times, not precise native event timestamps.

| Record / physical lines | Observation |
|---|---|
| `seq1–6`, lines1–6, T75 | Gate, Gameplay, Production UI, Log UI and Activity UI initialize; one load-close. The Activity diagnostic constructor ran. This does not establish that its refresh handler ran. |
| `seq7`, line20, T75 | Existing team `E0-1B0006-8`, unit3342342, WORKS at destination centre(20,13): request accepted, Store revision130 confirmed and saved phase matches TASK_PREPARING. `taskStart=NIL`, `taskDue=NIL`, `owned=false`, `releasePending=true`. |
| Lines22–24 | Subsequent READs still show TASK_PREPARING; END then reports ENDED. |
| `seq8–29`, lines25–46 | A replacement team is trained/bound in the same T75. Captured source population is11; native UI cost165. This is context, not a new training-cost/population acceptance campaign. |
| `seq30–33`, lines49–54 | New team `E0-350006-9`, unit3473414: dispatch accepted at revision139. Travel UI reads activity1797587246, moves4/4, ready=true, Spy operation-1/endTurn0 before native dispatch; request call returns. |
| `seq34–35`, lines55–56, T77 | Native arrival replaces unitID with3538954. Logical team key and sourceCity65536 persist; exact centre(20,13), ARRIVED and revision140 confirmed, savedMatches=true. Pre-arrival savedMatches=false is followed by the confirmed update, not by a captured binding error. |
| `seq36`, line57, T77 | WORKS accepted again, revision141/TASK_PREPARING confirmed. Task clock still NIL, owned=false, releasePending=true. No subsequent task transition is captured. |

Both an existing arrived team and a newly trained→dispatched→arrived team reach accepted TASK_PREPARING without recorded activation of the task clock. The collector continues reconnecting until its user-interrupted stop at23:43:37 UTC; there is no second recorded load generation in this session.

**Important evidence gap:** no ACTIVITY_START, ACTIVITY_FAILURE, ACTIVITY_RELEASE, Activity acknowledgement, evaluationOrigin, signalOrigin, coreBusy or operationEvent is captured. Therefore this session does **not** establish another native SLEEP refusal, a SLEEP request, or a handler that executed and rejected. It leaves the accepted Gameplay start→UI activity processing→acknowledgement chain unaccounted for. Context-local UNAVAILABLE getters in Gate records are not evidence of corrupt native state; the Travel UI could read those APIs.

`summary.txt` says `alerts:none`, but the collector alerts cover sampled population/cost anomalies, not mission completion. Snapshot META counters for suppressed/errors/sinkStatus are not preserved by the collector; absence of an activity record alone cannot prove flawless diagnostic transport or that every handler was absent. See [collector](../../../../tools/collect_expedition_trace.py) and [snapshot reader](../../../../tools/read_expedition_trace.py).

## Previous evidence and Primary attempts — starting points, not conclusions to preserve

| Evidence | Relevant boundary |
|---|---|
| [B194 native review](Specialization_B194_Expedition_Pending_Activity_Native_Review.md) | The earlier no-reward prototype reached observed SLEEP, completed its two-turn clock and released owned activity. The mechanism has worked; do not assume it is universally impossible. |
| [B214 repair/result](Specialization_B214_Expedition_Task_Start.md) | Successful-task assertion repair; its subsequent two PEOPLE successes are recorded in that same result. Earlier working paths are counterevidence to a blanket failure claim. |
| [B222 native review](Specialization_B222_Task_Start_Native_Review.md) | Three PEOPLE/PLACES successes followed by Ottawa pre-request DENIED; manual sleep→redispatch was a hypothesis. Final ACK coverage was incomplete. |
| [B223 diagnostics](Specialization_B223_Native_State_Diagnostic.md) | Existing-event native scalar and durable request/readback samples added. No new timer or automatic recovery. |
| [B224 native review](Specialization_B224_Native_Review.md) | Manual-SLEEP completion/menu omission, city-WORKS exact-object cancellation and subsequent native denial. Core-busy event-only denial was a supplied local counterexample, not observed engine causation. |
| [B225 implementation](Specialization_B225_Task_Scheduling_Lifecycle.md) | Events now request deferred UI refresh; ARM/SLEEP/WAKE observations are separated. Manual-unowned-SLEEP completion normalizes; WORKS uses current city-level eligibility; sale invalidation uses the native deal event. These are actual changes, not proof of the current native cause or a successful repair. |
| [B226 implementation](Specialization_B226_Culture_Network.md) | Adds network/retirement; does not change the B225 task scheduler. Local670 PASS did not certify that this custom UI context receives native deferred callbacks. |

The B225 report describes synchronous event evaluation as a structural fault. Its local counterexample demonstrated that supplied condition; treat attribution of the recurring native failure as a prior Primary interpretation to re-evaluate, not a premise Advisor must defend. The newest evidence fails earlier in the observable chain than the previously recorded native denial.

Existing Advisor findings are also starting points, not automatically current defects: [Expedition review](../../../Reports/Advisory/Architecture_Engineering_Audit/Expedition_Review.md) and the optional ignored local report `Specialization/Reports/Advisory/B204_Native_Issues/B204_Population_And_Task_Start.md` (not a public evidence link). Respect their versions and explicit corrections; do not revive withdrawn population attribution or spend this review repeating unrelated audits.

## Advisor commission — topic-scoped, independent and open-ended

**Authorized question:** Why does the Expedition's normal repeatable travel/task lifecycle still fail intermittently or stall after successive fixes, and what is the soundest bounded repair or architectural change? Assess whether the chosen activity, context and ownership approach itself is appropriate; do not assume the answer is another SLEEP guard, a delay, or a local patch.

This user-authorized review is topic-scoped, not a file whitelist. Independently follow relevant callers, dependencies, shared UI/lifecycle infrastructure, Git history, earlier native evidence and read-only Civilization VI/HD/other Mod sources as needed. Challenge Primary interpretations, fixture fidelity and the diagnostic channel; pursue alternative explanations or a different technical route when relevant. Record why significant expansions are necessary and where evidence stops. No per-file, per-history or external-location approval is needed; unrelated projects or a genuinely separate review topic still require user authorization.

Suggested entry points, **not mandatory hypotheses or limits**:

- [Activity Lua](../../../../Mod/UI/ExpeditionSpyActivity.lua): `schedule`, `pump`, `refresh`, `evaluate`, initialization/shutdown and acknowledgement; [its XML](../../../../Mod/UI/ExpeditionSpyActivity.xml), package context registration and actual native RequestRefresh delivery.
- [Gate](../../../../Mod/ExpeditionSpyGate.lua): published activity intent, task admission, ARM/ASLEEP/release/cleanup and saved readback; [Store](../../../../Mod/ExpeditionSpyStore.lua) if persistence or duplicated ownership matters.
- [UnitPanel adapter](../../../../Mod/UI/ExpeditionSpyUnitPanel.lua), [Window](../../../../Mod/UI/ExpeditionSpyWindow.lua), [travel/current-facts reader](../../../../Mod/ExpeditionSpyRead.lua), [shared diagnostic producer](../../../../Mod/ExpeditionTrainingDiagnostics.lua) and collector transport when following the chain requires them.
- [B225 targeted fixture](../../../../DevelopmentTests/test_b225_task_lifecycle.py) and [deferred refresh fixture](../../../../DevelopmentTests/refresh_fixture.py), read-only: which assumptions are native-confirmed versus supplied by the test? Prior local PASS remains scoped.
- [Current Expedition plan](../../../Architecture/v2/P0_N_Expedition.md), [accepted Culture contract](../../../Design/Content/Culture_D0051.json), and relevant native Spy/UI implementations. External evidence must identify source/version/context; source presence alone is not native behavior.

Current accepted constraints are context, not authority for Advisor to change them: own capacity/source binding/history, no ordinary-Spy interference or native espionage reward, city-centre execution for v0.1, no newly introduced timers, and no fabricated native acceptance. A route that would require changed gameplay or authorization must be presented to the user as such, not silently adopted. No new implementation or user test is authorized by this commission.

Follow [Advisory guidance](../../../Reports/Advisory/AGENTS.md). Write only an owned Markdown report in a suitable authorized Advisory topic (reuse a relevant topic or create `Reports/Advisory/Expedition_Task_Lifecycle/` beneath `Specialization/`). Do not modify Mod, tests, Design, Architecture, Status, governance, hashes, configuration or runtime; do not run tests/prototypes, launch the game, stage/commit/push, deploy or change roles. Primary writes no Advisor-owned report for this handoff.

Return: a short plain-language diagnosis; ranked findings with evidence strength and affected boundaries; competing explanations and counterevidence; a proposed repair boundary or alternative with tradeoffs; and the smallest discriminating next action if evidence is genuinely missing. Prefer existing logs/source to more user blind tests. Mark the exact owned report Stable and pause its writes for Primary review. Publication does not adopt findings or authorize repair.

## Checkpoint

Great Work refresh accepted in this scope; Expedition startup failed; Culture Network native gate remains pending and is not rejected solely because its source-category setup could not progress. Existing local results and deployed B226 package remain intact. No next implementation/deployment batch is authorized here.

User decision: none now. User testing: none newly requested. Primary next: provide this record to the existing Claude Advisor, await its independent report, review it and obtain any needed implementation decision. This record prepares the handoff; it does not claim that a message was delivered to an external conversation.
