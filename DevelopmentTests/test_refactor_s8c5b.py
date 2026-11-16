"""Actual composite core/Store/RuntimeWork with scalar native doubles; not production wiring."""
import unittest
from refactor_harness import measure
from test_refactor_s7f import actual_store

SETUP="""
ca,cb=a,b;originA=ca:GetID();s=shared.CityProgressionStore
include('BoostConfig');include('BoostIntegerConfig');include('LegacyCleanupCatalog');include('LegacyCleanup')
groups=SPCLegacyCleanupCatalog.Build(9,SPCBoostConfig.rows,SPCBoostIntegerConfig.rows);byGroup={};byID={};definitions={};local index=0
for _,row in ipairs(groups)do byGroup[row.key]=row;if row.kind=='buildings'then for _,name in ipairs(row.names)do
 index=index+1;definitions[name]={BuildingType=name,Index=index,InternalOnly=1};byID[index]={name=name,group=row.key}
end end end
setmetatable(definitions,{__call=function(t)local k;return function()k=next(t,k);return k and t[k]end end})
GameInfo={Buildings=definitions,Eras=function()local n=0;return function()n=n+1;if n<=9 then return {EraType='ERA_'..n}end end end}
removeCalls,plotWrites,postCalls,hasReads=0,0,0,0;removeByGroup={};readByGroup={};captured={};losses={};faultGroup=nil;faultCity=nil
for _,c in ipairs({ca,cb})do
 c.present={[999999]=true};c.plotValues={SPC_B029_ONE=1,SPC_B029_HALF=1,OTHER='keep'}
 for id in pairs(byID)do c.present[id]=true end
 c.GetBuildings=function(city)return {city=city}end
end
P.HasBuilding=function(b,id)
 hasReads=hasReads+1;local row=byID[id];if row then readByGroup[row.group]=(readByGroup[row.group]or 0)+1 end
 if row and row.group==faultGroup and(not faultCity or faultCity==b.city)then return nil end
 return b.city.present[id]==true
end
P.RemoveBuilding=function(b,id)
 assert(id~=999999);local row=assert(byID[id]);removeCalls=removeCalls+1;removeByGroup[row.group]=(removeByGroup[row.group]or 0)+1
 if beforeRemove then beforeRemove(b.city,id)end
 if removeMode=='BEFORE'then error('REMOVE_UNKNOWN')end
 b.city.present[id]=nil
 if removeMode=='AFTER'then error(setmetatable({},{__tostring=function()error('FORMAT_UNKNOWN')end}))end
end
P.CreateBuilding=function()error('LEGACY_MUST_NOT_ADD')end
local set=P.SetProperty
Map.GetPlot=function(x,y)
 local city;for _,c in ipairs({ca,cb})do if c:GetX()==x and c:GetY()==y then city=c end end
 assert(city);return {GetProperty=function(_,k)return city.plotValues[k]end,SetProperty=function(_,k,value)
  assert(k=='SPC_B029_ONE'or k=='SPC_B029_HALF');city.plotValues[k]=value;plotWrites=plotWrites+1
 end}
end
P.SetProperty=function(o,k,v)return set(o,k,v)end
for owner=9,10 do Players[owner]={GetCities=function()return {FindID=function(_,id)
 for _,c in ipairs({ca,cb})do if c:GetID()==id and c:GetOwner()==owner then return c end end end,
 Members=function()return ipairs({})end}end}end
coreBeforeTurns=#Events.PlayerTurnActivated.list;coreBeforePublish=#Events.GameCoreEventPublishComplete.list
core=SPCLegacyCleanup.Start(P,shared)
assert(#Events.PlayerTurnActivated.list==coreBeforeTurns and #Events.GameCoreEventPublishComplete.list==coreBeforePublish and hasReads==0 and removeCalls==0 and plotWrites==0)
jobsA=SPCRuntimeWork.NewTargets(P,shared,function()error('POSITIVE_A_FORBIDDEN')end,function(_,_,why)reportedA=why end)
jobsB=SPCRuntimeWork.NewTargets(P,shared,function()error('POSITIVE_B_FORBIDDEN')end,function()end)
function runnerA(clean,ack)cleanA=clean;ackA=ack;return jobsA.Exit(clean,'LegacyCleanup',ack)end
function runnerB(clean,ack)cleanB=clean;ackB=ack;return jobsB.Exit(clean,'LegacyCleanup',ack)end
function post(c,loss)
 postCalls=postCalls+1;for _,name in ipairs(byGroup.Dialogue.names)do assert(not c.present[definitions[name].Index],'POST_BEFORE_PHYSICAL_CLEANUP')end
 if postFault then error('POST_UNKNOWN')end;return true
end
core.RegisterRunner('Lv3Support',runnerA);core.RegisterRunner('Lv3Effects',runnerB);core.RegisterPostCleanup('Dialogue',post)
s.RegisterExit('LegacyCleanup',function(c,loss,ticket)captured[c]=ticket;losses[c]=M.Copy(loss);return core.Exit(c,loss,ticket)end)
function lose(c,id)T.loss(c,9,id)end
function status(c)return s.Status(c or ca).exitStatus end
function retryA()jobsA.Retry({player=9,city=900})end
function retryB()jobsB.Retry({player=9,city=900})end
function countPresent(c,key)local n=0;for _,name in ipairs(byGroup[key].names)do if c.present[definitions[name].Index]then n=n+1 end end;return n end
"""
def core_fixture(extra=''):
 v=actual_store();v.execute(SETUP+extra);return v


class Composite(unittest.TestCase):
 def test_full_exact_cleanup_flags_and_unrelated_values_preserved_without_creation(self):
  v=core_fixture();v.execute("local before=T.writes();lose(ca,900);assert(T.writes()==before+1);assert(status()=='WITHDRAWN'and removeCalls==1409 and plotWrites==2 and postCalls==1);assert(ca.present[999999]and cb.present[999999]and ca.plotValues.OTHER=='keep');for id in pairs(byID)do assert(not ca.present[id]and cb.present[id])end;local reads,writes=hasReads,T.writes();s.ExitConfirmed();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(hasReads==reads and T.writes()==writes)")
  measure('S8c5b_exact_composite',{'building_removals':1409,'plot_writes':2,'ordinary_and_other_city_untouched':True,'creation':0,'idle_extra_reads_writes':0,'production_wiring':'PENDING'})
 def test_boost_directory_unknown_does_not_suppress_fixed_groups_or_flags(self):
  v=core_fixture("SPCBoostConfig.rows['RESEARCH:1:1']=nil");v.execute("lose(ca,900);assert(status()=='PARTIAL_HELD'and plotWrites==2 and postCalls==1 and countPresent(ca,'NetworkBoost')==1126 and countPresent(ca,'HalfYieldProbe')==0 and countPresent(ca,'Lv3Support')==0)")
 def test_era_directory_unknown_only_holds_Dialogue_group(self):
  v=core_fixture("GameInfo.Eras=function()error('ERA_DIRECTORY_UNKNOWN')end");v.execute("lose(ca,900);assert(status()=='PARTIAL_HELD'and countPresent(ca,'Dialogue')==12 and countPresent(ca,'NetworkBoost')==0 and countPresent(ca,'HalfYieldProbe')==0 and plotWrites==2 and postCalls==0)")
 def test_native_Buildings_unavailable_is_not_all_definitions_absent_but_flags_still_clear(self):
  for mode in ('nil','throw'):
   v=core_fixture();v.execute("if ...=='nil'then GameInfo.Buildings=nil else GameInfo=setmetatable({Eras=GameInfo.Eras},{__index=function()error('BUILDINGS_UNKNOWN')end})end;lose(ca,900);assert(status()=='PARTIAL_HELD'and removeCalls==0 and plotWrites==2)",mode)
 def test_exact_missing_definition_is_absent_but_lookup_exception_is_UNKNOWN(self):
  v=core_fixture();v.execute("local name=byGroup.PurchaseProbe.names[1];local id=definitions[name].Index;definitions[name]=nil;ca.present[id]=nil;lose(ca,900);assert(status()=='WITHDRAWN'and removeCalls==1408)")
  v=core_fixture();v.execute("local name=byGroup.PurchaseProbe.names[1];local old=definitions[name];definitions[name]=nil;getmetatable(definitions).__index=function(_,k)if k==name then error('LOOKUP_UNKNOWN')end end;lose(ca,900);assert(status()=='PARTIAL_HELD'and countPresent(ca,'NetworkBoost')==0 and not removeByGroup.PurchaseProbe);getmetatable(definitions).__index=nil;definitions[name]=old;s.ExitConfirmed();assert(status()=='WITHDRAWN')")
 def test_bad_definition_does_not_authorize_writing_and_peers_continue(self):
  for mode in ('index','internal'):
   v=core_fixture();v.execute("local r=definitions[byGroup.PurchaseProbe.names[1]];if ...=='index'then r.Index='UNKNOWN'else r.InternalOnly=0 end;lose(ca,900);assert(status()=='PARTIAL_HELD'and not removeByGroup.PurchaseProbe and countPresent(ca,'NetworkBoost')==0)",mode)
 def test_unprintable_partial_removal_recovers_by_readback_without_rewriting_deleted_rows(self):
  v=core_fixture("removeMode='AFTER'");v.execute("lose(ca,900);assert(status()=='PARTIAL_HELD'and removeCalls==10 and plotWrites==2);removeMode=nil;s.ExitConfirmed();assert(status()=='WITHDRAWN'and removeCalls==1409)")
 def test_three_Store_attempts_then_independent_two_group_recovery_requires_both(self):
  v=core_fixture();v.execute("""
  local has=P.HasBuilding;P.HasBuilding=function(b,id)local key=byID[id].group;if key=='Lv3Support'and not readyA or key=='Lv3Effects'and not readyB then return nil end;return has(b,id)end
  lose(ca,900);s.ExitConfirmed();s.ExitConfirmed();assert(status()=='PARTIAL_HELD')
  local prior=removeCalls;readyA=true;retryA();assert(status()=='PARTIAL_HELD'and removeCalls==prior+12 and not jobsA.exits['9:900']and jobsB.exits['9:900'])
  readyB=true;retryB();assert(status()=='WITHDRAWN'and removeCalls==1409 and not jobsB.exits['9:900'])
  """)
 def test_newer_pending_during_physical_cleanup_is_preserved(self):
  v=core_fixture("faultGroup='Lv3Support'");v.execute("""
  lose(ca,900);jobsA.pending['9:900']={owner=9,city=900};local old=jobsA.pending['9:900'];faultGroup=nil;local once=true
  beforeRemove=function()if once then once=false;jobsA.pending['9:900']={owner=9,city=900}end end
  retryA();assert(status()=='WITHDRAWN'and not jobsA.exits['9:900']and jobsA.pending['9:900']~=old)
  """)
 def test_group_done_progress_does_not_cross_cities(self):
  v=core_fixture("faultGroup='NetworkBoost';faultCity=ca");v.execute("lose(ca,900);lose(cb,901);assert(status(ca)=='PARTIAL_HELD'and status(cb)=='WITHDRAWN'and countPresent(ca,'NetworkBoost')==1126 and countPresent(cb,'NetworkBoost')==0);faultGroup=nil;s.ExitConfirmed();assert(status(ca)=='WITHDRAWN'and removeCalls==2818)")
 def test_post_cleanup_failure_holds_only_group_and_runs_after_physical_readback(self):
  v=core_fixture("postFault=true");v.execute("lose(ca,900);assert(status()=='PARTIAL_HELD'and removeCalls==1409 and postCalls==1);postFault=false;s.ExitConfirmed();assert(status()=='WITHDRAWN'and removeCalls==1409 and postCalls==2)")
 def test_new_loss_rechecks_all_groups_and_old_ticket_cannot_write(self):
  v=core_fixture();v.execute("""
  lose(ca,900);local first=captured[ca];local proof=M.Copy(losses[ca]);assert(status()=='WITHDRAWN')
  ca.s.ref.owner=0;ca.s.ref.cityID=originA;Events.CityTransfered.Fire(0,originA,9);assert(T.record(ca).stage=='ACTIVE')
  for id in pairs(byID)do ca.present[id]=true end;ca.plotValues.SPC_B029_ONE=1;ca.plotValues.SPC_B029_HALF=1
  faultGroup='Lv3Support';lose(ca,900);assert(not rawequal(first,captured[ca])and status()=='PARTIAL_HELD')
  local writes,reads=removeCalls,hasReads;assert(not pcall(core.Exit,ca,proof,first));assert(removeCalls==writes and hasReads==reads)
  faultGroup=nil;retryA();assert(status()=='WITHDRAWN'and removeCalls==2818 and plotWrites==4)
  """)
 def test_duplicate_unknown_registrations_fail_without_overwriting_existing_owners(self):
  v=core_fixture();v.execute("assert(not pcall(core.RegisterRunner,'Lv3Support',function()end));assert(not pcall(core.RegisterRunner,'Other',runnerA));assert(not pcall(core.RegisterPostCleanup,'Dialogue',function()end));assert(not pcall(core.RegisterPostCleanup,'Other',post));lose(ca,900);assert(status()=='WITHDRAWN')")
 def test_direct_native_reentry_cannot_repeat_sweep_or_physical_group(self):
  v=core_fixture();v.execute("""
  local has=P.HasBuilding;local once=true
  P.HasBuilding=function(b,id)if once then once=false;assert(not pcall(core.Exit,ca,losses[ca],captured[ca]))end;return has(b,id)end
  lose(ca,900);assert(status()=='WITHDRAWN'and removeCalls==1409)
  """)

 def test_non_string_successful_tostring_does_not_skip_other_groups(self):
  for mode in ('table','number','boolean'):
   v=core_fixture();v.execute("""
   local get=Map.GetPlot;mode=...
   Map.GetPlot=function(...)local plot=get(...);plot.GetProperty=function()error(setmetatable({},{__tostring=function()
    if mode=='table'then return {}elseif mode=='number'then return 17 else return false end
   end}))end;return plot end
   lose(ca,900);assert(status()=='PARTIAL_HELD'and removeCalls==1409 and plotWrites==0 and postCalls==1)
   """,mode)
 def test_missing_required_participants_hold_only_their_groups(self):
  v=core_fixture();v.execute("""
  core=SPCLegacyCleanup.Start(P,shared);lose(ca,900)
  assert(status()=='PARTIAL_HELD'and countPresent(ca,'Lv3Support')==12 and countPresent(ca,'Lv3Effects')==11 and countPresent(ca,'NetworkBoost')==0 and plotWrites==2)
  core.RegisterRunner('Lv3Support',runnerA);core.RegisterRunner('Lv3Effects',runnerB);core.RegisterPostCleanup('Dialogue',post)
  s.ExitConfirmed();assert(status()=='WITHDRAWN'and removeCalls==1409 and postCalls==1)
  """)
 def test_failed_Composition_participant_cannot_be_invoked_as_success(self):
  for kind in ('runner','post'):
   v=core_fixture();v.execute("""
   core=SPCLegacyCleanup.Start(P,shared);include('RuntimeComposition');local composition=SPCRuntimeComposition.New(shared);kind=...
   if kind=='runner'then
    assert(not composition.Run('FailedRunner',{}, {},function()core.RegisterRunner('Lv3Support',runnerA);error('START_FAILED')end))
    core.RegisterRunner('Lv3Effects',runnerB);core.RegisterPostCleanup('Dialogue',post)
   else
    core.RegisterRunner('Lv3Support',runnerA);core.RegisterRunner('Lv3Effects',runnerB)
    assert(not composition.Run('FailedPost',{}, {},function()core.RegisterPostCleanup('Dialogue',post);error('START_FAILED')end))
   end
   lose(ca,900);assert(status()=='PARTIAL_HELD'and countPresent(ca,'NetworkBoost')==0)
   if kind=='runner'then assert(countPresent(ca,'Lv3Support')==12)else assert(postCalls==0 and countPresent(ca,'Dialogue')==0)end
   """,kind)
 def test_last_group_slot_replacement_keeps_old_candidate_unconfirmed(self):
  v=core_fixture("faultGroup='Lv3Support'");v.execute("""
  lose(ca,900);faultGroup=nil;local complete=s.ExitCompleted;insideACK=false
  s.ExitCompleted=function(name,c,loss,ticket,current)
   insideACK=true;local ok,value=pcall(complete,name,c,loss,ticket,current);insideACK=false;if not ok then error(value)end;return value
  end
  local get=ca.GetOwner;local once=true
  ca.GetOwner=function(c)
   if once and insideACK then once=false;faultGroup='Lv3Support';local newer=jobsA.Exit(cleanA,'LegacyCleanup',ackA);assert(not pcall(newer,ca,losses[ca],captured[ca]))end
   return get(c)
  end
  retryA();assert(status()=='PARTIAL_HELD'and jobsA.exits['9:900'])
  faultGroup=nil;retryA();assert(status()=='WITHDRAWN'and not jobsA.exits['9:900'])
  """)
 def test_newer_success_cannot_be_erased_by_old_failed_completion(self):
  v=core_fixture("faultGroup='Lv3Support'");v.execute("""
  lose(ca,900);faultGroup=nil;local complete=s.ExitCompleted;insideACK=false
  s.ExitCompleted=function(name,c,loss,ticket,current)
   insideACK=true;local ok,value=pcall(complete,name,c,loss,ticket,current);insideACK=false;if not ok then error(value)end;return value
  end
  local get=ca.GetOwner;local once=true
  ca.GetOwner=function(c)
   if once and insideACK then once=false;local newer=jobsA.Exit(cleanA,'LegacyCleanup',ackA);assert(pcall(newer,ca,losses[ca],captured[ca]))end
   return get(c)
  end
  retryA();assert(status()=='WITHDRAWN'and not jobsA.exits['9:900']);local before=removeCalls
  assert(core.Exit(ca,losses[ca],captured[ca])and removeCalls==before)
  """)
 def test_aggregate_ACK_rechecks_other_groups_not_just_last_slot(self):
  v=core_fixture("faultGroup='Lv3Support'");v.execute("""
  lose(ca,900);faultGroup=nil;local complete=s.ExitCompleted;insideACK=false
  s.ExitCompleted=function(name,c,loss,ticket,current)
   insideACK=true;local ok,value=pcall(complete,name,c,loss,ticket,current);insideACK=false;if not ok then error(value)end;return value
  end
  local get=ca.GetOwner;local once=true
  ca.GetOwner=function(c)
   if once and insideACK then once=false;faultGroup='Lv3Effects';local newer=jobsB.Exit(cleanB,'LegacyCleanup',ackB);assert(not pcall(newer,ca,losses[ca],captured[ca]))end
   return get(c)
  end
  retryA();assert(status()=='PARTIAL_HELD'and jobsA.exits['9:900']and jobsB.exits['9:900'])
  faultGroup=nil;retryB();assert(status()=='PARTIAL_HELD');retryA();assert(status()=='WITHDRAWN')
  """)
 def test_original_pending_cleared_but_known_and_transfers_not_deleted(self):
  v=core_fixture("faultGroup='Lv3Support'");v.execute("""
  lose(ca,900);jobsA.pending['9:900']={owner=9,city=900};jobsA.known['9:900']={keep=true};jobsA.transfers.sentinel={owner=10,city=777,oldOwner=0}
  faultGroup=nil;retryA();assert(status()=='WITHDRAWN'and not jobsA.pending['9:900']and jobsA.known['9:900'].keep and jobsA.transfers.sentinel)
  """)
 def test_explicit_group_physical_function_receives_ticket_and_current_slot(self):
  v=core_fixture("faultGroup='Lv3Support'");v.execute("""
  lose(ca,900);local e=jobsA.exits['9:900'];local clean=e.fn;physicalArgs=0
  e.fn=function(c,loss,ticket,current)physicalArgs=physicalArgs+1;assert(rawequal(ticket,captured[ca])and current());return clean(c,loss,ticket,current)end
  faultGroup=nil;retryA();assert(status()=='WITHDRAWN'and physicalArgs==1)
  """)

 def test_empty_or_unreadable_native_directory_is_not_individual_absence(self):
  for mode in ('empty','throw'):
   v=core_fixture();v.execute("""
   mode=...;GameInfo.Buildings=setmetatable({},{__call=function()
    if mode=='throw'then error('DIRECTORY_UNKNOWN')end;return function()return nil end
   end})
   lose(ca,900);assert(status()=='PARTIAL_HELD'and removeCalls==0 and plotWrites==2)
   """,mode)
 def test_async_non_string_error_format_is_not_retained_as_object(self):
  v=core_fixture("faultGroup='Lv3Support'");v.execute("""
  lose(ca,900);local has=P.HasBuilding;faultGroup=nil
  P.HasBuilding=function(b,id)if byID[id].group=='Lv3Support'then error(setmetatable({native=ca},{__tostring=function()return {}end}))end;return has(b,id)end
  retryA();assert(type(reportedA)=='string'and jobsA.exits['9:900']and status()=='PARTIAL_HELD')
  """)

 def test_native_read_creating_same_content_new_loss_cannot_continue_old_physical_write(self):
  v=core_fixture("faultGroup='Lv3Support'");v.execute("""
  lose(ca,900);local first=captured[ca];local oldLoss=M.Copy(losses[ca]);local removed=removeCalls
  local has=P.HasBuilding;local once=true
  P.HasBuilding=function(b,id)
   if once and byID[id].group=='Lv3Support'then
    once=false;assert(s.ExitCompleted('LegacyCleanup',ca,oldLoss,first))
    ca.s.ref.owner=0;ca.s.ref.cityID=originA;Events.CityTransfered.Fire(0,originA,9);assert(T.record(ca).stage=='ACTIVE')
    lose(ca,900);assert(T.record(ca).ownerChanges==2 and not rawequal(captured[ca],first))
   end
   return has(b,id)
  end
  retryA();assert(status()=='PARTIAL_HELD'and removeCalls==removed and jobsA.exits['9:900'])
  assert(not s.IsExitCurrent('LegacyCleanup',ca,oldLoss,first))
  faultGroup=nil;retryA();assert(status()=='WITHDRAWN'and removeCalls==1409)
  """)
 def test_completed_old_ticket_is_not_retained_by_weak_ledger_value(self):
  v=core_fixture();v.execute("""
  lose(ca,900);assert(status()=='WITHDRAWN');local weak=setmetatable({captured[ca]},{__mode='v'})
  ca.s.ref.owner=0;ca.s.ref.cityID=originA;Events.CityTransfered.Fire(0,originA,9);assert(T.record(ca).stage=='ACTIVE')
  lose(ca,900);assert(status()=='WITHDRAWN')
  collectgarbage('collect');assert(weak[1]==nil) -- isolated Lua test, no runtime GC policy/call introduced
  """)

 def test_ordinary_exit_physical_function_keeps_original_two_arguments(self):
  v=core_fixture();v.execute("""
  local targets=SPCRuntimeWork.NewTargets(P,shared,function()end,function()end)
  local fn=targets.Exit(function(...)ordinaryArgs=select('#',...);return true end,'Plain')
  s.RegisterExit('Plain',fn);lose(ca,900);assert(status()=='WITHDRAWN'and ordinaryArgs==2)
  """)

if __name__=='__main__':unittest.main()
