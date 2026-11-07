"""PU03 actual delivery owners; pure/engine-shaped Lua51 doubles, never native PASS."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import os
import subprocess
import unittest
from unittest.mock import patch

from refactor_harness import Context, ROOT, TrackedLua51, legacy_source_observation, measure, executed
from refactor_defect_fixtures import commerce

BASE = '3ab601da26d81d005a21c23f8a8e277f08d048da'
SCOPE = ('FactChanges', 'FactConsumerBindings', 'NetworkBridge', 'Commerce')


@contextmanager
def source_profile():
    if os.environ.get('SPC_PU03_BASELINE') != BASE:
        yield
        return
    original = {ROOT/'Mod'/(n+'.lua'): subprocess.check_output(
        ['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT).decode() for n in SCOPE}
    read = Path.read_text
    with patch.object(Path,'read_text',lambda p,*a,**k:original[p] if p in original else read(p,*a,**k)):
        yield


def registry():
    with source_profile():
        c = Context('PU03 registry');c.load('FactChanges')
        c.execute('''
          fc=SPCFactChanges.New(shared);calls={}
          function emit(id,kind,rev,reference)
           return fc.Emit({owner=0,cityID=id,reference=reference,kinds={kind or 'NETWORK'},cause='RELATED_FACT',revision=rev})
          end
          function receipt(e,status)
           if fc.Receipt then return fc.Receipt(e,status or 'REGISTERED')end
           return {status=status or 'REGISTERED',epoch=0,ticket=e.sequence}
          end
          function wake(name,cause,rev,scope)
           if fc.WakeConsumer then return fc.WakeConsumer(name,cause,rev,scope)end
           return false
          end
        ''')
        return c


def pipeline():
    with source_profile(),legacy_source_observation():
        l=commerce()
        l.execute('''
          fixtureDrain=true;fc=shared.FactChanges;bindings=shared.FactBindings
          -- This fixture explicitly proves its supported/foreign player identities.
          local supported=P.IsTestPlayer
          P.IsTestPlayer=function(pid)
           local allowed=supported(pid)
           return allowed,nil,allowed and 'ELIGIBLE'or 'INELIGIBLE'
          end
          -- The isolated proof fixture has no investor. The actual investment
          -- owners and their missing/failed receipt cases run in the O2 suite.
          local function outside(e)return fc.Receipt(e,'IRRELEVANT','FIXTURE_OUTSIDE_SCOPE')end
          shared.CapitalInvestment={AcceptFact=outside,Mark=function()end}
          shared.DevelopmentInvestment={AcceptFact=outside,SourceChanged=function()end}
          function drain()fc.Flush();bindings.Flush();Events.GameCoreEventPublishComplete.Fire()end
          function proof()
           shared.RouteSignalRevision=(shared.RouteSignalRevision or 0)+1
           local b=net.players[0]
           net.Receive(0,{Epoch=net.epoch,Seq=b.seq+1,Turn=turn,Signal=shared.RouteSignalRevision,
            Valid=1,Count=3,Data='0,4,0,2,10;0,2,0,1,11;0,2,0,5,12'})
          end
          function wakeOwner(revision,scope)
           if bindings.Wake then return bindings.Wake('Commerce','OWNER_READY',revision or 1,scope)end
           return false
          end
          net.RefreshFacts(0);drain()
        ''')
        return l


class Registry(unittest.TestCase):
    def test_false_nil_throw_and_missing_receipt_keep_scope_without_idle_retry(self):
        for body in ('return false','return nil',"error('OWNER_BUSY')",'return {}'):
            with self.subTest(body=body):
                c=registry();c.execute("fc.RegisterConsumer('Owner',function(e)calls[#calls+1]=e;"+body+" end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'});emit(1);fc.Flush();assert(fc.retained==1,'FALSE_DELIVERY_WAS_DROPPED');local n=fc.delivered;for i=1,30 do fc.Flush()end;assert(fc.delivered==n and #calls==1 and fc.errors.Owner)")

    def test_named_wake_recovers_same_ticket_once_and_successful_sibling_stays_idle(self):
        c=registry();c.execute('''
          ready=false;good,bad=0,0
          fc.RegisterConsumer('Good',function(e)good=good+1;return receipt(e)end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
          fc.RegisterConsumer('Bad',function(e)bad=bad+1;if ready then return receipt(e)end end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
          emit(1);fc.Flush();assert(fc.retained==1 and good==1 and bad==1)
          ready=true;wake('Bad','OWNER_READY',1,{player=0,city=1});fc.Flush()
          assert(fc.retained==0 and good==1 and bad==2,'READY_SCOPE_DID_NOT_RECOVER')
          for i=1,20 do wake('Bad','OWNER_READY',1);fc.Flush()end;assert(good==1 and bad==2)
        ''')

    def test_duplicate_wake_revision_does_not_repeat_failed_attempt(self):
        c=registry();c.execute("fc.RegisterConsumer('Owner',function()calls[#calls+1]=true;return false end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'});emit(1);fc.Flush();wake('Owner','READY',1);fc.Flush();for i=1,30 do wake('Owner','READY',1);fc.Flush()end;assert(#calls==2 and fc.retained==1);wake('Owner','READY',2);fc.Flush();assert(#calls==3)")

    def test_two_scopes_recovery_is_local_and_success_does_not_hide_failure(self):
        c=registry();c.execute('''
          ready={};fc.RegisterConsumer('Owner',function(e)calls[e.city]=(calls[e.city]or 0)+1;if ready[e.city]then return receipt(e)end end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
          emit(1);emit(2);fc.Flush();ready[1]=true;wake('Owner','READY',1,{player=0,city=1});fc.Flush()
          assert(calls[1]==2 and calls[2]==1 and fc.retained==1 and fc.errors.Owner)
          ready[2]=true;wake('Owner','READY',1,{player=0,city=2});fc.Flush();assert(calls[1]==2 and calls[2]==2 and fc.retained==0 and not fc.errors.Owner)
        ''')

    def test_replayed_ack_for_newer_change_cannot_clear_it(self):
        c=registry();c.execute("old=nil;fc.RegisterConsumer('Owner',function(e)if not old then old=receipt(e);return false end;return old end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'});emit(1,nil,1);fc.Flush();emit(1,nil,2);fc.Flush();assert(fc.retained==1 and fc.errors.Owner,'OLD_ACK_CLEARED_NEW_CHANGE')")

    def test_reentrant_new_change_survives_old_valid_ack_and_uses_next_snapshot(self):
        c=registry();c.execute('''
          fc.RegisterConsumer('Owner',function(e)calls[#calls+1]=e.sequence;if #calls==1 then emit(1,nil,2);assert(not fc.Flush())end;return receipt(e)end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
          emit(1,nil,1);fc.Flush();assert(#calls==1 and fc.retained==1 and fc.pending==1)
          fc.Flush();assert(#calls==2 and calls[1]~=calls[2] and fc.retained==0 and fc.pending==0)
        ''')

    def test_retained_kinds_and_topics_merge_without_reusing_an_old_revision(self):
        c=registry();c.execute('''
          ready=false;fc.RegisterConsumer('Owner',function(e)
           if ready then assert(e.kinds.NETWORK and e.kinds.ACTIVE and e.causes.RELATED_FACT);return receipt(e)end
          end,{kinds={'NETWORK','ACTIVE'},delivery='RESPONSIBILITY'})
          emit(1,'NETWORK',1);fc.Flush();ready=true;emit(1,'ACTIVE',2);fc.Flush();assert(fc.retained==0)
        ''')

    def test_capacity_reservation_is_atomic_and_existing_scope_can_be_updated(self):
        c=registry();c.execute('''
          fc.RegisterConsumer('Owner',function()return false end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
          for i=1,2047 do emit(i)end;assert(fc.retained==2047);emit(2048);assert(fc.retained==2048)
          local seq=fc.sequence;assert(not pcall(emit,2049) and fc.sequence==seq and fc.pending==2048 and fc.retained==2048)
          emit(1,nil,2);assert(fc.retained==2048 and fc.pending==2048);fc.Flush();assert(fc.retained==2048)
          fc.Close();assert(fc.retained==0 and fc.retryReady==0 and fc.pending==0)
        ''')
        measure('PU03_delivery_capacity',{'limit':2048,'tested':[2047,2048,2049],'silent_truncation':False})

    def test_phase0_derived_and_unrelated_next_snapshot_do_not_consume_each_other(self):
        c=registry();c.execute("""
          fc.RegisterConsumer('RestructuringSync',function()calls[#calls+1]='SYNC'end,{kinds={'ACTIVE'},phase=0})
          fc.RegisterConsumer('NetworkBridge',function()
           assert(calls[1]=='SYNC')
           fc.Emit({owner=0,cityID=1,kinds={'NETWORK'},cause='NEXT_SNAPSHOT'})
           fc.EmitDerived({owner=0,cityID=1,kinds={'NETWORK'},cause='CURRENT_PROOF'})
          end,{kinds={'ACTIVE'},phase=0})
          seen={};fc.RegisterConsumer('Owner',function(e)seen[#seen+1]=e;return receipt(e)end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
          emit(1,'ACTIVE');fc.Flush()
          assert(#seen==1 and seen[1].causes.CURRENT_PROOF and not seen[1].causes.NEXT_SNAPSHOT,'DERIVED_WINDOW_LEAKED_NEXT_CHANGE')
          assert(fc.pending==1 and fc.retained==1,'DERIVED_ACK_ERASED_NEXT_CHANGE')
          fc.Flush();assert(#seen==2 and seen[2].causes.NEXT_SNAPSHOT and fc.retained==0)
        """)

    def test_late_consumer_registration_reserves_existing_queued_scopes(self):
        c=registry();c.execute("emit(1);fc.RegisterConsumer('Owner',function(e)return receipt(e)end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'});assert(fc.retained==1);fc.Flush();assert(fc.retained==0)")

    def test_failed_phase0_cannot_be_replaced_by_an_ordinary_ticket_mode(self):
        c=registry();c.execute("assert(not pcall(fc.RegisterConsumer,'QueuedPhase0',function()return true end,{phase=0,kinds={'ACTIVE'},delivery='RESPONSIBILITY'}))")

    def test_new_delivery_subscription_is_not_half_registered_during_active_flush(self):
        c=registry();c.execute("fc.RegisterConsumer('Registrar',function()assert(not pcall(fc.RegisterConsumer,'Late',function(e)return receipt(e)end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'}))end,{kinds={'NETWORK'}});emit(1);fc.Flush();assert(fc.retained==0);fc.RegisterConsumer('Late',function(e)return receipt(e)end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'});emit(2);fc.Flush();assert(fc.retained==0)")

    def test_legacy_callbacks_keep_existing_nonreceipt_contract(self):
        c=registry();c.execute("fc.RegisterConsumer('Legacy',function()calls[#calls+1]=true end,{kinds={'NETWORK'}});emit(1);fc.Flush();assert(#calls==1 and fc.pending==0 and fc.retained==0)")

    def test_receipts_cannot_be_replayed_across_close_and_new_context(self):
        c=registry();c.execute('''
          local old
          fc.RegisterConsumer('Owner',function(e)old=receipt(e);return old end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
          emit(1);fc.Flush();local epoch=fc.epoch;local prior=fc;fc=SPCFactChanges.New(shared)
          fc.RegisterConsumer('Owner',function()return old end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
          emit(1);fc.Flush();assert(fc.epoch~=epoch and prior.closed and prior.retained==0 and fc.retained==1)
        ''')

    def test_old_reference_is_not_silently_forgotten_and_only_matching_wake_retries(self):
        c=registry();c.execute("fc.RegisterConsumer('Owner',function(e)calls[#calls+1]=e.reference;return false end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'});emit(1,nil,1,'OLD');fc.Flush();emit(1,nil,2,'NEW');fc.Flush();assert(fc.retained==2);wake('Owner','READY',1,{player=0,city=1,reference='NEW'});fc.Flush();assert(#calls==3 and calls[3]=='NEW' and fc.retained==2)")

    def test_native_reply_metatable_is_rejected_without_reading_it(self):
        c=registry();c.execute("reads=0;fc.RegisterConsumer('Owner',function()return setmetatable({},{__index=function()reads=reads+1;error('NATIVE_READ')end})end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'});emit(1);fc.Flush();assert(fc.retained==1 and reads==0)")


class ActualChain(unittest.TestCase):
    def test_bridge_failed_emit_retains_producer_intent_until_meaningful_resample(self):
        l=pipeline();l.execute('''
          local emit=fc.EmitDerived;local tries=0;fc.EmitDerived=function()tries=tries+1;error('QUEUE_UNAVAILABLE')end
          proof();local b=net.players[0];local pending=net.ProofRevision(0)
          assert(b.consumerError,'BRIDGE_FAILURE_NOT_VISIBLE')
          local n=tries;for i=1,20 do Events.GameCoreEventPublishComplete.Fire();fc.Flush()end;assert(tries==n)
          fc.EmitDerived=emit;net.RefreshFacts(0);drain()
          assert(not b.consumerError and not b.notificationIntent and net.ProofRevision(0)==pending,'SAME_PROOF_DID_NOT_RECOVER')
        ''')

    def test_bridge_silent_nil_or_false_emit_is_not_a_registered_delivery(self):
        for value in ('nil','false'):
            with self.subTest(value=value):
                l=pipeline();l.execute("local emit=fc.EmitDerived;fc.EmitDerived=function()return "+value+" end;proof();assert(net.players[0].notificationIntent and net.players[0].consumerError,'SILENT_EMIT_ACKED');fc.EmitDerived=emit;net.RefreshFacts(0);drain();assert(not net.players[0].notificationIntent and not net.players[0].consumerError)")

    def test_bridge_apply_then_throw_does_not_lose_intent_or_repeat_effect_writes(self):
        l=pipeline();l.execute("""
          local emit=fc.EmitDerived
          fc.EmitDerived=function(e)emit(e);error('AFTER_REGISTERING_SCOPE')end
          proof();local rev=net.ProofRevision(0);assert(net.players[0].notificationIntent and fc.retained==3)
          drain();local writes=com.writes;assert(fc.retained==0)
          fc.EmitDerived=emit;net.RefreshFacts(0);drain()
          assert(not net.players[0].notificationIntent and net.ProofRevision(0)==rev and com.writes==writes and fc.retained==0)
        """)

    def test_real_commerce_false_and_throw_do_not_consume_and_same_value_wake_recovers(self):
        for body in ('return false',"error('REGISTRATION_UNAVAILABLE')"):
            with self.subTest(body=body):
                l=pipeline();l.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));local mark=com.Mark;com.Mark=function()"+body+" end;proof();drain();assert(fc.retained==1 and bindings.errors.Commerce,'OWNER_SCOPE_WAS_DROPPED');local writes=com.writes;for i=1,20 do drain()end;assert(com.writes==writes and fc.retained==1);com.Mark=mark;wakeOwner(1,{player=0});drain();assert(fc.retained==0 and not bindings.errors.Commerce and com.TransactionCurrent(0,2))")

    def test_missing_failed_and_skipped_target_do_not_wake_successful_sibling_again(self):
        for state in ('MISSING','FAILED','SKIPPED_DEPENDENCY'):
            with self.subTest(state=state):
                l=pipeline();l.globals().failureState=state;l.execute('''
                  sibling=0;fc.RegisterConsumer('Sibling',function(e)sibling=sibling+1;return fc.Receipt(e,'REGISTERED')end,{kinds={'NETWORK'},delivery='RESPONSIBILITY'})
                  local owner=shared.Commerce;shared.StartStatus=shared.StartStatus or {}
                  if failureState=='MISSING'then shared.Commerce=nil else shared.StartStatus.Commerce={state=failureState}end
                  proof();drain();assert(fc.retained==1 and sibling==1 and bindings.errors.Commerce,'MISSING_OWNER_ACKED')
                  shared.Commerce=owner;shared.StartStatus.Commerce={state='OK'};wakeOwner(1,{player=0});drain()
                  assert(fc.retained==0 and sibling==1 and not bindings.errors.Commerce)
                ''')

    def test_actual_owner_failed_flush_retains_accepted_work_without_idle_retry(self):
        l=pipeline();l.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));assert(ownedGold(cities[2])==15)
          cities[1].yields.SCIENCE=200
          local phase=shared.EffectiveFacts.WithPhase;local attempts=0
          shared.EffectiveFacts.WithPhase=function(label,fn)
           if label=='COMMERCE_INPUTS'then attempts=attempts+1;error('READ_PHASE_UNAVAILABLE')end
           if phase then return phase(label,fn)else return fn()end
          end
          proof();drain();assert(com.error and ownedGold(cities[2])==15)
          local n=attempts;for i=1,20 do drain()end;assert(attempts==n,'OWNER_IDLE_RETRY')
          shared.EffectiveFacts.WithPhase=phase
          com.Mark(0,3);Events.GameCoreEventPublishComplete.Fire()
          assert(ownedGold(cities[2])==30,'ACCEPTED_OWNER_SCOPE_WAS_LOST')
        ''')

    def test_real_same_value_proof_and_second_same_turn_change_reach_owner_once_each(self):
        l=pipeline();l.execute('''
          assert(toggle(2,'DISTRICT_CAMPUS',true));local writes=com.writes;local input=net.Input(0).inputVersion
          proof();assert(not com.TransactionCurrent(0,2));drain()
          assert(com.TransactionCurrent(0,2) and net.Input(0).inputVersion==input and com.writes==writes and fc.retained==0)
          cities[1].yields.SCIENCE=200;proof();drain();assert(ownedGold(cities[2])==30 and fc.retained==0 and turn==1)
          local n=fc.delivered;for i=1,20 do drain()end;assert(fc.delivered==n)
        ''')

    def test_foreign_owner_notification_has_no_local_native_reads_or_effects(self):
        l=pipeline();l.execute('''
          nativeReads={};local writes=com.writes
          fc.Emit({owner=1,kinds={'NETWORK'},cause='FOREIGN_CONFIRMED'});drain()
          assert(not next(nativeReads) and com.writes==writes and fc.retained==0)
        ''')

    def test_reentrant_new_proof_cannot_be_erased_by_older_owner_receipt(self):
        l=pipeline();l.execute('''
          local take=com.AcceptFact;local once=true;local calls=0
          com.AcceptFact=function(e)calls=calls+1;local receipt=take(e);if once then once=false;proof()end;return receipt end
          -- The newer proof still owns Commerce plus both investment deliveries.
          proof();fc.Flush();bindings.Flush();assert(calls==1 and fc.retained==3)
          drain();assert(calls==2 and fc.retained==0)
        ''')

    def test_first_owner_ready_transition_is_an_explicit_named_wake(self):
        # Real initializer in a fresh owned Commerce instance; registry callback
        # is already installed and receives the owner-ready completion notice.
        l=pipeline();l.execute('''
          local old=shared.Commerce;shared.Commerce=nil;proof();drain();assert(fc.retained==1)
          exits.Commerce=nil;returns.Commerce=nil
          SPCCommerce.Start(P,shared);com=shared.Commerce
          assert(not com.ready);com.Audit();assert(com.ready and fc.retryReady==1)
          drain();assert(fc.retained==0 and not bindings.errors.Commerce)
        ''')

    def test_started_owner_can_register_before_ready_and_initialize_on_its_existing_drain(self):
        l=pipeline();l.execute("""
          exits.Commerce=nil;returns.Commerce=nil;SPCCommerce.Start(P,shared);com=shared.Commerce
          assert(not com.ready);nativeReads={};proof();fc.Flush();bindings.Flush()
          assert(fc.retained==0 and not com.ready and not next(nativeReads))
          Events.GameCoreEventPublishComplete.Fire();assert(com.ready and com.TransactionCurrent(0,2))
        """)

    def test_owner_busy_registers_scope_without_inline_native_work(self):
        l=pipeline();l.execute("""
          assert(toggle(2,'DISTRICT_CAMPUS',true));cities[1].yields.SCIENCE=200
          local get=cities[1].GetYield;local injected=false
          cities[1].GetYield=function(self,y)
           if not injected then
            injected=true;assert(com.busy==true);proof()
            local n=0;for _,count in pairs(nativeReads)do n=n+count end;local writes=com.writes
            fc.Flush();bindings.Flush()
            local after=0;for _,count in pairs(nativeReads)do after=after+count end
            assert(after==n and com.writes==writes and fc.retained==0)
           end
           return get(self,y)
          end
          com.Refresh(0,2);assert(injected and ownedGold(cities[2])==15)
          Events.GameCoreEventPublishComplete.Fire();assert(ownedGold(cities[2])==30 and com.TransactionCurrent(0,2))
        """)

    def test_invalid_or_old_context_receipt_cannot_register_owner_work(self):
        l=pipeline();l.execute("local mark=com.Mark;local calls=0;com.Mark=function(...)calls=calls+1;return mark(...)end;assert(not pcall(com.AcceptFact,{player=0,delivery={epoch=fc.epoch-1,consumer='NET_Binding_Commerce',ticket=1}}));assert(calls==0)")


class ReadAndOrder(unittest.TestCase):
    def test_actual_bridge_runs_after_sync_before_owner_receipt(self):
        l=pipeline();l.execute("""
          order={};shared.Restructuring={FactChanged=function()order[#order+1]='SYNC'end}
          local capture=SPCNetworkInput.Capture
          SPCNetworkInput.Capture=function(...)order[#order+1]='BRIDGE';return capture(...)end
          local take=com.AcceptFact
          com.AcceptFact=function(e)order[#order+1]='OWNER';return take(e)end
          fc.Emit({owner=0,cityID=2,kinds={'ACTIVE'},cause='ROLE_FACT_CONFIRMED'})
          fc.Flush();assert(order[1]=='SYNC' and order[2]=='BRIDGE' and order[3]=='OWNER' and fc.retained==0)
        """)

    def test_actual_gameplay_sealed_drain_uses_and_releases_real_fact_phase(self):
        from test_pu01_fact_use import fixture
        with legacy_source_observation():
            l=fixture()
            for name in ('RuntimeComposition','FactConsumerBindings'):
                l.execute((ROOT/'Mod'/(name+'.lua')).read_text())
            l.execute('composition=SPCRuntimeComposition.New(shared)')
            source=(ROOT/'Mod/Gameplay.lua').read_text()
            a=source.index("composition.Run('FactChanges',{}, {'FactChanges'},function()")
            b=source.index("composition.Run('CityProgressionStore'",a)
            executed('Mod/Gameplay.lua:fact_propagation_start',sha256(source.encode()).hexdigest(),'source_fragment',start=a,end=b)
            l.execute(source[a:b])
            l.execute("""
              local list=hooks.GameCoreEventPublishComplete;drain=list[#list]
              fc=shared.FactChanges;SPCFactConsumerBindings.New(shared)
              shared.NetworkBridge.RefreshFacts=function()end
              readers=0;fc.RegisterConsumer('PhaseReader',function(e)
               readers=readers+1;f.Read(0,c);audit();audit()
              end,{kinds={'ACTIVE'}})
              fc.Emit({owner=0,cityID=c.id,kinds={'ACTIVE'},cause='READ_PHASE_TEST'})
              local n=workerReads;drain();assert(readers==0 and fc.pending==1 and workerReads==n)
              composition.Complete();drain();assert(readers==1 and workerReads==n+1,'PHASE_COUNTS:'..readers..':'..workerReads..':'..n..':'..tostring(shared.FactPropagationError))
              audit();assert(workerReads==n+2) -- prior phase is released,not a global cache
            """)


class _TransportView:
    def __init__(self,lua):self.lua=lua
    def __getattr__(self,name):return getattr(self.lua,name)
    def execute(self,source,*args,**kwargs):
        # One frozen transport test installs a Mark-only wake counter. Supply
        # its current typed takeover contract and a bounded test-only queue.
        # Every original proof,replay,write and transport assertion is unchanged.
        old="shared.Commerce={Mark=function(pid)assert(pid==0);wakes=wakes+1 end}"
        if old in source:
            assert source.count(old)==1
            extra=""";shared.Commerce.AcceptFact=function(e)
              registeredScopes=registeredScopes or {};registeredScopes[e.player]={city=e.city,ticket=e.delivery.ticket}
              shared.Commerce.Mark(e.player);return shared.FactChanges.Receipt(e,'REGISTERED')end"""
            source=source.replace(old,old+extra,1)
        return self.lua.execute(source,*args,**kwargs)


class ExistingTransport(unittest.TestCase):
    def test_original_signal_catchup_assertions_with_current_mock_contract(self):
        import test_b397_network_transport as frozen
        original=frozen.pipeline
        with patch.object(frozen,'pipeline',lambda **kw:_TransportView(original(**kw))):
            frozen.SignalCatchUp.test_same_content_signal_only_event_reconfirms_and_wakes_real_bindings(self)


class Restricted(unittest.TestCase):
    def test_actual_chain_without_standard_io_and_observers(self):
        l=pipeline();l.execute('''
          io=nil;os=nil;debug=nil;package=nil;require=nil;dofile=nil;loadfile=nil;collectgarbage=nil
          SPCExpeditionTrainingDiagnostics.ENABLED=false
          proof();drain();assert(fc.retained==0 and net.TransactionCurrent(0))
        ''')


if __name__=='__main__':unittest.main()
