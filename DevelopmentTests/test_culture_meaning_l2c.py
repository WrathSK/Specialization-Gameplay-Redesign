"""P0-L2C targeted Lua/SQL checks; no native engine or settlement PASS.

Uses the maintained L2 fixture only, not its historical four-state/candidate
test suite. External DB is opened read-only by that fixture and copied into
memory. When run from /private/tmp, set SPC_L2C_ROOT to the develop checkout.
"""
from pathlib import Path
import os
import sys
import unittest

R = Path(os.environ.get("SPC_L2C_ROOT", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(R / "DevelopmentTests"))
import test_culture_meaning_probe as legacy

YIELDS = ("SCIENCE", "PRODUCTION", "GOLD", "FOOD", "FAITH")
BITS = {"SCIENCE": 4, "GOLD": 6, "CULTURE": 4,
        "PRODUCTION": 4, "FOOD": 3, "FAITH": 3}
CATEGORIES = ("WRITING", "MUSIC", "SCULPTURE", "PORTRAIT",
              "LANDSCAPE", "RELIGIOUS", "ARTIFACT")
OWNED = [f"BUILDING_SPC_MEANING_PROBE_{y}_{bit}"
         for y, bits in BITS.items() for bit in range(bits)] + [
    "BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3",
    "BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3_SCALE100",
    "BUILDING_SPC_MEANING_PROBE_PRODUCTION_SINGLE3",
]

HELPERS = r"""
function exactMeaning(c)
 local out={}
 for _,name in ipairs(SPCCultureMeaningModel.Owned)do
  if c.present[GameInfo.Buildings[name].Index]then out[name]=true end
 end
 return out
end
function seedAllMeaning(c)
 for _,name in ipairs(SPCCultureMeaningModel.Owned)do building(c,name,c.ds[1])end
 assert(#SPCCultureMeaningModel.Owned==27)
 local n=0;for _ in pairs(exactMeaning(c))do n=n+1 end;assert(n==27)
end
function snapshotBuildings(c)
 local out={};for id,value in pairs(c.present)do out[id]=value end;return out
end
function assertBuildingsSame(c,prior)
 for id,value in pairs(prior)do assert(c.present[id]==value,'CHANGED_OTHER_CITY')end
 for id,value in pairs(c.present)do assert(prior[id]==value,'NEW_OTHER_CITY')end
end
-- Explicit fact-service fixture for exact five-yield native-writer projection.
-- Physical building/pillage/ACTIVE tests below still use the real shared reader.
function fiveDepthFixture(c)
 local read=shared.DistrictCompleteness.Read
 shared.DistrictCompleteness.Read=function(pid,current,token)
  if current~=c then return read(pid,current,token)end
  assert(pid==current.owner and token==current.token)
  return {validity='VERIFIED',availability='READY',value={districts={},domains={
   DISTRICT_CAMPUS={value=6},DISTRICT_INDUSTRIAL_ZONE={value=6},
   DISTRICT_ENCAMPMENT={value=3},DISTRICT_COMMERCIAL_HUB={value=3},
   DISTRICT_HARBOR={value=3},DISTRICT_HOLY_SITE={value=6},
   DISTRICT_NEIGHBORHOOD={value=6},DISTRICT_GOVERNMENT={value=10},
   DISTRICT_DIPLOMATIC_QUARTER={value=10}}}}
 end
 return read
end
"""


class L2CTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.sql = legacy.database()

 @classmethod
 def tearDownClass(cls):
  cls.sql.close()

 def helper(self):
  helper = legacy.MeaningProbeTests()
  helper.sql = self.sql
  return helper

 def runtime(self, real_samples=False):
  lua = self.helper().runtime(real_samples=real_samples)
  lua.execute(HELPERS)
  return lua

 def real_sample_runtime(self):
  lua = self.helper().real_sample_runtime()
  lua.execute(HELPERS)
  return lua

 def test_seven_domain_mapping_floor_matrix_and_cap(self):
  lua = self.runtime()
  lua.execute(r"""
   local m=SPCCultureMeaningModel
   assert(table.concat(m.WriteYields,',')=='SCIENCE,PRODUCTION,GOLD,FOOD,FAITH')
   local expected={DISTRICT_CAMPUS='SCIENCE',DISTRICT_INDUSTRIAL_ZONE='PRODUCTION',
    DISTRICT_COMMERCIAL_HUB='GOLD',DISTRICT_HARBOR='GOLD',DISTRICT_ENCAMPMENT='PRODUCTION',
    DISTRICT_HOLY_SITE='FAITH',DISTRICT_NEIGHBORHOOD='FOOD'}
   assert(#m.Domains==7)
   for _,domain in ipairs(m.Domains)do assert(expected[domain[1]]==domain[2]);expected[domain[1]]=nil end
   assert(next(expected)==nil)
   local f={validity='VERIFIED',identity='CULTURE',potential=4,active=4,activeStatus='KNOWN'}
   local w={hasConfirmed=true,availability='KNOWN',count=1,modifierExcludedCount=0,unknownCategoryCount=0}
   local v={validity='VERIFIED',availability='READY',value={districts={},domains={}}}
   for _,depth in ipairs({0,1,3,6,10})do for _,count in ipairs({0,1,2})do
    w.count=count
    for _,domain in ipairs(m.Domains)do v.value.domains[domain[1]]={value=depth}end
    v.value.domains.DISTRICT_THEATER={value=10}
    v.value.domains.DISTRICT_GOVERNMENT={value=10}
    v.value.domains.DISTRICT_DIPLOMATIC_QUARTER={value=10}
    local p=m.Plan(f,w,v)
    local values={SCIENCE=math.floor(0.5*depth),PRODUCTION=2*math.floor(0.5*depth),
     GOLD=2*math.floor(1.5*depth),FOOD=math.floor(0.5*depth),FAITH=math.floor(0.5*depth)}
    for y,each in pairs(values)do assert(p.each[y]==each and p.total[y]==each*count,y)end
    assert(p.domains.DISTRICT_GOVERNMENT==nil and p.domains.DISTRICT_DIPLOMATIC_QUARTER==nil and p.domains.DISTRICT_THEATER==nil)
   end end
   local catalog={buildings={},Domain=function(kind)return kind end}
   for i,tier in ipairs({1,2,3,4,4})do catalog.buildings[i]={type='TEST_'..i,tier=tier,ordinary=true,domain='DISTRICT_CAMPUS'}end
   local raw={districts={}}
   for id,n in ipairs({2,5})do
    local d={id=id,type='DISTRICT_CAMPUS',complete=true,pillaged=false,buildings={}}
    raw.districts[#raw.districts+1]=d
    for index=1,n do d.buildings[#d.buildings+1]={index=index,complete=true,pillaged=false}end
   end
   local value=SPCDistrictCompleteness.Calculate(catalog,raw)
   assert(value.districts[2].uncapped==14 and value.domains.DISTRICT_CAMPUS.value==10 and value.domains.DISTRICT_CAMPUS.districtID==2)
   w.count=2;v.value=value;assert(m.Plan(f,w,v).total.SCIENCE==10)
   raw.districts[2].pillaged=true;v.value=SPCDistrictCompleteness.Calculate(catalog,raw)
   assert(v.value.domains.DISTRICT_CAMPUS.value==3 and m.Plan(f,w,v).total.SCIENCE==2)
  """)

 def test_floor_before_same_yield_sum_and_w_counterexamples(self):
  lua = self.runtime()
  lua.execute(r"""
   local m=SPCCultureMeaningModel
   local f={validity='VERIFIED',identity='CULTURE',potential=4,active=4,activeStatus='KNOWN'}
   local w={hasConfirmed=true,availability='KNOWN',count=2,modifierExcludedCount=0,unknownCategoryCount=0}
   local v={validity='VERIFIED',availability='READY',value={districts={},domains={}}}
   for _,domain in ipairs(m.Domains)do v.value.domains[domain[1]]={value=1}end
   local p=m.Plan(f,w,v)
   assert(p.each.GOLD==2 and p.total.GOLD==4)
   assert(p.each.PRODUCTION==0 and p.total.PRODUCTION==0 and p.total.SCIENCE==0)
   assert(p.domains.DISTRICT_COMMERCIAL_HUB.rawEach==1.5)
   v.value.domains.DISTRICT_COMMERCIAL_HUB.value=3;p=m.Plan(f,w,v)
   assert(p.each.GOLD==5 and p.total.GOLD==10)
   v.value.domains.DISTRICT_INDUSTRIAL_ZONE.value=3;p=m.Plan(f,w,v)
   assert(p.each.PRODUCTION==1 and p.total.PRODUCTION==2)
   -- Excluded domains cannot force an unrelated Meaning depth error.
   v.value.domains.DISTRICT_GOVERNMENT={value='UNKNOWN'}
   v.value.domains.DISTRICT_DIPLOMATIC_QUARTER={value=99}
   assert(m.Plan(f,w,v).each.GOLD==5)
   v.value.domains.DISTRICT_CAMPUS.value=11;assert(not pcall(m.Plan,f,w,v))
  """)

 def test_finite_encoding_and_culture_generation_disabled(self):
  lua = self.runtime()
  lua.execute(r"""
   local m=SPCCultureMeaningModel;local limits={SCIENCE=5,PRODUCTION=10,GOLD=30,FOOD=5,FAITH=5}
   local seen={};assert(#m.Owned==27)
   for _,name in ipairs(m.Owned)do assert(not seen[name]);seen[name]=true;assert(GameInfo.Buildings[name])end
   for y,limit in pairs(limits)do
    for amount=0,limit do
     local sum=0
     for _,name in ipairs(m.Parts(y,amount))do
      assert(seen[name] and not name:find('_CULTURE_',1,true))
      sum=sum+2^tonumber(name:match('_(%d+)$'))/m.ProbeScale[y]
     end
     assert(sum==amount,y)
    end
    for _,amount in ipairs({-1,math.huge,0/0})do assert(not pcall(m.Parts,y,amount))end
   end
   for _,y in ipairs({'PRODUCTION','FOOD','FAITH'})do assert(not pcall(m.Parts,y,0.5))end
   for _,amount in ipairs({0,1,3})do assert(not pcall(m.Parts,'CULTURE',amount))end
   for _,variant in ipairs({'SINGLE3','SINGLE3_SCALE100'})do assert(not pcall(m.Parts,'CULTURE',3,variant))end
   local single=m.DiagnosticSingle3
   assert(single.name=='BUILDING_SPC_MEANING_PROBE_PRODUCTION_SINGLE3' and single.amount==3 and seen[single.name])
   local parts=m.Parts('PRODUCTION',3)
   assert(#parts==2 and parts[1]=='BUILDING_SPC_MEANING_PROBE_PRODUCTION_0' and parts[2]=='BUILDING_SPC_MEANING_PROBE_PRODUCTION_1')
   for _,name in ipairs(parts)do assert(name~=single.name)end
  """)

 def test_sql_exact_27_owned_and_189_attachments(self):
  placeholders = ','.join('?' for _ in OWNED)
  rows = self.sql.execute(f'SELECT BuildingType,InternalOnly,CitizenSlots,Housing,PrereqDistrict FROM Buildings WHERE BuildingType IN ({placeholders})', OWNED).fetchall()
  self.assertEqual({row[0] for row in rows}, set(OWNED))
  count = 0
  for name, internal, slots, housing, district in rows:
   self.assertEqual((internal,slots,housing,district),(1,0,0,'DISTRICT_CITY_CENTER'))
   suffix=name.removeprefix('BUILDING_SPC_MEANING_PROBE_')
   y,part=suffix.split('_',1)
   amount=3 if part.startswith('SINGLE3') else 2**int(part)/(2 if y in ('SCIENCE','GOLD') else 1)
   attached=self.sql.execute('SELECT ModifierId FROM BuildingModifiers WHERE BuildingType=?',(name,)).fetchall()
   self.assertEqual(len(attached),7);count+=len(attached)
   categories=set()
   for (modifier,) in attached:
    self.assertEqual(self.sql.execute('SELECT ModifierType FROM Modifiers WHERE ModifierId=?',(modifier,)).fetchone()[0],'MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD')
    arguments=dict(self.sql.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(modifier,)))
    self.assertEqual(arguments['YieldType'],'YIELD_'+y)
    self.assertEqual(float(arguments['YieldChange']),amount)
    categories.add(arguments['GreatWorkObjectType'])
    self.assertEqual(set(arguments),{'GreatWorkObjectType','YieldType','YieldChange'}|({'ScalingFactor'} if part=='SINGLE3_SCALE100' else set()))
    if part=='SINGLE3_SCALE100':self.assertEqual(float(arguments['ScalingFactor']),100)
   self.assertEqual(categories,{'GREATWORKOBJECT_'+category for category in CATEGORIES})
  self.assertEqual(count,189)

 def test_zero_culture_three_state_flow_and_disabled_configuration(self):
  lua=self.runtime();legacy.bind_actual_request(lua)
  lua.execute(r"""
   fiveDepthFixture(a)
   local other=snapshotBuildings(b);local percent100=0;local hold=dialogue.HoldMeaningProbe
   dialogue.HoldMeaningProbe=function(pid,c,percent)if percent==100 then percent100=percent100+1 end;return hold(pid,c,percent)end
   local function request(action,token)
    meaningRequest(0,{Action=action,CityID=1,Token=token})
    assert(shared.LastToken==token and shared.CultureMeaningView.token==token)
    return shared.CultureMeaningView
   end
   local before=writes;local off=request('CULTURE_MEANING_CONFIG','off-blocked')
   assert(off.error:find('ME_VARIANT_DEFERRED') and writes==before and probe.mode=='OFF')
   request('CULTURE_MEANING_ADVANCE','baseline')
   assert(probe.mode=='BASELINE' and next(exactMeaning(a))==nil)
   local v=request('CULTURE_MEANING_ADVANCE','active')
   assert(v.mode=='ACTIVE' and not v.error and v.dialoguePercent==0 and v.configuredCulture==0)
   for field,value in pairs({science=3,production=4,gold=8,food=3,faith=3})do assert(v[field]==value,field)end
   for field,value in pairs({configuredScience=3,configuredProduction=4,configuredGold=8,configuredFood=3,configuredFaith=3})do assert(v[field]==value,field)end
   for name in pairs(exactMeaning(a))do assert(not name:find('_CULTURE_',1,true))end
   local before=writes;request('CULTURE_MEANING_ADVANCE','active');assert(writes==before and probe.mode=='ACTIVE')
   request('CULTURE_MEANING_READ','read');assert(writes==before and probe.mode=='ACTIVE')
   v=request('CULTURE_MEANING_CONFIG','blocked');assert(v.error:find('ME_VARIANT_DEFERRED') and writes==before and probe.mode=='ACTIVE')
   v=request('CULTURE_MEANING_END','end')
   assert(v.mode=='OFF' and not v.error and next(exactMeaning(a))==nil and old(a,'SCIENCE'))
   assert(dialogue.meaningOverride==nil and not gwa.IsMeaningHeld(0,a) and percent100==0)
   assertBuildingsSame(b,other)
   before=writes;request('CULTURE_MEANING_END','end');assert(writes==before)
   request('CULTURE_MEANING_END','off');assert(writes==before)
   request('CULTURE_MEANING_ADVANCE','baseline2');request('CULTURE_MEANING_ADVANCE','active2')
   request('CULTURE_MEANING_ADVANCE','advance-end');assert(probe.mode=='OFF' and next(exactMeaning(a))==nil)
  """)

 def test_real_same_turn_building_pillage_active_and_works_changes(self):
  lua=self.runtime();lua.execute(r"""
   local other=snapshotBuildings(b);begin()
   assert(configured(a,'GOLD')==1 and configured(a,'SCIENCE')==0)
   building(a,'BUILDING_UNIVERSITY',a.ds[6]);fire('CityBuildingsChanged',0,1)
   assert(configured(a,'SCIENCE')==1 and probe.lastPlan.domains.DISTRICT_CAMPUS.value==3)
   building(a,'BUILDING_MARKET',a.ds[3]);fire('CityBuildingsChanged',0,1)
   assert(configured(a,'GOLD')==4)
   a.pillaged[GameInfo.Buildings.BUILDING_UNIVERSITY.Index]=true
   fire('BuildingPillaged',0,1);assert(configured(a,'SCIENCE')==0)
   a.pillaged[GameInfo.Buildings.BUILDING_UNIVERSITY.Index]=false
   fire('BuildingRepaired',0,1);assert(configured(a,'SCIENCE')==1)
   a.workCount=2;confirmCollection()
   assert(probe.lastPlan.count==2 and probe.lastPlan.total.SCIENCE==2 and probe.lastPlan.total.GOLD==8)
   assert(configured(a,'SCIENCE')==1 and configured(a,'GOLD')==4)
   a.workCount=0;confirmCollection();assert(next(exactMeaning(a))==nil)
   a.workCount=1;confirmCollection();assert(configured(a,'SCIENCE')==1 and configured(a,'GOLD')==4)
   a.active=3;fire('GovernorChanged',0);assert(next(exactMeaning(a))==nil)
   a.active=4;fire('GovernorEstablished',0);assert(configured(a,'SCIENCE')==1 and configured(a,'GOLD')==4)
   local before=writes;probe.Audit();probe.Audit();assert(writes==before)
   assertBuildingsSame(b,other)
  """)

 def test_unknown_inputs_hold_confirmed_five_yields_and_reference_never_replays(self):
  lua=self.runtime();lua.execute(r"""
   fiveDepthFixture(a);begin();local expected=exactMeaning(a)
   local function unchanged()
    local now=exactMeaning(a);for name in pairs(expected)do assert(now[name])end
    for name in pairs(now)do assert(expected[name])end
   end
   local before=writes;a.worksUnknown=true;probe.Audit()
   assert(probe.error:find('ME_WORKS_UNKNOWN') and writes==before);unchanged()
   a.worksUnknown=false;a.active=nil;probe.Audit()
   assert(probe.error:find('ME_ACTIVE_UNKNOWN') and writes==before);unchanged()
   a.active=4;a.factsUnknown=true;probe.Audit()
   assert(probe.error:find('ME_FACT_UNKNOWN') and writes==before);unchanged()
   a.factsUnknown=false;probe.Audit();assert(not probe.error);unchanged()
   a.token='different-city';probe.Audit()
   assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and not gwa.IsMeaningHeld(0,a))
  """)

 def test_confirmed_loss_clears_all_27_owned_without_other_city_or_permanent_write(self):
  lua=self.runtime();lua.execute(r"""
   fiveDepthFixture(a);begin();seedAllMeaning(a)
   local other=snapshotBuildings(b);local token=a.token;a.owner=3
   local loss={confirmed=false,targetID=a.id,origin={owner=0}}
   local before=writes
   assert(not pcall(exits.CultureMeaningProbe,a,loss) and writes==before)
   local n=0;for _ in pairs(exactMeaning(a))do n=n+1 end;assert(n==27)
   loss.confirmed=true;loss.targetID=b.id
   assert(not pcall(exits.CultureMeaningProbe,a,loss) and writes==before)
   loss.targetID=a.id
   loss.confirmed=true;exits.CultureMeaningProbe(a,loss)
   assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and dialogue.meaningOverride==nil)
   assert(a.token==token and a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and a.present[GameInfo.Buildings.BUILDING_FAIR.Index])
   assertBuildingsSame(b,other)
   before=writes;exits.CultureMeaningProbe(a,loss);assert(writes==before)
   a.owner=0;fire('GovernorChanged',0)
   assert(probe.mode=='OFF' and next(exactMeaning(a))==nil)
  """)

 def test_cold_load_clears_all_27_owned_on_supported_and_foreign_cities(self):
  lua=self.runtime();lua.execute(r"""
   begin();seedAllMeaning(a);seedAllMeaning(b);a.owner=3
   local token=a.token;fire('LoadScreenClose')
   assert(probe.mode=='OFF' and probe.ready and next(exactMeaning(a))==nil and next(exactMeaning(b))==nil)
   assert(dialogue.meaningOverride==nil and not gwa.IsMeaningHeld(0,a))
   for _,c in ipairs({a,b})do
    assert(c.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and c.present[GameInfo.Buildings.BUILDING_FAIR.Index])
   end
   assert(a.token==token);a.owner=0;fire('PlayerTurnActivated',0)
   assert(probe.mode=='OFF' and next(exactMeaning(a))==nil)
   local before=writes;fire('LoadScreenClose');assert(next(exactMeaning(a))==nil and next(exactMeaning(b))==nil)
   -- Load may reconcile other modules; precise absence is the assertion, not a global zero-write claim.
  """)

 def test_create_and_exit_failure_preserve_holds_until_exact_cleanup(self):
  for after_write in (False, True):
   with self.subTest(after_write=after_write):
    lua=self.runtime();lua.globals().afterWrite=after_write;lua.execute(r"""
     fiveDepthFixture(a);probe.Advance(0,a,'baseline')
     local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_2.Index
     local create=P.CreateBuilding
     P.CreateBuilding=function(q,i)if i==id then if afterWrite then create(q,i);error('NATIVE_AFTER_WRITE')else return end end;return create(q,i)end
     assert(not pcall(probe.Advance,0,a,'failed') and probe.error)
     assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
     assert(old(b,'SCIENCE'));P.CreateBuilding=create
     probe.End(0,a,'recover-create');assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and old(a,'SCIENCE'))
     probe.Advance(0,a,'baseline2');probe.Advance(0,a,'active2')
     assert(a.present[id]);failRemove=id
     assert(not pcall(probe.End,0,a,'failed-end') and probe.stopping and probe.error)
     assert(a.present[id] and gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
     local before=writes;failRemove=nil;probe.End(0,a,'failed-end');assert(writes==before and probe.stopping)
     probe.End(0,a,'recover-end')
     assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and old(a,'SCIENCE') and old(b,'SCIENCE'))
     assert(dialogue.meaningOverride==nil and not gwa.IsMeaningHeld(0,a))
    """)

 def test_synchronous_building_notifications_are_bounded_without_dropping_changes(self):
  lua=self.runtime();lua.execute(r"""
   local create,remove=P.CreateBuilding,P.RemoveBuilding
   P.CreateBuilding=function(q,id)create(q,id);fire('CityBuildingsChanged',q.city.owner,q.city.id)end
   P.RemoveBuilding=function(buildings,id)remove(buildings,id);fire('CityBuildingsChanged',buildings.city.owner,buildings.city.id)end
   fiveDepthFixture(a);local other=snapshotBuildings(b)
   for _,mode in ipairs({'BASELINE','ACTIVE','OFF'})do
    probe.Advance(0,a,'sync:'..mode)
    assert(probe.mode==mode and not probe.error and not probe.busy and not probe.advancing and not probe.deferred and not dialogue.busy)
    local before=writes;fire('CityBuildingsChanged',0,1);assert(writes==before)
   end
   assert(next(exactMeaning(a))==nil and old(a,'SCIENCE'));assertBuildingsSame(b,other)
  """)

 # Targeted L2C reader fixtures/methods. Append inside L2CTests before aliases.
 # These mock the UI getter and verify reader behavior only, not native yield PASS.
 def reader_runtime(self):
  lua=self.runtime();lua.globals().include('UI/BoostGreatWorkRead')
  lua.execute(r"""
   fiveDepthFixture(a)
   readerNativeCalls=0;readerModifierCalls=0;readerThemed=false;readerMove=false
   readerOffsets={};readerStale=false;readerBad=nil;readerOverrides={}
   readerPopulation=a:GetPopulation()
   a.GetPopulation=function()return readerPopulation end
   local get=a.GetBuildings
   a.GetBuildings=function(c)
    local b=get(c)
    b.GetNumGreatWorkSlots=function(_,id)return id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index and c.workCount or 0 end
    b.GetGreatWorkInSlot=function(_,id,slot)return slot+100+(readerMove and 10 or 0)end
    b.GetGreatWorkTypeFromIndex=function()return 'GREATWORK_BHASA_1'end
    b.IsBuildingThemedCorrectly=function()return readerThemed end
    b.GetBuildingYieldFromGreatWorks=function(_,yield,id)
     readerNativeCalls=readerNativeCalls+1
     local typ=GameInfo.Yields[yield].YieldType:gsub('YIELD_','')
     if typ=='SCIENCE' and readerBad then
      if readerBad=='nil' then return nil elseif readerBad=='nan' then return 0/0
      elseif readerBad=='inf' then return math.huge end
     end
     local base={SCIENCE=2,PRODUCTION=3,GOLD=4,FOOD=5,FAITH=6}
     assert(base[typ]~=nil,'UNEXPECTED_CULTURE_READ')
     return (base[typ]+(readerStale and 0 or configured(c,typ)))*c.workCount+(readerOffsets[typ] or 0)
    end
    return b
   end
   GameEffects={GetModifiers=function()readerModifierCalls=readerModifierCalls+1;error('NO_GLOBAL_SCAN')end}
   function readerRead(mark)
    local v=probe.View(0,a)
    for key,value in pairs(readerOverrides)do v[key]=value end
    return SPCBoostGreatWorkRead.Meaning(P,a,v,mark)
   end
   function readerBegin()
    probe.Advance(0,a,'reader-baseline');readerBaseline=readerRead(true)
    assert(readerBaseline:find('同回合基线已记录',1,true))
    probe.Advance(0,a,'reader-active')
   end
  """)
  return lua

 def test_reader_five_native_deltas_and_no_gameplay_write(self):
  lua=self.reader_runtime();lua.execute(r"""
   readerBegin();local before=writes;local other=snapshotBuildings(b)
   local report=readerRead(false)
   for _,entry in ipairs({{'科研',3,5},{'生产力',4,7},{'金币',8,12},{'食物',3,8},{'信仰',3,9}})do
    local line=entry[1]..'｜每件 +'..entry[2]..'／本城 +'..entry[2]..'｜实测差值 '..string.format('%+.2f',entry[2])..'｜当前原生 '..string.format('%.2f',entry[3])
    assert(report:find(line,1,true),line)
   end
   assert(not report:find('作品文化',1,true) and report:find('不自动证明正常回合结算',1,true))
   assert(writes==before and readerModifierCalls==0 and probe.mode=='ACTIVE');assertBuildingsSame(b,other)
  """)

 def test_reader_reports_real_mismatch_and_explicit_refresh_after_delayed_native(self):
  lua=self.reader_runtime();lua.execute(r"""
   readerBegin();local before=writes;readerStale=true
   local report=readerRead(false)
   assert(report:find('科研｜每件 +3／本城 +3｜实测差值 +0.00｜当前原生 2.00',1,true))
   assert(not report:find('PASS',1,true))
   readerStale=false;readerOffsets.GOLD=-2
   report=readerRead(false)
   assert(report:find('金币｜每件 +8／本城 +8｜实测差值 +6.00｜当前原生 10.00',1,true))
   assert(report:find('科研｜每件 +3／本城 +3｜实测差值 +3.00',1,true))
   assert(writes==before and readerModifierCalls==0)
  """)

 def test_reader_nil_nan_inf_fail_and_release_successful_baseline(self):
  for bad in ('nil','nan','inf'):
   with self.subTest(bad=bad):
    lua=self.reader_runtime();lua.globals().readerBadCase=bad;lua.execute(r"""
     readerBegin();local before=writes;readerBad=readerBadCase
     local report=readerRead(false)
     assert(report:find('ME_UI_NATIVE_YIELD_UNKNOWN',1,true) and report:find('不记录成功基线',1,true))
     assert(not report:find('实测差值 +0.00',1,true))
     readerBad=nil;report=readerRead(false)
     assert(report:find('差值未确认',1,true) and report:find('当前原生 5.00',1,true))
     assert(writes==before and readerModifierCalls==0)
    """)

 def test_reader_current_facts_invalidate_comparison_but_preserve_finite_absolute_read(self):
  changes=(
   'readerPopulation=readerPopulation+1',
   'readerPopulation=0/0',
   'readerThemed=true',
   'readerMove=true',
   "readerOverrides.stamp='CHANGED_DEPTH'",
   'readerOverrides.currentActive=3',
   "readerOverrides.currentActiveStatus='UNKNOWN_GOVERNOR'",
   'readerOverrides.currentPotential=3',
   'turn=turn+1;collection();probe.Audit()',
  )
  for change in changes:
   with self.subTest(change=change):
    lua=self.reader_runtime();lua.execute('readerBegin();'+change);lua.execute(r"""
     local before=writes;local report=readerRead(false)
     assert(report:find('差值未确认',1,true) and report:find('实测差值 未确认',1,true))
     assert(report:find('当前原生 5.00',1,true) and not report:find('实测差值 +0.00',1,true))
     assert(writes==before and readerModifierCalls==0)
    """)

 def test_reader_new_turn_pending_pair_is_not_a_zero_or_successful_baseline(self):
  lua=self.reader_runtime();lua.execute(r"""
   readerBegin();turn=turn+1
   local before=writes;local calls=readerNativeCalls;local report=readerRead(false)
   assert(report:find('ME_UI_CONFIGURATION_PENDING',1,true) and report:find('不记录成功基线',1,true))
   assert(not report:find('实测差值 +0.00',1,true) and readerNativeCalls==calls and writes==before)
   collection();probe.Audit();before=writes;report=readerRead(false)
   assert(report:find('实测差值 未确认',1,true) and report:find('当前原生 5.00',1,true) and writes==before)
  """)

 def test_reader_count_definition_slots_theme_reference_guards(self):
  changes=(
   ('a.workCount=2','ME_UI_WORK_COUNT_MISMATCH'),
   ('readerThemed=nil','ME_UI_THEME_UNKNOWN'),
   ("a.GetBuildings().GetGreatWorkTypeFromIndex=function()return 'UNKNOWN_DEFINITION'end",'ME_UI_WORK_DEFINITION_UNKNOWN'),
   ('a.GetBuildings().GetNumGreatWorkSlots=function()return math.huge end','ME_UI_SLOTS_UNKNOWN'),
   ("readerOverrides.reference='WRONG_REFERENCE'",'ME_UI_REFERENCE_CHANGED'),
  )
  for change,code in changes:
   with self.subTest(code=code):
    lua=self.reader_runtime();lua.execute('readerBegin();'+change)
    # The fake GetBuildings recreates its function fields each call; persist
    # targeted method replacements by wrapping the existing getter.
    if code in ('ME_UI_WORK_DEFINITION_UNKNOWN','ME_UI_SLOTS_UNKNOWN'):
     method='GetGreatWorkTypeFromIndex' if code=='ME_UI_WORK_DEFINITION_UNKNOWN' else 'GetNumGreatWorkSlots'
     body="return 'UNKNOWN_DEFINITION'" if code=='ME_UI_WORK_DEFINITION_UNKNOWN' else 'return math.huge'
     lua.execute(f'local get=a.GetBuildings;a.GetBuildings=function(c)local b=get(c);b.{method}=function(){body} end;return b end')
    before=lua.globals().writes;report=lua.globals().readerRead(False)
    self.assertIn(code,report);self.assertNotIn('实测差值 +0.00',report)
    self.assertEqual(lua.globals().writes,before)

 def test_reader_off_clear_and_cold_cleanup_never_replay_previous_baseline(self):
  lua=self.reader_runtime();lua.execute(r"""
   local before=writes;assert(readerRead(false):find('测试已关闭',1,true));assert(writes==before)
   readerBegin();assert(readerRead(false):find('实测差值 +3.00',1,true))
   local before=writes;SPCBoostGreatWorkRead.ClearModifierRead()
   assert(readerRead(false):find('实测差值 +3.00',1,true)) -- Requests must not discard a good baseline.
   SPCBoostGreatWorkRead.ClearMeaningRead()
   local report=readerRead(false);assert(report:find('实测差值 未确认',1,true) and writes==before)
   probe.End(0,a,'reader-end');assert(readerRead(false):find('测试已关闭',1,true))
   probe.Advance(0,a,'reader-next-baseline');readerRead(true);probe.Advance(0,a,'reader-next-active')
   fire('LoadScreenClose');SPCBoostGreatWorkRead.ClearMeaningRead()
   assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and readerRead(false):find('测试已关闭',1,true))
   collection();probe.Advance(0,a,'reader-cold-baseline');probe.Advance(0,a,'reader-cold-active')
   assert(readerRead(false):find('实测差值 未确认',1,true)) -- Gameplay state cannot recreate UI baseline.
  """)
  source=(legacy.M/'UI/P0Panel.lua').read_text()
  self.assertIn('Events.LoadScreenClose.Add(showRoot)',source)
  show=source[source.index('local function showRoot()'):source.index('local function initialize()',source.index('local function showRoot()'))]
  self.assertIn('ClearMeaningRead()',show)
  self.assertIn('ContextPtr:SetShutdown(function()',source)
  shutdown=source[source.index('ContextPtr:SetShutdown(function()'):]
  self.assertIn('ClearMeaningRead()',shutdown)

 def test_panel_explicit_read_same_ack_and_copy_reuse_without_native_or_gameplay_work(self):
  lua=self.reader_runtime();lua.execute(r"""
   readerBegin();local before=writes
   UI={GetHeadSelectedCity=function()return a end}
   P.VERSION='L2C_READER_TEST';pendingToken='reader:ack';pendingAction='CULTURE_MEANING_READ';pageCity=1
   readings={};page=1;localReport=nil;meaningReadReference=SPCNetworkInput.Reference(a)
   function status(s)readerShown=s end;function print(s)readerLogged=s end
   local v=probe.View(0,a);v.token=pendingToken
   ExposedMembers.SPC_P0={Version=P.VERSION,LastToken=pendingToken,Snapshot='CURRENT_FIXTURE',CultureMeaningView=v}
  """)
  source=(legacy.M/'UI/P0Panel.lua').read_text()
  start=source.index('local function displayResponse()');end=source.index('-- B060 read/control requests',start)
  copy=source[source.index('local function copy()'):source.index("  local lines={'SPC_DIAGNOSTIC_REPORT_BEGIN'")]+"end\nreaderCopy=copy"
  lua.execute(source[start:end]+'\nreaderDisplay=displayResponse\n'+copy)
  lua.execute(r"""
   local before=writes;assert(readerDisplay())
   assert(readerShown:find('科研｜每件 +3／本城 +3｜实测差值 +3.00',1,true))
   local native=readerNativeCalls;local first=localReport
   assert(readerDisplay() and localReport==first and readerNativeCalls==native)
   readerCopy();readerCopy()
   assert(readerLogged:find('[SPC][MEANING_READ]',1,true) and readerNativeCalls==native)
   assert(readerModifierCalls==0 and writes==before and probe.mode=='ACTIVE')
  """)

 # Reviewed direct regressions, no four-state/native-reader/Culture candidate cases.
 test_k_pair_cold_request = legacy.MeaningProbeTests.test_real_sample_request_cold_c00_uses_both_receivers
 test_k_new_facts_not_old_dialogue = legacy.MeaningProbeTests.test_real_sample_callback_does_not_mix_new_facts_with_old_dialogue
 test_k_rejected_receiver_not_pair = legacy.MeaningProbeTests.test_real_sample_one_receiver_rejection_does_not_confirm_pair
 test_k_duplicate_sequence = legacy.MeaningProbeTests.test_real_sample_duplicate_sequence_does_not_reinterpret_changed_payload
 test_k_next_turn_recovers_same_phase = legacy.MeaningProbeTests.test_real_sample_next_turn_waits_for_current_pair_then_recovers_same_phase
 test_old_withdrawal_failure = legacy.MeaningProbeTests.test_old_withdrawal_failure_does_not_enable_new
 test_ingress_rejects_foreign_and_invalid_token = legacy.MeaningProbeTests.test_actual_request_invalid_or_foreign_ingress_does_not_run_probe
 test_exact_import_registry = legacy.MeaningProbeTests.test_import_registry_rejects_each_missing_action_import


if __name__ == '__main__':
 unittest.main()
