"""B058 actual Lua automatic integer consumer + D0020 pure per-work planner."""
from pathlib import Path
import math,runpy,sqlite3,json,zlib
R=Path(__file__).resolve().parents[1]
g=runpy.run_path(str(R/'tools/generate_boost_integer.py'))
for name,text in g['render']().items():assert (R/name).read_text()==text
s=(R/'DevelopmentTests/test_b055_boost_gw.py').read_text()
for old,new in [("[0]=='4.5'","[0]=='4.0'"),('2.2*math.sqrt(8)','2*math.sqrt(8)'),("get('version')=='72'","get('version')=='76'"),('4.5*math.sqrt(2)','6'),('RESEARCH.amount==2.2','RESEARCH.amount==2'),("['BoostConfig.lua','NetworkBridge.lua'","['BoostConfig.lua','BoostIntegerConfig.lua','NetworkBridge.lua'")]:
 assert s.count(old)==1,old;s=s.replace(old,new)
s=s.replace("lua.execute((M/'UI/BoostGreatWorkRead.lua').read_text())","lua.execute((M/'UI/GreatWorkBasis.lua').read_text());lua.execute((M/'UI/BoostGreatWorkRead.lua').read_text())")
s=s.replace("u.execute((M/'UI/BoostGreatWorkRead.lua').read_text())","u.execute((M/'UI/GreatWorkBasis.lua').read_text());u.execute((M/'UI/BoostGreatWorkRead.lua').read_text())")
exec(compile(s,str(R/'DevelopmentTests/test_b055_boost_gw.py'),'exec'))
lua.execute("""
Game.GetCurrentGameTurn=function() return 1 end;cities[1].owner=0;capital=cities[2];capital.active=1;routes={};receive()
local d=shared.NetworkBoost
assert(d.plans[0].RESEARCH.amount==1 and d.plans[0].RESEARCH.raw==1)
local writes=capital.writes
routes={{2,5,123}};receive()
assert(d.plans[0].RESEARCH.n==2 and d.plans[0].RESEARCH.amount==1 and capital.writes==writes)
capital.active=4;receive();assert(d.plans[0].RESEARCH.amount==6)
assert(math.abs(d.plans[0].RESEARCH.raw-4*math.sqrt(2))<1e-10)
for _,r in pairs(SPCBoostConfig.rows) do assert(not capital:GetBuildings():HasBuilding(P.Info('Buildings',r.building).Index)) end
writes=capital.writes;d.Audit();receive();assert(capital.writes==writes)
local old=SPCBoostIntegerConfig.rows['RESEARCH:6'];capital.active=1;d.Audit();assert(not capital:GetBuildings():HasBuilding(P.Info('Buildings',old).Index))
local k=SPCBoostConfig.k.RESEARCH;SPCBoostConfig.k.RESEARCH=100;d.Audit();assert(d.applied[0].RESEARCH==nil and d.errors[0]:find('B058_INTEGER_CATALOG_LIMIT'));SPCBoostConfig.k.RESEARCH=k
-- Rebuild persisted integer state, clear an intentionally incorrect carrier.
capital:GetBuildQueue():CreateBuilding(P.Info('Buildings',SPCBoostIntegerConfig.rows['RESEARCH:45']).Index)
SPCNetworkBoost.Start(P,shared);d=shared.NetworkBoost;d.EnsureReady(0)
assert(not capital:GetBuildings():HasBuilding(P.Info('Buildings',SPCBoostIntegerConfig.rows['RESEARCH:45']).Index))
local basis=SPCGreatWorkBasis
local a={id=1,name='A',object='GREATWORKOBJECT_WRITING',culture=12,faith=0,tourism=2}
local b={id=2,name='B',object='GREATWORKOBJECT_ARTIFACT',culture=2,faith=0,tourism=18}
local r={id=3,name='Relic',object='GREATWORKOBJECT_RELIC',culture=0,faith=4,tourism=8}
local r2={id=4,name='Relic2',object='GREATWORKOBJECT_RELIC',culture=0,faith=6,tourism=4}
local product={id=5,object='GREATWORKOBJECT_PRODUCT',culture=999,faith=999,tourism=999}
local p=basis.Plan({a,b,r,r2,product})
assert(p.groups.CULTURE.first==12 and p.groups.CULTURE.tourism==18 and p.groups.CULTURE.totalFirst==10 and p.groups.CULTURE.totalTourism==16)
assert(p.groups.RELIC.count==0 and p.groups.RELIC.totalFirst==0 and p.groups.RELIC.totalTourism==0 and p.excluded==3)
assert(a.culture==12 and b.culture==2) -- plans never write back to base values
assert(basis.Plan({b,r,product}).groups.CULTURE.totalFirst==0) -- high source moved away
assert(basis.Plan({}).groups.CULTURE.count==0)
assert(not pcall(basis.Plan,{a,a}))
-- Collector reads DB bases, not building yield totals (which include buffs).
local function iter(rows) return function() local i=0;return function() i=i+1;return rows[i] end end end
GameInfo.GreatWork_YieldChanges=iter({{GreatWorkType='A',YieldType='YIELD_CULTURE',YieldChange=2}})
GameInfo.Buildings=iter({{Index=1}})
local fakeP={Info=function() return {GreatWorkType='A',Name='A',GreatWorkObjectType='GREATWORKOBJECT_WRITING',Tourism=2} end}
Locale={Lookup=function(x) return x end}
local slots={GetNumGreatWorkSlots=function() return 1 end,HasBuilding=function() return true end,GetGreatWorkInSlot=function() return 12 end,GetGreatWorkTypeFromIndex=function() return 1 end,GetBuildingYieldFromGreatWorks=function() error('must not read final yield') end}
local c={GetBuildings=function() return slots end};assert(basis.Collect(fakeP,c)[1].culture==2)
""")
p=json.loads((R/'local/config.json').read_text())['debug_gameplay_db'];src=sqlite3.connect('file:'+p+'?mode=ro',uri=True);c=sqlite3.connect(':memory:');src.backup(c);src.close();c.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
for table,col in [('BuildingModifiers','ModifierId'),('ModifierArguments','ModifierId'),('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]:c.execute(f"delete from {table} where {col} like 'SPC_B058_%' or {col} like 'BUILDING_SPC_B058_%'")
c.executescript((R/'Mod/Data/NetworkBoostInteger.sql').read_text())
assert c.execute("select count(*) from Buildings where BuildingType like 'BUILDING_SPC_B058_%'").fetchone()[0]==90
for kind in ['RESEARCH','CULTURE']:
 for amount in range(1,46):assert c.execute("select Value from ModifierArguments where ModifierId=? and Name='Amount'",(f'SPC_B058_{kind}_{amount}',)).fetchone()[0]==str(amount)
s=(R/'DevelopmentTests/test_b055_regression.py').read_text().replace("'72'","'76'");exec(compile(s,str(R/'DevelopmentTests/test_b055_regression.py'),'exec'))
print('B058 LOCAL_SIMULATION_PASS: automatic terminal quantization, integer identity reuse, legacy cleanup, full regressions; D0020 independent maxima/base-only read/group isolation/no feedback.')
