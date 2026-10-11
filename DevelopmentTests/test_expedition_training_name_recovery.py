"""B203 actual background name observer; native event timing remains unproved."""
import unittest
from test_expedition_training_ui import naming
from test_expedition_spy_task import gate, ui

class Recovery(unittest.TestCase):
 def run_case(self,code):
  l=naming();l.execute(code);return l
 def test_delayed_readiness_retry_on_selection_without_panel(self):
  self.run_case("mirror();nameStatus='PENDING';hooks.GameCoreEventPublishComplete();update(.25);update(10);nameStatus='READY';hooks.GameCoreEventPublishComplete();assert(update==nil);nameSelection(2,50);update(.25);assert(calls==1)")
 def test_turn_retry_budget_and_event_burst_bounded(self):
  self.run_case("mirror();nameStatus='PENDING';hooks.GameCoreEventPublishComplete();for n=1,3 do update(10);for k=1,100 do hooks.GameCoreEventPublishComplete()end;if n<3 then nameTurn()end end;for k=1,100 do nameTurn();nameSelection(2,50)end;assert(update==nil and calls==0 and ExposedMembers.SPC_ExpeditionTrainingNameStatus.attempts==3 and ExposedMembers.SPC_ExpeditionTrainingNameStatus.status=='STOPPED')")
 def test_wrong_selection_cannot_retry(self):
  self.run_case("mirror();nameStatus='PENDING';hooks.GameCoreEventPublishComplete();update(10);nameSelection(3,50);nameSelection(2,51);selectedID=51;nameSelection(2,50);assert(update==nil)")
 def test_lost_ack_does_not_resend(self):
  self.run_case("mirror();hooks.GameCoreEventPublishComplete();update(.25);update(10);for k=1,100 do nameTurn();hooks.GameCoreEventPublishComplete()end;assert(calls==1 and update==nil and ExposedMembers.SPC_ExpeditionTrainingNameError=='TRAINING_NAME_ACK_UNCONFIRMED')")
 def test_late_authoritative_success_clears_error(self):
  self.run_case("mirror();hooks.GameCoreEventPublishComplete();update(.25);update(10);local v=ExposedMembers.SPC_ExpeditionActivity;v.phase='CREATED';v.expectedName=lastName.Name;hooks.GameCoreEventPublishComplete();assert(calls==1 and ExposedMembers.SPC_ExpeditionTrainingNameStatus.status=='READY' and ExposedMembers.SPC_ExpeditionTrainingNameError==nil)")
 def test_wrong_ack_owner_ignored(self):
  self.run_case("mirror();hooks.GameCoreEventPublishComplete();update(.25);ExposedMembers.SPC_ExpeditionGateReply={owner=3,token=lastName.Token,error='wrong'};update(.25);assert(update~=nil and ExposedMembers.SPC_ExpeditionTrainingNameError==nil)")
 def test_ack_without_authoritative_transition_is_not_success(self):
  self.run_case("mirror();hooks.GameCoreEventPublishComplete();update(.25);ExposedMembers.SPC_ExpeditionGateReply={owner=2,token=lastName.Token,phase='CREATED'};update(10);assert(ExposedMembers.SPC_ExpeditionTrainingNameStatus.status=='STOPPED')")
 def test_invalid_identity_terminal_not_retried(self):
  self.run_case("mirror();nameStatus='INVALID';hooks.GameCoreEventPublishComplete();update(.25);nameStatus='READY';nameTurn();nameSelection(2,50);assert(calls==0 and update==nil)")
 def test_send_exception_uncertain_no_replay(self):
  self.run_case("mirror();UI.RequestPlayerOperation=function()calls=calls+1;error('uncertain')end;hooks.GameCoreEventPublishComplete();update(.25);nameTurn();assert(calls==1 and update==nil and ExposedMembers.SPC_ExpeditionTrainingNameError=='TRAINING_NAME_SEND_UNCONFIRMED')")
 def test_reader_reentrancy_never_sends_for_changed_team(self):
  self.run_case("mirror();SPCExpeditionSpyRead.NativeName=function()ExposedMembers.SPC_ExpeditionActivity.unitID=51;return {status='READY',name='X'}end;hooks.GameCoreEventPublishComplete();update(.25);assert(calls==0 and update==nil)")
 def test_reader_exception_terminal(self):
  self.run_case("mirror();SPCExpeditionSpyRead.NativeName=function()error('read')end;hooks.GameCoreEventPublishComplete();update(.25);assert(calls==0 and ExposedMembers.SPC_ExpeditionTrainingNameError=='TRAINING_NAME_READ_ERROR')")
 def test_new_generation_gets_own_bounded_observer(self):
  self.run_case("mirror();nameStatus='INVALID';hooks.GameCoreEventPublishComplete();update(.25);ExposedMembers.SPC_ExpeditionActivity.teamKey='new';nameStatus='READY';hooks.GameCoreEventPublishComplete();update(.25);assert(calls==1 and ExposedMembers.SPC_ExpeditionTrainingNameStatus.attempts==1)")
 def test_shutdown_cancels_pending_callback(self):
  self.run_case("mirror();hooks.GameCoreEventPublishComplete();local cb=update;shutdown();cb(.25);assert(calls==0 and update==nil and ExposedMembers.SPC_ExpeditionTrainingNameStatus==nil)")
 def test_load_naming_can_confirm_without_panel(self):
  self.run_case("adapter.Before(city,{Type=kind},false);adapter.Pulse();adapter.Pulse();born();entries={};complete();pulse();SPCExpeditionSpyGate.Start(P,shared);shared.ExpeditionGate.Turn(2);direct=true;nameTurn();update(.25);assert(state().phase=='CREATED' and state().nameVerified and state().sourceCity==1)")
 def test_late_ready_gets_separate_ack_window(self):
  self.run_case("mirror();nameStatus='PENDING';hooks.GameCoreEventPublishComplete();update(9);nameStatus='READY';update(.25);update(1);assert(update~=nil and calls==1);update(9);assert(update==nil)")
 def test_wrong_name_transition_is_not_confirmation(self):
  self.run_case("mirror();hooks.GameCoreEventPublishComplete();update(.25);ExposedMembers.SPC_ExpeditionActivity.phase='CREATED';ExposedMembers.SPC_ExpeditionActivity.expectedName='wrong';update(.25);assert(ExposedMembers.SPC_ExpeditionTrainingNameStatus.status~='READY')")
 def test_duplicate_notifications_do_not_restart_live_job(self):
  self.run_case("mirror();nameStatus='PENDING';hooks.GameCoreEventPublishComplete();for k=1,100 do nameTurn();nameSelection(2,50);hooks.GameCoreEventPublishComplete()end;assert(ExposedMembers.SPC_ExpeditionTrainingNameStatus.attempts==1 and calls==0);nameStatus='READY';update(.25);for k=1,100 do nameTurn()end;assert(calls==1)")
 def test_source_change_before_confirmation_still_holds(self):
  self.run_case("adapter.Before(city,{Type=kind},false);adapter.Pulse();adapter.Pulse();born();entries={};complete();pulse();city.token='changed';direct=true;hooks.GameCoreEventPublishComplete();update(.25);assert(state().phase=='HELD' and not state().nameVerified)")

class Presentation(unittest.TestCase):
 def test_trained_read_does_not_submit_name(self):
  l=gate(ui=True,window=True)
  l.execute("""
   shared.ExpeditionGate.Training.Reserve(2,1,'train');units[40]=unit(40,100,2,1,1)
   shared.ExpeditionGate.Training.Evidence(2,'train','trainingQueued',true)
   shared.ExpeditionGate.Training.Evidence(2,'train','trainingBorn',40)
   shared.ExpeditionGate.Training.Evidence(2,'train','trainingCompleted',true)
   shared.ExpeditionGate.Training.Finish(2,'train')
   gateOpen();assert(ExposedMembers.SPC_ExpeditionGateReply.trainingToken=='train')
   assert(ExposedMembers.SPC_ExpeditionActivity.phase=='NAMING' and nameConfirmCalls==0)
   assert(Controls.Report.text:find('TRAINED_COUNT'))
  """)
 def test_pending_and_error_tooltips_exact_team_only(self):
  l=ui('UnitPanel');l.execute("""
   phase('NAMING');local v=ExposedMembers.SPC_ExpeditionActivity;v.trainingToken='r'
   assert(SPCExpeditionSpyUI.UnavailableText(team):find('NAME_PENDING'))
   ExposedMembers.SPC_ExpeditionTrainingNameStatus={owner=2,unitID=40,teamKey=v.teamKey,status='STOPPED',reason='TEST'}
   assert(SPCExpeditionSpyUI.UnavailableText(team):find('NAME_STOPPED'))
   ExposedMembers.SPC_ExpeditionTrainingNameStatus.unitID=99
   assert(SPCExpeditionSpyUI.UnavailableText(team):find('NAME_PENDING'))
   assert(not SPCExpeditionSpyUI.CanOpen('TRAVEL',team))
  """)
if __name__=='__main__':unittest.main()
