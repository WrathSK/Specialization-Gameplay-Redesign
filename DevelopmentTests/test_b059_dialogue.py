from pathlib import Path
import sqlite3,json,zlib,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
p=json.loads((R/'local/config.json').read_text())['debug_gameplay_db'];src=sqlite3.connect('file:'+p+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');src.backup(db);src.close();db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
for table,col in [('BuildingModifiers','ModifierId'),('ModifierArguments','ModifierId'),('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]:db.execute(f"delete from {table} where {col} like 'SPC_B059_%' or {col} like 'BUILDING_SPC_B059_%'")
db.execute('drop table if exists SPC_DialogueLevels');db.executescript((M/'Data/Dialogue.sql').read_text())
neras=db.execute('select count(*) from Eras').fetchone()[0]
assert db.execute('select count(*) from SPC_DialogueLevels').fetchone()[0]==neras-1
for n in range(2,neras+1):
 rows=db.execute("select a.Value from BuildingModifiers b join ModifierArguments a using(ModifierId) where b.BuildingType=? and a.Name='ScalingFactor'",('BUILDING_SPC_B059_D'+str(n),)).fetchall()
 assert len(rows)==14 and all(int(x[0])==100+25*(n-1) for x in rows)
assert not db.execute("select 1 from ModifierArguments where ModifierId like 'SPC_B059_%' and Value in ('GREATWORKOBJECT_RELIC','GREATWORKOBJECT_PRODUCT')").fetchall()
assert not db.execute("select 1 from Modifiers m left join DynamicModifiers d using(ModifierType) where m.ModifierId like 'SPC_B059_%' and d.ModifierType is null").fetchall()
root=ET.parse(M/'SpecializationP0.modinfo').getroot();assert root.get('version')=='77'
for el in root.findall('.//File'):assert (M/el.text).is_file(),el.text
l=LuaRuntime(unpack_returned_tuples=True);check=l.eval('function(s) local f,e=load(s);assert(f,e) end')
for f in ['Dialogue.lua','DialogueModel.lua','UI/DialogueRefresh.lua','Gameplay.lua','UI/P0Panel.lua','UI/BoostGreatWorkRead.lua']:check((M/f).read_text())
l.execute("""
function iter(rows) return function() local i=0;return function() i=i+1;return rows[i] end end end
include=function() end;Locale={Lookup=function(n) return n end};turn=1
Game={GetCurrentGameTurn=function() return turn end,GetLocalPlayer=function() return 0 end}
local eras={};for i=1,9 do eras[i]={EraType='E'..i} end
GameInfo={Eras=iter(eras)}
works={A={GreatWorkType='A',Name='A',GreatWorkObjectType='GREATWORKOBJECT_WRITING',GreatPersonIndividualType='GA',EraType='E8'},B={GreatWorkType='B',Name='B',GreatWorkObjectType='GREATWORKOBJECT_MUSIC',GreatPersonIndividualType='GB',EraType='E7'},C={GreatWorkType='C',Name='C',GreatWorkObjectType='GREATWORKOBJECT_ARTIFACT',EraType='E1'},R={GreatWorkType='R',GreatWorkObjectType='GREATWORKOBJECT_RELIC'},X={GreatWorkType='X',GreatWorkObjectType='GREATWORKOBJECT_PRODUCT'}}
gps={GA={EraType='E1'},GB={EraType='E2'}}
for i=3,9 do gps['G'..i]={EraType='E'..i};works['W'..i]={GreatWorkType='W'..i,Name='W'..i,GreatWorkObjectType='GREATWORKOBJECT_WRITING',GreatPersonIndividualType='G'..i} end
P={VERSION='P0-B-059.77',IsTestPlayer=function(pid) return pid==0 end,Field=function(t,k) return t and t[k] end,Info=function(t,k)
 if t=='GreatWorks' then return works[k] end
 if t=='GreatPersonIndividuals' then return gps[k] end
 if t=='Eras' then for _,e in ipairs(eras) do if e.EraType==k then return e end end end
 if t=='Buildings' then return {Index=k} end
end}
Events={}
function city(id)
 local c={id=id,owner=0,active=4,kind='CULTURE',b={},writes=0,slots={}}
 function c:GetID() return self.id end;function c:GetOwner() return self.owner end
 function c:GetBuildings() return {HasBuilding=function(_,i) return self.b[i]==true end,RemoveBuilding=function(_,i) self.b[i]=nil;self.writes=self.writes+1 end} end
 function c:GetBuildQueue() return {CreateBuilding=function(_,i) self.b[i]=true;self.writes=self.writes+1 end} end
 return c
end
c1=city(1);c2=city(2);cities={c1,c2}
local col={Members=function() local i=0;return function() i=i+1;if cities[i] then return i,cities[i] end end end,FindID=function(_,id) for _,c in ipairs(cities) do if c.id==id and c.owner==0 then return c end end end}
Players={[0]={GetCities=function() return col end}}
shared={Version=P.VERSION,EffectiveFacts={Read=function(pid,c) return {active=c.active,specialization=c.kind} end}}
ExposedMembers={SPC_P0=shared};SPCP0=P
""")
l.execute((M/'DialogueModel.lua').read_text());l.execute((M/'Dialogue.lua').read_text())
l.execute("""
local m=SPCDialogueModel
local p=m.Plan(P,{{id=1,type='A'},{id=2,type='B'},{id=3,type='C'},{id=4,type='X'},{id=5,type='R'}})
assert(p.d==2 and p.count==3 and p.excluded==2 and p.percent==25 and p.eras.E1 and not p.eras.E8)
assert(m.Plan(P,{}).percent==0)
local all={{id=1,type='A'},{id=2,type='B'}};for i=3,9 do all[#all+1]={id=i,type='W'..i} end
assert(m.Plan(P,all).percent==200) -- no D7 cap
assert(not pcall(m.Plan,P,{{id=1,type='A'},{id=1,type='B'}}))
SPCDialogue.Start(P,shared);local d=shared.Dialogue
function send(data,valid) sequence=(sequence or 0)+1;d.Receive(0,{Generation=d.generation,Seq=sequence,Valid=valid or 1,Turn=turn,Data=data,Count=select(2,data:gsub(';',''))+1}) end
send('1,-1,EMPTY;1,10,A;1,11,B;2,-1,EMPTY')
assert(c1.b.BUILDING_SPC_B059_D2 and not c2.b.BUILDING_SPC_B059_D2 and d.last[0][1].applied==25)
local n=c1.writes;send('1,-1,EMPTY;1,10,A;1,11,B;2,-1,EMPTY');assert(c1.writes==n)
c1.active=3;d.Audit(0);assert(not c1.b.BUILDING_SPC_B059_D2)
c1.active=4;d.Audit(0);assert(c1.b.BUILDING_SPC_B059_D2)
d.off[0]=true;d.Audit(0);assert(not c1.b.BUILDING_SPC_B059_D2);d.off[0]=false;d.Audit(0);assert(c1.b.BUILDING_SPC_B059_D2)
send('1,-1,EMPTY;1,10,A;2,-1,EMPTY;2,11,B');assert(not c1.b.BUILDING_SPC_B059_D2) -- highest era moved
send('1,-1,EMPTY;1,10,A;1,11,B;2,-1,EMPTY');send('1,-1,EMPTY;1,10,A;1,11,B;2,-1,EMPTY;2,11,B');assert(not c1.b.BUILDING_SPC_B059_D2 and d.errors[0])
send('1,-1,EMPTY;1,10,A;1,11,B;2,-1,EMPTY');turn=2;d.Audit(0);assert(not c1.b.BUILDING_SPC_B059_D2)
send('1,-1,EMPTY;1,10,A;1,11,B;2,-1,EMPTY');c1.kind='RESEARCH';d.Audit(0);assert(not c1.b.BUILDING_SPC_B059_D2)
c1.kind='CULTURE';d.Audit(0)
c1.b.BUILDING_SPC_B059_D9=true;SPCDialogue.Start(P,shared);d=shared.Dialogue;d.Init();assert(not c1.b.BUILDING_SPC_B059_D9 and not c1.b.BUILDING_SPC_B059_D2)
-- Background executes without any panel opening and detects active-level change in signature.
GameInfo.Buildings=iter({{Index='SLOT'}})
c1.b.SLOT=true;c1.slots={10,11};c2.slots={}
for _,c in ipairs(cities) do local old=c.GetBuildings;c.GetBuildings=function(self)
 local b=old(self);b.GetNumGreatWorkSlots=function() return #self.slots end;b.GetGreatWorkInSlot=function(_,i,s) return self.slots[s+1] end;b.GetGreatWorkTypeFromIndex=function(_,id) return id==10 and 'A' or 'B' end;return b
end end
ContextPtr={SetInitHandler=function(_,f) init=f end,SetUpdate=function(_,f) update=f end,SetShutdown=function() end,ClearUpdate=function() end}
PlayerOperations={EXECUTE_SCRIPT=1};requests=0
UI={RequestPlayerOperation=function(pid,op,a) requests=requests+1;shared.Dialogue.Receive(pid,a) end}
""")
l.execute((M/'UI/DialogueRefresh.lua').read_text());l.execute("init();assert(c1.b.BUILDING_SPC_B059_D2);local n=requests;update(2);assert(requests==n);c1.active=3;update(2);assert(not c1.b.BUILDING_SPC_B059_D2 and requests==n+1)")
# Frozen B058 suite only changes manifest expectation; it retains old planner as archival fixture.
s=(R/'DevelopmentTests/test_b058_boost_gw_basis.py').read_text().replace("'76'","'77'")
exec(compile(s,str(R/'DevelopmentTests/test_b058_boost_gw_basis.py'),'exec'))
print('B059 LOCAL_SIMULATION_PASS: SQL 14 modifiers per D, creator/artifact era union, no D7 cap, background init/no-panel/idempotence/governor/move/off/reload/stale/duplicate guards; regression pass.')
