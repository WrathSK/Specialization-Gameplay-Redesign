-- Explicit bounded scalar batch; does not call Gameplay functions through ExposedMembers.
SPCNetworkSender={}
function SPCNetworkSender.New(P)
 local seq=0;local last
 return function(public)
  local g=ExposedMembers.SPC_P0;local bridge=g and g.NetworkBridge
  if not bridge or not bridge.ready or g.Version~=P.VERSION then return end
  local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
  local signature=bridge.epoch..":"..tostring(public.generation)..":"..public.status..":"..tostring(g.RouteSignalRevision)
  if signature==last then return end
  local s=public.snapshot;local valid=public.status=="COMPLETE_UI_SHADOW" and s and s.count<=128
  local data={}
  if valid then
   for _,key in ipairs(s.keys) do
    local r=s.routes[key];data[#data+1]=table.concat({r.originPlayer,r.originCityID,r.destinationPlayer,r.destinationCityID,r.traderUnitID},",")
   end
  end
  local payload=table.concat(data,";")
  if #payload>16384 then valid=false;payload="" end
  local acknowledged=bridge.players and bridge.players[pid]
  seq=math.max(seq,acknowledged and acknowledged.seq or 0)+1
  local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart="SPC_P0_Request",Action="NETWORK_PUSH",Token=P.VERSION..":net:"..seq,
    Epoch=bridge.epoch,Seq=seq,Turn=valid and s.turn or Game.GetCurrentGameTurn(),Signal=valid and s.signal or (g.RouteSignalRevision or 0),
    Valid=valid and 1 or 0,Count=valid and s.count or 0,Data=payload})
  if ok then last=signature else print("[SPC][B025][SEND_ERROR] "..tostring(err)) end
 end
end
