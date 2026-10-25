"""S7a5 sequential Industry carrier order and actual BASE sender/receiver regression."""
from contextlib import contextmanager,nullcontext
from pathlib import Path
from hashlib import sha256
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s7a1 import kernel
from test_refactor_s4a import industry,load_industry_ui


@contextmanager
def old_source():
    path=ROOT/'Mod/IndustrySupport.lua';source=subprocess.check_output(['git','show','6e8db27:Mod/IndustrySupport.lua'],cwd=ROOT,text=True)
    digest=sha256(source.encode()).hexdigest();previous=Path.read_text;execute=TrackedLua51.execute
    def read(p,*a,**kw):return source if p==path else previous(p,*a,**kw)
    def run(vm,text,*a,**kw):
        if isinstance(text,str)and sha256(text.encode()).hexdigest()==digest:SOURCES[digest]='historical/6e8db27/Mod/IndustrySupport.lua'
        return execute(vm,text,*a,**kw)
    with patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',run):
        with legacy_source_observation():yield


class Sequential(unittest.TestCase):
    def test_per_bit_read_write_readback_not_global_preflight_or_removal_partition(self):
        c=kernel();c.execute("state.C=true;set.ApplySequential(city,{[0]=true},health,function()changes=changes+1 end);assert(changes==2 and table.concat(trace,',')=='READ:ZERO,CREATE:ZERO,READ:ZERO,READ:B,READ:C,REMOVE:C,READ:C')")
    def test_late_unknown_does_not_erase_prior_confirmed_bit(self):
        c=kernel();c.execute("unknown='C';local ok,e=pcall(set.ApplySequential,city,{[0]=true,B=true},health,function()changes=changes+1 end);assert(not ok and e:find('READ_UNKNOWN')and changes==2 and state.ZERO and state.B)")
    def test_negative_key_descriptor_and_readonly_observe(self):
        c=kernel();c.execute("set=SPCCarrierSet.Define(P,{{key=-1,name='FOOD'},{key=0,name='PROD'}},function(n)return n end,{read='READ_UNKNOWN',write='WRITE_UNKNOWN'});set.ApplySequential(city,{[-1]=true,[0]=true},health,function()changes=changes+1 end);assert(changes==2 and state.FOOD and state.PROD);trace={};local p=set.Observe(city,{});assert(p[1].key==-1 and p[1].present and #trace==2)")
    def test_unconfirmed_write_and_throw_keep_original_stop_boundary(self):
        for inject in ("unconfirmed='B'","fail='B'"):
            c=kernel();c.execute(inject+";assert(not pcall(set.ApplySequential,city,{[0]=true,B=true,C=true},health,function()changes=changes+1 end));assert(changes==1 and state.ZERO and not state.C)")


class ActualIndustry(unittest.TestCase):
    def test_same_values_order_reads_writes_partial_policy_and_withdrawal(self):
        results=[]
        for old in (True,False):
            with old_source()if old else nullcontext():l=industry()
            l.execute("""
              trace={};local h,a,r=P.HasBuilding,P.CreateBuilding,P.RemoveBuilding
              P.HasBuilding=function(b,id)trace[#trace+1]='H:'..id;return h(b,id)end
              P.CreateBuilding=function(b,id)trace[#trace+1]='C:'..id;return a(b,id)end
              P.RemoveBuilding=function(b,id)trace[#trace+1]='R:'..id;return r(b,id)end
              function snap()local out={};for id,v in pairs(cities[2].built)do if v then out[#out+1]=id end end;table.sort(out);return table.concat(out,',')end
              snapshots={}
            """)
            load_industry_ui(l)
            l.execute("""
              snapshots[#snapshots+1]=snap();assert(d.ReadBase(0,cities[2])==6)
              for _,n in ipairs({0,255,1,4})do districts[12].base=n;fire('CityWorkerChanged');pulse(2);assert(d.ReadBase(0,cities[2])==n);snapshots[#snapshots+1]=snap()end
              facts[2].active=0;fire('GovernorChanged');pulse(2);snapshots[#snapshots+1]=snap();assert(not cities[2].built.BUILDING_SPC_DEV_INDUSTRY_LV1_2)
              local w=writes;for i=1,1000 do pulse()end;assert(writes==w)
            """)
            results.append({'state':list(l.globals().snapshots.values()),'calls':list(l.globals().trace.values()),'changes':l.eval('d.changes'),'writes':l.eval('writes'),'sends':l.eval('sends')})
        self.assertEqual(results[0],results[1]);measure('S7a5_Industry_differential',{'baseline':'6e8db27','BASE':[6,0,255,1,4],'same_values_native_calls_writes_changes_and_sends':True,'idle_extra_writes':0,'native_source':'actual IndustrySupport/IndustryRefresh/SampleLifecycle with native doubles'})


if __name__=='__main__':unittest.main()
