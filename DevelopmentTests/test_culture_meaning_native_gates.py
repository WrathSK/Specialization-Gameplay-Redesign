"""B165 loaded-recipient proof / normal-environment gate. Local evidence only.

Uses the current configured DB read-only and maintained exact Lua fixtures.
Inherits B164's applicable checks; its frozen modinfo191 check is not applicable
and is replaced by an explicit current-package192 check, never edited or ignored
as a hidden failure. No simulated native amount is an engine PASS.
"""
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
import test_culture_meaning_quarantine as q
import test_neighborhood_depth_catalog as neighborhood
import test_culture_meaning_probe as legacy
R=Path(__file__).resolve().parents[1]

class NativeGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.sql=legacy.database()
    @classmethod
    def tearDownClass(cls):cls.sql.close()
    def helper(self):
        h=q.QuarantineTests();h.sql=self.sql;return h
    def runtime(self):
        l=self.helper().runtime();l.execute('sixDepthFixture(a)');return l
    def reader(self):
        l=self.helper().native_panel_runtime()
        source=(R/'Mod/Probe.lua').read_text()
        l.execute(source[source.index('function P.Call('):source.index('function P.Rows(')])
        l.execute(r"""
          local row=GameInfo.Buildings.BUILDING_AMPHITHEATER
          row.Hash=90909;row.Name='Test construction';row.InternalOnly=0;row.IsWonder=0
          local queue=a.GetBuildQueue
          a.GetBuildQueue=function(c)
            local v=queue(c)
            v.GetSize=function()return 1 end
            v.GetCurrentProductionTypeHash=function()return row.Hash end
            v.GetBuildingProgress=function()progressCalls=(progressCalls or 0)+1;return nativeProgress or 20 end
            v.GetBuildingCost=function()return 500 end
            v.GetProductionYield=function()return nativeRate or 30 end
            return v
          end
          GameInfo.Buildings[row.Hash]=row
          function gateRead(mark)return SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),mark)end
          function readerBegin()
            probe.GateAdvance(0,a,'gate-base');assert(gateRead(true):find('同回合基线已记录',1,true))
            probe.GateAdvance(0,a,'gate-active');setNativeFive()
          end
        """)
        return l
    def test_current_db_exact_loaded_recipient_set_and_seven_attachments(self):
        l=self.runtime();c=l.eval('SPCCultureMeaningModel.RecipientCoverage(P)')
        rows=self.sql.execute("SELECT GreatWorkObjectType,COUNT(*) FROM GreatWorks WHERE GreatWorkObjectType IN ('GREATWORKOBJECT_WRITING','GREATWORKOBJECT_MUSIC','GREATWORKOBJECT_SCULPTURE','GREATWORKOBJECT_PORTRAIT','GREATWORKOBJECT_LANDSCAPE','GREATWORKOBJECT_RELIGIOUS','GREATWORKOBJECT_ARTIFACT') GROUP BY 1").fetchall()
        self.assertEqual(c['status'],'VERIFIED_LOADED_SET');self.assertEqual(c['blocked'],0)
        self.assertEqual(c['verified'],sum(n for _,n in rows))
        for kind,n in rows:self.assertEqual(c['byCategory'][kind.removeprefix('GREATWORKOBJECT_')],n)
        for name in l.globals().SPCCultureMeaningModel.Owned.values():
            cats={x[0]for x in self.sql.execute("SELECT a.Value FROM BuildingModifiers b JOIN ModifierArguments a USING(ModifierId) WHERE b.BuildingType=? AND a.Name='GreatWorkObjectType'",(name,))}
            self.assertEqual(cats,{x[0]for x in rows})
    def test_unknown_same_class_anywhere_blocks_before_hold_or_positive_write(self):
        l=self.runtime();l.execute(r"""
          local rows=GameInfo.GreatWorks
          GameInfo.GreatWorks=setmetatable({}, {__index=rows,__call=function()
            local iter=rows();local done=false
            return function()local v=iter();if v then return v end
              if not done then done=true;return {GreatWorkType='GREATWORK_UNKNOWN_MOD',GreatWorkObjectType='GREATWORKOBJECT_WRITING'}end
            end
          end})
          local before=writes
          assert(not pcall(probe.GateAdvance,0,a,'blocked'))
          assert(probe.recipientCoverage.status=='BLOCKED_LOADED_SET' and probe.recipientCoverage.blocked==1)
          assert(probe.mode=='OFF' and not dialogue.meaningOverride and not gwa.IsMeaningHeld(0,a) and next(exactMeaning(a))==nil and writes==before)
          assert(probe.Describe(0,a):find('同类定义未获支持',1,true))
        """)
    def test_known_type_unreviewed_metadata_cannot_pass_coverage(self):
        l=self.runtime();l.execute(r"""
          GameInfo.GreatWorks.GREATWORK_BHASA_1.EraType='ERA_FUTURE'
          assert(not pcall(probe.GateAdvance,0,a,'metadata'))
          assert(probe.recipientCoverage.blocked==1 and probe.recipientCoverage.reasons[1]:find('UNREVIEWED_ERA',1,true))
          assert(not gwa.IsMeaningHeld(0,a) and next(exactMeaning(a))==nil)
        """)
    def test_other_work_classes_remain_excluded_without_blocking_loaded_set(self):
        l=self.runtime();l.execute(r"""
          local result=SPCCultureMeaningModel.RecipientCoverage(P)
          assert(result.other>0 and result.blocked==0)
          probe.GateAdvance(0,a,'base');assert(probe.recipientCoverage.status=='VERIFIED_LOADED_SET')
        """)
    def test_duplicate_empty_and_unavailable_metadata_fail_honestly(self):
        for kind in ('duplicate','empty','missing'):
            with self.subTest(kind=kind):
                l=self.runtime();l.globals().failureKind=kind;l.execute(r"""
                  if failureKind=='missing' then GameInfo.GreatWorks=nil
                  elseif failureKind=='empty' then GameInfo.GreatWorks=setmetatable({}, {__call=function()return function()end end})
                  else
                    local v=GameInfo.GreatWorks.GREATWORK_BHASA_1
                    GameInfo.GreatWorks=setmetatable({[v.GreatWorkType]=v},{__call=function()local n=0;return function()n=n+1;if n<=2 then return v end end end})
                  end
                  assert(not pcall(probe.GateAdvance,0,a,'invalid'))
                  assert(not gwa.IsMeaningHeld(0,a) and next(exactMeaning(a))==nil)
                """)
    def test_normal_positive_dialogue_preserved_and_same_turn_reconfiguration(self):
        l=self.runtime();l.execute(r"""
          a.workCount=2
          dialogue.samples[0].cities[1]={{id=1,type='GREATWORK_BHASA_1'},{id=2,type='GREATWORK_SHAKESPEARE_1'}}
          dialogue.Audit(0,1);local percent=dialogue.last[0][1].percent;assert(percent>0)
          probe.GateAdvance(0,a,'base');assert(not dialogue.meaningOverride and dialogue.ReadNormalForMeaning(0,a)==percent)
          probe.GateAdvance(0,a,'active');assert(configured(a,'SCIENCE')==3 and configured(a,'CULTURE')==0)
          assert(dialogue.ReadNormalForMeaning(0,a)==percent and gwa.IsMeaningHeld(0,a) and not old(a,'SCIENCE'))
          sixDepths.DISTRICT_CAMPUS=8;probe.Audit();assert(configured(a,'SCIENCE')==4 and dialogue.ReadNormalForMeaning(0,a)==percent)
          local before=writes;probe.Audit();assert(writes==before)
          probe.End(0,a,'end');assert(not dialogue.meaningOverride and not gwa.IsMeaningHeld(0,a) and next(exactMeaning(a))==nil)
        """)
    def test_actual_request_token_read_end_and_city_isolation(self):
        l=self.runtime();legacy.bind_actual_request(l);l.execute(r"""
          local other=snapshotBuildings(b)
          finalRequest('CULTURE_MEANING_GATE_ADVANCE','base');local v=finalRequest('CULTURE_MEANING_GATE_ADVANCE','active')
          assert(v.normalEnvironment and v.recipientStatus=='VERIFIED_LOADED_SET' and v.dialoguePercent==0)
          local before=writes;finalRequest('CULTURE_MEANING_GATE_ADVANCE','active');finalRequest('CULTURE_MEANING_READ','read');assert(writes==before)
          finalRequest('CULTURE_MEANING_END','end');before=writes;finalRequest('CULTURE_MEANING_END','end');assert(writes==before)
          assertBuildingsSame(b,other);assert(next(exactMeaning(a))==nil)
        """)
    def test_flow_conflict_cannot_change_existing_holder(self):
        l=self.runtime();l.execute(r"""
          probe.Advance(0,a,'old-base');local before=writes
          assert(not pcall(probe.GateAdvance,0,a,'gate-conflict') and writes==before and dialogue.IsMeaningProbeHeld(0,a,0))
          probe.End(0,a,'end');probe.GateAdvance(0,a,'normal-base');before=writes
          assert(not pcall(probe.Advance,0,a,'old-conflict') and writes==before and not dialogue.meaningOverride)
        """)
    def test_end_failure_keeps_gwa_hold_until_exact_withdrawal_succeeds(self):
        l=self.runtime();l.execute(r"""
          probe.GateAdvance(0,a,'base');probe.GateAdvance(0,a,'active')
          failRemove=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_3.Index
          assert(not pcall(probe.End,0,a,'fail') and gwa.IsMeaningHeld(0,a) and next(exactMeaning(a))~=nil)
          local before=writes;failRemove=nil;probe.End(0,a,'fail');assert(writes==before)
          probe.End(0,a,'recover');assert(next(exactMeaning(a))==nil and not gwa.IsMeaningHeld(0,a))
        """)
    def test_unknown_reference_and_confirmed_loss_remain_distinct(self):
        l=self.runtime();l.execute(r"""
          probe.GateAdvance(0,a,'base');probe.GateAdvance(0,a,'active');local before=writes
          sixUnknown=true;probe.Audit();assert(writes==before and gwa.IsMeaningHeld(0,a))
          sixUnknown=false;probe.Audit();assert(not probe.error)
          local loss={confirmed=false,targetID=a.id,origin={owner=0}}
          assert(not pcall(exits.CultureMeaningProbe,a,loss) and writes==before)
          loss.confirmed=true;a.owner=3;exits.CultureMeaningProbe(a,loss)
          assert(probe.mode=='OFF' and next(exactMeaning(a))==nil)
        """)
    def test_reader_normal_themed_context_uses_independent_values_and_flags_inflation(self):
        l=self.reader();l.execute(r"""
          local get=a.GetBuildings;a.GetBuildings=function(c)local bs=get(c);bs.IsBuildingThemedCorrectly=function()return true end;return bs end
          readerBegin();local s=gateRead(false)
          assert(s:find('已主题化',1,true) and s:find('生产力｜每件 +3／本城 +3｜实测差值 +3.00',1,true),s)
          nativeSix.PRODUCTION=6;s=gateRead(false);assert(s:find('生产力异常',1,true),s)
          assert(s:find('正常对话／主题环境',1,true))
        """)
    def test_read_only_queue_progress_across_turns_not_auto_pass_or_write(self):
        l=self.reader();l.execute(r"""
          readerBegin();local before=writes;nativeProgress=20;nativeRate=30
          local s=gateRead(false);assert(s:find('进度 20.00 / 500.00',1,true) and s:find('队列生产读数 30.00',1,true),s)
          nativeProgress=50;turn=turn+1;collection();probe.Audit()
          s=gateRead(false);assert(s:find('进度 50.00 / 500.00',1,true) and not s:find('PASS',1,true),s)
          assert(writes==before)
        """)
    def test_missing_rate_keeps_actual_progress_without_claiming_settlement(self):
        l=self.reader();l.execute(r"""
          readerBegin();local queue=a.GetBuildQueue;a.GetBuildQueue=function(c)local x=queue(c);x.GetProductionYield=nil;return x end
          local s=gateRead(false);assert(s:find('进度 20.00 / 500.00',1,true) and s:find('队列生产读数未确认',1,true),s)
          assert(not s:find('PASS',1,true))
        """)
    def test_changed_normal_dialogue_or_theme_invalidates_comparison(self):
        l=self.reader();l.execute(r"""
          readerBegin();local v=probe.View(0,a);v.dialoguePercent=25
          local s=SPCBoostGreatWorkRead.Meaning(P,a,v,false);assert(s:find('差值未确认',1,true),s)
          SPCBoostGreatWorkRead.ClearMeaningRead();assert(gateRead(false):find('差值未确认',1,true))
        """)
    def test_gate_metadata_read_is_cached_per_session_and_no_new_hooks(self):
        l=self.runtime();l.execute(r"""
          local count=0;local verify=SPCCultureMeaningModel.RecipientCoverage
          SPCCultureMeaningModel.RecipientCoverage=function(...)count=count+1;return verify(...)end
          probe.GateAdvance(0,a,'base');probe.GateAdvance(0,a,'active');probe.Audit();probe.View(0,a);probe.End(0,a,'end')
          probe.GateAdvance(0,a,'base2');assert(count==1)
        """)
        source=(R/'Mod/CultureMeaningProbe.lua').read_text()
        self.assertNotIn('collectgarbage',source)
        self.assertNotIn('SetProperty',source)
        old=__import__('subprocess').check_output(['git','show','09d35a0:Mod/CultureMeaningProbe.lua'],cwd=R,text=True)
        self.assertEqual(source.count('bind('),old.count('bind('))
    def test_valid_normal_dialogue_projection_reused_without_duplicate_audit(self):
        l=self.runtime();l.execute(r"""
          probe.GateAdvance(0,a,'base');local called=0;local audit=dialogue.Audit
          dialogue.Audit=function(...)called=called+1;return audit(...)end
          probe.GateAdvance(0,a,'active');probe.Audit();assert(called==0)
          sixDepths.DISTRICT_CAMPUS=8;probe.Audit();assert(called==0 and configured(a,'SCIENCE')==4)
        """)
    def test_package_syntax_imports_current_192_and_read_callback(self):
        root=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot();self.assertEqual(root.attrib['version'],'192')
        self.assertIn('B165.192',root.findtext('./Properties/Description'))
        legacy.require_meaning_imports(root)
        l=LuaRuntime(unpack_returned_tuples=True)
        for path in ('CultureMeaningModel.lua','CultureMeaningProbe.lua','Dialogue.lua','Gameplay.lua','UI/BoostGreatWorkRead.lua','UI/P0Panel.lua','Probe.lua'):
            src=(R/'Mod'/path).read_text()
            l.execute('assert(load(...))',src)
        text=(R/'Mod/Text/TestText.sql').read_text();self.assertIn('意义延展·接入门禁',text)
        panel=(R/'Mod/UI/P0Panel.lua').read_text();self.assertIn("request('CULTURE_MEANING_GATE_ADVANCE')",panel)
        self.assertEqual((R/'Mod/Data/CultureMeaningProbe.sql').read_bytes(),__import__('subprocess').check_output(['git','show','09d35a0:Mod/Data/CultureMeaningProbe.sql'],cwd=R))

def load_tests(loader,tests,pattern):
    # Stable inherited method list; only old package-version assertion is NA.
    inherited=loader.loadTestsFromTestCase(q.QuarantineTests)
    for test in inherited:
        if test._testMethodName!='test_package_syntax_exact_action_imports_and_current_191':tests.addTest(test)
    tests.addTests(loader.loadTestsFromModule(neighborhood))
    return tests

if __name__=='__main__':unittest.main()
