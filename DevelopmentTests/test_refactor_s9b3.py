"""Gameplay selects the Expedition entry; UI keeps exact native helper binding."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,Context,TrackedLua51,SOURCES,legacy_source_observation,measure
import test_expedition_gate as native
import test_expedition_spy_gate as spy
import test_expedition_missions as missions
import test_expedition_native_state_trace as trace
import test_expedition_spy_relocation_ui as relocation
import test_expedition_spy_selection_ui as selection

BASE='b2dd3d0'
@contextmanager
def before():
 paths={ROOT/'Mod'/p:subprocess.check_output(['git','show',BASE+':Mod/'+p],cwd=ROOT,text=True)for p in ('ExpeditionSpyGate.lua','ExpeditionSpyRead.lua')}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in paths.items()}
 def source(p,*a,**kw):return paths[p]if p in paths else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield
@contextmanager
def profile():
 def quiet(*a,**kw):
  vm=TrackedLua51(*a,**kw);vm.globals().print=lambda *parts:None
  vm.execute("local old=load;load=function(s,name,mode,env)if type(s)~='string'then return old(s,name)end;local f,e=loadstring(s,name);if f and env then setfenv(f,env)end;return f,e end")
  return vm
 with patch.object(native,'LuaRuntime',quiet),legacy_source_observation():yield

def runtime():
 with profile():v=spy.gate(ui=True)
 v.globals().print=lambda *a:None
 v.execute("""
 memberReads,visibilityReads,distanceReads=0,0,0;reveals={};rows={targetCity}
 Players[3].GetCities=function()return targetCities end
 local oldMembers=targetCities.Members
 targetCities.Members=function()memberReads=memberReads+1;return ipairs(rows)end
 function foreign(id,x,y,owner)
  local c={id=id,x=x,y=y,owner=owner or 3}
  function c:GetID()return self.id end;function c:GetOwner()return self.owner end
  function c:GetX()return self.x end;function c:GetY()return self.y end
  rows[#rows+1]=c;return c
 end
 function reveal(c,yes)reveals[c:GetX()..':'..c:GetY()]=yes end
 PlayersVisibility[2].IsRevealed=function(_,x,y)visibilityReads=visibilityReads+1;return reveals[x..':'..y]==true end
 function chosen()
  local c=reader.Entry(2,3,targetCity);return c and c:GetID()or -1
 end
 function counters()return memberReads,visibilityReads,distanceReads end
 """)
 return v

class Policy(unittest.TestCase):
 def test_actual_before_after_direct_nearest_tie_order_and_fallback_match(self):
  cases=("reveal(targetCity,true)","local a=foreign(11,18,8);reveal(a,true)","local a=foreign(11,18,8);local b=foreign(10,12,8);reveal(a,true);reveal(b,true)","local a=foreign(11,18,8);local b=foreign(10,12,8);reveal(a,true);reveal(b,true);rows={b,a,targetCity}","local a=foreign(11,18,8);local b=foreign(10,12,8);reveal(a,true);reveal(b,true);Map.GetPlotDistance=function(x)distanceReads=distanceReads+1;return x==18 and 1 or 8 end", "local a=foreign(11,18,8);reveal(a,true);Map.GetPlotDistance=function()distanceReads=distanceReads+1;return nil end", "local a=foreign(11,18,8);reveal(a,true);Map.GetPlotDistance=function()distanceReads=distanceReads+1;return false end", "local a=foreign(11,18,8,4);reveal(a,true)", "")
  for setup in cases:
   results=[]
   for old in (True,False):
    with before()if old else nullcontext():v=runtime()
    v.execute(setup+'\nresult=chosen()')
    results.append((v.eval('result'),v.eval('memberReads'),v.eval('visibilityReads'),v.eval('distanceReads')))
   self.assertEqual(*results,setup)
  measure('S9b3_entry_differential',{'baseline':BASE,'cases':9,'same_entry_and_native_visibility_distance_enumerations':True,'native_helper_change':False})
 def test_fast_path_does_not_enumerate_and_tie_uses_smallest_id(self):
  v=runtime();v.execute("reveal(targetCity,true);targetCities.Members=function()error('DIRECT_MUST_NOT_ENUMERATE')end;assert(chosen()==9)")
  v=runtime();v.execute("local a=foreign(11,18,8);local b=foreign(10,12,8);reveal(a,true);reveal(b,true);assert(chosen()==10 and memberReads==1)")
 def test_raw_policy_is_pure_bounded_dense_and_preserves_zero_distance(self):
  c=Context();c.load('ExpeditionEntry');c.execute("""
  function row(id,x)return {owner=3,id=id,x=x,y=8,revealed=true}end
  local t=row(9,15);t.revealed=false
  raw={protocol=1,target=t,cities={row(11,18),row(10,12)}}
  local a=SPCExpeditionEntry.Select(raw);assert(a.id==10 and a~=raw.cities[2]);raw.cities[1].distance=0;assert(SPCExpeditionEntry.Select(raw).id==11)
  for _,bad in ipairs({{[2]=row(11,18)},{x=row(11,18)},{[4097]=row(11,18)},{row(11,18),row(11,19)}})do raw.cities=bad;assert(not pcall(SPCExpeditionEntry.Select,raw))end
  raw.cities={row(11,18)};for _,d in ipairs({'3',-1,math.huge,0/0})do raw.cities[1].distance=d;assert(not pcall(SPCExpeditionEntry.Select,raw))end
  raw.target.revealed=true;raw.cities=nil;assert(SPCExpeditionEntry.Select(raw).id==9)
  """)
 def test_Gameplay_rule_call_reads_no_store_native_city_or_state_and_does_not_reserve(self):
  v=runtime();v.execute("local raw={protocol=1,observer=2,turn=currentTurn,target={owner=3,id=9,x=15,y=8,revealed=true}};local writes=storeWrites;Game.GetProperty=function()error('NO_SAVE_READ')end;Players={};P.Info=function()error('NO_METADATA')end;for i=1,100 do assert(shared.ExpeditionGate.ChooseEntry(2,raw).id==9)end;assert(storeWrites==writes and nativeCalls==0)")
 def test_missing_rule_dependency_fails_start_before_store_or_native_work(self):
  v=runtime();v.execute("SPCExpeditionEntry=nil;assert(not pcall(SPCExpeditionSpyGate.Start,P,shared)and storeWrites==0 and nativeCalls==0)")
 def test_wrong_observer_turn_and_protocol_are_not_interpreted(self):
  for change in ('r.observer=3','r.turn=r.turn-1','r.protocol=2'):
   v=runtime();v.execute('local r={protocol=1,observer=2,turn=currentTurn,target={owner=3,id=9,x=15,y=8,revealed=true}};'+change+';assert(not pcall(shared.ExpeditionGate.ChooseEntry,2,r)and storeWrites==0 and nativeCalls==0)')

class Binding(unittest.TestCase):
 def test_unavailable_or_replaced_backend_never_runs_native_travel_helpers(self):
  v=runtime();v.execute("req('CREATE','a');local gate=shared.ExpeditionGate;reveal(targetCity,true);local old=gate.ChooseEntry;gate.ChooseEntry=function(...)local r=old(...);ExposedMembers.SPC_P0.ExpeditionGate={ChooseEntry=old};return r end;local r=reader.Read(2,40,target);assert(r.status~='READ_OK'and nativeCalls==0);ExposedMembers.SPC_P0.ExpeditionGate=nil;assert(reader.Target(2,3,9)==nil)")
 def test_current_reference_or_turn_change_during_rule_call_rejects_sample(self):
  for change in ('currentTurn=currentTurn+1','targetCity.x=targetCity.x+1','targetCity.owner=4'):
   v=runtime();v.execute("reveal(targetCity,true);local gate=shared.ExpeditionGate;local old=gate.ChooseEntry;gate.ChooseEntry=function(...)local r=old(...);"+change+";return r end;assert(not pcall(chosen)and nativeCalls==0)")
 def test_selected_city_change_cannot_be_resolved_to_another_native_object(self):
  v=runtime();v.execute("local a=foreign(11,18,8);reveal(a,true);local gate=shared.ExpeditionGate;local old=gate.ChooseEntry;gate.ChooseEntry=function(...)local r=old(...);a.x=19;return r end;assert(not pcall(chosen)and nativeCalls==0)")
 def test_backend_replacement_from_final_native_reference_read_is_rejected_even_for_nil_choice(self):
  for revealed in ('true','false'):
   v=runtime();v.execute("reveal(targetCity,"+revealed+");local gate=shared.ExpeditionGate;local choose=gate.ChooseEntry;local x=targetCity.GetX;local armed=false;targetCity.GetX=function(c)if armed then ExposedMembers.SPC_P0.ExpeditionGate={ChooseEntry=choose}end;return x(c)end;gate.ChooseEntry=function(...)local r=choose(...);armed=true;return r end;assert(not pcall(chosen))")
 def test_real_Read_helpers_use_same_chosen_entry_and_do_not_submit(self):
  v=runtime();v.execute("req('CREATE','a');local a=foreign(11,18,8);reveal(a,true);helperOrder={};UnitManager.GetTravelTime=function(u,c)assert(c==a);helperOrder[#helperOrder+1]='TRAVEL';return 3 end;UnitManager.GetEstablishInCityTime=function(u,c)assert(c==a);helperOrder[#helperOrder+1]='ESTABLISH';return 1 end;UnitManager.CanStartOperation=function(u,op,plot,p)assert(plot.x==18 and p.X==18 and p.Y==8);helperOrder[#helperOrder+1]='ALLOWED';return true end;local r=reader.Read(2,40,target);assert(r.status=='READ_OK'and r.entryID==11 and r.entryX==18 and r.total==4 and table.concat(helperOrder,',')=='TRAVEL,ESTABLISH,ALLOWED'and nativeCalls==0)")
 def test_no_automatic_entry_sampling_or_irreversible_action_on_idle(self):
  with profile():v=relocation.created_window()
  v.execute("local old=shared.ExpeditionGate.ChooseEntry;entryCalls=0;shared.ExpeditionGate.ChooseEntry=function(...)entryCalls=entryCalls+1;return old(...)end;gateOpen('TRAVEL',40);chooseCity();local calls,w=entryCalls,storeWrites;assert(calls==3);for i=1,1000 do publish()end;assert(entryCalls==calls and storeWrites==w and nativeCalls==0 and properties==0)")
  measure('S9b3_work_scope',{'new_automatic_listeners':0,'direct_city_enumerations':0,'unrevealed_target_enumerations_before_after':[1,1],'extra_sync_rule_call_per_existing_Entry':1,'actual_window_open_and_selected_entry_calls':3,'thousand_idle_publish_extra_rule_calls':0,'save_schema_change':False,'no_replay':True,'new_all_candidates_dispatch_resample':False})


class Retained(unittest.TestCase):pass
for label,case in [('gate',spy.Gate),('reader',spy.Reader),('entry',missions.EntryTravel),('travel',trace.TravelAndArrival),('preview',relocation.PresentationBoundary),('selection',selection.Selection)]:
 for name in dir(case):
  if name.startswith('test_'):
   def run(self,case=case,name=name):
    with profile():getattr(case(),name)()
   setattr(Retained,'test_'+label+'_'+name.removeprefix('test_'),run)
del label,case,name

def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9b2'])])

if __name__=='__main__':unittest.main()
