"""Shared D L2 tests: actual old/new Lua business projections and bounded reads.

Uses only test_p0_a's fixture/function prefix, never its historical stress body.
Counters measure this synthetic fixture, not native CPU/memory improvement.
Requires lupa.lua55 and the reviewed pre-repair Git object; no external DB.
"""
from pathlib import Path
from functools import lru_cache
import subprocess
import unittest
from unittest.mock import patch

R = Path(__file__).resolve().parents[1]
BASELINE = 'df0cc39'
MODELS = ('ResearchApplyModel', 'ResearchChairModel', 'ResearchInfrastructureShadow',
          'CultureAestheticModel', 'CultureMeaningModel')


@lru_cache(maxsize=6)
def baseline_source(module):
    return subprocess.check_output(['git', 'show', BASELINE + ':Mod/' + module + '.lua'], cwd=R, text=True)


def fixture(old=False, setup='', instrument=False):
    path = R / 'DevelopmentTests/test_p0_a.py'
    source = path.read_text()
    boundary = '\nl=runtime()'
    assert source.count(boundary) == 2, 'maintained P0-A prefix boundary changed'
    namespace = {'__file__': str(path)}
    exec(compile(source[:source.index(boundary)], str(path), 'exec'), namespace)
    lua = namespace['runtime']()
    lua.globals().print = lambda *parts: None
    for module in MODELS:
        lua.execute(baseline_source(module) if old else (R / 'Mod' / (module + '.lua')).read_text())
    text = baseline_source('DistrictCompleteness') if old else (R / 'Mod/DistrictCompleteness.lua').read_text()
    if instrument:
        marker = 'local function clone(v)\n'
        assert text.count(marker) == 1, 'clone instrumentation seam changed'
        text = text.replace(marker, marker + ''' if type(v)=='table'then
 __cloneTables=__cloneTables+1
 if v.name~=nil then __cloneNamedRows=__cloneNamedRows+1 end
 if v.excluded~=nil then __cloneExcludedTrees=__cloneExcludedTrees+1 end
 end
''')
        lua.execute('__cloneTables=0;__cloneNamedRows=0;__cloneExcludedTrees=0;__compactCalculations=0;__detailCalculations=0')
    lua.execute(text)
    if instrument:
        lua.execute('''local calculate=SPCDistrictCompleteness.Calculate
SPCDistrictCompleteness.Calculate=function(catalog,raw,detail)
 if detail==false then __compactCalculations=__compactCalculations+1;__lastRaw=raw
 else __detailCalculations=__detailCalculations+1 end
 return calculate(catalog,raw,detail)
end''')
    lua.execute(r'''
returnCallbacks={}
shared.CityProgressionStore={RegisterReturn=function(name,callback)returnCallbacks[name]=callback end}
function restart()
 SPCDistrictCompleteness.Start(P,shared);svc=shared.DistrictCompleteness
 counters={};reads=0;writes=0
end
function sample(detail)
 if detail then return svc.Read(0,c,c.token)end
 return svc.ReadFacts and svc.ReadFacts(0,c,c.token)or svc.Read(0,c,c.token)
end
function compact(v)
 local out=SPCDistrictCompleteness.Clone(v)
 if out.value then
  out.value.excluded=nil
  for _,district in ipairs(out.value.districts)do
   for _,building in ipairs(district.buildings)do building.name=nil;building.tierSource=nil end
  end
 end
 return out
end
function encode(value)
 if type(value)~='table'then return type(value)..':'..tostring(value)end
 local keys={};for key in pairs(value)do keys[#keys+1]=key end
 table.sort(keys,function(a,b)return tostring(a)<tostring(b)end)
 local out={};for _,key in ipairs(keys)do out[#out+1]=encode(key)..'='..encode(value[key])end
 return '{'..table.concat(out,',')..'}'
end
function modelPlans(view)
 local first=c.ds[1]
 local f={validity='VERIFIED',identity='RESEARCH',active=c.active,potential=4,
  activeStatus=c.active and 'KNOWN'or 'UNKNOWN',first={districtID=first.id,type=GameInfo.Districts[first.type].DistrictType}}
 local targets={};for _,row in ipairs(brows)do targets[row.BuildingType]=true end
 local culture=SPCDistrictCompleteness.Clone(f);culture.identity='CULTURE'
 local works={hasConfirmed=true,availability='KNOWN',eraCount=2,count=2,modifierExcludedCount=0,unknownCategoryCount=0}
 local result={}
 local calls={
  Apply=function()return SPCResearchApplyModel.Plan(f,view,first.workers)end,
  Chair=function()return SPCResearchChairModel.Plan(f,view,first.workers,targets)end,
  Infrastructure=function()return SPCResearchInfrastructureShadow.Plan(SPCResearchInfrastructureShadow.WithWorkers(f,view),view)end,
  Aesthetic=function()return SPCCultureAestheticModel.Plan(culture,works,view,false)end,
  Meaning=function()return SPCCultureMeaningModel.Plan(culture,works,view)end}
 for name,call in pairs(calls)do
  local ok,plan=pcall(call)
  if ok then
   -- Chair name is a presentation field; all business rows/amounts stay compared.
   if name=='Chair'then for _,row in ipairs(plan.rows)do row.name=nil end end
   result[name]={ok=true,value=plan}
  else result[name]={ok=false,code=tostring(plan):match('[A-Z][A-Z0-9_]+')}end
 end
 return result
end
function building(v,name)
 for _,district in ipairs(v.value.districts)do for _,item in ipairs(district.buildings)do
  if item.type==name then return item,district end
 end end
end
function addDefinitions(n,kind)
 for i=1,n do
  local row={Index=#brows+1,BuildingType=(kind=='internal'and 'BUILDING_SPC_FIXTURE_'or 'BUILDING_UNKNOWN_FIXTURE_')..i,
   PrereqDistrict='DISTRICT_CAMPUS',Name='LOC_FIXTURE_'..i,InternalOnly=kind=='internal',IsWonder=false}
  brows[#brows+1]=row
 end
 GameInfo.Buildings=db(brows,'BuildingType')
end
''')
    lua.execute(setup + '\nrestart()')
    return lua


def writer_fixture(old=False):
    # Prefix includes the maintained in-memory SQL and P0-C native mocks only.
    # Both wrappers stop before their matrix/stress/version-guard bodies.
    original = Path.read_text
    owned = {module + '.lua' for module in MODELS +
             ('DistrictCompleteness', 'ResearchApply', 'ResearchChair', 'ResearchInfrastructure')}
    frozen = {name: baseline_source(name[:-4]) for name in owned} if old else {}

    def read(path, *args, **kwargs):
        if old and path.parent == R / 'Mod' and path.name in frozen:
            return frozen[path.name]
        return original(path, *args, **kwargs)

    with patch.object(Path, 'read_text', read):
        path = R / 'DevelopmentTests/test_research_chair.py'
        source = path.read_text()
        boundary = '\nchains='
        assert source.count(boundary) == 1, 'maintained Research Chair prefix boundary changed'
        namespace = {'__file__': str(path)}
        exec(compile(source[:source.index(boundary)], str(path), 'exec'), namespace)
        lua = namespace['runtime']()
    lua.globals().print = lambda *parts: None
    lua.execute('''function carrierSnapshot()
local out={}
for _,city in pairs(cities)do
 local ids={};for id,yes in pairs(city.carriers or {})do if yes then ids[#ids+1]=id end end
 table.sort(ids);out[#out+1]=city.id..':'..table.concat(ids,',')
end
 table.sort(out);return table.concat(out,'|')..';writes='..writes
end
c.active=4;d.workers=2;setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'})
i=addDistrict(c,20,'DISTRICT_INDUSTRIAL_ZONE');setBuildings(i,{'BUILDING_IZ_WATER_MILL'})
''')
    return lua


class SharedDFactRead(unittest.TestCase):

    def test_five_actual_models_match_frozen_business_values(self):
        scenarios = {
            'empty': '',
            'T1': "setBuildings(d,{'BUILDING_LIBRARY'})",
            'T2': "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'})",
            'T3': "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY','BUILDING_JNR_LABORATORY'})",
            'T4': "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY','BUILDING_JNR_LABORATORY','BUILDING_RESEARCH_LAB'})",
            'cap13': "setBuildings(d,{'BUILDING_JNR_LABORATORY','BUILDING_JNR_ARCHITECTURE','BUILDING_JNR_LIBERAL_ARTS','BUILDING_RESEARCH_LAB'})",
            'replacement': "setBuildings(d,{'BUILDING_MADRASA'});d.type=GameInfo.Districts.DISTRICT_SEOWON.Index",
            'pillage': "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});d.bs[1].pillaged=true",
            'unfinished': "setBuildings(d,{'BUILDING_LIBRARY'});d.complete=false",
            'queued': "setBuildings(d,{'BUILDING_LIBRARY'});c.queued='BUILDING_UNIVERSITY'",
            'tier0': "setBuildings(d,{'BUILDING_LIBRARY'});GameInfo.HD_BuildingTiers.BUILDING_LIBRARY.Tier=0",
            'tierNil': "setBuildings(d,{'BUILDING_LIBRARY'});GameInfo.HD_BuildingTiers.BUILDING_LIBRARY.Tier=nil",
            'tierUnsupported': "setBuildings(d,{'BUILDING_LIBRARY'});GameInfo.HD_BuildingTiers.BUILDING_LIBRARY.Tier=9",
            'foreignBuildingDomain': "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_BANK'})",
            'inactive': "setBuildings(d,{'BUILDING_LIBRARY'});c.active=1",
            'unknownActive': "setBuildings(d,{'BUILDING_LIBRARY'});c.active=nil",
            'mixedDomains': "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});local t=addDistrict(c,12,'DISTRICT_THEATER');setBuildings(t,{'BUILDING_AMPHITHEATER'});local z=addDistrict(c,13,'DISTRICT_INDUSTRIAL_ZONE');setBuildings(z,{'BUILDING_WORKSHOP','BUILDING_FACTORY'});local n=addDistrict(c,14,'DISTRICT_NEIGHBORHOOD');setBuildings(n,{'BUILDING_HD_INN','BUILDING_FOOD_MARKET'})",
        }
        for name, setup in scenarios.items():
            with self.subTest(scenario=name):
                values = []
                for old in (True, False):
                    lua = fixture(old, setup)
                    values.append(lua.execute('local v=sample(false);return encode(compact(v)),encode(modelPlans(v))'))
                self.assertEqual(values[0], values[1])

    def test_detail_shape_exact_legacy_and_normal_has_no_display_tree(self):
        setup = "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_WONDER','BUILDING_SPC_INTERNAL','BUILDING_UNKNOWN_MOD'});c.queued='BUILDING_UNIVERSITY'"
        old, new = fixture(True, setup), fixture(False, setup)
        self.assertEqual(old.execute('return encode(sample(true))'), new.execute('return encode(sample(true))'))
        new.execute(r'''
local v=sample(false);assert(v.value.excluded==nil)
for _,district in ipairs(v.value.districts)do for _,b in ipairs(district.buildings)do
 assert(b.name==nil and b.tierSource==nil)
end end
local full=sample(true);assert(#full.value.excluded==1)
assert(building(full,'BUILDING_LIBRARY').name=='BUILDING_LIBRARY')
assert(building(full,'BUILDING_LIBRARY').tierSource~=nil)
assert(building(full,'BUILDING_WONDER').reason=='WONDER')
assert(building(full,'BUILDING_SPC_INTERNAL').reason=='INTERNAL_OR_TECHNICAL')
''')

    def test_mode_switch_no_native_capture_revision_or_publish(self):
        lua = fixture(False, "setBuildings(d,{'BUILDING_LIBRARY'});c.queued='BUILDING_UNIVERSITY'")
        lua.execute(r'''
local v=sample(false);local cap=counters.dc_capture;local pub=counters.dc_publish
local rev=v.revision;local before=reads;local normal=encode(v)
local full=sample(true);assert(full.revision==rev and full.value.excluded[1].reason=='UNDER_CONSTRUCTION')
assert(encode(sample(false))==normal and counters.dc_capture==cap and counters.dc_publish==pub and reads==before)
local again=sample(true);assert(encode(again)==encode(full)and reads==before)
''')

    def test_detached_normal_and_detail_mutations(self):
        lua = fixture(False, "setBuildings(d,{'BUILDING_LIBRARY'});c.queued='BUILDING_UNIVERSITY'")
        lua.execute(r'''
local v=sample(false);local normal=encode(v);v.reference.token='bad';v.value.domains.DISTRICT_CAMPUS.value=999
v.value.districts[1].buildings[1].tier=99;assert(encode(sample(false))==normal)
local detail=sample(true);local expected=encode(detail);detail.value.excluded[1].reason='bad'
detail.value.districts[1].buildings[1].name='bad';assert(encode(sample(true))==expected)
assert(encode(sample(false))==normal and writes==0)
''')

    def test_same_turn_dirty_new_turn_and_hit(self):
        lua = fixture(False, "setBuildings(d,{'BUILDING_LIBRARY'})")
        lua.execute(r'''
local v=sample(false);local rev=v.revision;local cap=counters.dc_capture
sample(false);assert(counters.dc_capture==cap)
fire('CityBuildingsChanged',0,1);local same=sample(false);assert(same.revision==rev and counters.dc_capture==cap+1)
setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});fire('CityBuildingsChanged',0,1)
v=sample(false);assert(v.revision>rev and v.value.domains.DISTRICT_CAMPUS.value==3)
local full=sample(true);assert(full.revision==v.revision and #full.value.districts[1].buildings==2)
rev=v.revision;setBuildings(d,{'BUILDING_LIBRARY'});turn=turn+1;v=sample(false)
assert(v.revision>rev and v.value.domains.DISTRICT_CAMPUS.value==1)
''')

    def test_held_sample_and_initial_unknown_do_not_relax_availability(self):
        for old in (True, False):
            with self.subTest(old=old):
                lua = fixture(old, "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'})")
                lua.execute(r'''
local v=sample(false);local rev=v.revision;failRead=true;svc.MarkDirty(0,1);v=sample(false)
assert(v.validity=='VERIFIED'and v.availability=='TEMPORARILY_UNAVAILABLE'and v.revision==rev)
assert(v.value.domains.DISTRICT_CAMPUS.value==3)
local cap=counters.dc_capture;local detail=sample(true);assert(detail.availability=='TEMPORARILY_UNAVAILABLE')
assert(counters.dc_capture==cap and not modelPlans(v).Apply.ok)
c.token='new-reference';v=sample(false);assert(v.validity=='UNKNOWN'and v.value==nil)
failRead=false;turn=turn+1;v=sample(false);assert(v.availability=='READY')
''')

    def test_nonordinary_native_read_errors_remain_held(self):
        for cause in ('presence', 'pillage', 'location'):
            with self.subTest(cause=cause):
                expected = []
                for old in (True, False):
                    lua = fixture(old, "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_SPC_INTERNAL'})")
                    lua.execute('sample(false);broken=GameInfo.Buildings.BUILDING_SPC_INTERNAL.Index;originalBuildings=c.GetBuildings')
                    method = {'presence': 'HasBuilding', 'pillage': 'IsPillaged', 'location': 'GetBuildingLocation'}[cause]
                    lua.globals().methodName = method
                    lua.execute(r'''
c.GetBuildings=function(self)
 local b=originalBuildings(self);local original=b[methodName]
 b[methodName]=function(s,index)if index==broken then error('INTERNAL_READ_FAILED')end;return original(s,index)end
 return b
end
svc.MarkDirty(0,1);v=sample(false)
assert(v.availability=='TEMPORARILY_UNAVAILABLE'and v.validity=='VERIFIED')
''')
                    expected.append(lua.execute('return v.value.domains.DISTRICT_CAMPUS.value,v.error:match("INTERNAL_READ_FAILED")'))
                self.assertEqual(expected[0], expected[1])

    def test_location_failures_and_off_district_nonordinary(self):
        for location in (-1, 9999):
            with self.subTest(location=location):
                for old in (True, False):
                    lua = fixture(old, "setBuildings(d,{'BUILDING_LIBRARY'})")
                    lua.globals().badLocation = location
                    lua.execute('sample(false);d.bs[1].location=badLocation;svc.MarkDirty();local v=sample(false);assert(v.availability=="TEMPORARILY_UNAVAILABLE"and v.value.domains.DISTRICT_CAMPUS.value==1)')
        lua = fixture(False, "setBuildings(d,{'BUILDING_WONDER'});d.bs[1].location=9999")
        lua.execute('local v=sample(false);assert(v.availability=="READY"and v.value.excluded==nil);local f=sample(true);assert(f.value.excluded[1].reason=="WONDER"and f.value.excluded[1].plot==9999)')

    def test_reference_owner_epoch_return_and_city_isolation(self):
        lua = fixture(False, "setBuildings(d,{'BUILDING_LIBRARY'})")
        lua.execute(r'''
local first=sample(false);local other=newCity(2);local od=addDistrict(other,21,'DISTRICT_CAMPUS');setBuildings(od,{'BUILDING_UNIVERSITY'})
local control=svc.ReadFacts(0,other,other.token);local cap=counters.dc_capture
svc.MarkDirty(0,1);sample(false);svc.ReadFacts(0,other,other.token);assert(counters.dc_capture==cap+1)
c.token='replacement';local v=sample(false);assert(v.reference.token=='replacement')
c.owner=1;local ok,err=pcall(sample,false);assert(not ok and tostring(err):find('DC_OWNER_CHANGED'))
c.owner=0;local epoch=v.epoch;fire('LoadScreenClose');assert(svc.CacheSize()==0)
v=sample(false);assert(v.epoch==epoch+1)
cap=counters.dc_capture;returnCallbacks.DistrictCompleteness(0);sample(false);assert(counters.dc_capture==cap+1)
assert(svc.ReadFacts(0,other,other.token).value.domains.DISTRICT_CAMPUS.value==2 and writes==0)
''')

    def test_multiple_community_tie_and_highest_single_district(self):
        values = []
        setup = "local a=addDistrict(c,12,'DISTRICT_NEIGHBORHOOD');local b=addDistrict(c,13,'DISTRICT_NEIGHBORHOOD');setBuildings(a,{'BUILDING_HD_INN','BUILDING_FOOD_MARKET'});setBuildings(b,{'BUILDING_HD_TAVERN','BUILDING_JNR_ART_GALLERY'});setBuildings(d,{'BUILDING_LIBRARY'})"
        for old in (True, False):
            lua = fixture(old, setup)
            values.append(lua.execute(r'''
local v=sample(false);assert(v.value.domains.DISTRICT_NEIGHBORHOOD.districtID==12)
local before=encode(modelPlans(v));setBuildings(c.ds[3],{'BUILDING_HD_TAVERN','BUILDING_JNR_ART_GALLERY','BUILDING_JNR_HOSPITAL'})
svc.MarkDirty();v=sample(false);assert(v.value.domains.DISTRICT_NEIGHBORHOOD.districtID==13)
return before,encode(modelPlans(v)),encode(compact(v))
'''))
        self.assertEqual(values[0], values[1])

    def test_pure_calculate_detail_default_and_compact_share_values(self):
        lua = fixture()
        lua.execute(r'''
local raw={districts={{id=11,type='DISTRICT_CAMPUS',plot=d.plot,complete=true,pillaged=false,
 buildings={{index=GameInfo.Buildings.BUILDING_LIBRARY.Index,complete=true,pillaged=false}}}},
 unplaced={{type='BUILDING_WONDER',reason='WONDER',contribution=0,pillaged=false,plot=999}}}
local full=SPCDistrictCompleteness.Calculate(cat,raw)
local normal=SPCDistrictCompleteness.Calculate(cat,raw,false)
assert(full.excluded[1].reason=='WONDER'and full.districts[1].buildings[1].name=='BUILDING_LIBRARY')
assert(normal.excluded==nil and normal.districts[1].buildings[1].name==nil)
assert(encode(compact({value=full}))==encode({value=normal}))
''')

    def test_definition_scaling_counts_retained_presence_and_removed_detail(self):
        for kind in ('internal', 'unknown'):
            for extra in (0, 100, 1000):
                with self.subTest(kind=kind, extra=extra):
                    results = []
                    for old in (True, False):
                        lua = fixture(old, f"addDefinitions({extra},'{kind}');setBuildings(d,{{'BUILDING_LIBRARY'}});c.queued='BUILDING_UNIVERSITY'")
                        results.append(lua.execute(r'''
local v=sample(false);local native=reads;local checks=counters.building_check;local cap=counters.dc_capture
assert(checks==#brows and writes==0)
local before=counters.dc_publish;sample(true);sample(false)
assert(reads==native and counters.dc_capture==cap and counters.dc_publish==before)
return checks,encode(compact(v)),encode(modelPlans(v)),v.value.excluded~=nil
'''))
                    self.assertEqual(results[0][:3], results[1][:3])
                    self.assertTrue(results[0][3])
                    self.assertFalse(results[1][3])
                    print(f'D_FIXTURE {kind} +{extra}: presence_checks={results[1][0]} retained; '
                          'normal excluded_tree=absent; business=MATCH; not native CPU/memory evidence')

    def test_normal_miss_hit_and_post_detail_hit_avoid_full_construction_and_copy(self):
        lua = fixture(False, "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_WONDER'});d.bs[2].location=9999;c.queued='BUILDING_UNIVERSITY'", instrument=True)
        lua.execute(r'''
local first=sample(false);assert(__compactCalculations==1 and __detailCalculations==0)
assert(__cloneNamedRows==0 and __cloneExcludedTrees==0)
assert(__lastRaw.unplaced==nil and __lastRaw.queued=='BUILDING_UNIVERSITY')
assert(__lastRaw.observations[1].type==nil and __lastRaw.observations[1].reason==nil)
local tables=__cloneTables;sample(false)
assert(__cloneTables>tables and __detailCalculations==0 and __cloneNamedRows==0 and __cloneExcludedTrees==0)
local full=sample(true);assert(__detailCalculations==1 and #full.value.excluded==2)
assert(__cloneNamedRows==1 and __cloneExcludedTrees==1)
local named,excluded=__cloneNamedRows,__cloneExcludedTrees
sample(false);assert(__detailCalculations==1 and __cloneNamedRows==named and __cloneExcludedTrees==excluded)
sample(true);assert(__detailCalculations==1 and __cloneNamedRows==named+1 and __cloneExcludedTrees==excluded+1)
svc.MarkDirty();sample(false);assert(__compactCalculations==2 and __detailCalculations==1)
assert(__cloneNamedRows==named+1 and __cloneExcludedTrees==excluded+1)
sample(true);assert(__detailCalculations==2)
''')
        print('D_CONSTRUCTION normal miss/hit/detail-to-normal: full_calculations=0 and named/excluded clones=0; detailed read builds once per confirmed capture')

    def test_five_model_round_shares_one_capture_and_keeps_business_comparison(self):
        output = []
        setup = "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});local t=addDistrict(c,12,'DISTRICT_THEATER');setBuildings(t,{'BUILDING_AMPHITHEATER'});c.queued='BUILDING_JNR_LABORATORY'"
        for old in (True, False):
            lua = fixture(old, setup, instrument=True)
            output.append(lua.execute(r'''
local plans={};for _,name in ipairs({'Apply','Chair','Infrastructure','Aesthetic','Meaning'})do
 local v=sample(false);plans[name]=modelPlans(v)[name]
end
assert(counters.dc_read==5 and counters.dc_capture==1 and counters.building_check==#brows)
return encode(plans),__compactCalculations,__detailCalculations,__cloneNamedRows,__cloneExcludedTrees,counters.building_check
'''))
        self.assertEqual(output[0][0], output[1][0])
        self.assertEqual(output[0][2], 1)
        self.assertEqual(output[0][3:5], (15, 5))
        self.assertEqual(output[1][1:5], (1, 0, 0, 0))
        self.assertEqual(output[0][-1], output[1][-1])
        print(f'D_ROUND five projections: captures=1->1; presence={output[1][-1]} retained; '
              'full calculations=1->0; returned named-row clones=15->0; excluded-tree clones=5->0; business=MATCH')

    def test_owner_change_during_capture_holds_instead_of_publishing(self):
        for old in (True, False):
            with self.subTest(old=old):
                lua = fixture(old, "setBuildings(d,{'BUILDING_LIBRARY'})")
                lua.execute(r'''
local first=sample(false);local rev=first.revision;local pub=counters.dc_publish
local get=c.GetBuildings;local changed=false
c.GetBuildings=function(self)
 local b=get(self);local has=b.HasBuilding
 b.HasBuilding=function(s,index)
  if not changed then c.owner=1;changed=true end
  return has(s,index)
 end
 return b
end
svc.MarkDirty(0,1);local v=sample(false)
assert(v.validity=='VERIFIED'and v.availability=='TEMPORARILY_UNAVAILABLE')
assert(v.error:find('DC_OWNER_CHANGED_DURING_READ')and v.revision==rev and counters.dc_publish==pub)
c.owner=0;c.GetBuildings=get;turn=turn+1;assert(sample(false).availability=='READY')
''')

    def test_diagnostic_only_change_refreshes_detail_without_business_publish(self):
        lua = fixture(False, "setBuildings(d,{'BUILDING_LIBRARY'});c.queued='BUILDING_UNIVERSITY'", instrument=True)
        lua.execute(r'''
local v=sample(false);local rev=v.revision;local pub=counters.dc_publish
local before=encode(modelPlans(v));assert(sample(true).value.excluded[1].type=='BUILDING_UNIVERSITY')
c.queued='BUILDING_JNR_LABORATORY';svc.MarkDirty(0,1);v=sample(false)
assert(v.revision==rev and counters.dc_publish==pub and encode(modelPlans(v))==before)
assert(sample(true).value.excluded[1].type=='BUILDING_JNR_LABORATORY')
setBuildings(d,{'BUILDING_LIBRARY','BUILDING_WONDER'});d.bs[2].location=9999
svc.MarkDirty(0,1);v=sample(false)
assert(v.revision==rev and counters.dc_publish==pub and encode(modelPlans(v))==before)
local detail=sample(true);assert(detail.value.excluded[1].type=='BUILDING_WONDER'and #detail.value.excluded==2)
''')

    def test_actual_research_writers_carriers_and_writes_match_eight_transitions(self):
        outputs = []
        transitions = ('',
                       "setBuildings(i,{'BUILDING_IZ_WATER_MILL','BUILDING_WORKSHOP'});svc.MarkDirty()",
                       'd.bs[1].pillaged=true;svc.MarkDirty()',
                       'd.bs[1].pillaged=false;svc.MarkDirty()',
                       'failRead=true;svc.MarkDirty()',
                       'failRead=false;svc.MarkDirty()',
                       'c.active=2', 'c.active=4')
        for old in (True, False):
            lua = writer_fixture(old)
            trace = []
            for index, delta in enumerate(transitions):
                with self.subTest(old=old, transition=index):
                    lua.execute(delta + ';shared.ResearchApply.Audit();shared.ResearchChair.Audit();shared.ResearchInfrastructure.Audit()')
                    trace.append(lua.eval('carrierSnapshot()'))
            lua.execute(r'''
assert(not shared.ResearchApply.definitionError and not shared.ResearchChair.definitionError)
local before=writes;local cap=counters.dc_capture
local a=shared.ResearchApply.Describe(0,c,true)
local b=shared.ResearchChair.Describe(0,c,true)
local v=shared.ResearchInfrastructure.Describe(0,c,true)
assert(a:find('Tier')and b:find('Tier')and v:find('Tier'))
assert(writes==before and counters.dc_capture==cap)
''')
            outputs.append(trace)
        self.assertEqual(outputs[0], outputs[1])
        print('D_ACTUAL_WRITERS Apply/Chair/Infrastructure eight transitions: carrier sets and cumulative writes MATCH; detailed reports remain full and read-only')

    def test_actual_apply_missing_tier_guard_uses_correct_normal_reader(self):
        for old in (True, False):
            with self.subTest(old=old):
                lua = writer_fixture(old)
                lua.execute(r'''
local apply=shared.ResearchApply;apply.Audit({player=0})
assert(not apply.definitionError and not apply.errors[0][1])
local reader=svc.ReadFacts and 'ReadFacts'or 'Read';local original=svc[reader]
svc[reader]=function(...)
 local v=original(...)
 for _,district in ipairs(v.value.districts)do for _,b in ipairs(district.buildings)do
  if b.type=='BUILDING_LIBRARY'then b.tier=nil end
 end end
 return v
end
setBuildings(i,{'BUILDING_IZ_WATER_MILL','BUILDING_WORKSHOP'});svc.MarkDirty()
local before=writes;local snapshot=carrierSnapshot();apply.Audit({player=0})
assert(apply.errors[0][1]:find('AP_BUILDING_FACT_UNKNOWN'))
assert(writes==before and carrierSnapshot()==snapshot)
svc[reader]=original;apply.Audit({player=0});assert(not apply.errors[0][1]and writes>before)
''')

    def test_cache_bound_stays_eight(self):
        lua = fixture()
        lua.execute(r'''
for i=1,12 do local x=newCity(i);local district=addDistrict(x,100+i,'DISTRICT_CAMPUS')
 setBuildings(district,{'BUILDING_LIBRARY'});svc.ReadFacts(0,x,x.token)
 assert(svc.CacheSize()<=8)
end
assert(svc.CacheSize()==8 and writes==0)
''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
