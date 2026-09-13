"""Offline city facts reducer; no game, runtime writes, or actual Settler consumption."""
from pathlib import Path
import json
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
lua=LuaRuntime(unpack_returned_tuples=True)
lua.globals().State=lua.execute((p/'CitySpecializationState.lua').read_text())
lua.execute('''
id={contextSource="MOCK_ONLY",eligibility={contextSource="MOCK_ONLY",player=0,status="ENABLED"},isTestCivilization=true,present=true,owner=0,cityUID="city-generation-1",freshFoundationObserved=true}
local function fresh() local r=State.NewCity(id);assert(r.status=="READY");return r.facts end
local function batch(family,complete,uid)
 return {status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",owner=0,cityUID=id.cityUID,eventID="event-1",
 districts={{family=family,complete=complete,districtUID=uid or "district-1",mappingStatus="VALIDATED_FAMILY"}}}
end
local f=fresh()
assert(State.Derive(f,id,nil).active==0)
assert(State.Complete(f,id,batch("CAMPUS",false)).facts.specialization==nil)
assert(State.Complete(f,id,batch("NON_V01",true)).facts.specialization==nil)
for family,kind in pairs({CAMPUS="RESEARCH",THEATER_SQUARE="CULTURE",INDUSTRIAL_ZONE="INDUSTRY",COMMERCIAL_HUB="COMMERCE"}) do
 local x=State.Complete(fresh(),id,batch(family,true))
 assert(x.status=="READY" and x.facts.specialization==kind and x.facts.potential==1)
end
local done=State.Complete(f,id,batch("CAMPUS",true));assert(done.changed and f.specialization==nil)
f=done.facts
local rev=f.revision
assert(not State.Complete(f,id,batch("CAMPUS",true)).changed)
assert(State.Complete(f,id,batch("THEATER_SQUARE",true,"district-2")).facts.specialization=="RESEARCH")
assert(f.revision==rev)
local two=batch("CAMPUS",true);two.districts[2]={family="THEATER_SQUARE",complete=true,districtUID="district-2",mappingStatus="VALIDATED_FAMILY"}
assert(State.Complete(fresh(),id,two).facts.specialization=="RESEARCH")
two.districts[1],two.districts[2]=two.districts[2],two.districts[1]
assert(State.Complete(fresh(),id,two).facts.specialization=="CULTURE")
two.orderBasis="SORTED_BY_TYPE";assert(State.Complete(fresh(),id,two).status=="UNKNOWN")
local duplicate=batch("CAMPUS",true);duplicate.districts[2]=duplicate.districts[1]
assert(State.Complete(fresh(),id,duplicate).facts.specialization=="RESEARCH")
local sparse=batch("CAMPUS",true);sparse.districts[3]=sparse.districts[1]
assert(State.Complete(fresh(),id,sparse).status=="UNKNOWN")
local unknown=batch("UNMAPPED_MOD_DISTRICT",true);assert(State.Complete(fresh(),id,unknown).status=="UNKNOWN")
local wrong=batch("CAMPUS",true);wrong.owner=1;assert(State.Complete(fresh(),id,wrong).status=="UNKNOWN")
local function receipt(n)
 return {contextSource="MOCK_ONLY",status="COMMITTED",id="receipt-"..n,unitUID="settler-generation-"..n,
 unitType="SETTLER",unitConsumed=true,cityUID=id.cityUID,owner=0,expectedRevision=n}
end
assert(State.CommitInvestment(fresh(),id,receipt(1)).status=="UNKNOWN")
local unit={contextSource="MOCK_ONLY",owner=0,cityUID=id.cityUID,unitType="SETTLER",present=true,unitUID="settler-generation-1"}
assert(State.PlanInvestment(fresh(),id,unit).status=="UNKNOWN")
for n=1,3 do
 unit.unitUID="settler-generation-"..n
 local plan=State.PlanInvestment(f,id,unit);assert(plan.status=="READY" and not plan.consumed and plan.expectedRevision==f.revision)
 for cap=1,4 do
  local g={owner=0,cityUID=id.cityUID,governorGateStatus="KNOWN",governorLevelCeiling=cap}
  assert(State.Derive(f,id,g).active==math.min(f.potential,cap))
 end
 local stale=receipt(n);stale.expectedRevision=-1;assert(State.CommitInvestment(f,id,stale).status=="UNKNOWN")
 local before=f.potential
 local x=State.CommitInvestment(f,id,receipt(n));assert(x.status=="READY" and x.facts.potential==before+1)
 assert(f.potential==before);f=x.facts
 local repeated=State.CommitInvestment(f,id,receipt(n));assert(not repeated.changed and repeated.facts.revision==f.revision)
end
assert(State.PlanInvestment(f,id,unit).status=="UNKNOWN")
assert(f.potential==4 and State.CommitInvestment(f,id,receipt(4)).status=="UNKNOWN")
local duplicateUnit=receipt(1);duplicateUnit.id="other-receipt";assert(State.CommitInvestment(f,id,duplicateUnit).status=="UNKNOWN")
local conflicting=receipt(1);conflicting.unitUID="other-unit";assert(State.CommitInvestment(f,id,conflicting).status=="UNKNOWN")
local notSpent=receipt(4);notSpent.unitConsumed=false;assert(State.CommitInvestment(f,id,notSpent).status=="UNKNOWN")
local gov={owner=0,cityUID=id.cityUID,governorGateStatus="KNOWN",governorLevelCeiling=1}
for level=1,4 do
 gov.governorLevelCeiling=level;assert(State.Derive(f,id,gov).active==level)
end
-- ACTIVE drop never edits permanent Potential or ledger.
gov.governorLevelCeiling=1;assert(State.Derive(f,id,gov).active==1 and f.potential==4)
gov.governorGateStatus="UNKNOWN";assert(State.Derive(f,id,gov).status=="UNKNOWN")
gov.governorGateStatus="KNOWN";gov.cityUID="other-city";assert(State.Derive(f,id,gov).status=="UNKNOWN")
assert(State.Restore(nil,id).status=="UNKNOWN")
id.owner=1;assert(State.Restore(f,id).status=="UNKNOWN");id.owner=0
id.cityUID="city-generation-2";assert(State.Restore(f,id).status=="UNKNOWN");id.cityUID="city-generation-1"
id.isTestCivilization=false;assert(State.Restore(f,id).status=="READY");id.isTestCivilization=true
id.present=false;assert(State.Restore(f,id).status=="UNKNOWN");id.present=true
id.freshFoundationObserved=false;assert(State.NewCity(id).status=="UNKNOWN");id.freshFoundationObserved=true
local corrupted=State.Restore(f,id).facts;corrupted.potential=3;assert(State.Restore(corrupted,id).status=="UNKNOWN")
corrupted=State.Restore(f,id).facts;corrupted.schemaVersion=99;assert(State.Restore(corrupted,id).status=="UNKNOWN")
local copy=State.Restore(f,id).facts;copy.investments['receipt-1']='mutated';assert(f.investments['receipt-1']~='mutated')
saved=f
''')
def plain(t):
    return {k:plain(v) if hasattr(v,'items') else v for k,v in t.items()}
def table(d):
    return lua.table_from({k:table(v) if isinstance(v,dict) else v for k,v in d.items()})
# Real JSON roundtrip of the permanent facts, then a new Lua VM simulates process recreation.
serialized=json.dumps(plain(lua.globals().saved),sort_keys=True)
new=LuaRuntime(unpack_returned_tuples=True)
new.globals().State=new.execute((p/'CitySpecializationState.lua').read_text())
def newtable(d):
    return new.table_from({k:newtable(v) if isinstance(v,dict) else v for k,v in d.items()})
new.globals().saved=newtable(json.loads(serialized))
new.globals().id=newtable(plain(lua.globals().id))
new.execute('''
saved.active=4 -- cached derived data is deliberately stale and must never be restored.
local restored=State.Restore(saved,id);assert(restored.status=="READY" and restored.facts.active==nil)
local gov={owner=0,cityUID=id.cityUID,governorGateStatus="KNOWN",governorLevelCeiling=1}
local r=State.Derive(restored.facts,id,gov);assert(r.active==1 and r.potential==4)
assert(restored.facts.firstCompletion.eventID=="event-1")
''')
# Bridge existing Probe's actual KNOWN gate output into the offline reducer using fixture UID.
new.execute((p.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0/Probe.lua").read_text())
new.execute('''
PlayerConfigurations={[0]={GetCivilizationTypeName=function() return "CIVILIZATION_SPC_TEST" end,GetLeaderTypeName=function() return "LEADER_SPC_TEST" end}}
local props={SPC_P0_GOV_CONTROL_A007=1}
local city={GetID=function() return 1 end,GetOwner=function() return 0 end,
 GetProperty=function(self,k) return props[k] end,SetProperty=function() error("NO_ENGINE_WRITE") end}
Players={[0]={GetCities=function() return {GetCapitalCity=function() return city end} end}}
local function active()
 local g=SPCP0.CityRoleFacts(city);g.cityUID=id.cityUID -- explicit fixture mapping, not runtime UID implementation
 return State.Derive(saved,id,g)
end
assert(active().active==1) -- absent governor
props.SPC_P0_GOV_PRESENT=1;assert(active().active==1) -- assigned, not established
props.SPC_P0_GOV_ESTABLISHED=1;assert(active().active==1) -- established, title 1
for level=2,4 do props['SPC_P0_GOV_REQ_'..level]=1;assert(active().active==level) end
props.SPC_P0_GOV_REQ_3=0;assert(active().status=="UNKNOWN") -- inconsistent gates
props={SPC_P0_GOV_CONTROL_A007=1,SPC_P0_GOV_REQ_2=0,SPC_P0_GOV_REQ_3=0,SPC_P0_GOV_REQ_4=0}
assert(active().active==1 and saved.potential==4) -- moved away: permanent investment survives
props.SPC_P0_GOV_CONTROL_A007=nil;assert(active().status=="UNKNOWN")
''')
print('LOCAL_SIMULATION_PASS: four v0.1 families; completion lock; immutable facts; receipt replay/cap; ACTIVE/native gates; new-VM save reload; unresolved lifecycle rejection. No engine persistence or Settler action implemented.')
