"""S6i actual Store/Investment/UnitActions and Crew/targets with native site doubles."""
import unittest
from refactor_harness import TrackedLua51, legacy_source_observation, measure
import test_store_write_boundaries as stores
import test_b236_crews as crews
from test_refactor_s6h import ActualProfile


def actual_store():
    old=stores.LuaRuntime;stores.LuaRuntime=TrackedLua51
    try:
        with legacy_source_observation():l=stores.fixture()
    finally:stores.LuaRuntime=old
    return l


def investment(n=8):
    l=actual_store();l.execute("source,other=T.two();siteCities={source,other};siteRows={};for i=3,"+str(n)+" do local c=T.fresh(i);T.register(c);T.complete(c,'DISTRICT_CAMPUS');siteCities[#siteCities+1]=c end")
    l.execute(r'''
      for _,d in Players[0]:GetDistricts():Members()do
       local c=d:GetCity();d.GetX=function()return c:GetX()+1 end;d.GetY=function()return c:GetY()end
       siteRows[c:GetID()]=siteRows[c:GetID()]or {};table.insert(siteRows[c:GetID()],d)
      end
      for _,c in ipairs(siteCities)do
       local rows=siteRows[c:GetID()]
       c.GetDistricts=function()return {GetNumDistricts=function()if districtFailure then error('DISTRICT_READ_UNKNOWN')end;return #rows end,GetDistrictByIndex=function(_,i)if missingDistrict then return nil end;return rows[i+1]end}end
       c.GetName=function()return 'SITE '..c:GetID()end
      end
      siteWork={ownerDistricts=0,ownerCities=0,localDistricts=0,cities=0}
      local pd=Players[0].GetDistricts;local pc=Players[0].GetCities
      Players[0].GetDistricts=function()siteWork.ownerDistricts=siteWork.ownerDistricts+1;if forbidOwner then error('OWNER_DISTRICTS_FORBIDDEN')end;return pd()end
      Players[0].GetCities=function()local cs=pc();return {FindID=cs.FindID,GetCapitalCity=cs.GetCapitalCity,Members=function()siteWork.ownerCities=siteWork.ownerCities+1;if forbidOwner then error('OWNER_CITIES_FORBIDDEN')end;return cs:Members()end}end
      P.Count=function(k)if k=='district_scan'then siteWork.localDistricts=siteWork.localDistricts+1 elseif k=='city_scan'then siteWork.cities=siteWork.cities+1 end end
      local info=P.Info
      P.Info=function(tab,id)if tab=='Units'then return GameInfo.Units[id]end;return info(tab,id)end
      P.CrewBase=function()return nil end
      function addSiteUnit(id)
       addunit(id,source);local u=Players[0]:GetUnits():FindID(id)
       u.x=source:GetX()+1;u.y=source:GetY();u.GetID=function()return id end
       u.GetX=function()return u.x end;u.GetY=function()return u.y end;return u
      end
      Map.GetPlot=function(x,y)return {x=x,y=y,GetIndex=function()return x*1000+y end,GetOwner=function()return 0 end}end
      function resetWork()for k in pairs(siteWork)do siteWork[k]=0 end end
      function makePreview(id)
       local u=addSiteUnit(id);local out=shared.UnitActions.Run(0,{Action='UNIT_ACTION_PREPARE',UnitID=id,Token='SITE:'..id})
       assert(out:find('PREPARED'),out);return u,shared.UnitActionPreview.token
      end
      function confirm(id,token)return shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=id,PlanToken=token,Token='CONFIRM:'..id})end
    ''')
    with legacy_source_observation():
        l.globals().include('UnitTargets');l.globals().include('UnitActions')
    l.execute("SPCUnitTargets.Start(P,shared);SPCUnitActions.Start(P,shared);shared.UnitTargetSnapshot={token='MARKER_KEEP'};resetWork()")
    return l


def crew_site(n=8):
    old=stores.LuaRuntime;stores.LuaRuntime=TrackedLua51
    try:
        with legacy_source_observation():l=crews.Consumption().fixture()
    finally:stores.LuaRuntime=old
    l.execute("c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);siteCities={c};for i=2,"+str(n)+" do local q=H.city(i);C.queue(q);q:GetBuildQueue().CurrentlyBuilding=function()return 'UNIT_WARRIOR'end;siteCities[#siteCities+1]=q end")
    l.execute(r'''
      C.rows.Districts=C.rows.Districts or {};C.rows.Districts.DISTRICT_WONDER={Index=999}
      for _,city in ipairs(siteCities)do
       local rows={};for _,d in pairs(H.native)do if d:GetCity()==city then rows[#rows+1]=d end end
       city.GetDistricts=function()return {GetNumDistricts=function()return #rows end,GetDistrictByIndex=function(_,i)return rows[i+1]end}end
       city.GetName=function()return 'Crew site'end
      end
      local queue=c:GetBuildQueue();queue.CurrentlyBuilding=function()if queueMutates then return queueMutates()end;return queue.target end
      unit=C.units[20001];unit.x=500;unit.y=0
      plots={};function plot(id)
       local p={id=id,owner=0,mark=P.Info('Buildings','BUILDING_WONDER_2').Index}
       function p:GetOwner()return self.owner end;function p:GetIndex()return self.id end;function p:GetDistrictType()return 999 end
       function p:GetProperty()return self.mark end;return p
      end
      plots[500]=plot(500);plots[501]=plot(501)
      Map={GetPlot=function(x,y)return plots[x]end,GetPlotByIndex=function(id)return plots[id]end}
      -- Placed construction uses purchase city, completed districts use DistrictAt.
      CityManager.GetDistrictAt=function()if locatorFailure then error('LOCATOR_UNKNOWN')end;return nil end
      Cities={GetPlotPurchaseCity=function(p)return purchaseCity or c end}
      ExposedMembers.DLHD={Utils={GetCityPlots=function(pid,id)return hdPlots or {500,500}end}}
      siteWork={ownerDistricts=0,ownerCities=0,localDistricts=0,cities=0}
      local pd=Players[0].GetDistricts;local pc=Players[0].GetCities
      Players[0].GetDistricts=function()siteWork.ownerDistricts=siteWork.ownerDistricts+1;if forbidOwner then error('OWNER_DISTRICTS_FORBIDDEN')end;return pd()end
      Players[0].GetCities=function()local cs=pc();return {FindID=cs.FindID,GetCapitalCity=cs.GetCapitalCity,Members=function()siteWork.ownerCities=siteWork.ownerCities+1;if forbidOwner then error('OWNER_CITIES_FORBIDDEN')end;return cs:Members()end}end
      P.Count=function(k)if k=='district_scan'then siteWork.localDistricts=siteWork.localDistricts+1 elseif k=='city_scan'then siteWork.cities=siteWork.cities+1 end end
      function resetWork()for k in pairs(siteWork)do siteWork[k]=0 end end
    ''')
    with legacy_source_observation():l.globals().include('UnitTargets')
    l.execute("SPCUnitTargets.Start(P,shared);shared.UnitTargetSnapshot={token='MARKER_KEEP'};resetWork()")
    return l


class InvestmentSites(unittest.TestCase):
    def test_known_city_and_actual_action_path_have_no_owner_wide_reads(self):
        results=[]
        for n in (8,32,64):
            l=investment(n);l.execute("forbidOwner=true;local u,t=makePreview(900);local view=shared.UnitActions.ReadView(0,900,'VIEW');assert(view.legal and view.prepared);assert(confirm(900,t):find('INVESTED'));assert(shared.EffectiveFacts.Read(0,source).potential==2 and not Players[0]:GetUnits():FindID(900));assert(siteWork.ownerDistricts==0 and siteWork.ownerCities==0 and shared.UnitTargetSnapshot.token=='MARKER_KEEP')")
            results.append({k:l.globals().siteWork[k]for k in ('ownerDistricts','ownerCities','localDistricts','cities')})
        self.assertEqual(results[0],results[1]);self.assertEqual(results[1],results[2])
        measure('S6i_investment_current_site',{'cities':[8,32,64],'work':results,'actual_Store':True,'same_potential':2,'single_unit_consumed':True})

    def test_full_marker_discovery_still_lists_other_cities_when_unit_elsewhere(self):
        l=investment(32);l.execute("local u=addSiteUnit(901);u.x=199;shared.UnitTargets.Refresh(0,{UnitID=901,Token='ALL'});assert(not shared.UnitTargetSnapshot.error and #shared.UnitTargetSnapshot.plots==32 and siteWork.ownerDistricts==1 and siteWork.ownerCities==1)")

    def test_full_cap_tooltip_does_not_depend_on_current_target_list(self):
        l=investment();l.execute("for i=1,3 do T.invest(source,910+i)end;addSiteUnit(914);forbidOwner=true;local v=shared.UnitActions.ReadView(0,914,'CAP');assert(not v.legal and v.potential==4 and v.reason:find('POTENTIAL_CAP_4'))")

    def test_known_city_does_not_add_governor_pillage_or_purchase_city_requirement(self):
        l=investment();l.execute("T.governor(1);local d=siteRows[source:GetID()][1];d.IsPillaged=function()error('NO_NEW_PILLAGE_POLICY')end;Cities={GetPlotPurchaseCity=function()error('NO_NEW_PURCHASE_POLICY')end};forbidOwner=true;local u,t=makePreview(915);assert(confirm(915,t):find('INVESTED'))")

    def test_bad_first_type_id_completion_or_position_rejects_without_consumption(self):
        for mutation in ("local d=siteRows[source:GetID()][1];d.GetID=function()return 999 end", "local d=siteRows[source:GetID()][1];d.GetType=function()return 'DISTRICT_THEATER'end", "siteRows[source:GetID()][1].IsComplete=function()return false end",'u.x=u.x+1'):
            l=investment();l.execute("local u,t=makePreview(916);"+mutation+";local before=T.writes();local out=confirm(916,t);assert(out:find('REJECTED')and Players[0]:GetUnits():FindID(916)and T.writes()==before)")

    def test_known_city_native_failure_is_not_empty_success_or_global_fallback(self):
        l=investment();l.execute("addSiteUnit(917);forbidOwner=true;districtFailure=true;local v=shared.InvestmentAction.ReadView(0,source,917);assert(not v.legal and v.reason:find('DISTRICT_READ_UNKNOWN')and siteWork.ownerDistricts==0);districtFailure=false;assert(shared.InvestmentAction.ReadView(0,source,917).legal)")

    def test_intent_write_then_move_keeps_second_fresh_site_guard_and_no_replay(self):
        l=investment();l.execute("""
          local u,t=makePreview(918);local setter=Game.SetProperty;local once=true
          Game.SetProperty=function(o,k,v)
           setter(o,k,v)
           if once and k==T.key(source)and T.record(source).investment and T.record(source).investment.pending then once=false;u.x=u.x+1 end
          end
          local inner=shared.InvestmentAction.Confirm;local message,evidence
          shared.InvestmentAction.Confirm=function(...)message,evidence=inner(...);return message,evidence end
          confirm(918,t)
          assert(not once and message:find('HELD')and evidence.status=='UNKNOWN')
          local saved=T.record(source).investment
          assert(saved.pending.stage=='INTENT'and next(saved.investments)==nil)
          assert(Players[0]:GetUnits():FindID(918)and u:GetProperty('SPC_DEV_INVESTMENT_UNIT')==nil)
          local n=T.writes();confirm(918,t);assert(T.writes()==n and Players[0]:GetUnits():FindID(918))
        """)

    def test_locator_throw_falls_back_without_cancelling_prepared_or_cap_view(self):
        l=investment();l.execute("local u,t=makePreview(920);CityManager.GetDistrictAt=function()error('HINT_UNKNOWN')end;local v=shared.UnitActions.ReadView(0,920,'PREPARED');assert(v.legal and v.prepared and v.planToken==t);assert(confirm(920,t):find('INVESTED'))")
        l=investment();l.execute("for i=1,3 do T.invest(source,930+i)end;addSiteUnit(934);CityManager.GetDistrictAt=function()error('HINT_UNKNOWN')end;local v=shared.UnitActions.ReadView(0,934,'CAP');assert(not v.legal and v.potential==4 and v.reason:find('POTENTIAL_CAP_4'))")

    def test_nil_locator_is_unknown_and_does_not_remove_full_fallback(self):
        l=investment();l.execute("addSiteUnit(935);CityManager.GetDistrictAt=function()return nil end;Cities=nil;local s=shared.UnitTargets.ReadAtSite(0,{UnitID=935,Token='NIL'});assert(not s.error and #s.plots==8 and siteWork.ownerCities==1)")

    def test_missing_local_district_is_unknown_and_never_falls_back_as_empty(self):
        l=investment();l.execute("addSiteUnit(936);forbidOwner=true;missingDistrict=true;local v=shared.InvestmentAction.ReadView(0,source,936);assert(not v.legal and v.reason:find('UNIT_SITE_DISTRICT_UNKNOWN')and siteWork.ownerDistricts==0)")

    def test_unknown_location_falls_back_to_original_complete_discovery(self):
        l=investment(8);l.execute("local u=addSiteUnit(919);CityManager.GetDistrictAt=function()error('SITE_UNKNOWN')end;local s=shared.UnitTargets.ReadAtSite(0,{UnitID=919,Token='FALLBACK'});assert(not s.error and #s.plots==8 and siteWork.ownerDistricts==1 and siteWork.ownerCities==1)")


class CrewSites(unittest.TestCase):
    def test_real_crew_consumes_once_with_constant_current_city_reads(self):
        results=[]
        for n in (8,32,64):
            l=crew_site(n);l.execute("forbidOwner=true;local out=C.use(c,unit,'SITE');assert(out:find('CREW CONSUMED')and #c:GetBuildQueue().adds==1 and not C.units[20001]);assert(siteWork.ownerDistricts==0 and siteWork.ownerCities==0 and shared.UnitTargetSnapshot.token=='MARKER_KEEP');shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=20001,PlanToken='SITE'});assert(#c:GetBuildQueue().adds==1)")
            results.append({k:l.globals().siteWork[k]for k in ('ownerDistricts','ownerCities','localDistricts','cities')})
        self.assertEqual(results[0],results[1]);self.assertEqual(results[1],results[2])
        measure('S6i_Crew_current_site',{'cities':[8,32,64],'work':results,'actual_Store_Crew_UnitActions':True,'native_AddProgress_calls':1,'marker_slot_untouched':True})

    def test_same_city_two_matching_wonder_sites_are_still_ambiguous(self):
        l=crew_site();l.execute("forbidOwner=true;hdPlots={500,501};local s=shared.UnitTargets.ReadAtSite(0,{UnitID=20001,Token='AMBIG'});assert(#s.plots==0 and #s.unknown==1 and s.unknown[1].reason:find('AMBIGUOUS'));local out=shared.UnitActions.Run(0,{Action='UNIT_ACTION_PREPARE',UnitID=20001,Token='NO'});assert(out:find('REJECTED')and C.units[20001]and #c:GetBuildQueue().adds==0)")

    def test_duplicate_HD_indexes_are_deduplicated_but_marker_owner_queue_are_fresh(self):
        for change in ("plots[500].owner=3",'plots[500].mark=99999',"c:GetBuildQueue().target='BUILDING_A'","purchaseCity=siteCities[2]"):
            l=crew_site();l.execute("local s=shared.UnitTargets.ReadAtSite(0,{UnitID=20001,Token='DUPLICATE'});assert(#s.plots==1);"+change+";local s=shared.UnitTargets.ReadAtSite(0,{UnitID=20001,Token='CHANGED'});assert(#s.plots==0 and C.units[20001])")

    def test_queue_changed_during_read_is_unknown_not_a_target(self):
        l=crew_site();l.execute("local n=0;queueMutates=function()n=n+1;return n==1 and 'BUILDING_WONDER_2'or 'BUILDING_A'end;local s=shared.UnitTargets.ReadAtSite(0,{UnitID=20001,Token='QUEUE'});assert(#s.plots==0 and #s.unknown==1 and s.unknown[1].reason:find('QUEUE_CHANGED'))")

    def test_unknown_locator_preserves_full_fallback_and_marker_reply(self):
        l=crew_site();l.execute("locatorFailure=true;local s=shared.UnitTargets.ReadAtSite(0,{UnitID=20001,Token='UNKNOWN'});assert(not s.error and #s.plots==1 and siteWork.ownerDistricts>0 and siteWork.ownerCities>0 and shared.UnitTargetSnapshot.token=='MARKER_KEEP')")


if __name__=='__main__':unittest.main()
