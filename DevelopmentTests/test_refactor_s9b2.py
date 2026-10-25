"""Dialogue UI supplies raw slots; the real Gameplay catalogue interprets eras.
Frozen scalar-x protocol assertions remain labelled historical, not production.
"""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,Context,SOURCES,executed,completion,legacy_source_observation,measure
from test_refactor_s7d1 import profile
import test_dialogue_projects as projects
import test_dialogue_project_ui as ui_fixture

BASE='574764d'
@contextmanager
def before():
 originals={ROOT/'Mod'/p:subprocess.check_output(['git','show',BASE+':Mod/'+p],cwd=ROOT,text=True)for p in ('DialogueProjects.lua','GreatWorkFacts.lua','UI/DialogueProjectUI.lua')}
 read,execute,load=Path.read_text,TrackedLua51.execute,Context.load
 hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in originals.items()}
 def source(p,*a,**kw):return originals[p]if p in originals else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 def module(c,name):
  p=ROOT/'Mod'/(name if name.endswith('.lua')else name+'.lua')
  if p not in originals:return load(c,name)
  text=originals[p];h=sha256(text.encode()).hexdigest();key=hashes[h];executed(key,h)
  try:out=c.lua.execute(text)
  except Exception:completion(key,False);raise
  completion(key,True);return out
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),patch.object(Context,'load',module),legacy_source_observation():yield

def runtime(ui=False):
 with profile():v=projects.game()
 if ui:
  with legacy_source_observation():ui_fixture.ui(v)
  v.globals().include('TimedProjectReaders')
  v.execute("service=SPCTimedProjectReaders.New(P,shared);service.Attach('DialogueProjects',shared.DialogueProjects);service.Seal();ui.Connect();ui.Pulse();packets={}")
 return v

class Catalogue(unittest.TestCase):
 def test_zero_to_eight_and_unsupported_types_use_existing_catalogue_without_native_reads(self):
  v=runtime();v.execute("local f=shared.GreatWorkFacts;assert(f.state=='UNKNOWN');P.Info=function()error('NO_NATIVE_OR_METADATA_READ')end;Players={};for n=0,8 do assert(f.InterpretCompletion(rawCompletion(n))==n)end;local raw=rawCompletion(2);raw[3]={id=99,type='UNSUPPORTED_NATIVE_WORK',building=998,slot=99};assert(f.InterpretCompletion(raw)==2);raw[3].type=raw[1].type;assert(f.InterpretCompletion(raw)==2)")
 def test_missing_holes_metatables_duplicate_locations_and_bad_scalar_rows_are_unknown(self):
  cases=('nil',"'EMPTY'",'{[2]=rawCompletion(1)[1]}','{other=rawCompletion(1)[1]}','{[4097]=rawCompletion(1)[1]}',"setmetatable({},{__index=function()error('UNREADABLE')end})")
  for raw in cases:
   v=runtime();v.execute('assert(not pcall(shared.GreatWorkFacts.InterpretCompletion,'+raw+'))')
  mutations=("r[1].id=0/0","r[1].id=math.huge","r[1].building=-1","r[1].slot=256","r[1].type=''","r[1].type=false","r[2].id=r[1].id","r[2].slot=r[1].slot","r[1]=setmetatable(r[1],{})")
  for change in mutations:
   v=runtime();v.execute('local r=rawCompletion(2);'+change+';assert(not pcall(shared.GreatWorkFacts.InterpretCompletion,r))')
 def test_explicit_capacity_boundary_and_shutdown_rejects_old_service(self):
  v=runtime();v.execute("local f=shared.GreatWorkFacts;local r={};for i=1,4096 do r[i]={id=i,type=fixtureKinds[1],building=math.floor((i-1)/256),slot=(i-1)%256}end;assert(f.InterpretCompletion(r)==1);r[4097]={id=4097,type=fixtureKinds[1],building=16,slot=0};assert(not pcall(f.InterpretCompletion,r));f.Reset();assert(f.InterpretCompletion({})==0);f.Shutdown();assert(not pcall(f.InterpretCompletion,{}))")

class CurrentUI(unittest.TestCase):
 def test_actual_reader_returns_only_fresh_raw_slots_and_never_builds_or_plans_in_UI(self):
  v=runtime(True);v.execute("SPCGreatWorkCatalog.Build=function()error('UI_MUST_NOT_BUILD_CATALOGUE')end;local plan=SPCGreatWorkFacts.Plan;SPCGreatWorkFacts.Plan=function(...)assert(not inUIReader,'UI_MUST_NOT_INTERPRET');return plan(...)end;local f=shared.GreatWorkFacts;for n=1,3 do slots={};for i=1,n do slots[i]=i end;inUIReader=true;local x=ExposedMembers.SPC_DialogueProjectRead(0,c:GetID(),true);inUIReader=false;assert(x.protocol==2 and x.x==nil and #x.raw==n and f.InterpretCompletion(x.raw)==n)end;slots={};local x=ExposedMembers.SPC_DialogueProjectRead(0,c:GetID(),true);assert(f.InterpretCompletion(x.raw)==0 and x.x==nil);slots={1};c.b.GetGreatWorkInSlot=function()error('UNREADABLE')end;assert(not pcall(ExposedMembers.SPC_DialogueProjectRead,0,c:GetID(),true))")
 def test_real_raw_UI_and_Gameplay_complete_once_and_describe_current_collection(self):
  v=runtime(True);v.execute("slots={1,2};assert(dp.Describe(0,c):find('当前合格馆藏时代：2',1,true));begin(c);duplicate=true;endturn();assert(ledger(c).total==10 and ledger(c).used.ERA_CLASSICAL.x==2 and finishes==1);slots={1,2,3};assert(dp.Describe(0,c):find('当前合格馆藏时代：3',1,true));slots={};assert(dp.Describe(0,c):find('当前合格馆藏时代：0',1,true));assert(ledger(c).total==10)")
 def test_queue_only_and_thousand_idle_publishes_do_not_collect_work_slots(self):
  v=runtime(True);v.execute("slotReads=0;local old=c.b.GetNumGreatWorkSlots;c.b.GetNumGreatWorkSlots=function(...)slotReads=slotReads+1;return old(...)end;local w=T.writes();for i=1,1000 do ui.Pulse();Events.GameCoreEventPublishComplete.Fire()end;ExposedMembers.SPC_DialogueProjectRead(0,c:GetID(),false);assert(slotReads==0 and T.writes()==w)")
  measure('S9b2_completion_work',{'catalogue':'existing Gameplay Start instance','extra_city_scans':0,'new_events':0,'idle_publishes':1000,'idle_work_slot_reads':0,'queue_only_slot_reads':0,'background_ACK_used_for_completion':False})

class Completion(unittest.TestCase):
 def test_actual_before_after_zero_to_eight_receipts_and_sample_counts_are_equal(self):
  for n in range(9):
   out=[]
   for old in (True,False):
    with before()if old else nullcontext():v=runtime()
    v.execute('sampleX=...;duplicate=true;begin(c);endturn();result=T.encode(ledger(c));assert(samples==1 and finishes==1)',n)
    out.append(v.eval('result'))
   self.assertEqual(*out,n)
  measure('S9b2_completion_differential',{'before':BASE,'cases':9,'era_count':[0,8],'same_full_ledger_and_quota':True,'same_samples_and_finish_calls':True,'no_native_performance_claim':True})
 def test_untrusted_scalar_x_is_ignored_and_eight_real_eras_give_forty(self):
  v=runtime();v.execute("sampleX=8;local old=sample;ExposedMembers.SPC_DialogueProjectRead=function(...)local r=old(...);r.x=999;return r end;begin(c);endturn();assert(ledger(c).total==40 and ledger(c).used.ERA_CLASSICAL.x==8 and samples==1)")
 def test_bad_or_missing_raw_protocol_holds_once_without_late_resample(self):
  for mutation in ('r.raw=nil','r.protocol=nil',"r.protocol=1",'r.raw={[2]=r.raw[1]}',"r.raw[1].type=false"):
   v=runtime();v.execute("local old=sample;ExposedMembers.SPC_DialogueProjectRead=function(...)local r=old(...);"+mutation+";return r end;begin(c);endturn();assert(ledger(c).total==0 and ledger(c).pending.stage=='HELD'and samples==1);ExposedMembers.SPC_DialogueProjectRead=sample;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;Events.CityProjectCompleted.Fire(0,c:GetID(),999);assert(samples==1 and ledger(c).total==0)")
 def test_reader_or_owner_service_replacement_during_sampling_cannot_commit(self):
  for mutation in ('ExposedMembers.SPC_DialogueProjectRead=function()error("NEW_READER")end','shared.GreatWorkFacts={InterpretCompletion=function()return 8 end}'):
   v=runtime();v.execute('local old=sample;ExposedMembers.SPC_DialogueProjectRead=function(...)local r=old(...);'+mutation+';return r end;begin(c);endturn();assert(samples==1 and ledger(c).total==0 and not ledger(c).used.ERA_CLASSICAL)')
 def test_changes_during_interpretation_recheck_turn_owner_reference_and_saved_state(self):
  for mutation in ('T.turn(1)','c.s.ref.owner=3','c.s.ref.cityID=999','local n=T.record(c);n.dialogue.total=5;n.dialogue.used.ERA_OTHER={id="bad"};T.propsSet(T.key(c),n)'):
   v=runtime();v.execute('local f=shared.GreatWorkFacts;local old=f.InterpretCompletion;f.InterpretCompletion=function(raw)local x=old(raw);'+mutation+';return x end;begin(c);endturn();assert(samples==1 and not ledger(c).used.ERA_CLASSICAL)')

def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9b1'])])

if __name__=='__main__':unittest.main()
