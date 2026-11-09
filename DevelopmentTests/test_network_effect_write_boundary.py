"""Actual network effect writers with controlled native write/readback failures."""
import unittest
from unittest.mock import patch

from refactor_harness import TrackedLua51, legacy_source_observation, measure
from test_pu11_package_absence import scalars
from test_refactor_s4b import culture, warm_commerce


COMMERCE_PARTIAL = """
local c=cities[2]
local create,remove=P.CreateBuilding,P.RemoveBuilding
local writes=commerceWrites
local added,removedBefore=created,removed
function restoreCommerceWriter()
 P.CreateBuilding=create;P.RemoveBuilding=remove
end
P.CreateBuilding=function(q,id)
 if q.city==c and id=='BUILDING_SPC_COMMERCE_GOLD_4'then return end
 return create(q,id)
end
cities[1].yields.SCIENCE=200;com.SourceChanged(0,1)
local v=view(2)
return {physical=ownedGold(c),shown=v.totalGold,unconfirmed=v.writeUnconfirmed==true,
 access=c.present.BUILDING_SPC_COMMERCIALIZATION_ACCESS==true,
 ready=com.TransactionCurrent(0,2),bridge_ready=net.TransactionCurrent(0),
 stage=v.stage,attempted_removals=removed-removedBefore,successful_creates=created-added,
 config_writes=commerceWrites-writes}
"""


class CommercializationReadback(unittest.TestCase):
    def test_partial_write_reports_installed_gold_and_waits_for_an_existing_audit(self):
        game = warm_commerce()
        result = scalars(game.execute(COMMERCE_PARTIAL))
        self.assertEqual(result, {
            'physical': 14, 'shown': 14, 'unconfirmed': True, 'access': True,
            'ready': False, 'bridge_ready': True, 'stage': 'HELD',
            'attempted_removals': 1, 'successful_creates': 0, 'config_writes': 0,
        })
        measure('commerce_failed_effect_readback', result)
        game.execute("""
local c=cities[2]
local writes=created+removed
assert(com.Describe(0,c):find('基础金币：14',1,true))
net.CheckEvidence(false)
assert(view(2).writeUnconfirmed and view(2).totalGold==14 and not com.TransactionCurrent(0,2))
for i=1,100 do fixturePublication()end
assert(created+removed==writes and ownedGold(c)==14)
restoreCommerceWriter()
send(routeRows,3)
assert(ownedGold(c)==30 and com.TransactionCurrent(0,2) and not view(2).writeUnconfirmed)
""")

    def test_unreadable_or_replaced_city_has_no_reported_zero_or_foreign_readback(self):
        for replaced in (False, True):
            with self.subTest(replaced=replaced):
                game = warm_commerce()
                game.execute("""
local replaced=...
local c=cities[2]
local create,read=P.CreateBuilding,P.HasBuilding
local failed,readsAfterFailure=false,0
P.CreateBuilding=function(q,id)
 if q.city==c and id=='BUILDING_SPC_COMMERCE_GOLD_4'then
  failed=true
  if replaced then c.token='REPLACED_REFERENCE' end
  error('COMMERCE_NATIVE_WRITE_INJECTED',0)
 end
 return create(q,id)
end
P.HasBuilding=function(b,id)
 if failed and b.city==c then readsAfterFailure=readsAfterFailure+1;return nil end
 return read(b,id)
end
local previous=removed
cities[1].yields.SCIENCE=200;com.SourceChanged(0,1)
local v=view(2)
assert(failed and ownedGold(c)==14 and removed-previous==1)
assert(v.stage=='HELD' and v.writeUnconfirmed and v.totalGold==nil and #v.effective==0)
assert(not com.TransactionCurrent(0,2) and com.Describe(0,c):find('基础金币：未知',1,true))
assert((readsAfterFailure==0)==replaced)
""", replaced)

    def test_failed_confirmed_reduction_preserves_the_actual_residual(self):
        game = warm_commerce()
        game.execute("""
local c=cities[2]
local remove=P.RemoveBuilding
P.RemoveBuilding=function(b,id)
 if b.city==c and id=='BUILDING_SPC_COMMERCE_GOLD_1'then return end
 return remove(b,id)
end
c.active=2;com.SourceChanged(0,2)
assert(view(2).stage=='HELD' and view(2).writeUnconfirmed and view(2).totalGold==14)
assert(ownedGold(c)==14 and not com.TransactionCurrent(0,2))
P.RemoveBuilding=remove
com.SourceChanged(0,2)
assert(ownedGold(c)==0 and not view(2).writeUnconfirmed)
""")

    def test_confirmed_zero_workers_withdraws_after_partial_write_during_proof_wait(self):
        game = warm_commerce()
        game.execute(COMMERCE_PARTIAL)
        game.execute("""
local c=cities[2]
restoreCommerceWriter()
net.CheckEvidence(false)
assert(view(2).writeUnconfirmed and ownedGold(c)==14)
c.workers=0
com.SourceChanged(0,2)
assert(ownedGold(c)==0 and view(2).totalGold==0 and not view(2).writeUnconfirmed)
assert(not net.TransactionCurrent(0) and not com.TransactionCurrent(0,2))
""")

    def test_failed_write_does_not_block_an_independent_receiver(self):
        game = warm_commerce()
        game.execute("""
cities[3].kind='COMMERCE';cities[3].potential=3;cities[3].active=3
cities[3].depths={DISTRICT_CAMPUS=2}
commerceStates[3]=SPCCommerceModel.Select(SPCCommerceModel.New(0),'DISTRICT_CAMPUS',true)
send('0,1,0,2,10;0,1,0,3,11',2)
com.SourceChanged(0,3)
assert(ownedGold(cities[2])==15 and ownedGold(cities[3])==10)
local create=P.CreateBuilding
P.CreateBuilding=function(q,id)
 if q.city.id==2 and id=='BUILDING_SPC_COMMERCE_GOLD_4'then return end
 return create(q,id)
end
cities[1].yields.SCIENCE=200;com.SourceChanged(0,1)
assert(ownedGold(cities[2])==14 and view(2).writeUnconfirmed and not com.TransactionCurrent(0,2))
assert(ownedGold(cities[3])==20 and com.TransactionCurrent(0,3))
""")

    def test_actual_sidebar_uses_residual_and_disables_configuration(self):
        game = warm_commerce()
        game.execute(COMMERCE_PARTIAL)
        import test_b261_commerce as dashboard
        with patch.object(dashboard, 'LuaRuntime', TrackedLua51), legacy_source_observation():
            ui = dashboard.ui()
        ui.execute("""
ContextPtr.input(2,27)
c.GetID=function()return 2 end;c.GetX=function()return 2 end;c.GetY=function()return 10 end
Players[0].GetCities=function()return {FindID=function(_,id)if id==2 then return c end end}end
""")
        ui.globals().commerceView = ui.table_from(scalars(game.eval('view(2)')), recursive=True)
        ui.execute("""
ExposedMembers.SPC_P0.Commerce.views['0:2']=commerceView
LuaEvents.SPC_CommerceOpen(0,2);rows.items[1].Root.click()
assert(Controls.Confirm.disabled and Controls.Status.text:find('WRITE_UNCONFIRMED',1,true))
assert(Controls.Status.text:find('14',1,true) and Controls.Summary.text:find('WAITING',1,true))
Controls.Confirm.click();assert(#sent==0)
""")


CULTURE_PARTIAL = """
local c=cities[1]
for i=1,3 do complete(4,i)end
cn.SourceChanged(0,4)
assert(amount(c)==3 and amount(cities[5])==3)
local create,remove=P.CreateBuilding,P.RemoveBuilding
local attemptedRemovals=0
function restoreCultureWriter()
 P.CreateBuilding=create;P.RemoveBuilding=remove
end
P.CreateBuilding=function(q,id)
 if q.city==c and id=='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_2'then
  if onCultureWriteFailure then onCultureWriteFailure(c)end
  return
 end
 return create(q,id)
end
P.RemoveBuilding=function(b,id)
 if b.city==c then attemptedRemovals=attemptedRemovals+1 end
 return remove(b,id)
end
for i=4,6 do complete(4,i)end
cn.SourceChanged(0,4)
local r=cn.records['0:1']
return {physical=amount(c),shown=r and r.writeUnconfirmed and r.writeUnconfirmed.n,
 last_confirmed=r and r.n,attempted_removals=attemptedRemovals,
 sibling=amount(cities[5]),error=cn.errors['0:1']~=nil,
 route_ready=net.TransactionCurrent(0),properties=propertyWrites}
"""


class CultureNetworkReadback(unittest.TestCase):
    def test_partial_write_reports_residual_and_keeps_independent_receiver(self):
        game = culture()
        result = scalars(game.execute(CULTURE_PARTIAL))
        self.assertEqual(result, {
            'physical': 2, 'shown': 2, 'last_confirmed': 3,
            'attempted_removals': 1, 'sibling': 6, 'error': True,
            'route_ready': True, 'properties': 0,
        })
        measure('culture_failed_effect_readback', result)
        game.execute("""
local c=cities[1]
local writes=created+removed
local text=cn.Describe(0,c)
assert(text:find('载体配置读回：2',1,true) and not text:find('完整文明 3',1,true))
net.CheckEvidence(false);cn.SourceChanged(0,4)
assert(created+removed==writes and cn.records['0:1'].writeUnconfirmed.n==2 and amount(c)==2)
for i=1,100 do fixturePublication()end
assert(created+removed==writes)
restoreCultureWriter()
send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3)
assert(amount(c)==6 and not cn.records['0:1'].writeUnconfirmed and not cn.errors['0:1'])
assert(cn.records['0:1'].contributions[4].provenance=='CONFIRMED')
""")

    def test_unreadable_or_replaced_receiver_reports_unknown(self):
        for replaced in (False, True):
            with self.subTest(replaced=replaced):
                game = culture()
                game.execute("""
local replace=...
local read=P.HasBuilding
failedCultureWriteReads=0
function onCultureWriteFailure(c)
 if replace then c.token='REPLACEMENT' end
 P.HasBuilding=function(b,id)
  if b.city==c then failedCultureWriteReads=failedCultureWriteReads+1;return nil end
  return read(b,id)
 end
end
""", replaced)
                result = scalars(game.execute(CULTURE_PARTIAL))
                self.assertNotIn('shown', result)
                self.assertEqual((result['physical'], result['sibling']), (2, 6))
                # The create attempt already has one confirmation read. Only a
                # still-matching receiver may take the additional residue read.
                self.assertEqual(game.eval('failedCultureWriteReads'), 1 if replaced else 2)
                game.execute("""
local c=cities[1]
local text=cn.Report(0,c,true)
assert(text:find('载体配置读回：未知',1,true) and not text:find('：提供完整文明',1,true))
""")

    def test_cold_interrupted_reconciliation_keeps_observation_separate_from_saved_aggregate(self):
        game = culture(False)
        game.execute("""
local c=cities[1]
for bit=0,1 do
 local id='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_'..bit
 c.present[id]=true;c.locations[id]=100
end
fire('LoadScreenClose')
assert(amount(c)==3 and cn.records['0:1'].loaded and created==0 and removed==0)
for i=1,6 do complete(4,i)end
local create=P.CreateBuilding
P.CreateBuilding=function(q,id)
 if q.city==c and id=='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_2'then return end
 return create(q,id)
end
local routes='0,4,0,2,10;0,2,0,1,11;0,2,0,5,12'
send(routes,3)
local r=cn.records['0:1']
assert(amount(c)==2 and r.n==3 and r.loaded and r.writeUnconfirmed.n==2)
assert(next(r.contributions)==nil and amount(cities[5])==6 and propertyWrites==0)
net.CheckEvidence(false);cn.Audit({player=0,city=1})
assert(amount(c)==2 and cn.records['0:1'].writeUnconfirmed.n==2 and propertyWrites==0)
P.CreateBuilding=create
send(routes,3)
assert(amount(c)==6 and not cn.records['0:1'].loaded and not cn.records['0:1'].writeUnconfirmed)
assert(not cn.errors['0:1'] and propertyWrites==0)
""")

    def test_confirmed_receiver_loss_withdraws_during_proof_wait(self):
        game = culture()
        game.execute(CULTURE_PARTIAL)
        game.execute("""
local c=cities[1]
restoreCultureWriter();net.CheckEvidence(false)
c.incomplete=true
cn.Audit({player=0,city=1})
assert(amount(c)==0 and cn.records['0:1'].n==0 and not cn.records['0:1'].writeUnconfirmed)
assert(not cn.errors['0:1'] and amount(cities[5])==6 and not net.TransactionCurrent(0))
""")

    def test_confirmed_source_loss_can_reduce_a_readable_residual(self):
        game = culture()
        game.execute("""
local c=cities[1]
cities[3].kind='CULTURE';cities[3].potential=4;cities[3].active=4
complete(4,1);complete(4,2);complete(3,7)
send('0,4,0,2,10;0,3,0,2,13;0,2,0,1,11',3)
assert(amount(c)==3)
local create=P.CreateBuilding
P.CreateBuilding=function(q,id)
 if q.city==c and id=='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_2'then return end
 return create(q,id)
end
for i=3,5 do complete(4,i)end
cn.SourceChanged(0,4)
assert(amount(c)==2 and cn.records['0:1'].writeUnconfirmed.n==2)
P.CreateBuilding=create
net.CheckEvidence(false)
cities[4].active=3
cn.SourceChanged(0,4)
local r=cn.records['0:1']
assert(amount(c)==1 and r.n==1 and not r.writeUnconfirmed and r.contributions[4]==nil)
assert(r.contributions[3] and not net.TransactionCurrent(0))
""")
