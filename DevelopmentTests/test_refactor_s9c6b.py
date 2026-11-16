"""One typed presentation consumer; accepted UI handoff to actual Overview/Institutions."""
from pathlib import Path
from unittest.mock import patch
import json,unittest
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,measure
import test_culture_institutions as display_cases
import test_b265_city_presentation as prior
import test_b266_institution_recovery as recovery
import test_b251_institutions as institutions

class UIProfile:
 def setUp(self):
  self.old=display_cases.LuaRuntime;display_cases.LuaRuntime=TrackedLua51
  self.observation=legacy_source_observation();self.observation.__enter__()
 def tearDown(self):
  self.observation.__exit__(None,None,None);display_cases.LuaRuntime=self.old

class Consumer(UIProfile,unittest.TestCase):
 def test_global_mirror_cannot_change_either_typed_consumer(self):
  l=prior.presentation();l.execute("local v={owner=0,cityID=4,x=8,y=9,specialization='CULTURE',potential=4,active=4,activeStatus='KNOWN'};ExposedMembers.SPC_P0.CityPresentationView=v;LuaEvents.SPC_PresentationChanged();Events.GameCoreEventPublishComplete();ViewPanelBreakdown(data);assert(rows.items[4].State.text=='未激活'and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_3'and #requests==1)")
 def test_two_same_city_tokens_are_independent_and_old_reply_cannot_override_new(self):
  l=prior.presentation();l.execute("deferred=true;nativeActive=4;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete();local a=requests[#requests];nativeActive=2;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete();local b=requests[#requests];assert(a.Token~=b.Token);publishPresentation(a,{owner=0,cityID=4,x=8,y=9,token=a.Token,specialization='CULTURE',potential=4,active=4,activeStatus='KNOWN'});Events.GameCoreEventPublishComplete();assert(rows.items[4].State.text=='未激活');reply(b);Events.GameCoreEventPublishComplete();assert(rows.items[2].State.text=='当前'and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_2');reply(a);Events.GameCoreEventPlaybackComplete();assert(rows.items[2].State.text=='当前'and #requests==3)")
 def test_one_Take_serves_both_displays_and_Ready_replays_without_read_or_request(self):
  l=prior.presentation();l.execute("local port=ExposedMembers.SPC_P0.PlayerActionReplies.Presentations;local take=port.Take;local takes=0;port.Take=function(...)takes=takes+1;return take(...)end;nativeActive=4;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete();assert(takes==1 and rows.items[4].State.text=='当前'and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_4');local n=#requests;for i=1,1000 do LuaEvents.SPC_PresentationConsumerReady();Events.GameCoreEventPublishComplete()end;assert(takes==1 and #requests==n)")
  measure('S9c6b_dual_consumer',{'Take_per_received_reply':1,'UI_consumers':2,'thousand_Ready_or_idle_extra_requests':0,'DEV_global_consumed':False})
 def test_negative_without_coordinates_retains_rows_as_unknown_and_never_zero(self):
  l=prior.presentation();l.execute("deferred=true;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete();local p=requests[#requests];assert(ExposedMembers.SPC_P0.PlayerActionReplies.Presentations.FailPresentation(0,p));Events.GameCoreEventPublishComplete();assert(#rows.items==4 and rows.items[4].State.text=='待确认'and rows.items[4].Top.tip:find('当前数值待确认',1,true)and Controls.ActiveShortcut.hidden);local n=#requests;for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(#requests==n)")
 def test_equal_backend_restart_does_not_accept_old_epoch_and_clears_pending_rows(self):
  l=prior.presentation();l.execute("deferred=true;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete();local old=requests[#requests];local before=ExposedMembers.SPC_P0;newPresentationBackend({LevelBanners=before.LevelBanners});Events.GameCoreEventPlaybackComplete();local fresh=requests[#requests];assert(old.ReplyEpoch~=fresh.ReplyEpoch and Controls.InstitutionContainer.hidden);reply(old);Events.GameCoreEventPublishComplete();assert(Controls.InstitutionContainer.hidden);reply(fresh);Events.GameCoreEventPublishComplete();assert(#rows.items==4 and rows.items[4].State.text=='未激活')")
 def test_overview_late_load_replays_existing_accepted_data_without_Gameplay_request(self):
  path=ROOT/'Mod/UI/InstitutionOverview.lua';read=Path.read_text
  with patch.object(Path,'read_text',lambda p,*a,**kw:''if p==path else read(p,*a,**kw)):
   l=prior.presentation()
  l.execute("local n=#requests;assert(n==1);beforeLate=n;ContextPtr.LookUpControl=function(_,path)if path:find('CityPanelOverview',1,true)then return parent end;return actionParent end")
  l.execute(path.read_text());l.execute("ViewPanelBreakdown(data);assert(#requests==beforeLate and rows.items[4].State.text=='未激活'and not Controls.InstitutionContainer.hidden)")
 def test_hidden_overview_uses_cached_accepted_update_when_opened(self):
  l=prior.presentation();l.execute("Controls.PanelBreakdown:SetHide(true);nativeActive=1;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete();local n=#requests;Controls.PanelBreakdown:SetHide(false);ViewPanelBreakdown(data);assert(#requests==n and rows.items[1].State.text=='当前'and rows.items[4].State.text=='未激活')")
 def test_old_native_render_cannot_overwrite_new_typed_delivery_during_reentry(self):
  l=prior.presentation();l.execute("local once=true;duringNative=function()if once then once=false;nativeActive=1;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete()end end;ViewPanelBreakdown(data);assert(not once and #requests==2 and rows.items[1].State.text=='当前'and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_1');Events.GameCoreEventPublishComplete();assert(rows.items[1].State.text=='当前')")
 def test_shutdown_during_native_stamp_releases_wait_and_late_button_sends_nothing(self):
  l=prior.presentation();l.execute("deferred=true;local port=ExposedMembers.SPC_P0.PlayerActionReplies.Presentations;local take=port.Take;local armed=false;port.Take=function(...)local row=take(...);armed=true;return row end;local get=city.GetX;city.GetX=function(c)if armed then armed=false;stopBridge()end;return get(c)end;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete();local p=requests[#requests];reply(p);Events.GameCoreEventPublishComplete();local n=#requests;assert(Controls.ActiveShortcut.hidden and port.Count()==0);Controls.ActiveShortcut.click();LuaEvents.SPC_PresentationConsumerReady();Events.GameCoreEventPublishComplete();assert(#requests==n and Controls.ActiveShortcut.hidden)")
 def test_shutdown_from_icon_does_not_resume_size_or_shortcut_visibility(self):
  l=prior.presentation();l.execute("local icon=Controls.ActiveIcon.SetIcon;local sizes=0;Controls.ActiveIcon.SetIcon=function(...)icon(...);stopBridge()end;Controls.ActiveIcon.SetSizeVal=function()sizes=sizes+1 end;nativeActive=4;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete();assert(sizes==0 and Controls.ActiveShortcut.hidden);local n=#requests;Controls.ActiveShortcut.click();assert(#requests==n)")
 def test_older_UI_context_reset_cannot_clear_current_accepted_packet(self):
  l=prior.presentation();l.execute("LuaEvents.SPC_PresentationChanged({status='RESET',sourceSequence=0,version='B265'});assert(#rows.items==4 and rows.items[4].State.text=='未激活');LuaEvents.SPC_PresentationConsumerReady();assert(rows.items[4].State.text=='未激活'and #requests==1)")
 def test_evicted_or_bad_metadata_does_not_retry_or_read_global(self):
  for corruption in ('EVICT','BAD'):
   l=prior.presentation();l.execute("deferred=true;local port=ExposedMembers.SPC_P0.PlayerActionReplies.Presentations;local take=port.Take;local mode=...;if mode=='BAD'then port.Take=function(...)local r=take(...);if r then r.owner=1 end;return r end end;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete();local p=requests[#requests];reply(p);if mode=='EVICT'then for i=1,8 do local q={ReplyChannel=p.ReplyChannel,ReplyEpoch=p.ReplyEpoch,Action=p.Action,CityID=p.CityID,Token='OTHER'..i};assert(port.FailPresentation(0,q))end end;Events.GameCoreEventPublishComplete();local n=#requests;for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(#requests==n)",corruption)

 def test_source_close_during_READY_delivery_cannot_reanimate_Overview(self):
  l=prior.presentation();l.execute("local e=LuaEvents.SPC_PresentationChanged;local receiver=e.f;local once=true;e.f=function(packet)if once and packet and packet.status=='READY'then once=false;stopBridge()end;return receiver(packet)end;nativeActive=2;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete();assert(Controls.ActiveShortcut.hidden and Controls.InstitutionContainer.hidden and #rows.items==0);local n=#requests;for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(#requests==n)")
 def test_busy_native_read_new_cause_survives_and_sends_once_next_boundary(self):
  l=prior.presentation();l.execute("local once=true;UI.IsGameCoreBusy=function()if once then once=false;nativeActive=2;Events.GovernorPromoted(0)end;return false end;local n=#requests;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete();assert(#requests==n);Events.GameCoreEventPublishComplete();assert(#requests==n+1 and rows.items[2].State.text=='当前');for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(#requests==n+1)")
 def test_newer_RESET_during_delivery_rejects_older_READY_same_source(self):
  l=prior.presentation();l.execute("local e=LuaEvents.SPC_PresentationChanged;local receiver=e.f;local once=true;e.f=function(packet)if once and packet and packet.status=='READY'then once=false;city=nil;Events.CitySelectionChanged();receiver({status='RESET',sourceSequence=packet.sourceSequence,deliverySequence=packet.deliverySequence+1,version=packet.version})end;return receiver(packet)end;nativeActive=2;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete();city={GetOwner=function()return 0 end,GetID=function()return 4 end,GetX=function()return 8 end,GetY=function()return 9 end};ViewPanelBreakdown(data);assert(Controls.InstitutionContainer.hidden)")

 def test_READY_replay_reentry_with_new_real_typed_result_cannot_restore_old_values(self):
  l=prior.presentation();l.execute("local e=LuaEvents.SPC_PresentationChanged;local receiver=e.f;local once=true;e.f=function(packet)if once and packet and packet.status=='READY'then once=false;nativeActive=2;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete()end;return receiver(packet)end;LuaEvents.SPC_PresentationConsumerReady();assert(#requests==2 and rows.items[2].State.text=='当前'and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_2');for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(rows.items[2].State.text=='当前'and #requests==2)")
 def test_same_port_method_replacement_invalidates_and_observes_once(self):
  l=prior.presentation();l.execute("local d=ExposedMembers.SPC_P0.PlayerActionReplies.Presentations;local take=d.Take;d.Take=function(...)return take(...)end;local n=#requests;Events.GameCoreEventPublishComplete();assert(#requests==n+1 and rows.items[4].State.text=='未激活');for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(#requests==n+1)")

 def test_identical_ready_replay_during_native_render_is_idempotent(self):
  l=prior.presentation();l.execute("local once=true;duringNative=function()if once then once=false;LuaEvents.SPC_PresentationConsumerReady()end end;nativeActive=2;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete();assert(not once and rows.items[2].State.text=='当前'and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_2');local n=#requests;for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(rows.items[2].State.text=='当前'and #requests==n)")

class EventPresentation(UIProfile,prior.EventPresentation):pass
class NativeOverview(UIProfile,prior.NativeOverview):pass
class PresentationContract(UIProfile,prior.PresentationContract):pass
class NewCityLifecycle(UIProfile,recovery.NewCityLifecycle):pass
class ExceptionRelease(UIProfile,recovery.ExceptionRelease):pass
class CultureDisplay(UIProfile,display_cases.CultureInstitutionDisplay):pass
class InstitutionDisplay(UIProfile,institutions.Presentation):pass


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9c6a'])])

if __name__=='__main__':unittest.main()
