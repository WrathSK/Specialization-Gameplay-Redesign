"""Audit-only bounded retention fixture; actual GreatWorkFacts, mocked native API.
No gameplay test suite, native GC, external files, Property or carrier writes.
"""
import argparse
import hashlib
import json
from pathlib import Path
from lupa.lua55 import LuaRuntime

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
source = a.repo / 'Mod/GreatWorkFacts.lua'
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
include=function()end
function event()
 local fs={};return {Add=function(f)fs[#fs+1]=f end,
 Remove=function(f)for i=#fs,1,-1 do if fs[i]==f then table.remove(fs,i)end end end,
 Fire=function(...)for _,f in ipairs(fs)do f(...)end end}
end
Events={CityAddedToMap=event(),CityRemovedFromMap=event(),GreatWorkMoved=event(),GreatWorkCreated=event()}
ExposedMembers={};Game={GetCurrentGameTurn=function()return 40 end}
P={IsTestPlayer=function(pid)return pid==0 end,Field=function(t,k)return t and t[k]end}
SPCGreatWorkCatalog={Build=function()return {count=0,works={},excluded={},complete=true}end}
Players={[0]={GetCities=function()return {Members=function()return function()return nil end end}end}}
shared={}
function count(t)local n=0;for _ in pairs(t)do n=n+1 end;return n end
''')
lua.execute(source.read_text())
lua.execute('''
d=SPCGreatWorkFacts.Start(P,shared)
for cid=1,8 do Events.CityAddedToMap.Fire(0,cid);Events.CityRemovedFromMap.Fire(0,cid)end
marked=count(d.dirtyScope.cities);assert(marked==8)
for cid=1,8 do Events.CityRemovedFromMap.Fire(0,cid)end
Events.CityRemovedFromMap.Fire(1,99)
deduplicated=count(d.dirtyScope.cities);assert(deduplicated==8)
local ok,why=d.Receive(0,{FactsEpoch=d.epoch,Seq=1,Turn=40,FactsInput=d.inputRevision,FactsRefs='',FactsData={}})
assert(not ok and why=='GW_SAMPLE_SIZE');failureReason=why
failed=count(d.dirtyScope.cities);assert(failed==8)
d.Reset();afterReset=count(d.dirtyScope.cities);assert(afterReset==8)
local accepted=d.Receive(0,{FactsEpoch=d.epoch,Seq=1,Turn=40,FactsInput=d.inputRevision,
 FactsRefs='',FactsData='',FactsCount=0,FactsCities=0})
assert(accepted and d.state=='VERIFIED')
afterAccepted=count(d.dirtyScope.cities);assert(afterAccepted==0)
''')
result = {
 'scope':'LOCAL_STRUCTURAL_REPRODUCTION; not Civ VI VM, native memory or native event evidence',
 'source':{'Mod/GreatWorkFacts.lua': hashlib.sha256(source.read_bytes()).hexdigest()},
 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'lua_version':lua.eval('_VERSION'),
 'fixture': 'Eight synthetic local city IDs added then removed; current native city collection is empty. Catalog, Events, player scope and native collection are stubs. Actual source Start/handlers/Receive/Reset execute unchanged.',
 'dirty_keys':{k:int(lua.eval(k)) for k in ('marked','deduplicated','failed','afterReset','afterAccepted')},
 'failure_reason':lua.eval('failureReason'),
 'limits':'No historical gameplay tests executed; no allocation measurement, process/native GC, current-save frequency or all-module lifecycle claim.'
}
a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
