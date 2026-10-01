"""B142 scoped Tier 0 regression using the real read-only HD catalog and actual Lua handlers.
Requires Lupa and SPC_DEBUG_GAMEPLAY_DB (or local/config.json). SQL rowid is a
fixture index, not evidence about native GameInfo indexing. No engine PASS.
"""
from pathlib import Path
import json
import sqlite3
from project_paths import external_database

R = Path(__file__).resolve().parents[1]
source = (R / 'DevelopmentTests/test_b140_templates.py').read_text()
fixture = {'__file__': str(R / 'DevelopmentTests/test_b140_templates.py')}
exec(source[:source.rindex('exec(compile')], fixture)
with sqlite3.connect(external_database(R).as_uri() + '?mode=ro', uri=True) as db:
    db.row_factory = sqlite3.Row
    tiers = [dict(row) for row in db.execute('SELECT * FROM HD_BuildingTiers')]
    buildings = [dict(row) for row in db.execute(
        'SELECT rowid AS "Index", BuildingType, Name, PrereqDistrict, InternalOnly, IsWonder, PurchaseYield FROM Buildings')]
    dummy = [dict(row) for row in db.execute('SELECT BuildingType FROM HD_DUMMY_BUILDINGS')]

def lua(value):
    if value is None:
        return 'nil'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return '{' + ','.join(lua(item) for item in value) + '}'
    return '{' + ','.join('[' + lua(key) + ']=' + lua(item) for key, item in value.items()) + '}'

header = fixture['header'].replace(
    "'StandardizationDiscount','Standardization'",
    "'StandardizationCatalog','StandardizationDiscount','Standardization'")
setup = 'local dbTiers=' + lua(tiers) + '\nlocal dbBuildings=' + lua(buildings) + '\nlocal dbDummy=' + lua(dummy) + '\n'
cases = r'''
local dbRows={};for _,row in ipairs(dbBuildings)do dbRows[row.BuildingType]=row;dbRows[row.Index]=row end
local nativeInfo=P.Info
P.Info=function(t,k)if t=='Buildings' and dbRows[k]then return dbRows[k]end;return nativeInfo(t,k)end
local function iterator(rows)return function()local i=0;return function()i=i+1;return rows[i]end end end
local originalBoot=boot
function boot()
 originalBoot();GameInfo.HD_BuildingTiers=iterator(dbTiers);GameInfo.HD_DUMMY_BUILDINGS=iterator(dbDummy)
 SPCStandardization.Start(P,shared);Events.LoadScreenClose.Fire()
end
local function add(c,id)c.q.buildings[assert(dbRows[id]).Index]=true end
local function ledger(c)return shared.Standardization.ReadLedger(0,c)end
local function claimIndustry(c)Events.CityProjectCompleted.Fire(0,c:GetID(),103);flush()end
local function preview(r,t)
 return M.Preview({ref=r.origin,ledger=r.binding,values={TOKEN=r.base.token,JOURNAL=r.base,
 FLOW={schema=1,owner=r.base.owner,cityID=r.base.cityID,x=r.base.x,y=r.base.y,token=r.base.token,revision=1,stage='DONE',facts=r.base,target=r.base},TEMPLATES=t}})
end
-- A/F: continue an already-claimed UNINITIALIZED record; no reconquest/reclaim needed.
start();local c=conquered(1,'DISTRICT_INDUSTRIAL_ZONE');c.GetName=function()return 'Tier 0 fixture'end
local cat=SPCStandardizationCatalog.Build(P)
assert(cat.buildings.BUILDING_GRANARY.tier==0 and cat.buildings.BUILDING_GRANARY.enabled)
assert(cat.buildings.BUILDING_FAIR.tier==1 and cat.buildings.BUILDING_FAIR.enabled)
add(c,'BUILDING_GRANARY');add(c,'BUILDING_FAIR')
shared.Standardization.ready=false;claimIndustry(c)
assert(record(c).base.specialization=='INDUSTRY' and record(c).templateLifecycle.state=='UNINITIALIZED')
invest(c,1421);local receipt=encode(record(c).investment);local base=encode(record(c).base)
saved=true;boot();flush();local r=record(c);local d=shared.Standardization
assert(r.templateLifecycle.state=='INITIALIZED' and not r.templateLifecycle.reconcilePending)
assert(ledger(c).learned.BUILDING_GRANARY.tier==0 and ledger(c).learned.BUILDING_FAIR.tier==1)
assert(d.scans==1 and d.writes==1 and not d.errors['0:'..c:GetID()])
assert(encode(r.base)==base and encode(r.investment)==receipt)
assert(preview(r,r.templates).state=='LOCAL_CANDIDATE')
local snap=encode(props);local n=writes;boot();flush()
assert(encode(props)==snap and writes==n and shared.Standardization.scans==0)
print('A/F PASS: real HD Granary T0 + Fair T1; pending Claim continuation, atomic initialized ledger, settled cold load and receipts')
-- Direct first Claim and normal first district completion accept the same valid T0.
start();c=conquered(1,'DISTRICT_INDUSTRIAL_ZONE');add(c,'BUILDING_GRANARY');add(c,'BUILDING_FAIR');claimIndustry(c)
assert(ledger(c).learned.BUILDING_GRANARY and ledger(c).learned.BUILDING_FAIR)
start();c=fresh(1);register(c);add(c,'BUILDING_GRANARY');complete(c,'DISTRICT_INDUSTRIAL_ZONE');flush()
assert(ledger(c).learned.BUILDING_GRANARY.tier==0)
print('FIRST IDENTITY PASS: Claim and ordinary first-completion paths')
-- B/C/F: reliable Fair history remains after removal; foreign Granary enters union.
start();c=conquered(1,'DISTRICT_INDUSTRIAL_ZONE');add(c,'BUILDING_FAIR');claimIndustry(c)
local token=c.s.values.TOKEN;invest(c,1422);receipt=encode(record(c).investment)
local other=fresh(2);register(other);complete(other,'DISTRICT_CAMPUS');invest(other,1423)
local control=encode(record(other));loss(c,token,true)
c.q.buildings[dbRows.BUILDING_FAIR.Index]=nil;add(c,'BUILDING_GRANARY');retake(c)
assert(props[PREFIX..token].templateLifecycle.reconcilePending and not pcall(ledger,c))
saved=true;boot();flush()
assert(ledger(c).learned.BUILDING_FAIR and ledger(c).learned.BUILDING_GRANARY.tier==0)
assert(encode(props[PREFIX..token].investment)==receipt and encode(record(other))==control)
print('B/C/F PASS: history union with foreign-present T0, no reverse deletion, pending cold load and other-city isolation')
-- E: duplicates / read-only diagnostic do not write; genuine same-turn event still learns.
local function quiet()
 local before=encode(props);local w=writes;local scans=shared.Standardization.scans
 Events.CityTransfered.Fire(0,c:GetID(),3)
 for _=1,3 do
  Events.CityProjectCompleted.Fire(0,c:GetID(),103);flush();Events.PlayerTurnActivated.Fire(0)
  Events.BuildingAddedToMap.Fire(c:GetX(),5,dbRows.BUILDING_GRANARY.Index,0);flush()
 end
 c.GetName=function()return 'Tier 0 fixture'end
 local text=shared.Standardization.Describe(0,c,1);assert(text:find('T0') and text:find('状态=正常'))
 assert(encode(props)==before and writes==w and shared.Standardization.scans==scans)
end
quiet();add(c,'BUILDING_WATER_MILL')
assert(cat.buildings.BUILDING_WATER_MILL.tier==0)
Events.BuildingAddedToMap.Fire(c:GetX(),5,dbRows.BUILDING_WATER_MILL.Index,0);flush()
assert(ledger(c).learned.BUILDING_WATER_MILL.tier==0);quiet()
snap=encode(props);n=writes;saved=true;boot();flush();assert(encode(props)==snap and writes==n)
print('E PASS: duplicate notifications and diagnostics are write-free; real same-turn T0 addition preserved')
-- Structural validation remains strict; accepting zero does not relax the catalog match.
r=props[PREFIX..token]
for _,badTier in ipairs({-1,0.5,1000000000})do
 local bad=M.Copy(r.templates);bad.learned.BUILDING_GRANARY.tier=badTier
 assert(preview(r,bad).reason=='TEMPLATES')
end
local bad=M.Copy(r.templates);bad.learned.BUILDING_GRANARY.tier=1
local ok,why=pcall(shared.Standardization.ValidateRetained,c,bad)
assert(not ok and tostring(why):find('STD_CATALOG_MIGRATION_REQUIRED'))
-- D/G: missing/corrupt established history is never reinitialized from current sources.
for _,mode in ipairs({'MISSING','OLD_NIL','NEGATIVE','FRACTIONAL','REVISION'})do
 start();c=conquered(1,'DISTRICT_INDUSTRIAL_ZONE');add(c,'BUILDING_GRANARY');claimIndustry(c)
 r=record(c)
 if mode=='MISSING'then r.templates=nil
 elseif mode=='OLD_NIL'then r.templates=nil;r.templateLifecycle=nil
 elseif mode=='NEGATIVE'then r.templates.learned.BUILDING_GRANARY.tier=-1
 elseif mode=='FRACTIONAL'then r.templates.learned.BUILDING_GRANARY.tier=0.5
 else r.templates.revision=99 end
 add(c,'BUILDING_FAIR');snap=encode(props);saved=true;boot();flush()
 assert(not pcall(ledger,c),mode);assert(encode(props)==snap,mode..' silently rebuilt damaged history')
end
print('D PASS: invalid tiers/revision and missing history stay protected; no fake initialization')
-- G: UNKNOWN binding / foreign current owner are not granted writes by zero acceptance.
start();c=conquered(1,'DISTRICT_INDUSTRIAL_ZONE');add(c,'BUILDING_GRANARY');claimIndustry(c)
token=c.s.values.TOKEN;c.s.values.TOKEN='conflict';add(c,'BUILDING_FAIR');snap=encode(props)
Events.BuildingAddedToMap.Fire(c:GetX(),5,dbRows.BUILDING_FAIR.Index,0);flush()
assert(encode(props)==snap and not pcall(ledger,c));c.s.values.TOKEN=token
loss(c,token,true);snap=encode(props)
Events.BuildingAddedToMap.Fire(c:GetX(),5,dbRows.BUILDING_FAIR.Index,3);flush()
assert(encode(props)==snap and not pcall(ledger,c))
print('G PASS: UNKNOWN and foreign-owner guards unchanged')
-- Error reporting preserves Store failure, including write-path and read-path diagnostics.
start();c=conquered(1,'DISTRICT_INDUSTRIAL_ZONE');add(c,'BUILDING_GRANARY')
shared.Standardization.ready=false;claimIndustry(c);shared.Standardization.ready=true
local store=shared.CityProgressionStore;local rawWrite=store.WriteTemplates
store.WriteTemplates=function()error('STORE_RECORD_INVALID')end
snap=encode(props);shared.Standardization.Discover(0)
assert(encode(props)==snap and record(c).templateLifecycle.state=='UNINITIALIZED')
assert(shared.Standardization.errors['0:'..c:GetID()]=='STORE_RECORD_INVALID')
c.GetName=function()return 'Tier 0 fixture'end
assert(shared.Standardization.Describe(0,c,1):find('状态=STORE_RECORD_INVALID'))
local rawRead=store.ReadTemplates;store.ReadTemplates=function()error('STORE_READ_UNCONFIRMED')end
assert(shared.Standardization.Describe(0,c,1):find('STORE_READ_UNCONFIRMED'))
store.ReadTemplates=rawRead;store.WriteTemplates=rawWrite
shared.Standardization.Discover(0);assert(ledger(c).learned.BUILDING_GRANARY and not shared.Standardization.errors['0:'..c:GetID()])
print('REPORT PASS: actual store error survives guard and Describe; failed write leaves pending, successful retry clears error')
-- Actual unchanged discount consumer reads the real Tier 0 CENTER_BASIC template.
-- Qualification/native purchase is mocked here; this is not engine/effect PASS.
shared.NetworkBridge={DiscountBatch=function(pid)
 return {recipients={[c:GetID()]={[c:GetID()]=true}},input={player=pid,epoch=1,inputVersion=1,validity='VALID'}}end}
SPCStandardizationDiscount.Start(P,shared);local discount=shared.StandardizationDiscount
discount.EnsureReady(0);assert(not discount.globalError,discount.globalError)
local plan=assert(discount.plans[0]);local targets=assert(plan.targets[c:GetID()])
assert(targets.BUILDING_GRANARY==1)
local parts={};for id,level in pairs(targets)do
 assert(level==1);parts[#parts+1]=c:GetID()..','..assert(dbRows[id]).Index..',1'
end;table.sort(parts)
ExposedMembers={SPC_DiscountClientEpoch=1,SPC_DiscountIssued={ClientEpoch=1,Seq=1,Generation=discount.generation}}
local packet={ClientEpoch=1,Seq=1,Generation=discount.generation,Revision=plan.revision,
 Turn=turn,Valid=1,Count=#parts,Data=table.concat(parts,';')}
discount.Receive(0,packet);assert(discount.responses[0].Status=='ACCEPTED')
assert(c.q.buildings[assert(dbRows.BUILDING_SPC_B054_BUILDING_GRANARY_1).Index])
local changed=discount.changes;discount.Receive(0,packet);assert(discount.changes==changed)
print('T0 CONSUMER PASS: real catalog/group/carrier lookup + unchanged discount plan and sample; duplicate no effect')
print('B142 LOCAL_SIMULATION_PASS: actual catalog + Store + Standardization + Claim; native confirmation still required')
'''
exec(compile(header + fixture['helpers'] + fixture['claim_setup'] + fixture['return_setup'] + setup + cases
             + "\n" + chr(39)*3 + ")", str(__file__), 'exec'))
