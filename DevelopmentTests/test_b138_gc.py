"""B138 bounded actual GC coordinator/dispatch/UI tests with mocked native APIs.
Requires Python 3 and Lupa lua55. No native game, external DB, deployment,
Property writes, historical wrapper or stress suite. Use --repo while in /tmp.
"""
from pathlib import Path
import argparse
import re
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime


def runtime(repo, setup='', start=True):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
      turn=40;localID=4;human=true;heap=200*1024;gcCalls=0;countCalls=0;statusCalls=0
      cpu=10;wall=1000;cpuStep=0.25;wallStep=0;clockCalls=0;timeCalls=0
      gcRunning=true;logs={};modes={};propertyWrites=0
      print=function(s)logs[#logs+1]=tostring(s)end
      function event()
        local e={fs={}};e.Add=function(f)e.fs[#e.fs+1]=f end
        e.Fire=function(...)for _,f in ipairs(e.fs)do f(...)end end;return e
      end
      Events={LoadScreenClose=event(),PlayerTurnActivated=event(),PlayerTurnDeactivated=event(),
        GameCoreEventPublishComplete=event(),CityTransfered=event()}
      GameEvents={SPC_P0_Request=event()}
      Game={GetCurrentGameTurn=function()return turn end,GetLocalPlayer=function()return localID end}
      ExposedMembers={SPC_Performance={inflight=0}}
      P={VERSION='B138_TEST',IsTestPlayer=function(pid)return human and pid==4 end,
        Field=function(o,k)return o and o[k]end,Scalar=tostring,
        SetProperty=function()propertyWrites=propertyWrites+1;error('PROPERTY_WRITE_FORBIDDEN')end}
      SPCP0=P;include=function()end
      shared={NetworkBridge={ready=true,players={}},savedAuthority={identity='RESEARCH',potential=3,receipts=2}}
      function gcMock(mode)
        modes[#modes+1]=mode
        if mode=='count' then
          countCalls=countCalls+1
          if countUnavailable or countCalls==failCountAt or (postCountUnavailable and gcCalls>0)then error('COUNT_UNAVAILABLE')end
          if countInvalid then return -1 end
          return heap
        end
        if mode=='isrunning' then statusCalls=statusCalls+1;if statusUnavailable then error('UNSUPPORTED')end;return gcRunning end
        assert(mode=='collect','GC_STRATEGY_CHANGE_FORBIDDEN')
        gcCalls=gcCalls+1
        if duringCollect then local fn=duringCollect;duringCollect=nil;fn()end
        if collectError then error(collectError)end
        heap=afterHeap or 100*1024
        if runningAfter~=nil then gcRunning=runningAfter end
        return 0
      end
      collectgarbage=gcMock
      os={clock=function()
        clockCalls=clockCalls+1;if clockUnavailable or (clockFailAfter and clockCalls>1)then error('CPU_UNAVAILABLE')end
        cpu=cpu+cpuStep;return cpu
      end,time=function()
        timeCalls=timeCalls+1;if timeUnavailable or (timeFailAfter and timeCalls>1)then error('TIME_UNAVAILABLE')end
        wall=wall+wallStep;return wall
      end}
      function loadGame()Events.LoadScreenClose.Fire()end
      function activate(pid)Events.PlayerTurnActivated.Fire(pid)end
      function publish()Events.GameCoreEventPublishComplete.Fire()end
      function cycle(t,mib,pid)turn=t;if mib then heap=mib*1024 end;activate(pid or 4);publish()end
      function intact()
        assert(propertyWrites==0 and shared.savedAuthority.identity=='RESEARCH'
          and shared.savedAuthority.potential==3 and shared.savedAuthority.receipts==2)
        for _,mode in ipairs(modes)do assert(mode=='count' or mode=='isrunning' or mode=='collect')end
      end
    ''')
    lua.execute((repo / 'Mod/PerformanceCounters.lua').read_text())
    lua.execute('ExposedMembers.SPC_Performance=SPCPerformance.New()')
    if setup:
        lua.execute(setup)
    if start:
        lua.execute('SPCPerformance.StartMemory(P,shared);d=shared.MemoryObservation;a=d.AutoGC')
    return lua


def behavior(repo):
    lua=runtime(repo)
    lua.execute('''
      assert(gcCalls==0 and countCalls==0 and a.enabled and #a.rows==0)
      d.ReadGC(4);assert(gcCalls==0 and countCalls==0)
      loadGame();assert(gcCalls==0 and countCalls==1 and a.reason:find('LOAD_BASELINE',1,true))
      loadGame();assert(gcCalls==0 and countCalls==1)
      cycle(41,400);assert(gcCalls==0 and a.reason=='INTERVAL')
      cycle(42,327.99);assert(gcCalls==0 and a.reason=='BELOW_THRESHOLD')
      cycle(43,328);assert(gcCalls==1 and a.collections==1 and a.rows[1].before==328 and a.rows[1].after==100)
      local n=countCalls;activate(4);publish();publish();assert(gcCalls==1 and countCalls==n)
      cycle(44,500);assert(gcCalls==1 and a.reason=='INTERVAL')
      cycle(45,228);assert(gcCalls==2 and #a.rows==2)
      local n=countCalls;d.ReadGC(4);assert(gcCalls==2 and countCalls==n)
      -- The separate count observer remains read-only; it does not collect.
      d.Read(4,true);d.Read(4,false);assert(gcCalls==2)
      intact()
    ''')
    # No eligible local-human turn, pending turn abandonment, and stale callbacks.
    lua=runtime(repo)
    lua.execute('''
      loadGame();turn=42;heap=500*1024
      activate(0);publish();activate(7);publish();assert(gcCalls==0)
      human=false;activate(4);publish();human=true;assert(gcCalls==0)
      activate(4);activate(7);publish();assert(gcCalls==0)
      activate(4);Events.PlayerTurnDeactivated.Fire(4);publish();assert(gcCalls==0)
      activate(4);turn=43;publish();assert(gcCalls==0)
      activate(4);localID=7;publish();localID=4;assert(gcCalls==0)
      cycle(44,500);assert(gcCalls==1)
      local old=d;SPCPerformance.StartMemory(P,shared);d=shared.MemoryObservation;a=d.AutoGC
      assert(old.ReadGC(4):find('仅本地',1,true));old.CollectGC(4,'stale');old.SetAutoGC(4,false,'stale-switch')
      loadGame();assert(gcCalls==1 and a.collections==0 and a.enabled and #a.rows==0)
      cycle(46,628);assert(gcCalls==2 and a.collections==1)
      intact()
    ''')
    lua=runtime(repo)
    lua.execute('''
      loadGame();Game.GetLocalPlayer=nil
      assert(d.ReadGC(4):find('仅本地',1,true))
      d.SetAutoGC(4,false,'no-local');d.CollectGC(4,'no-local')
      cycle(42,500);assert(gcCalls==0 and not a.failure and a.enabled);intact()
    ''')
    lua=runtime(repo)
    lua.execute('''
      loadGame();turn=42;heap=400*1024
      activate(4);d.SetAutoGC(4,false,'off');publish();assert(gcCalls==0 and not a.enabled)
      d.SetAutoGC(4,true,'off');assert(not a.enabled) -- duplicate switch token
      d.SetAutoGC(7,true,'foreign');d.SetAutoGC(4,1,'bad');d.SetAutoGC(4,true,'');assert(not a.enabled)
      d.SetAutoGC(4,true,'on');assert(a.enabled and gcCalls==0);publish();assert(gcCalls==0)
      duringCollect=function()activate(4);publish();d.CollectGC(4,'nested');publish()end
      cycle(43,400);assert(gcCalls==1 and a.collections==1)
      activate(4);publish();assert(gcCalls==1)
      -- Retained explicit API shares one primitive and cooldown/token guard.
      d.CollectGC(4,'early');assert(gcCalls==1)
      turn=45;d.CollectGC(4,'manual');assert(gcCalls==2 and a.rows[#a.rows].reason=='MANUAL')
      turn=47;d.CollectGC(4,'manual');assert(gcCalls==2)
      intact()
    ''')
    print('PASS GC lifecycle: load/read/count-observer zero full GC; local player4, 128MiB/2T, AI/duplicate/stale/reentry/switch/cooldown')


def safety_gates(repo):
    cases=[
      ('shared.RequestDepth=1', 'shared.RequestDepth=0', 'REQUEST_INFLIGHT'),
      ('shared.NetworkIsolation={active=true}', 'shared.NetworkIsolation.active=false', 'NETWORK_ISOLATED'),
      ('claimBusy=true;shared.ClaimProjects={IsBusy=function()return claimBusy end}', 'claimBusy=false', 'CLAIM_BUSY'),
      ('shared.NetworkBridge=nil', 'shared.NetworkBridge={ready=true,players={}}', 'NETWORK_NOT_READY'),
      ('shared.NetworkBridge.ready=false', 'shared.NetworkBridge.ready=true', 'NETWORK_NOT_READY'),
      ('shared.NetworkBridge.players[4]={refreshing=true}', 'shared.NetworkBridge.players[4].refreshing=false', 'NETWORK_REFRESHING'),
      ('ExposedMembers.SPC_Performance.inflight=1', 'ExposedMembers.SPC_Performance.inflight=0', 'NETWORK_INFLIGHT'),
      ('shared.TestModule={busy=true}', 'shared.TestModule.busy=false', 'MODULE_BUSY:TestModule'),
      ('ExposedMembers.SPC_P0_BackgroundRoutes={awaitingNetwork=true}', 'ExposedMembers.SPC_P0_BackgroundRoutes.awaitingNetwork=false', 'ROUTES_PENDING'),
    ]
    for key in ['SPC_CopyBackground','SPC_IndustryBackground','SPC_ResearchCrossBackground','SPC_DiscountEligibility']:
        for pending in ['1','true']:
            cases.append((f'ExposedMembers.{key}={{pending={pending}}}', f'ExposedMembers.{key}.pending=0', f'UI_PENDING:{key}'))
    for setup,clear,reason in cases:
        lua=runtime(repo)
        lua.execute('loadGame();'+setup+';cycle(42,500)')
        assert lua.eval('gcCalls')==0 and lua.eval('a.reason')=='SKIP:'+reason,(setup,lua.eval('a.reason'))
        lua.execute(clear+''';local n=countCalls;activate(4);publish();assert(gcCalls==0 and countCalls==n)
          cycle(43,500);assert(gcCalls==1);intact()''')
    print(f'PASS automatic GC safe-boundary gates: {len(cases)} busy/isolation/network/UI-pending cases; no same-turn retry')


def failure_latches(repo):
    cases=[
      ('collectgarbage=nil', '', 'LOAD_COUNT_UNAVAILABLE',0),
      ('countInvalid=true', '', 'LOAD_COUNT_UNAVAILABLE',0),
      ('', 'countUnavailable=true', 'COUNT_UNAVAILABLE',0),
      ('', 'failCountAt=3', 'COUNT_UNAVAILABLE',0),
      ('', 'gcRunning=false', 'ENGINE_GC_STOPPED',0),
      ('', 'os=nil', 'CPU_CLOCK_UNAVAILABLE',0),
      ('', 'clockUnavailable=true', 'CPU_CLOCK_UNAVAILABLE',0),
      ('', 'collectError=string.rep("x",200)', 'COLLECT_FAILED:',1),
      ('', 'postCountUnavailable=true', 'POST_COUNT_UNAVAILABLE',1),
      ('', 'runningAfter=false', 'ENGINE_GC_STATE_CHANGED',1),
      ('', 'clockFailAfter=true', 'CLOCK_INVALID',1),
      ('', 'cpuStep=-0.25', 'CLOCK_INVALID',1),
      ('', 'wallStep=-1', 'CLOCK_INVALID',1),
      ('', 'timeFailAfter=true', 'CLOCK_INVALID',1),
      ('', 'cpuStep=2.01', 'OVER_2_SECONDS',1),
      ('', 'wallStep=3', 'OVER_2_SECONDS',1),
      ("Events.LoadScreenClose=nil", '', 'HOOK_UNAVAILABLE:LoadScreenClose',0),
      ("Events.PlayerTurnActivated.Add=function()error('hook denied')end", '', 'HOOK_REGISTRATION_FAILED:PlayerTurnActivated',0),
    ]
    for before,after,reason,collections in cases:
        lua=runtime(repo,before)
        if not lua.eval('a.failure'):
            lua.execute('loadGame()')
        if not lua.eval('a.failure'):
            lua.execute(after+';cycle(42,500)')
        assert lua.eval("type(d.Read)=='function'"), 'GC failure removed the count-only observer'
        failure=lua.eval('a.failure')
        assert failure and failure.startswith(reason),(before,after,reason,failure)
        assert lua.eval('gcCalls')==collections and lua.eval('a.enabled') is False,(reason,lua.eval('gcCalls'))
        lua.execute('''
          local n=gcCalls;local oldFailure=a.failure
          collectgarbage=gcMock;countUnavailable=false;countInvalid=false;gcRunning=true;runningAfter=nil;postCountUnavailable=false
          d.SetAutoGC(4,true,'cannot-rearm');d.CollectGC(4,'cannot-retry')
          turn=50;if Events.PlayerTurnActivated then Events.PlayerTurnActivated.Fire(4)end
          if Events.GameCoreEventPublishComplete then publish()end
          assert(gcCalls==n and a.failure==oldFailure and not a.enabled);intact()
        ''')
    for setup in ['statusUnavailable=true', 'timeUnavailable=true', 'cpuStep=2;wallStep=2']:
        lua=runtime(repo)
        lua.execute('loadGame();'+setup+';cycle(42,500);assert(gcCalls==1 and not a.failure);intact()')
    lua=runtime(repo)
    lua.execute('''
      loadGame();P.IsTestPlayer=function()error('eligibility read failed')end
      turn=42;activate(4);assert(not a.enabled and a.failure:find('CALLBACK_FAILED:',1,true) and gcCalls==0)
    ''')
    print(f'PASS GC failure latch: {len(cases)} missing/count/clock/stopped/collect/state/timing/hook cases + callback failure; optional status/wall and exact2s allowed')


def bounded_state(repo):
    lua=runtime(repo)
    lua.execute('''
      loadGame()
      for i=1,12 do cycle(40+2*i,i==1 and 328 or 228)end
      assert(gcCalls==12 and a.collections==12 and #a.rows==8 and a.rows[1].turn==50 and a.rows[8].turn==64)
      for i=1,30 do d.SetAutoGC(4,i%2==0,'switch'..i)end
      assert(#logs==24 and logs[24]:find('LOG_LIMIT',1,true))
      local n=#logs;d.SetAutoGC(4,false,'last');assert(#logs==n and not a.enabled and a.reason=='DISABLED_BY_USER')
      local report=d.ReadGC(4);assert(report:find('T50 ',1,true) and not report:find('T48 ',1,true))
      assert(#a.rows==8);intact()
    ''')
    print('PASS GC bounded state: result ring8/log24; continued current status after log cap; saved authority untouched')


def gameplay_and_ui(repo):
    gameplay=(repo/'Mod/Gameplay.lua').read_text()
    early=gameplay[:gameplay.index("  if params.Action=='CLAIM_BEGIN'")]
    wrapper=gameplay[gameplay.index('GameEvents.SPC_P0_Request.Add(function(...)'):gameplay.index('stage("INITIALIZED ISOLATED_PROBES USER_GAME_TEST_REQUIRED")')]
    lua=runtime(repo,start=False)
    lua.execute(early+'\nend\n'+wrapper+'\nrequestGC=request;requestShared=shared')
    lua.execute('''
      shared=requestShared;shared.NetworkBridge={ready=true,players={}}
      shared.savedAuthority={identity='RESEARCH',potential=3,receipts=2}
      SPCPerformance.StartMemory(P,shared);d=shared.MemoryObservation;a=d.AutoGC
      loadGame();local n=countCalls
      GameEvents.SPC_P0_Request.Fire(4,{Action='MEMORY_GC_READ',Token='read'})
      assert(shared.LastToken=='read' and shared.RequestDepth==0 and gcCalls==0 and countCalls==n)
      GameEvents.SPC_P0_Request.Fire(4,{Action='MEMORY_GC_AUTO_OFF',Token='off'})
      assert(not a.enabled and shared.LastToken=='off' and gcCalls==0)
      GameEvents.SPC_P0_Request.Fire(4,{Action='MEMORY_GC_AUTO_ON',Token='on'})
      assert(a.enabled and shared.LastToken=='on' and gcCalls==0)
      GameEvents.SPC_P0_Request.Fire(7,{Action='MEMORY_GC_AUTO_OFF',Token='foreign'});assert(a.enabled and gcCalls==0)
      turn=42;heap=500*1024;activate(4)
      local read=d.ReadGC;d.ReadGC=function(pid)
        assert(shared.RequestDepth==1);publish();return read(pid)
      end
      GameEvents.SPC_P0_Request.Fire(4,{Action='MEMORY_GC_READ',Token='nested-publish'})
      assert(gcCalls==0 and a.reason=='SKIP:REQUEST_INFLIGHT' and shared.RequestDepth==0)
      d.ReadGC=read;cycle(43,500);assert(gcCalls==1)
      shared.MemoryObservation=nil
      GameEvents.SPC_P0_Request.Fire(4,{Action='MEMORY_GC_READ',Token='notready'})
      assert(shared.Snapshot:find('GC诊断不可用',1,true) and shared.RequestDepth==0 and gcCalls==1)
      shared.MemoryObservation=d;intact()
    ''')
    # Actual P0Panel request closure and actual click registrations, no full UI startup.
    ui=(repo/'Mod/UI/P0Panel.lua').read_text()
    prefix=ui[:ui.index('local function legacyCopy(asBaseline)')]
    buttons=ui[ui.index(' Controls.PerformanceSnapshotButton:SetHide(false)'):ui.index(' local function projectAction(fn)')]
    lua.execute('''
      controls={};Controls=setmetatable({},{__index=function(t,k)
        local c={callbacks={}};c.SetText=function(_,v)c.text=v end;c.SetHide=function()end
        c.CalculateSize=function()end;c.ReprocessAnchoring=function()end;c.SetToolTipString=function(_,v)c.tooltip=v end
        c.RegisterCallback=function(_,button,f)c.callbacks[button]=f end;t[k]=c;return c
      end})
      Mouse={eLClick=1,eRClick=2};SPCCityIdentityEvidence={New=function()return{}end}
      SPCOverflowStorageRead={New=function()return{Pulse=function()end}end}
      ContextPtr={ClearUpdate=function()end,SetUpdate=function(_,f)update=f end}
      PlayerOperations={EXECUTE_SCRIPT=1};packets={}
      UI={GetHeadSelectedCity=function()error('CITY_READ_FORBIDDEN')end,
        RequestPlayerOperation=function(pid,op,packet)
          assert(pid==4 and op==1 and packet.CityID==nil);packets[#packets+1]=packet
          GameEvents.SPC_P0_Request.Fire(pid,packet)
        end}
      function click(button)Controls.PerformanceSnapshotButton.callbacks[button]()end
    ''')
    lua.execute(prefix+'\n'+buttons)
    lua.execute('''
      local n=gcCalls;click(1);assert(packets[#packets].Action=='MEMORY_GC_READ' and gcCalls==n)
      click(2);assert(packets[#packets].Action=='MEMORY_GC_AUTO_OFF' and not a.enabled and gcCalls==n)
      click(2);assert(packets[#packets].Action=='MEMORY_GC_AUTO_ON' and a.enabled and gcCalls==n)
      assert(Controls.Status.text:find('ACK',1,true));intact()
    ''')
    print('PASS actual early Gameplay/wrapper and P0Panel read/toggle buttons: no city read, no immediate collection, request-depth guard/response')


def static(repo):
    perf=(repo/'Mod/PerformanceCounters.lua').read_text()
    assert perf.count("pcall(collectgarbage,'collect')")==1
    calls=re.findall(r"collectgarbage\s*,\s*['\"]([^'\"]+)['\"]",perf)
    assert set(calls)=={'count','isrunning','collect'},calls
    assert 'SetProperty' not in perf and 'CreateBuilding' not in perf and 'RemoveBuilding' not in perf
    assert not re.search(r'collectgarbage\s*\(', perf), 'Unreviewed direct GC primitive' 
    lua=LuaRuntime()
    claim=(repo/'Mod/ClaimProjects.lua').read_text()
    assert 'function d.IsBusy()return busy end' in claim
    for name in ['PerformanceCounters.lua','Gameplay.lua','UI/P0Panel.lua','Probe.lua','ClaimProjects.lua']:
        lua.execute('assert(load(...))',(repo/'Mod'/name).read_text())
    manifest=ET.parse(repo/'Mod/SpecializationP0.modinfo').getroot()
    assert manifest.get('version')=='165'
    listed=[f.text for f in manifest.findall('./Files/File')]
    actual={str(p.relative_to(repo/'Mod')) for p in (repo/'Mod').rglob('*') if p.is_file() and p.name not in ('.DS_Store','SpecializationP0.modinfo')}
    assert len(listed)==len(set(listed)) and set(listed)==actual
    print('PASS static: one full-collection primitive, no GC strategy or gameplay/property writes, Claim read-only busy getter and five changed Lua files compile')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1])
    repo=parser.parse_args().repo.resolve()
    assert (repo/'Mod/PerformanceCounters.lua').is_file(),repo
    behavior(repo);safety_gates(repo);failure_latches(repo);bounded_state(repo);gameplay_and_ui(repo);static(repo)
    print('LOCAL_SIMULATION_PASS: bounded B138 GC contracts; native collector semantics/stall timing/heap or process benefit remain unverified')


if __name__=='__main__':
    main()
