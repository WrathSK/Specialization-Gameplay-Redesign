# B398.425 — bounded Study / Dialogue queue recovery

2026-10-31. User-approved [queue repair](../../../Reports/Proposals/Timed_Project_Queue_Recovery_and_Remaining_Playtest.md); PT016. Baseline `487d674`; last verified live B397.424 from `aa51feb`, stable/main B307.334. Design D0058 / Architecture A0183. **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED.** Deployment is recorded separately below only after the receipt succeeds.

## Behavior and scope

Engineering Study and Era Dialogue now opt into a bounded session-only queued-entry owner. A production-list choice must be confirmed in the real native queue; later same-city production/queue events may recheck it. When it becomes the sole eligible current project, Gameplay can establish a fresh complete-turn round. Waiting/interrupted time is not credited. Head-plus-tail remains paused under the accepted single-item rule. Normal ACTIVE rounds and their original id/start are preserved when a temporary tail is removed.

A second copy is refused, including repeated clicks before the first asynchronous insertion is confirmed. Explicit native index0 replacement/removal intent may abandon only an unconfirmed insertion, not a saved round or proven queued entry. Already-existing duplicates remain blocked with an explanation; no automatic queue removal or FinishProgress-based disposal is added. Exhausted knowledge/used-era candidates stop. Queues do not reserve E/L, future prerequisites, era quotas or rewards.

Both Gameplay owners fence a new start after their local END and recheck the existing native IsTurnActive boolean. An interrupted old round is canceled before DUE/MISSED normalization; current reference/qualification is reread. A missed round may restart without compensation; a valid DUE round settles through its original path, then ends this admission instead of chaining a second start. CALLING/ambiguous HELD and exact receipt/readback guards remain.

Verified receipt id/completion turn are projected as two temporary owner-view scalars, not new saved authority. An existing candidate retires when its completion id advances. Initialization captures queue evidence before Sync, and refuses automatic re-entry if a completion in this loading turn makes the remaining native item ambiguous. That case explains explicit reselection rather than assuming a stale getter proves a new queued round.

Only two project UIs opt in. Claim policy, profession formulas, E/L definitions, Dialogue start-era quota/completion collection, saved structures, network transport, D1/D2 policies, GC and unrelated modules are unchanged. No formal Design/Architecture or external Mod/game/config file is modified. User-confirmed no-P0 operation stays accepted and is not reissued as a test.

## Files and runtime impact

- `Mod/UI/TimedProjectQueueIntent.lua`: owned queued candidates, bounded canonical queue sampling, insertion/outcome gates, fixed-capacity status hints and lifecycle retirement. It never writes properties, changes native queues or grants rewards.
- `Mod/UI/TimedProjectSelectionClient.lua`: fixed opt-in hooks for existing city events, initialization and relevant deferred opening; Claim remains opt-out. Existing event-major listener order and no-frame setup stay.
- `Mod/UI/EngineeringStudyUI.lua`, `Mod/UI/DialogueProjectUI.lua`: opt-in, explicit selection/status integration and unconfirmed-selection cancellation. Existing owner status remains authoritative; hints are presentation-only.
- `Mod/UI/CrewProjectOrder.lua`: capture side-effecting CheckQueueItemSelected once for the adapter chain; selected existing slot cannot fall through to the base BUILD. The base operation/arguments/returns remain for a genuine native selection. Existing replacement/removal observations provide explicit cancellation evidence.
- `Mod/EngineeringStudyProjects.lua`, `Mod/DialogueProjects.lua`: local start-window fences, interruption-first normalization and receipt-derived temporary completion metadata. Their existing independent settlement owners remain.
- `Mod/Probe.lua`, `Mod/SpecializationP0.modinfo`: build425 and one packaged helper. `DevelopmentTests/test_b398_queue_recovery.py` adds41 methods; the common Store native double supplies the verified IsTurnActive method without altering assertions.

Runtime Impact Contract was recorded before code in the approved plan. Actual limits: at most2,048 candidate slots plus an independent2,048-entry hint ring per opt-in instance; native queue sampling rejects more than100entries using the existing Mod defensive ceiling, not a claimed engine capacity. Only scalar references/intent/proof state are retained; queue indexes are observation positions, not identities. Sampling uses existing GetSize/GetAt/Directive/ProjectType resolution and current hash, with before/after reference/turn/generation/revision fences. No building/district/empire sampling on a queue event.

Idle publish uses O(1) work/backend-revision/open/closed checks; without a cause it does not rescan candidate views or call native queue getters. Events are coalesced per candidate until safe publication. Deferred start-window recovery has at most one lifecycle permit per candidate/game-turn; unchanged repeated lifecycle callbacks do not replenish it. Unknown send outcomes gain no retry merely from turn passage; no timer, fixed delay, polling or no-progress resends. Optional diagnostics do not control start or settlement.

Native API evidence: Base UI LocalPlayerActionSupport.lua10 and WorldInput.lua1361/1384 use IsTurnActive; existing B397 Gameplay COMMERCE_TURN_END/STARTED records show false/true from the same getter. This avoids inventing a Gameplay-only API absent from the real environment. Native queue API/signature evidence is retained in the approved plan; only relevant source was read, not edited.

## Automated evidence

Python3.14.8 / Lupa2.8, actual Lua5.1 modules with explicit native method/event doubles. **85 selected unittest methods pass:** primary selection83, plus two existing RealOwners methods in independent processes (their shared measurement key cannot be registered twice in one process). New-file41 methods include three explicit historical-source counterexamples. Another five unchanged legacy adapter-differential methods pass against their exact old-source reference; these are historical controls, not current behavior-neutral certification.

Run from repository root with Lupa2.8 available and DevelopmentTests on PYTHONPATH (the local execution also used its ignored dependency installation):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q test_b398_queue_recovery test_refactor_s7d2.Permit test_refactor_s7d1.Classification test_refactor_s9e10.Roles test_refactor_s9a1.Registry test_refactor_s9a2.ActualUI test_b395_culture_recovery.DialogueStartup test_b395_culture_recovery.CurrentReplacement test_b267_preplaytest.Package.test_actual_lua51_syntax_and_manifest_closure
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q test_refactor_s7d1.RealOwners.test_ambiguous_nil_positive_preserves_pending_recovers_same_city_and_then_completes
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q test_refactor_s7d1.RealOwners.test_normal_full_turn_and_confirmed_other_outcomes_match_baseline
```

Actual UI adapters→selection client→TimedProjectReaders→independent owner→Store/notification fixtures prove: confirmed append across turns; reorder/multiple→sole; source-free events do nothing; duplicate and unresolved-insertion clicks; native read UNKNOWN/reentry; same-turn ACTIVE preservation; actual once-only reward; exhausted knowledge/era; closed/unknown/inactive phase; MISSED versus DUE; interruption-before-DUE; native END reentry; a stale queue after completion; Sync-before/after-completion initialization; bounded hints; fixed lifecycle budget;1,000idle publications with zero extra queue **and candidate-view** reads; diagnostics on/off identical business records/writes; restricted runtime without raw access/standard libraries; selected-slot and all eight sibling adapter isolation controls.

The committed baseline comparisons use `git show 487d674` with separate historical execution identities; no checkout/reset or frozen assertion changes. Baseline actual sources lose an explicitly confirmed queued candidate over a turn and drop multi→sole re-entry; the selected-slot double checks cause an unwanted native BUILD. Current counterparts pass. Review found asynchronous insertion duplication, notification reentry, unbounded terminal hints, interruption/DUE priority, and stale-read initialization cases in early drafts; dedicated assertions now pass. Those draft results are not native claims.

All **220 runtime Lua files compile under Lua5.1**,25XML files parse,342unique modinfo references resolve across343runtime files. No runtime deletion/SQL/save migration. Package digest before commit: `d068aace17220003524b5ffa7c1babaec194c7f903196f424c8e170d4d2a9274` (rechecked before deployment).

### Broader inherited selection was not all PASS

An initial overbroad module selection expanded to773 historical methods and did not pass; it is not the final gate or a full U4 claim. Three inherited assertion failures (Dialogue corrupt-history protection and two S8b8 template-history isolation expectations) were each reproduced unchanged in independent487d674/current-source runs. Eight other error records require absent external read-only DB configuration; no external DB was substituted or assertion weakened. Two RealOwners aggregate failures were duplicate-measurement registration, then passed separately. Five raw adapter-trace comparisons intentionally differ because the old contract repeatedly reevaluated the side-effecting selection check; all five still pass at their exact old source, while current native-operation/containment controls verify the explicitly approved fix. No out-of-scope repair or mechanical backlog closure follows.

## Evidence limits and minimum user delta

The composed fixtures use a single LuaVM and a fake native queue. UI sends call the real owner directly, not the live dispatcher/engine transport; newUI is a UI-generation rebuild, not a native save load. Late getter/END/order cases are conditional local counterexamples, not claims those exact engine schedules occurred. Actual queue events/transport and continued existing-save behavior remain USER_GAME_TEST_REQUIRED. There is no new persistent schema, but no general old-save migration guarantee.

With an available opportunity, no P0 needed:

1. Engineering Study behind an ordinary target: let the target finish naturally, leaving Study as the only entry. It must start a complete round and award one L only. Clicking its list entry again must not append another copy.
2. Dialogue: reorder with an ordinary target, then remove the other entry so Dialogue is sole. It must recover one-turn timing and settle once. Existing used-era restrictions remain.
3. When convenient, save/reload a queued **not-yet-started** project. Unambiguous queue evidence should recover. If this same turn already completed a previous round and the saved queue cannot prove a new item, the new explicit-reselection hint is the deliberate safe boundary. Existing ACTIVE timer recovery remains its own path.

No repeated profession-yield, GPP, ownership, forced pillage, all Crew variants or no-P0 test. Confirmed exhausted native leftovers are explained for removal by the player; the Mod does not remove them or use completion to dispose of them. Lost native BUILD confirmation remains locked until real entry or explicit replacement/removal evidence; no speculative retry.

User decision:none further inside this batch. User testing:the small queue delta after verified deployment;ordinary Commercial testing may continue separately. Primary next:finish integrity/privacy publication and existing safe temporary-develop deployment if the game is reliably exited;then stop. Option B migration,cold source-consumer integration,S10 and main promotion are outside this repair.
