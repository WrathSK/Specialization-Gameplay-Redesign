"""Gate capacity input provenance from existing scalar state and existing unit hooks."""
import json,unittest
from refactor_harness import ROOT,measure
from test_refactor_s9b3 import profile
import test_expedition_training as previous
import test_expedition_training_ui as prior_ui


def runtime():
 with profile():v=previous.fixture()
 v.execute("capacity=shared.ExpeditionGate.Training;function stamp()return capacity.CapacityInputStamp(2)end");return v

class Capacity(unittest.TestCase):
 def test_pure_getter_performs_zero_native_unit_store_clock_or_property_reads(self):
  v=runtime();v.execute("local before=stamp();local writes=storeWrites;local function no()error('NATIVE_FORBIDDEN')end;Players[2].GetUnits=no;Game.GetProperty=no;Game.GetCurrentGameTurn=no;P.IsTestPlayer=no;for i=1,1000 do assert(stamp()==before)end;assert(storeWrites==writes and capacity.CapacityInputStamp(3)=='OWNER_MISMATCH')")
  measure('S9a3b_capacity_input',{'queries':1000,'native_reads':0,'unit_enumerations':0,'Store_writes':0,'new_native_hooks':0,'new_unit_cache':0,'UI_migrated':False,'conservative_owner_unit_event_invalidation':True})
 def test_unreserved_birth_changes_capacity_stamp_without_activity_transition_or_adoption(self):
  v=runtime();v.execute("local before=stamp();local r=(ExposedMembers.SPC_ExpeditionActivity or {}).revision;local w=storeWrites;born();assert(stamp()~=before and (ExposedMembers.SPC_ExpeditionActivity or {}).revision==r and state().phase==nil and not capacity.Available(2)and storeWrites==w and initCalls==0)")
 def test_three_family_presence_and_removal_recover_through_original_Available(self):
  for kind in (100,102,104):
   v=runtime();v.execute("info[104]={UnitType='UNIT_SPC_EXPEDITION_ZERO'};local before=stamp();units[70]=unit(70,...,2,1,1);shared.ExpeditionTraining.Birth(2,70);local bornStamp=stamp();assert(bornStamp~=before and not capacity.Available(2));units[70]=nil;removed(2,70);assert(stamp()~=bornStamp and capacity.Available(2)and storeWrites==0 and initCalls==0)",kind)
 def test_known_foreign_events_do_not_invalidate_and_plain_local_units_only_mark(self):
  v=runtime();v.execute("local before=stamp();shared.ExpeditionTraining.Birth(3,999);removed(3,999);assert(stamp()==before);units[80]=unit(80,103,2,1,1);shared.ExpeditionTraining.Birth(2,80);assert(stamp()~=before and capacity.Available(2)and state().phase==nil and storeWrites==0 and initCalls==0)")
 def test_blocked_native_write_is_immediately_present_without_new_read(self):
  v=runtime();v.execute("local before=stamp();storeNoop=true;assert(train('RESERVE','r').error);local failed=stamp();assert(failed~=before and failed:find('BLOCKED',1,true));local writes=storeWrites;Game.GetProperty=function()error('NO_NATIVE')end;for i=1,1000 do assert(stamp()==failed)end;assert(storeWrites==writes and not marker)")
 def test_busy_native_callback_is_visible_then_returns_to_idle_without_epoch_churn(self):
  v=runtime();v.execute("local before=stamp();local read=Players[2].GetUnits;local inside;Players[2].GetUnits=function(...)inside=stamp();return read(...)end;req('READ','CAPACITY');assert(inside and inside:find(':BUSY:',1,true)and stamp()==before and storeWrites==0)")
 def test_observer_failure_does_not_change_existing_birth_or_training_receipt(self):
  v=runtime();v.execute("reserve();capacity.MarkUnitCapacity=function()error('SIGNAL_FAILED')end;born();assert(state().trainingBorn==50 and stamp():find('OBSERVER_FAILED',1,true));complete();pulse();assert(state().phase=='NAMING'and initCalls==0 and not marker)")
 def test_phase_and_same_turn_second_event_are_not_one_update_per_turn(self):
  v=runtime();v.execute("local before=stamp();reserve();local held=stamp();assert(held~=before and held:find('TRAINING',1,true));local turn=currentTurn;units[81]=unit(81,103,2,1,1);shared.ExpeditionTraining.Birth(2,81);local one=stamp();removed(2,81);assert(stamp()~=one and currentTurn==turn);queueCount=0;assert(train('CANCEL','c2').confirmed and stamp():find('ENDED',1,true))")

 def test_old_service_observer_failure_cannot_poison_successor_session(self):
  v=runtime();v.execute("local old=capacity;old.CapacityObservationFailed(true);assert(stamp():find('OBSERVER_FAILED',1,true));SPCExpeditionSpyGate.Start(P,shared);capacity=shared.ExpeditionGate.Training;local clean=stamp();assert(not clean:find('OBSERVER_FAILED',1,true));old.CapacityObservationFailed(true);old.MarkUnitCapacity(2);assert(stamp()==clean)")

 def test_public_observer_failure_cannot_interrupt_original_removed_duties(self):
  v=runtime();v.execute("reserve();born();complete();pulse();assert(state().phase=='NAMING');capacity.MarkUnitCapacity=function()error('PUBLIC_OBSERVER_FAILURE')end;units[50]=nil;assert(pcall(removed,2,50));local r=req('READ','REMOVED');assert(r.removedEvents==1 and r.phase=='HELD')")

class OriginalTraining(unittest.TestCase):
 def test_original_training_admission_completion_queue_receipts_and_nonreplay_assertions(self):
  names=unittest.defaultTestLoader.getTestCaseNames(previous.Training)
  with profile():
   for name in names:getattr(previous.Training(name),name)()
  measure('S9a3b_original_training',{'assertions':len(names),'current_runtime':True,'native_save_or_admission_rules_changed':False})
 def test_original_UI_reservation_build_and_lost_ACK_assertions_remain(self):
  names=unittest.defaultTestLoader.getTestCaseNames(prior_ui.UI)
  with profile():
   for name in names:getattr(prior_ui.UI(name),name)()
  measure('S9a3b_original_training_UI',{'assertions':len(names),'current_runtime':True,'global_refresh_still_present':True})


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9a3a'])])

if __name__=='__main__':unittest.main()
