"""D0001 NET-RC offline integration: actual Lua topology -> global strength, no Civ VI."""
from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
lua=LuaRuntime(unpack_returned_tuples=True)
lua.globals().Network=lua.execute((p/'NetworkState.lua').read_text())
lua.globals().Strength=lua.execute((p/'NetworkStrength.lua').read_text())
lua.execute('''
local ctx={revision=1,sources={
 R2={owner=0,kind="RESEARCH",activeLevel=2,potential=4},
 R4={owner=0,kind="RESEARCH",activeLevel=4},
 C3={owner=0,kind="CULTURE",activeLevel=3},
 I4={owner=0,kind="INDUSTRY",activeLevel=4,templateRevision=7},
 unattached={owner=0,kind="CULTURE",activeLevel=4}},
 centers={H1={owner=0},H2={owner=0}}}
local rows={{"R2","H1"},{"R4","H2"},{"C3","H1"},{"I4","H1"},
 {"H1","A"},{"H1","A"},{"H2","A"},{"H1","B"},{"H2","C"}}
local function routes()
 local state={status="READY",revision=1,routes={},orderedKeys={}}
 for i,row in ipairs(rows) do
  local k=tostring(i);state.orderedKeys[i]=k
  state.routes[k]={originUID=row[1],destinationUID=row[2],originPlayer=0,domestic=true}
 end
 return state
end
local function run(k)
 local topology=Network.Derive(routes(),ctx)
 local result=Strength.FromState(topology,0,k,"MOCK_ONLY")
 assert(result.status=="READY_OFFLINE_STRENGTH",result.reason)
 return result,topology
end
local function expect(n,kind,L,N,k)
 local v=n.networks[kind];assert(v.L==L and v.N==N)
 assert(math.abs(v.networkStrength-(k or 1)*L*math.sqrt(N))<1e-12)
end
local n,top=run();expect(n,"RESEARCH",4,3);expect(n,"CULTURE",3,2)
assert(n.networks.INDUSTRY==nil and top.sources.I4.templateRevision==7)
assert(n.networks.RESEARCH.sources.R2==2 and n.networks.RESEARCH.maxSources.R4)
assert(not n.networks.CULTURE.sources.unattached) -- high potential/unconnected high level ignored
-- Coefficients independent; no quantization; input order does not change global result.
n=run({RESEARCH=2.25});expect(n,"RESEARCH",4,3,2.25);expect(n,"CULTURE",3,2)
local old=rows[1];rows[1]=rows[9];rows[9]=old
n=run();expect(n,"RESEARCH",4,3)
-- ACTIVE only changes context revision; no route refresh or source-level summation.
ctx.sources.R4.activeLevel=1;ctx.revision=2;n=run();expect(n,"RESEARCH",2,3)
assert(n.routeRevision==1 and n.contextRevision==2)
ctx.sources.R4.activeLevel=2;n=run();assert(n.networks.RESEARCH.maxSources.R2 and n.networks.RESEARCH.maxSources.R4)
-- Highest source at a connected center with no distribution still participates in global L.
ctx.sources.R4.activeLevel=4
for i=#rows,1,-1 do if rows[i][1]=="H2" then table.remove(rows,i) end end
n=run();expect(n,"RESEARCH",4,2)
-- Disconnect the high source, fall back; no stale source or strength.
for i=#rows,1,-1 do if rows[i][1]=="R4" then table.remove(rows,i) end end
n=run();expect(n,"RESEARCH",2,2);assert(n.networks.RESEARCH.sources.R4==nil)
-- Free-self and route eligibility overlap, and retract independently.
ctx.centers.H1.freeSelfReceiver=true;n=run();expect(n,"RESEARCH",2,3)
rows[#rows+1]={"R2","H2"};rows[#rows+1]={"H2","H1"}
n=run();expect(n,"RESEARCH",2,3)
ctx.centers.H1.freeSelfReceiver=false;n=run();expect(n,"RESEARCH",2,3)
table.remove(rows);n=run();expect(n,"RESEARCH",2,2)
-- Center role change removes recipients even if routes unchanged.
ctx.centers.H1=nil;n=run();expect(n,"RESEARCH",2,0);expect(n,"CULTURE",0,0)
-- Complete empty rebuild, disconnected source metadata must not keep L alive.
rows={};n=run();expect(n,"RESEARCH",0,0);expect(n,"CULTURE",0,0)
-- Mutating returned results does not poison subsequent evaluations.
n.networks.RESEARCH.L=99;n.networks.CULTURE.networkStrength=999
n=run();expect(n,"RESEARCH",0,0)
ctx.centers.H1={owner=0};rows={{"R2","H1"},{"H1","A"}}
n,top=run();expect(n,"RESEARCH",2,1)
for i=1,10 do local repeated=run();expect(repeated,"RESEARCH",2,1) end
-- Unready/invalid inputs are UNKNOWN, not zero or stale valid strength.
assert(Strength.FromState({status="UNKNOWN"},0,nil,"MOCK_ONLY").status=="UNKNOWN")
assert(Strength.FromState(top,0,nil,"GAMEPLAY").status=="UNKNOWN")
assert(Strength.FromState(top,1,nil,"MOCK_ONLY").status=="UNKNOWN")
for _,bad in ipairs({-1,0/0,math.huge}) do
 assert(Strength.FromState(top,0,{RESEARCH=bad},"MOCK_ONLY").status=="UNKNOWN")
end
for _,bad in ipairs({0,5,2.5,0/0}) do
 top.sources.R2.activeLevel=bad
 assert(Strength.FromState(top,0,nil,"MOCK_ONLY").status=="UNKNOWN")
end
n,top=run();top.recipients.RESEARCH.A.qualifications={}
assert(Strength.FromState(top,0,nil,"MOCK_ONLY").status=="UNKNOWN")
-- Complete zero-k output is still valid and independent per type.
n=run({RESEARCH=0});expect(n,"RESEARCH",2,1,0)
''')
# Exercise the existing shadow adapter without promoting it to Gameplay authority.
lua.execute('''
local ctx={contextSource="MOCK_ONLY",sources={['0:1']={owner=0,kind="CULTURE",activeLevel=4}},centers={['0:2']={owner=0}}}
local state={status="READY_UI_SHADOW",authority="UI_SHADOW_ONLY",sourceContext="UI",schemaVersion=1,player=0,revision=8,routes={},orderedKeys={}}
for i,r in ipairs({{1,2},{2,3},{2,3}}) do
 local k=tostring(i);state.orderedKeys[i]=k
 state.routes[k]={current=true,originPlayer=0,destinationPlayer=0,originCityID=r[1],destinationCityID=r[2],
 originCityKey='0:'..r[1],destinationCityKey='0:'..r[2],domestic=true,identityKind="OWNER_CITY_ID_SNAPSHOT_ONLY"}
end
local top=Network.DeriveShadow(state,ctx)
local n=Strength.FromState(top,0,nil,"MOCK_ONLY")
assert(n.status=="READY_OFFLINE_STRENGTH" and n.authority=="UI_SHADOW_ONLY")
assert(n.networks.CULTURE.L==4 and n.networks.CULTURE.N==1 and n.networks.CULTURE.networkStrength==4)
assert(Network.Derive(state,ctx).status=="UNKNOWN")
''')
print('LOCAL_SIMULATION_PASS: multi-source max, dedup, separate k, ACTIVE changes, withdrawal/empty rebuild, no Industry merger, UNKNOWN rejection and UI authority isolation.')
