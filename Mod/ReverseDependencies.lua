-- Detached relation index only. No native reads, qualification or provenance policy.
SPCReverseDependencies={}
function SPCReverseDependencies.New(targetLimit,edgeLimit)
 targetLimit=targetLimit or 2048;edgeLimit=edgeLimit or 65536
 local targets,reverse={},{ };local targetCount,edgeCount=0,0;local unavailable
 local d={}
 local function id(v)return type(v)=='number'and v>=0 and v<2147483648 and v%1==0 end
 local function key(owner,city)return owner..':'..city end
 local function disable(reason)unavailable=reason;return false,reason end
 function d.Remove(owner,target)
  if not(id(owner)and id(target))then return disable('DEPENDENCY_INDEX_SCOPE')end
  local k=key(owner,target);local old=targets[k]
  if not old then return true end
  for source in pairs(old.sources)do
   local sk=key(owner,source);local row=reverse[sk];row[target]=nil
   if not next(row)then reverse[sk]=nil end
  end
  targetCount=targetCount-1;edgeCount=edgeCount-old.count;targets[k]=nil;return true
 end
 function d.Replace(owner,target,sources)
  if unavailable then return false,unavailable end
  if not(id(owner)and id(target))then return disable('DEPENDENCY_INDEX_SCOPE')end
  if type(sources)~='table'or getmetatable(sources)~=nil then return disable('DEPENDENCY_INDEX_INPUT')end
  -- Values may be false references, empty sets or UNKNOWN provenance. Keys own edges.
  local nextSources={};local count=0
  for source in pairs(sources)do
   if not id(source)then return disable('DEPENDENCY_INDEX_SOURCE')end
   count=count+1;if count>edgeLimit then return disable('DEPENDENCY_INDEX_CAPACITY')end
   nextSources[source]=true
  end
  local k=key(owner,target);local old=targets[k]
  if targetCount+(old and 0 or count>0 and 1 or 0)>targetLimit or edgeCount-(old and old.count or 0)+count>edgeLimit then return disable('DEPENDENCY_INDEX_CAPACITY')end
  -- All validation/capacity checks finish before replacing any old edge.
  d.Remove(owner,target)
  if count>0 then
   targets[k]={sources=nextSources,count=count};targetCount=targetCount+1;edgeCount=edgeCount+count
   for source in pairs(nextSources)do local sk=key(owner,source);reverse[sk]=reverse[sk]or {};reverse[sk][target]=true end
  end
  return true
 end
 function d.Dependents(owner,source)
  if unavailable then return nil,unavailable end
  if not(id(owner)and id(source))then return nil,'DEPENDENCY_INDEX_SCOPE'end
  local out={};for target in pairs(reverse[key(owner,source)]or {})do out[target]=true end;return out
 end
 function d.Stats()return {targets=targetCount,edges=edgeCount,unavailable=unavailable,targetLimit=targetLimit,edgeLimit=edgeLimit}end
 return d
end
