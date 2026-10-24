-- AV2-A: accepted logical inputs, not a shared derived-result cache or save ledger.
SPCNetworkInput={}
local N=SPCNetworkInput
local function atom(v)
 local s=type(v)..':'..(type(v)=='number' and string.format('%.17g',v) or tostring(v));return #s..':'..s
end
function N.Reference(c)
 local owner,id,x,y,token=c:GetOwner(),c:GetID(),c:GetX(),c:GetY(),c:GetProperty('SPC_DEV_BINDING_B013_TOKEN')
 for _,v in ipairs({owner,id,x,y})do assert(type(v)=='number' and v>=0 and v%1==0,'NETWORK_REFERENCE_UNAVAILABLE')end
 assert(type(owner)=='number' and type(id)=='number' and type(x)=='number' and type(y)=='number','NETWORK_REFERENCE_UNAVAILABLE')
 return table.concat({atom(owner),atom(id),atom(x),atom(y),atom(token)})
end
function N.Signature(input)
 local parts={atom(input.validity),atom(input.routeSignature),atom(input.capital),atom(input.kResearch),atom(input.kCulture)}
 local ids={};for id in pairs(input.cities) do ids[#ids+1]=id end;table.sort(ids)
 for _,id in ipairs(ids) do local f=input.cities[id]
  parts[#parts+1]=table.concat({atom(id),atom(f.reference),atom(f.token),atom(f.specialization),atom(f.potential),
   atom(f.active),atom(f.firstID),atom(f.firstType)})
 end
 return table.concat(parts)
end
function N.Capture(P,shared,pid,rows,routeSignature,previous)
 local player=assert(Players[pid],'NETWORK_PLAYER_UNAVAILABLE')
 local cities=player:GetCities();local capital=cities:GetCapitalCity()
 local out={validity='VERIFIED',routeSignature=routeSignature,cities={},capital=capital and capital:GetID() or nil,
  kResearch=SPCBoostConfig and SPCBoostConfig.k.RESEARCH or 1,kCulture=SPCBoostConfig and SPCBoostConfig.k.CULTURE or 1}
 out.factAvailability='CONFIRMED';out.provenance={}
 local function level(n)return type(n)=='number' and n>=0 and n<=4 and n%1==0 end
 local kinds={NONE=true,RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true}
 local count=0
 for _,c in cities:Members() do
  P.Count('city_scan');count=count+1;assert(count<=512,'NETWORK_CITY_LIMIT')
  local id=c:GetID();assert(c:GetOwner()==pid and not out.cities[id],'NETWORK_CITY_REFERENCE_INVALID')
  local reference=N.Reference(c);local old=previous and previous.cities[id]
  if old and old.reference~=reference then old=nil end
  local ok,f=pcall(function()return shared.EffectiveFacts.Read(pid,c)end)
  local valid=ok and type(f)=='table' and kinds[f.specialization] and level(f.potential) and level(f.active)
  local provenance='CONFIRMED';local reason
  if not valid then
   -- Identity/reference changes are negative facts even when ACTIVE is unreadable.
   -- A failed getter is not an unassigned city and must never erase a known center.
   local identity=ok and type(f)=='table' and kinds[f.specialization] and f.specialization or nil
   local baseFacts
   if not identity and shared.CityProgressionStore and shared.CityProgressionStore.Base then
    local read,base=pcall(shared.CityProgressionStore.Base,pid,c)
    if read and type(base)=='table' and base.owner==pid and base.cityID==id and kinds[base.specialization] then identity=base.specialization;baseFacts=base end
   end
   if old and (identity and identity~=old.specialization or ok and type(f)=='table' and f.token and f.token~=old.token) then old=nil end
   local untracked=false
   if not ok then
    local read,excluded=pcall(function()
     return not (shared.CityProgressionStore and shared.CityProgressionStore.BlocksLegacy(c))
      and shared.CityFlowProbe and shared.CityFlowProbe.ready and c:GetProperty('SPC_DEV_CITY_FLOW_B020')==nil
    end)
    untracked=read and excluded==true
   end
   if untracked then f={specialization='NONE',potential=0,active=0}
   elseif old and old.provenance~='UNKNOWN' then
    local partial=ok and type(f)=='table' and f or {}
    f={specialization=identity or old.specialization,potential=level(partial.potential) and partial.potential or old.potential,
     active=level(partial.active) and partial.active or old.active,token=partial.token or old.token,
     first=partial.first,firstID=old.firstID,firstType=old.firstType}
    provenance='RETAINED';reason='NETWORK_SOURCE_FACTS_UNAVAILABLE'
   else
    local partial=ok and type(f)=='table' and f or baseFacts or {}
    f={specialization=identity or 'UNKNOWN',potential=level(partial.potential) and partial.potential or 0,
     active=level(partial.active) and partial.active or 0,token=partial.token,first=partial.first}
    provenance='UNKNOWN';reason='NETWORK_SOURCE_NEVER_CONFIRMED'
    if not identity or identity~='NONE' and not level(partial.potential)then out.roleUnknown=true end
   end
  end
  if provenance~='CONFIRMED' then out.pending=true;out.factAvailability='MIXED' end
  local row={reference=reference,token=f.token,specialization=f.specialization,potential=f.potential,active=f.active,
   firstID=f.firstID or (f.first and f.first.districtID),firstType=f.firstType or (f.first and f.first.type),
   provenance=provenance,reason=reason}
  out.cities[id]=row;out.provenance[id]={reference=reference,status=provenance,reason=reason}
 end
 assert(not out.capital or out.cities[out.capital],'NETWORK_CAPITAL_UNAVAILABLE')
 -- Include all endpoints, including international references, without interpreting foreign progression.
 local refs={}
 for _,r in ipairs(rows) do
  local op,dp=assert(Players[r.op]),assert(Players[r.dp])
  local o,z=assert(op:GetCities():FindID(r.oc)),assert(dp:GetCities():FindID(r.dc))
  assert(o:GetOwner()==r.op and z:GetOwner()==r.dp,'NETWORK_ENDPOINT_CHANGED')
  local known,u=pcall(function() return op:GetUnits():FindID(r.trader) end)
  assert(not known or u,'NETWORK_TRADER_REMOVED')
  if r.op~=r.dp then
   local readable,war=pcall(function() return op:GetDiplomacy():IsAtWarWith(r.dp) end)
   assert(not readable or war~=true,'NETWORK_ROUTE_AT_WAR')
  end
  refs[#refs+1]=atom(r.trader)..N.Reference(o)..N.Reference(z)
 end
 table.sort(refs);out.routeSignature=atom(routeSignature)..table.concat(refs)
 out.signature=N.Signature(out);return out
end
