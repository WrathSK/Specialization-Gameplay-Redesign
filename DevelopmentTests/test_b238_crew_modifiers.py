"""D0053/B238 native-shaped injection and presentation regressions.
Simulated multipliers prove one-call/no-normalization behavior, not engine stacking or overflow.
"""
from pathlib import Path
import sqlite3
import unittest
from test_b236_crews import crew_runtime, ACTION
R=Path(__file__).resolve().parents[1]
M=R/'Mod'
def fixture(observer=False):
 l=crew_runtime();l.execute((M/'UnitActions.lua').read_text());l.execute(ACTION)
 if observer:l.execute((M/'CrewPrecision.lua').read_text())
 return l
class AcceptedInjection(unittest.TestCase):
 def test_remaining_clips_base_request_not_a_guessed_bonus_inverse(self):
  l=fixture();l.execute("""
   local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);local q=c:GetBuildQueue();q.progress=900
   q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;q.progress=q.progress+2*n end
   local v=shared.UnitActions.ReadView(0,20001,'v');assert(v.baseInput==100 and v.baseUnused==160 and v.after==nil)
   assert(C.use(c,C.units[20001],'x'):find('CREW CONSUMED'));assert(#q.adds==1 and q.adds[1]==100)
   -- This intentionally uncapped fixture makes no claim about native overflow disposal.
   assert(q.progress==1100)
  """)
 def test_old_saved_capacity_remains_asset_value_and_source_gate_does_not_block_use(self):
  l=fixture();l.execute("""
   local c=C.make();local p=C.begin(c);C.complete(c,p);local u=C.units[20001];local b=crew.Unit(0,u)
   b.capacity=250;u:SetProperty(SPCCrewModel.UNIT_PROPERTY,b);T.governor(1);C.actions(c)
   assert(C.use(c,u,'x'):find('CREW CONSUMED'));assert(c:GetBuildQueue().adds[1]==250)
  """)
 def test_post_native_exception_cannot_replay_or_double_credit(self):
  l=fixture();l.execute("""
   local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);local q=c:GetBuildQueue()
   q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;q.progress=q.progress+2*n;error('after native')end
   assert(C.use(c,C.units[20001],'x'):find('HELD'));assert(q.progress==530 and #q.adds==1)
   local receipts=C.props.SPC_CREW_ACTION_RECEIPTS_V1;local _,r=next(receipts);assert(r.state=='GRANT_ATTEMPTED')
   shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=20001,PlanToken='x'});assert(#q.adds==1 and not C.units[20001])
  """)
 def test_observer_separates_base_input_from_amplified_delta(self):
  l=fixture(True);l.execute("""
   local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);local q=c:GetBuildQueue()
   q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;q.progress=q.progress+2*n end
   local measured;crew.RecordPrecision=function(pid,r)measured=r end;SPCCrewPrecision.Start(P,shared)
   assert(C.use(c,C.units[20001],'x'):find('CREW CONSUMED'))
   assert(measured.baseInput==260 and measured.observed==520 and measured.expected==nil and measured.difference==nil)
  """)
 def test_completed_target_never_subtracts_next_target(self):
  l=fixture(True);l.execute("""
   local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);local q=c:GetBuildQueue()
   q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;q.target='BUILDING_A';q.progress=0 end
   local measured;crew.RecordPrecision=function(pid,r)measured=r end;SPCCrewPrecision.Start(P,shared)
   assert(C.use(c,C.units[20001],'x'):find('CREW CONSUMED'))
   assert(measured.observed==nil and measured.note:find('TARGET_COMPLETED_OR_CHANGED'))
  """)
 def test_diagnostic_failure_cannot_change_success_or_receipt(self):
  l=fixture(True);l.execute("""
   local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c)
   crew.RecordPrecision=function()error('diagnostic unavailable')end;SPCCrewPrecision.Start(P,shared)
   assert(C.use(c,C.units[20001],'x'):find('CREW CONSUMED'));assert(#c:GetBuildQueue().adds==1)
  """)
class Presentation(unittest.TestCase):
 def test_final_localized_crew_and_institution_text_matches_rule_without_balance_notes(self):
  db=sqlite3.connect(':memory:');db.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT,PRIMARY KEY(Language,Tag))')
  db.executescript((M/'Text/TestText.sql').read_text())
  for lang in ('zh_Hans_CN','en_US'):
   tags=['LOC_UNIT_SPC_CREW_'+str(i)+'_DESCRIPTION' for i in (250,420,750,1000,1360)]
   tags+=['LOC_SPC_INDUSTRY_INSTITUTION_3_HELP','LOC_SPC_INDUSTRY_INSTITUTION_4_HELP','LOC_SPC_CREW_BASE_PREVIEW','LOC_SPC_CREW_BASE_CONFIRM','LOC_SPC_CREW_BASE_READY']
   for tag in tags:
    with self.subTest(lang=lang,tag=tag):
     text=db.execute('select Text from LocalizedText where Language=? and Tag=?',(lang,tag)).fetchone()[0]
     self.assertIn('加成' if lang=='zh_Hans_CN' else ('amplify' if tag.endswith('4_HELP') else 'modifier'),text)
     for forbidden in ('不受普通','不放大','no ordinary','does not amplify','balance','平衡','暂行接受'):self.assertNotIn(forbidden,text)
  self.assertFalse(db.execute("select 1 from LocalizedText where Tag='LOC_SPC_CREW_INJECTION_HELD'").fetchall())
 def test_runtime_description_and_observation_have_no_exact_final_claim(self):
  text=(M/'UI/UnitPanelActions.lua').read_text();self.assertNotIn('施工后：',text);self.assertNotIn('v.after',text)
  diagnostic=(M/'UI/UnitSites.lua').read_text();self.assertIn('sample.baseInput',diagnostic);self.assertNotIn('sample.expected',diagnostic);self.assertNotIn('sample.difference',diagnostic)
  self.assertIn('baseInput=r.baseInput',(M/'CrewProjects.lua').read_text())
  self.assertIn("'baseCapacity','baseInput'",(M/'ExpeditionTrainingDiagnostics.lua').read_text())
if __name__=='__main__':unittest.main()
