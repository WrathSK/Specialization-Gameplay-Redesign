"""S7e exact retired IDs, reference-scoped success and actual owner hot paths."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import sqlite3
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,executed,completion,legacy_source_observation,measure
from project_paths import external_database
from test_refactor_s5d4c1 import actual_cross
from refactor_defect_fixtures import startup
import test_culture_aesthetic as aesthetic

BASE='c55b48406d1c504d5174e6ba27d950f3e9b4fc36'
FILES=('RuntimeWork','ResearchCross','ResearchInfrastructure','SpecialistSupport','Lv3Effects','Lv4Percent','CommerceConvergence')
@contextmanager
def history():
 original={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in FILES}
 read,execute,load=Path.read_text,TrackedLua51.execute,Context.load
 hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in original.items()}
 def source(p,*a,**kw):return original[p]if p in original else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 def module(c,name):
  p=ROOT/'Mod'/(name if name.endswith('.lua')else name+'.lua')
  if p not in original:return load(c,name)
  text=original[p];h=sha256(text.encode()).hexdigest();key=hashes[h];executed(key,h)
  try:out=c.lua.execute(text)
  except Exception:completion(key,False);raise
  completion(key,True);return out
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),patch.object(Context,'load',module),legacy_source_observation():yield


def retirement():
 c=Context();c.load('RuntimeWork');c.execute("""
 P={Field=function(t,k)return t and t[k]end};SPCRuntimeWork.StartRetirement(P,shared)
 calls=0
 function city(id)local c={owner=0,id=id,x=id,token='T'}
 function c:GetOwner()return self.owner end;function c:GetID()return self.id end
 function c:GetX()return self.x end;function c:GetY()return 1 end
 function c:GetProperty()return self.token end;return c end
 function clean()calls=calls+1;return 1 end
 function once(c,tag,fn)return SPCRuntimeWork.RetireOnce(P,shared,c,tag or 'test',fn or clean)end
 """);return c


def culture():
 with patch.object(aesthetic,'LuaRuntime',TrackedLua51),legacy_source_observation():
  if not hasattr(aesthetic.AestheticTests,'sql'):
   # This explicit engine copy already contains the configured SQL. Reapplying
   # the frozen non-idempotent initial schema would duplicate its bit rows.
   src=sqlite3.connect(external_database(ROOT).as_uri()+'?mode=ro',uri=True)
   aesthetic.AestheticTests.sql=sqlite3.connect(':memory:');src.backup(aesthetic.AestheticTests.sql);src.close()
  vm=aesthetic.AestheticTests().runtime()
 return vm


def convergence():
 c=Context();c.execute("""
 counts={reads=0,writes=0,references=0};present={};exits={};reference=true
 P={Field=function(t,k)return t and t[k]end,IsTestPlayer=function(pid)return pid==0 end,
 Info=function(_,name)return {Index=name,InternalOnly=1}end,
 HasBuilding=function(b,id)counts.reads=counts.reads+1;if unknown==id then return nil end;return present[id]==true end,
 RemoveBuilding=function(b,id)counts.writes=counts.writes+1;if failure~=id then present[id]=nil end end}
 a={owner=0,id=1,x=10,token='T'}
 function a:GetOwner()return self.owner end;function a:GetID()return self.id end
 function a:GetX()return self.x end;function a:GetY()return 20 end
 function a:GetProperty()return self.token end;function a:GetBuildings()return {}end
 shared.CityProgressionStore={HistoricalReference=function(c)counts.references=counts.references+1;return reference end,
 RegisterExit=function(name,fn)exits[name]=fn end,RemoveOwned=function(c,loss,ids)
 assert(c==a and loss==proof,'WRONG_EXIT');exitNames=ids
 for _,id in ipairs(ids)do if present[id]then P.RemoveBuilding({},id)end end end}
 Players={[0]={GetCities=function()return {Members=function()return ipairs({a})end}end}}
 """);c.load('RuntimeWork');c.execute('SPCRuntimeWork.StartRetirement(P,shared)');c.load('CommerceConvergence');c.execute("SPCCommerceConvergence.Start(P,shared,{retired=true});d=shared.CommerceConvergence")
 return c


class Registry(unittest.TestCase):
 def test_exact_legacy_groups_are_detached_and_data_only(self):
  c=Context();c.execute("Players=setmetatable({},{__index=function()error('NATIVE_READ')end})");c.load('Tombstones')
  expected={
   'ResearchCross':['BUILDING_SPC_DEV_LV3_POP_RESEARCH_'+str(i)for i in range(8)]+['BUILDING_SPC_B082_DISTRICT_'+s for s in ('03','05','1')],
   'ResearchInfrastructure':['BUILDING_SPC_LV4_PERCENT_RESEARCH_'+str(i)for i in range(8)]+['BUILDING_SPC_B051_SCIENCE_'+s+'_'+str(i)for s in ('POS','NEG','POP')for i in range(8 if s=='POP'else 16)],
   'SpecialistSupport':['BUILDING_SPC_DEV_LV3_'+s for s in ('RESEARCH','CULTURE','COMMERCE','INDUSTRY')]+['BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_'+str(i)for i in range(8)],
   'Lv3Culture':['BUILDING_SPC_DEV_LV3_POP_CULTURE_'+str(i)for i in range(8)],
   'Lv4Culture':['BUILDING_SPC_LV4_PERCENT_CULTURE_'+str(i)for i in range(8)],
   'CommerceConvergence':['BUILDING_SPC_B061_'+s+'_'+str(i)for s in ('SCIENCE','CULTURE','PRODUCTION')for i in range(16)]}
  for group,names in expected.items():
   self.assertEqual(list(c.globals().SPCTombstones.Names(group).values()),names)
   c.execute("local x=SPCTombstones.Names(...);x[1]='CORRUPT'",group)
   self.assertEqual(list(c.globals().SPCTombstones.Names(group).values()),names)
  self.assertEqual(sum(map(len,expected.values())),135)
  c.execute("assert(Events.LoadScreenClose.Count()==0 and Events.CityRemovedFromMap.Count()==0 and not pcall(SPCTombstones.Names,'UNKNOWN'))")
 def test_readonly_engine_copy_preserves_live_SQL_and_exact_cleanup_targets(self):
  c=Context();c.load('Tombstones');src=sqlite3.connect(external_database(ROOT).as_uri()+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');src.backup(db);src.close()
  groups={};allnames=[]
  for group in ('ResearchCross','ResearchInfrastructure','SpecialistSupport','Lv3Culture','Lv4Culture','CommerceConvergence'):
   names=list(c.globals().SPCTombstones.Names(group).values());allnames+=names;mods=0
   for name in names:
    self.assertEqual(db.execute('SELECT InternalOnly FROM Buildings WHERE BuildingType=?',(name,)).fetchone(),(1,))
    mods+=db.execute('SELECT count(*) FROM BuildingModifiers WHERE BuildingType=?',(name,)).fetchone()[0]
    for tab in ('Building_YieldChanges','Building_CitizenYieldChanges','Building_GreatPersonPoints'):
     self.assertEqual(db.execute('SELECT count(*) FROM '+tab+' WHERE BuildingType=?',(name,)).fetchone()[0],0)
   self.assertEqual(mods,48 if group=='CommerceConvergence'else 0);groups[group]={'rows':len(names),'modifier_links':mods}
  self.assertEqual(len(set(allnames)),135)
  self.assertEqual(subprocess.check_output(['git','diff','--name-only','--','Mod/Data'],cwd=ROOT,text=True),'')
  measure('S7e_registry_SQL',{'groups':groups,'inert_targets':87,'SQL_active_cleanup_targets':48,'SQL_modified':False,'native_cleanup':'USER_GAME_TEST_REQUIRED'})
  db.close()


class Retirement(unittest.TestCase):
 def test_false_is_not_a_success_marker_baseline_counterexample(self):
  for old in (True,False):
   with history()if old else nullcontext():c=retirement()
   c.execute("a=city(1);local ok,result=pcall(once,a,'test',function()calls=calls+1;return false end);firstOK=ok;firstResult=result;again=once(a)")
   self.assertEqual(c.eval('firstOK'),old)
   self.assertEqual(c.eval('again'),0 if old else 1)
   self.assertEqual(c.eval('calls'),1 if old else 2)
  measure('S7e_false_cleanup',{'before':'false callback cached as clean','after':'throws; next related attempt still runs'})
 def test_reference_change_or_load_inside_cleanup_never_publishes_success(self):
  for mutation in ("a.token='NEXT'","a.owner=1","a.id=2","a.x=90","Events.LoadScreenClose.Fire()"):
   c=retirement();c.execute("a=city(1);assert(not pcall(once,a,'test',function()"+mutation+";return 1 end));assert(shared.RuntimeRetirement.count==0);assert(once(a)==1)")
 def test_failure_after_native_effect_keeps_retry_and_successful_sibling_idle(self):
  c=retirement();c.execute("a=city(1);b=city(2);assert(once(b)==1);local present=true;assert(not pcall(once,a,'test',function()present=false;error('AFTER_REMOVE')end));assert(not present and once(b)==0);assert(once(a)==1 and shared.RuntimeRetirement.count==2)")
 def test_capacity_boundary_has_no_eviction_and_load_resets(self):
  c=retirement();c.execute("for i=1,2047 do once(city(i))end;assert(shared.RuntimeRetirement.count==2047);once(city(2048));assert(shared.RuntimeRetirement.count==2048);assert(not pcall(once,city(2049)));assert(once(city(1))==0);Events.LoadScreenClose.Fire();assert(shared.RuntimeRetirement.count==0 and once(city(2049))==1)")
 def test_tag_and_owner_index_limits_do_not_silently_drop_safety(self):
  c=retirement();c.execute("for t=1,4 do for i=1,2048 do once(city(i),'tag'..t)end end;assert(shared.RuntimeRetirement.count==8192);assert(not pcall(once,city(1),'overflow'));Events.CityRemovedFromMap.Fire(0,1);assert(shared.RuntimeRetirement.count==8188);assert(once(city(1),'overflow')==1)")


class Cross(unittest.TestCase):
 def test_actual_writer_skips_only_retired_reads_current_bits_and_amount_stay_fresh(self):
  results=[]
  for old in (True,False):
   with history()if old else nullcontext():vm=actual_cross()
   vm.execute("""
   oldReads,currentReads=0,0;local has=P.HasBuilding;local retired={}
   for _,name in ipairs(SPCResearchCross.Retired)do retired[P.Info('Buildings',name).Index]=true end
   P.HasBuilding=function(b,id)if retired[id]then oldReads=oldReads+1 else currentReads=currentReads+1 end;return has(b,id)end
   local before=writes;for i=1,20 do d.Audit({player=0,city=1});assert(not d.errors[0][1])end;assert(writes==before)
   """)
   results.append({'old':vm.eval('oldReads'),'current':vm.eval('currentReads'),'amount':vm.eval('d.plans[0][1].science')})
  self.assertEqual(results[0]['old'],220);self.assertEqual(results[1]['old'],0)
  self.assertEqual(results[0]['current'],results[1]['current']);self.assertGreater(results[1]['current'],0);self.assertEqual(results[0]['amount'],results[1]['amount'])
  measure('S7e_Cross_twenty_audits',{'before':results[0],'after':results[1],'active_scans_preserved':True})
 def test_actual_writer_unknown_cleanup_blocks_positive_then_exact_retry_and_readonly_report(self):
  vm=actual_cross();vm.execute("""
  local c=cities[1];shared.RuntimeRetirementCache={};local old=SPCResearchCross.Retired[1];local id=P.Info('Buildings',old).Index
  c.built[id]=true;local has=P.HasBuilding;P.HasBuilding=function(b,n)if n==id then return nil end;return has(b,n)end
  local before=writes;d.Audit({player=0,city=1});assert(d.errors[0][1]and c.built[id]and writes==before)
  P.HasBuilding=has;d.Audit({player=0,city=1});assert(not d.errors[0][1]and not c.built[id]);before=writes
  c.built[id]=true;local report=d.Describe(0,c);assert(report:find('残留 1')and writes==before)
  """)


class Culture(unittest.TestCase):
 def test_actual_aesthetic_legacy_reads_zero_after_warm_values_and_current_health_preserved(self):
  results=[]
  for old in (True,False):
   with history()if old else nullcontext():vm=culture()
   vm.execute("""
   oldReads=0;local has=P.HasBuilding;local old={}
   for bit=0,7 do for _,prefix in ipairs({'BUILDING_SPC_DEV_LV3_POP_CULTURE_','BUILDING_SPC_LV4_PERCENT_CULTURE_'})do old[GameInfo.Buildings[prefix..bit].Index]=true end end
   P.HasBuilding=function(b,id)if old[id]then oldReads=oldReads+1 end;return has(b,id)end
   local before=writes;for i=1,20 do one();assert(not data.errors['0:1'])end;assert(writes==before)
   """)
   results.append({'legacy':vm.eval('oldReads'),'total':vm.eval('total(a)')})
  self.assertEqual(results,[{'legacy':320,'total':12},{'legacy':0,'total':12}])
  measure('S7e_Aesthetic_twenty_audits',{'before':results[0],'after':results[1]})
 def test_partial_legacy_failure_stays_blocked_without_repeating_successful_sibling(self):
  vm=culture();vm.execute("""
  shared.RuntimeRetirementCache={};local iii=GameInfo.Buildings.BUILDING_SPC_DEV_LV3_POP_CULTURE_0.Index
  local iv=GameInfo.Buildings.BUILDING_SPC_LV4_PERCENT_CULTURE_0.Index
  a.present[iii]=true;a.present[iv]=true;failRemove=iv;one()
  assert(not a.present[iii]and a.present[iv]and total(a)==0 and data.errors['0:1'])
  local has=P.HasBuilding;local readsIII=0;P.HasBuilding=function(b,id)if id==iii then readsIII=readsIII+1 end;return has(b,id)end
  failRemove=nil;one();assert(not a.present[iv]and readsIII==0 and total(a)==12 and not data.errors['0:1'])
  a.active=2;one();assert(total(a)==0);a.active=3;one();assert(total(a)==12)
  """)


class Convergence(unittest.TestCase):
 def test_retired_48_read_hotpath_has_fresh_historical_proof_even_on_hit(self):
  results=[]
  for old in (True,False):
   with history()if old else nullcontext():c=convergence()
   c.execute("""
   assert(d.Withdraw(a));counts.reads=0;counts.references=0
   for i=1,20 do assert(d.Withdraw(a))end
   reference=false;assert(not pcall(d.Withdraw,a));assert(counts.references==21)
   """)
   results.append(c.eval('counts.reads'))
  self.assertEqual(results,[960,0]);measure('S7e_Convergence_twenty_withdrawals',{'before_presence':960,'after_presence':0,'historical_proof_calls_each':21})
 def test_failed_presence_and_removal_do_not_publish_clean_and_exit_never_uses_cache(self):
  c=convergence();c.execute("""
  local id='BUILDING_SPC_B061_SCIENCE_0';present[id]=true;unknown=id
  assert(not pcall(d.Withdraw,a)and present[id]and counts.writes==0)
  unknown=nil;failure=id;assert(not pcall(d.Withdraw,a)and present[id]);failure=nil;assert(d.Withdraw(a)and not present[id])
  present[id]=true;a.owner=9;proof={confirmed=true};exits.CommerceConvergence(a,proof)
  assert(not present[id]and #exitNames==48 and d.writes==1)
  """)
 def test_same_turn_changed_reference_forces_recheck_and_foreign_direct_call_rejected(self):
  c=convergence();c.execute("""
  d.Withdraw(a);counts.reads=0;a.token='NEW';d.Withdraw(a);assert(counts.reads==48)
  a.x=11;d.Withdraw(a);assert(counts.reads==96)
  a.owner=9;assert(not pcall(d.Withdraw,a)and counts.reads==96)
  """)
 def test_start_failure_skips_new_real_dependencies_without_changing_order(self):
  c=startup();include=c.globals().include
  def injected(name):
   out=include(name)
   if name=='RuntimeWork':c.execute("local start=SPCRuntimeWork.StartRetirement;SPCRuntimeWork.StartRetirement=function(...)start(...);error('OWNER_FAILED')end")
   return out
  c.globals().include=injected;c.load('Gameplay')
  c.execute("local s=ExposedMembers.SPC_P0;for _,n in ipairs({'ResearchCross','Lv4Percent','CommerceConvergence','CultureAesthetic'})do assert(s.StartStatus[n].state=='SKIPPED_DEPENDENCY',n)end;assert(s.StartStatus.NetworkBridge.state=='OK'and not s.RuntimeRetirement)")

if __name__=='__main__':unittest.main()
