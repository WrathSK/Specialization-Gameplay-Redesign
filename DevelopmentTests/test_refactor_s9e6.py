"""Accepted R01 source-local UNKNOWN effects; topology and transactions stay strict."""
from contextlib import contextmanager,nullcontext
from pathlib import Path
from hashlib import sha256
from unittest.mock import patch
import subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,measure
from refactor_defect_fixtures import commerce
from test_refactor_s4b import culture,standard
import test_refactor_s4b as old_cases


@contextmanager
def baseline():
 rows={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','9316565:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('NetworkBridge','Commerce')}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(s.encode()).hexdigest():'historical/9316565/'+str(p.relative_to(ROOT))for p,s in rows.items()}
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',lambda p,*a,**kw:rows[p]if p in rows else read(p,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield


def unknown_unrelated(v):
 v.execute("cities[3].fail=true;cities[3].identityFail=true;cities[3].token='NEW_UNREADABLE_REFERENCE';net.Refresh(0)")


class SourceLocal(unittest.TestCase):
 def test_unrelated_never_known_role_does_not_freeze_readable_commercialization(self):
  values=[]
  for old in (True,False):
   with baseline()if old else nullcontext():
    v=commerce();v.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));assert(ownedGold(cities[2])==15)")
    unknown_unrelated(v);v.execute("cities[1].yields.SCIENCE=900;com.SourceChanged(0,1)")
    values.append(dict(gold=v.eval('ownedGold(cities[2])'),configure=v.eval('view(2).canConfigure'),transaction=v.eval('net.TransactionCurrent(0)'),availability=v.eval('net.Input(0).effectAvailability')))
    if not old:v.execute("assert(net.Input(0).factAvailability=='MIXED'and net.Input(0).provenance[3].status=='UNKNOWN');assert(net.CurrentDomesticPartners(0,cities[2]).validity=='UNKNOWN'and not pcall(net.CurrentCapitalSources,0,cities[2],'RESEARCH'));assert(toggle(2,'DISTRICT_THEATER',true))")
  self.assertEqual(values[0]['gold'],15);self.assertEqual(values[1]['gold'],135)
  self.assertFalse(values[0]['configure']);self.assertTrue(values[1]['configure']);self.assertFalse(values[1]['transaction'])
  measure('S9e6_unrelated_unknown_role',{'baseline':'B378','before':values[0],'after':values[1],'rule':'accepted R01;reversible local configuration only;no transaction credential'})
 def test_unknown_city_is_not_added_as_source_until_new_reliable_fact(self):
  v=culture();unknown_unrelated(v);v.execute("""
  complete(3,2);complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1)
  assert(net.Input(0).provenance[3].status=='UNKNOWN'and cn.records['0:1'].contributions[3]==nil)
  cities[3].fail=false;cities[3].kind='CULTURE';cities[3].potential=4;cities[3].active=4
  send('0,4,0,2,10;0,3,0,2,11;0,2,0,1,12',3)
  assert(amount(cities[1])==2 and cn.records['0:1'].provenance[3].status=='CONFIRMED')
  """)
 def test_partial_retained_source_and_new_readable_source_can_update_same_receiver(self):
  v=culture();v.execute("complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1)");unknown_unrelated(v)
  v.execute("""
  cities[4].historyUnknown=true;cities[5].kind='CULTURE';cities[5].potential=4;cities[5].active=4;complete(5,2)
  send('0,4,0,2,10;0,5,0,2,11;0,2,0,1,12',3)
  local r=cn.records['0:1'];assert(amount(cities[1])==2 and r.provenance[4].status=='RETAINED'and r.provenance[5].status=='CONFIRMED')
  assert(not net.TransactionCurrent(0));local n=created+removed;for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(created+removed==n)
  """)
 def test_known_source_loss_and_other_positive_change_do_not_become_whole_continuity(self):
  v=culture();v.execute("complete(4,1);cn.SourceChanged(0,4)");unknown_unrelated(v)
  v.execute("""
  cities[4].kind='NONE';cities[4].potential=0;cities[4].active=0
  cities[5].kind='CULTURE';cities[5].potential=4;cities[5].active=4;complete(5,2);complete(5,3)
  send('0,4,0,2,10;0,5,0,2,11;0,2,0,1,12',3)
  local r=cn.records['0:1'];assert(amount(cities[1])==2 and r.set.CIVILIZATION_TEST_2 and r.set.CIVILIZATION_TEST_3 and not r.set.CIVILIZATION_TEST_1)
  assert(not net.Input(0).continuityOnly and net.Input(0).effectAvailability=='AVAILABLE'and not net.TransactionCurrent(0))
  """)
 def test_unadmitted_direct_source_retains_its_reliable_old_sample(self):
  v=commerce();v.execute("""
  assert(toggle(2,'DISTRICT_CAMPUS',true));local n=ownedGold(cities[2]);assert(n==15)
  cities[1].unregistered=true;cities[1].fail=true;cities[1].identityFail=true
  shared.CityProgressionStore.BlocksLegacy=function()return true end
  net.Refresh(0);com.SourceChanged(0,1)
  assert(ownedGold(cities[2])==15 and view(2).sourceProvenance.DISTRICT_CAMPUS[1].status=='RETAINED')
  assert(view(2).stage=='RETAINED'and not view(2).canConfigure and not net.TransactionCurrent(0))
  cities[1].unregistered=false;cities[1].fail=false;cities[1].identityFail=false;cities[1].yields.SCIENCE=200
  net.Refresh(0);com.SourceChanged(0,1);assert(ownedGold(cities[2])==30 and view(2).sourceProvenance.DISTRICT_CAMPUS[1].status=='CONFIRMED')
  """)
 def test_never_confirmed_unadmitted_source_is_unknown_not_invented_or_none(self):
  v=commerce();v.execute("""
  cities[1].unregistered=true;cities[1].identityFail=true;cities[1].fail=true
  shared.CityProgressionStore.BlocksLegacy=function()return true end
  net.Refresh(0);assert(toggle(2,'DISTRICT_CAMPUS',true)) -- reversible choice uses its confirmed local input
  -- Unknown external contribution is not fabricated and does not become a transaction credential.
  assert(ownedGold(cities[2])==6 and view(2).sourceProvenance.DISTRICT_CAMPUS[1].status=='UNKNOWN')
  """)
 def test_explicit_legacy_exclusion_and_confirmed_identity_exit_still_remove_old_sample(self):
  for modern in (False,True):
   v=commerce();v.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));assert(ownedGold(cities[2])==15)")
   if modern:v.execute("cities[1].kind='NONE';com.SourceChanged(0,1)")
   else:v.execute("cities[1].unregistered=true;shared.CityProgressionStore.BlocksLegacy=function()return false end;com.SourceChanged(0,1)")
   v.execute("assert(ownedGold(cities[2])==6 and view(2).sourceProvenance.DISTRICT_CAMPUS[1].status=='CONFIRMED')")
 def test_changed_source_reference_cannot_keep_previous_owner_contribution(self):
  v=commerce();v.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));cities[1].token='OTHER_REFERENCE';cities[1].identityFail=true;cities[1].fail=true;send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);com.SourceChanged(0,1);assert(ownedGold(cities[2])==6 and view(2).sourceProvenance.DISTRICT_CAMPUS[1].status=='UNKNOWN')")
 def test_topology_pending_and_Standardization_whole_hold_remain(self):
  v=standard();v.execute("local n=created+removed;assert(stdValue(1)==14);net.CheckEvidence(false);studies[3]=2;std.SourceChanged(0,3);assert(stdValue(1)==14 and created+removed==n and std.records['0:1'].retained)")


class FrozenBefore(unittest.TestCase):
 def test_original_global_role_freeze_assertion_unchanged_on_B378(self):
  with baseline():old_cases.NetworkProof().test_first_unknown_role_freezes_carrier_projection()

if __name__=='__main__':unittest.main()
