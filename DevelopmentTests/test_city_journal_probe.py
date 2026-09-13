"""Actual B013->B015 callback and gameplay journal under an isolated mock engine."""
from pathlib import Path
from lupa import LuaRuntime
r=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
for file in ['BindingProbe.lua','CityJournalProbe.lua']:l.execute((r/file).read_text())
l.execute('''
print=function() end
local function clone(v) if type(v)~="table" then return v end local r={};for k,x in pairs(v) do r[k]=clone(x) end;return r end
local function event() local e={fs={}};e.Add=function(f) e.fs[#e.fs+1]=f end;e.Fire=function(...) for _,f in ipairs(e.fs) do f(...) end end;return e end
local props,gprops={},{};local owner=0;local mode="ok";local scanError=false;local beforeLoad=false
local KEY="SPC_DEV_CITY_JOURNAL_B015";local dlist={};local s;local current;local physicalWrites=0
local city={GetID=function() return 5 end,GetOwner=function() return owner end,GetX=function() return 4 end,GetY=function() return 6 end,
 GetProperty=function(self,k) return clone(props[k]) end,SetProperty=function(self,k,v)
 if k==KEY then
  physicalWrites=physicalWrites+1
  if mode=="drop" then error("BEFORE_WRITE") end
 end
 props[k]=clone(v)
 if k==KEY and mode=="after" then error("AFTER_WRITE") end
 if k==KEY and mode=="reenter" then mode="ok";GameEvents.OnDistrictConstructed.Fire(0,1,4,6) end
end}
local function district(index,id)
 return {GetCity=function() return city end,GetType=function() return index end,GetID=function() return id end,
 GetOwner=function() return owner end,IsComplete=function() return true end}
end
local rows={{Index=0,DistrictType="DISTRICT_CITY_CENTER"},{Index=1,DistrictType="DISTRICT_CAMPUS"},{Index=2,DistrictType="DISTRICT_THEATER"}}
local P={VERSION="P0-B-015",Families={DISTRICT_CAMPUS="RESEARCH",DISTRICT_THEATER="CULTURE"},
 IsTestPlayer=function(pid) return pid==0 end,Field=function(t,k) return t and t[k] end,Rows=function() return {} end,
 Info=function(_,key) for _,r in ipairs(rows) do if r.Index==key or r.DistrictType==key then return r end end end}
Players={[0]={GetCities=function() return {Members=function() return ipairs({city}) end} end,
 GetDistricts=function() if scanError then error("SCAN_FAILURE") end return {Members=function() return ipairs(dlist) end} end}}
Game={GetCurrentGameTurn=function() return 12 end,GetProperty=function(self,k) return clone(gprops[k]) end,
 SetProperty=function(self,k,v) gprops[k]=clone(v) end}
CityManager={GetCity=function() return city end,GetDistrictAt=function() return current end}
local function boot()
 GameEvents={CityBuilt=event(),OnDistrictConstructed=event()};Events={LoadScreenClose=event()}
 s={};SPCBindingProbe.Start(P,s);SPCCityJournalProbe.Start(P,s)
end
local function fresh()
 props={};gprops={};owner=0;mode="ok";scanError=false;physicalWrites=0
 dlist={district(0,10)};current=dlist[1];boot();Events.LoadScreenClose.Fire()
end
local function found() GameEvents.CityBuilt.Fire(0,5,4,6) end
local function complete(index)
 current=district(index,70+index);GameEvents.OnDistrictConstructed.Fire(0,index,4,6)
end
fresh();assert(s.CityJournalProbe.Read(0,city):find("UNTRACKED_NO_WRITE"));assert(props[KEY]==nil)
found();assert(props[KEY].specialization=="NONE" and props[KEY].potential==0 and physicalWrites==1)
assert(s.BindingProbe.players[0].last=="NEW_CITY_BOUND")
found();assert(physicalWrites==1) -- duplicate foundation callback is NOT fired by binding
complete(1);assert(props[KEY].specialization=="RESEARCH" and props[KEY].potential==1 and physicalWrites==2)
complete(2);complete(1);s.CityJournalProbe.Read(0,city);assert(physicalWrites==2 and props[KEY].specialization=="RESEARCH")
local old=clone(props[KEY]);boot();Events.LoadScreenClose.Fire()
assert(s.CityJournalProbe.players[0].writes==0 and props[KEY].first.districtID==old.first.districtID)
assert(s.CityJournalProbe.Read(0,city):find("RESEARCH"));assert(physicalWrites==2)
-- An old B013 binding without B015 history is never adopted, even on a duplicate CityBuilt.
props[KEY]=nil;found();complete(2);assert(props[KEY]==nil and physicalWrites==2)
-- At foundation a completed specialty, scan error, or absent center refuses qualification.
fresh();dlist[2]=district(1,71);found();assert(props[KEY]==nil and s.CityJournalProbe.players[0].halted)
fresh();scanError=true;found();assert(props[KEY]==nil and s.CityJournalProbe.players[0].halted)
fresh();dlist={};found();assert(props[KEY]==nil)
-- Successful setter with thrown return is accepted by readback.
fresh();mode="after";found();assert(props[KEY].health=="TRACKING" and not s.CityJournalProbe.players[0].halted)
-- Failed completion stops later events; failed GAP persistence is not claimed successful.
fresh();found();mode="drop";complete(2)
assert(s.CityJournalProbe.players[0].halted and s.CityJournalProbe.players[0].last:find("GAP_WRITE_UNCONFIRMED"))
mode="ok";complete(1);assert(props[KEY].specialization=="NONE")
-- Object completeness failure preserves a GAP across reload; it cannot select next type.
fresh();found();current=district(2,72);current.IsComplete=function() return false end
GameEvents.OnDistrictConstructed.Fire(0,2,4,6);assert(props[KEY].health=="GAP")
boot();Events.LoadScreenClose.Fire();complete(1);assert(props[KEY].health=="GAP" and props[KEY].specialization=="NONE")
-- Reentrant completion during writing quarantines the record, even if outer write succeeded.
fresh();found();mode="reenter";complete(1)
assert(s.CityJournalProbe.players[0].halted and props[KEY].health=="GAP")
-- Ownership mismatch retains original record, no silent reset/transfer.
fresh();found();complete(1);owner=1;local before=physicalWrites
assert(s.CityJournalProbe.Read(0,city):find("READ_ERROR"));assert(props[KEY].owner==0 and physicalWrites==before)
-- No completion recorded during loading, nor for another civilization.
fresh();found();boot();complete(1);assert(props[KEY].specialization=="NONE")
Events.LoadScreenClose.Fire();current=district(1,71);GameEvents.OnDistrictConstructed.Fire(1,1,4,6)
assert(props[KEY].specialization=="NONE")
''')
print('LOCAL_SIMULATION_PASS: actual binding callback; fresh qualification; first notification/preservation; reload/no adoption; scan/write failures; persistent GAP; reentrancy stop; owner retention; load/civ gates. No Civ VI execution.')
