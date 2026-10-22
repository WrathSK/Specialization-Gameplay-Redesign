# B224 native review and proposed B225 repair

**PARTIAL native acceptance; task workflow FAIL.** Native evidence is the user's current test report plus ignored collector session `session-20261017T200209Z-be5b64` under `local/diagnostics/B205/`. No new Mod, tests, external package or configuration changes in this review. Live remains B224.251.

## Evidence

`records.log` SHA256: `9e2a6385e0c068524231612a27f95c548ca351b78b3dfd8534561227b5b4b806`. All104 lines, summary and event metadata were reviewed;39 unique trace records. Raw originals remain ignored and unchanged. No screenshots were required to reconstruct the task transitions.

| Observation | Evidence and scope |
|---|---|
| Ottawa PEOPLE success | T65 start; T67 SUCCESS / Canada / NEW; RELEASED returns ARRIVED revision117. |
| Ottawa WORKS success, task menu blocked | T70 starts while already manually SLEEP, ASLEEP acknowledged owned=false. T72 SUCCESS / Canada / NEW. Later READ remains TASK_COMPLETE; travel works but TASK UI requires ARRIVED with no taskStart. |
| Khmer WORKS cancellation | T74 starts; T75 CANCELLED TARGET_INVALID; owned release correctly returns ARRIVED revision127. Exact old building/slot/type/instance checks can cancel for movement/replacement; the log does not identify which concrete native field changed. |
| Khmer restart blocked | Next TASK accepted, but native SLEEP DENIED despite AWAKE,4/4 movement, ready=true, Spy operation=-1. No native request attempted. REJECTED response restores ARRIVED revision129 without task clock or ownership. This confirms B222's rejection unwind within this actual scenario; admission is still faulty. |
| City Insight Tourism | User confirms effective source-city Tourism, engine Floor accepted, no other-city gain. The explicit report shows7 effective Insights and source-city+14%. Native acceptance is user-reported for settlement and city isolation; collector confirms configuration, not arithmetic by itself. |
| Aesthetic empty collection | User confirms turn synchronization clears the benefit and putting works back restores it. Sale itself fails to refresh until the next turn: immediate trade invalidation remains FAIL. |

## Confirmed defects

1. **Unowned manual sleep misses logical completion.** Gate `releaseActivity` selects NONE when the task does not own native SLEEP, but never runs `returnToCentre`; task fields remain TASK_COMPLETE. UI permits travel from that state and rejects TASK. Actual current Lua counterexample reproduces a successful unowned task with TASK_COMPLETE/NONE and retained taskStart, and the actual UI reproduces TRAVEL=true/TASK=false. This is a completion omission, not a missing successful quota.
2. **Native admission after owned release is still rejected.** Khmer's confirmed logical return and subsequent final rejection are fully recorded. Restoring the task menu alone cannot address this path. Next investigation stays on the existing release/Wake/admission/native action sequence; no permission bypass, movement reset, timer or user blind-repeat package is proposed.
3. **Trade-completion invalidation is missing.** UI `DialogueRefresh` listens for GreatWorkCreated/Moved, city changes, local turn, load and district changes; governor events recompute without recollecting slots. Generic UI publication pulses only drain dirty/pending work. Neither the producer nor `GreatWorkFacts` listens for DiplomacyDealEnacted. Native UI does: `CIV6/Base/Assets/UI/LaunchBar.lua`369–373,818 refreshes works on the no-argument deal event. `GreatWorksOverview.lua`1045 confirms the existing first-four GreatWorkMoved callback arguments. This explains why a sale updates the original UI but waits for the Mod's turn refresh. Installed Mac Steam Civ VI1.4.6 /376653.178 is the inspected read-only source; CIV6 is a source-root label.

## Accepted Design delta

The user explicitly changes v0.1 WORKS to a target-city predicate: continue while any eligible work remains in that city. A different remaining work is not a substituted specific target because no specific work is now locked. Confirmed empty city cancels; UNKNOWN remains protected. PLACES retains its selected-Wonder contract. Recorded as Design D0051 / Culture D0051; B224 runtime still implements the earlier exact-target behavior.

## Focused follow-up — recurring native SLEEP rejection is the priority

The user redirects priority to the repeated common admission failure. It is not treated as an isolated mission detail. The task framework currently makes every custom task depend on a generic unit SLEEP admission; native espionage instead uses SPY_* operations and ACTIVITY_OPERATION. One successful no-reward task proved that route in its observed session, not reliable repeat/release across all native event phases.

**Confirmed local structural gaps:**

- `UI/ExpeditionSpyActivity.lua` immediately calls pump from GameCoreEventPublishComplete, UnitActivityChanged/Move and local-turn callbacks. pump may process four synchronously reentrant rounds; ARMED/ASLEEP/RELEASED acknowledgements submit another Gameplay request. The first false SLEEP predicate becomes terminal REJECTED and clears the attempt, even if a later native update would allow the action.
- Owned release is acknowledged on AWAKE/HOLD alone. `GetSpyOperation()==-1` excludes an espionage mission, not the generic SLEEP operation lifecycle. Native operation activation/deactivation/clear and activity are distinct event surfaces. The current bridge does not observe the former.
- B224 already re-resolves current units. Both independent UI contexts deny operations, and the exact same unit had SLEEP allowed before cancellation and denied afterward, with4/4 moves. Stale selected proxies, static unit classification, absent moves, mission category and the no-results/NO_TARGETS argument difference are poor explanations for this captured transition. Restoring mission teleport is not a relevant fix.

**Native scheduling precedent:** installed `CIV6/Base/Assets/UI/Panels/UnitPanel.lua`2424–2458 and2477–2479 request ContextPtr:RequestRefresh after movement/operation/command changes;2368–2370 clears the request then refreshes;4225 installs SetRefreshHandler. The comments explicitly describe a next-frame UI update. This is one event-requested coalesced refresh, not a timer or an every-frame scan. Native unit-selection and turn paths also have direct refreshes; the conclusion is specific to operation events and our synchronous ACK chain, not a blanket ban on synchronous reads.

The existing API inventory also distinguishes UI CanStartOperation/GetActivityType from Gameplay writers: [author-maintained UnitManager reference](https://sukritact.github.io/Civilization-VI-Modding-Knowledge-Base/UnitManager). The installed native/HD source, rather than that inventory alone, establishes the checked hashes/call signatures. WAKE is a generic command, not the native Spy CANCEL route.

**Actual-Lua counterexample:** the real Activity+Gate fixture was run with a native stub denying operations only during an explicitly modeled core-busy event phase. Current code immediately returns ARRIVED/ACTIVITY_SLEEP_NOT_ALLOWED with no SLEEP request; after the stub becomes available, publication does not resume the discarded attempt. This proves the terminal-handling vulnerability under that supplied condition; it does not claim that the actual B224 engine was busy. The actual log did not record callback origin, UI.IsGameCoreBusy or generic operation lifecycle events. The persistent event-driven DENIED samples do not independently sample a quiet UI refresh phase.

**Preferred next boundary:** fix the Activity context's native-operation scheduling first, using its own SetRefreshHandler and a single RequestRefresh from relevant events; re-read the current activityKey, exact unit/reference and native state in that handler. Publication callbacks should not synchronously initiate native operations. Coalesce events, discard stale work, and never self-schedule an indefinite retry. Preserve the UnitPanel's existing native refresh handler; request its refresh rather than replacing it. Retain native permission checks and one-request semantics. Release must distinguish activity observation from unresolved operation processing; do not blindly wait for a particular event that might not occur.

Only a small bounded evaluationOrigin/coreBusy and operation-event sample is needed alongside the existing ring to validate the repaired boundary. No generic telemetry layer, forced Wake, movement restoration, new timer or repeated blind task campaign. If native denial persists in a confirmed safe refresh, the next action is that exact operation lifecycle, not another unrelated UI patch. There is no new implementation authorization in this investigation.

## Proposed B225 scope — not implementation authorization

Priority: the common native-operation scheduling/release boundary above, before adding further task behavior.

- Normalize success/cancellation back to the same-city idle state whether native sleep was task-owned or manually pre-existing. Do not Wake unowned sleep. Keep the task panel openable even when every category is already complete; disable individual completed/unavailable rows. Preserve reward history and exact verified source/team references. Include actual pre-existing sleep completion/cancel/repeat counterexamples; existing tests that assert the old blocked UI must be corrected with the implementation.
- Change WORKS validation at both admission and continuation/completion to a fresh, bounded selected-city eligible-work predicate before old building/slot/plot checks. Do not merely remove workID comparison. Reuse the correct UI-context reader/catalog and check endpoint/turn; no global inventory or new persistent record. Cover work movement within city, sold original with another eligible work remaining, original building emptied, true city-empty cancellation and UNKNOWN retention. PLACES unchanged.
- Bind no-argument DiplomacyDealEnacted in the single UI work producer, dirtying local-player work scope and using the existing publication drain. The event does not provide a proven city/item list, so one coalesced local collection is appropriate. No per-consumer event copies, foreign-city scans or new Gameplay invalidation needed. Test sale with no GreatWorkMoved/no turn advance, burst coalescing, same-turn EMPTY withdrawal, recovery and idle no-repeat.
- Before finalizing the batch, compare native release/Wake and immediate restart with the established no-reward/activity route. Repair only a demonstrated local defect; retain the native permission gate. The captured failure already supplies a precise case, so no new diagnostic-only blind session is the default. Any unresolved native admission defect must remain an explicit batch outcome rather than be hidden by the new aggregate predicate.

## Verification and handoff

This review executes only the actual-Lua completion/UI and modeled event-phase counterexamples above and document/path/schema/selector/hash checks. It does not rerun the490 runtime tests or claim a new source package. Proposed implementation uses targeted tests for changed completion/aggregate facts/trade events plus existing activity/rejection/Store and affected three-consumer regression. Native validation should be one continuous combined session, chosen after the repair is concrete; no additional save/load ritual or standalone Floor test.

User decision: D0051 rule is already explicit; none remains for that change. User testing: no further B224 repeats requested. Primary next: implement B225 only after explicit batch authorization; preserve the current package meanwhile.
