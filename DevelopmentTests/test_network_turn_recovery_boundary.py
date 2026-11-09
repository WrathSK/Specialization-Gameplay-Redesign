"""Compare the retained Bridge turn entry with just that invocation suppressed."""

import unittest

from refactor_harness import measure
from test_network_effect_fact_receipts import composition
from test_refactor_s4b import warm_commerce
from test_refactor_s5c2 import fixture as bridge_commerce


def activation(lua, suppress):
    lua.execute("""
local suppress=...
local refresh=net.Refresh
local calls=0
net.Refresh=function(pid,...)
 assert(pid==0)
 calls=calls+1
 if not suppress then return refresh(pid,...)end
end
turn=turn+1;Events.PlayerTurnActivated.Fire(0)
net.Refresh=refresh
assert(calls==1)
""", suppress)


class NetworkTurnRecovery(unittest.TestCase):
    def test_recovered_role_without_a_new_packet_still_needs_its_turn_entry(self):
        outcomes = {}
        for suppress in (False, True):
            lua = composition(ready=False)
            lua.execute("""
cities[4].fail=true;complete(4,1)
send(routes,3);drain()
assert(not net.TransactionCurrent(0) and net.CurrentCultureBatch(0).rolesPending[1])
assert(amount(cities[1])==0)
accepted=net.players[0].acceptedSeq;proof=net.ProofRevision(0)
cities[4].fail=false
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();drain()end
assert(net.ProofRevision(0)==proof and amount(cities[1])==0)
""")
            activation(lua, suppress)
            result = lua.execute("""
drain();Events.GameCoreEventPublishComplete.Fire();drain()
assert(net.players[0].acceptedSeq==accepted)
return {trade_ready=net.TransactionCurrent(0),culture=amount(cities[1]),proof_changed=net.ProofRevision(0)>proof}
""")
            outcomes['turn_suppressed' if suppress else 'current'] = dict(result.items())
        self.assertEqual(outcomes, {
            'current': {'trade_ready': True, 'culture': 1, 'proof_changed': True},
            'turn_suppressed': {'trade_ready': False, 'culture': 0, 'proof_changed': False},
        })
        measure('bridge_turn_readiness_boundary', outcomes)

    def test_confirmed_loss_whose_projection_failed_still_needs_a_new_retry_owner(self):
        outcomes = {}
        for suppress in (False, True):
            lua = bridge_commerce()
            lua.execute("""
assert(toggle(2,'DISTRICT_CAMPUS',true))
assert(ownedGold(cities[2])==15)
local signature=SPCNetworkInput.Signature
local attempts=0
SPCNetworkInput.Signature=function(input)
 if input.negativeProof then attempts=attempts+1;error('INJECTED_NEGATIVE_PROJECTION')end
 return signature(input)
end
units[11]=nil
net.CheckEvidence(false,'TradeRouteRemovedFromMap')
assert(net.players[0].negativeHeld and not net.TransactionCurrent(0) and attempts>0)
SPCNetworkInput.Signature=signature
local capturesBefore=captures
for i=1,100 do Events.GameCoreEventPublishComplete.Fire()end
assert(captures==capturesBefore and net.players[0].negativeHeld and ownedGold(cities[2])==15)
""")
            activation(lua, suppress)
            result = lua.execute("""
shared.FactChanges.Flush();shared.FactBindings.Flush();Events.GameCoreEventPublishComplete.Fire()
local held=net.players[0].negativeHeld==true
return {negative_held=held,trade_ready=net.TransactionCurrent(0),gold=ownedGold(cities[2])}
""")
            outcomes['turn_suppressed' if suppress else 'current'] = dict(result.items())
        self.assertEqual(outcomes, {
            'current': {'negative_held': False, 'trade_ready': False, 'gold': 6},
            'turn_suppressed': {'negative_held': True, 'trade_ready': False, 'gold': 15},
        })
        measure('bridge_turn_negative_boundary', outcomes)


def compare_turn(lua, *, bridge=True, owner=None, owner_turn=True):
    lua.execute("""
local name,keepOwner=...
local owner=name and shared[name]
local mark=owner and owner.Mark
local calls=0
if owner then
 owner.Mark=function(pid,cid,...)
  if cid==nil then calls=calls+1;if not keepOwner then return end end
  return mark(pid,cid,...)
 end
end
function restoreTurnMark()
 if owner then owner.Mark=mark;assert(calls==1)end
end
""", owner, owner_turn)
    activation(lua, not bridge)
    lua.execute("restoreTurnMark();restoreTurnMark=nil")


class AuditedTurnDuties(unittest.TestCase):
    def test_failed_phase_zero_role_delivery_is_not_an_idle_retry(self):
        outcomes = {}
        for bridge in (True, False):
            lua = composition()
            lua.execute("""
complete(4,1);historyFact(4,'INSIGHTS');drain()
assert(net.TransactionCurrent(0) and stdValue(1)==14 and amount(cities[1])==1)
local refreshFacts=net.RefreshFacts
net.RefreshFacts=function()error('INJECTED_PHASE0_FAILURE',0)end
fc.Emit({owner=0,cityID=5,kinds={'ACTIVE'},cause='ACTIVE_CHANGED'});drain()
net.RefreshFacts=refreshFacts
assert(not net.TransactionCurrent(0) and fc.errors.NetworkBridge=='INJECTED_PHASE0_FAILURE')
proof=net.ProofRevision(0)
local reads=counts.city_scan
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();drain()end
assert(counts.city_scan==reads and not net.TransactionCurrent(0) and net.ProofRevision(0)==proof)
""")
            compare_turn(lua, bridge=bridge)
            result = lua.execute("""
drain()
assert(amount(cities[1])==1 and stdValue(1)==14)
return {ready=net.TransactionCurrent(0),proof_advanced=net.ProofRevision(0)>proof}
""")
            outcomes['current' if bridge else 'turn_suppressed'] = dict(result.items())
        self.assertEqual(outcomes, {
            'current': {'ready': True, 'proof_advanced': True},
            'turn_suppressed': {'ready': False, 'proof_advanced': False},
        })
        measure('phase_zero_failed_role_refresh_turn_dependency', outcomes)

    def test_failed_commerce_audit_keeps_its_turn_recovery_duty(self):
        outcomes = {}
        for owner_turn in (True, False):
            lua = warm_commerce()
            lua.execute("""
local proofRevision=net.ProofRevision
net.ProofRevision=function()error('INJECTED_COMMERCE_AUDIT_FAILURE')end
cities[2].workers=0
assert(shared.NativeFacts.Workers({player=0,city=2},'NATIVE_WORKER_CHANGED'))
fixturePublication();net.ProofRevision=proofRevision
assert(com.error and ownedGold(cities[2])==15)
for i=1,100 do fixturePublication()end;assert(ownedGold(cities[2])==15)
""")
            compare_turn(lua, owner='Commerce', owner_turn=owner_turn)
            result = lua.execute("""
fixturePublication()
return {gold=ownedGold(cities[2]),workers=view(2).workers,held=com.error~=nil}
""")
            outcomes['current' if owner_turn else 'turn_suppressed'] = dict(result.items())
        self.assertEqual(outcomes, {
            'current': {'gold': 0, 'workers': 0, 'held': False},
            'turn_suppressed': {'gold': 15, 'workers': 2, 'held': True},
        })
        measure('commerce_failed_audit_turn_dependency', outcomes)

    def test_silently_readable_culture_history_keeps_its_turn_recovery_duty(self):
        outcomes = {}
        for owner_turn in (True, False):
            lua = composition()
            lua.execute("""
complete(4,1);historyFact(4,'INSIGHTS');drain();assert(amount(cities[1])==1)
cities[4].historyUnknown=true;complete(4,2);historyFact(4,'INSIGHTS');drain()
assert(amount(cities[1])==1 and cn.records['0:1'].provenance[4].status=='RETAINED')
cities[4].historyUnknown=false
local reads=historyReads[4]
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();drain()end
assert(historyReads[4]==reads and amount(cities[1])==1)
""")
            compare_turn(lua, owner='CultureNetwork', owner_turn=owner_turn)
            result = lua.execute("""
drain();Events.GameCoreEventPublishComplete.Fire();drain()
return {culture=amount(cities[1]),provenance=cn.records['0:1'].provenance[4].status}
""")
            outcomes['current' if owner_turn else 'turn_suppressed'] = dict(result.items())
        self.assertEqual(outcomes, {
            'current': {'culture': 2, 'provenance': 'CONFIRMED'},
            'turn_suppressed': {'culture': 1, 'provenance': 'RETAINED'},
        })
        measure('culture_silent_history_turn_dependency', outcomes)

    def test_failed_registration_needs_at_least_one_of_the_two_turn_entries(self):
        outcomes = {}
        for bridge in (True, False):
            for culture in (True, False):
                lua = composition()
                lua.execute("""
complete(4,1);historyFact(4,'INSIGHTS');drain()
send('0,5,0,2,11;0,2,0,1,12',2);drain();assert(amount(cities[1])==0)
local emit=fc.EmitDerived
fc.EmitDerived=function()error('INJECTED_NOTIFICATION_CAPACITY')end
send(routes,3);drain();fc.EmitDerived=emit
assert(net.TransactionCurrent(0) and net.players[0].notificationIntent and amount(cities[1])==0)
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();drain()end
assert(amount(cities[1])==0)
""")
                compare_turn(lua, bridge=bridge, owner='CultureNetwork', owner_turn=culture)
                result = lua.execute("""
drain();Events.GameCoreEventPublishComplete.Fire();drain()
assert(net.TransactionCurrent(0))
return {culture=amount(cities[1]),intent_pending=net.players[0].notificationIntent~=nil}
""")
                outcomes[f'bridge_{bridge}_culture_{culture}'] = dict(result.items())
        self.assertEqual(outcomes, {
            'bridge_True_culture_True': {'culture': 1, 'intent_pending': False},
            'bridge_True_culture_False': {'culture': 1, 'intent_pending': False},
            'bridge_False_culture_True': {'culture': 1, 'intent_pending': True},
            'bridge_False_culture_False': {'culture': 0, 'intent_pending': True},
        })
        measure('failed_proof_registration_overlapping_turn_duties', outcomes)


class DeliveredRoleRefresh(unittest.TestCase):
    def test_next_role_change_completes_failed_refresh_in_the_same_turn(self):
        lua = composition()
        result = lua.execute("""
complete(4,1);historyFact(4,'INSIGHTS');drain()
local before=net.players[0].acceptedSeq
local startTurn=turn
local refresh=net.RefreshFacts
local attempts=0
local capture=SPCNetworkInput.Capture
local captures=0
SPCNetworkInput.Capture=function(...)captures=captures+1;return capture(...)end
net.RefreshFacts=function()attempts=attempts+1;error('INJECTED_PHASE0_FAILURE',0)end
cities[5].active=3
fc.Emit({owner=0,cityID=5,kinds={'ACTIVE'},cause='ACTIVE_CHANGED'});drain()
assert(attempts==1 and not net.TransactionCurrent(0))
assert(fc.errors.NetworkBridge=='INJECTED_PHASE0_FAILURE')
local input=net.Input(0)
assert(input.pendingRoleGeneration==fc.Generation(0,'NETWORK') and input.roleRefreshError=='NETWORK_ROLE_REFRESH_FAILED')
-- The confirmed local ACTIVE loss still clamps the old Industrial amount.
assert(stdValue(1)==10 and amount(cities[1])==1)
local proof=net.ProofRevision(0)
assert(net.ReadSnapshot(0,cities[1],false):find('NETWORK_ROLE_REFRESH_FAILED',1,true))
historyFact(4,'INSIGHTS');drain()
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();drain()end
assert(attempts==1 and net.ProofRevision(0)==proof and captures==0)
net.RefreshFacts=refresh
cities[5].active=2
fc.Emit({owner=0,cityID=5,kinds={'ACTIVE'},cause='ACTIVE_CHANGED'});drain()
assert(captures==1 and turn==startTurn and net.players[0].acceptedSeq==before and net.TransactionCurrent(0))
assert(net.ProofRevision(0)>proof and not fc.errors.NetworkBridge)
assert(not net.Input(0).pendingRoleGeneration and not net.Input(0).roleRefreshError)
assert(stdValue(1)==0 and amount(cities[1])==1 and propertyWrites==0)
return {idle_attempts=attempts-1,idle_publishes=100,captures_on_next_role_change=captures,
 same_turn=true,accepted_sequence_unchanged=true}
""")
        measure('role_refresh_recovers_on_delivered_fact', dict(result.items()))

    def test_existing_packet_finishes_duplicate_role_generation_after_capture_failure(self):
        lua = composition()
        lua.execute("""
local original=SPCNetworkInput.Capture
local captures=0
SPCNetworkInput.Capture=function(...)captures=captures+1;error('NETWORK_TEST_CAPTURE_FAILURE',0)end
local b=net.players[0];local inputVersion,seq=b.inputRevision,b.acceptedSeq
fc.Emit({owner=0,cityID=5,kinds={'ACTIVE'},cause='ACTIVE_CHANGED'});drain()
assert(captures==1 and b.inputRevision==inputVersion and not net.TransactionCurrent(0))
assert(net.Input(0).pendingRoleGeneration==fc.Generation(0,'NETWORK'))
assert(net.ReadSnapshot(0,cities[1],false):find('NETWORK_TEST_CAPTURE_FAILURE',1,true))
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();drain()end
assert(captures==1)
SPCNetworkInput.Capture=original
send(routes,3);drain()
assert(b.acceptedSeq>seq and b.inputRevision==inputVersion and net.TransactionCurrent(0))
assert(not net.Input(0).pendingRoleGeneration and not net.Input(0).roleRefreshError)
assert(stdValue(1)==14 and propertyWrites==0)
""")

    def test_reentrant_newer_generation_cannot_be_cleared_by_older_capture(self):
        lua = composition()
        lua.execute("""
local original=SPCNetworkInput.Capture
local captures=0
SPCNetworkInput.Capture=function(...)
 captures=captures+1
 local value=original(...)
 if captures==1 then
  cities[5].active=2
  fc.Emit({owner=0,cityID=5,kinds={'ACTIVE'},cause='ACTIVE_CHANGED'})
 end
 return value
end
cities[5].active=3
fc.Emit({owner=0,cityID=5,kinds={'ACTIVE'},cause='ACTIVE_CHANGED'});drain()
local b=net.players[0]
assert(captures==1 and b.factGeneration<fc.Generation(0,'NETWORK') and not net.TransactionCurrent(0))
assert(net.Input(0).pendingRoleGeneration==b.factGeneration)
drain()
assert(captures==2 and b.factGeneration==fc.Generation(0,'NETWORK') and net.TransactionCurrent(0))
assert(not net.Input(0).pendingRoleGeneration and stdValue(1)==0)
""")
