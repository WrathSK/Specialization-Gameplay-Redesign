"""Remove the unreferenced city totals reader while retaining live report paths."""
import unittest

from refactor_harness import Context, measure
from retired_crew_sources import B456, B457, gameplay, package, source
from test_o7_crew_retirement import verify_package_round_trip
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime

REMOVED = 'SourceYieldProbe.lua'


def reports(game):
    game.execute('''
      local s=ExposedMembers.SPC_P0
      local facts=s.EffectiveFacts
      local city=city1
      -- The report scenario models an accepted ledger at the fact boundary.
      s.CityProgressionStore.FailureReport=function()return nil end
      s.CityProgressionStore.Owns=function(c)assert(c==city);return true end
      facts.Read=function(pid,c)
        assert(pid==0 and c==city)
        return {cityID=c:GetID(),specialization='RESEARCH',potential=4,active=3,
          activeStatus='VERIFIED',investmentCount=3,investmentPending=false,ledgerStatus='VALID'}
      end
      local values={SPC_B029_ONE=1,SPC_B029_HALF=1}
      local writes={}
      local plot={GetOwner=function()return 0 end,
        GetProperty=function(_,k)return values[k] end,
        SetProperty=function(_,k,v)writes[#writes+1]=k;values[k]=v end}
      Map={GetPlot=function(x,y)assert(x==city:GetX() and y==city:GetY());return plot end}
      YieldTypes={SCIENCE=0,CULTURE=1,PRODUCTION=2}
      city.GetYield=function(_,kind)return 10+kind end
      local function report(action)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=action,CityID=city:GetID()})
        assert(s.LastToken==action and type(s.Snapshot)=='string')
        return s.Snapshot
      end
      progressReport=report('PROGRESSION_READ')
      assert(progressReport:find('RESEARCH') and progressReport:find('Potential=4 | ACTIVE=3',1,true))
      carrierReport=report('SOURCE_YIELDS')
      assert(carrierReport:find('configured=2.5',1,true) and #writes==0)
      carrierOff=report('CARRIER_OFF')
      assert(carrierOff:find('configured=0',1,true))
      assert(#writes==2 and writes[1]=='SPC_B029_ONE' and writes[2]=='SPC_B029_HALF')
    ''')
    return tuple(game.globals()[name] for name in ('progressReport','carrierReport','carrierOff'))


def progression_button(root):
    _, ui = panel_runtime(root/'Mod/UI')
    ui.execute('''
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      assert(#requests==1 and requests[1].Action=='PROGRESSION_READ')
    ''')
    return dict(ui.globals().requests[1].items()), ui.globals().Controls.SourceYieldButtonCaption.text


class SourceYieldPrototypeRetirement(unittest.TestCase):
    def test_real_package_keeps_city_report_carrier_reset_and_nonempty_route_proof(self):
        with package(B456) as previous, package(B457) as retired:
            old_game = gameplay(previous, revision=B456)
            old_ui = gameplay(previous, revision=B456, name='UI/BackgroundRoutes')
            game = gameplay(retired, revision=B457, forbidden_globals=('SPCSourceYieldProbe',))
            ui = gameplay(retired, revision=B457, name='UI/BackgroundRoutes',
                          forbidden_globals=('SPCSourceYieldProbe',))
            self.assertNotIn(REMOVED, game.vfs.files | game.vfs.imports)
            old_packets = exercise_proof(old_game, old_ui)
            new_packets = exercise_proof(game, ui)
            self.assertEqual(len(old_packets), 3)
            self.assertEqual(new_packets, old_packets)
            self.assertEqual(reports(game), reports(old_game))
            self.assertEqual(progression_button(retired), progression_button(previous))
        self.assertEqual(game.load_counts, {**old_game.load_counts,
            'attempts':old_game.load_counts['attempts']-1, 'completed':old_game.load_counts['completed']-1})
        self.assertEqual(ui.load_counts, old_ui.load_counts)
        for context in (old_game,old_ui,game,ui):
            self.assertEqual(context.load_counts['missing'] + context.load_counts['failed'], 0)
        measure('source_yield_retirement', {'removed_modeled_gameplay_loads':1,'matching_route_packets':3,
            'city_report_matches':True,'legacy_carrier_report_and_reset_match':True})

    def test_frozen_probe_still_replays_total_yield_and_ownership_cases(self):
        game = Context()
        game.execute(source(REMOVED, B456))
        game.execute('''
          YieldTypes={SCIENCE=0,CULTURE=1,PRODUCTION=2}
          local values={[0]=7.512345,[1]=1.25,[2]=11}
          local c={GetOwner=function()return 0 end,GetID=function()return 42 end,
            GetName=function()return 'City' end,GetYield=function(_,i)return values[i] end}
          shared.CityFlowProbe={SupportFacts=function()return {specialization='RESEARCH'} end}
          local function read()return SPCSourceYieldProbe.Read(0,c,shared)end
          local first=read()
          assert(first:find('SCIENCE total=7.512345',1,true)
            and first:find('CULTURE total=1.250000',1,true) and first:find('PRODUCTION total=11.000000',1,true))
          assert(read()==first)
          values[0]=8.5;values[1]=0/0
          assert(read():find('CULTURE UNKNOWN',1,true) and read():find('SCIENCE total=8.500000',1,true))
          assert(SPCSourceYieldProbe.Read(1,c,shared):find('OWNER_CHANGED',1,true))
          YieldTypes=nil
          GameInfo={Yields={YIELD_SCIENCE={Index=0},YIELD_CULTURE={Index=1},YIELD_PRODUCTION={Index=2}}}
          assert(read():find('SCIENCE total=8.500000',1,true))
        ''')

    def test_exact_temporary_switch_and_recovery(self):
        with package(B456) as previous, package(B457) as retired:
            verify_package_round_trip(self, previous/'Mod', retired/'Mod', (REMOVED,), 'YieldCarrierProbe.lua')
