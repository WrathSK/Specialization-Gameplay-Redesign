"""S9e1 real removed-trader filter and Crew fractional receipt readback; Lua51 only."""
import ast
import struct
import unittest
from refactor_harness import Context,ROOT,measure
from test_refactor_s4b import culture
from test_refactor_s7d5 import fixture as crew


def install_probe(vm):
 c=Context();source=c.fragment('Mod/Probe.lua','function P.RouteUnitRelevant(', '-- B213:')
 vm.execute('local P=P\n'+source)


def network():
 vm=culture();install_probe(vm)
 vm.execute("unitReads=0;local get=Players[0].GetUnits;Players[0].GetUnits=function()local u=get();local find=u.FindID;u.FindID=function(...)unitReads=unitReads+1;return find(...)end;return u end")
 return vm


def ui(cold=False):
 c=Context('UI');c.load('Probe');c.load('ShadowRouteState')
 tree=ast.parse((ROOT/'DevelopmentTests/test_background_routes.py').read_text())
 setup=next(n.value.args[0].value for n in tree.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='execute'and n.value.args and isinstance(n.value.args[0],ast.Constant)and isinstance(n.value.args[0].value,str)and 'function gameSample' in n.value.args[0].value)
 c.execute(setup)
 c.execute("SPCNetworkSender={New=function()return function()end,function()end end};SPCP0.IsTestPlayer=function(pid)return pid==0 end")
 c.load('UI/BackgroundRoutes')
 if cold:c.execute('count=1')  # First complete collection genuinely unavailable.
 c.execute('ContextPtr:init()');return c


class RemovedTraders(unittest.TestCase):
 def test_real_Probe_complete_empty_and_missing_snapshot(self):
  c=Context();c.execute("P={};reads=0;units={};Players={[0]={GetUnits=function()reads=reads+1;return {FindID=function(_,id)return units[id]end}end}};P.Info=function(_,id)return id end")
  install_probe(c);c.execute("""
  assert(not P.RouteUnitRelevant(0,999,{})and reads==0)
  assert(P.RouteUnitRelevant(0,10,{[10]={}})and reads==0)
  assert(not P.RouteUnitRelevant(0,20,{[10]={}})and reads==0)
  assert(P.RouteUnitRelevant(0,999)and reads==1)
  units[1]={GetType=function()return {MakeTradeRoute=false}end};assert(not P.RouteUnitRelevant(0,1))
  units[2]={GetType=function()return {MakeTradeRoute=1}end};assert(P.RouteUnitRelevant(0,2))
  assert(P.RouteUnitRelevant(nil,1,{})and P.RouteUnitRelevant(0,nil,{}))
  """)
 def test_thousand_removed_nonsnapshot_units_no_native_read_or_network_work(self):
  vm=network();vm.execute("""
  local seq=shared.RouteSignalRevision;local revision=net.players[0].revision;local visits=counts.city_scan
  for i=1,1000 do fire('UnitRemovedFromMap',0,9000+i)end
  assert(shared.RouteSignalRevision==seq and net.players[0].revision==revision and counts.city_scan==visits and unitReads==0)
  assert(net.TransactionCurrent(0))
  """)
  measure('S9e1_nontrader_removal',{'events':1000,'unit_lookups':0,'city_scans':0,'route_signals':0,'transaction_stayed_current':True,'native_CPU_claim':False})
 def test_removed_accepted_trader_still_prunes_and_invalidates_transaction(self):
  vm=network();vm.execute("""
  local seq=shared.RouteSignalRevision;units[10]=nil;fire('UnitRemovedFromMap',0,10)
  assert(shared.RouteSignalRevision==seq+1 and not net.TransactionCurrent(0)and unitReads>0)
  for _,r in ipairs(net.players[0].routes or {})do assert(r.trader~=10)end
  """)
 def test_foreign_removal_is_ignored_before_Probe_read(self):
  vm=network();vm.execute("local seq=shared.RouteSignalRevision;fire('UnitRemovedFromMap',9,10);assert(shared.RouteSignalRevision==seq and unitReads==0 and net.TransactionCurrent(0))")
 def test_new_trader_operation_uses_live_fallback_not_old_snapshot(self):
  vm=network();vm.execute("""
  local info=P.Info;P.Info=function(tab,key)if tab=='Units'then return {MakeTradeRoute=true}end;return info(tab,key)end
  units[999]={GetType=function()return 999 end};local seq=shared.RouteSignalRevision
  fire('UnitOperationStarted',0,999);assert(shared.RouteSignalRevision==seq+1 and unitReads==1)
  """)
 def test_no_snapshot_removal_keeps_conservative_recovery(self):
  vm=network();vm.execute("net.players[0].routeReferences=nil;local seq=shared.RouteSignalRevision;fire('UnitRemovedFromMap',0,999);assert(shared.RouteSignalRevision==seq+1 and unitReads>0 and not net.TransactionCurrent(0))")
 def test_real_UI_accepted_empty_set_skips_removed_builder(self):
  c=ui();c.execute("local n=reads;local g=s().generation;Events.UnitRemovedFromMap.Fire(0,999);Events.GameCoreEventPublishComplete.Fire();assert(reads==n and s().generation==g and s().snapshot.count==0)")
 def test_real_UI_trader_removal_marks_then_resamples_complete_routes(self):
  c=ui();c.execute("""
  outgoing[1]={route(10,1,2)};count=1;Events.TradeRouteActivityChanged.Fire();Events.GameCoreEventPublishComplete.Fire()
  assert(s().snapshot.traders[10]);local n=reads
  outgoing[1]={};count=0;Events.UnitRemovedFromMap.Fire(0,10);Events.GameCoreEventPublishComplete.Fire()
  assert(reads>n and s().snapshot.count==0)
  """)
 def test_real_UI_no_snapshot_is_not_mislabelled_empty(self):
  c=ui(cold=True);c.execute("assert(not s().snapshot);local n=reads;count=0;Events.UnitRemovedFromMap.Fire(0,999);Events.GameCoreEventPublishComplete.Fire();assert(reads>n and s().snapshot.count==0)")


class CrewReadback(unittest.TestCase):
 def test_fractional_native_remainder_quantizes_storage_but_not_actual_progress(self):
  cases=(0.1,0.49,0.51,1.1,7.333333333333,259.99999)
  for remaining in cases:
   with self.subTest(remaining=remaining):
    vm=crew();vm.globals().binary32=lambda n:struct.unpack('<f',struct.pack('<f',n))[0]
    vm.globals().remaining=remaining
    vm.execute("""
    local q=c:GetBuildQueue();q.cost=1000;q.progress=1000-remaining;local expected=q.cost-q.progress
    local set=Players[0].SetProperty;local stages={}
    Players[0].SetProperty=function(o,k,v)
     if k==SPCCrewModel.USE_RECEIPT_PROPERTY then
      v=SPCCrewModel.Copy(v);for _,row in pairs(v)do row.amount=binary32(row.amount);stages[#stages+1]=row.state end
     end
     return set(o,k,v)
    end
    assert(prepare():find('PREPARED'));local text,r,o=confirm()
    assert(o.status=='COMMITTED'and r==nil and #q.adds==1 and q.adds[1]==expected and not C.units[20001],text)
    local _,row=next(C.props[SPCCrewModel.USE_RECEIPT_PROPERTY]);assert(row.amount==math.floor(expected+0.5)and row.state=='GRANT_RETURNED')
    assert(#stages==3 and stages[1]=='INTENT'and stages[2]=='GRANT_ATTEMPTED'and stages[3]=='GRANT_RETURNED')
    for i=1,5 do confirm()end;assert(#q.adds==1)
    """)
  measure('S9e1_Crew_binary32_receipts',{'fractional_cases':len(cases),'receipt_integer':True,'actual_base_input_unchanged':True,'native_grant_calls_per_use':1})
 def test_corrupted_receipt_still_holds_before_debit_and_never_grants(self):
  vm=crew();vm.execute("""
  local set=Players[0].SetProperty
  Players[0].SetProperty=function(o,k,v)if k==SPCCrewModel.USE_RECEIPT_PROPERTY then v=SPCCrewModel.Copy(v);for _,row in pairs(v)do row.amount=row.amount+1 end end;return set(o,k,v)end
  prepare();local text,r,o=confirm();assert(o.status=='HELD'and o.phase=='INTENT'and C.units[20001]and #c:GetBuildQueue().adds==0)
  for i=1,5 do confirm()end;assert(#c:GetBuildQueue().adds==0)
  """)

if __name__=='__main__':unittest.main()
