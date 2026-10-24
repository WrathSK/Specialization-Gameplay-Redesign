include('SafeCallbacks')
include('RuntimeWork')
include('SampleLifecycle')
include('SpecialistSupport')
-- B036 IND-001: native per-specialist Food + base Production adjacency.
-- No actual-adjacency fallback, rounding or city-wide multiplication. Crew access is independently audited.
SPCIndustrySupport={}
function SPCIndustrySupport.Start(P,shared)
 local batch;local defer
 local pending,armed={},{} -- one current reference per affected city, cleared on success/loss/load
 local data={ready=false,busy=false,changes=0,errors={}};shared.IndustrySupport=data
 SPCSampleLifecycle.Reset(data,'industry')
 local trace=SPCExpeditionTrainingDiagnostics and SPCExpeditionTrainingDiagnostics.New(P,'INDUSTRY_SUPPORT')
 local function key(pid,cid)return tostring(pid)..':'..tostring(cid)end
 local function reference(c)return table.concat({c:GetOwner(),c:GetID(),c:GetX(),c:GetY(),tostring(c:GetProperty('SPC_DEV_BINDING_B013_TOKEN'))},':')end
 local function name(bit) return 'BUILDING_SPC_DEV_INDUSTRY_LV1_'..bit end
 local definitions;local ownedIndex={}
 local health=SPCRuntimeWork.NativeHealth(P,shared,data,function(id)return ownedIndex[id]==true end,function(scope)defer(scope)end)
 local function validate()
  if definitions then return definitions end
  local rows,nextOwned={},{}
  for bit=-1,7 do
   local row=P.Info('Buildings',name(bit));assert(row and row.Index,'B036_DATABASE_MISSING: restart/new test game required')
   rows[bit]=row.Index;nextOwned[row.Index]=true
  end
  definitions=rows;ownedIndex=nextOwned;return rows
 end
 local function inspect(pid,city,externalBatch)
  return SPCSpecialistSupport.Inspect(P,shared,pid,city,externalBatch or batch or SPCRuntimeWork.New(P,shared),function(kind,d,f,workers,geometry)
  if kind~='INDUSTRY' then return nil end
  local row=assert(P.Info('Districts',d.typeIndex),'INDUSTRY_FACT_INVALID')
  local batch=data.samples[pid];local sample=batch and batch.rows[city:GetID()..':'..d.id]
  assert(sample,'BASE_BACKGROUND_SAMPLE_PENDING')
  assert(sample.reference==SPCSampleLifecycle.AnchorReference(city,d,geometry()),'BASE_BACKGROUND_REFERENCE_PENDING')
  local n=sample.value
  assert(type(n)=='number' and n>=0 and n<=255 and n%1==0,'BASE_ADJACENCY_UNKNOWN_FRACTIONAL_OR_OUT_OF_RANGE')
  return n
  end)
 end
 local function carriers(city,n,write)
  local total,food=0,0;local removed=false
  for bit=-1,7 do
   local id=validate()[bit]
   local wanted=n~=nil and (bit==-1 or math.floor(n/2^bit)%2==1)
   local b=city:GetBuildings();local present=P.HasBuilding(b,id)
   assert(type(present)=='boolean','CARRIER_READ_UNKNOWN')
   if write and present~=wanted then
    if wanted then health.Create(city,id) else health.Remove(city,id);removed=true end
    assert(P.HasBuilding(b,id)==wanted,'CARRIER_WRITE_UNCONFIRMED')
    data.changes=data.changes+1;present=wanted
   end
   if present then if bit==-1 then food=3 else total=total+2^bit end end
  end
  if removed and n==nil then P.Count('industry_withdraw') end
  return total,food
 end
 local function startReady()
  if data.ready then return true end
  local store=shared.CityProgressionStore
  if store and store.HistoryStartStatus and store.HistoryStartStatus()=='WAITING'then return false end
  data.ready=true;return true
 end
 local function queue(c,wake)
  if not c or not P.IsTestPlayer(c:GetOwner())then return end
  local k=key(c:GetOwner(),c:GetID())
  pending[k]={player=c:GetOwner(),city=c:GetID(),reference=reference(c)}
  if wake then armed[k]=true end
 end
 function data.MarkCity(c)queue(c,true)end
 -- Only real incoming causes are retained while a visit is busy. Never retain cities/native handles.
 local deferred,deferredOrder,sampleWork={},{},{}
 defer=function(scope)
  local s=type(scope)=='table' and scope or {};local out={player=s.player,city=s.city,load=s.load==true or nil}
  local tag=tostring(out.player)..':'..tostring(out.city)..':'..tostring(out.load)
  if type(s.transfer)=='table'then
   out.transfer={owner=s.transfer.owner,city=s.transfer.city,oldOwner=s.transfer.oldOwner}
   tag='TRANSFER:'..tostring(out.transfer.owner)..':'..tostring(out.transfer.city)..':'..tostring(out.transfer.oldOwner)
  elseif type(s.plot)=='table'then out.plot={s.plot[1],s.plot[2]};tag='PLOT:'..tostring(out.plot[1])..':'..tostring(out.plot[2])end
  if not deferred[tag]then
   if #deferredOrder>=2048 then data.errors.deferred='INDUSTRY_CAUSE_LIMIT';return end
   deferredOrder[#deferredOrder+1]=tag
  end
  deferred[tag]=out
 end
 local targets=SPCRuntimeWork.NewTargets(P,shared,function(pid,c)
  local k=key(pid,c:GetID());armed[k]=nil -- consume only causes present before this visit
  local before=data.changes;local n=inspect(pid,c)
  SPCSpecialistSupport.Retire(P,c,shared);carriers(c,n,true)
  local k=pid..':'..c:GetID();local waiting=pending[k]
  local f=waiting and P.IsTestPlayer(pid) and batch.Facts(pid,c) or {specialization='EXIT'}
  if n~=nil or f.specialization~='NONE' or not waiting or reference(c)~=waiting.reference then if not armed[k]then pending[k]=nil end end
  if trace and data.changes~=before then trace.Record('INDUSTRY_SUPPORT',{owner=pid,city=c:GetID(),expected=n or 0,wanted=n~=nil and 'FOOD_3_PLUS_BASE_PRODUCTION' or 'NONE',readStatus='VERIFIED'})end
 end,function(pid,cid,why)data.errors[tostring(pid)..':'..cid]=why;local p=Players[pid];local c=why and P.IsTestPlayer(pid) and p and p:GetCities():FindID(cid);if c then queue(c,false)end end)
 function data.Audit(scope)
  if P.Observe then P.Observe('audit','IndustrySupport') end
  if data.busy then defer(scope);P.Count('busy_skip');return end
  if not startReady()then P.Count('busy_skip');return end
  local ok,err=pcall(validate);data.errors.definitions=not ok and tostring(err) or nil;if not ok then return end
  data.busy=true;batch=SPCRuntimeWork.New(P,shared)
  targets.Run(scope)
  data.busy=false;batch=nil
 end
 function data.FlushPending(pid,confirmedSample)
  if data.busy or not startReady() then return end
  if not confirmedSample and not next(armed)then return end
  local todo={};for k in pairs(confirmedSample and pending or armed)do
   local v=pending[k];if v and (pid==nil or pid==v.player)then todo[k]=v end
  end
  for k,v in pairs(todo)do
   local player=Players[v.player];local c=player and player:GetCities():FindID(v.city)
   if not c or c:GetOwner()~=v.player or reference(c)~=v.reference then pending[k]=nil;armed[k]=nil
   else
    armed[k]=nil -- consume the cause before Audit/native reentry; failure cannot re-arm it
    data.Audit({player=v.player,city=v.city})
   end
  end
 end
 local function drainCauses(pid)
  if data.busy or not startReady()then return end
  local samples={};for owner,cause in pairs(sampleWork)do if pid==nil or owner==pid then samples[owner]=cause;sampleWork[owner]=nil end end
  -- Snapshot before visits so a newer reentrant cause survives for the next publication.
  local work,order=deferred,deferredOrder;deferred={};deferredOrder={}
  for owner,cause in pairs(samples)do
   if cause=='CHANGED'then data.Audit({player=owner})else data.FlushPending(owner,true)end
  end
  for _,tag in ipairs(order)do data.Audit(work[tag])end
 end
 function data.BindPermanentWrites()
  if shared.FactChanges then shared.FactChanges.RegisterConsumer('IndustrySupport',function(e)
   local causes=e.causes or {}
   if causes.NATIVE_GOVERNOR_ASSIGNED or causes.NATIVE_GOVERNOR_ESTABLISHED
    or causes.NATIVE_GOVERNOR_CHANGED or causes.NATIVE_GOVERNOR_PROMOTED then
    defer({player=e.player,city=e.city});return
   end
   if type(e.city)~='number'then return end
   local player=Players[e.player];local c=player and player:GetCities():FindID(e.city)
   if c and c:GetOwner()==e.player then data.MarkCity(c)end
  end,{kinds={'IDENTITY','POTENTIAL','ACTIVE'}})end
 end
 data.ReadBase=inspect
 function data.Receive(pid,params)
  local changed,proof=SPCSampleLifecycle.Receive(P,data,'industry',pid,params,true)
  if changed or proof=='CONFIRMED_RECOVERED'then
   sampleWork[pid]=changed and 'CHANGED' or sampleWork[pid] or 'RECOVERED'
   drainCauses(pid)
  elseif proof=='CONFIRMED_UNCHANGED'then data.FlushPending(pid)end
 end
 function data.Describe(pid,city)
  local bg=ExposedMembers.SPC_IndustryBackground
  local ok,n=pcall(inspect,pid,city)
  local valid,p,f=pcall(carriers,city,nil,false)
  return 'P0-B1 Industry ACTIVE1–4 city='..city:GetID()
   ..'\nBASE Production adjacency='..(ok and tostring(n or 'N/A') or 'ERROR '..tostring(n))
   ..'\nPer worker expected='..(ok and n~=nil and ('3F / '..n..'P') or 'NONE')
   ..' carrier='..(valid and (f..'F / '..p..'P') or ('ERROR '..tostring(p)))
   ..'\nbackground='..tostring(bg and bg.state or 'NOT_STARTED')..' pending='..tostring(bg and bg.pending or 0)..' requests='..tostring(bg and bg.requests or 0)
   ..' receive='..tostring(data.receiveErrors and data.receiveErrors[pid] or 'NONE')
   ..'\nchanges='..data.changes..' error='..tostring(data.errors[pid..':'..city:GetID()] or 'NONE')
   ..'\nRead only; verify native specialist yields. Native district yields are additional; retired III Food/Gold upgrade cannot reactivate.'
 end
 local function hook(source,name,fn) local e=P.Field(source,name);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() pending={};armed={};deferred={};deferredOrder={};sampleWork={};data.ready=true;SPCSampleLifecycle.Reset(data,'industry');data.Audit({load=true}) end)
 hook(Events,'GameCoreEventPublishComplete',function()drainCauses();data.FlushPending()end)
 -- Shared D replaces only ordinary structural causes. Preserve independent
 -- raw-adjacency plot notifications and the no-provider startup fallback.
 for _,n in ipairs({'PlayerTurnActivated','CityTransfered','ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap'})do SPCRuntimeWork.TargetHook(P,Events,n,data.Audit)end
 if not shared.DistrictCompleteness then
 hook(GameEvents,'OnDistrictConstructed',function(pid,index,x,y)
  local r=P.Info('Districts',index)
  if not r or P.Family(r.DistrictType)~='INDUSTRY' or not P.IsTestPlayer(pid)then return end
  local district=CityManager.GetDistrictAt(x,y);local c=district and district:GetCity()
  if c and c:GetOwner()==pid and district:GetType()==index then data.MarkCity(c);data.FlushPending(pid)end
 end)
 for _,n in ipairs({'DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired'})do SPCRuntimeWork.TargetHook(P,Events,n,data.Audit)end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt','OnPillage'})do SPCRuntimeWork.TargetHook(P,GameEvents,n,data.Audit)end
 end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('IndustrySupport',targets.Exit(function(c,loss)
   local ids={};for bit=-1,7 do ids[#ids+1]=name(bit)end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
   pending[key(loss.origin.owner,loss.origin.cityID)]=nil;pending[key(c:GetOwner(),c:GetID())]=nil
   armed[key(loss.origin.owner,loss.origin.cityID)]=nil;armed[key(c:GetOwner(),c:GetID())]=nil
 end))end

 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterReturn('IndustrySupport',function(pid)SPCSampleLifecycle.Reset(data,'industry');data.last={} end)end

end
