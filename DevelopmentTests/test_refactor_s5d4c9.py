"""CultureNetwork physical health vs network proof; actual D cause producer."""
import unittest
import test_culture_network as historical
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,measure

def fixture(with_d=True,cold=False):
    historical.LuaRuntime=TrackedLua51
    l=TrackedLua51(unpack_returned_tuples=True)
    l.globals().include=lambda n:l.execute((ROOT/'Mod'/(n+'.lua')).read_text())
    with legacy_source_observation():
        l.execute(historical.BASE);l.execute(historical.ADAPT)
    l.execute("""
    local create,remove=P.CreateBuilding,P.RemoveBuilding
    P.CreateBuilding=function(q,id)create(q,id);GameEvents.BuildingPillageStateChanged.Fire(q.city.owner,q.city.id,id,false)end
    P.RemoveBuilding=function(b,id)local plot=b:GetBuildingLocation(id);remove(b,id);Events.BuildingRemovedFromMap.Fire(plot,0,id,b.city.owner)end
    local info=P.Info;P.Info=function(t,k)if t=='Buildings'and k=='BUILDING_SPC_OTHER'then return {BuildingType=k}end;return info(t,k)end
    Map.GetPlotIndex=function(x,y)return x end
    CityManager={GetDistrictAt=function(x,y)local c=cities[x/100];if c then return {GetCity=function()return c end}end end}
    function loss(id)P.RemoveBuilding(cities[id]:GetBuildings(),'BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0')end
    """)
    with legacy_source_observation():
        for n in ('FactChanges','NativeFacts','FactConsumerBindings','DistrictCompleteness'):l.globals().include(n)
    l.execute('SPCFactChanges.New(shared);SPCNativeFacts.New(P,shared)')
    if with_d:l.execute('SPCDistrictCompleteness.Start(P,shared)')
    with legacy_source_observation():
        for n in ('NetworkBridge','CultureNetwork'):l.globals().include(n)
    l.execute('SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true;cities[4].active=4;SPCCultureNetwork.Start(P,shared);cn=shared.CultureNetwork')
    l.execute("SPCFactConsumerBindings.New(shared);function pulse()shared.FactChanges.Flush();shared.FactBindings.Flush();Events.GameCoreEventPublishComplete.Fire()end;complete(4,1)")
    if cold:
        l.execute("cities[1].present.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0=true;cities[1].locations.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0=100;fire('LoadScreenClose');assert(amount(cities[1])==1)")
    else:l.execute("send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);fire('LoadScreenClose');pulse();assert(amount(cities[1])==1)")
    return l

class CultureNetworkHealth(unittest.TestCase):
    def test_external_loss_exact_receiver_then_idle_no_reads(self):
        l=fixture();l.execute("factReads={};historyReads={};loss(1);pulse();assert(amount(cities[1])==1 and factReads[1]==1 and historyReads[4]==1 and not factReads[2]and not factReads[5]);local a,b=created,removed;local h=historyReads[4];for i=1,1000 do pulse()end;assert(created==a and removed==b and historyReads[4]==h)")
        measure('S5d4c9_receiver_health',{'receiver_facts':1,'source_history_reads':1,'unrelated_receiver_reads':0,'thousand_idle_writes':0})
    def test_present_damage_uses_existing_location_pillage_policy(self):
        l=fixture();l.execute("cities[1].damage.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0=true;GameEvents.BuildingPillageStateChanged.Fire(0,1,'BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0',true);pulse();assert(amount(cities[1])==1 and not cities[1].damage.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0)")
    def test_pending_health_never_replays_or_promotes_retained_network(self):
        l=fixture();l.execute("net.CheckEvidence(false);loss(1);local a,b=created,removed;pulse();assert(amount(cities[1])==0 and created==a and removed==b and cn.records['0:1'].retained and not net.TransactionCurrent(0));local h=historyReads[4];for i=1,1000 do pulse()end;assert(created==a and removed==b and historyReads[4]==h);send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);pulse();assert(amount(cities[1])==1)")
    def test_continuity_only_health_does_not_rebuild_unchanged_retained_projection(self):
        l=fixture();l.execute("units[12]=nil;net.CheckEvidence(false);pulse();assert(net.Input(0).continuityOnly and amount(cities[1])==1 and amount(cities[5])==0);loss(1);local n=created;pulse();assert(amount(cities[1])==0 and created==n and not net.TransactionCurrent(0));send('0,4,0,2,10;0,2,0,1,11',2);pulse();assert(amount(cities[1])==1)")
    def test_cold_pending_installed_value_never_recreated_without_proof(self):
        l=fixture(cold=True);l.execute("loss(1);local n=created;pulse();assert(created==n and amount(cities[1])==0);send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);pulse();assert(amount(cities[1])==1 and propertyWrites==0)")
    def test_source_UNKNOWN_retains_prior_contribution_health_does_not_confirm_it(self):
        l=fixture();l.execute("cities[4].historyUnknown=true;loss(1);pulse();assert(amount(cities[1])==1 and cn.records['0:1'].provenance[4].status=='RETAINED');cities[4].active=3;shared.DistrictCompleteness.MarkDirty(0,4);pulse();assert(amount(cities[1])==0 and amount(cities[2])==0 and amount(cities[5])==0)")
    def test_exact_D_receiver_loss_preserves_other_receivers_and_repair(self):
        l=fixture();l.execute("cities[1].pillaged=true;factReads={};Events.DistrictPillaged.Fire(0,1,1);pulse();assert(amount(cities[1])==0 and amount(cities[2])==1 and not factReads[2]and not factReads[5]);cities[1].pillaged=false;Events.DistrictBuildProgressChanged.Fire(0,1,1);pulse();assert(amount(cities[1])==1)")
    def test_source_D_flows_reverse_dependencies(self):
        l=fixture();l.execute("cities[4].active=3;factReads={};Events.DistrictBuildProgressChanged.Fire(0,4,4);pulse();assert(amount(cities[1])==0 and amount(cities[2])==0 and amount(cities[5])==0 and factReads[1]==1 and factReads[2]==1 and factReads[5]==1)")
    def test_new_health_during_own_create_remains_next_snapshot(self):
        l=fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once then once=false;cities[5].present.BUILDING_SPC_CULTURE_NETWORK_INDUSTRY_0=nil;GameEvents.BuildingPillageStateChanged.Fire(0,5,'BUILDING_SPC_CULTURE_NETWORK_INDUSTRY_0',false)end end;loss(1);pulse();assert(amount(cities[1])==1 and amount(cities[5])==0);pulse();assert(amount(cities[5])==1)")
    def test_true_damage_during_create_not_suppressed(self):
        l=fixture();l.execute("onCreate=function(c,id)if c.id==1 then onCreate=nil;c.damage[id]=true;GameEvents.BuildingPillageStateChanged.Fire(0,c.id,id,true)end end;loss(1);pulse();assert(amount(cities[1])==0);pulse();assert(amount(cities[1])==1)")
    def test_failed_create_waits_actual_health_no_idle_retry(self):
        l=fixture();l.execute("createFail=true;loss(1);pulse();assert(cn.errors['0:1']and amount(cities[1])==0);createFail=false;local a,b=created,removed;for i=1,1000 do pulse()end;assert(created==a and removed==b);GameEvents.BuildingPillageStateChanged.Fire(0,1,'BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0',false);pulse();assert(amount(cities[1])==1 and not cn.errors['0:1'])")
    def test_foreign_and_unowned_health_do_not_read(self):
        l=fixture();l.execute("factReads={};GameEvents.BuildingPillageStateChanged.Fire(3,1,'BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0',true);GameEvents.BuildingPillageStateChanged.Fire(0,1,'BUILDING_SPC_OTHER',true);pulse();assert(not next(factReads))")
    def test_optional_D_absence_keeps_original_district_fallback(self):
        l=fixture(with_d=False);l.execute("cities[1].pillaged=true;Events.DistrictPillaged.Fire(0,999,1);pulse();assert(amount(cities[1])==0 and amount(cities[2])==1);cities[1].pillaged=false;Events.DistrictRepaired.Fire(0,999,1);pulse();assert(amount(cities[1])==1)")
    def test_busy_changed_set_preserved_without_owner_widening(self):
        l=fixture();l.execute("cn.busy=true;cn.Audit({player=0,changed={[1]=true}});cn.busy=false;factReads={};pulse();assert(factReads[1]==1 and not factReads[2]and not factReads[5])")

if __name__=='__main__':unittest.main()
