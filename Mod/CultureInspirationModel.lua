-- D0049: current collection diversity, never historical accumulation.
SPCCultureInspirationModel={PercentPerEra=3,MaxEras=7,Owned={}}
local M=SPCCultureInspirationModel
for e=1,M.MaxEras do M.Owned[e]='BUILDING_SPC_INSPIRATION_ERA_'..e end
local function integer(v)return type(v)=='number' and v>=0 and v<math.huge and v%1==0 end
function M.Plan(f,w)
 assert(f and f.validity=='VERIFIED','INSP_FACT_UNKNOWN')
 local out={status='INACTIVE',active=f.active,eras=0,percent=0}
 if f.identity~='CULTURE' then return out end
 assert(integer(f.potential),'INSP_POTENTIAL_UNKNOWN')
 if f.potential<4 then return out end
 assert(f.activeStatus=='KNOWN' and integer(f.active),'INSP_ACTIVE_UNKNOWN')
 if f.active<4 then return out end
 assert(w and w.hasConfirmed and w.availability=='KNOWN','INSP_COLLECTION_UNKNOWN')
 assert(integer(w.eraCount) and w.eraCount<=M.MaxEras,'INSP_ERA_RANGE_UNKNOWN')
 out.status='READY';out.eras=w.eraCount;out.percent=M.PercentPerEra*out.eras
 out.carrier=M.Owned[out.eras]
 return out
end
