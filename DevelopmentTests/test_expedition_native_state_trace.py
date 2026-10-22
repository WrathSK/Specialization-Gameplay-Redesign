"""B223 actual diagnostic/Travel/Gate/UI code; native admission remains unknown.
Local fixtures model observations, not the engine's post-sleep travel behavior.
"""
from pathlib import Path
import unittest
from test_expedition_training_diagnostics import fixture as diagnostic
from test_expedition_spy_task import gate
from test_expedition_spy_activity import ready
from test_expedition_spy_activity_integration import integrated
from test_expedition_activity_trace import fixture as activity
from test_expedition_task_rejection import PACKET
from test_expedition_missions import MISSION_FIXTURE
from test_expedition_trace_reader import reader

R = Path(__file__).resolve().parents[1]
SOURCE = R / 'Mod/ExpeditionTrainingDiagnostics.lua'
READERS = """
 function equip(u,moves,activity)
  u.moves=moves;u.activity=activity
  function u:GetMovesRemaining()return self.moves end
  function u:GetMaxMoves()return 4 end
  function u:IsReadyToMove()return true end
  function u:GetSpyOperationEndTurn()return -1 end
  return u
 end
 UnitManager.GetActivityType=function(u)return u.activity or 0 end
 Players[2].IsTurnActive=function()return true end
 Game.GetLocalPlayer=function()return 2 end
 UI=UI or {};UI.GetInterfaceMode=function()return 11 end
 function records(stage,result)
  local out={};for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do
   if e.stage==stage and (not result or e.requestResult==result)then out[#out+1]=e end
  end;return out
 end
 function latest(stage,result)local r=records(stage,result);return r[#r]end
"""


def enable(l, restart=True):
    l.execute('print=function()end')
    l.execute(SOURCE.read_text())
    l.execute(READERS)
    if restart:
        l.execute('SPCExpeditionSpyGate.Start(P,shared)')
    return l


def combined():
    l = integrated()
    l.execute('activityShutdown()')
    enable(l)
    l.execute('equip(units[41],0,0);activityInit();drainRefreshFrames()')
    return l


class NativeSample(unittest.TestCase):
    def test_zero_false_negative_and_stage_survive(self):
        l=diagnostic();l.execute("""
         u={GetOwner=function()return 2 end,GetID=function()return 41 end,
          GetX=function()return -1 end,GetY=function()return 8 end,
          GetMovesRemaining=function()return 0 end,GetMaxMoves=function()return 4 end,
          IsReadyToMove=function()return false end,GetSpyOperation=function()return -1 end,
          GetSpyOperationEndTurn=function()return -1 end}
         Players={[2]={IsTurnActive=function()return false end}}
         UnitManager={GetActivityType=function()return 0 end}
         Game.GetLocalPlayer=function()return 2 end;UI.GetInterfaceMode=function()return 11 end
         a.Unit('DISPATCH_BEFORE',u,{requestAccepted=false})
         local e=last();assert(e.nativeActivity=='0' and e.movesRemaining=='0' and e.maxMoves=='4')
         assert(e.nativeReady=='false' and e.ownerTurnActive=='false' and e.actualX=='-1' and e.spyOperation=='-1')
         assert(e.requestAccepted=='false' and e.interfaceMode=='11');unchanged()
        """)

    def test_missing_throwing_nil_and_invalid_readers_are_explicit_not_values(self):
        l=diagnostic();l.execute("""
         u={GetOwner=function()return 2 end,GetID=function()error('secret-path-token')end,
          GetX=function()return nil end,GetY=function()return {} end,
          GetMovesRemaining=function()return 0/0 end,GetMaxMoves=function()return math.huge end,
          GetSpyOperation=function()return 'secret-path-token' end}
         a.Unit('BAD_READ',u);local e=last()
         assert(e.nativeUnit=='READ_ERROR' and e.actualX=='NIL' and e.actualY=='INVALID_TYPE')
         assert(e.movesRemaining=='INVALID_TYPE' and e.maxMoves=='INVALID_TYPE' and e.spyOperation=='INVALID_TYPE')
         assert(e.nativeReady=='UNAVAILABLE' and not e.line:find('secret',1,true));unchanged()
        """)

    def test_disabled_or_exhausted_producer_stops_native_reads(self):
        l=diagnostic();l.execute("""
         reads=0;u={GetOwner=function()reads=reads+1;return 2 end}
         for i=1,200 do a.Unit('REPEAT',u,{eventUnit=i})end
         assert(reads==95 and trace().sequence==96 and #trace().entries==64 and trace().suppressed==105)
         M.ENABLED=false;local off=M.New(P,'OFF');off.Unit('OFF',u);assert(reads==95);unchanged()
        """)

    def test_reentrant_trace_notification_does_not_resample(self):
        l=diagnostic();l.execute("""
         reads=0;u={GetOwner=function()reads=reads+1;return 2 end}
         LuaEvents.SPC_B205TrainingTrace.Add(function()a.Unit('NESTED',u)end)
         a.Unit('OUTER',u);assert(reads==1 and #trace().entries==2);unchanged()
        """)


class TravelAndArrival(unittest.TestCase):
    def test_manual_sleep_dispatch_and_engine_return_sample_without_wake(self):
        l=enable(gate(ui=True));l.execute("""
         req('CREATE','create');equip(units[40],4,1)
         local r=nativeDispatch('travel');assert(r.nativePermit)
         local original=UnitManager.RequestOperation
         UnitManager.RequestOperation=function(u,op,p)local result=original(u,op,p);u.x=-1;u.y=-1;u.moves=0;u.activity=3;return result end
         local ok=reader.SubmitTravel(2,40,target,r.nativePermit);assert(ok)
         local pre=latest('DISPATCH_BEFORE');local post=latest('DISPATCH_RETURNED')
         assert(pre.nativeActivity=='1' and pre.movesRemaining=='4' and pre.nativeReady=='true')
         assert(post.nativeActivity=='3' and post.movesRemaining=='0' and post.actualX=='-1')
         assert(post.submitStatus=='CALL_RETURNED' and nativeCalls==1 and nameCalls==0 and properties==0)
         assert(not reader.SubmitTravel(2,40,target,r.nativePermit) and nativeCalls==1)
        """)

    def test_direct_arrival_keeps_moves_and_binding_and_is_recorded_once(self):
        l=enable(gate());l.execute("""
         req('CREATE','create');local source=req('READ','before');nativeDispatch('travel')
         local original=unit;unit=function(...)return equip(original(...),2,0)end
         local r=arrival(41,true,false)
         local pre=latest('ARRIVAL_BEFORE');local post=latest('ARRIVAL_CONFIRMED')
         assert(pre.phase=='TRAVELLING' and post.phase=='ARRIVED' and post.arrivalRoute=='DIRECT')
         assert(pre.movesRemaining=='2' and post.movesRemaining=='2' and post.nativeUnit=='41')
         assert(post.storeStatus=='CONFIRMED' and post.savedPhase=='ARRIVED' and post.savedMatches=='true')
         assert(r.teamKey==source.teamKey and r.sourceCity==source.sourceCity and r.bound and r.count==1)
         for i=1,10 do req('READ','duplicate'..i);ownTurn(2)end
         assert(#records('ARRIVAL_CONFIRMED')==1 and placeCalls==0 and finishCalls==0 and properties==0)
        """)

    def test_entry_relocation_exposes_existing_finish_moves_without_changing_it(self):
        l=enable(gate());l.execute(MISSION_FIXTURE);l.execute("""
         entryCity={id=11,owner=3,x=18,y=8}
         for k,v in pairs(targetCity)do if type(v)=='function'then entryCity[k]=v end end
         targetCities.Members=function()local list={targetCity,entryCity};local i=0;return function()i=i+1;if list[i]then return i,list[i]end end end
         PlayersVisibility={[2]={IsRevealed=function(self,x,y)return not (x==15 and y==8)end}}
         req('CREATE','a');nativeDispatch('b',{EntryX=18,EntryY=8})
         local old=units[40];local u=equip(unit(41,100,2,18,8),4,0);u.name=old.name;units[40]=nil;units[41]=u
         currentTurn=83;ownTurn(2);local r=req('READ','arr')
         local pre=latest('ARRIVAL_BEFORE');local post=latest('ARRIVAL_CONFIRMED')
         assert(r.phase=='ARRIVED' and post.arrivalRoute=='ENTRY_RELOCATE')
         assert(pre.movesRemaining=='4' and post.movesRemaining=='0' and pre.actualX=='18' and post.actualX=='15')
         assert(placeCalls==1 and finishCalls==1 and post.savedMatches=='true' and properties==0)
        """)

    def test_arrival_write_failure_is_not_confirmed(self):
        l=enable(gate());l.execute("""
         req('CREATE','create');nativeDispatch('travel');storeNoop=true
         local r=arrival(41,true,false)
         assert(r.phase=='HELD' and #records('ARRIVAL_BEFORE')==1 and #records('ARRIVAL_CONFIRMED')==0)
         assert(properties==0 and insightWrites==0)
        """)

    def test_trace_failure_does_not_change_travel_submission(self):
        l=enable(gate(ui=True));l.execute("""
         req('CREATE','create');local r=nativeDispatch('travel')
         SPCExpeditionTrainingDiagnostics.New=function()error('DIAGNOSTIC_UNAVAILABLE')end
         assert(reader.SubmitTravel(2,40,target,r.nativePermit) and nativeCalls==1 and properties==0)
        """)


class FinalReceipt(unittest.TestCase):
    def test_denial_retains_confirmed_final_idle_and_exact_attempt(self):
        l=enable(ready());l.execute(PACKET);l.execute("""
         equip(units[41],0,0);begin();local key=ExposedMembers.SPC_ExpeditionActivity.activityKey
         local r=reject('deny');local e=latest('GATE_RESULT','REJECTED')
         assert(e.requestKey==key and e.requestAccepted=='true' and e.phase=='ARRIVED' and e.mode=='NONE')
         assert(e.storeStatus=='CONFIRMED' and e.savedMatches=='true' and e.savedPhase=='ARRIVED')
         assert(e.taskStart=='NIL' and e.taskDue=='NIL' and e.owned=='false' and e.movesRemaining=='0')
         assert(not e.activityKey and not r.error and nativeCalls==0 and properties==0 and insightWrites==0)
        """)

    def test_failed_save_reports_blocked_and_last_confirmed_preparing(self):
        for fault in ('storeNoop=true','storeMalformed=true','storeThrowBefore=true'):
            with self.subTest(fault=fault):
                l=enable(ready());l.execute(PACKET);l.execute("""
                 begin();FAULT;local r=reject('deny');local e=latest('GATE_RESULT','REJECTED')
                 assert(r.error and e.requestAccepted=='false' and e.phase=='HELD' and e.mode=='BLOCKED')
                 assert(e.storeStatus=='BLOCKED' and e.savedPhase=='TASK_PREPARING' and e.savedMatches=='false')
                 assert(e.taskStart=='NIL' and insightWrites==0 and nativeCalls==0)
                """.replace('FAULT',fault))

    def test_stale_rejection_cannot_cancel_new_task_or_claim_success(self):
        l=enable(ready());l.execute(PACKET);l.execute("""
         begin();local _,old=reject('first');handler(2,{Action='TASK',Token='second',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1,Mission='PEOPLE',MissionX=15,MissionY=8});local key=ExposedMembers.SPC_ExpeditionActivity.activityKey
         old.Token='stale';local writes=storeWrites;handler(2,old)
         local e=latest('GATE_RESULT','REJECTED')
         assert(e.requestAccepted=='false' and e.phase=='TASK_PREPARING' and e.activityKey==key and e.requestKey~=key)
         assert(e.savedMatches=='true' and e.savedPhase=='TASK_PREPARING' and storeWrites==writes)
        """)

    def test_offline_snapshot_keeps_final_receipt_when_live_prints_were_missed(self):
        l=enable(ready());l.execute(PACKET);l.execute("""
         begin();reject('deny');ExposedMembers.SPC_ExpeditionActivity=nil
         lines={};print=function(s)lines[#lines+1]=s end
        """)
        l.execute(reader.command('trace','MARK:','DONE'))
        lines=list(l.globals().lines.values())
        self.assertTrue(any('ENTRY' in x and 'stage=GATE_RESULT' in x and 'requestResult=REJECTED' in x
                            and 'savedPhase=ARRIVED' in x for x in lines))


class ActualBridge(unittest.TestCase):
    def test_denied_zero_moves_ready_true_records_facts_without_extra_native_requests(self):
        l=activity();l.execute(READERS);l.execute("""
         equip(units[41],0,0);sleepDenied=true;publish('SLEEP')
         local e=latest('ACTIVITY_FAILURE')
         assert(e.movesRemaining=='0' and e.nativeReady=='true' and e.nativeActivity=='0' and e.guardStatus=='DENIED')
         assert(e.ownerTurnActive=='true' and e.localPlayer=='2' and e.interfaceMode=='11')
         assert(sleepChecks==2 and sleepCalls==0 and wakeCalls==0 and packets[1].Result=='REJECTED')
        """)

    def test_failed_unit_lookup_retains_failure_record_with_unavailable_native_sample(self):
        l=activity();l.execute(READERS);l.execute("""
         Players[2].GetUnits=function()error('private-lookup-detail')end
         publish('SLEEP');local e=latest('ACTIVITY_FAILURE')
         assert(e and e.nativeUnit=='UNAVAILABLE' and not e.line:find('private',1,true))
         assert(sleepCalls==0 and wakeCalls==0 and #packets==1 and packets[1].Result=='FAILED')
        """)

    def test_idle_ui_capture_uses_existing_revision_not_repeated_events(self):
        l=combined();l.execute("""
         local n=#records('IDLE_UI');assert(n==1)
         for i=1,100 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()end
         assert(#records('IDLE_UI')==n and sleepCalls==0 and wakeCalls==0 and not activityUpdate)
        """)

    def test_all_missions_trace_on_off_same_authority_writes_rewards_and_operations(self):
        for category in ('PEOPLE','WORKS','PLACES'):
            results=[]
            for traced in (False,True):
                l=combined() if traced else integrated()
                l.execute(MISSION_FIXTURE)
                l.execute("""
                 local before=storeWrites
                 local p={Action='TASK',Token='start',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1}
                 for k,v in pairs(CATEGORY)do p[k]=v end
                 handler(2,p);Events.GameCoreEventPublishComplete()
                 assert(view().phase=='TASK_RUNNING' and view().taskDue==85)
                 currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
                 deltaWrites=storeWrites-before
                 assert(view().phase=='ARRIVED' and view().mode=='NONE' and not activityUpdate)
                """.replace('CATEGORY',category))
                g=l.globals()
                results.append(tuple(g[k] for k in ('deltaWrites','sleepCalls','wakeCalls','insightWrites','placeCalls','finishCalls','properties','nativeCalls')))
                if traced:
                    l.execute("local e=latest('GATE_RESULT','RELEASED');assert(e.requestAccepted=='true' and e.savedPhase=='ARRIVED' and e.savedMatches=='true')")
            with self.subTest(category=category):
                self.assertEqual(results[0],results[1])
                self.assertEqual(results[1][1:],(1,1,1,0,0,0,0))

if __name__=='__main__':unittest.main()
