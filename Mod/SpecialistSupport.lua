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
function S.Retire(P,c)
 local removed=0;local b=c:GetBuildings()
 for _,name in ipairs(S.Retired) do
  local row=assert(P.Info('Buildings',name),'B1_RETIRED_DEFINITION_MISSING')
  local present=P.HasBuilding(b,row.Index);assert(type(present)=='boolean','B1_CARRIER_UNKNOWN')
  if present then P.RemoveBuilding(b,row.Index);assert(P.HasBuilding(b,row.Index)==false,'B1_RETIRE_UNCONFIRMED');removed=removed+1 end
 end
 return removed
end
-- Nil = confirmed ineligible; thrown read = UNKNOWN, retain existing projection.
function S.Anchor(P,shared,pid,c,batch)
 if c:GetOwner()~=pid or not P.IsTestPlayer(pid) then return nil end
 local f=batch.Facts(pid,c)
 if f.specialization=='NONE' then return nil end
 assert(P.Families and type(f.specialization)=='string','B1_IDENTITY_UNKNOWN')
 assert(f.first and type(f.potential)=='number' and f.potential>=1,'B1_FOUNDATION_UNKNOWN')
 for _,d in batch.Districts(pid,c) do
  if d:GetID()==f.first.districtID then
   local owner=d:GetCity();assert(owner,'B1_CITY_UNKNOWN')
   if owner:GetOwner()~=pid or owner:GetID()~=c:GetID() then return nil end
   local row=assert(P.Info('Districts',d:GetType()),'B1_DISTRICT_UNKNOWN')
   if row.DistrictType~=f.first.type or P.Family(row.DistrictType)~=f.specialization then return nil end
   local complete,pillaged=d:IsComplete(),d:IsPillaged()
   assert(type(complete)=='boolean' and type(pillaged)=='boolean','B1_DISTRICT_STATE_UNKNOWN')
   if not complete or pillaged then return nil end
   assert(type(f.active)=='number','B1_ACTIVE_UNKNOWN')
   if f.active<1 then return nil end
   assert(f.active%1==0 and f.active<=4 and f.active<=f.potential,'B1_ACTIVE_INVALID')
   return f.specialization,d,f
  end
 end
 return nil
end
