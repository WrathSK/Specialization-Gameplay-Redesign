-- D0007 offline qualification snapshot. Not an engine carrier or persisted city fact.
local M={}
local function validPlayer(p) return type(p)=="number" and p>=0 and p<math.huge and p%1==0 end
function M.Resolve(snapshot,player)
 local result={contextSource="MOCK_ONLY",player=player,status="UNKNOWN"}
 if not validPlayer(player) or type(snapshot)~="table" or snapshot.contextSource~="MOCK_ONLY"
  or snapshot.status~="COMPLETE" or type(snapshot.players)~="table" then return result end
 local row=snapshot.players[player]
 if type(row)=="table" and type(row.enabled)=="boolean" then
  result.status=row.enabled and "ENABLED" or "DISABLED"
 end
 return result
end
-- Cheap eligibility inspection precedes any caller-supplied city/network work.
-- An incomplete snapshot dispatches nobody; missing records never imply enabled.
function M.Dispatch(snapshot,visit)
 if type(snapshot)~="table" or snapshot.contextSource~="MOCK_ONLY" or snapshot.status~="COMPLETE"
  or type(snapshot.players)~="table" or type(visit)~="function" then
  return {status="UNKNOWN",visited=0}
 end
 local keys={}
 for p in pairs(snapshot.players) do
  if not validPlayer(p) then return {status="UNKNOWN",visited=0} end
  keys[#keys+1]=p
 end
 table.sort(keys) -- fixture determinism only; does not certify multiplayer timing.
 local count=0
 for _,p in ipairs(keys) do
  local e=M.Resolve(snapshot,p)
  if e.status=="ENABLED" then visit(p,e);count=count+1 end
 end
 return {status="READY",visited=count}
end
return M
