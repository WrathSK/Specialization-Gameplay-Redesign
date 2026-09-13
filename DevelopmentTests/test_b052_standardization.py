"""B052 real catalog/ledger Lua with native-event mocks; DB read-only, no game launch."""
from pathlib import Path
import os,sqlite3,hashlib,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from project_paths import external_database
r=Path(os.environ.get('SPC_TEST_MOD_DIR',Path(__file__).resolve().parents[1]/'Mod'))
l=LuaRuntime(unpack_returned_tuples=True)
def table(rows): return l.table_from([l.table_from(dict(x)) for x in rows])
with sqlite3.connect(external_database(Path(__file__).resolve().parents[1]).as_uri()+'?mode=ro',uri=True) as db:
 db.row_factory=sqlite3.Row
 buildings=list(db.execute('SELECT rowid AS "Index", * FROM Buildings'))
 tiers=list(db.execute('SELECT * FROM HD_BuildingTiers'))
 dummy=list(db.execute('SELECT * FROM HD_DUMMY_BUILDINGS'))
l.globals().dbBuildings=table(buildings);l.globals().dbTiers=table(tiers);l.globals().dbDummy=table(dummy)
l.execute('''
function iterator(rows) return function() local i=0;return function() i=i+1;return rows[i] end end end
GameInfo={HD_BuildingTiers=iterator(dbTiers),HD_DUMMY_BUILDINGS=iterator(dbDummy)}
rows={};for _,r in ipairs(dbBuildings) do rows[r.BuildingType]=r;rows[r.Index]=r end
P={Field=function(t,k) return t and t[k] end,Info=function(t,k) return rows[k] end,IsTestPlayer=function(p) return p==0 end}
turn=10;Game={GetCurrentGameTurn=function() return turn end};Locale={Lookup=function(n) return n end}
function copy(t) if type(t)~='table' then return t end;local r={};for k,v in pairs(t) do r[k]=copy(v) end;return r end
function reset()
 hooks={};local function events() return setmetatable({},{__index=function(t,k)
 local e={Add=function(f) hooks[k]=hooks[k] or {};table.insert(hooks[k],f) end};rawset(t,k,e);return e end}) end
 Events=events();GameEvents=events()
 shared={EffectiveFacts={Read=function(pid,c) assert(not c.unready,'UNREADY');return {token=c.token,specialization=c.kind} end}}
end
function fire(n,...) for _,f in ipairs(hooks[n] or {}) do f(...) end end
cities={};writes=0;checks=0
function city(id,kind)
 local c={id=id,kind=kind,token='foundation:'..id,owner=0,properties={},owned={}};cities[id]=c
 c.GetOwner=function() return c.owner end;c.GetID=function() return id end;c.GetX=function() return id*3 end;c.GetY=function() return 7 end;c.GetName=function() return 'City '..id end
 c.GetProperty=function(_,k) return copy(c.properties[k]) end
 c.SetProperty=function(_,k,v) c.properties[k]=copy(v);writes=writes+1 end
 c.GetBuildings=function() return {HasBuilding=function(_,index) checks=checks+1;return c.owned[index]==true end} end
 return c
end
Players={[0]={GetCities=function() return {Members=function() return ipairs(cities) end,FindID=function(_,id) return cities[id] end} end}}
function own(c,id) c.owned[rows[id].Index]=true end
function has(c,id) local v=c.properties[SPCStandardization.KEY];return v and v.learned[id]~=nil end
reset()
''')
l.execute((r/'StandardizationCatalog.lua').read_text());l.execute((r/'Standardization.lua').read_text())
l.execute('''
cat=SPCStandardizationCatalog.Build(P);assert(cat.count==167,cat.count)
assert(cat.buildings.BUILDING_MONUMENT.group==cat.buildings.BUILDING_GRANARY.group)
assert(cat.buildings.BUILDING_EXHIBITION.group~=cat.buildings.BUILDING_HD_POLICE_STATION.group)
assert(cat.buildings.BUILDING_EXHIBITION.enabled and cat.buildings.BUILDING_HD_POLICE_STATION.enabled)
assert(cat.buildings.BUILDING_NILOMETER_HD.enabled)
assert(not cat.buildings.BUILDING_PALGUM.enabled)
for id,row in pairs(cat.buildings) do
 assert(not (rows[id].IsWonder==1 or rows[id].InternalOnly==1))
 if row.district=='DISTRICT_GOVERNMENT' then assert(not row.enabled) end
 if rows[id].TraitType and row.district~='DISTRICT_CITY_CENTER' and row.district~='DISTRICT_GOVERNMENT' then assert(row.enabled) end
end
c1=city(1,'INDUSTRY');c2=city(2,'RESEARCH')
own(c1,'BUILDING_MONUMENT');own(c1,'BUILDING_WALLS');own(c2,'BUILDING_GRANARY')
SPCStandardization.Start(P,shared);d=shared.Standardization
assert(d.Describe(0,c1,1):find('尚无账本'));assert(writes==0 and checks==0)
fire('LoadScreenClose');assert(has(c1,'BUILDING_MONUMENT') and has(c1,'BUILDING_WALLS'))
assert(not c2.properties[SPCStandardization.KEY] and d.scans==1 and d.writes==1)
local n=checks;fire('PlayerTurnActivated',0);d.Describe(0,c1,1);d.Describe(0,c1,2);assert(checks==n and d.writes==1)
-- Exact city events, duplicate notification, Gold/free acquisition all test same physical fact.
own(c1,'BUILDING_GRANARY');fire('BuildingConstructed',0,1,rows.BUILDING_GRANARY.Index)
assert(has(c1,'BUILDING_GRANARY') and d.writes==2)
fire('OnBuildingConstructed',0,1,rows.BUILDING_GRANARY.Index);assert(d.writes==2)
-- AddedToMap is x,y,buildingIndex,owner, not owner,city,index.
own(c1,'BUILDING_WATER_MILL');fire('BuildingAddedToMap',3,7,rows.BUILDING_WATER_MILL.Index,0)
assert(has(c1,'BUILDING_WATER_MILL') and not has(c2,'BUILDING_WATER_MILL'))
fire('BuildingConstructed',0,1,rows.BUILDING_LIBRARY.Index)
for i=1,8 do fire('GameCoreEventPublishComplete') end
assert(not has(c1,'BUILDING_LIBRARY'))
own(c1,'BUILDING_LIBRARY');fire('GameCoreEventPublishComplete');assert(has(c1,'BUILDING_LIBRARY'))
-- Government and Faith catalog entries must also persist; classification does not unlock them.
for id,row in pairs(cat.buildings) do if row.district=='DISTRICT_GOVERNMENT' or row.purchaseYield=='YIELD_FAITH' then
 own(c1,id);fire('BuildingConstructed',0,1,rows[id].Index);assert(has(c1,id)) end end
c1.owned[rows.BUILDING_LIBRARY.Index]=nil;fire('PlayerTurnActivated',0);assert(has(c1,'BUILDING_LIBRARY'))
-- First becoming Industry backfills once, regardless ACTIVE (mock only contains identity).
c2.kind='INDUSTRY';fire('OnDistrictConstructed',0);assert(has(c2,'BUILDING_GRANARY') and d.scans==2)
local saved=copy(c1.properties);local oldwrites=writes
reset();SPCStandardization.Start(P,shared);d=shared.Standardization
local n=checks;fire('LoadScreenClose');assert(d.scans==0 and writes==oldwrites and checks==n)
assert(c1.properties[SPCStandardization.KEY].revision==saved[SPCStandardization.KEY].revision)
-- A changed owner foundation cannot append to or erase an existing ledger.
c1.token='new-owner-foundation';own(c1,'BUILDING_UNIVERSITY')
fire('BuildingConstructed',0,1,rows.BUILDING_UNIVERSITY.Index)
assert(not has(c1,'BUILDING_UNIVERSITY') and has(c1,'BUILDING_LIBRARY'))
assert(d.errors['0:1']=='STD_FOUNDATION_CHANGED');c1.token='foundation:1'
-- Corruption and changed HD classification fail closed, without rewriting receipts.
local v=c1.properties[SPCStandardization.KEY];v.revision=v.revision+1
local before=writes;fire('PlayerTurnActivated',0);assert(d.errors['0:1']=='STD_REVISION_CONFLICT' and writes==before)
c1.properties=copy(saved)
d.catalog.buildings.BUILDING_LIBRARY.tier=999
assert(d.Describe(0,c1,1):find('STD_CATALOG_MIGRATION_REQUIRED') and writes==before)
-- Missing tables never produce an empty initialized ledger. Recovery on later discovery works.
reset();c3=city(3,'INDUSTRY');GameInfo.HD_BuildingTiers=nil
SPCStandardization.Start(P,shared);d=shared.Standardization;fire('LoadScreenClose')
assert(c3.properties[SPCStandardization.KEY]==nil)
GameInfo.HD_BuildingTiers=iterator(dbTiers);fire('PlayerTurnActivated',0)
assert(c3.properties[SPCStandardization.KEY] and next(c3.properties[SPCStandardization.KEY].learned)==nil)
-- UI read leaves snapshots and counters untouched.
local n=writes;local b=checks;d.Describe(0,c1,1);d.Describe(0,c1,2);assert(writes==n and checks==b)
''')
for p in r.rglob('*.lua'):
 result=l.eval('load')(p.read_text(),str(p))
 assert not isinstance(result,tuple),(p,result)
manifest=ET.parse(r/'SpecializationP0.modinfo').getroot();assert manifest.get('version')=='68'
for name in ['Standardization.lua','StandardizationCatalog.lua']:
 assert any(e.text==name for e in manifest.findall('.//ImportFiles/File'))
 assert any(e.text==name for e in manifest.findall('./Files/File'))
for p in r.rglob('*.xml'): ET.parse(p)
panel=ET.parse(r/'UI/P0Panel.xml').getroot().find('./Container')
buttons=[x for x in panel.findall('./GridButton') if x.get('Hidden')!='1']
positions=[(x.get('Anchor'),x.get('Offset')) for x in buttons]
assert len(positions)==len(set(positions)), 'Visible action buttons overlap'
assert len(buttons)<=15
for name in ['Standardization.lua','StandardizationCatalog.lua']:
 source=(r/name).read_text();assert 'CreateBuilding(' not in source and 'AttachModifier' not in source
print('LOCAL_SIMULATION_PASS B052: 167-row real DB catalog; scope separation; one-time backfill; completion/AddedToMap adapters; delayed acquisition; duplicate/read/reload no writes; retained removed/disabled/Faith/unique templates; foundation/corruption/classification guards; Lua/XML manifest. Native event coverage USER_GAME_TEST_REQUIRED.')
