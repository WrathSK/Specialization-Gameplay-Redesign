-- B202: bounded admission adapter. Native production owns cost/progress/copy
-- history; this UI never spawns, destroys or teleports the trained unit.
if include then include('ExpeditionTrainingDiagnostics')end
SPCExpeditionTrainingUI={KIND='UNIT_SPC_EXPEDITION_SPY'}
function SPCExpeditionTrainingUI.New(P,send,notify,build)
 local M=SPCExpeditionTrainingUI;local api={};local pending;local selected;local sync;local view;local attempted,covered;local source;local cause=0;local closed=false;local pumping=false;local activeCity;local selectionDeferred=false;local diagnosticRowKey
 local diag=SPCExpeditionTrainingDiagnostics and SPCExpeditionTrainingDiagnostics.New(P,'PRODUCTION_UI')
 local function observe(stage,c,extra)if diag then pcall(diag.Event,stage,c,nil,extra)end end
 -- Scalar provenance only; admission never depends on these diagnostic fields.
 if diag then pcall(function()ExposedMembers.SPC_B205TrainingTrace.bridge=diag.id end)end
 local function request(action,c,reservation,id)
  ExposedMembers.SPC_ExpeditionTrainingSequence=(ExposedMembers.SPC_ExpeditionTrainingSequence or 0)+1
  local token='TRAIN:'..P.VERSION..':'..ExposedMembers.SPC_ExpeditionTrainingSequence
  local packet={OnStart='SPC_ExpeditionTrainingRequest',Action=action,Token=token,CityID=id or c:GetID(),Reservation=reservation}
  return token,packet
 end
 local function transmit(pid,p)send(pid,PlayerOperations.EXECUTE_SCRIPT,p)end
 local function city(pid,id)return Players[pid] and Players[pid]:GetCities():FindID(id)end
 local function localCity(c)
  if closed or not c then return false end
  local owner=c:GetOwner();if closed then return false end
  local pid=Game.GetLocalPlayer();if closed or owner~=pid then return false end
  local allowed=P.IsTestPlayer(owner);return not closed and allowed
 end
 ExposedMembers.SPC_ExpeditionQueueRead=function(pid,id)
  if closed then return nil end
  local c=assert(city(pid,id),'TRAINING_CITY_UNREADABLE');assert(c:GetOwner()==pid)
  local q=c:GetBuildQueue();local n=q:GetSize();assert(type(n)=='number' and n>=0 and n<=100,'TRAINING_QUEUE_SIZE_UNKNOWN')
  local count=0
  for i=0,n-1 do
   local e=assert(q:GetAt(i),'TRAINING_QUEUE_ENTRY_UNKNOWN')
   if e.Directive==CityProductionDirectives.TRAIN then
    local r=assert(GameInfo.Units[e.UnitType],'TRAINING_QUEUE_TYPE_UNKNOWN')
    if r.UnitType==M.KIND then count=count+1 end
   end
  end
  return {owner=pid,city=id,turn=Game.GetCurrentGameTurn(),count=count,
   _b205_context=diag and diag.id,_b205_load=diag and diag.loads}
 end
 local function field(o,k)return type(o)=='table'and o[k]or nil end
 local function sources()
  local b=ExposedMembers.SPC_P0;local store=field(b,'CityProgressionStore');local facts=field(b,'EffectiveFacts')
  local gate=field(b,'ExpeditionGate');local training=field(gate,'Training');local owner=field(b,'ExpeditionTraining')
  return {backend=b,store=store,storeRead=field(store,'TrainingInputStamp'),facts=facts,factsRead=field(facts,'Read'),
   issuer=field(facts,'TrainingObservationIssuer'),gate=gate,training=training,capacity=field(training,'CapacityInputStamp'),
   available=field(training,'Available'),gateRead=field(training,'Read'),owner=owner,request=field(owner,'Request'),
   begin=field(store,'BeginTrainingBindingObservation'),finish=field(store,'FinishTrainingBindingObservation')}
 end
 local function sameSource(a)
  local b=ExposedMembers.SPC_P0
  return a and rawequal(b,a.backend)and rawequal(field(b,'CityProgressionStore'),a.store) and field(a.store,'TrainingInputStamp')==a.storeRead
   and rawequal(field(b,'EffectiveFacts'),a.facts) and field(a.facts,'Read')==a.factsRead and rawequal(field(a.facts,'TrainingObservationIssuer'),a.issuer)
   and rawequal(field(b,'ExpeditionGate'),a.gate)and rawequal(field(a.gate,'Training'),a.training) and field(a.training,'CapacityInputStamp')==a.capacity
   and field(a.training,'Available')==a.available and field(a.training,'Read')==a.gateRead and rawequal(field(b,'ExpeditionTraining'),a.owner)
   and field(a.owner,'Request')==a.request and field(a.store,'BeginTrainingBindingObservation')==a.begin
   and field(a.store,'FinishTrainingBindingObservation')==a.finish
 end
 local function integer(v)return type(v)=='number'and v==v and v>=0 and v<1000000000 and v%1==0 end
 local function reference(c)
  if not localCity(c)then return nil end
  local owner=c:GetOwner();if closed then return nil end
  local id=c:GetID();if closed then return nil end
  local x=c:GetX();if closed then return nil end
  local y=c:GetY();if closed then return nil end
  local turn=Game.GetCurrentGameTurn();if closed then return nil end
  local r={owner=owner,city=id,x=x,y=y,turn=turn}
  if not(integer(r.owner)and integer(r.city)and integer(r.x)and integer(r.y)and integer(r.turn))then return nil end
  return r
 end
 local function sameReference(a,b)
  return a and b and a.owner==b.owner and a.city==b.city and a.x==b.x and a.y==b.y and a.turn==b.turn
 end
 local function pureRead(fn,fallback,limit,...)
  if type(fn)~='function'then return fallback end
  local ok,v=pcall(fn,...);return ok and type(v)=='string'and #v<=limit and v or fallback
 end
 local function signature(a,r)
  local banner=field(field(a.backend,'LevelBanners'),'views');local f=field(banner,r.owner..':'..r.city)or {}
  local base=table.concat({r.owner,r.city,r.x,r.y,r.turn,cause,
   tostring(field(ExposedMembers.SPC_ExpeditionActivity,'revision')),tostring(f.specialization),tostring(f.potential),tostring(f.active),tostring(f.activeStatus)},'|')
  local store=pureRead(a.storeRead,'STORE_INPUT_UNAVAILABLE',4096,r.owner,r.city,r.x,r.y)
  local capacity=pureRead(a.capacity,'CAPACITY_INPUT_UNAVAILABLE',1024,r.owner)
  return base..'|'..#store..':'..store..'|'..#capacity..':'..capacity,base,store,capacity
 end
 local function consume(r)
  local reply=ExposedMembers.SPC_ExpeditionTrainingReply;local wait=sync
  if not wait or not reply or reply.token~=wait.token then return end
  sync=nil;view=nil;covered=nil -- consume before notify/reentry
  local input=reply.input;local key,base,store,capacity=signature(source,r)
  if closed then return end
  if wait.source==source and sameSource(source)and sameReference(wait.reference,r)and reply.owner==r.owner and reply.city==r.city
   and type(input)=='table'and input.version==1 and input.owner==r.owner and input.cityID==r.city and input.x==r.x and input.y==r.y
   and input.turn==r.turn and base==wait.base and input.storeInput==store and input.capacityInput==capacity then
   view={city=r.city,eligible=reply.eligible==true};covered=key;attempted=key
   if diag then pcall(diag.Record,'TRAINING_UI_APPLIED',{owner=r.owner,city=r.city,requestKey=reply.token,eligibility=reply.eligible})end
  end
  notify(r.owner,r.city)
 end
 local function syncCity(c)
  local entered=cause;local r=reference(c)
  if closed or entered~=cause then return end
  if not r then selected=nil;source=nil;sync=nil;view=nil;attempted=nil;covered=nil;return end
  if not sameReference(selected,r)or not sameSource(source)then
   selected=r;source=sources();sync=nil;view=nil;attempted=nil;covered=nil
  else r=selected end
  consume(r) -- both render and publication accept the covered reply before deciding to re-SYNC
  if closed or selected~=r or selectionDeferred then return end
  local key,base=signature(source,r)
  if closed or selected~=r or selectionDeferred or not sameSource(source)then return end
  if covered~=key then view=nil;covered=nil end
  if pending then return end
  if sync and(sync.source~=source or sync.key~=key)then sync=nil end
  if sync or attempted==key then return end
  local token,packet=request('SYNC',c,nil,r.city)
  attempted=key;sync={token=token,owner=r.owner,city=r.city,reference=r,source=source,key=key,base=base}
  transmit(r.owner,packet)
  if not closed and selected==r and sameSource(source)then consume(r)end
 end
 function api.Sync(c)
  if closed then return end
  if pumping then
   if not rawequal(c,activeCity)then cause=cause+1;selectionDeferred=true end
   return
  end
  pumping=true;activeCity=c;selectionDeferred=false
  local ok,err=pcall(syncCity,c);pumping=false;activeCity=nil
  if not ok then error(err,0)end
 end
 function api.Items(data)
  if closed then return end
  local c=data.City;if not localCity(c)then return end
  api.Sync(c)
  local items={};for _,v in ipairs(data.UnitItems or {})do if v.Type~=M.KIND then items[#items+1]=v end end
  data.UnitItems=items
  if not selected or selected.owner~=c:GetOwner()or selected.city~=c:GetID()or selected.x~=c:GetX()or selected.y~=c:GetY()then
   cause=cause+1;selectionDeferred=true;return
  end
  if selectionDeferred or not sameSource(source)or covered~=signature(source,selected)then view=nil;covered=nil;return end
  if not view or view.city~=selected.city or not view.eligible then return end
  local renderReference,renderSource,renderView,renderCovered=selected,source,view,covered
  local function current()return not closed and selected==renderReference and source==renderSource and view==renderView
   and sameSource(source)and covered==renderCovered and covered==signature(source,selected)end
  local r=GameInfo.Units[M.KIND];if not r then return end
  local q=c:GetBuildQueue();if not current()then return end
  local nativeCost=q:GetUnitCost(r.Index);if not current()then return end
  -- Reuse the displayed cost. One disposable selected-row key avoids repeated
  -- diagnostic native reads on unchanged renders, including pre-training reads.
  if diag then pcall(function()
   local trace=ExposedMembers.SPC_B205TrainingTrace or {};local roles=trace.roles or {}
   local key=table.concat({c:GetID(),Game.GetCurrentGameTurn(),r.Index or -1,r.Cost or -1,
    nativeCost or -1,trace.loadSequence or 0,roles.GAMEPLAY or '-',roles.LOG_UI or '-'},':')
   if key~=diagnosticRowKey then
    diagnosticRowKey=key;observe('UI_ROW',c,{nativeCost=nativeCost})
   end
  end)end
  local tooltip=Locale.Lookup('LOC_SPC_EXPEDITION_TRAINING_HELP')..(ExposedMembers.SPC_ExpeditionTrainingUIError and ('[NEWLINE]'..Locale.Lookup('LOC_SPC_EXPEDITION_SPY_TRAINING_ERROR',ExposedMembers.SPC_ExpeditionTrainingUIError))or '')
  if not current()then return end
  local turns=q:GetTurnsLeft(r.Hash);if not current()then return end
  local progress=q:GetUnitProgress(r.Index);if not current()then return end
  local production=q:GetCurrentProductionTypeHash();if not current()then return end
  local final=reference(c);if not sameReference(final,renderReference)or not current()then return end
  items[#items+1]={Index=r.Index,Type=r.UnitType,Name=r.Name,Hash=r.Hash,Kind='KIND_UNIT',
   ToolTip=tooltip,TurnsLeft=turns,Disabled=pending~=nil,Civilian=true,Cost=nativeCost,Progress=progress,
   Corps=false,Army=false,CorpsCost=0,ArmyCost=0,CorpsTurnsLeft=1,ArmyTurnsLeft=1,
   CorpsTooltip="",ArmyTooltip="",CorpsName="",ArmyName="",ReligiousStrength=r.ReligiousStrength or 0,
   IsCurrentProduction=production==r.Hash,SortIndex=999}
 end
 function api.Before(c,item,queueSelected)
  if closed then return not(item and item.Type==M.KIND)end
  if not item or item.Type~=M.KIND then return true end
  if not localCity(c) or pending or queueSelected then return false end
  observe('UI_ORDER_BEFORE',c)
  local token,packet=request('RESERVE',c)
  if closed then return false end
  pending={owner=c:GetOwner(),city=c:GetID(),token=token,item=item,stage='RESERVE',turn=Game.GetCurrentGameTurn(),attempts=0}
  transmit(c:GetOwner(),packet);return false
 end
 function api.CancelQueue(c,index)
  if closed then return end
  if not localCity(c)then return end
  local e=c:GetBuildQueue():GetAt(index);local r=e and e.Directive==CityProductionDirectives.TRAIN and GameInfo.Units[e.UnitType]
  if closed then return end
  local v=ExposedMembers.SPC_ExpeditionActivity
  if r and r.UnitType==M.KIND and v and v.phase=='TRAINING' and v.trainingToken then
   pending={owner=c:GetOwner(),city=c:GetID(),reservation=v.trainingToken,stage='CANCEL',attempts=0}
  end
 end
 local function clear(p,err)
  if closed or pending~=p then return end
  pending=nil;sync=nil;view=nil;attempted=nil;covered=nil
  ExposedMembers.SPC_ExpeditionTrainingUIError=err
  notify(p.owner,p.city)
 end
 function api.Invalidate(pid)
  if closed then return end
  if pid==nil or pid==(selected and selected.owner or Game.GetLocalPlayer())then cause=cause+1 end
 end
 function api.RefreshFacts()
  if closed or pumping or pending or not selected then return end
  local reply=ExposedMembers.SPC_ExpeditionTrainingReply
  local ready=sync and reply and reply.token==sync.token
  if sameSource(source)and not ready then
   local key=signature(source,selected)
   if key==attempted or sync and key==sync.key then return end
  end
  api.Sync(UI.GetHeadSelectedCity()) -- only a new input/source or matching reply reaches native selection
 end
 function api.Pulse()
  if closed then return end
  api.RefreshFacts()
  local reply=ExposedMembers.SPC_ExpeditionTrainingReply
  local p=pending;if not p then return end
  p.age=(p.age or 0)+1
  if p.age>12 then clear(p,'TRAINING_HANDSHAKE_UNCONFIRMED');return end
  local c=city(p.owner,p.city);if closed or pending~=p then return end
  local valid=localCity(c);if closed or pending~=p then return end
  if not valid then clear(p,'TRAINING_CITY_CHANGED');return end
  if p.stage=='RESERVE' and reply and reply.token==p.token then
   if reply.error then clear(p,reply.error);return end
   if not reply.reserved then clear(p,'TRAINING_RESERVATION_UNCONFIRMED');return end
   p.reservation=reply.reservation
   local chosen=UI.GetHeadSelectedCity();if closed or pending~=p then return end
   local changed=not chosen or chosen:GetID()~=p.city or chosen:GetOwner()~=p.owner or CheckQueueItemSelected()
   if closed or pending~=p then return end
   if changed then p.stage='CANCEL'
   else
    local row=GameInfo.Units[M.KIND]
    local produce=c:GetBuildQueue():CanProduce({UnitType=row.Hash},false,true)
    if closed or pending~=p then return end
    if not produce then p.stage='CANCEL';p.cancelReason=Locale.Lookup('LOC_SPC_EXPEDITION_TRAINING_NATIVE_DENIED')
    else
     p.stage='QUEUE';p.issued=true -- before native callback; never resend BUILD
     observe('UI_BUILD_BEFORE',c);if closed or pending~=p then return end
     local ok,err=pcall(build,c,p.item);if closed or pending~=p then return end
     observe('UI_BUILD_RETURNED',c);if closed or pending~=p then return end
     if not ok then clear(p,tostring(err));return end
    end
   end
  end
  if p.stage=='QUEUE' then
   -- B209/B210: Gameplay already holds the queue evidence or a receipt, or the
   -- reservation ended (immediate completion, native replacement); stop
   -- waiting without an error instead of re-reading an emptied queue.
   local v=ExposedMembers.SPC_ExpeditionActivity
   if v and (v.trainingToken~=p.reservation or v.trainingQueued or v.trainingReceipt or v.phase~='TRAINING') then
    clear(p,v.phase=='HELD' and v.trainingToken==p.reservation and v.error or nil);return
   end
  end
  if p.stage=='QUEUE' or p.stage=='CANCEL' then
   local ok,q=pcall(ExposedMembers.SPC_ExpeditionQueueRead,p.owner,p.city)
   if closed or pending~=p then return end
   if not ok then clear(p,tostring(q));return end
   if p.stage=='QUEUE' and q.count==1 or p.stage=='CANCEL' and q.count==0 then
    local token,packet=request(p.stage=='QUEUE' and 'CONFIRM' or 'CANCEL',c,p.reservation)
    p.token=token;p.stage='ACK';transmit(p.owner,packet)
   else
    p.attempts=p.attempts+1
    if p.attempts>=12 then clear(p,'TRAINING_NATIVE_QUEUE_UNCONFIRMED');return end
   end
  elseif p.stage=='ACK' and reply and reply.token==p.token then
   clear(p,reply.error or p.cancelReason)
  end
 end
 function api.Close()
  if closed then return end;closed=true
  pending=nil;selected=nil;source=nil;sync=nil;view=nil;attempted=nil;covered=nil;activeCity=nil;diagnosticRowKey=nil
 end
 return api
end
