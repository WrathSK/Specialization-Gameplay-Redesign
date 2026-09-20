-- Independent UI observer. Never requests Gameplay, calls derives, or writes properties.
include('RuntimeAuditCore')
local M=SPCRuntimeAudit
local state={state='WAITING_FOR_COUNTERS',reason=''}
local counterIdentity=nil
local startTime=nil
local function now()
 if type(os)=='table' and type(os.time)=='function' then local ok,n=pcall(os.time);if ok and type(n)=='number' then return n end end
end
local function count(t)
 local n=0;if type(t)=='table' then for _ in pairs(t) do n=n+1 end end;return n
end
local function init()
 local c=ExposedMembers.SPC_Performance
 if not c then return false end
 if c==counterIdentity then return state.state=='ACTIVE' end
 counterIdentity=c;startTime=now()
 local ok,result=pcall(function()
  assert(type(io)=='table' and type(io.open)=='function','FILE_API_UNAVAILABLE')
  assert(type(os)=='table' and type(os.getenv)=='function','HOME_API_UNAVAILABLE')
  local home=os.getenv('HOME');assert(type(home)=='string' and home:sub(1,1)=='/','HOME_UNAVAILABLE')
  -- Current supported platform: macOS native Civ VI log directory. Never create guessed directories.
  local dir=home.."/Library/Application Support/Sid Meier's Civilization VI/Firaxis Games/Sid Meier's Civilization VI/Logs"
  local sink=M.FileSink(io,dir)
  return M.New(c,sink,{build='B082.109',modinfo=109,sourceBase='acf9ba7',start=startTime,turn=Game.GetCurrentGameTurn()})
 end)
 state=ok and result or {state='DISABLED',reason=tostring(result):sub(1,160)}
 ExposedMembers.SPC_RuntimeAudit=state
 return state.state=='ACTIVE'
end
local function finish()
 local ok,why=pcall(function()
  if not init() then return end
  local pid=Game.GetLocalPlayer();if type(pid)~='number' or pid<0 then return end
  local shared=ExposedMembers.SPC_P0 or {};local net=shared.NetworkBridge
  local b=net and net.players and net.players[pid]
  local p=Players[pid];local cities=p and p:GetCities()
  local t=now()
  state.EndTurn(Game.GetCurrentGameTurn(),ExposedMembers.SPC_Performance,{
   elapsed=t and startTime and math.max(0,t-startTime) or 'NA',player=pid,
   cities=cities and cities:GetCount() or 'NA',routes=b and b.routes and #b.routes or 'NA',
   inputRevision=b and b.inputRevision or 'NA',derivedRevision=b and b.derivedRevision or 'NA',
   validity=b and b.validity or 'UNKNOWN',networkPlayers=count(net and net.players),
   networkInputs=(b and b.input) and 1 or 0,diagnosticEntries=count(shared.Events)})
 end)
 if not ok then
  state.state='DISABLED';state.reason=tostring(why):sub(1,160)
  ExposedMembers.SPC_RuntimeAudit=state
 end
end
local function start() local ok,why=pcall(init);if not ok then state.state='DISABLED';state.reason=tostring(why):sub(1,160);ExposedMembers.SPC_RuntimeAudit=state end end
Events.LoadScreenClose.Add(start)
Events.LocalPlayerTurnEnd.Add(finish)
ContextPtr:SetShutdown(function()
 Events.LoadScreenClose.Remove(start);Events.LocalPlayerTurnEnd.Remove(finish)
end)
