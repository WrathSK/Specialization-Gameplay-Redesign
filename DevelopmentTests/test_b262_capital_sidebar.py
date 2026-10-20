"""B262 actual sidebar callbacks and retained transaction boundaries."""
from pathlib import Path
import unittest,re,xml.etree.ElementTree as E
from test_b261_commerce import ui as commerce
ROOT=Path(__file__).resolve().parents[1]
def ui():
 l=commerce();l.execute('ContextPtr.shutdown()');l.execute((ROOT/'Mod/UI/CapitalInvestmentUI.lua').read_text())
 l.execute(r"""
 managers={};InstanceManager={new=function(_,name)
  local m={items={}};managers[name]=m
  function m:ResetInstances()self.items={}end
  function m:GetInstance()local o={};local i=#self.items+1;for _,k in ipairs({'Root','Caption','Marker','State','Icon'})do o[k]=Controls[name..i..k]end;self.items[i]=o;return o end
  return m
 end}
 capitalView={available=true,canSign=true,stage='READY',token='city',reference='0:9:10:11',revision=1,balance=1000,contracts={},domains={}}
 for _,id in ipairs({'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE'})do
  capitalView.domains[#capitalView.domains+1]={id=id,canSign=true,reason='CAPITAL_READY',quote={principal=250,D=1,S=1,C=1,r=.01,due=10,safe=252.5,success=257.5,failure=125,probability=.41,expected=179.325,net=-70.675}}
 end
 capBackend={views={['0:9']=capitalView},revision=1};ExposedMembers.SPC_P0.CapitalInvestment=capBackend
 function ack(ok,reason,detail)local p=sent[#sent];capBackend.lastRequest={token=p.Token,owner=0,city=9,accepted=ok~=false,reason=reason,failure=detail};Events.GameCoreEventPublishComplete.Fire()end
 function notify()capitalView.revision=capitalView.revision+1;Events.GameCoreEventPublishComplete.Fire()end
 function pick(i,mode)managers.CapitalDomain.items[i or 1].Root.click();ack();if mode then managers.CapitalMode.items[mode].Root.click()end end
 """)
 l.execute((ROOT/'Mod/UI/CapitalInvestmentPanel.lua').read_text());l.execute('ContextPtr.initialize();LuaEvents.SPC_CapitalOpen(0,9);ack()');return l
class Sidebar(unittest.TestCase):
 def test_no_auto_selection_and_no_sign_from_browsing(self):
  ui().execute("assert(Controls.ModeColumn.hidden and Controls.DetailColumn.hidden and #sent==1 and sent[1].Action=='CAPITAL_OPEN');pick(2,2);assert(not Controls.DetailColumn.hidden and #sent==2 and sent[2].Action=='CAPITAL_REFRESH');assert(Controls.Returns.text:find('NEGATIVE_EV'));managers.CapitalMode.items[1].Root.click();assert(#sent==2 and Controls.Returns.text:find('STABLE_DETAIL'))")
 def test_modes_scalar_packets_and_repeat_guard(self):
  for mode in [1,2]:
   ui().execute(f"pick(1,{mode});Controls.Confirm.click();Controls.Confirm.click();assert(#sent==3 and sent[3].Action=='CAPITAL_CONFIRM' and sent[3].Mode=='{'STABLE' if mode==1 else 'VENTURE'}' and sent[3].Domain=='DISTRICT_CAMPUS' and sent[3].CityToken=='city' and sent[3].Revision==1 and Controls.Confirm.disabled)")
 def test_pending_domain_switch_and_synchronous_ack(self):
  ui().execute("pick(1,1);onSend=function(p)capitalView.canSign=false;capBackend.lastRequest={owner=0,city=9,token=p.Token,accepted=true};Events.GameCoreEventPublishComplete.Fire()end;Controls.Confirm.click();Controls.Confirm.click();assert(#sent==3 and Controls.Confirm.disabled)")
 def test_locked_contract_distinct_from_quote_and_errors(self):
  ui().execute("pick(1,2);capitalView.contracts.DISTRICT_CAMPUS={mode='STABLE',stage='ACTIVE',principal=200,debited=199.999,due=8,D=2,S=3,C=4,sSourceName='LOCKED_CITY'};capitalView.domains[1].canSign=false;capitalView.domains[1].reason='CAPITAL_DOMAIN_OCCUPIED';notify();assert(Controls.Current.text:find('199.999') and Controls.Current.text:find('LOCKED_CITY') and Controls.Quote.text:find('250') and Controls.Confirm.disabled and managers.CapitalDomain.items[1].Marker.text:find('INVESTING'));local n=#sent;Controls.Confirm.click();assert(#sent==n);capitalView.stage='HELD';capitalView.reason='CAPITAL_STATE_UNKNOWN';capitalView.failure={phase='NATIVE_DEBIT'};notify();assert(Controls.Current.text:find('PAUSE_DEBIT'))")
 def test_settled_venture_and_actual_credit(self):
  ui().execute("pick(1,1);capitalView.contracts.DISTRICT_CAMPUS={mode='VENTURE',stage='SETTLED',won=false,principal=200,debited=199.999,paid=100.001,due=8,D=2,S=3,C=4};notify();assert(Controls.Current.text:find('RESULT_FAILURE') and Controls.Current.text:find('100.001') and managers.CapitalDomain.items[1].Marker.hidden)")
 def test_refresh_keeps_selection_and_domain_change_clears_mode(self):
  ui().execute("pick(2,2);Controls.Refresh.click();ack();assert(not Controls.DetailColumn.hidden and Controls.ConfirmCaption.text:find('VENTURE'));pick(1);assert(Controls.DetailColumn.hidden and Controls.Confirm.disabled);capitalView.domains={};notify();assert(Controls.ModeColumn.hidden)")
 def test_geometry_and_escape(self):
  for w,h in [(1400,900),(960,600),(820,720),(700,600),(360,600)]:
   ui().execute(f"width={w};height={h};Events.SystemUpdateUI.Fire(7);pick(1,1);assert(Controls.Window.height+27==height);assert(Controls.DomainColumn.width==Controls.ModeColumn.width and Controls.ModeColumn.width==Controls.DetailColumn.width);assert(Controls.DetailColumn.y+Controls.DetailColumn.height+(width-16<800 and 40 or 0)==Controls.Window.height);assert(Controls.CurrentCard.y==Controls.BasisCard.y+Controls.BasisCard.height+12 and Controls.DetailScroll.height>0);assert(ContextPtr.input(inputEvent(1,27)) and not ContextPtr.hidden);assert(ContextPtr.input(inputEvent(2,27)) and ContextPtr.hidden);assert(not ContextPtr.input(inputEvent(1,27)))")
 def test_narrow_navigation_and_shutdown(self):
  ui().execute("width=360;Events.SystemUpdateUI.Fire(7);pick(1,1);Controls.Back.click();assert(not Controls.ModeColumn.hidden and Controls.DetailColumn.hidden);Controls.Back.click();assert(not Controls.DomainColumn.hidden and Controls.ModeColumn.hidden);ContextPtr.shutdown();assert(ContextPtr.hidden)")
 def test_commerce_single_action_and_narrow_double_action_padding(self):
  l=commerce();l.execute("rows.items[1].Root.click();assert(Controls.Footer.height==66 and Controls.Confirm.height==41 and Controls.Back.hidden);width=360;Events.SystemUpdateUI.Fire(7);assert(Controls.Footer.height==90 and not Controls.Back.hidden and Controls.Confirm.height==41)")
 def test_xml_controls_and_native_dimensions(self):
  t=E.parse(ROOT/'Mod/UI/CapitalInvestmentPanel.xml');ids={e.get('ID')for e in t.iter()if e.get('ID')};s=(ROOT/'Mod/UI/CapitalInvestmentPanel.lua').read_text()
  self.assertFalse(set(re.findall(r'Controls\.([A-Za-z]+)',s))-ids)
  self.assertEqual(t.find('.//Grid[@ID="Footer"]').get('Size'),'parent,90');self.assertEqual(t.find('.//GridButton[@ID="Confirm"]').get('Size'),'285,41')
  self.assertEqual(t.find('.//Label[@ID="RefreshCaption"]').get('Anchor'),'C,C');self.assertIsNone(t.find('.//Label[@ID="RefreshCaption"]').get('Offset'))
if __name__=='__main__':unittest.main()
