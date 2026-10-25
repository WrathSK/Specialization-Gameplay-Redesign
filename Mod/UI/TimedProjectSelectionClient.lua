-- One explicit intent-read gate, shared by the three independent project UIs.
-- No native listeners, clock retries, save authority or project eligibility here.
SPCTimedProjectSelectionClient={}
function SPCTimedProjectSelectionClient.New(P,pending)
 local d={};local closed,draining=false,false
 function d.QueueEvent(pid,id)
  if closed or type(pid)~='number' or type(id)~='number'then return end
  local p=pending[pid..':'..id]
  if p and not p.sent and p.turn==Game.GetCurrentGameTurn()and P.IsTestPlayer(pid)then p.read=true end
 end
 function d.Read(k,p,read)
  if closed or not p.read then return false,nil,false end
  p.read=nil -- consume before the getter; a new event can permit the next drain
  local ok,value=pcall(read)
  return ok,value,not closed and not p.read and pending[k]==p and p.turn==Game.GetCurrentGameTurn()
 end
 function d.Bind(fn)
  return function()
   if closed or draining then return end;draining=true
   local ok,value=pcall(fn);draining=false
   if not ok then error(value,0)end;return value
  end
 end
 function d.Close()closed=true;for k in pairs(pending)do pending[k]=nil end end
 return d
end
