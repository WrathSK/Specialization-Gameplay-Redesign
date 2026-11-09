"""Confirmed source and route losses survive an interrupted passive effect write."""
import unittest

from refactor_harness import measure
from test_network_effect_write_boundary import two_standardization_targets
from test_pu11_package_absence import scalars
from test_refactor_s4b import culture, warm_commerce
from test_refactor_s6d import get_index


class Commerce(unittest.TestCase):
    def test_confirmed_ineligible_source_stays_excluded_when_identity_becomes_unreadable(self):
        for fails in (False, True):
            with self.subTest(fails=fails):
                game = warm_commerce()
                result = scalars(game.execute("""
local fails=...
local c=cities[2];local remove=P.RemoveBuilding
if fails then P.RemoveBuilding=function(b,id)
 if b.city==c and id=='BUILDING_SPC_COMMERCE_GOLD_3'then return end
 return remove(b,id)
end end
cities[1].kind='NONE';com.SourceChanged(0,1)
assert(ownedGold(c)==(fails and 14 or 6))
assert(view(2).stage==(fails and 'HELD' or 'READY'))
P.RemoveBuilding=remove
cities[1].identityFail=true;com.SourceChanged(0,1)
local v=view(2)
return {gold=ownedGold(c),source=v.domains[1].source,stage=v.stage,
 strict=com.TransactionCurrent(0,2),proof=net.TransactionCurrent(0),properties=propertyWrites}
""", fails))
                self.assertEqual(result, {'gold': 6, 'source': 2, 'stage': 'RETAINED',
                                          'strict': False, 'proof': True, 'properties': 0})
                if fails:
                    measure('commerce_confirmed_source_loss_after_failed_write', result)
                game.execute("""
cities[1].identityFail=false;cities[1].kind='RESEARCH';com.SourceChanged(0,1)
assert(ownedGold(cities[2])==15 and com.TransactionCurrent(0,2))
""")


STANDARD_SPLIT_SOURCES = """
local fails=...
knowledge[5].learned.BUILDING_GRANARY=nil
knowledge[5].learned.BUILDING_MONUMENT={district='DISTRICT_CITY_CENTER',tier=1}
splitRoutes='0,5,0,2,10;0,3,0,2,11;0,2,0,1,12'
send(splitRoutes,3)
assert(stdValue(1)==12 and monument(cities[1])==14)
local create=P.CreateBuilding
function restoreStandardizationWrite()P.CreateBuilding=create end
if fails then P.CreateBuilding=function(q,id)
 if q.city==cities[1] and id=='BUILDING_SPC_STD_MONUMENT_12'then return end
 return create(q,id)
end end
"""


class Standardization(unittest.TestCase):
    def test_confirmed_route_loss_stays_excluded_during_subsequent_pending_loss(self):
        for fails in (False, True):
            with self.subTest(fails=fails):
                game = two_standardization_targets()
                game.execute(STANDARD_SPLIT_SOURCES, fails)
                result = scalars(game.execute("""
local fails=...
send('0,3,0,2,11;0,2,0,1,12',2)
assert(monument(cities[1])==(fails and 0 or 12))
restoreStandardizationWrite()
net.CheckEvidence(false);cities[3].kind='NONE';std.SourceChanged(0,3)
return {granary=stdValue(1),monument=monument(cities[1]),
 removed_source=std.records['0:1'].sources[5]==nil,
 strict=net.TransactionCurrent(0),properties=propertyWrites}
""", fails))
                self.assertEqual(result, {'granary': 0, 'monument': 0, 'removed_source': True,
                                          'strict': False, 'properties': 0})
                if fails:
                    measure('standardization_confirmed_route_loss_after_failed_write', result)

    def test_confirmed_ineligible_source_is_not_revived_by_an_unreadable_fact(self):
        for fails in (False, True):
            with self.subTest(fails=fails):
                game = two_standardization_targets()
                game.execute(STANDARD_SPLIT_SOURCES, fails)
                result = scalars(game.execute("""
local fails=...
cities[5].active=2;std.SourceChanged(0,5)
assert(monument(cities[1])==(fails and 0 or 12))
restoreStandardizationWrite()
cities[5].fail=true;std.SourceChanged(0,5)
local prior=std.records['0:1'].sources[5]
return {monument=monument(cities[1]),granary=stdValue(1),
 stale_target=prior and next(prior.targets)~=nil or false,properties=propertyWrites}
""", fails))
                self.assertEqual(result, {'monument': 12, 'granary': 12,
                                          'stale_target': False, 'properties': 0})
                if fails:
                    measure('standardization_confirmed_role_loss_after_failed_write', result)

    def test_pending_reduction_does_not_install_a_new_positive_witness(self):
        game = two_standardization_targets()
        result = scalars(game.execute("""
knowledge[3].learned.BUILDING_MONUMENT=nil
knowledge[5].learned.BUILDING_GRANARY=nil
knowledge[5].learned.BUILDING_MONUMENT={district='DISTRICT_CITY_CENTER',tier=1}
studies[5]=1
local routes='0,5,0,2,10;0,3,0,2,11;0,2,0,1,12'
send(routes,3)
assert(stdValue(1)==12 and monument(cities[1])==12)
local create=P.CreateBuilding
P.CreateBuilding=function(q,id)
 if q.city==cities[1] and id=='BUILDING_SPC_STD_MONUMENT_14'then return end
 return create(q,id)
end
studies[5]=2;std.SourceChanged(0,5);P.CreateBuilding=create
assert(monument(cities[1])==0 and std.records['0:1'].writeUnconfirmed)
net.CheckEvidence(false);cities[3].kind='NONE';std.SourceChanged(0,3)
local held=monument(cities[1])
assert(stdValue(1)==0 and not net.TransactionCurrent(0))
send(routes,3)
return {while_pending=held,after_proof=monument(cities[1]),granary=stdValue(1),properties=propertyWrites}
"""))
        self.assertEqual(result, {'while_pending': 0, 'after_proof': 14, 'granary': 0, 'properties': 0})
        measure('standardization_unapplied_positive_waits_for_proof', result)


class Culture(unittest.TestCase):
    def test_confirmed_recipient_link_loss_survives_failed_withdrawal(self):
        for fails in (False, True):
            with self.subTest(fails=fails):
                game = culture()
                get_index(game, 'cn')
                result = scalars(game.execute("""
local fails=...
local c=cities[1]
cities[3].kind='CULTURE';cities[3].potential=4;cities[3].active=4
complete(4,1);complete(4,2);complete(3,7)
send('0,4,0,2,10;0,3,0,2,13;0,2,0,1,11',3)
assert(amount(c)==3)
local remove=P.RemoveBuilding
if fails then P.RemoveBuilding=function(b,id)
 if b.city==c and id=='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0'then return end
 return remove(b,id)
end end
send('0,4,0,2,10;0,2,0,1,11',2)
assert(amount(c)==(fails and 3 or 2))
assert((idx.Dependents(0,3)[1]==true)==fails)
P.RemoveBuilding=remove
net.CheckEvidence(false);cities[4].active=3;cn.SourceChanged(0,4)
local r=cn.records['0:1']
assert(not idx.Dependents(0,3)[1])
return {culture=amount(c),removed_source=r.contributions[3]==nil,
 strict=net.TransactionCurrent(0),properties=propertyWrites}
""", fails))
                self.assertEqual(result, {'culture': 0, 'removed_source': True,
                                          'strict': False, 'properties': 0})
                if fails:
                    measure('culture_confirmed_link_loss_after_failed_write', result)
