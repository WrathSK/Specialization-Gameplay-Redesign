"""S7b1 one-attempt cell; real owners retain deliberately different commit policies."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
import test_store_write_boundaries as city
import test_expedition_spy_store as expedition
import test_expedition_spy_gate as gate
import test_expedition_spy_persistence as persistence

BASE='69acc27'
@contextmanager
def history():
    previous=Path.read_text;execute=TrackedLua51.execute
    originals={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('CityProgressionStore','ExpeditionSpyStore')}
    digests={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in originals.items()}
    def read(p,*a,**kw):return originals[p]if p in originals else previous(p,*a,**kw)
    def run(vm,s,*a,**kw):
        h=sha256(s.encode()).hexdigest()if isinstance(s,str)else None
        if h in digests:SOURCES[h]=digests[h]
        return execute(vm,s,*a,**kw)
    with patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

def quiet_vm(*a,**kw):
    vm=TrackedLua51(*a,**kw);vm.globals().print=lambda *parts:None;return vm

@contextmanager
def native_doubles():
    with patch.object(city,'LuaRuntime',quiet_vm),patch.object(expedition,'LuaRuntime',quiet_vm),patch.object(gate.previous,'LuaRuntime',quiet_vm),legacy_source_observation():yield

class Cell(unittest.TestCase):
    def test_one_attempt_then_one_read_despite_write_exception(self):
        c=Context();c.load('PropertyCell');c.execute("local order={};local r=SPCPropertyCell.WriteReadback(function()order[#order+1]='WRITE';error('AFTER')end,function()order[#order+1]='READ';return {applied=true},'REASON'end);assert(table.concat(order,',')=='WRITE,READ'and not r.writeReturned and r.readReturned and r.observed.applied and r.readReason=='REASON')")
    def test_false_nil_and_error_objects_are_not_interpreted_as_commit_policy(self):
        c=Context();c.load('PropertyCell');c.execute("local e={tag='EXACT'};local r=SPCPropertyCell.WriteReadback(function()return false end,function()return nil,'ABSENT'end);assert(r.writeReturned and r.writeResult==false and r.readReturned and r.observed==nil and r.readReason=='ABSENT');r=SPCPropertyCell.WriteReadback(function()error(e)end,function()error(e)end);assert(not r.writeReturned and not r.readReturned and r.writeResult==e and r.observed==e)")

class Policies(unittest.TestCase):
    def test_exact_readback_after_throw_remains_held_in_store_but_accepted_in_expedition(self):
        with native_doubles():
            l=city.fixture();l.execute("local x,y=T.two();T.reload();local s=T.storage(x);local old=s.Read();local next=T.normal(old);local raw=Game.SetProperty;Game.SetProperty=function(o,k,v)raw(o,k,v);error('AFTER_APPLY')end;assert(not pcall(s.Write,old,next));assert(T.encode(T.snapshot(x))==T.encode(old)and T.encode(T.props()[T.key(x)])==T.encode(next))")
            l=expedition.fixture();l.execute("writerMode='throw_after';local r,e=store.Write(P,2,nil,record());assert(r and not e and writes==1 and reads==2)")
    def test_city_pre_and_post_reads_and_single_write_match_frozen_source(self):
        results=[]
        for old in (True,False):
            for mode in ('normal','false_after','throw_before','throw_after','noop','third','corrupt','read_throw'):
                with history()if old else nullcontext(),native_doubles():l=city.fixture()
                l.globals().mode=mode;l.execute("""
                local x,y=T.two();T.reload();local s=T.storage(x);local before=s.Read();local candidate=T.normal(before);local key=T.key(x)
                local get,set=Game.GetProperty,Game.SetProperty;calls={read=0,write=0};local written=false
                Game.GetProperty=function(o,k)if k==key then calls.read=calls.read+1;if mode=='read_throw'and written then error('POSTREAD')end end;return get(o,k)end
                Game.SetProperty=function(o,k,v)
                 if k~=key then return set(o,k,v)end;calls.write=calls.write+1
                 if mode=='throw_before'then error('BEFORE')end;if mode=='noop'then return end
                 local value=M.Copy(v);if mode=='third'then value.revision=value.revision+1 elseif mode=='corrupt'then value.current=false end
                 set(o,k,value);written=true;if mode=='throw_after'then error('AFTER')end;if mode=='false_after'then return false end
                end
                accepted=pcall(s.Write,before,candidate);committed=T.encode(T.snapshot(x));physical=T.encode(T.props()[key]);assert(calls.write==1 and calls.read==2)
                """)
                results.append((old,mode,l.eval('accepted'),l.eval('committed'),l.eval('physical'),dict(l.globals().calls)))
        self.assertEqual([x[1:]for x in results[:8]],[x[1:]for x in results[8:]])
        measure('S7b1_city_property_policy',{'baseline':BASE,'modes':8,'pre_reads':1,'post_reads':1,'setter_attempts':1,'same_commit_protection_and_physical_record':True})
    def test_expedition_validation_and_native_counts_match_frozen_source(self):
        results=[]
        for old in (True,False):
            for mode in ('normal','false_after','throw_before','throw_after','noop','third','malformed','absent'):
                with history()if old else nullcontext(),native_doubles():l=expedition.fixture()
                l.globals().writerMode=mode;l.execute("local r,e=store.Write(P,2,nil,record());accepted=r~=nil;reason=e or 'NONE';assert(writes==1 and reads==2)")
                results.append((old,mode,l.eval('accepted'),l.eval('reason'),l.eval('reads'),l.eval('writes')))
        self.assertEqual([x[1:]for x in results[:8]],[x[1:]for x in results[8:]])
        measure('S7b1_expedition_property_policy',{'baseline':BASE,'modes':8,'pre_reads':1,'post_reads':1,'setter_attempts':1,'same_validated_readback_policy':True})

# Original assertions executed unchanged, with explicit Lua51/include-capable doubles.
class Retained(unittest.TestCase):pass

def retain(prefix,case,names):
    for name in names:
        def run(self,case=case,name=name):
            with native_doubles():getattr(case(),name)()
        setattr(Retained,'test_'+prefix+'_'+name.removeprefix('test_'),run)

retain('city',city.StoreWriteBoundaries,[n for n in dir(city.StoreWriteBoundaries)if n.startswith('test_')and n not in ('test_existing_b127_saved_claim_timer_regression','test_existing_b128_selected_store_return_regression','test_ordinary_age_write_cost_and_per_value_baseline','test_claim_timer_same_turn_progress_and_coldload')])
retain('exp_read',expedition.ReadTests,[n for n in dir(expedition.ReadTests)if n.startswith('test_')])
retain('exp_write',expedition.WriteTests,[n for n in dir(expedition.WriteTests)if n.startswith('test_')])
retain('exp_gate',gate.Gate,[n for n in dir(gate.Gate)if n.startswith('test_')])
retain('exp_persist',persistence.StoreFailureBoundaries,[n for n in dir(persistence.StoreFailureBoundaries)if n.startswith('test_')])
retain('exp_reload',persistence.Reconstruction,[n for n in dir(persistence.Reconstruction)if n.startswith('test_')])

if __name__=='__main__':unittest.main()
