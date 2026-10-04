"""One-city Writing/Production diagnostic: targeted local evidence only.

The maintained L2 fixtures execute actual Lua and the actual request ingress.
Native UI observations are independent fixed values, never derived from carrier
configuration. They verify reporting and cannot establish Civ VI engine PASS.
External DebugGameplay is explicitly configured and opened mode=ro by the
fixture; this module does not mutate it, game configuration, or live runtime.
"""
from pathlib import Path
import os
import sys
import unittest

R = Path(os.environ.get("SPC_L2C_ROOT", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(R / "DevelopmentTests"))
import test_culture_meaning_l2c as l2c
import test_culture_meaning_probe as legacy
import test_modifier_read as modifier

FIXTURE = r"""
sampleRequest(1)
assert(shared.GreatWorkFacts.Summary(0,1).count==1)
assert(shared.GreatWorkFacts.Read(0,1).works[1].category=='GREATWORKOBJECT_WRITING')
diagDepthCalls=0;legacyAestheticDepthReads=0
-- Existing L1 reconciles on the old GWA withdrawal event and legitimately
-- consumes D. Keep that actual source consumer; forbid D in the diagnostic's
-- own qualification/projection rather than disabling another ability.
local aestheticAudit=shared.CultureAesthetic.Audit
local legacyAestheticDepth=false
shared.CultureAesthetic.Audit=function(...)
 local prior=legacyAestheticDepth;legacyAestheticDepth=true
 local ok,result=pcall(aestheticAudit,...);legacyAestheticDepth=prior
 if not ok then error(result)end;return result
end
diagOriginalDepth=shared.DistrictCompleteness.Read
shared.DistrictCompleteness.Read=function(pid,c,token)
 if c==a then
  if legacyAestheticDepth then legacyAestheticDepthReads=legacyAestheticDepthReads+1
  else diagDepthCalls=diagDepthCalls+1;error('DIAGNOSTIC_MUST_NOT_READ_D')end
 end
 return diagOriginalDepth(pid,c,token)
end
function diagAdvance(token)probe.DiagnosticAdvance(0,a,token);return probe.View(0,a,true)end
function diagRequest(action,token,city)
 meaningRequest(0,{Action=action,CityID=city or 1,Token=token})
 assert(shared.LastToken==token and shared.CultureMeaningView.token==token)
 return shared.CultureMeaningView
end
function assertDiagnostic(v,stage,amount,names)
 assert(v.diagnostic==true and v.diagnosticStage==stage,stage)
 assert(v.diagnosticExpected==amount and v.configuredProduction==amount,stage)
 for _,key in ipairs({'configuredScience','configuredGold','configuredCulture','configuredFood','configuredFaith'})do assert(v[key]==0,key)end
 local expected={};for _,name in ipairs(names or {})do expected[name]=true end
 local actual=exactMeaning(a);local count=0
 for name in pairs(actual)do assert(expected[name],name);count=count+1 end
 for name in pairs(expected)do assert(actual[name],name)end
 assert(v.remainingOwned==count and #v.diagnosticCarriers==count)
 for _,part in ipairs(v.diagnosticCarriers)do
  assert(expected[part.name] and part.yield=='PRODUCTION' and part.pillaged==false)
  assert(part.amount==(part.name:sub(-1)=='0' and 1 or 2))
 end
 if stage~='OFF' then
  local work=v.diagnosticWork
  assert(work and work.id==100 and work.type=='GREATWORK_BHASA_1')
  assert(work.building==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index and work.slot==0)
 end
 assert(diagDepthCalls==0)
end
function assertSameOwned(prior)
 local now=exactMeaning(a)
 for name in pairs(prior)do assert(now[name],name)end
 for name in pairs(now)do assert(prior[name],name)end
end
"""

NATIVE_FIXTURE = r"""
nativeObservation=10;nativeCalls=0;globalScans=0
nativeBad=nil;nativeTheme=false;nativeWorkID=100
nativeBuilding=GameInfo.Buildings.BUILDING_AMPHITHEATER.Index
nativeType='GREATWORK_BHASA_1';nativeSlots=2;nativeMissing=false
UI={GetHeadSelectedCity=function()return a end}
local get=a.GetBuildings
a.GetBuildings=function(c)
 local buildings=get(c)
 buildings.GetNumGreatWorkSlots=function(_,id)return id==nativeBuilding and nativeSlots or 0 end
 buildings.GetGreatWorkInSlot=function(_,id,slot)return slot==0 and not nativeMissing and nativeWorkID or -1 end
 buildings.GetGreatWorkTypeFromIndex=function()return nativeType end
 buildings.IsBuildingThemedCorrectly=function()return nativeTheme end
 buildings.GetBuildingYieldFromGreatWorks=function(_,yield,id)
  assert(GameInfo.Yields[yield].YieldType=='YIELD_PRODUCTION','DIAG_OTHER_YIELD_READ')
  assert(id==nativeBuilding,'DIAG_OTHER_BUILDING_READ')
  nativeCalls=nativeCalls+1
  if nativeBad=='nil' then return nil elseif nativeBad=='nan' then return 0/0
  elseif nativeBad=='inf' then return math.huge end
  -- Deliberately independent of configured(), buildings, and diagnosticExpected.
  return nativeObservation
 end
 return buildings
end
GameEffects={GetModifiers=function()globalScans=globalScans+1;return {}end}
function nativeReport(mark,token,inspect,override)
 local v=probe.View(0,a,true);v.token=token
 for key,value in pairs(override or {})do v[key]=value end
 return SPCBoostGreatWorkRead.ProductionDiagnostic(P,a,v,mark,token,SPCNetworkInput.Reference(a),inspect or false)
end
function nativeBegin()
 diagAdvance('native-baseline')
 local report=nativeReport(true,'native-baseline',false)
 assert(report:find('BASELINE',1,true) and not report:find('不记录成功基线',1,true),report)
 return report
end
"""


class ProductionDiagnosticTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.sql=legacy.database()

 @classmethod
 def tearDownClass(cls):
  cls.sql.close()

 def runtime(self):
  helper=l2c.L2CTests();helper.sql=self.sql
  lua=helper.real_sample_runtime()
  lua.execute(FIXTURE)
  return lua

 def native_runtime(self):
  lua=self.runtime();lua.globals().include('UI/BoostGreatWorkRead')
  cursor=self.sql.execute('SELECT * FROM BuildingModifiers')
  columns=[entry[0] for entry in cursor.description]
  rows=[dict(zip(columns,row)) for row in cursor]
  lua.globals().GameInfo['BuildingModifiers']=lua.globals().db(modifier.table(lua,rows),'ModifierId')
  lua.execute(NATIVE_FIXTURE)
  return lua

 def panel_runtime(self):
  lua=self.native_runtime()
  source=(R/'Mod/UI/P0Panel.lua').read_text()
  start=source.index('local function displayResponse()')
  display=source[start:source.index('-- B060 read/control requests',start)]
  start=source.index('local function copy()')
  copy=source[start:source.index("  local lines={'SPC_DIAGNOSTIC_REPORT_BEGIN'",start)]+'end\n'
  start=source.index('local function cancelMeaningReply()')
  cancellation=source[start:source.index('local function initialize()',start)]
  start=source.index('  Controls.CloseButton:RegisterCallback(')
  close=source[start:source.index('  Controls.QualificationButton:RegisterCallback(',start)]
  lua.execute(r"""
   P.VERSION='DIAGNOSTIC_PANEL_TEST'
   panelSelected=a;UI.GetHeadSelectedCity=function()return panelSelected end
   panelClears=0;panelClosed=false
   ContextPtr={ClearUpdate=function()panelClears=panelClears+1 end,SetHide=function()end}
   Mouse={eLClick=1};Controls={Window={SetHide=function(_,value)panelClosed=value end},
    OpenButton={SetHide=function()end},CloseButton={RegisterCallback=function(_,mouse,callback)panelClose=callback end}}
   function placeEntry()end
   function status(value)panelShown=value end
   function print(value)panelLogged=value end
  """)
  lua.execute(r"""
   local pendingToken,pendingAction,meaningReadReference
   local meaningResponseToken,meaningResponseText,meaningResponseReference,meaningResponseTurn
   local readings,localReport={},nil
   local pageCity,page=1,1
  """+display+copy+cancellation+close+r"""
   panelDisplay=displayResponse;panelCopy=copy;panelLoad=showRoot
   function panelPrepare(action,token)
    pendingToken=token;pendingAction=action;pageCity=1;meaningReadReference=SPCNetworkInput.Reference(a)
    local v=probe.View(0,a,true);v.token=token
    ExposedMembers.SPC_P0={Version=P.VERSION,LastToken=token,Snapshot='FIXTURE_CURRENT_RESPONSE',CultureMeaningView=v}
   end
   function panelState()return pendingToken,pendingAction,localReport,meaningResponseToken end
  """)
  return lua

 def test_actual_request_four_stages_exact_existing_parts_and_other_city(self):
  lua=self.runtime();lua.execute(r"""
   local other=snapshotBuildings(b);local originalToken=a.token
   local advance='CULTURE_MEANING_DIAGNOSTIC_ADVANCE'
   local v=diagRequest(advance,'baseline')
   assert(v.mode=='BASELINE' and not v.error)
   assertDiagnostic(v,'BASELINE',0,{})
   assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
   v=diagRequest(advance,'single');assert(v.mode=='ACTIVE' and not v.error)
   assertDiagnostic(v,'SINGLE2',2,{'BUILDING_SPC_MEANING_PROBE_PRODUCTION_1'})
   local operations={};local create,remove=P.CreateBuilding,P.RemoveBuilding
   local id1=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_0.Index
   local id2=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_1.Index
   P.RemoveBuilding=function(buildings,id)
    if buildings.city==a and (id==id1 or id==id2)then operations[#operations+1]='remove:'..id end
    return remove(buildings,id)
   end
   P.CreateBuilding=function(queue,id)
    if queue.city==a and (id==id1 or id==id2)then operations[#operations+1]='create:'..id end
    return create(queue,id)
   end
   v=diagRequest(advance,'pair');assert(v.mode=='ACTIVE' and not v.error)
   assertDiagnostic(v,'PAIR12',3,{'BUILDING_SPC_MEANING_PROBE_PRODUCTION_0','BUILDING_SPC_MEANING_PROBE_PRODUCTION_1'})
   assert(#operations==3 and operations[1]=='remove:'..id2 and operations[2]=='create:'..id1 and operations[3]=='create:'..id2)
   P.CreateBuilding=create;P.RemoveBuilding=remove
   v=diagRequest(advance,'off');assert(v.mode=='OFF' and not v.error)
   assertDiagnostic(v,'OFF',0,{})
   assert(not gwa.IsMeaningHeld(0,a) and dialogue.meaningOverride==nil and old(a,'SCIENCE'))
   assert(a.token==originalToken);assertBuildingsSame(b,other)
  """)

 def test_duplicate_tokens_conflict_and_regular_advance_cannot_mix(self):
  lua=self.runtime();lua.execute(r"""
   for _,token in ipairs({'baseline','single','pair','off'})do
    diagAdvance(token);local before=writes;local stage=probe.diagnosticStage
    diagAdvance(token);assert(writes==before and probe.diagnosticStage==stage)
    assert(not pcall(probe.DiagnosticAdvance,0,b,token) and writes==before)
    assert(not pcall(probe.Advance,0,a,token) and writes==before)
   end
   diagAdvance('baseline2');diagAdvance('single2')
   local before=writes;assert(not pcall(probe.Advance,0,a,'regular-mixed'))
   assert(probe.diagnosticStage=='SINGLE2' and writes==before and configured(a,'PRODUCTION')==2)
   probe.End(0,a,'end');before=writes;probe.End(0,a,'end');assert(writes==before)
   shared.DistrictCompleteness.Read=diagOriginalDepth
   fiveDepthFixture(a)
   probe.Advance(0,a,'regular-baseline');probe.Advance(0,a,'regular-active')
   local v=probe.View(0,a)
   assert(v.mode=='ACTIVE' and v.configuredScience==3 and v.configuredProduction==4 and v.configuredGold==8)
   assert(v.configuredFood==3 and v.configuredFaith==3 and v.configuredCulture==0)
   probe.End(0,a,'regular-end');assert(next(exactMeaning(a))==nil)
  """)

 def test_explicit_read_is_off_capable_and_performs_no_projection(self):
  lua=self.runtime();lua.execute(r"""
   local before=writes;local v=diagRequest('CULTURE_MEANING_DIAGNOSTIC_READ','off-read')
   assertDiagnostic(v,'OFF',0,{});assert(writes==before)
   diagAdvance('baseline');diagAdvance('single')
   before=writes;local action=probe.lastAction
   v=diagRequest('CULTURE_MEANING_DIAGNOSTIC_READ','active-read')
   assertDiagnostic(v,'SINGLE2',2,{'BUILDING_SPC_MEANING_PROBE_PRODUCTION_1'})
   assert(writes==before and probe.lastAction==action)
   v=diagRequest('CULTURE_MEANING_END','end')
   assertDiagnostic(v,'OFF',0,{})
   before=writes;v=diagRequest('CULTURE_MEANING_DIAGNOSTIC_READ','end-read')
   assertDiagnostic(v,'OFF',0,{});assert(writes==before)
  """)

 def test_unknown_inputs_hold_exact_projection_and_cannot_advance(self):
  for kind in ('work','active','facts'):
   with self.subTest(kind=kind):
    lua=self.runtime();lua.globals().unknownKind=kind;lua.execute(r"""
     diagAdvance('baseline');diagAdvance('single')
     local prior=exactMeaning(a);local before=writes
     local summary,read=shared.GreatWorkFacts.Summary,shared.GreatWorkFacts.Read
     if unknownKind=='work' then
      shared.GreatWorkFacts.Summary=function(pid,id)local r=summary(pid,id);if id==1 then r.availability='UNKNOWN' end;return r end
      shared.GreatWorkFacts.Read=function(pid,id)local r=read(pid,id);if id==1 then r.availability='UNKNOWN' end;return r end
     elseif unknownKind=='active' then a.active=nil else a.factsUnknown=true end
     probe.Audit();assert(probe.error and writes==before and probe.diagnosticStage=='SINGLE2');assertSameOwned(prior)
     assert(not pcall(probe.DiagnosticAdvance,0,a,'unknown') and writes==before and probe.diagnosticStage=='SINGLE2')
     assertSameOwned(prior)
     shared.GreatWorkFacts.Summary=summary;shared.GreatWorkFacts.Read=read;a.active=4;a.factsUnknown=false
     probe.Audit();assert(not probe.error and probe.diagnosticStage=='SINGLE2');assertSameOwned(prior)
     local v=diagAdvance('recovered')
     assertDiagnostic(v,'PAIR12',3,{'BUILDING_SPC_MEANING_PROBE_PRODUCTION_0','BUILDING_SPC_MEANING_PROBE_PRODUCTION_1'})
    """)

 def test_known_work_location_changes_reapply_but_unsupported_collection_withdraws(self):
  for kind in ('id','slot','building','type','count'):
   with self.subTest(kind=kind):
    lua=self.runtime();lua.globals().changeKind=kind;lua.execute(r"""
     diagAdvance('baseline');diagAdvance('single');local other=snapshotBuildings(b)
     local bid=GameInfo.Buildings.BUILDING_AMPHITHEATER.Index
     local rows={{1,bid,0,100,'GREATWORK_BHASA_1'},{2,bid,0,200,'GREATWORK_BHASA_1'}}
     if changeKind=='id' then rows[1][4]=101
     elseif changeKind=='slot' then rows[1][3]=1
     elseif changeKind=='building' then rows[1][2]=GameInfo.Buildings.BUILDING_LIBRARY.Index
     elseif changeKind=='count' then table.insert(rows,2,{1,bid,1,101,'GREATWORK_BHASA_1'})
     else
      local found
      for work in GameInfo.GreatWorks()do
       if work.GreatWorkObjectType~='GREATWORKOBJECT_WRITING' and SPCGreatWorkCatalog.Build(P).works[work.GreatWorkType] then found=work.GreatWorkType;break end
      end
      assert(found,'FIXTURE_SECOND_ELIGIBLE_WORK_MISSING');rows[1][5]=found
     end
     sampleRequest(2,rows);probe.Audit()
     local v=probe.View(0,a,true)
     assert(v.diagnosticStage=='SINGLE2' and gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0))
     if changeKind=='type' or changeKind=='count' then
      assert(next(exactMeaning(a))==nil and v.planStatus=='DIAGNOSTIC_WORK_CHANGED')
     else
      assert(configured(a,'PRODUCTION')==2 and v.diagnosticWork.id==rows[1][4])
      assert(v.diagnosticWork.building==rows[1][2] and v.diagnosticWork.slot==rows[1][3])
     end
     assertBuildingsSame(b,other);assert(diagDepthCalls==0)
    """)

 def test_end_failure_keeps_holds_duplicate_no_retry_new_token_recovers(self):
  lua=self.runtime();lua.execute(r"""
   diagAdvance('baseline');diagAdvance('single');diagAdvance('pair')
   local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_1.Index
   failRemove=id;local v=diagRequest('CULTURE_MEANING_END','failed-end')
   assert(v.error and probe.stopping and a.present[id])
   assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
   local before=writes;failRemove=nil;diagRequest('CULTURE_MEANING_END','failed-end')
   assert(writes==before and probe.stopping and a.present[id])
   v=diagRequest('CULTURE_MEANING_END','recover-end')
   assertDiagnostic(v,'OFF',0,{});assert(not v.error and not probe.stopping)
   assert(not gwa.IsMeaningHeld(0,a) and dialogue.meaningOverride==nil and old(a,'SCIENCE') and old(b,'SCIENCE'))
   before=writes;diagRequest('CULTURE_MEANING_END','recover-end');assert(writes==before)
  """)

 def test_cold_load_and_confirmed_loss_clear_all_exact_owned_without_replay(self):
  for reason in ('load','loss','reference'):
   with self.subTest(reason=reason):
    lua=self.runtime();lua.globals().exitReason=reason;lua.execute(r"""
     diagAdvance('baseline');diagAdvance('single');seedAllMeaning(a)
     local token=a.token;local other=snapshotBuildings(b)
     if exitReason=='load' then
      seedAllMeaning(b);a.owner=3;fire('LoadScreenClose')
      assert(next(exactMeaning(b))==nil)
     elseif exitReason=='loss' then
      a.owner=3;local loss={confirmed=false,targetID=a.id,origin={owner=0}}
      local before=writes;assert(not pcall(exits.CultureMeaningProbe,a,loss) and writes==before)
      loss.confirmed=true;exits.CultureMeaningProbe(a,loss);assertBuildingsSame(b,other)
     else
      a.token='new-reference';probe.Audit();assertBuildingsSame(b,other)
     end
     assert(probe.mode=='OFF' and next(exactMeaning(a))==nil)
     assert(not gwa.IsMeaningHeld(0,a) and dialogue.meaningOverride==nil)
     assert(a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and a.present[GameInfo.Buildings.BUILDING_FAIR.Index])
     if exitReason~='reference' then assert(a.token==token)end
     a.owner=0;fire('PlayerTurnActivated',0);assert(probe.mode=='OFF' and next(exactMeaning(a))==nil)
     assert(probe.View(0,a,true).diagnosticStage=='OFF' and diagDepthCalls==0)
    """)

 def test_off_view_reports_exact_owned_residue_and_pillaged_health_without_writes(self):
  lua=self.runtime();lua.execute(r"""
   seedAllMeaning(a)
   local damaged=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_PRODUCTION_1.Index;a.pillaged[damaged]=true
   local before=writes;local v=probe.View(0,a,true)
   assert(v.diagnostic and v.diagnosticStage=='OFF' and v.remainingOwned==26 and #v.diagnosticCarriers==26)
   local seen={};for _,part in ipairs(v.diagnosticCarriers)do
    assert(not seen[part.name]);seen[part.name]=true
    assert(part.yield and type(part.amount)=='number' and type(part.pillaged)=='boolean')
    if part.name=='BUILDING_SPC_MEANING_PROBE_PRODUCTION_1' then assert(part.amount==2 and part.pillaged)end
   end
   for _,name in ipairs(SPCCultureMeaningModel.Owned)do assert(seen[name],name)end
   assert(writes==before and diagDepthCalls==0)
  """)

 def test_independent_native_observation_reports_composite_and_off_mismatch(self):
  lua=self.native_runtime();lua.execute(r"""
   nativeBegin();local other=snapshotBuildings(b)
   diagAdvance('single');nativeObservation=12;local before=writes
   local report=nativeReport(false,'single',false)
   assert(report:find('SINGLE2',1,true) and report:find('预期 +2',1,true))
   assert(report:find('当前原生作品生产力 12.00',1,true) and report:find('实测差值 +2.00',1,true))
   assert(report:find('一致（仅即时读数）',1,true) and not report:find('PASS',1,true));assert(writes==before)
   diagAdvance('pair');nativeObservation=11;before=writes
   report=nativeReport(false,'pair',false)
   assert(report:find('PAIR12',1,true) and report:find('预期 +3',1,true))
   assert(report:find('当前原生作品生产力 11.00',1,true) and report:find('实测差值 +1.00',1,true))
   assert(report:find('不一致',1,true) and not report:find('一致（仅即时读数）',1,true))
   assert(not report:find('PASS',1,true) and writes==before)
   probe.End(0,a,'end');before=writes
   report=nativeReport(false,'end',false)
   assert(report:find('OFF',1,true) and report:find('预期 +0',1,true) and report:find('实测差值 +1.00',1,true))
   assert(report:find('退出读数仅作对照：旧系统恢复后，不能把此差值直接归因为Meaning残留。',1,true))
   assert(not report:find('一致（仅即时读数）',1,true) and not report:find('PASS',1,true))
   assert(writes==before and globalScans==0 and next(exactMeaning(a))==nil)
   assertBuildingsSame(b,other)
  """)

 def test_native_unknown_clears_baseline_not_successful_zero(self):
  for bad in ('nil','nan','inf'):
   with self.subTest(bad=bad):
    lua=self.native_runtime();lua.globals().badCase=bad;lua.execute(r"""
     nativeBegin();diagAdvance('single');nativeObservation=12;nativeBad=badCase
     local before=writes;local report=nativeReport(false,'bad-native',false)
     assert(report:find('ME_UI_DIAG_NATIVE_UNKNOWN',1,true),report)
     assert(not report:find('实测差值 +0.00',1,true) and not report:find('一致（仅即时读数）',1,true))
     nativeBad=nil;report=nativeReport(false,'native-recovered',false)
     assert(report:find('实测差值 未确认',1,true) and report:find('当前原生作品生产力 12.00',1,true))
     assert(writes==before and globalScans==0)
    """)

 def test_native_comparison_guards_preserve_finite_absolute_observation(self):
  changes=("nativeWorkID=101",'turn=turn+1','nativeTheme=true','nativeTheme=nil',
           'a.active=nil',"a.token='other-reference'")
  for change in changes:
   with self.subTest(change=change):
    lua=self.native_runtime();lua.execute('nativeBegin();diagAdvance("single");nativeObservation=12;'+change)
    before=lua.globals().writes;report=lua.globals().nativeReport(False,'changed',False)
    self.assertNotIn('实测差值 +2.00',report)
    self.assertNotIn('一致（仅即时读数）',report)
    self.assertEqual(lua.globals().writes,before)
    self.assertEqual(lua.globals().globalScans,0)

 def test_native_off_inspection_is_explicit_cached_and_baseline_clear_is_final(self):
  lua=self.native_runtime();lua.execute(r"""
   local before=writes;local report=nativeReport(false,'off',false)
   assert(report:find('OFF',1,true) and report:find('当前原生作品生产力 10.00',1,true))
   assert(globalScans==0 and writes==before)
   report=nativeReport(false,'inspect',true);assert(globalScans==1 and writes==before)
   local calls=nativeCalls;local prior=report
   report=nativeReport(false,'inspect',true);assert(report==prior and globalScans==1)
   nativeReport(false,'inspect-new',true);assert(globalScans==2 and writes==before)
   nativeBegin();diagAdvance('single');nativeObservation=12
   assert(nativeReport(false,'active',false):find('实测差值 +2.00',1,true))
   SPCBoostGreatWorkRead.ClearMeaningRead()
   report=nativeReport(false,'cleared',false);assert(report:find('实测差值 未确认',1,true))
   fire('LoadScreenClose');SPCBoostGreatWorkRead.ClearMeaningRead()
   report=nativeReport(false,'cold-off',false)
   assert(report:find('OFF',1,true) and report:find('实测差值 未确认',1,true))
   assert(not report:find('一致（仅即时读数）',1,true) and not report:find('PASS',1,true))
  """)

 def test_off_native_instances_are_exact_and_residue_or_unknown_is_not_withdrawal_pass(self):
  lua=self.native_runtime()
  names=['SPC_MEANING_PROBE_PRODUCTION_1_WRITING','SPC_B060_PRODUCTION_P1_WRITING',
         'SPC_MEANING_PROBE_CULTURE_0_WRITING']
  definitions={}
  for instance,name in enumerate(names,701):
   definitions[instance]={'Id':name,'Arguments':dict(self.sql.execute(
       'SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(name,)))}
  definitions[704]={'Id':'HD_AMPHITHEATER_WRITING_CULTURE_BOOST',
                    'Arguments':{'GreatWorkObjectType':'GREATWORKOBJECT_WRITING','YieldType':'YIELD_CULTURE','YieldChange':2}}
  lua.globals().nativeDefinitions=modifier.table(lua,definitions)
  lua.execute(r"""
   local districts=a.GetDistricts
   a.GetDistricts=function(c)local out=districts(c)
    out.FindID=function(_,id)for _,d in ipairs(c.ds)do if d:GetID()==id then return d end end end
    return out
   end
   CityManager.GetCity=function(pid,id)if pid==0 then return Players[0]:GetCities():FindID(id)end end
   instanceList={701,702,703,704}
   GameEffects={GetModifiers=function()globalScans=globalScans+1;return instanceList end,
    GetModifierDefinition=function(id)return nativeDefinitions[id]end,GetModifierOwner=function()return 9001 end,
    GetObjectsPlayerId=function()return 0 end,GetObjectType=function()return 'LOC_MODIFIER_OBJECT_DISTRICT' end,
    GetObjectString=function()return 'District: 2, Owner: 0, SubType: 1, SubValue: 0, City: 1' end,
    GetModifierActive=function()return true end,GetModifierSubjects=function()return {9001}end}
   local before=writes;local report=nativeReport(false,'residue-read',true)
   assert(report:find('实例ID 701',1,true) and report:find('实例ID 702',1,true) and report:find('实例ID 703',1,true))
   assert(not report:find('HD_AMPHITHEATER_WRITING_CULTURE_BOOST',1,true))
   assert(report:find('本城Meaning Writing实例 2',1,true) and report:find('本城旧GWA Production实例 1',1,true))
   assert(report:find('异常：OFF仍观察到本城Meaning实例或精确载体',1,true))
   assert(writes==before and next(exactMeaning(a))==nil and globalScans==1 and not report:find('PASS',1,true))
   GameEffects.GetObjectString=function()return 'UNOBSERVED_SCHEMA' end
   report=nativeReport(false,'unknown-read',true)
   assert(report:find('城市UNKNOWN 3',1,true) and report:find('撤销未确认',1,true))
   assert(writes==before and not report:find('本次未观察到本城Meaning Writing实例',1,true))
   instanceList={};report=nativeReport(false,'empty-read',true)
   assert(report:find('本次未观察到本城Meaning Writing实例',1,true))
   assert(writes==before and not report:find('PASS',1,true))
  """)

 def test_panel_close_or_load_cancels_late_ack_without_recreating_baseline(self):
  for boundary in ('close','load'):
   with self.subTest(boundary=boundary):
    lua=self.panel_runtime();lua.globals().panelBoundary=boundary;lua.execute(r"""
     diagAdvance('baseline');panelPrepare('CULTURE_MEANING_DIAGNOSTIC_ADVANCE','late-baseline')
     ExposedMembers.SPC_P0.LastToken=nil
     local before=writes;local native=nativeCalls
     if panelBoundary=='close' then panelClose()else panelLoad()end
     local token,action,report=panelState();assert(token==nil and action==nil and report==nil)
     ExposedMembers.SPC_P0.LastToken='late-baseline'
     assert(not panelDisplay() and nativeCalls==native and writes==before and globalScans==0)
     assert(probe.mode=='BASELINE' and gwa.IsMeaningHeld(0,a))
     diagAdvance('single');nativeObservation=12
     local report=nativeReport(false,'read-after-close',false)
     assert(report:find('实测差值 未确认',1,true) and not report:find('同回合基线已记录',1,true))
    """)

 def test_panel_cached_display_and_copy_validate_current_selection_without_rescan(self):
  lua=self.panel_runtime();lua.execute(r"""
   diagAdvance('baseline');panelPrepare('CULTURE_MEANING_DIAGNOSTIC_ADVANCE','baseline-ui')
   assert(panelDisplay());diagAdvance('single');nativeObservation=12
   panelPrepare('CULTURE_MEANING_DIAGNOSTIC_READ','read-ui');local before=writes
   assert(panelDisplay());local _,_,report=panelState()
   assert(report:find('实测差值 +2.00',1,true),report)
   local native=nativeCalls;local scans=globalScans
   assert(panelDisplay());panelCopy();panelCopy()
   assert(nativeCalls==native and globalScans==scans and writes==before)
   panelSelected=b;assert(panelDisplay());local _,_,stale=panelState()
   assert(not stale:find('实测差值 +2.00',1,true) and not stale:find('当前原生作品生产力 12.00',1,true))
   panelCopy();assert(not panelLogged:find('实测差值 +2.00',1,true))
   assert(nativeCalls==native and globalScans==scans and writes==before)
   panelSelected=a;assert(panelDisplay());local _,_,returned=panelState()
   assert(not returned:find('实测差值 +2.00',1,true),'STALE_REPORT_REPLAYED_AFTER_SELECTION_RETURN')
   assert(nativeCalls==native and globalScans==scans and writes==before)
  """)
  lua=self.panel_runtime();lua.execute(r"""
   diagAdvance('first-baseline');panelPrepare('CULTURE_MEANING_DIAGNOSTIC_ADVANCE','first-ack')
   panelSelected=b
   local before=writes;local native=nativeCalls;local scans=globalScans
   assert(panelDisplay());local _,_,foreign=panelState()
   assert(not foreign:find('同回合基线已记录',1,true))
   assert(nativeCalls==native and globalScans==scans and writes==before)
   panelSelected=a;assert(panelDisplay());local _,_,returned=panelState()
   assert(not returned:find('同回合基线已记录',1,true) and not returned:find('当前原生作品生产力',1,true))
   assert(nativeCalls==native and globalScans==scans and writes==before)
   diagAdvance('single-after-first-ack');nativeObservation=12
   local report=nativeReport(false,'explicit-after-first-ack',false)
   assert(report:find('实测差值 未确认',1,true) and not report:find('实测差值 +2.00',1,true))
  """)

 def test_packaging_and_lua_syntax(self):
  lua=self.runtime()
  for name in ['CultureMeaningProbe.lua','Gameplay.lua','UI/BoostGreatWorkRead.lua','UI/P0Panel.lua']:
   lua.execute('assert(load(...))',(R/'Mod'/name).read_text())
  panel=(R/'Mod/UI/P0Panel.lua').read_text()
  for mouse,action in [('eLClick','CULTURE_MEANING_DIAGNOSTIC_ADVANCE'),('eRClick','CULTURE_MEANING_DIAGNOSTIC_READ')]:
   self.assertIn("Controls.MeaningProbeButton:RegisterCallback(Mouse."+mouse+",function() request('"+action+"') end)",panel)
  self.assertIn('SPCBoostGreatWorkRead.ProductionDiagnostic',panel)


class RetainedModifierRegressionTests(unittest.TestCase):
 def check(self,name):
  getattr(modifier.ModifierReadTests(),name)()

 def test_token_reference_and_unknown_observations(self):
  for name in ['test_same_token_no_rescan_new_token_fresh','test_clear_does_not_replay_consumed_token',
               'test_wrong_city_owner_reference_or_token_never_scans','test_bad_enumerations_are_incomplete_not_zero',
               'test_active_nonboolean_is_unknown']:
   with self.subTest(name=name):self.check(name)

 def test_exact_mapping_subject_and_current_parent(self):
  for name in ['test_observed_district_format_and_subject_verified_with_objects',
               'test_mapping_requires_current_district_parent_and_binding',
               'test_different_city_is_not_selected_city','test_subject_unknown_type_preserved_and_bounded']:
   with self.subTest(name=name):self.check(name)


if __name__=='__main__':
 unittest.main()
