"""Retire the two hidden city record requests while preserving their owners."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B469, package
from test_o7_legacy_completion_record_retirement import complete_second_city, load_cold_store, save_fixture, stored_records
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import scalars

CONTROLS = {'CityJournalButton': 'CITY_JOURNAL_READ', 'BindingReadButton': 'BINDING_READ'}


def store_and_reports(root, saved, revision=None):
    vfs = PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo')
    history = (root, revision) if revision else None
    vm = Context(name='Gameplay', vfs=vfs, history=history)
    cold = load_cold_store(vm, saved)
    vm.execute("""
      local retired=...
      local s=ExposedMembers.SPC_P0
      local store=s.CityProgressionStore
      local journal,binding=s.CityJournalProbe,s.BindingProbe
      local journalRead,bindingRead=journal.Read,binding.Read
      manual={journal=0,binding=0}
      journal.Read=function(...) manual.journal=manual.journal+1;return journalRead(...)end
      binding.Read=function(...) manual.binding=manual.binding+1;return bindingRead(...)end
      local before=#writeKeys
      retainedReports={}
      local function request(action,city,token)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,CityID=city:GetID(),Token=token})
        assert(s.RequestIngress.action==action and s.RequestDepth==0 and s.FailureAt==nil)
      end
      for i,city in ipairs({city1,city2})do
        local token='current-'..i
        request('PROGRESSION_STORE_READ',city,token)
        local current=s.Snapshot
        assert(s.LastToken==token and current==store.NativeDescribe(0,city))
        retainedReports[i]=current
        request('CITY_JOURNAL_READ',city,'old-journal')
        if retired then assert(s.LastToken==token and s.Snapshot==current)
        else assert(s.LastToken=='old-journal' and s.Snapshot=='Game进度记录；旧Journal冻结') end
        request('BINDING_READ',city,'old-binding')
        if retired then assert(s.LastToken==token and s.Snapshot==current)
        else assert(s.LastToken=='old-binding' and s.Snapshot==store.Describe(0,city)) end
        local id,status=binding.Resolve(0,city)
        assert(status=='BOUND_MATCH' and id==store.Base(0,city).token)
      end
      journal.EnsureInherited(0)
      assert(#writeKeys==before and cityWrites==0)
    """, revision is None)
    assert stored_records(vm) == cold
    complete_second_city(vm, saved, cold)
    version, reports = vm.eval('SPCP0.VERSION'), vm.eval('retainedReports')
    reports = [reports[i].removeprefix(version+' | ') for i in (1, 2)]
    return (scalars(vm.eval('properties')), reports, scalars(vm.eval('writeKeys')), scalars(vm.eval('manual')))


def panel(root, *, retired):
    doc, vm = panel_runtime(root/'Mod/UI')
    buttons = {e.get('ID'): vm.globals().Controls[e.get('ID')].hidden
               for e in doc.iter('GridButton') if e.get('ID')}
    vm.execute("""
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.InheritReadButton.callbacks[Mouse.eLClick]()
      Controls.NetworkButton.callbacks[Mouse.eRClick]()
      Controls.OpenButton.callbacks[Mouse.eRClick]()
      if ... then
        Controls.CityJournalButton.callbacks[Mouse.eLClick]()
        Controls.BindingReadButton.callbacks[Mouse.eLClick]()
      end
    """, not retired)
    return buttons, [dict(packet.items()) for packet in vm.globals().requests.values()]


class ManualCityRecordReportsRetirement(unittest.TestCase):
    def test_current_records_identity_and_stale_commands_after_cold_load(self):
        saved = save_fixture()
        with package(B469) as previous:
            before = store_and_reports(previous, saved, B469)
            for name in ('CityJournalProbe.lua', 'BindingProbe.lua', 'CityFlowProbe.lua', 'FreshBindingHook.lua',
                         'CityIdentityRead.lua', 'CityInheritance.lua', 'CityProgressionStore.lua', 'EffectiveFacts.lua'):
                self.assertEqual((previous/'Mod'/name).read_bytes(), (ROOT/'Mod'/name).read_bytes())
        after = store_and_reports(ROOT, saved)
        self.assertEqual(before[:3], after[:3])
        self.assertEqual((before[3], after[3]), ({'binding': 2, 'journal': 2}, {'binding': 0, 'journal': 0}))
        measure('manual_city_record_reports_retirement', dict(
            populated_cold_records=2, matching_first_completion_and_store_report=True,
            binding_resolution_matches=True, manual_read_calls={'binding': [2,0], 'journal': [2,0]}))

    def test_only_the_two_hidden_city_record_controls_retire(self):
        with package(B469) as previous:
            old_buttons, old_requests = panel(previous, retired=False)
        new_buttons, new_requests = panel(ROOT, retired=True)
        for control in CONTROLS:
            self.assertTrue(old_buttons.pop(control))
        self.assertEqual(old_buttons, new_buttons)
        self.assertEqual(old_requests[:-2], new_requests)
        self.assertEqual([r['Action'] for r in old_requests[-2:]], list(CONTROLS.values()))
        self.assertEqual([r['Action'] for r in new_requests],
                         ['PROGRESSION_READ', 'PROGRESSION_STORE_READ', 'NETWORK_DETAIL', 'EVENT_ORDER_TOGGLE'])
