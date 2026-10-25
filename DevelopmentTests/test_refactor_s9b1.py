"""Gameplay owns Development target policy; UI only samples raw native facts/prices."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,Context,SOURCES,executed,completion,legacy_source_observation,measure
import test_store_write_boundaries as store_fixture
import test_b246_development as development

BASE='0bf5fd5'
@contextmanager
def before():
 original={ROOT/'Mod'/p:subprocess.check_output(['git','show',BASE+':Mod/'+p],cwd=ROOT,text=True)for p in ('DevelopmentInvestment.lua','UI/DevelopmentInvestmentRead.lua','UI/CrewProjectOrder.lua')}
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


def runtime(tier0=False):
 text=development.SETUP.replace('Tier=1,Cost=100','Tier=0,Cost=100',1)if tier0 else development.SETUP
 with patch.object(store_fixture,'LuaRuntime',TrackedLua51),patch.object(development,'SETUP',text),legacy_source_observation():return development.runtime()


class Policy(unittest.TestCase):
 def test_actual_before_after_options_costs_existing_quotes_and_price_work_match(self):
  cases=("","prices[1101]=480;prices[1102]=480;","eligible[1101]=false;","research.markers[101]=true;research.markers[102]=true;","prices[1102]=nil;","prices[1103]=nil;","eligible[1101]=false;eligible[1102]=false;","GameInfo.Buildings.BUILDING_DEV_LIBRARY.PurchaseYield=nil;","prices[1101]=0;","priceFail=true;")
  rows=[]
  for tier0 in (False,True):
   for case in cases:
    results=[]
    for old in (True,False):
     with before()if old else nullcontext():v=runtime(tier0)
     v.execute(case+"local prior=readCalls;open();encoded=T.encode(view().options);calls=readCalls-prior;stateBytes=T.encode(value());money=moneyCalls")
     results.append((v.eval('encoded'),v.eval('calls'),v.eval('stateBytes'),v.eval('money')))
    self.assertEqual(results[0],results[1],(tier0,case));rows.append(results[1][1])
  measure('S9b1_target_policy_differential',{'cases':20,'same_options_price_cost_and_source_history':True,'same_native_purchase_cost_calls':True,'tier_zero_and_tie_rule':True})
 def test_bad_price_only_blocks_its_domain_and_other_domain_still_signs(self):
  v=runtime();v.execute("prices[1101]=nil;open();assert(view().options[1].domain=='DISTRICT_CAMPUS'and view().options[1].reason=='DEVELOPMENT_PRICE_UNAVAILABLE');assert(view().options[2].domain=='DISTRICT_INDUSTRIAL_ZONE'and view().options[2].canSign);assert(sign(source,research,'DISTRICT_INDUSTRIAL_ZONE')and moneyCalls==1)")
 def test_non_numeric_zero_negative_nan_infinite_price_never_debits(self):
  for price in ("'400.125'",'0','-1','0/0','math.huge','-math.huge'):
   v=runtime();v.execute("prices[1101]="+price+";open();assert(view().options[1].reason=='DEVELOPMENT_PRICE_UNAVAILABLE'and not sign()and moneyCalls==0)")
 def test_explicit_raw_and_price_control_calls_but_original_price_count_and_zero_idle_work(self):
  v=runtime();v.execute("local a,b=ExposedMembers.SPC_DevelopmentRead,ExposedMembers.SPC_DevelopmentPriceRead;rawCalls,priceCalls=0,0;ExposedMembers.SPC_DevelopmentRead=function(...)rawCalls=rawCalls+1;return a(...)end;ExposedMembers.SPC_DevelopmentPriceRead=function(...)priceCalls=priceCalls+1;return b(...)end;local prior=readCalls;open();assert(rawCalls==1 and priceCalls==1 and readCalls-prior==3);local w=T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(rawCalls==1 and priceCalls==1 and readCalls-prior==3 and T.writes()==w)")
  measure('S9b1_native_quote_work',{'targets':1,'raw_control_calls':1,'price_control_calls':1,'additional_exact_city_lookup':1,'purchase_cost_calls_before_after':[3,3],'idle_extra_control_calls':0,'all_price_tiers_read':False})
 def test_UI_returns_no_business_options_and_pricing_does_not_repeat_construction_reads(self):
  v=runtime();v.execute("local r=ExposedMembers.SPC_DevelopmentRead(0,research:GetID());assert(r.protocol==2 and r.phase=='ELIGIBILITY'and r.options==nil and r.existing==nil);local cat=SPCDevelopmentInvestmentCatalog.Build(P);local groups,existing,encoded,ids=SPCDevelopmentInvestmentTargets.Candidates(cat,r);assert(existing.DISTRICT_CAMPUS and #ids==3);local old=P.HasBuilding;P.HasBuilding=function()error('PRICE_MUST_NOT_RESCAN_BUILDINGS')end;local q=ExposedMembers.SPC_DevelopmentPriceRead(0,research:GetID(),encoded);assert(q.phase=='PRICES'and q.request==encoded and q.generation==r.generation and q.prices.BUILDING_DEV_LIBRARY.value==400.125);P.HasBuilding=old")


class Protocol(unittest.TestCase):
 def test_wrong_protocol_phase_generation_and_reference_are_rejected_without_money(self):
  changes=("r.protocol=1","r.phase='OTHER'","r.generation=nil","r.owner=9","r.cityID=9","r.x=99","r.y=99","r.turn=r.turn+1")
  for phase in ('RAW','PRICE'):
   for change in changes:
    v=runtime();v.execute("local name=...;local old=ExposedMembers[name];ExposedMembers[name]=function(...)local r=old(...);"+change+";return r end;open();assert(not sign()and moneyCalls==0)",'SPC_DevelopmentRead'if phase=='RAW'else'SPC_DevelopmentPriceRead')
 def test_missing_extra_status_or_request_mismatch_price_rows_cannot_form_quote(self):
  for change in ("r.request='OTHER'","r.prices.BUILDING_DEV_LIBRARY=nil","r.prices.OTHER={status='RETURNED',value=1}","r.prices.BUILDING_DEV_LIBRARY.status='UNKNOWN'"):
   v=runtime();v.execute("local old=ExposedMembers.SPC_DevelopmentPriceRead;ExposedMembers.SPC_DevelopmentPriceRead=function(...)local r=old(...);"+change+";return r end;open();assert(not sign()and moneyCalls==0)")
 def test_malformed_or_duplicate_price_request_fails_before_native_price_read(self):
  v=runtime();v.execute("local id='BUILDING_DEV_LIBRARY';local encoded=#id..':'..id;local before=readCalls;for _,bad in ipairs({'garbage','0:',encoded..encoded,'999:BAD','3:BAD'})do assert(not pcall(ExposedMembers.SPC_DevelopmentPriceRead,0,research:GetID(),bad))end;assert(readCalls==before)")
 def test_reader_context_replacement_between_phases_holds_then_next_explicit_open_recovers(self):
  v=runtime();v.execute("local first=ExposedMembers.SPC_DevelopmentRead;local once=true;ExposedMembers.SPC_DevelopmentRead=function(...)local r=first(...);if once then once=false;SPCDevelopmentInvestmentRead.New(P)end;return r end;open();assert(not sign()and moneyCalls==0);open();assert(sign()and moneyCalls==1)")
 def test_price_and_qualification_changes_still_require_fresh_confirmation(self):
  for change in ('prices[1101]=900','eligible[1101]=false','research.markers[101]=true;research.markers[102]=true'):
   v=runtime();v.execute(change+";assert(not sign()and moneyCalls==0);open();assert(sign()and moneyCalls==1)")
 def test_owner_loss_inside_price_return_cannot_publish_a_ready_target(self):
  v=runtime();v.execute("local price=ExposedMembers.SPC_DevelopmentPriceRead;ExposedMembers.SPC_DevelopmentPriceRead=function(...)local out=price(...);research.s.ref.owner=3;return out end;open();for _,row in ipairs(view().options)do if row.targetCity==research:GetID()then assert(not row.canSign and row.reason=='DEVELOPMENT_NATIVE_FACTS_STALE')end end;assert(moneyCalls==0)")
 def test_no_candidate_branch_rechecks_owner_after_pure_rule_boundary(self):
  v=runtime();v.execute("local rules=SPCDevelopmentInvestmentTargets.Candidates;SPCDevelopmentInvestmentTargets.Candidates=function(...)local groups,existing,encoded,ids=rules(...);research.s.ref.owner=3;return {},existing,'',{}end;open();for _,row in ipairs(view().options)do assert(not row.canSign)end;assert(moneyCalls==0)")
 def test_confirmation_reads_only_selected_target_until_existing_postconfirm_refresh(self):
  v=runtime();v.execute("outgoing={research:GetID(),other:GetID()};open();local raw,price=ExposedMembers.SPC_DevelopmentRead,ExposedMembers.SPC_DevelopmentPriceRead;local otherRaw,otherPrice=0,0;ExposedMembers.SPC_DevelopmentRead=function(pid,id)if id==other:GetID()then otherRaw=otherRaw+1;assert(moneyCalls==1)end;return raw(pid,id)end;ExposedMembers.SPC_DevelopmentPriceRead=function(pid,id,ids)if id==other:GetID()then otherPrice=otherPrice+1;assert(moneyCalls==1)end;return price(pid,id,ids)end;assert(sign()and otherRaw==1 and otherPrice==1 and moneyCalls==1)")


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9a2'])])

if __name__=='__main__':unittest.main()
