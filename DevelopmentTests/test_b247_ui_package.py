"""B247 UI/current native definitions. No real layout or growth PASS claimed."""
from pathlib import Path
import json
import os
import sqlite3
import zlib
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]
M=R/'Mod'

def ui():
 l=LuaRuntime(unpack_returned_tuples=True)
 l.execute('''
 GameInfo={Units={[7]={UnitType='UNIT_SPC_RESTRUCTURING_TEAM'}},UnitCommands={UNITCOMMAND_DELETE={Hash=99}}}
 Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return 5 end};PlayerOperations={EXECUTE_SCRIPT=100}
 u={GetUnitType=function()return 7 end,GetOwner=function()return 0 end,GetID=function()return 12 end,GetX=function()return 8 end,GetY=function()return 9 end}
 selected=u;sent={};g_isOkayToProcess=true
 UI={GetHeadSelectedUnit=function()return selected end,RequestPlayerOperation=function(pid,op,p)sent[#sent+1]=p end}
 Locale={Lookup=function(k,...)return k end};ExposedMembers={SPC_RestructuringViews={}}
 function AddActionToTable(a,row,disabled,tip,tag,callback)a.SPECIFIC[#a.SPECIFIC+1]={Disabled=disabled,CallbackFunc=callback,userTag=tag,helpString=tip}end
 function make()return {displayOrder={'MOVE','SPECIFIC'},MOVE={{userTag=1}},SPECIFIC={{userTag=99},{userTag=2}}}end
 v={owner=0,unit=12,x=8,y=9,turn=5,legal=true,cityName='City',potential=3,action='LIQUIDATE'};ExposedMembers.SPC_RestructuringViews['0:12']=v
 ''')
 l.execute((M/'RestructuringUI.lua').read_text());return l

class UI(unittest.TestCase):
 def test_only_own_delete_removed_native_move_idle_kept(self):
  ui().execute("local a=SPCRestructuringUI.Actions(u,make());assert(#a.MOVE==1 and #a.SPECIFIC==2 and a.SPECIFIC[1].userTag==2 and not a.SPECIFIC[2].Disabled);assert(SPCRestructuringUI.BlockDelete(99) and not SPCRestructuringUI.BlockDelete(1))")
 def test_preview_then_explicit_confirm_request_no_mutation_from_open(self):
  ui().execute("SPCRestructuringUI.SelectedChanged();assert(#sent==1 and sent[1].Action=='REST_READ');local a=SPCRestructuringUI.Actions(u,make());a.SPECIFIC[2].CallbackFunc();assert(sent[2].Action=='REST_PREPARE');v.prepared='p';a=SPCRestructuringUI.Actions(u,make());a.SPECIFIC[3].CallbackFunc();assert(sent[3].Action=='REST_CONFIRM' and sent[3].PlanToken=='p')")
 def test_stale_turn_position_and_other_selection_cannot_confirm(self):
  for change in ('v.turn=4','v.x=99','v.owner=3'):
   with self.subTest(change=change):ui().execute(change+";local a=SPCRestructuringUI.Actions(u,make());assert(a.SPECIFIC[2].Disabled)")
  ui().execute("v.prepared='p';local a=SPCRestructuringUI.Actions(u,make());selected=nil;a.SPECIFIC[3].CallbackFunc();assert(#sent==0)")
 def test_existing_panel_routes_delete_hash_prompt_and_captured_unit_guard(self):
  s=(M/'UI/ExpeditionSpyUnitPanel.lua').read_text()
  self.assertIn('BlockDelete(select(2,...))',s)
  self.assertIn('function OnPromptToDeleteUnit',s);self.assertIn('SPCRestructuringUI.IsTeam(UnitManager.GetUnit(id.player,id.id))',s)
 def test_current_and_legacy_institutions_render_without_old_active(self):
  from test_culture_institutions import display
  l=display();l.execute("v.institutionArchive={RESEARCH=4,CULTURE=3,COMMERCE=4};v.specialization='NONE';v.potential=3;v.active=0;v.progression='REALLOCATING';LuaEvents.SPC_PresentationChanged();assert(#rows.items==11);for _,r in ipairs(rows.items)do assert(r.State.text=='历史机构')end;v.specialization='CULTURE';v.progression='SETTLED';v.active=3;LuaEvents.SPC_PresentationChanged();assert(#rows.items==12 and rows.items[7].State.text=='当前' and rows.items[4].State.text=='历史机构')")

class Definitions(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from project_paths import external_database
  with sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True)as src:
   cls.db=sqlite3.connect(':memory:');src.backup(cls.db)
  cls.db.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode())) # fixture hash, not native API proof
  cls.before=set(cls.db.execute('PRAGMA foreign_key_check').fetchall())
  cls.db.executescript((M/'Data/Restructuring.sql').read_text())
 @classmethod
 def tearDownClass(cls):cls.db.close()
 def test_fixed_cost_no_population_purchase_or_escalation(self):
  row=self.db.execute("SELECT Cost,PopulationCost,CostProgressionModel,PurchaseYield,CanTrain,Spy,CanCapture,CanRetreatWhenCaptured FROM Units WHERE UnitType='UNIT_SPC_RESTRUCTURING_TEAM'").fetchone()
  self.assertEqual(row,(500,0,'NO_COST_PROGRESSION',None,1,0,0,1))
 def test_exact_training_gate_and_no_new_foreign_key_error(self):
  self.assertEqual(self.db.execute("SELECT PrereqBuilding FROM Unit_BuildingPrereqs WHERE Unit='UNIT_SPC_RESTRUCTURING_TEAM'").fetchall(),[('BUILDING_SPC_RESTRUCTURING_ACCESS',)])
  self.assertFalse(set(self.db.execute('PRAGMA foreign_key_check').fetchall())-self.before)
 def test_nonfood_minus75_and_native_growth_family(self):
  args=self.db.execute("SELECT m.ModifierId,m.ModifierType,a.Value FROM BuildingModifiers b JOIN Modifiers m USING(ModifierId) JOIN ModifierArguments a USING(ModifierId) WHERE b.BuildingType='BUILDING_SPC_REALLOCATING' AND a.Name='Amount'").fetchall()
  self.assertEqual(len(args),6);self.assertTrue(all(float(r[2])==-75 for r in args))
  self.assertFalse(any(r[0].endswith('FOOD') for r in args))
  self.assertEqual(self.db.execute("SELECT CollectionType,EffectType FROM DynamicModifiers WHERE ModifierType='MODIFIER_SINGLE_CITY_ADJUST_CITY_GROWTH'").fetchone(),('COLLECTION_OWNER','EFFECT_ADJUST_CITY_GROWTH'))
 def test_internal_carriers_are_non_specialist_empty_markers(self):
  rows=self.db.execute("SELECT InternalOnly,CitizenSlots,Housing,PrereqDistrict FROM Buildings WHERE BuildingType IN ('BUILDING_SPC_REALLOCATING','BUILDING_SPC_RESTRUCTURING_ACCESS')").fetchall()
  self.assertEqual(rows,[(1,0,0,'DISTRICT_CITY_CENTER')]*2)

class Package(unittest.TestCase):
 def test_changed_runtime_language_and_asset_closure(self):
  from lupa.lua51 import LuaRuntime as Lua51
  import subprocess
  files=subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines()+subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines()
  compiler=Lua51(unpack_returned_tuples=True).eval('function(s) local f,e=loadstring(s);return f~=nil,e end')
  for p in files:
   if p.startswith('Mod/') and p.endswith('.lua'):
    ok,e=compiler((R/p).read_text());self.assertTrue(ok,(p,e))
  root=ET.parse(M/'SpecializationP0.modinfo').getroot();self.assertEqual(root.get('version'),'274')
  listed=[e.text for e in root.findall('./Files/File')];self.assertEqual(len(listed),len(set(listed)))
  actual={str(p.relative_to(M))for p in M.rglob('*')if p.is_file()and p.name not in ('.DS_Store','SpecializationP0.modinfo')};self.assertEqual(set(listed),actual)
  for p in ['Restructuring.lua','RestructuringModel.lua','RestructuringUI.lua']:
   self.assertIn(p,[e.text for e in root.findall('./InGameActions/ImportFiles/File')])
  art=ET.parse(M/'ArtDefs/Units.artdef');names=[e.get('text') for e in art.findall('.//m_Name')];self.assertEqual(names.count('UNIT_SPC_RESTRUCTURING_TEAM'),1)
 def test_no_frame_or_timer_fallback(self):
  for path in ['Restructuring.lua','RestructuringUI.lua','RestructuringModel.lua']:
   s=(M/path).read_text()
   for call in ['SetUpdate(',"'SystemUpdateUI'",'ContextPtr:SetUpdate','Automation.GetTime','os.clock','collectgarbage(']:self.assertNotIn(call,s)
 def test_localized_actions_and_existing_art_only(self):
  d=sqlite3.connect(':memory:');d.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT,PRIMARY KEY(Language,Tag))');d.executescript((M/'Text/Restructuring.sql').read_text())
  names=dict(d.execute("SELECT Tag,Text FROM LocalizedText WHERE Language='zh_Hans_CN'"));self.assertEqual(names['LOC_SPC_REST_LIQUIDATE'],'资产清算');self.assertEqual(names['LOC_SPC_REST_CONFIGURE'],'资产配置');self.assertEqual(names['LOC_SPC_COMMERCE_INSTITUTION_4'],'资本信托')
  self.assertIn('ICON_UNIT_BUILDER',(M/'Data/Icons.sql').read_text())

if __name__=='__main__':unittest.main()
