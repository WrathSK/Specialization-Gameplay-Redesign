"""B239 presentation: actual Lua action interception, dashboard and scalar requests.

UI control/native-operation stubs prove protocol and event-only behavior locally;
font rendering, icon availability and native Gold remain user-game evidence.
"""
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from lupa.lua55 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
UI=ROOT/'Mod/UI'
SETUP=r'''
include=function()end
local function event()
 local callbacks={};return setmetatable({Add=function(fn)callbacks[#callbacks+1]=fn end,
  Remove=function(fn)for i=#callbacks,1,-1 do if callbacks[i]==fn then table.remove(callbacks,i)end end end,
  Fire=function(...)for _,fn in ipairs(callbacks)do fn(...)end end}, {__call=function(self,...)self.Fire(...)end})
end
Events=setmetatable({},{__index=function(t,k)local e=event();rawset(t,k,e);return e end})
LuaEvents=setmetatable({},{__index=function(t,k)local e=event();rawset(t,k,e);return e end})
local function control()
 local c={hidden=false,disabled=false,text=''}
 function c:SetText(v)self.text=v end;function c:SetHide(v)self.hidden=v end
 function c:SetDisabled(v)self.disabled=v end;function c:SetAlpha(v)self.alpha=v end
 function c:SetIcon(v)self.icon=v end;function c:SetToolTipString(v)self.tip=v end;function c:RegisterCallback(_,fn)self.click=fn end
 return c
end
Controls=setmetatable({},{__index=function(t,k)local c=control();rawset(t,k,c);return c end})
ContextPtr={hidden=true}
function ContextPtr:SetHide(v)self.hidden=v end
function ContextPtr:SetInitHandler(fn)self.initialize=fn end
function ContextPtr:SetShutdown(fn)self.shutdown=fn end
function ContextPtr:SetInputHandler(fn)self.input=fn end
function ContextPtr:SetUpdate()error('frame/timer forbidden')end
Game={GetLocalPlayer=function()return 0 end}
Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=99};Keys={VK_ESCAPE=27};KeyEvents={KeyUp=2}
SPCP0={VERSION='B239',IsTestPlayer=function(pid)return pid==0 end}
local strings={}
Locale={Lookup=function(key,...)
 local out={key};for _,v in ipairs({...})do out[#out+1]=tostring(v)end;return table.concat(out,'|')
end}
c={GetOwner=function()return owner end,GetID=function()return 9 end,GetX=function()return 10 end,GetY=function()return 11 end,GetName=function()return 'CITY_TEST'end};owner=0
Players={[0]={GetCities=function()return {FindID=function(_,id)if id==9 then return c end end}end}}
UI={GetHeadSelectedCity=function()return c end};sent={};notifications=0;opens=0
function UI.RequestPlayerOperation(pid,kind,packet)
 assert(pid==0 and kind==99)
 for _,value in pairs(packet)do assert(type(value)~='table','native arguments must be scalar')end
 sent[#sent+1]=packet
 if onSend then onSend(packet)end
 return sendResult
end
view={reference='0:9:10:11',token='city-token',revision=7,identity='COMMERCE',potential=3,active=3,activeStatus='KNOWN',
 workers=2,selected={'DISTRICT_CAMPUS','DISTRICT_THEATER'},effective={'DISTRICT_CAMPUS','DISTRICT_THEATER'},
 reputation={age=12,effective=0},totalRaw=3.79,totalGold=3,canConfigure=true,stage='READY',reason='COMMERCE_READY',domains={}}
local domains={'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE','DISTRICT_HOLY_SITE','DISTRICT_HARBOR'}
for i,id in ipairs(domains)do view.domains[i]={id=id,eligible=i<=3,selected=i<=2,effective=i<=2,suspended=false,
 reason=i<=2 and 'COMMERCE_EFFECTIVE' or i==3 and 'COMMERCE_NOT_SELECTED' or 'COMMERCE_LOCAL_DISTRICT_REQUIRED',
 localD=3,X=12,raw=1.8,gold=1,sourceName='CITY_SOURCE',sourceCity=8,sourceOwner=0}end
ExposedMembers={SPC_P0={Commerce={views={['0:9']=view},revision=1,ready=true}}}
LuaEvents.SPC_CommerceOpen.Add(function()opens=opens+1 end)
'''
def fixture(panel=False):
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(SETUP)
 # B241 adds this explicit adapter dependency; all previous assertions are retained.
 l.execute((UI/'CapitalInvestmentUI.lua').read_text())
 l.execute((UI/'CommerceUI.lua').read_text())
 if panel:
  l.execute((UI/'CommercePanel.lua').read_text());l.execute('ContextPtr.initialize()')
 else:l.execute('api=SPCCommerceUI.New(SPCP0,function()notifications=notifications+1 end)')
 return l

class Action(unittest.TestCase):
 def test_production_action_never_produces_or_toggles(self):
  fixture().execute("""
   local item={Type=SPCCommerceUI.PROJECT};assert(not api.Before(c,item,false));assert(opens==1 and #sent==0)
   assert(not api.Before(c,item,true) and opens==2 and #sent==0)
   assert(api.Before(c,{Type='PROJECT_OTHER'},false))
  """)
 def test_production_action_filter_scopes_identity_and_potential(self):
  for change in ("view.potential=2", "view.identity='INDUSTRY'", "ExposedMembers.SPC_P0.Commerce.views={}"):
   with self.subTest(change=change):fixture().execute(change+"""
    local data={City=c,ProjectItems={{Type='PROJECT_OTHER'},{Type=SPCCommerceUI.PROJECT}}}
    api.Items(data);assert(#data.ProjectItems==1 and data.ProjectItems[1].Type=='PROJECT_OTHER')
    assert(not api.Before(c,{Type=SPCCommerceUI.PROJECT},false) and opens==0 and #sent==0)
   """)
 def test_opener_is_zero_cost_action_and_retains_held_report_access(self):
  fixture().execute("""
   view.stage='HELD';view.canConfigure=false
   local data={City=c,ProjectItems={{Type=SPCCommerceUI.PROJECT,Disabled=true,Cost=1,TurnsLeft=1}}}
   api.Items(data);local item=data.ProjectItems[1]
   assert(item.SPC_CommerceAction and not item.Disabled and item.Cost==0 and item.TurnsLeft==0)
   assert(not api.Before(c,item,false) and opens==1 and #sent==0)
  """)
 def test_publication_no_change_does_not_refresh_or_request(self):
  fixture().execute("""
   api.Publish();assert(notifications==1)
   for i=1,100 do api.Publish()end;assert(notifications==1 and #sent==0)
   ExposedMembers.SPC_P0.Commerce.revision=2;api.Publish();assert(notifications==2)
  """)
 def test_actual_production_adapter_intercepts_before_any_native_or_other_intent(self):
  l=fixture();l.execute(r'''
   RefreshCurrentProduction=function()end;GetDataHelper=function()return nil end
   AdvanceProject=function()error('native project enqueue is forbidden')end
   BuildUnit=function()end;RemoveQueueItem=function()end;GetBuildInsertMode=function()end
   CheckQueueItemSelected=function()return false end
   local function selection()return {Before=function()error('unrelated intent must not run')end,Items=function()end,
    Sync=function()end,Publish=function()end,Pulse=function()end,WarmStart=function()end,CancelQueue=function()end}end
   SPCProjectTurnRead={New=function()end};SPCTimedProjectSelection={New=selection}
   SPCClaimProjectUI={New=selection};SPCDialogueProjectUI={New=selection};SPCEngineeringStudyUI={New=selection}
   SPCCrewProjectUI={New=selection};SPCExpeditionTrainingUI={New=selection}
  ''');l.execute((UI/'CrewProjectOrder.lua').read_text())
  l.execute("AdvanceProject(c,{Type=SPCCommerceUI.PROJECT});assert(opens==1 and #sent==0)")

class Dashboard(unittest.TestCase):
 def check(self,script):fixture(True).execute(script)
 def test_open_reads_formula_sources_floor_and_history_without_writes(self):
  self.check("""
   LuaEvents.SPC_CommerceOpen(0,9);assert(not ContextPtr.hidden and not Controls.Window.hidden and #sent==0)
   assert(Controls.Summary.text:find('2|2|2|3',1,true))
   assert(Controls.Reputation.text:find('12|0',1,true))
   assert(Controls.Domain1Details.text:find('3|12|1.8|1',1,true))
   assert(Controls.Domain1Source.text:find('CITY_SOURCE',1,true))
   assert(not Controls.Domain1Toggle.disabled and Controls.Domain4Toggle.disabled)
   assert(Controls.Domain1Icon.icon=='ICON_PROJECT_ENHANCE_DISTRICT_CAMPUS')
  """)
 def test_known_project_icon_names_and_full_formula_tooltip(self):
  self.check("""
   LuaEvents.SPC_CommerceOpen(0,9)
   local domains={'CAMPUS','THEATER','INDUSTRIAL_ZONE','HOLY_SITE','HARBOR'}
   for i,id in ipairs(domains)do assert(Controls['Domain'..i..'Icon'].icon=='ICON_PROJECT_ENHANCE_DISTRICT_'..id)end
   assert(Controls.Formula.tip==Controls.Formula.text and Controls.Formula.tip:find('FORMULA',1,true))
  """)
 def test_reputation_unstarted_and_unknown_are_not_loading_or_zero_history(self):
  self.check("""
   view.reputation={state='NOT_ESTABLISHED'};LuaEvents.SPC_CommerceOpen(0,9)
   assert(Controls.Reputation.text:find('REPUTATION_NOT_STARTED',1,true))
   view.revision=8;view.reason='COMMERCE_REPUTATION_UNKNOWN';view.stage='HELD';view.canConfigure=false
   Events.GameCoreEventPublishComplete.Fire()
   assert(Controls.Reputation.text:find('REPUTATION_UNKNOWN',1,true))
   assert(Controls.Reputation.tip==Controls.Reputation.text and Controls.Domain1Toggle.disabled)
   view.revision=9;view.reason='COMMERCE_READY';view.reputation={state='UNKNOWN_INTERVAL',age=10,effective=0}
   Events.GameCoreEventPublishComplete.Fire();assert(Controls.Reputation.text:find('REPUTATION_UNKNOWN',1,true))
  """)
 def test_explicit_toggle_sends_scalar_reference_and_never_resends(self):
  self.check("""
   LuaEvents.SPC_CommerceOpen(0,9);Controls.Domain1Toggle.click();assert(#sent==1)
   local p=sent[1];assert(p.Action=='COMMERCE_SELECT' and p.Domain=='DISTRICT_CAMPUS' and p.Enabled==false)
   assert(p.Reference=='0:9:10:11' and p.CityToken=='city-token' and p.Revision==7 and p.CityID==9)
   assert(Controls.Domain1Toggle.disabled and Controls.Error.text:find('REQUEST_WAIT',1,true))
   for i=1,100 do Controls.Domain1Toggle.click();Events.GameCoreEventPublishComplete.Fire()end;assert(#sent==1)
  """)
 def test_ack_refreshes_without_requiring_a_new_view_revision(self):
  self.check("""
   LuaEvents.SPC_CommerceOpen(0,9);Controls.Domain1Toggle.click()
   ExposedMembers.SPC_P0.Commerce.lastRequest={token=sent[1].Token,owner=0,city=9,accepted=false,reason='COMMERCE_CAPACITY'}
   Events.GameCoreEventPublishComplete.Fire()
   assert(not Controls.Domain1Toggle.disabled and Controls.Error.text:find('NO_WORKERS',1,true))
  """)
 def test_same_turn_published_state_updates_and_selects_remaining_domain(self):
  self.check("""
   LuaEvents.SPC_CommerceOpen(0,9);Controls.Domain3Toggle.click()
   assert(sent[1].Enabled and sent[1].Domain=='DISTRICT_INDUSTRIAL_ZONE')
   view.revision=8;view.workers=1;view.totalGold=1
   view.selected[3]='DISTRICT_INDUSTRIAL_ZONE';view.effective={'DISTRICT_CAMPUS'}
   view.domains[3].selected=true;view.domains[3].suspended=true;view.domains[3].reason='COMMERCE_CAPACITY'
   ExposedMembers.SPC_P0.Commerce.lastRequest={token=sent[1].Token,owner=0,city=9,accepted=true}
   Events.GameCoreEventPublishComplete.Fire()
   assert(Controls.Summary.text:find('1|1|3|1',1,true) and Controls.Domain3State.text:find('NO_WORKERS',1,true))
   assert(not Controls.Domain3Toggle.disabled and Controls.Domain3ToggleCaption.text:find('DISABLE',1,true))
  """)
 def test_hidden_panel_unchanged_publish_and_other_city_do_not_render(self):
  self.check("""
   local n=0;local set=Controls.Summary.SetText
   Controls.Summary.SetText=function(self,...)n=n+1;return set(self,...)end
   Events.GameCoreEventPublishComplete.Fire();assert(n==0)
   LuaEvents.SPC_CommerceOpen(0,9);assert(n==1)
   for i=1,100 do Events.GameCoreEventPublishComplete.Fire()end;assert(n==1 and #sent==0)
   ExposedMembers.SPC_P0.Commerce.revision=2;Events.GameCoreEventPublishComplete.Fire();assert(n==1)
   Controls.CloseButton.click();view.revision=8;Events.GameCoreEventPublishComplete.Fire();assert(n==1)
  """)
 def test_unknown_and_inactive_states_do_not_send_or_appear_as_zero(self):
  self.check("""
   view.canConfigure=false;view.stage='HELD';view.reason='COMMERCE_NETWORK_UNKNOWN';view.totalGold=nil
   view.domains[1].X=nil;view.domains[1].raw=nil;view.domains[1].gold=nil
   LuaEvents.SPC_CommerceOpen(0,9)
   assert(Controls.Error.text:find('NETWORK_WAIT',1,true) and Controls.Domain1Details.text:find('WAITING',1,true))
   Controls.Domain1Toggle.click();assert(#sent==0)
   view.revision=8;view.reason='COMMERCE_ACTIVE_III_REQUIRED';Events.GameCoreEventPublishComplete.Fire()
   assert(Controls.Error.text:find('INACTIVE',1,true) and Controls.Domain1Toggle.disabled)
  """)
 def test_unconfirmed_owned_cleanup_keeps_residual_gold_warning_visible(self):
  self.check("""
   view.stage='HELD';view.reason='COMMERCE_WRITE_UNCONFIRMED';view.canConfigure=false
   view.totalGold=0;view.cleanupConfirmed=false;view.remainingCarrierGold=3
   LuaEvents.SPC_CommerceOpen(0,9)
   assert(Controls.Error.text:find('CLEANUP_ERROR|3',1,true))
   assert(Controls.Error.tip==Controls.Error.text and Controls.Domain1Toggle.disabled and #sent==0)
   view.revision=8;view.cleanupConfirmed=true;view.remainingCarrierGold=0;Events.GameCoreEventPublishComplete.Fire()
   assert(not Controls.Error.text:find('CLEANUP_ERROR',1,true))
  """)
 def test_owner_or_reference_change_closes_and_blocks_stale_action(self):
  self.check("""
   LuaEvents.SPC_CommerceOpen(0,9);owner=1;Events.GameCoreEventPublishComplete.Fire()
   assert(ContextPtr.hidden and Controls.Window.hidden);Controls.Domain1Toggle.click();assert(#sent==0)
  """)
 def test_load_closes_mirror_and_escaped_close_has_no_backend_effect(self):
  self.check("""
   LuaEvents.SPC_CommerceOpen(0,9);assert(ContextPtr.input(2,27) and ContextPtr.hidden)
   LuaEvents.SPC_CommerceOpen(0,9);Events.LoadScreenClose.Fire();assert(ContextPtr.hidden and #sent==0)
   ContextPtr.shutdown();LuaEvents.SPC_CommerceOpen(0,9);assert(ContextPtr.hidden)
  """)

class Markup(unittest.TestCase):
 def test_all_actual_controls_exist_and_rows_leave_button_space(self):
  tree=ET.parse(UI/'CommercePanel.xml');ids={x.attrib['ID']:x for x in tree.iter() if 'ID'in x.attrib}
  for key in ('Window','Title','CloseButton','CloseButtonCaption','CityName','Summary','Reputation','Formula','Help','Error'):
   self.assertIn(key,ids)
  for i in range(1,6):
   for suffix in ('Icon','Name','State','Details','Source','Toggle','ToggleCaption'):self.assertIn(f'Domain{i}{suffix}',ids)
   self.assertEqual(ids[f'Domain{i}'].attrib['Size'],'764,76')
   self.assertEqual(ids[f'Domain{i}Details'].attrib['TruncateWidth'],'550')
  self.assertEqual(ids['Window'].attrib['Size'],'800,650')
 def test_no_timer_or_unrelated_probe_lifecycle_added(self):
  for file in ('CommerceUI.lua','CommercePanel.lua'):
   text=(UI/file).read_text()
   for token in ('SetUpdate(', 'ClearUpdate(', 'os.clock(', 'GetElapsedTime(', 'Events.GameCoreEventPlaybackComplete'):
    self.assertNotIn(token,text)

if __name__=='__main__':unittest.main()
