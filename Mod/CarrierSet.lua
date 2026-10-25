-- Ordered exact carrier mechanics only; caller owns eligibility, events and loss policy.
SPCCarrierSet={}
function SPCCarrierSet.Define(P,entries,resolve,errors)
 local d={};local descriptors={};local names,keys={},{}
 for _,v in ipairs(entries)do
  assert(v.key~=nil and type(v.name)=='string'and not names[v.name]and not keys[v.key],'CARRIER_DESCRIPTOR_INVALID')
  descriptors[#descriptors+1]={key=v.key,name=v.name};names[v.name]=true;keys[v.key]=true
 end
 local definitions,owned
 local function initialize()
  if definitions then return end
  local nextDefinitions,nextOwned={},{}
  for _,v in ipairs(descriptors)do local id=resolve(v.name,v.key);nextDefinitions[v.key]=id;nextOwned[id]=true end
  definitions,owned=nextDefinitions,nextOwned -- publish only a complete definition set
 end
 function d.Initialize()initialize()end
 function d.Index(key)initialize();return definitions[key]end
 function d.Owns(id)return owned~=nil and owned[id]==true end -- health hooks never resolve rows
 function d.Names()
  local out={};for _,v in ipairs(descriptors)do out[#out+1]=v.name end;return out
 end
 function d.Observe(city,wanted)
  initialize();local plan={}
  for _,v in ipairs(descriptors)do
   local id=definitions[v.key];local present=P.HasBuilding(city:GetBuildings(),id)
   assert(type(present)=='boolean',errors.read)
   plan[#plan+1]={key=v.key,id=id,present=present,wanted=wanted[v.key]==true}
  end
  return plan -- fresh complete preflight; no city/native handles retained by the set
 end
 function d.Apply(city,wanted,health,confirmed)
  local plan=d.Observe(city,wanted)
  for _,adding in ipairs({false,true})do for _,v in ipairs(plan)do
   if v.wanted==adding and v.present~=v.wanted then
    if adding then health.Create(city,v.id)else health.Remove(city,v.id)end
    assert(P.HasBuilding(city:GetBuildings(),v.id)==v.wanted,errors.write)
    if confirmed then confirmed(v.key,v.id,v.wanted)end
    v.present=v.wanted
   end
  end end
  return plan
 end
 function d.Exit(shared,city,loss)
  return shared.CityProgressionStore.RemoveOwned(city,loss,d.Names())
 end
 return d
end
