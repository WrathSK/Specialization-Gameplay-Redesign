"""B057 boundary quantization and explicit-integer native carrier contract; no game pass."""
from pathlib import Path
import math,sqlite3,json,zlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b055_boost_gw.py').read_text()
for old,new in [("[0]=='4.5'","[0]=='4.0'"),('2.2*math.sqrt(8)','2*math.sqrt(8)'),("get('version')=='72'","get('version')=='74'"),('4.5*math.sqrt(2)','4*math.sqrt(2)'),('RESEARCH.amount==2.2','RESEARCH.amount==2')]:
 assert s.count(old)==1,old
 s=s.replace(old,new)
exec(compile(s,str(R/'DevelopmentTests/test_b055_boost_gw.py'),'exec'))
# Real production boundary function; no early-round implementation in the test harness.
q=lua.globals().SPCNetworkBoost.Quantize
for raw,want in [(0,0),(1.2,1),(1.49,1),(1.5,2),(1.8,2),(2.5,3),(3.49,3),(3.5,4),(3.8,4),(4*math.sqrt(2),6),(4.47*1.2,5),(4.49*1.4,6)]:
 assert q(raw)==want,(raw,want)
assert q(1.49*1.4)==2 and q(q(1.49)*1.4)==1  # early quantization is observably different
for raw in [-1,float('inf'),float('nan')]:
 try:q(raw)
 except Exception:pass
 else:raise AssertionError(raw)
lua.execute("""
local d=shared.NetworkBoost
Game.GetCurrentGameTurn=function() return 1 end
cities[1].owner=0;capital=cities[2];routes={};receive()
d.Test(0,0);assert(d.testRaw[0]==0 and d.applied[0].RESEARCH==nil and d.applied[0].CULTURE==nil)
d.Test(0,1.5)
for _,kind in ipairs({'RESEARCH','CULTURE'}) do assert(d.applied[0][kind].amount==2 and d.plans[0][kind].finalRaw==1.5) end
local writes=capital.writes;d.Test(0,1.5);d.Audit();receive();assert(capital.writes==writes)
d.Test(0,3.6);writes=capital.writes;d.Test(0,3.9);assert(capital.writes==writes and d.applied[0].RESEARCH.amount==4)
for _,kind in ipairs({'RESEARCH','CULTURE'}) do assert(not capital:GetBuildings():HasBuilding(P.Info('Buildings','BUILDING_SPC_B057_'..kind..'_2').Index)) end
d.Test(0,0);assert(d.applied[0].RESEARCH==nil and d.applied[0].CULTURE==nil)
d.Test(0,nil);assert(d.testRaw[0]==nil and d.applied[0].RESEARCH and not d.applied[0].RESEARCH.building:find('B057'))
d.Test(0,3.8);SPCNetworkBoost.Start(P,shared);d=shared.NetworkBoost;d.EnsureReady(0)
assert(d.testRaw[0]==nil)
for _,kind in ipairs({'RESEARCH','CULTURE'}) do for _,amount in ipairs({2,4}) do
 assert(not capital:GetBuildings():HasBuilding(P.Info('Buildings','BUILDING_SPC_B057_'..kind..'_'..amount).Index))
end end
-- An old database lacking test carriers reports failure, leaving ordinary network mode intact.
local info=P.Info
P.Info=function(t,k) if type(k)=='string' and k:find('B057') then return nil end return info(t,k) end
assert(not pcall(d.Test,0,1.5));assert(d.testRaw[0]==nil)
P.Info=info
assert(not pcall(d.Test,1,1.5))
""")
# New test SQL evaluated only in a disposable copy of the user's database.
p=json.loads((R/'local/config.json').read_text())['debug_gameplay_db']
src=sqlite3.connect('file:'+p+'?mode=ro',uri=True);c=sqlite3.connect(':memory:');src.backup(c);src.close()
c.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
for table,col in [('BuildingModifiers','ModifierId'),('ModifierArguments','ModifierId'),('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]:
 c.execute(f"delete from {table} where {col} like 'SPC_B057_%' or {col} like 'BUILDING_SPC_B057_%'")
c.executescript((R/'Mod/Data/BoostIntegerTest.sql').read_text())
for kind in ['RESEARCH','CULTURE']:
 for amount in [2,4]:
  m=f'SPC_B057_{kind}_{amount}'
  assert c.execute("select Value from ModifierArguments where ModifierId=? and Name='Amount'",(m,)).fetchone()[0]==str(amount)
  assert c.execute("select Value from ModifierArguments where ModifierId=? and Name='Amount'",(m+'_HD',)).fetchone()[0]==str(amount)
assert c.execute("select count(*) from Buildings where BuildingType like 'BUILDING_SPC_B057_%'").fetchone()[0]==4
assert not c.execute("select 1 from Modifiers m left join DynamicModifiers d on m.ModifierType=d.ModifierType where m.ModifierId like 'SPC_B057_%' and d.ModifierType is null").fetchall()
# All new visible controls have callbacks; keep within the user's readability budget.
x=ET.parse(R/'Mod/UI/P0Panel.xml').getroot();window=x.find("./Container[@ID='Window']")
visible=[b for b in window.findall('GridButton') if b.get('Hidden')!='1' and b.get('ID')!='CloseButton'];assert len(visible)<=15
for name in ['Zero','Half','High','Auto']:assert 'Controls.BoostTest'+name+'Button:RegisterCallback' in (R/'Mod/UI/P0Panel.lua').read_text()
s=(R/'DevelopmentTests/test_b055_regression.py').read_text();assert s.count("'72'")==2;s=s.replace("'72'","'74'")
exec(compile(s,str(R/'DevelopmentTests/test_b055_regression.py'),'exec'))
print('B057 LOCAL_SIMULATION_PASS: final-only half-up; explicit integer SQL; replace/idempotence/zero/restore/reload; missing-DB guard; prior regressions.')
