"""R11 real UI -> request -> D/FC/Bindings -> actual writer work, local only."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import subprocess,unittest
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,executed,completion,legacy_source_observation,measure
from refactor_defect_fixtures import fact_publication_profile,request_context
from test_refactor_s5d1 import research
from test_refactor_s5d4b2 import ui,load_request


@contextmanager
def baseline():
 rows={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','6b6bf00:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('Gameplay','UI/GPPRefresh')}
 read,execute,load,fragment=Path.read_text,TrackedLua51.execute,Context.load,Context.fragment
 hashes={sha256(s.encode()).hexdigest():'historical/6b6bf00/'+str(p.relative_to(ROOT))for p,s in rows.items()}
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 def oldload(vm,name):
  p=ROOT/'Mod'/(name if name.endswith('.lua')else name+'.lua')
  if p not in rows:return load(vm,name)
  text=rows[p];h=sha256(text.encode()).hexdigest();key=hashes[h];executed(key,h)
  try:out=vm.execute(text)
  except Exception:completion(key,False);raise
  completion(key,True);return out
 def oldfragment(vm,path,start,end):
  p=ROOT/path
  if p not in rows:return fragment(vm,path,start,end)
  text=rows[p];assert text.count(start)==1 and text.count(end)==1;value=text[text.index(start):text.index(end)]
  executed('historical/6b6bf00/'+path+':'+start,sha256(text.encode()).hexdigest(),'source_fragment',fragment_sha256=sha256(value.encode()).hexdigest(),start=start,end=end)
  return value
 with patch.object(Path,'read_text',lambda p,*a,**kw:rows[p]if p in rows else read(p,*a,**kw)),patch.object(TrackedLua51,'execute',run),patch.object(Context,'load',oldload),patch.object(Context,'fragment',oldfragment):yield


def composed():
 g=research()
 with legacy_source_observation():fact_publication_profile(g,False)
 g.execute("P.Scalar=tostring");load_request(g);u=ui()
 def deliver(p):g.globals().rawRequest(0,g.table_from(dict(p)))
 deliver(u.globals().packets[1]);g.execute('drainworker()')
 u.globals().onSend=deliver
 u.execute('Events.PlayerTurnActivated.Fire(0)');g.execute('drainworker()')
 return g,u


class Work(unittest.TestCase):
 def test_actual_normal_GP_turn_then_UI_turn_does_not_capture_D_again(self):
  values=[]
  for old in (True,False):
   with baseline()if old else nullcontext():
    g,u=composed()
    g.execute("turn=2;fire('PlayerTurnActivated',0);drainworker();counters={};reads=0;writes=0")
    u.execute('turn=2;Events.PlayerTurnActivated.Fire(0)');g.execute('drainworker();assert(cc(\'BUILDING_LIBRARY\')==3 and cc(\'BUILDING_LIBRARY\',cities[2])==3)')
    values.append(dict(D_captures=g.eval('counters.dc_capture or 0'),city_visits=g.eval('counters.city_scan or 0'),building_checks=g.eval('counters.building_check or 0'),native_double_reads=g.eval('reads'),writes=g.eval('writes')))
  self.assertEqual(values[0]['D_captures'],2);self.assertEqual(values[1]['D_captures'],0)
  self.assertGreater(values[0]['building_checks'],values[1]['building_checks'])
  self.assertGreater(values[1]['city_visits'],0) # needed worker recovery remains
  self.assertEqual(values[0]['writes'],values[1]['writes'])
  measure('S9e5_GP_turn_then_UI_turn',{'baseline':'B377','local_cities':2,'chain':'actual UI packet->Gameplay request->D/FC/Bindings->Research writers','before':values[0],'after':values[1],'worker_recovery':'retained;not zero all-module work','native_CPU_heap':'USER_GAME_TEST_REQUIRED'})
 def test_single_city_worker_relay_and_same_turn_second_change_keep_sibling(self):
  g,u=composed();g.execute("cities[2].GetBuildings=function()error('UNRELATED_WORKER_CITY')end;counters={}")
  for workers in (1,2):
   g.execute('cities[1].ds[1].workers=...;fire(\'CityWorkerChanged\',0,1)',workers)
   u.execute('Events.CityWorkerChanged.Fire(0,1);publish();assert(packets[sends].CityID==1 and packets[sends].WorkerOnly and not packets[sends].FactsChanged)')
   g.execute("drainworker();assert(cc('BUILDING_LIBRARY')==... and cc('BUILDING_LIBRARY',cities[2])==3);assert(not chair.errors[0][2]and not shared.ResearchApply.errors[0][2])",workers)
  g.execute("local n=reads;local w=writes;for i=1,1000 do drainworker()end;assert(reads==n and writes==w)")
 def test_real_unknown_worker_recovers_from_new_scoped_UI_cause_only(self):
  g,u=composed();g.execute("cities[1].ds[1].workers=nil;fire('CityWorkerChanged',0,1);drainworker();assert(chair.errors[0][1]and cc('BUILDING_LIBRARY')==3);cities[1].ds[1].workers=1;local r,w=reads,writes;for i=1,1000 do drainworker()end;assert(reads==r and writes==w)")
  u.execute('Events.CityWorkerChanged.Fire(0,1);publish()');g.execute("drainworker();assert(cc('BUILDING_LIBRARY')==1 and not chair.errors[0][1])")


class Scope(unittest.TestCase):
 def test_same_city_coalesces_but_different_cities_widen_without_losing_either(self):
  c=ui();c.execute("Events.CityWorkerChanged.Fire(0,7);Events.CityWorkerChanged.Fire(0,7);publish();assert(packets[sends].CityID==7);Events.CityWorkerChanged.Fire(0,7);Events.CityWorkerChanged.Fire(0,8);publish();assert(packets[sends].CityID==nil and packets[sends].WorkerOnly)")
 def test_duplicate_known_local_turn_cannot_widen_queued_city(self):
  c=ui();c.execute("Events.PlayerTurnActivated.Fire(0);local n=sends;Events.CityWorkerChanged.Fire(0,7);Events.PlayerTurnActivated.Fire(0);assert(sends==n);publish();assert(packets[sends].CityID==7 and packets[sends].WorkerOnly)")
 def test_initial_load_unknown_and_focus_remain_conservative(self):
  c=ui();c.execute("assert(packets[1].FactsChanged and not packets[1].WorkerOnly and packets[1].CityID==nil);Events.CityFocusChanged.Fire(0,999);publish();assert(packets[sends].WorkerOnly and packets[sends].CityID==nil);Events.CityWorkerChanged.Fire();publish();assert(not packets[sends].WorkerOnly and packets[sends].CityID==nil);turn=2;Events.LoadScreenClose.Fire();assert(not packets[sends].WorkerOnly and packets[sends].CityID==nil)")
 def test_zero_city_is_preserved_invalid_and_foreign_metadata_never_narrow(self):
  c=ui();c.execute("Events.CityWorkerChanged.Fire(0,0);publish();assert(packets[sends].CityID==0);local n=sends;Events.CityWorkerChanged.Fire(1,0);publish();assert(sends==n);for _,cid in ipairs({-1,1.5,2147483648,'7',math.huge})do Events.CityWorkerChanged.Fire(0,cid);publish();assert(packets[sends].CityID==nil and packets[sends].WorkerOnly)end")
 def test_failed_send_merges_reentrant_different_city_without_resetting_retry_budget(self):
  c=ui();c.execute("""
  local once=true;onSend=function()if once then once=false;Events.CityWorkerChanged.Fire(0,8)end;error('TRANSPORT_FAILED')end
  Events.CityWorkerChanged.Fire(0,7);publish();assert(packets[sends].CityID==7);publish();assert(packets[sends].CityID==nil)
  for i=1,1000 do publish()end;assert(sends==5) -- the real reentrant cause legitimately rearms once
  onSend=nil;Events.CityWorkerChanged.Fire(0,9);publish();assert(sends==6 and packets[sends].CityID==nil)
  -- Previously undelivered owner-wide cause cannot be narrowed by the new city.
  for i=1,1000 do publish()end;assert(sends==6)
  """)
 def test_receiver_accepts_city_only_with_positive_worker_only_provenance(self):
  c=request_context();c.execute("""
  P.Observe=function()end;seen={};dmarks={};shared.NativeFacts.Workers=function(s,cause)seen[#seen+1]=s end
  shared.DistrictCompleteness.MarkDirty=function(pid,cid)dmarks[#dmarks+1]={pid=pid,cid=cid}end
  runRequest(0,{Action='LV2_GPP_DIRTY',Token='SCOPED_WORKER',WorkerOnly=true,FactsChanged=false,CityID=0});assert(seen[1].city==0 and #dmarks==0)
  runRequest(0,{Action='LV2_GPP_DIRTY',Token='SCOPED_WORKER',WorkerOnly=false,FactsChanged=true,CityID=7});assert(seen[2].city==nil and #dmarks==1 and dmarks[1].cid==nil)
  for _,cid in ipairs({-1,1.5,2147483648,'7',math.huge})do runRequest(0,{Action='LV2_GPP_DIRTY',Token='SCOPED_WORKER',WorkerOnly=true,FactsChanged=false,CityID=cid});assert(seen[#seen].city==nil and #dmarks==1)end
  """)

if __name__=='__main__':unittest.main()
