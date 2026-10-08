"""Audit-only actual Store event dispatch and delayed-readable transfer fixtures.
Reuses declarations, not historical tests. Native lookup counts are not timings.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args();root=a.repo.resolve();loader=root/'Specialization/Reports/Audit/Evidence/W03/progression_store_reproduction.py'
s=importlib.util.spec_from_file_location('w03fixture',loader);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
SCALE=r'''
start();for i=1,N do local c=fresh(i);register(c)end
local calls=0;local native=CityManager.GetCityAt;local before=writes
CityManager.GetCityAt=function(...)calls=calls+1;return native(...)end
Events.CityTransfered.Fire(3,9000,4)
assert(calls==N and writes==before)
auditResult={registered_records=N,unrelated_foreign_transfer_city_lookups=calls,
 permanent_writes=0,limits='Counts native function entries only; mocked lookup implementation cost excluded.'}
'''
UNKNOWN=r'''
start();local c=fresh(1);register(c);complete(c,'DISTRICT_CAMPUS')
local native=CityManager.GetCityAt;local exits=0;local suspended=true
local function registerExit()d.RegisterExit('AuditExit',function()exits=exits+1 end)end
registerExit()
if MODE~='OLD_REFERENCE' then c.s.ref.owner=3;c.s.ref.cityID=44 end
CityManager.GetCityAt=function(...)
 if suspended and MODE=='NIL_LOOKUP' then return nil end
 if suspended and MODE=='THROW_LOOKUP' then error('AUDIT_TEMPORARY_LOOKUP_ERROR')end
 return native(...)
end
Events.CityTransfered.Fire(3,44,0)
suspended=false;c.s.ref.owner=3;c.s.ref.cityID=44
Events.CityInitialized.Fire(3,44,c:GetX(),c:GetY())
local after=record(c);assert(after.stage=='ACTIVE' and after.loss==nil and exits==0)
local ok=pcall(shared.EffectiveFacts.Read,0,c);assert(not ok)
saved=true;boot();registerExit();assert(record(c).stage=='ACTIVE' and record(c).loss==nil and exits==0)
-- A fresh repeated matching Transfer is a positive recovery control.
Events.CityTransfered.Fire(3,44,0)
assert(record(c).stage=='HELD_TRANSFER' and record(c).loss.target.owner==3 and exits==1)
auditResult={mode=MODE,stage_after_later_initialized=after.stage,saved_loss_after_initialized=false,
 current_facts_readable=false,exit_calls_before_repeat=0,load_does_not_reconstruct_loss=true,
 repeated_matching_transfer_recovers=true,exit_calls_after_repeat=exits,
 native_timing_reachability='NOT_ESTABLISHED',limits='AuditExit callback is a stub; no actual effect residual or native incident measured.'}
'''
r={'evidence':'LOCAL_STRUCTURAL_REPRODUCTION','scope':'Actual unchanged Store and named native event handlers; no native game/runtime/saves accessed.',
 'source':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ['Mod/CityProgressionStore.lua','Mod/CityIdentityRead.lua','Mod/Probe.lua','DevelopmentTests/test_p0_e1.py','DevelopmentTests/test_p0_e2.py','DevelopmentTests/test_b108_e2_multicity.py','Specialization/Reports/Audit/Evidence/W03/progression_store_reproduction.py']},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scale':[m.runtime(root,f'local N={n}\n'+SCALE) for n in [1,4,20,40]],
 'unknown':[m.runtime(root,"local MODE='"+mode+"'\n"+UNKNOWN) for mode in ['NIL_LOOKUP','THROW_LOOKUP','OLD_REFERENCE']],
 'limits':['Native events/Property/objects are explicit mocks; loops do not establish engine frequency/latency or allocation.',
 'The fixture GetCityAt internally scans mocked cities; that fixture cost is not a production complexity measurement.',
 'Delayed readable and replayed Transfer are injected; no assumption that engine delivers either sequence.']}
a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
