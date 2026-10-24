-- B271 observational only. Bounded plain scalar state, never persisted.
SPCEventTimingDiagnostics={ENABLED=false,TURN_LIMIT=6,EVENT_LIMIT=400,SEQUENCE_ENABLED=false}
local M=SPCEventTimingDiagnostics
-- Union of current native subscriptions, including guarded optional names.
-- SystemUpdateUI is deliberately excluded: no new frame listener.
local catalog={Events={'CapitalCityChanged','CityBuildQueueChanged','CityBuildingsChanged','CityConquered','CityInitialized','CityLiberated','CityProductionChanged','CityProductionQueueChanged','CityProductionUpdated','CityProjectCompleted','CitySelectionChanged','CityYieldChanged','CityYieldsChanged','CulturalIdentityCityConverted','DiplomacyDealEnacted','DiplomacyDeclareWar','EndTurnBlockingChanged','EndTurnDirty','FeatureAddedToMap','FeatureRemovedFromMap','GreatWorkCreated','GreatWorkMoved','ImprovementAddedToMap','ImprovementRemovedFromMap','InterfaceModeChanged','NotificationAdded','NotificationDismissed','PlayerTurnStartComplete','ResearchChanged','ResourceAddedToMap','ResourceRemovedFromMap','TradeRoutePlundered','UnitAddedToMap','UnitCommandStarted','UnitMovementPointsChanged','UnitOperationAdded','UnitOperationSegmentComplete','UserOptionChanged','BuildingAddedToMap','BuildingPillaged','BuildingRemovedFromMap','BuildingRepaired','CityAddedToMap','CityFocusChanged','CityPopulationChanged','CityProductionCompleted','CityRemovedFromMap','CityTileOwnershipChanged','CityTransfered','CityWorkerChanged','CivicCompleted','DistrictAddedToMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRemovedFromMap','DistrictRepaired','GameCoreEventPlaybackComplete','GameCoreEventPublishComplete','GovernmentChanged','GovernmentPolicyChanged','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','LoadScreenClose','LocalPlayerChanged','LocalPlayerTurnBegin','LocalPlayerTurnEnd','PlayerTurnActivated','PlayerTurnDeactivated','ResearchCompleted','SpyMissionCompleted','TradeRouteActivityChanged','TradeRouteAddedToMap','TradeRouteRemovedFromMap','UnitActivityChanged','UnitMoveComplete','UnitOperationDeactivated','UnitOperationStarted','UnitOperationsCleared','UnitRemovedFromMap','UnitSelectionChanged','UnitTeleported'},GameEvents={'OnBuildingConstructed','BuildingConstructed','BuildingPillageStateChanged','CityBuilt','OnCityPopulationChanged','OnDistrictConstructed','OnPillage','PlayerTurnStarted'}}

local function safeRead(o,k)
 local ok,v=pcall(function()if not o or type(o[k])~='function'then return 'UNAVAILABLE'end;return o[k](o)end)
 if not ok then return 'READ_ERROR'end
 if type(v)=='number' and v==v and v>-math.huge and v<math.huge then return v end
 return v=='UNAVAILABLE' and v or 'UNKNOWN'
end
local function state()return ExposedMembers.SPC_EventTiming end
local function tick(s)s.seq=s.seq+1;return s.seq end
local function emit(trace,s,stage,data)
 if s.emitting then return end
 data.observationEpoch=s.epoch;data.observationSeq=data.observationSeq or tick(s)
 data.observationCycle=s.cycle;data.lastVerifiedSeq=data.lastVerifiedSeq or s.lastVerified
 s.emitting=true;pcall(trace.Record,stage,data);s.emitting=false
end
function M.Start(P,shared,side)
 -- B307: stop A/B/C before allocating trace state or registering any observer.
 -- This is a load-time switch; the UI sequence toggle cannot enable the probe.
 if not M.ENABLED then
  ExposedMembers.SPC_EventTiming=nil
  if shared then shared.EventTiming=nil end
  return nil
 end
 if side=='GAMEPLAY'then
  ExposedMembers.SPC_EventTiming={epoch=tostring({}):gsub('[^%w]',''),seq=0,cycle=0,turns={},turnCount=0,
   accepting=true,sequenceEnabled=M.SEQUENCE_ENABLED,lastVerified=0,counts={audit={},dispatch={}},sides={}}
 end
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'EVENT_TIMING_'..side)
 local hooks={};local missing={};local localState={rows={},total=0,publish=0,active=false,seen={},lastCounts={audit={},dispatch={}}}
 local function eligible()
  local s=state();local pid=Game.GetLocalPlayer()
  if not s then return nil end
  if not P.IsTestPlayer(pid)then s.accepting=false;return nil end
  local t=Game.GetCurrentGameTurn()
  if not s.turns[t]then
   if s.turnCount>=M.TURN_LIMIT then s.accepting=false;return nil end
   s.turns[t]=true;s.turnCount=s.turnCount+1
  end
  if not s.accepting then return nil end
  if localState.epoch~=s.epoch then
   localState={epoch=s.epoch,rows={},total=0,publish=0,active=false,seen={},lastCounts={audit={},dispatch={}}}
   s.sides[side]=localState
  end
  return s,pid,t
 end
 local function flush(s)
  if #localState.rows==0 then return end
  emit(trace,s,'EVENT_ORDER_BATCH',{observerSide=side,eventBatch=table.concat(localState.rows,'|'),eventCount=#localState.rows,eventTotal=localState.total})
  localState.rows={}
 end
 local function close(s,reason)
  if not localState.active then return end
  flush(s);localState.active=false
  emit(trace,s,'EVENT_ORDER_END',{observerSide=side,eventTotal=localState.total,eventPublishCount=localState.publish,eventTruncated=reason=='LIMIT' or reason=='WINDOW_EXPIRED',reason=reason,observerErrors=s.observerErrors or 0})
 end
 local function counts(s,point)
  local out={}
  for _,group in ipairs({'dispatch','audit'})do
   local rows,total,other={},0,0
   for k,n in pairs(s.counts[group])do
    local delta=n-(localState.lastCounts[group][k] or 0);localState.lastCounts[group][k]=n
    total=total+delta;if k=='OTHER'then other=delta end
    if delta>0 then rows[#rows+1]={k,delta}end
   end
   table.sort(rows,function(a,b)return a[2]>b[2] or a[2]==b[2] and a[1]<b[1]end)
   local shown=0;local limit=group=='audit' and 32 or 8
   for i=1,math.min(limit,#rows)do local v=rows[i];out[#out+1]=group..':'..v[1]..':'..v[2];shown=shown+v[2]end
   out[#out+1]=group..':TOTAL:'..total;out[#out+1]=group..':OTHER_TOTAL:'..other;out[#out+1]=group..':REST:'..(total-shown)
  end
  emit(trace,s,'TURN_EVENT_COUNTS',{point=point,observerSide=side,counterBatch=table.concat(out,'|')})
 end
 local function sample(s,pid,t,point)
  local k=t..':'..point;if localState.seen[k]then return end;localState.seen[k]=true
  local treasury;pcall(function()treasury=Players[pid]:GetTreasury()end)
  local net=shared.NetworkBridge;local b=net and net.players and net.players[pid]
  emit(trace,s,'TREASURY_POINT',{owner=pid,point=point,goldBalance=safeRead(treasury,'GetGoldBalance'),goldYield=safeRead(treasury,'GetGoldYield'),
   networkAvailability=b and b.availability or 'UNAVAILABLE',networkRevalidation=b and b.revalidation or 'UNAVAILABLE',observerSide=side})
 end
 local function observe(namespace,name,a,b,c,d)
  local s=state();if not s or s.emitting then return end
  -- No engine reads on ordinary events unless the bounded order window is active.
  local boundary=name=='PlayerTurnActivated' or name=='PlayerTurnDeactivated' or name=='LocalPlayerTurnBegin' or name=='LocalPlayerTurnEnd' or name=='PlayerTurnStarted'
  if not boundary and not localState.active and not (localState.afterBegin and name=='GameCoreEventPublishComplete') then return end
  local pid,t
  if boundary then s,pid,t=eligible()else
   if not s.accepting then close(s,'WINDOW_EXPIRED');return end
   pid=Game.GetLocalPlayer();t=Game.GetCurrentGameTurn()
  end
  if not s then local old=state();if old then close(old,'WINDOW_EXPIRED')end;return end
  local isLocal=a==pid
  local ending=name=='PlayerTurnDeactivated' and isLocal or name=='LocalPlayerTurnEnd'
  if ending and localState.endTurn~=t then
   localState.endTurn=t;localState.waitAI=true
   if side=='GAMEPLAY'then s.cycle=s.cycle+1 end
   if s.sequenceEnabled then
    localState.rows={};localState.total=0;localState.publish=0;localState.active=true
    emit(trace,s,'EVENT_ORDER_START',{observerSide=side,reason='LOCAL_END',eventCount=#hooks})
    for i=1,#missing,12 do
     local batch={};for j=i,math.min(i+11,#missing)do batch[#batch+1]=missing[j]end
     emit(trace,s,'EVENT_ORDER_HOOKS',{observerSide=side,point='UNAVAILABLE_HOOKS',eventBatch=table.concat(batch,'|')})
    end
   end
  end
  if localState.active then
   if not s.sequenceEnabled then close(s,'DISABLED')
   elseif name=='GameCoreEventPublishComplete'then localState.publish=localState.publish+1;flush(s)
   else
    local owner,city='UNKNOWN','UNKNOWN'
    if name=='LocalPlayerTurnBegin' or name=='LocalPlayerTurnEnd'then owner=pid end
    if name=='PlayerTurnActivated' or name=='PlayerTurnDeactivated' or name=='PlayerTurnStarted' or name=='CityWorkerChanged' or name=='CityPopulationChanged'then
     if type(a)=='number'then owner=a end
     if (name=='CityWorkerChanged' or name=='CityPopulationChanged') and type(b)=='number'then city=b end
    end
    localState.total=localState.total+1
    localState.rows[#localState.rows+1]=table.concat({tick(s),namespace..'.'..name,owner,city,t},':')
    if #localState.rows>=12 then flush(s)end
    if localState.total>=M.EVENT_LIMIT then close(s,'LIMIT')end
   end
  end
  if side=='GAMEPLAY'then
   if name=='PlayerTurnDeactivated' and isLocal then sample(s,pid,t,'LOCAL_DEACTIVATED');if localState.countEnd~=t then localState.countEnd=t;counts(s,'LOCAL_END')end
   elseif name=='PlayerTurnActivated' and not isLocal and localState.waitAI then localState.waitAI=false;sample(s,pid,t,'FIRST_FOREIGN_ACTIVATED')
   elseif name=='PlayerTurnStarted' and isLocal then sample(s,pid,t,'GAME_PLAYER_STARTED')
   elseif name=='PlayerTurnActivated' and isLocal then sample(s,pid,t,'LOCAL_ACTIVATED');if localState.countTurn~=t then localState.countTurn=t;counts(s,'LOCAL_BEGIN')end
   elseif name=='LocalPlayerTurnBegin'then sample(s,pid,t,'LOCAL_BEGIN');localState.afterBegin=true
   elseif name=='GameCoreEventPublishComplete' and localState.afterBegin then localState.afterBegin=false;sample(s,pid,t,'FIRST_PUBLISH_AFTER_BEGIN')end
  end
  if name=='LocalPlayerTurnBegin'then close(s,'LOCAL_BEGIN')end
 end
 for _,ns in ipairs({'Events','GameEvents'})do
  local source=ns=='Events' and Events or GameEvents
  for _,name in ipairs(catalog[ns])do
   local okField,e=pcall(P.Field,source,name);if not okField then e=nil end
   if e and type(e.Add)=='function'then
    local callback=function(...)local ok=pcall(observe,ns,name,...);if not ok then local s=state();if s then s.observerErrors=(s.observerErrors or 0)+1 end end end
    local ok=pcall(e.Add,callback);if ok then hooks[#hooks+1]={e,callback}else missing[#missing+1]=ns..'.'..name end
   else missing[#missing+1]=ns..'.'..name end
  end
 end
 local api={}
 function api.Toggle(pid)
  local s=state();if not s or not P.IsTestPlayer(pid)then return '仅测试玩家可使用'end
  if not s.accepting then return '本次加载的6回合观察窗口已结束；重新载入后可开启。'end
  s.sequenceEnabled=not s.sequenceEnabled
  return '事件顺序记录：'..(s.sequenceEnabled and '开启；从下一次本地回合结束观察' or '关闭')..'。每侧最多400条，仅本次加载前6个本地回合。'
 end
 function api.Verified(pid,b)
  local s=state();if not s or not s.accepting or not P.IsTestPlayer(pid)then return end
  if s.turnCount>=M.TURN_LIMIT and not s.turns[Game.GetCurrentGameTurn()]then s.accepting=false;return end
  s.lastVerified=tick(s)
  emit(trace,s,'TIMING_NETWORK_VERIFIED',{owner=pid,observationSeq=s.lastVerified,networkAvailability=b.availability,networkRevalidation=b.revalidation})
 end
 function api.Stop()for _,h in ipairs(hooks)do if h[1].Remove then pcall(h[1].Remove,h[2])end end end
 if side=='GAMEPLAY'then shared.EventTiming=api end
 return api
end
