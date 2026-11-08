"""The hidden B021 request retires while its production and recovery owners stay."""
import unittest
from unittest.mock import patch

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B468, B469, package
from test_p0_panel_current_layout import panel_runtime
import test_o7_legacy_completion_record_retirement as store_fixture


def store_and_request(root, saved, revision, *, retired):
    vfs = PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo')
    history = (root, revision)
    vm = Context(name='Gameplay', vfs=vfs, history=history)
    with patch.multiple(store_fixture, ROOT=root, context=lambda path: vm):
        completed = store_fixture.load_and_complete(root, saved)
    vm.execute("""
      local retired=...
      local s=ExposedMembers.SPC_P0
      local flow=s.CityFlowProbe
      assert(flow.ready and type(flow.Read)=='function' and type(flow.ResumeInherited)=='function')
      local reads=0
      local original=flow.Read
      flow.Read=function(...) reads=reads+1;return original(...)end
      local beforeCityWrites, beforeGameWrites = cityWrites, #writeKeys
      local function request(action,cid,token)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,CityID=cid,Token=token})
        assert(s.RequestIngress.action==action and s.RequestDepth==0 and s.FailureAt==nil)
      end
      request('CITY_JOURNAL_READ',city1:GetID(),'kept')
      local journal=s.Snapshot
      for i,city in ipairs({city1,city2})do
        local token='old-'..i
        request('CITY_FLOW_READ',city:GetID(),token)
        if retired then
          assert(s.LastToken=='kept' and s.Snapshot==journal and s.Stage=='ACK CITY_JOURNAL')
        else
          assert(s.LastToken==token and s.Snapshot=='Game进度记录；旧Flow冻结' and s.Stage=='ACK CITY_FLOW')
        end
        local f=flow.SupportFacts(0,city)
        assert(f.token==s.CityProgressionStore.Base(0,city).token and f.potential==1)
        assert(f.specialization==(i==1 and 'RESEARCH' or 'CULTURE'))
      end
      request('CITY_FLOW_READ',999999,'missing')
      if retired then assert(s.LastToken=='kept' and s.Snapshot==journal)
      else assert(s.LastToken==nil and s.Stage=='REJECT_CITY') end
      assert(cityWrites==beforeCityWrites and #writeKeys==beforeGameWrites)
      manualReads=reads
    """, retired)
    return completed, vm.eval('manualReads')


def panel(root, *, retired):
    doc, vm = panel_runtime(root/'Mod/UI')
    buttons = {e.get('ID'): vm.globals().Controls[e.get('ID')].hidden
               for e in doc.iter('GridButton') if e.get('ID')}
    vm.execute("""
      Controls.CityJournalButton.callbacks[Mouse.eLClick]()
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.InheritReadButton.callbacks[Mouse.eLClick]()
      Controls.NetworkButton.callbacks[Mouse.eRClick]()
      if ... then Controls.CityFlowButton.callbacks[Mouse.eLClick]()end
    """, not retired)
    return buttons, [dict(packet.items()) for packet in vm.globals().requests.values()]


class ManualCityFlowRetirement(unittest.TestCase):
    def test_cold_store_and_support_facts_survive_stale_city_flow_requests(self):
        saved = store_fixture.save_fixture()
        with package(B468) as previous, package(B469) as after:
            old, old_reads = store_and_request(previous, saved, B468, retired=False)
            for name in ('CityFlowProbe.lua', 'CityJournalProbe.lua', 'BindingProbe.lua', 'FreshBindingHook.lua',
                         'CityInheritance.lua', 'EffectiveFacts.lua', 'CityProgressionStore.lua', 'NetworkInput.lua'):
                self.assertEqual((previous/'Mod'/name).read_bytes(), (ROOT/'Mod'/name).read_bytes())
            new, new_reads = store_and_request(after, saved, B469, retired=True)
        self.assertEqual(old, new)
        self.assertEqual((old_reads, new_reads), (2, 0))
        measure('manual_city_flow_retirement', dict(
            populated_cold_records=2, matching_first_completion_and_support_facts=True,
            manual_flow_read_calls=[2, 0]))

    def test_only_the_hidden_city_flow_control_retires(self):
        with package(B468) as previous, package(B469) as after:
            old_buttons, old_requests = panel(previous, retired=False)
            new_buttons, new_requests = panel(after, retired=True)
        self.assertTrue(old_buttons.pop('CityFlowButton'))
        self.assertEqual(old_buttons, new_buttons)
        self.assertEqual(old_requests[:-1], new_requests)
        self.assertEqual(old_requests[-1]['Action'], 'CITY_FLOW_READ')
        self.assertEqual([row['Action'] for row in new_requests],
                         ['CITY_JOURNAL_READ', 'PROGRESSION_READ', 'PROGRESSION_STORE_READ', 'NETWORK_DETAIL'])
