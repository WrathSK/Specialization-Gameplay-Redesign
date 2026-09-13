"""Real catalog, ledger, discount and background Lua; native permissions are explicit mocks."""
from pathlib import Path
import os,sqlite3,zlib,xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
from project_paths import external_database
root=Path(__file__).resolve().parents[1];r=Path(os.environ.get('SPC_TEST_MOD_DIR',root/'Mod'))
db=sqlite3.connect(external_database(root).as_uri()+'?mode=ro',uri=True);m=sqlite3.connect(':memory:');db.backup(m);db.close();m.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
# The live read-only DB may already contain a deployed B054. Reset this prefix in memory only.
for table,col in [('BuildingModifiers','BuildingType'),('ModifierArguments','ModifierId'),('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]:
 m.execute(f'DELETE FROM {table} WHERE {col} LIKE ?',('BUILDING_SPC_B054_%',))
m.execute('DROP TABLE IF EXISTS SPC_B054_Targets')
m.executescript((r/'Data/StandardizationDiscount.sql').read_text());m.row_factory=sqlite3.Row
l=LuaRuntime(unpack_returned_tuples=True)
for name,sql in [('dbBuildings','select rowid as "Index",* from Buildings'),('dbTiers','select * from HD_BuildingTiers'),('dbDummy','select * from HD_DUMMY_BUILDINGS')]:l.globals()[name]=l.table_from([l.table_from(dict(x)) for x in m.execute(sql)])
assert m.execute("select count(*) from ModifierArguments where ModifierId like 'BUILDING_SPC_B054_%' and Name not in ('BuildingType','Amount')").fetchone()[0]==0
assert m.execute("select count(*) from Modifiers m join DynamicModifiers d using(ModifierType) where m.ModifierId like 'BUILDING_SPC_B054_%' and d.EffectType!='EFFECT_ADJUST_BUILDING_PURCHASE_COST'").fetchone()[0]==0
l.execute('''
function iter(rows) return function() local i=0;return function() i=i+1;return rows[i] end end end
GameInfo={HD_BuildingTiers=iter(dbTiers),HD_DUMMY_BUILDINGS=iter(dbDummy)}
rows={};byHash={};for _,b in ipairs(dbBuildings) do rows[b.BuildingType]=b;rows[b.Index]=b;b.Hash=b.Index;byHash[b.Hash]=b end
P={VERSION='P0-B-054',Field=function(t,k) return t and t[k] end,Info=function(t,k) if t=='Yields' then return {Index=1} end;return rows[k] end,IsTestPlayer=function(p) return p==0 end};SPCP0=P
turn=1;Game={GetCurrentGameTurn=function() return turn end,GetLocalPlayer=function() return 0 end};Locale={Lookup=function(n) return n end}
hooks={};function evs() return setmetatable({},{__index=function(t,k) local e={Add=function(f) hooks[k]=hooks[k] or {};table.insert(hooks[k],f) end};rawset(t,k,e);return e end}) end
Events=evs();GameEvents=evs();function fire(n,...) for _,f in ipairs(hooks[n] or {}) do f(...) end end
function clone(t) if type(t)~='table' then return t end;local r={};for k,v in pairs(t) do r[k]=clone(v) end;return r end
cities={};writes=0;propertyWrites=0;facts={};receivers={};allowed={}
function city(id,kind,level)
 local c={id=id,owner=0,props={},built={}};cities[id]=c
 facts[id]={specialization=kind,active=level,token='foundation:'..id,potential=level}
 c.GetID=function() return id end;c.GetName=function() return 'City '..id end;c.GetOwner=function() return c.owner end;c.GetX=function() return id end;c.GetY=function() return 7 end
 c.GetProperty=function(_,k) return clone(c.props[k]) end;c.SetProperty=function(_,k,v) c.props[k]=clone(v);propertyWrites=propertyWrites+1 end
 c.GetBuildings=function() return {HasBuilding=function(_,i) return c.built[i]==true end,RemoveBuilding=function(_,i) c.built[i]=nil;writes=writes+1 end} end
 c.GetBuildQueue=function() return {CreateBuilding=function(_,i) c.built[i]=true;writes=writes+1 end} end
 return c
end
c1=city(1,'INDUSTRY',1);c2=city(2,'INDUSTRY',4);c3=city(3,'CULTURE',1)
c1.built[rows.BUILDING_MONUMENT.Index]=true
receivers[3]={1,2};allowed[3]={BUILDING_MONUMENT=true,BUILDING_GRANARY=true}
Players={[0]={GetCities=function() return {Members=function() return ipairs(cities) end,FindID=function(_,id) return cities[id] end} end}}
shared={Version=P.VERSION,EffectiveFacts={Read=function(pid,c) assert(c.owner==pid,'OWNER');return facts[c.id] end},NetworkBridge={RecipientSources=function(pid,c,k) assert(k=='INDUSTRY');return receivers[c.id] or {} end}}
ExposedMembers={SPC_P0=shared}
''')
for f in ['StandardizationCatalog.lua','Standardization.lua','StandardizationDiscount.lua']:l.execute((r/f).read_text())
l.execute('''
SPCStandardization.Start(P,shared);SPCStandardizationDiscount.Start(P,shared);d=shared.StandardizationDiscount
function rate(c,id)
 local total=0;for level=1,4 do if c.built[rows['BUILDING_SPC_B054_'..id..'_'..level].Index] then total=total+level*10 end end;return total
end
ContextPtr={SetInitHandler=function(_,f) initUI=f end,SetShutdown=function(_,f) end};include=function() end
CityCommandTypes={PARAM_BUILDING_TYPE=1,PARAM_YIELD_TYPE=2,PURCHASE=3}
CityManager={CanStartCommand=function(c,cmd,visibility,args,results)
 assert(cmd==3 and visibility==false and results==true and args[2]==1)
 return (allowed[c.id] or {})[byHash[args[1]].BuildingType]==true
end}
PlayerOperations={EXECUTE_SCRIPT=1};sends=0
UI={RequestPlayerOperation=function(pid,op,p) sends=sends+1;if p.Action=='DISCOUNT_INIT' then d.EnsureReady(pid);return end;lastRequest=clone(p);d.Receive(pid,p) end}
''')
l.execute((r/'UI/DiscountEligibility.lua').read_text())
l.execute('''
-- Simulate missing one-shot LoadScreenClose: normal established ledger/network exist.
shared.Standardization.ready=true;shared.Standardization.Discover()
initUI();fire('SystemUpdateUI');fire('GameCoreEventPublishComplete')
assert(d.ready and d.generation==1)
local gen=d.generation;d.EnsureReady(0);assert(d.generation==gen)

assert(rate(c3,'BUILDING_GRANARY')==40 and rate(c3,'BUILDING_MONUMENT')==40)
assert(rate(c3,'BUILDING_NILOMETER_HD')==0) -- same group, but native Gold permission false
local n=writes;local p=propertyWrites;fire('GameCoreEventPublishComplete');d.Describe(0,c3,1);assert(writes==n and propertyWrites==p)
-- Max level supplier need not supply the template. Remove the only template source.
receivers[3]={2};fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==0)
assert(c1.props.SPC_STANDARDIZATION_LEDGER_V1.learned.BUILDING_MONUMENT)
receivers[3]={1,2};facts[2].active=2;fire('GovernorPromoted');fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==20)
receivers[3]={1};fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==10)
local stale=clone(lastRequest)
-- Lost recipient role and unknown source: revoke, no permanent fact changes.
receivers[3]={};fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==0)
stale.Seq=d.seq[0]+1;d.Receive(0,stale);assert(rate(c3,'BUILDING_GRANARY')==0)
receivers[3]={1};fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==10)
facts[1].active=nil;fire('GovernorChanged');assert(rate(c3,'BUILDING_GRANARY')==0)
facts[1].active=1;fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==10)
-- Native permission revoked (prerequisite/religion/unique etc): no residual Faith discount.
allowed[3].BUILDING_GRANARY=false;fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==0)
allowed[3].BUILDING_GRANARY=true;turn=2;fire('PlayerTurnActivated',0);fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==10)
-- Incomplete eligibility payload is not a partial fact.
local bad=clone(lastRequest);bad.Seq=d.seq[0]+1;bad.Data='';bad.Count=0;d.Receive(0,bad);assert(rate(c3,'BUILDING_GRANARY')==0)
fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==10)
-- Reload clears samples, reconstructs from source ledgers and background, no UI panel calls.
local p=propertyWrites;fire('LoadScreenClose');fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==10 and propertyWrites==p)
-- Different district/tier and disabled city-center entries do not join BASIC.
local targets=d.plans[0].targets[3];assert(not targets.BUILDING_LIBRARY and not targets.BUILDING_WALLS and not targets.BUILDING_EXHIBITION)
-- Source owner mismatch removes benefits; old templates are retained.
c1.owner=1;fire('GameCoreEventPublishComplete');assert(rate(c3,'BUILDING_GRANARY')==0)
assert(c1.props.SPC_STANDARDIZATION_LEDGER_V1.learned.BUILDING_MONUMENT)
''')
cat=l.eval('SPCStandardizationCatalog.Build(P)');enabled=sum(1 for _,b in cat['buildings'].items() if b['enabled'])
assert m.execute('select count(*) from SPC_B054_Targets').fetchone()[0]==enabled*4
for p in r.rglob('*.lua'):
 result=l.eval('load')(p.read_text(),str(p));assert not isinstance(result,tuple),(p,result)
for p in r.rglob('*.xml'):E.parse(p)
assert E.parse(r/'SpecializationP0.modinfo').getroot().get('version')=='71'
window=E.parse(r/'UI/P0Panel.xml').getroot().find('./Container');buttons=[x for x in window.findall('./GridButton') if x.get('Hidden')!='1'];pos=[(x.get('Anchor'),x.get('Offset')) for x in buttons];assert len(pos)==len(set(pos)) and len(pos)<=15
print('LOCAL_SIMULATION_PASS B054 real Lua end-to-end background: independent template/max sources; union/group/scope; idempotence; downgrade/disconnect; permission loss; stale/partial rejection; reload; retained facts. SQL carriers:',enabled*4,'. Actual engine purchase permissions/prices remain USER_GAME_TEST_REQUIRED.')
