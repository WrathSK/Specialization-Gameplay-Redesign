"""B265 actual consumer Lua, isolated native event/control boundary. No game PASS."""
from pathlib import Path
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
from test_culture_institutions import display
from test_expedition_training_ui import ui
R=Path(__file__).resolve().parents[1]


def presentation(setup=None):
 l=display()
 l.execute("""
  function event()
   local e={handlers={}}
   function e.Add(f)e.handlers[#e.handlers+1]=f end
   function e.Remove(f)for i=#e.handlers,1,-1 do if e.handlers[i]==f then table.remove(e.handlers,i)end end end
   return setmetatable(e,{__call=function(_,...)for _,f in ipairs(e.handlers)do f(...)end end})
  end
  Events=setmetatable({},{__index=function(t,k)local e=event();t[k]=e;return e end})
  LuaEvents.CityPanel_LiveCityDataChanged=event();LuaEvents.SPC_OpenInstitutions=event()
  local function control()
   local c={hidden=true}
   function c:SetHide(v)self.hidden=v end
   function c:SetIcon(v,n)self.icon=v;self.cell=n end
   function c:SetSizeVal(w,h)self.w=w;self.h=h end
   function c:SetToolTipString(v)self.tip=v end
   function c:ChangeParent(v)self.parent=v end
   function c:RegisterCallback(_,f)self.click=f end
   function c:CalculateSize()layouts=layouts+1 end
   function c:ReprocessAnchoring()end
   function c:GetParent()return self.parent end
   function c:DestroyChild(v)self.destroyed=v end
   return c
  end
  layouts=0;actionParent=control();actionParent.parent=control();actionParent.parent.parent=control()
  actionParent.parent.CalculateSize=nil
  actionParent.parent.DoAutoSize=function()layouts=layouts+1 end
  Controls.ActiveShortcut=control();Controls.ActiveIcon=control()
  ContextPtr={SetHide=function()end,LookUpControl=function()if not missingParent then return actionParent end end,
   SetInitHandler=function(_,f)startBridge=f end,SetShutdown=function(_,f)stopBridge=f end}
  Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=1}
  SPCP0={VERSION='B265',IsTestPlayer=function(pid)return pid==0 end}
  trace={};SPCExpeditionTrainingDiagnostics={New=function()return {Record=function(stage,s)trace[#trace+1]={stage=stage,s=s}end}end}
  turn=1;nativeActive=3;nativePotential=4;Game.GetCurrentGameTurn=function()return turn end
  UI.IsGameCoreBusy=function()return coreBusy end
  ExposedMembers.SPC_RuntimeUIRevision=0
  ExposedMembers.SPC_P0.LevelBanners={revision=1,views={['0:4']={specialization='CULTURE',active=3,potential=4,activeStatus='KNOWN'}}}
  requests={}
  function reply(p)
   local q={owner=0,cityID=p.CityID,x=8,y=9,token=p.Token,specialization='CULTURE',
    active=nativeActive,potential=nativePotential,activeStatus='KNOWN',institutionSummary={known=true,dialogue=0,insights=0}}
   ExposedMembers.SPC_P0.CityPresentationView=q
  end
  UI.RequestPlayerOperation=function(pid,op,p)
   requests[#requests+1]=p;if throwing then error('send failed')end
   if not deferred then reply(p)end
  end
 """)
 l.execute((R/'Mod/UI/LevelBannerModel.lua').read_text())
 if setup:l.execute(setup)
 l.execute((R/'Mod/UI/CityPotential.lua').read_text())
 l.execute('startBridge()')
 return l


class EventPresentation(unittest.TestCase):
 def test_consecutive_promotions_same_turn_without_writes_update_institutions(self):
  presentation().execute("""
   assert(rows.items[4].State.text=='未激活' and #requests==1)
   nativeActive=4;Events.GovernorPromoted(0);Events.GovernorPromoted(0);Events.GovernorPromoted(0)
   assert(#requests==1)
   Events.GameCoreEventPublishComplete()
   assert(#requests==2 and rows.items[4].State.text=='当前')
   assert(Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_4')
   assert(ExposedMembers.SPC_RuntimeUIRevision==0 and turn==1)
  """)
 def test_later_banner_publication_and_potential_only_change(self):
  presentation().execute("""
   Events.GameCoreEventPublishComplete();assert(#requests==1)
   nativeActive=4;ExposedMembers.SPC_P0.LevelBanners.views['0:4'].active=4
   Events.GameCoreEventPlaybackComplete();assert(#requests==2 and rows.items[4].State.text=='当前')
   nativeActive=1;nativePotential=1;local f=ExposedMembers.SPC_P0.LevelBanners.views['0:4'];f.active=1;f.potential=1
   Events.GameCoreEventPublishComplete();assert(rows.items[2].State.text=='尚未建立')
   nativePotential=2;f.potential=2;Events.GameCoreEventPlaybackComplete()
   assert(rows.items[2].State.text=='未激活')
  """)
 def test_idle_boundaries_foreign_events_and_unrelated_city_zero_requests(self):
  presentation().execute("""
   local n=#requests;local sizes=layouts
   for i=1,1000 do Events.GameCoreEventPublishComplete();Events.GameCoreEventPlaybackComplete();Events.GovernorPromoted(1)end
   assert(#requests==n and layouts==sizes)
   ExposedMembers.SPC_P0.LevelBanners.revision=99
   ExposedMembers.SPC_P0.LevelBanners.views['0:99']={active=4}
   Events.GameCoreEventPublishComplete();assert(#requests==n)
  """)
 def test_busy_defers_read_until_event_and_coalesces_notifications(self):
  presentation().execute("""
   coreBusy=true;nativeActive=4
   Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete();Events.GameCoreEventPlaybackComplete()
   assert(#requests==1)
   coreBusy=false;Events.GameCoreEventPlaybackComplete();assert(#requests==2 and rows.items[4].State.text=='当前')
  """)
 def test_late_reply_after_city_switch_or_deselection_never_applies(self):
  presentation().execute("""
   deferred=true;nativeActive=4;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete();local old=requests[#requests]
   city={GetOwner=function()return 0 end,GetID=function()return 7 end,GetX=function()return 3 end,GetY=function()return 4 end}
   Events.CitySelectionChanged();reply(old);Events.GameCoreEventPublishComplete()
   assert(Controls.ActiveShortcut.hidden)
   city=nil;Events.CitySelectionChanged();local n=#requests
   for i=1,20 do Events.GameCoreEventPublishComplete()end
   assert(#requests==n and Controls.ActiveShortcut.hidden)
  """)
 def test_missing_reply_has_no_poll_retry_and_new_semantic_event_recovers(self):
  presentation().execute("""
   deferred=true;nativeActive=4;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete()
   for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(#requests==2)
   deferred=false;Events.GovernorEstablished(0);Events.GameCoreEventPublishComplete()
   assert(#requests==3 and rows.items[4].State.text=='当前')
  """)
 def test_unavailable_backend_waits_without_requests_then_rebinds(self):
  presentation().execute("""
   local saved=ExposedMembers.SPC_P0;ExposedMembers.SPC_P0=nil
   for i=1,1000 do Events.GameCoreEventPublishComplete()end
   assert(#requests==1 and Controls.ActiveShortcut.hidden)
   ExposedMembers.SPC_P0=saved;Events.GameCoreEventPlaybackComplete();assert(#requests==2 and not Controls.ActiveShortcut.hidden)
  """)
 def test_reload_equal_values_and_unknown_reply_do_not_reuse_foreign_state(self):
  presentation().execute("""
   local prior=ExposedMembers.SPC_P0;ExposedMembers.SPC_P0={LevelBanners=prior.LevelBanners}
   Events.GameCoreEventPlaybackComplete();assert(#requests==2)
   deferred=true;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete()
   ExposedMembers.SPC_P0.CityPresentationView={owner=0,cityID=4,token=requests[#requests].Token,error='UNKNOWN'}
   Events.GameCoreEventPlaybackComplete();assert(Controls.ActiveShortcut.hidden and rows.items[4].State.text=='待确认')
  """)
 def test_shortcut_uses_current_active_local_city_and_shutdown_detaches(self):
  presentation().execute("""
   assert(Controls.ActiveShortcut.parent==actionParent and not Controls.ActiveShortcut.hidden)
   assert(Controls.ActiveIcon.cell==32 and Controls.ActiveIcon.w==32 and Controls.ActiveIcon.h==32)
   opened=0;LuaEvents.SPC_OpenInstitutions.Add(function(pid,id)assert(pid==0 and id==4);opened=opened+1 end)
   Controls.ActiveShortcut.click();assert(opened==1)
   city=nil;Controls.ActiveShortcut.click();assert(opened==1)
   stopBridge();assert(actionParent.destroyed==Controls.ActiveShortcut)
   local n=#requests;Events.GameCoreEventPublishComplete();assert(#requests==n)
  """)


class TrainingRefresh(unittest.TestCase):
 def test_same_turn_gate_refresh_without_effect_writes(self):
  ui().execute("""
   active=3;adapter.Sync(city);adapter.Pulse();local data={City=city};adapter.Items(data);assert(#data.UnitItems==0)
   active=4;adapter.Invalidate(2);adapter.Pulse();adapter.Items(data)
   assert(#data.UnitItems==1 and #sentPackets==2 and builds==0)
   assert(data.UnitItems[1].Cost==60)
   active=1;adapter.Invalidate(2);adapter.RefreshFacts();adapter.Items(data);assert(#data.UnitItems==0)
  """)
 def test_projection_change_after_first_boundary_refreshes_and_idle_is_free(self):
  ui().execute("""
   ExposedMembers.SPC_P0={LevelBanners={views={['2:1']={active=3,potential=4,activeStatus='KNOWN',specialization='CULTURE'}}}}
   active=3;adapter.Sync(city);adapter.Pulse();active=4;adapter.Pulse();assert(#sentPackets==1)
   ExposedMembers.SPC_P0.LevelBanners.views['2:1'].active=4
   adapter.RefreshFacts();local d={City=city};adapter.Items(d);assert(#d.UnitItems==1 and #sentPackets==2)
   for i=1,1000 do adapter.RefreshFacts();adapter.Pulse()end;assert(#sentPackets==2)
  """)
 def test_pending_reservation_not_overwritten_by_governor_notification(self):
  ui().execute("""
   adapter.Sync(city);adapter.Pulse();adapter.Before(city,{Type=kind},false)
   local token=sentPackets[#sentPackets].Token
   adapter.Invalidate(2);adapter.RefreshFacts();assert(sentPackets[#sentPackets].Token==token)
   adapter.Pulse();adapter.Pulse();assert(builds==1 and state().trainingQueued)
   local n=builds;adapter.RefreshFacts();assert(builds==n)
  """)
 def test_foreign_governor_does_not_resync(self):
  ui().execute("adapter.Sync(city);adapter.Pulse();adapter.Invalidate(1);adapter.RefreshFacts();assert(#sentPackets==1)")


class NativeOverview(unittest.TestCase):
 def test_shortcut_opens_buildings_idempotently_and_preserves_native_close(self):
  l=display();l.execute("""
   opened=0;closed=0;tabCalls=0;selectedTab='other'
   Controls.BuildingsButton={};Controls.HealthButton={}
   OnShowOverviewPanel=function(v)if v then opened=opened+1 else Close()end end
   Close=function()closed=closed+1 end
   GetSelectedTabButton=function()return selectedTab end
   OnToggleBuildingsTab=function()tabCalls=tabCalls+1;selectedTab=Controls.BuildingsButton end
   LuaEvents.SPC_OpenInstitutions=setmetatable({Add=function(f)openInstitutions=f end,Remove=function()end},{__call=function(_,...)openInstitutions(...)end})
  """)
  l.execute((R/'Mod/UI/InstitutionOverview.lua').read_text())
  l.execute("""
   LuaEvents.SPC_OpenInstitutions(0,4);assert(opened==1 and tabCalls==1 and closed==0)
   LuaEvents.SPC_OpenInstitutions(0,4);assert(opened==1 and tabCalls==1 and closed==0)
   selectedTab=Controls.HealthButton;LuaEvents.SPC_OpenInstitutions(0,4);assert(tabCalls==2 and opened==1)
   Close();LuaEvents.SPC_OpenInstitutions(0,4);assert(closed==1 and opened==2)
   LuaEvents.SPC_OpenInstitutions(1,4);LuaEvents.SPC_OpenInstitutions(0,9);assert(opened==2)
  """)


class PresentationContract(unittest.TestCase):
 def test_profession_metric_colors_stay_inside_their_ability(self):
  display().execute("""
   local colors={RESEARCH='ResScienceLabelCS',CULTURE='ResCultureLabelCS',COMMERCE='ResGoldLabelCS',INDUSTRY='ResProductionLabelCS'}
   for kind,color in pairs(colors)do
    v.specialization=kind
    v.institutionSummary={known=true,tradition={age=10,percent=10,nextAge=20,state='COUNTING'},reputation={age=8,state='COUNTING'},
     dialogue=30,insights=4,engineering=2,templatesKnown=true,buildingTemplates=7,districtTemplates=3}
    for i=1,4 do
     local text=SPCInstitutionPresentation.Tooltip(i,v)
     for token in text:gmatch('%[COLOR:([^%]]+)%]')do assert(token==color)end
     local _,starts=text:gsub('%[COLOR:','');local _,ends=text:gsub('%[ENDCOLOR%]','');assert(starts==ends)
    end
   end
  """)
 def test_exact_native_geometry_and_no_frame_or_timer_api(self):
  root=ET.parse(R/'Mod/UI/CityPotential.xml').getroot()
  button=root.find('./Button');self.assertEqual(button.get('Size'),'44,53')
  self.assertEqual(button.get('Texture'),'UnitPanel_ActionButton')
  self.assertEqual(button.find('./Image').get('Size'),'32,32')
  for path in ['UI/CityPotential.lua','UI/ExpeditionTrainingUI.lua']:
   source=(R/'Mod'/path).read_text()
   for forbidden in ['SetUpdate','SystemUpdateUI','SetTimer']:
    self.assertNotIn(forbidden,source)
  self.assertNotIn('WorldTracker',(R/'Mod/UI/CityPotential.xml').read_text())



def current_production():
 # B202 fixture predates five independent panel adapters. Supply their inert
 # interfaces here; the real CrewProjectOrder and Expedition adapter still run.
 from test_expedition_training_ui import production_adapter
 def seed():
  l=ui();l.execute("""
   local function factory()return {Sync=function()end,Pulse=function()end,Publish=function()end,
    WarmStart=function()end,Items=function()end,Before=function()return true end}end
   SPCEngineeringStudyUI={New=factory};SPCCapitalInvestmentUI={New=factory}
   SPCDevelopmentInvestmentUI={New=factory};SPCCommerceUI={New=factory};SPCCrewProjectUI={New=factory}
   SPCRestructuringUI={ObserveTraining=function()end};SPCCrewModel={Parse=function()end}
   ContextPtr={IsHidden=function()return true end}
   Events.GameCoreEventPlaybackComplete=event('GameCoreEventPlaybackComplete')
   Events.GovernorPromoted=event('GovernorPromoted')
  """);return l
 with patch('test_expedition_training_ui.ui',seed):return production_adapter()


class ProductionWiring(unittest.TestCase):
 def test_actual_event_wiring_refreshes_only_training_and_keeps_native_guard(self):
  current_production().execute("""
   active=3;GetDataHelper();hooks.GameCoreEventPublishComplete()
   assert(#GetDataHelper().UnitItems==0)
   active=4;hooks.GovernorPromoted(2);hooks.GameCoreEventPublishComplete()
   assert(#GetDataHelper().UnitItems==1)
   active=3;hooks.GovernorPromoted(2);hooks.GameCoreEventPlaybackComplete()
   assert(#GetDataHelper().UnitItems==0)
   queueSelected=true;BuildUnit(city,{Type='UNIT_SPY'})
   assert(nativeSelections==1 and nativeBuilds==0)
  """)
 def test_native_replacement_still_waits_for_actual_queue_removal(self):
  current_production().execute("""
   train('RESERVE','r');entries={{Directive=1,UnitType=100}};train('CONFIRM','c')
   BuildUnit(city,{Type='UNIT_SPY'});hooks.GameCoreEventPublishComplete();hooks.GameCoreEventPublishComplete()
   assert(state().phase=='ENDED' and nativeBuilds==1)
  """)
 def test_actual_bounded_diagnostics_capture_facts_and_admission_without_writes(self):
  from test_expedition_training_trace_integration import runtime
  l=runtime(True);l.execute("""
   print=function()end
   active=3;train('SYNC','first');local v=findStage('TRAINING_SYNC_FACTS')
   assert(v.active=='3' and v.specialization=='CULTURE' and v.eligibility=='false')
   assert(v.reason=='FACTS_INELIGIBLE' and v.requestKey=='first')
   active=4;train('SYNC','second');v=findStage('TRAINING_SYNC_FACTS')
   assert(v.active=='4' and v.eligibility=='true' and v.reason=='AVAILABLE')
   assert(storeWrites==0 and markerWrites==0 and initCalls==0)
  """)

if __name__=='__main__':unittest.main()
