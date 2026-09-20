"""Actual opt-in Lua/SQL. Native float retention is deliberately NOT simulated as proof."""
from pathlib import Path
import zlib,sqlite3,subprocess,json,xml.etree.ElementTree as ET,ast
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
l=LuaRuntime(unpack_returned_tuples=True)
l.execute("""
writes=0;reads=0;handlers={};buildings={};b={};failRemove=false;failCreate=false
function b:HasBuilding(id) reads=reads+1;return buildings[id]==true end
c={};d={};complete=true;pillaged=false;half=false
function d:GetType() return 2 end
function d:GetID() return 10 end
function d:GetX() return 5 end;function d:GetY() return 6 end
function d:IsComplete() return complete end;function d:IsPillaged() return pillaged end
function c:GetBuildings() return b end;function c:GetBuildQueue() return {} end
function c:GetOwner() return 0 end;function c:GetID() return 1 end
function c:GetX() return 1 end;function c:GetY() return 2 end
function c:GetPopulation() return 5 end;function c:GetProperty(k) return half end
function members(t) local i=0;return function() i=i+1;if t[i] then return i,t[i] end end end
function c:GetDistricts() return {Members=function() return members({d}) end} end
cities={Members=function() return members({c}) end,FindID=function() return c end}
Players={[0]={GetCities=function() return cities end}}
Events={LoadScreenClose={Add=function(f) handlers.load=f end}}
P={IsTestPlayer=function(id) return id==0 end,Field=function(t,k) return t[k] end,
Rows=function() return {{CivUniqueDistrictType='DISTRICT_SEOWON',ReplacesDistrictType='DISTRICT_CAMPUS'}} end,
Info=function(t,k) if t=='Buildings' then return {Index=k} elseif t=='Districts' then return {DistrictType='DISTRICT_SEOWON'} else return {Index=3} end end,
HasBuilding=function(b,id) return b:HasBuilding(id) end,
CreateBuilding=function(q,id) if not failCreate then buildings[id]=true;writes=writes+1 end end,
RemoveBuilding=function(b,id) if not failRemove then buildings[id]=false;writes=writes+1 end end}
shared={}
""")
l.execute((M/'DistrictPrecisionProbe.lua').read_text());l.execute('SPCDistrictPrecisionProbe.Start(P,shared);p=shared.DistrictPrecisionProbe')
l.execute("""
assert(writes==0);p.Run(0,c,'DP_READ');assert(writes==0 and p.view.amount==0)
p.Run(0,c,'DP_SET_03');assert(writes==1 and p.view.amount==0.3)
local r,w=reads,writes;for i=1,10000 do end;assert(reads==r and writes==w)
for i=1,10000 do p.Run(0,c,'DP_SET_03') end;assert(writes==1)
p.Run(0,c,'DP_SET_05');assert(writes==3 and p.view.amount==0.5)
failRemove=true;assert(not pcall(p.Run,0,c,'DP_SET_1'));assert(writes==3)
failRemove=false;p.Run(0,c,'DP_SET_1');assert(writes==5 and p.view.amount==1)
p.Run(0,c,'DP_OFF');assert(writes==6 and p.view.amount==0);p.Run(0,c,'DP_OFF');assert(writes==6)
pillaged=true;assert(not pcall(p.Run,0,c,'DP_SET_03'));assert(writes==6);pillaged=false
complete=false;assert(not pcall(p.Run,0,c,'DP_SET_03'));complete=true
half=true;assert(not pcall(p.Run,0,c,'DP_SET_03'));half=false
assert(not pcall(p.Run,1,c,'DP_SET_03'));assert(not pcall(p.Run,0,c,'DP_SET_FAKE'))
failCreate=true;assert(not pcall(p.Run,0,c,'DP_SET_03'));failCreate=false
p.Run(0,c,'DP_SET_03');handlers.load();assert(writes==8 and p.view==nil and not p.cleanupError)
handlers.load();assert(writes==8)
""")
print('PASS manual only, exact replacement/idempotence10000, failed removal prevents add, OFF/load cleanup, ownership/availability/old probe guard')
l.execute("""
Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return 1 end}
amount=0;function d:GetYield() reads=reads+1;return 4+amount end
function d:GetAdjacencyYield() return 4+amount end;function c:GetYield() return 10+amount*1.1 end
Map={GetPlot=function() return {GetAdjacencyYield=function() return 4 end} end}
v={owner=0,city=1,amount=0,token='t'}
""")
l.execute((M/'DistrictPrecisionRead.lua').read_text())
l.execute("""
local t=SPCDistrictPrecisionRead.Render(P,v,'t');assert(t:find('0.000000'))
v.amount=0.3;amount=0.3;t=SPCDistrictPrecisionRead.Render(P,v,'t');assert(t:find('+0.300000',1,true) and t:find('+0.330000',1,true))
assert(SPCDistrictPrecisionRead.Render(P,v,'old'):find('UNKNOWN'))
function d:GetYield() return nil end;assert(SPCDistrictPrecisionRead.Render(P,v,'t'):find('UNKNOWN'))
""")
print('PASS mock readout separates district/adjacency/Plot BASE/city, explicit baseline, stale response and nil stay UNKNOWN; NOT native decimal PASS')
# Real panel idle: controls exist and acknowledgments do not resample each frame.
t=ast.parse((R/'DevelopmentTests/test_arch_v2_d2.py').read_text())
fix=next(ast.literal_eval(x.value) for x in t.body if isinstance(x,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='UI_FIX' for k in x.targets))
u=LuaRuntime();u.execute(fix)
u.execute("Mouse.eRClick=2;P.Scalar=tostring;print=function() end;callbacks={};for _,k in ipairs({'Read','03','05','1'}) do local key=k;Controls['DP'..key..'Button'].RegisterCallback=function(c,e,f) callbacks[key..e]=f end end;UI.RequestPlayerOperation=function(pid,op,p) sends=sends+1;lastAction=p.Action;shared.LastToken=p.Token;shared.Snapshot='probe';end;nativeReads=0;SPCDistrictPrecisionRead={Render=function() nativeReads=nativeReads+1;return 'native' end}")
u.execute((M/'UI/P0Panel.lua').read_text())
u.execute("init();callbacks['Read1']();assert(sends==1 and nativeReads==1);for i=1,10000 do fire('SystemUpdateUI');if update then update(0.01) end end;assert(sends==1 and nativeReads==1);callbacks['051']();assert(lastAction=='DP_SET_05');callbacks['Read2']();assert(lastAction=='DP_OFF');assert(sends==3)")
print('PASS actual panel 10000 idle callbacks: no extra send or native reads; explicit amount actions and right-click OFF')
# Execute SQL in disposable copy of external read-only gameplay DB.
cfg=json.loads((R.parent/'Specialization-Gameplay-Redesign/local/config.json').read_text())
source=sqlite3.connect('file:'+cfg['debug_gameplay_db']+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');source.backup(db);source.close();db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
before={t:db.execute('select count(*) from '+t).fetchone()[0] for t in ['Modifiers','BuildingModifiers','Buildings']}
db.executescript((M/'Data/DistrictPrecisionProbe.sql').read_text())
for t,n in before.items():assert db.execute('select count(*) from '+t).fetchone()[0]==n+3
for key,a in [('03',.3),('05',.5),('1',1)]:
 mid='SPC_B082_DISTRICT_'+key
 assert db.execute('select ModifierType,SubjectRequirementSetId from Modifiers where ModifierId=?',(mid,)).fetchone()==('MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE','SPC_B082_CAMPUS')
 assert float(db.execute("select Value from ModifierArguments where ModifierId=? and Name='Amount'",(mid,)).fetchone()[0])==a
assert db.execute("select CollectionType,EffectType from DynamicModifiers where ModifierType='MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE'").fetchone()==('COLLECTION_CITY_DISTRICTS','EFFECT_ADJUST_DISTRICT_YIELD_CHANGE')
print('PASS SQL external DB read-only -> memory; +3 isolated carriers/modifiers, correct city-district collection. SQLite floats NOT engine proof')
allowed={'DistrictPrecisionProbe.lua','DistrictPrecisionRead.lua','Data/DistrictPrecisionProbe.sql','Gameplay.lua','UI/P0Panel.lua','UI/P0Panel.xml','SpecializationP0.modinfo','Probe.lua','UI/RuntimeAudit.lua'}
base='acf9ba7'
for p in M.rglob('*'):
 if p.is_file() and p.relative_to(M).as_posix() not in allowed:assert p.read_bytes()==subprocess.check_output(['git','show',base+':Mod/'+p.relative_to(M).as_posix()],cwd=R),p
subprocess.run(['git','diff','--exit-code',base,'--','Specialization/Design'],cwd=R,check=True)
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='109'
files=[r.text for r in x.findall('./Files/File')];assert len(files)==len(set(files))
assert set(files)=={p.relative_to(M).as_posix() for p in M.rglob('*') if p.is_file() and p.name!='SpecializationP0.modinfo'}
for p in M.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
panel=ET.parse(M/'UI/P0Panel.xml').getroot();ids=[e.get('ID') for e in panel.iter() if e.get('ID')];assert len(ids)==len(set(ids))
print('PASS all Lua compile, XML/manifest exact files, existing effect modules/SQL and Design unchanged')
