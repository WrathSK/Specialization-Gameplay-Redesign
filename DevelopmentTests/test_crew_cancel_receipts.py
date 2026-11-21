"""Cancellation reconciles independent city orders with real Crew and Store code."""
import unittest

from test_pu05a_receipts import pair


class CancellationProof(unittest.TestCase):
    def setUp(self):
        self.lua = pair()
        self.lua.execute("""
        function removeOrder(target)
         target:GetBuildQueue().items[p]=nil
         Events.CityProductionChanged.Fire(0,target:GetID())
         Events.GameCoreEventPublishComplete.Fire()
        end
        function ordersOf(target) return target:GetProperty(SPCCrewModel.ORDER_PROPERTY).orders end
        function assertReleased()
         assert(#ordersOf(other)==0 and not crew.views['0:'..other:GetID()].held)
         assert(not C.reserve(other).error)
        end
        """)

    def test_proven_other_city_completion_releases_only_cancelled_order(self):
        self.lua.execute("""
        C.complete(c,p)
        local proof=T.encode(C.props[SPCCrewModel.RECEIPT_PROPERTY])
        removeOrder(other);assertReleased()
        assert(C.count(c)==1 and C.count(other)==0 and C.calls==1)
        assert(T.encode(C.props[SPCCrewModel.RECEIPT_PROPERTY])==proof)
        Events.CityProjectCompleted.Fire(0,other:GetID(),C.rows.Projects[p].Index)
        assert(C.calls==1)
        """)

    def test_rebooking_before_the_queue_notification_uses_the_same_proof(self):
        self.lua.execute("""
        C.complete(c,p);other:GetBuildQueue().items[p]=nil
        local reply=C.reserve(other)
        assert(not reply.error and reply.reservation==2 and #ordersOf(other)==1)
        assert(C.calls==1 and C.count(other)==0)
        """)

    def test_existing_held_order_releases_on_new_proof(self):
        self.lua.execute("""
        c:GetBuildQueue().items[p]=nil;C.stats[p]=1
        removeOrder(other);assert(ordersOf(other)[1].stage=='HELD' and C.calls==0)
        Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index)
        Events.GameCoreEventPublishComplete.Fire()
        assertReleased();assert(C.calls==1 and C.count(c)==1)
        """)

    def test_same_type_different_serial_in_same_city(self):
        self.lua.execute("""
        C.begin(other);C.complete(other,p);removeOrder(other)
        assertReleased();assert(C.calls==1 and C.count(other)==1 and #ordersOf(c)==1)
        """)

    def test_several_accounted_completions_release_after_units_are_consumed(self):
        self.lua.execute("""
        C.begin(c);C.complete(c,p);C.complete(c,p)
        Players[0]:GetUnits():Destroy(C.units[20001]);Players[0]:GetUnits():Destroy(C.units[20002])
        removeOrder(other);assertReleased();assert(C.calls==2)
        """)

    def test_single_receipt_survives_cold_load_and_loss_of_unit(self):
        self.lua.execute("""
        C.complete(c,p);Players[0]:GetUnits():Destroy(C.units[20001])
        C.reload(c);removeOrder(other);assertReleased();assert(C.calls==1)
        """)

    def test_cold_multiple_ordinals_use_existing_first_unit_binding(self):
        self.lua.execute("""
        C.begin(c);C.complete(c,p);C.complete(c,p);C.reload(c)
        removeOrder(other);assertReleased();assert(C.calls==2 and C.count(c)==2)
        """)

    def test_cold_watermark_alone_cannot_reconstruct_a_missing_prefix(self):
        self.lua.execute("""
        C.begin(c);C.complete(c,p);C.complete(c,p)
        Players[0]:GetUnits():Destroy(C.units[20001]);Players[0]:GetUnits():Destroy(C.units[20002])
        C.reload(c);removeOrder(other)
        assert(ordersOf(other)[1].stage=='HELD' and C.reserve(other).error and C.calls==2)
        """)

    def test_a_gap_before_the_first_consumed_ordinal_does_not_clear(self):
        self.lua.execute("""
        removeOrder(c);C.stats[p]=1
        C.begin(c);C.complete(c,p)
        assert(C.props[SPCCrewModel.RECEIPT_PROPERTY].water[p]==2)
        removeOrder(other);assert(ordersOf(other)[1].stage=='HELD' and C.reserve(other).error)
        C.reload(c);assert(ordersOf(other)[1].stage=='HELD' and C.calls==1)
        """)

    def test_missing_ordinal_stays_held_with_or_without_foreign_type_receipt(self):
        self.lua.execute("""
        local second=C.begin(c,2);C.complete(c,second)
        C.stats[p]=1;removeOrder(other)
        assert(ordersOf(other)[1].stage=='HELD' and C.reserve(other).error and C.calls==1)
        """)

    def test_paid_progress_and_queued_order_keep_their_admission(self):
        self.lua.execute("""
        C.complete(c,p);assert(ordersOf(other)[1].stage=='QUEUED')
        other:GetBuildQueue().progressByProject[p]=9;removeOrder(other)
        assert(ordersOf(other)[1].stage=='PAUSED' and C.calls==1)
        """)

    def test_unresolved_own_grant_is_never_released_or_replayed(self):
        self.lua.execute("""
        C.grantFailure='before';C.complete(other,p);C.grantFailure=nil;C.complete(c,p)
        removeOrder(other);C.reload(c)
        assert(ordersOf(other)[1].stage=='CALLING' and C.props[SPCCrewModel.RECEIPT_PROPERTY].pending[Bkey()])
        assert(C.reserve(other).error and C.calls==2)
        """)

    def test_missing_or_regressed_native_count_keeps_the_order(self):
        for value in ('nil', '0'):
            with self.subTest(counter=value):
                lua=pair()
                lua.execute("""
                C.complete(c,p);local order=C.begin(c)
                local read=ExposedMembers.SPC_CrewNativeRead
                ExposedMembers.SPC_CrewNativeRead=function(pid,id)
                 local q=read(pid,id);if id==c:GetID() then q.completed[order]=COUNTER end;return q
                end
                local before=T.encode(c:GetProperty(SPCCrewModel.ORDER_PROPERTY))
                c:GetBuildQueue().items[order]=nil;crew.Refresh(0,c:GetID())
                assert(crew.errors['0:'..c:GetID()]=='CREW_NATIVE_COMPLETION_COUNTER_UNKNOWN')
                assert(T.encode(c:GetProperty(SPCCrewModel.ORDER_PROPERTY))==before and C.calls==1)
                """.replace('=COUNTER ', '=' + value + ' '))


if __name__ == '__main__':
    unittest.main()
