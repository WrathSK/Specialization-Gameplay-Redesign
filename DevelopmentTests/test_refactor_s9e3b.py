"""R09b actual D producers/consumers and bounded foreign target recovery."""
from contextlib import contextmanager, nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import subprocess
import unittest
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,measure,legacy_source_observation
from test_refactor_s5d1 import research,cross
from test_b270_event_scope import make_fixture,MODULES


@contextmanager
def baseline():
 paths=('RuntimeWork','ResearchApply','ResearchChair','ResearchCross','CultureNetwork')
 old={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','f55c41f:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in paths}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(s.encode()).hexdigest():'historical/f55c41f/'+str(p.relative_to(ROOT))for p,s in old.items()}
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',lambda p,*a,**kw:old[p]if p in old else read(p,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield


@contextmanager
def producer_before(module,create_d=False):
 """Fixture startup order: actual FC/D before actual writer, bindings after all.
 No writer source is transformed; no policy or native producer is replaced.
 """
 source=(ROOT/'Mod'/(module+'.lua')).read_text();execute=TrackedLua51.execute
 def run(vm,s,*a,**kw):
  if s==source and not vm.eval('shared.FactChanges~=nil'):
   execute(vm,(ROOT/'Mod/FactChanges.lua').read_text());execute(vm,'SPCFactChanges.New(shared)')
   if create_d:
    execute(vm,(ROOT/'Mod/OrdinaryBuildingCatalog.lua').read_text())
    execute(vm,(ROOT/'Mod/DistrictCompleteness.lua').read_text());execute(vm,'SPCDistrictCompleteness.Start(P,shared)')
  return execute(vm,s,*a,**kw)
 with patch.object(TrackedLua51,'execute',run):yield


def actual(name):
 with legacy_source_observation(),producer_before(name,create_d=name!='ResearchApply'):
  if name=='ResearchApply':v=research()
  elif name=='ResearchCross':v=cross()
  else:
   import test_culture_network as c
   c.LuaRuntime=TrackedLua51;v=c.fixture(False)
   v.execute("send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);fire('LoadScreenClose')")
  v.execute((ROOT/'Mod/FactConsumerBindings.lua').read_text());v.execute('SPCFactConsumerBindings.New(shared)')
 v.execute("""
 function pp()shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete')end
 audits={};local observe=P.Observe
 P.Observe=function(k,n)if k=='audit'then audits[n]=(audits[n]or 0)+1 end;if observe then observe(k,n)end end
 pp();audits={}
 if shared.CultureNetwork then local a=shared.CultureNetwork.Audit;shared.CultureNetwork.Audit=function(scope)audits.CultureNetwork=(audits.CultureNetwork or 0)+1;return a(scope)end end
 """)
 return v


class ProducerConsumers(unittest.TestCase):
 def test_unrelated_foreign_transfer_and_removal_do_not_audit_four_writers(self):
  values=[]
  for old in (True,False):
   row={}
   with baseline()if old else nullcontext():
    for name,owners in [('ResearchApply',('ResearchApply','ResearchChair')),('ResearchCross',('ResearchCross',)),('CultureNetwork',('CultureNetwork',))]:
     v=actual(name)
     v.execute("for i=1,10 do fire('CityTransfered',9,900+i,10);fire('CityRemovedFromMap',9,900+i);pp()end")
     for owner in owners:row[owner]=v.eval("audits['"+owner+"']or 0")
   values.append(row)
  self.assertTrue(all(n>0 for n in values[0].values()))
  self.assertEqual(values[1],dict.fromkeys(values[1],0))
  measure('S9e3b_four_readers_foreign_lifecycle',{'baseline':'B375','transfers':10,'removals':10,'before_audits':values[0],'after_audits':values[1],'scope':'actual D->FC->Bindings and real writers; other modules not implied'})
 def test_D_routes_incoming_city_once_and_same_turn_next_change_survives(self):
  for name,owners in [('ResearchApply',('ResearchApply','ResearchChair')),('ResearchCross',('ResearchCross',)),('CultureNetwork',('CultureNetwork',))]:
   with self.subTest(name=name):
    v=actual(name);v.execute("fire('CityTransfered',0,1,9);pp()")
    for owner in owners:self.assertEqual(v.eval("audits['"+owner+"']or 0"),1)
    v.execute("fire('CityTransfered',0,1,9);pp()")
    for owner in owners:self.assertEqual(v.eval("audits['"+owner+"']or 0"),2)
 def test_actual_D_propagates_supported_former_owner_without_aliasing_destination_ID(self):
  v=actual('ResearchApply');v.execute("""
  local seen={};shared.DistrictCompleteness.RegisterConsumer('capture',function(e)seen[#seen+1]=e end)
  local c=cities[2];cities[2]=nil;c.owner=9;c.id=900
  fire('CityTransfered',9,900,0);pp()
  assert(#seen==1 and seen[1].player==0 and seen[1].city==nil)
  assert(audits.ResearchApply==1 and audits.ResearchChair==1)
  assert(shared.ResearchApply.errors[0][900]==nil and chair.errors[0][900]==nil)
  """)
 def test_unknown_native_signature_keeps_conservative_D_work(self):
  v=actual('ResearchApply');v.execute("fire('CityTransfered',9,900);pp();assert(audits.ResearchApply==1 and audits.ResearchChair==1)")
 def test_no_provider_fallback_still_handles_known_incoming_and_ignores_foreign(self):
  v=cross();v.execute("""
  assert(not shared.DistrictCompleteness and not shared.FactChanges)
  local n=total('city_scan');fire('CityTransfered',9,900,10);fire('GameCoreEventPublishComplete');assert(total('city_scan')==n)
  fire('CityTransfered',0,1,9);fire('GameCoreEventPublishComplete');assert(total('city_scan')==n+1)
  """)


class SevenTargets(unittest.TestCase):
 def fixture(self,n=10):
  with legacy_source_observation():v,_,_=make_fixture(n,True)
  return v
 def test_actual_seven_owners_foreign_transfer_adds_zero_city_or_building_reads(self):
  result=[]
  for old in (True,False):
   with baseline()if old else nullcontext():v=self.fixture()
   v.execute("for i=1,10 do Events.CityTransfered.Fire(9,900+i,10);Events.GameCoreEventPublishComplete.Fire()end")
   result.append(dict(v.globals().counts))
  self.assertGreater(result[0].get('city_scan',0),0)
  self.assertEqual(result[1].get('city_scan',0),0);self.assertEqual(result[1].get('building_check',0),0)
  measure('S9e3b_seven_owners_foreign_transfer',{'baseline':'B375','owners':MODULES,'transfers':10,'before':result[0],'after':result[1],'scope':'NewTargets actual seven owners; own-turn/load behavior preserved'})
 def test_incoming_targets_new_city_and_keeps_existing_sibling_untouched(self):
  v=self.fixture();v.execute("""
  newCity=addCity(0,2,2,2);local sibling=cities[0][0]
  sibling.GetBuildings=function()error('UNRELATED_LOCAL_CITY_READ')end
  Events.CityTransfered.Fire(0,2,9);Events.GameCoreEventPublishComplete.Fire()
  for _,name in ipairs({'Lv2Housing','Lv2GPP','ResearchSupport','IndustrySupport','Lv3Effects','ResearchInfrastructure','Lv3Support'})do
   local errors=shared[name].errors;assert(not errors['0:0']and not(type(errors[0])=='table'and errors[0][0]),name)
  end
  assert(counts.city_scan==5 and not counts.building_create) -- two retired owners retry only; five current owners visit
  """)
 def test_foreign_pending_carrier_cleanup_follows_confirmed_transfer_with_new_ID(self):
  # Start cold: the historical standalone fixture omits RuntimeRetirement's
  # load reset; seeding damage after a successful cleanup is not a pending case.
  for old_owner in (0,1):
   with legacy_source_observation():v,_,_=make_fixture(2,old_owner==0,initial_load=False)
   v.execute("""
   c=cities[%d][%d];local id=P.Info('Buildings','BUILDING_SPC_DEV_LV3_POP_CULTURE_0').Index
   c.values[id]=true;c.bad=true;Events.LoadScreenClose.Fire()
   local oldOwner=c.owner;local oldID=c.id;cities[oldOwner][oldID]=nil;c.owner=2;c.id=11;cities[2][11]=c
   Events.CityTransfered.Fire(2,11,oldOwner);c.bad=false;Events.PlayerTurnActivated.Fire(2)
   assert(not c.values[id]and shared.Lv3Effects.busy==false)
   """%(old_owner,old_owner))
 def test_newtargets_unrelated_foreign_does_not_resolve_waiting_original_foreign_exit(self):
  c=Context();c.load('RuntimeWork');c.execute("""
  P={IsTestPlayer=function(p)return p==0 end,Count=function()end};reads=0;calls=0;allow=false
  local city={GetOwner=function()return 1 end,GetID=function()return 7 end,GetX=function()return 10 end,GetY=function()return 20 end}
  Players={[1]={GetCities=function()reads=reads+1;return {FindID=function(_,id)if id==7 then return city end end}end}}
  t=SPCRuntimeWork.NewTargets(P,shared,function()end,function()end)
  local exit=t.Exit(function(c)assert(c==city);calls=calls+1;assert(allow,'CLEANUP_UNKNOWN')end)
  assert(not pcall(exit,city,{}));allow=true;local n=reads
  t.Run({transfer={owner=9,city=90,oldOwner=10}});assert(reads==n and calls==1 and t.exits['1:7'])
  t.Run({transfer={owner=2,city=70,oldOwner=1}});assert(calls==2 and not next(t.exits))
  """)
 def test_failed_supported_source_transfer_is_retained_until_reliable_related_event(self):
  from test_refactor_s5d4d2 import targets
  c=targets();c.execute("""
  t.Run({transfer={owner=1,city=99,oldOwner=0}});assert(t.pending['0:7']and next(t.transfers))
  local n=#visited;available=true;t.Run({transfer={owner=9,city=900,oldOwner=10}});assert(#visited==n and t.pending['0:7'])
  t.Run({transfer={owner=1,city=99,oldOwner=2}});assert(#visited==n+1 and visited[#visited].owner==1 and visited[#visited].city==99)
  assert(not t.pending['0:7']and next(t.transfers)==nil)
  """)
 def test_scope_helper_second_owner_mark_survives_first_owner_failure(self):
  c=Context();c.load('RuntimeWork');c.execute("""
  P={IsTestPlayer=function(p)return p==0 or p==1 end};seen={}
  local ok,why=pcall(SPCRuntimeWork.LifecycleScopes,P,{transfer={owner=1,city=99,oldOwner=0}},function(s)
   seen[#seen+1]=s;if s.player==1 then error('FIRST_OWNER_MARK_FAILED')end
  end)
  assert(not ok and tostring(why):find('FIRST_OWNER_MARK_FAILED',1,true)and #seen==2 and seen[2].player==0)
  """)
 def test_scope_helper_preserves_both_supported_owners_and_unknown_fallback(self):
  c=Context();c.load('RuntimeWork');c.execute("""
  P={IsTestPlayer=function(p)return p==0 or p==1 end};seen={};local function add(s)seen[#seen+1]=s end
  SPCRuntimeWork.LifecycleScopes(P,{transfer={owner=1,city=99,oldOwner=0}},add)
  assert(#seen==2 and seen[1].player==1 and seen[1].city==99 and seen[2].player==0 and seen[2].city==nil)
  seen={};SPCRuntimeWork.LifecycleScopes(P,{transfer={owner=9,city=99,oldOwner=10}},add);assert(#seen==0)
  local fallback={};SPCRuntimeWork.LifecycleScopes(P,fallback,add);assert(seen[1]==fallback)
  seen={};SPCRuntimeWork.LifecycleScopes(P,{transfer={owner=0,city=99,oldOwner=0}},add);assert(#seen==1 and seen[1].player==0 and seen[1].city==nil)
  """)

if __name__=='__main__':unittest.main()
