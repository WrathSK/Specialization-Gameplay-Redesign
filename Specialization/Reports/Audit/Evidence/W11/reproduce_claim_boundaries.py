"""Audit-only actual Claim/Store composition on mocked native queues and Properties.
Reuses fixture declarations, not historical tests; no repository/runtime writes.
"""
from pathlib import Path
import argparse, hashlib, importlib.util, json
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args();root=a.repo.resolve();loader=root/'Specialization/Reports/Audit/Evidence/W03/progression_store_reproduction.py'
spec=importlib.util.spec_from_file_location('w03fixture',loader);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
conquest=m.literal(root/'DevelopmentTests/test_b111_district_snapshot.py','local function ai(c)').split('-- One candidate',1)[0]
claim=m.literal(root/'DevelopmentTests/test_b124_claim.py','local info=P.Info').split('start();local aCity=conquered',1)[0]
setup="include('ClaimProjects')\n"+conquest+claim+'''\nlocal originalBoot=boot
function boot()originalBoot();SPCClaimProjects.Start(P,shared);Events.LoadScreenClose.Fire()end
'''
FAIL=r'''
start();local c=conquered(1,'DISTRICT_CAMPUS');request(c,'RESEARCH')
local key=PREFIX..c.s.values.TOKEN;local original=Game.SetProperty;local callBefore=finishCalls
if MODE=='LATCH_WRITE_FAIL' then
 Game.SetProperty=function(o,k,v)
  if k==key and v.claimTimer and v.claimTimer.stage=='CALLING' then return end
  return original(o,k,v)
 end
elseif MODE=='FINAL_WRITE_FAIL' then
 Game.SetProperty=function(o,k,v)
  if k==key and v.claim then return end
  return original(o,k,v)
 end
end
Events.PlayerTurnDeactivated.Fire(0);turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush()
local observed=record(c);local calls=finishCalls-callBefore
if MODE=='LATCH_WRITE_FAIL' then assert(calls==0 and observed.claimTimer.stage=='ACTIVE')
elseif MODE=='FINAL_WRITE_FAIL' then assert(calls==1 and observed.claimTimer.stage=='CALLING' and not observed.claim and c.q.target=='NONE')
else assert(calls==1 and observed.claim and observed.base.specialization=='RESEARCH')end
Game.SetProperty=original;saved=true;boot();flush()
local recovered=record(c);local after=finishCalls-callBefore
if MODE=='LATCH_WRITE_FAIL' then assert(after==1 and recovered.claim)
elseif MODE=='FINAL_WRITE_FAIL' then assert(after==1 and not recovered.claim and recovered.claimTimer.stage=='CALLING')
else assert(after==1 and recovered.claim)end
local result={mode=MODE,native_calls_before_boot=calls,native_calls_after_boot=after,
 stage_after_boot=recovered.claim and 'COMPLETED' or recovered.claimTimer.stage,
 identity_after_boot=recovered.base.specialization,queue_target=c.q.target,
 duplicate_call_count=0,native_reachability='NOT_ESTABLISHED'}
local before=finishCalls;Events.PlayerTurnActivated.Fire(0);shared.ClaimProjects.Sync(0,c:GetID(),'AUDIT_SYNC');flush();assert(finishCalls==before)
if MODE=='FINAL_WRITE_FAIL' then
 -- A fresh independently validated native event remains a real recovery entry.
 Events.CityProjectCompleted.Fire(0,c:GetID(),101);flush()
 assert(record(c).claim and record(c).base.specialization=='RESEARCH' and finishCalls==before)
 result.fresh_valid_completion_event_recovers=true
end
auditResult=result
'''
LOSS=r'''
start();local c=conquered(1,'DISTRICT_CAMPUS');local token=c.s.values.TOKEN
local origin=c:GetID();request(c,'RESEARCH')
c.s.ref.owner=3;c.s.ref.cityID=44;Events.CityTransfered.Fire(3,44,0);flush()
assert(record(c).stage=='HELD_TRANSFER' and record(c).claimTimer==nil)
c.s.ref.owner=0;c.s.ref.cityID=500;Events.CityTransfered.Fire(0,500,3);flush()
assert(record(c).stage=='ACTIVE' and record(c).current.cityID==500)
request(c,'RESEARCH');assert(record(c).claimTimer.reference.cityID==500)
local callback=Events.PlayerTurnActivated.list[#Events.PlayerTurnActivated.list]
local function up(fn,name)
 for i=1,50 do local n,v=debug.getupvalue(fn,i);if not n then break end;if n==name then return v end end
 error('missing upvalue '..name)
end
local runTurn=up(callback,'turn');local active=up(runTurn,'active');assert(active['0:500'])
local originalCities=Players[0].GetCities;local lookups=0
Players[0].GetCities=function(...)
 local rows=originalCities(...);local find=rows.FindID
 rows.FindID=function(self,id)if id==500 then lookups=lookups+1 end;return find(self,id)end
 return rows
end
c.s.ref.owner=3;c.s.ref.cityID=45;Events.CityTransfered.Fire(3,45,0);flush()
assert(record(c).stage=='HELD_TRANSFER' and record(c).claimTimer==nil and not next(c.q.buildings))
assert(active['0:500'] and not active['0:'..origin])
local errors=up(shared.ClaimProjects.Flush,'safe');local errorMap=up(errors,'errors')
local before=writes;local beforeCalls=finishCalls
for i=1,3 do
 turn=turn+1;Events.PlayerTurnActivated.Fire(0)
 assert(active['0:500'] and errorMap['0:500'] and shared.ClaimProjects.views['0:500'].stage=='STOPPED')
end
assert(lookups==3 and writes==before and finishCalls==beforeCalls)
Events.CityProductionUpdated.Fire(0,500);flush();assert(active['0:500']==nil)
local afterDirty=lookups;turn=turn+1;Events.PlayerTurnActivated.Fire(0);assert(lookups==afterDirty)
auditResult={mode='RECAPTURE_SECOND_LOSS',origin_city_id=origin,prior_current_city_id=500,
 persisted_timer_after_loss='NONE',markers_after_loss=0,stale_active_entries=1,
 failed_city_lookups=3,explicit_dirty_prunes=true,post_prune_activation_lookups=0,extra_store_writes=0,extra_native_completions=0,
 limits='debug upvalues only observe session ownership; native timing/latency not measured'}
'''
result={'evidence':'LOCAL_STRUCTURAL_REPRODUCTION','scope':'Real unchanged Claim/Store; native queues/events/Properties are mocks. No gameplay regression or runtime operation.',
 'source':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ['Mod/ClaimProjects.lua','Mod/CityProgressionStore.lua','Mod/TimedProject.lua','Mod/UI/ClaimProjectUI.lua','DevelopmentTests/test_b111_district_snapshot.py','DevelopmentTests/test_b124_claim.py','Specialization/Reports/Audit/Evidence/W03/progression_store_reproduction.py']},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'cases':[m.runtime(root,setup+"local MODE='"+mode+"'\n"+FAIL) for mode in ['NORMAL','LATCH_WRITE_FAIL','FINAL_WRITE_FAIL']]}
result['loss_scope']=m.runtime(root,setup+LOSS)
a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
