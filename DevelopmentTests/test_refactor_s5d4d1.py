"""Typed transfer metadata transport only; no producer hook retirement yet."""
import unittest
from test_refactor_s5a import registry
from refactor_harness import measure

class TransferTransport(unittest.TestCase):
    def test_detached_triplet_survives_later_generic_evidence(self):
        c=registry();c.execute("local t={owner=1,city=900,oldOwner=0};d.RegisterConsumer('read',function(r)calls[#calls+1]=r end,{kinds={'D'}});d.Emit({owner=0,kinds={'D'},cause='TRANSFER',transfer=t,evidence={old=true}});t.city=777;d.Emit({owner=0,kinds={'D'},cause='LATER',evidence={latest=true}});d.Flush();assert(#calls==1 and calls[1].city==nil and calls[1].evidence.latest);local n=0;for _,v in pairs(calls[1].transfers)do n=n+1;assert(v.owner==1 and v.city==900 and v.oldOwner==0)end;assert(n==1)")
    def test_multiple_same_key_transfers_deduplicate_full_triplet(self):
        c=registry();c.execute("d.RegisterConsumer('read',function(r)calls[#calls+1]=r end,{kinds={'D'}});for _,t in ipairs({{owner=1,city=900,oldOwner=0},{owner=0,city=900,oldOwner=2},{owner=1,city=900,oldOwner=0}})do d.Emit({owner=0,kinds={'D'},cause='TRANSFER',transfer=t})end;assert(d.pending==1);d.Flush();local n=0;for _,v in pairs(calls[1].transfers)do n=n+1 end;assert(n==2)")
    def test_consumers_cannot_mutate_each_others_transfers(self):
        c=registry();c.execute("d.RegisterConsumer('bad',function(r)for k,v in pairs(r.transfers)do v.city=666;r.transfers[k]=nil end end,{kinds={'D'}});d.RegisterConsumer('read',function(r)for _,v in pairs(r.transfers)do assert(v.city==900);calls[#calls+1]=v end end,{kinds={'D'}});d.Emit({owner=0,kinds={'D'},cause='TRANSFER',transfer={owner=1,city=900,oldOwner=0}});d.Flush();assert(#calls==1)")
    def test_reentrant_transfer_waits_next_snapshot(self):
        c=registry();c.execute("d.RegisterConsumer('read',function(r)for _,v in pairs(r.transfers)do calls[#calls+1]=v.city end;if #calls==1 then d.Emit({owner=0,kinds={'D'},cause='TRANSFER',transfer={owner=1,city=901,oldOwner=0}});assert(not d.Flush())end end,{kinds={'D'}});d.Emit({owner=0,kinds={'D'},cause='TRANSFER',transfer={owner=1,city=900,oldOwner=0}});d.Flush();assert(#calls==1 and d.pending==1);d.Flush();assert(#calls==2 and calls[2]==901);local n=d.delivered;for i=1,1000 do d.Flush()end;assert(d.delivered==n)")
    def test_invalid_shape_native_metatable_and_functions_do_not_touch_queue(self):
        c=registry();c.execute("local native=setmetatable({},{__index=function()error('NATIVE_ACCESS_FORBIDDEN')end});for _,t in ipairs({native,{owner=1,city=900},{owner=1,city=900,oldOwner=0,extra=1},{owner=1,city=function()end,oldOwner=0},{owner=1,city=2147483648,oldOwner=0},{owner=1,city=-1,oldOwner=0}})do assert(not pcall(d.Emit,{owner=0,kinds={'D'},cause='INVALID',transfer=t}))end;assert(d.sequence==0 and d.pending==0 and d.Generation(0,'COMMERCE')==0)")
    def test_old_owner_never_receives_destination_city_alias(self):
        c=registry();c.execute("assert(not pcall(d.Emit,{owner=0,cityID=900,kinds={'D'},cause='BAD_ALIAS',transfer={owner=1,city=900,oldOwner=0}}));assert(not pcall(d.Emit,{owner=0,kinds={'D'},cause='BAD_OWNER',transfer={owner=1,city=900,oldOwner=2}}));assert(not pcall(d.Emit,{owner=1,cityID=901,kinds={'D'},cause='BAD_DESTINATION',transfer={owner=1,city=900,oldOwner=0}}));d.Emit({owner=1,cityID=900,kinds={'D'},cause='TRANSFER',transfer={owner=1,city=900,oldOwner=0}});assert(d.sequence==1 and d.pending==1)")
    def test_capacity_boundary_duplicate_and_overflow_are_atomic(self):
        c=registry();c.execute("for i=1,32 do d.Emit({owner=0,kinds={'D'},cause='TRANSFER',transfer={owner=1,city=900+i,oldOwner=0}})end;d.Emit({owner=0,kinds={'D'},cause='TRANSFER',transfer={owner=1,city=901,oldOwner=0}});local seq,gen=d.sequence,d.Generation(0,'COMMERCE');assert(not pcall(d.Emit,{owner=0,kinds={'D'},cause='OVERFLOW',transfer={owner=1,city=999,oldOwner=0}}));assert(d.sequence==seq and d.emitted==seq and d.Generation(0,'COMMERCE')==gen and d.pending==1);d.RegisterConsumer('read',function(r)local n=0;for _ in pairs(r.transfers)do n=n+1 end;assert(n==32 and not r.causes.OVERFLOW);calls[#calls+1]=n end,{kinds={'D'}});d.Flush();assert(#calls==1 and not d.errors.read)")
        measure('S5d4d1_transfer_boundary',{'per_row_limit':32,'overflow_state_changes':0,'idle_deliveries':0})
    def test_dense_existing_payload_and_full_transfer_set_fit_delivery_budget(self):
        c=registry();c.execute("local e,i={},{};for n=1,256 do e['E'..n]=n;i['I'..n]=n end;for n=1,32 do d.Emit({owner=0,kinds={'D'},cause='TRANSFER',transfer={owner=1,city=900+n,oldOwner=0},evidence=e,investment=i})end;d.RegisterConsumer('read',function(r)assert(r.evidence.E256==256 and r.investment.I256==256);local n=0;for _ in pairs(r.transfers)do n=n+1 end;assert(n==32);calls[#calls+1]=n end,{kinds={'D'}});d.Flush();assert(#calls==1 and not d.errors.read)")
    def test_optional_field_absent_keeps_old_generic_evidence_semantics(self):
        c=registry();c.execute("d.RegisterConsumer('read',function(r)assert(r.transfers==nil and r.evidence.last);calls[#calls+1]=r.city end,{kinds={'D'}});d.Emit({owner=0,cityID=7,kinds={'D'},cause='FIRST',evidence={first=true}});d.Emit({owner=0,cityID=7,kinds={'D'},cause='LATER',evidence={last=true}});d.Flush();assert(#calls==1 and calls[1]==7)")

if __name__=='__main__':unittest.main()
