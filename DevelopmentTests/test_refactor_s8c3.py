"""S8c3 actual Store ordering/reentry and deferred effect integration; native doubles only."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import ROOT,TrackedLua51,SOURCES,Context,legacy_source_observation,measure,executed,completion
from test_refactor_s7f import actual_store

BASE='55b4b6c6c348bc9f855ff5d1d728675aa909f569'
EFFECTS=('CultureAesthetic','CultureMeaning','CultureInspiration','DialogueEffects','CultureInsightsTourism')
@contextmanager
def history():
 original={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('CityProgressionStore',*EFFECTS)}
 read,execute,load=Path.read_text,TrackedLua51.execute,Context.load;hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in original.items()}
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

SETUP="""
c=a;origin=c:GetID();s=shared.CityProgressionStore;s.RegisterExit('Cleanup',function()end)
function lose()T.loss(c,9,900)end
function back()
 c.s.ref.owner=0;c.s.ref.cityID=origin;Events.CityTransfered.Fire(0,origin,9)
end
"""
def store():
 vm=actual_store();vm.execute(SETUP);return vm


class OrderedReturn(unittest.TestCase):
 def test_throwing_callbacks_counterexample_then_all_independent_invalidations_run(self):
  results=[]
  for old in (True,False):
   with history()if old else nullcontext():v=store()
   v.execute("calls=0;for _,n in ipairs({'Alpha','Beta','Zeta'})do s.RegisterReturn(n,function()calls=calls+1;error('DEPENDENCY_FAILED')end)end;lose();local w=T.writes();back();assert(T.record(c).stage=='HELD_TRANSFER'and T.writes()==w)")
   results.append(v.eval('calls'))
  self.assertEqual(results,[1,3]);measure('S8c3_return_fault_isolation',{'before_callbacks':1,'after_callbacks':3,'commit_on_failure':False,'new_retry':False})
 def test_phase_order_is_stable_across_registration_order(self):
  names=['ZLast','NetworkBridge','CultureAesthetic','GreatWorkFacts','Dialogue','DistrictCompleteness','IndustrySupport','DevelopmentInvestment']
  for order in (names,list(reversed(names)),names[3:]+names[:3]):
   v=store();v.execute('order={};labels=...;',v.table_from(order))
   v.execute("for _,n in ipairs(labels)do local label=n;s.RegisterReturn(n,function()order[#order+1]=label;assert(T.record(c).stage=='HELD_TRANSFER')end)end;lose();back();assert(T.record(c).stage=='ACTIVE')")
   self.assertEqual(list(v.eval('order').values()),['DistrictCompleteness','GreatWorkFacts','NetworkBridge','DevelopmentInvestment','Dialogue','IndustrySupport','CultureAesthetic','ZLast'])
 def test_false_and_unprintable_errors_block_commit_with_detached_recoverable_status(self):
  for mode in ('false','unprintable'):
   v=store();v.execute("""
   mode=...;later=0;s.RegisterReturn('Alpha',function()
    if repaired then return true end;if mode=='false'then return false end
    error(setmetatable({},{__tostring=function()error('FORMAT_UNKNOWN')end}))
   end)
   s.RegisterReturn('Zeta',function()later=later+1 end);lose();back()
   assert(T.record(c).stage=='HELD_TRANSFER'and later==1)
   local status=s.Status(c);assert(status.returnErrors.Alpha and status.returnRejection=='RETURN_CALLBACK_FAILED')
   status.returnErrors.Alpha=nil;assert(s.Status(c).returnErrors.Alpha)
   repaired=true;back();assert(T.record(c).stage=='ACTIVE'and later==2 and next(s.Status(c).returnErrors)==nil)
   """,mode)
 def test_same_native_event_reentry_runs_callbacks_once(self):
  v=store();v.execute("calls=0;s.RegisterReturn('Once',function()calls=calls+1;Events.CityTransfered.Fire(0,origin,9)end);lose();back();assert(calls==1 and T.record(c).stage=='ACTIVE')")
 def test_first_Handle_site_lookup_reentry_is_bounded(self):
  v=store();v.execute("""
  calls=0;s.RegisterReturn('Once',function()calls=calls+1 end);lose();local get=CityManager.GetCityAt
  lookups,depth,maxDepth=0,0,0
  CityManager.GetCityAt=function(x,y)
   if x==c:GetX()then
    lookups=lookups+1;depth=depth+1;maxDepth=math.max(depth,maxDepth)
    if depth<6 then Events.CityTransfered.Fire(0,origin,9)end
    depth=depth-1
   end
   return get(x,y)
  end
  back();assert(lookups==2 and maxDepth==1 and calls==1 and T.record(c).stage=='ACTIVE')
  """)
 def test_late_registration_from_final_native_read_keeps_candidate_held(self):
  v=store();v.execute("""
  local done=false;local after=0;local once=true;late=0
  s.RegisterReturn('First',function()done=true end);local get=c.GetOwner
  c.GetOwner=function(city)
   if done then after=after+1;if after==2 and once then once=false;s.RegisterReturn('Late',function()late=late+1 end)end end
   return get(city)
  end
  lose();back();assert(T.record(c).stage=='HELD_TRANSFER'and late==0)
  back();assert(T.record(c).stage=='ACTIVE'and late==1)
  """)
 def test_late_registration_inside_callback_is_not_silently_skipped(self):
  v=store();v.execute("""
  once=true;late=0;s.RegisterReturn('First',function()if once then once=false;s.RegisterReturn('Late',function()late=late+1 end)end end)
  lose();back();assert(T.record(c).stage=='HELD_TRANSFER'and late==0)
  back();assert(T.record(c).stage=='ACTIVE'and late==1)
  """)
 def test_native_reference_change_stops_unsafe_remaining_work_and_cannot_commit(self):
  v=store();v.execute("""
  later=0;s.RegisterReturn('Alpha',function()c.s.ref.owner=9;c.s.ref.cityID=900 end)
  s.RegisterReturn('Zeta',function()later=later+1 end);lose();back()
  assert(T.record(c).stage=='HELD_TRANSFER'and later==0 and s.Status(c).returnRejection=='RETURN_CONTEXT_CHANGED')
  """)
 def test_initial_unprintable_lookup_releases_busy_for_next_real_return(self):
  v=store();v.execute("""
  calls=0;s.RegisterReturn('Once',function()calls=calls+1 end);lose();local get=CityManager.GetCityAt
  CityManager.GetCityAt=function()error(setmetatable({},{__tostring=function()error('FORMAT_UNKNOWN')end}))end
  back();assert(T.record(c).stage=='HELD_TRANSFER'and calls==0)
  CityManager.GetCityAt=get;back();assert(T.record(c).stage=='ACTIVE'and calls==1)
  """)
 def test_write_boundary_rejects_new_registration_and_never_exposes_success(self):
  v=store();v.execute("""
  lose();local set=Game.SetProperty;local key=T.key(c)
  Game.SetProperty=function(o,k,value)
   set(o,k,value);if k==key and value.stage=='ACTIVE'then s.RegisterReturn('TooLate',function()end)end
  end
  back();assert(not pcall(s.Base,0,c)) -- setter may have applied; authority stays guarded, never guessed
  """)
 def test_healthy_return_record_bytes_and_write_counts_match_baseline(self):
  values=[]
  for old in (True,False):
   with history()if old else nullcontext():v=store()
   v.execute("s.RegisterReturn('Mark',function()end);lose();back();assert(T.record(c).stage=='ACTIVE');bytes=T.encode(T.record(c));writes=T.writes()")
   values.append((v.eval('bytes'),v.eval('writes')))
  self.assertEqual(values[0],values[1])
 def test_idle_publication_has_no_return_work(self):
  v=store();v.execute("calls=0;s.RegisterReturn('Once',function()calls=calls+1 end);lose();back();local w=T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(calls==1 and T.writes()==w)")


class DeferredEffects(unittest.TestCase):
 def test_five_actual_registrations_only_mark_existing_deferred_work(self):
  for name in EFFECTS:
   c=Context();c.execute("""
   P={Field=function(t,k)return t and t[k]end,IsTestPlayer=function(pid)return pid==0 end,Count=function()end,
    Info=function()error('INLINE_NATIVE_READ')end,Rows=function()error('INLINE_NATIVE_SCAN')end}
   returns={};shared.CityProgressionStore={RegisterExit=function()end,RegisterReturn=function(n,f)returns[n]=f end}
   shared.GreatWorkFacts={RegisterConsumer=function()end};shared.CultureInspirationProbe={retired=true}
   shared.GreatWorkAdjacency={retired=true};shared.Dialogue={Init=function()end}
   GameInfo={Eras=function()local i=0;return function()i=i+1;if i<=8 then return {EraType='ERA_'..i}end end end}
   """);c.load(name);c.execute("module=...;local d=_G['SPC'..module].Start(P,shared);local mark=d.MarkAudit;marks=0;d.Audit=function()error('INLINE_AUDIT')end;d.MarkAudit=function(scope)marks=marks+1;assert(scope.player==0 and scope.city==101);return mark(scope)end;returns[module](0,{GetID=function()return 101 end});assert(marks==1)",name)
 def test_original_fake_store_inline_assertion_retained_on_exact_source(self):
  from test_refactor_s5d4c6 import InsightsHealth
  with history():InsightsHealth().test_confirmed_exit_return_preserves_history()
  from test_refactor_s5d3 import Dialogue
  Dialogue.setUpClass()
  try:
   with history():Dialogue().test_confirmed_store_exit_and_return_keep_history_and_recompute()
  finally:Dialogue.tearDownClass()
 def test_actual_store_commit_then_existing_publish_restores_insight_carrier(self):
  v=actual_store();v.execute("""
  local oldA=a;a=shared.InvestmentAction
  for i=1,3 do T.invest(b,12000+i)end;a=oldA;T.governor(4)
  local store=shared.CityProgressionStore;assert(store.AddExpeditionInsight(0,b,'CIVILIZATION_OTHER','PEOPLE',T.now()))
  info={Buildings={},Modifiers={},DynamicModifiers={}};args={};links={};carrierCreates=0;factReads=0
  info.DynamicModifiers.MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS={CollectionType='COLLECTION_OWNER',EffectType='EFFECT_ADJUST_CITY_TOURISM_LATE_ERAS'}
  for n=1,192 do local bn='BUILDING_SPC_INSIGHT_TOURISM_'..n;local mid='SPC_INSIGHT_TOURISM_'..n
   info.Buildings[bn]={Index=n,InternalOnly=1,PrereqDistrict='DISTRICT_CITY_CENTER',CitizenSlots=0,Housing=0}
   info.Modifiers[mid]={ModifierType='MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS'}
   args[#args+1]={ModifierId=mid,Name='Modifier',Value=tostring(n*2)};args[#args+1]={ModifierId=mid,Name='MinimumEra',Value='ERA_ANCIENT'}
   links[#links+1]={BuildingType=bn,ModifierId=mid}
  end
  local infoBefore,rowsBefore=P.Info,P.Rows
  P.Info=function(t,k)if info[t]then return info[t][k]end;return infoBefore(t,k)end
  P.Rows=function(t)if t=='ModifierArguments'then return args elseif t=='BuildingModifiers'then return links end;return rowsBefore(t)end
  for _,city in ipairs({a,b})do
   city.present={};city.GetBuildings=function(c)return {city=c,GetBuildingLocation=function()return c:GetX()end,IsPillaged=function()return false end}end
   city.GetBuildQueue=function(c)return {city=c}end
  end
  P.HasBuilding=function(bs,n)return bs.city.present[n]==true end
  P.RemoveBuilding=function(bs,n)bs.city.present[n]=nil end
  P.CreateBuilding=function(q,n)assert(T.record(q.city).stage=='ACTIVE','INLINE_HELD_PROJECTION');q.city.present[n]=true;carrierCreates=carrierCreates+1 end
  PlayerConfigurations={[0]={GetCivilizationTypeName=function()return 'CIVILIZATION_HOME'end}}
  SPCDistrictCompleteness={Clone=M.Copy};local ef=shared.EffectiveFacts.Read
  shared.EffectiveFacts.Read=function(...)factReads=factReads+1;return ef(...)end
  include('CultureInsightsTourism');d=SPCCultureInsightsTourism.Start(P,shared);d.Audit();assert(b.present[1])
  local original=b:GetID();T.loss(b,9,900);assert(not b.present[1]and T.record(b).stage=='HELD_TRANSFER')
  local beforeFacts,beforeCreates= factReads,carrierCreates
  b.s.ref.owner=0;b.s.ref.cityID=original;Events.CityTransfered.Fire(0,original,9)
  assert(T.record(b).stage=='ACTIVE'and not b.present[1]and factReads==beforeFacts and carrierCreates==beforeCreates)
  Events.GameCoreEventPublishComplete.Fire()
  assert(b.present[1]and carrierCreates==beforeCreates+1 and factReads==beforeFacts+1 and not d.errors['0:'..original])
  assert(store.ExpeditionInsights(0,b)['CIVILIZATION_OTHER:PEOPLE'])
  local writes=T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end
  assert(carrierCreates==beforeCreates+1 and T.writes()==writes)
  """)
  measure('S8c3_real_Store_Insights_return',{'inline_HELD_projection':0,'post_commit_publication_projection':1,'archive_preserved':True,'idle_extra_writes':0,'native_doubles':'catalogue and carrier presence; actual Store/EF/Insights/RuntimeWork'})

if __name__=='__main__':unittest.main()
