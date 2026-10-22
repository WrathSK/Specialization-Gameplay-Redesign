-- UI-context native facts; read-only, synchronous and invoked on OPEN/CONFIRM.
-- Base ProductionPanel uses CanProduce(hash,false,true) and GetPurchaseCost(Gold,hash).
-- Deliberately never ask CanPurchase/CanStartCommand: permission is not price.
include('DevelopmentInvestmentCatalog')
SPCDevelopmentInvestmentRead={}
function SPCDevelopmentInvestmentRead.New(P)
 local catalog
 local function read(pid,id)
  assert(pid==Game.GetLocalPlayer() and P.IsTestPlayer(pid),'DEVELOPMENT_UI_OWNER')
  local c=assert(Players[pid] and Players[pid]:GetCities():FindID(id),'DEVELOPMENT_UI_CITY')
  assert(c:GetOwner()==pid,'DEVELOPMENT_UI_OWNER')
  catalog=catalog or SPCDevelopmentInvestmentCatalog.Build(P)
  local districts,existing,options={},{},{}
  local nativeDistricts=c:GetDistricts()
  for _,d in nativeDistricts:Members()do
   local row=assert(P.Info('Districts',d:GetType()),'DEVELOPMENT_DISTRICT_UNKNOWN')
   local complete=nativeDistricts:IsComplete(row.Index)
   assert(type(complete)=='boolean','DEVELOPMENT_DISTRICT_UNKNOWN')
   if complete then districts[catalog.base[row.DistrictType]]=true end
  end
  local buildings=c:GetBuildings();local queue=c:GetBuildQueue();local gold=assert(P.Info('Yields','YIELD_GOLD'),'DEVELOPMENT_GOLD_UNKNOWN')
  for domain,rows in pairs(catalog.domains)do if districts[domain]then
   local have,candidates,lowest={}, {},nil
   for _,b in ipairs(rows)do
    local has=P.HasBuilding(buildings,b.index);assert(type(has)=='boolean','DEVELOPMENT_BUILDING_UNKNOWN')
    if has then have[b.id]=true
    else
     local eligible=queue:CanProduce(b.hash,false,true)
     assert(type(eligible)=='boolean','DEVELOPMENT_CONSTRUCTION_UNKNOWN')
     if eligible then
      if lowest==nil or b.tier<lowest then lowest=b.tier;candidates={}end
      if b.tier==lowest then candidates[#candidates+1]=b end
     end
    end
   end
   existing[domain]=have
   if #candidates>0 then
    local choice,price,unknown
    for _,b in ipairs(candidates)do
     local ok,n=pcall(function()return c:GetGold():GetPurchaseCost(gold.Index,b.hash)end)
     if not ok or type(n)~='number' or n~=n or n<=0 or n==math.huge then unknown=true
     elseif not price or n<price or n==price and b.id<choice then choice=b.id;price=n end
    end
    -- The minimum is unproved if ANY eligible equal-tier price is unavailable.
    options[#options+1]={domain=domain,tier=lowest,building=not unknown and choice or nil,
     price=not unknown and price or nil,reason=unknown and 'DEVELOPMENT_PRICE_UNAVAILABLE' or 'DEVELOPMENT_READY',count=#candidates}
   end
  end end
  table.sort(options,function(a,b)return a.domain<b.domain end)
  return {owner=pid,cityID=id,x=c:GetX(),y=c:GetY(),turn=Game.GetCurrentGameTurn(),options=options,existing=existing}
 end
 ExposedMembers.SPC_DevelopmentRead=read
 return read
end
