"""R06/R07: scoped validation uncertainty and existing owner-epoch recovery."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,measure
from test_refactor_s8b2 import fixture,isolated,BAD
from test_refactor_s9b1 import runtime as development
import test_refactor_s8a as validation


@contextmanager
def baseline(*names):
 rows={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','f8f5914:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in names}
 read,execute=Path.read_text,TrackedLua51.execute;hashes={sha256(s.encode()).hexdigest():'historical/f8f5914/'+str(p.relative_to(ROOT))for p,s in rows.items()}
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',lambda p,*a,**kw:rows[p]if p in rows else read(p,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield


class Classifications(unittest.TestCase):
 def test_only_declared_record_assertions_are_CHECK_FAILED(self):
  v=fixture();v.execute("local n=seed();n.expeditionInsights="+BAD+";local c=SPCStoreSubrecords.CheckOne('expeditionInsights',n,M.Same);assert(c.status=='CHECK_FAILED'and not c.permanent);local original=SPCDevelopmentInvestmentModel.Decode;for _,why in ipairs({'TEMPORARY_READER_UNAVAILABLE','DEVELOPMENT_DEPENDENCY_UNAVAILABLE','CAPITAL_HISTORY_INVALID'})do SPCDevelopmentInvestmentModel.Decode=function()error(why)end;local c=SPCStoreSubrecords.CheckOne('development',n,M.Same);assert(c.status=='CHECK_UNKNOWN'and not c.permanent)end;SPCDevelopmentInvestmentModel.Decode=original")
 def test_unprintable_unknown_keeps_original_assertion_on_B381(self):
  with baseline('StoreSubrecords'):validation.ValidationRegistry().test_transient_model_exception_stays_unconfirmed_and_changes_no_record(expected_status='CHECK_FAILED')
 def test_unavailable_decoder_is_scoped_unknown_not_permanent_or_reset(self):
  v=fixture();v.execute("local n=seed();frozen=install(n);local decode=SPCDevelopmentInvestmentModel.Decode;SPCDevelopmentInvestmentModel.Decode=function()error('DEVELOPMENT_DEPENDENCY_UNAVAILABLE')end;testReload();local s=shared.CityProgressionStore;assert(pcall(s.Base,0,ca)and pcall(s.CapitalState,0,ca)and not pcall(s.DevelopmentState,0,ca));assert(s.Status(ca).subrecordIsolation.development.status=='CHECK_UNKNOWN'and T.encode(T.record(ca))==frozen and T.writes()==beforeWrites);SPCDevelopmentInvestmentModel.Decode=decode;testReload();assert(pcall(shared.CityProgressionStore.DevelopmentState,0,ca)and T.writes()==beforeWrites)")
 def test_missing_validator_and_runtime_type_failure_do_not_claim_bad_record(self):
  v=fixture();v.execute("local n=seed();local validate=SPCEngineeringStudyModel.Validate;SPCEngineeringStudyModel.Validate=nil;assert(SPCStoreSubrecords.CheckOne('engineering',n,M.Same).status=='CHECK_UNKNOWN');SPCEngineeringStudyModel.Validate=function()local x=nil;return x.missing end;assert(SPCStoreSubrecords.CheckOne('engineering',n,M.Same).status=='CHECK_UNKNOWN');SPCEngineeringStudyModel.Validate=validate")
 def test_declared_codes_really_exist_and_other_owner_codes_are_unknown(self):
  s=(ROOT/'Mod/StoreSubrecords.lua').read_text();body=s.split('local validationCodes={',1)[1].split('\n}',1)[0]
  import re
  rows=re.findall(r" (\w+)='([^']*)'",body);self.assertEqual(len(rows),9)
  sources='\n'.join((ROOT/'Mod'/p).read_text()for p in ['StoreSubrecords.lua','ResearchTradition.lua','DialogueProjectModel.lua','EngineeringStudyModel.lua','CapitalInvestmentModel.lua','DevelopmentInvestmentModel.lua','CommerceModel.lua','RestructuringModel.lua','CityIdentityRead.lua'])
  # Declared literals must also be owned by a validator outside this registry.
  sources=sources.replace(body,'')
  for _,words in rows:
   for word in words.split():self.assertTrue("'"+word+"'"in sources,word)


class Recovery(unittest.TestCase):
 def test_actual_valid_transient_loss_return_reload_closes_old_Development(self):
  v=development();v.execute("""
  assert(sign()and contract().stage=='ACTIVE'and active());local bytes=T.encode(T.record(source).development);local oldID=source:GetID();local decode=SPCDevelopmentInvestmentModel.Decode
  SPCDevelopmentInvestmentModel.Decode=function()error('TRANSIENT_MODEL_UNAVAILABLE')end
  reload();assert(shared.CityProgressionStore.Status(source).subrecordIsolation.development.status=='CHECK_UNKNOWN'and pcall(shared.CityProgressionStore.Base,0,source));assert(T.encode(T.record(source).development)==bytes)
  local info=P.Info;P.Info=function(kind,id)local r=info(kind,id);if kind=='Buildings'and id=='BUILDING_SPC_CAPITAL_ACCESS'then r.InternalOnly=1 end;return r end
  T.loss(source,9,900);assert(T.record(source).stage=='HELD_TRANSFER'and T.encode(T.record(source).development)==bytes)
  source.s.ref.owner=0;source.s.ref.cityID=oldID;Events.CityTransfered.Fire(0,oldID,9);assert(T.record(source).stage=='ACTIVE'and T.record(source).ownerChanges==1 and T.encode(T.record(source).development)==bytes)
  SPCDevelopmentInvestmentModel.Decode=decode;local m=moneyCalls;reload();assert(contract().stage=='TERMINATED'and contract().reason=='DEVELOPMENT_OWNER_CHANGED'and not active()and moneyCalls==m)
  local w=T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(T.writes()==w and moneyCalls==m)
  """)
  measure('S9e9_Development_opaque_lifecycle',{'actual_Store':True,'scenario':'valid -> transient decoder -> loss -> return -> cold reload -> owner-epoch reconcile','old_contract':'TERMINATED','native_payments_replayed':0,'new_persistent_fields':0,'extra_source_reference_samples':0})
 def test_current_source_epoch_is_compared_to_saved_contract_not_fresh_index(self):
  for old in (True,False):
   with baseline('DevelopmentInvestment')if old else nullcontext():v=development()
   v.execute("assert(sign());local key=T.key(source);local saved=M.Copy(T.record(source));saved.ownerChanges=(saved.ownerChanges or 0)+1;T.propsSet(key,saved);reload()")
   self.assertEqual(v.eval('contract().stage'),'ACTIVE'if old else'TERMINATED')
 def test_unknown_current_reference_never_terminates_or_replays(self):
  v=development();v.execute("assert(sign());local ref=shared.CityProgressionStore.CapitalReference;local old=T.encode(value());local encoded=T.encode(T.record(source).development);shared.CityProgressionStore.CapitalReference=function()error('REFERENCE_UNAVAILABLE')end;local w=T.writes();dev.Reconcile(0);assert(T.encode(T.record(source).development)==encoded and T.writes()==w and moneyCalls==1);shared.CityProgressionStore.CapitalReference=ref;dev.Reconcile(0);assert(T.encode(value())==old and contract().stage=='ACTIVE')")


class Reports(unittest.TestCase):
 def test_protected_and_partial_groups_are_read_only_and_not_permanent(self):
  v=isolated();v.execute("local n=T.writes();local s=shared.CityProgressionStore.Describe(0,ca);assert(s:find('记录不可用（已保护）',1,true)and s:find('考察见闻',1,true)and not s:find('永久损坏',1,true));for i=1,20 do shared.CityProgressionStore.Describe(0,ca)end;assert(T.writes()==n)")
 def test_unknown_labels_and_independent_known_marker_repair_share_one_report(self):
  v=fixture();v.execute("local n=seed();n.dialogueKnown=false;install(n);local decode=SPCDevelopmentInvestmentModel.Decode;SPCDevelopmentInvestmentModel.Decode=function()error('TEMPORARY_UNAVAILABLE')end;testReload();local s=shared.CityProgressionStore.Describe(0,ca);assert(s:find('发展投资（暂时无法验证）',1,true)and s:find('已验证修复',1,true)and s:find('时代对话',1,true));local w=T.writes();shared.CityProgressionStore.Describe(0,ca);assert(T.writes()==w);SPCDevelopmentInvestmentModel.Decode=decode")
 def test_healthy_unchanged_report_and_no_extra_native_reads(self):
  v=fixture();v.execute('local n=seed();install(n);testReload();text=shared.CityProgressionStore.Describe(0,ca);assert(not text:find("记录不可用",1,true)and not text:find("已验证修复",1,true))')

def load_tests(loader,standard,pattern):
 # S9b1 already inherits the maintained S9a2/Store profiles. Execute each exact
 # class/method once; do not rerun inherited measurements through a second path.
 suite=unittest.TestSuite();seen={}
 def visit(node):
  if isinstance(node,unittest.TestSuite):
   for item in node:visit(item)
  else:
   key=node.id()
   if key in seen:assert type(seen[key])is type(node),'CONFLICTING_TEST_PROFILE'
   else:seen[key]=node;suite.addTest(node)
 for node in (standard,loader.loadTestsFromName('test_refactor_s9e7'),loader.loadTestsFromName('test_refactor_s9b1')):visit(node)
 return suite

if __name__=='__main__':unittest.main()
