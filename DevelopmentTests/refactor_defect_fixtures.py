"""Real caller/consumer code with explicit isolated dependency doubles, all Lua51."""
import re
from refactor_harness import Context,ROOT,TrackedLua51,legacy_source_observation

def commerce():
    import test_culture_network
    test_culture_network.LuaRuntime=TrackedLua51
    from test_b239_commerce import fixture
    with legacy_source_observation():l=fixture()
    return fact_publication_profile(l)

def fact_publication_profile(l, automatic=True):
    l.execute((ROOT/'Mod/FactChanges.lua').read_text());l.execute((ROOT/'Mod/FactConsumerBindings.lua').read_text())
    l.execute((ROOT/'Mod/NativeFacts.lua').read_text());l.execute("SPCFactChanges.New(shared);if not shared.NativeFacts then SPCNativeFacts.New(P,shared)end;SPCFactConsumerBindings.New(shared)")
    if automatic:
        l.execute("""
        fixtureDrain=false
        function fixturePublication()
         if fixtureDrain then return end;fixtureDrain=true
         shared.FactChanges.Flush();shared.FactBindings.Flush()
         -- Existing dirty consumers drain at their real publish hook.
         Events.GameCoreEventPublishComplete.Fire();fixtureDrain=false
        end
        if fire and not fixtureNativeFire then
         fixtureNativeFire=fire
         fire=function(...)fixtureNativeFire(...);fixturePublication()end
        end
        for _,name in ipairs({'Refresh','CheckEvidence','Receive'})do
         local original=net[name]
         net[name]=function(...)local out=original(...);fixturePublication();return out end
        end
        """)
    return l

def gc():
    import test_b269_memory
    test_b269_memory.LuaRuntime=TrackedLua51
    case=test_b269_memory.LuaTests()
    with legacy_source_observation():case.setUp()
    case.l.execute('Events.LoadScreenClose.Fire();turn=3;heap=700*1024')
    return case.l

def request_context():
    c=Context();c.load('SafeCallbacks');c.load('FactChanges');c.load('FactConsumerBindings')
    c.execute("P={Scalar=tostring,IsTestPlayer=function(pid)return pid==0 end};shared={};stage=function()end;city={GetOwner=function()return 0 end};Players={[0]={GetCities=function()return {FindID=function()return city end}end}};SPCFactChanges.New(shared);SPCFactConsumerBindings.New(shared)")
    c.execute(c.fragment('Mod/Gameplay.lua','local function refreshInvestmentSupport(', 'local function request(playerID,params)')+'\n_G.refreshInvestmentSupport=refreshInvestmentSupport')
    # Maintained synchronous fixture explicitly closes one publication boundary
    # after the request; production request remains deferred and ACK is independent.
    c.execute(c.fragment('Mod/Gameplay.lua','local function request(playerID,params)','GameEvents.SPC_P0_Request.Add')+'\nrunRequest=function(...)request(...);shared.FactChanges.Flush();shared.FactBindings.Flush()end')
    return c

def startup():
    c=Context();c.execute(r"""
starts={};lateWrites=0;sealed=false
SPCP0={VERSION='S2',Scalar=tostring,Field=function(t,k)return t and t[k]end,IsTestPlayer=function(p)return p==0 end}
SPCPerformance={New=function()return {}end,StartMemory=function()end}
print=function()end
function module(name,export)
 return {Start=function(P,s)
  starts[#starts+1]=name
  local d=setmetatable({errors={},views={},seq={},generation=1},{__index=function()return function()end end})
  s[export or name]=d
  if name=='ResearchTraditionEffects'then
   Events.LoadScreenClose.Add(function()lateWrites=lateWrites+1 end)
   error('FIXTURE_LATE_START_FAILURE')
  end
  return d
 end,RegisterExit=function()end}
end
""")
    source=(ROOT/'Mod/Gameplay.lua').read_text()
    symbols=set(re.findall(r'(SPC\w+)\.Start\(',source))
    for symbol in symbols:
        c.execute('_G[...]=module(select(2,...))',symbol,symbol[3:])
    # Includes are isolated module doubles except the composition helper introduced by S3.
    def include(name):
        if name in ('RuntimeComposition','SafeCallbacks','ReadinessLatch','FactChanges','FactConsumerBindings','EffectiveFacts','RuntimeWork','NativeFacts') and (ROOT/'Mod'/f'{name}.lua').exists():return c.load(name)
        if name=='Probe':return
        if name=='ReadinessSummary':
            c.execute('SPCReadinessSummary={Start=function()return {Seal=function()sealed=true end}end}')
        elif name=='ExpeditionTrainingDiagnostics':
            c.execute('SPCExpeditionTrainingDiagnostics={ENABLED=false,New=function()return {Record=function()end}end}')
        else:
            c.execute('if _G[...] == nil then _G[...]=module(select(2,...))end','SPC'+name,name)
    c.globals().include=include
    return c

def greatworks(extra=""):
    c=Context('UI');c.execute(r"""
P={VERSION='S2',Count=function(k)counts[k]=(counts[k]or 0)+1 end,
 IsTestPlayer=function(p)return p==0 end,Field=function(t,k)return t and t[k]end}
SPCP0=P;SPCDiagnosticLog={For=function()return function()end end}
SPCGreatWorkFacts={Hex=tostring,Collector=function()return function(c)return {},{}end end}
SPCNetworkInput={Reference=function(c)return 'REF:'..c:GetID()end}
city1={GetID=function()return 1 end};city2={GetID=function()return 2 end}
Players={[0]={GetCities=function()return {Members=function()return ipairs({city1,city2})end}end}}
ExposedMembers.SPC_P0={Version='S2',Dialogue={seq={[0]=0},generation=1,ready=true},
 GreatWorkFacts={epoch=1,ack=0,inputRevision=1,dirtyScope={all=true,cities={}}},
 EffectiveFacts={Read=function(pid,c)return {specialization='CULTURE',active=c==city1 and nil or 1}end}}
-- Lua and/or cannot represent an intentional nil. Set it explicitly.
ExposedMembers.SPC_P0.EffectiveFacts.Read=function(pid,c)
 local f={specialization='CULTURE',active=1};if c==city1 then f.active=nil end;return f
end
PlayerOperations={EXECUTE_SCRIPT=1};UI={RequestPlayerOperation=function(pid,op,p)packet=p;return true end}
""")
    c.globals().include=lambda name:None
    if extra:c.execute(extra)
    c.load('UI/DialogueRefresh');c.execute('init()')
    return c

def panel(extra=""):
    c=Context('UI');c.execute(r"""
SPCP0={};SPCRestructuringUI={ObserveTraining=function()end};PlayerOperations={};UI={RequestPlayerOperation=function()end,GetHeadSelectedCity=function()end}
nativeAdvances=0;siblings=0
function noop()end
PopulateGenericItemData=function()end;CreateQueueInstance=function()end;RefreshCurrentProduction=function()end
GetDataHelper=function()return {ProjectItems={{Type='PROJECT_NATIVE',Name='native'}},UnitItems={{Type='UNIT_NATIVE'}},City={}}end
AdvanceProject=function()nativeAdvances=nativeAdvances+1 end;CheckQueueItemSelected=function()return false end
BuildUnit=noop;RemoveQueueItem=noop;GetBuildInsertMode=function()return 0 end
SPCTimedProjectDisplay={Current=noop,Items=noop};SPCCrewModel={Parse=function()end};SPCProjectTurnRead={New=noop}
function adapter(name)
 return {New=function()return {Items=function(data)
  if name=='CapitalInvestmentUI'then data.ProjectItems[1].Name='corrupt';data.ProjectItems[#data.ProjectItems+1]={Type='PROJECT_PARTIAL'};error('FIXTURE_ADAPTER_FAILURE')end
  if name=='DevelopmentInvestmentUI'then siblings=siblings+1 end
 end,Before=function()return true end,Sync=noop,Publish=noop,Pulse=noop,WarmStart=noop,Invalidate=noop,RefreshFacts=noop,CancelQueue=noop}end,
 IsProject=function()return false end,PROJECT='PROJECT_SPC_TEST',KIND='UNIT_SPC_TEST'}
end
""")
    symbols=['TimedProjectSelection','ClaimProjectUI','DialogueProjectUI','EngineeringStudyUI','CapitalInvestmentUI','DevelopmentInvestmentUI','CommerceUI','CrewProjectUI','ExpeditionTrainingUI']
    for name in symbols:c.execute('_G[...]=adapter(select(2,...))','SPC'+name,name)
    def include(name):
        if name in ('SafeAdapters','UI/SafeAdapters'):return c.load('UI/SafeAdapters')
    if extra:c.execute(extra)
    c.globals().include=include;c.load('UI/CrewProjectOrder');return c

def store_completion():
    c=Context();c.execute("""
d={};writes=0;root={schema=2,stage='ACTIVE',progression='UNASSIGNED',base={revision=1},revision=1,origin={owner=0,cityID=1}}
function cp(t)if type(t)~='table'then return t end;local o={};for k,v in pairs(t)do o[k]=cp(v)end;return o end
same=function(a,b)return a==b end;active=function()return root end;save=function(n)root=n;writes=writes+1 end
shared.FactChanges={InvalidateCommitted=function()end,Emit=function()error('FIXTURE_POST_COMMIT_OBSERVER')end}
""")
    c.execute(c.fragment('Mod/CityProgressionStore.lua','local function publishFact(', 'local function CreateProgressionRecord(')+'\n_G.publishFact=publishFact')
    c.execute(c.fragment('Mod/CityProgressionStore.lua',' function d.Complete(pid,c,e)',' -- Claim state belongs'))
    return c
