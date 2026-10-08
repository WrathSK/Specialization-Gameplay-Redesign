"""Audit-only actual Store/Standardization initialization with unknown presence.
Uses one controlled catalog object and existing fixtures; no game/DB/project writes.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args();root=a.repo.resolve();loader=root/'Specialization/Reports/Audit/Evidence/W03/progression_store_reproduction.py'
s=importlib.util.spec_from_file_location('w03fixture',loader);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
BODY=r'''
local restored=false;local reads=0
SPCStandardizationCatalog={Build=function()return {count=1,buildings={BUILDING_A={index=1,name='A',district='DISTRICT_CITY_CENTER',tier=0,group='CITY_CENTER',enabled=true}}}end}
P.HasBuilding=function()
 reads=reads+1
 if not restored and MODE=='NIL_PRESENCE' then return nil end
 if not restored and MODE=='THROW_PRESENCE' then error('AUDIT_PRESENCE_UNREADABLE')end
 return true
end
local oldBoot=boot
function boot()oldBoot();SPCStandardization.Start(P,shared);Events.LoadScreenClose.Fire()end
start();local c=fresh(1);c.GetBuildings=function()return {}end;register(c);complete(c,'DISTRICT_INDUSTRIAL_ZONE')
local first=record(c);local firstCount=first.templates and 0 or -1
if first.templates then for _ in pairs(first.templates.learned)do firstCount=firstCount+1 end end
local firstState=first.templateLifecycle.state;local firstPending=first.templateLifecycle.reconcilePending
if MODE=='THROW_PRESENCE' then assert(firstCount==-1 and firstState=='UNINITIALIZED' and firstPending)
elseif MODE=='NIL_PRESENCE' then assert(firstCount==0 and firstState=='INITIALIZED' and not firstPending)
else assert(firstCount==1 and firstState=='INITIALIZED' and not firstPending)end
restored=true;shared.Standardization.Discover(0)
local nextRecord=record(c);local count=0;for _ in pairs(nextRecord.templates.learned)do count=count+1 end
if MODE=='NIL_PRESENCE' then assert(count==0 and reads==1)else assert(count==1)end
local before=writes;saved=true;boot();local final=record(c);local finalCount=0
for _ in pairs(final.templates.learned)do finalCount=finalCount+1 end
assert(finalCount==count and writes==before and shared.Standardization.scans==0)
auditResult={mode=MODE,initial_ledger_count=firstCount,initial_lifecycle=firstState,
 initial_reconcile_pending=firstPending,after_readable_discover_count=count,
 coldboot_count=finalCount,coldboot_extra_writes=0,coldboot_scans=0,total_presence_reads=reads,
 native_nil_reachability='NOT_ESTABLISHED'}
'''
r={'evidence':'LOCAL_STRUCTURAL_REPRODUCTION','limits':['Actual unchanged Store/Standardization; one explicitly stubbed catalog and native presence/Property/event objects.',
 'NIL/throw are controlled faults, not observed native behavior; reliable-empty versus uninitialized tested, no whole catalog coverage.'],
 'source':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ['Mod/Standardization.lua','Mod/CityProgressionStore.lua','Mod/CityIdentityRead.lua','Specialization/Reports/Audit/Evidence/W03/progression_store_reproduction.py']},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'cases':[m.runtime(root,"local MODE='"+mode+"'\n"+BODY) for mode in ['KNOWN_TRUE','NIL_PRESENCE','THROW_PRESENCE']]}
a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
