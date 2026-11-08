"""Retire the old marker commands while keeping saved markers and current reports."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B467, package
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import scalars

CONTROLS = {'CaptureButton': 'CAPTURE', 'MarkButton': 'MARK_CITY'}


def roots(root, revision=None):
    history = (root, revision) if revision else None
    vfs = PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo')
    gp, ui = (Context(name=name, vfs=vfs, history=history) for name in ('Gameplay', 'UI/BackgroundRoutes'))
    packets = exercise_proof(gp, ui)
    gp.execute("""
      local retired=...
      local s=ExposedMembers.SPC_P0
      local key='SPC_P0_MARKER'
      local city2=Players[0]:GetCities():FindID(2)
      local values={[1]='saved-marker'}
      markerReads,markerWrites=0,0
      for _,city in ipairs({city1,city2})do
        local getProperty=city.GetProperty
        city.GetProperty=function(self,k)
          if k~=key then return getProperty(self,k) end
          markerReads=markerReads+1
          return values[self:GetID()]
        end
        city.SetProperty=function(self,k,value)
          assert(k==key and self==city2 and values[2]==nil)
          markerWrites=markerWrites+1
          values[2]=value
        end
      end
      local function send(action,id,token)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,CityID=id,Token=token,Page=1})
        assert(s.RequestIngress.action==action and s.RequestDepth==0 and s.FailureAt==nil)
      end
      send('NETWORK_READ',1,'retained-network')
      assert(s.LastToken=='retained-network' and net.TransactionCurrent(0))
      local network=s.Snapshot
      send('CITY_JOURNAL_READ',1,'retained-journal')
      assert(s.LastToken=='retained-journal' and type(s.Snapshot)=='string')
      local journal=s.Snapshot
      local cases={
        {'CAPTURE',1,'capture','saved-marker'},
        {'MARK_CITY',1,'overwrite','saved-marker'},
        {'MARK_CITY',2,'first-mark','first-mark'},
        {'MARK_CITY',2,'duplicate','first-mark'},
        {'MARK_CITY',999,'bad-city'},
      }
      for i,case in ipairs(cases)do
        send(case[1],case[2],case[3])
        if retired then
          assert(s.LastToken=='retained-journal' and s.Snapshot==journal and s.Stage=='ACK CITY_JOURNAL')
        elseif i==#cases then
          assert(s.LastToken==nil and s.Stage=='REJECT_CITY')
        else
          assert(s.LastToken==case[3] and s.Snapshot=='city='..case[2]..' marker='..case[4])
        end
      end
      assert(values[1]=='saved-marker' and values[2]==(not retired and 'first-mark' or nil))
      local beforeSummary=markerReads
      local summary=SPCP0.Summary(0,1)
      assert(summary:find('Marker=saved-marker',1,true) and markerReads==beforeSummary+1)
      markerReads=beforeSummary
      send('NETWORK_READ',1,'after-network')
      assert(s.LastToken=='after-network' and net.TransactionCurrent(0) and s.Snapshot==network)
      retained={network=network,journal=journal,summary=summary}
    """, revision is None)
    version = gp.eval('SPCP0.VERSION')
    reports = {key: value.removeprefix(version+' | ') for key, value in gp.eval('retained').items()}
    assert all(vm.load_counts['missing'] + vm.load_counts['failed'] == 0 for vm in (gp, ui))
    return (packets, reports, scalars(gp.eval('properties')), gp.load_counts, ui.load_counts,
            (gp.eval('markerReads'), gp.eval('markerWrites')))


def panel(root, *, retired):
    doc, ui = panel_runtime(root/'Mod/UI')
    controls = ui.globals().Controls
    buttons = {e.get('ID'): controls[e.get('ID')].hidden for e in doc.iter('GridButton') if e.get('ID')}
    ui.execute("""
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.InheritReadButton.callbacks[Mouse.eLClick]()
      Controls.NetworkButton.callbacks[Mouse.eRClick]()
      Controls.OpenButton.callbacks[Mouse.eRClick]()
      if ... then
        Controls.CaptureButton.callbacks[Mouse.eLClick]()
        Controls.MarkButton.callbacks[Mouse.eLClick]()
      end
    """, not retired)
    return buttons, [dict(packet.items()) for packet in ui.globals().requests.values()]


class CityMarkerRetirement(unittest.TestCase):
    def test_stale_requests_leave_saved_markers_and_current_reports_intact(self):
        with package(B467) as previous:
            before = roots(previous, B467)
        after = roots(ROOT)
        self.assertEqual(before[:-1], after[:-1])
        self.assertEqual((before[-1], after[-1]), ((5, 1), (0, 0)))
        self.assertEqual(len(after[0]), 3)
        measure('city_marker_retirement', dict(
            legacy_marker_reads=[5, 0], legacy_marker_writes=[1, 0],
            existing_marker_preserved=True, matching_route_packets=3,
            current_transaction_gate_and_reports_match=True))

    def test_only_the_two_hidden_marker_controls_retire(self):
        with package(B467) as previous:
            old_buttons, old_requests = panel(previous, retired=False)
        new_buttons, new_requests = panel(ROOT, retired=True)
        for control in CONTROLS:
            self.assertTrue(old_buttons.pop(control))
        self.assertEqual(old_buttons, new_buttons)
        self.assertEqual(old_requests[:-len(CONTROLS)], new_requests)
        self.assertEqual([p['Action'] for p in old_requests[-len(CONTROLS):]], list(CONTROLS.values()))
        self.assertEqual([p['Action'] for p in new_requests],
                         ['PROGRESSION_READ', 'PROGRESSION_STORE_READ', 'NETWORK_DETAIL', 'EVENT_ORDER_TOGGLE'])
