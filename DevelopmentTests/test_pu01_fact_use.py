"""PU01 actual HD catalogue/DC/EF/Commerce; Lua51, native doubles, LOCAL only."""
import unittest
from refactor_harness import ROOT, TrackedLua51, legacy_source_observation

MOD = ROOT / 'Mod'


def fixture():
    # Reuse only the maintained native-shape fixture prefix, never its stress body.
    path = ROOT / 'DevelopmentTests/test_p0_a.py'
    text = path.read_text()
    boundary = '\nl=runtime()'
    assert text.count(boundary) == 2
    namespace = {'__file__': str(path)}
    exec(compile(text[:text.index(boundary)], str(path), 'exec'), namespace)
    namespace['LuaRuntime'] = TrackedLua51
    with legacy_source_observation():
        v = namespace['runtime']()
        v.globals().print = lambda *parts: None
        v.globals().include = lambda n: v.execute((MOD / (n+'.lua')).read_text())
        for name in ('CommerceModel', 'FactChanges', 'EffectiveFacts'):
            v.globals().include(name)
    v.execute(r'''
      P.IsTestPlayer=function(pid)return pid==0 end
      hooks={};Events=setmetatable({},{__index=function(t,k)local e={Add=function(f)
        hooks[k]=hooks[k]or{};hooks[k][#hooks[k]+1]=f end};rawset(t,k,e);return e end})
      GameEvents=setmetatable({},{__index=function(t,k)local e={Add=function(f)
        local key='GameEvents.'..k;hooks[key]=hooks[key]or{};hooks[key][#hooks[key]+1]=f end};rawset(t,k,e);return e end})
      function fire(name,...)for _,fn in ipairs(hooks[name]or{})do fn(...)end end
      Game.GetLocalPlayer=function()return 0 end
      GameConfiguration={GetGameSpeedType=function()return 'GAMESPEED_STANDARD'end}
      GameInfo.GameSpeeds={GAMESPEED_STANDARD={GameSpeedType='GAMESPEED_STANDARD'}}
      P.Family=function(id)return ({DISTRICT_CAMPUS='RESEARCH',DISTRICT_THEATER='CULTURE',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY'})[id]end
      local info=P.Info
      P.Info=function(tab,id)
        if tab=='Yields'then return {Index=id:gsub('YIELD_','')}end
        if tab=='Buildings'and type(id)=='string'and id:match('^BUILDING_SPC_')then
          return {Index=id,BuildingType=id,InternalOnly=1}end
        return info(tab,id)
      end
      c.identity='COMMERCE';c.revision=1;c.markers={};c.name='Commerce'
      hub=addDistrict(c,12,'DISTRICT_COMMERCIAL_HUB');hub.workers=2
      setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'})
      theater=addDistrict(c,13,'DISTRICT_THEATER');setBuildings(theater,{'BUILDING_AMPHITHEATER'})
      first={districtID=hub.id,type='DISTRICT_COMMERCIAL_HUB',turn=0}
      c.ledger={schema=1,revision=4,anchor={owner=0,cityID=c.id,token=c.token,first=first,specialization='COMMERCE'},
        investments={a='UNIT_A',b='UNIT_B',c='UNIT_C'}}
      c.GetName=function()return c.name end
      yields={SCIENCE=100,CULTURE=80,PRODUCTION=40,FAITH=20,FOOD=30}
      yieldReads={};c.GetYield=function(_,id)
        yieldReads[id]=(yieldReads[id]or 0)+1
        if onYield then onYield(id)end
        if yieldFailure==id then error('NATIVE_YIELD_UNAVAILABLE')end
        return yields[id]or 0
      end
      local buildings=c.GetBuildings
      c.GetBuildings=function()
        local b=buildings();local has,location=b.HasBuilding,b.GetBuildingLocation
        b.HasBuilding=function(o,id)if type(id)=='string'and id:match('^BUILDING_SPC_')then return c.markers[id]==true end;return has(o,id)end
        b.GetBuildingLocation=function(o,id)if type(id)=='string'then return c.markers[id]and c.x or -1 end;return location(o,id)end
        b.RemoveBuilding=function(_,id)c.markers[id]=nil;effectWrites=effectWrites+1 end
        return b
      end
      local queue=c.GetBuildQueue
      c.GetBuildQueue=function()
        local q=queue();q.CreateBuilding=function(_,id)c.markers[id]=true;effectWrites=effectWrites+1 end;return q
      end
      local plot=Map.GetPlotByIndex(hub.plot);local worker=plot.GetWorkerCount
      workerReads=0;plot.GetWorkerCount=function()
        workerReads=workerReads+1
        if workerFailure then error('NATIVE_WORKER_UNAVAILABLE')end
        if workerOverride then return workerValue end
        return worker()
      end
      effectWrites=0;historyWrites=0
      P.HasBuilding=function(b,id)return b:HasBuilding(id)end
      P.GovernorGate=function(city)return city.owner,city.id,city.active and 'KNOWN'or 'UNKNOWN',city.active end
      local own=Players[0].GetCities
      Players[0].GetCities=function()local cs=own();cs.Members=function()return ipairs({c})end;return cs end
      shared.CityFlowProbe={SupportFacts=function(pid,city)
        assert(city==c and pid==city.owner)
        return {owner=pid,cityID=city.id,x=city.x,y=city.y,token=city.token,first=first,
          specialization=city.identity,potential=1,progression='ACTIVE'}
      end}
      state=SPCCommerceModel.Select(SPCCommerceModel.New(0),'DISTRICT_CAMPUS',true)
      local store={}
      store.Owns=function(city)return city==c end
      store.FactStamp=function(pid,city)return city.token..':'..city.revision end
      store.Investment=function(pid,city)return city.ledger end
      store.HistoricalReference=function(city)return {owner=city.owner,cityID=city.id,token=city.token,x=city.x,y=city.y}end
      store.HistoryStartStatus=function()return 'EXISTING'end
      store.CommerceState=function(pid,city)return {token=city.token,value=SPCCommerceModel.Copy(state)}end
      store.RegisterExit=function()end;store.RegisterReturn=function()end
      shared.CityProgressionStore=store
      SPCFactChanges.New(shared);SPCEffectiveFacts.Start(P,shared);f=shared.EffectiveFacts
      SPCDistrictCompleteness.Start(P,shared);dc=shared.DistrictCompleteness
      local proof=1
      shared.NetworkBridge={CurrentEffectPartners=function()return {validity='VERIFIED',partners={},references={}}end,
        TransactionCurrent=function()return not networkPending end,ProofRevision=function()return proof end}
      function bumpProof()proof=proof+1 end
      function gold()local n=0;for bit=0,30 do if c.markers['BUILDING_SPC_COMMERCE_GOLD_'..bit]then n=n+2^bit end end;return n end
      function dirtyD()dc.MarkDirty(0,c.id,'TEST_BUILDING_CHANGE')end
      function audit()com.Audit({player=0,city=c.id});return com.views['0:'..c.id]end
      function view()return com.views['0:'..c.id]end
    ''')
    # Execute the actual native write/barrier seam, not a mock that accepts a fence.
    probe = (MOD/'Probe.lua').read_text()
    start = probe.index('local function factWrite(')
    end = probe.index('-- A live non-trader', start)
    v.execute('local P=P\n'+probe[start:end])
    with legacy_source_observation():
        v.globals().include('Commerce')
    v.execute("SPCCommerce.Start(P,shared);com=shared.Commerce;com.BindPermanentWrites();audit();assert(gold()==15,view().reason)")
    return v


class ActualInputs(unittest.TestCase):
    def test_worker_unknown_retains_installed_amount_and_never_saves_zero(self):
        v=fixture();v.execute("local n=effectWrites;workerFailure=true;audit();assert(view().stage=='HELD'and gold()==15 and effectWrites==n and historyWrites==0)")

    def test_invalid_worker_values_are_unknown_and_true_zero_is_confirmed(self):
        for value in ('nil','-1','0/0','math.huge','.5'):
            with self.subTest(value=value):
                v=fixture();v.execute("workerOverride=true;workerValue="+value+";audit();assert(gold()==15 and view().stage=='HELD')")
        v=fixture();v.execute("workerOverride=true;workerValue=0;audit();assert(view().stage=='READY'and gold()==0 and historyWrites==0)")

    def test_confirmed_active_loss_does_not_depend_on_unreadable_D_or_workers(self):
        v=fixture();v.execute("c.active=2;failRead=true;workerFailure=true;dirtyD();local n=workerReads;audit();assert(gold()==0 and workerReads==n and view().reason=='COMMERCE_ACTIVE_III_REQUIRED')")

    def test_unavailable_D_keeps_output_then_new_actual_building_fact_recovers(self):
        v=fixture();v.execute("failRead=true;dirtyD();local n=effectWrites;audit();assert(gold()==15 and effectWrites==n and view().stage=='HELD');failRead=false;setBuildings(d,{'BUILDING_LIBRARY'});dirtyD();audit();assert(gold()==5)")

    def test_unchosen_domain_yield_failure_does_not_poison_selected_domain(self):
        v=fixture();v.execute("yieldFailure='CULTURE';audit();assert(gold()==15 and view().stage=='READY'and yieldReads.CULTURE==nil)")

    def test_same_reference_second_building_and_worker_changes_recompute(self):
        v=fixture();v.execute("local token=c.token;setBuildings(d,{'BUILDING_LIBRARY'});dirtyD();audit();assert(gold()==5);setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});dirtyD();audit();assert(gold()==15 and c.token==token);hub.workers=0;f.Invalidate();audit();assert(gold()==0);hub.workers=2;f.Invalidate();audit();assert(gold()==15)")

    def test_actual_native_write_during_source_read_cannot_apply_stale_plan(self):
        v=fixture();v.execute("local once=true;onYield=function()if once then once=false;P.CreateBuilding(c:GetBuildQueue(),'BUILDING_SPC_TEST_BOUNDARY')end end;yields.SCIENCE=200;local old=gold();audit();assert(gold()==old and view().stage=='HELD');onYield=nil;audit();assert(gold()==30)")

    def test_fact_change_during_source_read_revokes_current_plan(self):
        v=fixture();v.execute("local once=true;onYield=function()if once then once=false;shared.FactChanges.InvalidateCommitted(0,c.id,{'WORKERS'})end end;yields.SCIENCE=200;audit();assert(gold()==15 and not com.TransactionCurrent(0,c.id));onYield=nil;audit();assert(gold()==30 and com.TransactionCurrent(0,c.id))")

    def test_network_proof_change_during_source_read_is_not_transaction_current(self):
        v=fixture();v.execute("local once=true;onYield=function()if once then once=false;bumpProof()end end;yields.SCIENCE=200;audit();assert(gold()==15 and view().stage=='HELD'and not com.TransactionCurrent(0,c.id));onYield=nil;audit();assert(gold()==30 and com.TransactionCurrent(0,c.id))")

    def test_actual_write_fence_releases_after_native_error_and_nested_phase(self):
        v=fixture();v.execute("local before=f.Version();local q=c:GetBuildQueue();q.CreateBuilding=function()error('APPLIED_THEN_ERROR')end;assert(not pcall(P.CreateBuilding,q,'BUILDING_SPC_TEST'));assert(f.Version()==before+2);f.WithPhase('AFTER_FAILED_NATIVE',function()assert(f.Read(0,c).active==4)end);local n=gold();audit();assert(gold()==n)")

    def test_actual_ordinary_write_fence_invalidates_cached_D_before_native_event(self):
        v=fixture();v.execute("f.WithPhase('READ_WRITE_READ',function()audit();local b=c:GetBuildings();b.RemoveBuilding=function()setBuildings(d,{'BUILDING_LIBRARY'})end;P.RemoveBuilding(b,GameInfo.Buildings.BUILDING_UNIVERSITY.Index);audit();assert(gold()==5)end)")

    def test_failed_D_capture_does_not_retry_without_a_new_fact_or_write(self):
        v=fixture();v.execute("failRead=true;dirtyD();audit();local n=counters.dc_capture;for i=1,20 do audit()end;assert(counters.dc_capture==n and gold()==15)")

    def test_getters_and_idle_publication_do_not_create_work_or_writes(self):
        v=fixture();v.execute("local n=effectWrites;local reads=workerReads;local dreads=counters.dc_capture;for i=1,100 do com.Describe(0,c);fire('GameCoreEventPublishComplete')end;assert(effectWrites==n and workerReads==reads and counters.dc_capture==dreads and historyWrites==0)")


class StatusProjection(unittest.TestCase):
    def test_real_consumer_executes_in_restricted_Civ_Lua51_profile(self):
        v=fixture();v.execute("os=nil;io=nil;debug=nil;package=nil;require=nil;rawget=nil;loadfile=nil;dofile=nil;collectgarbage=nil;table.unpack=nil;table.pack=nil;audit();assert(_VERSION=='Lua 5.1'and gold()==15);workerOverride=true;workerValue=nil;audit();assert(gold()==15 and view().stage=='HELD');workerValue=0;audit();assert(gold()==0);workerValue=2;audit();assert(gold()==15)")

    def test_depth_absence_zero_and_unavailable_are_distinct(self):
        v=fixture();v.execute("local s=dc.ReadFacts(0,c,c.token);local zero=SPCDistrictCompleteness.Clone(s);zero.value.domains.DISTRICT_CAMPUS.value=0;local missing=SPCDistrictCompleteness.Clone(s);missing.value.domains.DISTRICT_CAMPUS=nil;assert(SPCFactUse.Depth(s,'DISTRICT_CAMPUS').value==3);assert(SPCFactUse.Depth(zero,'DISTRICT_CAMPUS').status=='CONFIRMED'and SPCFactUse.Depth(zero,'DISTRICT_CAMPUS').value==0);assert(SPCFactUse.Depth(missing,'DISTRICT_CAMPUS').status=='NOT_APPLICABLE');s.availability='TEMPORARILY_UNAVAILABLE';assert(SPCFactUse.Depth(s,'DISTRICT_CAMPUS').status=='UNKNOWN')")

    def test_anchor_projection_cannot_mutate_the_shared_snapshot(self):
        v=fixture();v.execute("local s=dc.ReadFacts(0,c,c.token);local a=SPCFactUse.Anchor(s,first);assert(a.status=='CONFIRMED');a.value.plot=999;assert(SPCFactUse.Anchor(s,first).value.plot==hub.plot)")

    def test_unselected_unknown_domain_is_not_misreported_as_absent(self):
        v=fixture();v.execute("local read=dc.ReadFacts;dc.ReadFacts=function(...)local s=read(...);s.value.domains.DISTRICT_THEATER.value=0/0;return s end;audit();assert(gold()==15 and view().stage=='READY');local found;for _,r in ipairs(view().domains)do if r.id=='DISTRICT_THEATER'then found=r end end;assert(found and found.inputStatus=='UNKNOWN'and not found.eligible and found.reason=='COMMERCE_DISTRICT_FACTS_UNKNOWN')")

    def test_known_zero_and_no_workers_revoke_without_deleting_selection(self):
        v=fixture();v.execute("workerOverride=true;workerValue=0;audit();assert(gold()==0 and view().factStatus.workers=='CONFIRMED'and state.selected[1]=='DISTRICT_CAMPUS');workerValue=2;audit();assert(gold()==15)")

    def test_foreign_scope_is_rejected_before_native_or_shared_reads(self):
        v=fixture();v.execute("local w=workerReads;local d=counters.dc_capture;com.Audit({player=1,city=c.id});assert(workerReads==w and counters.dc_capture==d)")

    def test_warm_shared_phase_and_explicit_read_cost_remain_bounded(self):
        v=fixture();v.execute("audit();local start=counters.dc_capture;local w=workerReads;local n=effectWrites;f.WithPhase('SAME_INPUTS',function()for i=1,20 do audit()end end);assert(counters.dc_capture==start and workerReads==w+1 and effectWrites==n);start=counters.dc_capture;w=workerReads;for i=1,20 do audit()end;assert(counters.dc_capture==start and workerReads==w+20 and effectWrites==n)")


if __name__=='__main__':unittest.main()
