"""B394 optional scalar observer: real-path differential, not native game proof."""
from pathlib import Path
import json
from hashlib import sha256
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from lupa.lua51 import LuaRuntime
from test_refactor_s7a2 import fixture as gpp_fixture
from timed_project_ui_fixture import fixture as project_fixture
from test_expedition_training import fixture as training_fixture
from test_expedition_spy_recovery_activity import recovery_bridge

ROOT=Path(__file__).resolve().parents[1]
OBS=(ROOT/'Mod/CultureDiagnostics.lua').read_text()
MODES=('off','on','absent','throw','lookup','sink','construct','classify')

def install(lua,mode):
    lua.execute('SPCCultureDiagnostics=nil')
    lua.execute(OBS)
    lua.execute('''
      diagRows={};diagStarts=0
      SPCExpeditionTrainingDiagnostics={New=function(_,role)
       diagStarts=diagStarts+1
       return {Record=function(stage,fields)
        local row={stage=stage};for k,v in pairs(fields)do row[k]=v end
        diagRows[#diagRows+1]=row
       end}
      end}
    ''')
    if mode=='off':lua.execute('SPCCultureDiagnostics.ENABLED=false')
    elif mode=='absent':lua.execute('SPCCultureDiagnostics=nil')
    elif mode=='throw':lua.execute("SPCCultureDiagnostics.Emit=function()error('OPTIONAL_OBSERVER_FAILED',0)end")
    elif mode=='lookup':lua.execute("SPCCultureDiagnostics=setmetatable({},{__index=function()error('OBSERVER_LOOKUP_FAILED',0)end})")
    elif mode=='sink':lua.execute("SPCExpeditionTrainingDiagnostics.New=function()return {Record=function()error('SINK_FAILED',0)end}end")
    elif mode=='construct':lua.execute("SPCExpeditionTrainingDiagnostics.New=function()error('CONSTRUCTOR_FAILED',0)end")
    elif mode=='classify':lua.execute("SPCCultureDiagnostics.Error=function()error('CLASSIFIER_FAILED',0)end")


def vector(lua,expr):
    return tuple(lua.eval(expr).values())


class Isolation(unittest.TestCase):
    def test_real_gpp_native_reads_writes_and_effects_match_all_modes(self):
        outcomes=[]
        for mode in MODES:
            l=gpp_fixture();install(l,mode)
            l.execute('''
              workerReads=0;local get=Map.GetPlot
              Map.GetPlot=function(...)local p=get(...);local read=p.GetWorkerCount
               p.GetWorkerCount=function(...)workerReads=workerReads+1;return read(...)end;return p end
            ''')
            l.execute('''
              result={}
              for _,n in ipairs({0,1,2,2,1,0,3})do count=n;gppAudit();result[#result+1]=gpp()end
              local before=#log;count=nil;shared.Lv2GPP.Audit({player=0,city=0})
              assert(#log==before and shared.Lv2GPP.errors['0:0'])
              count=2;gppAudit();assert(gpp()==4)
            ''')
            outcomes.append((vector(l,'result'),tuple(l.globals().log.values()),dict(l.globals().counts),l.eval('workerReads')))
            if mode=='on':
                l.execute("assert(#diagRows>0);local seen=false;for _,r in ipairs(diagRows)do if r.point=='GPP_APPLIED'then assert(r.expectedNumber==r.actualNumber and type(r.city)=='number');seen=true end end;assert(seen)")
            elif mode in ('off','absent','throw','lookup'):self.assertEqual(l.eval('#diagRows'),0)
        self.assertTrue(all(v==outcomes[0]for v in outcomes),outcomes)

    def test_real_dialogue_queue_failure_recovery_and_start_match(self):
        outcomes=[]
        for mode in MODES:
            l=project_fixture('Dialogue',connect=False);install(l,mode)
            l.execute('''
              ui.Connect();pumpUI();pumpUI()
              assert(selectUI());q.target=project;unreadable=true;ownEventUI();pumpUI()
              unreadable=false;local before=uiReads;idleUI(1000);assert(uiReads==before)
              ownEventUI();pumpUI();assert(uiBegins==1);pumpUI();assert(uiBegins==1)
              result={uiReads,uiBegins,uiSyncs,uiMembers,uiFinds,uiCollections,pending()and pending().stage or 'NONE'}
            ''')
            outcomes.append(vector(l,'result'))
            if mode=='on':
                l.execute("local failed,committed=false,false;for _,r in ipairs(diagRows)do if r.point=='UI_QUEUE_READ'and r.requestAccepted==false then failed=true end;if r.point=='DIALOGUE_BEGIN_COMMITTED'then committed=true end end;assert(failed and committed)")
        self.assertTrue(all(v==outcomes[0]for v in outcomes),outcomes)

    def test_native_no_start_completion_protection_is_unchanged(self):
        from test_refactor_s7d1 import profile
        from test_dialogue_projects import game
        outcomes=[]
        for mode in MODES:
            with profile():l=game()
            install(l,mode)
            l.execute("c.q.target='PROJECT_SPC_ERA_DIALOGUE';Events.CityProjectCompleted.Fire(0,c:GetID(),999);assert(not ledger(c));result={T.writes(),finishes}")
            outcomes.append(vector(l,'result'))
        self.assertTrue(all(v==outcomes[0]for v in outcomes),outcomes)

    def test_real_training_unreserved_birth_never_adopted(self):
        outcomes=[]
        for mode in MODES:
            import test_expedition_training as training
            import test_expedition_gate as base
            original=training.gate
            def prepared():
                vm=original()
                def include(name):vm.execute((ROOT/'Mod'/(name+'.lua')).read_text())
                vm.globals().include=include
                return vm
            with patch.object(base,'LuaRuntime',LuaRuntime),patch.object(training,'gate',prepared):l=training_fixture()
            install(l,mode)
            l.execute("born();assert(state().phase==nil);result={storeWrites,markerWrites,initCalls,state().phase or 'NONE'}")
            outcomes.append(vector(l,'result'))
            if mode=='on':l.execute("assert(#diagRows>=2);assert(diagRows[#diagRows].point=='EXPEDITION_BIRTH_STATE'and diagRows[#diagRows].ready==false)")
        self.assertTrue(all(v==outcomes[0]for v in outcomes),outcomes)

    def test_real_activity_recovery_all_states_and_displacement_match(self):
        for state in (0,1,2,3,8,'nil'):
            outcomes=[]
            for mode in MODES:
                l=recovery_bridge();install(l,mode)
                l.execute(f"units[41].activity={state};noRecoveryAck=true;publish('RECOVER',true);for i=1,1000 do Events.GameCoreEventPublishComplete()end;result={{#acks,sleepCalls,wakeCalls,sleepChecks,wakeChecks,acks[1]and acks[1].Result or 'NONE'}}")
                outcomes.append(vector(l,'result'))
            self.assertTrue(all(v==outcomes[0]for v in outcomes),(state,outcomes))
        for mode in MODES:
            l=recovery_bridge();install(l,mode)
            l.execute("units[41].x=99;publish('RECOVER',true);assert(#acks==1 and acks[1].Result=='FAILED'and sleepCalls==0 and wakeCalls==0)")
            if mode=='on':l.execute("local found=false;for _,r in ipairs(diagRows)do if r.point=='EXPEDITION_ACTIVITY_READ'then found=true;assert(r.actualX==99 and r.readStatus=='READ_ERROR')end end;assert(found)")

    def test_move_event_coordinates_do_not_replace_native_readback(self):
        for mode in ('off','on','absent','throw'):
            l=recovery_bridge();install(l,mode)
            l.execute("units[41].activity=3;noRecoveryAck=true;publish('RECOVER',true);Events.UnitMoveComplete(2,41,99,97);assert(#acks==0 and sleepCalls==0 and wakeCalls==0 and units[41].x==15)")
            if mode=='on':
                l.execute("local move,read=false,false;for _,r in ipairs(diagRows)do if r.point=='EXPEDITION_MOVE_EVENT'then move=true;assert(r.eventX==99 and r.eventY==97 and r.actualX==nil)end;if r.point=='EXPEDITION_ACTIVITY_READ'then read=true;assert(r.actualX==15)end end;assert(move and read)")

    def test_deleted_optional_module_does_not_prevent_loading(self):
        l=LuaRuntime();l.execute("include=function()error('OPTIONAL_FILE_REMOVED',0)end")
        for name in ('Mod/CultureDiagnostics.lua','Mod/UI/TimedProjectSelectionClient.lua','Mod/TimedProjectReaders.lua'):
            if name.endswith('CultureDiagnostics.lua'):continue
            # Only the optional include is removed; required RuntimeWork is a fixture stub.
            l.execute("include=function(name)if name=='CultureDiagnostics'then error('OPTIONAL_FILE_REMOVED',0)end end")
            l.execute((ROOT/name).read_text())
        self.assertTrue(l.eval("type(SPCTimedProjectReaders.New)=='function'and type(SPCTimedProjectSelectionClient.New)=='function'"))


    def test_baseline_and_instrumented_real_dialogue_are_equal(self):
        original=Path.read_text
        names=('DialogueProjects.lua','TimedProjectReaders.lua','UI/DialogueProjectUI.lua','UI/TimedProjectSelectionClient.lua')
        prior={ROOT/'Mod'/n:subprocess.check_output(['git','show','c99ec22:Mod/'+n],cwd=ROOT,text=True)for n in names}
        from refactor_harness import TrackedLua51,SOURCES
        native_execute=TrackedLua51.execute
        historical={sha256(v.encode()).hexdigest():'historical/c99ec22/'+str(p.relative_to(ROOT))for p,v in prior.items()}
        outcomes=[]
        for before in (True,False):
            def read(path,*a,**kw):return prior[path]if before and path in prior else original(path,*a,**kw)
            def execute(vm,source,*a,**kw):
                digest=sha256(source.encode()).hexdigest()
                if before and digest in historical:SOURCES[digest]=historical[digest]
                return native_execute(vm,source,*a,**kw)
            with patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',execute):l=project_fixture('Dialogue',connect=True)
            install(l,'off')
            l.execute("assert(selectUI());q.target=project;unreadable=true;ownEventUI();pumpUI();unreadable=false;idleUI(1000);ownEventUI();pumpUI();assert(uiBegins==1);result={snapshot(),uiReads,uiBegins,uiSyncs,uiMembers,uiFinds,uiCollections}")
            outcomes.append(vector(l,'result'))
        self.assertEqual(*outcomes)

    def test_real_ordinary_unit_replacement_keeps_existing_pending_failure(self):
        for mode in ('off','on','absent','throw'):
            l=project_fixture('Dialogue',connect=True);install(l,mode)
            include=l.globals().include
            def panel_include(name):
                if name in ('SafeAdapters','IdentityEqual'):return include(name)
                if name=='CultureDiagnostics':return
                return None  # Thin HD/base UI surface; unrelated adapter factories remain unavailable.
            l.globals().include=panel_include
            l.execute("""
              ContextPtr={SetShutdown=function(self,fn)panelShutdown=fn end,IsHidden=function()return false end}
              SPCP0=P;SPCDialogueProjectUI.New=function()return ui end
              baseAdvances=0;nativeBuilds=0
              AdvanceProject=function(c,item)baseAdvances=baseAdvances+1;q.target=item.Type;return true end
              BuildUnit=function(c,item)nativeBuilds=nativeBuilds+1;q.target=item.Type;return true end
              CheckQueueItemSelected=function()return false end
              GetBuildInsertMode=function()return true end
              UI={GetHeadSelectedCity=function()return c end,RequestPlayerOperation=sendUI}
            """)
            l.execute((ROOT/'Mod/UI/CrewProjectOrder.lua').read_text())
            l.execute("assert(AdvanceProject(c,{Type=project}));assert(BuildUnit(c,{Type='UNIT_DRONE'}));assert(not AdvanceProject(c,{Type=project}));assert(baseAdvances==1 and nativeBuilds==1 and q.target=='UNIT_DRONE')")

    def test_queue_delivery_and_handler_failure_are_not_committed_acceptance(self):
        l=project_fixture('Dialogue',connect=True);install(l,'on')
        l.execute("assert(selectUI());q.target=project;queueEventUI(3,999);ownEventUI();pumpUI();local wrong,right=false,false;for _,r in ipairs(diagRows)do if r.point=='UI_QUEUE_EVENT'then if r.ready then right=true else wrong=true end end end;assert(wrong and right)")
        l=project_fixture('Dialogue',connect=True);install(l,'on')
        l.execute("assert(selectUI());q.target=project;local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(...)local f=read(...);f.active=1;return f end;ownEventUI();pumpUI();local failed,commit=false,false;for _,r in ipairs(diagRows)do if r.point=='DIALOGUE_SAFE_FAILED'then failed=true end;if r.point=='DIALOGUE_BEGIN_COMMITTED'then commit=true end end;assert(failed and not commit)")


class Observer(unittest.TestCase):
    def test_disabled_missing_and_throwing_builders_never_reach_native(self):
        l=LuaRuntime();l.execute("Game=setmetatable({},{__index=function()error('NO_NATIVE_READ')end});ExposedMembers={}")
        install(l,'off');l.execute("SPCCultureDiagnostics.Emit('CULTURE_GP','TEST',function()error('BUILDER_MUST_NOT_RUN')end);assert(#diagRows==0 and diagStarts==0)")
        install(l,'on');l.execute("SPCCultureDiagnostics.Emit('CULTURE_GP','TEST',function()error('BUILDER_FAILED')end);assert(diagStarts==0)")

    def test_change_only_bounds_reentry_and_scalars(self):
        l=LuaRuntime();install(l,'on')
        l.execute('''
          for i=1,1000 do SPCCultureDiagnostics.Emit('CULTURE_GP','SAME',function()return {owner=0,city=1,workers=2}end)end
          assert(#diagRows==1 and diagStarts==1)
          for i=1,500 do SPCCultureDiagnostics.Emit('CULTURE_GP','CHANGE',function()return {owner=0,city=i,workers=i,native={}}end)end
          assert(#diagRows==193 and diagRows[#diagRows].eventTruncated==true)
          for _,r in ipairs(diagRows)do for _,v in pairs(r)do assert(type(v)~='table'and type(v)~='function'and type(v)~='userdata')end end
        ''')
        install(l,'on');l.execute("SPCCultureDiagnostics.Emit('CULTURE_GP','AFTER_LOAD',function()return {workers=1}end);assert(#diagRows==1)")

    def test_actual_b205_reader_and_collector_accept_rows(self):
        from test_expedition_training_diagnostics import fixture
        import collect_expedition_trace as collector
        l=fixture();l.execute('SPCCultureDiagnostics=nil');l.execute(OBS)
        l.execute("SPCCultureDiagnostics.Emit('CULTURE_GP','UI_QUEUE_READ',function()return {owner=0,city=1,queueSize=1,requestAccepted=false}end)")
        lines=list(l.globals().printed.values())
        row=next(str(s)for s in lines if 'CULTURE_DIAGNOSTIC'in str(s))
        self.assertEqual(collector.fields(row)['point'],'UI_QUEUE_READ')
        self.assertEqual(collector.train_line(row),row)
        self.assertEqual(collector.fields(row)['requestAccepted'],'false')
        with tempfile.TemporaryDirectory(dir=ROOT/'local')as directory:
            session=collector.Session(root=Path(directory),stamp='B394')
            try:
                session.add(row,'test')
                session.add('[SPC][B205][TRAIN] seq=99 stage=CULTURE_DIAGNOSTIC point=LIMIT_REACHED traceRole=CULTURE_GP eventTruncated=true eventCount=192','test')
                summary=session.summary('TEST')
                self.assertIn('culture_diagnostic_points:',summary)
                self.assertIn('CULTURE_DIAGNOSTIC_TRUNCATED',summary)
                self.assertIn(row,(session.directory/'records.log').read_text())
            finally:session.close()

    def test_repeated_event_arrivals_and_turn_boundaries_are_not_hidden(self):
        l=LuaRuntime();install(l,'on')
        l.execute("for i=1,2 do SPCCultureDiagnostics.Emit('CULTURE_GP','EXPEDITION_TURN_STATE',function()return {owner=0,phase='RECOVERING'}end);SPCCultureDiagnostics.Emit('CULTURE_GP','WORKER_CAUSE',function()return {owner=0,reason='UI_WORKERS_DIRTY'}end)end;assert(#diagRows==4 and diagRows[4].eventCount==4)")


if __name__=='__main__':unittest.main()
