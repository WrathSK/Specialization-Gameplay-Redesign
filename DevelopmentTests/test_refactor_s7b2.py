"""S7b2 Crew attempt boundaries and exact decimal wire equivalence; Lua51."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s6e import Profile,MoneyLua51
import test_b236_crews as crew_cases
import test_store_write_boundaries as city_fixture
import test_b244_capital_storage as numeric_cases
import test_b241_capital as capital_cases

BASE='f0c0827'
@contextmanager
def history():
    previous=Path.read_text;execute=TrackedLua51.execute
    originals={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('CrewProjects','CapitalInvestmentModel','DevelopmentInvestmentModel')}
    digests={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in originals.items()}
    def read(p,*a,**kw):return originals[p]if p in originals else previous(p,*a,**kw)
    def run(vm,s,*a,**kw):
        h=sha256(s.encode()).hexdigest()if isinstance(s,str)else None
        if h in digests:SOURCES[h]=digests[h]
        return execute(vm,s,*a,**kw)
    with patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

def private():
    c=Context();c.load('PropertyCell');c.load('CrewModel');c.execute("""
    state={old=true};reads,writes,clones=0,0,0;err={tag='EXACT_ERROR'}
    local copy=SPCCrewModel.Copy
    function clone(v)clones=clones+1;if failClone then error(err)end;return copy(v)end
    city={GetProperty=function()reads=reads+1;if failRead and reads==2 then error(err)end;return state end}
    Players={[0]=city}
    P={SetProperty=function(o,k,v)writes=writes+1;if mode=='before'then error(err)end;if mode~='noop'then state=v end;if mode=='after'then error(err)end;return mode~='false'end}
    """)
    source=c.fragment('Mod/CrewProjects.lua',' local function save(', ' local function queue(')
    receipt=c.fragment('Mod/CrewProjects.lua',' local function receiptSave(', ' local function safe(')
    c.execute('local P=P;local M=SPCCrewModel;local cp,same=clone,M.Same\n'+source+receipt+'\ncall=save;receipt=receiptSave')
    return c

class CrewCell(unittest.TestCase):
    def test_clone_failure_is_before_attempt_and_postread(self):
        for action in ('call(city,{old=true},{new=true})','receipt(0,{old=true},{new=true})'):
            c=private();c.execute('failClone=true;local ok,e=pcall(function()'+action+'end);assert(not ok and e==err and reads==1 and writes==0 and clones==1)')
    def test_stale_CAS_never_clones_or_calls_setter(self):
        for action in ('call(city,{wrong=true},{new=true})','receipt(0,{wrong=true},{new=true})'):
            c=private();c.execute('assert(not pcall(function()'+action+'end)and reads==1 and writes==0 and clones==0)')
    def test_postread_exception_preserves_original_object(self):
        for action in ('call(city,{old=true},{new=true})','receipt(0,{old=true},{new=true})'):
            c=private();c.execute('failRead=true;local ok,e=pcall(function()'+action+'end);assert(not ok and e==err and reads==2 and writes==1)')
    def test_setter_exception_is_observed_and_false_return_is_not_failure(self):
        c=private();c.execute("mode='after';assert(call(city,{old=true},{new=true})==false and reads==2 and writes==1 and state.new)")
        c=private();c.execute("mode='false';assert(call(city,{old=true},{new=true})==true and reads==2 and writes==1 and state.new)")
        c=private();c.execute("mode='after';assert(receipt(0,{old=true},{new=true})==nil and reads==2 and writes==1 and state.new)")
    def test_unknown_readback_does_not_replay_or_claim_success(self):
        c=private();c.execute("mode='noop';assert(not pcall(call,city,{old=true},{new=true})and reads==2 and writes==1 and state.old)")
    def test_actual_formation_failure_and_grants_match_pre_extraction(self):
        values=[]
        for old in (True,False):
            for mode in ('normal','after','drop','throw','third'):
                with history()if old else nullcontext(),patch.object(city_fixture,'LuaRuntime',MoneyLua51),legacy_source_observation():l=crew_cases.crew_runtime()
                l.globals().mode=mode;l.execute("""
                log={};local set=P.SetProperty;P.SetProperty=function(o,k,v)log[#log+1]=k;return set(o,k,v)end
                local c=C.make();if mode~='normal'then C.orderFailure=mode end
                local r=C.reserve(c);reason=r.error or 'NONE'
                if not r.error then local p=SPCCrewModel.Project(1,150);c:GetBuildQueue().items[p]=1;crew.Request(0,{CityID=c:GetID(),Token='ack',Action='CONFIRM',Reservation=r.reservation});C.complete(c,p)end
                orders=T.encode(c:GetProperty(SPCCrewModel.ORDER_PROPERTY));receipts=T.encode(Players[0]:GetProperty(SPCCrewModel.RECEIPT_PROPERTY));calls=C.calls
                """)
                values.append((old,mode,l.eval('reason'),l.eval('orders'),l.eval('receipts'),l.eval('calls'),list(l.globals().log.values())))
        self.assertEqual([v[1:]for v in values[:5]],[v[1:]for v in values[5:]])
        measure('S7b2_Crew_differential',{'baseline':BASE,'modes':5,'same_order_receipt_grant_and_setter_order':True,'attempt_replay':False})

class Numbers(unittest.TestCase):
    def test_nonnegative_finite_and_canonical_exact_decimal(self):
        c=Context();c.load('PropertyCell');c.execute("""
        for _,n in ipairs({0,1,.1,1/3,2^-1074,2^-1022,1e300,16777217,9007199254740991})do local s=string.format('%.17g',n);assert(SPCPropertyCell.NonnegativeFinite(n)and SPCPropertyCell.CanonicalDecimal17(s)==n)end
        for _,s in ipairs({'',' 1','1 ','01','1.0','+1','1e0','0x1','nan','NaN','inf','1e999','-1','1,5',string.rep('1',33)})do assert(SPCPropertyCell.CanonicalDecimal17(s)==nil,s)end
        for _,v in ipairs({-1,math.huge,0/0,'1',false,{}})do assert(not SPCPropertyCell.NonnegativeFinite(v))end
        for _,v in ipairs({-1,math.huge,0/0,1,false,{}})do assert(SPCPropertyCell.CanonicalDecimal17(v)==nil)end
        """)
    def test_both_models_keep_identical_wire_bytes_and_public_values(self):
        values=[]
        for old in (True,False):
            with history()if old else nullcontext(),legacy_source_observation():
                c=TrackedLua51(unpack_returned_tuples=True);c.globals().include=lambda n:c.execute((ROOT/'Mod'/(n+'.lua')).read_text())
                c.globals().include('CapitalInvestmentModel');c.globals().include('DevelopmentInvestmentModel')
            c.execute("""
            local C,D=SPCCapitalInvestmentModel,SPCDevelopmentInvestmentModel
            ref={owner=0,cityID=1,x=1,y=2,token='source',changes=0};local target=C.Copy(ref);target.cityID=2;target.x=3;target.token='target'
            local q=C.Quote{domain='DISTRICT_CAMPUS',source=ref,turn=5,balance=18004.92578125,D=7,R=20,failureCount=0,commercialized=true}
            local v=C.Begin(nil,q,'STABLE',0,'cap');local encoded=C.Encode(v);assert(C.Same(C.Decode(encoded),v));CAPITAL=encoded
            local d=D.Begin(nil,{source=ref,target=target,domain='DISTRICT_CAMPUS',building='BUILDING_LIBRARY',price=880,cost=132,balance=18004.92578125,turn=5,existing={}},'dev')
            local wire=D.Encode(d);assert(D.Same(D.Decode(wire),d));DEVELOPMENT=wire
            """)
            def plain(v):return {k:plain(x)for k,x in v.items()}if hasattr(v,'items')else v
            values.append((plain(c.globals().CAPITAL),plain(c.globals().DEVELOPMENT)))
        self.assertEqual(*values);measure('S7b2_decimal_wire_differential',{'baseline':BASE,'same_raw_DECIMAL17_V1_payloads':True,'rounding':False,'scope':'fractional investment whitelist only'})

class RetainedModel(capital_cases.Model):
    def setUp(self):
        self.patch=patch.object(capital_cases,'LuaRuntime',TrackedLua51);self.patch.start();self.observation=legacy_source_observation();self.observation.__enter__()
    def tearDown(self):self.observation.__exit__(None,None,None);self.patch.stop()

class RetainedCodec(Profile,numeric_cases.Codec):pass
class RetainedStorage(Profile,numeric_cases.ActualStore):pass
class RetainedFailures(Profile,numeric_cases.Failures):pass
class RetainedCrew(unittest.TestCase):pass
for _name in dir(crew_cases.Formation):
    if _name.startswith('test_'):
        def run(self,name=_name):
            with patch.object(city_fixture,'LuaRuntime',MoneyLua51),legacy_source_observation():
                case=crew_cases.Formation()
                # Lua55 accepted an empty statement emitted by one legacy body;
                # Lua51 requires removing only that duplicate separator.
                case.check=lambda body:crew_cases.crew_runtime().execute(body.replace(';;',';'))
                getattr(case,name)()
        setattr(RetainedCrew,_name,run)

if __name__=='__main__':unittest.main()
