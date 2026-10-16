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
      GetUnitCost=function()return 1 end,GetUnitProgress=function()return 0 end,
      GetSize=function()return queueCount end,GetCurrentProductionTypeHash=function()return 100 end}end
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
