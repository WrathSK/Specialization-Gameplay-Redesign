"""Independent scope/receipt limits and delivery isolation in the Lua51 registry."""
import unittest

from refactor_harness import measure
from test_pu01_fact_use import fixture
from test_pu03_delivery import registry


class DeliveryCapacity(unittest.TestCase):
    def test_actual_depth_producer_preserves_full_scope_capacity_with_ten_receivers(self):
        lua = fixture()
        lua.execute("""
local fc=shared.FactChanges
fc.Flush()
local called=0
-- Model the effect recipients absent from the real D/Commerce fixture.
for _,name in ipairs({'ResearchInfrastructure','ResearchSupport','Lv2Housing','Lv2GPP','ResearchApply','ResearchChair',
 'CultureAesthetic','CultureMeaning','CultureInspiration'})do
 shared[name]={AcceptFact=function()called=called+1;return true end}
end
local writes=effectWrites
for id=1001,3047 do dc.MarkDirty(0,id) end
assert(fc.retainedScopes==2047 and fc.retained==20470)
dc.MarkDirty(0,3048)
assert(fc.retainedScopes==2048 and fc.pending==2048 and fc.retained==20480)
local sequence=fc.sequence
local ok,err=pcall(dc.MarkDirty,0,3049)
assert(not ok and tostring(err):find('FACT_QUEUE_LIMIT') and fc.sequence==sequence)
assert(fc.retainedScopes==2048 and fc.retained==20480)
local delivered=fc.delivered
fc.Flush();shared.FactBindings.Flush()
assert(fc.delivered-delivered>=20480 and called==18432 and effectWrites==writes)
assert(fc.retainedScopes==0 and fc.retained==0 and fc.pending==0)
dc.MarkDirty(0,3049);fc.Flush();shared.FactBindings.Flush()
assert(called==18441 and fc.retainedScopes==0 and fc.retained==0)
""")
        measure('delivery_depth_fanout', {
            'receivers_interested_in_D': 10, 'scopes_admitted': 2048,
            'receipts_before_drain': 20480, 'additional_receiver_callbacks': 18432,
            'carrier_writes_during_receipt_drain': 0,
        })

    def test_receipt_cap_with_both_phases_held(self):
        lua = registry()
        lua.execute("""
local active,nextBatch,history=0,0,0
local function consume(e)
 if e.causes.PROOF and not e.causes.NEXT_BATCH then active=active+1 end
 if e.causes.NEXT_BATCH and not e.causes.PROOF then nextBatch=nextBatch+1 end
 if e.causes.HISTORY_READY then history=history+1 end
 return false
end
fc.RegisterConsumer('NetworkBridge',function(e)
 fc.Emit({owner=e.player,cityID=e.city,kinds={'NETWORK'},cause='NEXT_BATCH'})
 fc.EmitDerived({owner=e.player,cityID=e.city,kinds={'NETWORK'},cause='PROOF'})
end,{kinds={'ACTIVE'},phase=0})
for _,name in ipairs({'First','Second'}) do
 fc.RegisterConsumer(name,consume,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
end
fc.RegisterConsumer('Third',consume,{kinds={'NETWORK','HISTORY'},delivery='RESPONSIBILITY'})
for id=1,2048 do emit(id,'ACTIVE') end
fc.Flush()
assert(active==6144 and nextBatch==0 and fc.retainedScopes==2048 and fc.retained==12288)
fc.Flush()
assert(active==6144 and nextBatch==6144 and fc.pending==0 and fc.retained==12288)
local sequence=fc.sequence
local function historyChange(id)
 return fc.Emit({owner=0,cityID=id,kinds={'HISTORY'},cause='HISTORY_READY'})
end
local ok,err=pcall(historyChange,2049)
assert(not ok and tostring(err):find('FACT_DELIVERY_RECEIVER_LIMIT'))
assert(fc.retainedScopes==2048 and fc.retained==12288 and fc.sequence==sequence and fc.pending==0)
historyChange(1) -- Only Third replaces its two earlier receipts with one.
assert(fc.retainedScopes==2048 and fc.retained==12287 and fc.pending==1)
ok,err=pcall(historyChange,2049)
assert(not ok and tostring(err):find('FACT_DELIVERY_SCOPE_LIMIT'))
fc.Flush()
assert(active==6144 and nextBatch==6144 and history==1 and fc.retained==12287)
assert(not fc.Flush())
fc.Close()
assert(fc.retainedScopes==0 and fc.retained==0 and fc.retryReady==0)
""")
        measure('delivery_two_phase_capacity', {
            'declared_receivers': 3, 'live_batches_per_receiver_scope': 2,
            'scopes': 2048, 'receipts_at_limit': 12288, 'excess_receipts_refused': 1,
        })

    def test_late_registration_checks_all_queued_scopes_before_taking_any(self):
        lua = registry()
        lua.execute("""
local ready,calls=false,0
fc.RegisterConsumer('First',function(e)if ready then return receipt(e)end end,
 {kinds={'NETWORK'},delivery='RESPONSIBILITY'})
for id=1,2048 do emit(id)end
fc.Flush()
emit(1);emit(2049,'HISTORY')
local function declare()
 fc.RegisterConsumer('Late',function(e)calls=calls+1;return receipt(e)end,
  {kinds={'NETWORK','HISTORY'},delivery='RESPONSIBILITY'})
end
local ok,err=pcall(declare)
assert(not ok and tostring(err):find('FACT_DELIVERY_SCOPE_LIMIT'))
assert(fc.retainedScopes==2048 and fc.retained==2048 and fc.pending==2)
ready=true;fc.Flush()
assert(calls==0 and fc.retainedScopes==2047)
emit(2);emit(2049,'HISTORY');declare()
assert(fc.retainedScopes==2048 and fc.retained==2049)
fc.Flush()
assert(calls==2 and fc.retainedScopes==2046 and fc.retained==2046)
""")

    def test_receipts_isolate_callback_edits_and_held_history_from_successful_siblings(self):
        lua = registry()
        lua.execute("""
local good,held,other=0,0,0
local function first(e)
 if e.city==2 then other=other+1;return receipt(e)end
 if e.kinds.NETWORK and e.evidence.value==7 then good=good+1;e.evidence.value=0 end
 if e.kinds.ACTIVE and not e.kinds.NETWORK and not e.evidence then good=good+1 end
 return receipt(e)
end
local function slow(e)
 if e.city==2 then return receipt(e)end
 if e.kinds.NETWORK and e.evidence.value==7 then held=held+1 end
 if e.kinds.ACTIVE and e.kinds.NETWORK and e.evidence.value==7 then return receipt(e)end
end
local options={kinds={'NETWORK','ACTIVE'},delivery='RESPONSIBILITY'}
fc.RegisterConsumer('Good',first,options);fc.RegisterConsumer('Slow',slow,options)
fc.Emit({owner=0,cityID=1,reference='LIVE',kinds={'NETWORK'},cause='OLD_PROOF',evidence={value=7}})
emit(2);fc.Flush()
assert(good==1 and held==1 and other==1 and fc.retainedScopes==1 and fc.retained==1)
assert(not fc.Flush())
emit(1,'ACTIVE',2,'LIVE');fc.Flush()
assert(good==2 and held==2 and other==1 and fc.retainedScopes==0 and fc.retained==0)
""")
