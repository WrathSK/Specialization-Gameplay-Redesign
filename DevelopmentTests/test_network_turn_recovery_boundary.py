"""Compare the retained Bridge turn entry with just that invocation suppressed."""

import unittest

from refactor_harness import measure
from test_network_effect_fact_receipts import composition
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
