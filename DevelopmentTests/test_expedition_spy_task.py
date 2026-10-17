"""B187 actual-module name identity, inherited independent timer and exact-type UI boundary.
Native controlled-name survival/idle effects/rendering require the one-session game test.
"""
from pathlib import Path
import unittest
from lupa.lua55 import LuaRuntime
import test_expedition_spy_gate as previous
R=Path(__file__).resolve().parents[1]

def gate(ui=False,window=False):
    l=previous.gate(ui=ui,window=window)
    l.execute("""
      function arrival(id,keep,alias)
       local old=units[40];local u=unit(id,100,2,15,8)
       if keep then u.name=old.name end
       units[40]=nil;units[id]=u
       local us=Players[2]:GetUnits()
       if alias then us.FindID=function(self,key)if key==40 then return u end;return units[key]end end
       currentTurn=83;ownTurn(2);return req('READ','arrival')
      end
      function task(token,overrides)
       local p={Action='TASK',Token=token,UnitID=41,SampleTurn=currentTurn,NativeOperation=-1,Mission='PEOPLE',MissionX=15,MissionY=8}
       for k,v in pairs(overrides or {})do p[k]=v end
       handler(2,p)
       local r=ExposedMembers.SPC_ExpeditionGateReply
       if r.phase=='TASK_PREPARING' and not r.error then
        handler(2,{Action='ACTIVITY',Token=token..':arm',UnitID=41,ActivityKey=ExposedMembers.SPC_ExpeditionActivity.activityKey,
         Result='ARMED',Owned=true,Awake=true,Sleeping=false,SampleTurn=currentTurn,NativeOperation=-1})
        handler(2,{Action='ACTIVITY',Token=token..':sleep',UnitID=41,ActivityKey=ExposedMembers.SPC_ExpeditionActivity.activityKey,
         Result='ASLEEP',Owned=true,SampleTurn=currentTurn,NativeOperation=-1})
        return ExposedMembers.SPC_ExpeditionActivityReply
       end
       return ExposedMembers.SPC_ExpeditionGateReply
      end
    """)
    return l

class Continuity(unittest.TestCase):
    def test_name_not_native_id_proves_arrival_including_lookup_alias(self):
        for alias in ['true','false']:
            with self.subTest(alias=alias):
                l=gate();l.execute("req('CREATE','a');nativeDispatch('b');local r=arrival(41,true,"+alias+");assert(r.phase=='ARRIVED' and r.bound and not r.unbound and r.unitID==41 and r.createdID==40 and r.sourceCity==1 and r.count==1 and properties==0)")
    def test_default_name_coordinates_and_sole_unit_do_not_rebind(self):
        for change in ['units[41].name=nil','units[41].name="wrong"','units[41].owner=3','units[41].type_=103']:
            with self.subTest(change=change):
                l=gate();l.execute("req('CREATE','a');nativeDispatch('b');arrival(41,false,false);"+change+";currentTurn=85;ownTurn(2);local r=req('READ','c');assert(r.phase=='HELD' and not r.bound and r.sourceCity==1 and destroys==0 and properties==0)")
    def test_two_name_matches_are_ambiguous(self):
        l=gate();l.execute("req('CREATE','a');nativeDispatch('b');units[41]=unit(41,100,2,15,8);units[42]=unit(42,100,2,15,8);units[41].name=units[40].name;units[42].name=units[40].name;units[40]=nil;currentTurn=83;ownTurn(2);assert(req('READ','c').stop=='TEAM_NAME_AMBIGUOUS' and destroys==0 and properties==0)")
    def test_same_name_elsewhere_does_not_count_as_arrival(self):
        l=gate();l.execute("req('CREATE','a');nativeDispatch('b');units[40].x=16;units[40].y=8;currentTurn=85;ownTurn(2);assert(req('READ','r').phase=='HELD' and not req('READ','s').bound)")
    def test_source_replacement_during_travel_never_reattaches(self):
        l=gate();l.execute("req('CREATE','a');nativeDispatch('b');city.token='replacement';local r=arrival(41,true,true);assert(r.phase=='HELD' and not r.bound and r.createdID==40 and r.sourceCity==1 and properties==0)")
    def test_name_pending_does_not_create_or_dispatch_again(self):
        l=gate();l.execute("rawreq('CREATE','a');rawreq('CREATE','b');local r=nativeDispatch('d');assert(initCalls==1 and not r.nativePermit and r.phase=='NAMING' and properties==0)")
    def test_unbound_name_lost_team_can_be_explicitly_cleaned_not_adopted(self):
        l=gate();l.execute("req('CREATE','a');nativeDispatch('b');arrival(41,false,false);currentTurn=85;ownTurn(2);local r=req('READ','c');assert(not r.bound and r.unitID==41);req('END','e',41);assert(destroys==1 and req('READ','f').count==0)")
    def test_cold_session_never_claims_a_surviving_name(self):
        l=gate();l.execute("req('CREATE','a');gameProperties={};SPCExpeditionSpyGate.Start(P,shared);local r=req('READ','new');assert(r.unbound and not r.bound and r.unitID==40);req('CREATE','new2');assert(initCalls==1);req('END','e',40);assert(destroys==1)")
    def test_strict_id_guard_rejects_ui_dispatch_or_end_through_alias(self):
        l=gate(ui=True);l.execute("req('CREATE','a');nativeDispatch('b');arrival(41,true,true);assert(not reader.SubmitTravel(2,40,target,'stale'));req('END','e',40);assert(destroys==0 and units[41])")

class Timer(unittest.TestCase):
    def ready(self):
        l=gate();l.execute("req('CREATE','a');nativeDispatch('b');arrival(41,true,false)");return l
    def test_two_turn_task_has_no_rewards_native_operations_or_extra_writes(self):
        l=self.ready();l.execute("local r=task('t');assert(r.phase=='TASK_RUNNING' and r.taskDue==85);currentTurn=84;ownTurn(2);assert(req('READ','r').taskCompletions==0);currentTurn=85;ownTurn(2);ownTurn(2);r=req('READ','s');assert(r.phase=='TASK_COMPLETE' and r.taskCompletions==1 and nativeCalls==0 and properties==0 and placeCalls==0 and finishCalls==0 and destroys==0)")
    def test_completed_team_redispatches_after_release_and_runs_another_task(self):
        # B211: completion -> released activity -> new dispatch -> arrival -> second task with a fresh activity key.
        l=self.ready();l.execute("""
         task('t');currentTurn=85;ownTurn(2);ownTurn(2)
         local v=ExposedMembers.SPC_ExpeditionActivity;assert(v.phase=='TASK_COMPLETE' and v.mode=='RELEASE');local firstKey=v.activityKey
         -- A second met major's capital as the new target (v0.1 fixture targets capitals).
         local second={id=12,owner=4,x=20,y=5}
         for k,f in pairs({GetID=function(c)return c.id end,GetOwner=function(c)return c.owner end,GetX=function(c)return c.x end,GetY=function(c)return c.y end,GetName=function()return '第二目标城' end})do second[k]=f end
         local cs={FindID=function(self,id)if id==12 then return second end end,GetCapitalCity=function()return second end}
         Players[4]={IsMajor=function()return true end,IsAlive=function()return true end,GetCities=function()return cs end,
          GetUnits=function()return {FindID=function()return nil end}end}
         local early=nativeDispatch('early',{UnitID=41,FromX=15,FromY=8,TargetOwner=4,TargetID=12,TargetX=20,TargetY=5})
         assert(early.error and req('READ','still').phase=='TASK_COMPLETE')
         handler(2,{Action='ACTIVITY',Token='rel',UnitID=41,ActivityKey=v.activityKey,Result='RELEASED',Owned=true,SampleTurn=currentTurn,NativeOperation=-1})
         assert(ExposedMembers.SPC_ExpeditionActivity.mode=='NONE')
         local r=nativeDispatch('again',{UnitID=41,FromX=15,FromY=8,TargetOwner=4,TargetID=12,TargetX=20,TargetY=5})
         assert(r.phase=='TRAVELLING' and not r.error and r.taskStart==nil and r.taskCompleted==nil)
         local old=units[41];local u=unit(42,100,2,20,5);u.name=old.name;units[41]=nil;units[42]=u
         currentTurn=currentTurn+2;ownTurn(2);r=req('READ','arrived2');assert(r.phase=='ARRIVED' and r.trackedID==42,tostring(r.phase))
         handler(2,{Action='TASK',Token='t2',UnitID=42,SampleTurn=currentTurn,NativeOperation=-1,Mission='PEOPLE',MissionX=20,MissionY=5})
         local key=ExposedMembers.SPC_ExpeditionActivity.activityKey;assert(key~=firstKey and key:match(':attempt%d+$'),key)
         handler(2,{Action='ACTIVITY',Token='t2:arm',UnitID=42,ActivityKey=key,Result='ARMED',Owned=true,Awake=true,Sleeping=false,SampleTurn=currentTurn,NativeOperation=-1})
         handler(2,{Action='ACTIVITY',Token='t2:sleep',UnitID=42,ActivityKey=key,Result='ASLEEP',Owned=true,SampleTurn=currentTurn,NativeOperation=-1})
         r=ExposedMembers.SPC_ExpeditionActivityReply;assert(r.phase=='TASK_RUNNING',tostring(r.phase)..tostring(r.error))
         currentTurn=currentTurn+2;ownTurn(2);ownTurn(2);r=req('READ','done2')
         assert(r.phase=='TASK_COMPLETE' and r.taskCompletions==1 and destroys==0)
        """)
    def test_completed_team_without_release_cannot_redispatch(self):
        l=self.ready();l.execute("""
         task('t');currentTurn=85;ownTurn(2);ownTurn(2)
         local r=nativeDispatch('x',{UnitID=41,FromX=15,FromY=8});assert(r.error and req('READ','r').phase=='TASK_COMPLETE')
        """)
    def test_duplicate_start_and_completion_are_idempotent(self):
        l=self.ready();l.execute("task('t');task('t');task('t2');assert(req('READ','r').taskDue==85);currentTurn=85;ownTurn(2);task('t3');currentTurn=86;ownTurn(2);local r=req('READ','s');assert(r.taskCompletions==1 and r.taskCompleted==85 and properties==0)")
    def test_stale_or_nonidle_ui_sample_cannot_start(self):
        for fields in ['SampleTurn=82','NativeOperation=9','NativeOperation=false']:
            with self.subTest(fields=fields):
                l=self.ready();l.execute("local r=task('t',{"+fields+"});assert(r.error and r.phase=='ARRIVED' and not r.taskStart)")
    def test_gameplay_does_not_assume_ui_only_getter(self):
        l=self.ready();l.execute("units[41].GetSpyOperation=nil;task('t');currentTurn=85;ownTurn(2);assert(req('READ','r').phase=='TASK_COMPLETE')")
    def test_native_operation_when_readable_stops_completion(self):
        l=self.ready();l.execute("task('t');units[41].operation=9;currentTurn=85;ownTurn(2);local r=req('READ','r');assert(r.phase=='HELD' and r.taskCompletions==0 and r.stop=='NATIVE_MISSION_ACTIVE_STOP')")
    def test_source_unknown_loss_target_change_name_loss_or_displacement_holds(self):
        for change in ['city.token=nil','city.owner=3','units[41].name=nil','units[41].x=16']:
            with self.subTest(change=change):
                l=self.ready();l.execute("task('t');"+change+";currentTurn=85;ownTurn(2);local r=req('READ','r');assert(r.phase=='HELD' and r.taskCompletions==0 and destroys==0 and properties==0)")
    def test_target_invalidation_cancels_without_insight_and_returns(self):
        # B212 Design: target owner change / city loss cancels; no Insight, no quota; unit kept.
        for change in ['targetCity.owner=4','targetCity.id=10']:
            with self.subTest(change=change):
                l=self.ready();l.execute("task('t');"+change+";currentTurn=84;ownTurn(2);local r=req('READ','r');assert(r.phase=='TASK_COMPLETE' and r.taskOutcome=='CANCELLED' and r.taskCompletions==0 and insightWrites==0 and destroys==0)")
    def test_active_drop_does_not_erase_source_or_advance_on_foreign_turn(self):
        l=self.ready();l.execute("task('t');active=1;currentTurn=85;ownTurn(3);assert(ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_RUNNING');ownTurn(2);local r=req('READ','r');assert(r.phase=='TASK_COMPLETE' and r.sourceCity==1 and r.bound)")
    def test_read_at_due_turn_does_not_replace_player_turn_completion(self):
        l=self.ready();l.execute("task('t');currentTurn=85;ownTurn(3);assert(req('READ','before').phase=='TASK_RUNNING');ownTurn(2);assert(req('READ','after').phase=='TASK_COMPLETE')")
    def test_source_and_team_only_no_per_turn_player_scan_after_arrival(self):
        l=self.ready();l.execute("task('t');local us=Players[2]:GetUnits();local original=us.Members;us.Members=function()error('unexpected all-unit scan')end;currentTurn=84;ownTurn(2);currentTurn=85;ownTurn(2);us.Members=original;local r=req('READ','after');assert(shared.RequestDepth==0 and r.phase=='TASK_COMPLETE' and r.taskCompletions==1)")
    def test_window_closed_timer_and_source_diagnostics(self):
        l=gate(window=True);l.execute("gateOpen();Controls.CreateButton.click();Controls.ArmButton.click();arrival(41,true,false);Controls.RefreshButton.click();Controls.TaskButton.click();assert(lastPacket.Action=='TASK');local key=ExposedMembers.SPC_ExpeditionActivity.activityKey;handler(2,{Action='ACTIVITY',Token='arm',UnitID=41,ActivityKey=key,Result='ARMED',Owned=true,Awake=true,Sleeping=false,SampleTurn=currentTurn,NativeOperation=-1});handler(2,{Action='ACTIVITY',Token=key..':sleep',UnitID=41,ActivityKey=key,Result='ASLEEP',Owned=true,SampleTurn=currentTurn,NativeOperation=-1});Controls.CloseButton.click();currentTurn=85;ownTurn(2);gateOpen();assert(Controls.Report.text:find('PHASE_TASK_COMPLETE') and Controls.Report.text:find('TASK_ISOLATION:0,0,-1,0',1,true));Controls.EndButton.click();publish();assert(destroys==1 and Controls.Report.text:find('PHASE_ENDED'))")
    def test_task_button_requires_verified_arrival_and_idle_native_state(self):
        l=gate(window=True);l.execute("gateOpen();Controls.CreateButton.click();local n=sent;Controls.TaskButton.click();assert(sent==n);Controls.ArmButton.click();arrival(41,true,false);Controls.RefreshButton.click();units[41].operation=9;n=sent;Controls.TaskButton.click();assert(sent==n and Controls.Report.text:find('TASK_NATIVE_NOT_IDLE'))")

def ui(kind):
    l=LuaRuntime(unpack_returned_tuples=True)
    l.execute("""
      calls={};routed=0;routes={};selected=nil;mode=0
      function base(name)return function(...)calls[name]=(calls[name]or 0)+1;return 'ordinary' end end
      function event()local e={listeners={}};function e.Add(fn)e.listeners[fn]=true end;function e.Remove(fn)e.listeners[fn]=nil end
       return setmetatable(e,{__call=function(self,...)for f in pairs(self.listeners)do f(...)end end})end
      Game={GetLocalPlayer=function()return 2 end};GameInfo={Units={[1]={UnitType='UNIT_SPC_EXPEDITION_SPY'},[2]={UnitType='UNIT_SPY'},[3]={UnitType='UNIT_SETTLER'}},UnitOperations={UNITOPERATION_SKIP_TURN={Hash=8,CategoryInUI='INPLACE'}}}
      function unit(kind,owner,id)
       local u={id=id or (kind==1 and 40 or kind==2 and 41 or 43),owner=owner or 2,kind=kind,x=15,y=8,name='Native Named Spy',operation=-1}
       function u:GetUnitType()return self.kind end;function u:GetOwner()return self.owner end
       function u:GetID()return self.id end;function u:GetX()return self.x end;function u:GetY()return self.y end
       function u:GetName()return self.name end;function u:GetSpyOperation()return self.operation end
       function u:IsReadyToMove()return self.ready~=false end
       return u
      end
      team=unit(1);ordinary=unit(2);civilian=unit(3);otherTeam=unit(1,2,42)
      units={[40]=team,[41]=ordinary,[42]=otherTeam};selected=team
      ExposedMembers={SPC_ExpeditionActivity={owner=2,unitID=40,teamKey='team1',activityKey='',
       expectedName='Native Named Spy',x=15,y=8,phase='CREATED',mode='NONE',locked=false,revision=1}}
      function phase(value,modeValue,locked)
       local v=ExposedMembers.SPC_ExpeditionActivity;v.phase=value;v.mode=modeValue or 'NONE';v.locked=locked or false
      end
      function selectionCity(owner,id,x,y)
       return {GetOwner=function()return owner end,GetID=function()return id end,GetX=function()return x end,GetY=function()return y end}
      end
      homeCity=selectionCity(2,1,15,8);foreignCity=selectionCity(3,9,15,8);selectionCityObject=homeCity
      Players={[2]={GetUnits=function()return {FindID=function(self,id)return units[id]end}end,
       GetCities=function()return {FindID=function(self,id)if id==1 then return homeCity end end}end},
       [3]={GetCities=function()return {FindID=function(self,id)if id==9 then return foreignCity end end}end}}
      Map={GetPlot=function(x,y)return {}end};Cities={GetPlotPurchaseCity=function()cityLookups=(cityLookups or 0)+1;return selectionCityObject end}
      Events={UnitSelectionChanged=event(),UnitActivityChanged=event()}
      ActivityTypes={ACTIVITY_AWAKE=0,ACTIVITY_SLEEP=1};activityType=0
      UI={GetHeadSelectedUnit=function()return selected end,GetInterfaceMode=function()return mode end,SetInterfaceMode=function(m)mode=m;if onMode then onMode()end end}
      InterfaceModeTypes={SELECTION=0};Locale={Lookup=function(s)return s end};Mouse={eLClick=1}
      LuaEvents={SPC_ExpeditionActivityChanged=event(),SPC_ExpeditionGateOpen=event(),GameDebug_Return=event(),EspionageChooser_ShowMissionBriefing=event(),UnitPanel_CancelMission=event()}
      LuaEvents.SPC_ExpeditionGateOpen.Add(function(action,id)routed=routed+1;routes[#routes+1]={mode=action,id=id}end)
      Controls={};for _,id in ipairs({'ConfirmButton','AcceptButton','AbortButton'})do Controls[id]={RegisterCallback=function(self,key,fn)self.click=fn end}end
      ContextPtr={SetShutdown=function(self,fn)panelShutdown=fn end};Refresh=base('Refresh');include=function()end
      for _,name in ipairs({'Open','Close','GoToProperInterfaceMode','TeleportToSelectedCity','OnConfirmPlacement','OnCounterspySelected','OnMissionSelected','OnGameDebugReturn','OnShowMissionBriefing','OnShowMissionAbort','OnAccept','OnAbort','RenewMission','ShowMissionCompletedPopup','OnUnitActionClicked','OnUnitActionClicked_CancelSpyMission','GetUnitActionsTable','OnUnitSelectionChanged','OnShutdown'})do _G[name]=base(name)end
      Events.UnitSelectionChanged.Add(OnUnitSelectionChanged)
      function OnUnitActivityChanged()GoToProperInterfaceMode(UI.GetHeadSelectedUnit())end
      Events.UnitActivityChanged.Add(OnUnitActivityChanged)
      LuaEvents.GameDebug_Return.Add(OnGameDebugReturn)
      LuaEvents.EspionageChooser_ShowMissionBriefing.Add(OnShowMissionBriefing)
      LuaEvents.UnitPanel_CancelMission.Add(OnShowMissionAbort)
      function AddActionToTable(actions,row,disabled,tip,hash,callback)table.insert(actions[row.CategoryInUI],{CallbackFunc=callback,userTag=hash,disabled=disabled,tip=tip,icon=row.Icon})end
      UnitManager={GetActivityType=function()return activityType end,CanStartOperation=function(u,op)assert(op==8);return true end,RequestOperation=function(u,op)assert(op==8);calls.skip=(calls.skip or 0)+1 end}
    """)
    l.execute((R/'Mod/ExpeditionSpyUI.lua').read_text());l.execute((R/f'Mod/UI/ExpeditionSpy{kind}.lua').read_text());return l

class UIIsolation(unittest.TestCase):
    def test_action_layout_matches_native_primary_and_secondary_reader(self):
        l=ui('UnitPanel');l.execute("local a=GetUnitActionsTable(team);local n=0;for _,area in ipairs({'primaryArea','secondaryArea'})do for _,category in ipairs(a.displayOrder[area])do for _,action in ipairs(a[category])do assert(type(action.CallbackFunc)=='function');n=n+1 end end end;assert(n==2 and #a.SPECIFIC==2 and #a.INPLACE==0)")
    def test_unitpanel_custom_actions_do_not_build_base_native_hotkeys(self):
        l=ui('UnitPanel');l.execute("selected=team;phase('ARRIVED');local a=GetUnitActionsTable(team);assert(not calls.GetUnitActionsTable and #a.OFFENSIVESPY==0 and #a.SPECIFIC==2 and #a.INPLACE==0);a.SPECIFIC[1].CallbackFunc();a.SPECIFIC[2].CallbackFunc();OnUnitActionClicked(99,9);OnUnitActionClicked_CancelSpyMission();assert(routed==2 and not calls.skip and not calls.OnUnitActionClicked);assert(routes[1].mode=='TRAVEL' and routes[1].id==40 and routes[2].mode=='TASK' and routes[2].id==40);selected=ordinary;assert(GetUnitActionsTable(ordinary)=='ordinary');OnUnitActionClicked(99,9);assert(calls.OnUnitActionClicked==1)")
    def test_callbacks_recheck_current_selection(self):
        l=ui('UnitPanel');l.execute("selected=team;phase('ARRIVED');local a=GetUnitActionsTable(team);selected=ordinary;a.SPECIFIC[1].CallbackFunc();a.SPECIFIC[2].CallbackFunc();assert(routed==0 and not calls.skip)")
    def test_chooser_mouse_selection_hot_reload_and_globals_suppress_exact_type_without_report(self):
        l=ui('Chooser');l.execute("selected=team;Open();GoToProperInterfaceMode(team);Controls.ConfirmButton.click();OnCounterspySelected();OnMissionSelected();TeleportToSelectedCity();LuaEvents.GameDebug_Return('EspionageChooser',{selectedSpy=team,isVisible=true});assert(routed==0 and not calls.Open and not calls.OnConfirmPlacement and not calls.OnGameDebugReturn and calls.Close);selected=ordinary;Open();Controls.ConfirmButton.click();assert(calls.Open==1 and calls.OnConfirmPlacement==1)")
    def test_popup_briefing_cancel_accept_renew_and_hot_reload_never_cache_team(self):
        l=ui('Popup');l.execute("selected=team;LuaEvents.EspionageChooser_ShowMissionBriefing(9,40,{});Controls.AcceptButton.click();LuaEvents.UnitPanel_CancelMission(40);Controls.AbortButton.click();RenewMission(team,9,1,1);LuaEvents.GameDebug_Return('EspionagePopup',{spy=team,isHidden=false});assert(routed==0 and calls.Close and not calls.OnShowMissionBriefing and not calls.OnShowMissionAbort and not calls.RenewMission and not calls.OnGameDebugReturn);selected=ordinary;LuaEvents.EspionageChooser_ShowMissionBriefing(9,41,{});Controls.AcceptButton.click();RenewMission(ordinary,9,1,1);assert(calls.OnShowMissionBriefing==1 and calls.OnAccept==1 and calls.RenewMission==1)")
    def test_foreign_same_type_and_other_units_pass_through(self):
        l=ui('UnitPanel');l.execute("assert(GetUnitActionsTable(unit(1,3))=='ordinary' and GetUnitActionsTable(civilian)=='ordinary' and calls.GetUnitActionsTable==2)")

if __name__=='__main__':unittest.main()
