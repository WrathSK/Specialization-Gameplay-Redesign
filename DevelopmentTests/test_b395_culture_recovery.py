"""B395 real owner/Store missed-load and bounded recovery regression. No native claim."""
import unittest
from test_refactor_s7d1 import profile
from test_dialogue_projects import game

class DialogueStartup(unittest.TestCase):
 def test_begin_after_store_ready_without_controller_load(self):
  with profile():l=game(skip_controller_load=True)
  l.execute("assert(shared.CityProgressionStore.HistoryStartStatus()=='FRESH' or shared.CityProgressionStore.HistoryStartStatus()=='EXISTING');local v=begin(c);assert(v and v.pending and v.pending.stage=='ACTIVE','BEGIN_DROPPED');sampleX=2;endturn();assert(ledger(c).total==10 and finishes==1);Events.CityProjectCompleted.Fire(0,c:GetID(),999);assert(finishes==1 and ledger(c).total==10)")


 def test_waiting_held_and_error_never_start_then_explicit_fact_recovery(self):
  for status in ('WAITING','HELD','THROW'):
   with profile():l=game(skip_controller_load=True)
   l.execute("originalStatus=shared.CityProgressionStore.HistoryStartStatus")
   l.execute("shared.CityProgressionStore.HistoryStartStatus=function()"+("error('TEMP_UNKNOWN')" if status=='THROW' else "return '"+status+"'")+" end;begin(c);assert(not ledger(c));shared.CityProgressionStore.HistoryStartStatus=originalStatus;begin(c);assert(ledger(c).pending.stage=='ACTIVE')")

 def test_publication_bootstraps_once_without_repeated_city_reads(self):
  with profile():l=game(skip_controller_load=True)
  l.execute("members=0;local old=Players[0].GetCities;Players[0].GetCities=function(...)local c=old(...);local m=c.Members;c.Members=function(...)members=members+1;return m(...)end;return c end;Events.GameCoreEventPublishComplete.Fire();assert(view(c).stage=='AVAILABLE');local n=members;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(members==n and not ledger(c))")

 def test_sync_is_strict_and_forced_completion_does_not_create_history(self):
  with profile():l=game(skip_controller_load=True)
  l.execute("local status=shared.CityProgressionStore.HistoryStartStatus;shared.CityProgressionStore.HistoryStartStatus=function()return 'HELD'end;dp.Sync(0,c:GetID(),'held');assert(not dp.syncAck['0:'..c:GetID()]);Events.CityProjectCompleted.Fire(0,c:GetID(),999);assert(not ledger(c));shared.CityProgressionStore.HistoryStartStatus=status;dp.Sync(0,c:GetID(),'ready');assert(dp.syncAck['0:'..c:GetID()]=='ready');Events.CityProjectCompleted.Fire(0,c:GetID(),999);assert(not ledger(c)and finishes==0)")

class EarlyUnknownLoad(unittest.TestCase):
 def test_real_pending_unknown_early_publish_recovers_at_actual_load(self):
  with profile():l=game()
  l.execute("begin(c);skipControllerLoad=true;reload();local read=c.q.CurrentlyBuilding;c.q.CurrentlyBuilding=function()error('QUEUE_NOT_PUBLISHED')end;Events.GameCoreEventPublishComplete.Fire();assert(ledger(c).pending and finishes==0);c.q.CurrentlyBuilding=read;Events.LoadScreenClose.Fire();assert(view(c).stage=='ACTIVE');endturn();assert(finishes==1 and ledger(c).total==5)")

class CurrentReplacement(unittest.TestCase):
 def panel(self):
  from timed_project_ui_fixture import fixture
  from test_b394_culture_diagnostics import install,ROOT
  l=fixture('Dialogue',connect=True);install(l,'on');include=l.globals().include
  def panel_include(name):
   if name in ('SafeAdapters','IdentityEqual'):return include(name)
  l.globals().include=panel_include
  l.execute("""
   ContextPtr={SetShutdown=function(self,fn)panelShutdown=fn end,IsHidden=function()return false end}
   SPCP0=P;SPCDialogueProjectUI.New=function()return ui end
   CityOperationTypes={PARAM_PROJECT_TYPE='project',PARAM_INSERT_MODE='mode',PARAM_QUEUE_DESTINATION_LOCATION='index',VALUE_REPLACE_AT=1}
   insertMode=1;destination=0;baseAdvances=0;nativeBuilds=0
   GetBuildInsertMode=function(p)p.mode=insertMode;p.index=destination;return 17 end
   AdvanceProject=function(c,item)local p={project=GameInfo.Projects[item.Type].Hash};GetBuildInsertMode(p);baseAdvances=baseAdvances+1;q.target=item.Type;return true end
   BuildUnit=function(c,item)local p={};assert(GetBuildInsertMode(p)==17 and p.mode==insertMode and p.index==destination);nativeBuilds=nativeBuilds+1;q.target=item.Type;return true end
   CheckQueueItemSelected=function()return false end
   UI={GetHeadSelectedCity=function()return c end,RequestPlayerOperation=sendUI}
  """)
  l.execute((ROOT/'Mod/UI/CrewProjectOrder.lua').read_text());return l
 def test_native_current_replacement_allows_reselection(self):
  l=self.panel();l.execute("assert(AdvanceProject(c,{Type=project}));assert(BuildUnit(c,{Type='UNIT_DRONE'}));assert(AdvanceProject(c,{Type=project}));assert(baseAdvances==2 and nativeBuilds==1 and q.target==project);ownEventUI();pumpUI();assert(uiBegins==1 and pending().stage=='ACTIVE')")
 def test_append_and_tail_replacement_preserve_current_intent(self):
  for mode,index in ((2,0),(1,8)):
   l=self.panel();l.execute(f"assert(AdvanceProject(c,{{Type=project}}));insertMode={mode};destination={index};BuildUnit(c,{{Type='UNIT_DRONE'}});assert(not AdvanceProject(c,{{Type=project}}));assert(baseAdvances==1 and nativeBuilds==1)")

class ActivityLoad(unittest.TestCase):
 def cold(self):
  from test_expedition_spy_activity_integration import integrated,R
  l=integrated();l.execute("""
   beginTask();assert(view().mode=='ASLEEP' and sleepCalls==1);savedDue=view().taskDue
   activityShutdown();Events.LoadScreenClose=event();SPCExpeditionSpyGate.Start(P,shared)
   local send=UI.RequestPlayerOperation;loadClosed=false;recoveryAttempts=0;lostRecovery=0
   UI.RequestPlayerOperation=function(pid,op,p)
    if p.Result=='RECOVERED'then recoveryAttempts=recoveryAttempts+1;if not loadClosed then lostRecovery=lostRecovery+1;return false end end
    return send(pid,op,p)
   end
  """)
  l.eval("function(source)assert(load(source,'ExpeditionSpyActivity','t',activityEnvironment))()end")((R/'Mod/UI/ExpeditionSpyActivity.lua').read_text())
  l.execute('activityInit();Events.GameCoreEventPublishComplete();drainRefreshFrames()');return l
 def test_first_ack_after_load_not_loader_stack_then_exact_once_reward(self):
  l=self.cold();l.execute("""
   assert(recoveryAttempts==0 and lostRecovery==0 and view().mode=='RECOVER')
   loadClosed=true;Events.LoadScreenClose();assert(recoveryAttempts==0)
   Events.GameCoreEventPublishComplete();assert(recoveryAttempts==1 and lostRecovery==0)
   assert(view().mode=='ASLEEP' and view().taskDue==savedDue and sleepCalls==1 and wakeCalls==0)
   Events.LoadScreenClose();for i=1,100 do Events.GameCoreEventPublishComplete()end
   assert(recoveryAttempts==1 and sleepCalls==1)
   currentTurn=savedDue;ownTurn(2);Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin();ownTurn(2);Events.GameCoreEventPublishComplete()
   assert(view().phase=='ARRIVED' and view().mode=='NONE' and insightWrites==1 and sleepCalls==1 and wakeCalls==1)
   assert(placeCalls==0 and destroys==0 and properties==0)
  """)
 def test_ui_load_only_and_gp_load_mirror_late_ui(self):
  from test_expedition_spy_activity_ui import bridge
  for gp in (False,True):
   l=bridge(load_closed=False);l.execute("nativeAuto=false;noAck=true;units[41].activity=1;publish('RECOVER',true);assert(#packets==0)")
   if gp:l.execute("ExposedMembers.SPC_ExpeditionActivity.loadReady=true;Events.GameCoreEventPublishComplete()")
   else:l.execute("Events.LoadScreenClose();assert(#packets==0);Events.GameCoreEventPublishComplete()")
   l.execute("assert(#packets==1 and packets[1].Result=='RECOVERED'and sleepCalls==0);Events.LoadScreenClose();for i=1,100 do Events.GameCoreEventPublishComplete()end;assert(#packets==1)")
 def test_transport_unknown_is_observed_without_replay(self):
  from test_expedition_spy_activity_ui import bridge
  from test_b394_culture_diagnostics import install
  for outcome in ('false','nil','true',"error('RPC_UNKNOWN')"):
   l=bridge();install(l,'on')
   l.execute("attempts=0;UI.RequestPlayerOperation=function()attempts=attempts+1;"+(outcome if outcome.startswith('error')else 'return '+outcome)+" end;units[41].activity=1;publish('RECOVER',true);for i=1,100 do Events.LoadScreenClose();Events.GameCoreEventPublishComplete()end;assert(attempts==1 and sleepCalls==0 and wakeCalls==0);local send,ret=false,false;for _,r in ipairs(diagRows)do if r.point=='EXPEDITION_ACK_SEND'then send=true end;if r.point=='EXPEDITION_ACK_RETURN'then ret=true;assert(r.requestResult=='"+('THREW'if outcome.startswith('error')else outcome.upper())+"')end end;assert(send and ret)")
 def test_same_closure_shutdown_init_does_not_reuse_load_flag(self):
  from test_expedition_spy_activity_integration import integrated
  l=integrated();l.execute("beginTask();activityShutdown();Events.LoadScreenClose=event();SPCExpeditionSpyGate.Start(P,shared);local send=UI.RequestPlayerOperation;early=0;loadClosed=false;UI.RequestPlayerOperation=function(pid,op,p)if p.Result=='RECOVERED'and not loadClosed then early=early+1;return false end;return send(pid,op,p)end;activityInit();Events.GameCoreEventPublishComplete();assert(early==0 and view().mode=='RECOVER');loadClosed=true;Events.LoadScreenClose();Events.GameCoreEventPublishComplete();assert(early==0 and view().mode=='ASLEEP'and sleepCalls==1)")
 def test_preload_wait_has_no_timeout_and_displacement_still_rejected(self):
  from test_expedition_spy_activity_ui import bridge
  l=bridge(load_closed=False);l.execute("nativeAuto=false;noAck=true;units[41].activity=1;publish('RECOVER',true);turn=turn+2;Events.LocalPlayerTurnBegin();assert(#packets==0);units[41].x=99;Events.LoadScreenClose();Events.GameCoreEventPublishComplete();assert(#packets==1 and packets[1].Result=='FAILED' and sleepCalls==0 and wakeCalls==0)")

class GPPObserver(unittest.TestCase):
 def ui(self):
  from lupa.lua51 import LuaRuntime
  from test_b394_culture_diagnostics import install
  l=LuaRuntime();install(l,'on');l.execute("""
   reads=0;workers=0;commands=0;Map={GetPlotByIndex=function(i)return {GetDistrictType=function()return 7 end,GetWorkerCount=function()workers=workers+1;return 1 end}end}
   city={GetOwner=function()return 0 end,GetID=function()return 1 end,GetX=function()return 2 end,GetY=function()return 3 end}
   district={GetType=function()return 7 end,GetCity=function()return city end,GetX=function()return 4 end,GetY=function()return 5 end}
   city.GetDistricts=function()return {Members=function()local done;return function()if not done then done=true;return 0,district end end end}end
   Map.GetPlot=function()return {GetIndex=function()return 33 end}end
   Game={GetLocalPlayer=function()return 0 end};UI={GetHeadSelectedCity=function()return city end,GetInterfaceModeParameter=function(k)return 99 end}
   P={Family=function(t)return t=='DISTRICT_THEATER'and 'CULTURE'or 'NONE'end,IsTestPlayer=function(i)return i==0 end,Info=function(t,i)return {DistrictType='DISTRICT_THEATER'}end}
   CityCommandTypes={MANAGE=3,PARAM_MANAGE_CITIZEN=4};CityCommandResults={PLOTS=1,CITIZENS=2,MAX_CITIZENS=3,LOCKED_CITIZENS=4}
   rows={{[8]=33},{[8]=2},{[8]=3},{[8]=1}}
   CityManager={GetCommandTargets=function(c,cmd,p)assert(cmd==3 and p[4]==99);reads=reads+1;return rows end,RequestCommand=function()commands=commands+1;error('FORBIDDEN_WRITE')end}
   function observe(t)SPCCultureDiagnostics.ObserveGPPUI(P,t or 'read1',1,'CULTURE')end
  """);return l
 def test_same_key_actual_locked_capacity_once_and_no_command(self):
  l=self.ui();l.execute("observe();for i=1,100 do observe()end;assert(reads==1 and workers==1 and commands==0 and #diagRows==1);local r=diagRows[1];assert(r.workers==2 and r.count==1 and r.expectedNumber==3 and r.actualNumber==1 and r.requestKey=='read1')")
 def test_disabled_missing_ambiguous_and_invalid_facts(self):
  l=self.ui();l.execute("SPCCultureDiagnostics.ENABLED=false;observe();assert(reads==0 and #diagRows==0)")
  for change in ('rows[4]=nil','rows[4][8]=nil','rows[4][8]=true','rows[1][9]=33'):
   l=self.ui();l.execute(change+";observe();assert(#diagRows==1 and diagRows[1].readStatus=='UNKNOWN'and diagRows[1].workers==nil and commands==0);observe();assert(reads==1)")
 def test_foreign_anchor_and_selection_change_remain_unknown(self):
  for change in ("district.GetCity=function()return {GetOwner=function()return 0 end,GetID=function()return 99 end}end", "rows[1][8]=99", "local read=CityManager.GetCommandTargets;CityManager.GetCommandTargets=function(...)local r=read(...);UI.GetHeadSelectedCity=function()return nil end;return r end"):
   l=self.ui();l.execute(change+";observe();assert(diagRows[1].readStatus=='UNKNOWN'and diagRows[1].workers==nil and commands==0)")
 def test_bounded_recent_tokens_cannot_resample_A_B_A(self):
  l=self.ui();l.execute("observe('A');observe('B');observe('A');assert(reads==2 and #diagRows==2)")
 def test_observer_limit_precedes_any_extra_native_sample(self):
  l=self.ui();l.execute("for i=1,400 do observe('token'..i)end;assert(reads==192 and #diagRows==193 and diagRows[193].point=='LIMIT_REACHED')")
 def test_actual_p0_reply_is_identical_without_or_with_failing_observer(self):
  from test_b394_culture_diagnostics import ROOT
  source=(ROOT/'Mod/UI/P0Panel.lua').read_text();body=source[source.index('local function displayResponse()'):source.index('-- B060 read/control')]
  reports=[]
  for mode in ('on','off','absent','throw','lookup'):
   l=self.ui()
   if mode=='off':l.execute('SPCCultureDiagnostics.ENABLED=false')
   if mode=='absent':l.execute('SPCCultureDiagnostics=nil')
   if mode=='throw':l.execute("SPCCultureDiagnostics.ObserveGPPUI=function()error('OPTIONAL_FAILED')end")
   if mode=='lookup':l.execute("SPCCultureDiagnostics=setmetatable({},{__index=function()error('OPTIONAL_LOOKUP_FAILED')end})")
   l.execute("P.VERSION='B395';local pendingToken,pendingAction,pageCity,page,readings='read1','LV2_GPP_READ',1,1,{};local localReport;local function status(s)displayed=s end;SPCGPPReadout={Render=function(_,s)return s end};ExposedMembers={SPC_P0={Version=P.VERSION,LastToken='read1',Snapshot='city=1 CULTURE ACTIVE=4 workers=1'}};"+body+";assert(displayResponse());assert(displayResponse());assert(commands==0)")
   reports.append(l.globals().displayed);self.assertEqual(l.globals().reads,1 if mode=='on'else 0)
  self.assertTrue(all(v==reports[0]for v in reports))
 def test_success_does_not_emit_gpp_failure(self):
  from test_refactor_s7a2 import fixture
  from test_b394_culture_diagnostics import install
  l=fixture();install(l,'on');l.execute("gppAudit();for _,r in ipairs(diagRows)do assert(r.point~='GPP_FAILED')end;count=nil;shared.Lv2GPP.Audit({player=0,city=0});local found=false;for _,r in ipairs(diagRows)do if r.point=='GPP_FAILED'then found=true end end;assert(found)")

if __name__=='__main__':unittest.main()
