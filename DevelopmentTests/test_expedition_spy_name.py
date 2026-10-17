"""B189 native-name observation against actual Gate, UI reader and Window.
The fixture models a native assigned name, not proof Civ VI assigns/preserves it.
Tests isolate gameplay confirmation from UI observations and never send NAME_UNIT.
"""
import unittest
from test_expedition_spy_gate import gate


class NamePreparation(unittest.TestCase):
    def test_create_requires_explicit_independent_confirmation_before_dispatch(self):
        l=gate();l.execute("""
          local r=rawreq('CREATE','a')
          assert(r.phase=='NAMING' and not r.bound and not r.expectedName and r.teamKey and r.sourceCity==1 and properties==0)
          r=nativeDispatch('early');assert(r.error and not r.nativePermit and r.phase=='NAMING')
          r=rawreq('READ','wait');assert(r.phase=='NAMING' and not r.bound and not r.expectedName)
          r=confirmName('verify',40,'LOC_CITIZEN_TEST_A')
          assert(r.phase=='CREATED' and r.bound and r.expectedName=='LOC_CITIZEN_TEST_A')
          assert(nativeDispatch('ready').nativePermit=='ready' and properties==0 and nativeCalls==0)
        """)

    def test_source_current_id_and_location_required_for_confirmation(self):
        for change in ['city.token=nil','city.token="other"','city.owner=3','units[40].owner=3','units[40].type_=103','units[40].id=41','units[40].x=2']:
            with self.subTest(change=change):
                l=gate();l.execute("rawreq('CREATE','a');"+change+";local r=confirmName('n',40,'LOC_CITIZEN_TEST_A');assert(r.phase=='HELD' and not r.bound and r.count==1 and initCalls==1 and properties==0 and destroys==0)")

    def test_default_empty_wrong_unreadable_names_never_become_authority(self):
        for change in ['units[40].name=nil','units[40].name=""','units[40].name="LOC_TEST_DEFAULT"','units[40].name="wrong"','units[40].name="LOC_CITIZEN_OTHER"','units[40].GetName=nil',"units[40].GetName=function()error('unknown name')end"]:
            with self.subTest(change=change):
                l=gate();l.execute("rawreq('CREATE','a');"+change+";local r=confirmName('n',40,'LOC_CITIZEN_TEST_A');assert(not r.bound and r.phase=='HELD' and not r.expectedName);assert(not nativeDispatch('d').nativePermit and properties==0 and initCalls==1)")

    def test_gameplay_rechecks_readback_instead_of_trusting_ui_packet(self):
        l=gate();l.execute("""
          rawreq('CREATE','a');units[40].name='LOC_CITIZEN_TEST_B'
          local r=confirmName('stale',40,'LOC_CITIZEN_TEST_A')
          assert(r.phase=='HELD' and not r.bound and not r.expectedName and properties==0)
        """)

    def test_missing_pool_or_config_cannot_confirm_even_matching_name(self):
        for change in ['poolRows={}','GameInfo.CivilizationCitizenNames=nil',"GameInfo.CivilizationCitizenNames=function()error('db unavailable')end",'PlayerConfigurations[2]=nil','civilization="CIVILIZATION_EMPTY"']:
            with self.subTest(change=change):
                l=gate();l.execute("rawreq('CREATE','a');"+change+";local r=confirmName('n',40,'LOC_CITIZEN_TEST_A');assert(r.phase=='HELD' and not r.bound and not r.expectedName and initCalls==1 and properties==0)")

    def test_duplicate_live_name_outside_target_is_rejected(self):
        l=gate();l.execute("""
          rawreq('CREATE','a');units[50]=unit(50,100,2,99,99);units[50].name='LOC_CITIZEN_TEST_A'
          local r=confirmName('n',40,'LOC_CITIZEN_TEST_A')
          assert(r.phase=='HELD' and not r.bound and not r.expectedName and properties==0 and destroys==0)
        """)

    def test_missing_or_stale_ui_offmap_observation_does_not_confirm(self):
        # Native off-map enumeration is UI-only evidence, like travel permission.
        # Gameplay requires its fresh explicit sample, not an invented API call.
        for fields in ['', 'NameOffmapChecked=false,NameSampleTurn=81,', 'NameOffmapChecked=true,NameSampleTurn=80,']:
            with self.subTest(fields=fields):
                l=gate();l.execute("rawreq('CREATE','a');handler(2,{Action='NAME',Token='n',UnitID=40,Name='LOC_CITIZEN_TEST_A',"+fields+"});local r=ExposedMembers.SPC_ExpeditionGateReply;assert(r.phase=='HELD' and not r.bound and not r.expectedName and properties==0)")

    def test_unique_localized_name_is_preserved_verbatim(self):
        l=gate();l.execute("""
          local lookup=Locale.Lookup;Locale.Lookup=function(key,...)if key=='LOC_CITIZEN_TEST_A' then return 'Alice' end;return lookup(key,...)end
          nativeName='Alice';local r=req('CREATE','a')
          assert(r.phase=='CREATED' and r.expectedName=='Alice' and units[40].name=='Alice' and properties==0)
        """)

    def test_ambiguous_localized_name_is_not_identity(self):
        l=gate();l.execute("""
          local lookup=Locale.Lookup;Locale.Lookup=function(key,...)if key=='LOC_CITIZEN_TEST_A' or key=='LOC_CITIZEN_TEST_B' then return 'Same Name' end;return lookup(key,...)end
          nativeName='Same Name';rawreq('CREATE','a');local r=confirmName('n',40,'Same Name')
          assert(r.phase=='HELD' and not r.bound and not r.expectedName and properties==0)
        """)

    def test_unrelated_foreign_name_does_not_change_source_mapping(self):
        l=gate();l.execute("""
          foreignUnits[9]=unit(9,100,3,15,8);foreignUnits[9].name='LOC_CITIZEN_TEST_A'
          local r=req('CREATE','a');assert(r.bound and r.expectedName=='LOC_CITIZEN_TEST_A' and r.sourceCity==1)
        """)

    def test_duplicate_confirmation_is_idempotent_and_has_no_native_side_effect(self):
        l=gate();l.execute("""
          rawreq('CREATE','a');confirmName('n',40,'LOC_CITIZEN_TEST_A');confirmName('n',40,'LOC_CITIZEN_TEST_A')
          local r=rawreq('READ','r');assert(r.phase=='CREATED' and r.bound and r.expectedName=='LOC_CITIZEN_TEST_A')
          assert(initCalls==1 and properties==0 and nativeCalls==0 and destroys==0)
        """)

    def test_source_label_is_display_only_and_source_reference_stays_separate(self):
        l=gate();l.execute("""
          local r=req('CREATE','a');local expected=r.expectedName
          city.GetName=function()return '新名字' end
          r=req('READ','b');assert(r.bound and r.expectedName==expected and r.sourceCity==1)
          city.token='new-city-same-name';r=req('READ','c');assert(not r.bound and r.phase=='HELD')
        """)

    def test_native_name_may_be_reused_after_end_but_session_key_is_fresh(self):
        l=gate();l.execute("""
          local a=req('CREATE','a');local key=a.teamKey;local name=a.expectedName
          req('END','b',40);local b=req('CREATE','c')
          assert(b.phase=='CREATED' and b.unitID==40 and b.teamKey~=key and b.expectedName==name and initCalls==2 and properties==0)
        """)

    def test_long_city_label_never_becomes_or_truncates_native_identity(self):
        l=gate();l.execute("""
          -- Longest player-enterable label: the native city-name EditBox is MaxLength 32;
          -- 32 four-byte characters (128 bytes) stay inside the Store's 220-byte bound.
          city.GetName=function()return string.rep(utf8.char(0x1F3EF),32) end
          local r=req('CREATE','a')
          assert(r.phase=='CREATED' and r.expectedName=='LOC_CITIZEN_TEST_A' and r.sourceCity==1 and properties==0)
        """)

    def test_after_confirmation_name_mutation_holds_without_relabel_or_recreate(self):
        l=gate();l.execute("req('CREATE','a');units[40].name='unexpected';local r=req('READ','r');assert(r.phase=='HELD' and not r.bound and properties==0 and initCalls==1 and destroys==0);req('CREATE','again');assert(initCalls==1)")

    def test_observed_name_survives_without_any_unit_properties(self):
        l=gate();l.execute("""
          local r=req('CREATE','a');local name=r.expectedName;nativeDispatch('b')
          units[40]=nil;units[41]=unit(41,100,2,15,8);units[41].name=name
          units[41].GetProperty=nil;units[41].SetProperty=nil
          currentTurn=83;ownTurn(2);r=req('READ','c')
          assert(r.phase=='ARRIVED' and r.bound and r.unitID==41 and r.sourceCity==1 and properties==0)
        """)


class NativeNameReader(unittest.TestCase):
    def test_native_name_observation_never_uses_rename_api_or_selected_unit(self):
        l=gate(ui=True);l.execute("""
          units[7]=unit(7,103);rawreq('CREATE','a');UI={GetHeadSelectedUnit=function()return units[7]end}
          local r=reader.NativeName(2,40)
          assert(r.status=='READY' and r.name=='LOC_CITIZEN_TEST_A' and r.poolCount==2 and r.defaultName=='LOC_TEST_DEFAULT')
          assert(nameCalls==0 and nativeCalls==0 and properties==0 and units[7]:GetName()=='Native Spy')
          assert(rawreq('READ','r').phase=='NAMING')
        """)

    def test_default_empty_and_unreadable_names_are_pending(self):
        for change in ['units[40].name=nil','units[40].name=""','units[40].name="LOC_TEST_DEFAULT"','units[40].GetName=nil',"units[40].GetName=function()error('unknown name')end"]:
            with self.subTest(change=change):
                l=gate(ui=True);l.execute("rawreq('CREATE','a');"+change+";local r=reader.NativeName(2,40);assert(r.status=='PENDING' and r.reason and nameCalls==0 and nativeCalls==0 and properties==0)")

    def test_unavailable_pool_foreign_pool_and_duplicate_are_invalid(self):
        for change in ['poolRows={}','GameInfo.CivilizationCitizenNames=nil','PlayerConfigurations[2]=nil',"units[40].name='LOC_CITIZEN_OTHER'","units[7]=unit(7,100,2,99,99);units[7].name='LOC_CITIZEN_TEST_A'","offmap=1;offmapRows={{Name='LOC_CITIZEN_TEST_A'}}"]:
            with self.subTest(change=change):
                l=gate(ui=True);l.execute("rawreq('CREATE','a');"+change+";local r=reader.NativeName(2,40);assert(r.status=='INVALID' and r.reason and nameCalls==0 and nativeCalls==0 and properties==0)")

    def test_offmap_missing_record_name_or_count_is_pending(self):
        for change in ['offmap=1;offmapRows={}', 'offmap=1;offmapRows={{Name=nil}}', 'offmap=nil', 'offmap=-1']:
            with self.subTest(change=change):
                l=gate(ui=True);l.execute("rawreq('CREATE','a');"+change+";local r=reader.NativeName(2,40);assert(r.status=='PENDING' and r.reason and nameCalls==0 and nativeCalls==0 and properties==0)")

    def test_unique_localized_name_is_accepted_without_normalization(self):
        l=gate(ui=True);l.execute("""
          local lookup=Locale.Lookup;Locale.Lookup=function(key,...)if key=='LOC_CITIZEN_TEST_A' then return 'Alice' end;return lookup(key,...)end
          nativeName='Alice';rawreq('CREATE','a');local r=reader.NativeName(2,40)
          assert(r.status=='READY' and r.name=='Alice' and r.representation=='LOCALIZED_VALUE' and nameCalls==0)
        """)

    def test_ambiguous_localization_is_rejected_but_exact_raw_key_remains_valid(self):
        l=gate(ui=True);l.execute("""
          local lookup=Locale.Lookup;Locale.Lookup=function(key,...)if key=='LOC_CITIZEN_TEST_A' or key=='LOC_CITIZEN_TEST_B' then return 'Same Name' end;return lookup(key,...)end
          nativeName='Same Name';rawreq('CREATE','a');local r=reader.NativeName(2,40)
          assert(r.status=='INVALID' and r.reason=='TEAM_NATIVE_NAME_AMBIGUOUS_LOCALIZED')
          units[40].name='LOC_CITIZEN_TEST_A';r=reader.NativeName(2,40)
          assert(r.status=='READY' and r.representation=='RAW_KEY' and nameCalls==0)
        """)

    def test_exact_custom_unit_is_required_by_readiness(self):
        l=gate(ui=True);l.execute("""
          rawreq('CREATE','a')
          local state,why,u=reader.NameReadiness(2,40)
          assert(state=='READY' and why=='UI_UNIT_READY' and u==units[40])
          assert(nameCalls==0 and nativeCalls==0 and properties==0)
        """)

    def test_missing_and_unreadable_ui_evidence_is_pending(self):
        for change,reason in [
            ('Players[2].GetUnits=function()return nil end','UI_UNITS_UNREADABLE'),
            ("Players[2].GetUnits=function()error('unavailable')end",'UI_UNITS_UNREADABLE'),
            ('units[40]=nil','UI_UNIT_NOT_PUBLISHED'),
            ("Players[2].GetUnits=function()return {FindID=function()error('unavailable')end}end",'UI_UNIT_LOOKUP_UNREADABLE'),
            ("units[40].GetID=function()error('unavailable')end",'UI_UNIT_ID_UNREADABLE'),
            ("units[40].GetOwner=function()error('unavailable')end",'UI_UNIT_OWNER_UNREADABLE'),
            ("units[40].GetUnitType=function()error('unavailable')end",'UI_UNIT_TYPE_UNREADABLE'),
        ]:
            with self.subTest(reason=reason,change=change):
                l=gate(ui=True);l.globals().expectedReason=reason
                l.execute("rawreq('CREATE','a');"+change+";local state,why=reader.NameReadiness(2,40);assert(state=='PENDING' and why==expectedReason);assert(nameCalls==0 and nativeCalls==0 and properties==0)")

    def test_definite_identity_or_database_mismatch_is_invalid(self):
        for change,reason in [
            ('Players[2]=nil','UI_PLAYER_UNAVAILABLE'),
            ('units[40].id=41','UI_UNIT_ID_MISMATCH'),
            ('units[40].owner=3','UI_UNIT_OWNER_MISMATCH'),
            ('units[40].type_=103','UI_UNIT_TYPE_MISMATCH'),
            ('info[100]=nil','UI_UNIT_DEFINITION_UNAVAILABLE'),
        ]:
            with self.subTest(reason=reason):
                l=gate(ui=True);l.globals().expectedReason=reason
                l.execute("rawreq('CREATE','a');"+change+";local state,why=reader.NameReadiness(2,40);assert(state=='INVALID' and why==expectedReason);assert(nameCalls==0 and nativeCalls==0 and properties==0)")


def publication_window(mode='missing'):
    """Delay/alter only the UI view; the actual Gameplay unit stays exact."""
    l=gate(window=True);l.globals().uiMode=mode
    l.execute(r'''
      local realGetUnits=Players[2].GetUnits
      local originalHandler=handler
      uiReady=false;inGameplay=false
      local uiUnits={}
      function uiUnits:FindID(id)
       if uiReady or id~=40 then return realGetUnits():FindID(id) end
       if uiMode=='missing' then return nil end
       if uiMode=='unreadable' then error('UI object not yet readable')end
       if uiMode=='wrong_id' then return unit(41)end
       if uiMode=='wrong_owner' then return unit(40,100,3)end
       if uiMode=='wrong_type' then return unit(40,103)end
       return realGetUnits():FindID(id)
      end
      function uiUnits:Members()
       if not uiReady then return pairs({}) end
       return realGetUnits():Members()
      end
      Players[2].GetUnits=function()if inGameplay then return realGetUnits()end;return uiUnits end
      local realUnits=GameInfo.Units
      GameInfo.Units=setmetatable({},{__index=function(_,key)
       if not inGameplay and not uiReady and uiMode=='missing_definition' and key==100 then return nil end
       return realUnits[key]
      end})
      handler=function(...)
       inGameplay=true;local ok,err=pcall(originalHandler,...);inGameplay=false
       if not ok then error(err)end
      end
      auditCalls=0;local originalAudit=reader.Audit
      reader.Audit=function(...)auditCalls=auditCalls+1;return originalAudit(...)end
    ''')
    return l


class NativeNameWindow(unittest.TestCase):
    def test_create_confirms_native_name_once_without_automatic_dispatch(self):
        l=gate(window=True);l.execute("""
          gateOpen();Controls.CreateButton.click()
          assert(nameCalls==0 and nativeCalls==0 and initCalls==1 and nameConfirmCalls==1)
          assert(units[40].name=='LOC_CITIZEN_TEST_A' and ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED')
          for i=1,5 do publish();if update then update(0.5)end end
          assert(nameConfirmCalls==1 and nameCalls==0 and nativeCalls==0)
          Controls.ArmButton.click();assert(nativeCalls==1 and nameCalls==0)
        """)

    def test_default_name_waits_for_native_assignment_without_command(self):
        l=gate(window=True);l.execute("""
          nativeName='LOC_TEST_DEFAULT';gateOpen();Controls.CreateButton.click()
          assert(nameCalls==0 and nativeCalls==0 and nameConfirmCalls==0)
          Controls.ArmButton.click();assert(nativeCalls==0)
          units[40].name='LOC_CITIZEN_TEST_A';if update then update(1)end;publish()
          assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED' and nameConfirmCalls==1 and nameCalls==0)
          Controls.ArmButton.click();assert(nativeCalls==1)
        """)

    def test_native_name_timeout_holds_no_retry_and_exact_team_can_end(self):
        l=gate(window=True);l.execute("""
          nativeName='LOC_TEST_DEFAULT';gateOpen();Controls.CreateButton.click();update(11);publish();Controls.ArmButton.click()
          local r=ExposedMembers.SPC_ExpeditionGateReply
          assert(r.phase=='HELD' and r.errorDetail:find('TEAM_NATIVE_NAME_TIMEOUT',1,true))
          units[40].name='LOC_CITIZEN_TEST_A';publish();Controls.RefreshButton.click()
          assert(nameCalls==0 and nativeCalls==0 and nameConfirmCalls==0 and initCalls==1)
          Controls.EndButton.click();assert(destroys==1 and properties==0)
        """)

    def test_missing_pool_blocks_creation_and_has_no_native_command(self):
        for change in ['poolRows={}', 'GameInfo.CivilizationCitizenNames=nil']:
            with self.subTest(change=change):
                l=gate(window=True);l.execute(change+";gateOpen();Controls.CreateButton.click();assert(initCalls==0 and nameCalls==0 and nativeCalls==0 and nameConfirmCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.error);assert(destroys==0 and properties==0)")

    def test_invalid_assigned_name_holds_created_team_without_command(self):
        l=gate(window=True);l.execute("nativeName='LOC_CITIZEN_OTHER';gateOpen();Controls.CreateButton.click();assert(initCalls==1 and nameCalls==0 and nativeCalls==0 and nameConfirmCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.phase=='HELD');Controls.EndButton.click();assert(destroys==1 and properties==0)")

    def test_delayed_ui_publication_waits_then_confirms_once(self):
        for mode in ['missing','unreadable']:
            with self.subTest(mode=mode):
                l=publication_window(mode);l.execute("""
                  gateOpen();Controls.CreateButton.click()
                  local v=ExposedMembers.SPC_ExpeditionGateReply
                  assert(v.phase=='NAMING' and v.sourceCity==1 and v.count==1 and initCalls==1)
                  assert(nameCalls==0 and nameConfirmCalls==0 and nativeCalls==0 and auditCalls==1 and properties==0)
                  publish();update(0.5);Controls.ArmButton.click();assert(nameConfirmCalls==0 and auditCalls==1)
                  uiReady=true;publish()
                  assert(nameConfirmCalls==1 and nameCalls==0 and nativeCalls==0 and auditCalls>=2)
                  assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED')
                  for i=1,5 do publish();if update then update(0.5)end end
                  assert(nameConfirmCalls==1 and nameCalls==0 and nativeCalls==0 and initCalls==1 and properties==0)
                  Controls.ArmButton.click();assert(nativeCalls==1 and nameCalls==0)
                """)

    def test_permanent_ui_absence_times_out_and_no_late_confirmation(self):
        l=publication_window();l.execute("""
          gateOpen();Controls.CreateButton.click();update(11)
          local v=ExposedMembers.SPC_ExpeditionGateReply
          assert(v.phase=='HELD' and v.errorDetail:find('TEAM_UI_READY_TIMEOUT:UI_UNIT_NOT_PUBLISHED',1,true))
          assert(v.sourceCity==1 and v.count==1 and nameCalls==0 and nameConfirmCalls==0 and nativeCalls==0 and initCalls==1)
          uiReady=true;publish();Controls.RefreshButton.click();Controls.ArmButton.click()
          assert(nameConfirmCalls==0 and nameCalls==0 and nativeCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.phase=='HELD')
          Controls.EndButton.click();assert(destroys==1 and properties==0)
        """)

    def test_first_ready_at_deadline_is_not_confirmed_late(self):
        l=publication_window();l.execute("""
          gateOpen();Controls.CreateButton.click();uiReady=true;update(10)
          local v=ExposedMembers.SPC_ExpeditionGateReply
          assert(v.phase=='HELD' and v.errorDetail:find('TEAM_UI_READY_TIMEOUT',1,true))
          publish();assert(nameConfirmCalls==0 and nameCalls==0 and nativeCalls==0 and initCalls==1 and properties==0)
        """)

    def test_definite_ui_mismatch_stops_without_touching_gameplay_unit(self):
        for mode,reason in [('wrong_id','UI_UNIT_ID_MISMATCH'),('wrong_owner','UI_UNIT_OWNER_MISMATCH'),('wrong_type','UI_UNIT_TYPE_MISMATCH'),('missing_definition','UI_UNIT_DEFINITION_UNAVAILABLE')]:
            with self.subTest(mode=mode):
                l=publication_window(mode);l.globals().expectedReason=reason;l.execute("""
                  gateOpen();Controls.CreateButton.click();local v=ExposedMembers.SPC_ExpeditionGateReply
                  assert(v.phase=='HELD' and v.errorDetail:find(expectedReason,1,true))
                  assert(nameConfirmCalls==0 and nameCalls==0 and nativeCalls==0 and initCalls==1 and units[40].name=='LOC_CITIZEN_TEST_A')
                  uiReady=true;publish();assert(nameConfirmCalls==0 and nameCalls==0 and nativeCalls==0)
                  Controls.EndButton.click();assert(destroys==1 and properties==0)
                """)

    def test_close_cancels_wait_and_reopen_cannot_confirm_late(self):
        l=publication_window();l.execute("""
          gateOpen();Controls.CreateButton.click();assert(update);local oldUpdate=update
          Controls.CloseButton.click();assert(not update and ContextPtr.hidden)
          uiReady=true;publish();oldUpdate(11);assert(nameConfirmCalls==0 and nameCalls==0 and nativeCalls==0 and destroys==0 and units[40])
          -- B201+: reopening re-runs one fresh exact preparation for the persisted NAMING team.
          gateOpen();assert(nameConfirmCalls==1 and nameCalls==0 and nativeCalls==0 and initCalls==1)
          assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED')
          publish();oldUpdate(11);assert(nameConfirmCalls==1 and nameCalls==0 and nativeCalls==0)
          Controls.EndButton.click();assert(destroys==1 and properties==0)
        """)

    def test_delayed_unit_then_delayed_native_assignment_preserves_both_guards(self):
        l=publication_window();l.execute("""
          nativeName='LOC_TEST_DEFAULT';gateOpen();Controls.CreateButton.click();update(5)
          assert(nameConfirmCalls==0 and nameCalls==0 and nativeCalls==0)
          uiReady=true;publish();update(5);Controls.ArmButton.click();assert(nameConfirmCalls==0 and nativeCalls==0)
          units[40].name='LOC_CITIZEN_TEST_A';publish()
          assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED' and nameConfirmCalls==1 and nameCalls==0)
          Controls.ArmButton.click();assert(nativeCalls==1 and properties==0)
        """)

    def test_synchronous_reply_publish_keeps_readiness_timeout(self):
        l=publication_window();l.execute("""
          local originalRequest=UI.RequestPlayerOperation
          UI.RequestPlayerOperation=function(...)local result=originalRequest(...);publish();return result end
          gateOpen();Controls.CreateButton.click();assert(update and nameConfirmCalls==0)
          update(11);local v=ExposedMembers.SPC_ExpeditionGateReply
          assert(v.phase=='HELD' and v.errorDetail:find('TEAM_UI_READY_TIMEOUT',1,true))
          uiReady=true;publish();Controls.RefreshButton.click();assert(nameConfirmCalls==0 and nameCalls==0 and nativeCalls==0 and initCalls==1 and properties==0)
        """)

    def test_close_inside_create_request_does_not_reinstall_cancelled_timer(self):
        l=publication_window();l.execute("""
          local originalRequest=UI.RequestPlayerOperation
          UI.RequestPlayerOperation=function(pid,op,packet)
           local result=originalRequest(pid,op,packet)
           if packet.Action=='CREATE' then Controls.CloseButton.click()end;return result
          end
          gateOpen();Controls.CreateButton.click();assert(ContextPtr.hidden and not update and nameConfirmCalls==0 and nameCalls==0 and nativeCalls==0)
          uiReady=true;publish();assert(nameConfirmCalls==0 and nameCalls==0 and nativeCalls==0 and not update)
          -- B201+: reopening re-runs one fresh exact preparation; no second packet afterwards.
          gateOpen();publish();assert(nameConfirmCalls==1 and nameCalls==0 and nativeCalls==0 and initCalls==1 and properties==0)
          assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED')
          publish();assert(nameConfirmCalls==1);Controls.EndButton.click();assert(destroys==1)
        """)

    def test_publish_reentrant_during_name_confirmation_never_sends_second_packet(self):
        l=publication_window();l.execute("""
          local originalRequest=UI.RequestPlayerOperation
          UI.RequestPlayerOperation=function(pid,op,packet)
           if packet.Action=='NAME' then publish()end
           return originalRequest(pid,op,packet)
          end
          gateOpen();Controls.CreateButton.click();uiReady=true;publish()
          assert(nameConfirmCalls==1 and nameCalls==0 and nativeCalls==0 and initCalls==1)
          assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED')
          publish();Controls.ArmButton.click();assert(nameConfirmCalls==1 and nameCalls==0 and nativeCalls==1)
        """)


if __name__=='__main__':unittest.main()
