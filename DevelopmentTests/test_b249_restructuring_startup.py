"""B249: actual Store/service startup without assuming LoadScreenClose delivery.

Local event/readback fixtures only; no native training or save-file PASS.
"""
import subprocess
import unittest
import xml.etree.ElementTree as ET

from test_b247_restructuring import runtime, R
from test_b248_training_entry import investment

TRACE = """
traces={}
SPCExpeditionTrainingDiagnostics={New=function()return {Record=function(stage,v)
 traces[#traces+1]={stage=stage,v=v}
end}end}
function startService()SPCRestructuring.Start(P,shared);svc=shared.Restructuring end
function ready()
 assert(svc.ready and source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)
 assert(not c.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)
end
"""


def case():
    l = runtime()
    l.execute(TRACE)
    return l


class Startup(unittest.TestCase):
    def test_existing_store_starts_without_load_notification(self):
        case().execute("startService();ready()")

    def test_load_already_fired_before_subscription(self):
        case().execute("Events.LoadScreenClose.Fire();startService();ready()")

    def test_load_event_unavailable(self):
        case().execute("Events.LoadScreenClose=nil;startService();Events.GameCoreEventPublishComplete.Fire();ready()")

    def test_waiting_store_retries_on_publication_without_losing_city_dirty(self):
        case().execute("""
        local status=Z.st().HistoryStartStatus;Z.st().HistoryStartStatus=function()return 'WAITING'end
        local read=shared.EffectiveFacts.Read;local reads=0
        shared.EffectiveFacts.Read=function(...)reads=reads+1;return read(...)end
        startService();svc.Refresh(0,source:GetID());Events.GameCoreEventPublishComplete.Fire()
        assert(not svc.ready and reads==0 and T.control(source).active==4)
        assert(#traces==1 and traces[1].stage=='REST_INIT_WAIT' and traces[1].v.reason=='REST_STORE_WAITING')
        Z.st().HistoryStartStatus=status;Events.GameCoreEventPublishComplete.Fire();ready()
        assert(traces[2].stage=='REST_INIT_READY')
        """)

    def test_held_store_does_not_write_and_recovers_on_player_event(self):
        case().execute("""
        local status=Z.st().HistoryStartStatus;Z.st().HistoryStartStatus=function()return 'HELD'end
        local writes=T.writes();startService();Events.PlayerTurnActivated.Fire(0)
        assert(not svc.ready and not source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS and T.writes()==writes)
        assert(traces[1].v.reason=='REST_STORE_HELD')
        Z.st().HistoryStartStatus=status;Events.PlayerTurnActivated.Fire(0);ready()
        """)

    def test_unknown_store_status_is_not_assumed_ready(self):
        case().execute("Z.st().HistoryStartStatus=function()return nil end;startService();assert(not svc.ready and traces[1].v.reason=='REST_STORE_STATUS_UNKNOWN')")

    def test_dependency_error_is_redacted_and_recoverable_on_event(self):
        case().execute("""
        local status=Z.st().HistoryStartStatus
        Z.st().HistoryStartStatus=function()error('REST_STORE_UNAVAILABLE private detail')end
        startService();assert(not svc.ready and traces[1].v.reason=='REST_STORE_UNAVAILABLE')
        Z.st().HistoryStartStatus=status;Events.GameCoreEventPublishComplete.Fire();ready()
        """)

    def test_missing_facts_waits_then_committed_investment_can_start(self):
        l = case(); investment(l)
        l.execute("""
        local f=shared.EffectiveFacts;shared.EffectiveFacts=nil;startService()
        assert(not svc.ready and traces[1].v.reason=='REST_FACTS_UNAVAILABLE')
        shared.EffectiveFacts=f
        refreshInvestmentSupport(0,{status='COMMITTED',city=source:GetID()});ready()
        """)

    def test_missing_marker_definition_never_claims_ready(self):
        case().execute("""
        local info=P.Info;P.Info=function(t,k)if k=='BUILDING_SPC_RESTRUCTURING_ACCESS'then return nil end;return info(t,k)end
        startService();assert(not svc.ready and traces[1].v.reason=='REST_MARKER_MISSING')
        P.Info=info;Events.GameCoreEventPublishComplete.Fire();ready()
        """)

    def test_empty_city_collection_bootstraps_then_city_notification_grants_access(self):
        case().execute("""
        local cities=Players[0].GetCities;Players[0].GetCities=function()return {Members=function()return pairs({})end}end
        startService();assert(svc.ready and not source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)
        Players[0].GetCities=cities;svc.Refresh(0,source:GetID());ready()
        """)

    def test_wrong_player_and_noncommerce_never_granted_access(self):
        case().execute("""
        startService();ready();local read=shared.EffectiveFacts.Read
        shared.EffectiveFacts.Read=function()error('UNEXPECTED_READ')end
        svc.Refresh(3,source:GetID());Events.PlayerTurnActivated.Fire(3)
        shared.EffectiveFacts.Read=read;T.governor(3);Events.GovernorChanged.Fire(0)
        assert(not source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS and not other.markers.BUILDING_SPC_RESTRUCTURING_ACCESS)
        T.governor(4);Events.GovernorChanged.Fire(0);ready()
        """)


class RepeatedEvents(unittest.TestCase):
    def test_duplicate_load_publish_events_do_not_reinitialize_or_write(self):
        case().execute("""
        startService();ready();local writes=T.writes();local create,remove=P.CreateBuilding,P.RemoveBuilding;local calls=0
        P.CreateBuilding=function(...)calls=calls+1;return create(...)end
        P.RemoveBuilding=function(...)calls=calls+1;return remove(...)end
        for i=1,3 do Events.LoadScreenClose.Fire();Events.GameCoreEventPublishComplete.Fire();Events.PlayerTurnActivated.Fire(0)end
        ready();assert(calls==0 and T.writes()==writes)
        local n=0;for _,x in ipairs(traces)do if x.stage=='REST_INIT_READY'then n=n+1 end end;assert(n==1)
        """)

    def test_duplicate_load_preserves_prepared_action(self):
        case().execute("""
        startService();Z.command('REST_PREPARE','preview');assert(svc.views['0:400'].prepared=='preview')
        Events.LoadScreenClose.Fire();Events.GameCoreEventPublishComplete.Fire()
        assert(svc.Read(0,400).prepared=='preview');assert(Z.command('REST_CONFIRM','commit','preview').ok)
        assert(T.control(c).potential==3)
        """)

    def test_duplicate_load_preserves_unmatched_birth_and_completion(self):
        for first in ("birth", "completion"):
            with self.subTest(first=first):
                case().execute("""
                startService();local t=Z.team(401,false);t.x=source:GetX();t.y=source:GetY()
                if '%s'=='birth'then Events.UnitAddedToMap.Fire(0,401)
                else Events.CityProductionCompleted.Fire(0,source:GetID(),0,247,false)end
                Events.LoadScreenClose.Fire()
                if '%s'=='birth'then Events.CityProductionCompleted.Fire(0,source:GetID(),0,247,false)
                else Events.UnitAddedToMap.Fire(0,401)end
                Events.GameCoreEventPublishComplete.Fire()
                local b=t:GetProperty(SPCRestructuringModel.UNIT_KEY)
                assert(b and b.source.token==Z.st().HistoricalReference(source).token)
                """ % (first, first))

    def test_waiting_does_not_consume_training_pair(self):
        case().execute("""
        local status=Z.st().HistoryStartStatus;Z.st().HistoryStartStatus=function()return 'WAITING'end
        startService();local t=Z.team(401,false);t.x=source:GetX();t.y=source:GetY()
        Events.UnitAddedToMap.Fire(0,401);Events.CityProductionCompleted.Fire(0,source:GetID(),0,247,false)
        Events.GameCoreEventPublishComplete.Fire();assert(not t:GetProperty(SPCRestructuringModel.UNIT_KEY))
        Z.st().HistoryStartStatus=status;Events.GameCoreEventPublishComplete.Fire()
        assert(t:GetProperty(SPCRestructuringModel.UNIT_KEY).source.token==Z.st().HistoricalReference(source).token)
        """)

    def test_reentrant_marker_event_does_not_repeat_bootstrap(self):
        case().execute("""
        local create=P.CreateBuilding;local calls=0
        P.CreateBuilding=function(...)calls=calls+1;Events.GameCoreEventPublishComplete.Fire();return create(...)end
        startService();ready();assert(calls==1)
        """)


class Recovery(unittest.TestCase):
    def test_realallocating_recovery_without_load_repairs_binding_once(self):
        case().execute("""
        Z.begin();local before=T.encode(Z.state());T.reload()
        startService();assert(svc.ready and c.markers.BUILDING_SPC_REALLOCATING)
        assert(u:GetProperty(SPCRestructuringModel.UNIT_KEY).target and T.encode(Z.state())==before)
        local writes=T.writes();Events.LoadScreenClose.Fire();Events.GameCoreEventPublishComplete.Fire()
        assert(T.writes()==writes and T.control(c).potential==3 and Z.kills==0)
        """)

    def test_consumed_receipt_finalizes_once_without_native_replay(self):
        case().execute("""
        Z.begin();T.turn(5);Z.configure();Z.units[400]=nil;Z.st().ConfirmRestructuringConsumption(0,c,team)
        T.reload();startService();assert(T.control(c).specialization=='CULTURE' and Z.state().phase=='SETTLED')
        local writes=T.writes();Events.LoadScreenClose.Fire();Events.GameCoreEventPublishComplete.Fire()
        assert(T.writes()==writes and Z.kills==0 and not c.markers.BUILDING_SPC_REALLOCATING)
        """)

    def test_missing_consumption_receipt_stays_held(self):
        case().execute("""
        Z.begin();T.turn(5);Z.configure();T.reload();startService();local writes=T.writes()
        for i=1,3 do Events.LoadScreenClose.Fire();Events.GameCoreEventPublishComplete.Fire()end
        assert(Z.state().phase=='CONSUMING' and not Z.state().consumed and Z.units[400] and Z.kills==0)
        assert(T.writes()==writes and T.control(c).active==0 and c.markers.BUILDING_SPC_REALLOCATING)
        """)

    def test_per_city_recovery_failure_does_not_block_other_access(self):
        case().execute("""
        Z.begin();T.reload();local read=shared.EffectiveFacts.Read
        shared.EffectiveFacts.Read=function(pid,x)if x==c then error('REST_FACTS_UNAVAILABLE')end;return read(pid,x)end
        startService();ready();assert(not u:GetProperty(SPCRestructuringModel.UNIT_KEY).target)
        shared.EffectiveFacts.Read=read;svc.Refresh(0,c:GetID())
        assert(u:GetProperty(SPCRestructuringModel.UNIT_KEY).target and T.control(c).potential==3)
        """)


class Package(unittest.TestCase):
    def test_only_runtime_service_and_build_stamp_changed(self):
        changed = subprocess.check_output(['git','diff','1710c7e','--name-only','--','Mod'],cwd=R,text=True).splitlines()
        self.assertEqual(set(changed), {'Mod/Restructuring.lua', 'Mod/SpecializationP0.modinfo', 'Mod/Probe.lua'})
        probe = subprocess.check_output(['git','show','1710c7e:Mod/Probe.lua'],cwd=R,text=True)
        self.assertEqual((R/'Mod/Probe.lua').read_text(), probe.replace('P0-B-248.275','P0-B-249.276'))
        root = ET.parse(R/'Mod/SpecializationP0.modinfo').getroot()
        self.assertEqual(root.get('version'), '276')
        files = [x.text for x in root.findall('./Files/File')]
        actual = {str(p.relative_to(R/'Mod')) for p in (R/'Mod').rglob('*') if p.is_file() and p.name not in ('.DS_Store','SpecializationP0.modinfo')}
        self.assertEqual(len(files),len(set(files)));self.assertEqual(set(files),actual)

    def test_lua51_syntax(self):
        from lupa.lua51 import LuaRuntime
        LuaRuntime().execute("assert(loadstring(...))", (R/'Mod/Restructuring.lua').read_text())


if __name__ == '__main__':
    unittest.main()
