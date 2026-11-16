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

-- Resolve and withdraw only the historical carriers owned by Standardization.
-- The caller retains responsibility for the city reference and completion.
function SPCStandardizationCatalog.LegacyWithdrawal(P,group,counter)
 assert(group=='DISCOUNT' or group=='COPY','STD_LEGACY_GROUP_UNKNOWN')
 local tag='STD_OLD_'..group..'_'
 local ids
 local function resolve()
  local rows={}
  local function add(name)
   local b=assert(P.Info('Buildings',name),tag..'ROW')
   assert(b.InternalOnly==1 or b.InternalOnly==true,tag..'NOT_INTERNAL')
   rows[#rows+1]=assert(b.Index,tag..'ROW')
  end
  if group=='DISCOUNT' then
   for _,row in ipairs(P.Rows('SPC_B054_Targets'))do add(row.CarrierType)end
   assert(#rows>0,'STD_OLD_DISCOUNT_CATALOG_EMPTY')
  else
   for _,part in ipairs({'POS','NEG','POP'})do
    for bit=0,(part=='POP' and 7 or 15)do add('BUILDING_SPC_B051_PRODUCTION_'..part..'_'..bit)end
   end
  end
  return rows
 end
 return function(c)
  ids=ids or resolve()
  local b=c:GetBuildings()
  for _,id in ipairs(ids)do
   local has=P.HasBuilding(b,id)
   assert(type(has)=='boolean',tag..'UNKNOWN')
   if has then
    P.RemoveBuilding(b,id)
    assert(P.HasBuilding(b,id)==false,tag..'REMOVE')
    counter.changes=counter.changes+1
   end
  end
  return true
 end
end
