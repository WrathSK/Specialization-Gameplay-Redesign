"""Reproduce the narrow B413 review gate; local simulation, never native PASS.

Run from repository root with Lua51+Lua55 Lupa2.8 available. No ignored runner,
external DB,game,collector socket or deployment is used. Artifacts stay ignored.
"""
import argparse,contextlib,hashlib,io,json,subprocess,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'DevelopmentTests'))
import lupa,lupa.lua51,lupa.lua55
from refactor_harness import RUN,SOURCES,TrackedLua51,legacy_source_observation
from refactor_evidence import output_path,source_snapshot,environment,store_artifact
from refactor_static import check
from test_refactor_s7d1 import profile
from test_pu06c_capital_terms import numeric_fixture_profile
BASE='b8622426a50cef08beff6253bcf9de77a10944a6'
SUITES=[
 'test_b413_review_repairs','test_b412_crew_observation','test_pu05a_receipts',
 'test_refactor_s7d6_proof.OpenProof','test_pu11_package_absence',
 'test_expedition_trace_collector.CollectorTests','test_refactor_s4b.CommerceRetention',
 'test_refactor_s6f','test_pu06a_reputation_exit','test_pu06b_reputation_use','test_pu06c_capital_terms',
 'test_b245_capital_receipts.Receipts','test_b245_capital_receipts.Guards']
BEFORE=[
 'test_b413_review_repairs.ProbeBudget.test_unrelated_local_production_does_not_spend_completion_visits',
 'test_b413_review_repairs.ProbeBudget.test_long_build_keeps_completion_window_and_budget_after_bounded_prelude',
 'test_b413_review_repairs.ProbeBudget.test_stop_keeps_fixed_listeners_and_does_not_call_remove',
 'test_b413_review_repairs.DispatchIsolation.test_stopping_before_owner_preserves_units_orders_receipts_in_all_dispatch_models',
 'test_b413_review_repairs.DispatchIsolation.test_shifting_stop_before_owner_does_not_skip_real_grant',
 'test_b413_review_repairs.CommerceNegatives.test_unknown_governor_cannot_hide_confirmed_anchor_pillage',
 'test_b413_review_repairs.CommerceNegatives.test_unknown_governor_cannot_hide_confirmed_zero_workers',
 'test_b413_review_repairs.CommerceNegatives.test_same_turn_repair_waits_for_reliable_governor_then_restores']
NUMERIC=('test_b245_capital_receipts.','test_pu06a_reputation_exit.MoneyReceipts.')
@contextlib.contextmanager
def before_sources(enabled):
    if not enabled:yield;return
    texts={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)
           for n in ('Commerce','CrewCompletionDiagnostics')}
    read=Path.read_text
    for p,s in texts.items():SOURCES[hashlib.sha256(s.encode()).hexdigest()]='historical/'+BASE+'/'+p.relative_to(ROOT).as_posix()
    with patch.object(Path,'read_text',lambda p,*a,**kw:texts[p]if p in texts else read(p,*a,**kw)):yield

def flat(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flat(item)
        else:yield item

class Suite(unittest.TestSuite):
    def run(self,result,debug=False):
        for test in self:
            # Only these explicit legacy numeric fixtures get the versioned
            # synthetic input/terms/f32 bridge. Current protocol tests do not.
            with numeric_fixture_profile()if test.id().startswith(NUMERIC)else contextlib.nullcontext():test(result)
        return result

class Result(unittest.TextTestResult):
    def startTest(self,t):RUN['active_test']=t.id();super().startTest(t)
    def stopTest(self,t):RUN['active_test']=None;super().stopTest(t)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--before',action='store_true',help='Require the eight fixed-B412 defect counterexamples to fail;never gameplay PASS')
    args=parser.parse_args();path=output_path(ROOT,'B413_before'if args.before else'B413_review')
    selected=BEFORE if args.before else SUITES
    before=source_snapshot();out,err=io.StringIO(),io.StringIO()
    with patch.object(lupa.lua55,'LuaRuntime',TrackedLua51),profile(),legacy_source_observation(),before_sources(args.before),contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        cases=list(flat(unittest.defaultTestLoader.loadTestsFromNames(selected)))
        assert len({t.id()for t in cases})==len(cases)
        result=unittest.TextTestRunner(stream=err,resultclass=Result).run(Suite(cases))
    origins={n:str(Path(m.__file__).resolve().relative_to(ROOT))for n,m in sys.modules.items()if n.startswith('test_')and getattr(m,'__file__',None)}
    assert all(p.startswith('DevelopmentTests/')for p in origins.values()),'SHADOWED_TEST_MODULE'
    failures={t.id():reason for t,reason in result.errors+result.failures}
    static=check(json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text()));stable=before==source_snapshot()
    ok=(set(failures)==set(BEFORE)if args.before else result.wasSuccessful())and not result.skipped and stable and not static['widened']
    report={'schema':2,'stage':'B413_before'if args.before else'B413_review',
        'status':('BASELINE_COUNTEREXAMPLES_CONFIRMED'if args.before else'LOCAL_SIMULATION_PASS')if ok else'FAIL',
        'tests_run':result.testsRun,'errors':[t.id()for t,_ in result.errors],'failures':[t.id()for t,_ in result.failures],
        'failure_details':failures,'counterexamples':BEFORE if args.before else[],
        'passing_properties':[t.id()for t in cases if t.id()not in failures],
        'source_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'source_snapshot':before,'source_stable':stable,'environment':environment(lupa.__version__),
        'command':'PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<lupa-environment>:DevelopmentTests python3.14 DevelopmentTests/run_pre_u5_review.py'+(' --before'if args.before else''),
        'suites':selected,'module_origins':origins,'static_review':static,
        'fixture_profiles':{'lua51':'TrackedLua51 plus versioned S7d1 profile;all imported test origins verified',
            'legacy_numeric':list(NUMERIC),'adapter':'test_pu06c_capital_terms.numeric_fixture_profile;synthetic CONFIRMED input,selected terms and exact host f32 only in listed legacy tests',
            'current_protocol':'PU06b/PU06c and new Commerce tests have no numeric compatibility wrapper'},
        'external_input':{'game':'NOT_STARTED','database':'NOT_USED','native_dispatch':'Explicit snapshot,tombstone,shifting controls,not engine proof'},
        'limits':['Crew same-tier/same-turn completion attribution remains OPEN;no deployment/native PASS',
            'L2 global write-generation D recaptures retained for the existing O1 shared-fact slice',
            'B245 TraceAndScope whole-file historical equality,old quote byte comparison and obsolete UI fixture are NOT_PASS/not selected;unchanged originals preserved,current PU06c UI/protocol checks selected',
            'Full artifacts are local evidence,not permanent backup;versioned runner/source support comparable new runs'],**RUN}
    store_artifact(path,report,out.getvalue(),err.getvalue())
    print(json.dumps({'artifact':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'source_sha256':before['sha256'],'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
        'source_stable':stable,'new_alarms':len(static['widened']),'status':report['status']}))
    if not ok:print(err.getvalue()[-8000:])
    return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
