-- Finite declared observer edges. Errors never reverse an already committed write.
SPCSafeCallbacks={}
local M=SPCSafeCallbacks
-- An optional scalar trace can fail before any business listener is installed.
function M.OpenTrace(factory,P,role)
 if not factory then return nil end
 local ok,record=pcall(function()
  if factory.ENABLED==false then return nil end
  local trace=factory.New(P,role)
  return trace and trace.Record
 end)
 if ok and type(record)=='function'then return record end
end
-- Production records a failure it caught, so the cause can be investigated.
-- Recording never changes control flow. Probes only read shared.ErrorLog and
-- can be removed without touching production (Owner policy 2026-11-25).
local LOG_CAP=32
function M.Record(shared,label,err)
 local log=shared.ErrorLog
 if log==nil then log={seq=0,entries={}};shared.ErrorLog=log end
 local text=(tostring(err):gsub('[\r\n]+',' ')):sub(1,400)
 for _,e in ipairs(log.entries)do
  if e.label==label and e.text==text then e.count=e.count+1;return end
 end
 log.seq=log.seq+1
 local entries=log.entries;entries[#entries+1]={seq=log.seq,label=label,text=text,count=1}
 if #entries>LOG_CAP then table.remove(entries,1)end
end
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
