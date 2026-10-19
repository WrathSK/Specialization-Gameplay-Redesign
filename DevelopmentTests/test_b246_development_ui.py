"""B246 UI protocol, real loaded-HD definitions and package checks, no native PASS."""
import re,sqlite3,unittest,zlib,xml.etree.ElementTree as ET
from pathlib import Path
from lupa.lua55 import LuaRuntime
from test_b239_commerce_ui import SETUP
from project_paths import external_database
R=Path(__file__).resolve().parents[1];MOD=R/'Mod'
def ui():
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(SETUP)
 l.execute((MOD/'UI/DevelopmentInvestmentUI.lua').read_text())
 l.execute(r'''
GameInfo={Buildings={BUILDING_LIB={Name='图书馆'}},Districts={DISTRICT_CAMPUS={Name='学院'}}}
function Controls.Choices:CalculateSize()end;function Controls.Choices:ReprocessAnchoring()end;function Controls.Scroll:CalculateInternalSize()end
instances={};InstanceManager={new=function()return {
 ResetInstances=function()instances={}end,
 GetInstance=function()local i=#instances+1;local o={Root=Controls['Row'..i],Caption=Controls['Caption'..i],State=Controls['State'..i]};instances[i]=o;return o end}end}
local r={owner=0,cityID=9,x=10,y=11,token='city',changes=0}
developmentView={available=true,stage='READY',canSign=true,token='city',reference=r,revision=1,balance=1000,used=0,workers=2,contracts={},options={
 {targetCity=2,targetName='目标城',domain='DISTRICT_CAMPUS',building='BUILDING_LIB',price=400,cost=60,candidates=2,canSign=true,reason='DEVELOPMENT_READY'},
 {targetCity=3,targetName='第二城',domain='DISTRICT_CAMPUS',canSign=false,reason='DEVELOPMENT_PRICE_UNAVAILABLE'}}}
backend={views={['0:9']=developmentView},revision=1};ExposedMembers.SPC_P0.DevelopmentInvestment=backend
function ack(ok,reason)local p=sent[#sent];backend.lastRequest={owner=0,city=9,token=p.Token,accepted=ok~=false,reason=reason};Events.GameCoreEventPublishComplete.Fire()end
''')
 l.execute((MOD/'UI/DevelopmentInvestmentPanel.lua').read_text());l.execute('ContextPtr.initialize()')
 return l
class UI(unittest.TestCase):
 def test_one_open_snapshot_selection_and_hover_never_request(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);assert(#sent==1 and sent[1].Action=='DEVELOPMENT_OPEN');ack();assert(Controls.Confirm.disabled);instances[1].Root.click();instances[2].Root.click();assert(#sent==1 and Controls.Confirm.disabled);instances[1].Root.click();assert(not Controls.Confirm.disabled and #sent==1)")
 def test_scalar_confirmation_and_double_click_latch(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();instances[1].Root.click();Controls.Confirm.click();Controls.Confirm.click();assert(#sent==2 and sent[2].Action=='DEVELOPMENT_CONFIRM' and sent[2].TargetCity==2 and sent[2].Domain=='DISTRICT_CAMPUS' and sent[2].Revision==1)")
 def test_rejection_and_stale_publication_never_retry(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(0,9);ack();instances[1].Root.click();Controls.Confirm.click();ack(false,'DEVELOPMENT_QUOTE_STALE');assert(#sent==2 and Controls.Error.text:find('STALE'));developmentView.quoteStale=true;developmentView.revision=2;Events.GameCoreEventPublishComplete.Fire();assert(Controls.Confirm.disabled and #sent==2);Controls.Refresh.click();assert(#sent==3 and sent[3].Action=='DEVELOPMENT_REFRESH')")
 def test_current_contract_visible_without_source_active_or_route(self):
  ui().execute("developmentView.canSign=false;developmentView.options={};developmentView.used=1;developmentView.contracts.target={target={cityID=2},domain='DISTRICT_CAMPUS',cost=60,debited=60,stage='ACTIVE'};LuaEvents.SPC_DevelopmentOpen(0,9);ack();assert(#instances==1);instances[1].Root.click();assert(Controls.Contract.text:find('60') and Controls.Confirm.disabled)")
 def test_foreign_selection_and_shutdown_close(self):
  ui().execute("LuaEvents.SPC_DevelopmentOpen(1,9);assert(#sent==0);LuaEvents.SPC_DevelopmentOpen(0,9);ack();owner=1;Events.GameCoreEventPublishComplete.Fire();assert(Controls.Window.hidden);owner=0;ContextPtr.shutdown();LuaEvents.SPC_DevelopmentOpen(0,9);assert(#sent==1)")
 def test_action_intercept_never_enqueues_and_only_own_project(self):
  l=ui();l.execute("SPCDevelopmentInvestmentRead={New=function()end};api=SPCDevelopmentInvestmentUI.New(SPCP0,function()end);local item={Type=SPCDevelopmentInvestmentUI.PROJECT};local data={City=c,ProjectItems={item,{Type='OTHER'}}};api.Items(data);assert(item.Cost==0 and item.TurnsLeft==0 and not item.Disabled);assert(not api.Before(c,item,true));assert(#sent==1 and sent[1].Action=='DEVELOPMENT_OPEN');assert(api.Before(c,{Type='OTHER'},false));developmentView.available=false;api.Items(data);assert(#data.ProjectItems==1)")

class Definitions(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.db=sqlite3.connect(':memory:');cls.db.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode()));src=sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True)
  try:src.backup(cls.db)
  finally:src.close()
  cls.db.executescript((MOD/'Data/DevelopmentInvestment.sql').read_text())
 @classmethod
 def tearDownClass(cls):cls.db.close()
 def test_effect_is_exact_district_building_plus50_without_other_arguments(self):
  rows=self.db.execute('SELECT DistrictType,CarrierType FROM SPC_DevelopmentEffects').fetchall();self.assertGreater(len(rows),10)
  for district,carrier in rows:
   self.assertEqual(self.db.execute('SELECT ModifierType FROM Modifiers WHERE ModifierId=?',(carrier,)).fetchone(),('MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION',))
   self.assertEqual(dict(self.db.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(carrier,))),{'DistrictType':district,'Amount':'50'})
   self.assertEqual(self.db.execute('SELECT InternalOnly,CitizenSlots,Housing FROM Buildings WHERE BuildingType=?',(carrier,)).fetchone(),(1,0,0))
 def test_real_hd_branches_are_differently_priced_not_assumed_equal(self):
  rows=self.db.execute("SELECT BuildingType,Cost FROM Buildings WHERE BuildingType IN ('BUILDING_MUSEUM_ART','BUILDING_MUSEUM_ARTIFACT','BUILDING_JNR_OPERA')").fetchall()
  self.assertEqual(len(rows),3);self.assertGreater(len({cost for _,cost in rows}),1)
 def test_nonpurchasable_constructible_catalog_is_preserved(self):
  self.assertGreater(self.db.execute('SELECT COUNT(*) FROM Buildings b JOIN HD_BuildingTiers h USING(BuildingType) JOIN SPC_DevelopmentEffects d ON b.PrereqDistrict=d.DistrictType WHERE b.PurchaseYield IS NULL AND b.InternalOnly=0 AND b.IsWonder=0 AND b.MustPurchase=0').fetchone()[0],0)
 def test_access_project_has_no_reward_and_only_owned_marker(self):
  self.assertEqual(self.db.execute("SELECT Cost,RequiredBuilding FROM Projects WHERE ProjectType='PROJECT_SPC_DEVELOPMENT_INVESTMENT'").fetchone(),(1,'BUILDING_SPC_DEVELOPMENT_ACCESS'))
  self.assertIsNone(self.db.execute("SELECT 1 FROM ProjectCompletionModifiers WHERE ProjectType='PROJECT_SPC_DEVELOPMENT_INVESTMENT'").fetchone())

class Package(unittest.TestCase):
 def test_controls_and_localization_keys(self):
  lua=(MOD/'UI/DevelopmentInvestmentPanel.lua').read_text();xml=ET.parse(MOD/'UI/DevelopmentInvestmentPanel.xml');ids={e.get('ID')for e in xml.iter()if e.get('ID')}
  self.assertTrue(set(re.findall(r'Controls\.([A-Za-z0-9_]+)',lua))<=ids)
  db=sqlite3.connect(':memory:');db.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT,PRIMARY KEY(Language,Tag))');db.executescript((MOD/'Text/DevelopmentInvestment.sql').read_text())
  for k in set(re.findall(r"L\('([A-Z_]+)'",lua))|{'TITLE','HELP','CLOSE','CONFIRM','REFRESH','STATE_ACTIVE','STATE_HELD'}:
   if k.endswith('_'):continue # runtime suffixes checked explicitly below
   self.assertIsNotNone(db.execute('SELECT Text FROM LocalizedText WHERE Tag=?',('LOC_SPC_DEVELOPMENT_'+k,)).fetchone(),k)
  db.close()
 def test_manifest_lists_files_and_context_exactly_once(self):
  root=ET.parse(MOD/'SpecializationP0.modinfo').getroot();files=[e.text for e in root.findall('./Files/File')];imports={e.text for e in root.findall('./InGameActions/ImportFiles/File')}
  for p in ['DevelopmentInvestmentModel.lua','DevelopmentInvestmentCatalog.lua','DevelopmentInvestment.lua','UI/DevelopmentInvestmentRead.lua','UI/DevelopmentInvestmentUI.lua','UI/DevelopmentInvestmentPanel.lua','UI/DevelopmentInvestmentPanel.xml']:
   self.assertEqual(files.count(p),1,p);self.assertIn(p,imports);self.assertTrue((MOD/p).is_file())
  self.assertEqual(root.get('version'),'273');self.assertEqual(root.find("./InGameActions/AddUserInterfaces[@id='SPC_B246_DevelopmentPanel']").findtext('File'),'UI/DevelopmentInvestmentPanel.xml')
 def test_no_timer_or_purchase_permission_gate(self):
  runtime=(MOD/'DevelopmentInvestment.lua').read_text();reader=(MOD/'UI/DevelopmentInvestmentRead.lua').read_text()
  for f in [runtime,reader,(MOD/'UI/DevelopmentInvestmentPanel.lua').read_text()]:
   for forbidden in ['SetUpdate(',"'SystemUpdateUI'",'ChangeGoldBalance(-math.floor','ChangeGoldBalance(math.floor']:
    self.assertNotIn(forbidden,f)
  self.assertNotIn(':CanStartCommand(',reader);self.assertNotIn(':CanPurchase(',reader);self.assertIn('GetPurchaseCost(gold.Index,b.hash)',reader)
 def test_changed_lua_compiles_in_native_language_version(self):
  from lupa.lua51 import LuaRuntime as Lua51
  l=Lua51();compiler=l.eval('function(s) local fn,err=loadstring(s);return fn~=nil,err end')
  for p in [*MOD.glob('DevelopmentInvestment*.lua'),* (MOD/'UI').glob('DevelopmentInvestment*.lua'),MOD/'CityProgressionStore.lua',MOD/'NetworkBridge.lua',MOD/'Commerce.lua',MOD/'Gameplay.lua',MOD/'UI/CrewProjectOrder.lua']:
   okay,error=compiler(p.read_text());self.assertTrue(okay,(p.name,error))

if __name__=='__main__':unittest.main()
