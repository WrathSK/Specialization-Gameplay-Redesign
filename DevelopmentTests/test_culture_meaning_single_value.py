"""Production-only one-city final-value probe: targeted Lua/SQL evidence.

Reuses the maintained real request, facts, Dialogue and GWA fixtures. This is
not a native engine yield, settlement, permanent-state or full cutover PASS.
Historical five-yield writer assertions remain in their original suite.
"""
from pathlib import Path
import os
import sys
import unittest

R = Path(os.environ.get("SPC_L2C_ROOT", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(R / "DevelopmentTests"))
import test_culture_meaning_l2c as l2c
import test_culture_meaning_probe as legacy

CATEGORIES = ("WRITING", "MUSIC", "SCULPTURE", "PORTRAIT", "LANDSCAPE", "RELIGIOUS", "ARTIFACT")
VALUES = [f"BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_{n}" for n in range(1, 11)]
OLD_OWNED = [f"BUILDING_SPC_MEANING_PROBE_{y}_{bit}"
             for y,bits in l2c.BITS.items() for bit in range(bits)] + [
    "BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3",
    "BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3_SCALE100",
    "BUILDING_SPC_MEANING_PROBE_PRODUCTION_SINGLE3",
]
ALL_OWNED = OLD_OWNED + VALUES

HELPERS = r"""
function seedAllFinalMeaning(c)
 for _,name in ipairs(SPCCultureMeaningModel.Owned)do building(c,name,c.ds[1])end
 assert(#SPCCultureMeaningModel.Owned==37)
 local n=0;for _ in pairs(exactMeaning(c))do n=n+1 end;assert(n==37)
end
-- Only this selected city's shared fact result is controlled. The production
-- formula is independently checked by the retained model matrix/floor examples.
function finalDepthFixture(c)
 local read=shared.DistrictCompleteness.Read
 finalIndustry=6;finalMilitary=0;finalDepthUnknown=false
 shared.DistrictCompleteness.Read=function(pid,current,token)
  if current~=c then return read(pid,current,token)end
  assert(pid==current.owner and token==current.token)
  if finalDepthUnknown then return {validity='UNKNOWN',availability='UNKNOWN'}end
  return {validity='VERIFIED',availability='READY',value={districts={},domains={
   DISTRICT_CAMPUS={value=6},DISTRICT_INDUSTRIAL_ZONE={value=finalIndustry},
   DISTRICT_ENCAMPMENT={value=finalMilitary},DISTRICT_COMMERCIAL_HUB={value=3},
   DISTRICT_HARBOR={value=3},DISTRICT_HOLY_SITE={value=6},DISTRICT_NEIGHBORHOOD={value=6}}}}
 end
end
function assertFinal(c,amount)
 local actual=exactMeaning(c);local n=0
 for name in pairs(actual)do
  n=n+1;assert(amount>0 and name=='BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_'..amount,name)
 end
 assert(n==(amount>0 and 1 or 0));assert(configured(c,'PRODUCTION')==amount)
 local v=probe.View(c.owner,c)
 assert(v.productionOnly==true and v.configuredProduction==amount and not v.configurationError)
 for _,y in ipairs({'Science','Gold','Culture','Food','Faith'})do
  assert(v['configured'..y]==0,y);if v.mode~='OFF' then assert(v[y:lower()]==0,y)end
 end
end
function finalRequest(action,token,city)
 meaningRequest(0,{Action=action,CityID=city or 1,Token=token})
 assert(shared.LastToken==token and shared.CultureMeaningView.token==token)
 return shared.CultureMeaningView
end
"""


class SingleValueTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.sql = legacy.database()

 @classmethod
 def tearDownClass(cls):
  cls.sql.close()

 def runtime(self, real_samples=False):
  helper = l2c.L2CTests(); helper.sql = self.sql
  lua = helper.runtime(real_samples=real_samples)
  lua.execute(HELPERS)
  return lua

 def real_sample_runtime(self):
  helper = l2c.L2CTests(); helper.sql = self.sql
  lua = helper.real_sample_runtime()
  lua.execute(HELPERS)
  return lua

 def test_values_exact_zero_to_ten_and_legacy_diagnostic_remain_separate(self):
  lua=self.runtime()
  self.assertEqual({lua.globals().SPCCultureMeaningModel.Owned[i] for i in range(1,38)},set(ALL_OWNED))
  lua.execute(r"""
   local m=SPCCultureMeaningModel;local seen={}
   assert(table.concat(m.ActiveWriteYields,',')=='PRODUCTION' and #m.ProductionValues==10 and #m.Owned==37)
   for _,name in ipairs(m.Owned)do assert(not seen[name]);seen[name]=true;assert(GameInfo.Buildings[name])end
   assert(#m.Parts('PRODUCTION',0)==0)
   for amount=1,10 do
    local row=m.ProductionValues[amount];assert(row.amount==amount and row.name=='BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_'..amount)
    local parts=m.Parts('PRODUCTION',amount);assert(#parts==1 and parts[1]==row.name and seen[row.name])
   end
   for _,amount in ipairs({-1,0.5,11,math.huge,0/0})do assert(not pcall(m.Parts,'PRODUCTION',amount))end
   local pair=m.DiagnosticParts('PAIR12')
   assert(#pair==2 and pair[1]=='BUILDING_SPC_MEANING_PROBE_PRODUCTION_0' and pair[2]=='BUILDING_SPC_MEANING_PROBE_PRODUCTION_1')
   assert(m.DiagnosticParts('SINGLE3')[1]==m.DiagnosticSingle3.name)
   for _,stage in ipairs({'BASELINE','SINGLE1','CLEAR1','SINGLE2','PAIR12','REMAIN2','SINGLE3','OFF'})do
    for _,name in ipairs(m.DiagnosticParts(stage))do assert(not name:find('_VALUE_',1,true))end
   end
  """)

 def test_sql_exact_old_27_plus_ten_values_and_259_attachments(self):
  self.assertEqual(len(set(ALL_OWNED)),37)
  attached_total=0
  for name in ALL_OWNED:
   row=self.sql.execute('SELECT InternalOnly,CitizenSlots,Housing,PrereqDistrict FROM Buildings WHERE BuildingType=?',(name,)).fetchone()
   self.assertEqual(row,(1,0,0,'DISTRICT_CITY_CENTER'))
   attached=self.sql.execute('SELECT ModifierId FROM BuildingModifiers WHERE BuildingType=?',(name,)).fetchall()
   self.assertEqual(len(attached),7);attached_total+=len(attached)
   categories=set()
   for (mid,) in attached:
    self.assertEqual(self.sql.execute('SELECT ModifierType FROM Modifiers WHERE ModifierId=?',(mid,)).fetchone()[0],'MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD')
    args=dict(self.sql.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(mid,)))
    categories.add(args['GreatWorkObjectType'])
    if name in VALUES:
     self.assertEqual(set(args),{'GreatWorkObjectType','YieldType','YieldChange'})
     self.assertEqual(args['YieldType'],'YIELD_PRODUCTION')
     self.assertEqual(float(args['YieldChange']),VALUES.index(name)+1)
   self.assertEqual(categories,{'GREATWORKOBJECT_'+category for category in CATEGORIES})
  self.assertEqual(attached_total,259)

 def test_actual_request_zero_baseline_active_end_only_one_final_value(self):
  lua=self.runtime();legacy.bind_actual_request(lua);lua.execute(r"""
   finalDepthFixture(a);local other=snapshotBuildings(b);local token=a.token
   local before=writes;local v=finalRequest('CULTURE_MEANING_READ','off-read')
   assert(v.mode=='OFF' and writes==before);assertFinal(a,0)
   v=finalRequest('CULTURE_MEANING_ADVANCE','baseline');assert(v.mode=='BASELINE');assertFinal(a,0)
   assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
   v=finalRequest('CULTURE_MEANING_ADVANCE','active');assert(v.mode=='ACTIVE' and v.production==3 and v.totalProduction==3)
   assertFinal(a,3);assert(probe.lastPlan.each.GOLD==8 and probe.lastPlan.each.SCIENCE==3)
   v=finalRequest('CULTURE_MEANING_ADVANCE','end');assert(v.mode=='OFF');assertFinal(a,0)
   assert(old(a,'SCIENCE') and not gwa.IsMeaningHeld(0,a) and dialogue.meaningOverride==nil)
   assert(a.token==token);assertBuildingsSame(b,other)
  """)

 def test_same_turn_three_four_three_zero_replaces_exact_value_without_rebuilding_same(self):
  lua=self.runtime();lua.execute(r"""
   finalDepthFixture(a);local other=snapshotBuildings(b);begin();assertFinal(a,3)
   local ops={};local create,remove=P.CreateBuilding,P.RemoveBuilding
   local ids={};for n,row in ipairs(SPCCultureMeaningModel.ProductionValues)do ids[GameInfo.Buildings[row.name].Index]=n end
   P.CreateBuilding=function(q,id)if q.city==a and ids[id]then ops[#ops+1]='add'..ids[id]end;return create(q,id)end
   P.RemoveBuilding=function(bs,id)if bs.city==a and ids[id]then ops[#ops+1]='remove'..ids[id]end;return remove(bs,id)end
   finalMilitary=3;fire('CityBuildingsChanged',0,1);assertFinal(a,4)
   assert(table.concat(ops,',')=='remove3,add4');ops={}
   local before=writes;fire('CityBuildingsChanged',0,1);probe.Audit();assert(writes==before and #ops==0)
   finalMilitary=0;fire('CityBuildingsChanged',0,1);assertFinal(a,3)
   assert(table.concat(ops,',')=='remove4,add3');ops={}
   finalIndustry=1;finalMilitary=1;fire('CityBuildingsChanged',0,1);assertFinal(a,0)
   assert(table.concat(ops,',')=='remove3')
   assert(probe.lastPlan.each.PRODUCTION==0 and probe.lastPlan.total.PRODUCTION==0)
   assert(probe.lastPlan.domains.DISTRICT_INDUSTRIAL_ZONE.rawEach==0.5 and probe.lastPlan.domains.DISTRICT_ENCAMPMENT.rawEach==0.5)
   assertBuildingsSame(b,other)
  """)

 def test_actual_projection_all_ten_values_and_w_does_not_enter_carrier_amount(self):
  lua=self.runtime();lua.execute(r"""
   finalDepthFixture(a);begin()
   for amount=0,10 do
    finalIndustry=2*math.min(amount,5);finalMilitary=2*math.max(amount-5,0)
    fire('CityBuildingsChanged',0,1);assertFinal(a,amount)
    assert(probe.lastPlan.each.PRODUCTION==amount and probe.lastPlan.total.PRODUCTION==amount)
   end
   finalIndustry=6;finalMilitary=0;fire('CityBuildingsChanged',0,1);assertFinal(a,3)
   local before=probe.changes;a.workCount=2;confirmCollection()
   assertFinal(a,3);assert(probe.lastPlan.count==2 and probe.lastPlan.each.PRODUCTION==3 and probe.lastPlan.total.PRODUCTION==6)
   assert(probe.changes==before)
   a.workCount=0;confirmCollection();assertFinal(a,0)
   a.workCount=1;confirmCollection();assertFinal(a,3)
  """)

 def test_real_shared_building_and_pillage_active_changes_in_same_turn(self):
  lua=self.runtime();lua.execute(r"""
   local industrial=district(a,10,'DISTRICT_INDUSTRIAL_ZONE');local other=snapshotBuildings(b)
   begin();assertFinal(a,0)
   building(a,'BUILDING_WORKSHOP',industrial);fire('CityBuildingsChanged',0,1)
   -- This configured HD expansion DB has Workshop=T2 and Factory=T3.
   assert(probe.lastPlan.domains.DISTRICT_INDUSTRIAL_ZONE.value==2);assertFinal(a,1)
   building(a,'BUILDING_FACTORY',industrial);fire('CityBuildingsChanged',0,1)
   assert(probe.lastPlan.domains.DISTRICT_INDUSTRIAL_ZONE.value==5);assertFinal(a,2)
   a.pillaged[GameInfo.Buildings.BUILDING_FACTORY.Index]=true;fire('BuildingPillaged',0,1);assertFinal(a,1)
   a.pillaged[GameInfo.Buildings.BUILDING_FACTORY.Index]=false;fire('BuildingRepaired',0,1);assertFinal(a,2)
   a.active=3;fire('GovernorChanged',0);assertFinal(a,0)
   a.active=4;fire('GovernorEstablished',0);assertFinal(a,2)
   local before=writes;probe.Audit();probe.Audit();assert(writes==before);assertBuildingsSame(b,other)
  """)

 def test_unknown_inputs_retain_confirmed_value_reference_change_exits(self):
  lua=self.runtime();lua.execute(r"""
   finalDepthFixture(a);begin();assertFinal(a,3)
   local before=writes
   a.worksUnknown=true;probe.Audit();assert(probe.error:find('ME_WORKS_UNKNOWN') and writes==before);assertFinal(a,3)
   a.worksUnknown=false;a.active=nil;probe.Audit();assert(probe.error:find('ME_ACTIVE_UNKNOWN') and writes==before);assertFinal(a,3)
   a.active=4;a.factsUnknown=true;probe.Audit();assert(probe.error:find('ME_FACT_UNKNOWN') and writes==before);assertFinal(a,3)
   a.factsUnknown=false;finalDepthUnknown=true;probe.Audit();assert(probe.error:find('ME_DEPTH_UNKNOWN') and writes==before);assertFinal(a,3)
   finalDepthUnknown=false;probe.Audit();assert(not probe.error);assertFinal(a,3)
   a.token='another-persistent-city';probe.Audit();assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and not gwa.IsMeaningHeld(0,a))
  """)

 def test_confirmed_loss_and_load_clear_all_37_exact_ids_without_replay(self):
  for boundary in ('loss','load'):
   with self.subTest(boundary=boundary):
    lua=self.runtime();lua.globals().boundary=boundary;lua.execute(r"""
     finalDepthFixture(a);begin();seedAllFinalMeaning(a);local other=snapshotBuildings(b);local token=a.token
     a.owner=3
     if boundary=='loss' then
      local loss={confirmed=false,targetID=a.id,origin={owner=0}};local before=writes
      assert(not pcall(exits.CultureMeaningProbe,a,loss) and writes==before)
      loss.confirmed=true;loss.targetID=b.id;assert(not pcall(exits.CultureMeaningProbe,a,loss) and writes==before)
      loss.targetID=a.id;exits.CultureMeaningProbe(a,loss);assertBuildingsSame(b,other)
      before=writes;exits.CultureMeaningProbe(a,loss);assert(writes==before)
     else
      seedAllFinalMeaning(b);fire('LoadScreenClose');assert(next(exactMeaning(b))==nil)
     end
     assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and not gwa.IsMeaningHeld(0,a) and dialogue.meaningOverride==nil)
     assert(a.token==token and a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and a.present[GameInfo.Buildings.BUILDING_FAIR.Index])
     a.owner=0;fire('PlayerTurnActivated',0);assert(probe.mode=='OFF' and next(exactMeaning(a))==nil)
    """)

 def test_view_rejects_legacy_bits_nonproduction_and_mixed_final_residue_without_writes(self):
  for name in ['BUILDING_SPC_MEANING_PROBE_PRODUCTION_0','BUILDING_SPC_MEANING_PROBE_SCIENCE_0','BUILDING_SPC_MEANING_PROBE_CULTURE_0',VALUES[0],VALUES[1]]:
   with self.subTest(name=name):
    lua=self.runtime();lua.globals().residue=name;lua.execute(r"""
     finalDepthFixture(a);begin();assertFinal(a,3);building(a,residue,a.ds[1]);local before=writes
     local v=probe.View(0,a)
     assert(v.configurationError and v.configuredProduction==nil and writes==before)
     probe.End(0,a,'residue-end');assertFinal(a,0)
    """)

 def test_create_failure_and_exit_failure_preserve_holds_until_exact_recovery(self):
  for after_write in (False,True):
   with self.subTest(after_write=after_write):
    lua=self.runtime();lua.globals().afterWrite=after_write;lua.execute(r"""
     finalDepthFixture(a);probe.Advance(0,a,'baseline')
     local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_3.Index;local create=P.CreateBuilding
     P.CreateBuilding=function(q,i)if i==id then if afterWrite then create(q,i);error('NATIVE_AFTER_WRITE')else return end end;return create(q,i)end
     assert(not pcall(probe.Advance,0,a,'failed-create') and probe.error)
     assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE') and old(b,'SCIENCE'))
     P.CreateBuilding=create;probe.End(0,a,'recover-create');assertFinal(a,0)
     probe.Advance(0,a,'baseline2');probe.Advance(0,a,'active2');assertFinal(a,3)
     failRemove=id;assert(not pcall(probe.End,0,a,'failed-end') and probe.stopping and probe.error)
     assert(a.present[id] and gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
     local before=writes;failRemove=nil;probe.End(0,a,'failed-end');assert(writes==before and a.present[id])
     probe.End(0,a,'recover-end');assertFinal(a,0);assert(old(a,'SCIENCE') and old(b,'SCIENCE'))
    """)

 def test_failed_value_replacement_never_adds_new_or_releases_old_writer(self):
  lua=self.runtime();legacy.bind_actual_request(lua);lua.execute(r"""
   finalDepthFixture(a);finalRequest('CULTURE_MEANING_ADVANCE','baseline');finalRequest('CULTURE_MEANING_ADVANCE','active')
   local id3=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_3.Index
   local id4=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_4.Index
   finalMilitary=3;failRemove=id3;fire('CityBuildingsChanged',0,1)
   assert(probe.error and a.present[id3] and not a.present[id4] and gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0))
   failRemove=nil;probe.Audit();assertFinal(a,4);assert(not probe.error)
   probe.End(0,a,'replace-end');assertFinal(a,0)
  """)

 def test_load_failure_retains_holds_and_blocks_replay_until_exact_cleanup(self):
  lua=self.runtime();lua.execute(r"""
   finalDepthFixture(a);begin();local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_3.Index
   failRemove=id;fire('LoadScreenClose')
   assert(not probe.ready and probe.resetFailed and probe.error and a.present[id])
   assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0))
   local before=writes;fire('PlayerTurnActivated',0);assert(writes==before and a.present[id])
   failRemove=nil;fire('LoadScreenClose');assert(probe.ready and not probe.resetFailed and probe.mode=='OFF');assertFinal(a,0)
  """)

 def test_duplicate_tokens_zero_write_and_switching_fixture_is_scoped(self):
  lua=self.runtime();legacy.bind_actual_request(lua);lua.execute(r"""
   finalDepthFixture(a);finalRequest('CULTURE_MEANING_ADVANCE','baseline');finalRequest('CULTURE_MEANING_ADVANCE','active')
   local before=writes;finalRequest('CULTURE_MEANING_ADVANCE','active');assert(writes==before);assertFinal(a,3)
   local before=writes;finalRequest('CULTURE_MEANING_READ','read');assert(writes==before)
   finalRequest('CULTURE_MEANING_ADVANCE','other-baseline',2)
   assert(next(exactMeaning(a))==nil and old(a,'SCIENCE') and not gwa.IsMeaningHeld(0,a))
   assert(probe.mode=='BASELINE' and gwa.IsMeaningHeld(0,b));probe.End(0,b,'other-end')
   assert(probe.mode=='OFF' and next(exactMeaning(b))==nil and old(b,'SCIENCE'))
  """)

 def test_reentrant_building_notifications_are_bounded_and_keep_same_turn_real_changes(self):
  lua=self.runtime();lua.execute(r"""
   finalDepthFixture(a);local create,remove=P.CreateBuilding,P.RemoveBuilding
   P.CreateBuilding=function(q,id)create(q,id);fire('CityBuildingsChanged',q.city.owner,q.city.id)end
   P.RemoveBuilding=function(bs,id)remove(bs,id);fire('CityBuildingsChanged',bs.city.owner,bs.city.id)end
   local other=snapshotBuildings(b);begin();assertFinal(a,3)
   finalMilitary=3;fire('CityBuildingsChanged',0,1);assertFinal(a,4)
   assert(not probe.busy and not probe.advancing and not probe.deferred and not dialogue.busy)
   local before=writes;probe.Audit();assert(writes==before)
   probe.End(0,a,'sync-end');assertFinal(a,0);assertBuildingsSame(b,other)
  """)

 def test_real_sample_pair_order_unknown_and_next_turn_recovery_use_final_value(self):
  lua=self.real_sample_runtime();lua.execute(r"""
   finalDepthFixture(a);sampleRequest(1);meaningAction('CULTURE_MEANING_ADVANCE','baseline');meaningAction('CULTURE_MEANING_ADVANCE','active');assertFinal(a,3)
   local paired=probe.CollectionConfirmed;local pairCount=0
   probe.CollectionConfirmed=function(...)pairCount=pairCount+1;return paired(...)end
   local before=probe.changes;sampleRequest(1,twoWorks())
   assert(pairCount==0 and probe.lastPlan.count==1 and probe.changes==before)
   local bad=samplePacket(2,twoWorks());bad.Generation=bad.Generation+1;meaningRequest(0,bad)
   assert(pairCount==0 and probe.lastPlan.count==1 and probe.View(0,a).dialoguePercent==nil);assertFinal(a,3)
   sampleRequest(3,twoWorks());assert(pairCount==1 and not probe.error and probe.lastPlan.count==2 and probe.lastPlan.total.PRODUCTION==6);assertFinal(a,3)
   turn=turn+1;fire('PlayerTurnActivated',0)
   assert(probe.error and probe.mode=='ACTIVE' and probe.View(0,a).dialoguePercent==nil);assertFinal(a,3)
   sampleRequest(4,twoWorks());assert(not probe.error and probe.View(0,a).dialoguePercent==0);assertFinal(a,3)
  """)

 def native_panel_runtime(self):
  helper=l2c.L2CTests();helper.sql=self.sql
  lua=helper.reader_runtime();lua.execute(HELPERS)
  cursor=self.sql.execute('SELECT * FROM BuildingModifiers');columns=[r[0] for r in cursor.description]
  rows=[dict(zip(columns,row)) for row in cursor]
  lua.globals().GameInfo['BuildingModifiers']=lua.globals().db(legacy.ae.lua_table(lua,rows),'ModifierId')
  source=(R/'Mod/UI/P0Panel.lua').read_text()
  start=source.index('local function displayResponse()')
  display=source[start:source.index('-- B060 read/control requests',start)]
  copy=source[source.index('local function copy()'):source.index("  local lines={'SPC_DIAGNOSTIC_REPORT_BEGIN'")]+"end\n"
  lua.execute(r"""
   finalDepthFixture(a);selectedFinal=a;nativeProduction=10;finalNativeCalls=0;finalGlobalScans=0
   UI={GetHeadSelectedCity=function()return selectedFinal end}
   local getter=a.GetBuildings
   a.GetBuildings=function(c)local bs=getter(c)
    bs.GetBuildingYieldFromGreatWorks=function(_,yield,id)
     assert(GameInfo.Yields[yield].YieldType=='YIELD_PRODUCTION','NONPRODUCTION_NATIVE_READ')
     assert(id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index);finalNativeCalls=finalNativeCalls+1
     return nativeProduction -- independent of configured(), Plan, and expected amount.
    end
    return bs
   end
   GameEffects={GetModifiers=function()finalGlobalScans=finalGlobalScans+1;return {}end}
   P.VERSION='B161_FINAL_VALUE_PANEL';readings={};page=1;pageCity=1;localReport=nil
   function status(value)finalPanelShown=value end
   function print(value)finalPanelCopied=value end
   function finalPanelPrepare(action,token)
    pendingAction=action;pendingToken=token;meaningReadReference=SPCNetworkInput.Reference(a)
    local v=probe.View(0,a);v.token=token
    ExposedMembers.SPC_P0={Version=P.VERSION,LastToken=token,Snapshot='FINAL_VALUE_CURRENT_ACK',CultureMeaningView=v}
   end
  """+display+copy+r"""
   finalPanelDisplay=displayResponse;finalPanelCopy=copy
  """)
  return lua

 def test_independent_production_native_values_do_not_turn_configuration_into_pass(self):
  lua=self.native_panel_runtime();lua.execute(r"""
   probe.Advance(0,a,'native-baseline')
   local v=probe.View(0,a);local baseline=SPCBoostGreatWorkRead.Meaning(P,a,v,true)
   assert(baseline:find('同回合基线已记录',1,true))
   probe.Advance(0,a,'native-active');nativeProduction=11;local before=writes
   local report=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
   assert(report:find('生产力｜每件 +3／本城 +3｜实测差值 +1.00',1,true),report)
   assert(not report:find('PASS',1,true) and not report:find('科研｜',1,true))
   nativeProduction=13;report=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
   assert(report:find('生产力｜每件 +3／本城 +3｜实测差值 +3.00',1,true),report)
   assert(writes==before and finalGlobalScans==0 and not report:find('PASS',1,true))
  """)

 def test_actual_panel_explicit_read_enumerates_once_and_selection_change_never_replays(self):
  lua=self.native_panel_runtime();lua.execute(r"""
   probe.Advance(0,a,'panel-baseline');finalPanelPrepare('CULTURE_MEANING_ADVANCE','panel-baseline')
   assert(finalPanelDisplay() and finalGlobalScans==0)
   probe.Advance(0,a,'panel-active');nativeProduction=13
   finalPanelPrepare('CULTURE_MEANING_ADVANCE','panel-active');assert(finalPanelDisplay() and finalGlobalScans==0)
   finalPanelPrepare('CULTURE_MEANING_READ','panel-read');local before=writes
   assert(finalPanelDisplay() and finalGlobalScans==1)
   assert(finalPanelShown:find('生产力｜每件 +3／本城 +3｜实测差值 +3.00',1,true),finalPanelShown)
   local native=finalNativeCalls
   assert(finalPanelDisplay());finalPanelCopy();finalPanelCopy()
   assert(finalGlobalScans==1 and finalNativeCalls==native and writes==before)
   selectedFinal=b;assert(finalPanelDisplay());finalPanelCopy()
   assert(not finalPanelShown:find('实测差值 +3.00',1,true) and not finalPanelCopied:find('实测差值 +3.00',1,true))
   assert(finalGlobalScans==1 and finalNativeCalls==native and writes==before)
   selectedFinal=a;assert(finalPanelDisplay())
   assert(not finalPanelShown:find('实测差值 +3.00',1,true) and finalGlobalScans==1 and finalNativeCalls==native)
   probe.End(0,a,'panel-end');finalPanelPrepare('CULTURE_MEANING_END','panel-end')
   assert(finalPanelDisplay() and finalGlobalScans==1);assertFinal(a,0)
   finalPanelPrepare('CULTURE_MEANING_READ','panel-off-read');before=writes
   assert(finalPanelDisplay() and finalGlobalScans==2 and writes==before)
  """)

 # Source methods have no obsolete five-yield projection assertions.
 test_seven_domain_mapping_floor_matrix_and_cap = l2c.L2CTests.test_seven_domain_mapping_floor_matrix_and_cap
 test_floor_before_same_yield_sum_and_w_counterexamples = l2c.L2CTests.test_floor_before_same_yield_sum_and_w_counterexamples
 test_k_cold_pair = legacy.MeaningProbeTests.test_real_sample_request_cold_c00_uses_both_receivers
 test_k_duplicate_sequence = legacy.MeaningProbeTests.test_real_sample_duplicate_sequence_does_not_reinterpret_changed_payload
 test_old_writer_withdrawal_failure = legacy.MeaningProbeTests.test_old_withdrawal_failure_does_not_enable_new
 test_ingress_rejects_foreign_and_invalid_token = legacy.MeaningProbeTests.test_actual_request_invalid_or_foreign_ingress_does_not_run_probe
 test_import_registry = legacy.MeaningProbeTests.test_import_registry_rejects_each_missing_action_import


if __name__ == '__main__':
 unittest.main()
