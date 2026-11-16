"""O1 scoped D invalidation using actual Probe, EffectiveFacts and D owner."""
import unittest

from refactor_fixtures import depth_context
from refactor_harness import ROOT, legacy_source_observation
from test_refactor_s5d1 import research


def install_native_wrappers(lua):
    """Only engine-facing objects are doubles. Run the packaged write boundary."""
    lua.execute((ROOT / 'Mod/PerformanceCounters.lua').read_text())
    lua.execute("previousInclude=include;include=function()end")
    for module in ('Probe', 'EffectiveFacts'):
        lua.execute((ROOT / 'Mod' / (module + '.lua')).read_text())
    lua.execute("""
include=previousInclude;previousInclude=nil
local prior=shared.EffectiveFacts
SPCEffectiveFacts.Start(P,shared)
local facts=shared.EffectiveFacts
if prior then facts.Read=prior.Read;facts.Inspect=nil end
SPCP0.FactReadService=facts;SPCP0.Count=P.Count
SPCP0.Info=function(...)return P.Info(...)end
P.CreateBuilding=SPCP0.CreateBuilding;P.RemoveBuilding=SPCP0.RemoveBuilding
P.SetProperty=SPCP0.SetProperty
""")


def two_cities():
    ctx = depth_context()
    install_native_wrappers(ctx.lua)
    ctx.load('RuntimeWork')
    ctx.execute("""
local info=P.Info
P.Info=function(t,k)
 if t=='Buildings'and k==99 then return {Index=k,BuildingType='BUILDING_SPC_TEST_EFFECT',InternalOnly=true}end
 return info(t,k)
end
a,b=cities[1],cities[2]
a.native={};a.GetBuildQueue=function()return a.native end
a.native.CurrentlyBuilding=function()return 0 end
a.native.CreateBuilding=function(_,id)
 if onCreate then onCreate(id)end
 a.native[id]=true
 if throwAfter then error('APPLIED_THEN_THROW')end
end
local get=a.GetBuildings
a.GetBuildings=function()
 local object=get()
 object.RemoveBuilding=function(_,id)a.native[id]=nil end
 return object
end
health=SPCRuntimeWork.NativeHealth(P,shared,{},function(id)return id==99 end,function()end)
sample(1);sample(2);resetCounts()
""")
    return ctx


class ScopedDepthWrite(unittest.TestCase):
    def test_ten_related_mutations_refresh_own_city_and_keep_sibling_warm(self):
        ctx = two_cities()
        ctx.execute("""
for i=1,10 do
 if i%2==1 then health.Create(a,99)else health.Remove(a,99,100)end
 assert(sample(2).availability=='READY')
 if i==1 then firstRecapture=counts.dc_capture or 0 end
end
local total=counts.dc_capture or 0
assert(total==0,'UNRELATED_RECAPTURE_FIRST_'..firstRecapture..'_TEN_'..total)
assert(sample(1).availability=='READY' and counts.dc_capture==1)
health.Create(a,99)
assert(sample(1).availability=='READY' and counts.dc_capture==2,'SECOND_SAME_TURN_LOST')
assert(shared.EffectiveFacts.Version()==22)
""")

    def test_reentry_failure_and_unproven_scope_remain_fenced(self):
        ctx = two_cities()
        ctx.execute("""
onCreate=function()
 assert(sample(1).availability=='TEMPORARILY_UNAVAILABLE')
 assert(sample(2).availability=='READY')
end
throwAfter=true;assert(not pcall(health.Create,a,99)and a.native[99])
assert((counts.dc_capture or 0)==0)
assert(sample(1).availability=='READY' and counts.dc_capture==1)
sample(2);assert(counts.dc_capture==1)
throwAfter=false;onCreate=function()
 assert(sample(2).availability=='TEMPORARILY_UNAVAILABLE')
end
P.CreateBuilding(a.native,1)
sample(2);assert(counts.dc_capture==2,'UNKNOWN_SCOPE_DROPPED_GLOBAL_FENCE')
""")

    def test_no_stale_inflight_sample_and_no_idle_retry(self):
        ctx = two_cities()
        ctx.execute("""
local get=b.GetBuildings;local once=true
b.GetBuildings=function()
 if once then once=false;health.Create(a,99)end
 return get()
end
shared.DistrictCompleteness.MarkDirty(0,2)
local v=sample(2);assert(v.error=='DC_WRITE_DURING_CAPTURE'and v.value.domains.DISTRICT_CAMPUS.value==1)
local n=counts.dc_capture
for i=1,100 do assert(sample(2).availability=='TEMPORARILY_UNAVAILABLE')end
assert(counts.dc_capture==n)
b.token='NEW'
assert(sample(2).availability=='READY'and counts.dc_capture==n+1)
""")

    def test_actual_three_research_writers_do_not_recapture_other_city(self):
        lua = research()
        with legacy_source_observation():
            lua.execute("""
local create,remove=P.CreateBuilding,P.RemoveBuilding
for _,city in pairs(cities)do
 local q=city:GetBuildQueue();q.CreateBuilding=create
 local get=city.GetBuildings
 city.GetBuildings=function()local b=get();b.RemoveBuilding=remove;return b end
end
""")
            install_native_wrappers(lua)
            lua.execute("""
local peer=cities[2]
local function peerDepth()return svc.ReadFacts(0,peer,peer.token)end
assert(peerDepth().value.domains.DISTRICT_CAMPUS.value==3)
local initial=peerDepth().revision
local industry=addDistrict(c,20,'DISTRICT_INDUSTRIAL_ZONE')
setBuildings(industry,{'BUILDING_IZ_WATER_MILL','BUILDING_WORKSHOP'})
setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY','BUILDING_JNR_LABORATORY'})
svc.MarkDirty(0,1)
local extra=0
for _,name in ipairs({'ResearchApply','ResearchInfrastructure','ResearchChair'})do
 local owner=shared[name];local w=writes
 owner.Audit({player=0,city=1})
 assert(writes>w,name..':'..tostring(owner.errors[0]and owner.errors[0][1]))
 local n=counters.dc_capture
 local v=peerDepth()
 assert(v.availability=='READY'and v.revision==initial)
 extra=extra+counters.dc_capture-n
end
assert(extra==0,'RESEARCH_UNRELATED_RECAPTURE_'..extra)
""")


if __name__ == '__main__':
    unittest.main()
