"""S6f worker consumers: actual modules, Lua51; native/foundation doubles named."""
import unittest
from test_refactor_s6e import MoneyLua51
from refactor_harness import TrackedLua51, legacy_source_observation, measure
from test_refactor_s5d4c10 import fixture as commerce_fixture
import test_store_write_boundaries as store_fixture
import test_b246_development as development_cases
from test_b246_development import runtime as development_fixture


def commerce():
    l=commerce_fixture()
    l.execute('''
      local old=shared.EffectiveFacts.Read
      shared.CityFlowProbe={SupportFacts=function(pid,c)
       local f=old(pid,c);f.potential=f.specialization=='NONE'and 0 or 1;f.active=nil;f.activeStatus=nil;return f
      end}
      shared.CityProgressionStore.FactStamp=function(pid,c)return c.token..':'..tostring(c.active)end
      shared.CityProgressionStore.Investment=function(pid,c)assert(pid==c:GetOwner());return c:GetProperty('SPC_DEV_INVESTMENT_LEDGER_V1')end
      P.GovernorGate=function(c)return c.owner,c.id,c.active and 'KNOWN' or 'UNKNOWN',c.active end
      for _,c in pairs(cities)do
       local property=c.GetProperty
       c.GetProperty=function(self,k)
        if k~='SPC_DEV_INVESTMENT_LEDGER_V1'then return property and property(self,k)end
        local f=old(self.owner,self);if f.specialization=='NONE'then return nil end;local receipts={}
        for i=1,(f.potential or 1)-1 do receipts[tostring(i)]='UNIT_'..i end
        return {schema=1,revision=f.potential,anchor={owner=self.owner,cityID=self.id,token=f.token,first=f.first,specialization=f.specialization},investments=receipts}
       end
      end
    ''')
    with legacy_source_observation():l.globals().include('EffectiveFacts')
    l.execute('''
      SPCEffectiveFacts.Start(P,shared);f=shared.EffectiveFacts;workerReads=0
      local get=Map.GetPlotByIndex
      Map.GetPlotByIndex=function(id)
       local p=get(id);if not p then return end
       return {GetWorkerCount=function()workerReads=workerReads+1;if workerFailure then error('WORKER_NATIVE_UNKNOWN')end;return p:GetWorkerCount()end}
      end
      function audit()com.Audit({player=0,city=2})end
      audit();assert(com.views['0:2'].stage=='READY',com.views['0:2'].reason);workerReads=0
    ''')
    return l


def development():
    old=store_fixture.LuaRuntime;store_fixture.LuaRuntime=TrackedLua51
    try:
        from unittest.mock import patch
        expression='local first=T.control(c).first'
        replacement='local r=T.record(c);local first=r.current and r.currentFirst or r.base.first'
        assert development_cases.SETUP.count(expression)==1
        with legacy_source_observation(),patch.object(development_cases,'SETUP',development_cases.SETUP.replace(expression,replacement)):
            l=development_fixture()
    finally:store_fixture.LuaRuntime=old
    with legacy_source_observation():l.globals().include('FactChanges')
    l.execute('''
      SPCFactChanges.New(shared);f=shared.EffectiveFacts;workerReads=0
      local get=Map.GetPlotByIndex
      Map.GetPlotByIndex=function(id)
       local p=get(id)
       return {GetWorkerCount=function()
        workerReads=workerReads+1;if workerFailure then error('WORKER_NATIVE_UNKNOWN')end
        if onWorkers then onWorkers()end;return p:GetWorkerCount()
       end}
      end
      function refresh()return dev.Refresh(0,source:GetID(),false)end
      refresh();workerReads=0
    ''')
    return l


def combined():
    l=development()
    with legacy_source_observation():l.globals().include('Commerce')
    l.execute("""
      local info=P.Info
      P.Info=function(tab,id)
       if tab=='Yields'and id~='YIELD_GOLD'and type(id)=='string'then return {Index=id:gsub('YIELD_','')}end
       if tab=='Buildings'and type(id)=='string'and(id:match('^BUILDING_SPC_COMMERCE_GOLD_')or id=='BUILDING_SPC_COMMERCIALIZATION_ACCESS'or id:match('^BUILDING_SPC_DEV_LV3_COM_')or id:match('^BUILDING_SPC_B061_'))then return {Index=id,BuildingType=id}end
       return info(tab,id)
      end
      local families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_THEATER='CULTURE',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY'}
      P.Family=function(id)return families[id]end
      for _,c in ipairs({source,research,other})do function c:GetYield(y)return y=='SCIENCE'and 100 or 0 end end
      shared.NetworkBridge.CurrentEffectPartners=function()return {validity='VERIFIED',partners={},references={}}end
      -- Native write doubles retain the same Begin/End fence as production Probe.
      local create,remove=P.CreateBuilding,P.RemoveBuilding
      local function write(fn,...)local t=f.BeginWrite();local ok,v=pcall(fn,...);f.EndWrite(t);assert(ok,v);return v end
      P.CreateBuilding=function(...)return write(create,...)end
      P.RemoveBuilding=function(...)return write(remove,...)end
      SPCCommerce.Start(P,shared);com=shared.Commerce;com.BindPermanentWrites()
      function auditCommerce()
       com.Audit({player=0,city=source:GetID()});local v=com.views['0:'..source:GetID()]
       assert(v and v.stage=='READY',v and v.reason or com.error);return v
      end
      function gold()local n=0;for bit=0,30 do if source.markers['BUILDING_SPC_COMMERCE_GOLD_'..bit]then n=n+2^bit end end;return n end
      local v=auditCommerce()
      assert(com.Request(0,{Action='COMMERCE_SELECT',CityID=source:GetID(),Domain='DISTRICT_CAMPUS',Enabled=true,Reference=v.reference,CityToken=v.token,Revision=v.revision,Token='PAIR_SELECTION'}),com.lastRequest.reason)
      assert(gold()==15);workerReads=0
    """)
    return l


class Composition(unittest.TestCase):
    def test_actual_store_commerce_development_share_only_inside_phase_without_writes(self):
        l=combined();l.execute("auditCommerce();refresh();assert(workerReads==2);workerReads=0;local n=effectWrites;f.WithPhase('PAIR',function()auditCommerce();local v=refresh();assert(v.workers==2 and workerReads==1)end);assert(gold()==15 and effectWrites==n)")
        measure('S6f_actual_Commerce_Development',{'independent_workers':2,'existing_explicit_phase_workers':1,'unchanged_gold':15,'projection_writes':0,'scope':'actual Store/EF/Commerce/Development; D/Bridge/native doubles; production scheduler unchanged'})

    def test_actual_commerce_carrier_write_forces_fresh_development_sample(self):
        l=combined();l.execute("P.RemoveBuilding(source.markers,'BUILDING_SPC_COMMERCE_GOLD_0');assert(gold()==14);workerReads=0;local n=effectWrites;f.WithPhase('PAIR_WRITE',function()auditCommerce();refresh()end);assert(workerReads==2 and effectWrites==n+1 and gold()==15)")

    def test_real_pair_confirmation_fresh_after_shared_inspection(self):
        l=combined();l.execute("f.WithPhase('PAIR',function()auditCommerce();refresh()end);assert(open());local n=workerReads;assert(sign()and workerReads>n and moneyCalls==1 and active())")


class LegacyProfile:
    """Keep original Development assertions, with explicit nonrecursive D double."""
    def setUp(self):
        self.old_lua=store_fixture.LuaRuntime;store_fixture.LuaRuntime=MoneyLua51
        self.old_setup=development_cases.SETUP
        expression='local first=T.control(c).first'
        assert self.old_setup.count(expression)==1
        development_cases.SETUP=self.old_setup.replace(expression,'local r=T.record(c);local first=r.current and r.currentFirst or r.base.first')
        self.observation=legacy_source_observation();self.observation.__enter__()
    def tearDown(self):
        self.observation.__exit__(None,None,None)
        development_cases.SETUP=self.old_setup;store_fixture.LuaRuntime=self.old_lua


class RetainedDevelopment(LegacyProfile,development_cases.Runtime):
    """Original assertions unchanged; only test binary32 primitive gets a Lua51 bridge."""
    def check(self,body):
        expression="return string.unpack('f',string.pack('f',x))"
        body=body.replace(expression,'return _s6e_binary32(x)')
        development_fixture().execute(body)


class RetainedGuards(LegacyProfile,development_cases.AdditionalGuards):
    """Original reentry/failed readback/confirmation protections unchanged."""


class Consumers(unittest.TestCase):
    def test_actual_commerce_shared_phase_and_separate_fresh_reads(self):
        l=commerce();l.execute("audit();audit();assert(workerReads==2);workerReads=0;local before=ownedGold(cities[2]);local writes=com.writes;f.WithPhase('SHARED',function()audit();audit();assert(workerReads==1)end);assert(ownedGold(cities[2])==before and com.writes==writes)")
        measure('S6f_actual_commerce_worker_reads',{'independent':2,'explicit_phase':1,'same_carriers':True,'production_flushes_coalesced':False,'foundation':'explicit Store-stamp/foundation double; actual EF/Commerce/D/Bridge'})

    def test_actual_development_shared_phase_and_fresh_confirmation_path(self):
        l=development();l.execute("refresh();refresh();assert(workerReads==2);workerReads=0;local writes=effectWrites;f.WithPhase('SHARED',function()local a=refresh();local b=refresh();assert(a.workers==2 and b.workers==2 and workerReads==1)end);assert(effectWrites==writes);assert(open());local n=workerReads;assert(sign());assert(workerReads>n and moneyCalls==1)")
        measure('S6f_actual_development_worker_reads',{'independent':2,'explicit_phase':1,'native_money_confirmation_fresh':True,'production_flushes_coalesced':False,'foundation':'actual Store/EF/Capital/Development; explicit native Treasury/price/worker doubles'})

    def test_development_second_same_turn_mutation_and_write_barrier(self):
        l=development();l.execute("f.WithPhase('TWO',function()assert(refresh().workers==2);workerCounts[source:GetID()]=3;shared.FactChanges.InvalidateCommitted(0,source:GetID(),{'WORKERS'});assert(refresh().workers==3);workerCounts[source:GetID()]=1;do local t=f.BeginWrite();f.EndWrite(t)end;assert(refresh().workers==1 and workerReads==3)end)")

    def test_development_qualification_and_pillage_do_not_read_workers(self):
        l=development();l.execute("T.governor(3);workerReads=0;assert(not refresh().canSign and workerReads==0);T.governor(4);local read=shared.DistrictCompleteness.ReadFacts;shared.DistrictCompleteness.ReadFacts=function(...)local v=read(...);v.value.districts[1].pillaged=true;return v end;workerReads=0;assert(refresh().workers==0 and workerReads==0)")

    def test_development_unknown_worker_not_zero_or_cached_success(self):
        l=development();l.execute("f.WithPhase('UNKNOWN',function()workerFailure=true;local a=refresh();assert(a.stage=='HELD'and not a.canSign);workerFailure=false;local b=refresh();assert(b.stage=='READY'and b.workers==2 and workerReads==2)end)")

    def test_development_legacy_no_inspect_retains_fresh_path(self):
        l=development();l.execute("f.Inspect=nil;f.WithPhase('LEGACY',function()refresh();refresh();assert(workerReads==2)end)")

    def test_development_reentrant_typed_mutation_rejects_old_projection(self):
        l=development();l.execute("f.WithPhase('REENTRY',function()onWorkers=function()onWorkers=nil;shared.FactChanges.InvalidateCommitted(0,source:GetID(),{'WORKERS'})end;local v=refresh();assert(v.stage=='HELD'and not v.canSign);assert(refresh().workers==2)end)")

    def test_commerce_withdrawal_stays_outside_read_projection(self):
        l=commerce();l.execute("calls=0;shared.CommerceConvergence={Withdraw=function()calls=calls+1;do local t=f.BeginWrite();f.EndWrite(t)end end};f.WithPhase('WRITE',function()audit()end);assert(calls==1 and com.views['0:2'].stage=='READY',com.views['0:2'].reason)")

    def test_commerce_failed_body_retains_confirmed_facts_for_hold(self):
        l=commerce();l.execute("local read=shared.DistrictCompleteness.ReadFacts;shared.DistrictCompleteness.ReadFacts=function()return {validity='UNKNOWN'}end;local before=ownedGold(cities[2]);audit();assert(com.views['0:2'].stage=='HELD'and com.views['0:2'].identity=='COMMERCE'and ownedGold(cities[2])==before);shared.DistrictCompleteness.ReadFacts=read;audit();assert(com.views['0:2'].stage=='READY')")

    def test_commerce_legacy_no_inspect_keeps_existing_count(self):
        l=commerce();l.execute("f.Inspect=nil;f.WithPhase('LEGACY',function()audit();audit();assert(workerReads==2)end)")


if __name__=='__main__':unittest.main()
