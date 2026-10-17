# B225 — common task scheduling, release and current city facts

**LOCAL_SIMULATION_PASS; native verification pending.** Implementation and guarded deployment explicitly authorized by the user. Source B225.252 / modinfo252. Actual deployment is recorded separately below and in Status; a source version is not a runtime receipt.

## Scope and evidence

This batch implements the bounded plan in [B224 review](Specialization_B224_Native_Review.md). That frozen review retains the Ottawa manual-SLEEP completion omission, Khmer cancellation/rejection, and the missing sale invalidation evidence. D0051 already accepts city-level WORKS; this batch does not make another Design decision. No capacity/source binding, permanent schema, Insight rule, GC, configuration, site movement, main promotion or unrelated audit repair is included.

The structural fault was synchronous Activity evaluation inside native event publication and its reentrant Gameplay acknowledgements. B225 uses the native event→RequestRefresh→SetRefreshHandler boundary. A native SLEEP denial at that later boundary still rejects safely; this is not a permission bypass or a claim that the captured C++ denial has been fully explained.

## Implementation and ownership

| Path | B225 behavior |
|---|---|
| Activity UI | Events merge into one replaceable pending refresh. The handler re-resolves the current lease, identity and native state; known core-busy state waits for another real event without self-polling. Missing busy API remains explicitly UNAVAILABLE, not false. |
| ARM / SLEEP | One transition per refresh. Gameplay ARM acknowledgement cannot recursively initiate SLEEP in the same stack. Native SLEEP is requested at most once; actual SLEEP observation starts the task clock. |
| Release | WAKE request returns before release observation. A later refresh confirms exact-unit AWAKE/HOLD; no particular operation-cleared event is mandatory. Ambiguous attempted writes retain their existing ownership protection. |
| Native events / UnitPanel | Activity, operation add/deactivate/clear, command and movement-point events request refresh for the exact current unit. UnitPanel keeps its native refresh handler and ordinary-unit callbacks; native eligibility is evaluated during deferred rendering and fresh clicks, not event publication. |
| Gate completion | Successful/cancelled tasks with pre-existing unowned SLEEP normalize to ARRIVED and clear only the finished draft. They do not Wake player-owned sleep. Owned release still requires its existing verified acknowledgement. Fault handling never recursively re-enters failed normalization. |
| WORKS | The always-loaded read-only UI endpoint freshly checks eligible-work existence in the selected target city. Any reliable eligible work makes it VALID; a reliably empty city is INVALID; incomplete negative evidence is UNKNOWN. Work ID/slot/building hints are not a task lock. PLACES remains selected-Wonder. |
| Trade invalidation | Parameterless DiplomacyDealEnacted dirties the existing local work collection once per event burst; the existing publication drain sends current facts, including EMPTY/count0. Aesthetic, Meaning and Inspiration retain their existing named delivery and carrier ownership. |
| Diagnostics | Existing bounded ring adds evaluationOrigin, signalOrigin, coreBusy and last native operation event/hash. No new logger, saved state or timer. |

The existing post-request readback watcher retains its 0.25-second sampling and 10-second bound; its samples now also request the safe refresh. **No new timer or periodic admission retry is added.** Ordinary event requests do not install a watcher. Native readiness, source loss, UNKNOWN, stale keys, wrong owner and displacement still block unsafe writes.

WORKS only reads the selected city's completed district/building slots with finite bounds (256 districts,512 buildings per location,256 slots per building,4096 total slots); it stops at a confirmed eligible work. It does not add an AI inventory history or a global city scan. Unknown earlier slots do not hide a later reliable positive. Unreviewed catalog metadata is UNKNOWN, not an empty city.

Read-only native source basis: installed Mac Civ VI1.4.6 /376653.178, `CIV6_ASSETS/Base/Assets/UI/Panels/UnitPanel.lua`2368–2370,2424–2458,2477–2479,4225; `CIV6_ASSETS/Base/Assets/UI/LaunchBar.lua`369–373,818. CIV6_ASSETS is a source-root label. Native trade callbacks expose no established participant-ID contract; no speculative filter was added. No external source was edited.

## Local verification

**617 targeted tests PASS**, including18 B225 differential tests. Python3.14.8 / existing Lupa2.8 lua55; configured gameplay DB opened read-only and copied to memory only. New differential cases cover event-stack versus safe-refresh denial, burst coalescing, busy waiting, stale/shutdown disposal, operation-event isolation, deferred WAKE completion, manual-SLEEP success/cancel/repeat, failed cleanup, city-level replacement/empty/UNKNOWN and deal-only same-turn zero/recovery/idle behavior. Shared Store, pending/readback, current-unit UI, diagnostics/collector, catalog and three real Culture consumer regressions are retained.

Three historical package-only checks pin193/199/200; they are not rewritten or counted as current PASS. The obsolete standalone Aesthetic SQL bootstrap is not a current fixture; its actual writer is covered by the maintained three-consumer integration. This batch does not run a gameplay-wide/stress test or claim native CPU/memory improvement.

Independent read-only review checked scheduling/native API use and city facts/trade events. It identified an error-handler recursion risk in the initial cleanup placement; normalization was moved to explicit completion sites, leaving generic hold/release safe. Local simulation does not certify native SLEEP availability or engine settlement.

## One combined native session

Start the manual collector before the game. Use the current supported test campaign; do not repeat saved-state/cold-load rituals for unchanged infrastructure.

1. At an available destination, complete one unfinished task (奇观巡礼 or 艺文采撷). Start while normally awake. After completion, open **任务** again: the completed category should be unavailable individually, while the panel itself remains usable.
2. Click native **休眠**, then **派遣到新城市** to a destination with an unfinished category. On arrival, **跳过回合／休眠** should be present as appropriate. Start the available task and let it complete. This exercises the previously failing sleep→dispatch→arrival and release/restart boundary. If a city has multiple eligible works and conveniently allows replacement/movement during 艺文采撷, change the original work while leaving another eligible work: the city-level task should continue. No artificial target setup is required; defer that subcase if unavailable.
3. In a Culture city currently receiving 风雅熏陶, sell its last eligible Great Work. Without advancing the turn, check that the recorded current eras and Aesthetic contribution become0. Put an eligible work back and confirm recovery. Other cities' own effects should remain intact. Use the existing reports/collector; a screenshot is only needed if visible output contradicts the record.

Stop on an admission/cleanup failure and provide that collector session; do not repeatedly retry blind. The fixed diagnostic now distinguishes event request, safe UI refresh, native permission and release receipt. No separate Tourism Floor test, save/load sequence or complete old mission sweep is required.

## Delivery and stop point

B225.252 deployed from `9a73208` after clean/pushed source verification and fresh automatic OS exit checks before both guarded switches. Receipt `B225.252-9a73208-playtest.json`; **224/224 MATCH**, source/runtime digest `10a72d37e04ff43740a27911064f7f6ed459e9ea11880cb6e535bad28fb14634`. B224 and stable recovery retained; no pending transaction, configuration change, main promotion or game launch. Deployment integrity is not native acceptance. User decision: none. User testing: the combined differential session above. Primary next: review B225 evidence; no N3, reattachment or unrelated repair is authorized by this batch.
