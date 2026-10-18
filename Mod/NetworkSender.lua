-- B069: complete content publication, one in-flight request, bounded turn retry.
SPCNetworkSender={}
function SPCNetworkSender.New(P)
 local seq=0;local flight;local lastEpoch;local failedTurn;local lastFailure;local stopped=false
 local function stop(public)
  stopped=true;flight=nil;failedTurn=nil;lastEpoch=nil;lastFailure=nil
  public.awaitingNetwork=false;SPCPerformance.Flight(0)
 end
 local function send(public)
  if stopped then public.awaitingNetwork=false;return end
  local isolation=ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.NetworkIsolation
  if isolation and isolation.active==true and isolation.player==Game.GetLocalPlayer() then stop(public) end
  if stopped then public.awaitingNetwork=false;return end
  local g=ExposedMembers.SPC_P0;local bridge=g and g.NetworkBridge
  if not bridge or not bridge.ready or g.Version~=P.VERSION then public.awaitingNetwork=true;return end
  local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
  local b=bridge.players and bridge.players[pid]
  if bridge.epoch~=lastEpoch then flight=nil;lastEpoch=bridge.epoch;failedTurn=nil;lastFailure=nil;SPCPerformance.Flight(0) end
  if flight then
   if b and b.seq>=flight.seq then
    if flight.valid~=false and (not b.routes or b.fingerprint~=flight.fingerprint or (b.acceptedSeq or -1)<flight.seq) then
     failedTurn=flight.turn;P.Count('send_timeout')
    end
    flight=nil;SPCPerformance.Flight(0)
   elseif Game.GetCurrentGameTurn()==flight.turn then P.Count('send_inflight');return
   else P.Count('send_timeout');flight=nil;SPCPerformance.Flight(0) end
  end
  public.awaitingNetwork=false
  if public.status~='COMPLETE_UI_SHADOW' or not public.snapshot then return end
  local s=public.snapshot
  -- Equal content is a duplicate only after its requested route proof is confirmed.
  if b and b.routes and b.fingerprint==s.fingerprint and s.fingerprint~=nil
   and b.revalidation=='VERIFIED' then P.Count('send_duplicate');return end
  if s.turn~=Game.GetCurrentGameTurn() or s.signal~=(g.RouteSignalRevision or 0) or failedTurn==s.turn then return end
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
   if lastFailure==key then return end
   lastFailure=key
  else lastFailure=nil end
  seq=math.max(seq,b and b.seq or 0)+1
  public.awaitingNetwork=true;flight={seq=seq,turn=s.turn,fingerprint=s.fingerprint,valid=not failure};SPCPerformance.Flight(1);P.Count('net_send')
  local ok=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='NETWORK_PUSH',Token=P.VERSION..':net:'..seq,
    Epoch=bridge.epoch,Seq=seq,Turn=s.turn,Signal=s.signal,Valid=failure and 0 or 1,Failure=failure,
    Count=s.count,WireCount=not failure and s.count+1 or nil,Data=not failure and payload~='' and payload or 'EMPTY'})
  if stopped then public.awaitingNetwork=false;return end
  if not ok then public.awaitingNetwork=false;failedTurn=s.turn;flight=nil;SPCPerformance.Flight(0);P.Count('send_timeout') end
 end
 return send,stop
end
