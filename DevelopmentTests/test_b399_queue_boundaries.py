"""B399 real queue owners plus removable boundary observers; native doubles only."""
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch
from lupa.lua51 import LuaRuntime
from test_b398_queue_recovery import fixture, KINDS
from test_expedition_trace_collector import collector
from test_expedition_spy_task import gate
import test_expedition_gate as gate_fixture
import test_expedition_training_diagnostics as diagnostic_fixture

from refactor_harness import ROOT
OBS=(ROOT/'Mod/PlaytestBoundaryDiagnostics.lua').read_text()
REORDER="""
queue({project,'WORKER'});changedQueue();pumpUI()
queue({'WORKER',project});changedQueue();pumpUI()
queue({project,'WORKER'});changedQueue();pumpUI()
queue({project});changedQueue();pumpUI();pumpUI()
"""
HEADER=r'''
turn=10;nativeReads=0;clockReads=0;records={};treasuryBalance=100;goldYield=20;border=false
function event()
 local listeners={};local e={}
 function e.Add(f)listeners[#listeners+1]=f end
 function e.Remove(f)for i=#listeners,1,-1 do if listeners[i]==f then table.remove(listeners,i)end end end
 function e.Fire(a,b,c,d)local copy={};for i,f in ipairs(listeners)do copy[i]=f end;for _,f in ipairs(copy)do f(a,b,c,d)end end
 function e.Size()return #listeners end
 return e
end
Events={};GameEvents={PlayerTurnStarted=event()}
for _,n in ipairs({'PlayerTurnDeactivated','PlayerTurnActivated','LocalPlayerTurnBegin','LocalPlayerTurnEnd','LoadScreenClose','TreasuryChanged','PlayerTreasuryChanged','PlayerGoldChanged','GameCoreEventPublishComplete','UnitMoveComplete','UnitTeleported','UnitActivityChanged','DiplomacyRelationshipChanged','UnitRemovedFromMap'})do Events[n]=event()end
Game={GetCurrentGameTurn=function()clockReads=clockReads+1;return turn end,GetLocalPlayer=function()nativeReads=nativeReads+1;return 0 end}
P={IsTestPlayer=function(pid)return pid==0 end}
local function getter(fn)return function(...)nativeReads=nativeReads+1;if readError then error('PRIVATE-NATIVE-DETAIL')end;return fn(...)end end
local treasury={GetGoldBalance=getter(function()return treasuryBalance end),GetGoldYield=getter(function()return goldYield end),GetTotalMaintenance=getter(function()return 4 end)}
for _,n in ipairs({'GetBuildingMaintenance','GetDistrictMaintenance','GetUnitMaintenance','GetWMDMaintenance'})do treasury[n]=getter(function()return 1.25 end)end
u={x=8,y=9};u.GetOwner=getter(function()return 0 end);u.GetID=getter(function()return 7 end);u.GetX=getter(function()return u.x end);u.GetY=getter(function()return u.y end);u.GetType=getter(function()return 44 end);u.GetSpyOperation=getter(function()return -1 end);u.GetMovesRemaining=getter(function()return 0 end)
UnitManager={GetActivityType=getter(function()return 0 end)}
local units={FindID=getter(function(_,id)if id==7 then return u end end),Members=function()error('NO_UNIT_ENUMERATION')end}
local diplomacy={HasOpenBordersFrom=getter(function()return border end)}
Players={[0]={GetTreasury=getter(function()return treasury end),GetUnits=getter(function()return units end),GetDiplomacy=getter(function()return diplomacy end),IsTurnActive=getter(function()return false end)}}
shared={NetworkBridge={players={[0]={revalidation='VERIFIED',availability='AVAILABLE'}}}}
SPCExpeditionTrainingDiagnostics={ENABLED=true,New=function()
 return {id='TEST',Record=function(stage,data)
  if sinkError then error('PRIVATE-SINK-DETAIL')end
  local row={stage=stage};for k,v in pairs(data)do row[k]=v end;records[#records+1]=row
  if reentry then Events.TreasuryChanged.Fire(0)end
 end}
end}
function watch()SPCPlaytestBoundaryDiagnostics.Observe('EXPEDITION_TURN',function()return {owner=0,eventUnit=7,phase='ARRIVED',x=8,y=9,targetOwner=4,targetCity=12}end)end
function count(stage)local n=0;for _,v in ipairs(records)do if v.stage==stage then n=n+1 end end;return n end
function last(stage)for i=#records,1,-1 do if records[i].stage==stage then return records[i]end end end
'''

def observer(start=True):
    l=LuaRuntime(unpack_returned_tuples=True);l.execute(HEADER);l.execute(OBS)
    if start:l.execute('api=SPCPlaytestBoundaryDiagnostics.Start(P,shared)')
    return l

class QueueCancellation(unittest.TestCase):
    def test_already_started_reorder_then_remove_restarts_once_for_both_owners(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                l=fixture(kind);l.execute('assert(selectList());queue({project});changedQueue();pumpUI();pumpUI();oldID=pending().id')
                l.execute(REORDER)
                l.execute("assert(uiBegins==2 and pending()and pending().id>oldID and pending().stage=='ACTIVE');local n=entryReads;idleUI(1000);assert(uiBegins==2 and entryReads==n)")
    def test_same_turn_multiple_cancel_cycles_have_distinct_authoritative_ids(self):
        for kind in KINDS:
            l=fixture(kind);l.execute('assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()')
            for _ in range(3):l.execute('oldID=pending().id');l.execute(REORDER);l.execute("assert(pending().id>oldID and pending().stage=='ACTIVE')")
            l.execute("assert(uiBegins==4);local tokens={};for _,packet in ipairs(uiPackets)do if packet.Action==beginAction then assert(not tokens[packet.Token],'DUPLICATE_NEW_ROUND_PACKET');tokens[packet.Token]=true end end;Events.PlayerTurnDeactivated.Fire(0);T.turn(1);pumpUI();pumpUI();if fixtureKind=='Engineering'then assert(S.L(c)==1 and S.finishes(c)==1)else assert(finishes==1)end")
    def test_unknown_send_is_not_retried_by_queue_roundtrip_without_cancellation(self):
        for kind in KINDS:
            l=fixture(kind);l.execute('assert(selectList());queue({project});failBegin=true;changedQueue();pumpUI();assert(uiBegins==1 and not pending());failBegin=false')
            l.execute(REORDER);l.execute('idleUI(1000);assert(uiBegins==1 and not pending())')
    def test_unconfirmed_cancellation_cannot_grant_new_admission(self):
        for kind in KINDS:
            l=fixture(kind);l.execute("assert(selectList());queue({project});changedQueue();pumpUI();pumpUI();oldID=pending().id;local method=fixtureKind=='Engineering'and 'WriteEngineering'or 'WriteDialogue';oldWrite=shared.CityProgressionStore[method];shared.CityProgressionStore[method]=function()error('UNCONFIRMED_CANCEL')end")
            l.execute("queue({'WORKER',project});changedQueue();pumpUI();queue({project});changedQueue();pumpUI();pumpUI();assert(uiBegins==1 and pending().id==oldID)")
            l.execute("shared.CityProgressionStore[fixtureKind=='Engineering'and 'WriteEngineering'or 'WriteDialogue']=oldWrite;changedQueue();pumpUI();pumpUI();assert(uiBegins==2 and pending().id>oldID)")
    def test_completed_receipt_is_not_projected_as_cancellation(self):
        for kind in KINDS:
            l=fixture(kind);l.execute("assert(selectList());queue({project});changedQueue();pumpUI();pumpUI();Events.PlayerTurnDeactivated.Fire(0);T.turn(1);pumpUI();pumpUI();local v=shared[backendKey].views['0:'..c:GetID()];assert(v.completedID>0 and v.cancelledID==0)")
    def test_optional_probe_states_leave_actual_owner_records_and_rewards_equal(self):
        for kind in KINDS:
            results=[]
            for mode in ('absent','off','on','throw'):
                l=fixture(kind)
                if mode!='absent':
                    l.execute(OBS)
                    if mode=='off':l.execute('SPCPlaytestBoundaryDiagnostics.ENABLED=false')
                    l.execute('SPCPlaytestBoundaryDiagnostics.Start(P,shared)')
                    if mode=='throw':l.execute("SPCPlaytestBoundaryDiagnostics.Observe=function()error('OBSERVER_FAILURE')end")
                l.execute('assert(selectList());queue({project});changedQueue();pumpUI();pumpUI()');l.execute(REORDER)
                l.execute('Events.PlayerTurnDeactivated.Fire(0);T.turn(1);pumpUI();pumpUI()')
                results.append(l.eval('snapshot()'))
            self.assertEqual(len(set(results)),1,kind)

class BoundaryObserver(unittest.TestCase):
    def test_exact_balance_change_and_native_false_zero_are_retained(self):
        l=observer();l.execute("treasuryBalance=152;Events.TreasuryChanged.Fire(0);local v=last('PLAYTEST_TREASURY');assert(v.actualDelta==52 and v.ownerTurnActive==false and v.buildingMaintenance==1.25);watch();local p=last('PLAYTEST_POSITION');assert(p.reason=='BORDER_CLOSED'and p.actualX==8 and p.spyOperation==-1 and p.movesRemaining==0 and p.nativeActivity==0)")
    def test_disabled_start_has_no_hooks_records_or_native_reads(self):
        l=observer(False);l.execute("SPCPlaytestBoundaryDiagnostics.ENABLED=false;assert(not SPCPlaytestBoundaryDiagnostics.Start(P,shared));watch();Events.PlayerTurnActivated.Fire(0);assert(nativeReads==0 and clockReads==0 and #records==0 and Events.TreasuryChanged.Size()==0)")
    def test_idle_publish_and_foreign_events_do_no_native_work(self):
        l=observer();l.execute("watch();local n,t=nativeReads,clockReads;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire();Events.TreasuryChanged.Fire(9);Events.UnitMoveComplete.Fire(9,7);Events.UnitMoveComplete.Fire(0,99);Events.DiplomacyRelationshipChanged.Fire(8,9)end;assert(nativeReads==n and clockReads==t)")
    def test_identity_admission_is_cached_and_failed_local_lookup_is_bounded(self):
        l=observer(False);l.execute("identityReads=0;P.IsTestPlayer=function(pid)identityReads=identityReads+1;return pid==0 end;api=SPCPlaytestBoundaryDiagnostics.Start(P,shared);for i=1,1000 do Events.TreasuryChanged.Fire(9);Events.PlayerTurnActivated.Fire(0)end;assert(identityReads==1)")
        for unavailable in (False,True):
            l=observer(False)
            l.execute("identityReads=0;P.IsTestPlayer=function(pid)identityReads=identityReads+1;return false end")
            if unavailable:l.execute("Game.GetLocalPlayer=function()nativeReads=nativeReads+1;return -1 end")
            l.execute("api=SPCPlaytestBoundaryDiagnostics.Start(P,shared);for i=1,1000 do Events.TreasuryChanged.Fire(9);Events.PlayerTurnActivated.Fire(0);Events.LocalPlayerTurnBegin.Fire()end;assert(nativeReads==4 and identityReads<=4 and clockReads==0 and count('PLAYTEST_TREASURY')==0 and Events.TreasuryChanged.Size()==0)")
    def test_local_begin_grants_only_one_publish_sample(self):
        l=observer();l.execute("Events.LocalPlayerTurnBegin.Fire();Events.GameCoreEventPublishComplete.Fire();local n,t=nativeReads,clockReads;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(nativeReads==n and clockReads==t)")
    def test_treasury_changes_have_per_turn_and_total_caps(self):
        l=observer();l.execute("for i=1,1000 do treasuryBalance=i;Events.TreasuryChanged.Fire(0)end;assert(count('PLAYTEST_TREASURY')==9 and clockReads<20);assert(last('PLAYTEST_PROBE_STATUS').point=='CHANGE_LIMIT');SPCPlaytestBoundaryDiagnostics.TREASURY_LIMIT=10;Events.PlayerTurnActivated.Fire(0);local n=nativeReads;for i=1,1000 do Events.PlayerTurnActivated.Fire(0)end;assert(nativeReads==n and count('PLAYTEST_TREASURY')==10 and last('PLAYTEST_PROBE_STATUS').reason=='PHASE_LIMIT')")
    def test_unit_sampling_has_separate_bound_and_reports_truncation(self):
        l=observer();l.execute("SPCPlaytestBoundaryDiagnostics.POSITION_LIMIT=2;watch();u.x=9;Events.UnitMoveComplete.Fire(0,7);local n,t=nativeReads,clockReads;for i=1,1000 do Events.UnitMoveComplete.Fire(0,7);watch()end;assert(nativeReads==n and clockReads==t and count('PLAYTEST_POSITION')==2 and last('PLAYTEST_PROBE_STATUS').eventTruncated==true)")
    def test_window_expiry_unregisters_and_releases_all_observations(self):
        l=observer();l.execute("watch();turn=16;Events.PlayerTurnActivated.Fire(0);local n,t=nativeReads,clockReads;for i=1,100 do Events.TreasuryChanged.Fire(0);Events.UnitMoveComplete.Fire(0,7);watch()end;assert(nativeReads==n and clockReads==t and Events.PlayerTurnActivated.Size()==0 and last('PLAYTEST_PROBE_STATUS').reason=='WINDOW_END')")
    def test_lifecycle_rearms_change_budget_once_and_expiry_works_after_sample_cap(self):
        l=observer();l.execute("for i=1,20 do Events.TreasuryChanged.Fire(0)end;Events.PlayerTurnDeactivated.Fire(0);for i=1,20 do Events.TreasuryChanged.Fire(0)end;assert(count('PLAYTEST_TREASURY')==18);Events.PlayerTurnDeactivated.Fire(0);Events.TreasuryChanged.Fire(0);assert(count('PLAYTEST_TREASURY')==19);SPCPlaytestBoundaryDiagnostics.TREASURY_LIMIT=19;turn=16;Events.PlayerTurnActivated.Fire(0);assert(Events.TreasuryChanged.Size()==0)")
    def test_explicit_stop_and_runtime_disable_leave_foreign_listeners_untouched(self):
        for disable in (False,True):
            l=observer();l.execute('other=0;Events.PlayerTurnActivated.Add(function()other=other+1 end);watch()')
            l.execute('SPCPlaytestBoundaryDiagnostics.ENABLED=false;Events.PlayerTurnActivated.Fire(0)' if disable else 'SPCPlaytestBoundaryDiagnostics.Stop()')
            l.execute("local n=nativeReads;Events.PlayerTurnActivated.Fire(0);assert(nativeReads==n and other>=1 and Events.PlayerTurnActivated.Size()==1)")
    def test_missing_throwing_getters_and_sinks_do_not_escape(self):
        l=observer();l.execute("readError=true;Events.TreasuryChanged.Fire(0);assert(last('PLAYTEST_TREASURY').goldBalance=='READ_ERROR');watch();assert(last('PLAYTEST_POSITION').readStatus=='UNAVAILABLE');readError=false;sinkError=true;Events.TreasuryChanged.Fire(0);watch();SPCPlaytestBoundaryDiagnostics.Stop()")
    def test_reentrant_sink_does_not_trigger_recursive_native_read(self):
        l=observer();l.execute("reentry=true;local countBefore=count('PLAYTEST_TREASURY');Events.TreasuryChanged.Fire(0);assert(count('PLAYTEST_TREASURY')==countBefore+1)")
    def test_reinitialization_and_transport_absence_are_safe(self):
        l=observer();l.execute("SPCPlaytestBoundaryDiagnostics.Start(P,shared);assert(Events.TreasuryChanged.Size()==1);SPCPlaytestBoundaryDiagnostics.Stop();SPCExpeditionTrainingDiagnostics=nil;assert(not SPCPlaytestBoundaryDiagnostics.Start(P,shared));assert(Events.TreasuryChanged.Size()==0)")
    def test_phase_clock_has_hard_budget_and_noop_count_hook_is_not_business_authority(self):
        l=observer();l.execute("SPCPlaytestBoundaryDiagnostics.PHASE_LIMIT=5;P.Count=function()error('COUNTER_FAILED')end;for i=1,100 do Events.PlayerTurnActivated.Fire(0)end;local n,t=nativeReads,clockReads;Events.LocalPlayerTurnBegin.Fire();assert(nativeReads==n and clockReads==t and last('PLAYTEST_PROBE_STATUS').reason=='PHASE_LIMIT'and last('PLAYTEST_PROBE_STATUS').eventTruncated)")
    def test_optional_event_without_safe_remove_is_not_registered(self):
        l=observer(False);l.execute("Events.TreasuryChanged.Remove=nil;api=SPCPlaytestBoundaryDiagnostics.Start(P,shared);assert(Events.TreasuryChanged.Size()==0);SPCPlaytestBoundaryDiagnostics.Stop();assert(Events.PlayerTurnActivated.Size()==0)")
    def test_unit_removal_retires_scalar_watch(self):
        l=observer();l.execute("watch();Events.UnitRemovedFromMap.Fire(0,7);local n=nativeReads;Events.UnitMoveComplete.Fire(0,7);Events.DiplomacyRelationshipChanged.Fire(0,4);assert(nativeReads==n)")
    def test_arbitrary_native_strings_are_not_copied_into_records(self):
        l=observer();l.execute("local original=Players[0].GetTreasury;Players[0].GetTreasury=function()return{GetGoldBalance=function()return 'PRIVATE_DETAIL'end}end;Events.TreasuryChanged.Fire(0);assert(last('PLAYTEST_TREASURY').goldBalance=='INVALID_TYPE');Players[0].GetTreasury=original;UnitManager.GetActivityType=function()return 'PRIVATE_DETAIL'end;watch();assert(last('PLAYTEST_POSITION').nativeActivity=='UNAVAILABLE')")
    def test_restricted_lua_environment_and_no_native_writes_or_enumeration(self):
        l=observer(False);l.execute("rawget=nil;rawset=nil;rawequal=nil;os=nil;io=nil;debug=nil;package=nil;require=nil;loadfile=nil;dofile=nil;collectgarbage=nil;api=SPCPlaytestBoundaryDiagnostics.Start(P,shared);watch();Events.PlayerTurnDeactivated.Fire(0);treasuryBalance=152;Events.TreasuryChanged.Fire(0);SPCPlaytestBoundaryDiagnostics.Stop()")
    def test_invalid_builder_is_contained_without_overwriting_active_watch(self):
        l=observer();l.execute("watch();SPCPlaytestBoundaryDiagnostics.Observe('EXPEDITION_TURN',function()error('PRIVATE_DETAIL')end);Events.UnitMoveComplete.Fire(0,7);assert(last('PLAYTEST_POSITION').actualX==8)")

class OptionalStartup(unittest.TestCase):
    def test_actual_optional_startup_contains_absent_and_throwing_modules(self):
        line=next(x for x in (ROOT/'Mod/Gameplay.lua').read_text().splitlines() if x.startswith("pcall(function()include('PlaytestBoundaryDiagnostics')"))
        for body in ("include=function()error('MISSING_OPTIONAL_FILE')end","include=function()end;SPCPlaytestBoundaryDiagnostics={Start=function()error('BAD_OBSERVER')end}"):
            l=LuaRuntime();l.execute('sentinel=17;'+body);l.execute(line);self.assertEqual(l.eval('sentinel'),17)

class GateIsolation(unittest.TestCase):
    def test_real_gate_displacement_guard_is_identical_with_probe_on_off_absent_throwing(self):
        outcomes=[]
        for mode in ('absent','off','on','throw'):
            with patch.object(gate_fixture,'LuaRuntime',LuaRuntime):l=gate()
            l.execute("req('CREATE','a');nativeDispatch('b');arrival(41,true,false);Game.GetLocalPlayer=function()return 2 end")
            if mode!='absent':
                l.execute(OBS)
                if mode=='off':l.execute('SPCPlaytestBoundaryDiagnostics.ENABLED=false')
                if mode=='throw':l.execute("SPCPlaytestBoundaryDiagnostics.Observe=function()error('OBSERVER_FAILED')end")
                if mode=='on':
                    l.execute("SPCExpeditionTrainingDiagnostics={ENABLED=true,New=function()return{id='TEST',Record=function(stage,data)if stage=='PLAYTEST_POSITION'then positionRow=data end end}end};local originalTurn=ownTurn;Events.PlayerTurnActivated={Add=function()end,Remove=function()end};SPCPlaytestBoundaryDiagnostics.Start(P,shared);ownTurn=originalTurn")
            l.execute("units[41].x=16;currentTurn=84;ownTurn(2);result=req('READ','moved')")
            outcomes.append(tuple(l.eval(x)for x in ['result.phase','result.stop','properties','insightWrites','placeCalls','finishCalls']))
            if mode=='on':l.execute("assert(positionRow and positionRow.x==15 and positionRow.actualX==16)")
        self.assertEqual(len(set(outcomes)),1)
        self.assertEqual(outcomes[0][0:2],('HELD','TEAM_DISPLACED_STOP'))

class Transport(unittest.TestCase):
    def test_real_b205_transport_keeps_new_scalar_precision_and_reader_protocol(self):
        with patch.object(diagnostic_fixture,'LuaRuntime',LuaRuntime):l=diagnostic_fixture.fixture()
        l.execute("a.Record('PLAYTEST_TREASURY',{owner=2,point='STARTED',goldBalance=152.125,actualDelta=52,buildingMaintenance=1.23456789012345,districtMaintenance=0,unitMaintenance=-1,wmdMaintenance=0})")
        line=l.eval('last().line')
        self.assertEqual(collector.reader.training_line(line),line)
        self.assertIn('buildingMaintenance=1.23456789012345',line)
        self.assertIn('districtMaintenance=0',line)
        l.execute('unchanged()')

class CollectorSummary(unittest.TestCase):
    def test_new_records_are_retained_and_summary_truncation_is_explicit(self):
        with tempfile.TemporaryDirectory()as d, patch.object(collector,'ROOT',Path(d).resolve()):
            s=collector.Session(Path(d).resolve()/'local')
            try:
                for i in range(1,41):s.add('[SPC][B205][TRAIN] seq=%d stage=PLAYTEST_TREASURY context=TEST turn=61 owner=0 point=STARTED goldBalance=152 actualDelta=52 goldYield=20 maintenance=4 buildingMaintenance=1.25'%i,'snap')
                s.add('[SPC][B205][TRAIN] seq=41 stage=PLAYTEST_PROBE_STATUS context=TEST turn=61 point=CHANGE_LIMIT eventTruncated=true','live')
                text=s.summary('TEST')
                self.assertIn('first32 shown',text);self.assertIn('PLAYTEST_BOUNDARY_TRUNCATED',text)
                self.assertIn('seq=40', (s.directory/'records.log').read_text())
                self.assertEqual(len(s.boundary_rows),32)
            finally:s.close()

if __name__=='__main__':unittest.main()
