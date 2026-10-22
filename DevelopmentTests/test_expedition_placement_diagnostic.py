"""B220 retained entry-city placement diagnostics; mission-site movement is deferred."""
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
         targetCity.y=9
         entryCity={id=11,owner=3,x=15,y=8}
         for k,v in pairs(targetCity)do if type(v)=='function'then entryCity[k]=v end end
         targetCities.Members=function()local a={targetCity,entryCity};local i=0;return function()i=i+1;if a[i]then return i,a[i]end end end
         PlayersVisibility={[2]={IsRevealed=function(self,x,y)return y~=9 end}}
         req('CREATE','a');nativeDispatch('b',{TargetY=9,EntryX=15,EntryY=8})
         function entryArrival()
          local old=units[40];local u=unit(41,100,2,15,8);u.name=old.name
          units[40]=nil;units[41]=u;currentTurn=83;ownTurn(2);return req('READ','arrival')
         end
        """)
        l.execute(MISSION_FIXTURE)
        lines=[];l.globals().print=lines.append
        return l,lines

    def test_failed_immediate_readback_and_later_event_never_resume(self):
        l,lines=self.ready()
        l.execute("""
         foreignUnits[7]=unit(7,101,3,15,9);placeNoop=true
         local r=entryArrival()
         assert(r.phase=='HELD' and r.stop=='EXACT_PLACEMENT_REJECTED' and not r.taskStart and insightWrites==0)
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
         assert(entryArrival().phase=='ARRIVED' and units[41].y==9 and insightWrites==0)
        """)
        self.assertTrue(any('placement=MOVE_EVENT' in x for x in lines))

    def test_sync_removal_does_not_hide_post_sample(self):
        l,lines=self.ready()
        l.execute("UnitManager.PlaceUnit=function(u)units[41]=nil;removed(2,41)end;assert(entryArrival().phase=='HELD')")
        self.assertTrue(any('placement=POST' in x and 'actual=UNKNOWN,UNKNOWN' in x for x in lines))

    def test_native_exception_preserved_and_logged(self):
        l,lines=self.ready()
        l.execute("UnitManager.PlaceUnit=function()error('NATIVE_TEST_ERROR',0)end;local r=entryArrival();assert(r.stop=='NATIVE_TEST_ERROR' and r.phase=='HELD' and insightWrites==0)")
        self.assertTrue(any('placement=API_ERROR' in x for x in lines))

    def test_diagnostic_failure_does_not_change_success(self):
        l,lines=self.ready()
        l.execute("Units.GetUnitsInPlot=function()error('no diagnostic read')end;assert(entryArrival().phase=='ARRIVED' and placeCalls==1)")
        self.assertTrue(any('occupants=UNKNOWN' in x for x in lines))

    def test_unrelated_events_ignored_and_watch_bounded(self):
        l,lines=self.ready();l.execute("placeNoop=true;entryArrival()")
        n=len(lines);l.execute("for i=1,100 do movementEvent(3,41,1,1);movementEvent(2,42,1,1)end")
        self.assertEqual(n,len(lines))
        l.execute("for i=1,100 do movementEvent(2,41,15,8)end")
        self.assertEqual(6,sum('placement=MOVE_EVENT' in x and 'requested=' in x for x in lines))
        n=len(lines);l.execute("movementEvent(2,41,15,9)");self.assertEqual(n,len(lines))

    def test_turn_and_end_clear_watch_even_when_held(self):
        for action in ["ownTurn(2)","req('END','end',41)","removed(2,41)"]:
            with self.subTest(action=action):
                l,lines=self.ready();l.execute("placeNoop=true;entryArrival();"+action)
                n=len(lines);l.execute("movementEvent(2,41,15,9)");self.assertEqual(n,len(lines))

    def test_occupant_limit_and_no_persistent_diagnostic_fields(self):
        l,lines=self.ready();l.execute("for i=1,20 do foreignUnits[i]=unit(i,101,3,15,9)end;placeNoop=true;entryArrival()")
        self.assertTrue(any('occupants=TRUNCATED' in x for x in lines))
        self.assertEqual(8,sum('placement=PRE' in x and ' occupant=' in x for x in lines))
        l.execute("for _,v in pairs(gameProperties)do if type(v)=='table' and v.state then assert(v.state.placementWatch==nil and v.state.placementSequence==nil)end end")

if __name__=='__main__':unittest.main()
