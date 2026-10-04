"""B163 current six-yield final-value gate; local evidence, not native PASS.

Historical Production-only and bit-suite assertions are retained unchanged.
External SQL database is read-only; only an in-memory copy is rebuilt.
"""
import unittest
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
import test_culture_meaning_probe as legacy
import test_culture_meaning_l2c as l2c
import test_culture_meaning_single_value as single
import test_modifier_read as modifier
R=Path(__file__).resolve().parents[1]
LIMITS={'SCIENCE':5,'PRODUCTION':10,'GOLD':30,'FOOD':5,'FAITH':5,'CULTURE':10}
NEW=[f'BUILDING_SPC_MEANING_PROBE_{y}_VALUE_{n}' for y,limit in LIMITS.items() if y!='PRODUCTION' for n in range(1,limit+1)]
OWNED=single.ALL_OWNED+NEW
HELPERS=r"""
function seedAllFinalMeaning(c)
 for _,name in ipairs(SPCCultureMeaningModel.Owned)do building(c,name,c.ds[1])end
 assert(#SPCCultureMeaningModel.Owned==92)
 local n=0;for _ in pairs(exactMeaning(c))do n=n+1 end;assert(n==92)
end
function finalRequest(action,token,city)
 meaningRequest(0,{Action=action,CityID=city or 1,Token=token})
 assert(shared.LastToken==token and shared.CultureMeaningView.token==token)
 return shared.CultureMeaningView
end
function sixDepthFixture(c)
 local read=shared.DistrictCompleteness.Read
 sixDepths={DISTRICT_CAMPUS=6,DISTRICT_INDUSTRIAL_ZONE=6,DISTRICT_ENCAMPMENT=0,
 DISTRICT_COMMERCIAL_HUB=3,DISTRICT_HARBOR=3,DISTRICT_HOLY_SITE=6,
 DISTRICT_NEIGHBORHOOD=6,DISTRICT_GOVERNMENT=3,DISTRICT_DIPLOMATIC_QUARTER=3}
 sixUnknown=false
 shared.DistrictCompleteness.Read=function(pid,current,token)
  if current~=c then return read(pid,current,token)end
  assert(pid==current.owner and token==current.token)
  if sixUnknown then return {validity='UNKNOWN',availability='UNKNOWN'}end
  local domains={};for k,n in pairs(sixDepths)do domains[k]={value=n}end
  return {validity='VERIFIED',availability='READY',value={districts={},domains=domains}}
 end
end
function assertSix(c,expected)
 local actual=exactMeaning(c);local count=0
 for name in pairs(actual)do
  count=count+1;local y,n=name:match('^BUILDING_SPC_MEANING_PROBE_([A-Z]+)_VALUE_(%d+)$')
  assert(y and expected[y]==tonumber(n),name)
 end
 local total=0
 for _,y in ipairs(SPCCultureMeaningModel.WriteYields)do
  local n=expected[y] or 0;assert(configured(c,y)==n,y)
  if n>0 then total=total+1 end
 end
 assert(count==total)
 local v=probe.View(c.owner,c);assert(v.finalValues and not v.productionOnly and not v.configurationError)
end
"""
class FinalYieldTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.sql=legacy.database()
 @classmethod
 def tearDownClass(cls): cls.sql.close()
 def runtime(self,real_samples=False):
  helper=l2c.L2CTests();helper.sql=self.sql
  lua=helper.runtime(real_samples=real_samples);lua.execute(HELPERS)
  return lua
 def real_sample_runtime(self):
  helper=l2c.L2CTests();helper.sql=self.sql
  lua=helper.real_sample_runtime();lua.execute(HELPERS);return lua
 def test_exact_ranges_zero_and_invalid_values_legacy_controls_retained(self):
  lua=self.runtime();self.assertEqual(set(OWNED),set(lua.globals().SPCCultureMeaningModel.Owned.values()))
  lua.execute(r"""
   local m=SPCCultureMeaningModel;assert(#m.Owned==92 and #m.Domains==9 and #m.ActiveWriteYields==6)
   local seen={};for _,name in ipairs(m.Owned)do assert(not seen[name]);seen[name]=true end
   for _,y in ipairs(m.WriteYields)do
    assert(#m.Parts(y,0)==0)
    for n=1,m.FinalLimits[y]do local p=m.Parts(y,n);assert(#p==1 and p[1]==m.FinalValues[y][n].name and seen[p[1]])end
    for _,n in ipairs({-1,0.5,m.FinalLimits[y]+1,math.huge,0/0})do assert(not pcall(m.Parts,y,n))end
   end
   assert(#m.DiagnosticParts('PAIR12')==2 and m.DiagnosticParts('SINGLE3')[1]==m.DiagnosticSingle3.name)
  """)
 def test_sql_92_644_exact_hosts_flat_parameters_and_old_prefix(self):
  total=0
  for name in OWNED:
   with self.subTest(name=name):
    final=name in NEW or name in single.VALUES
    y,n=(name.split('_VALUE_') if final else (None,None))
    y=y.removeprefix('BUILDING_SPC_MEANING_PROBE_') if y else None
    host='DISTRICT_THEATER' if y=='CULTURE' else 'DISTRICT_CITY_CENTER'
    self.assertEqual(self.sql.execute('SELECT InternalOnly,CitizenSlots,Housing,PrereqDistrict FROM Buildings WHERE BuildingType=?',(name,)).fetchone(),(1,0,0,host))
    mids=self.sql.execute('SELECT ModifierId FROM BuildingModifiers WHERE BuildingType=?',(name,)).fetchall();self.assertEqual(len(mids),7);total+=len(mids)
    for (mid,) in mids:
     self.assertEqual(self.sql.execute('SELECT ModifierType FROM Modifiers WHERE ModifierId=?',(mid,)).fetchone()[0],'MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD')
     if final:
      args=dict(self.sql.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(mid,)))
      self.assertEqual(set(args),{'GreatWorkObjectType','YieldType','YieldChange'});self.assertEqual(args['YieldType'],'YIELD_'+y);self.assertEqual(float(args['YieldChange']),int(n))
  self.assertEqual(total,644)
  original=subprocess.check_output(['git','show','b9c6bb7:Mod/Data/CultureMeaningProbe.sql'],cwd=R)
  self.assertTrue((R/'Mod/Data/CultureMeaningProbe.sql').read_bytes().startswith(original))
 def test_nine_domain_floor_before_sum_and_w_matrix(self):
  lua=self.runtime();lua.execute(r"""
   local m=SPCCultureMeaningModel
   local f={validity='VERIFIED',identity='CULTURE',potential=4,activeStatus='KNOWN',active=4}
   local w={hasConfirmed=true,availability='KNOWN',count=2,modifierExcludedCount=0,unknownCategoryCount=0}
   for n=0,10 do
    local domains={};for _,d in ipairs(m.Domains)do domains[d[1]]={value=n}end
    local p=m.Plan(f,w,{validity='VERIFIED',availability='READY',value={districts={},domains=domains}})
    assert(p.each.CULTURE==2*math.floor(n/2) and p.each.PRODUCTION==2*math.floor(n/2))
    assert(p.each.GOLD==2*math.floor(1.5*n) and p.each.SCIENCE==math.floor(n/2))
    assert(p.total.CULTURE==p.each.CULTURE*2 and p.total.GOLD==p.each.GOLD*2)
   end
   sixDepthFixture(a);begin();assertSix(a,{SCIENCE=3,PRODUCTION=3,GOLD=8,FOOD=3,FAITH=3,CULTURE=2})
   sixDepths.DISTRICT_GOVERNMENT=1;sixDepths.DISTRICT_DIPLOMATIC_QUARTER=1
   sixDepths.DISTRICT_INDUSTRIAL_ZONE=1;sixDepths.DISTRICT_ENCAMPMENT=1
   probe.Audit();assert(probe.lastPlan.each.CULTURE==0 and probe.lastPlan.each.PRODUCTION==0 and probe.lastPlan.each.GOLD==8)
  """)
 def test_actual_request_six_baseline_active_end_idempotent_and_other_city(self):
  lua=self.runtime();legacy.bind_actual_request(lua);lua.execute(r"""
   sixDepthFixture(a);local other=snapshotBuildings(b);local token=a.token
   local before=writes;local v=finalRequest('CULTURE_MEANING_READ','off');assert(v.mode=='OFF' and writes==before)
   finalRequest('CULTURE_MEANING_ADVANCE','base');assertSix(a,{})
   finalRequest('CULTURE_MEANING_ADVANCE','active');assertSix(a,{SCIENCE=3,PRODUCTION=3,GOLD=8,FOOD=3,FAITH=3,CULTURE=2})
   assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
   before=writes;finalRequest('CULTURE_MEANING_ADVANCE','active');probe.Audit();assert(writes==before)
   finalRequest('CULTURE_MEANING_END','end');assertSix(a,{})
   assert(old(a,'SCIENCE') and not gwa.IsMeaningHeld(0,a) and not dialogue.meaningOverride and a.token==token)
   assertBuildingsSame(b,other)
  """)
 def test_same_turn_only_changed_value_replaced_before_add_no_rebuild(self):
  for y,domain in [('SCIENCE','DISTRICT_CAMPUS'),('GOLD','DISTRICT_COMMERCIAL_HUB'),('FOOD','DISTRICT_NEIGHBORHOOD'),('FAITH','DISTRICT_HOLY_SITE'),('CULTURE','DISTRICT_GOVERNMENT'),('PRODUCTION','DISTRICT_INDUSTRIAL_ZONE')]:
   with self.subTest(y=y):
    lua=self.runtime();lua.globals().changedYield=y;lua.globals().changedDomain=domain
    lua.execute(r"""
     sixDepthFixture(a);begin();local old=probe.lastPlan.each[changedYield];local ops={}
     local create,remove=P.CreateBuilding,P.RemoveBuilding
     P.CreateBuilding=function(q,id)if q.city==a and probe.IsOwnedCarrier(GameInfo.Buildings[id].BuildingType)then ops[#ops+1]='add:'..GameInfo.Buildings[id].BuildingType end;return create(q,id)end
     P.RemoveBuilding=function(bs,id)if bs.city==a and probe.IsOwnedCarrier(GameInfo.Buildings[id].BuildingType)then ops[#ops+1]='remove:'..GameInfo.Buildings[id].BuildingType end;return remove(bs,id)end
     sixDepths[changedDomain]=sixDepths[changedDomain]+2;fire('CityBuildingsChanged',0,1)
     local new=probe.lastPlan.each[changedYield];assert(new>old and #ops==2 and ops[1]:find('remove:',1,true)==1 and ops[2]:find('add:',1,true)==1)
     assert(ops[1]:find(changedYield..'_VALUE_'..old,1,true));assert(ops[2]:find(changedYield..'_VALUE_'..new,1,true))
     local before=writes;probe.Audit();assert(writes==before)
    """)
 def test_w_changes_total_not_carrier_count_and_zero_removes(self):
  lua=self.runtime();lua.execute(r"""
   sixDepthFixture(a);begin();local before=writes;a.workCount=2;confirmCollection()
   assert(writes==before and probe.lastPlan.count==2 and probe.lastPlan.total.GOLD==16 and probe.lastPlan.total.CULTURE==4)
   for k in pairs(sixDepths)do sixDepths[k]=0 end;probe.Audit();assertSix(a,{})
  """)
 def test_unknown_inputs_retain_and_confirmed_current_changes_recover(self):
  lua=self.runtime();lua.execute(r"""
   sixDepthFixture(a);begin();local prior=snapshotBuildings(a);local before=writes
   sixUnknown=true;probe.Audit();assert(probe.error and writes==before);assertBuildingsSame(a,prior)
   sixUnknown=false;a.active=nil;probe.Audit();assert(probe.error and writes==before);assertBuildingsSame(a,prior)
   a.active=4;probe.Audit();assert(not probe.error);a.active=3;probe.Audit();assertSix(a,{})
   a.active=4;probe.Audit();assertSix(a,{SCIENCE=3,PRODUCTION=3,GOLD=8,FOOD=3,FAITH=3,CULTURE=2})
  """)
 def test_reference_change_confirmed_loss_load_all_92_and_unknown_guard(self):
  for boundary in ('reference','loss','load'):
   with self.subTest(boundary=boundary):
    lua=self.runtime();lua.globals().boundary=boundary;lua.execute(r"""
     sixDepthFixture(a);begin();local other=snapshotBuildings(b);local token=a.token
     if boundary=='reference' then a.token='other-city';probe.Audit()
     elseif boundary=='loss' then
      seedAllFinalMeaning(a);a.owner=3;local loss={confirmed=false,targetID=a.id,origin={owner=0}};local before=writes
      assert(not pcall(exits.CultureMeaningProbe,a,loss) and writes==before);loss.confirmed=true
      exits.CultureMeaningProbe(a,loss);before=writes;exits.CultureMeaningProbe(a,loss);assert(writes==before)
     else seedAllFinalMeaning(a);fire('LoadScreenClose')end
     assert(probe.mode=='OFF' and next(exactMeaning(a))==nil);assertBuildingsSame(b,other)
     assert(a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index]);if boundary~='reference' then assert(a.token==token)end
    """)
 def test_failed_replacement_or_end_never_releases_old_and_new_token_recovers(self):
  for y in LIMITS:
   with self.subTest(y=y):
    lua=self.runtime();lua.globals().blockedYield=y;lua.execute(r"""
     sixDepthFixture(a);begin();local value=probe.lastPlan.each[blockedYield]
     local id=GameInfo.Buildings[SPCCultureMeaningModel.FinalValues[blockedYield][value].name].Index
     failRemove=id;assert(not pcall(probe.End,0,a,'blocked') and a.present[id] and gwa.IsMeaningHeld(0,a))
     local before=writes;failRemove=nil;probe.End(0,a,'blocked');assert(writes==before and a.present[id])
     probe.End(0,a,'recover');assertSix(a,{});assert(old(a,'SCIENCE') and not dialogue.meaningOverride)
    """)
 def test_new_create_failure_after_partial_writes_withdraws_exact_and_no_legacy_mix(self):
  lua=self.runtime();lua.execute(r"""
   sixDepthFixture(a);probe.Advance(0,a,'base');local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_CULTURE_VALUE_2.Index
   local create=P.CreateBuilding;P.CreateBuilding=function(q,i)if i==id then return end;return create(q,i)end
   assert(not pcall(probe.Advance,0,a,'active'));assert(next(exactMeaning(a))==nil and gwa.IsMeaningHeld(0,a) and not old(a,'SCIENCE'))
   P.CreateBuilding=create;probe.End(0,a,'end');assertSix(a,{})
  """)
 def test_synchronous_notifications_bounded_preserve_same_turn_changes(self):
  lua=self.runtime();lua.execute(r"""
   sixDepthFixture(a);local create,remove=P.CreateBuilding,P.RemoveBuilding
   P.CreateBuilding=function(q,id)create(q,id);fire('CityBuildingsChanged',q.city.owner,q.city.id)end
   P.RemoveBuilding=function(bs,id)remove(bs,id);fire('CityBuildingsChanged',bs.city.owner,bs.city.id)end
   begin();assert(not probe.busy and not probe.advancing)
   sixDepths.DISTRICT_GOVERNMENT=6;probe.Audit();assert(probe.lastPlan.each.CULTURE==4)
   local before=writes;probe.Audit();assert(writes==before);probe.End(0,a,'end');assertSix(a,{})
  """)
 def native_panel_runtime(self):
  helper=l2c.L2CTests();helper.sql=self.sql;lua=helper.reader_runtime();lua.execute(HELPERS)
  cur=self.sql.execute('SELECT * FROM BuildingModifiers');cols=[x[0] for x in cur.description]
  lua.globals().GameInfo.BuildingModifiers=lua.globals().db(legacy.ae.lua_table(lua,[dict(zip(cols,r)) for r in cur]),'ModifierId')
  source=(R/'Mod/UI/P0Panel.lua').read_text();start=source.index('local function displayResponse()')
  display=source[start:source.index('-- B060 read/control requests',start)]
  copy=source[source.index('local function copy()'):source.index("  local lines={'SPC_DIAGNOSTIC_REPORT_BEGIN'")]+"end\n"
  lua.execute(r"""
   sixDepthFixture(a);selectedSix=a;nativeSix={SCIENCE=0,PRODUCTION=0,GOLD=0,FOOD=0,FAITH=0,CULTURE=4};nativeCalls=0;globalScans=0
   UI={GetHeadSelectedCity=function()return selectedSix end}
   local getter=a.GetBuildings;a.GetBuildings=function(c)local bs=getter(c)
    bs.GetBuildingYieldFromGreatWorks=function(_,y,id)
     assert(id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index);nativeCalls=nativeCalls+1;return nativeSix[GameInfo.Yields[y].YieldType:sub(7)]
    end;return bs
   end
   GameEffects={GetModifiers=function()globalScans=globalScans+1;return {}end}
   P.VERSION='B163_CURRENT';readings={};page=1;pageCity=1;localReport=nil
   function status(s)shownSix=s end;function print(s)copiedSix=s end
   function panelPrepare(action,token)
    pendingAction=action;pendingToken=token;meaningReadReference=SPCNetworkInput.Reference(a)
    local v=probe.View(0,a);v.token=token
    ExposedMembers.SPC_P0={Version=P.VERSION,LastToken=token,Snapshot='CURRENT_ACK',CultureMeaningView=v}
   end
  """+display+copy+r"""panelDisplay=displayResponse;panelCopy=copy""")
  return lua
 def test_independent_native_culture_failure_not_configuration_success(self):
  lua=self.native_panel_runtime();lua.execute(r"""
   probe.Advance(0,a,'base');local s=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true);assert(s:find('同回合基线已记录',1,true))
   probe.Advance(0,a,'active');nativeSix.SCIENCE=3;nativeSix.GOLD=8
   s=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
   assert(s:find('文化｜每件 +2／本城 +2｜实测差值 +0.00',1,true),s)
   assert(s:find('科研｜每件 +3／本城 +3｜实测差值 +3.00',1,true),s)
   nativeSix.CULTURE=6;s=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(s:find('实测差值 +2.00',1,true))
   sixDepths.DISTRICT_GOVERNMENT=6;probe.Audit();s=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
   assert(s:find('差值未确认',1,true) and not s:find('PASS',1,true))
  """)
 def test_current_panel_read_show_copy_single_enumeration_and_stale_selection(self):
  lua=self.native_panel_runtime();lua.execute(r"""
   probe.Advance(0,a,'base');panelPrepare('CULTURE_MEANING_ADVANCE','base');assert(panelDisplay() and globalScans==0)
   probe.Advance(0,a,'active');nativeSix.CULTURE=6
   panelPrepare('CULTURE_MEANING_READ','read');local before=writes;assert(panelDisplay() and globalScans==1)
   assert(shownSix:find('文化｜',1,true) and not shownSix:find('城市引用',1,true),shownSix)
   local n=nativeCalls;panelCopy();panelCopy();panelDisplay();assert(globalScans==1 and nativeCalls==n and writes==before)
   assert(copiedSix:find('Modifier诊断',1,true));selectedSix=b;panelDisplay();panelCopy()
   assert(globalScans==1 and nativeCalls==n and not shownSix:find('实测差值 +2.00',1,true))
   assert(not SPCBoostGreatWorkRead.ModifierDetails('read') and not copiedSix:find('Modifier诊断',1,true))
  """)
 def test_new_modifier_values_summary_and_detail_share_cache(self):
  lua=modifier.ModifierReadTests().runtime();lua.execute(r"""
   v.finalValues=true;v.productionOnly=false;v.mode='ACTIVE';definitions[2]=all_definitions.SPC_MEANING_PROBE_CULTURE_VALUE_3_WRITING;local b=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_CULTURE_VALUE_3
   assert(b.PrereqDistrict=='DISTRICT_THEATER');b.present=true
   local report=read('six');assert(report:find('CULTURE_VALUE_3_WRITING',1,true),report)
   local summary=SPCBoostGreatWorkRead.ModifierSummary('six');assert(summary:find('意义延展',1,true))
   assert(SPCBoostGreatWorkRead.ModifierDetails('six')==report and calls==1)
   read('six');assert(calls==1);SPCBoostGreatWorkRead.ClearModifierRead();assert(not SPCBoostGreatWorkRead.ModifierDetails('six'))
  """)
 def test_same_token_changed_signature_discards_summary_detail_without_rescan(self):
  lua=modifier.ModifierReadTests().runtime();lua.execute(r"""
   v.finalValues=true;v.mode='ACTIVE';read('stale');assert(calls==1)
   assert(SPCBoostGreatWorkRead.ModifierDetails('stale'))
   v.configuredCulture=99;local expired=read('stale')
   assert(expired:find('已释放或过期',1,true),expired)
   assert(not SPCBoostGreatWorkRead.ModifierDetails('stale'))
   assert(SPCBoostGreatWorkRead.ModifierSummary('stale'):find('未确认',1,true))
   read('stale');assert(calls==1)
  """)
 def test_current_culture_native_host_type_known_unknown_and_conflict(self):
  for host in ('DISTRICT_THEATER','DISTRICT_CITY_CENTER',None):
   with self.subTest(host=host):
    lua=modifier.ModifierReadTests().mapped();lua.globals().actualHost=host
    lua.execute(r"""
     v.finalValues=true;v.mode='ACTIVE';ids={2};definitions[2]=all_definitions.SPC_MEANING_PROBE_CULTURE_VALUE_3_WRITING
     GameInfo.Districts={[7]={DistrictType=actualHost}};district.GetType=function()return 7 end
     local text=read('host')
     if actualHost=='DISTRICT_THEATER' then assert(text:find('读取完整',1,true) and not text:find('CARRIER_HOST_',1,true),text)
     else assert(text:find('CARRIER_HOST_',1,true) and text:find('读取不完整',1,true),text)end
     assert(text:find('宿主区域=',1,true) and calls==1)
    """)
 def test_package_syntax_current_exact_registry_and_old_design_frozen(self):
  from lupa.lua55 import LuaRuntime
  l=LuaRuntime(unpack_returned_tuples=True)
  for p in ['CultureMeaningModel.lua','CultureMeaningProbe.lua','UI/BoostGreatWorkRead.lua','UI/P0Panel.lua','Probe.lua']:
   with self.subTest(lua=p):self.assertIsNotNone(l.eval('function(s)return assert(load(s))end')((R/'Mod'/p).read_text()))
  root=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot();self.assertEqual(root.attrib['version'],'190')
  for f in root.findall('.//File'): self.assertTrue((R/'Mod'/f.text).is_file(),f.text)
  self.assertEqual((R/'Specialization/Design/Revisions/Specialization_Design_Spec_D0045.md').read_bytes(),subprocess.check_output(['git','show','b9c6bb7:Specialization/Design/Specialization_v0.1_Design_Spec.md'],cwd=R))
 test_k_cold_pair=legacy.MeaningProbeTests.test_real_sample_request_cold_c00_uses_both_receivers
 test_k_duplicate_sequence=legacy.MeaningProbeTests.test_real_sample_duplicate_sequence_does_not_reinterpret_changed_payload
 test_old_writer_failure=legacy.MeaningProbeTests.test_old_withdrawal_failure_does_not_enable_new
 test_ingress=legacy.MeaningProbeTests.test_actual_request_invalid_or_foreign_ingress_does_not_run_probe
 test_import_registry=legacy.MeaningProbeTests.test_import_registry_rejects_each_missing_action_import

if __name__=='__main__':unittest.main()
