-- B233: retained building knowledge plus typed District experience. No new effects.
SPCStandardization={KEY='SPC_STANDARDIZATION_LEDGER_V1'}
function SPCStandardization.Start(P,shared)
 local KEY=SPCStandardization.KEY
 local data={ready=false,busy=false,errors={},writes=0,scans=0,pending={},hooks={},last={},warnings={}};shared.Standardization=data
 local function clone(t) if type(t)~='table' then return t end;local o={};for k,v in pairs(t) do o[k]=clone(v) end;return o end
 local function same(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a) do if not same(v,b[k]) then return false end end
  for k in pairs(b) do if a[k]==nil then return false end end;return true
 end
 local function key(pid,cid) return tostring(pid)..':'..tostring(cid) end
 local function catalog()
  if not data.catalog then data.catalog=SPCStandardizationCatalog.Build(P) end
  return data.catalog
 end
 local function history(c,v)
  return SPCCityIdentityRead.ValidateTemplates(v,v and v.foundation,c:GetX(),c:GetY())
 end
 local function validate(c,v)
  history(c,v)
  for id,row in pairs(v.learned)do
   local current=catalog().buildings[id]
   assert(current and current.district==row.district and current.tier==row.tier,'STD_CATALOG_MIGRATION_REQUIRED')
  end
  return v
 end
 data.ValidateHistory=history -- Store recovery checks provenance, not effect availability.
 data.ValidateRetained=validate -- Legacy effect consumer retains its stricter boundary.
 local trace=SPCExpeditionTrainingDiagnostics and SPCExpeditionTrainingDiagnostics.New(P,'INDUSTRY_TEMPLATES')
 local function log(stage,c,v,reason)
  if not trace then return end
  local buildings,districts=0,0
  if v then
   for _ in pairs(v.learned)do buildings=buildings+1 end
   if v.districts then for _ in pairs(v.districts.learned)do districts=districts+1 end end
  end
  trace.Record(stage,{owner=c:GetOwner(),city=c:GetID(),templateCount=buildings,districtTemplateCount=districts,
   historyRevision=v and v.revision or 0,readStatus=v and v.districts and v.districts.coverage or 'UNAVAILABLE',reason=reason or 'OK'})
 end
 local function read(c)
  local store=shared.CityProgressionStore
  if store and (store.UsesNewAuthority or store.Owns(c))then return store.ReadTemplates(c)end
  return c:GetProperty(KEY)
 end
 local function write(c,old,nextValue)
  assert(same(read(c),old),'STD_CONCURRENT_CHANGE')
  local store=shared.CityProgressionStore
  if store and (store.UsesNewAuthority or store.Owns(c))then store.WriteTemplates(c,old,nextValue)else P.SetProperty(c,KEY,nextValue)end
  assert(same(read(c),nextValue),'STD_WRITE_UNCONFIRMED')
  if not same(old,nextValue) and shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'Standardization.lua') end
  data.writes=data.writes+1
  if not same(old,nextValue) then
   log('INDUSTRY_TEMPLATES_COMMITTED',c,nextValue)
   if shared.StandardizationDiscount and not same(old and old.learned,nextValue.learned) then shared.StandardizationDiscount.MarkDirty(c:GetOwner(),'template') end
  end
 end
 local function facts(pid,c)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'STD_OWNER_CHANGED')
  return shared.EffectiveFacts.Read(pid,c)
 end
 local function learn(c,v,id,evidence)
  local row=catalog().buildings[id];if not row then return false end
  if not P.HasBuilding(c:GetBuildings(),row.index) then return false end
  local prior=v.learned[id]
  if prior then
   return false -- Preserve historical classification; never remap it to today's catalog.
  end
  v.learned[id]={district=row.district,tier=row.tier,turn=Game.GetCurrentGameTurn(),evidence=evidence}
  v.revision=v.revision+1;return true
 end
 local function learnDistrict(c,v,district,evidence)
  assert(district and district:GetOwner()==c:GetOwner(),'STD_DISTRICT_OWNER_CHANGED')
  local city=district:GetCity()
  assert(city and city:GetOwner()==c:GetOwner() and city:GetID()==c:GetID()
   and city:GetX()==c:GetX() and city:GetY()==c:GetY(),'STD_DISTRICT_CITY_CHANGED')
  local complete=district:IsComplete();assert(type(complete)=='boolean','STD_DISTRICT_COMPLETENESS_UNKNOWN')
  if not complete then return false end
  local info=assert(P.Info('Districts',district:GetType()),'STD_DISTRICT_TYPE_UNAVAILABLE')
  local row=assert(catalog().districts,'STD_DISTRICT_CATALOG_UNAVAILABLE')[info.DistrictType]
  if not row or v.districts.learned[row.base] then return false end
  v.districts.learned[row.base]={observedType=info.DistrictType,turn=Game.GetCurrentGameTurn(),evidence=evidence,policy='D0045'}
  v.districts.revision=v.districts.revision+1;return true
 end
 local function scanDistricts(c,v,evidence)
  local list=assert(c:GetDistricts(),'STD_DISTRICT_COLLECTION_UNAVAILABLE')
  local n=list:GetNumDistricts()
  assert(type(n)=='number' and n>=0 and n%1==0,'STD_DISTRICT_COUNT_UNAVAILABLE')
  for i=0,n-1 do learnDistrict(c,v,assert(list:GetDistrictByIndex(i),'STD_DISTRICT_ENTRY_UNAVAILABLE'),evidence)end
 end
 local function initialize(pid,c)
  local old,pending=read(c)
  if old~=nil then history(c,old)end
  local h=shared.IndustryHistory;local needs=false
  if h then local ok,value=pcall(h.NeedsReconcile,c);needs=not ok or value end
  if old and not pending and old.districts and not needs then return false end
  local f=facts(pid,c);if f.specialization~='INDUSTRY' then return false end
  if h then
   local ok,err=pcall(h.Reconcile,pid,c)
   local k=key(pid,c:GetID())
   if not ok then
    local reason=tostring(err):match('IH_[A-Z_]+') or 'IH_RECONCILIATION_UNAVAILABLE'
    if data.warnings[k]~=reason then log('INDUSTRY_WONDER_RECONCILE_HELD',c,nil,reason)end
    data.warnings[k]=reason -- Wonder history failure does not suspend ordinary templates.
   elseif data.warnings[k] and data.warnings[k]:match('^IH_')then data.warnings[k]=nil end
  end
  if old and not pending and old.districts then return false end
  assert(type(f.token)=='string','STD_FOUNDATION_MISSING')
  if old then assert(old.foundation==f.token,'STD_FOUNDATION_CHANGED')end
  local nextValue=old and clone(old) or {schema=1,uid='STD:'..f.token,foundation=f.token,x=c:GetX(),y=c:GetY(),initialized=true,revision=1,learned={}}
  if not nextValue.districts then
   nextValue.knowledgeVersion=1
   nextValue.districts={version=1,policy='D0045',initialized=true,initializedTurn=Game.GetCurrentGameTurn(),
    coverage=old and 'PRESENT_AT_ADOPTION' or 'FROM_IDENTITY',revision=1,learned={}}
  end
  data.scans=data.scans+1
  for id in pairs(catalog().buildings) do learn(c,nextValue,id,old and 'REENTRY_PRESENT' or 'INITIAL_BACKFILL') end
  scanDistricts(c,nextValue,old and 'REENTRY_PRESENT' or 'INITIAL_BACKFILL')
  write(c,old,nextValue);data.last[key(pid,c:GetID())]=old and '当前建筑/区域同步完成；保留历史模板' or '首次模板初始化完成';return true
 end
 local function guard(pid,c,fn)
  local k=key(pid,c:GetID());local ok,err=pcall(fn)
  if not ok then
   local code=tostring(err):match('STD_[A-Z_]+') or tostring(err):match('TEMPLATES_[A-Z_]+') or tostring(err):match('STORE_[A-Z_]+') or 'STD_FACTS_NOT_READY'
   if data.errors[k]~=code then print('[SPC][B052] '..k..' '..tostring(err)) end
   data.errors[k]=code;log('INDUSTRY_TEMPLATES_HELD',c,nil,code)
  else data.errors[k]=nil end
  return ok
 end
 function data.Discover(pid)
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true
  for id,player in pairs(Players) do if (pid==nil or pid==id) and P.IsTestPlayer(id) then
   for _,c in player:GetCities():Members() do P.Count('city_scan'); guard(id,c,function() initialize(id,c) end) end
  end end
  data.busy=false
 end
 function data.Queue(pid,cid,bid,event)
  if type(pid)~='number' or not P.IsTestPlayer(pid) then return end
  local b=P.Info('Buildings',bid);if not b then return end
  local ok,cat=pcall(catalog);if not ok then print('[SPC][B052] '..tostring(cat));return end
  if not cat.buildings[b.BuildingType] then return end
  if type(cid)~='number' then return end
  local k=key(pid,cid);data.pending[k]=data.pending[k] or {pid=pid,cid=cid,buildings={}}
  data.pending[k].buildings[b.BuildingType]=data.pending[k].buildings[b.BuildingType] or {evidence=event,turn=Game.GetCurrentGameTurn()}
 end
 local function queueReconcile(pid,cid)
  if type(pid)~='number' or not P.IsTestPlayer(pid) or type(cid)~='number' then return end
  local k=key(pid,cid);local q=data.pending[k] or {pid=pid,cid=cid,buildings={}}
  q.reconcile=true;q.turn=Game.GetCurrentGameTurn();data.pending[k]=q
 end
 function data.Flush()
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true
  for k,q in pairs(data.pending) do
   local player=Players[q.pid];local c=player and player:GetCities():FindID(q.cid)
   if not c or c:GetOwner()~=q.pid or not P.IsTestPlayer(q.pid) then data.pending[k]=nil
   else
    local keep={}
    local function retry(id,e)
     -- Recheck only the signalled building; allow delayed acquisition until two turns later.
     if Game.GetCurrentGameTurn()<=e.turn+2 then keep[id]=e
     elseif e.evidence~='BUILDING_ADDED_RECHECK' then
      data.warnings[k]='STD_EVENT_EXPIRED: '..id
      print('[SPC][B052] '..k..' '..data.warnings[k])
     end
    end
    local ok=guard(q.pid,c,function()
     local f=facts(q.pid,c)
     if f.specialization~='INDUSTRY' then return end
     initialize(q.pid,c)
     local old=history(c,read(c));assert(old.foundation==f.token,'STD_FOUNDATION_CHANGED')
     local nextValue=clone(old);local changed=false
     for id,e in pairs(q.buildings) do
      local row=catalog().buildings[id]
      if row and P.HasBuilding(c:GetBuildings(),row.index) then
       if learn(c,nextValue,id,e.evidence) then changed=true;data.last[k]=id end
      else retry(id,e) end
     end
     for _,e in pairs(q.districts or {})do
      local district=CityManager.GetDistrictAt(e.x,e.y)
      assert(district and district:GetType()==e.index,'STD_DISTRICT_EVENT_CHANGED')
      if learnDistrict(c,nextValue,district,'DISTRICT_COMPLETED')then changed=true end
     end
     if changed then write(c,old,nextValue) end
    end)
    -- Unknown facts are retained for bounded retries; never guess or erase old knowledge.
    if not ok then for id,e in pairs(q.buildings) do retry(id,e) end end
    if not ok and q.districts then q.reconcile=true end
    q.reconcile=q.reconcile and not ok and Game.GetCurrentGameTurn()<=q.turn+2
    q.buildings=keep;if ok then q.districts=nil end;if not q.reconcile and next(keep)==nil then data.pending[k]=nil end
   end
  end
  data.busy=false
 end
 function data.ReadLedger(pid,c)
  local f=facts(pid,c);assert(f.specialization=='INDUSTRY','STD_SOURCE_CHANGED')
  local value,pending=read(c);assert(not pending,'STD_RECONCILIATION_PENDING')
  local v=validate(c,value);assert(v.foundation==f.token,'STD_FOUNDATION_CHANGED')
  return clone(v)
 end
 function data.Describe(pid,c,page)
  local ok,text=pcall(function()
   assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'STD_OWNER_CHANGED')
   local v,pending=read(c);local cat=catalog();local lines={'标准化模板 | '..tostring(c:GetName())}
   if v==nil then lines[#lines+1]='尚无账本：非工业专业或后台初始化尚未完成。'
   else
    history(c,v);local ids={};local enabled=0
    for id in pairs(v.learned) do ids[#ids+1]=id;if cat.buildings[id] and cat.buildings[id].enabled then enabled=enabled+1 end end;table.sort(ids)
    local pages=math.max(1,math.ceil(#ids/5));page=(math.max(1,tonumber(page) or 1)-1)%pages+1
    lines[#lines+1]='已初始化 | 模板='..#ids..' | revision='..v.revision..' | 页 '..page..'/'..pages
    lines[#lines+1]='建筑模板：当前目录内 '..enabled..' / 仅保留 '..(#ids-enabled)..'（不是购买资格或新效果）'
    for i=(page-1)*5+1,math.min(page*5,#ids) do
     local id=ids[i];local row=cat.buildings[id];local receipt=v.learned[id]
     local label=row and row.name or id;if Locale and Locale.Lookup then label=Locale.Lookup(label) end
     lines[#lines+1]=label..' | T'..receipt.tier..' | '..(row and row.group or '需分类迁移')
    end
   end
   if v then
    if v.districts then
     local names={}
     for id in pairs(v.districts.learned)do
      local row=P.Info('Districts',id);local name=row and row.Name or id
      names[#names+1]=Locale and Locale.Lookup and Locale.Lookup(name) or name
     end
     table.sort(names);lines[#lines+1]='区域模板：'..#names..' | '..(#names>0 and table.concat(names,'、') or '已初始化空集合')
     if v.districts.coverage=='PRESENT_AT_ADOPTION'then lines[#lines+1]='区域记录从本次接入开始；未补造此前已消失的区域。'end
    else lines[#lines+1]='区域模板：尚未建立，不能视为已知零。'end
    log('INDUSTRY_TEMPLATES_REPORT',c,v)
   end
   if pending then lines[#lines+1]='当前建筑/区域同步待完成；历史模板保留。'end
   lines[#lines+1]='本次加载：模板同步扫描='..data.scans..' / 写入='..data.writes
   lines[#lines+1]='最近记录='..tostring(data.last[key(pid,c:GetID())] or '无新增')
   lines[#lines+1]='状态='..tostring(data.errors[key(pid,c:GetID())] or data.warnings[key(pid,c:GetID())] or '正常')
   lines[#lines+1]='仅记录模板；本批没有新增标准化收益。'
   return table.concat(lines,'\n')
  end)
  if ok then return text end
  local reason=tostring(text):match('STD_[A-Z_]+') or tostring(text):match('TEMPLATES_[A-Z_]+') or tostring(text):match('STORE_[A-Z_]+') or 'STD_READ_FAILED'
  log('INDUSTRY_TEMPLATES_REPORT',c,nil,reason)
  return '模板读取未完成：'..reason
 end
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterReturn('Standardization',function(pid,c)
  data.pending[key(pid,c:GetID())]=nil;queueReconcile(pid,c:GetID()) -- callback precedes return commit; no reads/writes here
 end)end
 local function hook(src,n,fn)
  local ev=P.Field(src,n);if ev and ev.Add then ev.Add(fn);data.hooks[n]=true end
 end
 local started=false
 local function startReady()
  if started then return end
  local store=shared.CityProgressionStore
  if store and store.HistoryStartStatus and store.HistoryStartStatus()=='WAITING'then return end
  started=true;data.ready=true;data.Discover();data.Flush()
 end
 hook(Events,'LoadScreenClose',startReady)
 hook(Events,'PlayerTurnActivated',function(pid) data.Discover(pid);data.Flush() end)
 hook(GameEvents,'OnDistrictConstructed',function(pid,index,x,y)
  startReady()
  if not P.IsTestPlayer(pid)then return end
  local district=CityManager.GetDistrictAt(x,y);local c=district and district:GetCity()
  if not c or c:GetOwner()~=pid or district:GetType()~=index then return end
  local k=key(pid,c:GetID());queueReconcile(pid,c:GetID())
  data.pending[k].districts=data.pending[k].districts or {}
  data.pending[k].districts[tostring(index)..':'..x..':'..y]={index=index,x=x,y=y}
  data.Flush()
 end)
 for _,name in ipairs({'BuildingConstructed','OnBuildingConstructed'}) do
  hook(GameEvents,name,function(pid,cid,bid) data.Queue(pid,cid,bid,name);data.Flush() end)
 end
 -- HD RegionalYields.lua uses x,y,buildingId,playerId. Recheck this building only.
 hook(Events,'BuildingAddedToMap',function(x,y,bid,pid)
  if type(pid)~='number' or not P.IsTestPlayer(pid) then return end
  local b=P.Info('Buildings',bid);local ok,cat=pcall(catalog)
  if not ok or not b or not cat.buildings[b.BuildingType] then return end
  local player=Players[pid];if not player then return end
  for _,c in player:GetCities():Members() do P.Count('city_scan'); data.Queue(pid,c:GetID(),bid,'BUILDING_ADDED_RECHECK') end
  data.Flush()
 end)
 hook(Events,'CityProjectCompleted',function(pid,cid,bid)
  local row=P.Info('Projects',bid)
  if row and row.ProjectType=='PROJECT_SPC_CLAIM_INDUSTRY' then queueReconcile(pid,cid)end
 end)
 hook(Events,'GameCoreEventPublishComplete',function()startReady();data.Flush()end)
 startReady()
end
