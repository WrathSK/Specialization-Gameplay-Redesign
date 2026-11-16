-- Gameplay-only selection from detached UI observations. No native read/write.
SPCExpeditionEntry={}
function SPCExpeditionEntry.Select(raw)
 local function integer(n)return type(n)=='number' and n>=0 and n<math.huge and n%1==0 end
 local function city(c)
  assert(type(c)=='table' and getmetatable(c)==nil and integer(c.owner) and integer(c.id)
   and integer(c.x) and integer(c.y) and type(c.revealed)=='boolean','ENTRY_RAW_CITY')
 end
 assert(type(raw)=='table' and getmetatable(raw)==nil and raw.protocol==1,'ENTRY_RAW_PROTOCOL')
 city(raw.target)
 local target=raw.target
 local function copy(c)return {owner=c.owner,id=c.id,x=c.x,y=c.y}end
 if target.revealed then return copy(target)end -- original zero-enumeration fast path
 assert(type(raw.cities)=='table' and getmetatable(raw.cities)==nil,'ENTRY_RAW_CITIES')
 local n=0
 for k in pairs(raw.cities)do assert(integer(k) and k>=1 and k<=4096,'ENTRY_RAW_INDEX');n=n+1 end
 local best,bestD;local seen={}
 for i=1,n do
  local c=raw.cities[i];city(c)
  assert(not seen[c.id],'ENTRY_RAW_DUPLICATE');seen[c.id]=true
  if c.owner==target.owner and c.revealed then
   local d=c.distance
   if d==nil or d==false then d=math.abs(c.x-target.x)+math.abs(c.y-target.y)end
   assert(type(d)=='number' and d>=0 and d<math.huge,'ENTRY_RAW_DISTANCE')
   if not best or d<bestD or d==bestD and c.id<best.id then best,bestD=c,d end
  end
 end
 return best and copy(best)or nil
end
