"""Lua 5.1 public configuration, Store report and phase-zero delivery regressions."""
import unittest
from unittest.mock import patch

import test_store_write_boundaries as store_fixture
from refactor_harness import TrackedLua51, legacy_source_observation
from test_b247_restructuring import runtime


def configured_request():
    with legacy_source_observation(), patch.object(store_fixture, 'LuaRuntime', TrackedLua51):
        lua = runtime(True)
        for name in ('FactChanges', 'NetworkBridge', 'FactConsumerBindings'):
            lua.globals().include(name)
    lua.execute(r"""
local old=Players[0].GetCities
Players[0].GetCities=function(...)
 local list=old(...);list.GetCapitalCity=function()return source end;return list
end
Players[0].GetTrade=function()return {CountOutgoingRoutes=function()return 0 end}end
P.Count=P.Count or function()end
fc=SPCFactChanges.New(shared)
SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true
bindings=SPCFactConsumerBindings.New(shared)
function drain()fc.Flush();bindings.Flush()end
local function proof(seq)
 net.Receive(0,{Epoch=net.epoch,Seq=seq,Turn=T.now(),Signal=shared.RouteSignalRevision,Valid=1,Count=0,Data=''})
 drain()
 assert(net.TransactionCurrent(0),net.Input(0).transportFailure)
end
function eventReference(city)
 local a=Z.st().HistoricalReference(city)
 return table.concat({a.owner,a.cityID,a.x,a.y,a.token},':')
end
function emit(city)
 assert(fc.Emit({owner=0,cityID=city:GetID(),reference=eventReference(city),kinds={'ACTIVE'},cause='TEST_SCOPED_REFRESH'}))
end
proof(1)
assert(Z.run().ok and c.markers.BUILDING_SPC_REALLOCATING and Z.kills==0)
drain();T.turn(5);proof(2);u.x=second:GetX()
marker='BUILDING_SPC_REALLOCATING'
steps={};removals=0
local function note(x)steps[#steps+1]=x end
local finish=Z.st().FinishRestructuring
Z.st().FinishRestructuring=function(...)
 local result=finish(...);note('IDENTITY_COMMIT');return result
end
local units=Players[0].GetUnits
Players[0].GetUnits=function(...)
 local list=units(...);local destroy=list.Destroy
 list.Destroy=function(self,unit)note('DESTROY');return destroy(self,unit)end
 return list
end
local remove,has=P.RemoveBuilding,P.HasBuilding
local awaiting=false
P.RemoveBuilding=function(b,id)
 if b~=c.markers or id~=marker then return remove(b,id)end
 removals=removals+1;note('DISRUPTION_REMOVE');awaiting=true
 if not removalLost then return remove(b,id)end
end
P.HasBuilding=function(b,id)
 local result=has(b,id)
 if awaiting and b==c.markers and id==marker then
  awaiting=false;note('READBACK_PRESENT_'..tostring(result))
 end
 return result
end
local sample=net.RefreshFacts
net.RefreshFacts=function(...)note('BRIDGE_SAMPLE');return sample(...)end
function configure()
 local reply=Z.run()
 local role=T.control(c)
 assert(Z.state().phase=='SETTLED' and role.specialization=='CULTURE' and role.active==3 and role.potential==3)
 assert(Z.kills==1 and Z.units[400]==nil and not net.TransactionCurrent(0))
 assert(reply.ok==(not removalLost))
 assert((c.markers[marker]==true)==(removalLost==true))
 emit(source);drain()
 local network=net.players[0].input.cities[c:GetID()]
 assert(network.specialization=='CULTURE' and network.active==3 and net.TransactionCurrent(0))
 local report=Z.st().Describe(0,c)
 assert(report:find('新专业身份已提交',1,true) and not report:find('资产配置完成',1,true))
 return reply,report
end
""")
    return lua


class Completion(unittest.TestCase):
    def test_identity_commit_precedes_readback_and_network_publication(self):
        configured_request().execute("""
local reply,report=configure()
assert(not fc.errors.RestructuringSync and not report:find('混乱减益撤除未确认',1,true))
assert(table.concat(steps,',')=='DESTROY,IDENTITY_COMMIT,DISRUPTION_REMOVE,READBACK_PRESENT_false,BRIDGE_SAMPLE')
assert(removals==1)
""")

    def test_failed_readback_reaches_dispatch_and_later_verified_scope_clears_report(self):
        configured_request().execute("""
removalLost=true
local reply,report=configure()
local reason='REST_MARKER_WRITE_UNCONFIRMED'
assert(reply.reason==reason and fc.errors.RestructuringSync==reason)
assert(report:find('混乱减益撤除未确认',1,true))
assert(not Z.st().Describe(0,source):find('混乱减益撤除未确认',1,true))
local before=removals;local writes=T.writes()
for i=1,10 do drain()end
assert(removals==before and T.writes()==writes and Z.kills==1)
local skipped=svc.Refresh(0,c:GetID(),eventReference(c)..':older')
assert(skipped=='IRRELEVANT' and removals==before)
emit(source);drain()
assert(removals==before and Z.st().Describe(0,c):find('混乱减益撤除未确认',1,true))
removalLost=false;emit(c);drain()
assert(removals==before+1 and Z.kills==1 and not c.markers[marker])
assert(not fc.errors.RestructuringSync and not Z.st().Describe(0,c):find('混乱减益撤除未确认',1,true))
assert(T.writes()==writes)
""")

    def test_old_cleanup_error_does_not_belong_to_a_new_configuration(self):
        configured_request().execute("""
removalLost=true;configure()
local team={owner=0,id=401,uid='TEAM:401'}
local st=Z.st()
local first=T.record(c).base.first
st.BeginRestructuring(0,c,team,'SECOND_LIQUIDATION')
T.turn(5)
st.ConfigureRestructuring(0,c,team,'RESEARCH',first)
st.ConfirmRestructuringConsumption(0,c,team)
st.FinishRestructuring(0,c,team)
local report=st.Describe(0,c)
assert(report:find('新专业身份已提交',1,true) and report:find('科研',1,true))
assert(not report:find('混乱减益撤除未确认',1,true))
""")


if __name__ == '__main__':
    unittest.main()
