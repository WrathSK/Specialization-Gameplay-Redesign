"""S8a exact validation-phase extraction; recovery/isolation is NOT yet enabled."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s7f import actual_store

BASE='b444f2c39f3ef946f07128334c9599f4f7263cc4'
@contextmanager
def history():
 path=ROOT/'Mod/CityProgressionStore.lua';text=subprocess.check_output(['git','show',BASE+':Mod/CityProgressionStore.lua'],cwd=ROOT,text=True)
 read,execute=Path.read_text,TrackedLua51.execute;digest=sha256(text.encode()).hexdigest()
 def source(p,*a,**kw):return text if p==path else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h==digest:SOURCES[h]='historical/'+BASE+'/Mod/CityProgressionStore.lua'
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

BAD={
 'templateLifecycle':"n.templateLifecycle={version=1,state='BROKEN',reconcilePending=true}",
 'researchTradition':"n.researchTradition='BROKEN'",
 'dialogue':"n.dialogueKnown=false;n.dialogue=SPCDialogueProjectModel.New()",
 'engineering':"n.engineeringKnown=true;n.engineering='BROKEN'",
 'commerce':"n.commerceKnown=true;n.commerce={version=1,owner=0,selected={'DISTRICT_CAMPUS','DISTRICT_CAMPUS'}}",
 'capital':"n.capitalKnown=true;n.capital='BROKEN'",
 'development':"n.developmentKnown=true;n.development='BROKEN'",
 'expeditionInsights':"n.expeditionInsights={version=1,records={WRONG={}}}",
 'claimTimer':"n.claimTimer={version=1,stage='ACTIVE'}"}

SETUP="""
function equal(a,b)
 if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
 for k,v in pairs(a)do if not equal(v,b[k])then return false end end
 for k in pairs(b)do if a[k]==nil then return false end end;return true
end
"""


class ValidationRegistry(unittest.TestCase):
 def test_exact_declared_fields_are_detached_and_not_automatic(self):
  c=Context();c.execute("Players=setmetatable({},{__index=function()error('NATIVE_READ_FORBIDDEN')end})");c.load('StoreSubrecords')
  expected={'templateLifecycle':['templateLifecycle'],'researchTradition':['researchTradition'],'dialogue':['dialogueKnown','dialogue'],'engineering':['engineeringKnown','engineering'],'commerce':['commerceKnown','commerce'],'capital':['capitalKnown','capital'],'development':['developmentKnown','development'],'expeditionInsights':['expeditionInsights'],'claimTimer':['claimTimer']}
  self.assertEqual(list(c.globals().SPCStoreSubrecords.Keys().values()),list(expected))
  for key,fields in expected.items():
   self.assertEqual(list(c.globals().SPCStoreSubrecords.Fields(key).values()),fields)
   c.execute("local f=SPCStoreSubrecords.Fields(...);f[1]='MUTATE'",key)
   self.assertEqual(list(c.globals().SPCStoreSubrecords.Fields(key).values()),fields)
  c.execute("assert(Events.LoadScreenClose.Count()==0 and Events.PlayerTurnActivated.Count()==0 and not pcall(SPCStoreSubrecords.Fields,'UNKNOWN')and not pcall(SPCStoreSubrecords.Validate,{},'UNKNOWN'))")
 def test_original_statements_and_phase_positions_are_preserved(self):
  original=subprocess.check_output(['git','show',BASE+':Mod/CityProgressionStore.lua'],cwd=ROOT,text=True)
  registry=(ROOT/'Mod/StoreSubrecords.lua').read_text();current=(ROOT/'Mod/CityProgressionStore.lua').read_text()
  starts=['  -- B140: missing history','  if r.researchTradition then','  if r.dialogueKnown~=nil','  if r.engineeringKnown~=nil','  if r.commerceKnown~=nil','  if r.capitalKnown~=nil','  if r.developmentKnown~=nil']
  end=original.index('  if r.ownerChanges~=nil',original.index(starts[0]))
  for i,start in enumerate(starts):
   a=original.index(start);b=original.index(starts[i+1],a)if i+1<len(starts)else end
   self.assertIn(original[a:b].rstrip(),registry)
  a=original.index('  -- B212: city-owned Expedition Insight history');b=original.index('  if r.claimTimer then',a);z=original.index('  -- Reuse the established bounded structural validator',b)
  self.assertIn(original[a:b].rstrip(),registry);self.assertIn(original[b:z].rstrip(),registry)
  self.assertLess(current.index("SPCStoreSubrecords.Validate(r,'PROFESSION',same)"),current.index('  if r.ownerChanges~=nil'))
  self.assertLess(current.index('  if r.institutionTurns~=nil'),current.index("SPCStoreSubrecords.Validate(r,'EPISODES',same)"))
 def test_nine_independent_diagnostics_do_not_repair_write_or_assert_permanent_corruption(self):
  vm=actual_store();vm.execute(SETUP)
  for key,inject in BAD.items():
   vm.execute("local n=M.Copy(T.record(a));"+inject+";local before=T.encode(n);local writes=T.writes();local reports=SPCStoreSubrecords.Check(n,equal);local failures=0;for _,v in ipairs(reports)do if v.status=='CHECK_FAILED'then failures=failures+1;assert(v.key==... and v.reason and not v.permanent)end end;assert(failures==1 and #reports==9 and T.encode(n)==before and T.writes()==writes)",key)
 def test_transient_model_exception_stays_unconfirmed_and_changes_no_record(self,expected_status="CHECK_UNKNOWN"):
  vm=actual_store();vm.execute("expectedStatus=...",expected_status);vm.execute(SETUP+"""
  local n=M.Copy(T.record(a));n.engineeringKnown=true;n.engineering=SPCEngineeringStudyModel.New()
  local original=SPCEngineeringStudyModel.Validate;local encoded=T.encode(n);local writes=T.writes()
  SPCEngineeringStudyModel.Validate=function()error(setmetatable({},{__tostring=function()error('UNREADABLE_ERROR')end}))end
  local reports=SPCStoreSubrecords.Check(n,equal);local found
  for _,v in ipairs(reports)do if v.key=='engineering'then found=v end end
  assert(found.status==expectedStatus and found.reason=='SUBRECORD_VALIDATION_UNKNOWN'and not found.permanent)
  SPCEngineeringStudyModel.Validate=original
  for _,v in ipairs(SPCStoreSubrecords.Check(n,equal))do assert(v.status=='PASS')end
  assert(T.encode(n)==encoded and T.writes()==writes)
  """)


class ActualStore(unittest.TestCase):
 def test_each_corrupt_ability_keeps_exact_existing_fail_closed_behavior_without_rewriting(self):
  results=[]
  for old in (True,False):
   rows=[]
   with history()if old else nullcontext():
    for key,inject in BAD.items():
     vm=actual_store();vm.execute("local ca,cb=a,b;local n=M.Copy(T.record(ca));"+inject+";T.propsSet(T.key(ca),n);frozen=T.encode(T.record(ca));local before=T.writes();T.reload();held=not pcall(shared.CityProgressionStore.Base,0,ca);sibling=pcall(shared.CityProgressionStore.Base,0,cb);assert(T.encode(T.record(ca))==frozen and T.writes()==before)")
     rows.append((key,vm.eval('held'),vm.eval('sibling')))
   results.append(rows)
  self.assertEqual(results[0],results[1]);self.assertTrue(all(held and sibling for _,held,sibling in results[1]))
  measure('S8a_strict_pre_isolation_differential',{'cases':9,'same_bad_city_hold':True,'valid_sibling_city_usable':True,'writes_or_repairs':0,'D7_recovery':'NOT_YET_ENABLED'})
 def test_valid_history_bytes_and_normal_ticks_match_before_extraction(self):
  results=[]
  for old in (True,False):
   with history()if old else nullcontext():vm=actual_store()
   vm.execute("""
   a=shared.InvestmentAction;local c=T.research(3);T.turn(1);T.turn(3);r=M.Copy(T.record(c))
   r.dialogueKnown=true;r.dialogue=SPCDialogueProjectModel.New()
   r.engineeringKnown=true;r.engineering=SPCEngineeringStudyModel.New()
   r.commerceKnown=true;r.commerce=SPCCommerceModel.New(0)
   r.capitalKnown=true;r.capital=SPCCapitalInvestmentModel.Encode(SPCCapitalInvestmentModel.New())
   r.developmentKnown=true;r.development=SPCDevelopmentInvestmentModel.Encode(SPCDevelopmentInvestmentModel.New())
   r.expeditionInsights={version=1,records={}};T.propsSet(T.key(c),r);T.reload()
   assert(pcall(shared.CityProgressionStore.Base,0,c));T.turn(1);encoded=T.encode(T.record(c))
   """)
   results.append({'record':vm.eval('encoded'),'writes':vm.eval('T.writes()')})
  self.assertEqual(results[0],results[1]);measure('S8a_valid_history_differential',{'same_record_bytes':True,'same_write_count':True,'age_ticks_and_saved_ability_shapes':True})
 def test_base_identity_and_reference_corruption_remain_strict(self):
  for inject in ("n.base.token='FORGED'","n.origin.x=12345","n.schema=99"):
   vm=actual_store();vm.execute("local ca,cb=a,b;local n=M.Copy(T.record(ca));"+inject+";T.propsSet(T.key(ca),n);local before=T.writes();T.reload();assert(not pcall(shared.CityProgressionStore.Base,0,ca)and pcall(shared.CityProgressionStore.Base,0,cb)and T.writes()==before)")

if __name__=='__main__':unittest.main()
