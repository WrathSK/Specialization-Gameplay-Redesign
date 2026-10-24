"""Target assertions stay strict. Known pre-refactor failures are explicit counterexamples in the runner."""
import unittest
from refactor_harness import Context, measure, legacy_source_observation
from refactor_fixtures import depth_context

class Harness(unittest.TestCase):
    def test_lua51_hidden_context(self):
        c=Context();self.assertEqual(c.eval('_VERSION'),'Lua 5.1')
        self.assertFalse(c.execute('return pcall(ContextPtr.SetUpdate,function()end)')[0])
    def test_ordered_removable_multiple_listeners(self):
        c=Context();c.execute("out='';a=function()out=out..'A'end;b=function()out=out..'B'end;Events.X.Add(a);Events.X.Add(b);Events.X.Fire();assert(out=='AB');out='';Events.X.Order({2,1});Events.X.Fire();assert(out=='BA');Events.X.Order(nil);Events.X.Remove(a);out='';Events.X.Fire();assert(out=='B')")
    def test_context_and_event_namespaces_are_separate(self):
        a,b=Context('Gameplay'),Context('UI');a.execute('hit=0;Events.X.Add(function()hit=hit+1 end);GameEvents.X.Fire();assert(hit==0);Events.X.Fire()')
        self.assertEqual(a.eval('hit'),1);self.assertIsNone(b.eval('hit'))
    def test_publish_is_explicit_and_does_not_run_frames(self):
        c=Context();c.execute('n=0;Events.GameCoreEventPublishComplete.Add(function()n=n+1 end)');self.assertEqual(c.eval('n'),0)
        c.execute('publish()');self.assertEqual(c.eval('n'),1);self.assertEqual(c.eval('frames'),0)
    def test_cold_load_has_new_vm_and_scalar_copy(self):
        a=Context();a.execute('temporary=42');state={'property':{'age':3},'carriers':[1,2]};b=a.reload(state)
        state['property']['age']=99;self.assertIsNone(b.eval('temporary'));self.assertEqual(b.eval('retained.property.age'),3)
    def test_missing_event_is_explicit(self):
        c=Context(missing=['CityBuildingsChanged']);self.assertFalse(c.eval('Events.CityBuildingsChanged'))

class WorkScope(unittest.TestCase):
    def test_T02_unrelated_city_keeps_confirmed_D_capture(self):
        c=depth_context();c.execute('sample(1);sample(2);resetCounts();Events.DistrictBuildProgressChanged.Fire(0,1,1);sample(2)')
        n=c.eval('counts.dc_capture or 0');measure('T02_unrelated_capture',n)
        self.assertEqual(n,0,'S5_D_INVALIDATION_SCOPE')
    def test_T03_warm_capacity_boundaries(self):
        rows=[]
        for n in (8,9,16,32):
            c=depth_context(n);c.execute('for i=1,... do sample(i)end;resetCounts();for i=1,... do sample(i)end',n,n)
            rows.append({'cities':n,'captures':c.eval('counts.dc_capture or 0'),'checks':c.eval('counts.building_check or 0')})
        measure('T03_warm_capacity',rows)
        self.assertEqual([r['captures'] for r in rows],[0,0,0,0],'S6_D_CACHE_THRASH')
    def test_T07_catalogue_presence_and_lazy_detail_cost(self):
        rows=[]
        for n in (4,32,128):
            c=depth_context(1,n);c.execute('v=sample(1);cap=counts.dc_capture;checks=counts.building_check;full=sample(1,true);assert(counts.dc_capture==cap and counts.building_check==checks);assert(v.value.excluded==nil)')
            rows.append({'definitions':n,'presence_checks':c.eval('counts.building_check'),'captures':c.eval('counts.dc_capture')})
        measure('T07_residual_catalogue_cost',rows)
        self.assertEqual([r['presence_checks'] for r in rows],[4,32,128])
    def test_T08_two_same_turn_changes_and_copy_isolation(self):
        c=depth_context();c.execute("a=sample(1);cities[1].present[2]=true;shared.DistrictCompleteness.MarkDirty(0,1);b=sample(1);assert(b.revision>a.revision);cities[1].present[3]=true;shared.DistrictCompleteness.MarkDirty(0,1);d=sample(1);assert(d.revision>b.revision);d.value.domains.DISTRICT_CAMPUS.value=99;assert(sample(1).value.domains.DISTRICT_CAMPUS.value==3)")

class RealConsumers(unittest.TestCase):
    def test_T01_existing_foreign_event_positive_control(self):
        from test_b270_event_scope import make_fixture
        with legacy_source_observation():lua,reset,count=make_fixture(10,True)
        lua.execute('Events.DistrictBuildProgressChanged.Fire(1,1,1,0,0,1)')
        self.assertEqual(count().get('city_scan',0),0);self.assertEqual(count().get('building_check',0),0)
    def test_T04_real_writers_share_one_effective_fact_sample(self):
        from test_b270_event_scope import make_fixture
        with legacy_source_observation():lua,reset,count=make_fixture(0,True)
        # Both actual writers use the real shared phase. Native authority stamp/admission are doubles;
        # independent test_refactor_s5b.ActualWriters additionally proves the same count using the real Store.
        with legacy_source_observation():lua.execute((__import__('pathlib').Path(__file__).resolve().parents[1]/'Mod/EffectiveFacts.lua').read_text())
        lua.execute("foundationReads=0;shared.CityFlowProbe={SupportFacts=function(pid,c)foundationReads=foundationReads+1;return {owner=pid,cityID=c:GetID(),token='REF',specialization='NONE',potential=0}end};shared.CityProgressionStore={FactStamp=function()return 'FIXTURE_AUTHORITY_1'end,Owns=function()return false end};SPCEffectiveFacts.Start(P,shared);resetCounts();shared.EffectiveFacts.WithPhase('REAL_WRITER_TEST',function()shared.Lv2Housing.Audit({player=0,city=0});shared.Lv2GPP.Audit({player=0,city=0})end)")
        n=lua.eval('foundationReads');measure('T04_effective_captures_two_writers',n)
        self.assertEqual(n,1,'S5_FACT_CAPTURE_NOT_SHARED')
    def test_T05_unchanged_pending_has_attempt_budget(self):
        from test_b270_event_scope import make_fixture
        with legacy_source_observation():lua,reset,count=make_fixture(0,True)
        lua.execute("factAttempts=0;shared.EffectiveFacts.Read=function()factAttempts=factAttempts+1;error('FIXTURE_NATIVE_UNAVAILABLE')end;shared.IndustrySupport.Audit({player=0,city=0});resetCounts();factAttempts=0;for i=1,20 do Events.GameCoreEventPublishComplete.Fire()end")
        n=lua.eval('factAttempts');measure('T05_pending_fact_attempts',n)
        self.assertLessEqual(n,1,'S4_PENDING_RETRY_STORM')
    def test_T06_failed_retirement_blocks_positive_writes(self):
        c=Context();c.load('RuntimeWork');c.execute("c={GetOwner=function()return 0 end,GetID=function()return 1 end,GetX=function()return 1 end,GetY=function()return 2 end,GetProperty=function()return 'ref'end};local calls=0;local function apply()SPCRuntimeWork.RetireOnce({},shared,c,'owned',function()calls=calls+1;error('UNKNOWN')end);counts.positive=(counts.positive or 0)+1 end;assert(not pcall(apply));assert(not pcall(apply));assert(calls==2 and not counts.positive)")

    def test_T01_real_chair_honors_city_scope(self):
        from test_b270_event_scope import make_fixture
        with legacy_source_observation():lua,reset,count=make_fixture(0,True)
        lua.execute("other=addCity(0,2,2,2);oldRows=P.Rows;P.Rows=function(t)if t=='SPC_ResearchChairTargets'then return {{BuildingType='BUILDING_LIBRARY'}}end;return oldRows(t)end")
        with legacy_source_observation():lua.execute((__import__('pathlib').Path(__file__).resolve().parents[1]/'Mod/ResearchChair.lua').read_text())
        lua.execute('SPCResearchChair.Start(P,shared);shared.ResearchChair.ready=true;resetCounts();shared.ResearchChair.Audit({player=0,city=0})')
        self.assertIsNone(lua.eval('shared.ResearchChair.definitionError'))
        n=count().get('city_scan',0);measure('T01_chair_city_visits',n)
        self.assertEqual(n,1,'S5_CONSUMER_SCOPE_DISCARDED')
