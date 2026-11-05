"""PU06 final Capital modes/locked sources; explicit native doubles, no game claim."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import subprocess,unittest,struct
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s7d5 import profile
from test_b241_capital import runtime as raw_capital
BASE='c711059'
CONFIRMED="{status='CONFIRMED',reason='COMMERCE_REPUTATION_CONFIRMED',historyStatus='CONFIRMED',age=20,effective=20}"
@contextmanager
def before():
 paths={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ['CapitalInvestment','CapitalInvestmentModel','UI/CapitalInvestmentPanel']}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in paths.items()}
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',lambda f,*a,**kw:paths[f]if f in paths else read(f,*a,**kw)),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

def capital():
 with profile():v=raw_capital()
 v.execute("""
 function openQuote()return cap.Request(0,{Action='CAPITAL_OPEN',CityID=source:GetID(),Token='OPEN'})end
 function sign(mode,domain,token)local view=C.view();return cap.Request(0,{Action='CAPITAL_CONFIRM',CityID=source:GetID(),Domain=domain or 'DISTRICT_CAMPUS',Mode=mode or 'STABLE',Token=token or 'SIGN',Revision=view.revision,CityToken=view.token})end
 function first()return C.view().domains[1]end
 function clamp()shared.Commerce.views['0:'..source:GetID()].reputation={effective=0}end
 """);return v

def alter(v,code):
 v.execute("local n=M.Copy(T.record(source));"+code+";T.propsSet(T.key(source),n);local dc,net=shared.DistrictCompleteness,shared.NetworkBridge;C.reload();shared.DistrictCompleteness=dc;shared.NetworkBridge=net;clamp()")
 return v

def pure():
 v=TrackedLua51(unpack_returned_tuples=True)
 with legacy_source_observation():
  v.globals().include=lambda n:v.execute((ROOT/'Mod'/(n+'.lua')).read_text());v.globals().include('CapitalInvestmentModel')
 v.execute("M=SPCCapitalInvestmentModel;ref={owner=0,cityID=1,x=1,y=1,token='PURE',changes=0};function quote(use)return M.Quote{domain='DISTRICT_CAMPUS',source=ref,turn=0,D=3,reputationUse=use,balance=1000,failureCount=0}end")
 return v

class Sources(unittest.TestCase):
 def test_unsafe_r_cannot_become_a_new_venture_via_passive_numeric_zero(self):
  v=alter(capital(),"n.commerce.reputation.receipt='MISSING_ORIGIN'");v.execute("assert(openQuote());local before=balance;assert(not sign('VENTURE'),'UNSAFE_R_SIGNED_AS_ZERO');assert(moneyCalls==0 and rolls==0 and balance==before)")
 def test_fresh_store_source_replaces_stale_passive_display_value(self):
  v=capital();v.execute("assert(shared.Commerce.views['0:'..source:GetID()].reputation.effective==20);assert(openQuote());assert(first().quote.R==0,'PASSIVE_R_CLAMP_USED_AS_PROOF');assert(first().quote.reputationUse.status=='CONFIRMED'and first().modes.VENTURE.canSign)")
 def test_severe_leaf_policy_zero_signs_without_repairing_history(self):
  v=alter(capital(),'n.commerce.reputation.age=99');v.execute("local raw=T.encode(T.record(source).commerce.reputation);assert(openQuote()and first().modes.VENTURE.canSign);assert(first().quote.reputationUse.status=='POLICY_ZERO');assert(sign('VENTURE'));local c=C.contract();assert(c.R==0 and c.reputationSource.status=='POLICY_ZERO'and c.reputationSource.historyStatus=='SEVERE_LEAF');assert(T.encode(T.record(source).commerce.reputation)==raw and moneyCalls==1 and rolls==1)")
 def test_missing_required_history_blocks_risk_but_not_stable(self):
  v=alter(capital(),'n.commerce.reputation=nil');v.execute("assert(openQuote());assert(first().modes.STABLE.canSign and not first().modes.VENTURE.canSign and first().quote.failure==nil and first().quote.expected==nil and first().quote.R==nil);assert(sign('STABLE')and moneyCalls==1 and rolls==0)")
 def test_general_read_failure_does_not_block_independent_stable_confirmation(self):
  v=capital();v.execute("local read=shared.CityProgressionStore.CommerceState;Rreads=0;shared.CityProgressionStore.CommerceState=function(...)Rreads=Rreads+1;error('TEMPORARY_REPUTATION_READER')end;assert(openQuote()and Rreads==1);assert(first().modes.STABLE.canSign and not first().modes.VENTURE.canSign);Rreads=0;onMoney=function()assert(Rreads==0,'R_READ_BEFORE_STABLE_DEBIT')end;assert(sign('STABLE'),'STABLE_DEPENDS_ON_UNUSED_R');assert(Rreads==1 and moneyCalls==1 and rolls==0)")
 def test_non_iv_does_not_read_irrelevant_reputation_and_locks_not_applicable(self):
  v=capital();v.execute("T.governor(3);shared.CityProgressionStore.CommerceState=function()error('UNUSED_R')end;assert(openQuote()and first().modes.VENTURE.canSign and first().quote.R==0);assert(sign('VENTURE'));assert(C.contract().reputationSource.status=='NOT_APPLICABLE'and C.contract().reputationSource.reason=='COMMERCE_REPUTATION_ACTIVE_IV_REQUIRED')")
 def test_parent_and_reference_failure_cannot_use_policy_zero(self):
  for change in ("n.base.token='FORGED'","n.schema=99"):
   v=alter(capital(),change);v.execute("openQuote();assert(C.view().stage=='HELD'and not C.view().canSign);assert(not sign('VENTURE')and moneyCalls==0 and rolls==0)")
  v=capital();v.execute("source.s.ref.x=source.s.ref.x+1;openQuote();assert(not sign('VENTURE')and moneyCalls==0 and rolls==0)")
 def test_deferred_reputation_is_not_policy_zero(self):
  v=alter(capital(),'n.commerce.reputation.age=99');v.execute("local info=P.Info;P.Info=function(tab,id)local row=info(tab,id);if tab=='Buildings'and id=='BUILDING_SPC_CAPITAL_ACCESS'and row then local copy=SPCCapitalInvestmentModel.Copy(row);copy.InternalOnly=1;return copy end;return row end;local id=source:GetID();local store=shared.CityProgressionStore;store.RegisterExit('Fixture',function()end);T.loss(source,9,900);source.s.ref.owner=0;source.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);clamp();assert(openQuote());assert(first().modes.STABLE.canSign and not first().modes.VENTURE.canSign);assert(not sign('VENTURE')and moneyCalls==0 and rolls==0)")
 def test_strict_common_network_and_balance_guards_remain(self):
  v=alter(capital(),'n.commerce.reputation.age=99');v.execute("shared.Commerce.TransactionCurrent=function()return false end;openQuote();assert(not sign('STABLE')and not sign('VENTURE')and moneyCalls==0 and rolls==0)")
  v=capital();v.execute("assert(openQuote());balance=balance+1;assert(not sign('VENTURE')and moneyCalls==0 and rolls==0)")
 def test_unknown_capital_never_becomes_fresh_via_policy_zero(self):
  v=alter(capital(),"n.commerce.reputation.age=99;n.capitalKnown=true;n.capital='UNKNOWN_PAYMENT'");v.execute("local raw=T.encode(T.record(source).capital);openQuote();assert(C.view().stage=='HELD'and not C.view().canSign and not sign('VENTURE')and moneyCalls==0 and rolls==0);assert(T.encode(T.record(source).capital)==raw)")

class Terms(unittest.TestCase):
 def test_unknown_quote_has_stable_terms_but_no_invented_risk_return(self):
  v=pure();v.execute("local q=quote({status='UNKNOWN',reason='MISSING'});assert(not q.ventureAvailable and q.R==nil and q.failure==nil and q.expected==nil and q.net==nil);local s=M.Terms(q,'STABLE');assert(s and s.R==0 and s.reputationSource.reason=='STABLE_REPUTATION_NOT_REQUIRED');local r,why=M.Terms(q,'VENTURE');assert(r==nil and why=='CAPITAL_REPUTATION_UNKNOWN')")
 def test_numeric_r_is_not_a_compatibility_credential(self):
  v=pure();v.execute("assert(not pcall(M.Quote,{domain='DISTRICT_CAMPUS',source=ref,turn=0,D=3,R=0,balance=1000,failureCount=0}))")
 def test_stable_terms_ignore_changes_in_r_value_and_knownness(self):
  v=pure();v.execute("local known=quote("+CONFIRMED+");local unknown=quote({status='UNKNOWN',reason='MISSING'});assert(M.Same(M.Terms(known,'STABLE'),M.Terms(unknown,'STABLE')));assert(M.Terms(known,'VENTURE')and not M.Terms(unknown,'VENTURE'))")
 def test_malformed_provenance_never_admits_venture(self):
  v=pure();v.execute("for _,u in ipairs({{status='CONFIRMED',reason='COMMERCE_REPUTATION_CONFIRMED',historyStatus='CONFIRMED',effective=20,age=19},{status='POLICY_ZERO',reason='COMMERCE_REPUTATION_ISOLATED_LEAF_POLICY',historyStatus='UNKNOWN',effective=0},{status='NOT_APPLICABLE',reason='STABLE_REPUTATION_NOT_REQUIRED',historyStatus='NOT_REQUIRED',effective=0},{status='CONFIRMED',reason='COMMERCE_REPUTATION_CONFIRMED',historyStatus='CONFIRMED',effective=0,age=0,extra=true}})do local q=quote(u);assert(not q.ventureAvailable and M.Terms(q,'STABLE')and not M.Terms(q,'VENTURE'))end")
 def test_base_quote_cannot_bypass_mode_specific_terms(self):
  v=pure();v.execute("local q=quote("+CONFIRMED+");assert(not pcall(M.Begin,M.New(),q,'VENTURE',0,'NO_TERMS'));local s=M.Terms(q,'STABLE');assert(not pcall(M.Begin,M.New(),s,'VENTURE',0,'WRONG_MODE'))")
 def test_locked_source_is_copied_and_required_after_codec(self):
  v=pure();v.execute("local q=quote("+CONFIRMED+");local t=M.Terms(q,'VENTURE');local n=M.Begin(M.New(),t,'VENTURE',0,'LOCK');t.reputationSource.effective=0;q.reputationUse.age=0;assert(n.contracts.DISTRICT_CAMPUS.R==20 and n.contracts.DISTRICT_CAMPUS.reputationSource.age==20);local decoded=M.Decode(M.Encode(n));assert(M.Same(n,decoded));decoded.contracts.DISTRICT_CAMPUS.reputationSource.age=0;assert(not pcall(M.Validate,decoded))")
 def test_old_v2_is_rejected_without_migration_or_reset(self):
  v=pure();v.execute("assert(M.New().version==3);local n=M.New();n.version=2;assert(not pcall(M.Validate,n));local encoded=M.Encode(M.New());encoded.version=2;assert(not pcall(M.Decode,encoded))")
 def test_all_allowed_zero_origins_remain_distinct(self):
  v=pure();v.execute("local cases={{status='CONFIRMED',reason='COMMERCE_REPUTATION_CONFIRMED',historyStatus='CONFIRMED',age=0,effective=0},{status='NOT_APPLICABLE',reason='COMMERCE_REPUTATION_ACTIVE_IV_REQUIRED',historyStatus='ABSENT',effective=0},{status='POLICY_ZERO',reason='COMMERCE_REPUTATION_ISOLATED_LEAF_POLICY',historyStatus='SEVERE_LEAF',effective=0}};local previous;for i,u in ipairs(cases)do local n=M.Begin(M.New(),assert(M.Terms(quote(u),'VENTURE')),'VENTURE',0,'CASE'..i);local c=n.contracts.DISTRICT_CAMPUS;assert(c.R==0 and c.reputationSource.status==u.status);if previous then assert(not M.Same(previous,c.reputationSource))end;previous=c.reputationSource end")

class Confirmation(unittest.TestCase):
 def test_stable_confirmation_skips_reader_after_knownness_changes(self):
  v=capital();v.execute("assert(openQuote());shared.CityProgressionStore.CommerceState=function()error('BECAME_UNREADABLE')end;assert(sign('STABLE')and moneyCalls==1 and rolls==0)")
 def test_risk_revalidates_source_and_stops_before_roll_or_money(self):
  v=capital();v.execute("assert(openQuote());shared.CityProgressionStore.CommerceState=function()error('BECAME_UNREADABLE')end;assert(not sign('VENTURE')and moneyCalls==0 and rolls==0)")
 def test_changed_r_is_stale_for_risk_but_not_for_stable(self):
  for mode in ('VENTURE','STABLE'):
   v=capital();v.execute("assert(openQuote());local read=shared.CityProgressionStore.CommerceState;shared.CityProgressionStore.CommerceState=function(...)local x=read(...);x.reputationInput={status='CONFIRMED',age=20,state='COUNTING',reason='COMMERCE_REPUTATION_CONFIRMED'};return x end;local ok=sign('"+mode+"');assert("+('not ok and moneyCalls==0 and rolls==0'if mode=='VENTURE'else'ok and moneyCalls==1 and rolls==0')+")")
 def test_same_r_value_changed_provenance_is_stale_for_risk(self):
  v=capital();v.execute("assert(openQuote()and first().quote.R==0);local read=shared.CityProgressionStore.CommerceState;shared.CityProgressionStore.CommerceState=function(...)local x=read(...);x.reputationInput={status='SEVERE_LEAF',reason='COMMERCE_REPUTATION_INVALID'};return x end;assert(not sign('VENTURE')and moneyCalls==0 and rolls==0)")
 def test_signed_terms_survive_reputation_loss_reload_and_maturity(self):
  v=capital();v.execute("assert(openQuote()and sign('VENTURE'));locked=T.encode(C.contract());Rbefore=rolls;calls=moneyCalls;T.governor(1);C.reload();assert(T.encode(C.contract())==locked and moneyCalls==calls and rolls==Rbefore);T.turn(10);local c=C.contract();assert(c.stage=='SETTLED'and c.reputationSource.status=='CONFIRMED'and moneyCalls==calls+1 and rolls==Rbefore);local paid=c.paid;T.turn(1);assert(C.contract().paid==paid and moneyCalls==calls+1)")
 def test_signed_policy_source_survives_load_and_is_never_repriced(self):
  v=alter(capital(),'n.commerce.reputation.age=99');v.execute("assert(openQuote()and sign('VENTURE'));locked=T.encode(C.contract());calls=moneyCalls;Rbefore=rolls;C.reload();assert(T.encode(C.contract())==locked and moneyCalls==calls and rolls==Rbefore);T.turn(10);assert(C.contract().stage=='SETTLED'and C.contract().reputationSource.status=='POLICY_ZERO'and C.contract().R==0 and moneyCalls==calls+1 and rolls==Rbefore)")
 def test_debit_failures_never_retry_or_turn_into_r_policy_recovery(self):
  for failure in ('BEFORE','AFTER','IGNORE'):
   v=capital();v.execute("assert(openQuote());moneyFail='"+failure+"';assert(not sign('VENTURE'));local calls=moneyCalls;assert(calls==1);moneyFail=nil;C.reload();openQuote();assert(not sign('VENTURE','DISTRICT_THEATER','SECOND'));T.turn(10);assert(moneyCalls==calls)")
 def test_credit_calling_failures_never_retry_or_refund(self):
  for failure in ('BEFORE','AFTER','IGNORE'):
   v=capital();v.execute("assert(openQuote()and sign('STABLE'));moneyFail='"+failure+"';T.turn(10);local calls=moneyCalls;assert(calls==2);moneyFail=nil;C.reload();T.turn(1);assert(moneyCalls==calls and C.contract().stage=='HELD')")
 def test_duplicate_and_native_reentry_do_not_repeat_roll_or_debit(self):
  v=capital();v.execute("assert(openQuote());onMoney=function()assert(not sign('VENTURE'))end;assert(sign('VENTURE'));assert(moneyCalls==1 and rolls==1);assert(not sign('VENTURE')and moneyCalls==1 and rolls==1)")
 def test_automatic_stale_refresh_has_zero_reputation_reads(self):
  v=capital();v.execute("local read=shared.CityProgressionStore.CommerceState;Rreads=0;shared.CityProgressionStore.CommerceState=function(...)Rreads=Rreads+1;return read(...)end;cap.Refresh(0,source:GetID(),false);assert(Rreads==0 and C.view().quoteStale);assert(openQuote()and Rreads==1);Rreads=0;onMoney=function()assert(Rreads==0,'R_READ_BEFORE_STABLE_DEBIT')end;assert(sign('STABLE')and Rreads==1)")
 def test_bad_old_contract_does_not_become_an_empty_slot(self):
  v=capital();v.execute("assert(openQuote()and sign('STABLE'));local n=M.Copy(T.record(source));n.capital.version=2;old=T.encode(n.capital);T.propsSet(T.key(source),n);C.reload();openQuote();assert(C.view().stage=='HELD'and not sign('VENTURE','DISTRICT_THEATER')and moneyCalls==1 and T.encode(T.record(source).capital)==old)")


def sidebar(factory=None):
 import test_b261_commerce as base
 import test_b262_capital_sidebar as old
 execute=TrackedLua51.execute
 def run(vm,source,*a,**kw):
  value=execute(vm,source,*a,**kw)
  if isinstance(source,str)and 'function pick(i,mode)'in source and 'capitalView={'in source:
   execute(vm,"for _,row in ipairs(capitalView.domains)do row.modes={STABLE={canSign=true,reason='CAPITAL_READY'},VENTURE={canSign=true,reason='CAPITAL_READY'}};row.quote.kind='CAPITAL_QUOTE_V1';row.quote.R=0;row.quote.reputationUse={status='CONFIRMED',reason='COMMERCE_REPUTATION_CONFIRMED',historyStatus='CONFIRMED',age=0,effective=0}end")
  return value
 with patch.object(base,'LuaRuntime',TrackedLua51),patch.object(TrackedLua51,'execute',run),legacy_source_observation():return (factory or old.ui)()

class AllOwners(unittest.TestCase):
 def test_true_store_commerce_capital_uses_policy_source_not_passive_zero(self):
  from test_refactor_s8b7b import gold
  v=gold();v.execute("shared.NetworkBridge.CurrentCapitalSources=function(pid,c,kind)return kind=='RESEARCH'and {research:GetID()}or{}end;SPCCapitalInvestment.Start(P,shared);cap=shared.CapitalInvestment;local id=source:GetID();assert(com.TransactionCurrent(0,id));assert(cap.Request(0,{Action='CAPITAL_OPEN',CityID=id,Token='ALL_OPEN'}));local view=cap.views['0:'..id];assert(view.domains[1].quote.reputationUse.status=='POLICY_ZERO');assert(cap.Request(0,{Action='CAPITAL_CONFIRM',CityID=id,Domain='DISTRICT_CAMPUS',Mode='VENTURE',Token='ALL_SIGN',Revision=view.revision,CityToken=view.token}));local contract=shared.CityProgressionStore.CapitalState(0,source).value.contracts.DISTRICT_CAMPUS;assert(contract.reputationSource.status=='POLICY_ZERO'and contract.R==0 and moneyCalls==1 and rolls==1 and T.encode(T.record(source).commerce.reputation)==rawHistory)")
 def test_true_passive_unknown_preserves_gold_but_risk_stops_before_native(self):
  from test_refactor_s8b7b import gold
  v=gold();v.execute("local read=SPCCommerceModel.ValidateReputation;SPCCommerceModel.ValidateReputation=function(t,r)if t then error('DEPENDENCY_NOT_READY')end;return read(t,r)end;auditCommerce();assert(gold()==15 and com.views['0:'..source:GetID()].reputationUse.status=='UNKNOWN');shared.NetworkBridge.CurrentCapitalSources=function(pid,c,kind)return kind=='RESEARCH'and {research:GetID()}or{}end;SPCCapitalInvestment.Start(P,shared);cap=shared.CapitalInvestment;local id=source:GetID();assert(cap.Request(0,{Action='CAPITAL_OPEN',CityID=id,Token='ALL_OPEN'}));local view=cap.views['0:'..id];assert(not cap.Request(0,{Action='CAPITAL_CONFIRM',CityID=id,Domain='DISTRICT_CAMPUS',Mode='VENTURE',Token='ALL_BLOCK',Revision=view.revision,CityToken=view.token}),'UNSAFE_SHARED_R_SIGNED');assert(not view.domains[1].modes.VENTURE.canSign);assert(moneyCalls==0 and rolls==0 and gold()==15 and T.encode(T.record(source).commerce.reputation)==rawHistory)")

class Differential(unittest.TestCase):
 def test_normal_quote_financial_matrix_matches_fixed_source(self):
  from contextlib import nullcontext
  rows=[]
  for old in (True,False):
   with before()if old else nullcontext():
    v=pure();v.execute("results={};legacy=...;for d=1,10 do for level=1,4 do for flag=0,1 do for _,rep in ipairs({0,20,40})do local candidate={reference={owner=0,cityID=2,x=2,y=2,token='SOURCE',changes=0},level=level,attained=0};local input={domain='DISTRICT_CAMPUS',source=ref,turn=0,D=d,balance=1000,failureCount=2,commercialized=flag==1,candidates={candidate}};if legacy then input.R=rep else input.reputationUse={status='CONFIRMED',reason='COMMERCE_REPUTATION_CONFIRMED',historyStatus='CONFIRMED',age=rep,effective=rep}end;local q=M.Quote(input);results[#results+1]=string.format('%.17g:%.17g:%.17g:%.17g:%.17g',q.safe,q.success,q.failure,q.probability,q.expected)end end end end;result=table.concat(results,'|')",old);rows.append(v.eval('result'))
  self.assertEqual(rows[0],rows[1]);measure('PU06c_financial_matrix',{'combinations':240,'same_financial_fields_as_fixed_source':True})
 def test_quantized_actual_receipts_preserve_theory_and_once_only(self):
  v=capital();v.execute("Players[0].GetTreasury=function()return {GetGoldBalance=function()return balance end,ChangeGoldBalance=function(_,amount)moneyCalls=moneyCalls+1;balance=balance+math.floor(amount*256)/256 end}end;assert(openQuote());local quoted=first().quote;assert(sign('STABLE'));local c=C.contract();assert(c.principal==quoted.principal and c.debited>0 and c.debited==c.balanceBefore-c.debitAfter);T.turn(10);c=C.contract();assert(c.stage=='SETTLED'and c.paid>0 and math.abs(c.paid-c.safe)<=.01 and moneyCalls==2);C.reload();T.turn(1);assert(moneyCalls==2)")

class Presentation(unittest.TestCase):
 def test_unavailable_risk_cannot_send_but_stable_can(self):
  v=sidebar();v.execute("local row=capitalView.domains[1];row.modes.VENTURE={canSign=false,reason='CAPITAL_REPUTATION_UNKNOWN'};row.quote.reputationUse={status='UNKNOWN',reason='MISSING'};row.quote.failure=nil;row.quote.expected=nil;row.quote.net=nil;notify();pick(1,2);assert(Controls.Confirm.disabled);local n=#sent;Controls.Confirm.click();assert(#sent==n);managers.CapitalMode.items[1].Root.click();assert(not Controls.Confirm.disabled);Controls.Confirm.click();assert(#sent==n+1 and sent[#sent].Mode=='STABLE')")
 def test_locked_policy_explanation_does_not_follow_current_quote(self):
  v=sidebar();v.execute("local row=capitalView.domains[1];row.quote.reputationUse={status='CONFIRMED',age=20,effective=20};capitalView.contracts.DISTRICT_CAMPUS={mode='VENTURE',stage='ACTIVE',principal=250,debited=250,due=10,D=1,S=1,C=1,reputationSource={status='POLICY_ZERO',effective=0}};pick(1,2);assert(Controls.Basis.text:find('已确认商业信誉：20',1,true));assert(Controls.Current.text:find('签约时：',1,true)and Controls.Current.text:find('原记录保留',1,true));row.quote.reputationUse={status='CONFIRMED',age=40,effective=40};notify();assert(Controls.Basis.text:find('已确认商业信誉：40',1,true)and Controls.Current.text:find('原记录保留',1,true))")
 def test_missing_mode_protocol_fails_closed_without_sending(self):
  v=sidebar();v.execute("capitalView.domains[1].modes=nil;notify();pick(1,1);assert(Controls.Confirm.disabled);local n=#sent;Controls.Confirm.click();assert(#sent==n)")

@contextmanager
def numeric_fixture_profile():
 """Only old explicit test R values;production/new protocol tests never use this."""
 execute=TrackedLua51.execute;path=ROOT/'Mod/CapitalInvestmentModel.lua';digest=sha256(path.read_bytes()).hexdigest()
 def run(vm,source,*a,**kw):
  # Exact IEEE float32 operation in a frozen Lua55-only fixture;not a game API.
  if isinstance(source,str)and 'function f32(v)'in source and "string.unpack('f',string.pack('f',v))"in source:
   vm.globals().__fixture_f32=lambda n:struct.unpack('f',struct.pack('f',n))[0]
   source=source.replace("string.unpack('f',string.pack('f',v))",'__fixture_f32(v)')
  value=execute(vm,source,*a,**kw)
  if sha256(source.encode()if isinstance(source,str)else source).hexdigest()==digest:
   execute(vm,"local model=SPCCapitalInvestmentModel;local quote,begin=model.Quote,model.Begin;model.Quote=function(v)if v.R~=nil then local n=model.Copy(v);local r=n.R;n.R=nil;n.reputationUse={status='CONFIRMED',reason='COMMERCE_REPUTATION_CONFIRMED',historyStatus='CONFIRMED',age=r,effective=r};return quote(n)end;return quote(v)end;model.Begin=function(old,q,mode,...)if q.kind=='CAPITAL_QUOTE_V1'then q=assert(model.Terms(q,mode))end;return begin(old,q,mode,...)end")
  return value
 with patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

class Restricted(unittest.TestCase):
 def test_actual_both_modes_need_no_raw_debug_or_host_libraries(self):
  for mode in ('STABLE','VENTURE'):
   v=capital();v.execute("assert(openQuote());rawget=nil;rawset=nil;rawequal=nil;debug=nil;io=nil;os=nil;package=nil;collectgarbage=nil;assert(sign('"+mode+"')and moneyCalls==1);assert(C.contract().reputationSource)")

if __name__=='__main__':unittest.main()
