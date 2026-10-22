"""Fresh-session Meaning cleanup gates; actual request/consumer Lua simulation.

No native yield or load-event ordering PASS. Old fixtures keep their default
load notification; only these tests omit/delay it and model owner collections.
"""
import unittest
import test_culture_meaning_probe as legacy
import test_culture_meaning_l2c as l2c
import test_culture_meaning_final_yields as final

class StartupCleanupTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.sql=legacy.database()
 @classmethod
 def tearDownClass(cls):cls.sql.close()
 def runtime(self,real=False):
  helper=legacy.MeaningProbeTests();helper.sql=self.sql
  lua=helper.real_sample_runtime(meaning_ready=False) if real else helper.runtime(meaning_ready=False)
  lua.execute(l2c.HELPERS+final.HELPERS)
  lua.execute(r"""
   -- Native collections contain their owner's cities, not every fixture city.
   local original=Players[0]
   function ownerCities(pid)
    local list={};if not citiesPending then for _,c in ipairs(cities)do if c.owner==pid then list[#list+1]=c end end end
    return {Members=members(list),FindID=function(_,id)for _,c in ipairs(list)do if c.id==id then return c end end end}
   end
   Players[0].GetCities=function()return ownerCities(0)end
   Players[3]={GetCities=function()return ownerCities(3)end}
   function seedValue(c,n)building(c,'BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_'..n,c.ds[1])end
   function emptyMeaning(c)assert(next(exactMeaning(c))==nil)end
   function hasOld(c)local n=0;for id in pairs(c.present)do local row=GameInfo.Buildings[id];if row and gwa.IsOwnedCarrier(row.BuildingType)then n=n+1 end end;return n>0 end
  """)
  return lua
 def test_fresh_missing_load_read_is_readonly_then_background_sample_cleans(self):
  lua=self.runtime(real=True);lua.execute(r"""
   seedValue(a,5);local token=a.token;local before=writes
   local v=finalRequest('CULTURE_MEANING_READ','before-ready')
   assert(v.mode=='OFF' and v.remainingOwned==1 and v.cleanupStatus=='PENDING' and writes==before and not probe.ready)
   sampleRequest(1)
   assert(probe.ready and probe.cleanupStatus=='CONFIRMED' and probe.mode=='OFF');emptyMeaning(a)
   assert(shared.GreatWorkFacts.ack==1 and dialogue.seq[0]==1 and dialogue.samples[0] and gwa.samples[0])
   assert(hasOld(a) and hasOld(b) and a.token==token)
   before=writes;sampleRequest(2);assert(writes==before and probe.cleanupPasses==1)
  """)
 def test_each_legacy_writer_gates_before_positive_projection(self):
  for writer in ('dialogue','gwa'):
   with self.subTest(writer=writer):
    lua=self.runtime();lua.globals().writer=writer;lua.execute(r"""
     seedValue(a,5);local create=P.CreateBuilding
     P.CreateBuilding=function(q,id)
      local name=GameInfo.Buildings[id].BuildingType
      if gwa.IsOwnedCarrier(name) or dialogue.IsOwnedCarrier(name)then emptyMeaning(q.city)end
      return create(q,id)
     end
     if writer=='dialogue' then dialogue.Audit(0)else gwa.Audit(0)end
     assert(probe.ready and probe.cleanupPasses==1);emptyMeaning(a)
    """)
 def test_zero_cities_load_stays_pending_then_existing_turn_retries_once(self):
  lua=self.runtime();lua.execute(r"""
   seedValue(a,5);citiesPending=true;local before=writes;fire('LoadScreenClose')
   assert(not probe.ready and not probe.resetFailed and probe.cleanupStatus=='PENDING' and writes==before)
   citiesPending=false;fire('PlayerTurnActivated',0)
   assert(probe.ready and probe.cleanupStatus=='CONFIRMED');emptyMeaning(a)
   before=writes;fire('PlayerTurnActivated',0);assert(writes==before and probe.cleanupPasses==1)
  """)
 def test_support_unknown_does_not_confirm_or_remove_then_sample_can_retry(self):
  lua=self.runtime();lua.execute(r"""
   seedValue(a,5);local eligible=P.IsTestPlayer;P.IsTestPlayer=function()return false end
   local before=writes;fire('LoadScreenClose');assert(not probe.ready and not probe.resetFailed and writes==before)
   P.IsTestPlayer=eligible;gwa.Audit(0);assert(probe.ready);emptyMeaning(a)
  """)
 def test_all_exact_ids_foreign_scope_and_permanent_state_are_preserved(self):
  lua=self.runtime();lua.execute(r"""
   b.owner=3;seedAllFinalMeaning(a);seedAllFinalMeaning(b)
   local tokenA,tokenB=a.token,b.token;local library=GameInfo.Buildings.BUILDING_LIBRARY.Index
   gwa.Audit(0);emptyMeaning(a);emptyMeaning(b)
   assert(a.token==tokenA and b.token==tokenB and a.present[library] and b.present[library])
   local before=writes;probe.EnsureStartupCleanup('duplicate');assert(writes==before and probe.cleanupPasses==1)
  """)
 def test_failure_locks_automatic_retry_ack_remains_valid_other_city_runs(self):
  lua=self.runtime(real=True);lua.execute(r"""
   seedValue(a,5);seedValue(b,3);failRemove=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_5.Index
   sampleRequest(1)
   assert(probe.resetFailed and probe.cleanupStatus=='FAILED' and not probe.ready)
   assert(shared.GreatWorkFacts.ack==1 and dialogue.seq[0]==1 and dialogue.samples[0] and gwa.samples[0])
   assert(not hasOld(a) and hasOld(b));emptyMeaning(b)
   assert(gwa.last[0][1].error:find('ME_') and not gwa.last[0][2].error)
   local passes=probe.cleanupPasses;local before=writes
   sampleRequest(2);fire('PlayerTurnActivated',0)
   assert(probe.cleanupPasses==passes and writes==before and configured(a,'PRODUCTION')==5)
   failRemove=nil;probe.End(0,a,'explicit-recover');emptyMeaning(a);assert(hasOld(a) and hasOld(b))
   assert(probe.cleanupStatus=='FAILED') -- one-city END is not whole-load success
  """)
 def test_failure_sweep_attempts_foreign_and_other_city_after_failed_city(self):
  lua=self.runtime();lua.execute(r"""
   b.owner=3;seedValue(a,5);seedAllFinalMeaning(b)
   local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_5.Index;local remove=P.RemoveBuilding
   P.RemoveBuilding=function(bs,i)if bs.city==a and i==id then return end;return remove(bs,i)end
   gwa.Audit(0);assert(probe.resetFailed);emptyMeaning(b)
   assert(a.present[id] and not hasOld(a));assert(not probe.CanProjectLegacy(0,a))
  """)
 def test_off_end_with_saved_residue_is_real_scoped_cleanup_and_token_idempotent(self):
  lua=self.runtime();lua.execute(r"""
   seedValue(a,5);seedValue(b,4);local other=snapshotBuildings(b);assert(probe.mode=='OFF')
   probe.End(0,a,'off-end');emptyMeaning(a);assert(hasOld(a));assertBuildingsSame(b,other)
   local before=writes;probe.End(0,a,'off-end');assert(writes==before)
  """)
 def test_off_end_failure_keeps_residue_no_legacy_reapply_new_token_recovers(self):
  lua=self.runtime();lua.execute(r"""
   seedValue(a,5);local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_5.Index
   failRemove=id;local other=snapshotBuildings(b)
   assert(not pcall(probe.End,0,a,'failed-off-end') and a.present[id] and probe.error and not hasOld(a))
   failRemove=nil;local before=writes;probe.End(0,a,'failed-off-end');assert(writes==before and a.present[id])
   probe.End(0,a,'new-off-end');emptyMeaning(a);assert(hasOld(a));assertBuildingsSame(b,other)
  """)
 def test_reentrant_cleanup_never_restores_legacy_before_withdrawal(self):
  lua=self.runtime();lua.execute(r"""
   seedAllFinalMeaning(a);seedAllFinalMeaning(b);local remove=P.RemoveBuilding;local calls=0
   P.RemoveBuilding=function(bs,id)
    remove(bs,id);calls=calls+1;assert(calls<200)
    dialogue.Audit(0,bs.city.id);gwa.Audit(0,bs.city.id);probe.EnsureStartupCleanup('reentrant')
   end
   dialogue.Audit(0);gwa.Audit(0);assert(probe.ready and not probe.busy and not dialogue.busy and not gwa.busy)
   emptyMeaning(a);emptyMeaning(b);assert(probe.cleanupPasses==1 and hasOld(a) and hasOld(b))
  """)

 def test_off_end_global_audit_reentry_does_not_withdraw_clean_other_city(self):
  lua=self.runtime();lua.execute(r"""
   seedValue(a,5);local other=snapshotBuildings(b);local remove=P.RemoveBuilding;local calls=0
   P.RemoveBuilding=function(bs,id)
    remove(bs,id);calls=calls+1;assert(calls<200);dialogue.Audit(0);gwa.Audit(0)
   end
   probe.End(0,a,'reentrant-off-end');emptyMeaning(a);assert(hasOld(a));assertBuildingsSame(b,other)
   assert(not probe.busy and not dialogue.busy and not gwa.busy and probe.cleanupPasses==0)
  """)
 def test_confirmed_fast_path_adds_no_scan_or_write_and_same_turn_changes_still_apply(self):
  lua=self.runtime();lua.execute(r"""
   gwa.Audit(0);assert(probe.ready);local scans=counts.city_scan;local before=writes
   for i=1,5 do assert(probe.CanProjectLegacy(0,a) and probe.CanProjectLegacy(0,b))end
   assert(scans==counts.city_scan and writes==before)
   a.active=3;gwa.Audit(0,1);assert(not hasOld(a) and hasOld(b))
   a.active=4;gwa.Audit(0,1);assert(hasOld(a) and hasOld(b))
  """)

if __name__=='__main__':unittest.main()
