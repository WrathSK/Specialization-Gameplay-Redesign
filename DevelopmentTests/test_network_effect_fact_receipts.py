"""Real Bridge, Standardization and Culture network delivery under Lua 5.1."""
import unittest

from refactor_harness import measure
from test_refactor_s4b import standard


def composition(ready=True):
    lua = standard(ready=ready)
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
""")
    if ready:
        lua.execute("send(routes,3);drain();assert(net.TransactionCurrent(0) and stdValue(1)==14)")
    return lua


class CultureColdRestoration(unittest.TestCase):
    def test_existing_history_notice_reconciles_once_after_all_sources_are_readable(self):
        lua = composition(ready=False)
        lua.execute("""
cities[3].kind='CULTURE';cities[3].potential=4;cities[3].active=4
complete(3,1);complete(4,2);cities[4].historyUnknown=true
local c=cities[1];local id='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_1'
c.present[id]=true;c.locations[id]=100
local rawCreate,rawRemove=P.CreateBuilding,P.RemoveBuilding
local writes=0
P.CreateBuilding=function(q,id)if id:find('CULTURE_NETWORK',1,true) then writes=writes+1 end;return rawCreate(q,id)end
P.RemoveBuilding=function(b,id)if id:find('CULTURE_NETWORK',1,true) then writes=writes+1 end;return rawRemove(b,id)end
send('0,3,0,2,10;0,4,0,2,11;0,2,0,1,12',3);drain()
assert(net.TransactionCurrent(0) and amount(c)==2 and amount(cities[2])==0 and writes==0)
assert(cn.records['0:1'].loaded and next(cn.records['0:1'].contributions)==nil)
local n=historyReads[4]
for i=1,100 do drain()end
assert(historyReads[4]==n and writes==0)
cities[4].historyUnknown=false
historyFact(4,'INSIGHTS');drain()
assert(amount(c)==2 and amount(cities[2])==2 and writes==1)
assert(not cn.records['0:1'].loaded and not cn.errors['0:1'])
assert(cn.records['0:1'].provenance[3].status=='CONFIRMED' and cn.records['0:1'].provenance[4].status=='CONFIRMED')
complete(4,3);historyFact(4,'INSIGHTS');drain()
assert(amount(c)==3 and amount(cities[2])==3 and writes==3 and propertyWrites==0)
""")

    def test_confirmed_route_loss_fences_proof_before_the_cold_aggregate_can_reconcile(self):
        lua = composition(ready=False)
        lua.execute("""
cities[3].kind='CULTURE';cities[3].potential=4;cities[3].active=4
complete(3,1);complete(4,2);cities[4].historyUnknown=true
local c=cities[1];local id='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_1'
c.present[id]=true;c.locations[id]=100
send('0,3,0,2,10;0,4,0,2,11;0,2,0,1,12',3);drain()
assert(amount(c)==2 and cn.records['0:1'].loaded and net.TransactionCurrent(0))
units[10]=nil
net.CheckEvidence(false);drain()
assert(not net.TransactionCurrent(0) and net.Input(0).continuityOnly and amount(c)==2)
cities[4].historyUnknown=false
historyFact(4,'INSIGHTS');drain()
assert(not net.TransactionCurrent(0) and amount(c)==2 and cn.records['0:1'].loaded)
send('0,4,0,2,11;0,2,0,1,12',2);drain()
assert(net.TransactionCurrent(0) and amount(c)==1 and not cn.records['0:1'].loaded)
assert(not cn.records['0:1'].contributions[3] and propertyWrites==0)
""")

    def test_confirmed_receiver_exit_precedes_incomplete_source_history(self):
        lua = composition(ready=False)
        lua.execute("""
local c=cities[1];local id='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0'
c.present[id]=true;c.locations[id]=100
cities[4].historyUnknown=true
fire('LoadScreenClose');assert(amount(c)==1)
c.pillaged=true
cn.Audit({player=0,city=1})
assert(amount(c)==0 and not cn.records['0:1'].loaded and propertyWrites==0)
""")


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
