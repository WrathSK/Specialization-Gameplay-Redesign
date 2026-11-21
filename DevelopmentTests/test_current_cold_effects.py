"""Same-build reload observations. Only engine-owned fixture values cross the VM boundary."""
import unittest
from contextlib import contextmanager

from refactor_harness import measure
from test_b244_capital_storage import lua_value, plain
import test_refactor_s5d3 as dialogue
import test_refactor_s5d4c5 as collection
import test_refactor_s5d4c6 as insights
import test_refactor_s6f as investment


@contextmanager
def projections(case):
    """Reuse the SQL catalogue and native surface for each pair of independent VMs."""
    import test_culture_aesthetic as native
    previous_runtime = native.LuaRuntime
    case.setUpClass()
    try:
        yield case()
    finally:
        case.tearDownClass()
        native.LuaRuntime = previous_runtime


def restore_native_city_effects(before, after):
    # Copy installed buildings, their locations/health and native plot properties.
    # The receiver retains its own cities, new Lua modules and empty session caches.
    for name in ('a', 'b'):
        src, dst = before.globals()[name], after.globals()[name]
        for field in ('present', 'locations', 'pillaged'):
            dst[field] = lua_value(after, plain(src[field]))
    for index, plot in before.globals().plots.items():
        after.globals().plots[index].props = lua_value(after, plain(plot.props))


class ColdEffects(unittest.TestCase):
    def record(self, owner, saved, loaded, idle, recovered, **observations):
        measure('cold_effect_' + owner, {
            'saved': saved, 'loaded': loaded, 'idle': idle, 'after_evidence': recovered,
            'continuous_at_observed_boundaries': loaded == saved and idle == saved,
            **observations,
        })
        self.assertTrue(saved, owner)
        self.assertEqual(recovered, saved, owner)

    def test_late_collection_sample_reconciles_three_city_effects(self):
        def applied(vm, city):
            read = vm.eval('function(c) return total(c), finalAmount(c,"SCIENCE"), inspiration(c) end')
            tourism, science, gpp, carrier_count = read(vm.globals()[city])
            self.assertLessEqual(carrier_count, 1)
            return tourism, science, gpp

        with projections(collection.CultureProjection) as case:
            warm = case.fixture(real=True, ready=False)
            warm.execute("fire('LoadScreenClose'); sample(1,1,1); pp()")
            before = applied(warm, 'a')
            cold = case.fixture(real=True, ready=False)
            restore_native_city_effects(warm, cold)
            self.assertEqual(applied(cold, 'a'), before)
            cold.execute("fire('LoadScreenClose')")
            loaded = applied(cold, 'a')
            cold.execute("for n=1,3 do pp() end")
            idle = applied(cold, 'a')
            cold.execute("sample(1,1,1); pp()")
            recovered = applied(cold, 'a')
            for i, owner in enumerate(('aesthetic', 'meaning_science', 'inspiration')):
                self.record(owner, before[i], loaded[i], idle[i], recovered[i])
            self.assertEqual(applied(cold, 'b'), applied(warm, 'b'))
            writes = cold.eval('writes')
            cold.execute("sample(1,1,1); pp()")
            self.assertEqual(cold.eval('writes'), writes)
            cold.execute("sample(2,0,1); pp()")
            self.assertEqual(applied(cold, 'a'), (0, 0, 0))
            self.assertEqual(applied(cold, 'b'), applied(warm, 'b'))

    def test_dialogue_history_delivery_restores_earned_percent(self):
        with projections(dialogue.Dialogue) as case:
            warm = case.fixture()
            before = warm.eval('total(a)')
            cold = case.fixture(boot=False)
            restore_native_city_effects(warm, cold)
            self.assertEqual(cold.eval('total(a)'), before)
            cold.execute("""
                a.historyError = true
                SPCDialogueEffects.Start(P,shared)
                fire('LoadScreenClose')
            """)
            loaded = cold.eval('total(a)')
            self.assertEqual(cold.eval('total(b)'), warm.eval('total(b)'))
            cold.execute("for n=1,3 do publish() end")
            idle = cold.eval('total(a)')
            cold.execute("""
                a.historyError = false
                function historyChanged()
                    shared.FactChanges.Emit{owner=0, cityID=a.id, kinds={'HISTORY'}, topic='DIALOGUE', cause='DEFERRED_LIFECYCLE_RECOVERED'}
                    publish()
                end
                historyChanged()
            """)
            self.record('dialogue', before, loaded, idle, cold.eval('total(a)'))
            writes = cold.eval('writes')
            cold.execute('historyChanged()')
            self.assertEqual(cold.eval('writes'), writes)
            self.assertEqual(cold.eval('a.history.total'), before)

    def test_insight_ledger_becomes_readable_before_local_turn(self):
        warm = insights.fixture()
        cold = insights.fixture(boot=False)
        for name in ('a', 'b'):
            cold.globals()[name].present[1] = warm.globals()[name].present[1]

        def percent():
            return cold.eval('a.present[1] and 2 or 0')

        saved = percent()
        history = cold.eval('history()')
        cold.execute("""
            local read = shared.CityProgressionStore.ExpeditionInsights
            delay = true
            shared.CityProgressionStore.ExpeditionInsights = function(pid,c)
                if delay and c==a then error('TEST_LEDGER_UNAVAILABLE') end
                return read(pid,c)
            end
            Events.LoadScreenClose()
            assert(b.present[1])
        """)
        loaded = percent()
        cold.execute("for n=1,3 do pp() end")
        idle = percent()
        cold.execute("delay=false; Events.PlayerTurnActivated(0)")
        self.record('insights_tourism', saved, loaded, idle, percent())
        writes = cold.eval('creates + removes')
        cold.execute("Events.PlayerTurnActivated(0)")
        self.assertEqual(cold.eval('creates + removes'), writes)
        self.assertEqual(cold.eval('history()'), history)

    def test_development_reindexes_an_existing_paid_contract(self):
        warm = investment.development()
        warm.execute("assert(open()); assert(sign()); assert(active() and moneyCalls==1)")
        receipt = plain(warm.eval('value()'))
        cold = investment.development()
        for key, value in plain(warm.eval('T.props()')).items():
            cold.globals().T.propsSet(key, lua_value(cold, value))
        cold.globals().balance = warm.eval('balance')
        cold.globals().research.markers['BUILDING_SPC_DEVELOPMENT_DISTRICT_CAMPUS'] = warm.eval('active()')
        saved = cold.eval('active()')
        cold.execute("""
            local dc=shared.DistrictCompleteness
            T.reload(); C.service(); shared.DistrictCompleteness=dc
            SPCFactChanges.New(shared)
            local store=shared.CityProgressionStore
            local visit=store.VisitDevelopment
            local readiness=store.HistoryStartStatus
            waitForHistory=true; delayIndex=true
            store.HistoryStartStatus=function()
                if waitForHistory then return 'WAITING' end
                if readiness then return readiness() end
            end
            store.VisitDevelopment=function(...)
                if delayIndex then error('TEST_INDEX_UNAVAILABLE') end
                return visit(...)
            end
            setupDevelopment()
            duringHistoryWait=active()
            assert(duringHistoryWait)
            waitForHistory=false
            Events.GameCoreEventPublishComplete.Fire()
        """)
        loaded = cold.eval('active()')
        cold.execute("for n=1,3 do Events.GameCoreEventPublishComplete.Fire() end")
        idle = cold.eval('active()')
        cold.execute("""
            delayIndex=false
            Events.GameCoreEventPublishComplete.Fire()
            afterSilentReturn=active()
            Events.PlayerTurnActivated.Fire(0)
            afterTurn=active()
            function historyRecovered()
                shared.FactChanges.Emit{owner=0, cityID=source:GetID(), kinds={'HISTORY'}, topic='DEVELOPMENT_RECOVERY', cause='DEFERRED_LIFECYCLE_RECOVERED'}
                shared.FactChanges.Flush()
                Events.GameCoreEventPublishComplete.Fire()
            end
            historyRecovered()
        """)
        self.record('development', saved, loaded, idle, cold.eval('active()'),
                    waiting_for_store=cold.eval('duringHistoryWait'), readable_without_notice=cold.eval('afterSilentReturn'),
                    local_turn_without_other_changes=cold.eval('afterTurn'))
        writes = cold.eval('effectWrites')
        cold.execute('historyRecovered()')
        self.assertEqual(cold.eval('effectWrites'), writes)
        self.assertEqual(plain(cold.eval('value()')), receipt)
        self.assertEqual(cold.eval('moneyCalls'), 0)
        self.assertEqual(cold.eval('balance'), warm.eval('balance'))
