-- B069: complete content publication, one in-flight request, bounded turn retry.
SPCNetworkSender={}
function SPCNetworkSender.New(P)
 local seq=0;local flight;local lastEpoch;local failedTurn
 return function(public)
  local g=ExposedMembers.SPC_P0;local bridge=g and g.NetworkBridge
  if not bridge or not bridge.ready or g.Version~=P.VERSION then public.awaitingNetwork=true;return end
  local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
  local b=bridge.players and bridge.players[pid]
  if bridge.epoch~=lastEpoch then flight=nil;lastEpoch=bridge.epoch;failedTurn=nil;SPCPerformance.Flight(0) end
  if flight then
   if b and b.seq>=flight.seq then
    if not b.routes or b.fingerprint~=flight.fingerprint then failedTurn=flight.turn;P.Count('send_timeout') end
    flight=nil;SPCPerformance.Flight(0)
   elseif Game.GetCurrentGameTurn()==flight.turn then P.Count('send_inflight');return
   else P.Count('send_timeout');flight=nil;SPCPerformance.Flight(0) end
  end
  public.awaitingNetwork=false
  if public.status~='COMPLETE_UI_SHADOW' or not public.snapshot then return end
  local s=public.snapshot
  if b and b.routes and b.fingerprint==s.fingerprint and s.fingerprint~=nil then P.Count('send_duplicate');return end
  if s.turn~=Game.GetCurrentGameTurn() or s.signal~=(g.RouteSignalRevision or 0) or failedTurn==s.turn then return end
  if s.count>128 then return end
  local data={}
  for _,key in ipairs(s.keys) do local r=s.routes[key]
   data[#data+1]=table.concat({r.originPlayer,r.originCityID,r.destinationPlayer,r.destinationCityID,r.traderUnitID},',')
  end
  local payload=table.concat(data,';');if #payload>16384 then return end
  seq=math.max(seq,b and b.seq or 0)+1
  public.awaitingNetwork=true;flight={seq=seq,turn=s.turn,fingerprint=s.fingerprint};SPCPerformance.Flight(1);P.Count('net_send')
  local ok=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='NETWORK_PUSH',Token=P.VERSION..':net:'..seq,
    Epoch=bridge.epoch,Seq=seq,Turn=s.turn,Signal=s.signal,Valid=1,
    Count=s.count,WireCount=s.count+1,Data=payload~='' and payload or 'EMPTY'})
  if not ok then public.awaitingNetwork=false;failedTurn=s.turn;flight=nil;SPCPerformance.Flight(0);P.Count('send_timeout') end
 end
end
