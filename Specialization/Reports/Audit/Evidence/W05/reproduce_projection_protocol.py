"""P08a bounded in-memory injections; real Apply/Chair writers and pure models.

No repository writes, batch test runner, database, saves or engine execution.
Default repo is inferred from this audit evidence location; --repo may override it.
JSON is printed deterministically; engine callbacks and EffectiveFacts/DB/depth are stubs.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from lupa.lua55 import LuaRuntime

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[5])
args = parser.parse_args()
root = args.repo.resolve()
read_files = set()

BASE = r'''
local function copy(v)
 if type(v)~='table'then return v end
 local n={};for k,x in pairs(v)do n[k]=copy(x)end;return n
end
SPCDistrictCompleteness={Clone=copy}
Events={};GameEvents={};Game={GetCurrentGameTurn=function()return 20 end}
ExposedMembers={}
metadata={};citizenYields={};chairTargets={{BuildingType='BUILDING_LIBRARY'},{BuildingType='BUILDING_UNIVERSITY'}}
c={owner=0,id=1,token='token:1',active=4,present={},locations={}}
function c:GetOwner()return self.owner end
function c:GetID()return self.id end
function c:GetX()return 10 end
function c:GetY()return 20 end
function c:GetProperty(k)if k=='SPC_DEV_BINDING_B013_TOKEN'then return self.token end end
b={};q={city=c};creates=0;removes=0;reentries=0;createLog={}
function b:HasBuilding(id)return c.present[id]==true end
function b:GetBuildingLocation(id)return c.locations[id]or 7 end
function b:IsPillaged(id)return false end
function b:RemoveBuilding(id)c.present[id]=nil;c.locations[id]=nil;removes=removes+1 end
function q:CreateBuilding(id)
 creates=creates+1
 if mode=='second_create_throws' and creates==2 then error('INJECTED_SECOND_CREATE_FAILURE')end
 c.present[id]=true;c.locations[id]=7
 createLog[#createLog+1]={name=metadata[id].BuildingType,active=c.active,owner=c.owner}
 if mode=='active_drop_reentry' and creates==1 then
  c.active=1;reentries=reentries+1;writer.Audit({player=0})
 end
end
function c:GetBuildings()return b end
function c:GetBuildQueue()return q end
local collection={}
function collection:Members()return ipairs({c})end
function collection:FindID(id)return id==c.id and c or nil end
Players={[0]={GetCities=function()return collection end}}
Map={GetPlotByIndex=function(id)return {GetWorkerCount=function()return 3 end}end}
local first={districtID=1,type='DISTRICT_CAMPUS'}
local depth={validity='VERIFIED',availability='READY',value={
 domains={DISTRICT_CAMPUS={value=3,districtID=1},DISTRICT_INDUSTRIAL_ZONE={value=2,districtID=2},DISTRICT_COMMERCIAL_HUB={value=2,districtID=3}},
 districts={{id=1,type='DISTRICT_CAMPUS',domain='DISTRICT_CAMPUS',plot=7,complete=true,pillaged=false,
  buildings={{type='BUILDING_LIBRARY',ordinary=true,complete=true,pillaged=false,tier=1},
            {type='BUILDING_UNIVERSITY',ordinary=true,complete=true,pillaged=false,tier=2}}}}
}}
shared={EffectiveFacts={Read=function(pid,city)
 assert(pid==city.owner and not city.factsUnknown,'INJECTED_FACTS_UNKNOWN')
 return {specialization='RESEARCH',potential=4,active=city.active,activeStatus='KNOWN',token=city.token,first=first}
end},DistrictCompleteness={Read=function()return copy(depth)end}}
P={Count=function()end,Observe=function()end,IsTestPlayer=function(pid)return pid==0 end,
 Field=function(v,k)return v and v[k]end,
 Info=function(kind,key)if kind=='Buildings'then return metadata[key]end end,
 Rows=function(kind)
  if kind=='Building_CitizenYieldChanges'then return citizenYields end
  if kind=='SPC_ResearchChairTargets'then return chairTargets end
 end,
 HasBuilding=function(object,id)return object:HasBuilding(id)end,
 CreateBuilding=function(object,id)return object:CreateBuilding(id)end,
 RemoveBuilding=function(object,id)return object:RemoveBuilding(id)end}
exits={}
shared.CityProgressionStore={RegisterExit=function(name,fn)exits[name]=fn end,
 RemoveOwned=function(city,loss,names)
  assert(loss.confirmed and city.owner~=0,'INJECTED_EXIT_UNCONFIRMED')
  for _,name in ipairs(names)do local row=assert(metadata[name]);if city.present[row.Index]then b:RemoveBuilding(row.Index)end end
 end}
function addCarrier(name,y,amount)
 local id=#citizenYields+1
 if y==nil then id=1000;while metadata[id]do id=id+1 end end
 local row={Index=id,BuildingType=name,PrereqDistrict='DISTRICT_CAMPUS',InternalOnly=1,CitizenSlots=0,Housing=0}
 metadata[name]=row;metadata[id]=row
 if y then citizenYields[#citizenYields+1]={BuildingType=name,YieldType='YIELD_'..y,YieldChange=amount}end
end
function installedNames()
 local names={};for id,has in pairs(c.present)do if has then names[#names+1]=metadata[id].BuildingType end end
 table.sort(names);return names
end
function errorText()
 return writer.definitionError or writer.errors[0]and writer.errors[0][1]
end
'''

def table_list(value):
    return [value[i] for i in range(1, len(value) + 1)]

def run(module, mode):
    lua = LuaRuntime(unpack_returned_tuples=True)
    loaded = set()
    def include(name):
        if name in loaded:
            return
        loaded.add(name)
        rel = 'Mod/' + name + '.lua'
        read_files.add(rel)
        lua.execute((root / rel).read_text())
    lua.globals().include = include
    lua.execute(BASE)
    include('CurrentSpecializationFacts')
    include(module)
    lua.globals().mode = mode
    if module == 'ResearchApply':
        lua.execute("for _,y in ipairs(SPCResearchApplyModel.Yields)do for i=0,SPCResearchApply.Bits-1 do addCarrier('BUILDING_SPC_RESEARCH_APPLY_'..y..'_'..i,y,2^i)end end")
    else:
        lua.execute("for _,t in ipairs(chairTargets)do for i=0,SPCResearchChair.Bits-1 do addCarrier('BUILDING_SPC_RESEARCH_CHAIR_'..t.BuildingType..'_'..i)end end")
    lua.execute('SPC' + module + '.Start(P,shared);writer=shared.' + module + ';writer.ready=true;writer.Audit({player=0})')
    g = lua.globals()
    first = {
        'active': g.c.active,
        'installed': table_list(g.installedNames()),
        'create_attempts': g.creates,
        'reentrant_audit_calls': g.reentries,
        'busy': g.writer.busy,
        'error': g.errorText(),
        'pending_present': g.writer.pending is not None,
    }
    if mode == 'active_drop_reentry':
        assert first['active'] == 1 and len(first['installed']) == (3 if module == 'ResearchApply' else 4) and first['error'] is None
        assert first['busy'] is False
        assert first['reentrant_audit_calls'] == 1 and not first['pending_present']
        lua.execute("mode='normal';writer.Audit({player=0});assert(#installedNames()==0)")
    elif mode == 'second_create_throws':
        assert first['create_attempts'] == 2 and len(first['installed']) == 1
        assert 'INJECTED_SECOND_CREATE_FAILURE' in first['error']
        lua.execute("mode='normal';writer.Audit({player=0});assert(errorText()==nil)")
    else:
        raise AssertionError(mode)
    if mode == 'second_create_throws':
        assert len(g.installedNames()) == (3 if module == 'ResearchApply' else 4)
    assert g.writer.busy is False
    second = {'active': g.c.active, 'installed': table_list(g.installedNames()), 'error': g.errorText(), 'busy': g.writer.busy}
    return {'module': module, 'injection': mode, 'after_injected_audit': first, 'after_explicit_recovery_audit': second}

results = [run(module, mode) for module in ('ResearchApply', 'ResearchChair')
           for mode in ('active_drop_reentry', 'second_create_throws')]
output = {
    'classification': 'LOCAL_SIMULATION_CONFIRMED_CONDITIONAL_BEHAVIOR',
    'scope': 'Actual unmodified Lua writers, models, RuntimeWork and current-facts facade. In-memory engine/metadata/depth stubs; representative exact carriers (25 Apply, 2 Chair target buildings x 8 bits).',
    'limits': 'Artificial synchronous callback and second-create exception. No claim that these interleavings occur in Civ VI, no native yield or saved-state validation, no repository test suite executed.',
    'results': results,
    'lua_version': LuaRuntime().eval('_VERSION'),
    'fixture_sha256': hashlib.sha256(BASE.encode()).hexdigest(),
    'reproduction_script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'source_sha256': {rel: hashlib.sha256((root / rel).read_bytes()).hexdigest() for rel in sorted(read_files)},
}
print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
