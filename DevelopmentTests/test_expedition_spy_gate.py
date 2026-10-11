"""B189 Spy=1 native-name observation gate regression (extends prior fixture). Native travel/coexistence/rewards remain USER_GAME_TEST.
Reuses the preceding fixture environment; exercises actual current Lua/SQL/UI.
External DB is read-only and copied in memory. No ordinary Spy definitions change.
"""
from pathlib import Path
import re, sqlite3, unittest, zlib, xml.etree.ElementTree as ET
import test_expedition_gate as previous
from project_paths import external_database
R=Path(__file__).resolve().parents[1]

def gate(ui=False, window=False):
    l=previous.Window().runtime(False) if window else previous.Reader().runtime() if ui else previous.Gate().runtime()
    l.execute("""
      kind='UNIT_SPC_EXPEDITION_SPY';info[100].UnitType=kind;info[100].Spy=true
      info[100].PromotionClass='PROMOTION_CLASS_SPY';info[100].Name='LOC_TEST_DEFAULT';info[kind]=info[100]
      info[103]={UnitType='UNIT_SPY',Spy=true,Hash=103};info.UNIT_SPY=info[103]
      local originalUnit=unit
      function unit(...)
       local u=originalUnit(...);u.properties={};u.name=u.type_==100 and 'LOC_TEST_DEFAULT' or 'Native Spy'
       function u:GetName()return self.name end
       function u:GetProperty(k)return self.properties[k]end
       function u:SetProperty(k,v)properties=properties+1;error('Spy identity gate must not write Unit Properties')end
       function u:GetSpyOperation()return self.operation or -1 end
       return u
      end
      units={};nativeCalls=0;nativeAllow=true;trainable=true;offmap=0;sourceTurns=0
      -- Mock engine assignment only; native pool support remains an in-game gate.
      nativeName='LOC_CITIZEN_TEST_A';nameConfirmCalls=0
      local nativeInit=UnitManager.InitUnit
      UnitManager.InitUnit=function(...)
       local u=nativeInit(...);if u then u.name=nativeName end;return u
      end
      PlayerConfigurations={[2]={GetCivilizationTypeName=function()return civilization or 'CIVILIZATION_SPC_TEST' end}}
      P.PlayerConfigurations=PlayerConfigurations
      poolRows={{CivilizationType='CIVILIZATION_SPC_TEST',CitizenName='LOC_CITIZEN_TEST_A',Female=0,Modern=0},
       {CivilizationType='CIVILIZATION_SPC_TEST',CitizenName='LOC_CITIZEN_TEST_B',Female=1,Modern=1},
       {CivilizationType='CIVILIZATION_OTHER',CitizenName='LOC_CITIZEN_OTHER',Female=0,Modern=0}}
      GameInfo=GameInfo or {Units=info}
      GameInfo.CivilizationCitizenNames=function()
       local n=0;return function()n=n+1;return poolRows[n]end
      end
      P.GameInfo=GameInfo
      -- Gameplay-only fixture intentionally exposes no off-map Spy API.
      -- That evidence is read in UI and sent as an explicit current-turn sample.
      rawreq=req
      function confirmName(token,id,name)
       handler(2,{Action='NAME',Token=token,UnitID=id or 40,Name=name or units[id or 40].name,NameOffmapChecked=true,NameSampleTurn=currentTurn})
       return ExposedMembers.SPC_ExpeditionGateReply
      end
      function req(action,token,...)
       local r=rawreq(action,token,...)
       if action=='CREATE' and r.phase=='NAMING' and not r.error then
        r=confirmName(token..':fixture-name',r.unitID)
       end
       return r
      end
      Locale=Locale or {Lookup=function(s)return s end}
      local baseLookup=Locale.Lookup
      Locale.Lookup=function(s,...)
       if s=='LOC_SPC_EXPEDITION_SPY_NAME_PREFIX' then return '人文考察团·' end
       if s=='文化城' then return s end
       return baseLookup(s,...)
      end
      GameInfo=GameInfo or {Units=info};GameInfo.UnitOperations={UNITOPERATION_SPY_GAIN_SOURCES={Index=27,Hash=900}}
      function nativeDispatch(token,overrides)
       local p={NativeAllowed=true};for k,v in pairs(overrides or {})do p[k]=v end;return dispatch(token,p)
      end
    """)
    l.execute((R/'Mod/ExpeditionSpyGate.lua').read_text());l.execute("SPCExpeditionSpyGate.Start(P,shared);local h=handler;handler=function(pid,p)if p.Action=='NAME' then nameConfirmCalls=nameConfirmCalls+1 end;return h(pid,p)end")
    if ui or window:
        l.execute("""
          Players[2].GetDiplomacy=function()return {HasMet=function()return met~=false end,
           GetSpyCapacity=function()return spyCapacity end,GetNumSpiesOffMap=function()return offmap end,
           GetNthOffMapSpy=function(self,pid,n)return offmapRows and offmapRows[n+1]end,
           GetSourceTurnsRemaining=function()return sourceTurns end}end
          city.GetBuildQueue=function()return {CanProduce=function(self,params,a,b)
           assert(type(params)=='table' and params.UnitType==103 and a==false and b==true);return trainable end}end
          MilitaryFormationTypes={STANDARD_MILITARY_FORMATION=0}
          UnitOperationTypes.SPY_GAIN_SOURCES=9
          nameCalls=0
          -- Any accidental old rename path is a failure, not a simulated success.
          UnitCommandTypes={NAME_UNIT=10,PARAM_NAME='Name'}
          UnitManager.CanStartCommand=function()nameCalls=nameCalls+1;error('B189 must not query rename command')end
          UnitManager.RequestCommand=function()nameCalls=nameCalls+1;error('B189 must not rename')end
          UnitManager.CanStartOperation=function(u,op,plot,params)
           assert(op==8 or op==9);assert(plot.x==params.X and plot.y==params.Y);return nativeAllow end
          UnitManager.GetResultProbability=function(index,u,plot)assert(index==27);return {ESPIONAGE_SUCCESS_UNDETECTED=1,ESPIONAGE_SUCCESS_MUST_ESCAPE=0}end
          UnitManager.RequestOperation=function(u,op,params)
           assert(op==8);nativeCalls=nativeCalls+1;if nativeThrow then error('REQUEST_UNKNOWN')end
           if nativeFalse then return false end
          end
        """)
        l.execute((R/'Mod/ExpeditionSpyRead.lua').read_text());l.execute('reader=SPCExpeditionSpyRead')
    if window:
        l.execute("LuaEvents.SPC_ExpeditionActivityChanged={Add=function(fn)activityChanged=fn end,Remove=function(fn)assert(activityChanged==fn);activityChanged=nil end};makeControl('TaskButton');makeControl('TaskButtonCaption');P.VERSION='P0-B-189.216';Events.SpyMissionCompleted={Add=function(fn)mission=fn end,Remove=function(fn)assert(mission==fn);mission=nil end}")
        l.execute((R/'Mod/UI/ExpeditionSpyWindow.lua').read_text());l.execute('init()')
    return l

class Gate(unittest.TestCase):
    def test_create_own_source_capacity_one_native_name_and_no_native_mission(self):
        l=gate();l.execute("units[7]=unit(7,101);req('CREATE','a');req('CREATE','a');local r=req('READ','b');assert(r.phase=='CREATED' and r.count==1 and r.coLocated==1 and r.sourceCity==1 and r.unitID==40 and initCalls==1 and properties==0 and finishCalls==0 and placeCalls==0 and units[7])")
    def test_old_fixtures_count_and_cleanup_only(self):
        for kind in ['UNIT_SPC_EXPEDITION_GATE','UNIT_SPC_EXPEDITION_ZERO']:
            with self.subTest(kind=kind):
                l=gate();l.execute(f"info[102].UnitType='{kind}';units[5]=unit(5,102);assert(req('READ','a').legacy);req('CREATE','b');assert(initCalls==0);req('END','c',5);assert(destroys==1)")
    def test_native_permission_required_before_permit(self):
        for p in ["NativeAllowed=false","NativeStatus='UNKNOWN'","Travel=-1","FromX=4","SampleTurn=80","TargetID=123"]:
            with self.subTest(p=p):
                l=gate();l.execute("req('CREATE','a');local r=nativeDispatch('b',{"+p+"});assert(r.error and r.phase=='CREATED' and not r.nativePermit and placeCalls==0)")
    def test_native_offmap_reserves_cap_no_resurrection_or_second_create(self):
        l=gate();l.execute("req('CREATE','a');local r=nativeDispatch('b');assert(r.nativePermit=='b');units[40]=nil;removed(2,40);currentTurn=82;ownTurn(2);r=req('READ','c');assert(r.phase=='TRAVELLING' and r.count==1 and r.observedCount==0 and r.reservedCapacity and not r.unitID);req('CREATE','d');assert(initCalls==1 and destroys==0 and placeCalls==0)")
    def test_unknown_live_identity_prevents_create_without_intermediate_read(self):
        l=gate();l.execute("req('CREATE','a');units[40]=nil;req('CREATE','b');assert(initCalls==1 and ExposedMembers.SPC_ExpeditionGateReply.phase=='HELD')")
    def test_same_id_arrival_and_active_decline(self):
        l=gate();l.execute("req('CREATE','a');nativeDispatch('b');active=1;spec='REALLOCATING';units[40].x=15;units[40].y=8;foreignUnits[9]=unit(9,101,3,15,8);currentTurn=83;ownTurn(2);ownTurn(2);local r=req('READ','c');assert(r.phase=='ARRIVED' and r.sameUnit and r.sourceCity==1 and r.count==1 and r.coLocated==1 and foreignUnits[9] and placeCalls==0 and properties==0)")
    def test_changed_id_never_rebound_and_missing_arrival_stops(self):
        l=gate();l.execute("req('CREATE','a');nativeDispatch('b');units[40]=nil;units[41]=unit(41,100,2,15,8);currentTurn=85;ownTurn(2);local r=req('READ','c');assert(r.phase=='HELD' and r.stop=='NATIVE_IDENTITY_UNCONFIRMED' and r.unitID==41 and not r.bound and r.createdID==40 and r.reservedCapacity and units[41] and destroys==0)")
    def test_source_unknown_loss_or_target_change_retains_original_without_further_writes(self):
        for change in ['city.token=nil','city.token="new"','city.owner=3','targetCity.owner=4','met=false','visible=false']:
            with self.subTest(change=change):
                l=gate();l.execute("req('CREATE','a');nativeDispatch('b');"+change+";transfer();assert(req('READ','c').phase=='HELD' and units[40] and properties==0 and destroys==0)")
    def test_end_never_destroys_ordinary_spy_or_foreign_unit(self):
        for change in ['units[40].type_=103','units[40].owner=3']:
            with self.subTest(change=change):
                l=gate();l.execute("req('CREATE','a');"+change+";req('END','b',40);assert(units[40] and destroys==0)")
    def test_end_exact_prototype_only_and_repeated_token(self):
        l=gate();l.execute("req('CREATE','a');units[5]=unit(5,103);req('END','b',40);req('END','b',40);assert(destroys==1 and units[5] and not units[40] and properties==0)")
    def test_explicit_stop_blocks_dispatch_but_allows_exact_cleanup(self):
        l=gate();l.execute("req('CREATE','a');handler(2,{Action='STOP',Token='s',UnitID=40,Detail='ordinary spy changed'});assert(req('READ','r').phase=='HELD');nativeDispatch('b');assert(not ExposedMembers.SPC_ExpeditionGateReply.nativePermit);req('END','e',40);assert(destroys==1)")
    def test_qualification_unknown_never_creates(self):
        for change in ['active=3','active=nil','spec="RESEARCH"','pending=true','factsError=true','city.token=nil','city.owner=3']:
            with self.subTest(change=change):
                l=gate();l.execute(change+";req('CREATE','a');assert(initCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.error)")
    def test_bad_spy_definition_never_creates(self):
        for change in ['info[100].Spy=false','info[100].Stackable=false','info[100].IgnoreMoves=false','info[100].CanRetreatWhenCaptured=true','info[100].PromotionClass=nil']:
            with self.subTest(change=change):
                l=gate();l.execute(change+";req('CREATE','a');assert(initCalls==0 and ExposedMembers.SPC_ExpeditionGateReply.error=='TEST_DATABASE_NOT_READY')")
    def test_foreign_turn_does_not_observe_or_write(self):
        l=gate();l.execute("req('CREATE','a');nativeDispatch('b');units[40]=nil;currentTurn=999;ownTurn(3);assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='TRAVELLING' and placeCalls==0 and properties==0)")
    def test_failed_create_locks_no_blind_retry(self):
        for change in ['initNil=true','initThrowBefore=true','initThrowAfter=true']:
            with self.subTest(change=change):
                l=gate();l.execute(change+";req('CREATE','a');req('CREATE','b');assert(initCalls==1 and ExposedMembers.SPC_ExpeditionGateReply.phase=='HELD')")

class Reader(unittest.TestCase):
    def test_gain_sources_is_read_only_even_with_undetected_one(self):
        l=gate(ui=True);l.execute("req('CREATE','a');sourceTurns=6;local r=reader.GainSources(2,40,target);assert(r.readOK and r.canStart and r.ESPIONAGE_SUCCESS_UNDETECTED==1 and r.sourceTurns==6 and r.status=='NOT_ISOLATED' and not r.executionAllowed and nativeCalls==0 and properties==0)")
    def test_gain_sources_unknown_never_zero_or_success(self):
        l=gate(ui=True);l.execute("req('CREATE','a');sourceTurns=nil;UnitManager.GetResultProbability=nil;local r=reader.GainSources(2,40,target);assert(r.sourceTurns==nil and r.ESPIONAGE_SUCCESS_UNDETECTED==nil and not r.executionAllowed and nativeCalls==0)")
    def test_one_shot_native_travel_no_gain_sources_request(self):
        l=gate(ui=True);l.execute("req('CREATE','a');assert(reader.SubmitTravel(2,40,target,'one'));assert(not reader.SubmitTravel(2,40,target,'one'));assert(nativeCalls==1)")
    def test_native_unknown_result_consumes_permit(self):
        for change in ['nativeThrow=true','nativeFalse=true']:
            with self.subTest(change=change):
                l=gate(ui=True);l.execute("req('CREATE','a');"+change+";assert(not reader.SubmitTravel(2,40,target,'one'));assert(not reader.SubmitTravel(2,40,target,'one'));assert(nativeCalls==1)")
    def test_native_reject_foreign_or_ordinary_never_requested(self):
        for change in ['nativeAllow=false','units[40].owner=3','units[40].type_=103','targetCity.owner=4']:
            with self.subTest(change=change):
                l=gate(ui=True);l.execute("req('CREATE','a');"+change+";assert(not reader.SubmitTravel(2,40,target,'one'));assert(nativeCalls==0)")
    def test_ordinary_spy_classification_not_confused_with_own_cap(self):
        l=gate(ui=True);l.execute("units[8]=unit(8,103);local b=reader.Audit(2,1);req('CREATE','a');local a=reader.Audit(2,1);assert(a.nativeTotal==2 and a.normal==1 and a.capacity==2 and reader.Compare(b,a)=='SLOT_COST_ACCEPTED');trainable=false;assert(reader.Compare(b,reader.Audit(2,1))=='SLOT_COST_ACCEPTED')")
    def test_no_native_capacity_evidence_does_not_claim_isolation(self):
        l=gate(ui=True);l.execute("trainable=false;local b=reader.Audit(2,1);assert(reader.Compare(b,b)=='PARTIAL');spyCapacity=nil;assert(reader.Compare(b,reader.Audit(2,1))=='UNKNOWN')")

class Window(unittest.TestCase):
    def test_actual_ui_roundtrip_native_request_once_gain_sources_never(self):
        l=gate(window=True);l.execute("assert(sent==0 and nativeCalls==0 and Controls.Window.hidden);gateOpen();Controls.CreateButton.click();assert(initCalls==1);Controls.TravelButton.click();assert(Controls.Report.text:find('GAIN_BLOCKED'));Controls.ArmButton.click();assert(nativeCalls==1 and placeCalls==0 and not Controls.Window.hidden);units[40].x=15;units[40].y=8;currentTurn=85;ownTurn(2);Controls.RefreshButton.click();assert(Controls.Report.text:find('PHASE_ARRIVED'));Controls.EndButton.click();assert(destroys==1 and Controls.Report.text:find('PHASE_ENDED'))")
    def test_accepted_native_slot_trainability_cost_does_not_stop_creation(self):
        l=gate(window=True);l.execute("local f=UnitManager.InitUnit;UnitManager.InitUnit=function(...)local u=f(...);trainable=false;return u end;gateOpen();Controls.CreateButton.click();assert(Controls.Report.text:find('PHASE_CREATED') and Controls.Report.text:find('SLOT_COST_ACCEPTED') and nativeCalls==0 and units[40]);Controls.EndButton.click();assert(destroys==1)")
    def test_native_request_throw_holds_and_not_retried(self):
        l=gate(window=True);l.execute("gateOpen();Controls.CreateButton.click();nativeThrow=true;Controls.ArmButton.click();publish();Controls.ArmButton.click();assert(nativeCalls==1 and Controls.Report.text:find('BOUND_REQUIRED'))")
    def test_close_shutdown_no_creation_or_lingering_callbacks(self):
        l=gate(window=True);l.execute("gateOpen();Controls.CreateButton.click();Controls.CloseButton.click();assert(ContextPtr.hidden);shutdown();assert(not mission and not publish and not gateOpen and not turnBegin and units[40] and destroys==0)")
    def test_completion_event_is_read_only_bounded_and_never_attributed(self):
        l=gate(window=True);l.execute("gateOpen();Controls.CreateButton.click();for i=1,105 do mission(2,i)end;Controls.RefreshButton.click();assert(Controls.Report.text:find('EVENTS:99,UNKNOWN') and properties==0 and nativeCalls==0 and destroys==0)")
    def test_native_rejection_report_does_not_send_dispatch(self):
        l=gate(window=True);l.execute("gateOpen();Controls.CreateButton.click();nativeAllow=false;local n=sent;Controls.ArmButton.click();assert(sent==n and nativeCalls==0 and Controls.Report.text:find('TIMING'))")
    def test_timeout_does_not_retry(self):
        l=gate(window=True);l.execute("gateOpen();deferred=true;Controls.CreateButton.click();local n=sent;update(11);publish();assert(sent==n and nativeCalls==0 and Controls.Report.text:find('TIMEOUT'))")

class Package(unittest.TestCase):
    def test_sql_exact_new_type_ordinary_spy_operations_globals_and_modifiers_unchanged(self):
        p=external_database(R);src=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');src.backup(db);src.close();db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
        k='UNIT_SPC_EXPEDITION_SPY'
        for table,col in [('TypeTags','Type'),('Units','UnitType'),('Types','Type')]:db.execute(f'delete from {table} where {col}=?',(k,))
        tables=['Units','UnitOperations','GlobalParameters','Modifiers','ModifierArguments','UnitAbilities','UnitAbilityModifiers']
        before={t:db.execute(f'select * from {t} order by 1').fetchall() for t in tables}
        db.executescript((R/'Mod/Data/ExpeditionSpyGate.sql').read_text())
        for t in tables:
            after=db.execute(f'select * from {t}'+(' where UnitType != ?' if t=='Units' else '')+' order by 1',(k,) if t=='Units' else ()).fetchall();self.assertEqual(before[t],after,t)
        self.assertEqual(db.execute('select Spy,IgnoreMoves,Stackable,CanTrain,CanCapture,CanRetreatWhenCaptured,CanEarnExperience,PromotionClass from Units where UnitType=?',(k,)).fetchone(),(1,1,1,0,0,0,0,'PROMOTION_CLASS_SPY'))
        self.assertEqual(db.execute('select Tag from TypeTags where Type=?',(k,)).fetchall(),[('CLASS_LANDCIVILIAN',)])
        db.close()
    def test_package_active_entry_points_art_and_localization(self):
        m=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot();self.assertEqual(m.attrib['version'],'221')
        files=[e.text for e in m.findall('./Files/File')];self.assertEqual(len(files),len(set(files)))
        for e in m.findall('.//File'):self.assertTrue((R/'Mod'/e.text).is_file(),e.text)
        active=[e.text for e in m.findall('./InGameActions/AddUserInterfaces/File')]
        self.assertIn('UI/ExpeditionSpyActivity.xml',active);self.assertIn('UI/ExpeditionSpyWindow.xml',active);self.assertNotIn('UI/ExpeditionGateWindow.xml',active)
        code=(R/'Mod/Gameplay.lua').read_text();self.assertIn('SPCExpeditionSpyGate.Start(P,shared)',code);self.assertNotIn('SPCExpeditionGate.Start(P,shared)',code)
        art=ET.parse(R/'Mod/ArtDefs/Units.artdef').getroot();names=[e.attrib['text'] for e in art.findall('m_RootCollections/Element/Element/m_Name')];self.assertEqual(names.count('UNIT_SPC_EXPEDITION_SPY'),1);self.assertEqual(len(names),8)
        db=sqlite3.connect(':memory:');db.execute('create table LocalizedText(Language text,Tag text,Text text,primary key(Language,Tag))');db.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
        lua=(R/'Mod/UI/ExpeditionSpyWindow.lua').read_text();xml=(R/'Mod/UI/ExpeditionSpyWindow.xml').read_text()
        keys=set(re.findall(r"L\('([A-Z_]+)'",lua));keys-={'PHASE_','COMPARE_','IDENTITY_','NAME_STAGE_','ACTIVITY_','ACTIVITY_CAUSE_','DIAGNOSTIC_','FAILURE_DIAGNOSTIC_PHASE_'}
        keys|={f'PHASE_{p}' for p in ['IDLE','CREATING','NAMING','CREATED','TRAVELLING','ARRIVED','TASK_PREPARING','TASK_RUNNING','TASK_COMPLETE','HELD','ENDING','ENDED']}
        keys|={f'COMPARE_{p}' for p in ['UNKNOWN','CHANGED','PARTIAL','SCOPED_UNCHANGED','SLOT_COST_ACCEPTED']}
        keys|={f'IDENTITY_{p}' for p in ['MATCH','ABSENT','MISMATCH','UNREADABLE','NO_UNIT','NO_SESSION','WRONG_UNIT','AMBIGUOUS','PRESENT','OFF_MAP']}
        keys|={f'NAME_STAGE_{p}' for p in ['READINESS','READING','GAMEPLAY','CONFIRMED','CANCELLED']}
        keys|={f'ACTIVITY_{p}' for p in ['SLEEP','ASLEEP','RELEASE','NONE','BLOCKED']}
        keys|={f'ACTIVITY_CAUSE_{p}' for p in ['DATA','API','DENIED']}
        keys|={f'DIAGNOSTIC_{p}' for p in ['ALLOWED','DENIED','UNKNOWN']}
        keys|={f'FAILURE_DIAGNOSTIC_PHASE_{p}' for p in ['PRE_REQUEST_GUARD','POST_REQUEST_READBACK','PENDING_TIMEOUT','UNKNOWN']}
        keys|={'FAILURE_DIAGNOSTIC_HEADER','FAILURE_DIAGNOSTIC_ACTIVITY','FAILURE_DIAGNOSTIC_TIMEOUT_HEADER','FAILURE_DIAGNOSTIC_TIMEOUT_ACTIVITY'}
        keys|={'HELD_MATCH','HELD_RECHECK','HELD_SOURCE','ACTIVITY_FAILURE'}
        for k in keys:self.assertEqual(db.execute('select count(*) from LocalizedText where Tag=?',('LOC_SPC_EXPEDITION_SPY_'+k,)).fetchone()[0],2,k)
        for key in re.findall(r'String="(LOC_[A-Z0-9_]+)"',xml):self.assertEqual(db.execute('select count(*) from LocalizedText where Tag=?',(key,)).fetchone()[0],2,key)
        db.close()

if __name__=='__main__':unittest.main()
