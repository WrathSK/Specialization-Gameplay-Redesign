"""B022 actual Lua module + B013/B015/B021 flow and real cached schema in memory."""
from pathlib import Path
import sqlite3
import zlib
import xml.etree.ElementTree as ET
from lupa import LuaRuntime

P = Path(__file__).resolve().parent
R = P.parent / "Sid Meier's Civilization VI/Mods/SpecializationP0"
# Reuse the existing flow scenarios without altering the frozen B021 manifest assertion.
ns = {'__file__': str(P / 'test_city_flow_resume.py')}
exec((P / 'test_city_flow_resume.py').read_text().split('l=LuaRuntime(')[0], ns)
fixture = ns['f'] + '''
fresh();found();complete(1)
dlist[2]=current;current.GetX=function() return 4 end;current.GetY=function() return 6 end
local exists=false;local creates,removes=0,0;local broken=false
local buildings={HasBuilding=function() return exists end,
 RemoveBuilding=function() removes=removes+1;exists=false end}
city.GetBuildings=function() return buildings end
city.GetBuildQueue=function() return {CreateBuilding=function() creates=creates+1;if not broken then exists=true end end} end
local oldInfo=P.Info
P.Info=function(tableName,key)
 if tableName=="Buildings" then return {Index=444} end
 return oldInfo(tableName,key)
end
Map={GetPlot=function() return {GetWorkerCount=function() return 1 end} end}
local function start() SPCResearchSupport.Start(P,s) end
start()
assert(s.ResearchSupport.Run(0,city,"RESEARCH_READ"):find("support=OFF"))
assert(creates==0 and removes==0)
assert(s.ResearchSupport.Run(0,city,"RESEARCH_ON"):find("support=ON"))
assert(creates==1 and s.ResearchSupport.Run(0,city,"RESEARCH_ON"):find("workers=1"))
assert(creates==1) -- no stacked building or repeated create
boot();start();Events.LoadScreenClose.Fire()
assert(exists and creates==1 and s.ResearchSupport.changes==0)
assert(s.ResearchSupport.Run(0,city,"RESEARCH_READ"):find("support=ON"))
assert(s.ResearchSupport.Run(0,city,"RESEARCH_OFF"):find("support=OFF"))
s.ResearchSupport.Run(0,city,"RESEARCH_OFF");assert(removes==1)
broken=true
assert(s.ResearchSupport.Run(0,city,"RESEARCH_ON"):find("CARRIER_CHANGE_UNCONFIRMED"));broken=false
s.ResearchSupport.Run(0,city,"RESEARCH_ON");assert(exists)
s.CityFlowProbe.players[0].halted=true;s.ResearchSupport.Audit();assert(not exists)
-- No Research identity: explicit ON cannot grant the carrier.
fresh();found();start()
assert(s.ResearchSupport.Run(0,city,"RESEARCH_ON"):find("NOT_RESEARCH"));assert(not exists)
-- A captured/foreign city cannot retain a DEV carrier.
exists=true;local oldTest=P.IsTestPlayer;P.IsTestPlayer=function() return false end
s.ResearchSupport.Audit();assert(not exists);P.IsTestPlayer=oldTest
-- A missing definition is visible, never reported as successful ON.
local originalInfo=P.Info;P.Info=function(t,k) if t=="Buildings" then return nil end;return originalInfo(t,k) end
assert(s.ResearchSupport.Run(0,city,"RESEARCH_ON"):find("B022_DATABASE_MISSING"))
'''
lua = LuaRuntime(unpack_returned_tuples=True)
for name in ['BindingProbe.lua', 'CityJournalProbe.lua', 'FreshBindingHook.lua', 'CityFlowProbe.lua', 'ResearchSupport.lua']:
    lua.execute((R / name).read_text())
lua.execute(fixture)

source = sqlite3.connect(f'file:{P.parent / "Cache/DebugGameplay.sqlite"}?mode=ro', uri=True)
db = sqlite3.connect(':memory:')
source.backup(db)
# Schema trigger compatibility only; not proof of Civ VI runtime hashes.
db.create_function('Make_Hash', 1, lambda s: zlib.crc32(s.encode()))
prior_fk = set(db.execute('PRAGMA foreign_key_check'))
db.executescript((R / 'Data/ResearchSupport.sql').read_text())
assert set(db.execute('PRAGMA foreign_key_check')) == prior_fk
name = 'BUILDING_SPC_DEV_RESEARCH_SUPPORT'
assert db.execute('SELECT InternalOnly,CitizenSlots,Housing,Maintenance,PrereqDistrict FROM Buildings WHERE BuildingType=?', (name,)).fetchone() == (1, 0, 0, 0, 'DISTRICT_CAMPUS')
assert set(db.execute('SELECT YieldType,YieldChange FROM Building_CitizenYieldChanges WHERE BuildingType=?', (name,))) == {('YIELD_FOOD', 3), ('YIELD_PRODUCTION', 3)}
assert not db.execute('SELECT * FROM Building_YieldChanges WHERE BuildingType=?', (name,)).fetchall()
for path in R.rglob('*.lua'):
    lua.execute('assert(load(...))', path.read_text())
manifest = ET.parse(R / 'SpecializationP0.modinfo').getroot()
assert manifest.attrib == {'id': 'df9efdad-dd48-40a7-b868-87f0617bc16d', 'version': '29'}
for item in manifest.findall('.//File'):
    assert (R / item.text).is_file()
assert len(manifest.findall("./InGameActions/UpdateDatabase/File[.='Data/ResearchSupport.sql']")) == 1
ET.parse(R / 'UI/P0Panel.xml')
print('LOCAL_SIMULATION_PASS: actual flow + native-carrier API mocks; ON/OFF idempotence, reload, invalid identity cleanup, failed create, database missing; real SQL schema/foreign keys and all Lua/XML. Native yield magnitude is USER_GAME_TEST_REQUIRED.')
