"""B182: actual Spy=0 gate, independent timer/binding and database checks.
Native placement/coexistence remain unproved by local mocks.
Run with the project's Lua55/Lupa environment and explicit read-only HD DB path.
"""
from pathlib import Path
import re, sqlite3, unittest, zlib, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from project_paths import external_database
R=Path(__file__).resolve().parents[1]

class Gate(unittest.TestCase):
    def runtime(self):
        l=LuaRuntime(unpack_returned_tuples=True)
        l.execute(r'''
          kind='UNIT_SPC_EXPEDITION_ZERO'; currentTurn=81; initCalls=0; destroys=0; properties=0;placeCalls=0;finishCalls=0
          function event()return {listeners={},Add=function(self_or_fn)end}end
          Game={GetCurrentGameTurn=function()return currentTurn end}
          Events={UnitRemovedFromMap={Add=function(fn)removed=fn end},PlayerTurnActivated={Add=function(fn)ownTurn=fn end},CityTransfered={Add=function(fn)transfer=fn end}}
          GameEvents={SPC_ExpeditionGateRequest={Add=function(fn)handler=fn end}}
          ExposedMembers={};shared={}
          info={[100]={UnitType=kind,Spy=false,CanRetreatWhenCaptured=false,IgnoreMoves=true,Stackable=true,FormationClass='FORMATION_CLASS_CIVILIAN'},
                [101]={UnitType='UNIT_SETTLER',Spy=false,FormationClass='FORMATION_CLASS_CIVILIAN'}}
          info[kind]=info[100];info[102]={UnitType='UNIT_SPC_EXPEDITION_GATE',Spy=false}
          units={}; foreignUnits={};cities={};spyCapacity=2
          function unit(id,type_,owner,x,y)
           local u={id=id,type_=type_ or 100,owner=owner or 2,x=x or 1,y=y or 1}
           function u:GetID()return self.id end;function u:GetType()return self.type_ end;u.GetUnitType=u.GetType
           function u:GetOwner()return self.owner end;function u:GetX()return self.x end;function u:GetY()return self.y end
           function u:SetProperty()properties=properties+1;error('Unexpected property write')end
           return u
          end
          city={id=1,owner=2,x=1,y=1,token='source-token'}
          function city:GetProperty()return self.token end
          function city:GetID()return self.id end;function city:GetOwner()return self.owner end
          function city:GetX()return self.x end;function city:GetY()return self.y end
          function city:GetName()return '文化城' end
          cities[1]=city
          active=4;spec='CULTURE';pending=false
          shared.EffectiveFacts={Read=function(pid,c)if factsError then error('UNKNOWN_FACTS')end
            return {specialization=spec,active=active,investmentPending=pending,token=city.token}end}
          local us={}
          function us:Members()return pairs(units)end;function us:FindID(id)return units[id]end
          function us:Destroy(u)destroys=destroys+1;if not destroyFail then units[u.id]=nil;if removed then removed(u.owner,u.id)end end end
          local cs={FindID=function(self,id)return cities[id]end}
          Players={[2]={GetUnits=function()return us end,GetCities=function()return cs end,
            GetDiplomacy=function()return {HasMet=function()return met~=false end}end}}
          targetCity={id=9,owner=3,x=15,y=8}
          function targetCity:GetID()return self.id end;function targetCity:GetOwner()return self.owner end
          function targetCity:GetX()return self.x end;function targetCity:GetY()return self.y end
          function targetCity:GetName()return '目标城' end;function targetCity:IsCapital()return capital~=false end
          Players[3]={IsMajor=function()return major~=false end,IsAlive=function()return alive~=false end,
            GetUnits=function()return {FindID=function(self,id)return foreignUnits[id]end}end,
            GetCities=function()return {FindID=function(self,id)if id==targetCity.id then return targetCity end end}end}
          PlayersVisibility={[2]={IsRevealed=function()return visible~=false end}}
          Units={GetUnitsInPlot=function(x,y)
            local o={};for _,collection in ipairs({units,foreignUnits})do for _,u in pairs(collection)do
              if u.x==x and u.y==y then o[#o+1]=u end
            end end;return o end}
          P={IsTestPlayer=function(pid)return pid==2 end,Info=function(name,id)return info[id]end}
          UnitManager={InitUnit=function(pid,k,x,y)
            initCalls=initCalls+1
            if reentrant then handler(pid,{Action='CREATE',Token='reentrant',CityID=1})end
            if initThrowBefore then error('INIT_FAILURE')end
            local u=unit(40,100,pid,x,y);units[u.id]=u
            if initThrowAfter then error('INIT_FAILURE_AFTER')end
            if initNil then return nil end
            if wrongOwner then u.owner=3 end
            return u
          end,
            FinishMoves=function(u)finishCalls=finishCalls+1;if finishError then error('FINISH_ERROR')end;u.moves=0 end,
            RestoreMovement=function(u)u.moves=4 end,
            PlaceUnit=function(u,x,y)
              placeCalls=placeCalls+1
              if placeThrow then error('PLACE_FAILED')end
              if placeNoop then return end
              if displaceOther and foreignUnits[7]then foreignUnits[7].x=16 end
              u.x=x;u.y=y;if wrongArrival then u.x=x+1 end
              if removeArrival then units[u.id]=nil end
              if placeReentrant then ownTurn(2)end
            end}
          function dispatch(token,overrides)
            local p={Action='DISPATCH',Token=token,UnitID=40,SampleTurn=currentTurn,FromX=1,FromY=1,
              TargetOwner=3,TargetID=9,TargetX=15,TargetY=8,Travel=2,Establish=0,NativeAllowed=false,NativeStatus='KNOWN'}
            for k,v in pairs(overrides or {})do p[k]=v end;handler(2,p);return ExposedMembers.SPC_ExpeditionGateReply
          end
          function req(action,token,id,cityID,pid)
            handler(pid or 2,{Action=action,Token=token,UnitID=id,CityID=cityID or 1})
            return ExposedMembers.SPC_ExpeditionGateReply
          end
        ''')
        l.execute((R/'Mod/NetworkInput.lua').read_text())
        l.execute((R/'Mod/ExpeditionGate.lua').read_text())
        l.execute('SPCExpeditionGate.Start(P,shared)')
        return l
    def test_load_and_read_have_no_writes(self):
        l=self.runtime();l.execute("local r=req('READ','a');assert(r.count==0 and initCalls==0 and properties==0 and destroys==0)")
    def test_explicit_create_nonzero_human_and_duplicate_token(self):
        l=self.runtime();l.execute("req('CREATE','a');req('CREATE','a');assert(initCalls==1 and req('READ','b').unitID==40 and properties==0)")
    def test_second_live_team_rejected(self):
        l=self.runtime();l.execute("req('CREATE','a');req('CREATE','b');assert(initCalls==1 and ExposedMembers.SPC_ExpeditionGateReply.error=='EXISTING_TEST_TEAM_COUNTS')")
    def test_external_gate_unit_counts_including_after_reload(self):
        l=self.runtime();l.execute("units[8]=unit(8);req('CREATE','a');assert(initCalls==0);assert(req('READ','b').unitID==8)")
    def test_qualification_unknown_foreign_pending_not_granted(self):
        for change in ('active=3','active=nil','spec="RESEARCH"','pending=true','factsError=true','city.owner=3','cities[1]=nil'):
            with self.subTest(change=change):
                l=self.runtime();l.execute(change+";req('CREATE','a');assert(initCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.error)")
    def test_occupied_city_center_preserves_ordinary_unit(self):
        l=self.runtime();l.execute("units[5]=unit(5,101);local r=req('CREATE','a');assert(initCalls==1 and r.phase=='CREATED' and r.coLocated==1 and units[5].x==1)")
    def test_unsupported_player_and_malformed_request(self):
        l=self.runtime();l.execute("handler(3,{Action='CREATE',Token='a',CityID=1});handler(2,{});handler(2,{Token=string.rep('a',101)});assert(initCalls==0 and ExposedMembers.SPC_ExpeditionGateReply==nil)")
    def test_bad_database_flags(self):
        for change in ('info[100].Spy=true','info[100].Spy=nil','info[100].CanRetreatWhenCaptured=true','info[100].IgnoreMoves=false','info[100].Stackable=false','info[100].PromotionClass="PROMOTION_CLASS_SPY"','info[kind]=nil'):
            with self.subTest(change=change):
                l=self.runtime();l.execute(change+";req('CREATE','a');assert(initCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.error)")
    def test_native_spawn_uncertainty_locks_retry(self):
        for change in ('initNil=true','initThrowBefore=true','initThrowAfter=true','wrongOwner=true'):
            with self.subTest(change=change):
                l=self.runtime();l.execute(change+";req('CREATE','a');assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='HELD');req('CREATE','b');assert(initCalls==1 and shared.RequestDepth==0)")
    def test_reentrancy_cannot_spawn_twice(self):
        l=self.runtime();l.execute("reentrant=true;req('CREATE','a');assert(initCalls==1 and shared.RequestDepth==0)")
    def test_qualification_decline_does_not_delete_test_unit(self):
        l=self.runtime();l.execute("req('CREATE','a');active=1;spec='REALLOCATING';req('READ','b');assert(units[40] and destroys==0)")
    def test_unrequested_displacement_stops_no_corrective_teleport(self):
        l=self.runtime();l.execute("req('CREATE','a');units[40].x=9;local r=req('READ','b');assert(r.phase=='HELD' and r.stop=='TEAM_DISPLACED_STOP' and placeCalls==0 and destroys==0)")
    def test_missing_unit_never_respawned_by_read_or_event(self):
        l=self.runtime();l.execute("req('CREATE','a');removed(3,40);units[40]=nil;removed(2,40);local r=req('READ','c');assert(not r.sameUnit and r.removedEvents==1 and initCalls==1 and r.phase=='HELD')")
    def test_changed_owner_type_not_owned_cleanup_target(self):
        for change in ('units[40].owner=3','units[40].type_=101'):
            with self.subTest(change=change):
                l=self.runtime();l.execute("req('CREATE','a');"+change+";req('END','b',40);assert(destroys==0 and ExposedMembers.SPC_ExpeditionGateReply.error=='TEST_TEAM_CHANGED')")
    def test_end_exact_unit_only_and_repeated_request(self):
        l=self.runtime();l.execute("req('CREATE','a');units[4]=unit(4,101,2,8,8);req('END','b',40);req('END','b',40);assert(destroys==1 and units[4] and not units[40] and properties==0)")
    def test_end_failure_reported_without_success(self):
        l=self.runtime();l.execute("req('CREATE','a');destroyFail=true;req('END','b',40);assert(ExposedMembers.SPC_ExpeditionGateReply.error=='END_UNCONFIRMED' and units[40])")

    def test_independent_timer_exact_arrival_source_cap_and_no_repeat(self):
        l=self.runtime();l.execute("req('CREATE','a');dispatch('b');currentTurn=82;ownTurn(2);assert(placeCalls==0 and units[40].x==1);currentTurn=83;placeReentrant=true;ownTurn(2);ownTurn(2);local r=req('READ','c');assert(placeCalls==1 and r.phase=='ARRIVED' and r.unitID==40 and r.x==15 and r.y==8 and r.sourceCity==1 and r.count==1 and properties==0 and shared.RequestDepth==0)")
    def test_duplicate_dispatch_does_not_cancel_accepted_journey(self):
        l=self.runtime();l.execute("req('CREATE','a');dispatch('b');dispatch('b');local r=dispatch('c');assert(r.phase=='TRAVELLING' and r.error=='BOUND_TEAM_REQUIRED');currentTurn=83;ownTurn(2);assert(placeCalls==1)")
    def test_foreign_turn_does_not_advance_or_touch_unit(self):
        l=self.runtime();l.execute("req('CREATE','a');dispatch('b');local n=finishCalls;currentTurn=83;ownTurn(3);assert(placeCalls==0 and finishCalls==n)")
    def test_wrong_or_stale_sample_rejected_without_changing_bound_state(self):
        for change in ('SampleTurn=80','FromX=2','TargetID=8','TargetOwner=2','TargetX=14','Travel=-1','Travel=0/0','Travel=0.2','Travel=1001','Establish="x"'):
            with self.subTest(change=change):
                l=self.runtime();l.execute("req('CREATE','a');local r=dispatch('b',{"+change+"});assert(r.error and r.phase=='CREATED' and placeCalls==0)")
    def test_native_operation_rejection_does_not_block_own_zero_time_dispatch(self):
        l=self.runtime();l.execute("req('CREATE','a');local r=dispatch('b',{Travel=0});assert(r.phase=='ARRIVED' and r.nativeAllowed==false and placeCalls==1)")
    def test_arrival_preserves_occupied_target(self):
        l=self.runtime();l.execute("foreignUnits[7]=unit(7,101,3,15,8);req('CREATE','a');dispatch('b');currentTurn=83;ownTurn(2);local r=req('READ','c');assert(r.phase=='ARRIVED' and r.coLocated==1 and r.arrivalOthers==1 and foreignUnits[7].x==15)")
    def test_native_placement_failure_held_no_retry_or_respawn(self):
        for change in ('placeThrow=true','placeNoop=true','wrongArrival=true','removeArrival=true','displaceOther=true','UnitManager.PlaceUnit=nil'):
            with self.subTest(change=change):
                l=self.runtime();l.execute("foreignUnits[7]=unit(7,101,3,15,8);req('CREATE','a');dispatch('b');"+change+";currentTurn=83;ownTurn(2);local n=placeCalls;ownTurn(2);local r=req('READ','c');assert(r.phase=='HELD' and placeCalls==n and initCalls==1)")
    def test_source_loss_or_token_uncertainty_retains_team_blocks_dispatch(self):
        for change in ('city.owner=3','city.token=nil','city.token="replacement"','cities[1]=nil'):
            with self.subTest(change=change):
                l=self.runtime();l.execute("req('CREATE','a');dispatch('b');"+change+";transfer();currentTurn=83;ownTurn(2);local r=req('READ','c');assert(r.phase=='HELD' and units[40] and placeCalls==0 and properties==0)")
    def test_target_change_unknown_no_guessed_replacement(self):
        for change in ('targetCity.owner=4','targetCity.x=16','capital=false','alive=false','met=false','visible=false'):
            with self.subTest(change=change):
                l=self.runtime();l.execute("req('CREATE','a');dispatch('b');"+change+";currentTurn=83;ownTurn(2);assert(req('READ','c').phase=='HELD' and placeCalls==0 and units[40])")
    def test_active_decline_during_journey_preserves_binding_and_arrival(self):
        l=self.runtime();l.execute("req('CREATE','a');dispatch('b');active=1;spec='REALLOCATING';currentTurn=83;ownTurn(2);assert(req('READ','c').phase=='ARRIVED' and properties==0)")
    def test_source_token_required_before_spawn(self):
        l=self.runtime();l.execute("city.token=nil;req('CREATE','a');assert(initCalls==0)")
    def test_loaded_unit_is_cleanup_only_and_counts_against_cap(self):
        l=self.runtime();l.execute("units[8]=unit(8);local r=req('READ','a');assert(r.unbound and r.count==1);req('CREATE','b');assert(initCalls==0);dispatch('c',{UnitID=8});assert(placeCalls==0);req('END','d',8);assert(destroys==1)")
    def test_legacy_type_keeps_own_definition_and_explicit_cleanup(self):
        l=self.runtime();l.execute("units[8]=unit(8,102);assert(req('READ','a').legacy);req('CREATE','b');assert(initCalls==0);req('END','c',8);assert(destroys==1)")
    def test_finish_error_after_dispatch_locks_no_automatic_retry(self):
        l=self.runtime();l.execute("req('CREATE','a');finishError=true;assert(dispatch('b').phase=='HELD');finishError=false;currentTurn=83;ownTurn(2);assert(placeCalls==0)")

class Reader(unittest.TestCase):
    def runtime(self):
        l=Gate().runtime()
        l.execute(r'''
          unitID=40;units[40]=unit(40);helperCalls=0
          GameInfo={Units=info};PlayersVisibility={[2]={IsRevealed=function()return visible~=false end}}
          targetCity={id=9,owner=3,x=15,y=8}
          function targetCity:GetID()return self.id end;function targetCity:GetOwner()return self.owner end
          function targetCity:GetX()return self.x end;function targetCity:GetY()return self.y end
          function targetCity:GetName()return '目标首都' end;function targetCity:IsCapital()return capital~=false end
          major=true;alive=true;met=true
          Players[3]={IsMajor=function()return major end,IsAlive=function()return alive end,
            GetUnits=function()return {FindID=function(self,id)return foreignUnits[id]end}end,
            GetCities=function()return {FindID=function(self,id)if id==9 then return targetCity end end,GetCapitalCity=function()return targetCity end}end}
          Players[2].GetDiplomacy=function()return {HasMet=function(self,p)return met end,GetSpyCapacity=function()return spyCapacity end}end
          UnitManager.GetTravelTime=function(u,c)helperCalls=helperCalls+1;return travelValue or 3 end
          UnitManager.GetEstablishInCityTime=function(u,c)helperCalls=helperCalls+1;return establishValue or 1 end
          target={owner=3,id=9,name='目标首都',x=15,y=8}
          UnitOperationTypes={SPY_TRAVEL_NEW_CITY=8,PARAM_X='X',PARAM_Y='Y'};Map={GetPlot=function(x,y)return {x=x,y=y}end}
          UnitManager.CanStartOperation=function(u,op,plot,params)assert(op==8 and plot.x==params.X and plot.y==params.Y);return nativeAllow==true end
        ''')
        l.execute((R/'Mod/ExpeditionGateRead.lua').read_text());l.execute('reader=SPCExpeditionGateRead')
        return l
    def test_query_scalar_result_never_deployment_pass(self):
        l=self.runtime();l.execute("local r=reader.Read(2,40,target);assert(r.status=='READ_OK' and r.travel==3 and r.establish==1 and r.total==4 and helperCalls==2 and r.deployed==nil and r.nativePass==nil and r.spyBefore==2 and r.spyAfter==2)")
    def test_target_list_capital_only(self):
        l=self.runtime();l.execute("assert(#reader.Targets(2)==1);capital=false;assert(#reader.Targets(2)==0)")
    def test_invalid_unmet_minor_dead_changed_unrevealed_rejected(self):
        for change in ('met=false','major=false','alive=false','capital=false','visible=false','targetCity.owner=4','targetCity.x=16','target.id=8'):
            with self.subTest(change=change):
                l=self.runtime();l.execute(change+";local r=reader.Read(2,40,target);assert(r.status=='UNKNOWN' and r.error and helperCalls==0)")
    def test_war_and_alliance_are_not_filters(self):
        l=self.runtime();l.execute("Players[2].GetDiplomaticAI=function()error('must not filter diplomatic state')end;assert(reader.Read(2,40,target).status=='READ_OK')")
    def test_spy_or_wrong_owner_never_used_as_fallback(self):
        for change in ('info[100].Spy=true','units[40].owner=3','units[40].type_=101','units[40]=nil'):
            with self.subTest(change=change):
                l=self.runtime();l.execute(change+";assert(reader.Read(2,40,target).status=='UNKNOWN' and helperCalls==0)")
    def test_unavailable_exception_and_invalid_numbers_remain_unknown(self):
        for change in ('UnitManager.GetTravelTime=nil','UnitManager.GetTravelTime=function()error("native rejected")end','travelValue=-1','travelValue=0/0','travelValue=math.huge','travelValue=0.5','establishValue="2"'):
            with self.subTest(change=change):
                l=self.runtime();l.execute(change+";assert(reader.Read(2,40,target).status=='UNKNOWN')")
    def test_zero_not_changed_to_guessed_minimum(self):
        l=self.runtime();l.execute("travelValue=0;establishValue=0;assert(reader.Read(2,40,target).total==0)")
    def test_capacity_unknown_not_guessed(self):
        l=self.runtime();l.execute("spyCapacity=nil;local r=reader.Read(2,40,target);assert(r.status=='READ_OK' and r.spyBefore==nil and r.spyAfter==nil)")
    def test_unit_changed_during_read_not_accepted(self):
        l=self.runtime();l.execute("UnitManager.GetTravelTime=function(u,c)u.x=99;return 4 end;assert(reader.Read(2,40,target).status=='UNKNOWN')")

    def test_native_permission_is_separate_and_never_executes(self):
        l=self.runtime();l.execute("local r=reader.Read(2,40,target);assert(r.nativeStatus=='KNOWN' and r.nativeAllowed==false and r.status=='READ_OK');nativeAllow=true;assert(reader.Read(2,40,target).nativeAllowed==true)")
    def test_unknown_permission_keeps_valid_timing_without_claiming_rejection(self):
        for change in ('UnitManager.CanStartOperation=nil','UnitManager.CanStartOperation=function()error("no native support")end','UnitManager.CanStartOperation=function()return nil end'):
            with self.subTest(change=change):
                l=self.runtime();l.execute(change+";local r=reader.Read(2,40,target);assert(r.status=='READ_OK' and r.nativeStatus=='UNKNOWN' and r.nativeAllowed==nil)")

class Package(unittest.TestCase):
    def test_actual_database_and_no_existing_unit_change(self):
        p=external_database(R);external=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');external.backup(db);external.close();db.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode()))
        # Loaded DBs after B178 contain this exact fixture unit; remove only it
        # in memory before replaying source SQL. All other unit rows stay compared.
        for kind in ('UNIT_SPC_EXPEDITION_ZERO',):
            db.execute('delete from TypeTags where Type=?',(kind,));db.execute('delete from Units where UnitType=?',(kind,));db.execute('delete from Types where Type=?',(kind,))
        db.execute("delete from TypeTags where Type='UNIT_SPC_EXPEDITION_GATE'")
        db.execute("delete from Units where UnitType='UNIT_SPC_EXPEDITION_GATE'")
        db.execute("delete from Types where Type='UNIT_SPC_EXPEDITION_GATE'")
        before=db.execute('select * from Units order by UnitType').fetchall()
        db.executescript((R/'Mod/Data/ExpeditionGate.sql').read_text())
        after=db.execute("select * from Units where UnitType not in ('UNIT_SPC_EXPEDITION_GATE','UNIT_SPC_EXPEDITION_ZERO') order by UnitType").fetchall();self.assertEqual(before,after)
        row=db.execute("select Spy,CanTrain,CanCapture,CanRetreatWhenCaptured,PurchaseYield,PromotionClass,ExtractsArtifacts,BuildCharges from Units where UnitType='UNIT_SPC_EXPEDITION_GATE'").fetchone()
        self.assertEqual(row,(0,0,0,1,None,None,0,0))
        row=db.execute("select Spy,IgnoreMoves,Stackable,CanRetreatWhenCaptured,CanTrain,CanCapture,PromotionClass,PurchaseYield from Units where UnitType='UNIT_SPC_EXPEDITION_ZERO'").fetchone()
        self.assertEqual(row,(0,1,1,0,0,0,None,None))
        self.assertEqual(db.execute("select Tag from TypeTags where Type='UNIT_SPC_EXPEDITION_ZERO'").fetchall(),[('CLASS_LANDCIVILIAN',)])
        db.close()
    def test_registration_xml_localization_and_art(self):
        m=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot();files=[e.text for e in m.findall('./Files/File')]
        self.assertEqual(len(files),len(set(files)))
        new=['ExpeditionGate.lua','ExpeditionGateRead.lua','Data/ExpeditionGate.sql','Text/ExpeditionGate.sql','UI/ExpeditionGateWindow.lua','UI/ExpeditionGateWindow.xml']
        for p in new:self.assertIn(p,files)
        for e in m.findall('./InGameActions/*/File'):self.assertTrue((R/'Mod'/e.text).is_file(),e.text)
        self.assertEqual(m.attrib['version'],'209')
        ET.parse(R/'Mod/UI/ExpeditionGateWindow.xml')
        art=ET.parse(R/'Mod/ArtDefs/Units.artdef').getroot();names=[e.attrib['text']for e in art.findall('m_RootCollections/Element/Element/m_Name')]
        self.assertEqual(names.count('UNIT_SPC_EXPEDITION_GATE'),1);self.assertEqual(names.count('UNIT_SPC_EXPEDITION_ZERO'),1);self.assertEqual(len(names),7)
        db=sqlite3.connect(':memory:');db.execute('create table LocalizedText(Language text,Tag text,Text text,primary key(Language,Tag))');db.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
        text='\n'.join((R/'Mod'/p).read_text()for p in new)
        keys=set(re.findall(r'LOC_SPC_EXPEDITION_(?:GATE|ZERO)_[A-Z_]+',text))
        for k in keys:
            if k.endswith('_'):continue
            self.assertEqual(db.execute('select count(*) from LocalizedText where Tag=?',(k,)).fetchone()[0],2,k)
        db.close()
    def test_actual_icon_sql_reuses_builder_without_changing_existing_icons(self):
        db=sqlite3.connect(':memory:')
        db.execute('create table IconDefinitions(Name text primary key,Atlas text,"Index" integer)')
        db.executemany('insert into IconDefinitions values(?,?,?)', [('ICON_UNIT_BUILDER','BUILDER_ATLAS',3),('ICON_UNIT_BUILDER_PORTRAIT','BUILDER_PORTRAIT',4),('ICON_UNIT_SPY','SPY_ATLAS',5)])
        db.executescript((R/'Mod/Data/Icons.sql').read_text())
        for base in ('ICON_UNIT_BUILDER','ICON_UNIT_BUILDER_PORTRAIT'):
            expected=db.execute('select Atlas,"Index" from IconDefinitions where Name=?',(base,)).fetchone()
            for name in ('UNIT_SPC_EXPEDITION_GATE','UNIT_SPC_EXPEDITION_ZERO'):
                self.assertEqual(db.execute('select Atlas,"Index" from IconDefinitions where Name=?',(base.replace('UNIT_BUILDER',name),)).fetchone(),expected)
        self.assertEqual(db.execute('select Atlas,"Index" from IconDefinitions where Name=?',('ICON_UNIT_SPY',)).fetchone(),('SPY_ATLAS',5))
        db.close()
    def test_no_spy_operation_or_saved_gameplay_write(self):
        src=(R/'Mod/ExpeditionGate.lua').read_text();read=(R/'Mod/ExpeditionGateRead.lua').read_text()
        for marker in ('RequestOperation(', 'SetProperty(', 'SetXY(', 'GetSpyOperation(', 'SetSpyOperation('):
            self.assertNotIn(marker,src+read)
        self.assertNotIn('RegisterExit(',src);self.assertNotIn('SPY_TRAVEL_NEW_CITY',src)
        self.assertIn('CanStartOperation',read);self.assertIn('UnitManager.PlaceUnit(',src)
        for marker in ('SpyMissionCompleted','ChangeUnitAbilityCount','ChangeEraScore','SetSpy'):
            self.assertNotIn(marker,src+read)
    def test_ui_uses_own_ingress_and_no_periodic_native_read(self):
        s=(R/'Mod/UI/ExpeditionGateWindow.lua').read_text()
        self.assertIn("OnStart='SPC_ExpeditionGateRequest'",s)
        self.assertEqual(s.count('R.Read('),1);self.assertIn("Controls.TravelButton:RegisterCallback",s)
        self.assertNotIn('SPC_P0_Request',s)
        self.assertNotIn('SetProperty(',s)


class Window(unittest.TestCase):
    def runtime(self, initialize=True):
        l=Reader().runtime()
        l.execute(r"""
          P.VERSION='P0-B-182.209';SPCP0=P;units={};sent=0
          include=function()end;Mouse={eLClick=1};KeyEvents={KeyUp=1};Keys={VK_ESCAPE=27}
          Locale={Lookup=function(key,...)local a={...};for i,v in ipairs(a)do a[i]=tostring(v)end;return key..':'..table.concat(a,',')end}
          Controls={}
          function makeControl(id,hidden)
           local c={hidden=hidden}
           function c:SetText(v)self.text=v end;function c:SetHide(v)self.hidden=v end
           function c:IsHidden()return self.hidden end;function c:RegisterCallback(mouse,fn)self.click=fn end
           function c:CalculateSize()end;function c:ReprocessAnchoring()end;Controls[id]=c
          end
          ContextPtr={hidden=true,SetHide=function(self,value)self.hidden=value end,IsHidden=function(self)return self.hidden end,SetUpdate=function(self,fn)update=fn end,ClearUpdate=function()update=nil end,SetInputHandler=function(self,fn)input=fn end,
            SetInitHandler=function(self,fn)init=fn end,SetShutdown=function(self,fn)shutdown=fn end}
          LuaEvents={SPC_ExpeditionGateOpen={Add=function(fn)gateOpen=fn;gateAdds=(gateAdds or 0)+1 end,Remove=function(fn)assert(gateOpen==fn);gateOpen=nil end}}
          UI={GetHeadSelectedCity=function()return city end,RequestPlayerOperation=function(pid,operation,packet)
            sent=sent+1;lastPacket=packet;if not deferred then handler(pid,packet)end
          end}
          PlayerOperations={EXECUTE_SCRIPT=1};Game.GetLocalPlayer=function()return 2 end
          Events.LoadScreenClose={Add=function(fn)loadScreen=fn end,Remove=function(fn)assert(loadScreen==fn);loadScreen=nil end}
          Events.LocalPlayerTurnBegin={Add=function(fn)turnBegin=fn end,Remove=function(fn)assert(turnBegin==fn);turnBegin=nil end}
          Events.GameCoreEventPublishComplete={Add=function(fn)publish=fn end,Remove=function(fn)assert(publish==fn);publish=nil end}
        """)
        for element in ET.parse(R/'Mod/UI/ExpeditionGateWindow.xml').getroot().iter():
            if element.get('ID'):
                l.globals().makeControl(element.get('ID'),element.get('Hidden')=='1')
        l.execute((R/'Mod/UI/ExpeditionGateWindow.lua').read_text())
        if initialize:l.execute('init()')
        return l
    def test_closed_start_no_native_helpers_or_creation(self):
        l=self.runtime();l.execute("assert(Controls.Window.hidden and initCalls==0 and helperCalls==0 and sent==0);turnBegin();publish();assert(sent==0)")
    def test_native_hidden_addin_root_must_be_visible_before_open_ack(self):
        l=self.runtime();l.execute("assert(ContextPtr.hidden and not ExposedMembers.SPC_ExpeditionGateUIOpenVersion);gateOpen();assert(not ContextPtr.hidden and not Controls.Window.hidden);assert(ExposedMembers.SPC_ExpeditionGateUIOpenVersion==P.VERSION);Controls.CloseButton.click();assert(ContextPtr.hidden and Controls.Window.hidden and not ExposedMembers.SPC_ExpeditionGateUIOpenVersion)")
    def test_hidden_root_rejects_open_ack_without_gameplay_read(self):
        l=self.runtime();l.execute("ContextPtr.SetHide=function()end;gateOpen();assert(not ExposedMembers.SPC_ExpeditionGateUIOpenVersion and sent==0)")
    def test_close_escape_and_player_exit_hide_entire_context(self):
        l=self.runtime();l.execute("gateOpen();assert(input(KeyEvents.KeyUp,Keys.VK_ESCAPE));assert(ContextPtr.hidden and Controls.Window.hidden and not ExposedMembers.SPC_ExpeditionGateUIOpenVersion);gateOpen();Game.GetLocalPlayer=function()return 3 end;turnBegin();assert(ContextPtr.hidden and Controls.Window.hidden and not ExposedMembers.SPC_ExpeditionGateUIOpenVersion)")

    def test_actual_window_create_read_dispatch_refresh_end_flow(self):
        l=self.runtime();l.execute("gateOpen();Controls.CreateButton.click();assert(initCalls==1);Controls.TravelButton.click();assert(helperCalls==2 and Controls.Report.text:find('NATIVE_REJECTED'));Controls.ArmButton.click();assert(helperCalls==4 and lastPacket.Action=='DISPATCH' and Controls.Report.text:find('JOURNEY'));currentTurn=85;ownTurn(2);Controls.RefreshButton.click();assert(Controls.Report.text:find('ARRIVED') and placeCalls==1);Controls.EndButton.click();assert(destroys==1 and not Controls.Report.text:find('TIMING'))")
    def test_closing_window_does_not_own_travel_timer(self):
        l=self.runtime();l.execute("gateOpen();Controls.CreateButton.click();Controls.ArmButton.click();Controls.CloseButton.click();currentTurn=85;ownTurn(2);assert(placeCalls==1 and Controls.Window.hidden);gateOpen();assert(Controls.Report.text:find('ARRIVED'))")
    def test_hold_refresh_exposes_specific_stop_reason(self):
        l=self.runtime();l.execute("gateOpen();Controls.CreateButton.click();units[40].x=8;Controls.RefreshButton.click();assert(Controls.Report.text:find('TEAM_DISPLACED_STOP'))")
    def test_unknown_timing_blocks_dispatch_without_sending(self):
        l=self.runtime();l.execute("gateOpen();Controls.CreateButton.click();UnitManager.GetTravelTime=nil;local n=sent;Controls.ArmButton.click();assert(sent==n and placeCalls==0 and Controls.Report.text:find('TIMING_UNKNOWN'))")
    def test_pending_action_never_auto_reissued(self):
        l=self.runtime();l.execute("gateOpen();deferred=true;Controls.CreateButton.click();assert(sent==2);Controls.CreateButton.click();for i=1,3 do publish()end;assert(sent==2);update(11);assert(update==nil and sent==2 and Controls.Report.text:find('TIMEOUT'))")
    def test_close_does_not_cancel_accepted_request_or_spawn_again(self):
        l=self.runtime();l.execute("gateOpen();deferred=true;Controls.CreateButton.click();local p=lastPacket;Controls.CloseButton.click();handler(2,p);deferred=false;gateOpen();assert(initCalls==1 and Controls.Report.text:find('UNIT'))")
    def test_unknown_helpers_shown_without_operating_unit(self):
        l=self.runtime();l.execute("gateOpen();Controls.CreateButton.click();UnitManager.GetTravelTime=nil;Controls.TravelButton.click();assert(Controls.Report.text:find('TIMING_UNKNOWN') and destroys==0 and units[40].x==1)")

    def test_ready_only_after_successful_init_and_single_subscription(self):
        l=self.runtime(False);l.execute("assert(not ExposedMembers.SPC_ExpeditionGateUIVersion and not gateOpen);init();init();assert(gateAdds==1 and ExposedMembers.SPC_ExpeditionGateUIVersion==P.VERSION and sent==0)")
    def test_shutdown_unregisters_ui_without_destroying_or_sending(self):
        l=self.runtime();l.execute("gateOpen();Controls.CreateButton.click();local n=sent;shutdown();assert(not gateOpen and not publish and not turnBegin and not loadScreen and not ExposedMembers.SPC_ExpeditionGateUIVersion);assert(sent==n and units[40] and destroys==0)")
    def test_unsupported_local_player_cannot_open_and_existing_window_closes(self):
        l=self.runtime();l.execute("gateOpen();local n=sent;Game.GetLocalPlayer=function()return 3 end;turnBegin();assert(Controls.Window.hidden);gateOpen();assert(Controls.Window.hidden and sent==n)")
    def test_no_fixed_hud_entry_and_buttons_have_visible_child_captions(self):
        root=ET.parse(R/'Mod/UI/ExpeditionGateWindow.xml').getroot()
        self.assertIsNone(root.find("GridButton[@ID='OpenButton']"))
        buttons=root.findall(".//GridButton");self.assertEqual(len(buttons),8)
        for button in buttons:
            with self.subTest(button=button.get('ID')):
                label=button.find('Label');self.assertIsNotNone(label)
                self.assertEqual(label.get('Color'),'255,255,255,255')
                self.assertTrue(label.get('String'))
        l=self.runtime();l.execute("assert(Controls.CreateButtonCaption.text:find('CREATE') and Controls.EndButtonCaption.text:find('END'))")

    def test_target_controls_use_readable_captions_and_nonoverlapping_small_buttons(self):
        # MainButton has native MinSize=80x41; the old 40x30 arrow controls
        # overflowed their declared slot. Small style and explicit bounds avoid it.
        root=ET.parse(R/'Mod/UI/ExpeditionGateWindow.xml').getroot()
        window=root.find("Container[@ID='Window']");width=int(window.get('Size').split(',')[0])
        bounds=[]
        for name,key in [('PreviousButton','PREVIOUS'),('NextButton','NEXT')]:
            b=root.find(".//GridButton[@ID='"+name+"']")
            self.assertEqual(b.get('Style'),'MainButtonSmall')
            self.assertEqual(b.get('Anchor'),'L,T')
            x,y=map(int,b.get('Offset').split(','));w,h=map(int,b.get('Size').split(','))
            self.assertGreaterEqual(w,100);self.assertGreaterEqual(x,18);self.assertLessEqual(x+w,width-18)
            self.assertEqual(b.find('Label').get('String'),'LOC_SPC_EXPEDITION_GATE_'+key)
            bounds.append((x,x+w))
        label=root.find(".//Label[@ID='TargetLabel']");wrap=int(label.get('WrapWidth'))
        self.assertGreaterEqual((width-wrap)/2,bounds[0][1]+10)
        self.assertLessEqual((width+wrap)/2,bounds[1][0]-10)
        l=self.runtime();l.execute("assert(Controls.PreviousButtonCaption.text:find('PREVIOUS') and Controls.NextButtonCaption.text:find('NEXT'))")

if __name__=='__main__':unittest.main(verbosity=2)
