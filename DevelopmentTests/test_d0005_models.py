"""D0005 topology/industry/owner-transfer fixtures. No actual game operations."""
from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
l=LuaRuntime(unpack_returned_tuples=True)
for name,file in [('Network','NetworkState.lua'),('Industry','IndustryNetwork.lua'),('State','CitySpecializationState.lua')]:
    l.globals()[name]=l.execute((p/file).read_text())
l.execute('''
local ctx={revision=1,sources={C={owner=0,kind="RESEARCH",activeLevel=3},
 H={owner=0,kind="CULTURE",activeLevel=2}},centers={C={owner=0,isCapital=true},H={owner=0}}}
local routes={status="READY",revision=1,routes={},orderedKeys={}}
local n=Network.Derive(routes,ctx)
assert(n.centers.C.connectedSources.C.CAPITAL_SELF_CONNECTION and not next(n.recipients))
assert(not n.centers.H.connectedSources.H and #routes.orderedKeys==0)
local function route(k,a,b)
 routes.orderedKeys[#routes.orderedKeys+1]=k
 routes.routes[k]={originUID=a,destinationUID=b,originPlayer=0,domestic=true}
end
route("distribution","C","A");n=Network.Derive(routes,ctx)
assert(n.recipients.RESEARCH.A and not n.recipients.RESEARCH.C)
ctx.centers.C.isCapital=false;ctx.centers.H.isCapital=true;n=Network.Derive(routes,ctx)
assert(not n.recipients.RESEARCH and n.centers.H.connectedSources.H)
ctx.centers.C.isCapital=true;ctx.sources.C.owner=1;n=Network.Derive(routes,ctx)
assert(not n.centers.C.connectedSources.C)
-- Two industrial providers, only one supplies the requested building template.
ctx={revision=1,sources={I1={owner=0,kind="INDUSTRY",activeLevel=1,templateRevision=1},
 I4={owner=0,kind="INDUSTRY",activeLevel=4,templateRevision=2},
 I4b={owner=0,kind="INDUSTRY",activeLevel=4,templateRevision=3}},centers={H={owner=0},J={owner=0}}}
routes={status="READY",revision=1,routes={},orderedKeys={}}
route("s1","I1","H");route("s4","I4","H");route("s4b","I4b","J")
route("d1","H","A");route("d2","J","A");route("d3","J","B")
local details={I1={templateRevision=1,templates={LIBRARY=true}},I4={templateRevision=2,templates={FACTORY=true},productionOutput=18},
 I4b={templateRevision=3,templates={MUSEUM=true},productionOutput=31}}
local function calc()
 local r=Industry.FromState(Network.Derive(routes,ctx),0,details,"MOCK_ONLY")
 assert(r.status=="READY_OFFLINE_INDUSTRY",r.reason);return r
end
local r=calc()
assert(r.recipients.A.production==31 and r.recipients.A.discount==40)
assert(Industry.DiscountFor(r,"A","LIBRARY","GOLD")==40)
assert(Industry.DiscountFor(r,"A","LIBRARY","FAITH")==0)
assert(Industry.DiscountFor(r,"A","UNKNOWN","GOLD")==0)
assert(Industry.DiscountFor(r,"B","LIBRARY","GOLD")==0) -- no empire-wide leakage
assert(r.recipients.A.templateSources.LIBRARY.I1 and r.recipients.A.productionSources.I4b)
-- Duplicate support must not add outputs. Source disappearance removes ONLY its contribution.
route("duplicate","H","A");assert(calc().recipients.A.production==31)
ctx.sources.I4b=nil;r=calc();assert(r.recipients.A.production==18 and not r.recipients.A.templates.MUSEUM and not r.recipients.B)
ctx.sources.I4.activeLevel=2;r=calc();assert(r.recipients.A.production==0 and r.recipients.A.discount==20)
ctx.sources.I4=nil;r=calc();assert(r.recipients.A.discount==10 and not r.recipients.A.templates.FACTORY)
ctx.sources.I1=nil;r=calc();assert(not next(r.recipients))
ctx.sources.I1={owner=0,kind="INDUSTRY",activeLevel=1,templateRevision=9}
assert(Industry.FromState(Network.Derive(routes,ctx),0,details,"MOCK_ONLY").status=="UNKNOWN")
ctx.sources.I1.templateRevision=1
local top=Network.Derive(routes,ctx)
assert(Industry.FromState(top,0,details,"GAMEPLAY").status=="UNKNOWN")
top.status="READY_SHADOW_PROVENANCE_ONLY";assert(Industry.FromState(top,0,details,"MOCK_ONLY").status=="UNKNOWN")
-- Explicit SAME-city conquest: preserve permanent investment/templates, discard old cache.
local old={contextSource="MOCK_ONLY",eligibility={contextSource="MOCK_ONLY",player=0,status="ENABLED"},isTestCivilization=true,present=true,owner=0,cityUID="permanent-fixture",freshFoundationObserved=true}
local new={contextSource="MOCK_ONLY",isTestCivilization=false,present=true,owner=1,cityUID=old.cityUID}
local f=State.NewCity(old).facts
f=State.Complete(f,old,{status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",cityUID=old.cityUID,owner=0,eventID="first",
 districts={{family="CAMPUS",complete=true,districtUID="campus",mappingStatus="VALIDATED_FAMILY"}}}).facts
for i=1,3 do f=State.CommitInvestment(f,old,{contextSource="MOCK_ONLY",status="COMMITTED",cityUID=old.cityUID,owner=0,
 unitType="SETTLER",unitConsumed=true,id="receipt"..i,unitUID="unit"..i,expectedRevision=f.revision}).facts end
f.ownedTemplates={LIBRARY=true};f.active=4;f.receivedTemplates={MUSEUM=true};f.networkStrength=99
local proof={contextSource="MOCK_ONLY",status="VERIFIED_SAME_CITY",cityUID=old.cityUID,fromOwner=0,toOwner=1,expectedRevision=f.revision}
assert(State.Restore(f,new).status=="UNKNOWN")
assert(State.TransferOwnership(f,old,new,{}).status=="UNKNOWN")
local transfer=State.TransferOwnership(f,old,new,proof);assert(transfer.status=="READY",transfer.reason)
local g=transfer.facts
assert(g.owner==1 and g.specialization=="RESEARCH" and g.potential==4 and g.investments.receipt3=="unit3")
assert(g.ownedTemplates.LIBRARY and not g.receivedTemplates and not g.active and not g.networkStrength)
assert(f.owner==0 and f.active==4) -- original not mutated
assert(State.TransferOwnership(g,old,new,proof).status=="UNKNOWN") -- old proof cannot replay
-- Recapture from non-test owner also retains facts; no automatic effects for foreign civ.
proof.fromOwner=1;proof.toOwner=0;proof.expectedRevision=g.revision
local back=State.TransferOwnership(g,new,old,proof);assert(back.status=="READY")
assert(State.Derive(back.facts,old,{owner=0,cityUID=old.cityUID,governorGateStatus="KNOWN",governorLevelCeiling=1}).active==1)
assert(back.facts.potential==4 and back.facts.ownedTemplates.LIBRARY)
new.cityUID="different-city";assert(State.TransferOwnership(f,old,new,proof).status=="UNKNOWN")
assert(State.Restore(nil,old).status=="UNKNOWN") -- missing history is a compatibility limitation, not an unresolved design rule
''')
print('LOCAL_SIMULATION_PASS: capital self-source only; per-recipient industry max/union/cross-source discount; withdrawal/ACTIVE changes; Gold-only candidate; verified conquest/recapture preservation; no runtime effects.')
