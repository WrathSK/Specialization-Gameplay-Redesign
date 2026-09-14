-- B033 bounded test-civ investment. One Gameplay request owns the entire debit.
SPCInvestmentAction={}
function SPCInvestmentAction.Start(P,shared)
 local KEY='SPC_DEV_INVESTMENT_LEDGER_V1';local UNIT_KEY='SPC_DEV_INVESTMENT_UNIT'
 local plans,busy,halted={},{},{}
 local function cp(v) if type(v)~='table' then return v end;local c={};for k,x in pairs(v) do c[k]=cp(x) end;return c end
 local function same(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a) do if not same(v,b[k]) then return false end end
  for k in pairs(b) do if a[k]==nil then return false end end;return true
 end
 local function anchor(f) return {owner=f.owner,cityID=f.cityID,token=f.token,first=cp(f.first),specialization=f.specialization} end
 local function facts(pid,c)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'OWNER_CHANGED')
  return shared.EffectiveFacts.Read(pid,c)
 end
 local function settler(pid,c,id,site)
  assert(type(id)=='number' and id>=0 and id%1==0,'SELECT_SETTLER')
  local u=Players[pid]:GetUnits():FindID(id)
  assert(u and u:GetOwner()==pid,'SETTLER_MISSING_OR_OWNER_CHANGED')
  local info=GameInfo.Units[u:GetType()]
  assert(info and info.UnitType=='UNIT_SETTLER','NOT_A_SETTLER')
  if site then
   local f=facts(pid,c);local found=false
   for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
    local dc=d:GetCity();local di=P.Info('Districts',d:GetType())
    if dc and dc:GetOwner()==pid and dc:GetID()==c:GetID() and f.first and d:GetID()==f.first.districtID
     and di and di.DistrictType==f.first.type and d:IsComplete() and u:GetX()==d:GetX() and u:GetY()==d:GetY() then found=true end
   end
   assert(found,'MOVE_SETTLER_TO_IDENTITY_DISTRICT')
  else assert(u:GetX()==c:GetX() and u:GetY()==c:GetY(),'MOVE_SETTLER_TO_CITY_CENTER') end
  return u
 end
 local function write(pid,c,old,nextValue)
  assert(not halted[pid],'REENTRANT_HELD');facts(pid,c)
  assert(same(c:GetProperty(KEY),old),'STALE_LEDGER')
  P.SetProperty(c,KEY,cp(nextValue))
  assert(not halted[pid] and same(c:GetProperty(KEY),nextValue),'LEDGER_WRITE_UNCONFIRMED')
  if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'InvestmentAction.lua') end
  facts(pid,c) -- same native reader used by Lv1/network validates each state
 end
 local function finish(pid,c,ledger)
  local op=ledger.pending
  assert(op and op.stage=='CONSUMED_CONFIRMED','CONFIRMED_DEBIT_REQUIRED')
  local u=Players[pid]:GetUnits():FindID(op.unitID)
  assert(not u or u:GetProperty(UNIT_KEY)~=op.unitUID,'CONSUMED_UNIT_STILL_PRESENT')
  local nextValue=cp(ledger);nextValue.investments[op.receipt]=op.unitUID
  nextValue.revision=nextValue.revision+1;nextValue.pending=nil
  write(pid,c,ledger,nextValue)
 end
 local data={};shared.InvestmentAction=data
 -- Presentation snapshot only. The existing Prepare/Confirm transaction remains unchanged.
 function data.ReadView(pid,c,id)
  local v={legal=false,prepared=false}
  local ok,err=pcall(function()
   assert(not busy[pid] and not halted[pid],'INVESTMENT_HELD')
   local f=facts(pid,c);assert(f.specialization~='NONE','SPECIALIZATION_REQUIRED')
   settler(pid,c,id,true)
   v.specialization=f.specialization;v.potential=f.potential;v.nextPotential=f.potential+1
   assert(not f.investmentPending,'PENDING_REQUIRES_REVIEW');assert(f.potential<4,'POTENTIAL_CAP_4')
   local u=Players[pid]:GetUnits():FindID(id);assert(u:GetProperty(UNIT_KEY)==nil,'UNIT_ALREADY_RESERVED')
   v.legal=true
   local p=plans[pid]
   v.prepared=p~=nil and p.site and p.owner==pid and p.cityID==c:GetID() and p.unitID==id
    and p.turn==Game.GetCurrentGameTurn() and same(anchor(f),p.anchor)
    and same(c:GetProperty(KEY),p.ledger) and f.potential==p.potential
   if v.prepared then v.planToken=p.token end
  end)
  if not ok then v.reason=tostring(err);v.legal=false;v.prepared=false end
  if not v.prepared and plans[pid] and plans[pid].unitID==id then
   plans[pid]=nil;shared.InvestmentPreview=nil
  end
  return v
 end
 function data.CancelPreview(pid,id)
  if plans[pid] and plans[pid].unitID==id then plans[pid]=nil;shared.InvestmentPreview=nil end
 end
 function data.Prepare(pid,c,unitID,requestToken,site)
  shared.InvestmentPreview=nil;plans[pid]=nil
  local ok,out=pcall(function()
   assert(not busy[pid] and not halted[pid],'INVESTMENT_HELD')
   local f=facts(pid,c);assert(f.specialization~='NONE','SPECIALIZATION_REQUIRED')
   assert(not f.investmentPending,'PENDING_REQUIRES_REVIEW');assert(f.potential<4,'POTENTIAL_CAP_4')
   settler(pid,c,unitID,site)
   local plan={site=site==true,owner=pid,cityID=c:GetID(),unitID=unitID,token=f.token..':R'..(f.investmentCount+1)..':'..requestToken,
    turn=Game.GetCurrentGameTurn(),anchor=anchor(f),potential=f.potential,ledger=cp(c:GetProperty(KEY))}
   plans[pid]=plan
   shared.InvestmentPreview={owner=pid,cityID=plan.cityID,unitID=unitID,token=plan.token}
   return 'B033 PREPARED city='..c:GetID()..' '..f.specialization
    ..'\nPotential '..f.potential..' -> '..(f.potential+1)..' | consume 1 Settler # '..unitID
    ..'\nNo unit consumed yet. Click Confirm investment.'
    ..'\nACTIVE still requires the established governor/title threshold.'
  end)
  return ok and out or ('B033 REJECTED: '..tostring(out))
 end
 function data.Confirm(pid,c,token)
  if busy[pid] then halted[pid]=true;return 'B033 HELD: REENTRANT' end
  busy[pid]=true;local destructive=false
  local ok,out=pcall(function()
   assert(not halted[pid],'INVESTMENT_HELD')
   local f=facts(pid,c);local old=c:GetProperty(KEY)
   if old and old.investments[token] then return 'B033 ALREADY_COMMITTED\n'..shared.EffectiveFacts.Describe(pid,c) end
   local p=plans[pid]
   assert(p and p.token==token and p.owner==pid and p.cityID==c:GetID(),'PREPARE_FIRST')
   assert(p.turn==Game.GetCurrentGameTurn(),'PREVIEW_EXPIRED_PREPARE_AGAIN')
   assert(same(anchor(f),p.anchor) and same(old,p.ledger) and f.potential==p.potential,'PREVIEW_CHANGED_PREPARE_AGAIN')
   assert(not f.investmentPending and f.potential>=1 and f.potential<4,'POTENTIAL_OR_PENDING_CHANGED')
   local u=settler(pid,c,p.unitID,p.site)
   assert(u:GetProperty(UNIT_KEY)==nil,'UNIT_ALREADY_RESERVED')
   local uid=f.token..':'..pid..':'..p.unitID..':'..token
   local intent=old and cp(old) or {schema=1,anchor=anchor(f),revision=1,investments={}}
   intent.pending={stage='INTENT',receipt=token,unitUID=uid,unitID=p.unitID,owner=pid,
    cityUID=f.token,expectedRevision=intent.revision}
   destructive=true;write(pid,c,old,intent)
   u=settler(pid,c,p.unitID,p.site);P.SetProperty(u,UNIT_KEY,uid)
   assert(u:GetProperty(UNIT_KEY)==uid and not halted[pid],'UNIT_RESERVATION_UNCONFIRMED')
   Players[pid]:GetUnits():Destroy(u)
   assert(not Players[pid]:GetUnits():FindID(p.unitID),'UNIT_DEBIT_UNCONFIRMED')
   local confirmed=cp(intent);confirmed.pending.stage='CONSUMED_CONFIRMED';write(pid,c,intent,confirmed)
   finish(pid,c,confirmed)
   plans[pid]=nil
   -- Existing consumers read committed facts; no new Lv2-4 effects are granted.
   return 'B033 INVESTED: consumed 1 Settler\n'..shared.EffectiveFacts.Describe(pid,c)
  end)
  busy[pid]=false
  if not ok and destructive then halted[pid]=true end
  return ok and out or ('B033 '..(destructive and 'HELD' or 'REJECTED')..': '..tostring(out))
 end
 -- Invalidate a prepared unit if it is removed, even if its numeric ID is reused.
 local removed=P.Field(Events,'UnitRemovedFromMap')
 if removed and removed.Add then removed.Add(function(pid,id)
  if plans[pid] and plans[pid].unitID==id then plans[pid]=nil;shared.InvestmentPreview=nil end
 end) end
 local load=P.Field(Events,'LoadScreenClose')
 if load and load.Add then load.Add(function()
  plans={};shared.InvestmentPreview=nil
  for pid,player in pairs(Players) do
   if P.IsTestPlayer(pid) then
    for _,c in player:GetCities():Members() do P.Count('city_scan');
     local ledger=c:GetProperty(KEY)
     if type(ledger)=='table' and ledger.pending then
      local ok,err=pcall(function() facts(pid,c);finish(pid,c,ledger) end)
      if not ok then halted[pid]=true;print('[SPC][B033][RECOVERY_HELD] '..tostring(err)) end
     end
    end
   end
  end
 end) end
end
