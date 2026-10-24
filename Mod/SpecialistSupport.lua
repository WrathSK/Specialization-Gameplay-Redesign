-- P0-B1 specific support contract; no generic ability/state framework.
SPCSpecialistSupport={}
local S=SPCSpecialistSupport
S.RULESET='D0032-P0B1'
S.Retired={
 'BUILDING_SPC_DEV_LV3_RESEARCH','BUILDING_SPC_DEV_LV3_CULTURE',
 'BUILDING_SPC_DEV_LV3_COMMERCE','BUILDING_SPC_DEV_LV3_INDUSTRY',
 'BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_0','BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_1',
 'BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_2','BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_3',
 'BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_4','BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_5',
 'BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_6','BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_7'}
function S.Retire(P,c,shared)
 if shared then return SPCRuntimeWork.RetireOnce(P,shared,c,'SpecialistSupport',function()return S.Retire(P,c)end)end
 local removed=0;local b=c:GetBuildings()
 for _,name in ipairs(S.Retired) do
  local row=assert(P.Info('Buildings',name),'B1_RETIRED_DEFINITION_MISSING')
  local present=P.HasBuilding(b,row.Index);assert(type(present)=='boolean','B1_CARRIER_UNKNOWN')
  if present then P.RemoveBuilding(b,row.Index);assert(P.HasBuilding(b,row.Index)==false,'B1_RETIRE_UNCONFIRMED');removed=removed+1 end
 end
 return removed
end
-- Sampling is raw, city-scoped and read-only. Each caller retains its policy.
local function find(P,pid,c,first,batch)
 if type(c.GetDistricts)=='function'then
  local districts=c:GetDistricts();local n=districts:GetNumDistricts()
  assert(type(n)=='number'and n>=0 and n%1==0,'B1_DISTRICT_COUNT_UNKNOWN')
  for i=0,n-1 do
   local d=assert(districts:GetDistrictByIndex(i),'B1_DISTRICT_ENTRY_UNKNOWN');P.Count('district_scan')
   if d:GetID()==first.districtID then return d end
  end
 else
  -- Isolated legacy profiles without indexed native CityDistricts.
  for _,d in batch.Districts(pid,c)do if d:GetID()==first.districtID then return d end end
 end
end
local function sample(P,pid,c,f,batch)
 local d=find(P,pid,c,f.first,batch)
 if not d then return {present=false}end
 local owner=assert(d:GetCity(),'B1_CITY_UNKNOWN')
 local raw={present=true,id=f.first.districtID,owner=owner:GetOwner(),cityID=owner:GetID()}
 -- Confirmed mismatches win before getters that the old policy never needed.
 if raw.owner~=pid or raw.cityID~=c:GetID()then return raw end
 raw.typeIndex=d:GetType();local row=assert(P.Info('Districts',raw.typeIndex),'B1_DISTRICT_UNKNOWN');raw.type=row.DistrictType
 if raw.type~=f.first.type or P.Family(raw.type)~=f.specialization then return raw end
 raw.complete,raw.pillaged=d:IsComplete(),d:IsPillaged()
 assert(type(raw.complete)=='boolean'and type(raw.pillaged)=='boolean','B1_DISTRICT_STATE_UNKNOWN')
 return raw
end
-- Nil = confirmed ineligible; thrown read = UNKNOWN, retain existing projection.
function S.Inspect(P,shared,pid,c,batch,project)
 if c:GetOwner()~=pid or not P.IsTestPlayer(pid)then return project(nil)end
 local function inspect(f,workers,anchors)
  if f.specialization=='NONE'then return project(nil)end
  assert(P.Families and type(f.specialization)=='string','B1_IDENTITY_UNKNOWN')
  assert(f.first and type(f.potential)=='number'and f.potential>=1,'B1_FOUNDATION_UNKNOWN')
  local raw=anchors(f.first,function()return sample(P,pid,c,f,batch)end)
  if not raw.present or raw.owner~=pid or raw.cityID~=c:GetID() or raw.type~=f.first.type or P.Family(raw.type)~=f.specialization then return project(nil)end
  if not raw.complete or raw.pillaged then return project(nil)end
  assert(type(f.active)=='number','B1_ACTIVE_UNKNOWN')
  if f.active<1 then return project(nil)end
  assert(f.active%1==0 and f.active<=4 and f.active<=f.potential,'B1_ACTIVE_INVALID')
  local function geometry()
   return anchors(f.first,function()
    local d=assert(find(P,pid,c,f.first,batch),'B1_ANCHOR_GEOMETRY_UNKNOWN')
    return {x=d:GetX(),y=d:GetY()}
   end,true)
  end
  return project(f.specialization,raw,f,workers,geometry)
 end
 return batch.Inspect(pid,c,inspect)
end
function S.Anchor(P,shared,pid,c,batch)
 return S.Inspect(P,shared,pid,c,batch,function(kind,raw,f)return kind,raw,f end)
end
