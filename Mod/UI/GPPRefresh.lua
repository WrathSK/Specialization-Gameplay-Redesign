-- Optional/removable transport observations;never used by dirty/retry decisions.
pcall(include,'CultureDiagnostics')
local function cultureObserve(point,build)
 pcall(function()local d=SPCCultureDiagnostics;if d and d.ENABLED then d.Emit('CULTURE_GPP_DIRTY',point,build)end end)
end
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
local workerCity -- one scalar; conflicting/unknown scopes conservatively widen to owner
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
local function validCity(cid)return type(cid)=='number'and cid>=0 and cid<2147483648 and cid%1==0 end
local function retain(onlyWorkers,cid)
 local city=onlyWorkers and validCity(cid)and cid or nil
 if dirty then
  workerOnly=workerOnly and onlyWorkers
  if workerCity~=city then workerCity=nil end
 else workerOnly=onlyWorkers;workerCity=city end
 if not workerOnly then workerCity=nil end
 dirty=true
end
local function mark(onlyWorkers,cid)retain(onlyWorkers,cid);tries=0 end
local function flush()
 if not active or not dirty or busy or tries>=3 then return end
 local g=ExposedMembers.SPC_P0
 if not g or g.Version~=P.VERSION or not g.Lv2GPP or not g.Lv2GPP.ready then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 -- Detach this batch before sending: synchronous callbacks belong to the next batch.
 local sentFacts,sentWorkers,sentCity=factsDirty,workerOnly,workerCity
 busy=true;dirty=false;factsDirty=false;workerOnly=true;workerCity=nil;seq=seq+1;tries=tries+1
 observe('send')
 local packet={OnStart="SPC_P0_Request",Action="LV2_GPP_DIRTY",Token=P.VERSION..":gpp:"..seq,FactsChanged=sentFacts,WorkerOnly=sentWorkers,CityID=sentWorkers and not sentFacts and sentCity or nil}
 cultureObserve('GPP_DIRTY_SEND',function()return {owner=pid,city=packet.CityID,requestKey=packet.Token,observerSide='UI',
  recordType=sentFacts and 'FACTS_AND_WORKERS'or sentWorkers and 'WORKERS_ONLY'or 'CONSERVATIVE'}end)
 local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,packet)
 observe(ok and 'sent' or 'failed')
 cultureObserve('GPP_DIRTY_RETURN',function()return {owner=pid,city=packet.CityID,requestKey=packet.Token,observerSide='UI',
  requestResult=not ok and 'THREW'or err==false and 'FALSE'or err==true and 'TRUE'or err==nil and 'NIL'or 'OTHER'}end)
 if not ok then
  -- Retry the entire failed cause set, merging any callbacks received during send.
  retain(sentWorkers,sentCity);factsDirty=factsDirty or sentFacts
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
 for _,name in ipairs({"CityWorkerChanged","CityFocusChanged"}) do
  bind(name,function(pid,cid)
   local worker=name=='CityWorkerChanged' or name=='CityFocusChanged'
   source(name=='CityWorkerChanged' and 'worker' or 'focus',pid)
   if foreign(pid) then return end
   mark(worker and validPlayer(pid) and pid==Game.GetLocalPlayer(),name=='CityWorkerChanged'and cid or nil)
  end)
 end
 for _,name in ipairs({"LoadScreenClose","PlayerTurnActivated"}) do
  bind(name,function(pid)
   source(name=='LoadScreenClose' and 'load' or 'turn',pid)
   if name=='PlayerTurnActivated' and foreign(pid) then return end
   local t=Game.GetCurrentGameTurn()
   local localTurn=name=='PlayerTurnActivated'and validPlayer(pid)and pid==Game.GetLocalPlayer()
   if lastTurn~=t or busy then lastTurn=t;mark(localTurn);flush()
   elseif dirty and not localTurn then workerOnly=false;workerCity=nil end
   -- A known local turn retains worker recovery, not a new structural D cause.
   -- Load/unknown remains conservative; duplicate turns cannot widen real city work.
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
