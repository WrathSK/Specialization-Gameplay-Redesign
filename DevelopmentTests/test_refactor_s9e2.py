"""R15 real C2 producers/consumers and bounded scalar sampling; native APIs are doubles."""
from contextlib import nullcontext,contextmanager
from pathlib import Path
from hashlib import sha256
from unittest.mock import patch
import subprocess
import unittest
from refactor_harness import Context,ROOT,measure,TrackedLua51,SOURCES
from test_refactor_s4a import industry,load_industry_ui
from test_refactor_s5d1 import cross


ADAPT=r"""
function nativeEvent(name,...)
 local callbacks={};for i,f in ipairs(hooks[name]or {})do callbacks[i]=f end
 for _,f in ipairs(callbacks)do f(...)end
end
fullEnumerations,findReads,adjReads=0,0,0
local get=Players[0].GetDistricts
Players[0].GetDistricts=function()
 local ds=get();local members=ds.Members
 ds.Members=function(...)fullEnumerations=fullEnumerations+1;return members(...)end
 ds.FindID=function(_,id)findReads=findReads+1;return districts[id]end
 return ds
end
local dirs={{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}}
Map.GetAdjacentPlot=function(x,y,dir)
 local v=dirs[dir+1];local a,b=x+v[1],y+v[2]
 if a<0 or b<0 then return nil end
 return {GetX=function()return a end,GetY=function()return b end}
end
local plot=Map.GetPlot
Map.GetPlot=function(x,y)
 local p=plot(x,y);local read=p.GetAdjacencyYield
 p.GetAdjacencyYield=function(...)
  adjReads=adjReads+1
  if duringAdjacency then duringAdjacency(x,y)end
  return read(...)
 end
 return p
end
function addIndustry(cid,did)
 local c={id=cid,owner=0,pop=3,token='CITY'..cid,built={}};cities[cid]=c
 function c:GetID()return self.id end;function c:GetOwner()return self.owner end
 function c:GetX()return cid end;function c:GetY()return 1 end
 function c:GetPopulation()return self.pop end;function c:GetProperty()return self.token end
 function c:GetBuildings()return self.built end;function c:GetBuildQueue()return self.built end
 facts[cid]={specialization='INDUSTRY',potential=4,active=4,first={districtID=did,type='DISTRICT_INDUSTRIAL_ZONE'}}
 local x=district(did,cid,'DISTRICT_INDUSTRIAL_ZONE',7);x.IsPillaged=function()return false end
 return c
end
"""


def real_industry(many=0):
 vm=industry(with_depth=True);vm.execute(ADAPT)
 for i in range(3,3+many):vm.execute('addIndustry(...)',i,i*20)
 load_industry_ui(vm)
 vm.execute("pulse(2);audits={};actualAudits=0;local observe=P.Observe;P.Observe=function(kind,name)if kind=='audit'and name=='IndustrySupport'then actualAudits=actualAudits+1 end;if observe then return observe(kind,name)end end;local audit=d.Audit;d.Audit=function(scope)audits[#audits+1]=scope or {};return audit(scope)end")
 return vm


@contextmanager
def baseline_industry():
 paths=('SampleLifecycle','IndustrySupport','UI/IndustryRefresh')
 old={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','4bcee9e:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in paths}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(text.encode()).hexdigest():'historical/4bcee9e/'+str(path.relative_to(ROOT))for path,text in old.items()}
 def run(vm,text,*args,**kw):
  h=sha256(text.encode()if isinstance(text,str)else text).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,text,*args,**kw)
 with patch.object(Path,'read_text',lambda p,*a,**kw:old[p]if p in old else read(p,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield


class Workload(unittest.TestCase):
 def test_remote_AI_plot_burst_zero_local_sampling_or_consumer_work(self):
  values=[]
  for old in (True,False):
   with baseline_industry()if old else nullcontext():vm=real_industry(8)
   vm.execute("""
   local a,e,f=adjReads,fullEnumerations,findReads
   for i=1,100 do nativeEvent('ImprovementAddedToMap',10000+i,100,7,9);pulse(2)end
   result={adj=adjReads-a,enumerations=fullEnumerations-e,finds=findReads-f,audits=actualAudits}
   """)
   values.append(dict(vm.globals().result))
  self.assertGreater(values[0]['adj'],0);self.assertGreater(values[0]['audits'],0)
  self.assertEqual(values[1],dict(adj=0,enumerations=0,finds=0,audits=0))
  measure('S9e2_remote_AI_plots',{'baseline':'B372','cities':10,'events':100,'before':values[0],'after':values[1],'scope':'actual Industry UI+Gameplay pipeline; native mocks,not CPU/heap'})
 def test_single_relevant_foreign_plot_rereads_one_zone_and_one_consumer(self):
  vm=real_industry(8);vm.execute("""
  local a,e,f=adjReads,fullEnumerations,findReads;local n=sends
  districts[12].base=9;nativeEvent('ImprovementAddedToMap',13,1,7,9);pulse(2)
  assert(adjReads-a==1 and findReads-f==1 and #audits==1 and audits[1].city==2)
  assert(sends==n+1 and d.ReadBase(0,cities[2])==9)
  result={adj=adjReads-a,gameplay_validation_census=fullEnumerations-e,finds=findReads-f,consumer_audits=#audits}
  """)
  measure('S9e2_scoped_adjacency_change',dict(vm.globals().result))
 def test_equal_sample_sends_nothing_and_unchanged_idle_no_reads(self):
  vm=real_industry(8);vm.execute("""
  local a,e,f,n=adjReads,fullEnumerations,findReads,sends
  nativeEvent('FeatureRemovedFromMap',13,1);pulse(2)
  assert(adjReads==a+1 and fullEnumerations==e and findReads==f+1 and sends==n and #audits==0)
  a=adjReads;f=findReads;for i=1,1000 do pulse()end
  assert(adjReads==a and fullEnumerations==e and findReads==f and sends==n and #audits==0)
  """)
 def test_carrier_UI_write_revision_alone_does_not_recollect(self):
  vm=real_industry(8);vm.execute("local a,e=adjReads,fullEnumerations;ExposedMembers.SPC_RuntimeUIRevision=9000;pulse(20);assert(adjReads==a and fullEnumerations==e and #audits==0)")
 def test_own_qualification_cause_recovers_changed_token_without_global_UI_revision(self):
  vm=real_industry();vm.execute("""
  cities[2].token='NEW';local rev=ExposedMembers.SPC_RuntimeUIRevision;d.MarkCity(cities[2]);pulse(3)
  assert(d.ReadBase(0,cities[2])==6 and not d.errors['0:2']and ExposedMembers.SPC_RuntimeUIRevision==rev)
  """)
 def test_reentry_cause_is_not_lost_or_published_from_old_capture(self):
  vm=real_industry();vm.execute("""
  local n=sends;local once=true
  duringAdjacency=function(x,y)if once then once=false;districts[12].base=10;nativeEvent('ImprovementChanged',13,1,7,9,0,false,false)end end
  districts[12].base=8;nativeEvent('FeatureRemovedFromMap',13,1);pulse()
  assert(not once and sends==n);duringAdjacency=nil;pulse(2)
  assert(sends==n+1 and d.ReadBase(0,cities[2])==10)
  """)
 def test_state_change_pillage_notification_reads_native_value_without_assumption(self):
  vm=real_industry();vm.execute("districts[12].base=2;nativeEvent('ImprovementChanged',13,1,7,9,0,true,false);pulse(2);assert(d.ReadBase(0,cities[2])==2 and #audits==1)")
 def test_foreign_district_geometry_is_scoped_and_foreign_governor_is_ignored(self):
  vm=real_industry(3);vm.execute("""
  local a=adjReads;nativeEvent('GovernorPromoted',9);pulse(2);assert(adjReads==a)
  nativeEvent('DistrictAddedToMap',9,900,10,10000,10000,1);pulse(2);assert(adjReads==a)
  districts[12].base=7;nativeEvent('DistrictAddedToMap',9,901,10,13,1,1);pulse(2)
  assert(adjReads==a+1 and d.ReadBase(0,cities[2])==7)
  """)
 def test_full_turn_and_load_keep_safety_and_reset_reference_workset(self):
  vm=real_industry();vm.execute("""
  local a,n=adjReads,sends;turn=2;pulse(2);assert(adjReads>a and sends==n+1)
  local old=clone(queue[#queue]);local generation=d.generation
  nativeEvent('LoadScreenClose');pulse(3);assert(d.generation>generation)
  local before=writes;d.Receive(0,old);assert(writes==before)
  """)
 def test_unavailable_equal_recovery_and_two_same_turn_changes_remain(self):
  vm=real_industry();vm.execute("""
  unavailable=true;nativeEvent('ImprovementChanged',13,1);pulse(2);assert(d.responses[0].status=='UNAVAILABLE')
  factUnknown=true;d.Audit({player=0,city=2});local a=adjReads
  for i=1,1000 do pulse()end;assert(adjReads==a)
  unavailable=false;factUnknown=false;nativeEvent('ImprovementChanged',13,1);pulse(3)
  assert(not d.errors['0:2']and d.ReadBase(0,cities[2])==6)
  districts[12].base=7;nativeEvent('ImprovementChanged',13,1);pulse(2)
  districts[12].base=9;nativeEvent('ImprovementChanged',13,1);pulse(2)
  assert(d.ReadBase(0,cities[2])==9 and turn==1)
  """)

 def test_qualified_cause_during_native_read_supersedes_old_result(self):
  vm=real_industry();vm.execute("""
  local n=sends;local once=true
  duringAdjacency=function()if once then once=false;d.MarkCity(cities[2])end end
  districts[12].base=8;nativeEvent('ImprovementChanged',13,1);pulse()
  assert(not once and sends==n);duringAdjacency=nil;pulse(2)
  assert(sends==n+1 and d.ReadBase(0,cities[2])==8)
  """)
 def test_busy_receiver_merges_only_two_changed_cities(self):
  vm=real_industry(2);vm.execute("""
  d.busy=true;districts[12].base=7;nativeEvent('ImprovementChanged',13,1);pulse(2)
  districts[60].base=9;nativeEvent('ImprovementChanged',61,1);pulse(2)
  assert(#audits==0);d.busy=false;pulse()
  assert(#audits==2 and audits[1].city~=audits[2].city)
  for _,scope in ipairs(audits)do assert(scope.city==2 or scope.city==3)end
  assert(d.ReadBase(0,cities[2])==7 and d.ReadBase(0,cities[3])==9)
  """)
 def test_pending_transport_retries_do_not_repeat_native_sampling(self):
  vm=real_industry();vm.execute("""
  sync=false;districts[12].base=8;nativeEvent('ImprovementChanged',13,1);pulse()
  local a,e,f,n=adjReads,fullEnumerations,findReads,sends
  for i=1,20 do tick(6);pulse(5)end
  assert(adjReads==a and fullEnumerations==e and findReads==f and sends==n+2)
  """)


class Mechanism(unittest.TestCase):
 def test_default_reference_arity_remains_one(self):
  vm=real_industry();vm.execute("assert(select('#',SPCSampleLifecycle.Reference(cities[2],districts[12],P.Info('Districts',districts[12]:GetType())))==1)")
 def test_geometry_wrap_uses_native_ring_and_missing_API_degrades_conservatively(self):
  vm=real_industry();vm.execute("""
  Map.GetAdjacentPlot=function(x,y,dir)if dir==0 then return {GetX=function()return 100 end,GetY=function()return 1 end}end end
  nativeEvent('LoadScreenClose');pulse(2);local a=adjReads
  districts[12].base=8;nativeEvent('ImprovementChanged',100,1);pulse(2);assert(adjReads==a+1 and d.ReadBase(0,cities[2])==8)
  Map.GetAdjacentPlot=nil;nativeEvent('LoadScreenClose');pulse(2);a=adjReads
  nativeEvent('ImprovementChanged',10000,100);pulse(2);assert(adjReads>a)
  """)
 def test_capacity_limit_never_sends_partial_sample_and_recovery_needs_new_cause(self):
  c=Context();c.load('SampleLifecycle');c.execute("""
  P={Count=function()end};calls=0;local live=SPCSampleLifecycle.Live
  SPCSampleLifecycle.Live=function()local t={};for i=1,513 do t[i]={cityID=i,id=i,type='X',reference='R',x=i,y=1}end;return t end
  local s=SPCSampleLifecycle.Sampler(P,true,function()calls=calls+1;return 'ROW'end,60000)
  local valid,rows,n=s.Read(0);assert(valid==false and #rows==0 and n==0)
  local before=calls;for i=1,1000 do assert(s.Read(0)==false)end;assert(calls==before)
  SPCSampleLifecycle.Live=function()return {}end;s.All();assert(s.Read(0)==true)
  """)
 def test_snapshot_contains_only_scalars_no_native_objects_after_read(self):
  vm=real_industry();vm.execute("""
  local wire;local s=SPCSampleLifecycle.Sampler(P,true,function(pid,r)return 'X'end,60000)
  local valid,rows,n=s.Read(0);assert(valid and n==1);for _,v in pairs(rows)do assert(type(v)=='string')end
  local a=adjReads;for i=1,100 do assert(s.Read(0))end;assert(adjReads==a)
  """)

 def test_reset_during_capture_rejects_prior_lifetime_even_equal_serial(self):
  c=Context();c.load('SampleLifecycle');c.execute("""
  P={Count=function()end};SPCSampleLifecycle.Live=function()return {A={cityID=1,id=1,type='X',reference='R',x=1,y=1}}end
  local s;local once=true;s=SPCSampleLifecycle.Sampler(P,true,function()if once then once=false;s.Reset()end;return 'ROW'end,60000)
  local value=s.Read(0);assert(value==nil and s.Pending());assert(s.Read(0)==true)
  """)


class Cross(unittest.TestCase):
 def test_real_cross_UI_uses_same_ring_filter_and_scoped_native_values(self):
  vm=cross();vm.execute(ADAPT)
  vm.execute("""
  nativeEvent('LoadScreenClose');pulse(2);local a,e,n=adjReads,fullEnumerations,sends
  for i=1,100 do nativeEvent('ImprovementAddedToMap',10000+i,100,7,9);pulse()end
  assert(adjReads==a and fullEnumerations==e and sends==n)
  districts[13].base=10;nativeEvent('ImprovementChanged',14,1,7,9);pulse(2)
  assert(adjReads-a==6 and sends==n+1) -- only theater13 is in the native ring of14
  assert(d.samples[0].rows['1:13'].yields.CULTURE==10)
  """)

 def test_equal_reliable_cross_sample_retries_only_failed_consumer_city(self):
  vm=cross();vm.execute(ADAPT);vm.execute("""
  nativeEvent('LoadScreenClose');pulse(2)
  unavailable=true;nativeEvent('ImprovementChanged',14,1);pulse(3)
  assert(d.responses[0].status=='UNAVAILABLE')
  local calls={};local audit=d.Audit;d.errors[0][1]='SAMPLE_PENDING'
  d.Audit=function(scope)calls[#calls+1]=scope.city;return audit(scope)end
  unavailable=false;nativeEvent('ImprovementChanged',14,1);pulse(3)
  assert(d.responses[0].status=='UNCHANGED'and #calls==1 and calls[1]==1 and not d.errors[0][1])
  """)


class FactCause(unittest.TestCase):
 def test_real_binding_notifies_only_declared_work_and_retains_original_audit_on_notify_failure(self):
  from test_refactor_s5c1 import depth
  c=depth();c.load('FactConsumerBindings');c.execute("""
  SPCFactConsumerBindings.New(shared);wakes=0;audits=0
  shared.ResearchCross={SampleChanged=function()wakes=wakes+1;if notifyFailed then error('FAULT')end end,
   Audit=function(scope)audits=audits+1;assert(scope.player==0 and scope.city==1)end}
  d.MarkDirty(0,1);fc.Flush();shared.FactBindings.Flush();assert(wakes==1 and audits==1)
  for i=1,1000 do publish()end;assert(wakes==1 and audits==1)
  notifyFailed=true;d.MarkDirty(0,1);fc.Flush();shared.FactBindings.Flush()
  assert(wakes==2 and audits==2 and shared.FactBindings.errors.ResearchCross)
  """)

if __name__=='__main__':unittest.main()
