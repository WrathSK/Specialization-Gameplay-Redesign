"""Actual unit UI modules; explicit request receiver, native unit/lens/control doubles."""
import unittest
from refactor_harness import Context, measure, TrackedLua51, legacy_source_observation
import test_store_write_boundaries as store_fixture
import test_b236_crews as crew_cases
from test_refactor_s4b import culture


SETUP=r'''
include=function()end;print=function()end
P={VERSION='S6H',IsTestPlayer=function(pid)return pid==0 end,Field=function(t,k)return t and t[k]end,CrewBase=function(k)if k=='UNIT_SPC_CREW_250'then return 250 end end};SPCP0=P
function event()local e={listeners={}};function e.Add(f)e.listeners[f]=true end;function e.Remove(f)e.listeners[f]=nil end;function e.Fire(...)for f in pairs(e.listeners)do f(...)end end;return e end
Events=setmetatable({},{__index=function(t,k)local e=event();rawset(t,k,e);return e end})
LuaEvents={SPC_ToggleBuilderTargets=event()}
GameInfo={Units={[1]={UnitType='UNIT_SPC_CREW_250'},[2]={UnitType='UNIT_SETTLER'},[3]={UnitType='UNIT_GREAT_SCIENTIST',GreatPersonClass='SCIENCE'},[4]={UnitType='UNIT_BUILDER'}}}
counts={getters=0,selected=0,layout=0,lens=0,clears=0,requests=0};requests={};queued={};plan=nil;confirmed=0;autoReply=true;turn=1;localPlayer=0;mode=1
function makeUnit(id,kind,owner)
 local u={id=id,kind=kind or 1,owner=owner or 0,x=2,y=3}
 for name,field in pairs({GetID='id',GetType='kind',GetOwner='owner',GetX='x',GetY='y'})do u[name]=function(self)counts.getters=counts.getters+1;return self[field]end end
 return u
end
units={[7]=makeUnit(7),[8]=makeUnit(8,2),[9]=makeUnit(9,3),[10]=makeUnit(10,4),[11]=makeUnit(11,1,1)};selected=units[7]
ExposedMembers={SPC_P0={Version=P.VERSION}}
Game={GetLocalPlayer=function()return localPlayer end,GetCurrentGameTurn=function()counts.getters=counts.getters+1;return turn end}
InterfaceModeTypes={SELECTION=1};PlayerOperations={EXECUTE_SCRIPT=1};Mouse={eLClick=1};Locale={Lookup=function(k)return k end}
parent={CalculateSize=function()counts.layout=counts.layout+1;if layoutFailure then error('LAYOUT_FAILURE')end end,ReprocessAnchoring=function()counts.layout=counts.layout+1 end}
Controls=setmetatable({},{__index=function(t,k)local c={
 SetHide=function(self,v)self.hide=v end,SetDisabled=function(self,v)self.disabled=v end,SetSizeX=function(self,v)self.width=v end,SetOffsetX=function(self,v)self.offset=v end,
 SetIcon=function(self,v,n)self.icon=v;self.cell=n;if iconFailure then error('ICON_FAILURE')end end,SetToolTipString=function(self,v)self.tip=v end,
 ChangeParent=function(self,p)self.parent=p end,RegisterCallback=function(self,_,f)self.click=f end};t[k]=c;return c end})
ContextPtr={SetInitHandler=function(_,f)init=f end,SetShutdown=function(_,f)shutdown=f end,SetUpdate=function(_,f)tick=f end,ClearUpdate=function()tick=nil end,SetHide=function()end,LookUpControl=function()if not missingParent then return parent end end}
UILens={CreateLensLayerHash=function()return 1 end,ClearLayerHexes=function()counts.clears=counts.clears+1;if lensFailure then error('LENS_FAILURE')end end,ToggleLayerOff=function()end,SetLayerHexesColoredArea=function(_,owner,plots)counts.lens=counts.lens+1;painted=plots;if lensFailure then error('LENS_FAILURE')end end,ToggleLayerOn=function()end}
PlayersVisibility={[0]={IsVisible=function(_,id)return id~=999 end}}
function clone(v)if type(v)~='table'then return v end;local n={};for k,x in pairs(v)do n[k]=clone(x)end;return n end
function reply(p)
 local s=ExposedMembers.SPC_P0;local u=units[p.UnitID]
 if p.Action=='UNIT_ACTION_VIEW'then
  local v={owner=u.owner,unitID=u.id,token=p.Token,turn=turn,x=u.x,y=u.y,legal=true,prepared=plan~=nil,planToken=plan,amount=250,baseInput=100,baseUnused=0,progress=20,cost=400,targetName='WONDER',specialization='RESEARCH',potential=1,nextPotential=2}
  if p.ReplyChannel and not s.PlayerActionReplies.Views.Accepts(u.owner,p)then return end
  if mutateReply then mutateReply(v)end;s.UnitActionView=v
  if p.ReplyChannel then local port=s.PlayerActionReplies.Views;if not port.PublishView(u.owner,p,v)then port.FailView(u.owner,p)end end
 elseif p.Action=='UNIT_TARGETS_READ'then
  local v={version=P.VERSION,owner=u.owner,unitID=u.id,token=p.Token,turn=turn,x=u.x,y=u.y,mode='INVEST',plots={{plot=10},{plot=999}},unknown={}}
  if p.ReplyChannel and not s.PlayerActionReplies.Targets.Accepts(u.owner,p)then return end
  if mutateReply then mutateReply(v)end;s.UnitTargetSnapshot=v
  if p.ReplyChannel then local port=s.PlayerActionReplies.Targets;if not port.PublishTargets(u.owner,p,v)then port.FailTargets(u.owner,p)end end
 elseif p.Action=='UNIT_ACTION_PREPARE'then
  if p.ReplyChannel and not s.PlayerActionReplies.Accepts(u.owner,p)then return end
  plan='PLAN';s.UnitActionPreview={owner=u.owner,unitID=u.id,turn=turn,x=u.x,y=u.y,token=plan}
  if p.ReplyChannel then s.PlayerActionReplies.Publish(u.owner,p,'PREPARED',{status='PREPARED',kind='UNIT_ACTION',phase='PREPARE'})else s.LastToken=p.Token;s.Snapshot='PREPARED'end
 elseif p.Action=='UNIT_ACTION_CONFIRM'then
  if p.ReplyChannel and not s.PlayerActionReplies.Accepts(u.owner,p)then return end
  assert(p.PlanToken==plan and plan);confirmed=confirmed+1;plan=nil;s.UnitActionPreview=nil
  if p.ReplyChannel then s.PlayerActionReplies.Publish(u.owner,p,'DONE',{status='COMMITTED',kind='UNIT_ACTION',phase='CONFIRM'})else s.LastToken=p.Token;s.Snapshot='DONE'end
 end
end
UI={GetHeadSelectedUnit=function()counts.selected=counts.selected+1;return selected end,GetInterfaceMode=function()return mode end,GetColorValue=function()return 1 end,
 RequestPlayerOperation=function(pid,op,p)
  assert(pid==localPlayer and op==1 and p.OnStart=='SPC_P0_Request');counts.requests=counts.requests+1;requests[#requests+1]=clone(p)
  if dispatchFailure then error('DISPATCH_FAILURE')end
  if autoReply then reply(p)else queued[#queued+1]=clone(p)end
  if duringRequest then duringRequest(p)end
  if returnFalse then return false end
 end}
function publish()Events.GameCoreEventPublishComplete.Fire()end
function selectedChanged()Events.UnitSelectionChanged.Fire(selected and selected.owner,selected and selected.id)end
function resetCounts()for k in pairs(counts)do counts[k]=0 end end
function actionCount(kind)local n=0;for _,p in ipairs(requests)do if p.Action==kind then n=n+1 end end;return n end
function idle(n)for i=1,n do if tick then tick(.3)end;publish()end end
function deliver()local q=queued;queued={};for _,p in ipairs(q)do reply(p)end;publish()end
'''


def ui(markers=False,before=""):
    c=Context('unit-target-ui'if markers else'unit-action-ui');c.execute(SETUP);c.load('PlayerActionReplies');c.execute('SPCPlayerActionReplies.Start(P,ExposedMembers.SPC_P0)');c.execute(before)
    c.load('UI/UnitTargetMarkers'if markers else'UI/UnitPanelActions');c.execute('init()');return c


class Panel(unittest.TestCase):
    def test_current_raw_icons_and_two_step_packets_stay_unchanged(self):
        for kind,base in ((1,'CREW'),(2,'INVEST')):
            c=ui();c.execute("selected.kind="+str(kind)+";selectedChanged();assert(Controls.PrepareIcon.icon=='ICON_SPC_RAW_"+base+"_PREPARE'and Controls.ConfirmIcon.icon=='ICON_SPC_RAW_"+base+"_CONFIRM'and Controls.PrepareIcon.cell==38);assert(Controls.ConfirmButton.hide);Controls.PrepareButton.click();Controls.PrepareButton.click();publish();assert(not Controls.ConfirmButton.hide and actionCount('UNIT_ACTION_PREPARE')==1);Controls.ConfirmButton.click();Controls.ConfirmButton.click();publish();assert(confirmed==1 and actionCount('UNIT_ACTION_CONFIRM')==1)")

    def test_synchronous_read_and_deferred_read_are_consumed_without_tick_poll(self):
        c=ui();c.execute("assert(not Controls.ActionGroup.hide and Controls.PrepareIcon.icon=='ICON_SPC_RAW_CREW_PREPARE');autoReply=false;Events.CityProductionChanged.Fire(0,1);publish();local n=counts.requests;assert(#queued==1);resetCounts();idle(3);assert(counts.getters==0 and counts.requests==0);deliver();assert(counts.getters>0 and counts.requests==0)")

    def test_idle_and_known_foreign_events_do_zero_unit_or_layout_work(self):
        c=ui();c.execute("resetCounts();for i=1,1000 do Events.CityProductionChanged.Fire(1,1);Events.UnitMoveComplete.Fire(1,7);idle(1)end;assert(counts.getters==0 and counts.selected==0 and counts.requests==0 and counts.layout==0)")
        measure('S6h_panel_idle',{'idle_publishes':1000,'scalar_ticks':1000,'unit_getters':0,'requests':0,'layout':0,'known_foreign_signals':2000})

    def test_one_change_coalesces_then_does_not_publish_poll_waiting_action(self):
        c=ui();c.execute("autoReply=false;Controls.PrepareButton.click();for i=1,50 do Events.CityProductionChanged.Fire(0,1)end;publish();resetCounts();for i=1,1000 do publish()end;assert(counts.getters==0 and counts.selected==0 and counts.requests==0);deliver();assert(actionCount('UNIT_ACTION_PREPARE')==1)")

    def test_read_reply_wrong_stamp_is_dropped_once_without_new_read(self):
        for mutation in ('v.owner=1','v.unitID=99','v.turn=9','v.x=99','v.y=99'):
            c=ui();c.execute("autoReply=false;selectedChanged();mutateReply=function(v)"+mutation+" end;deliver();assert(Controls.ConfirmButton.hide);resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0)")

    def test_unrelated_reply_and_lost_action_ack_never_replay(self):
        c=ui();c.execute("autoReply=false;Controls.PrepareButton.click();local sent=requests[#requests].Token;ExposedMembers.SPC_P0.LastToken='OTHER';ExposedMembers.SPC_P0.Snapshot='OTHER';publish();resetCounts();for i=1,1000 do publish()end;assert(counts.getters==0 and counts.requests==0);tick(11);publish();assert(actionCount('UNIT_ACTION_PREPARE')==1 and actionCount('UNIT_ACTION_CONFIRM')==0);resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0)")

    def test_selection_mode_movement_and_turn_invalidate_without_implicit_polling(self):
        c=ui();c.execute("Controls.PrepareButton.click();publish();assert(not Controls.ConfirmButton.hide);selected=units[9];selectedChanged();assert(Controls.ActionGroup.hide);selected=units[8];selectedChanged();assert(not Controls.ActionGroup.hide and Controls.ConfirmButton.hide);mode=2;Events.InterfaceModeChanged.Fire();assert(Controls.ActionGroup.hide);mode=1;Events.InterfaceModeChanged.Fire();selected.x=8;Events.UnitMoveComplete.Fire(0,8);assert(Controls.ConfirmButton.hide);turn=2;Events.LocalPlayerTurnBegin.Fire();publish();assert(Controls.ConfirmButton.hide and confirmed==0)")

    def test_backend_replacement_and_wrong_version_cannot_accept_old_reply(self):
        c=ui();c.execute("autoReply=false;selectedChanged();local old=ExposedMembers.SPC_P0;ExposedMembers.SPC_P0={Version='OTHER',UnitActionView=old.UnitActionView,PlayerActionReplies=old.PlayerActionReplies};publish();assert(Controls.ConfirmButton.hide);local n=counts.requests;ExposedMembers.SPC_P0.Version=P.VERSION;publish();assert(counts.requests==n+1);deliver();assert(Controls.ConfirmButton.hide)")

    def test_synchronous_backend_or_selection_reentry_never_shows_old_confirmation(self):
        for code in ("ExposedMembers.SPC_P0=clone(ExposedMembers.SPC_P0)","selected=units[9];selectedChanged()"):
            c=ui();c.execute("duringRequest=function(p)if p.Action=='UNIT_ACTION_VIEW'then duringRequest=nil;"+code+" end end;Events.CityProductionChanged.Fire(0,1);publish();assert(Controls.ConfirmButton.hide and confirmed==0)")

    def test_error_timeout_and_missing_parent_wait_for_new_evidence(self):
        c=ui();c.execute("dispatchFailure=true;Events.CityProductionChanged.Fire(0,1);publish();resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0);dispatchFailure=false;iconFailure=true;selectedChanged();resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0);iconFailure=false;selectedChanged();assert(not Controls.ActionGroup.hide)")
        c=ui(before='missingParent=true');c.execute("resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0);missingParent=false;Events.LoadScreenClose.Fire();assert(counts.requests==1);shutdown();assert(tick==nil);for _,e in pairs(Events)do assert(not next(e.listeners))end")

    def test_false_dispatch_return_and_wrong_read_token_do_not_resend(self):
        c=ui();c.execute("autoReply=false;returnFalse=true;Controls.PrepareButton.click();publish();resetCounts();for i=1,1000 do publish()end;assert(counts.requests==0 and counts.getters==0);tick(11);publish();assert(actionCount('UNIT_ACTION_PREPARE')==1)")
        c=ui();c.execute("autoReply=false;selectedChanged();mutateReply=function(v)v.token='WRONG'end;deliver();resetCounts();for i=1,1000 do publish()end;assert(counts.getters==0 and counts.requests==0);tick(3);publish();resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")

    def test_new_cause_during_control_error_survives_for_one_publish(self):
        c=ui();c.execute("local set=Controls.PrepareIcon.SetIcon;local once=true;Controls.PrepareIcon.SetIcon=function(...)if once then once=false;Events.CityProductionChanged.Fire(0,1);error('CONTROL_FAIL_WITH_NEW_CAUSE')end;return set(...)end;selected=units[8];selectedChanged();assert(not once);resetCounts();publish();assert(counts.requests==1);resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0)")


class Markers(unittest.TestCase):
    def test_sync_reply_visibility_filter_and_idle_zero_native_work(self):
        c=ui(True);c.execute("assert(counts.lens==1 and #painted==1 and painted[1]==10);resetCounts();idle(1000);assert(counts.getters==0 and counts.selected==0 and counts.requests==0 and counts.lens==0 and counts.clears==0)")
        measure('S6h_markers_idle',{'idle_publishes':1000,'scalar_ticks':1000,'unit_getters':0,'requests':0,'lens_operations':0})

    def test_deferred_stale_stamp_and_timeout_no_resend(self):
        for mutation in ("v.version='BAD'",'v.owner=1','v.unitID=99','v.turn=2','v.x=99','v.y=99'):
            c=ui(True);c.execute("autoReply=false;selectedChanged();mutateReply=function(v)"+mutation+" end;deliver();resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0 and counts.lens==0)")
        c=ui(True);c.execute("autoReply=false;selectedChanged();resetCounts();tick(11);publish();resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0)")

    def test_toggle_selection_and_mode_are_immediate_ui_events(self):
        c=ui(True);c.execute("selected=units[10];selectedChanged();local n=counts.requests;LuaEvents.SPC_ToggleBuilderTargets.Fire();assert(counts.requests==n+1 and requests[#requests].BuilderPreview);mode=2;Events.InterfaceModeChanged.Fire();assert(counts.clears>0);local n=counts.requests;mode=1;Events.InterfaceModeChanged.Fire();assert(counts.requests==n+1)")

    def test_native_great_person_layer_survives_selected_unit_change(self):
        c=ui(True);c.execute("local n=counts.clears;selected=units[9];selectedChanged();assert(counts.clears==n);resetCounts();idle(1000);assert(counts.clears==0 and counts.getters==0)")

    def test_known_foreign_changes_zero_work_one_local_cause_one_read(self):
        c=ui(True);c.execute("resetCounts();for i=1,1000 do Events.CityProductionChanged.Fire(1,1);Events.UnitMoveComplete.Fire(1,7);publish()end;assert(counts.getters==0 and counts.requests==0);for i=1,50 do Events.CityProductionChanged.Fire(0,1)end;publish();assert(counts.requests==1);resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0)")

    def test_synchronous_reentry_backend_and_selection_cannot_paint_old_reply(self):
        for code in ("ExposedMembers.SPC_P0=clone(ExposedMembers.SPC_P0)","selected=units[9];selectedChanged()"):
            c=ui(True);c.execute("duringRequest=function()duringRequest=nil;"+code+" end;resetCounts();Events.CityProductionChanged.Fire(0,1);publish();assert(counts.lens==0)")

    def test_render_throw_releases_guard_no_idle_retry_and_shutdown_removes_hooks(self):
        c=ui(True);c.execute("lensFailure=true;selectedChanged();resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0);lensFailure=false;selectedChanged();assert(counts.lens==1);shutdown();assert(tick==nil and not next(LuaEvents.SPC_ToggleBuilderTargets.listeners));for _,e in pairs(Events)do assert(not next(e.listeners))end;resetCounts();publish();assert(counts.getters==0 and counts.requests==0)")

    def test_new_cause_during_lens_error_is_not_dropped_or_idle_retried(self):
        c=ui(True);c.execute("local set=UILens.SetLayerHexesColoredArea;local once=true;UILens.SetLayerHexesColoredArea=function(...)if once then once=false;Events.CityProductionChanged.Fire(0,1);error('LENS_FAIL_WITH_NEW_CAUSE')end;return set(...)end;selectedChanged();resetCounts();publish();assert(counts.requests==1 and counts.lens==1);resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0)")


class ActualProfile:
    def setUp(self):
        self.old=store_fixture.LuaRuntime;store_fixture.LuaRuntime=TrackedLua51
        self.observation=legacy_source_observation();self.observation.__enter__()
    def tearDown(self):
        self.observation.__exit__(None,None,None);store_fixture.LuaRuntime=self.old


class ActualConsumption(ActualProfile,crew_cases.Consumption):
    """Unchanged actual Store/Crew/UnitActions money and single-use assertions."""


class ActualTargets(ActualProfile,crew_cases.ActualTargets):
    """Actual target response and original wonder/ownership assertions."""
    def test_actual_producer_stamps_current_request_unit(self):
        l=crew_cases.crew_runtime()
        with legacy_source_observation():l.globals().include('UnitTargets')
        l.execute("local c=C.make();local p=C.begin(c);C.complete(c,p);SPCUnitTargets.Start(P,shared);shared.UnitTargets.Refresh(0,{UnitID=20001,Token='STAMP'});local u=C.units[20001];local s=shared.UnitTargetSnapshot;assert(s.token=='STAMP'and s.version==P.VERSION and s.unitID==u:GetID()and s.owner==u:GetOwner()and s.turn==Game.GetCurrentGameTurn()and s.x==u:GetX()and s.y==u:GetY())")


class ExistingCapitalScope(unittest.TestCase):
    def test_real_bridge_multi_kind_reads_do_not_capture_or_refresh(self):
        l=culture();l.execute("local n=counts.city_scan;local derive=counts.derive;local refresh=net.Refresh;net.Refresh=function()error('QUOTE_MUST_NOT_CAPTURE')end;for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY'})do local ids=net.CurrentCapitalSources(0,cities[2],kind);if kind=='CULTURE'then assert(#ids==1 and ids[1]==4)end end;assert(counts.city_scan==n and counts.derive==derive);net.Refresh=refresh;net.CheckEvidence(false);assert(not pcall(net.CurrentCapitalSources,0,cities[2],'CULTURE'))")


if __name__=='__main__':unittest.main()
