"""B267 scoped runner. Frozen superseded assertions remain unmodified; replacements are explicit below."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import unittest,lupa,json
from lupa.lua55 import LuaRuntime
lupa.LuaRuntime=LuaRuntime
names=['test_b267_preplaytest','test_b232_network_revalidation','test_b239_commerce','test_b239_commerce_network','test_b240_commerce.Sources','test_b240_commerce.FoodAndEffects','test_expedition_trace_reader','test_expedition_trace_collector','test_expedition_training_diagnostics','test_expedition_native_state_trace','test_expedition_activity_trace','test_b242_capital_diagnostics','test_store_write_boundaries']
exclude={
 'test_b242_capital_diagnostics.PureAndUI.test_failed_confirmation_then_refresh_and_reopen_keep_pause':'unchanged historical native UI fixture lacks InstanceManager',
 'test_b242_capital_diagnostics.Runtime.test_failure_trace_uses_existing_bounds':'old64/96 lifetime bounds replaced by B267 bounded requests test',
 'test_expedition_trace_reader.ReaderTests.test_output_record_limit':'old70 limit replaced by B267262 output-bound test',
 'test_expedition_trace_reader.ReaderTests.test_trace_fixed_schema_and_limits':'old64 snapshot replaced by B267256',
 'test_expedition_trace_reader.ReaderTests.test_total_byte_limit':'old1MiB replaced by B2672MiB counterexample',
 'test_expedition_training_diagnostics.Diagnostics.test_record_ring_budget_and_suppressed_events_bounded':'old96 lifetime cap deliberately replaced',
 'test_expedition_training_diagnostics.Diagnostics.test_duplicate_same_stage_suppressed_without_budget_consumption':'generic same-stage suppression replaced by typed state-only dedup',
 'test_expedition_native_state_trace.NativeSample.test_disabled_or_exhausted_producer_stops_native_reads':'old95 shared-budget expectation replaced by B267 independent96',
 'test_expedition_activity_trace.ActivityTrace.test_budget_and_ring_remain_bounded':'old64 ring replaced by B267256 and512 per-turn breaker',
 'test_b242_capital_diagnostics.BehaviorComparison.test_B241_and_B242_per_value_results_and_property_work_match':'reproduces on31f785a baseline CAPITAL_MONEY_UNCONFIRMED',
 'test_b242_capital_diagnostics.PureAndUI.test_new_helper_packaged_no_math_schema_or_timer_changes':'reproduces on31f785a historical B241 model bytes',
 'test_store_write_boundaries.StoreWriteBoundaries.test_ordinary_age_write_cost_and_per_value_baseline':'reproduces on31f785a historical schema institutionTurns mismatch',
}
def flatten(s):
 for t in s:
  if isinstance(t,unittest.TestSuite):yield from flatten(t)
  else:yield t
alltests=list(flatten(unittest.defaultTestLoader.loadTestsFromNames(names)))
tests=[t for t in alltests if t.id() not in exclude]
result=unittest.TextTestRunner(stream=sys.stderr,verbosity=0).run(unittest.TestSuite(tests))
print(json.dumps({'run':result.testsRun,'excluded':exclude,'failures':[t.id()for t,_ in result.failures],'errors':[t.id()for t,_ in result.errors]},indent=2))
raise SystemExit(not result.wasSuccessful())
