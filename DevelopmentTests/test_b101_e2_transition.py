"""Scoped L3 transition proof, actual store/consumers. Native engine still requires test."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[1]
l=runpy.run_path(str(R/'DevelopmentTests/test_p0_e2_recapture.py'))['l']
l.execute(r"""
local KEY=SPCCityProgressionStore.KEY
function held(kind)
 P.IsTestPlayer=function(pid)return pid==0 end
 reset(3,kind);import();districts();lose();s.values.TOKEN=nil
 boot();districts() -- foreign-held save/load; no City token
end
function removed()Events.CityRemovedFromMap.Fire(62,40)end
function added()s.ref.owner=0;s.ref.cityID=88;Events.CityAddedToMap.Fire(0,88,4,5)end
function initialized()Events.CityInitialized.Fire(0,88,4,5)end
function transferred()Events.CityTransfered.Fire(0,88,62,0)end
function chain()removed();added();initialized();transferred()end
held();local before=Game:GetProperty(KEY)
local oldFacts=P.CityRoleFacts;P.CityRoleFacts=function(city)return {owner=0,cityID=city:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=1}end
chain();local after=Game:GetProperty(KEY)
assert(after.stage=='ACTIVE',d.observation)
assert(after.returnEvidence=='NATIVE_TRANSITION_V1' and after.returnProof.from.owner==62 and after.returnProof.to.cityID==88)
assert(encode(before.base)==encode(after.base) and encode(before.investment)==encode(after.investment) and encode(before.binding)==encode(after.binding))
assert(s.values.TOKEN==nil and shared.EffectiveFacts.Read(0,c).active==1)
local rev=after.revision;transferred();transferred();assert(Game:GetProperty(KEY).revision==rev)
boot();districts();assert(shared.EffectiveFacts.Read(0,c).active==1 and s.values.TOKEN==nil)
-- New investment still uses original receipt authority, not a rewritten City token.
local receipt=prepare(51);assert(a.Confirm(0,c,receipt):find('INVESTED'))
assert(shared.EffectiveFacts.Read(0,c).potential==4 and s.values.TOKEN==nil)
-- Repeated ownership cycle and coldload after accepted return.
lose();s.values.TOKEN=nil;chain();boot();districts();assert(shared.EffectiveFacts.Read(0,c).potential==4)
-- Later removal invalidates accepted reference durably, even if an ID were reused.
Events.CityRemovedFromMap.Fire(0,88)
local removedRevision=Game:GetProperty(KEY).revision;Events.CityRemovedFromMap.Fire(0,88);assert(Game:GetProperty(KEY).revision==removedRevision)
assert(not pcall(shared.EffectiveFacts.Read,0,c));boot();assert(not pcall(shared.EffectiveFacts.Read,0,c))
P.CityRoleFacts=oldFacts
-- All four identities use retained state; never write native City properties.
for _,kind in ipairs({'RESEARCH','CULTURE','COMMERCE','INDUSTRY'})do
 held(kind);c.SetProperty=function()error('NO_CITY_PROPERTY_REWRITE')end
 local values=encode(s.values);chain();assert(Game:GetProperty(KEY).stage=='ACTIVE',d.observation)
 assert(shared.EffectiveFacts.Read(0,c).specialization==kind and encode(s.values)==values)
end
-- Old templates must not be synthesized where retained Industry history is missing.
assert(not pcall(d.ReadTemplates,c))
-- Unknown live object during typed event cannot apply; no retry by generic notification.
held();removed();added();initialized();local getCity=CityManager.GetCityAt
CityManager.GetCityAt=function()return nil end;transferred();CityManager.GetCityAt=getCity
assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER')
Events.CityInitialized.Fire(0,88,4,5);assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER')
-- Missing evidence, ordering, reload mid-chain, different reference, foreign token.
for _,case in ipairs({'missing','order','load','wrongid','wrongowner','wrongplace','foundation','newremoved','turn','token','duplicateconflict'})do
 held()
 if case=='missing' then added();initialized()
 elseif case=='order' then removed();s.ref.owner=0;s.ref.cityID=88;initialized();added()
 elseif case=='load' then removed();added();boot();districts();initialized()
 else
  removed();added();initialized()
  if case=='wrongid' then s.ref.cityID=89
  elseif case=='wrongowner' then s.ref.owner=1
  elseif case=='wrongplace' then s.ref.x=7
  elseif case=='foundation' then GameEvents.CityBuilt.Fire(0,88,4,5)
  elseif case=='newremoved' then Events.CityRemovedFromMap.Fire(0,88)
  elseif case=='turn' then Game.GetCurrentGameTurn=function()return 9 end
  elseif case=='token' then s.values.TOKEN='OTHER_CITY'
  elseif case=='duplicateconflict' then Events.CityAddedToMap.Fire(0,99,4,5)end
 end
 transferred();assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER',case)
 assert(not pcall(shared.EffectiveFacts.Read,0,c),case)
end
-- Unrelated events and identical duplicates cannot invalidate a complete legitimate chain.
held();removed();removed();Events.CityAddedToMap.Fire(0,999,10,10);added();added();initialized();initialized();transferred()
assert(Game:GetProperty(KEY).stage=='ACTIVE',d.observation)
-- Unreadable proof after save is refused rather than trusted as an opaque flag.
local corrupt=Game:GetProperty(KEY);corrupt.returnProof.added=corrupt.returnProof.removed
Game:SetProperty(KEY,corrupt);boot();assert(not pcall(shared.EffectiveFacts.Read,0,c))
-- No foreign witness after load: missing current object never authorizes a chain.
held();local get=CityManager.GetCityAt;CityManager.GetCityAt=function()return nil end;boot();districts()
CityManager.GetCityAt=get;chain();assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER')
-- Withdrawal incomplete remains a separate gate after valid identity proof.
held();d.RegisterExit('Failure',function()error('EXIT_FAIL')end);d.ExitConfirmed();chain()
assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER' and d.returnRejection=='RETURN_WITHDRAWAL_UNCONFIRMED')
-- Actual Network bridge: no old route/sample restoration for missing-token return.
held();include('NetworkBridge');ExposedMembers={};SPCNetworkBridge.Start(P,shared);local net=shared.NetworkBridge;net.ready=true
Players[0].GetTrade=function()return {CountOutgoingRoutes=function()return 0 end}end
net.Input(0);d.ExitConfirmed();chain();assert(Game:GetProperty(KEY).stage=='ACTIVE',d.observation)
assert(net.players[0].routes==nil)
local packet={Epoch=net.epoch,Seq=1,Turn=8,Signal=0,Valid=1,Count=0,Data=''}
net.Receive(0,packet);assert(net.Input(0).validity=='VERIFIED')
assert(net.players[0].input.cities[88] and not net.players[0].input.cities[7] and #net.players[0].routes==0)
assert(s.values.TOKEN==nil)
print('B101 LOCAL_SIMULATION_PASS: tokenless strict native chain, receipts/current governor, accepted coldload, duplicate/repeated cycles, malformed/incomplete/ambiguous/foundation rejection, persistent removal guard, current Network rebuild')
""")
