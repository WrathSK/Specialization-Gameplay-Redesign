"""B172 D0049 automatic Inspiration. Local Lua/SQL behavior, not native GPP proof.
Read-only external DB copied to memory. Actual normal writer / K ingress / retired
probe / request routing are exercised, without changing external data or fixtures.
"""
from pathlib import Path
import sqlite3, unittest, xml.etree.ElementTree as ET
import test_culture_aesthetic as ae
import test_culture_meaning_probe as legacy
import test_culture_meaning_automatic as meaning
import test_culture_inspiration_probe as old
R=Path(__file__).resolve().parents[1]

class InspirationAutomaticTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  old.InspirationTests.setUpClass();cls.sql=old.InspirationTests.sql
  carriers=[f'BUILDING_SPC_INSPIRATION_ERA_{e}' for e in range(1,8)]
  modifiers=[f'SPC_INSPIRATION_ERA_{e}' for e in range(1,8)]
  for table,col,values in [('BuildingModifiers','BuildingType',carriers),('Buildings','BuildingType',carriers),('Types','Type',carriers),('ModifierArguments','ModifierId',modifiers),('Modifiers','ModifierId',modifiers)]:
   cls.sql.executemany(f'DELETE FROM {table} WHERE {col}=?',[(v,)for v in values])
  cls.sql.executescript((R/'Mod/Data/CultureInspiration.sql').read_text())
 @classmethod
 def tearDownClass(cls):cls.sql.close()
 def runtime(self,ready=True,real=False):
  h=meaning.AutomaticMeaningTests();h.sql=self.sql;l=h.runtime(ready=False,real=real)
  for table,key in [('ModifierArguments','ModifierId'),('BuildingModifiers','BuildingType'),('GreatPersonClasses','GreatPersonClassType'),('DynamicModifiers','ModifierType')]:
   cur=self.sql.execute('SELECT * FROM '+table);cols=[x[0]for x in cur.description];rows=[dict(zip(cols,x))for x in cur]
   for i,row in enumerate(rows):row['Index']=i+1
   l.globals().GameInfo[table]=l.globals().db(ae.lua_table(l,rows),key)
  for name in ['CultureInspirationProbe','CultureInspiration','InspirationReadout']:l.globals().include(name)
  l.execute(r"""
   Locale.Lookup=function(k,...)local t={k};for _,v in ipairs({...})do t[#t+1]=tostring(v)end;return table.concat(t,' | ')end
   SPCCultureInspirationProbe.Start(P,shared,{retired=true});ip=shared.CultureInspirationProbe
   SPCCultureInspiration.Start(P,shared);ins=shared.CultureInspiration
   function inspiration(c)
    local n,value=0,0
    for e,name in ipairs(SPCCultureInspirationModel.Owned)do if c.present[GameInfo.Buildings[name].Index]then n=n+1;value=value+3*e end end
    return value,n
   end
   function retired(c)local n=0;for _,v in ipairs({1,3,6,10})do if c.present[GameInfo.Buildings['BUILDING_SPC_INSPIRE_PROBE_'..v].Index]then n=n+1 end end;return n end
   function refresh(c)ins.Audit({player=0,city=(c or a).id})end
  """)
  legacy.bind_actual_request(l)
  if ready:l.execute("fire('LoadScreenClose')")
  return l
 def test_sql_is_exact_city_percentage_primitive(self):
  d=self.sql
  typ='MODIFIER_CITY_INCREASE_GREAT_PERSON_POINT_BONUS'
  self.assertEqual(d.execute('SELECT CollectionType,EffectType FROM DynamicModifiers WHERE ModifierType=?',(typ,)).fetchone(),('COLLECTION_OWNER','EFFECT_ADJUST_CITY_GREAT_PERSON_POINTS_MODIFIER'))
  for mid,expected in [('GARDEN_ADJUST_GREAT_PERSON_POINT_BONUS',20),('HD_GOVERNOR_EDUCATOR_LEFT_1_GPP_BONUS',100)]:
   self.assertEqual(d.execute('SELECT ModifierType FROM Modifiers WHERE ModifierId=?',(mid,)).fetchone()[0],typ)
   self.assertEqual(int(d.execute("SELECT Value FROM ModifierArguments WHERE ModifierId=? AND Name='Amount'",(mid,)).fetchone()[0]),expected)
  for e in range(1,8):
   with self.subTest(era=e):
    mid=f'SPC_INSPIRATION_ERA_{e}'
    self.assertEqual(d.execute('SELECT ModifierType,OwnerRequirementSetId,SubjectRequirementSetId FROM Modifiers WHERE ModifierId=?',(mid,)).fetchone(),(typ,None,None))
    self.assertEqual(dict(d.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(mid,))),{'Amount':str(3*e)})
    self.assertEqual(d.execute('SELECT ModifierId FROM BuildingModifiers WHERE BuildingType=?',(f'BUILDING_{mid}',)).fetchall(),[(mid,)])
 def test_all_eras_current_only_no_work_count_or_d_scaling(self):
  l=self.runtime()
  for e in range(8):
   with self.subTest(era=e):
    l.execute(f"a.eras={e};a.workCount=30;local before=counts.dcCapture;refresh();local v,n=inspiration(a);assert(v=={3*e} and n=={int(e>0)});assert(counts.dcCapture==before and inspiration(b)==6)")
    l.execute("local before=writes;refresh();refresh();assert(writes==before)")
 def test_pure_model_unknown_and_gates(self):
  l=self.runtime()
  l.execute(r"""
   local f={validity='VERIFIED',identity='CULTURE',potential=4,activeStatus='KNOWN',active=4}
   for _,e in ipairs({-1,8,0.5})do assert(not pcall(SPCCultureInspirationModel.Plan,f,{hasConfirmed=true,availability='KNOWN',eraCount=e}))end
   f.activeStatus='UNKNOWN';assert(not pcall(SPCCultureInspirationModel.Plan,f,nil))
   f.potential=3;assert(SPCCultureInspirationModel.Plan(f,nil).status=='INACTIVE')
   f.identity='INDUSTRY';assert(SPCCultureInspirationModel.Plan(f,nil).status=='INACTIVE')
  """)
 def test_native_carrier_transition_removes_old_before_new(self):
  l=self.runtime();l.execute(r"""
   a.eras=1;refresh();assert(inspiration(a)==3)
   local create=P.CreateBuilding
   P.CreateBuilding=function(q,id)
    if q.city==a and GameInfo.Buildings[id].BuildingType=='BUILDING_SPC_INSPIRATION_ERA_2'then assert(inspiration(a)==0)end
    create(q,id)
   end
   a.eras=2;refresh();local v,n=inspiration(a);assert(v==6 and n==1)
  """)
 def test_real_packet_callback_era_change_and_same_era_no_duplicate_write(self):
  l=self.runtime(real=True);l.execute(r"""
   sample(1,1,1);assert(inspiration(a)==3 and inspiration(b)==3)
   local before=writes;sample(2,2,1);assert(inspiration(a)==3 and writes==before)
   local p=packet(3,2,1);local seen=0
   p.FactsData=p.FactsData:gsub('GREATWORK_BHASA_1',function()seen=seen+1;return seen==2 and 'GREATWORK_CHAUCER_1' or 'GREATWORK_BHASA_1'end)
   meaningRequest(0,p);assert(inspiration(a)==6 and inspiration(b)==3,shared.GreatWorkFacts.lastError)
   before=writes;meaningRequest(0,p);assert(writes==before)
   sample(4,0,2);assert(inspiration(a)==0 and inspiration(b)==3)
  """)
 def test_active_change_old_new_city_and_same_turn_restore(self):
  l=self.runtime();l.execute("a.active=1;fire('GovernorAssigned',0,2,0);assert(inspiration(a)==0 and inspiration(b)==6);a.active=4;fire('GovernorEstablished',0,1,0);assert(inspiration(a)==6);a.identity='RESEARCH';a.worksUnknown=true;refresh();assert(inspiration(a)==0)")
 def test_unknown_holds_only_confirmed_same_reference(self):
  for kind in ['factsUnknown','worksUnknown','active']:
   with self.subTest(kind=kind):
    l=self.runtime();l.globals().kind=kind;l.execute("if kind=='active'then a.active=nil else a[kind]=true end;local before=writes;refresh();assert(inspiration(a)==6 and writes==before and ins.errors['0:1']);a.token='changed';refresh();assert(inspiration(a)==0 and ins.records['0:1']==nil)")
 def test_retired_probe_has_no_active_hooks_or_manual_path(self):
  l=self.runtime();l.execute(r"""
   assert(ip.retired and ip.Request==nil and exits.CultureInspirationProbe==nil)
   local n=writes
   for _,action in ipairs({'INSPIRE_NEXT','INSPIRE_READ','INSPIRE_END','INSPIRE_STATUS','INSPIRE_DETAIL'})do
    meaningRequest(0,{Action=action,CityID=1,Token=action});assert(shared.LastToken==action and shared.CultureInspirationView.percent==6)
   end
   assert(writes==n and retired(a)==0 and inspiration(a)==6)
  """)
 def test_load_retires_old_then_uses_current_not_saved_value(self):
  l=self.runtime();l.execute(r"""
   seed(a,'BUILDING_SPC_INSPIRE_PROBE_10');a.eras=1;fire('LoadScreenClose')
   assert(retired(a)==0 and inspiration(a)==3 and inspiration(b)==6)
   a.worksUnknown=true;fire('LoadScreenClose');assert(inspiration(a)==0)
   a.worksUnknown=false;a.eras=7;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(inspiration(a)==21)
  """)
 def test_missed_load_uses_confirmed_collection_without_panel(self):
  l=self.runtime(ready=False,real=True);l.execute("sample(1,1,1);assert(ins.ready and inspiration(a)==3)")
 def test_foreign_saved_carriers_cleared_without_ai_state(self):
  l=self.runtime(False);l.execute("b.owner=3;seed(b,'BUILDING_SPC_INSPIRATION_ERA_7');seed(b,'BUILDING_SPC_INSPIRE_PROBE_10');fire('LoadScreenClose');assert(inspiration(b)==0 and retired(b)==0 and inspiration(a)==6 and not ins.records['3:2'])")
 def test_confirmed_loss_idempotent_and_return_recomputes(self):
  l=self.runtime();l.execute(r"""
   local ordinary=GameInfo.Buildings.BUILDING_MONUMENT.Index;local token=a.token
   local loss={confirmed=false,targetID=1,origin={owner=0}}
   assert(not pcall(exits.CultureInspiration,a,loss));assert(inspiration(a)==6)
   a.owner=3;loss.confirmed=true;exits.CultureInspiration(a,loss);exits.CultureInspiration(a,loss)
   assert(inspiration(a)==0 and inspiration(b)==6 and a.present[ordinary] and a.token==token)
   a.owner=0;a.active=1;returns.CultureInspiration(0,a);assert(inspiration(a)==0)
   a.active=4;a.eras=1;returns.CultureInspiration(0,a);assert(inspiration(a)==3)
  """)
 def test_remove_failure_cannot_add_new_value_or_contaminate_other_city(self):
  l=self.runtime();l.execute("failRemove=GameInfo.Buildings.BUILDING_SPC_INSPIRATION_ERA_2.Index;a.eras=3;refresh();assert(inspiration(a)==6 and ins.errors['0:1'] and inspiration(b)==6);failRemove=nil;refresh();assert(inspiration(a)==9 and not ins.errors['0:1'])")
 def test_unknown_presence_cannot_add_new_value(self):
  l=self.runtime();l.execute("failHas=GameInfo.Buildings.BUILDING_SPC_INSPIRATION_ERA_2.Index;a.eras=3;refresh();assert(inspiration(a)==6 and ins.errors['0:1'])")
 def test_failed_or_ambiguous_create_clears_projection(self):
  for mode in ['return','throw_after','owner','reference']:
   with self.subTest(mode=mode):
    l=self.runtime();l.globals().mode=mode;l.execute(r"""
     a.eras=0;refresh();a.eras=2
     local create=P.CreateBuilding;P.CreateBuilding=function(q,id)
      if mode=='return'then return end
      create(q,id)
      if mode=='throw_after'then error('CREATE_REPLY_LOST')elseif mode=='owner'then a.owner=3 elseif mode=='reference'then a.token='new'end
     end
     refresh();assert(inspiration(a)==0 and ins.errors['0:1'] and ins.records['0:1']==nil)
    """)
 def test_pillaged_carrier_repaired_once(self):
  l=self.runtime();l.execute("local id=GameInfo.Buildings.BUILDING_SPC_INSPIRATION_ERA_2.Index;a.pillaged[id]=true;refresh();assert(inspiration(a)==6 and not a.pillaged[id]);local n=writes;refresh();assert(writes==n)")
 def test_pending_same_turn_real_change_is_not_lost(self):
  l=self.runtime();l.execute(r"""
   a.eras=0;refresh();a.eras=1;local create=P.CreateBuilding;local once=false
   P.CreateBuilding=function(q,id)create(q,id);if q.city==a and not once then once=true;a.eras=2;shared.GreatWorkFacts.OnConfirmed(0,{1})end end
   refresh();assert(inspiration(a)==6 and not ins.pending)
  """)
 def test_upstream_callback_error_does_not_silence_new_consumer(self):
  l=self.runtime(False,real=True);l.execute(r"""
   local audit=data.Audit;data.Audit=function()error('AE_NOTIFY_FAILED')end
   sample(1,1,1)
   assert(inspiration(a)==3 and finalAmount(a,'SCIENCE')==3)
   assert(shared.GreatWorkFacts.ConsumerStatus('CultureAesthetic').error)
   data.Audit=audit;sample(2,1,1)
   assert(not shared.GreatWorkFacts.ConsumerStatus('CultureAesthetic').error and total(a)>0)
  """)
 def test_city_scoped_update_never_reads_shared_d_or_full_work_list(self):
  l=self.runtime();l.execute(r"""
   shared.DistrictCompleteness.Read=function()error('UNNEEDED_D_SCAN')end
   shared.GreatWorkFacts.Read=function()error('UNNEEDED_WORK_COPY')end
   for i=3,40 do local c=city(i);c.identity='RESEARCH' end
   local before=counts.city_scan;refresh();assert(counts.city_scan==before+1 and inspiration(a)==6)
   before=counts.city_scan;ins.Audit({player=0});assert(counts.city_scan==before+40 and not ins.error)
   local old=counts.city_scan;ins.Audit({player=3});assert(counts.city_scan==old)
  """)
 def test_readout_is_national_precise_readonly_and_bounded(self):
  l=self.runtime();l.execute(r"""
   Game.GetLocalPlayer=function()return 0 end
   Players[0].GetGreatPeoplePoints=function()return {GetPointsPerTurn=function()return 1.03 end,GetPointsTotal=function()return 50.199 end}end
   meaningRequest(0,{Action='INSPIRE_STATUS',CityID=1,Token='r'});local n=writes
   local out=SPCInspirationReadout.RenderAutomatic(P,shared.CultureInspirationView,'r',false)
   assert(out:find('1.030000') and out:find('50.199000') and out:find('NATIONAL') and writes==n)
   assert(SPCInspirationReadout.RenderAutomatic(P,shared.CultureInspirationView,'wrong',false):find('READ_UNKNOWN'))
   a.token='new';assert(SPCInspirationReadout.RenderAutomatic(P,shared.CultureInspirationView,'r',false):find('READ_UNKNOWN'))
  """)

 def test_automatic_native_detail_city_percent_sources_and_cache(self):
  l=self.runtime();l.execute(r"""
   Game.GetLocalPlayer=function()return 0 end
   Players[0].GetGreatPeoplePoints=function()return {GetPointsPerTurn=function()return 50.199 end,GetPointsTotal=function()return 400.5 end}end
   nativeCalls=0;defs={
    {Id='SPC_INSPIRATION_ERA_2',Arguments={Amount=6}},
    {Id='GARDEN_ADJUST_GREAT_PERSON_POINT_BONUS',Arguments={Amount=20}},
    {Id='HD_GOVERNOR_EDUCATOR_LEFT_1_GPP_BONUS',Arguments={Amount=100}}}
   GameEffects={GetModifiers=function()nativeCalls=nativeCalls+1;return {1,2,3}end,
    GetModifierDefinition=function(id)return defs[id]end,GetModifierOwner=function()return 101 end,
    GetObjectsPlayerId=function()return 0 end,GetObjectType=function()return 'CITY_UNVERIFIED'end,
    GetObjectString=function()return 'opaque city evidence'end,GetModifierSubjects=function()return {101}end,GetModifierActive=function()return true end}
   meaningRequest(0,{Action='INSPIRE_DETAIL',CityID=1,Token='d'})
   local view=shared.CultureInspirationView;SPCInspirationReadout.RenderAutomatic(P,view,'d',false);assert(nativeCalls==0)
   local n=writes;local out=SPCInspirationReadout.RenderAutomatic(P,view,'d',true)
   assert(out:find('DIAG_SCAN | COMPLETE | 1 | 0') and out:find('SPC_INSPIRATION_ERA_2 | true | 6'))
   assert(out:find('GARDEN_ADJUST_GREAT_PERSON_POINT_BONUS') and out:find('HD_GOVERNOR_EDUCATOR_LEFT_1_GPP_BONUS') and out:find('DIAG_MULTIPLIER'))
   SPCInspirationReadout.RenderAutomatic(P,view,'d',true);assert(nativeCalls==1 and writes==n)
   GameEffects=nil;view.token='e';out=SPCInspirationReadout.RenderAutomatic(P,view,'e',true);assert(out:find('DIAG_UNKNOWN') and not out:find('DIAG_NONE'))
  """)
 def test_panel_actual_callbacks_are_readonly_and_end_hidden(self):
  from test_p0_panel_current_layout import panel_runtime
  _,l=panel_runtime();l.execute(r"""
   assert(Controls.InspirationEndButton.hidden)
   Controls.MeaningConfigButton.callbacks[Mouse.eLClick]();assert(requests[#requests].Action=='INSPIRE_STATUS')
   Controls.MeaningConfigButton.callbacks[Mouse.eRClick]();assert(requests[#requests].Action=='INSPIRE_DETAIL')
  """)
 def test_startup_cleanup_failure_is_visible_and_city_scoped(self):
  l=self.runtime(False);l.execute(r"""
   seed(a,'BUILDING_SPC_INSPIRE_PROBE_10');failRemove=GameInfo.Buildings.BUILDING_SPC_INSPIRE_PROBE_10.Index
   fire('LoadScreenClose');assert(inspiration(a)==0 and ins.errors['0:1'] and inspiration(b)==6)
   assert(ins.Describe(0,b):find('CLEANUP_PENDING'))
   failRemove=nil;refresh();assert(retired(a)==0 and inspiration(a)==6 and not ins.errors['0:1'])
  """)
 def test_package_ui_and_localization_complete(self):
  root=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot();self.assertEqual(root.attrib['version'],'199')
  files=[e.text for e in root.find('Files')];imports=[e.text for e in root.findall("./InGameActions/ImportFiles[@id='SPCP0_Common']/File")]
  for name in ['CultureInspiration.lua','CultureInspirationModel.lua']:
   self.assertEqual(files.count(name),1);self.assertEqual(imports.count(name),1)
  self.assertEqual(files.count('Data/CultureInspiration.sql'),1)
  panel=(R/'Mod/UI/P0Panel.lua').read_text();self.assertIn("request('INSPIRE_STATUS')",panel);self.assertIn("request('INSPIRE_DETAIL')",panel);self.assertNotIn("request('INSPIRE_NEXT')",panel)
  xml=ET.parse(R/'Mod/UI/P0Panel.xml').getroot();self.assertEqual(xml.find(".//*[@ID='InspirationEndButton']").attrib['Hidden'],'1')
  db=sqlite3.connect(':memory:');db.execute('CREATE TABLE LocalizedText(Language,Tag,Text,PRIMARY KEY(Language,Tag))');db.executescript((R/'Mod/Text/TestText.sql').read_text())
  self.assertEqual(db.execute("SELECT COUNT(*) FROM LocalizedText WHERE Tag LIKE 'LOC_SPC_INSPIRATION_%'").fetchone()[0],32);db.close()

def load_tests(loader,tests,pattern):
 # Only directly affected regressions. Old package/probe-menu assertions remain
 # historical and are not rewritten to manufacture a current all-history PASS.
 for name in [
  'test_automatic_without_panel_two_cities_and_exact_final_values',
  'test_same_turn_d_replaces_old_single_value_and_duplicate_zero_writes',
  'test_active_downgrade_and_same_turn_governor_restoration',
  'test_cold_load_clears_saved_legacy_and_rebuilds_from_changed_facts',
  'test_confirmed_loss_exit_unknown_no_clear_and_recapture_current_gate',
  'test_actual_positive_dialogue_has_no_meaning_override']:
  tests.addTest(meaning.AutomaticMeaningTests(name))
 class RelatedAesthetic(ae.AestheticTests):
  @classmethod
  def setUpClass(cls):cls.sql=legacy.database() # exact owned SQL reset in memory
  @classmethod
  def tearDownClass(cls):cls.sql.close()
 for name in ['test_formula_and_two_cities','test_current_buildings_and_d_separation']:
  tests.addTest(RelatedAesthetic(name))
 for name in [
  'test_native_parameters_can_disagree_and_multiple_instances_not_hidden',
  'test_diagnostic_only_requested_cached_once_and_fresh_token_reads_again',
  'test_incomplete_native_enumeration_is_not_zero_and_rate_failure_does_not_hide_diagnostics',
  'test_unknown_owner_sparse_ids_and_api_failure_explicitly_incomplete',
  'test_unknown_native_fields_are_not_reported_complete',
  'test_percent_candidates_are_not_summed_and_foreign_subject_target_is_retained',
  'test_end_reports_native_residue_instead_of_claiming_complete_cleanup',
  'test_diagnostic_detail_is_bounded_and_does_not_interpret_missing_subjects']:
  tests.addTest(old.InspirationTests(name))
 import test_p0_panel_current_layout as panel
 cls=next(c for c in vars(panel).values() if isinstance(c,type) and issubclass(c,unittest.TestCase) and c is not unittest.TestCase)
 for name in ['test_meaning_both_clicks_are_read_only_status','test_core_read_and_detail_callbacks_keep_current_actions','test_unique_xml_control_ids_and_current_lua_parse']:
  tests.addTest(cls(name))
 return tests

if __name__=='__main__':unittest.main(verbosity=2)
