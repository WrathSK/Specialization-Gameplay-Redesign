from pathlib import Path
from lupa import LuaRuntime
r=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute((r/'BindingProbe.lua').read_text())
lua.execute('''
print=function() end
local function event()
 local e={callbacks={}};e.Add=function(fn) e.callbacks[#e.callbacks+1]=fn end
 e.Fire=function(...) for _,f in ipairs(e.callbacks) do f(...) end end;return e
end
local function copy(v) if type(v)~="table" then return v end local t={} for k,x in pairs(v) do t[k]=copy(x) end return t end
local props={};local cities={};local mode="ok"
local function city(id)
 local c={id=id,owner=0,props={}}
 c.GetID=function(self) return self.id end;c.GetOwner=function(self) return self.owner end
 c.GetX=function() return id end;c.GetY=function() return 1 end
 c.GetProperty=function(self,k) return self.props[k] end
 c.SetProperty=function(self,k,v) if mode=="city_fail" then error('fail city') end self.props[k]=v end
 cities[id]=c;return c
end
Game={GetProperty=function(self,k) return props[k] end,SetProperty=function(self,k,v)
 if mode=="game_fail" then error('fail game') end
 props[k]=copy(v)
 if mode=="after_write" then error('lost ack') end
end}
Players={[0]={GetCities=function() return {Members=function() return pairs(cities) end} end}}
CityManager={GetCity=function(pid,cid) return cities[cid] end}
local P={VERSION="P0-B-013",Field=function(t,k) return t and t[k] end,IsTestPlayer=function(pid) return pid==0 end}
local function start()
 GameEvents={CityBuilt=event()};Events={LoadScreenClose=event()}
 local shared={};SPCBindingProbe.Start(P,shared);return shared.BindingProbe
end
local old=city(1);local d=start()
GameEvents.CityBuilt.Fire(0,1,1,1)
assert(next(props)==nil and next(old.props)==nil)
Events.LoadScreenClose.Fire();assert(d.Read(0,old):find("UNTRACKED_NO_WRITE"))
local c=city(2);GameEvents.CityBuilt.Fire(0,2,2,1)
assert(d.Read(0,c):find("BOUND_MATCH") and d.players[0].gameWrites==2 and d.players[0].cityWrites==1)
local token=c.props.SPC_DEV_BINDING_B013_TOKEN
GameEvents.CityBuilt.Fire(0,2,2,1)
assert(d.players[0].gameWrites==2 and d.players[0].cityWrites==1 and d.players[0].last=="DUPLICATE_NO_WRITE")
local c2=city(3);mode="after_write";GameEvents.CityBuilt.Fire(0,3,3,1);mode="ok"
assert(d.Read(0,c2):find("BOUND_MATCH") and c2.props.SPC_DEV_BINDING_B013_TOKEN~=token)
d=start();Events.LoadScreenClose.Fire()
assert(d.Read(0,c):find("BOUND_MATCH") and d.players[0].gameWrites==0 and d.players[0].cityWrites==0)
assert(next(old.props)==nil)
local c3=city(4);mode="city_fail";GameEvents.CityBuilt.Fire(0,4,4,1);mode="ok"
assert(d.Read(0,c3):find("PARTIAL_NO_REPAIR"))
local gw,cw=d.players[0].gameWrites,d.players[0].cityWrites
GameEvents.CityBuilt.Fire(0,4,4,1)
assert(d.players[0].gameWrites==gw and d.players[0].cityWrites==cw)
local reused=city(2);GameEvents.CityBuilt.Fire(0,2,2,1)
assert(d.Read(0,reused):find("PARTIAL_NO_REPAIR") and next(reused.props)==nil)
local c4=city(5);mode="game_fail";GameEvents.CityBuilt.Fire(0,5,5,1);mode="ok"
assert(next(c4.props)==nil)
local c5=city(6);GameEvents.CityBuilt.Fire(1,6,6,1);assert(next(c5.props)==nil)
local before=d.players[0].gameWrites;GameEvents.CityBuilt.Fire(0,6,99,1)
assert(d.players[0].gameWrites==before and next(c5.props)==nil)
props.SPC_DEV_BINDING_B013_P0=nil
GameEvents.CityBuilt.Fire(0,6,6,1)
assert(d.players[0].last:find("TOKEN_WITHOUT_LEDGER") and next(c5.props)==nil)
''')
print('LOCAL_SIMULATION_PASS: B013 live foundation, old/load no writes, distinct tokens, repeated event, fresh-context audit, partial failure/reused reference refusal, failed/lost-ack writes, civ/event guards.')
