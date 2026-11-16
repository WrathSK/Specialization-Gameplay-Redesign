"""Actual D owner, FactChanges and strict Commerce read during backpressure."""
import unittest

from test_pu01_fact_use import fixture


class DepthDelivery(unittest.TestCase):
    def test_city_change_blocks_transaction_when_delivery_reservation_fails(self):
        lua = fixture()
        lua.execute("""
fc=shared.FactChanges;fc.Flush()
local allow=false
fc.RegisterConsumer('OtherDuty',function(e)
 if allow then return fc.Receipt(e,'REGISTERED')end
end,{kinds={'HISTORY'},topics={'UNRELATED'},delivery='RESPONSIBILITY'})
for id=1001,3048 do fc.Emit({owner=0,cityID=id,kinds={'HISTORY'},topic='UNRELATED',cause='OTHER'})end
fc.Flush();assert(fc.retained==2048 and fc.pending==0 and com.TransactionCurrent(0,c.id))
local proof=fc.Generation(0,'NETWORK');local seq=fc.sequence;local writes=effectWrites
setBuildings(d,{'BUILDING_LIBRARY'})
local ok,err=pcall(dc.MarkDirty,0,c.id)
assert(not ok and tostring(err):find('FACT_DELIVERY_SCOPE_LIMIT')and fc.sequence==seq)
assert(not com.TransactionCurrent(0,c.id),'TRANSACTION_USED_STALE_D_AFTER_DROPPED_DELIVERY')
assert(effectWrites==writes and gold()==15 and fc.Generation(0,'NETWORK')==proof)
allow=true;assert(fc.WakeConsumer('OtherDuty','READY',fc.sequence));fc.Flush()
assert(fc.retained==0)
dc.MarkDirty(0,c.id);audit();assert(com.TransactionCurrent(0,c.id)and gold()==5)
""")

    def test_unlocated_change_also_blocks_strict_use_at_publication_queue_cap(self):
        lua = fixture()
        lua.execute("""
local fc=shared.FactChanges;fc.Flush()
for id=1001,3048 do fc.Emit({owner=0,cityID=id,kinds={'HISTORY'},topic='UNRELATED',cause='OTHER'})end
assert(com.TransactionCurrent(0,c.id)and fc.pending==2048)
local proof=fc.Generation(0,'NETWORK')
local ok,err=pcall(dc.MarkDirty)
assert(not ok and tostring(err):find('FACT_QUEUE_LIMIT'))
assert(not com.TransactionCurrent(0,c.id)and fc.Generation(0,'NETWORK')==proof,
 'UNLOCATED_CHANGE_LEFT_STALE_TRANSACTION_CURRENT')
""")

    def test_city_stamp_capacity_uses_existing_owner_fence_without_eviction(self):
        lua = fixture()
        lua.execute("""
local fc=shared.FactChanges;fc.Flush()
for id=1001,3048 do fc.InvalidateCommitted(0,id,{'D'})end
local a=fc.Generation(0,'COMMERCE',1001);local owner=fc.Generation(0,'COMMERCE')
assert(com.TransactionCurrent(0,c.id))
fc.InvalidateCommitted(0,9999,{'D'})
assert(fc.Generation(0,'COMMERCE')>owner and fc.Generation(0,'COMMERCE',1001)==a)
assert(not com.TransactionCurrent(0,c.id)and fc.pending==0)
assert(not pcall(fc.InvalidateCommitted,nil,9999,{'D'}))
""")
