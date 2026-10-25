-- Gameplay-only target policy over explicit raw UI facts and the shared catalogue.
-- No native reads, price cache, hooks or persistent records.
SPCDevelopmentInvestmentTargets={}
local M=SPCDevelopmentInvestmentTargets
function M.Candidates(catalog,facts)
 assert(type(facts.completeDomains)=='table'and type(facts.buildings)=='table','DEVELOPMENT_NATIVE_FACTS_STALE')
 local groups,existing,ids={},{},{}
 for domain,rows in pairs(catalog.domains)do
  local complete=facts.completeDomains[domain];assert(complete==nil or type(complete)=='boolean','DEVELOPMENT_NATIVE_FACTS_STALE')
  if complete then
  local have,candidates,lowest={},{},nil
  for _,b in ipairs(rows)do
   local raw=assert(facts.buildings[b.id],'DEVELOPMENT_BUILDING_UNKNOWN')
   assert(type(raw.present)=='boolean','DEVELOPMENT_BUILDING_UNKNOWN')
   if raw.present then have[b.id]=true
   else
    assert(type(raw.constructible)=='boolean','DEVELOPMENT_CONSTRUCTION_UNKNOWN')
    if raw.constructible then
     if lowest==nil or b.tier<lowest then lowest=b.tier;candidates={}end
     if b.tier==lowest then candidates[#candidates+1]=b.id end
    end
   end
  end
  existing[domain]=have
  if #candidates>0 then
   groups[#groups+1]={domain=domain,tier=lowest,ids=candidates}
   for _,id in ipairs(candidates)do ids[#ids+1]=id end
  end
 end end
 table.sort(groups,function(a,b)return a.domain<b.domain end);table.sort(ids)
 local encoded={};for _,id in ipairs(ids)do encoded[#encoded+1]=#id..':'..id end
 return groups,existing,table.concat(encoded),ids
end
function M.Options(groups,ids,raw)
 assert(type(raw)=='table'and type(raw.prices)=='table','DEVELOPMENT_NATIVE_FACTS_STALE')
 local wanted={};for _,id in ipairs(ids)do wanted[id]=true end
 local count=0
 for id,v in pairs(raw.prices)do
  assert(wanted[id]and type(v)=='table'and(v.status=='RETURNED'or v.status=='UNAVAILABLE'),'DEVELOPMENT_NATIVE_FACTS_STALE')
  count=count+1
 end
 assert(count==#ids,'DEVELOPMENT_NATIVE_FACTS_STALE')
 local out={}
 for _,group in ipairs(groups)do
  local choice,price,unknown
  for _,id in ipairs(group.ids)do
   local v=raw.prices[id];local n=v.value
   if v.status~='RETURNED'or type(n)~='number'or n~=n or n<=0 or n==math.huge then unknown=true
   elseif not price or n<price or n==price and id<choice then choice=id;price=n end
  end
  out[#out+1]={domain=group.domain,tier=group.tier,building=not unknown and choice or nil,
   price=not unknown and price or nil,reason=unknown and 'DEVELOPMENT_PRICE_UNAVAILABLE'or'DEVELOPMENT_READY',count=#group.ids}
 end
 return out
end
