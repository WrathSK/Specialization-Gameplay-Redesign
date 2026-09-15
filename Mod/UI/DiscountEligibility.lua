include('DiagnosticLog')
local print=SPCDiagnosticLog and SPCDiagnosticLog.For('DiscountEligibility') or print
include('Probe')
local P=SPCP0;local busy=false;local seq=0;local hooks={};local generation;local initialized=false
local public={state='LOADED'};ExposedMembers.SPC_DiscountEligibility=public
local pending;local clock=0;local epoch;local last;local retries=0;local retryKey
local sampledKey;local permissionRevision=0
local MAX_SENDS=3;local TIMEOUT=5
local function count(n) if P.Count then P.Count(n) end end
local function reset()
 ExposedMembers.SPC_DiscountClientEpoch=(ExposedMembers.SPC_DiscountClientEpoch or 0)+1
 epoch=ExposedMembers.SPC_DiscountClientEpoch
 ExposedMembers.SPC_DiscountIssued=nil
 pending=nil;last=nil;retryKey=nil;retries=0;seq=0;initialized=false;generation=nil
 sampledKey=nil;permissionRevision=0
 public.pending=0;public.state='RESET'
end
local function transmit(pid,packet,key)
 if retryKey~=key then retryKey=key;retries=0 end
 if retries>=MAX_SENDS then public.state='RETRY_EXHAUSTED';return end
 retries=retries+1;seq=seq+1
 packet.Seq=seq;packet.ClientEpoch=epoch;packet.OnStart='SPC_P0_Request'
 packet.Token=P.VERSION..':discount:'..epoch..':'..seq
 -- Install before invoking engine: synchronous/reentrant callbacks see pending.
 ExposedMembers.SPC_DiscountIssued={ClientEpoch=epoch,Seq=seq,Generation=packet.Generation}
 pending={packet=packet,key=key,time=clock,turn=Game.GetCurrentGameTurn()};public.pending=1
 count('discount_send');if retries>1 then count('discount_retry') end
 local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,packet)
 if not ok then public.error=tostring(err);public.state='SEND_ERROR' end
end
local function refresh()
 count('discount_attempt')
 local shared=ExposedMembers.SPC_P0;local d=shared and shared.StandardizationDiscount
 if busy or not shared or shared.Version~=P.VERSION or not d then return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return end
 if generation~=nil and generation~=d.generation then
  local ack=d.responses and d.responses[pid]
  if pending and ack and ack.ClientEpoch==epoch and ack.Seq==pending.packet.Seq and ack.Generation==pending.packet.Generation then count('discount_ack') end
  -- New gameplay epoch: no old pending, sample signatures or retry budget survive.
  reset()
 end
 generation=d.generation
 if pending then
  local packet=pending.packet;local ack=d.responses and d.responses[pid]
  if ack and ack.ClientEpoch==epoch and ack.Seq==packet.Seq and ack.Generation==packet.Generation then
   count('discount_ack');public.pending=0;pending=nil
   if ack.Status=='ACCEPTED' or ack.Status=='UNCHANGED' then last=retryKey;initialized=true;public.state=ack.Status
   elseif ack.Status=='INITIALIZED' then public.state='INITIALIZED'
   else public.state=ack.Status end
  elseif clock-pending.time<TIMEOUT and Game.GetCurrentGameTurn()==pending.turn then
   count('discount_pending');public.state='PENDING';return
  else
   -- Retire before retry; delayed old sequence cannot finish the next request.
   pending=nil;public.pending=0;ExposedMembers.SPC_DiscountIssued=nil;count('discount_timeout')
  end
 end
 if not d.ready then
  transmit(pid,{Action='DISCOUNT_INIT',Generation=d.generation},'INIT:'..d.generation)
  return
 end
 if not d.plans[pid] then public.state='WAIT_PLAN';return end
 local plan=d.plans[pid];local revision=plan.revision
 -- Scheduling only: pending/ACK/timeout handling above remains the C1 contract.
 local key=generation..':'..revision..':'..Game.GetCurrentGameTurn()..':'..permissionRevision
 if sampledKey==key and ((initialized and last==retryKey) or retries>=MAX_SENDS) then
  count('discount_skipped_clean');return
 end
 sampledKey=key;count('discount_ui_scan');busy=true
 local rows={};local rowCount=0
 local ok,err=pcall(function()
  for cid,buildings in pairs(plan.targets) do
   local c=Players[pid]:GetCities():FindID(cid);assert(c and c:GetOwner()==pid,'DISCOUNT_UI_OWNER')
   for id in pairs(buildings) do
    local b=assert(P.Info('Buildings',id),'DISCOUNT_UI_BUILDING');local args={}
    args[CityCommandTypes.PARAM_BUILDING_TYPE]=b.Hash;args[CityCommandTypes.PARAM_YIELD_TYPE]=P.Info('Yields','YIELD_GOLD').Index
    -- Same enabled-command check as ProductionPanel; affordability is handled separately there.
    local allowed=CityManager.CanStartCommand(c,CityCommandTypes.PURCHASE,false,args,true)
    assert(type(allowed)=='boolean','DISCOUNT_UI_PERMISSION_UNKNOWN')
    rows[#rows+1]=cid..','..b.Index..','..(allowed and '1' or '0');rowCount=rowCount+1
   end
  end
  table.sort(rows)
 end)

 local turn=Game.GetCurrentGameTurn();local payload=ok and table.concat(rows,';') or ''
 local signature=generation..':'..revision..':'..turn..':'..tostring(ok)..':'..payload
 -- Unchanged native permission remains a C1 sample no-op.
 if signature~=last then
  transmit(pid,{Action='DISCOUNT_ELIGIBILITY',Generation=generation,Revision=revision,Turn=turn,
    Valid=ok and 1 or 0,Count=ok and rowCount or 0,Data=payload},signature)
 else count('discount_duplicate') end
 public.count=rowCount;public.error=not ok and tostring(err) or nil
 initialized=initialized or (ok and d.samples[pid]~=nil);busy=false
end
local function safe()
 local ok,err=pcall(refresh)
 if not ok then busy=false;public.state='ERROR';public.error=tostring(err) end
end
local function bind(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f);hooks[#hooks+1]={e,f} end end
ContextPtr:SetInitHandler(function()
 reset()
 for _,n in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','PlayerTurnActivated'}) do bind(n,safe) end
 bind('LoadScreenClose',function() reset();safe() end)
 local function permissionChanged(pid)
  if pid~=Game.GetLocalPlayer() then return end
  permissionRevision=permissionRevision+1;safe()
 end
 for _,n in ipairs({'ResearchCompleted','CivicCompleted','GovernmentChanged','GovernmentPolicyChanged','CityProductionChanged','DistrictAddedToMap','DistrictRemovedFromMap'}) do
  bind(n,permissionChanged)
 end
 local function buildingChanged(x,y,bid,pid)
  local b=P.Info('Buildings',bid)
  if b and b.BuildingType and not b.BuildingType:match('^BUILDING_SPC_') then permissionChanged(pid) end
 end
 bind('BuildingAddedToMap',buildingChanged);bind('BuildingRemovedFromMap',buildingChanged)
 -- Unknown/mod-specific prerequisites are reconciled once on the next turn key.

 bind('SystemUpdateUI',function()
  local shared=ExposedMembers.SPC_P0;local d=shared and shared.StandardizationDiscount
  if pending or not initialized or (d and d.generation~=generation) then safe() end
 end)
 -- Clock only: no scans, requests or logging from the timer. Turn change is fallback.
 ContextPtr:SetUpdate(function(dt) if type(dt)=='number' and dt>=0 then clock=clock+math.min(dt,10) end end)
 safe()
end)
ContextPtr:SetShutdown(function()
 ContextPtr:ClearUpdate();pending=nil;public.pending=0
 if ExposedMembers.SPC_DiscountClientEpoch==epoch then ExposedMembers.SPC_DiscountIssued=nil end
 for _,h in ipairs(hooks) do if h[1].Remove then h[1].Remove(h[2]) end end
 if ExposedMembers.SPC_DiscountEligibility==public then ExposedMembers.SPC_DiscountEligibility=nil end
end)
