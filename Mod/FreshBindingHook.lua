-- B020 DEV copy of validated hook candidate; no formal eligibility or city UID.
SPCFreshBindingHook={}
local M=SPCFreshBindingHook
function M.Install(shared,P,observer,context)
 assert(context=="DEV_ONLY","DEV_SCOPE_REQUIRED")
 assert(type(observer)=="function" and not shared.FreshHookCandidate,"OBSERVER_OR_SINGLE_INSTALL")
 local legacy=shared.OnFreshCityBinding
 assert(type(legacy)=="function" and shared.CityJournalProbe and shared.BindingProbe,"INSTALL_AFTER_B015")
 local state={players={}};shared.FreshHookCandidate=state
 local wrapper
 wrapper=function(pid,city)
  local b=state.players[pid] or {count=0};state.players[pid]=b
  if b.busy then b.halted=true;b.reason="REENTRANT_FRESH";return end
  b.busy=true
  -- Preserve legacy invocation, even when the new observer has stopped.
  local journal=shared.CityJournalProbe
  local prior=journal.players[pid];local before=prior and prior.writes or 0
  local ok,err=pcall(legacy,pid,city)
  local function verify()
   assert(ok,err)
   assert(not b.halted and shared.OnFreshCityBinding==wrapper,"HOOK_CHANGED_OR_HALTED")
   assert(P.IsTestPlayer(pid) and journal.phase=="AFTER_LOAD_CLOSE","OUTSIDE_FRESH_PHASE")
   assert(journal.hooks.OnDistrictConstructed=="REGISTERED" and journal.hooks.LoadScreenClose=="REGISTERED","LISTENER_NOT_READY")
   local result=journal.players[pid]
   assert(result and not result.halted and result.last=="FOUNDATION_SAVED" and result.writes==before+1,"LEGACY_FRESH_NOT_CONFIRMED")
   assert(city and city:GetOwner()==pid,"FRESH_OWNER_CHANGED")
   local token,status=shared.BindingProbe.Resolve(pid,city)
   assert(type(token)=="string" and status=="BOUND_MATCH","BINDING_UNCONFIRMED")
   local v=city:GetProperty("SPC_DEV_CITY_JOURNAL_B015")
   assert(type(v)=="table" and v.schema==1 and v.kind=="DEV_FOUNDATION_JOURNAL" and v.owner==pid
    and v.cityID==city:GetID() and v.token==token and v.x==city:GetX() and v.y==city:GetY()
    and v.health=="TRACKING" and v.revision==0 and v.specialization=="NONE" and v.potential==0 and v.first==nil
    and v.foundationTurn==Game.GetCurrentGameTurn(),"FRESH_JOURNAL_MISMATCH")
   assert(not b.halted,"REENTRANT_FRESH")
   -- No inferred proof from old Property alone: this particular legacy call wrote it.
   return {contextSource=context,owner=pid,cityID=v.cityID,token=token,legacyHealth="TRACKING",
    bindingValidated=true,foundationObserved=true,scanStatus="COMPLETE",centerComplete=true,completedV01Count=0}
  end
  local valid,evidence=pcall(verify)
  if valid then
   local delivered,why=pcall(observer,evidence)
   if not delivered or b.halted then b.halted=true;b.reason=tostring(why or "REENTRANT_OBSERVER")
   else b.count=b.count+1;b.reason="FRESH_EVIDENCE_DELIVERED" end
  else b.halted=true;b.reason=tostring(evidence) end
  b.busy=false
 end
 shared.OnFreshCityBinding=wrapper
 return state
end
