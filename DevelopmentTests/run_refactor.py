"""Versioned scoped runner; distinguishes confirmed counterexamples from passing properties."""
import argparse,contextlib,hashlib,io,json,platform,shlex,subprocess,sys,traceback,unittest
from pathlib import Path
from refactor_harness import RUN,TrackedLua51
from refactor_evidence import source_snapshot,output_path,environment,external_identity,store_artifact,summary
ROOT=Path(__file__).resolve().parents[1]

class Tee(io.StringIO):
    def __init__(self,stream):super().__init__();self.stream=stream
    def write(self,text):self.stream.write(text);return super().write(text)
    def flush(self):self.stream.flush()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',default='S2a');parser.add_argument('--output',type=Path);args=parser.parse_args()
    selection=json.loads((Path(__file__).with_name('refactor_selection.json')).read_text());names=selection['stages'][args.stage]
    output=output_path(ROOT,args.stage,args.output)
    expected=selection['counterexamples'];counterexamples=[];unexpected=[];passed=[];failure_details={};started=0
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    report={'schema':2,'stage':args.stage,'source_head':head,'source_dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True)),
      'python':platform.python_version(),'lupa':'UNAVAILABLE','backend':'Lua 5.1','tests_run':0,'passing_properties':passed,
      'counterexamples':counterexamples,'failures':[],'errors':[],'unexpected':unexpected,
      'exclusions':selection['exclusions'],'native_mocks':selection['native_mocks'],'external_prerequisites':selection['external_prerequisites'],
      'evidence':'LOCAL_SIMULATION; counterexamples are OPEN gates, never architecture/native PASS',
      'source_snapshot':{},'source_stable':False,'external_input_stable':False,
      'command':shlex.join(['python3','DevelopmentTests/run_refactor.py',*sys.argv[1:]]),
      'failure_details':failure_details,'static_review':{'widened':[],'status':'NOT_COMPLETED'},'status':'FAIL'}
    class Result(unittest.TextTestResult):
        def startTest(self,test):
            nonlocal started
            started+=1;RUN['active_test']=test.id();super().startTest(test)
        def stopTest(self,test):
            RUN['active_test']=None;super().stopTest(test)
        def addSuccess(self,test):
            if test.id() in expected:
                unexpected.append({'test':test.id(),'reason':'property now passes: retire its baseline counterexample entry'})
            passed.append(test.id());super().addSuccess(test)
        def addFailure(self,test,err):
            item=expected.get(test.id());message=self._exc_info_to_string(err,test);failure_details[test.id()]=message
            # Only actual exception text identifies the baseline; traceback source lines do not.
            if item and str(err[1]).endswith(' : '+item['code']):
                counterexamples.append({'test':test.id(),**item,'status':'COUNTEREXAMPLE_CONFIRMED','failure':message.splitlines()[-1]})
                self.stream.write('c')
            else:super().addFailure(test,err)
        def addError(self,test,err):
            failure_details[test.id()]=self._exc_info_to_string(err,test);super().addError(test,err)
    stdout,stderr=Tee(sys.stdout),Tee(sys.stderr);fatal=None;ok=False;phase='setup'
    try:
        with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr):
            before=source_snapshot(ROOT);report['source_snapshot']=before
            external_before=external_identity(ROOT);report['external_input']=external_before
            import lupa,lupa.lua51
            report['lupa']=lupa.__version__;report['environment']=environment(lupa.__version__)
            lupa.lua51.LuaRuntime=TrackedLua51
            phase='discovery';suite=unittest.defaultTestLoader.loadTestsFromNames(names)
            phase='execution';result=unittest.TextTestRunner(resultclass=Result,verbosity=0).run(suite)
            report['failures']=[t.id()for t,_ in result.failures];report['errors']=[t.id()for t,_ in result.errors]
            phase='post_validation'
            report['source_stable']=before==source_snapshot(ROOT)
            report['external_input_stable']=external_before==external_identity(ROOT)
            report['selection_sha256']=hashlib.sha256(Path(__file__).with_name('refactor_selection.json').read_bytes()).hexdigest()
            report['test_source_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'DevelopmentTests').glob('*refactor*.py'))}
            from refactor_static import check
            report['static_review']=check(selection)
            ok=result.wasSuccessful() and not unexpected and not report['static_review']['widened'] and report['source_stable'] and report['external_input_stable']
    except BaseException as error:
        fatal=error;key='runner:'+phase
        report['errors'].append(key);failure_details[key]=traceback.format_exc()
        stderr.write(failure_details[key])
    finally:
        report.update(RUN);report['tests_run']=started
        report['status']='BASELINE_RECORDED_WITH_OPEN_GATES'if ok and counterexamples else 'LOCAL_SIMULATION_PASS'if ok else 'FAIL'
        store_artifact(output,report,stdout.getvalue(),stderr.getvalue())
    print(summary(output,ROOT))
    if fatal and not isinstance(fatal,Exception):raise fatal
    return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
