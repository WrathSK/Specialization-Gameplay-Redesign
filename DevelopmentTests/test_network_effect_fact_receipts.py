"""Real Bridge, Standardization and Culture network delivery under Lua 5.1."""
import unittest

from refactor_harness import measure
from test_refactor_s4b import standard


def composition():
    lua = standard()
    lua.execute("""
fc=shared.FactChanges;bindings=shared.FactBindings
local eligible=P.IsTestPlayer
P.IsTestPlayer=function(pid)
 local good=eligible(pid)
 return good,nil,good and 'ELIGIBLE' or 'INELIGIBLE'
end
-- This fixture has both passive network owners, no Commerce or investments.
local function outside(e)return fc.Receipt(e,'IRRELEVANT','FIXTURE_OUTSIDE_SCOPE')end
for _,name in ipairs({'Commerce','CapitalInvestment','DevelopmentInvestment','ResearchTraditionEffects'})do
 shared[name]={AcceptFact=outside}
end
for _,name in ipairs({'ResearchSupport','Lv2Housing','Lv2GPP','IndustrySupport','ResearchInfrastructure',
 'ResearchCross','ResearchApply','ResearchChair','CultureAesthetic','CultureMeaning','CultureInspiration',
 'CultureInsightsTourism','DialogueEffects'})do shared[name]={AcceptFact=function()return true end}end
function historyFact(id,topic)
 fc.Emit({owner=0,cityID=id,kinds={'HISTORY'},topic=topic,cause='HISTORY_COMMITTED'})
end
function drain()fc.Flush();bindings.Flush()end
routes='0,4,0,2,10;0,5,0,2,11;0,2,0,1,12'
send(routes,3);drain()
assert(net.TransactionCurrent(0) and stdValue(1)==14)
""")
    return lua


class NetworkEffectFactReceipts(unittest.TestCase):
    def test_standardization_refusal_holds_only_its_own_receipt_and_proof_is_not_rerequested(self):
        lua = composition()
        lua.execute("""
local stdAudits,cnAudits,proofRequests=0,0,0
local sa,ca,request=std.AcceptFact,cn.AcceptFact,net.RequestPendingProof
std.AcceptFact=function(scope)
 assert(scope.player==0 and scope.changed[5] and not scope.changed[4])
 stdAudits=stdAudits+1;return sa(scope)
end
cn.AcceptFact=function(scope)
 assert(scope.player==0 and scope.changed[4] and not scope.changed[5])
 cnAudits=cnAudits+1;return ca(scope)
end
net.RequestPendingProof=function(pid)proofRequests=proofRequests+1;return request(pid)end
std.busy=true;studies[5]=1;complete(4,1)
historyFact(5,'ENGINEERING');historyFact(4,'INSIGHTS')
fc.Flush();assert(stdValue(1)==14 and amount(cities[1])==0 and stdAudits==0 and cnAudits==0)
bindings.Flush()
assert(stdValue(1)==14 and amount(cities[1])==1)
assert(fc.errors.Binding_StandardizationEffects and not fc.errors.Binding_CultureNetwork and fc.retained==1)
assert(stdAudits==1 and cnAudits==1 and proofRequests==2)
std.busy=false
for i=1,100 do drain()end
assert(stdAudits==1 and stdValue(1)==14)
assert(bindings.Wake('StandardizationEffects','TARGET_READY',fc.sequence,{player=0,city=5}))
drain()
assert(stdValue(1)==12 and amount(cities[1])==1 and fc.retained==0)
assert(stdAudits==2 and cnAudits==1 and proofRequests==2)
""")
        measure('network_effect_receipts', {
            'standardization_recovery_audits': 1,
            'successful_culture_replays': 0, 'proof_requests_on_named_wake': 0,
        })

    def test_pending_topology_retains_both_effects_until_real_proof(self):
        lua = composition()
        lua.execute("""
studies[5]=0;historyFact(5,'ENGINEERING')
complete(4,1);historyFact(4,'INSIGHTS');drain()
assert(amount(cities[1])==1 and stdValue(1)==10)
net.CheckEvidence(false)
assert(not net.TransactionCurrent(0))
local previous=created+removed
complete(4,2);studies[5]=2
historyFact(4,'INSIGHTS');historyFact(5,'ENGINEERING');drain()
assert(amount(cities[1])==1 and stdValue(1)==10 and previous==created+removed)
assert(not fc.errors.Binding_CultureNetwork and not fc.errors.Binding_StandardizationEffects)
assert(not net.TransactionCurrent(0))
send(routes,3);drain()
assert(net.TransactionCurrent(0) and amount(cities[1])==2 and stdValue(1)==14)
assert(fc.retained==0)
""")

    def test_culture_scoped_native_read_failure_does_not_discard_its_receipt_or_touch_peer(self):
        lua = composition()
        lua.execute("""
local c=cities[1];local prior=c.GetDistricts
local visits=0
c.GetDistricts=function()visits=visits+1;error('CULTURE_READ_UNKNOWN')end
complete(4,1);historyFact(4,'INSIGHTS');drain()
assert(fc.errors.Binding_CultureNetwork and cn.errors['0:1'] and amount(c)==0)
local before=visits;for i=1,100 do drain()end;assert(visits==before)
c.GetDistricts=prior
factReads={};historyFact(4,'INSIGHTS');drain()
assert(amount(c)==1 and not fc.errors.Binding_CultureNetwork and not cn.errors['0:1'])
assert(not factReads[3] and fc.retained==0)
""")

    def test_same_bridge_proof_recovers_culture_only_after_a_native_read_failure(self):
        lua = composition()
        lua.execute("""
local c=cities[1];local get=c.GetDistricts
local sa,ca=std.AcceptFact,cn.AcceptFact
local stdAudits,cnAudits=0,0
std.AcceptFact=function(s)stdAudits=stdAudits+1;return sa(s)end
cn.AcceptFact=function(s)cnAudits=cnAudits+1;return ca(s)end
c.GetDistricts=function()error('DISTRICT_COLLECTION_UNAVAILABLE')end
complete(4,1);net.CheckEvidence(false);send(routes,3);drain()
assert(net.TransactionCurrent(0) and fc.retained==1 and fc.errors.Binding_CultureNetwork)
assert(not fc.errors.Binding_StandardizationEffects and amount(c)==0 and stdValue(1)==14)
local stdBefore,cnBefore=stdAudits,cnAudits;c.GetDistricts=get
for i=1,100 do drain()end
assert(cnAudits==cnBefore and amount(c)==0)
assert(bindings.Wake('CultureNetwork','TARGET_READY',fc.sequence,{player=0}));drain()
assert(cnAudits==cnBefore+1 and stdAudits==stdBefore and amount(c)==1 and fc.retained==0)
""")
