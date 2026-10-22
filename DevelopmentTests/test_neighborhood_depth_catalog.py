"""B164 scoped Catalog -> Shared D consumers; LOCAL simulation, not native PASS.

The four reviewed Neighborhood definitions come from the explicitly configured
read-only DB. Frozen P0-A supplies fixture definitions only; its historical gates
and stress runs are never executed. No game, deployment, or external writes.
"""
from pathlib import Path
import ast
from contextlib import closing
import sqlite3
import unittest

from project_paths import external_database

R = Path(__file__).resolve().parents[1]
M = R / 'Mod'
TARGETS = {'BUILDING_HD_VILLA': 1, 'BUILDING_HD_MANSION': 1,
           'BUILDING_HD_BUS_STOP': 2, 'BUILDING_FOOD_MARKET': 3}
NEW_TARGETS = tuple(name for name in TARGETS if name != 'BUILDING_FOOD_MARKET')
fixture_path = R / 'DevelopmentTests/test_p0_a.py'
fixture_tree = ast.parse(fixture_path.read_text())
fixture_ns = {'__file__': str(fixture_path)}
kept = [node for node in fixture_tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
        or isinstance(node, ast.Assign)
        and all(isinstance(target, ast.Name) and target.id in {'R', 'M', 'NEW', 'FIX'}
                for target in node.targets)]
exec(compile(ast.Module(body=kept, type_ignores=[]), str(fixture_path), 'exec'), fixture_ns)

WRAPPER = r'''
P.Rows=function(t) local rows={};for row in GameInfo[t]() do rows[#rows+1]=row end;return rows end
P.HasBuilding=function(b,id) return b:HasBuilding(id) end
P.CreateBuilding=function(q,id)
 assert(not q.city.carriers[id]);q.city.carriers[id]=true;writes=writes+1
 fire('BuildingAddedToMap',0,0,id,q.city.owner)
end
P.RemoveBuilding=function(b,id)
 assert(b.city.carriers[id]);b.city.carriers[id]=nil;writes=writes+1
 fire('BuildingRemovedFromMap',0,0,id,b.city.owner)
end
function wrap(city)
 city.carriers={};local native=city.GetBuildings;local queue=city:GetBuildQueue()
 city.GetBuildings=function()
  local buildings=native();local has,location,pillaged=buildings.HasBuilding,buildings.GetBuildingLocation,buildings.IsPillaged
  buildings.city=city
  buildings.HasBuilding=function(_,id) return city.carriers[id]==true or has(buildings,id) end
  buildings.GetBuildingLocation=function(_,id) if city.carriers[id] then return city.ds[1].plot end;return location(buildings,id) end
  buildings.IsPillaged=function(_,id) if city.carriers[id] then return false end;return pillaged(buildings,id) end
  return buildings
 end
 queue.city=city;city.GetBuildQueue=function() return queue end
end
Players[0].GetCities=function() return {Members=function() return pairs(cities) end,FindID=function(_,id) return cities[id] end} end
function sample(city) city=city or c;return svc.Read(city.owner,city,city.token) end
function verified(city)
 local view=sample(city);assert(view.validity=='VERIFIED' and view.availability=='READY',view.error);return view
end
function meaning(view,count)
 return SPCCultureMeaningModel.Plan({validity='VERIFIED',identity='CULTURE',potential=4,active=4,activeStatus='KNOWN'},
  {hasConfirmed=true,availability='KNOWN',count=count or 1,modifierExcludedCount=0,unknownCategoryCount=0},view)
end
function applyPlan(city,view)
 return SPCResearchApplyModel.Plan(SPCCurrentSpecializationFacts.Read(P,shared,city.owner,city),view,2)
end
function auditApply()
 ap.Audit({player=0});assert(not ap.definitionError,ap.definitionError)
 for _,errors in pairs(ap.errors) do for _,err in pairs(errors) do error(err) end end
end
function food(city)
 local total=0;for bit=0,4 do
  if city.carriers[GameInfo.Buildings['BUILDING_SPC_RESEARCH_APPLY_FOOD_'..bit].Index] then total=total+2^bit end
 end;return total
end
function neighborhood(view) return view.value.domains.DISTRICT_NEIGHBORHOOD end
function buildingFact(view,kind)
 for _,district in ipairs(view.value.districts) do for _,building in ipairs(district.buildings) do
  if building.type==kind then return building end
 end end
end
'''


class NeighborhoodDepthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = external_database(R)
        marks = ','.join('?' for _ in TARGETS)
        with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as db:
            db.row_factory = sqlite3.Row
            cls.reviewed = [dict(row) for row in db.execute(
                f'SELECT BuildingType,Name,PrereqDistrict,Cost,InternalOnly,IsWonder FROM Buildings WHERE BuildingType IN ({marks})', tuple(TARGETS))]
            cls.tiers = [dict(row) for row in db.execute(
                f'SELECT * FROM HD_BuildingTiers WHERE BuildingType IN ({marks})', tuple(TARGETS))]
            assert {row['BuildingType'] for row in cls.reviewed} == set(TARGETS)
            assert {row['BuildingType']: row['Tier'] for row in cls.tiers} == TARGETS
            assert all(row['PrereqDistrict'] == 'DISTRICT_NEIGHBORHOOD' and not row['InternalOnly'] and not row['IsWonder'] for row in cls.reviewed)
            assert not list(db.execute(f'SELECT * FROM HD_DUMMY_BUILDINGS WHERE BuildingType IN ({marks})', tuple(TARGETS)))
            assert not list(db.execute(f'SELECT * FROM BuildingReplaces WHERE CivUniqueBuildingType IN ({marks}) OR ReplacesBuildingType IN ({marks})', tuple(TARGETS) * 2))
        with closing(sqlite3.connect(':memory:')) as sql:
            sql.row_factory = sqlite3.Row
            sql.executescript('CREATE TABLE Types(Type TEXT,Kind TEXT);CREATE TABLE Buildings(BuildingType TEXT,Name TEXT,Cost INTEGER,PrereqDistrict TEXT,InternalOnly INTEGER,CitizenSlots INTEGER,Housing INTEGER);CREATE TABLE Building_CitizenYieldChanges(BuildingType TEXT,YieldType TEXT,YieldChange INTEGER);')
            sql.executescript((M / 'Data/ResearchApply.sql').read_text())
            cls.carriers = [dict(row, Index=10000 + index, IsWonder=False) for index, row in enumerate(sql.execute('SELECT * FROM Buildings'))]
            cls.yields = [dict(row) for row in sql.execute('SELECT * FROM Building_CitizenYieldChanges')]
            assert len(cls.carriers) == len(cls.yields) == 25

    def runtime(self):
        lua = fixture_ns['runtime']()
        convert = lambda value: fixture_ns['to_lua'](lua, value)
        lua.globals().reviewed = convert(self.reviewed)
        lua.globals().reviewedTiers = convert(self.tiers)
        lua.globals().carriers = convert(self.carriers)
        lua.globals().yieldRows = convert(self.yields)
        lua.globals().include = lambda name: lua.execute((M / (name + '.lua')).read_text())
        lua.execute(r'''
         for _,source in ipairs(reviewed) do
          local target
          for _,row in ipairs(brows) do if row.BuildingType==source.BuildingType then target=row;break end end
          if not target then target={Index=#brows+1};brows[#brows+1]=target end
          for key,value in pairs(source) do target[key]=value end
         end
         for _,source in ipairs(reviewedTiers) do
          local target
          for _,row in ipairs(tiers) do if row.BuildingType==source.BuildingType then target=row;break end end
          if not target then target={};tiers[#tiers+1]=target end
          for key,value in pairs(source) do target[key]=value end
         end
         for _,row in ipairs(carriers) do brows[#brows+1]=row end
         GameInfo.Buildings=db(brows,'BuildingType');GameInfo.HD_BuildingTiers=db(tiers,'BuildingType')
         GameInfo.Building_CitizenYieldChanges=db(yieldRows,'BuildingType')
         cat=SPCOrdinaryBuildingCatalog.Build(P);assert(cat.revision=='D0035-B164-2')
         n=addDistrict(c,42,'DISTRICT_NEIGHBORHOOD')
         setBuildings(d,{'BUILDING_LIBRARY'});setBuildings(n,{'BUILDING_HD_VILLA','BUILDING_HD_BUS_STOP','BUILDING_FOOD_MARKET'})
         d.workers=2
        ''')
        lua.execute(WRAPPER)
        lua.execute("wrap(c);include('CultureMeaningModel');include('CultureAestheticModel');include('ResearchApply');SPCResearchApply.Start(P,shared);ap=shared.ResearchApply;ap.ready=true")
        return lua

    def test_exact_reviewed_catalog_and_shared_depth(self):
        lua = self.runtime()
        lua.execute("for _,row in ipairs(reviewedTiers) do local b=cat.buildings[row.BuildingType];assert(b.ordinary and b.tier==row.Tier and b.reason=='ELIGIBLE') end;local v=verified();assert(neighborhood(v).value==6);for _,kind in ipairs({'BUILDING_HD_VILLA','BUILDING_HD_BUS_STOP','BUILDING_FOOD_MARKET'}) do local b=buildingFact(v,kind);assert(b.depthEligible and b.reason=='INCLUDED' and b.contribution==b.tier) end;assert(writes==0)")

    def test_meaning_real_depth_food_and_culture_quarantine(self):
        lua = self.runtime()
        lua.execute("g=addDistrict(c,50,'DISTRICT_GOVERNMENT');q=addDistrict(c,51,'DISTRICT_DIPLOMATIC_QUARTER');setBuildings(g,{'BUILDING_GOV_CULTURE'});setBuildings(q,{'BUILDING_CONSULATE','BUILDING_CHANCERY'});local v=verified();assert(v.value.domains.DISTRICT_GOVERNMENT.value==3 and v.value.domains.DISTRICT_DIPLOMATIC_QUARTER.value==3);local p=meaning(v);assert(#SPCCultureMeaningModel.Domains==7 and #SPCCultureMeaningModel.ActiveWriteYields==5);assert(p.each.FOOD==3 and p.total.FOOD==3 and p.each.CULTURE==0 and p.total.CULTURE==0);p=meaning(v,2);assert(p.total.FOOD==6 and p.each.FOOD==3 and p.total.CULTURE==0);assert(writes==0)")

    def test_research_apply_real_depth_writer_and_repeat(self):
        lua = self.runtime()
        lua.execute("local v=verified();local p=applyPlan(c,v);assert(p.per.FOOD==3 and p.total.FOOD==6);auditApply();assert(food(c)==3);local w,cap=writes,counters.dc_capture;auditApply();assert(writes==w and counters.dc_capture==cap);assert(w==2)")

    def test_building_pillage_repair_unfinished_and_free(self):
        lua = self.runtime()
        lua.execute("auditApply();n.bs[1].pillaged=true;fire('BuildingPillaged');local v=verified();assert(neighborhood(v).value==5 and buildingFact(v,'BUILDING_HD_VILLA').reason=='BUILDING_PILLAGED');auditApply();assert(food(c)==2);n.bs[1].pillaged=false;fire('BuildingRepaired');assert(neighborhood(verified()).value==6);auditApply();assert(food(c)==3);n.bs[1].complete=false;c.queued='BUILDING_HD_VILLA';svc.MarkDirty(0,1);v=verified();assert(neighborhood(v).value==5 and v.value.excluded[1].reason=='UNDER_CONSTRUCTION');c.queued=nil;n.bs[1].complete=true;n.bs[1].obtainedFree=true;svc.MarkDirty(0,1);assert(neighborhood(verified()).value==6)")

    def test_district_pillage_and_unfinished(self):
        for field in ['pillaged', 'complete']:
            with self.subTest(field=field):
                lua = self.runtime()
                fault, repair = ('true', 'false') if field == 'pillaged' else ('false', 'true')
                lua.execute(f"auditApply();n.{field}={fault};svc.MarkDirty(0,1);local v=verified();assert(neighborhood(v)==nil and meaning(v).each.FOOD==0);auditApply();assert(food(c)==0);n.{field}={repair};svc.MarkDirty(0,1);auditApply();assert(food(c)==3)")

    def test_same_tier_missing_lower_tiers_and_zero(self):
        lua = self.runtime()
        lua.execute("setBuildings(n,{'BUILDING_HD_VILLA','BUILDING_HD_MANSION'});local v=verified();assert(neighborhood(v).value==2 and meaning(v).each.FOOD==1);setBuildings(n,{'BUILDING_HD_BUS_STOP'});svc.MarkDirty(0,1);assert(neighborhood(verified()).value==2);setBuildings(n,{});svc.MarkDirty(0,1);v=verified();assert(neighborhood(v).value==0 and meaning(v).each.FOOD==0);assert(writes==0)")

    def test_cap_uses_adapter_tiers_without_normalization(self):
        lua = self.runtime()
        lua.execute("for _,kind in ipairs({'BUILDING_HD_VILLA','BUILDING_HD_BUS_STOP','BUILDING_FOOD_MARKET'}) do GameInfo.HD_BuildingTiers[kind].Tier=4 end;local v=verified();assert(neighborhood(v).value==10);local uncapped;for _,district in ipairs(v.value.districts) do if district.id==n.id then uncapped=district.uncapped end end;assert(uncapped==12 and meaning(v).each.FOOD==5);local p=applyPlan(c,v);assert(p.per.FOOD==5 and p.total.FOOD==10)")

    def test_highest_single_neighborhood_and_city_isolation(self):
        lua = self.runtime()
        lua.execute("n2=addDistrict(c,43,'DISTRICT_NEIGHBORHOOD');setBuildings(n2,{'BUILDING_HD_MANSION','BUILDING_SHOPPING_MALL'});local v=verified();assert(neighborhood(v).value==6 and neighborhood(v).districtID==n.id);other=newCity(2);other.active=4;od=addDistrict(other,22,'DISTRICT_CAMPUS');setBuildings(od,{'BUILDING_LIBRARY'});on=addDistrict(other,44,'DISTRICT_NEIGHBORHOOD');setBuildings(on,{'BUILDING_HD_MANSION'});wrap(other);local ov=verified(other);assert(neighborhood(ov).value==1 and meaning(ov).each.FOOD==0 and meaning(v).each.FOOD==3);auditApply();assert(food(c)==3 and food(other)==0);local cap,rev=counters.dc_capture,v.revision;svc.MarkDirty(0,2);assert(verified().revision==rev and counters.dc_capture==cap);verified(other);assert(counters.dc_capture==cap+1)")

    def test_internal_dummy_and_wonder_precede_allowlist(self):
        for kind in NEW_TARGETS:
            for predicate in ['internal', 'dummy', 'wonder']:
                with self.subTest(kind=kind, predicate=predicate):
                    lua = self.runtime()
                    if predicate == 'dummy':
                        lua.execute(f"GameInfo.HD_DUMMY_BUILDINGS=db({{{{BuildingType='{kind}'}}}},'BuildingType')")
                    else:
                        field = 'InternalOnly' if predicate == 'internal' else 'IsWonder'
                        lua.execute(f"GameInfo.Buildings.{kind}.{field}=true")
                    lua.execute(f"setBuildings(n,{{'{kind}'}});local b=SPCOrdinaryBuildingCatalog.Build(P).buildings.{kind};assert(not b.ordinary and b.reason=='{'WONDER' if predicate == 'wonder' else 'INTERNAL_OR_TECHNICAL'}');local v=verified();assert(not (buildingFact(v,'{kind}') or {{}}).ordinary);assert(writes==0)")

    def test_unknown_row_never_enrolled_by_tier(self):
        lua = self.runtime()
        lua.execute("local b=GameInfo.Buildings.BUILDING_UNKNOWN_MOD;b.PrereqDistrict='DISTRICT_NEIGHBORHOOD';tiers[#tiers+1]={BuildingType=b.BuildingType,PrereqDistrict='DISTRICT_NEIGHBORHOOD',Tier=4};GameInfo.HD_BuildingTiers=db(tiers,'BuildingType');setBuildings(n,{'BUILDING_UNKNOWN_MOD'});local v=verified();assert(neighborhood(v).value==0 and buildingFact(v,b.BuildingType).reason=='UNREVIEWED_BUILDING' and meaning(v).each.FOOD==0 and writes==0)")

    def test_unknown_invalid_tiers_refuse_meaning_and_apply(self):
        for kind in NEW_TARGETS:
            for bad, reason in [(None, 'TIER_UNKNOWN'), (9, 'TIER_UNSUPPORTED'), (0.5, 'TIER_UNSUPPORTED'), ('1', 'TIER_UNSUPPORTED')]:
                with self.subTest(kind=kind, bad=bad):
                    lua = self.runtime()
                    lua.globals().badTier = bad
                    lua.execute(f"setBuildings(n,{{'{kind}'}});GameInfo.HD_BuildingTiers.{kind}.Tier=badTier;local b=SPCOrdinaryBuildingCatalog.Build(P).buildings.{kind};assert(b.ordinary and b.tier==nil and b.reason=='{reason}');local v=verified();local ok,err=pcall(meaning,v);assert(not ok and tostring(err):find('ME_TIER_UNKNOWN'));ap.Audit({{player=0}});assert(ap.errors[0][1]:find('AP_BUILDING_FACT_UNKNOWN') and writes==0)")

    def test_zero_tier_keeps_ordinary_without_positive_depth(self):
        for kind in NEW_TARGETS:
            with self.subTest(kind=kind):
                lua = self.runtime()
                lua.execute(f"setBuildings(n,{{'{kind}'}});GameInfo.HD_BuildingTiers.{kind}.Tier=0;local v=verified();local b=buildingFact(v,'{kind}');assert(b.ordinary and b.tier==0 and b.contribution==0 and b.reason=='ORDINARY_TIER_ZERO');assert(neighborhood(v).value==0 and meaning(v).each.FOOD==0);auditApply();assert(food(c)==0 and writes==0)")

    def test_definition_and_tier_district_conflicts(self):
        for source in ['Buildings', 'HD_BuildingTiers']:
            with self.subTest(source=source):
                lua = self.runtime()
                lua.execute(f"GameInfo.{source}.BUILDING_HD_VILLA.PrereqDistrict='DISTRICT_CAMPUS';local b=SPCOrdinaryBuildingCatalog.Build(P).buildings.BUILDING_HD_VILLA;assert(b.reason=='{'DISTRICT_CLASSIFICATION_CONFLICT' if source == 'Buildings' else 'TIER_DISTRICT_CONFLICT'}' and b.tier==nil)")
                if source == 'HD_BuildingTiers':
                    lua.execute("local v=verified();local ok,err=pcall(meaning,v);assert(not ok and tostring(err):find('ME_TIER_UNKNOWN'));ap.Audit({player=0});assert(ap.errors[0][1]:find('AP_BUILDING_FACT_UNKNOWN') and writes==0)")
                else:
                    lua.execute("local v=verified();assert(neighborhood(v).value==5 and not buildingFact(v,'BUILDING_HD_VILLA').ordinary)")

    def test_reviewed_replacement_resolution_and_protections(self):
        cases = [
            ("GameInfo.HD_BuildingTiers.BUILDING_HD_VILLA.Tier=nil;replaces={{CivUniqueBuildingType='BUILDING_HD_VILLA',ReplacesBuildingType='BUILDING_HD_MANSION'}}", 'REPLACEMENT_TIER', 1),
            ("replaces={{CivUniqueBuildingType='BUILDING_HD_VILLA',ReplacesBuildingType='BUILDING_HD_BUS_STOP'}}", 'REPLACEMENT_TIER_CONFLICT', None),
            ("replaces={{CivUniqueBuildingType='BUILDING_HD_VILLA',ReplacesBuildingType='BUILDING_UNKNOWN_MOD'}}", 'REPLACEMENT_UNREVIEWED', None),
            ("replaces={{CivUniqueBuildingType='BUILDING_HD_VILLA',ReplacesBuildingType='BUILDING_HD_MANSION'},{CivUniqueBuildingType='BUILDING_HD_MANSION',ReplacesBuildingType='BUILDING_HD_VILLA'}}", 'REPLACEMENT_CYCLE', None),
        ]
        for setup, reason, tier in cases:
            with self.subTest(reason=reason):
                lua = self.runtime()
                lua.execute(setup + ";GameInfo.BuildingReplaces=db(replaces,'CivUniqueBuildingType');local b=SPCOrdinaryBuildingCatalog.Build(P).buildings.BUILDING_HD_VILLA;assert(b.ordinary)")
                lua.execute(f"local b=SPCOrdinaryBuildingCatalog.Build(P).buildings.BUILDING_HD_VILLA;assert(b.tier=={'nil' if tier is None else tier} and {'b.reason' if tier is None else 'b.tierSource'}=='{reason}')")
                if tier is None:
                    lua.execute("local v=verified();local ok,err=pcall(meaning,v);assert(not ok and tostring(err):find('ME_TIER_UNKNOWN'));ap.Audit({player=0});assert(ap.errors[0][1]:find('AP_BUILDING_FACT_UNKNOWN') and writes==0)")
                else:
                    lua.execute("assert(neighborhood(verified()).value==6)")

    def test_wrong_native_domain_contributes_zero_and_apply_holds(self):
        lua = self.runtime()
        lua.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_HD_VILLA'});setBuildings(n,{'BUILDING_HD_BUS_STOP','BUILDING_FOOD_MARKET'});local v=verified();local b=buildingFact(v,'BUILDING_HD_VILLA');assert(b.reason=='BUILDING_LOCATION_DOMAIN_CONFLICT' and b.contribution==0 and neighborhood(v).value==5);ap.Audit({player=0});assert(ap.errors[0][1]:find('AP_BUILDING_FACT_UNKNOWN') and writes==0)")

    def test_unavailable_locations_hold_reference_and_cached_value(self):
        for location in [-1, 9999]:
            with self.subTest(location=location):
                lua = self.runtime()
                lua.execute(f"auditApply();local before,cap=writes,counters.dc_capture;n.bs[1].location={location};svc.MarkDirty(0,1);local v=sample();assert(v.validity=='VERIFIED' and v.availability=='TEMPORARILY_UNAVAILABLE' and neighborhood(v).value==6);local ok,err=pcall(meaning,v);assert(not ok and tostring(err):find('ME_DEPTH_UNKNOWN'));ap.Audit({{player=0}});assert(writes==before and food(c)==3);cap=counters.dc_capture;sample();sample();assert(counters.dc_capture==cap);c.token='new-reference';v=sample();assert(v.validity=='UNKNOWN' and v.value==nil);n.bs[1].location=nil;svc.MarkDirty(0,1);assert(neighborhood(verified()).value==6)")

    def test_same_turn_event_update_confirmed_removal_and_clone(self):
        lua = self.runtime()
        lua.execute("local v=verified();local rev=v.revision;v.value.domains.DISTRICT_NEIGHBORHOOD.value=999;assert(neighborhood(verified()).value==6);setBuildings(n,{'BUILDING_HD_BUS_STOP','BUILDING_FOOD_MARKET'});fire('BuildingRemovedFromMap',0,0,GameInfo.Buildings.BUILDING_HD_VILLA.Index,0);v=verified();assert(neighborhood(v).value==5 and v.revision>rev and meaning(v).each.FOOD==2);local cap=counters.dc_capture;fire('GameCoreEventPublishComplete');fire('SystemUpdateUI');verified();assert(counters.dc_capture==cap)")

    def test_aesthetic_ordinary_count_remains_independent_of_tier(self):
        lua = self.runtime()
        lua.execute("setBuildings(n,{'BUILDING_HD_VILLA','BUILDING_HD_BUS_STOP','BUILDING_HD_MANSION','BUILDING_FOOD_MARKET'});GameInfo.HD_BuildingTiers.BUILDING_HD_VILLA.Tier=nil;local v=verified();local p=SPCCultureAestheticModel.Plan({validity='VERIFIED',identity='CULTURE',potential=3,active=3,activeStatus='KNOWN'},{hasConfirmed=true,availability='KNOWN',eraCount=2},v,true);assert(p.count==5 and p.total==10);local ok,err=pcall(meaning,v);assert(not ok and tostring(err):find('ME_TIER_UNKNOWN') and writes==0)")


if __name__ == '__main__':
    unittest.main(verbosity=2)
