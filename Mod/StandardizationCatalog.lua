-- D0015 catalog and activation are independent. No purchase modifier is applied here.
SPCStandardizationCatalog={}
function SPCStandardizationCatalog.Build(P)
 local hd=P.Field(GameInfo,'HD_BuildingTiers');local dt=P.Field(GameInfo,'HD_DUMMY_BUILDINGS')
 assert(hd and dt,'STD_HD_TABLES_UNAVAILABLE')
 local dummy={};for x in dt() do dummy[x.BuildingType]=true end
 local enabled={CAMPUS=true,THEATER=true,INDUSTRIAL_ZONE=true,COMMERCIAL_HUB=true,ENCAMPMENT=true,HARBOR=true,HOLY_SITE=true,AERODROME=true,AQUEDUCT=true,DAM=true,NEIGHBORHOOD=true,ENTERTAINMENT_COMPLEX=true,WATER_ENTERTAINMENT_COMPLEX=true,PRESERVE=true,DIPLOMATIC_QUARTER=true}
 local center={BUILDING_MONUMENT='CENTER_BASIC',BUILDING_GRANARY='CENTER_BASIC',BUILDING_WATER_MILL='CENTER_BASIC',BUILDING_NILOMETER_HD='CENTER_BASIC',BUILDING_HD_TABLES_OF_LAW='CENTER_BASIC',BUILDING_EXHIBITION='CENTER_EXHIBITION',BUILDING_HD_POLICE_STATION='CENTER_POLICE'}
 local out={buildings={},count=0,policyRevision='D0015'}
 for x in hd() do
  local b=P.Info('Buildings',x.BuildingType)
  assert(b and b.PrereqDistrict==x.PrereqDistrict,'STD_HD_CLASSIFICATION_MISMATCH')
  assert(type(x.Tier)=='number' and x.Tier%1==0 and x.Tier>=0,'STD_TIER_INVALID')
  local internal=b.InternalOnly==true or b.InternalOnly==1
  local wonder=b.IsWonder==true or b.IsWonder==1
  if not internal and not wonder and not dummy[x.BuildingType] then
   local kind=x.PrereqDistrict:gsub('^DISTRICT_','');local group=x.PrereqDistrict..':'..x.Tier
   local active=enabled[kind]==true
   if kind=='CITY_CENTER' then group=center[x.BuildingType] or ('DISABLED_CENTER:'..x.BuildingType);active=center[x.BuildingType]~=nil end
   out.buildings[x.BuildingType]={index=b.Index,name=b.Name,district=x.PrereqDistrict,tier=x.Tier,group=group,enabled=active,purchaseYield=b.PurchaseYield}
   out.count=out.count+1
  end
 end
 assert(out.count>0,'STD_CATALOG_EMPTY');return out
end
