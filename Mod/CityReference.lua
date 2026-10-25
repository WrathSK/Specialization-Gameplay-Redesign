-- Scalar locator only, never proof of specialization, ACTIVE or transaction access.
-- Current Gameplay uses the Store index token. Raw City Properties are confined
-- to isolated legacy profiles without the modern Store reference API.
SPCCityReference={}
local R=SPCCityReference
local function integer(v)return type(v)=='number'and v>=0 and v<1000000000 and v%1==0 end
local function native(c)
 local r={owner=c:GetOwner(),cityID=c:GetID(),x=c.GetX and c:GetX(),y=c.GetY and c:GetY()}
 assert(integer(r.owner)and integer(r.cityID),'CITY_REFERENCE_NATIVE_UNKNOWN')
 assert((r.x==nil and r.y==nil)or(integer(r.x)and integer(r.y)),'CITY_REFERENCE_LOCATION_UNKNOWN')
 return r
end
function R.Equal(a,b)
 return a.owner==b.owner and a.cityID==b.cityID and a.x==b.x and a.y==b.y and a.token==b.token and a.source==b.source
end
function R.Read(shared,c)
 local r=native(c);local store=shared.CityProgressionStore
 if store and type(store.ReferenceToken)=='function'then
  assert(r.x~=nil,'CITY_REFERENCE_LOCATION_UNKNOWN')
  r.token=store.ReferenceToken(c);r.source='STORE'
 else
  assert(not(store and store.UsesNewAuthority==true),'CITY_REFERENCE_STORE_UNAVAILABLE')
  r.token=c.GetProperty and c:GetProperty('SPC_DEV_BINDING_B013_TOKEN')or nil;r.source='LEGACY_NATIVE'
 end
 assert(r.token==nil or(type(r.token)=='string'and #r.token>0),'CITY_REFERENCE_TOKEN_UNKNOWN')
 local after=native(c)
 assert(r.owner==after.owner and r.cityID==after.cityID and r.x==after.x and r.y==after.y,'CITY_REFERENCE_CHANGED_DURING_READ')
 return r
end
local function atom(v)
 if v==nil then return 'nil;'end
 local s=type(v)=='number'and string.format('%.17g',v)or v
 assert(type(s)=='string','CITY_REFERENCE_ATOM_UNKNOWN')
 return type(v)..':'..#s..':'..s
end
function R.Key(r)
 return table.concat({atom(r.owner),atom(r.cityID),atom(r.x),atom(r.y),atom(r.source),atom(r.token)})
end
