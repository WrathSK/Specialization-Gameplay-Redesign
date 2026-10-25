"""S7a1 ordered carrier mechanics and real-owner differential; Lua51/native doubles."""
import subprocess
import unittest
from refactor_harness import Context,ROOT,TrackedLua51,legacy_source_observation,measure


def kernel():
    c=Context();c.load('CarrierSet');c.execute("""
      rows={{key=0,name='ZERO'},{key='B',name='B'},{key='C',name='C'}};resolved=0;state={};trace={};changes=0
      P={HasBuilding=function(b,id)trace[#trace+1]='READ:'..id;if unknown==id then return nil end;return state[id]==true end}
      city={GetBuildings=function()return {}end};health={}
      health.Remove=function(c,id)trace[#trace+1]='REMOVE:'..id;if fail==id then error('WRITE_FAIL')end;if unconfirmed~=id then state[id]=nil end end
      health.Create=function(c,id)trace[#trace+1]='CREATE:'..id;if fail==id then error('WRITE_FAIL')end;if unconfirmed~=id then state[id]=true end end
      set=SPCCarrierSet.Define(P,rows,function(name)resolved=resolved+1;if badDefinition==name then error('DEFINITION_UNKNOWN')end;return name end,{read='READ_UNKNOWN',write='WRITE_UNCONFIRMED'})
      function apply(wanted)return set.Apply(city,wanted,health,function()changes=changes+1 end)end
    """);return c


class Kernel(unittest.TestCase):
    def test_definition_lazy_atomic_and_ownership_has_no_hidden_lookup(self):
        c=kernel();c.execute("assert(resolved==0 and not set.Owns('ZERO'));badDefinition='C';assert(not pcall(set.Initialize));assert(resolved==3 and not set.Owns('ZERO'));badDefinition=nil;set.Initialize();assert(resolved==6 and set.Index(0)=='ZERO'and set.Owns('C'));set.Initialize();assert(resolved==6)")
    def test_descriptor_names_and_observation_are_detached_and_readonly(self):
        c=kernel();c.execute("rows[1].name='MUTATE';local n=set.Names();n[1]='BAD';assert(set.Names()[1]=='ZERO'and resolved==0);state.ZERO=true;local p=set.Observe(city,{});assert(p[1].key==0 and p[1].present);p[1].present=false;assert(set.Observe(city,{})[1].present and changes==0);for _,v in ipairs(trace)do assert(v:find('READ:')==1)end")
    def test_all_carriers_preflight_before_any_write(self):
        c=kernel();c.execute("state.ZERO=true;unknown='C';local ok,e=pcall(apply,{B=true});assert(not ok and e:find('READ_UNKNOWN')and state.ZERO and changes==0);for _,v in ipairs(trace)do assert(v:find('READ:')==1)end")
    def test_remove_before_add_exact_readback_and_key_zero(self):
        c=kernel();c.execute("state.C=true;state.B=true;apply({[0]=true});assert(changes==3 and state.ZERO and not state.B and not state.C);assert(table.concat(trace,',')=='READ:ZERO,READ:B,READ:C,REMOVE:B,READ:B,REMOVE:C,READ:C,CREATE:ZERO,READ:ZERO')")
    def test_readback_failure_never_counts_unconfirmed_write(self):
        for kind in ('create','remove'):
            c=kernel();c.execute(("state.ZERO=true;"if kind=='remove'else '')+"unconfirmed='ZERO';local ok,e=pcall(apply,"+('{}'if kind=='remove'else '{[0]=true}')+");assert(not ok and e:find('WRITE_UNCONFIRMED')and changes==0)")
    def test_partial_confirmations_count_before_later_exception(self):
        c=kernel();c.execute("fail='C';assert(not pcall(apply,{[0]=true,B=true,C=true}));assert(changes==2 and state.ZERO and state.B and not state.C)")
    def test_exact_exit_delegates_reference_loss_to_store_without_definition_reads(self):
        c=kernel();c.execute("shared.CityProgressionStore={RemoveOwned=function(c,loss,ids)assert(c==city and loss==proof and #ids==3 and ids[1]=='ZERO');ids[1]='BAD';called=true;return 'OWNED'end};proof={};assert(set.Exit(shared,city,proof)=='OWNED'and called and resolved==0 and set.Names()[1]=='ZERO')")
    def test_noop_apply_has_no_create_remove_or_change(self):
        c=kernel();c.execute("state.ZERO=true;apply({[0]=true});assert(changes==0 and #trace==3 and state.ZERO)")


BASE='77b8c14'
class SourceSet:
    def __init__(self,old=False):self.old=old
    def __truediv__(self,name):
        old=self.old
        class File:
            def read_text(self):
                if old and name in ('ResearchSupport.lua','Lv2Housing.lua'):
                    return subprocess.check_output(['git','show',BASE+':Mod/'+name],cwd=ROOT,text=True)
                return (ROOT/'Mod'/name).read_text()
        return File()


def owners(old=False):
    import test_b270_event_scope as module
    previous=module.LuaRuntime;module.LuaRuntime=TrackedLua51
    try:
        with legacy_source_observation():l,_,_=module.make_fixture(0,True,mod=SourceSet(old),initial_load=False)
    finally:module.LuaRuntime=previous
    l.execute("""
      c=cities[0][0];level=2;tiers={1};raw={pillaged=false,complete=true}
      district={GetID=function()return 1 end,GetType=function()return 1 end,GetCity=function()return c end,
       IsComplete=function()return raw.complete end,IsPillaged=function()return raw.pillaged end}
      Players[0].GetDistricts=function()return {Members=function()return ipairs({district})end}end
      P.Families={DISTRICT_CAMPUS='RESEARCH'};P.Family=function()return 'RESEARCH'end
      shared.EffectiveFacts.Read=function()return {specialization='RESEARCH',potential=4,active=level,first={districtID=1,type='DISTRICT_CAMPUS'},token='TOKEN'}end
      shared.DistrictCompleteness={ReadFacts=function()
       local buildings={};for _,tier in ipairs(tiers)do buildings[#buildings+1]={type='BUILDING_FIXTURE_'..tier,ordinary=true,complete=true,pillaged=false,tier=tier,reason=tier==0 and 'ORDINARY_TIER_ZERO'or 'INCLUDED'}end
       return {validity='VERIFIED',availability='READY',value={districts={{id=1,type='DISTRICT_CAMPUS',complete=raw.complete,pillaged=raw.pillaged,buildings=buildings}}}}
      end}
      shared.ResearchSupport.ready=true;shared.Lv2Housing.ready=true
      log={};local create,remove=P.CreateBuilding,P.RemoveBuilding
      P.CreateBuilding=function(q,id)log[#log+1]='CREATE:'..names[id];return create(q,id)end
      P.RemoveBuilding=function(b,id)log[#log+1]='REMOVE:'..names[id];return remove(b,id)end
      function audit()shared.ResearchSupport.Audit({player=0,city=0});shared.Lv2Housing.Audit({player=0,city=0});assert(not shared.ResearchSupport.errors['0:0']and not shared.Lv2Housing.errors['0:0'])end
      function snapshot()local out={};for id,v in pairs(c.values)do if v then out[#out+1]=names[id]end end;table.sort(out);return table.concat(out,',')end
    """);return l


class RealOwners(unittest.TestCase):
    def test_source_baseline_same_carriers_reads_and_write_order_across_changes(self):
        observed=[]
        for old in (True,False):
            l=owners(old);l.execute("audit();local out={snapshot()};tiers={1,1,2,0};audit();out[#out+1]=snapshot();level=1;audit();out[#out+1]=snapshot();raw.pillaged=true;audit();out[#out+1]=snapshot();raw.pillaged=false;level=4;audit();out[#out+1]=snapshot();local w=counts.building_create+counts.building_remove;audit();assert(counts.building_create+counts.building_remove==w);result=table.concat(out,';')")
            observed.append({'state':l.eval('result'),'order':list(l.globals().log.values()),'counts':dict(l.globals().counts),'support_changes':l.eval('shared.ResearchSupport.changes'),'housing_changes':l.eval('shared.Lv2Housing.changes')})
        self.assertEqual(observed[0],observed[1]);measure('S7a1_real_owners_differential',{'baseline':BASE,'same_carriers':True,'same_native_order_and_counts':True,'source_owners':['ResearchSupport','Lv2Housing'],'states':5,'presence_only':True})
    def test_partial_carrier_unknown_holds_all_original_writes(self):
        l=owners();l.execute("audit();local before=snapshot();local has=P.HasBuilding;P.HasBuilding=function(b,id)if names[id]=='BUILDING_SPC_DEV_LV2_HOUSING_8'then return nil end;return has(b,id)end;tiers={1,2};local n=#log;shared.Lv2Housing.Audit({player=0,city=0});assert(#log==n and snapshot()==before and shared.Lv2Housing.errors['0:0'])")


if __name__=='__main__':unittest.main()
