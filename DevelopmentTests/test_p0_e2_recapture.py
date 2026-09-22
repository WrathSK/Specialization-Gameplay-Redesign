"""Actual E2 storage/facts/investment and Network bridge; local mocks, no native claim."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[1];M=R/'Mod'
l=runpy.run_path(str(R/'DevelopmentTests/test_p0_e2.py'))['l']
l.globals().include=lambda n:l.execute((M/(n+'.lua')).read_text())
l.execute(r"""
P.IsTestPlayer=function(pid)return pid==0 end
function encode(v)if type(v)~='table'then return tostring(v)end;local t={};for k,x in pairs(v)do t[#t+1]=tostring(k)..'='..encode(x)end;table.sort(t);return '{'..table.concat(t,';')..'}'end
local KEY=SPCCityProgressionStore.KEY
function districts()
 if not d.testExit then d.RegisterExit("TestNoCarriers",function()end);d.testExit=true end
 Players[0].GetDistricts=function()return {Members=function()return ipairs({{GetCity=function()return c end,GetType=function()return s.values.JOURNAL.first.type end,GetID=function()return 99 end,IsComplete=function()return true end}})end}end
end
function lose()s.ref.owner=62;s.ref.cityID=40;Events.CityTransfered.Fire(62,40,0,7);assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER')end
function regain()s.ref.owner=0;s.ref.cityID=88;Events.CityTransfered.Fire(0,88,62,0)end
for _,kind in ipairs({'RESEARCH','CULTURE','COMMERCE'})do
 reset(3,kind);import();districts();local before=Game:GetProperty(KEY)
 local old=P.CityRoleFacts;P.CityRoleFacts=function(city)return {owner=0,cityID=city:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=1}end
 lose();assert(not pcall(shared.EffectiveFacts.Read,0,c));regain()
 local after=Game:GetProperty(KEY);assert(after.stage=='ACTIVE',d.observation)
 assert(encode(before.base)==encode(after.base) and encode(before.investment)==encode(after.investment) and encode(before.binding)==encode(after.binding))
 local f=shared.EffectiveFacts.Read(0,c);assert(f.specialization==kind and f.potential==3 and f.active==1 and f.cityID==88 and f.first.districtID==99)
 local rev=after.revision;for i=1,100 do Events.CityTransfered.Fire(0,88,62,0)end;assert(Game:GetProperty(KEY).revision==rev)
 boot();districts();assert(shared.EffectiveFacts.Read(0,c).active==1)
 P.CityRoleFacts=function(city)return {owner=0,cityID=city:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=4}end
 assert(shared.EffectiveFacts.Read(0,c).active==3)
 local token=prepare(15);assert(a.Confirm(0,c,token):find('INVESTED'))
 assert(shared.EffectiveFacts.Read(0,c).potential==4)
 assert(Game:GetProperty(KEY).investment.anchor.cityID==7 and Game:GetProperty(KEY).investment.anchor.first.districtID==3)
 lose();regain();assert(shared.EffectiveFacts.Read(0,c).potential==4)
 P.CityRoleFacts=old
end
local unrelated={GetOwner=function()return 0 end,GetID=function()return 7 end,GetX=function()return 10 end,GetY=function()return 10 end}
assert(not d.Owns(unrelated),'OLD_ID_REUSE_MUST_NOT_CLAIM_OTHER_CITY')
-- Ambiguity, unrelated/first acquisition, no token, no event, pending debit remain held.
reset(2);districts();s.ref.cityID=88;Events.CityTransfered.Fire(0,88,62,0);assert(Game:GetProperty(KEY)==nil)
reset(2);import();districts();lose();local token=s.values.TOKEN
s.ref.owner=0;s.ref.cityID=88;s.values.TOKEN=nil;Events.CityTransfered.Fire(0,88,62,0);assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER')
s.values.TOKEN='another-city';Events.CityTransfered.Fire(0,88,62,0);assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER')
s.values.TOKEN=token;Events.CityTransfered.Fire(0,89,62,0);Events.CityTransfered.Fire(0,88,9,0);Events.CityAddedToMap.Fire(0,88,4,5)
assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER')
regain();assert(Game:GetProperty(KEY).stage=='ACTIVE')
-- Incomplete exit and incomplete debit cannot be bypassed by recapture.
reset(2);import();districts();d.RegisterExit('InjectedFailure',function()error('FAIL')end);lose();regain()
assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER' and d.observation:find('RETURN_WITHDRAWAL_UNCONFIRMED'))
reset(2);import();districts();local ledger=d.Investment(0,c);local pending=M.Copy(ledger)
pending.pending={stage='INTENT',unitID=10,owner=0,cityUID=s.values.TOKEN,expectedRevision=2,receipt='pending',unitUID='unit'}
d.WriteInvestment(0,c,ledger,pending);lose();regain()
assert(Game:GetProperty(KEY).stage=='HELD_TRANSFER' and d.observation:find('RETURN_PENDING_INVESTMENT'))
reset(2);import();districts()
-- Real bridge drops old topology and derives only accepted current route sample.
include('NetworkBridge');ExposedMembers={};SPCNetworkBridge.Start(P,shared);local net=shared.NetworkBridge;net.ready=true
Players[0].GetTrade=function()return {CountOutgoingRoutes=function()return 0 end}end
local packet={Epoch=net.epoch,Seq=1,Turn=8,Signal=0,Valid=1,Count=0,Data=''}
net.Receive(0,packet);assert(net.Input(0).validity=='VERIFIED')
lose();assert(net.Input(0).validity=='CONFIRMED_INVALID')
shared.RouteSignalRevision=1 -- TradeRouteProbe ownership event invalidates UI packet generation.
regain();assert(net.Input(0).validity=='CONFIRMED_INVALID' and net.players[0].routes==nil)
packet.Seq=2;net.Receive(0,packet);assert(net.Input(0).validity~='VERIFIED')
packet.Seq=3;packet.Signal=1;net.Receive(0,packet)
assert(net.Input(0).validity=='VERIFIED' and net.players[0].input.cities[88] and not net.players[0].input.cities[7])
assert(#net.players[0].routes==0 and net.players[62]==nil)
print('Recapture LOCAL_SIMULATION_PASS: immutable history, new city/district references, current governor, coldload, new investment, duplicate/loss cycles, missing token/wrong event/first acquisition hold, current Network-only rebuild')
""")
# Standardization actual storage adapter: exact learned receipts, no AI backfill.
l.execute((M/'Standardization.lua').read_text())
l.execute(r"""
reset(2,'INDUSTRY')
s.values.TEMPLATES={schema=1,initialized=true,uid='STD:'..s.values.TOKEN,foundation=s.values.TOKEN,x=4,y=5,revision=2,
 learned={OLD={district='DISTRICT_CAMPUS',tier=1,turn=3,evidence='COMPLETED'}}}
SPCStandardizationCatalog={Build=function()return {buildings={OLD={district='DISTRICT_CAMPUS',tier=1,index=1},NEW={district='DISTRICT_CAMPUS',tier=2,index=2}}}end}
SPCStandardization.Start(P,shared);shared.Standardization.ready=true
import();districts();lose();s.values.TEMPLATES=nil
c.GetBuildings=function()return {}end;P.HasBuilding=function()return true end
regain();assert(Game:GetProperty(SPCCityProgressionStore.KEY).stage=='ACTIVE',d.observation)
shared.Standardization.Discover(0)
local ledger=shared.Standardization.ReadLedger(0,c)
assert(ledger.learned.OLD and not ledger.learned.NEW and ledger.revision==2)
assert(s.values.TEMPLATES==nil,'NO_CITY_LEDGER_REWRITE')
local previousInfo=P.Info;P.Info=function(t,k)if t=='Buildings'then return {BuildingType=k}end;return previousInfo(t,k)end
shared.Standardization.Queue(0,88,'NEW','BUILDING_ADDED_RECHECK');shared.Standardization.Flush()
assert(not shared.Standardization.ReadLedger(0,c).learned.NEW)
shared.Standardization.pending['0:900']={pid=0,cid=900,buildings={}}
lose();regain();assert(shared.Standardization.pending['0:900'],'UNRELATED_PENDING_DROPPED')
P.Info=previousInfo
local nextValue=M.Copy(ledger);nextValue.learned.NEW={district='DISTRICT_CAMPUS',tier=2,turn=8,evidence='NEW_LOCAL_COMPLETION'};nextValue.revision=3
d.WriteTemplates(c,ledger,nextValue);lose();regain();assert(shared.Standardization.ReadLedger(0,c).revision==3)
reset(2,'INDUSTRY');import();districts();lose();regain()
assert(Game:GetProperty(SPCCityProgressionStore.KEY).stage=='ACTIVE')
assert(shared.EffectiveFacts.Read(0,c).potential==2 and not pcall(d.ReadTemplates,c))
print('Industry LOCAL_SIMULATION_PASS: saved own templates retained with absent old City property; no foreign-period backfill; separate ongoing ledger updates')
""")
assert '"CityTransfered"' in (M/'TradeRouteProbe.lua').read_text()
print('Recapture compile/regression PASS; native token survival/engine event ordering USER_GAME_TEST_REQUIRED')
