-- P0-A: reviewed ordinary ontology, NOT Standardization activation policy.
-- Supported named base/HD infrastructure only; unknown rows never auto-enroll.
-- The loaded upgrade graph and the selected assembly own Tier facts.
SPCOrdinaryBuildingCatalog={}
local M=SPCOrdinaryBuildingCatalog
M.REVISION='D0060-B416'
local known={
 ['BUILDING_HD_BUS_STOP']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_HD_MANSION']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_HD_VILLA']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_FAIR']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_HD_ART_PUBLISHING_HOUSE']='DISTRICT_THEATER',
 ['BUILDING_HD_DATA_CENTER']='DISTRICT_CAMPUS',
 ['BUILDING_HD_ELECTRONICS_FACTORY']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_HD_INTERNET_COMPANY']='DISTRICT_INDUSTRIAL_ZONE',

 ['BUILDING_AMPHITHEATER']='DISTRICT_THEATER',
 ['BUILDING_ARMORY']='DISTRICT_ENCAMPMENT',
 ['BUILDING_BANK']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_BARRACKS']='DISTRICT_ENCAMPMENT',
 ['BUILDING_BASILIKOI_PAIDES']='DISTRICT_ENCAMPMENT',
 ['BUILDING_BROADCAST_CENTER']='DISTRICT_THEATER',
 ['BUILDING_CATHEDRAL']='DISTRICT_HOLY_SITE',
 ['BUILDING_CHANCERY']='DISTRICT_DIPLOMATIC_QUARTER',
 ['BUILDING_COAL_POWER_PLANT']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_CONSULATE']='DISTRICT_DIPLOMATIC_QUARTER',
 ['BUILDING_DAR_E_MEHR']='DISTRICT_HOLY_SITE',
 ['BUILDING_ELECTRONICS_FACTORY']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_FACTORY']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_FILM_STUDIO']='DISTRICT_THEATER',
 ['BUILDING_FOOD_MARKET']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_FOSSIL_FUEL_POWER_PLANT']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_GOV_CITYSTATES']='DISTRICT_GOVERNMENT',
 ['BUILDING_GOV_CONQUEST']='DISTRICT_GOVERNMENT',
 ['BUILDING_GOV_CULTURE']='DISTRICT_GOVERNMENT',
 ['BUILDING_GOV_FAITH']='DISTRICT_GOVERNMENT',
 ['BUILDING_GOV_MILITARY']='DISTRICT_GOVERNMENT',
 ['BUILDING_GOV_SCIENCE']='DISTRICT_GOVERNMENT',
 ['BUILDING_GOV_SPIES']='DISTRICT_GOVERNMENT',
 ['BUILDING_GOV_TALL']='DISTRICT_GOVERNMENT',
 ['BUILDING_GOV_WIDE']='DISTRICT_GOVERNMENT',
 ['BUILDING_GRAND_BAZAAR']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_GURDWARA']='DISTRICT_HOLY_SITE',
 ['BUILDING_HD_INN']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_HD_REGIONAL_COUNCIL_CENTER']='DISTRICT_DIPLOMATIC_QUARTER',
 ['BUILDING_HD_TAVERN']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_HD_WORLD_PARLIAMENT_HEADQUARTERS']='DISTRICT_DIPLOMATIC_QUARTER',
 ['BUILDING_IZ_WATER_MILL']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_JNR_ACADEMY']='DISTRICT_CAMPUS',
 ['BUILDING_JNR_ALTAR']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_ARCHITECTURE']='DISTRICT_CAMPUS',
 ['BUILDING_JNR_ARSENAL']='DISTRICT_ENCAMPMENT',
 ['BUILDING_JNR_ART_GALLERY']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_JNR_ASSEMBLY']='DISTRICT_THEATER',
 ['BUILDING_JNR_CABINET']='DISTRICT_THEATER',
 ['BUILDING_JNR_CANDI']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_CAVALIER']='DISTRICT_ENCAMPMENT',
 ['BUILDING_JNR_CHEMICAL']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_JNR_COMMODITY_EXCHANGE']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_JNR_CRUISE_TERMINAL']='DISTRICT_HARBOR',
 ['BUILDING_JNR_DAOGUAN']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_DEPOT']='DISTRICT_ENCAMPMENT',
 ['BUILDING_JNR_EDUCATION']='DISTRICT_CAMPUS',
 ['BUILDING_JNR_FREEPORT']='DISTRICT_HARBOR',
 ['BUILDING_JNR_FREIGHT_YARD']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_JNR_GARDEN']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_GRAND_HOTEL']='DISTRICT_THEATER',
 ['BUILDING_JNR_GUILDHALL']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_JNR_HAVEN']='DISTRICT_HARBOR',
 ['BUILDING_JNR_HOSPITAL']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_JNR_HOSPITIUM']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_JINJA']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_KHALWAT']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_LABORATORY']='DISTRICT_CAMPUS',
 ['BUILDING_JNR_LIBERAL_ARTS']='DISTRICT_CAMPUS',
 ['BUILDING_JNR_LIGHTHOUSE_TRADE']='DISTRICT_HARBOR',
 ['BUILDING_JNR_MANDIR']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_MANSION']='DISTRICT_THEATER',
 ['BUILDING_JNR_MANUFACTURY']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_JNR_MARKETING_AGENCY']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_JNR_MBARI']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_MEDIA_CENTER']='DISTRICT_THEATER',
 ['BUILDING_JNR_MEDITATION']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_JNR_MERCHANT_QUARTER']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_JNR_MINT']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_JNR_MONASTERY']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_NAVAL_BASE']='DISTRICT_HARBOR',
 ['BUILDING_JNR_OPERA']='DISTRICT_THEATER',
 ['BUILDING_JNR_PERIPTEROS']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_PRISON']='DISTRICT_ENCAMPMENT',
 ['BUILDING_JNR_REAL_ACADEMY']='DISTRICT_CAMPUS',
 ['BUILDING_JNR_RECYCLING_PLANT']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_JNR_SCHOOL']='DISTRICT_CAMPUS',
 ['BUILDING_JNR_SOBOR']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_TARGET_RANGE']='DISTRICT_ENCAMPMENT',
 ['BUILDING_JNR_TOOLING_SHOP']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_JNR_TRANSIT_HUB']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_JNR_TZACUALLI']='DISTRICT_HOLY_SITE',
 ['BUILDING_JNR_WAYSTATION']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_JNR_WIND_MILL']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_LIBRARY']='DISTRICT_CAMPUS',
 ['BUILDING_LIGHTHOUSE']='DISTRICT_HARBOR',
 ['BUILDING_MADRASA']='DISTRICT_CAMPUS',
 ['BUILDING_MARAE']='DISTRICT_THEATER',
 ['BUILDING_MARKET']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_MEETING_HOUSE']='DISTRICT_HOLY_SITE',
 ['BUILDING_MILITARY_ACADEMY']='DISTRICT_ENCAMPMENT',
 ['BUILDING_MOSQUE']='DISTRICT_HOLY_SITE',
 ['BUILDING_MUSEUM_ART']='DISTRICT_THEATER',
 ['BUILDING_MUSEUM_ARTIFACT']='DISTRICT_THEATER',
 ['BUILDING_NAVIGATION_SCHOOL']='DISTRICT_CAMPUS',
 ['BUILDING_ORDU']='DISTRICT_ENCAMPMENT',
 ['BUILDING_PAGODA']='DISTRICT_HOLY_SITE',
 ['BUILDING_POWER_PLANT']='DISTRICT_INDUSTRIAL_ZONE',
 ['BUILDING_PRASAT']='DISTRICT_HOLY_SITE',
 ['BUILDING_QUEENS_BIBLIOTHEQUE']='DISTRICT_GOVERNMENT',
 ['BUILDING_RESEARCH_LAB']='DISTRICT_CAMPUS',
 ['BUILDING_SEAPORT']='DISTRICT_HARBOR',
 ['BUILDING_SHIPYARD']='DISTRICT_HARBOR',
 ['BUILDING_SHOPPING_MALL']='DISTRICT_NEIGHBORHOOD',
 ['BUILDING_SHRINE']='DISTRICT_HOLY_SITE',
 ['BUILDING_STABLE']='DISTRICT_ENCAMPMENT',
 ['BUILDING_STAVE_CHURCH']='DISTRICT_HOLY_SITE',
 ['BUILDING_STOCK_EXCHANGE']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_STUPA']='DISTRICT_HOLY_SITE',
 ['BUILDING_SUKIENNICE']='DISTRICT_COMMERCIAL_HUB',
 ['BUILDING_SYNAGOGUE']='DISTRICT_HOLY_SITE',
 ['BUILDING_TEMPLE']='DISTRICT_HOLY_SITE',
 ['BUILDING_UNIVERSITY']='DISTRICT_CAMPUS',
 ['BUILDING_WAT']='DISTRICT_HOLY_SITE',
 ['BUILDING_WORKSHOP']='DISTRICT_INDUSTRIAL_ZONE',
}
-- P0-L1 ordinary identity extension; NOT newly approved D/Tier coverage.
-- Named native/HD/JNR construction definitions reviewed; one-per-player alone
-- is not a Wonder predicate (e.g. ordinary government buildings/Data Center).
local ordinaryOnly={
 ['BUILDING_MONUMENT']='DISTRICT_CITY_CENTER',
 ['BUILDING_GRANARY']='DISTRICT_CITY_CENTER',
 ['BUILDING_WATER_MILL']='DISTRICT_CITY_CENTER',
 ['BUILDING_NILOMETER_HD']='DISTRICT_CITY_CENTER',
 ['BUILDING_PALGUM']='DISTRICT_CITY_CENTER',
 ['BUILDING_WALLS']='DISTRICT_CITY_CENTER',
 ['BUILDING_CASTLE']='DISTRICT_CITY_CENTER',
 ['BUILDING_STAR_FORT']='DISTRICT_CITY_CENTER',
 ['BUILDING_TSIKHE']='DISTRICT_CITY_CENTER',
 ['BUILDING_EXHIBITION']='DISTRICT_CITY_CENTER',
 ['BUILDING_FLOOD_BARRIER']='DISTRICT_CITY_CENTER',
 ['BUILDING_HD_POLICE_STATION']='DISTRICT_CITY_CENTER',
 ['BUILDING_HD_TABLES_OF_LAW']='DISTRICT_CITY_CENTER',
 ['BUILDING_HANGAR']='DISTRICT_AERODROME',
 ['BUILDING_AIRPORT']='DISTRICT_AERODROME',
 ['BUILDING_SEWER']='DISTRICT_AQUEDUCT',
 ['BUILDING_HD_HYDRAULIC_SPINNING_WHEEL']='DISTRICT_AQUEDUCT',
 ['BUILDING_JNR_BATHHOUSE']='DISTRICT_AQUEDUCT',
 ['BUILDING_JNR_HAMMER_WORKS']='DISTRICT_AQUEDUCT',
 ['BUILDING_JNR_ORCHARD']='DISTRICT_AQUEDUCT',
 ['BUILDING_HYDROELECTRIC_DAM']='DISTRICT_DAM',
 ['BUILDING_ARENA']='DISTRICT_ENTERTAINMENT_COMPLEX',
 ['BUILDING_ZOO']='DISTRICT_ENTERTAINMENT_COMPLEX',
 ['BUILDING_STADIUM']='DISTRICT_ENTERTAINMENT_COMPLEX',
 ['BUILDING_THERMAL_BATH']='DISTRICT_ENTERTAINMENT_COMPLEX',
 ['BUILDING_TLACHTLI']='DISTRICT_ENTERTAINMENT_COMPLEX',
 ['BUILDING_HD_SALON']='DISTRICT_ENTERTAINMENT_COMPLEX',
 ['BUILDING_JNR_BOTANICAL_GARDEN']='DISTRICT_ENTERTAINMENT_COMPLEX',
 ['BUILDING_JNR_THEME_PARK']='DISTRICT_ENTERTAINMENT_COMPLEX',
 ['BUILDING_JNR_TOURNEY']='DISTRICT_ENTERTAINMENT_COMPLEX',
 ['BUILDING_FERRIS_WHEEL']='DISTRICT_WATER_ENTERTAINMENT_COMPLEX',
 ['BUILDING_AQUARIUM']='DISTRICT_WATER_ENTERTAINMENT_COMPLEX',
 ['BUILDING_AQUATICS_CENTER']='DISTRICT_WATER_ENTERTAINMENT_COMPLEX',
 ['BUILDING_JNR_CASINO']='DISTRICT_WATER_ENTERTAINMENT_COMPLEX',
 ['BUILDING_JNR_FOOD_COURT']='DISTRICT_WATER_ENTERTAINMENT_COMPLEX',
 ['BUILDING_JNR_MARINA']='DISTRICT_WATER_ENTERTAINMENT_COMPLEX',
 ['BUILDING_GROVE']='DISTRICT_PRESERVE',
 ['BUILDING_SANCTUARY']='DISTRICT_PRESERVE',
 ['BUILDING_HD_CULTURE_HERITAGE_PRESERVE']='DISTRICT_PRESERVE',
 ['BUILDING_HD_LANDFORM_EPO']='DISTRICT_PRESERVE',
 ['BUILDING_HD_RESOURCE_EPO']='DISTRICT_PRESERVE',
 ['BUILDING_HD_SCENIC_EPO']='DISTRICT_PRESERVE',
 ['BUILDING_HD_SPECIES_EPO']='DISTRICT_PRESERVE',
 ['BUILDING_FISH_MARKET']='DISTRICT_HARBOR',
 ['BUILDING_LIGHTHOUSE_FISHING']='DISTRICT_HARBOR',
 ['BUILDING_OFFSHORE_TERMINAL']='DISTRICT_HARBOR',
 ['BUILDING_JNR_ENTREPOT']='DISTRICT_HARBOR',
 ['BUILDING_HD_ALCHEMY_ROOM']='DISTRICT_HOLY_SITE',
 ['BUILDING_EL_ESCORIAL_PALACE']='DISTRICT_GOVERNMENT',
 ['BUILDING_HD_HUMAN_RIGHTS_COUNCIL']='DISTRICT_DIPLOMATIC_QUARTER',
 ['BUILDING_HD_MINISTRY_OF_NATIONAL_DEFENSE']='DISTRICT_DIPLOMATIC_QUARTER',
}
local domains={
 ['DISTRICT_CAMPUS']=true,
 ['DISTRICT_INDUSTRIAL_ZONE']=true,
 ['DISTRICT_THEATER']=true,
 ['DISTRICT_COMMERCIAL_HUB']=true,
 ['DISTRICT_HARBOR']=true,
 ['DISTRICT_ENCAMPMENT']=true,
 ['DISTRICT_HOLY_SITE']=true,
 ['DISTRICT_GOVERNMENT']=true,
 ['DISTRICT_DIPLOMATIC_QUARTER']=true,
 ['DISTRICT_NEIGHBORHOOD']=true,
}

-- These are already in the Standardization/Development directory. Their
-- admission there does not extend D or the ordinary-building effects.
local effectOnly={
 BUILDING_PALACE='DISTRICT_CITY_CENTER',
 BUILDING_JNR_LIGHTHOUSE_FISHING='DISTRICT_HARBOR',
 BUILDING_JNR_FISH_MARKET='DISTRICT_HARBOR',
 BUILDING_JNR_OFFSHORE_TERMINAL='DISTRICT_HARBOR',
}
local function flag(v)return v==true or v==1 end

local function inputRows(P,name)
 return assert(P.Rows(name),'BUILDING_CATALOG_TABLE_UNAVAILABLE '..name)
end

local function districtDirectory(P)
 local districts,parents={},{}
 for _,row in ipairs(inputRows(P,'Districts'))do
  districts[row.DistrictType]={index=row.Index,name=row.Name,internal=flag(row.InternalOnly)}
 end
 for _,row in ipairs(inputRows(P,'DistrictReplaces'))do
  local kind,parent=row.CivUniqueDistrictType,row.ReplacesDistrictType
  assert(districts[kind] and districts[parent],'BUILDING_CATALOG_DISTRICT_REPLACEMENT_MISSING')
  assert(not parents[kind] or parents[kind]==parent,'BUILDING_CATALOG_DISTRICT_REPLACEMENT_CONFLICT')
  parents[kind]=parent
 end
 local visiting={}
 local function base(kind)
  local row=districts[kind]
  if row.base then return row.base end
  assert(not visiting[kind],'BUILDING_CATALOG_DISTRICT_REPLACEMENT_CYCLE')
  visiting[kind]=true
  row.base=parents[kind] and base(parents[kind])or kind
  visiting[kind]=nil
  return row.base
 end
 for kind in pairs(districts)do base(kind)end
 return districts
end

local function related(P,name,from,to,members)
 local result={}
 for _,row in ipairs(inputRows(P,name))do
  local key=row[from]
  if members[key]then
   local list=result[key]or {};result[key]=list
   list[#list+1]=assert(row[to],'BUILDING_CATALOG_RELATION_INCOMPLETE')
  end
 end
 return result
end

local function buildTiers(P,districts,native,excluded,members)
 local prereqs=related(P,'BuildingPrereqs','Building','PrereqBuilding',members)
 local replacements=related(P,'BuildingReplaces','CivUniqueBuildingType','ReplacesBuildingType',members)
 local visiting={}
 local solve
 local function resolve(kind,row)
  local replacement=replacements[kind]
  local inherited
  for _,parent in ipairs(replacement or {})do
   local original=members[parent]
   if not original or original.base~=row.base then return nil,'REPLACEMENT_UNREVIEWED' end
   local tier,why=solve(parent)
   if not tier then return nil,why end
   if inherited and inherited~=tier then return nil,'REPLACEMENT_TIER_CONFLICT' end
   inherited=tier
  end
  -- The retained city-center grouping uses a separate policy, with Tier 0 for
  -- its receipts and Development ordering. It has no district D chain.
  if row.base=='DISTRICT_CITY_CENTER'then return 0 end
  local previous
  for _,parent in ipairs(prereqs[kind]or {})do
   local b=native[parent]
   if not b then return nil,'TIER_PREREQUISITE_MISSING' end
   if not excluded[parent]then
    local d=districts[b.PrereqDistrict]
    if not d then return nil,'TIER_PREREQUISITE_UNCLASSIFIED' end
    if d.base==row.base then
     local tier,why=solve(parent)
     if not tier then return nil,why end
     if previous and previous~=tier then return nil,'TIER_PREREQUISITE_AMBIGUOUS' end
     previous=tier
    end
   end
  end
  local level=previous and previous+1 or inherited or 1
  if inherited and level~=inherited then return nil,'REPLACEMENT_TIER_CONFLICT' end
  row.tierSource=row.override and 'APPROVED_OVERRIDE' or (replacement and 'REPLACEMENT_TIER' or 'EFFECTIVE_CHAIN')
  return row.override or level
 end
 solve=function(kind)
  local row=members[kind]
  if not row then return nil,'TIER_PREREQUISITE_UNREVIEWED' end
  if row.tier~=nil or row.tierError then return row.tier,row.tierError end
  if visiting[kind]then return nil,'TIER_CHAIN_CYCLE' end
  visiting[kind]=true
  row.tier,row.tierError=resolve(kind,row)
  visiting[kind]=nil
  return row.tier,row.tierError
 end
 for kind in pairs(members)do solve(kind)end
end

function M.Build(P)
 local assembly=inputRows(P,'SPC_EnvironmentAssembly')
 assert(#assembly==1 and assembly[1].Id==1 and assembly[1].SchemaVersion==1
  and (assembly[1].Profile=='OFFICIAL' or assembly[1].Profile=='HD'),'BUILDING_CATALOG_ASSEMBLY_UNAVAILABLE')
 local districts=districtDirectory(P)
 local native,excluded,members={},{},{}
 local buildings=inputRows(P,'Buildings')
 for _,b in ipairs(buildings)do native[b.BuildingType]=b end
 for _,r in ipairs(inputRows(P,'SPC_EnvironmentExcludedBuildings'))do
  excluded[r.BuildingType]=true
 end
 local inventory=inputRows(P,'SPC_EnvironmentBuildings')
 assert(#inventory>0,'BUILDING_CATALOG_ASSEMBLY_EMPTY')
 for _,r in ipairs(inventory)do
  local kind=r.BuildingType
  local b=assert(native[kind],'BUILDING_CATALOG_DEFINITION_MISSING')
  local district=assert(districts[r.DistrictType],'BUILDING_CATALOG_DISTRICT_MISSING')
  assert(b.PrereqDistrict==r.DistrictType and not district.internal
   and not excluded[kind] and not flag(b.InternalOnly) and not flag(b.IsWonder)
   and not kind:match('^BUILDING_SPC_'),'BUILDING_CATALOG_DEFINITION_CONFLICT')
  local accepted=known[kind]or ordinaryOnly[kind]or effectOnly[kind]
  if kind=='BUILDING_SEWER' and district.base=='DISTRICT_CITY_CENTER'then accepted=district.base end
  if accepted then
   local row={type=kind,index=b.Index,hash=b.Hash,name=b.Name,district=r.DistrictType,base=district.base,
    mustPurchase=flag(b.MustPurchase),purchaseYield=b.PurchaseYield,override=r.TierOverride}
   if accepted~=district.base then row.tierError='DISTRICT_CLASSIFICATION_CONFLICT' end
   if r.TierOverride~=nil then
    assert(type(r.TierOverride)=='number' and r.TierOverride%1==0 and r.TierOverride>0
     and district.base~='DISTRICT_CITY_CENTER','BUILDING_CATALOG_TIER_OVERRIDE_INVALID')
   end
   members[kind]=row
  end
 end
 buildTiers(P,districts,native,excluded,members)
 local out={revision=M.REVISION,buildings={},effectBuildings=members,districts=districts}
 function out.District(kind)return districts[kind] and districts[kind].base end
 function out.Domain(kind)
  local base=out.District(kind)
  return domains[base] and base or nil
 end
 for _,b in ipairs(buildings)do
  local kind=b.BuildingType
  local entry=members[kind]
  local r={type=kind,index=b.Index,name=b.Name,domain=out.Domain(b.PrereqDistrict),
   ordinaryDistrict=out.District(b.PrereqDistrict),ordinary=false,depthEligible=false}
  if kind=='BUILDING_PALACE' then r.reason='PALACE'
  elseif flag(b.IsWonder) then r.reason='WONDER'
  elseif flag(b.InternalOnly) or excluded[kind] or kind:match('^BUILDING_SPC_') then r.reason='INTERNAL_OR_TECHNICAL'
  elseif known[kind] then
   r.ordinary=true;r.depthEligible=true
   r.tier=entry and entry.tier
   r.reason=r.tier and 'ELIGIBLE' or (entry and entry.tierError or 'TIER_INPUT_MISSING')
   r.tierSource=entry and entry.tierSource
  elseif ordinaryOnly[kind]then
   r.ordinary=entry~=nil and entry.tierError~='DISTRICT_CLASSIFICATION_CONFLICT'
   r.reason=r.ordinary and 'ORDINARY_DEPTH_NOT_REVIEWED' or 'DISTRICT_CLASSIFICATION_CONFLICT'
  else r.reason='UNREVIEWED_BUILDING' end
  r.ordinaryReason=r.ordinary and 'ELIGIBLE' or r.reason
  out.buildings[b.Index]=r;out.buildings[kind]=r
 end
 return out
end

-- Immutable definitions are shared by readers in this Lua context. City
-- presence, ownership and worker facts still use the live read barriers.
local definitions
function M.Read(P)
 if not definitions then definitions=M.Build(P)end
 return definitions
end
