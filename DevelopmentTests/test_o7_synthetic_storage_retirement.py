"""Scoped package replay for the B012/B019 experiment retirement."""
import unittest

from refactor_harness import Context, PackageVFS, measure
from retired_crew_sources import B463, B464, package
from test_o7_crew_retirement import verify_package_round_trip
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import NATIVE, scalars

REMOVED = ('EnvelopeProbe.lua', 'StorageProbe.lua')
GLOBALS = ('SPCEnvelopeProbe', 'SPCStorageProbe')
CONTROLS = ('EnvelopeReadButton', 'EnvelopeNextButton', 'StorageReadButton', 'StorageWriteButton')
ACTIONS = ('ENVELOPE_READ', 'ENVELOPE_NEXT', 'STORAGE_READ', 'STORAGE_WRITE')
EXPERIMENT_KEYS = {'SPC_DEV_STORAGE_B012_P0', 'SPC_DEV_ENVELOPE_B019_P0'}


def context(root, revision, name='Gameplay'):
    retired = revision == B464
    profile = PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo', forbidden_globals=GLOBALS if retired else ())
    return Context(name=name, vfs=profile, history=(root,revision))


def store_session(root, revision, seed, fresh):
    ctx = context(root, revision)
    ctx.execute(NATIVE)
    ctx.execute("""
      local seed,fresh=...
      legacyReads=0;legacyWrites=0;rosterReads=0;ordinaryWrites={}
      local function legacy(key)
        return key:find('^SPC_DEV_STORAGE_B012_P') or key:find('^SPC_DEV_ENVELOPE_B019_P')
      end
      properties.SPC_DEV_ENVELOPE_B019_P0=seed
      properties.SPC_DEV_STORAGE_B012_P1={untouched=true,nested={example=42}}
      properties.SPC_DEV_ENVELOPE_B019_P1={untouched=true,otherOwner=1}
      properties.FOREIGN_GAME_SENTINEL={example='preserve'}
      if not fresh then properties.SPC_PROGRESSION_INDEX_V3={schema=3,counter=0,entries={}}end
      function Game.GetProperty(obj,key)
        key=key or obj
        if legacy(key) then legacyReads=legacyReads+1 end
        return properties[key]
      end
      function Game.SetProperty(obj,key,value)
        if obj~=Game then key,value=obj,key end
        if legacy(key) then legacyWrites=legacyWrites+1 else ordinaryWrites[#ordinaryWrites+1]=key end
        properties[key]=value
      end
      Map={GetGridSize=function()return 80,52 end}
      GameConfiguration.GetStartTurn=Game.GetCurrentGameTurn
      PlayerManager={GetAliveIDs=function()rosterReads=rosterReads+1;return {0}end}
    """, ctx.table(seed), fresh)
    ctx.load('Gameplay')
    ctx.execute("""
      local retired,fresh=...
      local s=ExposedMembers.SPC_P0
      Events.LoadScreenClose.Fire();publish()
      for _,name in ipairs({'CityProgressionStore','ClaimProjects','NetworkBridge','CompletionRecordProbe','CityJournalProbe'})do
        assert(s.StartStatus[name].state=='OK',name)
      end
      local store=s.CityProgressionStore
      assert(store.UsesNewAuthority and store.FreshReady() and store.FailureReport()==nil)
      assert(store.HistoryStartStatus()==(fresh and 'FRESH' or 'EXISTING'))
      assert(legacyWrites==0)
      if retired then
        assert(s.EnvelopeProbe==nil and s.StorageProbe==nil)
        assert(s.StartStatus.EnvelopeProbe==nil and s.StartStatus.StorageProbe==nil)
      else
        assert(s.EnvelopeProbe.ready and s.EnvelopeProbe.players[0].autoStep==1)
        assert(s.StartStatus.EnvelopeProbe.state=='OK' and s.StartStatus.StorageProbe.state=='OK')
      end

      local city={GetID=function()return 11 end,GetOwner=function()return 0 end,
                  GetX=function()return 21 end,GetY=function()return 12 end,GetProperty=function()return nil end}
      Players[0]:GetCities().FindID=function(_,id)if id==11 then return city end end
      function request(action,token,stage,id)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=token,ExpectedStage=stage,CityID=id})
      end
      request('PROGRESSION_STORE_READ','store',nil,11)
      assert(s.LastToken=='store' and s.Snapshot:find('尚无已确认的新局记录',1,true))
      local description=s.Snapshot
      request('CITY_JOURNAL_READ','journal',nil,11)
      assert(s.LastToken=='journal' and s.Snapshot=='Game进度记录；旧Journal冻结')
      control={history=store.HistoryStartStatus(),store=description,journal=s.Snapshot}
    """, revision == B464, fresh)
    loaded = scalars(ctx.eval('properties'))
    writes = scalars(ctx.eval('ordinaryWrites'))
    observations = [ctx.eval(name) for name in ('legacyReads','rosterReads','Events.LoadScreenClose.Count()')]
    ctx.execute("""
      local retired=...
      local s=ExposedMembers.SPC_P0
      local cases={
        {'STORAGE_READ','EMPTY'},{'STORAGE_WRITE','MATCH'},{'STORAGE_WRITE','MATCH_NO_WRITE'},
        {'ENVELOPE_READ','READ_ONLY'},{'ENVELOPE_NEXT','SAVED_READBACK_MATCH',1},
        {'ENVELOPE_NEXT','STALE_NO_WRITE',1},
      }
      local count=s.RequestIngress.count
      for i,case in ipairs(cases) do
        local token='retired-case-'..i
        request(case[1],token,case[3])
        assert(s.RequestIngress.count==count+i and s.RequestIngress.action==case[1])
        assert(s.FailureAt==nil and s.RequestDepth==0)
        if retired then
          assert(s.LastToken=='journal' and s.RequestToken=='journal' and s.Stage=='ACK CITY_JOURNAL')
          assert(s.Snapshot==control.journal)
        else
          assert(s.LastToken==token and s.Snapshot:find(case[2],1,true))
        end
      end
      assert(legacyWrites==(retired and 0 or 2))
      if retired then assert(legacyReads==0)end
    """, revision == B464)
    assert ctx.load_counts['missing']+ctx.load_counts['failed']==0
    assert scalars(ctx.eval('ordinaryWrites'))==writes
    return loaded, scalars(ctx.eval('properties')), writes, observations, scalars(ctx.eval('control'))


def routes(root, revision):
    gp,ui = (context(root,revision,name) for name in ('Gameplay','UI/BackgroundRoutes'))
    packets = exercise_proof(gp,ui)
    assert all(c.load_counts['missing']+c.load_counts['failed']==0 for c in (gp,ui))
    return packets,gp.load_counts,ui.load_counts


def panel(root, revision):
    doc,ui = panel_runtime(root/'Mod/UI')
    controls = ui.globals().Controls
    buttons = {e.get('ID'):controls[e.get('ID')].hidden for e in doc.iter('GridButton') if e.get('ID')}
    ui.execute("""
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.InheritReadButton.callbacks[Mouse.eLClick]()
      Controls.CityJournalButton.callbacks[Mouse.eLClick]()
      Controls.CompletionRecordButton.callbacks[Mouse.eLClick]()
      Controls.OpenButton.callbacks[Mouse.eRClick]()
      if ... then
        selectedCity=nil
        ExposedMembers.SPC_P0.EnvelopeProbe={players={[0]={step=1}}}
        for _,name in ipairs({'EnvelopeReadButton','EnvelopeNextButton','StorageReadButton','StorageWriteButton'})do
          Controls[name].callbacks[Mouse.eLClick]()
        end
      end
    """, revision == B463)
    return buttons,[dict(p.items()) for p in ui.globals().requests.values()]


class SyntheticStorageRetirement(unittest.TestCase):
    def test_current_store_and_saved_experiment_values_survive(self):
        with package(B463) as previous, package(B464) as retired:
            seed = context(previous,B463)
            seed.load('EnvelopeProbe')
            stored = scalars(seed.eval('SPCEnvelopeProbe.Expected(0,1)'))
            for fresh in (False,True):
                with self.subTest(fresh=fresh):
                    old = store_session(previous,B463,stored,fresh)
                    new = store_session(retired,B464,stored,fresh)
                    self.assertEqual(old[0],new[0])
                    self.assertEqual(new[0],new[1])
                    self.assertEqual(old[2],new[2])
                    self.assertEqual(list(new[2].values()).count('SPC_PROGRESSION_INDEX_V3'),int(fresh))
                    self.assertEqual(old[3][:2],[2,1])
                    self.assertEqual(new[3][:2],[0,0])
                    self.assertEqual(old[3][2]-new[3][2],1)
                    self.assertEqual(old[4],new[4])
                    changed={key for key in old[1].keys()|new[1].keys() if old[1].get(key)!=new[1].get(key)}
                    self.assertEqual(changed,EXPERIMENT_KEYS)
                    self.assertEqual(old[1]['SPC_DEV_ENVELOPE_B019_P0']['storageRevision'],2)
            for name in ('CityProgressionStore.lua','CityJournalProbe.lua','CompletionRecordProbe.lua','ClaimProjects.lua'):
                self.assertEqual((retired/'Mod'/name).read_bytes(),(previous/'Mod'/name).read_bytes())
        measure('synthetic_storage_retirement',dict(modeled_load_listeners_removed=1,
            modeled_legacy_load_reads=[2,0],modeled_roster_reads=[1,0],modeled_manual_writes=[2,0],
            store_index_write_counts_fresh_and_existing=[1,0],saved_experiment_values_preserved=True))

    def test_real_roots_keep_nonempty_route_proofs(self):
        with package(B463) as previous, package(B464) as retired:
            old,new = routes(previous,B463),routes(retired,B464)
        self.assertEqual(old[0],new[0])
        self.assertEqual(len(new[0]),3)
        self.assertEqual(old[2],new[2])
        self.assertEqual(new[1],{**old[1],'attempts':old[1]['attempts']-2,'completed':old[1]['completed']-2})
        measure('synthetic_storage_route_proof',dict(matching_route_packets=3))

    def test_only_the_four_hidden_controls_and_requests_retire(self):
        with package(B463) as previous, package(B464) as retired:
            old_buttons,old_requests = panel(previous,B463)
            new_buttons,new_requests = panel(retired,B464)
        for name in CONTROLS:
            self.assertTrue(old_buttons.pop(name))
        self.assertEqual(old_buttons,new_buttons)
        self.assertEqual([p['Action'] for p in new_requests],
            ['PROGRESSION_READ','PROGRESSION_STORE_READ','CITY_JOURNAL_READ','COMPLETION_RECORD_READ','EVENT_ORDER_TOGGLE'])
        self.assertEqual(old_requests[:5],new_requests)
        self.assertEqual([p['Action'] for p in old_requests[5:]],list(ACTIONS))
        self.assertTrue(all('CityID' not in p for p in old_requests[5:]))
        self.assertEqual(old_requests[6]['ExpectedStage'],1)
        self.assertTrue(all('ExpectedStage' not in p for p in new_requests))

    def test_exact_temporary_switch_and_recovery(self):
        with package(B463) as previous, package(B464) as retired:
            verify_package_round_trip(self,previous/'Mod',retired/'Mod',REMOVED,'CityProgressionStore.lua')
