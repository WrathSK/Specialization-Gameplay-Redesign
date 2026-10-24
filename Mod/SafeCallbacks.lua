-- Finite declared observer edges. Errors never reverse an already committed write.
SPCSafeCallbacks={}
local M=SPCSafeCallbacks
function M.Call(shared,label,fn,...)
 if type(fn)~='function'then return false,'CALLBACK_ABSENT'end
 local ok,value=pcall(fn,...)
 shared.ObserverErrors=shared.ObserverErrors or {}
 shared.ObserverErrors[label]=not ok and tostring(value) or nil
 return ok,value
end
function M.Notify(shared,name,method,...)
 local d=shared[name]
 if d then return M.Call(shared,name..':'..method,d[method],...)end
 return false,'CONSUMER_ABSENT'
end
function M.Chain(shared,name,fn)
 local prior=shared.OnPermanentCityWrite
 shared.OnPermanentCityWrite=function(c,reason)
  if prior then M.Call(shared,name..':prior',prior,c,reason)end
  M.Call(shared,name..':self',fn,c,reason)
 end
end
