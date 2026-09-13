from pathlib import Path
import ast
import xml.etree.ElementTree as ET
from lupa import LuaRuntime
P=Path(__file__).resolve().parent;R=P.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
a=ast.parse((P/'test_city_journal_probe.py').read_text())
f=max((n.args[0].value for n in ast.walk(a) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='execute' and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)),key=len)
f=f[:f.index('fresh();assert(s.CityJournalProbe.Read')]
f=f.replace('SPCCityJournalProbe.Start(P,s)','SPCCityJournalProbe.Start(P,s);SPCCityFlowProbe.Start(P,s)')
f+='''
local FLOW="SPC_DEV_CITY_FLOW_B020"
fresh();found();assert(props[FLOW].revision==3)
-- Ordinary save/load before first completion, including a placed unfinished district.
dlist[2]=district(1,71);dlist[2].IsComplete=function() return false end
boot();Events.LoadScreenClose.Fire()
assert(not s.CityFlowProbe.players[0].halted and s.CityFlowProbe.players[0].writes==0)
assert(s.CityFlowProbe.Read(0,city):find("RESUMED_NORMAL"))
complete(1);assert(props[FLOW].facts.specialization=="RESEARCH" and props[FLOW].revision==6 and s.CityFlowProbe.players[0].writes==3)
complete(2);assert(s.CityFlowProbe.players[0].writes==3)
boot();Events.LoadScreenClose.Fire();assert(s.CityFlowProbe.Read(0,city):find("RESUMED_NORMAL"))
complete(2);assert(props[FLOW].facts.specialization=="RESEARCH" and s.CityFlowProbe.players[0].writes==0)
-- No existing record: never generate one on load or completion.
fresh();Events.LoadScreenClose.Fire();complete(1);assert(props[FLOW]==nil)
-- Interrupted record remains held, not silently completed.
fresh();found();props[FLOW].stage="TARGET_PENDING";boot();Events.LoadScreenClose.Fire()
assert(s.CityFlowProbe.players[0].halted and s.CityFlowProbe.players[0].writes==0)
assert(props[FLOW].stage=="TARGET_PENDING")
-- Known disagreement, GAP and observable missed completed district are rejected.
fresh();found();props[KEY].revision=99;boot();Events.LoadScreenClose.Fire();assert(s.CityFlowProbe.players[0].halted and s.CityFlowProbe.players[0].writes==0)
fresh();found();props[KEY].health="GAP";props[KEY].gapReason="test";boot();Events.LoadScreenClose.Fire();assert(s.CityFlowProbe.players[0].halted)
fresh();found();dlist[2]=district(1,71);boot();Events.LoadScreenClose.Fire();assert(s.CityFlowProbe.players[0].halted and props[FLOW].facts.specialization=="NONE")
fresh();found();scanError=true;boot();Events.LoadScreenClose.Fire();assert(s.CityFlowProbe.players[0].halted)
fresh();found();props[FLOW].token="wrong";boot();Events.LoadScreenClose.Fire();assert(s.CityFlowProbe.players[0].halted)
'''
l=LuaRuntime(unpack_returned_tuples=True)
for n in ['BindingProbe.lua','CityJournalProbe.lua','FreshBindingHook.lua','CityFlowProbe.lua']:l.execute((R/n).read_text())
l.execute(f)
c=LuaRuntime()
for p in R.rglob('*.lua'):c.execute('assert(load(...))',p.read_text())
m=ET.parse(R/'SpecializationP0.modinfo').getroot();assert m.attrib['version']=='28' and m.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for e in m.findall('.//File'):assert (R/e.text).is_file()
ET.parse(R/'UI/P0Panel.xml')
print('LOCAL_SIMULATION_PASS: actual B021 normal load -> first completion -> second reload; placed district allowed, old/missing state not adopted, PENDING/mismatch/GAP/observable missed completion/scan/binding failure held; no game execution.')
