"""B118 bounded exact-project primitive; native subtraction semantics NOT proven."""
import unittest, sqlite3, xml.etree.ElementTree as ET
from pathlib import Path
from lupa.lua55 import LuaRuntime
import test_b117_overflow_storage as old
ROOT=old.ROOT
GP=(ROOT/'Mod/OverflowStorageProbe.lua').read_text(); UI=(ROOT/'Mod/UI/OverflowStorageRead.lua').read_text()
EXTRA=r'''
project='PROJECT_SPC_OVERFLOW_SINK_TEST'; target=project;size=1;pp=8;pool=0;mode='project'
GameInfo.Projects=setmetatable({{Index=7,Hash=777,Name='test project'},[project]={Index=7,Hash=777,Name='test project'}},{__call=function(t)local done=false;return function()if not done then done=true;return t[1]end end end})
q.GetCurrentProductionTypeHash=function()return target==project and 777 or 9 end
q.GetProjectProgress=function()return pp end
q.AddProgress=function(_,v)writes=writes+1;sum=sum+v;if fail then error('native failure')end
 if mode=='project' then pp=pp+v elseif mode=='debt' then pool=pool+v elseif mode=='damage' then pp=pp+v;progress=0 end end
function prep(tok)shared.OverflowStorageProbe.Request(0,{Action='OVERFLOW_PREPARE',Token=tok or 't',CityID=10,StartTurn=20,Progress=pp})end
function apply(tok)shared.OverflowStorageProbe.Request(0,{Action='OVERFLOW_APPLY',Token=tok or 't',CityID=10,StartTurn=20,Progress=pp})end
'''
class ExactTests(unittest.TestCase):
 def setUp(self):
  self.lua=LuaRuntime(unpack_returned_tuples=True);self.runlua(old.FIXTURE);self.runlua(EXTRA);self.runlua(GP);self.runlua('SPCOverflowStorageProbe.Start(P,shared)');self.runlua(UI);self.runlua('ui=SPCOverflowStorageRead.New(P,function(s)shown=s end,send)')
 def runlua(self,s):return self.lua.execute(s)
 def get(self,s):return self.lua.eval(s)
 def test_prepare_no_write(self):
  self.runlua('ui.Click();ui.Read()');self.assertEqual(self.get('writes'),0);self.assertIn('尚未执行',self.get('shown'))
 def test_exact_once(self):
  self.runlua('ui.Click();ui.Click();ui.Click();ui.Read()');self.assertEqual(self.get('writes'),1);self.assertEqual(self.get('pp'),0);self.assertEqual(self.get('progress'),17)
 def test_fraction_not_rounded(self):
  self.runlua('pp=8.3;ui.Click();ui.Click()');self.assertAlmostEqual(self.get('sum'),-8.3)
 def test_invalid_values(self):
  for v in ['0','-1','10001','0/0','math.huge']:
   self.setUp();self.runlua('pp='+v+';ui.Click()');self.assertEqual(self.get('writes'),0)
 def test_wrong_target_queue(self):
  for x in ["target='NONE'","target='BUILDING_OLD'",'size=0','size=2']:
   self.setUp();self.runlua(x+';ui.Click()');self.assertEqual(self.get('#packets'),0)
 def test_changed_progress(self):
  self.runlua('ui.Click();pp=9;ui.Click()');self.assertEqual(self.get('writes'),0)
 def test_changed_other_progress(self):
  self.runlua('ui.Click();progress=18;ui.Click()');self.assertEqual(self.get('writes'),0)
 def test_guard_changes(self):
  for x in ['turn=21','owner=3','x=99',"target='NONE'",'size=2','pp=9']:
   self.setUp();self.runlua('prep();'+x+';apply()');self.assertEqual(self.get('writes'),0)
 def test_event_invalidates_even_back(self):
  self.runlua('prep();Events.CityProductionChanged(0,10);apply()');self.assertEqual(self.get('writes'),0)
 def test_unrelated_event(self):
  self.runlua('prep();Events.CityProductionUpdated(0,11);apply()');self.assertEqual(self.get('writes'),1)
 def test_no_prepare_or_bad_token(self):
  self.runlua('apply();prep();apply("wrong")');self.assertEqual(self.get('writes'),0)
 def test_missing_reader(self):
  self.runlua('prep();shared.OverflowExactRead=nil;apply()');self.assertEqual(self.get('writes'),0)
 def test_delayed_request_rechecks_progress(self):
  self.runlua('ui.Click();defer=true;ui.Click();pp=9;shared.OverflowStorageProbe.Request(0,packets[2]);ui.Pulse()');self.assertEqual(self.get('writes'),0)
 def test_native_error_no_retry(self):
  self.runlua('prep();fail=true;apply();fail=false;apply()');self.assertEqual(self.get('writes'),1)
 def test_hidden_debt_not_pass(self):
  self.runlua("mode='debt';ui.Click();ui.Click()");self.assertIn('停止',self.get('shown'));self.assertEqual(self.get('shared.OverflowStorage.status'),'CALLED_NOT_PROVEN')
 def test_other_damage_visible(self):
  self.runlua("mode='damage';ui.Click();ui.Click()");self.assertIn('停止',self.get('shown'))
 def test_negative_report(self):
  self.runlua('ui.Click();ui.Click();pp=-3;ui.Read()');self.assertIn('=-3',self.get('shown'))
 def test_ui_wait_no_retry(self):
  self.runlua('defer=true;ui.Click();ui.Click();ui.Read()');self.assertEqual(self.get('#packets'),1)
 def test_missing_project(self):
  self.runlua('GameInfo.Projects[project]=nil;ui.Click()');self.assertEqual(self.get('writes'),0)
 def test_actual_panel(self):
  self.runlua('SPCP0=P;include=function()end;SPCCityIdentityEvidence={New=function()return {}end};Events.GameCoreEventPublishComplete=event();Controls={Status={SetText=function(_,s)shown=s end}};UI.RequestPlayerOperation=send')
  panel=self.lua.execute((ROOT/'Mod/UI/P0Panel.lua').read_text().split('local function trace(s)')[0]+'\nreturn overflowRead')
  panel.Click();panel.Click();self.assertEqual(self.get('writes'),1);self.assertIn('→0',self.get('shown'))
 def test_dispatch(self):
  self.runlua('SPCP0=P;P.Scalar=tostring;P.VERSION="B118";SPCPerformance={New=function()return {}end};include=function()end')
  fn=self.lua.execute((ROOT/'Mod/Gameplay.lua').read_text().split('GameEvents.SPC_P0_Request.Add(function(...)')[0]+'\nreturn request')
  self.runlua('SPCOverflowStorageProbe.Start(P,ExposedMembers.SPC_P0);SPCOverflowStorageRead.New(P,function()end,send)')
  packet=self.lua.table_from(dict(Action='OVERFLOW_PREPARE',Token='dispatch',CityID=10,StartTurn=20,Progress=8));fn(0,packet);packet['Action']='OVERFLOW_APPLY';fn(0,packet);self.assertEqual(self.get('writes'),1)
class Regression(old.prior.EmptyTargetTests):
 def test_static(self):
  for f in ['Mod/OverflowStorageProbe.lua','Mod/UI/OverflowStorageRead.lua','Mod/UI/P0Panel.lua','Mod/Gameplay.lua','Mod/Probe.lua']:
   self.lua.execute('assert(load(...))',(ROOT/f).read_text())
  doc=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(doc.getroot().get('version'),'145')
  files=[n.text for n in doc.findall('./Files/File')];self.assertEqual(len(files),len(set(files)));self.assertTrue(all((ROOT/'Mod'/f).is_file() for f in files))
  self.assertNotIn('AddProgress(-1000)',GP);self.assertNotIn('SetUpdate',UI)
  self.assertIn('精确扣除试验',(ROOT/'Mod/UI/P0Panel.lua').read_text())
  db=sqlite3.connect(':memory:');db.executescript('CREATE TABLE Types(Type TEXT PRIMARY KEY,Kind TEXT);CREATE TABLE Projects(ProjectType TEXT PRIMARY KEY,Name TEXT,ShortName TEXT,Description TEXT,Cost INT,CostProgressionModel TEXT,PrereqDistrict TEXT);');sql=(ROOT/'Mod/Data/OverflowSinkTest.sql').read_text();db.executescript(sql);self.assertEqual(db.execute('select Cost from Projects').fetchone()[0],1000000)
  self.assertNotIn('INSERT INTO ProjectCompletionModifiers',sql)
if __name__=='__main__':unittest.main()
