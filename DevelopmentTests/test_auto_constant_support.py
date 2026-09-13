from pathlib import Path
import sqlite3,zlib,xml.etree.ElementTree as ET
from lupa import LuaRuntime
P=Path(__file__).resolve().parent;R=P.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
ns={'__file__':str(P/'test_city_flow_resume.py')}
exec((P/'test_city_flow_resume.py').read_text().split('l=LuaRuntime(')[0],ns)
f=ns['f']+'''
local present={};local calls=0;local fail=false
local defs={RESEARCH=444,CULTURE=445,COMMERCE=446}
local oldInfo=P.Info
P.Info=function(t,k)
 if t=="Buildings" then
  for kind,id in pairs(defs) do if k=="BUILDING_SPC_DEV_"..kind.."_SUPPORT" then return {Index=id} end end
  return nil
 end
 return oldInfo(t,k)
end
rows[4]={Index=3,DistrictType="DISTRICT_COMMERCIAL_HUB"};P.Families.DISTRICT_COMMERCIAL_HUB="COMMERCE"
city.GetBuildings=function() return {HasBuilding=function(_,id) return present[id]==true end,
 RemoveBuilding=function(_,id) calls=calls+1;present[id]=nil end} end
city.GetBuildQueue=function() return {CreateBuilding=function(_,id) calls=calls+1;if not fail then present[id]=true end end} end
Map={GetPlot=function() return {GetWorkerCount=function() return 1 end} end}
local function start() SPCResearchSupport.Start(P,s) end
local function newcity()
 present={};calls=0;fail=false;fresh();start();Events.LoadScreenClose.Fire();found()
 assert(calls==0) -- no completed specialty, no carrier
end
local function finish(index)
 current=district(index,70+index);current.GetX=function() return 4 end;current.GetY=function() return 6 end
 dlist[2]=current;GameEvents.OnDistrictConstructed.Fire(0,index,4,6)
end
for i,kind in ipairs({"RESEARCH","CULTURE","COMMERCE"}) do
 newcity();finish(i)
 assert(present[defs[kind]] and calls==1) -- event auto enables without a UI request
 s.ResearchSupport.Audit();assert(calls==1)
 local output=s.ResearchSupport.Run(0,city,"RESEARCH_OFF") -- old request is now read-only
 assert(output:find("carrier="..kind) and calls==1)
 boot();start();Events.LoadScreenClose.Fire()
 assert(present[defs[kind]] and calls==1 and s.ResearchSupport.changes==0)
 s.CityFlowProbe.players[0].halted=true;s.ResearchSupport.Audit();assert(not present[defs[kind]] and calls==2)
end
newcity();finish(1)
-- Wrong carrier is removed before the correct one remains; no cross-specialty benefit.
present[445]=true;s.ResearchSupport.Audit();assert(present[444] and not present[445])
-- Disabled/foreign owner loses effects; no facts are rewritten by this module.
local oldTest=P.IsTestPlayer;P.IsTestPlayer=function() return false end
s.ResearchSupport.Audit();assert(not present[444]);P.IsTestPlayer=oldTest
-- Failed mutation is surfaced, then held rather than retried each turn.
newcity();fail=true;finish(1);local prior=calls
s.ResearchSupport.Audit();assert(calls==prior)
assert(s.ResearchSupport.Run(0,city,"RESEARCH_READ"):find("CARRIER_CHANGE_UNCONFIRMED"))
-- Missing new database definition is visible for an eligible culture city.
newcity();defs.CULTURE=nil;finish(2)
assert(s.ResearchSupport.Run(0,city,"RESEARCH_READ"):find("B023_DATABASE_MISSING"))
'''
l=LuaRuntime(unpack_returned_tuples=True)
for n in ['BindingProbe.lua','CityJournalProbe.lua','FreshBindingHook.lua','CityFlowProbe.lua','ResearchSupport.lua']:l.execute((R/n).read_text())
l.execute(f)
source=sqlite3.connect(f'file:{P.parent / "Cache/DebugGameplay.sqlite"}?mode=ro',uri=True)
c=sqlite3.connect(':memory:');source.backup(c);c.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
before=set(c.execute('PRAGMA foreign_key_check'))
# Existing cache can contain B022; validate additions against existing identical Research definition.
for name in ['ResearchSupport.sql','ConstantSupport.sql']:
 marker='BUILDING_SPC_DEV_RESEARCH_SUPPORT' if name=='ResearchSupport.sql' else 'BUILDING_SPC_DEV_CULTURE_SUPPORT'
 if not c.execute('select 1 from Buildings where BuildingType=?',(marker,)).fetchone():c.executescript((R/'Data'/name).read_text())
for kind,district in [('RESEARCH','CAMPUS'),('CULTURE','THEATER'),('COMMERCE','COMMERCIAL_HUB')]:
 name='BUILDING_SPC_DEV_'+kind+'_SUPPORT'
 assert c.execute('select InternalOnly,CitizenSlots,Housing,Maintenance,PrereqDistrict from Buildings where BuildingType=?',(name,)).fetchone()==(1,0,0,0,'DISTRICT_'+district)
 assert set(c.execute('select YieldType,YieldChange from Building_CitizenYieldChanges where BuildingType=?',(name,)))=={('YIELD_FOOD',3),('YIELD_PRODUCTION',3)}
assert set(c.execute('PRAGMA foreign_key_check'))==before
for p in R.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=ET.parse(R/'SpecializationP0.modinfo').getroot();assert m.attrib=={'id':'df9efdad-dd48-40a7-b868-87f0617bc16d','version':'30'}
for e in m.findall('.//File'):assert (R/e.text).is_file()
ET.parse(R/'UI/P0Panel.xml')
print('LOCAL_SIMULATION_PASS: three actual completion flows automatically enable matching carriers; no UI write; repeat/load/invalid gate/foreign owner/wrong carrier/mutation error/database missing; SQL, Lua, XML; not a game test.')
