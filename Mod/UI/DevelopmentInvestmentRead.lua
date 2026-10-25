-- Raw UI-context reads only. Gameplay owns tier/target/price policy.
-- Same native CanProduce(hash,false,true) and GetPurchaseCost(Gold,hash) surfaces.
include('DevelopmentInvestmentCatalog')
SPCDevelopmentInvestmentRead={}
function SPCDevelopmentInvestmentRead.New(P)
 local catalog,limit,count
 ExposedMembers.SPC_DevelopmentReaderSequence=(ExposedMembers.SPC_DevelopmentReaderSequence or 0)+1
 local generation=ExposedMembers.SPC_DevelopmentReaderSequence
 assert(generation<9007199254740992,'DEVELOPMENT_READER_GENERATION_UNAVAILABLE')
 local function definitions()
  if not catalog then
   catalog=SPCDevelopmentInvestmentCatalog.Build(P);limit=0;count=0
   for id in pairs(catalog.buildings)do limit=limit+#id+20;count=count+1 end
  end
  return catalog
 end
 local function city(pid,id)
  assert(pid==Game.GetLocalPlayer()and P.IsTestPlayer(pid),'DEVELOPMENT_UI_OWNER')
  local c=assert(Players[pid]and Players[pid]:GetCities():FindID(id),'DEVELOPMENT_UI_CITY')
  assert(c:GetOwner()==pid,'DEVELOPMENT_UI_OWNER');return c
 end
 local function stamp(pid,id,c,phase)
  assert(c:GetOwner()==pid,'DEVELOPMENT_UI_OWNER')
  return {protocol=2,phase=phase,generation=generation,owner=pid,cityID=id,x=c:GetX(),y=c:GetY(),turn=Game.GetCurrentGameTurn()}
 end
 local function read(pid,id)
  local c=city(pid,id);definitions()
  local complete,raw={},{};local nativeDistricts=c:GetDistricts()
  for _,d in nativeDistricts:Members()do
   local row=assert(P.Info('Districts',d:GetType()),'DEVELOPMENT_DISTRICT_UNKNOWN')
   local value=nativeDistricts:IsComplete(row.Index);assert(type(value)=='boolean','DEVELOPMENT_DISTRICT_UNKNOWN')
   if value then complete[assert(catalog.base[row.DistrictType],'DEVELOPMENT_DISTRICT_UNKNOWN')]=true end
  end
  local buildings=c:GetBuildings();local queue=c:GetBuildQueue()
  for domain,rows in pairs(catalog.domains)do if complete[domain]then
   for _,b in ipairs(rows)do
    local has=P.HasBuilding(buildings,b.index);assert(type(has)=='boolean','DEVELOPMENT_BUILDING_UNKNOWN')
    local v={present=has};raw[b.id]=v
    if not has then v.constructible=queue:CanProduce(b.hash,false,true);assert(type(v.constructible)=='boolean','DEVELOPMENT_CONSTRUCTION_UNKNOWN')end
   end
  end end
  local out=stamp(pid,id,c,'ELIGIBILITY');out.completeDomains=complete;out.buildings=raw;return out
 end
 local function prices(pid,id,encoded)
  local c=city(pid,id);definitions()
  assert(type(encoded)=='string'and #encoded<=limit,'DEVELOPMENT_PRICE_REQUEST_INVALID')
  local ids,seen,pos={},{},1
  while pos<=#encoded do
   local a,b,digits=encoded:find('(%d+):',pos);assert(a==pos,'DEVELOPMENT_PRICE_REQUEST_INVALID')
   local size=tonumber(digits);assert(size and size>0 and size%1==0 and b+size<=#encoded,'DEVELOPMENT_PRICE_REQUEST_INVALID')
   local name=encoded:sub(b+1,b+size);assert(catalog.buildings[name]and not seen[name]and #ids<count,'DEVELOPMENT_PRICE_REQUEST_INVALID')
   ids[#ids+1]=name;seen[name]=true;pos=b+size+1
  end
  local gold=assert(P.Info('Yields','YIELD_GOLD'),'DEVELOPMENT_GOLD_UNKNOWN');local values={}
  for _,name in ipairs(ids)do
   local b=catalog.buildings[name];local ok,n=pcall(function()return c:GetGold():GetPurchaseCost(gold.Index,b.hash)end)
   -- Retain raw numeric values, never currency conversion or target choice.
   values[name]={status=ok and 'RETURNED'or'UNAVAILABLE',value=ok and type(n)=='number'and n or nil}
  end
  local out=stamp(pid,id,c,'PRICES');out.request=encoded;out.prices=values;return out
 end
 ExposedMembers.SPC_DevelopmentRead=read;ExposedMembers.SPC_DevelopmentPriceRead=prices
 return read
end
