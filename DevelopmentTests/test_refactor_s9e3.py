"""R09a actual route/Standardization lifecycle locality and central legacy exits."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import subprocess
import unittest
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,measure,legacy_source_observation
from test_refactor_s4b import standard
from test_refactor_s9e1 import ui
from test_refactor_s8c5c import production


@contextmanager
def baseline():
 paths=('NetworkBridge','StandardizationEffects','NetworkBoost','GreatWorkProbe','UI/BackgroundRoutes')
 old={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','55c0063:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in paths}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(text.encode()).hexdigest():'historical/55c0063/'+str(path.relative_to(ROOT))for path,text in old.items()}
 def run(vm,text,*a,**kw):
  h=sha256(text.encode()if isinstance(text,str)else text).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,text,*a,**kw)
 with patch.object(Path,'read_text',lambda p,*a,**kw:old[p]if p in old else read(p,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield


def observed():
 v=standard();v.execute("""
 visits=0;legacy=0;carrierReads=0;scopes={}
 local a=std.Audit;std.Audit=function(scope)visits=visits+1;scopes[#scopes+1]=scope or {};return a(scope)end
 shared.StandardizationDiscount.Withdraw=function()legacy=legacy+1;return true end
 shared.CopyYields.Withdraw=function()legacy=legacy+1;return true end
 local has=P.HasBuilding;P.HasBuilding=function(b,id)if tostring(id):find('BUILDING_SPC_STD_',1,true)then carrierReads=carrierReads+1 end;return has(b,id)end
 """);return v


class Transfer(unittest.TestCase):
 def test_foreign_to_foreign_no_Std_rebuild_or_route_census(self):
  values=[]
  for old in (True,False):
   with baseline()if old else nullcontext():v=observed()
   v.execute("local s,n=shared.RouteSignalRevision,counts.city_scan or 0;for i=1,10 do fire('CityTransfered',9,900+i,10)end;work={audits=visits,legacy=legacy,carriers=carrierReads,signals=shared.RouteSignalRevision-s,census=(counts.city_scan or 0)-n};assert(stdValue(1)==14)")
   values.append(dict(v.globals().work))
  self.assertGreater(values[0]['legacy'],0);self.assertGreater(values[0]['census'],0)
  self.assertEqual(values[1],dict(audits=0,legacy=0,carriers=0,signals=0,census=0))
  measure('S9e3_foreign_transfers',{'baseline':'B374','events':10,'before':values[0],'after':values[1],'scope':'actual Bridge+Std only;remaining Research/Culture and coordinate-unknown adjacency paths explicitly not closed'})
 def test_foreign_removed_unrelated_id_no_route_read(self):
  v=observed();v.execute("local signal=shared.RouteSignalRevision;local n=counts.city_scan;fire('CityRemovedFromMap',9,900);assert(shared.RouteSignalRevision==signal and counts.city_scan==n and visits==0)")
 def test_pending_stale_busy_or_missing_snapshot_is_conservative(self):
  for change in ("net.players[0].revalidation='NEEDS_REVALIDATION'","shared.RouteSignalRevision=shared.RouteSignalRevision+1","net.players[0].queuedWork=true","net.players[0].refreshing=true","net.players[0].receiving=true","net.players[0].routeReferences=nil","net.players[0].routes=nil"):
   with self.subTest(change=change):
    v=observed();v.execute(change+";assert(net.RouteLifecycleRelevant(9,900,10))")
 def test_accepted_empty_snapshot_is_not_missing(self):
  v=observed();v.execute("send('',0);assert(not net.RouteLifecycleRelevant(9,900,10)and not net.RouteLifecycleRelevant(9,900));assert(net.RouteLifecycleRelevant(0,1,9)and net.RouteLifecycleRelevant(nil,1,9)and net.RouteLifecycleRelevant(9,nil,10))")
 def test_foreign_route_endpoint_transfer_still_triggers_negative_proof(self):
  v=observed();v.execute("""
  local foreign={owner=9,id=90};function foreign:GetOwner()return self.owner end;function foreign:GetID()return self.id end
  function foreign:GetX()return 90 end;function foreign:GetY()return 10 end;function foreign:GetProperty()return 'FOREIGN'end
  Players[9]={GetCities=function()return {FindID=function(_,id)if id==90 and foreign.owner==9 then return foreign end end}end}
  send('0,5,0,2,10;0,3,0,2,11;0,2,9,90,12',3)
  assert(net.RouteLifecycleRelevant(10,100,9)and not net.RouteLifecycleRelevant(9,91))
  local signal=shared.RouteSignalRevision;foreign.owner=10;fire('CityTransfered',10,100,9)
  assert(shared.RouteSignalRevision==signal+1 and not net.TransactionCurrent(0))
  for _,r in ipairs(net.players[0].routes or {})do assert(r.dp~=9)end
  """)
 def test_local_incoming_retains_initialization_markers(self):
  v=observed();v.execute("fire('CityTransfered',0,1,9);assert(visits==2 and legacy==0 and stdValue(1)==14);assert(scopes[1].changed==nil and scopes[2].changed[1])")
 def test_malformed_transfer_keeps_conservative_work(self):
  v=observed();v.execute("fire('CityTransfered',9,900);assert(visits>0 and stdValue(1)==14)")
 def test_confirmed_exit_uses_original_city_scope_and_withdraws_dependents(self):
  v=observed();v.execute("""
  local c=cities[5];cities[5]=nil;c.owner=9;c.id=95
  exits.StandardizationEffects(c,{confirmed=true,origin={owner=0,cityID=5}})
  assert(std.records['0:5']==nil);fire('GameCoreEventPublishComplete')
  assert(stdValue(1)==12 and visits==1 and std.errors['0:95']==nil)
  """)


class UI(unittest.TestCase):
 def test_real_UI_gate_uses_actual_pure_Bridge_body(self):
  c=ui();fragment=c.fragment('Mod/NetworkBridge.lua',' function d.RouteLifecycleRelevant(', ' local function routeUnitRelevant(')
  c.execute("""
  ExposedMembers.SPC_P0.NetworkBridge={players={[0]={input={},routes={},routeReferences={},signal=0,revalidation='VERIFIED'}}}
  local d=ExposedMembers.SPC_P0.NetworkBridge;local shared=ExposedMembers.SPC_P0
  local function integer(v)return type(v)=='number'and v>=0 and v%1==0 and v<2147483648 end
  """+fragment)
  c.execute("local n=reads;local gen=s().generation;Events.CityTransfered.Fire(9,900,10);Events.CityRemovedFromMap.Fire(9,900);Events.GameCoreEventPublishComplete.Fire();assert(reads==n and s().generation==gen);ExposedMembers.SPC_P0.NetworkBridge.players[0].revalidation='NEEDS_REVALIDATION';Events.CityTransfered.Fire(9,900,10);Events.GameCoreEventPublishComplete.Fire();assert(reads>n)")


class CentralLegacy(unittest.TestCase):
 def test_production_central_options_do_not_run_world_Clean_on_transfer(self):
  v=production();v.execute("""
  calls=0;shared.NetworkBoost.ready=true;shared.GreatWorkProbe.ready=true
  shared.NetworkBoost.Clean=function()calls=calls+1 end;shared.GreatWorkProbe.Clean=function()calls=calls+1 end
  Events.CityTransfered.Fire(9,900,10);assert(calls==0)
  lose();assert(status()=='WITHDRAWN'and removeCalls==1409 and plotWrites==2)
  """)
 def test_standalone_legacy_callback_is_preserved_without_central_owner(self):
  c=Context();c.load('NetworkBoost');c.load('GreatWorkProbe');c.execute("""
  P={Field=function(t,k)return t and t[k]end};SPCNetworkBoost.Start(P,shared,{retired=true});SPCGreatWorkProbe.Start(P,shared)
  calls=0;shared.NetworkBoost.ready=true;shared.GreatWorkProbe.ready=true
  shared.NetworkBoost.Clean=function()calls=calls+1 end;shared.GreatWorkProbe.Clean=function()calls=calls+1 end
  Events.CityTransfered.Fire(9,900,10);assert(calls==2)
  """)

if __name__=='__main__':unittest.main()
