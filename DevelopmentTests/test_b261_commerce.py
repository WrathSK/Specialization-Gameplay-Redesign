"""Actual B261 UI callbacks; native layout and input routing need user review."""
from pathlib import Path
import unittest,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from test_b239_commerce_ui import SETUP
from test_b252_sidebar import ui as development
ROOT=Path(__file__).resolve().parents[1]
def ui():
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(SETUP)
 l.execute((ROOT/'Mod/UI/CommerceUI.lua').read_text())
 l.execute(r"""
 local old=getmetatable(Controls).__index
 getmetatable(Controls).__index=function(t,k)
  local c=old(t,k)
  function c:SetSizeVal(w,h)self.width=w;self.height=h end
  function c:SetSizeY(h)self.height=h end
  function c:SetOffsetX(x)self.x=x end;function c:SetOffsetY(y)self.y=y end
  function c:SetTruncateWidth(w)self.truncate=w end;function c:SetWrapWidth(w)self.wrap=w end
  function c:SetColorByName(v)self.color=v end
  function c:GetSizeY()return self.height or math.max(18,math.ceil(#self.text/math.max(1,(self.wrap or 240)/9))*18)end
  function c:CalculateSize()end;function c:ReprocessAnchoring()end;function c:CalculateInternalSize()end
  return c
 end
 width=1400;height=900;UIManager={GetScreenSizeVal=function()return width,height end};SystemUpdateUI={ScreenResize=7};KeyEvents.KeyDown=1
 InstanceManager={new=function()
  rows={items={}};function rows:ResetInstances()self.items={}end
  function rows:GetInstance()local o={};local i=#self.items+1;for _,k in ipairs({'Root','Caption','Marker','State','Icon'})do o[k]=Controls['row'..i..k]end;self.items[i]=o;return o end
  return rows
 end}
 function notify()view.revision=view.revision+1;Events.GameCoreEventPublishComplete.Fire()end
 function ack(ok,reason)local p=sent[#sent];ExposedMembers.SPC_P0.Commerce.lastRequest={owner=0,city=9,token=p.Token,accepted=ok~=false,reason=reason};notify()end
 function inputEvent(kind,key)return {GetKey=function()return key end,GetMessageType=function()return kind end}end
 """)
 l.execute((ROOT/'Mod/UI/CommercePanel.lua').read_text());l.execute('ContextPtr.initialize();LuaEvents.SPC_CommerceOpen(0,9)');return l
class Sidebar(unittest.TestCase):
 def test_select_view_toggle_scalar_and_pending(self):
  ui().execute("assert(#sent==0 and Controls.DetailColumn.hidden);rows.items[3].Root.click();assert(not Controls.DetailColumn.hidden and Controls.Value.text:find('AFTER_ENABLE'));Controls.Confirm.click();Controls.Confirm.click();assert(#sent==1 and sent[1].Enabled and sent[1].Domain=='DISTRICT_INDUSTRIAL_ZONE' and sent[1].Revision==7 and sent[1].Reference=='0:9:10:11');assert(Controls.Confirm.disabled)")
 def test_order_preservation_reopen_and_suspended(self):
  ui().execute("view.selected={'DISTRICT_THEATER','DISTRICT_CAMPUS'};view.domains[1].effective=false;view.domains[1].reason='COMMERCE_CAPACITY';notify();assert(rows.items[1].Caption.text:find('THEATER') and rows.items[2].Caption.text:find('CAMPUS') and rows.items[2].Marker.text:find('SELECTED_PAUSED'));rows.items[2].Root.click();assert(Controls.ConfirmCaption.text:find('STOP'));Controls.Confirm.click();assert(sent[1].Enabled==false);view.selected={'DISTRICT_THEATER'};view.domains[1].selected=false;ack();assert(Controls.ConfirmCaption.text:find('START'));Controls.Confirm.click();assert(sent[2].Enabled==true);view.selected={'DISTRICT_THEATER','DISTRICT_CAMPUS'};view.domains[1].selected=true;ack();assert(rows.items[2].Caption.text:find('CAMPUS'))")
 def test_actual_values_errors_and_no_false_preview(self):
  ui().execute("rows.items[1].Root.click();assert(Controls.Value.text:find('1.8') and Controls.Source.text:find('CITY_SOURCE'));Controls.Confirm.click();ack(false,'COMMERCE_CAPACITY');assert(Controls.Status.text:find('NO_WORKERS'));view.domains[1].effective=false;view.domains[1].selected=false;view.domains[1].X=nil;notify();assert(Controls.Value.text:find('AFTER_ENABLE') and not Controls.Value.text:find('1.8') and Controls.Source.text:find('AFTER_ENABLE'));view.cleanupConfirmed=false;view.remainingCarrierGold=3;notify();assert(Controls.Status.text:find('CLEANUP_ERROR'))")
 def test_refresh_keeps_domain_identity_and_never_sends(self):
  ui().execute("rows.items[2].Root.click();view.selected={'DISTRICT_THEATER','DISTRICT_CAMPUS'};notify();assert(rows.items[1].Caption.color=='Gold');for i=1,20 do Events.SystemUpdateUI.Fire(99);Events.GameCoreEventPublishComplete.Fire()end;assert(#sent==0);view.domains={};notify();assert(Controls.DetailColumn.hidden)")
 def test_dimensions_wrap_and_narrow_back(self):
  for w,h in [(1400,900),(960,600),(610,720),(550,600),(360,600)]:
   with self.subTest(w=w):
    ui().execute(f"width={w};height={h};Events.SystemUpdateUI.Fire(7);rows.items[1].Root.click();assert(Controls.Window.height+27==height and Controls.DomainColumn.width==Controls.DetailColumn.width);assert(Controls.DetailColumn.y+Controls.DetailColumn.height==Controls.Window.height);assert(Controls.StatusCard.y==Controls.RulesCard.y+Controls.RulesCard.height+12 and Controls.DetailScroll.height>0);assert(Controls.Confirm.height==41);if width-16<590 then assert(Controls.DomainColumn.hidden and not Controls.Back.hidden);Controls.Back.click();assert(not Controls.DomainColumn.hidden and Controls.DetailColumn.hidden)end;assert(#sent==0)")
 def test_escape_object_and_legacy_down_up_both_panels(self):
  for factory in [ui,development]:
   for native in [True,False]:
    l=factory()
    if factory==development:l.execute('LuaEvents.SPC_DevelopmentOpen(0,9);ack();KeyEvents.KeyDown=1')
    l.execute("function event(kind,key)return {GetKey=function()return key end,GetMessageType=function()return kind end}end")
    down='event(1,27)' if native else '1,27';up='event(2,27)' if native else '2,27'
    l.execute(f"local n=#sent;assert(ContextPtr.input({down})==true and not ContextPtr.hidden);assert(ContextPtr.input({up})==true and ContextPtr.hidden);assert(ContextPtr.input({down})==false and #sent==n)")
 def test_invalid_city_held_and_shutdown(self):
  ui().execute("rows.items[1].Root.click();view.canConfigure=false;view.stage='HELD';notify();assert(Controls.Confirm.disabled);Controls.Confirm.click();assert(#sent==0);owner=1;notify();assert(ContextPtr.hidden);ContextPtr.shutdown();assert(ContextPtr.hidden)")
 def test_xml_controls_footer_and_native_backing(self):
  t=ET.parse(ROOT/'Mod/UI/CommercePanel.xml');ids={e.get('ID'):e for e in t.iter()if e.get('ID')}
  self.assertEqual(ids['Window'].get('Offset'),'0,27');self.assertEqual(ids['Footer'].get('Size'),'parent,90')
  self.assertEqual(ids['DomainScroll'].find('ScrollBar').get('Anchor'),'L,C')
  self.assertEqual(ids['ConfirmCaption'].get('Anchor'),'C,C');self.assertIsNone(ids['ConfirmCaption'].get('Offset'))
  self.assertEqual(len(ids),len([e for e in t.iter()if e.get('ID')]))
  for name in ['Value','Source','Rules','Status']:self.assertIsNotNone(ids[name+'Card']);self.assertEqual(ids[name+'Body'].get('Offset'),'12,46')
if __name__=='__main__':unittest.main()
