include('CurrentSpecializationFacts')
include('NetworkInput')
-- B226: current network projection only. Store owns history; Bridge owns topology;
-- native district workers own the yield count. No received history or timer.
SPCCultureNetwork={Bits=8,Owned={},Districts={RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE',COMMERCE='DISTRICT_COMMERCIAL_HUB'}}
local M=SPCCultureNetwork
local function name(kind,bit)return 'BUILDING_SPC_CULTURE_NETWORK_'..kind..'_'..bit end
for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do
 for bit=0,M.Bits-1 do M.Owned[#M.Owned+1]=name(kind,bit)end
end
local function int(n)return type(n)=='number' and n>=0 and n<math.huge and n%1==0 end
function M.Source(records,own)
 assert(type(records)=='table' and type(own)=='string','CN_HISTORY_UNKNOWN')
 local groups,out={},{};local n=0
 for key,r in pairs(records)do
  assert(type(r)=='table' and type(r.civ)=='string' and key==r.civ..':'..tostring(r.category)
   and (r.category=='PEOPLE' or r.category=='WORKS' or r.category=='PLACES'),'CN_HISTORY_INVALID')
  n=n+1;assert(n<=192,'CN_HISTORY_RANGE')
  if r.civ~=own then groups[r.civ]=groups[r.civ] or {};groups[r.civ][r.category]=true end
 end
 for civ,t in pairs(groups)do if t.PEOPLE and t.WORKS and t.PLACES then out[civ]=true end end
 return out
end
function M.Start(P,shared)
 local store=assert(shared.CityProgressionStore,'CN_STORE_REQUIRED')
 local d={ready=false,busy=false,records={},errors={},changes=0};shared.CultureNetwork=d
 local definitions,dirty={},{};local initialized=false
 local function key(pid,id)return tostring(pid)..':'..tostring(id)end
 local function ref(c)return SPCNetworkInput.Reference(c)end
 local function isolated(pid)return shared.NetworkIsolation and shared.NetworkIsolation.Active(pid)==true end
 local function validate()
  if definitions[1]then return end
  local allowed={};local count=0
  for _,r in ipairs(assert(P.Rows('Civilizations'),'CN_CIV_DATABASE_UNKNOWN'))do
   assert(type(r.CivilizationType)=='string','CN_CIV_DATABASE_UNKNOWN')
   if not allowed[r.CivilizationType]then allowed[r.CivilizationType]=true;count=count+1 end
  end
  assert(count>0 and count<2^M.Bits,'CN_LOADED_CIV_ENCODING_RANGE') -- encoding, never clamp a gameplay set
  local yields={}
  for _,row in ipairs(assert(P.Rows('Building_CitizenYieldChanges'),'CN_YIELD_DATABASE_UNKNOWN'))do
   yields[row.BuildingType]=yields[row.BuildingType] or {};table.insert(yields[row.BuildingType],row)
  end
  local rows={}
  for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do for bit=0,M.Bits-1 do
   local id=name(kind,bit);local r=assert(P.Info('Buildings',id),'CN_CARRIER_MISSING');local ys=yields[id]
   assert(r.PrereqDistrict==M.Districts[kind] and (r.InternalOnly==1 or r.InternalOnly==true)
    and r.CitizenSlots==0 and r.Housing==0,'CN_CARRIER_INVALID')
   assert(ys and #ys==1 and ys[1].YieldType=='YIELD_CULTURE' and ys[1].YieldChange==2^bit,'CN_YIELD_INVALID')
   rows[#rows+1]={id=r.Index,kind=kind,bit=bit}
  end end
  definitions=rows;d.allowedCivilizations=allowed
 end
 local function remove(c,row)
  P.RemoveBuilding(c:GetBuildings(),row.id)
  assert(P.HasBuilding(c:GetBuildings(),row.id)==false,'CN_REMOVE_UNCONFIRMED');d.changes=d.changes+1
 end
 local function clear(c)
  d.writing=key(c:GetOwner(),c:GetID())
  local ok,why=pcall(function()
   local present={}
   for _,row in ipairs(definitions)do
    local yes=P.HasBuilding(c:GetBuildings(),row.id);assert(type(yes)=='boolean','CN_PRESENCE_UNKNOWN')
    if yes then present[#present+1]=row end
   end
   for _,row in ipairs(present)do remove(c,row)end
  end)
  d.writing=nil;assert(ok,why)
 end
 local function facts(batch,pid,c)
  local id=c:GetID();if not batch.facts[id]then batch.facts[id]=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)end
  return batch.facts[id]
 end
 local function anchor(batch,pid,c)
  assert(c:GetOwner()==pid,'CN_RECEIVER_OWNER_CHANGED')
  local f=facts(batch,pid,c);assert(f.validity=='VERIFIED' and type(f.identity)=='string','CN_RECEIVER_UNKNOWN')
  if f.identity=='NONE' then return nil end
  local domain=assert(M.Districts[f.identity],'CN_IDENTITY_UNSUPPORTED')
  assert(int(f.potential) and f.potential>=1 and f.first and int(f.first.districtID),'CN_ANCHOR_UNKNOWN')
  -- Receiver qualification is Identity, not ACTIVE. Avoid the support helper's ACTIVE gate.
  local ds=c:GetDistricts();local n=ds:GetNumDistricts();assert(int(n) and n<=256,'CN_DISTRICT_UNKNOWN')
  local found,count=nil,0
  for i=0,n-1 do
   local district=assert(ds:GetDistrictByIndex(i),'CN_DISTRICT_UNKNOWN')
   local row=assert(P.Info('Districts',district:GetType()),'CN_DISTRICT_UNKNOWN')
   if P.Family(row.DistrictType)==f.identity then
    count=count+1
    if district:GetID()==f.first.districtID then
     local complete,pillaged=district:IsComplete(),district:IsPillaged()
     assert(type(complete)=='boolean' and type(pillaged)=='boolean','CN_DISTRICT_UNKNOWN')
     assert(row.DistrictType==f.first.type,'CN_ANCHOR_CHANGED')
     if complete and not pillaged then found=district end
    end
   end
  end
  assert(count<=1,'CN_MULTIPLE_IDENTITY_DISTRICTS')
  if not found then return nil end
  local plot=assert(Map.GetPlot(found:GetX(),found:GetY()),'CN_PLOT_UNKNOWN'):GetIndex()
  assert(int(plot),'CN_PLOT_UNKNOWN');return f.identity,plot
 end
 local function source(batch,pid,id)
  if batch.sources[id]then return batch.sources[id]end
  local out={set={}};batch.sources[id]=out
  local ok,err=pcall(function()
   local c=Players[pid]:GetCities():FindID(id)
   if not c or c:GetOwner()~=pid then return end
   out.reference=ref(c);local f=facts(batch,pid,c)
   assert(f.validity=='VERIFIED' and type(f.identity)=='string','CN_SOURCE_UNKNOWN')
   if f.identity~='CULTURE' then return end
   assert(int(f.potential),'CN_SOURCE_UNKNOWN');if f.potential<4 then return end
   assert(f.activeStatus=='KNOWN' and int(f.active),'CN_SOURCE_ACTIVE_UNKNOWN')
   if f.active<4 then return end
   assert(f.active==4 and f.potential==4,'CN_SOURCE_LEVEL_INVALID')
   local config=PlayerConfigurations and PlayerConfigurations[pid]
   local own=config and config:GetCivilizationTypeName();assert(d.allowedCivilizations[own],'CN_OWNER_CIV_UNKNOWN')
   out.set=M.Source(store.ExpeditionInsights(pid,c),own)
   for civ in pairs(out.set)do assert(d.allowedCivilizations[civ],'CN_HISTORY_CIV_UNKNOWN')end
   assert(c:GetOwner()==pid and ref(c)==out.reference,'CN_SOURCE_CHANGED')
  end)
  if not ok then out.error=tostring(err)end
  return out
 end
 local function network(batch,pid)
  assert(not batch.networkFailed,batch.networkFailed)
  if batch.network then return batch.network end
  local bridge=assert(shared.NetworkBridge,'CN_NETWORK_UNAVAILABLE');local input=bridge.Input(pid)
  if input.validity=='CONFIRMED_INVALID' then batch.network={input=input,recipients={}};return batch.network end
  local current=bridge.CurrentCultureBatch(pid)
  assert(current.input.validity=='VERIFIED' and current.input.availability=='AVAILABLE','CN_NETWORK_PENDING')
  batch.network=current;return current
 end
 local function plan(batch,pid,c)
  local kind,plot=anchor(batch,pid,c);local p={kind=kind,plot=plot,n=0,set={},sources={},contributors={}}
  if not kind then return p end
  local view=network(batch,pid)
  for id in pairs(view.recipients[c:GetID()] or {})do
   local s=source(batch,pid,id);assert(not s.error,s.error)
   p.sources[id]=s.reference or false
   if next(s.set)then p.contributors[id]=s.reference end
   for civ in pairs(s.set)do p.set[civ]=true end
  end
  for _ in pairs(p.set)do p.n=p.n+1 end
  assert(p.n<2^M.Bits,'CN_UNION_ENCODING_RANGE');return p
 end
 local function confirmedSourceLoss(pid,old)
  if not old then return false end
  for id,reference in pairs(old.contributors or {})do
   if reference then
    local ok,lost=pcall(function()
     local c=Players[pid]:GetCities():FindID(id)
     if not c or c:GetOwner()~=pid or ref(c)~=reference then return true end
     local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
     return f.validity=='VERIFIED' and (f.identity~='CULTURE' or type(f.potential)=='number' and f.potential<4
      or f.activeStatus=='KNOWN' and type(f.active)=='number' and f.active<4)
    end)
    if ok and lost then return true end
   end
  end
  return false
 end
 local function reconcile(batch,pid,c)
  local k=key(pid,c:GetID());local reference=ref(c);local old=d.records[k]
  if old and old.reference~=reference then clear(c);d.records[k]=nil;old=nil end
  local ok,p=pcall(plan,batch,pid,c)
  if not ok then
   if confirmedSourceLoss(pid,old)then clear(c);d.records[k]=nil end
   error(p)
  end
  assert(c:GetOwner()==pid and ref(c)==reference,'CN_RECEIVER_CHANGED')
  d.writing=k
  local mutating=false
  local wrote,why=pcall(function()
   local rows={};local b=c:GetBuildings()
   for _,def in ipairs(definitions)do
    local yes=P.HasBuilding(b,def.id);assert(type(yes)=='boolean','CN_PRESENCE_UNKNOWN')
    local want=def.kind==p.kind and math.floor(p.n/2^def.bit)%2==1
    local row={id=def.id,want=want,yes=yes};rows[#rows+1]=row
    if yes then
     local at,damage=b:GetBuildingLocation(def.id),b:IsPillaged(def.id)
     assert(int(at) and type(damage)=='boolean','CN_LOCATION_UNKNOWN')
     row.remove=not want or at~=p.plot or damage
    end
   end
   for _,row in ipairs(rows)do if row.remove then mutating=true;remove(c,row);row.yes=false end end
   for _,row in ipairs(rows)do if row.want and not row.yes then
    mutating=true;P.CreateBuilding(c:GetBuildQueue(),row.id)
    assert(P.HasBuilding(b,row.id)==true and b:GetBuildingLocation(row.id)==p.plot and b:IsPillaged(row.id)==false,'CN_CREATE_UNCONFIRMED')
    d.changes=d.changes+1
   end end
   assert(c:GetOwner()==pid and ref(c)==reference,'CN_RECEIVER_CHANGED')
  end)
  d.writing=nil
  if not wrote then
   if mutating then d.records[k]=nil;pcall(clear,c)end
   error(why)
  end
  p.reference=reference;p.owner=pid;p.id=c:GetID();p.x=c:GetX();p.y=c:GetY();d.records[k]=p;d.errors[k]=nil
 end
 function d.Mark(pid,cid)
  if pid==nil then for owner in pairs(Players)do if P.IsTestPlayer(owner)then d.Mark(owner,cid)end end;return end
  if not P.IsTestPlayer(pid) or isolated(pid)then return end
  dirty[pid]=dirty[pid] or {cities={}}
  if cid==nil then dirty[pid].all=true else dirty[pid].cities[cid]=true end
 end
 function d.Audit(scope)
  if not d.ready then return end
  if d.busy then d.Mark(scope and scope.player,scope and scope.city);return end
  d.busy=true
  local good,why=pcall(function()
   validate()
   if not initialized then
    -- Saved derived carriers may exist under unsupported owners. Load-only exact cleanup.
    for _,player in pairs(Players)do for _,c in player:GetCities():Members()do clear(c)end end
    d.records={};d.errors={};initialized=true
   end
   for pid,player in pairs(Players)do if P.IsTestPlayer(pid) and not isolated(pid) and (not scope or scope.player==nil or pid==scope.player)then
    local batch={facts={},sources={}};local viewOk,view=pcall(network,batch,pid);if not viewOk then batch.networkFailed=tostring(view)end;local ids={}
    if viewOk then for cid in pairs(view.recipients)do ids[cid]=true end end
    for _,r in pairs(d.records)do if r.owner==pid then ids[r.id]=true end end
    if scope and scope.city~=nil then ids[scope.city]=true end
    local changed=scope and (scope.changed or scope.city~=nil and {[scope.city]=true})
    for cid in pairs(ids)do
     local old=d.records[key(pid,cid)];local visit=not changed or changed[cid]
     if changed then
      for src in pairs(viewOk and view.recipients[cid] or {})do if changed[src]then visit=true end end
      for src in pairs(old and old.sources or {})do if changed[src]then visit=true end end
     end
     if visit then
      local c=player:GetCities():FindID(cid);local k=key(pid,cid)
      if c and c:GetOwner()==pid then
       local ok,err=pcall(reconcile,batch,pid,c);if not ok then d.errors[k]=tostring(err):sub(1,180)end
      else d.records[k]=nil;d.errors[k]=nil end
     end
    end
    if not viewOk then d.playerError=d.playerError or {};d.playerError[pid]=tostring(view):sub(1,180)
    elseif d.playerError then d.playerError[pid]=nil end
   end end
  end)
  d.error=not good and tostring(why):sub(1,180) or nil;d.busy=false
 end
 function d.SourceChanged(pid,cid)d.Audit({player=pid,changed={[cid]=true}})end
 local function flush()
  if d.busy then return end
  local todo=dirty;dirty={}
  for pid,v in pairs(todo)do d.Audit({player=pid,changed=not v.all and v.cities or nil})end
 end
 function d.Describe(pid,c)
  local k=key(pid,c:GetID());local p=d.records[k];local error=d.errors[k] or d.error or d.playerError and d.playerError[pid]
  local ok,workers=pcall(function()
   assert(p and p.reference==ref(c) and not error,'CN_REPORT_PENDING')
   if not p.plot then return 0 end
   local n=Map.GetPlotByIndex(p.plot):GetWorkerCount();assert(int(n),'CN_WORKERS_UNKNOWN');return n
  end)
  if not ok then return '文化网络：等待当前连接或城市事实确认。'end
  print('[SPC][B191][N1_INSIGHT] kind=NETWORK owner='..pid..' city='..c:GetID()..' civilizations='..p.n..' workers='..workers..' expected='..p.n*workers)
  return '文化网络｜完整文明 '..p.n..'｜本专业工作专家 '..workers..'\n每名额外 +'..p.n..' 文化；本城预期 +'..p.n*workers..' 文化。'
 end
 function d.ExperimentalNetworkWithdraw(pid)
  assert(isolated(pid) and not d.busy,'CN_ISOLATION_REQUIRED');validate()
  for _,c in Players[pid]:GetCities():Members()do clear(c);d.records[key(pid,c:GetID())]=nil;d.errors[key(pid,c:GetID())]=nil end
  dirty[pid]=nil;return true
 end
 local function bind(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn)end end
 bind('LoadScreenClose',function()definitions={};initialized=false;d.ready=true;d.Audit()end)
 bind('GameCoreEventPublishComplete',flush)
 for _,event in ipairs({'GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted'})do bind(event,function(pid)d.Mark(type(pid)=='number' and pid or nil)end)end
 for _,event in ipairs({'CityBuildingsChanged','DistrictPillaged','DistrictRepaired','DistrictRemovedFromMap','DistrictBuildProgressChanged'})do
  local eventName=event
  bind(event,function(pid,id,cid)
   if eventName=='CityBuildingsChanged' then cid=id end
   if d.writing~=key(pid,cid)then d.Mark(type(pid)=='number' and pid or nil,cid)end
  end)
 end
 bind('CityTransfered',function()d.Mark()end)
 bind('PlayerTurnActivated',function(pid)if P.IsTestPlayer(pid)then d.Mark(pid)end end)
 -- Working specialists scale through the native carrier, not a stored/count ledger.
 store.RegisterExit('CultureNetwork',function(c,loss)
  assert(store.IsExitTarget(c,loss),'CN_EXIT_UNCONFIRMED');store.RemoveOwned(c,loss,M.Owned)
  for k,p in pairs(d.records)do if p.owner==loss.origin.owner and p.x==c:GetX() and p.y==c:GetY()then d.records[k]=nil;d.errors[k]=nil end end
  d.Mark(loss.origin.owner)
 end)
 store.RegisterReturn('CultureNetwork',function(pid,c)d.Mark(pid,c:GetID())end) -- facts commit later
 return d
end
