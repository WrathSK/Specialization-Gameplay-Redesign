-- B052: persistent building knowledge. No Gold/Faith price or unlock modification.
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
 local function validate(c,v)
  assert(type(v)=='table' and v.schema==1 and v.initialized==true and type(v.uid)=='string' and type(v.foundation)=='string','STD_LEDGER_INVALID')
  assert(v.x==c:GetX() and v.y==c:GetY(),'STD_LOCATION_CONFLICT')
  assert(type(v.learned)=='table' and type(v.revision)=='number','STD_LEDGER_INVALID')
  local count=0
  for id,row in pairs(v.learned) do
   assert(type(id)=='string' and type(row)=='table' and type(row.district)=='string' and type(row.tier)=='number' and type(row.turn)=='number' and type(row.evidence)=='string','STD_RECEIPT_INVALID')
   local current=catalog().buildings[id]
   assert(current and current.district==row.district and current.tier==row.tier,'STD_CATALOG_MIGRATION_REQUIRED')
   count=count+1
  end
  assert(v.revision==count+1,'STD_REVISION_CONFLICT');return v
 end
 local function write(c,old,nextValue)
  assert(same(c:GetProperty(KEY),old),'STD_CONCURRENT_CHANGE')
  P.SetProperty(c,KEY,nextValue)
  assert(same(c:GetProperty(KEY),nextValue),'STD_WRITE_UNCONFIRMED')
  if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'Standardization.lua') end
  data.writes=data.writes+1
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
   assert(prior.district==row.district and prior.tier==row.tier,'STD_CATALOG_MIGRATION_REQUIRED');return false
  end
  v.learned[id]={district=row.district,tier=row.tier,turn=Game.GetCurrentGameTurn(),evidence=evidence}
  v.revision=v.revision+1;return true
 end
 local function initialize(pid,c)
  local old=c:GetProperty(KEY)
  if old~=nil then validate(c,old);return false end
  local f=facts(pid,c);if f.specialization~='INDUSTRY' then return false end
  assert(type(f.token)=='string','STD_FOUNDATION_MISSING')
  local nextValue={schema=1,uid='STD:'..f.token,foundation=f.token,x=c:GetX(),y=c:GetY(),initialized=true,revision=1,learned={}}
  data.scans=data.scans+1
  for id in pairs(catalog().buildings) do learn(c,nextValue,id,'INITIAL_BACKFILL') end
  write(c,nil,nextValue);data.last[key(pid,c:GetID())]='首次补录完成';return true
 end
 local function guard(pid,c,fn)
  local k=key(pid,c:GetID());local ok,err=pcall(fn)
  if not ok then
   local code=tostring(err):match('STD_[A-Z_]+') or 'STD_FACTS_NOT_READY'
   if data.errors[k]~=code then print('[SPC][B052] '..k..' '..tostring(err)) end
   data.errors[k]=code
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
     local old=validate(c,c:GetProperty(KEY));assert(old.foundation==f.token,'STD_FOUNDATION_CHANGED')
     local nextValue=clone(old);local changed=false
     for id,e in pairs(q.buildings) do
      local row=catalog().buildings[id]
      if row and P.HasBuilding(c:GetBuildings(),row.index) then
       if learn(c,nextValue,id,e.evidence) then changed=true;data.last[k]=id end
      else retry(id,e) end
     end
     if changed then write(c,old,nextValue) end
    end)
    -- Unknown facts are retained for bounded retries; never guess or erase old knowledge.
    if not ok then for id,e in pairs(q.buildings) do retry(id,e) end end
    q.buildings=keep;if next(keep)==nil then data.pending[k]=nil end
   end
  end
  data.busy=false
 end
 function data.ReadLedger(pid,c)
  local f=facts(pid,c);assert(f.specialization=='INDUSTRY','STD_SOURCE_CHANGED')
  local v=validate(c,c:GetProperty(KEY));assert(v.foundation==f.token,'STD_FOUNDATION_CHANGED')
  return clone(v)
 end
 function data.Describe(pid,c,page)
  local ok,text=pcall(function()
   assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'STD_OWNER_CHANGED')
   local v=c:GetProperty(KEY);local cat=catalog();local lines={'B052 标准化模板 | '..tostring(c:GetName())..' | city='..c:GetID()}
   if v==nil then lines[#lines+1]='尚无账本：非工业专业或后台初始化尚未完成。'
   else
    validate(c,v);local ids={};local enabled=0
    for id in pairs(v.learned) do ids[#ids+1]=id;if cat.buildings[id] and cat.buildings[id].enabled then enabled=enabled+1 end end;table.sort(ids)
    local pages=math.max(1,math.ceil(#ids/5));page=(math.max(1,tonumber(page) or 1)-1)%pages+1
    lines[#lines+1]='已初始化 | 模板='..#ids..' | revision='..v.revision..' | 页 '..page..'/'..pages
    lines[#lines+1]='折扣范围内='..enabled..' | 仅保留='..(#ids-enabled)..'（不代表当前可金币购买）'
    for i=(page-1)*5+1,math.min(page*5,#ids) do
     local id=ids[i];local row=cat.buildings[id];local receipt=v.learned[id]
     local label=row and row.name or id;if Locale and Locale.Lookup then label=Locale.Lookup(label) end
     lines[#lines+1]=label..' | T'..receipt.tier..' | '..(row and row.group or '需分类迁移')
    end
   end
   lines[#lines+1]='本次加载：首次扫描='..data.scans..' / 写入='..data.writes
   lines[#lines+1]='最近记录='..tostring(data.last[key(pid,c:GetID())] or '无新增')
   lines[#lines+1]='状态='..tostring(data.errors[key(pid,c:GetID())] or data.warnings[key(pid,c:GetID())] or '正常')
   lines[#lines+1]='只读永久模板；当前折扣另见Read discounts。'
   return table.concat(lines,'\n')
  end)
  return ok and text or ('B052 读取未完成：'..(tostring(text):match('STD_[A-Z_]+') or 'STD_READ_FAILED'))
 end
 local function hook(src,n,fn)
  local ev=P.Field(src,n);if ev and ev.Add then ev.Add(fn);data.hooks[n]=true end
 end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.Discover();data.Flush() end)
 hook(Events,'PlayerTurnActivated',function(pid) data.Discover(pid);data.Flush() end)
 hook(GameEvents,'OnDistrictConstructed',function(pid) data.Discover(pid);data.Flush() end)
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
 hook(Events,'GameCoreEventPublishComplete',data.Flush)
end
