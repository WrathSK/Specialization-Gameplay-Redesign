"""Retire hidden B059 override requests while preserving current Dialogue."""
import unittest
from unittest.mock import patch

from refactor_harness import ROOT, measure
from retired_crew_sources import B472, package
from test_o7_legacy_completion_record_retirement import load_cold_store, save_fixture, stored_records
from test_o7_retired_great_work_adjacency_retirement import context
from test_p0_panel_current_layout import panel_runtime
import test_dialogue_effects as dialogue_fixture

CONTROLS = {
    'GWOffButton': 'DIALOGUE_OFF',
    'DialogueTest25Button': 'DIALOGUE_TEST25',
    'DialogueTest50Button': 'DIALOGUE_TEST50',
    'DialogueTest100Button': 'DIALOGUE_TEST100',
}
ACTIONS = list(CONTROLS.values())+['DIALOGUE_AUTO']


def requests(root, source, saved):
    vm = context(root, source)
    cold = load_cold_store(vm, saved)
    vm.execute("""
      local projected=...
      local s=ExposedMembers.SPC_P0
      local d=s.Dialogue
      assert(d.retired and not next(d.test) and not next(d.off))
      assert(s.StartStatus.DialogueProjects.state=='OK' and s.StartStatus.DialogueEffects.state=='OK')
      ExposedMembers.SPC_DialogueGameEra=function()return 'ERA_ANCIENT' end
      local beforeWrites=#writeKeys
      local audit=d.Audit
      local desc=d.Describe
      audits,reads=0,0
      d.Audit=function(...)
        audits=audits+1
        local applied,why=audit(...)
        assert(applied==false and why=='DIALOGUE_LEGACY_WRITER_RETIRED')
        return applied,why
      end
      d.Describe=function(...) reads=reads+1;return desc(...)end
      local function request(action,token)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=token,CityID=city1:GetID(),Page=1})
        assert(s.RequestIngress.action==action and s.RequestDepth==0 and s.FailureAt==nil)
        return s.Snapshot
      end
      currentProject=request('DIALOGUE_PROJECT_READ','project')
      assert(s.LastToken=='project' and currentProject:find('累计记录：+0%',1,true),currentProject)
      currentBaseline=request('GW_BASELINE','baseline')
      assert(s.LastToken=='baseline' and currentBaseline:find('实际收益：旅游业绩限定路径',1,true),currentBaseline)
      currentWorks=request('GREAT_WORK_FACTS_READ','works')
      assert(s.LastToken=='works' and #currentWorks>0)
      for _,action in ipairs({'DIALOGUE_TEST25','DIALOGUE_TEST50','DIALOGUE_TEST100','DIALOGUE_OFF','DIALOGUE_AUTO'})do
        request(action,action)
        if projected then
          assert(s.LastToken=='works' and s.Snapshot==currentWorks and not next(d.test) and not next(d.off))
        else
          assert(s.LastToken==action and s.Snapshot==currentBaseline)
          local percent=tonumber(action:match('^DIALOGUE_TEST(%d+)$'))
          assert(d.off[0]==(action=='DIALOGUE_OFF'))
          if percent then
            assert(d.test[0].city==city1:GetID() and d.test[0].percent==percent)
          else assert(d.test[0]==nil)end
        end
      end
      assert(request('DIALOGUE_PROJECT_READ','kept-project')==currentProject and s.LastToken=='kept-project')
      assert(request('GW_READ','kept-legacy-read')==currentBaseline and s.LastToken=='kept-legacy-read')
      assert(#writeKeys==beforeWrites and cityWrites==0)
    """, source is None)
    assert stored_records(vm)==cold
    assert vm.load_counts['missing']+vm.load_counts['failed']==0
    return tuple(vm.eval(expr) for expr in ('currentProject','currentBaseline','currentWorks','audits','reads'))


def restored_effects(root):
    # Run the actual positive Dialogue owner and both collection receivers.
    auto = dialogue_fixture.auto
    with patch.object(auto.ae,'M',root/'Mod'), patch.object(auto.legacy,'M',root/'Mod'):
        test = dialogue_fixture.Effects()
        # The pinned HD DB already includes the B177 definitions.
        test.sql=auto.legacy.database()
        try:
            vm = test.runtime(boot=False)
            vm.execute("""
              seed(a,'BUILDING_SPC_DIALOGUE_TOTAL_200')
              seed(a,'BUILDING_SPC_B059_D2')
              boot()
              assert(total(a)==5 and total(b)==10,effects.error or effects.startupError)
              assert(not a.present[GameInfo.Buildings.BUILDING_SPC_B059_D2.Index])
            """)
            vm = test.runtime(real=True)
            return vm.execute("""
              sample(1,1,1)
              assert(total(a)==5 and total(b)==10,effects.error or effects.startupError)
              local meaning=finalAmount(a,'SCIENCE')
              sample(2,2,1)
              assert(dialogue.seq[0]==2 and shared.GreatWorkFacts.ack==2)
              assert(total(a)==5 and total(b)==10 and finalAmount(a,'SCIENCE')==meaning)
              return total(a),total(b),shared.GreatWorkFacts.ack
            """)
        finally:
            test.sql.close()


def panel(root, *, retired):
    doc, vm = panel_runtime(root/'Mod/UI')
    controls=vm.globals().Controls
    buttons={e.get('ID'):controls[e.get('ID')].hidden for e in doc.iter('GridButton') if e.get('ID')}
    vm.execute("""
      Controls.GWCityButton.callbacks[Mouse.eLClick]()
      Controls.GWCityButton.callbacks[Mouse.eRClick]()
      Controls.GWReadButton.callbacks[Mouse.eLClick]()
      Controls.GWReadButton.callbacks[Mouse.eRClick]()
      Controls.MeaningProbeButton.callbacks[Mouse.eLClick]()
      if ... then
        Controls.GWOffButton.callbacks[Mouse.eLClick]()
        Controls.DialogueTest25Button.callbacks[Mouse.eLClick]()
        Controls.DialogueTest50Button.callbacks[Mouse.eLClick]()
        Controls.DialogueTest100Button.callbacks[Mouse.eLClick]()
      end
    """, not retired)
    return buttons,[dict(packet.items()) for packet in vm.globals().requests.values()]


class RetiredDialogueOverrides(unittest.TestCase):
    def test_old_requests_stop_before_retired_writer_and_keep_current_readouts(self):
        saved=save_fixture()
        with package(B472) as previous:
            before=requests(previous,B472,saved)
            for name in ('Dialogue.lua','DialogueProjects.lua','DialogueEffects.lua','DialogueProjectModel.lua',
                         'CityProgressionStore.lua','GreatWorkFacts.lua','UI/DialogueRefresh.lua',
                         'LegacyCleanup.lua','LegacyCleanupCatalog.lua','Data/DialogueEffects.sql'):
                self.assertEqual((ROOT/'Mod'/name).read_bytes(),(previous/'Mod'/name).read_bytes())
        after=requests(ROOT,None,saved)
        self.assertEqual(before[:3],after[:3])
        self.assertEqual((before[3:],after[3:]),((5,7),(0,2)))
        measure('retired_dialogue_requests',dict(old_audits=[5,0],readouts='MATCH',property_writes=[0,0]))

    def test_cold_reconstruction_and_real_collection_confirmations_match(self):
        with package(B472) as previous:
            before=restored_effects(previous)
        after=restored_effects(ROOT)
        self.assertEqual(before,after)
        self.assertEqual(after,(5,10,2))
        measure('retired_dialogue_effects',dict(legacy_carrier_withdrawn=True,
            modeled_carrier_bonuses=list(after[:2]),collection_ack=after[2]))

    def test_only_four_hidden_controls_leave_the_panel(self):
        with package(B472) as previous:
            before,old_requests=panel(previous,retired=False)
        after,new_requests=panel(ROOT,retired=True)
        for control in CONTROLS:
            self.assertTrue(before.pop(control))
        self.assertEqual(before,after)
        self.assertEqual(old_requests[:-4],new_requests)
        self.assertEqual([r['Action'] for r in old_requests[-4:]],list(CONTROLS.values()))
        self.assertEqual([r['Action'] for r in new_requests],
            ['DIALOGUE_PROJECT_READ','DIALOGUE_PROJECT_READ','GREAT_WORK_FACTS_READ',
             'GREAT_WORK_FACTS_DETAIL','CULTURE_MEANING_STATUS'])
