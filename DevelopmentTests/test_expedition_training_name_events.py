"""B204 event-first delta with the actual reader/Gate/Store; native delivery remains a game gate."""
import unittest
from test_expedition_training_ui import naming, R
from test_expedition_spy_task import ui


def trained(initialize=True):
    l=naming(initialize=initialize)
    l.execute((R/'Mod/ExpeditionSpyRead.lua').read_text())
    l.execute('''
      local old=Players[2].GetDiplomacy
      Players[2].GetDiplomacy=function()
       local d=old();d.GetNumSpiesOffMap=function()if offmapUnavailable then return nil end;return 0 end;return d
      end
      adapter.Before(city,{Type=kind},false);adapter.Pulse();adapter.Pulse()
      born();entries={};complete();pulse();direct=true
      assert(state().phase=='NAMING' and state().sourceCity==1)
      local reader=SPCExpeditionSpyRead.NativeName;realReads=0
      SPCExpeditionSpyRead.NativeName=function(...)realReads=realReads+1;return reader(...)end
    ''')
    return l


class EventFirst(unittest.TestCase):
    def test_ready_confirmation_never_needs_frame_or_panel(self):
        l=trained();l.execute("hooks.GameCoreEventPublishComplete();assert(calls==1 and realReads==1 and update==nil and state().phase=='CREATED' and state().sourceCity==1 and state().nameVerified)")

    def test_real_pending_name_then_ready_publication_without_frames(self):
        l=trained();l.execute("""
          units[50].name='LOC_TEST_DEFAULT';hooks.GameCoreEventPublishComplete()
          local n=ExposedMembers.SPC_ExpeditionTrainingNameStatus
          assert(calls==0 and n.status=='PENDING' and n.reason=='TEAM_NATIVE_NAME_DEFAULT' and n.readAttempted)
          assert(not shared.ExpeditionGate.Training.Available(2))
          units[50].name='LOC_CITIZEN_TEST_A';hooks.GameCoreEventPublishComplete()
          assert(calls==1 and realReads==2 and update==nil and state().phase=='CREATED')
        """)

    def test_pending_rechecks_on_each_existing_explicit_wakeup(self):
        for event in ['nameTurn()','nameSelection(2,50)','hooks.LoadScreenClose()']:
            with self.subTest(event=event):
                l=trained();l.execute("units[50].name='LOC_TEST_DEFAULT';hooks.GameCoreEventPublishComplete();units[50].name='LOC_CITIZEN_TEST_A';"+event+";assert(calls==1 and state().phase=='CREATED' and update==nil)")

    def test_saved_naming_is_discovered_at_init_without_event_or_frame(self):
        l=trained(initialize=False);l.execute("assert(not ExposedMembers.SPC_ExpeditionTrainingNameStatus.initialized and calls==0);initializeName();initializeName();assert(calls==1 and state().phase=='CREATED' and update==nil)")

    def test_missing_offmap_information_has_exact_reason_and_no_submission(self):
        l=trained();l.execute("offmapUnavailable=true;hooks.GameCoreEventPublishComplete();assert(calls==0 and ExposedMembers.SPC_ExpeditionTrainingNameStatus.reason=='OFFMAP_NAME_COUNT_UNAVAILABLE');offmapUnavailable=false;hooks.GameCoreEventPublishComplete();assert(calls==1 and state().phase=='CREATED')")

    def test_collision_is_terminal_even_if_later_disappears(self):
        l=trained();l.execute("units[80]=unit(80,103,2,2,1);units[80].name='LOC_CITIZEN_TEST_A';hooks.GameCoreEventPublishComplete();assert(calls==0 and ExposedMembers.SPC_ExpeditionTrainingNameStatus.reason=='TEAM_NATIVE_NAME_DUPLICATE_VISIBLE');units[80]=nil;nameTurn();assert(calls==0 and state().phase=='NAMING' and not shared.ExpeditionGate.Training.Available(2))")

    def test_same_native_name_never_overrides_changed_source(self):
        l=trained();l.execute("city.token='replacement';hooks.GameCoreEventPublishComplete();assert(calls==1 and state().phase=='HELD' and not state().nameVerified and not shared.ExpeditionGate.Training.Available(2))")

    def test_ready_bursts_never_repeat_reads_or_writes(self):
        l=trained();l.execute("hooks.GameCoreEventPublishComplete();local writes=storeWrites;for n=1,100 do hooks.GameCoreEventPublishComplete();nameTurn();nameSelection(2,50)end;assert(calls==1 and realReads==1 and storeWrites==writes and update==nil)")

    def test_pending_bursts_keep_one_job_without_publication_spam(self):
        l=trained();l.execute("""
          units[50].name='LOC_TEST_DEFAULT';notices=0
          LuaEvents={SPC_ExpeditionActivityChanged=function()notices=notices+1 end}
          hooks.GameCoreEventPublishComplete();local first=update
          for n=1,100 do hooks.GameCoreEventPublishComplete()end
          assert(calls==0 and update==first and notices==2 and ExposedMembers.SPC_ExpeditionTrainingNameStatus.attempts==1)
          units[50].name='LOC_CITIZEN_TEST_A';hooks.GameCoreEventPublishComplete();assert(calls==1)
        """)

    def test_notification_reentry_cannot_duplicate_submission(self):
        l=trained();l.execute("LuaEvents={SPC_ExpeditionActivityChanged=function()hooks.GameCoreEventPublishComplete();nameSelection(2,50)end};hooks.GameCoreEventPublishComplete();assert(calls==1 and realReads==1 and state().phase=='CREATED')")

    def test_failed_feedback_does_not_abort_first_attempt(self):
        l=trained();l.execute("warnings=0;print=function(s)if s:find('TRAIN_NAME_FEEDBACK')then warnings=warnings+1 end end;LuaEvents={SPC_ExpeditionActivityChanged=function()error('presentation error')end};hooks.GameCoreEventPublishComplete();assert(calls==1 and warnings==1 and state().phase=='CREATED')")

    def test_shutdown_from_feedback_cannot_submit(self):
        l=trained();l.execute("LuaEvents={SPC_ExpeditionActivityChanged=function()shutdown()end};hooks.GameCoreEventPublishComplete();assert(calls==0 and realReads==0 and update==nil and ExposedMembers.SPC_ExpeditionTrainingNameStatus==nil)")

    def test_delayed_authoritative_ack_is_processed_by_event_without_frames(self):
        l=trained();l.execute("direct=false;hooks.GameCoreEventPublishComplete();assert(calls==1 and state().phase=='NAMING' and ExposedMembers.SPC_ExpeditionTrainingNameStatus.status=='CONFIRMING');shared.ExpeditionGate.Request(2,lastName);hooks.GameCoreEventPublishComplete();assert(calls==1 and state().phase=='CREATED' and update==nil and ExposedMembers.SPC_ExpeditionTrainingNameStatus.status=='READY')")

    def test_error_ack_on_event_stops_and_does_not_resend(self):
        l=trained();l.execute("direct=false;hooks.GameCoreEventPublishComplete();ExposedMembers.SPC_ExpeditionGateReply={owner=2,token=lastName.Token,error='NATIVE_ERROR'};hooks.GameCoreEventPublishComplete();for n=1,100 do nameTurn()end;assert(calls==1 and ExposedMembers.SPC_ExpeditionTrainingNameStatus.reason=='NATIVE_ERROR' and update==nil)")

    def test_explicit_false_send_is_uncertain_not_replayed(self):
        l=trained();l.execute("UI.RequestPlayerOperation=function()calls=calls+1;return false end;hooks.GameCoreEventPublishComplete();advanceName(10);nameTurn();assert(calls==1 and state().phase=='NAMING' and ExposedMembers.SPC_ExpeditionTrainingNameStatus.reason=='TRAINING_NAME_ACK_UNCONFIRMED')")

    def test_name_changed_during_feedback_is_rejected_by_unchanged_gate(self):
        l=trained();l.execute("LuaEvents={SPC_ExpeditionActivityChanged=function()if ExposedMembers.SPC_ExpeditionTrainingNameStatus.status=='CONFIRMING'then units[50].name='LOC_CITIZEN_TEST_B' end end};hooks.GameCoreEventPublishComplete();assert(calls==1 and state().phase=='HELD' and not state().nameVerified)")

    def test_old_callback_cannot_advance_a_replacement_job(self):
        l=trained();l.execute("units[50].name='LOC_TEST_DEFAULT';hooks.GameCoreEventPublishComplete();local old=update;ExposedMembers.SPC_ExpeditionActivity.teamKey='replacement';hooks.GameCoreEventPublishComplete();local reads=realReads;old(10);assert(realReads==reads and calls==0 and ExposedMembers.SPC_ExpeditionTrainingNameStatus.teamKey=='replacement')")

    def test_idle_diagnostic_is_bounded_and_has_no_timer(self):
        l=naming();l.execute("for n=1,100 do hooks.GameCoreEventPublishComplete()end;assert(ExposedMembers.SPC_ExpeditionTrainingNameStatus.status=='IDLE' and ExposedMembers.SPC_ExpeditionTrainingNameStatus.initialized and update==nil and calls==0)")


def feedback():
    l=ui('UnitPanel')
    # The old action fixture returns only the localization key. Preserve and
    # inspect arguments too, so stage and readable reason are both exercised.
    l.execute("Locale.Lookup=function(s,...)local out={s};for _,v in ipairs({...})do out[#out+1]=tostring(v)end;return table.concat(out,':')end")
    return l


class Feedback(unittest.TestCase):
    def test_each_stage_has_distinct_text_and_never_grants_permission(self):
        l=feedback();l.execute("""
          phase('NAMING');local v=ExposedMembers.SPC_ExpeditionActivity;v.trainingToken='r'
          assert(SPCExpeditionSpyUI.UnavailableText(team):find('NAME_NOT_STARTED'))
          ExposedMembers.SPC_ExpeditionTrainingNameStatus={initialized=true,status='IDLE'}
          assert(SPCExpeditionSpyUI.UnavailableText(team):find('NAME_NOT_OBSERVED'))
          for status,key in pairs({READING='NAME_READING',PENDING='NAME_PENDING',CONFIRMING='NAME_CONFIRMING',WAITING='NAME_RETRY_WAIT',STOPPED='NAME_STOPPED'})do
           ExposedMembers.SPC_ExpeditionTrainingNameStatus={initialized=true,owner=v.owner,unitID=v.unitID,teamKey=v.teamKey,trainingToken='r',status=status,reason='TEAM_NATIVE_NAME_DEFAULT'}
           local text=SPCExpeditionSpyUI.UnavailableText(team);assert(text:find(key))
           if status=='PENDING'then assert(text:find('NAME_REASON_UNASSIGNED'))end
           assert(not SPCExpeditionSpyUI.CanOpen('TRAVEL',team))
          end
        """)

    def test_stale_reservation_cannot_supply_current_status(self):
        l=feedback();l.execute("phase('NAMING');local v=ExposedMembers.SPC_ExpeditionActivity;v.trainingToken='new';ExposedMembers.SPC_ExpeditionTrainingNameStatus={initialized=true,owner=v.owner,unitID=v.unitID,teamKey=v.teamKey,trainingToken='old',status='CONFIRMING'};assert(SPCExpeditionSpyUI.UnavailableText(team):find('NAME_NOT_OBSERVED'))")

    def test_observer_error_is_distinct_from_absent_discovery(self):
        l=feedback();l.execute("phase('NAMING');ExposedMembers.SPC_ExpeditionActivity.trainingToken='r';ExposedMembers.SPC_ExpeditionTrainingNameStatus={initialized=true,status='ERROR',reason='TRAINING_NAME_OBSERVER_ERROR'};assert(SPCExpeditionSpyUI.UnavailableText(team):find('NAME_REASON_OBSERVER'))")

if __name__=='__main__':unittest.main()
