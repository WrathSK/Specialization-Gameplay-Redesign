# B399.426 — canceled-round queue recovery and disposable boundary observations

2026-11-01. Primary;explicit user authorization after [fourth-playtest review](Specialization_B398_Fourth_Playtest_20261101.md). Baseline6a9a05d;D0058/A0183. **LOCAL_SIMULATION_PASS / USER_GAME_TEST_REQUIRED.** No Design/Architecture,formula,permanent record/schema,network,GC,Claim policy,other Mod or game configuration change. No main promotion or game launch. [Before-code Runtime Impact Contract](../../../Reports/Proposals/Timed_Project_Queue_Recovery_and_Remaining_Playtest.md#b399-authorized-follow-up--2026-11-01-runtime-impact-contract).

## Repair and unchanged protections

B398 reused the same turn/candidate/queue/view admission signature after an accepted round was canceled and the project was reordered back to sole. A legitimate restart could therefore be rejected as a duplicate. Both project owners now project a **cancelledID** derived from their existing validated last/pending/completion records into temporary views. It advances only for a confirmed canceled attempt;completion receipts are excluded. Engineering audit uses its already-verified post-cancel write result instead of publishing the pre-cancel object. No additional Store/native read or new saved field is introduced.

The queue view/attempt signature and outgoing request identity incorporate that cancellation evidence. A confirmed canceled round with fresh sole-queue proof may start a distinct complete round,including multiple real same-turn cancellations. An unknown send or unconfirmed cancel does not gain a fresh identity merely because an event/time passed. Existing id/reference/window/eligibility/receipt protection,uncertain CALLING/HELD handling,E/L/era limits and duplicate-entry prevention remain. Only Study and Dialogue opt in;no automatic queue deletion,multi-item counting or interrupted-time compensation.

Modified business paths:[EngineeringStudyProjects.lua](../../../../Mod/EngineeringStudyProjects.lua),[DialogueProjects.lua](../../../../Mod/DialogueProjects.lua),[TimedProjectQueueIntent.lua](../../../../Mod/UI/TimedProjectQueueIntent.lua). The native-selection wrapper and project models are unchanged.

## Independent observer and bounded cost

[PlaytestBoundaryDiagnostics.lua](../../../../Mod/PlaytestBoundaryDiagnostics.lua) is a new optional observer. Gameplay starts it in a protected standalone block **after** existing listeners/composition/readiness;it is absent from production dependencies. One protected lazy scalar tap in ExpeditionSpyGate.Turn supplies the tracked owner/unit/expected coordinate/target pair before its original guard. The tap's output and return value are never consumed by business code. No saved object,ACK,qualification,resume trigger,transaction or writer depends on this module.

Default enabled for the first **6consecutive game turns** observed per Gameplay context. Limits per load:96Treasury samples,64position samples,8Treasury-change samples per distinct END/ACTIVATED interval,512phase-clock reads and at most4local-player lookups and4existing identity-helper admissions(then observer-only cached);foreign events cannot repeatedly call the identity helper. Duplicate lifecycle callbacks do not replenish an interval. Exhausted change/position allowances stop before extra native reads;idle publish does only a fixed flag/guard check. A first publish sample is allowed only after an actual local lifecycle boundary. Clock expiry/fuse and explicit Stop unregister owned subscriptions. A native event without a safe Remove interface is not subscribed.

Fixed optional subscriptions:PlayerTurnDeactivated,GameEvents.PlayerTurnStarted,PlayerTurnActivated,LocalPlayerTurnBegin/End,LoadScreenClose,three existing Treasury event names,first pending GameCoreEventPublishComplete,exact watched-unit MoveComplete/Teleported/ActivityChanged,its two-player DiplomacyRelationshipChanged,and exact UnitRemovedFromMap. No SystemUpdateUI,timer,fixed delay,whole event union,city/district/building/unit enumeration or no-progress retry is added. Missing/undelivered events remain an evidence limitation.

Treasury rows record precise balance and adjacent-sample delta,GetGoldYield,total and building/district/unit/WMD maintenance,turn-active and already-published network state. No Treasury setter is patched or intercepted. Position rows record expected versus actual coordinates,owner/id match,type/activity/Spy operation/moves and optional HasOpenBordersFrom(target). Only the already tracked unit is looked up. An unavailable API is explicit;arbitrary native strings and raw errors are not copied. These samples locate observed phases and cost categories;they do **not** independently identify every native/foreign-Mod posting origin or authorize the unit to act.

Direct added getter attempts use the existing observer counter through a protected optional Count call;counter failure cannot influence reads or business. Existing P.IsTestPlayer admissions are separately bounded to4per load,each at most4native/configuration calls;those helper-internal calls are not included in this direct-getter counter. Existing B205 transport's per-record clock/notification cost remains and is not claimed to be zero. Up to160sample rows plus bounded status/context records are admitted;each row has a fixed small set of getters. Native event registration/removal and predicate work are additional fixed/event-local costs. There are no retained native city/unit objects. The old broad B271 EventTimingDiagnostics switch stays **false**.

## Transport, collection and exit

B205 receives four scalar/precise allowlist fields for maintenance;its protocol,ring,turn limits and other users are unchanged. Existing reader accepts the new uppercase stages. Collector preserves received records in records.log and appends an independently capped first32-row boundary summary. Both runtime budget stops and summary truncation are explicit. This does not promise that the shared ring/passive transport captures every engine action;missing samples never become PASS.

Removal paths:

1. Set only `SPCPlaytestBoundaryDiagnostics.ENABLED=false` and load the verified package normally:zero new observer registration/reads/output. A running observer can call its own `Stop()`;owned handlers/watch/delta/pending state retire without touching gameplay.
2. Comment the single protected Gameplay startup block for the next fresh context. The remaining protected gate tap becomes inert. Do not claim a source edit unregisters already-installed handlers in a running Lua context;Stop or the normal exited-game deployment/context restart is required.
3. To delete completely,remove this Lua file and its **two** modinfo declarations;the optional startup/tap can be removed too. No save migration,carrier withdrawal,controller reconstruction or pending-business cleanup is needed. The collector-only summary block and unused extra scalar names may be removed separately. **Do not delete the pre-existing B205 transport**,which has unrelated existing users.

Exact independent exit tests cover off,absent,throwing observer/startup/sink/getters/counter,reentry,expiry/Stop,missing safe Remove and ordinary sibling listeners. Existing displaced-unit guard still returns HELD/TEAM_DISPLACED_STOP;there is no speculative border/teleport repair or income correction in this batch.

## Validation and limits

Python3.14.8 / Lupa2.8. **178selected methods pass:**176in the explicit combined selection plus two existing RealOwners methods in independent processes(their shared measurement label prevents grouping). **29new-file methods** cover real owner/Store/UI reordered cancellation,three same-turn round trips with unique request tokens and one eventual reward,unknown-send no retry,failed cancellation/no restart until real recovery,completion versus cancellation,and observer modes with equal business records/rewards.

Observer/transport tests cover zero idle/foreign/disabled work,separate sampling/clock/cached-player/identity-admission bounds,phase rearming,complete handler cleanup,missing/throwing APIs,finite false/zero/negative values,raw-string exclusion,real B205 precision/reader parsing,collector retention/truncation,and the actual Expedition guard with expected15 versus actual16 in native doubles. New observer/queue/guard tests run Lua5.1,including a profile with raw access/OS/IO/debug/module/GC APIs removed. Some inherited tests retain their original Lua5.5fixture;their inclusion is not a claim that all176use Lua5.1. All **221runtime Lua** files separately compile with Lua5.1;25XML files parse;343unique modinfo references resolve across344runtime files.

Initial wider selection ran176methods before the final hardening and included four failures. They are independently reproduced at baseline6a9a05d:three already-known unchanged reader-limit assertions(expect64versus current256and old deadline/limit outcomes) and the old NativeSample budget assertion with the same64-entry expectation. Reader source is byte-identical to baseline;the original diagnostic file was retrieved with git show for its control. No assertions or unrelated production code were changed. These four are separately retained evidence,not silently reported PASS. The final explicit selector excludes only those named baseline failures and asserts every loaded test class comes from the repository,to avoid temporary draft shadowing. A separate attempted run lacked filesystem access for20existing collector test setups;it was rerun with access to their already required ignored local directory and then passed without changing assertions. This is not a full historical/U4/U5 PASS.

Reproducible command scope:DevelopmentTests/test_b399_queue_boundaries.py;the B39883-method queue/adapter/owner/package selection;full collector and applicable reader/native-state classes with the four named existing failures separately retained. Use DevelopmentTests on PYTHONPATH and an installed Lupa2.8;the exact selector below is retained here so ignored logs are not required to reconstruct this run. The two independent methods are `test_refactor_s7d1.RealOwners.test_ambiguous_nil_positive_preserves_pending_recovers_same_city_and_then_completes` and `.test_normal_full_turn_and_confirmed_other_outcomes_match_baseline`.

Regenerable logs,explicit selector and the concise environment/result manifest stay ignored in `local/diagnostics/B399/`. No expanded Closure snapshot is committed. Source package SHA256 `7f1eae6b8ef33a0c865cadb651428fa79b5f6bf98fffb6601b43afcc75278077`. Native API/event delivery and Treasury/border causes remain USER_GAME_TEST_REQUIRED/UNKNOWN;native doubles are not an engine reproduction. No general old-save migration guarantee is introduced by this temporary-view repair.

## User delta and batch boundary

Continue the existing save/reload and two-investment plan;the captured contracts are dueT68. With a convenient opportunity,one already-started Study/Dialogue reorder→sole case should now restart and complete once. Keep the collector running during ordinary next2–3turns;the new short observation window is automatic. No P0 toggle,new GPP/pillage/ownership campaign,repeat of accepted abilities or forced border test is requested.

User decision:none further within this authorized scope. User testing:the small queue delta and already intended commercial play;Treasury/border records are evidence,not a claimed root-cause repair. Primary next:publish the verified batch,perform the existing safe temporary-develop switch if the game is reliably exited,record actual receipt/recovery,and stop. Main promotion and broader refactor remain outside this batch.

## Re-run selection

From the repository root,with Python3.14.8 and Lupa2.8 available,run this selector with `PYTHONDONTWRITEBYTECODE=1 python3 -` and the following stdin. It reports the four independently reproduced baseline failures separately rather than weakening them. Run the two RealOwners names above separately with `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=DevelopmentTests python3 -m unittest <full-name>`. The initial wider/baseline comparison logs are regenerable controls,not required runtime or restore inputs.

```python
import sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'DevelopmentTests'))
import unittest
names='test_b399_queue_boundaries test_b398_queue_recovery test_refactor_s7d2.Permit test_refactor_s7d1.Classification test_refactor_s9e10.Roles test_refactor_s9a1.Registry test_refactor_s9a2.ActualUI test_b395_culture_recovery.DialogueStartup test_b395_culture_recovery.CurrentReplacement test_expedition_trace_collector test_expedition_trace_reader test_expedition_native_state_trace.NativeSample test_expedition_native_state_trace.TravelAndArrival test_b267_preplaytest.Package.test_actual_lua51_syntax_and_manifest_closure'.split()
existing={
 'test_expedition_native_state_trace.NativeSample.test_disabled_or_exhausted_producer_stops_native_reads',
 'test_expedition_trace_reader.ReaderTests.test_output_record_limit',
 'test_expedition_trace_reader.ReaderTests.test_total_byte_limit',
 'test_expedition_trace_reader.ReaderTests.test_trace_fixed_schema_and_limits'}
def flatten(s):
 for v in s:
  if isinstance(v,unittest.TestSuite):yield from flatten(v)
  else:yield v
all_cases=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(names)))
assert existing=={c.id()for c in all_cases if c.id()in existing}
selected=[c for c in all_cases if c.id()not in existing]
for case in all_cases:
 module=sys.modules[type(case).__module__];assert Path(module.__file__).resolve().is_relative_to(Path.cwd()/'DevelopmentTests'),module.__file__
print('SELECTED',len(selected),'PREEXISTING_SEPARATELY_REPRODUCED',len(existing),flush=True)
r=unittest.TextTestRunner(verbosity=0).run(unittest.TestSuite(selected))
raise SystemExit(0 if r.wasSuccessful()else 1)
```
