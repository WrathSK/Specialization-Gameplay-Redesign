"""Scoped D publisher, binding order and the real Research Infrastructure writer."""
import unittest

from refactor_harness import ROOT, legacy_source_observation, measure
from test_refactor_s5d1 import research
from test_scoped_depth_write import install_native_wrappers


def fixture():
    lua = research()
    with legacy_source_observation():
        lua.execute("""
local create,remove=P.CreateBuilding,P.RemoveBuilding
for _,city in pairs(cities)do
 city:GetBuildQueue().CreateBuilding=create
 local get=city.GetBuildings
 city.GetBuildings=function()local b=get();b.RemoveBuilding=remove;return b end
end
""")
        install_native_wrappers(lua)
        for name in ('FactChanges', 'FactConsumerBindings'):
            lua.execute((ROOT / 'Mod' / (name + '.lua')).read_text())
        lua.execute("""
fc=SPCFactChanges.New(shared);bindings=SPCFactConsumerBindings.New(shared)
infra=shared.ResearchInfrastructure
receiptName='Binding_ResearchInfrastructure'
function coefficient(city)
 local n=0
 for bit=0,3 do
  local id=P.Info('Buildings','BUILDING_SPC_RESEARCH_INFRA_'..bit).Index
  if city.carriers[id] then n=n+2^bit end
 end
 return n
end
function upgrade()
 setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY','BUILDING_JNR_LABORATORY'})
 svc.MarkDirty(0,1)
end
function drain()
 shared.EffectiveFacts.WithPhase('FACT_PROPAGATION',function()fc.Flush();bindings.Flush()end)
end
infra.Audit({player=0,city=1})
assert(infra.ready and coefficient(c)==3)
""")
    return lua


class OrderedReceipts(unittest.TestCase):
    def test_one_combined_fact_reuses_the_existing_order_and_city(self):
        lua = fixture()
        lua.execute("""
local names={ResearchInfrastructure=true,ResearchApply=true,ResearchChair=true}
local calls={}
P.Observe=function(kind,name)if kind=='audit' and names[name]then calls[#calls+1]=name end end
local peer=cities[2];local unchanged=coefficient(peer)
local peerBuildings=peer.GetBuildings
peer.GetBuildings=function()error('UNRELATED_CITY_TOUCHED')end
local visits,captures,previousWrites=counters.city_scan or 0,counters.dc_capture or 0,writes
upgrade()
fc.Emit({owner=0,cityID=1,kinds={'WORKERS'},cause='RELATED_WORKERS'})
shared.EffectiveFacts.WithPhase('FACT_PROPAGATION',function()
 fc.Flush()
 assert(coefficient(c)==3 and #calls==0 and fc.retained>0)
 bindings.Flush()
end)
assert(coefficient(c)==6 and not fc.errors[receiptName])
assert(table.concat(calls,',')=='ResearchInfrastructure,ResearchApply,ResearchChair')
assert(counters.city_scan-visits==3 and counters.dc_capture-captures==2 and writes-previousWrites==4)
peer.GetBuildings=peerBuildings;assert(coefficient(peer)==unchanged)
local n=fc.delivered;for i=1,50 do drain()end
assert(fc.delivered==n and #calls==3)
""")
        measure('ordered_research_delivery', {'combined_city_facts': 2, 'infra_audits': 1,
                'city_visits': 3, 'depth_captures': 2, 'carrier_writes': 4,
                'existing_audit_order': ['ResearchInfrastructure', 'ResearchApply', 'ResearchChair']})

    def test_target_refusal_is_held_and_a_named_wake_never_replays_siblings(self):
        lua = fixture()
        lua.execute("""
local sibling=0
P.Observe=function(kind,name)if kind=='audit' and name=='ResearchChair'then sibling=sibling+1 end end
infra.busy=true;upgrade();drain()
assert(fc.errors[receiptName] and sibling==1 and coefficient(c)==3)
local n=fc.delivered
infra.busy=false;for i=1,50 do drain()end
assert(coefficient(c)==3 and fc.delivered==n)
assert(bindings.Wake('ResearchInfrastructure','TARGET_READY',fc.sequence,{player=0,city=1}))
drain()
assert(not fc.errors[receiptName] and sibling==1 and coefficient(c)==6)
""")

    def test_unavailable_city_collection_does_not_acknowledge_owner_work(self):
        lua = fixture()
        lua.execute("""
local player=Players[0];local get=player.GetCities
upgrade()
player.GetCities=function()return nil end
drain()
assert(coefficient(c)==3 and fc.errors[receiptName])
player.GetCities=get
drain();assert(coefficient(c)==3 and fc.errors[receiptName])
svc.MarkDirty(0,1);drain()
assert(coefficient(c)==6 and not fc.errors[receiptName])
""")

    def test_unavailable_player_keeps_carriers_during_an_existing_city_retry(self):
        lua = fixture()
        lua.execute("""
local buildingReads=c.GetBuildings
c.GetBuildings=function()error('CITY_TEMPORARILY_UNREADABLE')end
upgrade();drain()
assert(coefficient(c)==3 and infra.errors[0][1] and not fc.errors[receiptName])
c.GetBuildings=buildingReads
local eligibility=P.IsTestPlayer
P.IsTestPlayer=function(pid)if pid==0 then return false,nil,'UNKNOWN'end;return eligibility(pid)end
fc.Emit({owner=0,cityID=1,kinds={'D'},cause='RELATED_WHILE_UNREADABLE'});drain()
assert(coefficient(c)==3 and fc.errors[receiptName])
P.IsTestPlayer=eligibility
svc.MarkDirty(0,1);drain()
assert(coefficient(c)==6 and not fc.errors[receiptName])
""")

    def test_new_scoped_fact_survives_reentry_before_old_completion(self):
        lua = fixture()
        lua.execute("""
local accept=infra.AcceptFact;local visits=0
infra.AcceptFact=function(scope)
 local accepted=accept(scope);visits=visits+1
 if visits==1 then
  setBuildings(d,{'BUILDING_LIBRARY'})
  svc.MarkDirty(0,1)
  fc.Flush();assert(not bindings.Flush())
 end
 return accepted
end
upgrade();drain()
assert(visits==1 and coefficient(c)==6)
bindings.Flush()
assert(visits==2 and coefficient(c)==1 and not fc.errors[receiptName])
""")

    def test_closed_context_does_not_execute_a_collected_old_audit(self):
        lua = fixture()
        lua.execute("""
upgrade();fc.Flush();assert(coefficient(c)==3 and fc.retained>0)
SPCFactChanges.New(shared)
assert(not bindings.Flush() and coefficient(c)==3 and fc.closed and fc.retained==0)
""")
