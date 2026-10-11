"""B187 controlled-name preparation and continuity delta against the actual Lua.
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


if __name__=='__main__':unittest.main()
