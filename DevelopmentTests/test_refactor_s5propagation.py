"""S5a complete production dispatch boundaries: Lua51, bounded explicit publish, no game PASS."""
import unittest
from refactor_harness import Context,ROOT,TrackedLua51,legacy_source_observation,separate_legacy_event_namespaces
from refactor_defect_fixtures import commerce,fact_publication_profile


def bindings():
    c=Context();c.load('FactChanges');c.load('FactConsumerBindings');c.execute('d=SPCFactChanges.New(shared);SPCFactConsumerBindings.New(shared);calls={};function drain()d.Flush();shared.FactBindings.Flush()end')
    return c


def investment():
    source=Context();namespace={'__file__':str(ROOT/'DevelopmentTests/test_investment_update_propagation.py')}
    text=source.prefix('DevelopmentTests/test_investment_update_propagation.py','class InvestmentPropagation(')
    with legacy_source_observation():exec(compile(text,'S5a investment fixture prefix','exec'),namespace)
    namespace['NS']['LuaRuntime']=TrackedLua51;namespace['NS']['ns']['LuaRuntime']=TrackedLua51
    namespace['NS']['ns']['FIX']=separate_legacy_event_namespaces(namespace['NS']['ns']['FIX'])
    with legacy_source_observation():l=namespace['fixture'](3)
    l.execute((ROOT/'Mod/SafeCallbacks.lua').read_text());l.execute((ROOT/'Mod/FactChanges.lua').read_text());l.execute((ROOT/'Mod/FactConsumerBindings.lua').read_text())
    l.execute('SPCFactChanges.New(shared);SPCFactConsumerBindings.New(shared);function drain()shared.FactChanges.Flush();shared.FactBindings.Flush()end')
    return l


class PhaseBarrier(unittest.TestCase):
    def test_network_derived_reaches_effect_phase_once_real_reentry_waits(self):
        c=Context();c.load('FactChanges');c.execute("""
        d=SPCFactChanges.New(shared);seen={}
        d.RegisterConsumer('NetworkBridge',function(e)
         d.EmitDerived({owner=0,kinds={'NETWORK'},cause='NETWORK_PROOF_PUBLISHED',revision=1})
         d.Emit({owner=0,cityID=2,kinds={'ACTIVE'},cause='SECOND_TRUE_CHANGE'})
        end,{kinds={'ACTIVE'},phase=0})
        d.RegisterConsumer('effect',function(e)seen[#seen+1]=e end,{kinds={'NETWORK'}})
        d.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='FIRST_CHANGE'});d.Flush()
        assert(#seen==1 and seen[1].revision==1 and d.pending==1 and d.flushRevision==1)
        """)
    def test_wrong_phase_producer_cannot_forward_and_nonnetwork_rejected(self):
        c=Context();c.load('FactChanges');c.execute("""
        d=SPCFactChanges.New(shared);seen=0
        d.RegisterConsumer('other',function()d.EmitDerived({owner=0,kinds={'NETWORK'},cause='PROOF'})end,{kinds={'ACTIVE'},phase=0})
        d.RegisterConsumer('effect',function()seen=seen+1 end,{kinds={'NETWORK'}})
        d.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='INPUT'});d.Flush();assert(seen==0 and d.pending==1)
        d.Flush();assert(seen==1);assert(not pcall(d.EmitDerived,{owner=0,kinds={'ACTIVE'},cause='BAD_DERIVED'}))
        """)
    def test_all_own_syncs_precede_one_network_capture_per_owner(self):
        c=bindings();c.execute("""
        shared.Restructuring={FactChanged=function(e)calls[#calls+1]='R'..e.city end}
        shared.NetworkBridge={Refresh=function(pid)calls[#calls+1]='N'..pid;d.EmitDerived({owner=pid,kinds={'NETWORK'},cause='NETWORK_PROOF_PUBLISHED'})end}
        shared.Lv3Effects={Audit=function(s)assert(s.player==0 and s.city==nil);calls[#calls+1]='E'end}
        d.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='COMMITTED'});d.Emit({owner=0,cityID=2,kinds={'POTENTIAL'},cause='COMMITTED'})
        drain();assert(table.concat(calls,',')=='R1,R2,N0,E')
        d.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='SECOND_CHANGE'});drain();assert(calls[6]=='N0')
        """)
    def test_consumer_native_reentry_retains_new_work_without_recursive_writes(self):
        c=bindings();c.execute("""
        local once=true;shared.ResearchChair={Audit=function(s)
         calls[#calls+1]=s.city
         if once then once=false;d.Emit({owner=0,cityID=2,kinds={'ACTIVE'},cause='SECOND_CHANGE'});d.Flush();assert(not shared.FactBindings.Flush())end
        end}
        d.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='FIRST_CHANGE'});drain();assert(#calls==1);shared.FactBindings.Flush();assert(#calls==2 and calls[2]==2)
        """)


class Scopes(unittest.TestCase):
    def test_source_city_union_and_owner_dominance_remove_narrow_receipt(self):
        c=bindings();c.execute("""
        shared.StandardizationEffects={Audit=function(s)assert(s.changed[1] and s.changed[2] and not s.city);calls[#calls+1]='S'end}
        d.Emit({owner=0,cityID=1,kinds={'HISTORY'},topic='TEMPLATES',cause='COMMIT'});d.Emit({owner=0,cityID=2,kinds={'HISTORY'},topic='ENGINEERING',cause='COMMIT'});drain();assert(#calls==1)
        shared.Lv3Effects={Audit=function(s)assert(s.player==0 and s.city==nil and s.investment==nil);calls[#calls+1]='O'end}
        d.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='INVESTMENT_COMMITTED',investment={status='COMMITTED'}})
        d.Emit({owner=0,kinds={'NETWORK'},cause='NETWORK_PROOF_PUBLISHED'});drain();assert(calls[#calls]=='O')
        """)
    def test_bad_city_and_target_do_not_suppress_other_city_or_sibling(self):
        c=bindings();c.execute("""
        shared.ResearchInfrastructure={Audit=function()error('BROKEN_TARGET')end}
        shared.ResearchChair={Audit=function(s)if s.city==1 then error('BAD_CITY')end;calls[#calls+1]=s.city end}
        d.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='COMMITTED'});d.Emit({owner=0,cityID=2,kinds={'ACTIVE'},cause='COMMITTED'})
        drain();assert(#calls==1 and calls[1]==2 and shared.FactBindings.errors.ResearchChair and shared.FactBindings.errors.ResearchInfrastructure)
        local n=d.delivered;for i=1,1000 do drain()end;assert(d.delivered==n and #calls==1)
        """)
    def test_restructuring_cause_cannot_keep_pretransition_investment_fastpath(self):
        c=bindings();c.execute("shared.Lv2Housing={Audit=function(s)assert(s.city==1 and s.investment==nil);calls[#calls+1]=1 end};d.Emit({owner=0,cityID=1,reference='REF',kinds={'ACTIVE'},cause='INVESTMENT_COMMITTED',investment={status='COMMITTED'}});d.Emit({owner=0,cityID=1,reference='REF',kinds={'IDENTITY'},cause='RESTRUCTURING_COMMITTED'});drain();assert(#calls==1)")

    def test_city_only_methods_keep_narrow_scope_when_owner_rows_coalesce(self):
        c=bindings();c.execute("""
        shared.Standardization={Refresh=function(pid,id)assert(id==1);calls[#calls+1]='S'end}
        shared.DialogueProjects={Refresh=function()error('LEGACY_EFFECT_RELAY')end,RefreshAccess=function(pid,id)assert(id==1);calls[#calls+1]='P'end}
        shared.DialogueEffects={Audit=function(s)assert(s.city==nil);calls[#calls+1]='E'end}
        shared.IndustrySupport={Audit=function()error('UNRELATED_RETRY')end}
        d.Emit({owner=0,cityID=1,kinds={'IDENTITY'},cause='RESTRUCTURING_COMMITTED'})
        d.Emit({owner=0,kinds={'ACTIVE','D','WORKERS'},cause='UI_FACTS_DIRTY'});drain()
        assert(table.concat(calls,',')=='S,E,P' and not next(shared.FactBindings.errors))
        """)
    def test_actual_dialogue_access_method_has_no_embedded_effect_relay(self):
        c=Context();c.load('DialogueProjectModel');c.load('DialogueProjects')
        c.execute("""
        P={IsTestPlayer=function()return true end,Field=function(o,k)return o[k]end};shared.CityProgressionStore={RegisterExit=function()end,RegisterReturn=function()end};effects=0
        shared.DialogueEffects={Audit=function()effects=effects+1 end}
        SPCDialogueProjects.Start(P,shared);shared.DialogueProjects.RefreshAccess(0,1);assert(effects==0)
        shared.DialogueProjects.Refresh(0,1);assert(effects==1)
        """)


class ActualInvestment(unittest.TestCase):
    def test_both_entrances_defer_narrow_actual_housing_gpp_without_second_consumption(self):
        for normal in (False,True):
            l=investment();l.execute("normal="+str(normal).lower()+";t=prepare(c,301,normal);drain();resetCounts();assert(confirm(c,301,t,normal):find('INVESTED'));assert(kills==1 and ledgerWrites==3 and housing(c)==0 and gpp(c,'RESEARCH')==0);drain();assert(housing(c)==1 and gpp(c,'RESEARCH')==6 and counters.city_scan==2 and members==0);local n=ledgerWrites;confirm(c,301,t,normal);drain();assert(kills==1 and ledgerWrites==n)")
    def test_actual_sibling_survives_writer_error_and_next_explicit_recovery(self):
        l=investment();l.execute("t=prepare(c,302,false);drain();local audit=shared.Lv2Housing.Audit;shared.Lv2Housing.Audit=function()error('FAILED_HOUSING')end;confirm(c,302,t,false);drain();assert(gpp(c,'RESEARCH')==6 and kills==1 and ledgerWrites==3);shared.Lv2Housing.Audit=audit;confirm(c,302,t,false);drain();assert(housing(c)==1 and kills==1 and ledgerWrites==3)")
    def test_queued_receipt_reference_change_prevents_stale_effect_write(self):
        l=investment();l.execute("t=prepare(c,303,false);drain();confirm(c,303,t,false);c.token='REPLACED';drain();assert(housing(c)==0 and gpp(c,'RESEARCH')==0 and kills==1 and ledgerWrites==3 and shared.Lv2GPP.errors['investment:0'])")


class NetworkOutput(unittest.TestCase):
    def test_new_proof_invalidates_old_commerce_before_deferred_drain(self):
        l=commerce();l.execute('assert(toggle(2,\'DISTRICT_CAMPUS\',true))');fact_publication_profile(l,False)
        # Disarm the legacy fixture's automatic closure for this explicit boundary test.
        l.execute("fixtureDrain=true;assert(com.TransactionCurrent(0,2));local old=ownedGold(cities[2]);local revision=net.ProofRevision(0);net.CheckEvidence(true);assert(net.ProofRevision(0)>revision and not com.TransactionCurrent(0,2) and ownedGold(cities[2])==old);local n=shared.FactChanges.sequence;for i=1,20 do net.RequestPendingProof(0)end;assert(shared.FactChanges.sequence==n);shared.FactChanges.Flush();shared.FactBindings.Flush();Events.GameCoreEventPublishComplete.Fire();assert(ownedGold(cities[2])==old and not com.TransactionCurrent(0,2))")
    def test_negative_proof_survives_later_unreadable_capture_before_delivery(self):
        l=commerce();l.execute("cities[5].kind='RESEARCH';cities[5].yields.SCIENCE=80;send('0,1,0,2,10;0,5,0,2,11',2);assert(toggle(2,'DISTRICT_CAMPUS',true));cities[5].GetProperty=function()error('TEMP_REFERENCE')end;units[10]=nil;net.CheckEvidence(false);assert(ownedGold(cities[2])==12 and net.Input(0).continuityOnly)")
    def test_output_revision_and_readiness_are_scalar_only(self):
        l=commerce();l.execute("local old=Players;Players=setmetatable({},{__index=function()error('NATIVE_READ')end});assert(type(net.ProofRevision(0))=='number' and net.TransactionCurrent(0));Players=old")


if __name__=='__main__':unittest.main()
