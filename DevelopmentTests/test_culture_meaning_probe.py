"""L2A scoped simulation / SQL evidence. Never a native precision PASS.
Requires configured read-only DebugGameplay and lupa.lua55; reuses maintained
L1 and K engine fixtures. Pinned older version/notification assertions remain
historical and are replaced here only for the explicitly changed contract.
"""
from pathlib import Path
import unittest,xml.etree.ElementTree as ET
import sqlite3,zlib
from project_paths import external_database
import test_culture_aesthetic as ae
from test_p0_k import Fixture

R=Path(__file__).resolve().parents[1];M=R/'Mod'

def database():
 # The external DB may already contain B149 definitions. Reset only the exact
 # test-owned L1 definitions in the disposable memory copy, then apply source.
 # No external DB mutation and no assertion weakened by fixture version drift.
 ro=sqlite3.connect('file:'+str(external_database(R))+'?mode=ro',uri=True)
 d=sqlite3.connect(':memory:');ro.backup(d);ro.close()
 d.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode()))
 carrier='BUILDING_SPC_CULTURE_AESTHETIC'
 for table,col,values in [
  ('BuildingModifiers','BuildingType',[carrier]),('Buildings','BuildingType',[carrier]),('Types','Type',[carrier]),
  ('ModifierArguments','ModifierId',[f'SPC_CULTURE_AESTHETIC_{i}'for i in range(16)]),
  ('Modifiers','ModifierId',[f'SPC_CULTURE_AESTHETIC_{i}'for i in range(16)]),
  ('RequirementArguments','RequirementId',[f'SPC_CULTURE_AESTHETIC_{i}_REQ'for i in range(16)]),
  ('Requirements','RequirementId',[f'SPC_CULTURE_AESTHETIC_{i}_REQ'for i in range(16)]),
  ('RequirementSetRequirements','RequirementSetId',[f'SPC_CULTURE_AESTHETIC_{i}_SET'for i in range(16)]),
  ('RequirementSets','RequirementSetId',[f'SPC_CULTURE_AESTHETIC_{i}_SET'for i in range(16)])]:
  d.executemany(f'DELETE FROM {table} WHERE {col}=?',[(x,)for x in values])
 d.execute('DROP TABLE IF EXISTS SPC_CultureAestheticBits')
 d.executescript((M/'Data/CultureAesthetic.sql').read_text())
 d.executescript((M/'Data/CultureMeaningProbe.sql').read_text())
 return d


class MeaningProbeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.sql=database()
 def runtime(self):
  helper=ae.AestheticTests();helper.sql=self.sql;l=helper.runtime()
  for table,key in [('GreatWorks','GreatWorkType'),('Yields','YieldType')]:
   cur=self.sql.execute('SELECT * FROM '+table);columns=[a[0]for a in cur.description];rows=[dict(zip(columns,r))for r in cur]
   for i,r in enumerate(rows):r['Index']=i+1
   l.globals().GameInfo[table]=l.globals().db(ae.lua_table(l,rows),key)
  for n in ['GreatWorkAdjacency','CultureMeaningProbe']:l.globals().include(n)
  l.execute("""
   Game.GetLocalPlayer=function()return 0 end
   for _,c in ipairs(cities)do building(c,'BUILDING_MARKET',c.ds[3],false);building(c,'BUILDING_FAIR',c.ds[3]);c.active=4;c.workCount=1;c.badCount=0;c.categoryUnknown=0;local campus=district(c,6,'DISTRICT_CAMPUS');building(c,'BUILDING_LIBRARY',campus)end
   shared.GreatWorkFacts.Summary=function(pid,id)
    local c=Players[pid]:GetCities():FindID(id)
    return c and {count=c.workCount,eraCount=c.eras,availability=c.worksUnknown and 'UNKNOWN' or 'KNOWN',hasConfirmed=not c.neverConfirmed,reference=SPCNetworkInput.Reference(c),modifierExcludedCount=c.badCount,unknownCategoryCount=c.categoryUnknown}
   end
   shared.Dialogue={samples={[0]={turn=turn,cities={[1]={{type='GREATWORK_BHASA_1'}},[2]={{type='GREATWORK_BHASA_1'}}}}}}
   SPCGWAdjacency.Start(P,shared);gwa=shared.GreatWorkAdjacency;gwa.Init()
   gwa.samples[0]={turn=turn,rows={{city=1,values={0,0,2,2,0,0}},{city=2,values={0,0,2,2,0,0}}}}
   gwa.Audit(0)
   SPCCultureMeaningProbe.Start(P,shared);probe=shared.CultureMeaningProbe
   fire('LoadScreenClose');svc.MarkDirty();gwa.Audit(0)
   function configured(c,y)
    local n=0;for bit=0,SPCCultureMeaningModel.ProbeBits[y]-1 do
     if c.present[GameInfo.Buildings['BUILDING_SPC_MEANING_PROBE_'..y..'_'..bit].Index]then n=n+2^bit/2 end
    end;return n
   end
   function old(c,y)return c.present[GameInfo.Buildings['BUILDING_SPC_B060_'..y..'_P1'].Index]==true end
   function begin()probe.Advance(0,a);assert(probe.mode=='BASELINE');probe.Advance(0,a);assert(probe.mode=='ACTIVE')end
  """)
  return l
 def test_model_matrix_per_work_and_shared_max_cap(self):
  l=self.runtime();l.execute("""
   local model=SPCCultureMeaningModel
   local f={validity='VERIFIED',identity='CULTURE',potential=4,active=4,activeStatus='KNOWN'}
   local w={hasConfirmed=true,availability='KNOWN',count=1,modifierExcludedCount=0,unknownCategoryCount=0}
   local view={validity='VERIFIED',availability='READY',value={districts={},domains={}}}
   for _,d in ipairs({0,1,3,6,10})do for _,count in ipairs({0,1,2})do
    w.count=count;view.value.domains={DISTRICT_CAMPUS={value=d},DISTRICT_COMMERCIAL_HUB={value=d}}
    local p=model.Plan(f,w,view);assert(p.each.SCIENCE==0.5*d and p.each.GOLD==1.5*d)
    assert(p.total.SCIENCE==0.5*d*count and p.total.GOLD==1.5*d*count)
   end end
   view.value.domains={};for _,entry in ipairs(model.Domains)do view.value.domains[entry[1]]={value=1}end
   view.value.domains.DISTRICT_THEATER={value=10};w.count=1
   local p=model.Plan(f,w,view)
   assert(p.each.SCIENCE==0.5 and p.each.GOLD==3 and p.each.PRODUCTION==1 and p.each.CULTURE==1 and p.each.FAITH==0.5 and p.each.FOOD==0.5)
   local cat={buildings={[1]={type='T1',tier=1,ordinary=true,domain='DISTRICT_CAMPUS'},[2]={type='T2',tier=2,ordinary=true,domain='DISTRICT_CAMPUS'},[3]={type='T3',tier=3,ordinary=true,domain='DISTRICT_CAMPUS'},[4]={type='T4',tier=4,ordinary=true,domain='DISTRICT_CAMPUS'},[5]={type='EXTRA',tier=4,ordinary=true,domain='DISTRICT_CAMPUS'}},Domain=function(t)return t end}
   local raw={districts={}}
   for id,n in ipairs({2,5})do local d={id=id,type='DISTRICT_CAMPUS',complete=true,pillaged=false,buildings={}};raw.districts[#raw.districts+1]=d;for bid=1,n do d.buildings[#d.buildings+1]={index=bid,complete=true,pillaged=false}end end
   local value=SPCDistrictCompleteness.Calculate(cat,raw)
   assert(value.districts[1].value==3 and value.districts[2].uncapped==14 and value.domains.DISTRICT_CAMPUS.value==10 and value.domains.DISTRICT_CAMPUS.districtID==2)
   view.value=value;p=model.Plan(f,w,view);assert(p.each.SCIENCE==5)
   raw.districts[2].pillaged=true;value=SPCDistrictCompleteness.Calculate(cat,raw);assert(value.domains.DISTRICT_CAMPUS.value==3)
  """)
 def test_switch_fixture_and_pillaged_owned_carrier(self):
  l=self.runtime();l.execute("""
   begin();probe.Advance(0,b);assert(probe.mode=='BASELINE' and old(a,'SCIENCE') and not old(b,'SCIENCE') and configured(a,'SCIENCE')==0)
   probe.Advance(0,b);assert(configured(b,'SCIENCE')==0.5 and configured(a,'SCIENCE')==0)
   local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_SCIENCE_0.Index;b.pillaged[id]=true
   assert(probe.View(0,b).configuredScience==0);probe.Audit();assert(b.pillaged[id]==false and probe.View(0,b).configuredScience==0.5)
   probe.Advance(0,b);assert(old(a,'SCIENCE') and old(b,'SCIENCE'))
  """)
 def test_duplicate_action_token_does_not_cycle(self):
  l=self.runtime();l.execute("""
   probe.Advance(0,a,'prepare');local w=writes;probe.Advance(0,a,'prepare');assert(probe.mode=='BASELINE' and writes==w)
   probe.Advance(0,a,'enable');local w=writes;probe.Advance(0,a,'enable');assert(probe.mode=='ACTIVE' and writes==w)
   assert(not pcall(probe.Advance,0,b,'enable'));assert(probe.mode=='ACTIVE')
   probe.Advance(0,a,'end');local w=writes;probe.Advance(0,a,'end');assert(probe.mode=='OFF' and writes==w)
  """)
 def test_model_never_rounds_or_substitutes_unknown(self):
  l=self.runtime();l.execute("""
   local f={validity='VERIFIED',identity='CULTURE',potential=4,active=4,activeStatus='KNOWN'}
   local w={hasConfirmed=true,availability='KNOWN',count=1,modifierExcludedCount=0,unknownCategoryCount=0}
   local v=svc.Read(0,a,a.token);local p=SPCCultureMeaningModel.Plan(f,w,v);assert(p.each.SCIENCE==0.5 and p.each.GOLD==1.5)
   assert(not pcall(SPCCultureMeaningModel.Parts,'SCIENCE',0.3))
   for _,n in ipairs({0,0.5,1.5,4.5,5})do local sum=0;for _,name in ipairs(SPCCultureMeaningModel.Parts('SCIENCE',n))do sum=sum+2^tonumber(name:match('_(%d+)$'))/2 end;assert(sum==n)end
   v.availability='TEMPORARILY_UNAVAILABLE';assert(not pcall(SPCCultureMeaningModel.Plan,f,w,v));v.availability='READY'
   for _,d in ipairs(v.value.districts)do if d.domain=='DISTRICT_CAMPUS'then d.buildings[1].tier=nil end end
   assert(not pcall(SPCCultureMeaningModel.Plan,f,w,v))
  """)
 def test_off_baseline_active_end_single_city(self):
  l=self.runtime();l.execute("""
   assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0 and old(a,'SCIENCE') and old(b,'SCIENCE'))
   probe.Advance(0,a);assert(not old(a,'SCIENCE') and old(b,'SCIENCE'));assert(configured(a,'SCIENCE')==0)
   probe.Advance(0,a);assert(configured(a,'SCIENCE')==0.5 and configured(a,'GOLD')==1.5 and configured(b,'GOLD')==0)
   gwa.Audit(0);assert(not old(a,'SCIENCE') and old(b,'SCIENCE'))
   local w=writes;probe.Audit();probe.Audit();assert(writes==w)
   probe.Advance(0,a);assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0 and old(a,'SCIENCE') and old(b,'SCIENCE'))
   assert(a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and a.present[GameInfo.Buildings.BUILDING_FAIR.Index])
  """)
 def test_same_era_work_change_and_l1_zero_write(self):
  l=self.runtime();l.execute("""
   begin();local w=writes;local prior=total(a);a.workCount=2;shared.GreatWorkFacts.OnConfirmed(0,{1})
   assert(probe.lastPlan.count==2 and probe.lastPlan.total.SCIENCE==1 and probe.lastPlan.total.GOLD==3)
   assert(configured(a,'SCIENCE')==0.5 and total(a)==prior and writes==w)
   a.workCount=0;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0)
   a.workCount=1;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(configured(a,'SCIENCE')==0.5)
  """)
 def test_real_confirmed_count_and_eligibility_notifications(self):
  f=Fixture();f.check("""
   notices={};shared.GreatWorkFacts.OnConfirmed=function(pid,ids)notices[#notices+1]=ids end
   local rows={{7,10,0,100,'GREATWORK_BHASA_1'},{7,10,1,101,'GREATWORK_BHASA_1'}}
   assert(receive(1,rows));assert(#notices==1);assert(receive(2,rows));assert(#notices==1)
   table.remove(rows,2);assert(receive(3,rows));assert(#notices==2 and #notices[2]==1 and notices[2][1]==7)
   local s=shared.GreatWorkFacts.Summary(0,7);assert(s.count==1 and s.eraCount==1 and s.modifierExcludedCount==0 and s.unknownCategoryCount==0)
   assert(s.works==nil and s.excluded==nil and s.eras==nil)
   rows[#rows+1]={7,10,1,105,'UNKNOWN_WRITING'};assert(receive(4,rows));s=shared.GreatWorkFacts.Summary(0,7)
   assert(#notices==3 and s.count==1 and s.modifierExcludedCount==1)
   rows[2]={7,10,1,106,'RELIC'};assert(receive(5,rows));assert(#notices==4 and shared.GreatWorkFacts.Summary(0,7).modifierExcludedCount==0)
  """)
 def test_building_governor_same_turn_and_unknown(self):
  l=self.runtime();l.execute("""
   begin();building(a,'BUILDING_UNIVERSITY',a.ds[6]);fire('CityBuildingsChanged',0,1)
   assert(configured(a,'SCIENCE')==1.5 and probe.lastPlan.domains.DISTRICT_CAMPUS.value==3)
   building(a,'BUILDING_MARKET',a.ds[3]);fire('CityBuildingsChanged',0,1);assert(configured(a,'GOLD')==4.5)
   local w=writes;a.worksUnknown=true;probe.Audit();assert(writes==w and configured(a,'SCIENCE')==1.5 and probe.error:find('ME_WORKS_UNKNOWN'))
   a.worksUnknown=false;a.active=nil;probe.Audit();assert(writes==w and probe.error:find('ME_ACTIVE_UNKNOWN'))
   a.active=3;fire('GovernorChanged',0);assert(configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0)
   a.active=4;fire('GovernorEstablished',0);assert(configured(a,'SCIENCE')==1.5 and configured(a,'GOLD')==4.5)
  """)
 def test_refuse_or_withdraw_unsupported_fixture(self):
  l=self.runtime();l.execute("""
   a.badCount=1;assert(not pcall(probe.Advance,0,a));assert(probe.mode=='OFF' and old(a,'SCIENCE') and configured(a,'SCIENCE')==0)
   a.badCount=0;a.categoryUnknown=1;assert(not pcall(probe.Advance,0,a));assert(probe.mode=='OFF')
   a.categoryUnknown=0;begin();a.badCount=1;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(configured(a,'SCIENCE')==0 and probe.error:find('ME_FIXTURE_UNSUPPORTED_WORK'))
   probe.Advance(0,a);assert(probe.mode=='OFF' and old(a,'SCIENCE'))
  """)
 def test_old_withdrawal_failure_does_not_enable_new(self):
  l=self.runtime();l.execute("""
   failRemove=GameInfo.Buildings.BUILDING_SPC_B060_SCIENCE_P1.Index
   assert(not pcall(probe.Advance,0,a));assert(gwa.IsMeaningHeld(0,a) and configured(a,'SCIENCE')==0 and probe.error)
   assert(old(a,'SCIENCE'));failRemove=nil;probe.Advance(0,a);assert(probe.mode=='OFF' and old(a,'SCIENCE'))
   begin();assert(configured(a,'SCIENCE')==0.5)
  """)
 def test_new_write_failure_and_no_early_old_resume(self):
  l=self.runtime();l.execute("""
   probe.Advance(0,a);failCreate=true;probe.Advance(0,a)
   assert(configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0 and gwa.IsMeaningHeld(0,a) and probe.error)
   failCreate=false;probe.Advance(0,a);assert(probe.mode=='OFF' and old(a,'SCIENCE'))
   begin();failRemove=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_SCIENCE_0.Index
   assert(not pcall(probe.Advance,0,a));assert(gwa.IsMeaningHeld(0,a) and not old(a,'SCIENCE') and probe.stopping);probe.Audit();assert(configured(a,'GOLD')==0)
   failRemove=nil;probe.Advance(0,a);assert(probe.mode=='OFF' and old(a,'SCIENCE'))
  """)
 def test_loss_confirmed_only_idempotent_no_recapture_replay(self):
  l=self.runtime();l.execute("""
   begin();a.owner=3
   local loss={confirmed=false,targetID=a.id,origin={owner=0}}
   assert(not pcall(exits.CultureMeaningProbe,a,loss));assert(configured(a,'SCIENCE')==0.5)
   loss.confirmed=true;exits.CultureMeaningProbe(a,loss);assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0)
   local w=writes;exits.CultureMeaningProbe(a,loss);assert(writes==w and old(b,'SCIENCE'))
   a.owner=0;fire('GovernorChanged',0);assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0)
  """)
 def test_load_cleanup_foreign_only_owned_no_probe_replay(self):
  l=self.runtime();l.execute("""
   begin();a.owner=3;fire('LoadScreenClose');assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0)
   assert(a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and a.token=='persistent:1')
   a.owner=0;fire('PlayerTurnActivated',0);assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0)
  """)
 def test_reference_change_never_adopts_old_probe(self):
  l=self.runtime();l.execute("begin();a.token='new-city';probe.Audit();assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0);assert(not gwa.IsMeaningHeld(0,a))")
 def test_read_only_bounded_diagnostic_and_affected_scope(self):
  l=self.runtime();l.execute("""
   begin();local w=writes;local n=counts.dc_read or 0;probe.Audit({player=3});probe.Audit({player=0,city=2});assert((counts.dc_read or 0)==n)
   local text=probe.Describe(0,a);local view=probe.View(0,a);assert(text:find('理论每件') and view.science==0.5 and view.totalGold==1.5);assert(writes==w)
   probe.Advance(0,a);local n=counts.dc_read or 0;probe.Audit();assert((counts.dc_read or 0)==n)
  """)
 def test_sql_exact_single_city_native_yield_definitions(self):
  rows=self.sql.execute("select BuildingType,InternalOnly,CitizenSlots,Housing,PrereqDistrict from Buildings where BuildingType like 'BUILDING_SPC_MEANING_PROBE_%'").fetchall();self.assertEqual(len(rows),10)
  for b,internal,slots,housing,district in rows:
   self.assertEqual((internal,slots,housing,district),(1,0,0,'DISTRICT_CITY_CENTER'))
   y,bit=b.removeprefix('BUILDING_SPC_MEANING_PROBE_').split('_');self.assertIn(y,{'SCIENCE','GOLD'})
   modifiers=self.sql.execute('select ModifierId from BuildingModifiers where BuildingType=?',(b,)).fetchall();self.assertEqual(len(modifiers),7)
   categories=set()
   for(mid,)in modifiers:
    self.assertEqual(self.sql.execute('select ModifierType from Modifiers where ModifierId=?',(mid,)).fetchone()[0],'MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD')
    args=dict(self.sql.execute('select Name,Value from ModifierArguments where ModifierId=?',(mid,)))
    self.assertEqual(args['YieldType'],'YIELD_'+y);self.assertEqual(float(args['YieldChange']),2**int(bit)/2);categories.add(args['GreatWorkObjectType'])
   self.assertEqual(categories,{'GREATWORKOBJECT_'+c for c in ['WRITING','MUSIC','SCULPTURE','PORTRAIT','LANDSCAPE','RELIGIOUS','ARTIFACT']})
 def test_native_read_baseline_guard_no_gameplay_writes(self):
  l=self.runtime();l.globals().include('UI/BoostGreatWorkRead')
  l.execute("""
   -- Deliberately mock the UI getter: verifies read/compare only, not engine precision.
   local get=a.GetBuildings
   a.GetBuildings=function(c)local b=get(c)
    b.GetNumGreatWorkSlots=function(_,id)return id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index and c.workCount or 0 end
    b.GetGreatWorkInSlot=function(_,id,s)return s+100 end;b.GetGreatWorkTypeFromIndex=function()return 'GREATWORK_BHASA_1'end
    b.IsBuildingThemedCorrectly=function()return false end
    b.GetBuildingYieldFromGreatWorks=function(_,y,id)return configured(c,GameInfo.Yields[y].YieldType:gsub('YIELD_',''))*c.workCount end
    return b
   end
   probe.Advance(0,a);local w=writes;assert(SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true):find('已记录'));assert(writes==w)
   probe.Advance(0,a);local w=writes;local t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(t:find('Δ%+0.5000') and t:find('Δ%+1.5000'));assert(writes==w)
   a.workCount=2;t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(t:find('差值基线不可用'))
   probe.Advance(0,a);assert(SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false):find('测试已关闭'))
  """)
 def test_registration_localization_exact_scope(self):
  root=ET.parse(M/'SpecializationP0.modinfo').getroot();self.assertEqual(root.get('version'),'177')
  files=[e.text for e in root.find('Files')];self.assertEqual(len(files),len(set(files)))
  self.assertEqual(set(files),{str(p.relative_to(M))for p in M.rglob('*')if p.is_file() and p.name not in {'.DS_Store','SpecializationP0.modinfo'}})
  self.assertTrue({'CultureMeaningModel.lua','CultureMeaningProbe.lua','Data/CultureMeaningProbe.sql'}<=set(files))
  self.assertEqual(root.find(".//UpdateDatabase[@id='SPC_CultureMeaningProbe']/File").text,'Data/CultureMeaningProbe.sql')
  xml=ET.parse(M/'UI/P0Panel.xml').getroot();self.assertIsNotNone(xml.find('.//*[@ID="MeaningProbeButtonCaption"]'))
  ui=(M/'UI/P0Panel.lua').read_text();self.assertIn("request('CULTURE_MEANING_ADVANCE')",ui);self.assertIn("request('CULTURE_MEANING_READ')",ui)
  text=(M/'Text/TestText.sql').read_text()
  for key in ['LOC_SPC_CULTURE_MEANING_PROBE','LOC_SPC_CULTURE_MEANING_PROBE_HINT','LOC_SPC_MEANING_PROBE_CARRIER']:self.assertEqual(text.count("'"+key+"'"),2)
  src=(M/'CultureMeaningProbe.lua').read_text()
  for forbidden in ['collectgarbage','SetProperty','SetUpdate','GameCoreEventPublishComplete','CityWorkerChanged','OnHover']:self.assertNotIn(forbidden,src)
  self.assertIn("RegisterExit('CultureMeaningProbe'",src)
  self.assertIn("include('CultureMeaningProbe')",(M/'Gameplay.lua').read_text())

if __name__=='__main__':unittest.main()
