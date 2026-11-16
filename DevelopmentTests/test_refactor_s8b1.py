"""S8b1 redundant known-flag reconstruction; no payload reset or native replay."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s7f import actual_store
import test_refactor_s8a as before_cases

BASE='801a85a1775453bdb6a831de5279bb562c6990de'
@contextmanager
def history():
 original={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('CityProgressionStore','StoreSubrecords')}
 read,execute=Path.read_text,TrackedLua51.execute;hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in original.items()}
 def source(p,*a,**kw):return original[p]if p in original else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield


SETUP="""
ca,cb=a,b
function seed()
 local n=M.Copy(T.record(ca))
 n.dialogueKnown=true;n.dialogue={version=1,serial=1,total=15,used={ERA_ANCIENT={id=1,start=0,completed=1,x=3,gain=15,forced=false}}}
 n.engineeringKnown=true;n.engineering={version=1,serial=1,L=1,receipts={[1]={id=1,start=0,completed=1}}}
 n.commerceKnown=true;n.commerce=SPCCommerceModel.New(0);n.commerce.selected={'DISTRICT_CAMPUS'}
 n.capitalKnown=true;n.capital=SPCCapitalInvestmentModel.Encode(SPCCapitalInvestmentModel.New())
 n.developmentKnown=true;n.development=SPCDevelopmentInvestmentModel.Encode(SPCDevelopmentInvestmentModel.New())
 return n
end
function install(n)T.propsSet(T.key(ca),n);beforeWrites=T.writes();beforeRevision=n.revision;return T.encode(n)end
function payloads(n)local out={};for _,key in ipairs({'dialogue','engineering','commerce','capital','development'})do out[key]=n[key]end;return T.encode(out)end
"""
FLAGS=('dialogueKnown','engineeringKnown','commerceKnown','capitalKnown','developmentKnown')

def fixture():
 vm=actual_store();vm.execute(SETUP);return vm


class FrozenBefore(unittest.TestCase):
 def test_original_strict_pre_isolation_assertions_frozen_before_known_flag_rebuild(self):
  with history():before_cases.ActualStore().test_each_corrupt_ability_keeps_exact_existing_fail_closed_behavior_without_rewriting()
  measure('S8b1_frozen_before',{'source':BASE,'unchanged_assertions':'S8a strict corrupt-ability differential','superseded':'redundant known flags with fully valid preserved payload only'})


 def test_original_dialogue_corruption_assertions_frozen_before_redundant_flag_rebuild(self):
  import test_refactor_s7d1 as projects
  with history():projects.Retained().test_dialogue_corrupt_history_is_held_not_reinitialized()

class Rebuild(unittest.TestCase):
 def test_each_flag_rebuilt_from_preserved_complete_payload_once(self):
  for flag in FLAGS:
   for missing in ('false','nil'):
    vm=fixture();vm.execute("local n=seed();n[...]=("+missing+");install(n);local before=payloads(n);T.reload();assert(pcall(shared.CityProgressionStore.Base,0,ca));local after=T.record(ca);assert(after[...]==true and after.revision==beforeRevision+1 and payloads(after)==before and T.writes()==beforeWrites+1)",flag)
    vm.execute("local status=shared.CityProgressionStore.Status(ca);assert(status.subrecordRecovery.kind=='KNOWN_FLAGS_REBUILT'and #status.subrecordRecovery.fields==1);status.subrecordRecovery.fields[1].field='MUTATE';assert(shared.CityProgressionStore.Status(ca).subrecordRecovery.fields[1].field~='MUTATE');local writes=T.writes();T.reload();assert(T.writes()==writes and not shared.CityProgressionStore.Status(ca).subrecordRecovery)")
  measure('S8b1_known_flag_reconstruction',{'flags':5,'mismatches':['missing','false'],'payload_changes':0,'writes_each_first_load':1,'writes_each_second_load':0})
 def test_all_five_flags_merge_to_one_record_revision_and_write(self):
  vm=fixture();vm.execute("local n=seed();for _,key in ipairs({'dialogueKnown','engineeringKnown','commerceKnown','capitalKnown','developmentKnown'})do n[key]=false end;install(n);local before=payloads(n);T.reload();assert(payloads(T.record(ca))==before and T.writes()==beforeWrites+1 and T.record(ca).revision==beforeRevision+1 and #shared.CityProgressionStore.Status(ca).subrecordRecovery.fields==5)")
 def test_actual_dialogue_pending_round_is_preserved_when_known_marker_is_rebuilt(self):
  import test_refactor_s7d1 as projects
  import test_dialogue_projects as dialogue
  for phase in ('ACTIVE','CALLING'):
   with projects.profile():vm=dialogue.game()
   vm.execute("""
   begin(c);Events.PlayerTurnDeactivated.Fire(0);local r=T.record(c)
   r.dialogue.pending.stage=...;r.dialogueKnown=nil;local before=T.encode(r.dialogue)
   T.propsSet(T.key(c),r);reload();local state=shared.CityProgressionStore.DialogueState(0,c)
   assert(T.encode(state.value)==before and state.value.pending.stage==... and finishes==0)
   """,phase)
 def test_actual_dialogue_missing_payload_bad_total_and_bad_reference_still_hold(self):
  import test_refactor_s7d1 as projects
  import test_dialogue_projects as dialogue
  for mutation in ('r.dialogue=nil','r.dialogue.total=999','r.dialogue.pending.reference.cityID=999'):
   with projects.profile():vm=dialogue.game()
   vm.execute('begin(c);local r=T.record(c);'+mutation+';T.propsSet(T.key(c),r);reload();assert(not pcall(shared.CityProgressionStore.DialogueState,0,c)and not c.b.present[998]and finishes==0 and shared.EffectiveFacts.Read(0,control).potential==1)')
 def test_healthy_restore_has_no_extra_property_write(self):
  vm=fixture();vm.execute("local n=seed();install(n);T.reload();assert(T.writes()==beforeWrites and pcall(shared.CityProgressionStore.Base,0,ca)and not shared.CityProgressionStore.Status(ca).subrecordRecovery)")
 def test_missing_payload_bad_payload_other_bad_field_and_bad_base_do_not_repair(self):
  for change in ("n.dialogue=nil","n.dialogue='BROKEN'","n.researchTradition='BROKEN'","n.schema=99","n.origin.x=12345","n.templateLifecycle={version=1,state='BROKEN'}"):
   vm=fixture();vm.execute("local n=seed();n.dialogueKnown=false;"+change+";local frozen=install(n);T.reload();assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and not pcall(shared.CityProgressionStore.Base,0,ca)and pcall(shared.CityProgressionStore.Base,0,cb))")
 def test_transient_decoder_exception_does_not_write_or_poll_and_fresh_load_recovers(self):
  vm=fixture();vm.execute("""
  local n=seed();n.capitalKnown=false;local frozen=install(n);local decode=SPCCapitalInvestmentModel.Decode;calls=0
  SPCCapitalInvestmentModel.Decode=function()calls=calls+1;error('TEMPORARY_DEPENDENCY_UNAVAILABLE')end
  T.reload();assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and not pcall(shared.CityProgressionStore.Base,0,ca))
  local first=calls;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(calls==first and T.writes()==beforeWrites)
  SPCCapitalInvestmentModel.Decode=decode;T.reload();assert(pcall(shared.CityProgressionStore.Base,0,ca)and T.writes()==beforeWrites+1)
  """)
 def test_unknown_getter_copy_failure_or_changed_prewrite_never_becomes_repair_success(self):
  for mode in ('getter','copy','prewrite'):
   vm=fixture();vm.execute("local n=seed();n.dialogueKnown=false;install(n);mode=...;local key=T.key(ca);local getter=Game.GetProperty;local reads=0;Game.GetProperty=function(o,k)if k==key then reads=reads+1;if mode=='getter'then error('TEMPORARY_NATIVE_READ')elseif mode=='copy'then return {self=corrupt}elseif mode=='prewrite'and reads>1 then local v=getter(o,k);v.revision=v.revision+1;return v end end;return getter(o,k)end;corrupt={};corrupt.self=corrupt;T.reload();assert(T.writes()==beforeWrites and not pcall(shared.CityProgressionStore.Base,0,ca)and pcall(shared.CityProgressionStore.Base,0,cb)and not shared.CityProgressionStore.Status(ca).subrecordRecovery)",mode)
 def test_setter_and_readback_failures_keep_guard_without_optimistic_publication(self):
  for mode in ('drop','throw_before','throw_after','readback_throw','readback_stale'):
   vm=fixture();vm.execute("""
   local n=seed();n.dialogueKnown=false;install(n);local key=T.key(ca);local setter,getter=Game.SetProperty,Game.GetProperty
   local stale=M.Copy(n);attempts=0;afterSet=false;optimistic=false
   Game.SetProperty=function(o,k,v)
    if k~=key then return setter(o,k,v)end
    attempts=attempts+1
    if pcall(shared.CityProgressionStore.Base,0,ca)then optimistic=true end
    if mode=='drop'then return end
    if mode=='throw_before'then error('SETTER_BEFORE')end
    setter(o,k,v);afterSet=true
    if mode=='throw_after'then error('SETTER_AFTER')end
   end
   Game.GetProperty=function(o,k)
    if k==key and afterSet then
     if mode=='readback_throw'then error('READBACK_UNAVAILABLE')end
     if mode=='readback_stale'then return M.Copy(stale)end
    end
    return getter(o,k)
   end
   T.reload();assert(attempts==1 and not optimistic and not pcall(shared.CityProgressionStore.Base,0,ca)and pcall(shared.CityProgressionStore.Base,0,cb)and not shared.CityProgressionStore.Status(ca).subrecordRecovery)
   for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(attempts==1)
   Game.SetProperty=setter;Game.GetProperty=getter;local writes=T.writes();T.reload();assert(pcall(shared.CityProgressionStore.Base,0,ca))
   assert(T.writes()==writes+((mode=='drop'or mode=='throw_before')and 1 or 0))
   """.replace('local n=seed();',"mode='"+mode+"';local n=seed();",1))
 def test_unprintable_model_failure_keeps_unknown_guard_and_sibling_usable(self):
  vm=fixture();vm.execute("""
  local n=seed();n.capitalKnown=false;local frozen=install(n)
  SPCCapitalInvestmentModel.Decode=function()error(setmetatable({},{__tostring=function()error('FORMAT_FAILED')end}))end
  T.reload();assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and not pcall(shared.CityProgressionStore.Base,0,ca)and pcall(shared.CityProgressionStore.Base,0,cb))
  """)
 def test_unprintable_setter_failure_releases_existing_fact_write_barrier(self):
  vm=fixture();vm.execute("""
  local n=seed();n.dialogueKnown=false;install(n);local key=T.key(ca);local setter=Game.SetProperty;local start=SPCCityProgressionStore.Start
  begins,ends=0,0
  SPCCityProgressionStore.Start=function(P,s,legacy)
   s.EffectiveFacts={BeginWrite=function()begins=begins+1;return {}end,EndWrite=function()ends=ends+1 end}
   return start(P,s,legacy)
  end
  Game.SetProperty=function(o,k,v)if k==key then error(setmetatable({},{__tostring=function()error('FORMAT_FAILED')end}))end;return setter(o,k,v)end
  T.reload();assert(begins==1 and ends==1 and T.writes()==beforeWrites and not pcall(shared.CityProgressionStore.Base,0,ca)and pcall(shared.CityProgressionStore.Base,0,cb)and not shared.CityProgressionStore.Status(ca).subrecordRecovery)
  """)
 def test_valid_money_CALLING_contracts_are_preserved_without_settling_or_debiting(self):
  for phase in ('DEBIT_CALLING','CREDIT_CALLING'):
   vm=fixture();vm.execute("""
   local n=seed();local C,D=SPCCapitalInvestmentModel,SPCDevelopmentInvestmentModel
   local source={owner=ca:GetOwner(),cityID=ca:GetID(),x=ca:GetX(),y=ca:GetY(),token=n.base.token,changes=0}
   local target={owner=cb:GetOwner(),cityID=cb:GetID(),x=cb:GetX(),y=cb:GetY(),token=T.record(cb).base.token,changes=0}
   local q={domain='DISTRICT_CAMPUS',source=source,turn=0,due=10,principal=100,D=3,S=2,C=1,R=0,safe=130,success=150,failure=80,probability=.5,failureCount=0,balance=1000}
   local capital=C.Begin(nil,q,'STABLE',.2,'ORIGINAL_CAPITAL');local cc=capital.contracts.DISTRICT_CAMPUS;cc.stage='DEBIT_CALLING'
   if phase=='CREDIT_CALLING'then capital=C.Activate(capital,'DISTRICT_CAMPUS',900);cc=capital.contracts.DISTRICT_CAMPUS;cc.stage='CREDIT_CALLING';cc.creditBefore=200;cc.creditAfter=330 end
   n.capital=C.Encode(capital);n.capitalKnown=false
   local development=D.Begin(nil,{source=source,target=target,domain='DISTRICT_CITY_CENTER',building='BUILDING_GRANARY',price=880,cost=132,balance=1000,existing={},turn=0},'ORIGINAL_DEVELOPMENT')
   development.contracts[target.token].stage='DEBIT_CALLING';n.development=D.Encode(development);n.developmentKnown=false
   local frozen=payloads(n);install(n);moneyCalls=0;Players[0].GetTreasury=function()moneyCalls=moneyCalls+1;error('MONEY_ACCESS_FORBIDDEN')end
   T.reload();assert(pcall(shared.CityProgressionStore.Base,0,ca)and payloads(T.record(ca))==frozen and T.writes()==beforeWrites+1 and moneyCalls==0)
   assert(shared.CityProgressionStore.CapitalState(0,ca).value.contracts.DISTRICT_CAMPUS.stage==phase)
   assert(shared.CityProgressionStore.DevelopmentState(0,ca).value.contracts[target.token].stage=='DEBIT_CALLING')
   """.replace('local n=seed();',"phase='"+phase+"';local n=seed();",1))
  measure('S8b1_CALLING_preservation',{'Capital':['DEBIT_CALLING','CREDIT_CALLING'],'Development':['DEBIT_CALLING'],'same_payloads':True,'treasury_operations':0,'settlement_replay':False})

if __name__=='__main__':unittest.main()
