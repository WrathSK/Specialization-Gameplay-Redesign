"""Method-shaped UI queue around actual Store/controllers/readiness.
UI native counters exclude actual Gameplay work. Historical UI doubles use the
same inputs but their original handshake; no fabricated ACK or saved timer.
"""
from refactor_harness import ROOT,legacy_source_observation
from test_refactor_s7d1 import actual

SPECS={
 'Claim':('ClaimProjectUI','SPCClaimProjectUI','ClaimProjects','SPC_ClaimQueueRead','CLAIM_BEGIN','CLAIM_SYNC'),
 'Dialogue':('DialogueProjectUI','SPCDialogueProjectUI','DialogueProjects','SPC_DialogueProjectRead','DIALOGUE_PROJECT_BEGIN','DIALOGUE_PROJECT_SYNC'),
 'Engineering':('EngineeringStudyUI','SPCEngineeringStudyUI','EngineeringStudy','SPC_EngineeringStudyRead','ENGINEERING_STUDY_BEGIN','ENGINEERING_STUDY_SYNC'),
}

def fixture(kind,gp_first=True,connect=False):
 vm=actual(kind)
 def include(name):
  candidates=(ROOT/'Mod/UI'/(name+'.lua'), ROOT/'Mod'/(name+'.lua'))
  p=next((x for x in candidates if x.is_file()),None)
  if p is None:raise FileNotFoundError(name)
  with legacy_source_observation():vm.execute(p.read_text())
 vm.globals().include=include
 module,exported,backend,reader,begin,sync=SPECS[kind]
 for k,v in dict(fixtureKind=kind,backendKey=backend,readerKey=reader,beginAction=begin,syncAction=sync).items():vm.globals()[k]=v
 vm.execute('''
 q.target='NORMAL';changed();assert(not pending()or pending().stage=='STOPPED')
 Game.GetLocalPlayer=function()return 0 end
 ExposedMembers=ExposedMembers or {};ExposedMembers.SPC_P0=shared
 PlayerOperations={EXECUTE_SCRIPT=1}
 local row=assert(P.Info('Projects',project));local hash=row.Hash or row.Index
 GameInfo.Projects=GameInfo.Projects or {};GameInfo.Projects[project]={Hash=hash}
 q.GetCurrentProductionTypeHash=function()return q.target==project and hash or 0 end
 uiQueueSize=1;q.GetSize=function()return uiQueueSize end
 if fixtureKind=='Dialogue'then GameInfo.Buildings=function()return function()end end end
 uiPackets={};uiBegins=0;uiNotifies=0;uiReads=0;uiSyncs=0;uiMembers=0;uiFinds=0;uiCollections=0
 inBackend=false
 local player=Players[0];local getCities=player.GetCities
 player.GetCities=function(...)
  if not inBackend then uiCollections=uiCollections+1 end
  local raw=getCities(...);local proxy=setmetatable({},{__index=raw})
  proxy.Members=function(_,...)if not inBackend then uiMembers=uiMembers+1 end;return raw.Members(raw,...)end
  proxy.FindID=function(_,...)if not inBackend then uiFinds=uiFinds+1 end;return raw.FindID(raw,...)end
  return proxy
 end
 function sendUI(pid,op,p)
  uiPackets[#uiPackets+1]=p
  if p.Action==beginAction then
   uiBegins=uiBegins+1
   if duringSend then duringSend(p)end
   if failBegin then error('BEGIN_UNCONFIRMED')end
   inBackend=true;local ok,err=pcall(shared[backendKey].Request,pid,p);inBackend=false
   if not ok then error(err)end
  elseif p.Action==syncAction then
   uiSyncs=uiSyncs+1
   if duringSync then duringSync(p)end
   if failSync then error('SYNC_UNCONFIRMED')end
   if dropSync then return end
   inBackend=true;local ok,err=pcall(shared[backendKey].Sync,pid,p.CityID,p.Token);inBackend=false
   if not ok then error(err)end
  else error('UNEXPECTED_UI_ACTION_'..tostring(p.Action))end
 end
 function newService()
  inBackend=true;service=SPCTimedProjectReaders.New(P,shared)
  service.Attach(backendKey,shared[backendKey]);service.Seal();inBackend=false
 end
 ''')
 include('TimedProjectReaders')
 if gp_first:vm.execute('newService();assert(service.epoch==1)')
 include(module)
 # Wrap only before Configure so the final owned reader identity is captured.
 vm.execute('''
 local function instrument(raw)
  return function(...)
   uiReads=uiReads+1
   if unreadable then error('QUEUE_READ_UNKNOWN')end
   local value=raw(...)
   if afterQueueRead then afterQueueRead()end
   return value
  end
 end
 local current=SPCTimedProjectSelectionClient and type(SPCTimedProjectSelectionClient.New)=='function'
 if current then
 local nativeNew=SPCTimedProjectSelectionClient.New
 SPCTimedProjectSelectionClient.New=function(...)
  local api=nativeNew(...);local configure=api.Configure
  if not configure then return api end
  api.Configure=function(kind,key,...)
   local raw=assert(ExposedMembers[key])
   ExposedMembers[key]=instrument(raw)
   return configure(kind,key,...)
  end
  return api
 end
 end
 ui=_G[...].New(P,sendUI,function()uiNotifies=uiNotifies+1 end)
 if not ui.Connect then ExposedMembers[readerKey]=instrument(assert(ExposedMembers[readerKey]))end
 function pumpUI()return (ui.Pulse or ui.Publish)()end
 function selectUI()return ui.Before(c,{Type=project},false)end
 function ordinaryUI()return ui.Before(c,{Type='NORMAL'},false)end
 function queueEventUI(pid,id)return ui.QueueEvent(pid,id)end
 function ownEventUI()return queueEventUI(c:GetOwner(),c:GetID())end
 function idleUI(n)for i=1,n do pumpUI()end end
 function counts()return uiReads,uiSyncs,uiMembers,uiFinds,uiCollections,uiBegins end
 ''',exported)
 if connect:
  vm.execute('''
  if ui.Connect then ui.Connect()elseif ui.WarmStart then ui.WarmStart()end
  pumpUI();pumpUI()
  uiPackets={};uiBegins=0;uiReads=0;uiSyncs=0;uiMembers=0;uiFinds=0;uiCollections=0
  ''')
 return vm
