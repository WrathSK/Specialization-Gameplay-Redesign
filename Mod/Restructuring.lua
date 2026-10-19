-- B247 event-driven team admission and city transaction coordinator.
include('RestructuringModel')
SPCRestructuring={ACCESS='BUILDING_SPC_RESTRUCTURING_ACCESS',DISRUPTION='BUILDING_SPC_REALLOCATING'}
function SPCRestructuring.Start(P,shared)
 local M=SPCRestructuringModel;local S=SPCRestructuring;local cp=M.Copy;local store=assert(shared.CityProgressionStore)
 local d={views={},errors={},ready=false};shared.Restructuring=d
 local busy=false;local births,completed,dirty,publication={},{},{},{};local plans={}
 local trace=SPCExpeditionTrainingDiagnostics and SPCExpeditionTrainingDiagnostics.New(P,'RESTRUCTURING')
 local function key(pid,id)return pid..':'..id end
 local function city(pid,id)return Players[pid] and Players[pid]:GetCities():FindID(id)end
 local function ref(c)return {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function code(e)return tostring(e):match('(REST_[A-Z_]+)') or tostring(e):match('([A-Z][A-Z_]+)') or 'REST_READ_FAILED'end
 local function log(stage,pid,c,s,reason)
  if trace then trace.Record(stage,{owner=pid,city=c and c:GetID(),phase=s and s.phase,
   teamKey=s and s.team and s.team.uid,taskStart=s and s.started,taskDue=s and s.started and s.started+5,
   expected=s and s.potential,previous=s and s.previous,mode=s and s.identity,reason=reason or 'OK'})end
 end
 local function unit(pid,id)
  local u=Players[pid] and Players[pid]:GetUnits():FindID(id);local row=u and P.Info('Units',u:GetType())
  assert(u and u:GetOwner()==pid and row and row.UnitType==M.UNIT,'REST_TEAM_UNAVAILABLE');return u
 end
 local function binding(u)
  local b=u:GetProperty(M.UNIT_KEY)
  assert(type(b)=='table' and b.version==1 and b.owner==u:GetOwner() and b.id==u:GetID() and type(b.uid)=='string'
   and type(b.source)=='table' and type(b.source.token)=='string','REST_TRAINING_UNCONFIRMED')
  return cp(b)
 end
 local function writeUnit(u,old,value)
  assert(M.Same(u:GetProperty(M.UNIT_KEY),old),'REST_TEAM_STALE');P.SetProperty(u,M.UNIT_KEY,cp(value))
  assert(M.Same(u:GetProperty(M.UNIT_KEY),value),'REST_TEAM_WRITE_UNCONFIRMED')
 end
 local function marker(c,name,wanted)
  local row=assert(P.Info('Buildings',name),'REST_MARKER_MISSING');local b=c:GetBuildings();local has=P.HasBuilding(b,row.Index)
  assert(type(has)=='boolean','REST_MARKER_UNKNOWN')
  if has~=wanted then
   if wanted then P.CreateBuilding(c:GetBuildQueue(),row.Index)else P.RemoveBuilding(b,row.Index)end
   assert(P.HasBuilding(b,row.Index)==wanted,'REST_MARKER_WRITE_UNCONFIRMED')
  end
 end
 local function standard()assert(SPCCommerceModel.IsStandardSpeed(),'REST_STANDARD_SPEED_ONLY')end
 local function place(pid,u)
  -- One player's existing district collection; no world scan or cached native object.
  local found
  for _,district in Players[pid]:GetDistricts():Members()do
   if district:GetX()==u:GetX() and district:GetY()==u:GetY() then
    local c=district:GetCity();local row=P.Info('Districts',district:GetType())
    if c and c:GetOwner()==pid and row then
     local kind=P.Family(row.DistrictType)
     if M.Kinds[kind] then
      assert(not found,'REST_SITE_AMBIGUOUS');assert(district:IsComplete() and not district:IsPillaged(),'REST_SITE_NOT_OPERATIONAL')
      found={city=c,kind=kind,first={districtID=district:GetID(),type=row.DistrictType,turn=Game.GetCurrentGameTurn()}}
     end
    end
   end
  end
  return assert(found,'REST_MOVE_TO_SPECIALTY_DISTRICT')
 end
 local function target(pid,b)
  local a=assert(b.target,'REST_TARGET_UNBOUND');local c=CityManager.GetCityAt(a.x,a.y)
  assert(c and M.Same(ref(c),a.reference),'REST_TARGET_OWNER_CHANGED')
  assert(store.HistoricalReference(c).token==a.token,'REST_TARGET_IDENTITY_CHANGED');return c
 end
 local function teamRef(b)return {owner=b.owner,id=b.id,uid=b.uid}end
 local function inspect(pid,id)
  standard();local u=unit(pid,id);local b=binding(u)
  local v={owner=pid,unit=id,x=u:GetX(),y=u:GetY(),turn=Game.GetCurrentGameTurn(),legal=false,uid=b.uid,sourceCity=b.source.cityID}
  if b.target then
   local c=target(pid,b);local s=assert(store.RestructuringState(pid,c),'REST_RECORD_MISSING')
   assert(M.Same(s.team,teamRef(b)),'REST_BOUND_TEAM_CHANGED')
   v.city=c:GetID();v.cityName=c:GetName();v.phase=s.phase;v.remaining=math.max(0,s.started+5-v.turn);v.potential=s.potential;v.previous=s.previous
   assert(s.phase=='REALLOCATING','REST_PENDING_REVIEW');v.action='CONFIGURE'
   local p=place(pid,u);assert(p.city:GetID()==c:GetID() and M.Same(ref(p.city),ref(c)),'REST_SAME_CITY_REQUIRED')
   assert(p.kind~=s.previous,'REST_DIFFERENT_IDENTITY_REQUIRED');v.kind=p.kind;v.first=p.first
   assert(v.remaining==0,'REST_FIVE_FULL_TURNS_REQUIRED');v.legal=true
  else
   local p=place(pid,u);local c=p.city;local f=shared.EffectiveFacts.Read(pid,c)
   assert(f.specialization==p.kind and f.first and f.first.districtID==p.first.districtID,'REST_CURRENT_SPECIALTY_DISTRICT_REQUIRED')
   assert(f.potential>=2 and not f.investmentPending,'REST_POTENTIAL_TWO_REQUIRED')
   local s=store.RestructuringState(pid,c);assert(not s or s.phase=='SETTLED','REST_ALREADY_ACTIVE')
   v.city=c:GetID();v.cityName=c:GetName();v.action='LIQUIDATE';v.potential=f.potential-1;v.previous=f.specialization;v.first=p.first;v.legal=true
  end
  return v
 end
 function d.Read(pid,id)
  local ok,v=pcall(inspect,pid,id)
  if not ok then
   v={owner=pid,unit=id,legal=false,reason=code(v),turn=Game.GetCurrentGameTurn()}
   -- Preserve only independently read transaction labels, never eligibility.
   local good,u=pcall(unit,pid,id)
   if good then
    v.x=u:GetX();v.y=u:GetY()
    local b=u:GetProperty(M.UNIT_KEY)
    if b and b.target then
     local known,c=pcall(target,pid,b)
     if known then
      local read,s=pcall(store.RestructuringState,pid,c)
      if read and s then v.city=c:GetID();v.cityName=c:GetName();v.phase=s.phase;v.remaining=math.max(0,s.started+5-v.turn);v.potential=s.potential;v.action='CONFIGURE'end
     end
    else v.action='LIQUIDATE'end
   end
  end
  local plan=plans[key(pid,id)]
  if plan and (not v.legal or not M.Same(plan.view,v))then plans[key(pid,id)]=nil;plan=nil end
  if plan then v=cp(v);v.prepared=plan.token end
  d.views[key(pid,id)]=cp(v);ExposedMembers.SPC_RestructuringViews=d.views;return v
 end
 local function mark(pid,id)
  if not P.IsTestPlayer(pid)then return end
  dirty[pid]=dirty[pid] or {};dirty[pid][id or 'all']=true
 end
 -- Dependency-specific publication, once per successful identity transition.
 -- Existing consumers own their carriers; no broad RemoveOwned or history deletion.
 function d.Publish(pid,c)
  local id=c:GetID();local errors={}
  local function call(name,method,...)
   local x=shared[name];if not x or type(x[method])~='function'then return end
   local ok,err=pcall(x[method],...);if not ok then errors[name]=code(err)end
  end
  call('NetworkBridge','Refresh',pid)
  call('Standardization','Refresh',pid,id)
  for _,name in ipairs({'ResearchSupport','IndustrySupport','Lv2Housing','Lv2GPP','Lv3Support','Lv3Effects',
   'ResearchInfrastructure','ResearchCross','ResearchApply','ResearchChair','CultureAesthetic','CultureMeaning','CultureInspiration',
   'DialogueEffects','CultureInsightsTourism'})do call(name,'Audit',{player=pid,city=id})end
  call('ResearchTraditionEffects','Update',pid,c)
  call('StandardizationEffects','SourceChanged',pid,id)
  for _,name in ipairs({'EngineeringStudy','IndustryWonderEffects','CrewProjects','DialogueProjects','CapitalInvestment'})do call(name,'Refresh',pid,id)end
  call('Commerce','SourceChanged',pid,id);call('CultureNetwork','Mark',pid,id)
  call('DevelopmentInvestment','Reconcile',pid,id)
  d.errors[key(pid,id)]=next(errors) and errors or nil
  for name,why in pairs(errors)do log('REST_PUBLICATION_HELD',pid,c,nil,name..':'..why)end
  ExposedMembers.SPC_RuntimeUIRevision=(ExposedMembers.SPC_RuntimeUIRevision or 0)+1
 end
 local function sync(pid,c,recover)
  local f=shared.EffectiveFacts.Read(pid,c);local s=store.RestructuringState(pid,c)
  marker(c,S.ACCESS,SPCCommerceModel.IsStandardSpeed() and f.specialization=='COMMERCE' and f.active==4 and not f.investmentPending)
  local disrupted=s and (s.phase=='REALLOCATING' or s.phase=='CONSUMING') or false
  marker(c,S.DISRUPTION,disrupted)
  if recover and s and s.phase=='CONSUMING' then
   -- Intent alone is not a consumed receipt. Never guess from an absent unit.
   if s.consumed==true then store.FinishRestructuring(pid,c,s.team);marker(c,S.DISRUPTION,false);log('REST_RECOVERED_CONFIGURATION',pid,c,store.RestructuringState(pid,c))
   else log('REST_RECOVERY_HELD',pid,c,s,'REST_CONSUMPTION_UNCONFIRMED')end
  end
  if recover and s and s.phase=='REALLOCATING' then
   local u=unit(pid,s.team.id);local b=binding(u)
   assert(M.Same(s.team,teamRef(b)),'REST_BOUND_TEAM_CHANGED')
   if not b.target then
    local n=cp(b);n.target={token=f.token,reference=ref(c),x=c:GetX(),y=c:GetY()};writeUnit(u,b,n)
   else assert(target(pid,b):GetID()==c:GetID(),'REST_TARGET_CHANGED')end
   log('REST_RESTORED',pid,c,s)
  end
 end
 function d.Flush(recover)
  if busy or not d.ready then return end;busy=true
  local todo=dirty;dirty={}
  for pid,ids in pairs(todo)do
   local function visit(c)
    if not c or not store.Owns(c)then return end
    local ok,err=pcall(sync,pid,c,recover);if not ok then d.errors[key(pid,c:GetID())]=code(err);log('REST_SYNC_HELD',pid,c,nil,code(err))end
   end
   if ids.all then for _,c in Players[pid]:GetCities():Members()do visit(c)end
   else for id in pairs(ids)do visit(city(pid,id))end end
  end
  busy=false
  local changed=publication;publication={}
  for _,c in pairs(changed)do if c:GetOwner()>=0 and P.IsTestPlayer(c:GetOwner())then d.Publish(c:GetOwner(),c)end end
 end
 function d.Request(pid,p)
  if not P.IsTestPlayer(pid) or type(p)~='table' or type(p.Token)~='string' or #p.Token>100 then return end
  if p.Action=='REST_READ' then return d.Read(pid,p.UnitID)end
  if busy then return end
  local k=key(pid,p.UnitID);local irreversible=false
  local ok,err=pcall(function()
   local v=d.Read(pid,p.UnitID);assert(v.legal,v.reason or 'REST_INELIGIBLE')
   if p.Action=='REST_PREPARE' then
    v.prepared=nil;plans[k]={token=p.Token,view=cp(v)};d.Read(pid,p.UnitID);return
   end
   assert(p.Action=='REST_CONFIRM','REST_ACTION_UNKNOWN')
   local plan=assert(plans[k],'REST_PREPARE_FIRST');assert(p.PlanToken==plan.token,'REST_PREVIEW_STALE')
   v.prepared=nil;assert(M.Same(v,plan.view),'REST_PREVIEW_STALE');plans[k]=nil;busy=true
   local u=unit(pid,p.UnitID);local b=binding(u);local psite=place(pid,u);local c=psite.city
   if v.action=='LIQUIDATE' then
    irreversible=true
    local n=cp(b);n.target={token=store.HistoricalReference(c).token,reference=ref(c),x=c:GetX(),y=c:GetY()}
    writeUnit(u,b,n) -- exact target reservation before any Potential debit
    local s=store.BeginRestructuring(pid,c,teamRef(b),p.Token)
    marker(c,S.DISRUPTION,true);mark(pid,c:GetID());log('REST_LIQUIDATED',pid,c,s)
   else
    assert(target(pid,b):GetID()==c:GetID(),'REST_TARGET_CHANGED');irreversible=true
    local s=store.ConfigureRestructuring(pid,c,teamRef(b),psite.kind,psite.first)
    assert(M.Same(store.RestructuringState(pid,c),s),'REST_CONFIGURATION_READBACK')
    -- Single native call; persisted intent blocks repeats if any result is unknown.
    Players[pid]:GetUnits():Destroy(u)
    assert(not Players[pid]:GetUnits():FindID(p.UnitID),'REST_CONSUMPTION_UNCONFIRMED')
    store.ConfirmRestructuringConsumption(pid,c,teamRef(b))
    store.FinishRestructuring(pid,c,teamRef(b));marker(c,S.DISRUPTION,false);mark(pid,c:GetID())
    log('REST_CONFIGURED',pid,c,store.RestructuringState(pid,c))
   end
  end)
  busy=false
  if not ok then
   d.errors[k]=code(err);log('REST_REQUEST_HELD',pid,nil,nil,code(err))
   if irreversible then plans[k]=nil end
  end
  d.Flush();d.Read(pid,p.UnitID)
  d.lastRequest={owner=pid,unit=p.UnitID,token=p.Token,ok=ok,reason=not ok and code(err) or nil}
  ExposedMembers.SPC_RestructuringReply=d.lastRequest
 end
 local function admit(pid)
  local list=births[pid];local queue=completed[pid]
  if not list or not queue then return end
  -- Match by native city tile first. A displaced birth is accepted only when
  -- one completion and one birth remain in this publish batch, never by nearest city.
  local remaining={};for id in pairs(list)do local ok,u=pcall(unit,pid,id);if ok and u:GetProperty(M.UNIT_KEY)==nil then remaining[#remaining+1]=u end end
  local orders={};for cid,count in pairs(queue)do for i=1,count do orders[#orders+1]=cid end end
  if #orders~=#remaining then return end
  while #remaining>0 do
   local index,order
   for i,u in ipairs(remaining)do for j,cid in ipairs(orders)do local c=city(pid,cid);if c and u:GetX()==c:GetX() and u:GetY()==c:GetY()then index=i;order=j;break end end;if index then break end end
   if not index and #remaining==1 then index=1;order=1 end
   if not index then log('REST_TRAINING_HELD',pid,nil,nil,'REST_BIRTH_AMBIGUOUS');return end
   local u=remaining[index];local c=assert(city(pid,orders[order]),'REST_SOURCE_UNAVAILABLE');local a=store.HistoricalReference(c)
   local b={version=1,owner=pid,id=u:GetID(),uid=a.token..':REST:'..u:GetID()..':'..Game.GetCurrentGameTurn(),source=a}
   writeUnit(u,nil,b);list[u:GetID()]=nil;queue[c:GetID()]=queue[c:GetID()]-1
   table.remove(remaining,index);table.remove(orders,order);log('REST_TRAINED',pid,c,{team=teamRef(b),phase='AVAILABLE'})
   d.Read(pid,u:GetID())
  end
  births[pid]=nil;completed[pid]=nil
 end
 local function hook(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn)end end
 hook('UnitAddedToMap',function(pid,id)
  if not P.IsTestPlayer(pid)then return end
  local ok,u=pcall(unit,pid,id);if not ok or u:GetProperty(M.UNIT_KEY)~=nil then return end
  births[pid]=births[pid] or {};births[pid][id]=true
 end)
 hook('CityProductionCompleted',function(pid,cid,kind,index,cancelled)
  if not P.IsTestPlayer(pid) or cancelled or kind~=0 then return end
  local row=P.Info('Units',index);if not row or row.UnitType~=M.UNIT then return end
  completed[pid]=completed[pid] or {};completed[pid][cid]=(completed[pid][cid] or 0)+1
 end)
 hook('GameCoreEventPublishComplete',function()
  if busy then return end
  for pid in pairs(births)do local ok,err=pcall(admit,pid);if not ok then log('REST_TRAINING_HELD',pid,nil,nil,code(err))end end
  d.Flush()
 end)
 hook('UnitRemovedFromMap',function(pid,id)plans[key(pid,id)]=nil;d.views[key(pid,id)]=nil;d.errors[key(pid,id)]=nil;if births[pid]then births[pid][id]=nil end end)
 hook('PlayerTurnDeactivated',function(pid)
  if births[pid] or completed[pid]then log('REST_TRAINING_HELD',pid,nil,nil,'REST_TRAINING_EVENT_PAIR_INCOMPLETE')end
  births[pid]=nil;completed[pid]=nil -- unmatched event pairs never survive a turn boundary
 end)
 for _,event in ipairs({'UnitMoveComplete','UnitMovementPointsChanged'})do hook(event,function(pid,id)if P.IsTestPlayer(pid)then local ok=pcall(unit,pid,id);if ok then d.Read(pid,id)end end end)end
 for _,event in ipairs({'GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','PlayerTurnActivated'})do hook(event,function(pid)
  if not P.IsTestPlayer(pid)then return end;mark(pid);d.Flush()
  for _,u in Players[pid]:GetUnits():Members()do local row=P.Info('Units',u:GetType());if row and row.UnitType==M.UNIT then d.Read(pid,u:GetID())end end
 end)end
 hook('LoadScreenClose',function()
  d.ready=true;births={};completed={};plans={};d.views={};ExposedMembers.SPC_RestructuringViews=d.views
  for pid in pairs(Players)do if P.IsTestPlayer(pid)then mark(pid)end end;d.Flush(true)
 end)
 local prior=shared.OnPermanentCityWrite
 shared.OnPermanentCityWrite=function(c,reason)
  if prior then prior(c,reason)end
  if c then mark(c:GetOwner(),c:GetID());if reason=='Restructuring' then publication[key(c:GetOwner(),c:GetID())]=c end end
 end
 store.RegisterExit('Restructuring',function(c,loss)
  store.RemoveOwned(c,loss,{S.ACCESS,S.DISRUPTION})
  local s=store.RestructuringExit(c)
  if s and s.phase=='DISCARDED' then
   local u=Players[s.team.owner]:GetUnits():FindID(s.team.id)
   if u then
    local b=binding(u);assert(M.Same(teamRef(b),s.team),'REST_EXIT_TEAM_CHANGED')
    Players[s.team.owner]:GetUnits():Destroy(u);assert(not Players[s.team.owner]:GetUnits():FindID(s.team.id),'REST_EXIT_TEAM_UNCONFIRMED')
   end
   log('REST_TARGET_LOST',loss.origin.owner,c,s)
  end
 end)
 store.RegisterReturn('Restructuring',function(pid,c)mark(pid,c:GetID())end)
end
