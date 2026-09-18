-- P0-A read facade. EffectiveFacts remains the existing progression authority.
SPCCurrentSpecializationFacts={}
function SPCCurrentSpecializationFacts.Read(P,shared,pid,city)
 local ok,f=pcall(shared.EffectiveFacts.Read,pid,city)
 if not ok then return {validity='UNKNOWN',reason=tostring(f)} end
 return {validity='VERIFIED',identity=f.specialization,potential=f.potential,active=f.active,
  activeStatus=f.activeStatus,token=f.token,first=f.first and SPCDistrictCompleteness.Clone(f.first)}
end
