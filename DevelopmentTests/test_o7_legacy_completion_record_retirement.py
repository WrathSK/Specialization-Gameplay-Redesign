"""B014 report retirement with a populated Store and the real Gameplay roots."""
from collections import Counter, deque
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B464, B465, B511, B513, B515, B516, B517, B518, B519, RETIRED_ADJACENCY_FILES, RETIRED_CITY_FILES, RETIRED_CITY_STARTS, package, source
from test_o7_crew_retirement import verify_package_round_trip, verify_stable_round_trip
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime
from test_pu07_source_attribution import runtime
from test_pu11_package_absence import NATIVE, scalars

REMOVED = 'CompletionRecordProbe.lua'
CONTROL = 'CompletionRecordButton'
ACTION = 'COMPLETION_RECORD_READ'


def context(root,name='Gameplay',revision=B464):
    retired=root==ROOT
    vfs=PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo',
                   forbidden_globals=('SPCCompletionRecordProbe',) if retired else ())
    return Context(name=name,vfs=vfs,history=None if retired else (root,revision))


def save_fixture():
    fixture,_=runtime()
    fixture.execute("""
      local completed=N.first(3)
      T.complete(completed,'DISTRICT_CAMPUS')
      local pending=N.first(4)
      local r,q=T.record(completed),T.record(pending)
      assert(r.base.specialization=='RESEARCH' and q.progression=='UNASSIGNED')
      local b,f=r.base,r.base.first
      saved={turn=T.now(),properties=T.props(),cities={
        {reference=r.origin,token=b.token,legacy={schema=1,kind='FIRST_OBSERVED_COMPLETION',
          bindingToken=b.token,owner=b.owner,cityID=b.cityID,districtID=f.districtID,
          districtType=f.type,observedFamily=b.specialization,turn=f.turn}},
        {reference=q.origin,token=q.base.token}
      }}
    """)
    return scalars(fixture.eval('saved'))


def stored_records(ctx):
    return tuple(scalars(ctx.eval(expr)) for expr in ('currentIndex()', 'currentRecord(1)', 'currentRecord(2)'))


def load_cold_store(ctx,saved, *, city_flow_missing=False):
    ctx.execute(NATIVE)
    ctx.execute("""
      local saved=...
      properties=saved.properties;turn=saved.turn
      local indexKey='SPC_PROGRESSION_INDEX_V3'
      local cityPrefix='SPC_PROGRESSION_CITY_V3_'
      local marker='SPC_DEV_COMPLETION_B014'
      writeKeys={};cityWrites=0;oldRecordReads=0
      local function read(a,b)return properties[b or a]end
      Game.GetProperty=read
      function Game.SetProperty(a,b,c)
        local k,v=b,c
        if a~=Game then k,v=a,b end
        writeKeys[#writeKeys+1]=k;properties[k]=v
      end
      Map={GetGridSize=function()return 200,100 end}
      GameConfiguration.GetStartTurn=function()return 0 end
      EventSubTypes={FOUND_CITY=-1828126782}
      local objects={}
      local function addCity(seed)
        local i=#objects+1
        local ref=seed.reference
        local row={SPC_DEV_BINDING_B013_TOKEN=seed.token,[marker]=seed.legacy}
        objects[i]={GetID=function()return ref.cityID end,GetOwner=function()return ref.owner end,
          GetX=function()return ref.x end,GetY=function()return ref.y end,GetName=function()return 'City '..i end,
          GetProperty=function(_,k)
            if k==marker then oldRecordReads=oldRecordReads+1 end
            return row[k]
          end,
          SetProperty=function(_,k,v)cityWrites=cityWrites+1;row[k]=v end}
        if i==1 then existingOldRecord=function()return row[marker]end end
        return objects[i]
      end
      for _,seed in ipairs(saved.cities)do addCity(seed) end
      city1,city2=objects[1],objects[2]
      Players[0].GetCities=function()return {
        Members=function()return ipairs(objects)end,
        FindID=function(_,id)for _,c in ipairs(objects)do if c:GetID()==id then return c end end end,
        GetCapitalCity=function()return city1 end,
      }end
      local districts={}
      GameInfo.Districts={}
      for id,name in pairs({[17]='DISTRICT_CAMPUS',[18]='DISTRICT_THEATER'})do
        local def={DistrictType=name,Index=id}
        GameInfo.Districts[id]=def;GameInfo.Districts[name]=def
      end
      CityManager={GetCityAt=function(x,y)
        for _,c in ipairs(objects)do if c:GetX()==x and c:GetY()==y then return c end end
      end,GetDistrictAt=function(x,y)return districts[x..':'..y]end}
      function complete(city,index)
        local x,y=city:GetX()+1,city:GetY()
        districts[x..':'..y]={GetCity=function()return city end,GetOwner=function()return city:GetOwner()end,
          GetID=function()return city:GetID()+500 end,GetType=function()return index end,IsComplete=function()return true end}
        GameEvents.OnDistrictConstructed.Fire(0,index,x,y);publish()
      end
      function currentRecord(i)return properties[cityPrefix..saved.cities[i].token]end
      function currentIndex()return properties[indexKey]end
      function foundNewCity(reverse)
        local id=990+#objects
        local city=addCity({reference={owner=0,cityID=id,x=116+2*#objects,y=8}})
        local x,y=city:GetX(),city:GetY()
        local function init()Events.CityInitialized.Fire(0,id,x,y)end
        local function found()Events.UnitActivate.Fire(0,id+1000,x,y,EventSubTypes.FOUND_CITY,false)end
        if reverse then found();init() else init();found() end
        publish()
        return city
      end
    """,ctx.table(saved))
    ctx.load('Gameplay')
    ctx.execute("""
      local s=ExposedMembers.SPC_P0
      local store=s.CityProgressionStore
      Events.LoadScreenClose.Fire();publish()
      local historical,flowMissing=...
      for _,name in ipairs({'CityProgressionStore','ClaimProjects','EffectiveFacts'})do
        assert(s.StartStatus[name].state=='OK',name)
      end
      for _,name in ipairs({'BindingProbe','CityJournalProbe','CityFlowProbe'})do
        local status=s.StartStatus[name]
        if historical then assert(status.state==(name=='CityFlowProbe' and flowMissing and 'FAILED' or 'OK'),name)
        else assert(status==nil and s[name]==nil,name) end
      end
      assert(store.UsesNewAuthority and store.FreshReady() and store.HistoryStartStatus()=='EXISTING')
      local b=store.Base(0,city1)
      assert(b.specialization=='RESEARCH' and b.potential==1)
      assert(store.Base(0,city2).specialization=='NONE')
    """,ctx.history is not None,city_flow_missing)
    cold=stored_records(ctx)
    assert cold == (saved['properties']['SPC_PROGRESSION_INDEX_V3'],
        *(saved['properties']['SPC_PROGRESSION_CITY_V3_'+saved['cities'][i]['token']] for i in (1,2)))
    assert not any(k.startswith('SPC_PROGRESSION_') for k in scalars(ctx.eval('writeKeys')).values())
    assert ctx.eval('cityWrites') == 0
    return cold


def complete_second_city(ctx,saved,cold):
    ctx.execute("""
      complete(city2,18)
      complete(city2,17)
      local store=ExposedMembers.SPC_P0.CityProgressionStore
      local b=store.Base(0,city2)
      assert(b.specialization=='CULTURE' and b.potential==1)
      assert(currentRecord(2).base.first.type=='DISTRICT_THEATER')
    """)
    assert scalars(ctx.eval('currentIndex()'))==cold[0] and scalars(ctx.eval('currentRecord(1)'))==cold[1]
    assert scalars(ctx.eval('existingOldRecord()'))==saved['cities'][1]['legacy']
    assert ctx.eval('cityWrites')==0 and ctx.load_counts['missing']+ctx.load_counts['failed']==0


def load_and_complete(root,saved, *, journal_retired=False):
    ctx=context(root)
    cold=load_cold_store(ctx,saved)
    ctx.execute("""
      local projected,journalRetired=...
      local s=ExposedMembers.SPC_P0
      if projected then
        assert(s.CompletionRecordProbe==nil and s.StartStatus.CompletionRecordProbe==nil)
      else
        assert(s.StartStatus.CompletionRecordProbe.state=='OK')
        assert(s.CompletionRecordProbe.phase=='AFTER_LOAD_CLOSE' and s.CompletionRecordProbe.hooks.OnDistrictConstructed==nil)
      end
      local function request(action,token)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=token,CityID=city1:GetID()})
        assert(s.RequestIngress.action==action and s.RequestDepth==0)
      end
      request('PROGRESSION_STORE_READ','retained-store')
      assert(s.LastToken=='retained-store' and s.Snapshot:find('已登记',1,true),s.Snapshot)
      retainedStoreReport=s.Snapshot
      request('CITY_JOURNAL_READ','retained-journal')
      if journalRetired then
        assert(s.LastToken=='retained-store' and s.Snapshot==retainedStoreReport)
      else
        assert(s.LastToken=='retained-journal' and s.Snapshot=='Game进度记录；旧Journal冻结')
      end
      local previousToken,previousReport=s.LastToken,s.Snapshot
      request('COMPLETION_RECORD_READ','retired-report')
      if projected then
        assert(s.LastToken==previousToken and s.Snapshot==previousReport)
      else
        assert(s.LastToken=='retired-report' and s.Snapshot:find('OBSERVED_RECORD_MATCH',1,true),s.Snapshot)
      end
      assert(s.FailureAt==nil)
    """,root==ROOT,journal_retired)
    assert stored_records(ctx) == cold
    assert not any(k.startswith('SPC_PROGRESSION_') for k in scalars(ctx.eval('writeKeys')).values())
    assert ctx.eval('cityWrites') == 0
    complete_second_city(ctx,saved,cold)
    report=ctx.eval('retainedStoreReport').removeprefix(ctx.eval('SPCP0.VERSION')+' | ')
    return (scalars(ctx.eval('properties')),scalars(ctx.eval('writeKeys')),report,
            ctx.eval('oldRecordReads'),ctx.eval('Events.LoadScreenClose.Count()'),
            ctx.eval('GameEvents.OnDistrictConstructed.Count()'))


def routes(root,revision=B464,*,retired_culture=False,old_commerce_absent=False):
    gp,ui=context(root,revision=revision),context(root,'UI/BackgroundRoutes',revision)
    if retired_culture:
        forbidden=('SPCCultureInspirationProbe','SPCGWAdjacency','SPCGWAdjacencyModel')
        if old_commerce_absent:
            vfs=PackageVFS(absent=('CommerceConvergence',),forbidden_globals=(*forbidden,'SPCCommerceConvergence'))
        else:
            vfs=PackageVFS(forbidden_globals=forbidden)
        for name in ('CultureInspirationProbe.lua',*RETIRED_ADJACENCY_FILES):
            assert name not in vfs.files and name not in vfs.imports
            assert not (ROOT/'Mod'/name).exists()
        gp=Context(name='Gameplay',vfs=vfs)
    gp.loads=deque(maxlen=768)
    packets=exercise_proof(gp,ui)
    assert all(c.load_counts['missing']+c.load_counts['failed']==0 for c in (gp,ui))
    assert len(gp.loads)==gp.load_counts['completed']
    if retired_culture:
        gp.execute("""local s=ExposedMembers.SPC_P0
          assert(s.StartStatus.CultureInspiration.state=='OK' and s.StartStatus.CultureInspirationProbe==nil)
          assert(s.CultureInspiration and s.CultureInspirationProbe==nil)
          assert(s.StartStatus.CultureMeaning.state=='OK' and s.CultureMeaning)
          assert(s.StartStatus.GreatWorkAdjacency==nil and s.GreatWorkAdjacency==nil)""")
    if old_commerce_absent:
        gp.execute("""local s=ExposedMembers.SPC_P0
          assert(s.StartStatus.CommerceLegacyCleanup.state=='OK' and s.StartStatus.Commerce.state=='OK')
          assert(s.StartStatus.CommerceConvergence==nil and s.CommerceConvergence==nil)""")
    return packets,gp.load_counts,ui.load_counts,Counter(row['module'] for row in gp.loads)


def panel(root, *, retired):
    doc,ui=panel_runtime(root/'Mod/UI')
    controls=ui.globals().Controls
    buttons={n.get('ID'):controls[n.get('ID')].hidden for n in doc.iter('GridButton') if n.get('ID')}
    ui.execute("""
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.InheritReadButton.callbacks[Mouse.eLClick]()
      Controls.CityJournalButton.callbacks[Mouse.eLClick]()
      Controls.OpenButton.callbacks[Mouse.eRClick]()
      if ... then Controls.CompletionRecordButton.callbacks[Mouse.eLClick]()end
    """,not retired)
    return buttons,[dict(p.items()) for p in ui.globals().requests.values()]


class LegacyCompletionRecordRetirement(unittest.TestCase):
    def test_populated_Store_and_first_completion_survive_with_old_value(self):
        saved=save_fixture()
        with package(B464) as previous, package(B465) as retired:
            before=load_and_complete(previous,saved)
            after=load_and_complete(ROOT,saved,journal_retired=True)
            for name in ('CityProgressionStore.lua','ClaimProjects.lua','CityJournalProbe.lua',
                         'BindingProbe.lua','CityFlowProbe.lua','FreshBindingHook.lua','EffectiveFacts.lua'):
                if name in RETIRED_CITY_FILES:
                    self.assertEqual(source(name,B516),(previous/'Mod'/name).read_text())
                    continue
                # EffectiveFacts moved to the Store after the B464/B465 retirement.
                owner = retired if name == 'EffectiveFacts.lua' else ROOT
                self.assertEqual((owner/'Mod'/name).read_bytes(),(previous/'Mod'/name).read_bytes())
        self.assertEqual(before[:3],after[:3])
        self.assertEqual((before[3],after[3]),(1,0))
        # B465 removed the completion listener. The later startup detachment
        # removes three more load callbacks while preserving the read and first completion.
        self.assertEqual(before[4]-after[4],1+len(RETIRED_CITY_STARTS))
        self.assertEqual(before[5],after[5])
        measure('legacy_completion_record_retirement',dict(populated_cold_records=2,matching_first_completion=True,
            saved_experiment_value_preserved=True,modeled_load_listeners_removed=1+len(RETIRED_CITY_STARTS),
            modeled_construction_listeners_removed=0,modeled_explicit_legacy_reads=[1,0]))

    def test_formal_facts_without_city_flow_probe(self):
        saved=save_fixture()
        expected=None
        with package(B515) as baseline:
            for mode in ('present','throw','silent_nil'):
                with self.subTest(mode=mode):
                    missing=mode!='present'
                    profile=PackageVFS(manifest=baseline/'Mod/SpecializationP0.modinfo',
                                       absent=('CityFlowProbe',) if missing else (),
                                       forbidden_globals=('SPCCityFlowProbe',) if missing else (),
                                       missing_include=mode if missing else 'throw')
                    gp=Context(name='Gameplay',vfs=profile,history=(baseline,B515))
                    load_cold_store(gp,saved,city_flow_missing=missing)
                    result=scalars(gp.execute("""
                      local s=ExposedMembers.SPC_P0
                      local facts=s.EffectiveFacts;local writes=#writeKeys
                      local research,proof=facts.ReadWithCarrierReference(0,city1)
                      local unassigned=facts.Read(0,city2)
                      assert(research.specialization=='RESEARCH' and research.active==1)
                      assert(unassigned.specialization=='NONE' and unassigned.active==0)
                      assert(type(proof)=='string' and proof==s.CityProgressionStore.CarrierReferenceStamp(
                       0,city1:GetID(),city1:GetX(),city1:GetY(),research.token))
                      local unknown={GetOwner=function()return 0 end,GetID=function()return 999 end,
                       GetX=function()return 150 end,GetY=function()return 70 end}
                      local ok,why=pcall(facts.Read,0,unknown)
                      assert(not ok and why:find('FOUNDATION_EVIDENCE_PENDING',1,true))
                      assert(#writeKeys==writes and cityWrites==0)
                      return {research,unassigned,proof}
                    """))
                    self.assertEqual(gp.load_counts['missing'],int(missing))
                    if expected is None:
                        expected=result
                    self.assertEqual(result,expected)
        measure('formal_city_facts_without_legacy_probe',dict(cold_records=2,
            matching_store_witness=True,unregistered_city='FOUNDATION_EVIDENCE_PENDING',
            no_fact_write=True,modeled_vfs=['present','throw','silent_nil'],source=B515))

    def test_current_roots_admit_cities_and_lock_first_completion_with_all_city_shells_absent(self):
        def exercise(ctx):
            cold=load_cold_store(ctx,saved)
            completed=scalars(ctx.execute("""
              local s=ExposedMembers.SPC_P0
              local store,facts=s.CityProgressionStore,s.EffectiveFacts
              local read,reference=facts.ReadWithCarrierReference(0,city1)
              assert(read.specialization=='RESEARCH' and read.active==1)
              assert(reference==store.CarrierReferenceStamp(0,city1:GetID(),city1:GetX(),city1:GetY(),read.token))
              local admitted={}
              for i=1,2 do
                local city=foundNewCity(i==2)
                local base=store.Base(0,city)
                assert(base.specialization=='NONE' and base.potential==0 and store.Owns(city))
                assert(city:GetProperty('SPC_DEV_BINDING_B013_TOKEN')==base.token)
                assert(facts.Read(0,city).potential==0)
                local first,second=i==1 and 17 or 18,i==1 and 18 or 17
                complete(city,first)
                complete(city,second)
                local applied=facts.Read(0,city)
                local expected=i==1 and 'RESEARCH' or 'CULTURE'
                assert(applied.specialization==expected and applied.potential==1)
                local record=properties['SPC_PROGRESSION_CITY_V3_'..base.token]
                local family=i==1 and 'DISTRICT_CAMPUS' or 'DISTRICT_THEATER'
                assert(record.base.first.type==family)
                assert(store.ClaimState(0,city)==nil)
                admitted[i]=record
              end
              assert(cityWrites==2 and oldRecordReads==0)
              return {admitted=admitted,index=currentIndex(),writes=writeKeys}
            """))
            self.assertEqual(stored_records(ctx)[1:],cold[1:])
            self.assertEqual(ctx.load_counts['missing']+ctx.load_counts['failed'],0)
            return completed, ctx.eval('Events.LoadScreenClose.Count()')

        saved=save_fixture()
        with package(B515) as baseline:
            expected,prior_load_callbacks=exercise(context(baseline,revision=B515))
        for mode in ('throw','silent_nil'):
            with self.subTest(mode=mode):
                profile=PackageVFS(forbidden_globals=tuple('SPC'+n.removesuffix('.lua') for n in RETIRED_CITY_FILES),
                                   missing_include=mode)
                for name in RETIRED_CITY_FILES:
                    self.assertFalse((ROOT/'Mod'/name).exists())
                    self.assertNotIn(name,profile.files)
                    self.assertNotIn(name,profile.imports)
                ctx=Context(name='Gameplay',vfs=profile)
                result,callbacks=exercise(ctx)
                self.assertEqual(result,expected)
                self.assertEqual(prior_load_callbacks-callbacks,len(RETIRED_CITY_STARTS))
        measure('store_registration_without_legacy_city_starts',dict(
            populated_cold_records=2,fresh_registrations=2,first_completions=2,
            old_files_requested=0,physically_absent_paths=list(RETIRED_CITY_FILES),
            modeled_load_callbacks_removed=len(RETIRED_CITY_STARTS),
            matched_index_token_records_and_writes=True,modeled_vfs=['throw','silent_nil']))

    def test_real_roots_keep_nonempty_route_proof(self):
        with (package(B464) as previous, package(B511) as pre_handoff,
              package(B513) as no_experiments, package(B515) as no_writers, package(B517) as no_city_probes,
              package(B518) as no_inspiration_probe, package(B519) as no_adjacency):
            stages = [routes(previous), routes(pre_handoff,B511), routes(no_experiments,B513),
                      routes(no_writers,B515), routes(no_city_probes,B517), routes(no_inspiration_probe,B518),
                      routes(no_adjacency,B519), routes(ROOT,retired_culture=True,old_commerce_absent=True)]
        self.assertEqual(len(stages[0][0]),3)
        retirements=(
            ('CompletionRecordProbe.lua',),
            ('PurchaseProbe.lua','GreatWorkProbe.lua'),
            ('CopyYields.lua','StandardizationDiscount.lua','RuntimeWork.lua','CityReference.lua','SampleLifecycle.lua'),
            RETIRED_CITY_FILES,
            ('CultureInspirationProbe.lua','CurrentSpecializationFacts.lua','NetworkInput.lua'),
            RETIRED_ADJACENCY_FILES,
            ('CommerceConvergence.lua','RuntimeWork.lua','CityReference.lua','Tombstones.lua'),
        )
        for before, after, retired in zip(stages, stages[1:], retirements):
            self.assertEqual(before[0],after[0])
            self.assertEqual(before[2],after[2])
            self.assertEqual(before[3]-after[3],Counter(retired))
            self.assertFalse(after[3]-before[3])
            self.assertEqual(after[1],{**before[1],'attempts':before[1]['attempts']-len(retired),
                                       'completed':before[1]['completed']-len(retired)})
        measure('legacy_completion_record_routes',dict(matching_route_packets=3,
            experiment_module_loads_removed=2, industrial_module_loads_removed=5,
            legacy_city_module_loads_removed=len(RETIRED_CITY_FILES), inspiration_includes_removed=3,
            meaning_includes_removed=len(RETIRED_ADJACENCY_FILES),commerce_legacy_includes_removed=4))

    def test_only_the_hidden_completion_record_request_retires(self):
        with package(B464) as previous, package(B465) as retired:
            old_buttons,old_requests=panel(previous,retired=False)
            new_buttons,new_requests=panel(retired,retired=True)
        self.assertTrue(old_buttons.pop(CONTROL))
        self.assertEqual(old_buttons,new_buttons)
        self.assertEqual(old_requests[-1]['Action'],ACTION)
        self.assertEqual(old_requests[:-1],new_requests)
        self.assertEqual([p['Action'] for p in new_requests],
            ['PROGRESSION_READ','PROGRESSION_STORE_READ','CITY_JOURNAL_READ','EVENT_ORDER_TOGGLE'])

    def test_exact_temporary_switch_and_recovery(self):
        with package(B464) as previous, package(B465) as retired:
            verify_package_round_trip(self,previous/'Mod',retired/'Mod',(REMOVED,),'CityProgressionStore.lua')

    def test_exact_legacy_city_package_switch_and_recovery(self):
        with package(B516) as previous, package(B517) as retired:
            prior,current=previous/'Mod',retired/'Mod'
            for name in ('CityProgressionStore.lua','CityIdentityRead.lua','EffectiveFacts.lua',
                         'ClaimProjects.lua','LegacyCleanup.lua','Gameplay.lua'):
                self.assertEqual((prior/name).read_bytes(),(current/name).read_bytes(),name)
            verify_package_round_trip(self,prior,current,RETIRED_CITY_FILES,'CityProgressionStore.lua')
            verify_stable_round_trip(self,prior,current,RETIRED_CITY_FILES)
