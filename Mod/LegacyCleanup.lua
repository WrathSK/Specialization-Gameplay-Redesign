if not SPCLegacyCleanupCatalog then include('LegacyCleanupCatalog')end
-- Confirmed city exit cleanup and the established load-only experiment withdrawals.
SPCLegacyCleanup={}

local function withdrawExperiment(P,city,names,missing,unconfirmed)
 for _,name in ipairs(names)do
  local row=assert(P.Info('Buildings',name),missing)
  local buildings=city:GetBuildings()
  if P.HasBuilding(buildings,row.Index)~=false then P.RemoveBuilding(buildings,row.Index)end
  assert(P.HasBuilding(buildings,row.Index)==false,unconfirmed)
 end
end

function SPCLegacyCleanup.InstallPurchaseLoad(P)
 local load=P.Field(Events,'LoadScreenClose')
 if load and load.Add then
  local names=SPCLegacyCleanupCatalog.Group('PurchaseProbe').names
  load.Add(function()
   for _,player in pairs(Players)do for _,city in player:GetCities():Members()do
    P.Count('city_scan')
    local ok,err=pcall(withdrawExperiment,P,city,names,'B053_DATABASE_MISSING','B053_CARRIER_UNCONFIRMED')
    if not ok then print('[SPC][B053][CLEANUP] '..tostring(err))end
   end end
  end)
 end
end

function SPCLegacyCleanup.StartGreatWorkLoad(P,shared)
 local cleanup={ready=false}
 local names=SPCLegacyCleanupCatalog.Group('GreatWorkProbe').names
 function cleanup.Clean()
  for _,player in pairs(Players)do
   local cities=player:GetCities()
   if cities then for _,city in cities:Members()do
    P.Count('city_scan')
    withdrawExperiment(P,city,names,'B055_GW_DATABASE_MISSING','B055_GW_WRITE_UNCONFIRMED')
   end end
  end
  cleanup.ready=true
 end
 shared.GreatWorkLoadCleanup=cleanup
end

function SPCLegacyCleanup.StartCommerceLoad(P,shared)
 local d={busy=false,errors={},writes=0}
 local names=SPCTombstones.Names('CommerceConvergence')
 function d.Withdraw(c)
  assert(c and P.IsTestPlayer(c:GetOwner()),'COM_LEGACY_OWNER_UNSUPPORTED')
  assert(shared.CityProgressionStore.HistoricalReference(c),'COM_LEGACY_REFERENCE_UNKNOWN')
  SPCRuntimeWork.RetireOnce(P,shared,c,'CommerceConvergence',function()
   local rows={}
   for _,name in ipairs(names)do
    local row=assert(P.Info('Buildings',name),'COM_LEGACY_DEFINITION_UNKNOWN')
    local has=P.HasBuilding(c:GetBuildings(),row.Index)
    assert(type(has)=='boolean','COM_LEGACY_PRESENCE_UNKNOWN')
    rows[#rows+1]={id=row.Index,has=has}
   end
   for _,row in ipairs(rows)do if row.has then
    P.RemoveBuilding(c:GetBuildings(),row.id)
    assert(P.HasBuilding(c:GetBuildings(),row.id)==false,'COM_LEGACY_REMOVE_UNCONFIRMED')
    d.writes=d.writes+1
   end end
   return 0
  end)
  return true
 end
 shared.CommerceLegacyCleanup=d
 local load=P.Field(Events,'LoadScreenClose')
 if load and load.Add then load.Add(function()
  if d.busy then return end
  d.busy=true
  for pid,player in pairs(Players)do if P.IsTestPlayer(pid)then
   local cities=player:GetCities()
   if cities then for _,city in cities:Members()do
    local ok,why=pcall(d.Withdraw,city)
    d.errors[pid..':'..city:GetID()]=not ok and tostring(why) or nil
   end end
  end end
  d.busy=false
 end)end
end

-- Load cleanup, scoped retries and confirmed-exit adapters for the old level-three groups.
function SPCLegacyCleanup.StartLv3Support(P,shared)
 include('RuntimeWork')
 include('SpecialistSupport')
 local data={ready=false,busy=false,errors={},changes=0,ruleset='RETIRED_D0032_P0B1'};shared.Lv3Support=data
 local targets=SPCRuntimeWork.NewTargets(P,shared,function(pid,c)
  data.changes=data.changes+SPCSpecialistSupport.Retire(P,c,shared)
 end,function(pid,cid,why)data.errors[tostring(pid)..':'..cid]=why end)
 function data.Audit(scope)
  if not data.ready or data.busy then return end
  data.busy=true
  if type(scope)=='table' and scope.load then targets.Run(scope)else targets.Retry(scope)end
  data.busy=false
 end
 function data.Describe(pid,c)
  return '\n旧三级专家升级：RETIRED（额外2F/2P、工业Gold不再生效）'
   ..'\nretiredRemoved='..data.changes..' error='..tostring(data.errors[pid..':'..c:GetID()] or 'NONE')
 end
 local e=P.Field(Events,'LoadScreenClose');if e and e.Add then e.Add(function() data.ready=true;data.Audit({load=true}) end) end
 SPCRuntimeWork.TargetHook(P,Events,'CityTransfered',data.Audit)
 -- No ordinary scan: only exact failed retirement/exit candidates are retried.
 SPCRuntimeWork.TargetHook(P,Events,'PlayerTurnActivated',data.Audit)
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 assert(shared.LegacyCleanup,'LEGACY_CLEANUP_UNAVAILABLE').RegisterRunner('Lv3Support',function(clean,ack)
  return targets.Exit(clean,'LegacyCleanup',ack)
 end)
end

function SPCLegacyCleanup.StartLv3Effects(P,shared)
 include('RuntimeWork')
 include('Tombstones')
 local batch
 local function readFacts(pid,c) return batch and batch.Facts(pid,c) or shared.EffectiveFacts.Read(pid,c) end
 local data={ready=false,busy=false,errors={},changes=0,observed={}};shared.Lv3Effects=data
 local function isolated(pid) return shared.NetworkIsolation and shared.NetworkIsolation.Active(pid)==true end
 local cultureNames=SPCTombstones.Names('Lv3Culture');local names=SPCTombstones.Names('Lv3Culture')
 for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do names[#names+1]='BUILDING_SPC_DEV_LV3_COM_'..k end
 local function read(c)
  local coefficients={RESEARCH=0,CULTURE=0};local flags={}
  for _,name in ipairs(names) do
   local row=P.Info('Buildings',name);assert(row and row.Index,'B038_DATABASE_MISSING')
   if P.HasBuilding(c:GetBuildings(),row.Index) then
    local k,bit=name:match('_POP_(%u+)_(%d+)$')
    if k then coefficients[k]=coefficients[k]+0.5*2^tonumber(bit)
    else flags[#flags+1]=name:match('_COM_(%u+)$') end
   end
  end
  return coefficients,flags
 end
 function data.WithdrawCulture(c)
  SPCRuntimeWork.RetireOnce(P,shared,c,'Lv3Culture',function()
  for _,name in ipairs(cultureNames)do
   local r=assert(P.Info('Buildings',name),'B038_DATABASE_MISSING')
   local b=c:GetBuildings();local present=P.HasBuilding(b,r.Index);assert(type(present)=='boolean','LV3_CARRIER_UNKNOWN')
   if present then P.RemoveBuilding(b,r.Index);assert(P.HasBuilding(b,r.Index)==false,'LV3_REMOVE_UNCONFIRMED');data.changes=data.changes+1 end
  end
  return 0
  end)
  return true
 end
 local targets=SPCRuntimeWork.NewTargets(P,shared,function(pid,c)
  return SPCRuntimeWork.RetireOnce(P,shared,c,'Lv3Effects',function()
   -- All current outputs are retired; preserve isolation-owned experiment bits.
   for _,name in ipairs(names)do
    if not (isolated(pid) and name:find('_COM_',1,true))then
     local id=assert(P.Info('Buildings',name),'B038_DATABASE_MISSING').Index
     local present=P.HasBuilding(c:GetBuildings(),id);assert(type(present)=='boolean','LV3_CARRIER_UNKNOWN')
     if present then P.RemoveBuilding(c:GetBuildings(),id);assert(P.HasBuilding(c:GetBuildings(),id)==false,'LV3_WRITE_UNCONFIRMED');data.changes=data.changes+1 end
    end
   end
   return 0
  end)
 end,function(pid,cid,why)data.errors[tostring(pid)..':'..cid]=why end)
 function data.Audit(scope) P.Count('audit_lv3');
  if P.Observe then P.Observe('audit','Lv3Effects') end
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true;batch=SPCRuntimeWork.New(P,shared)
  if type(scope)=='table' and scope.load then targets.Run(scope)else targets.Retry(scope)end
  data.busy=false;batch=nil
 end
 -- B137 session-only isolation: this module owns the exact list and native withdrawal.
 function data.ExperimentalNetworkWithdraw(pid)
  assert(isolated(pid),'NETWORK_ISOLATION_NOT_ARMED')
  assert(P.IsTestPlayer(pid),'NETWORK_ISOLATION_PLAYER')
  assert(not data.busy,'NETWORK_ISOLATION_CONSUMER_BUSY')
  data.busy=true
  local ok,why=pcall(function()
   local ids={};for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do ids[#ids+1]='BUILDING_SPC_DEV_LV3_COM_'..k end
   local indexes={};for _,id in ipairs(ids) do
    local r=assert(P.Info('Buildings',id),'NETWORK_ISOLATION_DATABASE:'..id)
    assert(type(r.Index)=='number','NETWORK_ISOLATION_INDEX:'..id);indexes[#indexes+1]=r.Index
   end
   local player=assert(Players[pid],'NETWORK_ISOLATION_PLAYER_MISSING')
   local cities=assert(player:GetCities(),'NETWORK_ISOLATION_CITIES_UNKNOWN')
   for _,c in cities:Members() do
    assert(c:GetOwner()==pid,'NETWORK_ISOLATION_OWNER_CHANGED')
    local b=c:GetBuildings()
    for _,index in ipairs(indexes) do
     local present=P.HasBuilding(b,index);assert(type(present)=='boolean','NETWORK_ISOLATION_CARRIER_UNKNOWN:'..index)
     if present then P.RemoveBuilding(b,index);assert(P.HasBuilding(b,index)==false,'NETWORK_ISOLATION_REMOVE_UNCONFIRMED:'..index);data.changes=data.changes+1 end
    end
   end

  end)
  data.busy=false;data.isolationError=not ok and tostring(why) or nil
  if not ok then error(why) end
  return true
 end
 function data.Describe(pid,c)
  local ok,out=pcall(function()
   local coef,flags=read(c);local pop=c:GetPopulation()
   local f=readFacts(pid,c)
   if f.specialization=='RESEARCH' then return shared.ResearchCross and shared.ResearchCross.Describe(pid,c) or '跨学科研究尚未初始化' end
   local lines={}
   if f.specialization=='CULTURE' then
    return '\n'..(shared.CultureAesthetic and shared.CultureAesthetic.Describe(pid,c) or '风雅熏陶等待确认；旧人口文化已退休。')
   else
    lines[#lines+1]='Commerce specialist +2 per type: '..(#flags>0 and table.concat(flags,',') or 'NONE')
   end
   return '\n'..table.concat(lines,'\n')

  end)
  return (ok and out or ('\nLv3 effects ERROR '..tostring(out)))..'\nLv3 effects status: '..tostring(data.errors[pid..':'..c:GetID()] or (data.ready and 'READY' or 'PENDING'))
 end
 local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit({load=true}) end)
 for _,n in ipairs({'PlayerTurnActivated','CityTransfered','CityPopulationChanged'}) do SPCRuntimeWork.TargetHook(P,Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do SPCRuntimeWork.TargetHook(P,GameEvents,n,data.Audit) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 assert(shared.LegacyCleanup,'LEGACY_CLEANUP_UNAVAILABLE').RegisterRunner('Lv3Effects',function(clean,ack)
  return targets.Exit(clean,'LegacyCleanup',ack)
 end)
end

-- Deferred Research effects still need exact legacy cleanup on the original startup signals.
function SPCLegacyCleanup.StartBoostLoad(P,shared)
 include('RuntimeWork')
 include('BoostConfig')
 include('BoostIntegerConfig')
 local d={ready=false,busy=false,retired=true,errors={},changes=0};shared.NetworkBoost=d
 local function isolated(pid)return shared.NetworkIsolation and shared.NetworkIsolation.Active(pid)==true end
 local testRows={}
 for _,kind in ipairs({'RESEARCH','CULTURE'}) do for _,amount in ipairs({2,4}) do
  testRows[#testRows+1]='BUILDING_SPC_B057_'..kind..'_'..amount
 end end
 local function remove(c,id)
  local row=assert(P.Info('Buildings',id),'B055_DATABASE_MISSING')
  local b=c:GetBuildings()
  local present=P.HasBuilding(b,row.Index)
  assert(type(present)=='boolean','B055_CARRIER_UNKNOWN')
  if present then
   P.RemoveBuilding(b,row.Index)
   assert(P.HasBuilding(b,row.Index)==false,'B055_WRITE_UNCONFIRMED')
   d.changes=d.changes+1
  end
 end
 function d.Clean()
  for _,player in pairs(Players) do local cities=player:GetCities();if cities then for _,c in cities:Members() do P.Count('city_scan');
   for _,r in pairs(SPCBoostConfig.rows) do remove(c,r.building) end
   for _,id in pairs(SPCBoostIntegerConfig.rows) do if P.Info('Buildings',id) then remove(c,id) end end
   for _,id in ipairs(testRows) do if P.Info('Buildings',id) then remove(c,id) end end
  end end end
 end
 function d.EnsureReady(pid)
  if isolated(pid) then return end
  if not P.IsTestPlayer(pid) or d.busy then P.Count('busy_skip');return end
  if not d.ready then
   d.busy=true;local ok,err=pcall(d.Clean);d.busy=false
   if not ok then d.errors[pid]=tostring(err);return end
   d.ready=true
   if SPCExpeditionTrainingDiagnostics then
    local trace=SPCExpeditionTrainingDiagnostics.New(P,'RESEARCH_NETWORK_EXIT')
    trace.Record('NETWORK_EFFECT_RETIRED',{owner=pid,networkKind='RESEARCH',readStatus='VERIFIED',count=d.changes,reason='DEFERRED_V01'})
   end
  end
 end
 -- B137 session-only isolation: this module owns the exact list and native withdrawal.
 function d.ExperimentalNetworkWithdraw(pid)
  assert(isolated(pid),'NETWORK_ISOLATION_NOT_ARMED')
  assert(P.IsTestPlayer(pid),'NETWORK_ISOLATION_PLAYER')
  assert(not d.busy,'NETWORK_ISOLATION_CONSUMER_BUSY')
  d.busy=true
  local ok,why=pcall(function()
   local ids={};for _,r in pairs(SPCBoostConfig.rows) do ids[#ids+1]=r.building end;for _,id in pairs(SPCBoostIntegerConfig.rows) do ids[#ids+1]=id end;for _,id in ipairs(testRows) do ids[#ids+1]=id end
   local indexes={};for _,id in ipairs(ids) do
    local r=assert(P.Info('Buildings',id),'NETWORK_ISOLATION_DATABASE:'..id)
    assert(type(r.Index)=='number','NETWORK_ISOLATION_INDEX:'..id);indexes[#indexes+1]=r.Index
   end
   local player=assert(Players[pid],'NETWORK_ISOLATION_PLAYER_MISSING')
   local cities=assert(player:GetCities(),'NETWORK_ISOLATION_CITIES_UNKNOWN')
   for _,c in cities:Members() do
    assert(c:GetOwner()==pid,'NETWORK_ISOLATION_OWNER_CHANGED')
    local b=c:GetBuildings()
    for _,index in ipairs(indexes) do
     local present=P.HasBuilding(b,index);assert(type(present)=='boolean','NETWORK_ISOLATION_CARRIER_UNKNOWN:'..index)
     if present then P.RemoveBuilding(b,index);assert(P.HasBuilding(b,index)==false,'NETWORK_ISOLATION_REMOVE_UNCONFIRMED:'..index);d.changes=d.changes+1 end
    end
   end
   d.errors[pid]=nil
  end)
  d.busy=false;d.isolationError=not ok and tostring(why) or nil
  if not ok then error(why) end
  return true
 end
 function d.Describe()
  return '科研网络鼓舞已按用户决定在 v0.1 隔离，重做留待后续。\n公共网络和科研本城能力保留。\n旧载体清理：'..(d.ready and '已确认' or '待完成')
 end
 local function hook(src,n,fn) local e=P.Field(src,n);if e and e.Add then e.Add(fn) end end
 -- The earlier publish fallback is only a Research attempt.
 -- Great Work cleanup waits for load close or an actual supported turn.
 local attempted,initializing=false,false
 local function initialize(afterLoad)
  local cleanup=afterLoad and shared.GreatWorkLoadCleanup or nil
  if initializing or d.busy or (d.ready and (not cleanup or cleanup.ready)) then return end
  local pid=Game.GetLocalPlayer()
  if not P.IsTestPlayer(pid)then return end
  attempted=true;initializing=true
  local ok,err=pcall(function()
   d.EnsureReady(pid)
   if cleanup and not cleanup.ready then cleanup.Clean()end
  end)
  initializing=false
  if not ok then print('[SPC][B055][INIT] '..tostring(err))end
 end
 hook(Events,'LoadScreenClose',function()initialize(true)end)
 hook(Events,'GameCoreEventPublishComplete',function()if not attempted then initialize(false)end end)
 hook(Events,'PlayerTurnActivated',function(pid)if P.IsTestPlayer(pid)then initialize(true)end end)
end

-- The old Dialogue carriers are removed before applying the current Tourism projection.
function SPCLegacyCleanup.InstallDialogueLoad(P,d,eraCount)
 local function remove(c,id)
  local row=assert(P.Info('Buildings',id),'DIALOGUE_DATABASE_MISSING');local b=c:GetBuildings()
  if P.HasBuilding(b,row.Index)~=false then
   P.RemoveBuilding(b,row.Index)
   assert(P.HasBuilding(b,row.Index)==false,'DIALOGUE_WRITE_FAILED');d.changes=d.changes+1
  end
 end
 function d.Init()
  if d.ready then return end
  assert(not d.initializing,'DIALOGUE_INIT_BUSY');d.initializing=true
  local ok,why=pcall(function()
   for _,p in pairs(Players) do local cities=p:GetCities();if cities then for _,c in cities:Members() do P.Count('city_scan');
    for n=2,eraCount do local id='BUILDING_SPC_B059_D'..n;if P.Info('Buildings',id) then remove(c,id) end end
    for _,v in ipairs({25,50,100,200}) do local id='BUILDING_SPC_B059_TEST'..v;if P.Info('Buildings',id) then remove(c,id) end end
    for _,m in ipairs({'CITY','OBJECT'}) do local id='BUILDING_SPC_B055_GW_'..m;if P.Info('Buildings',id) then remove(c,id) end end
   end end end
  end)
  d.initializing=false -- Only the invocation which acquired this lock releases it.
  if not ok then error(why)end
  d.ready=true
 end
end

function SPCLegacyCleanup.Start(P,shared)
 local store=assert(shared.CityProgressionStore,'LEGACY_STORE_UNAVAILABLE')
 assert(type(store.IsExitCurrent)=='function'and type(store.ExitCompleted)=='function','LEGACY_EXIT_PROOF_UNAVAILABLE')
 local d={};shared.LegacyCleanup=d
 local keys=SPCLegacyCleanupCatalog.Keys();local runners,posts={},{}
 local ledger=setmetatable({},{__mode='k'}) -- values contain no ticket, function or native object
 local requiresRunner={Lv3Support=true,Lv3Effects=true}
 local function text(value)local ok,s=pcall(tostring,value);return ok and type(s)=='string'and s:sub(1,180)or'LEGACY_GROUP_FAILED'end
 local function current(c,loss,ticket,slot)
  assert(store.IsExitCurrent('LegacyCleanup',c,loss,ticket,slot)==true,'LEGACY_EXIT_CHANGED')
 end
 local function state(ticket)
  assert(type(ticket)=='table','LEGACY_TICKET_INVALID')
  local s=ledger[ticket];if not s then s={done={},errors={},running={},awaiting={}};ledger[ticket]=s end;return s
 end
 local function allDone(s,except)
  for _,key in ipairs(keys)do if key~=except and not s.done[key]then return false end end;return true
 end
 function d.RegisterRunner(key,fn)
  assert(requiresRunner[key]and type(fn)=='function'and not runners[key],'LEGACY_RUNNER_REGISTRATION_INVALID');runners[key]=fn
 end
 function d.RegisterPostCleanup(key,fn)
  assert(key=='Dialogue'and type(fn)=='function'and not posts[key],'LEGACY_POST_REGISTRATION_INVALID');posts[key]=fn
 end
 local function read(c,loss,ticket,slot,fn)
  local ok,value=pcall(fn);current(c,loss,ticket,slot)
  if not ok then error(value,0)end;return value
 end
 local function descriptor(key,c,loss,ticket,slot)
  if key=='NetworkBoost'then
   if not SPCBoostConfig then include('BoostConfig')end
   if not SPCBoostIntegerConfig then include('BoostIntegerConfig')end
   current(c,loss,ticket,slot)
   return SPCLegacyCleanupCatalog.Group(key,nil,SPCBoostConfig and SPCBoostConfig.rows,SPCBoostIntegerConfig and SPCBoostIntegerConfig.rows)
  elseif key=='Dialogue'then
   local n=read(c,loss,ticket,slot,function()local count=0;for _ in GameInfo.Eras()do count=count+1 end;return count end)
   return SPCLegacyCleanupCatalog.Group(key,n)
  end
  return SPCLegacyCleanupCatalog.Group(key)
 end
 local function physical(key,c,loss,ticket,slot)
  local s=state(ticket)
  assert(not s.running[key],'LEGACY_GROUP_BUSY');s.running[key]=true
  local ok,why=pcall(function()
   current(c,loss,ticket,slot);s.done[key]=nil;s.awaiting[key]=nil
   local row=descriptor(key,c,loss,ticket,slot)
   if row.kind=='plot_flags'then
    local plot=read(c,loss,ticket,slot,function()return Map.GetPlot(c:GetX(),c:GetY())end);assert(plot,'LEGACY_PLOT_UNKNOWN')
    for _,name in ipairs(row.names)do
     local value=read(c,loss,ticket,slot,function()return plot:GetProperty(name)end)
     if value~=nil and value~=0 then
      current(c,loss,ticket,slot);P.SetProperty(plot,name,0);current(c,loss,ticket,slot)
      assert(read(c,loss,ticket,slot,function()return plot:GetProperty(name)end)==0,'LEGACY_PLOT_WRITE_UNCONFIRMED')
     end
    end
   else
    local catalog=read(c,loss,ticket,slot,function()return GameInfo and GameInfo.Buildings end);assert(catalog~=nil,'LEGACY_BUILDINGS_UNAVAILABLE')
    local readable=read(c,loss,ticket,slot,function()
     local iterator,source,key=catalog();assert(type(iterator)=='function','LEGACY_BUILDINGS_UNAVAILABLE')
     local first=iterator(source,key);return first~=nil and type(first.BuildingType)=='string'and #first.BuildingType>0
    end)
    assert(readable,'LEGACY_BUILDINGS_UNAVAILABLE') -- one readiness row, never a full catalogue scan
    local buildings=read(c,loss,ticket,slot,function()return c:GetBuildings()end);assert(buildings,'LEGACY_BUILDINGS_UNAVAILABLE')
    local rows,seen={},{}
    for _,name in ipairs(row.names)do
     local definition=read(c,loss,ticket,slot,function()return catalog[name]end)
     if definition~=nil then
      local v=read(c,loss,ticket,slot,function()return {id=definition.Index,internal=definition.InternalOnly}end)
      assert((v.internal==true or v.internal==1)and type(v.id)=='number'and v.id>=0 and v.id%1==0 and not seen[v.id],'LEGACY_DEFINITION_INVALID');seen[v.id]=true
      local has=read(c,loss,ticket,slot,function()return P.HasBuilding(buildings,v.id)end);assert(type(has)=='boolean','LEGACY_PRESENCE_UNKNOWN')
      rows[#rows+1]={id=v.id,has=has}
     end -- only a successful exact native lookup returning nil proves absence
    end
    for _,v in ipairs(rows)do if v.has then
     current(c,loss,ticket,slot);P.RemoveBuilding(buildings,v.id);current(c,loss,ticket,slot)
     assert(read(c,loss,ticket,slot,function()return P.HasBuilding(buildings,v.id)end)==false,'LEGACY_REMOVE_UNCONFIRMED')
    end end
   end
   if key=='Dialogue'then
    local post=assert(posts[key],'LEGACY_POST_UNAVAILABLE');assert(post(c,loss)~=false,'LEGACY_POST_UNCONFIRMED');current(c,loss,ticket,slot)
   end
  end)
  s.running[key]=nil
  if not ok then error(why,0)end
  current(c,loss,ticket,slot);return true
 end
 local function complete(key,c,loss,ticket,slot,proved)
  if not proved then return false end
  local s=state(ticket);local attempt={};s.awaiting[key]=attempt
  local ok,value=pcall(function()
   current(c,loss,ticket,slot)
   if s.awaiting[key]~=attempt then return false end
   if not s.sweeping and allDone(s,key)then
    local function confirmed()
     return ledger[ticket]==s and s.awaiting[key]==attempt and allDone(s,key)and(not slot or slot())
    end
    if store.ExitCompleted('LegacyCleanup',c,loss,ticket,confirmed)~=true then return false end
   end
   if s.awaiting[key]~=attempt then return false end
   s.done[key]=attempt;s.errors[key]=nil;return true
  end)
  if s.awaiting[key]==attempt then s.awaiting[key]=nil end
  return ok and value==true
 end
 local function runGroup(key,c,loss,ticket)
  local proved=false
  local function clean(city,proof,cap,slot)proved=false;physical(key,city,proof,cap,slot);proved=true;return true end
  if requiresRunner[key]then
   local factory=assert(runners[key],'LEGACY_RUNNER_UNAVAILABLE')
   local fn=factory(clean,function(city,proof,cap,slot)return complete(key,city,proof,cap,slot,proved)end)
   assert(type(fn)=='function','LEGACY_RUNNER_INVALID');assert(fn(c,loss,ticket)~=false,'LEGACY_RUNNER_UNCONFIRMED')
  else
   clean(c,loss,ticket);assert(complete(key,c,loss,ticket,nil,proved),'LEGACY_GROUP_UNCONFIRMED')
  end
 end
 function d.Exit(c,loss,ticket)
  local s=state(ticket);assert(not s.sweeping,'LEGACY_SWEEP_BUSY');s.sweeping=true
  local ok,why=pcall(function()
   current(c,loss,ticket)
   for _,key in ipairs(keys)do if not s.done[key]then
    local good,value=pcall(function()assert(not s.awaiting[key],'LEGACY_GROUP_BUSY');runGroup(key,c,loss,ticket)end)
    if not good then s.errors[key]=text(value)end
    current(c,loss,ticket)
   end end
   local pending={};for _,key in ipairs(keys)do if not s.done[key]then pending[#pending+1]=key end end
   assert(#pending==0,'LEGACY_GROUP_PENDING '..table.concat(pending,','))
   assert(store.ExitCompleted('LegacyCleanup',c,loss,ticket,function()return ledger[ticket]==s and allDone(s)end)==true,'LEGACY_ACK_UNCONFIRMED')
  end)
  s.sweeping=false
  if not ok then error(why,0)end;return true
 end
 return d
end
