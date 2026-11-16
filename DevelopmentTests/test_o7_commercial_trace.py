"""Optional TRAIN observations with real commercial owners and simulated natives."""

from collections import deque
import unittest
from unittest.mock import patch

from refactor_harness import Context, PackageVFS, ROOT, legacy_source_observation, measure
from retired_crew_sources import package as historical_package
from test_b241_capital import SETUP as CAPITAL_SETUP
from test_b246_development import SETUP as DEVELOPMENT_SETUP
from test_refactor_s6f import combined
import test_refactor_s6f
import test_store_write_boundaries as store_fixture


BASE = 'cefa39ff73a71d070e9072be7c41690bc6f6ccc1'
LOGGER = 'ExpeditionTrainingDiagnostics'
OWNERS = ('Commerce', 'CapitalInvestment', 'DevelopmentInvestment')
OFF = "SPCExpeditionTrainingDiagnostics.ENABLED=false"
PROFILE = {
    'present': '',
    'disabled': OFF,
    'factory_throws': "SPCExpeditionTrainingDiagnostics.New=function()error('OBSERVER_CONSTRUCTION')end",
    'malformed': "SPCExpeditionTrainingDiagnostics.New=function()return {Record=false}end",
    'record_throws': """SPCExpeditionTrainingDiagnostics.New=function()
       return {Record=function()error('OBSERVER_RECORD')end}
     end""",
    'throw': '',
    'silent_nil': '',
}


def context(mode, baseline=None):
    root = baseline or ROOT
    missing = mode in ('throw', 'silent_nil')
    vfs = PackageVFS(absent=[LOGGER] if missing else [], missing_include=mode if missing else 'throw',
                     forbidden_globals=['SPCExpeditionTrainingDiagnostics'] if missing else [],
                     manifest=root/'Mod/SpecializationP0.modinfo')
    ctx = Context(name='CommercialTrace', vfs=vfs, history=(root, BASE) if baseline else None)
    ctx.loads = deque(maxlen=512)
    return ctx


def fixture(mode):
    ctx = context(mode)
    with legacy_source_observation(), patch.object(store_fixture, 'LuaRuntime', lambda **_: ctx.lua):
        store_fixture.fixture()

    def include(name):
        result = ctx.load(name, included=True)
        if name == LOGGER and PROFILE[mode]:
            ctx.execute(PROFILE[mode])
        return result

    ctx.globals().include = include
    ctx.load('CapitalInvestment')
    ctx.execute(CAPITAL_SETUP)
    return ctx


def development(ctx):
    ctx.load('DevelopmentInvestment')
    ctx.load('UI/DevelopmentInvestmentRead')
    old = 'local first=T.control(c).first'
    new = 'local r=T.record(c);local first=r.current and r.currentFirst or r.base.first'
    assert DEVELOPMENT_SETUP.count(old) == 1
    ctx.execute(DEVELOPMENT_SETUP.replace(old, new))
    return ctx.lua


def run_commercial(mode):
    ctx = fixture(mode)
    ctx.execute("""
      local q=C.view().domains[1].quote
      assert(C.confirm());assert(not C.confirm() and moneyCalls==1)
      local a=C.contract();assert(a.stage=='ACTIVE' and a.principal==q.principal)
      T.turn(10);cap.Reconcile(0);cap.Reconcile(0)
      local s=C.contract();assert(s.stage=='SETTLED' and moneyCalls==2)
      capOutcome=T.encode({quote=q.principal,receipt=s,balance=balance,calls=moneyCalls})
    """)
    with patch.object(test_refactor_s6f, 'development_fixture', lambda: development(ctx)):
        combined()
    ctx.execute("""
      assert(open(),dev.lastRequest.reason) -- refresh the quote against the now-live Commerce view
      local before=moneyCalls;local expected=view().options[1].cost
      assert(sign(),dev.lastRequest.reason);assert(not sign() and moneyCalls==before+1)
      assert(active() and contract().stage=='ACTIVE' and contract().cost==expected)
      research.markers[102]=true;GameEvents.BuildingConstructed.Fire(0,research:GetID(),102)
      assert(contract().stage=='COMPLETED' and not active() and moneyCalls==before+1)
      devOutcome=T.encode({receipt=contract(),balance=balance,calls=moneyCalls,writes=effectWrites})
      local counts=P.Count
      observerReads=0
      P.Count=function(label,...)
       if label=='observer_native_attempt' or label=='observer_city_scan' then observerReads=observerReads+1 end
       if counts then return counts(label,...)end
      end
      Events.PlayerTurnDeactivated.Fire(0);GameEvents.PlayerTurnStarted.Fire(0)
      turnRows=0
      local log=ExposedMembers.SPC_B205TrainingTrace
      for _,r in ipairs(log and log.entries or {})do
       if r.stage=='COMMERCE_TURN_END' or r.stage=='COMMERCE_TURN_STARTED' then turnRows=turnRows+1 end
      end
      assert(gold()==15)
      commerceOutcome=T.encode({gold=gold(),writes=com.writes,v=auditCommerce()})
    """)
    return ctx


class CommercialTrace(unittest.TestCase):
    def test_b448_hard_import_depended_on_logger_at_each_owner(self):
        with historical_package(BASE) as checkout:
            for owner in OWNERS:
                with self.subTest(owner=owner):
                    ctx = context('throw', checkout)
                    with self.assertRaisesRegex(Exception, 'PACKAGE_ABSENT:ExpeditionTrainingDiagnostics.lua'):
                        ctx.load(owner)
                    self.assertTrue(any(row['parent']==f'historical/{BASE}/Mod/{owner}.lua'
                                        and row['module']==LOGGER+'.lua' and row['status']=='ABSENT'
                                        for row in ctx.loads))

    def test_unchanged_carriers_debits_credits_and_receipts_in_seven_profiles(self):
        baseline = None
        for mode in PROFILE:
            with self.subTest(mode=mode):
                ctx = run_commercial(mode)
                outcome = tuple(ctx.eval(key) for key in ('capOutcome', 'devOutcome', 'commerceOutcome'))
                if mode == 'present':
                    baseline = outcome
                    self.assertGreater(ctx.eval('observerReads'), 0)
                    self.assertEqual(ctx.eval('turnRows'), 2)
                else:
                    self.assertEqual(outcome, baseline)
                    self.assertEqual(ctx.eval('turnRows'), 0)
                    if mode != 'record_throws':
                        self.assertEqual(ctx.eval('observerReads'), 0)
                if mode in ('throw', 'silent_nil'):
                    self.assertIsNone(ctx.globals().SPCExpeditionTrainingDiagnostics)
                    touched = {row['parent'] for row in ctx.loads if row['module']==LOGGER+'.lua'
                               and row['status']=='ABSENT'}
                    self.assertEqual(touched, {'Mod/'+name+'.lua' for name in OWNERS})
                    self.assertEqual(ctx.load_counts['failed'], 0)
        measure('O7g_commercial_trace_profiles', {'profiles':list(PROFILE),'owners':list(OWNERS),
                'same_carrier_treasury_and_receipt_results':True,'owned_turn_rows_when_enabled':2,
                'missing_disabled_bad_factory_turn_reads':0,'fixture':'actual owners + Store; native and route input doubles'})

    def test_missing_or_faulty_observer_does_not_hide_business_failure_or_replay(self):
        for mode in ('present', 'factory_throws', 'record_throws', 'throw', 'silent_nil'):
            with self.subTest(mode=mode):
                ctx = fixture(mode)
                ctx.execute("""
                  moneyFail='AFTER'
                  assert(not C.confirm() and moneyCalls==1)
                  assert(cap.lastRequest.reason=='CAPITAL_MONEY_UNCONFIRMED')
                  assert(C.contract().stage=='DEBIT_CALLING')
                  cap.Reconcile(0);assert(not C.confirm() and moneyCalls==1)
                  moneyFail=nil
                """)
                development(ctx)
                ctx.execute("""
                  local before=moneyCalls;moneyFail='AFTER'
                  assert(not sign() and moneyCalls==before+1)
                  assert(dev.lastRequest.reason=='DEVELOPMENT_MONEY_UNCONFIRMED')
                  dev.Reconcile(0)
                  assert(not sign() and moneyCalls==before+1 and not active())
                """)
