include('RuntimeWork')
-- Declared native cause owner. No fact values, native handles or persisted state.
SPCNativeFacts={}
function SPCNativeFacts.New(P,shared)
 local d={errors={}};shared.NativeFacts=d
 local function enabled(pid)return P.IsTestPlayer(pid)end
 local function valid(v)return type(v)=='number' and v>=0 and v<2147483648 and v%1==0 end
 local function mark(scope,cause,kind)
  scope=type(scope)=='table' and scope or {}
  local owner=valid(scope.player) and scope.player or nil
  local city=owner and valid(scope.city) and scope.city or nil
  local function emit(pid,cid)
   -- A failed queue/observer must never leave an old transaction credential live.
   shared.FactChanges.InvalidateCommitted(pid,cid,{kind})
   shared.FactChanges.Emit({owner=pid,cityID=cid,kinds={kind},cause=cause})
  end
  if owner~=nil then
   if enabled(owner)then emit(owner,city)end
  else
   -- Existing consumers require an owner. Resolve supported participants once,
   -- never invent player zero or enumerate their cities on a dirty notification.
   local failed,why=false,nil
   for pid in pairs(Players)do
    local ok,err=pcall(function()if enabled(pid)then emit(pid)end end)
    if not ok then failed=true;why=err end
   end
   if failed then error(why or 'NATIVE_ROLE_MARK_FAILED',0)end
  end
 end
 local function guarded(slot,scope,cause,kind)
  local ok,err=pcall(mark,scope,cause,kind)
  if not ok then local safe,text=pcall(tostring,err);d.errors[slot]=safe and text:sub(1,180) or 'NATIVE_FACT_MARK_FAILED'end
  return ok
 end
 function d.Workers(scope,cause)
  assert(cause=='NATIVE_WORKER_CHANGED' or cause=='NATIVE_FOCUS_CHANGED'
   or cause=='UI_WORKERS_DIRTY' or cause=='UI_FACTS_DIRTY','WORKER_CAUSE_UNKNOWN')
  return guarded('WORKERS',scope,cause,'WORKERS')
 end
 SPCRuntimeWork.TargetHook(P,Events,'CityWorkerChanged',function(scope)d.Workers(scope,'NATIVE_WORKER_CHANGED')end)
 local focus=P.Field(Events,'CityFocusChanged')
 if focus and focus.Add then focus.Add(function(pid)
  -- Current evidence establishes the owner, not a narrower second argument.
  local scope={player=valid(pid) and pid or nil}
  if P.Observe then pcall(P.Observe,'dispatch','CityFocusChanged')end
  pcall(SPCRuntimeWork.NoteScope,P,Events,scope)
  d.Workers(scope,'NATIVE_FOCUS_CHANGED')
 end)end
 for _,entry in ipairs({{'GovernorAssigned','NATIVE_GOVERNOR_ASSIGNED'},{'GovernorEstablished','NATIVE_GOVERNOR_ESTABLISHED'},
  {'GovernorChanged','NATIVE_GOVERNOR_CHANGED'},{'GovernorPromoted','NATIVE_GOVERNOR_PROMOTED'}})do
  local name,cause=entry[1],entry[2]
  SPCRuntimeWork.TargetHook(P,Events,name,function(scope)
   guarded(name,scope,cause,'ACTIVE')
  end)
 end
 return d
end
