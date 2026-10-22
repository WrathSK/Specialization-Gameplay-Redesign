"""D0055 source qualification, total Food and event-driven idempotence. LOCAL only."""
import unittest
from pathlib import Path
from test_b239_commerce import fixture
from test_b239_commerce_ui import fixture as ui_fixture

class Sources(unittest.TestCase):
 def test_wrong_identity_higher_yields_do_not_win(self):
  l=fixture();l.execute("""
   cities[4].yields.SCIENCE=9999;cities[1].yields.CULTURE=9999
   cities[5].yields.SCIENCE=8888;cities[5].yields.CULTURE=8888
   assert(toggle(2,'DISTRICT_CAMPUS',true));assert(toggle(2,'DISTRICT_THEATER',true))
   assert(domain(2,'DISTRICT_CAMPUS').source==1 and domain(2,'DISTRICT_THEATER').source==4)
   assert(not nativeReads['4:SCIENCE'] and not nativeReads['1:CULTURE'])
  """)
 def test_identity_does_not_require_active_potential_or_district(self):
  for active in ('0','nil'):
   with self.subTest(active=active):
    l=fixture();l.execute("cities[1].active="+active+""";cities[1].potential=0
     cities[1].depths={};cities[1].dcFail=true;cities[1].storeFail=true
     assert(toggle(2,'DISTRICT_CAMPUS',true));assert(domain(2,'DISTRICT_CAMPUS').source==1)
     assert(not depthReads[1] and not nativeReads['4:SCIENCE'])
    """)
 def test_unknown_identity_holds_and_same_turn_recovery_updates(self):
  l=fixture();l.execute("""
   assert(toggle(2,'DISTRICT_CAMPUS',true));cities[1].identityFail=true
   shared.OnPermanentCityWrite(cities[1],'Identity');Events.GameCoreEventPublishComplete.Fire()
   assert(view(2).reason=='COMMERCE_SOURCE_IDENTITY_UNKNOWN' and ownedGold(cities[2])==0)
   cities[1].identityFail=false;shared.OnPermanentCityWrite(cities[1],'Identity');Events.GameCoreEventPublishComplete.Fire()
   assert(domain(2,'DISTRICT_CAMPUS').source==1 and ownedGold(cities[2])==15)
  """)
 def test_unregistered_source_is_not_inferred_from_yield_or_buildings(self):
  l=fixture();l.execute("""
   cities[1].unregistered=true;cities[1].yields.SCIENCE=9999
   assert(toggle(2,'DISTRICT_CAMPUS',true));assert(domain(2,'DISTRICT_CAMPUS').source==2)
   assert(not nativeReads['1:SCIENCE'])
  """)
 def test_identity_exit_and_new_match_preserve_reverse_dependencies(self):
  l=fixture();l.execute("""
   assert(toggle(2,'DISTRICT_CAMPUS',true));cities[1].kind='COMMERCE'
   shared.OnPermanentCityWrite(cities[1],'Identity');Events.GameCoreEventPublishComplete.Fire()
   assert(domain(2,'DISTRICT_CAMPUS').source==2)
   cities[5].yields.SCIENCE=200;cities[5].kind='RESEARCH'
   shared.OnPermanentCityWrite(cities[5],'Identity');Events.GameCoreEventPublishComplete.Fire()
   assert(domain(2,'DISTRICT_CAMPUS').source==5 and ownedGold(cities[2])==30)
  """)
 def test_source_loss_and_return_respect_owner_and_route_proof(self):
  l=fixture();l.execute("""
   assert(toggle(2,'DISTRICT_CAMPUS',true));cities[1].owner=8;com.SourceChanged(0,1)
   assert(view(2).stage=='HELD' and ownedGold(cities[2])==0)
   cities[1].owner=0;returns.Commerce(0,cities[1]);Events.GameCoreEventPublishComplete.Fire()
   assert(domain(2,'DISTRICT_CAMPUS').source==1 and ownedGold(cities[2])==15)
  """)
 def test_one_batch_reads_each_identity_once_without_remote_depth(self):
  l=fixture();l.execute("""
   assert(toggle(2,'DISTRICT_CAMPUS',true));assert(toggle(2,'DISTRICT_THEATER',true))
   identityReads={};depthReads={};com.Refresh(0,2)
   assert(identityReads[1]==1 and identityReads[4]==1 and identityReads[5]==1)
   assert(not depthReads[1] and not depthReads[4] and not depthReads[5])
  """)

class FoodAndEffects(unittest.TestCase):
 def test_total_food_not_surplus_or_gold_and_unknown_self_food_holds(self):
  l=fixture();l.execute("""
   cities[2].yields.FOOD=40;cities[2].yields.GOLD=9999;cities[2].goldMultiplier=2
   cities[2].GetGrowth=function()error('surplus is not the contract')end
   cities[4].yields.FOOD=9999
   assert(toggle(2,'DISTRICT_CAMPUS',true));assert(toggle(2,'DISTRICT_HARBOR',true))
   assert(domain(2,'DISTRICT_HARBOR').X==40 and domain(2,'DISTRICT_HARBOR').source==2)
   assert(domain(2,'DISTRICT_HARBOR').gold==6 and ownedGold(cities[2])==21 and #cleanOrder==0)
   cities[2].yieldFail='FOOD';com.SourceChanged(0,2)
   assert(view(2).stage=='HELD' and ownedGold(cities[2])==0)
  """)
 def test_unchanged_updates_and_report_reads_have_zero_writes(self):
  l=fixture();l.execute("""
   assert(toggle(2,'DISTRICT_CAMPUS',true));assert(toggle(2,'DISTRICT_HARBOR',true))
   local before=com.writes;local saved=SPCCommerceModel.Copy(commerceStates[2]);local revision=view(2).revision
   for i=1,10 do com.SourceChanged(0,2)end
   assert(com.writes==before and revision==view(2).revision and eq(saved,commerceStates[2]))
   local reads=nativeReads['2:FOOD']
   for i=1,10 do assert(com.Request(0,{Action='COMMERCE_READ',CityID=2}));com.Describe(0,cities[2])end
   assert(com.writes==before and nativeReads['2:FOOD']==reads)
  """)
 def test_delayed_native_yield_echo_settles_without_new_writes(self):
  l=fixture();l.execute("""
   pendingYield={};local create=P.CreateBuilding;local remove=P.RemoveBuilding
   P.CreateBuilding=function(q,id)create(q,id);pendingYield[q.city.id]=true end
   P.RemoveBuilding=function(b,id)remove(b,id);pendingYield[b.city.id]=true end
   assert(toggle(2,'DISTRICT_CAMPUS',true));assert(toggle(2,'DISTRICT_HARBOR',true))
   local before=com.writes;local revision=view(2).revision
   for i=1,6 do
    local todo=pendingYield;pendingYield={}
    for cid in pairs(todo)do Events.CityYieldsChanged.Fire(0,cid);Events.CityBuildingsChanged.Fire(0,cid)end
    Events.GameCoreEventPublishComplete.Fire();assert(com.writes==before)
   end
   assert(next(pendingYield)==nil and view(2).revision==revision and ownedGold(cities[2])==18)
   -- A real change sharing the publication with a late echo must not disappear.
   cities[2].yields.FOOD=40;Events.CityYieldsChanged.Fire(0,2);Events.CityYieldsChanged.Fire(0,2)
   Events.GameCoreEventPublishComplete.Fire();assert(ownedGold(cities[2])==21)
  """)
 def test_other_commerce_city_carriers_never_removed_for_sampling(self):
  l=fixture();l.execute("""
   cities[4].kind='COMMERCE';cities[4].potential=3;cities[4].active=3
   cities[4].depths={DISTRICT_CAMPUS=3};cities[4].yields.SCIENCE=1000;cities[4].yields.FOOD=9999
   commerceStates[4]=SPCCommerceModel.Select(SPCCommerceModel.New(0),'DISTRICT_CAMPUS',true)
   com.SourceChanged(0,4);assert(ownedGold(cities[4])==150)
   local remove=P.RemoveBuilding
   P.RemoveBuilding=function(b,id)assert(b.city.id~=4,'must not dismantle another consumer');remove(b,id)end
   assert(toggle(2,'DISTRICT_HARBOR',true));com.Refresh(0,2)
   assert(domain(2,'DISTRICT_HARBOR').source==2 and ownedGold(cities[4])==150)
  """)
 def test_food_zero_and_restored_same_turn_and_domain_off_cleanup(self):
  l=fixture();l.execute("""
   assert(toggle(2,'DISTRICT_HARBOR',true));local saved=SPCCommerceModel.Copy(commerceStates[2])
   cities[2].yields.FOOD=0;Events.CityYieldsChanged.Fire(0,2);Events.GameCoreEventPublishComplete.Fire()
   assert(domain(2,'DISTRICT_HARBOR').X==0 and ownedGold(cities[2])==0 and eq(saved,commerceStates[2]))
   cities[2].yields.FOOD=40;Events.CityYieldsChanged.Fire(0,2);Events.GameCoreEventPublishComplete.Fire()
   assert(ownedGold(cities[2])==6);assert(toggle(2,'DISTRICT_HARBOR',false));assert(ownedGold(cities[2])==0)
  """)

class EligibilityUI(unittest.TestCase):
 def test_unselected_missing_local_district_is_reported_with_configuration_entry(self):
  l=fixture();l.execute("""
   cities[2].depths={};com.SourceChanged(0,2);local report=com.Describe(0,cities[2]);local count=0
   for _,r in ipairs(view(2).domains)do assert(r.reason=='COMMERCE_LOCAL_DISTRICT_REQUIRED');count=count+1 end
   assert(count==5 and report:find('本城缺少对应区域',1,true) and report:find('城市生产列表',1,true))
   assert(report:find('总粮食，非余粮',1,true))
  """)
 def test_report_does_not_refresh_as_side_effect_even_with_dirty_inputs(self):
  l=fixture();l.execute("""
   assert(toggle(2,'DISTRICT_HARBOR',true));local n=com.writes
   cities[2].yields.FOOD=100;com.Mark(0,2)
   assert(com.Request(0,{Action='COMMERCE_READ',CityID=2}));assert(com.writes==n and domain(2,'DISTRICT_HARBOR').X==20)
   Events.GameCoreEventPublishComplete.Fire();assert(domain(2,'DISTRICT_HARBOR').X==100)
  """)
 def test_panel_displays_missing_district_reason_on_disabled_button(self):
  ui_fixture(panel=True).execute("""
   LuaEvents.SPC_CommerceOpen(0,9)
   assert(Controls.Domain4State.text:find('LOCAL_DISTRICT_REQUIRED',1,true))
   assert(Controls.Domain4Toggle.disabled and Controls.Domain4Toggle.tip==Controls.Domain4State.text)
  """)

if __name__=='__main__':unittest.main()
