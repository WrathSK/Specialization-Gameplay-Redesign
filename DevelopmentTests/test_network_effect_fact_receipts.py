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


class UnreadableRouteRoles(unittest.TestCase):
    def test_unknown_source_role_holds_only_reachable_receivers(self):
        lua = composition(ready=False)
        lua.execute("""
local id='BUILDING_SPC_STD_14'
cities[2].present[id]=true
cities[3].fail=true
complete(4,1)
units[13]={}
send('0,4,0,1,10;0,5,0,2,11;0,3,0,2,12;0,2,0,5,13',4);drain()
local culture,industry=net.CurrentCultureBatch(0),net.CurrentIndustryBatch(0)
assert(amount(cities[1])==1 and not cn.records['0:1'].loaded)
assert(stdValue(5)==0 and not net.TransactionCurrent(0))
assert(stdValue(2)==14 and std.records['0:2'].loaded and std.records['0:2'].retained)
assert(culture.rolesPending[2] and culture.rolesPending[5] and not culture.rolesPending[1])
assert(industry.rolesPending[2] and industry.rolesPending[5] and not industry.rolesPending[1])
cities[3].fail=false
net.Refresh(0);drain()
assert(net.TransactionCurrent(0) and not net.CurrentIndustryBatch(0).rolesPending)
assert(stdValue(2)==14 and stdValue(5)==14 and not std.records['0:2'].loaded)
""")

    def test_unknown_hub_does_not_make_its_recipient_a_forwarder(self):
        lua = composition(ready=False)
        lua.execute("""
local c=cities[2];local id='BUILDING_SPC_CULTURE_NETWORK_COMMERCE_0'
c.present[id]=true;c.locations[id]=200
complete(4,1)
cities[3].kind='COMMERCE';cities[3].potential=nil;cities[3].active=0
send('0,4,0,3,10;0,3,0,2,11;0,2,0,5,12',3);drain()
local v=net.CurrentCultureBatch(0)
assert(amount(c)==1 and cn.records['0:2'].loaded and amount(cities[5])==0)
assert(v.rolesPending[3] and v.rolesPending[2] and not v.rolesPending[5])
assert(not net.CurrentIndustryBatch(0).rolesPending[2])
local scoped=net.CurrentCultureBatch(0,{sources={},targets={[2]=true}})
assert(scoped.scoped and scoped.rolesPending[2] and not scoped.rolesPending[3])
cities[3].potential=1
net.Refresh(0);drain()
assert(not net.CurrentCultureBatch(0).rolesPending and net.TransactionCurrent(0))
assert(amount(c)==1 and not cn.records['0:2'].loaded and amount(cities[5])==0)
""")

    def test_known_empty_role_recovers_on_same_derived_membership(self):
        lua = composition(ready=False)
        lua.execute("""
local c=cities[3]
c.kind='CULTURE';c.potential=nil;c.active=0
send('0,3,0,2,10;0,2,0,1,11',2);drain()
assert(cn.records['0:1'].loaded and net.CurrentCultureBatch(0).rolesPending[1])
local revision=net.Input(0).inputVersion
local reads=counts.city_scan
for i=1,100 do drain()end
assert(counts.city_scan==reads)
c.potential=0
net.Refresh(0);drain()
assert(not net.CurrentCultureBatch(0).rolesPending and net.Input(0).inputVersion==revision+1)
assert(not cn.records['0:1'].loaded and not cn.errors['0:1'] and net.TransactionCurrent(0))
""")

    def test_unreadable_capital_source_role_only_holds_its_family(self):
        lua = composition(ready=False)
        lua.execute("""
local capital,c=cities[1],cities[2]
local id='BUILDING_SPC_CULTURE_NETWORK_COMMERCE_0'
c.present[id]=true;c.locations[id]=200
capital.kind='CULTURE';capital.potential=nil;capital.active=0
send('0,1,0,2,10',1);drain()
assert(amount(c)==1 and cn.records['0:2'].loaded)
local roles=net.CurrentCultureBatch(0).rolesPending
assert(roles[1] and roles[2] and not net.CurrentIndustryBatch(0).rolesPending[2])
capital.potential=4;capital.active=4;complete(1,1)
net.Refresh(0);drain()
assert(not net.CurrentCultureBatch(0).rolesPending and net.TransactionCurrent(0))
assert(amount(c)==1 and amount(capital)==1 and not cn.records['0:2'].loaded)
""")

    def test_unreadable_off_route_city_does_not_block_passive_projection(self):
        lua = composition(ready=False)
        lua.execute("""
cities[3].fail=true;complete(4,1)
send(routes,3);drain()
assert(not net.CurrentCultureBatch(0).rolesPending and not net.CurrentIndustryBatch(0).rolesPending)
assert(amount(cities[1])==1 and stdValue(1)==14 and not net.TransactionCurrent(0))
""")


class PendingProofFanout(unittest.TestCase):
    def test_warm_route_status_skips_only_passive_recomputation(self):
        lua = composition()
        result = lua.execute("""
complete(4,1);historyFact(4,'INSIGHTS');drain()
assert(amount(cities[1])==1 and stdValue(1)==14 and net.TransactionCurrent(0))
local audits={CultureNetwork=0,StandardizationEffects=0}
for name in pairs(audits)do
 local effect=shared[name];local accept=effect.AcceptFact
 effect.AcceptFact=function(scope)audits[name]=audits[name]+1;return accept(scope)end
end
local notices={}
for _,name in ipairs({'Commerce','CapitalInvestment','DevelopmentInvestment'})do
 local owner=shared[name];local accept=owner.AcceptFact
 owner.AcceptFact=function(e)notices[name]=e.cause;return accept(e)end
end
local requests=0
ExposedMembers.SPC_P0_BackgroundRoutes={RequestRevalidation=function(epoch,pid)
 assert(epoch==net.epoch and pid==0 and not net.TransactionCurrent(pid));requests=requests+1
end}
local before=created+removed;local version=net.Input(0).inputVersion
local revision=net.ProofRevision(0);local c=cities[1]
Locale={Lookup=function(s)return s end}
fire('TradeRouteActivityChanged',0);drain()
assert(net.ProofRevision(0)>revision and net.Input(0).inputVersion==version)
assert(not net.TransactionCurrent(0) and not pcall(net.CurrentCapitalSources,0,c,'CULTURE'))
assert(net.CurrentOutgoingDomestic(0,c).validity=='UNKNOWN')
assert(audits.CultureNetwork==0 and audits.StandardizationEffects==0 and fc.retained==0)
assert(requests==1 and amount(c)==1 and stdValue(1)==14 and created+removed==before)
for _,name in ipairs({'Commerce','CapitalInvestment','DevelopmentInvestment'})do
 assert(notices[name]=='NETWORK_PROOF_PENDING')
end
assert(cn.Describe(0,c):find('CN_NETWORK_PENDING',1,true))
assert(std.Describe(0,c):find('STD_NETWORK_PENDING',1,true))
for i=1,100 do drain()end
assert(audits.CultureNetwork==0 and audits.StandardizationEffects==0 and requests==1)
send(routes,3);drain()
assert(net.TransactionCurrent(0) and net.Input(0).inputVersion==version)
assert(audits.CultureNetwork==1 and audits.StandardizationEffects==1)
assert(amount(c)==1 and stdValue(1)==14 and created+removed==before and fc.retained==0)
assert(not cn.Describe(0,c):find('CN_NETWORK_PENDING',1,true))
assert(not std.Describe(0,c):find('STD_NETWORK_PENDING',1,true))
return {pending_owner_audits=0, ui_proof_requests=requests, same_value_owner_audits=2, carrier_writes=created+removed-before}
""")
        measure('warm_pending_proof_fanout', dict(result.items()))

    def test_confirmed_route_loss_merged_with_pending_is_delivered(self):
        lua = composition()
        lua.execute("""
complete(4,1);historyFact(4,'INSIGHTS');drain()
assert(amount(cities[1])==1 and stdValue(1)==14)
local causes
fc.RegisterConsumer('PendingLossWitness',function(e)causes=e.causes end,{kinds={'NETWORK'}})
units[10]=nil;units[11]=nil
fire('TradeRouteRemovedFromMap',0);drain()
assert(causes.NETWORK_PROOF_PENDING and causes.NETWORK_PROOF_PUBLISHED)
assert(not net.TransactionCurrent(0) and net.Input(0).continuityOnly)
assert(amount(cities[1])==0 and stdValue(1)==0 and fc.retained==0)
""")

    def test_local_fact_changes_still_withdraw_while_proof_is_pending(self):
        lua = composition()
        lua.execute('''
complete(4,1);historyFact(4,'INSIGHTS');drain()
assert(amount(cities[1])==1 and amount(cities[2])==1 and stdValue(1)==14)
fire('TradeRouteActivityChanged',0);drain()
cities[1].pillaged=true
fc.Emit({owner=0,cityID=1,kinds={'D'},cause='DISTRICT_FACTS_DIRTY'})
cities[5].active=2
fc.Emit({owner=0,cityID=5,kinds={'ACTIVE'},cause='ACTIVE_CHANGED'})
drain()
assert(not net.TransactionCurrent(0) and net.Input(0).continuityOnly)
assert(amount(cities[1])==0 and amount(cities[2])==1 and stdValue(1)==0 and fc.retained==0)
''')

    def test_pending_never_acknowledges_a_held_effect_delivery(self):
        lua = composition()
        lua.execute("""
local newRoutes=routes..';0,1,0,3,13';units[13]={}
std.busy=true;send(newRoutes,4);drain()
assert(net.TransactionCurrent(0) and fc.errors.Binding_StandardizationEffects and fc.retained==1)
fire('TradeRouteActivityChanged',0);drain()
assert(not net.TransactionCurrent(0) and fc.errors.Binding_StandardizationEffects and fc.retained==1)
std.busy=false;send(newRoutes,4);drain()
assert(net.TransactionCurrent(0) and not fc.errors.Binding_StandardizationEffects and fc.retained==0)
""")

    def test_pending_does_not_supersede_unregistered_proof_with_status_only(self):
        lua = composition()
        lua.execute("""
local newRoutes=routes..';0,1,0,3,13';units[13]={}
local emit=fc.EmitDerived
fc.EmitDerived=function()error('INJECTED_NOTIFICATION_CAPACITY')end
send(newRoutes,4);drain()
assert(net.TransactionCurrent(0) and net.players[0].notificationIntent)
fc.EmitDerived=emit
local cause
fc.RegisterConsumer('PendingIntentWitness',function(e)cause=e.cause end,{kinds={'NETWORK'}})
fire('TradeRouteActivityChanged',0);drain()
assert(cause=='NETWORK_PROOF_PUBLISHED' and not net.players[0].notificationIntent)
assert(not net.TransactionCurrent(0) and fc.retained==0)
send(newRoutes,4);drain()
assert(net.TransactionCurrent(0) and fc.retained==0)
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
fire('TradeRouteActivityChanged',0)
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
