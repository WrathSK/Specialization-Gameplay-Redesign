"""B241 UI/native protocol, exact shared network and package/SQL checks.
No game launch, rendered UI or native Treasury claim.
"""
from pathlib import Path
import unittest,re,sqlite3,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from test_b239_commerce_ui import SETUP
from test_culture_network import fixture as network_fixture
R=Path(__file__).resolve().parents[1];MOD=R/'Mod'

def ui(panel=True):
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(SETUP)
 l.execute((MOD/'UI/CapitalInvestmentUI.lua').read_text())
 l.execute("""
 local ref={owner=0,cityID=9,x=10,y=11,token='city',changes=0}
 capitalView={available=true,canSign=true,stage='READY',token='city',reference=ref,revision=1,balance=1000,contracts={},domains={}}
 for _,id in ipairs({'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE'})do
  capitalView.domains[#capitalView.domains+1]={id=id,canSign=true,reason='CAPITAL_READY',quote={principal=250,D=1,S=1,C=1,r=.01,due=10,safe=252.5,success=257.5,failure=125,probability=.41,expected=179.325,net=-70.675}}
 end
 ExposedMembers.SPC_P0.CapitalInvestment={views={['0:9']=capitalView},revision=1};capBackend=ExposedMembers.SPC_P0.CapitalInvestment
 LuaEvents.SPC_CapitalOpen.Add(function()opens=opens+1 end)
 function ack()
  local p=sent[#sent];capBackend.lastRequest={token=p.Token,owner=0,city=9,accepted=true};Events.GameCoreEventPublishComplete.Fire()
 end
 """)
 if panel:l.execute((MOD/'UI/CapitalInvestmentPanel.lua').read_text());l.execute('ContextPtr.initialize()')
 else:l.execute('api=SPCCapitalInvestmentUI.New(SPCP0,function()notifications=notifications+1 end)')
 return l
class UI(unittest.TestCase):
 def test_open_and_domain_selection_never_sign_or_touch_queue(self):
  ui().execute("LuaEvents.SPC_CapitalOpen(0,9);assert(#sent==1 and sent[1].Action=='CAPITAL_OPEN');ack();Controls.Domain2.click();assert(#sent==2 and sent[2].Action=='CAPITAL_REFRESH' and sent[2].Domain=='DISTRICT_THEATER')")
 def test_both_modes_use_same_scalar_confirm_and_latch_double_click(self):
  for button,mode in [('StableConfirm','STABLE'),('VentureConfirm','VENTURE')]:
   with self.subTest(mode=mode):ui().execute("LuaEvents.SPC_CapitalOpen(0,9);ack();Controls."+button+".click();Controls."+button+".click();assert(#sent==2 and sent[2].Action=='CAPITAL_CONFIRM' and sent[2].Mode=='"+mode+"');assert(Controls.StableConfirm.disabled and Controls.VentureConfirm.disabled)")
 def test_synchronous_ack_reentry_does_not_sign_twice(self):
  ui().execute("LuaEvents.SPC_CapitalOpen(0,9);ack();onSend=function(p)capitalView.canSign=false;capBackend.lastRequest={token=p.Token,owner=0,city=9,accepted=true};Events.GameCoreEventPublishComplete.Fire()end;Controls.StableConfirm.click();assert(#sent==2);assert(Controls.StableConfirm.disabled)")
 def test_rejected_stale_quote_shows_fresh_state_without_automatic_retry(self):
  ui().execute("LuaEvents.SPC_CapitalOpen(0,9);ack();Controls.StableConfirm.click();local p=sent[2];capitalView.revision=2;capBackend.lastRequest={token=p.Token,owner=0,city=9,accepted=false,reason='CAPITAL_QUOTE_STALE'};Events.GameCoreEventPublishComplete.Fire();assert(#sent==2 and Controls.Error.text:find('报价已变化'))")
 def test_contract_remains_readable_without_current_signing_gate(self):
  ui().execute("capitalView.canSign=false;capitalView.reason='CAPITAL_ACTIVE_III_REQUIRED';capitalView.contracts.DISTRICT_CAMPUS={stage='ACTIVE',principal=250,due=10,D=1,S=1,C=1};LuaEvents.SPC_CapitalOpen(0,9);ack();assert(Controls.Contract.text:find('ACTIVE')==nil and Controls.StableConfirm.disabled and Controls.VentureConfirm.disabled)")
 def test_foreign_city_and_shutdown_remove_handlers(self):
  ui().execute("LuaEvents.SPC_CapitalOpen(1,9);assert(#sent==0);LuaEvents.SPC_CapitalOpen(0,9);ack();owner=1;Events.GameCoreEventPublishComplete.Fire();assert(Controls.Window.hidden);owner=0;ContextPtr.shutdown();LuaEvents.SPC_CapitalOpen(0,9);assert(#sent==1)")
 def test_project_intercept_is_zero_turn_and_suppresses_stale_enqueue(self):
  ui(False).execute("local item={Type=SPCCapitalInvestmentUI.PROJECT};local data={City=c,ProjectItems={item,{Type='OTHER'}}};api.Items(data);assert(#data.ProjectItems==2 and item.Cost==0 and item.TurnsLeft==0);assert(not api.Before(c,item,false) and opens==1);capitalView.available=false;api.Items(data);assert(#data.ProjectItems==1);assert(not api.Before(c,item,true) and opens==1);assert(api.Before(c,{Type='OTHER'},false))")
class Network(unittest.TestCase):
 def test_reuses_recipient_sources_and_does_not_forward_again(self):
  l=network_fixture(False);l.execute("send('0,4,0,2,10;0,2,0,1,11;0,1,0,5,12',3);local a=net.CurrentCapitalSources(0,cities[2],'CULTURE');assert(#a==1 and a[1]==4);local b=net.CurrentCapitalSources(0,cities[1],'CULTURE');assert(#b==1 and b[1]==4);assert(#net.CurrentCapitalSources(0,cities[5],'CULTURE')==0)")
 def test_pending_proof_is_not_an_empty_or_stale_source_pool(self):
  l=network_fixture();l.execute("net.CheckEvidence(false);assert(not pcall(net.CurrentCapitalSources,0,cities[2],'CULTURE'))")
 def test_returns_independent_source_ids(self):
  l=network_fixture();l.execute("local a=net.CurrentCapitalSources(0,cities[2],'CULTURE');assert(#a==1);a[1]=999;assert(net.CurrentCapitalSources(0,cities[2],'CULTURE')[1]==4)")
class Package(unittest.TestCase):
 def test_control_ids_localization_keys_and_panel_bounds(self):
  p=MOD/'UI/CapitalInvestmentPanel.lua';txt=p.read_text();xml=ET.parse(MOD/'UI/CapitalInvestmentPanel.xml');ids={e.get('ID')for e in xml.iter()if e.get('ID')}
  direct=set(re.findall(r'Controls\.([A-Za-z0-9_]+)',txt));self.assertTrue(direct<=ids,direct-ids)
  self.assertTrue({'Domain'+str(i)+s for i in range(1,4)for s in ('','Caption')}<=ids)
  db=sqlite3.connect(':memory:');db.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT,PRIMARY KEY(Language,Tag))');db.executescript((MOD/'Text/Commerce.sql').read_text())
  keys=set(re.findall(r"L\('([A-Z_]+)'",txt))|{'RESEARCH','CULTURE','INDUSTRY'}
  for key in keys:self.assertIsNotNone(db.execute("SELECT Text FROM LocalizedText WHERE Language='zh_Hans_CN' AND Tag=?",('LOC_SPC_CAPITAL_'+key,)).fetchone(),key)
  self.assertNotIn('SetUpdate',txt);self.assertIn("contract.stage=='SETTLED'",txt)
 def test_manifest_lists_all_new_sources_once(self):
  xml=ET.parse(MOD/'SpecializationP0.modinfo');files=[e.text for e in xml.findall('./Files/File')];imports={e.text for e in xml.findall('./InGameActions/ImportFiles/File')}
  needed={'CapitalInvestment.lua','CapitalInvestmentModel.lua','UI/CapitalInvestmentUI.lua','UI/CapitalInvestmentPanel.lua','UI/CapitalInvestmentPanel.xml'}
  for p in needed:self.assertEqual(files.count(p),1,p);self.assertIn(p,imports);self.assertTrue((MOD/p).is_file())
  self.assertEqual(xml.getroot().get('version'),'268')
  action=xml.find("./InGameActions/AddUserInterfaces[@id='SPC_B241_CapitalPanel']");self.assertEqual(action.findtext('File'),'UI/CapitalInvestmentPanel.xml')
 def test_access_project_is_no_reward_and_uses_native_commerce_icon(self):
  from test_b239_commerce_integration import SQLAndPackage
  # Inherit its read-only loaded-DB copy and current SQL execution, not a native test.
  SQLAndPackage.setUpClass()
  try:
   db=SQLAndPackage.db;self.assertEqual(db.execute("SELECT Cost,RequiredBuilding FROM Projects WHERE ProjectType='PROJECT_SPC_CAPITAL_INVESTMENT'").fetchone(),(1,'BUILDING_SPC_CAPITAL_ACCESS'))
   self.assertEqual(db.execute("SELECT InternalOnly,CitizenSlots,Housing FROM Buildings WHERE BuildingType='BUILDING_SPC_CAPITAL_ACCESS'").fetchone(),(1,0,0))
   self.assertFalse(db.execute("SELECT 1 FROM ProjectCompletionModifiers WHERE ProjectType='PROJECT_SPC_CAPITAL_INVESTMENT'").fetchone())
  finally:SQLAndPackage.tearDownClass()
  line=next(x for x in (MOD/'Data/Icons.sql').read_text().splitlines()if "'ICON_PROJECT_SPC_CAPITAL_INVESTMENT'" in x);self.assertIn('ICON_PROJECT_ENHANCE_DISTRICT_COMMERCIAL_HUB',line)

if __name__=='__main__':unittest.main()
