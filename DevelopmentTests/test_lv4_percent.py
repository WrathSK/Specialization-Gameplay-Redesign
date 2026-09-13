from pathlib import Path
import sqlite3,zlib,xml.etree.ElementTree as E,hashlib
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
b=w/'DevelopmentBackups/Specialization-before-B048-lv4-percent/RuntimeSnapshot'
for n in ['UnitActions.lua','CrewProjects.lua','Data/Crew.sql','Data/CrewProjects.sql','ConstructionProbe.lua','InvestmentAction.lua','UI/UnitPanelActions.lua','Lv3Support.lua','Data/Lv3Effects.sql']:
 assert (r/n).read_bytes()==(b/n).read_bytes(),n
v=LuaRuntime(unpack_returned_tuples=True)
v.execute('''
rows={};idx=0
for _,k in ipairs({'RESEARCH','CULTURE'}) do for bit=0,7 do idx=idx+1;rows['BUILDING_SPC_LV4_PERCENT_'..k..'_'..bit]={Index=idx} end end
P={IsTestPlayer=function(pid) return pid==0 and enabled end,Field=function(t,k) return t and t[k] end,
Info=function(t,k) if t=='Buildings' then return rows[k] else return {DistrictType=k==1 and 'DISTRICT_CAMPUS' or 'DISTRICT_THEATER'} end end}
enabled=true;cities={};districts={};propertiesWrites=0;workers={2,3};facts={}
for i,k in ipairs({'RESEARCH','CULTURE'}) do
 local c={id=i,owner=0,b={OTHER=true}};cities[i]=c
 c.GetOwner=function() return c.owner end;c.GetID=function() return i end
 c.GetBuildings=function() return {HasBuilding=function(_,id) return c.b[id]==true end,RemoveBuilding=function(_,id) c.b[id]=nil end} end
 c.GetBuildQueue=function() return {CreateBuilding=function(_,id) c.b[id]=true end} end
 facts[i]={specialization=k,potential=4,active=4,first={districtID=i,type=i==1 and 'DISTRICT_CAMPUS' or 'DISTRICT_THEATER'}}
 local d={complete=true};districts[i]=d;d.GetCity=function() return c end;d.GetID=function() return i end
 d.GetType=function() return i end;d.GetX=function() return i end;d.GetY=function() return 0 end;d.IsComplete=function() return d.complete end
end
Players={[0]={GetCities=function() return {Members=function() return ipairs(cities) end} end,GetDistricts=function() return {Members=function() return ipairs(districts) end} end}}
Map={GetPlot=function(x) return {GetWorkerCount=function() return workers[x] end} end}
shared={EffectiveFacts={Read=function(_,c) if bad then error('fact failure') end;return facts[c.id] end}}
hooks={};Events=setmetatable({},{__index=function(t,k) local e={Add=function(f) hooks[k]=f end};t[k]=e;return e end});GameEvents={}
function amount(i,k)
 local sum=0;for b=0,7 do if cities[i].b[rows['BUILDING_SPC_LV4_PERCENT_'..k..'_'..b].Index] then sum=sum+5*2^b end end;return sum
end
''')
v.execute((r/'Lv4Percent.lua').read_text());v.execute('''
SPCLv4Percent.Start(P,shared);shared.Lv4Percent.Audit();assert(amount(1,'RESEARCH')==0)
hooks.LoadScreenClose();assert(amount(1,'RESEARCH')==10 and amount(2,'CULTURE')==15)
assert(amount(1,'CULTURE')==0 and amount(2,'RESEARCH')==0)
local n=shared.Lv4Percent.changes;shared.Lv4Percent.Audit();assert(shared.Lv4Percent.changes==n)
facts[1].active=3;hooks.GovernorChanged();assert(amount(1,'RESEARCH')==0 and amount(2,'CULTURE')==15)
assert(shared.Lv4Percent.Describe(0,cities[1]):find('实际专家=2',1,true))
facts[1].active=4;hooks.GovernorPromoted();assert(amount(1,'RESEARCH')==10)
workers[1]=1;hooks.CityWorkerChanged();assert(amount(1,'RESEARCH')==5)
workers[1]=0;hooks.CityWorkerChanged();assert(amount(1,'RESEARCH')==0)
workers[1]=2;hooks.CityWorkerChanged();assert(amount(1,'RESEARCH')==10)
SPCLv4Percent.Start(P,shared);hooks.LoadScreenClose();assert(shared.Lv4Percent.changes==0)
workers[1]=0.5;hooks.CityWorkerChanged();assert(amount(1,'RESEARCH')==0 and shared.Lv4Percent.errors['0:1'])
workers[1]=2;hooks.CityWorkerChanged();assert(amount(1,'RESEARCH')==10)
enabled=false;shared.Lv4Percent.Audit();assert(amount(1,'RESEARCH')==0 and amount(2,'CULTURE')==0)
enabled=true;shared.Lv4Percent.Audit();assert(amount(2,'CULTURE')==15)
districts[1].complete=false;shared.Lv4Percent.Audit();assert(amount(1,'RESEARCH')==0)
districts[1].complete=true;cities[1].owner=1;shared.Lv4Percent.Audit();assert(amount(1,'RESEARCH')==0)
cities[1].owner=0;shared.Lv4Percent.Audit();assert(amount(1,'RESEARCH')==10)
bad=true;shared.Lv4Percent.Audit();assert(amount(1,'RESEARCH')==0 and amount(2,'CULTURE')==0)
assert(cities[1].b.OTHER and cities[2].b.OTHER)
''')
# Execute actual SQL only on a read-only DB's in-memory copy.
d=sqlite3.connect((w/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True)
m=sqlite3.connect(':memory:');d.backup(m);m.create_function('Make_Hash',1,lambda x:zlib.crc32(x.encode()));m.executescript((r/'Data/Lv4Percent.sql').read_text())
assert m.execute("select CollectionType,EffectType from DynamicModifiers where ModifierType='MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_MODIFIER'").fetchone()==('COLLECTION_OWNER','EFFECT_ADJUST_CITY_YIELD_MODIFIER')
for k,y in [('RESEARCH','SCIENCE'),('CULTURE','CULTURE')]:
 for bit in range(8):
  mod=f'SPC_LV4_PERCENT_{k}_{bit}';name=f'BUILDING_SPC_LV4_PERCENT_{k}_{bit}'
  assert dict(m.execute('select Name,Value from ModifierArguments where ModifierId=?',(mod,)))=={'YieldType':'YIELD_'+y,'Amount':str(5*2**bit)}
  assert m.execute('select ModifierType from Modifiers where ModifierId=?',(mod,)).fetchone()[0]=='MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_MODIFIER'
  assert m.execute('select InternalOnly,CitizenSlots,Housing from Buildings where BuildingType=?',(name,)).fetchone()==(1,0,0)
  assert m.execute('select ModifierId from BuildingModifiers where BuildingType=?',(name,)).fetchone()[0]==mod
assert 'shared.Lv4Percent.Audit()' in (r/'Lv3Effects.lua').read_text()
# UI getter is exactly the native CitySupport API; narrow request must dispatch readonly Describe.
assert 'city:GetYieldToolTip(GameInfo.Yields[yieldType].Index)' in (r/'UI/P0Panel.lua').read_text()
assert 'shared.Lv4Percent.Describe(playerID,c)' in (r/'Gameplay.lua').read_text()
syntax=LuaRuntime(unpack_returned_tuples=True)
for p in r.rglob('*.lua'):syntax.execute('assert(load(...))',p.read_text())
for p in r.rglob('*.xml'):E.parse(p)
root=E.parse(r/'SpecializationP0.modinfo').getroot();assert root.get('version')=='61'
for f in root.findall('.//File'):assert (r/f.text).is_file()
print('LOCAL_SIMULATION_PASS B048: actual ACTIVE4/worker gating, +5pp bits, city/yield isolation, immediate event refresh, repeated/load no duplication, inactive/ineligible/unknown removal; SQL matches native city-yield-percent effect. Native yields require user testing.')
