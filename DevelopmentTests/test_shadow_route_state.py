"""Pure shadow cache contract; no game or engine mocks required."""
from pathlib import Path
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute((root/'ShadowRouteState.lua').read_text())
lua.execute('''
local function snapshot(spec)
 local s={status="COMPLETE_UI_SHADOW",sourceContext="UI",authority="UI_SHADOW_ONLY",player=0,turn=1,keys={},routes={},count=#spec}
 for _,x in ipairs(spec) do
  local k="0:"..x[1].."|0:"..x[2]..">"..(x[4] or 0)..":"..x[3]
  s.keys[#s.keys+1]=k
  s.routes[k]={traderUnitID=x[1],originPlayer=0,originCityID=x[2],destinationPlayer=x[4] or 0,destinationCityID=x[3],display="not normalized"}
 end
 return s
end
local c=SPCShadowRouteState.New()
assert(c:Read().status=="UNKNOWN")
assert(c:Replace(snapshot({})));assert(c:Read().count==0 and c:Read().revision==1)
local input=snapshot({{10,1,2},{11,1,3},{12,2,3}})
assert(c:Replace(input));local first=c:Read();assert(first.count==3 and first.revision==2)
for _,r in pairs(first.routes) do assert(r.display==nil and r.originUID==nil and r.current==true) end
input.routes={};first.routes[first.orderedKeys[1]].originCityID=999
assert(c:Read().routes[c:Read().orderedKeys[1]].originCityID==1)
assert(c:Replace(snapshot({{12,2,3},{10,1,2},{11,1,3}})))
assert(c:Read().revision==2 and c:Read().addedCount==0)
c:Invalidate("DIRTY");assert(c:Read().status=="UNKNOWN" and c:Read().routes==nil)
assert(c:Replace(snapshot({{10,1,2}})))
assert(c:Read().count==1 and c:Read().removedCount==2 and c:Read().revision==3)
-- Same route count, changed destination must revise and remove old identity.
assert(c:Replace(snapshot({{10,1,4,1}})))
local intl=c:Read();assert(intl.revision==4 and intl.addedCount==1 and intl.removedCount==1)
assert(not intl.routes[intl.orderedKeys[1]].domestic)
for _,kind in ipairs({"wrongauthority","missing","extra","duplicateTrader"}) do
 local bad=snapshot({{10,1,2}})
 if kind=="wrongauthority" then bad.authority="GAMEPLAY_CURRENT"
 elseif kind=="missing" then bad.routes={}
 elseif kind=="extra" then bad.routes.extra={}
 else bad=snapshot({{10,1,2},{10,1,3}}) end
 assert(not c:Replace(bad));assert(c:Read().status=="UNKNOWN" and c:Read().routes==nil)
end
assert(c:Replace(snapshot({{10,1,4,1}})));assert(c:Read().revision==4)
c:Reset();assert(c:Read().status=="UNKNOWN")
assert(c:Replace(snapshot({})));assert(c:Read().revision==1 and c:Read().count==0)
''')
print('LOCAL_SIMULATION_PASS: UI-only provenance, full replacement, revision idempotence, 3-to-1 revocation, changed endpoints, copied reads, malformed-source rejection, invalidation/reset. No engine validation.')
