"""Actual B202 UI adapters: no simulated native PASS."""
from pathlib import Path
import unittest
from test_expedition_training import fixture
R=Path(__file__).resolve().parents[1]

def ui():
 l=fixture();l.execute('''
 Game.GetLocalPlayer=function()return 2 end;P.VERSION='test';UI={GetHeadSelectedCity=function()return selectedCity end};selectedCity=city
 PlayerOperations={EXECUTE_SCRIPT=1};CheckQueueItemSelected=function()return queueSelected end
 CityProductionDirectives={TRAIN=1};GameInfo.Units=info
 info[100].Index=100;info[100].Hash=100
 queue={GetSize=function()return #entries end,GetAt=function(self,i)return entries[i+1]end,
 GetUnitCost=function()return 60 end,GetUnitProgress=function()return 0 end,GetTurnsLeft=function()return 5 end,
 GetCurrentProductionTypeHash=function()return 0 end,CanProduce=function()return marker and nativeProduce~=false end}
 function city:GetBuildQueue()return queue end
 entries={};sentPackets={};builds=0;notifies=0
 function send(pid,op,p)sentPackets[#sentPackets+1]=p;if not deferred then shared.ExpeditionTraining.Request(pid,p)end end
 function build(c,item)builds=builds+1;if buildThrow then error('uncertain')end;entries={{Directive=1,UnitType=100}}end
 function notify()notifies=notifies+1;if notifyReenter then adapter.Sync(city)end end
 ''');l.execute((R/'Mod/UI/ExpeditionTrainingUI.lua').read_text());l.execute('adapter=SPCExpeditionTrainingUI.New(P,send,notify,build)');return l
class UI(unittest.TestCase):
 def check(self,s):ui().execute(s)
 def test_normal_admission_and_one_native_request(self):
  self.check("assert(not adapter.Before(city,{Type=kind},false));adapter.Pulse();adapter.Pulse();adapter.Pulse();assert(builds==1 and state().trainingQueued);adapter.Pulse();assert(builds==1)")
 def test_double_click_reserves_once(self):
  self.check("adapter.Before(city,{Type=kind},false);adapter.Before(city,{Type=kind},false);assert(#sentPackets==1)")
 def test_other_unit_unaffected(self):self.check("assert(adapter.Before(city,{Type='UNIT_SPY'},false));assert(#sentPackets==0)")
 def test_native_queue_edit_mode_no_training(self):self.check("assert(not adapter.Before(city,{Type=kind},true));assert(#sentPackets==0)")
 def test_selected_city_changed_cancels_before_order(self):
  self.check("adapter.Before(city,{Type=kind},false);selectedCity=nil;adapter.Pulse();adapter.Pulse();assert(builds==0 and state().phase=='ENDED' and not marker)")
 def test_native_denial_does_not_build(self):
  self.check("nativeProduce=false;adapter.Before(city,{Type=kind},false);adapter.Pulse();adapter.Pulse();assert(builds==0 and not marker)")
 def test_native_throw_never_resends(self):
  self.check("buildThrow=true;adapter.Before(city,{Type=kind},false);adapter.Pulse();adapter.Pulse();assert(builds==1 and state().phase=='TRAINING')")
 def test_explicit_queue_removal_releases_reservation(self):
  self.check("adapter.Before(city,{Type=kind},false);adapter.Pulse();adapter.Pulse();adapter.CancelQueue(city,0);entries={};adapter.Pulse();adapter.Pulse();assert(state().phase=='ENDED' and not marker)")
 def test_refresh_reentry_does_not_repeat_sync(self):
  self.check("notifyReenter=true;adapter.Sync(city);adapter.Pulse();assert(#sentPackets==1 and notifies==1)")
 def test_eligible_entry_uses_native_cost_and_unrelated_preserved(self):
  self.check("adapter.Sync(city);adapter.Pulse();local d={City=city,UnitItems={{Type='UNIT_SPY'}}};adapter.Items(d);assert(#d.UnitItems==2 and d.UnitItems[1].Type=='UNIT_SPY' and d.UnitItems[2].Cost==60)")
 def test_ineligible_entry_hidden(self):
  self.check("active=3;adapter.Sync(city);adapter.Pulse();local d={City=city,UnitItems={{Type=kind}}};adapter.Items(d);assert(#d.UnitItems==0)")
 def test_stale_ack_never_builds(self):
  self.check("deferred=true;adapter.Before(city,{Type=kind},false);ExposedMembers.SPC_ExpeditionTrainingReply={token='old',reserved=true};adapter.Pulse();assert(builds==0)")
 def test_lost_ack_stops_without_replaying_or_freeing_capacity(self):
  self.check("deferred=true;adapter.Before(city,{Type=kind},false);for i=1,14 do adapter.Pulse()end;assert(builds==0 and #sentPackets==1 and ExposedMembers.SPC_ExpeditionTrainingUIError=='TRAINING_HANDSHAKE_UNCONFIRMED')")
 def test_queue_reader_uses_directive_and_type(self):
  self.check("entries={{Directive=2,UnitType=100},{Directive=1,UnitType=103},{Directive=1,UnitType=100}};assert(ExposedMembers.SPC_ExpeditionQueueRead(2,1).count==1)")

def production_adapter():
 l=ui();l.execute("""
 include=function()end;SPCP0=P;nativeSelections=0;nativeBuilds=0
 RefreshCurrentProduction=function()end;GetDataHelper=function()return {ProjectItems={},City=city,UnitItems={}}end
 AdvanceProject=function()end;RemoveQueueItem=function()entries={}end
 SPCTimedProjectDisplay={Current=function()end,Items=function()end}
 local function factory()return {Sync=function()end,Pulse=function()end,WarmStart=function()end,Before=function()return true end}end
 SPCProjectTurnRead={New=function()end};SPCTimedProjectSelection={New=factory}
 SPCClaimProjectUI={New=factory,IsProject=function()return false end};SPCDialogueProjectUI={New=factory,PROJECT='OTHER'}
 LuaEvents={SPC_TimedProjectDisplayChanged=setmetatable({Add=function()end},{__call=function()end})}
 CityOperationTypes={PARAM_INSERT_MODE='mode',VALUE_REPLACE_AT='replace',PARAM_QUEUE_DESTINATION_LOCATION='index'}
 GetBuildInsertMode=function(p)p.mode='replace';p.index=0 end
 CheckQueueItemSelected=function()nativeSelections=nativeSelections+1;local old=queueSelected;queueSelected=false;return old end
 BuildUnit=function(c,item)if CheckQueueItemSelected()then return end;nativeBuilds=nativeBuilds+1;local p={};GetBuildInsertMode(p);entries={{Directive=1,UnitType=103}}end
 UI.RequestPlayerOperation=send
 """);l.execute((R/'Mod/UI/CrewProjectOrder.lua').read_text());return l

class ProductionAdapter(unittest.TestCase):
 def test_ordinary_queue_selection_guard_called_once(self):
  l=production_adapter();l.execute("queueSelected=true;BuildUnit(city,{Type='UNIT_SPY'});assert(nativeSelections==1 and nativeBuilds==0)")
 def test_native_replacement_intent_releases_only_after_queue_change(self):
  l=production_adapter();l.execute("train('RESERVE','r');entries={{Directive=1,UnitType=100}};train('CONFIRM','c');BuildUnit(city,{Type='UNIT_SPY'});hooks.GameCoreEventPublishComplete();hooks.GameCoreEventPublishComplete();assert(state().phase=='ENDED' and nativeBuilds==1)")

def naming():
 l=ui();l.execute('''
 include=function()end;SPCP0=P;elapsed=0;nameReads=0;calls=0
 ContextPtr={SetUpdate=function(self,fn)update=fn end,ClearUpdate=function()update=nil end,SetShutdown=function(self,fn)shutdown=fn end,SetInitHandler=function(self,fn)initializeName=fn end}
 Events.GameCoreEventPublishComplete.Remove=function()end;Events.LoadScreenClose.Remove=function()end
 Events.LocalPlayerTurnBegin={Add=function(fn)nameTurn=fn end,Remove=function()nameTurn=nil end}
 Events.UnitSelectionChanged={Add=function(fn)nameSelection=fn end,Remove=function()nameSelection=nil end}
 UI.GetHeadSelectedUnit=function()return {GetOwner=function()return selectedOwner or 2 end,GetID=function()return selectedID or 50 end}end

 SPCExpeditionSpyRead={NativeName=function(pid,id)nameReads=nameReads+1;return {status=nameStatus or 'READY',name='LOC_CITIZEN_TEST_A',reason='TEST_ERROR'}end}
 UI.RequestPlayerOperation=function(pid,op,p)calls=calls+1;lastName=p;if direct then shared.ExpeditionGate.Request(pid,p)end end
 function mirror()ExposedMembers.SPC_ExpeditionActivity={owner=2,unitID=50,teamKey='K',phase='NAMING',trainingToken='r'}end
 ''');l.execute((R/'Mod/UI/ExpeditionTrainingName.lua').read_text());l.execute('initializeName()');return l
class Name(unittest.TestCase):
 def test_default_idle_no_polling(self):
  l=naming();l.execute("hooks.GameCoreEventPublishComplete();assert(update==nil and calls==0)")
 def test_exact_ready_name_sent_once(self):
  l=naming();l.execute("mirror();hooks.GameCoreEventPublishComplete();update(.25);update(.25);assert(calls==1 and lastName.UnitID==50 and lastName.NameOffmapChecked)")
 def test_pending_timeout_bounded(self):
  l=naming();l.execute("nameStatus='PENDING';mirror();hooks.GameCoreEventPublishComplete();update(.25);update(10);hooks.GameCoreEventPublishComplete();assert(update==nil and calls==0 and nameReads==1)")
 def test_invalid_never_mutates(self):
  l=naming();l.execute("nameStatus='INVALID';mirror();hooks.GameCoreEventPublishComplete();update(.25);assert(update==nil and calls==0)")
 def test_full_training_automatic_binding_without_panel(self):
  l=naming();l.execute("adapter.Before(city,{Type=kind},false);adapter.Pulse();adapter.Pulse();born();entries={};complete();pulse();direct=true;hooks.GameCoreEventPublishComplete();update(.25);assert(state().phase=='CREATED' and state().sourceCity==1 and state().nameVerified)")
 def test_name_ack_error_preserved(self):
  l=naming();l.execute("mirror();hooks.GameCoreEventPublishComplete();update(.25);ExposedMembers.SPC_ExpeditionGateReply={owner=2,token=lastName.Token,error='ERR'};update(.25);assert(ExposedMembers.SPC_ExpeditionTrainingNameError=='ERR')")
if __name__=='__main__':unittest.main()
