"""Pure bounded deferred lifecycle evidence. Not yet wired to production Store."""
import json,unittest
from refactor_harness import Context,ROOT,measure
from lupa.lua51 import lua_type

SETUP="""
M=SPCStoreDeferredLifecycle
origin={owner=0,cityID=9,x=4,y=5}
r={schema=2,base={token='CITY'},origin=origin,ownerChanges=1,stage='HELD_TRANSFER',loss={origin=origin,target={owner=3,cityID=20,x=4,y=5}}}
function returned(turn,id)
 r.stage='ACTIVE';r.current={owner=0,cityID=id or 19,x=4,y=5};r.lastLoss=r.loss;r.loss=nil
 return M.Return(v,r,{},turn)
end
function loss(turn,owner,id)
 r.ownerChanges=r.ownerChanges+1;r.stage='HELD_TRANSFER';r.loss={origin=origin,target={owner=owner,cityID=id,x=4,y=5}}
 return M.Loss(v,r,{},turn)
end
"""

def fixture():
 v=Context();v.load('StoreDeferredLifecycle');v.execute(SETUP);return v


def plain(x):return {k:plain(v)for k,v in x.items()}if lua_type(x)=='table'else x


class Model(unittest.TestCase):
 def test_all_nine_owners_coalesce_with_no_native_or_saved_side_effect(self):
  v=fixture();v.execute("local all={};for _,key in ipairs(M.Keys())do all[key]=true end;v=M.Loss(nil,r,all,0);local n=0;for _ in pairs(v.entries)do n=n+1 end;assert(n==9 and M.Validate(v,r)==v);v=returned(5);for _,key in ipairs(M.Keys())do local e=M.Entry(v,key,r);assert(e.key==key and e.token=='CITY'and e.epoch==1 and e.firstTurn==0 and e.lossTurn==0 and e.returnTurn==5 and e.returned.cityID==19);v=M.Clear(v,key,e,r)end;assert(v==nil)")
  measure('S9f1_deferred_model_bound',{'owners':9,'episodes_per_owner':1,'automatic_calls':0,'native_or_Property_access':0,'Store_wired':False})
 def test_duplicate_loss_and_return_preserve_first_observed_boundaries(self):
  v=fixture();v.execute("v=M.Loss(nil,r,{commerce=true},10);v=M.Loss(v,r,{commerce=true},12);assert(v.entries.commerce.lossTurn==10);v=returned(20);v=M.Return(v,r,{commerce=true},25);assert(v.entries.commerce.returnTurn==20 and v.entries.commerce.firstTurn==10)")
 def test_multiple_pending_episodes_keep_first_unresolved_turn_and_latest_loss(self):
  v=fixture();v.execute("v=M.Loss(nil,r,{researchTradition=true},2);v=returned(4);v=loss(7,8,28);assert(v.entries.researchTradition.epoch==2 and v.entries.researchTradition.firstTurn==2 and v.entries.researchTradition.lossTurn==7 and v.entries.researchTradition.returned==nil);v=returned(9,29);assert(v.entries.researchTradition.returnTurn==9 and v.entries.researchTradition.returned.cityID==29)")
 def test_return_only_never_invents_a_prior_loss_turn(self):
  v=fixture();v.execute("r.stage='ACTIVE';r.current={owner=0,cityID=19,x=4,y=5};r.lastLoss=r.loss;r.loss=nil;v=M.Return(nil,r,{commerce=true},40);assert(v.entries.commerce.lossTurn==nil and v.entries.commerce.firstTurn==40 and v.entries.commerce.returnTurn==40)")
 def test_no_wanted_or_existing_owner_keeps_optional_field_absent(self):
  v=fixture();v.execute("assert(M.Loss(nil,r,{},0)==nil);assert(returned(1)==nil);assert(M.Entry(nil,'commerce',r)==nil)")
 def test_clearing_one_owner_keeps_independent_pending_owners(self):
  v=fixture();v.execute("v=M.Loss(nil,r,{commerce=true,capital=true},10);local old=v;local e=M.Entry(v,'commerce',r);v=M.Clear(v,'commerce',e,r);assert(v.entries.commerce==nil and v.entries.capital and old.entries.commerce and old.entries.capital)")
 def test_detached_keys_and_witnesses_cannot_mutate_existing_evidence(self):
  v=fixture();v.execute("local keys=M.Keys();keys[1]='FORGED';assert(M.Keys()[1]=='expeditionInsights');v=M.Loss(nil,r,{commerce=true},3);local e=M.Entry(v,'commerce',r);e.lossTarget.cityID=999;assert(v.entries.commerce.lossTarget.cityID==20)")
 def test_stale_cross_owner_and_cross_token_witnesses_cannot_clear(self):
  v=fixture();v.execute("v=M.Loss(nil,r,{commerce=true,capital=true},3);local e=M.Entry(v,'commerce',r);assert(not pcall(M.Clear,v,'capital',e,r));e.token='OTHER';assert(not pcall(M.Clear,v,'commerce',e,r));e=M.Entry(v,'commerce',r);v=returned(4);assert(not pcall(M.Clear,v,'commerce',e,r));assert(v.entries.commerce and v.entries.capital)")
 def test_unknown_fields_owner_versions_and_extra_owners_are_rejected(self):
  for mutation in ("v.version=2","v.extra=true","v.entries.UNKNOWN=v.entries.commerce","v.entries.commerce.extra=true","v.entries.commerce.lossTarget.extra=true","v.entries={}"):
   v=fixture();v.execute("v=M.Loss(nil,r,{commerce=true},3);"+mutation+";assert(not pcall(M.Validate,v,r))")
 def test_wrong_parent_epoch_reference_and_stage_are_rejected(self):
  for mutation in ("r.base.token='OTHER'","r.ownerChanges=2","r.origin.x=6","r.loss.target.cityID=21","r.stage='ACTIVE'","r.schema=99"):
   v=fixture();v.execute("v=M.Loss(nil,r,{commerce=true},3);"+mutation+";assert(not pcall(M.Validate,v,r))")
 def test_nonfinite_fractional_reversed_and_false_selection_inputs_fail(self):
  v=fixture();v.execute("for _,n in ipairs({-1,.5,math.huge,-math.huge,0/0})do assert(not pcall(M.Loss,nil,r,{commerce=true},n))end;assert(not pcall(M.Loss,nil,r,{commerce=1},0));assert(not pcall(M.Loss,nil,r,{unknown=true},0));v=M.Loss(nil,r,{commerce=true},3);assert(not pcall(M.Loss,v,r,{},2));assert(not pcall(returned,2))")
 def test_same_epoch_cannot_be_reused_for_a_new_loss_after_return(self):
  v=fixture();v.execute("v=M.Loss(nil,r,{commerce=true},3);v=returned(4);r.stage='HELD_TRANSFER';r.loss=r.lastLoss;assert(not pcall(M.Loss,v,r,{},5))")
 def test_model_only_cold_detached_roundtrip_does_not_need_native_objects(self):
  v=fixture();v.execute('v=M.Loss(nil,r,{commerce=true},3);v=returned(8)');saved=json.loads(json.dumps({'value':plain(v.eval('v')),'parent':plain(v.eval('r'))}))
  other=fixture();other.execute('v=...;r=select(2,...)',other.lua.table_from(saved['value'],recursive=True),other.lua.table_from(saved['parent'],recursive=True));other.execute("assert(M.Validate(v,r));local e=M.Entry(v,'commerce',r);assert(e.returnTurn==8 and M.Clear(v,'commerce',e,r)==nil)")
 def test_metatable_cycles_and_native_surfaces_are_not_read(self):
  v=fixture();v.execute("Game=setmetatable({},{__index=function()error('NATIVE_ACCESS')end});Players=Game;Events=Game;GameEvents=Game;v=M.Loss(nil,r,{commerce=true},3);v=returned(4);assert(M.Validate(v,r));local cyclic={};cyclic.self=cyclic;v.entries.commerce.lossTarget=cyclic;assert(not pcall(M.Validate,v,r));assert(not pcall(M.Loss,nil,r,setmetatable({},{__index=function()error('NO_META')end}),3))")
 def test_publication_package_is_import_only_with_no_production_inclusion(self):
  import xml.etree.ElementTree as ET
  tree=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');name='StoreDeferredLifecycle.lua';self.assertEqual([x.text for x in tree.findall('./Files/File')].count(name),1);self.assertIn(name,[x.text for x in tree.findall('./InGameActions/ImportFiles/File')])
  for source in ('CityProgressionStore.lua','Gameplay.lua'):self.assertNotIn("include('StoreDeferredLifecycle')",(ROOT/'Mod'/source).read_text())

if __name__=='__main__':unittest.main()
