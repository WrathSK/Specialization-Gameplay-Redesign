"""S7a6 exact registry and real-owner validation/exit/native-order boundaries."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s5d4c1 import actual
from test_refactor_s5d4c8 import fixture as wonder

BASE='84ac7ae'
@contextmanager
def old_source():
    previous=Path.read_text;execute=TrackedLua51.execute
    originals={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('CarrierSet','ResearchApply','ResearchInfrastructure','ResearchChair','IndustryWonderEffects')}
    digests={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in originals.items()}
    def read(p,*a,**kw):return originals[p]if p in originals else previous(p,*a,**kw)
    def run(vm,s,*a,**kw):
        h=sha256(s.encode()).hexdigest()if isinstance(s,str)else None
        if h in digests:SOURCES[h]=digests[h]
        return execute(vm,s,*a,**kw)
    with patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

class Registry(unittest.TestCase):
    def test_detached_names_exact_order_duplicates_and_id_aliases(self):
        c=Context();c.load('CarrierSet');c.execute("local rows={{name='B',id=1},{name='A',id=1},{name='B',id=2}};local r=SPCCarrierSet.Registry(rows);rows[1].name='MUTATE';rows[1].id=9;local n=r.Names();assert(table.concat(n,',')=='B,A,B'and r.Owns(1)and r.Owns(2)and not r.Owns(9));n[1]='BAD';assert(r.Names()[1]=='B')")
    def test_failed_complete_definition_publish_does_not_expose_partial_owned(self):
        from test_refactor_s7a1 import kernel
        c=kernel();c.execute("badDefinition='C';assert(not pcall(set.Initialize)and not set.Owns('ZERO'));badDefinition=nil;set.Initialize();assert(set.Owns('ZERO')and set.Owns('C'))")

class ActualOwners(unittest.TestCase):
    def test_read_write_order_values_and_counts_match_pre_registry_source(self):
        results=[]
        for old in (True,False):
            with old_source()if old else nullcontext():l=actual()
            l.execute("""
            log={};local has,create,remove=P.HasBuilding,P.CreateBuilding,P.RemoveBuilding
            P.HasBuilding=function(b,id)log[#log+1]='H:'..id;return has(b,id)end
            P.CreateBuilding=function(q,id)log[#log+1]='C:'..id;return create(q,id)end
            P.RemoveBuilding=function(b,id)log[#log+1]='R:'..id;return remove(b,id)end
            function audits()for _,n in ipairs({'ResearchApply','ResearchInfrastructure','ResearchChair'})do shared[n].Audit({player=0,city=1});assert(not shared[n].definitionError and not shared[n].errors[0][1])end end
            local campus=cities[1].ds[1];local zone=addDistrict(cities[1],99,'DISTRICT_INDUSTRIAL_ZONE');setBuildings(zone,{'BUILDING_WORKSHOP','BUILDING_FACTORY'});shared.DistrictCompleteness.MarkDirty(0,1)
            audits();campus.workers=1;audits();cities[1].active=3;audits();cities[1].active=4;campus.workers=3;audits();local w=writes;audits();assert(writes==w)
            """)
            results.append({'log':list(l.globals().log.values()),'writes':l.eval('writes'),'changes':[l.globals().shared[n]['changes']for n in ('ResearchApply','ResearchInfrastructure','ResearchChair')]})
        self.assertEqual(*results);measure('S7a6_located_registry_differential',{'baseline':BASE,'same_native_calls_values_write_counts':True,'owners':3})
    def test_failed_owner_revalidation_retains_last_good_health_ownership(self):
        for owner,bad,known in (('ResearchApply','BUILDING_SPC_RESEARCH_APPLY_FAITH_4','BUILDING_SPC_RESEARCH_APPLY_FOOD_0'),('ResearchInfrastructure','BUILDING_SPC_RESEARCH_INFRA_3','BUILDING_SPC_RESEARCH_INFRA_0'),('ResearchChair','BUILDING_SPC_RESEARCH_CHAIR_BUILDING_LIBRARY_7','BUILDING_SPC_RESEARCH_CHAIR_BUILDING_LIBRARY_0')):
            l=actual();l.globals().owner=owner;l.globals().badName=bad;l.globals().knownName=known
            l.execute("""
            local native,ready=SPCRuntimeWork.NativeHealth,SPCRuntimeWork.StartReady
            SPCRuntimeWork.NativeHealth=function(P,s,d,owns,mark)ownership=owns;return native(P,s,d,owns,mark)end
            SPCRuntimeWork.StartReady=function(P,s,n,fn)initialize=fn end
            _G['SPC'..owner].Start(P,shared);local d=shared[owner];local index=P.Info('Buildings',knownName).Index
            assert(not ownership(index));initialize();assert(ownership(index))
            local info=P.Info;P.Info=function(t,n)if t=='Buildings'and n==badName then return nil end;return info(t,n)end
            pcall(initialize);assert(ownership(index))
            local marks=0;d.MarkAudit=function()marks=marks+1 end;fire('GameEvents.BuildingPillageStateChanged',0,1,index,false);assert(marks==1)
            P.Info=info;initialize();assert(ownership(index))
            SPCRuntimeWork.NativeHealth=native;SPCRuntimeWork.StartReady=ready
            """)
    def test_chair_exit_keeps_fresh_catalog_read_without_validation(self):
        l=actual();l.execute("""
        exits={};shared.CityProgressionStore=shared.CityProgressionStore or {};shared.CityProgressionStore.RegisterExit=function(n,fn)exits[n]=fn end
        shared.CityProgressionStore.RemoveOwned=function(c,loss,ids)exitNames=ids end
        SPCResearchChair.Start(P,shared);local rows=P.Rows;local calls=0
        P.Rows=function(n)if n=='SPC_ResearchChairTargets'then calls=calls+1;return {{BuildingType='BUILDING_FRESH_EXIT_ONLY'}}end;error('UNEXPECTED_EXIT_VALIDATION')end
        exits.ResearchChair(cities[1],{});assert(calls==1 and #exitNames==8 and exitNames[1]=='BUILDING_SPC_RESEARCH_CHAIR_BUILDING_FRESH_EXIT_ONLY_0')
        P.Rows=function()return nil end;assert(not pcall(exits.ResearchChair,cities[1],{}));P.Rows=rows
        """)
    def test_infrastructure_retired_not_health_owned_but_still_exit_owned(self):
        l=actual();l.execute("""
        local native=SPCRuntimeWork.NativeHealth;SPCRuntimeWork.NativeHealth=function(P,s,d,owns,mark)ownership=owns;return native(P,s,d,owns,mark)end
        exits={};shared.CityProgressionStore=shared.CityProgressionStore or {};shared.CityProgressionStore.RegisterExit=function(n,fn)exits[n]=fn end;shared.CityProgressionStore.RemoveOwned=function(c,loss,ids)exitNames=ids end
        SPCResearchInfrastructure.Start(P,shared);local d=shared.ResearchInfrastructure;d.ready=true;d.Audit({player=0,city=1})
        local old=SPCResearchInfrastructure.Retired[1];assert(not ownership(P.Info('Buildings',old).Index));exits.ResearchInfrastructure(cities[1],{origin={owner=0,city=1,x=1,y=1}})
        assert(#exitNames==4+#SPCResearchInfrastructure.Retired and exitNames[1]=='BUILDING_SPC_RESEARCH_INFRA_0'and exitNames[5]==old)
        """)

class ActualWonder(unittest.TestCase):
    def test_single_handle_read_write_and_exit_match_frozen_source(self):
        results=[]
        for old in (True,False):
            with old_source()if old else nullcontext():l=wonder()
            l.execute("""
            log={};local get=cities[1].GetBuildings;local has,create,remove=P.HasBuilding,P.CreateBuilding,P.RemoveBuilding
            cities[1].GetBuildings=function(c)log[#log+1]='GET';return get(c)end
            P.HasBuilding=function(b,id)log[#log+1]='H:'..id;return has(b,id)end
            P.CreateBuilding=function(q,id)log[#log+1]='C:'..id;return create(q,id)end
            P.RemoveBuilding=function(b,id)log[#log+1]='R:'..id;return remove(b,id)end
            era='ERA_INDUSTRIAL';w.Refresh(0,1);facts[1].active=3;w.Refresh(0,1);facts[1].active=4;w.Refresh(0,1);assert(not w.errors['0:1'])
            local removeOwned=shared.CityProgressionStore.RemoveOwned
            shared.CityProgressionStore.RemoveOwned=function(c,loss,ids)exitNames=table.concat(ids,',');return removeOwned(c,loss,ids)end
            exits.IndustryWonderEffects(cities[1],{origin={owner=0,x=1,y=1}});assert(not w.records['0:1'])
            """)
            results.append({'trace':list(l.globals().log.values()),'exit':l.eval('exitNames'),'writes':l.eval('writes')})
        self.assertEqual(*results);measure('S7a6_Wonder_registry_differential',{'baseline':BASE,'same_single_handle_calls_exit_list_and_writes':True})

if __name__=='__main__':unittest.main()
