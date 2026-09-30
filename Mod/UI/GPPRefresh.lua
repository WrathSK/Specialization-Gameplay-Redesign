include('DiagnosticLog')
local print=SPCDiagnosticLog and SPCDiagnosticLog.For('GPPRefresh') or print
-- Background dirty notification only. Never sends worker counts, yields or city facts.
include("Probe")
local P=SPCP0
local active=false
local dirty=true
local busy=false
local seq=0;local tries=0;local lastTurn;local factsDirty=true
local workerOnly=false -- initial batch is conservative; true requires positive local provenance
local hooks={}
local function observe(key) if P.Observe then P.Observe('ui',key) end end
local function source(name,pid)
 if name=='load' then pid=nil end
 local owner=type(pid)=='number' and pid>=0 and (pid==Game.GetLocalPlayer() and 'local' or 'foreign') or 'unknown'
 observe(name..'_'..owner)
end
-- Known foreign events cannot change this local player's GPP/support facts.
-- Missing/invalid owner metadata remains conservative; never guess player zero.
local function validPlayer(pid)
 return type(pid)=='number' and pid>=0 and pid%1==0
end
local function foreign(pid)
 local localPlayer=Game.GetLocalPlayer()
 return validPlayer(pid) and validPlayer(localPlayer) and pid~=localPlayer
end
local function mark(onlyWorkers)
 if dirty then workerOnly=workerOnly and onlyWorkers else workerOnly=onlyWorkers end
 dirty=true;tries=0
end
local function flush()
 if not active or not dirty or busy or tries>=3 then return end
 local g=ExposedMembers.SPC_P0
 if not g or g.Version~=P.VERSION or not g.Lv2GPP or not g.Lv2GPP.ready then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 -- Detach this batch before sending: synchronous callbacks belong to the next batch.
 local sentFacts,sentWorkers=factsDirty,workerOnly
 busy=true;dirty=false;factsDirty=false;workerOnly=true;seq=seq+1;tries=tries+1
 observe('send')
 local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
  {OnStart="SPC_P0_Request",Action="LV2_GPP_DIRTY",Token=P.VERSION..":gpp:"..seq,FactsChanged=sentFacts,WorkerOnly=sentWorkers})
 observe(ok and 'sent' or 'failed')
 if not ok then
  -- Retry the entire failed cause set, merging any callbacks received during send.
  dirty=true;factsDirty=factsDirty or sentFacts;workerOnly=workerOnly and sentWorkers
  print("[SPC][B035][GPP_SEND_ERROR] "..tostring(err))
 end
 busy=false
end
local function bind(name,fn)
 local e=P.Field(Events,name)
 if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
end
ContextPtr:SetInitHandler(function()
 if active then return end;active=true
 for _,name in ipairs({"CityWorkerChanged","CityFocusChanged","GovernorAssigned","GovernorChanged","GovernorEstablished","GovernorPromoted"}) do
  bind(name,function(pid)
   local worker=name=='CityWorkerChanged' or name=='CityFocusChanged'
   source(worker and (name=='CityWorkerChanged' and 'worker' or 'focus') or 'governor',pid)
   if foreign(pid) then return end
   if not worker then factsDirty=true end
   mark(worker and validPlayer(pid) and pid==Game.GetLocalPlayer())
  end)
 end
 for _,name in ipairs({"LoadScreenClose","PlayerTurnActivated"}) do
  bind(name,function(pid)
   source(name=='LoadScreenClose' and 'load' or 'turn',pid)
   if name=='PlayerTurnActivated' and foreign(pid) then return end
   local t=Game.GetCurrentGameTurn()
   if lastTurn~=t or busy then lastTurn=t;mark(false);flush()
   elseif dirty then workerOnly=false end -- duplicate turn/load must not bless pending workers
  end)
 end
 for _,name in ipairs({"GameCoreEventPublishComplete","GameCoreEventPlaybackComplete","SystemUpdateUI"}) do bind(name,flush) end
 flush()
end)
ContextPtr:SetShutdown(function()
 active=false
 for _,h in ipairs(hooks) do if h.event.Remove then h.event.Remove(h.fn) end end
 hooks={}
end)
