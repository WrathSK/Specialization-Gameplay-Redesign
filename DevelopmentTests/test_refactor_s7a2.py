"""S7a2 fresh changed-bit reads; original GPP source comparator and native doubles."""
import ast
import inspect
import subprocess
import unittest
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,measure
from test_refactor_s7a1 import kernel,owners,SourceSet


class GPPSource(SourceSet):
    def __truediv__(self,name):
        if name=='Lv2GPP.lua'and self.old:
            class File:
                def read_text(self):return subprocess.check_output(['git','show','d99a413:Mod/Lv2GPP.lua'],cwd=ROOT,text=True)
            return File()
        return super().__truediv__(name)


def fixture(old=False):
    import test_b270_event_scope as module
    previous=module.LuaRuntime;module.LuaRuntime=TrackedLua51
    try:
        with legacy_source_observation():l,_,_=module.make_fixture(0,True,mod=GPPSource(old),initial_load=False)
    finally:module.LuaRuntime=previous
    tree=ast.parse(inspect.getsource(owners));setup=next(node.value.args[0].value for node in ast.walk(tree)if isinstance(node,ast.Expr)and isinstance(node.value,ast.Call)and isinstance(node.value.func,ast.Attribute)and node.value.func.attr=='execute'and isinstance(node.value.args[0],ast.Constant))
    l.execute(setup);l.execute("""
      count=3;district.GetX=function()return 101 end;district.GetY=function()return 0 end
      Map={GetPlot=function()return {GetIndex=function()return 101 end,GetWorkerCount=function()return count end}end}
      shared.Lv2GPP.ready=true
      function gppAudit()shared.Lv2GPP.Audit({player=0,city=0});assert(not shared.Lv2GPP.errors['0:0'],shared.Lv2GPP.errors['0:0']);assert(not shared.Lv2GPP.auditError,shared.Lv2GPP.auditError)end
      function gpp()local n=0;for bit=0,7 do local id=P.Info('Buildings','BUILDING_SPC_DEV_GPP_RESEARCH_'..bit).Index;if c.values[id]then n=n+2*2^bit end end;return n end
    """);return l


class FreshMutation(unittest.TestCase):
    def test_fresh_prewrite_skips_reentrant_already_converged_bit(self):
        c=kernel();c.execute("state.B=true;local remove=health.Remove;health.Remove=function(city,id)remove(city,id);state.C=true end;set.Apply(city,{C=true},health,function()changes=changes+1 end,true);assert(changes==1 and state.C and not state.B);for _,v in ipairs(trace)do assert(v~='CREATE:C')end")
    def test_fresh_prewrite_unknown_preserves_prior_confirmed_changes(self):
        c=kernel();c.execute("state.B=true;local remove=health.Remove;health.Remove=function(city,id)remove(city,id);unknown='C'end;local ok,e=pcall(set.Apply,city,{C=true},health,function()changes=changes+1 end,true);assert(not ok and e:find('READ_UNKNOWN')and changes==1 and not state.C and not state.B)")
    def test_fresh_mode_checks_changed_bits_only_and_keeps_original_handle(self):
        c=kernel();c.execute("set.Apply(city,{B=true},health,function()changes=changes+1 end,true);assert(changes==1 and table.concat(trace,',')=='READ:ZERO,READ:B,READ:C,READ:B,CREATE:B,READ:B');trace={};set.Apply(city,{B=true},health,nil,true);assert(#trace==3)")


class RealGPP(unittest.TestCase):
    def test_frozen_source_identical_carriers_native_reads_write_order_and_counts(self):
        values=[]
        for old in (True,False):
            l=fixture(old);l.execute("result={};for _,n in ipairs({0,1,2,3,7,255,1})do count=n;gppAudit();assert(gpp()==2*n);result[#result+1]=snapshot()end;level=1;gppAudit();assert(gpp()==0);level=4;count=2;gppAudit();assert(gpp()==4);raw.pillaged=true;gppAudit();assert(gpp()==0);raw.pillaged=false;gppAudit();assert(gpp()==4);local n=#log;gppAudit();assert(#log==n)")
            values.append({'snapshots':list(l.globals().result.values()),'writes':list(l.globals().log.values()),'native_counts':dict(l.globals().counts),'changes':l.eval('shared.Lv2GPP.changes')})
        self.assertEqual(values[0],values[1]);measure('S7a2_GPP_differential',{'baseline':'d99a413','workers':[0,1,2,3,7,255,1],'same_native_presence_and_write_order':True,'same_confirmed_changes':True,'definition_lookup':'immutable indices resolved once after original schema validation; not a gameplay/native-point measurement'})
    def test_unknown_workers_all_bit_preflight_and_same_turn_recovery(self):
        l=fixture();l.execute("gppAudit();assert(gpp()==6);count=nil;local n=#log;shared.Lv2GPP.Audit({player=0,city=0});assert(#log==n and gpp()==6 and shared.Lv2GPP.errors['0:0']);count=2;gppAudit();assert(gpp()==4);local has=P.HasBuilding;P.HasBuilding=function(b,id)if names[id]=='BUILDING_SPC_DEV_GPP_COMMERCE_7'then return nil end;return has(b,id)end;count=7;local n=#log;shared.Lv2GPP.Audit({player=0,city=0});assert(#log==n and shared.Lv2GPP.errors['0:0']);P.HasBuilding=has;gppAudit();assert(gpp()==14)")
    def test_no_new_carrier_location_or_pillage_reads(self):
        l=fixture();l.execute("local get=c.GetBuildings;c.GetBuildings=function()local b=get();b.IsPillaged=function()error('NO_NEW_CARRIER_PILLAGE_POLICY')end;b.GetBuildingLocation=function()error('NO_NEW_CARRIER_LOCATION_POLICY')end;return b end;gppAudit();assert(gpp()==6)")


if __name__=='__main__':unittest.main()
