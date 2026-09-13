from pathlib import Path
from lupa import LuaRuntime
r=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
l.execute((r/'CompletionRecordProbe.lua').read_text())
l.execute('''
print=function() end
local function event() local e={fs={}};e.Add=function(f) e.fs[#e.fs+1]=f end
e.Fire=function(...) for _,f in ipairs(e.fs) do f(...) end end;return e end
local prop=nil;local writes=0;local complete=false;local bound=true;local writeMode="ok"
local city={GetID=function() return 5 end,GetOwner=function() return 0 end,
GetProperty=function() return prop end,SetProperty=function(self,k,v)
 assert(k=="SPC_DEV_COMPLETION_B014");writes=writes+1
 if writeMode=="before" then error('before') end
 prop=v;if writeMode=="after" then error('after') end
end}
local typeID=1
local district={GetID=function() return 7 end,GetOwner=function() return 0 end,GetType=function() return typeID end,
GetCity=function() return city end,IsComplete=function() return complete end}
CityManager={GetDistrictAt=function(x,y) assert(x==4 and y==6);return district end}
Game={GetCurrentGameTurn=function() return 12 end}
local rows={{Index=0,DistrictType="DISTRICT_CITY_CENTER"},{Index=1,DistrictType="DISTRICT_CAMPUS"},
{Index=2,DistrictType="DISTRICT_SEOWON"},{Index=3,DistrictType="DISTRICT_THEATER"}}
local P={VERSION="P0-B-014",Families={DISTRICT_CAMPUS="RESEARCH",DISTRICT_THEATER="CULTURE"},
IsTestPlayer=function(pid) return pid==0 end,Field=function(t,k) return t and t[k] end,
Rows=function() return {{CivUniqueDistrictType="DISTRICT_SEOWON",ReplacesDistrictType="DISTRICT_CAMPUS"}} end,
Info=function(t,k) for _,v in ipairs(rows) do if v.Index==k or v.DistrictType==k then return v end end end}
local function start()
 GameEvents={OnDistrictConstructed=event()};Events={LoadScreenClose=event()}
 local s={BindingProbe={Resolve=function(pid,c) if bound then return "DEV-token","BOUND_MATCH" end return nil,"UNTRACKED_NO_WRITE" end}}
 SPCCompletionRecordProbe.Start(P,s);return s.CompletionRecordProbe
end
local d=start();complete=true;GameEvents.OnDistrictConstructed.Fire(0,1,4,6);assert(writes==0)
Events.LoadScreenClose.Fire();assert(d.Read(0,city):find("NO_OBSERVED_RECORD") and writes==0)
GameEvents.OnDistrictConstructed.Fire(0,0,4,6);assert(writes==0)
complete=false;GameEvents.OnDistrictConstructed.Fire(0,1,4,6);assert(writes==0)
complete=true;bound=false;GameEvents.OnDistrictConstructed.Fire(0,1,4,6);assert(writes==0)
bound=true;GameEvents.OnDistrictConstructed.Fire(1,1,4,6);assert(writes==0)
typeID=2;GameEvents.OnDistrictConstructed.Fire(0,1,4,6);assert(writes==0)
GameEvents.OnDistrictConstructed.Fire(0,2,4,6)
assert(writes==1 and prop.observedFamily=="RESEARCH" and prop.districtType=="DISTRICT_SEOWON")
GameEvents.OnDistrictConstructed.Fire(0,2,4,6);assert(writes==1)
typeID=3;GameEvents.OnDistrictConstructed.Fire(0,3,4,6);assert(writes==1 and prop.observedFamily=="RESEARCH")
assert(d.Read(0,city):find("OBSERVED_RECORD_MATCH"))
d=start();Events.LoadScreenClose.Fire();assert(d.Read(0,city):find("OBSERVED_RECORD_MATCH") and d.players[0].writes==0)
prop.bindingToken="wrong";GameEvents.OnDistrictConstructed.Fire(0,3,4,6)
assert(writes==1 and d.Read(0,city):find("READ_ERROR"))
prop=nil;writeMode="before";GameEvents.OnDistrictConstructed.Fire(0,3,4,6);assert(prop==nil and d.players[0].last:find("ERROR"))
writeMode="after";GameEvents.OnDistrictConstructed.Fire(0,3,4,6)
assert(d.Read(0,city):find("OBSERVED_RECORD_MATCH") and d.players[0].last=="OBSERVATION_SAVED")
''')
print('LOCAL_SIMULATION_PASS: B014 binding gate, completed/type/owner checks, replacement family, non-v01/load ignored, preserved record, context reload, write/read failures. No formal specialization.')
