-- Explicit derived-slot adapter only. No startup, listener, retry, native object
-- cache or extension of permanent Store history/Copy. Actual consumers own the
-- source/physical proof and must opt in through their reviewed integration.
if not SPCNetworkRecoveryModel then include('NetworkRecoveryModel')end
if not SPCNetworkRecoveryCell then include('NetworkRecoveryCell')end
if not SPCNetworkInput then include('NetworkInput')end
SPCNetworkRecoveryStore={}
local M=SPCNetworkRecoveryStore
local PREFIX='SPC_DERIVED_NETWORK_RECOVERY_V1_'
function M.Key(family,token)
 assert(family=='COMMERCE'or family=='CULTURE','NREC_STORE_FAMILY_INVALID')
 assert(type(token)=='string'and #token>0 and #token<=256,'NREC_STORE_TOKEN_INVALID')
 return PREFIX..family..'_'..token
end
function M.Open(P,shared,pid,city,family)
 assert(family=='COMMERCE'or family=='CULTURE','NREC_STORE_FAMILY_INVALID')
 local store=assert(shared.CityProgressionStore,'NREC_STORE_REQUIRED')
 assert(store.UsesNewAuthority==true and P.IsTestPlayer(pid),'NREC_STORE_SCOPE_UNAVAILABLE')
 assert(type(P.SetProperty)=='function','NREC_STORE_SETTER_REQUIRED')
 local reference=store.HistoricalReference(city)
 assert(reference.owner==pid and reference.cityID==city:GetID()and reference.x==city:GetX()and reference.y==city:GetY(),'NREC_STORE_REFERENCE_CHANGED')
 local token,id,x,y=reference.token,reference.cityID,reference.x,reference.y
 local key=M.Key(family,token)
 -- Only detached scalars are captured. Every guard resolves this exact native
 -- location and retains original Store admission/binding/lifecycle protection.
 local function current()
  assert(P.IsTestPlayer(pid),'NREC_STORE_SCOPE_UNAVAILABLE')
  -- Reuse the proved initial Store admission. Its pure live stamp rejects
  -- commit/fault/removal/owner/epoch/role changes; the fresh canonical native
  -- reference below independently checks owner/id/location/raw binding.
  local stamp=store.CarrierReferenceStamp(pid,id,x,y,token)
  assert(type(stamp)=='string'and #stamp>0 and #stamp<=512,'NREC_STORE_LIFECYCLE_UNAVAILABLE')
  local c=assert(CityManager.GetCityAt(x,y),'NREC_STORE_CITY_UNAVAILABLE')
  local native=SPCNetworkInput.Reference(c)
  assert(c:GetOwner()==pid and c:GetID()==id,'NREC_STORE_REFERENCE_CHANGED')
  assert(store.CarrierReferenceStamp(pid,id,x,y,token)==stamp,'NREC_STORE_LIFECYCLE_CHANGED')
  return {reference=native,stamp=stamp}
 end
 local initial=current()
 local cell=SPCNetworkRecoveryCell.New(family,function()return Game:GetProperty(key)end,
  function(value)
   assert(type(value)=='string'and #value<=SPCNetworkRecoveryModel.MaxBytes+1,'NREC_STORE_VALUE_INVALID')
   P.SetProperty(Game,key,value) -- keep existing read barriers/counter/UI epoch
  end,current)
 return cell,initial
end
