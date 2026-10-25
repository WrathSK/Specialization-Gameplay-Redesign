"""R18 normal Half experiment retirement, central exact cleanup remains mandatory."""
from pathlib import Path
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from unittest.mock import patch
import re,subprocess,unittest
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,measure,executed,completion
from test_refactor_s8c5c import production,entry


@contextmanager
def baseline():
 paths=('Gameplay','HalfYieldProbe')
 rows={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','65c46ca:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in paths}
 read,execute,load=Path.read_text,TrackedLua51.execute,Context.load
 hashes={sha256(s.encode()).hexdigest():'historical/65c46ca/'+str(p.relative_to(ROOT))for p,s in rows.items()}
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 def historical_load(vm,name):
  p=ROOT/'Mod'/(name if name.endswith('.lua')else name+'.lua')
  if p not in rows:return load(vm,name)
  text=rows[p];h=sha256(text.encode()).hexdigest();key=hashes[h];executed(key,h)
  try:result=vm.execute(text)
  except Exception:completion(key,False);raise
  completion(key,True);return result
 with patch.object(Path,'read_text',lambda p,*a,**kw:rows[p]if p in rows else read(p,*a,**kw)),patch.object(TrackedLua51,'execute',run),patch.object(Context,'load',historical_load):yield


def half(cities=100):
 v=Context();v.execute("""
 reads=0;writes=0;P={IsTestPlayer=function(pid)return pid==0 end,Field=function(t,k)return t and t[k]end,
 Count=function(k)counts[k]=(counts[k]or 0)+1 end,SetProperty=function()writes=writes+1 end}
 Players={};for pid=0,...-1 do
  local city={GetID=function()return pid end,GetOwner=function()return pid end,
   GetProperty=function()reads=reads+1;return false end}
  Players[pid]={GetCities=function()reads=reads+1;return {Members=function()return ipairs({city})end}end}
 end
 composition={Run=function(name,deps,exports,fn)assert(name=='HalfYieldProbe');return fn()end}
 """,cities)
 # Execute the exact production entry, not independently invented startup flags.
 v.execute(entry('HalfYieldProbe'));return v


class Retired(unittest.TestCase):
 def test_actual_production_has_no_load_turn_population_or_transfer_city_scans(self):
  values=[]
  for old in (True,False):
   with baseline()if old else nullcontext():v=half()
   v.execute("Events.LoadScreenClose.Fire();for i=1,10 do Events.PlayerTurnActivated.Fire(i);Events.CityPopulationChanged.Fire(i,i);Events.CityTransfered.Fire(9,900+i,10)end;for i=1,1000 do publish()end")
   values.append(dict(reads=v.eval('reads'),writes=v.eval('writes'),city_scans=v.eval('counts.city_scan or 0')))
  self.assertEqual(values[0]['city_scans'],3100)
  self.assertEqual(values[1],dict(reads=0,writes=0,city_scans=0))
  measure('S9e4_Half_production_retirement',{'baseline':'B376','world_cities':100,'load_turn_population_transfer_boundaries':31,'before':values[0],'after':values[1],'scope':'actual Half module using actual Gameplay startup entry; other modules not implied'})
 def test_retired_DEV_compatibility_cannot_read_or_write_even_for_ON(self):
  v=half();v.execute("""
  local d=shared.HalfYieldProbe;assert(d.ready and d.retired and d.Audit==nil)
  local city=setmetatable({},{__index=function()error('RETIRED_NATIVE_READ')end})
  P.SetProperty=function()error('RETIRED_PROPERTY_WRITE')end
  for _,action in ipairs({'HALF_ON','HALF_OFF','HALF_READ'})do assert(d.Run(0,city,action):find('已退役',1,true))end
  assert(d.Describe(0,city):find('已退役',1,true)and reads==0 and writes==0)
  for _,name in ipairs({'LoadScreenClose','PlayerTurnActivated','CityPopulationChanged','CityTransfered'})do assert(Events[name].Count()==0)end
  """)
 def test_actual_central_exit_removes_all32_ids_without_probe_audit(self):
  v=production();v.execute("""
  assert(shared.HalfYieldProbe.retired and shared.HalfYieldProbe.Audit==nil)
  assert(#byGroup.HalfYieldProbe.names==32);lose();assert(status()=='WITHDRAWN'and removeCalls==1409 and plotWrites==2)
  for _,name in ipairs(byGroup.HalfYieldProbe.names)do assert(not ca.present[definitions[name].Index]and cb.present[definitions[name].Index])end
  """)
 def test_original_Store_ticket_recovers_failed_half_cleanup_without_experiment(self):
  v=production();v.execute("""
  faultGroup='HalfYieldProbe';lose();assert(status()=='PARTIAL_HELD'and removeCalls==1377 and plotWrites==2)
  for _,name in ipairs(byGroup.HalfYieldProbe.names)do assert(ca.present[definitions[name].Index])end
  faultGroup=nil;s.ExitConfirmed();assert(status()=='WITHDRAWN'and removeCalls==1409)
  local n=removeCalls;s.ExitConfirmed();assert(removeCalls==n and shared.HalfYieldProbe.retired)
  """)
 def test_probe_start_failure_cannot_disable_central_physical_cleanup(self):
  v=production(failure='HalfYieldProbe');v.execute("assert(shared.HalfYieldProbe==nil);lose();assert(status()=='WITHDRAWN'and removeCalls==1409 and plotWrites==2)")
 def test_SQL_save_keys_and_exact_catalog_remain_unchanged(self):
  p='Mod/Data/HalfYieldProbe.sql';self.assertEqual((ROOT/p).read_bytes(),subprocess.check_output(['git','show','65c46ca:'+p],cwd=ROOT))
  v=Context();v.load('LegacyCleanupCatalog');v.execute("local row=SPCLegacyCleanupCatalog.Group('HalfYieldProbe');assert(row.kind=='buildings'and #row.names==32);local seen={};for _,n in ipairs(row.names)do assert(n:match('^BUILDING_SPC_B050_')and not seen[n]);seen[n]=true end")
  self.assertIn('SPC_B050_HALF_ENABLED',(ROOT/'Mod/HalfYieldProbe.lua').read_text())

if __name__=='__main__':unittest.main()
