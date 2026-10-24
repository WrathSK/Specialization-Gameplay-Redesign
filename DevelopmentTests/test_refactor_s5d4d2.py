"""Actual native D→FC transfer producer; detached existing NewTargets recovery."""
import unittest
from test_refactor_s5c1 import depth
from refactor_harness import Context,measure

def targets():
    c=Context();c.load('RuntimeWork');c.execute("""
    P={IsTestPlayer=function(p)return p==0 end,Field=function(t,k)return t[k]end,Count=function()end}
    origin={owner=0,id=7,x=10,y=20};destination={owner=1,id=99,x=10,y=20}
    for _,city in ipairs({origin,destination})do city.GetOwner=function()return city.owner end;city.GetID=function()return city.id end;city.GetX=function()return city.x end;city.GetY=function()return city.y end end
    oldCities={[7]=origin};newCities={[99]=destination};available=false;visited={};errors={}
    Players={[0]={GetCities=function()return {FindID=function(_,id)return oldCities[id]end,Members=function()return pairs(oldCities)end}end},[1]={GetCities=function()if not available then error('NATIVE_DESTINATION_UNAVAILABLE')end;return {FindID=function(_,id)return newCities[id]end,Members=function()return pairs(newCities)end}end}}
    t=SPCRuntimeWork.NewTargets(P,shared,function(pid,city)visited[#visited+1]={owner=pid,city=city.id};if city.bad then error('DERIVED_CARRIER_UNAVAILABLE')end end,function(pid,id,err)errors[tostring(pid)..':'..tostring(id)]=err end)
    origin.bad=true;t.Run({player=0,city=7});oldCities[7]=nil;visited={}
    """);return c

class TransferProducer(unittest.TestCase):
    def test_foreign_destination_preserves_supported_old_owner_without_city_alias(self):
        c=depth();c.execute("d.RegisterConsumer('read',function(r)seen[#seen+1]=r end);resetCounts();Events.CityTransfered.Fire(1,900,0);assert(not counts.dc_capture and fc.pending==1);fc.Flush();assert(#seen==1 and seen[1].player==0 and seen[1].city==nil and seen[1].causes.NATIVE_CITY_TRANSFERRED);local n=0;for _,v in pairs(seen[1].transfers)do n=n+1;assert(v.owner==1 and v.city==900 and v.oldOwner==0)end;assert(n==1)")
        measure('S5d4d2_native_transfer_mark',{'native_city_reads':0,'supported_old_owner_city_aliases':0,'triplets_preserved':1})
    def test_same_key_transfer_metadata_survives_later_normal_D(self):
        c=depth();c.execute("d.RegisterConsumer('read',function(r)seen[#seen+1]=r end);Events.CityTransfered.Fire(1,900,0);Events.CityTransfered.Fire(2,901,0);d.MarkDirty(0);fc.Flush();assert(#seen==1);local n=0;for _,v in pairs(seen[1].transfers)do n=n+1 end;assert(n==2 and seen[1].causes.DISTRICT_FACTS_DIRTY)")
    def test_both_sides_and_one_failed_side_remains_isolated(self):
        c=depth();c.execute("P.IsTestPlayer=function(p)return p==0 or p==1 end;d.RegisterConsumer('read',function(r)seen[#seen+1]=r end);local emit=fc.Emit;fc.Emit=function(e)if e.owner==1 then error('NEW_OWNER_QUEUE_FAILURE')end;return emit(e)end;Events.CityTransfered.Fire(1,900,0);fc.Flush();assert(#seen==1 and seen[1].player==0 and seen[1].city==nil and d.transferError);fc.Emit=emit;seen={};Events.CityTransfered.Fire(1,900,0);fc.Flush();assert(#seen==2);for _,r in ipairs(seen)do if r.player==1 then assert(r.city==900)else assert(r.player==0 and r.city==nil)end end")
    def test_unknown_signature_remains_generic_scope_without_fabricated_metadata(self):
        c=depth();c.execute("d.RegisterConsumer('read',function(r)seen[#seen+1]=r end);Events.CityTransfered.Fire(-1,900,0);fc.Flush();assert(#seen==1 and seen[1].player==nil and seen[1].city==nil and seen[1].transfers==nil)")
    def test_foreign_only_transfer_keeps_existing_zero_work_gate(self):
        c=depth();c.execute("resetCounts();Events.CityTransfered.Fire(2,900,1);assert(fc.pending==0 and not counts.dc_capture)")

class PendingTransfer(unittest.TestCase):
    def test_pending_transfer_detaches_caller_and_recovers_original_destination(self):
        c=targets();c.execute("local v={owner=1,city=99,oldOwner=0};t.Retry({transfer=v});v.owner=4;v.city=666;v.oldOwner=5;local n=0;for _,r in pairs(t.transfers)do n=n+1;assert(r.owner==1 and r.city==99 and r.oldOwner==0)end;assert(n==1);oldCities[7]=nil;available=true;t.Retry({player=1,city=99});assert(#visited==1 and visited[1].owner==1 and visited[1].city==99 and next(t.transfers)==nil and t.pending['0:7']==nil)")
    def test_same_destination_different_former_owners_do_not_overwrite(self):
        c=targets();c.execute("t.Retry({transfer={owner=1,city=99,oldOwner=0}});t.Retry({transfer={owner=1,city=99,oldOwner=2}});t.Retry({transfer={owner=1,city=99,oldOwner=0}});local n=0;for _ in pairs(t.transfers)do n=n+1 end;assert(n==2)")
    def test_unrelated_recovery_scope_cannot_consume_waiting_transfer(self):
        c=targets();c.execute("t.Retry({transfer={owner=1,city=99,oldOwner=0}});available=true;oldCities[7]=nil;t.Retry({player=0,city=7});assert(next(t.transfers)and #visited==0);t.Retry({player=1,city=99});assert(next(t.transfers)==nil and #visited==1)")
    def test_reused_destination_reference_does_not_follow_wrong_city(self):
        c=targets();c.execute("t.Retry({transfer={owner=1,city=99,oldOwner=0}});oldCities[7]=nil;destination.x=30;available=true;t.Retry({player=1,city=99});assert(#visited==0 and t.pending['0:7']and not t.pending['1:99'])")
    def test_invalid_transfer_is_rejected_before_pending_mutation_or_native_read(self):
        c=targets();c.execute("local reads=0;local native=setmetatable({},{__index=function()reads=reads+1;error('NATIVE_READ')end});for _,v in ipairs({native,{owner=1,city=99},{owner=1,city=99,oldOwner=0,extra=1},{owner=1,city=2147483648,oldOwner=0}})do t.Retry({transfer=v});assert(next(t.transfers)==nil and t.error)end;assert(reads==0 and #visited==0)")
    def test_newtargets_bound_rejects_extra_triplet_without_overwriting_old_entries(self):
        c=targets();c.execute("for i=1,2048 do t.Retry({transfer={owner=1,city=i,oldOwner=0}})end;local n=0;for _ in pairs(t.transfers)do n=n+1 end;assert(n==2048);t.Retry({transfer={owner=1,city=9999,oldOwner=0}});n=0;for _ in pairs(t.transfers)do n=n+1 end;assert(n==2048 and t.error and not t.transfers['1:9999:0'])")

if __name__=='__main__':unittest.main()
