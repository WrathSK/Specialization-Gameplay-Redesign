"""S6b raw worker sharing inside existing full authority checks, Lua51 only."""
import unittest
from refactor_harness import Context, legacy_source_observation, measure
from test_refactor_s5b import synthetic, store
from test_refactor_s5d4c1 import actual


def workers():
    c=synthetic();c.load('FactChanges');c.execute("""
    SPCFactChanges.New(shared);workerReads=0;amount=3;anchor={id=11,type='DISTRICT_CAMPUS',plot=101}
    function native()workerReads=workerReads+1;return amount end
    function inspect()return f.Inspect(0,c,function(value,read)return read(anchor,native)end)end
    """);return c


def real_writers():
    l=actual()
    l.execute("""
    -- Explicit foundation/authority native double. Production EF and all three
    -- writers/DC/SQL are real; full Store authority is proved separately below.
    local native=shared.EffectiveFacts.Read
    shared.CityFlowProbe={SupportFacts=function(pid,city)
     local v=native(pid,city);v.potential=1;v.active=nil;v.activeStatus=nil;return v
    end}
    shared.CityProgressionStore={Owns=function()return false end,FactStamp=function(pid,city)return city.token..':'..tostring(city.active)end}
    P.GovernorGate=function(city)return city.owner,city.id,city.active and 'KNOWN' or 'UNKNOWN',city.active end
    for _,city in pairs(cities)do
     local get=city.GetProperty
     city.GetProperty=function(self,key)
      if key~='SPC_DEV_INVESTMENT_LEDGER_V1'then return get(self,key)end
      local base=shared.CityFlowProbe.SupportFacts(city.owner,city)
      return {schema=1,revision=4,anchor={owner=city.owner,cityID=city.id,token=city.token,first=base.first,specialization=base.specialization},investments={a='u1',b='u2',c='u3'}}
     end
    end
    """)
    with legacy_source_observation():l.globals().include('EffectiveFacts')
    l.execute("""
    SPCEffectiveFacts.Start(P,shared);f=shared.EffectiveFacts
    function audits()for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do
     shared[name].Audit({player=0,city=1});assert(not shared[name].errors[0][1],shared[name].errors[0][1]);assert(not shared[name].definitionError)
    end end
    audits();svc.ReadFacts(0,c,c.token);workerReads=0
    local get=Map.GetPlotByIndex
    Map.GetPlotByIndex=function(id)local p=get(id);if not p then return end
     return {GetWorkerCount=function()workerReads=workerReads+1;return p:GetWorkerCount()end,GetIndex=function()return p:GetIndex()end}
    end
    """);return l


class RawFacts(unittest.TestCase):
    def test_three_readers_one_sample_only_inside_same_phase(self):
        c=workers();c.execute("f.WithPhase('ONE',function()assert(inspect()==3 and inspect()==3 and inspect()==3 and workerReads==1 and reads==1)end);assert(inspect()==3 and inspect()==3 and workerReads==3);f.WithPhase('NEW',function()inspect();inspect();assert(workerReads==4)end)")
    def test_private_reader_expires_and_result_is_detached(self):
        c=workers();c.execute("local reader;f.WithPhase('DETACHED',function()local v=f.Inspect(0,c,function(value,r)reader=r;value.token='MUTATED';return value end);assert(v.token=='MUTATED' and f.Read(0,c).token=='T1');assert(not pcall(reader,anchor,native))end)")
    def test_city_owner_and_second_same_turn_change_invalidate(self):
        c=workers();c.execute("f.WithPhase('CHANGES',function()inspect();amount=2;shared.FactChanges.InvalidateCommitted(0,1,{'WORKERS'});assert(inspect()==2);amount=1;shared.FactChanges.InvalidateCommitted(0,nil,{'WORKERS'});assert(inspect()==1 and workerReads==3);shared.FactChanges.InvalidateCommitted(0,2,{'WORKERS'});assert(inspect()==1 and workerReads==3)end)")
    def test_native_exception_and_busy_reentry_release(self):
        c=workers();c.execute("f.WithPhase('BUSY',function()assert(not pcall(f.Inspect,0,c,function(v,r)return r(anchor,function()local ok,why=pcall(r,anchor,native);assert(not ok and why:find('WORKER_CAPTURE_IN_PROGRESS'));error('NATIVE_FAIL')end)end));assert(inspect()==3 and workerReads==1 and reads==1)end)")
    def test_invalid_counts_never_cached_unknown_not_silently_zero(self):
        for value in ('nil','-1','0/0','math.huge','1.5'):
            c=workers();c.execute("amount="+value+";f.WithPhase('BAD',function()local ok,why=pcall(inspect);assert(not ok and why:find('WORKER_COUNT_INVALID'));amount=3;assert(inspect()==3 and workerReads==2 and reads==1)end)")
    def test_projection_failure_preserves_independent_base_fact(self):
        c=workers();c.execute("f.WithPhase('POLICY',function()local ok,why=pcall(f.Inspect,0,c,function()error('OWN_POLICY_FAILURE')end);assert(not ok and why:find('OWN_POLICY_FAILURE'));assert(inspect()==3 and reads==1)end)")
    def test_write_during_sample_rejects_old_then_recovers_on_explicit_read(self):
        c=workers();c.execute("f.WithPhase('WRITE',function()local ok=pcall(f.Inspect,0,c,function(v,r)return r(anchor,function()local t=f.BeginWrite();amount=2;f.EndWrite(t);return 3 end)end);assert(not ok);assert(inspect()==2 and reads==2 and workerReads==1)end)")
    def test_fact_notification_during_projection_cannot_certify_old_count(self):
        c=workers();c.execute("f.WithPhase('FACT',function()local ok,why=pcall(f.Inspect,0,c,function(v,r)local n=r(anchor,native);amount=2;shared.FactChanges.InvalidateCommitted(0,1,{'WORKERS'});return n end);assert(not ok and why:find('WORKER_FACTS_CHANGED'));assert(inspect()==2 and workerReads==2)end)")
    def test_full_authority_change_after_worker_read_rejects_candidate(self):
        c=workers();c.execute("f.WithPhase('TOKEN',function()assert(not pcall(f.Inspect,0,c,function(v,r)local n=r(anchor,native);c.token='NEW';return n end));assert(inspect()==3 and reads==2 and workerReads==2)end)")
    def test_cold_same_city_base_reentry_cannot_overwrite_new_slot(self):
        c=workers();c.execute("f.WithPhase('REENTRY',function()local ok,why=pcall(f.Inspect,0,c,function(v,r)assert(f.Read(0,c).token=='T1');return r(anchor,native)end);assert(not ok and why:find('WORKER_FACTS_CHANGED'));assert(inspect()==3 and reads==2);for id=2,2048 do f.Read(0,add(id))end;local n=reads;f.Read(0,cities[2048]);assert(reads==n,'DOUBLE_COUNTED_BASE_SLOT')end)")
    def test_reentrant_new_governor_row_wins_even_without_store_version_change(self):
        c=workers();c.execute("shared.CityFlowProbe.SupportFacts=function(pid,c)reads=reads+1;return {owner=pid,cityID=c.id,token=c.token,specialization='RESEARCH',potential=1,first={districtID=11,type='DISTRICT_CAMPUS'}}end;c.GetProperty=function()return {schema=1,revision=2,anchor={owner=0,cityID=1,token='T1',specialization='RESEARCH',first={districtID=11,type='DISTRICT_CAMPUS'}},investments={a='u1'}}end;level=2;P.GovernorGate=function()return 0,1,'KNOWN',level end;f.WithPhase('GATE',function()assert(not pcall(f.Inspect,0,c,function()level=1;assert(f.Read(0,c).active==1)end));assert(f.Read(0,c).active==1 and reads==2)end)")
    def test_replacing_fact_service_with_same_generation_never_reuses_workers(self):
        c=workers();c.execute("f.WithPhase('SERVICE',function()assert(inspect()==3);SPCFactChanges.New(shared);amount=2;assert(inspect()==2 and workerReads==2)end)")
    def test_cached_governor_witness_certifies_after_native_body_without_extra_gate(self):
        c=workers();c.execute("shared.CityFlowProbe.SupportFacts=function(pid,c)reads=reads+1;return {owner=pid,cityID=c.id,token=c.token,specialization='RESEARCH',potential=1,first={districtID=11,type='DISTRICT_CAMPUS'}}end;c.GetProperty=function()return {schema=1,revision=2,anchor={owner=0,cityID=1,token='T1',specialization='RESEARCH',first={districtID=11,type='DISTRICT_CAMPUS'}},investments={a='u1'}}end;level=2;P.GovernorGate=function()return 0,1,'KNOWN',level end;f.WithPhase('GATE',function()f.Read(0,c);local v=f.Inspect(0,c,function(value,r)if level==2 then level=1 end;return value.active end);assert(v==1 and reads==2)end)")
    def test_real_probe_property_write_inside_worker_getter_rejects_stale_plan(self):
        l=store();l.execute("T.invest(c,8201);T.invest(c,8202);T.invest(c,8203);T.governor(4);f.WithPhase('PROBE',function()f.Read(0,c);assert(not pcall(f.Inspect,0,c,function(value,r)return r({id=11,type='DISTRICT_CAMPUS',plot=101},function()P.SetProperty({SetProperty=function()T.governor(3)end},'GOVERNOR',3);return 3 end)end));assert(f.Read(0,c).active==3)end)")
    def test_worker_capacity_degrades_overflow_without_evicting_warm_set(self):
        c=workers();c.execute("f.WithPhase('CAPACITY',function()for i=1,2049 do anchor.plot=i;assert(inspect()==3)end;assert(workerReads==2049);anchor.plot=1;inspect();assert(workerReads==2049);anchor.plot=2049;inspect();assert(workerReads==2050)end)")
    def test_anchor_reference_legacy_and_foreign_are_not_shared(self):
        c=workers();c.execute("f.WithPhase('ANCHOR',function()inspect();anchor.id=12;inspect();anchor.type='DISTRICT_SEOWON';inspect();anchor.plot=102;inspect();assert(workerReads==4);c.x=2;inspect();assert(workerReads==5);c.owner=1;assert(not pcall(inspect)and workerReads==5)end);c.owner=0;shared.CityProgressionStore.FactStamp=nil;f.WithPhase('LEGACY',function()inspect();inspect();assert(workerReads==7)end)")
    def test_production_counter_failure_cannot_latch_sampler(self):
        c=workers();c.execute("local count=P.Count;local once=true;P.Count=function(k)if once then once=false;error('COUNTER_FAILED')end;return count(k)end;f.WithPhase('DIAGNOSTIC',function()assert(not pcall(inspect));assert(inspect()==3 and workerReads==1)end)")


class Composition(unittest.TestCase):
    def test_real_store_full_witness_and_native_leaf_cost_not_increased(self):
        observations=[]
        for shared_read in (False,True):
            l=store();l.execute("""
            T.invest(c,8101);T.invest(c,8102);T.invest(c,8103);T.governor(4)
            nativeCalls={};local measuring=false
            local function wrap(t,k,label)local fn=t[k];if type(fn)=='function'then t[k]=function(...)if measuring then nativeCalls[label]=(nativeCalls[label]or 0)+1 end;return fn(...)end end end
            for _,k in ipairs({'GetID','GetOwner','GetX','GetY','GetProperty'})do wrap(c,k,'city.'..k)end
            for _,k in ipairs({'GetProperty','GetCurrentGameTurn'})do wrap(Game,k,'Game.'..k)end
            stamps=0;local stamp=shared.CityProgressionStore.FactStamp;shared.CityProgressionStore.FactStamp=function(...)if measuring then stamps=stamps+1 end;return stamp(...)end
            Map={GetPlotByIndex=function()if measuring then nativeCalls.plot=(nativeCalls.plot or 0)+1 end;return {GetWorkerCount=function()if measuring then nativeCalls.workers=(nativeCalls.workers or 0)+1 end;return 3 end}end}
            function worker()return Map.GetPlotByIndex(101):GetWorkerCount()end
            function run(combined)measuring=true;f.WithPhase('MEASURE',function()for i=1,3 do
             if combined then assert(f.Inspect(0,c,function(v,r)assert(v.active==4);return r({id=11,type='DISTRICT_CAMPUS',plot=101},worker)end)==3)
             else assert(f.Read(0,c).active==4 and worker()==3)end
            end end);measuring=false end
            """);l.globals().run(shared_read)
            observations.append({'stamps':l.eval('stamps'),'leaf':dict(l.globals().nativeCalls)})
        before,after=observations
        self.assertEqual(before['stamps'],7);self.assertEqual(after['stamps'],7)
        self.assertEqual(before['leaf']['workers'],3);self.assertEqual(after['leaf']['workers'],1)
        self.assertEqual(sum(after['leaf'].values()),sum(before['leaf'].values())-4)
        self.assertEqual({k:v for k,v in before['leaf'].items() if k not in ('plot','workers')},{k:v for k,v in after['leaf'].items() if k not in ('plot','workers')})
        measure('S6b_actual_Store_full_guard_leaf_cost',{'before':before,'after':after,'scope':'actual Store/Flow/EF/Probe; plot and governor native doubles; no CPU/native-heap claim'})
    def test_three_real_writers_same_carriers_no_writes_worker_three_to_one(self):
        observations=[]
        for sharing in (False,True):
            l=real_writers();l.globals().sharing=sharing
            l.execute("local w=writes;workerReads=0;if sharing then f.WithPhase('WRITERS',audits)else audits()end;assert(writes==w);result={};for id,yes in pairs(c.carriers)do if yes then result[id]=true end end")
            observations.append((l.eval('workerReads'),dict(l.globals().result)))
        self.assertEqual(observations[0][0],3);self.assertEqual(observations[1][0],1);self.assertEqual(observations[0][1],observations[1][1])
        measure('S6b_three_real_research_writers',{'before_worker_reads':3,'after_worker_reads':1,'same_carriers':True,'carrier_writes':0,'foundation':'explicit foundation/Stamp double; actual EF/DC/Infrastructure/Apply/Chair and SQL'})
    def test_real_writers_read_unknown_hold_then_new_cause_and_real_write_barrier(self):
        l=real_writers();l.execute("""
        local create,remove=P.CreateBuilding,P.RemoveBuilding
        local function write(fn,...)local t=f.BeginWrite();local ok,why=pcall(fn,...);f.EndWrite(t);assert(ok,why)end
        P.CreateBuilding=function(...)return write(create,...)end;P.RemoveBuilding=function(...)return write(remove,...)end
        local p=Map.GetPlotByIndex;local unknown=false;Map.GetPlotByIndex=function(id)if unknown then return {GetWorkerCount=function()return nil end}end;return p(id)end
        local w=writes;unknown=true;f.WithPhase('UNKNOWN',function()for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do shared[name].Audit({player=0,city=1});assert(shared[name].errors[0][1])end end);assert(writes==w)
        unknown=false;c.ds[1].workers=2;shared.FactChanges.InvalidateCommitted(0,1,{'WORKERS'});f.WithPhase('RECOVER',audits);assert(cc('BUILDING_LIBRARY')==2 and writes>w)
        """)

if __name__=='__main__':unittest.main()
