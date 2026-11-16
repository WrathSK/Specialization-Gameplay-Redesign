"""Fixed production phases preserve actual before ordering, isolation and native behavior."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,Context,SOURCES,executed,completion,measure
from refactor_defect_fixtures import panel

BASE='cffee6a'
@contextmanager
def before():
 paths={ROOT/'Mod'/p:subprocess.check_output(['git','show',BASE+':Mod/'+p],cwd=ROOT,text=True)for p in ('UI/SafeAdapters.lua','UI/CrewProjectOrder.lua')}
 read,load=Path.read_text,Context.load
 def source(p,*a,**kw):return paths[p]if p in paths else read(p,*a,**kw)
 def module(c,name):
  p=ROOT/'Mod'/(name if name.endswith('.lua')else name+'.lua')
  if p not in paths:return load(c,name)
  text=paths[p];h=sha256(text.encode()).hexdigest();key='historical/'+BASE+'/'+str(p.relative_to(ROOT));executed(key,h)
  try:out=c.lua.execute(text)
  except Exception:completion(key,False);raise
  completion(key,True);return out
 with patch.object(Path,'read_text',source),patch.object(Context,'load',module):yield


TRACE="""
trace={};function note(s)trace[#trace+1]=s end
local names={'TimedProjectSelection','ClaimProjectUI','DialogueProjectUI','EngineeringStudyUI','CapitalInvestmentUI','DevelopmentInvestmentUI','CommerceUI','CrewProjectUI','ExpeditionTrainingUI'}
for _,name in ipairs(names)do local n=name
 _G['SPC'..n].New=function(...)
  note('NEW:'..n);if newFailure==n then error('CONSTRUCTOR')end
  local api={}
  for _,method in ipairs({'Items','Before','Sync','Publish','Pulse','WarmStart','QueueEvent','Connect','Invalidate','RefreshFacts','CancelQueue','Close'})do local m=method
   api[m]=function(...)
    note(n..':'..m)
    if onCall then onCall(n,m,...)end
    if fail==n..':'..m then error('CALLBACK')end
    return true
   end
  end
  return api
 end
end
SPCTimedProjectDisplay.Items=function()note('TimedDisplay:Items')end
SPCRestructuringUI.ObserveTraining=function()note('Restructuring:ObserveTraining');if observeFail then error('OBSERVATION')end end
GetDataHelper=function()note('NATIVE:Data');return {City={native='CITY'},ProjectItems={{Type='PROJECT_NATIVE',Name='native'}},UnitItems={{Type='UNIT_NATIVE'}}}end
AdvanceProject=function(c,item)note('NATIVE:Advance:'..tostring(item.Type));return 'NATIVE_RESULT',item end
CheckQueueItemSelected=function()note('QUEUED');return queued or false end
OnShutdown=function()note('NATIVE:Shutdown')end
"""


def traced(extra=''):return panel(TRACE+extra)


class Differential(unittest.TestCase):
 def compare(self,body,extra=''):
  observations=[]
  for old in (True,False):
   with before()if old else nullcontext():c=traced(extra)
   c.execute(body+";observed=table.concat(trace,'|')")
   observations.append(c.eval('observed'))
  self.assertEqual(observations[0],observations[1]);return observations[1]
 def test_all_actual_phase_orders_constructors_hooks_and_close_match_before(self):
  seen=self.compare("""
  note('RENDER');local data=GetDataHelper();assert(data.ProjectItems[1].Name=='native')
  note('SELECT');local a,b=AdvanceProject({}, {Type='PROJECT_NATIVE'});assert(a=='NATIVE_RESULT'and b.Type=='PROJECT_NATIVE')
  note('PUBLISH');Events.GameCoreEventPublishComplete.Fire()
  note('LOAD');Events.LoadScreenClose.Fire();note('TURN');Events.LocalPlayerTurnBegin.Fire()
  for _,name in ipairs({'CityProductionChanged','CityProductionQueueChanged','CityProductionUpdated'})do note(name);Events[name].Fire(0,1)end
  note('CLOSE');shutdown();Events.GameCoreEventPublishComplete.Fire()
  """)
  self.assertIn('ExpeditionTrainingUI:Items|Restructuring:ObserveTraining|CrewProjectUI:Items|CapitalInvestmentUI:Items',seen)
  self.assertIn('DialogueProjectUI:WarmStart|ClaimProjectUI:WarmStart|EngineeringStudyUI:WarmStart',seen)
  measure('S9a1_actual_UI_phase_differential',{'baseline':BASE,'same_construct_render_before_event_connect_shutdown_order':True,'listener_merging':False,'native_parameters_returns':True})
 def test_every_before_failure_keeps_native_open_owned_closed_and_short_circuit_order(self):
  for name,project in (('CapitalInvestmentUI','PROJECT_SPC_CAPITAL_INVESTMENT'),('DevelopmentInvestmentUI','PROJECT_SPC_DEVELOPMENT_INVESTMENT'),('CommerceUI','PROJECT_SPC_COMMERCIALIZATION'),('CrewProjectUI','PROJECT_SPC_CREW_250'),('EngineeringStudyUI','PROJECT_SPC_ENGINEERING_STUDY'),('DialogueProjectUI','PROJECT_SPC_ERA_DIALOGUE'),('ClaimProjectUI','PROJECT_SPC_CLAIM_RESEARCH'),('TimedProjectSelection','PROJECT_SPC_OVERFLOW_SINK_TEST')):
   self.compare("trace={};fail='"+name+":Before';AdvanceProject({}, {Type='PROJECT_NATIVE'});AdvanceProject({}, {Type='"+project+"'})")
 def test_constructor_failures_and_render_observer_failure_remain_independently_contained(self):
  for name in ('CapitalInvestmentUI','ClaimProjectUI','CrewProjectUI','ExpeditionTrainingUI'):
   self.compare("GetDataHelper();AdvanceProject({}, {Type='PROJECT_NATIVE'});Events.GameCoreEventPublishComplete.Fire();shutdown()", "newFailure='"+name+"';observeFail=true")
 def test_before_reads_live_native_queue_function_after_earlier_adapter_changes_it(self):
  self.compare("trace={};onCall=function(n,m)if n=='CapitalInvestmentUI'and m=='Before'then CheckQueueItemSelected=function()note('NEW_QUEUED');return false end end end;AdvanceProject({}, {Type='PROJECT_NATIVE'})")
 def test_queued_sink_guard_and_native_query_failure_have_same_scope(self):
  self.compare("trace={};queued=true;assert(AdvanceProject({}, {Type='PROJECT_SPC_OVERFLOW_SINK_TEST'})==nil)")
  self.compare("trace={};CheckQueueItemSelected=function()note('QUEUE_THROW');error('NATIVE_READ')end;assert(not pcall(AdvanceProject,{}, {Type='PROJECT_NATIVE'}))")


class Registry(unittest.TestCase):
 def make(self):
  c=Context('UI');c.load('UI/SafeAdapters');c.execute("d=SPCSafeAdapters.New();seen={};function note(x)seen[#seen+1]=x end;function create(n)return function()note('new:'..n);return {Items=function()note('items:'..n)end,Sync=function(c)assert(c=='CITY');note('sync:'..n)end,Before=function(c,item,q)note('before:'..n..':'..tostring(q));return true end}end end");return c
 def test_ranks_are_independent_of_construction_and_caller_metadata_is_detached(self):
  c=self.make();c.execute("plan={Render={80,'Sync'},Before={10,'Before',true}};local a=d.Add('A',function()return false end,{},create('a'),plan);plan.Render[1]=1;d.Add('B',function()return false end,{},create('b'),{Render={10,'Items'},Before={20,'Before'}});d.Barrier('Render',20,function()note('barrier')end);d.Render({City='CITY',ProjectItems={},UnitItems={}});assert(d.BeforeAll({}, {},function()return false end));assert(table.concat(seen,',')=='new:a,new:b,items:b,barrier,sync:a,before:a:false,before:b:nil')")
 def test_invalid_phases_ranks_methods_and_collisions_reject_before_constructor(self):
  for spec in ("{Unknown={1,'Items'}}","{Render={0,'Items'}}","{Render={101,'Items'}}","{Render={1,'Before'}}","{Pulse={1,'Items'}}","{Render={1,'Items',true}}"):
   c=self.make();c.execute("assert(not pcall(d.Add,'Bad',function()return false end,{},create('bad'),"+spec+"));assert(#seen==0)")
  c=self.make();c.execute("d.Add('A',function()return false end,{},create('a'),{Render={10,'Items'}});assert(not pcall(d.Add,'B',function()return false end,{},create('b'),{Render={10,'Items'}}));assert(#seen==1)")
 def test_reentrant_constructor_does_not_publish_its_own_incomplete_phase(self):
  c=self.make();c.execute("d.Add('A',function()return false end,{},create('a'),{Render={10,'Items'}});d.Add('B',function()return false end,{},function()d.Render({City='CITY',ProjectItems={},UnitItems={}});return create('b')()end,{Render={20,'Items'}});assert(table.concat(seen,',')=='new:a,items:a,new:b')")


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S8b8'])])

if __name__=='__main__':unittest.main()
