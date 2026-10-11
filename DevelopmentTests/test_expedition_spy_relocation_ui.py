"""B198 relocation regression through actual UI creation and dispatch.

Uses current Gate/Read/Window Lua with isolated native fixtures. It proves the
permission boundary locally, not native travel, coexistence or visual rendering.
"""
import unittest
from test_expedition_spy_task import gate


def created_window():
    lua = gate(ui=True, window=True)
    lua.globals().print = lambda *args: None
    lua.execute("""
      units[50]=unit(50,103);gateOpen();Controls.CreateButton.click()
      assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED')
      assert(nameConfirmCalls==1 and initCalls==1 and units[40])
      selectedID=40;UI.GetHeadSelectedUnit=function()return units[selectedID]end
      Controls.CloseButton.click();assert(ContextPtr.hidden)
    """)
    return lua


class RelocationPermission(unittest.TestCase):
    def test_unchanged_control_through_real_create_dispatches_exactly_once(self):
        lua=created_window()
        lua.execute("""
          gateOpen('TRAVEL',40);Controls.NormalConfirmButton.click()
          assert(lastPacket.Action=='DISPATCH' and lastPacket.UnitID==40)
          assert(lastPacket.TargetOwner==3 and lastPacket.TargetID==9)
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='TRAVELLING' and nativeCalls==1)
          publish();Controls.NormalConfirmButton.click()
          assert(nativeCalls==1 and properties==0 and placeCalls==0 and destroys==0)
        """)

    def test_unrelated_post_create_spy_changes_remain_diagnostic_not_permission(self):
        for change in ["units[51]=unit(51,103)", "units[50].operation=27", "spyCapacity=3"]:
            with self.subTest(change=change):
                lua=created_window()
                lua.execute(change)
                lua.execute("""
                  -- The original snapshot is retained: diagnostics still report
                  -- CHANGED. It must no longer serve as dispatch permission.
                  gateOpen();Controls.RefreshButton.click();assert(Controls.Report.text:find('COMPARE_CHANGED'))
                  Controls.CloseButton.click();gateOpen('TRAVEL',40)
                  Controls.NormalConfirmButton.click()
                  assert(lastPacket.Action=='DISPATCH' and nativeCalls==1)
                  local r=ExposedMembers.SPC_ExpeditionGateReply
                  assert(r.phase=='TRAVELLING' and not r.error and r.sourceCity==1 and r.count==1)
                  assert(units[50] and properties==0 and destroys==0 and placeCalls==0)
                """)

    def test_later_audit_unknown_does_not_override_current_native_permission(self):
        lua=created_window()
        lua.execute("""
          spyCapacity=nil;gateOpen();Controls.RefreshButton.click()
          assert(Controls.Report.text:find('COMPARE_UNKNOWN'))
          Controls.CloseButton.click();gateOpen('TRAVEL',40);Controls.NormalConfirmButton.click()
          assert(lastPacket.Action=='DISPATCH' and nativeCalls==1)
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='TRAVELLING' and properties==0)
        """)

    def test_creation_time_changed_ordinary_spy_still_holds_before_name_binding(self):
        lua=gate(ui=True,window=True);lua.globals().print=lambda *args:None
        lua.execute("""
          units[50]=unit(50,103)
          local original=UnitManager.InitUnit
          UnitManager.InitUnit=function(...)local u=original(...);units[50].operation=27;return u end
          gateOpen();Controls.CreateButton.click()
          local r=ExposedMembers.SPC_ExpeditionGateReply
          assert(initCalls==1 and nameConfirmCalls==0 and nativeCalls==0)
          assert(r.phase=='HELD' and r.error=='ISOLATION_OR_REQUEST_STOP')
          assert(r.errorDetail:find('ORDINARY_SPY_PREFLIGHT_CHANGED',1,true))
          Controls.ArmButton.click();assert(nativeCalls==0 and properties==0)
        """)

    def test_creation_time_unknown_audit_is_still_a_stop(self):
        for timing in ['before','after']:
            with self.subTest(timing=timing):
                lua=gate(ui=True,window=True);lua.globals().print=lambda *args:None
                if timing=='before':
                    lua.execute("spyCapacity=nil;gateOpen();Controls.CreateButton.click();assert(initCalls==0 and nameConfirmCalls==0)")
                else:
                    lua.execute("""
                      local original=UnitManager.InitUnit
                      UnitManager.InitUnit=function(...)local u=original(...);spyCapacity=nil;return u end
                      gateOpen();Controls.CreateButton.click()
                      local r=ExposedMembers.SPC_ExpeditionGateReply
                      assert(initCalls==1 and nameConfirmCalls==0 and r.phase=='HELD')
                      assert(r.errorDetail:find('ORDINARY_SPY_PREFLIGHT_UNKNOWN',1,true))
                    """)
                lua.execute("assert(nativeCalls==0 and properties==0)")

    def test_real_create_does_not_relax_exact_team_or_source_proof(self):
        for change in ["city.token='replacement'", "city.owner=3", "units[40].owner=3", "units[40].name='not-the-bound-name'", "units[40].type_=103"]:
            with self.subTest(change=change):
                lua=created_window()
                lua.execute("gateOpen('TRAVEL',40);units[51]=unit(51,103);"+change+";Controls.NormalConfirmButton.click()")
                lua.execute("assert(nativeCalls==0 and destroys==0 and properties==0 and placeCalls==0)")

    def test_current_target_or_native_eligibility_rejects_without_dispatch(self):
        for change in ["targetCity.owner=4", "Players[3].GetCities=function()return {FindID=function()return nil end}end", "targetCity.x=16", "visible=false", "met=false", "nativeAllow=false", "UnitManager.CanStartOperation=nil"]:
            with self.subTest(change=change):
                lua=created_window()
                lua.execute("gateOpen('TRAVEL',40);units[51]=unit(51,103);"+change+";local count=sent;Controls.NormalConfirmButton.click();assert(sent==count and nativeCalls==0 and properties==0)")

    def test_stale_turn_between_sample_and_gameplay_ack_is_rejected(self):
        lua=created_window()
        lua.execute("""
          gateOpen('TRAVEL',40);deferred=true;Controls.NormalConfirmButton.click()
          local packet=lastPacket;assert(packet.Action=='DISPATCH' and nativeCalls==0)
          currentTurn=currentTurn+1;handler(2,packet);deferred=false;publish()
          assert(ExposedMembers.SPC_ExpeditionGateReply.error=='STALE_TRAVEL_SAMPLE')
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='CREATED' and nativeCalls==0 and properties==0)
        """)

    def test_current_native_rejection_after_ack_still_holds_no_retry(self):
        lua=created_window()
        lua.execute("""
          gateOpen('TRAVEL',40);deferred=true;Controls.NormalConfirmButton.click()
          local packet=lastPacket;nativeAllow=false;handler(2,packet);deferred=false;publish()
          assert(nativeCalls==0 and ExposedMembers.SPC_ExpeditionActivity.phase=='HELD')
          local before=sent;Controls.NormalConfirmButton.click();publish()
          assert(sent==before and nativeCalls==0 and properties==0)
        """)

    def test_native_false_or_unknown_outcome_consumes_request_and_holds(self):
        for change in ['nativeFalse=true','nativeThrow=true']:
            with self.subTest(change=change):
                lua=created_window()
                lua.execute("gateOpen('TRAVEL',40);"+change+";Controls.NormalConfirmButton.click()")
                lua.globals().expected_failure='NORMAL_FAILURE_NATIVE' if change=='nativeFalse=true' else 'NORMAL_FAILURE_UNKNOWN'
                lua.execute("""
                  local r=ExposedMembers.SPC_ExpeditionGateReply
                  assert(nativeCalls==1 and r.phase=='HELD' and r.error=='ISOLATION_OR_REQUEST_STOP')
                  assert(r.errorDetail and not r.errorDetail:find('ORDINARY_SPY_PREFLIGHT_CHANGED',1,true))
                  assert(Controls.NormalFeedback.text:find(expected_failure,1,true))
                  local before=sent;Controls.NormalConfirmButton.click();publish()
                  assert(sent==before and nativeCalls==1 and properties==0 and placeCalls==0)
                """)


def add_districts(lua,count=3):
    lua.execute("""
      districtReads=0;districtRows={};GameInfo.Districts={}
      for i=1,"""+str(count)+""" do
       local d={index=i,complete=i~=2}
       function d:GetType()return self.index end
       function d:IsComplete()return self.complete end
       function d:GetX()return 15 end;function d:GetY()return 8 end
       districtRows[i]=d
       GameInfo.Districts[i]={Index=i,DistrictType=i==3 and 'DISTRICT_WONDER' or 'DISTRICT_TEST_'..i,Name='LOC_DISTRICT_TEST_'..i}
      end
      targetCity.GetDistricts=function()districtReads=districtReads+1;return {Members=function()return ipairs(districtRows)end}end
    """)


class PresentationBoundary(unittest.TestCase):
    def test_preview_uses_native_travel_total_and_completed_nonwonder_districts_only(self):
        lua=created_window();add_districts(lua,4)
        lua.execute("""
          local reads=helperCalls
          UnitManager.CanStartOperation=function()error('preview must not check permission')end
          UnitManager.GetResultProbability=function()error('preview must not enumerate missions')end
          local v=reader.Presentation(2,40,target)
          assert(v.total==4 and v.travel==3 and v.establish==1 and #v.districts==2)
          assert(helperCalls==reads+2 and districtReads==1 and nativeCalls==0 and sent>0 and properties==0)
        """)

    def test_unavailable_optional_district_preview_never_rejects_valid_dispatch(self):
        lua=created_window()
        lua.execute("""
          targetCity.GetDistricts=function()error('display unavailable')end
          gateOpen('TRAVEL',40)
          assert(not Controls.NormalConfirmButton.disabled and Controls.NormalCityName.text)
          Controls.NormalConfirmButton.click()
          assert(nativeCalls==1 and ExposedMembers.SPC_ExpeditionActivity.phase=='TRAVELLING' and properties==0)
        """)

    def test_unrevealed_or_changed_target_has_no_timing_or_district_sample(self):
        for change in ['visible=false','met=false','targetCity.owner=4','targetCity.x=16']:
            with self.subTest(change=change):
                lua=created_window();add_districts(lua)
                lua.execute(change+";local reads=helperCalls;local v=reader.Presentation(2,40,target);assert(v.total==nil and #v.districts==0 and helperCalls==reads and districtReads==0 and nativeCalls==0)")

    def test_cached_preview_is_not_rebuilt_by_render_resize_publish_or_turn(self):
        lua=created_window();add_districts(lua,4)
        lua.execute("""
          local original=reader.Presentation;previewReads=0
          reader.Presentation=function(...)previewReads=previewReads+1;return original(...)end
          gateOpen('TRAVEL',40)
          assert(previewReads==1 and districtReads==1)
          local helpers=helperCalls;local requests=sent
          activityChanged();publish();turnBegin();systemUpdate(SystemUpdateUI.ScreenResize)
          assert(previewReads==1 and districtReads==1 and helperCalls==helpers and sent==requests)
          Controls.NormalCancelButton.click()
          assert(ContextPtr.hidden and sent==requests and nativeCalls==0)
          for _,manager in ipairs(instanceManagerList)do assert(#manager.instances==0)end
        """)

    def test_district_arrows_are_cached_and_retired_with_window(self):
        lua=created_window();add_districts(lua,10)
        lua.execute("""
          gateOpen('TRAVEL',40)
          local row=instanceManagers.SPCExpeditionDestination.instances[1]
          local calls=helperCalls;local reads=districtReads;local requests=sent
          assert(not row.DistrictsScrollRightButton.hidden)
          local old=row.DistrictsScrollRightButton.click
          assert(#row.iconPool.instances==8 and not row.iconPool.instances[1].DistrictIcon.hidden)
          assert(row.iconPool.instances[8].DistrictIcon.hidden)
          old();assert(row.iconPool.instances[1].DistrictIcon.hidden)
          assert(not row.iconPool.instances[8].DistrictIcon.hidden)
          assert(helperCalls==calls and districtReads==reads and sent==requests and nativeCalls==0)
          Controls.NormalCancelButton.click();gateOpen('TRAVEL',40)
          local fresh=instanceManagers.SPCExpeditionDestination.instances[1]
          assert(not fresh.iconPool.instances[1].DistrictIcon.hidden and fresh.iconPool.instances[8].DistrictIcon.hidden)
          old()
          assert(not fresh.iconPool.instances[1].DistrictIcon.hidden and fresh.iconPool.instances[8].DistrictIcon.hidden)
          assert(nativeCalls==0 and properties==0)
        """)


if __name__=='__main__':unittest.main()
