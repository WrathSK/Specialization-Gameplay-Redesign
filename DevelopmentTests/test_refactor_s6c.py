"""S6c narrow anchor state/geometry sharing; independent policies, Lua51."""
import unittest
from refactor_harness import Context, legacy_source_observation, measure
from test_refactor_s5b import store
from test_refactor_s5d4c2 import active
from test_refactor_s4a import industry, load_industry_ui


def anchor():
    l=store();l.globals().include('RuntimeWork');l.globals().include('SpecialistSupport')
    l.execute("""
    P.Families={DISTRICT_CAMPUS='RESEARCH'};P.Family=function(t)return P.Families[t]end
    raw={id=T.snapshot(c).base.first.districtID,type=T.snapshot(c).base.first.type,complete=true,pillaged=false,owner=0,city=c:GetID(),x=101,y=0}
    nativeReads=0;geometryReads=0
    d={GetID=function()return raw.id end,GetType=function()return 1 end,
     GetCity=function()return {GetOwner=function()return raw.owner end,GetID=function()return raw.city end}end,
     IsComplete=function()nativeReads=nativeReads+1;if stateError then error('STATE_FAILED')end;return raw.complete end,
     IsPillaged=function()return raw.pillaged end,
     GetX=function()geometryReads=geometryReads+1;if geometryError then error('GEOMETRY_FAILED')end;return raw.x end,GetY=function()return raw.y end}
    local info=P.Info;P.Info=function(t,k)if t=='Districts'then return {DistrictType=raw.type,Index=1}end;return info(t,k)end
    c.GetDistricts=function()return {GetNumDistricts=function()if enumerateError then error('ENUMERATION_FAILED')end;return missing and 0 or 1 end,GetDistrictByIndex=function()return d end}end
    Players[0].GetDistricts=function()error('OWNER_ENUMERATION_FORBIDDEN')end
    function readAnchor()return SPCSpecialistSupport.Anchor(P,shared,0,c,SPCRuntimeWork.New(P,shared))end
    function readGeometry()return SPCSpecialistSupport.Inspect(P,shared,0,c,SPCRuntimeWork.New(P,shared),function(k,r,f,w,g)assert(k=='RESEARCH');return g()end)end
    """);return l


def actual_supports():
    l=active()
    with legacy_source_observation():l.globals().include('ResearchSupport')
    l.execute("""
    local info=P.Info;local extra={};local serial=100000
    P.Info=function(t,k)
     local row=info(t,k);if row then return row end
     if t=='Buildings'and type(k)=='string'and(k:find('_SUPPORT')or k:find('BUILDING_SPC_DEV_LV3_'))then
      if not extra[k]then serial=serial+1;extra[k]={Index=serial,BuildingType=k};extra[serial]=extra[k]end;return extra[k]
     end
     return t=='Buildings'and extra[k]or nil
    end
    SPCResearchSupport.Start(P,shared);shared.ResearchSupport.ready=true;shared.ResearchSupport.Audit({player=0,city=1})
    -- Native authority double only; retain the actual EF investment overlay,
    -- original foundation fixture, DC, three writers and native carrier protocol.
    shared.CityProgressionStore={Owns=function()return false end,FactStamp=function(pid,city)return city.token end}
    f=shared.EffectiveFacts
    function audits()
     for _,name in ipairs({'ResearchSupport','Lv2Housing','Lv2GPP'})do shared[name].Audit({player=0,city=1});assert(not shared[name].errors['0:1'],shared[name].errors['0:1'])end
    end
    audits();svc.ReadFacts(0,c,c.token);states=0;indexed=0
    local complete=d.IsComplete;d.IsComplete=function(...)states=states+1;return complete(...)end
    local districts=c.GetDistricts;c.GetDistricts=function(...)indexed=indexed+1;return districts(...)end
    Players[0].GetDistricts=function()error('OWNER_ENUMERATION_FORBIDDEN')end
    """);return l


class AnchorPolicy(unittest.TestCase):
    def test_reuses_state_only_in_one_phase_and_returns_detached_dto(self):
        l=anchor();l.execute("f.WithPhase('SHARED',function()local k,r=readAnchor();assert(k=='RESEARCH'and r.complete);r.complete=false;local k,r=readAnchor();assert(k=='RESEARCH'and r.complete and nativeReads==1 and geometryReads==0)end);readAnchor();readAnchor();assert(nativeReads==3)")
    def test_confirmed_owner_and_type_mismatch_win_before_state_unknown(self):
        for change in ('raw.owner=1','raw.city=999','raw.type="DISTRICT_THEATER"'):
            l=anchor();l.execute(change+";stateError=true;geometryError=true;assert(readAnchor()==nil and nativeReads==0 and geometryReads==0)")
    def test_incomplete_or_pillaged_wins_before_active_unknown(self):
        for change in ('raw.complete=false','raw.pillaged=true'):
            l=anchor();l.execute("T.invest(c,8301);P.GovernorGate=function()return 0,c:GetID(),'UNKNOWN' end;"+change+";assert(readAnchor()==nil and geometryReads==0)")
    def test_missing_state_unknown_and_related_recovery(self):
        l=anchor();l.execute("f.WithPhase('STATE',function()raw.pillaged=nil;assert(not pcall(readAnchor));raw.pillaged=false;assert(readAnchor()=='RESEARCH');missing=true;shared.FactChanges.InvalidateCommitted(0,c:GetID(),{'D'});assert(readAnchor()==nil);missing=false;shared.FactChanges.InvalidateCommitted(0,c:GetID(),{'D'});assert(readAnchor()=='RESEARCH')end)")
    def test_geometry_unknown_does_not_poison_state_and_exception_releases(self):
        l=anchor();l.execute("f.WithPhase('GEOMETRY',function()geometryError=true;assert(not pcall(readGeometry));assert(readAnchor()=='RESEARCH'and nativeReads==1);geometryError=false;assert(readGeometry().x==101);readGeometry();assert(geometryReads==2)end)")
    def test_second_city_owner_change_and_registry_replacement_refresh(self):
        l=anchor();l.execute("f.WithPhase('VERSIONS',function()readAnchor();shared.FactChanges.InvalidateCommitted(0,c:GetID(),{'D'});readAnchor();shared.FactChanges.InvalidateCommitted(0,nil,{'D'});readAnchor();SPCFactChanges.New(shared);readAnchor();assert(nativeReads==4)end)")
    def test_actual_write_and_anchor_change_during_getter_never_certify_old(self):
        l=anchor();l.execute("local get=d.IsComplete;local once=true;d.IsComplete=function()if once then once=false;local t=f.BeginWrite();f.EndWrite(t)end;return get()end;f.WithPhase('WRITE',function()assert(not pcall(readAnchor));assert(readAnchor()=='RESEARCH'and nativeReads==2)end)")
    def test_geometry_reentry_is_bounded_and_recovers(self):
        l=anchor();l.execute("local get=d.GetX;local once=true;d.GetX=function()if once then once=false;local ok,why=pcall(readGeometry);assert(not ok and why:find('ANCHOR_CAPTURE_IN_PROGRESS'))end;return get()end;f.WithPhase('REENTRY',function()readAnchor();assert(readGeometry().x==101);assert(readGeometry().x==101 and geometryReads==1)end)")
    def test_batch_projection_works_outside_phase_and_private_reader_expires(self):
        l=anchor();l.execute("local b=SPCRuntimeWork.New(P,shared);local captured;local k=b.Inspect(0,c,function(v,w,a)captured=a;return v.specialization end);assert(k=='RESEARCH');assert(not pcall(captured,{districtID=1,type='DISTRICT_CAMPUS'},function()return {present=false}end));assert(readAnchor()=='RESEARCH')")
    def test_reference_and_owner_cannot_reuse_raw_sample(self):
        l=anchor();l.execute("f.WithPhase('REF',function()readAnchor();local token=c.s.values.TOKEN;c.s.values.TOKEN='BAD';assert(not pcall(readAnchor));c.s.values.TOKEN=token;assert(readAnchor()=='RESEARCH'and nativeReads==2);c.s.ref.owner=1;assert(readAnchor()==nil and nativeReads==2)end)")
    def test_payload_must_be_scalar_and_expired_reader_cannot_be_retained(self):
        l=anchor();l.execute("f.WithPhase('BOUND',function()local captured;f.Inspect(0,c,function(v,w,a)captured=a;assert(not pcall(a,v.first,function()return {present=false,object={}}end))end);assert(not pcall(captured,{districtID=1,type='DISTRICT_CAMPUS'},function()return {present=false}end))end)")
    def test_anchor_capacity_and_uncached_overflow_keep_warm_set(self):
        from test_refactor_s5b import synthetic
        c=synthetic();c.load('FactChanges');c.execute("SPCFactChanges.New(shared);samples=0;function get(city)return f.Inspect(0,city,function(v,w,a)return a({districtID=11,type='DISTRICT_CAMPUS'},function()samples=samples+1;return {present=false}end)end)end;f.WithPhase('LIMIT',function()for i=1,2049 do get(cities[i]or add(i))end;assert(samples==2049);get(cities[1]);assert(samples==2049);get(cities[2049]);assert(samples==2050)end)")


class Consumers(unittest.TestCase):
    def test_actual_three_writers_preserve_carriers_and_share_state(self):
        values=[]
        for combined in (False,True):
            l=actual_supports();l.globals().combined=combined
            l.execute("states=0;indexed=0;local w=writes;if combined then f.WithPhase('WRITERS',audits)else audits()end;assert(writes==w and housing(c)==1 and gpp(c,'RESEARCH')==6);result={};for k,v in pairs(c.carriers)do if v then result[k]=true end end")
            values.append((l.eval('states'),l.eval('indexed'),dict(l.globals().result)))
        self.assertEqual(values[0][:2],(3,4));self.assertEqual(values[1][:2],(1,2));self.assertEqual(values[0][2],values[1][2])
        measure('S6c_actual_support_housing_GPP',{'independent_state_samples':3,'shared_state_samples':1,'independent_city_index_reads':4,'shared_city_index_reads':2,'owner_district_enumerations':0,'writes':0,'same_carriers':True,'geometry':'one separate city-local lookup included; full D census not used for anchor','foundation':'actual EF overlay plus explicit foundation/Store-stamp doubles'})
    def test_bad_geometry_isolated_to_GPP_and_known_owner_loss_withdraws(self):
        l=actual_supports();l.execute("local gx=d.GetX;d.GetX=function()error('GEOMETRY_UNKNOWN')end;local w=writes;shared.ResearchSupport.Audit({player=0,city=1});shared.Lv2Housing.Audit({player=0,city=1});shared.Lv2GPP.Audit({player=0,city=1});assert(not shared.ResearchSupport.errors['0:1']and not shared.Lv2Housing.errors['0:1']and shared.Lv2GPP.errors['0:1']and writes==w);d.GetX=gx;local owner=d.GetCity;d.GetCity=function()return {GetOwner=function()return 1 end,GetID=function()return 999 end}end;d.IsComplete=function()error('UNNEEDED_STATE')end;audits();assert(housing(c)==0 and gpp(c,'RESEARCH')==0)")
    def test_GPP_shared_worker_still_enforces_own_limit_and_fresh_no_index_compatibility(self):
        l=actual_supports();l.execute("d.workers=256;local w=writes;f.WithPhase('LIMIT',function()f.Inspect(0,c,function(v,r)assert(r({id=d.id,type='DISTRICT_CAMPUS',plot=d.plot},function()return 256 end)==256)end);shared.Lv2GPP.Audit({player=0,city=1})end);assert(writes==w and shared.Lv2GPP.errors['0:1']);d.workers=3;local plot=Map.GetPlot;Map.GetPlot=function(x,y)local p=plot(x,y);return {GetWorkerCount=function()return p:GetWorkerCount()end}end;shared.Lv2GPP.Audit({player=0,city=1});assert(gpp(c,'RESEARCH')==6 and not shared.Lv2GPP.errors['0:1'])")
    def test_actual_industry_reference_bytes_unchanged_and_outside_phase_audit(self):
        l=industry();load_industry_ui(l);l.execute("local c=cities[2];local nd=districts[12];local kind,raw=SPCSpecialistSupport.Anchor(P,shared,0,c,SPCRuntimeWork.New(P,shared));assert(kind=='INDUSTRY');assert(SPCSampleLifecycle.AnchorReference(c,raw,{x=nd:GetX(),y=nd:GetY()})==SPCSampleLifecycle.Reference(c,nd,P.Info('Districts',nd:GetType())));assert(d.ReadBase(0,c)==6);local w=writes;d.Audit({player=0,city=2});assert(writes==w and not d.errors['0:2'])")

if __name__=='__main__':unittest.main()
