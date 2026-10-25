"""Pure lifecycle witness + final NativeHealth barrier; confirmed loss stops later writes."""
import json,unittest
from refactor_harness import ROOT,measure
from test_refactor_s9d1 import runtime

class Witness(unittest.TestCase):
 def test_default_Read_Inspect_arity_values_and_shared_phase_witness_remain_coherent(self):
  v=runtime();v.execute("local ef=shared.EffectiveFacts;assert(select('#',ef.Read(0,c))==1);local f,w=ef.ReadWithCarrierReference(0,c);local stamp=shared.CityProgressionStore.CarrierReferenceStamp;assert(type(w)=='string'and w==stamp(f.owner,f.cityID,f.x,f.y,f.token));assert(select('#',ef.Inspect(0,c,function()return 1,nil,3 end))==3);local a,b,d=ef.Inspect(0,c,function()return 1,nil,3 end);assert(a==1 and b==nil and d==3);local count=0;local old=P.Count;P.Count=function(label)if label=='facts'then count=count+1 end;return old(label)end;ef.WithPhase('CARRIER_TEST',function()local f=ef.Read(0,c);local g,w=ef.ReadWithCarrierReference(0,c);assert(T.encode(f)==T.encode(g)and type(w)=='string'and w==stamp(g.owner,g.cityID,g.x,g.y,g.token))end);assert(count==1)")
 def test_thousand_pure_reference_checks_use_no_native_fact_or_Property_reads(self):
  v=runtime();v.execute("local f,w=shared.EffectiveFacts.ReadWithCarrierReference(0,c);local stamp=shared.CityProgressionStore.CarrierReferenceStamp;local writes=T.writes();local function no()error('PURE_WITNESS_NATIVE_FORBIDDEN')end;for _,name in ipairs({'GetOwner','GetID','GetX','GetY','GetProperty'})do c[name]=no end;Game.GetProperty=no;Game.GetCurrentGameTurn=no;P.IsTestPlayer=no;shared.EffectiveFacts.Read=no;Players[0].GetCities=no;for i=1,1000 do assert(stamp(f.owner,f.cityID,f.x,f.y,f.token)==w)end;assert(stamp(9,f.cityID,f.x,f.y,f.token)==nil and stamp(f.owner,f.cityID,f.x,f.y,'WRONG')==nil and T.writes()==writes)")
  measure('S9d1b_reference_witness',{'queries':1000,'native_reads':0,'fact_or_Property_reads':0,'new_cache':False,'shared_phase_lifetime':True,'saved_schema_changed':False})
 def test_history_revision_does_not_invalidate_but_commit_barrier_returns_unavailable(self):
  v=runtime();v.execute("local f,w=shared.EffectiveFacts.ReadWithCarrierReference(0,c);local store=shared.CityProgressionStore;local stamp=store.CarrierReferenceStamp;local n=M.Copy(T.record(c));n.revision=n.revision+1;local set=Game.SetProperty;local observed=false;Game.SetProperty=function(o,k,value)if k==T.key(c)then observed=true;assert(stamp(f.owner,f.cityID,f.x,f.y,f.token)==nil)end;return set(o,k,value)end;assert(T.write(c,n)and observed and stamp(f.owner,f.cityID,f.x,f.y,f.token)==w)")
 def test_same_reference_loss_return_invalidates_old_Base_witness_before_facts_return(self):
  v=runtime();v.execute("nextTier();local gate=P.GovernorGate;local once=true;P.GovernorGate=function(city)local owner,id,status,ceiling=gate(city);if once and city==c then once=false;local original=c:GetID();T.loss(c,9,900);c.s.ref.owner=0;c.s.ref.cityID=original;Events.CityTransfered.Fire(0,original,9)end;return owner,id,status,ceiling end;effects.Update(0,c);assert(T.record(c).stage=='ACTIVE'and current(c)==0 and not c.fx[910]and effects.lastError.reason:find('TRADITION_WRITE_REFERENCE_CHANGED',1,true));P.GovernorGate=gate;effects.Update(0,c);assert(applied().applied==0)")
 def test_snapshot_captured_before_history_native_reentry_cannot_follow_new_lifetime(self):
  v=runtime();v.execute("nextTier();local read=shared.CityProgressionStore.ReadTradition;local once=true;shared.CityProgressionStore.ReadTradition=function(pid,city)local value=read(pid,city);if once and city==c then once=false;local original=c:GetID();T.loss(c,9,900);c.s.ref.owner=0;c.s.ref.cityID=original;Events.CityTransfered.Fire(0,original,9)end;return value end;effects.Update(0,c);assert(current(c)==0 and not c.fx[910]and effects.lastError.reason:find('TRADITION_WRITE_REFERENCE_CHANGED',1,true))")

class WriteBarrier(unittest.TestCase):
 def test_Remove_loss_then_later_Create_is_stopped_and_sibling_untouched(self):
  v=runtime();v.execute("nextTier();local remove=P.RemoveBuilding;local once=true;local creates=0;local create=P.CreateBuilding;P.CreateBuilding=function(...)creates=creates+1;return create(...)end;P.RemoveBuilding=function(b,id)remove(b,id);if once and b.city==c then once=false;T.loss(c,9,900)end end;effects.Update(0,c);assert(current(c)==0 and not c.fx[910]and creates==0 and current(other)==5 and effects.lastError.reason:find('TRADITION_WRITE_REFERENCE_CHANGED',1,true))")
 def test_final_create_queue_getter_loss_cannot_enter_native_create(self):
  v=runtime();v.execute("nextTier();local get=c.GetBuildQueue;local once=true;local creates=0;local create=P.CreateBuilding;P.CreateBuilding=function(...)creates=creates+1;return create(...)end;c.GetBuildQueue=function(city)local q=get(city);if once then once=false;T.loss(c,9,900)end;return q end;effects.Update(0,c);assert(creates==0 and current(c)==0 and not c.fx[910])")
 def test_optional_location_and_witness_owner_getters_are_before_last_guard(self):
  for mode in ('LOCATION','WITNESS_OWNER'):
   v=runtime();v.execute("mode=...;nextTier();local b=c:GetBuildings();local location=b.GetBuildingLocation;local owner=c.GetOwner;local armed=false;local once=true;b.GetBuildingLocation=function(...)local value=location(...);if once then if mode=='LOCATION'then once=false;T.loss(c,9,900)else armed=true end end;return value end;c.GetOwner=function(...)local value=owner(...);if armed and once then once=false;T.loss(c,9,900)end;return value end;effects.Update(0,c);assert(current(c)==0 and not c.fx[910])",mode)
 def test_final_remove_buildings_getter_is_before_last_guard(self):
  v=runtime();v.execute("nextTier();local b=c:GetBuildings();local location=b.GetBuildingLocation;local get=c.GetBuildings;local once=true;local armed=false;b.GetBuildingLocation=function(...)armed=true;return location(...)end;c.GetBuildings=function(city)local value=get(city);if armed and once then once=false;armed=false;T.loss(c,9,900)end;return value end;effects.Update(0,c);assert(current(c)==0 and not c.fx[910])")
 def test_loss_return_after_remove_same_owner_ID_token_still_rejects_old_scope(self):
  v=runtime();v.execute("nextTier();local remove=P.RemoveBuilding;local once=true;local original=c:GetID();P.RemoveBuilding=function(b,id)remove(b,id);if once and b.city==c then once=false;T.loss(c,9,900);c.s.ref.owner=0;c.s.ref.cityID=original;Events.CityTransfered.Fire(0,original,9)end end;effects.Update(0,c);assert(T.record(c).stage=='ACTIVE'and current(c)==0 and not c.fx[910]);effects.Update(0,c);assert(applied().applied==0)")
 def test_source_method_or_native_function_replacement_at_queue_boundary_blocks_old_call(self):
  for change in ("shared.CityProgressionStore={}","shared.ResearchTraditionEffects={}","local old=shared.CityProgressionStore.CarrierReferenceStamp;shared.CityProgressionStore.CarrierReferenceStamp=function(...)return old(...)end", "local old=P.CreateBuilding;P.CreateBuilding=function(...)return old(...)end", "local old=shared.EffectiveFacts.ReadWithCarrierReference;shared.EffectiveFacts.ReadWithCarrierReference=function(...)return old(...)end"):
   v=runtime();v.execute("nextTier();local get=c.GetBuildQueue;local once=true;c.GetBuildQueue=function(city)local q=get(city);if once then once=false;"+change+" end;return q end;effects.Update(0,c);assert(current(c)==0 and not c.fx[910]and effects.lastError.reason:find('TRADITION_WRITE_SOURCE_CHANGED',1,true))")
 def test_missing_witness_in_current_authority_does_not_fallback_to_plain_Read(self):
  v=runtime();v.execute("nextTier();local read=shared.EffectiveFacts.ReadWithCarrierReference;shared.EffectiveFacts.ReadWithCarrierReference=function(...)local f=read(...);return f,nil end;effects.Update(0,c);assert(current(c)==5 and not c.fx[910]and effects.lastError.reason:find('TRADITION_WRITE_REFERENCE_CHANGED',1,true))")


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9d1'])])
if __name__=='__main__':unittest.main()
