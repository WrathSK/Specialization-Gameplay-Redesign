from pathlib import Path
from lupa import LuaRuntime
r=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True);l.execute((r/'QualificationProbe.lua').read_text())
l.execute('''
print=function() end
local function deny() error("NO_CITY_PROPERTY_OR_UI") end
Players={[0]={GetCities=deny},[1]={GetCities=deny},[54]={GetCities=deny}}
PlayerConfigurations={[0]={GetCivilizationTypeName=function() return "TEST" end},
 [1]={GetCivilizationTypeName=function() return "OTHER" end},[54]={GetCivilizationTypeName=function() return "" end}}
GameInfo={Traits={TRAIT_CIVILIZATION_SPC_TEST={}},CivilizationTraits=function()
 local done=false;return function() if not done then done=true;return {CivilizationType="TEST",TraitType="TRAIT_CIVILIZATION_SPC_TEST"} end end
end}
local hooks={};Events={LoadScreenClose={Add=function(f) hooks[#hooks+1]=f end}}
local P={VERSION="P0-B-018"};local shared={}
PlayerManager=nil;SPCQualificationProbe.Start(P,shared)
assert(shared.QualificationProbe.status=="UNKNOWN")
PlayerManager={GetAliveIDs=function() return {0,1} end};hooks[1]()
local d=shared.QualificationProbe
assert(d.status=="COMPLETE_ROSTER" and d.phase=="LOAD_CLOSE" and d.permissions[0] and not d.permissions[1])
assert(d.text:find("PASS") and d.text:find("54%-61"))
assert(not d.gate and not d.tokens)
PlayerManager.GetAliveIDs=function() return {0,54} end;hooks[1]()
assert(d.permissions[0] and not d.permissions[54] and d.text:find("未知=54"))
PlayerManager.GetAliveIDs=function() error("ROSTER_LOST") end;hooks[1]()
assert(d.status=="UNKNOWN" and not d.permissions[0] and d.text:find("NOT_PROVEN"))
PlayerManager.GetAliveIDs=function() return {0} end;hooks[1]()
assert(d.permissions[0] and d.text:find("PASS"))
-- fresh Gameplay-like session, independently recollect before any panel read
hooks={};local reloaded={};SPCQualificationProbe.Start(P,reloaded)
assert(not reloaded.QualificationProbe.permissions[0]);hooks[1]()
assert(reloaded.QualificationProbe.permissions[0])
''')
import xml.etree.ElementTree as ET
m=ET.parse(r/'SpecializationP0.modinfo').getroot()
assert m.attrib['version']=='25'
assert sum(e.text=='QualificationProbe.lua' for e in m.findall('./InGameActions/ImportFiles/File'))==1
assert sum(e.text=='QualificationProbe.lua' for e in m.findall('./Files/File'))==1
print('LOCAL_SIMULATION_PASS: actual composed Gameplay diagnostic; late API readiness, active subset, unknown inside roster, private permits, invalidation/reacquisition self-check, failed roster clears permissions, fresh session; manifest. No real yield or lifecycle event proof.')
