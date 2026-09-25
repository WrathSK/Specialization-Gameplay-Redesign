"""L3 scoped: native conquest plus CityBuilt classification; actual store, no engine claim."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[1]
l=runpy.run_path(str(R/'DevelopmentTests/test_b101_e2_transition.py'))['l']
l.execute(r"""
local KEY=SPCCityProgressionStore.KEY
local function conquer()GameEvents.CityConquered.Fire(0,62,88,4,5)end
local function built()GameEvents.CityBuilt.Fire(0,88,4,5)end
-- CityBuilt timing wasn't in the first screenshot. All positions before final transfer
-- are allowed only when typed conquest precedes removal and endpoints exactly match.
for position=1,5 do
 held();local before=Game:GetProperty(KEY)
 if position==1 then built()end
 conquer();if position==2 then built()end
 removed();if position==3 then built()end
 added();if position==4 then built()end
 initialized();if position==5 then built()end
 transferred();local after=Game:GetProperty(KEY)
 assert(after.stage=='ACTIVE',d.observation)
 assert(after.returnProof.version==2 and after.returnProof.conquest.fromOwner==62)
 assert(encode(before.base)==encode(after.base) and encode(before.investment)==encode(after.investment))
 assert(shared.EffectiveFacts.Read(0,c).potential==3 and s.values.TOKEN==nil)
 local rev=after.revision;transferred();built();assert(Game:GetProperty(KEY).revision==rev)
 boot();districts();assert(shared.EffectiveFacts.Read(0,c).potential==3 and s.values.TOKEN==nil)
end
-- No typed conquest must continue to reject CityBuilt, even with plausible endpoints.
held();removed();added();initialized();built();transferred()
assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER' and d.returnRejection=='RETURN_NEW_FOUNDATION')
for _,case in ipairs({'oldowner','newowner','city','location','cross_turn','late','conflict','builtid','builtowner','builtturn','missingremove','reload'})do
 held()
 if case=='oldowner' then GameEvents.CityConquered.Fire(0,9,88,4,5)
 elseif case=='newowner' then GameEvents.CityConquered.Fire(1,62,88,4,5)
 elseif case=='city' then GameEvents.CityConquered.Fire(0,62,99,4,5)
 elseif case=='location' then GameEvents.CityConquered.Fire(0,62,88,6,5)
 elseif case=='cross_turn' then local t=Game.GetCurrentGameTurn;Game.GetCurrentGameTurn=function()return 7 end;conquer();Game.GetCurrentGameTurn=t
 elseif case~='late' then conquer()end
 if case~='missingremove' then removed()end
 if case=='late' then conquer()end
 added();initialized()
 if case=='conflict' then GameEvents.CityConquered.Fire(0,62,99,4,5)end
 if case=='builtid' then GameEvents.CityBuilt.Fire(0,99,4,5)
 elseif case=='builtowner' then GameEvents.CityBuilt.Fire(1,88,4,5)
 elseif case=='builtturn' then Game.GetCurrentGameTurn=function()return 9 end;built()
 else built()end
 if case=='reload' then boot();districts()end
 transferred();assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER',case)
 assert(not pcall(shared.EffectiveFacts.Read,0,c),case)
end
-- Exact duplicates + unrelated city notifications don't broaden or poison proof.
held();conquer();conquer();GameEvents.CityConquered.Fire(1,3,9,10,10)
removed();added();initialized();built();built();GameEvents.CityBuilt.Fire(1,99,10,10);transferred()
assert(Game:GetProperty(KEY).stage=='ACTIVE',d.observation)
-- Persisted v2 proof is validated on reload; edits don't become opaque trusted flags.
local good=Game:GetProperty(KEY)
for _,field in ipairs({'fromOwner','to','turn','sequence'})do
 local bad=M.Copy(good);bad.returnProof.conquest[field]=nil;Game:SetProperty(KEY,bad);boot()
 assert(not pcall(shared.EffectiveFacts.Read,0,c),field)
end
Game:SetProperty(KEY,good);boot();assert(shared.EffectiveFacts.Read(0,c).potential==3)
-- Read-only report now exposes CityBuilt itself for the next native timing evidence.
held();conquer();removed();added();initialized();built()
local before=encode(Game:GetProperty(KEY));local report=d.NativeDescribe(0)
assert(report:find('CityBuilt(0,88,4,5)',1,true),report)
assert(encode(Game:GetProperty(KEY))==before)
print('B102 LOCAL_SIMULATION_PASS: matched conquest/CityBuilt timings, persistent proof reload, exact duplicates, true-foundation/foreign/conflicting/missing/stale/malformed proof rejection, no token rewrite')
""")
