"""B014 report retirement with a populated Store and the real Gameplay roots."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B464, package
from test_o7_crew_retirement import verify_package_round_trip
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime
from test_pu07_source_attribution import runtime
from test_pu11_package_absence import NATIVE, scalars

REMOVED = 'CompletionRecordProbe.lua'
CONTROL = 'CompletionRecordButton'
ACTION = 'COMPLETION_RECORD_READ'


def context(root,name='Gameplay'):
    retired=root==ROOT
    vfs=PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo',
                   forbidden_globals=('SPCCompletionRecordProbe',) if retired else ())
    return Context(name=name,vfs=vfs,history=None if retired else (root,B464))


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


def load_and_complete(root,saved):
    ctx=context(root)
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
      for i,seed in ipairs(saved.cities) do
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
      end
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
    """,ctx.table(saved))
    ctx.load('Gameplay')
    ctx.execute("""
      local projected=...
      local s=ExposedMembers.SPC_P0
      local store=s.CityProgressionStore
      Events.LoadScreenClose.Fire();publish()
      for _,name in ipairs({'CityProgressionStore','ClaimProjects','BindingProbe','CityJournalProbe','CityFlowProbe','EffectiveFacts'})do
        assert(s.StartStatus[name].state=='OK',name)
      end
      assert(store.UsesNewAuthority and store.FreshReady() and store.HistoryStartStatus()=='EXISTING')
      local b=store.Base(0,city1)
      assert(b.specialization=='RESEARCH' and b.potential==1)
      assert(store.Base(0,city2).specialization=='NONE')
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
      assert(s.LastToken=='retained-journal' and s.Snapshot=='Game进度记录；旧Journal冻结')
      request('COMPLETION_RECORD_READ','retired-report')
      if projected then
        assert(s.LastToken=='retained-journal' and s.Snapshot=='Game进度记录；旧Journal冻结')
      else
        assert(s.LastToken=='retired-report' and s.Snapshot:find('OBSERVED_RECORD_MATCH',1,true),s.Snapshot)
      end
      assert(s.FailureAt==nil)
    """,root==ROOT)
    cold=(scalars(ctx.eval('currentIndex()')),scalars(ctx.eval('currentRecord(1)')),scalars(ctx.eval('currentRecord(2)')))
    assert cold == (saved['properties']['SPC_PROGRESSION_INDEX_V3'],
        *(saved['properties']['SPC_PROGRESSION_CITY_V3_'+saved['cities'][i]['token']] for i in (1,2)))
    assert not any(k.startswith('SPC_PROGRESSION_') for k in scalars(ctx.eval('writeKeys')).values())
    assert ctx.eval('cityWrites') == 0
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
    report=ctx.eval('retainedStoreReport').removeprefix(ctx.eval('SPCP0.VERSION')+' | ')
    return (scalars(ctx.eval('properties')),scalars(ctx.eval('writeKeys')),report,
            ctx.eval('oldRecordReads'),ctx.eval('Events.LoadScreenClose.Count()'),
            ctx.eval('GameEvents.OnDistrictConstructed.Count()'))


def routes(root):
    gp,ui=context(root),context(root,'UI/BackgroundRoutes')
    packets=exercise_proof(gp,ui)
    assert all(c.load_counts['missing']+c.load_counts['failed']==0 for c in (gp,ui))
    return packets,gp.load_counts,ui.load_counts


def panel(root):
    doc,ui=panel_runtime(root/'Mod/UI')
    controls=ui.globals().Controls
    buttons={n.get('ID'):controls[n.get('ID')].hidden for n in doc.iter('GridButton') if n.get('ID')}
    ui.execute("""
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.InheritReadButton.callbacks[Mouse.eLClick]()
      Controls.CityJournalButton.callbacks[Mouse.eLClick]()
      Controls.OpenButton.callbacks[Mouse.eRClick]()
      if ... then Controls.CompletionRecordButton.callbacks[Mouse.eLClick]()end
    """,root!=ROOT)
    return buttons,[dict(p.items()) for p in ui.globals().requests.values()]


class LegacyCompletionRecordRetirement(unittest.TestCase):
    def test_populated_Store_and_first_completion_survive_with_old_value(self):
        saved=save_fixture()
        with package(B464) as previous:
            before,after=(load_and_complete(root,saved) for root in (previous,ROOT))
            for name in ('CityProgressionStore.lua','ClaimProjects.lua','CityJournalProbe.lua',
                         'BindingProbe.lua','CityFlowProbe.lua','FreshBindingHook.lua','EffectiveFacts.lua'):
                self.assertEqual((ROOT/'Mod'/name).read_bytes(),(previous/'Mod'/name).read_bytes())
        self.assertEqual(before[:3],after[:3])
        self.assertEqual((before[3],after[3]),(1,0))
        self.assertEqual(before[4]-after[4],1)
        self.assertEqual(before[5],after[5])
        measure('legacy_completion_record_retirement',dict(populated_cold_records=2,matching_first_completion=True,
            saved_experiment_value_preserved=True,modeled_load_listeners_removed=1,
            modeled_construction_listeners_removed=0,modeled_explicit_legacy_reads=[1,0]))

    def test_real_roots_keep_nonempty_route_proof(self):
        with package(B464) as previous:
            before,after=(routes(root) for root in (previous,ROOT))
        self.assertEqual(before[0],after[0])
        self.assertEqual(len(after[0]),3)
        self.assertEqual(before[2],after[2])
        self.assertEqual(after[1],{**before[1],'attempts':before[1]['attempts']-1,
                                   'completed':before[1]['completed']-1})
        measure('legacy_completion_record_routes',dict(matching_route_packets=3))

    def test_only_the_hidden_completion_record_request_retires(self):
        with package(B464) as previous:
            old_buttons,old_requests=panel(previous)
            new_buttons,new_requests=panel(ROOT)
        self.assertTrue(old_buttons.pop(CONTROL))
        self.assertEqual(old_buttons,new_buttons)
        self.assertEqual(old_requests[-1]['Action'],ACTION)
        self.assertEqual(old_requests[:-1],new_requests)
        self.assertEqual([p['Action'] for p in new_requests],
            ['PROGRESSION_READ','PROGRESSION_STORE_READ','CITY_JOURNAL_READ','EVENT_ORDER_TOGGLE'])

    def test_exact_temporary_switch_and_recovery(self):
        with package(B464) as previous:
            verify_package_round_trip(self,previous/'Mod',ROOT/'Mod',(REMOVED,),'CityProgressionStore.lua')
