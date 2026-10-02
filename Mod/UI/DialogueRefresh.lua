include('DiagnosticLog')
local print=SPCDiagnosticLog and SPCDiagnosticLog.For('DialogueRefresh') or print
include('Probe')
include('DialogueModel')
include('GreatWorkAdjacencyModel')
include('GreatWorkFacts')
local P=SPCP0
local busy,dirty,revision=false,true,0
local sent,pending,seq,epoch,generation,inputRevision=nil,nil,0,nil,nil,nil
local hooks,cache,workDirty={}, {}, {}
local allWorks=true;local collect
local public={scans=0,slotReads=0,sends=0,retries=0,state='STARTUP',reason='INITIALIZATION'}
ExposedMembers.SPC_DialogueBackground=public
local function mark(reason,cid,works)
 dirty=true;revision=revision+1;public.reason=reason
 if works then if cid~=nil then workDirty[cid]=true else allWorks=true end end
end
local function dispatch(pid,packet)
 public.sends=public.sends+1
 local ok,result=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,packet)
 public.transport=ok and tostring(result) or ('ERROR: '..tostring(result))
 return ok and result~=false
end
local function acknowledged(s,pid,flight)
 return (s.Dialogue.seq[pid] or 0)>=flight.seq and s.GreatWorkFacts and s.GreatWorkFacts.ack>=flight.seq
end
local safe
local function refresh()
 local s=ExposedMembers.SPC_P0;local pid=Game.GetLocalPlayer()
 if busy or not s or s.Version~=P.VERSION or not s.Dialogue or not s.GreatWorkFacts or not P.IsTestPlayer(pid) then return end
 if epoch~=s.GreatWorkFacts.epoch or generation~=s.Dialogue.generation then
  epoch=s.GreatWorkFacts.epoch;generation=s.Dialogue.generation
  pending=nil;sent=nil;cache={};mark('SESSION_REFERENCE_CHANGED',nil,true)
 end
 if inputRevision~=s.GreatWorkFacts.inputRevision then
  inputRevision=s.GreatWorkFacts.inputRevision;pending=nil;sent=nil
  local scope=s.GreatWorkFacts.dirtyScope or {all=true,cities={}}
  if scope.all then allWorks=true end;for cid in pairs(scope.cities)do workDirty[cid]=true end
  mark('WORK_INPUT_CHANGED',nil,false)
 end
 local turn=Game.GetCurrentGameTurn();local ack=math.max(s.Dialogue.seq[pid] or 0,s.GreatWorkFacts.ack)
 if pending then
  if acknowledged(s,pid,pending) then pending=nil;public.state='IDLE'
  elseif turn~=pending.turn then pending=nil;sent=nil;mark('TURN_RETRY',nil,true)
  elseif dirty and public.state=='ACK_TIMEOUT' then pending=nil;sent=nil
  else if public.state~='ACK_TIMEOUT' then public.state='WAIT_ACK' end;return end
 end
 if not dirty then return end
 busy=true;dirty=false;local thisRevision=revision
 collect=collect or SPCGreatWorkFacts.Collector(P)
 local adjData,adjCount='',0
 local rows,signature,facts,refs={}, {}, {}, {};local factsCount,factsCities=0,0
 local seenCities={};public.scans=public.scans+1
 local ok,why=pcall(function()
  local cities={};for _,c in Players[pid]:GetCities():Members() do P.Count('city_scan');cities[#cities+1]=c;assert(#cities<=512,'GW_CITY_LIMIT') end
  table.sort(cities,function(a,b)return a:GetID()<b:GetID()end)
  local legacyValid=true
  for _,c in ipairs(cities) do
   local id=c:GetID();seenCities[id]=true
   local ref=SPCNetworkInput.Reference(c);local stored=cache[id]
   if allWorks or workDirty[id] or not stored or stored.reference~=ref then
    public.slotReads=public.slotReads+1
    local readable,raw,legacy=pcall(collect,c)
    stored={reference=ref,known=readable,raw=readable and raw or {},legacy=readable and legacy or {}}
    cache[id]=stored
   end
   factsCities=factsCities+1;refs[#refs+1]=id..','..SPCGreatWorkFacts.Hex(ref)..','..(stored.known and '1' or '0')..';'
   rows[#rows+1]=id..',-1,EMPTY'
   if not stored.known then legacyValid=false end
   for _,w in ipairs(stored.legacy) do rows[#rows+1]=id..','..w.id..','..w.type end
   for _,w in ipairs(stored.raw) do facts[#facts+1]=id..','..w.building..','..w.slot..','..w.id..','..w.type..';';factsCount=factsCount+1 end
   local f=s.EffectiveFacts.Read(pid,c);signature[#signature+1]=id..':'..f.specialization..':'..f.active
  end
  for id in pairs(cache) do if not seenCities[id] then cache[id]=nil end end
  assert(legacyValid,'GW_COLLECTION_UNAVAILABLE')
  if s.GreatWorkAdjacency then
   local aok,adata,acount=pcall(SPCGWAdjacencyModel.Collect,P,pid)
   public.adjacencyError=not aok and tostring(adata) or nil
   if aok then adjData,adjCount=adata,acount else adjData='';adjCount=-1 end
  end
 end)
 -- Clear only the work that this collection consumed; concurrent marks survive.
 if revision==thisRevision then workDirty={};allWorks=false end
 local data=ok and table.concat(rows,';') or ''
 local factData,refData=table.concat(facts),table.concat(refs)
 local key=turn..':'..tostring(ok)..':'..data..':'..table.concat(signature,';')..':'..adjData..':'..adjCount..':'..epoch..':'..refData..':'..factData
 if sent~=key or not s.Dialogue.ready then
  seq=math.max(seq,ack)+1;sent=key
  local packet={OnStart='SPC_P0_Request',Action='DIALOGUE_SAMPLE',Token=P.VERSION..':dialogue:'..seq,Generation=generation,Seq=seq,Turn=turn,Valid=ok and 1 or 0,Data=data,Count=#rows,AdjData=adjData,AdjCount=adjCount,
   FactsEpoch=epoch,FactsInput=inputRevision,FactsRefs=refData,FactsData=factData,FactsCount=factsCount,FactsCities=factsCities}
  pending={seq=seq,turn=turn,generation=generation,epoch=epoch,packet=packet,pulses=0,retries=0};public.state='WAIT_ACK'
  dispatch(pid,packet)
  if acknowledged(s,pid,pending) then pending=nil;public.state='IDLE' end
 else public.state='IDLE' end
 if not ok then public.state='COLLECT_ERROR';public.collectionError=tostring(why):match('GW_[A-Z_]+') or 'COLLECT_ERROR' else public.collectionError=nil end
 if revision~=thisRevision then dirty=true end
 busy=false
end
safe=function()
 local ok,err=pcall(refresh)
 if not ok then busy=false;public.state='ERROR';public.collectionError=tostring(err):sub(1,160);print('[SPC][K][UI] '..tostring(err)) end
end
-- Generic pulses drain a finite pending packet/dirty scope, never schedule new scans.
local function pulse()
 local s=ExposedMembers.SPC_P0;local pid=Game.GetLocalPlayer()
 if pending and s and s.GreatWorkFacts and s.Dialogue and not busy
  and pending.epoch==s.GreatWorkFacts.epoch and pending.generation==s.Dialogue.generation and not acknowledged(s,pid,pending) then
  pending.pulses=pending.pulses+1
  if pending.pulses>=3 and pending.retries<2 then
   pending.pulses=0;pending.retries=pending.retries+1;public.retries=public.retries+1
   local flight=pending;busy=true;dispatch(pid,flight.packet);busy=false
   if pending==flight and flight.retries>=2 then public.state='ACK_TIMEOUT' end
  end
 end
 safe()
end
local function bind(name,fn)
 local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,fn=fn} end
end
ContextPtr:SetInitHandler(function()
 bind('GreatWorkCreated',function(pid,creator,x,y)
  if pid~=Game.GetLocalPlayer() then return end
  local ok,c=pcall(function()return Cities.GetCityInPlot(Map.GetPlotIndex(x,y))end)
  mark('GreatWorkCreated',ok and c and c:GetOwner()==pid and c:GetID() or nil,true)
 end)
 bind('GreatWorkMoved',function(op,oc,dp,dc)
  local pid=Game.GetLocalPlayer()
  if type(op)~='number' or type(dp)~='number' then mark('GreatWorkMoved_UNLOCATED',nil,true);return end
  if op==pid then mark('GreatWorkMoved',type(oc)=='number' and oc or nil,true) end
  if dp==pid then mark('GreatWorkMoved',type(dc)=='number' and dc or nil,true) end
 end)
 for _,name in ipairs({'CityAddedToMap','CityRemovedFromMap'})do
  local reason=name;bind(name,function(pid,cid)if pid==Game.GetLocalPlayer()then if cid~=nil then cache[cid]=nil end;mark(reason,type(cid)=='number' and cid or nil,true)else mark(reason,nil,false)end end)
 end
 -- Transfer signature/object availability can be ambiguous: one bounded local scope.
 bind('CityTransfered',function()mark('CityTransfered',nil,true)end)
 bind('PlayerTurnActivated',function(pid)if pid==Game.GetLocalPlayer()then mark('PlayerTurnActivated',nil,true)end end)
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished'})do
  local reason=name;bind(name,function(cityOwner,cid,governorOwner)
   local pid=Game.GetLocalPlayer();if cityOwner==pid or governorOwner==pid then mark(reason,nil,false)end
  end)
 end
 for _,name in ipairs({'GovernorPromoted','GovernorChanged'})do
  local reason=name;bind(name,function(pid)if pid==Game.GetLocalPlayer()then mark(reason,nil,false)end end)
 end
 for _,name in ipairs({'DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged'})do
  local reason=name;bind(name,function(pid,districtID,cid)
   if pid==Game.GetLocalPlayer()then mark(reason,type(cid)=='number' and cid or nil,true)else mark(reason,nil,false)end
  end)
 end
 -- Preserve the existing adjacency dependencies. They do not recollect work slots.
 for _,name in ipairs({'ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap','FeatureAddedToMap','CityTileOwnershipChanged'})do
  local reason=name;bind(name,function()mark(reason,nil,false)end)
 end
 bind('LoadScreenClose',function()cache={};mark('LOAD_SCREEN_CLOSE',nil,true);safe()end)
 for _,name in ipairs({'SystemUpdateUI','GameCoreEventPublishComplete','GameCoreEventPlaybackComplete'})do bind(name,pulse)end
 safe()
end)
ContextPtr:SetShutdown(function()
 pending=nil;cache={};workDirty={}
 for _,h in ipairs(hooks)do if h.event.Remove then h.event.Remove(h.fn)end end
 hooks={}
 if ExposedMembers.SPC_DialogueBackground==public then ExposedMembers.SPC_DialogueBackground=nil end
end)
