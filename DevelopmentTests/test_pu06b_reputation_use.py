"""Final read-only Store -> Commerce reputation contract, not native acceptance."""
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import subprocess,unittest
from hashlib import sha256
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s8b7b import partial,gold
BASE='a9409ef'
NATURAL="n.commerce.reputation=SPCCommerceModel.Copy(T.record(c).commerce.reputation);"
def observe(v):
 v.execute("input=s.CommerceState(0,c).reputationInput;f=shared.EffectiveFacts.Read(0,c);use=SPCCommerceModel.ReputationUse(input,f)")
 return v
@contextmanager
def before():
 paths={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ['CityProgressionStore','CommerceModel','Commerce','UI/CommercePanel']}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in paths.items()}
 def run(vm,source,*a,**kw):
  h=sha256(source.encode()if isinstance(source,str)else source).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,source,*a,**kw)
 with patch.object(Path,'read_text',lambda f,*a,**kw:paths[f]if f in paths else read(f,*a,**kw)),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

class Input(unittest.TestCase):
 def test_actual_store_severe_leaf_has_explicit_candidate_without_exporting_raw_history(self):
  v=partial();v.execute("local st=s.CommerceState(0,c);assert(st.reputationInput and st.reputationInput.status=='SEVERE_LEAF','REPUTATION_SOURCE_CLASSIFICATION_MISSING');assert(st.reputationInput.reason=='COMMERCE_REPUTATION_INVALID'and st.value.reputation==nil and not st.reputationInput.age and st.reputationKnown==false);assert(T.encode(T.record(c))==frozen and T.writes()==beforeWrites)")
 def test_confirmed_zero_is_not_absence_or_policy_zero(self):
  v=observe(partial(NATURAL));v.execute("assert(input.status=='CONFIRMED'and input.age==0 and input.state=='COUNTING');assert(use.status=='CONFIRMED'and use.effective==0 and use.age==0)")
 def test_missing_required_p4_history_is_unknown_not_invented_zero(self):
  v=observe(partial('n.commerce.reputation=nil;'));v.execute("assert(input.status=='ABSENT'and use.status=='UNKNOWN'and use.effective==nil and use.reason=='COMMERCE_REPUTATION_REQUIRED_HISTORY_MISSING');assert(T.encode(T.record(c))==frozen and T.writes()==beforeWrites)")
 def test_parent_origin_failure_is_not_severe_leaf(self):
  v=observe(partial(NATURAL+"n.commerce.reputation.receipt='MISSING_ORIGIN';"));v.execute("assert(s.Status(c).reputationIsolation.status=='CHECK_FAILED'and input.status=='UNKNOWN'and use.status=='UNKNOWN'and use.effective==nil)")
 def test_qualification_failure_is_not_severe_leaf(self):
  v=observe(partial(NATURAL+'n.commerce.reputation.qualification={};'));v.execute("assert(input.status=='UNKNOWN'and use.status=='UNKNOWN'and use.effective==nil)")
 def test_general_reader_error_is_not_policy_zero(self):
  v=partial();v.execute("local read=SPCCommerceModel.ValidateReputation;SPCCommerceModel.ValidateReputation=function(t,r)if t then error('DEPENDENCY_NOT_READY')end;return read(t,r)end;testReload();s=shared.CityProgressionStore");observe(v);v.execute("assert(s.Status(c).reputationIsolation.status=='CHECK_UNKNOWN'and input.status=='UNKNOWN'and use.status=='UNKNOWN'and use.effective==nil)")
 def test_deferred_owner_duty_precedes_leaf_policy(self):
  v=partial();v.execute("local id=c:GetID();s.RegisterExit('Fixture',function()end);T.loss(c,9,900);c.s.ref.owner=0;c.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(T.record(c).deferredLifecycle.entries.commerce.scope=='REPUTATION')");observe(v);v.execute("assert(input.status=='UNKNOWN'and input.reason=='COMMERCE_REPUTATION_DEFERRED_LIFECYCLE'and use.status=='UNKNOWN'and use.effective==nil)")
 def test_whole_bad_configuration_never_exports_reputation_input(self):
  for extra in ("n.commerce.selected='BAD';","n.commerce.owner=9;"):
   v=partial(extra);v.execute("assert(not pcall(s.CommerceState,0,c)and s.Status(c).subrecordIsolation.commerce and T.writes()==beforeWrites)")
 def test_redundant_known_flag_rebuild_is_not_a_leaf_policy(self):
  v=observe(partial('n.commerceKnown=false;'+NATURAL));v.execute("assert(T.record(c).commerceKnown==true and input.status=='CONFIRMED'and use.status=='CONFIRMED'and use.effective==0);assert(T.writes()==beforeWrites+1 and T.encode(T.record(c).commerce.reputation)==T.encode(original.commerce.reputation))")
 def test_bad_leaf_with_unknown_marker_is_not_silently_repaired(self):
  v=observe(partial('n.commerceKnown=false;'));v.execute("assert(input.status=='SEVERE_LEAF'and use.status=='POLICY_ZERO'and T.record(c).commerceKnown==false and T.encode(T.record(c))==frozen and T.writes()==beforeWrites)")
 def test_parent_and_reference_failures_are_not_leaf_policies(self):
  for change in ("n.base.token='FORGED';",'n.schema=99;'):
   v=partial(change);v.execute("assert(not pcall(s.CommerceState,0,c)and T.writes()==beforeWrites and T.encode(T.record(c))==frozen)")
  v=partial();v.execute("c.s.ref.x=c.s.ref.x+1;assert(not pcall(s.CommerceState,0,c)and T.writes()==beforeWrites)")
 def test_read_projection_is_detached_and_has_no_write_authority(self):
  v=partial(NATURAL);v.execute("local state=s.CommerceState(0,c);state.reputationInput.age=999;state.reputationInput.status='POLICY_ZERO';state.value.selected[1]='BAD';local again=s.CommerceState(0,c);assert(again.reputationInput.status=='CONFIRMED'and again.reputationInput.age==0 and again.value.selected[1]=='DISTRICT_CAMPUS'and T.writes()==beforeWrites)")

class Use(unittest.TestCase):
 def test_severe_leaf_active_iv_has_explicit_narrow_policy_and_no_history_repair(self):
  v=observe(partial());v.execute("assert(use.status=='POLICY_ZERO'and use.effective==0 and use.age==nil and use.historyStatus=='SEVERE_LEAF');assert(T.encode(T.record(c))==frozen and T.writes()==beforeWrites and s.Status(c).reputationIsolation)")
 def test_current_non_iv_is_not_applicable_even_if_history_unknown(self):
  v=observe(partial(level=3));v.execute("assert(f.active==3 and use.status=='NOT_APPLICABLE'and use.effective==0 and use.age==nil and input.status=='SEVERE_LEAF')")
 def test_current_qualification_unknown_cannot_use_leaf_policy(self):
  v=partial();v.execute("local st=s.CommerceState(0,c);local use=SPCCommerceModel.ReputationUse(st.reputationInput,{specialization='COMMERCE',activeStatus='UNKNOWN',potential=4});assert(use.status=='UNKNOWN'and use.effective==nil)")
 def test_confirmed_ages_zero_to_forty_keep_exact_values(self):
  v=partial(NATURAL);v.execute("for age=0,40 do local input={status='CONFIRMED',age=age,state='COUNTING'};local use=SPCCommerceModel.ReputationUse(input,{specialization='COMMERCE',activeStatus='KNOWN',active=4,potential=4});assert(use.status=='CONFIRMED'and use.effective==age and use.age==age)end")
 def test_noncounting_saved_state_cannot_supply_current_r(self):
  v=partial(NATURAL);v.execute("for _,state in ipairs({'DORMANT_OWNER','UNKNOWN_INTERVAL'})do local use=SPCCommerceModel.ReputationUse({status='CONFIRMED',age=20,state=state},{specialization='COMMERCE',activeStatus='KNOWN',active=4,potential=4});assert(use.status=='UNKNOWN'and use.effective==nil)end")
 def test_malformed_or_missing_use_input_is_unknown(self):
  v=partial(NATURAL);v.execute("local f={specialization='COMMERCE',activeStatus='KNOWN',active=4,potential=4};for _,input in ipairs({false,{status='CONFIRMED',age=41,state='COUNTING'},{status='CONFIRMED',age=-1,state='COUNTING'},{status='SEVERE_LEAF',reason='UNKNOWN_DEPENDENCY'},{status='POLICY_ZERO',effective=0}})do local use=SPCCommerceModel.ReputationUse(input,f);assert(use.status=='UNKNOWN'and use.effective==nil)end;assert(SPCCommerceModel.ReputationUse(nil,f).status=='UNKNOWN')")
 def test_invalid_active_and_potential_do_not_prove_applicability(self):
  v=partial();v.execute("local input=s.CommerceState(0,c).reputationInput;for _,f in ipairs({{specialization='COMMERCE',activeStatus='KNOWN',active=4,potential=3},{specialization='COMMERCE',activeStatus='KNOWN',active=5,potential=5},{specialization='COMMERCE',activeStatus='KNOWN',active=0,potential=-1},{activeStatus='KNOWN',active=0,potential=0}})do local u=SPCCommerceModel.ReputationUse(input,f);assert(u.status=='UNKNOWN'and u.effective==nil)end")
 def test_known_noncommerce_has_no_reputation_bonus(self):
  v=partial();v.execute("local u=SPCCommerceModel.ReputationUse(nil,{specialization='RESEARCH',activeStatus='KNOWN',active=4,potential=4});assert(u.status=='NOT_APPLICABLE'and u.effective==0)")

class RealCommerce(unittest.TestCase):
 def test_severe_leaf_keeps_legal_gold_and_labels_policy_zero(self):
  v=gold();v.execute("local v=com.views['0:'..source:GetID()];assert(v.stage=='READY'and gold()==15 and v.reputationUse and v.reputationUse.status=='POLICY_ZERO','COMMERCE_REPUTATION_PROVENANCE_MISSING');assert(v.reputationKnown==false and v.reputation.age==nil and v.reputation.effective==0);assert(v.reputationMessage:find('原记录未改写',1,true)and com.Describe(0,source):find('R=0',1,true));assert(T.encode(T.record(source).commerce.reputation)==rawHistory and T.writes()==beforeWrites)")
 def test_unknown_reader_keeps_independent_gold_but_not_policy_zero(self):
  v=gold();v.execute("local read=SPCCommerceModel.ValidateReputation;SPCCommerceModel.ValidateReputation=function(t,r)if t then error('DEPENDENCY_NOT_READY')end;return read(t,r)end;auditCommerce();local v=com.views['0:'..source:GetID()];assert(v.stage=='READY'and gold()==15 and v.reputationUse.status=='UNKNOWN'and v.reputationUse.effective==nil and v.reputation.effective==0);assert(v.reputationMessage:find('暂不可确认',1,true));assert(T.encode(T.record(source).commerce.reputation)==rawHistory)")
 def test_cold_missing_network_keeps_installed_total_without_usable_policy_credential(self):
  v=gold(cold=True);v.execute("local v=com.views['0:'..source:GetID()];assert(v.stage=='HELD'and gold()==16 and v.appliedRetained and not v.canConfigure);assert(v.reputationUse and v.reputationUse.status=='UNKNOWN','PENDING_PURPOSE_EXPORTED_POLICY_ZERO');assert(T.encode(T.record(source).commerce.reputation)==rawHistory and T.writes()==beforeWrites)")
 def test_configuration_off_on_preserves_opaque_history(self):
  v=gold();v.execute("local id=source:GetID();local v=com.views['0:'..id];assert(com.Request(0,{Action='COMMERCE_SELECT',CityID=id,Domain='DISTRICT_CAMPUS',Enabled=false,Reference=v.reference,CityToken=v.token,Revision=v.revision,Token='OFF_POLICY'}));auditCommerce();assert(gold()==0);v=com.views['0:'..id];assert(com.Request(0,{Action='COMMERCE_SELECT',CityID=id,Domain='DISTRICT_CAMPUS',Enabled=true,Reference=v.reference,CityToken=v.token,Revision=v.revision,Token='ON_POLICY'}));auditCommerce();assert(gold()==15 and T.encode(T.record(source).commerce.reputation)==rawHistory)")
 def test_idle_has_no_new_reads_writes_or_notifications(self):
  v=gold();v.execute("local read=SPCCommerceModel.ReputationInput;inputReads=0;SPCCommerceModel.ReputationInput=function(...)inputReads=inputReads+1;return read(...)end;local writes=com.writes;local revision=com.views['0:'..source:GetID()].revision;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(inputReads==0 and com.writes==writes and com.views['0:'..source:GetID()].revision==revision and T.writes()==beforeWrites)")
 def test_restricted_lua_projection_uses_no_raw_or_debug_helpers(self):
  v=partial();v.execute('debug=nil;rawget=nil;rawset=nil;rawequal=nil;collectgarbage=nil;os=nil;io=nil;package=nil');observe(v);v.execute("assert(use.status=='POLICY_ZERO'and T.writes()==beforeWrites)")

class Differential(unittest.TestCase):
 def test_healthy_actual_gold_and_age_match_fixed_source(self):
  from test_refactor_s6f import combined
  from contextlib import nullcontext
  rows=[]
  for old in (True,False):
   with before()if old else nullcontext():
    v=combined();v.execute("result={};for age=0,40 do if age>0 then T.turn(1);auditCommerce()end;local view=com.views['0:'..source:GetID()];result[#result+1]=tostring(gold())..':'..view.reputation.age..':'..view.reputation.effective end;business=T.encode(result)");rows.append(v.eval('business'))
  self.assertEqual(rows[0],rows[1]);measure('PU06b_confirmed_gold',{'age_samples':41,'same_as_fixed_baseline':True})

class Presentation(unittest.TestCase):
 def test_actual_sidebar_displays_copied_backend_explanation_without_a_request(self):
  import test_b261_commerce as sidebar
  with patch.object(sidebar,'LuaRuntime',TrackedLua51),legacy_source_observation():v=sidebar.ui()
  v.execute("local sentBefore=#sent;view.reputationMessage='商业信誉记录异常；本次按无信誉加成政策计价（R=0），原记录未改写。';notify();assert(Controls.Reputation.text==view.reputationMessage and #sent==sentBefore);view.reputationMessage='商业信誉暂不可确认；不据此新增信誉加成。';notify();assert(Controls.Reputation.text==view.reputationMessage and #sent==sentBefore)")

if __name__=='__main__':unittest.main()
