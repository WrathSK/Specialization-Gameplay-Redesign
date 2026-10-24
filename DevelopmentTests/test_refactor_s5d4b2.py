"""Worker source normalization, actual carriers and bounded UI fallback; Lua51/local."""
import unittest
from refactor_harness import Context,ROOT,legacy_source_observation,measure
from refactor_defect_fixtures import request_context,fact_publication_profile
from test_refactor_s5propagation import investment
from test_refactor_s5d1 import research
from test_refactor_s5d4b1 import native


def ui(extra=''):
    c=Context('UI');c.execute("P={VERSION='WORKER_TEST',Field=function(t,k)return t and t[k]end,IsTestPlayer=function(pid)return pid==0 end,Observe=function()end};SPCP0=P;SPCDiagnosticLog={For=function()return function()end end};ExposedMembers.SPC_P0={Version=P.VERSION,Lv2GPP={ready=true}};PlayerOperations={EXECUTE_SCRIPT=1};sends=0;packets={};UI={RequestPlayerOperation=function(pid,op,p)sends=sends+1;packets[sends]=p;if onSend then onSend(p)end end}")
    c.globals().include=lambda name:None
    if extra:c.execute(extra)
    c.load('UI/GPPRefresh');c.execute('init()');return c


def load_request(l):
    c=Context()
    with legacy_source_observation():l.execute(c.fragment('Mod/Gameplay.lua','local function request(playerID,params)','GameEvents.SPC_P0_Request.Add')+'\n_G.rawRequest=request')
    l.execute("P.Observe=P.Observe or function()end;function drainworker()shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete')end")


def active_investment():
    l=investment();l.execute("t=prepare(c,401,false);drain();confirm(c,401,t,false);drain();assert(shared.EffectiveFacts.Read(0,c).active==2)")
    with legacy_source_observation():fact_publication_profile(l,False)
    return l


class WorkerScopes(unittest.TestCase):
    def test_known_worker_city_only_WORKERS_never_network_generation(self):
        c=native();c.execute("worker={};d.RegisterConsumer('worker',function(e)worker[#worker+1]=e end,{kinds={'WORKERS'}});Events.CityWorkerChanged.Fire(0,7);assert(d.Generation(0,'NETWORK')==0 and d.Generation(0,'COMMERCE',7)>0);d.Flush();assert(#seen==0 and #worker==1 and worker[1].city==7 and worker[1].kinds.WORKERS and not worker[1].kinds.ACTIVE and not worker[1].kinds.D)")
    def test_focus_is_owner_scope_unknown_remains_enabled_not_zero_guess(self):
        c=native();c.execute("worker={};d.RegisterConsumer('worker',function(e)worker[#worker+1]=e end,{kinds={'WORKERS'}});Events.CityFocusChanged.Fire(0,999);d.Flush();assert(#worker==1 and worker[1].city==nil);P.IsTestPlayer=function(pid)return pid==1 end;Events.CityWorkerChanged.Fire(-1,999);d.Flush();assert(#worker==2 and worker[2].player==1 and worker[2].city==nil)")
    def test_same_batch_native_and_UI_worker_input_delivers_once_per_writer(self):
        c=request_context();c.execute("P.Observe=function()end;calls=0;shared.Lv2GPP={Audit=function(s)calls=calls+1;assert(s.player==0 and s.city==nil)end};shared.NetworkBridge={Refresh=function()error('WORKERS_MUST_NOT_CAPTURE_NETWORK')end};shared.ResearchCross={Audit=function()error('WORKERS_MUST_NOT_REFRESH_CROSS')end};Events.CityWorkerChanged.Fire(0,1);runRequest(0,{Action='LV2_GPP_DIRTY',Token='WORKER_TEST',WorkerOnly=true,FactsChanged=false});assert(calls==1 and not next(shared.FactBindings.errors) and shared.FactChanges.Generation(0,'NETWORK')==0)")
    def test_UI_conservative_request_routes_real_D_owner_without_ACTIVE(self):
        c=request_context();c.execute("P.Observe=function()end;gotD=0;gotA=0;shared.FactChanges.RegisterConsumer('Dcheck',function(e)gotD=gotD+1;assert(e.causes.UI_FACTS_DIRTY)end,{kinds={'D'}});shared.FactChanges.RegisterConsumer('Acheck',function()gotA=gotA+1 end,{kinds={'ACTIVE'}});runRequest(0,{Action='LV2_GPP_DIRTY',Token='WORKER_TEST',WorkerOnly=false,FactsChanged=true});assert(gotD==1 and gotA==0 and shared.FactChanges.Generation(0,'NETWORK')==0)")
    def test_UI_D_warm_cache_really_invalidates_not_just_notifies(self):
        from test_refactor_s5c1 import depth
        c=depth();c.load('NativeFacts');c.execute("SPCNativeFacts.New(P,shared);P.Scalar=tostring;P.Observe=function()end;assert(sample(1).value.domains.DISTRICT_CAMPUS.value==1);cities[1].present[2]=true;assert(sample(1).value.domains.DISTRICT_CAMPUS.value==1)")
        c.execute(c.fragment('Mod/Gameplay.lua','local function request(playerID,params)','GameEvents.SPC_P0_Request.Add')+'\n_G.rawRequest=request')
        c.execute("rawRequest(0,{Action='LV2_GPP_DIRTY',Token='WORKER_TEST',WorkerOnly=false,FactsChanged=true});assert(sample(1).value.domains.DISTRICT_CAMPUS.value==2 and counts.dc_capture==2)")


class ActualWorkers(unittest.TestCase):
    def test_actual_GPP_same_turn_second_change_and_idle_no_repeat(self):
        l=active_investment()
        l.execute("d.workers=3;shared.Lv2GPP.Audit({player=0,city=1});assert(gpp(c,'RESEARCH')==6);function drainworker()shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete')end;d.workers=1;fire('CityWorkerChanged',0,1);assert(gpp(c,'RESEARCH')==6);drainworker();assert(gpp(c,'RESEARCH')==2);d.workers=2;fire('CityWorkerChanged',0,1);drainworker();assert(gpp(c,'RESEARCH')==4 and turn==1);local r,w=reads,writes;for i=1,1000 do drainworker()end;assert(reads==r and writes==w)")
    def test_actual_Chair_worker_scope_sibling_untouched(self):
        l=research()
        with legacy_source_observation():fact_publication_profile(l,False)
        l.execute("cities[2].GetBuildings=function()error('UNRELATED_WORKER_CITY_READ')end;cities[1].ds[1].workers=1;fire('CityWorkerChanged',0,1);shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete');assert(cc('BUILDING_LIBRARY')==1 and cc('BUILDING_LIBRARY',cities[2])==3);cities[1].ds[1].workers=2;fire('CityWorkerChanged',0,1);shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete');assert(cc('BUILDING_LIBRARY')==2 and turn==1)")
    def test_unknown_Gameplay_read_waits_later_UI_real_cause_not_time(self):
        l=active_investment()
        load_request(l)
        l.execute("d.workers=3;shared.Lv2GPP.Audit({player=0,city=1});assert(gpp(c,'RESEARCH')==6);d.workers=nil;fire('CityWorkerChanged',0,1);drainworker();assert(gpp(c,'RESEARCH')==6 and shared.Lv2GPP.errors['0:1']);d.workers=1;local r,w=reads,writes;for i=1,1000 do drainworker()end;assert(reads==r and writes==w and gpp(c,'RESEARCH')==6);rawRequest(0,{Action='LV2_GPP_DIRTY',Token='WORKER_TEST',WorkerOnly=true,FactsChanged=false});drainworker();assert(gpp(c,'RESEARCH')==2 and not shared.Lv2GPP.errors['0:1'])")
    def test_failed_D_mark_does_not_block_real_GPP_worker_recovery(self):
        l=active_investment();load_request(l)
        l.execute("d.workers=3;shared.Lv2GPP.Audit({player=0,city=1});assert(gpp(c,'RESEARCH')==6);d.workers=1;shared.DistrictCompleteness.MarkDirty=function()error('DEPTH_MARK_FAILED')end;rawRequest(0,{Action='LV2_GPP_DIRTY',Token='WORKER_TEST',WorkerOnly=false,FactsChanged=true});drainworker();assert(gpp(c,'RESEARCH')==2 and shared.ObserverErrors.UI_DEPTH_FACTS and not next(shared.FactBindings.errors))")
    def test_real_bridge_worker_only_never_captures_network(self):
        from test_refactor_s5c2 import fixture
        l=fixture();l.execute("Events.CityWorkerChanged.Fire(0,2);shared.FactChanges.Flush();shared.FactBindings.Flush();Events.GameCoreEventPublishComplete.Fire();assert(captures==0 and not next(shared.FactBindings.errors));Events.CityWorkerChanged.Fire(1,2);shared.FactChanges.Flush();shared.FactBindings.Flush();assert(captures==0)")


class UIRecovery(unittest.TestCase):
    def test_governor_removed_initial_and_workers_preserved_idle_zero(self):
        c=ui();c.execute("assert(sends==1 and packets[1].FactsChanged and not packets[1].WorkerOnly and Events.GovernorChanged.Count()==0);Events.GovernorChanged.Fire(0);Events.GovernorAssigned.Fire(0,1,0);for i=1,1000 do publish();Events.SystemUpdateUI.Fire()end;assert(sends==1);Events.CityWorkerChanged.Fire(0,1);publish();assert(sends==2 and packets[2].WorkerOnly and not packets[2].FactsChanged);for i=1,1000 do publish()end;assert(sends==2)")
        measure('S5d4b2_UI_idle',{'initial_requests':1,'governor_requests':0,'thousand_idle_extra_requests':0,'worker_requests':1})
    def test_foreign_zero_unknown_conservative_and_shutdown_hooks_removed(self):
        c=ui();c.execute("Events.CityWorkerChanged.Fire(1,2);Events.PlayerTurnActivated.Fire(1);publish();assert(sends==1);Events.CityWorkerChanged.Fire();publish();assert(sends==2 and not packets[2].WorkerOnly);shutdown();Events.CityWorkerChanged.Fire(0,1);publish();assert(sends==2 and Events.CityWorkerChanged.Count()==0)")
    def test_transport_failure_budget_is_bounded_and_new_real_cause_can_rearm(self):
        c=ui("onSend=function()error('SEND_FAILURE')end");c.execute("for i=1,1000 do publish();Events.SystemUpdateUI.Fire()end;assert(sends==3);onSend=nil;Events.CityWorkerChanged.Fire(0,1);publish();assert(sends==4);for i=1,1000 do publish()end;assert(sends==4)")
    def test_reentry_during_send_is_detached_to_next_batch(self):
        c=ui();c.execute("local once=true;onSend=function()if once then once=false;Events.CityWorkerChanged.Fire(0,1)end end;Events.CityWorkerChanged.Fire(0,1);publish();assert(sends==2);publish();assert(sends==3);publish();assert(sends==3)")

if __name__=='__main__':unittest.main()
