"""B266 selected-city lifecycle with actual UI Lua and native-shaped controls."""
import unittest
from test_b265_city_presentation import presentation

SETUP = """
 function makeCity(id,kind,x,y)
  return {id=id,kind=kind,x=x,y=y,active=kind and 1 or 0,potential=kind and 1 or 0,
   GetOwner=function()return 0 end,GetID=function(self)return self.id end,
   GetX=function(self)return self.x end,GetY=function(self)return self.y end}
 end
 cities={[4]=makeCity(4,'CULTURE',8,9)};cities[4].active=4;cities[4].potential=4
 city=cities[4];asynchronous=true
 function answer(p)
  local c=cities[p.CityID]
  local v={owner=0,cityID=c.id,x=c.x,y=c.y,token=p.Token,
   specialization=c.kind or 'NONE',active=c.active,potential=c.potential,activeStatus='KNOWN',
   institutionArchive={},institutionSummary={known=true,dialogue=2,insights=1,
    tradition={age=2,percent=1,nextAge=10,state='COUNTING'},engineering=1,templatesKnown=true,
    buildingTemplates=1,districtTemplates=1,reputation={age=3,state='COUNTING'}}}
  ExposedMembers.SPC_P0.CityPresentationView=v;publishPresentation(p,v)
 end
 UI.RequestPlayerOperation=function(pid,op,p)
  assert(pid==0 and p.Action=='CITY_PRESENTATION_READ')
  requestPorts[p]=ExposedMembers.SPC_P0.PlayerActionReplies.Presentations
  requests[#requests+1]=p;if not asynchronous then answer(p)end
 end
 function publishCity(c)
  ExposedMembers.SPC_P0.LevelBanners.views['0:'..c.id]={specialization=c.kind or 'NONE',
   potential=c.potential,active=c.active,activeStatus='KNOWN'}
 end
 function selectCity(id,overviewFirst)
  city=cities[id]
  data={Owner=0,City=city,BuildingsAndDistricts={{Buildings={{Type='BUILDING_SPC_OWN'},
   {Type='BUILDING_LIBRARY'},{Type='BUILDING_OTHER_MOD'}}}}}
  if overviewFirst then ViewPanelBreakdown(data)end
  Events.CitySelectionChanged()
  if not overviewFirst then ViewPanelBreakdown(data)end
 end
 function complete()
  answer(requests[#requests]);Events.GameCoreEventPublishComplete()
  Events.GameCoreEventPlaybackComplete()
 end
 publishCity(city)
"""

class NewCityLifecycle(unittest.TestCase):
 def test_loaded_city_then_each_new_profession_and_return_in_both_event_orders(self):
  for early in ('true','false'):
   with self.subTest(overview_first=early):
    presentation(SETUP).execute("""
     complete();assert(rows.items[4].State.text=='当前')
     for i,kind in ipairs({'RESEARCH','INDUSTRY','COMMERCE','CULTURE'})do
      local id=10+i;cities[id]=makeCity(id,nil,30+i,40+i);publishCity(cities[id])
      selectCity(id,"""+early+""");complete()
      cities[id].kind=kind;cities[id].active=1;cities[id].potential=1;publishCity(cities[id])
      Events.GameCoreEventPublishComplete();complete()
      assert(#rows.items==4 and not Controls.InstitutionContainer.hidden)
      assert(rows.items[1].Icon.icon=='ICON_SPC_LEVEL_'..kind..'_1')
      assert(rows.items[1].State.text=='当前' and rows.items[4].State.text=='尚未建立')
      assert(Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_'..kind..'_1' and not Controls.ActiveShortcut.hidden)
      assert(#rendered.BuildingsAndDistricts[1].Buildings==2)
      assert(rendered.BuildingsAndDistricts[1].Buildings[2].Type=='BUILDING_OTHER_MOD')
     end
     selectCity(4,"""+early+""");complete()
     assert(#rows.items==4 and rows.items[4].Name.text=='博雅总院' and rows.items[4].State.text=='当前')
    """)
 def test_first_new_city_after_no_selection_on_load(self):
  presentation(SETUP+'city=nil').execute("""
   assert(#requests==0)
   cities[5]=makeCity(5,'RESEARCH',3,6);publishCity(cities[5]);selectCity(5,true);complete()
   assert(rows.items[1].Name.text=='学者结社' and not Controls.ActiveShortcut.hidden)
  """)
 def test_busy_found_city_waits_for_real_boundary_and_then_converges(self):
  presentation(SETUP).execute("""
   complete();cities[5]=makeCity(5,'INDUSTRY',3,6);publishCity(cities[5]);coreBusy=true
   local n=#requests;selectCity(5,true)
   assert(#requests==n and Controls.InstitutionContainer.hidden and Controls.ActiveShortcut.hidden)
   coreBusy=false;Events.GameCoreEventPlaybackComplete();assert(#requests==n+1);complete()
   assert(rows.items[1].Name.text=='匠作坊')
   local n,s=#requests,layouts
   for i=1,1000 do Events.GameCoreEventPublishComplete();Events.GameCoreEventPlaybackComplete()end
   assert(#requests==n and layouts==s)
  """)
 def test_late_other_city_reply_cannot_restore_wrong_institutions(self):
  presentation(SETUP).execute("""
   complete();cities[5]=makeCity(5,'RESEARCH',3,6);publishCity(cities[5]);selectCity(5,true)
   local late=requests[#requests]
   cities[6]=makeCity(6,'INDUSTRY',9,2);publishCity(cities[6]);selectCity(6,true)
   answer(late);Events.GameCoreEventPublishComplete()
   assert(Controls.InstitutionContainer.hidden and Controls.ActiveShortcut.hidden)
   complete();assert(rows.items[1].Name.text=='匠作坊')
  """)
 def test_shutdown_removes_handlers_and_native_stack_reflows(self):
  presentation(SETUP).execute("""
   complete();assert(not Controls.ActiveShortcut.hidden)
   stopBridge();assert(Controls.ActiveShortcut.hidden and actionParent.destroyed==Controls.ActiveShortcut)
   local n=#requests;selectCity(4,true);Events.GameCoreEventPublishComplete();assert(#requests==n)
  """)

class ExceptionRelease(unittest.TestCase):
 def test_initial_grid_layout_error_records_stage_and_does_not_block_next_city(self):
  l=presentation(SETUP+"actionParent.parent.DoAutoSize=function()error('layout unavailable')end")
  l.execute("""
   local failure=trace[#trace];assert(failure.stage=='INSTITUTION_UI_FAILURE')
   assert(failure.s.viewStage=='LAYOUT_BACKING' and failure.s.errorCode=='PRESENTATION_CALLBACK_FAILED')
   assert(failure.s.owner==0 and failure.s.city==4)
   actionParent.parent.DoAutoSize=function()layouts=layouts+1 end
   cities[5]=makeCity(5,'RESEARCH',3,6);publishCity(cities[5]);selectCity(5,true);complete()
   assert(rows.items[1].Name.text=='学者结社' and #requests>=2)
  """)
 def test_late_grid_error_while_deselecting_does_not_latch_busy(self):
  presentation(SETUP).execute("""
   complete();local normal=actionParent.parent.DoAutoSize
   actionParent.parent.DoAutoSize=function()error('grid failure')end
   city=nil;Events.CitySelectionChanged()
   actionParent.parent.DoAutoSize=normal
   cities[5]=makeCity(5,'INDUSTRY',3,6);publishCity(cities[5]);selectCity(5,false);complete()
   assert(rows.items[1].Name.text=='匠作坊' and not Controls.ActiveShortcut.hidden)
  """)
 def test_subscriber_exception_releases_guard_and_later_semantic_event_recovers(self):
  presentation(SETUP).execute("""
   local normal=LuaEvents.SPC_PresentationChanged
   LuaEvents.SPC_PresentationChanged=function()error('subscriber failure')end
   complete();assert(trace[#trace].stage=='INSTITUTION_UI_FAILURE')
   LuaEvents.SPC_PresentationChanged=normal
   cities[4].active=2;publishCity(cities[4]);Events.GovernorPromoted(0)
   Events.GameCoreEventPublishComplete();complete()
   assert(rows.items[2].State.text=='当前' and rows.items[4].State.text=='未激活')
  """)
 def test_render_exception_keeps_reads_live_without_idle_request_retry(self):
  presentation(SETUP).execute("""
   local normal=Controls.ActiveIcon.SetIcon
   Controls.ActiveIcon.SetIcon=function()error('icon failure')end;complete()
   assert(rows.items[4].State.text=='当前')
   local n=#requests;for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(#requests==n)
   Controls.ActiveIcon.SetIcon=normal;Events.GameCoreEventPlaybackComplete()
   assert(Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_4' and #requests==n)
   cities[5]=makeCity(5,'COMMERCE',3,6);publishCity(cities[5]);selectCity(5,true);complete()
   assert(rows.items[1].Name.text=='商贾聚落' and not Controls.ActiveShortcut.hidden)
  """)
 def test_diagnostic_failure_cannot_disable_city_refresh(self):
  presentation(SETUP+"SPCExpeditionTrainingDiagnostics.New=function()return {Record=function()error('diagnostic failure')end}end").execute("""
   complete();cities[5]=makeCity(5,'INDUSTRY',3,6);publishCity(cities[5]);selectCity(5,true);complete()
   assert(rows.items[1].Name.text=='匠作坊')
  """)

if __name__=='__main__':unittest.main()
