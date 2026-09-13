"""Pure model tests. The full source is a MOCK, not a discovered engine API."""
from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
lua=LuaRuntime(unpack_returned_tuples=True)
lua.globals().State=lua.execute((p/'TradeRouteState.lua').read_text())
lua.globals().Network=lua.execute((p/'NetworkState.lua').read_text())
lua.execute(r'''
local cities={}
for i=1,8 do cities[i]={status="PRESENT",owner=0,cityID=i,uid="generation1-city"..i} end
local function resolve(p,c) return cities[c] or {status="ABSENT"} end
local war=false;local function atWar() return war end
local rows={};local authority="GAMEPLAY_CURRENT";local context="GAMEPLAY";local complete="COMPLETE"
local function fetch() return {status=complete,context=context,authority=authority,sourceID="MOCK_NOT_ENGINE",rows=rows,count=#rows} end
local function row(t,o,d,dp) return {traderUnitID=t,originPlayer=0,originCityID=o,destinationPlayer=dp or 0,destinationCityID=d,current=true} end
local s=State.New();assert(s:Read().status=="UNKNOWN")
local function refresh(expected)
 local ok,r=s:Refresh(fetch,resolve,atWar);assert(ok,r);assert(r.count==expected);return r
end
refresh(0) -- complete empty differs from unavailable
local A,B,C,D=row(10,1,2),row(11,1,3),row(12,4,2),row(13,1,2)
rows={A};refresh(1)
rows={A,B,C,D};refresh(4) -- same origin / same destination / same pair distinct traders
local rev=s.revision
rows={D,C,B,A,A};refresh(4);assert(s.revision==rev) -- order and exact duplicate invariant
for i=1,5 do s:MarkDirty("repeated event") end
assert(s:Read().status=="UNKNOWN");refresh(4);assert(s.revision==rev)
rows={B,C,D};local r=refresh(3);assert(#r.removed==1 and #r.added==0) -- remove only A
rows={A,B};cities[2].owner=1;refresh(1) -- stale ownership must not retarget endpoint
cities[2].owner=0;cities[1].owner=1;refresh(0) -- origin capture
cities[1].owner=0;cities[1].status="ABSENT";refresh(0) -- origin destroyed
cities[1].status="PRESENT";cities[3]=nil;refresh(1) -- invalid destination
cities[3]={status="UNKNOWN"};local ok=s:Refresh(fetch,resolve,atWar);assert(not ok and s:Read().status=="UNKNOWN")
cities[3]={status="PRESENT",owner=0,cityID=3,uid="generation1-city3"}
rows={A};refresh(1)
local saved=s:Read();saved.routes={phantom=true};saved.count=999
s=State.New();s.lastGood=saved;refresh(1);assert(s:Read().count==1) -- corrupt pre-load cache replaced
s=State.New();refresh(1) -- no cache/event history required
local read=s:Read();read.routes[read.orderedKeys[1]].originUID="MUTATED";assert(s:Read().routes[s:Read().orderedKeys[1]].originUID~="MUTATED")
local oldkey=s:Read().orderedKeys[1]
cities[2].uid="generation2-city2";r=refresh(1);assert(r.orderedKeys[1]~=oldkey and #r.removed==1)
cities[2].uid="generation1-city2"
rows={row(10,1,2,1)};cities[2].owner=1;refresh(1);war=true;refresh(0);war=false
cities[2].owner=0;rows={A};refresh(1)
for _,bad in ipairs({"UI_SNAPSHOT","EVENT_HISTORY","UNIT_OPERATION_CANDIDATE"}) do
 authority=bad;assert(not s:Refresh(fetch,resolve,atWar));assert(s:Read().status=="UNKNOWN")
end
authority="GAMEPLAY_CURRENT";context="UI";assert(not s:Refresh(fetch,resolve,atWar));context="GAMEPLAY"
complete="PARTIAL";assert(not s:Refresh(fetch,resolve,atWar));complete="COMPLETE"
assert(not s:Refresh(function() error("provider failed") end,resolve,atWar));assert(s:Read().status=="UNKNOWN")
rows={A,row(10,1,3)};assert(not s:Refresh(fetch,resolve,atWar)) -- same trader conflicting routes
rows={{current=true,originPlayer=0,originCityID=1,destinationPlayer=0,destinationCityID=2}};assert(not s:Refresh(fetch,resolve,atWar))
rows={A};refresh(1)
local inactive=row(14,1,3);inactive.current=false;rows={A,inactive};refresh(1)
local noStatus=row(15,1,3);noStatus.current=nil;rows={noStatus};assert(not s:Refresh(fetch,resolve,atWar))
local e1=row(10,1,2);e1.engineRouteID=55;local e2=row(11,1,3);e2.engineRouteID=55
rows={e1,e2};assert(not s:Refresh(fetch,resolve,atWar))
-- Topology is independently re-derived from current roles, no numeric merger.
local function uid(i) return cities[i].uid end
rows={row(21,1,2),row(22,4,2),row(23,2,3),row(24,2,3),row(25,2,5),row(26,5,6)}
refresh(6)
local ctx={revision=1,centers={[uid(2)]={owner=0},[uid(5)]={owner=0}},sources={
 [uid(1)]={owner=0,kind="RESEARCH",activeLevel=4,templateRevision=0},
 [uid(4)]={owner=0,kind="RESEARCH",activeLevel=2,templateRevision=1}}}
local function derive() return Network.Derive(s:Read(),ctx) end
local n=derive();assert(n.recipientCounts.RESEARCH==2) -- recipients 3,5; duplicate destination not extra
assert(n.recipients.RESEARCH[uid(3)].sources[uid(1)] and n.recipients.RESEARCH[uid(3)].sources[uid(4)])
assert(not n.recipients.RESEARCH[uid(6)]) -- no recursive center transfer
assert(n.networkStrength==nil and n.strengthStatus=="NOT_CALCULATED")
local routeRev=s.revision
ctx.sources[uid(1)].activeLevel=1;ctx.revision=2;n=derive()
assert(s.revision==routeRev and n.sources[uid(1)].activeLevel==1 and n.contextRevision==2)
ctx.centers[uid(2)]=nil;ctx.revision=3;n=derive();assert(n.recipientCounts.RESEARCH==nil and s.revision==routeRev)
ctx.centers[uid(2)]={owner=0,freeSelfReceiver=true};n=derive();assert(n.recipientCounts.RESEARCH==3)
-- Another center delivers to the free recipient: remove only free eligibility, keep real eligibility.
ctx.localConnections={[uid(5)]={[uid(1)]=true}}
rows[#rows+1]=row(27,5,2);refresh(7);n=derive();assert(n.recipients.RESEARCH[uid(2)])
ctx.centers[uid(2)].freeSelfReceiver=false;n=derive();assert(n.recipients.RESEARCH[uid(2)])
table.remove(rows);refresh(6);n=derive();assert(not n.recipients.RESEARCH[uid(2)])
-- Same routes carry all attached networks; Industry source provenance only.
ctx.sources[uid(4)].kind="INDUSTRY";n=derive();assert(n.recipientCounts.INDUSTRY==2 and n.sources[uid(4)].templateRevision==1)
assert(n.purchaseDiscount==nil and n.production==nil)
s:MarkDirty("unknown");assert(derive().status=="UNKNOWN")
''')
print('LOCAL_SIMULATION_PASS: authoritative contract with MOCK source; replacement/revocation/load corruption/idempotency/identity/ownership/unknown-source rejection; provenance topology, role/ACTIVE changes and no level merger. ENGINE_PROVIDER=BLOCKED')
