"""B164 five-yield quarantine: targeted current Lua/SQL/UI evidence only.

Compose maintained fixtures and selected applicable regression methods; retain
all historical suite assertions. The configured external DB is read-only and
rebuilt only in memory. No Civ VI yield, settlement or lifecycle PASS is claimed.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
import test_culture_meaning_probe as legacy
import test_culture_meaning_final_yields as final
import test_culture_meaning_cleanup as cleanup
import test_modifier_read as modifier

R = Path(__file__).resolve().parents[1]


class QuarantineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sql = legacy.database()

    @classmethod
    def tearDownClass(cls):
        cls.sql.close()

    def final_helper(self):
        helper = final.FinalYieldTests()
        helper.sql = self.sql
        return helper

    def runtime(self, real_samples=False):
        return self.final_helper().runtime(real_samples=real_samples)

    def real_sample_runtime(self):
        return self.final_helper().real_sample_runtime()

    def startup_runtime(self, real=False):
        helper = cleanup.StartupCleanupTests()
        helper.sql = self.sql
        return helper.runtime(real=real)

    def native_panel_runtime(self):
        lua = self.final_helper().native_panel_runtime()
        lua.execute(r"""
          local get=a.GetBuildings
          a.GetBuildings=function(c)
            local bs=get(c);local read=bs.GetBuildingYieldFromGreatWorks
            bs.GetBuildingYieldFromGreatWorks=function(self,y,id)
              assert(GameInfo.Yields[y].YieldType~='YIELD_CULTURE','DEFERRED_CULTURE_GETTER_CALLED')
              return read(self,y,id)
            end
            return bs
          end
          function setNativeFive()
            nativeSix.SCIENCE=3;nativeSix.PRODUCTION=3;nativeSix.GOLD=8
            nativeSix.FOOD=3;nativeSix.FAITH=3
          end
          function readFive(mark)return SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),mark)end
          function beginReadFive()
            probe.Advance(0,a,'native-base');assert(readFive(true):find('同回合基线已记录',1,true))
            probe.Advance(0,a,'native-active');setNativeFive()
          end
        """)
        return lua

    def test_seven_domains_five_projection_and_excluded_unknown_tiers(self):
        lua = self.runtime()
        lua.execute(r"""
          local m=SPCCultureMeaningModel
          assert(m.CultureDeferred and #m.Domains==7 and #m.ActiveWriteYields==5)
          assert(table.concat(m.ActiveWriteYields,',')=='SCIENCE,PRODUCTION,GOLD,FOOD,FAITH')
          assert(table.concat(m.WriteYields,',')=='SCIENCE,PRODUCTION,GOLD,FOOD,FAITH,CULTURE')
          local f={validity='VERIFIED',identity='CULTURE',potential=4,activeStatus='KNOWN',active=4}
          local w={hasConfirmed=true,availability='KNOWN',count=2,modifierExcludedCount=0,unknownCategoryCount=0}
          local depth={validity='VERIFIED',availability='READY',value={districts={},domains={}}}
          for _,domain in ipairs({'DISTRICT_GOVERNMENT','DISTRICT_DIPLOMATIC_QUARTER'})do
            depth.value.districts[#depth.value.districts+1]={domain=domain,complete=true,pillaged=false,
              buildings={{ordinary=true,depthEligible=true,complete=true,pillaged=false,tier=nil}}}
            depth.value.domains[domain]={value='UNKNOWN'}
          end
          for n=0,10 do
            for _,d in ipairs(m.Domains)do depth.value.domains[d[1]]={value=n}end
            local p=m.Plan(f,w,depth)
            assert(p.each.SCIENCE==math.floor(n/2) and p.each.FOOD==math.floor(n/2))
            assert(p.each.PRODUCTION==2*math.floor(n/2) and p.each.GOLD==2*math.floor(1.5*n))
            assert(p.total.GOLD==p.each.GOLD*2 and p.total.FAITH==math.floor(n/2)*2)
            assert(p.each.CULTURE==0 and p.total.CULTURE==0)
            assert(p.domains.DISTRICT_GOVERNMENT==nil and p.domains.DISTRICT_DIPLOMATIC_QUARTER==nil)
          end
          -- Floor each domain before adding the two Production/Gold contributors.
          for _,d in ipairs(m.Domains)do depth.value.domains[d[1]]={value=1}end
          local p=m.Plan(f,w,depth);assert(p.each.PRODUCTION==0 and p.each.GOLD==2 and p.total.GOLD==4)
          depth.value.domains.DISTRICT_COMMERCIAL_HUB.value=3
          assert(m.Plan(f,w,depth).each.GOLD==5)
          depth.value.domains.DISTRICT_CAMPUS.value=11;assert(not pcall(m.Plan,f,w,depth))
        """)

    def test_exact_92_directory_active_ranges_and_culture_generation_rejected(self):
        lua = self.runtime()
        self.assertEqual(set(final.OWNED), set(lua.globals().SPCCultureMeaningModel.Owned.values()))
        lua.execute(r"""
          local m=SPCCultureMeaningModel;local seen={};assert(#m.Owned==92)
          for _,name in ipairs(m.Owned)do assert(not seen[name]);seen[name]=true end
          for _,y in ipairs(m.ActiveWriteYields)do
            assert(#m.Parts(y,0)==0)
            for n=1,m.FinalLimits[y]do local names=m.Parts(y,n)
              assert(#names==1 and names[1]==m.FinalValues[y][n].name and seen[names[1]])
            end
            for _,n in ipairs({-1,0.5,m.FinalLimits[y]+1,math.huge,0/0})do assert(not pcall(m.Parts,y,n))end
          end
          assert(#m.Parts('CULTURE',0)==0 and #m.FinalValues.CULTURE==10)
          for n=1,10 do
            assert(not pcall(m.Parts,'CULTURE',n))
            assert(seen[m.FinalValues.CULTURE[n].name] and m.CarrierDistrict[m.FinalValues.CULTURE[n].name]=='DISTRICT_THEATER')
          end
          assert(#m.DiagnosticParts('PAIR12')==2 and m.DiagnosticParts('SINGLE3')[1]==m.DiagnosticSingle3.name)
        """)

    def test_sql_92_644_exact_hosts_parameters_and_original_prefix(self):
        final.FinalYieldTests.test_sql_92_644_exact_hosts_flat_parameters_and_old_prefix(self)

    def test_actual_request_five_values_end_duplicate_token_and_other_city(self):
        lua = self.runtime()
        legacy.bind_actual_request(lua)
        lua.execute(r"""
          sixDepthFixture(a);local other=snapshotBuildings(b);local token=a.token
          local before=writes;local v=finalRequest('CULTURE_MEANING_READ','off')
          assert(v.mode=='OFF' and v.cultureDeferred and writes==before)
          finalRequest('CULTURE_MEANING_ADVANCE','base');assertSix(a,{})
          v=finalRequest('CULTURE_MEANING_ADVANCE','active')
          assertSix(a,{SCIENCE=3,PRODUCTION=3,GOLD=8,FOOD=3,FAITH=3})
          assert(v.culture==0 and v.totalCulture==0 and v.configuredCulture==0 and v.remainingOwned==5)
          assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
          before=writes;finalRequest('CULTURE_MEANING_ADVANCE','active');probe.Audit();assert(writes==before)
          finalRequest('CULTURE_MEANING_END','end');assertSix(a,{})
          assert(old(a,'SCIENCE') and not gwa.IsMeaningHeld(0,a) and not dialogue.meaningOverride and a.token==token)
          assertBuildingsSame(b,other);before=writes;finalRequest('CULTURE_MEANING_END','end');assert(writes==before)
        """)

    def test_same_turn_changes_only_replace_affected_final_and_excluded_domains_zero_write(self):
        pairs = (("SCIENCE", "DISTRICT_CAMPUS"), ("PRODUCTION", "DISTRICT_INDUSTRIAL_ZONE"),
                 ("GOLD", "DISTRICT_COMMERCIAL_HUB"), ("FOOD", "DISTRICT_NEIGHBORHOOD"),
                 ("FAITH", "DISTRICT_HOLY_SITE"))
        for yield_name, domain in pairs:
            with self.subTest(yield_name=yield_name):
                lua = self.runtime()
                lua.globals().changedYield = yield_name
                lua.globals().changedDomain = domain
                lua.execute(r"""
                  sixDepthFixture(a);begin();local prior=probe.lastPlan.each[changedYield];local ops={}
                  local create,remove=P.CreateBuilding,P.RemoveBuilding
                  P.CreateBuilding=function(q,id)if q.city==a and probe.IsOwnedCarrier(GameInfo.Buildings[id].BuildingType)then ops[#ops+1]='add:'..GameInfo.Buildings[id].BuildingType end;return create(q,id)end
                  P.RemoveBuilding=function(bs,id)if bs.city==a and probe.IsOwnedCarrier(GameInfo.Buildings[id].BuildingType)then ops[#ops+1]='remove:'..GameInfo.Buildings[id].BuildingType end;return remove(bs,id)end
                  sixDepths[changedDomain]=sixDepths[changedDomain]+2;fire('CityBuildingsChanged',0,1)
                  local now=probe.lastPlan.each[changedYield]
                  assert(now>prior and #ops==2 and ops[1]:find('remove:',1,true)==1 and ops[2]:find('add:',1,true)==1)
                  assert(ops[1]:find(changedYield..'_VALUE_'..prior,1,true) and ops[2]:find(changedYield..'_VALUE_'..now,1,true))
                  local before=writes;sixDepths.DISTRICT_GOVERNMENT=10;sixDepths.DISTRICT_DIPLOMATIC_QUARTER=10
                  fire('CityBuildingsChanged',0,1);probe.Audit();assert(writes==before and probe.lastPlan.each.CULTURE==0)
                """)

    def test_work_count_changes_total_once_not_carriers_and_zero_withdraws(self):
        lua = self.runtime()
        lua.execute(r"""
          sixDepthFixture(a);begin();local before=writes;a.workCount=2;confirmCollection()
          assert(writes==before and probe.lastPlan.total.GOLD==16 and probe.lastPlan.total.CULTURE==0)
          assert(probe.View(0,a).remainingOwned==5)
          for k in pairs(sixDepths)do sixDepths[k]=0 end;probe.Audit();assertSix(a,{})
        """)

    def test_unknown_retains_five_then_current_qualification_withdraws_and_recovers(self):
        lua = self.runtime()
        lua.execute(r"""
          sixDepthFixture(a);begin();local before=writes;local prior=snapshotBuildings(a)
          sixUnknown=true;probe.Audit();assert(probe.error and writes==before);assertBuildingsSame(a,prior)
          sixUnknown=false;a.active=nil;probe.Audit();assert(probe.error and writes==before);assertBuildingsSame(a,prior)
          a.active=4;probe.Audit();assert(not probe.error)
          a.active=3;probe.Audit();assertSix(a,{})
          a.active=4;probe.Audit();assertSix(a,{SCIENCE=3,PRODUCTION=3,GOLD=8,FOOD=3,FAITH=3})
        """)

    def test_reference_confirmed_loss_load_all_92_unknown_guard(self):
        final.FinalYieldTests.test_reference_change_confirmed_loss_load_all_92_and_unknown_guard(self)

    def test_culture_healthy_or_pillaged_residue_is_reported_then_normal_projection_removes(self):
        for pillaged in (False, True):
            with self.subTest(pillaged=pillaged):
                lua = self.runtime()
                lua.globals().residuePillaged = pillaged
                lua.execute(r"""
                  sixDepthFixture(a);begin();local name='BUILDING_SPC_MEANING_PROBE_CULTURE_VALUE_3'
                  local id=GameInfo.Buildings[name].Index;building(a,name,a.ds[1]);a.pillaged[id]=residuePillaged
                  local before=writes;local v=probe.View(0,a)
                  assert(v.configurationError:find('ME_DEFERRED_CULTURE_PRESENT',1,true) and v.remainingOwned==6 and writes==before)
                  probe.Audit();assert(not a.present[id]);assertSix(a,{SCIENCE=3,PRODUCTION=3,GOLD=8,FOOD=3,FAITH=3})
                  assert(probe.lastPlan.each.CULTURE==0 and not probe.View(0,a).configurationError)
                """)

    def test_culture_removal_failure_holds_old_writers_duplicate_token_new_token_recovers(self):
        for pillaged in (False, True):
            with self.subTest(pillaged=pillaged):
                lua = self.runtime()
                lua.globals().residuePillaged = pillaged
                lua.execute(r"""
                  sixDepthFixture(a);begin();local name='BUILDING_SPC_MEANING_PROBE_CULTURE_VALUE_3'
                  local id=GameInfo.Buildings[name].Index;building(a,name,a.ds[1]);a.pillaged[id]=residuePillaged
                  failRemove=id;assert(not pcall(probe.End,0,a,'culture-failed'))
                  assert(a.present[id] and gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
                  local before=writes;failRemove=nil;probe.End(0,a,'culture-failed');assert(writes==before and a.present[id])
                  probe.End(0,a,'culture-recover');assertSix(a,{})
                  assert(not a.present[id] and old(a,'SCIENCE') and not gwa.IsMeaningHeld(0,a) and not dialogue.meaningOverride)
                """)

    def test_fresh_saved_culture_read_stays_readonly_background_sample_cleans(self):
        lua = self.startup_runtime(real=True)
        lua.execute(r"""
          building(a,'BUILDING_SPC_MEANING_PROBE_CULTURE_VALUE_3',a.ds[1]);local token=a.token;local before=writes
          local v=finalRequest('CULTURE_MEANING_READ','culture-before-ready')
          assert(v.mode=='OFF' and v.remainingOwned==1 and v.cleanupStatus=='PENDING' and writes==before)
          assert(v.configurationError:find('ME_DEFERRED_CULTURE_PRESENT',1,true))
          sampleRequest(1);assert(probe.ready and probe.cleanupStatus=='CONFIRMED' and probe.mode=='OFF');emptyMeaning(a)
          assert(shared.GreatWorkFacts.ack==1 and dialogue.seq[0]==1 and hasOld(a) and hasOld(b) and a.token==token)
          before=writes;sampleRequest(2);assert(writes==before and probe.cleanupPasses==1)
        """)

    def test_all_92_startup_foreign_and_permanent_state_preserved(self):
        helper = cleanup.StartupCleanupTests()
        helper.sql = self.sql
        cleanup.StartupCleanupTests.test_all_exact_ids_foreign_scope_and_permanent_state_are_preserved(helper)

    def test_culture_off_end_failure_retains_residue_scoped_other_city_and_new_token(self):
        lua = self.startup_runtime()
        lua.execute(r"""
          local name='BUILDING_SPC_MEANING_PROBE_CULTURE_VALUE_3';building(a,name,a.ds[1])
          local id=GameInfo.Buildings[name].Index;local other=snapshotBuildings(b);failRemove=id
          assert(not pcall(probe.End,0,a,'failed-off-culture') and a.present[id] and not hasOld(a))
          failRemove=nil;local before=writes;probe.End(0,a,'failed-off-culture');assert(writes==before and a.present[id])
          probe.End(0,a,'recover-off-culture');emptyMeaning(a);assert(hasOld(a));assertBuildingsSame(b,other)
        """)

    def test_five_independent_getters_no_culture_call_and_quarantine_wording(self):
        lua = self.native_panel_runtime()
        lua.execute(r"""
          beginReadFive();local before=writes;local report=readFive(false)
          for _,e in ipairs({{'科研',3},{'生产力',3},{'金币',8},{'食物',3},{'信仰',3}})do
            local line=e[1]..'｜每件 +'..e[2]..'／本城 +'..e[2]..'｜实测差值 '..string.format('%+.2f',e[2])
            assert(report:find(line,1,true),report)
          end
          assert(not report:find('文化｜',1,true) and not report:find('文化异常',1,true))
          assert(report:find('文化追加暂隔离',1,true) and not report:find('检验与古罗马剧场',1,true))
          assert(nativeCalls==10 and globalScans==0 and writes==before)
          assert(probe.Describe(0,a):find('五产出单值',1,true))
        """)

    def test_five_reader_independent_mismatch_is_not_configuration_success(self):
        lua = self.native_panel_runtime()
        lua.execute(r"""
          beginReadFive();nativeSix.GOLD=6;nativeSix.FOOD=0;local before=writes;local report=readFive(false)
          assert(report:find('金币｜每件 +8／本城 +8｜实测差值 +6.00',1,true))
          assert(report:find('金币异常',1,true) and report:find('食物异常',1,true))
          assert(not report:find('PASS',1,true) and writes==before)
          setNativeFive();report=readFive(false);assert(not report:find('异常',1,true) and writes==before)
        """)

    def test_five_reader_depth_work_or_unknown_change_invalidates_baseline(self):
        changes = ("sixDepths.DISTRICT_CAMPUS=8;probe.Audit()",
                   "a.workCount=2;confirmCollection();nativeSix.SCIENCE=6",
                   "readerThemed=true", "readerMove=true",
                   "readerPopulation=0/0", "readerOverrides.currentActiveStatus='UNKNOWN_GOVERNOR'")
        for change in changes:
            with self.subTest(change=change):
                lua = self.native_panel_runtime()
                lua.execute("beginReadFive();" + change)
                lua.execute(r"""
                  local v=probe.View(0,a);for k,value in pairs(readerOverrides)do v[k]=value end
                  local before=writes;local report=SPCBoostGreatWorkRead.Meaning(P,a,v,false)
                  assert(report:find('差值未确认',1,true) and report:find('实测差值 未确认',1,true),report)
                  assert(not report:find('实测差值 +0.00',1,true) and report:find('当前原生',1,true) and writes==before)
                """)

    def test_five_reader_unknown_native_clears_baseline_and_uses_five_label(self):
        for bad in ("nil", "0/0", "math.huge"):
            with self.subTest(bad=bad):
                lua = self.native_panel_runtime()
                lua.execute("beginReadFive();nativeSix.SCIENCE=" + bad)
                lua.execute(r"""
                  local before=writes;local report=readFive(false)
                  assert(report:find('五产出原生读数未确认',1,true) and report:find('ME_UI_NATIVE_YIELD_UNKNOWN',1,true))
                  assert(not report:find('实测差值 +0.00',1,true))
                  setNativeFive();report=readFive(false);assert(report:find('差值未确认',1,true) and writes==before)
                """)

    def test_actual_panel_read_show_copy_one_enumeration_stale_selection_releases(self):
        lua = self.native_panel_runtime()
        lua.execute(r"""
          beginReadFive();panelPrepare('CULTURE_MEANING_READ','five-read');local before=writes
          assert(panelDisplay() and globalScans==1 and shownSix:find('文化追加暂隔离',1,true))
          assert(not shownSix:find('文化｜',1,true));local n=nativeCalls;local first=shownSix
          panelCopy();panelCopy();panelDisplay();assert(globalScans==1 and nativeCalls==n and writes==before and shownSix==first)
          assert(copiedSix:find('Modifier诊断',1,true));selectedSix=b;panelDisplay();panelCopy()
          assert(globalScans==1 and nativeCalls==n and not shownSix:find('实测差值 +3.00',1,true))
          assert(not SPCBoostGreatWorkRead.ModifierDetails('five-read') and not copiedSix:find('Modifier诊断',1,true))
        """)

    def test_modifier_allowlist_keeps_culture_residue_and_hd_while_deferred(self):
        lua = modifier.ModifierReadTests().mapped()
        old_name = "BUILDING_SPC_B060_CULTURE_P1"
        old_id = "SPC_B060_CULTURE_P1_WRITING"
        row = self.sql.execute("SELECT BuildingType,PrereqDistrict FROM Buildings WHERE BuildingType=?", (old_name,)).fetchone()
        self.assertIsNotNone(row)
        arguments = dict(self.sql.execute("SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?", (old_id,)))
        self.assertTrue(arguments)
        lua.globals().oldCultureBuilding = modifier.table(lua, {"BuildingType": row[0], "PrereqDistrict": row[1], "Index": 10001})
        lua.globals().oldCultureDefinition = modifier.table(lua, {"Id": old_id, "Arguments": arguments})
        lua.execute(r"""
          GameInfo.Buildings[oldCultureBuilding.BuildingType]=oldCultureBuilding
          GameInfo.Buildings[oldCultureBuilding.Index]=oldCultureBuilding
          local attachments={};for row in GameInfo.BuildingModifiers()do attachments[#attachments+1]=row end
          attachments[#attachments+1]={BuildingType=oldCultureBuilding.BuildingType,ModifierId=oldCultureDefinition.Id}
          GameInfo.BuildingModifiers=db(attachments,'ModifierId')
          v.finalValues=true;v.cultureDeferred=true;v.mode='OFF';v.remainingOwned=1
          definitions[2]=all_definitions.SPC_MEANING_PROBE_CULTURE_VALUE_3_WRITING
          definitions[3]=oldCultureDefinition;ids={1,2,3}
          GameInfo.Districts={[7]={DistrictType='DISTRICT_THEATER'}};district.GetType=function()return 7 end
          local report=read('culture-residue')
          assert(report:find('CULTURE_VALUE_3_WRITING',1,true) and report:find('HD_AMPHITHEATER_WRITING_CULTURE_BOOST',1,true))
          assert(report:find('本城Meaning Writing实例 1',1,true) and report:find('OFF仍观察到',1,true))
          assert(report:find('SPC_B060_CULTURE_P1_WRITING',1,true) and report:find('本城旧GWA 六产出实例 1',1,true))
          assert(SPCBoostGreatWorkRead.ModifierSummary('culture-residue'):find('异常：结束后仍有残留',1,true))
          assert(SPCBoostGreatWorkRead.ModifierDetails('culture-residue')==report and calls==1)
          read('culture-residue');assert(calls==1)
        """)

    def test_culture_deferred_flag_invalidates_same_token_modifier_cache_without_rescan(self):
        lua = modifier.ModifierReadTests().runtime()
        lua.execute(r"""
          v.finalValues=true;v.cultureDeferred=true;read('flag');assert(calls==1)
          assert(SPCBoostGreatWorkRead.ModifierDetails('flag'))
          v.cultureDeferred=false;local report=read('flag')
          assert(report:find('已释放或过期',1,true) and calls==1 and not SPCBoostGreatWorkRead.ModifierDetails('flag'))
          assert(SPCBoostGreatWorkRead.ModifierSummary('flag'):find('未确认',1,true));read('flag');assert(calls==1)
        """)

    def test_package_syntax_exact_action_imports_and_current_191(self):
        lua = LuaRuntime(unpack_returned_tuples=True)
        for path in ("CultureMeaningModel.lua", "CultureMeaningProbe.lua", "UI/BoostGreatWorkRead.lua", "UI/P0Panel.lua", "Probe.lua"):
            with self.subTest(lua=path):
                self.assertIsNotNone(lua.eval("function(s)return assert(load(s))end")((R / "Mod" / path).read_text()))
        root = ET.parse(R / "Mod/SpecializationP0.modinfo").getroot()
        self.assertEqual(root.attrib["version"], "191")
        legacy.require_meaning_imports(root)
        for node in root.findall(".//File"):
            self.assertTrue((R / "Mod" / node.text).is_file(), node.text)


if __name__ == "__main__":
    unittest.main()
