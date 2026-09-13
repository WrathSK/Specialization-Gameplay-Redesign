-- Read-only family lookup using Districts + DistrictReplaces. No engine registration.
local M={}
local bases={DISTRICT_CAMPUS="CAMPUS",DISTRICT_THEATER="THEATER_SQUARE",
 DISTRICT_INDUSTRIAL_ZONE="INDUSTRIAL_ZONE",DISTRICT_COMMERCIAL_HUB="COMMERCIAL_HUB"}
function M.Build(districtRows,replacementRows)
 local ok,result=pcall(function()
  local known,parent={},{}
  for _,row in ipairs(districtRows) do
   assert(type(row.DistrictType)=="string" and not known[row.DistrictType],"DISTRICT_TYPE_INVALID")
   known[row.DistrictType]=true
  end
  for _,row in ipairs(replacementRows) do
   local child,base=row.CivUniqueDistrictType,row.ReplacesDistrictType
   assert(known[child] and known[base],"REPLACEMENT_ENDPOINT_MISSING")
   assert(not parent[child] or parent[child]==base,"REPLACEMENT_AMBIGUOUS")
   parent[child]=base
  end
  for base in pairs(bases) do assert(known[base],"BASE_DISTRICT_MISSING") end
  local mapping={}
  for district in pairs(known) do
   local seen,current={},district
   while parent[current] do
    assert(not seen[current],"REPLACEMENT_CYCLE");seen[current]=true
    assert(not bases[current],"CANONICAL_BASE_REPLACED")
    current=parent[current]
   end
   mapping[district]={family=bases[current] or "NON_V01",rootType=current}
  end
  return {status="READY",mapping=mapping}
 end)
 if not ok then return {status="UNKNOWN",reason=tostring(result)} end
 return result
end
function M.Resolve(registry,districtType)
 if type(registry)~="table" or registry.status~="READY" then return {status="UNKNOWN",reason="REGISTRY_UNAVAILABLE"} end
 local entry=registry.mapping[districtType]
 if not entry then return {status="UNKNOWN",reason="DISTRICT_NOT_IN_DATABASE"} end
 return {status="READY",mappingStatus="VALIDATED_FAMILY",family=entry.family,rootType=entry.rootType,districtType=districtType}
end
return M
