include('TimedProjectModel')
-- Synchronous per-call observation; no controller policy, lifecycle or retries.
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
