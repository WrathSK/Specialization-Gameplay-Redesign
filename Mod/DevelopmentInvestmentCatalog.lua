-- Static definitions only. No eligibility, current yield or current-price cache.
SPCDevelopmentInvestmentCatalog={}
function SPCDevelopmentInvestmentCatalog.Build(P)
 local dummy,parents,tiers={},{},{}
 for r in assert(P.Field(GameInfo,'HD_DUMMY_BUILDINGS'),'DEVELOPMENT_HD_CATALOG_UNAVAILABLE')()do dummy[r.BuildingType]=true end
 for r in assert(P.Field(GameInfo,'DistrictReplaces'),'DEVELOPMENT_DISTRICTS_UNAVAILABLE')()do parents[r.CivUniqueDistrictType]=r.ReplacesDistrictType end
 local out={buildings={},domains={},base={}}
 for r in GameInfo.Districts()do
  local id=r.DistrictType;local seen={}
  while parents[id]do assert(not seen[id],'DEVELOPMENT_DISTRICT_CYCLE');seen[id]=true;id=parents[id]end
  out.base[r.DistrictType]=id
 end
 for r in assert(P.Field(GameInfo,'HD_BuildingTiers'),'DEVELOPMENT_HD_CATALOG_UNAVAILABLE')()do
  assert(type(r.Tier)=='number' and r.Tier>=0 and r.Tier%1==0,'DEVELOPMENT_TIER_UNKNOWN');tiers[r.BuildingType]=r.Tier
 end
 for b in GameInfo.Buildings()do
  if tiers[b.BuildingType]~=nil and not dummy[b.BuildingType] and b.InternalOnly~=true and b.InternalOnly~=1
   and b.IsWonder~=true and b.IsWonder~=1 and b.MustPurchase~=true and b.MustPurchase~=1 then
   local domain=out.base[b.PrereqDistrict]
   assert(domain,'DEVELOPMENT_DISTRICT_UNKNOWN')
   local row={id=b.BuildingType,index=b.Index,hash=b.Hash,name=b.Name,domain=domain,tier=tiers[b.BuildingType]}
   out.buildings[row.id]=row;out.domains[domain]=out.domains[domain] or {};table.insert(out.domains[domain],row)
  end
 end
 for _,rows in pairs(out.domains)do table.sort(rows,function(a,b)return a.id<b.id end)end
 return out
end
