"""B117 primitive guard/UI tests. Engine storage/clamp semantics remain native-only."""
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from lupa.lua55 import LuaRuntime
import test_b116_empty_target as prior
ROOT=Path(__file__).resolve().parents[1]
GP=(ROOT/'Mod/OverflowStorageProbe.lua').read_text()
UI=(ROOT/'Mod/UI/OverflowStorageRead.lua').read_text()
class ObserverRegression(prior.EmptyTargetTests):
 def test_static(self):
  for f in ['Mod/Gameplay.lua','Mod/TimedProductionProbe.lua','Mod/UI/TimedTurnProbe.lua','Mod/UI/P0Panel.lua','Mod/Probe.lua','Mod/OverflowStorageProbe.lua','Mod/UI/OverflowStorageRead.lua']:
   self.lua.execute('assert(load(...))',(ROOT/f).read_text())
  doc=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(doc.getroot().get('version'),'144')
  files=[n.text for n in doc.findall('./Files/File')];self.assertEqual(len(files),len(set(files)))
  self.assertTrue(all((ROOT/'Mod'/n).is_file() for n in files))
  for x in ['SetProperty','AddProgress','FinishProgress','RequestOperation','SetUpdate']:self.assertNotIn(x,prior.previous.GP)
  self.assertNotIn('SetUpdate',UI)
  self.assertIn('Controls.GWAReadButtonCaption:SetText("溢出清除试验")',(ROOT/'Mod/UI/P0Panel.lua').read_text())
FIXTURE=r'''
function event() local t={f={}};t.Add=function(f)table.insert(t.f,f)end;return setmetatable(t,{__call=function(_,...)for _,f in ipairs(t.f)do f(...)end end})end
Events={};for _,n in ipairs({'CityProductionChanged','CityProductionQueueChanged','CityProductionUpdated','CityProductionCompleted','CityRemovedFromMap'})do Events[n]=event()end
turn=20;owner=0;id=10;x=2;target='NONE';size=0;writes=0;sum=0;progress=17;selected=true;mode='storage';pool=8;fail=false;defer=false;shown='';packets={}
Game={GetCurrentGameTurn=function()return turn end,GetLocalPlayer=function()return 0 end}
q={CurrentlyBuilding=function()return target end,GetSize=function()return size end,
 AddProgress=function(_,v) writes=writes+1;sum=sum+v;if fail then error('native unknown')end
 if mode=='storage' then pool=math.max(0,pool+v) elseif mode=='debt' then pool=pool+v elseif mode=='target' then progress=math.max(0,progress+v)end end,
 GetBuildingProgress=function()return progress end,GetUnitProgress=function()return 0 end,GetDistrictProgress=function()return 0 end,GetProjectProgress=function()return 0 end}
c={GetOwner=function()return owner end,GetID=function()return id end,GetX=function()return x end,GetY=function()return 3 end,GetBuildQueue=function()return q end}
Players={[0]={GetCities=function()return {FindID=function(_,v)if v==id then return c end end}end}}
P={IsTestPlayer=function(pid)return pid==0 end,Field=function(o,k)return o and o[k]end,Call=function(o,k,...)if not o or not o[k]then return false,'MISSING'end;return pcall(o[k],o,...)end}
shared={};ExposedMembers={SPC_P0=shared};UI={GetHeadSelectedCity=function()if selected then return c end end};Locale={Lookup=function(v)return v end};PlayerOperations={EXECUTE_SCRIPT=1}
local function catalog(rows)return setmetatable(rows,{__call=function(t)local i=0;return function()i=i+1;return t[i]end end})end
GameInfo={Buildings=catalog({{Index=1,Name='old building'}}),Units=catalog({}),Projects=catalog({}),Districts=catalog({})}
function send(pid,op,p) packets[#packets+1]=p;if not defer then shared.OverflowStorageProbe.Request(pid,p)end end
function prep(tok)shared.OverflowStorageProbe.Request(0,{Action='OVERFLOW_PREPARE',Token=tok or 't',CityID=10,StartTurn=20})end
function apply(tok)shared.OverflowStorageProbe.Request(0,{Action='OVERFLOW_APPLY',Token=tok or 't',CityID=10,StartTurn=20})end
'''
class OverflowTests(unittest.TestCase):
 def setUp(self):
  self.lua=LuaRuntime(unpack_returned_tuples=True);self.runlua(FIXTURE);self.runlua(GP);self.runlua('SPCOverflowStorageProbe.Start(P,shared)');self.runlua(UI);self.runlua('ui=SPCOverflowStorageRead.New(P,function(s)shown=s end,send)')
 def runlua(self,s):return self.lua.execute(s)
 def get(self,s):return self.lua.eval(s)
 def test_prepare_read_only(self):
  self.runlua('prep()');self.assertEqual(self.get('writes'),0);self.assertEqual(self.get('shared.OverflowStorage.status'),'PREPARED')
 def test_confirm_one_call_only(self):
  self.runlua('prep();apply();apply();prep("second");apply("second")');self.assertEqual(self.get('writes'),1);self.assertEqual(self.get('sum'),-1000)
 def test_nonempty_never_writes(self):
  for condition in ["target='BUILDING_OLD'",'size=1',"target=0"]:
   self.setUp();self.runlua('prep();'+condition+';apply()');self.assertEqual(self.get('writes'),0)
 def test_stale_city_turn_owner_never_writes(self):
  for condition in ['turn=21','x=99','owner=3','id=11']:
   self.setUp();self.runlua('prep();'+condition+';apply()');self.assertEqual(self.get('writes'),0)
 def test_changed_and_back_is_invalidated(self):
  self.runlua('prep();Events.CityProductionChanged(0,10);apply()');self.assertEqual(self.get('writes'),0)
 def test_unrelated_events_do_not_cancel(self):
  self.runlua('prep();Events.CityProductionChanged(0,11);Events.CityProductionChanged(3,10);apply()');self.assertEqual(self.get('writes'),1)
 def test_wrong_token(self):
  self.runlua('prep();apply("other")');self.assertEqual(self.get('writes'),0)
 def test_no_prepare(self):
  self.runlua('apply()');self.assertEqual(self.get('writes'),0)
 def test_native_exception_latches(self):
  self.runlua('prep();fail=true;apply()');self.assertEqual(self.get('shared.OverflowStorage.status'),'UNCERTAIN_NO_RETRY');self.runlua('fail=false;apply()');self.assertEqual(self.get('writes'),1)
 def test_missing_api_refuses(self):
  self.runlua('q.AddProgress=nil;prep();apply()');self.assertEqual(self.get('writes'),0)
 def test_missing_event_refuses(self):
  self.runlua('Events.CityProductionUpdated=nil;SPCOverflowStorageProbe.Start(P,shared);prep();apply()');self.assertEqual(self.get('writes'),0)
 def test_no_size_api_still_requires_target(self):
  self.runlua('q.GetSize=nil;prep();apply()');self.assertEqual(self.get('writes'),1)
 def test_other_player_rejected(self):
  self.runlua("shared.OverflowStorageProbe.Request(3,{Action='OVERFLOW_PREPARE',Token='x',CityID=10,StartTurn=20})");self.assertEqual(self.get('writes'),0)
 def test_no_native_clear_claim_for_models(self):
  for model in ['storage','debt','target']:
   self.setUp();self.runlua("mode='"+model+"';prep();apply()");self.assertEqual(self.get('shared.OverflowStorage.status'),'CALLED_NOT_PROVEN')
 def test_ui_two_clicks_and_read_no_write(self):
  self.runlua('ui.Click();ui.Read()');self.assertEqual(self.get('writes'),0)
  self.runlua('ui.Click()');self.assertEqual(self.get('writes'),1);self.assertIn('未变化',self.get('shown'))
  self.runlua('ui.Read();ui.Read()');self.assertEqual(self.get('writes'),1)
 def test_ui_existing_progress_damage_visible(self):
  self.runlua("mode='target';ui.Click();ui.Click()");self.assertIn('停止实验',self.get('shown'))
 def test_ui_snapshot_change_blocks(self):
  self.runlua('ui.Click();progress=18;ui.Click()');self.assertEqual(self.get('writes'),0)
 def test_ui_unknown_progress_blocks(self):
  self.runlua('q.GetBuildingProgress=function()return nil end;ui.Click()');self.assertEqual(self.get('#packets'),0)
 def test_ui_nonempty_blocks(self):
  self.runlua('size=1;ui.Click()');self.assertEqual(self.get('#packets'),0)
 def test_ui_wrong_selection_blocks(self):
  self.runlua('ui.Click();selected=false;ui.Click()');self.assertEqual(self.get('writes'),0)
 def test_ui_async_no_automatic_retry(self):
  self.runlua('defer=true;ui.Click();ui.Click();ui.Read()');self.assertEqual(self.get('#packets'),1)
  self.runlua('shared.OverflowStorageProbe.Request(0,packets[1]);ui.Pulse();ui.Click();ui.Click()');self.assertEqual(self.get('#packets'),2);self.assertEqual(self.get('writes'),0)
  self.runlua('shared.OverflowStorageProbe.Request(0,packets[2]);ui.Pulse()');self.assertEqual(self.get('writes'),1)
 def test_ui_negative_values_not_hidden(self):
  self.runlua('ui.Click();ui.Click();progress=-3;ui.Read()');self.assertIn('=-3',self.get('shown'))
 def test_actual_panel_report_scope(self):
  self.runlua('SPCP0=P;include=function()end;SPCCityIdentityEvidence={New=function()return {}end};Events.GameCoreEventPublishComplete=event();Controls={Status={SetText=function(_,s)shown=s end}};UI.RequestPlayerOperation=send')
  prefix=(ROOT/'Mod/UI/P0Panel.lua').read_text().split('local function trace(s)')[0]
  panel=self.lua.execute(prefix+'\nreturn overflowRead')
  panel.Click();self.assertIn('尚未执行',self.get('shown'))
  panel.Click();self.assertIn('未变化',self.get('shown'));self.assertEqual(self.get('writes'),1)
 def test_actual_dispatch(self):
  self.runlua('SPCP0=P;P.Scalar=tostring;P.VERSION="B117";SPCPerformance={New=function()return {}end};include=function()end')
  source=(ROOT/'Mod/Gameplay.lua').read_text().split('GameEvents.SPC_P0_Request.Add(function(...)')[0]
  fn=self.lua.execute(source+'\nreturn request')
  self.runlua('SPCOverflowStorageProbe.Start(P,ExposedMembers.SPC_P0)')
  packet=self.lua.table_from({'Action':'OVERFLOW_PREPARE','Token':'dispatch','CityID':10,'StartTurn':20})
  fn(0,packet);packet['Action']='OVERFLOW_APPLY';fn(0,packet);self.assertEqual(self.get('writes'),1)
if __name__=='__main__':unittest.main()
