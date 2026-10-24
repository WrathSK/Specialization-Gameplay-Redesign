"""S4b actual bridge + actual effect owners. Lua51, explicit native/Store doubles."""
import ast
import unittest
from pathlib import Path
from refactor_harness import TrackedLua51,legacy_source_observation,ROOT
from refactor_defect_fixtures import commerce


def culture(ready=True):
    import test_culture_network as module
    module.LuaRuntime=TrackedLua51
    with legacy_source_observation():return module.fixture(ready)


def standard(ready=True,cold=False):
    l=culture(False)
    l.execute(r"""
      local rows=P.Rows
      P.Rows=function(tab)
       if tab=='SPC_StandardizationTargets'then return {{Kind='BUILDING',TargetType='BUILDING_GRANARY',CarrierType='BUILDING_SPC_STD_10'}}end
       if tab=='SPC_StandardizationLevels'then return {{Kind='BUILDING',TargetType='BUILDING_GRANARY',CarrierType='BUILDING_SPC_STD_12',Level=1},{Kind='BUILDING',TargetType='BUILDING_GRANARY',CarrierType='BUILDING_SPC_STD_14',Level=2}}end
       return rows(tab)
      end
      for _,n in ipairs({10,12,14})do local name='BUILDING_SPC_STD_'..n;info[name]={Index=name,BuildingType=name,InternalOnly=1,PrereqDistrict='DISTRICT_CITY_CENTER',CitizenSlots=0,Housing=0}end
      SPCStandardizationCatalog={Build=function()return {buildings={BUILDING_GRANARY={enabled=true,group='G',district='DISTRICT_CITY_CENTER',tier=1,name='Granary'}},districts={}}end}
      shared.StandardizationDiscount={retired=true,changes=0,Withdraw=function()return true end}
      shared.CopyYields={retired=true,changes=0,Withdraw=function()return true end}
      knowledge={};studies={};for id in pairs(cities)do knowledge[id]={learned={},districts={learned={}}};studies[id]=0 end
      shared.Standardization={ReadKnowledge=function(pid,c)if knowledge[c.id]==false then error('STD_HISTORY_UNAVAILABLE')end;return knowledge[c.id]end}
      shared.CityProgressionStore.EngineeringState=function(pid,c)return {token=c.token,value={L=studies[c.id]}}end
      function learn(id)knowledge[id].learned.BUILDING_GRANARY={district='DISTRICT_CITY_CENTER',tier=1}end
      cities[3].kind='INDUSTRY';cities[3].potential=4;cities[3].active=4
      cities[5].active=4;studies[3]=1;studies[5]=2;learn(3);learn(5)
      function stdValue(id)for _,n in ipairs({10,12,14})do if cities[id].present['BUILDING_SPC_STD_'..n]then return n end end;return 0 end
    """)
    if cold:l.execute("cities[1].present.BUILDING_SPC_STD_14=true")
    l.execute((ROOT/'Mod/StandardizationEffects.lua').read_text());l.execute('SPCStandardizationEffects.Start(P,shared);std=shared.StandardizationEffects')
    if ready:l.execute("send('0,5,0,2,10;0,3,0,2,11;0,2,0,1,12',3);fire('LoadScreenClose')")
    return l


def cold_commerce():
    # Reuse only the explicitly engine-shaped setup block; do not restart owners
    # or copy context caches. Actual Commerce source then runs once in a new VM.
    l=culture(False)
    l.execute((ROOT/'Mod/CommerceModel.lua').read_text())
    tree=ast.parse((ROOT/'DevelopmentTests/test_b239_commerce.py').read_text())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='fixture')
    setup=next(n.value.args[0].value for n in fn.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='execute' and n.value.args and isinstance(n.value.args[0],ast.Constant) and isinstance(n.value.args[0].value,str))
    l.execute(setup)
    l.execute("cities[2].present.BUILDING_SPC_COMMERCE_GOLD_0=true;cities[2].present.BUILDING_SPC_COMMERCE_GOLD_1=true;cities[2].present.BUILDING_SPC_COMMERCE_GOLD_2=true;cities[2].present.BUILDING_SPC_COMMERCE_GOLD_3=true")
    l.execute((ROOT/'Mod/Commerce.lua').read_text());l.execute('SPCCommerce.Start(P,shared);com=shared.Commerce;com.Audit()')
    return l


class NetworkProof(unittest.TestCase):
    def test_equal_proof_once_and_failed_capture_never_exposes_fresh_effects(self):
        l=commerce();l.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));local old=ownedGold(cities[2]);capitalFail=true;net.Refresh(0);assert(net.CurrentEffectPartners(0,cities[2]).validity=='UNKNOWN');cities[1].yields.SCIENCE=900;com.SourceChanged(0,1);assert(ownedGold(cities[2])==old);capitalFail=false;send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);assert(ownedGold(cities[2])==135)")
    def test_partial_facts_role_retained_and_transaction_remains_strict(self):
        l=culture();l.execute("cities[4].active=nil;net.Refresh(0);local p=net.Input(0);assert(p.factAvailability=='MIXED' and p.effectAvailability=='AVAILABLE');assert(p.provenance[4].status=='RETAINED');assert(net.CurrentDomesticPartners(0,cities[2]).validity=='UNKNOWN');assert(not pcall(net.CurrentCapitalSources,0,cities[1],'CULTURE'));assert(net.CurrentEffectPartners(0,cities[2]).validity=='VERIFIED');cities[4].active=4;fire('GovernorChanged',0);assert(net.Input(0).provenance[4].status=='CONFIRMED')")
    def test_first_unknown_role_freezes_carrier_projection(self):
        l=culture();l.execute("local c=cities[3];c.fail=true;net.Refresh(0);assert(net.Input(0).effectAvailability=='AVAILABLE');c.token='NEW';net.Refresh(0);assert(net.Input(0).effectAvailability~='AVAILABLE' and net.Input(0).provenance[3].status=='UNKNOWN')")
    def test_confirmed_route_loss_prunes_only_its_paths(self):
        l=culture();l.execute("cities[3].kind='CULTURE';cities[3].potential=4;cities[3].active=4;complete(4,1);complete(3,2);send('0,4,0,2,10;0,3,0,2,11;0,2,0,1,12',3);assert(amount(cities[1])==2);units[10]=nil;net.CheckEvidence(false);assert(amount(cities[1])==1 and net.Input(0).validity=='VERIFIED' and net.Input(0).continuityOnly);assert(net.CurrentDomesticPartners(0,cities[2]).validity=='UNKNOWN')")
    def test_known_center_loss_survives_other_fact_failure(self):
        l=culture();l.execute("complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1);cities[2].kind='NONE';cities[2].potential=0;cities[2].active=nil;net.Refresh(0);assert(amount(cities[1])==0)")
    def test_unknown_owner_is_not_negative_and_numeric_owner_loss_is(self):
        l=culture();l.execute("complete(4,1);cn.SourceChanged(0,4);local owner=cities[4].GetOwner;cities[4].GetOwner=function()return nil end;net.CheckEvidence(false);assert(amount(cities[1])==1 and net.Input(0).validity=='VERIFIED');cities[4].GetOwner=owner;cities[4].owner=3;net.CheckEvidence(false);assert(amount(cities[1])==0)")
    def test_negative_route_prune_keeps_unreadable_other_partner_contribution(self):
        l=commerce();l.execute("cities[5].kind='RESEARCH';cities[5].yields.SCIENCE=80;send('0,1,0,2,10;0,5,0,2,11',2);assert(toggle(2,'DISTRICT_CAMPUS',true));cities[5].GetProperty=function()error('TEMP_REFERENCE')end;units[10]=nil;net.CheckEvidence(false);assert(ownedGold(cities[2])==12)")
    def test_known_nontrader_and_foreign_unit_do_not_invalidate(self):
        l=culture();l.execute("P.RouteUnitRelevant=function(pid,id)return id~=999 end;local n=counts.city_scan;fire('UnitRemovedFromMap',0,999);fire('UnitRemovedFromMap',9,1);assert(counts.city_scan==n and net.Input(0).availability=='AVAILABLE')")


class CommerceRetention(unittest.TestCase):
    def test_pending_freezes_positive_changes_but_honors_capacity_and_active_loss(self):
        l=commerce();l.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));assert(toggle(2,'DISTRICT_THEATER',true));local n=created+removed;net.CheckEvidence(false);cities[1].yields.SCIENCE=900;com.SourceChanged(0,1);assert(ownedGold(cities[2])==23 and created+removed==n);cities[2].workers=1;com.SourceChanged(0,2);assert(ownedGold(cities[2])==15);cities[2].active=2;com.SourceChanged(0,2);assert(ownedGold(cities[2])==0)")
    def test_mixed_max_retained_loser_and_confirmed_zero_no_resurrection(self):
        l=commerce();l.execute("cities[5].kind='RESEARCH';cities[5].yields.SCIENCE=80;send('0,1,0,2,10;0,5,0,2,11',2);assert(toggle(2,'DISTRICT_CAMPUS',true));cities[5].yieldFail='SCIENCE';cities[1].kind='NONE';com.SourceChanged(0,1);assert(ownedGold(cities[2])==12 and view(2).stage=='RETAINED');assert(view(2).sourceProvenance.DISTRICT_CAMPUS[5].status=='RETAINED');assert(not toggle(2,'DISTRICT_CAMPUS',false));cities[5].kind='NONE';cities[5].yieldFail=nil;com.SourceChanged(0,5);assert(ownedGold(cities[2])==6);cities[5].kind='RESEARCH';cities[5].identityFail=true;com.SourceChanged(0,5);assert(ownedGold(cities[2])==6)")
    def test_cold_pending_installed_gold_kept_without_property_write(self):
        l=cold_commerce();l.execute("assert(ownedGold(cities[2])==15 and propertyWrites==0 and commerceWrites==0);assert(com.views['0:2'].stage=='HELD');local n=created+removed;for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(created+removed==n)")
    def test_unknown_source_or_receiver_reference_never_clears_applied_gold(self):
        l=commerce();l.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));local read=cities[1].GetProperty;cities[1].GetProperty=function()error('REFERENCE_UNAVAILABLE')end;com.SourceChanged(0,1);assert(ownedGold(cities[2])==15);cities[1].GetProperty=read;cities[2].fail=true;com.SourceChanged(0,2);assert(ownedGold(cities[2])==15 and view(2).stage=='HELD')")
    def test_pending_active_iv_to_iii_removes_reputation_bonus(self):
        l=commerce();l.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));commerceStates[2].reputation={version=1,start=0,cursor=20,age=20,receipt='P4',state='COUNTING'};cities[2].active=4;cities[2].potential=4;com.SourceChanged(0,2);assert(ownedGold(cities[2])==16);net.CheckEvidence(false);cities[2].active=3;com.SourceChanged(0,2);assert(ownedGold(cities[2])==15)")


class CultureRetention(unittest.TestCase):
    def test_mixed_union_and_equal_history_recovery(self):
        l=culture();l.execute("cities[3].kind='CULTURE';cities[3].potential=4;cities[3].active=4;complete(3,1);complete(4,2);send('0,4,0,2,10;0,3,0,2,11;0,2,0,1,12',3);assert(amount(cities[1])==2);cities[4].historyUnknown=true;complete(3,3);cn.SourceChanged(0,3);assert(amount(cities[1])==3);assert(cn.records['0:1'].provenance[4].status=='RETAINED');cities[4].historyUnknown=false;cn.SourceChanged(0,4);assert(cn.records['0:1'].provenance[4].status=='CONFIRMED')")
    def test_confirmed_source_loss_then_unknown_cannot_resurrect(self):
        l=culture();l.execute("complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1);net.CheckEvidence(false);cities[4].active=3;cn.SourceChanged(0,4);assert(amount(cities[1])==0);cities[4].active=nil;send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);assert(amount(cities[1])==0)")
    def test_unknown_source_reference_preserves_completed_civilizations(self):
        l=culture();l.execute("complete(4,1);cn.SourceChanged(0,4);local read=cities[4].GetProperty;cities[4].GetProperty=function()error('REFERENCE_UNAVAILABLE')end;cn.SourceChanged(0,4);assert(amount(cities[1])==1 and cn.records['0:1'].provenance[4].status=='RETAINED');cities[4].GetProperty=read;cn.SourceChanged(0,4);assert(amount(cities[1])==1)")
    def test_whole_hold_demotes_source_provenance(self):
        l=culture();l.execute("complete(4,1);cn.SourceChanged(0,4);net.CheckEvidence(false);cn.SourceChanged(0,4);assert(cn.records['0:1'].provenance[4].status=='RETAINED' and amount(cities[1])==1)")
    def test_cold_confirmed_topology_never_invents_unknown_source_history(self):
        l=culture(False);l.execute("cities[1].present.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0=true;cities[1].locations.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0=100;cities[4].historyUnknown=true;send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);assert(amount(cities[1])==0 and cn.records['0:1'].provenance[4].status=='UNKNOWN')")
    def test_cold_no_topology_preserves_installed_set(self):
        l=culture(False);l.execute("cities[1].present.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0=true;cities[1].locations.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0=100;fire('LoadScreenClose');assert(amount(cities[1])==1 and propertyWrites==0);local n=created+removed;for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(created+removed==n)")


class StandardizationRetention(unittest.TestCase):
    def test_actual_bridge_pending_freezes_self_and_network_combination(self):
        l=standard();l.execute("assert(stdValue(1)==14);local n=created+removed;net.CheckEvidence(false);studies[3]=2;std.SourceChanged(0,3);assert(stdValue(1)==14 and created+removed==n);assert(std.records['0:1'].retained)")
    def test_mixed_sources_take_max_and_confirmed_loss_keeps_other(self):
        l=standard();l.execute("knowledge[5]=false;studies[3]=2;std.SourceChanged(0,3);assert(stdValue(1)==14 and std.records['0:1'].sources[5].provenance=='RETAINED');cities[5].active=2;std.SourceChanged(0,5);assert(stdValue(1)==14);cities[3].active=3;std.SourceChanged(0,3);assert(stdValue(1)==10)")
    def test_unknown_source_reference_retains_previous_contribution(self):
        l=standard();l.execute("local read=cities[5].GetProperty;cities[5].GetProperty=function()error('REFERENCE_UNAVAILABLE')end;std.SourceChanged(0,5);assert(stdValue(1)==14 and std.records['0:1'].sources[5].provenance=='RETAINED');cities[5].GetProperty=read;std.SourceChanged(0,5);assert(stdValue(1)==14)")
    def test_pending_iv_to_iii_loses_only_confirmed_extra_share(self):
        l=standard();l.execute("net.CheckEvidence(false);cities[5].active=3;std.SourceChanged(0,5);assert(stdValue(1)==12);cities[3].active=3;std.SourceChanged(0,3);assert(stdValue(1)==10);assert(std.records['0:1'].sources[3].provenance=='RETAINED')")
    def test_pending_source_provenance_is_retained_and_unknown_owner_holds(self):
        l=standard();l.execute("net.CheckEvidence(false);std.SourceChanged(0,5);assert(std.records['0:1'].sources[5].provenance=='RETAINED');cities[5].GetOwner=function()return nil end;std.SourceChanged(0,5);assert(stdValue(1)==14)")
    def test_cold_exception_A_exact_hold_then_event_recompute(self):
        l=standard(False,True);l.execute("cities[3].active=2;knowledge[5]=false;send('0,5,0,2,10;0,3,0,2,11;0,2,0,1,12',3);assert(stdValue(1)==14 and std.records['0:1'].loaded and std.records['0:1'].retained);knowledge[5]={learned={},districts={learned={}}};std.SourceChanged(0,5);assert(stdValue(1)==0 and not std.records['0:1'].loaded and propertyWrites==0)")


class DevelopmentContainment(unittest.TestCase):
    def test_one_startup_city_failure_does_not_poison_index_or_existing_contract(self):
        import test_b246_development as module
        import test_store_write_boundaries as storage
        storage.LuaRuntime=TrackedLua51
        with legacy_source_observation():l=module.runtime()
        l.execute("assert(sign());local old=T.encode(value());local b=balance;local raw=P.HasBuilding;P.HasBuilding=function(bs,id)if bs==other.markers and tostring(id):find('BUILDING_SPC_DEVELOPMENT',1,true)then error('LOCAL_CARRIER_UNAVAILABLE')end;return raw(bs,id)end;reload();assert(active() and T.encode(value())==old and balance==b and moneyCalls==1);assert(dev.startupErrors['0:'..other:GetID()]);local n=effectWrites;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(effectWrites==n);P.HasBuilding=raw;dev.SourceChanged(0,other:GetID());Events.GameCoreEventPublishComplete.Fire();assert(not dev.startupErrors['0:'..other:GetID()] and active() and moneyCalls==1)")

    def test_pending_target_cannot_debit_and_failed_city_reads_do_not_poll(self):
        import test_b246_development as module
        import test_store_write_boundaries as storage
        storage.LuaRuntime=TrackedLua51
        with legacy_source_observation():l=module.runtime()
        l.execute("local raw=P.HasBuilding;local reads=0;P.HasBuilding=function(bs,id)if bs==research.markers and tostring(id):find('BUILDING_SPC_DEVELOPMENT',1,true)then reads=reads+1;error('TARGET_CARRIER_UNAVAILABLE')end;return raw(bs,id)end;reload();open();assert(not sign() and moneyCalls==0);local n=reads;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(reads==n);P.HasBuilding=raw;dev.SourceChanged(0,research:GetID());Events.GameCoreEventPublishComplete.Fire();open();assert(sign() and moneyCalls==1)")
    def test_partial_index_blocks_signing_then_real_commit_recovery_releases_it(self):
        import test_b246_development as module
        import test_store_write_boundaries as storage
        storage.LuaRuntime=TrackedLua51
        with legacy_source_observation():l=module.runtime()
        l.execute("local dc=shared.DistrictCompleteness;T.reload();C.service();shared.DistrictCompleteness=dc;local visit=shared.CityProgressionStore.VisitDevelopment;local failed=true;shared.CityProgressionStore.VisitDevelopment=function(pid,fn)visit(pid,fn);if failed then error('DEVELOPMENT_PARTIAL_INDEX')end end;setupDevelopment();open();assert(not view().canSign and not sign() and moneyCalls==0);failed=false;dev.SourceChanged(0,source:GetID());Events.GameCoreEventPublishComplete.Fire();open();assert(view().canSign and sign() and moneyCalls==1)")

if __name__=='__main__':unittest.main()
