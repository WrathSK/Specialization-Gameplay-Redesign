"""City ownership D0061: production Store, Lua 5.1, simulated native delivery."""
import unittest
from unittest.mock import patch

from lupa.lua51 import LuaRuntime
import test_store_write_boundaries as store_fixture
from test_pu07a_completion_scope import SETUP as CLAIM_SETUP


SETUP = """
T.start()
P.Call=function(object,method,...)
 local f=P.Field(object,method)
 if type(f)~='function' then return false end
 return pcall(f,object,...)
end
CityTransferTypes = {BY_GIFT=-1821839791, BY_LIBERATION=361156668,
                     BY_CULTURAL_IDENTITY=-738490196, BY_COMBAT=-1173539618}
function sourceCity(i)
 return T.ai(T.fresh(i))
end
function mapTransfer(c,newOwner,newID)
 local oldOwner,oldID=c:GetOwner(),c:GetID()
 c.s.ref.owner,c.s.ref.cityID=newOwner,newID
 local x,y=c:GetX(),c:GetY()
 GameEvents.CityBuilt.Fire(newOwner,newID,x,y)
 Events.GameCoreEventPublishComplete.Fire()
 Events.CityRemovedFromMap.Fire(oldOwner,oldID)
 Events.CityAddedToMap.Fire(newOwner,newID,x,y)
 Events.CityInitialized.Fire(newOwner,newID,x,y)
end
function final(c,reason,oldOwner)
 Events.CityTransfered.Fire(c:GetOwner(),c:GetID(),oldOwner or 3,reason)
end
"""


class PeacefulAcquisition(unittest.TestCase):
    def setUp(self):
        with patch.object(store_fixture, "LuaRuntime", LuaRuntime):
            self.lua = store_fixture.fixture()
        self.lua.execute(SETUP)

    def test_gift_freezes_completed_districts_at_transfer_and_survives_reload(self):
        self.lua.execute("""
        local c=sourceCity(1)
        local writes=T.writes()
        mapTransfer(c,0,c:GetID())
        assert(not T.record(c) and T.writes()==writes)
        T.district(c,'DISTRICT_CAMPUS',201,true)
        T.district(c,'DISTRICT_THEATER',202,false)
        final(c,CityTransferTypes.BY_GIFT)
        local r=assert(T.record(c),shared.CityProgressionStore.Describe(0,c))
        local proof=r.acquisition
        assert(r.schema==3 and proof.mode=='LEGACY_CLAIM' and proof.conquered==nil)
        assert(proof.oldOwner==3 and proof.reference.owner==0 and proof.reference.cityID==c:GetID())
        assert(proof.evidence=='GIFT+Initialized+Transfer' and proof.added<proof.initialized and proof.initialized<proof.transferred)
        assert(proof.legacySet.RESEARCH and not proof.legacySet.CULTURE and T.control(c).potential==0)
        assert(shared.CityProgressionStore.ClaimState(0,c).eligible)
        local save,w=T.encode(T.props()),T.writes()
        T.complete(c,'DISTRICT_THEATER');final(c,CityTransferTypes.BY_GIFT)
        T.reload()
        assert(T.encode(T.props())==save and T.writes()==w and T.record(c).acquisition.legacySet.RESEARCH)
        """)

    def test_actual_claim_project_offers_gift_candidates_and_settles_only_once(self):
        self.lua.execute(CLAIM_SETUP)
        self.lua.execute("""
        local c=sourceCity(3)
        local q={buildings={},target='NONE',size=0};local finishes=0
        c.GetBuildings=function()return q.buildings end;c.GetBuildQueue=function()return q end
        q.CurrentlyBuilding=function()return q.target end;q.GetSize=function()return q.size end
        q.GetCurrentProductionTypeHash=function()return q.size==1 and 102 or 0 end
        q.FinishProgress=function()
         finishes=finishes+1;q.target='NONE';q.size=0
         Events.CityProjectCompleted.Fire(0,c:GetID(),102)
        end
        T.district(c,'DISTRICT_CAMPUS',501,true);T.district(c,'DISTRICT_THEATER',502,true)
        mapTransfer(c,0,901);final(c,CityTransferTypes.BY_GIFT);Events.GameCoreEventPublishComplete.Fire()
        assert(q.buildings[201] and q.buildings[202] and not q.buildings[203] and not q.buildings[204])
        q.target='PROJECT_SPC_CLAIM_CULTURE';q.size=1
        shared.ClaimProjects.Request(0,{CityID=901,Project=q.target,StartTurn=T.now()})
        assert(T.record(c).claimTimer.stage=='ACTIVE' and not T.record(c).claim and finishes==0)
        Events.PlayerTurnDeactivated.Fire(0);T.turn(1);Events.GameCoreEventPublishComplete.Fire()
        assert(finishes==1 and T.record(c).claim.kind=='CULTURE' and T.control(c).potential==1)
        local receipt=T.encode(T.record(c));Events.CityProjectCompleted.Fire(0,901,102)
        assert(finishes==1 and T.encode(T.record(c))==receipt and not next(q.buildings))
        """)

    def test_cultural_transfer_from_free_cities_uses_new_id_and_waits_for_completion(self):
        self.lua.execute("""
        local c=sourceCity(1);Players[3].IsMajor=function()return false end
        PlayerConfigurations={[3]={GetCivilizationTypeName=function()return 'CIVILIZATION_FREE_CITIES'end}}
        local info=P.Info
        P.Info=function(t,k)
         if t=='Civilizations' and k=='CIVILIZATION_FREE_CITIES' then
          return {StartingCivilizationLevelType='CIVILIZATION_LEVEL_FREE_CITIES'}
         end
         return info(t,k)
        end
        local old=c:GetID()
        mapTransfer(c,0,old+100);Events.CityTransfered.Fire(0,old,3,CityTransferTypes.BY_CULTURAL_IDENTITY)
        assert(not T.record(c))
        final(c,CityTransferTypes.BY_CULTURAL_IDENTITY)
        local f=assert(T.record(c),shared.CityProgressionStore.Describe(0,c)).acquisition
        assert(f.mode=='FIRST_COMPLETION' and f.reference.cityID==old+100 and f.evidence=='CULTURAL_IDENTITY+Initialized+Transfer')
        T.reload();T.complete(c,'DISTRICT_INDUSTRIAL_ZONE')
        assert(T.control(c).specialization=='INDUSTRY' and T.control(c).potential==1)
        """)

    def test_liberation_to_third_party_then_real_local_acquisition(self):
        self.lua.execute("""
        local c=sourceCity(1);local writes=T.writes()
        Players[4]={IsMajor=function()return true end,IsHuman=function()return false end}
        mapTransfer(c,4,706);final(c,CityTransferTypes.BY_LIBERATION)
        assert(not T.record(c) and T.writes()==writes)
        mapTransfer(c,0,808);final(c,CityTransferTypes.BY_LIBERATION,4)
        local f=assert(T.record(c)).acquisition
        assert(f.oldOwner==4 and f.reference.cityID==808 and f.evidence=='LIBERATION+Initialized+Transfer')
        """)

    def test_ambiguous_reason_and_single_event_do_not_grant(self):
        for expression in ("nil", "723", "CityTransferTypes.BY_COMBAT", "false"):
            with self.subTest(reason=expression):
                self.lua.execute("T.start();local c=sourceCity(1);local writes=T.writes();"
                                 "mapTransfer(c,0,606);final(c," + expression + ");"
                                 "assert(not T.record(c) and T.writes()==writes)")
        self.lua.execute("""
        T.start();local c=sourceCity(1);c.s.ref.owner=0
        final(c,CityTransferTypes.BY_GIFT)
        assert(not T.record(c))
        mapTransfer(c,0,202);CityTransferTypes=nil;final(c,-1821839791)
        assert(not T.record(c))
        """)

    def test_order_and_source_conflicts_are_scoped_to_the_candidate(self):
        self.lua.execute("""
        local a,b=sourceCity(1),sourceCity(2)
        a.s.ref.owner=0
        local id,x,y=a:GetID(),a:GetX(),a:GetY()
        Events.CityInitialized.Fire(0,id,x,y);Events.CityAddedToMap.Fire(0,id,x,y)
        final(a,CityTransferTypes.BY_GIFT)
        assert(not T.record(a))
        mapTransfer(b,0,908);final(b,CityTransferTypes.BY_GIFT);assert(T.record(b))
        T.start();a=sourceCity(1);a.s.ref.owner=0;id,x,y=a:GetID(),a:GetX(),a:GetY()
        GameEvents.CityConquered.Fire(0,3,id,x,y)
        Events.CityAddedToMap.Fire(0,id,x,y);Events.CityInitialized.Fire(0,id,x,y)
        final(a,CityTransferTypes.BY_GIFT);assert(not T.record(a))
        """)

    def test_failed_live_lookup_never_marks_an_unrelated_city(self):
        self.lua.execute("""
        local a,b=sourceCity(1),sourceCity(2);mapTransfer(a,0,701);mapTransfer(b,0,702)
        local get=CityManager.GetCity
        CityManager.GetCity=function(owner,id)
         if id==701 then error('injected lookup unavailable')end
         return get(owner,id)
        end
        final(a,CityTransferTypes.BY_GIFT);CityManager.GetCity=get
        assert(not T.record(a));final(b,CityTransferTypes.BY_GIFT);assert(T.record(b))
        """)

    def test_id_and_position_must_agree_even_when_both_objects_are_readable(self):
        self.lua.execute("""
        local a,b=sourceCity(1),sourceCity(2);mapTransfer(a,0,701);mapTransfer(b,0,702)
        local get=CityManager.GetCityAt
        CityManager.GetCityAt=function(x,y)if x==a:GetX() then return b end;return get(x,y)end
        final(a,CityTransferTypes.BY_GIFT)
        CityManager.GetCityAt=get
        assert(not T.record(a));final(b,CityTransferTypes.BY_GIFT);assert(T.record(b))
        """)

    def test_failing_plot_read_or_wrong_registered_city_cannot_hold_another_record(self):
        for failure_throws in (True, False):
            with self.subTest(failure_throws=failure_throws):
                self.lua.globals().failure_throws = failure_throws
                self.lua.execute("""
                T.start();local other=T.fresh(3);T.register(other)
                local a,b=sourceCity(1),sourceCity(2);mapTransfer(a,0,701);mapTransfer(b,0,702)
                local get=CityManager.GetCityAt
                CityManager.GetCityAt=function(x,y)
                 if x==a:GetX() then if failure_throws then error('injected') end;return other end
                 return get(x,y)
                end
                local before=T.encode(T.record(other));final(a,CityTransferTypes.BY_GIFT)
                CityManager.GetCityAt=get
                assert(not T.record(a) and T.encode(T.record(other))==before)
                final(b,CityTransferTypes.BY_GIFT);assert(T.record(b))
                T.complete(other,'DISTRICT_CAMPUS');assert(T.control(other).specialization=='RESEARCH')
                """)

    def test_wrong_source_unknown_level_or_cross_turn_cannot_allocate_identity(self):
        self.lua.execute("""
        local c=sourceCity(1);mapTransfer(c,0,701);final(c,CityTransferTypes.BY_GIFT,0)
        assert(not T.record(c))
        T.start();c=sourceCity(1);mapTransfer(c,0,701);T.turn(1);final(c,CityTransferTypes.BY_GIFT)
        assert(not T.record(c))
        T.start();c=sourceCity(1);Players[3].IsHuman=function()return true end
        mapTransfer(c,0,701);final(c,CityTransferTypes.BY_GIFT);assert(not T.record(c))
        T.start();c=sourceCity(1);Players[3].IsMajor=function()return false end
        PlayerConfigurations={};mapTransfer(c,0,701);final(c,CityTransferTypes.BY_GIFT)
        assert(not T.record(c) and T.index().counter==0)
        """)

    def test_missing_marker_direct_gift_restores_old_candidates_without_resnapshot(self):
        self.lua.execute("""
        local c=sourceCity(1);T.district(c,'DISTRICT_CAMPUS',201,true)
        mapTransfer(c,0,701);final(c,CityTransferTypes.BY_GIFT)
        include('RuntimeWork');SPCRuntimeWork.StartRetirement(P,shared)
        local s=shared.CityProgressionStore;s.RegisterExit('TestCleanup',function()end)
        local key=T.key(c);local old=T.encode(T.record(c).acquisition)
        T.loss(c,3,50);c.s.values.TOKEN=nil
        assert(s.Status(c).exitStatus=='WITHDRAWN')
        T.district(c,'DISTRICT_THEATER',202,true)
        mapTransfer(c,0,902);final(c,CityTransferTypes.BY_GIFT)
        local r=T.props()[key]
        assert(r.stage=='ACTIVE',s.Status(c).returnRejection)
        assert(T.index().counter==1 and r.returnProof.version==3 and r.returnProof.conquest==nil)
        assert(r.returnEvidence=='GIFT+Initialized+Transfer' and r.current.cityID==902 and r.lastLoss.target.cityID==50)
        assert(T.encode(r.acquisition)==old and not r.acquisition.legacySet.CULTURE)
        local save,w=T.encode(T.props()),T.writes()
        final(c,CityTransferTypes.BY_GIFT);T.reload()
        assert(T.control(c).potential==0 and T.encode(T.props())==save and T.writes()==w)
        """)

    def test_return_after_foreign_load_keeps_research_investment_and_uses_current_governor(self):
        self.lua.execute("""
        local c=T.fresh(1);T.register(c);T.complete(c,'DISTRICT_CAMPUS');T.invest(c,8001)
        local key=T.key(c);local token=T.record(c).base.token
        local function startExit()
         include('RuntimeWork');SPCRuntimeWork.StartRetirement(P,shared)
         shared.CityProgressionStore.RegisterExit('TestCleanup',function()end)
         shared.CityProgressionStore.ExitConfirmed()
        end
        startExit();T.loss(c,3,50);c.s.values.TOKEN=nil
        T.reload();startExit();T.governor(1)
        mapTransfer(c,0,902);final(c,CityTransferTypes.BY_GIFT)
        local r=T.props()[key];assert(r.stage=='ACTIVE' and r.base.token==token)
        assert(T.control(c).potential==2 and T.control(c).active==1 and T.index().counter==1)
        local save,w=T.encode(T.props()),T.writes();T.reload()
        assert(T.control(c).potential==2 and T.encode(T.props())==save and T.writes()==w)
        """)

    def test_invalid_saved_return_witness_cannot_restore_a_missing_marker(self):
        self.lua.execute("""
        local c=T.fresh(1);T.register(c);local key=T.key(c)
        include('RuntimeWork');SPCRuntimeWork.StartRetirement(P,shared)
        shared.CityProgressionStore.RegisterExit('TestCleanup',function()end)
        T.loss(c,3,50);c.s.values.TOKEN=nil;mapTransfer(c,0,902);final(c,CityTransferTypes.BY_GIFT)
        local r=T.props()[key];assert(r.stage=='ACTIVE')
        r.returnProof.foundation.sequence=r.returnProof.removed
        local before,w=T.encode(T.props()),T.writes();T.reload()
        assert(not pcall(T.control,c) and T.encode(T.props())==before and T.writes()==w)
        """)

    def test_peaceful_reason_cannot_replace_missing_old_removal_or_verified_exit(self):
        for missing in ("old_removal", "exit", "reason", "destination", "built_after_removal"):
            with self.subTest(missing=missing):
                self.lua.globals().missing = missing
                self.lua.execute("""
                T.start()
                local c=T.fresh(1);T.register(c)
                local key=T.key(c);include('RuntimeWork');SPCRuntimeWork.StartRetirement(P,shared)
                local s=shared.CityProgressionStore
                s.RegisterExit('TestCleanup',function()return missing~='exit'end)
                T.loss(c,3,50);c.s.values.TOKEN=nil
                c.s.ref.owner,c.s.ref.cityID=0,902
                local x,y=c:GetX(),c:GetY()
                if missing~='built_after_removal' then GameEvents.CityBuilt.Fire(0,902,x,y) end
                if missing~='old_removal' then Events.CityRemovedFromMap.Fire(3,50) end
                if missing=='built_after_removal' then GameEvents.CityBuilt.Fire(0,902,x,y) end
                Events.CityAddedToMap.Fire(0,902,x,y);Events.CityInitialized.Fire(0,902,x,y)
                local get=CityManager.GetCity
                if missing=='destination' then CityManager.GetCity=function()return nil end end
                local reason=CityTransferTypes.BY_GIFT;if missing=='reason' then reason=nil end
                final(c,reason);CityManager.GetCity=get
                assert(T.props()[key].stage=='HELD_TRANSFER' and T.index().counter==1)
                """)

    def test_known_history_and_existing_conquest_keep_their_own_paths(self):
        self.lua.execute("""
        local c=sourceCity(1);T.district(c,'DISTRICT_CAMPUS',201,true);T.take(c)
        local record=T.record(c);assert(record.acquisition.evidence=='CONQUEST+Initialized+Transfer')
        local original,token=T.encode(record.acquisition),record.base.token
        T.loss(c,3,700);mapTransfer(c,0,701);final(c,CityTransferTypes.BY_GIFT)
        assert(T.index().counter==1 and T.record(c).base.token==token)
        assert(T.encode(T.record(c).acquisition)==original)
        """)
