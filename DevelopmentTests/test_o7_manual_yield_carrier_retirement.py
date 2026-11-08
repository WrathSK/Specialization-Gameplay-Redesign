"""Retire the hidden B029 tool while retaining its separate city-exit cleanup."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B457, B458, gameplay, package
from test_o7_crew_retirement import verify_package_round_trip
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime
from test_refactor_s8c5c import production as cleanup_production

REMOVED = 'YieldCarrierProbe.lua'


def request_scenario(game, retired):
    game.execute('''
      local retired=...
      local s=ExposedMembers.SPC_P0
      assert(s.StartStatus.LegacyCleanup.state=='OK')
      local city=city1
      local values={}
      local writes=0
      local plot={GetOwner=function()return 0 end,
        GetProperty=function(_,k)return values[k] end,
        SetProperty=function(_,k,v)writes=writes+1;values[k]=v end}
      Map={GetPlot=function(x,y)assert(x==city:GetX() and y==city:GetY());return plot end}
      GameInfo.Modifiers=setmetatable({},{__index=function()return {} end})
      YieldTypes={SCIENCE=0,CULTURE=1,PRODUCTION=2}
      city.GetYield=function(_,kind)return 10+kind end
      -- Provide accepted ledger facts while exercising the actual report and dispatch.
      s.CityProgressionStore.FailureReport=function()return nil end
      s.CityProgressionStore.Owns=function(c)assert(c==city);return true end
      s.EffectiveFacts.Read=function(pid,c)
        assert(pid==0 and c==city)
        return {cityID=c:GetID(),specialization='RESEARCH',potential=4,active=3,
          activeStatus='VERIFIED',investmentCount=3,investmentPending=false,ledgerStatus='VALID'}
      end
      local function request(action)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=action,CityID=city:GetID()})
        assert(s.RequestIngress.action==action)
      end
      request('PROGRESSION_READ')
      progressReport=s.Snapshot
      assert(s.LastToken=='PROGRESSION_READ' and progressReport:find('Potential=4 | ACTIVE=3',1,true))
      request('CARRIER_STEP')
      if not retired then assert(writes==2 and s.LastToken=='CARRIER_STEP' and values.SPC_B029_ONE==1) end
      request('SOURCE_YIELDS')
      if not retired then assert(writes==2 and s.LastToken=='SOURCE_YIELDS' and s.Snapshot:find('configured=1',1,true)) end
      request('CARRIER_OFF')
      if retired then
        assert(writes==0 and s.LastToken=='PROGRESSION_READ' and s.Snapshot==progressReport and next(values)==nil)
      else
        assert(writes==4 and s.LastToken=='CARRIER_OFF' and values.SPC_B029_ONE==0 and values.SPC_B029_HALF==0)
      end
      manualWrites=writes
    ''', retired)
    return game.globals().progressReport, game.globals().manualWrites


def panel_controls(root):
    doc, ui = panel_runtime(root/'Mod/UI')
    controls = ui.globals().Controls
    buttons = {n.get('ID'): controls[n.get('ID')].hidden for n in doc.iter('GridButton') if n.get('ID')}
    ui.execute('''
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.CarrierStepButton.callbacks[Mouse.eLClick]()
      assert(#requests==2 and requests[1].Action=='PROGRESSION_READ' and requests[2].Action=='NETWORK_DETAIL')
    ''')
    return buttons, [dict(packet.items()) for packet in ui.globals().requests.values()]


class ManualYieldCarrierRetirement(unittest.TestCase):
    def test_legacy_commands_retire_while_route_and_progression_reports_match(self):
        with package(B457) as previous:
            old_game = gameplay(previous, revision=B457)
            old_ui = gameplay(previous, revision=B457, name='UI/BackgroundRoutes')
            vfs = PackageVFS(forbidden_globals=('SPCYieldCarrierProbe',))
            self.assertNotIn(REMOVED, vfs.files | vfs.imports)
            game = Context(vfs=vfs)
            ui = Context(name='UI/BackgroundRoutes', vfs=vfs)
            packets = exercise_proof(old_game, old_ui)
            self.assertEqual(exercise_proof(game, ui), packets)
            self.assertEqual(len(packets), 3)
            old_report, old_writes = request_scenario(old_game, False)
            new_report, new_writes = request_scenario(game, True)
            self.assertEqual(new_report, old_report)
            self.assertEqual((old_writes,new_writes), (4,0))
        for context in (old_game,old_ui,game,ui):
            self.assertEqual(context.load_counts['failed'] + context.load_counts['missing'], 0)
        measure('manual_yield_carrier_retirement', {'old_manual_plot_writes':old_writes,
            'current_manual_plot_writes':new_writes,'matching_route_packets':len(packets)})

    def test_only_hidden_control_retires_and_exit_clears_exact_flags(self):
        with package(B457) as previous:
            old_buttons, old_requests = panel_controls(previous)
            new_buttons, new_requests = panel_controls(ROOT)
            self.assertTrue(old_buttons.pop('CarrierOffButton'))
            self.assertEqual(new_buttons, old_buttons)
            self.assertEqual(new_requests, old_requests)
            for path in ('LegacyCleanup.lua','LegacyCleanupCatalog.lua','Data/YieldCarrierProbe.sql'):
                self.assertEqual((ROOT/'Mod'/path).read_bytes(), (previous/'Mod'/path).read_bytes())
        game = cleanup_production()
        game.execute('''
          assert(SPCYieldCarrierProbe==nil and shared.StartStatus.LegacyCleanup.state=='OK')
          assert(plotWrites==0 and ca.plotValues.SPC_B029_ONE==1 and ca.plotValues.SPC_B029_HALF==1)
          lose()
          assert(status()=='WITHDRAWN' and plotWrites==2 and removeCalls==1409)
          assert(ca.plotValues.SPC_B029_ONE==0 and ca.plotValues.SPC_B029_HALF==0)
          assert(cb.plotValues.SPC_B029_ONE==1 and cb.plotValues.SPC_B029_HALF==1)
          assert(ca.plotValues.OTHER=='keep' and cb.plotValues.OTHER=='keep')
          assert(ca.present[999999] and cb.present[999999])
        ''')
        measure('manual_yield_carrier_exit', {'plot_writes':2,'other_city_and_flags_preserved':True})

    def test_exact_temporary_switch_and_recovery(self):
        with package(B457) as previous, package(B458) as retired:
            verify_package_round_trip(self, previous/'Mod', retired/'Mod', (REMOVED,), 'LegacyCleanup.lua')
