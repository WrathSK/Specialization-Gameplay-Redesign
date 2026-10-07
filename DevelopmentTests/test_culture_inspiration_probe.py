"""B167 native precision gate: local behavior/SQL only, not native fractional PASS."""
from pathlib import Path
import unittest, xml.etree.ElementTree as ET
import test_culture_aesthetic as ae
import test_culture_meaning_probe as legacy
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]
class InspirationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.sql=legacy.database()
  cls.sql.executescript((R/'Mod/Data/CultureInspirationProbe.sql').read_text())
 @classmethod
 def tearDownClass(cls):cls.sql.close()
 def runtime(self,ready=True):
  h=ae.AestheticTests();h.sql=self.sql;l=h.runtime(ready=False)
  for table,key in [('ModifierArguments','ModifierId'),('BuildingModifiers','BuildingType'),('GreatPersonClasses','GreatPersonClassType')]:
   cur=self.sql.execute('select * from '+table);cols=[x[0] for x in cur.description];rows=[dict(zip(cols,row))for row in cur]
   for i,row in enumerate(rows):row['Index']=i+1
   l.globals().GameInfo[table]=l.globals().db(ae.lua_table(l,rows),key)
  l.globals().include('CultureInspirationProbe')
  l.execute("""
   a.active=4;b.active=4;seq=0
   Locale.Lookup=function(k,...)local out={k};for _,v in ipairs({...})do out[#out+1]=tostring(v)end;return table.concat(out,' | ')end
   SPCCultureInspirationProbe.Start(P,shared);ip=shared.CultureInspirationProbe
   function req(action,c)seq=seq+1;return ip.Request(0,c or a,action,'r'..seq)end
   function amount(c)local n=0;for _,v in ipairs({1,3,6,10})do if c.present[GameInfo.Buildings['BUILDING_SPC_INSPIRE_PROBE_'..v].Index]then n=n+v/10 end end;return n end
  """)
  if ready:l.execute("fire('LoadScreenClose')")
  return l
 def test_exact_single_values_replace_and_end(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');assert(ip.stage==0 and amount(a)==0);for _,v in ipairs({0.1,0.3,0.6,1})do req('INSPIRE_NEXT');assert(math.abs(amount(a)-v)<1e-9 and amount(b)==0)end;req('INSPIRE_END');assert(amount(a)==0 and ip.stage==-1)")
 def test_duplicate_request_and_read_do_not_write(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');local n=writes;ip.Request(0,a,'INSPIRE_NEXT','r2');assert(ip.stage==1 and writes==n);req('INSPIRE_READ');assert(writes==n)")
 def test_different_city_cannot_steal_fixture(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');assert(req('INSPIRE_NEXT',b):find('INSPIRE_FINISH_PREVIOUS_CITY'));assert(amount(a)==0.1 and amount(b)==0)")
 def test_unknown_holds_confirmed_exit_clears(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');a.factsUnknown=true;ip.Audit(0);assert(amount(a)==0.1);a.factsUnknown=false;a.active=3;ip.Audit(0);assert(amount(a)==0 and ip.stage==-1)")
 def test_foreign_rejected_and_confirmed_loss_owned_only(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');local ordinary=GameInfo.Buildings.BUILDING_MONUMENT.Index;a.present[ordinary]=true;a.owner=3;exits.CultureInspirationProbe(a,{confirmed=true,targetID=1,origin={owner=0}});assert(amount(a)==0 and a.present[ordinary] and ip.stage==-1);assert(ip.Request(3,a,'INSPIRE_NEXT','foreign'):find('INSPIRE_OWNER_UNKNOWN'))")
 def test_unknown_loss_does_not_clear(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');exits.CultureInspirationProbe(a,{confirmed=false,targetID=1,origin={owner=0}});assert(amount(a)==0.1)")
 def test_reference_change_never_replays(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');a.token='new';ip.Audit(0);assert(amount(a)==0 and ip.stage==-1)")
 def test_load_cleanup_off_and_no_permanent_writes(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');fire('LoadScreenClose');assert(ip.ready and amount(a)==0 and ip.stage==-1 and a.token=='persistent:1');req('INSPIRE_READ');assert(amount(a)==0)")
 def test_missed_load_request_fallback(self):
  l=self.runtime(False);l.execute("req('INSPIRE_NEXT');assert(ip.ready and ip.stage==0)")
 def test_removal_failure_blocks_new_value(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');failRemove=GameInfo.Buildings.BUILDING_SPC_INSPIRE_PROBE_1.Index;assert(req('INSPIRE_NEXT'):find('INSPIRE_REMOVE_UNCONFIRMED'));assert(amount(a)==0.1 and ip.stage==1)")
 def test_create_failure_not_reported_applied(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');failCreate=true;assert(req('INSPIRE_NEXT'):find('INSPIRE_CREATE_UNCONFIRMED'));assert(amount(a)==0 and ip.stage==0 and not shared.CultureInspirationView)")
 def test_presence_unknown_blocks_mixed_write(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');failHas=GameInfo.Buildings.BUILDING_SPC_INSPIRE_PROBE_1.Index;local n=writes;req('INSPIRE_NEXT');assert(amount(a)==0.1 and writes==n)")
 def test_owner_change_during_create_retracts(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');local old=P.CreateBuilding;P.CreateBuilding=function(q,id)old(q,id);a.owner=3 end;req('INSPIRE_NEXT');assert(amount(a)==0 and not shared.CultureInspirationView)")
 def test_cleanup_failure_locks_until_load(self):
  l=self.runtime(False);l.execute("a.present[GameInfo.Buildings.BUILDING_SPC_INSPIRE_PROBE_1.Index]=true;failRemove=GameInfo.Buildings.BUILDING_SPC_INSPIRE_PROBE_1.Index;req('INSPIRE_NEXT');assert(not ip.ready);failRemove=nil;req('INSPIRE_NEXT');assert(not ip.ready and amount(a)==0.1);fire('LoadScreenClose');assert(ip.ready and amount(a)==0)")
 def test_wrong_identity_and_low_potential_rejected(self):
  l=self.runtime();l.execute("a.identity='RESEARCH';assert(req('INSPIRE_NEXT'):find('INSPIRE_REQUIRE_ACTIVE_IV'));a.identity='CULTURE';a.potential=3;assert(req('INSPIRE_NEXT'):find('INSPIRE_REQUIRE_ACTIVE_IV'));assert(amount(a)==0)")
 def test_no_target_idle_never_scans(self):
  l=self.runtime();l.execute("local n=writes;for i=1,3 do ip.Audit(0);fire('PlayerTurnActivated',0)end;assert(writes==n)")
 def test_native_readout_scope_and_stale_baseline(self):
  l=self.runtime();l.globals().include('InspirationReadout');l.execute("""
   Game.GetLocalPlayer=function()return 0 end;rate=50
   Players[0].GetGreatPeoplePoints=function()return {GetPointsPerTurn=function()return rate end}end
   req('INSPIRE_NEXT');local s=SPCInspirationReadout.Render(P,shared.CultureInspirationView,'r1','INSPIRE_NEXT');assert(s:find('50.000') and s:find('0.000'))
   req('INSPIRE_NEXT');rate=50.1;s=SPCInspirationReadout.Render(P,shared.CultureInspirationView,'r2','INSPIRE_NEXT');assert(s:find('0.100'))
   turn=turn+1;s=SPCInspirationReadout.Render(P,shared.CultureInspirationView,'r2','INSPIRE_READ');assert(s:find('NO_BASELINE'))
   rate=nil;s=SPCInspirationReadout.Render(P,shared.CultureInspirationView,'r2','INSPIRE_READ');assert(s:find('READ_UNKNOWN'))
  """)
 def test_actual_dispatch_and_readonly_ui_hooks(self):
  l=self.runtime()
  src=(R/'Mod/Gameplay.lua').read_text();a=src.index("  if type(params.Action)=='string' and params.Action:find('^INSPIRE_')");b=src.index('  if shared.CultureMeaning',a)
  l.execute('function route(playerID,params) '+src[a:b]+' end');l.execute("route(0,{Action='INSPIRE_NEXT',CityID=1,Token='dispatch'});assert(shared.LastToken=='dispatch' and ip.stage==0)")
  panel=(R/'Mod/UI/P0Panel.lua').read_text();self.assertIn("request('INSPIRE_READ')",panel);self.assertIn("request('INSPIRE_END')",panel)
 def test_unknown_active_is_not_confirmed_inactive(self):
  l=self.runtime();l.execute("req('INSPIRE_NEXT');req('INSPIRE_NEXT');local old=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(pid,c)local f=old(pid,c);f.activeStatus='UNKNOWN_GOVERNOR';f.active=1;return f end;ip.Audit(0);assert(amount(a)==0.1 and ip.error:find('INSPIRE_ACTIVE_UNKNOWN'))")
 def test_native_end_delta_and_wrong_token(self):
  l=self.runtime();l.globals().include('InspirationReadout');l.execute("""
   Game.GetLocalPlayer=function()return 0 end;rate=50
   Players[0].GetGreatPeoplePoints=function()return {GetPointsPerTurn=function()return rate end}end
   req('INSPIRE_NEXT');SPCInspirationReadout.Render(P,shared.CultureInspirationView,'r1','INSPIRE_NEXT')
   req('INSPIRE_NEXT');rate=50.1;SPCInspirationReadout.Render(P,shared.CultureInspirationView,'r2','INSPIRE_NEXT')
   req('INSPIRE_END');rate=50;local s=SPCInspirationReadout.Render(P,shared.CultureInspirationView,'r3','INSPIRE_END');assert(s:find('0.000'))
   assert(SPCInspirationReadout.Render(P,shared.CultureInspirationView,'wrong','INSPIRE_READ'):find('READ_UNKNOWN'))
  """)
 def test_probe_and_normal_meaning_coexist(self):
  import test_culture_meaning_automatic as auto
  h=auto.AutomaticMeaningTests();h.sql=self.sql;l=h.runtime()
  for table,key in [('ModifierArguments','ModifierId'),('BuildingModifiers','BuildingType')]:
   cur=self.sql.execute('select * from '+table);cols=[x[0] for x in cur.description];rows=[dict(zip(cols,row))for row in cur]
   l.globals().GameInfo[table]=l.globals().db(ae.lua_table(l,rows),key)
  l.globals().include('CultureInspirationProbe');l.execute("""
   Locale={Lookup=function(k,...)return k end};SPCCultureInspirationProbe.Start(P,shared);ip=shared.CultureInspirationProbe
   local before=finalAmount(a,'SCIENCE');local other=finalAmount(b,'SCIENCE')
   ip.Request(0,a,'INSPIRE_NEXT','a');ip.Request(0,a,'INSPIRE_NEXT','b');assert(ip.stage==1)
   update();assert(finalAmount(a,'SCIENCE')==before and finalAmount(b,'SCIENCE')==other)
   ip.Request(0,a,'INSPIRE_END','c');update();assert(finalAmount(a,'SCIENCE')==before and finalAmount(b,'SCIENCE')==other)
  """)
 def test_sql_and_package(self):
  rows=self.sql.execute("select Value from ModifierArguments where ModifierId like 'SPC_INSPIRE_PROBE_%' and Name='Amount'").fetchall();self.assertEqual(sorted(float(x[0])for x in rows),[.1,.3,.6,1])
  tree=ET.parse(R/'Mod/SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'194')
  for f in ['CultureInspirationProbe.lua','InspirationReadout.lua','Data/CultureInspirationProbe.sql']:
   self.assertEqual([x.text for x in tree.findall('./Files/File')].count(f),1)
  xml=ET.parse(R/'Mod/UI/P0Panel.xml');ids=[n.get('ID')for n in xml.iter()if n.get('ID')];self.assertEqual(len(ids),len(set(ids)))
 def test_changed_lua_parses(self):
  l=LuaRuntime();parse=l.eval('function(s) local f,e=load(s);return f~=nil,e end')
  for f in ['CultureInspirationProbe.lua','InspirationReadout.lua','Gameplay.lua','UI/P0Panel.lua','Probe.lua']:
   ok,error=parse((R/'Mod'/f).read_text());self.assertTrue(ok,(f,error))
def load_tests(loader,tests,pattern):
 import test_culture_meaning_automatic as auto
 for name in ['test_automatic_without_panel_two_cities_and_exact_final_values','test_same_turn_d_replaces_old_single_value_and_duplicate_zero_writes','test_active_downgrade_and_same_turn_governor_restoration','test_cold_load_clears_saved_legacy_and_rebuilds_from_changed_facts','test_confirmed_loss_exit_unknown_no_clear_and_recapture_current_gate','test_actual_positive_dialogue_has_no_meaning_override']:
  tests.addTest(auto.AutomaticMeaningTests(name))
 return tests
if __name__=='__main__':unittest.main(verbosity=2)
