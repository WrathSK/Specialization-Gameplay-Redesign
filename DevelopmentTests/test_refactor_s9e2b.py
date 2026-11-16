"""R15 actual cross-UI BASE Production reuse, with explicit native/write windows."""
from contextlib import nullcontext,contextmanager
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import subprocess
import unittest
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,measure
from test_refactor_s9e2 import cross,ADAPT


def cache():
 c=Context('UI');c.load('SampleLifecycle');c.execute("""
 P={VERSION='TEST',Count=function(k)counts[k]=(counts[k]or 0)+1 end}
 ExposedMembers.SPC_P0={Version=P.VERSION,IndustrySupport={ready=true,generation=1},ResearchCross={ready=true,generation=2}}
 ExposedMembers.SPC_C2_industry_generation=1;ExposedMembers.SPC_C2_cross_generation=2
 ExposedMembers.SPC_C2_industry_epoch=1;ExposedMembers.SPC_C2_cross_epoch=1
 r={cityID=1,id=11,type='DISTRICT_INDUSTRIAL_ZONE',reference='EXACT',x=1,y=1};native=0;value=7
 Map={};Map.GetPlot=function()return {GetAdjacencyYield=function()native=native+1;if onRead then onRead()end;if failure then error('UNKNOWN')end;return value end}end
 function read()return SPCSampleLifecycle.ReadBaseProduction(P,0,r,3,1,turn)end
 """);return c


@contextmanager
def baseline():
 paths=('SampleLifecycle','UI/IndustryRefresh','UI/ResearchCrossRefresh','PerformanceCounters')
 old={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','dc7b324:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in paths}
 previous,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(text.encode()).hexdigest():'historical/dc7b324/'+str(path.relative_to(ROOT))for path,text in old.items()}
 def run(vm,text,*a,**kw):
  h=sha256(text.encode()if isinstance(text,str)else text).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,text,*a,**kw)
 with patch.object(Path,'read_text',lambda p,*a,**kw:old[p]if p in old else previous(p,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield


def dual(reverse=False):
 vm=cross();vm.execute(ADAPT)
 # Use the real Probe factWrite boundary, with native-shaped queue/building doubles.
 c=Context();source=c.fragment('Mod/Probe.lua','local function factWrite(', '-- A live non-trader')
 vm.execute("""
 P.Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY'};P.Family=function(k)return P.Families[k]end
 for _,city in pairs(cities)do
  local b=city.built;b.CreateBuilding=function(_,id)b[id]=true;writes=writes+1 end
  b.RemoveBuilding=function(_,id)b[id]=nil;writes=writes+1 end
 end
 local old=Map.GetPlot
 production={[12]=6};productionReads=0
 Map.GetPlot=function(x,y)
  local plot=old(x,y);local read=plot.GetAdjacencyYield
  plot.GetAdjacencyYield=function(_,pid,cid,kind,yield)
   if yield=='PRODUCTION'then productionReads=productionReads+1;return production[x]or 0 end
   return read(plot,pid,cid,kind,yield)
  end;return plot
 end
 crossPublish=hooks.GameCoreEventPublishComplete[#hooks.GameCoreEventPublishComplete]
 crossTick=tick;crossInit=initUI
 """)
 vm.execute('local P=P\n'+source)
 vm.execute((ROOT/'Mod/IndustrySupport.lua').read_text())
 vm.execute("SPCIndustrySupport.Start(P,shared);ind=shared.IndustrySupport;ind.ready=true")
 vm.execute("""
 UI.RequestPlayerOperation=function(pid,op,p)
  sends=sends+1;queue[#queue+1]=p
  if p.Action=='INDUSTRY_BASE'then ind.Receive(pid,p)else shared.ResearchCross.Receive(pid,p)end
 end
 """)
 vm.execute((ROOT/'Mod/UI/IndustryRefresh.lua').read_text());vm.execute('initUI();pulse(4);industryPublish=hooks.GameCoreEventPublishComplete[#hooks.GameCoreEventPublishComplete]')
 if reverse:vm.execute("local list=hooks.GameCoreEventPublishComplete;local a,b;for i,f in ipairs(list)do if f==crossPublish then a=i elseif f==industryPublish then b=i end end;assert(a and b);list[a],list[b]=list[b],list[a]")
 vm.execute("""
 function state()
  local out={};for _,p in ipairs(queue)do out[#out+1]=p.Action..':'..p.Generation..':'..p.Valid..':'..p.Count..':'..p.Data end
  return table.concat(out,'|')
 end
 nativeEvent('LoadScreenClose');pulse(4);queue={}
 """)
 return vm


class Values(unittest.TestCase):
 def test_two_producers_reuse_one_value_within_exact_window(self):
  c=cache();c.execute("assert(read()==7 and read()==7 and native==1 and counts.adj_base_hit==1);assert(ExposedMembers.SPC_C2_BaseProduction.authority=='NATIVE_SAMPLE_ONLY')")
 def test_every_scalar_boundary_prevents_reuse(self):
  cases=("turn=2","r.reference='NEW'","r.id=12","r.cityID=2","r.x=2","r.type='OTHER'",
   "ExposedMembers.SPC_RuntimeUIRevision=1","ExposedMembers.SPC_P0.IndustrySupport.sampleRevision=1",
   "ExposedMembers.SPC_P0.ResearchCross.sampleRevision=1",
   "ExposedMembers.SPC_C2_industry_epoch=2","ExposedMembers.SPC_C2_cross_epoch=2",
   "ExposedMembers.SPC_C2_industry_generation=3;ExposedMembers.SPC_P0.IndustrySupport.generation=3",
   "ExposedMembers.SPC_C2_cross_generation=3;ExposedMembers.SPC_P0.ResearchCross.generation=3",
   "SPCSampleLifecycle.InvalidateBaseProduction()")
  for change in cases:
   with self.subTest(change=change):
    c=cache();c.execute("assert(read()==7);value=9;"+change+";assert(read()==9 and native==2)")
 def test_UNKNOWN_never_installed_and_no_replay(self):
  c=cache();c.execute("failure=true;assert(not pcall(read)and native==1);failure=false;value=9;assert(read()==9 and native==2);assert(read()==9 and native==2)")
 def test_nonfinite_native_values_never_cached(self):
  for value in ('0/0','math.huge','-math.huge'):
   c=cache();c.execute('value='+value+';read();read();assert(native==2)')
 def test_write_or_related_cause_during_native_read_does_not_install(self):
  for change in ('ExposedMembers.SPC_RuntimeUIRevision=1','SPCSampleLifecycle.InvalidateBaseProduction()','ExposedMembers.SPC_C2_BaseProduction=nil'):
   c=cache();c.execute("onRead=function()"+change+";end;assert(read()==7);onRead=nil;value=9;assert(read()==9 and native==2)")
 def test_missing_or_unready_other_producer_keeps_fresh_native_behavior(self):
  for change in ('ExposedMembers.SPC_C2_cross_epoch=nil','ExposedMembers.SPC_P0.ResearchCross=nil','ExposedMembers.SPC_P0.ResearchCross.ready=false'):
   c=cache();c.execute(change+';assert(read()==7);value=9;assert(read()==9 and native==2)')
 def test_capacity_fallback_never_rejects_or_discards_warm_entry(self):
  c=cache();c.execute("for i=1,513 do r.id=i;assert(read()==7)end;local data=ExposedMembers.SPC_C2_BaseProduction;assert(data.count==512 and native==513);r.id=1;assert(read()==7 and native==513);r.id=513;assert(read()==7 and native==514)")
 def test_text_capacity_is_not_a_gameplay_or_read_limit(self):
  c=cache();c.execute("r.reference=string.rep('X',262145);assert(read()==7);value=9;assert(read()==9 and native==2 and ExposedMembers.SPC_C2_BaseProduction.count==0)")
 def test_entry_is_scalar_only_and_reference_replacement_does_not_grow_history(self):
  c=cache();c.execute("for i=1,100 do r.reference='R'..i;read()end;local cache=ExposedMembers.SPC_C2_BaseProduction;assert(cache.count==1);for _,row in pairs(cache.rows)do for _,v in pairs(row)do assert(type(v)=='number'or type(v)=='string')end end")

 def test_nonscalar_native_metadata_never_enters_cache(self):
  c=cache();c.execute("""
  local nativeType={};local nativeYield={}
  assert(SPCSampleLifecycle.ReadBaseProduction(P,0,r,nativeType,nativeYield,turn)==7)
  assert(ExposedMembers.SPC_C2_BaseProduction==nil and native==1)
  """)


class ActualUI(unittest.TestCase):
 def test_real_two_UI_producers_same_C2_values_with_one_less_native_read(self):
  states=[];costs=[]
  for old in (True,False):
   with baseline()if old else nullcontext():vm=dual()
   vm.execute("local a=productionReads;districts[13].base=7;nativeEvent('ImprovementChanged',13,1,7,9);pulse(3);cost=productionReads-a;assert(#queue==1 and queue[1].Action=='RESEARCH_CROSS_SAMPLE');result=state()")
   costs.append(vm.eval('cost'));states.append(vm.eval('result'))
  self.assertEqual(states[0],states[1]);self.assertEqual(costs,[3,2])
  measure('S9e2b_actual_UI_BaseProduction',{'baseline':'B373','before_native_reads':3,'after_native_reads':2,'duplicate_industrial_reads_before':2,'after':1,'identical_C2_payloads':True,'native_CPU_heap_claim':False})
 def test_reverse_UI_delivery_also_reuses_native_value(self):
  vm=dual(True);vm.execute("local n=productionReads;nativeEvent('ImprovementChanged',13,1,7,9);pulse(3);assert(productionReads-n==2)")
 def test_real_Probe_write_barrier_requires_fresh_next_context(self):
  vm=dual(True);vm.execute("""
  local n=productionReads;local rev=ExposedMembers.SPC_RuntimeUIRevision
  production[12]=8;nativeEvent('ImprovementChanged',13,1,7,9);pulse(4)
  assert(ExposedMembers.SPC_RuntimeUIRevision>rev and productionReads-n==3)
  assert(ind.ReadBase(0,cities[2])==8 and shared.ResearchCross.samples[0].rows['2:12'].yields.PRODUCTION==8)
  """)
 def test_second_same_turn_change_and_idle_remain_fresh_and_bounded(self):
  vm=dual();vm.execute("""
  production[12]=8;nativeEvent('ImprovementChanged',13,1,7,9);pulse(4)
  production[12]=9;nativeEvent('ImprovementChanged',13,1,7,9);pulse(4)
  assert(ind.ReadBase(0,cities[2])==9 and shared.ResearchCross.samples[0].rows['2:12'].yields.PRODUCTION==9)
  local n=productionReads;for i=1,1000 do pulse()end;assert(productionReads==n and turn==1)
  """)
 def test_actual_UI_turn_change_during_read_never_retags_old_sample(self):
  vm=dual();vm.execute("""
  local n=sends;local once=true
  duringAdjacency=function()if once then once=false;turn=turn+1 end end
  nativeEvent('ImprovementChanged',13,1,7,9);pulse();duringAdjacency=nil;pulse(4)
  assert(not once and turn==2 and sends>n)
  for _,p in ipairs(queue)do assert(p.Turn==2)end
  """)

if __name__=='__main__':unittest.main()
