"""B140 scoped actual Store/Standardization/Claim lifecycle tests, not native PASS.
Reuse existing fixtures without changing historical tests or assertions.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
claim_source=(R/'DevelopmentTests/test_b124_claim.py').read_text()
exec(claim_source[:claim_source.index("cases=r"+chr(39)*3)])
# Current governor facts use the real Probe reader, with native-shaped fixture properties.
header=header.replace("'CityIdentityRead',", "'Probe','CityIdentityRead',").replace("'Standardization',", "'StandardizationDiscount','Standardization',")
header=header.replace('l=LuaRuntime()', "l=LuaRuntime()\nl.globals().include=lambda name:l.execute((R/'Mod'/(name+'.lua')).read_text())")
old_gate="CityRoleFacts=function(c)return {owner=c:GetOwner(),cityID=c:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=governor}end,"
new_getter="""function c:GetProperty(k)
 if k=='SPC_P0_GOV_CONTROL_A007' then return governor~=nil and 1 or nil end
 if k=='SPC_P0_GOV_PRESENT' or k=='SPC_P0_GOV_ESTABLISHED' then return governor and governor>=2 and 1 or 0 end
 for level=2,4 do if k=='SPC_P0_GOV_REQ_'..level then return governor and governor>=level and 1 or 0 end end
 for n,key in pairs(M.Keys)do"""
header=header.replace('l.execute(h+r', "h=h.replace("+repr(old_gate)+",'GovernorGate=SPCP0.GovernorGate,').replace('function c:GetProperty(k)for n,key in pairs(M.Keys)do',"+repr(new_getter)+")\nl.execute('SPCP0.IsTestPlayer=function(pid)return pid==0 end')\nl.execute(h+r")
claim_setup=claim_source.split("cases=r"+chr(39)*3,1)[1].split('start();local aCity',1)[0]
return_setup=(R/'DevelopmentTests/test_b128_unassigned_return.py').read_text().split('extra=r'+chr(34)*3,1)[1].split("for _,mode in ipairs",1)[0]
# Ordinary buildings survive withdrawal; only Claim-owned markers disappear.
return_setup=return_setup.replace('not next(c.q.buildings)', 'not c.q.buildings[201] and not c.q.buildings[202] and not c.q.buildings[203] and not c.q.buildings[204]')
# Observe the persistent pending flag before publish/cold load where requested.
return_setup=return_setup.replace('Events.CityTransfered.Fire(0,id,3);flush()', 'Events.CityTransfered.Fire(0,id,3)')
extra=r'''
local catalogRows={
 BUILDING_A={index=11,district='DISTRICT_INDUSTRIAL_ZONE',tier=1},
 BUILDING_B={index=12,district='DISTRICT_INDUSTRIAL_ZONE',tier=2},
 BUILDING_C={index=13,district='DISTRICT_CAMPUS',tier=1}}
SPCStandardizationCatalog={Build=function()return {buildings=catalogRows}end}
local baseInfo=P.Info
P.Info=function(t,k)
 if t=='Buildings'then for id,row in pairs(catalogRows)do if k==row.index or k==id then return {BuildingType=id,Index=row.index}end end end
 return baseInfo(t,k)
end
local originalBoot=boot
function boot()
 originalBoot();SPCStandardization.Start(P,shared);Events.LoadScreenClose.Fire()
end
local function ledger(c)return shared.Standardization.ReadLedger(0,c)end
local function claimIndustry(c)
 Events.CityProjectCompleted.Fire(0,c:GetID(),103);flush()
end
local function industry()
 start();local c=fresh(1);register(c);c.q.buildings[11]=true
 complete(c,'DISTRICT_INDUSTRIAL_ZONE');flush()
 assert(ledger(c).learned.BUILDING_A)
 return c,c.s.values.TOKEN
end
-- A: first Claim after an unassigned loss/return; foreign present buildings qualify.
start();local c=conquered(1,'DISTRICT_INDUSTRIAL_ZONE');local token=c.s.values.TOKEN
local other=fresh(2);register(other);complete(other,'DISTRICT_CAMPUS');invest(other,801)
local control=encode(record(other));loss(c,token,true)
c.q.buildings[11]=true;retake(c);flush()
assert(props[PREFIX..token].progression=='UNASSIGNED' and props[PREFIX..token].templates==nil)
claimIndustry(c);local r=props[PREFIX..token]
assert(r.templateLifecycle.state=='INITIALIZED' and not r.templateLifecycle.reconcilePending)
assert(ledger(c).learned.BUILDING_A and encode(record(other))==control)
invest(c,802);local receipt=encode(r.investment);saved=true;boot();flush()
assert(ledger(c).learned.BUILDING_A and shared.EffectiveFacts.Read(0,c).potential==2 and encode(record(other))==control)
-- Normal first-completion path, including return before its first Industry identity.
start();c=fresh(1);register(c);token=c.s.values.TOKEN;loss(c,token,true)
c.q.buildings[12]=true;retake(c);flush();complete(c,'DISTRICT_INDUSTRIAL_ZONE');flush()
assert(ledger(c).learned.BUILDING_B)
print('A PASS: actual Claim + first completion, foreign currently present sources')
-- B/C: retain A even absent, add B on recapture; never backfill removed/unobserved C.
c,token=industry();invest(c,810);local investments=encode(props[PREFIX..token].investment)
loss(c,token,true);c.q.buildings[11]=nil;c.q.buildings[12]=true;c.q.buildings[13]=nil
retake(c);r=props[PREFIX..token];assert(r.templateLifecycle.reconcilePending)
assert(not pcall(ledger,c),'pending ledger exposed as synchronized source')
-- F: persisted pending survives cold load without relying on the session return queue.
saved=true;boot();flush();r=props[PREFIX..token]
assert(ledger(c).learned.BUILDING_A and ledger(c).learned.BUILDING_B and not ledger(c).learned.BUILDING_C)
assert(encode(r.investment)==investments and not r.templateLifecycle.reconcilePending)
local snap=encode(props);local writesBefore=writes;boot();flush()
assert(encode(props)==snap and writes==writesBefore and shared.Standardization.scans==0)
print('B/C/F PASS: union, no reverse deletion, pending/settled cold load, receipts')
-- E: duplicate return/project/building notifications; only unseen template writes once.
local scans=shared.Standardization.scans;local before=encode(props)
Events.CityTransfered.Fire(0,c:GetID(),3)
for _=1,3 do Events.CityProjectCompleted.Fire(0,c:GetID(),103);flush();Events.PlayerTurnActivated.Fire(0)end
assert(encode(props)==before and shared.Standardization.scans==scans)
c.q.buildings[13]=true
Events.BuildingAddedToMap.Fire(c:GetX(),5,13,0);flush()
assert(ledger(c).learned.BUILDING_C,'recaptured city suppressed native building notification')
before=encode(props);for _=1,3 do Events.BuildingAddedToMap.Fire(c:GetX(),5,13,0);flush()end
assert(encode(props)==before)
print('E PASS: no duplicate scan/write; genuine same-turn addition retained')
-- Initialized-empty is reliable, not missing; legacy reliable table may adopt once.
start();c=fresh(1);register(c);complete(c,'DISTRICT_INDUSTRIAL_ZONE');flush()
assert(next(ledger(c).learned)==nil and ledger(c).revision==1)
record(c).templateLifecycle=nil;saved=true;boot();flush()
assert(record(c).templateLifecycle.state=='INITIALIZED' and next(ledger(c).learned)==nil)
before=encode(props);boot();flush();assert(encode(props)==before)
-- D: missing initialized history, ambiguous old nil, corrupt table/state all stay held.
for _,mode in ipairs({'MISSING','OLD_NIL','CORRUPT_TABLE','CORRUPT_STATE'})do
 c,token=industry();other=fresh(2);register(other);complete(other,'DISTRICT_CAMPUS')
 control=encode(record(other));r=props[PREFIX..token]
 if mode=='MISSING'then r.templates=nil
 elseif mode=='OLD_NIL'then r.templates=nil;r.templateLifecycle=nil
 elseif mode=='CORRUPT_TABLE'then r.templates.revision=99
 else r.templateLifecycle.state='UNKNOWN'end
 c.q.buildings[12]=true;before=encode(props);saved=true;boot();flush()
 assert(not pcall(ledger,c),mode);assert(encode(props)==before,mode..' silently rewrote history')
 assert(encode(record(other))==control and shared.EffectiveFacts.Read(0,other).specialization=='RESEARCH')
end
print('D PASS: empty vs missing/corrupt; no silent reconstruction')
-- G: unknown binding/owner, foreign events and unrelated city must not change authority.
c,token=industry();other=fresh(2);register(other);complete(other,'DISTRICT_CAMPUS')
control=encode(record(other));c.s.values.TOKEN='conflict';c.q.buildings[12]=true;before=encode(props)
Events.BuildingAddedToMap.Fire(c:GetX(),5,12,0);flush();assert(encode(props)==before and not pcall(ledger,c))
c.s.values.TOKEN=token;loss(c,token,true);before=encode(props)
Events.BuildingAddedToMap.Fire(c:GetX(),5,12,3);Events.CityTransfered.Fire(nil,nil,nil);flush()
assert(encode(props)==before and encode(record(other))==control and not pcall(ledger,c))
print('G PASS: binding/owner/foreign/other-city isolation')
-- Atomic failure: failed initial ledger write leaves pending intent, never a false initialized marker.
start();c=fresh(1);register(c)
-- First identity is persisted; delay standardization by its ready flag.
shared.Standardization.ready=false;complete(c,'DISTRICT_INDUSTRIAL_ZONE')
token=c.s.values.TOKEN;assert(record(c).templateLifecycle.state=='UNINITIALIZED')
shared.Standardization.ready=true;failKey=PREFIX..token;shared.Standardization.Discover(0)
assert(record(c).templates==nil and record(c).templateLifecycle.state=='UNINITIALIZED')
assert(not pcall(ledger,c));failKey=nil
print('WRITE FAILURE PASS: initialization and ledger cannot commit separately')
-- Actual unchanged discount consumer sees the reconciled union, then applies only
-- a fresh eligible sample. No database rates or native purchase claims in this test.
c,token=industry();loss(c,token,true);c.q.buildings[12]=true;retake(c);flush()
c.GetName=function()return 'Fixture Industry' end
local carrierRows={};local n=600
for id,row in pairs(catalogRows)do row.enabled=true;row.group=id
 for level=1,4 do n=n+1;local name='BUILDING_SPC_B054_'..id..'_'..level
  local x={Index=n,BuildingType=name};carrierRows[name]=x;carrierRows[n]=x
 end
end
local originalInfo=P.Info
P.Info=function(t,k)if t=='Buildings' and carrierRows[k]then return carrierRows[k]end;return originalInfo(t,k)end
shared.NetworkBridge={DiscountBatch=function(pid)
 return {recipients={[c:GetID()]={[c:GetID()]=true}},input={player=pid,epoch=1,inputVersion=1,validity='VALID'}}end}
SPCStandardizationDiscount.Start(P,shared);local discount=shared.StandardizationDiscount
discount.EnsureReady(0);assert(not discount.globalError,discount.globalError)
local plan=assert(discount.plans[0]);local targets=plan.targets[c:GetID()]
assert(targets.BUILDING_A==1 and targets.BUILDING_B==1 and not targets.BUILDING_C)
ExposedMembers={}
ExposedMembers.SPC_DiscountClientEpoch=1
ExposedMembers.SPC_DiscountIssued={ClientEpoch=1,Seq=1,Generation=discount.generation}
local packet={ClientEpoch=1,Seq=1,Generation=discount.generation,Revision=plan.revision,
 Turn=turn,Valid=1,Count=2,Data=c:GetID()..',11,1;'..c:GetID()..',12,1'}
discount.Receive(0,packet)
assert(discount.responses[0].Status=='ACCEPTED',discount.receiveError)
assert(c.q.buildings[carrierRows.BUILDING_SPC_B054_BUILDING_A_1.Index]
 and c.q.buildings[carrierRows.BUILDING_SPC_B054_BUILDING_B_1.Index])
local effects=discount.changes;discount.Receive(0,packet);assert(discount.changes==effects)
local savedTemplates=encode(props[PREFIX..token].templates)
c.s.ref.owner=3;c.s.ref.cityID=44;Events.CityTransfered.Fire(3,44,0)
assert(props[PREFIX..token].stage=='HELD_TRANSFER' and encode(props[PREFIX..token].templates)==savedTemplates)
for _,row in pairs(carrierRows)do assert(not c.q.buildings[row.Index])end
assert(c.q.buildings[11] and c.q.buildings[12],'ordinary buildings affected by exit')
print('CONSUMER PASS: real discount plan/sample/carriers; duplicate no effects; owned withdrawal preserves ordinary buildings/ledger')

'''
exec(compile(header+helpers+claim_setup+return_setup+extra+"\n"+chr(39)*3+")",str(R/'DevelopmentTests/test_b140_templates.py'),'exec'))
