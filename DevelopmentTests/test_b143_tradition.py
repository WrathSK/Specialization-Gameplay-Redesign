"""P0-F1 scoped L3 tests: actual Store/Investment handlers, pure shadow. Not native evidence."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b140_templates.py').read_text()
exec(s[:s.index("extra=r"+chr(39)*3)])
# Current fixture boots Store's real include and the same report used by Gameplay.
header=header.replace('SPCClaimProjects.Start(P,shared);Events.LoadScreenClose.Fire()',
 'SPCClaimProjects.Start(P,shared);SPCResearchTradition.Start(P,shared);Events.LoadScreenClose.Fire()')
extra=r'''
local T=SPCResearchTradition
local function research()
 start();local c=fresh(1);register(c);complete(c,'DISTRICT_CAMPUS')
 invest(c,801);invest(c,802);return c
end
local function tick(n)turn=turn+n;Events.PlayerTurnActivated.Fire(0)end
local function tradition(c)return shared.CityProgressionStore.ReadTradition(0,c)end
local function speed()
 GameConfiguration.GetGameSpeedType=function()return 'STANDARD'end
 GameInfo.GameSpeeds={STANDARD={CostMultiplier=100}}
end
-- Actual prepare/consume/commit: only the final P4 receipt creates age, atomically.
local c=research();assert(record(c).researchTradition==nil)
local other=fresh(2);register(other);complete(other,'DISTRICT_THEATER')
local control=encode(record(other));local request=invest(c,803)
assert(tradition(c).age==0 and tradition(c).start==turn and tradition(c).receipt==request)
assert(record(c).investment.investments[request] and encode(record(other))==control)
local before=encode(props);local w=writes
Events.PlayerTurnActivated.Fire(0);a.Confirm(0,c,request)
speed();assert(shared.ResearchTradition.Describe(0,c):find('+5%%'))
for _=1,4 do shared.ResearchTradition.Describe(0,c);Events.GameCoreEventPublishComplete.Fire()end
assert(encode(props)==before and writes==w,'same-turn/diagnostic wrote state')
-- No governor/ACTIVE dependency; legitimate per-turn updates, no foreign callback writes.
governor=1;tick(1);assert(tradition(c).age==1 and shared.EffectiveFacts.Read(0,c).active==1)
before=encode(props);Events.PlayerTurnActivated.Fire(3);assert(encode(props)==before)
tick(1);assert(tradition(c).age==2 and encode(record(other))==control)
-- Normal save/cold-load preserves age; no double count. Next-turn load settles once.
before=encode(props);w=writes;saved=true;boot();assert(encode(props)==before and writes==w)
turn=turn+1;boot();assert(tradition(c).age==3);before=encode(props);boot();assert(encode(props)==before)
print('FIRST_P4 / ACTIVE / DUPLICATE / COLD_LOAD PASS')
-- Every independently floored threshold, including Quick 67% (6/13/20/26).
for _,s in ipairs({0.5,0.67,1,1.5,3})do
 for age=0,125 do
  local expected=5;for j=1,4 do if age>=math.floor(10*j*s)then expected=5*(j+1)end end
  assert(T.Shadow(age,s)==expected)
 end
end
assert(T.Shadow(12,0.67)==10 and T.Shadow(13,0.67)==15 and T.Shadow(999,1)==25)
assert(not pcall(T.Shadow,1,nil) and not pcall(T.Shadow,1,0))
-- Ordered identity transitions: pause/resume uses retained age, not absolute start.
local t=T.Begin(10,'receipt');t=T.Advance(t,11,'RESEARCH');t=T.Advance(t,11,'REALLOCATING')
assert(t.age==1 and t.state=='PAUSED_IDENTITY')
t=T.Advance(t,12,'NONE');t=T.Advance(t,13,'RESEARCH');assert(t.age==1)
t=T.Advance(t,14,'RESEARCH');assert(t.age==2)
print('SPEED / IDENTITY_PAUSE_RESUME PASS (pure contract, no respecialization UI)')
-- Existing P4 cannot silently receive a synthesized origin; malformed state fails closed.
c=research();invest(c,803);record(c).researchTradition=nil;saved=true;boot();speed()
assert(tradition(c)==nil and shared.ResearchTradition.Describe(0,c):find('起点不可确认'))
c=research();invest(c,803);record(c).researchTradition.age=-1;saved=true;boot()
assert(not pcall(tradition,c))
-- Uncertain reference does not touch history/other cities; missed interval is explicit.
c=research();invest(c,803);local token=c.s.values.TOKEN;c.s.values.TOKEN='conflict'
before=encode(props);tick(1);assert(encode(props)==before and not pcall(tradition,c))
c.s.values.TOKEN=token;tick(1)
assert(tradition(c).age==0 and tradition(c).state=='UNKNOWN_INTERVAL')
print('MISSING_ORIGIN / CORRUPT / UNKNOWN PASS')
-- Confirmed ownership boundary retains age through actual loss/cold-load/return.
c=research();invest(c,803);tick(1);token=c.s.values.TOKEN
loss(c,token,true)
local held=props[PREFIX..token].researchTradition
assert(held.age==1 and held.state=='OWNER_POLICY_UNRESOLVED')
saved=true;boot();turn=turn+1;retake(c);flush();tick(1)
assert(tradition(c).age==1 and tradition(c).state=='OWNER_POLICY_UNRESOLVED')
print('OWNER_POLICY_HOLD PASS: retained, never reactivated/caught up')
-- The final write failing cannot persist P4 without its origin, or origin without P4.
c=research();token=c.s.values.TOKEN;local original=Game.SetProperty
Game.SetProperty=function(self,key,value)
 if key==PREFIX..token and value.researchTradition then return end
 return original(self,key,value)
end
addunit(803,c);assert(a.Prepare(0,c,803,'FAIL',false):find('PREPARED'))
assert(a.Confirm(0,c,shared.InvestmentPreview.token):find('HELD'))
assert(props[PREFIX..token].researchTradition==nil and props[PREFIX..token].investment.pending.stage=='CONSUMED_CONFIRMED')
Game.SetProperty=original;saved=true;boot()
assert(tradition(c).age==0 and shared.EffectiveFacts.Read(0,c).potential==4)
print('ATOMIC_FAILURE / CONFIRMED_DEBIT_RECOVERY PASS')
print('B143 LOCAL_SIMULATION_PASS: no Science/carrier effects; native validation pending')
'''
exec(compile(header+helpers+claim_setup+return_setup+extra+"\n"+chr(39)*3+")",str(__file__),'exec'))
