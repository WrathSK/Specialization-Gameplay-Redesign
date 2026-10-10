"""B178: actual gate Lua and database checks. Native travel/retreat remain unproved.
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
          kind='UNIT_SPC_EXPEDITION_GATE'; currentTurn=81; initCalls=0; destroys=0; properties=0
          function event()return {listeners={},Add=function(self_or_fn)end}end
          Game={GetCurrentGameTurn=function()return currentTurn end}
          Events={UnitRemovedFromMap={Add=function(fn)removed=fn end}}
          GameEvents={SPC_ExpeditionGateRequest={Add=function(fn)handler=fn end}}
          ExposedMembers={};shared={}
          info={[100]={UnitType=kind,Spy=false,CanRetreatWhenCaptured=true,FormationClass='FORMATION_CLASS_CIVILIAN'},
                [101]={UnitType='UNIT_SETTLER',Spy=false,FormationClass='FORMATION_CLASS_CIVILIAN'}}
          info[kind]=info[100]
          units={}; foreignUnits={};cities={};spyCapacity=2
          function unit(id,type_,owner,x,y)
           local u={id=id,type_=type_ or 100,owner=owner or 2,x=x or 1,y=y or 1}
           function u:GetID()return self.id end;function u:GetType()return self.type_ end;u.GetUnitType=u.GetType
           function u:GetOwner()return self.owner end;function u:GetX()return self.x end;function u:GetY()return self.y end
           function u:SetProperty()properties=properties+1;error('Unexpected property write')end
           return u
          end
          city={id=1,owner=2,x=1,y=1}
          function city:GetID()return self.id end;function city:GetOwner()return self.owner end
          function city:GetX()return self.x end;function city:GetY()return self.y end
          function city:GetName()return '文化城' end
          cities[1]=city
          active=4;spec='CULTURE';pending=false
          shared.EffectiveFacts={Read=function(pid,c)if factsError then error('UNKNOWN_FACTS')end
            return {specialization=spec,active=active,investmentPending=pending}end}
          local us={}
          function us:Members()return pairs(units)end;function us:FindID(id)return units[id]end
          function us:Destroy(u)destroys=destroys+1;if not destroyFail then units[u.id]=nil;if removed then removed(u.owner,u.id)end end end
          local cs={FindID=function(self,id)return cities[id]end}
          Players={[2]={GetUnits=function()return us end,GetCities=function()return cs end}}
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
          end}
          function req(action,token,id,cityID,pid)
            handler(pid or 2,{Action=action,Token=token,UnitID=id,CityID=cityID or 1})
            return ExposedMembers.SPC_ExpeditionGateReply
          end
        ''')
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
    def test_occupied_city_center(self):
        l=self.runtime();l.execute("units[5]=unit(5,101);req('CREATE','a');assert(initCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.error=='CITY_CENTER_OCCUPIED')")
    def test_unsupported_player_and_malformed_request(self):
        l=self.runtime();l.execute("handler(3,{Action='CREATE',Token='a',CityID=1});handler(2,{});handler(2,{Token=string.rep('a',101)});assert(initCalls==0 and ExposedMembers.SPC_ExpeditionGateReply==nil)")
    def test_bad_database_flags(self):
        for change in ('info[100].Spy=true','info[100].CanRetreatWhenCaptured=false','info[kind]=nil'):
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
    def test_watch_and_same_owner_movement_are_observation_only(self):
        l=self.runtime();l.execute("req('CREATE','a');req('ARM','b',40);units[40].x=9;local r=req('READ','c');assert(r.watchedAlive and r.watchX==1 and r.watchedX==9 and r.protectionPass==nil)")
    def test_missing_unit_never_respawned_by_read_or_event(self):
        l=self.runtime();l.execute("req('CREATE','a');req('ARM','b',40);removed(3,40);units[40]=nil;removed(2,40);local r=req('READ','c');assert(r.watchedAlive==false and r.removedEvents==1 and initCalls==1)")
    def test_changed_owner_type_not_owned_cleanup_target(self):
        for change in ('units[40].owner=3','units[40].type_=101'):
            with self.subTest(change=change):
                l=self.runtime();l.execute("req('CREATE','a');"+change+";req('END','b',40);assert(destroys==0 and ExposedMembers.SPC_ExpeditionGateReply.error=='TEST_TEAM_CHANGED')")
    def test_end_exact_unit_only_and_repeated_request(self):
        l=self.runtime();l.execute("req('CREATE','a');units[4]=unit(4,101,2,8,8);req('END','b',40);req('END','b',40);assert(destroys==1 and units[4] and not units[40] and properties==0)")
    def test_end_failure_reported_without_success(self):
        l=self.runtime();l.execute("req('CREATE','a');destroyFail=true;req('END','b',40);assert(ExposedMembers.SPC_ExpeditionGateReply.error=='END_UNCONFIRMED' and units[40])")

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
            GetCities=function()return {FindID=function(self,id)if id==9 then return targetCity end end,GetCapitalCity=function()return targetCity end}end}
          Players[2].GetDiplomacy=function()return {HasMet=function(self,p)return met end,GetSpyCapacity=function()return spyCapacity end}end
          UnitManager.GetTravelTime=function(u,c)helperCalls=helperCalls+1;return travelValue or 3 end
          UnitManager.GetEstablishInCityTime=function(u,c)helperCalls=helperCalls+1;return establishValue or 1 end
          target={owner=3,id=9,name='目标首都',x=15,y=8}
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

class Package(unittest.TestCase):
    def test_actual_database_and_no_existing_unit_change(self):
        p=external_database(R);external=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');external.backup(db);external.close();db.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode()))
        # Loaded DBs after B178 contain this exact fixture unit; remove only it
        # in memory before replaying source SQL. All other unit rows stay compared.
        db.execute("delete from TypeTags where Type='UNIT_SPC_EXPEDITION_GATE'")
        db.execute("delete from Units where UnitType='UNIT_SPC_EXPEDITION_GATE'")
        db.execute("delete from Types where Type='UNIT_SPC_EXPEDITION_GATE'")
        before=db.execute('select * from Units order by UnitType').fetchall()
        db.executescript((R/'Mod/Data/ExpeditionGate.sql').read_text())
        after=db.execute("select * from Units where UnitType<>'UNIT_SPC_EXPEDITION_GATE' order by UnitType").fetchall();self.assertEqual(before,after)
        row=db.execute("select Spy,CanTrain,CanCapture,CanRetreatWhenCaptured,PurchaseYield,PromotionClass,ExtractsArtifacts,BuildCharges from Units where UnitType='UNIT_SPC_EXPEDITION_GATE'").fetchone()
        self.assertEqual(row,(0,0,0,1,None,None,0,0));db.close()
    def test_registration_xml_localization_and_art(self):
        m=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot();files=[e.text for e in m.findall('./Files/File')]
        self.assertEqual(len(files),len(set(files)))
        new=['ExpeditionGate.lua','ExpeditionGateRead.lua','Data/ExpeditionGate.sql','Text/ExpeditionGate.sql','UI/ExpeditionGateWindow.lua','UI/ExpeditionGateWindow.xml']
        for p in new:self.assertIn(p,files)
        for e in m.findall('./InGameActions/*/File'):self.assertTrue((R/'Mod'/e.text).is_file(),e.text)
        self.assertEqual(m.attrib['version'],'206')
        ET.parse(R/'Mod/UI/ExpeditionGateWindow.xml')
        art=ET.parse(R/'Mod/ArtDefs/Units.artdef').getroot();names=[e.attrib['text']for e in art.findall('m_RootCollections/Element/Element/m_Name')]
        self.assertEqual(names.count('UNIT_SPC_EXPEDITION_GATE'),1);self.assertEqual(len(names),6)
        db=sqlite3.connect(':memory:');db.execute('create table LocalizedText(Language text,Tag text,Text text,primary key(Language,Tag))');db.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
        text='\n'.join((R/'Mod'/p).read_text()for p in new)
        keys=set(re.findall(r'LOC_SPC_EXPEDITION_GATE_[A-Z_]+',text))
        for k in keys:
            if k.endswith('_'):continue
            self.assertEqual(db.execute('select count(*) from LocalizedText where Tag=?',(k,)).fetchone()[0],2,k)
        db.close()
    def test_no_spy_operation_or_saved_gameplay_write(self):
        src=(R/'Mod/ExpeditionGate.lua').read_text();read=(R/'Mod/ExpeditionGateRead.lua').read_text()
        for marker in ('RequestOperation(', 'SetProperty(', 'SetXY(', 'PlaceUnit(', 'GetSpyOperation(', 'SetSpyOperation('):
            self.assertNotIn(marker,src+read)
        self.assertNotIn('RegisterExit(',src);self.assertNotIn('SPY_TRAVEL_NEW_CITY',src+read)
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
          P.VERSION='P0-B-179.206';SPCP0=P;units={};sent=0
          include=function()end;Mouse={eLClick=1};KeyEvents={KeyUp=1};Keys={VK_ESCAPE=27}
          Locale={Lookup=function(key,...)local a={...};for i,v in ipairs(a)do a[i]=tostring(v)end;return key..':'..table.concat(a,',')end}
          Controls={}
          function makeControl(id,hidden)
           local c={hidden=hidden}
           function c:SetText(v)self.text=v end;function c:SetHide(v)self.hidden=v end
           function c:IsHidden()return self.hidden end;function c:RegisterCallback(mouse,fn)self.click=fn end
           function c:CalculateSize()end;function c:ReprocessAnchoring()end;Controls[id]=c
          end
          ContextPtr={SetUpdate=function(self,fn)update=fn end,ClearUpdate=function()update=nil end,SetInputHandler=function(self,fn)input=fn end,
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
    def test_actual_window_create_read_arm_end_flow(self):
        l=self.runtime();l.execute("gateOpen();Controls.CreateButton.click();assert(initCalls==1);Controls.TravelButton.click();assert(helperCalls==2 and Controls.Report.text:find('TIMING'));Controls.ArmButton.click();units[40].x=8;Controls.RefreshButton.click();assert(Controls.Report.text:find('WATCH'));Controls.EndButton.click();assert(destroys==1 and not Controls.Report.text:find('TIMING'))")
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

if __name__=='__main__':unittest.main(verbosity=2)
