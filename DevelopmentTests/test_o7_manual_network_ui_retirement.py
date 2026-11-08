"""The hidden manual readers leave the package, with the formal P0 pager intact."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B466, package
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime

CONTROLS = ('AdjacencyButton', 'TradeButton', 'NextButton')


def panel(root, *, retired):
    doc, ui = panel_runtime(root/'Mod/UI')
    controls = ui.globals().Controls
    hidden = {e.get('ID'): controls[e.get('ID')].hidden for e in doc.iter('GridButton') if e.get('ID')}
    ui.execute("""
        local retired=...
        if not retired then
          local calls={}
          SPCP0.NetworkProbe=function(city,action,stage,page)
            assert(city==selectedCity)
            calls[#calls+1]=action..':'..page
            return 'OLD_LOCAL_REPORT'
          end
          Controls.AdjacencyButton.callbacks[Mouse.eLClick]()
          Controls.NextButton.callbacks[Mouse.eLClick]()
          Controls.TradeButton.callbacks[Mouse.eLClick]()
          Controls.NextButton.callbacks[Mouse.eLClick]()
          assert(table.concat(calls,',')=='ADJACENCY:1,ADJACENCY:2,TRADE:1,TRADE:2')
          assert(#requests==0 and Controls.Status.text:find('OLD_LOCAL_REPORT',1,true))
        end
        ExposedMembers.SPC_P0_BackgroundRoutes={version=SPCP0.VERSION,text='BACKGROUND_ROUTE_REPORT'}
        Controls.BackgroundRoutesButton.callbacks[Mouse.eLClick]()
        assert(#requests==0 and Controls.Status.text:find('BACKGROUND_ROUTE_REPORT',1,true))
        Controls.NetworkButton.callbacks[Mouse.eLClick]()
        Controls.NetworkButton.callbacks[Mouse.eRClick]()
        Controls.CarrierStepButton.callbacks[Mouse.eLClick]()
        Controls.CarrierStepButton.callbacks[Mouse.eLClick]()
        Controls.CityJournalButton.callbacks[Mouse.eLClick]()
        Controls.OpenButton.callbacks[Mouse.eRClick]()
    """, retired)
    return hidden, [dict(p.items()) for p in ui.globals().requests.values()]


def proof(root, revision=None):
    vfs = PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo')
    history = (root,revision) if revision else None
    gp,ui = (Context(name=name,vfs=vfs,history=history) for name in ('Gameplay','UI/BackgroundRoutes'))
    packets = exercise_proof(gp,ui)
    for vm in (gp,ui):
        assert vm.eval('type(SPCP0.NetworkProbe)') == ('function' if revision else 'nil')
        assert vm.load_counts['missing'] + vm.load_counts['failed'] == 0
    return packets,gp.load_counts,ui.load_counts


class ManualNetworkUIRetirement(unittest.TestCase):
    def test_formal_network_detail_pagination_and_other_commands_match(self):
        with package(B466) as previous:
            old_buttons,old_requests = panel(previous,retired=False)
        new_buttons,new_requests = panel(ROOT,retired=True)
        for control in CONTROLS:
            self.assertTrue(old_buttons.pop(control))
        self.assertEqual(old_buttons,new_buttons)
        self.assertEqual(old_requests,new_requests)
        self.assertEqual([p['Action'] for p in new_requests],
            ['NETWORK_READ','NETWORK_DETAIL','NETWORK_DETAIL','NETWORK_DETAIL','CITY_JOURNAL_READ','EVENT_ORDER_TOGGLE'])
        self.assertEqual([p['Page'] for p in new_requests[1:4]],[1,2,3])
        measure('manual_network_ui_paging',dict(retired_hidden_controls=list(CONTROLS),
            retained_network_detail_pages=[1,2,3],background_report_matches=True))

    def test_route_transport_and_shared_adjacency_owners_remain(self):
        with package(B466) as previous:
            old = proof(previous,B466)
            for path in ('Gameplay.lua','SampleLifecycle.lua','UI/IndustryRefresh.lua','UI/ResearchCrossRefresh.lua',
                         'UI/BackgroundRoutes.lua','NetworkSender.lua','NetworkBridge.lua','NetworkInput.lua'):
                self.assertEqual((previous/'Mod'/path).read_bytes(),(ROOT/'Mod'/path).read_bytes())
        new = proof(ROOT)
        self.assertEqual(old,new)
        self.assertEqual(len(new[0]),3)
        measure('manual_network_ui_route_proof',dict(matching_production_packets=3))
