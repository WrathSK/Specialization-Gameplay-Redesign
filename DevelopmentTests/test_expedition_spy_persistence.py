"""B201 actual Gate + Property Store reconstruction and native-action boundaries.

Mocks retain the same native world while recreating the Gameplay context. These
tests establish local state/action behavior, not native serialization or travel.
"""
import unittest

import test_expedition_spy_gate as previous


def fixture():
    lua = previous.gate()
    lua.execute("""
      function copy(value)
       if type(value)~='table'then return value end
       local out={};for key,v in pairs(value)do out[key]=copy(v)end;return out
      end
      function restart()
       gameProperties=copy(gameProperties)
       ExposedMembers={};SPCExpeditionSpyGate.Start(P,shared)
      end
      function saved()return gameProperties.SPC_EXPEDITION_TEAM_P2 end
      function create()return req('CREATE','create')end
      function arrive()
       local old=units[40];local name=old and old.name or saved().state.expectedName
       units[40]=nil;units[41]=unit(41,100,2,15,8);units[41].name=name
       currentTurn=83;ownTurn(2);return req('READ','arrival')
      end
      function ready()create();nativeDispatch('dispatch');return arrive()end
      function activity(result,token,overrides)
       local view=ExposedMembers.SPC_ExpeditionActivity
       local packet={Action='ACTIVITY',Token=token,UnitID=view.unitID,
        ActivityKey=view.activityKey,Result=result,Owned=true,
        SampleTurn=currentTurn,NativeOperation=-1,Sleeping=true,Awake=false}
       if result=='ARMED' then packet.Sleeping=false;packet.Awake=true end
       for k,v in pairs(overrides or {})do packet[k]=v end
       handler(2,packet);return ExposedMembers.SPC_ExpeditionActivityReply
      end
      function prepare()
       handler(2,{Action='TASK',Token='task',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1,Mission='PEOPLE',MissionX=15,MissionY=8})
       return ExposedMembers.SPC_ExpeditionGateReply
      end
      function running()
       ready();prepare();activity('ARMED','arm');return activity('ASLEEP','asleep')
      end
      function denyRespawn(token)
       local before=initCalls;req('CREATE',token);assert(initCalls==before)
      end
      function noNativeSideEffects()
       assert(nativeCalls==0 and properties==0 and placeCalls==0 and finishCalls==0)
      end
    """)
    return lua


class Reconstruction(unittest.TestCase):
    def test_empty_load_is_read_only_and_has_no_reservation(self):
        lua = fixture()
        lua.execute("restart();local r=req('READ','empty');assert(r.persistence=='ABSENT' and r.count==0 and not r.reservedCapacity and storeWrites==0 and initCalls==0);noNativeSideEffects()")

    def test_created_binding_and_generation_survive_context_restart(self):
        lua = fixture()
        lua.execute("""
          create();local before=req('READ','before');local writes=storeWrites;restart()
          local r=req('READ','after');assert(r.phase=='CREATED' and r.bound and r.persistence=='RESTORED')
          assert(r.teamKey==before.teamKey and r.expectedName==before.expectedName and r.sourceCity==1)
          assert(r.generation==before.generation and r.unitID==40 and storeWrites==writes and initCalls==1)
          noNativeSideEffects()
        """)

    def test_naming_load_does_not_invent_confirmation(self):
        lua = fixture()
        lua.execute("""
          rawreq('CREATE','create');assert(saved().state.phase=='NAMING');restart()
          local r=req('READ','after');assert(r.phase=='NAMING' and not r.bound and not r.expectedName)
          assert(not nativeDispatch('premature').nativePermit);denyRespawn('duplicate')
          r=confirmName('confirm');assert(r.phase=='CREATED' and r.bound and initCalls==1)
        """)

    def test_offmap_load_reserves_capacity_without_replaying_native_travel(self):
        lua = fixture()
        lua.execute("""
          create();nativeDispatch('dispatch');units[40]=nil;currentTurn=82;restart()
          local writes=storeWrites;local r=req('READ','after')
          assert(r.phase=='TRAVELLING' and r.count==1 and r.observedCount==0 and r.reservedCapacity)
          assert(not r.unitID and r.trackedID==40 and r.sourceCity==1 and not r.nativePermit)
          denyRespawn('duplicate');ownTurn(2);assert(storeWrites==writes and initCalls==1);noNativeSideEffects()
        """)

    def test_changed_id_arrival_updates_saved_binding_after_reload(self):
        lua = fixture()
        lua.execute("""
          create();nativeDispatch('dispatch');units[40]=nil;restart();local r=arrive()
          assert(r.phase=='ARRIVED' and r.bound and r.unitID==41 and r.createdID==40 and r.sourceCity==1)
          assert(saved().state.unitID==41 and saved().state.createdID==40)
          restart();r=req('READ','again');assert(r.phase=='ARRIVED' and r.bound and initCalls==1)
        """)

    def test_two_arrival_candidates_are_held_not_adopted(self):
        lua = fixture()
        lua.execute("""
          create();nativeDispatch('dispatch');local name=units[40].name;units[40]=nil;restart()
          for _,id in ipairs({41,42})do units[id]=unit(id,100,2,15,8);units[id].name=name end
          currentTurn=83;ownTurn(2);local r=req('READ','after')
          assert(r.phase=='HELD' and r.stop=='TEAM_NAME_AMBIGUOUS' and not r.bound)
          assert(saved().state.unitID==40);denyRespawn('duplicate');assert(initCalls==1 and destroys==0)
        """)

    def test_default_name_or_wrong_destination_does_not_reconstruct_identity(self):
        for change in ("units[41].name='LOC_TEST_DEFAULT'", "units[41].x=16"):
            with self.subTest(change=change):
                lua = fixture()
                lua.execute("create();nativeDispatch('dispatch');local name=units[40].name;units[40]=nil;restart();units[41]=unit(41,100,2,15,8);units[41].name=name;" + change + ";currentTurn=85;ownTurn(2);local r=req('READ','after');assert(r.phase=='HELD' and not r.bound and saved().state.unitID==40);denyRespawn('duplicate');assert(initCalls==1)")

    def test_prebatch_survivor_with_absent_record_is_cleanup_only(self):
        lua = fixture()
        lua.execute("""
          units[8]=unit(8,100,2,1,1);units[8].name='LOC_CITIZEN_TEST_A';restart()
          local r=req('READ','old');assert(r.persistence=='ABSENT' and r.unbound and r.count==1)
          denyRespawn('duplicate');assert(not nativeDispatch('dispatch',{UnitID=8}).nativePermit)
          req('END','end',8);assert(destroys==1 and not units[8] and saved().state.phase=='ENDED')
        """)

    def test_ended_record_retains_generation_and_new_team_key_survives_id_reuse(self):
        lua = fixture()
        lua.execute("""
          create();local oldKey=saved().state.teamKey;req('END','end',40);restart()
          local r=req('READ','ended');assert(r.phase=='ENDED' and r.count==0 and r.generation==1)
          create();r=req('READ','new');assert(r.phase=='CREATED' and r.generation==2 and r.unitID==40 and r.persistence=='CONFIRMED')
          assert(r.teamKey~=oldKey and initCalls==2 and destroys==1)
        """)

    def test_reloaded_uncertain_create_or_end_never_replays_native_action(self):
        for phase in ("CREATING", "ENDING"):
            with self.subTest(phase=phase):
                lua = fixture()
                lua.execute("create();saved().state.phase='" + phase + "';restart();local r=req('READ','after');assert(r.phase=='HELD' and r.stop=='EXPEDITION_NATIVE_TRANSACTION_UNCONFIRMED');denyRespawn('duplicate');assert(initCalls==1 and destroys==0);noNativeSideEffects()")

    def test_spawn_exception_without_unit_keeps_capacity_across_restart(self):
        lua = fixture()
        lua.execute("initThrowBefore=true;create();assert(not units[40]);restart();local r=req('READ','after');assert(r.phase=='HELD' and r.count==1 and r.observedCount==0 and r.reservedCapacity);initThrowBefore=false;denyRespawn('duplicate');assert(initCalls==1 and destroys==0)")

    def test_loaded_record_never_adopts_same_id_wrong_owner_type_or_name(self):
        for change in ("units[40].owner=3", "units[40].type_=103", "units[40].name='different'"):
            with self.subTest(change=change):
                lua = fixture()
                lua.execute("create();" + change + ";restart();local r=req('READ','after');assert(r.phase=='HELD' and not r.bound and r.reservedCapacity);denyRespawn('duplicate');assert(initCalls==1 and destroys==0)")


class ActivityReconstruction(unittest.TestCase):
    def test_pending_unarmed_load_requires_fresh_observation_without_starting_timer(self):
        lua = fixture()
        lua.execute("""
          ready();prepare();restart();local r=req('READ','after')
          assert(r.phase=='TASK_PREPARING' and r.recovering and not r.taskDue)
          assert(ExposedMembers.SPC_ExpeditionActivity.mode=='RECOVER')
          activity('RECOVERED','recover',{Sleeping=false,Awake=true,Owned=false})
          r=req('READ','awake');assert(r.phase=='TASK_PREPARING' and not r.recovering and not r.taskDue)
          assert(ExposedMembers.SPC_ExpeditionActivity.mode=='SLEEP');noNativeSideEffects()
        """)

    def test_preexisting_sleep_is_never_claimed_as_owned_or_released(self):
        lua = fixture()
        lua.execute("""
          ready();prepare();restart();activity('RECOVERED','recover',{Owned=false})
          local r=req('READ','sleep');assert(r.phase=='TASK_RUNNING' and not r.activityOwned and r.taskDue==85)
          currentTurn=85;ownTurn(2);r=req('READ','complete')
          assert(r.phase=='TASK_COMPLETE' and r.activityMode=='NONE' and not r.activityOwned)
          noNativeSideEffects()
        """)

    def test_armed_sleep_recovery_starts_full_timer_only_after_new_observation(self):
        lua = fixture()
        lua.execute("""
          ready();prepare();activity('ARMED','arm');restart();currentTurn=84
          ownTurn(2);assert(not req('READ','before').taskDue)
          activity('RECOVERED','recover');local r=req('READ','after')
          assert(r.phase=='TASK_RUNNING' and r.taskStart==84 and r.taskDue==86 and r.activityOwned)
          assert(saved().state.sleepConfirmed and saved().state.activityMode=='ASLEEP')
        """)

    def test_armed_awake_is_unknown_outcome_not_a_second_sleep_attempt(self):
        lua = fixture()
        lua.execute("""
          ready();prepare();activity('ARMED','arm');restart()
          activity('RECOVERED','recover',{Sleeping=false,Awake=true})
          local r=req('READ','after');assert(r.phase=='HELD' and r.stop=='ACTIVITY_SLEEP_OUTCOME_UNKNOWN')
          assert(not r.taskDue and r.taskCompletions==0);noNativeSideEffects()
        """)

    def test_running_sleep_recovers_original_due_turn_not_a_restarted_timer(self):
        lua = fixture()
        lua.execute("""
          running();currentTurn=84;restart();activity('RECOVERED','recover')
          local r=req('READ','after');assert(r.phase=='TASK_RUNNING' and r.taskStart==83 and r.taskDue==85)
          assert(not r.recovering and r.activityMode=='ASLEEP')
          currentTurn=85;ownTurn(2);r=req('READ','complete');assert(r.taskCompletions==1 and r.taskCompleted==85)
        """)

    def test_running_unexpected_awake_holds_without_fabricated_completion(self):
        lua = fixture()
        lua.execute("""
          running();currentTurn=85;restart();activity('RECOVERED','recover',{Sleeping=false,Awake=true})
          ownTurn(2);local r=req('READ','after');assert(r.phase=='HELD' and r.stop=='ACTIVITY_UNEXPECTED_WAKE')
          assert(r.taskCompletions==0 and not r.taskCompleted and destroys==0);noNativeSideEffects()
        """)

    def test_due_record_cannot_complete_on_read_foreign_turn_or_before_recovery(self):
        lua = fixture()
        lua.execute("""
          running();currentTurn=85;restart();ownTurn(2);ownTurn(3)
          assert(req('READ','before').taskCompletions==0)
          activity('RECOVERED','recover');ownTurn(3);assert(req('READ','still').taskCompletions==0)
          ownTurn(2);ownTurn(2);assert(req('READ','done').taskCompletions==1)
        """)

    def test_stale_unknown_or_native_mission_recovery_cannot_resume(self):
        for override in ("SampleTurn=82", "Sleeping=false,Awake=false", "Sleeping=true,Awake=true", "NativeOperation=9"):
            with self.subTest(override=override):
                lua = fixture()
                lua.execute("running();restart();local r=activity('RECOVERED','bad',{" + override + "});assert(r.error and r.phase=='HELD' and not r.recovering and r.activityMode=='RELEASE');currentTurn=85;ownTurn(2);assert(req('READ','after').taskCompletions==0);noNativeSideEffects()")

    def test_failed_recovery_consumes_observation_and_exposes_owned_release(self):
        lua = fixture()
        lua.execute("""
          running();restart();activity('FAILED','failure',{Detail='ACTIVITY_RECOVERY_STATE_UNKNOWN'})
          local r=req('READ','held');assert(r.phase=='HELD' and not r.recovering and r.activityMode=='RELEASE')
          assert(ExposedMembers.SPC_ExpeditionActivity.mode=='RELEASE' and saved().state.activityMode=='RELEASE')
          assert(r.taskDue==85 and r.taskCompletions==0 and not r.taskCompleted);noNativeSideEffects()
        """)

    def test_source_loss_before_recovery_ack_exposes_owned_release(self):
        lua = fixture()
        lua.execute("""
          running();restart();city.token=nil;ownTurn(2)
          local r=req('READ','held');assert(r.phase=='HELD' and not r.recovering and r.activityMode=='RELEASE')
          assert(r.stop=='SOURCE_REFERENCE_CHANGED' and r.taskCompletions==0 and not r.taskCompleted)
          assert(ExposedMembers.SPC_ExpeditionActivity.mode=='RELEASE');noNativeSideEffects()
        """)

    def test_wrong_activity_key_cannot_resume_loaded_task(self):
        lua = fixture()
        lua.execute("running();restart();local r=activity('RECOVERED','bad',{ActivityKey='old-session-task'});assert(r.error=='ACTIVITY_REFERENCE_CHANGED');assert(req('READ','after').recovering and saved().state.phase=='TASK_RUNNING')")

    def test_owned_sleep_release_is_reconstructed_without_repeating_completion(self):
        lua = fixture()
        lua.execute("""
          running();currentTurn=85;ownTurn(2);assert(saved().state.activityMode=='RELEASE');restart()
          activity('RECOVERED','recover');local r=req('READ','before')
          assert(r.phase=='TASK_COMPLETE' and r.taskCompletions==1 and r.activityMode=='RELEASE')
          activity('RELEASED','release');restart();r=req('READ','after')
          -- B212: release returns the team to the target centre, ready for another mission.
          assert(r.phase=='ARRIVED' and r.activityMode==nil and not r.recovering and insightWrites==1)
        """)

    def test_release_already_awake_clears_lease_without_new_native_request(self):
        lua = fixture()
        lua.execute("""
          running();currentTurn=85;ownTurn(2);restart()
          activity('RECOVERED','recover',{Sleeping=false,Awake=true})
          local r=req('READ','after');assert(r.phase=='ARRIVED' and r.activityMode==nil and not r.activityOwned)
          assert(saved().state.phase=='ARRIVED' and insightWrites==1);noNativeSideEffects()
        """)

    def test_previous_generation_activity_reply_cannot_start_replacement_team(self):
        lua = fixture()
        lua.execute("""
          ready();prepare();local oldKey=ExposedMembers.SPC_ExpeditionActivity.activityKey
          req('END','end',41);restart();currentTurn=81;ready();prepare()
          local newKey=ExposedMembers.SPC_ExpeditionActivity.activityKey;assert(newKey~=oldKey)
          local r=activity('ARMED','oldreply',{ActivityKey=oldKey})
          assert(r.error=='ACTIVITY_REFERENCE_CHANGED' and saved().state.activityMode=='SLEEP')
          assert(not saved().state.taskStart and saved().generation==2)
        """)


class SourcePreflight(unittest.TestCase):
    def test_invalid_reference_before_reservation_never_spawns(self):
        for ref in ("nil", "''", "string.rep('x',2049)"):
            with self.subTest(reference=ref):
                lua = fixture()
                lua.execute("SPCNetworkInput.Reference=function()return " + ref + " end;local r=create();assert(r.error=='SOURCE_REFERENCE_UNKNOWN' and initCalls==0 and storeWrites==0 and not saved());noNativeSideEffects()")

    def test_occupancy_reader_source_mutation_never_reserves_or_spawns(self):
        for change in ("city.token=nil", "city.token='replacement'", "city.owner=3", "city.id=9", "city.x=2"):
            with self.subTest(change=change):
                lua = fixture()
                lua.execute("local read=Units.GetUnitsInPlot;Units.GetUnitsInPlot=function(...)local out=read(...);" + change + ";return out end;local r=create();assert(r.error=='SOURCE_REFERENCE_CHANGED' and initCalls==0 and storeWrites==0 and not saved());noNativeSideEffects()")

    def test_reservation_callback_source_mutation_holds_without_spawning(self):
        for change in ("city.token=nil", "city.token='replacement'", "city.owner=3", "city.id=9", "city.x=2"):
            with self.subTest(change=change):
                lua = fixture()
                lua.execute("""
                  local write=P.SetProperty
                  P.SetProperty=function(object,key,value)
                   local result=write(object,key,value)
                   if value.state.phase=='CREATING' then SOURCE_MUTATION end
                   return result
                  end
                  local r=create();assert(r.phase=='HELD' and r.error=='SOURCE_REFERENCE_CHANGED' and initCalls==0)
                  assert(saved().state.phase=='HELD' and saved().state.sourceRef and r.reservedCapacity)
                  denyRespawn('duplicate');restart();r=req('READ','cold')
                  assert(r.phase=='HELD' and r.reservedCapacity and initCalls==0 and destroys==0);noNativeSideEffects()
                """.replace('SOURCE_MUTATION',change))

    def test_exact_city_lookup_alias_is_rejected_before_native_creation(self):
        lua = fixture()
        lua.execute("city.id=9;local r=create();assert(r.error=='OWN_CITY_REQUIRED' and initCalls==0 and storeWrites==0 and not saved());noNativeSideEffects()")


class StoreFailureBoundaries(unittest.TestCase):
    def test_reservation_write_failure_prevents_init_and_retry(self):
        for fault in ("storeNoop=true", "storeThrowBefore=true", "storeThird=true", "storeMalformed=true", "storeReadError=true"):
            with self.subTest(fault=fault):
                lua = fixture()
                lua.execute(fault + ";create();local r=req('READ','after');assert(r.phase=='HELD' and r.count==1 and r.reservedCapacity);denyRespawn('duplicate');assert(initCalls==0 and destroys==0);noNativeSideEffects()")

    def test_failed_postspawn_write_retains_exact_survivor_and_reservation(self):
        lua = fixture()
        lua.execute("""
          local oldInit=UnitManager.InitUnit
          UnitManager.InitUnit=function(...)local u=oldInit(...);storeNoop=true;return u end
          create();local r=req('READ','after');assert(r.phase=='HELD' and r.persistence=='UNAVAILABLE' and units[40])
          denyRespawn('duplicate');assert(initCalls==1 and destroys==0)
          storeNoop=false;restart();r=req('READ','cold');assert(r.phase=='HELD' and r.reservedCapacity)
          denyRespawn('aftercold');assert(initCalls==1)
        """)

    def test_unconfirmed_dispatch_write_never_grants_native_permit(self):
        lua = fixture()
        lua.execute("create();storeNoop=true;local r=nativeDispatch('dispatch');assert(r.phase=='HELD' and not r.nativePermit);denyRespawn('duplicate');assert(saved().state.phase=='CREATED' and initCalls==1);noNativeSideEffects()")

    def test_arrival_write_failure_holds_and_does_not_publish_bound_success(self):
        lua = fixture()
        lua.execute("create();nativeDispatch('dispatch');storeNoop=true;local r=arrive();assert(r.phase=='HELD' and not r.bound and r.persistence=='UNAVAILABLE' and units[41]);denyRespawn('duplicate');assert(initCalls==1 and saved().state.unitID==40 and destroys==0)")

    def test_end_intent_failure_prevents_destroy(self):
        lua = fixture()
        lua.execute("create();storeNoop=true;req('END','end',40);local r=req('READ','after');assert(r.phase=='HELD' and units[40] and destroys==0);denyRespawn('duplicate');assert(initCalls==1)")

    def test_failed_end_tombstone_keeps_no_unit_reservation_on_reload(self):
        lua = fixture()
        lua.execute("""
          create();local us=Players[2]:GetUnits();local oldDestroy=us.Destroy
          us.Destroy=function(self,u)oldDestroy(self,u);storeNoop=true end
          req('END','end',40);assert(not units[40] and destroys==1 and saved().state.phase=='ENDING')
          storeNoop=false;restart();local r=req('READ','after')
          assert(r.phase=='HELD' and r.observedCount==0 and r.count==1 and r.reservedCapacity)
          denyRespawn('duplicate');assert(initCalls==1 and destroys==1)
        """)

    def test_write_exception_after_exact_readback_is_success_not_second_spawn(self):
        lua = fixture()
        lua.execute("storeThrowAfter=true;local r=create();assert(r.phase=='CREATED' and r.bound and not r.error);restart();r=req('READ','after');assert(r.phase=='CREATED' and r.bound and initCalls==1);denyRespawn('duplicate')")

    def test_corrupt_or_unreadable_offmap_record_is_not_absence(self):
        for change in ("gameProperties.SPC_EXPEDITION_TEAM_P2='corrupt'", "storeReadError=true"):
            with self.subTest(change=change):
                lua = fixture()
                lua.execute("create();nativeDispatch('dispatch');units[40]=nil;" + change + ";restart();local r=req('READ','after');assert(r.phase=='HELD' and r.persistence=='UNAVAILABLE' and r.count==1 and r.reservedCapacity and not r.unitID);denyRespawn('duplicate');assert(initCalls==1 and destroys==0)")

    def test_third_or_malformed_readback_retains_reservation_without_known_unit(self):
        for fault in ("storeThird=true", "storeMalformed=true"):
            with self.subTest(fault=fault):
                lua = fixture()
                lua.execute("create();nativeDispatch('dispatch');units[40]=nil;" + fault + ";currentTurn=85;ownTurn(2);local r=req('READ','after');assert(r.phase=='HELD' and r.persistence=='UNAVAILABLE' and r.count==1 and r.reservedCapacity and not r.unitID);denyRespawn('duplicate');assert(initCalls==1)")

    def test_stale_external_write_is_not_overwritten(self):
        lua = fixture()
        lua.execute("""
          create();saved().revision=saved().revision+1;local external=copy(saved())
          local writes=storeWrites;local r=nativeDispatch('dispatch')
          assert(r.phase=='HELD' and r.error=='STORE_STALE_EXPECTED' and not r.nativePermit)
          assert(storeWrites==writes and saved().revision==external.revision and saved().state.phase=='CREATED')
        """)

    def test_postspawn_unreadable_readback_holds_and_preserves_uncertain_unit(self):
        lua = fixture()
        lua.execute("""
          local oldWrite=P.SetProperty
          P.SetProperty=function(object,key,value)
           local out=oldWrite(object,key,value)
           if storeWrites==2 then storeReadError=true end
           return out
          end
          create();local r=req('READ','after')
          assert(r.phase=='HELD' and r.persistence=='UNAVAILABLE' and units[40] and initCalls==1)
          denyRespawn('duplicate');restart();r=req('READ','cold')
          assert(r.phase=='HELD' and r.count==1 and r.reservedCapacity and destroys==0)
        """)


class LifecycleAndIsolation(unittest.TestCase):
    def test_unchanged_reads_turns_and_notifications_do_not_write_properties(self):
        lua = fixture()
        lua.execute("""
          create();local n=storeWrites
          for i=1,5 do req('READ','read'..i);ownTurn(2);transfer()end
          assert(storeWrites==n);nativeDispatch('dispatch');units[40]=nil;currentTurn=82;n=storeWrites
          for i=1,5 do req('READ','travel'..i);ownTurn(2);removed(2,40)end
          assert(storeWrites==n and initCalls==1)
        """)

    def test_duplicate_start_completion_and_release_write_once_per_transition(self):
        lua = fixture()
        lua.execute("""
          running();local n=storeWrites;activity('ASLEEP','asleep');assert(storeWrites==n)
          currentTurn=85;ownTurn(2);n=storeWrites
          ownTurn(2);ownTurn(2);req('READ','complete');assert(storeWrites==n and saved().state.taskCompletions==1)
          activity('RELEASED','release');n=storeWrites;activity('RELEASED','release')
          assert(storeWrites==n and saved().state.phase=='ARRIVED' and saved().state.activityMode==nil and insightWrites==1)
        """)

    def test_source_active_or_identity_decline_survives_reload_and_completion(self):
        lua = fixture()
        lua.execute("running();active=1;spec='REALLOCATING';restart();activity('RECOVERED','recover');currentTurn=85;ownTurn(2);local r=req('READ','after');assert(r.phase=='TASK_COMPLETE' and r.bound and r.sourceCity==1 and r.taskCompletions==1 and destroys==0)")

    def test_source_loss_or_unknown_holds_retains_team_and_never_reattaches(self):
        for change in ("city.owner=3", "city.token=nil", "city.token='replacement'", "cities[1]=nil"):
            with self.subTest(change=change):
                lua = fixture()
                lua.execute("running();restart();" + change + ";transfer();currentTurn=85;ownTurn(2);local r=req('READ','after');assert(r.phase=='HELD' and not r.bound and r.sourceCity==1 and r.taskCompletions==0 and units[41] and destroys==0);denyRespawn('duplicate')")

    def test_target_change_at_loaded_task_cannot_complete(self):
        lua = fixture()
        lua.execute("running();restart();targetCity.owner=4;activity('RECOVERED','recover');currentTurn=85;ownTurn(2);local r=req('READ','after');assert(r.phase=='HELD' and r.taskCompletions==0 and units[41] and destroys==0)")

    def test_other_units_other_player_properties_and_city_record_are_unchanged(self):
        lua = fixture()
        lua.execute("""
          units[9]=unit(9,103,2,7,9);units[10]=unit(10,101,2,3,4)
          foreignUnits[7]=unit(7,103,3,15,8);gameProperties.UNRELATED={value=9}
          gameProperties.SPC_EXPEDITION_TEAM_P3={unrelated='preserved'}
          running();restart();activity('RECOVERED','recover');currentTurn=85;ownTurn(2)
          activity('RELEASED','release');req('END','end',41)
          assert(units[9].x==7 and units[9].y==9 and units[10].x==3 and foreignUnits[7].owner==3)
          assert(gameProperties.UNRELATED.value==9 and gameProperties.SPC_EXPEDITION_TEAM_P3.unrelated=='preserved')
          assert(city.token=='source-token' and destroys==1);noNativeSideEffects()
        """)


if __name__ == '__main__':
    unittest.main()
