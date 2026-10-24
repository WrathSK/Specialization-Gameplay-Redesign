"""Default-off B271 observers: actual Lua 5.1, no native connection or disk writes."""
from pathlib import Path
import sqlite3
import unittest
from project_paths import external_database
from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]


class ProbeDisable(unittest.TestCase):
    def lua(self):
        runtime = LuaRuntime(unpack_returned_tuples=True)
        runtime.execute('''
            nativeReads=0;traceCreates=0;records=0;adds=0;businessCalls=0
            ExposedMembers={};shared={};Game={};Players={}
            local function forbidden()nativeReads=nativeReads+1;error('unexpected native read')end
            setmetatable(Game,{__index=function()return forbidden end})
            setmetatable(Players,{__index=forbidden})
            P={Field=forbidden,IsTestPlayer=forbidden,Audit=forbidden,Mark=forbidden,
               SetProperty=forbidden,CreateBuilding=forbidden,RemoveBuilding=forbidden}
            SPCExpeditionTrainingDiagnostics={New=function()
                traceCreates=traceCreates+1
                return {Record=function()records=records+1 end}
            end}
            local function source()
                return setmetatable({},{__index=function(t,k)
                    local e={callbacks={}}
                    e.Add=function(f)adds=adds+1;e.callbacks[#e.callbacks+1]=f end
                    e.Remove=function(f)
                        for i=#e.callbacks,1,-1 do
                            if e.callbacks[i]==f then table.remove(e.callbacks,i)end
                        end
                    end
                    e.Fire=function(...)for _,f in ipairs(e.callbacks)do f(...)end end
                    t[k]=e;return e
                end})
            end
            Events=source();GameEvents=source()
        ''')
        runtime.execute((ROOT / 'Mod/EventTimingDiagnostics.lua').read_text())
        return runtime

    def assert_quiet(self, runtime):
        for name in ('nativeReads', 'traceCreates', 'records'):
            self.assertEqual(runtime.eval(name), 0, name)
        self.assertIsNone(runtime.eval('ExposedMembers.SPC_EventTiming'))
        self.assertIsNone(runtime.eval('shared.EventTiming'))

    def test_disabled_gameplay_and_ui_before_any_dependency_read(self):
        for order in (('GAMEPLAY', 'UI'), ('UI', 'GAMEPLAY')):
            with self.subTest(order=order):
                runtime = self.lua()
                self.assertFalse(runtime.eval('SPCEventTimingDiagnostics.ENABLED'))
                for side in order:
                    shared = 'shared' if side == 'GAMEPLAY' else 'nil'
                    runtime.execute(f"result=SPCEventTimingDiagnostics.Start(P,{shared},'{side}')")
                    self.assertIsNone(runtime.eval('result'))
                    self.assert_quiet(runtime)
                self.assertEqual(runtime.eval('adds'), 0)

    def test_ordinary_callbacks_and_order_survive_many_turns_and_events(self):
        runtime = self.lua()
        runtime.execute('''
            order={}
            Events.CityWorkerChanged.Add(function()order[#order+1]='first';businessCalls=businessCalls+1 end)
            Events.CityWorkerChanged.Add(function()order[#order+1]='second';businessCalls=businessCalls+1 end)
            Events.PlayerTurnActivated.Add(function()businessCalls=businessCalls+1 end)
            GameEvents.PlayerTurnStarted.Add(function()businessCalls=businessCalls+1 end)
            SPCEventTimingDiagnostics.Start(P,shared,'GAMEPLAY')
            SPCEventTimingDiagnostics.Start(P,nil,'UI')
            for turn=1,12 do
                Events.PlayerTurnDeactivated.Fire(0);Events.LocalPlayerTurnEnd.Fire()
                Events.PlayerTurnActivated.Fire(1);GameEvents.PlayerTurnStarted.Fire(0)
                Events.PlayerTurnActivated.Fire(0);Events.LocalPlayerTurnBegin.Fire()
                for i=1,500 do Events.CityWorkerChanged.Fire(0,17);Events.GameCoreEventPublishComplete.Fire()end
            end
        ''')
        self.assertEqual(runtime.eval('adds'), 4)
        self.assertEqual(runtime.eval('businessCalls'), 12 * 1003)
        self.assertTrue(runtime.eval("(function()for i=1,#order,2 do if order[i]~='first' or order[i+1]~='second'then return false end end;return true end)()"))
        self.assert_quiet(runtime)

    def test_load_clears_stale_scalars_and_observer_reference(self):
        runtime = self.lua()
        for side in ('UI', 'GAMEPLAY'):
            runtime.execute('''
                stale={accepting=true,sequenceEnabled=true,counts={audit={},dispatch={}}}
                ExposedMembers.SPC_EventTiming=stale
                shared.EventTiming={Verified=function()error('stale observer called')end}
            ''')
            runtime.execute(f"SPCEventTimingDiagnostics.Start(P,shared,'{side}')")
            self.assert_quiet(runtime)

    def test_right_click_cannot_reenable_or_touch_native_facts(self):
        runtime = self.lua()
        runtime.execute("SPCEventTimingDiagnostics.SEQUENCE_ENABLED=true;SPCEventTimingDiagnostics.Start(P,shared,'GAMEPLAY')")
        source = (ROOT / 'Mod/Gameplay.lua').read_text()
        start = source.index("  if params.Action=='EVENT_ORDER_TOGGLE' then")
        end = source.index("  if params.Action=='MEMORY_BEGIN'", start)
        runtime.execute('function request(playerID,params)\n' + source[start:end] + '\nend')
        runtime.execute("request(0,{Action='EVENT_ORDER_TOGGLE',Token='disabled-request'})")
        self.assertEqual(runtime.eval('shared.Snapshot'), 'B271时序探针已停用。')
        self.assertEqual(runtime.eval('shared.LastToken'), 'disabled-request')
        self.assertEqual(runtime.eval('adds'), 0)
        self.assert_quiet(runtime)

    def test_old_manual_counters_retained_without_automatic_b271_accumulation(self):
        runtime = self.lua()
        runtime.execute((ROOT / 'Mod/PerformanceCounters.lua').read_text())
        runtime.execute('''
            stale={accepting=true,counts={audit={},dispatch={}}}
            ExposedMembers.SPC_EventTiming=stale
            SPCEventTimingDiagnostics.Start(P,shared,'GAMEPLAY')
            for i=1,1000 do
                SPCPerformance.Observe('audit','CultureAesthetic')
                SPCPerformance.Observe('dispatch','FutureEvent')
            end
            assert(next(stale.counts.audit)==nil and next(stale.counts.dispatch)==nil)
            Game.GetCurrentGameTurn=function()return 5 end
            ExposedMembers.SPC_Performance=SPCPerformance.New()
            SPCPerformance.Count('building_check',3)
            ExposedMembers.SPC_MemoryAttribution={active=true,startTurn=5,audit={},dispatch={}}
            SPCPerformance.Observe('audit','CultureAesthetic')
            SPCPerformance.Observe('audit','NewUnknown')
            SPCPerformance.Observe('dispatch','FutureEvent')
        ''')
        self.assertEqual(runtime.eval('ExposedMembers.SPC_Performance.entries.building_check.total'), 3)
        self.assertEqual(runtime.eval('ExposedMembers.SPC_MemoryAttribution.audit.CultureAesthetic'), 1)
        self.assertEqual(runtime.eval('ExposedMembers.SPC_MemoryAttribution.audit.OTHER'), 1)
        self.assertEqual(runtime.eval('ExposedMembers.SPC_MemoryAttribution.dispatch.OTHER'), 1)
        self.assert_quiet(runtime)


class CarrierPillagePreserved(unittest.TestCase):
    def test_loaded_and_fresh_sql_on_readonly_engine_database_copy(self):
        source = sqlite3.connect(external_database(ROOT).as_uri() + '?mode=ro', uri=True)
        db = sqlite3.connect(':memory:')
        source.backup(db)
        source.close()
        self.addCleanup(db.close)
        target = {row[0] for row in db.execute(
            "SELECT BuildingType FROM Buildings WHERE InternalOnly=1 AND substr(BuildingType,1,13)='BUILDING_SPC_'"
        )}
        self.assertGreater(len(target), 4000)
        before = list(db.execute('SELECT * FROM Buildings_XP2 ORDER BY BuildingType'))
        columns = [row[1] for row in db.execute('PRAGMA table_info(Buildings_XP2)')]
        pillage = columns.index('Pillage')
        present = [row for row in before if row[0] in target]
        self.assertTrue(all(row[pillage] == 0 for row in present))
        foreign = [row for row in before if row[0] not in target]
        sql = (ROOT / 'Mod/Data/InternalCarrierPillage.sql').read_text()
        # Recreate only the original pre-SPC XP2 state in this disposable memory copy.
        db.execute("DELETE FROM Buildings_XP2 WHERE BuildingType IN (SELECT BuildingType FROM Buildings WHERE InternalOnly=1 AND substr(BuildingType,1,13)='BUILDING_SPC_')")
        self.assertEqual(list(db.execute('SELECT * FROM Buildings_XP2 ORDER BY BuildingType')), foreign)
        db.executescript(sql)
        after = list(db.execute('SELECT * FROM Buildings_XP2 ORDER BY BuildingType'))
        self.assertEqual([row for row in after if row[0] not in target], foreign)
        self.assertEqual({row[0] for row in after if row[0] in target and row[pillage] == 0}, target)
        db.executescript(sql)
        self.assertEqual(list(db.execute('SELECT * FROM Buildings_XP2 ORDER BY BuildingType')), after)
        print('B307 copied-engine carriers:', len(target), 'already applied:', len(present))


if __name__ == '__main__':
    unittest.main()
