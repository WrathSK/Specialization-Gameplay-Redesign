"""B018 actual runtime script; automatic sampling, no gameplay writes or UI reads."""
from pathlib import Path
from lupa import LuaRuntime
r=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
l.execute((r/'EligibilityProbe.lua').read_text())
l.execute('''
print=function() end
local function deny() error("FORBIDDEN_GAMEPLAY_OR_UI_ACCESS") end
local rows={{CivilizationType="TEST",TraitType="TRAIT_CIVILIZATION_SPC_TEST"}}
local broken=false
local function iter()
 local i=0;return function() i=i+1;if broken and i>1 then error("INTERRUPTED_DB") end;return rows[i] end
end
GameInfo={Traits={TRAIT_CIVILIZATION_SPC_TEST={}},CivilizationTraits=iter}
Players={[0]={GetCities=deny,GetProperty=deny,SetProperty=deny},[1]={GetCities=deny},[2]={}}
PlayerConfigurations={
 [0]={GetCivilizationTypeName=function() return "TEST" end,IsHuman=deny},
 [1]={GetCivilizationTypeName=function() return "OTHER" end},
 [2]={GetCivilizationTypeName=function() return "TEST" end}}
UI={};Game={SetProperty=deny};local handlers={}
Events={LoadScreenClose={Add=function(fn) handlers[#handlers+1]=fn end}}
local P={VERSION="P0-B-018"};local s={}
SPCEligibilityProbe.Start(P,s)
local d=s.EligibilityProbe
assert(d.samples.INITIALIZE.rows[0].status=="ENABLED")
assert(d.samples.INITIALIZE.enabled==2 and d.samples.INITIALIZE.disabled==1)
assert(not d.samples.LOAD_CLOSE and d.hooks.LoadScreenClose=="REGISTERED")
handlers[1]()
assert(d.samples.LOAD_CLOSE.rows[0].status=="ENABLED")
assert(d.samples.LOAD_CLOSE.unknown==0)
-- Read failures remain unknown; matching first row must not hide failed iteration.
broken=true;handlers[1]()
assert(d.samples.LOAD_CLOSE.rows[0].status=="UNKNOWN")
assert(d.samples.INITIALIZE.rows[0].status=="ENABLED") -- frozen startup sample
broken=false;PlayerConfigurations[0]=nil;handlers[1]()
assert(d.samples.LOAD_CLOSE.rows[0].status=="UNKNOWN")
PlayerConfigurations[0]={GetCivilizationTypeName=function() return "TEST" end}
-- New script session rebuilds from engine tables, with no prior state or panel use.
handlers={};local fresh={};SPCEligibilityProbe.Start(P,fresh);handlers[1]()
assert(fresh.EligibilityProbe.samples.LOAD_CLOSE.rows[0].status=="ENABLED")
Events={};local absent={};SPCEligibilityProbe.Start(P,absent)
assert(absent.EligibilityProbe.hooks.LoadScreenClose=="ABSENT")
Players=nil;local missing={};SPCEligibilityProbe.Start(P,missing)
assert(missing.EligibilityProbe.samples.INITIALIZE.status=="UNKNOWN")
''')
# UI inspection checks the actual callback has no dispatch or scan pathway.
s=(r/'UI/P0Panel.lua').read_text()
handler=s.split('Controls.EligibilityButton:RegisterCallback',1)[1].split('Controls.CityJournalButton:RegisterCallback',1)[0]
assert 'UI.RequestPlayerOperation' not in handler and 'request(' not in handler and 'GameInfo' not in handler
assert 'd.samples[phase]' in handler and 'localReport=' in handler
import xml.etree.ElementTree as ET
mod=ET.parse(r/'SpecializationP0.modinfo').getroot()
assert mod.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d' and mod.attrib['version']=='25'
assert sum(e.text=='EligibilityProbe.lua' for e in mod.findall('./InGameActions/ImportFiles/File'))==1
assert sum(e.text=='EligibilityProbe.lua' for e in mod.findall('./Files/File'))==1
assert 'EligibilityButton' in {e.attrib.get('ID') for e in ET.parse(r/'UI/P0Panel.xml').iter()}
print('LOCAL_SIMULATION_PASS: actual B018 automatic initialize/load, failure isolation, human-independent binding, recreated session, missing hook/roster; no write/city/UI API; UI display-only callback; XML/manifest linkage.')
