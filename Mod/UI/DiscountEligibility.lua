include('DiagnosticLog')
local print=SPCDiagnosticLog and SPCDiagnosticLog.For('DiscountEligibility') or print
-- Background native purchase checks, independent of any open panel.
include('Probe')
local P=SPCP0;local busy=false;local sent;local seq=0;local hooks={};local generation;local initialized=false
local public={state='LOADED'};ExposedMembers.SPC_DiscountEligibility=public
local function refresh()
 local shared=ExposedMembers.SPC_P0;local d=shared and shared.StandardizationDiscount
 if busy or not shared or shared.Version~=P.VERSION or not d then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 if not d.ready then
  -- Background context may initialize after the one-shot gameplay load event.
  busy=true;public.state='REQUEST_INITIALIZATION'
  local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='DISCOUNT_INIT',Token=P.VERSION..':discount:init'})
  busy=false
  if not ok then public.state='INIT_SEND_ERROR';public.error=tostring(err) end
  return
 end
 if not d.plans[pid] then public.state='WAIT_PLAN';return end
 busy=true;local plan=d.plans[pid];local revision=plan.revision;generation=d.generation
 local rows={};local count=0
 local ok,err=pcall(function()
  for cid,buildings in pairs(plan.targets) do
   local c=Players[pid]:GetCities():FindID(cid);assert(c and c:GetOwner()==pid,'DISCOUNT_UI_OWNER')
   for id in pairs(buildings) do
    local b=assert(P.Info('Buildings',id),'DISCOUNT_UI_BUILDING');local args={}
    args[CityCommandTypes.PARAM_BUILDING_TYPE]=b.Hash;args[CityCommandTypes.PARAM_YIELD_TYPE]=P.Info('Yields','YIELD_GOLD').Index
    -- Same enabled-command check as ProductionPanel; affordability is handled separately there.
    local allowed=CityManager.CanStartCommand(c,CityCommandTypes.PURCHASE,false,args,true)
    assert(type(allowed)=='boolean','DISCOUNT_UI_PERMISSION_UNKNOWN')
    rows[#rows+1]=cid..','..b.Index..','..(allowed and '1' or '0');count=count+1
   end
  end
  table.sort(rows)
 end)
 local turn=Game.GetCurrentGameTurn();local payload=ok and table.concat(rows,';') or ''
 local signature=generation..':'..revision..':'..turn..':'..tostring(ok)..':'..payload
 if signature~=sent or (d.seq[pid] or -1)~=seq then
  seq=math.max(seq,d.seq[pid] or 0)+1;local old=sent;sent=signature
  local delivered,why=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='DISCOUNT_ELIGIBILITY',Token=P.VERSION..':discount:'..seq,Seq=seq,Generation=generation,Revision=revision,Turn=turn,Valid=ok and 1 or 0,Count=ok and count or 0,Data=payload})
  if not delivered then sent=old;ok=false;err=why end
 end
 public.state=ok and 'SAMPLED' or 'ERROR';public.count=count
 public.error=not ok and tostring(err) or nil
 initialized=ok and d.samples[pid]~=nil;busy=false
end
local function safe()
 local ok,err=pcall(refresh);if not ok then busy=false;public.state='ERROR';public.error=tostring(err);print('[SPC][B054][UI] '..tostring(err)) end
end
local function bind(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f);hooks[#hooks+1]={e,f} end end
ContextPtr:SetInitHandler(function()
 for _,n in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','PlayerTurnActivated'}) do bind(n,safe) end
 bind('LoadScreenClose',function() sent=nil;initialized=false;safe() end)
 bind('SystemUpdateUI',function()
  local shared=ExposedMembers.SPC_P0;local d=shared and shared.StandardizationDiscount
  if not initialized or (d and d.generation~=generation) then safe() end
 end)
 safe()
end)
ContextPtr:SetShutdown(function() for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end end)
