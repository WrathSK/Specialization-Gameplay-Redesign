"""F2 targeted actual Store/effect lifecycle and read-only database-copy checks."""
from pathlib import Path
import sqlite3, zlib
from project_paths import external_database
R=Path(__file__).resolve().parents[1]
# Use the known native-shaped fixture, retaining historical assertions unchanged.
s=(R/'DevelopmentTests/test_b143_tradition.py').read_text()
exec(s[:s.index("extra=r"+chr(39)*3)])
header=header.replace("'StandardizationDiscount',", "'ResearchTraditionEffects','StandardizationDiscount',")
extra=r'''
local nativeInfo=P.Info;local carrier={};local names={}
for _,n in ipairs({5,10,15,20,25})do
 local name='BUILDING_SPC_RESEARCH_TRADITION_'..n
 local row={BuildingType=name,Index=900+n,InternalOnly=true,PrereqDistrict='DISTRICT_CITY_CENTER',CitizenSlots=0,Housing=0}
 carrier[name]=row;carrier[row.Index]=row;names[n]=row.Index
end
P.Info=function(t,k)if t=='Buildings' and carrier[k]then return carrier[k]end;return nativeInfo(t,k)end
local freshBefore=fresh
fresh=function(...)
 local c=freshBefore(...);c.pillaged={};c.q.buildings.IsPillaged=function(_,id)return c.pillaged[id]==true end
 return c
end
local oldBoot=boot
function boot()
 oldBoot();SPCResearchTraditionEffects.Start(P,shared);Events.LoadScreenClose.Fire()
end
local function begin()
 start();GameConfiguration.GetGameSpeedType=function()return 'STANDARD'end
 GameInfo.GameSpeeds={STANDARD={CostMultiplier=100}};governor=4
 local c=fresh(1);register(c);complete(c,'DISTRICT_CAMPUS');invest(c,801);invest(c,802)
 return c
end
local function configured(c)
 local amount=0;local count=0
 for n,id in pairs(names)do if c.q.buildings[id]then amount=amount+n;count=count+1 end end
 assert(count<=1,'tiers stacked');return amount
end
local function tick()turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush()end
local c=begin();invest(c,803);flush();assert(configured(c)==5)
local other=fresh(2);register(other);complete(other,'DISTRICT_THEATER');local untouched=encode(record(other))
local state=encode(record(c));local changes=shared.ResearchTraditionEffects.changes
for _=1,5 do Events.GovernorChanged.Fire(0);flush();shared.ResearchTradition.Describe(0,c)end
assert(shared.ResearchTraditionEffects.changes==changes and encode(record(c))==state)
-- Every stage through real age handler; only four replacements, no per-turn writes.
for i=1,40 do tick();assert(configured(c)==5*(1+math.min(4,math.floor(i/10))))end
assert(shared.ResearchTraditionEffects.changes==changes+8 and encode(record(other))==untouched)
print('F2 STAGES / IDEMPOTENCE / ISOLATION PASS')
-- Same-turn qualification changes, no coarse once-per-turn suppression.
state=encode(record(c));governor=1;Events.GovernorChanged.Fire(0);flush();assert(configured(c)==0)
governor=4;Events.GovernorEstablished.Fire(0);flush();assert(configured(c)==25 and encode(record(c))==state)
-- UNKNOWN preserves last configuration; native-backed facts notification resumes.
governor=nil;Events.GovernorChanged.Fire(0);flush();assert(configured(c)==25 and shared.ResearchTraditionEffects.lastError)
governor=1;shared.ResearchTraditionEffects.Mark(0);flush();assert(configured(c)==0 and not shared.ResearchTraditionEffects.lastError)
governor=4;shared.ResearchTraditionEffects.Mark(0);flush();assert(configured(c)==25)
-- Cold load reconstructs exactly one tier without age/receipt mutation.
state=encode(record(c));c.q.buildings[names[25]]=nil;saved=true;boot()
assert(configured(c)==25 and encode(record(c))==state)
changes=shared.ResearchTraditionEffects.changes;Events.LoadScreenClose.Fire();flush()
assert(shared.ResearchTraditionEffects.changes==changes and encode(record(c))==state)
print('F2 ACTIVE / UNKNOWN / COLD_LOAD PASS')
-- Real confirmed ownership loss withdrawal, duplicate exit; ordinary/history retained.
local token=c.s.values.TOKEN;local age=record(c).researchTradition.age
local receipts=encode(record(c).investment);c.q.buildings[11]=true
loss(c,token,true);assert(configured(c)==0 and c.q.buildings[11])
assert(props[PREFIX..token].researchTradition.age==age and encode(props[PREFIX..token].investment)==receipts)
shared.CityProgressionStore.ExitConfirmed();assert(configured(c)==0)
saved=true;boot();retake(c);flush();assert(configured(c)==0)
assert(shared.CityProgressionStore.ReadTradition(0,c).state=='OWNER_POLICY_UNRESOLVED')
print('F2 CONFIRMED_EXIT / RETURN_POLICY_HOLD PASS')
-- Explicit guards do not reactivate; unknown interval and absent origin produce 0.
c=begin();invest(c,803);flush();turn=turn+2;Events.PlayerTurnActivated.Fire(0);flush()
assert(configured(c)==0 and record(c).researchTradition.state=='UNKNOWN_INTERVAL')
c=begin();invest(c,803);flush();c.q.buildings[names[5]]=nil;record(c).researchTradition=nil;saved=true;boot()
assert(configured(c)==0 and shared.ResearchTraditionEffects.Read(0,c)==0)
-- Failed native creation is reported, never written as persistent success.
c=begin();local create=P.CreateBuilding
P.CreateBuilding=function(q,id)if not carrier[id]then create(q,id)end end
invest(c,803);flush();assert(configured(c)==0 and shared.ResearchTraditionEffects.lastError)
assert(record(c).researchTradition.age==0 and shared.EffectiveFacts.Read(0,c).potential==4)
P.CreateBuilding=create;shared.ResearchTraditionEffects.Mark(0);flush();assert(configured(c)==5)
print('F2 MISSING_ORIGIN / UNKNOWN_INTERVAL / NATIVE_WRITE_FAILURE PASS')
'''
exec(compile(header+helpers+claim_setup+return_setup+extra+"\n"+chr(39)*3+")",str(__file__),'exec'))
with sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True) as source:
 db=sqlite3.connect(':memory:');source.backup(db)
# Fixture-only deterministic hash, as in existing SQL tests; not a claim about engine hashing.
db.create_function('Make_Hash',1,lambda value:zlib.crc32(value.encode()))
db.executescript((R/'Mod/Data/ResearchTradition.sql').read_text())
rows=db.execute("SELECT b.BuildingType,b.InternalOnly,b.CitizenSlots,b.Housing,m.ModifierType,a.Value FROM Buildings b JOIN BuildingModifiers bm USING(BuildingType) JOIN Modifiers m USING(ModifierId) JOIN ModifierArguments a USING(ModifierId) WHERE b.BuildingType LIKE 'BUILDING_SPC_RESEARCH_TRADITION_%' AND a.Name='Amount'").fetchall()
assert len(rows)==5
assert sorted(int(x[5]) for x in rows)==[5,10,15,20,25]
assert all(x[1:4]==(1,0,0) and x[4]=='MODIFIER_SINGLE_CITY_ADJUST_CITY_YIELD_MODIFIER' for x in rows)
assert db.execute("SELECT count(*) FROM BuildingModifiers WHERE BuildingType LIKE 'BUILDING_SPC_LV4_PERCENT_RESEARCH_%'").fetchone()[0]==0
assert db.execute("SELECT count(*) FROM ModifierArguments WHERE ModifierId LIKE 'SPC_RESEARCH_TRADITION_%' AND Name='YieldType' AND Value='YIELD_SCIENCE'").fetchone()[0]==5
print('F2 SQL STATIC_PASS: five exact hidden tiers, Science binding; old Research tombstones inert. Native effect still pending.')
