-- D0015 catalog and activation are independent. No purchase modifier is applied here.
SPCStandardizationCatalog={}
function SPCStandardizationCatalog.Build(P)
 local hd=P.Field(GameInfo,'HD_BuildingTiers');local dt=P.Field(GameInfo,'HD_DUMMY_BUILDINGS')
 assert(hd and dt,'STD_HD_TABLES_UNAVAILABLE')
 local dummy={};for x in dt() do dummy[x.BuildingType]=true end
 local enabled={CAMPUS=true,THEATER=true,INDUSTRIAL_ZONE=true,COMMERCIAL_HUB=true,ENCAMPMENT=true,HARBOR=true,HOLY_SITE=true,AERODROME=true,AQUEDUCT=true,DAM=true,NEIGHBORHOOD=true,ENTERTAINMENT_COMPLEX=true,WATER_ENTERTAINMENT_COMPLEX=true,PRESERVE=true,DIPLOMATIC_QUARTER=true}
 local center={BUILDING_MONUMENT='CENTER_BASIC',BUILDING_GRANARY='CENTER_BASIC',BUILDING_WATER_MILL='CENTER_BASIC',BUILDING_NILOMETER_HD='CENTER_BASIC',BUILDING_HD_TABLES_OF_LAW='CENTER_BASIC',BUILDING_EXHIBITION='CENTER_EXHIBITION',BUILDING_HD_POLICE_STATION='CENTER_POLICE'}
 local out={buildings={},count=0,policyRevision='D0015',districtPolicy='D0045'}
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
 -- Typed District knowledge is separate from the legacy building effect catalog.
 local districts=P.Field(GameInfo,'Districts');local replacements=P.Field(GameInfo,'DistrictReplaces')
 assert(districts and replacements,'STD_DISTRICT_CATALOG_UNAVAILABLE')
 local parents={};for r in replacements()do
  assert(not parents[r.CivUniqueDistrictType] or parents[r.CivUniqueDistrictType]==r.ReplacesDistrictType,'STD_DISTRICT_MAPPING_CONFLICT')
  parents[r.CivUniqueDistrictType]=r.ReplacesDistrictType
 end
 out.districts={}
 for r in districts()do
  local id=r.DistrictType;local seen={}
  while parents[id]do
   assert(not seen[id],'STD_DISTRICT_MAPPING_CYCLE');seen[id]=true;id=parents[id]
   assert(P.Info('Districts',id),'STD_DISTRICT_MAPPING_INVALID')
  end
  if enabled[id:gsub('^DISTRICT_','')] and r.InternalOnly~=true and r.InternalOnly~=1 then
   out.districts[r.DistrictType]={base=id,index=r.Index,name=r.Name}
  end
 end
 assert(out.count>0,'STD_CATALOG_EMPTY');return out
end
