include('DiagnosticLog')
local print=SPCDiagnosticLog and SPCDiagnosticLog.For('DialogueRefresh') or print
-- Event-driven collection refresh. Generic UI notifications ONLY drain dirty/ACK state.
include('Probe')
include('DialogueModel')
include('GreatWorkAdjacencyModel')
local P=SPCP0;local busy=false;local dirty=true;local revision=0;local sent;local pending;local seq=0;local hooks={}
local public={scans=0,sends=0,retries=0,state='STARTUP',reason='INITIALIZATION'}
ExposedMembers.SPC_DialogueBackground=public
local function mark(reason)
 dirty=true;revision=revision+1;public.reason=reason
end
-- Empty background contexts do not reliably receive SetUpdate in Civ VI.
-- Generic engine pulses may retransmit the SAME packet at most twice; never scan.
local safe
local function stopRetry() end
local function dispatch(pid,packet)
 public.sends=public.sends+1
 local ok,result=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,packet)
 public.transport=ok and tostring(result) or ('ERROR: '..tostring(result))
 return ok and result~=false
end
local function pulse()
 if pending then
  local s=ExposedMembers.SPC_P0;local pid=Game.GetLocalPlayer()
  if not busy and s and s.Dialogue and (s.Dialogue.seq[pid] or 0)<pending.seq then
   pending.pulses=pending.pulses+1
   if pending.pulses>=3 and pending.retries<2 then
    pending.pulses=0;pending.retries=pending.retries+1;public.retries=public.retries+1
    local flight=pending;busy=true;dispatch(pid,flight.packet);busy=false
    if pending==flight and flight.retries>=2 then public.state='ACK_TIMEOUT' end
   end
  end
 end
 safe()
end
local function refresh()
 local s=ExposedMembers.SPC_P0;local pid=Game.GetLocalPlayer()
 if busy or not s or s.Version~=P.VERSION or not s.Dialogue or not P.IsTestPlayer(pid) then return end
 local turn=Game.GetCurrentGameTurn();local ack=s.Dialogue.seq[pid] or 0
 if pending then
  if ack>=pending.seq then stopRetry();pending=nil;public.state='IDLE'
  elseif turn~=pending.turn then pending=nil;sent=nil;mark('TURN_RETRY')
  elseif dirty and public.state=='ACK_TIMEOUT' then pending=nil;sent=nil
  else if public.state~='ACK_TIMEOUT' then public.state='WAIT_ACK' end;return end
 end
 if not dirty then return end
 busy=true;dirty=false;local thisRevision=revision
 local adjData,adjCount='',0
 local rows,signature={},{};public.scans=public.scans+1
 local ok,why=pcall(function()
  local cities={};for _,c in Players[pid]:GetCities():Members() do P.Count('city_scan'); cities[#cities+1]=c end
  table.sort(cities,function(a,b) return a:GetID()<b:GetID() end)
  for _,c in ipairs(cities) do
   local id=c:GetID();rows[#rows+1]=id..',-1,EMPTY'
   for _,w in ipairs(SPCDialogueModel.Collect(P,c)) do rows[#rows+1]=id..','..w.id..','..w.type end
   local f=s.EffectiveFacts.Read(pid,c);signature[#signature+1]=id..':'..f.specialization..':'..f.active
  end
  if s.GreatWorkAdjacency then
   local aok,adata,acount=pcall(SPCGWAdjacencyModel.Collect,P,pid)
   public.adjacencyError=not aok and tostring(adata) or nil
   if aok then adjData,adjCount=adata,acount else adjData='';adjCount=-1 end
  end
 end)
 local data=ok and table.concat(rows,';') or '';local key=turn..':'..tostring(ok)..':'..data..':'..table.concat(signature,';')..':'..adjData..':'..adjCount
 if sent~=key or not s.Dialogue.ready then
  seq=math.max(seq,ack)+1;sent=key
  -- Set before dispatch: engine callbacks may occur before gameplay acknowledgement.
  local packet={OnStart='SPC_P0_Request',Action='DIALOGUE_SAMPLE',Token=P.VERSION..':dialogue:'..seq,Generation=s.Dialogue.generation,Seq=seq,Turn=turn,Valid=ok and 1 or 0,Data=data,Count=#rows,AdjData=adjData,AdjCount=adjCount}
  pending={seq=seq,turn=turn,generation=s.Dialogue.generation,packet=packet,pulses=0,retries=0};public.state='WAIT_ACK'
  dispatch(pid,packet)
  if (s.Dialogue.seq[pid] or 0)>=seq then pending=nil;public.state='IDLE';stopRetry() end
 else public.state='IDLE' end
 if not ok then public.state='COLLECT_ERROR';print('[SPC][B059][COLLECT] '..tostring(why)) end
 if revision~=thisRevision then dirty=true end
 busy=false
end
safe=function() local ok,err=pcall(refresh);if not ok then busy=false;public.state='ERROR';print('[SPC][B059][UI] '..tostring(err)) end end
local function bind(name,fn)
 local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
end
ContextPtr:SetInitHandler(function()
 -- These events describe collection/city/eligibility changes, not our own yield refreshes.
 for _,name in ipairs({'GreatWorkCreated','GreatWorkMoved','CityAddedToMap','CityRemovedFromMap','CityTransfered','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','PlayerTurnActivated','DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap','FeatureAddedToMap','CityTileOwnershipChanged'}) do
  local reason=name;bind(name,function() mark(reason) end)
 end
 bind('LoadScreenClose',function() mark('LOAD_SCREEN_CLOSE');safe() end)
 for _,name in ipairs({'SystemUpdateUI','GameCoreEventPublishComplete','GameCoreEventPlaybackComplete'}) do bind(name,pulse) end
 safe()
end)
ContextPtr:SetShutdown(function()
 stopRetry()
 for _,h in ipairs(hooks) do if h.event.Remove then h.event.Remove(h.fn) end end
 if ExposedMembers.SPC_DialogueBackground==public then ExposedMembers.SPC_DialogueBackground=nil end
end)
