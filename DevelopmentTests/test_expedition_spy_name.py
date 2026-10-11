"""B188 UI publication readiness and B187 controlled-name continuity against actual Lua.
Mock command acceptance/readback is local evidence, not native rename/travel proof.
Inherited tests use a successful-name fixture; these explicitly bypass it with rawreq.
"""
import unittest
from test_expedition_spy_gate import gate


class NamePreparation(unittest.TestCase):
    def test_create_is_unready_and_readback_is_required_before_dispatch(self):
        l=gate();l.execute("""
          local r=rawreq('CREATE','a')
          assert(r.phase=='NAMING' and not r.bound and r.expectedName and r.teamKey and r.sourceCity==1 and properties==0)
          local expected=r.expectedName
          r=nativeDispatch('early');assert(r.error and not r.nativePermit and r.phase=='NAMING')
          r=rawreq('READ','wait');assert(r.phase=='NAMING' and not r.bound)
          units[40].name=expected
          r=rawreq('READ','verified');assert(r.phase=='CREATED' and r.bound and r.expectedName==expected)
          assert(nativeDispatch('ready').nativePermit=='ready' and properties==0 and nativeCalls==0)
        """)

    def test_source_current_id_and_location_still_required_for_initial_readback(self):
        for change in ['city.token=nil','city.token="other"','city.owner=3','units[40].owner=3','units[40].type_=103','units[40].id=41','units[40].x=2']:
            with self.subTest(change=change):
                l=gate();l.execute("local r=rawreq('CREATE','a');units[40].name=r.expectedName;"+change+";r=rawreq('READ','r');assert(r.phase=='HELD' and not r.bound and r.count==1 and initCalls==1 and properties==0 and destroys==0)")

    def test_nil_wrong_and_unreadable_names_never_count_as_verified(self):
        for change in ['units[40].name=nil','units[40].name="wrong"','units[40].GetName=nil',"units[40].GetName=function()error('unknown name')end"]:
            with self.subTest(change=change):
                l=gate();l.execute("rawreq('CREATE','a');"+change+";local r=rawreq('READ','r');assert(not r.bound and r.phase~='CREATED');assert(not nativeDispatch('d').nativePermit and properties==0 and initCalls==1)")

    def test_source_label_is_display_only_and_source_reference_stays_separate(self):
        l=gate();l.execute("""
          local r=req('CREATE','a');local expected=r.expectedName
          city.GetName=function()return '新名字' end
          r=req('READ','b');assert(r.bound and r.expectedName==expected and r.sourceCity==1)
          city.token='new-city-same-name';r=req('READ','c');assert(not r.bound and r.phase=='HELD')
        """)

    def test_key_fresh_after_end_even_with_reused_native_id(self):
        l=gate();l.execute("""
          local a=req('CREATE','a');local key=a.teamKey;local name=a.expectedName
          req('END','b',40);local b=req('CREATE','c')
          assert(b.phase=='CREATED' and b.unitID==40 and b.teamKey~=key and b.expectedName~=name and initCalls==2 and properties==0)
        """)

    def test_long_unicode_label_keeps_whole_key_and_valid_bounded_name(self):
        l=gate();l.execute("""
          city.GetName=function()return string.rep('长城港湾',40) end
          local r=rawreq('CREATE','a')
          assert(r.phase=='NAMING' and utf8.len(r.expectedName) and utf8.len(r.expectedName)<=48)
          assert(r.expectedName:find(r.teamKey,1,true) and #r.teamKey>0)
        """)

    def test_after_verification_name_mutation_holds_without_relabel_or_recreate(self):
        l=gate();l.execute("req('CREATE','a');units[40].name='unexpected';local r=req('READ','r');assert(r.phase=='HELD' and not r.bound and properties==0 and initCalls==1 and destroys==0);req('CREATE','again');assert(initCalls==1)")

    def test_controlled_name_survives_without_any_unit_properties(self):
        l=gate();l.execute("""
          local r=req('CREATE','a');local name=r.expectedName;nativeDispatch('b')
          units[40]=nil;units[41]=unit(41,100,2,15,8);units[41].name=name
          units[41].GetProperty=nil;units[41].SetProperty=nil
          currentTurn=83;ownTurn(2);r=req('READ','c')
          assert(r.phase=='ARRIVED' and r.bound and r.unitID==41 and r.sourceCity==1 and properties==0)
        """)


class NameCommand(unittest.TestCase):
    def test_exact_custom_unit_renamed_once_and_raw_readback_returned(self):
        l=gate(ui=True);l.execute("""
          units[7]=unit(7,103);local r=rawreq('CREATE','a')
          UI={GetHeadSelectedUnit=function()return units[7]end}
          local ok,status=reader.SubmitName(2,40,r.expectedName,'name-one')
          assert(ok and nameCalls==1 and lastNamedID==40 and units[40]:GetName()==r.expectedName and units[7]:GetName()=='Native Spy')
          assert(not reader.SubmitName(2,40,r.expectedName,'name-one') and nameCalls==1)
          assert(rawreq('READ','ready').phase=='CREATED' and nativeCalls==0 and properties==0)
        """)

    def test_delayed_readback_is_pending_and_never_resubmits_command(self):
        l=gate(ui=True);l.execute("""
          local r=rawreq('CREATE','a');nameDelayed=true
          local ok,status=reader.SubmitName(2,40,r.expectedName,'name-one')
          assert(ok and status=='NAME_PENDING' and nameCalls==1)
          assert(rawreq('READ','wait').phase=='NAMING')
          assert(not reader.SubmitName(2,40,r.expectedName,'name-one') and nameCalls==1)
          units[40].name=requestedName
          assert(rawreq('READ','ready').phase=='CREATED' and nativeCalls==0)
        """)

    def test_capability_native_permission_missing_api_and_wrong_unit_block_command(self):
        for change in ['renameCapability=false','nameAllow=false','UnitManager.CanStartCommand=nil','UnitManager.RequestCommand=nil','UnitCommandTypes.NAME_UNIT=nil','units[40].owner=3','units[40].type_=103','units[40].id=41']:
            with self.subTest(change=change):
                l=gate(ui=True);l.execute("local r=rawreq('CREATE','a');"+change+";assert(not reader.SubmitName(2,40,r.expectedName,'name-one') and nameCalls==0 and nativeCalls==0 and properties==0)")

    def test_request_false_or_throw_consumes_permit_without_blind_retry(self):
        for change in ['nameFalse=true','nameThrow=true']:
            with self.subTest(change=change):
                l=gate(ui=True);l.execute("local r=rawreq('CREATE','a');"+change+";assert(not reader.SubmitName(2,40,r.expectedName,'name-one'));assert(not reader.SubmitName(2,40,r.expectedName,'name-one') and nameCalls==1 and nativeCalls==0 and properties==0)")

    def test_invalid_name_or_permit_cannot_issue_command(self):
        for name,permit in [('nil',"'ok'"),("''","'ok'"),("'name'",'nil'),("'name'","''")]:
            with self.subTest(name=name,permit=permit):
                l=gate(ui=True);l.execute("rawreq('CREATE','a');assert(not reader.SubmitName(2,40,"+name+","+permit+") and nameCalls==0)")


class NameWindow(unittest.TestCase):
    def test_create_names_and_verifies_without_automatic_dispatch(self):
        l=gate(window=True);l.execute("""
          gateOpen();Controls.CreateButton.click()
          assert(nameCalls==1 and nativeCalls==0 and initCalls==1 and units[40].name==requestedName)
          assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED' and Controls.Report.text:find('PHASE_CREATED'))
          Controls.ArmButton.click();assert(nativeCalls==1 and nameCalls==1)
        """)

    def test_async_rename_completes_bounded_readback_without_auto_dispatch(self):
        l=gate(window=True);l.execute("""
          nameDelayed=true;gateOpen();Controls.CreateButton.click();assert(nameCalls==1 and nativeCalls==0)
          Controls.ArmButton.click();assert(nativeCalls==0)
          units[40].name=requestedName
          if update then update(1)end;publish()
          assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED' and nameCalls==1 and nativeCalls==0)
          Controls.ArmButton.click();assert(nativeCalls==1 and nameCalls==1)
        """)

    def test_async_rename_timeout_holds_and_does_not_retry_or_dispatch(self):
        l=gate(window=True);l.execute("""
          nameDelayed=true;gateOpen();Controls.CreateButton.click();assert(nameCalls==1)
          if update then update(11)end;publish();Controls.ArmButton.click()
          assert(nativeCalls==0 and nameCalls==1 and ExposedMembers.SPC_ExpeditionGateReply.phase=='HELD')
          Controls.RefreshButton.click();assert(nameCalls==1 and nativeCalls==0)
          Controls.EndButton.click();assert(destroys==1)
        """)

    def test_rejected_name_is_readable_stop_and_existing_team_can_end(self):
        for change in ['nameAllow=false','nameFalse=true','nameThrow=true','renameCapability=false']:
            with self.subTest(change=change):
                l=gate(window=True);l.execute(change+";gateOpen();Controls.CreateButton.click();assert(initCalls==1 and nativeCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.phase=='HELD');Controls.ArmButton.click();assert(nativeCalls==0);Controls.EndButton.click();assert(destroys==1 and properties==0)")


def publication_window(mode='missing'):
    """Actual Gate/Read/Window with distinct Gameplay and UI unit publication.
    Only the UI view is delayed or invalid; the created Gameplay unit stays exact.
    """
    l=gate(window=True)
    l.globals().uiMode=mode
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
      Players[2].GetUnits=function()
       if inGameplay then return realGetUnits()end
       return uiUnits
      end
      local realUnits=GameInfo.Units
      GameInfo.Units=setmetatable({},{__index=function(_,key)
       if not inGameplay and not uiReady and uiMode=='missing_definition' and key==100 then return nil end
       return realUnits[key]
      end})
      handler=function(...)
       inGameplay=true
       local ok,err=pcall(originalHandler,...)
       inGameplay=false
       if not ok then error(err)end
      end
      auditCalls=0
      local originalAudit=reader.Audit
      reader.Audit=function(...)
       auditCalls=auditCalls+1
       return originalAudit(...)
      end
    ''')
    return l


class NameReadiness(unittest.TestCase):
    def test_readiness_is_read_only_and_requires_exact_custom_identity(self):
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


class NamePublicationWindow(unittest.TestCase):
    def test_delayed_ui_publication_waits_then_names_exactly_once_without_dispatch(self):
        for mode in ['missing','unreadable']:
            with self.subTest(mode=mode):
                l=publication_window(mode);l.execute("""
                  gateOpen();Controls.CreateButton.click()
                  local v=ExposedMembers.SPC_ExpeditionGateReply
                  assert(v.phase=='NAMING' and v.sourceCity==1 and v.count==1 and initCalls==1)
                  assert(nameCalls==0 and nativeCalls==0 and auditCalls==1 and properties==0)
                  publish();update(0.5);Controls.ArmButton.click()
                  assert(nameCalls==0 and nativeCalls==0 and auditCalls==1)
                  uiReady=true;publish()
                  assert(nameCalls==1 and nativeCalls==0 and lastNamedID==40 and auditCalls>=2)
                  assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED')
                  for i=1,5 do publish();if update then update(0.5)end end
                  assert(nameCalls==1 and nativeCalls==0 and initCalls==1 and properties==0)
                  Controls.ArmButton.click();assert(nativeCalls==1 and nameCalls==1)
                """)

    def test_permanent_ui_absence_times_out_with_no_rename_and_no_late_retry(self):
        l=publication_window();l.execute("""
          gateOpen();Controls.CreateButton.click();update(11)
          local v=ExposedMembers.SPC_ExpeditionGateReply
          assert(v.phase=='HELD' and v.errorDetail:find('TEAM_UI_READY_TIMEOUT:UI_UNIT_NOT_PUBLISHED',1,true))
          assert(v.sourceCity==1 and v.count==1 and nameCalls==0 and nativeCalls==0 and initCalls==1)
          uiReady=true;publish();Controls.RefreshButton.click();Controls.ArmButton.click()
          assert(nameCalls==0 and nativeCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.phase=='HELD')
          Controls.EndButton.click();assert(destroys==1 and properties==0)
        """)

    def test_ui_first_ready_at_deadline_does_not_issue_a_late_name_command(self):
        l=publication_window();l.execute("""
          gateOpen();Controls.CreateButton.click()
          uiReady=true;update(10)
          local v=ExposedMembers.SPC_ExpeditionGateReply
          assert(v.phase=='HELD' and v.errorDetail:find('TEAM_UI_READY_TIMEOUT',1,true))
          publish();assert(nameCalls==0 and nativeCalls==0 and initCalls==1 and properties==0)
        """)

    def test_definite_ui_mismatch_stops_immediately_without_renaming_gameplay_unit(self):
        for mode,reason in [
            ('wrong_id','UI_UNIT_ID_MISMATCH'),
            ('wrong_owner','UI_UNIT_OWNER_MISMATCH'),
            ('wrong_type','UI_UNIT_TYPE_MISMATCH'),
            ('missing_definition','UI_UNIT_DEFINITION_UNAVAILABLE'),
        ]:
            with self.subTest(mode=mode):
                l=publication_window(mode);l.globals().expectedReason=reason
                l.execute("""
                  gateOpen();Controls.CreateButton.click()
                  local v=ExposedMembers.SPC_ExpeditionGateReply
                  assert(v.phase=='HELD' and v.errorDetail:find(expectedReason,1,true))
                  assert(nameCalls==0 and nativeCalls==0 and initCalls==1 and units[40].name=='Native Spy')
                  uiReady=true;publish();assert(nameCalls==0 and nativeCalls==0)
                  Controls.EndButton.click();assert(destroys==1 and properties==0)
                """)

    def test_close_cancels_wait_and_publish_or_reopen_cannot_send_late_name_command(self):
        l=publication_window();l.execute("""
          gateOpen();Controls.CreateButton.click();assert(update)
          local oldUpdate=update
          Controls.CloseButton.click();assert(not update and ContextPtr.hidden)
          uiReady=true;publish();oldUpdate(11)
          assert(nameCalls==0 and nativeCalls==0 and destroys==0 and units[40])
          gateOpen();publish();assert(nameCalls==0 and nativeCalls==0 and initCalls==1)
          assert(Controls.Report.text:find('NAME_STAGE_CANCELLED',1,true))
          Controls.EndButton.click();assert(destroys==1 and properties==0)
        """)

    def test_delayed_unit_then_delayed_name_preserves_both_guards(self):
        l=publication_window();l.execute("""
          nameDelayed=true;gateOpen();Controls.CreateButton.click();update(5)
          assert(nameCalls==0 and nativeCalls==0)
          uiReady=true;publish();assert(nameCalls==1 and nativeCalls==0)
          update(5);Controls.ArmButton.click();assert(nativeCalls==0)
          units[40].name=requestedName;publish()
          assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED' and nameCalls==1)
          Controls.ArmButton.click();assert(nativeCalls==1 and properties==0)
        """)

    def test_synchronous_reply_publish_keeps_readiness_timeout_and_never_renames_late(self):
        l=publication_window();l.execute("""
          local originalRequest=UI.RequestPlayerOperation
          UI.RequestPlayerOperation=function(...)
           local result=originalRequest(...)
           publish()
           return result
          end
          gateOpen();Controls.CreateButton.click();assert(update and nameCalls==0)
          update(11)
          local v=ExposedMembers.SPC_ExpeditionGateReply
          assert(v.phase=='HELD' and v.errorDetail:find('TEAM_UI_READY_TIMEOUT',1,true))
          uiReady=true;publish();Controls.RefreshButton.click()
          assert(nameCalls==0 and nativeCalls==0 and initCalls==1 and properties==0)
        """)

    def test_close_inside_gameplay_request_does_not_reinstall_cancelled_timer(self):
        l=publication_window();l.execute("""
          local originalRequest=UI.RequestPlayerOperation
          UI.RequestPlayerOperation=function(pid,op,packet)
           local result=originalRequest(pid,op,packet)
           if packet.Action=='CREATE' then Controls.CloseButton.click()end
           return result
          end
          gateOpen();Controls.CreateButton.click()
          assert(ContextPtr.hidden and not update and nameCalls==0 and nativeCalls==0)
          uiReady=true;publish();gateOpen();publish()
          assert(nameCalls==0 and nativeCalls==0 and initCalls==1 and properties==0)
          assert(Controls.Report.text:find('NAME_STAGE_CANCELLED',1,true))
          Controls.EndButton.click();assert(destroys==1)
        """)

    def test_publish_reentrant_during_name_request_never_sends_second_command(self):
        l=publication_window();l.execute("""
          local originalNameRequest=UnitManager.RequestCommand
          UnitManager.RequestCommand=function(...)
           publish()
           return originalNameRequest(...)
          end
          gateOpen();Controls.CreateButton.click();uiReady=true;publish()
          assert(nameCalls==1 and nativeCalls==0 and initCalls==1)
          assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED')
          publish();Controls.ArmButton.click();assert(nameCalls==1 and nativeCalls==1)
        """)


if __name__=='__main__':unittest.main()
