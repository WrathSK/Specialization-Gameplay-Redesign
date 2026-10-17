"""B218 actual Gameplay Gate; diagnostic observations never repair a task."""
import sys
import unittest
from pathlib import Path
import test_expedition_spy_task as base
from test_expedition_missions import MISSION_FIXTURE
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from read_expedition_trace import GATE_PATTERN

class PlacementDiagnostic(unittest.TestCase):
    def ready(self):
        l=base.gate()
        l.execute("""
         Events.UnitMoveComplete={Add=function(fn)movementEvent=fn end}
         SPCExpeditionSpyGate.Start(P,shared)
         req('CREATE','a');nativeDispatch('b');arrival(41,true,false)
        """)
        l.execute(MISSION_FIXTURE)
        lines=[];l.globals().print=lines.append
        return l,lines

    def test_failed_immediate_readback_and_later_event_never_resume(self):
        l,lines=self.ready()
        l.execute("""
         foreignUnits[7]=unit(7,101,3,15,9);placeNoop=true
         local r=startMission('t',PLACES)
         assert(r.phase=='HELD' and r.error=='EXACT_PLACEMENT_REJECTED' and not r.taskStart and insightWrites==0)
         local writes=storeWrites;units[41].y=9;movementEvent(2,41,15,9)
         assert(storeWrites==writes and insightWrites==0 and foreignUnits[7].y==9)
         assert(req('READ','read').phase=='HELD')
        """)
        diag=[x for x in lines if 'placement=' in x]
        self.assertTrue(any('placement=POST' in x and 'actual=15,8' in x for x in diag))
        self.assertTrue(any('placement=MOVE_EVENT' in x and 'actual=15,9' in x for x in diag))
        self.assertTrue(any('otherOwner=3 otherID=7' in x for x in diag))
        self.assertTrue(all(GATE_PATTERN.fullmatch(x) for x in diag))

    def test_success_with_synchronous_event_preserves_task_and_reward(self):
        l,lines=self.ready()
        l.execute("""
         local original=UnitManager.PlaceUnit
         UnitManager.PlaceUnit=function(u,x,y)original(u,x,y);movementEvent(u:GetOwner(),u:GetID(),x,y)end
         assert(startMission('t',PLACES).phase=='TASK_RUNNING')
         currentTurn=85;ownTurn(2);release('r');assert(insightWrites==1 and units[41].y==8)
        """)
        self.assertTrue(any('placement=MOVE_EVENT' in x for x in lines))

    def test_sync_removal_does_not_hide_post_sample(self):
        l,lines=self.ready()
        l.execute("UnitManager.PlaceUnit=function(u)units[41]=nil;removed(2,41)end;assert(startMission('t',PLACES).phase=='HELD')")
        self.assertTrue(any('placement=POST' in x and 'actual=UNKNOWN,UNKNOWN' in x for x in lines))

    def test_native_exception_preserved_and_logged(self):
        l,lines=self.ready()
        l.execute("UnitManager.PlaceUnit=function()error('NATIVE_TEST_ERROR',0)end;local r=startMission('t',PLACES);assert(r.error=='NATIVE_TEST_ERROR' and r.phase=='HELD' and insightWrites==0)")
        self.assertTrue(any('placement=API_ERROR' in x for x in lines))

    def test_diagnostic_failure_does_not_change_success(self):
        l,lines=self.ready()
        l.execute("Units.GetUnitsInPlot=function()error('no diagnostic read')end;assert(startMission('t',PLACES).phase=='TASK_RUNNING' and placeCalls==1)")
        self.assertTrue(any('occupants=UNKNOWN' in x for x in lines))

    def test_unrelated_events_ignored_and_watch_bounded(self):
        l,lines=self.ready();l.execute("placeNoop=true;startMission('t',PLACES)")
        n=len(lines);l.execute("for i=1,100 do movementEvent(3,41,1,1);movementEvent(2,42,1,1)end")
        self.assertEqual(n,len(lines))
        l.execute("for i=1,100 do movementEvent(2,41,15,8)end")
        self.assertEqual(6,sum('placement=MOVE_EVENT' in x and 'requested=' in x for x in lines))
        n=len(lines);l.execute("movementEvent(2,41,15,9)");self.assertEqual(n,len(lines))

    def test_turn_and_end_clear_watch_even_when_held(self):
        for action in ["ownTurn(2)","req('END','end',41)","removed(2,41)"]:
            with self.subTest(action=action):
                l,lines=self.ready();l.execute("placeNoop=true;startMission('t',PLACES);"+action)
                n=len(lines);l.execute("movementEvent(2,41,15,9)");self.assertEqual(n,len(lines))

    def test_occupant_limit_and_no_persistent_diagnostic_fields(self):
        l,lines=self.ready();l.execute("for i=1,20 do foreignUnits[i]=unit(i,101,3,15,9)end;placeNoop=true;startMission('t',PLACES)")
        self.assertTrue(any('occupants=TRUNCATED' in x for x in lines))
        self.assertEqual(8,sum('placement=PRE' in x and ' occupant=' in x for x in lines))
        l.execute("for _,v in pairs(gameProperties)do if type(v)=='table' and v.state then assert(v.state.placementWatch==nil and v.state.placementSequence==nil)end end")

if __name__=='__main__':unittest.main()
