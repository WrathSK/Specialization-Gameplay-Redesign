from pathlib import Path
from lupa import LuaRuntime
r=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute((r/'StorageProbe.lua').read_text())
lua.execute('''
print=function() end
local props={};local writes=0
Game={GetProperty=function(self,k) return props[k] end,SetProperty=function(self,k,v) writes=writes+1;props[k]=v end}
local P={VERSION="P0-B-012",IsTestPlayer=function(pid) return pid==0 end}
local shared={};SPCStorageProbe.Start(P,shared)
local run=shared.StorageProbe.Run
assert(run(1,true)=="OUTSIDE_TEST_CIV" and writes==0)
assert(run(0,false):find("EMPTY") and writes==0)
assert(run(0,true):find("MATCH") and writes==1)
assert(run(0,true):find("MATCH_NO_WRITE") and writes==1)
local fresh={};SPCStorageProbe.Start(P,fresh)
assert(fresh.StorageProbe.Run(0,false):find("MATCH") and fresh.StorageProbe.players[0].attempts==0 and writes==1)
props.SPC_DEV_STORAGE_B012_P0.records['sample:beta'].enabled=true
assert(run(0,true):find("MISMATCH_NO_OVERWRITE") and writes==1)
props={}
Game.SetProperty=function(self,k,v) writes=writes+1;props[k]=v;error('after') end
assert(run(0,true):find("MATCH") and shared.StorageProbe.players[0].ack=="THREW_CHECK_READBACK")
Game.GetProperty=function() error('read') end
local before=writes;assert(run(0,true):find("READ_ERROR") and writes==before)
Game.GetProperty=function() return nil end
Game.SetProperty=function() error('before') end
assert(run(0,true):find("WRITE_UNCONFIRMED"))
-- Panel wiring must dispatch without a selected city and leave the payload narrow.
SPCP0=P;P.Scalar=tostring
ExposedMembers={};callbacks={}
Controls=setmetatable({}, {__index=function(t,k) local v={SetText=function() end,SetHide=function() end,
RegisterCallback=function(self,_,fn) callbacks[k]=fn end};rawset(t,k,v);return v end})
ContextPtr={SetInitHandler=function(self,fn) init=fn end,SetHide=function() end,ClearUpdate=function() end,
SetUpdate=function() end,SetShutdown=function() end}
Events={LoadScreenClose={Add=function() end,Remove=function() end}}
Mouse={eLClick=1};include=function() end
Game.GetLocalPlayer=function() return 0 end;Game.GetCurrentGameTurn=function() return 1 end
UI={GetHeadSelectedCity=function() error('NO_CITY_NEEDED') end,RequestPlayerOperation=function(pid,op,args) dispatched=args end}
PlayerOperations={EXECUTE_SCRIPT=1}
''')
lua.execute((r/'UI/P0Panel.lua').read_text())
lua.execute('''
init();callbacks.StorageWriteButton();assert(dispatched.Action=="STORAGE_WRITE" and dispatched.CityID==nil and dispatched.OnStart=="SPC_P0_Request")
callbacks.StorageReadButton();assert(dispatched.Action=="STORAGE_READ")
''')
print('LOCAL_SIMULATION_PASS: B012 table comparison, scoped writes, duplicate no-write, fresh-context reads, mismatch refusal, failed setter/read handling, no-city UI dispatch.')

# Execute the real Gameplay request branch without a selected city / Players lookup.
g=LuaRuntime(unpack_returned_tuples=True)
g.execute((r/'StorageProbe.lua').read_text())
g.execute('''
print=function() end;include=function() end
SPCP0={VERSION="P0-B-012",Scalar=tostring,IsTestPlayer=function(p) return p==0 end,Field=function() return nil end}
ExposedMembers={};Events={}
GameEvents={SPC_P0_Request={Add=function(fn) handle=fn end}}
SPCTradeRouteProbe={Start=function() end};SPCCompletionProbe={Start=function() end};SPCBindingProbe={Start=function() end};SPCCompletionRecordProbe={Start=function() end};SPCCityJournalProbe={Start=function() end}
local props={}
Game={GetProperty=function(self,k) return props[k] end,SetProperty=function(self,k,v) props[k]=v end}
''')
g.execute((r/'Gameplay.lua').read_text())
g.execute('''
handle(0,{Action="STORAGE_WRITE",Token="test"})
assert(ExposedMembers.SPC_P0.LastToken=="test" and ExposedMembers.SPC_P0.Snapshot:find("MATCH"))
handle(0,{Action="STORAGE_READ",Token="read"})
assert(ExposedMembers.SPC_P0.LastToken=="read")
handle(1,{Action="STORAGE_WRITE",Token="other"})
assert(ExposedMembers.SPC_P0.LastToken=="read")
''')
print('LOCAL_SIMULATION_PASS: real Gameplay storage request routing, ACK and foreign-player rejection.')
