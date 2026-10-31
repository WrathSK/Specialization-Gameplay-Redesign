"""B398 actual Lua51 UI/reader/owner/Store composition; native queue doubles only."""
import unittest
import subprocess
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
from refactor_harness import ROOT, Context, TrackedLua51, SOURCES, executed, completion
from hashlib import sha256
from test_refactor_s7d2 import ui_actual
from refactor_defect_fixtures import panel

KINDS=('Engineering','Dialogue')
def fixture(kind):
    v=ui_actual(kind)
    v.execute('''
    Players[0].IsTurnActive=function()phaseReads=(phaseReads or 0)+1;if phaseUnknown then error('UNKNOWN_PHASE')end;return phaseActive~=false end
    CityProductionDirectives={PROJECT=3,TRAIN=1}
    local row=P.Info('Projects',project);GameInfo.Projects[project]=row;GameInfo.Projects[row.Index]=row;GameInfo.Projects[row.Hash]=row
    entryReads=0;queueEntries={};afterEntryRead=nil
    function queue(items)
     queueEntries={};for i,x in ipairs(items)do queueEntries[i]=x end
     uiQueueSize=#queueEntries;q.target=queueEntries[1]==project and project or (#queueEntries>0 and 'NORMAL'or nil)
    end
    q.GetAt=function(_,i)
     entryReads=entryReads+1
     if entryUnknown then error('QUEUE_UNKNOWN')end
     local x=queueEntries[i+1];local e=x and(x==project and {Directive=3,ProjectType=row.Index}or {Directive=1,UnitType=8})
     if afterEntryRead then local fn=afterEntryRead;afterEntryRead=nil;fn()end
     return e
    end
    local finish=q.FinishProgress
    q.FinishProgress=function(...)
     table.remove(queueEntries,1);uiQueueSize=#queueEntries
     return finish(...)
    end
    function changedQueue()changed();ownEventUI()end
    function selectList()return ui.Before(c,{Type=project},false)end
    function newUI()
     ui.Close();ui=_G[fixtureKind=='Engineering'and 'SPCEngineeringStudyUI'or 'SPCDialogueProjectUI'].New(P,sendUI,function()uiNotifies=uiNotifies+1 end)
     ui.Connect();pumpUI();pumpUI()
    end
    queue({'WORKER'})
    ''')
    return v

@contextmanager
def baseline_sources():
    read=Path.read_text;cache={}
    def source(p,*args,**kwargs):
        if p.is_relative_to(ROOT/'Mod'):
            name=str(p.relative_to(ROOT))
            if name not in cache:cache[name]=subprocess.check_output(['git','show','487d674:'+name],cwd=ROOT,text=True)
            return cache[name]
        return read(p,*args,**kwargs)
    execute=TrackedLua51.execute;load=Context.load
    def historical_execute(vm,text,*args,**kwargs):
        digest=sha256(text.encode()).hexdigest() if isinstance(text,str) else None
        for name,value in cache.items():
            if digest==sha256(value.encode()).hexdigest():SOURCES[digest]='historical/487d674/'+name;break
        return execute(vm,text,*args,**kwargs)
    def historical_load(vm,module):
        p=ROOT/'Mod'/(module if module.endswith('.lua')else module+'.lua')
        if not p.is_relative_to(ROOT/'Mod'):return load(vm,module)
        text=source(p)
        execution_label='historical/487d674/'+str(p.relative_to(ROOT))
        executed(execution_label,sha256(text.encode()).hexdigest())
        try:result=vm.lua.execute(text)
        except Exception:completion(execution_label,False);raise
        completion(execution_label,True);return result
    with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',historical_execute),patch.object(Context,'load',historical_load):yield

class BaselineCounterexamples(unittest.TestCase):
    def test_original_actual_sources_drop_a_confirmed_queued_entry_across_turns(self):
        with baseline_sources():
            for kind in KINDS:
                with self.subTest(kind=kind):
                    v=fixture(kind);v.execute("assert(selectList());queue({'WORKER',project});changedQueue();pumpUI();T.turn(1);queue({project});changedQueue();pumpUI()")
                    self.assertEqual(v.eval('uiBegins'),0)
                    self.assertIsNone(v.eval('pending()'))
    def test_original_actual_sources_drop_multi_to_sole_reentry(self):
        with baseline_sources():
            for kind in KINDS:
                with self.subTest(kind=kind):
                    v=fixture(kind);v.execute("assert(selectList());queue({project,'WORKER'});changedQueue();pumpUI();queue({project});changedQueue();pumpUI()")
                    self.assertEqual(v.eval('uiBegins'),0)
    def test_original_selected_slot_recheck_performs_an_unwanted_native_build(self):
        with baseline_sources():
            v=panel("checks=0;selected=true;nativeBuilds=0;CheckQueueItemSelected=function()checks=checks+1;local x=selected;selected=false;return x end;AdvanceProject=function()if not CheckQueueItemSelected()then nativeBuilds=nativeBuilds+1 end end")
            v.execute("AdvanceProject({}, {Type='PROJECT_NATIVE'})")
            self.assertEqual(v.eval('nativeBuilds'),1)
            self.assertGreater(v.eval('checks'),1)

class QueueRecovery(unittest.TestCase):
    def test_confirmed_appended_entry_waits_across_turn_then_starts_once(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute('''
                assert(selectList());queue({'WORKER',project});changedQueue();pumpUI()
                assert(uiBegins==0 and not pending())
                T.turn(1);queue({project});changedQueue();pumpUI();pumpUI()
                assert(uiBegins==1 and pending()and pending().stage=='ACTIVE')
                local reads=entryReads;idleUI(1000);assert(entryReads==reads and uiBegins==1)
                ''')
    def test_multi_to_sole_needs_new_event_not_idle(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute('''
                assert(selectList());queue({project,'WORKER'});changedQueue();pumpUI()
                assert(uiBegins==0);local reads=entryReads
                queue({project});idleUI(1000);assert(uiBegins==0 and entryReads==reads)
                changedQueue();pumpUI();assert(uiBegins==1 and pending().stage=='ACTIVE')
                ''')
    def test_no_candidate_event_and_unrelated_city_are_inert(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("queue({project});changedQueue();idleUI(1000);assert(uiBegins==0 and entryReads==0)")
    def test_explicit_replacement_can_abandon_unconfirmed_native_insert(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("assert(selectList());assert(not selectList());ui.CancelSelection(c);queue({'WORKER'});changedQueue();pumpUI();assert(selectList());queue({project});changedQueue();pumpUI();assert(uiBegins==1)")
    def test_notification_reentry_cannot_allow_old_native_insert(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("ui.Close();ui=_G[fixtureKind=='Engineering'and 'SPCEngineeringStudyUI'or 'SPCDialogueProjectUI'].New(P,sendUI,function()ui.Close()end);ui.Connect();assert(not ui.Before(c,{Type=project},false));assert(uiBegins==0)")
    def test_async_first_insert_cannot_be_repeated_before_queue_ack(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("assert(selectList());assert(not selectList());assert(not selectList());assert(#queueEntries==1 and uiBegins==0);queue({'WORKER',project});changedQueue();pumpUI();queue({project});changedQueue();pumpUI();assert(uiBegins==1)")
    def test_duplicate_copy_is_refused_but_existing_entry_can_recover(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute('''
                assert(selectList());queue({'WORKER',project});changedQueue();pumpUI()
                assert(not selectList());assert(#queueEntries==2)
                queue({project});changedQueue();pumpUI();assert(uiBegins==1)
                ''')
    def test_multiple_duplicate_entries_do_not_start(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("assert(selectList());queue({project,project});changedQueue();pumpUI();assert(uiBegins==0 and not pending());local n=entryReads;idleUI(1000);assert(entryReads==n)")
    def test_native_unknown_waits_for_a_related_cause(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute('''
                assert(selectList());queue({project});entryUnknown=true;changedQueue();pumpUI()
                assert(uiBegins==0);local n=entryReads;entryUnknown=false;idleUI(1000);assert(entryReads==n and uiBegins==0)
                changedQueue();pumpUI();assert(uiBegins==1)
                ''')
    def test_queue_before_start_is_recovered_on_new_ui_generation(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("queue({'WORKER',project});newUI();assert(uiBegins==0);queue({project});changedQueue();pumpUI();assert(uiBegins==1)")
    def test_existing_selected_slot_does_not_insert_or_create_intent(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("queue({project});assert(not ui.Before(c,{Type=project},true));changedQueue();pumpUI();assert(uiBegins==0 and not pending())")
    def test_reentrant_queue_change_invalidates_old_observation(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute('''
                assert(selectList());queue({project});afterEntryRead=function()queue({'WORKER',project});changedQueue();pumpUI()end
                changedQueue();pumpUI();assert(uiBegins==0)
                queue({project});changedQueue();pumpUI();assert(uiBegins==1)
                ''')

class NativeSelection(unittest.TestCase):
    def test_selected_queue_slot_is_consumed_once_without_native_build(self):
        v=panel('''
        checks=0;selected=true;nativeCalls=0;nativeBuilds=0
        CheckQueueItemSelected=function()checks=checks+1;local r=selected;selected=false;return r end
        AdvanceProject=function()nativeCalls=nativeCalls+1;if not CheckQueueItemSelected()then nativeBuilds=nativeBuilds+1 end end
        ''');v.execute("AdvanceProject({}, {Type='PROJECT_NATIVE'});assert(checks==1 and nativeCalls==0 and nativeBuilds==0)")

CASES = {
'one_award_after_recovery': '''
assert(selectList());queue({'WORKER',project});changedQueue();pumpUI()
T.turn(1);queue({project});changedQueue();pumpUI();pumpUI()
assert(uiBegins==1 and pending()and pending().stage=='ACTIVE')
Events.PlayerTurnDeactivated.Fire(0);T.turn(1);pumpUI();pumpUI()
if fixtureKind=='Engineering'then assert(S.L(c)==1 and S.finishes(c)==1)else assert(finishes==1 and ledger(c).used.ERA_CLASSICAL)end
for i=1,100 do changedQueue();pumpUI()end
if fixtureKind=='Engineering'then assert(S.L(c)==1 and S.finishes(c)==1)else assert(finishes==1)end
''',
'active_multi_same_turn_resume': '''
assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()
local id,start=pending().id,pending().start
queue({project,'WORKER'});changedQueue();pumpUI();assert(pending()and pending().stage=='ACTIVE')
queue({project});changedQueue();pumpUI();pumpUI()
assert(uiBegins==1 and pending().id==id and pending().start==start)
Events.PlayerTurnDeactivated.Fire(0);T.turn(1);pumpUI()
if fixtureKind=='Engineering'then assert(S.L(c)==1 and S.finishes(c)==1)else assert(finishes==1 and ledger(c).used.ERA_CLASSICAL)end
''',
'send_failure_no_idle_retry': '''
assert(selectList());queue({project});failBegin=true;changedQueue();pumpUI()
assert(uiBegins==1 and not pending());failBegin=false;local n=entryReads
idleUI(1000);assert(uiBegins==1 and entryReads==n and not pending())
''',
'closed_window_reopen': '''
assert(selectList());Events.PlayerTurnDeactivated.Fire(0)
queue({project});changedQueue();pumpUI();assert(uiBegins==0 and not pending())
T.turn(1);ui.WarmStart();pumpUI();pumpUI()
assert(uiBegins==1 and pending()and pending().start==Game.GetCurrentGameTurn())
''',
'direct_begin_after_end_rejected': '''
queue({project});Events.PlayerTurnDeactivated.Fire(0)
shared[backendKey].Request(0,{CityID=c:GetID(),StartTurn=Game.GetCurrentGameTurn()})
assert(not pending())
''',
'missed_old_before_begin': '''
assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()
local oldid=pending().id;local t=Game.GetCurrentGameTurn()
Game.GetCurrentGameTurn=function()return t+2 end
queue({project});changedQueue();pumpUI();pumpUI()
assert(uiBegins==2 and pending()and pending().stage=='ACTIVE'and pending().id~=oldid and pending().start==t+2 and not pending().ended)
if fixtureKind=='Engineering'then assert(S.L(c)==0 and S.finishes(c)==0)else assert(finishes==0 and not ledger(c).used.ERA_CLASSICAL)end
''',
'due_old_settled_before_new_begin': '''
assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()
Events.PlayerTurnDeactivated.Fire(0);local t=Game.GetCurrentGameTurn();Game.GetCurrentGameTurn=function()return t+1 end
shared[backendKey].beginClosedTurns[0]=nil
shared[backendKey].Request(0,{CityID=c:GetID(),StartTurn=t+1})
assert(not pending())
if fixtureKind=='Engineering'then assert(S.L(c)==1 and S.finishes(c)==1)else assert(finishes==1 and ledger(c).used.ERA_CLASSICAL)end
''',
'stale_queued_exhausted_after_ui_restart': '''
local roundsToExhaust=fixtureKind=='Engineering'and 2 or 1
for i=1,roundsToExhaust do
 assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()
 assert(pending()and pending().stage=='ACTIVE')
 Events.PlayerTurnDeactivated.Fire(0);T.turn(1);pumpUI();pumpUI()
end
local before=uiBegins;queue({project});newUI();changedQueue();idleUI(1000)
assert(uiBegins==before and not pending())
if fixtureKind=='Engineering'then assert(S.L(c)==2 and S.finishes(c)==2)else assert(finishes==1 and ledger(c).used.ERA_CLASSICAL)end
''',
}

def _case(body):
    def run(self):
        for kind in KINDS:
            with self.subTest(kind=kind):fixture(kind).execute(body)
    return run
class Rounds(unittest.TestCase):pass
for _name,_body in CASES.items():setattr(Rounds,'test_'+_name,_case(_body))

class ScopeAndFailure(unittest.TestCase):
    def test_idle_publishes_do_not_even_rescan_candidate_views(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("""
                assert(selectList());queue({'WORKER',project});changedQueue();pumpUI();pumpUI()
                local b=shared[backendKey];local actual=b.views;viewReads=0
                b.views=setmetatable({},{__index=function(_,k)viewReads=viewReads+1;return actual[k]end})
                local n=entryReads;idleUI(1000);assert(viewReads==0 and entryReads==n and uiBegins==0)
                """)
    def test_unknown_send_does_not_gain_a_retry_from_turn_passage(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("assert(selectList());queue({project});failBegin=true;changedQueue();pumpUI();local n=entryReads;failBegin=false;T.turn(1);ui.WarmStart();idleUI(1000);assert(uiBegins==1 and entryReads==n and not pending())")
    def test_repeated_same_turn_lifecycle_does_not_replenish_window_recovery(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("assert(selectList());queue({project});phaseActive=false;changedQueue();pumpUI();ui.WarmStart();pumpUI();local n=entryReads;for i=1,1000 do ui.WarmStart();pumpUI()end;assert(entryReads==n and uiBegins==0)")
    def test_inactive_and_unknown_native_phase_require_a_new_related_cause(self):
        for kind in KINDS:
            for unknown in (False,True):
                with self.subTest(kind=kind,unknown=unknown):
                    v=fixture(kind);v.globals().phaseUnknown=unknown;v.globals().phaseActive=False
                    v.execute("assert(selectList());queue({project});changedQueue();pumpUI();assert(uiBegins==0 and not pending());local n=entryReads;phaseUnknown=false;phaseActive=true;idleUI(1000);assert(entryReads==n and uiBegins==0);changedQueue();pumpUI();assert(uiBegins==1)")
    def test_unknown_or_inactive_phase_is_also_rejected_by_owner(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("queue({project});phaseActive=false;local n=T.writes();shared[backendKey].Request(0,{CityID=c:GetID(),StartTurn=Game.GetCurrentGameTurn()});phaseUnknown=true;shared[backendKey].Request(0,{CityID=c:GetID(),StartTurn=Game.GetCurrentGameTurn()});assert(not pending()and T.writes()==n)")
    def test_optional_diagnostics_do_not_control_recovery_or_business_writes(self):
        for kind in KINDS:
            results=[]
            for enabled in (False,True):
                v=fixture(kind);v.execute("if SPCCultureDiagnostics then SPCCultureDiagnostics.ENABLED=... end",enabled)
                v.execute("assert(selectList());queue({'WORKER',project});changedQueue();pumpUI();T.turn(1);queue({project});changedQueue();pumpUI();Events.PlayerTurnDeactivated.Fire(0);T.turn(1);pumpUI()")
                results.append((v.eval("T.encode(T.record(c))"),v.eval("T.writes()")))
            self.assertEqual(results[0],results[1])
    def test_restricted_runtime_can_recover_without_raw_access_or_standard_libraries(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("os=nil;io=nil;debug=nil;package=nil;require=nil;rawget=nil;rawset=nil;rawequal=nil;loadfile=nil;dofile=nil;collectgarbage=nil;table.unpack=nil;table.pack=nil;assert(selectList());queue({'WORKER',project});changedQueue();pumpUI();T.turn(1);queue({project});changedQueue();pumpUI();assert(uiBegins==1 and pending().stage=='ACTIVE')")

class SelectionControls(unittest.TestCase):
    def test_native_returns_and_every_adapter_failure_keep_owned_isolation(self):
        from test_refactor_s9a1 import traced
        rows=(('CapitalInvestmentUI','PROJECT_SPC_CAPITAL_INVESTMENT'),('DevelopmentInvestmentUI','PROJECT_SPC_DEVELOPMENT_INVESTMENT'),('CommerceUI','PROJECT_SPC_COMMERCIALIZATION'),('CrewProjectUI','PROJECT_SPC_CREW_250'),('EngineeringStudyUI','PROJECT_SPC_ENGINEERING_STUDY'),('DialogueProjectUI','PROJECT_SPC_ERA_DIALOGUE'),('ClaimProjectUI','PROJECT_SPC_CLAIM_RESEARCH'),('TimedProjectSelection','PROJECT_SPC_OVERFLOW_SINK_TEST'))
        for name,project in rows:
            with self.subTest(adapter=name):
                v=traced();v.execute("fail=...;trace={};local a,b=AdvanceProject({}, {Type='PROJECT_NATIVE'});assert(a=='NATIVE_RESULT'and b.Type=='PROJECT_NATIVE');local n=#trace;AdvanceProject({}, {Type=select(2,...)});for i=n+1,#trace do assert(not trace[i]:find('NATIVE:Advance',1,true))end",name+':Before',project)
    def test_native_selection_exception_stops_before_the_base_operation(self):
        v=panel("CheckQueueItemSelected=function()error('NATIVE_SELECTION_UNKNOWN')end")
        v.execute("assert(not pcall(AdvanceProject,{}, {Type='PROJECT_NATIVE'}));assert(nativeAdvances==0)")
    def test_selected_slot_snapshot_is_shared_even_if_an_adapter_changes_the_function(self):
        from test_refactor_s9a1 import traced
        v=traced();v.execute("checks=0;CheckQueueItemSelected=function()checks=checks+1;return false end;onCall=function(n,m,c,item,selected)if m=='Before'and n~='TimedProjectSelection'then assert(selected==false)end;if n=='CapitalInvestmentUI'and m=='Before'then CheckQueueItemSelected=function()error('SHOULD_NOT_BE_READ_BY_LATER_ADAPTERS')end end end;local a=AdvanceProject({}, {Type='PROJECT_NATIVE'});assert(a=='NATIVE_RESULT'and checks==1)")

class Boundaries(unittest.TestCase):
    def test_confirmed_interruption_wins_over_due_completion(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("""
                assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()
                Events.PlayerTurnDeactivated.Fire(0)
                local fire=Events.PlayerTurnActivated.Fire;Events.PlayerTurnActivated.Fire=function()end;T.turn(1);Events.PlayerTurnActivated.Fire=fire
                queue({'WORKER'});Events.CityProductionChanged.Fire(0,c:GetID())
                queue({project});Events.CityProductionChanged.Fire(0,c:GetID())
                shared[backendKey].Request(0,{CityID=c:GetID(),StartTurn=Game.GetCurrentGameTurn()})
                assert(pending()and pending().stage=='ACTIVE'and pending().start==Game.GetCurrentGameTurn()and not pending().ended)
                if fixtureKind=='Engineering'then assert(S.L(c)==0)else assert(next(ledger(c).used)==nil)end
                """)
    def test_owner_rechecks_window_after_queue_getter_reentry(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("""
                queue({project});local get=q.GetSize;local once=true
                q.GetSize=function(...)local n=get(...);if once then once=false;Events.PlayerTurnDeactivated.Fire(0)end;return n end
                shared[backendKey].Request(0,{CityID=c:GetID(),StartTurn=Game.GetCurrentGameTurn()})
                assert(not pending());if fixtureKind=='Engineering'then assert(S.L(c)==0)else assert(next(ledger(c).used)==nil)end
                """)
    def test_due_settlement_cannot_chain_a_new_round_from_stale_native_getter(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("""
                assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()
                Events.PlayerTurnDeactivated.Fire(0);local t=Game.GetCurrentGameTurn();Game.GetCurrentGameTurn=function()return t+1 end
                shared[backendKey].beginClosedTurns[0]=nil
                local finish=q.FinishProgress;q.FinishProgress=function(...)local value=finish(...);q.target=project;uiQueueSize=1;return value end
                shared[backendKey].Request(0,{CityID=c:GetID(),StartTurn=t+1})
                assert(not pending());if fixtureKind=='Engineering'then assert(S.L(c)==1)else assert(finishes==1)end
                """)
    def test_initial_sync_completion_cannot_seed_a_new_round_from_old_queue(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("""
                assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()
                Events.PlayerTurnDeactivated.Fire(0);local t=Game.GetCurrentGameTurn();Game.GetCurrentGameTurn=function()return t+1 end
                shared[backendKey].beginClosedTurns[0]=nil
                local before=uiBegins;local finish=q.FinishProgress;q.FinishProgress=function(...)local result=finish(...);queue({project});return result end
                newUI();changedQueue();idleUI(1000)
                assert(uiBegins==before and not pending());if fixtureKind=='Engineering'then assert(S.L(c)==1)else assert(finishes==1)end
                """)
    def test_initial_after_same_turn_completion_also_rejects_ambiguous_old_queue(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("""
                assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()
                local before=uiBegins;local finish=q.FinishProgress;q.FinishProgress=function(...)local result=finish(...);queue({project});return result end
                Events.PlayerTurnDeactivated.Fire(0);T.turn(1)
                newUI();changedQueue();idleUI(1000)
                assert(uiBegins==before and not pending());if fixtureKind=='Engineering'then assert(S.L(c)==1)else assert(finishes==1)end
                """)
    def test_completed_entry_cannot_automatically_restart_on_a_stale_queue_read(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("""
                assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()
                local before=uiBegins
                local finish=q.FinishProgress;q.FinishProgress=function(...)local value=finish(...);queue({project});return value end
                Events.PlayerTurnDeactivated.Fire(0);T.turn(1);changedQueue();pumpUI();idleUI(1000)
                assert(uiBegins==before and not pending());if fixtureKind=='Engineering'then assert(S.L(c)==1)else assert(finishes==1)end
                """)
    def test_terminal_hints_have_a_separate_fixed_bound(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                v=fixture(kind);v.execute("""
                SPCTimedProjectQueueIntent.LIMIT=2
                for i=1,6 do
                 local fake={GetOwner=function()return 0 end,GetID=function()return 1000+i end,GetX=function()return i end,GetY=function()return 0 end,GetBuildQueue=function()return q end}
                 shared[backendKey].views['0:'..(1000+i)]={stage='INELIGIBLE',reason='NOT_ELIGIBLE'}
                 assert(not ui.Before(fake,{Type=project},false))
                end
                local f=ExposedMembers[fixtureKind=='Engineering'and 'SPC_EngineeringStudyQueueStatus'or 'SPC_DialogueQueueStatus']
                assert(f(0,1001)==nil and f(0,1006)~=nil)
                """)

if __name__=='__main__':unittest.main()

