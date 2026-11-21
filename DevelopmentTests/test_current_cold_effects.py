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
        self.assertEqual(loaded, saved, owner)
        self.assertEqual(idle, saved, owner)
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
            cold.execute("""
                plotWrites=0
                local set=P.SetProperty
                P.SetProperty=function(plot,key,value)
                    if key:find(SPCCultureAesthetic.Key,1,true)==1 then plotWrites=plotWrites+1 end
                    return set(plot,key,value)
                end
                function projectionWrites()
                    return plotWrites+shared.CultureAesthetic.changes+shared.CultureMeaning.changes+shared.CultureInspiration.changes
                end
            """)
            writes = cold.eval('projectionWrites()')
            cold.execute("fire('LoadScreenClose')")
            loaded = applied(cold, 'a')
            cold.execute("for n=1,3 do pp() end")
            idle = applied(cold, 'a')
            cold.execute("sample(1,1,1); pp()")
            recovered = applied(cold, 'a')
            self.assertEqual(cold.eval('projectionWrites()'), writes)
            for i, owner in enumerate(('aesthetic', 'meaning_science', 'inspiration')):
                self.record(owner, before[i], loaded[i], idle[i], recovered[i])
            self.assertEqual(applied(cold, 'b'), applied(warm, 'b'))
            writes = cold.eval('writes')
            cold.execute("sample(1,1,1); pp()")
            self.assertEqual(cold.eval('writes'), writes)
            cold.execute("sample(2,0,1); pp()")
            self.assertEqual(applied(cold, 'a'), (0, 0, 0))
            self.assertEqual(applied(cold, 'b'), applied(warm, 'b'))

    def test_confirmed_city_change_precedes_a_delayed_work_packet(self):
        with projections(collection.CultureProjection) as case:
            warm = case.fixture(real=True, ready=False)
            warm.execute("fire('LoadScreenClose'); sample(1,1,1); pp()")
            for change in ("a.active=2", "a.token='REPLACED'"):
                with self.subTest(change=change):
                    cold = case.fixture(real=True, ready=False)
                    restore_native_city_effects(warm, cold)
                    cold.execute("fire('LoadScreenClose'); assert(total(a)>0 and finalAmount(a,'SCIENCE')>0 and inspiration(a)>0)")
                    cold.execute(change)
                    cold.execute("""
                        local scope={player=0,city=1}
                        shared.CultureAesthetic.Audit(scope)
                        shared.CultureMeaning.Audit(scope)
                        shared.CultureInspiration.Audit(scope)
                        assert(total(a)==0 and finalAmount(a,'SCIENCE')==0 and inspiration(a)==0)
                        assert(total(b)>0 and finalAmount(b,'SCIENCE')>0 and inspiration(b)>0)
                    """)

    def test_dialogue_history_delivery_restores_earned_percent(self):
        with projections(dialogue.Dialogue) as case:
            warm = case.fixture()
            before = warm.eval('total(a)')
            cold = case.fixture(boot=False)
            restore_native_city_effects(warm, cold)
            self.assertEqual(cold.eval('total(a)'), before)
            cold.execute("""
                a.historyError = true
                dialogueWrites=0
                local create,remove=P.CreateBuilding,P.RemoveBuilding
                local function observe(c,id)
                    if c==a and GameInfo.Buildings[id].BuildingType:find('^BUILDING_SPC_DIALOGUE_TOTAL_')then
                        dialogueWrites=dialogueWrites+1
                    end
                end
                P.CreateBuilding=function(q,id)observe(q.city,id);return create(q,id)end
                P.RemoveBuilding=function(b,id)observe(b.city,id);return remove(b,id)end
                SPCDialogueEffects.Start(P,shared)
                fire('LoadScreenClose')
                assert(shared.DialogueEffects.records['0:1'].applied==nil)
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
            self.assertEqual(cold.eval('dialogueWrites'), 0)
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
        initial_writes = cold.eval('creates + removes')
        cold.execute("""
            local read = shared.CityProgressionStore.ExpeditionInsights
            delay = true
            shared.CityProgressionStore.ExpeditionInsights = function(pid,c)
                if delay and c==a then error('TEST_LEDGER_UNAVAILABLE') end
                return read(pid,c)
            end
            Events.LoadScreenClose()
            assert(b.present[1] and d.records['0:1'].n==nil)
        """)
        loaded = percent()
        cold.execute("for n=1,3 do pp() end")
        idle = percent()
        cold.execute("delay=false; Events.PlayerTurnActivated(0)")
        self.record('insights_tourism', saved, loaded, idle, percent())
        self.assertEqual(cold.eval('creates + removes'), initial_writes)
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
            partialRows=0; paidTargetWrites=0
            local effect='BUILDING_SPC_DEVELOPMENT_DISTRICT_CAMPUS'
            other.markers[effect]=true
            local create,remove=P.CreateBuilding,P.RemoveBuilding
            local function observe(bs,id)
                if bs==research.markers and id==effect then paidTargetWrites=paidTargetWrites+1 end
            end
            P.CreateBuilding=function(bs,id)observe(bs,id);return create(bs,id)end
            P.RemoveBuilding=function(bs,id)observe(bs,id);return remove(bs,id)end
            store.HistoryStartStatus=function()
                if waitForHistory then return 'WAITING' end
                if readiness then return readiness() end
            end
            store.VisitDevelopment=function(pid,receive)
                visit(pid,function(value,r)
                    receive(value,r)
                    if delayIndex then partialRows=partialRows+1 end
                end)
                if delayIndex then error('DEVELOPMENT_TEST_INDEX_UNAVAILABLE')end
            end
            setupDevelopment()
            duringHistoryWait=active()
            assert(duringHistoryWait)
            waitForHistory=false
            Events.GameCoreEventPublishComplete.Fire()
            local view=dev.Refresh(0,source:GetID(),true)
            assert(partialRows>0 and view.stage=='HELD' and view.canSign==false)
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
            assert(afterSilentReturn and afterTurn and active(other))
            function historyRecovered()
                shared.FactChanges.Emit{owner=0, cityID=source:GetID(), kinds={'HISTORY'}, topic='DEVELOPMENT_RECOVERY', cause='DEFERRED_LIFECYCLE_RECOVERED'}
                shared.FactChanges.Flush()
                Events.GameCoreEventPublishComplete.Fire()
            end
            historyRecovered()
            assert(not active(other) and paidTargetWrites==0)
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
