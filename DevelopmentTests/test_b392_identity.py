"""B392 restricted-Lua identity regression; local simulation, not native PASS."""
from pathlib import Path
from unittest.mock import patch
import unittest
from lupa.lua51 import LuaRuntime
from refactor_harness import ROOT,TrackedLua51,Context

HELPER=ROOT/'Mod/IdentityEqual.lua'
class Compatibility(unittest.TestCase):
 def test_identity_preserves_raw_semantics_without_optional_functions(self):
  v=LuaRuntime();v.execute(HELPER.read_text())
  v.execute("""
   local original=rawequal;rawequal=nil;rawget=nil;rawset=nil
   local eq=SPCIdentityEqual.Same
   local mt={__eq=function()error('METAMETHOD_MUST_NOT_RUN')end}
   local a,b=setmetatable({},mt),setmetatable({},mt)
   assert(eq(a,a)and not eq(a,b)and not eq(nil,a)and eq(nil,nil))
   assert(eq(false,false)and not eq(false,nil)and not eq(false,0))
   assert(eq(1,1)and not eq(1,'1')and not eq(0/0,0/0))
   local u,w=newproxy(true),newproxy(true);local m=getmetatable(u)
   m.__eq=function()error('USERDATA_EQ_MUST_NOT_RUN')end
   assert(eq(u,u)and not eq(u,w))
   local fn=function()end;local co=coroutine.create(fn)
   assert(eq(fn,fn)and not eq(fn,function()end)and eq(co,co))
   local weak=setmetatable({},{__mode='v'})
   do local x,y={},{};weak[1]=x;weak[2]=y;for i=1,1000 do assert(not eq(x,y))end end
   collectgarbage('collect');assert(weak[1]==nil and weak[2]==nil)
   assert(rawequal==nil and rawget==nil and rawset==nil)
  """)
 def test_actual_store_and_facts_recover_without_raw_equality(self):
  from test_refactor_s9a3a import runtime
  v=runtime();v.execute("rawequal=nil;local writes=T.writes();assert(shared.CityProgressionStore.Base(0,ca));assert(shared.EffectiveFacts.Read(0,ca).specialization=='RESEARCH');assert(T.writes()==writes);a=shared.InvestmentAction;T.invest(ca,99891);assert(shared.EffectiveFacts.Read(0,ca).potential==2)")
 def test_fresh_city_establishment_in_restricted_context_from_start(self):
  from test_refactor_s9a3a import runtime
  original=TrackedLua51.__init__
  def restricted(vm,*a,**kw):
   original(vm,*a,**kw);vm.execute('rawequal=nil')
  with patch.object(TrackedLua51,'__init__',restricted):
   v=runtime()
   v.execute("assert(shared.EffectiveFacts.Read(0,ca).specialization=='RESEARCH');assert(shared.EffectiveFacts.Read(0,cb).specialization=='CULTURE');assert(rawequal==nil)")
 def test_actual_ui_request_and_reply_and_same_turn_promotion(self):
  import test_culture_institutions as display
  from test_b265_city_presentation import presentation
  with patch.object(display,'LuaRuntime',TrackedLua51):
   v=presentation('rawequal=nil')
   v.execute("assert(Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_3');nativeActive=4;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete();assert(rows.items[4].State.text=='当前'and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_4');for _,r in ipairs(trace)do assert(r.stage~='INSTITUTION_UI_FAILURE')end;local n=#requests;for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(#requests==n)")
 def test_production_owner_observer_rejects_equal_but_replaced_table(self):
  v=LuaRuntime();v.execute(HELPER.read_text());v.execute((ROOT/'Mod/UI/SafeAdapters.lua').read_text())
  v.execute("rawequal=nil;local m={__eq=function()return true end};local a=setmetatable({revision=1},m);local b=setmetatable({revision=1},m);local d=SPCSafeAdapters.NewViewObserver();assert(d.SourceChanged(a));assert(not d.SourceChanged(a));assert(d.SourceChanged(b));assert(not d.SourceChanged(b))")
 def test_runtime_has_no_remaining_optional_raw_equality_calls(self):
  for p in (ROOT/'Mod').rglob('*.lua'):
   self.assertNotIn('rawequal(',p.read_text(),str(p))

if __name__=='__main__':
 # Frozen UI fixtures stub include; explicitly load the real new pure dependency.
 # Assertions and old source comparisons remain unchanged.
 modules=['test_refactor_s9a3a','test_refactor_s9a3c','test_refactor_s9a3d','test_refactor_s9a3e',
  'test_refactor_s9b3','test_refactor_s9c4b','test_refactor_s9c5b','test_refactor_s9c6b',
  'test_refactor_s9d1']
 loader=unittest.TestLoader();suite=loader.loadTestsFromTestCase(Compatibility)
 # Direct classes only: avoid repeatedly expanding inherited stage closures.
 import importlib
 for name in modules:
  module=importlib.import_module(name)
  for cls in vars(module).values():
   if isinstance(cls,type)and issubclass(cls,unittest.TestCase)and cls.__module__==name:
    suite.addTests(loader.loadTestsFromTestCase(cls))
 result=unittest.TextTestRunner(verbosity=2).run(suite)
 raise SystemExit(not result.wasSuccessful())
