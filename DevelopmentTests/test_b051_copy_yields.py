"""B051 real Lua + background UI mock and read-only DB -> memory checks; no game launch."""
from pathlib import Path
import sqlite3,zlib,xml.etree.ElementTree as E
from project_paths import external_database
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Mod"
l=LuaRuntime(unpack_returned_tuples=True)
l.execute((r/'CopyYields.lua').read_text())
l.execute('''
for pop=1,255 do for _,n in ipairs({0,0.5,1,1.5,3.5,999.5,65535.5}) do
 local p=SPCCopyYields.Plan(n,pop);assert(p.integer+pop*p.coefficient==n)
end end
assert(not pcall(SPCCopyYields.Plan,0.25,3));assert(not pcall(SPCCopyYields.Plan,0.5,256))
turn=1;enabled=true;network=true;recipients={2,3};hooks={};rows={};districts={};cities={};facts={};changes=0;requests=0
for _,y in ipairs({'SCIENCE','PRODUCTION'}) do for _,mode in ipairs({'POS','NEG','POP'}) do for bit=0,(mode=='POP' and 7 or 15) do
 local key='BUILDING_SPC_B051_'..y..'_'..mode..'_'..bit
 rows[key]={Index=key,y=y,mode=mode,amount=mode=='POP' and 1/2^(bit+1) or (mode=='NEG' and -2^bit or 2^bit)}
end end end
function amount(c,y) local n=0;for id in pairs(c.stored) do local v=rows[id];if v.y==y then n=n+v.amount*(v.mode=='POP' and c.pop or 1) end end;return n end
for id=1,3 do local c={id=id,pop=3,stored={},owner=0};cities[id]=c
 c.GetID=function() return c.id end;c.GetOwner=function() return c.owner end;c.GetPopulation=function() return c.pop end
 c.GetProperty=function() return nil end;c.GetYield=function(_,y) return 10+amount(c,y) end
 c.GetBuildings=function() return {HasBuilding=function(_,i) return c.stored[i]==true end,RemoveBuilding=function(_,i) c.stored[i]=nil;changes=changes+1 end} end
 c.GetBuildQueue=function() return {CreateBuilding=function(_,i) c.stored[i]=true;changes=changes+1 end} end
end
function district(id,cid,kind,prod,culture)
 local d={id=id,cid=cid,kind=kind,prod=prod,culture=culture or 0,complete=true}
 d.GetID=function() return d.id end;d.GetType=function() return d.kind end;d.GetCity=function() return cities[d.cid] end
 d.IsComplete=function() return d.complete end;d.GetYield=function(_,y) return y=='PRODUCTION' and d.prod or (y=='CULTURE' and d.culture or 0) end
 districts[#districts+1]=d;return d
end
campus=district(1,1,'DISTRICT_CAMPUS',100) -- must never enter research copy
localiz=district(2,1,'DISTRICT_INDUSTRIAL_ZONE',7,2) -- cross-yield actual 9 vs hypothetical base 6
source2=district(3,2,'DISTRICT_INDUSTRIAL_ZONE',7)
source3=district(4,3,'DISTRICT_INDUSTRIAL_ZONE',11)
facts[1]={specialization='RESEARCH',active=4,first={districtID=1,type='DISTRICT_CAMPUS'}}
facts[2]={specialization='INDUSTRY',active=4,first={districtID=3,type='DISTRICT_INDUSTRIAL_ZONE'}}
facts[3]={specialization='INDUSTRY',active=4,first={districtID=4,type='DISTRICT_INDUSTRIAL_ZONE'}}
Players={[0]={GetCities=function() return {Members=function() return ipairs(cities) end,FindID=function(_,id) return cities[id] end} end,
 GetDistricts=function() return {Members=function() return ipairs(districts) end} end}}
P={VERSION='P0-B-051',Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY',DISTRICT_THEATER='CULTURE',DISTRICT_COMMERCIAL_HUB='COMMERCE'},
 IsTestPlayer=function() return enabled end,Field=function(t,k) return t[k] end,
 Info=function(t,k) if t=='Buildings' then return rows[k] elseif t=='Yields' then return {Index=k:gsub('YIELD_','')} else return {DistrictType=k,RequiresPopulation=true} end end}
Events=setmetatable({},{__index=function(t,k) local e={Add=function(f) hooks[k]=hooks[k] or {};table.insert(hooks[k],f) end};rawset(t,k,e);return e end})
function fire(n) for _,f in ipairs(hooks[n] or {}) do f() end end
Game={GetCurrentGameTurn=function() return turn end,GetLocalPlayer=function() return 0 end}
shared={Version=P.VERSION,EffectiveFacts={Read=function(_,c) return facts[c.id] end},NetworkBridge={RecipientSources=function(_,c)
 assert(network,'NETWORK_REFRESH_PENDING');return c.id==1 and recipients or {} end}}
SPCCopyYields.Start(P,shared)
SPCP0=P;ExposedMembers={SPC_P0=shared};include=function() end;PlayerOperations={EXECUTE_SCRIPT=1}
UI={RequestPlayerOperation=function(pid,op,p) requests=requests+1;if drop then drop=false;return end;shared.CopyYields.Receive(pid,p) end}
ContextPtr={SetInitHandler=function(_,f) init=f end,SetUpdate=function(_,f) update=f end,SetShutdown=function() end,ClearUpdate=function() end}
''')
l.execute((r/'UI/CopyYieldRefresh.lua').read_text())
l.execute('''
init();update(1);assert(requests==0) -- no sample before gameplay readiness
fire('LoadScreenClose');update(1)
assert(amount(cities[1],'SCIENCE')==4.5 and amount(cities[1],'PRODUCTION')==5.5)
local n=changes;local q=requests
for i=1,5 do update(1);shared.CopyYields.Audit();shared.CopyYields.Describe(0,cities[1]) end
assert(changes==n and requests==q) -- no duplication, no panel-driven refresh
facts[3].active=3;fire('GovernorPromoted');assert(amount(cities[1],'PRODUCTION')==3.5)
recipients={};shared.CopyYields.Audit();assert(amount(cities[1],'PRODUCTION')==0)
recipients={2,3};facts[3].active=4;shared.CopyYields.Audit();assert(amount(cities[1],'PRODUCTION')==5.5)
network=false;shared.CopyYields.Audit();assert(amount(cities[1],'PRODUCTION')==0 and amount(cities[1],'SCIENCE')==4.5)
network=true;shared.CopyYields.Audit();assert(amount(cities[1],'PRODUCTION')==5.5)
-- policy/non-adjacency changes come from actual district source, not city copy totals
source3.prod=13;localiz.prod=13;update(1)
assert(amount(cities[1],'PRODUCTION')==6.5 and amount(cities[1],'SCIENCE')==7.5)
for _,p in ipairs({4,7,128,255,3}) do cities[1].pop=p;fire('CityPopulationChanged');assert(amount(cities[1],'SCIENCE')==7.5 and amount(cities[1],'PRODUCTION')==6.5) end
facts[1].active=3;fire('GovernorAssigned');assert(amount(cities[1],'SCIENCE')==0)
facts[1].active=4;fire('GovernorEstablished');assert(amount(cities[1],'SCIENCE')==7.5)
-- same-context load reset forces resend even same turn/payload; cache replaced
shared.CopyYields.samples[0].rows['1:2'].total=999
fire('LoadScreenClose');assert(amount(cities[1],'SCIENCE')==0);update(1);assert(amount(cities[1],'SCIENCE')==7.5)
-- dropped request is retried via sequence acknowledgement
localiz.prod=15;drop=true;update(1);assert(amount(cities[1],'SCIENCE')==7.5);update(1);assert(amount(cities[1],'SCIENCE')==8.5)
-- finer than half target is reported and cleared, never rounded
localiz.prod=15.5;update(1);assert(amount(cities[1],'SCIENCE')==0)
assert(shared.CopyYields.errors['0:1:SCIENCE']:find('PRECISION_UNSUPPORTED'))
localiz.prod=15;update(1);assert(amount(cities[1],'SCIENCE')==8.5)
local n=changes;shared.CopyYields.Receive(0,{Seq=999,Generation=-1});assert(changes==n)
-- incomplete source endpoint removal invalidates full sample and never keeps old output
source3.complete=false;facts[3].active=3;fire('DistrictRemovedFromMap');assert(amount(cities[1],'PRODUCTION')==0)
update(1);assert(amount(cities[1],'PRODUCTION')==3.5)
-- unknown specialty district is an explicit scope limitation, not partial research grant
unknown=district(9,1,'DISTRICT_UNKNOWN',1);update(1);assert(amount(cities[1],'SCIENCE')==0)
assert(shared.CopyYields.errors['0:1:SCIENCE']:find('SCOPE_UNRESOLVED'))
unknown.complete=false;update(1);assert(amount(cities[1],'SCIENCE')==8.5)
-- dormant cleanup is lifecycle-only; periodic audit skips disabled player
n=changes;enabled=false;shared.CopyYields.Audit();assert(changes==n)
fire('CityTransfered');assert(amount(cities[1],'SCIENCE')==0 and amount(cities[1],'PRODUCTION')==0)
''')
db=sqlite3.connect(external_database(w).as_uri()+'?mode=ro',uri=True)
m=sqlite3.connect(':memory:');db.backup(m);db.close();m.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
m.executescript((r/'Data/CopyYields.sql').read_text())
assert m.execute("select count(*) from Buildings where BuildingType GLOB 'BUILDING_SPC_B051_*'").fetchone()[0]==80
assert m.execute("select count(*) from TraitModifiers where ModifierId GLOB 'SPC_B051_*'").fetchone()[0]==0
assert m.execute("select count(*) from BuildingModifiers where BuildingType GLOB 'BUILDING_SPC_B051_*'").fetchone()[0]==80
assert m.execute("select count(*) from Building_YieldChanges where BuildingType GLOB 'BUILDING_SPC_B051_*'").fetchone()[0]==0
for y in ['SCIENCE','PRODUCTION']:
 for mode in ['POS','NEG','POP']:
  for bit in range(8 if mode=='POP' else 16):
   mid=f'SPC_B051_{y}_{mode}_{bit}'
   val=m.execute("select Value from ModifierArguments where ModifierId=? and Name='Amount'",(mid,)).fetchone()[0]
   assert float(val)==(1/2**(bit+1) if mode=='POP' else (-1 if mode=='NEG' else 1)*2**bit)
for mt in ['MODIFIER_SINGLE_CITY_ADJUST_YIELD_CHANGE','MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_PER_POPULATION']:
 assert m.execute('select CollectionType from DynamicModifiers where ModifierType=?',(mt,)).fetchone()[0]=='COLLECTION_OWNER'
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
for p in r.rglob('*.xml'):E.parse(p)
root=E.parse(r/'SpecializationP0.modinfo').getroot();assert root.get('version')=='65';assert root.get('id')=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for f in root.findall('.//File'):assert (r/f.text).is_file(),f.text
b=w/'DevelopmentTests/Fixtures/B051-before-copy'
for name in ['InvestmentAction.lua','UnitActions.lua','NetworkBridge.lua','Lv4Percent.lua','CrewProjects.lua','Data/CrewProjects.sql','HalfYieldProbe.lua']:
 assert (r/name).read_bytes()==(b/name).read_bytes(),name
print('LOCAL_SIMULATION_PASS B051: actual Lua/background bridge, half plans 255 populations, automatic apply/remove/max fallback, stale/partial/unknown scope, reload/resend/drop recovery, repeat/read idempotence; SQL 80 carriers; Lua/XML/manifest; protected mechanics unchanged. Native integration USER_GAME_TEST_REQUIRED.')
