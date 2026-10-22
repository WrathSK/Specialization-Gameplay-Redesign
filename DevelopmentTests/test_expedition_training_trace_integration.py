"""B205 diagnostic delta against actual Gate/Store/Training; native effects mocked."""
from pathlib import Path
import os
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get('SPC_B205_REPO', HERE.parent))
if not (ROOT / 'DevelopmentTests/test_expedition_training.py').exists():
    raise RuntimeError('Set SPC_B205_REPO to the repository when running temporary integration tests')
sys.path.insert(0, str(ROOT / 'DevelopmentTests'))
from test_expedition_training import fixture

SOURCE = Path(os.environ.get('SPC_B205_DIAGNOSTICS_SOURCE', ROOT / 'Mod/ExpeditionTrainingDiagnostics.lua'))


def runtime(enabled=True):
    lua = fixture()
    lua.execute('''
    print=function()end
    population=16
    function city:GetPopulation()return population end
    function buildings:HasBuilding(id)assert(id==999);return marker end
    local row=info.UNIT_SPC_EXPEDITION_SPY;row.Index=100;row.Cost=60;row.CostProgressionParam1=15
    function city:GetBuildQueue()return {
      GetUnitCost=function(self,i)if i==7 then return 200 end;return 1 end,GetUnitProgress=function()return 0 end,
      GetSize=function()return queueCount end,GetCurrentProductionTypeHash=function()return 100 end}end
    info.UNIT_SPY=info.UNIT_SPY or {};info.UNIT_SPY.Index=7
    GameEvents.OnCityPopulationChanged=event('popGame');Events.CityPopulationChanged=event('popEvent')
    Events.PlayerTurnDeactivated=event('PlayerTurnDeactivated')
    function grow(n,pid,id)for i=1,n do population=population+1;hooks.popGame(pid or 2,id or 1,1);hooks.popEvent(pid or 2,id or 1,population)end end
    function stages(name)local t,n=diagnostic(),{};for _,e in ipairs(t and t.entries or {})do if e.stage==name then n[#n+1]=e end end;return n end
    function diagnostic()return ExposedMembers.SPC_B205TrainingTrace end
    function findStage(stage)
      local t=diagnostic();if not t then return end
      for i=#t.entries,1,-1 do if t.entries[i].stage==stage then return t.entries[i]end end
    end
    ''')
    lua.execute(SOURCE.read_text())
    lua.globals().SPCExpeditionTrainingDiagnostics.ENABLED = enabled
    lua.execute('SPCExpeditionTraining.Start(P,shared)')
    return lua


def plain(value):
    if hasattr(value, 'items'):
        return {plain(k): plain(v) for k, v in value.items()}
    return value


def snapshot(lua):
    return plain(lua.eval('''{state=state(), saved=gameProperties, writes=storeWrites,
      marker=marker, markerWrites=markerWrites, initCalls=initCalls,
      depth=shared.RequestDepth, nativeCalls=nativeCalls, properties=properties}'''))


class Integration(unittest.TestCase):
    def equivalent(self, script):
        baseline = runtime(False)
        observed = runtime(True)
        baseline.execute(script)
        observed.execute(script)
        self.assertEqual(snapshot(observed), snapshot(baseline))
        return observed

    def test_reserve_both_callback_orders_and_named_binding_equivalent(self):
        for order in ('born();complete()', 'complete();born()'):
            with self.subTest(order=order):
                lua = self.equivalent("reserve();" + order + ";pulse();confirmName('name',50)")
                lua.execute("assert(state().phase=='CREATED' and state().sourceCity==1 and state().unitID==50)")

    def test_pretraining_row_observed_without_build_and_reobserved_after_load_or_cost_change(self):
        from test_expedition_training_ui import ui
        lua = ui()
        lua.execute(SOURCE.read_text())
        lua.execute("""
         print=function()end
         adapter=SPCExpeditionTrainingUI.New(P,send,notify,build)
         adapter.Sync(city);adapter.Pulse()
         function rows()local data={City=city,UnitItems={}};adapter.Items(data);return data end
         rows()
         local trace=ExposedMembers.SPC_B205TrainingTrace
         assert(trace.entries[#trace.entries].stage=='UI_ROW')
         local n=trace.sequence
         for i=1,100 do rows()end
         assert(trace.sequence==n and builds==0 and storeWrites==0 and not marker)
         queue.GetUnitCost=function()return 1 end
         local data=rows();assert(data.UnitItems[1].Cost==1)
         assert(trace.sequence==n+1 and trace.entries[#trace.entries].nativeCost=='1')
         local loader=SPCExpeditionTrainingDiagnostics.New(P,'GAMEPLAY');loader.Load()
         n=trace.sequence;rows();assert(trace.sequence==n+1)
         assert(builds==0 and storeWrites==0 and state().phase==nil)
        """)

    def test_explicit_cancel_equivalent(self):
        self.equivalent("reserve();queueCount=0;assert(train('CANCEL','x').confirmed)")

    def test_bad_queue_and_marker_failure_equivalent(self):
        for script in ('reserve();queueCount=2;pulse()', "markerFail=true;train('RESERVE','r')"):
            with self.subTest(script=script):
                self.equivalent(script)

    def test_duplicate_notifications_equivalent(self):
        self.equivalent('reserve();born();born();complete();complete();pulse();pulse()')

    def test_loaded_training_recovery_equivalent(self):
        self.equivalent('reserve();hooks.LoadScreenClose()')

    def test_population_notifications_equivalent_and_aggregated(self):
        lua = self.equivalent('reserve();grow(2431);complete();born();pulse()')
        lua.execute("""
         local game={};for _,e in ipairs(stages('POP_CHANGE'))do if e.popSource=='GAME' then game[#game+1]=e.popEvents end end
         -- 1st, 2nd, 4th ... 2048th within the 64-entry ring (EVENT shares it).
         assert(table.concat(game,',')=='1,2,4,8,16,32,64,128,256,512,1024,2048',table.concat(game,','))
         local s=stages('POP_SUMMARY');assert(#s==2)
         for _,e in ipairs(s)do assert(e.popEvents=='2431' and e.population=='2447')end
         local g=s[1].popSource=='GAME' and s[1] or s[2];local v=s[1].popSource=='EVENT' and s[1] or s[2]
         assert(g.popSum=='2431' and g.popMin=='1' and g.popMax=='1' and g.popDelta=='1' and g.popTurn=='81')
         assert(v.popTo=='2447' and v.popSum=='0')
         local seq={};for _,e in ipairs(diagnostic().entries)do seq[e.stage]=seq[e.stage]or e.sequence end
         assert(seq.POP_SUMMARY<seq.COMPLETE_CALLBACK)
        """)

    def test_population_outside_training_or_source_city_not_observed(self):
        lua = runtime(True)
        lua.execute("""grow(3);reserve();grow(2,2,999);grow(1,3,1)
         assert(#stages('POP_CHANGE')==0 and #stages('POP_SUMMARY')==0)""")

    def test_turn_boundaries_flush_and_mark_training_city(self):
        lua = self.equivalent('reserve();grow(3);hooks.PlayerTurnDeactivated(2);currentTurn=currentTurn+1;grow(1);hooks.PlayerTurnActivated(2)')
        lua.execute("""
         local e=stages('TURN_END');assert(#e==1 and e[1].population=='19' and e[1].phase=='TRAINING')
         local b=stages('TURN_BEGIN');assert(#b==1 and b[1].population=='20')
         -- Turn 81 had unreported 3rd events; the single turn-82 event was emitted at once.
         local s=stages('POP_SUMMARY');assert(#s==2 and s[1].popTurn=='81' and s[1].popEvents=='3' and s[2].popEvents=='3')
         local c=stages('POP_CHANGE');assert(c[#c].popTurn=='82' and c[#c].popEvents=='1')
         assert(s[2].sequence<e[1].sequence and e[1].sequence<c[#c].sequence and c[#c].sequence<b[1].sequence)
        """)

    def test_spy_native_cost_recorded_beside_expedition_cost(self):
        lua = runtime(True)
        lua.execute("reserve();local e=findStage('RESERVE_ENTRY');assert(e.nativeCost=='1' and e.spyNativeCost=='200')")

    def test_population_observer_exception_cannot_change_progression(self):
        baseline = runtime(False)
        observed = runtime(True)
        observed.execute("""SPCExpeditionTrainingDiagnostics.New=function()return {
          Event=function()error('DIAG_EVENT_FAIL')end,Load=function()end,Record=function()end}end
          SPCExpeditionTraining.Start(P,shared)""")
        script = "reserve();grow(5);hooks.PlayerTurnDeactivated(2);complete();born();pulse();confirmName('name',50)"
        baseline.execute(script)
        observed.execute(script)
        self.assertEqual(snapshot(observed), snapshot(baseline))

    def test_population_delta_is_logged_at_marker_boundary_only(self):
        lua = runtime(True)
        lua.execute('''reserve();born();complete();
         local remove=P.RemoveBuilding
         P.RemoveBuilding=function(...)local result=remove(...);population=2447;return result end
         pulse();
         assert(findStage('MARKER_BEFORE').population=='16')
         assert(findStage('MARKER_AFTER').population=='2447')
         assert(findStage('COMPLETE_CALLBACK').population=='16')
         assert(findStage('FINISH_EXIT').population=='2447')
         assert(state().phase=='NAMING' and state().sourceCity==1)
        ''')

    def test_population_already_bad_before_completion_is_visible(self):
        lua = runtime(True)
        lua.execute("reserve();born();population=2447;complete();pulse();assert(findStage('COMPLETE_CALLBACK').population=='2447' and findStage('MARKER_BEFORE').population=='2447' and findStage('MARKER_AFTER').population=='2447')")

    def test_successful_callbacks_record_new_receipt_flags(self):
        lua = runtime(True)
        lua.execute("reserve();born();complete();assert(findStage('BIRTH_EXIT').born=='50' and findStage('COMPLETE_EXIT').completed=='true')")

    def test_diagnostic_event_exception_cannot_change_progression(self):
        baseline = runtime(False)
        observed = runtime(True)
        observed.execute('''SPCExpeditionTrainingDiagnostics.New=function()return {
          Event=function()error('DIAG_EVENT_FAIL')end,Load=function()end,Record=function()end}end
          SPCExpeditionTraining.Start(P,shared)''')
        script = "reserve();born();complete();pulse();confirmName('name',50)"
        baseline.execute(script)
        observed.execute(script)
        self.assertEqual(snapshot(observed), snapshot(baseline))

    def test_diagnostic_load_record_exception_cannot_skip_recovery(self):
        baseline = runtime(False)
        observed = runtime(True)
        observed.execute('''SPCExpeditionTrainingDiagnostics.New=function()return {
          Event=function()end,Load=function()error('DIAG_LOAD_FAIL')end,
          Record=function()error('DIAG_RECORD_FAIL')end}end
          SPCExpeditionTraining.Start(P,shared)''')
        script = 'reserve();hooks.LoadScreenClose()'
        baseline.execute(script)
        observed.execute(script)
        self.assertEqual(snapshot(observed), snapshot(baseline))

    def test_no_source_city_nontraining_birth_and_completion_do_not_lookup_nil(self):
        lua = runtime(True)
        lua.execute('''local cities=Players[2]:GetCities();local find=cities.FindID
         cities.FindID=function(self,id)assert(id~=nil,'NIL_ID');return find(self,id)end
         born();shared.ExpeditionTraining.Complete(2,nil,0,100,false)
         assert(state().phase==nil and storeWrites==0 and markerWrites==0)
        ''')

    def test_diagnostic_city_lookup_error_cannot_escape_nontraining_callback(self):
        lua = runtime(True)
        lua.execute('''local cities=Players[2]:GetCities();local find=cities.FindID
         cities.FindID=function(self,id)if id==999 then error('DIAG_LOOKUP_ONLY')end;return find(self,id)end
         shared.ExpeditionTraining.Complete(2,999,0,100,false)
         assert(state().phase==nil and storeWrites==0 and markerWrites==0)
        ''')


if __name__ == '__main__':
    unittest.main()
