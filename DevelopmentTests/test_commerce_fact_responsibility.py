"""O2 actual ordinary-commerce delivery, retaining the PU03 proof path."""
import unittest

from test_pu03_delivery import pipeline


class OrdinaryCommerceDelivery(unittest.TestCase):
    def test_missing_owner_retains_ordinary_scope_until_explicit_recovery(self):
        lua = pipeline()
        lua.execute("""
local good=0;fc.RegisterConsumer('Good',function()good=good+1 end,{kinds={'WORKERS'}})
shared.Commerce=nil
fc.Emit({owner=0,cityID=2,kinds={'WORKERS'},cause='NATIVE_WORKER_CHANGED'})
drain()
assert(fc.retained==1 and good==1 and bindings.errors.Commerce,'ORDINARY_SCOPE_DROPPED')
local n=fc.delivered
for i=1,100 do drain()end
assert(fc.retained==1 and fc.delivered==n)
shared.Commerce=com
assert(wakeOwner(fc.sequence,{player=0,city=2}));drain()
assert(fc.retained==0 and good==1 and not bindings.errors.Commerce)
""")

    def test_combined_proof_and_role_have_one_owner_takeover(self):
        lua = pipeline()
        lua.execute("""
local accept,mark=com.AcceptFact,com.Mark;local calls,marks=0,0
com.Mark=function(...)marks=marks+1;return mark(...)end
com.AcceptFact=function(e)
 assert(e.kinds.NETWORK and e.kinds.WORKERS and e.player==0)
 calls=calls+1;return accept(e)
end
fc.Emit({owner=0,kinds={'WORKERS'},cause='NATIVE_WORKER_CHANGED'})
fc.Emit({owner=0,kinds={'NETWORK'},cause='NETWORK_VERIFIED'})
drain()
assert(calls==1 and marks==1 and fc.retained==0 and com.TransactionCurrent(0,2),'DUPLICATE_OWNER_MARK')
""")

    def test_owner_keeps_failed_ordinary_work_until_related_cause(self):
        lua = pipeline()
        lua.execute("""
local real=com.Audit;local attempts={}
com.Audit=function(s)
 attempts[#attempts+1]=s
 if #attempts==1 then return false end
 return real(s)
end
fc.Emit({owner=0,cityID=2,kinds={'WORKERS'},cause='NATIVE_WORKER_CHANGED'})
drain();assert(#attempts==1 and attempts[1].changed[2] and fc.retained==0)
for i=1,100 do drain()end
assert(#attempts==1)
fc.Emit({owner=0,cityID=4,kinds={'WORKERS'},cause='NATIVE_WORKER_CHANGED'})
drain()
assert(#attempts==2 and attempts[2].changed[2] and attempts[2].changed[4],'OWNER_LOST_FAILED_ORDINARY_SCOPE')
""")

    def test_existing_all_owner_and_topic_filters_stay_scoped(self):
        lua = pipeline()
        lua.execute("""
local real=com.Audit;local scope,n=nil,0
com.Audit=function(s)scope=s;n=n+1;return real(s)end
fc.Emit({owner=0,kinds={'HISTORY'},topic='ENGINEERING',cause='ENGINEERING_HISTORY'})
drain();assert(n==0)
fc.Emit({kinds={'D'},cause='DISTRICT_FACTS_DIRTY'})
drain();assert(n==1 and scope.player==0 and scope.changed==nil and fc.retained==0)
""")
