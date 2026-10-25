-- Raw, call-local site reads only. No startup, cache, qualification or write owner.
SPCUnitSiteFacts={}
local M=SPCUnitSiteFacts
function M.Districts(P,pid,c)
 local out={};local id=c:GetID();assert(c:GetOwner()==pid,'OWNER_CHANGED')
 local function take(d,localRead)
  assert(d,'UNIT_SITE_DISTRICT_UNKNOWN');P.Count('district_scan')
  local owner=d:GetCity()
  if localRead then assert(owner and type(owner:GetOwner())=='number'and type(owner:GetID())=='number','UNIT_SITE_CITY_UNKNOWN')end
  if owner and owner:GetOwner()==pid and owner:GetID()==id then out[#out+1]=d end
 end
 local getter=P.Field(c,'GetDistricts')
 local ds=getter and getter(c)
 if ds and type(P.Field(ds,'GetNumDistricts'))=='function'and type(P.Field(ds,'GetDistrictByIndex'))=='function'then
  local n=ds:GetNumDistricts();assert(type(n)=='number'and n>=0 and n<math.huge and n%1==0,'UNIT_SITE_DISTRICTS_UNKNOWN')
  for i=0,n-1 do take(ds:GetDistrictByIndex(i),true)end
 elseif ds and type(P.Field(ds,'Members'))=='function'then
  for _,d in ds:Members()do take(d,true)end
 else
  -- Compatibility only when the city-local API is absent; a failed read above
  -- remains UNKNOWN and never becomes an empty, apparently successful list.
  for _,d in Players[pid]:GetDistricts():Members()do take(d)end
 end
 return out
end
function M.DistrictCity(P,pid,u)
 local get=CityManager and CityManager.GetDistrictAt
 if type(get)~='function'then return nil,false end
 local d=get(u:GetX(),u:GetY())
 if not d then return nil,false end
 local c=d:GetCity();assert(c and type(c:GetOwner())=='number','UNIT_SITE_CITY_UNKNOWN')
 if c:GetOwner()~=pid then return nil,false end
 return c,true
end
function M.CityAt(P,pid,u)
 local c,known=M.DistrictCity(P,pid,u)
 if c then return c,true end
 local get=Cities and Cities.GetPlotPurchaseCity
 if type(get)~='function'then return nil,false end
 local plot=assert(Map.GetPlot(u:GetX(),u:GetY()),'UNIT_SITE_PLOT_UNKNOWN')
 local owner=plot:GetOwner();assert(type(owner)=='number','UNIT_SITE_OWNER_UNKNOWN')
 if owner~=pid then return nil,true end
 c=get(plot)
 if not c then return nil,false end
 assert(type(c:GetOwner())=='number','UNIT_SITE_CITY_UNKNOWN')
 if c:GetOwner()~=pid then return nil,false end
 return c,true
end
