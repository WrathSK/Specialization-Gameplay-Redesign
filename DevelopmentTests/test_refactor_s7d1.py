"""S7d1 actual-owner queue facts. Explicit Lua51 events, no native-game claim."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
import lupa.lua55 as lua55
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
import test_store_write_boundaries as city
import test_dialogue_projects as dialogue
import test_b235_engineering as engineering
import test_refactor_s5history as histories

BASE='324df73'
@contextmanager
def profile():
    with patch.object(city,'LuaRuntime',TrackedLua51),patch.object(lua55,'LuaRuntime',TrackedLua51),patch.object(engineering,'runtime',composed_industry),legacy_source_observation():yield
@contextmanager
def history():
    previous=Path.read_text;execute=TrackedLua51.execute
    originals={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('ClaimProjects','DialogueProjects','EngineeringStudyProjects')}
    digests={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in originals.items()}
    def read(p,*a,**kw):return originals[p]if p in originals else previous(p,*a,**kw)
    def run(vm,s,*a,**kw):
        h=sha256(s.encode()).hexdigest()if isinstance(s,str)else None
        if h in digests:SOURCES[h]=digests[h]
        return execute(vm,s,*a,**kw)
    with patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

def composed_industry():
    # The frozen Study assertions predate typed history propagation. Compose its
    # real replacement; observe committed ENGINEERING, never fake a successful emit.
    l=histories.industry();l.globals().include('FactConsumerBindings');l.execute("""
    local installed
    local function installPropagation()
     local changes=shared.FactChanges;if installed==changes then return end
     SPCFactConsumerBindings.New(shared)
     changes.RegisterConsumer('ObservedEngineering',function(e)S.notifications=(S.notifications or 0)+1 end,{kinds={'HISTORY'},topics={'ENGINEERING'}})
     table.insert(Events.GameCoreEventPublishComplete.list,1,function()shared.FactChanges.Flush();shared.FactBindings.Flush()end)
     installed=changes
    end
    installPropagation();local reload=H.reload
    H.reload=function(...)local result=reload(...);installPropagation();return result end
    """);return l

def claim_runtime():
    path=ROOT/'DevelopmentTests/test_b140_templates.py';source=path.read_text();ns={'__file__':str(path)}
    exec(compile(source[:source.index("extra=r"+chr(39)*3)],str(path),'exec'),ns)
    header=ns['header'].replace('l=LuaRuntime()', 'l=LuaRuntime()\nl.globals().print=lambda *parts:None')
    body="""
    start();c=conquered(1,'DISTRICT_CAMPUS');request(c,'RESEARCH')
    function pending()return record(c).claimTimer end
    function snapshot()return encode(record(c))end
    function pulse()flush()end
    ExposedMembers=ExposedMembers or {};q=c.q;project='PROJECT_SPC_CLAIM_RESEARCH'
    function nextTurn()turn=turn+1;Events.PlayerTurnActivated.Fire(0)end
    function finished()return record(c).claim~=nil end
    function changed(id)Events.CityProductionChanged.Fire(0,id or c:GetID());flush()end
    """
    exec(compile(header+ns['helpers']+ns['claim_setup']+body+"\n"+chr(39)*3+")",str(path),'exec'),ns)
    return ns['l']

def actual(kind):
    with profile():
        if kind=='Claim':return claim_runtime()
        if kind=='Dialogue':
            l=dialogue.game();l.execute("begin(c);q=c.q;project='PROJECT_SPC_ERA_DIALOGUE';function pending()return ledger(c).pending end;function snapshot()return T.encode(T.record(c))end;function pulse()dp.Flush()end;function finished()return ledger(c).used.ERA_CLASSICAL~=nil end;function changed(id)Events.CityProductionChanged.Fire(0,id or c:GetID());pulse()end")
        else:
            l=engineering.study_runtime();l.execute("c=S.make();S.begin(c);q=c:GetBuildQueue();project='PROJECT_SPC_ENGINEERING_STUDY';function pending()return S.state(c).value.pending end;function snapshot()return T.encode(T.record(c))end;function pulse()study.Flush()end;function finished()return S.L(c)>0 end;function changed(id)Events.CityProductionChanged.Fire(0,id or c:GetID());pulse()end")
    return l

def pure():
    c=Context();c.load('TimedProjects');c.execute("""
    calls={};q={target='P',size=1};city={GetBuildQueue=function()calls[#calls+1]='QUEUE';return q end}
    function q:CurrentlyBuilding()calls[#calls+1]='TARGET';if targetThrow then error('TARGET')end;return self.target end
    function q:GetSize()calls[#calls+1]='SIZE';if sizeThrow then error('SIZE')end;return self.size end
    P={Call=function(o,k,...)if type(o and o[k])~='function'then return false end;return pcall(o[k],o,...)end}
    function fallback(target)calls[#calls+1]='FALLBACK';if fallbackThrow then error('FALLBACK')end;return fallbackSize end
    function read()return SPCTimedProjects.Queue(P,city,'P',fallback,{read='READ_UNKNOWN',unique='UNIQUE',appendSize=true})end
    """);return c

class Classification(unittest.TestCase):
    def test_fact_matrix_keeps_empty_unknown_current_and_multiple_distinct(self):
        c=pure();c.execute("""
        local f=SPCTimedProjectModel.ClassifyQueue
        assert(f('P',1,'P')=='CURRENT'and f('P',2,'P')=='MULTIPLE')
        assert(f(nil,0,'P')=='EMPTY'and f('',0,'P')=='EMPTY')
        for _,n in ipairs({-1,0,.5,'1',false,{},0/0,math.huge})do assert(f('P',n,'P')=='UNKNOWN')end
        assert(f('P',nil,'P')=='UNKNOWN'and f(nil,nil,'P')=='UNKNOWN'and f(nil,1,'P')=='UNKNOWN'and f('',1,'P')=='UNKNOWN')
        for _,v in ipairs({false,0,{},true})do assert(f(v,0,'P')=='UNKNOWN')end
        assert(f('OTHER',nil,'P')=='OTHER')
        """)
    def test_other_keeps_original_early_return_without_size_or_fallback(self):
        c=pure();c.execute("q.target='OTHER';sizeThrow=true;fallbackThrow=true;local a,b,s=read();assert(a==q and b==false and s=='OTHER'and table.concat(calls,',')=='QUEUE,TARGET')")
    def test_current_empty_and_fallback_have_exact_read_order(self):
        for target,size,state,match in (("'P'",1,'CURRENT','true'),('nil',0,'EMPTY','false'),("''",0,'EMPTY','false')):
            for fallback in (False,True):
                c=pure();c.execute("q.target="+target+";q.size="+str(size)+(";sizeThrow=true;fallbackSize="+str(size)if fallback else '')+";local _,m,s=read();assert(m=="+match+" and s=='"+state+"'and table.concat(calls,',')=='QUEUE,TARGET,SIZE"+(',FALLBACK'if fallback else '')+"')")
    def test_unproven_or_broken_reads_cannot_yield_match_or_empty(self):
        for setup in ("targetThrow=true","q.target=false","q.target=0","q.target=nil;q.size=1","q.target='';q.size=nil","sizeThrow=true;fallbackSize=nil","sizeThrow=true;fallbackThrow=true","q.size=2"):
            c=pure();c.execute(setup+";assert(not pcall(read))")

class RealOwners(unittest.TestCase):
    def test_ambiguous_nil_positive_preserves_pending_recovers_same_city_and_then_completes(self):
        for kind in ('Claim','Dialogue','Engineering'):
            with self.subTest(owner=kind):
                l=actual(kind);l.execute("""
                local before=snapshot();local get=q.GetSize;q.target=nil;q.GetSize=function()return 1 end
                changed();assert(snapshot()==before and pending().stage=='ACTIVE'and not finished())
                for i=1,1000 do pulse()end;assert(snapshot()==before)
                q.target=project;q.GetSize=get;changed();assert(snapshot()==before and pending().stage=='ACTIVE')
                Events.PlayerTurnDeactivated.Fire(0)
                """+ ("nextTurn()"if kind=='Claim'else"T.turn(1)")+";pulse();assert(finished())")
        measure('S7d1_actual_unknown_recovery',{'owners':3,'ambiguous_nil_cancel_or_complete':0,'idle_publishes':1000,'recovery':'same-city CityProductionChanged','then_full_turn':'original independent receipts'})
    def test_confirmed_empty_or_other_cancels_but_unknown_does_not(self):
        for kind in ('Claim','Dialogue','Engineering'):
            for target,size in (('nil',0),("''",0),("'NORMAL'",1)):
                with self.subTest(owner=kind,target=target):
                    l=actual(kind);l.execute("q.target="+target+";q.GetSize=function()return "+str(size)+" end;changed();assert(not finished()and (not pending()or pending().stage=='STOPPED'))")
    def test_unrelated_events_and_idle_do_not_read_the_pending_city_queue(self):
        for kind in ('Claim','Dialogue','Engineering'):
            l=actual(kind);l.execute("local get=q.GetSize;queueReads=0;q.GetSize=function(...)queueReads=queueReads+1;return get(...)end;changed(999);Events.CityProductionChanged.Fire(3,c:GetID());pulse();for i=1,1000 do pulse()end;assert(queueReads==0 and pending().stage=='ACTIVE')")
    def test_missing_size_and_unverified_UI_fallback_hold_ledger(self):
        for kind in ('Claim','Dialogue','Engineering'):
            l=actual(kind);l.execute("local before=snapshot();q.target=nil;q.GetSize=nil;ExposedMembers.SPC_ClaimQueueRead=nil;ExposedMembers.SPC_DialogueProjectRead=nil;ExposedMembers.SPC_EngineeringStudyRead=nil;changed();assert(snapshot()==before and pending().stage=='ACTIVE'and not finished())")
    def test_UI_fallback_rejects_stale_or_wrong_reference_or_conflicting_target(self):
        for kind in ('Claim','Dialogue','Engineering'):
            reader={'Claim':'SPC_ClaimQueueRead','Dialogue':'SPC_DialogueProjectRead','Engineering':'SPC_EngineeringStudyRead'}[kind]
            for error in ('owner','city','turn','target','count'):
                l=actual(kind);l.globals().bad=error;l.execute("""
                local before=snapshot();q.target=nil;q.GetSize=nil
                local r={owner=0,id=c:GetID(),turn=Game.GetCurrentGameTurn(),project=nil,size=0,reference={owner=0,cityID=c:GetID(),x=c:GetX(),y=c:GetY()}}
                if bad=='owner'then r.owner=3;r.reference.owner=3 elseif bad=='city'then r.id=99;r.reference.cityID=99 elseif bad=='turn'then r.turn=r.turn-1 elseif bad=='target'then r.project=project elseif bad=='count'then r.size=1 end
                ExposedMembers[...]=function()return r end;changed();assert(snapshot()==before and pending().stage=='ACTIVE'and not finished())
                """,reader)
    def test_UI_fallback_can_confirm_empty_with_current_exact_reference(self):
        for kind in ('Claim','Dialogue','Engineering'):
            reader={'Claim':'SPC_ClaimQueueRead','Dialogue':'SPC_DialogueProjectRead','Engineering':'SPC_EngineeringStudyRead'}[kind]
            l=actual(kind);l.execute("q.target=nil;q.GetSize=nil;ExposedMembers[...]=function()return {owner=0,id=c:GetID(),turn=Game.GetCurrentGameTurn(),size=0,reference={owner=0,cityID=c:GetID(),x=c:GetX(),y=c:GetY()}}end;changed();assert(not finished()and (not pending()or pending().stage=='STOPPED'))",reader)
    def test_normal_full_turn_and_confirmed_other_outcomes_match_baseline(self):
        for kind in ('Claim','Dialogue','Engineering'):
            for cancel in (False,True):
                values=[]
                for old in (True,False):
                    with history()if old else nullcontext():
                        l=actual(kind)
                        if cancel:l.execute("q.target='NORMAL';changed()")
                        l.execute("Events.PlayerTurnDeactivated.Fire(0);"+("nextTurn()"if kind=='Claim'else"T.turn(1)")+";pulse();result=snapshot()")
                        values.append(l.eval('result'))
                self.assertEqual(*values,(kind,cancel))
        measure('S7d1_normal_differential',{'baseline':BASE,'actual_owners':3,'full_turn_and_other_target':'identical complete Store record','native_or_save_format_change':False})

class Retained(unittest.TestCase):pass
for label,case in (('dialogue',dialogue.DialogueProjects),('engineering',engineering.Study)):
    for name in dir(case):
        if name.startswith('test_'):
            def run(self,case=case,name=name):
                with profile():getattr(case(),name)()
            setattr(Retained,'test_'+label+'_'+name.removeprefix('test_'),run)
for name in ('test_existing_b127_saved_claim_timer_regression','test_claim_timer_same_turn_progress_and_coldload'):
    def run(self,name=name):
        with profile():getattr(city.StoreWriteBoundaries(),name)()
    setattr(Retained,'test_claim_'+name.removeprefix('test_'),run)

del case,label
if __name__=='__main__':unittest.main()
