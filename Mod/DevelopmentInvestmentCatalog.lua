-- Static definitions only. No eligibility, current yield or current-price cache.
if not SPCOrdinaryBuildingCatalog then include('OrdinaryBuildingCatalog')end
SPCDevelopmentInvestmentCatalog={}
function SPCDevelopmentInvestmentCatalog.Build(P)
 local source=SPCOrdinaryBuildingCatalog.Read(P)
 local out={buildings={},domains={},base={}}
 for kind,row in pairs(source.districts)do out.base[kind]=row.base end
 for kind,b in pairs(source.effectBuildings)do
  if not b.mustPurchase then
   assert(b.tier~=nil,'DEVELOPMENT_TIER_UNKNOWN '..kind..' '..tostring(b.tierError))
   local row={id=kind,index=b.index,hash=b.hash,name=b.name,domain=b.base,tier=b.tier}
   out.buildings[kind]=row
   out.domains[b.base]=out.domains[b.base]or {}
   table.insert(out.domains[b.base],row)
  end
 end
 for _,rows in pairs(out.domains)do table.sort(rows,function(a,b)return a.id<b.id end)end
 return out
end
