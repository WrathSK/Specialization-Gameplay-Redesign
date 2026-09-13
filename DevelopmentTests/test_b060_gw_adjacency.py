from pathlib import Path
from lupa.lua55 import LuaRuntime
import sqlite3,json,zlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];M=R/'Mod'
# Preserve preceding suite, adapting only the current manifest version.
s=(R/'DevelopmentTests/test_b059_baseline_read.py').read_text().replace('"78","83"','"78","84"')
exec(compile(s,str(R/'DevelopmentTests/test_b059_baseline_read.py'),'exec'))
src=sqlite3.connect('file:'+json.loads((R/'local/config.json').read_text())['debug_gameplay_db']+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');src.backup(db);src.close();db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
for table,col in [('BuildingModifiers','ModifierId'),('ModifierArguments','ModifierId'),('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]: db.execute(f"delete from {table} where {col} like 'SPC_B060_%' or {col} like 'BUILDING_SPC_B060_%'")
db.executescript((M/'Data/GreatWorkAdjacency.sql').read_text())
assert db.execute("select count(*) from Buildings where BuildingType like 'BUILDING_SPC_B060_%'").fetchone()[0]==156
assert db.execute("select count(*) from Modifiers where ModifierId like 'SPC_B060_%'").fetchone()[0]==1092
assert db.execute("select Value from ModifierArguments where ModifierId='SPC_B060_SCIENCE_P0_WRITING' and Name='YieldChange'").fetchone()[0]=='0.5'
assert not db.execute("select 1 from ModifierArguments where ModifierId like 'SPC_B060_%' and Value in ('GREATWORKOBJECT_RELIC','GREATWORKOBJECT_PRODUCT')").fetchall()
l=LuaRuntime(unpack_returned_tuples=True)
for f in ['GreatWorkAdjacency.lua','GreatWorkAdjacencyModel.lua','UI/DialogueRefresh.lua','UI/P0Panel.lua','UI/BoostGreatWorkRead.lua','Gameplay.lua']: l.eval('function(s) assert(load(s)) end')((M/f).read_text())
l.execute("""
include=function() end;turn=1;kind='CULTURE';active=4;writes=0
function iter(rows) return function() local i=0;return function() i=i+1;if rows[i] then return i,rows[i] end end end end
Game={GetCurrentGameTurn=function() return turn end}
local ids={FOOD=1,PRODUCTION=2,GOLD=3,SCIENCE=4,CULTURE=5,FAITH=6}
P={IsTestPlayer=function(pid) return pid==0 end,Info=function(t,k)
 if t=='Buildings' then return {Index=k} end
 if t=='Yields' then return {Index=ids[k:gsub('YIELD_','')]} end
 if t=='Districts' then return {DistrictType=k,RequiresPopulation=k~='DISTRICT_AQUEDUCT'} end
 if t=='GreatWorks' then return {GreatWorkObjectType=k} end
end}
b={};city={GetID=function() return 1 end,GetOwner=function() return 0 end,GetBuildings=function() return {
 HasBuilding=function(_,id) return b[id]==true end,RemoveBuilding=function(_,id) b[id]=nil;writes=writes+1 end} end,
 GetBuildQueue=function() return {CreateBuilding=function(_,id) b[id]=true;writes=writes+1 end} end}
function district(id,kind,done)
 return {GetID=function() return id end,GetCity=function() return city end,GetType=function() return kind end,IsComplete=function() return done end,GetX=function() return id end,GetY=function() return 0 end}
end
all={district(10,'DISTRICT_CAMPUS',true),district(11,'DISTRICT_THEATER',true),district(12,'DISTRICT_AQUEDUCT',true),district(13,'DISTRICT_HARBOR',false),district(14,'DISTRICT_HANSA',true)}
Players={[0]={GetCities=function() return {Members=iter({city})} end,GetDistricts=function() return {Members=iter(all)} end}}
base={[10]={[4]=3},[11]={[5]=2},[14]={[2]=4}}
Map={GetPlot=function(x,y) return {GetAdjacencyYield=function(_,pid,cid,typ,yi) return (base[x] or {})[yi] or 0 end,GetYield=function() error('actual must never be queried') end} end}
works={{type='GREATWORKOBJECT_WRITING'},{type='GREATWORKOBJECT_ARTIFACT'},{type='GREATWORKOBJECT_RELIC'},{type='GREATWORKOBJECT_PRODUCT'}}
shared={Dialogue={samples={[0]={turn=1,cities={[1]=works}}}},EffectiveFacts={Read=function() return {specialization=kind,active=active} end}}
""")
l.execute((M/'GreatWorkAdjacencyModel.lua').read_text());l.execute((M/'GreatWorkAdjacency.lua').read_text())
l.execute("""
SPCGWAdjacency.Start(P,shared);local d=shared.GreatWorkAdjacency;local m=SPCGWAdjacencyModel
local payload,n=m.Collect(P,0);assert(n==3 and payload:find('DISTRICT_THEATER') and payload:find('DISTRICT_HANSA') and not payload:find('AQUEDUCT'))
local a={Valid=1,Turn=1,AdjData=payload,AdjCount=n};d.Receive(0,a)
assert(d.last[0][1].count==2 and d.last[0][1].base.SCIENCE==3)
-- Base3 -> per-work1.5, not count2 * 1.5 passed per-work.
assert(b.BUILDING_SPC_B060_SCIENCE_P0 and b.BUILDING_SPC_B060_SCIENCE_P1 and not b.BUILDING_SPC_B060_SCIENCE_P2)
assert(b.BUILDING_SPC_B060_CULTURE_P1 and b.BUILDING_SPC_B060_PRODUCTION_P2)
local before=writes;d.Receive(0,a);assert(writes==before)
active=3;d.Audit(0);for _,v in pairs(b) do assert(not v) end
active=4;d.Audit(0);assert(b.BUILDING_SPC_B060_SCIENCE_P0)
d.off[0]=true;d.Audit(0);assert(not b.BUILDING_SPC_B060_SCIENCE_P0);d.off[0]=false;d.Audit(0)
shared.Dialogue.samples[0].cities[1]={};d.Audit(0);assert(not b.BUILDING_SPC_B060_SCIENCE_P0)
shared.Dialogue.samples[0].cities[1]=works
-- Changed/partial endpoint snapshot clears applied derived yields.
d.Receive(0,{Valid=1,Turn=1,AdjData='1,99,DISTRICT_CAMPUS,0,0,0,3,0,0',AdjCount=1});assert(d.errors[0] and not b.BUILDING_SPC_B060_SCIENCE_P0)
d.Receive(0,a);assert(b.BUILDING_SPC_B060_SCIENCE_P0)
turn=2;d.Audit(0);assert(not b.BUILDING_SPC_B060_SCIENCE_P0)
turn=1;d.Receive(0,a);SPCGWAdjacency.Start(P,shared);shared.GreatWorkAdjacency.Init();assert(not b.BUILDING_SPC_B060_SCIENCE_P0)
assert(not pcall(m.Parts,.5)) -- unsupported quarter-per-work reports, never floors silently
for v=-8191,8191 do local total=0;for _,part in ipairs(m.Parts(v)) do total=total+(part:sub(1,1)=='N' and -1 or 1)*2^tonumber(part:sub(2))/2 end;assert(total==v/2) end
""")
ui=(M/'UI/DialogueRefresh.lua').read_text();assert 'AdjData=adjData' in ui and 'pcall(SPCGWAdjacencyModel.Collect,P,pid)' in ui
assert 'GreatWorkAdjacency.Receive(pid,a)' in (M/'Dialogue.lua').read_text()
print('B060.84 LOCAL_SIMULATION_PASS: six-yield BASE-only complete specialty/unique collection; native half SQL; per-work not count squared; bit precision; idempotence; ACTIVE/OFF/no-works/removal/stale/load cleanup. Native half/multiplier behavior USER_GAME_TEST_REQUIRED.')

l.execute("""
-- Wire-level sample through actual new UI collector. Adjacency failure cannot invalidate works.
P.VERSION='test';P.Field=function(t,k) return t and t[k] end;SPCP0=P
shared.Version='test';shared.Dialogue.ready=true;shared.Dialogue.seq={};shared.Dialogue.generation=1
ExposedMembers={SPC_P0=shared};Game.GetLocalPlayer=function() return 0 end
SPCDialogueModel={Collect=function() return {{id=10,type='GREATWORK_WRITING'}} end}
Events=setmetatable({}, {__index=function(t,k) local e={list={}};e.Add=function(f) e.list[#e.list+1]=f end;rawset(t,k,e);return e end})
function fire(k) for _,f in ipairs(Events[k].list) do f() end end
ContextPtr={SetInitHandler=function(_,f) init=f end,SetShutdown=function() end};PlayerOperations={EXECUTE_SCRIPT=1}
UI={RequestPlayerOperation=function(pid,op,a) packet=a;shared.Dialogue.seq[pid]=a.Seq;return true end}
""")
l.execute((M/'UI/DialogueRefresh.lua').read_text())
l.execute("""
init();assert(packet.Valid==1 and packet.AdjCount==3 and packet.AdjData:find('DISTRICT_HANSA'))
Map.GetPlot=function() error('injected base read failure') end
fire('ImprovementAddedToMap');fire('GameCoreEventPlaybackComplete')
assert(packet.Valid==1 and packet.Data:find('GREATWORK_WRITING') and packet.AdjCount==-1)
""")
print('B060.84 LOCAL_SIMULATION_PASS: actual UI payload carries six BASE yields; failed adjacency collection isolated from Dialogue works.')
