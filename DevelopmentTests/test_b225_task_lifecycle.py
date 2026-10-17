"""B225 delta: event-phase scheduling, release, city Works, deal invalidation.
Real Lua paths with engine-shaped fixtures; LOCAL_SIMULATION only.
"""
import unittest
from test_expedition_spy_activity_ui import bridge
from test_expedition_spy_activity_integration import integrated
import test_expedition_missions as missions
from test_expedition_missions import MISSION_FIXTURE
from test_p0_k import Fixture

class Scheduling(unittest.TestCase):
 def test_burst_coalesces_without_native_query_in_event_stack(self):
  l=bridge();l.execute("""
   refreshAuto=false
   local native=UnitManager.CanStartOperation
   UnitManager.CanStartOperation=function(...)assert(refreshEventDepth==0);return native(...)end
   local before=ContextPtr.refreshRequests or 0
   publish('SLEEP');for i=1,30 do Events.GameCoreEventPublishComplete()end
   assert(sleepChecks==0 and sleepCalls==0 and arms==0 and ContextPtr.refreshRequests==before+1)
   drainRefreshFrames(1);assert(arms==1 and sleepCalls==0 and #packets==0)
   drainRefreshFrames(1);assert(sleepCalls==1 and #packets==0)
   drainRefreshFrames(1);assert(#packets==1 and packets[1].Result=='ASLEEP')
   drainRefreshFrames();assert(not ContextPtr.refreshPending)
  """)
 def test_core_busy_waits_for_real_event_without_self_poll(self):
  l=bridge();l.execute("""
   refreshAuto=false;coreBusy=true;publish('SLEEP');drainRefreshFrames()
   assert(sleepChecks==0 and arms==0 and not ContextPtr.refreshPending and update==nil)
   coreBusy=false;drainRefreshFrames();assert(arms==0)
   Events.GameCoreEventPublishComplete();drainRefreshFrames();assert(sleepCalls==1 and #packets==1)
  """)
 def test_event_time_denial_not_evaluated_before_safe_refresh(self):
  l=bridge();l.execute("""
   refreshAuto=false;sleepDenied=true;publish('SLEEP');assert(#packets==0)
   sleepDenied=false;drainRefreshFrames();assert(sleepCalls==1 and packets[1].Result=='ASLEEP')
  """)
 def test_safe_refresh_denial_retains_no_bypass(self):
  l=bridge();l.execute("refreshAuto=false;sleepDenied=true;publish('SLEEP');drainRefreshFrames();assert(sleepCalls==0 and packets[1].Result=='REJECTED')")
 def test_release_awaits_later_refresh_not_writer_stack_or_mandatory_clear_event(self):
  l=bridge();l.execute("""
   publish('SLEEP');refreshAuto=false;publish('RELEASE',true)
   drainRefreshFrames(1);assert(wakeCalls==1 and units[41].activity==0 and #packets==1)
   drainRefreshFrames(1);assert(#packets==2 and packets[2].Result=='RELEASED')
   drainRefreshFrames();assert(wakeCalls==1 and not ContextPtr.refreshPending)
  """)
 def test_operation_events_filter_unit_and_resume_readback(self):
  l=bridge();l.execute("""
   refreshAuto=false;delaySleep=true;publish('SLEEP');drainRefreshFrames()
   assert(sleepCalls==1 and #packets==0)
   Events.UnitOperationsCleared(2,42);assert(not ContextPtr.refreshPending)
   units[41].activity=1;Events.UnitOperationsCleared(2,41);assert(ContextPtr.refreshPending)
   drainRefreshFrames();assert(packets[1].Result=='ASLEEP' and sleepCalls==1 and update==nil)
  """)
 def test_pending_owner_change_and_shutdown_do_not_write_stale_unit(self):
  l=bridge();l.execute("refreshAuto=false;publish('SLEEP');localOwner=3;drainRefreshFrames();assert(sleepCalls==0 and arms==0);shutdown();assert(not ContextPtr.refreshPending)")
 def test_missing_busy_api_is_diagnostic_not_permanent_block(self):
  l=bridge(with_trace=True);l.execute("UI.IsGameCoreBusy=nil;publish('SLEEP');assert(sleepCalls==1 and packets[1].Result=='ASLEEP')")

 def test_scheduler_diagnostic_uses_existing_bounded_ring(self):
  from test_expedition_activity_trace import fixture
  l=fixture();l.execute("""
   UI.IsGameCoreBusy=nil;sleepDenied=true;publish('SLEEP')
   local f=records('ACTIVITY_FAILURE')[1]
   assert(f.evaluationOrigin=='UI_REFRESH' and f.coreBusy=='UNAVAILABLE' and f.signalOrigin=='PUBLICATION')
   assert(f.operationEvent=='NONE' and f.lastOperationHash=='NIL')
  """)

class Completion(unittest.TestCase):
 def test_manual_sleep_success_then_next_category_without_wake_or_locked_menu(self):
  l=integrated();l.execute(MISSION_FIXTURE);l.execute("""
   units[41].activity=1;beginTask();assert(not view().owned and sleepCalls==0)
   currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
   assert(view().phase=='ARRIVED' and not view().taskStart and wakeCalls==0 and units[41].activity==1)
   local p={Action='TASK',Token='works',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1}
   for k,v in pairs(WORKS)do p[k]=v end;handler(2,p);Events.GameCoreEventPublishComplete()
   assert(view().phase=='TASK_RUNNING' and not view().owned)
   currentTurn=87;ownTurn(2);Events.GameCoreEventPublishComplete()
   assert(view().phase=='ARRIVED' and insightWrites==2 and wakeCalls==0 and not view().taskStart)
  """)
 def test_manual_sleep_cancel_clears_draft_preserves_sleep(self):
  l=integrated();l.execute("""
   units[41].activity=1;beginTask()
   local cities=Players[3]:GetCities();cities.GetCapitalCity=function()return city end;Players[3].GetCities=function()return cities end
   currentTurn=84;ownTurn(2);Events.GameCoreEventPublishComplete()
   assert(view().phase=='ARRIVED' and not view().taskStart and insightWrites==0 and wakeCalls==0 and units[41].activity==1)
  """)
 def test_hold_with_unowned_complete_does_not_reenter_failing_cleanup(self):
  l=integrated();l.execute("""
   units[41].activity=1;beginTask()
   units[41].GetX=function(self)if insightWrites>0 then error('CLEANUP_READ_FAILED')end;return self.x end
   currentTurn=85;assert(pcall(ownTurn,2));Events.GameCoreEventPublishComplete()
   assert(view().phase=='HELD' and not view().owned and insightWrites==1 and wakeCalls==0)
  """)

class WorksCity(unittest.TestCase):
 def test_unknown_earlier_slot_does_not_hide_known_eligible_later_slot(self):
  l=missions.Missions().ready();l.execute("""
   uiMissionBuildings.GetNumGreatWorkSlots=function()return 2 end
   uiMissionBuildings.GetGreatWorkInSlot=function(_,b,s)if s==0 then error('UNKNOWN')end;return 12 end
   assert(startMission('w',WORKS).phase=='TASK_RUNNING')
  """)
 def test_incomplete_negative_unknown_and_reliable_empty_invalid(self):
  l=missions.Missions().ready();l.execute("slotError=true;assert(startMission('u',WORKS).missionStatus=='UNKNOWN');slotError=false;slotWork=nil;assert(startMission('e',WORKS).error=='MISSION_TARGET_INVALID')")
 def test_unreviewed_era_is_unknown_not_reliable_empty(self):
  l=missions.Missions().ready();l.execute("SPCGreatWorkCatalog.Resolve=function()return nil,'UNREVIEWED_ERA'end;assert(startMission('u',WORKS).missionStatus=='UNKNOWN')")
 def test_work_moves_between_buildings_without_cancelling_or_duplicate_reward(self):
  l=missions.Missions().ready();l.execute("""
   startMission('w',WORKS);slotWork=nil;has[5]=false;wonderSlotWork=13
   currentTurn=84;ownTurn(2);assert(req('READ','r').missionStatus=='VALID')
   currentTurn=85;ownTurn(2);release('r');ownTurn(2)
   assert(insightWrites==1 and req('READ','done').phase=='ARRIVED')
  """)

class SaleEvent(unittest.TestCase):
 def test_deal_without_work_moved_refreshes_empty_same_turn_once_and_recovers(self):
  fx=Fixture();fx.check('a.slots[10]={100};b.slots[10]={103}')
  from test_p0_k import PRODUCER, m
  fx.check(PRODUCER);fx.lua.execute((m/'UI/DialogueRefresh.lua').read_text())
  fx.check("""
   init();local d=ExposedMembers.SPC_DialogueBackground;local scans=d.scans;local sends=d.sends
   assert(shared.GreatWorkFacts.Summary(0,7).count==1)
   a.slots[10]={};for i=1,20 do fire('DiplomacyDealEnacted')end
   assert(d.scans==scans and d.sends==sends)
   fire('GameCoreEventPublishComplete')
   assert(d.scans==scans+1 and d.sends==sends+1 and lastPacket.FactsCount==1)
   assert(shared.GreatWorkFacts.Summary(0,7).count==0 and shared.GreatWorkFacts.Summary(0,8).count==1)
   b.slots[10]={};fire('DiplomacyDealEnacted');fire('GameCoreEventPublishComplete')
   assert(lastPacket.FactsCount==0 and lastPacket.FactsData=='EMPTY')
   scans=d.scans;sends=d.sends
   for i=1,30 do fire('SystemUpdateUI');fire('GameCoreEventPublishComplete')end
   assert(d.scans==scans and d.sends==sends)
   a.slots[10]={100};fire('DiplomacyDealEnacted');fire('GameCoreEventPublishComplete')
   assert(shared.GreatWorkFacts.Summary(0,7).count==1 and propertyWrites==0)
  """)


class SaleConsumers(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  import test_great_work_notifications as consumers
  consumers.CultureIntegrationTests.setUpClass()
 @classmethod
 def tearDownClass(cls):
  import test_great_work_notifications as consumers
  consumers.CultureIntegrationTests.tearDownClass()
 def test_deal_producer_to_three_actual_writers_same_turn(self):
  import test_great_work_notifications as consumers
  from test_p0_k import m
  l=consumers.CultureIntegrationTests().runtime()
  l.execute("""
   local sourceInclude=include;include=function(n)if n~='Probe' and n~='DiagnosticLog'then sourceInclude(n)end end
   SPCP0=P;Game.GetLocalPlayer=function()return 0 end;shared.Version=P.VERSION;ExposedMembers.SPC_P0=shared
   for _,name in ipairs({'DiplomacyDealEnacted','SystemUpdateUI','GameCoreEventPublishComplete'})do
    Events[name]={list={}};Events[name].Add=function(f)table.insert(Events[name].list,f)end
    Events[name].Remove=function()end
   end
   local bid=GameInfo.Buildings.BUILDING_AMPHITHEATER.Index
   for _,c in ipairs({a,b})do
    c.actualWorks=1;local original=c.GetBuildings
    c.GetBuildings=function(self)
     local v=original(self)
     v.GetNumGreatWorkSlots=function(_,index)return index==bid and c.actualWorks or 0 end
     v.GetGreatWorkInSlot=function(_,index,slot)return c.id*100+slot end
     v.GetGreatWorkTypeFromIndex=function()return 'GREATWORK_BHASA_1'end
     return v
    end
   end
   PlayerOperations={EXECUTE_SCRIPT=1}
   UI={RequestPlayerOperation=function(pid,op,p)lastPacket=p;meaningRequest(pid,p);return true end}
   ContextPtr={SetInitHandler=function(_,f)producerInit=f end,SetShutdown=function()end}
  """)
  l.execute((m/'UI/DialogueRefresh.lua').read_text())
  l.execute("""
   producerInit();assert(total(a)>0 and meaningCount(a)>0 and inspiration(a)==3,tostring(ExposedMembers.SPC_DialogueBackground.collectionError)..':'..tostring(shared.GreatWorkFacts.lastError)..':'..tostring(ExposedMembers.SPC_DialogueBackground.state)..':'..tostring(ExposedMembers.SPC_DialogueBackground.transport))
   a.actualWorks=0;fire('DiplomacyDealEnacted');fire('GameCoreEventPublishComplete')
   assert(total(a)==0 and meaningCount(a)==0 and inspiration(a)==0)
   assert(total(b)>0 and meaningCount(b)>0 and inspiration(b)==3)
   a.actualWorks=1;fire('DiplomacyDealEnacted');fire('GameCoreEventPublishComplete')
   assert(total(a)>0 and meaningCount(a)>0 and inspiration(a)==3)
   local n=writes;for i=1,20 do fire('GameCoreEventPublishComplete')end;assert(writes==n)
  """)

if __name__=='__main__':unittest.main()
