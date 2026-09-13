"""Execute runtime B011 probe + panel with mocks; prohibit gameplay writes."""
from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute((p/'Probe.lua').read_text())
lua.execute((p/'CompletionProbe.lua').read_text())
lua.execute('''
print=function() end
local function ev() return {listeners={},Add=function(fn) end} end
local function event()
 local t={listeners={}};t.Add=function(fn) t.listeners[#t.listeners+1]=fn end
 t.Fire=function(...) for _,fn in ipairs(t.listeners) do fn(...) end end
 return t
end
Events={DistrictAddedToMap=event(),LoadScreenClose=event()}
GameEvents={CityBuilt=event(),OnDistrictConstructed=event()}
Game={GetCurrentGameTurn=function() return 9 end,GetLocalPlayer=function() return 0 end}
PlayerConfigurations={[0]={GetCivilizationTypeName=function() return "CIVILIZATION_SPC_TEST" end,GetLeaderTypeName=function() return "LEADER_SPC_TEST" end}}
local rows={{DistrictType="DISTRICT_CAMPUS",Index=0},{DistrictType="DISTRICT_SEOWON",Index=1}}
SPCP0.Info=function(t,k) for _,r in ipairs(rows) do if k==r.Index or k==r.DistrictType then return r end end end
SPCP0.Rows=function(t) return {{CivUniqueDistrictType="DISTRICT_SEOWON",ReplacesDistrictType="DISTRICT_CAMPUS"}} end
local complete=false
local city={GetID=function() return 65536 end,GetOwner=function() return 0 end,GetName=function() return 'Test City' end,
 SetProperty=function() error("FORBIDDEN_WRITE") end}
local district={GetID=function() return 7 end,GetOwner=function() return 0 end,GetType=function() return 1 end,
 IsComplete=function() return complete end,IsPillaged=function() return false end,GetCity=function() return city end}
CityManager={GetCity=function(p,c) assert(p==0 and c==65536);return city end,GetDistrictAt=function(x,y) assert(x==3 and y==4);return district end}
shared={};SPCCompletionProbe.Start(SPCP0,shared)
assert(shared.CompletionProbe.hooks.OnDistrictConstructed=="REGISTERED")
SPCCompletionProbe.Start(SPCP0,shared);assert(#GameEvents.OnDistrictConstructed.listeners==1)
GameEvents.CityBuilt.Fire(1,1,3,4);assert(shared.CompletionProbe.players[1]==nil)
GameEvents.CityBuilt.Fire(0,65536,3,4)
Events.DistrictAddedToMap.Fire(0,7,65536,3,4,1,99,99,0.4)
local b=shared.CompletionProbe.players[0]
assert(b.built==1 and b.added==1 and b.constructed==0)
assert(b.rows[2].observation=="NOT_COMPLETE" and b.rows[2].family=="RESEARCH")
complete=true;GameEvents.OnDistrictConstructed.Fire(0,1,3,4)
assert(b.constructed==1 and b.rows[3].cityID==65536 and b.rows[3].districtID==7)
assert(b.rows[3].observation=="COMPLETE_OBSERVED" and b.rows[3].rawType==1)
assert(b.rows[3].phase=="BEFORE_LOAD_CLOSE")
Events.LoadScreenClose.Fire();assert(shared.CompletionProbe.phase=="AFTER_LOAD_CLOSE")
Events.DistrictAddedToMap.Fire(0,999,65536,3,4,1);assert(b.rows[#b.rows].observation=="OBJECT_MISMATCH")
district.IsComplete=function() error('GETTER_FAILED') end
GameEvents.OnDistrictConstructed.Fire(0,1,3,4);assert(b.rows[#b.rows].observation=="COMPLETENESS_UNAVAILABLE")
CityManager.GetDistrictAt=function() error('MISSING_OBJECT') end
GameEvents.OnDistrictConstructed.Fire(0,1,3,4);assert(b.errors==1 and b.rows[#b.rows].observation=="READ_ERROR")
for i=1,70 do GameEvents.CityBuilt.Fire(0,65536,3,4) end
assert(#b.rows==64 and b.dropped>0)
-- UI only reads the shared log. No request, clipboard or game state write is needed.
ExposedMembers={SPC_P0={CompletionProbe=shared.CompletionProbe}}
callbacks={};Controls=setmetatable({}, {__index=function(t,k)
 local c={SetText=function(self,s) panelText=s end,SetHide=function() end,
 RegisterCallback=function(self,event,fn) callbacks[k]=fn end};rawset(t,k,c);return c
end})
Mouse={eLClick=1};ContextPtr={SetInitHandler=function(self,fn) initPanel=fn end,SetHide=function() end,
 ClearUpdate=function() end,SetShutdown=function() end}
include=function() end
UI={RequestPlayerOperation=function() error('UI_DISPATCH_FORBIDDEN') end}
''')
lua.execute((p/'UI/P0Panel.lua').read_text())
lua.execute('''
initPanel();local n=shared.CompletionProbe.sequence
callbacks.CompletionButton();assert(panelText:find(SPCP0.VERSION,1,true) and panelText:find("建城="))
callbacks.CompletionNextButton();assert(shared.CompletionProbe.sequence==n)
-- Context recreation makes a fresh memory log; no saved history copied in.
local fresh={};SPCCompletionProbe.Start(SPCP0,fresh);assert(next(fresh.CompletionProbe.players)==nil)
assert(fresh.CompletionProbe.sequence==0)
GameEvents.OnDistrictConstructed=nil;local absent={};SPCCompletionProbe.Start(SPCP0,absent)
assert(absent.CompletionProbe.hooks.OnDistrictConstructed=="ABSENT")
''')
# Scope assertions complement execution: new probe has no writer or operation dispatch.
code=(p/'CompletionProbe.lua').read_text()
for forbidden in ['SetProperty(', 'RequestPlayerOperation(', 'InitUnit(', 'Destroy(', 'ChangePointsTotal(']:
 assert forbidden not in code
print('LOCAL_SIMULATION_PASS: B011 event typing, complete vs added, native family, owner scope, load phase, ring bounds/errors, UI read-only paging and fresh context; no gameplay writes.')
