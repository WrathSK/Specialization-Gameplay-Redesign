from pathlib import Path
import sqlite3,zlib,xml.etree.ElementTree as E,hashlib
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True);l.execute((r/'HalfYieldProbe.lua').read_text())
l.execute('''
for pop=1,255 do local p=SPCHalfYieldProbe.Plan(pop);assert(pop*p.coefficient-p.subtract==0.5) end
assert(not pcall(SPCHalfYieldProbe.Plan,0));assert(not pcall(SPCHalfYieldProbe.Plan,256))
pop=3;stored={};enabled=nil;changes=0;hooks={};rows={};idx=0
for _,y in ipairs({'SCIENCE','PRODUCTION'}) do for _,mode in ipairs({'POP','SUB'}) do for bit=0,7 do
 idx=idx+1;rows['BUILDING_SPC_B050_'..y..'_'..mode..'_'..bit]={Index=idx,y=y,mode=mode,amount=mode=='POP' and 1/2^(bit+1) or -2^bit}
end end end
function amount(y) local n=0;for _,v in pairs(rows) do if stored[v.Index] and v.y==y then n=n+v.amount*(v.mode=='POP' and pop or 1) end end;return n end
city={GetOwner=function() return 0 end,GetID=function() return 1 end,GetPopulation=function() return pop end,
GetProperty=function() return enabled end,SetProperty=function(_,_,v) enabled=v end,
GetYield=function(_,y) return 10+amount(y) end,
GetBuildings=function() return {HasBuilding=function(_,i) return stored[i]==true end,RemoveBuilding=function(_,i) stored[i]=nil;changes=changes+1 end} end,
GetBuildQueue=function() return {CreateBuilding=function(_,i) stored[i]=true;changes=changes+1 end} end}
Players={[0]={GetCities=function() return {Members=function() return ipairs({city}) end} end}}
P={IsTestPlayer=function() return true end,Field=function(t,k) return t[k] end,Info=function(t,k) if t=='Buildings' then return rows[k] end;return {Index=k:gsub('YIELD_','')} end}
Events=setmetatable({},{__index=function(t,k) return {Add=function(f) hooks[k]=f end} end});shared={}
SPCHalfYieldProbe.Start(P,shared);local d=shared.HalfYieldProbe
hooks.LoadScreenClose();assert(changes==0)
d.Run(0,city,'HALF_ON');assert(amount('SCIENCE')==0.5 and amount('PRODUCTION')==0.5)
local n=changes;d.Run(0,city,'HALF_ON');d.Run(0,city,'HALF_READ');assert(changes==n)
for _,p in ipairs({4,2,7,128,255,1}) do pop=p;hooks.CityPopulationChanged();assert(amount('SCIENCE')==0.5 and amount('PRODUCTION')==0.5) end
SPCHalfYieldProbe.Start(P,shared);d=shared.HalfYieldProbe;n=changes;hooks.LoadScreenClose();assert(changes==n)
d.Run(0,city,'HALF_OFF');assert(not enabled and amount('SCIENCE')==0 and amount('PRODUCTION')==0)
n=changes;d.Run(0,city,'HALF_OFF');assert(changes==n)
''')
l.execute('Ledger=assert(load(...))()', (w/'DevelopmentTests/StandardizationLedger.lua').read_text())
l.execute('''
catalog={revision='HD_SAMPLE_1',buildings={A={district='CAMPUS',tier=1},B={district='CAMPUS',tier=1},C={district='THEATER',tier=1},D={district='CAMPUS',tier=2},H={district='CAMPUS',tier=1,internal=true}}}
local e={authorized=true,completed=true,evidence='completion:1',turn=5,buildingType='A'}
local one,changed=Ledger.Record(nil,'city-a',e,catalog);assert(changed and one.revision==1)
local same,again=Ledger.Record(one,'city-a',e,catalog);assert(not again and same.revision==1 and one.revision==1)
assert(not pcall(Ledger.Record,one,'other-city',e,catalog))
e.authorized=false;assert(not pcall(Ledger.Record,nil,'city-z',e,catalog));e.authorized=true
local empty={schema=1,cityUID='city-b',catalogRevision=catalog.revision,revision=0,learned={}}
local sources={['city-a']={owner=0,kind='INDUSTRY',active=1},['city-b']={owner=0,kind='INDUSTRY',active=4}}
local ledgers={['city-a']=one,['city-b']=empty};local result=Ledger.ForRecipient(0,sources,ledgers,catalog)
assert(Ledger.Discount(result,'B','GOLD',catalog)==40) -- template and discount from different cities
assert(Ledger.Discount(result,'B','FAITH',catalog)==0 and Ledger.Discount(result,'C','GOLD',catalog)==0 and Ledger.Discount(result,'D','GOLD',catalog)==0)
sources['city-a']=nil;assert(Ledger.Discount(Ledger.ForRecipient(0,sources,ledgers,catalog),'B','GOLD',catalog)==0)
assert(one.learned.A) -- disconnect never deletes permanent knowledge
sources={['city-a']={owner=1,kind='INDUSTRY',active=2}}
assert(Ledger.Discount(Ledger.ForRecipient(1,sources,ledgers,catalog),'B','GOLD',catalog)==20)
assert(not pcall(Ledger.ForRecipient,0,sources,ledgers,catalog))
''')
db=sqlite3.connect((w/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True);m=sqlite3.connect(':memory:');db.backup(m);db.close();m.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()));m.executescript((r/'Data/HalfYieldProbe.sql').read_text())
assert m.execute("select count(*) from Buildings where BuildingType GLOB 'BUILDING_SPC_B050_*'").fetchone()[0]==32
for row in m.execute("select Value from ModifierArguments where ModifierId GLOB 'SPC_B050_*_POP_*' and Name='Amount'"):assert 0<float(row[0])<=0.5
assert m.execute("select count(*) from TraitModifiers where ModifierId GLOB 'SPC_B050_*'").fetchone()[0]==0
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
for p in r.rglob('*.xml'):E.parse(p)
root=E.parse(r/'SpecializationP0.modinfo').getroot();assert root.get('version')=='64'
for f in root.findall('.//File'):assert (r/f.text).is_file()
b=w/'DevelopmentBackups/Specialization-before-B050-half-standardization/RuntimeSnapshot'
for name in ['InvestmentAction.lua','UnitActions.lua','NetworkBridge.lua','Lv4CopyRead.lua','Lv4Percent.lua','CrewProjects.lua','Data/CrewProjects.sql']:assert (r/name).read_bytes()==(b/name).read_bytes()
print('LOCAL_SIMULATION_PASS B050: exact half plan all 255 populations; real module ON/repeat/read/population/reload/OFF; SQL/Lua/XML; offline ledger idempotence, city inheritance, same district+tier, union/max cross-source, Gold-only query. Native fractional effect NOT verified.')
