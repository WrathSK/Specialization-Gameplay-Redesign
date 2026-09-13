from pathlib import Path
import ast
import xml.etree.ElementTree as ET
from lupa import LuaRuntime
P=Path(__file__).resolve().parent;R=P.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
a=ast.parse((P/'test_city_journal_probe.py').read_text())
f=max((n.args[0].value for n in ast.walk(a) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='execute' and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)),key=len)
f=f.replace('local props,gprops={},{}','local flowMode="ok";local props,gprops={},{}')
f=f.replace(' if k==KEY then\n  physicalWrites', ' if k=="SPC_DEV_CITY_FLOW_B020" and flowMode=="drop" then return end\n if k==KEY then\n  physicalWrites',1)
f=f.replace('SPCCityJournalProbe.Start(P,s)','SPCCityJournalProbe.Start(P,s);SPCCityFlowProbe.Start(P,s)')
f+='''
local FLOW="SPC_DEV_CITY_FLOW_B020"
fresh();assert(s.CityFlowProbe.Read(0,city):find("UNTRACKED_NO_WRITE"));found()
assert(props[FLOW].stage=="DONE" and props[FLOW].revision==3 and props[FLOW].facts.specialization=="NONE")
assert(s.CityFlowProbe.players[0].writes==3 and physicalWrites==1)
found();assert(s.CityFlowProbe.players[0].writes==3)
complete(1);assert(props[FLOW].revision==6 and props[FLOW].facts.specialization=="RESEARCH" and s.CityFlowProbe.players[0].writes==6)
complete(2);assert(props[FLOW].facts.specialization=="RESEARCH" and s.CityFlowProbe.players[0].writes==6)
assert(s.CityFlowProbe.Read(0,city):find("LIVE_THIS_LOAD"))
boot();Events.LoadScreenClose.Fire();assert(s.CityFlowProbe.Read(0,city):find("LOAD_READ_ONLY"))
assert(s.CityFlowProbe.players[0].writes==0 and props[FLOW].revision==6)
complete(2);assert(s.CityFlowProbe.players[0].writes==0)
-- Reloading an unassigned city never silently grants continuity permission.
fresh();found();boot();Events.LoadScreenClose.Fire();complete(1)
assert(props[FLOW].facts.specialization=="NONE" and s.CityFlowProbe.players[0].writes==0)
-- B015 remains independent if the new table write fails.
fresh();flowMode="drop";found();assert(props[FLOW]==nil and props[KEY].health=="TRACKING" and s.CityFlowProbe.players[0].halted)
flowMode="ok";complete(1);assert(props[FLOW]==nil and props[KEY].specialization=="RESEARCH")
-- Reversed engine callback order cannot mistake a specialty for NON_V01.
fresh();found();local fs=GameEvents.OnDistrictConstructed.fs;fs[1],fs[2]=fs[2],fs[1]
complete(1);assert(s.CityFlowProbe.players[0].halted and props[FLOW].facts.specialization=="NONE")
-- Invalid record or changed owner is reported, never reset by Read.
fresh();found();props[FLOW].token="wrong";assert(s.CityFlowProbe.Read(0,city):find("READ_ERROR"));assert(s.CityFlowProbe.players[0].writes==3)
fresh();found();owner=1;assert(s.CityFlowProbe.Read(0,city):find("READ_ERROR"));assert(props[FLOW].owner==0)
'''
l=LuaRuntime(unpack_returned_tuples=True)
for name in ['BindingProbe.lua','CityJournalProbe.lua','FreshBindingHook.lua','CityFlowProbe.lua']:l.execute((R/name).read_text())
l.execute(f)
c=LuaRuntime()
for p in R.rglob('*.lua'):c.execute('assert(load(...))',p.read_text())
mod=ET.parse(R/'SpecializationP0.modinfo').getroot();assert mod.attrib['version']=='27' and mod.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for e in mod.findall('.//File'):assert (R/e.text).is_file()
imports=[e.text for e in mod.findall('./InGameActions/ImportFiles/File')];assert all(x in imports for x in ['FreshBindingHook.lua','CityFlowProbe.lua'])
ids=[e.attrib['ID'] for e in ET.parse(R/'UI/P0Panel.xml').iter() if 'ID' in e.attrib];assert len(ids)==len(set(ids)) and 'CityFlowButton' in ids
print('LOCAL_SIMULATION_PASS: actual B013/B015/B020, legacy regression, fresh3/completion6, first lock, loaded read-only, dropped new write isolation, reversed listener order held, corrupt/owner rejection; Lua/XML/manifest. No game execution.')
# Real request handler and panel dispatch, scoped to the new selected-city read action.
g=LuaRuntime(unpack_returned_tuples=True)
g.execute('''print=function() end;include=function() end
SPCP0={VERSION="P0-B-020",IsTestPlayer=function(pid) return pid==0 end,Scalar=tostring}
ExposedMembers={};GameEvents={SPC_P0_Request={Add=function(fn) handle=fn end}}
city={GetOwner=function() return 0 end,GetID=function() return 5 end}
Players={[0]={GetCities=function() return {FindID=function(_,cid) if cid==5 then return city end end} end}}
''')
g.execute((R/'Gameplay.lua').read_text().split('-- Installed HD Gameplay')[0])
g.execute('''ExposedMembers.SPC_P0.CityFlowProbe={Read=function(pid,c) assert(pid==0 and c==city);return "B020_OK" end}
callbacks={};Controls=setmetatable({}, {__index=function(t,k) local v={SetText=function() end,SetHide=function() end,RegisterCallback=function(self,_,fn) callbacks[k]=fn end};rawset(t,k,v);return v end})
ContextPtr={SetInitHandler=function(self,fn) init=fn end,SetHide=function() end,ClearUpdate=function() end,SetUpdate=function() end,SetShutdown=function() end}
Events={LoadScreenClose={Add=function() end,Remove=function() end}};Mouse={eLClick=1}
Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return 1 end}
UI={GetHeadSelectedCity=function() return city end,RequestPlayerOperation=function(pid,op,args) dispatched=args;handle(pid,args) end};PlayerOperations={EXECUTE_SCRIPT=1}
''')
g.execute((R/'UI/P0Panel.lua').read_text());g.execute('''init();callbacks.CityFlowButton();assert(dispatched.Action=="CITY_FLOW_READ" and dispatched.CityID==5);assert(ExposedMembers.SPC_P0.Snapshot=="B020_OK")''')
print('LOCAL_SIMULATION_PASS: real B020 button -> selected-city request -> Gameplay read ACK.')
