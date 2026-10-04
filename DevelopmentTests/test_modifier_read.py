"""B156 UI-only Modifier diagnostics: deterministic fixtures, no Civ VI claim."""
from pathlib import Path
import sqlite3, unittest
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]; M=R/'Mod'

def table(l,v):
 if isinstance(v,dict):return l.table_from({k:table(l,x) for k,x in v.items()})
 if isinstance(v,list):return l.table_from([table(l,x) for x in v])
 return v

class ModifierReadTests(unittest.TestCase):
 def runtime(self):
  l=LuaRuntime(unpack_returned_tuples=True)
  def include(name):l.execute((M/(name+'.lua')).read_text())
  l.globals().include=include
  l.execute('''function db(rows,key) local t={} for i,r in ipairs(rows)do r.Index=r.Index or i;t[r[key]]=r;t[r.Index]=r end return setmetatable(t,{__call=function()local i=0;return function()i=i+1;return rows[i]end end})end''')
  d=sqlite3.connect(':memory:')
  d.executescript('CREATE TABLE Types(Type,Kind); CREATE TABLE Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing); CREATE TABLE Modifiers(ModifierId,ModifierType); CREATE TABLE ModifierArguments(ModifierId,Name,Value); CREATE TABLE BuildingModifiers(BuildingType,ModifierId);')
  d.executescript((M/'Data/CultureMeaningProbe.sql').read_text())
  def rows(q):
   cur=d.execute(q);return [dict(zip([x[0]for x in cur.description],r))for r in cur]
  builds=rows('SELECT * FROM Buildings');builds.append(dict(BuildingType='BUILDING_AMPHITHEATER',Name='LOC_AMPHITHEATER'))
  attachments=rows('SELECT * FROM BuildingModifiers');hd='HD_AMPHITHEATER_WRITING_CULTURE_BOOST';tour='HD_AMPHITHEATER_WRITING_TOURISM_BOOST'
  attachments.extend([dict(BuildingType='BUILDING_AMPHITHEATER',ModifierId=x)for x in [hd,tour]])
  gi=l.table();l.globals().GameInfo=gi
  for name,data,key in [('Buildings',builds,'BuildingType'),('BuildingModifiers',attachments,'ModifierId'),('Eras',[{'EraType':'ANCIENT'},{'EraType':'CLASSICAL'}],'EraType'),('Yields',[{'YieldType':'YIELD_CULTURE'}],'YieldType'),('GreatWorks',[dict(GreatWorkType='TEST_WRITING',GreatWorkObjectType='GREATWORKOBJECT_WRITING',Index=7)],'GreatWorkType'),('GreatWork_YieldChanges',[dict(GreatWorkType='TEST_WRITING',YieldType='YIELD_CULTURE',YieldChange=2)],'GreatWorkType')]:gi[name]=l.globals().db(table(l,data),key)
  names=[hd,'SPC_MEANING_PROBE_CULTURE_SINGLE3_WRITING','SPC_MEANING_PROBE_SCIENCE_1_WRITING','SPC_MEANING_PROBE_GOLD_3_WRITING',tour]
  defs=[]
  for name in names:
   args=dict(d.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(name,)))
   if name==hd:args=dict(GreatWorkObjectType='GREATWORKOBJECT_WRITING',YieldType='YIELD_CULTURE',YieldChange=2)
   if name==tour:args=dict(GreatWorkObjectType='GREATWORKOBJECT_WRITING',ScalingFactor=150)
   defs.append(dict(Id=name,Arguments=args))
  l.globals().all_definitions=table(l,{r['ModifierId']:dict(Id=r['ModifierId'],Arguments=dict(d.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(r['ModifierId'],))))for r in rows('SELECT ModifierId FROM Modifiers')})
  d.close();l.globals().definitions=table(l,defs)
  l.execute('''
  calls=0;detailCalls=0;turn=62;owner=0;cityID=42;binding='ORIGINAL';mode='OFF';active=true
  b={IsPillaged=function()return false end,GetNumGreatWorkSlots=function()return 2 end,GetGreatWorkInSlot=function(self,index,slot)return slot==0 and 9 or -1 end,GetGreatWorkTypeFromIndex=function()return 7 end,GetBuildingYieldFromGreatWorks=function()return 4 end}
  c={GetName=function()return '测试城' end,GetOwner=function()return owner end,GetID=function()return cityID end,GetX=function()return 8 end,GetY=function()return 9 end,GetProperty=function()return binding end,GetBuildings=function()return b end}
  selected=c;Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return turn end};UI={GetHeadSelectedCity=function()return selected end};Locale={Lookup=function(s)return s end}
  P={HasBuilding=function(buildings,index)return true end}
  ids={1,2,3,4,5}
  GameEffects={GetModifiers=function()calls=calls+1;return ids end,GetModifierDefinition=function(id)return definitions[id]end,GetModifierOwner=function(id)return id*10 end,GetObjectsPlayerId=function()return 0 end,GetObjectType=function()return 'LOC_MODIFIER_OBJECT_CITY' end,GetObjectString=function()return 'City (42), Owner: 0, Name: SAME_NAME' end,GetModifierActive=function()detailCalls=detailCalls+1;return active end,GetModifierSubjects=function()return nil end}
  ''')
  l.execute((M/'UI/BoostGreatWorkRead.lua').read_text())
  l.execute("v={owner=0,cityID=42,reference=SPCNetworkInput.Reference(c),mode='OFF',variant='SINGLE3',configuredScience=0,configuredGold=0,configuredCulture=0,stamp=''}; requested=v.reference; function read(token)v.token=token;return SPCBoostGreatWorkRead.Modifiers(P,c,v,token,requested)end")
  return l
 def test_off_reads_exact_instances_and_actual_building_without_writes(self):
  l=self.runtime();s=l.globals().read('a');self.assertIn('读取完整',s);self.assertIn('所选城 测试城',s);self.assertIn('UNKNOWN:FORMAT',s);self.assertIn('flat=3',s);self.assertIn('实际文化 4',s);self.assertIn('定义基础文化 2',s);self.assertEqual(l.globals().calls,1)
 def test_same_token_no_rescan_new_token_fresh(self):
  l=self.runtime();a=l.globals().read('a');self.assertEqual(a,l.globals().read('a'));self.assertEqual(l.globals().calls,1);l.globals().read('b');self.assertEqual(l.globals().calls,2)
 def test_clear_does_not_replay_consumed_token(self):
  l=self.runtime();l.globals().read('a');l.execute('SPCBoostGreatWorkRead.ClearModifierRead()');self.assertIn('释放',l.globals().read('a'));self.assertEqual(l.globals().calls,1)
 def test_wrong_city_owner_reference_or_token_never_scans(self):
  for mutate in ['cityID=43','owner=2',"binding='OTHER'",'selected=nil',"requested='OTHER'"]:
   with self.subTest(mutate=mutate):
    l=self.runtime();l.execute(mutate);self.assertIn('STALE',l.globals().read('a'));self.assertEqual(l.globals().calls,0)
 def test_change_during_read_or_cached_turn_is_stale(self):
  l=self.runtime();l.execute('GameEffects.GetModifiers=function()calls=calls+1;turn=turn+1;return ids end');self.assertIn('STALE',l.globals().read('a'))
  l=self.runtime();l.globals().read('a');l.execute('turn=63');self.assertIn('过期',l.globals().read('a'));self.assertEqual(l.globals().calls,1)
 def test_configuration_error_does_not_prevent_read(self):
  l=self.runtime();l.execute("v.configurationError='TEST';v.error='TEST'");self.assertIn('HD_AMPHITHEATER',l.globals().read('a'))
 def test_bad_enumerations_are_incomplete_not_zero(self):
  for value in ['nil','false','{[1]=1,[3]=3}','{1,1}','{[32769]=1}','{true}']:
   with self.subTest(value=value):
    l=self.runtime();l.execute('ids='+value);s=l.globals().read('a');self.assertIn('读取不完整',s);self.assertIn('不能解释为零实例',s)
 def test_empty_enumeration_is_observation_only(self):
  l=self.runtime();l.execute('ids={}');s=l.globals().read('a');self.assertIn('本次未观察到',s);self.assertIn('不等于本城没有效果',s)
 def test_missing_api_and_definition_fail_closed(self):
  for code in ['GameEffects.GetModifiers=nil',"GameEffects.GetModifiers=function()error('native failed')end",'definitions[2]=nil']:
   l=self.runtime();l.execute(code);self.assertIn('读取不完整',l.globals().read('a'))
 def test_foreign_is_filtered_but_unknown_owner_is_preserved(self):
  l=self.runtime();l.execute('GameEffects.GetObjectsPlayerId=function(id)if id==10 then return 2 elseif id==20 then return nil else return 0 end end');s=l.globals().read('a');self.assertIn('其它玩家跳过 1',s);self.assertIn('玩家未知 1',s);self.assertNotIn('HD_AMPHITHEATER_WRITING_CULTURE_BOOST',s);self.assertIn('CULTURE_SINGLE3_WRITING',s)
 def test_active_nonboolean_is_unknown(self):
  l=self.runtime();l.execute('active=1');s=l.globals().read('a');self.assertIn('Active=UNKNOWN',s);self.assertIn('ACTIVE_UNKNOWN',s);self.assertNotIn('Active=false',s)
 def test_subjects_nil_empty_error_and_overflow_remain_distinct(self):
  for value,want in [('nil','subjects=nil'),('{}','subjects=empty'),('{11,12}','subjects=2对象'),('{[65]=11}','SUBJECTS_ARRAY_KEY')]:
   l=self.runtime();l.execute('GameEffects.GetModifierSubjects=function()return '+value+' end');self.assertIn(want,l.globals().read('a'))
 def test_wrong_arguments_and_attachment_report_unknown(self):
  l=self.runtime();l.execute('definitions[2].Arguments=nil');self.assertIn('ARGUMENTS_UNKNOWN',l.globals().read('a'))
  l=self.runtime();l.execute("GameInfo.BuildingModifiers=db({},'ModifierId')");self.assertIn('ATTACHMENT_MISSING',l.globals().read('a'))
 def test_bounded_matching_output_and_raw_markup(self):
  l=self.runtime();l.execute("ids={};for i=1,65 do ids[i]=i;definitions[i]=definitions[1]end;GameEffects.GetObjectString=function()return string.rep('[NEWLINE]长',100)end")
  s=l.globals().read('a');self.assertIn('MATCH_LIMIT',s);self.assertIn('未展开',s);self.assertNotIn('[NEWLINE]',s);self.assertLess(len(s),9000)
 def test_current_panel_dispatch_is_read_only_and_cached(self):
  l=self.runtime();src=(M/'UI/P0Panel.lua').read_text();start=src.index('local function displayResponse()');end=src.index('-- B060 read/control requests',start)
  l.execute("P.VERSION='TEST';pendingToken='a';pendingAction='CULTURE_MEANING_READ';pageCity=42;meaningReadReference=requested;readings={};page=1;function status(s)shown=s end;Players={[0]={GetCities=function()return {FindID=function()return c end}end}};v.token='a';ExposedMembers={SPC_P0={Version='TEST',LastToken='a',Snapshot='OLD',CultureMeaningView=v}}")
  l.execute(src[start:end]+'\ndisplay=displayResponse');l.globals().display();self.assertIn('Modifier诊断',l.globals().shown);self.assertNotIn('四态原生读数',l.globals().shown);l.globals().display();self.assertEqual(l.globals().calls,1)
  l.execute("pendingAction='CULTURE_MEANING_END'");l.globals().display();self.assertEqual(l.globals().calls,1)
 def test_copy_reuses_report_without_global_scan(self):
  l=self.runtime();src=(M/'UI/P0Panel.lua').read_text();start=src.index('local function displayResponse()');end=src.index('-- B060 read/control requests',start)
  l.execute("P.VERSION='TEST';pendingToken='a';pendingAction='CULTURE_MEANING_READ';pageCity=42;meaningReadReference=requested;readings={};page=1;function status(s)shown=s end;function print(s)logged=s end;Players={[0]={GetCities=function()return {FindID=function()return c end}end}};v.token='a';ExposedMembers={SPC_P0={Version='TEST',LastToken='a',Snapshot='OLD',CultureMeaningView=v}}")
  copy=src[src.index('local function copy()'):src.index("  local lines={'SPC_DIAGNOSTIC_REPORT_BEGIN'")]+"end\ncopyReport=copy"
  l.execute(src[start:end]+copy);l.globals().copyReport();l.globals().copyReport();self.assertEqual(l.globals().calls,1);self.assertIn('[SPC][MODIFIER_READ]',l.globals().logged)
 def test_missing_argument_values_and_bad_work_yield_not_successful_zero(self):
  l=self.runtime();l.execute('definitions[2].Arguments={}');self.assertIn('ARGUMENTS_UNKNOWN',l.globals().read('a'))
  l=self.runtime();l.execute('b.GetBuildingYieldFromGreatWorks=function()return 0/0 end');s=l.globals().read('a');self.assertIn('WORK_YIELD_UNKNOWN',s);self.assertNotIn('实际文化 0',s)
 def mapped(self):
  l=self.runtime();l.execute("""
  district={GetID=function()return 1114126 end,GetCity=function()return c end}
  c.GetDistricts=function()return {FindID=function(self,id)if id==1114126 then return district end end}end
  CityManager={GetCity=function(pid,cid)if pid==0 and cid==42 then return c end end}
  GameEffects.GetObjectType=function()return 'LOC_MODIFIER_OBJECT_DISTRICT' end
  GameEffects.GetObjectString=function()return 'District: 1114126, Owner: 0, SubType: 1, SubValue: 762987263, City: 42' end
  GameEffects.GetModifierSubjects=function()return {10}end
  """);return l
 def test_observed_district_format_and_subject_verified_with_objects(self):
  l=self.mapped();s=l.globals().read('a');self.assertIn('本城已核验',s);self.assertIn('接收对象1｜本城已核验',s)
 def test_observed_negative_subvalue_maps_owner_and_subject(self):
  l=self.mapped();l.execute("GameEffects.GetObjectString=function()return 'District: 1114126, Owner: 0, SubType: 1, SubValue: -544493210, City: 42' end")
  s=l.globals().read('signed');self.assertIn('读取完整',s);self.assertIn('接收对象1｜本城已核验',s);self.assertNotIn('UNKNOWN:',s)
  self.assertIn('SubValue: -544493210',s);self.assertEqual(l.globals().calls,1)
  self.assertEqual(s,l.globals().read('signed'));self.assertEqual(l.globals().calls,1)
 def test_signed_subvalue_still_requires_current_objects_and_identity(self):
  raw='District: 1114126, Owner: 0, SubType: 1, SubValue: -544493210, City: 42'
  for mutate in ['CityManager=nil','district.GetID=function()return 99 end',"district.GetCity=function()return {GetOwner=function()return 0 end,GetID=function()return 42 end,GetX=function()return 8 end,GetY=function()return 9 end,GetProperty=function()return 'OTHER' end}end"]:
   with self.subTest(mutate=mutate):
    l=self.mapped();l.globals().signed_raw=raw;l.execute('GameEffects.GetObjectString=function()return signed_raw end;'+mutate)
    s=l.globals().read('signed');self.assertNotIn('本城已核验',s);self.assertIn('UNKNOWN:OBJECT_CHECK',s)
  for bad,want in [(raw.replace('Owner: 0','Owner: 1'),'UNKNOWN:OWNER_CONFLICT'),(raw.replace('City: 42','City: 43'),'UNKNOWN:OBJECT_CHECK')]:
   with self.subTest(bad=bad):
    l=self.mapped();l.globals().bad=bad;l.execute('GameEffects.GetObjectString=function()return bad end')
    s=l.globals().read('signed');self.assertNotIn('本城已核验',s);self.assertIn(want,s)
 def test_signed_subvalue_does_not_expand_other_district_fields_or_format(self):
  raw='District: 1114126, Owner: 0, SubType: 1, SubValue: -544493210, City: 42'
  bads=[raw+' extra','prefix '+raw,raw.replace('SubType: 1','SubType: -1'),raw.replace('District: 1114126','District: -1114126'),raw.replace('Owner: 0','Owner: -1'),raw.replace('City: 42','City: -42')]
  bads.extend(raw.replace('SubValue: -544493210','SubValue: '+value)for value in ['-','--544493210','+544493210','-544493210.0','-544493210x'])
  for bad in bads:
   with self.subTest(bad=bad):
    l=self.mapped();l.globals().bad=bad;l.execute('GameEffects.GetObjectString=function()return bad end')
    s=l.globals().read('signed');self.assertNotIn('本城已核验',s);self.assertIn('UNKNOWN:FORMAT',s)
 def production(self):
  l=self.mapped();l.execute("""
  GameInfo.Yields=db({{YieldType='YIELD_CULTURE',Index=1},{YieldType='YIELD_PRODUCTION',Index=2}},'YieldType')
  P.Info=function(name,key)return GameInfo[name][key]end
  P.HasBuilding=function(buildings,index)return index==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index end
  c.GetPopulation=function()return 4 end
  b.IsBuildingThemedCorrectly=function()return false end
  workCount=1;nativeProduction=0;yieldCalls=0
  b.GetGreatWorkInSlot=function(self,index,slot)return slot<workCount and slot+9 or -1 end
  b.GetBuildingYieldFromGreatWorks=function(self,y,index)assert(y==GameInfo.Yields.YIELD_PRODUCTION.Index,'OTHER_YIELD_READ');yieldCalls=yieldCalls+1;return nativeProduction end
  v.productionOnly=true;v.mode='BASELINE';v.count=1;v.production=3;v.totalProduction=3;v.configuredProduction=0;v.configuredCulture=0
  v.oldHeld=true;v.dialoguePercent=0;v.planStatus='READY';v.currentIdentity='CULTURE';v.currentPotential=4;v.currentActive=4;v.currentActiveStatus='KNOWN';v.stamp='INDUSTRY:6';v.remainingOwned=0
  function meaning(mark)return SPCBoostGreatWorkRead.Meaning(P,c,v,mark)end
  """);return l
 def test_production_only_meaning_reads_production_and_counts_w_once(self):
  for count in [1,2]:
   with self.subTest(count=count):
    l=self.production();l.execute(f'workCount={count};v.count={count};v.totalProduction=3*{count}')
    self.assertIn('同回合基线已记录',l.globals().meaning(True))
    l.execute(f"v.mode='ACTIVE';v.configuredProduction=3;nativeProduction=3*{count}")
    s=l.globals().meaning(False);self.assertIn(f'合格W={count}',s);self.assertIn(f'每件 +3／本城 +{3*count}',s);self.assertIn(f'实测差值 +{3*count:.2f}',s)
    self.assertIn('其它产出未验证',s);self.assertNotIn('科研｜',s);self.assertNotIn('金币｜',s);self.assertNotIn('未确认',s);self.assertEqual(l.globals().yieldCalls,2)
 def test_production_only_absolute_off_and_unknown_are_independent(self):
  l=self.production();l.execute("v.mode='OFF';nativeProduction=7;ids={}")
  s=l.globals().read('off');self.assertIn('当前原生作品生产力 7',s);self.assertNotIn('实际文化',s);self.assertIn('真实退出收益及旧系统恢复另行核对',s)
  off=l.globals().meaning(False);self.assertIn('当前原生作品生产力 7.00',off);self.assertIn('不作追加差值PASS',off);self.assertEqual(l.globals().calls,1)
  l=self.production();l.execute("v.mode='OFF';nativeProduction=0/0;ids={}")
  s=l.globals().read('unknown');self.assertIn('WORK_YIELD_UNKNOWN',s);self.assertIn('不以0代替未知',s);self.assertNotIn('当前原生作品生产力 0',s)
 def test_finite_production_value_writing_native_allowlist(self):
  for amount in range(1,11):
   with self.subTest(amount=amount):
    l=self.production();l.execute(f"ids={{1}};definitions={{all_definitions['SPC_MEANING_PROBE_PRODUCTION_VALUE_{amount}_WRITING']}};v.mode='ACTIVE';nativeProduction={amount};v.production={amount};v.configuredProduction={amount};v.remainingOwned=1")
    s=l.globals().read('value');self.assertIn('读取完整',s);self.assertIn(f'SPC_MEANING_PROBE_PRODUCTION_VALUE_{amount}_WRITING',s);self.assertIn(f'flat={amount}',s);self.assertIn('本城Meaning Writing实例 1',s);self.assertIn('实例ID 1',s);self.assertEqual(l.globals().calls,1)
 def test_production_allowlist_does_not_match_lookalike_or_nonwriting(self):
  l=self.production();l.execute("""
  ids={1,2,3,4,5};definitions={all_definitions.SPC_MEANING_PROBE_PRODUCTION_VALUE_3_WRITING,
   {Id='SPC_MEANING_PROBE_PRODUCTION_VALUE_11_WRITING',Arguments={YieldType='YIELD_PRODUCTION',YieldChange=11}},
   {Id='SPC_MEANING_PROBE_PRODUCTION_VALUE_0_WRITING',Arguments={YieldType='YIELD_PRODUCTION',YieldChange=0}},
   {Id='SPC_MEANING_PROBE_PRODUCTION_VALUE_3_EXTRA_WRITING',Arguments={YieldType='YIELD_PRODUCTION',YieldChange=3}},
   all_definitions.SPC_MEANING_PROBE_PRODUCTION_VALUE_3_MUSIC}
  v.mode='ACTIVE';nativeProduction=3;v.production=3;v.configuredProduction=3;v.remainingOwned=1
  """)
  s=l.globals().read('exact');self.assertIn('读取完整',s);self.assertIn('本城Meaning Writing实例 1',s)
  for name in ['VALUE_11_WRITING','VALUE_0_WRITING','VALUE_3_EXTRA_WRITING','VALUE_3_MUSIC']:self.assertNotIn(name,s)
 def test_production_mode_change_invalidates_cached_modifier_report(self):
  l=self.production();l.execute('ids={}');l.globals().read('mode');l.execute('v.productionOnly=false')
  self.assertIn('过期',l.globals().read('mode'));self.assertEqual(l.globals().calls,1)
 def test_production_read_lifecycle_does_not_automatically_enumerate(self):
  l=self.production();l.globals().meaning(True);self.assertEqual(l.globals().calls,0)
  l.execute("v.mode='ACTIVE';v.configuredProduction=3;nativeProduction=3")
  l.globals().meaning(False);self.assertEqual(l.globals().calls,0)
  l.globals().read('explicit');l.globals().read('explicit');self.assertEqual(l.globals().calls,1)
  l.execute("v.mode='OFF';v.configuredProduction=0")
  l.globals().meaning(False);self.assertEqual(l.globals().calls,1)
  l.globals().read('off');self.assertEqual(l.globals().calls,2)
  l.execute('SPCBoostGreatWorkRead.ClearModifierRead()');self.assertIn('释放',l.globals().read('off'));self.assertEqual(l.globals().calls,2)
 def test_production_late_or_stale_reference_does_not_scan_or_replay(self):
  for mutate in ["binding='REPLACED'",'selected=nil',"requested='OTHER'"]:
   with self.subTest(mutate=mutate):
    l=self.production();l.execute(mutate);self.assertIn('STALE',l.globals().read('late'));self.assertEqual(l.globals().calls,0)
  l=self.production();l.execute("GameEffects.GetModifiers=function()calls=calls+1;binding='REPLACED';return ids end")
  self.assertIn('STALE',l.globals().read('race'));self.assertEqual(l.globals().calls,1)
  l.execute("binding='ORIGINAL'");self.assertIn('STALE',l.globals().read('race'));self.assertEqual(l.globals().calls,1)
 def test_production_value_amount_uses_model_metadata(self):
  l=self.production();l.execute("""
  v.diagnostic=true;v.diagnosticStage='OFF';v.diagnosticExpected=0;v.configuredProduction=2;v.remainingOwned=1
  v.diagnosticCarriers={{name=SPCCultureMeaningModel.ProductionValues[3].name,yield='PRODUCTION',amount=2,pillaged=false}}
  """)
  s=l.globals().SPCBoostGreatWorkRead.ProductionDiagnostic(l.globals().P,l.globals().c,l.globals().v,False,'metadata',l.globals().requested,False)
  self.assertIn('配置未确认：ME_UI_DIAG_CONFIGURATION',s);self.assertEqual(l.globals().calls,0)
 def test_mapping_rejects_partial_malformed_ids_and_owner(self):
  raw='District: 1114126, Owner: 0, SubType: 1, SubValue: 762987263, City: 42'
  for value in [raw+' extra','prefix '+raw,raw.replace('City: 42','City: 43'),raw.replace('Owner: 0','Owner: 1'),raw.replace('1114126','9007199254740992')]:
   l=self.mapped();l.globals().bad=value;l.execute('GameEffects.GetObjectString=function()return bad end');s=l.globals().read('a');self.assertNotIn('本城已核验',s);self.assertIn('UNKNOWN:',s)
 def test_mapping_requires_current_district_parent_and_binding(self):
  for mutate in ['CityManager=nil','district.GetID=function()return 99 end',"district.GetCity=function()return {GetOwner=function()return 0 end,GetID=function()return 42 end,GetX=function()return 8 end,GetY=function()return 9 end,GetProperty=function()return 'OTHER' end}end",'c.GetDistricts=function()error("missing")end']:
   l=self.mapped();l.execute(mutate);s=l.globals().read('a');self.assertNotIn('本城已核验',s);self.assertIn('UNKNOWN:OBJECT_CHECK',s)
 def test_different_city_is_not_selected_city(self):
  l=self.mapped();l.execute("other={GetOwner=function()return 0 end,GetID=function()return 65536 end,GetX=function()return 1 end,GetY=function()return 2 end,GetProperty=function()return 'OTHER' end,GetDistricts=c.GetDistricts};district.GetCity=function()return other end;CityManager.GetCity=function()return other end;GameEffects.GetObjectString=function()return 'District: 1114126, Owner: 0, SubType: 1, SubValue: 762987263, City: 65536' end")
  s=l.globals().read('a');self.assertIn('其它城已核验: 0/65536',s);self.assertNotIn('本城已核验',s)
 def test_subject_unknown_type_preserved_and_bounded(self):
  l=self.mapped();l.execute("GameEffects.GetModifierSubjects=function()return {101,102,103,104}end;GameEffects.GetObjectType=function(id)return id>100 and 'UNOBSERVED' or 'LOC_MODIFIER_OBJECT_DISTRICT' end")
  s=l.globals().read('a');self.assertIn('接收对象1｜UNKNOWN:FORMAT',s);self.assertIn('另1个接收对象未展开',s);self.assertNotIn('接收对象4',s)
 def test_packaging_and_lua_syntax(self):
  l=self.runtime()
  for file in ['UI/BoostGreatWorkRead.lua','UI/P0Panel.lua','Probe.lua']:
   l.execute('assert(load(...))',(M/file).read_text())
  info=(M/'SpecializationP0.modinfo').read_text();self.assertEqual(info.count('<File>UI/BoostGreatWorkRead.lua</File>'),2);self.assertIn('version="184"',info)

if __name__=='__main__':unittest.main()
