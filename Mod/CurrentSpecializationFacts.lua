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
function SPCCurrentSpecializationFacts.Inspect(P,shared,pid,city,project,negativeAnchor)
 local service=shared.EffectiveFacts
 if not service.Inspect then local function fresh(_,read)return read()end;return project(SPCCurrentSpecializationFacts.Read(P,shared,pid,city),fresh,fresh)end
 local function use(f,workers,anchors)
  local current={validity='VERIFIED',identity=f.specialization,potential=f.potential,active=f.active,
   activeStatus=f.activeStatus,token=f.token,first=f.first and SPCDistrictCompleteness.Clone(f.first)}
  return project(current,workers,anchors)
 end
 return service.Inspect(pid,city,function(f,workers,anchors)
  if negativeAnchor and f.activeStatus=='UNKNOWN_GOVERNOR' then
   -- Opt-in negative inspection needs the full existing parent/reference and
   -- write-phase checks, even when its caller did not declare a shared phase.
   assert(type(service.WithPhase)=='function','CURRENT_ANCHOR_READ_PHASE_UNKNOWN')
   return service.WithPhase('CURRENT_ANCHOR_NEGATIVE',function()return service.Inspect(pid,city,use)end)
  end
  return use(f,workers,anchors)
 end)
end

-- Only a reliable structural negative may override UNKNOWN_GOVERNOR. Intact or
-- unreadable anchors do not invent an ACTIVE level; ordinary policy still holds.
function SPCCurrentSpecializationFacts.AnchorUnavailable(P,shared,pid,city,f,anchors)
 if f.active~=nil or f.activeStatus~='UNKNOWN_GOVERNOR' then return false end
 assert(f.validity=='VERIFIED' and type(f.identity)=='string' and type(f.token)=='string'
  and type(f.first)=='table','CURRENT_ANCHOR_FOUNDATION_UNKNOWN')
 local raw=SPCSpecialistSupport.ReadAnchor(P,pid,city,{first=f.first,specialization=f.identity},nil,anchors)
 if raw.present==false then return true end
 assert(raw.present==true,'CURRENT_ANCHOR_UNKNOWN')
 if raw.owner~=pid or raw.cityID~=city:GetID() or raw.type~=f.first.type or P.Family(raw.type)~=f.identity then return true end
 assert(type(raw.complete)=='boolean' and type(raw.pillaged)=='boolean','CURRENT_ANCHOR_UNKNOWN')
 return not raw.complete or raw.pillaged
end
