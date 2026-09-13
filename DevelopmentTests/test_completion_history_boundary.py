"""Counterexamples against actual B014 code; synthetic engine, no game writes.
Passing means the authority limitations reproduce, not that formal locking works.
"""
from pathlib import Path
from lupa import LuaRuntime
import json
ROOT=Path(__file__).resolve().parents[1]
CODE=(ROOT/"Sid Meier's Civilization VI/Mods/SpecializationP0/CompletionRecordProbe.lua").read_text()
SETUP='''
print=function() end
local function event()
 local e={fs={}};e.Add=function(f) e.fs[#e.fs+1]=f end
 e.Fire=function(...) for _,f in ipairs(e.fs) do f(...) end end;return e
end
record=nil;attempts=0;dropWrite=false;districtType=1
local city={GetID=function() return 5 end,GetOwner=function() return 0 end,
 GetProperty=function() return record end,SetProperty=function(self,k,v)
 assert(k=="SPC_DEV_COMPLETION_B014");attempts=attempts+1
 if dropWrite then error("SIMULATED_WRITE_LOSS") end;record=v end}
local district={GetID=function() return 70+districtType end,GetOwner=function() return 0 end,
 GetType=function() return districtType end,GetCity=function() return city end,IsComplete=function() return true end}
CityManager={GetDistrictAt=function() return district end};Game={GetCurrentGameTurn=function() return 12 end}
local rows={{Index=1,DistrictType="DISTRICT_CAMPUS"},{Index=2,DistrictType="DISTRICT_THEATER"}}
local P={VERSION="P0-B-014",Families={DISTRICT_CAMPUS="RESEARCH",DISTRICT_THEATER="CULTURE"},
 IsTestPlayer=function(pid) return pid==0 end,Field=function(t,k) return t[k] end,Rows=function() return {} end,
 Info=function(_,key) for _,r in ipairs(rows) do if r.Index==key or r.DistrictType==key then return r end end end}
function boot()
 GameEvents={OnDistrictConstructed=event()};Events={LoadScreenClose=event()}
 local s={BindingProbe={Resolve=function() return "DEV-B013-P0-1","BOUND_MATCH" end}}
 SPCCompletionRecordProbe.Start(P,s);probe=s.CompletionRecordProbe
end
function complete(index) districtType=index;GameEvents.OnDistrictConstructed.Fire(0,index,4,6) end
function ready() Events.LoadScreenClose.Fire() end
function read() return probe.Read(0,city) end
boot()
'''
def scenario(script):
    vm=LuaRuntime(unpack_returned_tuples=True)
    vm.execute(CODE);vm.execute(SETUP);vm.execute(script)
    return dict(vm.globals().record.items()), vm.globals().attempts
# Two different actual histories yield indistinguishable stored observations.
clean,_=scenario('ready();complete(1)')
gap,_=scenario('complete(2);assert(record==nil);ready();complete(1)')
assert clean==gap  # ignored load-phase Culture leaves no persistent history barrier
# Same candidate set, reversed delivery order: no batch identity or tie resolution.
research_first,_=scenario('ready();complete(1);complete(2)')
culture_first,_=scenario('ready();complete(2);complete(1)')
assert research_first['observedFamily']=='RESEARCH'
assert culture_first['observedFamily']=='CULTURE'
# First completion write fails, later success replaces diagnostic error and loses earlier history.
failed_first,n=scenario('ready();dropWrite=true;complete(2);assert(record==nil and probe.players[0].last:find("ERROR"));dropWrite=false;complete(1);assert(probe.players[0].last=="OBSERVATION_SAVED")')
assert failed_first==clean and n==2
# Reload restores observation but cannot add missing history provenance.
restored,_=scenario('ready();complete(1);boot();ready();assert(read():find("OBSERVED_RECORD_MATCH") and probe.players[0].writes==0)')
assert restored==clean
# Reading is never an authority upgrade or a write.
repeated,n=scenario('ready();complete(1);for i=1,5 do read() end')
assert repeated==clean and n==1
print(json.dumps({'verification':'LOCAL_SIMULATION_PASS','scope':'synthetic counterexamples using actual B014 module','checks':[
'different histories / identical observation','reversed delivery changes first observation',
'failed earlier write / later success hides missing history','reload preserves observation only','repeated reads do not write'],
'formal_initialization':'NOT_VALIDATED','runtime_changed':False},ensure_ascii=False))
