"""B239 actual consumer/calculation with engine-shaped Lua mocks. LOCAL only."""
from pathlib import Path
import unittest

from test_culture_network import fixture as network_fixture

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT/'Mod'


def fixture():
    lua = network_fixture()
    lua.execute((MOD/'CommerceModel.lua').read_text())
    lua.execute(r'''
      local original=P.Info
      P.Info=function(tab,id)
        if tab=='Yields' then return {Index=id:gsub('YIELD_','')} end
        return original(tab,id)
      end
      cities[2].potential=3;cities[2].active=3
      GameConfiguration={GetGameSpeedType=function()return 2 end}
      GameInfo=GameInfo or {};GameInfo.GameSpeeds={
        [2]={GameSpeedType='GAMESPEED_STANDARD'},[1]={GameSpeedType='GAMESPEED_QUICK'}}
      nativeReads={};depthReads={};commerceStates={};commerceWrites=0;cleanOrder={};applyOrder={}
      function eq(a,b)
        if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
        for k,v in pairs(a)do if not eq(v,b[k])then return false end end
        for k in pairs(b)do if a[k]==nil then return false end end;return true
      end
      function ownedGold(c)
        local n=0;for bit=0,30 do if c.present['BUILDING_SPC_COMMERCE_GOLD_'..bit]then n=n+2^bit end end;return n
      end
      for _,c in pairs(cities)do
        c.depths={};c.yields={SCIENCE=0,CULTURE=0,PRODUCTION=0,FAITH=0,GOLD=10};c.goldMultiplier=1
        function c:GetYield(y)
          local k=c.id..':'..y;nativeReads[k]=(nativeReads[k]or 0)+1
          if c.yieldFail==y then error('COMMERCE_NATIVE_YIELD_UNREADABLE')end
          if y=='GOLD'then cleanOrder[#cleanOrder+1]={city=c.id,owned=ownedGold(c)}end
          return c.yields[y]+(y=='GOLD' and ownedGold(c)*c.goldMultiplier or 0)
        end
      end
      cities[1].depths.DISTRICT_CAMPUS=6;cities[1].yields.SCIENCE=100
      cities[4].depths.DISTRICT_THEATER=6;cities[4].yields.CULTURE=80
      cities[5].depths.DISTRICT_INDUSTRIAL_ZONE=6;cities[5].yields.PRODUCTION=60
      cities[2].depths={DISTRICT_CAMPUS=3,DISTRICT_THEATER=2,DISTRICT_INDUSTRIAL_ZONE=4,DISTRICT_HOLY_SITE=2,DISTRICT_HARBOR=3}
      cities[2].yields={SCIENCE=40,CULTURE=30,PRODUCTION=20,FAITH=10,GOLD=20}
      local oldFacts=shared.EffectiveFacts.Read
      shared.EffectiveFacts.Read=function(pid,c)
        local f=oldFacts(pid,c);f.owner=pid;f.cityID=c.id;f.activeStatus=c.active==nil and 'UNKNOWN_GOVERNOR' or 'KNOWN';return f
      end
      shared.DistrictCompleteness={ReadFacts=function(pid,c,token)
        depthReads[c.id]=(depthReads[c.id] or 0)+1
        assert(c.owner==pid and token==c.token,'DC_REFERENCE_INVALID')
        if c.dcFail then return {validity='UNKNOWN',availability='TEMPORARILY_UNAVAILABLE'}end
        local domains={};for k,v in pairs(c.depths)do domains[k]={value=v}end
        return {validity='VERIFIED',availability='READY',value={domains=domains,districts={{
          id=c.id,type=families[c.kind],plot=c.id*100,complete=true,pillaged=c.pillaged==true}}}}
      end}
      local st=shared.CityProgressionStore
      st.HistoryStartStatus=function()return 'EXISTING'end
      st.HistoricalReference=function(c)
        assert(c.owner==0 and not c.bindingFail,'COMMERCE_BINDING_UNAVAILABLE')
        return {owner=c.owner,cityID=c.id,token=c.token,x=c:GetX(),y=c:GetY()}
      end
      st.CommerceState=function(pid,c)
        assert(pid==c.owner and not c.storeFail,'COMMERCE_STORE_UNAVAILABLE')
        return {value=SPCCommerceModel.Copy(commerceStates[c.id]),token=c.token,
          reference={owner=pid,cityID=c.id,x=c:GetX(),y=c:GetY()}}
      end
      st.WriteCommerce=function(pid,c,old,value)
        assert(eq(commerceStates[c.id],old),'COMMERCE_STALE')
        assert(eq(old and old.reputation,value.reputation),'COMMERCE_REPUTATION_STORE_OWNED')
        assert(not failStoreWrite,'COMMERCE_STORE_WRITE_FAILED')
        SPCCommerceModel.Validate(value);commerceStates[c.id]=SPCCommerceModel.Copy(value);commerceWrites=commerceWrites+1
      end
      Locale={Lookup=function(s)return s end}
      priorPermanent=0;shared.OnPermanentCityWrite=function()priorPermanent=priorPermanent+1 end
      CityManager={GetCityAt=function(x,y)
        for _,c in pairs(cities)do if c:GetX()==x and c:GetY()==y then return c end end
      end}
      onCreate=function(c,id)
        if id:find('BUILDING_SPC_COMMERCE_GOLD_',1,true)then applyOrder[#applyOrder+1]={city=c.id,owned=ownedGold(c)}end
        Events.BuildingAddedToMap.Fire(c:GetX(),c:GetY(),id,c.owner)
      end
    ''')
    lua.execute((MOD/'Commerce.lua').read_text())
    lua.execute('''
      SPCCommerce.Start(P,shared);com=shared.Commerce;com.BindPermanentWrites();com.Audit()
      function view(cid)return com.views['0:'..cid]end
      function toggle(cid,domain,enabled)
        local v=view(cid)
        return com.Request(0,{Action='COMMERCE_SELECT',CityID=cid,Domain=domain,Enabled=enabled,
          Reference=v.reference,CityToken=v.token,Revision=v.revision,Token='LOCAL_TEST'})
      end
      function domain(cid,id)for _,r in ipairs(view(cid).domains)do if r.id==id then return r end end end
    ''')
    return lua


class Commercialization(unittest.TestCase):
    def test_quick_speed_clears_effects_without_rescaling_or_deleting_choices(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));local saved=SPCCommerceModel.Copy(commerceStates[2])
          GameConfiguration.GetGameSpeedType=function()return 1 end;com.SourceChanged(0,2)
          assert(view(2).stage=='HELD' and view(2).reason=='COMMERCE_STANDARD_SPEED_ONLY')
          assert(ownedGold(cities[2])==0 and not cities[2].present.BUILDING_SPC_COMMERCIALIZATION_ACCESS)
          assert(eq(saved,commerceStates[2]))
        ''')

    def test_unavailable_speed_reader_holds_without_assuming_standard(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));GameConfiguration.GetGameSpeedType=nil
          com.SourceChanged(0,2)
          assert(view(2).stage=='HELD' and view(2).reason=='COMMERCE_SPEED_UNKNOWN')
          assert(ownedGold(cities[2])==0 and #commerceStates[2].selected==1)
        ''')

    def test_direct_pool_local_depth_and_per_domain_floor(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));assert(toggle(2,'DISTRICT_THEATER',true))
          assert(domain(2,'DISTRICT_CAMPUS').source==1 and domain(2,'DISTRICT_CAMPUS').localD==3)
          assert(domain(2,'DISTRICT_CAMPUS').X==100 and domain(2,'DISTRICT_CAMPUS').gold==15)
          assert(domain(2,'DISTRICT_THEATER').source==4 and view(2).totalGold==23 and ownedGold(cities[2])==23)
          cities[1].yields.SCIENCE=11.9;cities[2].yields.SCIENCE=11.9
          cities[4].yields.CULTURE=19.9;cities[2].yields.CULTURE=19.9
          com.SourceChanged(0,1);com.SourceChanged(0,4)
          assert(math.abs(view(2).totalRaw-3.775)<1e-9 and view(2).totalGold==2)
          assert(domain(2,'DISTRICT_CAMPUS').gold==1 and domain(2,'DISTRICT_THEATER').gold==1)
        ''')

    def test_self_source_is_legal_and_distributed_non_direct_source_is_excluded(self):
        lua=fixture();lua.execute('''
          cities[3].depths.DISTRICT_CAMPUS=10;cities[3].yields.SCIENCE=9999
          assert(toggle(2,'DISTRICT_CAMPUS',true));assert(domain(2,'DISTRICT_CAMPUS').source==1)
          send('0,4,0,2,10;0,2,0,5,12',2)
          assert(domain(2,'DISTRICT_CAMPUS').source==2 and domain(2,'DISTRICT_CAMPUS').X==40)
        ''')

    def test_remote_total_yield_needs_no_matching_district_or_store_record(self):
        lua=fixture();lua.execute('''
          cities[1].depths={};cities[1].dcFail=true;cities[1].storeFail=true;cities[1].yields.SCIENCE=400
          assert(toggle(2,'DISTRICT_CAMPUS',true))
          assert(domain(2,'DISTRICT_CAMPUS').source==1 and domain(2,'DISTRICT_CAMPUS').X==400)
          assert(ownedGold(cities[2])==60)
        ''')

    def test_lifo_suspend_restore_and_manual_reopen_changes_order(self):
        lua=fixture();lua.execute('''
          cities[2].workers=3;com.SourceChanged(0,2)
          for _,id in ipairs({'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE'})do assert(toggle(2,id,true))end
          assert(#view(2).effective==3 and #commerceStates[2].selected==3)
          cities[2].workers=1;com.SourceChanged(0,2)
          assert(#view(2).effective==1 and view(2).effective[1]=='DISTRICT_CAMPUS')
          assert(domain(2,'DISTRICT_THEATER').suspended and domain(2,'DISTRICT_INDUSTRIAL_ZONE').suspended)
          cities[2].workers=2;com.SourceChanged(0,2);assert(#view(2).effective==2 and domain(2,'DISTRICT_THEATER').effective)
          cities[2].workers=3;com.SourceChanged(0,2);assert(#view(2).effective==3)
          assert(toggle(2,'DISTRICT_CAMPUS',false));assert(toggle(2,'DISTRICT_CAMPUS',true))
          cities[2].workers=1;com.SourceChanged(0,2)
          assert(view(2).effective[1]=='DISTRICT_THEATER' and commerceStates[2].selected[3]=='DISTRICT_CAMPUS')
        ''')

    def test_ineligible_local_domain_is_suspended_without_deleting_selection(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));assert(toggle(2,'DISTRICT_THEATER',true))
          cities[2].depths.DISTRICT_CAMPUS=nil;com.SourceChanged(0,2)
          assert(domain(2,'DISTRICT_CAMPUS').suspended and domain(2,'DISTRICT_THEATER').effective)
          assert(#commerceStates[2].selected==2)
          cities[2].depths.DISTRICT_CAMPUS=3;com.SourceChanged(0,2);assert(domain(2,'DISTRICT_CAMPUS').effective)
        ''')

    def test_reputation_multiplier_only_while_active_iv_and_backend_never_ticks_it(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true))
          commerceStates[2].reputation={version=1,start=0,cursor=20,age=20,receipt='P4',state='COUNTING'}
          cities[2].potential=4;cities[2].active=4;com.SourceChanged(0,2)
          assert(view(2).reputation.effective==20 and view(2).totalGold==16)
          local writes=commerceWrites;turn=21;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()
          assert(commerceStates[2].reputation.age==20 and commerceWrites==writes)
          cities[2].active=3;com.SourceChanged(0,2)
          assert(view(2).reputation.age==20 and view(2).reputation.effective==0 and view(2).totalGold==15)
          cities[2].active=2;com.SourceChanged(0,2)
          assert(view(2).totalGold==0 and ownedGold(cities[2])==0 and #commerceStates[2].selected==1)
          cities[2].active=4;com.SourceChanged(0,2);assert(view(2).totalGold==16)
        ''')

    def test_unprovable_p4_start_is_not_fabricated(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));cities[2].potential=4;cities[2].active=4
          com.SourceChanged(0,2);assert(view(2).stage=='HELD' and view(2).reason=='COMMERCE_REPUTATION_UNKNOWN')
          assert(ownedGold(cities[2])==0 and commerceStates[2].reputation==nil)
        ''')

    def test_unknown_reputation_interval_does_not_claim_a_complete_current_iv_value(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true))
          commerceStates[2].reputation={version=1,start=0,cursor=20,age=20,receipt='P4',state='UNKNOWN_INTERVAL'}
          cities[2].potential=4;cities[2].active=4;com.SourceChanged(0,2)
          assert(view(2).stage=='HELD' and ownedGold(cities[2])==0 and commerceStates[2].reputation.age==20)
          cities[2].active=3;com.SourceChanged(0,2)
          assert(view(2).stage=='READY' and view(2).reputation.effective==0 and ownedGold(cities[2])==15)
        ''')

    def test_unknown_facts_and_network_withdraw_owned_gold_without_erasing_choices(self):
        for change in ["cities[2].active=nil", "cities[2].storeFail=true", "cities[2].dcFail=true", "net.CheckEvidence(false)"]:
            with self.subTest(change=change):
                lua=fixture();lua.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));"+change+";com.SourceChanged(0,2);assert(view(2).stage=='HELD' and ownedGold(cities[2])==0 and #commerceStates[2].selected==1)")

    def test_source_unknown_blocks_use_and_recovery_is_event_driven(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));cities[1].yieldFail='SCIENCE';com.SourceChanged(0,1)
          assert(view(2).stage=='HELD' and ownedGold(cities[2])==0)
          cities[1].yieldFail=nil;com.SourceChanged(0,1);assert(view(2).stage=='READY' and ownedGold(cities[2])==15)
        ''')

    def test_no_change_non_harbor_has_no_carrier_or_store_writes(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));local n=com.writes;local p=commerceWrites;local r=view(2).revision
          for i=1,10 do com.SourceChanged(0,1)end
          assert(com.writes==n and commerceWrites==p and view(2).revision==r)
          local reads=nativeReads['1:SCIENCE'];for i=1,20 do Events.GameCoreEventPublishComplete.Fire()end
          assert(nativeReads['1:SCIENCE']==reads and com.writes==n)
        ''')

    def test_same_turn_real_changes_recompute_and_burst_notifications_coalesce(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));cities[1].yields.SCIENCE=200
          local reads=nativeReads['1:SCIENCE']
          for i=1,12 do Events.CityWorkerChanged.Fire(0,1)end
          assert(nativeReads['1:SCIENCE']==reads)
          Events.GameCoreEventPublishComplete.Fire();assert(ownedGold(cities[2])==30 and nativeReads['1:SCIENCE']==reads+1)
          cities[1].yields.SCIENCE=300;com.SourceChanged(0,1);assert(ownedGold(cities[2])==45)
          cities[1].yields.SCIENCE=100;com.SourceChanged(0,1);assert(ownedGold(cities[2])==15)
        ''')

    def test_other_profession_carrier_event_after_commerce_recomputes_dependency(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));local before=nativeReads['1:SCIENCE']
          -- A later producer in the same publication changes total native Science.
          cities[1].yields.SCIENCE=300
          Events.BuildingAddedToMap.Fire(cities[1]:GetX(),cities[1]:GetY(),'BUILDING_SPC_OTHER_PROFESSION_YIELD',0)
          assert(ownedGold(cities[2])==15)
          Events.GameCoreEventPublishComplete.Fire()
          assert(ownedGold(cities[2])==45 and nativeReads['1:SCIENCE']==before+1)
          before=nativeReads['1:SCIENCE']
          Events.BuildingAddedToMap.Fire(cities[2]:GetX(),cities[2]:GetY(),'BUILDING_SPC_COMMERCE_GOLD_0',0)
          Events.GameCoreEventPublishComplete.Fire();assert(nativeReads['1:SCIENCE']==before)
        ''')

    def test_permanent_identity_write_discovers_new_consumer_and_keeps_previous_callback(self):
        lua=fixture();lua.execute('''
          cities[3].kind='COMMERCE';cities[3].potential=3;cities[3].active=3;cities[3].depths={DISTRICT_CAMPUS=2}
          shared.OnPermanentCityWrite(cities[3],'CityProgressionStore.lua')
          Events.GameCoreEventPublishComplete.Fire();assert(view(3).stage=='READY' and priorPermanent==1)
          -- Native construction's second value is a district type, not a city ID.
          GameEvents.OnDistrictConstructed.Fire(0,999,3,10)
          Events.GameCoreEventPublishComplete.Fire();assert(view(999)==nil and view(3).stage=='READY')
        ''')

    def test_explicit_network_isolation_clears_only_owned_effects_and_preserves_history(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));local saved=SPCCommerceModel.Copy(commerceStates[2])
          cities[2].present.UNRELATED=true
          shared.NetworkIsolation={Active=function(pid)return pid==nil or pid==0 end}
          assert(com.ExperimentalNetworkWithdraw(0))
          assert(ownedGold(cities[2])==0 and cities[2].present.UNRELATED and eq(saved,commerceStates[2]))
          assert(view(2).reason=='COMMERCE_EXPERIMENT_ISOLATED')
          local writes=com.writes;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()
          assert(com.writes==writes and ownedGold(cities[2])==0)
        ''')

    def test_unknown_legacy_residue_prevents_double_grant(self):
        for carrier in ['BUILDING_SPC_DEV_LV3_COM_RESEARCH','BUILDING_SPC_B061_SCIENCE_0']:
            with self.subTest(carrier=carrier):
                lua=fixture();lua.globals().legacyCarrier=carrier
                lua.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));cities[2].present[legacyCarrier]=true;com.SourceChanged(0,2);assert(view(2).reason=='COMMERCE_LEGACY_REMAINS' and ownedGold(cities[2])==0)")

    def test_shared_native_source_read_once_and_no_remote_depth_capture(self):
        lua=fixture();lua.execute('''
          cities[3].kind='COMMERCE';cities[3].potential=3;cities[3].active=3
          cities[3].depths={DISTRICT_CAMPUS=2}
          commerceStates[3]=SPCCommerceModel.Select(SPCCommerceModel.New(0),'DISTRICT_CAMPUS',true)
          com.SourceChanged(0,3);assert(toggle(2,'DISTRICT_CAMPUS',true))
          send('0,1,0,2,10;0,1,0,3,11',2)
          nativeReads={};depthReads={};com.Audit({player=0})
          assert(ownedGold(cities[2])==15 and ownedGold(cities[3])==10)
          assert(nativeReads['1:SCIENCE']==1 and depthReads[2]==1 and depthReads[3]==1 and not depthReads[1])
        ''')

    def test_failed_configuration_write_does_not_publish_or_grant_candidate_choice(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));failStoreWrite=true
          assert(not toggle(2,'DISTRICT_THEATER',true))
          assert(#commerceStates[2].selected==1 and #view(2).selected==1 and ownedGold(cities[2])==15)
        ''')

    def test_failed_effect_readback_clears_partial_candidate_and_reports_held(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));local original=P.CreateBuilding
          P.CreateBuilding=function(q,id)if id=='BUILDING_SPC_COMMERCE_GOLD_4'then return end;original(q,id)end
          cities[1].yields.SCIENCE=200;com.SourceChanged(0,1)
          assert(view(2).stage=='HELD' and #view(2).effective==0 and ownedGold(cities[2])==0)
          assert(view(2).cleanupConfirmed and view(2).remainingCarrierGold==0)
        ''')

    def test_failed_withdrawal_does_not_claim_native_cleanup_pass(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));local original=P.RemoveBuilding
          P.RemoveBuilding=function(b,id)if id:find('BUILDING_SPC_COMMERCE_GOLD_',1,true)then return end;original(b,id)end
          cities[2].active=2;com.SourceChanged(0,2)
          assert(view(2).stage=='HELD' and not view(2).cleanupConfirmed and view(2).remainingCarrierGold==15)
          assert(com.Describe(0,cities[2]):find('清理尚未确认',1,true))
        ''')

    def test_unknown_harbor_source_carrier_presence_never_leaves_stale_ready_result(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_HARBOR',true));local original=P.HasBuilding
          P.HasBuilding=function(b,id)if b.city.id==1 and id=='BUILDING_SPC_COMMERCE_GOLD_0'then return nil end;return original(b,id)end
          com.SourceChanged(0,1)
          assert(view(2).stage=='HELD' and ownedGold(cities[2])==0 and #view(2).effective==0)
        ''')

    def test_domain_log_contains_source_depth_x_raw_and_final_without_names(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));local found=false
          for _,r in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do
            if r.stage=='COMMERCE_DOMAIN' and r.city=='2' then
              assert(r.networkKind=='DISTRICT_CAMPUS' and r.sourceCity=='1' and r.count=='3')
              assert(r.previous=='100' and tonumber(r.baseInput)==15 and r.expected=='15');found=true
            end
          end
          assert(found)
        ''')

    def test_confirmed_exit_removes_exact_owned_effect_and_target_dependencies(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));cities[2].present.UNRELATED=true
          exits.Commerce(cities[2],{confirmed=true,origin={owner=0,cityID=2}})
          assert(ownedGold(cities[2])==0 and cities[2].present.UNRELATED and view(2)==nil)
        ''')

    def test_readable_report_and_stale_request_rejection(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));assert(com.Describe(0,cities[2]):find('合计 +15',1,true))
          local old=SPCCommerceModel.Copy(view(2));cities[2].workers=0
          local yes,reason=com.Request(0,{Action='COMMERCE_SELECT',CityID=2,Domain='DISTRICT_THEATER',Enabled=true,
            Reference=old.reference,CityToken=old.token,Revision=old.revision,Token='STALE'})
          assert(not yes and reason=='COMMERCE_VIEW_STALE' and #commerceStates[2].selected==1)
          assert(com.lastRequest.token=='STALE' and not com.lastRequest.accepted)
        ''')

    def test_new_consumer_session_reconstructs_selection_and_removes_saved_output_first(self):
        lua=fixture();lua.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));assert(toggle(2,'DISTRICT_THEATER',true))
          saved=SPCCommerceModel.Copy(commerceStates[2]);oldRegisterExit=shared.CityProgressionStore.RegisterExit
          shared.CityProgressionStore.RegisterExit=function()end;shared.CityProgressionStore.RegisterReturn=function()end
          local old=com;SPCCommerce.Start(P,shared);com=shared.Commerce;com.Audit()
          assert(eq(commerceStates[2],saved) and #view(2).effective==2 and ownedGold(cities[2])==23)
          assert(com~=old and com.ready)
        ''')


class GoldRecursion(unittest.TestCase):
    def test_actual_owned_gold_removed_before_harbor_read_with_city_multiplier(self):
        lua=fixture();lua.execute('''
          cities[2].goldMultiplier=2;assert(toggle(2,'DISTRICT_CAMPUS',true));assert(ownedGold(cities[2])==15)
          assert(cities[2]:GetYield('GOLD')==50)
          cleanOrder={};assert(toggle(2,'DISTRICT_HARBOR',true))
          local harbor=domain(2,'DISTRICT_HARBOR')
          assert(harbor.X==20 and harbor.gold==3 and ownedGold(cities[2])==18)
          for _,r in ipairs(cleanOrder)do assert(r.owned==0)end
          for i=1,5 do com.SourceChanged(0,2);assert(domain(2,'DISTRICT_HARBOR').X==20 and ownedGold(cities[2])==18)end
        ''')

    def test_two_commerce_sources_are_planned_clean_before_any_new_gold(self):
        lua=fixture();lua.execute('''
          cities[4].kind='COMMERCE';cities[4].potential=3;cities[4].active=3
          cities[4].depths={DISTRICT_HARBOR=3};cities[4].yields.GOLD=40;cities[4].goldMultiplier=2
          commerceStates[4]=SPCCommerceModel.Select(SPCCommerceModel.New(0),'DISTRICT_HARBOR',true)
          com.SourceChanged(0,4);assert(toggle(2,'DISTRICT_HARBOR',true))
          cleanOrder={};applyOrder={};com.Audit({player=0})
          assert(domain(2,'DISTRICT_HARBOR').X==40 and domain(4,'DISTRICT_HARBOR').X==40)
          assert(ownedGold(cities[2])==6 and ownedGold(cities[4])==6)
          for _,r in ipairs(cleanOrder)do assert(r.owned==0)end
          assert(#applyOrder>0)
        ''')

    def test_non_target_gold_source_is_restored_without_its_gold_entering_x(self):
        lua=fixture();lua.execute('''
          cities[4].kind='COMMERCE';cities[4].potential=3;cities[4].active=3
          cities[4].depths={DISTRICT_CAMPUS=3};cities[4].yields.SCIENCE=1000;cities[4].yields.GOLD=50
          commerceStates[4]=SPCCommerceModel.Select(SPCCommerceModel.New(0),'DISTRICT_CAMPUS',true)
          com.SourceChanged(0,4);assert(ownedGold(cities[4])==150)
          assert(toggle(2,'DISTRICT_HARBOR',true))
          com.SourceChanged(0,1)
          assert(domain(2,'DISTRICT_HARBOR').X==50 and ownedGold(cities[4])==150)
        ''')


if __name__=='__main__':
    unittest.main()
