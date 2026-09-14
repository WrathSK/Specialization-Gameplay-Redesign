-- AV2-A: accepted logical inputs, not a shared derived-result cache or save ledger.
SPCNetworkInput={}
local N=SPCNetworkInput
local function atom(v)
 local s=type(v)..':'..(type(v)=='number' and string.format('%.17g',v) or tostring(v));return #s..':'..s
end
function N.Reference(c)
 return table.concat({atom(c:GetOwner()),atom(c:GetID()),atom(c:GetX()),atom(c:GetY()),
  atom(c:GetProperty('SPC_DEV_BINDING_B013_TOKEN'))})
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
 local count=0
 for _,c in cities:Members() do
  P.Count('city_scan');count=count+1;assert(count<=512,'NETWORK_CITY_LIMIT')
  local id=c:GetID();assert(c:GetOwner()==pid and not out.cities[id],'NETWORK_CITY_REFERENCE_INVALID')
  local reference=N.Reference(c)
  local ok,f=pcall(shared.EffectiveFacts.Read,pid,c)
  local old=previous and previous.cities[id]
  local usable=ok and type(f.active)=='number'
  if not usable and old and old.reference==reference then
   f=old;out.pending=true
  elseif not ok then
   -- Never adopt old/untracked cities. A known absent flow is the existing exclusion rule,
   -- not a guessed specialization. Broken/non-ready existing records remain UNKNOWN.
   if shared.CityFlowProbe and shared.CityFlowProbe.ready and c:GetProperty('SPC_DEV_CITY_FLOW_B020')==nil then
    f={specialization='NONE',potential=0,active=0}
   else error('NETWORK_FACTS_UNAVAILABLE') end
  end
  assert(type(f.potential)=='number' and f.potential>=0 and f.potential<=4 and f.potential%1==0,'NETWORK_POTENTIAL_UNAVAILABLE')
  assert(type(f.active)=='number' and f.active>=0 and f.active<=4 and f.active%1==0,'NETWORK_ACTIVE_UNAVAILABLE')
  assert(f.specialization=='NONE' or f.specialization=='RESEARCH' or f.specialization=='CULTURE'
   or f.specialization=='INDUSTRY' or f.specialization=='COMMERCE','NETWORK_IDENTITY_UNAVAILABLE')
  out.cities[id]={reference=reference,token=f.token,specialization=f.specialization,potential=f.potential,active=f.active,
   firstID=f.firstID or (f.first and f.first.districtID),firstType=f.firstType or (f.first and f.first.type)}
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
