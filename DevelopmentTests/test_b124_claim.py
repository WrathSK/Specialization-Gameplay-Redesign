"""B124 targeted L3 actual Store + Claim handlers; engine/native gate remains separate."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b108_e2_multicity.py').read_text()
header=s[:s.index('-- Scale and write locality')].replace("'Standardization']:","'Standardization','ClaimProjects']:")
header=header.replace("Events.LoadScreenClose.Fire()", "SPCClaimProjects.Start(P,shared);Events.LoadScreenClose.Fire()") # boot text actually extracted by header below
header=header.replace("l.execute(h+r", "h=h.replace('Events.LoadScreenClose.Fire()', 'SPCClaimProjects.Start(P,shared);Events.LoadScreenClose.Fire()')\nl.execute(h+r")
helpers=(R/'DevelopmentTests/test_b111_district_snapshot.py').read_text().split("cases=r"+chr(39)*3,1)[1].split('-- One candidate',1)[0]
cases=r'''
local info=P.Info
local pr={};local buildings={};local byName={};local finishCalls=0
for i,k in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do
 local name='PROJECT_SPC_CLAIM_'..k;local row={ProjectType=name,Index=100+i,Hash=100+i};pr[name]=row;pr[100+i]=row
 local b='BUILDING_SPC_CLAIM_'..k;buildings[b]={BuildingType=b,Index=200+i,InternalOnly=true};byName[200+i]=b
end
P.Info=function(t,k)if t=='Projects'then return pr[k]elseif t=='Buildings'then return buildings[k]end;return info(t,k)end
P.Call=function(o,k,...)if not o or type(o[k])~='function'then return false end;return pcall(o[k],o,...)end
P.HasBuilding=function(b,id)return b[id]==true end
P.CreateBuilding=function(q,id)q.buildings[id]=true end
P.RemoveBuilding=function(b,id)b[id]=nil end
local rawReset=reset
function reset(...)rawReset(...);GameInfo.Projects=pr end
local freshOld=fresh
fresh=function(...)
 local c=freshOld(...);local q={target='NONE',size=0,buildings={}}
 c.q=q;c.GetBuildQueue=function()return q end;c.GetBuildings=function()return q.buildings end
 q.CurrentlyBuilding=function()return q.target end;q.GetSize=function()return q.size end
 q.GetCurrentProductionTypeHash=function()return pr[q.target] and pr[q.target].Hash or 0 end
 q.FinishProgress=function()
  finishCalls=finishCalls+1;local row=assert(pr[q.target]);q.target='NONE';q.size=0
  Events.CityProductionChanged.Fire(c:GetOwner(),c:GetID())
  Events.CityProjectCompleted.Fire(c:GetOwner(),c:GetID(),row.Index)
 end
 return c
end
local function request(c,kind)
 c.q.target='PROJECT_SPC_CLAIM_'..kind;c.q.size=1
 shared.ClaimProjects.Request(0,{CityID=c:GetID(),Project=c.q.target,StartTurn=turn})
end
local function flush()Events.GameCoreEventPublishComplete.Fire()end
local function conquered(i,kind)
 local c=ai(fresh(i));district(c,kind,200+i,true);take(c);flush();return c
end
start();local aCity=conquered(1,'DISTRICT_COMMERCIAL_HUB');local bCity=conquered(2,'DISTRICT_CAMPUS')
assert(aCity.q.buildings[204] and not aCity.q.buildings[203]);assert(bCity.q.buildings[201])
request(aCity,'COMMERCE');request(bCity,'RESEARCH')
assert(record(aCity).base.specialization=='NONE' and record(aCity).claimTimer.stage=='ACTIVE')
local before=encode(props);local n=writes;saved=true;boot();assert(encode(props)==before and writes==n,'reload changed timer')
Events.PlayerTurnDeactivated.Fire(0);assert(record(aCity).claimTimer.deactivated)
turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush()
assert(record(aCity).claim and record(aCity).base.specialization=='COMMERCE',shared.ClaimProjects.views['0:'..aCity:GetID()].reason)
assert(record(bCity).base.specialization=='RESEARCH' and finishCalls==2)
assert(not next(aCity.q.buildings) and not next(bCity.q.buildings))
local receipt=encode(record(aCity));Events.CityProjectCompleted.Fire(0,aCity:GetID(),104);flush();assert(encode(record(aCity))==receipt)
assert(shared.EffectiveFacts.Read(0,aCity).potential==1);invest(aCity,1991);assert(shared.EffectiveFacts.Read(0,aCity).potential==2)
before=encode(props);boot();assert(encode(props)==before and shared.EffectiveFacts.Read(0,aCity).potential==2)
-- Multi-candidate completion chooses exactly one; native Cheat event valid without timer.
start();local c=ai(fresh(1));district(c,'DISTRICT_CAMPUS',201,true);district(c,'DISTRICT_THEATER',202,true);take(c);flush()
assert(c.q.buildings[201] and c.q.buildings[202]);Events.CityProjectCompleted.Fire(0,c:GetID(),102);flush()
assert(record(c).base.specialization=='CULTURE' and not next(c.q.buildings));before=encode(record(c));Events.CityProjectCompleted.Fire(0,c:GetID(),101);flush();assert(encode(record(c))==before)
-- Ineligible domain cannot write; ordinary completion and no candidate leave no Claim.
start();c=conquered(1,'DISTRICT_CAMPUS');before=encode(record(c));Events.CityProjectCompleted.Fire(0,c:GetID(),104);flush();assert(encode(record(c))==before)
request(c,'COMMERCE');assert(not record(c).claimTimer)
-- Target change cancels, reselect starts anew; no replay of stale native timer.
request(c,'RESEARCH');c.q.target='BUILDING_TEST';Events.CityProductionChanged.Fire(0,c:GetID());flush();assert(record(c).claimTimer.stage=='STOPPED')
turn=turn+1;request(c,'RESEARCH');assert(record(c).claimTimer.start==turn)
Events.PlayerTurnDeactivated.Fire(0);turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush();assert(record(c).claim)
-- Uncertain native call persisted CALLING, load/duplicate activation never calls twice.
start();c=conquered(1,'DISTRICT_CAMPUS');request(c,'RESEARCH');local calls=0;c.q.FinishProgress=function()calls=calls+1 end
Events.PlayerTurnDeactivated.Fire(0);turn=turn+1;Events.PlayerTurnActivated.Fire(0);assert(record(c).claimTimer.stage=='CALLING')
boot();Events.PlayerTurnActivated.Fire(0);assert(calls==1 and not record(c).claim)
-- Ownership loss clears timing but preserves candidate history, exact markers withdrawn.
start();c=conquered(1,'DISTRICT_CAMPUS');request(c,'RESEARCH');local token=c.s.values.TOKEN
c.s.ref.owner=3;c.s.ref.cityID=44;Events.CityTransfered.Fire(3,44,0)
assert(props[PREFIX..token].stage=='HELD_TRANSFER' and props[PREFIX..token].claimTimer==nil)
assert(not next(c.q.buildings) and props[PREFIX..token].acquisition.legacySet.RESEARCH)
-- Failed completion write cannot publish specialization, blocks investment after reload.
start();c=conquered(1,'DISTRICT_CAMPUS');before=encode(record(c));failKey=PREFIX..c.s.values.TOKEN
Events.CityProjectCompleted.Fire(0,c:GetID(),101);flush();assert(encode(record(c))==before and not pcall(shared.EffectiveFacts.Read,0,c))
failKey=nil;boot();assert(shared.EffectiveFacts.Read(0,c).potential==0)
-- Corrupt extension rejected, no normalization/recovery inference.
request(c,'RESEARCH');record(c).claimTimer.token='wrong';boot();assert(not pcall(shared.EffectiveFacts.Read,0,c))
-- Saved end-turn confirmation survives a load on the next turn without re-activation.
start();c=conquered(1,'DISTRICT_CAMPUS');request(c,'RESEARCH');Events.PlayerTurnDeactivated.Fire(0)
turn=turn+1;boot();assert(record(c).claim and record(c).base.specialization=='RESEARCH')
-- Away/back before publish still invalidates the old continuous occupancy.
start();c=conquered(1,'DISTRICT_CAMPUS');request(c,'RESEARCH')
c.q.target='BUILDING_OTHER';Events.CityProductionChanged.Fire(0,c:GetID());c.q.target='PROJECT_SPC_CLAIM_RESEARCH';flush()
assert(record(c).claimTimer.stage=='STOPPED');request(c,'RESEARCH');assert(record(c).claimTimer.stage=='ACTIVE')
-- True multi-item queue, stale request turn and other player never begin.
start();c=conquered(1,'DISTRICT_CAMPUS');c.q.target='PROJECT_SPC_CLAIM_RESEARCH';c.q.size=2
shared.ClaimProjects.Request(0,{CityID=c:GetID(),Project=c.q.target,StartTurn=turn});assert(not record(c).claimTimer)
c.q.size=1;shared.ClaimProjects.Request(0,{CityID=c:GetID(),Project=c.q.target,StartTurn=turn-1});assert(not record(c).claimTimer)
shared.ClaimProjects.Request(3,{CityID=c:GetID(),Project=c.q.target,StartTurn=turn});assert(not record(c).claimTimer)
-- No write/scan loop after stable publish; unknown identity cannot grant or erase ledger.
flush();local stableWrites=writes;for _=1,10 do flush()end;assert(writes==stableWrites)
local snapshot=encode(record(c));local token=c.s.values.TOKEN;c.s.values.TOKEN='conflict'
Events.CityProductionChanged.Fire(0,c:GetID());flush();assert(encode(props[PREFIX..token])==snapshot and not next(c.q.buildings))
c.s.values.TOKEN=token
print('B124 LOCAL_SIMULATION_PASS: actual Claim and per-city record handlers, dual-city timing, save/load, native completion, receipt/idempotence, investment, marker exit, unknown/failure guards')
'''
exec(compile(header+helpers+cases+"\n"+chr(39)*3+")",str(R/'DevelopmentTests/test_b124_claim.py'),'exec'))
