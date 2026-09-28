"""B110 scoped actual-handler conquest snapshot/mode persistence; native timing unproven."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
# Inherited B109 production regression; only release stamp differs, no assertions removed.
s=(R/'DevelopmentTests/test_b109_session_origin.py').read_text().replace('"==\'136\'"','"==\'137\'"').replace('"modinfo136"','"modinfo137"')
exec(compile(s,str(R/'DevelopmentTests/test_b109_session_origin.py'),'exec'))
s=(R/'DevelopmentTests/test_b108_e2_multicity.py').read_text()
header=s[:s.index('-- Scale and write locality')]
cases=r'''
local function ai(c)
 c.s.ref.owner=3
 Players[3]={IsMajor=function()return true end,IsHuman=function()return false end}
 c.GetDistricts=function()local rows={};for _,v in pairs(ds)do if v:GetCity()==c then rows[#rows+1]=v end end;return {Members=function()return ipairs(rows)end}end
 return c
end
local function district(c,kind,id,done)
 local v={GetCity=function()return c end,GetOwner=function()return c:GetOwner()end,GetID=function()return id end,
 GetType=function()return kind end,IsComplete=function()return done end}
 ds[id..':5']=v;return v
end
local function take(c,mode)
 local old=c:GetID();c.s.ref.owner=0;c.s.ref.cityID=old+1000
 GameEvents.CityBuilt.Fire(0,c:GetID(),c:GetX(),c:GetY())
 GameEvents.CityConquered.Fire(0,3,c:GetID(),c:GetX(),c:GetY())
 Events.CityRemovedFromMap.Fire(3,old)
 if mode~='missing-added' then Events.CityAddedToMap.Fire(0,c:GetID(),c:GetX(),c:GetY())end
 Events.CityInitialized.Fire(0,c:GetID(),c:GetX(),c:GetY())
 Events.CityTransfered.Fire(0,c:GetID(),3)
end
-- One candidate is NEVER auto-claimed. Later construction cannot append or specialize.
start();local control=fresh(1);register(control);complete(control,'DISTRICT_CAMPUS');invest(control,890)
local prior=encode(record(control));local c=ai(fresh(2));district(c,'DISTRICT_CAMPUS',201,true);district(c,'DISTRICT_THEATER',202,false)
take(c);assert(record(c) and record(c).schema==3,d.Describe(0,c))
assert(record(c).acquisition.mode=='LEGACY_CLAIM' and record(c).acquisition.legacySet.RESEARCH)
assert(not record(c).acquisition.legacySet.CULTURE and shared.EffectiveFacts.Read(0,c).potential==0)
local frozen=encode(record(c));complete(c,'DISTRICT_THEATER');assert(encode(record(c))==frozen)
addunit(891,c);assert(a.Prepare(0,c,891,'NOCLAIM',false):find('SPECIALIZATION_REQUIRED') and kills==1)
Events.CityTransfered.Fire(0,c:GetID(),3);assert(encode(record(c))==frozen)
local before=encode(props);local n=writes;saved=true;boot();assert(writes==n and encode(props)==before)
assert(record(c).acquisition.mode=='LEGACY_CLAIM' and shared.EffectiveFacts.Read(0,c).potential==0)
assert(encode(record(control))==prior and shared.EffectiveFacts.Read(0,control).potential==2)
assert(d.Describe(0,c):find('待完成对应认定项目') and d.Describe(0,c):find('科研'))
-- Empty snapshot: subsequent valid completion locks once; persisted, no load inference.
start();c=ai(fresh(1));district(c,'DISTRICT_CAMPUS',201,false);take(c)
assert(record(c).acquisition.mode=='FIRST_COMPLETION' and record(c).base.potential==0)
saved=true;n=writes;boot();assert(writes==n and shared.EffectiveFacts.Read(0,c).potential==0)
complete(c,'DISTRICT_THEATER');complete(c,'DISTRICT_CAMPUS')
assert(shared.EffectiveFacts.Read(0,c).specialization=='CULTURE' and shared.EffectiveFacts.Read(0,c).potential==1)
invest(c,801);before=encode(props);boot();assert(encode(props)==before and shared.EffectiveFacts.Read(0,c).potential==2)
-- All four families + replacement, deduplicated. Incomplete remains excluded.
start();c=ai(fresh(1));local rows=P.Rows
P.Rows=function(t)if t=='DistrictReplaces'then return {{CivUniqueDistrictType='DISTRICT_TEST_REPLACEMENT',ReplacesDistrictType='DISTRICT_CAMPUS'}}end;return rows(t)end
for i,k in ipairs({'DISTRICT_CAMPUS','DISTRICT_TEST_REPLACEMENT','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE','DISTRICT_COMMERCIAL_HUB'})do district(c,k,200+i,true)end
take(c);local set=record(c).acquisition.legacySet;local count=0;for _ in pairs(set)do count=count+1 end;assert(count==4);P.Rows=rows
-- Unreadable snapshot / incomplete chain / nonmajor/human are never known-empty.
for _,mode in ipairs({'missing-added','unknown-completeness','not-major','human','legacy-property','snapshot-throws'})do
 start();c=ai(fresh(1));if mode=='unknown-completeness'then district(c,'DISTRICT_CAMPUS',201,nil)end
 if mode=='not-major'then Players[3].IsMajor=function()return false end end
 if mode=='human'then Players[3].IsHuman=function()return true end end
 if mode=='legacy-property'then c.s.values.TOKEN='UNPROVEN' end
 if mode=='snapshot-throws'then c.GetDistricts=function()error('read failed')end end
 take(c,mode);assert(not record(c) and not pcall(shared.EffectiveFacts.Read,0,c),mode)
 saved=true;boot();assert(not pcall(shared.EffectiveFacts.Read,0,c),mode..' reload')
end
-- Trade has no conquest proof; retained indexed city isn't enrolled as a fresh AI city.
start();c=ai(fresh(1));c.s.ref.owner=0;Events.CityAddedToMap.Fire(0,c:GetID(),c:GetX(),c:GetY());Events.CityInitialized.Fire(0,c:GetID(),c:GetX(),c:GetY());Events.CityTransfered.Fire(0,c:GetID(),3);assert(not record(c))
start();c=fresh(1);register(c);complete(c,'DISTRICT_CAMPUS');local token=c.s.values.TOKEN;ai(c);take(c)
assert(props[INDEX].counter==1 and c.s.values.TOKEN==token and record(c).schema==2 and not record(c).acquisition)
-- Failed durable write leaves reserved identity held, no fallback/re-admission after load.
start();c=ai(fresh(1));failKey=PREFIX..'DEV-B013-P0-1';take(c);assert(props[INDEX].counter==1 and not record(c))
failKey=nil;saved=true;boot();assert(not pcall(shared.EffectiveFacts.Read,0,c));Events.CityTransfered.Fire(0,c:GetID(),3);assert(not record(c))
-- Corrupt mode/set is rejected, never normalized on load.
start();c=ai(fresh(1));district(c,'DISTRICT_CAMPUS',201,true);take(c);record(c).acquisition.mode='FIRST_COMPLETION';boot();assert(not pcall(shared.EffectiveFacts.Read,0,c))
-- A valid post-transfer completion delivered reentrantly during persistence is not lost.
start();c=ai(fresh(1));local fired=false
hook=function(key)if key==INDEX and not fired then fired=true;complete(c,'DISTRICT_CAMPUS')end end
take(c);hook=nil;assert(shared.EffectiveFacts.Read(0,c).specialization=='RESEARCH')
-- The same callback cannot alter a nonempty candidate set or auto-claim one candidate.
start();c=ai(fresh(1));district(c,'DISTRICT_CAMPUS',201,true);fired=false
hook=function(key)if key==INDEX and not fired then fired=true;complete(c,'DISTRICT_THEATER')end end
take(c);hook=nil;assert(record(c).base.specialization=='NONE' and not record(c).acquisition.legacySet.CULTURE)
-- No transfer completion means no record; an event from a later turn cannot finish it.
start();c=ai(fresh(1));c.s.ref.owner=0;GameEvents.CityConquered.Fire(0,3,c:GetID(),c:GetX(),c:GetY())
Events.CityAddedToMap.Fire(0,c:GetID(),c:GetX(),c:GetY());Events.CityInitialized.Fire(0,c:GetID(),c:GetX(),c:GetY())
assert(not record(c));turn=turn+1;Events.CityTransfered.Fire(0,c:GetID(),3);assert(not record(c))
print('B110 LOCAL_SIMULATION_PASS: frozen nonempty/single/multi candidates, empty first completion, persistence/investment isolation, exact event gate, no-history/major guard, duplicate/failure/corrupt-record handling')
'''
exec(compile(header+cases+"\n''')",str(R/'DevelopmentTests/test_b108_e2_multicity.py'),'exec'))
