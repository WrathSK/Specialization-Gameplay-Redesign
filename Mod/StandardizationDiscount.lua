-- B054: derived network discount, permanent templates remain owned by Standardization.
SPCStandardizationDiscount={}
function SPCStandardizationDiscount.Start(P,shared)
 local d={ready=false,busy=false,generation=0,plans={},samples={},seq={},applied={},errors={},changes=0,responses={},appliedSamples=0,holdLoaded=true};shared.StandardizationDiscount=d
 local catalog,carriers,cleanupOtherOwners
 local function init()
  if catalog then return end
  local cat=SPCStandardizationCatalog.Build(P);local rows={}
  for id,b in pairs(cat.buildings) do if b.enabled then
   rows[id]={};for level=1,4 do rows[id][level]=assert(P.Info('Buildings','BUILDING_SPC_B054_'..id..'_'..level),'DISCOUNT_DATABASE_MISSING').Index end
  end end
  catalog,carriers=cat,rows
 end
 local function count(n) if P.Count then P.Count(n) end end
 local function ref(c) return c:GetOwner()..':'..c:GetID()..':'..c:GetX()..':'..c:GetY() end
 local function city(pid,id) local c=Players[pid]:GetCities():FindID(id);assert(c and c:GetOwner()==pid,'DISCOUNT_OWNER_CHANGED');return c end
 local function candidate(pid,c)
  local out={};local groups={};local maxLevel=0;local sourceNames={}
  local ok,ids=pcall(shared.NetworkBridge.RecipientSources,pid,c,'INDUSTRY')
  if not ok then
   local b=shared.NetworkBridge.players and shared.NetworkBridge.players[pid]
   if b and b.validity=='CONFIRMED_INVALID' then return out,sourceNames,0 end
   error(ids)
  end
  for _,id in ipairs(ids) do
   local source=Players[pid]:GetCities():FindID(id)
   -- An absent/transferred source is confirmed loss; unreadable ACTIVE is not.
   if source and source:GetOwner()==pid then
   local f=shared.EffectiveFacts.Read(pid,source)
   assert(type(f.specialization)=='string' and type(f.active)=='number' and f.active>=0 and f.active<=4 and f.active%1==0,'DISCOUNT_SOURCE_UNRESOLVED')
   if f.specialization=='INDUSTRY' and f.active>=1 then
   local ledger=shared.Standardization.ReadLedger(pid,source)
   for building in pairs(ledger.learned) do local b=catalog.buildings[building];assert(b,'DISCOUNT_CLASSIFICATION_CHANGED');groups[b.group]=true end
   maxLevel=math.max(maxLevel,f.active);sourceNames[#sourceNames+1]=tostring(source:GetName())..' ACTIVE '..f.active
   end end
  end
  for id,b in pairs(catalog.buildings) do if b.enabled and groups[b.group] then out[id]=maxLevel end end
  table.sort(sourceNames);return out,sourceNames,maxLevel
 end
 local function reconcile(pid,c,want)
  local key=pid..':'..c:GetID();local b=c:GetBuildings();local old=d.applied[key]
  if not old then
   old={};for id,levels in pairs(carriers) do for level,index in pairs(levels) do if P.HasBuilding(b,index) then old[index]=true end end end
   d.applied[key]=old
  end
  local needed={};for id,level in pairs(want) do needed[carriers[id][level]]=true end
  for index in pairs(old) do if not needed[index] then
   P.RemoveBuilding(b,index);count('discount_withdraw');assert(not P.HasBuilding(b,index),'DISCOUNT_REMOVE_UNCONFIRMED');old[index]=nil;d.changes=d.changes+1
  end end
  for index in pairs(needed) do if not P.HasBuilding(b,index) then
   P.CreateBuilding(c:GetBuildQueue(),index);assert(P.HasBuilding(b,index),'DISCOUNT_ADD_UNCONFIRMED');d.changes=d.changes+1
  end;old[index]=true end
 end
 -- One bounded acknowledgement per player; stale clients cannot replace it.
 local function clientValid(p)
  local issued=ExposedMembers.SPC_DiscountIssued
  return issued and type(p)=='table' and issued.ClientEpoch==p.ClientEpoch and issued.Seq==p.Seq and issued.Generation==p.Generation and type(p.ClientEpoch)=='number'
   and p.ClientEpoch==ExposedMembers.SPC_DiscountClientEpoch
   and type(p.Seq)=='number' and p.Seq>=1 and p.Seq%1==0
 end
 local function respond(pid,p,status)
  d.responses[pid]={ClientEpoch=p.ClientEpoch,Seq=p.Seq,Generation=p.Generation,Status=status}
 end
 function d.Initialize(pid,p)
  count('discount_receive')
  if not P.IsTestPlayer(pid) or not clientValid(p) or p.Generation~=d.generation then count('discount_stale');return end
  local old=d.responses[pid]
  if old and old.ClientEpoch==p.ClientEpoch and old.Seq>=p.Seq then count('discount_duplicate');return end
  d.EnsureReady(pid);respond(pid,p,'INITIALIZED')
 end
 function d.EnsureReady(pid)
  if not P.IsTestPlayer(pid) then return end
  if not d.ready then
   d.ready=true;d.generation=d.generation+1;d.samples={};d.seq={};d.applied={}
   if cleanupOtherOwners then cleanupOtherOwners() end
  end
  d.Audit()
 end
 function d.Audit() P.Count('audit_standard');
  if not d.ready or d.busy then P.Count('busy_skip');return end;d.busy=true
  local success,why=pcall(function()
   init()
   for pid,p in pairs(Players) do if P.IsTestPlayer(pid) then
    local targets,info,parts,refs={},{},{},{};local previous=d.plans[pid]
    for _,c in p:GetCities():Members() do P.Count('city_scan');
     local id=c:GetID();local ok,t,names,level=pcall(candidate,pid,c)
     refs[id]=ref(c)
     targets[id]=ok and t or (previous and previous.refs[id]==refs[id] and previous.targets[id] or {})
     local lastInfo=previous and previous.refs[id]==refs[id] and previous.info[id]
     info[id]={sources=ok and names or (lastInfo and lastInfo.sources or {}),level=ok and level or (lastInfo and lastInfo.level or 0),reason=not ok and tostring(t) or nil}
     parts[#parts+1]='C'..id..':'..c:GetX()..':'..c:GetY()
     for building,l in pairs(targets[id]) do parts[#parts+1]=id..':'..building..':'..l end
    end
    table.sort(parts);local sig=table.concat(parts,';');
    if not previous or previous.signature~=sig then
     d.plans[pid]={revision=previous and previous.revision+1 or 1,signature=sig,targets=targets,info=info,refs=refs}
    else previous.info=info end
    local sample=d.samples[pid];local current=sample~=nil
    if sample then
     -- Confirmed plan/reference loss permanently retires that permission observation.
     -- A later reappearance must obtain a fresh native permission sample.
     for cid,allowed in pairs(sample.rows) do
      if refs[cid]~=sample.refs[cid] then sample.rows[cid]=nil;sample.refs[cid]=nil;sample.signature=nil
      elseif not info[cid].reason then
       for id in pairs(allowed) do if not (targets[cid] or {})[id] then allowed[id]=nil;sample.signature=nil end end
      end
     end
    end
    for _,c in p:GetCities():Members() do P.Count('city_scan');
     local want={};local id=c:GetID()
     if current and sample.refs[id]==refs[id] then for building,l in pairs(targets[id]) do if (sample.rows[id] or {})[building] then want[building]=l end end end
     local held=d.holdLoaded and not sample and info[id].reason~=nil
     if d.holdLoaded and not sample and not held then
      -- Loaded carriers are a temporary projection, never restored sample authority.
      -- Keep only already-present, still-planned entries; confirmed removals still withdraw.
      for building,l in pairs(targets[id]) do
       for _,index in pairs(carriers[building]) do
        if P.HasBuilding(c:GetBuildings(),index) then want[building]=l;break end
       end
      end
     end
     local ok,err=true,nil;if not held then ok,err=pcall(reconcile,pid,c,want) end
     local key=pid..':'..id;local reason=not ok and tostring(err) or info[id].reason
     if reason and reason~=d.errors[key] then print('[SPC][B054][CITY] '..key..' '..reason) end
     d.errors[key]=reason
    end
   end end
  end)
  if not success then d.globalError=tostring(why);print('[SPC][B054] '..tostring(why)) else d.globalError=nil end
  d.busy=false
 end
 function d.Receive(pid,p)
  count('discount_receive')
  if not d.ready or not P.IsTestPlayer(pid) or not clientValid(p) or p.Generation~=d.generation then count('discount_stale');return end
  local ack=d.responses[pid]
  if ack and ack.ClientEpoch==p.ClientEpoch and p.Seq<=ack.Seq then count('discount_duplicate');return end
  -- Still performs the existing pre-Audit. D1 owns its scan cost.
  d.Audit()
  local plan=d.plans[pid]
  if not plan or p.Revision~=plan.revision or p.Turn~=Game.GetCurrentGameTurn() then
   count('discount_stale');respond(pid,p,'STALE');return
  end
  if p.Valid~=1 then respond(pid,p,'UNAVAILABLE');return end
  local rows,refs,canonical={},{},{}
  local ok,err=pcall(function()
   assert(type(p.Data)=='string' and #p.Data<=60000,'DISCOUNT_SAMPLE_SIZE')
   local n=0
   for line in p.Data:gmatch('[^;]+') do
    local cid,index,value=line:match('^(%d+),(%d+),([01])$');cid,index=tonumber(cid),tonumber(index)
    local b=index and P.Info('Buildings',index);assert(b and plan.targets[cid] and plan.targets[cid][b.BuildingType],'DISCOUNT_SAMPLE_TARGET')
    local c=city(pid,cid);assert(ref(c)==plan.refs[cid],'DISCOUNT_SAMPLE_REFERENCE')
    refs[cid]=ref(c);rows[cid]=rows[cid] or {};assert(rows[cid][b.BuildingType]==nil,'DISCOUNT_SAMPLE_DUPLICATE')
    rows[cid][b.BuildingType]=value=='1';n=n+1
    canonical[#canonical+1]=cid..':'..refs[cid]..':'..b.BuildingType..':'..value
   end
   assert(n==p.Count,'DISCOUNT_SAMPLE_PARTIAL')
   for cid,buildings in pairs(plan.targets) do for id in pairs(buildings) do assert(rows[cid] and rows[cid][id]~=nil,'DISCOUNT_SAMPLE_PARTIAL') end end
   table.sort(canonical)
  end)
  if not ok then d.receiveError=tostring(err);respond(pid,p,'UNAVAILABLE');return end
  local signature=table.concat(canonical,';');local old=d.samples[pid]
  d.seq[pid]=p.Seq;d.receiveError=nil
  if old and old.signature==signature then
   old.turn=p.Turn;old.revision=p.Revision;respond(pid,p,'UNCHANGED');count('discount_duplicate');return
  end
  -- Validate the entire replacement before publishing it. False rows are confirmed loss.
  d.samples[pid]={revision=p.Revision,turn=p.Turn,rows=rows,refs=refs,signature=signature}
  d.appliedSamples=d.appliedSamples+1;count('discount_apply');respond(pid,p,'ACCEPTED');d.Audit()
 end
 function d.Describe(pid,c,page)
  local plan=d.plans[pid];if not plan then return 'B054.71：后台折扣尚未初始化。ready='..tostring(d.ready)..' busy='..tostring(d.busy)..' generation='..d.generation..(d.globalError and (' 状态='..(d.globalError:match('DISCOUNT_[A-Z_]+') or 'ERROR')) or '') end
  local info=plan.info[c:GetID()];local targets=plan.targets[c:GetID()] or {};local ids={};for id in pairs(targets) do ids[#ids+1]=id end;table.sort(ids)
  local sample=d.samples[pid];local current=sample and sample.turn==Game.GetCurrentGameTurn() and sample.revision==plan.revision
  local pages=math.max(1,math.ceil(#ids/5));page=(math.max(1,tonumber(page) or 1)-1)%pages+1
  local lines={'B054.71标准化折扣 | '..c:GetName()..' | city='..c:GetID(),'有效来源：'..table.concat(info and info.sources or {},' / '),'最高折扣='..((info and info.level or 0)*10)..'% | 匹配建筑='..#ids..' | 页 '..page..'/'..pages,'后台金币资格='..(current and '已读取' or '待刷新')..' | 本次加载载体变更='..d.changes}
  for i=(page-1)*5+1,math.min(page*5,#ids) do
   local id=ids[i];local applied=d.applied[pid..':'..c:GetID()] or {};local index=carriers[id][targets[id]]
   lines[#lines+1]=Locale.Lookup(catalog.buildings[id].name)..' | 配置='..(applied[index] and targets[id]*10 or 0)..'%'
  end
  local err=d.errors[pid..':'..c:GetID()] or d.globalError or d.receiveError
  if err then lines[#lines+1]='状态='..(tostring(err):match('DISCOUNT_[A-Z_]+') or '来源/后台待更新') end
  lines[#lines+1]='只读；原生价格以购买页为准，允许同一合格建筑双币折扣。'
  return table.concat(lines,'\n')
 end
 local function hook(n,f) local e=P.Field(Events,n);if e and e.Add then e.Add(f) end end
 cleanupOtherOwners=function()
  local ok,err=pcall(function() init();for pid,p in pairs(Players) do if not P.IsTestPlayer(pid) then for _,c in p:GetCities():Members() do P.Count('city_scan'); reconcile(pid,c,{}) end end end end)
  if not ok then print('[SPC][B054][CLEANUP] '..tostring(err)) end
 end
 hook('LoadScreenClose',function() d.ready=true;d.generation=d.generation+1;d.samples={};d.seq={};d.responses={};d.plans={};d.applied={};d.holdLoaded=true;cleanupOtherOwners();d.Audit() end)
 hook('CityTransfered',function() d.applied={};cleanupOtherOwners();d.Audit() end)
 for _,n in ipairs({'GameCoreEventPublishComplete','PlayerTurnActivated','GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged'}) do hook(n,d.Audit) end
end
