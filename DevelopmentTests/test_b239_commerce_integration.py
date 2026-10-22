"""B239 retirement + SQL/package boundary checks. LOCAL_SIMULATION only.
The configured loaded game database is opened read-only and copied into memory.
These checks do not establish native Gold settlement or UI visual acceptance.
"""
from pathlib import Path
import re
import sqlite3
import unittest
import zlib
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from project_paths import external_database

ROOT=Path(__file__).resolve().parents[1]
MOD=ROOT/'Mod'
SETUP=r"""
ExposedMembers={};hooks={};removeCount=0;reads=0;unproven={};failRemove=nil;unknownPresence=nil
local function events()
 return setmetatable({},{__index=function(t,k)
  local e={Add=function(f)hooks[k]=hooks[k] or {};table.insert(hooks[k],f)end}
  rawset(t,k,e);return e
 end})
end
Events=events();GameEvents=events();Game={GetCurrentGameTurn=function()return 1 end}
function emit(name,...)for _,fn in ipairs(hooks[name] or {})do fn(...)end end
cities={}
for i=1,3 do
 local c={id=i,owner=i==3 and 3 or 0,built={}};cities[i]=c
 function c:GetOwner()return self.owner end
 function c:GetID()return self.id end
 function c:GetBuildings()return self.built end
 function c:GetBuildQueue()return self.built end
end
Players={}
for _,pid in ipairs({0,3})do
 Players[pid]={GetCities=function()
  local own={};for _,c in ipairs(cities)do if c.owner==pid then own[#own+1]=c end end
  return {Members=function()return ipairs(own)end}
 end}
end
P={IsTestPlayer=function(pid)return pid==0 end,Count=function()end,Field=function(t,k)return t[k]end}
P.Info=function(tab,name)if tab=='Buildings'then return {Index=name,BuildingType=name,InternalOnly=1}end end
P.HasBuilding=function(b,id)reads=reads+1;if id==unknownPresence then return nil end;return b[id]==true end
P.RemoveBuilding=function(b,id)removeCount=removeCount+1;if failRemove==id then return end;b[id]=nil end
P.CreateBuilding=function(b,id)error('retirement must never create a building')end
exits={};shared={CityProgressionStore={}}
shared.CityProgressionStore.HistoricalReference=function(c)
 assert(c.owner==0 and not unproven[c.id],'STORE_REFERENCE_UNKNOWN')
 return {owner=c.owner,cityID=c.id,token='C'..c.id}
end
shared.CityProgressionStore.RegisterExit=function(name,fn)exits[name]=fn end
shared.CityProgressionStore.RemoveOwned=function(c,loss,names)
 assert(loss.confirmed,'EXIT_NOT_CONFIRMED')
 for _,id in ipairs(names)do if c.built[id]then P.RemoveBuilding(c.built,id);assert(not c.built[id],'EXIT_REMOVE_UNCONFIRMED')end end
end
shared.EffectiveFacts={Read=function(pid,c)return {specialization='COMMERCE',active=3,potential=3}end}
function seed(c)
 c.built.KEEP_EXTERNAL=true;c.built.BUILDING_SPC_COMMERCE_GOLD_0=true
 for _,yield in ipairs({'SCIENCE','CULTURE','PRODUCTION'})do for bit=0,15 do
  c.built['BUILDING_SPC_B061_'..yield..'_'..bit]=true
 end end
end
function remaining(c)
 local count=0;for _,yield in ipairs({'SCIENCE','CULTURE','PRODUCTION'})do for bit=0,15 do
  if c.built['BUILDING_SPC_B061_'..yield..'_'..bit]then count=count+1 end
 end end;return count
end
"""

def retirement_runtime():
 lua=LuaRuntime(unpack_returned_tuples=True)
 lua.globals().include=lambda name:lua.execute((MOD/(name+'.lua')).read_text())
 lua.execute(SETUP);lua.execute((MOD/'CommerceConvergence.lua').read_text())
 lua.execute('SPCCommerceConvergence.Start(P,shared,{retired=true});d=shared.CommerceConvergence')
 return lua

class Retirement(unittest.TestCase):
 def check(self,body):retirement_runtime().execute(body)
 def test_exact_48_supported_confirmed_cleanup_preserves_other_owners(self):
  self.check("seed(cities[1]);seed(cities[2]);seed(cities[3]);unproven[2]=true;d.Audit();assert(remaining(cities[1])==0 and remaining(cities[2])==48 and remaining(cities[3])==48);assert(removeCount==48);for _,c in ipairs(cities)do assert(c.built.KEEP_EXTERNAL and c.built.BUILDING_SPC_COMMERCE_GOLD_0)end;assert(d.errors['0:2']);assert(not pcall(d.Withdraw,cities[3]))")
 def test_retired_mode_never_subscribes_old_global_output_or_native_forward_events(self):
  self.check("assert(hooks.LoadScreenClose and #hooks.LoadScreenClose==1);for _,n in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','CityWorkerChanged','GovernorChanged','PlayerTurnActivated'})do assert(not hooks[n],n)end;local n=removeCount;assert(d.Control(0,cities[1],'READ')==nil);for _,a in ipairs({'AUTO','OFF','TEST5'})do assert(not pcall(d.Control,0,cities[1],a))end;assert(removeCount==n)")
 def test_unknown_presence_preflight_prevents_partial_withdrawal(self):
  self.check("seed(cities[1]);unknownPresence='BUILDING_SPC_B061_CULTURE_7';assert(not pcall(d.Withdraw,cities[1]));assert(remaining(cities[1])==48 and removeCount==0)")
 def test_failed_remove_holds_and_explicit_retry_cleans_exactly(self):
  self.check("seed(cities[1]);failRemove='BUILDING_SPC_B061_SCIENCE_0';d.Audit({player=0});assert(d.errors['0:1'] and remaining(cities[1])==48);assert(cities[1].built.BUILDING_SPC_COMMERCE_GOLD_0);failRemove=nil;d.Audit({player=0});assert(not d.errors['0:1'] and remaining(cities[1])==0);local n=removeCount;d.Audit({player=0});assert(removeCount==n)")
 def test_confirmed_loss_callback_exact_ids_only(self):
  self.check("seed(cities[3]);assert(not pcall(exits.CommerceConvergence,cities[3],{}));assert(remaining(cities[3])==48);exits.CommerceConvergence(cities[3],{confirmed=true});assert(remaining(cities[3])==0 and cities[3].built.KEEP_EXTERNAL and cities[3].built.BUILDING_SPC_COMMERCE_GOLD_0)")
 def test_three_old_specialist_carriers_retire_without_touching_new_gold(self):
  lua=retirement_runtime();lua.execute((MOD/'Lv3Effects.lua').read_text())
  lua.execute("""
for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY'})do cities[1].built['BUILDING_SPC_DEV_LV3_COM_'..kind]=true end
cities[1].built.KEEP_EXTERNAL=true;cities[1].built.BUILDING_SPC_COMMERCE_GOLD_2=true
SPCLv3Effects.Start(P,shared,{retireCommerce=true});emit('LoadScreenClose')
for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY'})do assert(not cities[1].built['BUILDING_SPC_DEV_LV3_COM_'..kind])end
assert(cities[1].built.KEEP_EXTERNAL and cities[1].built.BUILDING_SPC_COMMERCE_GOLD_2)
""")
 def test_actual_new_writer_holds_legacy_until_confirmed_retirement(self):
  from test_b239_commerce import fixture
  lua=fixture();lua.execute((MOD/'CommerceConvergence.lua').read_text())
  lua.execute("""
SPCCommerceConvergence.Start(P,shared,{retired=true});local legacy=shared.CommerceConvergence
cities[2].present.BUILDING_SPC_B061_SCIENCE_0=true;removeFail=true
assert(not toggle(2,'DISTRICT_CAMPUS',true));assert(ownedGold(cities[2])==0)
assert(cities[2].present.BUILDING_SPC_B061_SCIENCE_0)
removeFail=false;com.SourceChanged(0,2);assert(not cities[2].present.BUILDING_SPC_B061_SCIENCE_0)
assert(toggle(2,'DISTRICT_CAMPUS',true));assert(ownedGold(cities[2])==15)
""")

class SQLAndPackage(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.db=sqlite3.connect(':memory:')
  cls.db.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode())) # local fixture hash only
  src=sqlite3.connect(external_database(ROOT).as_uri()+'?mode=ro',uri=True)
  try:src.backup(cls.db)
  finally:src.close()
  # Rebuild only exact Commerce definitions in the memory copy, including B241 access.
  own=['BUILDING_SPC_COMMERCIALIZATION_ACCESS','BUILDING_SPC_CAPITAL_ACCESS']+['BUILDING_SPC_COMMERCE_GOLD_'+str(b) for b in range(31)]
  for ident in own:
   for table,col in [('ModifierArguments','ModifierId'),('BuildingModifiers','BuildingType'),('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]:
    cls.db.execute('DELETE FROM '+table+' WHERE '+col+'=?',(ident,))
  for project in ('PROJECT_SPC_COMMERCIALIZATION','PROJECT_SPC_CAPITAL_INVESTMENT'):
   cls.db.execute('DELETE FROM Projects WHERE ProjectType=?',(project,))
   cls.db.execute('DELETE FROM Types WHERE Type=?',(project,))
  cls.db.execute('DROP TABLE IF EXISTS SPC_CommerceGold')
  cls.db.executescript((MOD/'Data/Commerce.sql').read_text())
 @classmethod
 def tearDownClass(cls):cls.db.close()
 def test_gold_definitions_match_owned_directory_and_city_effect(self):
  rows=self.db.execute('SELECT Bit,Amount,CarrierType FROM SPC_CommerceGold ORDER BY Bit').fetchall()
  self.assertEqual(len(rows),31)
  for bit,amount,carrier in rows:
   self.assertEqual(amount,2**bit);self.assertEqual(carrier,'BUILDING_SPC_COMMERCE_GOLD_'+str(bit))
   self.assertEqual(dict(self.db.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(carrier,))),{'YieldType':'YIELD_GOLD','Amount':str(amount)})
   modifier=self.db.execute('SELECT ModifierType FROM Modifiers WHERE ModifierId=?',(carrier,)).fetchone()[0]
   self.assertEqual(self.db.execute('SELECT CollectionType,EffectType FROM DynamicModifiers WHERE ModifierType=?',(modifier,)).fetchone(),('COLLECTION_OWNER','EFFECT_ADJUST_CITY_YIELD_CHANGE'))
   self.assertEqual(self.db.execute('SELECT InternalOnly,CitizenSlots,Housing,PrereqDistrict FROM Buildings WHERE BuildingType=?',(carrier,)).fetchone(),(1,0,0,'DISTRICT_CITY_CENTER'))
   self.assertEqual(self.db.execute('SELECT ModifierId FROM BuildingModifiers WHERE BuildingType=?',(carrier,)).fetchall(),[(carrier,)])
 def test_single_configuration_project_has_no_completion_reward(self):
  row=self.db.execute("SELECT Cost,RequiredBuilding,PrereqDistrict FROM Projects WHERE ProjectType='PROJECT_SPC_COMMERCIALIZATION'").fetchone()
  self.assertEqual(row,(1,'BUILDING_SPC_COMMERCIALIZATION_ACCESS','DISTRICT_CITY_CENTER'))
  self.assertFalse(self.db.execute("SELECT 1 FROM ProjectCompletionModifiers WHERE ProjectType='PROJECT_SPC_COMMERCIALIZATION'").fetchall())
 def test_package_files_and_shared_imports_cover_new_runtime_paths(self):
  root=ET.parse(MOD/'SpecializationP0.modinfo').getroot();files={e.text for e in root.findall('./Files/File')}
  required={'CommerceModel.lua','CommerceCalculation.lua','Commerce.lua','UI/CommerceUI.lua','Data/Commerce.sql','Text/Commerce.sql','UI/CommercePanel.lua','UI/CommercePanel.xml'}
  self.assertTrue(required<=files)
  imports={e.text for e in root.findall('./InGameActions/ImportFiles/File')}
  self.assertTrue({'CommerceModel.lua','CommerceCalculation.lua','Commerce.lua','UI/CommerceUI.lua'}<=imports)
  self.assertTrue(all((MOD/p).is_file() for p in required))
  actions=root.find('InGameActions')
  expected={'SPC_B239_Commerce':('UpdateDatabase','Data/Commerce.sql'),'SPC_B239_CommerceText':('UpdateText','Text/Commerce.sql'),'SPC_B239_CommercePanel':('AddUserInterfaces','UI/CommercePanel.xml')}
  for ident,(kind,path) in expected.items():
   matches=[e for e in actions if e.attrib.get('id')==ident]
   self.assertEqual(len(matches),1);self.assertEqual(matches[0].tag,kind);self.assertEqual(matches[0].findtext('File'),path)
 def test_reused_project_icon_alias_and_chinese_localization_keys_exist(self):
  icons=(MOD/'Data/Icons.sql').read_text();alias=next(line for line in icons.splitlines() if "'ICON_PROJECT_SPC_COMMERCIALIZATION'" in line)
  db=sqlite3.connect(':memory:');db.execute('CREATE TABLE IconDefinitions(Name TEXT PRIMARY KEY,Atlas TEXT,"Index" INTEGER)')
  db.execute("INSERT INTO IconDefinitions VALUES ('ICON_PROJECT_ENHANCE_DISTRICT_COMMERCIAL_HUB','NATIVE_PROJECT',8)");db.executescript(alias)
  self.assertEqual(db.execute("SELECT Atlas,\"Index\" FROM IconDefinitions WHERE Name='ICON_PROJECT_SPC_COMMERCIALIZATION'").fetchone(),('NATIVE_PROJECT',8))
  db.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT,PRIMARY KEY(Language,Tag))');db.executescript((MOD/'Text/Commerce.sql').read_text())
  panel=(MOD/'UI/CommercePanel.lua').read_text();keys=set(re.findall(r"L\('([A-Z_]+)'",panel))
  keys.discard('DOMAIN_') # completed dynamic suffixes are enumerated below
  keys.update({'DOMAIN_'+s for s in ('CAMPUS','THEATER','INDUSTRIAL_ZONE','HOLY_SITE','HARBOR')})
  keys.update({'ENABLE','DISABLE','EFFECTIVE','NOT_SELECTED','UNAVAILABLE','NO_WORKERS','INACTIVE','NETWORK_WAIT'})
  for key in keys:
   self.assertTrue(db.execute('SELECT Text FROM LocalizedText WHERE Language=? AND Tag=?',('zh_Hans_CN','LOC_SPC_COMMERCE_'+key)).fetchone(),key)
  db.close()

if __name__=='__main__':unittest.main()
