"""Remove the retired B050 shell while keeping the current cleanup owner."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B459, gameplay, package
from test_o7_crew_retirement import verify_package_round_trip
from test_o7_manual_yield_carrier_retirement import panel_controls
from test_o7_route_observer_retirement import exercise_proof
from test_refactor_s8c5c import production
from test_refactor_s9e4 import half_production

REMOVED = 'HalfYieldProbe.lua'
CONTROLS = ('HalfReadButton', 'HalfOnButton', 'HalfOffButton')
RETAINED = ('Data/HalfYieldProbe.sql','LegacyCleanup.lua','LegacyCleanupCatalog.lua','CityProgressionStore.lua',
            'ResearchCross.lua','ResearchInfrastructure.lua','CopyYields.lua','DistrictPrecisionProbe.lua')


def request_scenario(game, removed):
    game.execute("""
      local removed=...
      local s=ExposedMembers.SPC_P0
      assert(s.StartStatus.LegacyCleanup.state=='OK')
      if removed then
        assert(s.StartStatus.HalfYieldProbe==nil and s.HalfYieldProbe==nil and SPCHalfYieldProbe==nil)
      else
        assert(s.StartStatus.HalfYieldProbe.state=='OK' and s.HalfYieldProbe.retired)
      end
      local city=city1
      local cityAccess=0
      local function forbid()
        cityAccess=cityAccess+1;error('RETIRED_REQUEST_ACCESSED_NATIVE_CITY_STATE')
      end
      city.GetProperty=forbid
      city.GetPopulation=forbid
      city.GetYield=forbid
      city.GetBuildings=forbid
      city.GetBuildQueue=forbid
      city.SetProperty=forbid
      -- Feed a valid ledger view through the actual request and report handlers.
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
      halfAcknowledgments=0
      for _,action in ipairs({'HALF_READ','HALF_ON','HALF_OFF'})do
        request(action)
        if removed then
          assert(s.LastToken=='PROGRESSION_READ' and s.Snapshot==progressReport)
        else
          assert(s.LastToken==action and s.Snapshot:find('旧半点实验已退役',1,true))
          halfAcknowledgments=halfAcknowledgments+1
        end
      end
      assert(cityAccess==0)
    """,removed)
    return game.globals().progressReport, game.globals().halfAcknowledgments


class HalfYieldExperimentRetirement(unittest.TestCase):
    def test_real_roots_keep_route_packets_and_only_drop_retired_acknowledgments(self):
        profile = PackageVFS(forbidden_globals=('SPCHalfYieldProbe',))
        self.assertNotIn(REMOVED, profile.files | profile.imports)
        current_game = Context(vfs=profile)
        current_ui = Context(name='UI/BackgroundRoutes',vfs=profile)
        with package(B459) as previous:
            old_game = gameplay(previous,revision=B459)
            old_ui = gameplay(previous,revision=B459,name='UI/BackgroundRoutes')
            packets = exercise_proof(old_game,old_ui)
            self.assertEqual(exercise_proof(current_game,current_ui),packets)
            self.assertEqual(len(packets),3)
            before, old_acks = request_scenario(old_game,False)
            after, new_acks = request_scenario(current_game,True)
            self.assertEqual(before,after)
            self.assertEqual((old_acks,new_acks),(3,0))
        for context in (old_game,old_ui,current_game,current_ui):
            self.assertEqual(context.load_counts['missing']+context.load_counts['failed'],0)
        self.assertEqual(current_ui.load_counts,old_ui.load_counts)
        self.assertEqual(current_game.load_counts,{**old_game.load_counts,
            'attempts':old_game.load_counts['attempts']-1,'completed':old_game.load_counts['completed']-1})
        measure('half_yield_experiment_retirement',{'modeled_acknowledgments':[old_acks,new_acks],
            'matching_route_packets':len(packets),'request_city_accesses':0})

    def test_only_three_hidden_controls_leave_the_panel(self):
        with package(B459) as previous:
            old_buttons, old_requests = panel_controls(previous)
            new_buttons, new_requests = panel_controls(ROOT)
            for button in CONTROLS:
                self.assertTrue(old_buttons.pop(button))
            self.assertEqual(new_buttons,old_buttons)
            self.assertEqual(new_requests,old_requests)

    def test_exact_exit_and_Store_retry_preserve_flags_and_the_other_city(self):
        with package(B459) as previous:
            for path in RETAINED:
                self.assertEqual((ROOT/'Mod'/path).read_bytes(),(previous/'Mod'/path).read_bytes())
        for context, removed in ((half_production(),False),(production(),True)):
            context.execute("""
              local removed=...
              assert((shared.HalfYieldProbe==nil)==removed)
              assert(shared.StartStatus.LegacyCleanup.state=='OK' and plotWrites==0)
              local names=byGroup.HalfYieldProbe.names
              assert(#names==32)
              ca.s.values.SPC_B050_HALF_ENABLED=true
              cb.s.values.SPC_B050_HALF_ENABLED=true
              faultGroup='HalfYieldProbe';lose()
              assert(status()=='PARTIAL_HELD' and removeCalls==1377 and plotWrites==2)
              for _,name in ipairs(names)do
                local id=definitions[name].Index
                assert(ca.present[id] and cb.present[id])
              end
              faultGroup=nil;s.ExitConfirmed()
              assert(status()=='WITHDRAWN' and removeCalls==1409 and removeByGroup.HalfYieldProbe==32)
              s.ExitConfirmed();assert(removeCalls==1409 and plotWrites==2)
              for _,name in ipairs(names)do
                local id=definitions[name].Index
                assert(not ca.present[id] and cb.present[id])
              end
              assert(ca.s.values.SPC_B050_HALF_ENABLED==true and cb.s.values.SPC_B050_HALF_ENABLED==true)
              assert(ca.plotValues.OTHER=='keep' and cb.plotValues.OTHER=='keep')
              assert(ca.present[999999] and cb.present[999999])
            """,removed)
        measure('half_yield_exit',{'target_B050_carriers':32,'unrelated_city_and_flags_preserved':True,
            'existing_Store_retry':'CONFIRMED_IN_FIXTURE'})

    def test_exact_temporary_switch_and_recovery(self):
        with package(B459) as previous:
            verify_package_round_trip(self,previous/'Mod',ROOT/'Mod',(REMOVED,),'LegacyCleanup.lua')
