"""Retire three obsolete P0 controls while preserving current Commerce."""
import unittest
from unittest.mock import patch

from refactor_harness import ROOT, measure
from retired_crew_sources import B473, B474, package
from test_o7_legacy_completion_record_retirement import load_cold_store, save_fixture, stored_records
from test_o7_retired_great_work_adjacency_retirement import context
from test_p0_panel_current_layout import panel_runtime
import test_b261_commerce as commerce_fixture

CONTROLS = {
    'CommerceOFFButton': 'COMMERCE_OFF',
    'CommerceAUTOButton': 'COMMERCE_AUTO',
    'CommerceTEST5Button': 'COMMERCE_TEST5',
}


def panel(root, *, retired):
    doc, vm = panel_runtime(root/'Mod/UI')
    controls=vm.globals().Controls
    buttons={e.get('ID'):controls[e.get('ID')].hidden for e in doc.iter('GridButton') if e.get('ID')}
    vm.execute("""
      assert(not Controls.CommerceREADButton.hidden)
      Controls.CommerceREADButton.callbacks[Mouse.eLClick]()
      Controls.GWCityButton.callbacks[Mouse.eLClick]()
      Controls.GWAReadButton.callbacks[Mouse.eRClick]()
      if ... then
        Controls.CommerceOFFButton.callbacks[Mouse.eLClick]()
        Controls.CommerceAUTOButton.callbacks[Mouse.eLClick]()
        Controls.CommerceTEST5Button.callbacks[Mouse.eLClick]()
      end
    """,not retired)
    return buttons,[dict(packet.items()) for packet in vm.globals().requests.values()],dict(vm.globals().eventAdds.items())


def report_and_stale_guard(root,source,saved):
    vm=context(root,source)
    cold=load_cold_store(vm,saved)
    result=vm.execute("""
      local s=ExposedMembers.SPC_P0
      local commerce=s.Commerce
      assert(s.StartStatus.Commerce.state=='OK')
      local original=commerce.Request
      local calls,before=0,#writeKeys
      commerce.Request=function(...)
        calls=calls+1
        return original(...)
      end
      local function request(action,token)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=token,CityID=city1:GetID(),Page=1})
        assert(s.RequestIngress.action==action and s.LastToken==token and s.RequestDepth==0 and s.FailureAt==nil)
        return s.Snapshot
      end
      local first=request('COMMERCE_READ','read-before')
      local receipt=commerce.lastRequest
      assert(first:find('商业化',1,true) and receipt.accepted and receipt.token=='read-before' and calls==1)
      for _,action in ipairs({'COMMERCE_OFF','COMMERCE_AUTO','COMMERCE_TEST5'})do
        assert(request(action,action)=='商业化暂不可用：COM_LEGACY_RETIRED')
        assert(commerce.lastRequest==receipt and calls==1 and #writeKeys==before)
      end
      assert(request('COMMERCE_READ','read-after')==first and commerce.lastRequest.accepted)
      assert(calls==2 and #writeKeys==before and cityWrites==0)
      return first,calls
    """)
    assert stored_records(vm)==cold
    assert vm.load_counts['missing']+vm.load_counts['failed']==0
    return result


def production_dashboard(root):
    with patch.object(commerce_fixture,'ROOT',root):
        vm=commerce_fixture.ui()
        vm.execute("""
          assert(not ContextPtr.hidden and not Controls.Window.hidden and #sent==0)
          assert(Controls.Summary.text:find('SIDEBAR_CAPACITY|2|2',1,true))
          rows.items[1].Root.click()
          assert(Controls.ConfirmCaption.text:find('STOP',1,true))
          Controls.Confirm.click()
          for i=1,20 do Events.GameCoreEventPublishComplete.Fire()end
          assert(#sent==1)
          local p=sent[1]
          assert(p.Action=='COMMERCE_SELECT' and p.Domain=='DISTRICT_CAMPUS' and p.Enabled==false)
          assert(p.Reference=='0:9:10:11' and p.CityToken=='city-token' and p.Revision==7 and p.CityID==9)
        """)
        return dict(vm.eval('sent[1]').items())


class RetiredCommerceControls(unittest.TestCase):
    def test_only_three_hidden_buttons_leave_and_current_callbacks_match(self):
        with package(B473) as previous, package(B474) as retired:
            old_buttons,old_packets,old_listeners=panel(previous,retired=False)
            new_buttons,new_packets,new_listeners=panel(retired,retired=True)
        current_buttons,current_packets,current_listeners=panel(ROOT,retired=True)
        self.assertTrue(CONTROLS.keys().isdisjoint(current_buttons))
        self.assertEqual((current_packets,current_listeners),(new_packets,new_listeners))
        for control in CONTROLS:
            self.assertTrue(old_buttons.pop(control))
        self.assertEqual(old_buttons,new_buttons)
        self.assertEqual(old_listeners,new_listeners)
        self.assertEqual(old_packets[:-3],new_packets)
        self.assertEqual([p['Action'] for p in old_packets[-3:]],list(CONTROLS.values()))
        self.assertEqual([p['Action'] for p in new_packets],['COMMERCE_READ','DIALOGUE_PROJECT_READ','MEMORY_READ'])
        measure('retired_commerce_controls',dict(old_button_packets=[3,0],remaining_packets='MATCH',listeners='MATCH'))

    def test_real_report_and_stale_ingress_guard_stay_read_only(self):
        saved=save_fixture()
        with package(B473) as previous:
            before=report_and_stale_guard(previous,B473,saved)
            for name in ('Gameplay.lua','Commerce.lua','CommerceModel.lua','UI/CommerceUI.lua',
                         'UI/CommercePanel.lua','UI/CommercePanel.xml','CityProgressionStore.lua'):
                self.assertEqual((ROOT/'Mod'/name).read_bytes(),(previous/'Mod'/name).read_bytes())
        after=report_and_stale_guard(ROOT,None,saved)
        self.assertEqual(before,after)
        measure('retired_commerce_guard',dict(stale_requests_blocked=3,property_writes=[0,0],report='MATCH'))

    def test_real_configuration_panel_sends_the_same_scoped_selection(self):
        with package(B473) as previous:
            before=production_dashboard(previous)
        after=production_dashboard(ROOT)
        self.assertEqual(before,after)
        measure('retired_commerce_dashboard',dict(selection_packets_per_click=1,scoped_packet='MATCH'))
