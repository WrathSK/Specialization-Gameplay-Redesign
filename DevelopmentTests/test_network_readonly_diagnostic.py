"""Run the retained copy diagnostic through actual Gameplay and a real network view."""

import unittest

from refactor_harness import ROOT, measure
from retired_crew_sources import package
from test_network_effect_fact_receipts import composition
from test_o7_retired_great_work_adjacency_retirement import context
from test_o7_route_observer_retirement import exercise_proof

B479 = '6932e768644308849a761343c458bb4bc6c649b2'


def read_production_report(root, revision=None):
    game = context(root, revision)
    ui = context(root, revision, 'UI/BackgroundRoutes')
    packets = exercise_proof(game, ui)
    readings = game.execute("""
local shared=ExposedMembers.SPC_P0
local counts={refresh=0,verify=0,role=0}
local refresh,verify,read=net.Refresh,net.Verified,shared.EffectiveFacts.Read
net.Refresh=function(...)counts.refresh=counts.refresh+1;return refresh(...)end
net.Verified=function(...)counts.verify=counts.verify+1;return verify(...)end
shared.EffectiveFacts.Read=function(...)counts.role=counts.role+1;return read(...)end
local version=net.Input(0).inputVersion;local proof=net.ProofRevision(0)
local function request(action,token)
 GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=token,CityID=1,Page=1})
 assert(shared.LastToken==token and shared.RequestIngress.action==action and shared.RequestDepth==0)
 return shared.Snapshot
end
local standard=request('NETWORK_DETAIL','CURRENT')
assert(counts.refresh==0 and counts.verify==0 and counts.role==0)
local oldCopy=request('LV4_COPY_READ','COPY')
assert(oldCopy:find('旧工业区域生产力复制已退出',1,true))
local metadata=shared.Lv4CopyRead
assert(metadata.token=='COPY' and metadata.cityID==1 and metadata.kind=='CULTURE' and metadata.active==4)
assert(metadata.industryRecipient==false and #metadata.sources==0 and not metadata.error)
assert(request('NETWORK_DETAIL','AFTER')==standard)
assert(net.TransactionCurrent(0) and net.ProofRevision(0)==proof and net.Input(0).inputVersion==version)
return counts
""")
    return packets, dict(readings.items())


class NetworkDiagnostic(unittest.TestCase):
    def test_real_request_uses_the_publication_without_recapture(self):
        with package(B479) as old:
            before = read_production_report(old, B479)
        after = read_production_report(ROOT)
        self.assertEqual(before[0], after[0])
        self.assertEqual(before[1], {'refresh': 1, 'verify': 2, 'role': 3})
        self.assertEqual(after[1], {'refresh': 0, 'verify': 0, 'role': 1})
        measure('network_diagnostic_role_read', {'before': before[1], 'after': after[1]})

    def test_report_requires_current_proof_and_preserves_the_applied_template(self):
        lua = composition()
        lua.globals().include('Lv4CopyRead')
        lua.execute("""
local c=cities[1];local read=SPCLv4CopyRead.Metadata
local first=read(P,shared,0,c,'BEFORE')
assert(first.industryRecipient and #first.sources==1 and first.sources[1].cityID==5)
fire('TradeRouteActivityChanged',0);drain()
local proof,revision=net.ProofRevision(0),net.Input(0).inputVersion
local previous=created+removed
local original,checked=net.Refresh,net.Verified
net.Refresh=function()error('DIAGNOSTIC_REFRESHED')end
net.Verified=function()error('DIAGNOSTIC_VERIFIED')end
local waiting=read(P,shared,0,c,'PENDING')
assert(waiting.networkError:find('NETWORK_REFRESH_PENDING',1,true))
assert(waiting.industryRecipient==nil and #waiting.sources==0 and stdValue(1)==14)
assert(net.ProofRevision(0)==proof and net.Input(0).inputVersion==revision and created+removed==previous)
net.Refresh,net.Verified=original,checked
send(routes,3);drain()
local restored=read(P,shared,0,c,'RESTORED')
assert(restored.industryRecipient and restored.sources[1].cityID==5 and created+removed==previous)
""")

    def test_reference_replacement_is_reported_without_a_hidden_reconciliation(self):
        lua = composition()
        lua.globals().include('Lv4CopyRead')
        lua.execute("""
local c=cities[1];local read=SPCLv4CopyRead.Metadata
local proof=net.ProofRevision(0);local writes=created+removed
cities[5].token='NEW_REFERENCE'
local output=read(P,shared,0,c,'REPLACED')
assert(output.networkError:find('NETWORK_REFERENCE_CHANGED',1,true))
assert(#output.sources==0 and output.industryRecipient==nil)
assert(net.ProofRevision(0)==proof and created+removed==writes and stdValue(1)==14)
""")
