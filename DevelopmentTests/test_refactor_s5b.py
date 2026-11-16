"""S5b new independent proofs; existing T04 baseline/registry intentionally untouched."""
import unittest
from refactor_harness import Context,ROOT,legacy_source_observation,measure
from test_refactor_s5a2 import actual_store


def probe(l, governor=False):
    c=Context();l.execute('ExposedMembers=ExposedMembers or {}');l.execute('local P=P\n'+c.fragment('Mod/Probe.lua','local function factWrite(', '-- A live non-trader'))
    if governor:
        l.execute("P.Call=function(o,k,...)local fn=o and o[k];if type(fn)~='function'then return false end;return pcall(fn,o,...)end")
        l.execute('local P=P\n'+c.fragment('Mod/Probe.lua','local function governorProperty(', '-- Selected-city role facts'))


def store():
    l=actual_store();l.execute("T.start();c=T.fresh(1);T.register(c);T.complete(c,'DISTRICT_CAMPUS');reads=0;counts={};P.Count=function(k)counts[k]=(counts[k]or 0)+1 end;local fn=shared.CityFlowProbe.SupportFacts;shared.CityFlowProbe.SupportFacts=function(...)reads=reads+1;return fn(...)end;f=shared.EffectiveFacts")
    probe(l);return l


def synthetic():
    c=Context();c.load('EffectiveFacts');c.execute("""
    P={IsTestPlayer=function(pid)return pid==0 end,Count=function(k)counts[k]=(counts[k]or 0)+1 end}
    cities={};function add(id)
     local c={id=id,owner=0,x=id,y=1,revision=1,token='T'..id}
     function c:GetID()return self.id end;function c:GetOwner()return self.owner end
     function c:GetX()return self.x end;function c:GetY()return self.y end
     function c:GetProperty()return nil end;cities[id]=c;return c
    end
    c=add(1);reads=0;bad=false
    shared.CityProgressionStore={FactStamp=function(pid,c)assert(not bad,'AUTHORITY_UNKNOWN');return c.token..':'..c.revision end,Owns=function()return false end}
    shared.CityFlowProbe={SupportFacts=function(pid,c)reads=reads+1;return {owner=pid,cityID=c.id,token=c.token,specialization='NONE',potential=0}end}
    SPCEffectiveFacts.Start(P,shared);f=shared.EffectiveFacts
    """);return c


class Authority(unittest.TestCase):
    def test_actual_store_phase_copy_and_outside_freshness(self):
        l=store();l.execute("f.WithPhase('TEST',function()local a=f.Read(0,c);a.first.type='CHANGED';local b=f.Read(0,c);assert(b.first.type=='DISTRICT_CAMPUS' and reads==1 and counts.facts_reuse==1)end);f.Read(0,c);f.Read(0,c);assert(reads==3)")
    def test_actual_store_two_investments_between_reads_same_phase(self):
        l=store();l.execute("f.WithPhase('INVESTMENT',function()assert(f.Read(0,c).potential==1);T.invest(c,9901);assert(f.Read(0,c).potential==2);T.invest(c,9902);assert(f.Read(0,c).potential==3)end);assert(fixtureStats().kills==2)")
    def test_actual_store_commit_reentry_cannot_hit_old_success(self):
        l=store();l.execute("local setter=Game.SetProperty;local held=0;Game.SetProperty=function(o,k,v)if k==T.key(c)then local ok,err=pcall(f.Read,0,c);assert(not ok and tostring(err):find('IDENTITY_COMMIT_IN_PROGRESS'));held=held+1 end;return setter(o,k,v)end;f.WithPhase('COMMIT',function()f.Read(0,c);T.invest(c,9903);assert(f.Read(0,c).potential==2)end);assert(held==3)")
    def test_applied_then_throw_keeps_actual_store_held(self):
        l=store();l.execute("local setter=Game.SetProperty;Game.SetProperty=function(o,k,v)local out=setter(o,k,v);if k==T.key(c)then error('AFTER_APPLY')end;return out end;f.WithPhase('FAULT',function()f.Read(0,c);assert(not pcall(T.invest,c,9904));assert(not pcall(f.Read,0,c))end);assert(not pcall(f.Read,0,c));local value=f.Version();local t=f.BeginWrite();f.EndWrite(t);assert(f.Version()==value+2)")
    def test_real_six_property_governor_same_turn_unknown_and_recovery(self):
        l=store();l.execute('T.invest(c,9905);T.invest(c,9906);T.invest(c,9907)');probe(l,True)
        l.execute("""
        local get=c.GetProperty;local raw={SPC_P0_GOV_CONTROL_A007=1,SPC_P0_GOV_PRESENT=1,SPC_P0_GOV_ESTABLISHED=1,SPC_P0_GOV_REQ_2=1,SPC_P0_GOV_REQ_3=1,SPC_P0_GOV_REQ_4=1}
        c.GetProperty=function(self,k)if k:find('SPC_P0_GOV_')then return raw[k]end;return get(self,k)end
        reads=0;f.WithPhase('GOVERNOR',function()
         assert(f.Read(0,c).active==4);assert(f.Read(0,c).active==4 and reads==1)
         raw.SPC_P0_GOV_REQ_4=0;assert(f.Read(0,c).active==3 and reads==2)
         raw.SPC_P0_GOV_CONTROL_A007=nil;assert(f.Read(0,c).activeStatus=='UNKNOWN_GOVERNOR' and reads==3)
         raw.SPC_P0_GOV_CONTROL_A007=1;assert(f.Read(0,c).active==3 and reads==4)
         raw.SPC_P0_GOV_REQ_4=1;raw.SPC_P0_GOV_REQ_3=0;assert(f.Read(0,c).activeStatus=='UNKNOWN_GOVERNOR')
         raw.SPC_P0_GOV_REQ_3=1;assert(f.Read(0,c).active==4 and reads==6)
        end)
        """)
    def test_governor_getter_changes_identity_on_hit_and_final_miss_witness(self):
        for when in (1,2):
            l=store();l.execute('T.invest(c,9911);reads=0;counts={}');probe(l,True)
            l.execute("""
            local get=c.GetProperty;calls=0;armed=false;original=c.s.values.TOKEN
            c.GetProperty=function(self,k)
             if k=='SPC_P0_GOV_CONTROL_A007'then calls=calls+1;if armed and calls==mutationAt then c.s.values.TOKEN='CHANGED' end;return 1 end
             if k:find('SPC_P0_GOV_')then return 1 end;return get(self,k)
            end
            """)
            l.globals().mutationAt=when
            if when==1:
                l.execute("f.WithPhase('HIT',function()f.Read(0,c);calls=0;armed=true;assert(not pcall(f.Read,0,c));c.s.values.TOKEN=original;armed=false;f.Read(0,c);assert(reads==2 and not counts.facts_reuse)end)")
            else:
                l.execute("f.WithPhase('MISS',function()armed=true;assert(not pcall(f.Read,0,c));c.s.values.TOKEN=original;armed=false;f.Read(0,c);assert(reads==2 and not counts.facts_reuse)end)")
    def test_actual_store_token_position_owner_and_new_vm(self):
        l=store();l.execute("f.WithPhase('REF',function()f.Read(0,c);local x=c.s.ref.x;c.s.ref.x=x+100;assert(not pcall(f.Read,0,c));c.s.ref.x=x;local token=c.s.values.TOKEN;c.s.values.TOKEN='REUSED';assert(not pcall(f.Read,0,c));c.s.values.TOKEN=token;c.s.ref.owner=1;assert(not pcall(f.Read,0,c));c.s.ref.owner=0;assert(f.Read(0,c).active==1)end);local old=f;T.reload();assert(shared.EffectiveFacts~=old and shared.EffectiveFacts.Version()==0)")


class Phase(unittest.TestCase):
    def test_failed_witness_drops_old_success_before_recovery(self):
        c=synthetic();c.execute("f.WithPhase('UNKNOWN',function()f.Read(0,c);bad=true;assert(not pcall(f.Read,0,c));bad=false;f.Read(0,c);assert(reads==2)end)")
    def test_nested_phase_exception_and_nil_multiple_returns(self):
        c=synthetic();c.execute("local a,b,z=f.WithPhase('OUTER',function()return f.WithPhase('INNER',function()return nil,2,nil end)end);assert(a==nil and b==2 and z==nil);assert(not pcall(f.WithPhase,'FAIL',function()f.Read(0,c);error('STOP')end));local before=reads;f.Read(0,c);assert(reads==before+1)")
    def test_actual_probe_mutations_refresh_same_runtime_batch_even_on_throw(self):
        c=synthetic();c.load('RuntimeWork');probe(c.lua)
        c.execute("""
        local b=SPCRuntimeWork.New(P,shared);local object={SetProperty=function()assert(b.Facts(0,c).token=='T1');error('AFTER_APPLY')end,CreateBuilding=function()return 1,nil,3 end,RemoveBuilding=function()return nil end}
        f.WithPhase('WRITE',function()
         b.Facts(0,c);b.Facts(0,c);assert(reads==1);local before=ExposedMembers.SPC_RuntimeUIRevision
         assert(not pcall(P.SetProperty,object,'key',2));assert(ExposedMembers.SPC_RuntimeUIRevision==before)
         b.Facts(0,c);assert(reads==3);local a,z,v=P.CreateBuilding(object,1);assert(a==1 and z==nil and v==3)
         f.Read(0,c);P.RemoveBuilding(object,1);f.Read(0,c);assert(reads==5)
        end)
        """)
    def test_native_reentry_during_capture_not_confirmed(self):
        c=synthetic();c.execute("local read=shared.CityFlowProbe.SupportFacts;local once=true;shared.CityFlowProbe.SupportFacts=function(...)local value=read(...);if once then once=false;local t=f.BeginWrite();f.EndWrite(t)end;return value end;f.WithPhase('REENTRY',function()assert(not pcall(f.Read,0,c));assert(f.Read(0,c).token=='T1' and reads==2)end)")
    def test_turn_and_capacity_fallback_bounded(self):
        c=synthetic();c.execute("f.WithPhase('CAPACITY',function()for id=1,2050 do f.Read(0,cities[id]or add(id))end;assert(reads==2050);f.Read(0,cities[1]);assert(reads==2050);f.Read(0,cities[2050]);assert(reads==2051);turn=turn+1;f.Read(0,cities[1]);assert(reads==2052)end)")
    def test_runtime_batch_retains_guarded_local_reuse_outside_shared_phase(self):
        c=synthetic();c.load('RuntimeWork');probe(c.lua)
        c.execute("local b=SPCRuntimeWork.New(P,shared);b.Facts(0,c);b.Facts(0,c);assert(reads==1);P.CreateBuilding({CreateBuilding=function()end},1);b.Facts(0,c);assert(reads==2);c.token='NEXT';assert(b.Facts(0,c).token=='NEXT' and reads==3);f.Read(0,c);f.Read(0,c);assert(reads==5)")
    def test_real_counter_schema_exposes_reuse_without_extra_sampling(self):
        c=Context();c.load('PerformanceCounters');c.execute("ExposedMembers.SPC_Performance=SPCPerformance.New();SPCPerformance.Count('facts_reuse');assert(ExposedMembers.SPC_Performance.entries.facts_reuse.total==1)")
    def test_legacy_flow_without_store_stamp_stays_fresh(self):
        c=synthetic();c.execute("shared.CityProgressionStore=nil;f.WithPhase('LEGACY',function()f.Read(0,c);f.Read(0,c);assert(reads==2)end)")


class ActualWriters(unittest.TestCase):
    def test_real_store_and_two_real_writers_reuse_only_before_mutation(self):
        l=store();l.execute("""
        c=T.fresh(2);T.register(c);c.values={};local ids={};local serial=0;local info=P.Info
        P.Info=function(t,k)if t~='Buildings'then return info(t,k)end;if not ids[k]then serial=serial+1;ids[k]=serial end;return {Index=ids[k],Housing=k:find('HOUSING')and 1 or 0,CitizenSlots=0,PrereqDistrict=({RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE',COMMERCE='DISTRICT_COMMERCIAL_HUB'})[k:match('DEV_GPP_(%u+)_')]or'DISTRICT_CAMPUS'}end
        P.Rows=function(t)local rows={};if t=='Building_GreatPersonPoints'then for kind,classes in pairs({RESEARCH={'SCIENTIST'},CULTURE={'WRITER','ARTIST','MUSICIAN'},COMMERCE={'MERCHANT'},INDUSTRY={'ENGINEER'}})do for bit=0,7 do for _,cl in ipairs(classes)do rows[#rows+1]={BuildingType='BUILDING_SPC_DEV_GPP_'..kind..'_'..bit,GreatPersonClassType='GREAT_PERSON_CLASS_'..cl,PointsPerTurn=2*2^bit}end end end end;return rows end
        P.HasBuilding=function(b,k)return b:HasBuilding(k)end
        c.GetBuildings=function()return {HasBuilding=function(_,k)return c.values[k]==true end,RemoveBuilding=function(_,k)c.values[k]=nil end}end
        c.GetBuildQueue=function()return {CreateBuilding=function(_,k)c.values[k]=true end}end
        """)
        with legacy_source_observation():l.globals().include('Lv2Housing');l.globals().include('Lv2GPP')
        l.execute("SPCLv2Housing.Start(P,shared);SPCLv2GPP.Start(P,shared);shared.Lv2Housing.ready=true;shared.Lv2GPP.ready=true;reads=0;counts={};f.WithPhase('WRITERS',function()shared.Lv2Housing.Audit({player=0,city=c:GetID()});shared.Lv2GPP.Audit({player=0,city=c:GetID()})end);assert(reads==1 and not next(shared.Lv2Housing.errors) and not next(shared.Lv2GPP.errors) and not counts.building_create and not counts.building_remove);reads=0;c.values[P.Info('Buildings','BUILDING_SPC_DEV_LV2_HOUSING_0').Index]=true;f.WithPhase('REMOVAL',function()shared.Lv2Housing.Audit({player=0,city=c:GetID()});shared.Lv2GPP.Audit({player=0,city=c:GetID()})end);assert(reads==2 and counts.building_remove==1)")
        measure('S5b_real_Store_and_writers',{'no_write_captures':1,'real_removal_captures':2,'native_doubles':'catalogue and carrier presence; actual Store/Flow/EffectiveFacts/Housing/GPP/Probe'})

if __name__=='__main__':unittest.main()
