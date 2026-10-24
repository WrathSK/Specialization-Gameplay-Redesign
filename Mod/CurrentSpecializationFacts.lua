-- P0-A read facade. EffectiveFacts remains the existing progression authority.
SPCCurrentSpecializationFacts={}
function SPCCurrentSpecializationFacts.Read(P,shared,pid,city)
 local ok,f=pcall(shared.EffectiveFacts.Read,pid,city)
 if not ok then return {validity='UNKNOWN',reason=tostring(f)} end
 return {validity='VERIFIED',identity=f.specialization,potential=f.potential,active=f.active,
  activeStatus=f.activeStatus,token=f.token,first=f.first and SPCDistrictCompleteness.Clone(f.first)}
end

-- Optional read-only projection shares the real EffectiveFacts guard; legacy
-- profiles retain their original direct reads and independent policy checks.
function SPCCurrentSpecializationFacts.Inspect(P,shared,pid,city,project)
 local service=shared.EffectiveFacts
 if not service.Inspect then return project(SPCCurrentSpecializationFacts.Read(P,shared,pid,city),function(_,read)return read()end)end
 return service.Inspect(pid,city,function(f,workers)
  local current={validity='VERIFIED',identity=f.specialization,potential=f.potential,active=f.active,
   activeStatus=f.activeStatus,token=f.token,first=f.first and SPCDistrictCompleteness.Clone(f.first)}
  return project(current,workers)
 end)
end
