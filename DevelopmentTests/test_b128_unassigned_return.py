"""B128 targeted actual-handler lifecycle matrix; inherited B124 Claim assertions unchanged."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b124_claim.py').read_text()
extra=r"""
local function make(mode)
 start();local c
 if mode=='FOUND'then c=fresh(1);register(c)
 elseif mode=='EMPTY'then c=ai(fresh(1));take(c)
 else c=conquered(1,'DISTRICT_CAMPUS')end
 local token=c.s.values.TOKEN;flush();return c,token
end
local function loss(c,token,erase)
 c.s.ref.owner=3;c.s.ref.cityID=44;Events.CityTransfered.Fire(3,44,0);flush()
 assert(props[PREFIX..token].stage=='HELD_TRANSFER' and not next(c.q.buildings))
 if erase then c.s.values.TOKEN=nil end
 saved=true;boot();flush()
 assert(props[PREFIX..token].stage=='HELD_TRANSFER' and not pcall(shared.EffectiveFacts.Read,0,c))
end
local function retake(c,skipAdded)
 local old=c:GetID();local id=old+1000
 GameEvents.CityConquered.Fire(0,3,id,c:GetX(),5)
 Events.CityRemovedFromMap.Fire(3,old)
 c.s.ref.owner=0;c.s.ref.cityID=id
 if not skipAdded then Events.CityAddedToMap.Fire(0,id,c:GetX(),5)end
 Events.CityInitialized.Fire(0,id,c:GetX(),5)
 -- Engine may publish restored district state before ownership confirmation.
 if ds[(c:GetX()+1)..':5'] then GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_INDUSTRIAL_ZONE',c:GetX()+1,5)end
 GameEvents.CityBuilt.Fire(0,id,c:GetX(),5)
 Events.CityTransfered.Fire(0,id,3);flush()
end
for _,mode in ipairs({'FOUND','EMPTY','CLAIM'})do for _,erase in ipairs({false,true})do
 local c,token=make(mode)
 local control=fresh(2);register(control);complete(control,'DISTRICT_THEATER');invest(control,920)
 local unchanged=encode(record(control));local origin=encode(props[PREFIX..token].origin)
 local acquisition=encode(props[PREFIX..token].acquisition)
 if mode=='CLAIM'then request(c,'RESEARCH');Events.PlayerTurnDeactivated.Fire(0)end
 loss(c,token,erase)
 -- Foreign completions do not grant identity or extend frozen candidates.
 complete(c,'DISTRICT_INDUSTRIAL_ZONE');turn=turn+2
 retake(c)
 local r=props[PREFIX..token]
 assert(r.stage=='ACTIVE' and r.progression=='UNASSIGNED',d.Describe(0,c))
 assert(r.current.cityID==c:GetID() and r.currentFirst==nil and r.base.first==nil)
 assert(encode(r.origin)==origin and encode(r.acquisition)==acquisition and not r.claimTimer)
 assert(shared.EffectiveFacts.Read(0,c).potential==0 and shared.EffectiveFacts.Read(0,c).active==0)
 assert(encode(record(control))==unchanged)
 local snap=encode(r);Events.CityTransfered.Fire(0,c:GetID(),3);flush();assert(encode(props[PREFIX..token])==snap)
 saved=true;boot();flush();assert(encode(props[PREFIX..token])==snap and shared.EffectiveFacts.Read(0,c).specialization=='NONE')
 if mode=='CLAIM'then
  assert(c.q.buildings[201] and not c.q.buildings[203])
  assert(shared.ClaimProjects.views['0:'..c:GetID()].stage=='STOPPED')
  -- Queue retention never restarts timing or completes an interrupted project.
  Events.PlayerTurnActivated.Fire(0);flush();assert(not props[PREFIX..token].claim)
  c.q.target='BUILDING_TEST';Events.CityProductionChanged.Fire(0,c:GetID());flush()
  request(c,'RESEARCH');assert(props[PREFIX..token].claimTimer.reference.cityID==c:GetID())
  local oldref=M.Copy(props[PREFIX..token].origin)
  local bad={reference=oldref,token=token,kind='RESEARCH',project='PROJECT_SPC_CLAIM_RESEARCH',turn=turn,districtID=201,type='DISTRICT_CAMPUS'}
  assert(not pcall(d.ClaimComplete,0,c,bad),'old reference accepted')
  saved=true;boot();assert(props[PREFIX..token].claimTimer.stage=='ACTIVE')
  Events.PlayerTurnDeactivated.Fire(0);turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush()
  assert(props[PREFIX..token].claim and encode(props[PREFIX..token].claim.reference)==origin)
 else complete(c,'DISTRICT_CAMPUS')end
 r=props[PREFIX..token];assert(r.progression=='SPECIALIZED' and r.base.specialization=='RESEARCH' and r.currentFirst)
 assert(shared.EffectiveFacts.Read(0,c).first.districtID==r.currentFirst.districtID)
 invest(c,921);saved=true;boot();flush()
 assert(shared.EffectiveFacts.Read(0,c).potential==2 and encode(record(control))==unchanged)
 -- Subsequent specialized loss/return and current Governor remain correct.
 governor=1;loss(c,token,true);retake(c)
 assert(shared.EffectiveFacts.Read(0,c).potential==2 and shared.EffectiveFacts.Read(0,c).active==1)
end end
-- Same coordinates or owner change without the required sequence are insufficient.
for _,case in ipairs({'MISSING_ADDED','BAD_TOKEN','NO_PROOF'})do
 local c,token=make('CLAIM');loss(c,token,true)
 if case=='BAD_TOKEN'then c.s.values.TOKEN='different' end
 if case=='NO_PROOF'then c.s.ref.owner=0;c.s.ref.cityID=1044;Events.CityTransfered.Fire(0,1044,3);flush()
 else retake(c,case=='MISSING_ADDED')end
 assert(props[PREFIX..token].stage=='HELD_TRANSFER' and not pcall(shared.EffectiveFacts.Read,0,c))
 assert(not props[PREFIX..token].claim and not next(c.q.buildings))
end
-- Unknown owner/event, unrelated city and duplicate loss cannot revive or rewrite records.
local c,token=make('FOUND');loss(c,token,true);local before=encode(props[PREFIX..token])
Events.CityTransfered.Fire(nil,nil,nil);Events.CityTransfered.Fire(0,99999,3);flush()
assert(encode(props[PREFIX..token])==before)
-- All four Claim kinds use current anchors; missing Industry template history stays held.
for _,v in ipairs({{'RESEARCH','DISTRICT_CAMPUS'},{'CULTURE','DISTRICT_THEATER'},{'INDUSTRY','DISTRICT_INDUSTRIAL_ZONE'},{'COMMERCE','DISTRICT_COMMERCIAL_HUB'}})do
 start();local q=conquered(1,v[2]);local key=q.s.values.TOKEN;loss(q,key,true);retake(q)
 request(q,v[1]);Events.PlayerTurnDeactivated.Fire(0);turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush()
 assert(shared.EffectiveFacts.Read(0,q).specialization==v[1])
 invest(q,992);saved=true;boot();assert(shared.EffectiveFacts.Read(0,q).potential==2)
 if v[1]=='INDUSTRY'then
  local ok,why=pcall(d.ReadTemplates,q);assert(not ok and tostring(why):find('TEMPLATES_HISTORY_UNAVAILABLE'))
 end
end
-- Failed return persistence cannot make the city readable; other records survive.
local q,key=make('CLAIM');local other=fresh(2);register(other);local otherBefore=encode(record(other))
loss(q,key,true);failKey=PREFIX..key;retake(q)
assert(props[PREFIX..key].stage=='HELD_TRANSFER' and not pcall(shared.EffectiveFacts.Read,0,q))
assert(encode(record(other))==otherBefore and shared.EffectiveFacts.Read(0,other).potential==0)
failKey=nil
print('B128 LOCAL_SIMULATION_PASS: 3 modes x retained/missing token, foreign coldload, frozen scope, P0/current reference, new completion/Claim/investment, second specialized return, controls and rejection guards')
"""
s=s.replace('exec(compile(header+helpers+cases+', 'cases+=extra\nexec(compile(header+helpers+cases+')
exec(compile(s,str(R/'DevelopmentTests/test_b124_claim.py'),'exec'))
