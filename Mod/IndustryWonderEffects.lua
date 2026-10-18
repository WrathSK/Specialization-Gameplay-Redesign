include('NetworkInput')
include('ExpeditionTrainingDiagnostics')
-- Derived ordinary-production effects only. No progress injection, N/E/L ledger
-- reads, topology or Crew writes. Native effect filters each Wonder's own era.
SPCIndustryWonderEffects={}
function SPCIndustryWonderEffects.Start(P,shared)
 local d={records={},errors={}};shared.IndustryWonderEffects=d
 local definitions,eras;local dirty={};local initialized=false;local busy=false;local playerEra={}
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'INDUSTRY_WONDER_EFFECT')
 local function key(pid,id)return pid..':'..id end
 local function mark(pid,id)if P.IsTestPlayer(pid)then local q=dirty[pid] or {};dirty[pid]=q;if id==nil then q.all=true else q[id]=true end end end
 local function validate()
  if definitions then return end
  local list,byEra={},{}
  for _,r in ipairs(P.Rows('SPC_IndustryWonderEffects'))do
   local e=assert(P.Info('Eras',r.EraType),'IW_ERA_MISSING');local b=assert(P.Info('Buildings',r.CarrierType),'IW_CARRIER_MISSING')
   assert(type(e.ChronologyIndex)=='number' and (b.InternalOnly==true or b.InternalOnly==1) and b.CitizenSlots==0 and b.Housing==0,'IW_DEFINITION_INVALID')
   local row={id=r.CarrierType,index=b.Index,era=r.EraType,chronology=e.ChronologyIndex,amount=r.Amount}
   assert(row.amount==10 or row.amount==20 or row.amount==30,'IW_AMOUNT_INVALID')
   list[#list+1]=row;byEra[r.EraType]=byEra[r.EraType] or {};byEra[r.EraType][r.Amount]=row
  end
  assert(#list>0,'IW_DEFINITION_EMPTY');definitions,eras=list,byEra
 end
 local function current(pid)
  local ok,e=P.Call(Players[pid],'GetEra');assert(ok,'IW_CIVILIZATION_ERA_UNKNOWN')
  local row=assert(P.Info('Eras',e),'IW_CIVILIZATION_ERA_UNKNOWN');return row.ChronologyIndex
 end
 local function present(c)
  local a={};local b=c:GetBuildings()
  for _,r in ipairs(definitions)do local has=P.HasBuilding(b,r.index);assert(type(has)=='boolean','IW_PRESENCE_UNKNOWN');if has then a[r.id]=true end end;return a
 end
 local function write(c,old,want)
  local b=c:GetBuildings()
  for _,r in ipairs(definitions)do if old[r.id] and not want[r.id]then
   if P.HasBuilding(b,r.index)then P.RemoveBuilding(b,r.index)end
   assert(P.HasBuilding(b,r.index)==false,'IW_REMOVE_UNCONFIRMED');old[r.id]=nil
  end end
  for _,r in ipairs(definitions)do if want[r.id] and not old[r.id]then
   local has=P.HasBuilding(b,r.index);assert(type(has)=='boolean','IW_PRESENCE_UNKNOWN')
   if not has then P.CreateBuilding(c:GetBuildQueue(),r.index)end
   assert(P.HasBuilding(b,r.index)==true,'IW_ADD_UNCONFIRMED');old[r.id]=true
  end end
 end
 local function reconcile(pid,c)
  local k=key(pid,c:GetID());local reference=SPCNetworkInput.Reference(c);local r=d.records[k]
  if not r or r.reference~=reference then r={owner=pid,x=c:GetX(),y=c:GetY(),reference=reference,applied=present(c)};d.records[k]=r end
  local f=shared.EffectiveFacts.Read(pid,c);local want={};local era
  assert(type(f.specialization)=='string','IW_FACTS_UNKNOWN')
  if f.specialization=='INDUSTRY'then
   assert(f.activeStatus=='KNOWN' and not f.investmentPending,'IW_ACTIVE_UNKNOWN')
   if f.active==4 then
    era=current(pid);assert(type(era)=='number','IW_CIVILIZATION_ERA_UNKNOWN')
    for _,levels in pairs(eras)do
     local gap=era-levels[10].chronology
     if gap>=1 then local amount=math.min(gap,3)*10;assert(levels[amount],'IW_ERA_GAP_INVALID');want[levels[amount].id]=true end
    end
   end
  end
  assert(reference==SPCNetworkInput.Reference(c) and c:GetOwner()==pid,'IW_REFERENCE_CHANGED')
  write(c,r.applied,want);r.era=era;r.active=f.active;d.errors[k]=nil
  local sig=tostring(era)..':'..tostring(f.active)
  if sig~=r.observed then r.observed=sig;trace.Record('INDUSTRY_WONDER_EFFECT',{owner=pid,city=c:GetID(),count=f.active,eraCount=era,readStatus='VERIFIED',reason='IW_ERA_SCOPED'})end
 end
 function d.Flush()
  if busy or shared.CityProgressionStore.HistoryStartStatus()=='WAITING'then return end;busy=true
  local ok,err=pcall(function()
   validate()
   if not initialized then
    -- Store's existing confirmed-exit/load callbacks own foreign-city cleanup.
    -- Initialization reads supported owners only; no extra world-city scan.
    for pid in pairs(Players)do mark(pid)end;initialized=true
   end
   local work=dirty;dirty={}
   for pid,q in pairs(work)do
    local live={}
    for _,c in Players[pid]:GetCities():Members()do
     local k=key(pid,c:GetID());live[k]=true
     if q.all or q[c:GetID()]then
      local good,why=pcall(reconcile,pid,c)
      if not good then d.errors[k]=tostring(why):match('IW_[A-Z_]+') or 'IW_READ_PENDING';trace.Record('INDUSTRY_WONDER_EFFECT',{owner=pid,city=c:GetID(),readStatus='PENDING',reason=d.errors[k]})end
     end
    end
    for k in pairs(d.records)do if k:match('^'..pid..':') and not live[k]then d.records[k]=nil;d.errors[k]=nil end end
   end
  end)
  d.error=not ok and (tostring(err):match('IW_[A-Z_]+') or 'IW_READ_PENDING') or nil;busy=false
 end
 function d.Refresh(pid,id)mark(pid,id);d.Flush()end
 function d.Describe(pid,c)
  local k=key(pid,c:GetID());local r=d.records[k];local reason=d.errors[k] or d.error
  return '巨构工程学：'..(reason and '等待 '..reason or r and r.active==4 and '本城自行生产旧时代奇观：时代差 1 / 2 / 3+ → +10% / +20% / +30%' or '未生效（需要工业 ACTIVE IV）')
   ..'\n按本文明时代与奇观自身时代比较；适用时也可加成施工队投入的基础施工力。'
 end
 local function hook(n,f)local e=P.Field(Events,n);if e and e.Add then e.Add(f)end end
 hook('CityRemovedFromMap',function(pid)mark(pid)end)
 hook('GameCoreEventPublishComplete',d.Flush)
 hook('LoadScreenClose',function()for pid in pairs(Players)do mark(pid)end;d.Flush()end)
 for _,n in ipairs({'GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged','PlayerEraChanged'})do hook(n,function(pid)mark(pid);d.Flush()end)end
 hook('PlayerTurnActivated',function(pid)
  if not P.IsTestPlayer(pid)then return end
  local ok,era=pcall(current,pid)
  if ok and era~=playerEra[pid]then playerEra[pid]=era;mark(pid)end
  for k in pairs(d.errors)do local p,id=k:match('^(%d+):(%d+)$');if tonumber(p)==pid then mark(pid,tonumber(id))end end
  d.Flush()
 end)
 local store=shared.CityProgressionStore
 store.RegisterExit('IndustryWonderEffects',function(c,loss)
  validate();local ids={};for _,r in ipairs(definitions)do ids[#ids+1]=r.id end;store.RemoveOwned(c,loss,ids)
  for k,r in pairs(d.records)do if r.owner==loss.origin.owner and r.x==loss.origin.x and r.y==loss.origin.y then d.records[k]=nil;d.errors[k]=nil end end
  mark(loss.origin.owner)
 end)
 store.RegisterReturn('IndustryWonderEffects',function(pid,c)mark(pid,c:GetID())end)
end
