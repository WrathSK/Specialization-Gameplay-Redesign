"""Remove the B060 manual requests and retain the reused memory control."""
import unittest
from unittest.mock import patch

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B471, B472, package
from test_o7_legacy_completion_record_retirement import load_cold_store, save_fixture, stored_records
from test_o7_route_observer_retirement import exercise_proof
from test_o7_runtime_gc import GC_NATIVE
from test_p0_panel_current_layout import panel_runtime
import test_culture_meaning_automatic as meaning_fixture

CONTROLS = {'GWAOffButton': 'GWA_OFF', 'GWAAutoButton': 'GWA_AUTO'}


def context(root, source, name='Gameplay'):
    history = (root, source) if source else None
    return Context(name=name, vfs=PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo'), history=history)


def requests_and_routes(root, source):
    gp, ui = (context(root, source, name) for name in ('Gameplay', 'UI/BackgroundRoutes'))
    packets = exercise_proof(gp, ui)
    gp.execute("""
      local retired=...
      local s=ExposedMembers.SPC_P0
      local d=s.GreatWorkAdjacency
      assert(d.retired and not next(d.off) and s.StartStatus.MemoryObservation.state=='OK')
      local beforeRevision=ExposedMembers.SPC_RuntimeUIRevision
      local audit=d.Audit
      auditCalls,readCalls=0,0
      d.Audit=function(...) auditCalls=auditCalls+1;return audit(...)end
      local describe=d.Describe
      d.Describe=function(...) readCalls=readCalls+1;return describe(...)end
      local function request(action,token)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=token,CityID=1,Page=1})
        assert(s.RequestIngress.action==action and s.RequestDepth==0 and s.FailureAt==nil)
      end
      request('NETWORK_READ','kept')
      local network=s.Snapshot
      assert(s.LastToken=='kept' and net.TransactionCurrent(0))
      for _,action in ipairs({'GWA_READ','GWA_OFF','GWA_AUTO'})do
        request(action,action)
        if retired then
          assert(s.LastToken=='kept' and s.Snapshot==network)
        elseif action=='GWA_READ' then
          assert(s.LastToken==action and s.Snapshot:find('旧巨作相邻已退役',1,true))
        else
          assert(s.LastToken==action and s.Snapshot:find('GWA_RETIRED',1,true))
        end
      end
      assert(auditCalls==0 and not next(d.off) and ExposedMembers.SPC_RuntimeUIRevision==beforeRevision)
      request('NETWORK_READ','end')
      assert(s.LastToken=='end' and s.Snapshot==network and net.TransactionCurrent(0))
    """, source is None)
    assert all(vm.load_counts['missing'] + vm.load_counts['failed'] == 0 for vm in (gp, ui))
    return packets, gp.eval('readCalls')


def memory_report(root, source, saved):
    # The route fixture has no admitted cities. The memory report reads the
    # actual Store's record count, so use the populated cold-load fixture.
    vm = context(root, source)
    vm.execute(GC_NATIVE)
    cold = load_cold_store(vm, saved)
    vm.execute("""
      local s=ExposedMembers.SPC_P0
      local before=#writeKeys
      local function request(action,token)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=token,CityID=city1:GetID(),Page=1})
        assert(s.LastToken==token and s.RequestDepth==0 and s.FailureAt==nil)
      end
      request('MEMORY_BEGIN','memory-start')
      assert(s.Snapshot:find('运行中',1,true),s.Snapshot)
      memoryStart=s.Snapshot
      request('MEMORY_READ','memory-read')
      assert(s.Snapshot:find('手动读取',1,true) and gcCalls==0,s.Snapshot)
      memoryRead=s.Snapshot
      assert(#writeKeys==before and cityWrites==0)
    """)
    assert stored_records(vm)==cold
    return vm.eval('memoryStart'), vm.eval('memoryRead')


def meaning_cold(root):
    # Run the current Meaning owner against the established two-city fixture.
    with patch.object(meaning_fixture.ae, 'M', root/'Mod'), patch.object(meaning_fixture.legacy, 'M', root/'Mod'):
        test = meaning_fixture.AutomaticMeaningTests()
        test.sql = meaning_fixture.legacy.database()
        try:
            vm = test.runtime(ready=False)
            return vm.execute("""
              seed(a,'BUILDING_SPC_B060_SCIENCE_P1')
              assert(oldCount(a)==1)
              fire('LoadScreenClose')
              assert(meaning.ready)
              return oldCount(a),finalAmount(a,'SCIENCE'),finalAmount(b,'SCIENCE')
            """)
        finally:
            test.sql.close()


def panel(root, *, retired):
    doc, vm = panel_runtime(root/'Mod/UI')
    controls=vm.globals().Controls
    buttons={e.get('ID'):controls[e.get('ID')].hidden for e in doc.iter('GridButton') if e.get('ID')}
    vm.execute("""
      assert(Controls.GWAReadButtonCaption.text=='内存观测')
      Controls.GWAReadButton.callbacks[Mouse.eLClick]()
      Controls.GWAReadButton.callbacks[Mouse.eRClick]()
      Controls.MeaningProbeButton.callbacks[Mouse.eLClick]()
      Controls.GWReadButton.callbacks[Mouse.eRClick]()
      Controls.NetworkButton.callbacks[Mouse.eRClick]()
      if ... then
        Controls.GWAOffButton.callbacks[Mouse.eLClick]()
        Controls.GWAAutoButton.callbacks[Mouse.eLClick]()
      end
    """, not retired)
    return (buttons, [dict(packet.items()) for packet in vm.globals().requests.values()],
            vm.eval('eventAdds.SystemUpdateUI'))


class RetiredGreatWorkAdjacency(unittest.TestCase):
    def test_stale_adjacency_commands_leave_current_route_proof_intact(self):
        with package(B471) as previous:
            before, before_reads = requests_and_routes(previous, B471)
            for name in ('GreatWorkAdjacency.lua', 'CultureMeaning.lua', 'GreatWorkFacts.lua', 'UI/DialogueRefresh.lua',
                         'LegacyCleanup.lua', 'LegacyCleanupCatalog.lua', 'NetworkBridge.lua'):
                self.assertEqual((previous/'Mod'/name).read_bytes(), (ROOT/'Mod'/name).read_bytes())
        after, after_reads = requests_and_routes(ROOT, None)
        self.assertEqual(before, after)
        self.assertEqual(len(after), 3)
        self.assertEqual((before_reads, after_reads), (1, 0))
        measure('retired_gwa_requests', dict(manual_read_calls=[1,0], matching_route_packets=3,
            retired_audit_calls=[0,0], carrier_and_session_state_preserved=True))

    def test_memory_observation_reports_match_with_populated_store(self):
        saved = save_fixture()
        with package(B471) as previous:
            before = memory_report(previous, B471, saved)
        after = memory_report(ROOT, None, saved)
        self.assertEqual(before, after)
        measure('retired_gwa_memory', dict(current_commands=['MEMORY_BEGIN','MEMORY_READ'], reports='MATCH'))

    def test_cold_meaning_withdraws_legacy_and_rebuilds_current_carriers(self):
        with package(B471) as previous:
            before = meaning_cold(previous)
        after = meaning_cold(ROOT)
        self.assertEqual(before, after)
        self.assertEqual(after, (0,3,3))
        measure('retired_gwa_meaning', dict(old_carriers=after[0], science_values=list(after[1:])))

    def test_panel_retains_memory_and_removes_only_one_update_listener(self):
        with package(B471) as previous, package(B472) as retired:
            old_buttons, old_requests, old_updates = panel(previous, retired=False)
            new_buttons, new_requests, new_updates = panel(retired, retired=True)
        current_buttons, current_requests, current_updates = panel(ROOT, retired=True)
        self.assertTrue(CONTROLS.keys().isdisjoint(current_buttons))
        self.assertEqual((current_requests, current_updates), (new_requests, new_updates))
        for control in CONTROLS:
            self.assertTrue(old_buttons.pop(control))
        self.assertEqual(old_buttons, new_buttons)
        self.assertEqual(old_requests[:-2], new_requests)
        self.assertEqual([r['Action'] for r in old_requests[-2:]], list(CONTROLS.values()))
        self.assertEqual([r['Action'] for r in new_requests],
            ['MEMORY_BEGIN','MEMORY_READ','CULTURE_MEANING_STATUS','GREAT_WORK_FACTS_DETAIL','NETWORK_DETAIL'])
        self.assertEqual((old_updates, new_updates), (2, 1))
        measure('retired_gwa_panel', dict(system_update_listeners=[2,1], reused_memory_control=True))
