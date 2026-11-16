"""B412 removable observations. Native-shaped controls, never native proof PASS."""
from contextlib import nullcontext
from pathlib import Path
import tempfile,unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,PackageVFS,TrackedLua51,legacy_source_observation,measure
from test_expedition_trace_collector import collector

NATIVE=r"""
turn=10;reads=0;writes=0;requests=0;prints={};print=function(s)prints[#prints+1]=s end
Game.GetLocalPlayer=function()return 0 end
GameConfiguration={IsAnyMultiplayer=function()return false end,GetGameSpeedType=function()return 'STANDARD'end}
PlayerConfigurations={[0]={GetCivilizationTypeName=function()return 'CIVILIZATION_SPC_AMERICA'end,GetLeaderTypeName=function()return 'LEADER_SPC_T_ROOSEVELT'end}}
GameInfo={Projects={},GameSpeeds={STANDARD={CostMultiplier=100}}}
CityProductionDirectives={PROJECT=3};CityProductionTypes={PROJECT=3};PlayerOperations={EXECUTE_SCRIPT=1}
local index=100;nativeCompleted={};cityMap={};receipts={version=2,water={},pending={}}
for tier in ipairs(SPCCrewModel.CAPACITY)do for _,ratio in ipairs(SPCCrewModel.RATIOS)do
 local name=SPCCrewModel.Project(tier,ratio);index=index+1
 local row={ProjectType=name,Index=index,Hash=index,Cost=390};GameInfo.Projects[index]=row;GameInfo.Projects[name]=row;nativeCompleted[index]=0
end end
project=SPCCrewModel.Project(1,150);projectIndex=GameInfo.Projects[project].Index
for id=1,2 do
 local c={id=id};c.raw={version=1,source='SOURCE_'..id,owner=0,x=id,y=0,serial=1,orders={{serial=1,stage='QUEUED',project=project,base=0,capacity=260,price=390}}}
 local q={size=1,progress=50}
 function q:GetSize()reads=reads+1;return self.size end
 function q:GetAt(i)reads=reads+1;assert(i==0);return {Directive=3,ProjectType=projectIndex}end
 function q:GetProjectCost(i)reads=reads+1;return 390 end
 function q:GetProjectProgress(i)reads=reads+1;return i==projectIndex and self.progress or 0 end
 function c:GetOwner()reads=reads+1;return 0 end;function c:GetID()return self.id end
 function c:GetX()return self.id end;function c:GetY()return 0 end
 function c:GetProperty(key)reads=reads+1;assert(key==SPCCrewModel.ORDER_PROPERTY);return self.raw end
 function c:SetProperty()writes=writes+1;error('PROBE_WRITE_FORBIDDEN')end
 function c:GetBuildQueue()reads=reads+1;return q end
 c.q=q;cityMap[id]=c
end
local collection={FindID=function(_,id)reads=reads+1;return cityMap[id]end}
Players={[0]={IsHuman=function()return true end,GetCities=function()reads=reads+1;return collection end,
 GetProperty=function(_,key)reads=reads+1;assert(key==SPCCrewModel.RECEIPT_PROPERTY);return receipts end,
 SetProperty=function()writes=writes+1;error('PROBE_WRITE_FORBIDDEN')end,
 GetStats=function()reads=reads+1;return {GetNumProjectsAdvanced=function(_,index)reads=reads+1;return nativeCompleted[index]end}end}}
UI={GetHeadSelectedCity=function()return cityMap[1]end,RequestPlayerOperation=function()requests=requests+1;error('PROBE_OPERATION_FORBIDDEN')end}
ExposedMembers.SPC_P0={CrewProjects={errors={},views={}}}
for id=1,2 do ExposedMembers.SPC_P0.CrewProjects.views['0:'..id]={owner=0,city=id,reserved=1,queued=1,retained={[project]={stage='QUEUED'}}}end
function proofRows(stage,phase)
 local a={};local trace=ExposedMembers.SPC_B205TrainingTrace
 for _,row in ipairs(trace and trace.entries or {})do if row.stage==stage and(not phase or row.phase==phase)then a[#a+1]=row end end
 return a
end
function fire(...)Events.CityProjectCompleted.Fire(...)end
"""

def pure(side='GAMEPLAY',enabled=True):
    c=Context();c.load('Probe');c.load('CrewModel');c.execute(NATIVE)
    c.load('ExpeditionTrainingDiagnostics');c.load('CrewCompletionDiagnostics');c.execute('SPCCrewCompletionDiagnostics.ENABLED=...',enabled)
    if side=='GAMEPLAY':c.execute("probe=SPCCrewCompletionDiagnostics.Start(SPCP0,'GAMEPLAY')")
    c.load('UI/CrewProjectUI');c.execute('ui=SPCCrewProjectUI.New(SPCP0,UI.RequestPlayerOperation,function()end,function()requests=requests+1;error("BUILD_FORBIDDEN")end)')
    if side=='UI':c.execute("probe=SPCCrewCompletionDiagnostics.Start(SPCP0,'UI')")
    return c

def actual(mode='on',dispatch='tombstone'):
    import test_b236_crews as crews
    from test_refactor_s7d5 import profile
    text=(ROOT/'Mod/Gameplay.lua').read_text();start=text.index('-- B412 removable observation seams');end=text.index("composition.Run('CrewProjects'",start)
    before=text[start:end];after="pcall(function()if crewCompletionObservation then crewCompletionObservation.After()end end)"
    source=crews.SETUP.replace('C.install();SPCCrewProjects.Start(P,shared);','C.install();'+before+'SPCCrewProjects.Start(P,shared);'+after+';')
    assert source!=crews.SETUP
    with profile(),patch.object(crews,'SETUP',source):v=crews.crew_runtime()
    # Install dispatch semantics BEFORE the observer captures registrations.
    v.execute("""
     print=function()end;Game.GetLocalPlayer=function()return 0 end
     dispatch=...;removes=0
     for _,name in ipairs({'CityProjectCompleted','CityProductionChanged','CityProductionCompleted','GameCoreEventPublishComplete'})do
      local e=Events[name]
      e.Remove=function(fn)removes=removes+1;for i=1,#e.list do if e.list[i]==fn then
       if dispatch=='tombstone'then e.list[i]=function()end else table.remove(e.list,i)end;break end end end
      e.Fire=function(...)
       local a=e.list;if dispatch=='snapshot'then a={};for i,fn in ipairs(e.list)do a[i]=fn end end
       for _,fn in ipairs(a)do fn(...)end
      end
     end
    """,dispatch)
    v.execute((ROOT/'Mod/ExpeditionTrainingDiagnostics.lua').read_text())
    if mode!='absent':v.execute((ROOT/'Mod/CrewCompletionDiagnostics.lua').read_text())
    if mode=='off':v.execute('SPCCrewCompletionDiagnostics.ENABLED=false')
    def include(name):
        if mode=='absent' and name=='CrewCompletionDiagnostics':raise FileNotFoundError('EXPECTED_OPTIONAL_ABSENCE')
        return v.execute((ROOT/'Mod'/(name+'.lua')).read_text())
    v.globals().include=include
    v.execute("""
     c=C.make();other=H.city(2);other.buildings[10]=true;H.district(other,'DISTRICT_INDUSTRIAL_ZONE',true)
     for i=1,3 do T.invest(other,9700+i)end;C.queue(other);crew.Refresh(0,other:GetID())
     mutationLog={};local set=P.SetProperty;P.SetProperty=function(o,k,payload)mutationLog[#mutationLog+1]=k..':'..T.encode(payload);return set(o,k,payload)end
     function state()
      local units={};for id,u in pairs(C.units)do units[id]=u:GetProperty(SPCCrewModel.UNIT_PROPERTY)end
      return T.encode({a=c:GetProperty(SPCCrewModel.ORDER_PROPERTY),b=other:GetProperty(SPCCrewModel.ORDER_PROPERTY),receipts=C.props,units=units,calls=C.calls})
     end
    """)
    return v

class Probe(unittest.TestCase):
    def test_before_after_and_one_publish_followup_record_raw_and_committed_views(self):
        c=pure();c.execute("""
         Events.CityProjectCompleted.Add(function(pid,id,index)
          if pid==0 and id==1 and index==projectIndex then
           cityMap[1].raw.orders={};receipts.water[project]=1;nativeCompleted[projectIndex]=1;cityMap[1].q.size=0
          end
         end);probe.After();fire(0,1,projectIndex,nil,false,7)
         local a=proofRows('CREW_PROOF_EVENT');assert(#a==2 and a[1].phase=='BEFORE_CREW'and a[2].phase=='AFTER_CREW')
         assert(a[1].eventCount=='6'and a[1].eventBatch:find('4:nil:NIL',1,true)and a[1].eventBatch:find('5:boolean:false',1,true))
         local s=proofRows('CREW_PROOF_STATE');assert(s[1].eventBatch:find('QUEUED',1,true)and s[1].completed=='0')
         assert(s[2].eventBatch=='NO_ORDER_ROWS'and s[2].completed=='1'and s[2].controlState:find('water:1',1,true))
         publish();assert(#proofRows('CREW_PROOF_STATE','FOLLOWUP')==1)
         local n=reads;for i=1,1000 do publish()end;assert(reads==n and writes==0 and requests==0)
        """)
    def test_real_ui_factory_attaches_one_observer_and_reads_existing_reader(self):
        c=pure('UI');c.execute("fire(0,1,projectIndex);local s=proofRows('CREW_PROOF_STATE');assert(#s==1 and s[1].observerSide=='UI'and s[1].reader=='RETURNED_CURRENT');local n=Events.CityProjectCompleted.Count();SPCCrewProjectUI.New(SPCP0,UI.RequestPlayerOperation,function()end,function()end);assert(Events.CityProjectCompleted.Count()==n and writes==0 and requests==0)")
    def test_disabled_before_start_has_no_hooks_output_or_native_reads(self):
        c=pure(enabled=False);c.execute("local n=reads;for i=1,1000 do fire(0,1,projectIndex);publish()end;assert(reads==n and probe==nil and ExposedMembers.SPC_B205TrainingTrace==nil and writes==0 and requests==0)")
    def test_stop_or_disable_leaves_inert_fixed_listeners(self):
        for mode in ('stop','disable'):
            c=pure();c.execute('business=0;Events.CityProjectCompleted.Add(function()business=business+1 end);probe.After()')
            c.execute('SPCCrewCompletionDiagnostics.Stop()'if mode=='stop'else'SPCCrewCompletionDiagnostics.ENABLED=false;fire(0,1,projectIndex)')
            c.execute("local n=reads;local prior=business;for i=1,1000 do fire(0,1,projectIndex);publish()end;assert(reads==n and business==prior+1000 and not probe.Stats().live and writes==0 and requests==0)")
    def test_foreign_irrelevant_events_do_not_visit_cities_or_sample_queues(self):
        c=pure();c.execute("local n=reads;for i=1,1000 do fire(1,1,projectIndex);publish()end;assert(reads==n and probe.Stats().samples==0 and writes==0 and requests==0)")
    def test_unresolved_project_index_in_known_crew_city_is_visible_not_proof(self):
        c=pure();c.execute("fire(0,1,999999);local a=proofRows('CREW_PROOF_EVENT');assert(#a==1 and a[1].projectType==nil and a[1].eventBatch:find('3:number:999999',1,true));assert(writes==0 and requests==0)")
    def test_missing_city_known_crew_event_is_logged_without_guess_or_retry(self):
        c=pure();c.execute("cityMap[1]=nil;fire(0,1,projectIndex);local e=proofRows('CREW_PROOF_EVENT');local s=proofRows('CREW_PROOF_STATE');assert(#e==1 and s[1].reader=='CITY_UNAVAILABLE'and s[1].readStatus=='ORDER_READ_ERROR');local n=reads;for i=1,1000 do publish()end;assert(reads==n)")
    def test_extra_arguments_and_native_objects_are_bounded_without_stringification(self):
        c=pure();c.execute("local bad=setmetatable({},{__tostring=function()error('OBJECT_STRINGIFICATION')end});fire(0,1,projectIndex,nil,false,bad,function()end,'PRIVATE_PLAYER_NAME',1,2,3,4,5,6);local e=proofRows('CREW_PROOF_EVENT')[1];assert(e.eventCount=='14'and e.eventTruncated=='true'and e.eventBatch:find('OMITTED_table',1,true)and not e.eventBatch:find('PRIVATE_PLAYER_NAME',1,true));assert(#e.eventBatch<1800 and writes==0 and requests==0)")
    def test_reader_throw_or_stale_scope_is_observation_only_and_not_retried(self):
        for setup,status in (("ExposedMembers.SPC_CrewNativeRead=function()error('PRIVATE_PATH')end",'READ_ERROR'),("ExposedMembers.SPC_CrewNativeRead=function()return {owner=0,city=2,turn=turn}end",'STALE_OR_WRONG_SCOPE'),('ExposedMembers.SPC_CrewNativeRead=nil','UNAVAILABLE')):
            c=pure();c.execute(setup+";fire(0,1,projectIndex)")
            self.assertEqual(c.eval("proofRows('CREW_PROOF_STATE')[1].reader"),status)
            c.execute('local n=reads;for i=1,1000 do publish()end;assert(reads==n and writes==0 and requests==0)')
    def test_exact_pending_order_receipt_is_visible_without_root_enumeration(self):
        c=pure();c.execute("local key=SPCCrewModel.ReceiptKey('SOURCE_1',1);receipts.water[project]=1;receipts.pending[key]={stage='CALLING',count=1};fire(0,1,projectIndex);local e=proofRows('CREW_PROOF_STATE')[1];assert(e.eventBatch:find(':CALLING:1',1,true)and e.writerState:find('SOURCE_1',1,true)and e.controlState:find('water:1',1,true));assert(writes==0)")
    def test_all_limits_stop_with_explicit_truncation_and_no_budget_replenishment(self):
        for limit,value in (('EVENT_LIMIT',1),('VISIT_LIMIT',1),('SAMPLE_LIMIT',1),('ROW_LIMIT',2),('CITY_LIMIT',1)):
            c=pure();c.execute('local key,value=...;SPCCrewCompletionDiagnostics[key]=value',limit,value)
            c.execute("fire(0,1,projectIndex);fire(0,2,projectIndex);fire(0,1,projectIndex);publish();local a=proofRows('CREW_PROOF_STATUS');assert(a[#a].point=='STOP'and a[#a].eventTruncated=='true');local n=reads;for i=1,1000 do fire(0,1,projectIndex);publish()end;assert(reads==n and not probe.Stats().live);SPCCrewCompletionDiagnostics.Start(SPCP0,'GAMEPLAY');assert(not probe.Stats().live)")
    def test_window_arms_on_first_verified_completion_not_loading_and_has_fresh_reload(self):
        c=pure();c.execute("turn=80;fire(0,1,projectIndex);assert(probe.Stats().live);turn=86;fire(0,1,projectIndex);assert(not probe.Stats().live);local n=reads;publish();assert(reads==n)")
        fresh=pure();fresh.execute('turn=86;fire(0,1,projectIndex);assert(probe.Stats().live and probe.Stats().events==1)')
    def test_missing_remove_is_supported_and_missing_logger_adds_no_dependency(self):
        c=Context();c.load('CrewCompletionDiagnostics');c.execute("n=Events.CityProjectCompleted.Count();assert(SPCCrewCompletionDiagnostics.Start({},'GAMEPLAY')==nil and Events.CityProjectCompleted.Count()==n)")
        c=pure(enabled=False);c.execute("SPCCrewCompletionDiagnostics.ENABLED=true;Events.CityProjectCompleted.Remove=nil;probe=SPCCrewCompletionDiagnostics.Start(SPCP0,'GAMEPLAY');assert(Events.CityProjectCompleted.Count()==1);SPCCrewCompletionDiagnostics.Stop();local n=reads;fire(0,1,projectIndex);assert(reads==n)")
    def test_missing_hooks_and_constructor_failure_are_visible_or_inert(self):
        c=pure(enabled=False);c.execute("SPCCrewCompletionDiagnostics.ENABLED=true;Events.CityProjectCompleted.Add=nil;probe=SPCCrewCompletionDiagnostics.Start(SPCP0,'GAMEPLAY');local a=proofRows('CREW_PROOF_STATUS');assert(a[1].point=='HOOK_UNAVAILABLE'and a[1].reason=='CityProjectCompleted')")
        c=pure(enabled=False);c.execute("SPCCrewCompletionDiagnostics.ENABLED=true;SPCExpeditionTrainingDiagnostics.New=function()error('PRIVATE_FACTORY_FAILURE')end;assert(SPCCrewCompletionDiagnostics.Start(SPCP0,'GAMEPLAY')==nil and Events.CityProjectCompleted.Count()==0)")
    def test_order_excerpt_limit_is_explicit_and_never_changes_saved_rows(self):
        c=pure();c.execute("for i=2,10 do cityMap[1].raw.orders[i]={serial=i,stage='PAUSED',project=project,base=0,price=390,capacity=260}end;fire(0,1,projectIndex);local e=proofRows('CREW_PROOF_STATE')[1];assert(e.eventTruncated=='true'and #cityMap[1].raw.orders==10 and writes==0)")

class ProductionIsolation(unittest.TestCase):
    def test_actual_store_crew_native_results_and_mutation_order_match_on_off_absent(self):
        results=[]
        for mode in ('on','off','absent'):
            with legacy_source_observation():v=actual(mode)
            v.execute("p=C.begin(c);C.begin(other);C.complete(c,p);C.complete(other,p);snapshot=state();for i=1,5 do Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index)end;assert(state()==snapshot and C.calls==2)")
            results.append((v.eval('snapshot'),list(v.globals().mutationLog.values())))
        self.assertEqual(results[0],results[1]);self.assertEqual(results[0],results[2])
    def test_probe_cannot_turn_shared_counter_ambiguity_into_extra_grants(self):
        for mode in ('on','off','absent'):
            with legacy_source_observation():v=actual(mode)
            v.execute("p=C.begin(c);C.begin(other);c:GetBuildQueue().items[p]=nil;other:GetBuildQueue().items[p]=nil;C.stats[p]=2;Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);Events.CityProjectCompleted.Fire(0,other:GetID(),C.rows.Projects[p].Index);assert(C.calls==0 and crew.errors['0:'..c:GetID()]=='CREW_COMPLETION_SEQUENCE_AMBIGUOUS')")
    def test_actual_gameplay_roots_load_with_probe_disabled_or_file_truly_absent(self):
        from test_pu11_package_absence import root,NATIVE
        for mode in ('off','throw','silent_nil'):
            if mode=='off':
                c=Context(vfs=PackageVFS());c.execute(NATIVE);c.load('CrewCompletionDiagnostics');c.execute('SPCCrewCompletionDiagnostics.ENABLED=false');c.load('Gameplay')
            else:c=root(profile=PackageVFS(absent=['CrewCompletionDiagnostics'],missing_include=mode,forbidden_globals=['SPCCrewCompletionDiagnostics']))
            self.assertEqual(c.eval('ExposedMembers.SPC_P0.StartStatus.CrewProjects.state'),'OK')
            self.assertIsNone(c.globals().ExposedMembers.SPC_CrewCompletionAuthority)
    def test_actual_ui_factory_survives_true_file_and_global_absence(self):
        for mode in ('throw','silent_nil'):
            c=Context(vfs=PackageVFS(absent=['CrewCompletionDiagnostics'],missing_include=mode,forbidden_globals=['SPCCrewCompletionDiagnostics']))
            c.load('Probe');c.load('CrewModel');c.execute(NATIVE);c.load('ExpeditionTrainingDiagnostics');c.load('UI/CrewProjectUI')
            c.execute('ui=SPCCrewProjectUI.New(SPCP0,UI.RequestPlayerOperation,function()end,function()end);assert(type(ExposedMembers.SPC_CrewNativeRead)=="function"and type(ui.Before)=="function"and Events.CityProjectCompleted.Count()==0 and writes==0 and requests==0)')
            self.assertIsNone(c.globals().SPCCrewCompletionDiagnostics)
    def test_existing_zero_and_positive_progress_cancel_remain_original_owner_rules(self):
        for progress in (0,50):
            states=[]
            for mode in ('on','off','absent'):
                with legacy_source_observation():v=actual(mode)
                v.execute("p=C.begin(c);c:GetBuildQueue().progressByProject[p]=...;c:GetBuildQueue().items[p]=nil;Events.CityProductionChanged.Fire(0,c:GetID());Events.GameCoreEventPublishComplete.Fire();result=state()",progress)
                states.append(v.eval('result'))
            self.assertEqual(states[0],states[1]);self.assertEqual(states[0],states[2])

class Collector(unittest.TestCase):
    def test_real_logger_reader_collector_roundtrip_and_summary(self):
        c=pure();c.execute('probe.After();fire(0,1,projectIndex,nil,false);publish()')
        lines=list(c.globals().prints.values());records=[collector.train_line(line)for line in lines];self.assertTrue(all(records))
        with tempfile.TemporaryDirectory(dir=ROOT/'local')as directory:
            s=collector.Session(Path(directory),stamp='CREW-PROOF')
            try:
                for record in records:s.add(record,'test')
                summary=s.summary('TEST');raw=(s.directory/'records.log').read_text()
                self.assertIn('crew_proof_scope:',summary);self.assertIn('BEFORE_CREW',summary)
                self.assertIn('eventCount=5',raw);self.assertIn('4:nil:NIL',raw)
                self.assertIn('writerState=source:SOURCE_1',raw);self.assertIn('controlState=receipt:2',raw)
                self.assertIn('not a gameplay PASS',summary);self.assertIn('no completion-instance or native uniqueness PASS',summary)
            finally:s.close()
    def test_probe_and_summary_truncation_are_explicit_without_protocol_changes(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'local')as directory:
            s=collector.Session(Path(directory),stamp='CREW-CAP')
            try:
                for n in range(100):s.add('[SPC][B205][TRAIN] seq=%d stage=CREW_PROOF_EVENT observerSide=GAMEPLAY point=CityProjectCompleted eventCount=14 eventTruncated=true'%n,'test')
                text=s.summary('TEST');self.assertEqual(len(s.crew_proof_rows),96)
                self.assertIn('CREW_PROOF_TRUNCATED',text);self.assertIn('crew_proof_summary_truncated:',text)
                self.assertEqual(s.record_total,100)
            finally:s.close()

if __name__=='__main__':unittest.main()
