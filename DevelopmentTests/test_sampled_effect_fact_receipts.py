"""Current sampled effects take scoped fact work without waking their UI samplers twice."""
import unittest

from refactor_harness import ROOT, measure
from test_refactor_s4a import industry, load_industry_ui
from test_refactor_s5d1 import cross


def research():
    lua = cross()
    for name in ('FactChanges', 'FactConsumerBindings'):
        lua.execute((ROOT / 'Mod' / f'{name}.lua').read_text())
    lua.execute("""
fc=SPCFactChanges.New(shared);bindings=SPCFactConsumerBindings.New(shared)
function emit()
 fc.Emit({owner=0,cityID=1,kinds={'D'},cause='RELATED_DEPTH'})
end
function drain()fc.Flush();bindings.Flush()end
""")
    return lua


class SampledEffectReceipts(unittest.TestCase):
    def test_named_research_wake_does_not_rearm_the_ui_sampler(self):
        lua = research()
        lua.execute("""
local revision=d.sampleRevision or 0;local before=sends
local unrelated=cities[2];unrelated.GetBuildings=function()error('UNRELATED_CITY_TOUCHED')end
local attempted=0;local accept=d.AcceptFact
d.AcceptFact=function(scope)
 assert(scope.player==0 and scope.city==1)
 attempted=attempted+1;return accept(scope)
end
d.busy=true;emit();fc.Flush()
assert((d.sampleRevision or 0)==revision and attempted==0)
bindings.Flush()
assert(d.sampleRevision==revision+1 and attempted==1 and fc.errors.Binding_ResearchCross)
d.busy=false;drain();assert(attempted==1)
assert(bindings.Wake('ResearchCross','OWNER_READY',fc.sequence,{player=0,city=1}))
drain()
assert(d.sampleRevision==revision+1 and attempted==2 and not fc.errors.Binding_ResearchCross)
assert(sends==before)
for i=1,100 do drain()end
assert(attempted==2 and sends==before)
""")
        measure('ordered_cross_research_scope', {
            'new_fact_sampler_wakes': 1, 'extra_sampler_wakes_on_receiver_recovery': 0,
            'unrelated_city_visits': 0,
        })

    def test_research_pending_sample_is_consumed_by_real_ui_response(self):
        lua = research()
        lua.execute("""
local revision=d.sampleRevision or 0;local before=sends
local writesBefore=writes
local old=d.plans[0][1].science
d.samples[0]=nil;districts[13].base=14
emit();drain()
assert(d.errors[0][1]=='CROSS_SAMPLE_PENDING' and not fc.errors.Binding_ResearchCross)
assert(d.sampleRevision==revision+1 and sends==before and writes==writesBefore)
pulse()
assert(sends==before+1 and not d.errors[0][1] and d.plans[0][1].science>old)
local count=sends;for i=1,100 do drain();pulse()end
assert(sends==count and not fc.errors.Binding_ResearchCross)
""")

    def test_industry_busy_scope_is_retained_and_reentrant_depth_gets_its_own_receipt(self):
        lua = industry(with_depth=True)
        load_industry_ui(lua)
        lua.execute("""
fc=shared.FactChanges;bindings=shared.FactBindings
function drain()fc.Flush();bindings.Flush()end
local function emit()
 fc.Emit({owner=0,cityID=2,kinds={'D'},cause='DISTRICT_FACTS_DIRTY'})
end
local called=0;local accept=d.AcceptFact
d.AcceptFact=function(s)
 assert(s.player==0 and s.city==2)
 called=called+1;local done=accept(s)
 if called==2 then emit();fc.Flush();assert(not bindings.Flush())end
 return done
end
local previous=sends;local revision=d.sampleRevision or 0
cities[1].GetBuildings=function()error('UNRELATED_CITY_TOUCHED')end
d.busy=true;emit();drain()
assert(called==1 and fc.errors.Binding_IndustrySupport)
d.busy=false;drain();assert(called==1)
assert(bindings.Wake('IndustrySupport','OWNER_READY',fc.sequence,{player=0,city=2}))
drain();assert(called==2)
bindings.Flush()
assert(called==3 and not fc.errors.Binding_IndustrySupport)
assert((d.sampleRevision or 0)==revision and sends==previous and d.ReadBase(0,cities[2])==6)
for i=1,100 do drain()end
assert(called==3)
""")
