"""Audit-only investment recovery composition using actual unchanged Lua modules.
Reuse W03 fixture loader; no old test cases, game, DB, runtime or repository writes.
Requires the existing lupa.lua55 environment. Native objects/events are mocks.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args();root=a.repo.resolve()
loader=root/'Specialization/Reports/Audit/Evidence/W03/progression_store_reproduction.py'
spec=importlib.util.spec_from_file_location('audit_w03_fixture',loader)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
BODY=r'''
start();local c=fresh(1);register(c);complete(c,'DISTRICT_CAMPUS')
local other=fresh(2);register(other);local control=encode(record(other))
local key=PREFIX..c.s.values.TOKEN
local original=Game.SetProperty;local offset
if MODE=='INTENT' then offset=2 elseif MODE=='CONSUMED_CONFIRMED' then offset=3 end
if offset then
 local stop=(perKey[key]or 0)+offset
 Game.SetProperty=function(o,k,v)
  if k==key and (perKey[k]or 0)+1==stop then failKey=k end
  return original(o,k,v)
 end
end
addunit(999,c);assert(a.Prepare(0,c,999,'AUDIT',false):find('PREPARED'))
local request=shared.InvestmentPreview.token;local result=a.Confirm(0,c,request)
if offset then assert(result:find('HELD'))else assert(result:find('INVESTED'))end
Game.SetProperty=original;failKey=nil
local persisted=record(c);local debit=kills
assert(debit==1 and not units[999])
if MODE=='CONSUMED_CONFIRMED' then assert(persisted.investment.pending.stage==MODE)
elseif MODE=='INTENT' then assert(persisted.investment.pending.stage==MODE)
else assert(persisted.investment.pending==nil)end
-- Simulate the foreign-owner native state at the next initialization. This is
-- an explicit enclosing-state fixture, not proof of native transfer timing.
c.s.ref.owner=3;c.s.ref.cityID=45
Players[0].GetCities=function()
 local owned={};for _,v in ipairs(cities)do if v:GetOwner()==0 then owned[#owned+1]=v end end
 return {Members=function()return ipairs(owned)end,FindID=function(_,id)return CityManager.GetCity(0,id)end,GetCapitalCity=function()return other end}
end
saved=true;boot();d.RegisterExit('AuditNoEffects',function()end)
Events.CityTransfered.Fire(3,45,0);d.ExitConfirmed()
assert(record(c).stage=='HELD_TRANSFER')
local afterLoss=record(c).investment.pending and record(c).investment.pending.stage or 'NONE'
-- Original binding deliberately retained: no invented token or city matching.
c.s.ref.owner=0;c.s.ref.cityID=500
Events.CityTransfered.Fire(0,500,3)
local first=record(c);local revision=first.revision;local report=d.Describe(0,c);local repeatWrites=writes
Events.CityTransfered.Fire(0,500,3);assert(record(c).revision==revision and writes==repeatWrites)
local readable,f=pcall(shared.EffectiveFacts.Read,0,c)
if MODE=='COMPLETED' then assert(first.stage=='ACTIVE' and readable and f.potential==2)
else assert(first.stage=='HELD_TRANSFER' and not readable and report:find('RETURN_PENDING_INVESTMENT'))end
local beforeLoad=encode(record(c));local loadWrites=writes;boot()
assert(kills==debit and writes==loadWrites and encode(record(c))==beforeLoad and encode(record(other))==control)
auditResult={mode=MODE,unit_debits=debit,pending_after_loss=afterLoss,
 stage_after_return=first.stage,return_rejection=report:match('RETURN_PENDING_INVESTMENT'),
 effective_readable=readable,potential=readable and f.potential or 'HELD_NOT_ZERO',
 repeated_return_no_write=true,coldload_no_additional_debit=true,other_record_unchanged=true,
 native_interleaving_reachability='NOT_ESTABLISHED'}
'''
result={'evidence':'LOCAL_STRUCTURAL_REPRODUCTION',
 'scope':'Actual InvestmentAction/EffectiveFacts/Store with borrowed mocked native fixture. Only repository reads and explicit JSON output.',
 'limits':['Loss after a persisted confirmed pending is injected as enclosing state after a failed final write; native timing is not established.',
 'Foreign-owner native enumeration excludes the city; original binding remains, so no guessed identity or copied token.',
 'AuditNoEffects is an exit stub; no real effect withdrawal or user-game save/load, engine atomicity or current incident claim.'],
 'source':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in [
 'Mod/InvestmentAction.lua','Mod/EffectiveFacts.lua','Mod/CityProgressionStore.lua',
 'Mod/CityIdentityRead.lua','Mod/Probe.lua','Mod/UnitActions.lua',
 'DevelopmentTests/test_p0_e1.py','DevelopmentTests/test_p0_e2.py',
 'DevelopmentTests/test_b108_e2_multicity.py',
 'Specialization/Reports/Audit/Evidence/W03/progression_store_reproduction.py']},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'cases':[m.runtime(root,"local MODE='"+mode+"'\n"+BODY) for mode in ['COMPLETED','INTENT','CONSUMED_CONFIRMED']]}
a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result['cases'],ensure_ascii=False,indent=2))
