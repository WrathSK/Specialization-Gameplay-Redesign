"""Real Tradition effect takeover at the established Store/projection boundary."""
import unittest

from refactor_harness import measure
from test_refactor_s5d4c7 import fixture


class TraditionFactResponsibility(unittest.TestCase):
    def test_unavailable_owner_holds_a_fact_until_the_named_wake(self):
        lua = fixture()
        lua.execute("""
local fc=shared.FactChanges
local name='Binding_ResearchTraditionEffects'
local bindings=shared.FactBindings
local n=T.writes()
shared.ResearchTraditionEffects=nil
T.governor(1)
Events.GovernorChanged.Fire(0) -- actual native-fact router
pp()
assert(fc.errors[name] and current(c)==5 and current(other)==5)
local delivered=fc.delivered
for i=1,20 do pp()end
assert(fc.delivered==delivered)
shared.ResearchTraditionEffects=effects
assert(bindings.Wake('ResearchTraditionEffects','OWNER_RESTORED',fc.sequence,{player=0}))
fc.Flush();bindings.Flush()
assert(not fc.errors[name] and current(c)==5 and current(other)==5)
Events.GameCoreEventPublishComplete.Fire()
assert(current(c)==0 and current(other)==0 and T.writes()==n)
""")

    def test_startup_keeps_taken_work_and_visits_once_when_store_becomes_ready(self):
        lua = fixture(wait_for_store=True)
        lua.execute("""
local fc=shared.FactChanges
local name='Binding_ResearchTraditionEffects'
local store=shared.CityProgressionStore
local visit=store.VisitTradition;local visits=0
store.VisitTradition=function(...)visits=visits+1;return visit(...)end
local function emit()
 fc.Emit({owner=0,cityID=c:GetID(),kinds={'HISTORY'},topic='TRADITION',cause='AGE_COMMITTED'})
end
emit();pp()
assert(not effects.ready and not fc.errors[name] and current(c)==0 and visits==0)
readyStore()
Events.GameCoreEventPublishComplete.Fire()
assert(effects.ready and current(c)==5 and visits==1)
pp()
assert(not fc.errors[name] and current(c)==5 and visits==1)
""")

    def test_grouped_marks_keep_one_owner_visit_and_same_turn_recomputation(self):
        lua = fixture()
        lua.execute("""
local fc=shared.FactChanges;local store=shared.CityProgressionStore
local read=store.VisitTradition;local visits=0
store.VisitTradition=function(pid,fn)
 assert(pid==0,'UNRELATED_OWNER_VISIT')
 visits=visits+1;return read(pid,fn)
end
local original=P.IsTestPlayer
P.IsTestPlayer=function(pid)
 if pid==3 then return false,nil,'INELIGIBLE'end
 return original(pid)
end
local function history(pid,city,topic)
 fc.Emit({owner=pid,cityID=city,kinds={'HISTORY'},topic=topic,cause='HISTORY_CHANGED'})
end
history(0,c:GetID(),'INSIGHTS');history(3,999,'TRADITION')
pp();assert(visits==0)
local old=T.writes();local writes=fxWrites
T.governor(1);Events.GovernorChanged.Fire(0)
history(0,c:GetID(),'TRADITION');history(0,other:GetID(),'TRADITION')
pp()
assert(visits==1 and current(c)==0 and current(other)==0)
T.governor(4);Events.GovernorChanged.Fire(0)
pp()
assert(visits==2 and current(c)==5 and current(other)==5 and fxWrites-writes==4 and T.writes()==old)
""")
        measure('tradition_owner_delivery', {
            'owner_visits_for_three_relevant_scopes': 1,
            'owner_visits_for_unrelated_topic_and_foreign_owner': 0,
            'visits_for_two_changes_same_turn': 2,
            'history_writes_from_effect': 0,
        })

    def test_unreadable_player_is_held_and_a_new_related_fact_recovers(self):
        lua = fixture()
        lua.execute("""
local fc=shared.FactChanges;local name='Binding_ResearchTraditionEffects'
local original=P.IsTestPlayer
P.IsTestPlayer=function(pid)
 if pid==0 then return false,nil,'UNKNOWN'end
 return original(pid)
end
local function emit()
 fc.Emit({owner=0,cityID=c:GetID(),kinds={'HISTORY'},topic='TRADITION',cause='AGE_COMMITTED'})
end
T.governor(1);emit();pp()
assert(fc.errors[name] and current(c)==5)
P.IsTestPlayer=original
pp();assert(current(c)==5 and fc.errors[name])
emit();pp();assert(not fc.errors[name] and current(c)==0)
""")
