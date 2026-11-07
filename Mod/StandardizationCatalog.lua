-- D0015 catalog and activation are independent. No purchase modifier is applied here.
if not SPCOrdinaryBuildingCatalog then include('OrdinaryBuildingCatalog')end
SPCStandardizationCatalog={}
function SPCStandardizationCatalog.Build(P)
 local enabled={CAMPUS=true,THEATER=true,INDUSTRIAL_ZONE=true,COMMERCIAL_HUB=true,ENCAMPMENT=true,HARBOR=true,HOLY_SITE=true,AERODROME=true,AQUEDUCT=true,DAM=true,NEIGHBORHOOD=true,ENTERTAINMENT_COMPLEX=true,WATER_ENTERTAINMENT_COMPLEX=true,PRESERVE=true,DIPLOMATIC_QUARTER=true}
 local center={BUILDING_MONUMENT='CENTER_BASIC',BUILDING_GRANARY='CENTER_BASIC',BUILDING_WATER_MILL='CENTER_BASIC',BUILDING_NILOMETER_HD='CENTER_BASIC',BUILDING_HD_TABLES_OF_LAW='CENTER_BASIC',BUILDING_EXHIBITION='CENTER_EXHIBITION',BUILDING_HD_POLICE_STATION='CENTER_POLICE'}
 local out={buildings={},count=0,policyRevision='D0015',districtPolicy='D0045'}
 local source=SPCOrdinaryBuildingCatalog.Read(P)
 for id,b in pairs(source.effectBuildings)do
  assert(b.tier~=nil,'STD_TIER_UNKNOWN '..id..' '..tostring(b.tierError))
  local kind=b.district:gsub('^DISTRICT_','')
  local group=b.district..':'..b.tier
  local active=enabled[kind]==true
  if kind=='CITY_CENTER'then group=center[id]or ('DISABLED_CENTER:'..id);active=center[id]~=nil end
  out.buildings[id]={index=b.index,name=b.name,district=b.district,tier=b.tier,group=group,enabled=active,purchaseYield=b.purchaseYield}
  out.count=out.count+1
 end
 out.districts={}
 for kind,row in pairs(source.districts)do
  if enabled[row.base:gsub('^DISTRICT_','')] and not row.internal then
   out.districts[kind]={base=row.base,index=row.index,name=row.name}
  end
 end
 assert(out.count>0,'STD_CATALOG_EMPTY');return out
end
