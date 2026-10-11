"""B202 actual Store/Gate/Training local tests; native queue/event ordering remains a game gate."""
from pathlib import Path
import unittest
from test_expedition_spy_gate import gate
R=Path(__file__).resolve().parents[1]

def fixture():
    l=gate()
    l.execute('''
    hooks={};function event(name)return {Add=function(fn)hooks[name]=fn end}end
    for _,n in ipairs({'UnitAddedToMap','CityProductionCompleted','CityProductionChanged','CityProductionQueueChanged','GameCoreEventPublishComplete','PlayerTurnActivated','LoadScreenClose','CityTransfered'})do Events[n]=event(n)end
    GameEvents.SPC_ExpeditionTrainingRequest=event('request')
    marker=false;markerWrites=0;queueCount=0
    info.BUILDING_SPC_EXPEDITION_TRAINING_ACCESS={Index=999}
    buildings={};function city:GetBuildings()return buildings end
    function city:GetBuildQueue()return {}end
    P.HasBuilding=function(b,id)assert(id==999);return marker end
    P.CreateBuilding=function(q,id)markerWrites=markerWrites+1;if markerFail then return end;marker=true end
    P.RemoveBuilding=function(b,id)markerWrites=markerWrites+1;marker=false end
    ExposedMembers.SPC_ExpeditionQueueRead=function(pid,id)
      if queueError then error('UNREADABLE')end
      return {owner=pid,city=id,turn=currentTurn,count=queueCount}
    end
    function train(action,token,extra)
      local p={Action=action,Token=token,CityID=1,Reservation='r'};for k,v in pairs(extra or {})do p[k]=v end
      shared.ExpeditionTraining.Request(2,p);return ExposedMembers.SPC_ExpeditionTrainingReply
    end
    function reserve()assert(train('RESERVE','r').reserved);queueCount=1;assert(train('CONFIRM','c').confirmed)end
    function born(id,x)
      id=id or 50;units[id]=unit(id,100,2,x or 1,1);units[id].name='LOC_CITIZEN_TEST_A'
      shared.ExpeditionTraining.Birth(2,id)
    end
    function complete()queueCount=0;shared.ExpeditionTraining.Complete(2,1,0,100,false)end
    function pulse()shared.ExpeditionTraining.Pulse(2,false)end
    function state()return shared.ExpeditionGate.Training.Read(2)end
    ''')
    l.execute((R/'Mod/ExpeditionTraining.lua').read_text());l.execute('SPCExpeditionTraining.Start(P,shared)')
    return l

class Training(unittest.TestCase):
    def check(self,code):fixture().execute(code)
    def test_reserve_before_marker_and_no_spawn(self):
        self.check("assert(train('RESERVE','r').reserved);assert(state().phase=='TRAINING' and marker and storeWrites==1 and initCalls==0)")
    def test_both_event_orders_and_unchanged_travel_binding(self):
        for order in ['born();complete()','complete();born()']:
            with self.subTest(order=order):
                self.check("reserve();"+order+";pulse();assert(state().phase=='NAMING' and state().unitID==50 and state().sourceCity==1 and not marker);confirmName('name',50);assert(state().phase=='CREATED' and state().expectedName=='LOC_CITIZEN_TEST_A')")
    def test_competing_reservation_does_not_poison_first(self):
        self.check("reserve();assert(train('RESERVE','other').error);assert(state().phase=='TRAINING' and marker and state().trainingToken=='r')")
    def test_duplicate_notifications_idempotent(self):
        self.check("reserve();born();shared.ExpeditionTraining.Birth(2,50);complete();complete();pulse();local n=storeWrites;pulse();complete();assert(state().unitID==50 and storeWrites==n)")
    def test_multiple_births_hold(self):
        self.check("reserve();born();born(51);assert(state().phase=='HELD' and not marker)")
    def test_completion_other_city_hold(self):
        self.check("reserve();shared.ExpeditionTraining.Complete(2,2,0,100,false);assert(state().phase=='HELD' and not marker)")
    def test_endpoint_not_guessed(self):
        self.check("reserve();born(50,2);assert(state().phase=='HELD')")
    def test_birth_without_reserved_queue_not_adopted(self):
        self.check("born();assert(state().phase==nil and not shared.ExpeditionGate.Training.Available(2))")
    def test_unconfirmed_queue_birth_hold(self):
        self.check("train('RESERVE','r');born();assert(state().phase=='HELD')")
    def test_empty_queue_does_not_guess_cancellation(self):
        self.check("reserve();queueCount=0;pulse();assert(state().phase=='TRAINING' and not marker);born();complete();pulse();assert(state().phase=='NAMING')")
    def test_explicit_cancel_releases_only_proven_empty(self):
        self.check("reserve();queueCount=0;assert(train('CANCEL','x').confirmed);assert(state().phase=='ENDED' and not marker and shared.ExpeditionGate.Training.Available(2))")
    def test_cancel_with_birth_holds(self):
        self.check("reserve();born();queueCount=0;assert(train('CANCEL','x').error);assert(state().phase=='HELD')")
    def test_wrong_token_cannot_cancel_other_reservation(self):
        self.check("reserve();queueCount=0;assert(train('CANCEL','x',{Reservation='wrong'}).error);assert(state().phase=='TRAINING')")
    def test_native_duplicate_queue_hold(self):
        self.check("reserve();queueCount=2;pulse();assert(state().phase=='HELD' and not marker)")
    def test_source_reference_change_hold(self):
        self.check("reserve();city.token='changed';pulse();assert(state().phase=='HELD')")
    def test_qualification_not_assumed(self):
        for field in ["active=3","spec='RESEARCH'","factsError=true","pending=true"]:
            with self.subTest(field=field):self.check(field+";assert(train('RESERVE','r').error and not marker and state().phase==nil)")
    def test_write_failure_never_grants_marker(self):
        self.check("storeNoop=true;assert(train('RESERVE','r').error);assert(state().blocked and not marker and not shared.ExpeditionGate.Training.Available(2))")
    def test_marker_failure_keeps_reservation(self):
        self.check("markerFail=true;assert(train('RESERVE','r').error);assert(state().phase=='HELD' and not shared.ExpeditionGate.Training.Available(2))")
    def test_queue_unknown_after_admission_holds(self):
        self.check("reserve();queueError=true;pulse();assert(state().phase=='HELD')")
    def test_unrelated_units_and_completions_ignored(self):
        self.check("reserve();units[80]=unit(80,103,2,1,1);shared.ExpeditionTraining.Birth(2,80);shared.ExpeditionTraining.Complete(2,1,0,103,false);assert(state().phase=='TRAINING' and not state().trainingBorn and not state().trainingCompleted)")
    def test_load_queued_recovers_without_new_generation(self):
        self.check("reserve();local n=storeWrites;SPCExpeditionSpyGate.Start(P,shared);SPCExpeditionTraining.Start(P,shared);shared.ExpeditionTraining.Pulse(2,true);assert(state().phase=='TRAINING' and storeWrites==n)")
    def test_load_half_receipt_held_never_adopted(self):
        self.check("reserve();born();SPCExpeditionSpyGate.Start(P,shared);assert(state().phase=='HELD' and state().unitID==nil)")
    def test_load_missing_queue_held(self):
        self.check("reserve();queueCount=0;shared.ExpeditionTraining.Pulse(2,true);assert(state().phase=='HELD')")
    def test_long_training_partial_receipt_waits_for_matching_event(self):
        self.check("reserve();currentTurn=currentTurn+20;born();queueCount=0;pulse();assert(state().phase=='TRAINING');complete();pulse();assert(state().phase=='NAMING')")
    def test_completed_queue_stale_read_waits_with_capacity_reserved(self):
        self.check("reserve();born();complete();queueCount=1;pulse();assert(state().phase=='TRAINING');queueCount=0;pulse();assert(state().phase=='NAMING')")
    def test_held_loaded_transaction_revokes_access(self):
        self.check("reserve();born();SPCExpeditionSpyGate.Start(P,shared);SPCExpeditionTraining.Start(P,shared);shared.ExpeditionTraining.Pulse(2,true);assert(not marker and state().phase=='HELD')")
    def test_load_waits_bounded_for_ui_queue_reader(self):
        self.check("reserve();local reader=ExposedMembers.SPC_ExpeditionQueueRead;ExposedMembers.SPC_ExpeditionQueueRead=nil;shared.ExpeditionTraining.Pulse(2,true);assert(state().phase=='TRAINING');ExposedMembers.SPC_ExpeditionQueueRead=reader;hooks.GameCoreEventPublishComplete();assert(state().phase=='TRAINING' and marker)")
    def test_missing_ui_reader_event_budget_holds(self):
        self.check("reserve();ExposedMembers.SPC_ExpeditionQueueRead=nil;shared.ExpeditionTraining.Pulse(2,true);for i=1,12 do hooks.GameCoreEventPublishComplete()end;assert(state().phase=='HELD' and not marker)")
    def test_source_changes_during_final_registration_readback_holds(self):
        self.check("reserve();born();complete();local writer=P.SetProperty;P.SetProperty=function(...)local v=writer(...);city.token='changed';return v end;pulse();assert(state().phase=='HELD' and not marker)")
    def test_final_registration_write_failure_holds(self):
        self.check("reserve();born();complete();storeNoop=true;pulse();assert(state().phase=='HELD' and state().blocked and not marker)")
    def test_capacity_blocks_p0_create(self):
        self.check("reserve();req('CREATE','old');assert(initCalls==0 and state().phase=='TRAINING')")
    def test_error_before_reservation_does_not_mutate(self):
        self.check("queueError=true;assert(train('RESERVE','r').error);assert(storeWrites==0 and not marker)")

if __name__=='__main__':unittest.main()
