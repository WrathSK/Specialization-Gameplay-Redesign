"""S8c2 bounded existing-turn held cleanup; actual Store/RuntimeWork, native doubles."""
import unittest
from refactor_harness import measure
from test_refactor_s8c1 import fixture,actual_store


def timed():
 vm=fixture();vm.execute("Game.GetLocalPlayer=function()localReads=(localReads or 0)+1;return localOwner or 0 end")
 return vm


class BoundedTurnExit(unittest.TestCase):
 def test_initial_same_turn_and_duplicate_do_not_retry_then_new_turn_recovers(self):
  vm=timed();vm.execute("""
  lose(ca,900);assert(tries==1);local writes=T.writes()
  T.turn(0);T.turn(0);assert(tries==1 and not localReads)
  T.turn(1);assert(tries==2 and localReads==1);T.turn(0);assert(tries==2 and localReads==1)
  canClean=true;T.turn(1);assert(tries==3 and status()=='WITHDRAWN')
  for i=1,20 do T.turn(1)end
  assert(tries==3 and localReads==2 and T.writes()==writes)
  """)
  measure('S8c2_bounded_held_turn',{'same_turn_extra_cleanup':0,'next_turn_permits':1,'original_callback_budget':3,'automatic_site_budget':3,'additional_saved_writes':0,'new_timer_or_listener':False})
 def test_unreadable_site_consumes_three_automatic_attempts_without_publish_retry(self):
  vm=timed();vm.execute("""
  lose(ca,900);local get=CityManager.GetCityAt;siteReads=0;local writes=T.writes()
  CityManager.GetCityAt=function()siteReads=siteReads+1;error('SITE_UNKNOWN')end
  for i=1,20 do T.turn(1);T.turn(0)end
  assert(siteReads==3 and tries==1 and localReads==3 and T.writes()==writes)
  for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end
  assert(siteReads==3 and tries==1)
  CityManager.GetCityAt=get;canClean=true;shared.CityProgressionStore.ExitConfirmed()
  assert(tries==2 and status()=='WITHDRAWN')
  """)
 def test_existing_callback_budget_and_successful_sibling_do_not_reset(self):
  vm=timed();vm.execute("""
  siblings=0;shared.CityProgressionStore.RegisterExit('Sibling',function()siblings=siblings+1 end)
  lose(ca,900);shared.CityProgressionStore.ExitConfirmed();shared.CityProgressionStore.ExitConfirmed()
  assert(tries==3 and siblings==1);local get=CityManager.GetCityAt;siteReads=0
  CityManager.GetCityAt=function(...)siteReads=siteReads+1;return get(...)end
  for i=1,20 do T.turn(1)end
  assert(tries==3 and siblings==1 and siteReads==0 and not localReads and status()=='PARTIAL_HELD')
  canClean=true;retry();assert(tries==4 and status()=='WITHDRAWN')
  """)
 def test_same_loss_private_storage_revision_preserves_budget(self):
  vm=timed();vm.execute("""
  lose(ca,900);local get=CityManager.GetCityAt;siteReads=0
  CityManager.GetCityAt=function()siteReads=siteReads+1;return nil end
  for i=1,3 do T.turn(1)end;assert(siteReads==3)
  assert(T.write(ca,T.normal(T.record(ca))));T.turn(1);assert(siteReads==3)
  """)
 def test_new_loss_gets_its_own_bounded_generation(self):
  vm=timed();vm.execute("""
  lose(ca,900);local get=CityManager.GetCityAt;siteReads=0
  CityManager.GetCityAt=function()siteReads=siteReads+1;return nil end
  for i=1,3 do T.turn(1)end;assert(siteReads==3)
  CityManager.GetCityAt=get;canClean=true;shared.CityProgressionStore.ExitConfirmed();assert(status()=='WITHDRAWN')
  ca.s.ref.owner=0;ca.s.ref.cityID=originID;Events.CityTransfered.Fire(0,originID,9)
  assert(T.record(ca).stage=='ACTIVE');canClean=false;lose(ca,900)
  CityManager.GetCityAt=function()siteReads=siteReads+1;return nil end
  T.turn(0);assert(siteReads==3);T.turn(1);assert(siteReads==4 and status()=='TARGET_UNAVAILABLE')
  """)
 def test_nonlocal_missing_and_throwing_local_provider_skip_only_retry_and_age_continues(self):
  for mode in ('nonlocal','missing','throw'):
   vm=timed();vm.execute("""
   local cityA=a;a=shared.InvestmentAction;local research=T.research(3);a=cityA
   T.governor(1);lose(ca,900);local age=T.record(research).researchTradition.age
   mode=...
   if mode=='nonlocal'then Game.GetLocalPlayer=function()return 9 end
   elseif mode=='missing'then Game.GetLocalPlayer=nil
   else Game.GetLocalPlayer=function()error('LOCAL_UNKNOWN')end end
   T.turn(1);assert(tries==1 and T.record(research).researchTradition.age==age+1)
   """,mode)
 def test_healthy_completed_nonparticipant_and_busy_workers_add_no_site_reads(self):
  vm=timed();vm.execute("""
  local get=CityManager.GetCityAt;siteReads=0
  CityManager.GetCityAt=function(...)siteReads=siteReads+1;return get(...)end
  T.turn(1);Events.PlayerTurnActivated.Fire(9);assert(siteReads==0 and not localReads)
  canClean=true;lose(ca,900);assert(status()=='WITHDRAWN');local before=siteReads
  for i=1,10 do T.turn(1)end;assert(siteReads==before and not localReads)
  """)
 def test_cold_load_existing_cleanup_does_not_double_retry_on_same_turn(self):
  vm=timed();vm.execute("""
  lose(ca,900);T.reload();local s=shared.CityProgressionStore;coldCalls=0
  s.RegisterExit('Cold',function()coldCalls=coldCalls+1;return false end)
  Events.LoadScreenClose.Fire();assert(coldCalls==1)
  T.turn(0);T.turn(0);assert(coldCalls==1)
  T.turn(1);assert(coldCalls==2);T.turn(0);assert(coldCalls==2)
  """)
 def test_two_held_cities_recover_independently_with_one_local_sample(self):
  vm=timed();vm.execute("""
  lose(ca,900);lose(cb,901);assert(tries==2)
  canClean=true;T.turn(1)
  assert(tries==4 and status(ca)=='WITHDRAWN'and status(cb)=='WITHDRAWN'and localReads==1)
  """)
 def test_reentrant_site_activation_does_not_consume_twice_or_repeat_cleanup(self):
  vm=timed();vm.execute("""
  lose(ca,900);local get=CityManager.GetCityAt;siteReads=0
  CityManager.GetCityAt=function(...)siteReads=siteReads+1;T.turn(0);return get(...)end
  T.turn(1);assert(siteReads==1 and tries==2 and localReads==1)
  T.turn(0);assert(siteReads==1 and tries==2)
  """)
 def test_existing_cleanup_survives_unknown_clock_and_reentrant_clock_is_busy_guarded(self):
  for mode in ('throw','invalid','reenter'):
   vm=timed();vm.execute("""
   lose(ca,900);local clock=Game.GetCurrentGameTurn;canClean=true;mode=...
   Game.GetCurrentGameTurn=function()
    if mode=='throw'then error('CLOCK_UNKNOWN')end
    if mode=='invalid'then return 'UNKNOWN'end
    shared.CityProgressionStore.ExitConfirmed();return clock()
   end
   shared.CityProgressionStore.ExitConfirmed();assert(tries==2 and status()=='WITHDRAWN')
   """,mode)
 def test_local_provider_reentry_that_creates_new_loss_does_not_spend_old_permit(self):
  vm=timed();vm.execute("""
  lose(ca,900);local once=true
  Game.GetLocalPlayer=function()
   if once then
    once=false;assert(shared.CityProgressionStore.ExitCompleted('Async',ca,losses[ca],tickets[ca]))
    ca.s.ref.owner=0;ca.s.ref.cityID=originID;Events.CityTransfered.Fire(0,originID,9)
    assert(T.record(ca).stage=='ACTIVE');lose(ca,900)
   end
   return 0
  end
  T.turn(1);assert(tries==2 and T.record(ca).ownerChanges==2 and status()=='PARTIAL_HELD')
  T.turn(0);assert(tries==2);T.turn(1);assert(tries==3)
  """)
 def test_unknown_clock_without_baseline_waits_for_reliable_boundary_before_retry(self):
  vm=timed();vm.execute("""
  lose(ca,900);local clock=Game.GetCurrentGameTurn
  -- Cold workers have no session clock; existing load cleanup still proceeds.
  clockReads=0;Game.GetCurrentGameTurn=function()clockReads=clockReads+1;if clockReads==1 then return clock()end;error('CLOCK_UNKNOWN')end
  calls=0;local start=SPCCityProgressionStore.Start
  SPCCityProgressionStore.Start=function(P,shared,...)
   start(P,shared,...);shared.CityProgressionStore.RegisterExit('Clock',function()calls=calls+1;return false end)
  end
  T.reload();assert(calls==1)
  Game.GetCurrentGameTurn=clock;T.turn(1);assert(calls==1)
  T.turn(0);assert(calls==1);T.turn(1);assert(calls==2)
  """)

if __name__=='__main__':unittest.main()
