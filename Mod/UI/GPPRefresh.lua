include('DiagnosticLog')
local print=SPCDiagnosticLog and SPCDiagnosticLog.For('GPPRefresh') or print
-- Background dirty notification only. Never sends worker counts, yields or city facts.
include("Probe")
local P=SPCP0
local active=false
local dirty=true
local busy=false
local seq=0
local hooks={}
local function mark() dirty=true end
local function flush()
 if not active or not dirty or busy then return end
 local g=ExposedMembers.SPC_P0
 if not g or g.Version~=P.VERSION or not g.Lv2GPP or not g.Lv2GPP.ready then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 busy=true;dirty=false;seq=seq+1
 local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
  {OnStart="SPC_P0_Request",Action="LV2_GPP_DIRTY",Token=P.VERSION..":gpp:"..seq})
 if not ok then dirty=true;print("[SPC][B035][GPP_SEND_ERROR] "..tostring(err)) end
 busy=false
end
local function bind(name,fn)
 local e=P.Field(Events,name)
 if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
end
ContextPtr:SetInitHandler(function()
 if active then return end;active=true
 for _,name in ipairs({"CityWorkerChanged","CityFocusChanged","GovernorAssigned","GovernorChanged","GovernorEstablished","GovernorPromoted"}) do bind(name,mark) end
 for _,name in ipairs({"LoadScreenClose","PlayerTurnActivated","PlayerTurnDeactivated"}) do bind(name,function() mark();flush() end) end
 for _,name in ipairs({"GameCoreEventPublishComplete","GameCoreEventPlaybackComplete","SystemUpdateUI"}) do bind(name,flush) end
 flush()
end)
ContextPtr:SetShutdown(function()
 active=false
 for _,h in ipairs(hooks) do if h.event.Remove then h.event.Remove(h.fn) end end
 hooks={}
end)
