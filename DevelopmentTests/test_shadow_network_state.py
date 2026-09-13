"""Offline B009 route-schema to provenance integration. Roles are explicit fixtures."""
from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
root=p.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute((root/'ShadowRouteState.lua').read_text())
lua.globals().Network=lua.execute((p/'NetworkState.lua').read_text())
lua.execute('''
local cache=SPCShadowRouteState.New()
local function snapshot(pairs)
 local s={status="COMPLETE_UI_SHADOW",sourceContext="UI",authority="UI_SHADOW_ONLY",player=0,turn=1,keys={},routes={},count=#pairs}
 for i,r in ipairs(pairs) do
  local dp=r[3] or 0;local key="0:"..i.."|0:"..r[1]..">"..dp..":"..r[2]
  s.keys[#s.keys+1]=key;s.routes[key]={traderUnitID=i,originPlayer=0,originCityID=r[1],destinationPlayer=dp,destinationCityID=r[2]}
 end
 assert(cache:Replace(s));return cache:Read()
end
local context={contextSource="MOCK_ONLY",revision=1,
 sources={['0:1']={owner=0,kind="RESEARCH",activeLevel=4},['0:2']={owner=0,kind="CULTURE",activeLevel=3},['0:3']={owner=0,kind="INDUSTRY",activeLevel=2,templateRevision=7}},
 centers={['0:4']={owner=0},['0:5']={owner=0}}}
local routePairs={{1,4},{2,4},{3,4},{4,6},{4,6},{4,7},{4,5},{5,8},{4,9,1}}
local routes=snapshot(routePairs)
assert(Network.Derive(routes,context).status=="UNKNOWN") -- UI still rejected by original entry point
local function derive() return Network.DeriveShadow(routes,context) end
local n=derive();assert(n.status=="READY_SHADOW_PROVENANCE_ONLY" and n.authority=="UI_SHADOW_ONLY")
assert(n.contextSource=="MOCK_ONLY" and n.sources['0:1'].uid==nil)
for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do
 assert(n.recipientCounts[kind]==3) -- cities 5,6,7; duplicate route not extra N
 assert(n.recipients[kind]['0:6'] and not n.recipients[kind]['0:8']) -- no recursive transfer via center 5
 assert(not n.recipients[kind]['1:9']) -- no international recipient
end
assert(n.strengthStatus=="NOT_CALCULATED" and n.strength==nil)
-- ACTIVE/template changes affect source metadata while route facts/revision stay fixed.
local revision=routes.revision
context.sources['0:1'].activeLevel=2;context.sources['0:3'].templateRevision=8;context.revision=2
n=derive();assert(n.sources['0:1'].activeLevel==2 and n.sources['0:3'].templateRevision==8)
assert(n.routeRevision==revision and n.contextRevision==2 and n.recipientCounts.RESEARCH==3)
-- Another Research source of a different level, connecting via the second center.
context.sources['0:10']={owner=0,kind="RESEARCH",activeLevel=4}
routePairs[#routePairs+1]={10,5};routePairs[#routePairs+1]={5,6};routes=snapshot(routePairs)
n=derive();assert(n.recipientCounts.RESEARCH==4) -- 5,6,7,8; city 6 counts once
assert(n.recipients.RESEARCH['0:6'].sources['0:1'] and n.recipients.RESEARCH['0:6'].sources['0:10'])
assert(n.sources['0:1'].activeLevel==2 and n.sources['0:10'].activeLevel==4 and n.strength==nil)
-- Cut first source connection; retain other sources and the second Research source.
routePairs[1]={1,7};routes=snapshot(routePairs);n=derive()
assert(n.recipientCounts.RESEARCH==2 and not n.recipients.RESEARCH['0:6'].sources['0:1'])
assert(n.recipients.RESEARCH['0:6'].sources['0:10'] and n.recipientCounts.CULTURE==3)
-- Remove center role with unchanged routes; rederive and withdraw its recipients.
context.centers['0:5']=nil;context.revision=3;n=derive()
assert(n.recipientCounts.RESEARCH==nil and n.recipientCounts.CULTURE==3)
-- Explicit free-self eligibility is unioned and independently revocable.
context.centers['0:4'].freeSelfReceiver=true;n=derive();assert(n.recipientCounts.CULTURE==4)
context.centers['0:4'].freeSelfReceiver=false;n=derive();assert(n.recipientCounts.CULTURE==3)
-- Losing all route truth never leaves previous topology visible.
cache:Invalidate('DIRTY');assert(Network.DeriveShadow(cache:Read(),context).status=="UNKNOWN")
routes=snapshot({});n=derive();assert(next(n.recipients)==nil)
context.contextSource="GAMEPLAY";assert(derive().status=="UNKNOWN")
context.contextSource="MOCK_ONLY";context.centers['1:4']={owner=1};assert(derive().status=="UNKNOWN")
''')
print('LOCAL_SIMULATION_PASS: shadow route schema + MOCK roles; all-networks distribution, city dedup, no recursive forwarding, multi-source provenance, source/center/ACTIVE/template changes, withdrawal and UNKNOWN; no source-level merger or effects.')
