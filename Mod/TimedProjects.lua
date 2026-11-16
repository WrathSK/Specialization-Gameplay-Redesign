include('TimedProjectModel')
-- Shared technical observation/work sets; no project eligibility or completion policy.
SPCTimedProjects={}
function SPCTimedProjects.Queue(P,city,project,fallback,errors)
 local q=city:GetBuildQueue();local ok,target=P.Call(q,'CurrentlyBuilding')
 assert(ok,errors.read)
 local first=SPCTimedProjectModel.ClassifyQueue(target,nil,project)
 if first=='OTHER'then return q,false,first end
 assert(target==project or target==nil or target=='',errors.read)
 local good,size=P.Call(q,'GetSize')
 if not good then size=fallback(target)end
 local state=SPCTimedProjectModel.ClassifyQueue(target,size,project)
 assert(state~='UNKNOWN',errors.read);assert(state~='MULTIPLE',errors.unique..(errors.appendSize and tostring(size)or ''))
 return q,state=='CURRENT',state
end

-- Session-only pending identities and runnable timers. An UNKNOWN result removes
-- timer work; only a related event or explicit initialization/sync can Wake it.
function SPCTimedProjects.WorkSet(copy)
 local d={};local pending,timing,blocked,recovery={},{},{},{}
 local function key(pid,id)return tostring(pid)..':'..tostring(id)end
 function d.Forget(pid,id)
  local k=key(pid,id);pending[k]=nil;timing[k]=nil;blocked[k]=nil;recovery[k]=nil
 end
 function d.Track(pid,id,stage)
  if stage~='ACTIVE'and stage~='CALLING'and stage~='HELD'then d.Forget(pid,id);return end
  local k=key(pid,id);pending[k]={pid,id}
  timing[k]=stage=='ACTIVE'and not blocked[k]and pending[k]or nil
 end
 function d.Defer(pid,id)timing[key(pid,id)]=nil end
 function d.Block(pid,id)
  local k=key(pid,id);timing[k]=nil;recovery[k]=nil
  if pending[k]then blocked[k]=true end
 end
 function d.Wake(pid,id)
  local k=key(pid,id)
  if blocked[k]then blocked[k]=nil;recovery[k]=pending[k]end
 end
 function d.CanRead(pid,id)return not blocked[key(pid,id)]end
 function d.Runnable(pid,id)return timing[key(pid,id)]~=nil end
 function d.Has(pid,id)return pending[key(pid,id)]~=nil end
 function d.Active()return copy(timing)end
 function d.All()return copy(pending)end
 function d.TakeRecovery()
  local out={};for k,v in pairs(recovery)do if timing[k]then out[k]=v end end
  recovery={} -- consume before any owner/native reentry
  return out
 end
 return d
end
