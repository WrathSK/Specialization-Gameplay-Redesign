"""O1 Tier/D composition with the two fixed environment databases.

Requires SPC_OFFICIAL_DB and SPC_HD_DB (see test_environment_assembly).
SQL and the real Lua catalog, D producer and consumer projections run locally.
GameInfo and city observations are modeled; no native runtime claims.
"""
from contextlib import closing
from pathlib import Path
import sqlite3
import unittest

from lupa.lua51 import LuaRuntime

from test_environment_assembly import prepare_hd_inputs, replay, snapshot

MOD = Path(__file__).resolve().parents[1] / 'Mod'
TABLES = (
    'Buildings', 'Districts', 'DistrictReplaces', 'BuildingPrereqs', 'BuildingReplaces',
    'SPC_EnvironmentAssembly', 'SPC_EnvironmentBuildings', 'SPC_EnvironmentExcludedBuildings',
)
MODULES = (
    'OrdinaryBuildingCatalog', 'DistrictCompleteness', 'FactUse',
    'StandardizationCatalog', 'DevelopmentInvestmentCatalog', 'DevelopmentInvestmentTargets',
    'ResearchApplyModel', 'ResearchChairModel', 'CultureMeaningModel', 'ResearchInfrastructureShadow',
    'CommerceCalculation',
)


def game_rows(db, names=TABLES):
    db.row_factory = sqlite3.Row
    return {name: [dict(r) for r in db.execute(f'SELECT rowid AS "Index",* FROM "{name}"')]
            for name in names}


def lua_value(runtime, value):
    if isinstance(value, dict):
        return runtime.table_from({key: lua_value(runtime, item) for key, item in value.items()})
    if isinstance(value, list):
        return runtime.table_from([lua_value(runtime, item) for item in value])
    return value


def runtime(tables):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().rows = lua_value(lua, tables)
    lua.execute("""
P={Rows=function(name)return rows[name]end}
for _,b in ipairs(rows.Buildings)do b.InternalOnly=b.InternalOnly==1;b.IsWonder=b.IsWonder==1 end
function byType(kind)
 for _,b in ipairs(rows.Buildings)do if b.BuildingType==kind then return b end end
 error('Unknown fixture type '..kind)
end
function district(id,kind,types)
 local buildings={}
 for _,kind in ipairs(types)do
  buildings[#buildings+1]={index=byType(kind).Index,complete=true,pillaged=false}
 end
 return {id=id,type=kind,plot=id,complete=true,pillaged=false,buildings=buildings}
end
function verified(...)
 return {validity='VERIFIED',availability='READY',value=SPCDistrictCompleteness.Calculate(
  SPCOrdinaryBuildingCatalog.Read(P),{districts={...}},false)}
end
""")
    for name in MODULES:
        lua.execute((MOD / (name + '.lua')).read_text())
    return lua


class EffectiveBuildingTiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with closing(snapshot('SPC_OFFICIAL_DB')) as db:
            replay(db, hd=False)
            cls.official = game_rows(db)
        with closing(snapshot('SPC_HD_DB')) as db:
            prepare_hd_inputs(db)
            cls.hd = game_rows(db)
            cls.old = dict(db.execute('SELECT BuildingType,Tier FROM HD_BuildingTiers'))

    def test_fixed_environments_and_existing_building_admissions(self):
        for profile, fixture, count, expected_market in (
            ('OFFICIAL', self.official, 82, 1), ('HD', self.hd, 162, 2),
        ):
            with self.subTest(profile=profile):
                lua = runtime(fixture)
                lua.globals().count = count
                lua.globals().market = expected_market
                lua.execute("""
local cat=SPCOrdinaryBuildingCatalog.Read(P)
local std=SPCStandardizationCatalog.Build(P)
local dev=SPCDevelopmentInvestmentCatalog.Build(P)
assert(cat==SPCOrdinaryBuildingCatalog.Read(P)and std.count==count)
assert(std.buildings.BUILDING_MARKET.tier==market and dev.buildings.BUILDING_MARKET.tier==market)
assert(std.buildings.BUILDING_BANK.tier==market+1 and dev.buildings.BUILDING_STOCK_EXCHANGE.tier==market+2)
assert(std.buildings.BUILDING_PALACE.tier==0 and not std.buildings.BUILDING_PALACE.enabled)
assert(dev.buildings.BUILDING_PALACE.tier==0 and not cat.buildings.BUILDING_PALACE.ordinary)
assert(cat.buildings.BUILDING_SEWER.ordinary and not cat.buildings.BUILDING_SEWER.depthEligible)
assert(dev.buildings.BUILDING_WAT.tier==3 and std.buildings.BUILDING_WAT.tier==3)
assert(cat.buildings.BUILDING_MADRASA.tier==2)
assert(cat.buildings.BUILDING_GRAND_BAZAAR.tier==market+1
 and cat.buildings.BUILDING_GRAND_BAZAAR.tierSource=='REPLACEMENT_TIER')
""")
        lua = runtime(self.hd)
        found = lua.eval('SPCOrdinaryBuildingCatalog.Read(P).effectBuildings')
        self.assertEqual(set(found.keys()), {row['BuildingType'] for row in self.hd['SPC_EnvironmentBuildings']})
        self.assertEqual(
            {key: (self.old[key], row['tier']) for key, row in found.items() if self.old[key] != row['tier']},
            {'BUILDING_HD_DATA_CENTER': (4, 5)},
        )
        lua.execute("""
local c=SPCOrdinaryBuildingCatalog.Read(P)
for _,kind in ipairs({'BUILDING_JNR_LIGHTHOUSE_FISHING','BUILDING_JNR_FISH_MARKET','BUILDING_JNR_OFFSHORE_TERMINAL'})do
 assert(c.effectBuildings[kind].base=='DISTRICT_HARBOR' and not c.buildings[kind].ordinary)
end
assert(c.effectBuildings.BUILDING_IZ_WATER_MILL.tier==1)
assert(c.effectBuildings.BUILDING_HD_MANSION.tier==1)
assert(c.effectBuildings.BUILDING_JNR_HOSPITIUM.tier==4 and c.effectBuildings.BUILDING_JNR_GARDEN.tier==4)
""")

    def test_d_cap_and_consumer_roles(self):
        lua = runtime(self.hd)
        lua.execute("""
local hs='DISTRICT_HOLY_SITE'
local holy=district(1,hs,{'BUILDING_SHRINE','BUILDING_TEMPLE','BUILDING_JNR_DAOGUAN','BUILDING_JNR_HOSPITIUM'})
local v=verified(holy)
assert(SPCFactUse.Depth(v,hs).value==10)
holy.buildings[4].pillaged=true
assert(SPCFactUse.Depth(verified(holy),hs).value==6)
local campus=district(2,'DISTRICT_CAMPUS',{'BUILDING_LIBRARY','BUILDING_UNIVERSITY',
 'BUILDING_JNR_LABORATORY','BUILDING_RESEARCH_LAB','BUILDING_HD_DATA_CENTER'})
v=verified(holy,campus)
assert(v.value.districts[2].uncapped==15 and SPCFactUse.Depth(v,'DISTRICT_CAMPUS').value==10)
local f={validity='VERIFIED',identity='RESEARCH',potential=4,active=4,activeStatus='KNOWN',
 first={districtID=2,type='DISTRICT_CAMPUS'},workers=2}
local p=SPCResearchChairModel.Plan(f,v,2,{BUILDING_LIBRARY=true,BUILDING_UNIVERSITY=true,
 BUILDING_JNR_LABORATORY=true,BUILDING_RESEARCH_LAB=true,BUILDING_HD_DATA_CENTER=true})
assert(p.total==8 and p.count==4 and p.amounts.BUILDING_HD_DATA_CENTER==nil)
p=SPCResearchInfrastructureShadow.Plan(f,v)
assert(p.status=='READY' and p.d==10 and p.science==20)
local actual=SPCCommerceCalculation.Layout({hs},1,3,{[hs]=SPCFactUse.Depth(v,hs).value})
assert(actual[4].localD==6 and actual[4].effective)
""")

    def test_next_tier_uses_native_eligibility_and_keeps_the_lowest_price_rule(self):
        for fixture in (self.official, self.hd):
            lua = runtime(fixture)
            lua.execute("""
local first,second='BUILDING_MARKET','BUILDING_BANK'
local dev=SPCDevelopmentInvestmentCatalog.Build(P)
local std=SPCStandardizationCatalog.Build(P)
local domain='DISTRICT_COMMERCIAL_HUB'
local inputs={completeDomains={[domain]=true},buildings={}}
for _,b in ipairs(dev.domains[domain])do
 inputs.buildings[b.id]={present=false,constructible=b.id==first or b.id==second}
end
local target=SPCDevelopmentInvestmentTargets
local groups,_,_,ids=target.Candidates(dev,inputs)
assert(#ids==1 and ids[1]==first and groups[1].tier==std.buildings[first].tier)
local quote=target.Options(groups,ids,{prices={[first]={status='RETURNED',value=240}}})[1]
assert(quote.price==240 and quote.building==first)
inputs.buildings[first]={present=true}
groups,_,_,ids=target.Candidates(dev,inputs)
assert(#ids==1 and ids[1]==second and groups[1].tier==std.buildings[second].tier)
""")

    def test_missing_cycles_and_incompatible_alternatives_are_not_low_tiers(self):
        for extra, reason in (
            ("{Building='BUILDING_UNIVERSITY',PrereqBuilding='BUILDING_MISSING'}", 'TIER_PREREQUISITE_MISSING'),
            ("{Building='BUILDING_LIBRARY',PrereqBuilding='BUILDING_UNIVERSITY'}", 'TIER_CHAIN_CYCLE'),
            ("{Building='BUILDING_RESEARCH_LAB',PrereqBuilding='BUILDING_LIBRARY'}", 'TIER_PREREQUISITE_AMBIGUOUS'),
        ):
            with self.subTest(reason=reason):
                lua = runtime(self.official)
                lua.execute(f'table.insert(rows.BuildingPrereqs,{extra})')
                lua.globals().reason = reason
                lua.execute("""
local v=verified(district(1,'DISTRICT_CAMPUS',{'BUILDING_RESEARCH_LAB'}),
 district(2,'DISTRICT_HARBOR',{'BUILDING_LIGHTHOUSE'}),district(3,'DISTRICT_THEATER',{}))
assert(v.value.domains.DISTRICT_CAMPUS.depthError==reason)
assert(SPCFactUse.Depth(v,'DISTRICT_CAMPUS').status=='UNKNOWN')
assert(SPCFactUse.Depth(v,'DISTRICT_HARBOR').value==1)
assert(SPCFactUse.Depth(v,'DISTRICT_THEATER').value==0)
assert(SPCFactUse.Depth(v,'DISTRICT_HOLY_SITE').status=='NOT_APPLICABLE')
local f={validity='VERIFIED',identity='RESEARCH',potential=4,active=4,activeStatus='KNOWN',
 first={districtID=1,type='DISTRICT_CAMPUS'},workers=2}
assert(SPCResearchInfrastructureShadow.Plan(f,v).status=='HELD_COMPLETENESS')
f.identity='CULTURE'
local ok,message=pcall(SPCCultureMeaningModel.Plan,f,
 {hasConfirmed=true,availability='KNOWN',eraCount=2,count=2,modifierExcludedCount=0,unknownCategoryCount=0},v)
assert(not ok and tostring(message):find('ME_TIER_UNKNOWN'),message)
""")

    def test_missing_assembly_does_not_fall_back_to_hd_tables(self):
        lua = runtime(self.hd)
        lua.execute("""
rows.SPC_EnvironmentAssembly={}
rows.HD_BuildingTiers={{BuildingType='BUILDING_LIBRARY',Tier=1}}
local ok,err=pcall(SPCOrdinaryBuildingCatalog.Read,P)
assert(not ok and tostring(err):find('BUILDING_CATALOG_ASSEMBLY_UNAVAILABLE'))
""")


if __name__ == '__main__':
    unittest.main()
