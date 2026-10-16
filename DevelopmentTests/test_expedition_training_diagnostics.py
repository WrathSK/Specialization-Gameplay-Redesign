"""B205 actual Lua diagnostic-only counterexamples; no native game claims."""
from pathlib import Path
import os
import unittest
from lupa import LuaRuntime

HERE = Path(__file__).resolve().parent
DEFAULT = HERE.parent / 'Mod/ExpeditionTrainingDiagnostics.lua'
if not DEFAULT.exists():
    DEFAULT = HERE / 'ExpeditionTrainingDiagnostics.lua'
SOURCE = Path(os.environ.get('SPC_B205_DIAGNOSTICS_SOURCE', DEFAULT))


def fixture():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
    ExposedMembers={}; currentTurn=88; population=16; nativeCost=1; marker=false
    propertyWrites=0; gcCalls=0; nativeWrites=0; printed={}; logged={}; listeners={}
    Game={GetCurrentGameTurn=function()return currentTurn end,
     SetProperty=function()propertyWrites=propertyWrites+1;error('UNEXPECTED_WRITE')end}
    collectgarbage=function()gcCalls=gcCalls+1;error('UNEXPECTED_GC')end
    print=function(line)printed[#printed+1]=line end
    local event={Add=function(fn)listeners[fn]=true end,Remove=function(fn)listeners[fn]=nil end}
    setmetatable(event,{__call=function()for fn in pairs(listeners)do fn()end end})
    LuaEvents={SPC_B205TrainingTrace=event}
    UI={DataError=function(line)logged[#logged+1]=line end}
    Locale={Lookup=function(key,...)return key end}
    local unit={Index=248,Hash=10248,UnitType='UNIT_SPC_EXPEDITION_SPY',Cost=60,
      CostProgressionModel='COST_PROGRESSION_PREVIOUS_COPIES',CostProgressionParam1=15}
    local building={Index=2802,Hash=12802,BuildingType='BUILDING_SPC_EXPEDITION_TRAINING_ACCESS'}
    info={Units={UNIT_SPC_EXPEDITION_SPY=unit,[248]=unit,UNIT_SPY={Cost=60}},
      Buildings={BUILDING_SPC_EXPEDITION_TRAINING_ACCESS=building,[2802]=building}}
    P={Info=function(name,key)return info[name] and info[name][key]end}
    queue={GetUnitCost=function(self,id)assert(id==248);return nativeCost end,
      GetUnitProgress=function()return 0 end,GetSize=function()return 1 end,
      GetCurrentProductionTypeHash=function()return 10248 end}
    buildings={HasBuilding=function(self,id)assert(id==2802);return marker end}
    city={GetOwner=function()return 2 end,GetID=function()return 393220 end,
      GetPopulation=function()return population end,GetBuildQueue=function()return queue end,
      GetBuildings=function()return buildings end,
      SetProperty=function()propertyWrites=propertyWrites+1;error('UNEXPECTED_WRITE')end,
      ChangePopulation=function()nativeWrites=nativeWrites+1;error('UNEXPECTED_WRITE')end}
    state={phase='TRAINING',trainingToken='TRAIN:B205:1',trainingQueued=true,trainingBorn=50,trainingCompleted=true}
    function trace()return ExposedMembers.SPC_B205TrainingTrace end
    function last()return trace().entries[#trace().entries]end
    function unchanged()assert(propertyWrites==0 and nativeWrites==0 and gcCalls==0)end
    ''')
    lua.execute(SOURCE.read_text())
    lua.execute('M=SPCExpeditionTrainingDiagnostics; a=M.New(P,"GAMEPLAY")')
    return lua


class Diagnostics(unittest.TestCase):
    def check(self, code):
        lua = fixture()
        lua.execute(code)
        lua.execute('unchanged()')

    def test_definition60_native1_recorded_independently(self):
        self.check("a.Event('ADMISSION',city,state);assert(last().definitionCost=='60' and last().nativeCost=='1' and last().costStep=='15' and last().populationCost=='NIL')")

    def test_reverse_type_identity_and_zero_progress(self):
        self.check("a.Event('ADMISSION',city,state);assert(last().unitIndex=='248' and last().unitReverse=='UNIT_SPC_EXPEDITION_SPY' and last().markerIndex=='2802' and last().markerReverse=='BUILDING_SPC_EXPEDITION_TRAINING_ACCESS' and last().nativeProgress=='0')")

    def test_marker_absent_is_false_not_unknown(self):
        self.check("marker=false;a.Event('MARKER_AFTER',city,state);assert(last().markerPresent=='false',last().markerPresent)")

    def test_marker_before_after_population_localization(self):
        self.check("marker=true;a.Event('MARKER_BEFORE',city,state);local before=last();population=2447;marker=false;a.Event('MARKER_AFTER',city,state);assert(before.population=='16' and before.markerPresent=='true' and last().population=='2447' and last().markerPresent=='false');assert(state.phase=='TRAINING' and state.trainingBorn==50)")

    def test_already_bad_completion_population_not_attributed_later(self):
        self.check("population=2447;a.Event('COMPLETE_ENTRY',city,state);local before=last();a.Event('MARKER_AFTER',city,state);assert(before.population=='2447' and last().population=='2447')")

    def test_record_ring_budget_and_suppressed_events_bounded(self):
        self.check("for i=1,1000 do a.Record('REPEAT',{count=i})end;assert(trace().sequence==96 and #trace().entries==64 and trace().suppressed==905);assert(#printed==96)")

    def test_duplicate_same_stage_suppressed_without_budget_consumption(self):
        self.check("for i=1,1000 do a.Record('SAME',{count=1})end;assert(trace().sequence==2 and #trace().entries==2 and trace().suppressed==0)")

    def test_no_native_objects_or_private_strings_retained(self):
        self.check("local object=setmetatable({},{__tostring=function()error('STRINGIFIED')end});a.Record('SAFE',{reservation=object,reader='/private/home/user',bridge='line\\nsecret',count=string.rep('x',101)});local e=last();assert(e.reservation=='OMITTED_table' and e.reader=='REDACTED' and e.bridge=='REDACTED' and e.count=='REDACTED');for k,v in pairs(e)do assert(type(v)=='string' or k=='sequence' and type(v)=='number')end;assert(not e.line:find('/private'))")

    def test_throwing_native_getters_do_not_propagate(self):
        self.check("city.GetPopulation=function()error('PRIVATE_PATH')end;queue.GetUnitCost=function()error('SECRET')end;buildings.HasBuilding=function()error('BAD')end;a.Event('READ_FAIL',city,state);assert(last().population=='READ_ERROR' and last().nativeCost=='READ_ERROR' and last().markerPresent=='READ_ERROR');assert(not last().line:find('PRIVATE_PATH') and not last().line:find('SECRET'))")

    def test_missing_native_getters_and_info_do_not_propagate(self):
        self.check("city.GetPopulation=nil;P.Info=function()error('PRIVATE_PATH')end;a.Event('MISSING',city,state);assert(last().population=='UNAVAILABLE' and last().nativeCost=='INDEX_UNKNOWN' and last().markerPresent=='INDEX_UNKNOWN')")

    def test_getter_reentry_has_one_sample(self):
        self.check("local n=trace().sequence;city.GetPopulation=function()a.Event('REENTER',city,state);return 16 end;a.Event('OUTER',city,state);assert(trace().sequence==n+1 and last().stage=='OUTER')")

    def test_print_and_event_errors_do_not_propagate(self):
        self.check("print=function()error('PRINT_ERROR')end;LuaEvents.SPC_B205TrainingTrace=setmetatable({},{__call=function()error('EVENT_ERROR')end});a.Event('CAPTURE',city,state);assert(last().stage=='CAPTURE')")

    def test_sink_missing_does_not_discard_trace(self):
        self.check("UI=nil;local sink=M.Sink(P);a.Event('NO_SINK',city,state);assert(trace().sinkStatus=='UNAVAILABLE' and last().stage=='NO_SINK');sink.Stop()")

    def test_sink_throw_stops_without_retry(self):
        self.check("local calls=0;UI.DataError=function()calls=calls+1;error('PRIVATE_ERROR')end;local sink=M.Sink(P);assert(calls==1 and trace().sinkStatus=='ERROR_STOP');for i=1,20 do a.Record('LATER',{count=i})end;sink.Stop();assert(calls==1)")

    def test_sink_reentry_cannot_loop(self):
        self.check("local calls=0;UI.DataError=function()calls=calls+1;LuaEvents.SPC_B205TrainingTrace();a.Record('REENTER_SINK',{count=1})end;local sink=M.Sink(P);a.Event('NEXT',city,state);assert(calls<10 and trace().sequence<10);sink.Stop()")

    def test_sink_calls_returned_does_not_claim_disk_success(self):
        self.check("local sink=M.Sink(P);a.Event('NEXT',city,state);assert(trace().sinkStatus=='CALLS_RETURNED' and #logged>0);sink.Stop();local n=#logged;a.Record('STOPPED');assert(#logged==n)")

    def test_sink_emit_budget_is_bounded(self):
        self.check("local sink=M.Sink(P);for j=1,3 do local x=M.New(P,'GAMEPLAY');for i=1,90 do x.Record('VALUE',{count=i})end end;assert(#logged==128 and trace().sinkStatus=='BUDGET_STOP');sink.Stop()")

    def test_retained_exposedmembers_gameplay_then_ui_replacement(self):
        self.check("local gp1=a.id;local ui1=M.New(P,'PRODUCTION_UI');local oldUI=ui1.id;local gp2=M.New(P,'GAMEPLAY');assert(gp2.id~=gp1 and last().previous==gp1 and last().ui==oldUI);local ui2=M.New(P,'PRODUCTION_UI');assert(last().previous==oldUI and last().gp==gp2.id);assert(trace().roles.GAMEPLAY==gp2.id and trace().roles.PRODUCTION_UI==ui2.id)")

    def test_retained_exposedmembers_ui_then_gameplay_replacement(self):
        self.check("local oldGP=a.id;local ui1=M.New(P,'PRODUCTION_UI');local ui2=M.New(P,'PRODUCTION_UI');assert(last().gp==oldGP and last().previous==ui1.id);local gp2=M.New(P,'GAMEPLAY');assert(last().ui==ui2.id and last().previous==oldGP and last().gp==gp2.id)")

    def test_bridge_generations_observed_without_replacement(self):
        self.check("local reader=function()return 'OLD' end;ExposedMembers.SPC_ExpeditionQueueRead=reader;trace().bridge='UI:OLD';a.Event('QUEUE_READ',city,state,{reader='UI:OLD',readerLoad=1});assert(last().bridge=='UI:OLD' and last().reader=='UI:OLD' and last().readerLoad=='1');assert(ExposedMembers.SPC_ExpeditionQueueRead==reader and state.phase=='TRAINING')")

    def test_load_counts_and_report_bounded(self):
        self.check("a.Load();a.Load();assert(a.loads==2 and last().loads=='2');for i=1,20 do a.Record('READ',{count=i})end;local report=M.Report();local _,n=report:gsub('#','');assert(n==8)")

    def test_disabled_no_additional_trace_or_sink(self):
        self.check("local n=trace().sequence;M.ENABLED=false;local x=M.New(P,'PRODUCTION_UI');x.Event('OFF',city,state);x.Load();local sink=M.Sink(P);sink.Stop();assert(trace().sequence==n and #logged==0 and M.Report()=='')")


if __name__ == '__main__':
    unittest.main()
