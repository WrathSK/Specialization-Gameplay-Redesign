"""Verified archive loss, city choice and the Expedition action bar. Native game behavior is separate."""
import unittest
from unittest.mock import patch

from lupa.lua51 import LuaRuntime
import test_expedition_gate as gate_fixture
import test_expedition_spy_task as panel_fixture

from test_expedition_training_source_loss import runtime
from test_expedition_spy_actions_ui import normal_window
from test_expedition_spy_task import gate, ui
import test_expedition_missions as missions


FORM_TEAM = """
reserveHome()
entity(77)
GameInfo.Units[90].Name='LOC_TEAM'
Locale={Lookup=function(key)return key end}
unit=Players[0]:GetUnits():FindID(77)
unit.GetName=function()return 'LOC_TEST_NAME' end
capacity.Evidence(0,'reserve_A','trainingBorn',77)
capacity.Evidence(0,'reserve_A','trainingCompleted',true)
capacity.Finish(0,'reserve_A')
function act(action,token,fields)
 local p=fields or {};p.Action=action;p.Token=token;p.UnitID=p.UnitID or 77
 shared.ExpeditionGate.Request(0,p)
 return ExposedMembers.SPC_ExpeditionGateReply
end
local named=act('NAME','name',{NameOffmapChecked=true,NameSampleTurn=Game.GetCurrentGameTurn(),Name='LOC_TEST_NAME'})
assert(named.phase=='CREATED' and not named.error,named.error)
teamKey=capacity.Read(0).teamKey
function options(token)return act('ARCHIVES',token,{TeamKey=teamKey})end
function bind(list,token)
 local c=list.archives[1]
 return act('REBIND',token,{TeamKey=teamKey,Revision=list.storeRevision,CityID=c.id,ArchiveRef=c.ref})
end
"""


class ArchiveChoice(unittest.TestCase):
    def setUp(self):
        self.vm = runtime()
        self.vm.execute(FORM_TEAM)

    def test_verified_exit_cold_load_and_free_choice_without_governor(self):
        self.vm.execute("""
        shared.CityProgressionStore.AddExpeditionInsight(0,home,'CIVILIZATION_TEST','PEOPLE',1)
        local savedKey=capacity.Read(0).teamKey
        T.governor(0)
        assert(not ExposedMembers.SPC_ExpeditionActivity.archivePending)
        assert(options('before').error and capacity.Read(0).sourceCity==home:GetID())
        lose();cold()
        assert(ExposedMembers.SPC_ExpeditionActivity.archivePending and not capacity.Available(0))
        assert(act('DISPATCH','oldTravel').error and act('TASK','oldTask').error)
        local list=options('choices');assert(not list.error,list.error)
        assert(#list.archives==1 and list.archives[1].id==other:GetID())
        assert(bind(list,'bind').archiveAccepted)
        local writes=teamWrites
        assert(bind(list,'bind').archiveAccepted and teamWrites==writes)
        assert(bind(list,'stale').error and teamWrites==writes)
        local s=capacity.Read(0)
        assert(s.teamKey==savedKey and s.unitID==77 and s.sourceCity==other:GetID() and not s.stop)
        assert(not next(shared.CityProgressionStore.ExpeditionInsights(0,other)))
        assert(T.record(home).expeditionInsights.records['CIVILIZATION_TEST:PEOPLE'].turn==1)
        cold();assert(capacity.Read(0).sourceCity==other:GetID() and not capacity.Available(0))
        """)

    def test_no_second_culture_city_keeps_unit_and_rechecks_open_list(self):
        self.vm.execute("""
        lose()
        local list=options('beforeLoss');assert(#list.archives==1)
        T.loss(other,9,933)
        local stale=bind(list,'no');assert(stale.error and not stale.archiveAccepted)
        assert(#options('empty').archives==0 and capacity.Read(0).stop=='ARCHIVE_SOURCE_LOST')
        assert(Players[0]:GetUnits():FindID(77)==unit and not capacity.Available(0))
        """)

    def test_unavailable_source_is_not_confirmation_and_unrelated_exit_does_not_detach(self):
        self.vm.execute("""
        T.loss(other,9,933)
        assert(not ExposedMembers.SPC_ExpeditionActivity.archivePending)
        local old=home.GetOwner;home.GetOwner=function()return 9 end
        assert(act('READ','unconfirmed').phase=='HELD')
        assert(options('blocked').error and not ExposedMembers.SPC_ExpeditionActivity.archivePending)
        home.GetOwner=old;lose()
        assert(ExposedMembers.SPC_ExpeditionActivity.archivePending)
        """)

    def test_city_list_uses_current_identity_at_potential_one_and_reports_unknown_separately(self):
        self.vm.execute("""
        local low=T.fresh(3);T.register(low);T.complete(low,'DISTRICT_THEATER')
        low.GetName=function()return 'Small archive' end
        local science=T.fresh(4);T.register(science);T.complete(science,'DISTRICT_CAMPUS')
        science.GetName=function()return 'Research' end
        lose();T.governor(0)
        local list=options('initial')
        assert(#list.archives==2 and list.archives[2].id==low:GetID())
        local realBase=shared.CityProgressionStore.Base
        shared.CityProgressionStore.Base=function(pid,c)
         if c:GetID()==other:GetID() then error('unavailable')end
         return realBase(pid,c)
        end
        local partial=options('one-unreadable')
        assert(partial.partial and #partial.archives==1 and partial.archives[1].id==low:GetID())
        assert(bind(partial,'choose-low').archiveAccepted)
        """)


class MissionLoss(unittest.TestCase):
    def test_ongoing_task_cancels_without_credit_and_releases_owned_sleep(self):
        with patch.object(gate_fixture, 'LuaRuntime', LuaRuntime):
            vm = missions.Missions().ready()
        vm.execute("""
        local run=startMission('start',PEOPLE);assert(run.phase=='TASK_RUNNING')
        local training=shared.ExpeditionGate.Training
        local s=training.Read(2)
        assert(training.LoseArchive(2,s.sourceRef,s.teamKey))
        local lost=training.Read(2)
        assert(lost.stop=='ARCHIVE_SOURCE_LOST' and not lost.taskDue and not lost.missionCategory)
        assert(lost.activityMode=='RELEASE' and lost.activityKey==s.activityKey)
        currentTurn=88;ownTurn(2)
        assert(release('release').phase=='ARRIVED')
        assert(not training.Read(2).activityKey and insightWrites==0 and placeCalls==0 and destroys==0)
        assert(startMission('stale',PEOPLE).error and insightWrites==0)
        """)

    def test_next_mission_uses_chosen_archive_and_its_own_quota(self):
        with patch.object(gate_fixture, 'LuaRuntime', LuaRuntime):
            vm = missions.Missions().ready()
        vm.execute("""
        local t=shared.ExpeditionGate.Training;local s=t.Read(2)
        t.LoseArchive(2,s.sourceRef,s.teamKey)
        local new={id=8,x=2,y=4,owner=2,token='second-archive'}
        for k,v in pairs(city)do if type(v)=='function' then new[k]=v end end
        local roster=Players[2]:GetCities()
        roster.Members=function()return ipairs({new})end
        roster.FindID=function(_,id)if id==8 then return new end end
        local store=shared.CityProgressionStore
        store.Base=function(pid,c)return {owner=pid,cityID=c.id,x=c.x,y=c.y,token=c.token,specialization='CULTURE'}end
        local recorded={['CIVILIZATION_TARGET:PEOPLE']={civ='CIVILIZATION_TARGET',category='PEOPLE',turn=40}}
        store.ExpeditionInsights=function(pid,c)assert(pid==2 and c==new);return recorded end
        store.AddExpeditionInsight=function(pid,c,civ,cat,turn)
         assert(pid==2 and c==new and not recorded[civ..':'..cat])
         recorded[civ..':'..cat]={civ=civ,category=cat,turn=turn};insightWrites=insightWrites+1;return true
        end
        local function archive(action,token,extra)
         local p=extra or {};p.Action=action;p.Token=token;p.UnitID=41;p.TeamKey=s.teamKey
         handler(2,p);return ExposedMembers.SPC_ExpeditionGateReply
        end
        local choices=archive('ARCHIVES','list')
        assert(archive('REBIND','confirm',{CityID=8,ArchiveRef=choices.archives[1].ref,Revision=choices.storeRevision}).archiveAccepted)
        assert(startMission('already-recorded',PEOPLE).error=='MISSION_ALREADY_COMPLETED')
        assert(startMission('another-category',WORKS).phase=='TASK_RUNNING')
        currentTurn=85;ownTurn(2);ownTurn(2)
        assert(recorded['CIVILIZATION_TARGET:WORKS'].turn==85 and insightWrites==1)
        """)

    def test_already_dispatched_team_must_complete_existing_native_arrival(self):
        with patch.object(gate_fixture, 'LuaRuntime', LuaRuntime):
            vm = gate()
        vm.execute("""
        req('CREATE','new');nativeDispatch('travel')
        local t=shared.ExpeditionGate.Training;local s=t.Read(2)
        t.LoseArchive(2,s.sourceRef,s.teamKey)
        assert(t.Read(2).phase=='TRAVELLING' and t.Read(2).stop=='ARCHIVE_SOURCE_LOST')
        assert(arrival(41,true).phase=='ARRIVED')
        local v=ExposedMembers.SPC_ExpeditionActivity
        assert(v.archivePending and v.unitID==41 and v.teamKey==s.teamKey)
        """)



class ArchiveUI(unittest.TestCase):
    def test_archive_replaces_both_actions_for_only_the_selected_team(self):
        with patch.object(panel_fixture, 'LuaRuntime', LuaRuntime):
            vm = ui('UnitPanel')
        vm.execute("""
        phase('ARRIVED');local old=GetUnitActionsTable(team)
        ExposedMembers.SPC_ExpeditionActivity.archivePending=true
        local a=GetUnitActionsTable(team)
        assert(#a.SPECIFIC==1 and not a.SPECIFIC[1].disabled)
        old.SPECIFIC[1].CallbackFunc();old.SPECIFIC[2].CallbackFunc()
        assert(routed==0)
        a.SPECIFIC[1].CallbackFunc();assert(routed==1 and routes[1].mode=='ARCHIVE' and routes[1].id==40)
        """)

    def test_city_picker_confirms_without_native_dispatch(self):
        with patch.object(gate_fixture, 'LuaRuntime', LuaRuntime):
            vm = normal_window()
        vm.execute("""
        local training=shared.ExpeditionGate.Training;local s=training.Read(2)
        assert(training.LoseArchive(2,s.sourceRef,s.teamKey))
        local startCalls=nativeCalls;local t=city
        local function foreignRead()error('archive selection requested spy travel or mission facts')end
        SPCExpeditionSpyRead.Targets=foreignRead;SPCExpeditionSpyRead.Presentation=foreignRead
        local c={};for k,v in pairs(t)do c[k]=v end
        c.id=8;c.token='new-token';c.GetName=function()return 'Archive B'end
        local cities=Players[2]:GetCities()
        cities.Members=function()return ipairs({c})end
        cities.FindID=function(_,id)if id==8 then return c end end
        shared.CityProgressionStore.Base=function()
         return {owner=2,cityID=8,x=c:GetX(),y=c:GetY(),specialization='CULTURE',token='new-token'}
        end
        gateOpen('ARCHIVE',40)
        assert(lastPacket.Action=='ARCHIVES' and not ContextPtr.hidden)
        assert(lastPacket.UnitID==40 and Controls.NormalConfirmButton.disabled and #instanceManagers.SPCExpeditionDestination.instances==1)
        local oldClick=instanceManagers.SPCExpeditionDestination.instances[1].DestinationButton.click
        Controls.NormalCloseButton.click()
        cities.Members=function()return ipairs({})end
        gateOpen('ARCHIVE',40);assert(Controls.NormalConfirmButton.disabled and not Controls.NormalEmptyLabel.hidden)
        oldClick();assert(Controls.NormalConfirmButton.disabled and training.Read(2).stop=='ARCHIVE_SOURCE_LOST')
        Controls.NormalCloseButton.click()
        cities.Members=function()return ipairs({c})end
        gateOpen('ARCHIVE',40);oldClick();assert(Controls.NormalConfirmButton.disabled)
        chooseCity();assert(not Controls.NormalConfirmButton.disabled)
        Controls.NormalConfirmButton.click()
        local reply=ExposedMembers.SPC_ExpeditionGateReply
        assert(reply.archiveAccepted,reply.error)
        assert(ContextPtr.hidden and training.Read(2).sourceCity==8 and nativeCalls==startCalls)
        """)
