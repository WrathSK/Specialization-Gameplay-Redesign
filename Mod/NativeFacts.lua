include('RuntimeWork')
-- Declared native cause owner. No fact values, native handles or persisted state.
SPCNativeFacts={}
function SPCNativeFacts.New(P,shared)
 local d={errors={}};shared.NativeFacts=d
 local function enabled(pid)return P.IsTestPlayer(pid)end
 local function role(scope,cause)
  scope=scope or {}
  local function emit(pid,cid)
   -- A failed queue/observer must never leave an old transaction credential live.
   shared.FactChanges.InvalidateCommitted(pid,cid,{'ACTIVE'})
   shared.FactChanges.Emit({owner=pid,cityID=cid,kinds={'ACTIVE'},cause=cause})
  end
  if scope.player~=nil then
   if enabled(scope.player)then emit(scope.player,scope.city)end
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
 for _,entry in ipairs({{'GovernorAssigned','NATIVE_GOVERNOR_ASSIGNED'},{'GovernorEstablished','NATIVE_GOVERNOR_ESTABLISHED'},
  {'GovernorChanged','NATIVE_GOVERNOR_CHANGED'},{'GovernorPromoted','NATIVE_GOVERNOR_PROMOTED'}})do
  local name,cause=entry[1],entry[2]
  SPCRuntimeWork.TargetHook(P,Events,name,function(scope)
   local ok,err=pcall(role,scope,cause)
   -- Four bounded last-failure slots; a sibling success cannot erase evidence.
   if not ok then local safe,text=pcall(tostring,err);d.errors[name]=safe and text:sub(1,180) or 'NATIVE_ROLE_MARK_FAILED'end
  end)
 end
 return d
end
