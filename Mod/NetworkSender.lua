-- B397: complete proof publication, signal-aware deduplication and bounded lifecycle recovery.
SPCNetworkSender={}
function SPCNetworkSender.New(P)
 local result='NOT_STARTED';local seq=0;local flight;local lastEpoch;local failedTurn;local lastFailure;local stopped=false
 local recoveryTurn;local recoveryUsed={}
 local function stop(public)
  stopped=true;flight=nil;failedTurn=nil;lastEpoch=nil;lastFailure=nil;recoveryTurn=nil;recoveryUsed={}
  public.awaitingNetwork=false;public.awaitingTurn=false;SPCPerformance.Flight(0)
 end
 local function send(public,wake)
  if stopped then public.awaitingNetwork=false;result='STOPPED';return end
  local isolation=ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.NetworkIsolation
  if isolation and isolation.active==true and isolation.player==Game.GetLocalPlayer() then stop(public) end
  if stopped then public.awaitingNetwork=false;result='STOPPED';return end
  local g=ExposedMembers.SPC_P0;local bridge=g and g.NetworkBridge
  if not bridge or not bridge.ready or g.Version~=P.VERSION then public.awaitingNetwork=true;result='BRIDGE_WAIT';return end
  local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then result='NOT_OWNER';return end
  local b=bridge.players and bridge.players[pid]
  if bridge.epoch~=lastEpoch then flight=nil;lastEpoch=bridge.epoch;failedTurn=nil;lastFailure=nil;recoveryTurn=nil;recoveryUsed={};SPCPerformance.Flight(0) end
  local turn=Game.GetCurrentGameTurn()
  if recoveryTurn~=turn then recoveryTurn=turn;recoveryUsed={} end
  local lifecycle=wake=='LoadScreenClose' or wake=='LocalPlayerTurnBegin'
  local retry=false
  if flight then
   if b and b.seq>=flight.seq then
    if flight.valid~=false and (not b.routes or b.fingerprint~=flight.fingerprint or (b.acceptedSeq or -1)<flight.seq) then
     failedTurn=flight.turn;P.Count('send_timeout')
    end
    flight=nil;SPCPerformance.Flight(0)
   elseif turn==flight.turn then
    -- Only a new lifecycle witness can replace an unacknowledged request.
    -- Ordinary publish/playback/frame pulses never reopen a flight.
    if lifecycle and not recoveryUsed[wake] then retry=true
    else P.Count('send_inflight');result='IN_FLIGHT';return end
   else P.Count('send_timeout');flight=nil;SPCPerformance.Flight(0) end
  end
  public.awaitingNetwork=false
  if public.status~='COMPLETE_UI_SHADOW' or not public.snapshot then result='SHADOW_WAIT';return end
  local s=public.snapshot
  -- Equal content is a duplicate only after its requested route proof is confirmed.
  if b and b.routes and b.fingerprint==s.fingerprint and s.fingerprint~=nil
   and b.revalidation=='VERIFIED' and b.signal==s.signal
   and s.signal==(g.RouteSignalRevision or 0) then public.awaitingTurn=false;P.Count('send_duplicate');result='DUPLICATE';return end
  if s.turn~=turn or s.signal~=(g.RouteSignalRevision or 0) or failedTurn==s.turn then result=failedTurn==s.turn and 'FAILED_TURN' or 'STALE_SNAPSHOT';return end
  -- A confirmed inactive local turn cannot accept a script operation. Unknown
  -- availability keeps the existing transport attempt, not a readiness claim;
  -- only the unchanged Bridge validation/receipt can confirm proof.
  local activeState='UNAVAILABLE'
  local activeOK,active=pcall(function()return Players[pid]:IsTurnActive()end)
  if activeOK and type(active)=='boolean' then activeState=active and 'YES' or 'NO' end
  if activeState=='NO' then public.awaitingNetwork=flight~=nil;public.awaitingTurn=true;result='TURN_WAIT';return end
  public.awaitingTurn=false
  local failure=s.count>128 and 'NETWORK_ROUTE_LIMIT' or nil
  local data={}
  if not failure then for _,key in ipairs(s.keys) do local r=s.routes[key]
    data[#data+1]=table.concat({r.originPlayer,r.originCityID,r.destinationPlayer,r.destinationCityID,r.traderUnitID},',')
   end
  end
  local payload=table.concat(data,';');if #payload>16384 then failure='NETWORK_PAYLOAD_LIMIT' end
  public.networkFailure=failure
  if failure then
   local key=table.concat({bridge.epoch,s.turn,s.signal,failure,tostring(s.fingerprint),s.count},':')
   if lastFailure==key then result='TRANSPORT_LIMIT';return end
   lastFailure=key
  else lastFailure=nil end
  -- At most one send at each named boundary per epoch/local game turn.
  -- Consume only when issuing an operation; never clear a rejected ACK budget.
  if lifecycle then recoveryUsed[wake]=true end
  if retry then P.Count('send_timeout') end
  seq=math.max(seq,b and b.seq or 0)+1
  public.awaitingNetwork=true;flight={seq=seq,turn=s.turn,fingerprint=s.fingerprint,valid=not failure};SPCPerformance.Flight(1);P.Count('net_send')
  result=failure and 'TRANSPORT_LIMIT' or 'SENT'
  local ok=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='NETWORK_PUSH',Token=P.VERSION..':net:'..seq,
    Epoch=bridge.epoch,Seq=seq,Turn=s.turn,Signal=s.signal,Valid=failure and 0 or 1,Failure=failure,
    Count=s.count,WireCount=not failure and s.count+1 or nil,Data=not failure and payload~='' and payload or 'EMPTY'})
  if stopped then public.awaitingNetwork=false;result='STOPPED';return end
  if not ok then result='SEND_ERROR';public.awaitingNetwork=false;failedTurn=s.turn;flight=nil;SPCPerformance.Flight(0);P.Count('send_timeout') end
 end
 local function observe(public)
  if SPCExpeditionTrainingDiagnostics and not SPCExpeditionTrainingDiagnostics.ENABLED then return end
  public.senderResult=result;public.senderFailedTurn=failedTurn or 'NONE'
  local ok,turn=pcall(Game.GetCurrentGameTurn);public.senderTurn=ok and turn or 'UNAVAILABLE'
  local activeOK,active=pcall(function()return Players[Game.GetLocalPlayer()]:IsTurnActive()end)
  public.senderTurnActive=activeOK and type(active)=='boolean' and (active and 'YES' or 'NO') or 'UNAVAILABLE'
 end
 return function(public,wake)send(public,wake);pcall(observe,public)end,
  function(public)stop(public);result='STOPPED';pcall(observe,public)end
end
