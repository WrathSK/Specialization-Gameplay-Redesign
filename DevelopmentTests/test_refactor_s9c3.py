"""Player ACK consumer: real reply transport, fake UI, and real Crew integration."""
import json,unittest
from refactor_harness import ROOT,Context,legacy_source_observation,measure
from test_refactor_s6h import ui,SETUP
from test_refactor_s7d5 import fixture as crew
from test_refactor_s5d4b2 import load_request


class Consumer(unittest.TestCase):
 def test_player_packets_use_channel_and_DEV_matching_token_cannot_complete_them(self):
  c=ui();c.execute("autoReply=false;Controls.PrepareButton.click();local p=requests[#requests];assert(p.ReplyChannel=='UNIT_ACTION'and p.ReplyEpoch==ExposedMembers.SPC_P0.PlayerActionReplies.epoch);ExposedMembers.SPC_P0.LastToken=p.Token;ExposedMembers.SPC_P0.Snapshot='SPOOFED_DEV';publish();assert(Controls.ConfirmButton.hide and ExposedMembers.SPC_UnitPanelStatus~='SPOOFED_DEV');deliver();deliver();assert(not Controls.ConfirmButton.hide and ExposedMembers.SPC_UnitPanelStatus=='PREPARED')")
 def test_real_terminal_survives_another_DEV_report_and_is_consumed_once(self):
  c=ui();c.execute("Controls.PrepareButton.click();local d=ExposedMembers.SPC_P0.PlayerActionReplies;assert(d.Count()==1);ExposedMembers.SPC_P0.LastToken='DEV';ExposedMembers.SPC_P0.Snapshot='OTHER';publish();assert(ExposedMembers.SPC_UnitPanelStatus=='PREPARED'and d.Count()==0);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")
 def test_selection_change_preserves_receipt_link_but_never_grants_new_unit_confirmation(self):
  c=ui();c.execute("autoReply=false;Controls.PrepareButton.click();local id=selected.id;selected=units[8];selectedChanged();deliver();assert(ExposedMembers.SPC_UnitPanelStatus=='PREPARED'and Controls.ConfirmButton.hide);Controls.ConfirmButton.click();assert(actionCount('UNIT_ACTION_CONFIRM')==0 and ExposedMembers.SPC_P0.PlayerActionReplies.Count()==0)")
 def test_wrong_terminal_metadata_is_dropped_once_without_busy_refresh_or_resend(self):
  for change in ("r.owner=1","r.unitID=99","r.action='UNIT_ACTION_CONFIRM'","r.epoch=r.epoch+1","r.version='OLD'"):
   c=ui();c.execute("local d=ExposedMembers.SPC_P0.PlayerActionReplies;local take=d.Take;d.Take=function(...)local r=take(...);if r then "+change+" end;return r end;Controls.PrepareButton.click();publish();assert(ExposedMembers.SPC_UnitPanelStatus~='PREPARED'and d.Count()==0);resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0 and confirmed==0)")
 def test_backend_replacement_during_Take_cannot_display_stale_success(self):
  c=ui();c.execute("local d=ExposedMembers.SPC_P0.PlayerActionReplies;local take=d.Take;d.Take=function(...)local r=take(...);SPCPlayerActionReplies.Start(P,ExposedMembers.SPC_P0);return r end;Controls.PrepareButton.click();publish();assert(ExposedMembers.SPC_UnitPanelStatus~='PREPARED'and confirmed==0);resetCounts();idle(1000);assert(counts.requests==0)")
 def test_ring_eviction_and_late_reply_remain_unknown_and_do_not_repeat_actions(self):
  c=ui();c.execute("Controls.PrepareButton.click();local d=ExposedMembers.SPC_P0.PlayerActionReplies;for i=1,8 do assert(d.Publish(0,{ReplyChannel='UNIT_ACTION',ReplyEpoch=d.epoch,Token='OTHER'..i,Action='UNIT_ACTION_PREPARE',UnitID=8},'OTHER'))end;publish();tick(11);publish();assert(actionCount('UNIT_ACTION_PREPARE')==1 and actionCount('UNIT_ACTION_CONFIRM')==0 and plan=='PLAN');resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")
  c=ui();c.execute("autoReply=false;Controls.PrepareButton.click();tick(11);publish();deliver();assert(actionCount('UNIT_ACTION_PREPARE')==1 and actionCount('UNIT_ACTION_CONFIRM')==0)")
 def test_pending_discard_on_shutdown_does_not_close_shared_service(self):
  c=ui();c.execute("Controls.PrepareButton.click();local d=ExposedMembers.SPC_P0.PlayerActionReplies;assert(d.Count()==1);shutdown();assert(d.Count()==0);assert(d.Publish(0,{ReplyChannel='UNIT_ACTION',ReplyEpoch=d.epoch,Token='NEW',Action='UNIT_ACTION_PREPARE',UnitID=8},'OK'));local n=counts.requests;publish();assert(counts.requests==n and d.Count()==1)")
 def test_old_send_failure_cannot_discard_a_newer_confirm_terminal(self):
  c=ui();c.execute("duringRequest=function(p)if p.Action=='UNIT_ACTION_PREPARE'then duringRequest=nil;publish();Controls.ConfirmButton.click();innerToken=requests[#requests].Token;error('OLD_PREPARE_STACK_FAILED')end end;Controls.PrepareButton.click();local d=ExposedMembers.SPC_P0.PlayerActionReplies;assert(confirmed==1 and d.Has(0,innerToken));publish();assert(ExposedMembers.SPC_UnitPanelStatus=='DONE'and not d.Has(0,innerToken)and actionCount('UNIT_ACTION_CONFIRM')==1)")
 def test_shutdown_during_synchronous_send_cannot_resume_or_resend_old_attempt(self):
  c=ui();c.execute("duringRequest=function(p)if p.Action=='UNIT_ACTION_PREPARE'then duringRequest=nil;shutdown();error('CLOSED_SEND')end end;Controls.PrepareButton.click();assert(actionCount('UNIT_ACTION_PREPARE')==1 and actionCount('UNIT_ACTION_CONFIRM')==0);local n=counts.requests;publish();assert(counts.requests==n)")
 def test_missing_result_service_does_not_fall_back_to_DEV_or_send(self):
  c=ui();c.execute("ExposedMembers.SPC_P0.PlayerActionReplies=nil;local n=counts.requests;Controls.PrepareButton.click();assert(counts.requests==n and confirmed==0 and plan==nil)")


def real_panel():
 v=crew();v.globals().include('SafeCallbacks');v.globals().include('PlayerActionReplies')
 controls=SETUP[SETUP.index('parent={'):SETUP.index('PlayersVisibility=')]
 v.execute("counts={layout=0};P.VERSION='PANEL_TEST';P.Scalar=tostring;P.Field=function(t,k)return t and t[k]end;P.Observe=function()end;shared.Version=P.VERSION;ExposedMembers.SPC_P0=shared;SPCPlayerActionReplies.Start(P,shared);Game.GetLocalPlayer=function()return 0 end;mode=1;Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=1};InterfaceModeTypes={SELECTION=1};Locale={Lookup=function(k)return k end};GameInfo.Units={[u:GetType()]={UnitType='UNIT_SPC_CREW_250'}};selectedID=20001;requests={};stage=function()end")
 v.execute(controls)
 ctx=Context();v.execute(ctx.fragment('Mod/Gameplay.lua','local function refreshInvestmentSupport(', 'local function request(playerID,params)')+'\n_G.refreshInvestmentSupport=refreshInvestmentSupport');load_request(v)
 v.execute("""
 UI={GetHeadSelectedUnit=function()return C.units[selectedID]end,GetInterfaceMode=function()return mode end,
 RequestPlayerOperation=function(pid,op,p)requests[#requests+1]=p;return rawRequest(pid,p)end}
 local units=Players[0]:GetUnits();local destroy=units.Destroy
 local get=Players[0].GetUnits;Players[0].GetUnits=function(...)
  local collection=get(...);collection.Destroy=function(self,unit)
   local id=unit:GetID();local result=destroy(self,unit)
   Events.UnitRemovedFromMap.Fire(0,id);Events.UnitSelectionChanged.Fire(0,id)
   return result
  end;return collection
 end
 function publishPanel()Events.GameCoreEventPublishComplete.Fire()end
 function actionCount(kind)local n=0;for _,p in ipairs(requests)do if p.Action==kind then n=n+1 end end;return n end
 """)
 v.globals().include=lambda name:None # Probe is already represented by this fixture's explicit P
 v.execute('SPCP0=P')
 with legacy_source_observation():v.execute((ROOT/'Mod/UI/UnitPanelActions.lua').read_text())
 v.execute('init()');return v


class Integration(unittest.TestCase):
 def test_actual_Crew_destroy_events_before_ACK_keep_terminal_and_never_read_it_as_new_preview(self):
  v=real_panel();v.execute("Controls.PrepareButton.click();publishPanel();assert(not Controls.ConfirmButton.hide);Controls.ConfirmButton.click();assert(C.units[20001]==nil);publishPanel();assert(ExposedMembers.SPC_UnitPanelStatus:find('CREW CONSUMED',1,true)and shared.PlayerActionReplies.Count()==0 and #c:GetBuildQueue().adds==1);local n=#requests;for i=1,1000 do publishPanel()end;assert(#requests==n and actionCount('UNIT_ACTION_CONFIRM')==1 and #c:GetBuildQueue().adds==1)")
  measure('S9c3_actual_Crew_UI',{'native_removal_and_selection_before_terminal':True,'typed_result_consumed':True,'grant_calls':1,'thousand_idle_extra_requests':0,'DEV_ACK_used':False})
 def test_actual_ambiguous_grant_remains_HELD_without_UI_replay(self):
  v=real_panel();v.execute("Controls.PrepareButton.click();publishPanel();local q=c:GetBuildQueue();q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;error('NATIVE_UNKNOWN')end;Controls.ConfirmButton.click();publishPanel();assert(C.units[20001]==nil and #q.adds==1 and shared.PlayerActionReplies.Count()==0 and ExposedMembers.SPC_UnitPanelStatus~=nil);for i=1,1000 do publishPanel()end;Controls.ConfirmButton.click();assert(actionCount('UNIT_ACTION_CONFIRM')==1 and #q.adds==1)")


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9c2'])])

if __name__=='__main__':unittest.main()
