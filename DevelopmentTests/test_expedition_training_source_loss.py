"""Source-loss orderings through the real city Store, Gate, Training and save cell; native inputs are simulated."""
import unittest
from unittest.mock import patch

from lupa.lua51 import LuaRuntime
import test_store_write_boundaries as cities


SETUP = """
T.start()
home,other=T.fresh(1),T.fresh(2)
for i,c in ipairs({home,other}) do
 T.register(c)
 T.complete(c,'DISTRICT_THEATER')
 for j=1,3 do T.invest(c,1000*i+j) end
 c.GetName=function(self)return 'Culture '..self:GetID() end
 c.buildings={}; c.trainingCount=0
 c.GetBuildings=function(self)return self.buildings end
 c.GetBuildQueue=function(self)
  return {city=self,GetSize=function()return self.trainingCount end,
   GetAt=function(_,i)assert(i==0);return {Directive=1,UnitType=90} end}
 end
end
T.governor(4)
assert(T.control(home).active==4 and T.control(other).active==4)
local oldSet=Game.SetProperty
local savedKey='SPC_EXPEDITION_TEAM_P0'
teamWrites=0
Game.SetProperty=function(self,k,v)
 if k==savedKey then teamWrites=teamWrites+1;T.propsSet(k,v);return end
 return oldSet(self,k,v)
end
local oldInfo=P.Info
local unitRow={Index=90,UnitType='UNIT_SPC_EXPEDITION_SPY'}
local markerRow={Index=777,InternalOnly=1,BuildingType='BUILDING_SPC_EXPEDITION_TRAINING_ACCESS'}
P.Info=function(t,k)
 if t=='Buildings' and (k==markerRow.BuildingType or k==markerRow.Index) then return markerRow end
 if t=='Units' and (k==unitRow.Index or k==unitRow.UnitType) then return unitRow end
 return oldInfo(t,k)
end
P.HasBuilding=function(b,id)return b[id]==true end
P.RemoveBuilding=function(b,id) b[id]=nil end
P.CreateBuilding=function(q,id) q.city.buildings[id]=true end
PlayerConfigurations={[0]={GetCivilizationTypeName=function()return 'CIVILIZATION_SPC_AMERICA' end}}
GameInfo.CivilizationCitizenNames=function()
 local once=true
 return function()if once then once=false;return {CivilizationType='CIVILIZATION_SPC_AMERICA',CitizenName='LOC_TEST_NAME'} end end
end
local ordinarySpy={Index=91,UnitType='UNIT_SPY'}
CityProductionDirectives={TRAIN=1}
GameInfo.Units={[90]=unitRow,[91]=ordinarySpy}
offMap,offReads=0,0
Players[0].GetDiplomacy=function()
 return {GetNumSpiesOffMap=function()
  offReads=offReads+1
  if onOffRead then onOffRead() end
  return offMap
 end}
end
Game.GetLocalPlayer=function()return 0 end
local onMap={}
Players[0].GetUnits=function()
 return {Members=function()return pairs(onMap)end,FindID=function(_,id)return onMap[id]end}
end
function entity(id,unitType)
 onMap[id]={GetID=function()return id end,GetType=function()return unitType or unitRow.Index end,
 GetOwner=function()return 0 end,GetX=function()return home:GetX()end,GetY=function()return home:GetY()end}
end
function bootExpedition()
 ExposedMembers={}
 include('UI/ExpeditionTrainingUI')
 productionUI=SPCExpeditionTrainingUI.New(P,function()end,function()end,function()end)
 include('NetworkInput');include('ExpeditionSpyStore');include('ExpeditionSpyGate');include('ExpeditionTraining')
 SPCExpeditionSpyGate.Start(P,shared)
 SPCExpeditionTraining.Start(P,shared)
 capacity=shared.ExpeditionGate.Training
end
function request(c,action,token,reservation)
 shared.ExpeditionTraining.Request(0,{Action=action,CityID=c:GetID(),Token=token,Reservation=reservation})
 return ExposedMembers.SPC_ExpeditionTrainingReply
end
function reserveHome()
 assert(request(home,'SYNC','sync_A').eligible)
 assert(request(other,'SYNC','sync_B').eligible)
 local reply=request(home,'RESERVE','reserve_A');assert(reply.reserved,reply.error)
 home.trainingCount=1
 assert(request(home,'CONFIRM','confirm_A','reserve_A').confirmed)
 assert(capacity.Read(0).trainingQueued and home.buildings[777])
end
function lose()
 home.trainingCount=0
 T.loss(home,9,901)
 assert(T.record(home).stage=='HELD_TRANSFER')
 assert(shared.CityProgressionStore.Status(home).exitStatus=='WITHDRAWN',shared.CityProgressionStore.Describe(9,home))
 assert(not home.buildings[777])
end
function cold()
 T.reload();bootExpedition();Events.LoadScreenClose.Fire()
end
function cancelNotice()
 Events.CityProductionCompleted.Fire(0,home:GetID(),0,90,true)
end
function checkOther(available,token)
 assert(T.control(other).active==4 and T.control(other).specialization=='CULTURE')
 assert(request(other,'SYNC',token).eligible==available)
end
bootExpedition()
"""


def runtime():
    with patch.object(cities, "LuaRuntime", LuaRuntime):
        vm = cities.fixture()
    vm.execute(SETUP)
    return vm


class SourceLoss(unittest.TestCase):
    def setUp(self):
        self.vm = runtime()
        self.vm.execute("reserveHome()")

    def test_confirmed_cancellation_then_transfer_allows_other_city_after_reload(self):
        self.vm.execute("""
        home.trainingCount=0;cancelNotice()
        assert(capacity.Read(0).phase=='ENDED','KNOWN_EMPTY_CANCEL_SHOULD_RELEASE')
        assert(not home.buildings[777]);checkOther(true,'after_cancel')
        local writes=teamWrites
        lose();cold()
        assert(capacity.Read(0).phase=='ENDED' and teamWrites==writes)
        checkOther(true,'after_reload')
        assert(request(other,'RESERVE','reserve_B').reserved)
        assert(capacity.Read(0).sourceCity==other:GetID() and other.buildings[777])
        """)

    def test_queue_removal_processed_before_transfer_already_releases(self):
        self.vm.execute("""
        home.trainingCount=0
        Events.CityProductionQueueChanged.Fire(0,home:GetID())
        Events.GameCoreEventPublishComplete.Fire()
        assert(capacity.Read(0).phase=='ENDED');lose();cold()
        checkOther(true,'after_reload')
        """)

    def test_confirmed_transfer_releases_once_and_other_city_can_train_after_reload(self):
        self.vm.execute("""
        local oldID=home:GetID();home.trainingCount=0
        Events.CityProductionQueueChanged.Fire(0,oldID)
        lose()
        assert(not CityManager.GetCity(0,oldID) and capacity.NoUnits(0))
        local s=capacity.Read(0)
        assert(s.phase=='HELD' and s.stop==capacity.TransferredOrder and s.trainingQueued)
        assert(not s.unitID and not s.trainingBorn and not s.trainingCompleted)
        checkOther(false,'before_publish')
        Events.GameCoreEventPublishComplete.Fire()
        assert(capacity.Read(0).phase=='ENDED' and offReads==1)
        local writes=teamWrites
        shared.CityProgressionStore.ExitConfirmed();cold();Events.PlayerTurnActivated.Fire(0)
        assert(teamWrites==writes);checkOther(true,'after_reload')
        assert(request(other,'RESERVE','reserve_B').reserved)
        other.trainingCount=1;assert(request(other,'CONFIRM','confirm_B','reserve_B').confirmed)
        Events.CityProductionCompleted.Fire(0,oldID,0,90,true)
        assert(capacity.Read(0).phase=='TRAINING' and capacity.Read(0).sourceCity==other:GetID())
        assert(other.buildings[777])
        """)

    def test_unknown_off_map_then_spy_returns_without_repeated_idle_samples(self):
        self.vm.execute("""
        offMap=1;lose();Events.GameCoreEventPublishComplete.Fire()
        assert(offReads==1 and capacity.Read(0).stop==capacity.TransferredOrder)
        for i=1,50 do
         Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()
        end
        checkOther(false,'offmap_wait');assert(offReads==1)
        cold();assert(offReads==2 and capacity.Read(0).phase=='HELD')
        local info=P.Info
        P.Info=function(t,k)if t=='Units' and k==91 then return GameInfo.Units[91] end;return info(t,k)end
        entity(72,91);offMap=0;Events.UnitAddedToMap.Fire(0,72)
        Events.GameCoreEventPublishComplete.Fire()
        assert(offReads==3 and capacity.Read(0).phase=='ENDED');checkOther(true,'spy_return')
        """)

    def test_unavailable_off_map_reader_never_certifies_zero(self):
        for bad in ("nil", "'0'", "-1", "0/0"):
            with self.subTest(value=bad):
                vm=runtime()
                vm.execute("reserveHome();offMap="+bad+""";lose()
                Events.GameCoreEventPublishComplete.Fire();checkOther(false,'unknown')
                assert(capacity.Read(0).stop==capacity.TransferredOrder)
                offMap=0;cold();checkOther(true,'cold')
                """)

    def test_closed_or_replaced_ui_cannot_release_from_stale_sample(self):
        self.vm.execute("""
        onOffRead=function()productionUI.Close();onOffRead=nil end
        lose();Events.GameCoreEventPublishComplete.Fire()
        checkOther(false,'closed');assert(offReads==1)
        local replacement=SPCExpeditionTrainingUI.New(P,function()end,function()end,function()end)
        Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()
        assert(offReads==2);checkOther(true,'new_reader')
        """)

    def test_receipt_during_or_after_transfer_never_releases_order(self):
        for notice in ("Events.CityProductionCompleted.Fire(0,oldID,0,90,false)",
                       "entity(71);Events.UnitAddedToMap.Fire(0,71)"):
            for boundary in ("marker", "before_read", "during_read"):
                with self.subTest(notice=notice, boundary=boundary):
                    vm=runtime()
                    vm.execute("reserveHome();oldID=home:GetID();function notice()"+notice+" end")
                    if boundary=="marker":
                        vm.execute("local remove=P.RemoveBuilding;P.RemoveBuilding=function(b,id)remove(b,id);notice()end")
                    if boundary=="during_read":
                        vm.execute("onOffRead=function()onOffRead=nil;notice()end")
                    vm.execute("lose()")
                    if boundary=="before_read":
                        vm.execute("notice()")
                    vm.execute("""
                    Events.GameCoreEventPublishComplete.Fire();cold()
                    assert(capacity.Read(0).stop=='TRAINING_SOURCE_RECEIPT_CONFLICT')
                    checkOther(false,'protected')
                    """)

    def test_early_source_read_failure_requires_matching_verified_handover(self):
        self.vm.execute("""
        home.s.ref.owner=9;home.s.ref.cityID=901
        Events.PlayerTurnActivated.Fire(0)
        assert(capacity.Read(0).stop=='TRAINING_SOURCE_CHANGED')
        checkOther(false,'unproven');assert(offReads==0)
        lose();Events.GameCoreEventPublishComplete.Fire();checkOther(true,'verified')
        """)

    def test_completion_between_source_disappearance_and_verified_handover_is_preserved(self):
        self.vm.execute("""
        local oldID=home:GetID();home.s.ref.owner=9;home.s.ref.cityID=901
        Events.PlayerTurnActivated.Fire(0);assert(capacity.Read(0).stop=='TRAINING_SOURCE_CHANGED')
        Events.CityProductionCompleted.Fire(0,oldID,0,90,false)
        lose();Events.GameCoreEventPublishComplete.Fire();cold()
        assert(capacity.Read(0).stop=='TRAINING_SOURCE_RECEIPT_CONFLICT')
        checkOther(false,'late_receipt')
        """)

    def test_unconfirmed_reservation_and_different_binding_never_release(self):
        vm=runtime()
        vm.execute("""
        assert(request(home,'RESERVE','unconfirmed').reserved);lose();cold()
        assert(capacity.Read(0).phase=='HELD' and offReads==0)
        checkOther(false,'unconfirmed')
        """)
        self.vm.execute("""
        shared.CityProgressionStore.ReferenceToken=function()return 'not-the-reserved-token' end
        T.loss(home,9,901);Events.GameCoreEventPublishComplete.Fire()
        assert(shared.CityProgressionStore.Status(home).exitStatus=='PARTIAL_HELD')
        checkOther(false,'wrong_incarnation');assert(offReads==0)
        """)

    def test_positive_receipt_inside_marker_withdrawal_wins_over_cancellation(self):
        for cancel in ("cancelNotice()", "request(home,'CANCEL','cancel','reserve_A')",
                       "Events.CityProductionQueueChanged.Fire(0,home:GetID());Events.GameCoreEventPublishComplete.Fire()"):
            with self.subTest(trigger=cancel):
                vm=runtime()
                vm.execute("""reserveHome();home.trainingCount=0
                local remove=P.RemoveBuilding
                P.RemoveBuilding=function(b,id)
                 remove(b,id);Events.CityProductionCompleted.Fire(0,home:GetID(),0,90,false)
                end""")
                vm.execute(cancel)
                vm.execute("assert(capacity.Read(0).phase=='HELD');lose();cold();checkOther(false,'other')")

    def test_cancel_before_queue_updates_then_actual_handover(self):
        self.vm.execute("""
        cancelNotice();assert(capacity.Read(0).phase=='TRAINING' and home.buildings[777])
        lose();Events.GameCoreEventPublishComplete.Fire();checkOther(true,'other')
        """)

    def test_new_unit_event_during_absence_read_requires_a_new_sample(self):
        self.vm.execute("""
        local info=P.Info
        P.Info=function(t,k)if t=='Units' and k==91 then return GameInfo.Units[91]end;return info(t,k)end
        onOffRead=function()onOffRead=nil;entity(44,91);Events.UnitAddedToMap.Fire(0,44)end
        lose();Events.GameCoreEventPublishComplete.Fire()
        checkOther(false,'raced')
        Events.GameCoreEventPublishComplete.Fire();checkOther(true,'fresh')
        assert(offReads==2)
        """)

    def test_off_map_zero_with_a_live_or_unidentifiable_unit_blocks(self):
        for known in (True, False):
            with self.subTest(known=known):
                vm=runtime()
                vm.execute("reserveHome();entity(71)")
                if not known:
                    vm.execute("local info=P.Info;P.Info=function(t,k)if t=='Units' and k==90 then return nil end;return info(t,k)end")
                vm.execute("lose();Events.GameCoreEventPublishComplete.Fire();cold();checkOther(false,'uncleared')")

    def test_positive_birth_or_completion_receipt_cannot_be_released_by_cancel(self):
        for event in (
            "entity(71);Events.UnitAddedToMap.Fire(0,71)",
            "Events.CityProductionCompleted.Fire(0,home:GetID(),0,90,false)",
        ):
            with self.subTest(event=event):
                vm=runtime()
                vm.execute("reserveHome();"+event+"""
                home.trainingCount=0;cancelNotice();lose();cold()
                local s=capacity.Read(0);assert(s.phase=='HELD')
                assert(s.trainingBorn==71 or s.trainingCompleted)
                checkOther(false,'other')
                """)

    def test_present_unit_without_birth_callback_keeps_capacity(self):
        self.vm.execute("""
        entity(71);home.trainingCount=0;cancelNotice();lose();cold()
        assert(not capacity.NoUnits(0) and capacity.Read(0).phase=='HELD')
        checkOther(false,'other')
        """)

    def test_unreadable_unit_type_does_not_prove_absence(self):
        self.vm.execute("""
        entity(71);local raw=P.Info
        -- The event's type must be readable; fail only the roster sample.
        local count=0
        P.Info=function(t,k)
         if t=='Units' and k==90 then count=count+1;if count>1 then return nil end end
         return raw(t,k)
        end
        home.trainingCount=0;cancelNotice()
        assert(count>1 and capacity.Read(0).phase=='HELD')
        cold();checkOther(false,'other')
        """)

    def test_stale_or_repopulated_queue_cannot_be_released(self):
        self.vm.execute("""
        local reads=0;local reader=ExposedMembers.SPC_ExpeditionQueueRead
        ExposedMembers.SPC_ExpeditionQueueRead=function(pid,id)
         reads=reads+1;if reads==2 then home.trainingCount=1 end
         return reader(pid,id)
        end
        home.trainingCount=0;cancelNotice()
        assert(reads==2 and capacity.Read(0).phase=='HELD')
        checkOther(false,'other')
        """)

    def test_unrelated_city_handover_keeps_order_and_marker(self):
        self.vm.execute("""
        local saved=T.encode(T.props().SPC_EXPEDITION_TEAM_P0)
        T.loss(other,9,901)
        assert(capacity.Read(0).phase=='TRAINING' and home.buildings[777])
        assert(T.encode(T.props().SPC_EXPEDITION_TEAM_P0)==saved)
        cold();assert(capacity.Read(0).phase=='TRAINING' and home.buildings[777])
        """)

if __name__ == '__main__':
    unittest.main()
