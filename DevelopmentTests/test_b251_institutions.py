"""B251 actual UI/Store: previews, scalar history, isolated unknowns and assets.
Local proof only; native icon loading/font/layout remains a visual acceptance.
"""
from pathlib import Path
import sqlite3
import struct
import unittest
import xml.etree.ElementTree as ET
from test_culture_institutions import display
from test_store_write_boundaries import fixture
ROOT=Path(__file__).resolve().parents[1]

class Presentation(unittest.TestCase):
 def test_all_four_previews_preserve_current_and_historical_meanings(self):
  l=display();l.execute("""
   v.potential=1;v.active=1;LuaEvents.SPC_PresentationChanged()
   assert(#rows.items==4 and rows.items[1].State.text=='当前')
   assert(rows.items[4].State.text=='尚未建立' and rows.items[4].Top.tip:find('未来机构预览',1,true))
   assert(rows.items[1].Name.color=='Gold' and rows.items[1].State.color=='Gold')
   assert(rows.items[2].Name.color=='White' and rows.items[2].Name.alpha<rows.items[1].Name.alpha)
   v.potential=4;v.active=1;LuaEvents.SPC_PresentationChanged()
   assert(rows.items[4].State.text=='未激活' and rows.items[4].Name.alpha>.8)
   v.active=4;LuaEvents.SPC_PresentationChanged()
   assert(rows.items[1].Name.color=='White' and rows.items[4].Name.color=='Gold')
  """)
 def test_dialogue_values_below_own_ability_before_next_and_zero_refresh(self):
  display().execute("""
   v.institutionSummary={known=true,dialogue=35,insights=6};LuaEvents.SPC_PresentationChanged()
   local tip=rows.items[3].Top.tip
   assert(tip:find('已累计巨作旅游业绩倍率：+35%',1,true)<tip:find('风雅熏陶',1,true))
   assert(rows.items[4].Top.tip:find('文化见闻：6 份',1,true))
   v.institutionSummary.dialogue=0;v.institutionSummary.insights=0;LuaEvents.SPC_PresentationChanged()
   assert(rows.items[3].Top.tip:find('倍率：+0%',1,true) and rows.items[4].Top.tip:find('文化见闻：0 份',1,true))
  """)
 def test_unknown_is_not_zero_or_not_started_and_stale_mirror_clears_numbers(self):
  display().execute("""
   v.institutionSummary={known=true,dialogue=35,insights=6};LuaEvents.SPC_PresentationChanged()
   ExposedMembers.SPC_P0.CityPresentationView={owner=0,cityID=4,error='unknown'};LuaEvents.SPC_PresentationChanged()
   assert(rows.items[3].Top.tip:find('当前数值待确认',1,true))
   assert(not rows.items[3].Top.tip:find('倍率：+35%',1,true) and not rows.items[3].Top.tip:find('倍率：+0%',1,true))
   ExposedMembers.SPC_P0.CityPresentationView=v;v.specialization='RESEARCH';v.institutionSummary={known=false};LuaEvents.SPC_PresentationChanged()
   assert(rows.items[4].Top.tip:find('当前数值待确认',1,true) and not rows.items[4].Top.tip:find('尚未开始积累',1,true))
  """)
 def test_research_reputation_engineering_and_standardization(self):
  display().execute("""
   v.specialization='RESEARCH';v.institutionSummary={known=true,tradition={age=10,percent=10,nextAge=20,state='COUNTING'}};LuaEvents.SPC_PresentationChanged()
   assert(rows.items[4].Top.tip:find('已累计 10 回合',1,true) and rows.items[4].Top.tip:find('距下一档还需 10 回合',1,true))
   v.specialization='COMMERCE';v.institutionSummary={known=true,reputation={age=21,state='COUNTING'}};LuaEvents.SPC_PresentationChanged()
   assert(rows.items[4].Top.tip:find('信誉 21/40',1,true) and rows.items[4].Top.tip:find('+10.5%',1,true))
   v.specialization='INDUSTRY';v.institutionSummary={known=true,engineering=2,templatesKnown=true,buildingTemplates=7,districtTemplates=3};LuaEvents.SPC_PresentationChanged()
   assert(rows.items[3].Top.tip:find('建筑 7 项，区域 3 项',1,true))
   assert(rows.items[3].Top.tip:find('生产力 +14%',1,true) and rows.items[3].Top.tip:find('折扣 4%',1,true))
   assert(rows.items[4].Top.tip:find('已完成研习：2 层',1,true)<rows.items[4].Top.tip:find('工程实践',1,true))
   v.active=3;LuaEvents.SPC_PresentationChanged()
   assert(rows.items[3].Top.tip:find('生产力 +10%',1,true) and rows.items[3].Top.tip:find('折扣 0%',1,true))
   v.active=2;LuaEvents.SPC_PresentationChanged();assert(rows.items[3].Top.tip:find('当前不提供标准化',1,true))
   assert(rows.items[3].Top.tip:find('建筑 7 项',1,true))
  """)
 def test_metric_no_change_and_unrelated_revision_do_not_rebuild(self):
  display().execute("""
   v.institutionSummary={known=true,dialogue=5,insights=1,revision=2};LuaEvents.SPC_PresentationChanged()
   local n=resets;v.institutionSummary.revision=3
   for i=1,1000 do LuaEvents.SPC_PresentationChanged()end
   assert(n==resets)
   v.institutionSummary.insights=2;LuaEvents.SPC_PresentationChanged();assert(resets==n+1)
  """)
 def test_new_city_cannot_inherit_old_city_summary(self):
  display().execute("""
   v.institutionSummary={known=true,dialogue=35,insights=6};LuaEvents.SPC_PresentationChanged()
   city={GetID=function()return 7 end,GetOwner=function()return 0 end,GetX=function()return 1 end,GetY=function()return 2 end}
   ViewPanelBreakdown({Owner=0,City=city,BuildingsAndDistricts={}});assert(Controls.InstitutionContainer.hidden)
  """)

class StoreSummary(unittest.TestCase):
 def runtime(self):
  l=fixture();l.execute('T.start();c=T.research(1);other=T.fresh(2);T.register(other);T.complete(other,"DISTRICT_THEATER");st=shared.CityProgressionStore');return l
 def test_actual_store_detached_scalars_no_writes_no_other_record_visits(self):
  self.runtime().execute("""
   st.AddExpeditionInsight(0,c,'CIVILIZATION_TEST','PEOPLE',T.now())
   local original=T.encode(T.record(c));local before=T.writes();T.scanReset()
   local s=st.InstitutionSummary(0,c)
   assert(s.known and s.tradition.age==0 and s.dialogue==0 and s.engineering==0 and s.insights==1)
   assert(s.reference.cityID==c:GetID() and s.templatesKnown==false)
   assert(not s.records and not s.used and not s.receipts)
   s.tradition.age=400;s.reference.cityID=987;s.insights=50
   assert(T.encode(T.record(c))==original and T.writes()==before and T.scanCount()==0)
   assert(st.InstitutionSummary(0,other).insights==0)
  """)
 def test_actual_presentation_request_publishes_values_and_isolates_read_failure(self):
  l=self.runtime()
  source=(ROOT/'Mod/Gameplay.lua').read_text()
  branch=source.split("  if params.Action=='CITY_PRESENTATION_READ' then",1)[1].split("  if type(params.Action)=='string' and params.Action:find('^INSPIRE_')",1)[0]
  l.execute("function presentation(params)local playerID=0;if params.Action=='CITY_PRESENTATION_READ' then"+branch+"end")
  l.execute("""
   GameConfiguration.GetGameSpeedType=function()return 'GAMESPEED_STANDARD'end
   GameInfo.GameSpeeds={GAMESPEED_STANDARD={CostMultiplier=100}}
   local before=T.writes()
   presentation({Action='CITY_PRESENTATION_READ',CityID=c:GetID(),Token='read'})
   local v=shared.CityPresentationView
   assert(not v.error and v.token=='read' and v.institutionSummary.known and v.institutionSummary.tradition.percent==5)
   assert(v.institutionSummary.tradition.nextAge==10 and T.writes()==before)
   st.InstitutionSummary=function()error('unavailable')end
   presentation({Action='CITY_PRESENTATION_READ',CityID=c:GetID(),Token='held'})
   assert(not shared.CityPresentationView.error and shared.CityPresentationView.potential==4)
   assert(shared.CityPresentationView.institutionSummary.known==false and T.writes()==before)
  """)
 def test_wrong_owner_failure_and_known_empty(self):
  self.runtime().execute("""
   assert(not pcall(st.InstitutionSummary,1,c))
   local s=st.InstitutionSummary(0,other);assert(s.known and s.tradition==false and s.reputation==false and s.insights==0)
  """)
 def test_no_lazy_capture_uninitialized_or_legacy_template_history(self):
  self.runtime().execute("""
   local r=T.storage(c).Read();r.templatesCaptured=false;r.templateLifecycle=nil
   assert(T.write(c,r));T.reload();st=shared.CityProgressionStore
   local before=T.writes();local s=st.InstitutionSummary(0,c)
   assert(s.known and not s.templatesKnown and T.writes()==before and not T.record(c).templatesCaptured)
  """)
 def test_template_counts_pending_and_history_validation(self):
  l=fixture();l.execute("""
   T.start();c=T.fresh(1);T.register(c);T.complete(c,'DISTRICT_INDUSTRIAL_ZONE');st=shared.CityProgressionStore
   local r=T.record(c);local t={schema=1,uid='STD:'..r.base.token,foundation=r.base.token,x=c:GetX(),y=c:GetY(),initialized=true,revision=2,learned={BUILDING_TEST={district='DISTRICT_CAMPUS',tier=1,turn=0,evidence='OBSERVED'}}}
   st.WriteTemplates(c,nil,t)
   shared.Standardization={ValidateHistory=function(city,v)return SPCCityIdentityRead.ValidateTemplates(v,v.foundation,city:GetX(),city:GetY())end}
   local before=T.writes();local s=st.InstitutionSummary(0,c)
   assert(s.templatesKnown and s.buildingTemplates==1 and s.districtTemplates==nil and T.writes()==before)
   shared.Standardization.ValidateHistory=function()error('corrupt')end
   s=st.InstitutionSummary(0,c);assert(s.known and not s.templatesKnown)
  """)
 def test_summary_survives_fixture_reload_without_new_state(self):
  self.runtime().execute("""
   st.AddExpeditionInsight(0,c,'CIVILIZATION_TEST','WORKS',T.now())
   local before=T.encode(st.InstitutionSummary(0,c));T.reload();st=shared.CityProgressionStore
   assert(T.encode(st.InstitutionSummary(0,c))==before)
  """)

class Package(unittest.TestCase):
 def test_16_icons_two_reviewed_atlases_and_package_closure(self):
  db=sqlite3.connect(':memory:')
  db.executescript('CREATE TABLE IconDefinitions(Name TEXT PRIMARY KEY,Atlas TEXT,"Index" INTEGER);CREATE TABLE IconTextureAtlases(Name TEXT,IconSize INTEGER,IconsPerRow INTEGER,IconsPerColumn INTEGER,Filename TEXT,PRIMARY KEY(Name,IconSize));')
  db.executescript((ROOT/'Mod/Data/Icons.sql').read_text())
  icons=db.execute("SELECT Name,\"Index\" FROM IconDefinitions WHERE Atlas='ICON_ATLAS_SPC_INSTITUTIONS' ORDER BY \"Index\"").fetchall()
  self.assertEqual(len(icons),16)
  for n,(name,index) in enumerate(icons):self.assertEqual(index,n)
  for size in (32,64):
   a=db.execute('SELECT IconsPerRow,IconsPerColumn,Filename FROM IconTextureAtlases WHERE Name=? AND IconSize=?',('ICON_ATLAS_SPC_INSTITUTIONS',size)).fetchone()
   self.assertEqual(a,(4,4,f'SPC_Institutions_{size}.dds'))
   b=(ROOT/'Mod/Textures'/a[2]).read_bytes();self.assertEqual(b[:4],b'DDS ');self.assertEqual(b[84:88],b'DXT5')
   self.assertEqual(struct.unpack_from('<II',b,12),(4*size,4*size));self.assertEqual(len(b),128+(4*size)**2)
  root=ET.parse(ROOT/'Mod/SpecializationP0.modinfo').getroot();self.assertEqual(root.get('version'),'278')
  listed=[x.text for x in root.findall('./Files/File')]
  actual={str(p.relative_to(ROOT/'Mod'))for p in (ROOT/'Mod').rglob('*')if p.is_file()and p.name not in ('.DS_Store','SpecializationP0.modinfo')}
  self.assertEqual(set(listed),actual);self.assertEqual(len(listed),len(set(listed)))
  imports={x.text for x in root.findall('./InGameActions/ImportFiles/File')}
  self.assertTrue({f'Textures/SPC_Institutions_{s}.dds'for s in (32,64)}<=imports)
 def test_reserved_width_spacing_and_no_new_update_or_write_paths(self):
  tree=ET.parse(ROOT/'Mod/UI/Institutions.xml')
  controls={x.get('ID'):x for x in tree.getroot().iter()if x.get('ID')}
  self.assertEqual(controls['InstitutionRows'].get('StackPadding'),'3')
  self.assertEqual(controls['Icon'].get('Size'),'32,32')
  self.assertEqual(controls['State'].get('Anchor'),'R,C')
  self.assertEqual(controls['Name'].get('TruncateWidth'),'parent')
  self.assertNotIn('Stage',controls)
  source=(ROOT/'Mod/CityProgressionStore.lua').read_text()
  function=source.split(' function d.InstitutionSummary(pid,c)',1)[1].split(' function d.InstitutionArchive',1)[0]
  for bad in ('save(', 'ReadTemplates(', 'Refresh(', 'Discover(', ':Members(', 'SetProperty(', 'SetUpdate('):self.assertNotIn(bad,function)
  self.assertIn('PRESENTATION_COMMIT_IN_PROGRESS',function)
 def test_changed_lua_compiles_in_lua51(self):
  from lupa.lua51 import LuaRuntime
  l=LuaRuntime(unpack_returned_tuples=True);compile=l.eval('function(s)local f,e=loadstring(s);return f~=nil,e end')
  for filename in ('Gameplay.lua','CityProgressionStore.lua','InstitutionPresentation.lua','UI/InstitutionOverview.lua','UI/Institutions.lua','Probe.lua'):
   ok,why=compile((ROOT/'Mod'/filename).read_text());self.assertTrue(ok,(filename,why))

if __name__=='__main__':unittest.main()
