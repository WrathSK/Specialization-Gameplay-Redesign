"""B413 narrow review regressions. Native dispatch models are not engine proof."""
import unittest
from refactor_harness import legacy_source_observation,measure
from test_b412_crew_observation import pure,actual

def owner_views(c):
    c.execute("""local views={};ExposedMembers.SPC_P0.CrewProjects.views=views
    for id=1,2 do views['0:'..id]={owner=0,city=id,reserved=1,queued=1,paused=0,retained={[project]={stage='QUEUED'}}}end
    """)
    return c

class ProbeBudget(unittest.TestCase):
    def test_unrelated_local_production_does_not_spend_completion_visits(self):
        c=owner_views(pure());c.execute("""
        cityMap[3]={GetOwner=function()reads=reads+1;return 0 end,GetProperty=function()reads=reads+1;return nil end}
        local n=reads
        for i=1,1000 do Events.CityProductionChanged.Fire(0,3);Events.CityProductionCompleted.Fire(0,3,999);publish()end
        assert(reads==n and probe.Stats().visits==0 and probe.Stats().live,'LOCAL_ORDINARY_EXHAUSTED_COMPLETION_BUDGET')
        fire(0,1,projectIndex);assert(#proofRows('CREW_PROOF_EVENT')==1 and probe.Stats().samples==1)
        """)
    def test_long_build_keeps_completion_window_and_budget_after_bounded_prelude(self):
        c=owner_views(pure());c.execute("""
        Events.CityProductionChanged.Fire(0,1);publish()
        for t=11,80 do turn=t;Events.CityProductionChanged.Fire(0,1);publish()end
        assert(probe.Stats().live,'BUILD_DURATION_EXPIRED_COMPLETION_WINDOW')
        local n=reads
        for i=1,1000 do Events.CityProductionChanged.Fire(0,1);publish()end
        assert(reads==n,'PRELUDE_CONTINUES_NATIVE_SAMPLING')
        local before=#proofRows('CREW_PROOF_EVENT');fire(0,1,projectIndex)
        assert(probe.Stats().live and #proofRows('CREW_PROOF_EVENT')==before+1,'COMPLETION_EVIDENCE_LOST')
        local status=proofRows('CREW_PROOF_STATUS');local cut=false
        for _,v in ipairs(status)do if v.point=='PRELUDE_LIMIT'then cut=v.eventTruncated=='true'end end;assert(cut)
        turn=85;fire(0,2,projectIndex);assert(probe.Stats().live)
        turn=86;fire(0,2,projectIndex);assert(not probe.Stats().live)
        local stopped=reads;for i=1,1000 do fire(0,1,projectIndex);publish()end;assert(reads==stopped)
        """)
    def test_known_related_unverified_arguments_remain_raw_observations(self):
        c=owner_views(pure());c.execute("""
        Events.CityProductionCompleted.Fire(0,1,nil,false,999)
        fire(0,1,999999,nil,false)
        local a=proofRows('CREW_PROOF_EVENT');assert(#a==2 and a[1].eventCount=='5'and a[2].projectType==nil)
        assert(a[1].eventBatch:find('4:boolean:false',1,true)and a[2].eventBatch:find('999999',1,true))
        turn=40;fire(0,1,projectIndex);assert(probe.Stats().live,'UNVERIFIED_EVENT_ARMED_COMPLETION_WINDOW')
        """)
    def test_stop_keeps_fixed_listeners_and_does_not_call_remove(self):
        c=pure();c.execute("""
        removes=0;for _,name in ipairs({'CityProjectCompleted','CityProductionChanged','CityProductionCompleted','GameCoreEventPublishComplete'})do
         Events[name].Remove=function()removes=removes+1;error('REMOVE_FORBIDDEN')end
        end
        probe.After();local count=probe.Stats().hooks;SPCCrewCompletionDiagnostics.Stop()
        assert(removes==0 and probe.Stats().hooks==count,'STOP_MUTATED_LISTENER_LIST')
        local n=reads;for i=1,1000 do fire(0,1,projectIndex);publish()end;assert(reads==n)
        probe.After();assert(probe.Stats().hooks==count)
        """)
    def test_stop_inside_snapshot_does_not_repopulate_pending(self):
        c=owner_views(pure('UI'));c.execute("SPCCrewCompletionDiagnostics.SAMPLE_LIMIT=0;fire(0,1,projectIndex);assert(not probe.Stats().live and not probe.Stats().pending);local n=reads;publish();assert(reads==n)")


class DispatchIsolation(unittest.TestCase):
    def test_stopping_before_owner_preserves_units_orders_receipts_in_all_dispatch_models(self):
        for dispatch in ('snapshot','tombstone','shifting'):
            states=[]
            for mode in ('on','off','absent'):
                with legacy_source_observation():v=actual(mode,dispatch)
                v.execute("""
                p=C.begin(c);C.begin(other)
                if SPCCrewCompletionDiagnostics and SPCCrewCompletionDiagnostics.ENABLED then SPCCrewCompletionDiagnostics.EVENT_LIMIT=0 end
                C.complete(c,p);C.complete(other,p)
                assert(C.calls==2,'STOP_SKIPPED_REAL_CREW_CALLBACK_'..dispatch)
                assert(removes==0,'OBSERVER_REMOVED_DURING_DISPATCH')
                snapshot=state();Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index)
                assert(state()==snapshot and C.calls==2)
                """)
                states.append((v.eval('snapshot'),list(v.globals().mutationLog.values())))
            self.assertEqual(states[0],states[1],dispatch);self.assertEqual(states[0],states[2],dispatch)
        measure('B413_stop_dispatch',{'dispatch_models':3,'mode_equivalence':['on','off','absent'],'actual_units_per_case':2,'removes':0,'native_dispatch_model':'UNKNOWN'})

    def test_shifting_stop_before_owner_does_not_skip_real_grant(self):
        with legacy_source_observation():v=actual('on','shifting')
        v.execute("p=C.begin(c);C.begin(other);SPCCrewCompletionDiagnostics.EVENT_LIMIT=0;C.complete(c,p);C.complete(other,p);assert(C.calls==2,'SHIFTING_STOP_SKIPPED_REAL_CREW_CALLBACK');assert(removes==0)")


def commerce():
    from test_refactor_s6f import combined
    with legacy_source_observation():v=combined()
    # Replace the old D double with the actual capture/catalogue/cache service.
    # Engine buildings/districts/Map remain explicit city-local native controls.
    with legacy_source_observation():
        v.globals().include('OrdinaryBuildingCatalog');v.globals().include('DistrictCompleteness')
    v.execute("""
    GameInfo.Buildings=tableInfo({
     {BuildingType='BUILDING_LIBRARY',Index=2001,PrereqDistrict='DISTRICT_CAMPUS',Tier=1},
     {BuildingType='BUILDING_UNIVERSITY',Index=2002,PrereqDistrict='DISTRICT_CAMPUS',Tier=2}},'BuildingType')
    GameInfo.HD_BuildingTiers=GameInfo.Buildings
    GameInfo.BuildingReplaces=tableInfo({},'CivUniqueBuildingType')
    local info=P.Info;P.Info=function(t,k)return GameInfo[t]and GameInfo[t][k]or info(t,k)end
    local first=shared.EffectiveFacts.Read(0,source).first
    GameInfo.Districts=tableInfo({{DistrictType='DISTRICT_COMMERCIAL_HUB',Index=81},{DistrictType='DISTRICT_CAMPUS',Index=82}},'DistrictType')
    raw={complete=true,pillaged=false,workers=2};anchorReads=0
    local function district(id,index,x)
     return {GetID=function()return id end,GetType=function()return index end,
      GetX=function()return x end,GetY=function()return 0 end,
      IsComplete=function()if index==81 then anchorReads=anchorReads+1;if anchorError then error('ANCHOR_UNKNOWN')end;return raw.complete end;return true end,
      IsPillaged=function()return index==81 and raw.pillaged or false end}
    end
    local a=district(first.districtID,81,501);local b=district(first.districtID+1,82,502)
    source.GetDistricts=function()return {GetNumDistricts=function()return 2 end,GetDistrictByIndex=function(_,i)return i==0 and a or b end}end
    source.markers[2001]=true;source.markers[2002]=true
    source.markers.HasBuilding=function(self,k)return self[k]==true end
    source.markers.IsPillaged=function()return false end
    source.markers.GetBuildingLocation=function(_,k)return 502 end
    source.markers.CurrentlyBuilding=function()return nil end
    Map.GetPlot=function(x,y)return {GetIndex=function()return x end}end
    Map.GetPlotByIndex=function(index)return {GetWorkerCount=function()
     assert(index==501);workerReads=workerReads+1
     if onWorkers then onWorkers()end;if workerFailure then error('WORKERS_UNKNOWN')end;return raw.workers
    end}end
    SPCDistrictCompleteness.Start(P,shared);dc=shared.DistrictCompleteness
    function change()dc.MarkDirty(0,source:GetID());f.Invalidate()end
    function audit()com.Audit({player=0,city=source:GetID()});return com.views['0:'..source:GetID()]end
    assert(audit().stage=='READY'and gold()==15,'REAL_DC_SETUP')
    local governor=P.GovernorGate
    P.GovernorGate=function(c)if governorUnknown and c:GetID()==source:GetID()then return 0,c:GetID(),'UNKNOWN'end;return governor(c)end
    function unknown()governorUnknown=true;change()end
    """)
    return v

class CommerceNegatives(unittest.TestCase):
    def test_unknown_governor_cannot_hide_confirmed_anchor_pillage(self):
        v=commerce();v.execute("unknown();raw.pillaged=true;local saved=T.encode(T.record(source));local out=audit();assert(gold()==0,'CONFIRMED_PILLAGE_RETAINED_GOLD');assert(out.stage=='INELIGIBLE'and not out.canConfigure and not com.TransactionCurrent(0,source:GetID()));assert(T.encode(T.record(source))==saved)")
    def test_unknown_governor_cannot_hide_confirmed_zero_workers(self):
        v=commerce();v.execute("unknown();raw.workers=0;local out=audit();assert(gold()==0,'CONFIRMED_ZERO_WORKERS_RETAINED_GOLD');assert(out.workers==0 and out.stage=='INELIGIBLE'and not out.canConfigure)")
    def test_unknown_anchor_workers_and_identity_hold_without_inventing_zero(self):
        for fault in ('anchorError=true','workerFailure=true',"raw.workers=nil","source.s.values.TOKEN='WRONG_REFERENCE'"):
            v=commerce();v.execute("unknown();"+fault+";local out=audit();assert(gold()==15 and out.stage=='HELD'and not out.canConfigure,'UNKNOWN_BECAME_ZERO')")
    def test_same_turn_repair_waits_for_reliable_governor_then_restores(self):
        v=commerce();v.execute("unknown();raw.pillaged=true;audit();assert(gold()==0);raw.pillaged=false;change();assert(audit().stage=='HELD'and gold()==0);governorUnknown=false;change();assert(audit().stage=='READY'and gold()==15)")
    def test_native_mutation_during_zero_sample_does_not_commit_stale_zero(self):
        v=commerce();v.execute("unknown();raw.workers=0;local once=true;onWorkers=function()if once then once=false;local t=f.BeginWrite();f.EndWrite(t)end end;local out=audit();assert(out.stage=='HELD'and gold()==15,'STALE_ZERO_COMMITTED')")
    def test_unrelated_city_and_idle_publication_remain_untouched(self):
        v=commerce();v.execute("local otherBefore=T.encode(T.record(other));unknown();raw.workers=0;audit();local n=effectWrites;local r=workerReads;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(effectWrites==n and workerReads==r and T.encode(T.record(other))==otherBefore and gold()==0)")

if __name__=='__main__':unittest.main()
