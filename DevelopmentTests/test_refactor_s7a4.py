"""S7a4 located mutations vs B317; policy/preflight stays in actual owners."""
from contextlib import contextmanager,nullcontext
from pathlib import Path
from hashlib import sha256
import sqlite3
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s5d4c1 import actual


@contextmanager
def old_source():
    previous=Path.read_text;execute=TrackedLua51.execute
    originals={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','55106b4:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('ResearchApply','ResearchInfrastructure','ResearchChair')}
    digests={sha256(text.encode()).hexdigest():'historical/55106b4/'+str(p.relative_to(ROOT))for p,text in originals.items()}
    def read(p,*a,**kw):return originals[p]if p in originals else previous(p,*a,**kw)
    def run(vm,source,*a,**kw):
        digest=sha256(source.encode()).hexdigest()if isinstance(source,str)else None
        if digest in digests:SOURCES[digest]=digests[digest]
        return execute(vm,source,*a,**kw)
    with patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',run):
        with legacy_source_observation():yield


def located():
    c=Context();c.load('CarrierSet');c.execute("""
      state={[1]=true,[2]=false};locations={[1]=10};log={};count=0
      P={HasBuilding=function(b,id)log[#log+1]='HAS:'..id;return state[id]==true end}
      building={GetBuildingLocation=function(_,id)log[#log+1]='LOC:'..id;return locations[id]end,IsPillaged=function()return damaged==true end}
      city={GetBuildings=function()return building end}
      health={Remove=function(c,id,plot)log[#log+1]='REMOVE:'..id..':'..tostring(plot);if failRemove then error('REMOVE_FAIL')end;if not noRemove then state[id]=nil;locations[id]=nil end end,
       Create=function(c,id,plot)log[#log+1]='CREATE:'..id..':'..plot;if failCreate then error('CREATE_FAIL')end;state[id]=true;locations[id]=wrongLocation or plot end}
      rows={{id=1,yes=true,plot=10,want=false},{id=2,yes=false,want=true}}
      options={observedRemoval=true,removeError='REMOVE_UNKNOWN',createError='CREATE_UNKNOWN'}
      function apply()SPCCarrierSet.ApplyLocated(P,city,rows,20,health,options,function()count=count+1 end)end
    """);return c


class LocatedMechanics(unittest.TestCase):
    def test_exact_order_observed_plot_and_per_confirmed_counts(self):
        c=located();c.execute("apply();assert(count==2 and state[2]and not state[1]);assert(table.concat(log,',')=='REMOVE:1:10,HAS:1,CREATE:2:20,HAS:2,LOC:2')")
    def test_fresh_removal_witness_option_does_not_pass_stale_sample(self):
        c=located();c.execute("options.observedRemoval=false;apply();assert(log[1]=='REMOVE:1:nil')")
    def test_failure_after_first_confirmed_operation_keeps_count(self):
        for inject in ('failCreate=true','wrongLocation=99','damaged=true'):
            c=located();c.execute(inject+";assert(not pcall(apply)and count==1 and not state[1])")
    def test_removal_readback_failure_blocks_all_creates(self):
        c=located();c.execute("noRemove=true;local ok,e=pcall(apply);assert(not ok and e:find('REMOVE_UNKNOWN')and count==0 and not state[2])")
    def test_present_correct_location_noop_and_wrong_location_replaces(self):
        c=located();c.execute("rows={{id=1,yes=true,plot=20,want=true}};locations[1]=20;apply();assert(count==0 and #log==0);rows[1].plot=10;apply();assert(count==2 and locations[1]==20)")


class ActualOwners(unittest.TestCase):
    def test_native_calls_values_order_and_confirmed_counts_match_frozen_source(self):
        values=[]
        for old in (True,False):
            with old_source()if old else nullcontext():l=actual()
            l.execute("""
              trace={};local has,create,remove=P.HasBuilding,P.CreateBuilding,P.RemoveBuilding
              P.HasBuilding=function(b,id)trace[#trace+1]='H:'..id;return has(b,id)end
              P.CreateBuilding=function(q,id)trace[#trace+1]='C:'..id;return create(q,id)end
              P.RemoveBuilding=function(b,id)trace[#trace+1]='R:'..id;return remove(b,id)end
              function audits()for _,n in ipairs({'ResearchApply','ResearchInfrastructure','ResearchChair'})do
               shared[n].Audit({player=0,city=1});assert(not shared[n].definitionError and not shared[n].errors[0][1])
              end end
              function snapshot()local out={};for id,yes in pairs(cities[1].carriers)do if yes then out[#out+1]=id..':'..cities[1].locations[id]end end;table.sort(out);return table.concat(out,',')end
              local campus=cities[1].ds[1];results={};audits();results[#results+1]=snapshot()
              campus.workers=1;audits();results[#results+1]=snapshot()
              for id,yes in pairs(cities[1].carriers)do if yes then cities[1].locations[id]=999 end end;audits();results[#results+1]=snapshot()
              cities[1].active=3;audits();results[#results+1]=snapshot()
              cities[1].active=4;campus.workers=3;audits();results[#results+1]=snapshot()
              local w=writes;audits();assert(writes==w)
            """)
            values.append({'states':list(l.globals().results.values()),'calls':list(l.globals().trace.values()),'changes':{n:l.globals().shared[n]['changes']for n in ('ResearchApply','ResearchInfrastructure','ResearchChair')}})
        self.assertEqual(values[0],values[1]);measure('S7a4_located_differential',{'baseline':'55106b4','same_values_order_native_presence_and_counts':True,'owners':['ResearchApply','ResearchInfrastructure','ResearchChair'],'states':5,'includes_wrong_location':True,'native_objects':'doubles only'})
    def test_owner_full_location_preflight_UNKNOWN_prevents_partial_mutation(self):
        for owner in ('ResearchApply','ResearchInfrastructure','ResearchChair'):
            l=actual();l.globals().owner=owner;l.execute("local c=cities[1];local zone=addDistrict(c,99,'DISTRICT_INDUSTRIAL_ZONE');setBuildings(zone,{'BUILDING_WORKSHOP','BUILDING_FACTORY'});shared.DistrictCompleteness.MarkDirty(0,1);shared[owner].Audit({player=0,city=1});local get=c.GetBuildings;c.GetBuildings=function()local b=get();b.GetBuildingLocation=function()return nil end;return b end;local w=writes;shared[owner].Audit({player=0,city=1});assert(writes==w and shared[owner].errors[0][1])")


if __name__=='__main__':unittest.main()
