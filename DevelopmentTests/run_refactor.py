"""Versioned scoped runner; distinguishes confirmed counterexamples from passing properties."""
import argparse,hashlib,json,platform,subprocess,sys,unittest
from pathlib import Path
from refactor_harness import RUN,TrackedLua51
ROOT=Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',default='S2a');parser.add_argument('--output',type=Path);args=parser.parse_args()
    selection=json.loads((Path(__file__).with_name('refactor_selection.json')).read_text());names=selection['stages'][args.stage]
    import lupa,lupa.lua51
    lupa.lua51.LuaRuntime=TrackedLua51
    expected=selection['counterexamples'];counterexamples=[];unexpected=[];passed=[]
    class Result(unittest.TextTestResult):
        def startTest(self,test):
            RUN['active_test']=test.id();super().startTest(test)
        def stopTest(self,test):
            RUN['active_test']=None;super().stopTest(test)
        def addSuccess(self,test):
            if test.id() in expected:
                unexpected.append({'test':test.id(),'reason':'property now passes: retire its baseline counterexample entry'})
            passed.append(test.id());super().addSuccess(test)
        def addFailure(self,test,err):
            item=expected.get(test.id());message=self._exc_info_to_string(err,test)
            # Source lines in a traceback may contain a different coded assertion.
            # Only the actual exception text can identify this baseline failure.
            if item and str(err[1]).endswith(' : '+item['code']):
                counterexamples.append({'test':test.id(),**item,'status':'COUNTEREXAMPLE_CONFIRMED','failure':message.splitlines()[-1]})
                self.stream.write('c')
            else:super().addFailure(test,err)
    suite=unittest.defaultTestLoader.loadTestsFromNames(names)
    result=unittest.TextTestRunner(resultclass=Result,verbosity=0).run(suite)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    report={'schema':1,'stage':args.stage,'source_head':head,'source_dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True)),
      'python':platform.python_version(),'lupa':lupa.__version__,'backend':'Lua 5.1','tests_run':result.testsRun,'passing_properties':passed,
      'counterexamples':counterexamples,'failures':[t.id()for t,_ in result.failures],'errors':[t.id()for t,_ in result.errors],'unexpected':unexpected,
      **RUN,'selection_sha256':hashlib.sha256(Path(__file__).with_name('refactor_selection.json').read_bytes()).hexdigest(),
      'exclusions':selection['exclusions'],'native_mocks':selection['native_mocks'],'external_prerequisites':selection['external_prerequisites'],
      'test_source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'DevelopmentTests').glob('*refactor*.py'))},
      'evidence':'LOCAL_SIMULATION; counterexamples are OPEN gates, never architecture/native PASS'}
    from refactor_static import check
    report['static_review']=check(selection)
    ok=result.wasSuccessful() and not unexpected and not report['static_review']['widened']
    report['status']='BASELINE_RECORDED_WITH_OPEN_GATES'if ok and counterexamples else 'LOCAL_SIMULATION_PASS'if ok else 'FAIL'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k]for k in ['stage','status','tests_run','counterexamples','failures','errors','unexpected']},ensure_ascii=False,indent=2))
    return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
