"""S7f Store locator identity, explicit native guards and bounded pending recovery."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,executed,completion,legacy_source_observation,measure
import test_store_write_boundaries as store_cases
from test_refactor_s4a import industry,load_industry_ui
from test_refactor_s7e import retirement

BASE='604aa32923e6eaf29efe53ec7cd33ca0a2f354c9'
@contextmanager
def history():
 paths=('RuntimeWork','IndustrySupport','CityProgressionStore')
 original={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in paths}
 read,execute,load=Path.read_text,TrackedLua51.execute,Context.load
 hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in original.items()}
 def source(p,*a,**kw):return original[p]if p in original else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 def module(c,name):
  p=ROOT/'Mod'/(name if name.endswith('.lua')else name+'.lua')
  if p not in original:return load(c,name)
  text=original[p];h=sha256(text.encode()).hexdigest();key=hashes[h];executed(key,h)
  try:out=c.lua.execute(text)
  except Exception:completion(key,False);raise
  completion(key,True);return out
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),patch.object(Context,'load',module),legacy_source_observation():yield


def actual_store():
 with patch.object(store_cases,'LuaRuntime',TrackedLua51),legacy_source_observation():vm=store_cases.fixture()
 vm.execute("T.start();a,b=T.two();include('RuntimeWork');SPCRuntimeWork.StartRetirement(P,shared)")
 return vm


def pending():
 vm=industry();load_industry_ui(vm);vm.execute("""
 refReads=0;badReference=false;local raw=cities[2].GetProperty
 cities[2].GetProperty=function(c,key)
 if key=='SPC_DEV_BINDING_B013_TOKEN'then refReads=refReads+1;if badReference then error('REFERENCE_TEMPORARILY_UNKNOWN')end end
 return raw(c,key)end
 shared.CityProgressionStore=shared.CityProgressionStore or {}
 shared.CityProgressionStore.ReferenceToken=function(c)
 refReads=refReads+1;if badReference and c==cities[2]then error('REFERENCE_TEMPORARILY_UNKNOWN')end
 if onReference then onReference(c)end;return 'STORE:'..c:GetID()end
 d.MarkCity(cities[2]);refReads=0
 """);return vm


class ScalarReference(unittest.TestCase):
 def fixture(self):
  c=Context();c.load('CityReference');c.execute("""
  a={owner=0,id=1,x=10,y=20,token='RAW'}
  function a:GetOwner()return self.owner end;function a:GetID()return self.id end
  function a:GetX()return self.x end;function a:GetY()return self.y end
  function a:GetProperty()rawReads=rawReads+1;return self.token end
  rawReads=0;shared.CityProgressionStore={UsesNewAuthority=true,ReferenceToken=function(c)if callback then callback(c)end;return formalToken end}
  formalToken='FORMAL'
  """);return c
 def test_modern_token_never_follows_city_marker_and_unregistered_is_not_fallback(self):
  c=self.fixture();c.execute("r=SPCCityReference.Read(shared,a);assert(r.token=='FORMAL'and r.source=='STORE'and rawReads==0);a.token='OTHER';assert(SPCCityReference.Equal(r,SPCCityReference.Read(shared,a)));formalToken=nil;local unregistered=SPCCityReference.Read(shared,a);assert(unregistered.token==nil and unregistered.source=='STORE'and rawReads==0)")
 def test_missing_or_failed_modern_provider_cannot_fall_back(self):
  c=self.fixture();c.execute("shared.CityProgressionStore.ReferenceToken=nil;assert(not pcall(SPCCityReference.Read,shared,a)and rawReads==0);shared.CityProgressionStore.ReferenceToken=function()error('STORE_UNKNOWN')end;assert(not pcall(SPCCityReference.Read,shared,a)and rawReads==0)")
 def test_native_owner_id_location_mutation_inside_provider_is_unknown(self):
  for field in ('owner','id','x','y'):
   c=self.fixture();c.execute("local field=...;callback=function(c)c[field]=99 end",field);c.execute("assert(not pcall(SPCCityReference.Read,shared,a)and rawReads==0)")
 def test_detached_scalar_and_length_delimited_key_keep_same_turn_changes(self):
  c=self.fixture();c.execute("local r=SPCCityReference.Read(shared,a);local k=SPCCityReference.Key(r);r.token='MUTATE';assert(SPCCityReference.Key(SPCCityReference.Read(shared,a))==k);formalToken='FORMAL:next';assert(SPCCityReference.Key(SPCCityReference.Read(shared,a))~=k);formalToken='FORMAL';a.id=2;assert(SPCCityReference.Key(SPCCityReference.Read(shared,a))~=k)")
 def test_explicit_isolated_legacy_profile_retains_native_marker_without_service(self):
  c=self.fixture();c.execute("shared.CityProgressionStore=nil;local r=SPCCityReference.Read(shared,a);assert(r.token=='RAW'and r.source=='LEGACY_NATIVE'and rawReads==1);a.GetX=nil;a.GetY=nil;assert(SPCCityReference.Read(shared,a).x==nil)")


class ActualStore(unittest.TestCase):
 def test_retirement_uses_actual_store_token_with_no_raw_marker_read_or_permanent_write(self):
  vm=actual_store();vm.execute("""
  local token=shared.CityProgressionStore.ReferenceToken(a);assert(token==T.record(a).base.token)
  local raw=a.GetProperty;a.GetProperty=function(c,k)if k=='SPC_DEV_BINDING_B013_TOKEN'then error('RAW_MARKER_MUST_NOT_BE_READ')end;return raw(c,k)end
  local before=T.writes();clean=0
  local function retire()return SPCRuntimeWork.RetireOnce(P,shared,a,'ACTUAL',function()clean=clean+1;return 1 end)end
  assert(retire()==1 and retire()==0 and clean==1 and T.writes()==before)
  assert(not pcall(shared.CityProgressionStore.HistoricalReference,a)) -- locator is not active/history authority
  """)
 def test_foreign_held_reference_retains_locator_but_never_grants_history_access(self):
  vm=actual_store();vm.execute("""
  local token=shared.CityProgressionStore.ReferenceToken(a);local before=SPCCityReference.Read(shared,a)
  T.loss(a,9,900);assert(shared.CityProgressionStore.ReferenceToken(a)==token)
  local after=SPCCityReference.Read(shared,a);assert(after.owner==9 and after.cityID==900 and after.token==token and not SPCCityReference.Equal(before,after))
  assert(not pcall(shared.CityProgressionStore.Base,0,a)and not pcall(shared.CityProgressionStore.HistoricalReference,a))
  local writes=T.writes();SPCRuntimeWork.RetireOnce(P,shared,a,'FOREIGN',function()return 0 end);assert(T.writes()==writes)
  """)
 def test_unregistered_city_stays_unregistered_and_pristine_uninitialized_is_unknown(self):
  vm=actual_store();vm.execute("local c=T.fresh(3);c.s.values.TOKEN='FORGED';local w=T.writes();assert(shared.CityProgressionStore.ReferenceToken(c)==nil and SPCCityReference.Read(shared,c).token==nil and T.writes()==w)")
  with patch.object(store_cases,'LuaRuntime',TrackedLua51),legacy_source_observation():cold=store_cases.fixture()
  cold.execute("T.start();local c=T.fresh(1);T.propsSet(SPCCityProgressionStore.INDEX,nil);shared={};SPCCityProgressionStore.Start(P,shared);include('CityReference');assert(not pcall(SPCCityReference.Read,shared,c))")
 def test_actual_store_write_barrier_rejects_locator_and_after_commit_recovers(self):
  vm=actual_store();vm.execute("""
  local set=Game.SetProperty;observed=0
  Game.SetProperty=function(o,k,v)
  if k==T.key(a)then observed=observed+1;local ok,why=pcall(shared.CityProgressionStore.ReferenceToken,a);assert(not ok and tostring(why):find('STORE_COLLECTION_BUSY'))end
  return set(o,k,v)end
  local s=T.storage(a);local n=T.normal(s.Read());assert(s.Write(s.Read(),n)==nil)
  assert(observed==1 and shared.CityProgressionStore.ReferenceToken(a)==n.base.token)
  """)


class IndustryPending(unittest.TestCase):
 def test_reference_unknown_does_not_rearm_thousand_publish_baseline_counterexample(self):
  results=[]
  for old in (True,False):
   with history()if old else nullcontext():vm=pending()
   vm.execute("""
   badReference=true;pcall(fire,'GameCoreEventPublishComplete');local first=refReads
   for i=1,1000 do pcall(fire,'GameCoreEventPublishComplete')end;extra=refReads-first
   """)
   results.append(vm.eval('extra'))
  self.assertEqual(results,[1000,0]);measure('S7f_Industry_reference_UNKNOWN',{'before_extra_reference_reads':1000,'after_extra_reference_reads':0,'periodic_retry_added':False})
 def test_related_recovery_repairs_once_and_unknown_sibling_does_not_block(self):
  vm=pending();vm.execute("""
  d.MarkCity(cities[1]);badReference=true;local visits={};local audit=d.Audit
  d.Audit=function(s)visits[s.city]=(visits[s.city]or 0)+1;return audit(s)end
  fire('GameCoreEventPublishComplete');assert(visits[1]==1 and not visits[2]and d.errors['0:2'])
  local n=refReads;for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(refReads==n)
  badReference=false;cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']=nil
  d.MarkCity(cities[2]);fire('GameCoreEventPublishComplete');assert(visits[2]==1 and not d.errors['0:2']and cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'])
  """)
 def test_same_turn_newer_pending_cause_inside_reference_read_survives(self):
  vm=pending();vm.execute("""
  local audit=d.Audit;visits=0;d.Audit=function(s)visits=visits+1;return audit(s)end
  onReference=function(c)if c==cities[2]then onReference=nil;d.MarkCity(c)end end
  fire('GameCoreEventPublishComplete');assert(visits==0)
  fire('GameCoreEventPublishComplete');assert(visits==1)
  local n=refReads;for i=1,100 do fire('GameCoreEventPublishComplete')end;assert(visits==1 and refReads==n)
  """)
 def test_confirmed_replaced_token_drops_old_work_until_new_related_cause(self):
  vm=pending();vm.execute("""
  local audit=d.Audit;visits=0;d.Audit=function(s)visits=visits+1;return audit(s)end
  shared.CityProgressionStore.ReferenceToken=function()return 'REPLACED'end
  fire('GameCoreEventPublishComplete');assert(visits==0)
  d.MarkCity(cities[2]);fire('GameCoreEventPublishComplete');assert(visits==1)
  """)

if __name__=='__main__':unittest.main()
