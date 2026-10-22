"""Targeted L3: real Lua experimental mapping, not native identity certification."""
from pathlib import Path
import subprocess, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod';l=LuaRuntime()
for name in ['CityIdentityRead','CityIdentityExperiment','CityIdentityMapping']:l.execute((M/(name+'.lua')).read_text())
old=(R/'DevelopmentTests/test_p0_e1.py').read_text()
l.execute('M=SPCCityIdentityRead\n'+old[old.index('function fixture()'):old.index('function expect(')])
l.execute(r'''
key=SPCCityIdentityMapping.KEY;store={};writes=0;turn=8
function events()return setmetatable({}, {__index=function(t,k)local e={};function e.Add(f)e.fn=f end;rawset(t,k,e);return e end})end
function setup(owner,id,missing)
 Events=events();GameEvents=events();s=fixture();exists=not missing;badwrite=false
 if owner then s.ref.owner=owner;s.ref.cityID=id;s.values={}end
 city={GetOwner=function()return s.ref.owner end,GetID=function()return s.ref.cityID end,GetX=function()return s.ref.x end,GetY=function()return s.ref.y end,
 GetProperty=function(self,k)for name,v in pairs(M.Keys)do if k==v then return s.values[name]end end;error('unknown key')end,SetProperty=function()error('CITY_WRITE')end}
 Game={GetProperty=function(self,k)if k==key then return M.Copy(store[k])end;assert(k=='SPC_DEV_BINDING_B013_P0','READ_LEGACY_EXPERIMENT');return s.ledger end,
 SetProperty=function(self,k,v)assert(k==key,'OLD_WRITER');writes=writes+1;if not badwrite then store[k]=M.Copy(v)end end,GetCurrentGameTurn=function()return turn end}
 CityManager={GetCityAt=function(x,y)assert(x==4 and y==5);return exists and city or nil end}
 P={VERSION='B093.120',Field=function(t,k)return t[k]end,IsTestPlayer=function(p)return p==0 end}
 shared={};SPCCityIdentityMapping.Start(P,shared);d=shared.CityIdentityExperiment
end
function fresh()store={};writes=0;turn=8;setup();assert(d.Begin(0,city):find('已建立'));assert(writes==1)end
function transfer()
 s.ref.owner=62;s.ref.cityID=40;s.values={}
 GameEvents.CityBuilt.fn(62,40,4,5);Events.CityRemovedFromMap.fn(0,7);Events.CityAddedToMap.fn(62,40,4,5);Events.CityInitialized.fn(62,40,4,5)
 Events.CulturalIdentityCityConverted.fn(62,40,0,24576);Events.CityTransfered.fn(62,40,0,-738490196)
end
setup();assert(writes==0);Events.CityRemovedFromMap.fn(0,7);assert(writes==0)
fresh();local begin=d.Begin(0,city);assert(begin:find('不覆盖') and writes==1)
transfer();assert(store[key].mappingState=='MAPPED_EXPERIMENT' and writes==3)
local saved=M.Copy(store[key]);local text=d.Describe(0);assert(text:find('映射已保存') and writes==3)
for i=1,10000 do Events.CityTransfered.fn(62,40,0,-738490196);Events.CulturalIdentityCityConverted.fn(62,40,0,24576);Events.CityAddedToMap.fn(99,i,20,20)end
assert(writes==3 and #store[key].transition.evidence<=16)
assert(Events.PublishComplete.fn==nil and Events.PlaybackComplete.fn==nil and Events.UnitMoved.fn==nil)
-- Cold gameplay context initializes without diagnostic or LoadScreenClose.
setup(62,40);assert(not d.error and writes==3);assert(d.Describe(0):find('已保存映射恢复'));assert(store[key].candidateKey==saved.candidateKey and writes==3)
Events.LoadScreenClose.fn();assert(writes==3)
Events.CityRemovedFromMap.fn(62,40);assert(store[key].mappingState=='HELD' and writes==4)
Events.CityRemovedFromMap.fn(62,40);assert(writes==4)
-- No click needed before cold save restoration: fixture reads the auto-written store.
fresh();transfer();setup(62,40);assert(d.Describe(0):find('已保存映射恢复'))
-- Starting reference reload does not reset experiment or require Begin.
fresh();setup();transfer();assert(store[key].mappingState=='MAPPED_EXPERIMENT')
-- Pending cold load never uses old observations; only one HELD write.
fresh();s.ref.owner=62;s.ref.cityID=40;Events.CityRemovedFromMap.fn(0,7);assert(store[key].mappingState=='TRANSFER_PENDING')
setup(62,40);assert(store[key].mappingState=='HELD');local w=writes;Events.CulturalIdentityCityConverted.fn(62,40,0);d.Describe(0);assert(writes==w)
-- Temporary missing object, later direct event completes.
fresh();s.ref.owner=62;s.ref.cityID=40;exists=false;Events.CityRemovedFromMap.fn(0,7);assert(store[key].mappingState=='TRANSFER_PENDING');exists=true
Events.CityAddedToMap.fn(62,40,4,5);Events.CulturalIdentityCityConverted.fn(62,40,0);assert(store[key].mappingState=='MAPPED_EXPERIMENT')
-- Reverse matching order; typed arrives first, no new schema magic.
fresh();s.ref.owner=62;s.ref.cityID=40
Events.CulturalIdentityCityConverted.fn(62,40,0);Events.CityAddedToMap.fn(62,40,4,5);Events.CityRemovedFromMap.fn(0,7);assert(store[key].mappingState=='MAPPED_EXPERIMENT')
-- Matching late initialization after earlier complete proof is not a new transfer.
local w=writes;Events.CityInitialized.fn(62,40,4,5);assert(writes==w and store[key].mappingState=='MAPPED_EXPERIMENT')
setup(62,40,true);local w=writes;assert(not d.error and store[key].mappingState=='MAPPED_EXPERIMENT');assert(d.Describe(0):find('暂不可读'));assert(writes==w)
exists=true;assert(d.Describe(0):find('已保存映射恢复'));assert(writes==w)
-- Missing proof / stale turn, wrong prior owner, additional removal.
fresh();s.ref.owner=62;s.ref.cityID=40;Events.CityAddedToMap.fn(62,40,4,5);Events.CityRemovedFromMap.fn(0,7);assert(store[key].mappingState=='TRANSFER_PENDING');turn=9;d.Describe(0);assert(store[key].mappingState=='HELD')
fresh();s.ref.owner=62;s.ref.cityID=40;Events.CityAddedToMap.fn(62,40,4,5);Events.CulturalIdentityCityConverted.fn(62,40,2);assert(store[key].mappingState=='HELD')
fresh();s.ref.owner=62;s.ref.cityID=40;Events.CityAddedToMap.fn(62,40,4,5);Events.CityRemovedFromMap.fn(62,40);assert(store[key].mappingState=='HELD')
fresh();transfer();s.ref.owner=1;s.ref.cityID=50;Events.CityAddedToMap.fn(1,50,4,5);assert(store[key].mappingState=='HELD')
fresh();GameEvents.CityConquered.fn(62,0,40,4,5);assert(store[key].mappingState=='HELD')
fresh();Events.CityLiberated.fn(0,7);assert(store[key].mappingState=='HELD')
-- Corrupt / concurrent / write-readback failure all stop, never retry each event.
fresh();store[key].revision=99;local w=writes;Events.CityRemovedFromMap.fn(0,7);assert(d.error and writes==w and store[key].revision==99)
fresh();badwrite=true;local w=writes;Events.CityRemovedFromMap.fn(0,7);assert(d.error and writes==w+1);Events.CityRemovedFromMap.fn(0,7);assert(writes==w+1)
fresh();store[key].schema=99;local w=writes;setup();assert(d.error and writes==w)
fresh();transfer();store[key].transition.evidence={};local w=writes;setup(62,40);assert(d.error and writes==w)
fresh();transfer();setup(62,41);assert(store[key].mappingState=='HELD')
-- Missing selection/record read availability is retryable; no old records touched.
store={};setup();assert(d.Begin(0,nil):find('请选择'));assert(not d.error);assert(d.Begin(0,city):find('已建立'))
''')
l.execute(r"""
-- Civ-like missing unpack support: no dependency, including pre-enable callbacks.
table.unpack=nil;unpack=nil;store={};setup()
local w=writes;Events.CityAddedToMap.fn(99,99,20,20);Events.CityTransfered.fn(99,99)
assert(not d.error and writes==w)
assert(d.Begin(0,city):find('已建立'));transfer();assert(store[key].mappingState=='MAPPED_EXPERIMENT')
setup(62,40);assert(d.Describe(0):find('已保存映射恢复'))
fresh();badwrite=true;Events.CityRemovedFromMap.fn(0,7);assert(d.error:find('事件/CityRemovedFromMap'))
store={};setup();badwrite=true;d.Begin(0,city);assert(d.error:find('登记'))
fresh();store[key].schema=99;setup();assert(d.error:find('加载'))
fresh();local get=CityManager.GetCityAt;CityManager.GetCityAt=function()error('injected')end;d.Describe(0);assert(d.error:find('核对'));CityManager.GetCityAt=get
""")
for p in M.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
assert 'P0-B-094.121' in (M/'Probe.lua').read_text()
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='121'
assert sorted(f.text for f in x.findall('./Files/File'))==sorted(str(p.relative_to(M)) for p in M.rglob('*') if p.is_file() and p.suffix!='.modinfo')
assert 'CityIdentityMapping.lua' in [f.text for f in x.findall('./InGameActions/ImportFiles/File')]
g=(M/'Gameplay.lua').read_text();assert 'SPCCityIdentityMapping.Start(P,shared)' in g and 'SPCCityIdentityExperiment.Start(P,shared)' not in g
assert 'shared.InheritanceIsolation=true' in g
allowed={'Mod/'+p for p in ['CityIdentityMapping.lua','Gameplay.lua','Probe.lua','SpecializationP0.modinfo','UI/RuntimeAudit.lua']}
for p in subprocess.check_output(['git','ls-tree','-r','--name-only','d81623f','Mod','Specialization/Design'],cwd=R,text=True).splitlines():
 if p not in allowed:assert (R/p).read_bytes()==subprocess.check_output(['git','show','d81623f:'+p],cwd=R),p
print('LOCAL_SIMULATION_PASS: real Lua automatic mapping/save/cold-load; 10000 duplicates bounded; pending/conflict/failure guards; protected Design and legacy writers unchanged; all Lua syntax/modinfo121.')
